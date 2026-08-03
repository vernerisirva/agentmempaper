from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from paper_scout.full_text import SelectedPaperText, SelectedSection
from paper_scout.models import PaperCandidate
from paper_scout.quality import assess_quality_deterministically


@dataclass(frozen=True)
class QualityFixture:
    name: str
    title: str
    text: str
    expected_type: str
    score_range: tuple[int, int] | None
    recommendation: str
    confidence: tuple[str, ...]
    concerns: tuple[str, ...] = ()
    scope: str = "full_text"


def quality_fixtures() -> list[QualityFixture]:
    return [
        QualityFixture(
            "strong empirical paper",
            "Evaluating Persistent Memory Policies for LLM Agents",
            """Abstract\nWe propose and evaluate a memory policy.\nIntroduction\nOur contribution is a controlled study.\nMethodology\nWe use a public dataset with documented preprocessing and five random seeds.\nEvaluation\nWe compare against three baselines using accuracy 84.2%, precision 81.0%, recall 86.0%, and latency 120 ms. We report ablation, robustness checks, statistical significance, and error analysis.\nLimitations\nThe benchmark covers English tasks only. Code and data are available at github.com/example/repo.\nConclusion\nThe method improves accuracy under the evaluated conditions.""",
            "empirical_research",
            (75, 100),
            "promising",
            ("medium", "high"),
        ),
        QualityFixture(
            "strong systems paper",
            "A Deployed Shared-Memory System for Research Agents",
            """Abstract\nWe introduce a deployed system architecture.\nMethod\nThe system integrates established components to solve a difficult coordination problem.\nEvaluation\nCompared with two baselines on a public benchmark, accuracy is 91.4% and latency is 95 ms. Ablation isolates the shared-memory component. A six-month real-world deployment and expert evaluation measure operational reliability and cost.\nLimitations\nDeployment was limited to one organization. Code artifacts are available.""",
            "systems_or_application",
            (70, 100),
            "promising",
            ("medium", "high"),
        ),
        QualityFixture(
            "weak integration-only prototype",
            "Research Paper Assistant with Hybrid Retrieval and Knowledge Graphs",
            """Abstract\nWe present a research-paper assistant.\nSystem Architecture\nThe prototype uses PDF parsing, chunks text, generates Sentence-BERT embeddings, stores vectors in ChromaDB, combines dense search with BM25, sends evidence to an LLM, adds Neo4j, and provides a Streamlit interface.\nResults\nWe successfully implemented the prototype, processed papers, and generated cited answers. No defined evaluation dataset, retrieval metrics, citation-faithfulness metrics, baseline comparison, ablation study, user study, latency, or scalability measurements are reported. Neo4j is not evaluated independently.\nLimitations\nBroader evaluation, user studies, and scalability measurement are future work. The high-level architecture is documented clearly.""",
            "systems_or_application",
            (25, 45),
            "weak",
            ("medium", "high"),
            ("functionality rather than comparative effectiveness", "established components"),
        ),
        QualityFixture(
            "survey paper",
            "A Systematic Survey of Long-Term Memory in Language Agents",
            """Abstract\nWe present a systematic review and taxonomy.\nMethodology\nFollowing PRISMA, we searched five databases, publish the search strategy, and define inclusion criteria, exclusion criteria, and a screening process.\nResults\nThe survey compares 240 papers across memory writing, retrieval, consolidation, and evaluation, synthesizes conflicting evidence, and proposes a taxonomy.\nLimitations\nThe search covers English publications through 2025.""",
            "survey_or_review",
            (65, 100),
            "promising",
            ("medium", "high"),
        ),
        QualityFixture(
            "theoretical paper",
            "A Formal Theory of Memory Consistency for Agents",
            """Abstract\nWe give formal definitions for memory consistency.\nMethod\nTheorem 1 establishes convergence under stated assumptions. Lemma 2 and its proof provide the key bound. Counterexamples show why weaker assumptions fail.\nRelated Work\nWe distinguish prior consistency models.\nLimitations\nThe theory assumes deterministic updates.""",
            "theoretical",
            (60, 100),
            "promising",
            ("medium", "high"),
        ),
        QualityFixture(
            "dataset paper",
            "MemBench: A Dataset and Benchmark for Agent Memory",
            """Abstract\nWe release a benchmark and dataset.\nMethodology\nCollection methodology, annotation guidelines, inter-annotator agreement, quality control, license, and ethics review are documented.\nEvaluation\nFive baseline systems are compared using accuracy 72.5%, recall 68.4%, and robustness analysis.\nLimitations\nThe benchmark has limited multilingual coverage. Data and code are available.""",
            "dataset_or_benchmark",
            (70, 100),
            "promising",
            ("medium", "high"),
        ),
        QualityFixture(
            "position paper",
            "Position: Agent Memory Requires Governance",
            """Abstract\nWe argue that persistent agent memory requires governance.\nIntroduction\nThe thesis is grounded in prior work and documented incidents. We address counterarguments about user control and practical implications for system design.\nLimitations\nThis position paper does not establish empirical effectiveness and identifies evidence needed in future work.""",
            "position_or_conceptual",
            (45, 85),
            "uncertain",
            ("medium", "high"),
        ),
        QualityFixture(
            "incomplete extraction",
            "A New Agent Memory Method",
            "Abstract\nWe propose a potentially useful agent-memory method, but the evaluation pages could not be extracted.",
            "methods_or_algorithm",
            (40, 80),
            "uncertain",
            ("low",),
            scope="title_and_abstract",
        ),
    ]


def evaluate_quality_fixtures() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures: list[str] = []
    for index, fixture in enumerate(quality_fixtures()):
        candidate = PaperCandidate(fixture.title, ["Fixture Author"], fixture.text, "fixture", fixture.name)
        selected = SelectedPaperText(
            text=fixture.text,
            sections=[SelectedSection("Fixture full text", fixture.text, 1)],
            scope=fixture.scope,
            content_hash=f"fixture-{index}",
            section_detection_uncertain=fixture.scope != "full_text",
            warnings=["Evaluation section extraction was incomplete."] if fixture.scope != "full_text" else [],
        )
        assessment = assess_quality_deterministically(candidate, f"fixture:{index}", selected)
        type_ok = assessment.paper_type == fixture.expected_type
        score_ok = fixture.score_range is None or (
            assessment.overall_quality_score is not None
            and fixture.score_range[0] <= assessment.overall_quality_score <= fixture.score_range[1]
        )
        recommendation_ok = assessment.recommendation == fixture.recommendation
        confidence_ok = assessment.confidence in fixture.confidence
        concern_text = " ".join(assessment.concerns).lower()
        concerns_ok = all(expected.lower() in concern_text for expected in fixture.concerns)
        passed = type_ok and score_ok and recommendation_ok and confidence_ok and concerns_ok
        if not passed:
            failures.append(fixture.name)
        rows.append(
            {
                "name": fixture.name,
                "expected_type": fixture.expected_type,
                "actual_type": assessment.paper_type,
                "expected_score_range": fixture.score_range,
                "actual_score": assessment.overall_quality_score,
                "expected_recommendation": fixture.recommendation,
                "actual_recommendation": assessment.recommendation,
                "expected_confidence": fixture.confidence,
                "actual_confidence": assessment.confidence,
                "expected_concerns": fixture.concerns,
                "actual_concerns": assessment.concerns,
                "passed": passed,
            }
        )
    return {"fixtures": rows, "failures": failures, "passed": not failures}


def write_quality_evaluation_report(report: dict[str, object], report_dir: Path, report_date: str) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"quality-eval-{report_date}.md"
    rows = report["fixtures"]
    lines = [
        f"# Paper Scout quality evaluation - {report_date}",
        "",
        "> Deterministic fixture regression coverage; this is not a claim of production-level quality-assessment accuracy.",
        "",
        f"- Passed: {len(rows) - len(report['failures'])}/{len(rows)}",
        f"- Failed: {len(report['failures'])}",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['name']}",
                "",
                f"- Result: {'PASS' if row['passed'] else 'FAIL'}",
                f"- Paper type: expected `{row['expected_type']}`, actual `{row['actual_type']}`",
                f"- Score: expected `{row['expected_score_range']}`, actual `{row['actual_score']}`",
                f"- Recommendation: expected `{row['expected_recommendation']}`, actual `{row['actual_recommendation']}`",
                f"- Confidence: expected `{row['expected_confidence']}`, actual `{row['actual_confidence']}`",
                f"- Concerns: {'; '.join(row['actual_concerns']) or 'none'}",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
