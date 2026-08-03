from __future__ import annotations

from datetime import UTC, datetime
import json
import logging

from paper_scout.full_text import SelectedPaperText
from paper_scout.http import HttpClient
from paper_scout.llm import openai_compatible_settings_from_env
from paper_scout.models import PaperCandidate
from paper_scout.quality_models import QualityAssessment, QualityEvidence, recommendation_for_score


LOGGER = logging.getLogger(__name__)


def assess_with_optional_quality_llm(
    candidate: PaperCandidate,
    selected: SelectedPaperText,
    deterministic: QualityAssessment,
    mode: str,
    http: HttpClient | None = None,
) -> QualityAssessment:
    if mode in {"off", "deterministic"}:
        return deterministic
    settings = openai_compatible_settings_from_env("PAPER_SCOUT_QUALITY_LLM_MODEL")
    if settings is None:
        return deterministic
    try:
        payload = _request_payload(candidate, selected, deterministic, settings.model)
        headers = {"Authorization": f"Bearer {settings.api_key}"}
        response = (http or HttpClient()).post_json(f"{settings.base_url}/chat/completions", payload, headers=headers)
        content = json.loads(response)["choices"][0]["message"]["content"]
        parsed = json.loads(_strip_json_fence(content))
        return validate_llm_quality_response(parsed, deterministic, settings.model, mode)
    except Exception as exc:  # noqa: BLE001 - malformed or unavailable LLM output must not fail a run.
        LOGGER.warning("Quality LLM assessment failed for %s: %s", candidate.title, exc)
        return deterministic


def validate_llm_quality_response(
    value: dict[str, object],
    deterministic: QualityAssessment,
    model: str,
    mode: str = "hybrid",
) -> QualityAssessment:
    score = int(value["overall_quality_score"]) if value.get("overall_quality_score") is not None else None
    confidence = str(value.get("confidence", deterministic.confidence))
    dimensions = value.get("dimension_scores") or deterministic.dimension_scores
    evidence_values = value.get("evidence") or []
    evidence = [QualityEvidence.from_dict(dict(item)) for item in evidence_values if isinstance(item, dict)]
    cap = deterministic.applied_score_cap
    cap_reason = deterministic.applied_score_cap_reason
    if cap is not None and score is not None:
        score = min(score, cap)
    recommendation = recommendation_for_score(score, confidence)
    llm_positive = [str(item) for item in value.get("positive_signals") or []]
    llm_concerns = [str(item) for item in value.get("concerns") or []]
    return QualityAssessment(
        canonical_id=deterministic.canonical_id,
        overall_quality_score=score,
        confidence=confidence,
        recommendation=recommendation,
        paper_type=str(value.get("paper_type", deterministic.paper_type)),
        assessment_scope=deterministic.assessment_scope,
        assessment_version=deterministic.assessment_version,
        rubric_version=deterministic.rubric_version,
        assessor_type="hybrid" if mode in {"hybrid", "auto"} else "llm",
        assessor_model=model,
        source_content_hash=deterministic.source_content_hash,
        assessed_at=datetime.now(UTC).replace(microsecond=0).isoformat(),
        dimension_scores={str(key): int(item) if item is not None else None for key, item in dict(dimensions).items()},
        positive_signals=_ordered_unique([*deterministic.positive_signals, *llm_positive]),
        concerns=_ordered_unique([*deterministic.concerns, *llm_concerns]),
        evidence=[*deterministic.evidence, *evidence],
        missing_information=_ordered_unique([*deterministic.missing_information, *[str(item) for item in value.get("missing_information") or []]]),
        concise_summary=str(value.get("concise_summary") or deterministic.concise_summary),
        applied_score_cap=cap,
        applied_score_cap_reason=cap_reason,
    )


def _request_payload(candidate: PaperCandidate, selected: SelectedPaperText, deterministic: QualityAssessment, model: str) -> dict[str, object]:
    prompt = {
        "paper": {"title": candidate.title, "authors": candidate.authors, "text": selected.text},
        "extraction": {
            "scope": selected.scope,
            "section_detection_uncertain": selected.section_detection_uncertain,
            "warnings": selected.warnings,
        },
        "deterministic_assessment": deterministic.to_dict(),
        "required_schema": {
            "overall_quality_score": "integer 0-100 or null",
            "confidence": "low|medium|high",
            "paper_type": "validated paper type",
            "dimension_scores": "object with 0-5 or null values",
            "positive_signals": "array of cautious strings",
            "concerns": "array of cautious strings",
            "missing_information": "array of strings",
            "evidence": "array of evidence objects",
            "concise_summary": "string",
        },
    }
    system = (
        "Assess scholarly quality only from the supplied paper text and extraction metadata. "
        "Do not use venue prestige, citation count, author identity, institution, or paper age. "
        "Classify paper type before applying type-appropriate expectations. Distinguish routine integration from a supported scholarly contribution. "
        "Do not require empirical experiments for surveys, theoretical, position, dataset, or replication papers. "
        "Every major judgment needs evidence; distinguish missing text from absent evidence. Do not invent sections or accuse authors of misconduct. "
        "Return only valid JSON matching the supplied schema."
    )
    return {
        "model": model,
        "temperature": 0,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(prompt)}],
    }


def _strip_json_fence(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:]
    return stripped.strip()


def _ordered_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))
