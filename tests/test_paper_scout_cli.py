import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from paper_scout.cli import main
from paper_scout.models import PaperCandidate
from paper_scout.site import SiteBuildResult


class PaperScoutCliTest(unittest.TestCase):
    def test_ingest_paper_by_arxiv_id_uses_normal_classification_and_state(self):
        candidate = PaperCandidate(
            title="Procedural Memory Distillation: Online Reflection for Self-Improving Language Models",
            authors=["Ada"],
            abstract="Cross-episode signals create reusable procedural memory distilled into language model weights.",
            source="arxiv",
            source_id="2607.01480",
            arxiv_id="2607.01480",
            published_date="2026-07-01",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            state_path = Path(tmpdir) / "state.sqlite3"
            config_path.write_text(f'state:\n  sqlite_path: "{state_path}"\n', encoding="utf-8")
            output = io.StringIO()
            with patch("paper_scout.cli.ArxivFetcher.fetch_by_id", return_value=candidate), redirect_stdout(output):
                code = main(["--config", str(config_path), "ingest-paper", "--arxiv-id", "2607.01480"])
            self.assertEqual(code, 0)
            self.assertIn("status=new", output.getvalue())
            self.assertIn("decision=relevant", output.getvalue())

    def test_evaluate_discovery_command_writes_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "discovery.md"
            with patch("paper_scout.cli.write_discovery_report", return_value=report_path), redirect_stdout(io.StringIO()):
                code = main(["--config", "config/tracks/agent_memory.yaml", "evaluate-discovery", "--date", "2026-07-14"])
            self.assertEqual(code, 0)

    def test_smoke_live_accepts_ci_flag(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "missing.yaml"
            with patch("paper_scout.cli.run_live_smoke") as run_live_smoke:
                run_live_smoke.return_value = {
                    "candidate_count": 0,
                    "unique_count": 0,
                    "source_failures": [],
                    "report_path": str(Path(tmpdir) / "reports" / "live-smoke-2026-06-26.md"),
                }

                with redirect_stdout(io.StringIO()):
                    exit_code = main(
                        [
                            "--config",
                            str(config_path),
                            "smoke-live",
                            "--days",
                            "14",
                            "--max-results-per-source",
                            "25",
                            "--no-notify",
                            "--ci",
                            "--date",
                            "2026-06-26",
                        ]
                    )

            self.assertEqual(exit_code, 0)
            self.assertTrue(run_live_smoke.call_args.kwargs["ci"])
            self.assertEqual(run_live_smoke.call_args.kwargs["days"], 14)
            self.assertEqual(run_live_smoke.call_args.kwargs["max_results_per_source"], 25)

    def test_build_site_invokes_static_generator(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "missing.yaml"
            docs_dir = Path(tmpdir) / "docs"
            with patch("paper_scout.cli.build_site") as build_site:
                build_site.return_value = SiteBuildResult(
                    built=True,
                    message="Built Paper Scout dashboard",
                    latest_date="2026-06-26",
                    output_dir=docs_dir,
                )

                output = io.StringIO()
                with redirect_stdout(output):
                    exit_code = main(
                        [
                            "--config",
                            str(config_path),
                            "build-site",
                            "--docs-dir",
                            str(docs_dir),
                        ]
                    )

            self.assertEqual(exit_code, 0)
            self.assertIn("Built Paper Scout dashboard", output.getvalue())
            self.assertEqual(build_site.call_args.kwargs["docs_dir"], docs_dir)

    def test_build_site_uses_track_specific_defaults(self):
        with patch("paper_scout.cli.build_site") as build_site:
            build_site.return_value = SiteBuildResult(
                built=True,
                message="Built deep research dashboard",
                latest_date="2026-06-26",
                output_dir=Path("docs/deep-research"),
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(["build-site", "--track", "deep_research"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Built deep research dashboard", output.getvalue())
        self.assertEqual(build_site.call_args.kwargs["docs_dir"], Path("docs/deep-research"))
        self.assertEqual(build_site.call_args.kwargs["digest_dir"], Path("digests/deep_research"))
        self.assertEqual(build_site.call_args.kwargs["report_dir"], Path("reports/paper_scout/deep_research"))
        self.assertEqual(build_site.call_args.kwargs["state_path"], Path("data/deep_research/paper_scout.sqlite3"))
        self.assertEqual(build_site.call_args.kwargs["relevance_profile"], "deep_research")

    def test_explain_paper_reports_rule_matches_for_arxiv_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "papers.json"
            data_path.write_text(
                json.dumps(
                    [
                        {
                            "title": "Are We Ready For An Agent-Native Memory System?",
                            "authors": ["Wei Zhou"],
                            "abstract_summary": "Memory for large language model agents supports storage, retrieval, update, and consolidation.",
                            "source": "arxiv",
                            "source_id": "2606.24775",
                            "arxiv_id": "2606.24775",
                            "url": "https://arxiv.org/abs/2606.24775",
                            "publication_date": "2026-06-23",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "explain-paper",
                        "--arxiv-id",
                        "2606.24775",
                        "--data-path",
                        str(data_path),
                    ]
                )

            text = output.getvalue()
            self.assertEqual(exit_code, 0)
            self.assertIn("Are We Ready For An Agent-Native Memory System?", text)
            self.assertIn("decision=relevant", text)
            self.assertIn("memory-systems", text)
            self.assertIn("agent-native memory", text)

    def test_explain_paper_can_find_generated_paper_by_doi(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "papers.json"
            data_path.write_text(
                json.dumps(
                    [
                        {
                            "title": "OpenClaw and Ollama in Agentic AI: Toward Fully Autonomous and Scalable AI Agent Systems",
                            "authors": ["Konstantinos I. Roumeliotis"],
                            "abstract_summary": "Agentic AI architecture with persistent, action-capable systems and orchestration layers.",
                            "source": "semantic_scholar",
                            "source_id": "openclaw",
                            "doi": "10.2139/ssrn.6584998",
                            "url": "https://www.semanticscholar.org/paper/openclaw",
                            "publication_date": "2026",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = main(
                    [
                        "explain-paper",
                        "--doi",
                        "10.2139/ssrn.6584998",
                        "--data-path",
                        str(data_path),
                    ]
                )

            text = output.getvalue()
            self.assertEqual(exit_code, 0)
            self.assertIn("Toward Fully Autonomous and Scalable AI Agent Systems", text)
            self.assertIn("decision=maybe", text)


if __name__ == "__main__":
    unittest.main()
