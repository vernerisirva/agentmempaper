"""Bounded, idempotent bootstrap using the ordinary ingestion and identity path."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from paper_scout.config import ScoutConfig
from paper_scout.deduplication import normalize_arxiv_id, normalize_text
from paper_scout.ingestion import fetch_direct_paper
from paper_scout.models import PaperCandidate
from paper_scout.scout import ingest_candidate
from paper_scout.state import PaperStore


def load_seed_manifest(config: ScoutConfig) -> dict:
    if config.seed_manifest is None:
        return {"track": config.track_id, "papers": []}
    manifest = json.loads(config.seed_manifest.read_text(encoding="utf-8"))
    if manifest.get("track") != config.track_id:
        raise ValueError("seed manifest track does not match selected track")
    papers = manifest.get("papers")
    if not isinstance(papers, list) or len(papers) > 20:
        raise ValueError("seed manifest must contain at most 20 paper IDs")
    seen = set()
    for item in papers:
        identity = normalize_arxiv_id(item.get("arxiv_id"))
        if not identity or identity in seen or not item.get("expected_title"):
            raise ValueError("each seed requires a unique arXiv ID and expected title")
        seen.add(identity)
    return manifest


def ingest_seeds(config: ScoutConfig, fetch=None) -> dict:
    manifest = load_seed_manifest(config)
    store = PaperStore(config.sqlite_path)
    fetch = fetch or fetch_direct_paper
    results = []
    for item in manifest["papers"]:
        identity = normalize_arxiv_id(item["arxiv_id"])
        placeholder = PaperCandidate(item["expected_title"], [], "", "arxiv", identity, arxiv_id=identity)
        existing_key = store.existing_key(placeholder)
        if existing_key:
            from paper_scout.relevance import classify_with_rules
            saved = store.candidate_by_key(existing_key)
            results.append({"arxiv_id": identity, "status": "already_known", "lookup": "saved state; no network request",
                            "source": saved.source, "title": saved.title, "published_date": saved.published_date,
                            "updated_date": saved.updated_date, "decision": classify_with_rules(saved, config.relevance_profile).decision})
            continue
        try:
            candidate = fetch(arxiv_id=identity)
            if candidate is None:
                raise ValueError("primary metadata lookup returned no paper")
            if normalize_arxiv_id(candidate.arxiv_id) != identity or normalize_text(candidate.title) != normalize_text(item["expected_title"]):
                raise ValueError("source identity/title does not match the manifest")
            if not candidate.abstract or not candidate.authors or candidate.publication_date_precision != "day" or not candidate.updated_date:
                raise ValueError("incomplete metadata: abstract, authors, initial date and revision date required")
            status, key, classification = ingest_candidate(config, candidate)
            results.append({"arxiv_id": identity, "status": status, "canonical_key": key,
                            "source": candidate.source, "title": candidate.title,
                            "published_date": candidate.published_date, "updated_date": candidate.updated_date,
                            "decision": classification.decision})
        except Exception as exc:  # Keep other seeds useful; never manufacture metadata.
            from paper_scout.site import _redact_secrets
            results.append({"arxiv_id": identity, "status": "unresolved", "error": _redact_secrets(str(exc))})
    report = {"track": config.track_id, "checked_at": datetime.now(timezone.utc).isoformat(),
              "notifications_sent": 0, "results": results,
              "unresolved": [r["arxiv_id"] for r in results if r["status"] == "unresolved"]}
    config.report_dir.mkdir(parents=True, exist_ok=True)
    (config.report_dir / "seed-ingestion.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
