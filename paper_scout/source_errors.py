from __future__ import annotations

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
    return (
        "Semantic Scholar rate limit (HTTP 429). This is expected without "
        "SEMANTIC_SCHOLAR_API_KEY; configure the GitHub secret/environment variable "
        "SEMANTIC_SCHOLAR_API_KEY to raise limits. arXiv and OpenAlex can still work."
    )


def _is_429(exc: Exception) -> bool:
    if isinstance(exc, HttpRequestError):
        return "429" in exc.message or "429" in str(exc)
    return "429" in str(exc)
