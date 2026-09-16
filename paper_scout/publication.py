"""Descriptive publication provenance, deliberately independent of quality."""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse
from paper_scout.models import PaperCandidate

PUBLICATION_STATUSES = {"peer_reviewed", "preprint", "repository_only", "unknown"}

@dataclass(frozen=True)
class PublicationStatus:
    status: str
    evidence: str


def publication_status(candidate: PaperCandidate) -> PublicationStatus:
    raw = candidate.raw or {}
    # A published journal/proceedings location is evidence; a DOI or Crossref
    # record alone is not. Aggregator metadata is descriptive, not verification.
    for loc in [raw.get("primary_location"), *(raw.get("locations") or [])]:
        if not isinstance(loc, dict):
            continue
        source = loc.get("source") or {}
        venue = str(source.get("display_name") or "")
        if (loc.get("is_published") is True and source.get("type") in {"journal", "conference"}
                and venue and not _repository_name(venue)):
            return PublicationStatus("peer_reviewed", f"OpenAlex records a published {source['type']} location: {venue}. Peer review inferred from venue metadata, not independently verified.")
    types = set(raw.get("publicationTypes") or [])
    venue = str(raw.get("venue") or (raw.get("journal") or {}).get("name") or "")
    if types & {"JournalArticle", "Conference"} and venue and not _repository_name(venue):
        return PublicationStatus("peer_reviewed", f"Semantic Scholar records a journal/conference article at {venue}. Peer review inferred from venue metadata, not independently verified.")
    if candidate.arxiv_id or candidate.source == "arxiv" or str(candidate.doi or "").lower().startswith("10.48550/arxiv."):
        return PublicationStatus("preprint", "arXiv manuscript identifier; no external publication established by the available metadata.")
    hosts = {urlparse(str(candidate.url or "")).hostname or ""}
    for loc in [raw.get("primary_location"), *(raw.get("locations") or [])]:
        if isinstance(loc, dict):
            hosts.add(urlparse(str(loc.get("landing_page_url") or "")).hostname or "")
    if candidate.source == "zenodo" or str(candidate.doi or "").startswith("10.5281/zenodo.") or any(h == "zenodo.org" or h.endswith(".zenodo.org") for h in hosts):
        subtype = (raw.get("metadata") or {}).get("resource_type", {}).get("subtype")
        declared = f" Depositor resource subtype: {subtype}." if subtype else ""
        return PublicationStatus("repository_only", "Zenodo deposit; no external journal/conference publication evidence in supplied metadata." + declared)
    if raw.get("type") in {"preprint", "posted-content"} or "Preprint" in types or any(h in {"arxiv.org", "www.arxiv.org", "ssrn.com", "papers.ssrn.com", "www.biorxiv.org", "www.medrxiv.org"} for h in hosts):
        return PublicationStatus("preprint", "Source metadata identifies a working manuscript/preprint; peer review is not established.")
    loc = raw.get("primary_location") or {}
    if isinstance(loc, dict) and (loc.get("source") or {}).get("type") == "repository":
        return PublicationStatus("repository_only", "Only a repository location is documented; external publication is not established.")
    return PublicationStatus("unknown", "Insufficient publication provenance; DOI registration alone does not establish peer review.")


def _repository_name(name: str) -> bool:
    return any(word in name.lower() for word in ("arxiv", "zenodo", "ssrn", "preprint", "repository", "figshare", "research square"))
