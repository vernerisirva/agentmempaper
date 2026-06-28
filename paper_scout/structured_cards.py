from __future__ import annotations

from typing import Any


NOT_EXTRACTED = "Not extracted yet"
SCHEMA_VERSION = "paper-scout-card-v1"


def structured_card_for_paper(paper: Any) -> dict[str, dict[str, str]]:
    """Build a conservative, provenance-aware structured card from existing metadata."""
    method, relation, provenance = _classify_method_and_relation(paper)
    research_relevance = _research_relevance(paper)
    evidence = _evidence_field(method, provenance)
    return {
        "research_relevance": research_relevance,
        "method_or_system_type": _field(method, "medium", provenance) if method != NOT_EXTRACTED else _not_extracted(),
        "key_contribution": _not_extracted(),
        "evidence_or_evaluation": evidence,
        "relation_to_agentic_memory": _field(relation, _relation_confidence(relation), provenance) if relation != NOT_EXTRACTED else _not_extracted(),
        "limitations_or_uncertainty": _field(
            "Only title, abstract/summary, metadata, screening rules, and curation were used; full text was not analyzed.",
            "high",
            "rule",
        ),
    }


def related_topics_for_paper(paper: Any) -> list[str]:
    text = _combined_text(paper)
    topics = set(_tags(paper))
    if _contains_any(text, ["benchmark", "evaluation", "agentshield", "mgbench", "memprobe"]):
        topics.add("memory-benchmark")
    if _contains_any(text, ["poisoning", "jailbreak", "cross-session", "security", "robustness"]):
        topics.add("memory-security")
    if _contains_any(text, ["engram", "parametric memory"]):
        topics.add("parametric-memory")
    if _contains_any(text, ["memory system", "agent-native memory", "memory module", "trustmem", "governed shared memory"]):
        topics.add("agent-memory")
    return sorted(topic for topic in topics if topic)


def paper_card_schema() -> dict[str, Any]:
    field_schema = {
        "type": "object",
        "required": ["value", "confidence", "provenance"],
        "properties": {
            "value": {"type": "string"},
            "confidence": {"enum": ["high", "medium", "low", "unknown", "not_extracted"]},
            "provenance": {"enum": ["curation", "abstract", "metadata", "rule", "not_extracted"]},
        },
        "additionalProperties": False,
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Paper Scout Structured Paper Card",
        "type": "object",
        "required": [
            "schema_version",
            "canonical_id",
            "title",
            "authors",
            "publication",
            "relevance",
            "structured_card",
            "provenance",
        ],
        "properties": {
            "schema_version": {"const": SCHEMA_VERSION},
            "canonical_id": {"type": "string"},
            "title": {"type": "string"},
            "authors": {"type": "array", "items": {"type": "string"}},
            "url": {"type": ["string", "null"]},
            "sources": {"type": "array", "items": {"type": "string"}},
            "source_ids": {"type": "object"},
            "doi": {"type": ["string", "null"]},
            "arxiv_id": {"type": ["string", "null"]},
            "ssrn_id": {"type": ["string", "null"]},
            "openalex_id": {"type": ["string", "null"]},
            "semantic_scholar_id": {"type": ["string", "null"]},
            "publication": {"type": "object"},
            "first_seen_at": {"type": ["string", "null"]},
            "last_seen_at": {"type": ["string", "null"]},
            "relevance": {"type": "object"},
            "structured_card": {
                "type": "object",
                "required": [
                    "research_relevance",
                    "method_or_system_type",
                    "key_contribution",
                    "evidence_or_evaluation",
                    "relation_to_agentic_memory",
                    "limitations_or_uncertainty",
                ],
                "properties": {
                    "research_relevance": field_schema,
                    "method_or_system_type": field_schema,
                    "key_contribution": field_schema,
                    "evidence_or_evaluation": field_schema,
                    "relation_to_agentic_memory": field_schema,
                    "limitations_or_uncertainty": field_schema,
                },
                "additionalProperties": False,
            },
            "related_topics": {"type": "array", "items": {"type": "string"}},
            "provenance": {"type": "object"},
        },
        "additionalProperties": True,
    }


def _research_relevance(paper: Any) -> dict[str, str]:
    note = getattr(paper, "research_note", None)
    if note:
        return _field(note, "high", "curation")
    if getattr(paper, "decision", "") == "relevant":
        return _field("Directly relevant to agentic-memory research based on screening evidence.", "medium", "rule")
    if getattr(paper, "decision", "") == "maybe":
        return _field("Review candidate", "low", "rule")
    return _not_extracted()


def _classify_method_and_relation(paper: Any) -> tuple[str, str, str]:
    text = _combined_text(paper)
    if _is_peripheral_memory_candidate(text, paper):
        return NOT_EXTRACTED, "Agentic-AI connection exists, but memory focus is weak or indirect", "rule"
    if _contains_any(text, ["poisoning", "jailbreak", "cross-session", "security", "robustness"]):
        provenance = _keyword_provenance(paper, ["poisoning", "jailbreak", "cross-session", "security", "robustness"])
        return "Security / robustness evaluation", "Studies memory-related safety risks in LLM agents", provenance
    if _contains_any(text, ["engram", "parametric memory"]):
        provenance = _keyword_provenance(paper, ["engram", "parametric memory"])
        return "Parametric memory mechanism", "Studies memory encoded in or attached to model behavior", provenance
    if _contains_any(text, ["agent-native memory", "memory system", "memory module", "trustmem", "governed shared memory"]):
        provenance = _keyword_provenance(paper, ["agent-native memory", "memory system", "memory module", "trustmem", "governed shared memory"])
        return "Memory architecture / system", "Studies memory mechanisms or governance for LLM agents", provenance
    if _contains_any(text, ["benchmark", "evaluation", "agentshield", "mgbench", "memprobe"]):
        provenance = _keyword_provenance(paper, ["benchmark", "evaluation", "agentshield", "mgbench", "memprobe"])
        return "Benchmark / evaluation", "Evaluates memory behavior, safety, or retrieval in LLM agents", provenance
    if _contains_any(text, ["memory system", "agent-native memory", "memory module", "trustmem", "governed shared memory", "long-term memory", "persistent memory"]):
        provenance = _keyword_provenance(
            paper,
            ["memory system", "agent-native memory", "memory module", "trustmem", "governed shared memory", "long-term memory", "persistent memory"],
        )
        return "Memory architecture / system", "Studies memory mechanisms or governance for LLM agents", provenance
    return NOT_EXTRACTED, NOT_EXTRACTED, "not_extracted"


def _evidence_field(method: str, provenance: str) -> dict[str, str]:
    if method == "Benchmark / evaluation":
        return _field(
            "Abstract-level signal: benchmark or evaluation evidence is mentioned in title, abstract, tags, or screening metadata.",
            "medium",
            provenance,
        )
    if method == "Security / robustness evaluation":
        return _field(
            "Abstract-level signal: safety, security, or robustness evaluation is mentioned in available metadata.",
            "medium",
            provenance,
        )
    return _not_extracted()


def _relation_confidence(relation: str) -> str:
    if relation == "Agentic-AI connection exists, but memory focus is weak or indirect":
        return "low"
    return "medium"


def _field(value: str, confidence: str, provenance: str) -> dict[str, str]:
    return {"value": value, "confidence": confidence, "provenance": provenance}


def _not_extracted() -> dict[str, str]:
    return {"value": NOT_EXTRACTED, "confidence": "not_extracted", "provenance": "not_extracted"}


def _combined_text(paper: Any) -> str:
    return " ".join(
        part
        for part in [
            getattr(paper, "title", "") or "",
            getattr(paper, "abstract_summary", "") or "",
            getattr(paper, "reason", "") or "",
            getattr(paper, "research_note", "") or "",
            " ".join(_tags(paper)),
        ]
        if part
    ).lower()


def _tags(paper: Any) -> list[str]:
    tags = getattr(paper, "tags", []) or []
    return [str(tag) for tag in tags]


def _contains_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def _is_peripheral_memory_candidate(text: str, paper: Any) -> bool:
    if getattr(paper, "decision", "") != "maybe":
        return False
    return _contains_any(
        text,
        [
            "peripheral candidate",
            "memory focus is weak",
            "does not clearly study persistent agent memory",
            "lacks explicit persistent memory evidence",
            "without explicit persistent agent memory",
        ],
    )


def _keyword_provenance(paper: Any, needles: list[str]) -> str:
    note = (getattr(paper, "research_note", None) or "").lower()
    abstract = (getattr(paper, "abstract_summary", None) or "").lower()
    title = (getattr(paper, "title", None) or "").lower()
    reason = (getattr(paper, "reason", None) or "").lower()
    tags = " ".join(_tags(paper)).lower()
    if _contains_any(note, needles):
        return "curation"
    if _contains_any(abstract, needles):
        return "abstract"
    if _contains_any(reason, needles):
        return "rule"
    if _contains_any(title, needles) or _contains_any(tags, needles):
        return "metadata"
    return "rule"
