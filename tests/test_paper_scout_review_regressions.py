from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from paper_scout.engram_evaluation import seed_fixtures
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.relevance import classify_with_rules
from paper_scout.site import _library_paper_to_json, _load_library_papers, _merge_two_papers
from paper_scout.state import PaperStore


class IndependentReviewRegressions(unittest.TestCase):
    def classify(self, title, abstract):
        return classify_with_rules(PaperCandidate(title, [], abstract, "fixture", title), "engram").decision

    def test_result_uncertainty_and_indirect_addressing_remain_relevant(self):
        for conclusion in (
            "The gains are uncertain across seeds, and we report unsuccessful replications.",
            "Indirect addressing reduces reader throughput without improving reasoning.",
            "A baseline without conditional memory matches its reasoning accuracy.",
        ):
            with self.subTest(conclusion=conclusion):
                self.assertEqual(self.classify(
                    "Engram conditional-memory replication",
                    "We evaluate Engram conditional memory and its lookup reader inside transformer backbones. " + conclusion,
                ), "relevant")

    def test_named_rag_memory_banks_do_not_establish_model_integration(self):
        for description in (
            "an external memory bank for vector lookup",
            "a learned memory bank for document lookup",
        ):
            with self.subTest(description=description):
                self.assertEqual(self.classify(
                    "Engram for enterprise retrieval",
                    "We introduce Engram, a language model RAG application using " + description
                    + ". Retrieved text is inserted into the prompt. The model has no internal memory module.",
                ), "irrelevant")

    def test_lookup_tables_with_internal_readers_remain_relevant(self):
        self.assertEqual(self.classify(
            "Learned lookup tables for language models",
            "We introduce learned lookup tables attached to transformer backbones through a trained reader. "
            "Unlike prompt-based RAG, these values modify hidden states inside the model.",
        ), "relevant")

    def test_source_update_cannot_replace_an_arxiv_revision(self):
        paper = seed_fixtures()[0]
        classification = ClassificationResult(92, "relevant", "Synthetic provenance regression")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.sqlite3"
            store = PaperStore(path)
            key = store.upsert_paper(paper, classification)
            initial = _load_library_papers(path)[0]
            indexed = replace(paper, source="openalex", source_id="W-probe", openalex_id="W-probe", updated_date="2026-09-05")
            self.assertEqual(store.upsert_paper(indexed, classification), key)
            current = _load_library_papers(path)[0]
            self.assertEqual(current.first_seen_at, initial.first_seen_at)
            self.assertEqual(_library_paper_to_json(current)["latest_revision_date"], paper.updated_date)
            self.assertEqual(store.paper_count(), 1)

    def test_out_of_order_arxiv_versions_keep_latest_revision(self):
        paper = seed_fixtures()[0]
        classification = ClassificationResult(92, "relevant", "Synthetic revision regression")
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / "state.sqlite3")
            key = store.upsert_paper(replace(paper, arxiv_id=paper.arxiv_id + "v3", updated_date="2026-09-01"), classification)
            self.assertEqual(store.upsert_paper(replace(paper, arxiv_id=paper.arxiv_id + "v1", updated_date="2026-01-12"), classification), key)
            self.assertEqual(store.candidate_by_key(key).updated_date, "2026-09-01")

    def test_source_change_carries_its_own_update_date(self):
        paper = seed_fixtures()[0]
        classification = ClassificationResult(92, "relevant", "Synthetic source switch regression")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.sqlite3"
            store = PaperStore(path)
            year_only = replace(paper, source="semantic_scholar", published_date="2026",
                                publication_date_precision="year", publication_date_source="semantic_scholar",
                                updated_date="2026-09-05")
            key = store.upsert_paper(year_only, classification)
            self.assertEqual(store.upsert_paper(paper, classification), key)
            output = _library_paper_to_json(_load_library_papers(path)[0])
            self.assertEqual(output["source"], "arxiv")
            self.assertEqual(output["latest_revision_date"], paper.updated_date)

    def test_rendered_duplicate_merge_keeps_update_provenance(self):
        paper = seed_fixtures()[0]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.sqlite3"
            PaperStore(path).upsert_paper(paper, ClassificationResult(92, "relevant", "Synthetic merge regression"))
            arxiv = _load_library_papers(path)[0]
            indexed = replace(arxiv, source="openalex", source_id="W-probe", score=80, updated_date="2026-09-05")
            for left, right in ((arxiv, indexed), (indexed, arxiv)):
                merged = _merge_two_papers(left, right)
                self.assertEqual(_library_paper_to_json(merged)["latest_revision_date"], paper.updated_date)
            newer = replace(arxiv, updated_date="2026-09-01")
            self.assertEqual(_merge_two_papers(arxiv, newer).updated_date, "2026-09-01")


if __name__ == "__main__":
    unittest.main()
