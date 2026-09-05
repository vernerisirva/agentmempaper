from __future__ import annotations

from dataclasses import dataclass, field
import os
import posixpath
from pathlib import Path


DEFAULT_TERMS = [
    "agent memory",
    "agentic memory",
    "LLM agent memory",
    "long-term memory agents",
    "persistent memory agents",
    "episodic memory LLM agent",
    "semantic memory LLM agent",
    "procedural memory LLM agent",
    "memory-augmented language agent",
    "memory write policy agent",
    "memory retrieval policy agent",
    "agent-native memory",
    "agent native memory",
    "agent memory system",
    "agent memory systems",
    "LLM agent memory system",
    "memory system for LLM agents",
    "memory module LLM agent",
    "persistent memory LLM agent",
    "long-term memory LLM agent",
    "memory retrieval LLM agent",
    "memory consolidation LLM agent",
    "agent memory evaluation",
    "agent memory benchmark",
    "deep research agent",
    "deep research agents",
    "deep research memory",
    "deep research agent memory",
    "agentic memory deep research",
    "autonomous research agent memory",
    "literature review agent memory",
    "research agent long-term memory",
    "parametric memory LLM",
    "Engram LLM",
    "Engram memory LLM",
    "multilingual Engram",
    "Megatron-LM Engram",
    "memory mechanism language model",
]

DEFAULT_EXCLUSIONS = [
    "GPU memory",
    "CUDA memory",
    "memory-efficient attention",
    "memory optimization",
    "database memory",
    "operating system memory",
    "human cognitive memory without AI-agent connection",
    "generic RAG without persistent memory",
    "generic vector search without agent memory",
]

DEFAULT_RESEARCH_CONTEXT = [
    "Deep research agents are relevant to this thesis scope.",
    "The thesis concerns agentic memory, LLM agent memory, and memory mechanisms for long-running/deep research agents.",
    "The research group has explored Engram-style / parametric-memory mechanisms in Megatron-LM, but the prior attempt did not succeed as intended.",
    "Relevant context includes NVIDIA/Megatron-LM PR #3689, NVIDIA/Megatron-LM issue #3382, and the DeepSeek Engram paper.",
]

DEFAULT_CONFIG_PATH = Path("config/paper_scout.yaml")
TRACK_CONFIG_PATHS = {
    "agent_memory": Path("config/tracks/agent_memory.yaml"),
    "deep_research": Path("config/tracks/deep_research.yaml"),
    "engram": Path("config/tracks/engram.yaml"),
}

# Public paths, independent of local build/output overrides.
TRACK_SITES = {
    "agent_memory": ("Agentic Memory", "."),
    "deep_research": ("Deep Research", "deep-research"),
    "engram": ("Engram", "engram"),
}


def validate_track(track_id: str) -> str:
    if track_id not in TRACK_CONFIG_PATHS:
        raise ValueError(f"unknown Paper Scout track: {track_id}")
    return track_id


def track_links(track_id: str) -> tuple[tuple[str, str], ...]:
    validate_track(track_id)
    current = TRACK_SITES[track_id][1]
    return tuple(
        (label, posixpath.relpath(posixpath.join(path, "index.html"), current))
        for key, (label, path) in TRACK_SITES.items() if key != track_id
    )


@dataclass(frozen=True)
class DiscoveryQuery:
    query: str
    mode: str = "all_terms"


@dataclass(frozen=True)
class ArxivSweepConfig:
    enabled: bool = False
    categories: tuple[str, ...] = ()
    days: int = 10
    max_results: int = 300


@dataclass(frozen=True)
class QualityAssessmentConfig:
    version: str = "quality-v1"
    rubric_version: str = "scholarly-rubric-v1"
    assess_relevant: bool = True
    assess_maybe_relevant: bool = True
    assess_irrelevant: bool = False
    max_assessments_per_run: int = 5


@dataclass(frozen=True)
class QualityFullTextConfig:
    enabled: bool = True
    cache_dir: Path = Path("data/cache/full_text")
    timeout_seconds: int = 20
    max_pdf_megabytes: int = 20
    max_pages: int = 80
    max_extracted_characters: int = 120_000
    max_prompt_characters: int = 60_000
    max_section_characters: int = 8_000


@dataclass(frozen=True)
class QualityRankingConfig:
    behavior: str = "downrank"
    relevance_weight: float = 0.75
    quality_weight: float = 0.25
    downrank_below: int = 60
    weak_below: int = 55
    hide_below: int = 40
    minimum_confidence_for_hiding: str = "high"
    unknown_quality_is_neutral: bool = True


@dataclass(frozen=True)
class QualityDisplayConfig:
    show_score: bool = True
    show_confidence: bool = True
    show_scope: bool = True
    show_strengths: int = 2
    show_concerns: int = 3
    show_evidence: bool = True


@dataclass(frozen=True)
class QualityConfig:
    enabled: bool = False
    mode: str = "auto"
    assessment: QualityAssessmentConfig = field(default_factory=QualityAssessmentConfig)
    full_text: QualityFullTextConfig = field(default_factory=QualityFullTextConfig)
    ranking: QualityRankingConfig = field(default_factory=QualityRankingConfig)
    display: QualityDisplayConfig = field(default_factory=QualityDisplayConfig)


@dataclass(frozen=True)
class ScoutConfig:
    terms: list[str]
    track_id: str = "agent_memory"
    title: str = "Agentic Memory Paper Library"
    subtitle: str = "A daily updated library of papers on agentic memory, deep research agents, and memory mechanisms."
    days: int = 7
    max_results_per_source: int = 25
    max_metadata_requests: int | None = None
    sqlite_path: Path = Path("data/paper_scout.sqlite3")
    digest_dir: Path = Path("digests")
    report_dir: Path = Path("reports/paper_scout")
    docs_dir: Path = Path("docs")
    curation_path: Path = Path("config/curation.yaml")
    relevance_profile: str = "agent_memory"
    relevance_llm_enabled: bool = True
    site_enrichment_enabled: bool = True
    seed_manifest: Path | None = None
    cross_track_label: str = "Deep Research Library"
    cross_track_href: str = "deep-research/index.html"
    research_context: list[str] = field(default_factory=lambda: list(DEFAULT_RESEARCH_CONTEXT))
    exclusions: list[str] = field(default_factory=lambda: list(DEFAULT_EXCLUSIONS))
    discovery_queries: dict[str, tuple[DiscoveryQuery, ...]] = field(default_factory=dict)
    query_budgets: dict[str, int] = field(default_factory=lambda: {"arxiv": 6, "openalex": 5, "semantic_scholar": 5})
    arxiv_sweep: ArxivSweepConfig = field(default_factory=ArxivSweepConfig)
    quality: QualityConfig = field(default_factory=QualityConfig)

    def __post_init__(self) -> None:
        validate_track(self.track_id)
        validate_track(self.relevance_profile)


def load_config(
    path: Path | str = DEFAULT_CONFIG_PATH,
    env: dict[str, str] | None = None,
    track_id: str | None = None,
) -> ScoutConfig:
    active_env = os.environ if env is None else env
    config_path = Path(path)
    active_track_id = validate_track(track_id or "agent_memory")
    if track_id and config_path == DEFAULT_CONFIG_PATH:
        track_path = TRACK_CONFIG_PATHS.get(active_track_id)
        if track_path:
            config_path = track_path
    if not config_path.exists():
        if active_track_id != "agent_memory":
            raise FileNotFoundError(f"missing track configuration: {config_path}")
        return ScoutConfig(
            terms=DEFAULT_TERMS,
            track_id=active_track_id,
            sqlite_path=Path(_state_path_from_env(active_env, active_track_id, "data/paper_scout.sqlite3")),
            research_context=DEFAULT_RESEARCH_CONTEXT,
            exclusions=DEFAULT_EXCLUSIONS,
        )

    config_text = config_path.read_text(encoding="utf-8")
    data = _parse_simple_yaml(config_text)
    track = data.get("track", {})
    search = data.get("search", {})
    output = data.get("output", {})
    state = data.get("state", {})
    curation = data.get("curation", {})
    track_values = track if isinstance(track, dict) else {}
    output_values = output if isinstance(output, dict) else {}
    state_values = state if isinstance(state, dict) else {}
    curation_values = curation if isinstance(curation, dict) else {}
    search_values = search if isinstance(search, dict) else {}
    discovery_queries = _parse_discovery_queries(config_text)
    if not discovery_queries:
        discovery_queries = _fallback_discovery_queries(search_values.get("terms") or DEFAULT_TERMS)
    query_budgets = _parse_int_mapping(config_text, "query_budgets") or {"arxiv": 6, "openalex": 5, "semantic_scholar": 5}
    sweep_values = _parse_mapping(config_text, "arxiv_sweep")
    quality_values = _parse_nested_mapping(config_text, "quality")

    loaded_track_id = validate_track(str(track_values.get("id") or active_track_id))
    if track_id and loaded_track_id != track_id:
        raise ValueError(f"requested track {track_id} does not match config track {loaded_track_id}")
    terms = search_values.get("terms") or DEFAULT_TERMS
    default_sqlite = str(state_values.get("sqlite_path", "data/paper_scout.sqlite3"))
    sqlite_path = Path(_state_path_from_env(active_env, loaded_track_id, default_sqlite))
    return ScoutConfig(
        terms=[str(term) for term in terms if str(term).strip()],
        track_id=loaded_track_id,
        title=str(track_values.get("title") or "Agentic Memory Paper Library"),
        subtitle=str(track_values.get("subtitle") or "A daily updated library of papers on agentic memory, deep research agents, and memory mechanisms."),
        days=int(search_values.get("days", 7)),
        max_results_per_source=int(search_values.get("max_results_per_source", 25)),
        max_metadata_requests=max(0, int(search_values["max_metadata_requests"])) if "max_metadata_requests" in search_values else None,
        sqlite_path=sqlite_path,
        digest_dir=Path(output_values.get("digest_dir", "digests")),
        report_dir=Path(output_values.get("report_dir", "reports/paper_scout")),
        docs_dir=Path(output_values.get("docs_dir", "docs")),
        curation_path=Path(curation_values.get("path", "config/curation.yaml")),
        relevance_profile=str(track_values.get("relevance_profile") or loaded_track_id),
        relevance_llm_enabled=_as_bool(track_values.get("relevance_llm_enabled"), True),
        site_enrichment_enabled=_as_bool(track_values.get("site_enrichment_enabled"), True),
        seed_manifest=Path(track_values["seed_manifest"]) if track_values.get("seed_manifest") else None,
        cross_track_label=str(track_values.get("cross_track_label") or "Deep Research Library"),
        cross_track_href=str(track_values.get("cross_track_href") or "deep-research/index.html"),
        research_context=[str(item) for item in data.get("research_context", DEFAULT_RESEARCH_CONTEXT)],
        exclusions=[str(item) for item in data.get("exclusions", DEFAULT_EXCLUSIONS)],
        discovery_queries=discovery_queries,
        query_budgets=query_budgets,
        arxiv_sweep=ArxivSweepConfig(
            enabled=_as_bool(sweep_values.get("enabled"), False),
            categories=tuple(_parse_section_list(config_text, "arxiv_sweep", "categories")),
            days=int(sweep_values.get("days", 10)),
            max_results=int(sweep_values.get("max_results", 300)),
        ),
        quality=_quality_config(quality_values),
    )


def _quality_config(values: dict[str, str]) -> QualityConfig:
    mode = values.get("mode", "auto").lower()
    if mode not in {"off", "deterministic", "llm", "hybrid", "auto"}:
        raise ValueError(f"unsupported quality mode: {mode}")
    behavior = values.get("ranking.behavior", "downrank").lower()
    if behavior not in {"ignore", "annotate", "downrank", "hide"}:
        raise ValueError(f"unsupported quality ranking behavior: {behavior}")
    minimum_confidence = values.get("ranking.minimum_confidence_for_hiding", "high").lower()
    if minimum_confidence not in {"low", "medium", "high"}:
        raise ValueError(f"unsupported quality hiding confidence: {minimum_confidence}")
    relevance_weight = float(values.get("ranking.relevance_weight", 0.75))
    quality_weight = float(values.get("ranking.quality_weight", 0.25))
    if relevance_weight < 0 or quality_weight < 0 or relevance_weight + quality_weight <= 0:
        raise ValueError("quality ranking weights must be non-negative and have a positive total")
    thresholds = {
        "downrank_below": int(values.get("ranking.downrank_below", 60)),
        "weak_below": int(values.get("ranking.weak_below", 55)),
        "hide_below": int(values.get("ranking.hide_below", 40)),
    }
    if any(value < 0 or value > 100 for value in thresholds.values()):
        raise ValueError("quality ranking thresholds must be between 0 and 100")
    return QualityConfig(
        enabled=_as_bool(values.get("enabled"), False),
        mode=mode,
        assessment=QualityAssessmentConfig(
            version=values.get("assessment.version", "quality-v1"),
            rubric_version=values.get("assessment.rubric_version", "scholarly-rubric-v1"),
            assess_relevant=_as_bool(values.get("assessment.assess_relevant"), True),
            assess_maybe_relevant=_as_bool(values.get("assessment.assess_maybe_relevant"), True),
            assess_irrelevant=_as_bool(values.get("assessment.assess_irrelevant"), False),
            max_assessments_per_run=max(0, int(values.get("assessment.max_assessments_per_run", 5))),
        ),
        full_text=QualityFullTextConfig(
            enabled=_as_bool(values.get("full_text.enabled"), True),
            cache_dir=Path(values.get("full_text.cache_dir", "data/cache/full_text")),
            timeout_seconds=max(1, int(values.get("full_text.timeout_seconds", 20))),
            max_pdf_megabytes=max(1, int(values.get("full_text.max_pdf_megabytes", 20))),
            max_pages=max(1, int(values.get("full_text.max_pages", 80))),
            max_extracted_characters=max(1_000, int(values.get("full_text.max_extracted_characters", 120_000))),
            max_prompt_characters=max(1_000, int(values.get("full_text.max_prompt_characters", 60_000))),
            max_section_characters=max(500, int(values.get("full_text.max_section_characters", 8_000))),
        ),
        ranking=QualityRankingConfig(
            behavior=behavior,
            relevance_weight=relevance_weight,
            quality_weight=quality_weight,
            downrank_below=thresholds["downrank_below"],
            weak_below=thresholds["weak_below"],
            hide_below=thresholds["hide_below"],
            minimum_confidence_for_hiding=minimum_confidence,
            unknown_quality_is_neutral=_as_bool(values.get("ranking.unknown_quality_is_neutral"), True),
        ),
        display=QualityDisplayConfig(
            show_score=_as_bool(values.get("display.show_score"), True),
            show_confidence=_as_bool(values.get("display.show_confidence"), True),
            show_scope=_as_bool(values.get("display.show_scope"), True),
            show_strengths=max(0, int(values.get("display.show_strengths", 2))),
            show_concerns=max(0, int(values.get("display.show_concerns", 3))),
            show_evidence=_as_bool(values.get("display.show_evidence"), True),
        ),
    )


def _state_path_from_env(env: dict[str, str] | os._Environ[str], track_id: str, default: str) -> str:
    track_env_key = f"PAPER_SCOUT_{track_id.upper()}_STATE_PATH"
    return env.get(track_env_key) or env.get("PAPER_SCOUT_STATE_PATH") or default


def _parse_simple_yaml(text: str) -> dict[str, object]:
    """Parse the small YAML subset used by this repo's config file."""
    root: dict[str, object] = {}
    current_section: dict[str, object] | list[str] | None = None
    current_list_key: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and line.endswith(":"):
            section_name = line[:-1].strip()
            if section_name in {"research_context", "exclusions"}:
                current_section = []
            else:
                current_section = {}
            root[section_name] = current_section
            current_list_key = None
            continue
        if current_section is None:
            continue
        stripped = line.strip()
        if isinstance(current_section, list):
            if stripped.startswith("- "):
                current_section.append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if stripped.endswith(":"):
            current_list_key = stripped[:-1]
            current_section[current_list_key] = []
            continue
        if stripped.startswith("- ") and current_list_key:
            item = stripped[2:].strip().strip('"').strip("'")
            current_section[current_list_key].append(item)  # type: ignore[union-attr]
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            current_list_key = None
            current_section[key.strip()] = value.strip().strip('"').strip("'")

    return root


def _fallback_discovery_queries(terms: object) -> dict[str, tuple[DiscoveryQuery, ...]]:
    values = [str(term) for term in terms if str(term).strip()] if isinstance(terms, list) else list(DEFAULT_TERMS)
    bounded = tuple(DiscoveryQuery(term, "all_terms") for term in values[:5])
    return {source: bounded for source in ("arxiv", "openalex", "semantic_scholar")}


def _parse_discovery_queries(text: str) -> dict[str, tuple[DiscoveryQuery, ...]]:
    lines = text.splitlines()
    start = _section_start(lines, "discovery_queries")
    if start is None:
        return {}
    result: dict[str, list[DiscoveryQuery]] = {}
    source: str | None = None
    pending: dict[str, str] | None = None
    for raw in lines[start + 1 :]:
        if raw.strip() and not raw.startswith(" "):
            break
        stripped = raw.split("#", 1)[0].strip()
        indent = len(raw) - len(raw.lstrip(" "))
        if not stripped:
            continue
        if indent == 2 and stripped.endswith(":"):
            if source and pending and pending.get("query"):
                result.setdefault(source, []).append(DiscoveryQuery(pending["query"], pending.get("mode", "all_terms")))
            source = stripped[:-1]
            pending = None
            continue
        if source is None or not stripped.startswith("-") and pending is None:
            continue
        if stripped.startswith("- "):
            if pending and pending.get("query"):
                result.setdefault(source, []).append(DiscoveryQuery(pending["query"], pending.get("mode", "all_terms")))
            value = stripped[2:].strip()
            if value.startswith("query:"):
                pending = {"query": _scalar(value.split(":", 1)[1])}
            else:
                result.setdefault(source, []).append(DiscoveryQuery(_scalar(value), "all_terms"))
                pending = None
            continue
        if pending is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            pending[key.strip()] = _scalar(value)
    if source and pending and pending.get("query"):
        result.setdefault(source, []).append(DiscoveryQuery(pending["query"], pending.get("mode", "all_terms")))
    return {key: tuple(values) for key, values in result.items()}


def _parse_mapping(text: str, section: str) -> dict[str, str]:
    lines = text.splitlines()
    start = _section_start(lines, section)
    if start is None:
        return {}
    values: dict[str, str] = {}
    for raw in lines[start + 1 :]:
        if raw.strip() and not raw.startswith(" "):
            break
        stripped = raw.split("#", 1)[0].strip()
        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 2 and ":" in stripped and not stripped.endswith(":"):
            key, value = stripped.split(":", 1)
            values[key.strip()] = _scalar(value)
    return values


def _parse_int_mapping(text: str, section: str) -> dict[str, int]:
    return {key: int(value) for key, value in _parse_mapping(text, section).items()}


def _parse_nested_mapping(text: str, section: str) -> dict[str, str]:
    lines = text.splitlines()
    start = _section_start(lines, section)
    if start is None:
        return {}
    result: dict[str, str] = {}
    stack: list[tuple[int, str]] = []
    for raw in lines[start + 1 :]:
        if raw.strip() and not raw.startswith(" "):
            break
        content = raw.split("#", 1)[0].rstrip()
        if not content.strip() or ":" not in content:
            continue
        indent = len(content) - len(content.lstrip(" "))
        key, value = content.strip().split(":", 1)
        while stack and stack[-1][0] >= indent:
            stack.pop()
        if not value.strip():
            stack.append((indent, key.strip()))
            continue
        path = ".".join([item[1] for item in stack] + [key.strip()])
        result[path] = _scalar(value)
    return result


def _parse_section_list(text: str, section: str, key: str) -> list[str]:
    lines = text.splitlines()
    start = _section_start(lines, section)
    if start is None:
        return []
    in_list = False
    values: list[str] = []
    for raw in lines[start + 1 :]:
        if raw.strip() and not raw.startswith(" "):
            break
        stripped = raw.split("#", 1)[0].strip()
        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 2:
            in_list = stripped == f"{key}:"
            continue
        if in_list and stripped.startswith("- "):
            values.append(_scalar(stripped[2:]))
    return values


def _section_start(lines: list[str], section: str) -> int | None:
    marker = f"{section}:"
    return next((index for index, line in enumerate(lines) if line.strip() == marker and not line.startswith(" ")), None)


def _scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}
