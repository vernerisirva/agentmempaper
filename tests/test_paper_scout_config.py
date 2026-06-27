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


if __name__ == "__main__":
    unittest.main()
