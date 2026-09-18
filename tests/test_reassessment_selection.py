"""What a routine reassess-quality run selects once the scientific rubric moves.

The evaluation-independence change moved the assessment and rubric versions, so a
historical non-pass row is no longer current and becomes reachable by a routine run,
while a stored pass is still excluded on its own. These tests exercise the selection
in paper_scout/cli.py rather than a copy of it, and stop before any assessment: the
assessor is replaced, so no model is ever called and no report is ever written
outside the test's own temporary tree.
"""
from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import replace
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.cli import main
from paper_scout.config import load_config
from paper_scout.models import ClassificationResult
from paper_scout.promotion_gate import assess_promotion
from paper_scout.promotion_protocol import parse_response
from paper_scout.state import PaperStore
from test_gemini_promotion_pair import PairModels
from test_promotion_gate import ENV, fixture


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

    def store_with(self, status, versions=None, cap=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        store = PaperStore(root / 'state.sqlite3')
        candidate, _, _, _ = fixture()
        key = store.upsert_paper(candidate, ClassificationResult(95, 'relevant', 'Synthetic match'))
        store.save_quality_assessment(self.historical_row(key, status))
        pinned = ''
        if versions or cap is not None:
            pinned = '  assessment:\n'
            if versions:
                pinned += (f'    version: "{versions[0]}"\n'
                           f'    rubric_version: "{versions[1]}"\n')
            if cap is not None:
                pinned += f'    max_assessments_per_run: {cap}\n'
        # Output is redirected into the temporary tree, so a run can never write over
        # the committed daily quality report or any published digest.
        config = root / 'config.yaml'
        config.write_text(f'state:\n  sqlite_path: "{root / "state.sqlite3"}"\n'
                          f'output:\n  report_dir: "{root / "reports"}"\n'
                          f'  digest_dir: "{root / "digests"}"\n'
                          f'quality:\n  enabled: true\n  mode: "deterministic"\n{pinned}',
                          encoding='utf-8')
        return config, key

    def selected(self, config, limit=None):
        seen = []

        def record(quality_config, store, candidate, canonical_id, classification, **kwargs):
            seen.append(canonical_id)
            return None

        with (patch('paper_scout.cli.assess_and_store_candidate', record),
              redirect_stdout(io.StringIO())):
            argv = ['--config', str(config), 'reassess-quality']
            if limit is not None:
                argv += ['--limit', str(limit)]
            self.assertEqual(main(argv), 0)
        return seen

    def test_a_historical_non_pass_becomes_reachable_under_the_new_rubric(self):
        # No --limit, so this is the routine path an operator or schedule would take.
        config, key = self.store_with('uncertain')
        self.assertEqual(self.selected(config, limit=None), [key])

    def test_a_stored_pass_is_still_excluded_on_its_own(self):
        config, _ = self.store_with('pass')
        self.assertEqual(self.selected(config, limit=None), [])

    def test_nothing_is_selected_while_the_row_matches_the_configured_versions(self):
        config, _ = self.store_with('uncertain',
                                    versions=('quality-promotion-v1', 'scholarly-rubric-v1'))
        self.assertEqual(self.selected(config, limit=None), [])

    def test_a_routine_run_is_still_bounded_by_the_per_run_assessment_cap(self):
        """The moved rubric widens what is reachable; it does not widen one run.

        Reachability and per-run volume are separate limits. Every shipped track
        config keeps a small max_assessments_per_run, and reassess-quality applies it
        to this path, so the backlog is worked through a few papers at a time rather
        than in one sweep.
        """
        for track in ('config/paper_scout.yaml', 'config/tracks/agent_memory.yaml',
                      'config/tracks/deep_research.yaml', 'config/tracks/engram.yaml'):
            with self.subTest(track=track):
                cap = load_config(Path(track)).quality.assessment.max_assessments_per_run
                self.assertGreater(cap, 0)
                self.assertLessEqual(cap, 5)
        # With no --limit the configured cap governs this path: a cap of zero selects
        # nothing even though the row is reachable, so volume is bounded by the cap
        # rather than by the size of the reachable set.
        capped, _ = self.store_with('uncertain', cap=0)
        self.assertEqual(self.selected(capped, limit=None), [])
        uncapped, key = self.store_with('uncertain', cap=5)
        self.assertEqual(self.selected(uncapped, limit=None), [key])
