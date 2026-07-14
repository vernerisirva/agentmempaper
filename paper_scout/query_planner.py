from __future__ import annotations

from dataclasses import dataclass
import logging
import re

from paper_scout.config import DiscoveryQuery, ScoutConfig

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class PlannedQuery:
    source: str
    query: str
    provider_query: str
    mode: str
    route: str = "keyword"
    max_results: int | None = None
    days_override: int | None = None

    @property
    def normalized_query(self) -> str:
        return normalize_query(self.provider_query)


def plan_queries(config: ScoutConfig, sources: set[str] | None = None, include_sweep: bool = True) -> list[PlannedQuery]:
    planned: list[PlannedQuery] = []
    active_sources = sources or set(config.discovery_queries)
    for source in sorted(active_sources):
        budget = max(0, int(config.query_budgets.get(source, 5)))
        source_queries: list[PlannedQuery] = []
        seen: set[str] = set()
        configured = config.discovery_queries.get(source, ())
        if not configured:
            configured = tuple(DiscoveryQuery(term, "all_terms") for term in config.terms)
        for query in configured:
            item = build_query(source, query)
            if item.normalized_query in seen:
                continue
            seen.add(item.normalized_query)
            source_queries.append(item)
        if source == "arxiv" and include_sweep and config.arxiv_sweep.enabled and config.arxiv_sweep.categories:
            category_query = " OR ".join(f"cat:{category}" for category in config.arxiv_sweep.categories)
            sweep = PlannedQuery(
                source="arxiv",
                query=",".join(config.arxiv_sweep.categories),
                provider_query=category_query,
                mode="raw",
                route="category_sweep",
                max_results=config.arxiv_sweep.max_results,
                days_override=config.arxiv_sweep.days,
            )
            if sweep.normalized_query not in seen:
                source_queries.append(sweep)
        selected = source_queries[:budget]
        LOGGER.info("%s planned queries: %s (budget %s)", source, len(selected), budget)
        for item in selected:
            LOGGER.debug("Planned %s query [%s/%s]: %s", source, item.route, item.mode, item.provider_query)
        planned.extend(selected)
    return planned


def build_query(source: str, spec: DiscoveryQuery) -> PlannedQuery:
    mode = spec.mode.strip().lower() or "all_terms"
    if mode not in {"phrase", "all_terms", "raw"}:
        raise ValueError(f"unsupported discovery query mode: {spec.mode}")
    if source != "arxiv":
        provider_query = spec.query
    elif mode == "phrase":
        provider_query = f'all:"{spec.query.strip()}"'
    elif mode == "all_terms":
        terms = _query_terms(spec.query)
        provider_query = " AND ".join(f"all:{term}" for term in terms)
    else:
        provider_query = spec.query.strip()
    return PlannedQuery(source=source, query=spec.query.strip(), provider_query=provider_query, mode=mode)


def normalize_query(value: str) -> str:
    return " ".join(value.lower().split())


def _query_terms(value: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+", value)
