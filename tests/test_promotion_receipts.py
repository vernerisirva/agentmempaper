"""Receipt representation only: saved bug bytes plus synthetic model responses."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_promotion_gate import ENV, Models, fixture
from paper_scout.evidence_context import build_evidence_context, digest
from paper_scout.promotion_gate import assess_promotion
from paper_scout.promotion_protocol import canonical_json, parse_response, validate_receipt
from paper_scout.quality_models import QualityAssessment, QualityEvidence
from paper_scout.state import PaperStore

UNICODE = 'α β μ ± × ≤ ≥ → – — “ ” é Å'


class FormattedModels(Models):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.raw_contents = []

    def post_json(self, url, payload, headers):
        envelope = json.loads(super().post_json(url, payload, headers))
        value = json.loads(envelope['choices'][0]['message']['content'])
        content = ' \n\t' + json.dumps(dict(reversed(list(value.items()))),
                                      indent=3, ensure_ascii=False) + '\n '
        envelope['choices'][0]['message']['content'] = content
        self.raw_contents.append(content)
        return json.dumps(envelope)


class ReceiptTests(unittest.TestCase):
    def run_gate(self, models=None, text=None, seed=None):
        candidate, _, original, original_seed = fixture()
        with patch.dict('os.environ', ENV, clear=True):
            return assess_promotion(candidate, text or original, seed or original_seed,
                                    'llm', http=models or Models())

    def test_original_batch3_excerpt_survives_store_without_repair(self):
        saved = json.loads((Path(__file__).parent / 'fixtures/batch3_receipt_whitespace.json').read_text())
        excerpt = saved['source_excerpt']
        self.assertEqual(excerpt.encode()[-1:].hex(), saved['removed_utf8_hex'])
        self.assertEqual(excerpt.strip(), saved['old_deserialized_excerpt'])
        _, _, text, seed = fixture()
        # Exact failing bytes in an otherwise synthetic manuscript/context. No
        # additional frozen papers are used, acquired, inspected or sent to models.
        text = replace(text, text=excerpt, sections=[replace(text.sections[0], text=excerpt)],
                       coverage={**text.coverage, "assessment_input_sha256": digest(excerpt)})
        result = self.run_gate(FormattedModels(), text, seed)
        self.assertEqual(result.quality_status, 'pass')
        self.assertEqual(result.evidence[0].excerpt, excerpt)
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp) / 'state.sqlite3')
            store.save_quality_assessment(result)
            loaded = store.get_current_quality_assessment(result.canonical_id)
            self.assertEqual(loaded, result)
            validate_receipt(loaded)

    def test_formatting_canonicalization_and_raw_preservation_both_roles(self):
        models = FormattedModels()
        result = self.run_gate(models)
        context = build_evidence_context('fixture', fixture()[2])
        for i, role in enumerate(('primary', 'adjudicator')):
            call = result.execution['calls'][i]
            value = result.execution[role]
            self.assertEqual(call['raw_content'], models.raw_contents[i])
            self.assertEqual(parse_response(call['raw_content'], role, context), value)
            self.assertEqual(call['canonical_response_sha256'], digest(canonical_json(value)))
            changed_order = dict(reversed(list(value.items())))
            self.assertEqual(canonical_json(value), canonical_json(changed_order))
        self.assertEqual(QualityAssessment.from_dict(json.loads(json.dumps(result.to_dict()))), result)

    def test_unicode_and_scientific_whitespace_are_exact(self):
        prose = '  95 % confidence; ' + UNICODE + '; e\u0301 A\u030a\n '
        models = FormattedModels(change=lambda v,r: v.update(quality_rationale=prose) if r == 0 else v.update(blocking_reasons=[prose]))
        result = self.run_gate(models)
        self.assertEqual(result.quality_status, 'uncertain')
        self.assertEqual(result.quality_rationale, prose)
        restored = QualityAssessment.from_dict(json.loads(json.dumps(result.to_dict(), ensure_ascii=True)))
        self.assertEqual(restored, result)
        for i, role in enumerate(('primary', 'adjudicator')):
            call = result.execution['calls'][i]
            self.assertIn(UNICODE, call['raw_content'])
            self.assertIn('e\u0301 A\u030a', canonical_json(result.execution[role]))
            self.assertEqual(call['canonical_response_sha256'], digest(canonical_json(restored.execution[role])))
        for role, field, value in [('primary','quality_rationale',prose.strip()),
                                    ('adjudicator','blocking_reasons',[prose.replace('95 %','95%')])]:
            d = deepcopy(result.to_dict()); d['execution'][role][field] = value
            with self.assertRaises(ValueError): QualityAssessment.from_dict(d)

    def test_material_changes_missing_extra_and_array_order_fail_closed(self):
        result = self.run_gate()
        for role in ('primary', 'adjudicator'):
            mutations = [lambda v: v.update(evidence_ids=v['evidence_ids'][1:]),
                         lambda v: v.update(evidence_ids=list(reversed(v['evidence_ids']))),
                         lambda v: v.pop('source_content_hash'),
                         lambda v: v.update(unsupported_decision='pass'),
                         lambda v: v.update(canonical_id='another-paper')]
            if role == 'primary':
                mutations += [lambda v: v.update(decision='uncertain'),
                              lambda v: v.update(method_assessment='Materially altered method.'),
                              lambda v: v.update(quality_rationale='Materially altered rationale.')]
            else:
                mutations += [lambda v: v.update(promotion_decision='uncertain'),
                              lambda v: v.update(blocking_reasons=['Material concern.'])]
            for mutate in mutations:
                with self.subTest(role=role, mutation=mutate):
                    d = deepcopy(result.to_dict()); mutate(d['execution'][role])
                    with self.assertRaises(ValueError): QualityAssessment.from_dict(d)
        for field in ('quality_rationale', 'quality_uncertainty', 'concise_summary'):
            d = deepcopy(result.to_dict()); d[field] = 'Altered scientific text.'
            with self.assertRaises(ValueError): QualityAssessment.from_dict(d)

    def test_request_run_model_and_raw_content_substitution_fail_closed(self):
        result = self.run_gate(); another_run = self.run_gate()
        for index in (0, 1):
            for field, value in [('request_sha256','0'*64), ('model','another/model'),
                                 ('context_id','0'*64), ('raw_content','{}'),
                                 ('canonical_response_sha256','0'*64), ('response_binding_sha256','0'*64)]:
                d = deepcopy(result.to_dict()); d['execution']['calls'][index][field] = value
                with self.assertRaises(ValueError): QualityAssessment.from_dict(d)
            d = deepcopy(result.to_dict())
            d['execution']['calls'][index] = deepcopy(another_run.execution['calls'][index])
            with self.assertRaises(ValueError): QualityAssessment.from_dict(d)
        for mutate in [lambda d: d['execution'].pop('receipt_version'),
                       lambda d: d['execution'].update(run_id='0'*32),
                       lambda d: d.update(canonical_id='another-paper'),
                       lambda d: d['evidence'][0].update(excerpt=d['evidence'][0]['excerpt']+' '),
                       lambda d: d['execution']['calls'].pop()]:
            d = deepcopy(result.to_dict()); mutate(d)
            with self.assertRaises(ValueError): QualityAssessment.from_dict(d)

    def test_strict_parser_rejects_duplicates_non_json_and_surrogates(self):
        result = self.run_gate(); context = build_evidence_context('fixture', fixture()[2])
        for role in ('primary','adjudicator'):
            value = result.execution[role]; content = canonical_json(value)
            cases = [content[:-1]+',"canonical_id":"fixture"}', content+' garbage',
                     content.replace('"fixture"','NaN'), content.replace('"fixture"','"\\ud800"')]
            for raw in cases:
                with self.assertRaises(Exception): parse_response(raw, role, context)
        # Decision tokens are schema enums: surrounding whitespace is NOT allowed.
        d = deepcopy(result.execution['primary']); d['decision'] = ' pass '
        with self.assertRaises(Exception): parse_response(json.dumps(d), 'primary', context)

    def test_legacy_optional_display_excerpt_retains_its_contract(self):
        item = self.run_gate().evidence[0].to_dict(); item['excerpt'] = ' legacy text \n'
        self.assertEqual(QualityEvidence.from_dict(item).excerpt, 'legacy text')
        self.assertEqual(QualityEvidence.from_dict(item, exact_excerpt=True).excerpt, ' legacy text \n')


if __name__ == '__main__':
    unittest.main()
