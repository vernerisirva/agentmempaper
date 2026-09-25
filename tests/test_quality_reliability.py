from dataclasses import replace
from datetime import UTC, datetime, timedelta
from email.utils import format_datetime
from http.client import IncompleteRead
import json
from pathlib import Path
import tempfile
import socket
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from test_paper_scout_scientific_gate import candidate, manuscript
from paper_scout.full_text import ExtractedPage, FullTextDocument, SelectedPaperText, SelectedSection, select_assessment_text, _detect_sections
from paper_scout.http import HttpClient, HttpRequestError, retry_after_seconds
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_llm import assess_with_optional_quality_llm, locate_evidence, _request_payload
from paper_scout.quality_models import QualityAssessment, QualityEvidence, QUALITY_DIMENSIONS

ENV = {"PAPER_SCOUT_LLM_PROVIDER": "openrouter", "PAPER_SCOUT_LLM_API_KEY": "test-only-key",
       "PAPER_SCOUT_LLM_MODEL": "test-model", "PAPER_SCOUT_LLM_BASE_URL": "https://openrouter.ai/api/v1",
       "PAPER_SCOUT_QUALITY_LLM_REASONING": "off"}


def block_fixture(value=None):
    from paper_scout.evidence_context import build_evidence_context, EVIDENCE_VERSION
    selected, original = manuscript()
    value = original if value is None else value
    if 'evidence_schema_version' in value:
        return value
    context = build_evidence_context('fixture', selected)
    evidence = []
    for e in value.get('evidence', []):
        ids = [b.evidence_id for b in context.blocks if b.spans[0].section == e.get('section')]
        evidence.append({'dimension': e['dimension'], 'signal_type': e['signal_type'],
            'claim': e['paraphrase'], 'explanation': e['explanation'],
            'support_status': 'supported', 'evidence_ids': ids, 'statement_kind': 'source_claim'})
    return {**{k: value[k] for k in ('quality_status', 'quality_rationale', 'quality_uncertainty',
                                   'overall_quality_score', 'confidence', 'paper_type')},
            'evidence_schema_version': EVIDENCE_VERSION, 'evidence_context_id': context.context_id,
            'uncertainty_reason': value.get('uncertainty_reason'), 'evidence': evidence,
            'dimension_scores': {d: (value.get('dimension_scores') or {}).get(d, 4) for d in QUALITY_DIMENSIONS}}


def envelope(value=None, finish="stop"):
    return json.dumps({"id": "fixture-request", "usage": {"prompt_tokens": 123, "completion_tokens": 55, "cost": 0.01},
                       "choices": [{"finish_reason": finish, "message": {"content": json.dumps(block_fixture(value))}}]})


class SequenceHttp:
    def __init__(self, responses):
        self.responses = list(responses)
        self.payloads = []
        self.verifier_payloads = []

    def post_json(self, url, payload, headers=None):
        if payload['response_format']['json_schema']['name'] == 'claim_support':
            self.verifier_payloads.append(payload)
            items = json.loads(payload['messages'][1]['content'])['items']
            content = {'items': [{'item_id': v['item_id'], 'status': 'supported', 'reason': 'Mocked scoped support.'} for v in items]}
            return json.dumps({'usage': {'prompt_tokens': 50, 'completion_tokens': 25, 'cost': 0.005},
                'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(content)}}]})
        self.payloads.append(payload)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


class ReliabilityTest(unittest.TestCase):
    def assess(self, client):
        text, _ = manuscript()
        with patch.dict("os.environ", ENV, clear=True), patch("paper_scout.quality_llm.time.sleep") as sleep:
            result = assess_with_optional_quality_llm(candidate(), text,
                assess_quality_deterministically(candidate(), "fixture", text), "llm", http=client)
        self.assertEqual(QualityAssessment.from_dict(result.to_dict()), result)
        return result, sleep

    def test_transient_retry_recovers_same_model_with_ledger(self):
        for kind in ("dns", "network", "timeout", "incomplete_response", "connection_error"):
            client = SequenceHttp([HttpRequestError(kind, "https://example.test", "fixture"), envelope()])
            result, sleep = self.assess(client)
            self.assertEqual(result.quality_status, "pass")
            self.assertEqual(result.execution["outcome"], "scientific")
            self.assertEqual([c["kind"] for c in result.execution["calls"]], ["initial", "retry"] + ["verifier"]*7)
            self.assertIsNone(result.execution["calls"][0]["usage"]["cost_usd"])
            sleep.assert_called_once_with(2.0)
            self.assertEqual(client.payloads[0], client.payloads[1])
            self.assertEqual(client.payloads[0]["response_format"]["type"], "json_schema")
            self.assertEqual(client.payloads[0]["provider"], {"require_parameters": True})
            self.assertEqual(client.payloads[0]["reasoning"], {"enabled": False, "exclude": True})

    def test_exhaustion_has_two_calls_and_never_insufficient(self):
        error = HttpRequestError("timeout", "https://example.test", "fixture")
        result, _ = self.assess(SequenceHttp([error, error]))
        self.assertEqual(result.quality_status, "uncertain")
        self.assertEqual(result.execution["outcome"], "transport_failure")
        self.assertFalse(result.full_text_assessed)
        self.assertEqual(len(result.execution["calls"]), 2)

    def test_retry_after_respected_or_deferred_without_early_retry(self):
        for status, delay, count in ((429, 5, 2), (503, 12, 2), (429, 120, 1), (403, None, 1)):
            result, sleep = self.assess(SequenceHttp([
                HttpRequestError("http", "https://example.test", "fixture", status_code=status, retry_after_seconds=delay), envelope()]))
            self.assertEqual(len(result.execution["calls"]), count + 7*(result.quality_status == "pass"))
            if count == 2:
                sleep.assert_called_once_with(float(delay))
            else:
                sleep.assert_not_called()
                self.assertEqual(result.quality_status, "uncertain")

    def test_retry_after_date_seconds_invalid(self):
        self.assertEqual(retry_after_seconds("7"), 7)
        self.assertIsNone(retry_after_seconds("invalid"))
        date = format_datetime(datetime.now(UTC) + timedelta(seconds=30), usegmt=True)
        self.assertTrue(28 <= retry_after_seconds(date) <= 30)

    def test_real_http_wraps_original_incomplete_body_dns_and_status(self):
        for exc, kind, status, delay in ((IncompleteRead(b"partial"), "incomplete_response", None, None),
                (URLError(socket.gaierror(8, "fixture DNS")), "dns", None, None),
                (ConnectionResetError("fixture reset"), "connection_error", None, None),
                (HTTPError("https://example.test", 429, "fixture", {"Retry-After": "9"}, None), "http", 429, 9)):
            with patch("paper_scout.http.urlopen", side_effect=exc) as request:
                with self.assertRaises(HttpRequestError) as caught:
                    HttpClient(retries=1).post_json("https://example.test", {})
            request.assert_called_once()
            self.assertEqual((caught.exception.kind, caught.exception.status_code, caught.exception.retry_after_seconds), (kind, status, delay))

    def test_malformed_and_schema_invalid_responses_fail_closed_without_repair(self):
        invalid = {**manuscript()[1], "confidence": "absolutely", "quality_status": "insufficient"}
        for raw in ("not-json", envelope(invalid), '{"choices":[]}',
                    json.dumps({"choices": [{"message": {"content": '{"quality_status":"insufficient",'}}]})):
            result, sleep = self.assess(SequenceHttp([raw]))
            self.assertEqual(result.quality_status, "uncertain")
            self.assertEqual(result.execution["outcome"], "protocol_failure")
            self.assertFalse(result.full_text_assessed)
            self.assertEqual(len(result.execution["calls"]), 1)
            sleep.assert_not_called()

    def test_provider_error_envelope_retries_and_preserves_usage(self):
        result, _ = self.assess(SequenceHttp([json.dumps({"error": {"code": 503}}), envelope()]))
        self.assertEqual(result.quality_status, "pass")
        self.assertEqual(result.execution["calls"][0]["http_status"], 503)

    def test_no_hidden_nested_retries(self):
        with self.assertRaises(ValueError):
            self.assess(HttpClient(retries=3))

    def test_reasoning_switch_is_scoped_to_exact_openrouter_host(self):
        text, _ = manuscript()
        for base, expected in (("https://OPENROUTER.AI/api/v1", True), ("https://api.openai.com/v1", False), ("https://openrouter.ai.example.com/v1", False)):
            client = SequenceHttp([envelope()])
            with patch.dict("os.environ", {**ENV, "PAPER_SCOUT_LLM_BASE_URL": base}, clear=True):
                assess_with_optional_quality_llm(candidate(), text, assess_quality_deterministically(candidate(), "fixture", text), "llm", http=client)
            self.assertEqual("reasoning" in client.payloads[0], expected)

    def test_telemetry_does_not_include_content_or_credentials(self):
        with self.assertLogs("paper_scout.quality_llm", level="INFO") as logs:
            result, _ = self.assess(SequenceHttp([envelope(finish="length"), envelope(finish="length")]))
        output = json.dumps(result.execution) + " ".join(logs.output)
        self.assertNotIn("test-only-key", output)
        self.assertNotIn(manuscript()[1]["quality_rationale"], output)
        self.assertEqual(result.execution["calls"][0]["finish_reason"], "length")


class AnchorRegressionTest(unittest.TestCase):
    def anchor(self, quote, text, page=2, sections=None):
        e = QualityEvidence("methodological_rigor", "positive", "Evidence", "Fixture", page=page, excerpt=quote)
        selected = SelectedPaperText(text, sections or [SelectedSection("Methods", text, 2)], "partial_full_text", "hash", False)
        return locate_evidence(e, selected)

    def test_real_as_if_pdf_line_hyphenation_and_parenthesis_spacing(self):
        # Calibration: doi:10.1007/s44206-026-00290-2, extracted body fragments.
        self.assertIsNotNone(self.anchor("methodological", "methodologi -\ncal"))
        self.assertIsNotNone(self.anchor("answerable", "answer -\nable"))
        self.assertIsNotNone(self.anchor("(2019)", "( 2019)"))

    def test_unicode_ligature_quotes_and_line_wrapping(self):
        self.assertIsNotNone(self.anchor('"specific operation"', '“speciﬁc\n  operation”'))
        self.assertIsNotNone(self.anchor("long-term", "long‑term"))

    def test_nearby_semantic_changes_numbers_negation_and_glued_words_rejected(self):
        for quote, text in (("private and shared memory", "both private and shared memories"),
                ("experiment trajectories", "execution trajectories"),
                ("81% accuracy", "18% accuracy"), ("is supported", "is not supported"),
                ("not able", "notable"), ("a;b", "a; intervening clause; b"),
                ("first ... last", "first middle last"), ("stateoftheart", "state-of-the-art"), ("x2", "x²"), ("R", "ℝ")):
            self.assertIsNone(self.anchor(quote, text), (quote, text))

    def test_unique_localization_corrects_page_and_records_actual_section(self):
        result = self.anchor("Exact body quote.", "Exact body quote.", page=22)
        self.assertEqual((result.page, result.section), (2, "Methods"))
        sections = [SelectedSection("Methods", "Same quote", 2), SelectedSection("Results", "Same quote", 3)]
        self.assertIsNone(self.anchor("Same quote", "Same quote", page=22, sections=sections))

    def test_abstract_and_text_outside_prompt_never_qualify(self):
        self.assertIsNone(self.anchor("abstract quote", "abstract quote", sections=[SelectedSection("Abstract", "abstract quote", 2)]))
        self.assertIsNone(self.anchor("hidden quote", "visible quote", sections=[SelectedSection("Methods", "hidden quote", 2)]))

    def test_real_numbered_headings_end_abstract_without_accepting_abstract_lists(self):
        pages = [ExtractedPage(1, "Abstract\nSummary.\n1. An Abstract List Item\nMore summary.\n1. Introduction: The Portability Assumption\nBody claim.\n2. The HibriMind Frame\nBody method.")]
        sections = _detect_sections(pages)
        self.assertEqual([s.heading for s in sections], ["Abstract", "Introduction", "The Hibrimind Frame"])
        self.assertIn("An Abstract List Item", sections[0].text)
        doc = FullTextDocument("https://example.test/p.pdf", pages, "hash", True)
        selected = select_assessment_text(candidate(), doc)
        self.assertIn("Body method.", selected.text)
        self.assertIsNotNone(self.anchor("Body method.", selected.text, page=1, sections=selected.sections))


class JatsTest(unittest.TestCase):
    def test_public_jats_retains_body_sections_source_hash_and_logical_location_warning(self):
        from paper_scout.full_text import _extract_jats, _public_jats_url
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13573717/fullTextXML"
        payload = b'<article><front><abstract>Abstract only</abstract></front><body><sec><title>1.Introduction</title><p>A body claim.</p></sec><sec><title>Descriptive Heading</title><p>Body <italic>evidence</italic>.</p></sec></body></article>'
        self.assertTrue(_public_jats_url(url))
        self.assertFalse(_public_jats_url(url.replace("www.ebi.ac.uk", "www.ebi.ac.uk.example.test")))
        document = _extract_jats(payload, url, 10, 1000)
        selected = select_assessment_text(candidate(), document)
        self.assertTrue(document.complete)
        self.assertEqual(document.source_url, url)
        self.assertIn("not PDF pages", selected.warnings[0])
        self.assertNotIn("Abstract only", selected.text)
        self.assertTrue(any(s.heading == "Descriptive Heading" and s.first_page == 2 for s in selected.sections))
        self.assertFalse(_extract_jats(payload, url, 1, 1000).complete)
        self.assertFalse(_extract_jats(payload, url, 10, 30).complete)
        for invalid in (b'<html/>', b'<article><body/></article>', b'<!DOCTYPE article><article/>'):
            with self.assertRaises(ValueError):
                _extract_jats(invalid, url, 10, 1000)

    def test_public_jats_fetch_round_trip_uses_normal_full_text_cache(self):
        from paper_scout.full_text import fetch_and_extract_pdf
        from paper_scout.config import QualityFullTextConfig
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13573717/fullTextXML"
        payload = b'<article><body><sec><title>Methods</title><p>Manuscript evidence.</p></sec></body></article>'
        with tempfile.TemporaryDirectory() as temp, patch("paper_scout.full_text._download_pdf", return_value=(payload, "application/xml")) as download:
            settings = QualityFullTextConfig(cache_dir=Path(temp))
            first = fetch_and_extract_pdf(url, settings)
            second = fetch_and_extract_pdf(url, settings)
        download.assert_called_once()
        self.assertEqual(first.pages, second.pages)
        self.assertTrue(second.cache_hit)


class ProviderContractTest(unittest.TestCase):
    def test_strict_schema_accepts_explicit_null_optional_locations(self):
        from jsonschema import Draft202012Validator
        from paper_scout.quality_llm import _strict_schema, quality_review_schema
        schema = _strict_schema(quality_review_schema())
        Draft202012Validator.check_schema(schema)
        value = {**manuscript()[1], "quality_status": "uncertain", "uncertainty_reason": None, "dimension_scores": {},
                 "positive_signals": [], "concerns": [], "missing_information": [], "concise_summary": ""}
        for key in schema["properties"]["dimension_scores"]["properties"]:
            value["dimension_scores"][key] = None
        for evidence in value["evidence"]:
            evidence.update(page=None, section=None, excerpt=None)
        Draft202012Validator(schema).validate(value)
        Draft202012Validator(quality_review_schema()).validate(value)

    def test_recovered_retry_counts_one_failed_and_one_successful_attempt(self):
        client = SequenceHttp([HttpRequestError("incomplete_response", "https://example.test", "fixture"), envelope()])
        result, _ = ReliabilityTest().assess(client)
        calls = result.execution["calls"]
        self.assertEqual(len(client.payloads), 2)
        self.assertEqual([c["status"] for c in calls], ["failed", "success"] + ["success"]*7)
        self.assertEqual(sum(c["usage"]["cost_usd"] or 0 for c in calls), 0.045)
        self.assertEqual(sum(c["usage"]["cost_usd"] is None for c in calls), 1)

    def test_deploy_only_keeps_site_validation_before_deployment(self):
        import yaml
        root = Path(__file__).resolve().parents[1]
        workflow = yaml.load((root / ".github/workflows/paper-scout.yml").read_text(), Loader=yaml.BaseLoader)
        self.assertEqual(workflow["on"]["workflow_dispatch"]["inputs"]["deploy_only"]["type"], "boolean")
        self.assertEqual(workflow["on"]["workflow_dispatch"]["inputs"]["deploy_only"]["default"], "false")
        steps = workflow["jobs"]["scout"]["steps"]
        by_name = {s["name"]: s for s in steps}
        for name in ("Restore private Paper Scout state", "Run discovery and metadata update",
                     "Commit scout updates", "Bounded scientific assessment",
                     "Scientific credential preflight"):
            self.assertIn("!inputs.deploy_only", by_name[name]["if"])
        validation = by_name["Validate generated schemas, links, and runtime exclusion"]
        self.assertNotIn("if", validation)
        self.assertLess(steps.index(validation), steps.index(by_name["Deploy to GitHub Pages"]))
        self.assertEqual(by_name["Deploy to GitHub Pages"]["if"], "success()")

    def test_operational_workflow_invariants(self):
        """The workflow-level guarantees the operationalization depends on."""
        import yaml
        root = Path(__file__).resolve().parents[1]
        text = (root / ".github/workflows/paper-scout.yml").read_text()
        workflow = yaml.load(text, Loader=yaml.BaseLoader)
        steps = workflow["jobs"]["scout"]["steps"]
        by_name = {s["name"]: s for s in steps}

        # The schedule is live. What must not drift are the bounds it runs under.
        self.assertEqual(workflow["on"]["schedule"], [{"cron": "0 4 * * 1-5"}])
        from paper_scout.operational_preflight import (
            DEFAULT_OPENROUTER_RUN_CEILING_USD, MAX_PAPERS_PER_RUN, MAX_PAPERS_PER_TRACK)
        from paper_scout.batch_population import TRACKS
        self.assertEqual(MAX_PAPERS_PER_TRACK, 1)
        # One slot per track and no transfer between them, so the run ceiling is exactly
        # the track count. A raise that is not a new track is a policy change, not drift.
        self.assertEqual(MAX_PAPERS_PER_RUN, len(TRACKS))
        self.assertEqual(MAX_PAPERS_PER_RUN, 4)
        # Adding the fourth track did not buy more money. The ceiling is unchanged.
        self.assertEqual(DEFAULT_OPENROUTER_RUN_CEILING_USD, 0.30)

        # Discovery must not be able to enter the scientific gate: it neither receives a
        # scientific credential nor runs the assessment queue.
        discovery = by_name["Run discovery and metadata update"]
        self.assertNotIn("GEMINI_API_KEY", discovery.get("env", {}))
        self.assertNotIn("OPENROUTER_API_KEY", discovery.get("env", {}))
        for track in TRACKS:
            self.assertIn(f"run --track {track} --no-llm", discovery["run"])

        # Assessment runs behind the RUN_ASSESSMENT gate and a passing preflight, and
        # carries the per-run cost ceiling.
        assess = by_name["Bounded scientific assessment"]
        self.assertIn("env.RUN_ASSESSMENT == 'true'", assess["if"])
        self.assertEqual(assess["env"]["PAPER_SCOUT_OPENROUTER_RUN_CEILING_USD"], "0.30")
        preflight = by_name["Scientific credential preflight"]
        self.assertLess(steps.index(preflight), steps.index(assess))

        # The preflight gates the assessment stage; it must not fail the job. A failed
        # job skips the if: success() persist step, so a missing secret would cost the
        # run's discovery as well as its assessment.
        self.assertIn("steps.preflight.outputs.ok == 'true'", assess["if"])

        # The defect this pins: `inputs` is null on a schedule trigger, so gating the
        # scientific steps on inputs.run_assessment alone made every scheduled run skip
        # the assessment it exists to perform. Run 35508285811 did exactly that.
        gate = workflow["jobs"]["scout"]["env"]["RUN_ASSESSMENT"]
        self.assertIn("github.event_name == 'schedule'", gate)
        for step in ("Scientific credential preflight", "Bounded scientific assessment"):
            self.assertNotIn("inputs.run_assessment", by_name[step]["if"],
                             f"{step} must not gate on inputs alone; it is null on a schedule")
        self.assertNotIn("sys.exit(1)", preflight["run"])
        self.assertIn("::error::", preflight["run"])

        # State is restored and verified before anything reads it, and persisted before
        # Pages so a deployment failure cannot strand it.
        self.assertLess(steps.index(by_name["Restore private Paper Scout state"]),
                        steps.index(by_name["Run discovery and metadata update"]))
        self.assertLess(steps.index(by_name["Verify restored state integrity"]),
                        steps.index(by_name["Run discovery and metadata update"]))
        self.assertLess(steps.index(by_name["Persist private Paper Scout state"]),
                        steps.index(by_name["Deploy to GitHub Pages"]))

        # No public-release transport may return.
        self.assertNotIn("gh release upload", text)
        self.assertNotIn("download-paper-scout-state", text)
        self.assertIn("PAPER_SCOUT_STATE_REPO", text)

        # The state PAT reaches only the two steps that invoke the transport. A
        # workflow- or job-level env block would hand it to every third-party action in
        # the job, which is a far wider blast radius than the transport needs.
        self.assertNotIn("PAPER_SCOUT_STATE_TOKEN", (workflow.get("env") or {}))
        self.assertNotIn("PAPER_SCOUT_STATE_TOKEN", (workflow["jobs"]["scout"].get("env") or {}))
        carrying = [s["name"] for s in steps if "PAPER_SCOUT_STATE_TOKEN" in (s.get("env") or {})]
        self.assertEqual(sorted(carrying), ["Persist private Paper Scout state",
                                            "Restore private Paper Scout state"])
        for name in carrying:
            self.assertIn("paper_scout_state.py", by_name[name]["run"])

    def test_a_scheduled_run_would_reach_the_assessment_steps(self):
        """Evaluate the real gate expression under both trigger shapes.

        On a schedule GitHub supplies no `inputs`, which is precisely what made the
        deployed gate evaluate false on every scheduled run.
        """
        import yaml
        root = Path(__file__).resolve().parents[1]
        workflow = yaml.load((root / ".github/workflows/paper-scout.yml").read_text(),
                             Loader=yaml.BaseLoader)
        gate = workflow["jobs"]["scout"]["env"]["RUN_ASSESSMENT"]

        # Pin the structure, not substrings: a pure disjunction of exactly these operands.
        # A substring check let `... || inputs.trigger == 'daily' && inputs.run_assessment`
        # pass, which would make the external trigger (it sends only trigger=daily) skip
        # assessment while reporting success.
        self.assertTrue(gate.startswith("${{ ") and gate.endswith(" }}"), gate)
        body = gate[4:-3]
        self.assertNotIn("&&", body)
        self.assertNotIn("!", body.replace("!=", ""))
        self.assertEqual({operand.strip() for operand in body.split("||")},
                         {"github.event_name == 'schedule'", "inputs.trigger == 'daily'",
                          "inputs.run_assessment"})

    def test_the_daily_guard_gates_the_whole_scout_job(self):
        """Two daily triggers must not both reach the scientific stage on one day."""
        import yaml
        root = Path(__file__).resolve().parents[1]
        workflow = yaml.load((root / ".github/workflows/paper-scout.yml").read_text(),
                             Loader=yaml.BaseLoader)
        guard_module = _load_daily_run_guard()
        daily = "github.event_name == 'schedule' || (inputs.trigger == 'daily' && !inputs.deploy_only)"
        self.assertEqual(workflow["env"]["IS_DAILY_RUN"], "${{ " + daily + " }}")
        # run-name cannot read env, so it repeats the dispatch half of the same condition.
        self.assertEqual(workflow["run-name"],
                         "${{ inputs.trigger == 'daily' && !inputs.deploy_only && "
                         f"'{guard_module.DAILY_TITLE}' || 'Paper Scout' }}}}")
        self.assertEqual(workflow["on"]["workflow_dispatch"]["inputs"]["trigger"]["default"], "manual")
        self.assertEqual(workflow["permissions"]["actions"], "read")

        guard = workflow["jobs"]["daily-guard"]
        self.assertEqual(guard["permissions"], {"actions": "read", "contents": "read"})
        self.assertEqual(guard["outputs"], {"skip": "${{ steps.guard.outputs.skip }}"})
        step = guard["steps"][-1]
        self.assertEqual(step["id"], "guard")
        self.assertEqual(step["run"], "python3 .github/scripts/daily_run_guard.py")
        self.assertNotIn("IS_DAILY_RUN", step["env"], "one definition, at workflow level")

        scout = workflow["jobs"]["scout"]
        self.assertEqual(scout["needs"], "daily-guard")
        self.assertEqual(scout["if"], "${{ needs.daily-guard.outputs.skip != 'true' }}")
        self.assertNotIn("permissions", scout, "a job-level block would drop actions: read")
        names = [s["name"] for s in scout["steps"]]
        recheck = scout["steps"][names.index("Re-check the daily guard")]
        self.assertEqual(recheck["run"], "python3 .github/scripts/daily_run_guard.py --enforce")
        self.assertNotIn("if", recheck)
        # Before every step that writes state or spends money.
        for later in ("Restore private Paper Scout state", "Run discovery and metadata update",
                      "Scientific credential preflight", "Bounded scientific assessment",
                      "Commit scout updates", "Persist private Paper Scout state"):
            self.assertLess(names.index("Re-check the daily guard"), names.index(later), later)


    def test_both_scheduled_writers_share_one_concurrency_group(self):
        """Single-writer discipline is what makes two scheduled workflows safe."""
        import yaml
        root = Path(__file__).resolve().parents[1]
        groups = []
        for name in ("paper-scout.yml", "paper-scout-backfill.yml"):
            workflow = yaml.load((root / ".github/workflows" / name).read_text(),
                                 Loader=yaml.BaseLoader)
            concurrency = workflow["concurrency"]
            groups.append(concurrency["group"])
            # Cancelling mid-run could abandon state between snapshot and persist.
            self.assertEqual(concurrency["cancel-in-progress"], "false")
            self.assertEqual(concurrency["queue"], "max")
        self.assertEqual(len(set(groups)), 1, "the two writers must serialize")

    def test_backfill_workflow_scopes_the_state_credential_too(self):
        import yaml
        root = Path(__file__).resolve().parents[1]
        workflow = yaml.load((root / ".github/workflows/paper-scout-backfill.yml").read_text(),
                             Loader=yaml.BaseLoader)
        self.assertEqual(workflow["on"]["schedule"], [{"cron": "40 5 * * 0"}])
        job = workflow["jobs"]["backfill"]
        self.assertNotIn("PAPER_SCOUT_STATE_TOKEN", (workflow.get("env") or {}))
        self.assertNotIn("PAPER_SCOUT_STATE_TOKEN", (job.get("env") or {}))
        carrying = [s["name"] for s in job["steps"]
                    if "PAPER_SCOUT_STATE_TOKEN" in (s.get("env") or {})]
        self.assertEqual(len(carrying), 2)
        # Backfill must not run the scientific gate either.
        commands = "\n".join(s.get("run", "") for s in job["steps"])
        self.assertIn("backfill --track agent_memory --days 45 --no-notify --no-llm", commands)
        self.assertIn("backfill --track engram --days 45 --no-notify --no-llm", commands)


class SelectionCoverageTest(unittest.TestCase):
    def test_descriptive_methods_and_results_precede_long_conclusion_continuations(self):
        # Regression shape from Mr.LHDR: descriptive body headings plus many
        # continuation pages previously labelled Conclusion consume the prompt.
        pages = [ExtractedPage(1, "Abstract\nSummary.\n1. Introduction\n" + "Background. " * 60),
                 ExtractedPage(2, "2. Quality Standards and Validation Protocol\nLocated methods evidence."),
                 ExtractedPage(3, "3. Overall Capability\nLocated results evidence."),
                 ExtractedPage(4, "Limitations\nOnly a scoped benchmark.\nConclusion\n" + "Closing. " * 200)]
        pages += [ExtractedPage(i, "Continuation. " * 200) for i in range(5, 15)]
        doc = FullTextDocument("https://example.test/p.pdf", pages, "hash", True)
        selected = select_assessment_text(candidate(), doc, max_prompt_characters=1800, max_section_characters=500)
        self.assertIn("Located methods evidence.", selected.text)
        self.assertIn("Located results evidence.", selected.text)
        self.assertGreater(selected.coverage["omitted_body_characters"], 0)
        self.assertEqual(selected.coverage["status"], "text_coverage_failure")
        self.assertLessEqual(len(selected.text), 1800)
        self.assertTrue(all(s.text in selected.text for s in selected.sections))
        self.assertEqual(selected.scope, "partial_full_text")

    def test_prompt_truncation_removes_unseen_section_text(self):
        doc = FullTextDocument("https://example.test/p.pdf", [ExtractedPage(1, "Introduction\n" + "body " * 2000)], "hash", True)
        selected = select_assessment_text(candidate(), doc, max_prompt_characters=400)
        self.assertLessEqual(len(selected.text), 400)
        self.assertTrue(all(s.text in selected.text for s in selected.sections))
        self.assertEqual(selected.scope, "partial_full_text")


class ReviewRegressionTest(unittest.TestCase):
    def test_all_common_latin_ligatures_expand_without_math_compatibility_mapping(self):
        from paper_scout.quality_llm import _normalized
        for glyph, letters in zip("ﬀﬁﬂﬃﬄﬅﬆ", ("ff", "fi", "fl", "ffi", "ffl", "st", "st")):
            self.assertEqual(_normalized(glyph), letters)
        self.assertNotEqual(_normalized("x²"), _normalized("x2"))
        self.assertNotEqual(_normalized("ℝ"), _normalized("R"))

    def test_namespaced_jats_with_unselected_body_paragraph_is_partial(self):
        from paper_scout.full_text import _extract_jats
        payload = b'<article xmlns="urn:fixture-jats"><body><p>Body preface.</p><sec><title>Methods</title><p>Located evidence.</p><sec><title>Nested</title><p>Nested evidence.</p></sec></sec></body></article>'
        document = _extract_jats(payload, "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC1/fullTextXML", 10, 1000)
        self.assertFalse(document.complete)
        self.assertIn("Nested evidence.", document.text)
        self.assertTrue(any("outside section" in warning for warning in document.warnings))
        self.assertEqual(select_assessment_text(candidate(), document).scope, "partial_full_text")


class ProviderTerminationTest(unittest.TestCase):
    def test_http_200_provider_error_is_retried_once_and_never_a_scientific_failure(self):
        result, _ = ReliabilityTest().assess(SequenceHttp([envelope(finish="error"), envelope()]))
        self.assertEqual(result.quality_status, "pass")
        self.assertEqual(result.execution["calls"][0]["error_kind"], "provider_failure")
        self.assertEqual(result.execution["calls"][0]["finish_reason"], "error")
        self.assertEqual([c["status"] for c in result.execution["calls"]], ["failed", "success"] + ["success"]*7)
        exhausted, _ = ReliabilityTest().assess(SequenceHttp([envelope(finish="error"), envelope(finish="error")]))
        self.assertEqual(exhausted.quality_status, "uncertain")
        self.assertEqual(exhausted.execution["outcome"], "transport_failure")
        self.assertEqual(len(exhausted.execution["calls"]), 2)


class SameModelReroutingTest(unittest.TestCase):
    def test_named_failed_provider_is_excluded_only_on_the_bounded_retry(self):
        first = json.loads(envelope(finish="error"))
        first["provider"] = "NextBit"
        client = SequenceHttp([json.dumps(first), envelope()])
        result, _ = ReliabilityTest().assess(client)
        self.assertEqual(result.quality_status, "pass")
        self.assertEqual(result.execution["calls"][0]["provider"], "NextBit")
        self.assertNotIn("ignore", client.payloads[0]["provider"])
        self.assertEqual(client.payloads[1]["provider"]["ignore"], ["nextbit"])
        self.assertEqual(client.payloads[0]["model"], client.payloads[1]["model"])
        self.assertEqual(len(client.payloads), 2)


class UnknownProviderRoutingTest(unittest.TestCase):
    def test_unknown_provider_display_name_does_not_become_a_guessed_slug(self):
        first = json.loads(envelope(finish="error"))
        first["provider"] = "New Provider Display Name"
        client = SequenceHttp([json.dumps(first), envelope()])
        result, _ = ReliabilityTest().assess(client)
        self.assertEqual(result.quality_status, "pass")
        self.assertNotIn("ignore", client.payloads[1]["provider"])


class LiteralLineWrapRegressionTest(unittest.TestCase):
    def test_actual_autorecsys_and_lngram_quotes_preserve_line_wrap_parity(self):
        check = AnchorRegressionTest().anchor
        self.assertIsNotNone(check("de- pends on complex infrastructure", "de-\npends on complex infrastructure"))
        self.assertIsNotNone(check("depends on complex infrastructure", "de-\npends on complex infrastructure"))
        self.assertIsNotNone(check("sparse compu- tational capacity", "sparse compu-\ntational capacity"))
        self.assertIsNone(check("sparse computational capacity", "sparse compu- tational capacity"))
        self.assertIsNone(check("supports the claim", "does not support the claim"))

    def test_both_views_still_require_visible_nonabstract_and_unique_evidence(self):
        check = AnchorRegressionTest().anchor
        quote = "de- pends on evidence"
        source = "de-\npends on evidence"
        self.assertIsNone(check(quote, source, sections=[SelectedSection("Abstract", source, 2)]))
        self.assertIsNone(check(quote, "other visible text", sections=[SelectedSection("Methods", source, 2)]))
        self.assertIsNone(check(quote, source, page=30, sections=[SelectedSection("Methods", source, 2), SelectedSection("Results", source, 3)]))
        # Two normalization views matching the same section are not two locations.
        self.assertIsNotNone(check("ordinary evidence", "ordinary evidence"))

    def test_rejected_decision_preserves_its_original_rationale_for_audit(self):
        from paper_scout.quality_llm import validate_llm_quality_response
        selected, value = manuscript()
        value["evidence"][0]["excerpt"] = "Invented evidence."
        result = validate_llm_quality_response(value, assess_quality_deterministically(candidate(), "fixture", selected), "test-model", selected=selected)
        self.assertEqual(result.quality_status, "uncertain")
        self.assertEqual(result.execution["proposed_decision"], {key: value[key] for key in ("quality_status", "quality_rationale", "quality_uncertainty")})
        self.assertNotEqual(result.quality_rationale, value["quality_rationale"])


def _load_daily_run_guard():
    import importlib.util
    path = Path(__file__).resolve().parents[1] / ".github/scripts/daily_run_guard.py"
    spec = importlib.util.spec_from_file_location("daily_run_guard", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DailyRunGuardTests(unittest.TestCase):
    CURRENT = 900

    def setUp(self):
        self.guard = _load_daily_run_guard()

    def run_(self, run_id, created_at, event="workflow_dispatch", title="Paper Scout (daily trigger)",
             conclusion="success"):
        return {"id": run_id, "event": event, "display_title": title,
                "created_at": created_at, "conclusion": conclusion}

    def earlier(self, runs, now):
        return self.guard.earlier_success_today(runs, self.CURRENT, now)

    def test_the_late_github_cron_skips_after_the_morning_trigger_succeeded(self):
        now = datetime(2026, 9, 28, 9, 5, tzinfo=UTC)
        morning = self.run_(1, "2026-09-28T04:00:10Z")
        self.assertEqual(self.earlier([morning], now), morning)

    def test_the_morning_trigger_skips_after_an_on_time_github_cron_succeeded(self):
        now = datetime(2026, 11, 2, 5, 0, tzinfo=UTC)  # 06:00 CET
        cron = self.run_(1, "2026-11-02T04:02:00Z", event="schedule", title="Paper Scout")
        self.assertEqual(self.earlier([cron], now), cron)

    def test_a_failed_or_unfinished_daily_run_does_not_block_the_retry(self):
        now = datetime(2026, 9, 28, 9, 5, tzinfo=UTC)
        runs = [self.run_(1, "2026-09-28T04:00:10Z", conclusion="failure"),
                self.run_(2, "2026-09-28T04:30:00Z", conclusion="cancelled"),
                self.run_(3, "2026-09-28T09:00:00Z", event="schedule", conclusion=None)]
        self.assertIsNone(self.earlier(runs, now))

    def test_the_current_run_and_ordinary_manual_runs_do_not_count(self):
        now = datetime(2026, 9, 28, 9, 5, tzinfo=UTC)
        runs = [self.run_(self.CURRENT, "2026-09-28T09:00:00Z", event="schedule"),
                self.run_(1, "2026-09-28T07:00:00Z", title="Paper Scout")]
        self.assertIsNone(self.earlier(runs, now))

    def decide(self, env, runs):
        env = {"GITHUB_REPOSITORY": "o/r", "GITHUB_TOKEN": "t", "GITHUB_RUN_ID": str(self.CURRENT), **env}
        with patch.object(self.guard, "fetch_runs", return_value=runs) as fetch:
            result = self.guard.decide(env, datetime(2026, 9, 28, 9, 5, tzinfo=UTC))
        return result, fetch

    def test_a_non_daily_run_never_reads_history(self):
        (skip, _), fetch = self.decide({"IS_DAILY_RUN": "false"}, [self.run_(1, "2026-09-28T04:00:10Z")])
        self.assertFalse(skip)
        fetch.assert_not_called()

    def test_a_daily_run_queries_from_stockholm_midnight(self):
        (skip, reason), fetch = self.decide({"IS_DAILY_RUN": "true"}, [self.run_(1, "2026-09-28T04:00:10Z")])
        self.assertTrue(skip, reason)
        self.assertEqual(fetch.call_args.args[1], "paper-scout.yml")
        self.assertEqual(fetch.call_args.args[3], datetime(2026, 9, 27, 22, 0, tzinfo=UTC))

    def run_main(self, argv, skip):
        with tempfile.TemporaryDirectory() as tmp:
            output, summary = Path(tmp, "out"), Path(tmp, "summary")
            env = {"GITHUB_OUTPUT": str(output), "GITHUB_STEP_SUMMARY": str(summary)}
            with patch.dict("os.environ", env), \
                 patch.object(self.guard, "decide", return_value=(skip, "because")):
                code = self.guard.main(argv)
            return code, output.read_text() if output.exists() else None

    def test_the_guard_job_writes_the_skip_output_and_succeeds(self):
        self.assertEqual(self.run_main([], skip=True), (0, "skip=true\n"))
        self.assertEqual(self.run_main([], skip=False), (0, "skip=false\n"))

    def test_the_in_job_recheck_fails_a_replayed_duplicate_and_writes_nothing(self):
        self.assertEqual(self.run_main(["--enforce"], skip=True), (1, None))
        self.assertEqual(self.run_main(["--enforce"], skip=False), (0, None))

    def test_the_day_boundary_is_stockholm_midnight_not_utc(self):
        # 23:30 UTC on the 27th is 01:30 CEST on the 28th: the same Stockholm day.
        now = datetime(2026, 9, 28, 4, 0, tzinfo=UTC)
        same_day = self.run_(1, "2026-09-27T23:30:00Z")
        previous_day = self.run_(2, "2026-09-27T21:30:00Z")  # 23:30 CEST on the 27th
        self.assertEqual(self.earlier([same_day], now), same_day)
        self.assertIsNone(self.earlier([previous_day], now))
