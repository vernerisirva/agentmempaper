from __future__ import annotations

import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

from paper_scout.config import QualityConfig, QualityRankingConfig
from paper_scout.digest import write_digest
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.quality_models import QUALITY_DIMENSIONS, QualityAssessment, QualityEvidence
from paper_scout.site import build_site
from paper_scout.state import PaperStore


class PaperScoutQualitySiteTest(unittest.TestCase):
    def test_quality_assessment_is_rendered_in_html_json_csv_and_detail_page(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            state_path = root / "data" / "state.sqlite3"
            digest_dir = root / "digests"
            docs_dir = root / "docs"
            reports_dir = root / "reports"
            curation_path = root / "curation.yaml"
            digest_dir.mkdir()
            curation_path.write_text("pinned:\noverrides:\nexcluded:\ndate_overrides:\n", encoding="utf-8")
            write_digest(digest_dir / "2026-08-03.md", "2026-08-03", [])

            candidate = PaperCandidate(
                "A Carefully Evaluated Agent Memory System",
                ["Ada Researcher", "Grace Scholar"],
                "We evaluate persistent memory for LLM agents against baselines with accuracy 83.4%.",
                "fixture",
                "fixture-1",
                url="https://example.test/paper",
                published_date="2026-08-01",
                publication_year="2026",
                publication_date_precision="day",
                publication_date_source="fixture",
            )
            store = PaperStore(state_path)
            canonical_id = store.upsert_paper(candidate, ClassificationResult(94, "relevant", "Directly studies persistent memory for LLM agents.", ["agent-memory"]))
            assessment = QualityAssessment(
                canonical_id=canonical_id,
                overall_quality_score=42,
                confidence="high",
                recommendation="weak",
                paper_type="systems_or_application",
                assessment_scope="full_text",
                assessment_version="quality-v1",
                rubric_version="scholarly-rubric-v1",
                assessor_type="deterministic",
                source_content_hash="fixture-content-hash",
                assessed_at="2026-08-03T08:00:00+00:00",
                dimension_scores={dimension: 2 for dimension in QUALITY_DIMENSIONS},
                positive_signals=["The contribution is stated explicitly."],
                concerns=["The available results demonstrate functionality rather than comparative effectiveness."],
                evidence=[
                    QualityEvidence(
                        "evaluation_or_validation_strength",
                        "concern",
                        "Only functionality evidence was found.",
                        "The results section lacks comparative evidence.",
                        section="Results",
                        page=6,
                    )
                ],
                missing_information=["No ablation was detected."],
                concise_summary="The topic is relevant, but the available scholarly validation is weak.",
                applied_score_cap=44,
                applied_score_cap_reason="Only functionality evidence was detected.",
            )
            store.save_quality_assessment(assessment)
            quality = QualityConfig(enabled=True, ranking=QualityRankingConfig(behavior="downrank", downrank_below=60))

            result = build_site(
                digest_dir=digest_dir,
                report_dir=reports_dir,
                docs_dir=docs_dir,
                state_path=state_path,
                curation_path=curation_path,
                build_time="2026-08-03 12:00:00",
                quality_config=quality,
            )
            self.assertTrue(result.built)
            index_html = (docs_dir / "index.html").read_text(encoding="utf-8")
            about_html = (docs_dir / "about.html").read_text(encoding="utf-8")
            papers = json.loads((docs_dir / "data" / "papers.json").read_text(encoding="utf-8"))
            paper = papers[0]
            detail_html = (docs_dir / paper["detail_page"]).read_text(encoding="utf-8")
            detail_json = json.loads((docs_dir / paper["detail_json"]).read_text(encoding="utf-8"))
            csv_rows = list(csv.DictReader(io.StringIO((docs_dir / "data" / "papers.csv").read_text(encoding="utf-8"))))

            self.assertIn("Automated evidence-based assessment", index_html)
            self.assertIn("42/100", index_html)
            self.assertIn("Scholarly quality filters", index_html)
            self.assertIn('value="quality-desc"', index_html)
            self.assertIn('value="combined-desc"', index_html)
            self.assertIn('data-quality-downranked="true"', index_html)
            self.assertIn("Scholarly-quality assessment", about_html)
            self.assertIn("Automated evidence-based assessment", detail_html)
            self.assertIn("Only functionality evidence was found.", detail_html)
            self.assertIn("Assessment version", detail_html)
            self.assertEqual(paper["scholarly_quality"]["overall_quality_score"], 42)
            self.assertEqual(paper["scholarly_quality"]["recommendation"], "weak")
            self.assertTrue(paper["scholarly_quality"]["downranked"])
            self.assertEqual(detail_json["publication"]["source"], "fixture")
            self.assertEqual(csv_rows[0]["quality_score"], "42")
            self.assertEqual(csv_rows[0]["quality_assessment_scope"], "full_text")

            generated = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in docs_dir.rglob("*") if path.is_file())
            self.assertNotIn("PAPER_SCOUT_LLM_API_KEY", generated)
            self.assertNotRegex(generated, r"sk-[A-Za-z0-9]{20,}")

    def test_unassessed_quality_is_explicitly_unknown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            digest_dir = root / "digests"
            digest_dir.mkdir()
            write_digest(digest_dir / "2026-08-03.md", "2026-08-03", [])
            store = PaperStore(root / "state.sqlite3")
            store.upsert_paper(
                PaperCandidate("Relevant but Unassessed", [], "Persistent memory for LLM agents.", "fixture", "2"),
                ClassificationResult(90, "relevant", "Core topic."),
            )
            result = build_site(
                digest_dir=digest_dir,
                report_dir=root / "reports",
                docs_dir=root / "docs",
                state_path=root / "state.sqlite3",
                curation_path=root / "missing.yaml",
                quality_config=QualityConfig(enabled=True),
                build_time="2026-08-03 12:00:00",
            )
            self.assertTrue(result.built)
            html = (root / "docs" / "index.html").read_text(encoding="utf-8")
            payload = json.loads((root / "docs" / "data" / "papers.json").read_text(encoding="utf-8"))[0]
            self.assertNotIn("Automated evidence-based assessment", html)
            self.assertIsNone(payload["scholarly_quality"]["overall_quality_score"])
            self.assertEqual(payload["scholarly_quality"]["recommendation"], "unknown")


if __name__ == "__main__":
    unittest.main()
