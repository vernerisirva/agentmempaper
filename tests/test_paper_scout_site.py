import tempfile
import unittest
from pathlib import Path

from paper_scout.site import build_site


SAMPLE_DIGEST = """# Paper Scout Digest - 2026-06-26

## Run Summary

- **Run ID:** 9
- **Candidates fetched:** 12
- **New unique papers:** 3
- **Relevant:** 1
- **Maybe relevant:** 1
- **Irrelevant:** 10
- **Source summary:** arxiv: 2, openalex: 10, semantic_scholar: 0

## Source Warnings

- semantic_scholar failed for 'agent memory': Semantic Scholar rate limit (HTTP 429). This is expected without SEMANTIC_SCHOLAR_API_KEY.

## Highly Relevant

### [Persistent Memory for LLM Agents](https://example.test/persistent)

- **Authors:** Ada Lovelace, Grace Hopper
- **Date:** 2026-06-26
- **Source:** arxiv
- **Relevance:** relevant (94/100)
- **Reason:** Directly studies persistent memory for LLM agents.
- **Tags:** agent-memory, persistent-memory
- **Abstract summary:** A compact summary of persistent memory for LLM agents.

## Maybe Relevant

### [Deep Research Agent Retrieval Memory](https://example.test/maybe)

- **Authors:** Jane Smith
- **Date:** 2026-06-25
- **Source:** openalex
- **Relevance:** maybe (48/100)
- **Reason:** Deep research agent retrieval may connect to persistent memory.
- **Tags:** deep-research, retrieval
- **Abstract summary:** A compact summary of retrieval memory for deep research agents.
"""


class PaperScoutSiteTest(unittest.TestCase):
    def test_generates_static_dashboard_files_and_latest_pointer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")
            (report_dir / "digest-quality-2026-06-26.md").write_text(
                "# Paper Scout Digest Quality - 2026-06-26\n\n- Likely false positives flagged: 2\n",
                encoding="utf-8",
            )

            result = build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir)

            self.assertTrue(result.built)
            self.assertEqual(result.latest_date, "2026-06-26")
            self.assertTrue((docs_dir / "index.html").exists())
            self.assertTrue((docs_dir / "latest.html").exists())
            self.assertTrue((docs_dir / "archive.html").exists())
            self.assertTrue((docs_dir / "data" / "papers.json").exists())
            self.assertTrue((docs_dir / "data" / "latest.json").exists())
            self.assertTrue((docs_dir / "style.css").exists())
            self.assertTrue((digest_dir / "latest.md").exists())

    def test_paper_cards_include_required_fields_and_compact_warnings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir)

            html = (docs_dir / "latest.html").read_text(encoding="utf-8")
            self.assertIn("Persistent Memory for LLM Agents", html)
            self.assertIn("2026-06-26", html)
            self.assertIn("arxiv", html)
            self.assertIn("94/100", html)
            self.assertIn("Directly studies persistent memory for LLM agents.", html)
            self.assertIn("agent-memory", html)
            self.assertIn("https://example.test/persistent", html)
            self.assertIn("<details", html)
            self.assertIn("Source warnings", html)
            self.assertIn("Copy citation", html)

    def test_build_site_exits_gracefully_when_no_digest_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            result = build_site(
                digest_dir=root / "digests",
                report_dir=root / "reports" / "paper_scout",
                docs_dir=root / "docs",
            )

            self.assertFalse(result.built)
            self.assertIn("No daily digest files found", result.message)
            self.assertFalse((root / "docs" / "index.html").exists())

    def test_generated_site_redacts_token_shaped_secrets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            secret = "sk-proj-abcdefghijklmnopqrstuvwxyz1234567890"
            digest = SAMPLE_DIGEST.replace(
                "## Highly Relevant",
                f"- semantic_scholar failed with accidental token {secret}\n\n## Highly Relevant",
            )
            (digest_dir / "2026-06-26.md").write_text(digest, encoding="utf-8")

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir)

            html = (docs_dir / "latest.html").read_text(encoding="utf-8")
            latest_json = (docs_dir / "data" / "latest.json").read_text(encoding="utf-8")
            self.assertNotIn(secret, html)
            self.assertNotIn(secret, latest_json)


if __name__ == "__main__":
    unittest.main()
