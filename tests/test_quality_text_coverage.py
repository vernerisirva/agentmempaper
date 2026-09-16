from dataclasses import replace
import hashlib
import json
import unittest
from unittest.mock import patch

from paper_scout.full_text import (ExtractedPage, FullTextDocument, SelectedSection, select_assessment_text,
    _extract_pdf, _detect_sections, _bounded_pages)
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_llm import _request_payload, locate_evidence, validate_llm_quality_response
from paper_scout.quality_models import QualityEvidence, QualityAssessment
from test_paper_scout_scientific_gate import candidate, manuscript
import test_quality_reliability as fixtures
from test_quality_reliability import SequenceHttp, envelope


class CoverageTests(unittest.TestCase):
    def test_full_scientific_body_is_not_limited_per_heading_and_references_are_excluded(self):
        pages=[ExtractedPage(1, 'Abstract\nSummary.\n1 Introduction\nClaim.'),
               ExtractedPage(2, '2 Methods\n'+'method evidence. '*1000),
               ExtractedPage(3, '3 Results\nMeasured effect.\n4 Limitations\nScope is bounded.'),
               ExtractedPage(4, 'References\n1 Smith, J. A Citation\n'+'Citation. '*3000),
               ExtractedPage(5, 'A Implementation Details\nAppendix training protocol.')]
        selected=select_assessment_text(candidate(),FullTextDocument('https://example.org/a.pdf',pages,'sha',True),max_section_characters=200)
        self.assertEqual(selected.scope,'full_text')
        self.assertIn('Appendix training protocol.',selected.text)
        self.assertNotIn('Smith',selected.text)
        self.assertEqual(selected.coverage['omitted_body_characters'],0)
        self.assertTrue(selected.coverage['excluded_back_matter_characters']>20000)
        self.assertEqual(selected.coverage['assessment_input_sha256'],hashlib.sha256(selected.text.encode()).hexdigest())

    def test_numbered_supplement_resumes_after_references_without_promoting_citations(self):
        sections=_detect_sections([ExtractedPage(1,'References\nS. M. Katz. Estimation of probabilities from sparse data\n1 Smith, J. Citation'),
            ExtractedPage(2,'7 Supplementary Details\n7.1 Implementation Details\nTraining seeds and loss.\n7.2 Additional Results\nA measured result.')])
        self.assertTrue(any(s.heading=='Implementation Details' and 'Training seeds' in s.text for s in sections))
        self.assertFalse(any(s.heading.startswith('Appendix: M. Katz') for s in sections))

    def test_glued_uppercase_appendix_heading_does_not_disappear_in_references(self):
        selected=select_assessment_text(candidate(),FullTextDocument('https://example.org/a.pdf',[
            ExtractedPage(1,'Introduction\nA claim.\nReferences\nA citation.'),
            ExtractedPage(2,'A DETAILEDDERIVATION OF THECOUNTERFACTUALSURROGATE\nProof.\nB.4 SUMMARY\nAn explicit limitation.')], 'sha',True))
        self.assertIn('An explicit limitation.',selected.text)
        self.assertTrue(any(s.heading.startswith('Appendix:') for s in selected.sections))

    def test_oversized_selection_represents_scientific_groups_and_records_gaps(self):
        headings=['Introduction','Methods','Results','Limitations','Discussion','Conclusion']
        pages=[ExtractedPage(i+1,heading+'\n'+('Evidence '+heading+'. ')*2000) for i,heading in enumerate(headings)]
        pages.append(ExtractedPage(7,'References\n'+'Citation. '*6000))
        selected=select_assessment_text(candidate(),FullTextDocument('https://example.org/a.pdf',pages,'sha',True),max_prompt_characters=12000,max_section_characters=1600)
        self.assertLessEqual(len(selected.text),12000)
        self.assertEqual(selected.scope,'partial_full_text')
        self.assertTrue(selected.coverage['selected_instead_of_full_text'])
        self.assertGreater(selected.coverage['omitted_body_characters'],0)
        self.assertEqual({s.heading for s in selected.sections},set(headings))
        self.assertTrue(all(s.text in selected.text for s in selected.sections))
        self.assertTrue(any('omitted' in w for w in selected.warnings))

    def test_rank_bounded_first_numbered_body_after_abstract_is_not_abstract(self):
        pages=[ExtractedPage(1,'Abstract\nAn abstract.'),ExtractedPage(2,'2 / 31\n1. The problem: memory outlives the defense\nReal body evidence.'),ExtractedPage(3,'2. Threat model: what by design covers\nThreat details.')]
        selected=select_assessment_text(candidate(),FullTextDocument('https://example.org/a.pdf',pages,'sha',True))
        evidence=QualityEvidence('contribution_clarity','positive','Body','Body',page=2,excerpt='Real body evidence.')
        self.assertIsNotNone(locate_evidence(evidence,selected))
        self.assertIn('Threat details.',selected.text)

    def test_canonical_prompt_and_validator_share_text_and_preserve_hyphens(self):
        text='The long-\nterm system supports ofﬁce memory. It does not improve recall.'
        selected=select_assessment_text(candidate(),FullTextDocument('https://example.org/a.pdf',[ExtractedPage(2,'Methods\n'+text)],'sha',True))
        supplied=json.loads(_request_payload(candidate(),selected,assess_quality_deterministically(candidate(),'id',selected),'model')['messages'][1]['content'])
        self.assertEqual(supplied['paper']['text'],selected.text)
        self.assertNotIn('deterministic_assessment',supplied)
        self.assertIn('office',selected.text)
        evidence=QualityEvidence('methodological_rigor','positive','Test','Test',page=2,excerpt='long-term system supports office memory')
        self.assertIsNotNone(locate_evidence(evidence,selected))
        self.assertIsNone(locate_evidence(replace(evidence,excerpt='system improves recall'),selected))
        self.assertIsNone(locate_evidence(replace(evidence,excerpt='unseen appendix evidence'),selected))

    def test_source_evidence_omitted_from_actual_prompt_remains_rejected(self):
        selected=select_assessment_text(candidate(),FullTextDocument('https://example.org/a.pdf',[ExtractedPage(2,'Methods\n'+'visible material '*100+'HIDDEN TERMINAL QUOTE')],'sha',True),max_prompt_characters=200)
        e=QualityEvidence('methodological_rigor','positive','Test','Test',page=2,excerpt='HIDDEN TERMINAL QUOTE')
        if e.excerpt not in selected.text:self.assertIsNone(locate_evidence(e,selected))
        # Explicit mismatch must fail even if a caller supplies a source-only section.
        self.assertIsNone(locate_evidence(e,replace(selected,sections=[SelectedSection('Methods',e.excerpt,2)])))

    def test_pdf_page_limits_and_empty_pages_cannot_claim_complete(self):
        class Page:
            def __init__(self,text):self.text=text
            def extract_text(self):return self.text
        with patch('pypdf.PdfReader',return_value=type('Reader',(),{'pages':[Page('start'),Page(''),Page('middle'),Page('later'),Page('end')]})()):
            full=_extract_pdf(b'fixture','https://example.org/a.pdf',10,1000)
            self.assertFalse(full.complete);self.assertEqual(full.coverage['unreadable_pages'],[2])
            bounded=_extract_pdf(b'fixture','https://example.org/a.pdf',3,1000)
            self.assertEqual([p.page for p in bounded.pages],[1,3,5]);self.assertEqual(bounded.coverage['source_pages'],5)
        retained=_bounded_pages([ExtractedPage(1,'A'*900),ExtractedPage(2,'B'*900)],600)
        self.assertLessEqual(sum(len(p.text) for p in retained),600)
        self.assertTrue(all('Extraction gap' in p.text for p in retained))

    def test_incomplete_extraction_cannot_become_scientific_insufficient(self):
        selected,value=manuscript();selected=replace(selected,coverage={'extraction_truncated':True,'omitted_body_characters':20})
        value={**value,'quality_status':'insufficient','evidence':[{**e,'signal_type':'concern'} for e in value['evidence']]}
        result=validate_llm_quality_response(value,assess_quality_deterministically(candidate(),'id',selected),'model',selected=selected)
        self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'text_coverage_failure');self.assertFalse(result.full_text_assessed)
        complete=replace(selected,coverage={'extraction_truncated':False,'omitted_body_characters':0})
        result=validate_llm_quality_response(value,assess_quality_deterministically(candidate(),'id',complete),'model',selected=complete)
        self.assertEqual(result.quality_status,'insufficient')
        self.assertEqual(QualityAssessment.from_dict(result.to_dict()),result)


class SubstantiveResponseTests(unittest.TestCase):
    def test_seed_echo_retries_once_with_same_manuscript_and_no_hidden_reasoning(self):
        selected,value=manuscript();seed=assess_quality_deterministically(candidate(),'fixture',selected)
        bad={**value,'quality_status':'uncertain','quality_rationale':seed.quality_rationale}
        client=SequenceHttp([envelope(bad),envelope(value)])
        result,_=fixtures.ReliabilityTest().assess(client)
        self.assertEqual(result.quality_status,'pass');self.assertEqual(len(result.execution['calls']),2)
        self.assertEqual(result.execution['calls'][0]['response_problem'],'deterministic_seed_echo')
        self.assertEqual(client.payloads[0]['messages'][1],client.payloads[1]['messages'][1])
        self.assertIn('Hidden reasoning is neither needed',client.payloads[1]['messages'][-1]['content'])

    def test_second_empty_response_and_transport_share_two_request_ceiling(self):
        from paper_scout.http import HttpRequestError
        _,value=manuscript();empty={**value,'quality_status':'uncertain','evidence':[]}
        for responses in ([envelope(empty),envelope(empty)], [HttpRequestError('timeout','https://example.org','fixture'),envelope(empty)]):
            result,_=fixtures.ReliabilityTest().assess(SequenceHttp(responses))
            self.assertEqual(result.quality_status,'uncertain');self.assertEqual(result.execution['outcome'],'protocol_failure')
            self.assertEqual(len(result.execution['calls']),2);self.assertFalse(result.full_text_assessed)
