from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
import hashlib
import json
import logging
from pathlib import Path

from paper_scout.config import QualityConfig
from paper_scout.curation import QualityCuration, quality_curation_for_paper
from paper_scout.full_text import FullTextDocument, fetch_and_extract_pdf, locate_full_text_urls, select_assessment_text
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.quality import assess_quality_deterministically, should_suppress_quality
from paper_scout.quality_llm import assess_with_optional_quality_llm
from paper_scout.llm import openai_compatible_settings_from_env
from paper_scout.quality_models import QualityAssessment, recommendation_for_score
from paper_scout.state import PaperStore


LOGGER = logging.getLogger(__name__)


@dataclass
class QualityRunStats:
    assessed: list[QualityAssessment] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    extraction_failures: list[str] = field(default_factory=list)
    cache_hits: int = 0
    cache_misses: int = 0
    suppressed: list[str] = field(default_factory=list)
    downranked: list[str] = field(default_factory=list)

    def record(self, assessment: QualityAssessment, cache_hit: bool) -> None:
        self.assessed.append(assessment)
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1


def assess_and_store_candidate(
    config: QualityConfig,
    store: PaperStore,
    candidate: PaperCandidate,
    canonical_id: str,
    classification: ClassificationResult,
    stats: QualityRunStats | None = None,
    force: bool = False,
    no_full_text: bool = False,
    no_llm: bool = False,
    direct_pdf_url: str | None = None,
    curation_path: Path | None = None,
) -> QualityAssessment | None:
    if not config.enabled or config.mode == "off" or not _should_assess(config, classification.decision):
        return None
    document: FullTextDocument | None = None
    extraction_errors: list[str] = []
    if config.full_text.enabled and not no_full_text:
        for url in locate_full_text_urls(candidate, direct_pdf_url or _direct_pdf_url(candidate)):
            try:
                document = fetch_and_extract_pdf(url, config.full_text, refresh=force)
                break
            except Exception as exc:  # noqa: BLE001 - full-text enrichment is optional.
                extraction_errors.append(f"{candidate.title}: {exc}")
                LOGGER.info("Full-text enrichment unavailable for %s via %s: %s", candidate.title, url, exc)
    selected = select_assessment_text(
        candidate,
        document,
        max_prompt_characters=config.full_text.max_prompt_characters,
        max_section_characters=config.full_text.max_section_characters,
    )
    matching = store.get_current_quality_assessment(
        canonical_id,
        assessment_version=config.assessment.version,
        rubric_version=config.assessment.rubric_version,
        source_content_hash=selected.content_hash,
    )
    if matching and not force and quality_assessment_matches_mode(config, matching, no_llm=no_llm):
        if stats:
            stats.extraction_failures.extend(extraction_errors)
        return _finalize_assessment(config, store, candidate, matching, curation_path, stats, cache_hit=True)

    deterministic = assess_quality_deterministically(
        candidate,
        canonical_id,
        selected,
        assessment_version=config.assessment.version,
        rubric_version=config.assessment.rubric_version,
    )
    mode = "deterministic" if no_llm else config.mode
    assessment = assess_with_optional_quality_llm(candidate, selected, deterministic, mode)
    if stats:
        stats.extraction_failures.extend(extraction_errors)
    return _finalize_assessment(
        config,
        store,
        candidate,
        assessment,
        curation_path,
        stats,
        cache_hit=bool(document and document.cache_hit),
    )


def _finalize_assessment(
    config: QualityConfig,
    store: PaperStore,
    candidate: PaperCandidate,
    assessment: QualityAssessment,
    curation_path: Path | None,
    stats: QualityRunStats | None,
    cache_hit: bool,
) -> QualityAssessment:
    curation = quality_curation_for_paper(curation_path, assessment.canonical_id, candidate.title)
    final = _apply_manual_curation(assessment, curation)
    assessment_id = store.save_quality_assessment(assessment)
    if final != assessment:
        assessment_id = store.save_quality_assessment(final)
    suppressed = should_suppress_quality(
        final,
        config.ranking.behavior,
        config.ranking.hide_below,
        config.ranking.minimum_confidence_for_hiding,
        pinned=curation.pinned,
        include_despite_quality=curation.include_despite_quality,
        suppress_for_quality=curation.suppress_for_quality,
    )
    if suppressed:
        reason = final.applied_score_cap_reason or final.concise_summary
        store.set_quality_suppression(final.canonical_id, assessment_id, reason)
        if stats:
            stats.suppressed.append(final.canonical_id)
    else:
        store.clear_quality_suppression(final.canonical_id)
    if (
        config.ranking.behavior == "downrank"
        and final.overall_quality_score is not None
        and final.overall_quality_score < config.ranking.downrank_below
        and final.confidence in {"medium", "high"}
        and final.assessment_scope in {"partial_full_text", "full_text"}
        and not curation.pinned
        and not curation.include_despite_quality
    ):
        if stats:
            stats.downranked.append(final.canonical_id)
    if stats:
        stats.record(final, cache_hit=cache_hit)
    return final


def _apply_manual_curation(assessment: QualityAssessment, curation: QualityCuration) -> QualityAssessment:
    if not curation.has_manual_assessment:
        return assessment
    score = curation.quality_score_override if curation.quality_score_override is not None else assessment.overall_quality_score
    if score is None:
        recommendation = "unknown"
    else:
        recommendation = curation.quality_recommendation_override or recommendation_for_score(score, "high")
        if recommendation == "unknown":
            recommendation = recommendation_for_score(score, "high")
    if (
        assessment.assessor_type == "manual_override"
        and assessment.assessor_model == "curation"
        and assessment.overall_quality_score == score
        and assessment.recommendation == recommendation
        and (not curation.quality_note or assessment.concise_summary == curation.quality_note)
    ):
        return assessment
    override_payload = json.dumps(
        {
            "score": score,
            "recommendation": recommendation,
            "note": curation.quality_note,
        },
        sort_keys=True,
    )
    source_hash = hashlib.sha256(f"{assessment.source_content_hash}\n{override_payload}".encode("utf-8")).hexdigest()
    summary = curation.quality_note or assessment.concise_summary
    return replace(
        assessment,
        overall_quality_score=score,
        recommendation=recommendation,
        confidence="high",
        assessor_type="manual_override",
        assessor_model="curation",
        source_content_hash=source_hash,
        assessed_at=datetime.now(UTC).replace(microsecond=0).isoformat(),
        concise_summary=summary,
    )


def _should_assess(config: QualityConfig, decision: str) -> bool:
    return {
        "relevant": config.assessment.assess_relevant,
        "maybe": config.assessment.assess_maybe_relevant,
        "irrelevant": config.assessment.assess_irrelevant,
    }.get(decision, False)


def quality_assessment_matches_mode(
    config: QualityConfig,
    assessment: QualityAssessment,
    no_llm: bool = False,
) -> bool:
    if assessment.assessor_type == "manual_override":
        return True
    mode = "deterministic" if no_llm else config.mode
    settings = None if mode in {"off", "deterministic"} else openai_compatible_settings_from_env("PAPER_SCOUT_QUALITY_LLM_MODEL")
    if settings is None:
        return assessment.assessor_type == "deterministic"
    expected_type = "llm" if mode == "llm" else "hybrid"
    return assessment.assessor_type == expected_type and assessment.assessor_model == settings.model


def reconcile_quality_curation(
    config: QualityConfig,
    store: PaperStore,
    candidate: PaperCandidate,
    assessment: QualityAssessment,
    curation_path: Path | None,
) -> QualityAssessment:
    curation = quality_curation_for_paper(curation_path, assessment.canonical_id, candidate.title)
    if not curation.has_quality_directive:
        return assessment
    return _finalize_assessment(config, store, candidate, assessment, curation_path, None, cache_hit=True)


def _direct_pdf_url(candidate: PaperCandidate) -> str | None:
    value = candidate.raw.get("direct_pdf_url") if isinstance(candidate.raw, dict) else None
    return str(value) if value else None
