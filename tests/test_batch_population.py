"""Deterministic eligible-population construction, manifest and reconstruction. Offline."""
from dataclasses import replace
import json
from pathlib import Path
import sys
import tempfile
import unittest

from paper_scout.batch_population import (
    ELIGIBLE_RELEVANCE, MIN_TITLE_IDENTITY_LENGTH, TRACKS, build_population, identities,
    manifest_digest, population_manifest, repository_code_sha, verify_manifest,
    write_manifest,
)
from paper_scout.config import ScoutConfig
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.promotion_protocol import canonical_json
from paper_scout.batch_population import paper_identities
from paper_scout.site import _infer_arxiv_id_from_text
from paper_scout.site import _load_library_papers
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

    def write_config(self, root, tracks, papers=3, link_arxiv=None):
        """A real config the command can load, plus the per-track state overrides.

        The file carries no track id, so every track resolves against it, and each
        track's database is pointed somewhere separate through the environment. That
        is what lets a restricted build be tested against a real second track.
        """
        track_id = tracks[0]
        # A DOI outranks the arXiv id when the canonical key is derived, so a linked
        # paper is matched by the alias rather than by the identifier it is keyed on.
        first = candidate(1, doi="10.9999/paper.one", arxiv_id=link_arxiv) if link_arxiv else candidate(1)
        config, store, keys = self.track(root, track_id,
                                         [first, *(candidate(i) for i in range(2, papers + 1))])
        self.store, self.keys = store, keys
        self.env = {f"PAPER_SCOUT_{track.upper()}_STATE_PATH":
                    str(Path(root) / track / "state.sqlite3") for track in TRACKS}
        path = Path(root) / "config.yaml"
        path.write_text(
            f'track:\n  relevance_profile: "{config.relevance_profile}"\n'
            f'output:\n  digest_dir: "{config.digest_dir}"\n'
            f'  report_dir: "{config.report_dir}"\n  docs_dir: "{config.docs_dir}"\n'
            f'curation:\n  path: "{config.curation_path}"\n', encoding="utf-8")
        return path


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

    def test_a_reference_to_another_paper_is_not_an_identity(self):
        # A source record names other papers; the first arXiv id inside one is not
        # necessarily its own, and attributing it here would exclude an unrelated paper.
        cited = "https://arxiv.org/abs/2609.07777"
        self.assertIsNone(_infer_arxiv_id_from_text("no identifier here"))
        self.assertEqual(_infer_arxiv_id_from_text(cited), "2609.07777")
        found = identities("openalex:W1", title="A Record That Cites Other Work",
                           openalex_id="W1", url="https://example.test/landing")
        self.assertEqual([i for i in found if i.startswith("arxiv:")], [])
        self.assertEqual(set(found) & set(identities("arxiv:2609.07777")), set())

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

    def test_an_arxiv_id_only_in_the_raw_record_still_matches_a_candidate(self):
        # Neither side scans a raw record. The two sides still meet, because the site
        # loader picks one arXiv id out of the record into the paper's own field.
        with tempfile.TemporaryDirectory() as tmp:
            buried = replace(candidate(1), source="openalex", openalex_id="W7168439999",
                             raw={"locations": [{"landing_page_url": "https://arxiv.org/abs/2609.09999"}]})
            config, store, keys = self.track(tmp, "agent_memory", [buried, candidate(2)])
            papers = _load_library_papers(Path(config.sqlite_path))
            loaded = next(p for p in papers if p.canonical_id == keys[0])
            self.assertIsNone(buried.arxiv_id)
            self.assertEqual(loaded.arxiv_id, "2609.09999")
            self.assertIn("arxiv:2609.09999", paper_identities(loaded))
            self.assess(store, "arxiv:2609.09999")
            track = build_population({"agent_memory": config}, BUILD_TIME).track("agent_memory")
            excluded = next(e for e in track.excluded if e.canonical_id == keys[0])
            self.assertEqual(excluded.matched_identity, "arxiv:2609.09999")

    def test_a_curation_suppression_reaches_the_paper_s_other_identifiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            title = "Persistent Long-Term Memory for LLM Agents, A Curated Study"
            target = replace(candidate(1, title=title), doi="10.9999/paper.one",
                             arxiv_id="2609.09999")
            config, store, keys = self.track(tmp, "agent_memory", [target, candidate(2)])
            # The rule names the paper by title alone; the stored row supplies the rest.
            # An overrides rule keeps the paper in the ranking domain, where a curation
            # exclusion would have removed it before it could be a candidate at all.
            Path(config.curation_path).write_text(
                f'overrides:\n  - title: "{title}"\n    suppress_for_quality: true\n',
                encoding="utf-8")
            track = build_population({"agent_memory": config}, BUILD_TIME).track("agent_memory")
            excluded = next(e for e in track.excluded if e.canonical_id == keys[0])
            self.assertEqual(excluded.reason, "suppressed")
            self.assertEqual(excluded.source, "agent_memory:curation")
            self.assertIn(excluded.matched_identity, identities(
                keys[0], title=title, doi="10.9999/paper.one", arxiv_id="2609.09999"))
            self.assertEqual(len(track.eligible), 1)

    def test_an_explicitly_empty_exclusion_scope_is_not_widened(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, store, keys = self.track(tmp, "agent_memory", [candidate(1), candidate(2)])
            self.assess(store, keys[0])
            narrowed = build_population({"agent_memory": config}, BUILD_TIME,
                                        exclusion_configs={}).track("agent_memory")
            self.assertEqual(len(narrowed.eligible), 2)
            self.assertEqual(narrowed.excluded, ())
            default = build_population({"agent_memory": config}, BUILD_TIME).track("agent_memory")
            self.assertEqual(len(default.eligible), 1)

    def test_the_recorded_code_sha_does_not_follow_the_working_directory(self):
        import os
        here = repository_code_sha()
        self.assertRegex(here, r"^[0-9a-f]{40}$")
        cwd = os.getcwd()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                os.chdir(tmp)
                self.assertEqual(repository_code_sha(), here)
        finally:
            os.chdir(cwd)

    def test_a_cited_arxiv_id_in_an_assessed_row_does_not_exclude_that_paper(self):
        with tempfile.TemporaryDirectory() as tmp:
            # The assessed paper's record mentions a third paper's arXiv id. That third
            # paper is separately ranked and must stay eligible.
            assessed = candidate(1, doi="10.9999/paper.one", raw={
                "references": [{"externalIds": {"ArXiv": "2609.07777"}},
                               {"url": "https://arxiv.org/abs/2609.07777"}]})
            cited = candidate(2, title="The Separately Ranked Cited Manuscript",
                              arxiv_id="2609.07777")
            config, store, keys = self.track(tmp, "agent_memory", [assessed, cited])
            self.assess(store, keys[0])
            track = build_population({"agent_memory": config}, BUILD_TIME).track("agent_memory")
            self.assertEqual(keys[1], "arxiv:2609.07777")
            self.assertIn(keys[1], track.ordered_canonical_ids)
            self.assertEqual([e.canonical_id for e in track.excluded], [keys[0]])

    def test_a_track_without_a_database_is_recorded_rather_than_passed_over(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, store, keys = self.track(tmp, "agent_memory", [candidate(1), candidate(2)])
            absent = replace(config, track_id="deep_research", relevance_profile="deep_research",
                             sqlite_path=Path(tmp) / "deep_research" / "missing.sqlite3")
            self.assertFalse(absent.sqlite_path.exists())
            population = build_population({"agent_memory": config}, BUILD_TIME,
                                          exclusion_configs={"agent_memory": config,
                                                             "deep_research": absent})
            self.assertEqual(population.sources["exclusion_tracks_without_state"], ["deep_research"])
            self.assertEqual(sorted(population.sources["exclusion_tracks"]),
                             ["agent_memory", "deep_research"])
            self.assertEqual(len(population.track("agent_memory").eligible), 2)

    def test_verification_rejects_a_manifest_recorded_against_other_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            config, store, keys = self.track(tmp, "agent_memory", [candidate(1), candidate(2)])
            configs = {"agent_memory": config}
            manifest = population_manifest(build_population(configs, BUILD_TIME), "sha")
            moved = json.loads(canonical_json(manifest))
            moved["sources"]["tracks"]["agent_memory"]["state_path"] = "/elsewhere/state.sqlite3"
            result = verify_manifest(moved, configs)
            self.assertFalse(result.sources_match)
            self.assertFalse(result.reproduced)
            # The ordered identifiers still rebuild; only the recorded inputs diverge.
            self.assertTrue(result.tracks["agent_memory"]["ordered_ids_match"])

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


class CommandTests(PopulationFixture):
    def run_cli(self, *args, config=None):
        """Run the command the way an operator does, as a module entry point.

        `python3 -m paper_scout.cli` executes the module body top to bottom, so this
        also fixes the dispatch order: a handler defined after the entry-point guard
        would not be bound by the time the command dispatches to it.
        """
        import os
        import subprocess
        return subprocess.run(
            [sys.executable, "-m", "paper_scout.cli", *(["--config", str(config)] if config else []),
             "batch-population", *args],
            capture_output=True, text=True, cwd=Path(__file__).resolve().parents[1],
            env={**os.environ, **getattr(self, "env", {})})

    def test_the_command_builds_and_verifies_a_manifest_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.write_config(tmp, ["agent_memory"])
            manifest = Path(tmp) / "manifest.json"
            built = self.run_cli("--manifest", str(manifest), "--build-time", BUILD_TIME,
                                 "--population-track", "agent_memory", config=config)
            self.assertEqual(built.returncode, 0, built.stderr)
            self.assertIn("manifest_sha256=", built.stdout)
            self.assertIn("eligible=3", built.stdout)
            verified = self.run_cli("--manifest", str(manifest), "--verify", config=config)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            self.assertIn("reproduced=True", verified.stdout)
            self.assertIn("sources_match=True", verified.stdout)
            self.assertIn("ordered_ids_match=True", verified.stdout)
            # The same pinned time over the same state rebuilds the identical digest.
            again = Path(tmp) / "again.json"
            rebuilt = self.run_cli("--manifest", str(again), "--build-time", BUILD_TIME,
                                   "--population-track", "agent_memory", config=config)
            self.assertEqual(rebuilt.returncode, 0, rebuilt.stderr)
            self.assertEqual(json.loads(again.read_text(encoding="utf-8"))["manifest_sha256"],
                             json.loads(manifest.read_text(encoding="utf-8"))["manifest_sha256"])

    def test_verification_covers_the_manifest_s_tracks_not_the_command_line_s(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.write_config(tmp, ["agent_memory"])
            manifest = Path(tmp) / "manifest.json"
            self.run_cli("--manifest", str(manifest), "--build-time", BUILD_TIME,
                         "--population-track", "agent_memory", config=config)
            for narrowing in (["--population-track", "agent_memory"],
                              ["--population-track", "engram"]):
                rejected = self.run_cli("--manifest", str(manifest), "--verify", *narrowing,
                                        config=config)
                self.assertNotEqual(rejected.returncode, 0)
                self.assertIn("not used with --verify", rejected.stderr)
            stored = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(list(stored["sources"]["tracks"]), ["agent_memory"])
            self.assertEqual(sorted(stored["sources"]["exclusion_tracks"]), sorted(TRACKS))

    def test_verification_exits_non_zero_when_the_population_moved(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.write_config(tmp, ["agent_memory"])
            manifest = Path(tmp) / "manifest.json"
            self.run_cli("--manifest", str(manifest), "--build-time", BUILD_TIME,
                         "--population-track", "agent_memory", config=config)
            stored = json.loads(manifest.read_text(encoding="utf-8"))
            stored["tracks"]["agent_memory"]["ordered_canonical_ids"].pop()
            manifest.write_text(json.dumps(stored), encoding="utf-8")
            result = self.run_cli("--manifest", str(manifest), "--verify", config=config)
            self.assertEqual(result.returncode, 1)
            self.assertIn("reproduced=False", result.stdout)

    def test_a_restricted_build_still_excludes_another_track_s_assessment(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.write_config(tmp, ["agent_memory"], link_arxiv="2609.09999")
            memory_keys = self.keys
            # The same manuscript under a different canonical id and a different title,
            # discovered by a track that is not being built. The only shared handle is
            # an arXiv id, which the twin carries in its URL rather than its own field.
            twin = candidate(9, title="A Separately Titled Record Of The Same Manuscript",
                             source="openalex", openalex_id="W7168439999",
                             url="https://arxiv.org/abs/2609.09999")
            research, research_store, research_keys = self.track(
                tmp, "deep_research", [twin], profile="deep_research")
            self.assess(research_store, research_keys[0])
            result = self.run_cli("--manifest", str(Path(tmp) / "m.json"), "--build-time",
                                  BUILD_TIME, "--population-track", "agent_memory", config=config)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((Path(tmp) / "m.json").read_text(encoding="utf-8"))
            track = manifest["tracks"]["agent_memory"]
            self.assertEqual(list(manifest["tracks"]), ["agent_memory"])
            # Only the built track is in the manifest, but every track was scanned.
            self.assertEqual(sorted(manifest["sources"]["exclusion_tracks"]), sorted(TRACKS))
            self.assertNotIn(memory_keys[0], track["ordered_canonical_ids"])
            self.assertEqual(memory_keys[0], "doi:10.9999/paper.one")
            excluded = next(e for e in track["excluded"] if e["canonical_id"] == memory_keys[0])
            self.assertEqual(excluded["reason"], "prior_assessment")
            self.assertEqual(excluded["matched_identity"], "arxiv:2609.09999")
            self.assertTrue(excluded["source"].startswith("deep_research:"))

    def test_verification_reports_a_mismatch_when_pointed_at_other_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.write_config(tmp, ["agent_memory"])
            manifest = Path(tmp) / "manifest.json"
            self.run_cli("--manifest", str(manifest), "--build-time", BUILD_TIME,
                         "--population-track", "agent_memory", config=config)
            elsewhere = self.write_config(Path(tmp) / "other", ["agent_memory"], papers=4)
            result = self.run_cli("--manifest", str(manifest), "--verify", config=elsewhere)
            self.assertEqual(result.returncode, 1)
            self.assertIn("sources_match=False", result.stdout)
            self.assertIn("reproduced=False", result.stdout)

    def test_building_requires_a_pinned_build_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.write_config(tmp, ["agent_memory"])
            result = self.run_cli("--manifest", str(Path(tmp) / "m.json"),
                                  "--population-track", "agent_memory", config=config)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--build-time is required", result.stderr)
            self.assertFalse((Path(tmp) / "m.json").exists())

    def test_a_roster_built_manifest_round_trips_through_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = self.write_config(tmp, ["agent_memory"])
            roster = Path(tmp) / "roster.json"
            roster.write_text(json.dumps({"tracks": {"agent_memory": [
                {"canonical_id": self.keys[0]}]}}), encoding="utf-8")
            manifest = Path(tmp) / "manifest.json"
            built = self.run_cli("--manifest", str(manifest), "--build-time", BUILD_TIME,
                                 "--roster", str(roster), "--population-track", "agent_memory",
                                 config=config)
            self.assertEqual(built.returncode, 0, built.stderr)
            self.assertIn("eligible=2", built.stdout)
            stored = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(len(stored["sources"]["frozen_rosters"]), 1)
            self.assertNotIn(self.keys[0], stored["tracks"]["agent_memory"]["ordered_canonical_ids"])
            # Verification rereads the roster the manifest records rather than any
            # roster the caller supplies, so the population rebuilds identically.
            verified = self.run_cli("--manifest", str(manifest), "--verify", config=config)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            self.assertIn("reproduced=True", verified.stdout)
            rejected = self.run_cli("--manifest", str(manifest), "--verify", "--roster",
                                    str(roster), config=config)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("not used with --verify", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
