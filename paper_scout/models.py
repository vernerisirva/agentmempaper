from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PaperCandidate:
    title: str
    authors: list[str]
    abstract: str
    source: str
    source_id: str
    doi: str | None = None
    arxiv_id: str | None = None
    semantic_scholar_id: str | None = None
    openalex_id: str | None = None
    url: str | None = None
    published_date: str | None = None
    updated_date: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SourceFetchResult:
    raw_count: int
    candidates: list[PaperCandidate]


@dataclass(frozen=True)
class ClassificationResult:
    score: int
    decision: str
    reason: str
    tags: list[str] = field(default_factory=list)
    abstract_summary: str | None = None
    classifier: str = "rules"


@dataclass(frozen=True)
class DigestPaper:
    canonical_key: str
    title: str
    authors: list[str]
    abstract: str
    source: str
    url: str | None
    published_date: str | None
    score: int
    decision: str
    reason: str
    tags: list[str] = field(default_factory=list)
    abstract_summary: str | None = None
