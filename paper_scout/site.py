from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date
from html import escape
import io
import json
from pathlib import Path
import re
import sqlite3


@dataclass(frozen=True)
class SiteBuildResult:
    built: bool
    message: str
    latest_date: str | None = None
    output_dir: Path | None = None


@dataclass(frozen=True)
class ParsedPaper:
    title: str
    url: str | None
    authors: str
    date: str
    source: str
    decision: str
    score: str
    reason: str
    tags: list[str]
    abstract_summary: str
    section: str

    @property
    def citation(self) -> str:
        parts = [self.title]
        if self.authors and self.authors != "Unknown authors":
            parts.append(self.authors)
        if self.date and self.date != "unknown":
            parts.append(self.date)
        if self.url:
            parts.append(self.url)
        return ". ".join(parts)


@dataclass(frozen=True)
class ParsedDigest:
    date: str
    summary: dict[str, str] = field(default_factory=dict)
    source_warnings: list[str] = field(default_factory=list)
    papers: list[ParsedPaper] = field(default_factory=list)
    digest_quality_warning_count: int = 0


@dataclass(frozen=True)
class LibraryPaper:
    canonical_id: str
    title: str
    authors: list[str]
    abstract_summary: str
    reason: str
    score: int
    decision: str
    tags: list[str]
    source: str
    source_id: str | None
    doi: str | None
    arxiv_id: str | None
    semantic_scholar_id: str | None
    openalex_id: str | None
    url: str | None
    published_date: str | None
    first_seen_at: str | None
    last_seen_at: str | None
    notified_at: str | None
    notified_date: str | None
    appeared_in_latest_run: bool = False
    newly_discovered_in_latest_run: bool = False
    sources: list[str] = field(default_factory=list)
    source_ids: dict[str, list[str]] = field(default_factory=dict)
    alternate_urls: list[str] = field(default_factory=list)
    pinned: bool = False
    research_note: str | None = None
    review_status: str | None = None
    relevance_label: str | None = None
    future_date: bool = False

    @property
    def authors_text(self) -> str:
        return ", ".join(self.authors) if self.authors else "Unknown authors"

    @property
    def first_seen_date(self) -> str:
        return _date_part(self.first_seen_at) or "unknown"

    @property
    def last_seen_date(self) -> str:
        return _date_part(self.last_seen_at) or "unknown"

    @property
    def citation(self) -> str:
        parts = [self.title]
        if self.authors:
            parts.append(self.authors_text)
        if self.published_date:
            parts.append(self.published_date)
        if self.url:
            parts.append(self.url)
        return ". ".join(parts)


@dataclass(frozen=True)
class CurationRule:
    title: str | None = None
    canonical_id: str | None = None
    note: str | None = None
    decision: str | None = None
    score: int | None = None
    tags: list[str] = field(default_factory=list)
    review_status: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class CurationConfig:
    pinned: list[CurationRule] = field(default_factory=list)
    overrides: list[CurationRule] = field(default_factory=list)
    excluded: list[CurationRule] = field(default_factory=list)


def build_site(
    digest_dir: Path | str = Path("digests"),
    report_dir: Path | str = Path("reports/paper_scout"),
    docs_dir: Path | str = Path("docs"),
    state_path: Path | str = Path("data/paper_scout.sqlite3"),
    curation_path: Path | str = Path("config/curation.yaml"),
) -> SiteBuildResult:
    digest_path = _latest_digest_path(Path(digest_dir))
    if digest_path is None:
        return SiteBuildResult(False, f"No daily digest files found in {digest_dir}. Run `python3 -m paper_scout run` first.")

    digest_root = Path(digest_dir)
    report_root = Path(report_dir)
    docs_root = Path(docs_dir)
    archive_digests = [_parse_digest(path, report_root) for path in _daily_digest_paths(digest_root)]
    latest = archive_digests[-1]
    library_papers = _load_library_papers(Path(state_path))
    using_state = bool(library_papers)
    if not library_papers:
        library_papers = _library_from_digests(archive_digests)
    library_papers = _merge_dashboard_duplicates(library_papers)
    library_papers = _apply_curation(library_papers, _load_curation(Path(curation_path)), latest.date)
    library_papers = _sort_recommended(library_papers)
    latest_discoveries = [paper for paper in library_papers if paper.newly_discovered_in_latest_run]
    if not using_state and not latest_discoveries:
        latest_discoveries = _library_from_digest(latest, latest_run=True, newly_discovered=True)

    docs_root.mkdir(parents=True, exist_ok=True)
    (docs_root / "data").mkdir(parents=True, exist_ok=True)
    (docs_root / "style.css").write_text(STYLE_CSS, encoding="utf-8")
    (docs_root / "index.html").write_text(_render_library_page(library_papers, latest, archive_digests), encoding="utf-8")
    (docs_root / "latest.html").write_text(_render_latest_discoveries_page(latest_discoveries, latest, archive_digests), encoding="utf-8")
    (docs_root / "archive.html").write_text(_render_archive_page(archive_digests), encoding="utf-8")
    (docs_root / "about.html").write_text(_render_about_page(), encoding="utf-8")
    (docs_root / "data" / "papers.json").write_text(json.dumps([_library_paper_to_json(paper) for paper in library_papers], indent=2, sort_keys=True), encoding="utf-8")
    (docs_root / "data" / "latest.json").write_text(json.dumps(_latest_to_json(latest, latest_discoveries), indent=2, sort_keys=True), encoding="utf-8")
    (docs_root / "data" / "papers.csv").write_text(_papers_csv(library_papers), encoding="utf-8")
    (docs_root / "data" / "papers.bib").write_text(_papers_bibtex(library_papers), encoding="utf-8")
    _write_latest_markdown(digest_root, latest.date, digest_path)

    return SiteBuildResult(True, f"Built Paper Scout dashboard for {latest.date} in {docs_root}", latest.date, docs_root)


def _latest_digest_path(digest_dir: Path) -> Path | None:
    paths = _daily_digest_paths(digest_dir)
    return paths[-1] if paths else None


def _daily_digest_paths(digest_dir: Path) -> list[Path]:
    if not digest_dir.exists():
        return []
    return sorted(path for path in digest_dir.glob("*.md") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", path.stem))


def _parse_digest(path: Path, report_dir: Path) -> ParsedDigest:
    lines = path.read_text(encoding="utf-8").splitlines()
    date = _date_from_title(lines[0] if lines else path.stem) or path.stem
    summary: dict[str, str] = {}
    warnings: list[str] = []
    papers: list[ParsedPaper] = []
    current_section: str | None = None
    current_paper: dict[str, object] | None = None

    for line in lines:
        if line.startswith("## "):
            if current_paper is not None:
                papers.append(_paper_from_dict(current_paper))
                current_paper = None
            current_section = line[3:].strip()
            continue
        if current_section == "Run Summary" and line.startswith("- **"):
            key, value = _parse_bold_bullet(line)
            if key:
                summary[key] = value
            continue
        if current_section == "Source Warnings" and line.startswith("- "):
            warnings.append(_redact_secrets(line[2:].strip()))
            continue
        if current_section in {"Highly Relevant", "Maybe Relevant"}:
            if line.startswith("### "):
                if current_paper is not None:
                    papers.append(_paper_from_dict(current_paper))
                title, url = _parse_heading_link(line[4:].strip())
                current_paper = {"title": _redact_secrets(title), "url": _redact_secrets(url) if url else url, "section": current_section}
                continue
            if current_paper is not None and line.startswith("- **"):
                key, value = _parse_bold_bullet(line)
                current_paper[key] = _redact_secrets(value)

    if current_paper is not None:
        papers.append(_paper_from_dict(current_paper))

    return ParsedDigest(
        date=date,
        summary=summary,
        source_warnings=warnings,
        papers=papers,
        digest_quality_warning_count=_digest_quality_count(report_dir / f"digest-quality-{date}.md"),
    )


def _date_from_title(title: str) -> str | None:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", title)
    return match.group(1) if match else None


def _parse_bold_bullet(line: str) -> tuple[str | None, str]:
    match = re.match(r"- \*\*(.+?):\*\* ?(.*)", line)
    if not match:
        return None, ""
    return match.group(1), match.group(2).strip()


def _parse_heading_link(text: str) -> tuple[str, str | None]:
    match = re.match(r"\[(.+?)\]\((.+?)\)", text)
    if match:
        return match.group(1), match.group(2)
    return text, None


def _paper_from_dict(data: dict[str, object]) -> ParsedPaper:
    relevance = str(data.get("Relevance", "unknown (0/100)"))
    decision_match = re.match(r"([a-zA-Z_-]+)\s+\((.+?)\)", relevance)
    decision = decision_match.group(1) if decision_match else relevance
    score = decision_match.group(2) if decision_match else "unknown"
    tags = [tag.strip() for tag in str(data.get("Tags", "")).split(",") if tag.strip() and tag.strip() != "untagged"]
    return ParsedPaper(
        title=str(data.get("title", "")),
        url=data.get("url") if isinstance(data.get("url"), str) else None,
        authors=str(data.get("Authors", "Unknown authors")),
        date=str(data.get("Date", "unknown")),
        source=str(data.get("Source", "unknown")),
        decision=decision,
        score=score,
        reason=str(data.get("Reason", "")),
        tags=tags,
        abstract_summary=str(data.get("Abstract summary", "")),
        section=str(data.get("section", "Maybe Relevant")),
    )


def _digest_quality_count(path: Path) -> int:
    if not path.exists():
        return 0
    match = re.search(r"Likely false positives flagged:\s*(\d+)", path.read_text(encoding="utf-8"))
    return int(match.group(1)) if match else 0


def _redact_secrets(text: str) -> str:
    patterns = [
        r"sk-[A-Za-z0-9_-]{20,}",
        r"sk-proj-[A-Za-z0-9_-]{20,}",
        r"gho_[A-Za-z0-9_]{20,}",
        r"ghp_[A-Za-z0-9_]{20,}",
        r"github_pat_[A-Za-z0-9_]{20,}",
    ]
    redacted = text
    for pattern in patterns:
        redacted = re.sub(pattern, "[REDACTED]", redacted)
    return redacted


def _date_part(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"\d{4}-\d{2}-\d{2}", value)
    return match.group(0) if match else None


def _json_list(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    return [str(item) for item in parsed] if isinstance(parsed, list) else []


def _ordered_unique(values: list[str | None]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value:
            continue
        clean = str(value).strip()
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return result


def _initial_sources(row: sqlite3.Row, sightings: list[sqlite3.Row]) -> list[str]:
    return _ordered_unique([str(row["source"])] + [str(sighting["source"]) for sighting in sightings])


def _initial_source_ids(row: sqlite3.Row, sightings: list[sqlite3.Row]) -> dict[str, list[str]]:
    source_ids: dict[str, list[str]] = {}

    def add(source: str | None, value: str | None) -> None:
        if not source or not value:
            return
        source_ids[source] = _ordered_unique([*source_ids.get(source, []), value])

    add(str(row["source"]), str(row["source_id"]) if row["source_id"] else None)
    add("arxiv", str(row["arxiv_id"]) if row["arxiv_id"] else None)
    add("semantic_scholar", str(row["semantic_scholar_id"]) if row["semantic_scholar_id"] else None)
    add("openalex", str(row["openalex_id"]) if row["openalex_id"] else None)
    for sighting in sightings:
        add(str(sighting["source"]), str(sighting["source_id"]) if sighting["source_id"] else None)
    return source_ids


def _initial_urls(row: sqlite3.Row) -> list[str]:
    urls = [str(row["url"]) if row["url"] else None]
    if row["doi"]:
        urls.append(f"https://doi.org/{row['doi']}")
    if row["arxiv_id"]:
        urls.append(f"https://arxiv.org/abs/{row['arxiv_id']}")
    if row["semantic_scholar_id"]:
        urls.append(f"https://www.semanticscholar.org/paper/{row['semantic_scholar_id']}")
    if row["openalex_id"]:
        openalex_id = str(row["openalex_id"])
        urls.append(openalex_id if openalex_id.startswith("http") else f"https://openalex.org/{openalex_id}")
    return _ordered_unique(urls)


def _normalized_title(title: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", title.lower())).strip()


def _paper_year(paper: LibraryPaper) -> str:
    date_value = paper.published_date or paper.first_seen_date
    match = re.match(r"(\d{4})", date_value or "")
    return match.group(1) if match else ""


def _merge_key(paper: LibraryPaper) -> str:
    normalized = _normalized_title(paper.title)
    if len(normalized) > 12:
        return f"title:{normalized}"
    first_author = _normalized_title(paper.authors[0]) if paper.authors else ""
    return f"title-author-year:{normalized}:{first_author}:{_paper_year(paper)}"


def _merge_dashboard_duplicates(papers: list[LibraryPaper]) -> list[LibraryPaper]:
    merged: dict[str, LibraryPaper] = {}
    for paper in papers:
        key = _merge_key(paper)
        if key not in merged:
            merged[key] = _with_aggregates(paper)
            continue
        merged[key] = _merge_two_papers(merged[key], paper)
    return sorted(
        merged.values(),
        key=lambda paper: (
            paper.published_date or paper.first_seen_date or "",
            paper.score,
            paper.title.lower(),
        ),
        reverse=True,
    )


def _sort_recommended(papers: list[LibraryPaper]) -> list[LibraryPaper]:
    return sorted(papers, key=_recommended_sort_key)


def _recommended_sort_key(paper: LibraryPaper) -> tuple[object, ...]:
    return (
        0 if paper.pinned else 1,
        0 if paper.decision == "relevant" else 1,
        -paper.score,
        1 if paper.future_date else 0,
        _reverse_date_sort_value(paper.published_date),
        _reverse_date_sort_value(paper.first_seen_date),
        paper.title.lower(),
    )


def _reverse_date_sort_value(value: str | None) -> int:
    parsed = _date_ordinal(value)
    return -parsed if parsed is not None else 0


def _date_ordinal(value: str | None) -> int | None:
    date_value = _date_part(value)
    if not date_value:
        return None
    try:
        return date.fromisoformat(date_value).toordinal()
    except ValueError:
        return None


def _is_future_date(published_date: str | None, build_date: str) -> bool:
    published = _date_ordinal(published_date)
    built = _date_ordinal(build_date)
    return bool(published is not None and built is not None and published > built)


def _apply_curation(papers: list[LibraryPaper], curation: CurationConfig, build_date: str) -> list[LibraryPaper]:
    curated: list[LibraryPaper] = []
    for paper in papers:
        if _matching_rule(paper, curation.excluded):
            continue
        pinned_rule = _matching_rule(paper, curation.pinned)
        override_rule = _matching_rule(paper, curation.overrides)
        updated = paper
        if override_rule:
            updated = _apply_override(updated, override_rule)
        if pinned_rule:
            updated = LibraryPaper(
                **{
                    **updated.__dict__,
                    "pinned": True,
                    "research_note": pinned_rule.note or updated.research_note,
                    "review_status": pinned_rule.review_status or updated.review_status,
                }
            )
        updated = LibraryPaper(
            **{
                **updated.__dict__,
                "future_date": _is_future_date(updated.published_date, build_date),
                "relevance_label": _relevance_label(updated),
            }
        )
        curated.append(updated)
    return curated


def _apply_override(paper: LibraryPaper, rule: CurationRule) -> LibraryPaper:
    decision = paper.decision
    if rule.decision:
        decision = "relevant" if rule.decision in {"highly_relevant", "relevant"} else rule.decision
    tags = _ordered_unique([*(rule.tags or []), *paper.tags]) if rule.tags else paper.tags
    return LibraryPaper(
        **{
            **paper.__dict__,
            "decision": decision,
            "score": rule.score if rule.score is not None else paper.score,
            "tags": tags,
            "research_note": rule.note or paper.research_note,
            "review_status": rule.review_status or paper.review_status,
        }
    )


def _matching_rule(paper: LibraryPaper, rules: list[CurationRule]) -> CurationRule | None:
    normalized = _normalized_title(paper.title)
    for rule in rules:
        if rule.canonical_id and rule.canonical_id == paper.canonical_id:
            return rule
        if rule.title and _normalized_title(rule.title) == normalized:
            return rule
    return None


def _load_curation(path: Path) -> CurationConfig:
    if not path.exists():
        return CurationConfig()
    sections = _parse_curation_yaml(path.read_text(encoding="utf-8"))
    return CurationConfig(
        pinned=[_curation_rule(item) for item in sections.get("pinned", [])],
        overrides=[_curation_rule(item) for item in sections.get("overrides", [])],
        excluded=[_curation_rule(item) for item in sections.get("excluded", [])],
    )


def _parse_curation_yaml(text: str) -> dict[str, list[dict[str, object]]]:
    sections: dict[str, list[dict[str, object]]] = {"pinned": [], "overrides": [], "excluded": []}
    current_section: str | None = None
    current_item: dict[str, object] | None = None
    current_list_key: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current_section = line[:-1].strip()
            sections.setdefault(current_section, [])
            current_item = None
            current_list_key = None
            continue
        if current_section not in sections:
            continue
        stripped = line.strip()
        if stripped.startswith("- ") and current_list_key and current_item is not None:
            value = _clean_yaml_value(stripped[2:])
            current_item.setdefault(current_list_key, [])
            if isinstance(current_item[current_list_key], list):
                current_item[current_list_key].append(value)  # type: ignore[index]
            continue
        if stripped.startswith("- "):
            current_item = {}
            sections[current_section].append(current_item)
            current_list_key = None
            rest = stripped[2:].strip()
            if ":" in rest:
                key, value = rest.split(":", 1)
                current_item[key.strip()] = _clean_yaml_value(value)
            continue
        if current_item is None:
            continue
        if stripped.endswith(":"):
            current_list_key = stripped[:-1].strip()
            current_item[current_list_key] = []
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            current_list_key = None
            current_item[key.strip()] = _clean_yaml_value(value)
    return sections


def _clean_yaml_value(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def _curation_rule(item: dict[str, object]) -> CurationRule:
    score_value = item.get("score")
    try:
        score = int(str(score_value)) if score_value not in {None, ""} else None
    except ValueError:
        score = None
    tags_value = item.get("tags", [])
    tags = [_redact_secrets(str(tag)) for tag in tags_value] if isinstance(tags_value, list) else []
    return CurationRule(
        title=_redact_secrets(str(item["title"])) if item.get("title") else None,
        canonical_id=_redact_secrets(str(item["canonical_id"])) if item.get("canonical_id") else None,
        note=_redact_secrets(str(item["note"])) if item.get("note") else None,
        decision=_redact_secrets(str(item["decision"])) if item.get("decision") else None,
        score=score,
        tags=tags,
        review_status=_redact_secrets(str(item["review_status"])) if item.get("review_status") else None,
        reason=_redact_secrets(str(item["reason"])) if item.get("reason") else None,
    )


def _relevance_label(paper: LibraryPaper) -> str:
    tags = set(paper.tags)
    text = " ".join([paper.title, paper.reason, paper.abstract_summary, " ".join(paper.tags)]).lower()
    if "benchmark" in tags or "evaluation" in text or "benchmark" in text:
        return "Memory benchmark/evaluation"
    if {"memory-policy", "procedural-memory"} & tags or "write" in text or "read" in text or "retrieval policy" in text or "architecture" in text:
        return "Memory architecture or policy"
    if "deep-research" in tags or "deep research" in text or "literature review" in text:
        return "Deep research agent relevance"
    if "parametric-memory" in tags or "engram" in text or "parametric" in text:
        return "Parametric/Engram-style memory"
    if paper.decision == "relevant" and ("agent-memory" in tags or "memory" in text and "agent" in text):
        return "Core agent-memory paper"
    return "Peripheral/maybe relevant"


def _with_aggregates(paper: LibraryPaper) -> LibraryPaper:
    sources = _ordered_unique([paper.source, *paper.sources])
    source_ids = _merge_source_ids(paper.source_ids, {paper.source: _ordered_unique([paper.source_id])})
    alternate_urls = _ordered_unique([paper.url, *paper.alternate_urls])
    return LibraryPaper(**{**paper.__dict__, "sources": sources, "source_ids": source_ids, "alternate_urls": alternate_urls})


def _merge_two_papers(left: LibraryPaper, right: LibraryPaper) -> LibraryPaper:
    right = _with_aggregates(right)
    best = left if left.score >= right.score else right
    sources = _ordered_unique([*left.sources, left.source, *right.sources, right.source])
    source_ids = _merge_source_ids(left.source_ids, right.source_ids)
    alternate_urls = _ordered_unique([left.url, right.url, *left.alternate_urls, *right.alternate_urls])
    tags = _ordered_unique([*left.tags, *right.tags])
    first_seen_at = _min_date_value(left.first_seen_at, right.first_seen_at)
    last_seen_at = _max_date_value(left.last_seen_at, right.last_seen_at)
    notified_at = _min_date_value(left.notified_at, right.notified_at)
    notified_date = _min_date_value(left.notified_date, right.notified_date)
    decision = "relevant" if "relevant" in {left.decision, right.decision} else best.decision
    return LibraryPaper(
        canonical_id=best.canonical_id,
        title=best.title,
        authors=best.authors or left.authors or right.authors,
        abstract_summary=best.abstract_summary,
        reason=best.reason,
        score=max(left.score, right.score),
        decision=decision,
        tags=tags,
        source=best.source,
        source_id=best.source_id,
        doi=best.doi or left.doi or right.doi,
        arxiv_id=best.arxiv_id or left.arxiv_id or right.arxiv_id,
        semantic_scholar_id=best.semantic_scholar_id or left.semantic_scholar_id or right.semantic_scholar_id,
        openalex_id=best.openalex_id or left.openalex_id or right.openalex_id,
        url=best.url or left.url or right.url or (alternate_urls[0] if alternate_urls else None),
        published_date=_max_date_value(left.published_date, right.published_date),
        first_seen_at=first_seen_at,
        last_seen_at=last_seen_at,
        notified_at=notified_at,
        notified_date=notified_date,
        appeared_in_latest_run=left.appeared_in_latest_run or right.appeared_in_latest_run,
        newly_discovered_in_latest_run=left.newly_discovered_in_latest_run or right.newly_discovered_in_latest_run,
        sources=sources,
        source_ids=source_ids,
        alternate_urls=alternate_urls,
    )


def _merge_source_ids(*groups: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {}
    for group in groups:
        for source, values in group.items():
            merged[source] = _ordered_unique([*merged.get(source, []), *values])
    return {source: values for source, values in merged.items() if values}


def _min_date_value(left: str | None, right: str | None) -> str | None:
    values = [value for value in [left, right] if value]
    return min(values) if values else None


def _max_date_value(left: str | None, right: str | None) -> str | None:
    values = [value for value in [left, right] if value]
    return max(values) if values else None


def _load_library_papers(state_path: Path) -> list[LibraryPaper]:
    if not state_path.exists():
        return []
    with sqlite3.connect(state_path) as db:
        db.row_factory = sqlite3.Row
        latest_run = db.execute("SELECT id, started_at FROM runs ORDER BY id DESC LIMIT 1").fetchone()
        latest_run_id = int(latest_run["id"]) if latest_run else None
        latest_started_at = str(latest_run["started_at"]) if latest_run else None
        latest_keys: set[str] = set()
        if latest_run_id is not None:
            latest_keys = {
                str(row["canonical_key"])
                for row in db.execute("SELECT DISTINCT canonical_key FROM sightings WHERE run_id = ?", (latest_run_id,)).fetchall()
            }
        rows = db.execute(
            """
            SELECT p.*, n.digest_date, n.notified_at
            FROM papers p
            LEFT JOIN notifications n ON n.canonical_key = p.canonical_key
            WHERE p.relevance_decision IN ('relevant', 'maybe')
            ORDER BY
              CASE WHEN p.published_date IS NULL OR p.published_date = '' THEN 1 ELSE 0 END,
              p.published_date DESC,
              p.first_seen_at DESC,
              p.relevance_score DESC
            """
        ).fetchall()
        sighting_rows = db.execute(
            "SELECT canonical_key, source, source_id FROM sightings ORDER BY id"
        ).fetchall()

    sightings_by_key: dict[str, list[sqlite3.Row]] = {}
    for sighting in sighting_rows:
        sightings_by_key.setdefault(str(sighting["canonical_key"]), []).append(sighting)
    papers: list[LibraryPaper] = []
    for row in rows:
        canonical_id = str(row["canonical_key"])
        row_sightings = sightings_by_key.get(canonical_id, [])
        first_seen_at = str(row["first_seen_at"]) if row["first_seen_at"] else None
        appeared_in_latest_run = canonical_id in latest_keys
        newly_discovered = appeared_in_latest_run and bool(latest_started_at and first_seen_at and first_seen_at >= latest_started_at)
        papers.append(
            LibraryPaper(
                canonical_id=_redact_secrets(canonical_id),
                title=_redact_secrets(str(row["title"])),
                authors=[_redact_secrets(author) for author in _json_list(row["authors_json"])],
                abstract_summary=_redact_secrets(str(row["abstract_summary"] or row["abstract"] or "")),
                reason=_redact_secrets(str(row["relevance_reason"] or "")),
                score=int(row["relevance_score"]),
                decision=str(row["relevance_decision"]),
                tags=[_redact_secrets(tag) for tag in _json_list(row["tags_json"])],
                source=str(row["source"]),
                source_id=_redact_secrets(str(row["source_id"])) if row["source_id"] else None,
                doi=_redact_secrets(str(row["doi"])) if row["doi"] else None,
                arxiv_id=_redact_secrets(str(row["arxiv_id"])) if row["arxiv_id"] else None,
                semantic_scholar_id=_redact_secrets(str(row["semantic_scholar_id"])) if row["semantic_scholar_id"] else None,
                openalex_id=_redact_secrets(str(row["openalex_id"])) if row["openalex_id"] else None,
                url=_redact_secrets(str(row["url"])) if row["url"] else None,
                published_date=str(row["published_date"]) if row["published_date"] else None,
                first_seen_at=first_seen_at,
                last_seen_at=str(row["last_seen_at"]) if row["last_seen_at"] else None,
                notified_at=str(row["notified_at"]) if row["notified_at"] else None,
                notified_date=str(row["digest_date"]) if row["digest_date"] else None,
                appeared_in_latest_run=appeared_in_latest_run,
                newly_discovered_in_latest_run=newly_discovered,
                sources=_initial_sources(row, row_sightings),
                source_ids=_initial_source_ids(row, row_sightings),
                alternate_urls=_initial_urls(row),
            )
        )
    return papers


def _library_from_digests(digests: list[ParsedDigest]) -> list[LibraryPaper]:
    papers: dict[str, LibraryPaper] = {}
    for digest in digests:
        for paper in _library_from_digest(digest, latest_run=False, newly_discovered=False):
            existing = papers.get(paper.canonical_id)
            if existing is None:
                papers[paper.canonical_id] = paper
            else:
                papers[paper.canonical_id] = LibraryPaper(
                    **{**existing.__dict__, "last_seen_at": digest.date}
                )
    if digests:
        latest_date = digests[-1].date
        latest_titles = {paper.title for paper in digests[-1].papers}
        for key, paper in list(papers.items()):
            if paper.title in latest_titles:
                papers[key] = LibraryPaper(
                    **{**paper.__dict__, "appeared_in_latest_run": True, "newly_discovered_in_latest_run": True, "last_seen_at": latest_date}
                )
    return list(papers.values())


def _library_from_digest(digest: ParsedDigest, latest_run: bool, newly_discovered: bool) -> list[LibraryPaper]:
    papers: list[LibraryPaper] = []
    for paper in digest.papers:
        score_match = re.match(r"(\d+)", paper.score)
        papers.append(
            LibraryPaper(
                canonical_id=f"digest:{digest.date}:{paper.title.lower()}",
                title=paper.title,
                authors=[author.strip() for author in paper.authors.split(",") if author.strip() and paper.authors != "Unknown authors"],
                abstract_summary=paper.abstract_summary,
                reason=paper.reason,
                score=int(score_match.group(1)) if score_match else 0,
                decision=paper.decision,
                tags=paper.tags,
                source=paper.source,
                source_id=None,
                doi=None,
                arxiv_id=None,
                semantic_scholar_id=None,
                openalex_id=None,
                url=paper.url,
                published_date=None if paper.date == "unknown" else paper.date,
                first_seen_at=digest.date,
                last_seen_at=digest.date,
                notified_at=None,
                notified_date=digest.date,
                appeared_in_latest_run=latest_run,
                newly_discovered_in_latest_run=newly_discovered,
            )
        )
    return papers


def _write_latest_markdown(digest_dir: Path, latest_date: str, latest_path: Path) -> None:
    body = latest_path.read_text(encoding="utf-8")
    latest = digest_dir / "latest.md"
    latest.write_text(
        f"# Latest Paper Scout Digest\n\nLatest daily digest: [{latest_date}]({latest_date}.md).\n\n{body}",
        encoding="utf-8",
    )


def _digest_to_json(digest: ParsedDigest) -> dict[str, object]:
    return {
        "date": digest.date,
        "summary": digest.summary,
        "source_warnings": digest.source_warnings,
        "digest_quality_warning_count": digest.digest_quality_warning_count,
        "papers": [
            {
                "title": paper.title,
                "url": paper.url,
                "authors": paper.authors,
                "date": paper.date,
                "source": paper.source,
                "decision": paper.decision,
                "score": paper.score,
                "reason": paper.reason,
                "tags": paper.tags,
                "abstract_summary": paper.abstract_summary,
                "section": paper.section,
                "citation": paper.citation,
            }
            for paper in digest.papers
        ],
    }


def _library_paper_to_json(paper: LibraryPaper) -> dict[str, object]:
    return {
        "canonical_id": paper.canonical_id,
        "title": paper.title,
        "authors": paper.authors,
        "abstract_summary": paper.abstract_summary,
        "relevance_reason": paper.reason,
        "relevance_label": paper.relevance_label or _relevance_label(paper),
        "relevance_score": paper.score,
        "relevance_decision": paper.decision,
        "tags": paper.tags,
        "source": paper.source,
        "sources": paper.sources or [paper.source],
        "source_id": paper.source_id,
        "source_ids": paper.source_ids,
        "doi": paper.doi,
        "arxiv_id": paper.arxiv_id,
        "semantic_scholar_id": paper.semantic_scholar_id,
        "openalex_id": paper.openalex_id,
        "url": paper.url,
        "alternate_urls": paper.alternate_urls,
        "publication_date": paper.published_date,
        "first_seen_date": paper.first_seen_date,
        "first_seen_at": paper.first_seen_at,
        "last_seen_date": paper.last_seen_date,
        "last_seen_at": paper.last_seen_at,
        "notified_date": paper.notified_date,
        "notified_at": paper.notified_at,
        "appeared_in_latest_run": paper.appeared_in_latest_run,
        "newly_discovered_in_latest_run": paper.newly_discovered_in_latest_run,
        "future_date": paper.future_date,
        "pinned": paper.pinned,
        "research_note": paper.research_note,
        "review_status": paper.review_status,
        "citation": paper.citation,
    }


def _latest_to_json(latest: ParsedDigest, latest_discoveries: list[LibraryPaper]) -> dict[str, object]:
    return {
        "latest_run_date": latest.date,
        "latest_run_summary": latest.summary,
        "newly_discovered_papers": [_library_paper_to_json(paper) for paper in latest_discoveries],
        "source_diagnostics": latest.source_warnings,
        "digest_quality_warning_count": latest.digest_quality_warning_count,
    }


def _render_library_page(papers: list[LibraryPaper], latest: ParsedDigest, archive: list[ParsedDigest]) -> str:
    source_buttons = sorted({source for paper in papers for source in (paper.sources or [paper.source]) if source})
    tag_options = sorted({tag for paper in papers for tag in paper.tags})
    latest_markdown_url = f"https://github.com/vernerisirva/agentmempaper/blob/main/digests/{escape(latest.date)}.md"
    recommended = _recommended_papers(papers)
    return _page(
        "Agentic Memory Paper Library",
        f"""
        <header class="briefing-hero">
          <nav class="top-nav" aria-label="Primary">
            <a class="brand" href="index.html">Paper Scout</a>
            <span class="nav-links">
              <a href="latest.html">Latest discoveries</a>
              <a href="archive.html">Archive</a>
              <a href="about.html">About</a>
              <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/latest.md">Markdown digest</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub repo</a>
            </span>
          </nav>
          <div class="hero-grid">
            <div>
              <p class="eyebrow">Paper Scout</p>
              <h1>Agentic Memory Paper Library</h1>
              <p class="hero-copy">Updated daily with new papers on agentic memory, deep research agents, and memory mechanisms.</p>
              <div class="hero-actions">
                <a class="button primary" href="#paper-library">Browse library</a>
                <a class="button secondary" href="latest.html">Latest discoveries</a>
                <a class="button secondary" href="data/papers.bib">Download BibTeX</a>
                <a class="button secondary" href="archive.html">Browse archive</a>
              </div>
            </div>
            <aside class="digest-note" aria-label="Latest digest metadata">
              <span>Latest update</span>
              <strong>{escape(latest.date)}</strong>
              <a href="{latest_markdown_url}">Open Markdown digest</a>
            </aside>
          </div>
        </header>
        <section class="paper-section recommended-section" id="recommended-reading">
          <div class="section-heading">
            <p class="section-kicker">Start here</p>
            <h2>Recommended reading</h2>
            <p>The strongest current matches, ranked by curation, relevance, score, source-date quality, and recency.</p>
          </div>
          <div class="recommended-grid">
            {_recommended_cards(recommended)}
          </div>
        </section>
        <section class="export-strip" aria-label="Export library">
          <span>Share or export the library</span>
          <a href="data/papers.csv">Download CSV</a>
          <a href="data/papers.bib">Download BibTeX</a>
          <a href="data/papers.json">Download JSON</a>
        </section>
        {_library_controls(source_buttons, tag_options)}
        {_library_summary_strip(papers, latest)}
        <section class="paper-section primary-section" id="paper-library" data-section="library">
          <div class="section-heading">
            <p class="section-kicker">Cumulative collection</p>
            <h2>Full library</h2>
            <p>The full Paper Scout library across all daily runs. Highly relevant papers rank first by default; maybe-relevant papers remain available for edge cases.</p>
          </div>
          <div class="paper-list" id="paper-list">
            {_library_paper_cards(papers)}
          </div>
        </section>
        {_warnings(latest.source_warnings)}
        <section class="archive-strip" aria-labelledby="recent-archive-heading">
          <div>
            <p class="section-kicker">Provenance</p>
            <h2 id="recent-archive-heading">Daily digests</h2>
          </div>
          <div class="archive-links">{''.join(f'<a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/{escape(item.date)}.md">{escape(item.date)}</a>' for item in reversed(archive[:8]))}</div>
        </section>
        {FILTER_SCRIPT}
        """,
    )


def _render_latest_discoveries_page(papers: list[LibraryPaper], latest: ParsedDigest, archive: list[ParsedDigest]) -> str:
    source_buttons = sorted({source for paper in papers for source in (paper.sources or [paper.source]) if source})
    tag_options = sorted({tag for paper in papers for tag in paper.tags})
    return _page(
        "Latest Paper Scout Discoveries",
        f"""
        <header class="archive-hero">
          <nav class="top-nav" aria-label="Primary">
            <a class="brand" href="index.html">Paper Scout</a>
            <span class="nav-links">
              <a href="index.html">Library</a>
              <a href="archive.html">Archive</a>
              <a href="about.html">About</a>
              <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/latest.md">Markdown digest</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub repo</a>
            </span>
          </nav>
          <p class="eyebrow">Latest update {escape(latest.date)}</p>
          <h1>Latest discoveries</h1>
          <p class="hero-copy">Papers first seen in the latest Paper Scout run. The main library remains cumulative.</p>
        </header>
        {_latest_summary_strip(papers, latest)}
        {_library_controls(source_buttons, tag_options, latest_toggle=False)}
        <section class="paper-section primary-section" id="paper-library" data-section="latest">
          <div class="section-heading">
            <p class="section-kicker">New this run</p>
            <h2>Papers first seen in the latest Paper Scout run.</h2>
          </div>
          <div class="paper-list" id="paper-list">
            {_library_paper_cards(papers)}
          </div>
        </section>
        {_warnings(latest.source_warnings)}
        <section class="archive-strip" aria-labelledby="recent-archive-heading">
          <div>
            <p class="section-kicker">Context</p>
            <h2 id="recent-archive-heading">Daily run archive</h2>
          </div>
          <div class="archive-links">{''.join(f'<a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/{escape(item.date)}.md">{escape(item.date)}</a>' for item in reversed(archive[:8]))}</div>
        </section>
        {FILTER_SCRIPT}
        """,
    )


def _render_archive_page(archive: list[ParsedDigest]) -> str:
    rows = "\n".join(
        f"""
        <article class="archive-entry">
          <div>
            <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/{escape(item.date)}.md">{escape(item.date)}</a>
            <p>{escape(item.summary.get('Candidates fetched', '0'))} candidates fetched · {escape(item.summary.get('New unique papers', '0'))} new unique papers</p>
          </div>
          <dl>
            <div><dt>Highly relevant</dt><dd>{_section_count(item, 'Highly Relevant')}</dd></div>
            <div><dt>Maybe relevant</dt><dd>{_section_count(item, 'Maybe Relevant')}</dd></div>
            <div><dt>Warnings</dt><dd>{len(item.source_warnings)}</dd></div>
          </dl>
        </article>
        """
        for item in reversed(archive)
    )
    return _page(
        "Paper Scout Archive",
        f"""
        <header class="archive-hero">
          <nav class="top-nav" aria-label="Primary">
            <a class="brand" href="index.html">Paper Scout</a>
            <span class="nav-links">
              <a href="index.html">Library</a>
              <a href="latest.html">Latest discoveries</a>
              <a href="about.html">About</a>
              <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/latest.md">Latest Markdown</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub repo</a>
            </span>
          </nav>
          <p class="eyebrow">Paper Scout provenance</p>
          <h1>Daily run archive</h1>
          <p class="hero-copy">The main library is cumulative; daily digests are kept for provenance and for seeing what changed on a specific day.</p>
        </header>
        <section class="archive-list" aria-label="Digest archive">{rows}</section>
        """,
    )


def _render_about_page() -> str:
    return _page(
        "About Paper Scout",
        """
        <header class="archive-hero">
          <nav class="top-nav" aria-label="Primary">
            <a class="brand" href="index.html">Paper Scout</a>
            <span class="nav-links">
              <a href="index.html">Library</a>
              <a href="latest.html">Latest discoveries</a>
              <a href="archive.html">Archive</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub repo</a>
            </span>
          </nav>
          <p class="eyebrow">About</p>
          <h1>How Paper Scout works</h1>
          <p class="hero-copy">A static daily research monitor for papers around agentic memory, LLM agent memory, deep research agents, and memory mechanisms.</p>
        </header>
        <section class="about-grid">
          <article>
            <h2>What Paper Scout tracks</h2>
            <p>Paper Scout watches for work on agentic memory, LLM agent memory, long-term, episodic, semantic, and procedural memory, memory benchmarks, deep research agents, and Engram-style or parametric memory mechanisms.</p>
          </article>
          <article>
            <h2>Sources</h2>
            <p>The daily scout queries arXiv, OpenAlex, and Semantic Scholar. Source metadata can disagree, lag, or contain future publication dates from publisher feeds.</p>
          </article>
          <article>
            <h2>Deduplication</h2>
            <p>Candidate papers are canonicalized by DOI, arXiv ID, Semantic Scholar ID, OpenAlex work ID, then normalized title, first author, and year. The dashboard also collapses duplicate titles while preserving alternate source links.</p>
          </article>
          <article>
            <h2>Relevance scoring</h2>
            <p>The scout uses deterministic filters and optional LLM classification. Highly relevant means the paper directly supports agent-memory research; maybe relevant means it may be useful but needs human judgment.</p>
          </article>
          <article>
            <h2>Manual curation</h2>
            <p>Optional curation can pin, annotate, override, or hide papers in the static dashboard without deleting anything from SQLite state.</p>
          </article>
          <article>
            <h2>Limitations</h2>
            <p>Relevance scoring can produce false positives or false negatives. Semantic Scholar rate limits may occur. Source metadata can be wrong, and future publication dates may reflect source metadata rather than actual availability.</p>
          </article>
        </section>
        """,
    )


def _page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="Daily Paper Scout briefing for agentic memory, deep research agents, and memory mechanisms.">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <main class="page" id="main-content">
    {body}
  </main>
</body>
</html>
"""


def _summary_strip(digest: ParsedDigest) -> str:
    cells = [
        ("Candidates fetched", digest.summary.get("Candidates fetched", "0")),
        ("New unique papers", digest.summary.get("New unique papers", "0")),
        ("Highly relevant", digest.summary.get("Relevant", "0")),
        ("Maybe relevant", digest.summary.get("Maybe relevant", "0")),
        ("Digest-quality warnings", str(digest.digest_quality_warning_count)),
    ]
    metric_cells = "".join(f"<div><span>{escape(label)}</span><strong>{escape(value)}</strong></div>" for label, value in cells)
    return f"""
    <section class="summary-strip" aria-label="Run summary metrics">
      {metric_cells}
      <div class="source-summary"><span>Source summary</span><strong>{escape(digest.summary.get("Source summary", "none"))}</strong></div>
    </section>
    """


def _library_summary_strip(papers: list[LibraryPaper], latest: ParsedDigest) -> str:
    highly = sum(1 for paper in papers if paper.decision == "relevant")
    maybe = sum(1 for paper in papers if paper.decision == "maybe")
    latest_count = sum(1 for paper in papers if paper.newly_discovered_in_latest_run)
    cells = [
        ("Total known papers", str(len(papers))),
        ("New in latest run", str(latest_count)),
        ("Highly relevant", str(highly)),
        ("Maybe relevant", str(maybe)),
        ("Latest update date", latest.date),
        ("Source warning count", str(len(latest.source_warnings))),
    ]
    metric_cells = "".join(f"<div><span>{escape(label)}</span><strong>{escape(value)}</strong></div>" for label, value in cells)
    return f"""
    <section class="summary-strip library-summary" aria-label="Library summary metrics">
      {metric_cells}
    </section>
    """


def _latest_summary_strip(papers: list[LibraryPaper], latest: ParsedDigest) -> str:
    cells = [
        ("Latest update date", latest.date),
        ("New in latest run", str(len(papers))),
        ("Highly relevant", str(sum(1 for paper in papers if paper.decision == "relevant"))),
        ("Maybe relevant", str(sum(1 for paper in papers if paper.decision == "maybe"))),
        ("Source warning count", str(len(latest.source_warnings))),
    ]
    metric_cells = "".join(f"<div><span>{escape(label)}</span><strong>{escape(value)}</strong></div>" for label, value in cells)
    return f"""
    <section class="summary-strip" aria-label="Latest run summary metrics">
      {metric_cells}
      <div class="source-summary"><span>Run summary</span><strong>{escape(latest.summary.get("Source summary", "none"))}</strong></div>
    </section>
    """


def _controls(sources: list[str]) -> str:
    source_buttons = "".join(f'<button data-source="{escape(source)}">{escape(source)}</button>' for source in sources)
    return f"""
    <section class="reading-controls" aria-label="Reading controls">
      <label class="search-field" for="paper-search">
        <span>Search papers</span>
        <input id="paper-search" type="search" placeholder="Search title, abstract, tags">
      </label>
      <div class="control-group">
        <span>Relevance</span>
        <div class="segmented" id="relevance-filters">
          <button data-decision="all" class="active">All</button>
          <button data-decision="relevant">Highly relevant</button>
          <button data-decision="maybe">Maybe relevant</button>
        </div>
      </div>
      <label class="high-toggle">
        <input id="high-only" type="checkbox">
        <span>Show only highly relevant</span>
      </label>
      <div class="control-group sources">
        <span>Source</span>
        <div class="source-buttons" id="source-filters">
          <button data-source="all" class="active">All sources</button>
          {source_buttons}
        </div>
      </div>
    </section>
    """


def _library_controls(sources: list[str], tags: list[str], latest_toggle: bool = True) -> str:
    source_buttons = "".join(f'<button data-source="{escape(source)}">{escape(_source_label(source))}</button>' for source in sources)
    tag_options = "".join(f'<option value="{escape(tag)}">{escape(tag)}</option>' for tag in tags)
    latest_toggle_markup = (
        """
      <label class="toggle-control">
        <input id="latest-only" type="checkbox">
        <span>Latest-run only</span>
      </label>
        """
        if latest_toggle
        else ""
    )
    return f"""
    <section class="reading-controls library-controls" aria-label="Library controls">
      <label class="search-field" for="paper-search">
        <span>Search papers</span>
        <input id="paper-search" type="search" placeholder="Search title, authors, summary, tags">
      </label>
      <label class="select-field" for="paper-sort">
        <span>Sort library</span>
        <select id="paper-sort">
          <option value="recommended" selected>Recommended</option>
          <option value="score-desc">Relevance score, highest first</option>
          <option value="published-desc">Publication date, newest first</option>
          <option value="published-asc">Publication date, oldest first</option>
          <option value="first-seen-desc">First seen date, newest first</option>
          <option value="title-asc">Title A-Z</option>
          <option value="source-asc">Source</option>
        </select>
      </label>
      <div class="control-group">
        <span>Relevance</span>
        <div class="segmented" id="relevance-filters">
          <button data-decision="all" class="active">All</button>
          <button data-decision="relevant">Highly relevant</button>
          <button data-decision="maybe">Maybe relevant</button>
        </div>
      </div>
      {latest_toggle_markup}
      <label class="select-field tag-filter" for="tag-filter">
        <span>Tag</span>
        <select id="tag-filter">
          <option value="all">All tags</option>
          {tag_options}
        </select>
      </label>
      <div class="control-group sources">
        <span>Source</span>
        <div class="source-buttons" id="source-filters">
          <button data-source="all" class="active">All sources</button>
          {source_buttons}
        </div>
      </div>
    </section>
    """


def _warnings(warnings: list[str]) -> str:
    if not warnings:
        return '<details class="source-diagnostics"><summary>Source diagnostics <span>0 warnings</span></summary><p>No source warnings.</p></details>'
    compact = "\n".join(f"<li>{escape(warning)}</li>" for warning in warnings)
    return f'<details class="source-diagnostics"><summary>Source diagnostics <span>{len(warnings)} warnings</span></summary><ul>{compact}</ul></details>'


def _recommended_papers(papers: list[LibraryPaper], limit: int = 8) -> list[LibraryPaper]:
    highly = [paper for paper in papers if paper.pinned or paper.decision == "relevant"]
    pool = highly if len(highly) >= min(limit, 5) else papers
    return _sort_recommended(pool)[:limit]


def _recommended_cards(papers: list[LibraryPaper]) -> str:
    if not papers:
        return '<p class="empty">No recommended papers yet.</p>'
    return "\n".join(_recommended_card(paper) for paper in papers)


def _recommended_card(paper: LibraryPaper) -> str:
    tags = "".join(f'<span class="badge tag">{escape(tag)}</span>' for tag in paper.tags[:4])
    sources = paper.sources or [paper.source]
    source_badges = "".join(f'<span class="badge source">{escape(_source_label(source))}</span>' for source in sources)
    link = f'<a class="paper-link" href="{escape(paper.url)}">Open paper</a>' if paper.url else '<span class="paper-link disabled">No link available</span>'
    pinned = '<span class="badge pinned">Pinned</span>' if paper.pinned else ""
    status = f'<span class="badge review">{escape(paper.review_status)}</span>' if paper.review_status else ""
    return f"""
    <article class="recommended-card">
      <div class="paper-kicker">{source_badges}<span class="badge relevance">{escape(_decision_label(paper.decision))} · {paper.score}/100</span>{pinned}{status}</div>
      <h3>{escape(paper.title)}</h3>
      <p class="meta">{escape(paper.authors_text)} · {_published_text(paper)}</p>
      <p class="relevance-label">{escape(paper.relevance_label or _relevance_label(paper))}</p>
      <p class="reason">{escape(_short_reason(paper))}</p>
      <div class="tags">{tags}</div>
      {link}
    </article>
    """


def _library_paper_cards(papers: list[LibraryPaper]) -> str:
    if not papers:
        return '<p class="empty">No papers in this section.</p>'
    return "\n".join(_library_paper_card(paper) for paper in papers)


def _library_paper_card(paper: LibraryPaper) -> str:
    tags = "".join(f'<span class="badge tag">{escape(tag)}</span>' for tag in paper.tags) or '<span class="badge tag">untagged</span>'
    sources = paper.sources or [paper.source]
    source_badges = "".join(f'<span class="badge source">{escape(_source_label(source))}</span>' for source in sources)
    link = f'<a class="paper-link" href="{escape(paper.url)}">Open paper</a>' if paper.url else '<span class="paper-link disabled">No link available</span>'
    secondary_links = _secondary_links(paper)
    published = _published_text(paper)
    search_text = " ".join([paper.title, paper.authors_text, paper.abstract_summary, paper.reason, paper.research_note or "", paper.relevance_label or "", " ".join(paper.tags), " ".join(sources), paper.decision]).lower()
    tag_text = " ".join(paper.tags)
    source_text = " ".join(sources)
    density = "primary" if paper.decision == "relevant" else "compact"
    pinned = '<span class="badge pinned">Pinned</span>' if paper.pinned else ""
    status = f'<span class="badge review">{escape(paper.review_status)}</span>' if paper.review_status else ""
    note = f'<p class="research-note"><strong>Research note</strong> {escape(paper.research_note)}</p>' if paper.research_note else ""
    relevance_label = paper.relevance_label or _relevance_label(paper)
    return f"""
    <article class="paper-card {escape(density)}" data-source="{escape(paper.source)}" data-sources="{escape(source_text)}" data-decision="{escape(paper.decision)}" data-tags="{escape(tag_text)}" data-latest-run="{str(paper.newly_discovered_in_latest_run).lower()}" data-published="{escape(paper.published_date or '')}" data-first-seen="{escape(paper.first_seen_date)}" data-score="{paper.score}" data-pinned="{str(paper.pinned).lower()}" data-future-date="{str(paper.future_date).lower()}" data-title="{escape(paper.title.lower())}" data-search="{escape(search_text)}">
      <div class="paper-main">
        <div class="paper-kicker">
          {source_badges}
          <span class="badge relevance">{escape(_decision_label(paper.decision))} · {paper.score}/100</span>
          {('<span class="badge latest">latest run</span>' if paper.newly_discovered_in_latest_run else '')}
          {pinned}
          {status}
        </div>
        <h3>{escape(paper.title)}</h3>
        <p class="meta">{escape(paper.authors_text)}</p>
        <dl class="paper-dates">
          <div><dt>Published</dt><dd>{escape(published)}</dd></div>
          <div><dt>First seen by Paper Scout</dt><dd>{escape(paper.first_seen_date)}</dd></div>
        </dl>
        <p class="relevance-label">{escape(relevance_label)}</p>
        <p class="reason">{escape(_short_reason(paper))}</p>
        {note}
        <p class="abstract-summary">{escape(paper.abstract_summary)}</p>
        <div class="tags">{tags}</div>
      </div>
      <div class="paper-side">
        {link}
        {secondary_links}
        <button class="citation-button" type="button" data-citation="{escape(paper.citation)}">Copy citation</button>
        <span class="copy-status" aria-live="polite"></span>
      </div>
    </article>
    """


def _secondary_links(paper: LibraryPaper) -> str:
    primary = paper.url
    links: list[tuple[str, str]] = []
    for url in paper.alternate_urls:
        if not url or url == primary:
            continue
        label = _url_label(url)
        if (label, url) not in links:
            links.append((label, url))
    if not links:
        return ""
    rendered = "".join(f'<a href="{escape(url)}">{escape(label)}</a>' for label, url in links[:4])
    return f'<div class="secondary-links">{rendered}</div>'


def _url_label(url: str) -> str:
    if "doi.org" in url:
        return "DOI"
    if "arxiv.org" in url:
        return "arXiv"
    if "semanticscholar.org" in url:
        return "Semantic Scholar"
    if "openalex.org" in url:
        return "OpenAlex"
    return "Alternate link"


def _paper_cards(papers: list[ParsedPaper], density: str) -> str:
    if not papers:
        return '<p class="empty">No papers in this section.</p>'
    return "\n".join(_paper_card(paper, density) for paper in papers)


def _paper_card(paper: ParsedPaper, density: str) -> str:
    tags = "".join(f'<span class="badge tag">{escape(tag)}</span>' for tag in paper.tags) or '<span class="badge tag">untagged</span>'
    link = f'<a class="paper-link" href="{escape(paper.url)}">Open paper</a>' if paper.url else '<span class="paper-link disabled">No link available</span>'
    search_text = " ".join([paper.title, paper.abstract_summary, " ".join(paper.tags), paper.source, paper.decision]).lower()
    return f"""
    <article class="paper-card {escape(density)}" data-source="{escape(paper.source)}" data-decision="{escape(paper.decision)}" data-search="{escape(search_text)}">
      <div class="paper-main">
        <div class="paper-kicker">
          <span class="badge source">{escape(paper.source)}</span>
          <span class="badge relevance">{escape(paper.decision)} · {escape(paper.score)}</span>
        </div>
        <h3>{escape(paper.title)}</h3>
        <p class="meta">{escape(paper.authors)} · {escape(paper.date)}</p>
        <p class="reason">{escape(paper.reason)}</p>
        <p class="abstract-summary">{escape(paper.abstract_summary)}</p>
        <div class="tags">{tags}</div>
      </div>
      <div class="paper-side">
        {link}
        <details class="citation"><summary>Copy citation</summary><textarea readonly>{escape(paper.citation)}</textarea></details>
      </div>
    </article>
    """


def _section_count(digest: ParsedDigest, section: str) -> int:
    return sum(1 for paper in digest.papers if paper.section == section)


def _source_label(source: str) -> str:
    labels = {
        "arxiv": "arXiv",
        "openalex": "OpenAlex",
        "semantic_scholar": "Semantic Scholar",
    }
    return labels.get(source, source)


def _decision_label(decision: str) -> str:
    return "Highly relevant" if decision == "relevant" else "Maybe relevant" if decision == "maybe" else decision


def _published_text(paper: LibraryPaper) -> str:
    if not paper.published_date:
        return "unknown"
    if paper.future_date:
        return f"Published: {paper.published_date} · source date"
    return paper.published_date


def _short_reason(paper: LibraryPaper) -> str:
    reason = paper.reason.strip() or (paper.relevance_label or _relevance_label(paper))
    sentence = re.split(r"(?<=[.!?])\s+", reason, maxsplit=1)[0].strip()
    return sentence if sentence else reason


def _papers_csv(papers: list[LibraryPaper]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "title",
            "authors",
            "publication_date",
            "first_seen_date",
            "relevance_decision",
            "relevance_score",
            "tags",
            "sources",
            "url",
            "doi",
            "arxiv_id",
        ],
    )
    writer.writeheader()
    for paper in papers:
        writer.writerow(
            {
                "title": paper.title,
                "authors": paper.authors_text,
                "publication_date": paper.published_date or "",
                "first_seen_date": paper.first_seen_date,
                "relevance_decision": paper.decision,
                "relevance_score": paper.score,
                "tags": "; ".join(paper.tags),
                "sources": "; ".join(paper.sources or [paper.source]),
                "url": paper.url or "",
                "doi": paper.doi or "",
                "arxiv_id": paper.arxiv_id or "",
            }
        )
    return output.getvalue()


def _papers_bibtex(papers: list[LibraryPaper]) -> str:
    entries = [_paper_bibtex(paper) for paper in papers]
    return "\n\n".join(entries) + ("\n" if entries else "")


def _paper_bibtex(paper: LibraryPaper) -> str:
    year = _paper_year(paper) or _paper_year(LibraryPaper(**{**paper.__dict__, "published_date": paper.first_seen_date}))
    key = _bibtex_key(paper, year)
    fields = [
        ("title", paper.title),
        ("author", " and ".join(paper.authors) if paper.authors else ""),
        ("year", year),
        ("url", paper.url or ""),
        ("doi", paper.doi or ""),
        ("eprint", paper.arxiv_id or ""),
        ("note", f"Paper Scout relevance: {_decision_label(paper.decision)} ({paper.score}/100)"),
    ]
    rendered = [f"  {name} = {{{_bibtex_escape(value)}}}" for name, value in fields if value]
    return "@misc{" + key + ",\n" + ",\n".join(rendered) + "\n}"


def _bibtex_key(paper: LibraryPaper, year: str) -> str:
    first = _normalized_title(paper.authors[0]).split(" ")[-1] if paper.authors else "paper"
    title_word = _normalized_title(paper.title).split(" ")[0] if _normalized_title(paper.title) else "memory"
    return re.sub(r"[^A-Za-z0-9_:-]", "", f"{first}{year or 'n.d.'}{title_word}")


def _bibtex_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


STYLE_CSS = """
:root {
  color-scheme: light;
  --bg: #f4f1ea;
  --paper: #fffdf8;
  --paper-soft: #fbf7ef;
  --text: #191816;
  --muted: #676059;
  --faint: #8b8176;
  --line: #ddd4c8;
  --line-strong: #c8b9a8;
  --accent: #27615d;
  --accent-dark: #174744;
  --amber: #8a5a17;
  --shadow: rgba(64, 48, 32, .09);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background:
    radial-gradient(circle at top left, rgba(39, 97, 93, .09), transparent 28rem),
    linear-gradient(180deg, #f8f5ee 0%, var(--bg) 34rem);
  color: var(--text);
  font: 16px/1.62 ui-serif, Georgia, Cambria, "Times New Roman", serif;
  text-rendering: optimizeLegibility;
}
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: .16;
  background-image: radial-gradient(rgba(25, 24, 22, .16) .55px, transparent .55px);
  background-size: 8px 8px;
}
a { color: var(--accent-dark); text-decoration-thickness: .08em; text-underline-offset: .18em; }
a:hover { color: var(--accent); }
button, input, textarea, select { font: inherit; }
button, a, input, summary, textarea, select { transition: background-color .2s ease, border-color .2s ease, color .2s ease, box-shadow .2s ease, transform .2s ease; }
button:focus-visible, a:focus-visible, input:focus-visible, summary:focus-visible, textarea:focus-visible, select:focus-visible {
  outline: 3px solid rgba(39, 97, 93, .28);
  outline-offset: 3px;
}
.skip-link {
  position: absolute;
  left: 1rem;
  top: .75rem;
  z-index: 2;
  transform: translateY(-160%);
  background: var(--text);
  color: var(--paper);
  padding: .55rem .8rem;
  border-radius: .45rem;
}
.skip-link:focus { transform: translateY(0); }
.page { width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 30px 0 64px; }
.top-nav {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
  padding-bottom: 2.25rem;
}
.brand {
  color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-weight: 760;
  text-decoration: none;
}
.nav-links { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: flex-end; }
.nav-links a {
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .93rem;
  font-weight: 600;
  text-decoration: none;
}
.nav-links a:hover { color: var(--accent-dark); }
.briefing-hero, .archive-hero { padding: 1rem 0 2rem; }
.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(220px, 310px);
  gap: clamp(1.5rem, 4vw, 4rem);
  align-items: end;
}
.eyebrow, .section-kicker, .summary-strip span, .control-group > span, .search-field span, .select-field span {
  margin: 0;
  color: var(--accent-dark);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .72rem;
  font-weight: 760;
  letter-spacing: .13em;
  text-transform: uppercase;
}
h1, h2, h3 { margin: 0; text-wrap: balance; }
h1 {
  max-width: 11ch;
  font-size: clamp(4rem, 14vw, 9.5rem);
  line-height: .82;
  letter-spacing: -.055em;
}
.archive-hero h1 { max-width: 12ch; font-size: clamp(3.4rem, 11vw, 7rem); }
h2 { font-size: clamp(1.95rem, 4vw, 3.2rem); line-height: .95; letter-spacing: -.035em; }
h3 { font-size: clamp(1.35rem, 2vw, 1.95rem); line-height: 1.12; letter-spacing: -.018em; }
.hero-copy {
  max-width: 34rem;
  margin: 1.35rem 0 0;
  color: var(--muted);
  font-size: clamp(1.1rem, 2vw, 1.35rem);
  line-height: 1.5;
  text-wrap: pretty;
}
.hero-actions { display: flex; flex-wrap: wrap; gap: .7rem; margin-top: 1.55rem; }
.button, .paper-link, .citation-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.65rem;
  border-radius: .55rem;
  padding: .72rem 1rem;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .94rem;
  font-weight: 720;
  text-decoration: none;
}
.button.primary, .paper-link {
  background: var(--accent-dark);
  color: #fffdf7;
  box-shadow: 0 12px 28px rgba(23, 71, 68, .18);
}
.button.secondary {
  background: rgba(255, 253, 248, .72);
  border: 1px solid var(--line);
  color: var(--accent-dark);
}
.button:hover, .paper-link:hover { transform: translateY(-1px); }
.button:active, .paper-link:active, button:active { transform: translateY(1px); }
.digest-note {
  background: rgba(255, 253, 248, .76);
  border: 1px solid rgba(200, 185, 168, .76);
  border-radius: .9rem;
  box-shadow: 0 22px 60px var(--shadow);
  padding: 1.15rem;
}
.digest-note span, .digest-note a {
  display: block;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.digest-note span { color: var(--faint); font-size: .82rem; font-weight: 650; }
.digest-note strong {
  display: block;
  margin: .2rem 0 .75rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 1.7rem;
  font-variant-numeric: tabular-nums;
}
.recommended-section {
  margin-top: 1.5rem;
  padding: 1.35rem;
  background: rgba(255, 253, 248, .54);
  border: 1px solid var(--line);
  border-radius: 1rem;
}
.recommended-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
  gap: .9rem;
}
.recommended-card {
  display: flex;
  flex-direction: column;
  gap: .7rem;
  min-height: 100%;
  padding: 1rem;
  background: var(--paper);
  border: 1px solid var(--line);
  border-top: 4px solid var(--accent-dark);
  border-radius: .75rem;
  box-shadow: 0 16px 34px rgba(64, 48, 32, .055);
}
.recommended-card h3 {
  margin: .1rem 0 0;
  font-size: clamp(1.18rem, 1.7vw, 1.55rem);
}
.recommended-card .paper-link { margin-top: auto; }
.recommended-card .reason {
  margin: 0;
  padding: .65rem .75rem;
}
.export-strip {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: .55rem;
  margin: 1.2rem 0;
  padding: .75rem .9rem;
  border: 1px solid var(--line);
  border-radius: .75rem;
  background: rgba(255, 253, 248, .62);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.export-strip span {
  color: var(--muted);
  font-weight: 720;
  margin-right: .25rem;
}
.export-strip a {
  padding: .38rem .58rem;
  border: 1px solid var(--line);
  border-radius: .42rem;
  color: var(--accent-dark);
  text-decoration: none;
  font-size: .88rem;
  font-weight: 700;
}
.summary-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(7rem, 1fr));
  gap: 0;
  margin: 1.5rem 0 1.25rem;
  background: rgba(255, 253, 248, .82);
  border: 1px solid var(--line);
  border-radius: .85rem;
  overflow: hidden;
  box-shadow: 0 18px 42px rgba(64, 48, 32, .06);
}
.summary-strip div { padding: .95rem 1rem; border-left: 1px solid var(--line); }
.summary-strip div:first-child { border-left: 0; }
.summary-strip strong {
  display: block;
  margin-top: .15rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 1.15rem;
  font-variant-numeric: tabular-nums;
}
.summary-strip .source-summary {
  grid-column: 1 / -1;
  border-left: 0;
  border-top: 1px solid var(--line);
}
.summary-strip .source-summary strong {
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .98rem;
  font-weight: 650;
}
.reading-controls {
  display: grid;
  grid-template-columns: minmax(18rem, 1.35fr) minmax(15rem, .9fr) minmax(15rem, 1fr) auto;
  gap: .9rem;
  align-items: end;
  margin: 1.4rem 0 2.6rem;
  padding: .95rem;
  background: rgba(248, 245, 238, .8);
  border: 1px solid var(--line);
  border-radius: .85rem;
}
.search-field, .select-field, .control-group { display: grid; gap: .45rem; }
input[type="search"], select {
  width: 100%;
  min-height: 2.75rem;
  border: 1px solid var(--line-strong);
  border-radius: .55rem;
  background: var(--paper);
  color: var(--text);
  padding: .7rem .85rem;
}
input[type="search"]::placeholder { color: var(--faint); }
.segmented, .source-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: .35rem;
}
button {
  border: 1px solid var(--line);
  background: rgba(255, 253, 248, .72);
  color: var(--muted);
  border-radius: .48rem;
  padding: .58rem .72rem;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .88rem;
  font-weight: 650;
  cursor: pointer;
}
button:hover { border-color: var(--line-strong); color: var(--text); background: var(--paper); }
button.active { background: var(--accent-dark); border-color: var(--accent-dark); color: #fffdf7; }
.toggle-control {
  display: inline-flex;
  gap: .55rem;
  align-items: center;
  min-height: 2.75rem;
  padding: .58rem .72rem;
  border: 1px solid var(--line);
  border-radius: .55rem;
  background: rgba(255, 253, 248, .66);
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .88rem;
  font-weight: 650;
}
.toggle-control input { accent-color: var(--accent-dark); }
.tag-filter { min-width: 12rem; }
.sources { grid-column: 1 / -1; }
.paper-section { margin-top: 2.5rem; }
.section-heading {
  max-width: 44rem;
  margin-bottom: 1.05rem;
}
.section-heading p:not(.section-kicker) {
  margin: .7rem 0 0;
  color: var(--muted);
  font-size: 1.03rem;
}
.paper-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(11rem, 14rem);
  gap: clamp(1rem, 3vw, 2rem);
  margin: 1rem 0;
  padding: clamp(1.1rem, 3vw, 1.65rem);
  background: var(--paper);
  border-top: 1px solid var(--line-strong);
  border-radius: .75rem;
  box-shadow: 0 18px 46px rgba(64, 48, 32, .055);
}
.paper-card.primary { border-top: 4px solid var(--accent-dark); }
.paper-card.compact {
  background: rgba(255, 253, 248, .68);
  box-shadow: none;
  border-top-color: rgba(200, 185, 168, .72);
  padding-top: 1rem;
  padding-bottom: 1rem;
}
.paper-card.compact h3 {
  font-size: clamp(1.15rem, 1.6vw, 1.45rem);
}
.paper-kicker, .tags { display: flex; gap: .45rem; flex-wrap: wrap; align-items: center; }
.paper-card h3 { margin-top: .7rem; }
.meta, .empty {
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.meta { margin: .55rem 0 0; font-size: .95rem; }
.paper-dates {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, max-content));
  gap: .6rem 1rem;
  margin: .85rem 0 0;
}
.paper-dates div {
  padding: .55rem .65rem;
  background: var(--paper-soft);
  border: 1px solid var(--line);
  border-radius: .48rem;
}
.paper-dates dt {
  color: var(--faint);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .72rem;
  font-weight: 720;
}
.paper-dates dd {
  margin: .12rem 0 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: .9rem;
  font-weight: 720;
  font-variant-numeric: tabular-nums;
}
.reason {
  margin: 1rem 0 0;
  padding: .85rem .95rem;
  border-left: 3px solid rgba(39, 97, 93, .45);
  background: #f3f8f6;
  color: #244c49;
  border-radius: .35rem .55rem .55rem .35rem;
  font-weight: 600;
}
.relevance-label {
  display: inline-flex;
  width: fit-content;
  margin: .9rem 0 0;
  padding: .28rem .5rem;
  border-radius: .35rem;
  background: #e9f2f0;
  color: var(--accent-dark);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .82rem;
  font-weight: 760;
}
.research-note {
  margin: .85rem 0 0;
  padding: .75rem .85rem;
  border: 1px dashed var(--line-strong);
  border-radius: .55rem;
  background: rgba(255, 253, 248, .74);
  color: var(--muted);
}
.research-note strong {
  display: block;
  color: var(--accent-dark);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .78rem;
  text-transform: uppercase;
  letter-spacing: .08em;
}
.abstract-summary {
  max-width: 67ch;
  margin: .95rem 0 0;
  color: #3d3934;
  text-wrap: pretty;
}
.badge {
  display: inline-flex;
  align-items: center;
  border-radius: .35rem;
  padding: .2rem .5rem;
  border: 1px solid var(--line);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .76rem;
  font-weight: 760;
}
.source { background: #e7f0ee; color: var(--accent-dark); border-color: #c9dfdc; }
.relevance { background: #fff1d8; color: var(--amber); border-color: #ecd6ad; }
.latest { background: #edf1df; color: #586723; border-color: #d7dfb5; }
.pinned { background: #efe8d8; color: #5f4520; border-color: #dac7a3; }
.review { background: #ece7f0; color: #554361; border-color: #d8cddf; }
.tag { background: #f2eee7; color: #574f47; }
.tags { margin-top: .95rem; }
.paper-side {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: .75rem;
}
.paper-link.disabled {
  background: #eee7dc;
  color: var(--faint);
  box-shadow: none;
}
.secondary-links {
  display: flex;
  flex-wrap: wrap;
  gap: .45rem;
}
.secondary-links a {
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: .35rem .55rem;
  border: 1px solid var(--line);
  border-radius: .4rem;
  background: rgba(255, 253, 248, .72);
  color: var(--accent-dark);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .82rem;
  font-weight: 700;
  text-decoration: none;
}
.citation-button {
  border: 1px solid var(--line-strong);
  background: var(--paper-soft);
  color: var(--accent-dark);
  cursor: pointer;
}
.citation-button:hover {
  background: var(--paper);
  border-color: var(--accent);
}
.copy-status {
  min-height: 1.2rem;
  color: var(--faint);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .78rem;
}
.citation summary {
  cursor: pointer;
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .88rem;
  font-weight: 650;
}
textarea {
  width: 100%;
  min-height: 6rem;
  margin-top: .55rem;
  border: 1px solid var(--line);
  border-radius: .55rem;
  background: var(--paper-soft);
  color: var(--text);
  padding: .7rem;
  resize: vertical;
}
.source-diagnostics {
  margin: 2.6rem 0 0;
  padding: .9rem 1rem;
  background: rgba(255, 253, 248, .58);
  border: 1px solid var(--line);
  border-radius: .65rem;
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.source-diagnostics summary {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  font-weight: 720;
  color: var(--text);
}
.source-diagnostics summary span {
  color: var(--faint);
  font-size: .9rem;
  font-weight: 650;
}
.source-diagnostics ul {
  max-height: 13rem;
  overflow: auto;
  margin: .85rem 0 0;
  padding-left: 1.1rem;
}
.archive-strip {
  display: grid;
  grid-template-columns: minmax(10rem, 16rem) 1fr;
  gap: 1.5rem;
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--line);
}
.archive-strip h2 { font-size: 2rem; }
.archive-links {
  display: flex;
  flex-wrap: wrap;
  gap: .55rem;
  align-content: start;
}
.archive-links a {
  padding: .45rem .6rem;
  border: 1px solid var(--line);
  border-radius: .45rem;
  background: rgba(255, 253, 248, .6);
  color: var(--accent-dark);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: .88rem;
  text-decoration: none;
}
.archive-list {
  display: grid;
  gap: .85rem;
  margin-top: 1.6rem;
}
.archive-entry {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(18rem, 28rem);
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 253, 248, .72);
  border: 1px solid var(--line);
  border-radius: .75rem;
}
.archive-entry a {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 1.1rem;
  font-weight: 760;
  text-decoration: none;
}
.archive-entry p {
  margin: .35rem 0 0;
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.archive-entry dl {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: .55rem;
  margin: 0;
}
.archive-entry dl div {
  padding: .65rem;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: .5rem;
}
.archive-entry dt {
  color: var(--faint);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .75rem;
  font-weight: 720;
}
.archive-entry dd {
  margin: .15rem 0 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 1.2rem;
  font-weight: 760;
}
.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
  gap: 1rem;
  margin-top: 1.6rem;
}
.about-grid article {
  padding: 1.15rem;
  background: rgba(255, 253, 248, .72);
  border: 1px solid var(--line);
  border-radius: .75rem;
}
.about-grid h2 {
  font-size: clamp(1.45rem, 3vw, 2.1rem);
}
.about-grid p {
  margin: .75rem 0 0;
  color: var(--muted);
  text-wrap: pretty;
}
[hidden] { display: none !important; }
@media (max-width: 640px) {
  .page { width: min(100% - 22px, 1180px); padding-top: 18px; }
  .top-nav, .hero-grid, .paper-card, .archive-strip, .archive-entry { grid-template-columns: 1fr; }
  .top-nav { align-items: flex-start; }
  .nav-links { justify-content: flex-start; }
  .summary-strip { grid-template-columns: repeat(2, 1fr); }
  .summary-strip div:nth-child(odd) { border-left: 0; }
  .reading-controls { grid-template-columns: 1fr; }
  .recommended-section { padding: .9rem; }
  .paper-dates { grid-template-columns: 1fr; }
  .archive-entry dl { grid-template-columns: 1fr; }
  h1 { font-size: clamp(3.4rem, 24vw, 5.3rem); }
}
@media print {
  body { background: #fff; }
  body::before, .reading-controls, .hero-actions, .source-diagnostics, .archive-strip, .top-nav, .export-strip { display: none; }
  .page { width: 100%; padding: 0; }
  .paper-card { break-inside: avoid; box-shadow: none; }
}
"""


FILTER_SCRIPT = """
<script>
(() => {
  const search = document.querySelector('#paper-search');
  const latestOnly = document.querySelector('#latest-only');
  const tagFilter = document.querySelector('#tag-filter');
  const sortSelect = document.querySelector('#paper-sort');
  const list = document.querySelector('#paper-list');
  const cards = Array.from(document.querySelectorAll('.paper-card'));
  let decision = 'all';
  let source = 'all';
  function sortableDate(card, attr) {
    const value = card.dataset[attr] || '';
    return /^\\d{4}-\\d{2}-\\d{2}/.test(value) ? value : (card.dataset.firstSeen || '');
  }
  function recommendedRank(a, b) {
    const pinned = (b.dataset.pinned === 'true') - (a.dataset.pinned === 'true');
    if (pinned) return pinned;
    const rel = (a.dataset.decision === 'relevant' ? 0 : 1) - (b.dataset.decision === 'relevant' ? 0 : 1);
    if (rel) return rel;
    const score = Number(b.dataset.score || 0) - Number(a.dataset.score || 0);
    if (score) return score;
    const future = (a.dataset.futureDate === 'true' ? 1 : 0) - (b.dataset.futureDate === 'true' ? 1 : 0);
    if (future) return future;
    return sortableDate(b, 'published').localeCompare(sortableDate(a, 'published')) ||
      sortableDate(b, 'firstSeen').localeCompare(sortableDate(a, 'firstSeen')) ||
      a.dataset.title.localeCompare(b.dataset.title);
  }
  function sortCards() {
    if (!list || !sortSelect) return;
    const mode = sortSelect.value || 'recommended';
    const sorted = [...cards].sort((a, b) => {
      if (mode === 'recommended') return recommendedRank(a, b);
      if (mode === 'published-asc') return sortableDate(a, 'published').localeCompare(sortableDate(b, 'published')) || a.dataset.title.localeCompare(b.dataset.title);
      if (mode === 'first-seen-desc') return sortableDate(b, 'firstSeen').localeCompare(sortableDate(a, 'firstSeen')) || b.dataset.score - a.dataset.score;
      if (mode === 'score-desc') return Number(b.dataset.score || 0) - Number(a.dataset.score || 0) || a.dataset.title.localeCompare(b.dataset.title);
      if (mode === 'title-asc') return a.dataset.title.localeCompare(b.dataset.title);
      if (mode === 'source-asc') return a.dataset.source.localeCompare(b.dataset.source) || a.dataset.title.localeCompare(b.dataset.title);
      return sortableDate(b, 'published').localeCompare(sortableDate(a, 'published')) || b.dataset.score - a.dataset.score;
    });
    for (const card of sorted) list.appendChild(card);
  }
  function update() {
    const query = (search.value || '').toLowerCase();
    const tag = tagFilter ? tagFilter.value : 'all';
    for (const card of cards) {
      const matchesQuery = !query || card.dataset.search.includes(query);
      const matchesDecision = decision === 'all' || card.dataset.decision === decision;
      const matchesSource = source === 'all' || (card.dataset.sources || card.dataset.source || '').split(' ').includes(source);
      const matchesTag = tag === 'all' || (card.dataset.tags || '').split(' ').includes(tag);
      const matchesLatest = !latestOnly || !latestOnly.checked || card.dataset.latestRun === 'true';
      card.hidden = !(matchesQuery && matchesDecision && matchesSource && matchesTag && matchesLatest);
    }
  }
  function bindButtons(selector, attr, setter) {
    document.querySelectorAll(selector).forEach(button => {
      button.addEventListener('click', () => {
        button.parentElement.querySelectorAll('button').forEach(item => item.classList.remove('active'));
        button.classList.add('active');
        setter(button.dataset[attr]);
        update();
      });
    });
  }
  if (search) search.addEventListener('input', update);
  if (latestOnly) latestOnly.addEventListener('change', update);
  if (tagFilter) tagFilter.addEventListener('change', update);
  if (sortSelect) sortSelect.addEventListener('change', () => { sortCards(); update(); });
  bindButtons('#relevance-filters button', 'decision', value => decision = value);
  bindButtons('#source-filters button', 'source', value => source = value);
  document.querySelectorAll('.citation-button').forEach(button => {
    button.addEventListener('click', async () => {
      const status = button.parentElement.querySelector('.copy-status');
      const citation = button.dataset.citation || '';
      try {
        if (!navigator.clipboard) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(citation);
        if (status) status.textContent = 'Copied';
      } catch (error) {
        if (status) status.textContent = 'Select citation text from the page source if copying is unavailable.';
      }
    });
  });
  sortCards();
  update();
})();
</script>
"""
