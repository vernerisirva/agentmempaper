"""The read-only integrity check over stored assessment history.

The private databases are not committed, so the operator check cannot run against real
history here. These tests build stores with the shapes that history actually holds and
assert the check reads them, plus the inconsistent shapes it exists to surface. Nothing
is written to any database the check inspects.
"""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from dataclasses import replace
import io

from paper_scout.models import ClassificationResult
from paper_scout.promotion_protocol import INDEPENDENCE_FIELD
from paper_scout.state import PaperStore
from evaluation_independence_scenarios import EXTERNAL
from test_evaluation_independence_gate import HistoricalShapeTests
from test_gemini_promotion_pair import PairModels, run_gate
from test_promotion_gate import fixture

SCRIPT = Path(__file__).resolve().parents[1] / '.github' / 'scripts' / 'check_stored_assessments.py'
_spec = importlib.util.spec_from_file_location('check_stored_assessments', SCRIPT)
check_stored_assessments = importlib.util.module_from_spec(_spec)
sys.modules['check_stored_assessments'] = check_stored_assessments
_spec.loader.exec_module(check_stored_assessments)


class StoredAssessmentCheckTests(unittest.TestCase):
    def store(self, assessments):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / 'state.sqlite3'
        store = PaperStore(path)
        candidate, _, _, _ = fixture()
        store.upsert_paper(candidate, ClassificationResult(95, 'relevant', 'Synthetic match'))
        for assessment in assessments:
            store.save_quality_assessment(assessment)
        return path

    def run_check(self, *paths):
        output = io.StringIO()
        with redirect_stdout(output):
            code = check_stored_assessments.main([str(p) for p in paths])
        return code, output.getvalue()

    def rows(self):
        """One row of each shape the databases hold, plus a current-gate row."""
        return [HistoricalShapeTests.row(self, 'quality-promotion-v1', gate, status)
                for gate, status in (('dual-promotion-v1', 'pass'),
                                     ('dual-promotion-v1', 'uncertain'),
                                     ('dual-promotion-v2', 'pass'),
                                     ('dual-promotion-v2', 'uncertain'))]

    def assessments(self):
        from paper_scout.quality_models import QualityAssessment
        return [QualityAssessment.from_dict(row) for row in self.rows()]

    def test_every_historical_shape_reads_clean(self):
        path = self.store(self.assessments() + [run_gate(PairModels(independence=EXTERNAL))])
        code, output = self.run_check(path)
        self.assertEqual(code, 0)
        self.assertIn('stored assessment checks: 0 errors', output)
        self.assertIn('5 stored assessments', output)

    def test_no_argument_selects_the_defaults_and_an_empty_list_selects_nothing(self):
        """The contract the docstring states, which only a programmatic caller reaches."""
        empty = io.StringIO()
        with redirect_stdout(empty):
            self.assertEqual(check_stored_assessments.main([]), 0)
        self.assertIn('0 stored assessments', empty.getvalue())
        self.assertNotIn('skipped', empty.getvalue())
        defaults = io.StringIO()
        with redirect_stdout(defaults):
            self.assertEqual(check_stored_assessments.main(None), 0)
        for database in check_stored_assessments.DEFAULT_DATABASES:
            self.assertIn(str(database), defaults.getvalue())

    def test_an_absent_database_is_skipped_rather_than_failing(self):
        code, output = self.run_check(Path('does/not/exist.sqlite3'))
        self.assertEqual(code, 0)
        self.assertIn('skipped (absent)', output)
        self.assertIn('0 stored assessments', output)

    def test_a_promotion_version_pass_on_a_legacy_gate_is_reported_not_raised(self):
        """The invariant the widened load guard enforces, surfaced as a plain report."""
        row = dict(self.rows()[0], quality_gate_version='scientific-gate-v1')
        path = self.store(self.assessments())
        self.write_raw(path, row)
        code, output = self.run_check(path)
        self.assertEqual(code, 1)
        self.assertIn('pass on legacy gate scientific-gate-v1', output)
        self.assertIn('stored assessment checks: 1 errors', output)

    def test_a_current_gate_row_gets_a_named_diagnosis_too(self):
        """A current-gate row is named as specifically as a legacy one."""
        from paper_scout.promotion_protocol import INDEPENDENCE_FIELD as field
        current = run_gate(PairModels(independence=EXTERNAL)).to_dict()
        for mutate, expected in (
                (lambda r: r['execution']['primary'].pop(field), 'missing evaluation independence'),
                (lambda r: r['execution'].pop('independence_contract'),
                 'missing evaluation-independence contract version'),
                (lambda r: r['execution']['primary'][field].update(
                    signal_reuse='materially_reused', independent_corroboration='absent',
                    corroboration_direction='unavailable', concern='none'),
                 'violate their contract')):
            with self.subTest(expected=expected):
                import copy
                row = copy.deepcopy(current)
                mutate(row)
                path = self.store(self.assessments())
                self.write_raw(path, row)
                code, output = self.run_check(path)
                self.assertEqual(code, 1)
                self.assertIn(expected, output)

    def test_an_assessment_version_borrowed_across_gates_is_reported(self):
        row = dict(self.rows()[0], assessment_version='quality-promotion-v2')
        path = self.store(self.assessments())
        self.write_raw(path, row)
        code, output = self.run_check(path)
        self.assertEqual(code, 1)
        self.assertIn('assessment version quality-promotion-v2 on gate dual-promotion-v1', output)

    def test_an_earlier_gate_carrying_the_dimension_is_reported(self):
        row = self.rows()[0]
        row['execution']['primary'][INDEPENDENCE_FIELD] = dict(EXTERNAL)
        path = self.store(self.assessments())
        self.write_raw(path, row)
        code, output = self.run_check(path)
        self.assertEqual(code, 1)
        self.assertIn('carries evaluation independence', output)

    def test_a_present_database_without_an_assessment_history_is_reported(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / 'other.sqlite3'
        import sqlite3
        connection = sqlite3.connect(path)
        with connection:
            connection.execute('CREATE TABLE unrelated(id INTEGER PRIMARY KEY)')
        connection.close()
        code, output = self.run_check(path)
        self.assertEqual(code, 1)
        self.assertIn('unreadable database', output)
        self.assertIn('paper_quality_assessments', output)

    def test_a_malformed_payload_is_reported_and_the_run_continues(self):
        """The never-raise contract: one bad row must not abort the remaining ones."""
        import sqlite3
        path = self.store(self.assessments())
        connection = sqlite3.connect(path)
        with connection:
            connection.execute(
                'INSERT INTO paper_quality_assessments(canonical_id, assessment_version,'
                ' rubric_version, assessor_type, assessor_model, source_content_hash,'
                ' assessed_at, overall_quality_score, recommendation, confidence,'
                ' assessment_scope, paper_type, payload_json)'
                " VALUES('fixture','quality-promotion-v1','scholarly-rubric-v1','llm',"
                "'corrupted-history','hash','2026-09-18T00:00:00',NULL,'unknown','low',"
                "'full_text','unclear','{not json')")
        connection.close()
        code, output = self.run_check(path)
        self.assertEqual(code, 1)
        self.assertIn('unreadable payload', output)
        # The four good rows were still counted after the bad one was reported.
        self.assertIn('4 stored assessments', output)

    def test_valid_json_that_is_not_an_assessment_is_reported_not_raised(self):
        """Valid JSON is not necessarily a stored assessment."""
        import sqlite3
        for payload in ('[1]', '1', '"text"', 'null', 'true'):
            with self.subTest(payload=payload):
                path = self.store(self.assessments())
                connection = sqlite3.connect(path)
                with connection:
                    connection.execute(
                        'INSERT INTO paper_quality_assessments(canonical_id,'
                        ' assessment_version, rubric_version, assessor_type, assessor_model,'
                        ' source_content_hash, assessed_at, overall_quality_score,'
                        ' recommendation, confidence, assessment_scope, paper_type,'
                        " payload_json) VALUES('fixture','quality-promotion-v1',"
                        "'scholarly-rubric-v1','llm','corrupted-history','hash',"
                        "'2026-09-18T00:00:00',NULL,'unknown','low','full_text',"
                        f"'unclear','{payload}')")
                connection.close()
                code, output = self.run_check(path)
                self.assertEqual(code, 1)
                self.assertIn('not an object', output)
                # The four good rows were still counted after the bad one.
                self.assertIn('4 stored assessments', output)

    def test_a_database_path_containing_uri_syntax_is_still_opened(self):
        """A '?' or '#' in a name is part of the path, not URI query or fragment."""
        path = self.store(self.assessments())
        odd = path.parent / 'state?#odd.sqlite3'
        path.rename(odd)
        code, output = self.run_check(odd)
        self.assertEqual(code, 0)
        self.assertIn('4 stored assessments', output)
        self.assertNotIn('unreadable', output)

    def test_the_error_count_is_exact_while_the_listing_is_bounded(self):
        """A broken history reports its shape without reproducing itself."""
        import sqlite3
        path = self.store(self.assessments())
        bad = check_stored_assessments.MAX_REPORTED_FAILURES + 7
        connection = sqlite3.connect(path)
        with connection:
            for index in range(bad):
                connection.execute(
                    'INSERT INTO paper_quality_assessments(canonical_id, assessment_version,'
                    ' rubric_version, assessor_type, assessor_model, source_content_hash,'
                    ' assessed_at, overall_quality_score, recommendation, confidence,'
                    ' assessment_scope, paper_type, payload_json)'
                    " VALUES(?,'quality-promotion-v1','scholarly-rubric-v1','llm',?,'hash',"
                    "'2026-09-18T00:00:00',NULL,'unknown','low','full_text','unclear','[1]')",
                    (f'fixture-{index}', f'corrupted-history-{index}'))
        connection.close()
        code, output = self.run_check(path)
        self.assertEqual(code, 1)
        self.assertIn(f'stored assessment checks: {bad} errors', output)
        self.assertEqual(output.count('not an object'), check_stored_assessments.MAX_REPORTED_FAILURES)
        self.assertIn(f'... and {bad - check_stored_assessments.MAX_REPORTED_FAILURES} more', output)

    def test_a_later_database_is_still_checked_after_an_earlier_one_fails(self):
        good = self.store(self.assessments())
        code, output = self.run_check(Path('does/not/exist.sqlite3'), good)
        self.assertEqual(code, 0)
        self.assertIn('4 stored assessments', output)

    def write_raw(self, path, row):
        """Insert a row the model layer would refuse, as a corrupted history would hold."""
        import json
        import sqlite3
        connection = sqlite3.connect(path)
        with connection:
            connection.execute(
                'INSERT INTO paper_quality_assessments(canonical_id, assessment_version,'
                ' rubric_version, assessor_type, assessor_model, source_content_hash,'
                ' assessed_at, overall_quality_score, recommendation, confidence,'
                ' assessment_scope, paper_type, payload_json)'
                ' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (row['canonical_id'], row['assessment_version'], row['rubric_version'],
                 row['assessor_type'], 'corrupted-history', row['source_content_hash'],
                 row['assessed_at'], row['overall_quality_score'], row['recommendation'],
                 row['confidence'], row['assessment_scope'], row['paper_type'],
                 json.dumps(row, sort_keys=True)))
        connection.close()


if __name__ == '__main__':
    unittest.main()
