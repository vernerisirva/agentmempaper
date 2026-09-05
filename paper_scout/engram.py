"""Conservative title/abstract screening for model-integrated conditional memory.

No bibliographic IDs, author names, platform or positive-result requirements.
"""
from __future__ import annotations

import re

from paper_scout.models import ClassificationResult, PaperCandidate

LM = r"\b(?:language[- ]models?|llms?|transformers?|backbones?)\b"
MECHANISMS = {
    "conditional-memory": r"\bconditional[- ]memor(?:y|ies)\b",
    "hashed-ngram-memory": r"\b(?:hash\w*|n[- ]grams?)\b.{0,100}\b(?:memor\w*|embeddings?|lookup)\b|\b(?:memory|embedding)\b.{0,100}\b(?:hash\w*|n[- ]grams?)\b",
    "learned-lookup": r"\b(?:learned|trainable|frozen|external)\b.{0,60}\b(?:memory tables?|lookup tables?|memory banks?)\b",
    "memory-transfer": r"\bcross[- ]model (?:frozen[- ])?memory (?:transfer|extraction)\b",
    "memory-grafting": r"\bmemory grafting\b",
}
READERS = r"\b(?:readers?|gates?|gating|injection|inject\w*|address\w*|lookup|projections?|hidden (?:states?|representations?))\b"
ADJACENT = {
    "product-key-memory": r"\bproduct[- ]key memor\w*\b",
    "neural-memory-layer": r"\b(?:neural|learned) memory layers?\b",
    "model-memory-editing": r"\b(?:model[- ]memory|memory[- ]table) editing\b",
    "test-time-memory": r"\btest[- ]time memory\b",
}
BIOLOGY = r"\b(?:hippocamp\w*|neuronal engrams?|engram cells?|neuroscience|synaptic|mice|rodents?)\b"
CONTRIBUTION = r"\b(?:we|this (?:paper|work|study))\b.{0,100}\b(?:propos\w*|introduc\w*|stud\w*|evaluat\w*|replicat\w*|analy[sz]\w*|investigat\w*|adapt\w*|train\w*|test\w*|compar\w*|implement\w*|show\w*)\b"
CITATION_ONLY = r"\b(?:related work|cites?|citing|mentioned|inspired by)\b|\b(?:prior|previous) work\b"
NEGATED = r"\b(?:without|no|unrelated to|does not (?:use|study|evaluate))\b.{0,30}\b(?:conditional[- ]memory|learned lookup|engram[- ]style)\b"
INDIRECT_CONNECTION = (
    r"\b(?:indirect|unestablished|uncertain) (?:relation(?:ship)?|connection|link)\b.{0,60}\b(?:engram|conditional[- ]memory)\b"
    r"|\b(?:relation(?:ship)?|connection|link)\b.{0,60}\b(?:engram|conditional[- ]memory)\b.{0,35}\b(?:indirect|unestablished|uncertain)\b"
)
MODEL_INTEGRATION = (
    r"\b(?:integrat\w*|inject\w*|fus\w*|attach\w*|connect\w*|consum\w*)\b.{0,100}"
    r"\b(?:backbones?|transformers?|hidden states?|activations?|model computation)\b"
    r"|\b(?:memory|lookup) tables?\b.{0,120}\b(?:readers?|gating|projections?)\b.{0,120}\b(?:backbones?|transformers?|hidden states?|layers?)\b"
)


def _hits(patterns: dict[str, str], text: str) -> list[str]:
    return [name for name, pattern in patterns.items() if re.search(pattern, text)]


def engram_evidence(candidate: PaperCandidate) -> dict[str, object]:
    title = candidate.title.lower()
    abstract = candidate.abstract.lower()
    # A citation/background mention alone cannot supply the study's mechanism.
    sentences = re.split(r"(?<=[.!?;])\s+", abstract)
    focused = [s for s in sentences if not re.search(CITATION_ONLY, s) or re.search(CONTRIBUTION, s)]
    # A memory-free baseline is not a denial of the mechanism being evaluated.
    # Nor can a negated/background mechanism supply positive architecture hits.
    negative = [s for s in [title, *focused] if re.search(NEGATED, s)]
    negated = any(not re.search(r"\b(?:baselines?|controls?|ablations?)\b", s) for s in negative)
    positive = [s for s in focused if s not in negative]
    text = (title if title not in negative else "") + "\n" + " ".join(positive)
    mechanisms = _hits(MECHANISMS, text)
    model_context = bool(re.search(LM, text))
    named = bool(re.search(r"\bengram(?:-style)?\b", text))
    reader = bool(re.search(READERS, text))
    title_focus = bool(_hits(MECHANISMS, title) or re.search(r"\bengram\b", title))
    study_focus = title_focus or any(re.search(CONTRIBUTION, s) and (_hits(MECHANISMS, s) or re.search(r"\bengram\b", s)) for s in positive)
    indirect = bool(re.search(INDIRECT_CONNECTION, text))
    # External/learned memory banks also occur in prompt-based RAG. A lookup
    # bank alone needs evidence that its values participate inside the model.
    architecture = bool(set(mechanisms) & {"conditional-memory", "hashed-ngram-memory"}) or (
        "learned-lookup" in mechanisms and bool(re.search(MODEL_INTEGRATION, text))
    )
    core = not indirect and model_context and architecture and study_focus and (named or reader) and not negated
    adjacent = _hits(ADJACENT, text) if model_context and not negated else []
    exclusions = []
    if re.search(BIOLOGY, text) and not core:
        exclusions.append("biological engram without a model-integrated mechanism")
    if negated:
        exclusions.append("explicitly lacks a conditional-memory connection")
    return {
        "text": text,
        "include_tags": (["engram"] if named and core else []) + (mechanisms if core else adjacent),
        "high_confidence_hits": mechanisms if core else [],
        "exclude_hits": exclusions,
        "review_hits": adjacent,
        "biological_memory_hits": exclusions[:1] if re.search(BIOLOGY, text) else [],
        "agent_context_hits": [],
        "broad_peripheral_hits": [],
        "negated_memory_focus_hits": ["explicit negation"] if negated else [],
        "negated_research_focus_hits": [],
    }


def classify_engram(candidate: PaperCandidate) -> ClassificationResult:
    evidence = engram_evidence(candidate)
    if evidence["high_confidence_hits"]:
        decision, score = "relevant", 92
        reason = "Studies model-integrated conditional memory; matched title/abstract rules: " + ", ".join(evidence["high_confidence_hits"]) + "."
    elif evidence["review_hits"] and not evidence["exclude_hits"]:
        decision, score = "maybe", 45
        reason = "Review candidate: adjacent learned-memory mechanism; direct Engram connection is unestablished. Matched: " + ", ".join(evidence["review_hits"]) + "."
    else:
        decision, score = "irrelevant", 10
        reason = "Excluded: " + ("; ".join(evidence["exclude_hits"]) or "no substantive title/abstract evidence of Engram-style or related model-integrated conditional memory") + "."
    summary = " ".join(candidate.abstract.split())
    if len(summary) > 320:
        summary = summary[:317].rstrip() + "..."
    return ClassificationResult(score, decision, reason, list(evidence["include_tags"]), summary)
