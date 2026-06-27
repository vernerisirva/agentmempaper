import unittest

from paper_scout.models import PaperCandidate
from paper_scout.relevance import classify_with_rules, should_consider_for_llm
from paper_scout.evaluation import relevance_fixture_examples, evaluate_relevance_examples


class PaperScoutRelevanceTest(unittest.TestCase):
    def test_rules_mark_agent_native_memory_system_paper_highly_relevant(self):
        candidate = PaperCandidate(
            title="Are We Ready For An Agent-Native Memory System?",
            authors=["Wei Zhou", "Guoliang Li", "Fan Wu"],
            abstract=(
                "Memory for large language model (LLM) agents has rapidly evolved "
                "from retrieval-augmented mechanisms into a data management system "
                "that supports persistent information storage, retrieval, update, "
                "consolidation, and lifecycle governance throughout agent execution. "
                "We evaluate agent-native memory systems for LLM agents."
            ),
            source="arxiv",
            source_id="2606.24775",
            arxiv_id="2606.24775",
            url="https://arxiv.org/abs/2606.24775",
            published_date="2026-06-23",
        )

        result = classify_with_rules(candidate)

        self.assertEqual(result.decision, "relevant")
        self.assertGreaterEqual(result.score, 85)
        self.assertIn("agent-memory", result.tags)
        self.assertIn("memory-systems", result.tags)
        self.assertIn("llm-agents", result.tags)
        self.assertIn("evaluation", result.tags)

    def test_rules_mark_memory_systems_for_llm_agents_highly_relevant(self):
        candidate = PaperCandidate(
            title="Memory Modules for LLM Agents",
            authors=["Ada Lovelace"],
            abstract=(
                "This paper studies a memory system for LLM agents with memory "
                "representation, storage, retrieval, maintenance, and consolidation."
            ),
            source="fixture",
            source_id="memory-system-llm-agents",
            url="https://example.test/memory-system",
            published_date="2026-01-01",
        )

        result = classify_with_rules(candidate)

        self.assertEqual(result.decision, "relevant")
        self.assertGreaterEqual(result.score, 85)
        self.assertIn("memory-systems", result.tags)
        self.assertIn("memory-policy", result.tags)

    def test_rules_mark_agent_memory_paper_relevant(self):
        candidate = PaperCandidate(
            title="Long-Term Memory for LLM Agents",
            authors=["Ada Lovelace"],
            abstract=(
                "We introduce persistent episodic and semantic memory write and "
                "retrieval policies for language model agents."
            ),
            source="arxiv",
            source_id="2601.1",
            url="https://arxiv.org/abs/2601.1",
            published_date="2026-01-01",
        )

        result = classify_with_rules(candidate)

        self.assertEqual(result.decision, "relevant")
        self.assertGreaterEqual(result.score, 70)
        self.assertIn("agent-memory", result.tags)
        self.assertTrue(should_consider_for_llm(result))

    def test_rules_exclude_gpu_memory_papers(self):
        candidate = PaperCandidate(
            title="GPU Memory Efficient Attention for Transformers",
            authors=["Grace Hopper"],
            abstract="This paper improves kernel memory utilization and throughput.",
            source="openalex",
            source_id="W1",
            url="https://example.test/gpu",
            published_date="2026-01-01",
        )

        result = classify_with_rules(candidate)

        self.assertEqual(result.decision, "irrelevant")
        self.assertLess(result.score, 30)
        self.assertFalse(should_consider_for_llm(result))

    def test_fixture_evaluation_has_no_rule_false_negatives_or_false_positives(self):
        report = evaluate_relevance_examples(relevance_fixture_examples(), use_llm=False)

        self.assertEqual(report["false_positives"], [])
        self.assertEqual(report["false_negatives"], [])
        self.assertGreaterEqual(report["precision"], 0.95)
        self.assertGreaterEqual(report["recall"], 0.95)


if __name__ == "__main__":
    unittest.main()
