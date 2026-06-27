from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from html import unescape
from urllib.parse import parse_qs, quote, urlparse

from .dates import precision_rank, publication_date
from .http import HttpClient
from .models import PaperCandidate


@dataclass
class DateEnrichmentDiagnostics:
    warnings: list[str] = field(default_factory=list)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


@dataclass(frozen=True)
class EnrichedDate:
    value: str
    source: str
    confidence: str


def enrich_candidate_publication_date(
    candidate: PaperCandidate,
    http: HttpClient | None = None,
    diagnostics: DateEnrichmentDiagnostics | None = None,
) -> PaperCandidate:
    diagnostics = diagnostics or DateEnrichmentDiagnostics()
    current = publication_date(candidate.published_date, candidate.publication_date_source or candidate.source, candidate.publication_year)
    doi = candidate.doi or infer_ssrn_doi(candidate.url) or infer_ssrn_doi(candidate.doi)
    raw = dict(candidate.raw)
    ssrn_id = extract_ssrn_id(candidate.url) or extract_ssrn_id(doi)
    if ssrn_id:
        raw["ssrn_id"] = ssrn_id

    if not _should_enrich(current.precision, candidate.publication_date_source):
        return _with_metadata(candidate, current.value, current.year, current.precision, current.source, candidate.publication_date_confidence, doi, raw)

    active_http = http or HttpClient(retries=1, pause_seconds=0.2)
    enriched: EnrichedDate | None = None
    if ssrn_id:
        enriched = _try_ssrn_enrichment(candidate.url, ssrn_id, active_http, diagnostics, raw)
    if enriched is None and doi:
        enriched = _try_crossref_enrichment(doi, active_http, diagnostics)

    if enriched is None or precision_rank(publication_date(enriched.value, enriched.source).precision) < precision_rank(current.precision):
        return _with_metadata(candidate, current.value, current.year, current.precision, current.source, candidate.publication_date_confidence, doi, raw)

    published = publication_date(enriched.value, enriched.source)
    precision = "exact" if enriched.source == "ssrn" and published.precision == "day" else published.precision
    return _with_metadata(candidate, published.value, published.year, precision, enriched.source, enriched.confidence, doi, raw)


def extract_ssrn_id(value: str | None) -> str | None:
    if not value:
        return None
    parsed = urlparse(value)
    abstract_id = parse_qs(parsed.query).get("abstract_id")
    if abstract_id and abstract_id[0].isdigit():
        return abstract_id[0]
    match = re.search(r"(?:ssrn\.|abstract_id=)(\d{5,})", value, flags=re.I)
    return match.group(1) if match else None


def infer_ssrn_doi(value: str | None) -> str | None:
    ssrn_id = extract_ssrn_id(value)
    return f"10.2139/ssrn.{ssrn_id}" if ssrn_id else None


def _should_enrich(precision: str | None, source: str | None) -> bool:
    if precision_rank(precision) < precision_rank("day"):
        return True
    return bool(source and source.lower() in {"source", "unknown"})


def _try_ssrn_enrichment(
    url: str | None,
    ssrn_id: str,
    http: HttpClient,
    diagnostics: DateEnrichmentDiagnostics,
    raw: dict[str, object],
) -> EnrichedDate | None:
    target = url if url and "papers.ssrn.com" in url else f"https://papers.ssrn.com/sol3/papers.cfm?abstract_id={ssrn_id}"
    try:
        html = http.get_text(target, headers={"Accept": "text/html"})
    except Exception as exc:  # noqa: BLE001 - blocked landing pages should not fail a run.
        diagnostics.warn(f"SSRN enrichment failed for {ssrn_id}: {exc}")
        return None
    doi = _extract_ssrn_doi(html)
    if doi:
        raw["ssrn_doi"] = doi
    date_value = _extract_ssrn_date(html)
    if not date_value:
        diagnostics.warn(f"SSRN enrichment found no exact date for {ssrn_id}")
        return None
    raw["ssrn_date_written"] = date_value
    return EnrichedDate(date_value, "ssrn", "high")


def _try_crossref_enrichment(doi: str, http: HttpClient, diagnostics: DateEnrichmentDiagnostics) -> EnrichedDate | None:
    url = f"https://api.crossref.org/works/{quote(doi, safe='')}"
    try:
        payload = json.loads(http.get_text(url, headers={"Accept": "application/json"}))
    except Exception as exc:  # noqa: BLE001
        diagnostics.warn(f"Crossref enrichment failed for {doi}: {exc}")
        return None
    message = payload.get("message", {}) if isinstance(payload, dict) else {}
    for key in ["published-print", "published-online", "posted", "created", "deposited"]:
        if key not in message:
            continue
        value = _date_from_crossref_parts(message[key])
        if value:
            confidence = "low" if key in {"created", "deposited"} else "medium"
            return EnrichedDate(value, f"crossref-{key}", confidence)
    diagnostics.warn(f"Crossref enrichment found no usable date for {doi}")
    return None


def _extract_ssrn_date(html: str) -> str | None:
    text = unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)))
    patterns = [
        r"Date\s+Written:\s*([A-Z][a-z]+\s+\d{1,2},\s+\d{4})",
        r"Date\s+posted:?\s*([A-Z][a-z]+\s+\d{1,2},\s+\d{4})",
        r"Posted:?\s*([A-Z][a-z]+\s+\d{1,2},\s+\d{4})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            parsed = _parse_human_date(match.group(1))
            if parsed:
                return parsed
    meta_match = re.search(
        r'<meta[^>]+name=["\'](?:citation_publication_date|dc\.date|article:published_time)["\'][^>]+content=["\']([^"\']+)["\']',
        html,
        flags=re.I,
    )
    if meta_match:
        return _normalize_machine_date(meta_match.group(1))
    return None


def _extract_ssrn_doi(html: str) -> str | None:
    match = re.search(r"10\.2139/ssrn\.\d{5,}", html, flags=re.I)
    return match.group(0).lower() if match else None


def _parse_human_date(value: str) -> str | None:
    for fmt in ["%B %d, %Y", "%b %d, %Y"]:
        try:
            return datetime.strptime(value.strip(), fmt).date().isoformat()
        except ValueError:
            continue
    return None


def _normalize_machine_date(value: str) -> str | None:
    cleaned = value.strip().replace("/", "-")
    match = re.match(r"(\d{4})-(\d{1,2})(?:-(\d{1,2}))?", cleaned)
    if not match:
        return _parse_human_date(cleaned)
    year, month, day = match.group(1), match.group(2), match.group(3) or "01"
    return f"{year}-{int(month):02d}-{int(day):02d}"


def _date_from_crossref_parts(value: object) -> str | None:
    if not isinstance(value, dict):
        return None
    parts = value.get("date-parts")
    if not isinstance(parts, list) or not parts or not isinstance(parts[0], list) or not parts[0]:
        return None
    try:
        year = int(parts[0][0])
        month = int(parts[0][1]) if len(parts[0]) > 1 else 1
        day = int(parts[0][2]) if len(parts[0]) > 2 else 1
    except (TypeError, ValueError):
        return None
    if len(parts[0]) == 1:
        return f"{year:04d}"
    if len(parts[0]) == 2:
        return f"{year:04d}-{month:02d}"
    return f"{year:04d}-{month:02d}-{day:02d}"


def _with_metadata(
    candidate: PaperCandidate,
    value: str | None,
    year: str | None,
    precision: str | None,
    source: str | None,
    confidence: str | None,
    doi: str | None,
    raw: dict[str, object],
) -> PaperCandidate:
    return PaperCandidate(
        **{
            **candidate.__dict__,
            "doi": doi or candidate.doi,
            "published_date": value,
            "publication_year": year,
            "publication_date_precision": precision,
            "publication_date_source": source,
            "publication_date_confidence": confidence or candidate.publication_date_confidence or _default_confidence(precision, source),
            "raw": raw,
        }
    )


def _default_confidence(precision: str | None, source: str | None) -> str | None:
    if not precision or precision == "unknown":
        return None
    if precision == "year":
        return "low"
    if source in {"arxiv", "ssrn"}:
        return "high"
    if source and source.startswith("crossref-created") or source and source.startswith("crossref-deposited"):
        return "low"
    if source and source.startswith("crossref"):
        return "medium"
    return "medium" if precision in {"day", "month"} else "low"
