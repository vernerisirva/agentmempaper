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

    def test_rules_mark_memory_consolidation_for_llm_agents_highly_relevant(self):
        candidate = PaperCandidate(
            title="Trustworthy Memory Consolidation for LLM Agents",
            authors=["Ada Lovelace"],
            abstract=(
                "We study memory consolidation for LLM agents with persistent memory, "
                "retrieval, and update policies across long-horizon tasks."
            ),
            source="fixture",
            source_id="memory-consolidation",
            url="https://example.test/memory-consolidation",
            published_date="2026-01-01",
        )

        result = classify_with_rules(candidate)

        self.assertEqual(result.decision, "relevant")
        self.assertGreaterEqual(result.score, 85)
        self.assertIn("memory-policy", result.tags)

    def test_rules_mark_agent_memory_benchmarks_highly_relevant(self):
        candidate = PaperCandidate(
            title="MGBench: Memory Governance Benchmark for Agentic Long-Term Memory",
            authors=["Grace Hopper"],
            abstract=(
                "This benchmark evaluates memory governance, retrieval, update, and "
                "long-term memory behavior in LLM agents."
            ),
            source="fixture",
            source_id="agent-memory-benchmark",
            url="https://example.test/benchmark",
            published_date="2026-01-01",
        )

        result = classify_with_rules(candidate)

        self.assertEqual(result.decision, "relevant")
        self.assertGreaterEqual(result.score, 85)
        self.assertIn("benchmark", result.tags)

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

    def test_rules_do_not_make_broad_agent_papers_highly_relevant(self):
        examples = [
            (
                "Exploring Recommender System Evaluation: A Multi-Modal LLM Agent Framework for A/B Testing",
                "We propose LLM agents for recommender-system A/B testing and evaluation, with updating experiment dashboards.",
            ),
            (
                "Agentic Artificial Intelligence and Artificial General Intelligence: Emerging Paradigms",
                "A broad survey of agentic AI and AGI foundations, autonomy, planning, and societal impact.",
            ),
            (
                "The meek shall inherit the Earth: personality, empathy, and the human shaping of LLMs",
                "We study personality, empathy, and human preference shaping in LLM behavior over long-term interactions.",
            ),
            (
                "A Lightweight Agentic AI Framework with DeepSeek-R1 for Adaptive Phishing URL Detection",
                "LLM agents coordinate tool calls for phishing URL detection and cybersecurity classification.",
            ),
            (
                "LLM-Guided Multi-Agent Evacuation Coordination via Episodic Memory and Cognitive Task Analysis",
                "Agents coordinate evacuation and traffic simulation with cognitive task analysis, but not persistent agent memory systems.",
            ),
            (
                "SwarmX: Agentic Scheduling for Low-Latency Agentic Systems",
                "Agentic scheduling improves GPU serving throughput and low-latency model inference.",
            ),
            (
                "Memory-Efficient Attention for LLM Agents",
                "Attention kernels reduce KV cache use and GPU memory allocation for serving agents.",
            ),
            (
                "RAVEN: Agentic RAG for Automated Vulnerability Repair",
                "A generic RAG system retrieves repository context for software repair without persistent memory.",
            ),
        ]

        for title, abstract in examples:
            with self.subTest(title=title):
                result = classify_with_rules(
                    PaperCandidate(
                        title=title,
                        authors=["Fixture Author"],
                        abstract=abstract,
                        source="fixture",
                        source_id=title,
                        url="https://example.test/peripheral",
                        published_date="2026-01-01",
                    )
                )

                self.assertNotEqual(result.decision, "relevant")
                self.assertLess(result.score, 70)

    def test_fixture_evaluation_has_no_rule_false_negatives_or_false_positives(self):
        report = evaluate_relevance_examples(relevance_fixture_examples(), use_llm=False)

        self.assertEqual(report["false_positives"], [])
        self.assertEqual(report["false_negatives"], [])
        self.assertGreaterEqual(report["precision"], 0.95)
        self.assertGreaterEqual(report["recall"], 0.95)


if __name__ == "__main__":
    unittest.main()
