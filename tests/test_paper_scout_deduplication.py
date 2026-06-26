import unittest

from paper_scout.models import PaperCandidate
from paper_scout.deduplication import canonical_key


class PaperScoutDeduplicationTest(unittest.TestCase):
    def test_prefers_doi_for_canonical_key(self):
        candidate = PaperCandidate(
            title="Agent Memory",
            authors=["Ada Lovelace"],
            abstract="",
            source="arxiv",
            source_id="2601.12345",
            doi="10.48550/arxiv.2601.12345",
            arxiv_id="2601.12345",
            semantic_scholar_id="S2",
            openalex_id="W1",
            url="https://arxiv.org/abs/2601.12345",
            published_date="2026-01-01",
        )

        self.assertEqual(canonical_key(candidate), "doi:10.48550/arxiv.2601.12345")

    def test_uses_normalized_title_author_year_when_ids_are_missing(self):
        candidate = PaperCandidate(
            title="Memory-Augmented LLM Agents: A Survey!",
            authors=["Jane Smith", "John Doe"],
            abstract="",
            source="openalex",
            source_id="missing",
            url="https://example.test/paper",
            published_date="2026-05-20",
        )

        self.assertEqual(
            canonical_key(candidate),
            "title:memory augmented llm agents a survey|author:jane smith|year:2026",
        )


if __name__ == "__main__":
    unittest.main()
