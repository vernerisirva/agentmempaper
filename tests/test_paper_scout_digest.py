import unittest

from paper_scout.digest import DigestMetadata, render_digest
from paper_scout.models import DigestPaper


class PaperScoutDigestTest(unittest.TestCase):
    def test_renders_relevant_and_maybe_groups(self):
        papers = [
            DigestPaper(
                canonical_key="doi:10.1/example",
                title="Persistent Memory for LLM Agents",
                authors=["Ada Lovelace", "Grace Hopper"],
                abstract="A long abstract about persistent memory for LLM agents.",
                source="arxiv",
                url="https://arxiv.org/abs/2601.1",
                published_date="2026-01-01",
                score=91,
                decision="relevant",
                reason="Directly studies persistent LLM agent memory.",
                tags=["agent-memory"],
            ),
            DigestPaper(
                canonical_key="title:maybe",
                title="Parametric Memory in Language Models",
                authors=["Jane Smith"],
                abstract="Connects parametric memory to agent behavior.",
                source="openalex",
                url="https://example.test/maybe",
                published_date="2026-01-02",
                score=61,
                decision="maybe",
                reason="Relevant if framed around agents.",
                tags=["parametric-memory"],
            ),
        ]

        rendered = render_digest(
            "2026-06-26",
            papers,
            DigestMetadata(
                run_id=7,
                source_counts={"arxiv": 3, "openalex": 2},
                fetched_count=5,
                unique_count=2,
                decision_counts={"relevant": 1, "maybe": 1, "irrelevant": 3},
            ),
        )

        self.assertIn("# Paper Scout Digest - 2026-06-26", rendered)
        self.assertIn("- **Run ID:** 7", rendered)
        self.assertIn("- **Candidates fetched:** 5", rendered)
        self.assertIn("## Highly Relevant", rendered)
        self.assertIn("## Maybe Relevant", rendered)
        self.assertIn("Persistent Memory for LLM Agents", rendered)
        self.assertIn("Parametric Memory in Language Models", rendered)
        self.assertIn("Directly studies persistent LLM agent memory.", rendered)


if __name__ == "__main__":
    unittest.main()
