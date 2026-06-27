from __future__ import annotations

import re

from paper_scout.models import ClassificationResult, PaperCandidate

INCLUDE_PATTERNS = {
    "agent-memory": [
        r"\bagent(ic)? memory\b",
        r"\bmemory (for|in) (llm|language model|large language model)(?:\s+\([^)]+\))? agents?\b",
    ],
    "llm-agents": [r"\bllm agents?\b", r"\blarge language model(?:\s+\([^)]+\))? agents?\b", r"\blanguage model agents?\b"],
    "memory-systems": [
        r"\bagent[- ]native memory\b",
        r"\bagent memory systems?\b",
        r"\bmemory systems?\b",
        r"\bmemory modules?\b",
        r"\bdata management systems?\b",
    ],
    "long-term-memory": [r"\blong[- ]term memory\b", r"\bpersistent memory\b"],
    "memory-types": [r"\bepisodic memory\b", r"\bsemantic memory\b", r"\bprocedural memory\b"],
    "memory-policy": [
        r"\bmemory (write|read|retrieval|update|maintenance|governance|policy|policies|representation|storage|consolidation)\b",
        r"\b(write|read|retrieval) polic(y|ies)\b",
        r"\bstorage\b.*\bretrieval\b.*\bmaintenance\b",
    ],
    "benchmark": [r"\b(agent )?memory benchmark\b", r"\bagent memory evaluation\b", r"\blongmemeval\b", r"\blocomo\b"],
    "evaluation": [r"\bevaluat(e|es|ed|ion|ing)\b", r"\bbenchmark\b"],
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

HIGH_CONFIDENCE_AGENT_MEMORY_PATTERNS = {
    "agent-native memory": r"\bagent[- ]native memory\b",
    "agent memory system": r"\bagent memory systems?\b",
    "memory system for LLM agents": r"\bmemory systems?\b.*\b(llm|large language model|language model)(?:\s+\([^)]+\))? agents?\b|\bmemory (for|in) (llm|large language model|language model)(?:\s+\([^)]+\))? agents?\b.*\b(systems?|storage|retrieval|update|consolidation|maintenance|governance)\b",
    "memory systems and LLM agents": r"\bmemory systems?\b.*\bagents?\b|\bagents?\b.*\bmemory systems?\b",
    "memory module LLM agent": r"\bmemory modules?\b.*\b(llm|large language model|language model)?\s*agents?\b",
    "persistent memory agent": r"\bpersistent memory\b.*\bagents?\b|\bagents?\b.*\bpersistent memory\b",
    "long-term memory agent": r"\blong[- ]term memory\b.*\bagents?\b|\bagents?\b.*\blong[- ]term memory\b",
    "memory representation retrieval agent": r"\bmemory representation\b.*\bretrieval\b.*\bagents?\b|\bagents?\b.*\bmemory representation\b.*\bretrieval\b",
    "storage retrieval maintenance memory": r"\bstorage\b.*\bretrieval\b.*\bmaintenance\b.*\bmemory\b|\bmemory\b.*\bstorage\b.*\bretrieval\b.*\bmaintenance\b",
    "memory consolidation agent": r"\bmemory consolidation\b.*\bagents?\b|\bagents?\b.*\bmemory consolidation\b",
    "agent memory evaluation": r"\bagent memory evaluation\b",
    "memory benchmark agent": r"\bmemory benchmark\b.*\bagents?\b|\bagents?\b.*\bmemory benchmark\b",
}


def classify_with_rules(candidate: PaperCandidate) -> ClassificationResult:
    evidence = explain_rule_matches(candidate)
    text = evidence["text"]
    exclude_hits = evidence["exclude_hits"]
    include_tags = list(evidence["include_tags"])
    high_confidence_hits = evidence["high_confidence_hits"]
    has_agent_context = bool(evidence["agent_context_hits"])

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
    if "memory-systems" in include_tags and has_agent_context:
        score += 12
    if "benchmark" in include_tags:
        score += 8
    if high_confidence_hits:
        score = max(score, 90)
    score = min(100, score)

    if high_confidence_hits:
        decision = "relevant"
        reason = "Directly discusses agent-native memory systems or memory modules for LLM agents."
    elif score >= 70:
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


def explain_rule_matches(candidate: PaperCandidate) -> dict[str, object]:
    text = _paper_text(candidate)
    include_tags = [
        tag
        for tag, patterns in INCLUDE_PATTERNS.items()
        if _matches(patterns, text)
    ]
    high_confidence_hits = _matches_labeled(HIGH_CONFIDENCE_AGENT_MEMORY_PATTERNS, text)
    if high_confidence_hits:
        for tag in ["agent-memory", "memory-systems", "llm-agents"]:
            if tag not in include_tags:
                include_tags.append(tag)
        if _matches(INCLUDE_PATTERNS["memory-policy"], text) and "memory-policy" not in include_tags:
            include_tags.append("memory-policy")
        if _matches(INCLUDE_PATTERNS["evaluation"], text) and "evaluation" not in include_tags:
            include_tags.append("evaluation")
    return {
        "text": text,
        "include_tags": include_tags,
        "exclude_hits": _matches(EXCLUDE_PATTERNS, text),
        "agent_context_hits": _matches(AGENT_CONTEXT, text),
        "high_confidence_hits": high_confidence_hits,
    }


def should_consider_for_llm(result: ClassificationResult) -> bool:
    return result.decision in {"relevant", "maybe"} and result.score >= 40


def _paper_text(candidate: PaperCandidate) -> str:
    return f"{candidate.title}\n{candidate.abstract}".lower()


def _matches(patterns: list[str], text: str) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, flags=re.I)]


def _matches_labeled(patterns: dict[str, str], text: str) -> list[str]:
    return [label for label, pattern in patterns.items() if re.search(pattern, text, flags=re.I)]


def _summary(abstract: str, max_chars: int = 320) -> str:
    compact = " ".join((abstract or "").split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."
