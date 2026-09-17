"""Batch-2 regressions are engineering data, never fresh holdout evidence."""
from dataclasses import replace
import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.evidence_context import build_evidence_context, digest, resolve_evidence_ids
from paper_scout.evidence_semantics import (candidate_for_support, evidence_guidance,
    numerical_support, verifier_items, VERIFIER_INSTRUCTIONS)
from paper_scout.evidence_support import (ARTIFACT, SCIENTIFIC, effective_claim,
    resolve_claim_blocks, source_urls, ARTIFACT_EXPLANATION)
from paper_scout.full_text import (canonical_manuscript_text, ExtractedPage, FullTextDocument,
    SelectedSection, SelectedPaperText, select_assessment_text)
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_llm import (validate_block_quality_response, _request_payload,
    assess_with_optional_quality_llm, block_review_schema)
from paper_scout.quality_models import QualityAssessment
from paper_scout.site import _quality_evidence_detail
from test_evidence_context import verified_fixture
from test_evidence_semantics import StrictHttp
from test_paper_scout_scientific_gate import candidate, manuscript
from test_quality_reliability import block_fixture, envelope, ENV

CASES = json.loads((Path(__file__).parent/'fixtures/batch2_artifact_failures.json').read_text())


def artifact_proposal(text, heading='Abstract', urls=None):
    selected, _ = manuscript()
    sections = [*selected.sections, SelectedSection(heading, text, 20)]
    selected = replace(selected, sections=sections, text='\n'.join(s.text for s in sections))
    ctx = build_evidence_context('fixture', selected)
    v = block_fixture();v['evidence_context_id'] = ctx.context_id
    for i, e in enumerate(v['evidence']):e['evidence_ids'] = [b.evidence_id for b in ctx.blocks if b.spans[0].section_index == i]
    v['evidence'].append({'dimension':'reproducibility_and_transparency','signal_type':'positive',
        'claim':'This code proves excellent methodological quality.', 'explanation':'A deliberately overbroad model proposal, never the stored artifact fact.',
        'support_status':'supported','statement_kind':'source_claim','evidence_purpose':ARTIFACT,
        'artifact_urls':urls or source_urls(text),'include_adjacent_context':False,
        'evidence_ids':[b.evidence_id for b in ctx.blocks if b.spans[0].section_index == len(sections)-1]})
    return selected, ctx, v


def validate(selected, ctx, value, overrides=None):
    seed = assess_quality_deterministically(candidate(), 'fixture', selected)
    return validate_block_quality_response(value, seed, 'fixture', selected, ctx,
        verification=verified_fixture(value, ctx, overrides))


class ArtifactTests(unittest.TestCase):
    def test_all_four_real_abstract_links_support_only_attributed_artifacts(self):
        for case in CASES:
            source=case['blocks'][0]
            self.assertEqual(source['section_role'],'abstract')
            self.assertEqual(digest(source['text']), source['content_hash'])
            selected,ctx,v=artifact_proposal(source['text'])
            result=validate(selected,ctx,v)
            self.assertEqual(result.quality_status,'pass')
            e=result.evidence[-1]
            self.assertEqual(e.claim_role,ARTIFACT)
            self.assertEqual(e.paraphrase,'The paper provides these artifact links: '+', '.join(source_urls(source['text'])))
            self.assertEqual(e.explanation,ARTIFACT_EXPLANATION)
            self.assertNotIn('excellent',e.paraphrase)
            self.assertNotIn('methodological',e.explanation)
            self.assertIn(source['text'],e.excerpt)
            self.assertEqual(result.execution['reference_audit'][-1]['claim'],v['evidence'][-1]['claim'])
            self.assertIn('not independently checked',_quality_evidence_detail(e.to_dict()))
            for item in verifier_items(v,ctx)[-2:]:
                self.assertNotIn(e.evidence_ids[0], [b['evidence_id'] for b in item['sources']])

    def test_abstract_link_cannot_supply_method_evaluation_or_inference(self):
        selected,ctx,v=artifact_proposal('Code: https://github.com/example/project')
        for dim in ('methodological_rigor','evaluation_or_validation_strength','evidence_to_claim_alignment'):
            bad=copy.deepcopy(v);bad['evidence'][-1]['dimension']=dim
            result=validate(selected,ctx,bad)
            self.assertEqual(result.execution['outcome'],'scientific')
            self.assertFalse(result.execution['reference_audit'][-1]['accepted'])
        bad=copy.deepcopy(v);bad['evidence'][-1]['evidence_purpose']=SCIENTIFIC;bad['evidence'][-1]['artifact_urls']=[]
        self.assertEqual(validate(selected,ctx,bad).execution['outcome'],'scientific')
        bad=copy.deepcopy(v);bad['evidence'][-1]['statement_kind']='assessor_inference'
        self.assertEqual(validate(selected,ctx,bad).execution['outcome'],'scientific')

    def test_artifact_does_not_replace_missing_core_criterion(self):
        selected,ctx,v=artifact_proposal('Code: https://github.com/example/project')
        v['evidence']=[e for e in v['evidence'] if e['dimension']!='methodological_rigor']
        result=validate(selected,ctx,v)
        self.assertEqual(result.quality_status,'uncertain')
        self.assertIn('methodological_rigor',result.quality_uncertainty)

    def test_invented_or_foreign_url_and_foreign_context_fail(self):
        selected,ctx,v=artifact_proposal('Code: https://github.com/example/project')
        v['evidence'][-1]['artifact_urls']=['https://github.com/other/paper']
        self.assertEqual(validate(selected,ctx,v).execution['outcome'],'scientific')
        selected,ctx,v=artifact_proposal('Code: https://github.com/example/project')
        other=build_evidence_context('different-paper',selected)
        v['evidence'][-1]['evidence_ids']=[other.blocks[-1].evidence_id]
        self.assertEqual(validate(selected,ctx,v).execution['outcome'],'evidence_validation_failure')

    def test_malformed_source_url_is_not_an_artifact_candidate(self):
        self.assertEqual(source_urls('Code: https://user:password@example.test/repo'),[])
        self.assertEqual(source_urls('Code: https://bad.example:abc/repo'),[])

    def test_front_metadata_exception_does_not_open_references_or_gaps(self):
        for heading in ('Front Matter','Title Page','Metadata','Appendix'):
            selected,ctx,v=artifact_proposal('Code: https://github.com/example/project',heading)
            self.assertEqual(validate(selected,ctx,v).quality_status,'pass')
            if heading!='Appendix':
                with self.assertRaises(ValueError):resolve_evidence_ids(v['evidence'][-1]['evidence_ids'],ctx,expected_context_id=ctx.context_id)
        for heading,text in [('References','Code: https://github.com/example/project'),('Front Matter','[Extraction gap: source text omitted] Code: https://github.com/example/project')]:
            selected,ctx,v=artifact_proposal(text,heading)
            self.assertEqual(validate(selected,ctx,v).execution['outcome'],'scientific')

    def test_body_artifact_text_is_excluded_from_scientific_narrative_support(self):
        selected,ctx,v=artifact_proposal('Code: https://github.com/example/project', 'Methods')
        artifact_id=v['evidence'][-1]['evidence_ids'][0]
        self.assertEqual(validate(selected,ctx,v).quality_status,'pass')
        for item in verifier_items(v,ctx)[-2:]:
            self.assertNotIn(artifact_id,[b['evidence_id'] for b in item['sources']])

    def test_wire_calls_isolate_scientific_sources_and_skip_typed_artifacts(self):
        selected,ctx,v=artifact_proposal('Code: https://github.com/example/project')
        verified=verified_fixture(v,ctx)
        wire=json.dumps({'_fixture_pool':True,'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'items':verified['items']})}}]})
        client=StrictHttp([envelope(v),wire])
        with patch.dict('os.environ',ENV,clear=True):
            result=assess_with_optional_quality_llm(candidate(),selected,assess_quality_deterministically(candidate(),'fixture',selected),'llm',http=client)
        self.assertEqual(result.quality_status,'pass');self.assertEqual(len(client.payloads),8)
        self.assertEqual(len(verified['items']),2*len(v['evidence'])+2)
        self.assertNotIn('excellent',json.dumps(client.payloads[1]))


class UnicodeTests(unittest.TestCase):
    def test_scientific_unicode_and_utf16_pairs_normalize_stably(self):
        text='α β μ ± × ≤ ≥ → – — “” é Å x₂ 𝒜 \ud835\udc9c'
        canonical=canonical_manuscript_text(text)
        self.assertEqual(canonical,canonical_manuscript_text(canonical))
        self.assertEqual(canonical.count('𝒜'),2)
        for symbol in 'αβμ±×≤≥→–—éÅ₂':self.assertIn(symbol,canonical)
        self.assertEqual(json.loads(json.dumps(canonical,ensure_ascii=False).encode('utf-8')),canonical)

    def test_actual_memforest_lone_surrogates_are_visible_before_hash_transport_storage_and_site(self):
        text='KMeans clustering divides historical memory \ud835 into initial event units {\ud835\ud835}.'
        body='Methods\n'+text+' α β μ ± × ≤ ≥ → – — “” é Å x₂ 𝒜'
        doc=FullTextDocument('https://example.test/paper.pdf',[ExtractedPage(1,body)],'original-pdf-sha',True)
        selected=select_assessment_text(candidate(),doc)
        self.assertIn('\ufffd',selected.text);self.assertEqual(selected.coverage['surrogate_code_units'],3)
        self.assertEqual(selected.coverage['assessment_input_sha256'],hashlib.sha256(selected.text.encode('utf-8')).hexdigest())
        ctx=build_evidence_context('fixture',selected);self.assertEqual(ctx,build_evidence_context('fixture',selected))
        # Canonical text is the same through assessor, verifier, JSON, SQLite and display.
        seed=assess_quality_deterministically(candidate(),'fixture',selected)
        request=_request_payload(candidate(),selected,seed,'fixture',context=ctx)
        self.assertIn(ctx.text,json.loads(request['messages'][1]['content'])['paper']['text'])
        selected2,ctx2,v=artifact_proposal('Code: https://github.com/example/project')
        unicode_selected=replace(selected2,sections=[replace(s,text=s.text+' '+canonical_manuscript_text(body)) for s in selected2.sections])
        unicode_selected=replace(unicode_selected,text='\n'.join(s.text for s in unicode_selected.sections))
        uc=build_evidence_context('fixture',unicode_selected);v['evidence_context_id']=uc.context_id
        for i,item in enumerate(v['evidence']):item['evidence_ids']=[b.evidence_id for b in uc.blocks if b.spans[0].section_index==i]
        # Use a claim with no unsupported numerical assertions for mocked entailment.
        v['evidence'][0]['claim']='The protocol describes the contribution.'
        result=validate(unicode_selected,uc,v)
        encoded=json.dumps(verifier_items(v,uc),ensure_ascii=False).encode('utf-8');self.assertIn('α'.encode(),encoded)
        con=sqlite3.connect(':memory:');con.execute('create table records (payload text)');con.execute('insert into records values (?)',(json.dumps(result.to_dict(),ensure_ascii=False),))
        restored=QualityAssessment.from_dict(json.loads(con.execute('select payload from records').fetchone()[0]));con.close()
        self.assertEqual(restored,result);self.assertIn('α',_quality_evidence_detail(restored.evidence[0].to_dict()));self.assertIn('�',_quality_evidence_detail(restored.evidence[0].to_dict()))


class WindowsAndSupportTests(unittest.TestCase):
    def context(self):
        text=('The benchmark uses Method Y. '+ 'Padding sentence. '*44+'Accuracy improved to 82%. '+ 'Following context. '*90)
        selected=SelectedPaperText(text,[SelectedSection('Results',text,1)],'full_text','hash',False)
        return build_evidence_context('fixture',selected)

    def test_window_is_contiguous_bounded_and_inside_supplied_section(self):
        ctx=self.context();self.assertGreaterEqual(len(ctx.blocks),3)
        item={'evidence_ids':[ctx.blocks[1].evidence_id],'include_adjacent_context':True}
        blocks=resolve_claim_blocks(item,ctx,ctx.context_id)
        self.assertEqual([b.sequence for b in blocks],[1,2,3])
        self.assertEqual([b.content_hash for b in blocks],[b.content_hash for b in ctx.blocks[:3]])
        self.assertTrue(all(b in ctx.blocks for b in blocks))
        item['evidence_ids']=[ctx.blocks[0].evidence_id,ctx.blocks[-1].evidence_id]
        with self.assertRaises(ValueError):resolve_claim_blocks(item,ctx,ctx.context_id)
        item['evidence_ids']=['E'+ctx.context_id[:16]+'-B9999']
        with self.assertRaises(ValueError):resolve_claim_blocks(item,ctx,ctx.context_id)

    def test_window_never_crosses_section_or_extraction_gap(self):
        sections=[SelectedSection('Results','Accuracy was 82%.',1),SelectedSection('Results','Different selected excerpt.',3),SelectedSection('Methods','Unrelated protocol.',4)]
        selected=SelectedPaperText('\n'.join(s.text for s in sections),sections,'partial_full_text','hash',False)
        ctx=build_evidence_context('fixture',selected);item={'evidence_ids':[ctx.blocks[0].evidence_id],'include_adjacent_context':True}
        self.assertEqual(len(resolve_claim_blocks(item,ctx,ctx.context_id)),1)

    def test_supported_independent_runs_and_scoped_inference_remain_accepted(self):
        selected,_=manuscript();sections=list(selected.sections)
        sections[2]=replace(sections[2],text='Results are averaged over five independently seeded runs. The experiment covers one benchmark.')
        selected=replace(selected,sections=sections,text='\n'.join(s.text for s in sections))
        ctx=build_evidence_context('fixture',selected);v=block_fixture();v['evidence_context_id']=ctx.context_id
        for i,e in enumerate(v['evidence']):e['evidence_ids']=[ctx.blocks[i].evidence_id]
        v['evidence'][2].update(claim='The experiment used five independent runs.',explanation='The reported results average independently seeded runs.')
        self.assertTrue(validate(selected,ctx,v).execution['reference_audit'][2]['accepted'])
        v['evidence'][2].update(claim='The cited evaluation has limited benchmark breadth.',explanation='The cited experiment covers one benchmark.',statement_kind='assessor_inference')
        self.assertTrue(validate(selected,ctx,v).execution['reference_audit'][2]['accepted'])

    def test_original_numeric_locator_and_article_boundaries_do_not_reject_scoped_support(self):
        self.assertNotEqual(numerical_support('Experiment 1 shows success on 32/32 cases.',['Success on 32/32 cases.'])['status'],'unsupported')
        self.assertNotEqual(numerical_support('Contributions: (1) formalization, (2) relation, (3) experiments.',['Formalization, relation and experiments.'])['status'],'unsupported')
        self.assertNotEqual(numerical_support('A 10-user shared-agent setting.',['We construct a10-user shared-agent memory store.'])['status'],'unsupported')
        for claim,evidence in [('Accuracy (95) improved.','Accuracy improved.'),('Accuracy is 96%.','Accuracy is 95%.'),('Improved by 5 percentage points.','Improved by 5%.'),('K=10.','The retriever is described.'),('Improved 3x.','The positive control is described.')]:
            self.assertEqual(numerical_support(claim,[evidence])['status'],'unsupported')

    def test_partial_support_is_rejected_by_scoped_semantic_verifier(self):
        selected,_=manuscript();sections=list(selected.sections);sections[2]=replace(sections[2],text='Performance improved on two of three evaluated tasks.')
        selected=replace(selected,sections=sections,text='\n'.join(s.text for s in sections));ctx=build_evidence_context('fixture',selected);v=block_fixture();v['evidence_context_id']=ctx.context_id
        for i,e in enumerate(v['evidence']):e['evidence_ids']=[ctx.blocks[i].evidence_id]
        v['evidence'][2].update(claim='The method consistently improves performance across all tasks.',explanation='The evaluated tasks establish the universal claim.')
        result=validate(selected,ctx,v,{'evidence-2':'unsupported'})
        self.assertFalse(result.execution['reference_audit'][2]['accepted']);self.assertEqual(result.quality_status,'uncertain')

    def test_explanation_overreach_is_checked_independently(self):
        selected,_=manuscript();ctx=build_evidence_context('fixture',selected);v=block_fixture()
        result=validate(selected,ctx,v,{'explanation-0':'unsupported'})
        row=result.execution['reference_audit'][0];self.assertEqual(row['support_verification']['claim_status'],'supported')
        self.assertFalse(row['accepted']);self.assertEqual(result.quality_status,'uncertain')

    def test_actual_audit_overreach_is_rejected_semantically(self):
        selected,_=manuscript();ctx=build_evidence_context('fixture',selected)
        for claim in ['This synthesis is not available in a single source elsewhere.', 'The manuscript does not provide a dedicated limitations section.']:
            v=block_fixture();v['evidence'][0]['claim']=claim
            result=validate(selected,ctx,v,{'evidence-0':'unsupported'})
            self.assertFalse(result.execution['reference_audit'][0]['accepted'])
            self.assertEqual(result.execution['outcome'],'scientific')
        self.assertIn('directional entailment',VERIFIER_INSTRUCTIONS)
