import tempfile
import unittest
import gc
import warnings
from pathlib import Path

from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.state import PaperStore


class PaperScoutDatabaseTest(unittest.TestCase):
    def test_persists_papers_sightings_runs_and_notifications(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PaperStore(Path(tmpdir) / "state.sqlite3")
            run_id = store.start_run(days=3)
            candidate = PaperCandidate(
                title="Agentic Memory Benchmark",
                authors=["Ada Lovelace"],
                abstract="Benchmark for persistent memory in LLM agents.",
                source="semantic_scholar",
                source_id="S2",
                semantic_scholar_id="S2",
                url="https://example.test/s2",
                published_date="2026-01-01",
            )
            classification = ClassificationResult(
                score=88,
                decision="relevant",
                reason="Tests persistent memory in LLM agents.",
                tags=["agent-memory", "benchmark"],
            )

            key = store.upsert_paper(candidate, classification)
            store.record_sighting(run_id, key, candidate, "agent memory")
            store.finish_run(run_id, fetched_count=1, new_count=1, notified_count=0)

            unnotified = store.get_unnotified_digest_papers()
            self.assertEqual([paper.title for paper in unnotified], ["Agentic Memory Benchmark"])

            store.mark_notified([key], digest_date="2026-06-26")

            self.assertEqual(store.get_unnotified_digest_papers(), [])
            notified = store.get_notified_for_date("2026-06-26")
            self.assertEqual([paper.canonical_key for paper in notified], [key])

    def test_store_operations_do_not_leak_sqlite_connections(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always", ResourceWarning)
                store = PaperStore(Path(tmpdir) / "state.sqlite3")
                run_id = store.start_run(days=3)
                store.finish_run(run_id, fetched_count=0, new_count=0, notified_count=0)
                store.get_unnotified_digest_papers()
                del store
                gc.collect()

            leaked = [warning for warning in caught if issubclass(warning.category, ResourceWarning)]
            self.assertEqual(leaked, [])


if __name__ == "__main__":
    unittest.main()
