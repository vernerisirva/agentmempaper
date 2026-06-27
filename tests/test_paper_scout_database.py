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

    def test_upsert_keeps_exact_publication_date_over_year_only_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PaperStore(Path(tmpdir) / "state.sqlite3")
            semantic = PaperCandidate(
                title="ProcMEM: Learning Reusable Procedural Memory from Experience via Non-Parametric PPO for LLM Agents",
                authors=["Ada Lovelace"],
                abstract="Procedural memory for LLM agents.",
                source="semantic_scholar",
                source_id="S2-PROCMEM",
                doi="10.48550/arxiv.2602.01869",
                arxiv_id="2602.01869",
                semantic_scholar_id="S2-PROCMEM",
                url="https://www.semanticscholar.org/paper/S2-PROCMEM",
                published_date="2026",
                publication_year="2026",
                publication_date_precision="year",
                publication_date_source="semantic_scholar",
            )
            arxiv = PaperCandidate(
                title=semantic.title,
                authors=["Ada Lovelace"],
                abstract="Procedural memory for LLM agents.",
                source="arxiv",
                source_id="2602.01869",
                doi="10.48550/arxiv.2602.01869",
                arxiv_id="2602.01869",
                url="https://arxiv.org/abs/2602.01869",
                published_date="2026-02-02",
                publication_year="2026",
                publication_date_precision="day",
                publication_date_source="arxiv",
            )
            classification = ClassificationResult(91, "relevant", "Studies procedural memory for LLM agents.", ["agent-memory"])

            store.upsert_paper(semantic, classification)
            key = store.upsert_paper(arxiv, classification)

            paper = store.get_unnotified_digest_papers()[0]
            self.assertEqual(paper.canonical_key, key)
            self.assertEqual(paper.published_date, "2026-02-02")
            self.assertEqual(paper.publication_year, "2026")
            self.assertEqual(paper.publication_date_precision, "day")
            self.assertEqual(paper.publication_date_source, "arxiv")


if __name__ == "__main__":
    unittest.main()
