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
        result = run_scout(config, digest_date=args.date, notifications_enabled=not args.no_notify)
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
        result = run_backfill(config, days=backfill_days, sources=sources, report_date=args.date)
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
