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
from paper_scout.quality_models import QualityAssessment, QualityEvidence

ENV = {"PAPER_SCOUT_LLM_PROVIDER": "openrouter", "PAPER_SCOUT_LLM_API_KEY": "test-only-key",
       "PAPER_SCOUT_LLM_MODEL": "test-model", "PAPER_SCOUT_LLM_BASE_URL": "https://openrouter.ai/api/v1",
       "PAPER_SCOUT_QUALITY_LLM_REASONING": "off"}


def envelope(value=None, finish="stop"):
    return json.dumps({"id": "fixture-request", "usage": {"prompt_tokens": 123, "completion_tokens": 55, "cost": 0.01},
                       "choices": [{"finish_reason": finish, "message": {"content": json.dumps(value or manuscript()[1])}}]})


class SequenceHttp:
    def __init__(self, responses):
        self.responses = list(responses)
        self.payloads = []

    def post_json(self, url, payload, headers=None):
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
            self.assertEqual([c["kind"] for c in result.execution["calls"]], ["initial", "retry"])
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
            self.assertEqual(len(result.execution["calls"]), count)
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
        for raw in ("not-json", envelope(invalid), envelope(finish="length"), '{"choices":[]}',
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
            result, _ = self.assess(SequenceHttp([envelope(finish="length")]))
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
        value = {**manuscript()[1], "quality_status": "uncertain", "dimension_scores": {},
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
        self.assertEqual([c["status"] for c in calls], ["failed", "success"])
        self.assertEqual(sum(c["usage"]["cost_usd"] or 0 for c in calls), 0.01)
        self.assertEqual(sum(c["usage"]["cost_usd"] is None for c in calls), 1)

    def test_deploy_only_keeps_site_validation_before_deployment(self):
        import yaml
        root = Path(__file__).resolve().parents[1]
        workflow = yaml.load((root / ".github/workflows/paper-scout.yml").read_text(), Loader=yaml.BaseLoader)
        self.assertEqual(workflow["on"]["workflow_dispatch"]["inputs"]["deploy_only"]["type"], "boolean")
        self.assertEqual(workflow["on"]["workflow_dispatch"]["inputs"]["deploy_only"]["default"], "false")
        steps = workflow["jobs"]["scout"]["steps"]
        by_name = {s["name"]: s for s in steps}
        for name in ("Restore durable Paper Scout state", "Run daily paper scout", "Commit scout updates"):
            self.assertIn("!inputs.deploy_only", by_name[name]["if"])
        validation = by_name["Validate generated schemas, links, and runtime exclusion"]
        self.assertNotIn("if", validation)
        self.assertLess(steps.index(validation), steps.index(by_name["Deploy to GitHub Pages"]))
        self.assertEqual(by_name["Deploy to GitHub Pages"]["if"], "success()")


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
        self.assertLessEqual(sum(len(s.text) for s in selected.sections if s.heading == "Conclusion"), 500)
        self.assertLessEqual(len(selected.text), 1800)
        self.assertTrue(all(s.text in selected.text for s in selected.sections))
        self.assertEqual(selected.scope, "partial_full_text")

    def test_prompt_truncation_removes_unseen_section_text(self):
        doc = FullTextDocument("https://example.test/p.pdf", [ExtractedPage(1, "Introduction\n" + "body " * 2000)], "hash", True)
        selected = select_assessment_text(candidate(), doc, max_prompt_characters=400)
        self.assertLessEqual(len(selected.text), 400)
        self.assertTrue(all(s.text in selected.text for s in selected.sections))
        self.assertEqual(selected.scope, "partial_full_text")
