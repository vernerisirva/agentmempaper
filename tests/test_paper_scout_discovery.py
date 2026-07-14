import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from paper_scout.config import ArxivSweepConfig, DiscoveryQuery, ScoutConfig, load_config
from paper_scout.discovery_evaluation import evaluate_discovery
from paper_scout.models import PaperCandidate
from paper_scout.query_planner import build_query, plan_queries
from paper_scout.relevance import classify_with_rules
from paper_scout.scout import ingest_candidate, run_backfill, run_scout
from paper_scout.state import PaperStore


TARGET = PaperCandidate(
    title="Procedural Memory Distillation: Online Reflection for Self-Improving Language Models",
    authors=["Researcher One", "Researcher Two"],
    abstract=(
        "We use cross-episode signals and online reflection to convert experience into reusable procedural memory. "
        "The learned memory is distilled into a language model's policy and model weights, enabling self-improving language models."
    ),
    source="arxiv",
    source_id="2607.01480",
    doi="10.48550/arXiv.2607.01480",
    arxiv_id="2607.01480",
    url="https://arxiv.org/abs/2607.01480",
    published_date="2026-07-01",
    publication_date_precision="day",
    publication_date_source="arxiv",
)


class StaticFetcher:
    source = "arxiv"

    def search_planned(self, query, days, max_results):
        return [TARGET]


class FailingArxivFetcher:
    source = "arxiv"

    def search_planned(self, query, days, max_results):
        raise RuntimeError("temporary source outage")


class PaperScoutDiscoveryTest(unittest.TestCase):
    def test_arxiv_query_modes_and_budget(self):
        all_terms = build_query("arxiv", DiscoveryQuery("procedural memory LLM agent", "all_terms"))
        phrase = build_query("arxiv", DiscoveryQuery("agent-native memory", "phrase"))
        self.assertEqual(all_terms.provider_query, "all:procedural AND all:memory AND all:LLM AND all:agent")
        self.assertNotIn('"procedural memory LLM agent"', all_terms.provider_query)
        self.assertEqual(phrase.provider_query, 'all:"agent-native memory"')

        config = ScoutConfig(
            terms=[],
            discovery_queries={"arxiv": (DiscoveryQuery("agent memory"), DiscoveryQuery("agent  memory"), DiscoveryQuery("procedural memory"))},
            query_budgets={"arxiv": 2},
        )
        planned = plan_queries(config, sources={"arxiv"}, include_sweep=False)
        self.assertEqual(len(planned), 2)
        self.assertEqual(len({query.normalized_query for query in planned}), 2)

    def test_category_sweep_is_bounded_and_covers_expected_categories(self):
        config = ScoutConfig(
            terms=[],
            discovery_queries={"arxiv": (DiscoveryQuery("agent memory"),)},
            query_budgets={"arxiv": 2},
            arxiv_sweep=ArxivSweepConfig(True, ("cs.AI", "cs.CL", "cs.LG"), 10, 300),
        )
        planned = plan_queries(config, sources={"arxiv"})
        sweep = next(query for query in planned if query.route == "category_sweep")
        self.assertEqual(sweep.provider_query, "cat:cs.AI OR cat:cs.CL OR cat:cs.LG")
        self.assertEqual(sweep.max_results, 300)

    def test_agent_memory_config_has_bounded_source_specific_plan(self):
        config = load_config(track_id="agent_memory")
        planned = plan_queries(config)
        counts = {source: sum(query.source == source for query in planned) for source in config.query_budgets}
        self.assertEqual(counts, {"arxiv": 6, "openalex": 4, "semantic_scholar": 4})
        self.assertTrue(any(query.route == "category_sweep" for query in planned))

    def test_target_is_highly_relevant_with_specific_tags_and_reason(self):
        result = classify_with_rules(TARGET)
        self.assertEqual(result.decision, "relevant")
        self.assertGreaterEqual(result.score, 90)
        for tag in ["procedural-memory", "parametric-memory", "memory-distillation", "self-improvement", "language-model-memory", "cross-episode-learning"]:
            self.assertIn(tag, result.tags)
        self.assertIn("cross-episode experience", result.reason)
        self.assertIn("language model's weights", result.reason)

    def test_discovery_evaluation_covers_target_and_all_fixtures(self):
        report = evaluate_discovery(load_config(track_id="agent_memory"))
        target = next(item for item in report["results"] if item["name"] == "procedural-memory-distillation")
        self.assertEqual(report["recall"], 1.0)
        self.assertIn("category_sweep", target["routes"])
        self.assertIn("direct_id", target["routes"])

    def test_failed_query_is_persisted_and_resolved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PaperStore(Path(tmpdir) / "state.sqlite3")
            store.record_failed_query("agent_memory", "arxiv", "all:procedural and all:memory", 10, "http")
            rows = store.retryable_failed_queries("agent_memory", include_not_due=True)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0].attempt_count, 1)
            store.resolve_failed_query("agent_memory", "arxiv", rows[0].normalized_query, 10)
            self.assertEqual(store.failed_queries("agent_memory"), [])

    def test_due_failed_query_is_retried_and_resolved_by_later_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            config = ScoutConfig(
                terms=["procedural memory"],
                track_id="agent_memory",
                days=10,
                discovery_queries={"arxiv": (DiscoveryQuery("procedural memory"),)},
                query_budgets={"arxiv": 1},
                sqlite_path=root / "state.sqlite3",
                digest_dir=root / "digests",
                report_dir=root / "reports",
            )
            run_scout(config, fetchers=[FailingArxivFetcher()], digest_date="2026-07-13", notifications_enabled=False)
            with sqlite3.connect(config.sqlite_path) as db:
                db.execute("UPDATE failed_queries SET next_retry_at = '2000-01-01T00:00:00+00:00'")
            result = run_scout(config, fetchers=[StaticFetcher()], digest_date="2026-07-14", notifications_enabled=False)
            self.assertEqual(result.failed_query_retry_count, 1)
            self.assertEqual(PaperStore(config.sqlite_path).failed_queries("agent_memory"), [])

    def test_backfill_recovers_old_paper_without_notifications(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            config = ScoutConfig(
                terms=["procedural memory"],
                track_id="agent_memory",
                discovery_queries={"arxiv": (DiscoveryQuery("procedural memory"),)},
                query_budgets={"arxiv": 1},
                sqlite_path=root / "state.sqlite3",
                digest_dir=root / "digests",
                report_dir=root / "reports",
            )
            result = run_backfill(config, days=45, sources={"arxiv"}, report_date="2026-07-14", fetchers=[StaticFetcher()])
            store = PaperStore(config.sqlite_path)
            self.assertEqual(store.paper_count(), 1)
            self.assertEqual(store.get_notified_for_date("2026-07-14"), [])
            self.assertIn("Newly recovered: 1", result.digest_path.read_text(encoding="utf-8"))

    def test_backfill_does_not_duplicate_existing_notification(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            config = ScoutConfig(
                terms=["procedural memory"],
                discovery_queries={"arxiv": (DiscoveryQuery("procedural memory"),)},
                query_budgets={"arxiv": 1},
                sqlite_path=root / "state.sqlite3",
                digest_dir=root / "digests",
                report_dir=root / "reports",
            )
            first = run_scout(config, fetchers=[StaticFetcher()], digest_date="2026-07-13", notifier=lambda _: True)
            backfill = run_backfill(config, days=45, sources={"arxiv"}, report_date="2026-07-14", fetchers=[StaticFetcher()])
            self.assertEqual(first.new_digest_count, 1)
            self.assertEqual(backfill.new_digest_count, 0)
            self.assertEqual(len(PaperStore(config.sqlite_path).get_notified_for_date("2026-07-13")), 1)

    def test_direct_ingestion_deduplicates_and_tracks_are_isolated(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            agent = ScoutConfig(terms=[], track_id="agent_memory", sqlite_path=root / "agent.sqlite3")
            deep = ScoutConfig(terms=[], track_id="deep_research", relevance_profile="deep_research", sqlite_path=root / "deep.sqlite3")
            first = ingest_candidate(agent, TARGET)
            second = ingest_candidate(agent, TARGET)
            self.assertEqual(first[0], "new")
            self.assertEqual(second[0], "already_known")
            self.assertEqual(PaperStore(agent.sqlite_path).paper_count(), 1)
            self.assertEqual(PaperStore(deep.sqlite_path).paper_count(), 0)

    def test_category_sweep_candidate_is_locally_screened(self):
        irrelevant = PaperCandidate(
            title="CUDA Memory Allocation",
            authors=["A"],
            abstract="GPU memory bandwidth optimization.",
            source="arxiv",
            source_id="x",
        )
        self.assertEqual(classify_with_rules(irrelevant).decision, "irrelevant")


if __name__ == "__main__":
    unittest.main()
