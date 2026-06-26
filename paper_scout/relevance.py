from __future__ import annotations

import re

from paper_scout.models import ClassificationResult, PaperCandidate

INCLUDE_PATTERNS = {
    "agent-memory": [r"\bagent(ic)? memory\b", r"\bmemory (for|in) (llm|language model) agents?\b"],
    "long-term-memory": [r"\blong[- ]term memory\b", r"\bpersistent memory\b"],
    "memory-types": [r"\bepisodic memory\b", r"\bsemantic memory\b", r"\bprocedural memory\b"],
    "memory-policy": [r"\bmemory (write|read|retrieval|update|maintenance|governance|policy|policies)\b", r"\b(write|read|retrieval) polic(y|ies)\b"],
    "benchmark": [r"\b(agent )?memory benchmark\b", r"\blongmemeval\b", r"\blocomo\b"],
    "deep-research": [r"\bdeep research\b", r"\bautoresearch\b", r"\bliterature[- ]review agents?\b", r"\bresearch agents?\b"],
    "parametric-memory": [r"\bparametric memory\b", r"\bengram\b", r"\bmodel[- ]internal memory\b", r"\bmemory mechanism\b"],
    "memory-augmented": [r"\bmemory[- ]augmented (llm|language model|agent)\b", r"\bmemory[- ]augmented language agents?\b"],
}

EXCLUDE_PATTERNS = [
    r"\bgpu memory\b",
    r"\bcuda memory\b",
    r"\bmemory[- ]efficient attention\b",
    r"\bmemory optimization\b",
    r"\bkv cache\b",
    r"\bdatabase memory\b",
    r"\bin-memory database\b",
    r"\boperating system memory\b",
    r"\bmemory paging\b",
    r"\bmemory bandwidth\b",
    r"\bcache optimization\b",
    r"\bvector database\b",
    r"\bvector search\b",
    r"\bgeneric rag\b",
    r"\bwithout agent memory\b",
    r"\bwithout persistent memory\b",
    r"\bhuman memory\b",
    r"\bhuman cognitive memory\b",
    r"\bworking memory in humans\b",
]

AGENT_CONTEXT = [
    r"\bagents?\b",
    r"\bllm\b",
    r"\blarge language model\b",
    r"\blanguage model\b",
    r"\bautonomous research\b",
    r"\bdeep research\b",
]


def classify_with_rules(candidate: PaperCandidate) -> ClassificationResult:
    text = _paper_text(candidate)
    exclude_hits = _matches(EXCLUDE_PATTERNS, text)
    include_tags = [
        tag
        for tag, patterns in INCLUDE_PATTERNS.items()
        if _matches(patterns, text)
    ]
    has_agent_context = bool(_matches(AGENT_CONTEXT, text))

    if exclude_hits and (not include_tags or _matches([r"\bwithout agent memory\b", r"\bwithout persistent memory\b"], text)):
        return ClassificationResult(
            score=5,
            decision="irrelevant",
            reason="Matches excluded memory sense such as GPU, database, or human memory.",
            tags=["excluded-memory-sense"],
            abstract_summary=_summary(candidate.abstract),
        )

    score = min(95, len(include_tags) * 22 + (18 if has_agent_context else 0))
    if "agent-memory" in include_tags:
        score += 15
    if "benchmark" in include_tags:
        score += 8
    score = min(100, score)

    if score >= 70:
        decision = "relevant"
        reason = "Matches the agent-memory rubric with explicit LLM or agent context."
    elif score >= 40:
        decision = "maybe"
        reason = "Touches memory concepts that may be relevant if connected to agent behavior."
    else:
        decision = "irrelevant"
        reason = "Does not clearly address persistent memory for LLM agents."

    return ClassificationResult(
        score=score,
        decision=decision,
        reason=reason,
        tags=include_tags,
        abstract_summary=_summary(candidate.abstract),
    )


def should_consider_for_llm(result: ClassificationResult) -> bool:
    return result.decision in {"relevant", "maybe"} and result.score >= 40


def _paper_text(candidate: PaperCandidate) -> str:
    return f"{candidate.title}\n{candidate.abstract}".lower()


def _matches(patterns: list[str], text: str) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, flags=re.I)]


def _summary(abstract: str, max_chars: int = 320) -> str:
    compact = " ".join((abstract or "").split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."
