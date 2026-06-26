from __future__ import annotations

import re

from paper_scout.models import PaperCandidate


def canonical_key(candidate: PaperCandidate) -> str:
    doi = normalize_doi(candidate.doi)
    if doi:
        return f"doi:{doi}"

    arxiv_id = normalize_arxiv_id(candidate.arxiv_id)
    if arxiv_id:
        return f"arxiv:{arxiv_id}"

    if candidate.semantic_scholar_id:
        return f"semantic_scholar:{candidate.semantic_scholar_id.strip()}"

    openalex_id = normalize_openalex_id(candidate.openalex_id)
    if openalex_id:
        return f"openalex:{openalex_id}"

    year = (candidate.published_date or candidate.updated_date or "unknown")[:4]
    first_author = normalize_text(candidate.authors[0]) if candidate.authors else "unknown"
    return f"title:{normalize_text(candidate.title)}|author:{first_author}|year:{year}"


def normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    value = doi.strip()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value, flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    value = value.strip().lower()
    return value or None


def normalize_arxiv_id(arxiv_id: str | None) -> str | None:
    if not arxiv_id:
        return None
    value = arxiv_id.strip()
    value = re.sub(r"^arxiv:", "", value, flags=re.I)
    value = re.sub(r"^https?://arxiv\.org/(abs|pdf)/", "", value, flags=re.I)
    value = re.sub(r"\.pdf$", "", value, flags=re.I)
    value = re.sub(r"v\d+$", "", value)
    return value or None


def normalize_openalex_id(openalex_id: str | None) -> str | None:
    if not openalex_id:
        return None
    value = openalex_id.strip()
    value = re.sub(r"^https?://openalex\.org/", "", value, flags=re.I)
    return value or None


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.lower())).strip()
