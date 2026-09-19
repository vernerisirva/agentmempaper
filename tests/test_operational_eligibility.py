"""Operational retry eligibility, credential preflight, budget and private state.

No paid calls. Every model interaction is the offline ``Models`` double from
test_promotion_gate, and the credential tests assert on presence only: no test reads,
prints or asserts a credential value.

The invariant under test throughout is the one the operationalization exists to
establish: a technical failure must never be mistaken for a scientific decision, and
must never permanently consume a paper's eligibility.
"""
from contextlib import closing
from dataclasses import replace
from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
import sqlite3
import tarfile
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.operational_eligibility import (
    LEGACY_EXCLUSION_POLICY, MAX_OPERATIONAL_ATTEMPTS, OPERATIONAL_EXCLUSION_POLICY,
    RETRY_COOLDOWN_HOURS, excludes_from_eligibility, is_completed_scientific_assessment,
    is_technical_attempt, retry_state,
)
from paper_scout.operational_preflight import (
    CostCeilingExceeded, MAX_PAPERS_PER_RUN, MAX_PAPERS_PER_TRACK, RunBudget,
    credential_preflight,
)
from paper_scout.promotion_gate import assess_promotion
from paper_scout.runtime_snapshot import (
    CURRENT_MANIFEST_VERSION, MANIFEST, STATE_PATHS, pack_snapshot, restore_snapshot,
)
from paper_scout.state import PaperStore
from test_promotion_gate import ENV, Models, fixture


def insert_assessment(path, canonical_id, payload):
    """Insert one row through the real schema, which is fully NOT NULL constrained."""
    with closing(sqlite3.connect(path)) as db:
        db.execute(
            "INSERT INTO paper_quality_assessments (canonical_id, assessment_version,"
            " rubric_version, assessor_type, assessor_model, source_content_hash,"
            " assessed_at, recommendation, confidence, assessment_scope, paper_type,"
            " payload_json) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (canonical_id, "quality-promotion-v2", "scholarly-rubric-v2",
             payload.get("assessor_type", "hybrid"), "synthetic-model",
             "0" * 64, payload.get("assessed_at", "2026-09-19T00:00:00+00:00"),
             "unknown", "low", payload.get("assessment_scope", "full_text"),
             "empirical", json.dumps(payload)))
        db.commit()


def row(outcome=None, *, assessor="hybrid", scope="full_text", status="pass", at=None):
    """One stored assessment payload, shaped as the database holds it."""
    payload = {"assessor_type": assessor, "assessment_scope": scope, "quality_status": status,
               "assessed_at": at or datetime.now(UTC).isoformat()}
    if outcome is not None:
        payload["execution"] = {"outcome": outcome}
    return payload


class CompletedAssessmentPredicate(unittest.TestCase):
    """A completed scientific assessment is a decision, not merely a stored row."""

    def test_successful_dual_gate_row_is_completed(self):
        self.assertTrue(is_completed_scientific_assessment(row("success")))
        self.assertFalse(is_technical_attempt(row("success")))

    def test_legacy_scientific_row_is_completed(self):
        self.assertTrue(is_completed_scientific_assessment(row("scientific", status="uncertain")))

    def test_pre_receipt_legacy_row_is_completed(self):
        # Rows written before execution receipts existed carry no outcome. Assessor type
        # and scope are the only evidence, and both say a semantic assessor read it.
        self.assertTrue(is_completed_scientific_assessment(row(None, assessor="llm")))

    def test_deterministic_placeholder_is_not_completed_and_not_an_attempt(self):
        placeholder = row(None, assessor="deterministic", scope="abstract", status="uncertain")
        self.assertFalse(is_completed_scientific_assessment(placeholder))
        self.assertFalse(is_technical_attempt(placeholder))

    def test_every_technical_outcome_is_incomplete(self):
        for outcome in ("not_assessed", "transport_failure", "protocol_failure",
                        "manuscript_unavailable", "text_coverage_failure", "integrity_failure",
                        "evidence_validation_failure", "support_verification_pending",
                        "credential_unavailable"):
            with self.subTest(outcome=outcome):
                record = row(outcome, status="uncertain")
                self.assertFalse(is_completed_scientific_assessment(record))
                self.assertTrue(is_technical_attempt(record))

    def test_abstract_only_row_is_not_a_manuscript_assessment(self):
        self.assertFalse(is_completed_scientific_assessment(row("success", scope="abstract")))


class RetryEligibility(unittest.TestCase):
    def test_never_assessed_paper_is_eligible(self):
        state = retry_state("p", [])
        self.assertTrue(state.eligible)
        self.assertEqual(state.reason, "never_assessed")
        self.assertEqual(state.attempts, 0)

    def test_completed_assessment_ends_eligibility(self):
        state = retry_state("p", [row("success")])
        self.assertFalse(state.eligible)
        self.assertEqual(state.reason, "completed_scientific_assessment")

    def test_non_promotion_is_still_a_completed_assessment(self):
        # An uncertain scientific decision is a decision. Reassessing it would duplicate
        # a settled scientific result, which is exactly what must not loop.
        state = retry_state("p", [row("success", status="uncertain")])
        self.assertFalse(state.eligible)
        self.assertEqual(state.reason, "completed_scientific_assessment")

    def test_technical_failure_leaves_the_paper_eligible(self):
        stale = (datetime.now(UTC) - timedelta(hours=RETRY_COOLDOWN_HOURS + 1)).isoformat()
        for outcome in ("transport_failure", "protocol_failure", "manuscript_unavailable",
                        "text_coverage_failure", "integrity_failure", "not_assessed"):
            with self.subTest(outcome=outcome):
                state = retry_state("p", [row(outcome, status="uncertain", at=stale)])
                self.assertTrue(state.eligible)
                self.assertEqual(state.reason, "retry_eligible")
                self.assertEqual(state.attempts, 1)

    def test_cooldown_blocks_an_immediate_retry(self):
        state = retry_state("p", [row("transport_failure", status="uncertain")])
        self.assertFalse(state.eligible)
        self.assertEqual(state.reason, "retry_cooldown")

    def test_retry_budget_is_bounded(self):
        stale = (datetime.now(UTC) - timedelta(days=30)).isoformat()
        rows = [row("manuscript_unavailable", status="uncertain", at=stale)
                for _ in range(MAX_OPERATIONAL_ATTEMPTS)]
        state = retry_state("p", rows)
        self.assertFalse(state.eligible)
        self.assertEqual(state.reason, "retry_budget_exhausted")
        self.assertEqual(state.attempts, MAX_OPERATIONAL_ATTEMPTS)

    def test_a_success_after_failures_still_ends_eligibility(self):
        stale = (datetime.now(UTC) - timedelta(days=30)).isoformat()
        rows = [row("transport_failure", status="uncertain", at=stale), row("success")]
        state = retry_state("p", rows)
        self.assertFalse(state.eligible)
        self.assertEqual(state.reason, "completed_scientific_assessment")

    def test_success_cannot_be_reassessed_into_a_duplicate_loop(self):
        # The loop this guards against: assess -> succeed -> remain selectable ->
        # assess again. One completed decision must terminate selection permanently.
        rows = [row("success")]
        for _ in range(5):
            state = retry_state("p", rows)
            self.assertFalse(state.eligible)
            rows = rows + [row("success")]

    def test_deterministic_rows_do_not_consume_the_retry_budget(self):
        rows = [row(None, assessor="deterministic", scope="abstract", status="uncertain")
                for _ in range(10)]
        state = retry_state("p", rows)
        self.assertTrue(state.eligible)
        self.assertEqual(state.attempts, 0)


class ExclusionPolicy(unittest.TestCase):
    def test_legacy_policy_excludes_on_any_row(self):
        technical = [row("manuscript_unavailable", status="uncertain")]
        self.assertTrue(excludes_from_eligibility(technical, LEGACY_EXCLUSION_POLICY))

    def test_operational_policy_excludes_only_on_a_decision(self):
        technical = [row("manuscript_unavailable", status="uncertain")]
        self.assertFalse(excludes_from_eligibility(technical, OPERATIONAL_EXCLUSION_POLICY))
        self.assertTrue(excludes_from_eligibility([row("success")], OPERATIONAL_EXCLUSION_POLICY))

    def test_unknown_policy_fails_closed(self):
        with self.assertRaises(ValueError):
            excludes_from_eligibility([], "whatever")

    def test_legacy_default_matches_the_original_select_distinct_semantics(self):
        """The default must stay bug-for-bug identical to the pre-fix exclusion.

        The frozen Batch 2-6 manifests were built when any stored row excluded a paper,
        and they are verified by rebuilding. Changing the default would silently
        invalidate a published scientific artifact, so the operational policy is opt-in.
        """
        from paper_scout.batch_population import excluded_identities
        from paper_scout.config import load_config
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.sqlite3"
            PaperStore(path)
            insert_assessment(path, "doi:10.1/technical",
                              row("manuscript_unavailable", status="uncertain"))
            insert_assessment(path, "doi:10.1/decided", row("success"))
            config = load_config(track_id="agent_memory")
            config = replace(config, sqlite_path=str(path))
            legacy = excluded_identities({"agent_memory": config}, (), LEGACY_EXCLUSION_POLICY)
            operational = excluded_identities({"agent_memory": config}, (),
                                              OPERATIONAL_EXCLUSION_POLICY)
        # Legacy excludes both; operational excludes only the decided paper.
        self.assertIn("canonical:doi:10.1/technical", legacy)
        self.assertIn("canonical:doi:10.1/decided", legacy)
        self.assertNotIn("canonical:doi:10.1/technical", operational)
        self.assertIn("canonical:doi:10.1/decided", operational)
        self.assertEqual(legacy["canonical:doi:10.1/decided"][0], "prior_assessment")
        self.assertEqual(operational["canonical:doi:10.1/decided"][0], "prior_completed_assessment")

    def test_a_legacy_manifest_still_reproduces_after_a_technical_row_appears(self):
        """The backward-compatibility claim, exercised end to end.

        A manifest written under the historical policy must keep rebuilding
        byte-identically, including its digest, after the operational policy exists. The
        frozen Batch 2-6 manifests carry no exclusion_policy field, so verify_manifest has
        to read an absent field as the historical policy rather than the current default.
        """
        from paper_scout.batch_population import (
            LEGACY_EXCLUSION_POLICY as legacy, OPERATIONAL_EXCLUSION_POLICY as operational,
            build_population, manifest_digest, population_manifest, verify_manifest)
        from paper_scout.config import load_config
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.sqlite3"
            PaperStore(path)
            config = replace(load_config(track_id="agent_memory"), sqlite_path=str(path))
            configs = {"agent_memory": config}

            population = build_population(configs, "2026-09-19T00:00:00", (), configs, legacy)
            manifest = population_manifest(population, "test-sha")
            # A frozen manifest predates the field entirely.
            self.assertNotIn("exclusion_policy", manifest["sources"])

            verification = verify_manifest(manifest, configs, configs)
            self.assertTrue(verification.reproduced)
            self.assertEqual(verification.stored_digest, verification.rebuilt_digest)
            self.assertEqual(manifest_digest(manifest), manifest["manifest_sha256"])

            # An operational manifest records its policy and therefore hashes differently,
            # which is correct: it describes a genuinely different population.
            operational_manifest = population_manifest(
                build_population(configs, "2026-09-19T00:00:00", (), configs, operational),
                "test-sha")
            self.assertEqual(operational_manifest["sources"]["exclusion_policy"], operational)
            self.assertTrue(verify_manifest(operational_manifest, configs, configs).reproduced)

    def test_historical_technical_rows_remain_auditable(self):
        # The fix must not delete or rewrite history. A technical row stays readable and
        # keeps reporting what it was; it simply stops being read as a decision.
        stored = [row("protocol_failure", status="uncertain", at="2026-01-01T00:00:00+00:00")]
        state = retry_state("p", stored)
        self.assertEqual(state.attempts, 1)
        self.assertEqual(state.last_outcome, "protocol_failure")
        self.assertEqual(state.last_attempt_at, "2026-01-01T00:00:00+00:00")
        self.assertEqual(stored[0]["execution"]["outcome"], "protocol_failure")


class CredentialPreflight(unittest.TestCase):
    """Presence only. No test asserts, prints or compares a credential value."""

    def test_both_credentials_present_permits_assessment(self):
        result = credential_preflight(environ=dict(ENV))
        self.assertTrue(result.ok)
        self.assertEqual(result.missing_roles, ())

    def test_missing_gemini_key_blocks_assessment(self):
        env = {"OPENROUTER_API_KEY": "synthetic-openrouter-key"}
        result = credential_preflight(environ=env)
        self.assertFalse(result.ok)
        self.assertIn("primary", result.missing_roles)
        self.assertIn("missing_credential", result.reason)

    def test_missing_openrouter_key_blocks_assessment(self):
        env = {"GEMINI_API_KEY": "synthetic-google-key"}
        result = credential_preflight(environ=env)
        self.assertFalse(result.ok)
        self.assertIn("adjudicator", result.missing_roles)

    def test_no_credentials_blocks_assessment(self):
        result = credential_preflight(environ={})
        self.assertFalse(result.ok)
        self.assertEqual(set(result.missing_roles), {"primary", "adjudicator"})

    def test_blank_credential_counts_as_absent(self):
        env = {"GEMINI_API_KEY": "   ", "OPENROUTER_API_KEY": "synthetic"}
        self.assertFalse(credential_preflight(environ=env).ok)

    def test_disabled_provider_blocks_assessment(self):
        env = {**ENV, "PAPER_SCOUT_LLM_PROVIDER": "off"}
        result = credential_preflight(environ=env)
        self.assertFalse(result.ok)
        self.assertEqual(result.reason, "scientific_provider_disabled")

    def test_preflight_report_never_carries_a_credential_value(self):
        report = json.dumps(credential_preflight(environ=dict(ENV)).to_dict())
        for value in ENV.values():
            self.assertNotIn(value, report)


class MissingCredentialWritesNoRow(unittest.TestCase):
    """The central regression: no credential must mean no stored row at all."""

    def test_gate_without_credentials_produces_no_completed_assessment(self):
        _, _, text, seed = fixture()
        with patch.dict("os.environ", {}, clear=True):
            result = assess_promotion(None, text, seed, "hybrid", http=None)
        self.assertEqual(result.execution["outcome"], "not_assessed")
        self.assertFalse(is_completed_scientific_assessment({
            "assessor_type": result.assessor_type, "assessment_scope": result.assessment_scope,
            "quality_status": result.quality_status, "execution": result.execution}))

    def test_a_not_assessed_row_leaves_the_paper_retry_eligible(self):
        stale = (datetime.now(UTC) - timedelta(days=2)).isoformat()
        state = retry_state("p", [row("not_assessed", assessor="deterministic",
                                      status="uncertain", at=stale)])
        self.assertTrue(state.eligible)

    def test_service_skips_without_persisting_when_credentials_are_absent(self):
        from paper_scout.quality_service import QualityRunStats, assess_and_store_candidate
        from paper_scout.config import load_config
        from paper_scout.models import ClassificationResult
        candidate, document, _, _ = fixture()
        config = load_config(track_id="agent_memory").quality
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / "state.sqlite3")
            stats = QualityRunStats()
            with patch.dict("os.environ", {}, clear=True), \
                 patch("paper_scout.quality_service.fetch_and_extract_pdf", return_value=document), \
                 patch("paper_scout.quality_service.locate_full_text_urls",
                       return_value=[document.source_url]):
                result = assess_and_store_candidate(
                    config, store, candidate, "fixture",
                    ClassificationResult(90, "relevant", "rule"), stats=stats)
            self.assertIsNone(result)
            self.assertTrue(stats.credential_skipped)
            with closing(sqlite3.connect(Path(tmp) / "state.sqlite3")) as db:
                stored = db.execute("SELECT COUNT(*) FROM paper_quality_assessments").fetchone()[0]
        # Nothing was written, so the paper is exactly as eligible as before the run.
        self.assertEqual(stored, 0)


class ProviderFailureKeepsPapersEligible(unittest.TestCase):
    def assess(self, models):
        _, _, text, seed = fixture()
        with patch.dict("os.environ", ENV, clear=True):
            return assess_promotion(None, text, seed, "hybrid", http=models)

    def test_primary_auth_failure_is_retry_eligible(self):
        from paper_scout.http import HttpRequestError

        class Failing(Models):
            def post_json(self, url, payload, headers):
                raise HttpRequestError("http", url, "401 unauthorized", status_code=401)

        result = self.assess(Failing())
        self.assertEqual(result.execution["outcome"], "transport_failure")
        stale = (datetime.now(UTC) - timedelta(days=2)).isoformat()
        self.assertTrue(retry_state("p", [row("transport_failure", status="uncertain",
                                              at=stale)]).eligible)

    def test_adjudicator_failure_is_retry_eligible(self):
        from paper_scout.http import HttpRequestError

        class FailingSecond(Models):
            def post_json(self, url, payload, headers):
                if len(self.payloads) >= 1:
                    raise HttpRequestError("http", url, "502 bad gateway", status_code=502)
                return super().post_json(url, payload, headers)

        result = self.assess(FailingSecond())
        self.assertEqual(result.execution["outcome"], "transport_failure")

    def test_protocol_failure_is_retry_eligible_under_the_bounded_policy(self):
        # A primary that answers outside the response contract. The gate exhausts its
        # bounded in-run retries and records a protocol failure rather than inventing a
        # scientific verdict from a malformed response.
        malformed = Models(change=lambda value, role: value.update(decision="FAIL") if role == 0 else None)
        result = self.assess(malformed)
        self.assertEqual(result.execution["outcome"], "protocol_failure")
        self.assertNotIn(result.execution.get("error_type"), {"TypeError"})
        stale = (datetime.now(UTC) - timedelta(days=2)).isoformat()
        state = retry_state("p", [row("protocol_failure", status="uncertain", at=stale)])
        self.assertTrue(state.eligible)

    def test_a_successful_assessment_is_no_longer_never_assessed(self):
        result = self.assess(Models())
        self.assertEqual(result.execution["outcome"], "success")
        stored = {"assessor_type": result.assessor_type,
                  "assessment_scope": result.assessment_scope,
                  "quality_status": result.quality_status, "execution": result.execution}
        self.assertTrue(is_completed_scientific_assessment(stored))
        self.assertFalse(retry_state("p", [stored]).eligible)


class RunBudgetBounds(unittest.TestCase):
    def test_default_limits_are_the_conservative_initial_policy(self):
        budget = RunBudget()
        self.assertEqual(budget.max_per_track, 1)
        self.assertEqual(budget.max_per_run, 3)
        self.assertEqual(budget.openrouter_ceiling_usd, 0.30)

    def test_one_paper_per_track(self):
        budget = RunBudget()
        budget.record("agent_memory", openrouter_usd=0.01)
        allowed, reason = budget.may_assess("agent_memory")
        self.assertFalse(allowed)
        self.assertEqual(reason, "track_paper_limit_reached")
        self.assertTrue(budget.may_assess("deep_research")[0])

    def test_run_total_is_capped(self):
        budget = RunBudget(max_per_track=3)
        for track in ("a", "b", "c"):
            budget.record(track, openrouter_usd=0.01)
        self.assertEqual(budget.may_assess("a")[1], "run_paper_limit_reached")

    def test_projection_past_the_ceiling_stops_the_run(self):
        budget = RunBudget()
        with self.assertRaises(CostCeilingExceeded):
            budget.reserve("agent_memory", 0.31)
        self.assertEqual(budget.stopped_reason, "openrouter_projection_exceeds_ceiling")

    def test_spend_reaching_the_ceiling_stops_further_papers(self):
        budget = RunBudget(max_per_track=5)
        budget.record("agent_memory", openrouter_usd=0.30)
        self.assertFalse(budget.may_assess("agent_memory")[0])
        self.assertEqual(budget.stopped_reason, "openrouter_ceiling_reached")

    def test_retry_cost_cannot_loop_unbounded(self):
        budget = RunBudget(max_per_track=100, max_per_run=100)
        attempts = 0
        while budget.may_assess("agent_memory")[0] and attempts < 1000:
            budget.record("agent_memory", openrouter_usd=0.05)
            attempts += 1
        self.assertLessEqual(attempts, 6)
        self.assertLessEqual(budget.openrouter_spend_usd, 0.35)

    def test_gemini_cost_is_recorded_as_tokens_and_never_as_money(self):
        budget = RunBudget()
        budget.record("agent_memory", gemini_calls=1, gemini_input_tokens=1000,
                      gemini_output_tokens=50)
        report = budget.to_dict()
        self.assertEqual(report["gemini_input_tokens"], 1000)
        self.assertEqual(report["gemini_monetary_cost"], "UNKNOWN / MSc allocation")

    def test_ceiling_from_env_fails_closed_on_a_bad_value(self):
        with self.assertRaises(ValueError):
            RunBudget.from_env({"PAPER_SCOUT_OPENROUTER_RUN_CEILING_USD": "free"})
        with self.assertRaises(ValueError):
            RunBudget.from_env({"PAPER_SCOUT_OPENROUTER_RUN_CEILING_USD": "-1"})
        self.assertEqual(RunBudget.from_env({}).openrouter_ceiling_usd, 0.30)


class CostAttribution(unittest.TestCase):
    """Unpriced and unattributed calls must be visible, never counted as free."""

    def usage(self, calls):
        from paper_scout.cli import _role_usage
        return _role_usage(type("A", (), {"execution": {"calls": calls}})())

    def test_provider_comes_from_the_pinned_model_map_not_the_model_name(self):
        # Stored receipts frequently carry no provider field at all.
        usage = self.usage([{"model": "gemini-3.8-flash",
                             "usage": {"prompt_tokens": 100, "completion_tokens": 10}},
                            {"model": "deepseek/deepseek-v4-pro-0813",
                             "usage": {"prompt_tokens": 200, "completion_tokens": 20,
                                       "cost": 0.03}}])
        self.assertEqual(usage["gemini_calls"], 1)
        self.assertEqual(usage["gemini_input"], 100)
        self.assertEqual(usage["openrouter_calls"], 1)
        self.assertAlmostEqual(usage["openrouter_usd"], 0.03)
        self.assertEqual(usage["unknown_cost_calls"], 0)
        self.assertEqual(usage["unattributed_calls"], 0)

    def test_an_unpriced_call_is_counted_not_treated_as_free(self):
        usage = self.usage([{"model": "deepseek/deepseek-v4-pro-0813",
                             "usage": {"prompt_tokens": 200, "completion_tokens": 20}}])
        self.assertEqual(usage["unknown_cost_calls"], 1)
        self.assertEqual(usage["openrouter_usd"], 0.0)

    def test_an_unrecognised_provider_is_flagged(self):
        usage = self.usage([{"model": "some/unmapped-model",
                             "usage": {"prompt_tokens": 1, "completion_tokens": 1}}])
        self.assertEqual(usage["unattributed_calls"], 1)
        self.assertEqual(usage["unknown_cost_calls"], 1)

    def test_a_zero_price_is_known_money_and_a_missing_price_is_not(self):
        priced = self.usage([{"model": "deepseek/deepseek-v4-pro-0813",
                              "usage": {"prompt_tokens": 1, "completion_tokens": 1,
                                        "cost": 0.0}}])
        self.assertEqual(priced["unknown_cost_calls"], 0)

    def test_reserve_is_a_pure_precheck_and_holds_no_state(self):
        """Nothing to release on a skip: reserve() only ever checks, never charges.

        This is the semantics the None path in _assess_selected depends on. If reserve()
        ever starts holding a reservation, that path has to release it.
        """
        budget = RunBudget(max_per_track=3, max_per_run=3)
        budget.reserve("agent_memory")
        budget.reserve("agent_memory")
        self.assertEqual(budget.openrouter_spend_usd, 0.0)
        self.assertEqual(budget.total_assessed, 0)
        self.assertIsNone(budget.stopped_reason)

    def test_a_skip_before_any_call_charges_nothing(self):
        budget = RunBudget()
        budget.reserve("agent_memory")  # then assess_and_store_candidate returns None
        self.assertEqual(budget.openrouter_spend_usd, 0.0)
        self.assertTrue(budget.may_assess("agent_memory")[0])

    def test_a_failure_after_calls_may_have_started_charges_the_estimate(self):
        from paper_scout.operational_preflight import ESTIMATED_OPENROUTER_USD_PER_PAPER
        budget = RunBudget()
        budget.reserve("agent_memory")
        # The exception path in _assess_selected charges this, because the provider may
        # already have been billed for calls whose receipt never came back.
        budget.record("agent_memory", openrouter_usd=ESTIMATED_OPENROUTER_USD_PER_PAPER)
        self.assertAlmostEqual(budget.openrouter_spend_usd, ESTIMATED_OPENROUTER_USD_PER_PAPER)
        self.assertEqual(budget.total_assessed, 1)

    def test_the_estimate_keeps_a_full_run_under_the_ceiling(self):
        from paper_scout.operational_preflight import ESTIMATED_OPENROUTER_USD_PER_PAPER
        budget = RunBudget(max_per_track=1, max_per_run=MAX_PAPERS_PER_RUN)
        for track in ("agent_memory", "deep_research", "engram"):
            budget.reserve(track)
            budget.record(track, openrouter_usd=ESTIMATED_OPENROUTER_USD_PER_PAPER)
        self.assertLess(budget.openrouter_spend_usd, budget.openrouter_ceiling_usd)

    def test_metrics_surface_the_unpriced_counters(self):
        from paper_scout.operational_run import OperationalMetrics
        metrics = OperationalMetrics()
        metrics.unknown_cost_calls = 2
        metrics.unattributed_calls = 1
        cost = metrics.to_dict()["cost"]
        self.assertEqual(cost["unknown_cost_calls"], 2)
        self.assertEqual(cost["unattributed_calls"], 1)
        self.assertEqual(cost["gemini_monetary_cost"], "UNKNOWN / MSc allocation")


class OperationalSelection(unittest.TestCase):
    """Selection uses the completed-assessment predicate and never moves a track's quota."""

    def test_engram_quota_is_not_transferred(self):
        from paper_scout.operational_run import MAX_PAPERS_PER_RUN as run_cap
        self.assertEqual(MAX_PAPERS_PER_TRACK, 1)
        self.assertEqual(run_cap, MAX_PAPERS_PER_RUN)
        # A track with nothing eligible contributes nothing; it cannot lend its slot,
        # because the per-track ceiling is enforced per track rather than globally.
        budget = RunBudget()
        budget.record("agent_memory", openrouter_usd=0.0)
        budget.record("deep_research", openrouter_usd=0.0)
        self.assertFalse(budget.may_assess("agent_memory")[0])
        self.assertFalse(budget.may_assess("deep_research")[0])
        self.assertTrue(budget.may_assess("engram")[0])
        self.assertEqual(budget.total_assessed, 2)


class PrivateStateSnapshot(unittest.TestCase):
    """Snapshot integrity, first-run semantics and every fail-closed path."""

    def make_state(self, root: Path, tracks=STATE_PATHS):
        for name in tracks:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            PaperStore(path)
        return root

    def test_roundtrip_restores_every_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            archive = Path(tmp) / "state.tar.gz"
            manifest = pack_snapshot(archive, root=source)
            self.assertEqual(manifest["version"], CURRENT_MANIFEST_VERSION)
            self.assertEqual(list(manifest["databases"]), list(STATE_PATHS))
            self.assertIn("created_at", manifest)
            self.assertIn("source", manifest)
            target = Path(tmp) / "dst"
            target.mkdir()
            report: dict = {}
            restore_snapshot(archive, root=target, report=report)
            for name in STATE_PATHS:
                self.assertTrue((target / name).exists())
            self.assertEqual(set(report["verification"]["databases"]), set(STATE_PATHS))

    def test_manifest_records_row_counts_and_digests(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            manifest = pack_snapshot(Path(tmp) / "s.tar.gz", root=source)
            for name in STATE_PATHS:
                self.assertEqual(len(manifest["sha256"][name]), 64)
                self.assertIn("paper_quality_assessments", manifest["row_counts"][name])

    def test_corrupt_database_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            archive = Path(tmp) / "state.tar.gz"
            pack_snapshot(archive, root=source)
            broken = Path(tmp) / "broken.tar.gz"
            with tarfile.open(archive, "r:gz") as src, tarfile.open(broken, "w:gz") as dst:
                for member in src.getmembers():
                    data = src.extractfile(member).read()
                    if member.name == STATE_PATHS[0]:
                        data = b"not a sqlite database" + data[21:]
                    member.size = len(data)
                    dst.addfile(member, __import__("io").BytesIO(data))
            target = Path(tmp) / "dst"
            target.mkdir()
            with self.assertRaises(ValueError):
                restore_snapshot(broken, root=target)
            self.assertFalse((target / STATE_PATHS[0]).exists())

    def test_partial_snapshot_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            archive = Path(tmp) / "state.tar.gz"
            pack_snapshot(archive, root=source)
            partial = Path(tmp) / "partial.tar.gz"
            with tarfile.open(archive, "r:gz") as src, tarfile.open(partial, "w:gz") as dst:
                for member in src.getmembers():
                    if member.name == STATE_PATHS[2]:
                        continue
                    dst.addfile(member, src.extractfile(member))
            with self.assertRaises(ValueError):
                restore_snapshot(partial, root=Path(tmp) / "dst")

    def test_wrong_manifest_hash_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            archive = Path(tmp) / "state.tar.gz"
            pack_snapshot(archive, root=source)
            tampered = Path(tmp) / "tampered.tar.gz"
            with tarfile.open(archive, "r:gz") as src, tarfile.open(tampered, "w:gz") as dst:
                for member in src.getmembers():
                    data = src.extractfile(member).read()
                    if member.name == MANIFEST:
                        manifest = json.loads(data)
                        manifest["sha256"][STATE_PATHS[0]] = "0" * 64
                        data = json.dumps(manifest).encode()
                        member.size = len(data)
                    dst.addfile(member, __import__("io").BytesIO(data))
            with self.assertRaises(ValueError):
                restore_snapshot(tampered, root=Path(tmp) / "dst")

    def test_unexpected_member_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            archive = Path(tmp) / "state.tar.gz"
            pack_snapshot(archive, root=source)
            hostile = Path(tmp) / "hostile.tar.gz"
            with tarfile.open(archive, "r:gz") as src, tarfile.open(hostile, "w:gz") as dst:
                for member in src.getmembers():
                    dst.addfile(member, src.extractfile(member))
                info = tarfile.TarInfo("../escape.sh")
                payload = b"#!/bin/sh\n"
                info.size = len(payload)
                dst.addfile(info, __import__("io").BytesIO(payload))
            with self.assertRaises(ValueError):
                restore_snapshot(hostile, root=Path(tmp) / "dst")

    def test_non_empty_state_is_never_replaced_by_an_empty_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            target = self.make_state(Path(tmp) / "dst")
            with closing(sqlite3.connect(target / STATE_PATHS[0])) as db:
                db.execute("INSERT INTO notifications (canonical_key, digest_date,"
                           " notified_at) VALUES ('keep', '2026-09-19', '2026-09-19T00:00:00')")
                db.commit()
            before = (target / STATE_PATHS[0]).read_bytes()
            archive = Path(tmp) / "state.tar.gz"
            pack_snapshot(archive, root=source)
            # A legitimate empty snapshot does overwrite; what must never happen is an
            # overwrite that was not verified. Corrupt the archive and confirm the
            # populated database survives untouched.
            broken = Path(tmp) / "broken.tar.gz"
            with tarfile.open(archive, "r:gz") as src, tarfile.open(broken, "w:gz") as dst:
                for member in src.getmembers():
                    data = src.extractfile(member).read()
                    if member.name == STATE_PATHS[1]:
                        data = b"corrupt"
                        member.size = len(data)
                    dst.addfile(member, __import__("io").BytesIO(data))
            with self.assertRaises(ValueError):
                restore_snapshot(broken, root=target)
            self.assertEqual((target / STATE_PATHS[0]).read_bytes(), before)

    def test_older_v1_snapshot_still_restores(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            archive = Path(tmp) / "state.tar.gz"
            manifest = pack_snapshot(archive, root=source)
            legacy = Path(tmp) / "v1.tar.gz"
            v1 = json.dumps({"version": 1, "sha256": manifest["sha256"]},
                            sort_keys=True).encode()
            with tarfile.open(archive, "r:gz") as src, tarfile.open(legacy, "w:gz") as dst:
                for member in src.getmembers():
                    if member.name == MANIFEST:
                        member.size = len(v1)
                        dst.addfile(member, __import__("io").BytesIO(v1))
                    else:
                        dst.addfile(member, src.extractfile(member))
            target = Path(tmp) / "dst"
            target.mkdir()
            restore_snapshot(legacy, root=target)
            for name in STATE_PATHS:
                self.assertTrue((target / name).exists())

    def test_snapshot_refuses_an_unflushed_wal(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_state(Path(tmp) / "src")
            wal = Path(str(source / STATE_PATHS[0]) + "-wal")
            wal.write_bytes(b"pending")
            with self.assertRaises(ValueError):
                pack_snapshot(Path(tmp) / "s.tar.gz", root=source)


class PrivateDestinationGuards(unittest.TestCase):
    """The transport must refuse anything that is not a verified private destination."""

    def script(self):
        import importlib.util
        path = Path(__file__).resolve().parents[1] / ".github/scripts/paper_scout_state.py"
        spec = importlib.util.spec_from_file_location("paper_scout_state", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_unset_destination_is_an_error(self):
        module = self.script()
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(module.StateError):
                module._destination()

    def test_public_repository_is_refused(self):
        module = self.script()
        env = {"PAPER_SCOUT_STATE_REPO": module.PUBLIC_REPO,
               "PAPER_SCOUT_STATE_TOKEN": "synthetic"}
        with patch.dict("os.environ", env, clear=True):
            with self.assertRaises(module.StateError) as caught:
                module._destination()
        self.assertIn("private", str(caught.exception))

    def test_missing_token_is_an_error(self):
        module = self.script()
        with patch.dict("os.environ", {"PAPER_SCOUT_STATE_REPO": "owner/state"}, clear=True):
            with self.assertRaises(module.StateError):
                module._destination()

    def test_a_public_destination_repo_is_refused_before_any_write(self):
        module = self.script()
        completed = type("R", (), {"returncode": 0, "stdout": '{"isPrivate": false,'
                                                              ' "visibility": "PUBLIC"}',
                                   "stderr": ""})()
        with patch.object(module, "_run", return_value=completed):
            with self.assertRaises(module.StateError) as caught:
                module.assert_private("owner/state", "synthetic")
        self.assertIn("not private", str(caught.exception))

    def test_a_private_destination_is_accepted(self):
        module = self.script()
        completed = type("R", (), {"returncode": 0, "stdout": '{"isPrivate": true,'
                                                              ' "visibility": "PRIVATE"}',
                                   "stderr": ""})()
        with patch.object(module, "_run", return_value=completed):
            module.assert_private("owner/state", "synthetic")

    def test_missing_release_is_distinguished_from_an_access_failure(self):
        module = self.script()
        for stderr, missing in (("release not found", True),
                                ("HTTP 404: Not Found", True),
                                ("HTTP 403: Resource not accessible", False),
                                ("unauthorized", False),
                                ("dial tcp: connection refused", False),
                                ("", False)):
            with self.subTest(stderr=stderr):
                self.assertEqual(module._is_missing_release(stderr), missing)

    def test_explicit_initialize_creates_empty_state_only_when_none_exists(self):
        """--allow-initialize is the one path that may create empty databases."""
        module = self.script()
        private = type("R", (), {"returncode": 0, "stdout": '{"isPrivate": true,'
                                                            ' "visibility": "PRIVATE"}',
                                 "stderr": ""})()
        absent = type("R", (), {"returncode": 1, "stdout": "",
                                "stderr": "release not found (HTTP 404)"})()
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            env = {"PAPER_SCOUT_STATE_REPO": "owner/state",
                   "PAPER_SCOUT_STATE_TOKEN": "synthetic", "RUNNER_TEMP": tmp}
            try:
                import os
                os.chdir(tmp)
                with patch.dict("os.environ", env, clear=True), \
                     patch.object(module, "_run", side_effect=[private, absent]):
                    self.assertEqual(module.restore("tag", allow_initialize=True,
                                                    report_path=None), 0)
                for name in STATE_PATHS:
                    self.assertTrue(Path(tmp, name).exists(), name)
            finally:
                os.chdir(cwd)

    def test_persist_removes_the_plaintext_scratch_copy_when_verification_fails(self):
        """A failed round-trip must not leave the databases unpacked on the runner."""
        module = self.script()
        private = type("R", (), {"returncode": 0, "stdout": '{"isPrivate": true,'
                                                            ' "visibility": "PRIVATE"}',
                                 "stderr": ""})()
        with tempfile.TemporaryDirectory() as tmp:
            env = {"PAPER_SCOUT_STATE_REPO": "owner/state",
                   "PAPER_SCOUT_STATE_TOKEN": "synthetic", "RUNNER_TEMP": tmp}
            scratch = Path(tmp) / "paper-scout-state-verify"
            archive = Path(tmp) / module.ASSET_NAME
            with patch.dict("os.environ", env, clear=True), \
                 patch.object(module, "_run", return_value=private), \
                 patch.object(module, "pack_snapshot", return_value={"version": 2}), \
                 patch.object(module, "restore_snapshot",
                              side_effect=ValueError("snapshot checksum mismatch")):
                # Fail-closed shape: a StateError main() renders as ::error::, not a
                # raw traceback from deep inside the snapshot code.
                with self.assertRaises(module.StateError) as caught:
                    module.persist("tag", report_path=None)
                self.assertIn("round-trip verification", str(caught.exception))
            self.assertFalse(scratch.exists(), "scratch copy of the databases was left behind")
            self.assertFalse(archive.exists(), "plaintext archive was left behind")

    def test_state_hash_outputs_are_labelled_by_track_not_by_directory(self):
        module = self.script()
        self.assertEqual(module._track_label("data/paper_scout.sqlite3"), "agent_memory")
        self.assertEqual(module._track_label("data/deep_research/paper_scout.sqlite3"),
                         "deep_research")
        self.assertEqual(module._track_label("data/engram/paper_scout.sqlite3"), "engram")
        # Every packed database must have a label, or a consumer keyed on the track name
        # silently reads nothing.
        for name in STATE_PATHS:
            self.assertIn(name, module.TRACK_FOR_STATE_PATH)

    def test_permission_error_fails_instead_of_claiming_a_new_track(self):
        """A 403 must not be read as "no snapshot yet" and must not initialize state.

        Ported from the retired public-release transport test. Confusing an access
        failure with an absent snapshot is how a healthy history gets replaced by empty
        databases, so the two must stay distinguishable.
        """
        module = self.script()
        denied = type("R", (), {"returncode": 1, "stdout": "",
                                "stderr": "HTTP 403: Resource not accessible"})()
        private = type("R", (), {"returncode": 0, "stdout": '{"isPrivate": true,'
                                                            ' "visibility": "PRIVATE"}',
                                 "stderr": ""})()
        env = {"PAPER_SCOUT_STATE_REPO": "owner/state", "PAPER_SCOUT_STATE_TOKEN": "synthetic"}
        # Even with --allow-initialize the 403 must fail: it is not an absent snapshot.
        for allow in (False, True):
            with self.subTest(allow_initialize=allow):
                with patch.dict("os.environ", env, clear=True), \
                     patch.object(module, "_run", side_effect=[private, denied]):
                    with self.assertRaises(module.StateError) as caught:
                        module.restore("tag", allow_initialize=allow, report_path=None)
                self.assertIn("cannot determine", str(caught.exception).lower())

    def test_download_failure_after_a_found_release_fails_closed(self):
        module = self.script()
        private = type("R", (), {"returncode": 0, "stdout": '{"isPrivate": true,'
                                                            ' "visibility": "PRIVATE"}',
                                 "stderr": ""})()
        found = type("R", (), {"returncode": 0, "stdout": '{"id": 1}', "stderr": ""})()
        failed = type("R", (), {"returncode": 1, "stdout": "", "stderr": "network error"})()
        env = {"PAPER_SCOUT_STATE_REPO": "owner/state", "PAPER_SCOUT_STATE_TOKEN": "synthetic"}
        with patch.dict("os.environ", env, clear=True), \
             patch.object(module, "_run", side_effect=[private, found, failed]):
            with self.assertRaises(module.StateError):
                module.restore("tag", allow_initialize=True, report_path=None)

    def test_missing_snapshot_without_explicit_initialize_fails_closed(self):
        module = self.script()
        missing = type("R", (), {"returncode": 1, "stdout": "",
                                 "stderr": "release not found"})()
        private = type("R", (), {"returncode": 0, "stdout": '{"isPrivate": true,'
                                                            ' "visibility": "PRIVATE"}',
                                 "stderr": ""})()
        env = {"PAPER_SCOUT_STATE_REPO": "owner/state", "PAPER_SCOUT_STATE_TOKEN": "synthetic"}
        with patch.dict("os.environ", env, clear=True), \
             patch.object(module, "_run", side_effect=[private, missing]):
            with self.assertRaises(module.StateError) as caught:
                module.restore("tag", allow_initialize=False, report_path=None)
        self.assertIn("Refusing to continue", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
