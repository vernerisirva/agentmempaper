import tempfile
import unittest
from pathlib import Path

from paper_scout.config import load_config


class PaperScoutConfigTest(unittest.TestCase):
    def test_default_config_includes_agent_native_memory_search_terms(self):
        config = load_config("config/paper_scout.yaml")

        for term in [
            "agent-native memory",
            "agent native memory",
            "agent memory system",
            "agent memory systems",
            "LLM agent memory system",
            "memory system for LLM agents",
            "memory module LLM agent",
            "persistent memory LLM agent",
            "long-term memory LLM agent",
            "memory retrieval LLM agent",
            "memory consolidation LLM agent",
            "agent memory evaluation",
            "agent memory benchmark",
        ]:
            self.assertIn(term, config.terms)

    def test_loads_research_context_and_env_state_override(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "paper_scout.yaml"
            config_path.write_text(
                """
search:
  days: 14
  max_results_per_source: 10
  terms:
    - "deep research agent memory"
state:
  sqlite_path: "data/paper_scout.sqlite3"
output:
  digest_dir: "digests"
  report_dir: "reports/paper_scout"
research_context:
  - "Deep research agents are relevant to this thesis scope."
exclusions:
  - "GPU memory"
""",
                encoding="utf-8",
            )

            config = load_config(config_path, env={"PAPER_SCOUT_STATE_PATH": str(Path(tmpdir) / "override.sqlite3")})

            self.assertEqual(config.terms, ["deep research agent memory"])
            self.assertEqual(config.days, 14)
            self.assertEqual(config.sqlite_path, Path(tmpdir) / "override.sqlite3")
            self.assertEqual(config.report_dir, Path("reports/paper_scout"))
            self.assertIn("Deep research agents are relevant", config.research_context[0])
            self.assertIn("GPU memory", config.exclusions)

    def test_loads_deep_research_track_config(self):
        config = load_config(track_id="deep_research")

        self.assertEqual(config.track_id, "deep_research")
        self.assertEqual(config.title, "Deep Research Paper Library")
        self.assertEqual(config.docs_dir, Path("docs/deep-research"))
        self.assertEqual(config.sqlite_path, Path("data/deep_research/paper_scout.sqlite3"))
        self.assertEqual(config.report_dir, Path("reports/paper_scout/deep_research"))
        self.assertEqual(config.curation_path, Path("config/curation/deep_research.yaml"))
        self.assertEqual(config.relevance_profile, "deep_research")
        for term in [
            "deep research agent",
            "autonomous research agent",
            "AI scientist",
            "automated literature review",
            "citation verification agent",
            "scientific discovery LLM agent",
        ]:
            self.assertIn(term, config.terms)

    def test_loads_nested_discovery_queries_and_sweep(self):
        config = load_config(track_id="agent_memory")

        self.assertEqual(config.discovery_queries["arxiv"][1].query, "procedural memory")
        self.assertEqual(config.discovery_queries["arxiv"][1].mode, "all_terms")
        self.assertEqual(config.query_budgets["semantic_scholar"], 4)
        self.assertTrue(config.arxiv_sweep.enabled)
        self.assertEqual(config.arxiv_sweep.categories, ("cs.AI", "cs.CL", "cs.LG"))

    def test_loads_quality_configuration_for_both_tracks(self):
        for track in ("agent_memory", "deep_research"):
            config = load_config(track_id=track)
            self.assertTrue(config.quality.enabled)
            self.assertEqual(config.quality.mode, "auto")
            self.assertEqual(config.quality.assessment.version, "quality-v1")
            self.assertEqual(config.quality.assessment.rubric_version, "scholarly-rubric-v1")
            self.assertEqual(config.quality.ranking.behavior, "downrank")
            self.assertTrue(config.quality.ranking.unknown_quality_is_neutral)
            self.assertIn(track, str(config.quality.full_text.cache_dir))

    def test_rejects_invalid_quality_ranking_configuration(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "invalid.yaml"
            config_path.write_text(
                """quality:\n  enabled: true\n  ranking:\n    behavior: hide\n    quality_weight: -1\n""",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "ranking weights"):
                load_config(config_path)


if __name__ == "__main__":
    unittest.main()
