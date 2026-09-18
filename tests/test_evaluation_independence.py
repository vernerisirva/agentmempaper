"""Evaluation independence: optimization signal versus headline evaluation signal.

Every response here is synthetic and no live model is called. These tests cover the
structural contract over the values each scientific role declares, the scenarios that
must and must not raise a concern, and the historical compatibility of rows written
before the dimension existed. They never assert that any real manuscript is good
science, and no scenario is tied to a particular paper, system or evaluator vendor.
"""
from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import replace
import io
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.cli import main
from paper_scout.evidence_context import build_evidence_context
from paper_scout.models import ClassificationResult
from paper_scout.state import PaperStore
from paper_scout.promotion_gate import assess_promotion, request_payload, role_settings
from paper_scout.promotion_protocol import (
    ADJUDICATOR_MODEL, GATE_VERSION, INDEPENDENCE_CONTRACT, INDEPENDENCE_FIELD,
    INDEPENDENCE_GATE_VERSIONS, INDEPENDENCE_PROSE, PRIMARY_MODEL, RUBRIC,
    RECEIPT_VERSION, ResponseContractError, CORROBORATION, CORROBORATION_DIRECTION,
    INDEPENDENCE_CONCERN, SIGNAL_REUSE, evaluation_independence_error, parse_response,
    response_binding, schema, validate_receipt,
)
from paper_scout.quality_models import QualityAssessment
from test_gemini_promotion_pair import PairModels, legacy_receipt, run_gate
from test_promotion_gate import ENV, INDEPENDENT, Models, fixture


def block(**overrides):
    return {**INDEPENDENT, **overrides}


# Each scenario is a shape a manuscript can take, not a named paper. The prose is
# generic on purpose: the contract reads only the enum values beneath it.
CIRCULAR = block(
    optimization_signal='An automated evaluator rejects units and its decisions drive local repair.',
    final_evaluation_signal='The repaired artifact is scored again under the same evaluator protocol.',
    signal_reuse='materially_reused', independent_corroboration='absent',
    corroboration_summary='No human labels, agreement statistics or held-out evaluator are reported.',
    corroboration_direction='unavailable', concern='major')

VALIDATED = block(
    optimization_signal='A learned evaluator supplies the feedback the system is revised against.',
    final_evaluation_signal='The same evaluator scores the revised artifact.',
    signal_reuse='materially_reused', independent_corroboration='present',
    corroboration_summary='Blinded expert raters scored a sample and agreement statistics are reported.',
    corroboration_direction='supports', concern='moderate')

CONTRADICTED = block(
    optimization_signal='Evaluator feedback selects and repairs the candidate outputs.',
    final_evaluation_signal='The same evaluator protocol establishes the reported gain.',
    signal_reuse='materially_reused', independent_corroboration='present',
    corroboration_summary='One evaluator-independent measurement is reported and declines against the baseline.',
    corroboration_direction='contradicts', concern='major')

EXTERNAL = block(
    optimization_signal='Training rewards come from verified synthetic tasks built before evaluation.',
    final_evaluation_signal='Accuracy on established third-party benchmarks with their own ground truth.',
    signal_reuse='independent', independent_corroboration='present',
    corroboration_summary='Several external benchmarks are reported against published baselines.',
    corroboration_direction='supports', concern='none')

REPORTING_ONLY = block(
    optimization_signal='Nothing in the studied system is tuned, selected or repaired against the evaluator.',
    final_evaluation_signal='A model evaluator scores the final outputs once, for reporting only.',
    signal_reuse='independent', independent_corroboration='absent',
    corroboration_summary='No further measurement is reported; nothing is optimized against this evaluator.',
    corroboration_direction='unavailable', concern='none')

OBJECTIVE_OUTCOME = block(
    optimization_signal='A model evaluator flags steps and guidance is generated for the flagged ones.',
    final_evaluation_signal='Task success under the established deterministic grader for the benchmark.',
    signal_reuse='independent', independent_corroboration='present',
    corroboration_summary='The headline number comes from the external grader, not the evaluator.',
    corroboration_direction='supports', concern='none')

UNRESOLVED = block(
    optimization_signal='The manuscript does not state what signal the system was adapted against.',
    final_evaluation_signal='The reported outcome is scored by an automated procedure that is not described.',
    signal_reuse='uncertain', independent_corroboration='absent',
    corroboration_summary='No validation of the scoring procedure is reported anywhere in the manuscript.',
    corroboration_direction='unavailable', concern='moderate')


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
            self.assertEqual(payload['response_format']['json_schema']['schema'], schema(role))
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

    def test_an_earlier_row_cannot_borrow_the_new_contract(self):
        legacy = legacy_receipt()
        for mutate in (lambda e: e.update(independence_contract=INDEPENDENCE_CONTRACT),
                       lambda e: e['primary'].update({INDEPENDENCE_FIELD: dict(EXTERNAL)}),
                       lambda e: e['adjudicator'].update({INDEPENDENCE_FIELD: dict(EXTERNAL)})):
            with self.subTest():
                execution = deepcopy(legacy.execution)
                mutate(execution)
                with self.assertRaises(ValueError):
                    QualityAssessment.from_dict(replace(legacy, execution=execution).to_dict())

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
              patch('paper_scout.promotion_gate.GATE_VERSION', 'dual-promotion-v2')):
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


class RoutineSelectionTests(unittest.TestCase):
    """What a routine reassess-quality run selects, through the real CLI predicate.

    The rubric moved, so a historical non-pass row is no longer current and becomes
    reachable by a routine run; a stored pass is still excluded on its own. This
    exercises the selection in paper_scout/cli.py rather than a copy of it, and stops
    before any assessment: the assessor is replaced, so no model is called.
    """

    def historical_row(self, key, status):
        """A row as the retired pair wrote one, bound to this store's canonical key."""
        decision = 'pass' if status == 'pass' else 'uncertain'
        candidate, _, text, seed = fixture(key)

        def legacy_parse(content, role, context, **kwargs):
            return parse_response(content, role, context, **{**kwargs, 'independence': False})

        with (patch('paper_scout.promotion_gate.parse_response', legacy_parse),
              patch('paper_scout.promotion_gate.INDEPENDENCE_CONTRACT', None),
              patch('paper_scout.promotion_gate.GATE_VERSION', 'dual-promotion-v2'),
              patch.dict('os.environ', ENV, clear=True)):
            result = assess_promotion(candidate, text, seed, 'llm',
                                      http=PairModels(decision, decision, independence=None))
        self.assertEqual(result.quality_status, status)
        execution = deepcopy(result.execution)
        for field in ('independence_contract', 'model_pair', 'primary_provider',
                      'adjudicator_provider', 'generation'):
            execution.pop(field, None)
        for call in execution['calls']:
            call.pop('provider', None)
            call.pop('billing', None)
        return replace(result, quality_gate_version='dual-promotion-v1', execution=execution,
                       assessment_version='quality-promotion-v1', rubric_version='scholarly-rubric-v1')

    def store_with(self, status, versions=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        store = PaperStore(root / 'state.sqlite3')
        candidate, _, _, _ = fixture()
        key = store.upsert_paper(candidate, ClassificationResult(95, 'relevant', 'Synthetic match'))
        store.save_quality_assessment(self.historical_row(key, status))
        pinned = ''
        if versions:
            pinned = (f'  assessment:\n    version: "{versions[0]}"\n'
                      f'    rubric_version: "{versions[1]}"\n')
        # Output is redirected into the temporary tree, so a run can never write over
        # the committed daily quality report or any published digest.
        config = root / 'config.yaml'
        config.write_text(f'state:\n  sqlite_path: "{root / "state.sqlite3"}"\n'
                          f'output:\n  report_dir: "{root / "reports"}"\n'
                          f'  digest_dir: "{root / "digests"}"\n'
                          f'quality:\n  enabled: true\n  mode: "deterministic"\n{pinned}',
                          encoding='utf-8')
        return config, key

    def selected(self, config):
        seen = []

        def record(quality_config, store, candidate, canonical_id, classification, **kwargs):
            seen.append(canonical_id)
            return None

        with (patch('paper_scout.cli.assess_and_store_candidate', record),
              redirect_stdout(io.StringIO())):
            self.assertEqual(main(['--config', str(config), 'reassess-quality', '--limit', '10']), 0)
        return seen

    def test_a_historical_non_pass_becomes_reachable_under_the_new_rubric(self):
        config, key = self.store_with('uncertain')
        self.assertEqual(self.selected(config), [key])

    def test_a_stored_pass_is_still_excluded_on_its_own(self):
        config, _ = self.store_with('pass')
        self.assertEqual(self.selected(config), [])

    def test_nothing_is_selected_while_the_row_matches_the_configured_versions(self):
        config, _ = self.store_with('uncertain',
                                    versions=('quality-promotion-v1', 'scholarly-rubric-v1'))
        self.assertEqual(self.selected(config), [])


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
