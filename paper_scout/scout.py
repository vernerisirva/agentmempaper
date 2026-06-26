from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from paper_scout.config import ScoutConfig
from paper_scout.digest import DigestMetadata, render_digest, write_digest
from paper_scout.fetchers import ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher
from paper_scout.llm import classify_with_optional_llm
from paper_scout.models import PaperCandidate
from paper_scout.notifications import send_optional_notifications
from paper_scout.relevance import classify_with_rules, should_consider_for_llm
from paper_scout.state import PaperStore

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunResult:
    run_id: int
    fetched_count: int
    new_digest_count: int
    digest_path: Path
    unique_count: int = 0
    decision_counts: dict[str, int] | None = None
    source_counts: dict[str, int] | None = None
    source_failures: list[str] | None = None


def default_fetchers():
    return [ArxivFetcher(), SemanticScholarFetcher(), OpenAlexFetcher()]


def search_sources(config: ScoutConfig, days: int | None = None, fetchers=None) -> list[PaperCandidate]:
    active_days = days if days is not None else config.days
    candidates: list[PaperCandidate] = []
    for term in config.terms:
        for fetcher in fetchers or default_fetchers():
            try:
                candidates.extend(fetcher.search(term, active_days, config.max_results_per_source))
            except Exception as exc:  # noqa: BLE001 - one flaky source must not fail the whole run.
                LOGGER.warning("Fetcher %s failed for %r: %s", getattr(fetcher, "source", fetcher), term, exc)
    return candidates


def run_scout(config: ScoutConfig, fetchers=None, digest_date: str | None = None, notifier=None) -> RunResult:
    active_date = digest_date or date.today().isoformat()
    store = PaperStore(config.sqlite_path)
    run_id = store.start_run(config.days)
    fetched_count = 0
    source_counts: dict[str, int] = {}
    decision_counts = {"relevant": 0, "maybe": 0, "irrelevant": 0}
    seen_keys: set[str] = set()
    source_failures: list[str] = []
    active_fetchers = fetchers or default_fetchers()
    active_notifier = notifier or send_optional_notifications

    try:
        for term in config.terms:
            for fetcher in active_fetchers:
                source = getattr(fetcher, "source", fetcher.__class__.__name__)
                try:
                    candidates = fetcher.search(term, config.days, config.max_results_per_source)
                except Exception as exc:  # noqa: BLE001
                    message = f"{source} failed for {term!r}: {exc}"
                    LOGGER.warning("Fetcher %s failed for %r: %s", source, term, exc)
                    source_failures.append(message)
                    continue
                fetched_count += len(candidates)
                source_counts[source] = source_counts.get(source, 0) + len(candidates)
                for candidate in candidates:
                    rule_result = classify_with_rules(candidate)
                    classification = (
                        classify_with_optional_llm(candidate, rule_result)
                        if should_consider_for_llm(rule_result)
                        else rule_result
                    )
                    key = store.upsert_paper(candidate, classification)
                    seen_keys.add(key)
                    decision_counts[classification.decision] = decision_counts.get(classification.decision, 0) + 1
                    store.record_sighting(run_id, key, candidate, term)

        digest_papers = store.get_unnotified_digest_papers()
        digest_path = config.digest_dir / f"{active_date}.md"
        metadata = DigestMetadata(
            run_id=run_id,
            source_counts=source_counts,
            fetched_count=fetched_count,
            unique_count=len(seen_keys),
            decision_counts=decision_counts,
            source_failures=source_failures,
        )
        write_digest(digest_path, active_date, digest_papers, metadata)
        notified_count = 0
        if digest_papers:
            notification_ok = active_notifier(render_digest(active_date, digest_papers, metadata))
            if notification_ok:
                store.mark_notified([paper.canonical_key for paper in digest_papers], active_date)
                notified_count = len(digest_papers)
            else:
                LOGGER.warning("Digest written but notification failed; papers were not marked notified")
        store.finish_run(run_id, fetched_count=fetched_count, new_count=len(digest_papers), notified_count=notified_count)
        return RunResult(
            run_id=run_id,
            fetched_count=fetched_count,
            new_digest_count=len(digest_papers),
            digest_path=digest_path,
            unique_count=len(seen_keys),
            decision_counts=decision_counts,
            source_counts=source_counts,
            source_failures=source_failures,
        )
    except Exception:
        store.finish_run(run_id, fetched_count=fetched_count, new_count=0, notified_count=0, status="failed")
        raise
