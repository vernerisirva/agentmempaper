from types import SimpleNamespace
import unittest

from paper_scout.structured_cards import NOT_EXTRACTED, structured_card_for_paper


def paper(**overrides):
    data = {
        "title": "Untitled Paper",
        "abstract_summary": "",
        "reason": "",
        "tags": [],
        "decision": "maybe",
        "research_note": None,
    }
    data.update(overrides)
    return SimpleNamespace(**data)


class StructuredCardsTest(unittest.TestCase):
    def test_benchmark_paper_gets_conservative_benchmark_mapping(self):
        card = structured_card_for_paper(
            paper(
                title="MGBench: Memory Governance Benchmark for Agentic Long-Term Memory",
                abstract_summary="A benchmark for evaluating long-term memory behavior in LLM agents.",
                reason="Evaluates persistent memory in agents.",
                tags=["benchmark", "agent-memory"],
                decision="relevant",
            )
        )

        self.assertEqual(card["method_or_system_type"]["value"], "Benchmark / evaluation")
        self.assertEqual(
            card["relation_to_agentic_memory"]["value"],
            "Evaluates memory behavior, safety, or retrieval in LLM agents",
        )
        self.assertEqual(card["method_or_system_type"]["provenance"], "abstract")
        self.assertIn("Abstract-level signal", card["evidence_or_evaluation"]["value"])

    def test_memory_architecture_paper_gets_system_mapping(self):
        card = structured_card_for_paper(
            paper(
                title="Are We Ready For An Agent-Native Memory System?",
                abstract_summary="Studies memory systems and memory modules for LLM agents.",
                reason="Studies memory systems or memory modules for LLM agents.",
                tags=["agent-memory", "memory-systems", "llm-agents"],
                decision="relevant",
            )
        )

        self.assertEqual(card["method_or_system_type"]["value"], "Memory architecture / system")
        self.assertEqual(
            card["relation_to_agentic_memory"]["value"],
            "Studies memory mechanisms or governance for LLM agents",
        )
        self.assertEqual(card["key_contribution"]["value"], NOT_EXTRACTED)

    def test_peripheral_paper_stays_review_candidate(self):
        card = structured_card_for_paper(
            paper(
                title="Broad Agentic AI System Architecture",
                abstract_summary="A broad agentic AI system without explicit persistent memory evidence.",
                reason="Peripheral candidate: discusses agentic AI system architecture, but does not clearly study persistent agent memory.",
                tags=["llm-agents"],
                decision="maybe",
            )
        )

        self.assertEqual(card["research_relevance"]["value"], "Review candidate")
        self.assertEqual(
            card["relation_to_agentic_memory"]["value"],
            "Agentic-AI connection exists, but memory focus is weak or indirect",
        )
        self.assertEqual(card["relation_to_agentic_memory"]["confidence"], "low")

    def test_unknown_fields_are_not_hallucinated(self):
        card = structured_card_for_paper(paper(title="A Sparse Metadata Record"))

        self.assertEqual(card["method_or_system_type"]["value"], NOT_EXTRACTED)
        self.assertEqual(card["key_contribution"]["value"], NOT_EXTRACTED)
        self.assertEqual(card["evidence_or_evaluation"]["value"], NOT_EXTRACTED)
        self.assertEqual(card["limitations_or_uncertainty"]["confidence"], "high")


if __name__ == "__main__":
    unittest.main()
