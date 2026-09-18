"""Bounded adjudication contract recovery on synthetic manuscripts only; no network."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import jsonschema

from test_promotion_gate import ENV, Models, fixture
from paper_scout.evidence_context import build_evidence_context
from paper_scout.promotion_gate import assess_promotion
from paper_scout.promotion_protocol import schema, validate_response, validate_receipt
from paper_scout.quality_models import QualityAssessment
from paper_scout.state import PaperStore


def large_fixture():
    c, _, text, seed = fixture()
    raw = '\n'.join(f'Synthetic observation {i}. ' + 'Controlled experiment evidence. ' * 28
                    for i in range(40))
    text = replace(text, text=raw, sections=[replace(text.sections[0], text=raw)])
    context = build_evidence_context(seed.canonical_id, text)
    assert len(context.blocks) > 30
    return c, text, seed, context


class RetryModels(Models):
    def __init__(self, counts=(26, 3), decisions=('pass', 'pass'), mutate=None, raw=None):
        super().__init__()
        self.counts, self.adjudications, self.mutate, self.raw = counts, decisions, mutate, raw
        self.contents = []

    def post_json(self, url, payload, headers):
        envelope = json.loads(super().post_json(url, payload, headers))
        index = len(self.payloads) - 1
        value = json.loads(envelope['choices'][0]['message']['content'])
        if index:
            prompt = json.loads(payload['messages'][1]['content'])
            ids = re.findall(r'\[(E[a-f0-9]+-B\d+)\]', prompt['manuscript'])
            count = self.counts[min(index - 1, len(self.counts) - 1)]
            value['evidence_ids'] = ids[:count] if index == 1 else ids[-count:]
            value['promotion_decision'] = self.adjudications[index - 1]
            value['blocking_reasons'] = (['Independent retry concern.']
                                         if value['promotion_decision'] == 'uncertain' else [])
        if self.mutate:
            self.mutate(value, index)
        content = json.dumps(value)
        if self.raw and index == 1:
            content = self.raw(content)
        self.contents.append(content)
        envelope['choices'][0]['message']['content'] = content
        return json.dumps(envelope)


class RetryTests(unittest.TestCase):
    def run_gate(self, models):
        candidate, text, seed, _ = large_fixture()
        with patch.dict('os.environ', ENV, clear=True):
            result = assess_promotion(candidate, text, seed, 'llm', http=models)
        return result

    def test_24_accepted_25_and_26_rejected_by_same_generation_schema(self):
        _, _, _, context = large_fixture()
        result = self.run_gate(RetryModels(counts=(24,)))
        self.assertEqual(result.execution['outcome'], 'success')
        self.assertEqual(len(result.execution['calls']), 2)
        for role in ('primary', 'adjudicator'):
            value = deepcopy(result.execution[role])
            for count in (24, 25, 26):
                value['evidence_ids'] = [b.evidence_id for b in context.blocks[:count]]
                if count == 24:
                    self.assertIs(validate_response(value, role, context), value)
                else:
                    with self.assertRaises(jsonschema.ValidationError) as raised:
                        validate_response(value, role, context)
                    self.assertEqual(raised.exception.validator, 'maxItems')
        models = RetryModels(); self.run_gate(models)
        for payload in models.payloads:
            role = 'primary' if payload['model'].startswith('deepseek/') else 'adjudicator'
            fmt = payload['response_format']['json_schema']
            self.assertTrue(fmt['strict'])
            self.assertTrue(payload['provider']['require_parameters'])
            self.assertEqual(fmt['schema'], schema(role))
            self.assertEqual(fmt['schema']['properties']['evidence_ids']['maxItems'], 24)
            self.assertTrue(fmt['schema']['properties']['evidence_ids']['uniqueItems'])
        self.assertIn('at most 24 distinct evidence IDs', models.payloads[1]['messages'][0]['content'])

    def test_26_then_valid_is_fresh_and_never_truncated(self):
        models = RetryModels(); result = self.run_gate(models)
        self.assertEqual(result.quality_status, 'pass')
        self.assertEqual(len(models.payloads), 3)
        self.assertEqual(models.payloads[1]['messages'][1], models.payloads[2]['messages'][1])
        self.assertEqual(len(models.payloads[2]['messages']), 2)
        self.assertNotIn(models.contents[1], json.dumps(models.payloads[2]))
        calls = result.execution['calls']
        self.assertEqual([c['attempt'] for c in calls], [1, 1, 2])
        self.assertEqual([c['status'] for c in calls], ['success', 'contract_failure', 'success'])
        self.assertEqual(calls[1]['raw_content'], models.contents[1])
        self.assertEqual(len(json.loads(calls[1]['raw_content'])['evidence_ids']), 26)
        self.assertEqual(result.execution['adjudicator'], json.loads(models.contents[2]))
        self.assertEqual(len(result.execution['adjudicator']['evidence_ids']), 3)
        self.assertNotIn('canonical_response_sha256', calls[1])
        self.assertEqual(sum(c['usage']['cost_usd'] for c in calls), .003)
        self.assertNotIn('DO NOT RETAIN', json.dumps(result.to_dict()))
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / 'state.sqlite3')
            first = store.save_quality_assessment(result)
            self.assertEqual(store.save_quality_assessment(result), first)
            loaded = store.get_current_quality_assessment(result.canonical_id)
            self.assertEqual(loaded, result)
            validate_receipt(loaded)

    def test_second_over_cap_stops_no_third_adjudication_or_promotion(self):
        for second in (25, 26):
            models = RetryModels(counts=(26, second)); result = self.run_gate(models)
            self.assertEqual(len(models.payloads), 3)
            self.assertEqual(result.execution['outcome'], 'protocol_failure')
            self.assertEqual(result.quality_status, 'uncertain')
            self.assertFalse(result.full_text_assessed)
            self.assertEqual(result.evidence, [])
            self.assertNotIn('adjudicator', result.execution)
            self.assertEqual([len(json.loads(c['raw_content'])['evidence_ids'])
                              for c in result.execution['calls'][1:]], [26, second])

    def test_retry_integrity_checks_invented_foreign_version_context_and_duplicates(self):
        changes = {'evidence_ids': ['invented'], 'canonical_id': 'other-manuscript',
                   'source_content_hash': '0' * 64, 'context_id': '0' * 64}
        for key, value in changes.items():
            models = RetryModels(mutate=lambda v, i: v.update({key: value}) if i == 2 else None)
            result = self.run_gate(models)
            self.assertEqual(len(models.payloads), 3)
            self.assertEqual(result.execution['outcome'], 'protocol_failure')
            self.assertEqual(result.quality_status, 'uncertain')
        models = RetryModels(mutate=lambda v, i: v.update(evidence_ids=v['evidence_ids'] * 2)
                             if i == 2 else None)
        self.assertEqual(self.run_gate(models).execution['outcome'], 'protocol_failure')
        self.assertEqual(len(models.payloads), 3)
        models = RetryModels(counts=(3, 3), mutate=lambda v, i:
                             v.update(evidence_ids=v['evidence_ids'] * 2) if i == 1 else None)
        self.assertEqual(self.run_gate(models).execution['outcome'], 'success')
        self.assertEqual(len(models.payloads), 3)

    def test_first_identity_failures_are_not_retryable(self):
        for key, value in [('canonical_id', 'foreign'), ('evidence_ids', ['invented'])]:
            models = RetryModels(counts=(3,), mutate=lambda v, i: v.update({key: value}) if i == 1 else None)
            self.assertEqual(self.run_gate(models).execution['outcome'], 'protocol_failure')
            self.assertEqual(len(models.payloads), 2)

    def test_schema_and_json_retry_but_primary_and_transport_are_not_retried(self):
        for raw in (lambda s: 'not json', lambda s: s[:-1] + ',"context_id":"duplicate"}',
                    lambda s: s.replace('"promotion_decision": "pass"', '"promotion_decision": "INVALID"')):
            models = RetryModels(counts=(3, 3), raw=raw)
            self.assertEqual(self.run_gate(models).execution['outcome'], 'success')
            self.assertEqual(len(models.payloads), 3)
        models = RetryModels(mutate=lambda v, i: v.update(decision='INVALID') if i == 0 else None)
        self.assertEqual(self.run_gate(models).execution['outcome'], 'protocol_failure')
        self.assertEqual(len(models.payloads), 1)
        from paper_scout.http import HttpRequestError
        models = RetryModels()
        with patch.object(models, 'post_json', side_effect=HttpRequestError('POST', 'https://example.test', 'synthetic')):
            result = self.run_gate(models)
        self.assertEqual(result.execution['outcome'], 'transport_failure')
        self.assertEqual(len(result.execution['calls']), 1)

    def test_valid_retry_decides_science_independently_in_both_directions(self):
        for first, second in [('pass', 'uncertain'), ('uncertain', 'pass')]:
            models = RetryModels(decisions=(first, second)); result = self.run_gate(models)
            self.assertEqual(result.quality_status, second)
            self.assertEqual(result.execution['adjudicator']['promotion_decision'], second)
            self.assertEqual(result.execution['outcome'], 'success')
            validate_receipt(result)

    def test_failed_attempt_binding_and_retry_receipt_tampering_fail_closed(self):
        result = self.run_gate(RetryModels())
        changes = [('raw_content', '{}'), ('request_sha256', '0' * 64), ('model', 'foreign'),
                   ('context_id', '0' * 64), ('status', 'success'), ('attempt', 2),
                   ('contract_error', 'json'), ('usage', {}), ('attempt_binding_sha256', '0' * 64)]
        for key, value in changes:
            d = deepcopy(result.to_dict()); d['execution']['calls'][1][key] = value
            with self.assertRaises(ValueError): QualityAssessment.from_dict(d)
        for mutate in (lambda e: e['calls'].pop(1), lambda e: e['calls'].append(e['calls'][-1]),
                       lambda e: e.update(total_request_limit=4), lambda e: e.pop('retry_policy'),
                       lambda e: e.update(attempt_limit_per_role={'primary': 2, 'adjudicator': 2})):
            d = deepcopy(result.to_dict()); mutate(d['execution'])
            with self.assertRaises(ValueError): QualityAssessment.from_dict(d)

    def test_legacy_two_success_receipt_remains_readable(self):
        result = self.run_gate(RetryModels(counts=(3,)))
        d = result.to_dict(); e = d['execution']
        e.pop('retry_policy'); e.update(total_request_limit=2, attempt_limit_per_role=1)
        for c in e['calls']:
            c.pop('attempt'); c.pop('attempt_binding_sha256')
        legacy = QualityAssessment.from_dict(d)
        validate_receipt(legacy)


if __name__ == '__main__':
    unittest.main()
