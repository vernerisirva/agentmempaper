"""Automatic queue behavior and budget safety, without network or model calls."""
from dataclasses import replace
from datetime import UTC, datetime
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from paper_scout.operational_preflight import RunBudget
from paper_scout.operational_run import select_operational_candidates
from paper_scout.site import _assessment_label
import test_operational_eligibility as operational_tests
from test_operational_eligibility import row


def paper(key, seen, decision="relevant"):
    return SimpleNamespace(canonical_id=key, title=key, first_seen_at=seen,
                           decision=decision, doi=None, arxiv_id=None, openalex_id=None,
                           semantic_scholar_id=None, url=None)


class AutomaticSelection(unittest.TestCase):
    def select(self, papers, day="2026-10-16", stored=None, suppressed=None, **kwargs):
        configs = {track: SimpleNamespace(sqlite_path=track, track=track) for track in papers}
        with patch("paper_scout.operational_run.ranked_candidates",
                   side_effect=lambda config, _: (papers[config.track], day)), \
             patch("paper_scout.operational_run._stored_assessments", return_value=stored or {}), \
             patch("paper_scout.operational_run._suppressed", return_value=suppressed or set()):
            return select_operational_candidates(
                configs, day + "T00:00:00", now=datetime.fromisoformat(day).replace(tzinfo=UTC),
                **kwargs)

    def test_oldest_waiting_paper_gets_a_turn_before_new_arrivals(self):
        selected, summaries = self.select({"agent_memory": [
            paper("new", "2026-10-16"), paper("MemAgent", "2026-09-29"),
            paper("oldest", "2026-09-01"), paper("boundary", "2026-10-09"),
            paper("six-days", "2026-10-10")]})
        self.assertEqual([(c.canonical_id, c.queue) for c in selected], [
            ("oldest", "backlog"), ("MemAgent", "backlog"), ("boundary", "backlog"),
            ("new", "recent"), ("six-days", "recent")])
        self.assertEqual(summaries["agent_memory"].eligible, 5)
        self.assertEqual(summaries["agent_memory"].backlog_eligible, 3)

    def test_completed_suppressed_and_cooling_papers_do_not_block_the_oldest(self):
        selected, summaries = self.select({"t": [
            paper("done", "2026-09-01"), paper("blocked", "2026-09-01"),
            paper("cooldown", "2026-09-01"), paper("maybe", "2026-09-01", "maybe"),
            paper("ready", "2026-09-29")]},
            stored={"done": [row("success")],
                    "cooldown": [row("transport_failure", at="2026-10-15T22:00:00+00:00")]},
            suppressed={"blocked"})
        self.assertEqual([c.canonical_id for c in selected], ["ready"])
        self.assertEqual(summaries["t"].eligible, 1)

    def test_backlog_keeps_moving_despite_daily_new_arrivals(self):
        stored = {}
        old = [paper(f"old-{i}", f"2026-09-{i+1:02}") for i in range(3)]
        for i in range(3):
            selected, _ = self.select({"t": [paper(f"new-{i}", f"2026-10-{16+i}")] + old},
                                      day=f"2026-10-{16+i}", stored=stored)
            self.assertEqual(selected[0].canonical_id, f"old-{i}")
            stored[f"old-{i}"] = [row("success")]

    def test_tracks_rotate_and_take_turns_before_another_attempt(self):
        first_tracks = []
        for i in range(4):
            selected, _ = self.select({t: [paper(t+str(j), "2026-09-01") for j in range(8)]
                                      for t in ("a", "b", "c", "d")}, day=f"2026-10-{16+i}")
            first_tracks.append(selected[0].track)
            self.assertEqual(len({c.track for c in selected[:4]}), 4)
            self.assertTrue(all(c.queue == "backlog" for c in selected[:4]))
        self.assertEqual(set(first_tracks), {"a", "b", "c", "d"})

    def test_bounded_nominations_report_the_full_backlog_and_do_not_duplicate(self):
        selected, summaries = self.select({"t": [paper(str(i), "2026-09-01") for i in range(100)]})
        self.assertEqual(len(selected), 12)
        self.assertEqual(len({c.canonical_id for c in selected}), 12)
        self.assertEqual(sum(c.queue == "backlog" for c in selected), 6)
        self.assertEqual(summaries["t"].eligible, 100)
        self.assertEqual(summaries["t"].backlog_eligible, 100)

    def test_missing_and_future_discovery_dates_cannot_jump_the_queue(self):
        selected, _ = self.select({"t": [paper("missing", None), paper("bad", "unknown"),
                                         paper("future", "2027-01-01")]})
        self.assertTrue(all(c.queue == "recent" for c in selected))

    def test_small_old_only_queue_can_use_both_slots(self):
        selected, _ = self.select({"t": [paper("older", "2026-09-01"), paper("old", "2026-09-02")]})
        self.assertEqual([(c.canonical_id, c.queue) for c in selected],
                         [("older", "backlog"), ("old", "recent")])

    def test_arxiv_assessment_survives_a_doi_identity_change(self):
        # Production reproduction: MemCode was assessed under arxiv:2610.19472,
        # then merged into its arXiv DOI during the next discovery run.
        selected, summaries = self.select({"t": [
            paper("doi:10.48550/arxiv.2610.19472", "2026-10-15")]},
            stored={"arxiv:2610.19472": [row("success")]})
        self.assertEqual(selected, [])
        self.assertEqual(summaries["t"].already_assessed, 1)

    def test_doi_assessment_survives_the_reverse_identity_change(self):
        selected, _ = self.select({"t": [paper("arxiv:2610.19472", "2026-10-15")]},
            stored={"doi:10.48550/arxiv.2610.19472": [row("success", status="uncertain")]})
        self.assertEqual(selected, [])

    def test_alias_matching_does_not_multiply_technical_attempts(self):
        selected, _ = self.select({"t": [paper("doi:10.48550/arxiv.2610.19472", "2026-10-01")]},
            stored={"doi:10.48550/arxiv.2610.19472": [
                row("transport_failure", at="2026-10-01T00:00:00+00:00")]})
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].retry.attempts, 1)

    def test_suppression_follows_an_identifier_alias(self):
        selected, summaries = self.select({"t": [paper("doi:10.48550/arxiv.2610.19472", "2026-10-01")]},
                                          suppressed={"arxiv:2610.19472"})
        self.assertEqual(selected, [])
        self.assertEqual(summaries["t"].suppressed, 1)

    def test_an_unrelated_assessment_does_not_exclude_a_new_paper(self):
        selected, _ = self.select({"t": [paper("arxiv:2610.19472", "2026-10-15")]},
                                 stored={"arxiv:2610.19473": [row("success")]})
        self.assertEqual(len(selected), 1)


class AutomaticWalk(unittest.TestCase):
    def setUp(self):
        self.h = operational_tests.AcquisitionWalk()

    def success(self):
        return self.h.fake_assessment("success", gemini=1, openrouter=1, cost=0.03, status="pass")

    def test_one_backlog_and_one_recent_paper_are_assessed(self):
        nominees = [replace(self.h.nominee("t", i, str(i)), queue=q)
                    for i, q in enumerate(["backlog", "backlog", "recent", "recent"])]
        metrics, budget, seen, _ = self.h.walk(
            nominees, {str(i): self.success() for i in range(4)}, budget=RunBudget())
        self.assertEqual(seen, ["0", "2"])
        self.assertEqual(budget.total_assessed, 2)
        self.assertEqual(metrics.papers_walked + metrics.nominees_not_walked, 4)

    def test_failed_acquisition_preserves_the_backlog_slot(self):
        nominees = [replace(self.h.nominee("t", i, str(i)), queue=q)
                    for i, q in enumerate(["backlog", "backlog", "recent"])]
        _, budget, seen, _ = self.h.walk(nominees, {
            "0": self.h.fake_assessment("manuscript_unavailable"),
            "1": self.success(), "2": self.success()}, budget=RunBudget())
        self.assertEqual(seen, ["0", "1", "2"])
        self.assertEqual(budget.total_assessed, 2)

    def test_without_backlog_two_recent_papers_can_use_the_capacity(self):
        nominees = [self.h.nominee("t", i, str(i)) for i in range(3)]
        _, budget, seen, _ = self.h.walk(nominees, {str(i): self.success() for i in range(3)},
                                       budget=RunBudget())
        self.assertEqual(seen, ["0", "1"])
        self.assertEqual(budget.total_assessed, 2)

    def test_cross_track_alias_is_not_assessed_twice(self):
        nominees = [replace(self.h.nominee(t, 1, key), identities=("arxiv:2609.32521",))
                    for t, key in [("a", "arxiv-id"), ("b", "doi-id")]]
        _, budget, seen, summaries = self.h.walk(
            nominees, {"arxiv-id": self.success(), "doi-id": self.success()}, budget=RunBudget())
        self.assertEqual(seen, ["arxiv-id"])
        self.assertEqual(budget.total_assessed, 1)
        self.assertEqual(summaries["b"].skipped_before_model[0]["outcome"], "already_attempted_this_run")

    def test_unpriced_receipt_stops_before_another_track_spends(self):
        unpriced = self.success()
        del unpriced.execution["calls"][1]["usage"]["cost"]
        nominees = [self.h.nominee(t, 1, t) for t in ("a", "b")]
        metrics, budget, seen, _ = self.h.walk(nominees, {"a": unpriced, "b": self.success()},
                                             budget=RunBudget())
        self.assertEqual(seen, ["a"])
        self.assertEqual(budget.stopped_reason, "unknown_model_cost")
        self.assertEqual(metrics.unknown_cost_calls, 1)

    def test_nonfinite_prices_and_limits_cannot_bypass_the_budget(self):
        from paper_scout.cli import _role_usage
        for value in (float("nan"), float("inf"), -1, "not-a-price"):
            with self.subTest(value=value):
                result = self.success()
                result.execution["calls"][1]["usage"]["cost"] = value
                self.assertEqual(_role_usage(result)["unknown_cost_calls"], 1)
        for value in ("nan", "inf", "-inf"):
            with self.assertRaises(ValueError):
                RunBudget.from_env({"PAPER_SCOUT_OPENROUTER_RUN_CEILING_USD": value})
        with self.assertRaises(ValueError):
            RunBudget().reserve("t", float("nan"))

    def test_shared_cost_ceiling_stops_before_the_paper_count_limit(self):
        nominees = [self.h.nominee(t, i, t+str(i)) for i in range(2) for t in ("a", "b", "c", "d")]
        result = self.h.fake_assessment("success", gemini=1, openrouter=1, cost=0.08)
        _, budget, seen, _ = self.h.walk(nominees, {c.canonical_id: result for c in nominees},
                                       budget=RunBudget())
        self.assertEqual(len(seen), 4)
        self.assertEqual(budget.stopped_reason, "openrouter_ceiling_reached")


class AutomaticStatus(unittest.TestCase):
    def label(self, **changes):
        p = dict(quality_status="not_assessed", quality_promotion={}, decision="relevant",
                 quality_assessor_type=None, quality_full_text_assessed=False)
        p.update(changes)
        return _assessment_label(SimpleNamespace(**p))

    def test_pending_and_inconclusive_are_distinct(self):
        self.assertEqual(self.label(), "Awaiting AI assessment")
        self.assertEqual(self.label(quality_status="uncertain", quality_assessor_type="hybrid",
                                    quality_full_text_assessed=True,
                                    quality_promotion={"outcome": "success"}), "AI assessment inconclusive")

    def test_technical_failure_and_possible_match_do_not_promise_a_decision(self):
        self.assertEqual(self.label(quality_status="uncertain",
                                    quality_promotion={"outcome": "text_coverage_failure"}),
                         "AI assessment unavailable")
        self.assertEqual(self.label(decision="maybe"), "Possible topical match")

    def test_deterministic_placeholder_is_not_an_ai_assessment(self):
        self.assertEqual(self.label(quality_status="uncertain", quality_assessor_type="deterministic"),
                         "Awaiting AI assessment")


class MergedAssessmentHistory(unittest.TestCase):
    def candidate(self, key, **changes):
        from paper_scout.site import LibraryPaper
        p = dict(canonical_id=key, title="MemCode: Discrete Semantic Representations for Long-Term Agent Memory",
                 authors=[], abstract_summary="Memory study", reason="Relevant", score=90,
                 decision="relevant", tags=[], source="arxiv", source_id="2610.19472",
                 doi=None, arxiv_id="2610.19472", semantic_scholar_id=None, openalex_id=None,
                 url=None, published_date="2026-10-14", first_seen_at="2026-10-15",
                 last_seen_at="2026-10-16", notified_at=None, notified_date=None)
        p.update(changes)
        return LibraryPaper(**p)

    def assessed(self, status="pass", at="2026-10-16T08:00:00+00:00", outcome="success"):
        return self.candidate("arxiv:2610.19472", quality_status=status,
                              quality_assessed_at=at, quality_assessor_type="hybrid",
                              quality_scope="full_text", quality_full_text_assessed=True,
                              quality_promotion={"outcome": outcome, "primary": {"canonical_id": "arxiv:2610.19472"}})

    def test_richer_source_metadata_cannot_erase_the_assessment(self):
        from paper_scout.site import _main_library, _merge_two_papers
        known = self.assessed()
        richer = self.candidate("doi:10.48550/arxiv.2610.19472", score=99)
        for left, right in ((known, richer), (richer, known)):
            merged = _merge_two_papers(left, right)
            self.assertEqual(merged.canonical_id, richer.canonical_id)
            self.assertTrue(_main_library(merged))
            self.assertEqual(merged.quality_promotion, known.quality_promotion)

    def test_latest_scientific_decision_wins_including_nonpasses(self):
        from paper_scout.site import _main_library, _merge_two_papers
        for status in ("uncertain", "insufficient"):
            latest = replace(self.assessed(status, at="2026-10-16T10:00:00+00:00"),
                             canonical_id="doi:10.48550/arxiv.2610.19472")
            merged = _merge_two_papers(self.assessed(), latest)
            self.assertEqual(merged.quality_status, status)
            self.assertFalse(_main_library(merged))

    def test_technical_failure_does_not_replace_a_completed_decision(self):
        from paper_scout.site import _merge_two_papers
        failed = self.assessed("uncertain", at="2026-10-16T10:00:00+00:00", outcome="transport_failure")
        merged = _merge_two_papers(self.assessed(), failed)
        self.assertEqual(merged.quality_status, "pass")
        self.assertEqual(merged.quality_promotion["outcome"], "success")

    def test_receipt_times_are_compared_as_times_across_formats_and_offsets(self):
        from paper_scout.site import _merge_two_papers
        for timestamp in ("2026-10-16 09:00:00", "2026-10-16T11:00:00+02:00"):
            merged = _merge_two_papers(self.assessed(), self.assessed("insufficient", at=timestamp))
            self.assertEqual(merged.quality_status, "insufficient")

    def test_suppression_is_preserved_when_metadata_aliases_merge(self):
        from paper_scout.site import _main_library, _merge_two_papers
        merged = _merge_two_papers(replace(self.assessed(), quality_suppressed=True),
                                   self.candidate("doi:10.48550/arxiv.2610.19472", score=99))
        self.assertTrue(merged.quality_suppressed)
        self.assertFalse(_main_library(merged))


if __name__ == "__main__":
    unittest.main()
