from __future__ import annotations

from collections import Counter
from pathlib import Path

from paper_scout.quality_models import QualityAssessment
from paper_scout.quality_service import QualityRunStats


def write_paper_quality_report(
    report_dir: Path,
    report_date: str,
    stats: QualityRunStats,
    assessment_version: str,
    rubric_version: str,
) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"paper-quality-{report_date}.md"
    assessments = stats.assessed
    scope_counts = Counter(item.assessment_scope for item in assessments)
    confidence_counts = Counter(item.confidence for item in assessments)
    recommendation_counts = Counter(item.recommendation for item in assessments)
    assessor_counts = Counter(item.assessor_type for item in assessments)
    score_distribution = Counter(_score_band(item.overall_quality_score) for item in assessments)
    capped = [item for item in assessments if item.applied_score_cap is not None]
    unknown = [item for item in assessments if item.recommendation == "unknown"]
    lines = [
        f"# Paper Scout scholarly-quality report - {report_date}",
        "",
        "> Advisory automated assessment. Relevance and scholarly quality are independent, and human review remains necessary.",
        "",
        "## Summary",
        "",
        f"- Papers assessed or reused: {len(assessments)}",
        f"- Assessment scopes: {_counts(scope_counts)}",
        f"- Confidence: {_counts(confidence_counts)}",
        f"- Recommendations: {_counts(recommendation_counts)}",
        f"- Score distribution: {_counts(score_distribution)}",
        f"- Assessor types: {_counts(assessor_counts)}",
        f"- Papers downranked: {len(stats.downranked)}",
        f"- Papers hidden: {len(stats.suppressed)}",
        f"- Assessments with score caps: {len(capped)}",
        f"- Assessment failures: {len(stats.failures)}",
        f"- Extraction failures: {len(stats.extraction_failures)}",
        f"- Cache hits / misses: {stats.cache_hits} / {stats.cache_misses}",
        f"- Assessment version: `{assessment_version}`",
        f"- Rubric version: `{rubric_version}`",
        "",
        "## Per-paper assessment",
        "",
    ]
    if not assessments:
        lines.append("No papers required assessment in this run.")
    for item in assessments:
        score = str(item.overall_quality_score) if item.overall_quality_score is not None else "not enough evidence"
        lines.extend(
            [
                f"### `{item.canonical_id}`",
                "",
                f"- Automated score: {score}",
                f"- Recommendation: {item.recommendation}",
                f"- Confidence / scope: {item.confidence} / {item.assessment_scope}",
                f"- Paper type: {item.paper_type}",
                f"- Summary: {item.concise_summary}",
            ]
        )
        if item.concerns:
            lines.append(f"- Main concerns: {'; '.join(item.concerns[:3])}")
        if item.positive_signals:
            lines.append(f"- Positive signals: {'; '.join(item.positive_signals[:2])}")
        lines.append("")
    if stats.extraction_failures:
        lines.extend(["## Extraction failures", ""])
        lines.extend(f"- {failure}" for failure in stats.extraction_failures)
        lines.append("")
    if stats.suppressed:
        lines.extend(["## Suppressed papers", ""])
        lines.extend(f"- `{canonical_id}`" for canonical_id in stats.suppressed)
        lines.append("")
    if unknown:
        lines.extend(["## Unknown quality", ""])
        lines.extend(f"- `{item.canonical_id}`: {item.concise_summary}" for item in unknown)
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def _counts(values: Counter[str]) -> str:
    return ", ".join(f"{key}: {count}" for key, count in sorted(values.items())) or "none"


def _score_band(score: int | None) -> str:
    if score is None:
        return "unknown"
    lower = (score // 10) * 10
    return f"{lower:02d}-{min(100, lower + 9):02d}"
