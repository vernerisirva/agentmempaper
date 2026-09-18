"""Evaluation independence end to end: gate outcomes, receipts and history.

Every response here is synthetic and no live model is called. These tests cover the
outcomes the dimension produces through the unchanged dual-agreement promotion rule,
the versioned receipt dispatch, and the compatibility of rows written before the
dimension existed. The structural contract itself lives in test_evaluation_independence.
"""
from copy import deepcopy
from dataclasses import replace
import json
import unittest
from unittest.mock import patch

from paper_scout.promotion_gate import assess_promotion
from paper_scout.promotion_protocol import (
    DUAL_PROMOTION_GATE_VERSIONS, GATE_ASSESSMENT_VERSIONS, GATE_VERSION,
    INDEPENDENCE_CONTRACT, INDEPENDENCE_FIELD, INDEPENDENCE_GATE_VERSIONS, RECEIPT_VERSION,
    parse_response, response_binding, schema, validate_receipt,
)
from paper_scout.quality_models import QualityAssessment
from evaluation_independence_scenarios import CIRCULAR, CONTRADICTED, EXTERNAL, OBJECTIVE_OUTCOME, REPORTING_ONLY, VALIDATED, block
from test_gemini_promotion_pair import PairModels, legacy_receipt, run_gate
from test_promotion_gate import ENV, Models, fixture


class GateOutcomeTests(unittest.TestCase):
    """End-to-end outcomes through the unchanged dual-agreement promotion rule."""

    def outcome(self, independence, primary='pass', adjudicator='pass'):
        return run_gate(PairModels(primary, adjudicator, independence=independence))

    def test_clear_circularity_is_withheld_and_stays_a_scientific_outcome(self):
        result = self.outcome(CIRCULAR, 'uncertain', 'uncertain')
        self.assertEqual(result.execution['outcome'], 'success')
        self.assertEqual(result.quality_status, 'uncertain')
        self.assertEqual(result.execution['primary'][INDEPENDENCE_FIELD]['concern'], 'major')
        self.assertEqual(result.execution['adjudicator'][INDEPENDENCE_FIELD]['concern'], 'major')

    def test_contradicting_independent_evidence_is_withheld(self):
        self.assertEqual(self.outcome(CONTRADICTED, 'uncertain', 'uncertain').quality_status, 'uncertain')

    def test_validated_dependence_and_independent_designs_remain_promotable(self):
        for name, independence in (('validated', VALIDATED), ('external', EXTERNAL),
                                   ('reporting_only', REPORTING_ONLY),
                                   ('objective_outcome', OBJECTIVE_OUTCOME)):
            with self.subTest(scenario=name):
                result = self.outcome(independence)
                self.assertEqual(result.execution['outcome'], 'success')
                self.assertEqual(result.quality_status, 'pass')

    def test_evaluator_based_work_is_not_rejected_as_a_class(self):
        """Model-evaluator designs still pass; only the unsupported ones are withheld.

        Three of these four rely on a model evaluator somewhere, one of them with the
        evaluator on both sides of the study, and all four remain promotable. What is
        withheld above is unsupported reuse, not the use of an evaluator.
        """
        scenarios = (VALIDATED, EXTERNAL, REPORTING_ONLY, OBJECTIVE_OUTCOME)
        promoted = [i for i in scenarios if self.outcome(i).quality_status == 'pass']
        self.assertEqual(len(promoted), len(scenarios))
        self.assertEqual(sum(i['signal_reuse'] == 'materially_reused' for i in promoted), 1)
        withheld = [i for i in (CIRCULAR, CONTRADICTED)
                    if self.outcome(i, 'uncertain', 'uncertain').quality_status == 'pass']
        self.assertEqual(withheld, [])

    def test_a_role_that_breaks_the_contract_fails_closed_and_is_never_promoted(self):
        # The primary has no retry, so its contract violation is a technical outcome.
        primary = run_gate(PairModels('pass', 'pass', independence=block(**{**CIRCULAR, 'concern': 'none'})))
        self.assertEqual(primary.execution['outcome'], 'protocol_failure')
        self.assertNotEqual(primary.quality_status, 'pass')

    def test_a_pending_outcome_carries_the_contract_without_any_role_response(self):
        """A technical outcome records the contract it ran under and still loads.

        The contract version is recorded as soon as the pair resolves, before the
        coverage and identity checks, exactly as the model pair and generation settings
        already were. A run that stops there has no role responses at all, so this
        pins that such a row is still a readable technical outcome and never a
        scientific one, rather than tripping receipt validation on the new key.
        """
        from paper_scout.http import HttpRequestError

        class Outage(PairModels):
            def post_json(self, url, payload, headers):
                raise HttpRequestError('timeout', url, 'synthetic provider outage')

        result = run_gate(Outage())
        self.assertEqual(result.execution['outcome'], 'transport_failure')
        self.assertEqual(result.execution['independence_contract'], INDEPENDENCE_CONTRACT)
        self.assertNotIn('primary', result.execution)
        self.assertNotIn('adjudicator', result.execution)
        self.assertNotEqual(result.quality_status, 'pass')
        restored = QualityAssessment.from_dict(result.to_dict())
        self.assertEqual(restored.execution['independence_contract'], INDEPENDENCE_CONTRACT)
        self.assertEqual(restored.to_dict(), result.to_dict())

    def test_the_receipt_records_the_contract_version(self):
        result = self.outcome(EXTERNAL)
        self.assertEqual(result.quality_gate_version, GATE_VERSION)
        self.assertIn(GATE_VERSION, INDEPENDENCE_GATE_VERSIONS)
        self.assertEqual(result.execution['independence_contract'], INDEPENDENCE_CONTRACT)
        validate_receipt(result)


class HistoricalCompatibilityTests(unittest.TestCase):
    """I and J: rows written before the dimension stay readable and stay valid."""

    def test_i_a_receipt_from_an_earlier_gate_loads_and_revalidates_unchanged(self):
        legacy = legacy_receipt()
        restored = QualityAssessment.from_dict(legacy.to_dict())
        self.assertEqual(restored.quality_gate_version, 'dual-promotion-v1')
        self.assertEqual(restored.assessment_version, 'quality-promotion-v1')
        self.assertEqual(restored.rubric_version, 'scholarly-rubric-v1')
        self.assertNotIn('independence_contract', restored.execution)
        for role in ('primary', 'adjudicator'):
            self.assertNotIn(INDEPENDENCE_FIELD, restored.execution[role])
        self.assertEqual(restored.quality_status, 'pass')
        validate_receipt(restored)
        self.assertEqual(restored.to_dict(), legacy.to_dict())

    def test_j_an_earlier_row_keeps_its_stored_decision_and_is_not_reinterpreted(self):
        legacy = legacy_receipt()
        # The stored pass survives a reload even though its responses answer nothing
        # about evaluation independence: it is a historical record, not a new judgment.
        self.assertEqual(QualityAssessment.from_dict(legacy.to_dict()).quality_status, 'pass')
        withheld = legacy_receipt(PairModels('uncertain', 'pass', independence=None))
        self.assertEqual(QualityAssessment.from_dict(withheld.to_dict()).quality_status, 'uncertain')

    def test_no_earlier_gate_version_can_borrow_the_new_contract(self):
        """Both earlier gates are covered, including the one that does carry provenance.

        dual-promotion-v2 is the interesting case: it must carry provider provenance and
        must not carry the dimension, so a row mixing the two shapes is rejected rather
        than read as if the newer scientific guarantee applied to it.
        """
        rows = {'dual-promotion-v1': legacy_receipt(),
                'dual-promotion-v2': QualityAssessment.from_dict(
                    HistoricalShapeTests.row(self, 'quality-promotion-v1',
                                             'dual-promotion-v2', 'pass'))}
        for gate, row in rows.items():
            self.assertEqual(row.quality_gate_version, gate)
            for mutate in (lambda e: e.update(independence_contract=INDEPENDENCE_CONTRACT),
                           lambda e: e['primary'].update({INDEPENDENCE_FIELD: dict(EXTERNAL)}),
                           lambda e: e['adjudicator'].update({INDEPENDENCE_FIELD: dict(EXTERNAL)})):
                with self.subTest(gate=gate):
                    execution = deepcopy(row.execution)
                    mutate(execution)
                    with self.assertRaises(ValueError):
                        QualityAssessment.from_dict(replace(row, execution=execution).to_dict())

    def test_an_assessment_version_cannot_be_borrowed_across_admission_gates(self):
        """Each gate wrote one response schema, so the pair it claims is determined.

        Without this, a row could claim the newer schema version while its gate says
        the older contract produced it, or the reverse: the stored provenance would
        describe an assessment that never happened.
        """
        current = run_gate(PairModels(independence=EXTERNAL))
        earlier = QualityAssessment.from_dict(
            HistoricalShapeTests.row(self, 'quality-promotion-v1', 'dual-promotion-v1', 'pass'))
        self.assertEqual(GATE_ASSESSMENT_VERSIONS[GATE_VERSION], current.assessment_version)
        self.assertEqual(set(GATE_ASSESSMENT_VERSIONS), set(DUAL_PROMOTION_GATE_VERSIONS))
        for row, borrowed in ((current, 'quality-promotion-v1'),
                              (earlier, 'quality-promotion-v2')):
            with self.subTest(gate=row.quality_gate_version, borrowed=borrowed):
                self.assertNotEqual(row.assessment_version, borrowed)
                with self.assertRaises(ValueError):
                    QualityAssessment.from_dict(
                        replace(row, assessment_version=borrowed).to_dict())
                # The pair each row actually carries still loads unchanged.
                self.assertEqual(QualityAssessment.from_dict(row.to_dict()).to_dict(),
                                 row.to_dict())

    def test_a_current_row_cannot_omit_the_contract_or_carry_broken_values(self):
        result = run_gate(PairModels(independence=EXTERNAL))
        for mutate in (lambda e: e.pop('independence_contract'),
                       lambda e: e.update(independence_contract='evaluation-independence-v0'),
                       lambda e: e['primary'][INDEPENDENCE_FIELD].update(concern='major'),
                       lambda e: e['adjudicator'][INDEPENDENCE_FIELD].update(
                           independent_corroboration='absent')):
            with self.subTest():
                execution = deepcopy(result.execution)
                mutate(execution)
                with self.assertRaises(ValueError):
                    QualityAssessment.from_dict(replace(result, execution=execution).to_dict())


class HistoricalShapeTests(unittest.TestCase):
    """The shapes actually present in the stored databases stay loadable.

    The legacy-gate guard covers every promotion assessment version rather than only
    the current one, so this pins down what that guard does and does not reject.
    """

    def row(self, assessment_version, gate_version, status):
        decision = 'pass' if status == 'pass' else 'uncertain'
        if gate_version != 'dual-promotion-v2':
            legacy = legacy_receipt(PairModels(decision, decision, independence=None))
            return replace(legacy, assessment_version=assessment_version,
                           quality_gate_version=gate_version).to_dict()

        # A dual-promotion-v2 row: the current pair and its provider provenance, written
        # under the output contract of its own time, before the dimension existed.
        def legacy_parse(content, role, context, **kwargs):
            return parse_response(content, role, context, **{**kwargs, 'independence': False})

        with (patch('paper_scout.promotion_gate.parse_response', legacy_parse),
              patch('paper_scout.promotion_gate.INDEPENDENCE_CONTRACT', None),
              patch('paper_scout.promotion_gate.GATE_VERSION', 'dual-promotion-v2'),
              patch('paper_scout.promotion_gate.ASSESSMENT_VERSION', 'quality-promotion-v1')):
            result = run_gate(PairModels(decision, decision, independence=None))
        execution = deepcopy(result.execution)
        execution.pop('independence_contract', None)
        return replace(result, assessment_version=assessment_version,
                       quality_gate_version=gate_version, execution=execution).to_dict()

    def test_every_stored_promotion_shape_still_loads(self):
        # These are the (assessment_version, gate, status) combinations the production
        # databases actually hold for promotion rows, checked read-only before this change.
        for version, gate, status in (('quality-promotion-v1', 'dual-promotion-v1', 'pass'),
                                      ('quality-promotion-v1', 'dual-promotion-v1', 'uncertain'),
                                      ('quality-promotion-v1', 'dual-promotion-v2', 'pass'),
                                      ('quality-promotion-v1', 'dual-promotion-v2', 'uncertain')):
            with self.subTest(version=version, gate=gate, status=status):
                restored = QualityAssessment.from_dict(self.row(version, gate, status))
                self.assertEqual(restored.quality_status, status)
                self.assertEqual(restored.assessment_version, version)
                self.assertNotIn(INDEPENDENCE_FIELD, restored.execution['primary'])

    def test_a_promotion_version_pass_on_a_legacy_gate_is_still_rejected(self):
        """No such row exists; the guard covers every promotion version, not just the new one."""
        for version in ('quality-promotion-v1', 'quality-promotion-v2'):
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    QualityAssessment.from_dict(self.row(version, 'scientific-gate-v1', 'pass'))


class ReceiptDispatchTests(unittest.TestCase):
    """The stored gate version is the only thing that selects a response schema.

    The receipt envelope is unchanged by this dimension, so RECEIPT_VERSION stays
    canonical-response-v1 and every response-shape decision is keyed off the gate
    version instead. That is only safe if nothing else selects the schema, which is
    what these tests pin down. Bumping RECEIPT_VERSION is not an available
    alternative: response_binding hashes the module constant, so moving it would
    invalidate the stored binding of every receipt written before the change.
    """

    def test_the_schema_depends_only_on_the_role_and_the_independence_flag(self):
        for role in ('primary', 'adjudicator'):
            with_dimension, without = schema(role), schema(role, independence=False)
            self.assertEqual(set(with_dimension['properties']) - set(without['properties']),
                             {INDEPENDENCE_FIELD})
            self.assertEqual({k: v for k, v in with_dimension['properties'].items()
                              if k != INDEPENDENCE_FIELD}, without['properties'])

    def test_the_receipt_version_is_unchanged_and_bound_into_every_response(self):
        result = run_gate(PairModels(independence=EXTERNAL))
        self.assertEqual(result.execution['receipt_version'], RECEIPT_VERSION)
        self.assertEqual(RECEIPT_VERSION, 'canonical-response-v1')
        for call in result.execution['calls']:
            self.assertEqual(response_binding(call, result.execution['run_id']),
                             call['response_binding_sha256'])

    def test_each_gate_version_revalidates_under_its_own_response_shape(self):
        shapes = {'dual-promotion-v1': False, 'dual-promotion-v2': False, GATE_VERSION: True}
        for gate, carries in shapes.items():
            with self.subTest(gate=gate):
                if carries:
                    row = run_gate(PairModels(independence=EXTERNAL))
                else:
                    row = QualityAssessment.from_dict(
                        HistoricalShapeTests.row(self, 'quality-promotion-v1', gate, 'pass'))
                self.assertEqual(row.quality_gate_version, gate)
                self.assertEqual(row.execution['receipt_version'], RECEIPT_VERSION)
                for role in ('primary', 'adjudicator'):
                    self.assertEqual(INDEPENDENCE_FIELD in row.execution[role], carries)
                self.assertEqual(row.execution.get('independence_contract') is not None, carries)
                # The receipt version is identical across all three; only the gate
                # version distinguishes their response shapes, and each rereads cleanly.
                validate_receipt(row)


class RetryTests(unittest.TestCase):
    def test_one_contract_violation_costs_exactly_one_fresh_adjudication(self):
        class Violating(Models):
            """The adjudicator declares a major concern beside its own pass, once."""

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.adjudications = 0

            def post_json(self, url, payload, headers):
                envelope = json.loads(super().post_json(url, payload, headers))
                value = json.loads(envelope['choices'][0]['message']['content'])
                if 'promotion_decision' in value:
                    self.adjudications += 1
                    if self.adjudications == 1:
                        value[INDEPENDENCE_FIELD] = dict(CIRCULAR)
                envelope['choices'][0]['message']['content'] = json.dumps(value, ensure_ascii=False)
                return json.dumps(envelope, ensure_ascii=False)

        models = Violating()
        candidate, _, text, seed = fixture()
        with patch.dict('os.environ', ENV, clear=True):
            result = assess_promotion(candidate, text, seed, 'llm', http=models)
        calls = result.execution['calls']
        self.assertEqual([(c['kind'], c['attempt'], c['status']) for c in calls],
                         [('primary', 1, 'success'), ('adjudicator', 1, 'contract_failure'),
                          ('adjudicator', 2, 'success')])
        self.assertEqual(calls[1]['contract_error'], 'independence')
        self.assertEqual(result.execution['outcome'], 'success')
        validate_receipt(result)


if __name__ == '__main__':
    unittest.main()
