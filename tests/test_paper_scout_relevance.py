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

    def test_persistent_action_capable_systems_do_not_imply_persistent_memory(self):
        result = classify_with_rules(
            PaperCandidate(
                title="OpenClaw and Ollama in Agentic AI: Toward Fully Autonomous and Scalable AI Agent Systems",
                authors=["Konstantinos I. Roumeliotis", "Ranjan Sapkota"],
                abstract=(
                    "The rapid transition from reactive large language model interfaces to persistent, "
                    "action-capable systems has revealed gaps in architectural understanding of Agentic AI, "
                    "particularly in disentangling inference, orchestration, and execution layers. "
                    "The architecture discusses memory hierarchy and says persistent memory can emerge "
                    "from system integration as one autonomous capability among tool use, planning, "
                    "orchestration, execution, governance, and benchmarking."
                ),
                source="semantic_scholar",
                source_id="openclaw",
                doi="10.2139/ssrn.6584998",
                published_date="2026",
            )
        )

        self.assertEqual(result.decision, "maybe")
        self.assertLess(result.score, 70)
        self.assertIn("Peripheral candidate", result.reason)
        self.assertNotIn("persistent or long-term memory", result.reason)
        self.assertNotIn("long-term-memory", result.tags)
        self.assertNotIn("memory-systems", result.tags)

    def test_rules_exclude_biological_and_human_memory_without_ai_agent_context(self):
        examples = [
            (
                "No evidence for a protein-synthesis-dependent form of long-term fear memory",
                "Translational inhibition and neural inactivation disrupt short- and long-term memory measures in animal fear memory to the same degree.",
            ),
            (
                "Hippocampus and Amygdala Contributions to Long-Term Memory",
                "Neuroscience experiments examine hippocampus, amygdala, neural inactivation, and animal memory consolidation.",
            ),
            (
                "Human Cognitive Memory Recall in Psychology",
                "Psychology experiments study human cognitive memory, working memory, and recall without AI agents.",
            ),
        ]

        for title, abstract in examples:
            with self.subTest(title=title):
                result = classify_with_rules(
                    PaperCandidate(
                        title=title,
                        authors=["Memory Researcher"],
                        abstract=abstract,
                        source="fixture",
                        source_id=title,
                        published_date="2026-01-01",
                    )
                )

                self.assertEqual(result.decision, "irrelevant")
                self.assertLess(result.score, 40)
                self.assertIn("biological/cognitive", result.reason)

    def test_rules_keep_memory_security_benchmarks_for_autonomous_llm_agents_highly_relevant(self):
        result = classify_with_rules(
            PaperCandidate(
                title="AgentShield Bench v2: Evaluating Memory Security, Persistent Jailbreaks, and Cross Session Compromise in Autonomous LLM Agents",
                authors=["Security Researcher"],
                abstract=(
                    "We evaluate memory security, persistent jailbreaks, cross-session compromise, "
                    "and memory isolation failures in autonomous LLM agents."
                ),
                source="fixture",
                source_id="agentshield",
                published_date="2026-01-01",
            )
        )

        self.assertEqual(result.decision, "relevant")
        self.assertGreaterEqual(result.score, 85)
        self.assertIn("benchmark", result.tags)
        self.assertIn("agent-memory", result.tags)

    def test_rules_review_strong_agent_memory_candidates(self):
        examples = [
            (
                "Memory Contagion: Cross-Temporal Propagation of Evaluator Bias via Agent Memory",
                "This paper studies how evaluator bias propagates across sessions via persistent agent memory in LLM agent evaluations.",
            ),
            (
                "Governed Shared Memory for Multi-Agent LLM Systems",
                "We propose governed shared memory for multi-agent LLM systems with memory access control, write policies, and retrieval governance.",
            ),
            (
                "MiS Protocol: A Cognitive Memory Protocol for Personal AI Agents",
                "A cognitive memory protocol for personal AI agents manages persistent memory storage, retrieval, and update.",
            ),
            (
                "Negative Knowledge as Failure-aware Shared Memory for AutoResearch",
                "AutoResearch agents share failure-aware memory across literature-review and experiment-planning sessions.",
            ),
        ]

        for title, abstract in examples:
            with self.subTest(title=title):
                result = classify_with_rules(
                    PaperCandidate(
                        title=title,
                        authors=["Agent Memory Researcher"],
                        abstract=abstract,
                        source="fixture",
                        source_id=title,
                        published_date="2026-01-01",
                    )
                )

                self.assertEqual(result.decision, "relevant")
                self.assertGreaterEqual(result.score, 70)

    def test_reason_text_is_conservative_for_weak_memory_or_agent_evidence(self):
        weak_memory = classify_with_rules(
            PaperCandidate(
                title="Memory Mentioned in Agentic Software Engineering",
                authors=["Ada Lovelace"],
                abstract="This paper mentions memory in passing while discussing agents, but not persistent LLM-agent memory systems.",
                source="fixture",
                source_id="weak-memory",
                published_date="2026-01-01",
            )
        )
        generic_agent = classify_with_rules(
            PaperCandidate(
                title="Agents for Enterprise Task Routing",
                authors=["Ada Lovelace"],
                abstract="LLM agents route tasks and call tools, but the system does not include persistent memory.",
                source="fixture",
                source_id="generic-agent",
                published_date="2026-01-01",
            )
        )

        self.assertIn("Peripheral candidate", weak_memory.reason)
        self.assertNotIn("Studies memory storage, retrieval, update, or consolidation for LLM agents", weak_memory.reason)
        self.assertIn("Peripheral candidate", generic_agent.reason)

    def test_fixture_evaluation_has_no_rule_false_negatives_or_false_positives(self):
        report = evaluate_relevance_examples(relevance_fixture_examples(), use_llm=False)

        self.assertEqual(report["false_positives"], [])
        self.assertEqual(report["false_negatives"], [])
        self.assertGreaterEqual(report["precision"], 0.95)
        self.assertGreaterEqual(report["recall"], 0.95)

    def test_deep_research_profile_surfaces_autonomous_research_agents(self):
        result = classify_with_rules(
            PaperCandidate(
                title="Autonomous Research Agents for Source-Grounded Scientific Discovery",
                authors=["Researcher"],
                abstract="A deep research agent plans multi-step literature reviews, verifies citations, and generates source-grounded research reports.",
                source="fixture",
                source_id="deep-research-core",
            ),
            profile="deep_research",
        )

        self.assertEqual(result.decision, "relevant")
        self.assertGreaterEqual(result.score, 85)
        self.assertIn("deep-research-agents", result.tags)
        self.assertIn("citation-grounding", result.tags)

    def test_deep_research_profile_downgrades_generic_deep_learning_and_market_research(self):
        generic_deep_learning = classify_with_rules(
            PaperCandidate(
                title="Deep Learning Optimization for Image Classification",
                authors=["Researcher"],
                abstract="A generic deep learning training method unrelated to autonomous research workflows.",
                source="fixture",
                source_id="generic-dl",
            ),
            profile="deep_research",
        )
        market_research = classify_with_rules(
            PaperCandidate(
                title="Market Research Automation with Chatbots",
                authors=["Researcher"],
                abstract="Business market research automation using a chatbot for customer surveys.",
                source="fixture",
                source_id="market-research",
            ),
            profile="deep_research",
        )

        self.assertEqual(generic_deep_learning.decision, "irrelevant")
        self.assertNotEqual(market_research.decision, "relevant")

    def test_deep_research_profile_keeps_generic_rag_automl_and_human_ai_bibliometrics_out_of_high_relevance(self):
        examples = [
            (
                "Generic RAG for Enterprise Knowledge Search",
                "Retrieval augmented generation improves document search, but does not include autonomous research planning, citation verification, or literature-review agents.",
            ),
            (
                "AutoML Optimization for Tabular Prediction",
                "AutoML searches model hyperparameters for generic deep learning and tabular prediction without scientific-discovery agents or research workflows.",
            ),
            (
                "Young AI Scientists in the New AI Age",
                "A bibliometric study of human AI researchers, career novelty, and research trajectories in the AI field.",
            ),
        ]

        for title, abstract in examples:
            with self.subTest(title=title):
                result = classify_with_rules(
                    PaperCandidate(
                        title=title,
                        authors=["Researcher"],
                        abstract=abstract,
                        source="fixture",
                        source_id=title,
                    ),
                    profile="deep_research",
                )

                self.assertNotEqual(result.decision, "relevant")
                self.assertLess(result.score, 70)


if __name__ == "__main__":
    unittest.main()
