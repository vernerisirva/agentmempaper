"""Structural adjudication contract and its bounded recovery. Synthetic only; no network."""
from copy import deepcopy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_promotion_gate import ENV, INDEPENDENT, Models, fixture
from paper_scout.evidence_context import build_evidence_context, digest
from paper_scout.models import ClassificationResult
from paper_scout.promotion_gate import assess_promotion, request_payload, role_settings
from paper_scout.promotion_protocol import (
    ADJUDICATOR_MODEL, INDEPENDENCE_FIELD, RETRY_POLICY, RETRY_POLICIES, ResponseContractError,
    adjudicator_consistency_error, agreement, attempt_binding, canonical_json,
    parse_response, response_binding, schema, validate_receipt, validate_response,
)
from paper_scout.quality_models import QualityAssessment
from paper_scout.site import (
    _load_library_papers, _main_library, _review_candidate, _withheld_scientific_decision,
)
from paper_scout.state import PaperStore

# The exact shape Batch 4 recorded on arxiv:2609.03727: a promotion pass returned
# together with one prose string asserting that nothing blocks promotion.
SENTINEL = ("No blocking reasons: the manuscript's scoped survey contribution, formal decision "
            "framework, critical evaluation protocol, and explicit limitation handling are well "
            "supported by the supplied evidence.")


class ContractModels(Models):
    """Return `contradictions` contradictory adjudications, then consistent ones."""

    def __init__(self, contradictions=1, reason=SENTINEL, **kwargs):
        super().__init__(**kwargs)
        self.contradictions, self.reason, self.adjudications = contradictions, reason, 0
        self.contents = []

    def post_json(self, url, payload, headers):
        envelope = json.loads(super().post_json(url, payload, headers))
        value = json.loads(envelope['choices'][0]['message']['content'])
        if 'promotion_decision' in value:
            self.adjudications += 1
            if self.adjudications <= self.contradictions:
                value.update(promotion_decision='pass', blocking_reasons=[self.reason])
        content = json.dumps(value, ensure_ascii=False)
        self.contents.append(content)
        envelope['choices'][0]['message']['content'] = content
        return json.dumps(envelope, ensure_ascii=False)


class ContractTests(unittest.TestCase):
    def run_gate(self, models):
        candidate, _, text, seed = fixture()
        with patch.dict('os.environ', ENV, clear=True):
            return assess_promotion(candidate, text, seed, 'llm', http=models)

    def adjudication(self, decision, reasons):
        _, _, text, seed = fixture()
        context = build_evidence_context(seed.canonical_id, text)
        return {'canonical_id': context.canonical_id, 'source_content_hash': context.source_hash,
                'context_id': context.context_id,
                'evidence_ids': [context.blocks[0].evidence_id],
                'promotion_decision': decision, 'blocking_reasons': reasons,
                INDEPENDENCE_FIELD: dict(INDEPENDENT)}, context

    def test_only_a_pass_with_blocking_reasons_violates_the_contract(self):
        cases = [('pass', [], None), ('pass', [SENTINEL], 'consistency'),
                 ('pass', ['Unsupported central claim.'], 'consistency'),
                 ('uncertain', ['Unsupported central claim.'], None),
                 ('uncertain', [SENTINEL], None), ('uncertain', [], None)]
        for decision, reasons, expected in cases:
            with self.subTest(decision=decision, reasons=len(reasons)):
                value, context = self.adjudication(decision, reasons)
                self.assertEqual(adjudicator_consistency_error(value), expected)
                # The schema and the identity contract are unchanged by consistency:
                # a contradictory response is still schema-valid, which is why nothing
                # detected it before and why runtime validation has to.
                accepted = dict(value)
                self.assertIs(validate_response(accepted, 'adjudicator', context), accepted)
                raw = json.dumps(value)
                if expected is None:
                    self.assertEqual(parse_response(raw, 'adjudicator', context), value)
                else:
                    with self.assertRaises(ResponseContractError) as raised:
                        parse_response(raw, 'adjudicator', context)
                    self.assertEqual(raised.exception.reason, expected)
                # A receipt written before the contract is reread under its own policy.
                self.assertEqual(parse_response(raw, 'adjudicator', context, consistency=False), value)

    def test_the_contract_is_structural_and_reads_no_prose(self):
        # Identical decision/array shapes must agree whatever the reasons say, so no
        # wording — a "none" sentinel or a real concern — can change the outcome.
        for reason in (SENTINEL, 'None', 'No issues found.', 'The evaluation omits a baseline.'):
            with self.subTest(reason=reason[:20]):
                passed, _ = self.adjudication('pass', [reason])
                uncertain, _ = self.adjudication('uncertain', [reason])
                self.assertEqual(adjudicator_consistency_error(passed), 'consistency')
                self.assertIsNone(adjudicator_consistency_error(uncertain))

    def test_the_invariant_is_stated_in_the_schema_and_both_instructions(self):
        properties = schema('adjudicator')['properties']
        self.assertIn('blocking_reasons is empty', properties['promotion_decision']['description'])
        self.assertIn('Empty array', properties['blocking_reasons']['description'])
        # The adjudication invariant is stated only where it applies: none of the
        # primary's own fields carries a description, and the shared evaluation
        # independence dimension is byte-identical for both roles.
        primary = dict(schema('primary')['properties'])
        self.assertEqual(primary.pop(INDEPENDENCE_FIELD),
                         schema('adjudicator')['properties'][INDEPENDENCE_FIELD])
        self.assertNotIn('description', json.dumps(primary))
        _, _, text, seed = fixture()
        context = build_evidence_context(seed.canonical_id, text)
        with patch.dict('os.environ', ENV, clear=True):
            settings = role_settings(ADJUDICATOR_MODEL)
        for retry in (False, True):
            payload = request_payload('adjudicator', settings, context, text.coverage,
                                      {'decision': 'pass'}, retry=retry)
            instruction = payload['messages'][0]['content']
            self.assertIn('blocking_reasons', instruction)
            self.assertIn('cannot be pass', instruction)
            self.assertEqual(payload['response_format']['json_schema']['schema'], schema('adjudicator'))

    def test_one_contradictory_adjudication_costs_exactly_one_fresh_retry(self):
        models = ContractModels(contradictions=1)
        result = self.run_gate(models)
        calls = result.execution['calls']
        self.assertEqual([(c['kind'], c['attempt'], c['status']) for c in calls],
                         [('primary', 1, 'success'), ('adjudicator', 1, 'contract_failure'),
                          ('adjudicator', 2, 'success')])
        self.assertEqual(calls[1]['contract_error'], 'consistency')
        self.assertEqual(result.execution['outcome'], 'success')
        self.assertEqual(result.quality_status, 'pass')
        self.assertEqual(result.concerns, [])
        # The retry is a fresh adjudication of the original inputs: the rejected output
        # is never fed back, and the user message is byte-identical to the first attempt.
        self.assertEqual(len(models.payloads), 3)
        self.assertEqual(models.payloads[1]['messages'][1], models.payloads[2]['messages'][1])
        self.assertNotIn(SENTINEL, json.dumps(models.payloads[2]))
        validate_receipt(result)

    def test_a_second_contradictory_adjudication_is_a_protocol_failure(self):
        models = ContractModels(contradictions=2)
        result = self.run_gate(models)
        self.assertEqual(len(models.payloads), 3)
        self.assertEqual([c['status'] for c in result.execution['calls']],
                         ['success', 'contract_failure', 'contract_failure'])
        self.assertEqual(result.execution['outcome'], 'protocol_failure')
        self.assertEqual(result.quality_status, 'uncertain')
        self.assertNotIn('adjudicator', result.execution)
        self.assertEqual(result.concerns, [])
        self.assertEqual(result.evidence, [])

    def test_neither_attempt_is_repaired_reinterpreted_or_discarded(self):
        models = ContractModels(contradictions=1)
        result = self.run_gate(models)
        rejected, accepted = result.execution['calls'][1], result.execution['calls'][2]
        # The rejected attempt is stored exactly as returned: its pass and its blocking
        # reason both survive, so no field was deleted and no decision was rewritten.
        self.assertEqual(rejected['raw_content'], models.contents[1])
        original = json.loads(rejected['raw_content'])
        self.assertEqual(original['promotion_decision'], 'pass')
        self.assertEqual(original['blocking_reasons'], [SENTINEL])
        self.assertNotIn('canonical_response_sha256', rejected)
        self.assertNotIn('response_binding_sha256', rejected)
        self.assertEqual(accepted['raw_content'], models.contents[2])
        self.assertEqual(result.execution['adjudicator'], json.loads(models.contents[2]))
        # The accepted adjudication is the model's own second judgment, not a repair of
        # the first: its decision came back from the provider, unmodified.
        self.assertEqual(canonical_json(result.execution['adjudicator']),
                         canonical_json(json.loads(accepted['raw_content'])))

    def test_both_attempts_keep_their_provenance_and_cost(self):
        models = ContractModels(contradictions=1)
        result = self.run_gate(models)
        receipt = result.execution
        self.assertEqual(receipt['retry_policy'], RETRY_POLICY)
        self.assertEqual(receipt['attempt_limit_per_role'], {'primary': 1, 'adjudicator': 2})
        for call in receipt['calls']:
            self.assertEqual(call['attempt_binding_sha256'],
                             attempt_binding(call, receipt['run_id'], RETRY_POLICY))
            self.assertEqual(call['provider'], 'google' if call['kind'] == 'primary' else 'openrouter')
            self.assertEqual(call['usage']['cost_usd'], 0.001)
            self.assertEqual(call['billing']['basis'], 'provider_reported')
        self.assertEqual(sum(c['usage']['cost_usd'] for c in receipt['calls']), 0.003)
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / 'state.sqlite3')
            store.save_quality_assessment(result)
            loaded = store.get_current_quality_assessment(result.canonical_id)
            self.assertEqual(loaded, result)
            validate_receipt(loaded)
            self.assertEqual(len(loaded.execution['calls']), 3)

    def test_a_stored_contradictory_receipt_fails_closed_under_the_new_policy(self):
        result = self.run_gate(ContractModels(contradictions=0))
        stored = result.to_dict()
        stored['execution']['adjudicator']['blocking_reasons'] = [SENTINEL]
        with self.assertRaises(ValueError):
            QualityAssessment.from_dict(deepcopy(stored))
        # Recorded under the policy that predates the contract, the identical row keeps
        # its original meaning and stays readable: history is never reinterpreted.
        legacy = deepcopy(result.to_dict())
        legacy['execution']['retry_policy'] = RETRY_POLICIES[0]
        for call in legacy['execution']['calls']:
            call['attempt_binding_sha256'] = attempt_binding(call, legacy['execution']['run_id'],
                                                             RETRY_POLICIES[0])
        validate_receipt(QualityAssessment.from_dict(legacy))

    def historical_row(self, store, key):
        """Reconstruct the stored Batch-4 shape: a receipt written under the policy that
        predates the contract, whose adjudication passed the paper while returning one
        blocking reason. The current policy refuses to produce one, so it is rebuilt.
        """
        _, _, text, seed = fixture(key)
        models = Models(adjudicator='uncertain',
                        change=lambda v, r: v.update(blocking_reasons=[SENTINEL]) if r else None)
        with patch.dict('os.environ', ENV, clear=True):
            result = assess_promotion(fixture(key)[0], text, seed, 'llm', http=models)
        self.assertEqual(result.concerns, [SENTINEL])
        stored = result.to_dict()
        receipt = stored['execution']
        receipt['retry_policy'] = RETRY_POLICIES[0]
        receipt['adjudicator']['promotion_decision'] = 'pass'
        call = receipt['calls'][1]
        call['raw_content'] = canonical_json(receipt['adjudicator'])
        call['content_sha256'] = digest(call['raw_content'])
        call['canonical_response_sha256'] = digest(canonical_json(receipt['adjudicator']))
        call['response_binding_sha256'] = response_binding(call, receipt['run_id'])
        for entry in receipt['calls']:
            entry['attempt_binding_sha256'] = attempt_binding(entry, receipt['run_id'],
                                                              RETRY_POLICIES[0])
        historical = QualityAssessment.from_dict(stored)
        validate_receipt(historical)
        self.assertEqual(historical.execution['adjudicator']['promotion_decision'], 'pass')
        self.assertEqual(historical.concerns, [SENTINEL])
        store.save_quality_assessment(historical)
        return historical

    def test_a_known_invalid_decision_is_withheld_from_publication_not_deleted(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / 'state.sqlite3')
            key = store.upsert_paper(fixture()[0],
                                     ClassificationResult(95, 'relevant', 'Synthetic topical match'))
            historical = self.historical_row(store, key)
            paper = _load_library_papers(store.path)[0]
        self.assertIsNotNone(_withheld_scientific_decision(historical))
        # Published as awaiting assessment, with the contradictory reason nowhere in the
        # public record and the paper still reviewable rather than hidden.
        self.assertEqual(paper.quality_status, 'not_assessed')
        self.assertEqual(paper.quality_concerns, [])
        self.assertEqual(paper.quality_promotion, {})
        self.assertNotIn(SENTINEL, json.dumps(paper.__dict__))
        self.assertIn('withheld from publication', paper.quality_rationale)
        self.assertFalse(paper.quality_suppressed)
        self.assertFalse(_main_library(paper))
        self.assertTrue(_review_candidate(paper))
        # Internal history is untouched: the stored row still carries both halves.
        self.assertEqual(historical.execution['adjudicator']['blocking_reasons'], [SENTINEL])
        self.assertEqual(historical.quality_status, 'uncertain')

    def test_a_consistent_decision_publishes_normally(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / 'state.sqlite3')
            key = store.upsert_paper(fixture()[0],
                                     ClassificationResult(95, 'relevant', 'Synthetic topical match'))
            _, _, text, seed = fixture(key)
            with patch.dict('os.environ', ENV, clear=True):
                valid = assess_promotion(fixture(key)[0], text, seed, 'llm', http=ContractModels(0))
            store.save_quality_assessment(valid)
            paper = _load_library_papers(store.path)[0]
        self.assertIsNone(_withheld_scientific_decision(valid))
        self.assertEqual(paper.quality_status, 'pass')
        self.assertTrue(_main_library(paper))

    def test_agreement_is_unchanged_and_still_the_only_promotion_rule(self):
        primary = {'decision': 'pass', 'evidence_ids': ['E1']}
        for decision, reasons, expected in [('pass', [], True), ('pass', [SENTINEL], False),
                                            ('uncertain', ['Real concern.'], False),
                                            ('uncertain', [], False)]:
            adjudicator = {'promotion_decision': decision, 'blocking_reasons': reasons,
                           'evidence_ids': ['E2']}
            self.assertEqual(agreement(primary, adjudicator), expected)
        self.assertFalse(agreement({'decision': 'uncertain', 'evidence_ids': ['E1']},
                                   {'promotion_decision': 'pass', 'blocking_reasons': [],
                                    'evidence_ids': ['E2']}))


if __name__ == '__main__':
    unittest.main()
