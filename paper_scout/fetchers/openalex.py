from __future__ import annotations

import json
import os
from datetime import date, timedelta

from paper_scout.deduplication import normalize_doi, normalize_openalex_id
from paper_scout.http import HttpClient
from paper_scout.models import PaperCandidate, SourceFetchResult


class OpenAlexFetcher:
    source = "openalex"

    def __init__(self, http: HttpClient | None = None) -> None:
        self.http = http or HttpClient()

    def search(self, term: str, days: int, max_results: int) -> list[PaperCandidate]:
        return self.search_with_diagnostics(term, days, max_results).candidates

    def search_with_diagnostics(self, term: str, days: int, max_results: int) -> SourceFetchResult:
        cutoff = date.today() - timedelta(days=days)
        params: dict[str, str | int] = {
            "search": term,
            "filter": f"from_publication_date:{cutoff.isoformat()}",
            "per-page": max_results,
        }
        if os.environ.get("OPENALEX_MAILTO"):
            params["mailto"] = os.environ["OPENALEX_MAILTO"]
        payload = self.http.get_text("https://api.openalex.org/works", params=params)
        return SourceFetchResult(raw_count=_raw_record_count(payload), candidates=parse_openalex_works(payload))


def parse_openalex_works(json_text: str) -> list[PaperCandidate]:
    payload = json.loads(json_text)
    papers: list[PaperCandidate] = []
    for item in payload.get("results", []):
        openalex_id = normalize_openalex_id(item.get("id"))
        landing_page_url = ((item.get("primary_location") or {}).get("landing_page_url")) or item.get("id")
        papers.append(
            PaperCandidate(
                title=item.get("title") or item.get("display_name") or "",
                authors=[
                    authorship.get("author", {}).get("display_name", "")
                    for authorship in item.get("authorships", [])
                    if authorship.get("author", {}).get("display_name")
                ],
                abstract=_abstract_from_inverted_index(item.get("abstract_inverted_index")),
                source="openalex",
                source_id=openalex_id or item.get("id") or "",
                doi=normalize_doi(item.get("doi")),
                openalex_id=openalex_id,
                url=landing_page_url,
                published_date=item.get("publication_date"),
                updated_date=(item.get("updated_date") or "")[:10] or None,
                raw=item,
            )
        )
    return papers


def _raw_record_count(json_text: str) -> int:
    payload = json.loads(json_text)
    return len(payload.get("results", []))


def _abstract_from_inverted_index(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    positioned: list[tuple[int, str]] = []
    for word, positions in index.items():
        for position in positions:
            positioned.append((position, word))
    return " ".join(word for _, word in sorted(positioned))
