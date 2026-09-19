from __future__ import annotations

import argparse
import json
import logging
import os
import re
from dataclasses import replace
from datetime import date
from pathlib import Path

from paper_scout.batch_population import (
    TRACKS, build_population, population_manifest, repository_code_sha, track_configs,
    verify_manifest, write_manifest,
)
from paper_scout.config import TRACK_CONFIG_PATHS, load_config
from paper_scout.discovery_evaluation import evaluate_discovery, write_discovery_report
from paper_scout.digest import write_digest
from paper_scout.evaluation import evaluate_relevance_examples, relevance_fixture_examples, write_relevance_report
from paper_scout.fetchers import ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.relevance import classify_with_rules, explain_rule_matches
from paper_scout.quality_evaluation import evaluate_quality_fixtures, write_quality_evaluation_report
from paper_scout.quality_report import write_paper_quality_report
from paper_scout.promotion_protocol import DUAL_PROMOTION_GATE_VERSIONS
from paper_scout.quality_models import QUALITY_GATE_VERSION
from paper_scout.quality_service import QualityRunStats, assess_and_store_candidate
from paper_scout.scout import ingest_candidate, run_backfill, run_scout, search_sources
from paper_scout.site import build_site
from paper_scout.state import PaperStore
from paper_scout.validation import run_live_smoke, validate_idempotency


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="paper_scout")
    parser.add_argument("--config", default="config/paper_scout.yaml")
    parser.add_argument("--verbose", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Fetch, classify, persist, and write today's digest")
    run_parser.add_argument("--no-notify", action="store_true")
    run_parser.add_argument("--no-llm", action="store_true",
                            help="Discovery only; do not run the scientific assessment queue")
    run_parser.add_argument("--date", default=date.today().isoformat())
    _add_track_argument(run_parser)

    search_parser = subparsers.add_parser("search", help="Fetch candidates without writing state")
    search_parser.add_argument("--days", type=int, default=None)
    _add_track_argument(search_parser)

    digest_parser = subparsers.add_parser("digest", help="Render a digest from stored notifications")
    digest_parser.add_argument("--date", required=True)
    _add_track_argument(digest_parser)

    mark_parser = subparsers.add_parser("mark-notified", help="Mark all current relevant/maybe papers as notified")
    mark_parser.add_argument("--date", default=date.today().isoformat())
    _add_track_argument(mark_parser)

    eval_parser = subparsers.add_parser("evaluate-relevance", help="Evaluate deterministic relevance rules on fixture papers")
    eval_parser.add_argument("--date", default=date.today().isoformat())
    eval_parser.add_argument("--with-llm", action="store_true", help="Also use the optional LLM classifier when configured")
    _add_track_argument(eval_parser)

    smoke_parser = subparsers.add_parser("smoke-live", help="Run live source checks without notification side effects")
    smoke_parser.add_argument("--days", type=int, default=14)
    smoke_parser.add_argument("--max-results-per-source", type=int, default=25)
    smoke_parser.add_argument("--no-notify", action="store_true")
    smoke_parser.add_argument("--strict", action="store_true")
    smoke_parser.add_argument("--ci", action="store_true", help="Write CI-friendly JSON output alongside Markdown")
    smoke_parser.add_argument("--date", default=date.today().isoformat())
    _add_track_argument(smoke_parser)

    idem_parser = subparsers.add_parser("validate-idempotency", help="Validate duplicate notification protection")
    idem_parser.add_argument("--date", default=date.today().isoformat())
    _add_track_argument(idem_parser)

    build_site_parser = subparsers.add_parser("build-site", help="Build the static Paper Scout dashboard under docs/")
    build_site_parser.add_argument("--offline", action="store_true", help="Build from saved metadata without network date enrichment")
    build_site_parser.add_argument("--docs-dir", default=None)
    _add_track_argument(build_site_parser)

    explain_parser = subparsers.add_parser("explain-paper", help="Explain deterministic relevance rules for a generated paper")
    explain_parser.add_argument("--arxiv-id")
    explain_parser.add_argument("--doi")
    explain_parser.add_argument("--title")
    explain_parser.add_argument("--data-path", default=None)
    _add_track_argument(explain_parser)

    discovery_parser = subparsers.add_parser("evaluate-discovery", help="Evaluate fixture-based discovery regression coverage")
    discovery_parser.add_argument("--date", default=date.today().isoformat())
    _add_track_argument(discovery_parser)

    backfill_parser = subparsers.add_parser("backfill", help="Recover papers missed during the normal daily lookback")
    backfill_parser.add_argument("--since", help="One-time historical start date; never scheduled implicitly")
    backfill_parser.add_argument("--days", type=int, default=45)
    backfill_parser.add_argument("--sources", default="arxiv,openalex,semantic_scholar")
    backfill_parser.add_argument("--no-notify", action="store_true")
    backfill_parser.add_argument("--no-llm", action="store_true",
                                 help="Recovery only; do not run the scientific assessment queue")
    backfill_parser.add_argument("--date", default=date.today().isoformat())
    _add_track_argument(backfill_parser)

    failed_parser = subparsers.add_parser("failed-queries", help="List unresolved source queries awaiting retry")
    failed_parser.add_argument("--include-resolved", action="store_true")
    _add_track_argument(failed_parser)

    ingest_parser = subparsers.add_parser("ingest-paper", help="Fetch and ingest one paper without notifications")
    ingest_parser.add_argument("--arxiv-id")
    ingest_parser.add_argument("--doi")
    ingest_parser.add_argument("--url")
    ingest_parser.add_argument("--pdf-url", help="Optional direct open-access PDF URL used only for quality assessment")
    _add_track_argument(ingest_parser)

    seed_parser = subparsers.add_parser("ingest-seeds", help="Ingest missing declarative seed IDs outside the daily window; no notifications")
    _add_track_argument(seed_parser)

    quality_eval_parser = subparsers.add_parser("evaluate-quality", help="Evaluate deterministic scholarly-quality rules on fixture papers")
    quality_eval_parser.add_argument("--date", default=date.today().isoformat())
    _add_track_argument(quality_eval_parser)

    population_parser = subparsers.add_parser(
        "batch-population",
        help="Build or verify the deterministic eligible-population manifest for an unseen batch")
    population_parser.add_argument("--manifest", type=Path, required=True,
                                   help="Manifest path to write, or to verify with --verify")
    population_parser.add_argument("--verify", action="store_true",
                                   help="Rebuild from the manifest's own inputs and compare instead of writing")
    population_parser.add_argument("--build-time", default=None,
                                   help="Pinned build time for the ranking's newness key; required to build")
    population_parser.add_argument("--roster", type=Path, action="append", default=[],
                                   help="Frozen roster manifest whose canonical ids are excluded; repeatable")
    # Not --track: the shared track argument selects one config for the whole process,
    # while a population spans every track so one manuscript cannot slip through twice.
    population_parser.add_argument("--population-track", action="append", choices=list(TRACKS),
                                   default=[], dest="population_tracks",
                                   help="Restrict to these tracks (default: all); repeatable")

    operational_parser = subparsers.add_parser(
        "operational-assess",
        help="One bounded daily scientific-assessment run across all tracks")
    operational_parser.add_argument("--build-time", default=None,
                                    help="Pinned build time for the ranking's newness key")
    operational_parser.add_argument("--metrics", type=Path,
                                    help="Write the operational metrics record here as JSON")
    operational_parser.add_argument("--max-per-track", type=int, default=None,
                                    help="Override the per-track paper limit; never above the policy default")
    operational_parser.add_argument("--max-per-run", type=int, default=None,
                                    help="Override the per-run paper limit; never above the policy default")
    operational_parser.add_argument("--dry-run", action="store_true",
                                    help="Select and report candidates without any model call")
    operational_parser.add_argument("--date", default=date.today().isoformat())

    reassess_parser = subparsers.add_parser("reassess-quality", help="Assess or reassess stored relevant papers")
    reassess_parser.add_argument("--limit", type=int, default=None, help="Maximum papers (default: track run limit; hard ceiling 50)")
    reassess_parser.add_argument("--assessment-json", type=Path, help="Import one manuscript review; requires --paper-id, validates excerpt anchors")
    reassess_parser.add_argument("--pdf-url", help="Open PDF for a single-paper assessment")
    reassess_parser.add_argument("--full-text", action="store_true", help="Explicitly enable bounded full-text acquisition")
    reassess_parser.add_argument("--days", type=int, default=None)
    reassess_parser.add_argument("--paper-id")
    reassess_parser.add_argument("--mode", choices=["off", "deterministic", "llm", "hybrid", "auto"], default=None)
    reassess_parser.add_argument("--assessment-version")
    reassess_parser.add_argument("--rubric-version")
    reassess_parser.add_argument("--model", help="Optional quality LLM model override for this process")
    reassess_parser.add_argument("--force", action="store_true")
    reassess_parser.add_argument("--no-full-text", action="store_true")
    reassess_parser.add_argument("--no-llm", action="store_true")
    reassess_parser.add_argument("--report-only", action="store_true")
    reassess_parser.add_argument("--date", default=date.today().isoformat())
    _add_track_argument(reassess_parser)

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(message)s")
    track_id = getattr(args, "track", None)
    config = load_config(args.config, track_id=track_id)

    if args.command == "run":
        result = run_scout(config, digest_date=args.date, notifications_enabled=not args.no_notify,
                           no_llm=args.no_llm)
        print(f"run_id={result.run_id} fetched={result.fetched_count} unique={result.unique_count} digest_items={result.new_digest_count} digest={result.digest_path}")
        return 0

    if args.command == "search":
        candidates = search_sources(config, days=args.days)
        for candidate in candidates:
            classification = classify_with_rules(candidate, profile=config.relevance_profile)
            print(f"[{classification.decision} {classification.score:03d}] {candidate.title} ({candidate.source}) {candidate.url or ''}")
        return 0

    if args.command == "digest":
        store = PaperStore(config.sqlite_path)
        papers = store.get_notified_for_date(args.date)
        if not papers:
            papers = store.get_unnotified_digest_papers()
        output_path = config.digest_dir / f"{args.date}.md"
        write_digest(output_path, args.date, papers)
        print(output_path)
        return 0

    if args.command == "mark-notified":
        store = PaperStore(config.sqlite_path)
        papers = store.get_unnotified_digest_papers()
        store.mark_notified([paper.canonical_key for paper in papers], args.date)
        print(f"marked={len(papers)}")
        return 0

    if args.command == "evaluate-relevance":
        report = evaluate_relevance_examples(
            relevance_fixture_examples(config.relevance_profile),
            use_llm=args.with_llm,
            profile=config.relevance_profile,
        )
        path = write_relevance_report(report, config.report_dir, args.date)
        print(f"precision={report['precision']:.3f} recall={report['recall']:.3f} false_positives={len(report['false_positives'])} false_negatives={len(report['false_negatives'])} report={path}")
        return 0 if not report["false_positives"] and not report["false_negatives"] and not report.get("decision_mismatches") else 1

    if args.command == "smoke-live":
        report = run_live_smoke(
            config,
            fetchers=[ArxivFetcher(), SemanticScholarFetcher(max_metadata_requests=config.max_metadata_requests), OpenAlexFetcher()],
            report_date=args.date,
            days=args.days,
            max_results_per_source=args.max_results_per_source,
            strict=args.strict,
            ci=args.ci,
        )
        print(f"candidates={report['candidate_count']} unique={report['unique_count']} failures={len(report['source_failures'])} report={report['report_path']}")
        return 0

    if args.command == "validate-idempotency":
        report = validate_idempotency(
            report_date=args.date,
            report_dir=config.report_dir,
            track_id=config.track_id,
            relevance_profile=config.relevance_profile,
        )
        print(f"passed={report['passed']} first={report['first_digest_count']} second={report['second_digest_count']} report={report['report_path']}")
        return 0 if report["passed"] else 1

    if args.command == "build-site":
        result = build_site(
            digest_dir=config.digest_dir,
            report_dir=config.report_dir,
            docs_dir=Path(args.docs_dir) if args.docs_dir else config.docs_dir,
            state_path=config.sqlite_path,
            curation_path=config.curation_path,
            site_title=config.title,
            site_subtitle=config.subtitle,
            cross_track_label=config.cross_track_label,
            cross_track_href=config.cross_track_href,
            relevance_profile=config.relevance_profile,
            quality_config=config.quality,
            enrich_dates=config.site_enrichment_enabled and not args.offline,
        )
        print(result.message)
        return 0

    if args.command == "batch-population":
        return _batch_population(args)

    if args.command == "explain-paper":
        return _explain_paper(args, config)

    if args.command == "evaluate-discovery":
        report = evaluate_discovery(config)
        path = write_discovery_report(report, config.report_dir, args.date)
        print(f"recall={report['recall']:.3f} discovered={report['discovered_count']}/{report['fixture_count']} missed={len(report['missed'])} report={path}")
        return 0 if not report["missed"] else 1

    if args.command == "backfill":
        sources = {value.strip() for value in args.sources.split(",") if value.strip()}
        unknown = sources - {"arxiv", "openalex", "semantic_scholar"}
        if unknown:
            print(f"unknown sources: {','.join(sorted(unknown))}")
            return 2
        backfill_days = args.days
        if args.since:
            backfill_days = (date.today() - date.fromisoformat(args.since)).days + 1
            if backfill_days < 1:
                parser.error("--since must not be in the future")
        result = run_backfill(config, days=backfill_days, sources=sources, report_date=args.date,
                              no_llm=args.no_llm)
        print(f"run_id={result.run_id} fetched={result.fetched_count} unique={result.unique_count} report={result.digest_path}")
        return 0

    if args.command == "failed-queries":
        store = PaperStore(config.sqlite_path)
        rows = store.failed_queries(config.track_id, include_resolved=args.include_resolved)
        for row in rows:
            print(f"{row['source']} attempts={row['attempt_count']} days={row['requested_days']} next={row['next_retry_at']} resolved={row['resolved_at'] or '-'} query={row['normalized_query']}")
        print(f"count={len(rows)}")
        return 0

    if args.command == "ingest-seeds":
        from paper_scout.seeds import ingest_seeds
        report = ingest_seeds(config)
        print(json.dumps(report, indent=2))
        return 1 if report["unresolved"] else 0

    if args.command == "ingest-paper":
        try:
            candidate = _fetch_direct_paper(args)
        except Exception as exc:  # noqa: BLE001 - direct recovery should fail cleanly on provider/network errors.
            logging.getLogger(__name__).error("Direct paper fetch failed: %s", exc)
            print(f"paper could not be fetched: {exc}")
            return 1
        if candidate is None:
            print("paper could not be fetched")
            return 1
        if args.pdf_url:
            candidate = PaperCandidate(**{**candidate.__dict__, "raw": {**candidate.raw, "direct_pdf_url": args.pdf_url}})
        status, key, classification = ingest_candidate(config, candidate)
        print(f"status={status} canonical_key={key} decision={classification.decision} score={classification.score} title={candidate.title}")
        print(f"tags={','.join(classification.tags)}")
        print(f"reason={classification.reason}")
        return 0

    if args.command == "evaluate-quality":
        report = evaluate_quality_fixtures()
        path = write_quality_evaluation_report(report, config.report_dir, args.date)
        print(f"passed={report['passed']} fixtures={len(report['fixtures'])} failures={len(report['failures'])} report={path}")
        return 0 if report["passed"] else 1

    if args.command == "operational-assess":
        return _operational_assess(args, parser)

    if args.command == "reassess-quality":
        if not config.quality.enabled:
            print("quality assessment is disabled for this track")
            return 0
        if args.limit is not None and not 1 <= args.limit <= 50:
            parser.error("--limit must be between 1 and 50")
        if (args.assessment_json or args.pdf_url) and not args.paper_id:
            parser.error("--assessment-json and --pdf-url require --paper-id")
        if args.full_text and args.no_full_text:
            parser.error("--full-text conflicts with --no-full-text")
        manual_assessment = None
        if args.assessment_json:
            from paper_scout.quality_llm import validate_manual_quality_review
            try:
                manual_assessment = validate_manual_quality_review(json.loads(args.assessment_json.read_text()))
            except (OSError, ValueError) as exc:
                parser.error(str(exc))
        assessment_config = replace(
            config.quality.assessment,
            version=args.assessment_version or config.quality.assessment.version,
            rubric_version=args.rubric_version or config.quality.assessment.rubric_version,
        )
        quality_config = replace(config.quality, mode=args.mode or config.quality.mode, assessment=assessment_config)
        if args.full_text:
            quality_config = replace(quality_config, full_text=replace(quality_config.full_text, enabled=True))
        if args.model:
            os.environ["PAPER_SCOUT_QUALITY_LLM_MODEL"] = args.model
        stats = QualityRunStats()
        store = PaperStore(config.sqlite_path)
        if args.report_only:
            for assessment in store.list_current_quality_assessments():
                stats.record(assessment, cache_hit=True)
        else:
            candidates = store.quality_candidates(days=args.days, paper_id=args.paper_id)
            limit = args.limit if args.limit is not None else quality_config.assessment.max_assessments_per_run
            if not args.force and not args.paper_id:
                candidates = [row for row in candidates if not (
                    (existing := store.get_current_quality_assessment(row[0]))
                    and (existing.quality_status == "pass" or (
                        existing.quality_gate_version in {QUALITY_GATE_VERSION, *DUAL_PROMOTION_GATE_VERSIONS}
                        and existing.assessment_version == quality_config.assessment.version
                        and existing.rubric_version == quality_config.assessment.rubric_version
                    ))
                )]
            candidates = candidates[:limit]
            for canonical_id, candidate, decision in candidates:
                classification = ClassificationResult(0, decision, "Stored relevance classification.")
                try:
                    assess_and_store_candidate(
                        quality_config,
                        store,
                        candidate,
                        canonical_id,
                        classification,
                        stats=stats,
                        force=args.force,
                        no_full_text=args.no_full_text,
                        no_llm=args.no_llm,
                        direct_pdf_url=args.pdf_url,
                        manual_assessment=manual_assessment,
                        curation_path=config.curation_path,
                    )
                except Exception as exc:  # noqa: BLE001 - one assessment must not stop a batch.
                    logging.getLogger(__name__).warning("Quality reassessment failed for %s: %s", candidate.title, exc)
                    stats.failures.append(f"{candidate.title}: {exc}")
        path = write_paper_quality_report(
            config.report_dir,
            args.date,
            stats,
            quality_config.assessment.version,
            quality_config.assessment.rubric_version,
        )
        print(f"assessed={len(stats.assessed)} failures={len(stats.failures)} extraction_failures={len(stats.extraction_failures)} report={path}")
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


def _operational_assess(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    """One bounded daily run: preflight, select, assess, report.

    Fails loudly and assesses nothing when the scientific credentials are absent, rather
    than entering the gate and letting it record a technical row against every candidate.
    Discovery and site building are separate steps in the workflow and are unaffected.
    """
    from paper_scout.config import load_config
    from paper_scout.operational_eligibility import TECHNICAL_OUTCOMES
    from paper_scout.operational_preflight import (
        MAX_PAPERS_PER_RUN, MAX_PAPERS_PER_TRACK, CostCeilingExceeded, RunBudget,
        credential_preflight)
    from paper_scout.operational_run import OperationalMetrics, select_operational_candidates
    from paper_scout.batch_population import TRACKS

    metrics = OperationalMetrics()
    configs = {track: load_config(track_id=track) for track in TRACKS}

    preflight = credential_preflight()
    metrics.preflight = preflight.to_dict()
    budget = RunBudget.from_env()
    if args.max_per_track is not None:
        budget.max_per_track = min(args.max_per_track, MAX_PAPERS_PER_TRACK)
    if args.max_per_run is not None:
        budget.max_per_run = min(args.max_per_run, MAX_PAPERS_PER_RUN)

    build_time = args.build_time or f"{args.date}T00:00:00"
    selected, summaries = select_operational_candidates(configs, build_time, budget)
    metrics.tracks = {track: summary.to_dict() for track, summary in summaries.items()}
    metrics.high_relevance_candidates = sum(s.high_relevance for s in summaries.values())
    metrics.papers_discovered = sum(s.ranked for s in summaries.values())
    metrics.assessment_candidates = len(selected)

    def finish(code: int) -> int:
        # Re-serialize after the walk: the summaries gain skipped_before_model during it.
        metrics.tracks = {track: summary.to_dict() for track, summary in summaries.items()}
        metrics.budget = budget.to_dict()
        record = metrics.to_dict()
        if args.metrics:
            args.metrics.parent.mkdir(parents=True, exist_ok=True)
            args.metrics.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(record, indent=2, sort_keys=True))
        return code

    for candidate in selected:
        print(f"nominee {candidate.track} rank={candidate.rank} {candidate.canonical_id}"
              f" ({candidate.retry.reason})")
    if args.dry_run:
        return finish(0)
    if not preflight.ok:
        # Loud, and nothing is written. Every selected paper stays exactly as eligible as
        # it was, because no assessment row is created for a credential problem.
        metrics.credential_skipped = len(selected)
        print(f"::error::Scientific assessment stage cannot run: {preflight.reason}."
              f" No assessment was attempted and no candidate eligibility was consumed.")
        return finish(1)

    try:
        _assess_selected(selected, configs, budget, metrics, summaries)
    except Exception as exc:  # noqa: BLE001 - the metrics record must survive any failure.
        logging.getLogger(__name__).warning("Operational assessment run aborted: %s", exc)
        metrics.technical_failures += 1
        return finish(1)
    return finish(0)


def _assess_selected(selected, configs, budget, metrics, summaries=None) -> None:
    """Walk each track's nominees in rank order until one actually reaches a model.

    Selection cannot tell whether a manuscript is retrievable without fetching it, so a
    track nominates several candidates and this walk tries them in order. A candidate
    rejected by acquisition or the coverage gate issues no request, costs nothing, and
    does not consume the track's assessment slot; the walk moves on. The first candidate
    that actually contacts a model ends that track for this run, so the frozen bound of
    one assessed paper per track per run is unchanged.

    Rejections are still persisted, exactly as before. That is deliberate: it is what
    parks a permanently unavailable manuscript at the retry budget instead of re-probing
    it every day, and it is why the walk does not grow without limit over time.
    """
    from paper_scout.operational_eligibility import TECHNICAL_OUTCOMES
    from paper_scout.operational_preflight import (
        ESTIMATED_OPENROUTER_USD_PER_PAPER, RUN_LEVEL_STOP_REASONS, CostCeilingExceeded)

    summaries = summaries or {}
    consumed: set[str] = set()

    def record_skip(candidate, outcome: str) -> None:
        """Note in the track summary why a nomination produced no assessment."""
        summary = summaries.get(candidate.track)
        if summary is not None:
            summary.skipped_before_model.append(
                {"canonical_id": candidate.canonical_id, "rank": candidate.rank,
                 "outcome": outcome})

    def note_not_walked(candidate, outcome: str) -> None:
        """Account for a nomination that was never tried, so the record reconciles.

        papers_walked + nominees_not_walked must equal the nominated list, or the per-run
        record silently loses candidates and cannot be audited afterwards. Only use this
        for a candidate the walk never reached; one that was tried is already counted in
        papers_walked and needs record_skip alone.
        """
        metrics.nominees_not_walked += 1
        record_skip(candidate, outcome)

    for position, candidate in enumerate(selected):
        if candidate.track in consumed:
            # This track already spent its one model-consuming assessment this run.
            note_not_walked(candidate, "track_slot_consumed")
            continue
        allowed, reason = budget.may_assess(candidate.track)
        if not allowed:
            if reason in RUN_LEVEL_STOP_REASONS:
                print(f"::warning::Stopping the walk: {reason}")
                for remaining in selected[position:]:
                    note_not_walked(remaining, reason)
                return
            consumed.add(candidate.track)
            note_not_walked(candidate, reason)
            continue
        config = configs[candidate.track]
        store = PaperStore(config.sqlite_path)
        rows = store.quality_candidates(days=None, paper_id=candidate.canonical_id)
        if not rows:
            # Nominated from the ranking but absent from the store. Count it, or the walk
            # audit silently loses a nomination: not walked, not skipped, not failed.
            metrics.papers_walked += 1
            metrics.nominees_missing_from_store += 1
            record_skip(candidate, "absent_from_store")
            continue
        canonical_id, paper, decision = rows[0]
        try:
            # Reserve the measured per-paper estimate before any call is issued.
            budget.reserve(candidate.track)
        except CostCeilingExceeded as exc:
            print(f"::warning::Stopping before {candidate.canonical_id}: {exc}")
            for remaining in selected[position:]:
                note_not_walked(remaining, str(exc) or "cost_ceiling_exceeded")
            return
        metrics.papers_walked += 1
        try:
            assessment = assess_and_store_candidate(
                config.quality, store, paper, canonical_id,
                ClassificationResult(0, decision, "Stored relevance classification."),
                curation_path=config.curation_path)
        except Exception as exc:  # noqa: BLE001 - one paper must not stop the run.
            logging.getLogger(__name__).warning("Operational assessment failed for %s: %s",
                                                canonical_id, exc)
            metrics.papers_attempted += 1
            metrics.technical_failures += 1
            metrics.retry_eligible_failures += 1
            # A raise can happen after requests were issued, so this is treated as a
            # model-consuming attempt: charge the estimate rather than zero, and end the
            # track. Walking on could spend a second paper's worth of unaccounted money.
            budget.record(candidate.track,
                          openrouter_usd=ESTIMATED_OPENROUTER_USD_PER_PAPER)
            metrics.unknown_cost_calls += 1
            consumed.add(candidate.track)
            continue
        if assessment is None:
            # Returned only before any model call: the quality path was disabled for this
            # paper, or the credential preflight refused it. Nothing was billed, and
            # reserve() is a pure pre-check that holds no state, so there is no
            # reservation to release and nothing to charge.
            #
            # The track ends anyway, which looks inconsistent with the walk's rule that a
            # free rejection does not consume a slot. It is deliberate: both causes of a
            # None are run-global rather than paper-specific. A disabled quality mode and
            # an unusable credential pair apply identically to every remaining nominee, so
            # walking on would re-fetch five more manuscripts only to refuse them all. The
            # slot is not really spent here — no model ran and the papers stay eligible —
            # the run simply stops asking a question whose answer cannot change.
            metrics.credential_skipped += 1
            consumed.add(candidate.track)
            record_skip(candidate, "scientific_path_unavailable")
            continue
        outcome = (assessment.execution or {}).get("outcome")
        usage = _role_usage(assessment)
        model_calls = usage["gemini_calls"] + usage["openrouter_calls"]
        if model_calls == 0:
            # Rejected by acquisition or the coverage gate before any request. It cost
            # nothing, so it does not consume the track's assessment slot; record why and
            # walk on to the next nominee.
            metrics.skipped_before_model += 1
            # Gate both counters on the same condition. Incrementing technical_failures
            # unconditionally would count an unrecognised outcome as a failure and
            # double-report it alongside the specific counters below.
            if outcome in TECHNICAL_OUTCOMES:
                metrics.technical_failures += 1
                metrics.retry_eligible_failures += 1
            if outcome == "manuscript_unavailable":
                metrics.unavailable_manuscripts += 1
            if outcome == "text_coverage_failure":
                metrics.coverage_failures += 1
            record_skip(candidate, outcome)
            print(f"  walked past {candidate.track} rank={candidate.rank} "
                  f"{candidate.canonical_id}: {outcome} (no model call)")
            continue
        metrics.papers_attempted += 1
        consumed.add(candidate.track)
        budget.record(candidate.track, openrouter_usd=usage["openrouter_usd"],
                      openrouter_calls=usage["openrouter_calls"],
                      gemini_calls=usage["gemini_calls"],
                      gemini_input_tokens=usage["gemini_input"],
                      gemini_output_tokens=usage["gemini_output"])
        metrics.deepseek_calls += usage["openrouter_calls"]
        metrics.deepseek_input_tokens += usage["openrouter_input"]
        metrics.deepseek_output_tokens += usage["openrouter_output"]
        metrics.deepseek_cost_usd += usage["openrouter_usd"]
        metrics.gemini_calls += usage["gemini_calls"]
        metrics.gemini_input_tokens += usage["gemini_input"]
        metrics.gemini_output_tokens += usage["gemini_output"]
        metrics.unknown_cost_calls += usage["unknown_cost_calls"]
        metrics.unattributed_calls += usage["unattributed_calls"]
        if outcome == "success":
            metrics.papers_successfully_assessed += 1
            if assessment.quality_status == "pass":
                metrics.promoted += 1
            else:
                metrics.non_promoted += 1
        else:
            metrics.technical_failures += 1
            if outcome in TECHNICAL_OUTCOMES:
                metrics.retry_eligible_failures += 1
            if outcome == "manuscript_unavailable":
                metrics.unavailable_manuscripts += 1
            if outcome == "text_coverage_failure":
                metrics.coverage_failures += 1


def _role_usage(assessment) -> dict:
    """Per-provider calls, tokens and known money from one assessment receipt.

    Provider attribution comes from the pinned model-to-provider map, not from a substring
    of the model name: stored receipts often carry no provider field, and guessing from
    the name would file an unrecognised model under OpenRouter with no cost.

    A call whose provider reported no price is counted in unknown_cost_calls rather than
    as $0. Treating an unpriced call as free is what would let the per-run ceiling pass
    while real money was being spent, so the run has to be able to see it.
    """
    from paper_scout.promotion_protocol import MODEL_PROVIDERS

    usage = {"openrouter_usd": 0.0, "openrouter_calls": 0, "openrouter_input": 0,
             "openrouter_output": 0, "gemini_calls": 0, "gemini_input": 0,
             "gemini_output": 0, "unknown_cost_calls": 0, "unattributed_calls": 0}
    for call in (assessment.execution or {}).get("calls", []) or []:
        counts = call.get("usage") or {}
        prompt = int(counts.get("prompt_tokens") or 0)
        completion = int(counts.get("completion_tokens") or 0)
        provider = call.get("provider") or MODEL_PROVIDERS.get(call.get("model") or "")
        if provider == "google":
            usage["gemini_calls"] += 1
            usage["gemini_input"] += prompt
            usage["gemini_output"] += completion
            continue
        if provider != "openrouter":
            # An unrecognised provider is recorded as such rather than silently filed
            # under a priced one.
            usage["unattributed_calls"] += 1
        usage["openrouter_calls"] += 1
        usage["openrouter_input"] += prompt
        usage["openrouter_output"] += completion
        price = counts.get("cost", counts.get("cost_usd"))
        if price is None:
            usage["unknown_cost_calls"] += 1
        else:
            usage["openrouter_usd"] += float(price)
    return usage


def _add_track_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--track", choices=list(TRACK_CONFIG_PATHS), default=None)


def _explain_paper(args: argparse.Namespace, config) -> int:
    data_path = Path(args.data_path) if args.data_path else config.docs_dir / "data" / "papers.json"
    if not data_path.exists():
        print(f"papers data not found: {data_path}")
        return 1
    papers = json.loads(data_path.read_text(encoding="utf-8"))
    paper = _find_generated_paper(papers, arxiv_id=args.arxiv_id, doi=args.doi, title=args.title)
    if paper is None:
        print("paper not found")
        return 1
    candidate = _candidate_from_generated_paper(paper)
    result = classify_with_rules(candidate, profile=config.relevance_profile)
    evidence = explain_rule_matches(candidate, profile=config.relevance_profile)
    source_ids = paper.get("source_ids") if isinstance(paper.get("source_ids"), dict) else {}
    print(f"title={candidate.title}")
    print(f"url={candidate.url or ''}")
    print(f"source={candidate.source} source_id={candidate.source_id}")
    print(f"arxiv_id={candidate.arxiv_id or paper.get('arxiv_id') or ''}")
    print(f"source_ids={json.dumps(source_ids, sort_keys=True)}")
    print(f"decision={result.decision}")
    print(f"score={result.score}")
    print(f"tags={', '.join(result.tags)}")
    print(f"reason={result.reason}")
    print(f"include_tags={', '.join(evidence['include_tags'])}")
    print(f"high_confidence_rules={', '.join(evidence['high_confidence_hits']) or 'none'}")
    print(f"agent_context_rules={len(evidence['agent_context_hits'])}")
    print(f"exclude_rules={len(evidence['exclude_hits'])}")
    return 0


def _find_generated_paper(papers: list[dict[str, object]], arxiv_id: str | None, doi: str | None, title: str | None) -> dict[str, object] | None:
    title_query = title.lower() if title else None
    doi_query = doi.lower() if doi else None
    for paper in papers:
        arxiv_values = [str(paper.get("arxiv_id") or "")]
        doi_values = [str(paper.get("doi") or "")]
        source_ids = paper.get("source_ids")
        if isinstance(source_ids, dict):
            arxiv_values.extend(str(value) for value in source_ids.get("arxiv", []) if value)
        alternate_urls = paper.get("alternate_urls")
        if isinstance(alternate_urls, list):
            arxiv_values.extend(str(value) for value in alternate_urls)
            doi_values.extend(str(value) for value in alternate_urls)
        if arxiv_id and any(arxiv_id in value for value in arxiv_values):
            return paper
        if doi_query and any(doi_query in value.lower() for value in doi_values):
            return paper
        if title_query and str(paper.get("title", "")).lower() == title_query:
            return paper
    return None


def _candidate_from_generated_paper(paper: dict[str, object]) -> PaperCandidate:
    authors = paper.get("authors")
    return PaperCandidate(
        title=str(paper.get("title", "")),
        authors=[str(author) for author in authors] if isinstance(authors, list) else [],
        abstract=str(paper.get("abstract") or paper.get("abstract_summary") or ""),
        source=str(paper.get("source") or "generated"),
        source_id=str(paper.get("source_id") or paper.get("canonical_id") or ""),
        doi=str(paper.get("doi") or "") or None,
        arxiv_id=str(paper.get("arxiv_id") or "") or None,
        semantic_scholar_id=str(paper.get("semantic_scholar_id") or "") or None,
        openalex_id=str(paper.get("openalex_id") or "") or None,
        url=str(paper.get("url") or "") or None,
        published_date=str(paper.get("publication_date") or "") or None,
        raw=paper,
    )


def _fetch_direct_paper(args: argparse.Namespace) -> PaperCandidate | None:
    from paper_scout.ingestion import fetch_direct_paper
    return fetch_direct_paper(arxiv_id=args.arxiv_id, doi=args.doi, url=args.url)


def _batch_population(args) -> int:
    """Build or verify the deterministic eligible-population manifest.

    Building persists the ordered identities themselves next to their digest, before any
    scientific model call, so a later run can rebuild the population and compare it item
    by item.

    Verification always covers exactly what the manifest committed to. The tracks, the
    exclusion scope, the pinned build time and the frozen rosters all come from the
    manifest, so none of them can be narrowed from the command line, and the configured
    state, curation and digest locations are compared against the recorded ones.

    Exclusions are always read from every track, whatever is being built: one manuscript
    can be discovered by more than one track, and restricting a build must narrow what
    the manifest contains rather than what it excludes.
    """
    rosters = tuple(Path(path) for path in args.roster)
    if args.verify:
        for name, value in (("--roster", rosters), ("--population-track", args.population_tracks)):
            if value:
                raise SystemExit(f"{name} is not used with --verify; verification covers "
                                 "exactly the tracks, rosters and build time the manifest records")
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        scanned = tuple(manifest["sources"]["exclusion_tracks"])
        built = tuple(manifest["sources"]["tracks"])
        # A manifest naming an unknown track, or a built track outside its own exclusion
        # scope, cannot be verified. Say so rather than failing on a lookup deeper in.
        unverifiable = sorted({*scanned, *built} - set(TRACKS) | (set(built) - set(scanned)))
        if unverifiable:
            raise SystemExit("this manifest cannot be verified: it names "
                             + ", ".join(unverifiable)
                             + " outside the tracks its own exclusion scope covers")
        recorded = track_configs(Path(args.config), scanned)
        result = verify_manifest(manifest, {track: recorded[track] for track in built}, recorded)
        for track, detail in sorted(result.tracks.items()):
            print(f"{track} ordered_ids_match={detail['ordered_ids_match']} "
                  f"population_sha256_match={detail['population_sha256_match']} "
                  f"stored={detail['stored_count']} rebuilt={detail['rebuilt_count']}")
        print(f"self_consistent={result.self_consistent} sources_match={result.sources_match} "
              f"reproduced={result.reproduced} "
              f"stored={result.stored_digest} rebuilt={result.rebuilt_digest}")
        return 0 if result.reproduced and result.self_consistent else 1
    # The ranking's newness key reads the build time, so an unpinned build bakes in
    # wall-clock time and two builds of identical state can order differently. A
    # manifest is a commitment, so the time is pinned explicitly rather than defaulted.
    if not args.build_time:
        raise SystemExit("--build-time is required to build a manifest, so the population "
                         "is pinned to a stated time rather than to the clock")
    tracks = tuple(args.population_tracks) or TRACKS
    exclusion_configs = track_configs(Path(args.config), TRACKS)
    configs = {track: exclusion_configs[track] for track in tracks}
    population = build_population(configs, args.build_time, rosters, exclusion_configs)
    manifest = population_manifest(population, repository_code_sha())
    path = write_manifest(Path(args.manifest), manifest)
    for track in population.tracks:
        print(f"{track.track} ranked={track.ranked_count} eligible={len(track.eligible)} "
              f"excluded={len(track.excluded)} population_sha256={track.population_sha256}")
    print(f"manifest={path} manifest_sha256={manifest['manifest_sha256']} "
          f"code_sha={manifest['code_sha']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
