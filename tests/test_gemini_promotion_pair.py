"""Gemini primary with an independent DeepSeek adjudicator. No live model calls.

Every response here is synthetic. These tests cover provider routing, credential
isolation, model-pair provenance, usage/billing accounting and the unchanged
promotion rule. They never assert that any real manuscript is good science.
"""
from contextlib import closing
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.http import HttpRequestError
from paper_scout.config import QualityConfig
from paper_scout.models import ClassificationResult
from paper_scout.promotion_gate import assess_promotion, role_settings, settings_from_env
from paper_scout.promotion_protocol import (
    ADJUDICATOR_MODEL, ASSESSMENT_VERSION, DUAL_PROMOTION_GATE_VERSIONS, FIELDS, GATE_VERSION,
    MODEL_FAMILIES, MODEL_PROVIDERS, PRIMARY_MODEL, model_pair_provenance, validate_pair,
)
from paper_scout.quality_models import QUALITY_GATE_VERSION, QualityAssessment
from paper_scout.quality_service import quality_assessment_matches_mode
from paper_scout.state import PaperStore
from test_promotion_gate import ENV, fixture

GOOGLE_URL = 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions'
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'


class PairModels:
    """Provider-shaped stub: Google reports tokens only, OpenRouter also reports cost."""

    retries = 1

    def __init__(self, primary='pass', adjudicator='pass', fail=None, bad_adjudications=0):
        self.decisions = (primary, adjudicator)
        self.fail = fail
        self.bad_adjudications = bad_adjudications
        self.calls = []

    def post_json(self, url, payload, headers):
        role = 'primary' if not self.calls else 'adjudicator'
        self.calls.append({'url': url, 'payload': deepcopy(payload), 'headers': dict(headers)})
        if self.fail == role:
            raise HttpRequestError('timeout', url, 'synthetic provider outage')
        prompt = json.loads(payload['messages'][1]['content'])
        import re
        ids = re.findall(r'\[(E[a-f0-9]+-B\d+)\]', prompt['manuscript'])
        value = {k: prompt[k] for k in ('canonical_id', 'source_content_hash', 'context_id')}
        value['evidence_ids'] = ids[:3]
        if role == 'primary':
            value.update({k: 'Scoped scientific judgment with canonical evidence.' for k in FIELDS})
            value['decision'] = self.decisions[0]
        else:
            value['promotion_decision'] = self.decisions[1]
            value['blocking_reasons'] = [] if self.decisions[1] == 'pass' else ['Unsupported overclaim.']
        content = json.dumps(value, ensure_ascii=False)
        if role == 'adjudicator' and self.bad_adjudications > 0:
            self.bad_adjudications -= 1
            content = content.replace('"promotion_decision"', '"promotion_verdict"')  # schema violation
        usage = {'prompt_tokens': 1200, 'completion_tokens': 300, 'total_tokens': 1500}
        if 'openrouter.ai' in url:  # Only OpenRouter returns a per-call charge.
            usage['cost'] = 0.0042
        return json.dumps({'model': payload['model'], 'usage': usage,
                           'choices': [{'finish_reason': 'stop', 'message': {
                               'content': content,
                               'extra_content': {'google': {'thought_signature': 'DO NOT RETAIN'}}}}]},
                          ensure_ascii=False)


def run_gate(models, env=None):
    candidate, _, text, seed = fixture()
    with patch.dict('os.environ', env or ENV, clear=True):
        return assess_promotion(candidate, text, seed, 'llm', http=models)


LEGACY_ENV = {**ENV,
              'PAPER_SCOUT_QUALITY_LLM_MODEL': 'deepseek/deepseek-v4-pro-0813',
              'PAPER_SCOUT_QUALITY_ADJUDICATOR_MODEL': 'anthropic/claude-sonnet-4.6'}


def legacy_receipt(models=None):
    """A receipt as the retired pair actually wrote one.

    The old pair is genuinely executed so every binding hash is authentic, then
    only the fields that version never recorded are removed. Rewriting a bound
    field instead would produce a receipt no real run could have produced.
    """
    result = run_gate(models or PairModels(), LEGACY_ENV)
    execution = deepcopy(result.execution)
    for key in ('model_pair', 'primary_provider', 'adjudicator_provider', 'generation'):
        execution.pop(key, None)
    for call in execution['calls']:
        call.pop('provider', None)
        call.pop('billing', None)
    return replace(result, quality_gate_version='dual-promotion-v1', execution=execution)


class ConfigurationTests(unittest.TestCase):
    def test_production_pair_is_gemini_primary_and_deepseek_adjudicator(self):
        self.assertEqual(PRIMARY_MODEL, 'gemini-3.8-flash')
        self.assertEqual(ADJUDICATOR_MODEL, 'deepseek/deepseek-v4-pro-0813')
        self.assertEqual(MODEL_PROVIDERS[PRIMARY_MODEL], 'google')
        self.assertEqual(MODEL_PROVIDERS[ADJUDICATOR_MODEL], 'openrouter')
        self.assertNotEqual(MODEL_FAMILIES[PRIMARY_MODEL], MODEL_FAMILIES[ADJUDICATOR_MODEL])
        validate_pair(PRIMARY_MODEL, ADJUDICATOR_MODEL)

    def test_same_family_unknown_model_and_unknown_provider_fail_closed(self):
        for primary, adjudicator in ((PRIMARY_MODEL, PRIMARY_MODEL),
                                     ('anthropic/claude-sonnet-4.6', 'anthropic/claude-opus-4.6'),
                                     (PRIMARY_MODEL, 'gemini-3.8-flash-latest'),
                                     ('made-up-model', ADJUDICATOR_MODEL)):
            with self.assertRaises(ValueError):
                validate_pair(primary, adjudicator)

    def test_each_role_resolves_its_own_provider_credential_and_host(self):
        with patch.dict('os.environ', ENV, clear=True):
            primary, adjudicator = settings_from_env()
        self.assertEqual((primary.provider, adjudicator.provider), ('google', 'openrouter'))
        self.assertEqual(primary.api_key, ENV['GEMINI_API_KEY'])
        self.assertEqual(adjudicator.api_key, ENV['OPENROUTER_API_KEY'])
        self.assertNotEqual(primary.api_key, adjudicator.api_key)
        self.assertIn('generativelanguage.googleapis.com', primary.base_url)
        self.assertIn('openrouter.ai', adjudicator.base_url)

    def test_missing_either_credential_disables_the_gate_without_calls(self):
        for missing in ('GEMINI_API_KEY', 'OPENROUTER_API_KEY'):
            env = {k: v for k, v in ENV.items() if k != missing}
            with patch.dict('os.environ', env, clear=True):
                self.assertIsNone(settings_from_env())
            models = PairModels()
            result = run_gate(models, env)
            self.assertEqual(result.execution['outcome'], 'not_assessed')
            self.assertEqual(result.execution['calls'], [])
            self.assertEqual(models.calls, [])

    def test_provider_host_mismatch_is_rejected(self):
        for name, value in (('PAPER_SCOUT_GOOGLE_BASE_URL', 'https://generativelanguage.googleapis.com.evil.test/v1'),
                            ('PAPER_SCOUT_OPENROUTER_BASE_URL', 'https://openrouter.ai.evil.test/api/v1')):
            with patch.dict('os.environ', {**ENV, name: value}, clear=True):
                with self.assertRaises(ValueError):
                    settings_from_env()

    def test_unknown_model_has_no_provider(self):
        with self.assertRaises(ValueError):
            role_settings('not-a-pinned-model')


class PromotionOutcomeTests(unittest.TestCase):
    def test_gemini_pass_and_deepseek_pass_is_eligible_for_promotion(self):
        models = PairModels('pass', 'pass')
        result = run_gate(models)
        self.assertEqual(result.quality_status, 'pass')
        self.assertEqual(result.execution['outcome'], 'success')
        self.assertEqual(result.execution['provenance_status'], 'pass')
        self.assertEqual(len(models.calls), 2)
        self.assertEqual(models.calls[0]['url'], GOOGLE_URL)
        self.assertEqual(models.calls[1]['url'], OPENROUTER_URL)

    def test_disagreement_in_either_direction_is_not_promoted(self):
        for primary, adjudicator in (('pass', 'uncertain'), ('uncertain', 'pass'), ('uncertain', 'uncertain')):
            with self.subTest(primary=primary, adjudicator=adjudicator):
                result = run_gate(PairModels(primary, adjudicator))
                self.assertEqual(result.execution['outcome'], 'success')
                self.assertEqual(result.quality_status, 'uncertain')
                self.assertNotEqual(result.quality_status, 'pass')

    def test_either_provider_failure_is_technical_and_never_a_scientific_rejection(self):
        for failing in ('primary', 'adjudicator'):
            with self.subTest(failing=failing):
                models = PairModels(fail=failing)
                result = run_gate(models)
                self.assertEqual(result.execution['outcome'], 'transport_failure')
                self.assertEqual(result.quality_status, 'uncertain')
                self.assertEqual(result.evidence, [])
                # Infrastructure trouble is never a scientific rejection.
                self.assertNotEqual(result.quality_status, 'insufficient')
                self.assertNotEqual(result.execution['outcome'], 'success')
                self.assertIn('technical', result.quality_rationale.lower())
                self.assertEqual(len(models.calls), 1 if failing == 'primary' else 2)

    def test_each_role_receives_only_its_own_provider_credential(self):
        models = PairModels()
        run_gate(models)
        self.assertEqual(models.calls[0]['headers']['Authorization'],
                         'Bearer ' + ENV['GEMINI_API_KEY'])
        self.assertEqual(models.calls[1]['headers']['Authorization'],
                         'Bearer ' + ENV['OPENROUTER_API_KEY'])
        self.assertNotIn(ENV['OPENROUTER_API_KEY'], json.dumps(models.calls[0]))
        self.assertNotIn(ENV['GEMINI_API_KEY'], json.dumps(models.calls[1]))

    def test_provider_specific_generation_parameters(self):
        models = PairModels()
        run_gate(models)
        google, openrouter = models.calls[0]['payload'], models.calls[1]['payload']
        self.assertEqual(google['reasoning_effort'], 'none')
        self.assertNotIn('provider', google)
        self.assertNotIn('reasoning', google)
        self.assertEqual(openrouter['reasoning'], {'enabled': False, 'exclude': True})
        self.assertTrue(openrouter['provider']['require_parameters'])
        self.assertNotIn('reasoning_effort', openrouter)
        for payload in (google, openrouter):
            self.assertEqual(payload['temperature'], 0)
            self.assertTrue(payload['response_format']['json_schema']['strict'])


class ProvenanceTests(unittest.TestCase):
    def test_model_pair_identity_and_providers_are_persisted(self):
        result = run_gate(PairModels())
        execution = result.execution
        self.assertEqual(result.quality_gate_version, GATE_VERSION)
        self.assertEqual(execution['primary_model'], PRIMARY_MODEL)
        self.assertEqual(execution['adjudicator_model'], ADJUDICATOR_MODEL)
        self.assertEqual(execution['primary_provider'], 'google')
        self.assertEqual(execution['adjudicator_provider'], 'openrouter')
        self.assertEqual(execution['model_pair'], model_pair_provenance(PRIMARY_MODEL, ADJUDICATOR_MODEL))
        self.assertTrue(execution['model_pair']['independent_families'])
        self.assertEqual([c['provider'] for c in execution['calls']], ['google', 'openrouter'])
        self.assertEqual(execution['generation']['hidden_reasoning'], 'disabled')

    def test_tampered_or_missing_provider_provenance_is_rejected(self):
        result = run_gate(PairModels())
        mutations = [
            lambda e: e.pop('model_pair'),
            lambda e: e.pop('primary_provider'),
            lambda e: e.pop('adjudicator_provider'),
            lambda e: e.update(primary_provider='openrouter'),
            lambda e: e.update(adjudicator_provider='google'),
            lambda e: e['model_pair'].update(independent_families=False),
            lambda e: e['model_pair']['primary'].update(provider='openrouter'),
            lambda e: e['model_pair']['adjudicator'].update(family='gemini'),
            lambda e: e['calls'][0].update(provider='openrouter'),
            lambda e: e['calls'][1].pop('provider'),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                execution = deepcopy(result.execution)
                mutate(execution)
                with self.assertRaises(ValueError):
                    QualityAssessment.from_dict(replace(result, execution=execution).to_dict())

    def test_legacy_model_pair_receipt_remains_readable(self):
        legacy = legacy_receipt()
        restored = QualityAssessment.from_dict(legacy.to_dict())
        self.assertEqual(restored.quality_gate_version, 'dual-promotion-v1')
        self.assertEqual(restored.execution['primary_model'], 'deepseek/deepseek-v4-pro-0813')
        self.assertEqual(restored.execution['adjudicator_model'], 'anthropic/claude-sonnet-4.6')
        self.assertNotIn('model_pair', restored.execution)
        self.assertEqual(restored.quality_status, 'pass')

    def test_legacy_receipt_cannot_borrow_new_provider_provenance(self):
        legacy = legacy_receipt()
        execution = deepcopy(legacy.execution)
        execution['model_pair'] = model_pair_provenance('deepseek/deepseek-v4-pro-0813',
                                                        'anthropic/claude-sonnet-4.6')
        with self.assertRaises(ValueError):
            QualityAssessment.from_dict(replace(legacy, execution=execution).to_dict())

    def test_new_gate_version_stores_beside_old_rows_without_mutating_them(self):
        current = run_gate(PairModels())
        legacy = legacy_receipt()
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / 'state.sqlite3')
            candidate, _, _, _ = fixture()
            store.upsert_paper(candidate, ClassificationResult(95, 'relevant', 'Synthetic topical match'))
            store.save_quality_assessment(legacy)
            before = store.get_current_quality_assessment(legacy.canonical_id)
            store.save_quality_assessment(current)
            with closing(sqlite3.connect(store.path)) as db:
                rows = [QualityAssessment.from_dict(json.loads(payload)) for (payload,) in db.execute(
                    'select payload_json from paper_quality_assessments where canonical_id=? order by id',
                    (current.canonical_id,))]
        self.assertEqual(before.quality_gate_version, 'dual-promotion-v1')
        self.assertEqual(len(rows), 2)
        self.assertEqual([r.quality_gate_version for r in rows],
                         ['dual-promotion-v1', 'dual-promotion-v2'])
        # The retired row keeps its original pair; history is appended, never rewritten.
        self.assertEqual(rows[0].execution['primary_model'], 'deepseek/deepseek-v4-pro-0813')
        self.assertEqual(rows[1].execution['primary_model'], PRIMARY_MODEL)
        self.assertIn(rows[0].quality_gate_version, DUAL_PROMOTION_GATE_VERSIONS)

    def test_usage_and_billing_accounting_per_provider(self):
        result = run_gate(PairModels())
        primary, adjudicator = result.execution['calls']
        for call in (primary, adjudicator):
            self.assertEqual(call['usage']['prompt_tokens'], 1200)
            self.assertEqual(call['usage']['completion_tokens'], 300)
            self.assertEqual(call['usage']['total_tokens'], 1500)
        # Google reports no charge, so the cost is attributed, never invented.
        self.assertIsNone(primary['usage']['cost_usd'])
        self.assertIsNone(primary['billing']['cost_usd'])
        self.assertEqual(primary['billing']['basis'], 'covered_by_msc_allocation')
        self.assertEqual(primary['billing']['billing_cost'], 'UNKNOWN')
        self.assertEqual(adjudicator['usage']['cost_usd'], 0.0042)
        self.assertEqual(adjudicator['billing']['basis'], 'provider_reported')
        self.assertNotIn('billing_cost', adjudicator['billing'])

    def test_credentials_and_hidden_reasoning_are_never_persisted(self):
        result = run_gate(PairModels())
        serialized = json.dumps(result.to_dict())
        for secret in (ENV['GEMINI_API_KEY'], ENV['OPENROUTER_API_KEY'],
                       'Authorization', 'DO NOT RETAIN', 'thought_signature'):
            self.assertNotIn(secret, serialized)

    def test_adjudicator_retry_keeps_provider_provenance_intact(self):
        models = PairModels(bad_adjudications=1)
        result = run_gate(models)
        self.assertEqual(result.quality_status, 'pass')
        self.assertEqual(result.execution['outcome'], 'success')
        calls = result.execution['calls']
        self.assertEqual(len(calls), 3)
        # One rejected adjudication is retained; the retry stays on its own provider.
        self.assertEqual([c['provider'] for c in calls], ['google', 'openrouter', 'openrouter'])
        self.assertEqual([c['status'] for c in calls],
                         ['success', 'contract_failure', 'success'])
        self.assertEqual(calls[1]['contract_error'], 'schema')
        self.assertEqual(result.execution['model_pair'],
                         model_pair_provenance(PRIMARY_MODEL, ADJUDICATOR_MODEL))
        self.assertEqual(QualityAssessment.from_dict(result.to_dict()).execution['calls'][1]['provider'],
                         'openrouter')

    def test_openrouter_role_accepts_the_legacy_credential_name(self):
        env = {'GEMINI_API_KEY': ENV['GEMINI_API_KEY'],
               'PAPER_SCOUT_LLM_API_KEY': 'legacy-openrouter-key'}
        with patch.dict('os.environ', env, clear=True):
            primary, adjudicator = settings_from_env()
        self.assertEqual(adjudicator.api_key, 'legacy-openrouter-key')
        self.assertEqual(adjudicator.provider, 'openrouter')
        self.assertEqual(primary.api_key, env['GEMINI_API_KEY'])
        models = PairModels()
        self.assertEqual(run_gate(models, env).quality_status, 'pass')
        self.assertEqual(models.calls[1]['headers']['Authorization'], 'Bearer legacy-openrouter-key')

    def test_provider_host_mismatch_fails_closed_without_calls_or_credentials(self):
        """A stale endpoint override is a technical outcome, never a crash or a leak."""
        for name in ('PAPER_SCOUT_LLM_BASE_URL', 'PAPER_SCOUT_GOOGLE_BASE_URL'):
            with self.subTest(override=name):
                models = PairModels()
                result = run_gate(models, {**ENV, name: 'https://api.openai.com/v1'})
                self.assertEqual(result.execution['outcome'], 'protocol_failure')
                self.assertEqual(result.quality_status, 'uncertain')
                self.assertEqual(models.calls, [])
                self.assertNotIn(ENV['GEMINI_API_KEY'], json.dumps(result.to_dict()))

    def test_retired_pair_receipt_is_not_treated_as_the_current_configuration(self):
        """A v1 row is honestly reported as not matching the v2 pair.

        Routine selection still excludes it, because the assessment and rubric
        versions are unchanged, so history is not swept into a re-run.
        """
        legacy = legacy_receipt()
        config = QualityConfig(enabled=True, mode='llm')
        with patch.dict('os.environ', ENV, clear=True):
            self.assertFalse(quality_assessment_matches_mode(config, legacy))
        self.assertEqual(legacy.assessment_version, ASSESSMENT_VERSION)
        self.assertEqual(legacy.rubric_version, 'scholarly-rubric-v1')
        # This is exactly the exclusion a routine reassessment run applies.
        self.assertTrue(legacy.quality_status == 'pass' or (
            legacy.quality_gate_version in {QUALITY_GATE_VERSION, *DUAL_PROMOTION_GATE_VERSIONS}
            and legacy.assessment_version == ASSESSMENT_VERSION
            and legacy.rubric_version == 'scholarly-rubric-v1'))

    def test_returned_model_must_equal_the_pinned_model(self):
        """A provider alias in the response envelope fails closed, not silently."""
        class AliasModels(PairModels):
            def post_json(self, url, payload, headers):
                raw = json.loads(super().post_json(url, payload, headers))
                raw['model'] = raw['model'] + '-001'
                return json.dumps(raw)

        models = AliasModels()
        result = run_gate(models)
        self.assertEqual(result.execution['outcome'], 'protocol_failure')
        self.assertEqual(result.quality_status, 'uncertain')
        self.assertEqual(len(models.calls), 1)

    def test_receipt_and_coverage_checks_remain_intact(self):
        result = run_gate(PairModels())
        self.assertEqual(result.execution['receipt_version'], 'canonical-response-v1')
        self.assertEqual(result.execution['coverage_gate']['status'], 'pass')
        for index, call in enumerate(result.execution['calls']):
            self.assertEqual(call['status'], 'success')
            self.assertEqual(call['finish_reason'], 'stop')
            self.assertEqual(len(call['response_binding_sha256']), 64)
            self.assertEqual(call['kind'], 'primary' if index == 0 else 'adjudicator')
        # Any bound field change must still invalidate the stored receipt.
        execution = deepcopy(result.execution)
        execution['calls'][0]['raw_content'] = execution['calls'][0]['raw_content'].replace('pass', 'uncertain')
        with self.assertRaises(ValueError):
            QualityAssessment.from_dict(replace(result, execution=execution).to_dict())


if __name__ == '__main__':
    unittest.main()
