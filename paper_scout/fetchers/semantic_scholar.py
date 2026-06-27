from __future__ import annotations

import json
import os
import re
from datetime import date, timedelta

from paper_scout.deduplication import normalize_arxiv_id
from paper_scout.dates import publication_date
from paper_scout.fetchers.arxiv import parse_arxiv_feed
from paper_scout.http import HttpClient
from paper_scout.models import PaperCandidate, SourceFetchResult


class SemanticScholarFetcher:
    source = "semantic_scholar"

    def __init__(self, http: HttpClient | None = None) -> None:
        self.http = http or HttpClient()

    def search(self, term: str, days: int, max_results: int) -> list[PaperCandidate]:
        return self.search_with_diagnostics(term, days, max_results).candidates

    def search_with_diagnostics(self, term: str, days: int, max_results: int) -> SourceFetchResult:
        headers = {}
        if os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
            headers["x-api-key"] = os.environ["SEMANTIC_SCHOLAR_API_KEY"]
        params = {
            "query": term,
            "limit": max_results,
            "fields": "paperId,title,abstract,url,year,publicationDate,authors,externalIds",
        }
        payload = self.http.get_text("https://api.semanticscholar.org/graph/v1/paper/search", params=params, headers=headers)
        cutoff = date.today() - timedelta(days=days)
        papers = _enrich_year_only_arxiv_papers(parse_semantic_scholar_results(payload), self.http)
        return SourceFetchResult(raw_count=_raw_record_count(payload), candidates=[paper for paper in papers if _is_recent(paper, cutoff)])


def parse_semantic_scholar_results(json_text: str) -> list[PaperCandidate]:
    payload = json.loads(json_text)
    papers: list[PaperCandidate] = []
    for item in payload.get("data", []):
        external = item.get("externalIds") or {}
        paper_id = item.get("paperId") or ""
        arxiv_id = _arxiv_id_from_semantic_item(item, external)
        published = publication_date(item.get("publicationDate") or (str(item["year"]) if item.get("year") else None), "semantic_scholar", item.get("year"))
        papers.append(
            PaperCandidate(
                title=item.get("title") or "",
                authors=[author.get("name", "") for author in item.get("authors", []) if author.get("name")],
                abstract=item.get("abstract") or "",
                source="semantic_scholar",
                source_id=paper_id,
                doi=external.get("DOI"),
                arxiv_id=arxiv_id,
                semantic_scholar_id=paper_id or None,
                url=item.get("url"),
                published_date=published.value,
                publication_year=published.year,
                publication_date_precision=published.precision,
                publication_date_source=published.source,
                raw=item,
            )
        )
    return papers


def _enrich_year_only_arxiv_papers(papers: list[PaperCandidate], http: HttpClient) -> list[PaperCandidate]:
    enriched: list[PaperCandidate] = []
    for paper in papers:
        if paper.publication_date_precision != "year" or not paper.arxiv_id:
            enriched.append(paper)
            continue
        try:
            payload = http.get_text("https://export.arxiv.org/api/query", params={"id_list": paper.arxiv_id, "max_results": 1})
            arxiv_papers = parse_arxiv_feed(payload)
        except Exception:
            enriched.append(paper)
            continue
        arxiv_match = next((candidate for candidate in arxiv_papers if candidate.arxiv_id == paper.arxiv_id), None)
        if not arxiv_match or arxiv_match.publication_date_precision != "day":
            enriched.append(paper)
            continue
        raw = {**paper.raw, "enriched_sources": sorted({*paper.raw.get("enriched_sources", []), "arxiv"})}
        enriched.append(
            PaperCandidate(
                **{
                    **paper.__dict__,
                    "published_date": arxiv_match.published_date,
                    "publication_year": arxiv_match.publication_year or paper.publication_year,
                    "publication_date_precision": arxiv_match.publication_date_precision,
                    "publication_date_source": "arxiv",
                    "updated_date": arxiv_match.updated_date or paper.updated_date,
                    "url": paper.url or arxiv_match.url,
                    "raw": raw,
                }
            )
        )
    return enriched


def _arxiv_id_from_semantic_item(item: dict[str, object], external: dict[str, object]) -> str | None:
    values = [
        external.get("ArXiv"),
        external.get("ARXIV"),
        external.get("DOI"),
        item.get("url"),
    ]
    for value in values:
        arxiv_id = _arxiv_id_from_text(str(value or ""))
        if arxiv_id:
            return arxiv_id
    return None


def _arxiv_id_from_text(value: str) -> str | None:
    if not value:
        return None
    doi_match = re.search(r"10\.48550/arxiv\.([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", value, flags=re.I)
    if doi_match:
        return normalize_arxiv_id(doi_match.group(1))
    url_match = re.search(r"arxiv\.org/(?:abs|pdf)/([^?#\s]+)", value, flags=re.I)
    if url_match:
        return normalize_arxiv_id(url_match.group(1))
    return normalize_arxiv_id(value) if re.fullmatch(r"(arxiv:)?[0-9]{4}\.[0-9]{4,5}(v\d+)?", value, flags=re.I) else None


def _raw_record_count(json_text: str) -> int:
    payload = json.loads(json_text)
    return len(payload.get("data", []))


def _is_recent(paper: PaperCandidate, cutoff: date) -> bool:
    value = paper.published_date
    if not value:
        return True
    if len(value) == 4:
        return int(value) >= cutoff.year
    try:
        return date.fromisoformat(value[:10]) >= cutoff
    except ValueError:
        return True
