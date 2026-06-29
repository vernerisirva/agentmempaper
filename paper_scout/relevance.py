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
        r"\bmemory systems?\b.*\b(llm|large language model|language model|autonomous) agents?\b",
        r"\b(llm|large language model|language model|autonomous) agents?\b.*\bmemory systems?\b",
        r"\bmemory modules?\b.*\b(llm|large language model|language model|autonomous) agents?\b",
    ],
    "long-term-memory": [r"\blong[- ]term memory\b", r"\bpersistent memory\b"],
    "memory-types": [r"\bepisodic memory\b", r"\bsemantic memory\b", r"\bprocedural memory\b"],
    "memory-policy": [
        r"\bmemory (write|read|retrieval|update|maintenance|governance|policy|policies|representation|storage|consolidation|security|isolation|access control)\b",
        r"\b(write|read|retrieval) polic(y|ies)\b",
        r"\bshared memory\b.*\b(governance|access control|write polic(y|ies)|retrieval)\b",
        r"\bmemory\b.*\bstorage\b.*\bretrieval\b.*\bmaintenance\b",
    ],
    "benchmark": [r"\b(agent )?memory benchmark\b", r"\bmemory\b.{0,60}\bbenchmark\b", r"\bagent memory evaluation\b", r"\blongmemeval\b", r"\blocomo\b", r"\bagentshield bench\b"],
    "evaluation": [
        r"\bagent memory evaluation\b",
        r"\bmemory\b.{0,80}\bevaluat(e|es|ed|ion|ing)\b",
        r"\bevaluat(e|es|ed|ion|ing)\b.{0,80}\bmemory\b",
        r"\bare we ready\b.{0,120}\b(agent[- ]native )?memory systems?\b",
    ],
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
    r"\bprotein[- ]synthesis[- ]dependent\b",
    r"\bfear memory\b",
    r"\bneural inactivation\b",
    r"\bhippocampus\b",
    r"\bamygdala\b",
    r"\banimal memory\b",
    r"\bpsychology experiments?\b",
    r"\bneuroscience\b",
]

BIOLOGICAL_MEMORY_PATTERNS = [
    r"\bprotein[- ]synthesis[- ]dependent\b",
    r"\bfear memory\b",
    r"\bneural inactivation\b",
    r"\bhippocampus\b",
    r"\bamygdala\b",
    r"\banimal memory\b",
    r"\bhuman cognitive memory\b",
    r"\bpsychology experiments?\b",
    r"\bneuroscience\b",
]

AGENT_CONTEXT = [
    r"\bagents?\b",
    r"\bllm\b",
    r"\blarge language model\b",
    r"\blanguage model\b",
    r"\bautonomous research\b",
    r"\bdeep research\b",
]

AI_MEMORY_CONTEXT = [
    r"\bllm\b",
    r"\blarge language model\b",
    r"\blanguage model agents?\b",
    r"\bai agents?\b",
    r"\bagent memory\b",
    r"\bagent[- ]native memory\b",
]

HIGH_CONFIDENCE_AGENT_MEMORY_PATTERNS = {
    "agent-native memory": r"\bagent[- ]native memory\b",
    "agent memory system": r"\bagent memory systems?\b",
    "memory system for LLM agents": r"\bmemory systems?\b.*\b(llm|large language model|language model)(?:\s+\([^)]+\))? agents?\b|\bmemory (for|in) (llm|large language model|language model)(?:\s+\([^)]+\))? agents?\b.*\b(systems?|storage|retrieval|update|consolidation|maintenance|governance)\b",
    "memory systems and LLM agents": r"\b(llm|large language model|language model) agents?\b.*\bmemory systems?\b|\bmemory systems?\b.*\b(llm|large language model|language model) agents?\b",
    "memory module LLM agent": r"\bmemory modules?\b.*\b(llm|large language model|language model)?\s*agents?\b",
    "persistent memory agent": r"\bpersistent memory\b.*\bagents?\b|\bagents?\b.*\bpersistent memory\b",
    "long-term memory agent": r"\blong[- ]term memory\b.*\bagents?\b|\bagents?\b.*\blong[- ]term memory\b",
    "memory type agent": r"\b(episodic|semantic|procedural) memory\b.*\bagents?\b|\bagents?\b.*\b(episodic|semantic|procedural) memory\b",
    "memory policy LLM agent": r"\bmemory (write|read|retrieval|update|maintenance|governance|policy|policies)\b.*\b(llm|large language model|language model)?\s*agents?\b",
    "memory representation retrieval agent": r"\bmemory representation\b.*\bretrieval\b.*\bagents?\b|\bagents?\b.*\bmemory representation\b.*\bretrieval\b",
    "storage retrieval maintenance memory": r"\b(llm|agent|agents)\b.*\bmemory\b.*\bstorage\b.*\bretrieval\b.*\bmaintenance\b|\bmemory\b.*\bstorage\b.*\bretrieval\b.*\bmaintenance\b.*\b(llm|agent|agents)\b",
    "memory consolidation agent": r"\bmemory consolidation\b.*\bagents?\b|\bagents?\b.*\bmemory consolidation\b",
    "agent memory evaluation": r"\bagent memory evaluation\b",
    "memory benchmark agent": r"\bmemory\b.{0,60}\bbenchmark\b.*\bagents?\b|\bagents?\b.*\bmemory\b.{0,60}\bbenchmark\b",
    "memory security autonomous LLM agents": r"\bmemory security\b.*\bautonomous llm agents?\b|\bautonomous llm agents?\b.*\bmemory security\b",
    "shared memory multi-agent LLM": r"\bshared memory\b.*\bmulti[- ]agent llm systems?\b|\bmulti[- ]agent llm systems?\b.*\bshared memory\b",
    "personal AI agent memory protocol": r"\bmemory protocol\b.*\bpersonal ai agents?\b|\bpersonal ai agents?\b.*\bmemory protocol\b",
    "autoresearch shared memory": r"\bautoresearch\b.*\bshared memory\b|\bshared memory\b.*\bautoresearch\b",
    "agent memory cross-session": r"\bagent memory\b.*\b(cross[- ]session|cross[- ]temporal|persistent)\b|\b(cross[- ]session|cross[- ]temporal|persistent)\b.*\bagent memory\b",
    "parametric memory LLM": r"\b(parametric memory|engram)\b.*\b(llm|large language model|language model|agents?)\b",
}

BROAD_PERIPHERAL_PATTERNS = {
    "recommender-system evaluation": r"\brecommender\b|\ba/b testing\b",
    "broad agentic AI/AGI": r"\bagentic ai\b|\bagentic artificial intelligence\b|\bartificial general intelligence\b|\bagi\b",
    "personality/empathy": r"\bpersonality\b|\bempathy\b|\bhuman shaping\b",
    "cybersecurity/phishing": r"\bphishing\b|\bcybersecurity\b|\bvulnerabilit(y|ies)\b",
    "evacuation/traffic/simulation": r"\bevacuation\b|\btraffic\b|\bsimulation\b|\bphysics-based building\b",
    "GPU/infrastructure": r"\bgpu\b|\bscheduling\b|\bserving\b|\binfrastructure\b|\blow-latency\b",
    "generic RAG": r"\brag\b|\bretrieval augmented generation\b",
}

WEAK_CONTEXT_TAGS = {"llm-agents", "evaluation"}
SYSTEM_LEVEL_HIGH_CONFIDENCE = {
    "agent-native memory",
    "agent memory system",
    "memory system for LLM agents",
    "memory systems and LLM agents",
    "memory module LLM agent",
    "agent memory evaluation",
    "memory benchmark agent",
    "memory security autonomous LLM agents",
    "shared memory multi-agent LLM",
    "personal AI agent memory protocol",
    "autoresearch shared memory",
    "agent memory cross-session",
    "parametric memory LLM",
}
NEGATED_AGENT_MEMORY_PATTERNS = [
    r"\bwithout (studying )?(persistent |long[- ]term |agent[- ]native )?agent memory\b",
    r"\bwithout (studying )?(persistent |long[- ]term )?memory\b",
    r"\bnot (a |about |studying )?(persistent |long[- ]term )?agent memory\b",
    r"\bdoes not (include|use|study|address|evaluate) (persistent |long[- ]term |agent[- ]native )?memory\b",
    r"\bdoes not (study|address|evaluate) (persistent |long[- ]term |agent[- ]native )?agent memory systems?\b",
    r"\bnot (persistent )?(llm[- ]agent|llm agent|agent) memory systems?\b",
    r"\bnot (a |about |studying )?(persistent |long[- ]term )?memory systems?\b",
]

DEEP_RESEARCH_INCLUDE_PATTERNS = {
    "deep-research-agents": [
        r"\bdeep research agents?\b",
        r"\bautonomous research agents?\b",
        r"\bautomated research agents?\b",
        r"\bai research agents?\b",
        r"\bresearch assistant agents?\b",
        r"\bllm research assistants?\b",
    ],
    "ai-scientist": [
        r"\bai scientists?\b",
        r"\bai scientific discovery\b",
        r"\bautomated scientific discovery\b",
        r"\bscientific discovery (llm|language model) agents?\b",
    ],
    "literature-review": [
        r"\bliterature[- ]review agents?\b",
        r"\bautomated literature review\b",
        r"\bllm literature review\b",
    ],
    "citation-grounding": [
        r"\bcitation verification\b",
        r"\bevidence[- ]ground(ed|ing)\b",
        r"\bsource[- ]grounded research\b",
        r"\bresearch reports?\b.{0,80}\bcitations?\b",
        r"\bcitations?\b.{0,80}\bresearch reports?\b",
    ],
    "research-planning": [
        r"\bresearch planning agents?\b",
        r"\bresearch task decomposition\b",
        r"\bmulti[- ]step research planning\b",
        r"\bresearch workflow agents?\b",
    ],
    "multi-agent-research": [
        r"\bmulti[- ]agent research systems?\b",
        r"\bmulti[- ]agent research workflows?\b",
    ],
    "hypothesis-experiment": [
        r"\bhypothesis generation agents?\b",
        r"\bexperiment design agents?\b",
        r"\bhypothesis generation\b.{0,80}\bexperiment design\b",
    ],
    "web-research": [
        r"\bweb[- ]browsing research agents?\b",
        r"\bopenresearch agents?\b",
        r"\bautoresearch\b",
    ],
    "research-memory": [
        r"\bresearch[- ]agent memory\b",
        r"\bresearch state\b",
        r"\biterative research state\b",
    ],
    "benchmark": [
        r"\bresearch agents?\b.{0,80}\bbenchmark\b",
        r"\bbenchmark\b.{0,80}\bresearch agents?\b",
    ],
}

HIGH_CONFIDENCE_DEEP_RESEARCH_PATTERNS = {
    "autonomous research agent": r"\b(autonomous|automated|deep) research agents?\b",
    "source-grounded research agent": r"\bsource[- ]grounded research agents?\b",
    "citation verification": r"\bcitation verification\b|\bevidence[- ]ground(ed|ing)\b.*\bresearch\b",
    "AI scientist": r"\bai scientists?\b|\bai scientific discovery\b|\bautomated scientific discovery\b|\bscientific discovery (llm|language model) agents?\b",
    "literature review agent": r"\bliterature[- ]review agents?\b|\bautomated literature review\b.*\b(llm|agent|agents)\b",
    "research planning": r"\bmulti[- ]step research planning\b|\bresearch planning agents?\b|\bresearch task decomposition\b",
    "multi-agent research workflow": r"\bmulti[- ]agent research (workflow|system)s?\b",
    "hypothesis experiment agent": r"\bhypothesis generation agents?\b|\bexperiment design agents?\b",
    "research reports with citations": r"\bresearch reports?\b.{0,80}\bcitations?\b|\bcitations?\b.{0,80}\bresearch reports?\b",
    "research-agent memory": r"\bresearch[- ]agent memory\b|\biterative research state\b",
}

DEEP_RESEARCH_EXCLUDE_PATTERNS = {
    "generic deep learning": r"\bgeneric deep learning\b|\bdeep learning\b.*\b(image classification|training method|optimization)\b",
    "generic automl": r"\bautoml\b(?!.*\b(research workflow|research agent|scientific discovery|hypothesis|experiment design)\b)",
    "market research": r"\bmarket research\b|\bbusiness research\b|\bcustomer surveys?\b",
    "robotics/autonomous driving": r"\bautonomous driving\b|\brobotics\b|\bmobile robots?\b",
    "general chatbot": r"\bchatbots?\b(?!.*\b(research|citation|evidence|literature review)\b)",
    "generic rag": r"\brag\b(?!.*\b(research|citation|evidence|literature review|source[- ]grounded)\b)|\bretrieval augmented generation\b(?!.*\b(research|citation|evidence|literature review|source[- ]grounded)\b)",
    "generic benchmark": r"\bbenchmark\b(?!.*\b(research agent|deep research|literature review|citation|scientific discovery)\b)",
}

DEEP_RESEARCH_REVIEW_PATTERNS = {
    "general LLM agent research workflow": r"\bllm agents?\b.*\bresearch\b|\bresearch\b.*\bllm agents?\b",
    "research-adjacent rag": r"\b(rag|retrieval augmented generation)\b.*\b(citation|evidence|literature review|research)\b",
    "scientific automl": r"\bautoml\b.*\b(scientific discovery|experiment design|hypothesis|research workflow)\b",
    "web browsing agent": r"\bweb[- ]browsing agents?\b.*\bresearch\b|\bresearch\b.*\bweb[- ]browsing agents?\b",
}

NEGATED_DEEP_RESEARCH_PATTERNS = [
    r"\bwithout (an? )?(autonomous |agentic |source[- ]grounded )?research workflows?\b",
    r"\bwithout (citation verification|evidence[- ]grounding|source[- ]grounded research)\b",
    r"\bnot about research agents?\b",
    r"\bunrelated to research workflows?\b",
    r"\bnot (a |about )?(deep research|autonomous research|research[- ]agent) systems?\b",
]


def classify_with_rules(candidate: PaperCandidate, profile: str = "agent_memory") -> ClassificationResult:
    if profile == "deep_research":
        return _classify_deep_research_with_rules(candidate)
    evidence = explain_rule_matches(candidate)
    text = evidence["text"]
    exclude_hits = evidence["exclude_hits"]
    biological_hits = evidence["biological_memory_hits"]
    include_tags = list(evidence["include_tags"])
    high_confidence_hits = evidence["high_confidence_hits"]
    has_agent_context = bool(evidence["agent_context_hits"])
    broad_hits = evidence["broad_peripheral_hits"]
    negated_memory_focus = bool(evidence["negated_memory_focus_hits"])
    effective_high_confidence_hits = [] if negated_memory_focus else list(high_confidence_hits)
    if broad_hits and not any(hit in SYSTEM_LEVEL_HIGH_CONFIDENCE for hit in effective_high_confidence_hits):
        effective_high_confidence_hits = []

    if biological_hits and not _matches(AI_MEMORY_CONTEXT, text):
        return ClassificationResult(
            score=5,
            decision="irrelevant",
            reason="Excluded: memory topic is biological/cognitive, not LLM-agent memory.",
            tags=["excluded-memory-sense"],
            abstract_summary=_summary(candidate.abstract),
        )

    if negated_memory_focus:
        return ClassificationResult(
            score=20 if has_agent_context else 10,
            decision="irrelevant",
            reason="Peripheral candidate: mentions memory, but not clearly LLM-agent memory.",
            tags=[tag for tag in include_tags if tag in WEAK_CONTEXT_TAGS],
            abstract_summary=_summary(candidate.abstract),
        )

    if exclude_hits and (not include_tags or _matches([r"\bwithout agent memory\b", r"\bwithout persistent memory\b"], text)):
        return ClassificationResult(
            score=5,
            decision="irrelevant",
            reason="Excluded: memory topic is biological/cognitive, hardware, database, or otherwise not LLM-agent memory.",
            tags=["excluded-memory-sense"],
            abstract_summary=_summary(candidate.abstract),
        )

    core_tags = [tag for tag in include_tags if tag not in WEAK_CONTEXT_TAGS]
    if not core_tags and not effective_high_confidence_hits:
        if broad_hits and has_agent_context:
            return ClassificationResult(
                score=45,
                decision="maybe",
                reason="Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.",
                tags=[tag for tag in include_tags if tag in WEAK_CONTEXT_TAGS],
                abstract_summary=_summary(candidate.abstract),
            )
        return ClassificationResult(
            score=20 if has_agent_context else 10,
            decision="irrelevant",
            reason="Peripheral candidate: discusses agents, but not persistent agent memory." if has_agent_context else "Peripheral candidate: mentions memory, but not clearly LLM-agent memory.",
            tags=include_tags,
            abstract_summary=_summary(candidate.abstract),
        )

    score = min(85, len(core_tags) * 18 + (10 if has_agent_context else 0))
    if "agent-memory" in include_tags:
        score += 15
    if "memory-systems" in include_tags and has_agent_context:
        score += 12
    if "benchmark" in include_tags:
        score += 8
    if effective_high_confidence_hits:
        score = max(score, 90)
    if broad_hits and not effective_high_confidence_hits:
        include_tags = [tag for tag in include_tags if tag in WEAK_CONTEXT_TAGS]
        score = max(45, min(score, 62))
    score = min(100, score)

    if effective_high_confidence_hits:
        decision = "relevant"
        reason = _high_confidence_reason(effective_high_confidence_hits)
    elif score >= 70:
        decision = "relevant"
        reason = _focused_reason(include_tags)
    elif score >= 40:
        decision = "maybe"
        reason = (
            "Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory."
            if broad_hits
            else "Peripheral candidate: mentions memory or agents, but not clearly LLM-agent memory."
        )
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


def _classify_deep_research_with_rules(candidate: PaperCandidate) -> ClassificationResult:
    evidence = explain_rule_matches(candidate, profile="deep_research")
    include_tags = list(evidence["include_tags"])
    high_confidence_hits = list(evidence["high_confidence_hits"])
    exclude_hits = list(evidence["exclude_hits"])
    review_hits = list(evidence["review_hits"])
    negated_research_focus = bool(evidence["negated_research_focus_hits"])
    text = evidence["text"]
    summary = _summary(candidate.abstract)

    if negated_research_focus:
        return ClassificationResult(
            score=10,
            decision="irrelevant",
            reason="Excluded: explicitly lacks autonomous research-agent or citation-grounded workflow focus.",
            tags=[],
            abstract_summary=summary,
        )

    if exclude_hits and not high_confidence_hits:
        if review_hits or include_tags:
            return ClassificationResult(
                score=45,
                decision="maybe",
                reason="Review candidate: research-adjacent system, but the agentic research workflow evidence is limited.",
                tags=include_tags or ["research-adjacent"],
                abstract_summary=summary,
            )
        return ClassificationResult(
            score=10,
            decision="irrelevant",
            reason="Excluded: not clearly about autonomous research agents or source-grounded research workflows.",
            tags=["excluded-research-sense"],
            abstract_summary=summary,
        )

    if high_confidence_hits:
        score = min(100, 86 + len(high_confidence_hits) * 3 + len(include_tags) * 2)
        return ClassificationResult(
            score=score,
            decision="relevant",
            reason=_deep_research_reason(high_confidence_hits, include_tags),
            tags=include_tags,
            abstract_summary=summary,
        )

    if include_tags:
        score = min(78, 42 + len(include_tags) * 9 + len(review_hits) * 4)
        decision = "relevant" if score >= 70 and len(include_tags) >= 3 else "maybe"
        reason = (
            "Studies autonomous or source-grounded research-agent workflows."
            if decision == "relevant"
            else "Review candidate: may support deep research workflows but needs human judgment."
        )
        return ClassificationResult(score=score, decision=decision, reason=reason, tags=include_tags, abstract_summary=summary)

    if review_hits:
        return ClassificationResult(
            score=45,
            decision="maybe",
            reason="Review candidate: adjacent to research-agent workflows, but not clearly a deep research system.",
            tags=["research-adjacent"],
            abstract_summary=summary,
        )

    if _matches([r"\bresearch\b", r"\bscientific\b", r"\bliterature review\b"], text):
        return ClassificationResult(
            score=25,
            decision="irrelevant",
            reason="Peripheral candidate: mentions research, but not autonomous research agents or citation-grounded workflows.",
            tags=[],
            abstract_summary=summary,
        )

    return ClassificationResult(
        score=10,
        decision="irrelevant",
        reason="Does not clearly address autonomous research agents or AI-assisted scientific discovery workflows.",
        tags=[],
        abstract_summary=summary,
    )


def explain_rule_matches(candidate: PaperCandidate, profile: str = "agent_memory") -> dict[str, object]:
    text = _paper_text(candidate)
    if profile == "deep_research":
        include_tags = [
            tag
            for tag, patterns in DEEP_RESEARCH_INCLUDE_PATTERNS.items()
            if _matches(patterns, text)
        ]
        high_confidence_hits = _matches_labeled(HIGH_CONFIDENCE_DEEP_RESEARCH_PATTERNS, text)
        if high_confidence_hits:
            for tag in ["deep-research-agents"]:
                if tag not in include_tags:
                    include_tags.append(tag)
        return {
            "text": text,
            "include_tags": include_tags,
            "exclude_hits": _matches_labeled(DEEP_RESEARCH_EXCLUDE_PATTERNS, text),
            "biological_memory_hits": [],
            "agent_context_hits": [],
            "high_confidence_hits": high_confidence_hits,
            "broad_peripheral_hits": [],
            "negated_memory_focus_hits": [],
            "negated_research_focus_hits": _matches(NEGATED_DEEP_RESEARCH_PATTERNS, text),
            "review_hits": _matches_labeled(DEEP_RESEARCH_REVIEW_PATTERNS, text),
        }
    include_tags = [
        tag
        for tag, patterns in INCLUDE_PATTERNS.items()
        if _matches(patterns, text)
    ]
    high_confidence_hits = _matches_labeled(HIGH_CONFIDENCE_AGENT_MEMORY_PATTERNS, text)
    negated_memory_focus_hits = _matches(NEGATED_AGENT_MEMORY_PATTERNS, text)
    if high_confidence_hits and not negated_memory_focus_hits:
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
        "biological_memory_hits": _matches(BIOLOGICAL_MEMORY_PATTERNS, text),
        "agent_context_hits": _matches(AGENT_CONTEXT, text),
        "high_confidence_hits": high_confidence_hits,
        "broad_peripheral_hits": _matches_labeled(BROAD_PERIPHERAL_PATTERNS, text),
        "negated_memory_focus_hits": negated_memory_focus_hits,
        "negated_research_focus_hits": [],
        "review_hits": [],
    }


def should_consider_for_llm(result: ClassificationResult) -> bool:
    return result.decision in {"relevant", "maybe"} and result.score >= 40


def _paper_text(candidate: PaperCandidate) -> str:
    return f"{candidate.title}\n{candidate.abstract}".lower()


def _matches(patterns: list[str], text: str) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, flags=re.I)]


def _matches_labeled(patterns: dict[str, str], text: str) -> list[str]:
    return [label for label, pattern in patterns.items() if re.search(pattern, text, flags=re.I)]


def _high_confidence_reason(matches: list[str]) -> str:
    if any("benchmark" in match or "evaluation" in match for match in matches):
        return "Evaluates memory mechanisms or benchmarks for LLM agents."
    if any("security" in match for match in matches):
        return "Evaluates memory security or cross-session memory risks in autonomous LLM agents."
    if any("shared memory" in match or "protocol" in match or "cross-session" in match for match in matches):
        return "Studies governed shared memory or persistent memory protocols for LLM agents."
    if any("parametric" in match or "Engram" in match for match in matches):
        return "Discusses Engram-style or parametric memory mechanisms for language models."
    if any("consolidation" in match or "policy" in match or "storage" in match or "retrieval" in match for match in matches):
        return "Studies memory storage, retrieval, update, or consolidation for LLM agents."
    if any("persistent" in match or "long-term" in match for match in matches):
        return "Focuses on persistent or long-term memory for agent behavior."
    return "Studies memory systems or memory modules for LLM agents."


def _focused_reason(tags: list[str]) -> str:
    if "benchmark" in tags or "evaluation" in tags:
        return "Evaluates memory mechanisms or benchmarks for LLM agents."
    if "parametric-memory" in tags:
        return "Discusses Engram-style or parametric memory mechanisms for language models."
    if "memory-policy" in tags:
        return "Studies memory storage, retrieval, update, or consolidation for LLM agents."
    if "long-term-memory" in tags:
        return "Focuses on persistent or long-term memory for agent behavior."
    if "memory-types" in tags:
        return "Studies episodic, semantic, or procedural memory for agents."
    if "memory-systems" in tags:
        return "Studies memory systems or memory modules for LLM agents."
    return "Studies agent memory with explicit LLM or agent context."


def _deep_research_reason(matches: list[str], tags: list[str]) -> str:
    if any("citation" in match or "source-grounded" in match or "reports" in match for match in matches):
        return "Studies source-grounded research workflows, citation verification, or evidence-backed research reports."
    if any("AI scientist" in match or "scientific discovery" in match for match in matches):
        return "Studies AI-scientist or scientific-discovery agents."
    if any("literature" in match for match in matches) or "literature-review" in tags:
        return "Studies automated literature-review systems or literature-review agents."
    if any("planning" in match or "multi-agent" in match or "hypothesis" in match for match in matches):
        return "Studies multi-step planning, multi-agent workflows, or hypothesis and experiment-design agents for research."
    if "research-memory" in tags:
        return "Studies research-agent memory or iterative research state."
    return "Studies autonomous or deep research agents."


def _summary(abstract: str, max_chars: int = 320) -> str:
    compact = " ".join((abstract or "").split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."
