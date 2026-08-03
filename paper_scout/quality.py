from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import re

from paper_scout.full_text import SelectedPaperText, SelectedSection, select_assessment_text
from paper_scout.models import PaperCandidate
from paper_scout.quality_models import QUALITY_DIMENSIONS, QualityAssessment, QualityEvidence, recommendation_for_score


ASSESSMENT_VERSION = "quality-v1"
RUBRIC_VERSION = "scholarly-rubric-v1"

COMMON_WEIGHTS = {
    "contribution_clarity": 0.10,
    "scholarly_novelty_or_value": 0.20,
    "methodological_rigor": 0.15,
    "evaluation_or_validation_strength": 0.25,
    "evidence_to_claim_alignment": 0.15,
    "related_work_and_gap_positioning": 0.05,
    "reproducibility_and_transparency": 0.07,
    "limitations_and_uncertainty_handling": 0.02,
    "presentation_and_precision": 0.01,
}
THEORETICAL_WEIGHTS = {
    **COMMON_WEIGHTS,
    "methodological_rigor": 0.30,
    "evaluation_or_validation_strength": 0.20,
    "evidence_to_claim_alignment": 0.10,
    "reproducibility_and_transparency": 0.03,
    "limitations_and_uncertainty_handling": 0.01,
}
SURVEY_WEIGHTS = {
    "contribution_clarity": 0.10,
    "scholarly_novelty_or_value": 0.20,
    "methodological_rigor": 0.20,
    "evaluation_or_validation_strength": 0.20,
    "evidence_to_claim_alignment": 0.10,
    "related_work_and_gap_positioning": 0.10,
    "reproducibility_and_transparency": 0.05,
    "limitations_and_uncertainty_handling": 0.03,
    "presentation_and_precision": 0.02,
}
DATASET_WEIGHTS = {
    "contribution_clarity": 0.10,
    "scholarly_novelty_or_value": 0.15,
    "methodological_rigor": 0.20,
    "evaluation_or_validation_strength": 0.20,
    "evidence_to_claim_alignment": 0.10,
    "related_work_and_gap_positioning": 0.05,
    "reproducibility_and_transparency": 0.15,
    "limitations_and_uncertainty_handling": 0.04,
    "presentation_and_precision": 0.01,
}


@dataclass
class QualitySignals:
    positive: list[str] = field(default_factory=list)
    concerns: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    evidence: list[QualityEvidence] = field(default_factory=list)
    flags: set[str] = field(default_factory=set)

    def add_positive(self, flag: str, message: str, dimension: str, selected: SelectedPaperText, pattern: str | None = None) -> None:
        if flag in self.flags:
            return
        self.flags.add(flag)
        self.positive.append(message)
        self.evidence.append(_evidence(dimension, "positive", message, selected, pattern))

    def add_concern(self, flag: str, message: str, dimension: str, selected: SelectedPaperText, pattern: str | None = None) -> None:
        if flag in self.flags:
            return
        self.flags.add(flag)
        self.concerns.append(message)
        self.evidence.append(_evidence(dimension, "concern", message, selected, pattern))

    def add_missing(self, flag: str, message: str, dimension: str) -> None:
        if flag in self.flags:
            return
        self.flags.add(flag)
        self.missing.append(message)
        self.evidence.append(
            QualityEvidence(
                dimension=dimension,
                signal_type="missing",
                paraphrase=message,
                explanation="The item was not detected in the available material; human review may find evidence outside the extracted text.",
            )
        )


def assess_quality_deterministically(
    candidate: PaperCandidate,
    canonical_id: str,
    selected_text: SelectedPaperText | None = None,
    assessment_version: str = ASSESSMENT_VERSION,
    rubric_version: str = RUBRIC_VERSION,
) -> QualityAssessment:
    selected = selected_text or select_assessment_text(candidate, None)
    paper_type = classify_paper_type(candidate.title, selected.text)
    if selected.scope == "metadata_only" or len(selected.text.strip()) < 80:
        missing = ["Not enough paper content was available for a defensible scholarly-quality score.", *selected.warnings]
        return QualityAssessment(
            canonical_id=canonical_id,
            overall_quality_score=None,
            confidence="low",
            recommendation="unknown",
            paper_type=paper_type,
            assessment_scope=selected.scope,
            assessment_version=assessment_version,
            rubric_version=rubric_version,
            assessor_type="deterministic",
            source_content_hash=selected.content_hash,
            assessed_at=_now(),
            dimension_scores={dimension: None for dimension in QUALITY_DIMENSIONS},
            missing_information=missing,
            concise_summary="Not enough evidence was available for an automated scholarly-quality assessment.",
        )

    signals = detect_quality_signals(selected, paper_type)
    dimensions = dimension_scores(paper_type, signals, selected)
    score = _weighted_score(dimensions, _weights_for_type(paper_type))
    cap, cap_reason = _score_cap(paper_type, signals, selected)
    if cap is not None:
        score = min(score, cap)
    confidence = _confidence(selected, signals)
    recommendation = recommendation_for_score(score, confidence)
    summary = _summary(score, recommendation, confidence, signals, selected.scope)
    return QualityAssessment(
        canonical_id=canonical_id,
        overall_quality_score=score,
        confidence=confidence,
        recommendation=recommendation,
        paper_type=paper_type,
        assessment_scope=selected.scope,
        assessment_version=assessment_version,
        rubric_version=rubric_version,
        assessor_type="deterministic",
        source_content_hash=selected.content_hash,
        assessed_at=_now(),
        dimension_scores=dimensions,
        positive_signals=signals.positive,
        concerns=signals.concerns,
        evidence=signals.evidence,
        missing_information=[*signals.missing, *selected.warnings],
        concise_summary=summary,
        applied_score_cap=cap,
        applied_score_cap_reason=cap_reason,
    )


def classify_paper_type(title: str, text: str) -> str:
    haystack = f"{title}\n{text}".lower()
    title_lower = title.lower()
    if re.search(r"\b(systematic|scoping|literature) review\b|\bsurvey\b|\bmeta-analysis\b", haystack):
        return "survey_or_review"
    if re.search(r"\bposition paper\b|\bperspective\b|\bconceptual framework\b|\bwe argue\b", haystack):
        return "position_or_conceptual"
    if re.search(r"\btheorem\b|\blemma\b|\bproof\b|\bformal definition\b", haystack):
        return "theoretical"
    if re.search(r"\breplication\b|\breproducibility study\b", haystack):
        return "replication"
    if re.search(r"\bcase study\b|\bcase analysis\b", haystack):
        return "case_study"
    if re.search(r"\b(dataset|benchmark|corpus|data set)\b", title_lower) or re.search(
        r"\b(we (?:release|introduce|present)|this paper (?:releases|introduces|presents)) (?:a |an )?(?:new )?(dataset|benchmark|corpus|data set)\b",
        haystack,
    ):
        return "dataset_or_benchmark"
    if re.search(r"\bsystem architecture\b|\bprototype\b|\bplatform\b|\bdeployed (?:system|application)\b", haystack) or re.search(
        r"\b(system|assistant|platform|architecture)\b", title_lower
    ):
        return "systems_or_application"
    if re.search(r"\b(method|algorithm)\b", title_lower):
        return "methods_or_algorithm"
    if re.search(r"\bexperiment\b|\bevaluat(?:e|es|ed|ing|ion)\b|\bparticipants?\b|\bcontrolled study\b", haystack):
        return "empirical_research"
    if re.search(r"\bmethod\b|\balgorithm\b|\boptimization\b|\bmodel architecture\b", haystack):
        return "methods_or_algorithm"
    return "unclear"


def detect_quality_signals(selected: SelectedPaperText, paper_type: str) -> QualitySignals:
    text = selected.text
    lower = text.lower()
    signals = QualitySignals()
    _positive_if(signals, lower, r"\b(our contributions?|we contribute|this paper introduces|we (?:propose|introduce|present|release))\b", "explicit_contribution", "The contribution is stated explicitly.", "contribution_clarity", selected)
    _positive_if(signals, lower, r"\b(dataset|corpus|benchmark)\b", "dataset", "The available text identifies data or a benchmark used by the work.", "methodological_rigor", selected)
    _positive_if(signals, lower, r"\b(baseline|compar(?:e|ed) (?:against|with)|comparison (?:against|with)|state-of-the-art)\b", "baseline", "A baseline or comparison system is described.", "evaluation_or_validation_strength", selected)
    _positive_if(signals, lower, r"\b(accuracy|precision|recall|f1|auc|bleu|rouge|latency|throughput|cost|seconds?|milliseconds?)\b.{0,80}\b\d+(?:\.\d+)?(?:%|ms|s)?\b", "metrics", "Quantitative evaluation signals were detected.", "evaluation_or_validation_strength", selected)
    _positive_if(signals, lower, r"\bablation\b", "ablation", "An ablation analysis is reported.", "evaluation_or_validation_strength", selected)
    _positive_if(signals, lower, r"\b(error analysis|failure analysis|qualitative analysis)\b", "error_analysis", "The work reports an error or qualitative analysis.", "evaluation_or_validation_strength", selected)
    _positive_if(signals, lower, r"\b(user study|participants?|expert evaluation|operational evaluation|real-world deployment)\b", "user_evaluation", "User, expert, operational, or deployment evidence is described.", "evaluation_or_validation_strength", selected)
    _positive_if(signals, lower, r"\b(robustness|sensitivity analysis|statistical significance|confidence interval|p\s*[<=>])\b", "robustness", "Robustness or statistical analysis is reported.", "methodological_rigor", selected)
    _positive_if(signals, lower, r"\b(limitations?|threats to validity)\b", "limitations", "Limitations or threats to validity are acknowledged.", "limitations_and_uncertainty_handling", selected)
    _positive_if(signals, lower, r"\b(code|data|repository|artifacts?) (?:is|are|will be) (?:available|released)|github\.com", "artifacts", "Code, data, or research artifacts are described as available.", "reproducibility_and_transparency", selected)
    _positive_if(signals, lower, r"\b(theorem|lemma|proof|proposition)\b", "proof", "Formal definitions or proof-oriented evidence is present.", "methodological_rigor", selected)
    _positive_if(signals, lower, r"\b(prisma|search strategy|inclusion criteria|exclusion criteria|databases searched|screening process)\b", "review_method", "A review or study-selection methodology is described.", "methodological_rigor", selected)
    _positive_if(signals, lower, r"\b(ethics|license|annotation guidelines|quality control|inter-annotator)\b", "dataset_documentation", "Dataset documentation, quality control, licensing, or ethics is discussed.", "reproducibility_and_transparency", selected)

    # Lists of absent evaluation elements are common in limitations. Do not turn
    # those negated mentions into positive evidence.
    negated_signals = {
        "dataset": r"dataset|benchmark|corpus",
        "baseline": r"baseline|comparison",
        "metrics": r"metrics?|accuracy|precision|recall|f1|auc|latency|scalability measurements?",
        "ablation": r"ablation",
        "user_evaluation": r"user stud(?:y|ies)|expert evaluation|deployment",
    }
    for flag, phrase in negated_signals.items():
        if re.search(rf"\bno\b[^.\n]{{0,320}}\b(?:{phrase})\b", lower):
            _remove_positive(signals, flag)

    standard_stack = sum(term in lower for term in ("pdf parsing", "sentence-bert", "chromadb", "bm25", "neo4j", "streamlit", "vector database", "knowledge graph"))
    if standard_stack >= 4 and not {"baseline", "metrics", "ablation", "user_evaluation"} & signals.flags:
        signals.add_concern(
            "integration_only",
            "The available contribution appears to combine established components without comparative evidence that the integration adds scholarly value.",
            "scholarly_novelty_or_value",
            selected,
            r"sentence-bert|chromadb|bm25|neo4j|streamlit",
        )
    if re.search(r"\b(successfully (?:implemented|developed|processed|generated)|prototype (?:worked|runs?|operates?))\b", lower):
        signals.add_concern(
            "functionality_only",
            "The available results appear to demonstrate functionality rather than comparative effectiveness.",
            "evaluation_or_validation_strength",
            selected,
            r"successfully (?:implemented|developed|processed|generated)|prototype (?:worked|runs?|operates?)",
        )
    if re.search(r"\b(future work|future research)\b.{0,160}\b(evaluat|benchmark|user stud|ablation|scalab|latency)\w*", lower):
        signals.add_concern(
            "evaluation_deferred",
            "Meaningful evaluation appears to be deferred to future work in the available text.",
            "evaluation_or_validation_strength",
            selected,
            r"future work|future research",
        )

    empirical_types = {"empirical_research", "systems_or_application", "methods_or_algorithm", "case_study", "replication"}
    if paper_type in empirical_types:
        if "baseline" not in signals.flags:
            signals.add_missing("no_baseline", "No suitable baseline comparison was detected in the available text.", "evaluation_or_validation_strength")
        if "metrics" not in signals.flags and "user_evaluation" not in signals.flags:
            signals.add_missing("no_metrics", "No quantitative, user, expert, or operational evaluation was detected in the available text.", "evaluation_or_validation_strength")
        if "ablation" not in signals.flags and standard_stack >= 2:
            signals.add_concern(
                "components_not_validated",
                "Architecture components are presented, but their individual contribution was not evaluated in the available text.",
                "evidence_to_claim_alignment",
                selected,
            )
    comparative_claim = bool(re.search(r"\b(improv(?:e|es|ed)|better|outperform|more (?:accurate|efficient|scalable)|reduce[sd]? hallucination|higher quality)\b", lower))
    if comparative_claim and "baseline" not in signals.flags:
        signals.add_concern(
            "unsupported_comparison",
            "Comparative claims were detected without a suitable baseline in the available text.",
            "evidence_to_claim_alignment",
            selected,
        )
    if paper_type == "survey_or_review" and "review_method" not in signals.flags:
        signals.add_missing("no_review_method", "No reproducible review or selection methodology was detected.", "methodological_rigor")
    if paper_type == "theoretical" and "proof" not in signals.flags:
        signals.add_missing("no_proof", "No formal proof or internal-consistency evidence was detected.", "methodological_rigor")
    if paper_type == "dataset_or_benchmark" and "dataset_documentation" not in signals.flags:
        signals.add_missing("no_dataset_controls", "Dataset quality controls, licensing, ethics, or documentation were not detected.", "reproducibility_and_transparency")
    return signals


def dimension_scores(paper_type: str, signals: QualitySignals, selected: SelectedPaperText) -> dict[str, int | None]:
    flags = signals.flags
    scores = {dimension: 3 for dimension in QUALITY_DIMENSIONS}
    scores["contribution_clarity"] = 4 if "explicit_contribution" in flags else 2
    scores["scholarly_novelty_or_value"] = 1 if "integration_only" in flags else (4 if "explicit_contribution" in flags else 3)
    scores["methodological_rigor"] = min(5, 2 + sum(flag in flags for flag in ("dataset", "robustness", "review_method", "proof", "dataset_documentation")))
    validation_flags = ("baseline", "metrics", "ablation", "error_analysis", "user_evaluation", "robustness", "proof", "review_method")
    scores["evaluation_or_validation_strength"] = min(5, sum(flag in flags for flag in validation_flags))
    if "functionality_only" in flags:
        scores["evaluation_or_validation_strength"] = min(scores["evaluation_or_validation_strength"], 1)
    scores["evidence_to_claim_alignment"] = max(0, 4 - sum(flag in flags for flag in ("unsupported_comparison", "components_not_validated", "functionality_only")))
    scores["related_work_and_gap_positioning"] = 3 if re.search(r"\brelated work\b|\bprior work\b", selected.text.lower()) else 2
    scores["reproducibility_and_transparency"] = min(5, 2 + sum(flag in flags for flag in ("artifacts", "dataset_documentation", "review_method")))
    scores["limitations_and_uncertainty_handling"] = 4 if "limitations" in flags else 1
    scores["presentation_and_precision"] = 3
    if paper_type == "position_or_conceptual":
        scores["evaluation_or_validation_strength"] = 3
        scores["methodological_rigor"] = 3 if re.search(r"\b(counterargument|evidence|prior work)\b", selected.text.lower()) else 2
    elif paper_type == "survey_or_review" and "review_method" in flags:
        scores["methodological_rigor"] = 5
        scores["evaluation_or_validation_strength"] = 4
        scores["evidence_to_claim_alignment"] = 4
        scores["related_work_and_gap_positioning"] = 4
    elif paper_type == "theoretical" and "proof" in flags:
        scores["methodological_rigor"] = 5
        scores["evaluation_or_validation_strength"] = 4
        scores["evidence_to_claim_alignment"] = 4
    if selected.scope == "title_and_abstract":
        for dimension in QUALITY_DIMENSIONS:
            if dimension not in {"contribution_clarity", "presentation_and_precision"}:
                scores[dimension] = None
    return scores


def combined_rank_score(
    relevance_score: int,
    assessment: QualityAssessment | None,
    relevance_weight: float = 0.75,
    quality_weight: float = 0.25,
    unknown_quality_is_neutral: bool = True,
) -> float:
    relevance = max(0, min(100, relevance_score)) / 100
    if assessment is None or assessment.overall_quality_score is None:
        return relevance if unknown_quality_is_neutral else relevance_weight * relevance
    confidence_factor = {"high": 1.0, "medium": 0.65, "low": 0.25}[assessment.confidence]
    scope_factor = {"full_text": 1.0, "partial_full_text": 0.8, "title_and_abstract": 0.35, "metadata_only": 0.0}[assessment.assessment_scope]
    effective_quality = quality_weight * confidence_factor * scope_factor
    effective_relevance = max(0.0, relevance_weight + quality_weight - effective_quality)
    denominator = effective_relevance + effective_quality
    return (effective_relevance * relevance + effective_quality * (assessment.overall_quality_score / 100)) / denominator


def should_suppress_quality(
    assessment: QualityAssessment | None,
    behavior: str,
    hide_below: int,
    minimum_confidence: str,
    pinned: bool = False,
    include_despite_quality: bool = False,
    suppress_for_quality: bool = False,
) -> bool:
    if pinned or include_despite_quality:
        return False
    if suppress_for_quality:
        return True
    if behavior != "hide" or assessment is None or assessment.overall_quality_score is None:
        return False
    if assessment.assessment_scope in {"metadata_only", "title_and_abstract"}:
        return False
    confidence_rank = {"low": 1, "medium": 2, "high": 3}
    return assessment.overall_quality_score < hide_below and confidence_rank[assessment.confidence] >= confidence_rank[minimum_confidence]


def _positive_if(signals: QualitySignals, lower: str, pattern: str, flag: str, message: str, dimension: str, selected: SelectedPaperText) -> None:
    if re.search(pattern, lower, flags=re.DOTALL):
        signals.add_positive(flag, message, dimension, selected, pattern)


def _remove_positive(signals: QualitySignals, flag: str) -> None:
    if flag not in signals.flags:
        return
    signals.flags.remove(flag)
    matching = [item for item in signals.evidence if item.signal_type == "positive" and _positive_flag_matches(flag, item.paraphrase)]
    removed_messages = {item.paraphrase for item in matching}
    signals.evidence = [item for item in signals.evidence if item not in matching]
    signals.positive = [message for message in signals.positive if message not in removed_messages]


def _positive_flag_matches(flag: str, paraphrase: str) -> bool:
    markers = {
        "dataset": "data or a benchmark",
        "baseline": "baseline or comparison",
        "metrics": "quantitative evaluation",
        "ablation": "ablation analysis",
        "user_evaluation": "user, expert, operational",
    }
    return markers.get(flag, "") in paraphrase.lower()


def _score_cap(paper_type: str, signals: QualitySignals, selected: SelectedPaperText) -> tuple[int | None, str | None]:
    empirical_types = {"empirical_research", "systems_or_application", "methods_or_algorithm", "case_study", "replication"}
    if paper_type not in empirical_types or selected.scope in {"metadata_only", "title_and_abstract"}:
        return None, None
    if "functionality_only" in signals.flags:
        return 44, "The available results demonstrate prototype execution rather than effectiveness."
    if "no_metrics" in signals.flags and "no_baseline" in signals.flags:
        return 49, "No meaningful evaluation or suitable comparison was detected for the central systems/method claim."
    if "unsupported_comparison" in signals.flags:
        return 54, "Comparative claims were detected without a suitable baseline."
    return None, None


def _confidence(selected: SelectedPaperText, signals: QualitySignals) -> str:
    if selected.scope in {"metadata_only", "title_and_abstract"}:
        return "low"
    if selected.scope == "full_text" and not selected.section_detection_uncertain and not selected.warnings:
        return "high"
    if selected.scope in {"full_text", "partial_full_text"} and len(selected.text) >= 4_000:
        return "medium"
    return "low"


def _weighted_score(scores: dict[str, int | None], weights: dict[str, float]) -> int:
    available = [(dimension, score) for dimension, score in scores.items() if score is not None and weights.get(dimension, 0) > 0]
    if not available:
        return 0
    total_weight = sum(weights[dimension] for dimension, _ in available)
    value = sum(weights[dimension] * (score / 5) for dimension, score in available) / total_weight
    return max(0, min(100, round(value * 100)))


def _weights_for_type(paper_type: str) -> dict[str, float]:
    if paper_type == "theoretical":
        return THEORETICAL_WEIGHTS
    if paper_type == "survey_or_review":
        return SURVEY_WEIGHTS
    if paper_type == "dataset_or_benchmark":
        return DATASET_WEIGHTS
    return COMMON_WEIGHTS


def _evidence(dimension: str, signal_type: str, message: str, selected: SelectedPaperText, pattern: str | None) -> QualityEvidence:
    section = _matching_section(selected.sections, pattern) if pattern else None
    excerpt = _short_excerpt(section.text, pattern) if section and pattern else None
    return QualityEvidence(
        dimension=dimension,
        signal_type=signal_type,
        section=section.heading if section else None,
        page=section.first_page if section else None,
        excerpt=excerpt,
        paraphrase=message,
        explanation="This automated signal is based only on the supplied material and should be checked against the paper.",
    )


def _matching_section(sections: list[SelectedSection], pattern: str | None) -> SelectedSection | None:
    if not pattern:
        return None
    return next((section for section in sections if re.search(pattern, section.text.lower(), flags=re.DOTALL)), None)


def _short_excerpt(text: str, pattern: str, limit: int = 180) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    start = max(0, match.start() - 50)
    end = min(len(text), match.end() + 80)
    return " ".join(text[start:end].split())[:limit]


def _summary(score: int, recommendation: str, confidence: str, signals: QualitySignals, scope: str) -> str:
    if recommendation == "weak":
        lead = "The available evidence suggests weak or incomplete scholarly validation."
    elif recommendation == "strong":
        lead = "The available evidence suggests a clearly supported scholarly contribution."
    elif recommendation == "promising":
        lead = "The available evidence suggests a credible contribution with some limitations."
    else:
        lead = "The available evidence is mixed or incomplete."
    return f"{lead} Automated score {score}/100, {confidence} confidence, based on {scope.replace('_', ' ')}."


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()
