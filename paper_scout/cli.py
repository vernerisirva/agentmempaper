from __future__ import annotations

import argparse
import json
import logging
import os
import re
from dataclasses import replace
from datetime import date
from pathlib import Path

from paper_scout.config import load_config
from paper_scout.discovery_evaluation import evaluate_discovery, write_discovery_report
from paper_scout.digest import write_digest
from paper_scout.evaluation import evaluate_relevance_examples, relevance_fixture_examples, write_relevance_report
from paper_scout.fetchers import ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.relevance import classify_with_rules, explain_rule_matches
from paper_scout.quality_evaluation import evaluate_quality_fixtures, write_quality_evaluation_report
from paper_scout.quality_report import write_paper_quality_report
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

    quality_eval_parser = subparsers.add_parser("evaluate-quality", help="Evaluate deterministic scholarly-quality rules on fixture papers")
    quality_eval_parser.add_argument("--date", default=date.today().isoformat())
    _add_track_argument(quality_eval_parser)

    reassess_parser = subparsers.add_parser("reassess-quality", help="Assess or reassess stored relevant papers")
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
    track_id = getattr(args, "track", None) or "agent_memory"
    config = load_config(args.config, track_id=track_id)

    if args.command == "run":
        result = run_scout(config, digest_date=args.date)
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
        return 0 if not report["false_positives"] and not report["false_negatives"] else 1

    if args.command == "smoke-live":
        report = run_live_smoke(
            config,
            fetchers=[ArxivFetcher(), SemanticScholarFetcher(), OpenAlexFetcher()],
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
        )
        print(result.message)
        return 0

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
        result = run_backfill(config, days=args.days, sources=sources, report_date=args.date)
        print(f"run_id={result.run_id} fetched={result.fetched_count} unique={result.unique_count} report={result.digest_path}")
        return 0

    if args.command == "failed-queries":
        store = PaperStore(config.sqlite_path)
        rows = store.failed_queries(config.track_id, include_resolved=args.include_resolved)
        for row in rows:
            print(f"{row['source']} attempts={row['attempt_count']} days={row['requested_days']} next={row['next_retry_at']} resolved={row['resolved_at'] or '-'} query={row['normalized_query']}")
        print(f"count={len(rows)}")
        return 0

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
        assessment_config = replace(
            config.quality.assessment,
            version=args.assessment_version or config.quality.assessment.version,
            rubric_version=args.rubric_version or config.quality.assessment.rubric_version,
        )
        quality_config = replace(config.quality, mode=args.mode or config.quality.mode, assessment=assessment_config)
        if args.model:
            os.environ["PAPER_SCOUT_QUALITY_LLM_MODEL"] = args.model
        stats = QualityRunStats()
        store = PaperStore(config.sqlite_path)
        if args.report_only:
            for assessment in store.list_current_quality_assessments():
                stats.record(assessment, cache_hit=True)
        else:
            for canonical_id, candidate, decision in store.quality_candidates(days=args.days, paper_id=args.paper_id):
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
    parser.add_argument("--track", choices=["agent_memory", "deep_research"], default="agent_memory")


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
    arxiv_id = args.arxiv_id
    doi = args.doi
    url = args.url
    if url and not arxiv_id:
        match = re.search(r"arxiv\.org/(?:abs|pdf)/([^?#/]+)", url, flags=re.I)
        if match:
            arxiv_id = match.group(1).removesuffix(".pdf")
    if url and not doi:
        match = re.search(r"(?:doi\.org/)?(10\.\d{4,9}/[^?#\s]+)", url, flags=re.I)
        if match:
            doi = match.group(1)
    if arxiv_id:
        try:
            return ArxivFetcher().fetch_by_id(arxiv_id)
        except Exception:
            return OpenAlexFetcher().fetch_by_doi(f"10.48550/arXiv.{arxiv_id}")
    if doi:
        try:
            return SemanticScholarFetcher().fetch_by_identifier(f"DOI:{doi}")
        except Exception:
            return OpenAlexFetcher().fetch_by_doi(doi)
    raise ValueError("ingest-paper requires --arxiv-id, --doi, or a supported --url")


if __name__ == "__main__":
    raise SystemExit(main())
