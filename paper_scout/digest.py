from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from paper_scout.models import DigestPaper


@dataclass(frozen=True)
class DigestMetadata:
    run_id: int | None = None
    source_counts: dict[str, int] = field(default_factory=dict)
    fetched_count: int = 0
    unique_count: int = 0
    decision_counts: dict[str, int] = field(default_factory=dict)
    source_failures: list[str] = field(default_factory=list)


def render_digest(digest_date: str, papers: list[DigestPaper], metadata: DigestMetadata | None = None) -> str:
    lines = [f"# Paper Scout Digest - {digest_date}", ""]
    if metadata:
        lines.extend(
            [
                "## Run Summary",
                "",
                f"- **Run ID:** {metadata.run_id if metadata.run_id is not None else 'n/a'}",
                f"- **Candidates fetched:** {metadata.fetched_count}",
                f"- **New unique papers:** {metadata.unique_count}",
                f"- **Relevant:** {metadata.decision_counts.get('relevant', 0)}",
                f"- **Maybe relevant:** {metadata.decision_counts.get('maybe', 0)}",
                f"- **Irrelevant:** {metadata.decision_counts.get('irrelevant', 0)}",
                f"- **Source summary:** {_source_summary(metadata.source_counts)}",
                "",
            ]
        )
        if metadata.source_failures:
            lines.extend(["## Source Warnings", ""])
            for failure in metadata.source_failures:
                lines.append(f"- {failure}")
            lines.append("")

    if not papers:
        lines.extend(["No new relevant or maybe-relevant papers found.", ""])
        return "\n".join(lines)

    groups: dict[str, list[DigestPaper]] = defaultdict(list)
    for paper in papers:
        groups[paper.decision].append(paper)

    for decision, heading in [("relevant", "Highly Relevant"), ("maybe", "Maybe Relevant")]:
        if not groups.get(decision):
            continue
        lines.extend([f"## {heading}", ""])
        for paper in groups[decision]:
            lines.extend(_render_paper(paper))
    return "\n".join(lines).rstrip() + "\n"


def write_digest(path, digest_date: str, papers: list[DigestPaper], metadata: DigestMetadata | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_digest(digest_date, papers, metadata), encoding="utf-8")


def _render_paper(paper: DigestPaper) -> list[str]:
    authors = ", ".join(paper.authors[:6]) if paper.authors else "Unknown authors"
    if len(paper.authors) > 6:
        authors += ", et al."
    tags = ", ".join(paper.tags) if paper.tags else "untagged"
    summary = paper.abstract_summary or _summary(paper.abstract)
    title = _escape_brackets(paper.title)
    link = paper.url or ""
    linked_title = f"[{title}]({link})" if link else title
    return [
        f"### {linked_title}",
        "",
        f"- **Authors:** {authors}",
        f"- **Date:** {paper.published_date or 'unknown'}",
        f"- **Source:** {paper.source}",
        f"- **Relevance:** {paper.decision} ({paper.score}/100)",
        f"- **Reason:** {paper.reason}",
        f"- **Tags:** {tags}",
        f"- **Abstract summary:** {summary or 'No abstract available.'}",
        "",
    ]


def _summary(abstract: str, max_chars: int = 420) -> str:
    compact = " ".join((abstract or "").split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."


def _escape_brackets(text: str) -> str:
    return text.replace("[", "\\[").replace("]", "\\]")


def _source_summary(source_counts: dict[str, int]) -> str:
    if not source_counts:
        return "none"
    return ", ".join(f"{source}: {count}" for source, count in sorted(source_counts.items()))
