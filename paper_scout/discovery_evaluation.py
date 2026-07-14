from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from paper_scout.config import ScoutConfig
from paper_scout.query_planner import PlannedQuery, plan_queries


@dataclass(frozen=True)
class DiscoveryFixture:
    name: str
    title: str
    abstract: str
    arxiv_id: str | None
    categories: tuple[str, ...]
    expected_routes: tuple[str, ...]


def discovery_fixtures() -> list[DiscoveryFixture]:
    return [
        DiscoveryFixture(
            "procedural-memory-distillation",
            "Procedural Memory Distillation: Online Reflection for Self-Improving Language Models",
            "Cross-episode signals are converted into reusable procedural memory and distilled into model weights through online reflection.",
            "2607.01480",
            ("cs.CL", "cs.AI"),
            ("keyword", "category_sweep", "direct_id"),
        ),
        DiscoveryFixture("agent-native-memory", "Are We Ready For An Agent-Native Memory System?", "An agent memory system for LLM agents.", "2606.24775", ("cs.AI",), ("keyword", "category_sweep", "direct_id")),
        DiscoveryFixture("persistent-agent-memory", "Persistent Memory for LLM Agents", "Long-term memory for language model agents.", None, ("cs.AI",), ("keyword", "category_sweep")),
        DiscoveryFixture("procedural-agent-memory", "Procedural Memory for Language Agents", "Procedural memory supports recurring agent workflows.", None, ("cs.CL",), ("keyword", "category_sweep")),
        DiscoveryFixture("engram-parametric-memory", "Engram Parametric Memory for Language Models", "Parametric memory mechanisms for language model behavior.", None, ("cs.CL",), ("keyword", "category_sweep")),
        DiscoveryFixture("memory-security-benchmark", "Agent Memory Security Benchmark", "A benchmark for poisoning attacks on persistent LLM-agent memory.", None, ("cs.AI",), ("keyword", "category_sweep")),
    ]


def evaluate_discovery(config: ScoutConfig) -> dict[str, object]:
    planned = plan_queries(config)
    results = []
    caught = 0
    for fixture in discovery_fixtures():
        routes = _routes_for_fixture(fixture, planned, config)
        discovered = bool(routes)
        caught += int(discovered)
        results.append({"name": fixture.name, "title": fixture.title, "discovered": discovered, "routes": routes})
    fixtures = discovery_fixtures()
    return {
        "fixture_count": len(fixtures),
        "discovered_count": caught,
        "recall": caught / len(fixtures) if fixtures else 1.0,
        "missed": [item["name"] for item in results if not item["discovered"]],
        "results": results,
        "query_plan_counts": {source: sum(1 for query in planned if query.source == source) for source in sorted({query.source for query in planned})},
    }


def write_discovery_report(report: dict[str, object], report_dir: Path, report_date: str) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"discovery-eval-{report_date}.md"
    lines = [
        f"# Discovery regression evaluation - {report_date}",
        "",
        "> Fixture-based regression coverage only; this does not estimate production literature-discovery recall.",
        "",
        f"- Discovery recall: {float(report['recall']):.3f} ({report['discovered_count']}/{report['fixture_count']})",
        f"- Missed fixtures: {', '.join(report['missed']) if report['missed'] else 'none'}",
        "- Query plan: " + ", ".join(f"{source}={count}" for source, count in report["query_plan_counts"].items()),
        "",
        "## Fixtures",
        "",
    ]
    for item in report["results"]:
        routes = ", ".join(item["routes"]) if item["routes"] else "missed"
        lines.append(f"- **{item['title']}**: {routes}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _routes_for_fixture(fixture: DiscoveryFixture, planned: list[PlannedQuery], config: ScoutConfig) -> list[str]:
    text = f"{fixture.title} {fixture.abstract}".lower()
    routes: set[str] = set()
    for query in planned:
        if query.route == "category_sweep":
            if set(fixture.categories).intersection(config.arxiv_sweep.categories):
                routes.add("category_sweep")
            continue
        terms = _terms(query.query)
        if terms and all(term in text for term in terms):
            routes.add("keyword")
    if fixture.arxiv_id:
        routes.add("direct_id")
    return sorted(routes)


def _terms(value: str) -> list[str]:
    return re.findall(r"[a-z0-9][a-z0-9_-]*", value.lower())
