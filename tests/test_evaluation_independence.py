"""The structural evaluation-independence contract and the prompt that states it.

Every response here is synthetic and no live model is called. These tests cover the
contract over the values each scientific role declares, and the scenarios that must and
must not raise a concern. They never assert that any real manuscript is good science,
and no scenario is tied to a particular paper, system or evaluator vendor. The gate,
receipt and historical-compatibility side lives in test_evaluation_independence_gate.
"""
import json
import unittest
from unittest.mock import patch

from paper_scout.evidence_context import build_evidence_context
from paper_scout.promotion_gate import request_payload, role_settings
from paper_scout.promotion_protocol import (
    ADJUDICATOR_MODEL, INDEPENDENCE_FIELD, INDEPENDENCE_PROSE, PRIMARY_MODEL, RUBRIC,
    ResponseContractError, CORROBORATION, CORROBORATION_DIRECTION, INDEPENDENCE_CONCERN,
    SIGNAL_REUSE, evaluation_independence_error, parse_response, schema,
)
from evaluation_independence_scenarios import (
    CIRCULAR, CONTRADICTED, EXTERNAL, OBJECTIVE_OUTCOME, REPORTING_ONLY, UNRESOLVED,
    VALIDATED, block,
)
from test_promotion_gate import ENV, fixture


class ContractTests(unittest.TestCase):
    """The structural contract over each role's own declared values."""

    def response(self, role, decision, independence):
        _, _, text, seed = fixture()
        context = build_evidence_context(seed.canonical_id, text)
        value = {'canonical_id': context.canonical_id, 'source_content_hash': context.source_hash,
                 'context_id': context.context_id, 'evidence_ids': [context.blocks[0].evidence_id],
                 INDEPENDENCE_FIELD: dict(independence)}
        if role == 'primary':
            value['decision'] = decision
            value.update({k: 'Scoped judgment.' for k in (
                'scoped_contribution', 'method_assessment', 'evaluation_assessment',
                'claim_evidence_alignment', 'limitations', 'quality_rationale')})
        else:
            value['promotion_decision'] = decision
            value['blocking_reasons'] = [] if decision == 'pass' else ['Unsupported central claim.']
        return value, context

    def assert_contract(self, independence, decision, expected, *, roles=('primary', 'adjudicator')):
        for role in roles:
            with self.subTest(role=role, decision=decision):
                value, context = self.response(role, decision, independence)
                self.assertEqual(evaluation_independence_error(value, role), expected)
                raw = json.dumps(value)
                if expected is None:
                    self.assertEqual(parse_response(raw, role, context), value)
                else:
                    with self.assertRaises(ResponseContractError) as raised:
                        parse_response(raw, role, context)
                    self.assertEqual(raised.exception.reason, 'independence')
                # A receipt written before the dimension is reread under its own gate.
                stripped = {k: v for k, v in value.items() if k != INDEPENDENCE_FIELD}
                self.assertEqual(
                    parse_response(json.dumps(stripped), role, context, independence=False), stripped)

    def test_a_material_reuse_with_no_corroboration_cannot_be_a_minor_concern(self):
        """A: clear circularity with no independent validation is a major concern."""
        for concern in ('none', 'moderate'):
            self.assert_contract(block(**{**CIRCULAR, 'concern': concern}), 'uncertain', 'independence')
        self.assert_contract(CIRCULAR, 'uncertain', None)

    def test_a_material_reuse_is_major_unless_corroboration_is_actually_present(self):
        """An unresolved answer establishes independence no better than silence does."""
        for corroboration, direction in (('absent', 'unavailable'), ('uncertain', 'unavailable'),
                                         ('not_applicable', 'not_applicable')):
            reused = block(signal_reuse='materially_reused',
                           independent_corroboration=corroboration,
                           corroboration_direction=direction)
            with self.subTest(corroboration=corroboration):
                for concern in ('none', 'moderate'):
                    self.assert_contract(block(**{**reused, 'concern': concern}),
                                         'uncertain', 'independence')
                self.assert_contract(block(**{**reused, 'concern': 'major'}), 'uncertain', None)
                self.assert_contract(block(**{**reused, 'concern': 'major'}), 'pass', 'independence')
        # Unresolved *reuse* is a weaker claim and is not forced to major on its own.
        self.assert_contract(UNRESOLVED, 'pass', None)

    def test_b_a_major_concern_cannot_accompany_that_role_s_pass(self):
        """B: the same evaluator on both sides surfaces and binds the role's decision."""
        self.assert_contract(CIRCULAR, 'pass', 'independence')
        self.assert_contract(CIRCULAR, 'uncertain', None)

    def test_c_dependence_with_supporting_independent_validation_may_pass(self):
        """C: a dependent evaluator validated against blinded human judgement."""
        self.assert_contract(VALIDATED, 'pass', None)
        self.assert_contract(VALIDATED, 'uncertain', None)

    def test_d_contradicting_independent_evidence_is_major_and_blocks_the_pass(self):
        """D: presence of an independent metric is not enough; direction decides."""
        for concern in ('none', 'moderate'):
            self.assert_contract(block(**{**CONTRADICTED, 'concern': concern}), 'uncertain', 'independence')
        self.assert_contract(CONTRADICTED, 'uncertain', None)
        self.assert_contract(CONTRADICTED, 'pass', 'independence')
        # The same contradiction under an unresolved signal is treated the same way.
        unresolved = block(**{**CONTRADICTED, 'signal_reuse': 'uncertain', 'concern': 'moderate'})
        self.assert_contract(unresolved, 'uncertain', 'independence')

    def test_e_an_independent_evaluator_or_external_benchmark_raises_no_concern(self):
        """E: separate optimization and evaluation signals are unconstrained."""
        self.assert_contract(EXTERNAL, 'pass', None)

    def test_f_an_evaluator_used_only_for_reporting_is_not_automatically_circular(self):
        """F: nothing is optimized against it, so no corroboration is demanded."""
        self.assert_contract(REPORTING_ONLY, 'pass', None)

    def test_g_an_objectively_established_outcome_is_judged_on_that_outcome(self):
        """G: an evaluator inside the loop with an external grader for the headline."""
        self.assert_contract(OBJECTIVE_OUTCOME, 'pass', None)

    def test_h_unresolved_independence_with_no_corroboration_is_never_no_concern(self):
        """H: missing information is uncertainty, never automatic assurance."""
        self.assert_contract(block(**{**UNRESOLVED, 'concern': 'none'}), 'uncertain', 'independence')
        self.assert_contract(UNRESOLVED, 'uncertain', None)
        self.assert_contract(block(**{**UNRESOLVED, 'concern': 'major'}), 'pass', 'independence')

    def test_h_only_present_and_supporting_corroboration_is_an_all_clear(self):
        """Silence, an unresolved answer and partial support are all unestablished.

        Under reused or unresolved signals, none of the three may be declared free of
        concern, and partial support is not treated more leniently than silence. Where
        the corroboration is present and supports, nothing is forced. Where the signals
        are genuinely independent, none of this applies at all.
        """
        for reuse in SIGNAL_REUSE:
            for corroboration, direction in (('absent', 'unavailable'), ('uncertain', 'unavailable'),
                                             ('not_applicable', 'not_applicable'),
                                             ('present', 'mixed'), ('present', 'supports')):
                value = block(signal_reuse=reuse, independent_corroboration=corroboration,
                              corroboration_direction=direction, concern='none')
                established = corroboration == 'present' and direction == 'supports'
                forbidden = reuse in ('materially_reused', 'uncertain') and not established
                with self.subTest(reuse=reuse, corroboration=corroboration, direction=direction):
                    self.assertEqual(
                        evaluation_independence_error({'decision': 'uncertain', INDEPENDENCE_FIELD: value},
                                                      'primary'),
                        'independence' if forbidden else None)
                    # Except where material reuse without present corroboration forces
                    # major, moderate stays available and promotion is still the role's call.
                    if not (reuse == 'materially_reused' and corroboration != 'present'):
                        self.assert_contract(block(**{**value, 'concern': 'moderate'}), 'pass', None)

    def test_partial_support_under_reuse_is_not_an_all_clear_but_may_still_pass(self):
        """Mixed evidence is a concern to weigh, not a verdict and not a clearance."""
        mixed = block(signal_reuse='materially_reused', independent_corroboration='present',
                      corroboration_direction='mixed')
        self.assert_contract(block(**{**mixed, 'concern': 'none'}), 'uncertain', 'independence')
        self.assert_contract(block(**{**mixed, 'concern': 'moderate'}), 'pass', None)
        self.assert_contract(block(**{**mixed, 'concern': 'major'}), 'pass', 'independence')
        # Fully supporting corroboration under the same reuse remains a clean all-clear.
        supported = block(**{**mixed, 'corroboration_direction': 'supports', 'concern': 'none'})
        self.assert_contract(supported, 'pass', None)

    def test_a_direction_is_reportable_exactly_when_corroboration_is_present(self):
        for corroboration in CORROBORATION:
            for direction in CORROBORATION_DIRECTION:
                value = block(independent_corroboration=corroboration,
                              corroboration_direction=direction, concern='moderate')
                coherent = (direction in ('supports', 'mixed', 'contradicts')) == (corroboration == 'present')
                # Rules beyond coherence are exercised separately; hold signal_reuse clear.
                value['signal_reuse'] = 'independent'
                response = {'decision': 'uncertain', INDEPENDENCE_FIELD: value}
                with self.subTest(corroboration=corroboration, direction=direction):
                    self.assertEqual(evaluation_independence_error(response, 'primary'),
                                     None if coherent else 'independence')

    def test_the_contract_reads_no_prose_and_no_keyword(self):
        """Wording never changes the outcome: only the declared values do."""
        prose = ['Uses an LLM judge for everything.', 'circular self-evaluation',
                 'Fully validated against blinded human annotators.', 'no concerns at all', '.']
        for text in prose:
            fields = {k: text for k in INDEPENDENCE_PROSE}
            with self.subTest(prose=text[:24]):
                self.assertIsNone(evaluation_independence_error(
                    {'decision': 'pass', INDEPENDENCE_FIELD: block(**fields)}, 'primary'))
                self.assertEqual(evaluation_independence_error(
                    {'decision': 'pass', INDEPENDENCE_FIELD: block(**{**CIRCULAR, **fields})},
                    'primary'), 'independence')

    def test_a_missing_or_malformed_dimension_fails_closed(self):
        for value in ({'decision': 'pass'}, {'decision': 'pass', INDEPENDENCE_FIELD: None},
                      {'decision': 'pass', INDEPENDENCE_FIELD: 'materially_reused'}):
            self.assertEqual(evaluation_independence_error(value, 'primary'), 'independence')


class SchemaAndPromptTests(unittest.TestCase):
    def test_both_roles_carry_the_same_dimension_and_it_is_required(self):
        for role in ('primary', 'adjudicator'):
            body = schema(role)
            self.assertIn(INDEPENDENCE_FIELD, body['required'])
            dimension = body['properties'][INDEPENDENCE_FIELD]
            self.assertEqual(dimension['additionalProperties'], False)
            self.assertEqual(set(dimension['required']), set(dimension['properties']))
            self.assertEqual(dimension['properties']['signal_reuse']['enum'], list(SIGNAL_REUSE))
            self.assertEqual(dimension['properties']['independent_corroboration']['enum'], list(CORROBORATION))
            self.assertEqual(dimension['properties']['corroboration_direction']['enum'],
                             list(CORROBORATION_DIRECTION))
            self.assertEqual(dimension['properties']['concern']['enum'], list(INDEPENDENCE_CONCERN))
        self.assertEqual(schema('primary')['properties'][INDEPENDENCE_FIELD],
                         schema('adjudicator')['properties'][INDEPENDENCE_FIELD])

    def test_an_earlier_gate_s_schema_has_no_dimension(self):
        for role in ('primary', 'adjudicator'):
            self.assertNotIn(INDEPENDENCE_FIELD, schema(role, independence=False)['properties'])

    def test_both_roles_are_instructed_to_answer_it_and_the_adjudicator_not_to_inherit(self):
        _, _, text, seed = fixture()
        context = build_evidence_context(seed.canonical_id, text)
        with patch.dict('os.environ', ENV, clear=True):
            settings = {'primary': role_settings(PRIMARY_MODEL),
                        'adjudicator': role_settings(ADJUDICATOR_MODEL)}
        instructions = {}
        for role in ('primary', 'adjudicator'):
            payload = request_payload(role, settings[role], context, text.coverage,
                                      {'decision': 'pass'} if role == 'adjudicator' else None)
            instructions[role] = payload['messages'][0]['content']
            self.assertIn(INDEPENDENCE_FIELD, instructions[role])
            self.assertIn('materially', instructions[role])
            declared = payload['response_format']['json_schema']
            self.assertEqual(declared['schema'], schema(role))
            self.assertTrue(declared['strict'])
            # The response contract changed, so the name sent with it moves too. Both
            # providers were probed live with this name and the nested dimension, and
            # each returned all seven fields; nothing here can verify that again.
            self.assertEqual(declared['name'], 'promotion_' + role + '_v2')
        self.assertIn('never inherit', instructions['adjudicator'])
        retry = request_payload('adjudicator', settings['adjudicator'], context, text.coverage,
                                {'decision': 'pass'}, retry=True)['messages'][0]['content']
        self.assertIn(INDEPENDENCE_FIELD, retry)

    def test_the_rubric_is_general_and_names_no_paper_system_or_banned_technology(self):
        text = RUBRIC.lower()
        for mechanism in ('judge', 'reward model', 'automated grader', 'self-evaluation',
                          'heuristic score', 'synthetic labeller', 'model-generated'):
            self.assertIn(mechanism, text)
        for corroboration in ('human', 'inter-rater', 'calibration', 'held-out',
                              'objective external metric', 'external benchmark'):
            self.assertIn(corroboration, text)
        # No paper, system, author or dataset is named, and no technology is banned.
        for forbidden in ('pearl', 'minicheck', 'cg/rea', 'arex', 'appworld', 'openalex', 'arxiv'):
            self.assertNotIn(forbidden, text)
        self.assertIn('no particular technology is required; independence is', text)
        self.assertIn('silence establishes nothing', text)
        self.assertIn('not circular by itself', text)


if __name__ == '__main__':
    unittest.main()
