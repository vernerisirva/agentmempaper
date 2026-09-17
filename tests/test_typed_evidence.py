"""Deterministic recovery regressions. No live model calls or outcome repairs."""
import copy
from dataclasses import replace
import json
from pathlib import Path
import sqlite3
import unittest
from unittest.mock import patch

from paper_scout.evidence_atoms import atoms_for_block, numeric_mentions, url_mentions
from paper_scout.evidence_context import build_evidence_context, digest
from paper_scout.evidence_semantics import numerical_support
from paper_scout.evidence_support import source_urls
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_llm import assess_with_optional_quality_llm
from paper_scout.quality_models import QualityAssessment
from test_batch2_recovery import validate, artifact_proposal
from test_paper_scout_scientific_gate import candidate, manuscript
from test_quality_reliability import block_fixture, envelope, ENV, SequenceHttp

CASES=json.loads((Path(__file__).parent/'fixtures/batch2_typed_evidence.json').read_text(encoding='utf-8'))


class TypedAtomsTests(unittest.TestCase):
    def test_url_punctuation_and_balanced_path_query_characters(self):
        url='https://github.com/org/repo'
        for text in (url,'('+url+')',url+'.',url+','):
            self.assertEqual(source_urls(text),[url])
        special='https://example.org/a(b)/x;v=1?q=a,b&c=%25#part'
        self.assertEqual(source_urls('('+special+').'),[special])
        self.assertEqual(source_urls('https://example.org/path/'),['https://example.org/path/'])

    def test_actual_arex_does_not_join_next_label(self):
        case=next(c for c in CASES if c['canonical_id']=='openalex:W7171268386')
        text=case['blocks'][0]['text'];urls=source_urls(text)
        self.assertEqual(urls,['https://arex-research.com','https://vectorspacelab.github.io/arex-model/','https://huggingface.co/collections/BAAI/arex'])
        self.assertNotIn('Models:', ''.join(urls))
        for atom in url_mentions(text):self.assertEqual(atom['literal'],text[atom['start']:atom['end']])

    def test_actual_split_hostname_cannot_be_accepted_as_partial_url(self):
        case=next(c for c in CASES if c['canonical_id']=='doi:10.48550/arxiv.2607.20872')
        urls=[u for b in case['blocks'] for u in source_urls(b['text'])]
        self.assertIn('https://tongyi.aliyun.com/farui/home',urls)
        self.assertNotIn('https://tongyi.aliyun',urls)

    def test_explicit_units_and_all_percentage_spellings(self):
        for form in ('95%','95 %','95 percent','95 per cent'):
            self.assertEqual(numerical_support('95% accuracy',[form+' accuracy'])['status'],'requires_semantic_verification')
        for source in ('95 percentage points','0.95 accuracy','5% relative improvement'):
            self.assertEqual(numerical_support('95% accuracy',[source])['status'],'unsupported')
        self.assertEqual(numerical_support('5 percentage-point improvement',['5% relative improvement'])['status'],'unsupported')

    def test_actual_glued_numbers_and_ranges_no_longer_false_reject(self):
        for case in CASES:
            if case['canonical_id']!='openalex:W7171268620':continue
            with self.subTest(item=case['item_id']):
                check=numerical_support(case['claim'],[b['text'] for b in case['blocks']])
                self.assertNotEqual(check['status'],'unsupported',check)
        self.assertEqual([n['unit'] for n in numeric_mentions('60–76%')],['%','%'])
        self.assertEqual([n['value'] for n in numeric_mentions('60-76%')],['6E+1','76'])

    def test_same_quantity_wrong_metric_entity_and_relative_meaning_need_semantics(self):
        selected,_=manuscript();ctx=build_evidence_context('fixture',selected)
        for claim in ('Precision is 74%.','Retention is 74% on an unrelated dataset.',
                      'The control system has 74% retention.','Retention increased by 74% relative to the baseline.'):
            v=block_fixture();v['evidence'][2]['claim']=claim
            self.assertNotEqual(numerical_support(claim,[ctx.blocks[2].text])['status'],'unsupported')
            result=validate(selected,ctx,v,{'evidence-2':'unsupported'})
            self.assertFalse(result.execution['reference_audit'][2]['accepted'])
            self.assertEqual(result.execution['outcome'],'scientific')

    def test_atoms_have_stable_provenance_and_utf8_roundtrip(self):
        symbols='α β μ ± × ≤ ≥ → – — “ ” é Å'
        selected,ctx,v=artifact_proposal('Code: https://example.org/repo '+symbols)
        atoms=atoms_for_block(ctx.blocks[-1],ctx)
        self.assertEqual({a['kind'] for a in atoms},{'text_span','url'})
        for atom in atoms:
            self.assertEqual(atom['raw'],ctx.blocks[-1].text[atom['start']:atom['end']])
            self.assertEqual(atom['context_id'],ctx.context_id)
            self.assertEqual(atom['manuscript_hash'],selected.content_hash)
            self.assertEqual(atom['block_hash'],digest(ctx.blocks[-1].text))
            self.assertEqual(atom['context_hash'],digest(ctx.text))
        encoded=json.dumps(atoms,ensure_ascii=False).encode('utf-8')
        con=sqlite3.connect(':memory:');con.execute('create table atoms(payload text)');con.execute('insert into atoms values (?)',(encoded.decode('utf-8'),))
        self.assertEqual(json.loads(con.execute('select payload from atoms').fetchone()[0]),atoms)
        con.close()
        self.assertEqual(atoms_for_block(ctx.blocks[-1],ctx),atoms)
        with self.assertRaises(ValueError):atoms_for_block(replace(ctx.blocks[-1],text='foreign'),ctx)
        result=validate(selected,ctx,v)
        restored=QualityAssessment.from_dict(json.loads(json.dumps(result.to_dict(),ensure_ascii=False).encode('utf-8')))
        self.assertEqual(restored,result)
        self.assertIn(symbols,json.dumps(restored.execution,ensure_ascii=False))


class ClaimTaxonomyTests(unittest.TestCase):
    def setUp(self):
        self.selected,_=manuscript();self.ctx=build_evidence_context('fixture',self.selected);self.value=block_fixture()

    def test_missing_optional_citation_drops_only_bad_model_claim(self):
        bad={**self.value['evidence'][0],'dimension':'reproducibility_and_transparency',
             'claim':'The paper releases a complete implementation.','evidence_ids':[]}
        self.value['evidence'].append(bad)
        result=validate(self.selected,self.ctx,self.value)
        self.assertEqual(result.quality_status,'pass')
        self.assertEqual(result.execution['outcome'],'scientific')
        self.assertEqual(result.execution['reference_audit'][-1]['disposition'],'claim_rejected')
        self.assertEqual(len(result.evidence),6)
        self.assertEqual(result.execution['claim_counts']['claim_rejected'],1)

    def test_missing_required_dimension_is_scientific_uncertainty(self):
        self.value['evidence'][1]['evidence_ids']=[]
        result=validate(self.selected,self.ctx,self.value)
        self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'scientific')
        self.assertIn('methodological_rigor',result.quality_uncertainty)

    def test_unsupported_optional_prose_does_not_veto_complete_grounded_assessment(self):
        self.value['evidence'].append({**self.value['evidence'][2],'dimension':'scholarly_novelty_or_value',
            'claim':'The method consistently outperforms every previous method.'})
        result=validate(self.selected,self.ctx,self.value,{'evidence-6':'unsupported'})
        self.assertEqual(result.quality_status,'pass');self.assertEqual(len(result.evidence),6)
        self.assertEqual(result.execution['reference_audit'][-1]['disposition'],'claim_rejected')

    def test_bad_url_is_claim_rejection_but_unknown_id_is_technical(self):
        selected,ctx,v=artifact_proposal('Code: https://example.org/repo')
        v['evidence'][-1]['artifact_urls']=['https://other.org/repo']
        result=validate(selected,ctx,v)
        self.assertEqual(result.execution['outcome'],'scientific');self.assertEqual(result.quality_status,'pass')
        v['evidence'][-1]['evidence_ids']=['foreign-context']
        result=validate(selected,ctx,v)
        self.assertEqual(result.execution['outcome'],'evidence_validation_failure');self.assertEqual(result.quality_status,'uncertain')

    def test_bad_optional_window_is_a_claim_rejection(self):
        self.value['evidence'].append({**self.value['evidence'][0],
            'dimension':'presentation_and_precision',
            'evidence_ids':[self.ctx.blocks[0].evidence_id,self.ctx.blocks[1].evidence_id],
            'include_adjacent_context':True})
        result=validate(self.selected,self.ctx,self.value)
        self.assertEqual(result.execution['outcome'],'scientific');self.assertEqual(result.quality_status,'pass')
        self.assertEqual(result.execution['reference_audit'][-1]['disposition'],'claim_rejected')

    def test_corrupt_provenance_cannot_be_hidden_as_scientific_uncertainty(self):
        ctx=replace(self.ctx,source_hash='corrupted')
        result=validate(self.selected,ctx,self.value)
        self.assertEqual(result.execution['outcome'],'evidence_validation_failure')
        self.assertEqual(result.execution['claim_counts']['technical_failure'],6)

    def test_all_citationless_claims_are_scientific_uncertainty_without_verifier_calls(self):
        for e in self.value['evidence']:e['evidence_ids']=[]
        client=SequenceHttp([envelope(self.value)])
        with patch.dict('os.environ',ENV,clear=True):
            result=assess_with_optional_quality_llm(candidate(),self.selected,
                assess_quality_deterministically(candidate(),'fixture',self.selected),'llm',http=client)
        self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'scientific')
        self.assertEqual(len(client.verifier_payloads),0)
        self.assertEqual(result.execution['claim_counts']['claim_rejected'],6)

    def test_code_link_alone_never_proves_scientific_reproducibility(self):
        selected,ctx,v=artifact_proposal('Code: https://example.org/repo','Methods')
        v['evidence'][-1].update(evidence_purpose='scientific_claim',artifact_urls=[],
            claim='The implementation reproduces all reported results.',explanation='The work is reproducible.')
        result=validate(selected,ctx,v,{'evidence-6':'unsupported','explanation-6':'unsupported'})
        self.assertFalse(result.execution['reference_audit'][-1]['accepted'])
        self.assertEqual(result.execution['outcome'],'scientific')
        self.assertEqual(result.quality_status,'pass')  # Other six criteria remain supported.

    def test_provider_failure_cannot_be_insufficient(self):
        self.value['quality_status']='insufficient';self.value['evidence'][1]['signal_type']='concern'
        from test_evidence_semantics import StrictHttp
        client=StrictHttp([envelope(self.value),'not JSON'])
        with patch.dict('os.environ',ENV,clear=True):
            result=assess_with_optional_quality_llm(candidate(),self.selected,
                assess_quality_deterministically(candidate(),'fixture',self.selected),'llm',http=client)
        self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'protocol_failure')
        self.assertEqual(len(client.payloads),2)

    def test_legacy_assessments_do_not_migrate_or_lose_provenance(self):
        result=validate(self.selected,self.ctx,self.value);raw=result.to_dict()
        raw['execution'].pop('claim_outcome_version');raw['execution'].pop('atom_version')
        for a in raw['execution']['reference_audit']:a.pop('evidence_atoms',None)
        self.assertEqual(QualityAssessment.from_dict(raw).to_dict(),raw)

    def test_maximum_schema_assessment_uses_at_most_thirteen_verifier_calls(self):
        from paper_scout.full_text import SelectedSection
        extra=[SelectedSection('Methods',f'Additional protocol {i} records independent runs.',20+i) for i in range(6)]
        sections=[*self.selected.sections,*extra]
        selected=replace(self.selected,sections=sections,text='\n'.join(s.text for s in sections))
        ctx=build_evidence_context('fixture',selected);value=copy.deepcopy(self.value)
        value['evidence_context_id']=ctx.context_id
        for i,e in enumerate(value['evidence']):e['evidence_ids']=[ctx.blocks[i].evidence_id]
        for i in range(6):
            value['evidence'].append({**value['evidence'][1],
                'evidence_ids':[ctx.blocks[6+i].evidence_id],
                'claim':'The protocol records independent runs.',
                'explanation':'The cited protocol describes independent runs.'})
        client=SequenceHttp([envelope(value)])
        with patch.dict('os.environ',ENV,clear=True):
            result=assess_with_optional_quality_llm(candidate(),selected,
                assess_quality_deterministically(candidate(),'fixture',selected),'llm',http=client)
        self.assertEqual(result.quality_status,'pass')
        self.assertEqual(len(client.verifier_payloads),13)
        self.assertEqual(len(result.execution['calls']),14)
        self.assertEqual(result.execution['total_request_limit'],15)

    def test_verifier_source_isolation_prevents_cross_item_evidence_leakage(self):
        client=SequenceHttp([envelope(self.value)])
        with patch.dict('os.environ',ENV,clear=True):
            result=assess_with_optional_quality_llm(candidate(),self.selected,
                assess_quality_deterministically(candidate(),'fixture',self.selected),'llm',http=client)
        self.assertEqual(result.quality_status,'pass');self.assertEqual(len(client.verifier_payloads),7)
        for payload in client.verifier_payloads[:-1]:
            items=json.loads(payload['messages'][1]['content'])['items']
            sources={tuple(s['evidence_id'] for s in i['sources']) for i in items}
            self.assertEqual(len(sources),1)
            self.assertEqual(len(items),2)
            self.assertEqual(items[1]['statement_kind'],'assessor_inference')
        for case in CASES:
            for b in case['blocks']:self.assertEqual(b['content_hash'],digest(b['text']))
