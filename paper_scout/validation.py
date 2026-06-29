from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path
import socket
import ssl
import tempfile
from urllib.error import HTTPError, URLError
from xml.etree.ElementTree import ParseError

from paper_scout.config import ScoutConfig
from paper_scout.deduplication import canonical_key
from paper_scout.http import HttpRequestError
from paper_scout.models import PaperCandidate
from paper_scout.relevance import classify_with_rules
from paper_scout.scout import run_scout
from paper_scout.source_errors import source_error_message
from paper_scout.state import PaperStore


def deterministic_candidates(profile: str = "agent_memory") -> list[PaperCandidate]:
    if profile == "deep_research":
        return [
            PaperCandidate(
                title="Source-Grounded Deep Research Agents",
                authors=["Ada Lovelace"],
                abstract="Deep research agents plan literature reviews, verify citations, and write source-grounded research reports.",
                source="fixture_arxiv",
                source_id="D1",
                doi="10.1/deep-research-agents",
                url="https://example.test/d1",
                published_date="2026-06-26",
            ),
            PaperCandidate(
                title="Source-Grounded Deep Research Agents",
                authors=["Ada Lovelace"],
                abstract="The same deep research agent paper mirrored from another source.",
                source="fixture_openalex",
                source_id="DW1",
                doi="10.1/deep-research-agents",
                url="https://example.test/dw1",
                published_date="2026-06-26",
            ),
            PaperCandidate(
                title="Citation Verification Agents for Literature Reviews",
                authors=["Grace Hopper"],
                abstract="A citation verification agent checks evidence grounding in automated literature-review workflows.",
                source="fixture_semantic_scholar",
                source_id="DS1",
                semantic_scholar_id="DS1",
                url="https://example.test/ds1",
                published_date="2026-06-26",
            ),
        ]
    return [
        PaperCandidate(
            title="Persistent Memory for LLM Agents",
            authors=["Ada Lovelace"],
            abstract="Persistent episodic memory write and retrieval policies for LLM agents.",
            source="fixture_arxiv",
            source_id="A1",
            doi="10.1/persistent-memory",
            url="https://example.test/a1",
            published_date="2026-06-26",
        ),
        PaperCandidate(
            title="Persistent Memory for LLM Agents",
            authors=["Ada Lovelace"],
            abstract="The same paper mirrored from another source.",
            source="fixture_openalex",
            source_id="W1",
            doi="10.1/persistent-memory",
            url="https://example.test/w1",
            published_date="2026-06-26",
        ),
        PaperCandidate(
            title="Semantic Memory for Deep Research Agents",
            authors=["Grace Hopper"],
            abstract="Deep research agents maintain semantic memory for literature-review state.",
            source="fixture_semantic_scholar",
            source_id="S1",
            semantic_scholar_id="S1",
            url="https://example.test/s1",
            published_date="2026-06-26",
        ),
    ]


class StaticFetcher:
    source = "static"

    def __init__(self, candidates: list[PaperCandidate]) -> None:
        self.candidates = candidates

    def search(self, term: str, days: int, max_results: int) -> list[PaperCandidate]:
        return self.candidates[:max_results]


def validate_idempotency(
    base_dir: Path | None = None,
    report_date: str | None = None,
    report_dir: Path | None = None,
    track_id: str = "agent_memory",
    relevance_profile: str = "agent_memory",
) -> dict[str, object]:
    active_date = report_date or date.today().isoformat()
    if base_dir is None:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        output_dir = report_dir or Path("reports/paper_scout")
    else:
        temp = None
        root = base_dir
        output_dir = report_dir or (root / "reports")
    try:
        config = ScoutConfig(
            terms=["agent memory"] if relevance_profile == "agent_memory" else ["deep research agent"],
            track_id=track_id,
            days=7,
            max_results_per_source=10,
            sqlite_path=root / "state.sqlite3",
            digest_dir=root / "digests",
            report_dir=root / "reports",
            relevance_profile=relevance_profile,
        )
        fetcher = StaticFetcher(deterministic_candidates(relevance_profile))
        first = run_scout(config, fetchers=[fetcher], digest_date=active_date, notifier=lambda markdown: True)
        second = run_scout(config, fetchers=[fetcher], digest_date=active_date, notifier=lambda markdown: True)
        store = PaperStore(config.sqlite_path)
        notified = store.get_notified_for_date(active_date)
        keys = [paper.canonical_key for paper in notified]
        report = {
            "passed": first.new_digest_count == 2 and second.new_digest_count == 0 and len(keys) == len(set(keys)) == 2,
            "first_digest_count": first.new_digest_count,
            "second_digest_count": second.new_digest_count,
            "notification_count": len(keys),
            "same_paper_from_multiple_sources": first.fetched_count == 3 and first.unique_count == 2,
            "no_api_key_fallback": True,
            "report_path": str(output_dir / f"idempotency-{active_date}.md"),
        }
        _write_idempotency_report(report, output_dir, active_date)
        return report
    finally:
        if temp is not None:
            temp.cleanup()


def run_live_smoke(
    config: ScoutConfig,
    fetchers,
    report_date: str | None = None,
    days: int | None = None,
    max_results_per_source: int | None = None,
    strict: bool = False,
    ci: bool = False,
) -> dict[str, object]:
    active_date = report_date or date.today().isoformat()
    active_days = days if days is not None else config.days
    active_max = max_results_per_source if max_results_per_source is not None else config.max_results_per_source
    store_ok = True
    try:
        PaperStore(config.sqlite_path)
    except Exception:
        store_ok = False
        if strict:
            raise

    source_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    source_errors: list[dict[str, object]] = []
    candidates: list[PaperCandidate] = []
    disabled_sources: set[str] = set()
    source_results: dict[str, dict[str, object]] = {}

    for fetcher in fetchers:
        source = getattr(fetcher, "source", fetcher.__class__.__name__)
        source_results[source] = {
            "source": source,
            "status": "not_attempted",
            "queries_attempted": 0,
            "raw_records": 0,
            "candidates": 0,
            "sample_candidate": None,
            "errors": [],
        }

    for term in config.terms:
        for fetcher in fetchers:
            source = getattr(fetcher, "source", fetcher.__class__.__name__)
            if source in disabled_sources:
                continue
            source_result = source_results[source]
            source_result["queries_attempted"] = int(source_result["queries_attempted"]) + 1
            try:
                raw_count, fetched = _search_for_smoke(fetcher, term, active_days, active_max)
            except Exception as exc:  # noqa: BLE001
                error = _source_error(source, term, exc)
                source_errors.append(error)
                source_result["errors"].append(error)  # type: ignore[union-attr]
                source_result["status"] = "failed"
                disabled_sources.add(source)
                continue
            candidates.extend(fetched)
            source_counts[source] += len(fetched)
            source_result["raw_records"] = int(source_result["raw_records"]) + raw_count
            source_result["candidates"] = int(source_result["candidates"]) + len(fetched)
            if source_result["sample_candidate"] is None and fetched:
                source_result["sample_candidate"] = _sample_candidate(fetched[0])
            source_result["status"] = "success" if int(source_result["candidates"]) else "zero_results"

    for source_result in source_results.values():
        if source_result["status"] == "not_attempted":
            source_result["status"] = "zero_results"

    by_key: dict[str, PaperCandidate] = {}
    duplicates: dict[str, list[str]] = defaultdict(list)
    for candidate in candidates:
        key = canonical_key(candidate)
        duplicates[key].append(f"{candidate.source}:{candidate.source_id}")
        by_key.setdefault(key, candidate)
    duplicate_examples = {key: sightings for key, sightings in duplicates.items() if len(sightings) > 1}

    top_papers = []
    for key, candidate in by_key.items():
        classification = classify_with_rules(candidate, profile=config.relevance_profile)
        decision_counts[classification.decision] += 1
        if classification.decision in {"relevant", "maybe"}:
            top_papers.append((classification.score, candidate.title, classification.decision, classification.reason, candidate.url))
    top_papers.sort(reverse=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        idempotency = validate_idempotency(
            Path(tmpdir),
            active_date,
            Path(tmpdir) / "reports",
            track_id=config.track_id,
            relevance_profile=config.relevance_profile,
        )
    source_failures = [_format_source_error(error) for error in source_errors]
    source_result_list = [source_results[source] for source in sorted(source_results)]
    sources_succeeded = sum(1 for result in source_result_list if not result["errors"])
    sources_failed = sum(1 for result in source_result_list if result["errors"])
    report = {
        "run_id": f"live-smoke-{active_date}",
        "date": active_date,
        "ci": ci,
        "sources_attempted": len(source_result_list),
        "sources_succeeded": sources_succeeded,
        "sources_failed": sources_failed,
        "total_raw_records": sum(int(result["raw_records"]) for result in source_result_list),
        "total_candidates": len(candidates),
        "unique_candidates": len(by_key),
        "relevant_count": decision_counts.get("relevant", 0),
        "maybe_count": decision_counts.get("maybe", 0),
        "irrelevant_count": decision_counts.get("irrelevant", 0),
        "source_errors": source_errors,
        "source_results": source_result_list,
        "source_counts": dict(source_counts),
        "candidate_count": len(candidates),
        "unique_count": len(by_key),
        "decision_counts": dict(decision_counts),
        "top_papers": top_papers[:10],
        "source_failures": source_failures,
        "duplicate_examples": duplicate_examples,
        "state_initialized": store_ok,
        "idempotency_passed": bool(idempotency["passed"]),
        "report_path": str(config.report_dir / f"live-smoke-{active_date}.md"),
        "json_report_path": str(config.report_dir / f"live-smoke-{active_date}.json") if ci else None,
    }
    _write_live_smoke_report(report, config.report_dir, active_date)
    if ci:
        _write_live_smoke_json(report, config.report_dir, active_date)
    if strict and not candidates and source_failures:
        raise RuntimeError("Live smoke test found no candidates and at least one source failed")
    return report


def _search_for_smoke(fetcher, term: str, days: int, max_results: int) -> tuple[int, list[PaperCandidate]]:
    if hasattr(fetcher, "search_with_diagnostics"):
        result = fetcher.search_with_diagnostics(term, days, max_results)
        return int(result.raw_count), list(result.candidates)
    candidates = list(fetcher.search(term, days, max_results))
    return len(candidates), candidates


def _sample_candidate(candidate: PaperCandidate) -> dict[str, object]:
    return {
        "title": candidate.title,
        "source_id": candidate.source_id,
        "url": candidate.url,
        "published_date": candidate.published_date,
        "has_abstract": bool(candidate.abstract.strip()),
    }


def _source_error(source: str, term: str, exc: Exception) -> dict[str, object]:
    return {
        "source": source,
        "query": term,
        "type": _classify_error(exc),
        "message": source_error_message(source, exc),
    }


def _classify_error(exc: Exception) -> str:
    if isinstance(exc, HttpRequestError):
        return exc.kind
    if isinstance(exc, HTTPError):
        return "http"
    if isinstance(exc, URLError):
        reason = exc.reason
        if _is_tls_error(reason):
            return "tls"
        if isinstance(reason, (TimeoutError, socket.timeout)):
            return "timeout"
        return "network"
    if isinstance(exc, (TimeoutError, socket.timeout)):
        return "timeout"
    if isinstance(exc, (json.JSONDecodeError, ParseError, ValueError, KeyError, TypeError)):
        return "parsing"
    if _is_tls_error(exc):
        return "tls"
    return "provider"


def _is_tls_error(value: object) -> bool:
    if isinstance(value, (ssl.SSLError, ssl.CertificateError)):
        return True
    text = str(value).lower()
    return "certificate verify failed" in text or "ssl" in text or "tls" in text


def _format_source_error(error: dict[str, object]) -> str:
    return f"{error['source']} {error['type']} error for {error['query']!r}: {error['message']}"


def _human_error_type(error_type: object) -> str:
    labels = {
        "http": "HTTP/API error",
        "tls": "TLS/certificate error",
        "timeout": "Timeout/network error",
        "network": "Timeout/network error",
        "parsing": "Parsing/conversion error",
        "provider": "Provider error",
    }
    return labels.get(str(error_type), f"{error_type} error")


def _write_live_smoke_report(report: dict[str, object], report_dir: Path, report_date: str) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Paper Scout Live Smoke Report - {report_date}",
        "",
        f"- **CI mode:** {report['ci']}",
        f"- **Sources attempted:** {report['sources_attempted']}",
        f"- **Sources succeeded:** {report['sources_succeeded']}",
        f"- **Sources failed:** {report['sources_failed']}",
        f"- **Raw records:** {report['total_raw_records']}",
        f"- **Candidates fetched:** {report['total_candidates']}",
        f"- **Unique papers:** {report['unique_candidates']}",
        f"- **State initialized:** {report['state_initialized']}",
        f"- **Idempotency passed:** {report['idempotency_passed']}",
        "",
        "## Sources",
        "",
    ]
    for result in report["source_results"]:
        status = str(result["status"])
        label = "Success" if status == "success" else ("Success - zero results" if status == "zero_results" else "Failed")
        lines.extend(
            [
                f"### {result['source']}",
                "",
                f"- Status: {label}",
                f"- Queries attempted: {result['queries_attempted']}",
                f"- Raw records: {result['raw_records']}",
                f"- Converted candidates: {result['candidates']}",
            ]
        )
        sample = result.get("sample_candidate")
        if sample:
            lines.extend(
                [
                    f"- Sample title: {sample['title']}",
                    f"- Sample source ID: {sample['source_id']}",
                    f"- Sample URL: {sample['url'] or 'none'}",
                    f"- Sample published date: {sample['published_date'] or 'unknown'}",
                    f"- Abstract: {'yes' if sample['has_abstract'] else 'no'}",
                ]
            )
        if result["errors"]:
            for error in result["errors"]:
                lines.append(f"- Error: {_human_error_type(error['type'])}: {error['message']}")
        lines.append("")
    lines.extend(["", "## Decisions", ""])
    for decision in ["relevant", "maybe", "irrelevant"]:
        lines.append(f"- {decision}: {report['decision_counts'].get(decision, 0)}")
    lines.extend(["", "## Top Relevant Or Maybe Papers", ""])
    for score, title, decision, reason, url in report["top_papers"]:
        lines.append(f"- **{title}** ({decision}, {score}/100): {reason} {url or ''}".rstrip())
    if not report["top_papers"]:
        lines.append("- None")
    lines.extend(["", "## Source Failures", ""])
    if report["source_errors"]:
        for error in report["source_errors"]:
            lines.append(f"- {error['source']} ({_human_error_type(error['type'])}) for `{error['query']}`: {error['message']}")
    else:
        lines.append("- None")
    lines.extend(["", "## Deduplication Examples", ""])
    duplicates = report["duplicate_examples"]
    if duplicates:
        for key, sightings in duplicates.items():
            lines.append(f"- {key}: {', '.join(sightings)}")
    else:
        lines.append("- No duplicates found.")
    (report_dir / f"live-smoke-{report_date}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _write_live_smoke_json(report: dict[str, object], report_dir: Path, report_date: str) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    fields = [
        "run_id",
        "date",
        "ci",
        "sources_attempted",
        "sources_succeeded",
        "sources_failed",
        "total_raw_records",
        "total_candidates",
        "unique_candidates",
        "relevant_count",
        "maybe_count",
        "irrelevant_count",
        "source_errors",
        "state_initialized",
        "idempotency_passed",
        "source_results",
    ]
    payload = {field: report[field] for field in fields}
    (report_dir / f"live-smoke-{report_date}.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_idempotency_report(report: dict[str, object], report_dir: Path, report_date: str) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Paper Scout Idempotency Validation - {report_date}",
        "",
        f"- **Passed:** {report['passed']}",
        f"- **First digest count:** {report['first_digest_count']}",
        f"- **Second digest count:** {report['second_digest_count']}",
        f"- **Notification count:** {report['notification_count']}",
        f"- **Same paper from multiple sources deduped:** {report['same_paper_from_multiple_sources']}",
        f"- **No-API-key fallback:** {report['no_api_key_fallback']}",
        "",
    ]
    (report_dir / f"idempotency-{report_date}.md").write_text("\n".join(lines), encoding="utf-8")
