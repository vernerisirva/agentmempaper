"""Deterministic eligible-population construction, manifest and reconstruction. Offline."""
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest

from paper_scout.batch_population import (
    ELIGIBLE_RELEVANCE, MIN_TITLE_IDENTITY_LENGTH, build_population, identities,
    manifest_digest, population_manifest, repository_code_sha, verify_manifest,
    write_manifest,
)
from paper_scout.config import ScoutConfig
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.promotion_protocol import canonical_json
from paper_scout.state import PaperStore

DIGEST = """# Paper Scout Digest - 2026-09-18

## Run Summary

- **Run ID:** 1
- **Candidates fetched:** 0
- **New unique papers:** 0
- **Relevant:** 0
- **Maybe relevant:** 0
- **Irrelevant:** 0
- **Source summary:** arxiv: 0

## Highly Relevant

## Maybe Relevant
"""
BUILD_TIME = "2026-09-18T12:00:00"


def candidate(index, **kwargs):
    """A distinctly titled, plainly on-topic paper so rule refresh keeps it relevant."""
    title = kwargs.pop("title", f"Persistent Long-Term Memory for LLM Agents, Study {index}")
    return PaperCandidate(title, ["Ada Lovelace"],
                          "A controlled study of persistent long-term memory for LLM agents.",
                          kwargs.pop("source", "arxiv"), f"source-{index}", **kwargs)


class PopulationFixture(unittest.TestCase):
    def track(self, root, track_id, candidates, profile=None):
        """One synthetic track: its own state, digest archive and empty curation."""
        base = Path(root) / track_id
        digests, reports = base / "digests", base / "reports"
        digests.mkdir(parents=True)
        reports.mkdir(parents=True)
        (digests / "2026-09-18.md").write_text(DIGEST, encoding="utf-8")
        curation = base / "curation.yaml"
        curation.write_text("pinned:\noverrides:\nexcluded:\n", encoding="utf-8")
        store = PaperStore(base / "state.sqlite3")
        run_id = store.start_run(7)
        keys = []
        for item in candidates:
            keys.append(store.upsert_paper(item, ClassificationResult(95, "relevant", "Synthetic match")))
        store.finish_run(run_id, fetched_count=len(candidates), new_count=len(candidates),
                         notified_count=0)
        config = ScoutConfig(terms=["agent memory"], track_id=track_id,
                             relevance_profile=profile or track_id,
                             sqlite_path=base / "state.sqlite3", digest_dir=digests,
                             report_dir=reports, docs_dir=base / "docs", curation_path=curation)
        return config, store, keys


class IdentityTests(unittest.TestCase):
    def test_every_supported_alias_resolves_to_the_same_manuscript(self):
        canonical = "doi:10.48550/arxiv.2609.03727"
        found = identities(canonical, title="Proactive Service Agents: A Unified Decision Framework",
                           doi="https://doi.org/10.48550/arXiv.2609.03727",
                           arxiv_id="arXiv:2609.03727v2", openalex_id="https://openalex.org/W7168433647",
                           semantic_scholar_id=" 4f2b ", url="https://arxiv.org/pdf/2609.03727v2.pdf")
        for expected in ("canonical:doi:10.48550/arxiv.2609.03727",
                         "doi:10.48550/arxiv.2609.03727",
                         "arxiv:2609.03727",
                         "openalex:W7168433647",
                         "semantic_scholar:4f2b",
                         "title:proactive service agents a unified decision framework"):
            self.assertIn(expected, found)
        # The same manuscript reached by any single alias meets the full record.
        for partial in (identities("arxiv:2609.03727"),
                        identities("openalex:W7168433647", openalex_id="W7168433647"),
                        identities("other:1", url="https://arxiv.org/abs/2609.03727"),
                        identities("other:2", doi="10.48550/arXiv.2609.03727")):
            self.assertTrue(set(partial) & set(found), partial)

    def test_a_url_derived_arxiv_id_matches_a_stored_one(self):
        stored = identities("arxiv:2609.03727", arxiv_id="2609.03727")
        for url in ("https://arxiv.org/abs/2609.03727", "http://arxiv.org/pdf/2609.03727v3.pdf"):
            derived = identities("openalex:W1", url=url)
            self.assertIn("arxiv:2609.03727", derived)
            self.assertTrue(set(stored) & set(derived))

    def test_title_matching_stays_narrow(self):
        short = identities("a:1", title="Memory")
        self.assertFalse([i for i in short if i.startswith("title:")])
        self.assertLessEqual(len("memory"), MIN_TITLE_IDENTITY_LENGTH)
        # Only an exact normalized match counts: neither a prefix nor an extra word does.
        base = identities("a:1", title="Persistent Memory for LLM Agents")
        for other, overlap in [("persistent memory for llm agents", True),
                               ("Persistent  memory, for LLM agents!", True),
                               ("Persistent Memory for LLM Agents II", False),
                               ("Persistent Memory for LLM", False)]:
            found = identities("b:2", title=other)
            titles = {i for i in found if i.startswith("title:")}
            self.assertEqual(bool(titles & set(base)), overlap, other)

    def test_namespaces_keep_unrelated_fields_apart(self):
        # The same string in a DOI and in an OpenAlex id is not a match.
        left = identities("a:1", doi="10.1234/abc")
        right = identities("b:2", openalex_id="10.1234/abc")
        self.assertEqual(set(left) & set(right), set())


class PopulationTests(PopulationFixture):
    def test_manifest_round_trips_with_identical_ordered_ids_and_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, store, keys = self.track(tmp, "agent_memory",
                                             [candidate(i) for i in range(1, 6)])
            configs = {"agent_memory": config}
            population = build_population(configs, BUILD_TIME)
            manifest = population_manifest(population, repository_code_sha(Path(tmp)))
            path = write_manifest(Path(tmp) / "manifest.json", manifest)
            stored = json.loads(path.read_text(encoding="utf-8"))

            rebuilt = build_population(configs, BUILD_TIME)
            rebuilt_manifest = population_manifest(rebuilt, "a-different-commit")
            track, rebuilt_track = population.track("agent_memory"), rebuilt.track("agent_memory")

            self.assertEqual(len(track.eligible), 5)
            self.assertEqual(track.ordered_canonical_ids, rebuilt_track.ordered_canonical_ids)
            self.assertEqual(track.population_sha256, rebuilt_track.population_sha256)
            self.assertEqual(stored["manifest_sha256"], rebuilt_manifest["manifest_sha256"])
            self.assertEqual(manifest_digest(stored), stored["manifest_sha256"])
            # The ordered identifiers are in the manifest, not only their digest.
            self.assertEqual(stored["tracks"]["agent_memory"]["ordered_canonical_ids"],
                             list(track.ordered_canonical_ids))
            self.assertEqual([c["canonical_id"] for c in stored["tracks"]["agent_memory"]["eligible"]],
                             list(track.ordered_canonical_ids))
            verification = verify_manifest(stored, configs)
            self.assertTrue(verification.reproduced)
            self.assertTrue(verification.self_consistent)
            self.assertTrue(all(t["ordered_ids_match"] and t["population_sha256_match"]
                                for t in verification.tracks.values()))

    def test_verification_fails_when_the_stored_population_no_longer_rebuilds(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, store, keys = self.track(tmp, "agent_memory",
                                             [candidate(i) for i in range(1, 5)])
            configs = {"agent_memory": config}
            manifest = population_manifest(build_population(configs, BUILD_TIME), "sha")
            tampered = json.loads(canonical_json(manifest))
            tampered["tracks"]["agent_memory"]["ordered_canonical_ids"].pop()
            result = verify_manifest(tampered, configs)
            self.assertFalse(result.reproduced)
            self.assertFalse(result.self_consistent)
            self.assertFalse(result.tracks["agent_memory"]["ordered_ids_match"])
            self.assertEqual(len(result.tracks["agent_memory"]["unexpected"]), 1)
            # A digest that no longer covers the list it sits beside is caught too.
            digest_only = json.loads(canonical_json(manifest))
            digest_only["tracks"]["agent_memory"]["ordered_canonical_ids"] = []
            self.assertFalse(verify_manifest(digest_only, configs).reproduced)

    def assess(self, store, canonical_id):
        """Store one real assessment row keyed by the given canonical identifier."""
        from test_promotion_gate import ENV, Models, fixture
        from unittest.mock import patch
        from paper_scout.promotion_gate import assess_promotion
        target, _, text, seed = fixture(canonical_id)
        with patch.dict("os.environ", ENV, clear=True):
            assessment = assess_promotion(target, text, seed, "llm", http=Models())
        self.assertEqual(assessment.canonical_id, canonical_id)
        store.save_quality_assessment(assessment)

    def test_a_prior_assessment_excludes_the_paper_under_any_alias(self):
        # The assessment row is keyed by a different identifier than the ranked paper in
        # every case but the first, so each alias is what does the matching.
        # A DOI outranks every other identifier when the canonical key is derived, so
        # each case carries one and the alias under test is a genuinely separate handle.
        doi = {"doi": "10.9999/paper.one"}
        aliases = [
            ("canonical id and DOI", doi, "doi:10.9999/paper.one"),
            ("arXiv id", {**doi, "arxiv_id": "2609.09999"}, "arxiv:2609.09999"),
            ("OpenAlex id", {**doi, "openalex_id": "W7168439999"}, "openalex:W7168439999"),
            ("URL-derived arXiv id", {**doi, "url": "https://arxiv.org/abs/2609.09999"},
             "arxiv:2609.09999"),
        ]
        for label, fields, assessed_id in aliases:
            with self.subTest(alias=label), tempfile.TemporaryDirectory() as tmp:
                target = candidate(1, **fields)
                config, store, keys = self.track(
                    tmp, "agent_memory", [target, candidate(2), candidate(3)])
                self.assertEqual(keys[0], "doi:10.9999/paper.one")
                self.assess(store, assessed_id)
                track = build_population({"agent_memory": config}, BUILD_TIME).track("agent_memory")
                self.assertNotIn(keys[0], track.ordered_canonical_ids)
                self.assertEqual(len(track.eligible), 2)
                excluded = next(e for e in track.excluded if e.canonical_id == keys[0])
                self.assertEqual(excluded.reason, "prior_assessment")
                self.assertIn("paper_quality_assessments", excluded.source)
                self.assertIn(excluded.matched_identity,
                              identities(keys[0], title=target.title, **fields))
                self.assertIn(excluded.matched_identity, identities(assessed_id))
                if label != "canonical id and DOI":
                    self.assertNotEqual(assessed_id, keys[0])
                    self.assertFalse(excluded.matched_identity.startswith("canonical:"))

    def test_a_normalized_title_match_excludes_across_tracks(self):
        with tempfile.TemporaryDirectory() as tmp:
            title = "Persistent Long-Term Memory for LLM Agents, A Distinctive Study"
            # The two records share nothing but the title, punctuated differently.
            memory, memory_store, memory_keys = self.track(
                tmp, "agent_memory",
                [candidate(1, title=title, arxiv_id="2609.01111"), candidate(2)])
            research, research_store, research_keys = self.track(
                tmp, "deep_research",
                [candidate(3, title=title.replace(",", " --"), source="openalex",
                           openalex_id="W7168430000")], profile="deep_research")
            self.assertNotEqual(memory_keys[0], research_keys[0])
            self.assess(research_store, research_keys[0])
            configs = {"agent_memory": memory, "deep_research": research}
            track = build_population(configs, BUILD_TIME).track("agent_memory")
            excluded = next(e for e in track.excluded if e.canonical_id == memory_keys[0])
            self.assertEqual(excluded.reason, "prior_assessment")
            self.assertTrue(excluded.matched_identity.startswith("title:"))
            self.assertTrue(excluded.source.startswith("deep_research:"))

    def test_an_assessment_in_another_track_excludes_the_same_manuscript(self):
        with tempfile.TemporaryDirectory() as tmp:
            shared = candidate(1, arxiv_id="2609.09999", doi="10.48550/arXiv.2609.09999")
            # The same manuscript, discovered by the other track under its OpenAlex id.
            other_side = replace(shared, doi=None, arxiv_id=None,
                                 openalex_id="W7168439999", source="openalex",
                                 url="https://arxiv.org/abs/2609.09999")
            memory, memory_store, memory_keys = self.track(
                tmp, "agent_memory", [shared, candidate(2)])
            research, research_store, research_keys = self.track(
                tmp, "deep_research", [other_side], profile="deep_research")
            from test_promotion_gate import ENV, Models, fixture
            from unittest.mock import patch
            from paper_scout.promotion_gate import assess_promotion
            _, _, text, seed = fixture(research_keys[0])
            with patch.dict("os.environ", ENV, clear=True):
                research_store.save_quality_assessment(
                    assess_promotion(other_side, text, seed, "llm", http=Models()))
            configs = {"agent_memory": memory, "deep_research": research}
            track = build_population(configs, BUILD_TIME).track("agent_memory")
            self.assertNotIn(memory_keys[0], track.ordered_canonical_ids)
            excluded = next(e for e in track.excluded if e.canonical_id == memory_keys[0])
            self.assertEqual(excluded.reason, "prior_assessment")
            self.assertTrue(excluded.source.startswith("deep_research:"))

    def test_a_frozen_roster_and_a_suppression_exclude_with_their_own_reasons(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, store, keys = self.track(tmp, "agent_memory",
                                             [candidate(i) for i in range(1, 5)])
            roster = Path(tmp) / "roster.json"
            roster.write_text(json.dumps({"tracks": {"agent_memory": [
                {"canonical_id": keys[0], "rank": 1}]}}), encoding="utf-8")
            store.set_quality_suppression(keys[1], 0, "explicit suppression")
            track = build_population({"agent_memory": config}, BUILD_TIME, (roster,)).track("agent_memory")
            reasons = {e.canonical_id: e.reason for e in track.excluded}
            self.assertEqual(reasons[keys[0]], "frozen_roster")
            self.assertEqual(reasons[keys[1]], "suppressed")
            self.assertEqual(len(track.eligible), 2)
            self.assertNotIn(keys[0], track.ordered_canonical_ids)
            self.assertNotIn(keys[1], track.ordered_canonical_ids)

    def test_every_removed_candidate_is_accounted_for(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, store, keys = self.track(tmp, "agent_memory",
                                             [candidate(i) for i in range(1, 6)])
            store.set_quality_suppression(keys[0], 0, "explicit suppression")
            track = build_population({"agent_memory": config}, BUILD_TIME).track("agent_memory")
            self.assertEqual(track.ranked_count, len(track.eligible) + len(track.excluded))
            self.assertTrue(all(e.reason and e.matched_identity and e.source for e in track.excluded))
            self.assertEqual(sorted({*track.ordered_canonical_ids,
                                     *(e.canonical_id for e in track.excluded)}), sorted(keys))

    def test_the_population_is_built_from_the_ranking_domain_in_its_own_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, store, keys = self.track(tmp, "agent_memory",
                                             [candidate(i) for i in range(1, 6)])
            store.upsert_paper(candidate(9, title="An unrelated quantum chemistry benchmark"),
                               ClassificationResult(20, "maybe", "Weak topical match"))
            track = build_population({"agent_memory": config}, BUILD_TIME).track("agent_memory")
            # Only the frozen relevance level takes part, and ranks are contiguous over it.
            self.assertEqual([c.rank for c in track.eligible], list(range(1, len(track.eligible) + 1)))
            self.assertEqual(ELIGIBLE_RELEVANCE, "relevant")
            self.assertTrue(all(c.identities for c in track.eligible))


if __name__ == "__main__":
    unittest.main()
