from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from paper_scout.models import DigestPaper


RISK_TERMS = {
    "GPU memory": r"\bgpu memory\b",
    "CUDA memory": r"\bcuda memory\b",
    "memory bandwidth": r"\bmemory bandwidth\b",
    "memory allocation": r"\bmemory allocation\b",
    "memory-efficient attention": r"\bmemory[- ]efficient attention\b",
    "operating system memory": r"\boperating system memory\b",
    "database memory": r"\bdatabase memory\b|\bin-memory database\b",
}

STRONG_AGENT_MEMORY_TERMS = {
    "agent memory": r"\bagent memory\b|\bagentic memory\b",
    "LLM agent": r"\bllm agents?\b",
    "autonomous agent": r"\bautonomous agents?\b",
    "deep research agent": r"\bdeep research agents?\b",
    "persistent memory": r"\bpersistent memory\b",
    "episodic memory": r"\bepisodic memory\b",
    "semantic memory": r"\bsemantic memory\b",
    "Engram": r"\bengram\b",
    "parametric memory": r"\bparametric memory\b",
}


@dataclass(frozen=True)
class DigestQualityFlag:
    title: str
    source: str
    url: str | None
    decision: str
    score: int
    matched_risk_terms: list[str]


@dataclass(frozen=True)
class DigestQualityReport:
    checked_count: int
    flagged: list[DigestQualityFlag]

    @property
    def flagged_count(self) -> int:
        return len(self.flagged)


def analyze_digest_quality(papers: list[DigestPaper]) -> DigestQualityReport:
    flagged = []
    for paper in papers:
        text = f"{paper.title}\n{paper.abstract}".lower()
        risk_terms = _matches(RISK_TERMS, text)
        strong_terms = _matches(STRONG_AGENT_MEMORY_TERMS, text)
        if risk_terms and not strong_terms:
            flagged.append(
                DigestQualityFlag(
                    title=paper.title,
                    source=paper.source,
                    url=paper.url,
                    decision=paper.decision,
                    score=paper.score,
                    matched_risk_terms=risk_terms,
                )
            )
    return DigestQualityReport(checked_count=len(papers), flagged=flagged)


def write_digest_quality_report(report_dir: Path, report_date: str, papers: list[DigestPaper]) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    report = analyze_digest_quality(papers)
    path = report_dir / f"digest-quality-{report_date}.md"
    lines = [
        f"# Paper Scout Digest Quality - {report_date}",
        "",
        f"- **Digest papers checked:** {report.checked_count}",
        f"- Likely false positives flagged: {report.flagged_count}",
        "- **Workflow behavior:** advisory only; this report does not fail the daily run.",
        "",
        "## Likely False Positives",
        "",
    ]
    if not report.flagged:
        lines.append("- None")
    for flag in report.flagged:
        link = f" [{flag.url}]({flag.url})" if flag.url else ""
        lines.extend(
            [
                f"### {flag.title}",
                "",
                f"- **Source:** {flag.source}{link}",
                f"- **Decision:** {flag.decision} ({flag.score}/100)",
                f"- **Matched risk terms:** {', '.join(flag.matched_risk_terms)}",
                "",
            ]
        )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def _matches(patterns: dict[str, str], text: str) -> list[str]:
    return [label for label, pattern in patterns.items() if re.search(pattern, text, flags=re.I)]
