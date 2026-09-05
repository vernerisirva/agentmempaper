"""Canonical direct metadata lookup shared by CLI and declarative seeds."""
from __future__ import annotations

import re
from paper_scout.fetchers import ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher
from paper_scout.models import PaperCandidate


def fetch_direct_paper(arxiv_id: str | None = None, doi: str | None = None, url: str | None = None) -> PaperCandidate | None:
    if url and not arxiv_id:
        match = re.search(r"arxiv\.org/(?:abs|pdf)/([^?#/]+)", url, flags=re.I)
        if match:
            arxiv_id = match.group(1).removesuffix(".pdf")
    if url and not doi:
        match = re.search(r"(?:doi\.org/)?(10\.\d{4,9}/[^?#\s]+)", url, flags=re.I)
        if match:
            doi = match.group(1)
    if arxiv_id:
        try:
            return ArxivFetcher().fetch_by_id(arxiv_id)
        except Exception:
            return OpenAlexFetcher().fetch_by_doi(f"10.48550/arXiv.{arxiv_id}")
    if doi:
        try:
            return SemanticScholarFetcher().fetch_by_identifier(f"DOI:{doi}")
        except Exception:
            return OpenAlexFetcher().fetch_by_doi(doi)
    raise ValueError("ingest-paper requires --arxiv-id, --doi, or a supported --url")
