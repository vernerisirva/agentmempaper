from __future__ import annotations

import logging
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from paper_scout.config import ScoutConfig
from paper_scout.digest import DigestMetadata, render_digest, write_digest
from paper_scout.digest_quality import write_digest_quality_report
from paper_scout.fetchers import ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher
from paper_scout.llm import classify_with_optional_llm
from paper_scout.models import ClassificationResult, PaperCandidate, SourceFetchResult
from paper_scout.notifications import send_optional_notifications
from paper_scout.relevance import classify_with_rules, should_consider_for_llm
from paper_scout.http import HttpRequestError
from paper_scout.query_planner import PlannedQuery, normalize_query, plan_queries
from paper_scout.quality_report import write_paper_quality_report
from paper_scout.quality_service import (
    QualityRunStats,
    assess_and_store_candidate,
    quality_assessment_matches_mode,
    reconcile_quality_curation,
)
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
    query_diagnostics: list[dict] | None = None


def default_fetchers(config: ScoutConfig | None = None):
    return [ArxivFetcher(), SemanticScholarFetcher(max_metadata_requests=config.max_metadata_requests if config else None), OpenAlexFetcher()]


def search_sources(config: ScoutConfig, days: int | None = None, fetchers=None) -> list[PaperCandidate]:
    active_days = days if days is not None else config.days
    candidates: list[PaperCandidate] = []
    active_fetchers = fetchers or default_fetchers(config)
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
    query_diagnostics: list[dict] = []
    active_fetchers = fetchers or default_fetchers(config)
    if sources:
        active_fetchers = [fetcher for fetcher in active_fetchers if getattr(fetcher, "source", "") in sources]
    fetchers_by_source = {getattr(fetcher, "source", fetcher.__class__.__name__): fetcher for fetcher in active_fetchers}
    active_notifier = notifier or send_optional_notifications
    quality_stats = QualityRunStats()
    quality_queue: dict[str, tuple[PaperCandidate, ClassificationResult]] = {}

    try:
        queries = _queries_for_run(config, store, set(fetchers_by_source), active_days)
        query_plan_counts = {source: sum(1 for query in queries if query.source == source) for source in fetchers_by_source}
        failed_query_retry_count = sum(1 for query in queries if query.route == "failed_query_retry")
        for query in queries:
            fetcher = fetchers_by_source[query.source]
            query_days = max(active_days, query.days_override or active_days)
            http = getattr(fetcher, "http", None)
            before_requests = getattr(http, "request_count", 0)
            before_retries = getattr(http, "retry_count", 0)
            diagnostic = {"source": query.source, "query": query.provider_query, "route": query.route, "days": query_days,
                          "page_limit": 1, "record_limit": query.max_results or config.max_results_per_source}
            try:
                result = _execute_query_with_diagnostics(fetcher, query, query_days, config.max_results_per_source)
                candidates = result.candidates
                diagnostic.update(raw_count=result.raw_count, candidates=len(candidates), pages=result.page_count,
                                  incomplete=result.incomplete, metadata_requests=result.metadata_requests)
            except Exception as exc:  # noqa: BLE001
                message = format_source_failure(query.source, query.query, exc)
                LOGGER.warning("Fetcher %s failed for %r: %s", query.source, query.query, exc)
                source_failures.append(message)
                diagnostic.update(status="failed", incomplete=True, error_type=_failure_type(exc))
                store.record_failed_query(
                    config.track_id,
                    query.source,
                    query.normalized_query,
                    query_days,
                    _failure_type(exc),
                )
                continue
            finally:
                diagnostic.update(http_attempts=getattr(http, "request_count", 0) - before_requests,
                                  http_retries=getattr(http, "retry_count", 0) - before_retries)
                query_diagnostics.append(diagnostic)
            if result.incomplete:
                diagnostic["status"] = "incomplete_window"
                source_failures.append(f"{query.source}: incomplete discovery window for {query.query!r}; single-page record limit reached.")
                store.record_failed_query(config.track_id, query.source, query.normalized_query, query_days, "incomplete_window")
            else:
                diagnostic["status"] = "success"
                store.resolve_failed_query(config.track_id, query.source, query.normalized_query, query_days)
            fetched_count += len(candidates)
            source_counts[query.source] = source_counts.get(query.source, 0) + len(candidates)
            for candidate in candidates:
                rule_result = classify_with_rules(candidate, profile=config.relevance_profile)
                classification = (
                    classify_with_optional_llm(candidate, rule_result)
                    if config.relevance_llm_enabled and should_consider_for_llm(rule_result)
                    else rule_result
                )
                key = store.upsert_paper(candidate, classification)
                seen_keys.add(key)
                decision_counts[classification.decision] = decision_counts.get(classification.decision, 0) + 1
                store.record_sighting(run_id, key, candidate, f"{query.route}:{query.query}")
                if config.quality.enabled and _quality_decision_enabled(config, classification.decision):
                    quality_queue.setdefault(key, (candidate, classification))

        _run_bounded_quality_queue(config, store, quality_queue, quality_stats)

        digest_papers = store.get_unnotified_digest_papers(
            exclude_quality_suppressed=config.quality.enabled and config.quality.ranking.behavior == "hide"
        )
        digest_papers = _rank_digest_papers(digest_papers, config)
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
            if config.quality.enabled:
                write_paper_quality_report(
                    config.report_dir,
                    active_date,
                    quality_stats,
                    config.quality.assessment.version,
                    config.quality.assessment.rubric_version,
                )
        notified_count = 0
        if digest_papers and notifications_enabled:
            notification_ok = active_notifier(render_digest(active_date, digest_papers, metadata))
            if notification_ok:
                store.mark_notified([paper.canonical_key for paper in digest_papers], active_date)
                notified_count = len(digest_papers)
            else:
                LOGGER.warning("Digest written but notification failed; papers were not marked notified")
        store.finish_run(run_id, fetched_count=fetched_count, new_count=len(digest_papers), notified_count=notified_count)
        config.report_dir.mkdir(parents=True, exist_ok=True)
        report = {"track": config.track_id, "run_id": run_id, "query_diagnostics": query_diagnostics,
                  "query_plan_counts": query_plan_counts, "failed_query_retries": failed_query_retry_count,
                  "coverage_complete": False,
                  "coverage_note": "Bounded query coverage only; source indexes and omitted queries may miss papers.",
                  "quality_assessments": len(quality_stats.assessed), "notifications_sent": notified_count}
        (config.report_dir / f"discovery-run-{run_id}.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
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
            query_diagnostics=query_diagnostics,
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
    if config.quality.enabled and classification.decision in {"relevant", "maybe"}:
        try:
            assess_and_store_candidate(config.quality, store, candidate, key, classification, curation_path=config.curation_path)
        except Exception as exc:  # noqa: BLE001 - direct ingestion remains useful when quality enrichment fails.
            LOGGER.warning("Quality assessment failed during direct ingestion for %s: %s", candidate.title, exc)
    return ("already_known" if existed else "new", key, classification)


def _quality_decision_enabled(config: ScoutConfig, decision: str) -> bool:
    return {
        "relevant": config.quality.assessment.assess_relevant,
        "maybe": config.quality.assessment.assess_maybe_relevant,
        "irrelevant": config.quality.assessment.assess_irrelevant,
    }.get(decision, False)


def _run_bounded_quality_queue(
    config: ScoutConfig,
    store: PaperStore,
    queue: dict[str, tuple[PaperCandidate, ClassificationResult]],
    stats: QualityRunStats,
) -> None:
    if not config.quality.enabled or config.quality.mode == "off":
        return
    ranked: list[tuple[int, str, PaperCandidate, ClassificationResult]] = []
    for canonical_id, (candidate, classification) in queue.items():
        current = store.get_current_quality_assessment(
            canonical_id,
            assessment_version=config.quality.assessment.version,
            rubric_version=config.quality.assessment.rubric_version,
        )
        current_matches = bool(current and quality_assessment_matches_mode(config.quality, current))
        priority = 0 if current is None or not current_matches else 1 if current.assessment_scope in {"metadata_only", "title_and_abstract"} else 2
        if priority == 2 and current is not None:
            reconcile_quality_curation(config.quality, store, candidate, current, config.curation_path)
        ranked.append((priority, canonical_id, candidate, classification))
    limit = config.quality.assessment.max_assessments_per_run
    attempted = 0
    for priority, canonical_id, candidate, classification in sorted(ranked, key=lambda item: (item[0], item[1])):
        if priority == 2:
            continue
        if attempted >= limit:
            break
        attempted += 1
        try:
            assess_and_store_candidate(
                config.quality,
                store,
                candidate,
                canonical_id,
                classification,
                stats=stats,
                curation_path=config.curation_path,
            )
        except Exception as exc:  # noqa: BLE001 - assessment must never break discovery or persistence.
            LOGGER.warning("Quality assessment failed for %s: %s", candidate.title, exc)
            stats.failures.append(f"{candidate.title}: {exc}")


def _rank_digest_papers(papers, config: ScoutConfig):
    if not config.quality.enabled or config.quality.ranking.behavior in {"ignore", "annotate"}:
        return papers
    from dataclasses import replace

    from paper_scout.quality import combined_rank_score
    from paper_scout.quality_models import QualityAssessment

    ranked = []
    for paper in papers:
        assessment = None
        if paper.quality_recommendation:
            assessment = QualityAssessment(
                canonical_id=paper.canonical_key,
                overall_quality_score=paper.quality_score,
                confidence=paper.quality_confidence or "low",
                recommendation=paper.quality_recommendation,
                paper_type="unclear",
                assessment_scope=paper.quality_scope or "metadata_only",
                assessment_version=paper.quality_assessment_version or config.quality.assessment.version,
                rubric_version=config.quality.assessment.rubric_version,
                assessor_type="deterministic",
                source_content_hash="digest",
                assessed_at=paper.quality_assessed_at or "unknown",
            )
        combined = combined_rank_score(
            paper.score,
            assessment,
            config.quality.ranking.relevance_weight,
            config.quality.ranking.quality_weight,
            config.quality.ranking.unknown_quality_is_neutral,
        )
        ranked.append(replace(paper, combined_rank_score=combined))
    return sorted(
        ranked,
        key=lambda paper: (
            paper.decision == "maybe",
            -(paper.combined_rank_score or 0),
            -(paper.score or 0),
            paper.title.lower(),
        ),
    )


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
        budget = max(0, config.query_budgets.get(source, 5))
        if budget == 0:
            continue
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


def _execute_query_with_diagnostics(fetcher, query: PlannedQuery, days: int, max_results: int) -> SourceFetchResult:
    if hasattr(fetcher, "search_planned_with_diagnostics"):
        return fetcher.search_planned_with_diagnostics(query, days, max_results)
    candidates = _execute_query(fetcher, query, days, max_results)
    return SourceFetchResult(len(candidates), candidates)
