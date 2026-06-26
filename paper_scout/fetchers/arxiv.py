from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from datetime import date, timedelta

from paper_scout.deduplication import normalize_arxiv_id
from paper_scout.http import HttpClient
from paper_scout.models import PaperCandidate, SourceFetchResult

LOGGER = logging.getLogger(__name__)
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"


class ArxivFetcher:
    source = "arxiv"

    def __init__(self, http: HttpClient | None = None) -> None:
        self.http = http or HttpClient(pause_seconds=3.0)

    def search(self, term: str, days: int, max_results: int) -> list[PaperCandidate]:
        return self.search_with_diagnostics(term, days, max_results).candidates

    def search_with_diagnostics(self, term: str, days: int, max_results: int) -> SourceFetchResult:
        params = {
            "search_query": f'all:"{term}"',
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        payload = self.http.get_text("https://export.arxiv.org/api/query", params=params)
        cutoff = date.today() - timedelta(days=days)
        papers = parse_arxiv_feed(payload)
        return SourceFetchResult(raw_count=_raw_entry_count(payload), candidates=[paper for paper in papers if _is_recent(paper, cutoff)])


def parse_arxiv_feed(xml_text: str) -> list[PaperCandidate]:
    root = ET.fromstring(xml_text)
    papers: list[PaperCandidate] = []
    for entry in root.findall(f"{ATOM}entry"):
        entry_id = _text(entry, f"{ATOM}id") or ""
        arxiv_id = normalize_arxiv_id(entry_id)
        authors = [_clean_text(author.findtext(f"{ATOM}name") or "") for author in entry.findall(f"{ATOM}author")]
        doi = _text(entry, f"{ARXIV}doi")
        url = _alternate_link(entry) or (f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else entry_id)
        papers.append(
            PaperCandidate(
                title=_clean_text(_text(entry, f"{ATOM}title") or ""),
                authors=[author for author in authors if author],
                abstract=_clean_text(_text(entry, f"{ATOM}summary") or ""),
                source="arxiv",
                source_id=arxiv_id or entry_id,
                doi=doi,
                arxiv_id=arxiv_id,
                url=url,
                published_date=_date_part(_text(entry, f"{ATOM}published")),
                updated_date=_date_part(_text(entry, f"{ATOM}updated")),
                raw={"entry_id": entry_id},
            )
        )
    return papers


def _raw_entry_count(xml_text: str) -> int:
    root = ET.fromstring(xml_text)
    return len(root.findall(f"{ATOM}entry"))


def _alternate_link(entry: ET.Element) -> str | None:
    for link in entry.findall(f"{ATOM}link"):
        if link.attrib.get("rel") == "alternate" and link.attrib.get("href"):
            return link.attrib["href"]
    return None


def _text(entry: ET.Element, name: str) -> str | None:
    value = entry.findtext(name)
    return value.strip() if value else None


def _clean_text(text: str) -> str:
    return " ".join(text.split())


def _date_part(value: str | None) -> str | None:
    return value[:10] if value else None


def _is_recent(paper: PaperCandidate, cutoff: date) -> bool:
    value = paper.published_date or paper.updated_date
    if not value:
        return True
    try:
        return date.fromisoformat(value[:10]) >= cutoff
    except ValueError:
        LOGGER.debug("Could not parse arXiv date %s", value)
        return True
