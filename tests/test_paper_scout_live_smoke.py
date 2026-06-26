import json
import os
import sqlite3
import ssl
import tempfile
import unittest
from pathlib import Path
from urllib.error import URLError
from unittest.mock import patch

from paper_scout.config import ScoutConfig
from paper_scout.http import HttpRequestError
from paper_scout.models import PaperCandidate
from paper_scout.validation import run_live_smoke


class SuccessfulFetcher:
    source = "fixture_success"

    def search(self, term, days, max_results):
        return [
            PaperCandidate(
                title="Agent Memory Benchmark for Deep Research Agents",
                authors=["Ada Lovelace"],
                abstract="An agent memory benchmark for long-term memory in deep research agents.",
                source=self.source,
                source_id="success-1",
                url="https://example.test/success-1",
                published_date="2026-06-25",
            )
        ]


class ZeroFetcher:
    source = "fixture_zero"

    def search(self, term, days, max_results):
        return []


class TlsFailingFetcher:
    source = "fixture_tls"

    def search(self, term, days, max_results):
        raise URLError(ssl.SSLCertVerificationError("certificate verify failed: unable to get local issuer certificate"))


class HttpFailingFetcher:
    source = "fixture_http"

    def search(self, term, days, max_results):
        raise HttpRequestError("http", "https://example.test/api", "503 service unavailable")


class ParsingFailingFetcher:
    source = "fixture_parse"

    def search(self, term, days, max_results):
        raise ValueError("invalid source payload")


def smoke_config(tmpdir: str) -> ScoutConfig:
    return ScoutConfig(
        terms=["agent memory"],
        days=14,
        max_results_per_source=25,
        sqlite_path=Path(tmpdir) / "state.sqlite3",
        digest_dir=Path(tmpdir) / "digests",
        report_dir=Path(tmpdir) / "reports",
    )


class PaperScoutLiveSmokeTest(unittest.TestCase):
    def test_ci_mode_writes_json_report_and_markdown_sample_candidate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report = run_live_smoke(
                smoke_config(tmpdir),
                fetchers=[SuccessfulFetcher()],
                report_date="2026-06-26",
                ci=True,
            )

            json_path = Path(tmpdir) / "reports" / "live-smoke-2026-06-26.json"
            markdown_path = Path(tmpdir) / "reports" / "live-smoke-2026-06-26.md"
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            markdown = markdown_path.read_text(encoding="utf-8")

            self.assertEqual(report["json_report_path"], str(json_path))
            self.assertTrue(payload["ci"])
            self.assertEqual(payload["sources_attempted"], 1)
            self.assertEqual(payload["sources_succeeded"], 1)
            self.assertEqual(payload["sources_failed"], 0)
            self.assertEqual(payload["total_raw_records"], 1)
            self.assertEqual(payload["total_candidates"], 1)
            self.assertEqual(payload["unique_candidates"], 1)
            self.assertEqual(payload["relevant_count"], 1)
            self.assertEqual(payload["source_errors"], [])
            self.assertIn("fixture_success", markdown)
            self.assertIn("Success", markdown)
            self.assertIn("Raw records: 1", markdown)
            self.assertIn("Converted candidates: 1", markdown)
            self.assertIn("Agent Memory Benchmark for Deep Research Agents", markdown)
            self.assertIn("Abstract: yes", markdown)

    def test_zero_results_are_success_not_source_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report = run_live_smoke(
                smoke_config(tmpdir),
                fetchers=[ZeroFetcher()],
                report_date="2026-06-26",
                ci=True,
            )

            self.assertEqual(report["sources_succeeded"], 1)
            self.assertEqual(report["sources_failed"], 0)
            self.assertEqual(report["source_errors"], [])
            self.assertEqual(report["source_results"][0]["status"], "zero_results")

    def test_source_failures_are_classified_without_becoming_zero_results(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report = run_live_smoke(
                smoke_config(tmpdir),
                fetchers=[TlsFailingFetcher(), HttpFailingFetcher(), ParsingFailingFetcher()],
                report_date="2026-06-26",
                ci=True,
            )

            error_types = {error["source"]: error["type"] for error in report["source_errors"]}
            self.assertEqual(report["sources_succeeded"], 0)
            self.assertEqual(report["sources_failed"], 3)
            self.assertEqual(error_types["fixture_tls"], "tls")
            self.assertEqual(error_types["fixture_http"], "http")
            self.assertEqual(error_types["fixture_parse"], "parsing")

            markdown = (Path(tmpdir) / "reports" / "live-smoke-2026-06-26.md").read_text(encoding="utf-8")
            self.assertIn("TLS/certificate error", markdown)
            self.assertIn("HTTP/API error", markdown)
            self.assertIn("Parsing/conversion error", markdown)

    def test_smoke_live_does_not_notify_or_mark_notified(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config = smoke_config(tmpdir)

            with patch.dict(os.environ, {"PAPER_SCOUT_WEBHOOK_URL": "https://example.test/webhook"}):
                with patch("paper_scout.http.HttpClient.post_json") as post_json:
                    run_live_smoke(
                        config,
                        fetchers=[SuccessfulFetcher()],
                        report_date="2026-06-26",
                        ci=True,
                    )

            post_json.assert_not_called()

            with sqlite3.connect(config.sqlite_path) as db:
                notification_count = db.execute("SELECT COUNT(*) FROM notifications").fetchone()[0]
                paper_count = db.execute("SELECT COUNT(*) FROM papers").fetchone()[0]

            self.assertEqual(notification_count, 0)
            self.assertEqual(paper_count, 0)


if __name__ == "__main__":
    unittest.main()
