"""The operator probe that asks each provider to accept the promotion schema.

No live call is made here. These tests assert the probe sends exactly the production
schema and generation parameters for both roles, carries no manuscript or scientific
content, and reports rather than raises. The live run is an explicit operator step.
"""
import importlib.util
import io
import json
import re
from contextlib import redirect_stdout
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from paper_scout.promotion_protocol import (
    GATE_VERSION, INDEPENDENCE_CONTRACT, INDEPENDENCE_FIELD, schema)
from test_promotion_gate import ENV

SCRIPT = Path(__file__).resolve().parents[1] / '.github' / 'scripts' / 'probe_promotion_schema.py'
_spec = importlib.util.spec_from_file_location('probe_promotion_schema', SCRIPT)
probe_promotion_schema = importlib.util.module_from_spec(_spec)
sys.modules['probe_promotion_schema'] = probe_promotion_schema
_spec.loader.exec_module(probe_promotion_schema)


def refuse(*args, **kwargs):
    raise AssertionError('the probe must not send anything unless asked to')


class ProbeTests(unittest.TestCase):
    def run_probe(self, argv=None, send=refuse):
        output = io.StringIO()
        with (patch.dict('os.environ', ENV, clear=True),
              patch.object(probe_promotion_schema, 'send', send),
              redirect_stdout(output)):
            code = probe_promotion_schema.main(argv or [])
        return code, output.getvalue()

    def test_it_sends_nothing_unless_asked_and_names_the_versions(self):
        code, output = self.run_probe()
        self.assertEqual(code, 0)
        self.assertIn(GATE_VERSION, output)
        self.assertIn(INDEPENDENCE_CONTRACT, output)
        self.assertIn('pass --live to send', output)

    def test_it_carries_the_production_schema_and_no_scientific_content(self):
        sent = []
        self.run_probe(['--live'], send=lambda settings, body: sent.append((settings, body)) or {
            'model': settings.model, 'choices': [{'finish_reason': 'stop', 'message': {
                'content': json.dumps(self.valid(body))}}], 'usage': {'total_tokens': 1}})
        self.assertEqual(len(sent), 2)
        for (settings, body), role in zip(sent, ('primary', 'adjudicator')):
            declared = body['response_format']['json_schema']
            self.assertEqual(declared['schema'], schema(role))
            self.assertIn(INDEPENDENCE_FIELD, declared['schema']['properties'])
            self.assertTrue(declared['strict'])
            self.assertEqual(body['temperature'], 0)
            # A probe evaluates nothing. The prompt names the fields the model must
            # fill, so what must be absent is the content itself: no manuscript text,
            # no real evidence ID and no real content hash.
            text = json.dumps(body['messages'])
            self.assertNotIn('"manuscript"', text)
            self.assertIsNone(re.search(r'E[a-f0-9]{16}-B\d{4}', text))
            self.assertIsNone(re.search(r'[a-f0-9]{64}', text))
            self.assertIn('probe', text)

    def valid(self, body):
        role = 'primary' if 'decision' in json.dumps(body['response_format']) else 'adjudicator'
        body_schema = body['response_format']['json_schema']['schema']
        value = {k: 'probe' for k in body_schema['required']}
        value['evidence_ids'] = []
        value[INDEPENDENCE_FIELD] = {
            k: 'probe' for k in body_schema['properties'][INDEPENDENCE_FIELD]['required']}
        return value

    def test_a_provider_rejection_is_reported_not_raised(self):
        def reject(settings, body):
            raise RuntimeError('synthetic provider rejection')

        code, output = self.run_probe(['--live'], send=reject)
        self.assertEqual(code, 1)
        self.assertIn('synthetic provider rejection', output)
        self.assertIn('promotion schema probe: 2 errors', output)

    def test_a_response_missing_the_dimension_is_reported(self):
        def incomplete(settings, body):
            value = self.valid(body)
            value.pop(INDEPENDENCE_FIELD)
            return {'model': settings.model, 'usage': {}, 'choices': [
                {'finish_reason': 'stop', 'message': {'content': json.dumps(value)}}]}

        code, output = self.run_probe(['--live'], send=incomplete)
        self.assertEqual(code, 1)
        self.assertIn(INDEPENDENCE_FIELD, output)

    def test_an_unconfigured_pair_fails_a_live_probe_and_passes_a_dry_run(self):
        """Asking for a live answer and getting none is a failure to answer."""
        for argv, expected in ((['--live'], 1), ([], 0)):
            output = io.StringIO()
            with (patch.dict('os.environ', {}, clear=True),
                  patch.object(probe_promotion_schema, 'send', refuse), redirect_stdout(output)):
                self.assertEqual(probe_promotion_schema.main(argv), expected)
            self.assertIn('no scientific model pair is configured', output.getvalue())


if __name__ == '__main__':
    unittest.main()
