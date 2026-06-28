from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
import hashlib
from html import escape
import io
import json
from pathlib import Path
import re
import sqlite3

from .deduplication import normalize_arxiv_id
from .dates import effective_sort_date, precision_rank, publication_date, sort_date_value
from .enrichment import DateEnrichmentDiagnostics, enrich_candidate_publication_date
from .fetchers.arxiv import parse_arxiv_feed
from .http import HttpClient
from .models import PaperCandidate
from .relevance import classify_with_rules
from .structured_cards import SCHEMA_VERSION, paper_card_schema, related_topics_for_paper, structured_card_for_paper


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
    publication_year: str | None = None
    publication_date_precision: str | None = None
    publication_date_source: str | None = None
    publication_date_confidence: str | None = None
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
    is_new: bool = False
    screening_abstract: str | None = None
    metadata_warnings: list[str] = field(default_factory=list)

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
class DateOverride:
    title: str | None = None
    canonical_id: str | None = None
    doi: str | None = None
    publication_date: str | None = None
    publication_date_precision: str | None = None
    publication_date_source: str | None = None
    publication_date_confidence: str | None = None
    display_label: str | None = None
    note: str | None = None


@dataclass(frozen=True)
class CurationConfig:
    pinned: list[CurationRule] = field(default_factory=list)
    overrides: list[CurationRule] = field(default_factory=list)
    excluded: list[CurationRule] = field(default_factory=list)
    date_overrides: list[DateOverride] = field(default_factory=list)


def build_site(
    digest_dir: Path | str = Path("digests"),
    report_dir: Path | str = Path("reports/paper_scout"),
    docs_dir: Path | str = Path("docs"),
    state_path: Path | str = Path("data/paper_scout.sqlite3"),
    curation_path: Path | str = Path("config/curation.yaml"),
    build_time: datetime | str | None = None,
) -> SiteBuildResult:
    digest_path = _latest_digest_path(Path(digest_dir))
    if digest_path is None:
        return SiteBuildResult(False, f"No daily digest files found in {digest_dir}. Run `python3 -m paper_scout run` first.")

    digest_root = Path(digest_dir)
    report_root = Path(report_dir)
    docs_root = Path(docs_dir)
    archive_digests = [_parse_digest(path, report_root) for path in _daily_digest_paths(digest_root)]
    latest = archive_digests[-1]
    site_build_time = _site_build_time(build_time)
    library_papers = _load_library_papers(Path(state_path))
    using_state = bool(library_papers)
    if not library_papers:
        library_papers = _library_from_digests(archive_digests)
    library_papers = _merge_dashboard_duplicates(library_papers)
    library_papers = _enrich_library_dates(library_papers)
    if using_state:
        library_papers = _refresh_rule_classifications(library_papers)
    library_papers = _apply_curation(library_papers, _load_curation(Path(curation_path)), latest.date)
    library_papers = _mark_new_papers(library_papers, site_build_time, latest.date)
    library_papers = _sort_latest_relevant(library_papers)
    latest_discoveries = [paper for paper in library_papers if paper.newly_discovered_in_latest_run]
    if not using_state and not latest_discoveries:
        latest_discoveries = _mark_new_papers(
            _library_from_digest(latest, latest_run=True, newly_discovered=True),
            site_build_time,
            latest.date,
        )

    docs_root.mkdir(parents=True, exist_ok=True)
    (docs_root / "data").mkdir(parents=True, exist_ok=True)
    generated_at = site_build_time.isoformat(sep=" ")
    _write_paper_detail_pages(docs_root, library_papers, generated_at)
    (docs_root / "style.css").write_text(STYLE_CSS, encoding="utf-8")
    (docs_root / "index.html").write_text(_render_library_page(library_papers, latest, archive_digests), encoding="utf-8")
    (docs_root / "latest.html").write_text(_render_latest_discoveries_page(latest_discoveries, latest, archive_digests), encoding="utf-8")
    (docs_root / "archive.html").write_text(_render_archive_page(archive_digests), encoding="utf-8")
    (docs_root / "about.html").write_text(_render_about_page(), encoding="utf-8")
    (docs_root / "data" / "papers.json").write_text(json.dumps([_library_paper_to_json(paper) for paper in library_papers], indent=2, sort_keys=True), encoding="utf-8")
    (docs_root / "data" / "latest.json").write_text(json.dumps(_latest_to_json(latest, latest_discoveries), indent=2, sort_keys=True), encoding="utf-8")
    (docs_root / "data" / "paper-card.schema.json").write_text(json.dumps(paper_card_schema(), indent=2, sort_keys=True), encoding="utf-8")
    (docs_root / "data" / "papers.csv").write_text(_papers_csv(library_papers), encoding="utf-8")
    (docs_root / "data" / "papers.bib").write_text(_papers_bibtex(library_papers), encoding="utf-8")
    _write_metadata_quality_report(report_root, latest.date, library_papers)
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
            warnings.append(_normalize_source_warning(_redact_secrets(line[2:].strip())))
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


def _normalize_source_warning(warning: str) -> str:
    if "semantic_scholar" in warning and re.search(r"\b429\b|rate[- ]?limit", warning, flags=re.IGNORECASE):
        prefix = re.split(r":\s*Semantic Scholar", warning, maxsplit=1)[0]
        return f"{prefix}: Semantic Scholar returned HTTP 429. This can happen when query volume is high, even with an API key. The run continued with other sources."
    return warning


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


def _site_build_time(value: datetime | str | None) -> datetime:
    if isinstance(value, datetime):
        return value.replace(microsecond=0)
    if isinstance(value, str):
        parsed = _datetime_value(value)
        if parsed:
            return parsed
    return datetime.now(UTC).replace(tzinfo=None, microsecond=0)


def _datetime_value(value: str | None) -> datetime | None:
    if not value:
        return None
    match = re.search(r"(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})(?::(\d{2}))?", value.strip())
    if not match:
        return None
    seconds = match.group(3) or "00"
    try:
        return datetime.fromisoformat(f"{match.group(1)} {match.group(2)}:{seconds}")
    except ValueError:
        return None


def _first_seen_display(value: str | None) -> str:
    parsed = _datetime_value(value)
    if parsed:
        return parsed.strftime("%Y-%m-%d %H:%M")
    return _date_part(value) or "unknown"


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


def _initial_sources(row: sqlite3.Row, sightings: list[sqlite3.Row], arxiv_id: str | None = None) -> list[str]:
    inferred = ["arxiv"] if arxiv_id else []
    return _ordered_unique([str(row["source"])] + [str(sighting["source"]) for sighting in sightings] + inferred)


def _initial_source_ids(row: sqlite3.Row, sightings: list[sqlite3.Row], arxiv_id: str | None = None) -> dict[str, list[str]]:
    source_ids: dict[str, list[str]] = {}

    def add(source: str | None, value: str | None) -> None:
        if not source or not value:
            return
        source_ids[source] = _ordered_unique([*source_ids.get(source, []), value])

    add(str(row["source"]), str(row["source_id"]) if row["source_id"] else None)
    add("arxiv", str(row["arxiv_id"]) if row["arxiv_id"] else arxiv_id)
    add("semantic_scholar", str(row["semantic_scholar_id"]) if row["semantic_scholar_id"] else None)
    add("openalex", str(row["openalex_id"]) if row["openalex_id"] else None)
    for sighting in sightings:
        add(str(sighting["source"]), str(sighting["source_id"]) if sighting["source_id"] else None)
    return source_ids


def _initial_urls(row: sqlite3.Row, arxiv_id: str | None = None) -> list[str]:
    urls = [str(row["url"]) if row["url"] else None]
    if row["doi"]:
        urls.append(f"https://doi.org/{row['doi']}")
    if row["arxiv_id"] or arxiv_id:
        urls.append(f"https://arxiv.org/abs/{row['arxiv_id'] or arxiv_id}")
    if row["semantic_scholar_id"]:
        urls.append(f"https://www.semanticscholar.org/paper/{row['semantic_scholar_id']}")
    if row["openalex_id"]:
        openalex_id = str(row["openalex_id"])
        urls.append(openalex_id if openalex_id.startswith("http") else f"https://openalex.org/{openalex_id}")
    return _ordered_unique(urls)


def _normalized_title(title: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", title.lower())).strip()


def _infer_arxiv_id_from_text(value: str) -> str | None:
    doi_match = re.search(r"10\.48550/arxiv\.([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", value, flags=re.I)
    if doi_match:
        return normalize_arxiv_id(doi_match.group(1))
    url_match = re.search(r"arxiv\.org/(?:abs|pdf)/([^?#\s\"}]+)", value, flags=re.I)
    if url_match:
        return normalize_arxiv_id(url_match.group(1))
    return None


def _paper_year(paper: LibraryPaper) -> str:
    date_value = paper.publication_year or paper.published_date or paper.first_seen_date
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
            _latest_relevant_date(paper) or "",
            paper.score,
            paper.title.lower(),
        ),
        reverse=True,
    )


def _enrich_library_dates(papers: list[LibraryPaper]) -> list[LibraryPaper]:
    http = HttpClient(retries=1, pause_seconds=0.1)
    cache: dict[str, tuple[str | None, str | None]] = {}
    enriched: list[LibraryPaper] = []
    for paper in papers:
        candidate = _paper_to_candidate(paper)
        diagnostics = DateEnrichmentDiagnostics()
        enriched_candidate = enrich_candidate_publication_date(candidate, http=http, diagnostics=diagnostics)
        if enriched_candidate.published_date and (
            enriched_candidate.published_date != paper.published_date
            or enriched_candidate.publication_date_source != paper.publication_date_source
        ):
            enriched.append(_paper_with_candidate_date(paper, enriched_candidate, diagnostics.warnings))
            continue
        if _publication_precision(paper) != "year" or not paper.arxiv_id:
            if diagnostics.warnings:
                enriched.append(LibraryPaper(**{**paper.__dict__, "metadata_warnings": [*paper.metadata_warnings, *diagnostics.warnings]}))
            else:
                enriched.append(paper)
            continue
        if paper.arxiv_id not in cache:
            cache[paper.arxiv_id] = _fetch_arxiv_publication_date(paper.arxiv_id, http)
        published_date, updated_date = cache[paper.arxiv_id]
        if not published_date:
            enriched.append(LibraryPaper(**{**paper.__dict__, "metadata_warnings": [*paper.metadata_warnings, *diagnostics.warnings]}))
            continue
        enriched.append(
            LibraryPaper(
                **{
                    **paper.__dict__,
                    "published_date": published_date,
                    "publication_year": _paper_year_from_value(published_date) or paper.publication_year,
                    "publication_date_precision": "day",
                    "publication_date_source": "arxiv",
                    "publication_date_confidence": "high",
                    "last_seen_at": paper.last_seen_at,
                    "alternate_urls": _ordered_unique([*paper.alternate_urls, f"https://arxiv.org/abs/{paper.arxiv_id}"]),
                    "sources": _ordered_unique([*paper.sources, "arxiv"]),
                    "source_ids": _merge_source_ids(paper.source_ids, {"arxiv": [paper.arxiv_id]}),
                    "screening_abstract": paper.screening_abstract,
                    "metadata_warnings": [*paper.metadata_warnings, *diagnostics.warnings],
                }
            )
        )
    return enriched


def _paper_to_candidate(paper: LibraryPaper) -> PaperCandidate:
    return PaperCandidate(
        title=paper.title,
        authors=paper.authors,
        abstract=paper.screening_abstract or paper.abstract_summary,
        source=paper.source,
        source_id=paper.source_id or paper.canonical_id,
        doi=paper.doi,
        arxiv_id=paper.arxiv_id,
        semantic_scholar_id=paper.semantic_scholar_id,
        openalex_id=paper.openalex_id,
        url=paper.url,
        published_date=paper.published_date,
        publication_year=paper.publication_year,
        publication_date_precision=paper.publication_date_precision,
        publication_date_source=paper.publication_date_source,
        publication_date_confidence=paper.publication_date_confidence,
        raw={},
    )


def _paper_with_candidate_date(paper: LibraryPaper, candidate: PaperCandidate, warnings: list[str]) -> LibraryPaper:
    alternate_urls = paper.alternate_urls
    if candidate.doi:
        alternate_urls = _ordered_unique([*alternate_urls, f"https://doi.org/{candidate.doi}"])
    sources = paper.sources
    if candidate.publication_date_source == "ssrn":
        sources = _ordered_unique([*sources, "ssrn"])
    return LibraryPaper(
        **{
            **paper.__dict__,
            "doi": candidate.doi or paper.doi,
            "published_date": candidate.published_date,
            "publication_year": candidate.publication_year,
            "publication_date_precision": candidate.publication_date_precision,
            "publication_date_source": candidate.publication_date_source,
            "publication_date_confidence": candidate.publication_date_confidence,
            "alternate_urls": alternate_urls,
            "sources": sources,
            "metadata_warnings": [*paper.metadata_warnings, *warnings],
        }
    )


def _fetch_arxiv_publication_date(arxiv_id: str, http: HttpClient) -> tuple[str | None, str | None]:
    try:
        payload = http.get_text("https://export.arxiv.org/api/query", params={"id_list": arxiv_id, "max_results": 1})
        papers = parse_arxiv_feed(payload)
    except Exception:
        return None, None
    match = next((paper for paper in papers if paper.arxiv_id == arxiv_id), None)
    if not match or match.publication_date_precision != "day":
        return None, None
    return match.published_date, match.updated_date


def _sort_latest_relevant(papers: list[LibraryPaper]) -> list[LibraryPaper]:
    return sorted(papers, key=_latest_relevant_sort_key)


def _sort_recommended(papers: list[LibraryPaper]) -> list[LibraryPaper]:
    return _sort_latest_relevant(papers)


def _latest_relevant_sort_key(paper: LibraryPaper) -> tuple[object, ...]:
    return (
        0 if paper.is_new else 1,
        0 if paper.decision == "relevant" else 1,
        _latest_relevant_date_bucket(paper),
        _reverse_date_sort_value(_latest_relevant_date(paper)),
        -paper.score,
        paper.title.lower(),
    )


def _recommended_sort_key(paper: LibraryPaper) -> tuple[object, ...]:
    return _latest_relevant_sort_key(paper)


def _latest_relevant_date(paper: LibraryPaper) -> str | None:
    return effective_sort_date(
        paper.published_date,
        _publication_precision(paper),
        paper.first_seen_date,
        paper.future_date,
    )


def _latest_relevant_date_bucket(paper: LibraryPaper) -> int:
    if paper.future_date:
        return 2
    if precision_rank(_publication_precision(paper)) >= precision_rank("month"):
        return 0
    return 1


def _reverse_date_sort_value(value: str | None) -> int:
    parsed = _date_ordinal(sort_date_value(value, publication_date(value, None).precision))
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
    published_meta = publication_date(published_date, None)
    published = _date_ordinal(sort_date_value(published_meta.value, published_meta.precision))
    built = _date_ordinal(build_date)
    return bool(published is not None and built is not None and published > built)


def _mark_new_papers(papers: list[LibraryPaper], build_time: datetime, fallback_date: str) -> list[LibraryPaper]:
    return [
        LibraryPaper(
            **{
                **paper.__dict__,
                "is_new": _is_new_since_first_seen(paper.first_seen_at, build_time, fallback_date),
            }
        )
        for paper in papers
    ]


def _is_new_since_first_seen(first_seen_at: str | None, build_time: datetime, fallback_date: str) -> bool:
    first_seen_time = _datetime_value(first_seen_at)
    if first_seen_time:
        age = build_time - first_seen_time
        return timedelta(0) <= age <= timedelta(hours=24)
    first_seen_date = _date_part(first_seen_at)
    return bool(first_seen_date and first_seen_date == fallback_date)


def _apply_curation(papers: list[LibraryPaper], curation: CurationConfig, build_date: str) -> list[LibraryPaper]:
    curated: list[LibraryPaper] = []
    for paper in papers:
        if _matching_rule(paper, curation.excluded):
            continue
        pinned_rule = _matching_rule(paper, curation.pinned)
        override_rule = _matching_rule(paper, curation.overrides)
        date_override = _matching_date_override(paper, curation.date_overrides)
        updated = paper
        if override_rule:
            updated = _apply_override(updated, override_rule)
        if date_override:
            updated = _apply_date_override(updated, date_override)
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


def _matching_date_override(paper: LibraryPaper, overrides: list[DateOverride]) -> DateOverride | None:
    normalized = _normalized_title(paper.title)
    for override in overrides:
        if override.canonical_id and override.canonical_id == paper.canonical_id:
            return override
        if override.doi and paper.doi and override.doi.lower() == paper.doi.lower():
            return override
        if override.title and _normalized_title(override.title) == normalized:
            return override
    return None


def _apply_date_override(paper: LibraryPaper, override: DateOverride) -> LibraryPaper:
    published = publication_date(override.publication_date, override.publication_date_source or "manual", paper.publication_year)
    return LibraryPaper(
        **{
            **paper.__dict__,
            "published_date": published.value or paper.published_date,
            "publication_year": published.year or paper.publication_year,
            "publication_date_precision": override.publication_date_precision or published.precision,
            "publication_date_source": override.publication_date_source or published.source or paper.publication_date_source,
            "publication_date_confidence": override.publication_date_confidence or paper.publication_date_confidence,
            "research_note": paper.research_note or override.note,
        }
    )


def _refresh_rule_classifications(papers: list[LibraryPaper]) -> list[LibraryPaper]:
    refreshed: list[LibraryPaper] = []
    for paper in papers:
        candidate = PaperCandidate(
            title=paper.title,
            authors=paper.authors,
            abstract=paper.screening_abstract or paper.abstract_summary,
            source=paper.source,
            source_id=paper.source_id or paper.canonical_id,
            doi=paper.doi,
            arxiv_id=paper.arxiv_id,
            semantic_scholar_id=paper.semantic_scholar_id,
            openalex_id=paper.openalex_id,
            url=paper.url,
            published_date=paper.published_date,
            publication_year=paper.publication_year,
            publication_date_precision=paper.publication_date_precision,
            publication_date_source=paper.publication_date_source,
            raw={},
        )
        classification = classify_with_rules(candidate)
        refreshed.append(
            LibraryPaper(
                **{
                    **paper.__dict__,
                    "abstract_summary": classification.abstract_summary or paper.abstract_summary,
                    "reason": classification.reason,
                    "score": classification.score,
                    "decision": classification.decision,
                    "tags": classification.tags,
                }
            )
        )
    return refreshed


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
        date_overrides=[_date_override(item) for item in sections.get("date_overrides", [])],
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


def _date_override(item: dict[str, object]) -> DateOverride:
    return DateOverride(
        title=_redact_secrets(str(item["title"])) if item.get("title") else None,
        canonical_id=_redact_secrets(str(item["canonical_id"])) if item.get("canonical_id") else None,
        doi=_redact_secrets(str(item["doi"])) if item.get("doi") else None,
        publication_date=_redact_secrets(str(item["publication_date"])) if item.get("publication_date") else None,
        publication_date_precision=_redact_secrets(str(item["publication_date_precision"])) if item.get("publication_date_precision") else None,
        publication_date_source=_redact_secrets(str(item["publication_date_source"])) if item.get("publication_date_source") else None,
        publication_date_confidence=_redact_secrets(str(item["publication_date_confidence"])) if item.get("publication_date_confidence") else None,
        display_label=_redact_secrets(str(item["display_label"])) if item.get("display_label") else None,
        note=_redact_secrets(str(item["note"])) if item.get("note") else None,
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
    return "Peripheral review candidate"


def _with_aggregates(paper: LibraryPaper) -> LibraryPaper:
    sources = _ordered_unique([paper.source, *paper.sources])
    source_ids = _merge_source_ids(paper.source_ids, {paper.source: _ordered_unique([paper.source_id])})
    alternate_urls = _ordered_unique([paper.url, *paper.alternate_urls])
    return LibraryPaper(**{**paper.__dict__, "sources": sources, "source_ids": source_ids, "alternate_urls": alternate_urls})


def _merge_two_papers(left: LibraryPaper, right: LibraryPaper) -> LibraryPaper:
    right = _with_aggregates(right)
    best = left if left.score >= right.score else right
    best_date = _best_publication_metadata(left, right)
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
        published_date=best_date.value,
        first_seen_at=first_seen_at,
        last_seen_at=last_seen_at,
        notified_at=notified_at,
        notified_date=notified_date,
        publication_year=best_date.year,
        publication_date_precision=best_date.precision,
        publication_date_source=best_date.source,
        publication_date_confidence=_best_publication_confidence(left, right, best_date.source),
        appeared_in_latest_run=left.appeared_in_latest_run or right.appeared_in_latest_run,
        newly_discovered_in_latest_run=left.newly_discovered_in_latest_run or right.newly_discovered_in_latest_run,
        sources=sources,
        source_ids=source_ids,
        alternate_urls=alternate_urls,
        screening_abstract=best.screening_abstract or left.screening_abstract or right.screening_abstract,
        metadata_warnings=[*left.metadata_warnings, *right.metadata_warnings],
    )


def _best_publication_metadata(left: LibraryPaper, right: LibraryPaper):
    left_date = publication_date(left.published_date, left.publication_date_source, left.publication_year)
    right_date = publication_date(right.published_date, right.publication_date_source, right.publication_year)
    if precision_rank(right_date.precision) > precision_rank(left_date.precision):
        return right_date
    return left_date


def _best_publication_confidence(left: LibraryPaper, right: LibraryPaper, source: str | None) -> str | None:
    if source == right.publication_date_source:
        return right.publication_date_confidence
    if source == left.publication_date_source:
        return left.publication_date_confidence
    return left.publication_date_confidence or right.publication_date_confidence


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
        _ensure_site_column(db, "publication_year", "TEXT")
        _ensure_site_column(db, "publication_date_precision", "TEXT")
        _ensure_site_column(db, "publication_date_source", "TEXT")
        _ensure_site_column(db, "publication_date_confidence", "TEXT")
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
        doi = _redact_secrets(str(row["doi"])) if row["doi"] else None
        url = _redact_secrets(str(row["url"])) if row["url"] else None
        arxiv_id = _redact_secrets(str(row["arxiv_id"])) if row["arxiv_id"] else _infer_arxiv_id_from_text(" ".join([str(row["doi"] or ""), str(row["url"] or ""), str(row["raw_json"] or "")]))
        sources = _initial_sources(row, row_sightings, arxiv_id)
        source_ids = _initial_source_ids(row, row_sightings, arxiv_id)
        alternate_urls = _initial_urls(row, arxiv_id)
        papers.append(
            LibraryPaper(
                canonical_id=_redact_secrets(canonical_id),
                title=_redact_secrets(str(row["title"])),
                authors=[_redact_secrets(author) for author in _json_list(row["authors_json"])],
                abstract_summary=_redact_secrets(str(row["abstract_summary"] or row["abstract"] or "")),
                screening_abstract=_redact_secrets(str(row["abstract"] or row["abstract_summary"] or "")),
                reason=_redact_secrets(str(row["relevance_reason"] or "")),
                score=int(row["relevance_score"]),
                decision=str(row["relevance_decision"]),
                tags=[_redact_secrets(tag) for tag in _json_list(row["tags_json"])],
                source=str(row["source"]),
                source_id=_redact_secrets(str(row["source_id"])) if row["source_id"] else None,
                doi=doi,
                arxiv_id=arxiv_id,
                semantic_scholar_id=_redact_secrets(str(row["semantic_scholar_id"])) if row["semantic_scholar_id"] else None,
                openalex_id=_redact_secrets(str(row["openalex_id"])) if row["openalex_id"] else None,
                url=url,
                published_date=str(row["published_date"]) if row["published_date"] else None,
                first_seen_at=first_seen_at,
                last_seen_at=str(row["last_seen_at"]) if row["last_seen_at"] else None,
                notified_at=str(row["notified_at"]) if row["notified_at"] else None,
                notified_date=str(row["digest_date"]) if row["digest_date"] else None,
                publication_year=str(row["publication_year"]) if row["publication_year"] else _paper_year_from_value(row["published_date"]),
                publication_date_precision=str(row["publication_date_precision"]) if row["publication_date_precision"] else publication_date(row["published_date"], None).precision,
                publication_date_source=str(row["publication_date_source"]) if row["publication_date_source"] else str(row["source"]),
                publication_date_confidence=str(row["publication_date_confidence"]) if row["publication_date_confidence"] else _date_confidence(str(row["publication_date_precision"]) if row["publication_date_precision"] else None, str(row["publication_date_source"]) if row["publication_date_source"] else str(row["source"])),
                appeared_in_latest_run=appeared_in_latest_run,
                newly_discovered_in_latest_run=newly_discovered,
                sources=sources,
                source_ids=source_ids,
                alternate_urls=alternate_urls,
            )
        )
    return papers


def _ensure_site_column(db: sqlite3.Connection, column: str, definition: str) -> None:
    columns = {row["name"] for row in db.execute("PRAGMA table_info(papers)").fetchall()}
    if column not in columns:
        db.execute(f"ALTER TABLE papers ADD COLUMN {column} {definition}")


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
        published = publication_date(None if paper.date == "unknown" else paper.date, paper.source)
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
                published_date=published.value,
                first_seen_at=digest.date,
                last_seen_at=digest.date,
                notified_at=None,
                notified_date=digest.date,
                publication_year=published.year,
                publication_date_precision=published.precision,
                publication_date_source=published.source,
                publication_date_confidence=_date_confidence(published.precision, published.source),
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


def _write_paper_detail_pages(docs_root: Path, papers: list[LibraryPaper], generated_at: str) -> None:
    papers_dir = docs_root / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)
    for stale_path in papers_dir.iterdir():
        if stale_path.suffix in {".html", ".json"}:
            stale_path.unlink()
    for paper in papers:
        slug = _paper_slug(paper)
        (papers_dir / f"{slug}.html").write_text(_render_paper_detail_page(paper), encoding="utf-8")
        (papers_dir / f"{slug}.json").write_text(
            json.dumps(_paper_detail_json(paper, generated_at), indent=2, sort_keys=True),
            encoding="utf-8",
        )


def _paper_slug(paper: LibraryPaper) -> str:
    title = re.sub(r"[^a-z0-9]+", "-", paper.title.lower()).strip("-") or "paper"
    title = title[:84].strip("-") or "paper"
    digest = hashlib.sha1(paper.canonical_id.encode("utf-8")).hexdigest()[:8]
    return f"{title}-{digest}"


def _paper_detail_url(paper: LibraryPaper) -> str:
    return f"papers/{_paper_slug(paper)}.html"


def _paper_detail_json_url(paper: LibraryPaper) -> str:
    return f"papers/{_paper_slug(paper)}.json"


def _paper_detail_json(paper: LibraryPaper, generated_at: str) -> dict[str, object]:
    data = _library_paper_to_json(paper)
    data["detail_page"] = _paper_detail_url(paper)
    data["detail_json"] = _paper_detail_json_url(paper)
    structured_card = structured_card_for_paper(paper)
    data["schema_version"] = SCHEMA_VERSION
    data["ssrn_id"] = _ssrn_id(paper)
    data["publication"] = {
        "date": paper.published_date,
        "year": paper.publication_year or _paper_year_from_value(paper.published_date),
        "precision": _publication_precision(paper),
        "source": paper.publication_date_source,
        "confidence": paper.publication_date_confidence or "unknown",
        "publication_date_confidence": paper.publication_date_confidence or "unknown",
        "display": _published_text(paper),
    }
    data["relevance"] = {
        "decision": paper.decision,
        "public_label": _decision_label(paper.decision),
        "score": paper.score,
        "reason": paper.reason,
        "tags": paper.tags,
        "curation_note": paper.research_note,
        "review_status": paper.review_status,
    }
    data["structured_card"] = structured_card
    data["related_topics"] = related_topics_for_paper(paper)
    data["provenance"] = _paper_provenance(paper, generated_at)
    data["structured_sections"] = {
        "possible_key_claims": [],
        "method_or_system_type": structured_card["method_or_system_type"]["value"],
        "evidence_or_evaluation_signals": [],
        "relation_to_agentic_memory": structured_card["relation_to_agentic_memory"]["value"],
    }
    return data


def _paper_provenance(paper: LibraryPaper, generated_at: str | None = None) -> dict[str, object]:
    has_curation = bool(paper.research_note or paper.pinned or paper.review_status)
    return {
        "screening_source": "deterministic rules + curation" if has_curation else "deterministic rules",
        "metadata_sources": paper.sources or [paper.source],
        "source_ids": paper.source_ids,
        "date_source": paper.publication_date_source,
        "publication_date_source": paper.publication_date_source,
        "publication_date_precision": _publication_precision(paper),
        "publication_date_confidence": paper.publication_date_confidence,
        "relevance_source": "deterministic screening + curation" if has_curation else "deterministic screening",
        "curation_note": "manually added" if has_curation else None,
        "curated": has_curation,
        "generated_at": generated_at,
        "first_seen_at": paper.first_seen_at,
        "last_seen_at": paper.last_seen_at,
    }


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
        "detail_page": _paper_detail_url(paper),
        "detail_json": _paper_detail_json_url(paper),
        "publication_date": paper.published_date,
        "publication_year": paper.publication_year or _paper_year_from_value(paper.published_date),
        "publication_date_precision": _publication_precision(paper),
        "publication_date_source": paper.publication_date_source,
        "publication_date_confidence": paper.publication_date_confidence,
        "effective_sort_date": _latest_relevant_date(paper),
        "latest_relevant_date_bucket": _latest_relevant_date_bucket(paper),
        "first_seen_date": paper.first_seen_date,
        "first_seen_at": paper.first_seen_at,
        "is_new": paper.is_new,
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
    default_decision = _default_homepage_decision(papers)
    return _page(
        "Agentic Memory Paper Library",
        f"""
        <header class="briefing-hero">
          <nav class="top-nav" aria-label="Primary">
            <a class="brand" href="index.html">Library</a>
            <span class="nav-links">
              <a href="about.html">About</a>
              <a href="archive.html">Archive</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub</a>
            </span>
          </nav>
          <div class="library-hero">
            <h1>Agentic Memory Paper Library</h1>
            <p class="hero-copy">A daily updated library of papers on agentic memory, deep research agents, and memory mechanisms.</p>
            <p class="hero-line">{_hero_line(papers, latest)}</p>
          </div>
        </header>
        {_library_controls(default_decision=default_decision)}
        <section class="paper-section primary-section" id="paper-library" data-section="library">
          <div class="section-heading">
            <h2>Papers to look at</h2>
            <p>Newest relevant papers first. New papers are shown first for 24 hours.</p>
          </div>
          <div class="paper-list" id="paper-list">
            {_library_paper_cards(papers, default_decision=default_decision)}
          </div>
          <p class="empty no-results" id="no-results" hidden>No papers match the current search.</p>
        </section>
        {_secondary_footer(latest, archive)}
        {FILTER_SCRIPT}
        """,
    )


def _render_latest_discoveries_page(papers: list[LibraryPaper], latest: ParsedDigest, archive: list[ParsedDigest]) -> str:
    has_highly_relevant = any(paper.decision == "relevant" for paper in papers)
    if not papers:
        paper_cards = '<p class="empty latest-empty">No new papers were found in the latest run. The cumulative library was refreshed.</p>'
        latest_heading = "Papers first seen in the latest Paper Scout run."
        latest_notice = ""
    elif not has_highly_relevant:
        paper_cards = _library_paper_cards(papers, default_decision="all")
        latest_heading = "Review candidates found in the latest run"
        latest_notice = '<p class="empty latest-empty">No highly relevant papers were found in the latest run. The cumulative library was refreshed.</p>'
    else:
        paper_cards = _library_paper_cards(papers, default_decision="all")
        latest_heading = "Papers first seen in the latest Paper Scout run."
        latest_notice = ""
    return _page(
        "Latest Paper Scout Run",
        f"""
        <header class="archive-hero">
          <nav class="top-nav" aria-label="Primary">
            <a class="brand" href="index.html">Paper Scout</a>
            <span class="nav-links">
              <a href="index.html">Library</a>
              <a href="archive.html">Archive</a>
              <a href="about.html">About</a>
              <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/latest.md">Markdown digest</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub</a>
            </span>
          </nav>
          <p class="eyebrow">Latest update {escape(latest.date)}</p>
          <h1>Latest run</h1>
          <p class="hero-copy">Papers first seen in the latest Paper Scout run. The main library remains cumulative.</p>
        </header>
        {_latest_summary_strip(papers, latest)}
        {_library_controls(default_decision="all")}
        <section class="paper-section primary-section" id="paper-library" data-section="latest">
          <div class="section-heading">
            <p class="section-kicker">New this run</p>
            <h2>{escape(latest_heading)}</h2>
          </div>
          {latest_notice}
          <div class="paper-list" id="paper-list">
            {paper_cards}
          </div>
          <p class="empty no-results" id="no-results" hidden>No papers match the current search.</p>
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
            <div><dt>Review candidates</dt><dd>{_section_count(item, 'Maybe Relevant')}</dd></div>
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
              <a href="latest.html">Latest run</a>
              <a href="about.html">About</a>
              <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/latest.md">Latest Markdown</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub</a>
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
              <a href="latest.html">Latest run</a>
              <a href="archive.html">Archive</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub</a>
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
            <p>The scout uses deterministic filters and optional LLM classification. Highly relevant means the paper directly supports agent-memory research; review candidates may be useful but need human judgment.</p>
          </article>
          <article>
            <h2>Manual curation</h2>
            <p>Optional curation can pin, annotate, override, or hide papers in the static dashboard without deleting anything from SQLite state.</p>
          </article>
          <article>
            <h2>Structured paper cards</h2>
            <p>The cumulative library links each paper to a structured detail page and sidecar JSON. These static records are meant for human review and future agent workflows; fields are provenance-aware, incomplete extraction is shown as “Not extracted yet”, and the sidecar schema is published at <a href="data/paper-card.schema.json">paper-card.schema.json</a>.</p>
            <p>Structured cards are generated from title, abstract or summary, metadata, deterministic screening, and curation notes. They do not claim that Paper Scout has deeply read the full paper.</p>
          </article>
          <article>
            <h2>Limitations</h2>
            <p>Relevance scoring can produce false positives or false negatives. Semantic Scholar rate limits may occur. Source metadata can be wrong, and future publication dates may reflect source metadata rather than actual availability.</p>
          </article>
        </section>
        """,
    )


def _structured_card_html(card: dict[str, dict[str, str]]) -> str:
    rows = []
    labels = [
        ("research_relevance", "Research relevance"),
        ("method_or_system_type", "Method / system type"),
        ("key_contribution", "Key contribution"),
        ("evidence_or_evaluation", "Evidence / evaluation"),
        ("relation_to_agentic_memory", "Relation to agentic memory"),
        ("limitations_or_uncertainty", "Limitations / uncertainty"),
    ]
    for key, label in labels:
        field = card.get(key, {})
        value = field.get("value", "Not extracted yet")
        confidence = field.get("confidence", "unknown")
        provenance = field.get("provenance", "unknown")
        value_class = ' class="structured-empty"' if value == "Not extracted yet" else ""
        rows.append(
            f"""
            <div>
              <dt>{escape(label)}</dt>
              <dd{value_class}>{escape(value)}</dd>
              <dd class="structured-provenance">Confidence: {escape(confidence)} · Provenance: {escape(provenance)}</dd>
            </div>
            """
        )
    return f'<dl class="detail-metadata structured-card-fields">{"".join(rows)}</dl>'


def _render_paper_detail_page(paper: LibraryPaper) -> str:
    sources = paper.sources or [paper.source]
    source_items = "".join(f"<li>{escape(_source_label(source))}</li>" for source in sources)
    alternate_links = _secondary_links(paper) or '<p class="muted">No alternate source links recorded.</p>'
    identifiers = "".join(f"<li>{item}</li>" for item in _identifier_list(paper)) or "<li>No additional identifiers recorded.</li>"
    structured_card = structured_card_for_paper(paper)
    structured_card_html = _structured_card_html(structured_card)
    research_note = (
        f"""
        <section class="detail-panel">
          <p class="section-kicker">Research note</p>
          <p>{escape(paper.research_note)}</p>
        </section>
        """
        if paper.research_note
        else ""
    )
    json_href = f"{_paper_slug(paper)}.json"
    open_link = f'<a class="paper-link" href="{escape(paper.url)}">Open paper</a>' if paper.url else '<span class="paper-link disabled">No link available</span>'
    provenance = _paper_provenance(paper)
    provenance_items = "".join(
        f"<li>{escape(label)}: {escape(_display_value(value))}</li>"
        for label, value in [
            ("Metadata sources", ", ".join(str(source) for source in provenance["metadata_sources"])),
            ("Publication date source", provenance["publication_date_source"]),
            ("Publication date precision", provenance["publication_date_precision"]),
            ("Publication date confidence", provenance["publication_date_confidence"]),
            ("Relevance source", provenance["relevance_source"]),
            ("Curation note", provenance["curation_note"]),
            ("First seen by Paper Scout", provenance["first_seen_at"] or paper.first_seen_date),
            ("Last seen by Paper Scout", provenance["last_seen_at"] or paper.last_seen_date),
        ]
    )
    return _page(
        paper.title,
        f"""
        <header class="archive-hero paper-detail-hero">
          <nav class="top-nav" aria-label="Primary">
            <a class="brand" href="../index.html">Library</a>
            <span class="nav-links">
              <a href="../index.html">All papers</a>
              <a href="../about.html">About</a>
              <a href="../archive.html">Archive</a>
            </span>
          </nav>
          <p class="eyebrow">Structured paper detail</p>
          <h1>{escape(paper.title)}</h1>
          <p class="hero-copy">{escape(paper.authors_text)}</p>
          <div class="paper-detail-actions">
            {open_link}
            <a class="paper-detail-link" href="{escape(json_href)}">Download paper JSON</a>
          </div>
        </header>
        <section class="paper-detail-layout">
          <section class="detail-panel">
            <p class="section-kicker">Authors</p>
            <p>{escape(paper.authors_text)}</p>
          </section>
          <section class="detail-panel">
            <p class="section-kicker">Publication/date metadata</p>
            <dl class="detail-metadata">
              <div><dt>Display date</dt><dd>{escape(_published_text(paper))}</dd></div>
              <div><dt>Publication date</dt><dd>{escape(_display_value(paper.published_date))}</dd></div>
              <div><dt>Publication year</dt><dd>{escape(_display_value(paper.publication_year or _paper_year_from_value(paper.published_date)))}</dd></div>
              <div><dt>Publication date source</dt><dd>{escape(_display_value(paper.publication_date_source))}</dd></div>
              <div><dt>Publication date precision</dt><dd>{escape(_display_value(_publication_precision(paper)))}</dd></div>
              <div><dt>Publication date confidence</dt><dd>{escape(_display_value(paper.publication_date_confidence))}</dd></div>
            </dl>
          </section>
          <section class="detail-panel">
            <p class="section-kicker">Sources</p>
            <ul>{source_items}</ul>
            {alternate_links}
          </section>
          <section class="detail-panel">
            <p class="section-kicker">Why included</p>
            <p>{escape(_short_reason(paper))}</p>
          </section>
          {research_note}
          <section class="detail-panel wide">
            <p class="section-kicker">Abstract / summary</p>
            <p>{escape(paper.abstract_summary or "No abstract summary available.")}</p>
          </section>
          <section class="detail-panel wide structured-card-panel">
            <p class="section-kicker">Structured research card</p>
            {structured_card_html}
          </section>
          <section class="detail-panel">
            <p class="section-kicker">Screening details</p>
            <ul>
              <li>Decision: {escape(_decision_label(paper.decision))}</li>
              <li>Score: {paper.score}/100</li>
              <li>Classifier label: {escape(paper.relevance_label or _relevance_label(paper))}</li>
              <li>Tags: {escape(", ".join(paper.tags) or "untagged")}</li>
            </ul>
          </section>
          <section class="detail-panel">
            <p class="section-kicker">Provenance</p>
            <ul>{provenance_items}</ul>
            <ul>{identifiers}</ul>
          </section>
          <section class="detail-panel">
            <p class="section-kicker">Exports</p>
            <p><a href="{escape(json_href)}">Download paper JSON</a></p>
            <details class="paper-more">
              <summary>Citation text</summary>
              <p>{escape(paper.citation)}</p>
            </details>
          </section>
        </section>
        """,
        stylesheet="../style.css",
    )


def _display_value(value: object) -> str:
    return str(value) if value is not None and value != "" else "unknown"


def _page(title: str, body: str, stylesheet: str = "style.css") -> str:
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="Daily Paper Scout briefing for agentic memory, deep research agents, and memory mechanisms.">
  <link rel="stylesheet" href="{escape(stylesheet)}">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <main class="page" id="main-content">
    {body}
  </main>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in html.splitlines()) + "\n"


def _summary_strip(digest: ParsedDigest) -> str:
    cells = [
        ("Candidates fetched", digest.summary.get("Candidates fetched", "0")),
        ("New unique papers", digest.summary.get("New unique papers", "0")),
        ("Highly relevant", digest.summary.get("Relevant", "0")),
        ("Review candidates", digest.summary.get("Maybe relevant", "0")),
        ("Digest-quality warnings", str(digest.digest_quality_warning_count)),
    ]
    metric_cells = "".join(f"<div><span>{escape(label)}</span><strong>{escape(value)}</strong></div>" for label, value in cells)
    return f"""
    <section class="summary-strip" aria-label="Run summary metrics">
      {metric_cells}
      <div class="source-summary"><span>Source summary</span><strong>{escape(digest.summary.get("Source summary", "none"))}</strong></div>
    </section>
    """


def _hero_line(papers: list[LibraryPaper], latest: ParsedDigest) -> str:
    highly = sum(1 for paper in papers if paper.decision == "relevant")
    return f"Updated {escape(latest.date)} · {len(papers)} papers · {highly} highly relevant"


def _default_homepage_decision(papers: list[LibraryPaper]) -> str:
    return "relevant" if any(paper.decision == "relevant" for paper in papers) else "all"


def _library_summary_strip(papers: list[LibraryPaper], latest: ParsedDigest) -> str:
    highly = sum(1 for paper in papers if paper.decision == "relevant")
    maybe = sum(1 for paper in papers if paper.decision == "maybe")
    latest_count = sum(1 for paper in papers if paper.newly_discovered_in_latest_run)
    cells = [
        ("Total known papers", str(len(papers))),
        ("New in latest run", str(latest_count)),
        ("Highly relevant", str(highly)),
        ("Review candidates", str(maybe)),
        ("Latest update date", latest.date),
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
        ("Review candidates", str(sum(1 for paper in papers if paper.decision == "maybe"))),
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
          <button data-decision="maybe">Review candidates</button>
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


def _library_controls(default_decision: str = "all") -> str:
    selected = {
        "all": " selected" if default_decision == "all" else "",
        "relevant": " selected" if default_decision == "relevant" else "",
        "maybe": " selected" if default_decision == "maybe" else "",
    }
    return f"""
    <section class="reading-controls library-controls" aria-label="Library controls" data-default-decision="{escape(default_decision)}">
      <label class="search-field" for="paper-search">
        <span>Search</span>
        <input id="paper-search" type="search" placeholder="Search papers...">
      </label>
      <label class="select-field" for="paper-sort">
        <span>Sort</span>
          <select id="paper-sort">
          <option value="latest-relevant" selected>Latest relevant</option>
          <option value="score-desc">Screening match</option>
          <option value="published-desc">Publication date</option>
          <option value="first-seen-desc">First seen</option>
          <option value="title-asc">Title</option>
        </select>
      </label>
      <label class="select-field relevance-filter" for="relevance-filter">
        <span>Show</span>
        <select id="relevance-filter">
          <option value="relevant"{selected["relevant"]}>Highly relevant</option>
          <option value="all"{selected["all"]}>All papers</option>
          <option value="maybe"{selected["maybe"]}>Review candidates</option>
        </select>
      </label>
      <label class="toggle-control new-only-filter" for="new-only">
        <input id="new-only" type="checkbox">
        <span>New only</span>
      </label>
    </section>
    """


def _warnings(warnings: list[str]) -> str:
    if not warnings:
        return '<details class="source-diagnostics"><summary>Source diagnostics <span>0 warnings</span></summary><p>No source warnings.</p></details>'
    summary = _source_warning_summary(warnings)
    compact = "\n".join(f"<li>{escape(warning)}</li>" for warning in warnings)
    return f'<details class="source-diagnostics"><summary>Source diagnostics <span>{escape(summary)}</span></summary><ul>{compact}</ul></details>'


def _source_warning_summary(warnings: list[str]) -> str:
    if not warnings:
        return "0 warnings"
    rate_limited = sum(1 for warning in warnings if re.search(r"\b(429|rate[- ]?limit)", warning, flags=re.IGNORECASE))
    other = len(warnings) - rate_limited
    if rate_limited and not other:
        return "Some source queries were rate-limited. The library was still refreshed from available sources."
    if rate_limited:
        return "Some source queries were rate-limited. Details are available below."
    return "Some source diagnostics need review. Details are available below."


def _secondary_footer(latest: ParsedDigest, archive: list[ParsedDigest]) -> str:
    recent = "".join(
        f'<a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/{escape(item.date)}.md">{escape(item.date)}</a>'
        for item in reversed(archive[:8])
    )
    warnings = "\n".join(f"<li>{escape(warning)}</li>" for warning in latest.source_warnings) or "<li>No source warnings.</li>"
    warning_summary = _source_warning_summary(latest.source_warnings)
    return f"""
    <footer class="library-footer">
      <details class="export-library">
        <summary>Export library</summary>
        <div class="footer-links">
          <a href="data/papers.csv">Download CSV</a>
          <a href="data/papers.bib">Download BibTeX</a>
          <a href="data/papers.json">Download JSON</a>
        </div>
      </details>
      <details class="technical-diagnostics">
        <summary>Technical diagnostics <span>{escape(warning_summary)}</span></summary>
        <div class="diagnostic-grid">
          <div>
            <h3>Run metadata</h3>
            <p>Latest update: {escape(latest.date)}</p>
            <p>Candidates fetched: {escape(latest.summary.get("Candidates fetched", "0"))}</p>
            <p>New unique papers: {escape(latest.summary.get("New unique papers", "0"))}</p>
            <p>Digest-quality warnings: {latest.digest_quality_warning_count}</p>
          </div>
          <div>
            <h3>Sources</h3>
            <p>{escape(latest.summary.get("Source summary", "none"))}</p>
          </div>
          <div>
            <h3>Source warnings</h3>
            <ul>{warnings}</ul>
          </div>
        </div>
      </details>
      <nav class="footer-links" aria-label="Secondary">
        <a href="latest.html">Latest run</a>
        <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/latest.md">Markdown digest</a>
        {recent}
      </nav>
    </footer>
    """


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


def _library_paper_cards(papers: list[LibraryPaper], default_decision: str = "all") -> str:
    if not papers:
        return '<p class="empty">No papers in this section.</p>'
    return "\n".join(_library_paper_card(paper, default_decision=default_decision) for paper in papers)


def _library_paper_card(paper: LibraryPaper, default_decision: str = "all") -> str:
    details_tags = _all_tag_badges(paper.tags)
    sources = paper.sources or [paper.source]
    source_badges = "".join(f'<span class="badge source">{escape(_source_label(source))}</span>' for source in sources)
    source_names = ", ".join(_source_label(source) for source in sources)
    link = f'<a class="paper-link" href="{escape(paper.url)}">Open paper</a>' if paper.url else '<span class="paper-link disabled">No link available</span>'
    detail_link = f'<a class="paper-detail-link" href="{escape(_paper_detail_url(paper))}">Details</a>'
    secondary_links = _secondary_links(paper)
    published = _published_text(paper)
    search_text = " ".join([paper.title, paper.authors_text, paper.abstract_summary, paper.reason, paper.research_note or "", " ".join(paper.tags), " ".join(sources), paper.decision]).lower()
    tag_text = " ".join(paper.tags)
    source_text = " ".join(sources)
    density = "primary" if paper.decision == "relevant" else "compact"
    pinned_detail = "<li>Pinned for thesis review.</li>" if paper.pinned else ""
    status_detail = f"<li>Review status: {escape(paper.review_status)}</li>" if paper.review_status else ""
    note = f'<p class="research-note"><strong>Research note</strong> {escape(paper.research_note)}</p>' if paper.research_note else ""
    relevance_label = paper.relevance_label or _relevance_label(paper)
    ids = _identifier_list(paper)
    more_items = "".join(f"<li>{item}</li>" for item in ids) or "<li>No additional identifiers.</li>"
    hidden = " hidden" if default_decision != "all" and paper.decision != default_decision else ""
    new_badge = '<span class="new-badge" title="New in the last 24 hours" aria-label="New in the last 24 hours">New</span>' if paper.is_new else ""
    first_seen_text = _first_seen_display(paper.first_seen_at)
    return f"""
    <article class="paper-card {escape(density)}" data-source="{escape(paper.source)}" data-sources="{escape(source_text)}" data-decision="{escape(paper.decision)}" data-tags="{escape(tag_text)}" data-latest-run="{str(paper.newly_discovered_in_latest_run).lower()}" data-is-new="{str(paper.is_new).lower()}" data-published="{escape(paper.published_date or '')}" data-first-seen="{escape(paper.first_seen_date)}" data-score="{paper.score}" data-pinned="{str(paper.pinned).lower()}" data-future-date="{str(paper.future_date).lower()}" data-date-bucket="{_latest_relevant_date_bucket(paper)}" data-title="{escape(paper.title.lower())}" data-search="{escape(search_text)}"{hidden}>
      <div class="paper-main">
        <h3>{escape(paper.title)}{new_badge}</h3>
        <p class="meta">{escape(paper.authors_text)} · {escape(published)} · Source: {escape(source_names)}</p>
        <p class="reason"><strong>Why included:</strong> {escape(_short_reason(paper))}</p>
      </div>
      <div class="paper-side">
        {link}
        {detail_link}
        <details class="paper-more">
          <summary>Details</summary>
          <p class="abstract-summary">{escape(paper.abstract_summary)}</p>
          {note}
          <div class="details-group">
            <strong>Screening details</strong>
            <ul>
              <li>Decision: {escape(_decision_label(paper.decision))}</li>
              <li>Score: {paper.score}/100</li>
              <li>Classifier label: {escape(relevance_label)}</li>
              {pinned_detail}
              {status_detail}
            </ul>
          </div>
          <div class="details-group"><strong>Sources</strong><div class="tags">{source_badges}</div></div>
          <div class="details-group"><strong>Tags</strong><div class="tags">{details_tags}</div></div>
          <ul>
            <li>First seen by Paper Scout: {escape(first_seen_text)}</li>
            {more_items}
          </ul>
          {secondary_links}
          <p class="details-reason"><strong>Screening rationale</strong> {escape(paper.reason)}</p>
          <button class="citation-button" type="button" data-citation="{escape(paper.citation)}">Copy citation</button>
          <span class="copy-status" aria-live="polite"></span>
        </details>
      </div>
    </article>
    """


def _visible_tag_badges(tags: list[str], limit: int = 4) -> str:
    if not tags:
        return '<span class="badge tag">untagged</span>'
    visible = tags[:limit]
    badges = "".join(f'<span class="badge tag">{escape(tag)}</span>' for tag in visible)
    remaining = len(tags) - len(visible)
    if remaining > 0:
        badges += f'<span class="badge tag tag-more">+{remaining} more</span>'
    return badges


def _all_tag_badges(tags: list[str]) -> str:
    return "".join(f'<span class="badge tag">{escape(tag)}</span>' for tag in tags) or '<span class="badge tag">untagged</span>'


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


def _identifier_list(paper: LibraryPaper) -> list[str]:
    identifiers: list[str] = []
    if paper.doi:
        identifiers.append(f"DOI: {escape(paper.doi)}")
    if paper.arxiv_id:
        identifiers.append(f"arXiv: {escape(paper.arxiv_id)}")
    if paper.semantic_scholar_id:
        identifiers.append(f"Semantic Scholar: {escape(paper.semantic_scholar_id)}")
    if paper.openalex_id:
        identifiers.append(f"OpenAlex: {escape(paper.openalex_id)}")
    for source, values in paper.source_ids.items():
        if values:
            identifiers.append(f"{escape(_source_label(source))} IDs: {escape(', '.join(values))}")
    return _ordered_unique(identifiers)


def _ssrn_id(paper: LibraryPaper) -> str | None:
    candidates = [paper.doi or "", paper.url or "", *paper.alternate_urls]
    for candidate in candidates:
        match = re.search(r"(?:ssrn\.|abstract_id=)(\d+)", candidate, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


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
        <h3>{escape(paper.title)}</h3>
        <p class="meta">{escape(paper.authors)} · Published {escape(paper.date)} · Source: {escape(paper.source)}</p>
        <p class="reason"><strong>Why included:</strong> {escape(paper.reason)}</p>
      </div>
      <div class="paper-side">
        {link}
        <details class="paper-more">
          <summary>Details</summary>
          <p class="abstract-summary">{escape(paper.abstract_summary)}</p>
          <div class="details-group">
            <strong>Screening details</strong>
            <ul>
              <li>Decision: {escape(paper.decision)}</li>
              <li>Score: {escape(paper.score)}</li>
            </ul>
          </div>
          <div class="details-group"><strong>Tags</strong><div class="tags">{tags}</div></div>
        </details>
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
        "ssrn": "SSRN",
    }
    return labels.get(source, source)


def _decision_label(decision: str) -> str:
    return "Highly relevant" if decision == "relevant" else "Review candidate" if decision == "maybe" else decision


def _published_text(paper: LibraryPaper) -> str:
    precision = _publication_precision(paper)
    if precision == "year":
        year = paper.publication_year or _paper_year_from_value(paper.published_date)
        return f"Published date unavailable · Year: {year}" if year else "Publication date unavailable"
    if not paper.published_date:
        return "Publication date unavailable"
    if paper.future_date:
        return f"Date from source {paper.published_date}"
    if paper.publication_date_source == "ssrn":
        return f"Date written {paper.published_date}"
    return f"Published {paper.published_date}"


def _publication_precision(paper: LibraryPaper) -> str:
    return paper.publication_date_precision or publication_date(paper.published_date, paper.publication_date_source, paper.publication_year).precision


def _paper_year_from_value(value: object) -> str | None:
    match = re.match(r"(\d{4})", str(value or ""))
    return match.group(1) if match else None


def _date_confidence(precision: str | None, source: str | None) -> str | None:
    if not precision or precision == "unknown":
        return None
    if precision == "year":
        return "low"
    if source in {"arxiv", "ssrn"}:
        return "high"
    if source and source.startswith(("crossref-created", "crossref-deposited")):
        return "low"
    if source and source.startswith("crossref"):
        return "medium"
    return "medium"


def _short_reason(paper: LibraryPaper) -> str:
    reason = (paper.research_note or paper.reason).strip() or (paper.relevance_label or _relevance_label(paper))
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
            "publication_year",
            "publication_date_precision",
            "publication_date_source",
            "publication_date_confidence",
            "effective_sort_date",
        ],
        lineterminator="\n",
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
                "publication_year": paper.publication_year or "",
                "publication_date_precision": _publication_precision(paper),
                "publication_date_source": paper.publication_date_source or "",
                "publication_date_confidence": paper.publication_date_confidence or "",
                "effective_sort_date": _latest_relevant_date(paper) or "",
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


def _write_metadata_quality_report(report_dir: Path, report_date: str, papers: list[LibraryPaper]) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    year_only = [paper for paper in papers if _publication_precision(paper) == "year"]
    high_without_exact = [paper for paper in papers if paper.decision == "relevant" and precision_rank(_publication_precision(paper)) < precision_rank("day")]
    future_or_imprecise = [paper for paper in papers if paper.future_date or _publication_precision(paper) in {"year", "month"}]
    high_generic_reason = [
        paper
        for paper in papers
        if paper.decision == "relevant"
        and re.search(r"peripheral|does not clearly|mentions memory", paper.reason, flags=re.I)
    ]
    biological_terms = re.compile(r"protein synthesis|fear memory|neural inactivation|hippocampus|amygdala|animal memory|human cognitive|psychology|neuroscience", re.I)
    biological_high = [paper for paper in papers if paper.decision == "relevant" and biological_terms.search(" ".join([paper.title, paper.abstract_summary, paper.reason]))]
    maybe_core = [
        paper
        for paper in papers
        if paper.decision == "maybe"
        and re.search(r"agent[- ]native memory|llm agents?.{0,80}memory|memory systems?.{0,80}llm agents?|autonomous llm agents?.{0,80}memory", " ".join([paper.title, paper.abstract_summary]), flags=re.I)
    ]
    persistent_reason_without_memory = [
        paper
        for paper in papers
        if re.search(r"persistent or long[- ]term memory", paper.reason, flags=re.I)
        and not _has_explicit_agent_memory_evidence(paper)
    ]
    high_agentic_without_memory = [
        paper
        for paper in papers
        if paper.score >= 70
        and re.search(r"\bagentic ai\b|\bagentic artificial intelligence\b|\borchestration\b|\bexecution layers?\b", " ".join([paper.title, paper.abstract_summary]), flags=re.I)
        and not _has_explicit_agent_memory_evidence(paper)
    ]
    enrichment_warnings = [paper for paper in papers if paper.metadata_warnings]
    ssrn_or_doi_weak = [
        paper
        for paper in papers
        if precision_rank(_publication_precision(paper)) < precision_rank("day")
        and (
            (paper.url and "ssrn.com" in paper.url)
            or (paper.doi and paper.doi.lower().startswith("10.2139/ssrn."))
            or any("ssrn.com" in url for url in paper.alternate_urls)
        )
    ]
    first_seen_sort_fallback = [
        paper
        for paper in papers
        if _latest_relevant_date(paper) == paper.first_seen_date and _publication_precision(paper) in {"unknown", "year"}
    ]
    low_confidence_dates = [
        paper
        for paper in papers
        if paper.publication_date_confidence == "low"
        or (paper.publication_date_source or "").startswith(("crossref-created", "crossref-deposited"))
    ]
    lines = [
        f"# Paper Scout Metadata Quality - {report_date}",
        "",
        f"- **Year-only publication dates:** {len(year_only)}",
        f"- **SSRN/DOI date enrichment warnings:** {len(enrichment_warnings)}",
        f"- **SSRN/DOI papers still without exact dates:** {len(ssrn_or_doi_weak)}",
        f"- **First-seen sort fallbacks:** {len(first_seen_sort_fallback)}",
        f"- **Low-confidence date fields:** {len(low_confidence_dates)}",
        f"- **Highly relevant without exact date:** {len(high_without_exact)}",
        f"- **Biological/cognitive high-relevance risks:** {len(biological_high)}",
        f"- **Highly relevant with generic/peripheral reasons:** {len(high_generic_reason)}",
        f"- **Persistent-memory reason without explicit memory evidence:** {len(persistent_reason_without_memory)}",
        f"- **High-scoring agentic-AI papers without explicit memory evidence:** {len(high_agentic_without_memory)}",
        f"- **Maybe papers with core memory phrases:** {len(maybe_core)}",
        f"- **Future or imprecise source dates:** {len(future_or_imprecise)}",
        "",
    ]
    sections = [
        ("Year-Only Publication Dates", year_only),
        ("SSRN/DOI Date Enrichment Warnings", enrichment_warnings),
        ("SSRN/DOI Papers Still Without Exact Dates", ssrn_or_doi_weak),
        ("First-Seen Sort Fallbacks", first_seen_sort_fallback),
        ("Low-Confidence Date Fields", low_confidence_dates),
        ("Highly Relevant Without Exact Date", high_without_exact),
        ("Biological/Cognitive High-Relevance Risks", biological_high),
        ("Highly Relevant With Generic Reasons", high_generic_reason),
        ("Persistent-Memory Reasons Without Explicit Memory Evidence", persistent_reason_without_memory),
        ("High-Scoring Agentic-AI Papers Without Explicit Memory Evidence", high_agentic_without_memory),
        ("Maybe Papers With Core Memory Phrases", maybe_core),
        ("Future Or Imprecise Source Dates", future_or_imprecise),
    ]
    for title, items in sections:
        lines.extend([f"## {title}", ""])
        if not items:
            lines.extend(["- None", ""])
            continue
        for paper in items[:50]:
            date_text = paper.published_date or "unknown"
            lines.append(f"- **{paper.title}** — {paper.decision}, {date_text}, precision={_publication_precision(paper)}, source={paper.publication_date_source or 'unknown'}")
            for warning in paper.metadata_warnings[:3]:
                lines.append(f"  - {warning}")
        lines.append("")
    (report_dir / f"metadata-quality-{report_date}.md").write_text("\n".join(lines), encoding="utf-8")


def _has_explicit_agent_memory_evidence(paper: LibraryPaper) -> bool:
    text = " ".join([paper.title, paper.abstract_summary, paper.reason, " ".join(paper.tags)]).lower()
    patterns = [
        r"\bagent[- ]native memory\b",
        r"\bagent memory\b",
        r"\bmemory systems?\b",
        r"\bmemory modules?\b",
        r"\bpersistent memory\b",
        r"\blong[- ]term memory\b",
        r"\b(episodic|semantic|procedural) memory\b",
        r"\bmemory (storage|retrieval|update|consolidation|governance|policy|benchmark|evaluation)\b",
        r"\bshared memory\b",
        r"\bparametric memory\b",
        r"\bengram\b",
    ]
    return any(re.search(pattern, text) for pattern in patterns)


def _bibtex_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


STYLE_CSS = """
:root {
  color-scheme: light;
  --bg: #f5f5f7;
  --surface: #ffffff;
  --surface-soft: #fbfbfd;
  --surface-muted: #f1f3f6;
  --text: #1d1d1f;
  --muted: #5f6369;
  --faint: #7b8088;
  --line: #d9dde4;
  --line-soft: #e8ebf0;
  --accent: #1769d2;
  --accent-strong: #0a4fa8;
  --accent-soft: #edf5ff;
  --success-soft: #edf8f2;
  --success-text: #25684a;
  --warning-soft: #fff7e8;
  --warning-text: #805a1d;
  --shadow: rgba(28, 35, 48, .08);
  --radius-lg: 1.35rem;
  --radius-md: .95rem;
  --radius-sm: .65rem;
  --font-sans: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", sans-serif;
  --font-mono: "SFMono-Regular", ui-monospace, Menlo, Monaco, Consolas, monospace;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: linear-gradient(180deg, #fbfbfd 0%, var(--bg) 28rem);
  color: var(--text);
  font: 16px/1.58 var(--font-sans);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(circle at 50% -12rem, rgba(23, 105, 210, .08), transparent 34rem);
}
a {
  color: var(--accent-strong);
  text-decoration-thickness: .08em;
  text-underline-offset: .18em;
}
a:hover { color: var(--accent); }
button, input, textarea, select { font: inherit; }
button, a, input, summary, textarea, select {
  transition: background-color .18s ease, border-color .18s ease, color .18s ease, box-shadow .18s ease, transform .18s ease;
}
button:focus-visible, a:focus-visible, input:focus-visible, summary:focus-visible, textarea:focus-visible, select:focus-visible {
  outline: 3px solid rgba(23, 105, 210, .26);
  outline-offset: 3px;
}
.skip-link {
  position: absolute;
  left: 1rem;
  top: .75rem;
  z-index: 2;
  transform: translateY(-160%);
  background: var(--text);
  color: var(--surface);
  padding: .55rem .8rem;
  border-radius: var(--radius-sm);
}
.skip-link:focus { transform: translateY(0); }
.page {
  width: min(1040px, calc(100% - 40px));
  margin: 0 auto;
  padding: 28px 0 68px;
}
.top-nav {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
  padding-bottom: 1.75rem;
}
.brand {
  color: var(--text);
  font-weight: 650;
  text-decoration: none;
  letter-spacing: -.01em;
}
.nav-links { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: flex-end; }
.nav-links a {
  color: var(--muted);
  font-size: .94rem;
  font-weight: 520;
  text-decoration: none;
}
.nav-links a:hover { color: var(--accent-strong); }
.briefing-hero, .archive-hero { padding: .8rem 0 2rem; }
.library-hero {
  max-width: 48rem;
  padding: 1.2rem 0 .8rem;
}
.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(220px, 280px);
  gap: clamp(1.5rem, 4vw, 3.25rem);
  align-items: end;
}
.eyebrow, .section-kicker, .summary-strip span, .control-group > span, .search-field span, .select-field span {
  margin: 0;
  color: var(--faint);
  font-size: .78rem;
  font-weight: 650;
  letter-spacing: .04em;
  text-transform: uppercase;
}
h1, h2, h3 { margin: 0; text-wrap: balance; }
h1 {
  max-width: 15ch;
  font-size: clamp(2.85rem, 6vw, 5.35rem);
  line-height: .92;
  letter-spacing: -.045em;
  font-weight: 720;
}
.archive-hero h1 { max-width: 15ch; font-size: clamp(2.7rem, 5.6vw, 4.8rem); }
.library-hero h1 {
  max-width: 14ch;
  font-size: clamp(3rem, 6vw, 5.6rem);
}
h2 {
  font-size: clamp(1.7rem, 3vw, 2.45rem);
  line-height: 1.05;
  letter-spacing: -.03em;
  font-weight: 690;
}
h3 {
  font-size: clamp(1.18rem, 1.8vw, 1.55rem);
  line-height: 1.2;
  letter-spacing: -.018em;
  font-weight: 650;
}
.hero-copy {
  max-width: 38rem;
  margin: 1.15rem 0 0;
  color: var(--muted);
  font-size: clamp(1.05rem, 2vw, 1.22rem);
  line-height: 1.55;
  text-wrap: pretty;
}
.hero-actions { display: flex; flex-wrap: wrap; gap: .7rem; margin-top: 1.55rem; }
.hero-line {
  margin: 1rem 0 0;
  color: var(--faint);
  font-family: var(--font-mono);
  font-size: .9rem;
  line-height: 1.6;
  font-variant-numeric: tabular-nums;
  overflow-wrap: anywhere;
}
.button, .paper-link, .citation-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.55rem;
  border-radius: 999px;
  padding: .66rem .95rem;
  font-size: .93rem;
  font-weight: 620;
  text-decoration: none;
}
.button.primary, .paper-link {
  background: var(--accent);
  color: #fff;
  box-shadow: 0 10px 24px rgba(23, 105, 210, .18);
}
.paper-detail-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.35rem;
  border: 1px solid var(--line-soft);
  border-radius: 999px;
  padding: .56rem .86rem;
  background: rgba(255, 255, 255, .72);
  color: var(--accent-strong);
  font-size: .9rem;
  font-weight: 610;
  text-decoration: none;
}
.button.secondary {
  background: rgba(255, 255, 255, .74);
  border: 1px solid var(--line-soft);
  color: var(--accent-strong);
}
.button:hover, .paper-link:hover, .paper-detail-link:hover { transform: translateY(-1px); }
.button:active, .paper-link:active, .paper-detail-link:active, button:active { transform: translateY(1px); }
.digest-note {
  background: rgba(255, 255, 255, .78);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-lg);
  box-shadow: 0 16px 40px var(--shadow);
  padding: 1.15rem;
}
.digest-note span, .digest-note a {
  display: block;
}
.digest-note span { color: var(--faint); font-size: .82rem; font-weight: 600; }
.digest-note strong {
  display: block;
  margin: .2rem 0 .75rem;
  font-family: var(--font-mono);
  font-size: 1.45rem;
  font-variant-numeric: tabular-nums;
}
.recommended-section {
  margin-top: 1.5rem;
  padding: 1.35rem;
  background: rgba(255, 255, 255, .64);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-lg);
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
  background: var(--surface);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-md);
  box-shadow: 0 14px 34px var(--shadow);
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
  padding: .8rem .9rem;
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, .72);
}
.export-strip span {
  color: var(--muted);
  font-weight: 620;
  margin-right: .25rem;
}
.export-strip a {
  padding: .38rem .58rem;
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  color: var(--accent-strong);
  text-decoration: none;
  font-size: .88rem;
  font-weight: 600;
}
.summary-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(7rem, 1fr));
  gap: 0;
  margin: 1.45rem 0 1.2rem;
  background: rgba(255, 255, 255, .86);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 16px 44px var(--shadow);
}
.summary-strip div { padding: .95rem 1rem; border-left: 1px solid var(--line-soft); }
.summary-strip div:first-child { border-left: 0; }
.summary-strip strong {
  display: block;
  margin-top: .15rem;
  font-family: var(--font-mono);
  font-size: 1.05rem;
  font-variant-numeric: tabular-nums;
}
.summary-strip .source-summary {
  grid-column: 1 / -1;
  border-left: 0;
  border-top: 1px solid var(--line-soft);
}
.summary-strip .source-summary strong {
  font-size: .98rem;
  font-weight: 560;
}
.reading-controls {
  display: grid;
  grid-template-columns: minmax(18rem, 1fr) minmax(10rem, .38fr) minmax(11rem, .44fr) max-content;
  gap: .8rem;
  align-items: end;
  margin: .9rem 0 1.65rem;
  padding: .85rem;
  background: rgba(255, 255, 255, .78);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-lg);
  box-shadow: 0 14px 38px rgba(28, 35, 48, .055);
}
.search-field, .select-field, .control-group { display: grid; gap: .45rem; }
input[type="search"], select {
  width: 100%;
  min-height: 2.8rem;
  border: 1px solid var(--line);
  border-radius: .8rem;
  background: var(--surface);
  color: var(--text);
  padding: .72rem .86rem;
  font-size: .96rem;
}
select {
  appearance: none;
  background-image: linear-gradient(45deg, transparent 50%, var(--faint) 50%), linear-gradient(135deg, var(--faint) 50%, transparent 50%);
  background-position: calc(100% - 18px) 50%, calc(100% - 13px) 50%;
  background-size: 5px 5px, 5px 5px;
  background-repeat: no-repeat;
  padding-right: 2rem;
}
input[type="search"]::placeholder { color: var(--faint); }
.segmented, .source-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: .35rem;
}
button {
  border: 1px solid var(--line-soft);
  background: var(--surface);
  color: var(--muted);
  border-radius: 999px;
  padding: .56rem .78rem;
  font-size: .88rem;
  font-weight: 580;
  cursor: pointer;
}
button:hover { border-color: var(--line); color: var(--text); background: var(--surface-soft); }
button.active { background: var(--text); border-color: var(--text); color: #fff; }
.toggle-control {
  display: inline-flex;
  gap: .55rem;
  align-items: center;
  min-height: 2.75rem;
  padding: .58rem .72rem;
  border: 1px solid var(--line-soft);
  border-radius: .85rem;
  background: var(--surface);
  color: var(--muted);
  font-size: .88rem;
  font-weight: 580;
}
.toggle-control input { accent-color: var(--accent); }
.tag-filter { min-width: 12rem; }
.tag-filter span { color: var(--faint); }
.sources { grid-column: 1 / -1; }
.paper-section { margin-top: 2.2rem; }
.section-heading {
  max-width: 44rem;
  margin-bottom: 1.05rem;
}
.section-heading p:not(.section-kicker) {
  margin: .7rem 0 0;
  color: var(--muted);
  font-size: 1rem;
}
.paper-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(8rem, 9.75rem);
  gap: clamp(1rem, 2.2vw, 1.55rem);
  margin: .72rem 0;
  padding: clamp(1rem, 1.8vw, 1.25rem);
  background: rgba(255, 255, 255, .92);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-lg);
  box-shadow: 0 14px 40px rgba(28, 35, 48, .055);
}
.paper-card.primary { border-color: rgba(23, 105, 210, .2); }
.paper-card.compact {
  background: rgba(255, 255, 255, .66);
  box-shadow: none;
  border-color: var(--line-soft);
  padding-top: 1rem;
  padding-bottom: 1rem;
  opacity: .78;
}
.paper-card.compact h3 {
  font-size: clamp(1.08rem, 1.5vw, 1.32rem);
}
.paper-kicker, .tags { display: flex; gap: .45rem; flex-wrap: wrap; align-items: center; }
.paper-card h3 {
  display: flex;
  align-items: baseline;
  gap: .5rem;
  flex-wrap: wrap;
  margin-top: .55rem;
  font-size: clamp(1.16rem, 1.65vw, 1.46rem);
  overflow-wrap: anywhere;
}
.meta, .empty {
  color: var(--muted);
}
.meta { margin: .55rem 0 0; font-size: .95rem; }
.paper-dates {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, max-content));
  gap: .6rem 1rem;
  margin: .85rem 0 0;
}
.paper-dates div {
  padding: .52rem .62rem;
  background: var(--surface-soft);
  border: 1px solid var(--line-soft);
  border-radius: .72rem;
}
.paper-dates dt {
  color: var(--faint);
  font-size: .72rem;
  font-weight: 650;
}
.paper-dates dd {
  margin: .12rem 0 0;
  font-family: var(--font-mono);
  font-size: .9rem;
  font-weight: 650;
  font-variant-numeric: tabular-nums;
}
.reason {
  max-width: 68ch;
  margin: .55rem 0 0;
  padding: 0;
  border-left: 0;
  background: transparent;
  color: #334155;
  font-weight: 560;
}
.relevance-label {
  display: inline-flex;
  width: fit-content;
  margin: .65rem 0 0;
  padding: .28rem .55rem;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-strong);
  font-size: .82rem;
  font-weight: 650;
}
.research-note {
  margin: .85rem 0 0;
  padding: .75rem .85rem;
  border: 1px dashed var(--line);
  border-radius: var(--radius-sm);
  background: var(--surface-soft);
  color: var(--muted);
}
.research-note strong {
  display: block;
  color: var(--accent-strong);
  font-size: .78rem;
  text-transform: uppercase;
  letter-spacing: .05em;
}
.abstract-summary {
  max-width: 67ch;
  margin: .75rem 0;
  color: #383c43;
  text-wrap: pretty;
}
.badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: .2rem .5rem;
  border: 1px solid var(--line-soft);
  font-size: .76rem;
  font-weight: 620;
}
.source { background: var(--accent-soft); color: var(--accent-strong); border-color: #d5e8ff; }
.relevance { background: var(--warning-soft); color: var(--warning-text); border-color: #f3dfb9; }
.latest { background: var(--success-soft); color: var(--success-text); border-color: #cfe9dc; }
.pinned { background: #f2f0ff; color: #514a93; border-color: #ddd9ff; }
.review { background: #f4f4f6; color: #4f5560; border-color: var(--line-soft); }
.tag { background: #f4f5f7; color: #555b64; }
.new-badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: .16rem .42rem;
  border: 1px solid #cfe1f7;
  background: #eef6ff;
  color: #1e5f9f;
  font-size: .72rem;
  font-weight: 680;
  letter-spacing: .01em;
  vertical-align: middle;
}
.tags { margin-top: .65rem; }
.tag-more { color: var(--faint); }
.paper-side {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: .6rem;
}
.paper-link.disabled {
  background: var(--surface-muted);
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
  border: 1px solid var(--line-soft);
  border-radius: 999px;
  background: var(--surface);
  color: var(--accent-strong);
  font-size: .82rem;
  font-weight: 600;
  text-decoration: none;
}
.citation-button {
  border: 1px solid var(--line);
  background: var(--surface-soft);
  color: var(--accent-strong);
  cursor: pointer;
}
.paper-more {
  color: var(--muted);
  font-size: .84rem;
}
.paper-more summary {
  cursor: pointer;
  color: var(--faint);
  font-weight: 620;
}
.paper-more ul {
  margin: .55rem 0;
  padding-left: 1rem;
}
.details-group {
  margin: .75rem 0;
}
.details-group strong, .details-reason strong {
  display: block;
  color: var(--text);
  margin-bottom: .25rem;
  font-weight: 650;
}
.details-reason {
  margin: .75rem 0;
}
.citation-button:hover {
  background: var(--surface);
  border-color: var(--accent);
}
.copy-status {
  min-height: 1.2rem;
  color: var(--faint);
  font-size: .78rem;
}
.paper-detail-hero {
  margin-bottom: 2rem;
}
.paper-detail-actions {
  display: flex;
  flex-wrap: wrap;
  gap: .65rem;
  margin-top: 1.35rem;
}
.paper-detail-layout {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}
.detail-panel {
  background: rgba(255, 255, 255, .82);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-md);
  padding: 1rem;
}
.detail-panel.wide {
  grid-column: 1 / -1;
}
.detail-panel p {
  margin: .35rem 0 0;
}
.detail-panel ul {
  margin: .55rem 0 0;
  padding-left: 1.1rem;
  color: var(--muted);
}
.detail-metadata {
  display: grid;
  gap: .55rem;
  margin: .5rem 0 0;
}
.detail-metadata div {
  display: grid;
  grid-template-columns: minmax(8rem, .65fr) 1fr;
  gap: .75rem;
  border-top: 1px solid var(--line-soft);
  padding-top: .55rem;
}
.detail-metadata dt {
  color: var(--faint);
  font-size: .84rem;
}
.detail-metadata dd {
  margin: 0;
  color: var(--text);
}
.structured-card-fields .structured-provenance {
  grid-column: 2;
  color: var(--faint);
  font-size: .8rem;
}
.structured-empty, .muted {
  color: var(--faint);
}
.citation summary {
  cursor: pointer;
  color: var(--muted);
  font-size: .88rem;
  font-weight: 600;
}
textarea {
  width: 100%;
  min-height: 6rem;
  margin-top: .55rem;
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
  background: var(--surface-soft);
  color: var(--text);
  padding: .7rem;
  resize: vertical;
}
.source-diagnostics {
  margin: 2.6rem 0 0;
  padding: .9rem 1rem;
  background: rgba(255, 255, 255, .58);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-md);
  color: var(--muted);
}
.library-footer {
  display: grid;
  gap: .8rem;
  margin-top: 2.4rem;
  padding-top: 1.2rem;
  border-top: 1px solid var(--line);
}
.export-library, .technical-diagnostics {
  padding: .8rem .9rem;
  background: rgba(255, 255, 255, .58);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-md);
  color: var(--muted);
}
.export-library summary, .technical-diagnostics summary {
  cursor: pointer;
  color: var(--text);
  font-weight: 650;
}
.diagnostic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
  gap: 1rem;
  margin-top: .85rem;
}
.diagnostic-grid h3 {
  font-size: 1rem;
  letter-spacing: 0;
}
.diagnostic-grid p, .diagnostic-grid ul {
  margin: .35rem 0 0;
}
.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: .55rem;
}
.footer-links a {
  padding: .38rem .55rem;
  border: 1px solid var(--line-soft);
  border-radius: 999px;
  background: rgba(255, 255, 255, .68);
  color: var(--accent-strong);
  font-size: .86rem;
  font-weight: 600;
  text-decoration: none;
}
.source-diagnostics summary {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  font-weight: 650;
  color: var(--text);
}
.source-diagnostics summary span {
  color: var(--faint);
  font-size: .9rem;
  font-weight: 560;
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
  border: 1px solid var(--line-soft);
  border-radius: 999px;
  background: rgba(255, 255, 255, .68);
  color: var(--accent-strong);
  font-family: var(--font-mono);
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
  background: rgba(255, 255, 255, .74);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-md);
}
.archive-entry a {
  font-family: var(--font-mono);
  font-size: 1.1rem;
  font-weight: 650;
  text-decoration: none;
}
.archive-entry p {
  margin: .35rem 0 0;
  color: var(--muted);
}
.archive-entry dl {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: .55rem;
  margin: 0;
}
.archive-entry dl div {
  padding: .65rem;
  background: var(--surface);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-sm);
}
.archive-entry dt {
  color: var(--faint);
  font-size: .75rem;
  font-weight: 650;
}
.archive-entry dd {
  margin: .15rem 0 0;
  font-family: var(--font-mono);
  font-size: 1.2rem;
  font-weight: 650;
}
.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
  gap: 1rem;
  margin-top: 1.6rem;
}
.about-grid article {
  padding: 1.15rem;
  background: rgba(255, 255, 255, .74);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius-md);
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
  .page { width: calc(100% - 24px); padding-top: 18px; }
  .top-nav, .hero-grid, .paper-card, .archive-strip, .archive-entry { grid-template-columns: 1fr; }
  .top-nav { align-items: flex-start; flex-direction: column; gap: .75rem; }
  .nav-links { justify-content: flex-start; }
  .library-hero { padding-top: .6rem; }
  .summary-strip { grid-template-columns: repeat(2, 1fr); }
  .summary-strip div:nth-child(odd) { border-left: 0; }
  .reading-controls { grid-template-columns: 1fr; }
  .recommended-section { padding: .9rem; }
  .paper-dates { grid-template-columns: 1fr; }
  .paper-card { border-radius: 1rem; }
  .paper-detail-layout, .detail-metadata div { grid-template-columns: 1fr; }
  .archive-entry dl { grid-template-columns: 1fr; }
  h1 { font-size: clamp(2.7rem, 14vw, 4.35rem); }
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
  const relevanceFilter = document.querySelector('#relevance-filter');
  const newOnly = document.querySelector('#new-only');
  const sortSelect = document.querySelector('#paper-sort');
  const list = document.querySelector('#paper-list');
  const cards = Array.from(document.querySelectorAll('.paper-card'));
  const emptyState = document.querySelector('#no-results');
  let decision = relevanceFilter ? relevanceFilter.value : 'all';
  function sortableDate(card, attr) {
    const value = card.dataset[attr] || '';
    return /^\\d{4}-\\d{2}-\\d{2}/.test(value) ? value : (card.dataset.firstSeen || '');
  }
  function latestRelevantDate(card) {
    return card.dataset.futureDate === 'true'
      ? sortableDate(card, 'firstSeen')
      : sortableDate(card, 'published');
  }
  function latestRelevantRank(a, b) {
    const newness = (a.dataset.isNew === 'true' ? 0 : 1) - (b.dataset.isNew === 'true' ? 0 : 1);
    if (newness) return newness;
    const rel = (a.dataset.decision === 'relevant' ? 0 : 1) - (b.dataset.decision === 'relevant' ? 0 : 1);
    if (rel) return rel;
    const bucket = Number(a.dataset.dateBucket || 1) - Number(b.dataset.dateBucket || 1);
    if (bucket) return bucket;
    const date = latestRelevantDate(b).localeCompare(latestRelevantDate(a));
    if (date) return date;
    const score = Number(b.dataset.score || 0) - Number(a.dataset.score || 0);
    if (score) return score;
    return a.dataset.title.localeCompare(b.dataset.title);
  }
  function sortCards() {
    if (!list || !sortSelect) return;
    const mode = sortSelect.value || 'latest-relevant';
    const sorted = [...cards].sort((a, b) => {
      if (mode === 'latest-relevant') return latestRelevantRank(a, b);
      if (mode === 'first-seen-desc') return sortableDate(b, 'firstSeen').localeCompare(sortableDate(a, 'firstSeen')) || b.dataset.score - a.dataset.score;
      if (mode === 'score-desc') return Number(b.dataset.score || 0) - Number(a.dataset.score || 0) || a.dataset.title.localeCompare(b.dataset.title);
      if (mode === 'title-asc') return a.dataset.title.localeCompare(b.dataset.title);
      if (mode === 'published-desc') return sortableDate(b, 'published').localeCompare(sortableDate(a, 'published')) || b.dataset.score - a.dataset.score;
      return latestRelevantRank(a, b);
    });
    for (const card of sorted) {
      list.appendChild(card);
    }
  }
  function update() {
    const query = (search.value || '').toLowerCase();
    let visibleCount = 0;
    for (const card of cards) {
      const matchesQuery = !query || card.dataset.search.includes(query);
      const matchesDecision = decision === 'all' || card.dataset.decision === decision;
      const matchesNewOnly = !newOnly || !newOnly.checked || card.dataset.isNew === 'true';
      card.hidden = !(matchesQuery && matchesDecision && matchesNewOnly);
      if (!card.hidden) visibleCount += 1;
    }
    if (emptyState) emptyState.hidden = visibleCount > 0;
  }
  if (search) search.addEventListener('input', update);
  if (relevanceFilter) relevanceFilter.addEventListener('change', () => { decision = relevanceFilter.value || 'all'; update(); });
  if (newOnly) newOnly.addEventListener('change', update);
  if (sortSelect) sortSelect.addEventListener('change', () => { sortCards(); update(); });
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
