from __future__ import annotations

import os

from paper_scout.http import HttpRequestError


def format_source_failure(source: str, term: str, exc: Exception) -> str:
    detail = _format_semantic_scholar_rate_limit(source, exc)
    if detail:
        return f"{source} failed for {term!r}: {detail}"
    return f"{source} failed for {term!r}: {exc}"


def source_error_message(source: str, exc: Exception) -> str:
    return _format_semantic_scholar_rate_limit(source, exc) or str(exc)


def _format_semantic_scholar_rate_limit(source: str, exc: Exception) -> str | None:
    if source != "semantic_scholar" or not _is_429(exc):
        return None
    if os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        return "Semantic Scholar returned HTTP 429 despite an API key, likely because query volume was high. The run continued with other sources."
    return "Semantic Scholar returned HTTP 429. Configure SEMANTIC_SCHOLAR_API_KEY for higher rate limits."


def _is_429(exc: Exception) -> bool:
    if isinstance(exc, HttpRequestError):
        return "429" in exc.message or "429" in str(exc)
    return "429" in str(exc)
