"""Synthetic promotion integration tests. No corpus selection or network requests."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.config import QualityConfig
from paper_scout.evidence_context import build_evidence_context, digest
from paper_scout.full_text import FullTextDocument, ExtractedPage, select_assessment_text
from paper_scout.models import ClassificationResult, PaperCandidate
from paper_scout.promotion_gate import assess_promotion, MAX_INPUT_BYTES
from paper_scout.promotion_protocol import (
    ASSESSMENT_VERSION, GATE_VERSION, PRIMARY_MODEL, ADJUDICATOR_MODEL,
    identity_from_document, validate_context, validate_pair, FIELDS,
)
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_models import QualityAssessment
from paper_scout.quality_service import assess_and_store_candidate
from paper_scout.site import _load_library_papers, _main_library, _review_candidate, _quality_to_json
from paper_scout.state import PaperStore

ENV = {'PAPER_SCOUT_LLM_API_KEY': 'synthetic-key', 'PAPER_SCOUT_LLM_MODEL': PRIMARY_MODEL,
       'PAPER_SCOUT_LLM_BASE_URL': 'https://openrouter.ai/api/v1'}


def fixture(key='fixture'):
    candidate = PaperCandidate('Synthetic temporal memory experiment', ['Anonymous'],
                               'A synthetic controlled experiment.', 'fixture', key)
    raw = candidate.title + '\n1 Introduction\nWe study scoped temporal retrieval.\n2 Methods\n'
    raw += 'Two matched conditions use fixed tasks and independent seeds.\n3 Results\n'
    raw += 'Accuracywas95% on the held-out tasks; α = 0.5 × β. ' * 30
    raw += '\n4 Limitations\nTransfer to different tasks remains untested. '
    raw += 'The paper lists https://example.test/artifact but does not validate its reproducibility.'
    document = FullTextDocument('https://example.test/paper.pdf', [ExtractedPage(1, raw)], digest(raw), True)
    text = select_assessment_text(candidate, document)
    text = replace(text, coverage={**text.coverage, 'manuscript_identity': identity_from_document(candidate, document)})
    seed = replace(assess_quality_deterministically(candidate, key, text, assessment_version=ASSESSMENT_VERSION),
                   full_text_url=document.source_url)
    return candidate, document, text, seed


class Models:
    retries = 1

    def __init__(self, primary='pass', adjudicator='pass', change=None, finish='stop'):
        self.decisions = (primary, adjudicator)
        self.change = change
        self.finish = finish
        self.payloads = []

    def post_json(self, url, payload, headers):
        role = len(self.payloads)
        self.payloads.append(deepcopy(payload))
        prompt = json.loads(payload['messages'][1]['content'])
        import re
        ids = re.findall(r'\[(E[a-f0-9]+-B\d+)\]', prompt['manuscript'])
        value = {k: prompt[k] for k in ('canonical_id', 'source_content_hash', 'context_id')}
        value['evidence_ids'] = ids[:3]
        if role == 0:
            value.update({k: 'Scoped scientific judgment with canonical evidence.' for k in FIELDS})
            value.update(decision=self.decisions[0], evaluation_assessment='Ninety-five percent accuracy supports this scoped comparison.',
                         limitations='Cross-task transfer is untested.')
        else:
            value.update(promotion_decision=self.decisions[1],
                         blocking_reasons=[] if self.decisions[1] == 'pass' else ['Important unsupported overclaim.'])
        if self.change:
            self.change(value, role)
        return json.dumps({'model': payload['model'], 'choices': [{'finish_reason': self.finish,
            'message': {'content': json.dumps(value, ensure_ascii=False), 'reasoning': 'DO NOT RETAIN'}}],
            'usage': {'prompt_tokens': 100, 'completion_tokens': 50, 'cost': 0.001}}, ensure_ascii=False)


class PromotionTests(unittest.TestCase):
    def run_gate(self, models=None, text=None, seed=None):
        c, _, original, original_seed = fixture()
        models = models or Models()
        with patch.dict('os.environ', ENV, clear=True):
            result = assess_promotion(c, text or original, seed or original_seed, 'llm', http=models)
        return result, models

    def library(self, result, decision='relevant', suppressed=False):
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp)/'state.sqlite3')
            c, _, _, _ = fixture()
            key = store.upsert_paper(c, ClassificationResult(95, decision, 'Synthetic topical match'))
            # Use real canonical IDs, regenerating context rather than relabeling evidence.
            c, _, text, seed = fixture(key)
            result2, _ = self.run_gate(Models(result.execution['primary']['decision'],
                                            result.execution['adjudicator']['promotion_decision']), text, seed)
            row = store.save_quality_assessment(result2)
            if suppressed:
                store.set_quality_suppression(key, row, 'explicit suppression')
            papers = _load_library_papers(store.path)
            return papers[0]

    def test_promotion_matrix_and_suppression(self):
        for p, a, expected in [('pass','pass',True), ('pass','uncertain',False), ('uncertain','pass',False)]:
            result, models = self.run_gate(Models(p,a))
            self.assertEqual(result.quality_status == 'pass', expected)
            self.assertEqual(result.execution['outcome'], 'success')
            self.assertEqual(len(models.payloads), 2)
            paper = self.library(result)
            self.assertEqual(_main_library(paper), expected)
            self.assertEqual(_review_candidate(paper), not expected)
        result, _ = self.run_gate()
        self.assertFalse(_main_library(self.library(result, suppressed=True)))
        self.assertFalse(_main_library(self.library(result, decision='maybe')))

    def test_invented_id_wrong_manuscript_version_and_context_fail_closed(self):
        for key, value in [('evidence_ids',['invented']), ('canonical_id','foreign'),
                           ('source_content_hash','0'*64), ('context_id','0'*64)]:
            for role in (0, 1):
                def mutate(v, r):
                    if r == role: v[key] = value
                result, _ = self.run_gate(Models(change=mutate))
                self.assertEqual(result.quality_status, 'uncertain')
                self.assertEqual(result.execution['outcome'], 'protocol_failure')
                self.assertFalse(result.full_text_assessed)

    def test_malformed_truncated_and_missing_finish_rejected(self):
        for finish in ('length', None, 'error', 'content_filter'):
            result, models = self.run_gate(Models(finish=finish))
            self.assertEqual(result.execution['outcome'], 'protocol_failure')
            self.assertEqual(len(models.payloads), 1)
        result, _ = self.run_gate(Models(change=lambda v,r: v.update(decision='FAIL') if r == 0 else None))
        self.assertEqual(result.execution['outcome'], 'protocol_failure')

    def test_disagreement_is_scientific_and_artifact_does_not_imply_reproducibility(self):
        def reject(v, role):
            if role: v['blocking_reasons'] = ['A source URL does not establish reproducibility; the primary overclaims.']
        result, _ = self.run_gate(Models(adjudicator='uncertain', change=reject))
        self.assertEqual(result.quality_status, 'uncertain')
        self.assertEqual(result.execution['outcome'], 'success')
        self.assertTrue(result.full_text_assessed)
        self.assertFalse(_main_library(self.library(result)))

    def test_numeric_wording_has_no_lexical_veto_and_unicode_roundtrips(self):
        with patch('paper_scout.evidence_semantics.numerical_support', side_effect=AssertionError('legacy parser invoked')):
            result, models = self.run_gate()
        self.assertEqual(result.quality_status, 'pass')
        self.assertIn('α = 0.5 × β', json.dumps(result.to_dict(), ensure_ascii=False))
        self.assertEqual(QualityAssessment.from_dict(json.loads(json.dumps(result.to_dict()))), result)
        self.assertNotIn('DO NOT RETAIN', json.dumps(result.to_dict()))
        self.assertNotIn('DO NOT RETAIN', json.dumps(models.payloads[1]))
        self.assertNotIn('authors', json.loads(models.payloads[0]['messages'][1]['content']))
        self.assertNotEqual(models.payloads[0]['model'], models.payloads[1]['model'])

    def test_receipt_tampering_and_source_snippet_integrity(self):
        result, _ = self.run_gate()
        mutations = [lambda d: d['execution']['adjudicator'].update(promotion_decision='uncertain'),
                     lambda d: d['execution']['context']['blocks'][0].update(text='invented'),
                     lambda d: d['execution']['calls'][1].update(finish_reason='length'),
                     lambda d: d['evidence'][0]['source_blocks'][0].update(text='invented'),
                     lambda d: d['evidence'][0].update(excerpt='invented'),
                     lambda d: d.update(canonical_id='foreign')]
        for mutate in mutations:
            value = deepcopy(result.to_dict()); mutate(value)
            with self.assertRaises((ValueError, KeyError)):
                QualityAssessment.from_dict(value)

    def test_empty_citations_or_blocking_reasons_with_pass_are_not_promoted(self):
        for mutate in (lambda v,r: v.update(evidence_ids=[]),
                       lambda v,r: v.update(blocking_reasons=['Unresolved scientific concern']) if r else None):
            result, _ = self.run_gate(Models(change=mutate))
            self.assertEqual(result.quality_status, 'uncertain')
            self.assertEqual(result.execution['outcome'], 'success')

    def test_wrong_document_missing_provenance_and_unavailable(self):
        c, doc, text, seed = fixture()
        wrong = replace(doc, pages=[ExtractedPage(1, 'A different manuscript')])
        self.assertFalse(identity_from_document(c, wrong)['verified'])
        for coverage in ({}, {**text.coverage,'manuscript_identity':{'verified':False}}):
            result, models = self.run_gate(text=replace(text,coverage=coverage))
            self.assertEqual(result.execution['outcome'], 'integrity_failure')
            self.assertEqual(models.payloads, [])
        result, _ = self.run_gate(text=replace(text,scope='title_and_abstract'))
        self.assertEqual(result.execution['outcome'], 'manuscript_unavailable')

    def test_different_families_required_and_request_bounds(self):
        for a in (PRIMARY_MODEL,'deepseek/rolling','anthropic/claude-latest'):
            with self.assertRaises(ValueError): validate_pair(PRIMARY_MODEL,a)
        _, _, text, seed = fixture()
        huge = replace(text, text=text.text + 'a'*MAX_INPUT_BYTES,
                       sections=[replace(text.sections[0], text=text.text+'a'*MAX_INPUT_BYTES)])
        result, models = self.run_gate(text=huge)
        self.assertEqual(result.execution['outcome'], 'protocol_failure')
        self.assertEqual(models.payloads, [])

    def test_runtime_alias_and_nested_retry_guards_send_no_calls(self):
        c, _, text, seed = fixture()
        models = Models()
        with patch.dict('os.environ', {**ENV, 'PAPER_SCOUT_QUALITY_ADJUDICATOR_MODEL': 'anthropic/claude-latest'}, clear=True):
            result = assess_promotion(c, text, seed, 'llm', http=models)
        self.assertEqual(result.execution['outcome'], 'protocol_failure')
        self.assertEqual(models.payloads, [])
        models.retries = 3
        result, _ = self.run_gate(models)
        self.assertEqual(result.execution['outcome'], 'protocol_failure')
        self.assertEqual(models.payloads, [])

    def test_malformed_envelope_and_wrong_returned_model_are_technical(self):
        for response in ('not json', '{}', '{"choices": []}',
                         '{"model": "another/model", "choices": []}'):
            client = Models()
            with patch.object(client, 'post_json', return_value=response):
                result, _ = self.run_gate(client)
            self.assertEqual(result.execution['outcome'], 'protocol_failure')
            self.assertEqual(result.quality_status, 'uncertain')
            self.assertEqual(len(result.execution['calls']), 1)

    def test_public_card_retains_both_final_judgments_without_private_context(self):
        result, _ = self.run_gate()
        public = _quality_to_json(self.library(result))['promotion']
        self.assertEqual(public['primary_model'], PRIMARY_MODEL)
        self.assertEqual(public['adjudicator_model'], ADJUDICATOR_MODEL)
        self.assertEqual(public['adjudicator']['promotion_decision'], 'pass')
        self.assertNotIn('context', public)
        self.assertNotIn('calls', public)

    def test_store_append_roundtrip_idempotency_and_manual_bypass(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = PaperStore(Path(tmp)/'state.sqlite3')
            c, doc, text, seed = fixture()
            with patch.dict('os.environ', ENV, clear=True), patch('paper_scout.quality_service.fetch_and_extract_pdf', return_value=doc), patch('paper_scout.promotion_gate.HttpClient', return_value=Models()):
                result = assess_and_store_candidate(QualityConfig(enabled=True, mode='llm'), store, c, 'fixture', ClassificationResult(90,'relevant','fixture'), direct_pdf_url=doc.source_url)
            self.assertEqual(result.quality_status, 'pass')
            first = store.save_quality_assessment(result)
            self.assertEqual(store.save_quality_assessment(result),first)
            again, _ = self.run_gate()
            self.assertNotEqual(store.save_quality_assessment(again), first)
            self.assertEqual(store.get_current_quality_assessment('fixture'),again)
            with self.assertRaises(ValueError):
                assess_and_store_candidate(QualityConfig(enabled=True), store, c, 'fixture', ClassificationResult(90,'relevant','fixture'), manual_assessment={})
            with patch('paper_scout.quality_service.fetch_and_extract_pdf', side_effect=AssertionError('historical pass reacquired')):
                self.assertEqual(assess_and_store_candidate(QualityConfig(enabled=True),store,c,'fixture',ClassificationResult(90,'relevant','fixture')),again)


if __name__ == '__main__':
    unittest.main()
