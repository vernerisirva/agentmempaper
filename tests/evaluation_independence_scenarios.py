"""Evaluation-independence scenario shapes shared by the contract and gate tests.

Each is a shape a manuscript can take, not a named paper, and the prose is generic on
purpose: the structural contract reads only the enum values beneath it.
"""
from test_promotion_gate import INDEPENDENT


def block(**overrides):
    return {**INDEPENDENT, **overrides}


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
