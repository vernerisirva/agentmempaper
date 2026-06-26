from __future__ import annotations

import argparse
import logging
from datetime import date

from paper_scout.config import load_config
from paper_scout.digest import write_digest
from paper_scout.evaluation import evaluate_relevance_examples, relevance_fixture_examples, write_relevance_report
from paper_scout.fetchers import ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher
from paper_scout.relevance import classify_with_rules
from paper_scout.scout import run_scout, search_sources
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

    search_parser = subparsers.add_parser("search", help="Fetch candidates without writing state")
    search_parser.add_argument("--days", type=int, default=None)

    digest_parser = subparsers.add_parser("digest", help="Render a digest from stored notifications")
    digest_parser.add_argument("--date", required=True)

    mark_parser = subparsers.add_parser("mark-notified", help="Mark all current relevant/maybe papers as notified")
    mark_parser.add_argument("--date", default=date.today().isoformat())

    eval_parser = subparsers.add_parser("evaluate-relevance", help="Evaluate deterministic relevance rules on fixture papers")
    eval_parser.add_argument("--date", default=date.today().isoformat())
    eval_parser.add_argument("--with-llm", action="store_true", help="Also use the optional LLM classifier when configured")

    smoke_parser = subparsers.add_parser("smoke-live", help="Run live source checks without notification side effects")
    smoke_parser.add_argument("--days", type=int, default=14)
    smoke_parser.add_argument("--max-results-per-source", type=int, default=25)
    smoke_parser.add_argument("--no-notify", action="store_true")
    smoke_parser.add_argument("--strict", action="store_true")
    smoke_parser.add_argument("--ci", action="store_true", help="Write CI-friendly JSON output alongside Markdown")
    smoke_parser.add_argument("--date", default=date.today().isoformat())

    idem_parser = subparsers.add_parser("validate-idempotency", help="Validate duplicate notification protection")
    idem_parser.add_argument("--date", default=date.today().isoformat())

    build_site_parser = subparsers.add_parser("build-site", help="Build the static Paper Scout dashboard under docs/")
    build_site_parser.add_argument("--docs-dir", default="docs")

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(message)s")
    config = load_config(args.config)

    if args.command == "run":
        result = run_scout(config, digest_date=args.date)
        print(f"run_id={result.run_id} fetched={result.fetched_count} unique={result.unique_count} digest_items={result.new_digest_count} digest={result.digest_path}")
        return 0

    if args.command == "search":
        candidates = search_sources(config, days=args.days)
        for candidate in candidates:
            classification = classify_with_rules(candidate)
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
        report = evaluate_relevance_examples(relevance_fixture_examples(), use_llm=args.with_llm)
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
        report = validate_idempotency(report_date=args.date, report_dir=config.report_dir)
        print(f"passed={report['passed']} first={report['first_digest_count']} second={report['second_digest_count']} report={report['report_path']}")
        return 0 if report["passed"] else 1

    if args.command == "build-site":
        result = build_site(digest_dir=config.digest_dir, report_dir=config.report_dir, docs_dir=args.docs_dir, state_path=config.sqlite_path)
        print(result.message)
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
