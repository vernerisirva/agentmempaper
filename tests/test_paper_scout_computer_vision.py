"""The computer vision track: registration, screening, state, site and operation.

Grouped by what could actually go wrong rather than by module. The three things that
would be expensive to get wrong are screening precision (a detection-heavy profile is
easy to overfit), track isolation (four tracks sharing one manuscript must not share a
decision), and the durable-state migration (a three-track snapshot must upgrade without
touching the tracks it does carry).

No test here issues a paid model call or reaches the network.
"""
from __future__ import annotations

from contextlib import redirect_stdout
from dataclasses import replace
import io
import json
from pathlib import Path
import sqlite3
import tarfile
import tempfile
import unittest

from paper_scout.batch_population import TRACKS
from paper_scout.config import TRACK_CONFIG_PATHS, TRACK_SITES, load_config, track_links
from paper_scout.discovery_evaluation import evaluate_discovery
from paper_scout.evaluation import evaluate_relevance_examples, relevance_fixture_examples
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.query_planner import plan_queries
from paper_scout.relevance import classify_with_rules, explain_rule_matches
from paper_scout.runtime_snapshot import (
    LEGACY_DATABASE_SETS, MANIFEST, STATE_PATHS, pack_snapshot, restore_snapshot,
)
from paper_scout.seeds import load_seed_manifest
from paper_scout.site import TOPIC_FILTERS, build_site
from paper_scout.state import PaperStore
from paper_scout.structured_cards import related_topics_for_paper, structured_card_for_paper

ROOT = Path(__file__).resolve().parents[1]
TRACK = "computer_vision"


def candidate(title: str, abstract: str, source_id: str = "cv-1") -> PaperCandidate:
    return PaperCandidate(title=title, authors=["Fixture Author"], abstract=abstract,
                          source="fixture", source_id=source_id,
                          url="https://example.test/cv", published_date="2026-01-01")


class TrackRegistration(unittest.TestCase):
    def test_computer_vision_is_a_registered_track(self):
        self.assertIn(TRACK, TRACK_CONFIG_PATHS)
        self.assertIn(TRACK, TRACK_SITES)
        self.assertIn(TRACK, TRACKS)
        config = load_config(track_id=TRACK, env={})
        self.assertEqual(config.track_id, TRACK)
        self.assertEqual(config.relevance_profile, TRACK)
        self.assertEqual(config.title, "Computer Vision Paper Library")
        self.assertEqual(config.docs_dir, Path("docs/computer-vision"))
        self.assertEqual(config.sqlite_path, Path("data/computer_vision/paper_scout.sqlite3"))
        self.assertEqual(config.digest_dir, Path("digests/computer_vision"))
        self.assertEqual(config.curation_path, Path("config/curation/computer_vision.yaml"))
        self.assertTrue(config.quality.enabled)

    def test_the_default_track_is_still_agent_memory(self):
        """Adding a track must not change what an unqualified call resolves to."""
        default = load_config(env={})
        self.assertEqual(default.track_id, "agent_memory")
        self.assertEqual(default.sqlite_path, Path("data/paper_scout.sqlite3"))
        self.assertEqual(default.docs_dir, Path("docs"))
        self.assertEqual(classify_with_rules(candidate("Agent Memory Systems", "Persistent memory for LLM agents.")).decision,
                         classify_with_rules(candidate("Agent Memory Systems", "Persistent memory for LLM agents."),
                                             profile="agent_memory").decision)

    def test_state_and_output_paths_are_not_shared_with_another_track(self):
        paths = {track: load_config(track_id=track, env={}) for track in TRACK_CONFIG_PATHS}
        for attribute in ("sqlite_path", "digest_dir", "docs_dir", "report_dir", "curation_path"):
            values = [str(getattr(config, attribute)) for config in paths.values()]
            self.assertEqual(len(values), len(set(values)), f"{attribute} is shared between tracks")

    def test_every_track_can_navigate_to_every_other_track(self):
        for track in TRACK_CONFIG_PATHS:
            labels = {label for label, _ in track_links(track)}
            self.assertEqual(labels, {label for key, (label, _) in TRACK_SITES.items() if key != track})
            self.assertIn("Computer Vision", labels | {TRACK_SITES[track][0]})
        # Relative, and pointing at the published locations rather than at a build path.
        self.assertIn(("Computer Vision", "computer-vision/index.html"), track_links("agent_memory"))
        self.assertIn(("Agentic Memory", "../index.html"), track_links(TRACK))
        self.assertIn(("Engram", "../engram/index.html"), track_links(TRACK))


class RelevanceScreening(unittest.TestCase):
    def test_pinned_relevance_fixtures_all_land_where_they_are_pinned(self):
        report = evaluate_relevance_examples(relevance_fixture_examples(TRACK), profile=TRACK)
        self.assertEqual(report["decision_mismatches"], [])
        self.assertEqual(report["false_positives"], [])
        self.assertEqual(report["false_negatives"], [])
        self.assertEqual(report["precision"], 1.0)
        self.assertEqual(report["recall"], 1.0)

    def test_the_fixture_set_covers_positives_negatives_and_borderline_cases(self):
        expected = {example.expected_decision for example in relevance_fixture_examples(TRACK)}
        self.assertEqual(expected, {"relevant", "maybe", "irrelevant"})

    def test_a_paper_with_no_visual_subject_is_never_relevant(self):
        for title, abstract in [
            ("A Multi-Agent LLM Framework for Tool Use",
             "A multi-agent language model framework orchestrates tool calls for text tasks."),
            ("In-Memory Database Indexing",
             "Database memory indexing and GPU memory management improve transaction throughput."),
            ("Collaborative Filtering for Recommendation",
             "A recommender system ranks items using collaborative filtering."),
        ]:
            with self.subTest(title=title):
                result = classify_with_rules(candidate(title, abstract), profile=TRACK)
                self.assertEqual(result.decision, "irrelevant")

    def test_a_domain_application_is_held_at_review_until_it_claims_a_general_method(self):
        """The policy the track turns on: breadth of claim, not application area."""
        applied = candidate(
            "Automated Polyp Detection in Colonoscopy Video Using YOLOv8",
            "We apply a standard pre-trained YOLOv8 detector to a private colonoscopy dataset "
            "and report clinical screening accuracy for our hospital.")
        general = candidate(
            "A Scale-Aware Detection Head for Small Lesion Detection",
            "We propose a novel detection head for small-object detection. Although motivated by "
            "medical imaging, the module is plug-and-play and generalizes across detectors and "
            "datasets; ablations isolate its contribution.")
        self.assertEqual(classify_with_rules(applied, profile=TRACK).decision, "maybe")
        self.assertEqual(classify_with_rules(general, profile=TRACK).decision, "relevant")

    def test_competing_detector_families_are_in_scope_alongside_yolo(self):
        """The library must not become a single-family echo chamber."""
        for title, abstract in [
            ("Real-Time Detection Transformers with an Efficient Hybrid Encoder",
             "A query-based end-to-end object detection architecture evaluated on COCO."),
            ("Region Proposal Networks Revisited",
             "We revisit the two-stage detector and its region proposal network, with ablations across backbones."),
            ("Segment Anything at Scale",
             "A promptable segmentation foundation model evaluated across datasets."),
        ]:
            with self.subTest(title=title):
                self.assertEqual(classify_with_rules(candidate(title, abstract), profile=TRACK).decision,
                                 "relevant")

    def test_yolo_papers_are_tagged_for_the_dashboard_filter(self):
        result = classify_with_rules(
            candidate("An Anchor-Free Detector in the YOLO Lineage",
                      "A real-time one-stage object detector evaluated on COCO with ablations across scales."),
            profile=TRACK)
        self.assertIn("yolo", result.tags)
        self.assertIn("object-detection", result.tags)
        # Every tag offered as a dashboard filter must be a tag the screen can produce,
        # or the control would show a topic that selects nothing.
        producible = set(explain_rule_matches(
            candidate("YOLO and DETR for semantic segmentation, multi-object tracking and pose estimation",
                      "A vision transformer visual backbone for visual representation learning and "
                      "vision-language tasks, with 3D reconstruction, depth estimation and "
                      "real-time object detection on an edge device."),
            profile=TRACK)["include_tags"])
        self.assertEqual({value for value, _ in TOPIC_FILTERS[TRACK]} - producible, set())

    def test_detection_metrics_are_recognized_without_being_conflated(self):
        """AP50 and mAP50-95 are different numbers; FPS and latency are different measures.

        The screen may recognize the vocabulary, because that is how detection papers are
        found. What it must not do is treat one as the other, so the two metric names and
        the two timing names are checked for separate patterns rather than a shared one.
        """
        from paper_scout.relevance import COMPUTER_VISION_INCLUDE_PATTERNS
        metrics = COMPUTER_VISION_INCLUDE_PATTERNS["metrics"]
        efficiency = COMPUTER_VISION_INCLUDE_PATTERNS["efficient-vision"]
        matched = lambda patterns, text: {p for p in patterns if __import__("re").search(p, text, __import__("re").I)}
        self.assertNotEqual(matched(metrics, "we report ap50 on coco"),
                            matched(metrics, "we report map50-95 on coco"))
        self.assertNotEqual(matched(efficiency, "the detector reaches 120 fps"),
                            matched(efficiency, "the detector has 8 ms inference latency"))

    def test_contrasting_with_text_only_models_does_not_exclude_a_vision_paper(self):
        """A vision-language paper writes "unlike text-only models, we ..." routinely.

        Treated as a hard negation this excluded a real open-vocabulary detection paper,
        so the phrase is an exclude signal that a high-confidence vision hit overrides.
        """
        result = classify_with_rules(
            candidate("Grounding Visual Detection in Vision-Language Models",
                      "Unlike text-only language models, our vision-language model performs "
                      "open-vocabulary object detection, and we evaluate visual grounding on "
                      "COCO with ablations that generalize across backbones."),
            profile=TRACK)
        self.assertEqual(result.decision, "relevant")
        # A paper that really is text-only still has no visual subject to gate on.
        self.assertEqual(classify_with_rules(
            candidate("Instruction Tuning for Text-Only Language Models",
                      "We study text-only instruction tuning for large language models."),
            profile=TRACK).decision, "irrelevant")

    def test_no_reported_number_earns_relevance_on_its_own(self):
        """A benchmark gain is not a contribution, and no threshold is encoded anywhere."""
        result = classify_with_rules(
            candidate("Improved Numbers", "We improve ap50 by 0.4 points and reach 250 fps."),
            profile=TRACK)
        self.assertNotEqual(result.decision, "relevant")

    def test_other_track_profiles_are_unchanged(self):
        for profile in ("agent_memory", "deep_research", "engram"):
            with self.subTest(profile=profile):
                report = evaluate_relevance_examples(relevance_fixture_examples(profile), profile=profile)
                self.assertEqual(report["decision_mismatches"], [])
                self.assertEqual(report["precision"], 1.0)
                self.assertEqual(report["recall"], 1.0)


class DiscoveryPlan(unittest.TestCase):
    def test_query_budgets_are_bounded_and_include_the_category_sweep(self):
        config = load_config(track_id=TRACK, env={})
        planned = plan_queries(config)
        per_source = {}
        for query in planned:
            per_source.setdefault(query.source, []).append(query)
        for source, queries in per_source.items():
            self.assertLessEqual(len(queries), config.query_budgets[source],
                                 f"{source} planned more queries than its budget")
        self.assertLessEqual(len(planned), 14)
        sweeps = [q for q in planned if q.route == "category_sweep"]
        self.assertEqual(len(sweeps), 1, "the cs.CV sweep was displaced by a keyword query")
        self.assertEqual(sweeps[0].provider_query, "cat:cs.CV")
        self.assertEqual(config.arxiv_sweep.categories, ("cs.CV",))
        # Breadth comes from the sweep, not from a wider category list.
        self.assertNotIn("cs.LG", config.arxiv_sweep.categories)

    def test_detection_queries_are_present_without_crowding_out_the_field(self):
        planned = plan_queries(load_config(track_id=TRACK, env={}))
        text = " ".join(q.provider_query.lower() for q in planned)
        for term in ("yolo", "object", "detection", "vocabulary", "transformer", "segmentation",
                     "representation"):
            self.assertIn(term, text)

    def test_the_documented_slot_budget_matches_the_configured_queries(self):
        """The README's provider-slot arithmetic is used for rate-limit planning.

        It read "three normal daily runs use 38 logical search slots" until this track was
        added, which is the kind of number that silently stops describing reality. Pinned
        against the planner rather than against a literal, so the prose has to be corrected
        whenever a budget or a track changes.
        """
        planned = sum(len(plan_queries(load_config(track_id=track, env={})))
                      for track in TRACK_CONFIG_PATHS)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        words = {3: "three", 4: "four", 5: "five", 6: "six"}
        count = len(TRACK_CONFIG_PATHS)
        self.assertIn(f"{words.get(count, count)} normal daily runs", readme)
        self.assertIn(f"{planned} logical search slots", readme)

    def test_discovery_fixtures_are_all_reachable(self):
        report = evaluate_discovery(load_config(track_id=TRACK, env={}))
        self.assertEqual(report["missed"], [])
        self.assertEqual(report["recall"], 1.0)

    def test_every_registered_track_has_idempotency_fixtures(self):
        """The workflow validates idempotency per track, so a track without fixtures
        does not fail a check -- it raises a KeyError and takes the step down with it."""
        from paper_scout.validation import deterministic_candidates, validate_idempotency
        for track in TRACK_CONFIG_PATHS:
            with self.subTest(track=track):
                self.assertTrue(deterministic_candidates(track))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = validate_idempotency(base_dir=root, report_date="2026-09-21",
                                          report_dir=root / "reports",
                                          track_id=TRACK, relevance_profile=TRACK)
        self.assertTrue(report["passed"], report)
        self.assertEqual(report["first_digest_count"], 2)
        self.assertEqual(report["second_digest_count"], 0)
        self.assertTrue(report["same_paper_from_multiple_sources"])


class Seeds(unittest.TestCase):
    def manifest(self):
        config = load_config(ROOT / TRACK_CONFIG_PATHS[TRACK], env={})
        return load_seed_manifest(replace(config, seed_manifest=ROOT / config.seed_manifest))

    def test_the_seed_manifest_is_valid_bounded_and_detection_anchored(self):
        manifest = self.manifest()
        self.assertEqual(manifest["track"], TRACK)
        papers = manifest["papers"]
        self.assertTrue(papers)
        self.assertLessEqual(len(papers), 20)
        self.assertEqual(len({p["arxiv_id"] for p in papers}), len(papers))
        titles = " ".join(p["expected_title"].lower() for p in papers)
        for anchor in ("you only look once", "yolo9000", "faster r-cnn", "mask r-cnn",
                       "end-to-end object detection", "deformable detr", "swin transformer",
                       "segment anything"):
            self.assertIn(anchor, titles)

    def test_seed_ingestion_verifies_identity_and_is_idempotent(self):
        """Seeds take the ordinary ingestion path, and a mismatch is reported, not written.

        Offline: the fetcher is a stub. What is under test is the manifest contract --
        the arXiv id and the title both have to match the source record -- and that a
        second run issues no further lookups and adds no second copy.
        """
        from paper_scout.seeds import ingest_seeds
        manifest = self.manifest()
        first = manifest["papers"][0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = replace(load_config(ROOT / TRACK_CONFIG_PATHS[TRACK], env={}),
                           seed_manifest=ROOT / "config/seeds/computer_vision.json",
                           sqlite_path=root / "state.sqlite3", report_dir=root / "reports")
            calls: list[str] = []

            def fetch(arxiv_id=None, **_):
                calls.append(arxiv_id)
                title = first["expected_title"] if arxiv_id == first["arxiv_id"] else "A Different Paper"
                return PaperCandidate(title=title, authors=["Ada Lovelace"],
                                      abstract="A real-time one-stage object detector evaluated on COCO.",
                                      source="arxiv", source_id=arxiv_id, arxiv_id=arxiv_id,
                                      url=f"https://arxiv.org/abs/{arxiv_id}",
                                      published_date="2015-06-08", updated_date="2016-05-09",
                                      publication_date_precision="day")

            report = ingest_seeds(base, fetch=fetch)
            statuses = {item["arxiv_id"]: item["status"] for item in report["results"]}
            self.assertEqual(statuses[first["arxiv_id"]], "new")
            # Every other seed's title disagreed with the source, so none of them was written.
            self.assertEqual(set(report["unresolved"]), set(statuses) - {first["arxiv_id"]})
            self.assertEqual(PaperStore(base.sqlite_path).paper_count(), 1)

            calls.clear()
            again = ingest_seeds(base, fetch=fetch)
            self.assertEqual(PaperStore(base.sqlite_path).paper_count(), 1)
            self.assertEqual(next(i["status"] for i in again["results"]
                                  if i["arxiv_id"] == first["arxiv_id"]), "already_known")
            self.assertNotIn(first["arxiv_id"], calls, "a known seed issued another lookup")

    def test_every_seed_note_matches_by_title_as_well_as_identifier(self):
        """The canonical key depends on which provider resolved the record.

        An arXiv lookup keys the paper on `arxiv:<id>`; the OpenAlex DOI fallback keys the
        same paper on `doi:10.48550/arxiv.<id>`. Curation matches on canonical id *or*
        title, so a note keyed only on the identifier silently detaches whenever the
        fallback route is taken -- which is exactly what happened when arXiv throttled.
        """
        import yaml
        curation = yaml.safe_load((ROOT / "config/curation/computer_vision.yaml").read_text())
        overrides = curation["overrides"] or []
        titles = {paper["expected_title"] for paper in self.manifest()["papers"]}
        self.assertEqual(len(overrides), len(titles))
        for rule in overrides:
            self.assertIn("canonical_id", rule)
            self.assertIn(rule.get("title"), titles, rule.get("canonical_id"))

    def test_seeding_confers_no_library_admission(self):
        """A curation note marks an anchor; it must not fabricate a quality decision."""
        curation = (ROOT / "config/curation/computer_vision.yaml").read_text(encoding="utf-8")
        self.assertIn("Foundational anchor", curation)
        for forbidden in ("include_despite_quality", "quality_status", "suppress_for_quality"):
            self.assertNotIn(forbidden, curation)


class TrackIsolation(unittest.TestCase):
    def test_one_manuscript_in_two_tracks_keeps_two_independent_records(self):
        """Overlap is expected; shared decisions, review state or first_seen are not."""
        paper = candidate(
            "Visual Memory for Embodied Agents",
            "A persistent memory system for LLM agents that also performs object detection on camera frames.")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stores, keys = {}, {}
            for track in ("agent_memory", TRACK):
                store = PaperStore(root / track / "state.sqlite3")
                classification = classify_with_rules(paper, profile=track)
                keys[track] = store.upsert_paper(paper, classification)
                stores[track] = store
            self.assertEqual(len(set(keys.values())), 1, "the same manuscript changed identity")
            stores["agent_memory"].mark_notified([keys["agent_memory"]], "2026-09-21")
            self.assertEqual(stores[TRACK].get_notified_for_date("2026-09-21"), [])
            self.assertEqual([record.canonical_key for record
                              in stores["agent_memory"].get_notified_for_date("2026-09-21")],
                             [keys["agent_memory"]])

    def test_each_track_screens_the_same_paper_under_its_own_rules(self):
        paper = candidate("Real-Time Object Detection on Edge Devices",
                          "A one-stage object detector with an anchor-free head, evaluated on COCO.")
        decisions = {track: classify_with_rules(paper, profile=track).decision
                     for track in TRACK_CONFIG_PATHS}
        self.assertEqual(decisions[TRACK], "relevant")
        self.assertNotEqual(decisions["agent_memory"], "relevant")
        self.assertNotEqual(decisions["deep_research"], "relevant")


class StructuredCards(unittest.TestCase):
    class Paper:
        def __init__(self, title, abstract, tags, decision="relevant"):
            self.title, self.abstract_summary, self.tags, self.decision = title, abstract, tags, decision
            self.reason = ""
            self.research_note = None
            self.quality_scope = None

    def test_the_relation_field_is_computer_vision_specific(self):
        card = structured_card_for_paper(
            self.Paper("An Anchor-Free YOLO Detector",
                       "A real-time one-stage object detector evaluated on COCO.", ["yolo", "object-detection"]),
            relevance_profile=TRACK)
        self.assertIn("YOLO", card["method_or_system_type"]["value"])
        self.assertIn("detection", card["relation_to_agentic_memory"]["value"].lower())
        self.assertIn("computer-vision", card["research_relevance"]["value"])

    def test_unsupported_fields_stay_unextracted_rather_than_invented(self):
        card = structured_card_for_paper(
            self.Paper("Semantic Segmentation with Transformers", "A segmentation decoder.", ["segmentation"]),
            relevance_profile=TRACK)
        self.assertEqual(card["key_contribution"]["value"], "Not extracted yet")
        self.assertEqual(card["key_contribution"]["provenance"], "not_extracted")

    def test_related_topics_do_not_borrow_another_track_s_vocabulary(self):
        topics = related_topics_for_paper(
            self.Paper("A Detection Benchmark on COCO", "A detection benchmark with robustness analysis.",
                       ["object-detection", "benchmark"]),
            relevance_profile=TRACK)
        self.assertIn("vision-benchmark", topics)
        self.assertNotIn("memory-benchmark", topics)
        self.assertNotIn("memory-security", topics)


class SiteBuild(unittest.TestCase):
    DIGEST = """# Paper Scout Digest - 2026-09-21

## Run Summary

- **Run ID:** 1
- **Candidates fetched:** 4
- **New unique papers:** 2
- **Relevant:** 1
- **Maybe relevant:** 1
- **Irrelevant:** 2
- **Source summary:** arxiv: 2, openalex: 2, semantic_scholar: 0

## Source Warnings

## Highly Relevant

### [An Anchor-Free One-Stage Detector](https://example.test/detector)

- **Authors:** Ada Lovelace
- **Date:** 2026-09-21
- **Source:** arxiv
- **Relevance:** relevant (96/100)
- **Reason:** Studies YOLO-family or real-time object detection.
- **Tags:** object-detection, yolo
- **Abstract summary:** A real-time one-stage object detector evaluated on COCO.

## Maybe Relevant

### [Polyp Detection with a Pre-Trained Detector](https://example.test/polyp)

- **Authors:** Grace Hopper
- **Date:** 2026-09-20
- **Source:** openalex
- **Relevance:** maybe (55/100)
- **Reason:** Review candidate: applies vision models in a specific domain.
- **Tags:** yolo
- **Abstract summary:** Applies a pre-trained detector to a clinical dataset.

## Irrelevant

"""

    def build(self, root: Path):
        digest_dir = root / "digests" / "computer_vision"
        report_dir = root / "reports" / "paper_scout" / "computer_vision"
        docs_dir = root / "docs" / "computer-vision"
        curation_path = root / "config" / "curation" / "computer_vision.yaml"
        digest_dir.mkdir(parents=True)
        report_dir.mkdir(parents=True)
        curation_path.parent.mkdir(parents=True)
        curation_path.write_text("pinned:\noverrides:\nexcluded:\ndate_overrides:\n", encoding="utf-8")
        (digest_dir / "2026-09-21.md").write_text(self.DIGEST, encoding="utf-8")
        config = load_config(ROOT / TRACK_CONFIG_PATHS[TRACK], env={})
        result = build_site(
            digest_dir=digest_dir, report_dir=report_dir, docs_dir=docs_dir,
            state_path=root / "data" / "computer_vision" / "missing.sqlite3",
            curation_path=curation_path, site_title=config.title, site_subtitle=config.subtitle,
            cross_track_label=None, cross_track_href=None, relevance_profile=TRACK,
            quality_config=config.quality, enrich_dates=False)
        return result, docs_dir

    def test_the_dashboard_builds_with_the_usual_pages_and_sidecars(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, docs_dir = self.build(Path(tmp))
            self.assertTrue(result.built, result.message)
            for name in ("index.html", "review.html", "latest.html", "archive.html", "about.html"):
                self.assertTrue((docs_dir / name).exists(), name)
            for name in ("papers.json", "latest.json", "paper-card.schema.json", "papers.csv", "papers.bib"):
                self.assertTrue((docs_dir / "data" / name).exists(), name)
            self.assertTrue(list((docs_dir / "papers").glob("*.html")))
            sidecars = list((docs_dir / "papers").glob("*.json"))
            self.assertTrue(sidecars)
            import jsonschema
            schema = json.loads((docs_dir / "data" / "paper-card.schema.json").read_text())
            validator = jsonschema.Draft202012Validator(schema)
            for path in sidecars:
                self.assertEqual(list(validator.iter_errors(json.loads(path.read_text()))), [])

    def test_the_page_carries_the_track_title_navigation_and_topic_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, docs_dir = self.build(Path(tmp))
            index = (docs_dir / "index.html").read_text(encoding="utf-8")
            review = (docs_dir / "review.html").read_text(encoding="utf-8")
            self.assertIn("Computer Vision Paper Library", index)
            for label, href in track_links(TRACK):
                self.assertIn(f'href="{href}"', index)
                self.assertIn(label, index)
            self.assertIn('id="topic-filter"', index)
            self.assertIn('value="yolo"', index)
            self.assertIn('value="object-detection"', index)
            self.assertIn("Research card", review)
            # A restrained reading surface: no raw diagnostics in the main list.
            self.assertNotIn("high_confidence_hits", index)

    def test_the_about_page_states_the_scope_and_its_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, docs_dir = self.build(Path(tmp))
            about = (docs_dir / "about.html").read_text(encoding="utf-8")
            for claim in (
                "YOLO",                      # why detection is emphasised
                "competing detector families",
                "segmentation",              # the broader field
                "AP50",                      # metrics are not interchangeable
                "not a claim of complete literature coverage",
                "Foundational anchor" if False else "Foundational papers",
            ):
                self.assertIn(claim, about)
            # Relevance and quality are separate, and prestige is not a criterion.
            self.assertIn("Relevance is topical only and says nothing about scientific quality.", about)
            self.assertIn("prestige are not quality criteria", about)
            self.assertNotIn("agentic-memory research", about)

    def test_only_relative_links_are_emitted(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, docs_dir = self.build(Path(tmp))
            for page in [*docs_dir.glob("*.html"), *(docs_dir / "papers").glob("*.html")]:
                for match in __import__("re").findall(r'href="([^"]+)"', page.read_text(encoding="utf-8")):
                    if match.startswith(("http://", "https://", "#", "mailto:")):
                        continue
                    self.assertFalse(match.startswith("/"), f"{page.name} -> {match}")

    def test_no_generated_page_contains_control_bytes(self):
        """A published page has to be text.

        Bounded full-text extraction emits NUL for glyphs pypdf cannot map -- mathematical
        symbols, mostly -- and those reach a page through the quality evidence excerpts. One
        committed detail page carried 42 of them: `file` reported "data", Git treated it as
        binary, and a browser may stop parsing at the first one. Sixteen already-published
        pages across all four tracks were affected.
        """
        import re
        control = re.compile(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]")
        with tempfile.TemporaryDirectory() as tmp:
            _, docs_dir = self.build(Path(tmp))
            for path in docs_dir.rglob("*"):
                if path.is_file():
                    self.assertEqual(control.findall(path.read_bytes()), [], path.name)
        # And every page this repository has already published.
        for base in (ROOT / "docs", ROOT / "digests", ROOT / "reports/paper_scout"):
            for path in base.rglob("*"):
                if path.is_file():
                    self.assertEqual(control.findall(path.read_bytes()), [],
                                     str(path.relative_to(ROOT)))

    def test_the_page_renderer_strips_control_characters_it_is_handed(self):
        """The strip sits at the single choke point every generated page passes through."""
        from paper_scout.site import _page, _strip_control_characters
        self.assertEqual(_strip_control_characters("a\x00b\x1fc"), "abc")
        # Tab, newline and carriage return are legitimate and must survive.
        self.assertEqual(_strip_control_characters("a\tb\nc\rd"), "a\tb\nc\rd")
        rendered = _page("Title", "<p>evidence\x00 with \x0bglyphs</p>")
        self.assertNotIn("\x00", rendered)
        self.assertIn("evidence with glyphs", rendered)

    def test_no_state_or_secret_shaped_value_reaches_the_generated_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, docs_dir = self.build(Path(tmp))
            for path in docs_dir.rglob("*"):
                if not path.is_file():
                    continue
                self.assertNotIn(".sqlite3", path.name)
                text = path.read_text(encoding="utf-8", errors="replace")
                for marker in ("GEMINI_API_KEY=", "OPENROUTER_API_KEY=", "PAPER_SCOUT_STATE_TOKEN="):
                    self.assertNotIn(marker, text)


class DurableState(unittest.TestCase):
    def make_state(self, root: Path, names=STATE_PATHS, seeded: bool = True):
        for index, name in enumerate(names):
            store = PaperStore(root / name)
            if seeded:
                paper = PaperCandidate(f"Track {index} paper", [], "Synthetic", "fixture", str(index))
                store.upsert_paper(paper, ClassificationResult(90, "relevant", "Synthetic"))
        return root

    def fingerprint(self, root: Path, names):
        import hashlib
        return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}

    def test_the_snapshot_carries_the_fourth_database(self):
        self.assertIn("data/computer_vision/paper_scout.sqlite3", STATE_PATHS)
        self.assertEqual(len(STATE_PATHS), len(TRACKS))
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            archive = Path(tmp) / "state.tar.gz"
            manifest = pack_snapshot(archive, root=source)
            self.assertEqual(list(manifest["databases"]), list(STATE_PATHS))
            target = Path(tmp) / "dst"
            target.mkdir()
            report: dict = {}
            self.assertEqual(restore_snapshot(archive, root=target, report=report), [])
            self.assertEqual(self.fingerprint(source, STATE_PATHS), self.fingerprint(target, STATE_PATHS))

    def three_track_archive(self, tmp: Path, source: Path, manifest: dict) -> Path:
        """Rewrite a four-track archive as the three-track one that predates this track."""
        three = list(STATE_PATHS[:3])
        older = {"version": 2, "schema": "paper-scout-state-snapshot",
                 "sha256": {name: manifest["sha256"][name] for name in three},
                 "databases": three,
                 "row_counts": {name: manifest["row_counts"][name] for name in three},
                 "created_at": manifest["created_at"], "source": manifest["source"]}
        encoded = json.dumps(older, sort_keys=True).encode()
        legacy = tmp / "three-track.tar.gz"
        with tarfile.open(tmp / "state.tar.gz", "r:gz") as src, tarfile.open(legacy, "w:gz") as dst:
            for member in src.getmembers():
                if member.name == MANIFEST:
                    member.size = len(encoded)
                    dst.addfile(member, io.BytesIO(encoded))
                elif member.name in three:
                    dst.addfile(member, src.extractfile(member))
        return legacy

    def test_a_three_track_snapshot_upgrades_without_touching_the_tracks_it_carries(self):
        self.assertIn(frozenset(STATE_PATHS[:3]), LEGACY_DATABASE_SETS)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            source = self.make_state(tmp / "src")
            manifest = pack_snapshot(tmp / "state.tar.gz", root=source)
            legacy = self.three_track_archive(tmp, source, manifest)
            target = tmp / "dst"
            target.mkdir()
            initialized = restore_snapshot(legacy, root=target)
            self.assertEqual(initialized, ["data/computer_vision/paper_scout.sqlite3"])
            self.assertEqual(self.fingerprint(source, STATE_PATHS[:3]),
                             self.fingerprint(target, STATE_PATHS[:3]))
            self.assertEqual(PaperStore(target / STATE_PATHS[3]).paper_count(), 0)

    def test_restoring_a_three_track_snapshot_again_never_resets_this_track(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            source = self.make_state(tmp / "src")
            manifest = pack_snapshot(tmp / "state.tar.gz", root=source)
            legacy = self.three_track_archive(tmp, source, manifest)
            target = tmp / "dst"
            target.mkdir()
            restore_snapshot(legacy, root=target)
            store = PaperStore(target / STATE_PATHS[3])
            store.upsert_paper(PaperCandidate("Kept", [], "Real history", "fixture", "keep"),
                               ClassificationResult(90, "relevant", "Real history"))
            before = self.fingerprint(target, STATE_PATHS[3:])
            self.assertEqual(restore_snapshot(legacy, root=target), [])
            self.assertEqual(self.fingerprint(target, STATE_PATHS[3:]), before)

    def test_restoring_a_legacy_snapshot_leaves_state_that_can_be_persisted(self):
        """The exact first-run-after-upgrade sequence: restore a three-track snapshot, pack.

        Whichever workflow runs first after this track merges will restore a snapshot that
        predates it and then persist. `pack_snapshot` verifies every path in STATE_PATHS, so
        a restore that did not create the new database would fail the persist step and lose
        the run's work. Pinned end to end rather than inferred from the two halves.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            source = self.make_state(tmp / "src")
            manifest = pack_snapshot(tmp / "state.tar.gz", root=source)
            legacy = self.three_track_archive(tmp, source, manifest)
            runner = tmp / "runner"
            runner.mkdir()
            self.assertEqual(restore_snapshot(legacy, root=runner),
                             ["data/computer_vision/paper_scout.sqlite3"])
            packed = pack_snapshot(tmp / "persist.tar.gz", root=runner)
            self.assertEqual(list(packed["databases"]), list(STATE_PATHS))

    def test_a_snapshot_missing_an_established_track_still_fails_closed(self):
        """Dropping engram while carrying this track is a partial archive, not an upgrade."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            source = self.make_state(tmp / "src")
            manifest = pack_snapshot(tmp / "state.tar.gz", root=source)
            keep = [STATE_PATHS[0], STATE_PATHS[1], STATE_PATHS[3]]
            broken = {"version": 2, "schema": "paper-scout-state-snapshot",
                      "sha256": {name: manifest["sha256"][name] for name in keep},
                      "databases": keep,
                      "row_counts": {name: manifest["row_counts"][name] for name in keep},
                      "created_at": manifest["created_at"], "source": manifest["source"]}
            encoded = json.dumps(broken, sort_keys=True).encode()
            partial = tmp / "partial.tar.gz"
            with tarfile.open(tmp / "state.tar.gz", "r:gz") as src, tarfile.open(partial, "w:gz") as dst:
                for member in src.getmembers():
                    if member.name == MANIFEST:
                        member.size = len(encoded)
                        dst.addfile(member, io.BytesIO(encoded))
                    elif member.name in keep:
                        dst.addfile(member, src.extractfile(member))
            target = tmp / "dst"
            target.mkdir()
            with self.assertRaises(ValueError):
                restore_snapshot(partial, root=target)
            self.assertFalse((target / STATE_PATHS[0]).exists())

    def test_a_corrupt_fourth_database_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            source = self.make_state(tmp / "src")
            pack_snapshot(tmp / "state.tar.gz", root=source)
            corrupt = tmp / "corrupt.tar.gz"
            with tarfile.open(tmp / "state.tar.gz", "r:gz") as src, tarfile.open(corrupt, "w:gz") as dst:
                for member in src.getmembers():
                    data = src.extractfile(member).read()
                    if member.name == STATE_PATHS[3]:
                        data = b"not a sqlite database" + data[21:]
                    member.size = len(data)
                    dst.addfile(member, io.BytesIO(data))
            target = self.make_state(tmp / "dst")
            before = self.fingerprint(target, STATE_PATHS)
            with self.assertRaises(ValueError):
                restore_snapshot(corrupt, root=target)
            self.assertEqual(self.fingerprint(target, STATE_PATHS), before)

    def test_the_transport_labels_the_fourth_database_by_its_track(self):
        import importlib.util
        path = ROOT / ".github/scripts/paper_scout_state.py"
        spec = importlib.util.spec_from_file_location("paper_scout_state", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.TRACK_FOR_STATE_PATH["data/computer_vision/paper_scout.sqlite3"],
                         TRACK)
        self.assertEqual(set(module.TRACK_FOR_STATE_PATH), set(STATE_PATHS))
        self.assertEqual(module._track_label("data/computer_vision/paper_scout.sqlite3"), TRACK)


class OperationalBounds(unittest.TestCase):
    def test_the_run_ceiling_is_one_slot_per_track_and_nothing_more(self):
        from paper_scout.operational_preflight import MAX_PAPERS_PER_RUN, MAX_PAPERS_PER_TRACK
        self.assertEqual(MAX_PAPERS_PER_TRACK, 1)
        self.assertEqual(MAX_PAPERS_PER_RUN, len(TRACKS))

    def test_an_unused_track_slot_is_never_lent_to_another_track(self):
        from paper_scout.operational_preflight import RunBudget
        budget = RunBudget()
        budget.record(TRACK, openrouter_usd=0.01)
        self.assertEqual(budget.may_assess(TRACK), (False, "track_paper_limit_reached"))
        self.assertTrue(budget.may_assess("agent_memory")[0])
        # Three tracks with nothing eligible do not hand their slots to this one.
        self.assertEqual(budget.total_assessed, 1)

    def test_the_cost_ceiling_was_not_raised_for_the_fourth_track(self):
        from paper_scout.operational_preflight import (
            DEFAULT_OPENROUTER_RUN_CEILING_USD, ESTIMATED_OPENROUTER_USD_PER_PAPER, RunBudget)
        self.assertEqual(DEFAULT_OPENROUTER_RUN_CEILING_USD, 0.30)
        budget = RunBudget()
        for index in range(budget.max_per_run):
            budget.reserve(f"track{index}")
            budget.record(f"track{index}", openrouter_usd=ESTIMATED_OPENROUTER_USD_PER_PAPER)
        self.assertLess(budget.openrouter_spend_usd, DEFAULT_OPENROUTER_RUN_CEILING_USD)

    def test_selection_nominates_this_track_under_the_shared_eligibility_rules(self):
        from paper_scout.operational_run import select_operational_candidates
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = PaperStore(root / "cv.sqlite3")
            store.upsert_paper(
                PaperCandidate("An Anchor-Free One-Stage Detector", ["Ada"],
                               "A real-time one-stage object detector evaluated on COCO.",
                               "arxiv", "2609.00001", arxiv_id="2609.00001",
                               published_date="2026-09-20"),
                ClassificationResult(96, "relevant", "Studies YOLO-family detection."))
            digest_dir = root / "digests"
            digest_dir.mkdir()
            (digest_dir / "2026-09-21.md").write_text(SiteBuild.DIGEST, encoding="utf-8")
            config = replace(load_config(ROOT / TRACK_CONFIG_PATHS[TRACK], env={}),
                             sqlite_path=root / "cv.sqlite3", digest_dir=digest_dir,
                             docs_dir=root / "docs", report_dir=root / "reports",
                             curation_path=root / "missing.yaml")
            selected, summaries = select_operational_candidates(
                {TRACK: config}, "2026-09-21T00:00:00",
                assessment_sources={TRACK: root / "cv.sqlite3"})
            self.assertEqual({c.track for c in selected}, {TRACK})
            self.assertGreaterEqual(summaries[TRACK].high_relevance, 1)
            # Nomination is bounded by the acquisition walk, not by the assessment budget.
            from paper_scout.operational_preflight import MAX_ACQUISITION_WALK
            self.assertLessEqual(len(selected), MAX_ACQUISITION_WALK)

    def test_an_already_assessed_paper_in_another_track_is_not_reassessed_here(self):
        """Cross-track overlap must not buy a manuscript a second scientific assessment."""
        from paper_scout.operational_run import select_operational_candidates
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = PaperStore(root / "cv.sqlite3")
            paper = PaperCandidate("An Anchor-Free One-Stage Detector", ["Ada"],
                                   "A real-time one-stage object detector evaluated on COCO.",
                                   "arxiv", "2609.00001", arxiv_id="2609.00001",
                                   published_date="2026-09-20")
            key = store.upsert_paper(paper, ClassificationResult(96, "relevant", "Studies detection."))
            # A completed scientific assessment stored by a *different* track, through the
            # real storage path rather than a hand-written row.
            other = PaperStore(root / "other.sqlite3")
            from test_promotion_gate import ENV, Models, fixture
            from unittest.mock import patch
            from paper_scout.promotion_gate import assess_promotion
            target, _, full_text, seed = fixture(key)
            with patch.dict("os.environ", ENV, clear=True):
                other.save_quality_assessment(
                    assess_promotion(target, full_text, seed, "llm", http=Models()))
            digest_dir = root / "digests"
            digest_dir.mkdir()
            (digest_dir / "2026-09-21.md").write_text(SiteBuild.DIGEST, encoding="utf-8")
            config = replace(load_config(ROOT / TRACK_CONFIG_PATHS[TRACK], env={}),
                             sqlite_path=root / "cv.sqlite3", digest_dir=digest_dir,
                             docs_dir=root / "docs", report_dir=root / "reports",
                             curation_path=root / "missing.yaml")
            selected, summaries = select_operational_candidates(
                {TRACK: config}, "2026-09-21T00:00:00",
                assessment_sources={TRACK: root / "cv.sqlite3", "other": root / "other.sqlite3"})
            self.assertNotIn(key, {c.canonical_id for c in selected})
            self.assertGreaterEqual(summaries[TRACK].already_assessed, 1)


class WorkflowIntegration(unittest.TestCase):
    def workflow(self, name: str) -> tuple[dict, str]:
        import yaml
        text = (ROOT / ".github/workflows" / name).read_text(encoding="utf-8")
        return yaml.load(text, Loader=yaml.BaseLoader), text

    def test_the_daily_workflow_discovers_seeds_evaluates_and_builds_this_track(self):
        workflow, _ = self.workflow("paper-scout.yml")
        commands = "\n".join(step.get("run", "") for step in workflow["jobs"]["scout"]["steps"])
        for command in (f"run --track {TRACK} --no-llm",
                        f"ingest-seeds --track {TRACK}",
                        f"build-site --track {TRACK}",
                        f"evaluate-relevance --track {TRACK}",
                        f"evaluate-quality --track {TRACK}",
                        f"evaluate-discovery --track {TRACK}",
                        f"validate-idempotency --track {TRACK}"):
            self.assertIn(command, commands)

    def test_the_daily_assessment_stage_covers_every_registered_track(self):
        """The assessment step names no track, so a new one must reach it automatically.

        Every other stage lists its tracks explicitly, which makes it easy to read the
        assessment step as having been missed. It has not: `operational-assess` accepts no
        --track flag and builds its configs from TRACKS. This pins both halves -- the
        command really does take no narrowing flag, and the selection it performs really
        does cover every registered track -- so a fifth track cannot be silently left out
        of the only path that can promote a paper into a main library.
        """
        workflow, _ = self.workflow("paper-scout.yml")
        assess = next(step for step in workflow["jobs"]["scout"]["steps"]
                      if step["name"] == "Bounded scientific assessment")
        self.assertIn("operational-assess", assess["run"])
        self.assertNotIn("--track", assess["run"],
                         "a --track flag here would narrow the daily assessment to one track")

        from paper_scout.operational_run import select_operational_candidates
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            configs, sources = {}, {}
            for track in TRACKS:
                digest_dir = root / track / "digests"
                digest_dir.mkdir(parents=True)
                (digest_dir / "2026-09-21.md").write_text(SiteBuild.DIGEST, encoding="utf-8")
                state = root / track / "state.sqlite3"
                PaperStore(state)
                configs[track] = replace(load_config(ROOT / TRACK_CONFIG_PATHS[track], env={}),
                                         sqlite_path=state, digest_dir=digest_dir,
                                         docs_dir=root / track / "docs",
                                         report_dir=root / track / "reports",
                                         curation_path=root / "missing.yaml")
                sources[track] = state
            _, summaries = select_operational_candidates(
                configs, "2026-09-21T00:00:00", assessment_sources=sources)
        self.assertEqual(set(summaries), set(TRACKS))

    def test_an_unresolvable_seed_cannot_cost_the_run_its_other_work(self):
        """Run 35594457409: two seeds failed and the whole daily run was lost.

        `ingest-seeds` exits 1 when an identifier does not resolve, which is right for a
        manual run. In the scheduled workflow that exit aborts the discovery step under
        `set -e`, so assessment, the site build and -- worst -- the state persist were all
        skipped, for every track, because of two papers. A seed can be unresolvable for
        reasons this repository does not control: on that run arXiv refused one lookup and
        OpenAlex resolved the other identifier to an entirely different paper, which the
        identity check correctly refused rather than ingesting the wrong manuscript.

        Every scheduled bootstrap therefore passes --allow-unresolved, which reports loudly
        and exits 0. Pinned for both workflows and every track, not just this one.
        """
        for name in ("paper-scout.yml", "paper-scout-backfill.yml"):
            workflow, _ = self.workflow(name)
            job = next(iter(workflow["jobs"].values()))
            for step in job["steps"]:
                for line in (step.get("run") or "").splitlines():
                    if "ingest-seeds" in line and not line.strip().startswith("#"):
                        self.assertIn("--allow-unresolved", line,
                                      f"{name}: a failed bootstrap would abort the run: {line.strip()}")

    def test_the_bootstrap_reports_unresolved_seeds_either_way(self):
        """The flag changes the exit code, never what is written or reported."""
        from paper_scout.seeds import ingest_seeds
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = replace(load_config(ROOT / TRACK_CONFIG_PATHS[TRACK], env={}),
                             seed_manifest=ROOT / "config/seeds/computer_vision.json",
                             sqlite_path=root / "state.sqlite3", report_dir=root / "reports")

            def fetch(arxiv_id=None, **_):
                # Third-party metadata resolving the right id to the wrong paper: exactly
                # what OpenAlex returned for Segment Anything on that run.
                return PaperCandidate(title="A Completely Different Paper", authors=["Ada"],
                                      abstract="Unrelated.", source="openalex",
                                      source_id=arxiv_id, arxiv_id=arxiv_id,
                                      url="https://example.test/x", published_date="2023-04-05",
                                      updated_date="2023-04-05", publication_date_precision="day")

            report = ingest_seeds(config, fetch=fetch)
            self.assertEqual(len(report["unresolved"]), len(report["results"]))
            self.assertEqual(PaperStore(config.sqlite_path).paper_count(), 0,
                             "a title mismatch must never write the wrong manuscript")
            for item in report["results"]:
                self.assertIn("does not match the manifest", item["error"])

    def test_the_bootstrap_cli_exit_code_depends_only_on_the_flag(self):
        """The branch the outage fix turns on, exercised through the CLI itself.

        The workflow wiring and the seeds layer are pinned elsewhere; this covers the exit
        code and the annotation, which is what actually decided whether run 35594457409
        kept or lost its work. No network: the fetch is replaced, and the unresolved path
        is reached by a title that disagrees with the manifest.
        """
        from unittest.mock import patch
        from paper_scout.cli import main

        def unresolvable(arxiv_id=None, **_):
            return PaperCandidate(title="A Completely Different Paper", authors=["Ada"],
                                  abstract="Unrelated.", source="openalex", source_id=arxiv_id,
                                  arxiv_id=arxiv_id, url="https://example.test/x",
                                  published_date="2023-04-05", updated_date="2023-04-05",
                                  publication_date_precision="day")

        for flag, expected_exit in (([], 1), (["--allow-unresolved"], 0)):
            with self.subTest(flag=flag or "default"), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                config = replace(load_config(ROOT / TRACK_CONFIG_PATHS[TRACK], env={}),
                                 seed_manifest=ROOT / "config/seeds/computer_vision.json",
                                 sqlite_path=root / "state.sqlite3", report_dir=root / "reports")
                stdout = io.StringIO()
                with patch("paper_scout.cli.load_config", return_value=config), \
                        patch("paper_scout.seeds.fetch_direct_paper", unresolvable), \
                        redirect_stdout(stdout), patch("sys.stderr", new=io.StringIO()) as stderr:
                    code = main(["ingest-seeds", "--track", TRACK, *flag])
                self.assertEqual(code, expected_exit)
                reported = stdout.getvalue() + stderr.getvalue()
                self.assertIn("seed bootstrap left unresolved IDs", reported)
                self.assertIn("::error::", reported, "an unresolved seed must stay loud")
                # Nothing is written on either path.
                self.assertEqual(PaperStore(config.sqlite_path).paper_count(), 0)

    def test_the_unresolved_annotation_cannot_emit_extra_workflow_commands(self):
        """A workflow annotation is line-oriented and identifiers are not shape-constrained.

        normalize_arxiv_id strips prefixes and version suffixes but passes anything else
        through, newlines included. The manifest is repo-controlled so this is not an
        external input, but a malformed entry would otherwise inject workflow commands.
        """
        from unittest.mock import patch
        from paper_scout.cli import main
        hostile = "2304.02643\n::set-output name=pwned::yes"
        manifest = {"track": TRACK,
                    "papers": [{"arxiv_id": hostile, "expected_title": "Segment Anything"}]}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_path = root / "seeds.json"
            seed_path.write_text(json.dumps(manifest), encoding="utf-8")
            config = replace(load_config(ROOT / TRACK_CONFIG_PATHS[TRACK], env={}),
                             seed_manifest=seed_path, sqlite_path=root / "state.sqlite3",
                             report_dir=root / "reports")
            stdout = io.StringIO()
            with patch("paper_scout.cli.load_config", return_value=config), \
                    patch("paper_scout.seeds.fetch_direct_paper",
                          lambda **_: (_ for _ in ()).throw(ValueError("unreachable"))), \
                    redirect_stdout(stdout), patch("sys.stderr", new=io.StringIO()):
                main(["ingest-seeds", "--track", TRACK, "--allow-unresolved"])
        printed = stdout.getvalue()
        annotation = next(line for line in printed.splitlines() if line.startswith("::error::"))
        # A workflow command is only interpreted when it begins a line, so the property that
        # matters is that the injected text cannot start one -- not that it is absent. The
        # identifier is still reported, which is the point of the annotation.
        self.assertNotIn("\n", annotation)
        self.assertIn("pwned::yes", annotation, "the identifier is still reported")
        self.assertEqual([line for line in printed.splitlines()
                          if line.lstrip().startswith("::set-output")], [])
        self.assertEqual(len([line for line in printed.splitlines()
                              if line.startswith("::")]), 1, printed)

    def test_every_state_path_is_checkpointed_before_it_is_persisted(self):
        for name in ("paper-scout.yml", "paper-scout-backfill.yml"):
            workflow, _ = self.workflow(name)
            job = next(iter(workflow["jobs"].values()))
            commands = "\n".join(step.get("run", "") for step in job["steps"])
            for path in STATE_PATHS:
                self.assertIn(path, commands, f"{name} does not checkpoint {path}")

    def test_the_site_check_flags_control_bytes_instead_of_silently_decoding_them(self):
        """The guard itself, not just its current result.

        Every generated file is clean today, so the assertion that none contains control
        bytes would pass even if the check were broken. This feeds it a corrupt file.
        """
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "check_paper_scout_site", ROOT / ".github/scripts/check_paper_scout_site.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "digests").mkdir(parents=True)
            (root / "reports/paper_scout").mkdir(parents=True)
            (root / "docs").mkdir(parents=True)
            (root / "digests" / "corrupt.md").write_bytes(b"a NUL \x00 and a \x0b here\n")
            (root / "digests" / "clean.md").write_bytes(b"tabs\tand\nnewlines\r\nare fine\n")
            errors = module.validate_site(root)
            flagged = [e for e in errors if "control bytes" in e]
            self.assertEqual(len(flagged), 1, errors)
            self.assertIn("corrupt.md", flagged[0])
            self.assertIn("2 occurrences", flagged[0])
            self.assertNotIn("clean.md", " ".join(errors))

    def test_the_pull_request_check_builds_this_track_too(self):
        _, text = self.workflow("paper-scout-checks.yml")
        self.assertIn(TRACK, text)

    def test_discovery_still_cannot_reach_the_scientific_gate(self):
        workflow, _ = self.workflow("paper-scout.yml")
        discovery = next(step for step in workflow["jobs"]["scout"]["steps"]
                         if step["name"] == "Run discovery and metadata update")
        self.assertNotIn("GEMINI_API_KEY", discovery.get("env", {}))
        self.assertNotIn("OPENROUTER_API_KEY", discovery.get("env", {}))
        self.assertIn(f"run --track {TRACK} --no-llm", discovery["run"])

    def test_no_track_config_can_raise_the_daily_assessment_bound(self):
        """A track's own assessment quota cannot reach the scheduled pipeline.

        `quality.assessment.max_assessments_per_run` is 4 or 5 on every track, which reads
        as if a daily run could assess five papers from one track. It cannot: the daily
        discovery step passes --no-llm, which disables the queue that setting bounds, and
        the assessment stage goes through `operational-assess`, where RunBudget enforces
        the frozen limits. Both halves are pinned here, because a discovery step that lost
        its --no-llm would silently hand a track five adjudications.
        """
        from paper_scout.operational_preflight import MAX_PAPERS_PER_RUN, MAX_PAPERS_PER_TRACK
        workflow, _ = self.workflow("paper-scout.yml")
        discovery = next(step for step in workflow["jobs"]["scout"]["steps"]
                         if step["name"] == "Run discovery and metadata update")
        for line in discovery["run"].splitlines():
            if "paper_scout run --track" in line:
                self.assertIn("--no-llm", line, f"discovery without --no-llm can assess: {line.strip()}")
        for track in TRACK_CONFIG_PATHS:
            quota = load_config(track_id=track, env={}).quality.assessment.max_assessments_per_run
            self.assertGreater(quota, 0)
            # Deliberately NOT asserting quota <= 1: the field is inert in the scheduled
            # pipeline, and forcing it to 1 would change what a manual run does.
        budget_track, budget_run = MAX_PAPERS_PER_TRACK, MAX_PAPERS_PER_RUN
        self.assertEqual((budget_track, budget_run), (1, len(TRACKS)))

    def test_the_committed_ceiling_matches_the_code(self):
        from paper_scout.operational_preflight import DEFAULT_OPENROUTER_RUN_CEILING_USD
        workflow, _ = self.workflow("paper-scout.yml")
        assess = next(step for step in workflow["jobs"]["scout"]["steps"]
                      if step["name"] == "Bounded scientific assessment")
        self.assertEqual(float(assess["env"]["PAPER_SCOUT_OPENROUTER_RUN_CEILING_USD"]),
                         DEFAULT_OPENROUTER_RUN_CEILING_USD)


class QualityPolicyUnchanged(unittest.TestCase):
    def test_this_track_adds_no_rubric_of_its_own(self):
        """The promotion gate is shared and versioned; a per-track rubric would fork it."""
        config = load_config(track_id=TRACK, env={})
        reference = load_config(track_id="agent_memory", env={})
        self.assertEqual(config.quality.assessment.version, reference.quality.assessment.version)
        self.assertEqual(config.quality.assessment.rubric_version, reference.quality.assessment.rubric_version)
        self.assertEqual(config.quality.mode, reference.quality.mode)
        self.assertEqual(config.quality.ranking, reference.quality.ranking)

    def test_no_computer_vision_special_case_reached_the_scientific_modules(self):
        for module in ("quality.py", "quality_llm.py", "quality_models.py", "promotion_gate.py",
                       "promotion_protocol.py", "quality_service.py"):
            text = (ROOT / "paper_scout" / module).read_text(encoding="utf-8")
            for marker in ("computer_vision", "yolo", "YOLO", "mAP", "AP50"):
                self.assertNotIn(marker, text, f"{module} was specialised for this track")


if __name__ == "__main__":
    unittest.main()
