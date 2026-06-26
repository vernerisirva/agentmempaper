from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from paper_scout.llm import classify_with_optional_llm
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.relevance import classify_with_rules, should_consider_for_llm


@dataclass(frozen=True)
class RelevanceExample:
    name: str
    expected_relevant: bool
    candidate: PaperCandidate


def relevance_fixture_examples() -> list[RelevanceExample]:
    relevant = [
        ("long-term memory for LLM agents", "Long-Term Memory for LLM Agents", "Persistent long-term memory for language model agents with retrieval and update policies."),
        ("episodic memory in autonomous agents", "Episodic Memory in Autonomous Agents", "Autonomous LLM agents store episodic memory across multi-step tasks."),
        ("semantic memory for deep research agents", "Semantic Memory for Deep Research Agents", "Deep research agents maintain semantic memory while producing literature reviews."),
        ("procedural memory for tool-using agents", "Procedural Memory for Tool-Using Agents", "Tool-using language agents learn procedural memory for recurring workflows."),
        ("persistent memory in literature-review agents", "Persistent Memory in Literature-Review Agents", "Research agents use persistent memory to avoid stale literature-review context."),
        ("memory write/read policies for LLM agents", "Memory Write and Read Policies for LLM Agents", "We evaluate memory write policy and retrieval policy choices in LLM agents."),
        ("agent memory benchmark", "Agent Memory Benchmark", "A benchmark for persistent memory in language model agents."),
        ("parametric memory for language agents", "Parametric Memory for Language Agents", "Parametric memory mechanisms are evaluated in agent behavior."),
        ("Engram-style mechanisms in LLMs", "Engram-Style Mechanisms in LLMs", "Engram memory mechanisms alter language model behavior for long-running agents."),
        ("multilingual Engram-style memory", "Multilingual Engram-Style Memory", "A multilingual Engram memory mechanism for language model agents."),
    ]
    irrelevant = [
        ("GPU memory allocation", "GPU Memory Allocation for Training", "CUDA kernels allocate GPU memory efficiently."),
        ("CUDA memory fragmentation", "CUDA Memory Fragmentation", "A runtime method reduces CUDA memory fragmentation."),
        ("memory-efficient attention only", "Memory-Efficient Attention", "Attention kernels reduce KV cache and memory use."),
        ("database in-memory indexing", "In-Memory Database Indexing", "Database memory indexing improves transaction throughput."),
        ("operating system memory paging", "Operating System Memory Paging", "A memory paging algorithm for operating systems."),
        ("human memory psychology without AI agents", "Human Cognitive Memory", "Psychology experiments study human memory recall."),
        ("generic RAG without persistent memory", "Generic RAG for Question Answering", "A generic RAG system retrieves documents without persistent memory."),
        ("vector database retrieval without agent memory", "Vector Database Retrieval", "Vector search improves document retrieval without agent memory."),
        ("memory bandwidth optimization", "Memory Bandwidth Optimization", "Hardware memory bandwidth optimization for GPUs."),
        ("cache optimization", "Cache Optimization", "Compiler cache optimization for numerical kernels."),
    ]
    examples: list[RelevanceExample] = []
    for name, title, abstract in relevant:
        examples.append(
            RelevanceExample(
                name=name,
                expected_relevant=True,
                candidate=PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract, source="fixture", source_id=name, url="https://example.test/relevant", published_date="2026-01-01"),
            )
        )
    for name, title, abstract in irrelevant:
        examples.append(
            RelevanceExample(
                name=name,
                expected_relevant=False,
                candidate=PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract, source="fixture", source_id=name, url="https://example.test/irrelevant", published_date="2026-01-01"),
            )
        )
    return examples


def evaluate_relevance_examples(examples: list[RelevanceExample], use_llm: bool = False) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    false_positives: list[str] = []
    false_negatives: list[str] = []
    true_positive = false_positive = true_negative = false_negative = 0

    for example in examples:
        rule_result = classify_with_rules(example.candidate)
        result = (
            classify_with_optional_llm(example.candidate, rule_result)
            if use_llm and should_consider_for_llm(rule_result)
            else rule_result
        )
        predicted_relevant = result.decision in {"relevant", "maybe"}
        if predicted_relevant and example.expected_relevant:
            true_positive += 1
        elif predicted_relevant and not example.expected_relevant:
            false_positive += 1
            false_positives.append(example.name)
        elif not predicted_relevant and example.expected_relevant:
            false_negative += 1
            false_negatives.append(example.name)
        else:
            true_negative += 1

        rows.append(
            {
                "name": example.name,
                "expected": "relevant" if example.expected_relevant else "irrelevant",
                "decision": result.decision,
                "score": result.score,
                "reason": result.reason,
                "tags": result.tags,
            }
        )

    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 1.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 1.0
    return {
        "precision": precision,
        "recall": recall,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "true_negative": true_negative,
        "false_negative": false_negative,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "rows": rows,
        "used_llm": use_llm,
    }


def write_relevance_report(report: dict[str, object], report_dir: Path, report_date: str | None = None) -> Path:
    active_date = report_date or date.today().isoformat()
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"relevance-eval-{active_date}.md"
    path.write_text(render_relevance_report(report, active_date), encoding="utf-8")
    return path


def render_relevance_report(report: dict[str, object], report_date: str) -> str:
    lines = [
        f"# Paper Scout Relevance Evaluation - {report_date}",
        "",
        f"- **Precision-like score:** {report['precision']:.3f}",
        f"- **Recall-like score:** {report['recall']:.3f}",
        f"- **False positives:** {len(report['false_positives'])}",
        f"- **False negatives:** {len(report['false_negatives'])}",
        f"- **LLM classifier used:** {report['used_llm']}",
        "",
        "## False Positives",
        "",
    ]
    lines.extend([f"- {name}" for name in report["false_positives"]] or ["- None"])
    lines.extend(["", "## False Negatives", ""])
    lines.extend([f"- {name}" for name in report["false_negatives"]] or ["- None"])
    lines.extend(["", "## Per-Example Decisions", ""])
    for row in report["rows"]:
        lines.extend(
            [
                f"### {row['name']}",
                "",
                f"- **Expected:** {row['expected']}",
                f"- **Decision:** {row['decision']}",
                f"- **Score:** {row['score']}",
                f"- **Reason:** {row['reason']}",
                f"- **Tags:** {', '.join(row['tags']) if row['tags'] else 'none'}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
