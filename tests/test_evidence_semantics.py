from dataclasses import replace
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from paper_scout.evidence_context import EVIDENCE_VERSION, build_evidence_context, resolve_evidence_ids
from paper_scout.evidence_semantics import eligible_for, candidate_for_support, evidence_guidance, numerical_support, numeric_mentions, verifier_items
from paper_scout.full_text import SelectedPaperText, SelectedSection
from paper_scout.http import HttpRequestError
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_llm import (_request_payload, assess_with_optional_quality_llm,
    validate_block_quality_response, _support_input_hash)
from paper_scout.quality_models import QualityAssessment
from test_evidence_context import verified_fixture
from test_paper_scout_scientific_gate import candidate, manuscript, assessment
from test_quality_reliability import ENV, block_fixture, envelope

CASES = json.loads((Path(__file__).parent / 'fixtures/evidence_semantics_cases.json').read_text())


class StrictHttp:
    """Wire responses are explicit; a declared verifier pool serves isolated subsets."""
    retries = 1
    def __init__(self, responses):self.responses=list(responses);self.payloads=[]
    def post_json(self, url, payload, headers=None):
        self.payloads.append(payload)
        item=self.responses.pop(0)
        if isinstance(item,Exception):raise item
        if isinstance(item, str) and payload['response_format']['json_schema']['name'] == 'claim_support':
            try:pool=json.loads(item)
            except ValueError:return item
            if isinstance(pool,dict) and pool.get('_fixture_pool'):
                requested={v['item_id'] for v in json.loads(payload['messages'][1]['content'])['items']}
                content=json.loads(pool['choices'][0]['message']['content'])
                selected=[v for v in content['items'] if v['item_id'] in requested]
                assert selected, 'Verifier fixture pool has no decisions for requested item IDs'
                remaining=[v for v in content['items'] if v['item_id'] not in requested]
                if remaining:
                    import copy
                    next_pool=copy.deepcopy(pool);next_pool['choices'][0]['message']['content']=json.dumps({'items':remaining})
                    self.responses.insert(0,json.dumps(next_pool))
                pool.pop('_fixture_pool');pool['choices'][0]['message']['content']=json.dumps({'items':selected})
                return json.dumps(pool)
        return item


def verifier_response(value=None, overrides=None, finish='stop'):
    selected,_=manuscript();ctx=build_evidence_context('fixture',selected)
    v=verified_fixture(value or block_fixture(),ctx,overrides)
    return json.dumps({'_fixture_pool':True,'usage':{'prompt_tokens':80,'completion_tokens':30,'cost':.005},
        'choices':[{'finish_reason':finish,'message':{'content':json.dumps({'items':v['items']})}}]})


class SemanticsTests(unittest.TestCase):
    def setUp(self):
        self.selected,_=manuscript();self.context=build_evidence_context('fixture',self.selected)
        self.seed=assess_quality_deterministically(candidate(),'fixture',self.selected)
        self.value=block_fixture()

    def validate(self,value=None,overrides=None,verified=True):
        value=value or self.value
        return validate_block_quality_response(value,self.seed,'fixture',self.selected,self.context,
            verification=verified_fixture(value,self.context,overrides) if verified else None)

    def test_real_abstract_cases_have_body_alternatives_and_claim_specific_eligibility(self):
        for case in CASES:
            for rejected in case['rejected_items']:
                for source in rejected['blocks']:
                    role=source['role'];heading={'body':'Adapted Apex','related':'Related Work'}.get(role,role)
                    selected=SelectedPaperText(source['text'],[SelectedSection(heading,source['text'],source['pages'][0])],
                                               'full_text',case['source_hash'],False)
                    ctx=build_evidence_context(case['canonical_id'],selected);block=ctx.blocks[0]
                    self.assertEqual(block.section_role,role)
                    self.assertTrue(resolve_evidence_ids([block.evidence_id],ctx,expected_context_id=ctx.context_id))
                    if role=='abstract':
                        self.assertTrue(eligible_for(block,'contribution_clarity','source_claim'))
                        self.assertFalse(eligible_for(block,'contribution_clarity','assessor_inference'))
                        for dimension in ('scholarly_novelty_or_value','methodological_rigor','evaluation_or_validation_strength',
                                          'evidence_to_claim_alignment','limitations_and_uncertainty_handling','reproducibility_and_transparency'):
                            for kind in ('source_claim','assessor_inference'):
                                self.assertFalse(eligible_for(block,dimension,kind))
                    else:self.assertTrue(candidate_for_support(block,rejected['dimension'],'source_claim'))

    def test_abstract_contribution_can_coexist_with_body_backed_gate(self):
        # Same canonical introduction statement can be attributed from Abstract;
        # methods, evaluation, alignment, related work and limitations stay body.
        self.selected=replace(self.selected,sections=[replace(self.selected.sections[0],heading='Abstract'),*self.selected.sections[1:]])
        self.context=build_evidence_context('fixture',self.selected);self.value['evidence_context_id']=self.context.context_id
        for item,block in zip(self.value['evidence'],self.context.blocks):item['evidence_ids']=[block.evidence_id]
        result=self.validate();self.assertEqual(result.quality_status,'pass')
        self.assertEqual(result.evidence[0].source_blocks[0]['section_role'],'abstract')

    def test_pass_cannot_be_assembled_from_abstract_claims(self):
        self.selected=replace(self.selected,sections=[replace(s,heading='Abstract') for s in self.selected.sections])
        self.context=build_evidence_context('fixture',self.selected);self.value['evidence_context_id']=self.context.context_id
        for e,b in zip(self.value['evidence'],self.context.blocks):e['evidence_ids']=[b.evidence_id]
        result=self.validate();self.assertEqual(result.quality_status,'uncertain')
        self.assertEqual(result.execution['outcome'],'scientific')

    def test_role_guidance_supplies_only_compatible_visible_candidates(self):
        payload=_request_payload(candidate(),self.selected,self.seed,'fixture',context=self.context)
        guidance=json.loads(payload['messages'][1]['content'])['evidence_guidance']
        index={b.evidence_id:b for b in self.context.blocks}
        for d,ids in guidance['body_candidate_ids_by_dimension'].items():
            for i in ids:self.assertTrue(eligible_for(index[i],d,'source_claim'));self.assertNotEqual(index[i].section_role,'abstract')
        methods=guidance['body_candidate_ids_by_dimension']['methodological_rigor']
        self.assertIn(self.context.blocks[1].evidence_id,methods)
        self.assertNotIn(self.context.blocks[2].evidence_id,methods)
        self.assertIn('metric, population, denominator',payload['messages'][0]['content'])

    def test_exact_and_formatting_equivalent_values_and_units_are_necessary(self):
        for claim,source in [('42% accuracy.','Accuracy: 42 %.'),('0.73 score','score 0.730'),
                             ('17 datasets','17 datasets'),('3.2× improvement','improvement 3.2 x'),('128K tokens','128k tokens')]:
            self.assertEqual(numerical_support(claim,[source])['status'],'requires_semantic_verification')
        for claim,source in [('43% accuracy','42% accuracy'),('42% accuracy','42 datasets'),
                             ('3.2× improvement','3.3× improvement'),('128K tokens','128 tokens')]:
            self.assertEqual(numerical_support(claim,[source])['status'],'unsupported')
        self.assertEqual(numeric_mentions('score 0.73.')[0]['value'],'0.73')

    def test_scimmr_real_claim_fails_despite_valid_canonical_sources(self):
        case=next(c for c in CASES if c['unsupported_numeric_items']);e=case['unsupported_numeric_items'][0]
        result=numerical_support(e['claim'],[b['text'] for b in e['sources']])
        self.assertEqual(result['status'],'unsupported');self.assertIn('20%',result['missing_values_or_units'])

    def test_absent_number_cannot_be_borrowed_from_other_cited_items_or_manuscript(self):
        # 74% exists in the full fixture and the evaluation item, not this item's Methods citation.
        self.value['evidence'][1]['claim']='The method achieves 74% retention.'
        result=self.validate();self.assertEqual(result.quality_status,'uncertain')
        self.assertEqual(result.execution['outcome'],'scientific')
        self.assertTrue(result.execution['support_errors'])
        self.assertFalse(any('74%' in e.paraphrase and e.dimension=='methodological_rigor' for e in result.evidence))
        self.assertNotEqual(result.quality_rationale,self.value['quality_rationale'])

    def test_same_number_with_wrong_metric_requires_and_fails_semantic_verification(self):
        self.value['evidence'][2]['claim']='Held-out precision is 74%.'
        self.assertNotEqual(numerical_support(self.value['evidence'][2]['claim'],[self.context.blocks[2].text])['status'],'unsupported')
        result=self.validate(overrides={'evidence-2':'unsupported'})
        self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'scientific')
        self.assertFalse(any('precision' in e.paraphrase for e in result.evidence))

    def test_supported_inference_need_not_be_a_literal_source_sentence(self):
        self.value['evidence'][5].update(statement_kind='assessor_inference',
            claim='The findings have limited demonstrated generality.',explanation='The stated design and unknown transfer leave broader scope unresolved.')
        result=self.validate();self.assertEqual(result.quality_status,'pass')
        self.assertNotIn(self.value['evidence'][5]['claim'],self.context.blocks[5].text)
        self.assertEqual(result.evidence[5].statement_kind,'assessor_inference')

    def test_unsupported_inference_is_removed_from_operational_assessment(self):
        self.value['evidence'][5].update(statement_kind='assessor_inference',claim='All language models will fail in production.')
        result=self.validate(overrides={'evidence-5':'unsupported'})
        self.assertEqual(result.quality_status,'uncertain')
        self.assertNotIn('All language models',result.concise_summary)
        self.assertFalse(any('All language models' in e.paraphrase for e in result.evidence))
        self.assertIn('All language models',result.execution['reference_audit'][5]['claim'])

    def test_unverified_id_or_assessor_support_label_cannot_grant_pass(self):
        result=self.validate(verified=False)
        self.assertEqual(result.quality_status,'uncertain')
        self.assertEqual(result.execution['outcome'],'support_verification_pending')
        self.assertEqual(result.evidence,[])

    def test_narrative_cannot_smuggle_unsupported_numerical_claim(self):
        self.value['quality_rationale']='The paper establishes 99% retention.'
        result=self.validate();self.assertEqual(result.quality_status,'uncertain')
        self.assertNotIn('99%',result.quality_rationale)
        self.assertNotIn('99%',result.concise_summary)
        self.assertIn('99%',result.execution['proposed_decision']['quality_rationale'])

    def test_support_result_must_bind_exact_claims_and_canonical_sources(self):
        record=verified_fixture(self.value,self.context)
        self.value['evidence'][0]['claim']='A different claim.'
        result=validate_block_quality_response(self.value,self.seed,'fixture',self.selected,self.context,verification=record)
        self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'protocol_failure')
        for key in ('items','input_sha256'):
            bad=verified_fixture(self.value,self.context);bad.pop(key)
            result=validate_block_quality_response(self.value,self.seed,'fixture',self.selected,self.context,verification=bad)
            self.assertEqual(result.quality_status,'uncertain')

    def test_new_decision_loading_rejects_missing_or_unsupported_verification(self):
        result=self.validate()
        for status in (None,'unsupported','uncertain'):
            stored=result.to_dict()
            stored['evidence'][0]['support_verification']={} if status is None else {'status':status}
            with self.assertRaisesRegex(ValueError,'supported claims'):QualityAssessment.from_dict(stored)
        stored=result.to_dict();stored['execution'].pop('support_verification')
        with self.assertRaisesRegex(ValueError,'claim-support verification'):QualityAssessment.from_dict(stored)

    def test_narrative_union_excludes_dimension_ineligible_blocks(self):
        self.selected=replace(self.selected,sections=[replace(self.selected.sections[0],heading='Abstract'),*self.selected.sections[1:]])
        self.context=build_evidence_context('fixture',self.selected)
        self.value['evidence_context_id']=self.context.context_id
        for e,b in zip(self.value['evidence'],self.context.blocks):e['evidence_ids']=[b.evidence_id]
        self.value['evidence'][0]['dimension']='methodological_rigor'
        items=verifier_items(self.value,self.context)
        self.assertTrue(items[0]['sources'])
        for narrative in items[-2:]:
            self.assertNotIn(self.context.blocks[0].evidence_id,[b['evidence_id'] for b in narrative['sources']])
        result=self.validate()
        self.assertEqual(result.execution['outcome'],'scientific')

    def test_numeric_comparisons_and_percentage_points_remain_checked(self):
        self.assertEqual([n['value'] for n in numeric_mentions('39%→73%')],['39','73'])
        self.assertEqual(numerical_support('exceeds 20 percentage points',['difference 19 points'])['status'],'unsupported')
        self.assertEqual(numerical_support('exceeds 20 percentage points',['20% relative gain'])['status'],'unsupported')
        self.assertEqual(numerical_support('42%→73%',['42%→72%'])['status'],'unsupported')
        self.assertEqual(numerical_support('improved by 20 percentage points',['gain: 20 percentage points'])['status'],'requires_semantic_verification')

    def test_uncertain_v2_hydrates_even_when_verification_is_missing(self):
        stored=self.validate().to_dict();stored['quality_status']='uncertain'
        stored['execution']['support_verification']={'status':'failed'}
        stored['evidence'][0]['support_verification']={}
        loaded=QualityAssessment.from_dict(stored)
        self.assertEqual(loaded.quality_status,'uncertain')
        self.assertEqual(loaded.to_dict(),stored)

    def test_limited_inference_from_introduction_is_only_a_candidate(self):
        self.value['evidence'][5].update(statement_kind='assessor_inference',
            claim='The evaluation proves nothing can generalize.', evidence_ids=[self.context.blocks[0].evidence_id])
        self.assertTrue(candidate_for_support(self.context.blocks[0],'limitations_and_uncertainty_handling','assessor_inference'))
        result=self.validate(overrides={'evidence-5':'unsupported'})
        self.assertEqual(result.execution['outcome'],'scientific')
        self.assertEqual(result.quality_status,'uncertain')
        self.assertFalse(any(e.dimension=='limitations_and_uncertainty_handling' for e in result.evidence))

    def test_numeric_identifiers_are_excluded_without_losing_signed_values_or_ranges(self):
        for text in ('GPT-5.5','K-2.7','Engram-27B','x-5.5','model123'):
            self.assertEqual(numeric_mentions(text),[])
        self.assertEqual([n['value'] for n in numeric_mentions('range 10-20; change -5.5; gain +3.2')],['1E+1','2E+1','-5.5','3.2'])

    def test_narrative_sources_are_a_deterministic_deduplicated_union(self):
        self.value['evidence'][5].update(statement_kind='assessor_inference',evidence_ids=self.value['evidence'][0]['evidence_ids'])
        items=verifier_items(self.value,self.context);ids=[s['evidence_id'] for item in items[:-2] for s in item['sources']]
        for item in items[-2:]:self.assertEqual([s['evidence_id'] for s in item['sources']],list(dict.fromkeys(ids)))

    def test_substantive_appendix_content_can_support_body_dimensions(self):
        # Location in an appendix does not erase actual methods/results content.
        self.selected=replace(self.selected,sections=[replace(s,heading='Appendix') for s in self.selected.sections])
        self.context=build_evidence_context('fixture',self.selected);self.value['evidence_context_id']=self.context.context_id
        for item,block in zip(self.value['evidence'],self.context.blocks):item['evidence_ids']=[block.evidence_id]
        self.assertEqual(self.validate().quality_status,'pass')
        # Eligible appendix IDs alone cannot establish adequacy for a generic or unsupported claim.
        rejected=self.validate(overrides={'evidence-1':'unsupported'})
        self.assertEqual(rejected.quality_status,'uncertain')
        self.assertEqual(rejected.execution['outcome'],'scientific')

    def test_rejected_item_cannot_leave_its_claim_in_published_narrative(self):
        for numeric in (False,True):
            value=copy.deepcopy(self.value)
            claim='The method establishes universal generalization.' if not numeric else 'The method achieves 99% retention.'
            value['evidence'][1]['claim']=claim;value['quality_rationale']=claim
            # Even a mistaken narrative verifier approval cannot rescue an item
            # rejected numerically or by its own verifier result.
            result=self.validate(value,overrides={} if numeric else {'evidence-1':'unsupported'})
            self.assertEqual(result.quality_status,'uncertain')
            self.assertNotIn(claim,result.quality_rationale)
            self.assertNotIn(claim,result.concise_summary)
            self.assertFalse(any(claim==e.paraphrase for e in result.evidence))
            self.assertEqual(result.execution['proposed_decision']['quality_rationale'],claim)

    def test_legacy_reviewed_assessment_remains_unchanged(self):
        old=assessment();stored=old.to_dict();self.assertEqual(QualityAssessment.from_dict(stored),old)
        self.assertEqual(old.quality_status,'pass');self.assertEqual(old.to_dict(),stored)
        self.assertEqual(EVIDENCE_VERSION,'block-evidence-v2')

    def test_verifier_gets_only_claims_and_their_cited_blocks(self):
        text='Uncited private-looking manuscript appendix sentinel.'
        selected=replace(self.selected,text=self.selected.text+'\n'+text,
            sections=[*self.selected.sections,SelectedSection('Appendix',text,20)])
        ctx=build_evidence_context('fixture',selected);v=copy.deepcopy(self.value);v['evidence_context_id']=ctx.context_id
        for item,b in zip(v['evidence'],ctx.blocks):item['evidence_ids']=[b.evidence_id]
        items=verifier_items(v,ctx);self.assertNotIn(text,json.dumps(items));self.assertNotIn('quality_status',json.dumps(items))
        for item in items[:-2]:self.assertEqual(len(item['sources']),1)


class VerifierExecutionTests(unittest.TestCase):
    def assess(self,responses):
        client=StrictHttp(responses);text,_=manuscript()
        with patch.dict('os.environ',ENV,clear=True),patch('paper_scout.quality_llm.time.sleep'):
            result=assess_with_optional_quality_llm(candidate(),text,assess_quality_deterministically(candidate(),'fixture',text),'llm',http=client)
        return result,client

    def test_bounded_isolated_verifier_calls_and_complete_accounting(self):
        result,client=self.assess([envelope(),verifier_response()])
        self.assertEqual(result.quality_status,'pass');self.assertEqual(len(client.payloads),8)
        self.assertEqual([c['kind'] for c in result.execution['calls']],['initial']+['verifier']*7)
        self.assertEqual(sum(c['usage']['cost_usd'] for c in result.execution['calls']),.045)
        self.assertEqual(sum(c['usage']['prompt_tokens'] for c in result.execution['calls']),683)
        self.assertEqual(result.execution['total_request_limit'],15)
        self.assertEqual(client.payloads[1]['response_format']['json_schema']['name'],'claim_support')
        self.assertEqual(client.payloads[1]['model'],client.payloads[0]['model'])

    def test_assessor_retry_and_bounded_source_groups(self):
        result,client=self.assess([envelope(finish='length'),envelope(),verifier_response()])
        self.assertEqual(result.quality_status,'pass');self.assertEqual(len(client.payloads),9)
        self.assertEqual([c['kind'] for c in result.execution['calls']],['initial','retry']+['verifier']*7)
        self.assertEqual(sum(c['usage']['cost_usd'] for c in result.execution['calls']),.055)

    def test_verifier_truncation_transport_and_bad_schema_fail_without_retry(self):
        malformed=json.loads(verifier_response());content=json.loads(malformed['choices'][0]['message']['content']);content['items'][1]['item_id']=content['items'][0]['item_id'];malformed['choices'][0]['message']['content']=json.dumps(content)
        for response in (verifier_response(finish='length'),HttpRequestError('timeout','https://example.test','fixture'),'not json',json.dumps({'error':{'code':503,'message':'fixture error'},'usage':{'prompt_tokens':80,'completion_tokens':0,'cost':.002}}),json.dumps(malformed)):
            result,client=self.assess([envelope(),response]);self.assertEqual(len(client.payloads),2)
            self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'protocol_failure')
            self.assertEqual(result.execution['calls'][-1]['status'],'failed')

    def test_verifier_input_limit_is_enforced_before_any_request(self):
        with patch('paper_scout.quality_llm.SUPPORT_MAX_INPUT_BYTES',1):
            result,client=self.assess([envelope()])
        self.assertEqual(len(client.payloads),1)
        self.assertEqual(result.quality_status,'uncertain')
        call=result.execution['calls'][-1]
        self.assertFalse(call['request_sent']);self.assertEqual(call['status'],'not_sent')
        self.assertEqual(call['usage']['cost_usd'],0)

    def test_verifier_byte_limit_includes_provider_and_reasoning_fields(self):
        result,client=self.assess([envelope(),verifier_response()])
        payload=client.payloads[1];self.assertIn('provider',payload);self.assertIn('reasoning',payload)
        actual=len(json.dumps(payload).encode())
        self.assertEqual(result.execution['calls'][1]['request_bytes'],actual)
        largest=max(len(json.dumps(p).encode()) for p in client.payloads[1:])
        with patch('paper_scout.quality_llm.SUPPORT_MAX_INPUT_BYTES',actual-1):
            rejected,client=self.assess([envelope()])
        self.assertEqual(len(client.payloads),1)
        self.assertFalse(rejected.execution['calls'][-1]['request_sent'])
        with patch('paper_scout.quality_llm.SUPPORT_MAX_INPUT_BYTES',largest):
            accepted,client=self.assess([envelope(),verifier_response()])
        self.assertEqual(len(client.payloads),8);self.assertEqual(accepted.quality_status,'pass')

    def test_nonobject_error_and_empty_envelopes_record_clear_protocol_failures(self):
        for response,problem in (([], 'non_object_envelope'),(None,'non_object_envelope'),('text','non_object_envelope'),
            ({},'invalid_choices'),({'choices':[]},'invalid_choices'),({'choices':[None]},'invalid_choices'),
            ({'error':{'code':503}},'provider_error_envelope'),
            ({'choices':[{'finish_reason':'stop','message':None}]},'invalid_message'),
            ({'choices':[{'finish_reason':'stop','message':{'content':[]}}]},'non_string_content')):
            result,client=self.assess([envelope(),json.dumps(response)])
            self.assertEqual(result.execution['outcome'],'protocol_failure')
            self.assertEqual(result.execution['calls'][-1]['response_problem'],problem)
            self.assertEqual(len(client.payloads),2)

    def test_invalid_reference_prevents_verifier_call(self):
        for key in ('invented','Eforeign-B0001'):
            value=block_fixture();value['evidence'][0]['evidence_ids']=[key]
            result,client=self.assess([envelope(value)]);self.assertEqual(len(client.payloads),1)
            self.assertEqual(result.execution['outcome'],'evidence_validation_failure')

    def test_verifier_unsupported_is_scientific_uncertainty_not_transport_failure(self):
        result,client=self.assess([envelope(),verifier_response(overrides={'evidence-2':'unsupported'})])
        self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'scientific')
        self.assertEqual(result.execution['calls'][-1]['status'],'success')
