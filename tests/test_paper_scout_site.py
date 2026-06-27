import tempfile
import unittest
import json
import re
from pathlib import Path

from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.site import build_site
from paper_scout.state import PaperStore


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


def _visible_card_html(html: str, title_slug: str) -> str:
    match = re.search(
        rf'<article class="paper-card[^"]*"[^>]+data-title="{re.escape(title_slug)}"[^>]*>(.*?)<details class="paper-more">',
        html,
        flags=re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Could not find visible card for {title_slug!r}")
    return match.group(1)


class PaperScoutSiteTest(unittest.TestCase):
    def _write_state_fixture(self, state_path: Path) -> None:
        store = PaperStore(state_path)
        old_run_id = store.start_run(days=7)
        old_candidate = PaperCandidate(
            title="Older Episodic Memory for Agents",
            authors=["Alan Turing"],
            abstract="A study of episodic memory for autonomous LLM agents.",
            source="semantic_scholar",
            source_id="s2-old",
            semantic_scholar_id="s2-old",
            url="https://example.test/old",
            published_date="2025-12-15",
            raw={"paperId": "s2-old"},
        )
        old_key = store.upsert_paper(
            old_candidate,
            ClassificationResult(
                score=88,
                decision="relevant",
                reason="Studies episodic memory for autonomous agents.",
                tags=["episodic-memory", "agent-memory"],
                abstract_summary="Older but relevant autonomous-agent memory work.",
            ),
        )
        store.record_sighting(old_run_id, old_key, old_candidate, "episodic memory LLM agent")
        store.finish_run(old_run_id, fetched_count=1, new_count=1, notified_count=1)
        store.mark_notified([old_key], "2026-06-25")

        latest_run_id = store.start_run(days=7)
        latest_candidate = PaperCandidate(
            title="Latest Deep Research Memory",
            authors=["Ada Lovelace", "Grace Hopper"],
            abstract="Persistent semantic memory for deep research agents.",
            source="openalex",
            source_id="W123",
            doi="10.1234/latest",
            openalex_id="W123",
            url="https://example.test/latest",
            published_date=None,
            raw={"id": "W123"},
        )
        latest_key = store.upsert_paper(
            latest_candidate,
            ClassificationResult(
                score=51,
                decision="maybe",
                reason="Connects semantic memory to deep research agents.",
                tags=["deep-research", "semantic-memory"],
                abstract_summary="A latest-run paper about semantic memory for research agents.",
            ),
        )
        store.record_sighting(latest_run_id, latest_key, latest_candidate, "deep research agent memory")
        duplicate_candidate = PaperCandidate(
            title="Latest Deep Research Memory",
            authors=["Ada Lovelace", "Grace Hopper"],
            abstract="Persistent semantic memory for deep research agents.",
            source="arxiv",
            source_id="2606.12345",
            doi="10.1234/latest-v2",
            arxiv_id="2606.12345",
            url="https://arxiv.org/abs/2606.12345",
            published_date=None,
            raw={"id": "2606.12345"},
        )
        duplicate_key = store.upsert_paper(
            duplicate_candidate,
            ClassificationResult(
                score=76,
                decision="relevant",
                reason="A duplicate source variant with a stronger agent-memory score.",
                tags=["deep-research", "agent-memory"],
                abstract_summary="A duplicate latest-run paper variant from arXiv.",
            ),
        )
        store.record_sighting(latest_run_id, duplicate_key, duplicate_candidate, "deep research agent memory")
        store.finish_run(latest_run_id, fetched_count=1, new_count=1, notified_count=1)
        store.mark_notified([latest_key], "2026-06-26")

    def _write_ranking_fixture(self, state_path: Path) -> None:
        store = PaperStore(state_path)
        run_id = store.start_run(days=7)
        examples = [
            (
                PaperCandidate(
                    title="Maybe Future Memory Paper",
                    authors=["Future Author"],
                    abstract="A maybe relevant future-dated memory paper.",
                    source="openalex",
                    source_id="future",
                    url="https://example.test/future",
                    published_date="2026-07-04",
                    raw={},
                ),
                ClassificationResult(45, "maybe", "May touch agent memory.", ["long-term-memory"], "Future-dated maybe paper."),
            ),
            (
                PaperCandidate(
                    title="Future Source Relevant Memory Paper",
                    authors=["Future Relevant Author"],
                    abstract="A relevant paper with a future source-provided publication date.",
                    source="openalex",
                    source_id="future-relevant",
                    url="https://example.test/future-relevant",
                    published_date="2026-07-05",
                    raw={},
                ),
                ClassificationResult(50, "relevant", "Relevant but future-dated by source metadata.", ["agent-memory"], "Future source date relevant paper."),
            ),
            (
                PaperCandidate(
                    title="Fresh First Seen Agent Memory",
                    authors=["No Date Author"],
                    abstract="A relevant paper without a publication date, first seen in the current run.",
                    source="openalex",
                    source_id="fresh-first-seen",
                    url="https://example.test/fresh-first-seen",
                    published_date=None,
                    raw={},
                ),
                ClassificationResult(70, "relevant", "Relevant and missing publication date.", ["agent-memory"], "Fresh first-seen relevant paper."),
            ),
            (
                PaperCandidate(
                    title="Newer Low Score Agent Memory",
                    authors=["Recent Author"],
                    abstract="A newer relevant paper with a lower score than older relevant papers.",
                    source="arxiv",
                    source_id="newer-low-score",
                    url="https://example.test/newer-low-score",
                    published_date="2026-06-21",
                    raw={},
                ),
                ClassificationResult(70, "relevant", "Newer relevant work should rank before older high-score papers.", ["agent-memory"], "Newer lower-score relevant paper."),
            ),
            (
                PaperCandidate(
                    title="Core Agent Memory Architecture",
                    authors=["Ada Lovelace"],
                    abstract="Long-term memory architecture and read/write policies for LLM agents.",
                    source="arxiv",
                    source_id="core",
                    arxiv_id="2606.11111",
                    url="https://example.test/core",
                    published_date="2026-06-20",
                    raw={},
                ),
                ClassificationResult(
                    91,
                    "relevant",
                    "Studies long-term memory architecture for LLM agents.",
                    ["agent-memory", "memory-policy", "long-term-memory", "procedural-memory", "benchmark"],
                    "Core agent memory architecture.",
                ),
            ),
            (
                PaperCandidate(
                    title="Memory Benchmark for Agents",
                    authors=["Grace Hopper"],
                    abstract="Benchmark for evaluating persistent memory in autonomous agents.",
                    source="semantic_scholar",
                    source_id="benchmark",
                    semantic_scholar_id="benchmark",
                    url="https://example.test/benchmark",
                    published_date="2026-06-18",
                    raw={},
                ),
                ClassificationResult(86, "relevant", "Evaluates persistent memory in agents.", ["benchmark", "agent-memory"], "Agent-memory benchmark."),
            ),
            (
                PaperCandidate(
                    title="Same Date Higher Score Agent Memory",
                    authors=["Tie Break Author"],
                    abstract="A relevant paper sharing a publication date with a lower-scored paper.",
                    source="arxiv",
                    source_id="same-date-high",
                    url="https://example.test/same-date-high",
                    published_date="2026-06-17",
                    raw={},
                ),
                ClassificationResult(82, "relevant", "Higher relevance should break same-date ties.", ["agent-memory"], "Same-date higher-score paper."),
            ),
            (
                PaperCandidate(
                    title="Same Date Lower Score Agent Memory",
                    authors=["Tie Break Author"],
                    abstract="A relevant paper sharing a publication date with a higher-scored paper.",
                    source="arxiv",
                    source_id="same-date-low",
                    url="https://example.test/same-date-low",
                    published_date="2026-06-17",
                    raw={},
                ),
                ClassificationResult(60, "relevant", "Lower relevance should follow on same-date ties.", ["agent-memory"], "Same-date lower-score paper."),
            ),
            (
                PaperCandidate(
                    title="Alpha Stable Tie Agent Memory",
                    authors=["Stable Sort Author"],
                    abstract="A relevant paper with the same date and score as another paper.",
                    source="openalex",
                    source_id="alpha-stable",
                    url="https://example.test/alpha-stable",
                    published_date="2026-06-16",
                    raw={},
                ),
                ClassificationResult(65, "relevant", "Title should break final ties.", ["agent-memory"], "Alphabetical stable tie paper."),
            ),
            (
                PaperCandidate(
                    title="Zulu Stable Tie Agent Memory",
                    authors=["Stable Sort Author"],
                    abstract="A relevant paper with the same date and score as another paper.",
                    source="openalex",
                    source_id="zulu-stable",
                    url="https://example.test/zulu-stable",
                    published_date="2026-06-16",
                    raw={},
                ),
                ClassificationResult(65, "relevant", "Title should break final ties.", ["agent-memory"], "Alphabetical stable tie paper."),
            ),
            (
                PaperCandidate(
                    title="Pinned Thesis Candidate",
                    authors=["Katherine Johnson"],
                    abstract="Procedural memory for tool-using research agents.",
                    source="openalex",
                    source_id="pinned",
                    openalex_id="W999",
                    url="https://example.test/pinned",
                    published_date="2025-11-01",
                    raw={},
                ),
                ClassificationResult(64, "maybe", "May inform procedural memory in research agents.", ["deep-research"], "Possible thesis candidate."),
            ),
            (
                PaperCandidate(
                    title="Excluded False Positive",
                    authors=["Cache Engineer"],
                    abstract="Cache memory optimization with no agent memory.",
                    source="openalex",
                    source_id="excluded",
                    url="https://example.test/excluded",
                    published_date="2026-06-19",
                    raw={},
                ),
                ClassificationResult(41, "maybe", "Touches memory terms.", ["long-term-memory"], "False positive."),
            ),
        ]
        for candidate, classification in examples:
            key = store.upsert_paper(candidate, classification)
            store.record_sighting(run_id, key, candidate, "agent memory")
        store.finish_run(run_id, fetched_count=len(examples), new_count=len(examples), notified_count=len(examples))

    def test_generates_static_dashboard_files_and_latest_pointer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            state_path = root / "data" / "paper_scout.sqlite3"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            self._write_state_fixture(state_path)
            (digest_dir / "2026-06-25.md").write_text(
                SAMPLE_DIGEST.replace("2026-06-26", "2026-06-25"),
                encoding="utf-8",
            )
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")
            (report_dir / "digest-quality-2026-06-26.md").write_text(
                "# Paper Scout Digest Quality - 2026-06-26\n\n- Likely false positives flagged: 2\n",
                encoding="utf-8",
            )

            result = build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir, state_path=state_path)

            self.assertTrue(result.built)
            self.assertEqual(result.latest_date, "2026-06-26")
            self.assertTrue((docs_dir / "index.html").exists())
            self.assertTrue((docs_dir / "latest.html").exists())
            self.assertTrue((docs_dir / "archive.html").exists())
            self.assertTrue((docs_dir / "about.html").exists())
            self.assertTrue((docs_dir / "data" / "papers.json").exists())
            self.assertTrue((docs_dir / "data" / "latest.json").exists())
            self.assertTrue((docs_dir / "data" / "papers.csv").exists())
            self.assertTrue((docs_dir / "data" / "papers.bib").exists())
            self.assertTrue((docs_dir / "style.css").exists())
            self.assertTrue((digest_dir / "latest.md").exists())
            html = (docs_dir / "index.html").read_text(encoding="utf-8")
            archive_html = (docs_dir / "archive.html").read_text(encoding="utf-8")
            self.assertIn("Agentic Memory Paper Library", html)
            self.assertIn("A daily updated library of papers on agentic memory, deep research agents, and memory mechanisms.", html)
            self.assertIn("Updated 2026-06-26", html)
            self.assertIn("2 papers", html)
            self.assertIn("2 highly relevant", html)
            self.assertIn("Highly relevant", html)
            self.assertNotIn("Recommended reading", html)
            self.assertNotIn("Full library", html)
            self.assertNotIn("New in latest run", html)
            self.assertNotIn("Source warning count", html)
            self.assertNotIn("Candidates fetched", html.split("</header>", 1)[0])
            self.assertNotIn("Run ID", html.split("</header>", 1)[0])
            self.assertIn('<option value="latest-relevant" selected>Latest relevant</option>', html)
            self.assertIn("First seen", html)
            self.assertIn("2026-06-25", archive_html)
            self.assertIn("2026-06-26", archive_html)
            self.assertIn("daily digests are kept for provenance", archive_html)

    def test_cumulative_library_data_and_latest_discoveries_are_split(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            state_path = root / "data" / "paper_scout.sqlite3"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            self._write_state_fixture(state_path)
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir, state_path=state_path)

            papers_json = (docs_dir / "data" / "papers.json").read_text(encoding="utf-8")
            latest_json = (docs_dir / "data" / "latest.json").read_text(encoding="utf-8")
            self.assertIn("Older Episodic Memory for Agents", papers_json)
            self.assertIn("Latest Deep Research Memory", papers_json)
            self.assertIn("\"first_seen_date\"", papers_json)
            self.assertIn("\"appeared_in_latest_run\": true", papers_json)
            self.assertIn("\"doi\": \"10.1234/latest-v2\"", papers_json)
            self.assertIn("https://doi.org/10.1234/latest", papers_json)
            self.assertIn("\"newly_discovered_papers\"", latest_json)
            self.assertIn("Latest Deep Research Memory", latest_json)
            self.assertNotIn("Older Episodic Memory for Agents", latest_json)

    def test_duplicate_title_variants_are_collapsed_with_sources_and_urls_preserved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            state_path = root / "data" / "paper_scout.sqlite3"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            self._write_state_fixture(state_path)
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir, state_path=state_path)

            papers_json = (docs_dir / "data" / "papers.json").read_text(encoding="utf-8")
            index_html = (docs_dir / "index.html").read_text(encoding="utf-8")
            self.assertEqual(papers_json.count('"title": "Latest Deep Research Memory"'), 1)
            self.assertEqual(index_html.count('data-title="latest deep research memory"'), 1)
            self.assertIn('"sources": [', papers_json)
            self.assertIn('"arxiv"', papers_json)
            self.assertIn('"openalex"', papers_json)
            self.assertIn('"alternate_urls": [', papers_json)
            self.assertIn("https://example.test/latest", papers_json)
            self.assertIn("https://arxiv.org/abs/2606.12345", papers_json)
            self.assertIn("76/100", index_html)
            visible_card = _visible_card_html(index_html, "latest deep research memory")
            self.assertNotIn("/100", visible_card)
            self.assertNotIn("Memory architecture or policy", visible_card)
            self.assertIn("Screening details", index_html)

    def test_index_and_latest_pages_have_library_and_latest_run_framing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            state_path = root / "data" / "paper_scout.sqlite3"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            self._write_state_fixture(state_path)
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir, state_path=state_path)

            index_html = (docs_dir / "index.html").read_text(encoding="utf-8")
            latest_html = (docs_dir / "latest.html").read_text(encoding="utf-8")
            self.assertIn("Sort", index_html)
            self.assertIn("Latest relevant", index_html)
            self.assertIn("Newest relevant papers first.", index_html)
            self.assertIn("Publication date", index_html)
            self.assertIn("First seen", index_html)
            self.assertIn("Published", index_html)
            self.assertIn('<label class="select-field relevance-filter" for="relevance-filter">', index_html)
            self.assertIn('<option value="relevant" selected>Highly relevant</option>', index_html)
            self.assertIn('<option value="all">All papers</option>', index_html)
            self.assertIn('<option value="maybe">Maybe relevant</option>', index_html)
            self.assertNotIn('id="source-filters"', index_html)
            self.assertNotIn('id="tag-filter"', index_html)
            self.assertIn("Technical diagnostics", index_html)
            self.assertIn("Latest discoveries", latest_html)
            self.assertIn("Papers first seen in the latest Paper Scout run.", latest_html)
            self.assertIn("Latest Deep Research Memory", latest_html)
            self.assertNotIn("Older Episodic Memory for Agents", latest_html)

    def test_homepage_has_one_main_list_and_secondary_details(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            state_path = root / "data" / "paper_scout.sqlite3"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            self._write_state_fixture(state_path)
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir, state_path=state_path)

            html = (docs_dir / "index.html").read_text(encoding="utf-8")
            self.assertEqual(html.count('id="paper-list"'), 1)
            self.assertEqual(html.count('data-title="latest deep research memory"'), 1)
            self.assertNotIn("recommended-card", html)
            self.assertNotIn("recommended-section", html)
            self.assertLess(html.index("Search papers..."), html.index("Latest Deep Research Memory"))
            self.assertIn('<details class="technical-diagnostics">', html)
            self.assertIn("<summary>Technical diagnostics</summary>", html)
            self.assertIn('<details class="export-library">', html)
            self.assertLess(html.index("Latest Deep Research Memory"), html.index("Export library"))
            self.assertNotIn("Download CSV", html.split("</header>", 1)[0])

    def test_paper_cards_include_required_fields_and_secondary_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir, state_path=root / "data" / "missing.sqlite3")

            html = (docs_dir / "index.html").read_text(encoding="utf-8")
            papers_json = (docs_dir / "data" / "papers.json").read_text(encoding="utf-8")
            self.assertIn("Persistent Memory for LLM Agents", html)
            self.assertIn("2026-06-26", html)
            self.assertIn("arxiv", html)
            self.assertIn("Screening details", html)
            self.assertIn("Score: 94/100", html)
            self.assertIn('"relevance_score": 94', papers_json)
            self.assertIn("Directly studies persistent memory for LLM agents.", html)
            self.assertIn("agent-memory", html)
            self.assertIn("https://example.test/persistent", html)
            self.assertIn("Open paper", html)
            self.assertIn('<details class="paper-more">', html)
            self.assertIn("Copy citation", html)
            self.assertLess(html.index("Open paper"), html.index("Copy citation"))
            self.assertLess(html.index('<details class="paper-more">'), html.index("A compact summary of persistent memory for LLM agents."))
            self.assertRegex(
                html,
                r'<article class="paper-card compact"[^>]+data-title="deep research agent retrieval memory"[^>]+hidden>',
            )
            visible_card = _visible_card_html(html, "persistent memory for llm agents")
            self.assertIn("Why included", visible_card)
            self.assertIn("Published 2026-06-26", visible_card)
            self.assertIn("Source: arXiv", visible_card)
            self.assertNotIn("/100", visible_card)
            self.assertNotIn("Memory architecture or policy", visible_card)
            self.assertNotIn("agent-memory", visible_card)

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

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir, state_path=root / "data" / "missing.sqlite3")

            generated = [
                docs_dir / "index.html",
                docs_dir / "latest.html",
                docs_dir / "archive.html",
                docs_dir / "about.html",
                docs_dir / "data" / "latest.json",
                docs_dir / "data" / "papers.json",
                docs_dir / "data" / "papers.csv",
                docs_dir / "data" / "papers.bib",
            ]
            for path in generated:
                self.assertNotIn(secret, path.read_text(encoding="utf-8"))

    def test_latest_relevant_sort_future_dates_and_curation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            state_path = root / "data" / "paper_scout.sqlite3"
            curation_path = root / "config" / "curation.yaml"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            curation_path.parent.mkdir()
            self._write_ranking_fixture(state_path)
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")
            curation_path.write_text(
                """
pinned:
  - title: "Pinned Thesis Candidate"
    note: "Important thesis candidate for procedural memory in research agents."
    review_status: thesis_candidate
overrides:
  - title: "Pinned Thesis Candidate"
    decision: highly_relevant
    score: 93
    tags:
      - deep-research
      - procedural-memory
    note: "Manual review found this connects directly to deep research agent memory."
  - title: "Memory Benchmark for Agents"
    review_status: important
excluded:
  - title: "Excluded False Positive"
    reason: "False positive: cache optimization, not agent memory."
""",
                encoding="utf-8",
            )

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir, state_path=state_path, curation_path=curation_path)

            index_html = (docs_dir / "index.html").read_text(encoding="utf-8")
            papers = json.loads((docs_dir / "data" / "papers.json").read_text(encoding="utf-8"))
            titles = [paper["title"] for paper in papers]
            self.assertEqual(titles[0], "Fresh First Seen Agent Memory")
            self.assertLess(titles.index("Fresh First Seen Agent Memory"), titles.index("Future Source Relevant Memory Paper"))
            self.assertLess(titles.index("Newer Low Score Agent Memory"), titles.index("Core Agent Memory Architecture"))
            self.assertLess(titles.index("Core Agent Memory Architecture"), titles.index("Memory Benchmark for Agents"))
            self.assertLess(titles.index("Same Date Higher Score Agent Memory"), titles.index("Same Date Lower Score Agent Memory"))
            self.assertLess(titles.index("Alpha Stable Tie Agent Memory"), titles.index("Zulu Stable Tie Agent Memory"))
            self.assertLess(titles.index("Memory Benchmark for Agents"), titles.index("Pinned Thesis Candidate"))
            self.assertLess(titles.index("Core Agent Memory Architecture"), titles.index("Maybe Future Memory Paper"))
            self.assertNotIn("Excluded False Positive", index_html)
            self.assertIn("Research note", index_html)
            self.assertIn("Important thesis candidate for procedural memory in research agents.", index_html)
            self.assertIn("thesis_candidate", index_html)
            self.assertIn("Published: 2026-07-04 · source date", index_html)
            core_visible = _visible_card_html(index_html, "core agent memory architecture")
            self.assertNotIn("benchmark", core_visible)
            self.assertIn("benchmark", index_html)
            self.assertNotIn('class="maybe-separator"', index_html)
            future = next(paper for paper in papers if paper["title"] == "Maybe Future Memory Paper")
            future_relevant = next(paper for paper in papers if paper["title"] == "Future Source Relevant Memory Paper")
            pinned = next(paper for paper in papers if paper["title"] == "Pinned Thesis Candidate")
            self.assertTrue(future["future_date"])
            self.assertTrue(future_relevant["future_date"])
            self.assertTrue(pinned["pinned"])
            self.assertEqual(pinned["review_status"], "thesis_candidate")
            self.assertEqual(pinned["relevance_score"], 93)

    def test_about_page_and_exports_are_generated(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            report_dir = root / "reports" / "paper_scout"
            docs_dir = root / "docs"
            state_path = root / "data" / "paper_scout.sqlite3"
            digest_dir.mkdir()
            report_dir.mkdir(parents=True)
            self._write_state_fixture(state_path)
            (digest_dir / "2026-06-26.md").write_text(SAMPLE_DIGEST, encoding="utf-8")

            build_site(digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir, state_path=state_path)

            about_html = (docs_dir / "about.html").read_text(encoding="utf-8")
            csv_text = (docs_dir / "data" / "papers.csv").read_text(encoding="utf-8")
            bib_text = (docs_dir / "data" / "papers.bib").read_text(encoding="utf-8")
            self.assertIn("What Paper Scout tracks", about_html)
            self.assertIn("arXiv", about_html)
            self.assertIn("OpenAlex", about_html)
            self.assertIn("Semantic Scholar", about_html)
            self.assertIn("Deduplication", about_html)
            self.assertIn("relevance scoring", about_html.lower())
            self.assertIn("future publication dates", about_html)
            self.assertIn("Download CSV", (docs_dir / "index.html").read_text(encoding="utf-8"))
            self.assertNotIn("Download CSV", (docs_dir / "index.html").read_text(encoding="utf-8").split("</header>", 1)[0])
            self.assertIn("title,authors,publication_date,first_seen_date,relevance_decision,relevance_score,tags,sources,url,doi,arxiv_id", csv_text.splitlines()[0])
            self.assertIn("Latest Deep Research Memory", csv_text)
            self.assertIn("@misc", bib_text)
            self.assertIn("title = {Latest Deep Research Memory}", bib_text)


if __name__ == "__main__":
    unittest.main()
