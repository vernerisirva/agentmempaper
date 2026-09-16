from dataclasses import replace
import copy
import json
import unittest

from paper_scout.evidence_context import build_evidence_context, resolve_evidence_ids, digest
from paper_scout.full_text import SelectedPaperText, SelectedSection
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_llm import validate_block_quality_response, validate_block_review
from paper_scout.quality_models import QualityAssessment
from paper_scout.site import _quality_evidence_detail, _evidence_page_suffix
from test_paper_scout_scientific_gate import candidate, manuscript, assessment
from test_quality_reliability import block_fixture, envelope, SequenceHttp
import test_quality_reliability as fixtures


class EvidenceContextTests(unittest.TestCase):
    def setUp(self):
        self.selected, _ = manuscript()
        self.seed = assess_quality_deterministically(candidate(), 'fixture', self.selected)
        self.context = build_evidence_context('fixture', self.selected)
        self.value = block_fixture()

    def validate(self, value=None, context=None, selected=None):
        return validate_block_quality_response(value or self.value, self.seed, 'model',
                                              selected or self.selected, context or self.context)

    def test_valid_ids_derive_exact_quotes_and_keep_interpretation_separate(self):
        self.value['evidence'][0]['claim'] = 'A paraphrased claim — punctuation need not copy the source.'
        result = self.validate()
        self.assertEqual(result.quality_status, 'pass')
        self.assertEqual(result.evidence[0].excerpt, self.context.blocks[0].text)
        self.assertNotEqual(result.evidence[0].excerpt, result.evidence[0].paraphrase)
        self.assertEqual(result.evidence[0].source_blocks[0]['content_hash'], digest(result.evidence[0].excerpt))
        self.assertEqual(QualityAssessment.from_dict(result.to_dict()), result)
        self.assertEqual(build_evidence_context('fixture', self.selected), self.context)
        rendered = _quality_evidence_detail(result.evidence[0].to_dict())
        self.assertIn('Canonical source evidence', rendered)
        self.assertNotIn(self.context.blocks[0].evidence_id, rendered)

    def test_invented_foreign_stale_and_unseen_references_fail_closed(self):
        foreign = build_evidence_context('other-manuscript', self.selected)
        changed = build_evidence_context('fixture', replace(self.selected, content_hash='different-source-version'))
        for evidence_id in ('P012-C999', foreign.blocks[0].evidence_id, changed.blocks[0].evidence_id):
            value = copy.deepcopy(self.value)
            value['evidence'][0]['evidence_ids'] = [evidence_id]
            result = self.validate(value)
            self.assertEqual(result.quality_status, 'uncertain')
            self.assertEqual(result.execution['outcome'], 'evidence_validation_failure')
        stale = replace(self.context, version='obsolete-addressing-version')
        self.assertEqual(self.validate(context=stale).execution['outcome'], 'evidence_validation_failure')
        value = copy.deepcopy(self.value);value['evidence_context_id'] = changed.context_id
        self.assertEqual(self.validate(value).quality_status, 'uncertain')
        # A real block in a larger source is not in the actual assessor selection.
        shorter = replace(self.selected, text='\n'.join(s.text for s in self.selected.sections[1:]), sections=self.selected.sections[1:])
        short_context = build_evidence_context('fixture', shorter)
        value['evidence_context_id'] = short_context.context_id
        self.assertEqual(self.validate(value, short_context, shorter).quality_status, 'uncertain')

    def test_hash_tampering_abstract_and_source_only_sections_are_rejected(self):
        tampered = replace(self.context, blocks=(replace(self.context.blocks[0], text='invented data'), *self.context.blocks[1:]))
        self.assertEqual(self.validate(context=tampered).quality_status, 'uncertain')
        with self.assertRaises(ValueError):resolve_evidence_ids([tampered.blocks[0].evidence_id], tampered)
        abstract = replace(self.selected, sections=[replace(s,heading='Abstract') for s in self.selected.sections])
        ctx = build_evidence_context('fixture', abstract)
        with self.assertRaises(ValueError):resolve_evidence_ids([ctx.blocks[0].evidence_id],ctx)
        with self.assertRaises(ValueError):build_evidence_context('fixture',replace(self.selected,text='not the source text'))

    def test_real_block_does_not_establish_an_unsupported_interpretation(self):
        self.value['evidence'][0].update(claim='This proves general intelligence.', support_status='unsupported',
            explanation='The cited experiment is scoped to retention tasks and does not support this generalization.')
        result = self.validate()
        self.assertEqual(result.quality_status, 'uncertain')
        self.assertEqual(result.execution['outcome'], 'scientific')
        self.assertTrue(all(a['provenance_valid'] for a in result.execution['reference_audit']))
        self.assertNotIn('contribution_clarity',result.execution['validated_dimensions'])

    def test_page_spanning_evidence_preserves_exact_spans_without_joining_unrelated_sections(self):
        # Real failure shapes: Grounding Agent Memory related work and ProtLingo
        # sampling limitation continue after page labels; the model now cites IDs.
        parts=['These advances change memory content, representation, retrieval, or rewriting, but post-\ntask curation still operates mainly over existing records,',
               'recorded trajectories, grades, and usage signals.']
        sections=[SelectedSection('Related Work',parts[0],2),SelectedSection('Related Work',parts[1],3)]
        selected=SelectedPaperText('\n\n'.join(parts),sections,'full_text','source',False,coverage={'extraction_complete':True})
        ctx=build_evidence_context('paper',selected);block=next(b for b in ctx.blocks if b.pages==[2,3])
        self.assertEqual([s.text for s in block.spans],parts)
        self.assertEqual(resolve_evidence_ids([block.evidence_id],ctx)[0],block)
        self.assertEqual(_evidence_page_suffix({'pages':[2,3]},' — page '),' — pages 2–3')
        hyphen=replace(selected,text='long-\nterm memory',sections=[SelectedSection('Methods','long-',4),SelectedSection('Methods','term memory',5)])
        joined=build_evidence_context('paper',hyphen).blocks[0]
        self.assertEqual(joined.text,'long-term memory');self.assertEqual(joined.pages,[4,5])
        distinct=replace(hyphen,sections=[hyphen.sections[0],replace(hyphen.sections[1],heading='Limitations')])
        self.assertEqual(len(build_evidence_context('paper',distinct).blocks),2)
        partial=replace(hyphen,scope='partial_full_text',coverage={'selected_instead_of_full_text':True})
        self.assertEqual(len(build_evidence_context('paper',partial).blocks),2)

    def test_context_change_never_rewrites_legacy_pass_and_infrastructure_cannot_be_insufficient(self):
        old=assessment();stored=old.to_dict();self.assertEqual(QualityAssessment.from_dict(stored).quality_status,'pass')
        self.value['quality_status']='insufficient';self.value['evidence'][0]['signal_type']='concern'
        self.assertEqual(self.validate().quality_status,'insufficient')
        partial=replace(self.selected,coverage={'extraction_truncated':True});ctx=build_evidence_context('fixture',partial)
        self.assertEqual(ctx.context_id,self.context.context_id)  # identical supplied bytes, no page joins here
        self.assertEqual(self.validate(selected=partial,context=ctx).execution['outcome'],'text_coverage_failure')
        self.value['evidence'][0]['evidence_ids']=['invented']
        self.assertEqual(self.validate().quality_status,'uncertain')
        self.assertEqual(old.to_dict(),stored)


class OutputRecoveryTests(unittest.TestCase):
    def test_length_partial_json_is_discarded_and_compact_retry_succeeds_with_both_costs(self):
        first=json.loads(envelope(finish='length'));first['choices'][0]['message']['content']='{"quality_status":"insufficient",'
        client=SequenceHttp([json.dumps(first),envelope()]);result,_=fixtures.ReliabilityTest().assess(client)
        self.assertEqual(result.quality_status,'pass');self.assertEqual(len(client.payloads),2)
        self.assertEqual(result.execution['calls'][0]['error_kind'],'output_limit')
        self.assertEqual(sum(c['usage']['cost_usd'] for c in result.execution['calls']),.02)
        self.assertEqual(client.payloads[0]['messages'][1],client.payloads[1]['messages'][1])
        self.assertIn('compact COMPLETE',client.payloads[1]['messages'][-1]['content'])
        self.assertNotIn(first['choices'][0]['message']['content'],json.dumps(client.payloads[1]))
        first['choices'][0].pop('message')
        recovered,_=fixtures.ReliabilityTest().assess(SequenceHttp([json.dumps(first),envelope()]))
        self.assertEqual(recovered.quality_status,'pass')
        self.assertEqual(recovered.execution['calls'][0]['error_kind'],'output_limit')

    def test_all_recovery_paths_share_two_calls_and_second_failure_remains_technical(self):
        from paper_scout.http import HttpRequestError
        for responses in ([envelope(finish='length'),envelope(finish='max_tokens')],
                          [HttpRequestError('timeout','https://example.org','timeout'),envelope(finish='length')],
                          [envelope(finish='max_output_tokens'),'not JSON']):
            client=SequenceHttp(responses);result,_=fixtures.ReliabilityTest().assess(client)
            self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'protocol_failure')
            self.assertEqual(len(client.payloads),2);self.assertFalse(result.full_text_assessed)

    def test_schema_rejects_quoted_legacy_shape_extra_fields_and_oversized_output(self):
        value=block_fixture()
        for bad in ({**value,'evidence':[{'excerpt':'invented'}]}, {**value,'quality_rationale':'x'*1601},
                    {**value,'evidence':value['evidence']*3},manuscript()[1]):
            with self.assertRaises(ValueError):validate_block_review(bad)
