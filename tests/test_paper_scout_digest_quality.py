import tempfile
import unittest
from pathlib import Path

from paper_scout.digest_quality import analyze_digest_quality, write_digest_quality_report
from paper_scout.models import DigestPaper


def digest_paper(title: str, abstract: str) -> DigestPaper:
    return DigestPaper(
        canonical_key=title.lower().replace(" ", "-"),
        title=title,
        authors=["Ada Lovelace"],
        abstract=abstract,
        source="fixture",
        url="https://example.test/paper",
        published_date="2026-06-26",
        score=77,
        decision="relevant",
        reason="fixture",
        tags=[],
    )


class PaperScoutDigestQualityTest(unittest.TestCase):
    def test_flags_obvious_gpu_cuda_and_database_false_positives(self):
        papers = [
            digest_paper("CUDA GPU Memory Allocation for Kernels", "Improves memory bandwidth and allocation."),
            digest_paper("Database Memory Indexing", "An in-memory database storage layout."),
        ]

        report = analyze_digest_quality(papers)

        self.assertEqual(report.flagged_count, 2)
        self.assertEqual([item.title for item in report.flagged], [paper.title for paper in papers])
        self.assertIn("GPU memory", report.flagged[0].matched_risk_terms)
        self.assertIn("database memory", report.flagged[1].matched_risk_terms)

    def test_does_not_flag_clearly_relevant_agentic_memory_papers(self):
        papers = [
            digest_paper(
                "Persistent Memory for LLM Agents",
                "A deep research agent uses persistent memory and episodic memory across sessions.",
            ),
            digest_paper(
                "Engram Parametric Memory for Language Models",
                "Engram-style parametric memory mechanisms for model-internal agent knowledge.",
            ),
        ]

        report = analyze_digest_quality(papers)

        self.assertEqual(report.flagged_count, 0)

    def test_writes_markdown_report(self):
        papers = [digest_paper("GPU Memory Bandwidth", "Memory bandwidth optimization for accelerators.")]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_digest_quality_report(Path(tmpdir), "2026-06-26", papers)

            markdown = path.read_text(encoding="utf-8")
            self.assertIn("Paper Scout Digest Quality", markdown)
            self.assertIn("Likely false positives flagged: 1", markdown)
            self.assertIn("GPU Memory Bandwidth", markdown)


if __name__ == "__main__":
    unittest.main()
