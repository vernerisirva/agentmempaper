import tempfile
import unittest
import logging
from pathlib import Path
from unittest.mock import patch

from paper_scout.config import ScoutConfig
from paper_scout.http import HttpRequestError
from paper_scout.models import PaperCandidate
from paper_scout.scout import run_scout
from paper_scout.validation import run_live_smoke, validate_idempotency


class FakeFetcher:
    source = "fake"

    def search(self, term, days, max_results):
        return [
            PaperCandidate(
                title="Persistent Memory for LLM Agents",
                authors=["Ada Lovelace"],
                abstract="Persistent episodic memory write and retrieval policies for LLM agents.",
                source="fake",
                source_id="fake-1",
                doi="10.1/fake",
                url="https://example.test/fake",
                published_date="2026-06-26",
            )
        ]


class FailingFetcher:
    source = "failing"

    def search(self, term, days, max_results):
        raise RuntimeError("temporary outage")


class SemanticScholarRateLimitedFetcher:
    source = "semantic_scholar"

    def search(self, term, days, max_results):
        raise HttpRequestError("http", "https://api.semanticscholar.org/graph/v1/paper/search", "HTTP Error 429")


class PaperScoutRunTest(unittest.TestCase):
    def test_run_survives_fetcher_failure_and_does_not_notify_twice(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ScoutConfig(
                terms=["agent memory"],
                days=7,
                max_results_per_source=5,
                sqlite_path=Path(tmpdir) / "state.sqlite3",
                digest_dir=Path(tmpdir) / "digests",
                report_dir=Path(tmpdir) / "reports",
            )

            logging.disable(logging.CRITICAL)
            try:
                first = run_scout(config, fetchers=[FailingFetcher(), FakeFetcher()], digest_date="2026-06-26")
                second = run_scout(config, fetchers=[FakeFetcher()], digest_date="2026-06-27")
            finally:
                logging.disable(logging.NOTSET)

            self.assertEqual(first.new_digest_count, 1)
            self.assertEqual(second.new_digest_count, 0)
            self.assertIn(
                "Persistent Memory for LLM Agents",
                first.digest_path.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "No new relevant or maybe-relevant papers found.",
                second.digest_path.read_text(encoding="utf-8"),
            )

    def test_semantic_scholar_429_is_clear_and_non_fatal(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ScoutConfig(
                terms=["agent memory"],
                days=7,
                max_results_per_source=5,
                sqlite_path=Path(tmpdir) / "state.sqlite3",
                digest_dir=Path(tmpdir) / "digests",
                report_dir=Path(tmpdir) / "reports",
            )

            logging.disable(logging.CRITICAL)
            try:
                result = run_scout(
                    config,
                    fetchers=[SemanticScholarRateLimitedFetcher(), FakeFetcher()],
                    digest_date="2026-06-26",
                )
            finally:
                logging.disable(logging.NOTSET)

            digest = result.digest_path.read_text(encoding="utf-8")

            self.assertEqual(result.new_digest_count, 1)
            self.assertIn("Semantic Scholar returned HTTP 429", digest)
            self.assertIn("Configure SEMANTIC_SCHOLAR_API_KEY for higher rate limits.", digest)
            self.assertIn("The run continued with other sources.", digest)
            self.assertNotIn("expected without SEMANTIC_SCHOLAR_API_KEY", digest)

    def test_semantic_scholar_429_mentions_api_key_when_present(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ScoutConfig(
                terms=["agent memory"],
                days=7,
                max_results_per_source=5,
                sqlite_path=Path(tmpdir) / "state.sqlite3",
                digest_dir=Path(tmpdir) / "digests",
                report_dir=Path(tmpdir) / "reports",
            )

            logging.disable(logging.CRITICAL)
            try:
                with patch.dict("os.environ", {"SEMANTIC_SCHOLAR_API_KEY": "test-key"}):
                    result = run_scout(
                        config,
                        fetchers=[SemanticScholarRateLimitedFetcher(), FakeFetcher()],
                        digest_date="2026-06-26",
                    )
            finally:
                logging.disable(logging.NOTSET)

            digest = result.digest_path.read_text(encoding="utf-8")

            self.assertIn("Semantic Scholar returned HTTP 429 despite an API key", digest)
            self.assertIn("query volume was high", digest)
            self.assertIn("The run continued with other sources.", digest)
            self.assertNotIn("expected without SEMANTIC_SCHOLAR_API_KEY", digest)

    def test_run_writes_digest_quality_report_without_failing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ScoutConfig(
                terms=["agent memory"],
                days=7,
                max_results_per_source=5,
                sqlite_path=Path(tmpdir) / "state.sqlite3",
                digest_dir=Path(tmpdir) / "digests",
                report_dir=Path(tmpdir) / "reports",
            )

            logging.disable(logging.CRITICAL)
            try:
                result = run_scout(config, fetchers=[FakeFetcher()], digest_date="2026-06-26")
            finally:
                logging.disable(logging.NOTSET)

            quality_report = Path(tmpdir) / "reports" / "digest-quality-2026-06-26.md"
            self.assertEqual(result.new_digest_count, 1)
            self.assertTrue(quality_report.exists())

    def test_notification_failure_does_not_mark_papers_notified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ScoutConfig(
                terms=["agent memory"],
                days=7,
                max_results_per_source=5,
                sqlite_path=Path(tmpdir) / "state.sqlite3",
                digest_dir=Path(tmpdir) / "digests",
                report_dir=Path(tmpdir) / "reports",
            )

            def failing_notifier(markdown):
                return False

            logging.disable(logging.CRITICAL)
            try:
                result = run_scout(
                    config,
                    fetchers=[FakeFetcher()],
                    digest_date="2026-06-26",
                    notifier=failing_notifier,
                )
                repeat = run_scout(config, fetchers=[FakeFetcher()], digest_date="2026-06-27")
            finally:
                logging.disable(logging.NOTSET)

            self.assertEqual(result.new_digest_count, 1)
            self.assertEqual(repeat.new_digest_count, 1)

    def test_validate_idempotency_reports_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report = validate_idempotency(Path(tmpdir), report_date="2026-06-26")

            self.assertTrue(report["passed"])
            self.assertTrue(report["same_paper_from_multiple_sources"])
            self.assertEqual(report["first_digest_count"], 2)
            self.assertEqual(report["second_digest_count"], 0)

    def test_live_smoke_with_mocked_fetchers_reports_failures_and_no_notifications(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ScoutConfig(
                terms=["agent memory"],
                days=14,
                max_results_per_source=25,
                sqlite_path=Path(tmpdir) / "state.sqlite3",
                digest_dir=Path(tmpdir) / "digests",
                report_dir=Path(tmpdir) / "reports",
            )

            report = run_live_smoke(
                config,
                fetchers=[FailingFetcher(), FakeFetcher()],
                report_date="2026-06-26",
            )

            self.assertEqual(report["source_counts"]["fake"], 1)
            self.assertEqual(len(report["source_failures"]), 1)
            self.assertTrue(report["state_initialized"])
            self.assertTrue(report["idempotency_passed"])
            self.assertTrue((Path(tmpdir) / "reports" / "live-smoke-2026-06-26.md").exists())


if __name__ == "__main__":
    unittest.main()
