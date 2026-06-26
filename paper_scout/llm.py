from __future__ import annotations

import json
import logging
import os

from paper_scout.http import HttpClient
from paper_scout.models import ClassificationResult, PaperCandidate

LOGGER = logging.getLogger(__name__)


class LlmClassifier:
    def classify(self, candidate: PaperCandidate, rule_result: ClassificationResult) -> ClassificationResult:
        raise NotImplementedError


class NoopLlmClassifier(LlmClassifier):
    def classify(self, candidate: PaperCandidate, rule_result: ClassificationResult) -> ClassificationResult:
        return rule_result


class OpenAICompatibleClassifier(LlmClassifier):
    def __init__(self, api_key: str, model: str, base_url: str = "https://api.openai.com/v1", http: HttpClient | None = None) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.http = http or HttpClient()

    def classify(self, candidate: PaperCandidate, rule_result: ClassificationResult) -> ClassificationResult:
        prompt = {
            "rubric": (
                "Relevant: long-term memory for LLM agents; episodic, semantic, or procedural memory in agents; "
                "memory write/read/retrieval policies; agent memory benchmarks; persistent memory for deep research agents; "
                "memory-augmented LLM systems; parametric memory or engram mechanisms when connected to agents or LLM behavior. "
                "Irrelevant: GPU memory, memory-efficient attention, database memory systems, human memory without AI-agent connection, "
                "or generic RAG without persistent agent memory."
            ),
            "title": candidate.title,
            "authors": candidate.authors,
            "abstract": candidate.abstract,
            "rule_score": rule_result.score,
            "rule_decision": rule_result.decision,
        }
        payload = {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Classify paper relevance. Return only JSON with keys: "
                        "score integer 0-100, decision relevant/maybe/irrelevant, reason string, tags array, abstract_summary string."
                    ),
                },
                {"role": "user", "content": json.dumps(prompt)},
            ],
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = self.http.post_json(f"{self.base_url}/chat/completions", payload, headers=headers)
        content = json.loads(response)["choices"][0]["message"]["content"]
        parsed = json.loads(_strip_json_fence(content))
        return ClassificationResult(
            score=max(0, min(100, int(parsed.get("score", rule_result.score)))),
            decision=_clean_decision(parsed.get("decision", rule_result.decision)),
            reason=str(parsed.get("reason", rule_result.reason)),
            tags=[str(tag) for tag in parsed.get("tags", rule_result.tags)],
            abstract_summary=str(parsed.get("abstract_summary", rule_result.abstract_summary or "")),
            classifier="llm",
        )


def classifier_from_env() -> LlmClassifier:
    provider = os.environ.get("PAPER_SCOUT_LLM_PROVIDER", "auto").lower()
    if provider in {"", "none", "off", "rules"}:
        return NoopLlmClassifier()

    api_key = os.environ.get("PAPER_SCOUT_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return NoopLlmClassifier()

    model = os.environ.get("PAPER_SCOUT_LLM_MODEL")
    if not model:
        return NoopLlmClassifier()
    base_url = os.environ.get("PAPER_SCOUT_LLM_BASE_URL", "https://api.openai.com/v1")
    return OpenAICompatibleClassifier(api_key=api_key, model=model, base_url=base_url)


def classify_with_optional_llm(
    candidate: PaperCandidate,
    rule_result: ClassificationResult,
    classifier: LlmClassifier | None = None,
) -> ClassificationResult:
    llm = classifier or classifier_from_env()
    try:
        return llm.classify(candidate, rule_result)
    except Exception as exc:  # noqa: BLE001 - classifier failure should not fail the scout run.
        LOGGER.warning("LLM classification failed for %s: %s", candidate.title, exc)
        return rule_result


def _clean_decision(value: object) -> str:
    decision = str(value).lower()
    return decision if decision in {"relevant", "maybe", "irrelevant"} else "maybe"


def _strip_json_fence(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:]
    return stripped.strip()
