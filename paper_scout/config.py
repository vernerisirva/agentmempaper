from __future__ import annotations

from dataclasses import dataclass, field
import os
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


@dataclass(frozen=True)
class ScoutConfig:
    terms: list[str]
    days: int = 7
    max_results_per_source: int = 25
    sqlite_path: Path = Path("data/paper_scout.sqlite3")
    digest_dir: Path = Path("digests")
    report_dir: Path = Path("reports/paper_scout")
    research_context: list[str] = field(default_factory=lambda: list(DEFAULT_RESEARCH_CONTEXT))
    exclusions: list[str] = field(default_factory=lambda: list(DEFAULT_EXCLUSIONS))


def load_config(path: Path | str = "config/paper_scout.yaml", env: dict[str, str] | None = None) -> ScoutConfig:
    active_env = os.environ if env is None else env
    config_path = Path(path)
    if not config_path.exists():
        return ScoutConfig(
            terms=DEFAULT_TERMS,
            sqlite_path=Path(active_env.get("PAPER_SCOUT_STATE_PATH", "data/paper_scout.sqlite3")),
            research_context=DEFAULT_RESEARCH_CONTEXT,
            exclusions=DEFAULT_EXCLUSIONS,
        )

    data = _parse_simple_yaml(config_path.read_text(encoding="utf-8"))
    search = data.get("search", {})
    output = data.get("output", {})
    state = data.get("state", {})

    terms = search.get("terms") or DEFAULT_TERMS
    sqlite_path = Path(active_env.get("PAPER_SCOUT_STATE_PATH", str(state.get("sqlite_path", "data/paper_scout.sqlite3"))))
    return ScoutConfig(
        terms=[str(term) for term in terms if str(term).strip()],
        days=int(search.get("days", 7)),
        max_results_per_source=int(search.get("max_results_per_source", 25)),
        sqlite_path=sqlite_path,
        digest_dir=Path(output.get("digest_dir", "digests")),
        report_dir=Path(output.get("report_dir", "reports/paper_scout")),
        research_context=[str(item) for item in data.get("research_context", DEFAULT_RESEARCH_CONTEXT)],
        exclusions=[str(item) for item in data.get("exclusions", DEFAULT_EXCLUSIONS)],
    )


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
