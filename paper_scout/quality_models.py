from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


PAPER_TYPES = {
    "empirical_research",
    "systems_or_application",
    "methods_or_algorithm",
    "theoretical",
    "survey_or_review",
    "position_or_conceptual",
    "dataset_or_benchmark",
    "case_study",
    "replication",
    "unclear",
}
ASSESSMENT_SCOPES = {"metadata_only", "title_and_abstract", "partial_full_text", "full_text"}
QUALITY_CONFIDENCES = {"low", "medium", "high"}
QUALITY_RECOMMENDATIONS = {"strong", "promising", "uncertain", "weak", "unknown"}
ASSESSOR_TYPES = {"deterministic", "llm", "hybrid", "manual_override"}
EVIDENCE_SIGNAL_TYPES = {"positive", "concern", "missing"}

QUALITY_DIMENSIONS = (
    "contribution_clarity",
    "scholarly_novelty_or_value",
    "methodological_rigor",
    "evaluation_or_validation_strength",
    "evidence_to_claim_alignment",
    "related_work_and_gap_positioning",
    "reproducibility_and_transparency",
    "limitations_and_uncertainty_handling",
    "presentation_and_precision",
)


@dataclass(frozen=True)
class QualityEvidence:
    dimension: str
    signal_type: str
    paraphrase: str
    explanation: str
    section: str | None = None
    page: int | None = None
    excerpt: str | None = None

    def __post_init__(self) -> None:
        if self.dimension not in QUALITY_DIMENSIONS:
            raise ValueError(f"unknown quality dimension: {self.dimension}")
        if self.signal_type not in EVIDENCE_SIGNAL_TYPES:
            raise ValueError(f"unknown evidence signal type: {self.signal_type}")
        if self.page is not None and self.page < 1:
            raise ValueError("evidence page must be positive")
        if not self.paraphrase.strip() or not self.explanation.strip():
            raise ValueError("quality evidence requires a paraphrase and explanation")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "QualityEvidence":
        return cls(
            dimension=str(value.get("dimension", "")),
            signal_type=str(value.get("signal_type", "")),
            paraphrase=str(value.get("paraphrase", "")),
            explanation=str(value.get("explanation", "")),
            section=_optional_text(value.get("section")),
            page=int(value["page"]) if value.get("page") is not None else None,
            excerpt=_optional_text(value.get("excerpt")),
        )


@dataclass(frozen=True)
class QualityAssessment:
    canonical_id: str
    overall_quality_score: int | None
    confidence: str
    recommendation: str
    paper_type: str
    assessment_scope: str
    assessment_version: str
    rubric_version: str
    assessor_type: str
    source_content_hash: str
    assessed_at: str
    dimension_scores: dict[str, int | None] = field(default_factory=dict)
    positive_signals: list[str] = field(default_factory=list)
    concerns: list[str] = field(default_factory=list)
    evidence: list[QualityEvidence] = field(default_factory=list)
    missing_information: list[str] = field(default_factory=list)
    concise_summary: str = ""
    assessor_model: str | None = None
    applied_score_cap: int | None = None
    applied_score_cap_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.canonical_id.strip():
            raise ValueError("quality assessment requires a canonical identifier")
        if self.overall_quality_score is not None and not 0 <= self.overall_quality_score <= 100:
            raise ValueError("overall quality score must be between 0 and 100")
        if self.confidence not in QUALITY_CONFIDENCES:
            raise ValueError(f"unknown quality confidence: {self.confidence}")
        if self.recommendation not in QUALITY_RECOMMENDATIONS:
            raise ValueError(f"unknown quality recommendation: {self.recommendation}")
        if self.paper_type not in PAPER_TYPES:
            raise ValueError(f"unknown paper type: {self.paper_type}")
        if self.assessment_scope not in ASSESSMENT_SCOPES:
            raise ValueError(f"unknown assessment scope: {self.assessment_scope}")
        if self.assessor_type not in ASSESSOR_TYPES:
            raise ValueError(f"unknown assessor type: {self.assessor_type}")
        if self.overall_quality_score is None and self.recommendation != "unknown":
            raise ValueError("unknown quality scores require the unknown recommendation")
        if self.recommendation == "unknown" and self.overall_quality_score is not None:
            raise ValueError("the unknown recommendation requires a null score")
        if self.applied_score_cap is not None and not 0 <= self.applied_score_cap <= 100:
            raise ValueError("quality score cap must be between 0 and 100")
        if self.applied_score_cap is not None and not self.applied_score_cap_reason:
            raise ValueError("an applied score cap requires a reason")
        for dimension, score in self.dimension_scores.items():
            if dimension not in QUALITY_DIMENSIONS:
                raise ValueError(f"unknown quality dimension: {dimension}")
            if score is not None and not 0 <= score <= 5:
                raise ValueError(f"dimension score for {dimension} must be between 0 and 5")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "QualityAssessment":
        score = value.get("overall_quality_score")
        cap = value.get("applied_score_cap")
        dimensions = value.get("dimension_scores") or {}
        evidence = value.get("evidence") or []
        return cls(
            canonical_id=str(value.get("canonical_id", "")),
            overall_quality_score=int(score) if score is not None else None,
            confidence=str(value.get("confidence", "low")),
            recommendation=str(value.get("recommendation", "unknown")),
            paper_type=str(value.get("paper_type", "unclear")),
            assessment_scope=str(value.get("assessment_scope", "metadata_only")),
            assessment_version=str(value.get("assessment_version", "")),
            rubric_version=str(value.get("rubric_version", "")),
            assessor_type=str(value.get("assessor_type", "deterministic")),
            assessor_model=_optional_text(value.get("assessor_model")),
            source_content_hash=str(value.get("source_content_hash", "")),
            assessed_at=str(value.get("assessed_at", "")),
            dimension_scores={str(key): int(item) if item is not None else None for key, item in dict(dimensions).items()},
            positive_signals=[str(item) for item in value.get("positive_signals") or []],
            concerns=[str(item) for item in value.get("concerns") or []],
            evidence=[QualityEvidence.from_dict(dict(item)) for item in evidence],
            missing_information=[str(item) for item in value.get("missing_information") or []],
            concise_summary=str(value.get("concise_summary", "")),
            applied_score_cap=int(cap) if cap is not None else None,
            applied_score_cap_reason=_optional_text(value.get("applied_score_cap_reason")),
        )


def recommendation_for_score(score: int | None, confidence: str) -> str:
    if score is None:
        return "unknown"
    if confidence == "low":
        return "uncertain"
    if score >= 85:
        return "strong"
    if score >= 70:
        return "promising"
    if score >= 55:
        return "uncertain"
    return "weak"


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
