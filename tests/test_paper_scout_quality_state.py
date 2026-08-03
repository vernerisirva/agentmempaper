from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.config import QualityConfig, QualityFullTextConfig, QualityRankingConfig
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.quality_models import QualityAssessment
from paper_scout.quality_service import QualityRunStats, assess_and_store_candidate, quality_assessment_matches_mode
from paper_scout.state import PaperStore


def _candidate() -> PaperCandidate:
    return PaperCandidate(
        "Evaluating Persistent Memory for LLM Agents",
        ["Ada Researcher"],
        "We propose and evaluate persistent agent memory against a baseline using accuracy 81.2%.",
        "fixture",
        "fixture-1",
    )


def _assessment(version: str = "quality-v1", content_hash: str = "hash-1") -> QualityAssessment:
    return QualityAssessment(
        canonical_id="fixture:fixture-1",
        overall_quality_score=72,
        confidence="high",
        recommendation="promising",
        paper_type="empirical_research",
        assessment_scope="full_text",
        assessment_version=version,
        rubric_version="scholarly-rubric-v1",
        assessor_type="deterministic",
        source_content_hash=content_hash,
        assessed_at="2026-08-03T10:00:00+00:00",
        concise_summary="Supported fixture assessment.",
    )


class PaperScoutQualityStateTest(unittest.TestCase):
    def test_additive_schema_persists_versioned_assessments_and_cache_key(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "state.sqlite3"
            store = PaperStore(path)
            first_id = store.save_quality_assessment(_assessment())
            duplicate_id = store.save_quality_assessment(_assessment())
            changed_id = store.save_quality_assessment(_assessment(content_hash="hash-2"))
            new_version_id = store.save_quality_assessment(_assessment(version="quality-v2", content_hash="hash-2"))
            self.assertEqual(first_id, duplicate_id)
            self.assertNotEqual(first_id, changed_id)
            self.assertNotEqual(changed_id, new_version_id)
            self.assertEqual(store.get_current_quality_assessment("fixture:fixture-1", source_content_hash="hash-1").overall_quality_score, 72)
            with sqlite3.connect(path) as db:
                tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertIn("paper_quality_assessments", tables)
            self.assertIn("quality_suppressions", tables)

    def test_model_change_invalidates_quality_cache(self):
        config = QualityConfig(enabled=True, mode="hybrid")
        hybrid = replace(_assessment(), assessor_type="hybrid", assessor_model="model-a")
        env = {
            "PAPER_SCOUT_LLM_PROVIDER": "auto",
            "PAPER_SCOUT_LLM_API_KEY": "test-only-key",
            "PAPER_SCOUT_LLM_MODEL": "model-b",
        }
        with patch.dict("os.environ", env, clear=True):
            self.assertFalse(quality_assessment_matches_mode(config, hybrid))
            self.assertTrue(quality_assessment_matches_mode(config, replace(hybrid, assessor_model="model-b")))

    def test_quality_failure_or_missing_full_text_does_not_break_paper_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PaperStore(Path(tmpdir) / "state.sqlite3")
            candidate = _candidate()
            classification = ClassificationResult(90, "relevant", "Core memory study.")
            key = store.upsert_paper(candidate, classification)
            config = QualityConfig(enabled=True, mode="deterministic", full_text=QualityFullTextConfig(enabled=False))
            stats = QualityRunStats()
            result = assess_and_store_candidate(config, store, candidate, key, classification, stats=stats)
            self.assertIsNotNone(result)
            self.assertEqual(result.assessment_scope, "title_and_abstract")
            self.assertEqual(store.paper_count(), 1)

    def test_pdf_fetch_failure_falls_back_to_abstract_and_is_reported(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = PaperStore(Path(tmpdir) / "state.sqlite3")
            candidate = replace(_candidate(), arxiv_id="2608.00001")
            classification = ClassificationResult(90, "relevant", "Core memory study.")
            key = store.upsert_paper(candidate, classification)
            config = QualityConfig(enabled=True, mode="deterministic", full_text=QualityFullTextConfig(enabled=True))
            stats = QualityRunStats()
            with patch("paper_scout.quality_service.fetch_and_extract_pdf", side_effect=RuntimeError("TLS unavailable")):
                result = assess_and_store_candidate(config, store, candidate, key, classification, stats=stats)
            self.assertEqual(result.assessment_scope, "title_and_abstract")
            self.assertEqual(result.confidence, "low")
            self.assertTrue(any("TLS unavailable" in item for item in stats.extraction_failures))

    def test_manual_curation_override_and_pinned_precedence_are_auditable(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            store = PaperStore(root / "state.sqlite3")
            candidate = _candidate()
            classification = ClassificationResult(90, "relevant", "Core memory study.")
            key = store.upsert_paper(candidate, classification)
            curation = root / "curation.yaml"
            curation.write_text(
                f'''pinned:\n  - canonical_id: "{key}"\n    quality_score_override: 36\n    quality_recommendation_override: weak\n    quality_note: "Manual full-paper review found weak validation."\n    suppress_for_quality: true\noverrides:\nexcluded:\n''',
                encoding="utf-8",
            )
            config = QualityConfig(
                enabled=True,
                mode="deterministic",
                full_text=QualityFullTextConfig(enabled=False),
                ranking=QualityRankingConfig(behavior="hide", hide_below=40, minimum_confidence_for_hiding="high"),
            )
            result = assess_and_store_candidate(config, store, candidate, key, classification, curation_path=curation)
            self.assertEqual(result.overall_quality_score, 36)
            self.assertEqual(result.assessor_type, "manual_override")
            self.assertEqual(result.assessor_model, "curation")
            self.assertEqual(result.concise_summary, "Manual full-paper review found weak validation.")
            self.assertEqual(store.get_unnotified_digest_papers(exclude_quality_suppressed=True)[0].canonical_key, key)
            assess_and_store_candidate(config, store, candidate, key, classification, curation_path=curation)
            with sqlite3.connect(root / "state.sqlite3") as db:
                count = db.execute("SELECT COUNT(*) FROM paper_quality_assessments WHERE canonical_id = ?", (key,)).fetchone()[0]
            self.assertEqual(count, 2)

    def test_explicit_quality_suppression_hides_unpinned_paper(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            store = PaperStore(root / "state.sqlite3")
            candidate = _candidate()
            classification = ClassificationResult(90, "relevant", "Core memory study.")
            key = store.upsert_paper(candidate, classification)
            curation = root / "curation.yaml"
            curation.write_text(
                f'''pinned:\noverrides:\n  - canonical_id: "{key}"\n    suppress_for_quality: true\n    quality_note: "Human review suppression."\nexcluded:\n''',
                encoding="utf-8",
            )
            config = QualityConfig(enabled=True, mode="deterministic", full_text=QualityFullTextConfig(enabled=False))
            assess_and_store_candidate(config, store, candidate, key, classification, curation_path=curation)
            self.assertEqual(store.get_unnotified_digest_papers(exclude_quality_suppressed=True), [])


if __name__ == "__main__":
    unittest.main()
