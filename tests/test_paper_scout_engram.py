from contextlib import redirect_stdout
from dataclasses import replace
from datetime import datetime, timezone, timedelta
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import Mock, patch

from paper_scout.cli import main
from paper_scout.config import TRACK_CONFIG_PATHS, load_config, track_links
from paper_scout.discovery_evaluation import evaluate_discovery
from paper_scout.engram_evaluation import regression_cases, seed_fixtures
from paper_scout.evaluation import evaluate_relevance_examples, relevance_fixture_examples
from paper_scout.models import PaperCandidate, SourceFetchResult
from paper_scout.query_planner import plan_queries
from paper_scout.relevance import classify_with_rules, explain_rule_matches
from paper_scout.scout import ingest_candidate, run_backfill, run_scout, _queries_for_run
from paper_scout.seeds import ingest_seeds
from paper_scout.site import build_site, _is_new_since_first_seen
from paper_scout.state import PaperStore

ROOT = Path(__file__).resolve().parents[1]


def isolated(root, track="engram"):
    config = load_config(track_id=track, env={})
    return replace(config, sqlite_path=root / config.sqlite_path,
                   digest_dir=root / config.digest_dir, report_dir=root / config.report_dir,
                   docs_dir=root / config.docs_dir, relevance_llm_enabled=False,
                   quality=replace(config.quality, mode="deterministic", full_text=replace(config.quality.full_text, enabled=False)))


class EngramTests(unittest.TestCase):
    def test_tracks_registered_unknown_rejected_and_defaults_unchanged(self):
        self.assertEqual(set(TRACK_CONFIG_PATHS), {"agent_memory", "deep_research", "engram"})
        self.assertEqual(load_config(env={}).sqlite_path, Path("data/paper_scout.sqlite3"))
        config = load_config(track_id="engram", env={})
        self.assertEqual(config.docs_dir, Path("docs/engram"))
        self.assertEqual(config.sqlite_path, Path("data/engram/paper_scout.sqlite3"))
        self.assertEqual(config.quality.mode, "deterministic")
        self.assertFalse(config.relevance_llm_enabled)
        for action in (lambda: load_config(track_id="typo"),
                       lambda: classify_with_rules(seed_fixtures()[0], "typo"),
                       lambda: explain_rule_matches(seed_fixtures()[0], "typo")):
            with self.assertRaises(ValueError):
                action()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unknown.yaml"
            path.write_text('track:\n  id: typo\n')
            with self.assertRaises(ValueError):
                load_config(path, env={})
            path.write_text('track:\n  id: deep_research\n')
            with self.assertRaises(ValueError):
                load_config(path, track_id="engram", env={})
        with redirect_stdout(io.StringIO()), patch("sys.stderr", new=io.StringIO()):
            with self.assertRaises(SystemExit):
                main(["build-site", "--track", "typo"])

    def test_seed_records_classify_without_curation_or_agent_keyword(self):
        for paper in seed_fixtures():
            with self.subTest(id=paper.arxiv_id):
                result = classify_with_rules(paper, "engram")
                self.assertEqual(result.decision, "relevant", result.reason)
                self.assertIn("title/abstract", result.reason)
                self.assertTrue(explain_rule_matches(paper, "engram")["high_confidence_hits"])

    def test_adversarial_scope_and_adjacent_review(self):
        for title, abstract, expected in regression_cases():
            with self.subTest(title=title):
                paper = PaperCandidate(title, [], abstract, "fixture", title)
                self.assertEqual(classify_with_rules(paper, "engram").decision, expected)
        report = evaluate_relevance_examples(relevance_fixture_examples("engram"), profile="engram")
        self.assertEqual(report["decision_mismatches"], [])
        self.assertEqual(report["precision"], 1)

    def test_query_budget_modes_and_retry_zero_budget(self):
        config = load_config(track_id="engram", env={})
        queries = plan_queries(config)
        for source in config.query_budgets:
            self.assertEqual(sum(q.source == source for q in queries), 4)
        self.assertFalse(any(q.route == "category_sweep" for q in queries))
        self.assertTrue(any(q.mode == "phrase" for q in queries))
        self.assertTrue(any(" AND " in q.provider_query for q in queries))
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / "state.sqlite3")
            store.record_failed_query("engram", "arxiv", "all:old", 240, "timeout")
            with sqlite3.connect(store.path) as db:
                db.execute("UPDATE failed_queries SET next_retry_at = '2000-01-01'")
            planned = _queries_for_run(config, store, {"arxiv"}, 10)
            self.assertEqual(len(planned), 4)
            self.assertEqual(planned[0].route, "failed_query_retry")
            self.assertEqual(planned[0].days_override, 240)
            self.assertEqual(_queries_for_run(replace(config, query_budgets={"arxiv": 0}), store, {"arxiv"}, 10), [])
        for track in TRACK_CONFIG_PATHS:
            self.assertEqual(evaluate_discovery(load_config(track_id=track))["missed"], [])

    def test_seed_ingestion_outside_window_and_repeat_has_no_requests_or_notifications(self):
        papers = {p.arxiv_id: p for p in seed_fixtures()}
        fetch = Mock(side_effect=lambda arxiv_id: papers[arxiv_id])
        with tempfile.TemporaryDirectory() as tmp, patch("paper_scout.scout.send_optional_notifications") as notify:
            config = isolated(Path(tmp))
            first = ingest_seeds(config, fetch=fetch)
            store = PaperStore(config.sqlite_path)
            with sqlite3.connect(store.path) as db:
                before = db.execute("SELECT canonical_key, published_date, updated_date, first_seen_at FROM papers ORDER BY canonical_key").fetchall()
            self.assertEqual(store.paper_count(), 4)
            self.assertEqual(fetch.call_count, 4)
            second = ingest_seeds(config, fetch=fetch)
            self.assertEqual(fetch.call_count, 4)
            self.assertEqual(first["unresolved"], [])
            self.assertTrue(all(r["status"] == "already_known" for r in second["results"]))
            with sqlite3.connect(store.path) as db:
                after = db.execute("SELECT canonical_key, published_date, updated_date, first_seen_at FROM papers ORDER BY canonical_key").fetchall()
                self.assertEqual(db.execute("SELECT COUNT(*) FROM notifications").fetchone()[0], 0)
            self.assertEqual(before, after)
            self.assertEqual(before[0][1:3], ("2026-01-12", "2026-07-12"))
            for row in before:
                self.assertLess(abs((datetime.now(timezone.utc) - datetime.fromisoformat(row[3]).replace(tzinfo=timezone.utc)).total_seconds()), 60)
            notify.assert_not_called()

    def test_unresolved_seed_reports_mismatch_and_missing_metadata_honestly(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = isolated(Path(tmp))
            wrong = replace(seed_fixtures()[0], arxiv_id="wrong")
            report = ingest_seeds(config, fetch=lambda **_: wrong)
            self.assertEqual(len(report["unresolved"]), 4)
            self.assertEqual(PaperStore(config.sqlite_path).paper_count(), 0)
            report = ingest_seeds(config, fetch=lambda **_: None)
            self.assertEqual(len(report["unresolved"]), 4)

    def test_revisions_aliases_backfill_and_notifications_are_idempotent(self):
        paper = seed_fixtures()[0]
        with tempfile.TemporaryDirectory() as tmp:
            config = replace(isolated(Path(tmp)), query_budgets={"arxiv": 1})
            one = ingest_candidate(config, replace(paper, arxiv_id=paper.arxiv_id + "v1"))
            revised = replace(paper, arxiv_id=paper.arxiv_id + "v3", doi="10.48550/arXiv." + paper.arxiv_id, updated_date="2026-09-03")
            two = ingest_candidate(config, revised)
            self.assertEqual(one[1], two[1])
            fetcher = Mock(source="arxiv")
            fetcher.search_planned_with_diagnostics.return_value = SourceFetchResult(1, [revised])
            fetcher.http = None
            notifier = Mock(return_value=True)
            first = run_scout(config, fetchers=[fetcher], notifier=notifier)
            again = run_backfill(config, days=240, fetchers=[fetcher])
            last = run_scout(config, fetchers=[fetcher], notifier=notifier)
            self.assertEqual(PaperStore(config.sqlite_path).paper_count(), 1)
            self.assertEqual(notifier.call_count, 1)
            self.assertEqual((first.new_digest_count, again.new_digest_count, last.new_digest_count), (1, 0, 0))

    def test_tracks_can_overlap_with_independent_screening_and_notification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paper = seed_fixtures()[0]
            configs = [isolated(root, track) for track in TRACK_CONFIG_PATHS]
            results = [ingest_candidate(c, paper) for c in configs]
            self.assertEqual([PaperStore(c.sqlite_path).paper_count() for c in configs], [1, 1, 1])
            self.assertEqual(results[2][2].decision, "relevant")
            self.assertNotEqual(results[1][2].decision, "relevant")
            self.assertEqual(len({r[1] for r in results}), 1)
            PaperStore(configs[0].sqlite_path).mark_notified([results[0][1]], "2026-09-04")
            self.assertEqual(PaperStore(configs[2].sqlite_path).get_notified_for_date("2026-09-04"), [])

    def test_incomplete_window_is_retained_and_not_resolved_by_truncated_response(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = replace(isolated(Path(tmp)), query_budgets={"arxiv": 1})
            class Truncated:
                source = "arxiv"
                def search_planned_with_diagnostics(self, query, days, max_results):
                    return SourceFetchResult(25, seed_fixtures(), incomplete=True)
            result = run_scout(config, fetchers=[Truncated()], notifications_enabled=False)
            self.assertEqual(result.query_diagnostics[0]["status"], "incomplete_window")
            self.assertIn("incomplete discovery window", result.source_failures[0])
            self.assertEqual(PaperStore(config.sqlite_path).failed_queries("engram")[0]["failure_type"], "incomplete_window")

    def test_pages_exports_schema_links_and_no_cross_track_wording(self):
        import jsonschema
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            configs = [isolated(root, track) for track in TRACK_CONFIG_PATHS]
            class FixtureFetcher:
                source = "arxiv"
                def search_planned(self, *args):
                    return seed_fixtures()
            for config in configs:
                run_scout(config, fetchers=[FixtureFetcher()], notifications_enabled=False)
                result = build_site(digest_dir=config.digest_dir, report_dir=config.report_dir, docs_dir=config.docs_dir,
                                    state_path=config.sqlite_path, curation_path=config.curation_path,
                                    site_title=config.title, site_subtitle=config.subtitle,
                                    relevance_profile=config.relevance_profile, quality_config=config.quality)
                self.assertTrue(result.built)
            for config in configs:
                schema = json.loads((config.docs_dir / "data/paper-card.schema.json").read_text())
                for name in ["index.html", "latest.html", "archive.html", "about.html", "data/papers.json", "data/latest.json", "data/papers.csv", "data/papers.bib"]:
                    self.assertTrue((config.docs_dir / name).exists(), name)
                if config.track_id == "engram":
                    self.assertIn("blob/main/digests/engram/latest.md", (config.docs_dir / "index.html").read_text())
                for sidecar in (config.docs_dir / "papers").glob("*.json"):
                    data = json.loads(sidecar.read_text())
                    jsonschema.validate(data, schema)
                    if config.track_id == "engram":
                        if data.get("arxiv_id") == "2601.07372":
                            self.assertEqual(data["publication"]["date"], "2026-01-12")
                            self.assertEqual(data["publication"]["latest_revision_date"], "2026-07-12")
                        self.assertNotIn("Directly relevant to agentic-memory", sidecar.read_text())
                        self.assertEqual(data["structured_card"]["key_contribution"]["value"], "Not extracted yet")
                for html in [*config.docs_dir.glob("*.html"), *(config.docs_dir / "papers").glob("*.html")]:
                    text = html.read_text()
                    for label, href in track_links(config.track_id):
                        expected = ("../" if html.parent.name == "papers" else "") + href
                        self.assertIn(f'href="{expected}"', text)
                        self.assertTrue((html.parent / expected).resolve().exists())
                    if config.track_id != "engram":
                        self.assertNotIn("Relation to Engram / conditional memory", text)
                        self.assertNotIn("Implementation references", text)
            # Rebuilding the root does not remove either nested track.
            snapshots = {path: path.read_bytes() for config in configs[1:] for path in config.docs_dir.rglob("*") if path.is_file()}
            c = configs[0]
            build_site(c.digest_dir, c.report_dir, c.docs_dir, c.sqlite_path, c.curation_path)
            self.assertTrue(all(path.read_bytes() == content for path, content in snapshots.items()))

    def test_future_first_seen_is_never_new(self):
        now = datetime.now(timezone.utc)
        self.assertFalse(_is_new_since_first_seen((now + timedelta(hours=1)).isoformat(), now, now.date().isoformat()))
        self.assertTrue(_is_new_since_first_seen((now - timedelta(hours=1)).isoformat(), now, now.date().isoformat()))
        self.assertFalse(_is_new_since_first_seen(now.date().isoformat(), now, now.date().isoformat()))
        self.assertFalse(_is_new_since_first_seen(now.date().isoformat() + " broken", now, now.date().isoformat()))
        # A future instant with a negative offset must not look old after dropping the offset.
        future = (now + timedelta(hours=1)).astimezone(timezone(timedelta(hours=-5)))
        self.assertFalse(_is_new_since_first_seen(future.isoformat(), now, now.date().isoformat()))
