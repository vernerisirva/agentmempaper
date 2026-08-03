from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.config import QualityFullTextConfig
from paper_scout.digest import render_digest
from paper_scout.full_text import (
    ExtractedPage,
    FullTextDocument,
    SelectedPaperText,
    SelectedSection,
    fetch_and_extract_pdf,
    locate_full_text_urls,
    select_assessment_text,
)
from paper_scout.models import DigestPaper, PaperCandidate
from paper_scout.quality import (
    assess_quality_deterministically,
    classify_paper_type,
    combined_rank_score,
    should_suppress_quality,
)
from paper_scout.quality_evaluation import evaluate_quality_fixtures
from paper_scout.quality_llm import assess_with_optional_quality_llm
from paper_scout.quality_llm import validate_llm_quality_response
from paper_scout.quality_models import QUALITY_DIMENSIONS, QualityAssessment, QualityEvidence


class FailingQualityHttp:
    def post_json(self, url, payload, headers=None):
        return "not-json"


def _candidate(title: str = "Agent Memory Study", abstract: str = "We evaluate persistent memory for LLM agents.") -> PaperCandidate:
    return PaperCandidate(title, ["Ada Researcher"], abstract, "fixture", "fixture-1")


def _assessment(score: int | None = 72, confidence: str = "high", scope: str = "full_text") -> QualityAssessment:
    recommendation = "promising" if score is not None else "unknown"
    return QualityAssessment(
        canonical_id="fixture:1",
        overall_quality_score=score,
        confidence=confidence,
        recommendation=recommendation,
        paper_type="empirical_research",
        assessment_scope=scope,
        assessment_version="quality-v1",
        rubric_version="scholarly-rubric-v1",
        assessor_type="deterministic",
        source_content_hash="content-1",
        assessed_at="2026-08-03T10:00:00+00:00",
        dimension_scores={dimension: 3 for dimension in QUALITY_DIMENSIONS},
        evidence=[QualityEvidence("methodological_rigor", "positive", "A method is described.", "Fixture evidence.")],
        concise_summary="A fixture quality assessment.",
    )


class PaperScoutQualityTest(unittest.TestCase):
    def test_quality_model_round_trip_and_validation(self):
        assessment = _assessment()
        self.assertEqual(QualityAssessment.from_dict(assessment.to_dict()), assessment)
        with self.assertRaises(ValueError):
            replace(assessment, overall_quality_score=101)
        with self.assertRaises(ValueError):
            replace(assessment, confidence="certain")

    def test_deterministic_fixture_suite_covers_paper_types_and_weak_integration(self):
        report = evaluate_quality_fixtures()
        self.assertTrue(report["passed"], report["failures"])
        weak = next(row for row in report["fixtures"] if row["name"] == "weak integration-only prototype")
        self.assertLessEqual(weak["actual_score"], 45)
        self.assertEqual(weak["actual_recommendation"], "weak")
        self.assertIn("established components", " ".join(weak["actual_concerns"]))

    def test_paper_type_uses_primary_contribution_not_incidental_benchmark_mention(self):
        self.assertEqual(
            classify_paper_type(
                "A Deployed Shared-Memory System",
                "We introduce a deployed system architecture and compare it on a benchmark.",
            ),
            "systems_or_application",
        )
        self.assertEqual(classify_paper_type("MemBench: An Agent Memory Benchmark", "We release a benchmark."), "dataset_or_benchmark")

    def test_abstract_only_assessment_is_low_confidence_and_never_strong(self):
        candidate = _candidate()
        selected = select_assessment_text(candidate, None)
        assessment = assess_quality_deterministically(candidate, "fixture:abstract", selected)
        self.assertEqual(assessment.assessment_scope, "title_and_abstract")
        self.assertEqual(assessment.confidence, "low")
        self.assertEqual(assessment.recommendation, "uncertain")
        self.assertFalse(should_suppress_quality(assessment, "hide", 90, "low"))

    def test_missing_content_produces_unknown_not_zero(self):
        candidate = _candidate(abstract="")
        assessment = assess_quality_deterministically(candidate, "fixture:missing", select_assessment_text(candidate, None))
        self.assertIsNone(assessment.overall_quality_score)
        self.assertEqual(assessment.recommendation, "unknown")

    def test_publication_date_and_venue_do_not_change_quality_score(self):
        text = "We propose a method and compare against a baseline with accuracy 81.2%. Limitations are discussed."
        selected = SelectedPaperText(text, [SelectedSection("Evaluation", text, 2)], "full_text", "same-content", False)
        past = replace(_candidate(abstract=text), published_date="2024-01-01", raw={"venue": "Prestigious Venue"})
        future = replace(_candidate(abstract=text), published_date="2030-01-01", raw={"venue": "Unknown Venue"})
        past_result = assess_quality_deterministically(past, "fixture:past", selected)
        future_result = assess_quality_deterministically(future, "fixture:future", selected)
        self.assertEqual(past_result.overall_quality_score, future_result.overall_quality_score)

    def test_combined_ranking_keeps_unknown_neutral_and_scales_by_confidence(self):
        self.assertEqual(combined_rank_score(80, None), 0.8)
        high = combined_rank_score(80, _assessment(score=40, confidence="high"))
        low = combined_rank_score(80, _assessment(score=40, confidence="low"))
        self.assertLess(high, low)
        self.assertLess(low, 0.8)

    def test_hide_requires_supported_assessment_and_respects_manual_precedence(self):
        weak = _assessment(score=30, confidence="high", scope="full_text")
        self.assertTrue(should_suppress_quality(weak, "hide", 40, "high"))
        self.assertFalse(should_suppress_quality(weak, "hide", 40, "high", pinned=True))
        self.assertFalse(should_suppress_quality(weak, "hide", 40, "high", include_despite_quality=True))
        self.assertTrue(should_suppress_quality(weak, "annotate", 40, "high", suppress_for_quality=True))

    def test_full_text_locator_prefers_supplied_then_open_access_sources(self):
        candidate = PaperCandidate(
            "Paper",
            [],
            "Abstract",
            "semantic_scholar",
            "S2",
            arxiv_id="2601.12345",
            raw={
                "openAccessPdf": {"url": "https://example.test/s2.pdf"},
                "best_oa_location": {"pdf_url": "https://example.test/openalex.pdf"},
            },
        )
        urls = locate_full_text_urls(candidate, "https://example.test/supplied.pdf")
        self.assertEqual(urls[0], "https://example.test/supplied.pdf")
        self.assertIn("https://arxiv.org/pdf/2601.12345.pdf", urls)
        self.assertIn("https://example.test/s2.pdf", urls)
        self.assertIn("https://example.test/openalex.pdf", urls)
        rejected = locate_full_text_urls(candidate, "http://127.0.0.1/private.pdf")
        self.assertNotIn("http://127.0.0.1/private.pdf", rejected)

    def test_section_selection_is_bounded_and_preserves_page_provenance(self):
        candidate = _candidate()
        document = FullTextDocument(
            "https://example.test/paper.pdf",
            [
                ExtractedPage(1, "Abstract\nSummary text.\nIntroduction\nBackground."),
                ExtractedPage(2, "Methodology\nMethod details.\nEvaluation\nAccuracy 80%."),
                ExtractedPage(3, "Limitations\nOne dataset only.\nConclusion\nClosing."),
            ],
            "pdf-hash",
            True,
        )
        selected = select_assessment_text(candidate, document, max_prompt_characters=1_000, max_section_characters=100)
        self.assertLessEqual(len(selected.text), 1_000)
        self.assertTrue(any(section.first_page == 2 for section in selected.sections))
        self.assertIn(selected.scope, {"partial_full_text", "full_text"})

    def test_pdf_extraction_failure_is_clean_and_does_not_cache_invalid_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            settings = QualityFullTextConfig(cache_dir=Path(tmpdir))
            with patch("paper_scout.full_text._download_pdf", return_value=(b"not a pdf", "text/html")):
                with self.assertRaisesRegex(ValueError, "plausible PDF"):
                    fetch_and_extract_pdf("https://example.test/not-pdf", settings)
            self.assertEqual(list(Path(tmpdir).glob("*.json")), [])

    def test_malformed_llm_output_falls_back_to_deterministic(self):
        candidate = _candidate()
        selected = SelectedPaperText(
            candidate.abstract,
            [SelectedSection("Abstract", candidate.abstract, None)],
            "title_and_abstract",
            "abstract-hash",
            False,
        )
        deterministic = assess_quality_deterministically(candidate, "fixture:llm", selected)
        env = {
            "PAPER_SCOUT_LLM_PROVIDER": "auto",
            "PAPER_SCOUT_LLM_API_KEY": "test-only-key",
            "PAPER_SCOUT_LLM_MODEL": "test-model",
        }
        with patch.dict("os.environ", env, clear=True):
            result = assess_with_optional_quality_llm(candidate, selected, deterministic, "hybrid", http=FailingQualityHttp())
        self.assertEqual(result, deterministic)

    def test_well_formed_llm_output_is_validated_and_keeps_deterministic_cap(self):
        deterministic = replace(
            _assessment(score=44),
            applied_score_cap=44,
            applied_score_cap_reason="Functionality-only evidence.",
        )
        result = validate_llm_quality_response(
            {
                "overall_quality_score": 88,
                "confidence": "high",
                "paper_type": "systems_or_application",
                "dimension_scores": {dimension: 4 for dimension in QUALITY_DIMENSIONS},
                "positive_signals": ["A baseline is reported."],
                "concerns": [],
                "evidence": [],
                "missing_information": [],
                "concise_summary": "Model-validated assessment.",
            },
            deterministic,
            "test-model",
        )
        self.assertEqual(result.overall_quality_score, 44)
        self.assertEqual(result.assessor_type, "hybrid")
        self.assertEqual(result.assessor_model, "test-model")
        self.assertEqual(result.applied_score_cap, 44)

    def test_extracted_text_cache_avoids_repeated_pdf_work(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            settings = QualityFullTextConfig(cache_dir=Path(tmpdir))
            document = FullTextDocument(
                "https://example.test/paper.pdf",
                [ExtractedPage(1, "Abstract\nCached text")],
                "payload-hash",
                True,
            )
            with patch("paper_scout.full_text._download_pdf", return_value=(b"%PDF-fixture", "application/pdf")) as download:
                with patch("paper_scout.full_text._extract_pdf", return_value=document) as extract:
                    first = fetch_and_extract_pdf("https://example.test/paper.pdf", settings)
                    second = fetch_and_extract_pdf("https://example.test/paper.pdf", settings)
            self.assertFalse(first.cache_hit)
            self.assertTrue(second.cache_hit)
            self.assertEqual(download.call_count, 1)
            self.assertEqual(extract.call_count, 1)

            with patch("paper_scout.full_text._download_pdf", return_value=(b"%PDF-updated", "application/pdf")) as refresh_download:
                with patch("paper_scout.full_text._extract_pdf", return_value=document):
                    refreshed = fetch_and_extract_pdf("https://example.test/paper.pdf", settings, refresh=True)
            self.assertFalse(refreshed.cache_hit)
            self.assertEqual(refresh_download.call_count, 1)

    def test_digest_keeps_relevance_and_quality_as_separate_lines(self):
        paper = DigestPaper(
            canonical_key="fixture:1",
            title="Relevant but Weakly Evaluated",
            authors=["Ada Researcher"],
            abstract="Abstract",
            source="fixture",
            url="https://example.test/paper",
            published_date="2026-08-01",
            score=95,
            decision="relevant",
            reason="Directly studies agent memory.",
            tags=["agent-memory"],
            abstract_summary="Summary.",
            quality_score=31,
            quality_recommendation="weak",
            quality_confidence="high",
            quality_scope="full_text",
            quality_summary="Weak validation.",
            quality_concerns=["Only functionality evidence was found."],
            quality_strengths=["The contribution is explicit."],
        )
        digest = render_digest("2026-08-03", [paper])
        self.assertIn("Relevance:** relevant (95/100)", digest)
        self.assertIn("Automated evidence-based assessment:** 31/100", digest)
        self.assertIn("Only functionality evidence was found.", digest)


if __name__ == "__main__":
    unittest.main()
