from __future__ import annotations

import json
import os
from datetime import date, timedelta

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
        papers = parse_semantic_scholar_results(payload)
        return SourceFetchResult(raw_count=_raw_record_count(payload), candidates=[paper for paper in papers if _is_recent(paper, cutoff)])


def parse_semantic_scholar_results(json_text: str) -> list[PaperCandidate]:
    payload = json.loads(json_text)
    papers: list[PaperCandidate] = []
    for item in payload.get("data", []):
        external = item.get("externalIds") or {}
        paper_id = item.get("paperId") or ""
        papers.append(
            PaperCandidate(
                title=item.get("title") or "",
                authors=[author.get("name", "") for author in item.get("authors", []) if author.get("name")],
                abstract=item.get("abstract") or "",
                source="semantic_scholar",
                source_id=paper_id,
                doi=external.get("DOI"),
                arxiv_id=external.get("ArXiv"),
                semantic_scholar_id=paper_id or None,
                url=item.get("url"),
                published_date=item.get("publicationDate") or (str(item["year"]) if item.get("year") else None),
                raw=item,
            )
        )
    return papers


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
