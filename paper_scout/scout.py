from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from paper_scout.config import ScoutConfig
from paper_scout.digest import DigestMetadata, render_digest, write_digest
from paper_scout.digest_quality import write_digest_quality_report
from paper_scout.fetchers import ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher
from paper_scout.llm import classify_with_optional_llm
from paper_scout.models import PaperCandidate
from paper_scout.notifications import send_optional_notifications
from paper_scout.relevance import classify_with_rules, should_consider_for_llm
from paper_scout.http import HttpRequestError
from paper_scout.query_planner import PlannedQuery, normalize_query, plan_queries
from paper_scout.source_errors import format_source_failure
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
    query_plan_counts: dict[str, int] | None = None
    failed_query_retry_count: int = 0


def default_fetchers():
    return [ArxivFetcher(), SemanticScholarFetcher(), OpenAlexFetcher()]


def search_sources(config: ScoutConfig, days: int | None = None, fetchers=None) -> list[PaperCandidate]:
    active_days = days if days is not None else config.days
    candidates: list[PaperCandidate] = []
    active_fetchers = fetchers or default_fetchers()
    by_source = {getattr(fetcher, "source", fetcher.__class__.__name__): fetcher for fetcher in active_fetchers}
    for query in plan_queries(config, sources=set(by_source)):
        fetcher = by_source[query.source]
        try:
            candidates.extend(_execute_query(fetcher, query, active_days, config.max_results_per_source))
        except Exception as exc:  # noqa: BLE001 - one flaky source must not fail the whole run.
            LOGGER.warning("Fetcher %s failed for %r: %s", query.source, query.query, exc)
    return candidates


def run_scout(
    config: ScoutConfig,
    fetchers=None,
    digest_date: str | None = None,
    notifier=None,
    days: int | None = None,
    notifications_enabled: bool = True,
    digest_path_override: Path | None = None,
    write_quality_report: bool = True,
    sources: set[str] | None = None,
) -> RunResult:
    active_date = digest_date or date.today().isoformat()
    active_days = days if days is not None else config.days
    store = PaperStore(config.sqlite_path)
    run_id = store.start_run(active_days)
    fetched_count = 0
    source_counts: dict[str, int] = {}
    decision_counts = {"relevant": 0, "maybe": 0, "irrelevant": 0}
    seen_keys: set[str] = set()
    source_failures: list[str] = []
    active_fetchers = fetchers or default_fetchers()
    if sources:
        active_fetchers = [fetcher for fetcher in active_fetchers if getattr(fetcher, "source", "") in sources]
    fetchers_by_source = {getattr(fetcher, "source", fetcher.__class__.__name__): fetcher for fetcher in active_fetchers}
    active_notifier = notifier or send_optional_notifications

    try:
        queries = _queries_for_run(config, store, set(fetchers_by_source), active_days)
        query_plan_counts = {source: sum(1 for query in queries if query.source == source) for source in fetchers_by_source}
        failed_query_retry_count = sum(1 for query in queries if query.route == "failed_query_retry")
        for query in queries:
            fetcher = fetchers_by_source[query.source]
            query_days = max(active_days, query.days_override or active_days)
            try:
                candidates = _execute_query(fetcher, query, query_days, config.max_results_per_source)
            except Exception as exc:  # noqa: BLE001
                message = format_source_failure(query.source, query.query, exc)
                LOGGER.warning("Fetcher %s failed for %r: %s", query.source, query.query, exc)
                source_failures.append(message)
                store.record_failed_query(
                    config.track_id,
                    query.source,
                    query.normalized_query,
                    query_days,
                    _failure_type(exc),
                )
                continue
            store.resolve_failed_query(config.track_id, query.source, query.normalized_query, query_days)
            fetched_count += len(candidates)
            source_counts[query.source] = source_counts.get(query.source, 0) + len(candidates)
            for candidate in candidates:
                rule_result = classify_with_rules(candidate, profile=config.relevance_profile)
                classification = (
                    classify_with_optional_llm(candidate, rule_result)
                    if should_consider_for_llm(rule_result)
                    else rule_result
                )
                key = store.upsert_paper(candidate, classification)
                seen_keys.add(key)
                decision_counts[classification.decision] = decision_counts.get(classification.decision, 0) + 1
                store.record_sighting(run_id, key, candidate, f"{query.route}:{query.query}")

        digest_papers = store.get_unnotified_digest_papers()
        digest_path = digest_path_override or config.digest_dir / f"{active_date}.md"
        metadata = DigestMetadata(
            run_id=run_id,
            source_counts=source_counts,
            fetched_count=fetched_count,
            unique_count=len(seen_keys),
            decision_counts=decision_counts,
            source_failures=source_failures,
        )
        write_digest(digest_path, active_date, digest_papers, metadata)
        if write_quality_report:
            write_digest_quality_report(config.report_dir, active_date, digest_papers)
        notified_count = 0
        if digest_papers and notifications_enabled:
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
            query_plan_counts=query_plan_counts,
            failed_query_retry_count=failed_query_retry_count,
        )
    except Exception:
        store.finish_run(run_id, fetched_count=fetched_count, new_count=0, notified_count=0, status="failed")
        raise


def run_backfill(
    config: ScoutConfig,
    days: int,
    sources: set[str] | None = None,
    report_date: str | None = None,
    fetchers=None,
) -> RunResult:
    active_date = report_date or date.today().isoformat()
    store = PaperStore(config.sqlite_path)
    before = store.paper_count()
    report_path = config.report_dir / f"backfill-{active_date}.md"
    result = run_scout(
        config,
        fetchers=fetchers,
        digest_date=active_date,
        days=days,
        notifications_enabled=False,
        digest_path_override=report_path,
        write_quality_report=False,
        sources=sources,
    )
    recovered = max(0, PaperStore(config.sqlite_path).paper_count() - before)
    existing = report_path.read_text(encoding="utf-8")
    report_path.write_text(
        f"# Paper Scout backfill - {active_date}\n\n- Track: `{config.track_id}`\n- Lookback: {days} days\n- Newly recovered: {recovered}\n- Notifications sent: 0\n- Source plan: {', '.join(f'{source}={count}' for source, count in (result.query_plan_counts or {}).items())}\n- Failed-query retries: {result.failed_query_retry_count}\n\n{existing}",
        encoding="utf-8",
    )
    return result


def ingest_candidate(config: ScoutConfig, candidate: PaperCandidate) -> tuple[str, str, object]:
    store = PaperStore(config.sqlite_path)
    existed = store.paper_exists(candidate)
    classification = classify_with_rules(candidate, profile=config.relevance_profile)
    key = store.upsert_paper(candidate, classification)
    return ("already_known" if existed else "new", key, classification)


def _queries_for_run(config: ScoutConfig, store: PaperStore, sources: set[str], active_days: int) -> list[PlannedQuery]:
    base = plan_queries(config, sources=sources)
    by_source: dict[str, list[PlannedQuery]] = {source: [] for source in sources}
    for failed in store.retryable_failed_queries(config.track_id, limit=sum(config.query_budgets.values())):
        if failed.source not in sources:
            continue
        by_source[failed.source].append(
            PlannedQuery(
                source=failed.source,
                query=failed.normalized_query,
                provider_query=failed.normalized_query,
                mode="raw",
                route="failed_query_retry",
                days_override=max(active_days, failed.requested_days),
            )
        )
    for query in base:
        by_source.setdefault(query.source, []).append(query)
    selected: list[PlannedQuery] = []
    for source in sorted(by_source):
        seen: set[str] = set()
        budget = config.query_budgets.get(source, 5)
        for query in by_source[source]:
            if query.normalized_query in seen:
                continue
            seen.add(query.normalized_query)
            selected.append(query)
            if sum(1 for item in selected if item.source == source) >= budget:
                break
    return selected


def _execute_query(fetcher, query: PlannedQuery, days: int, max_results: int) -> list[PaperCandidate]:
    if hasattr(fetcher, "search_planned"):
        return list(fetcher.search_planned(query, days, max_results))
    return list(fetcher.search(query.query, days, query.max_results or max_results))


def _failure_type(exc: Exception) -> str:
    return exc.kind if isinstance(exc, HttpRequestError) else exc.__class__.__name__.lower()
