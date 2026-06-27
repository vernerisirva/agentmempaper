from __future__ import annotations

import argparse
import json
import logging
from datetime import date
from pathlib import Path

from paper_scout.config import load_config
from paper_scout.digest import write_digest
from paper_scout.evaluation import evaluate_relevance_examples, relevance_fixture_examples, write_relevance_report
from paper_scout.fetchers import ArxivFetcher, OpenAlexFetcher, SemanticScholarFetcher
from paper_scout.models import PaperCandidate
from paper_scout.relevance import classify_with_rules, explain_rule_matches
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

    explain_parser = subparsers.add_parser("explain-paper", help="Explain deterministic relevance rules for a generated paper")
    explain_parser.add_argument("--arxiv-id")
    explain_parser.add_argument("--title")
    explain_parser.add_argument("--data-path", default="docs/data/papers.json")

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

    if args.command == "explain-paper":
        return _explain_paper(args)

    parser.error(f"unknown command {args.command}")
    return 2


def _explain_paper(args: argparse.Namespace) -> int:
    data_path = Path(args.data_path)
    if not data_path.exists():
        print(f"papers data not found: {data_path}")
        return 1
    papers = json.loads(data_path.read_text(encoding="utf-8"))
    paper = _find_generated_paper(papers, arxiv_id=args.arxiv_id, title=args.title)
    if paper is None:
        print("paper not found")
        return 1
    candidate = _candidate_from_generated_paper(paper)
    result = classify_with_rules(candidate)
    evidence = explain_rule_matches(candidate)
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


def _find_generated_paper(papers: list[dict[str, object]], arxiv_id: str | None, title: str | None) -> dict[str, object] | None:
    title_query = title.lower() if title else None
    for paper in papers:
        arxiv_values = [str(paper.get("arxiv_id") or "")]
        source_ids = paper.get("source_ids")
        if isinstance(source_ids, dict):
            arxiv_values.extend(str(value) for value in source_ids.get("arxiv", []) if value)
        alternate_urls = paper.get("alternate_urls")
        if isinstance(alternate_urls, list):
            arxiv_values.extend(str(value) for value in alternate_urls)
        if arxiv_id and any(arxiv_id in value for value in arxiv_values):
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


if __name__ == "__main__":
    raise SystemExit(main())
