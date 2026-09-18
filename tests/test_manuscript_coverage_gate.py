"""Offline structure/coverage tests. No models or scientific outcome fixtures."""
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from paper_scout.full_text import ExtractedPage, FullTextDocument, select_assessment_text
from paper_scout.manuscript_coverage import validate_assessment_coverage
from paper_scout.promotion_gate import assess_promotion
from paper_scout.promotion_protocol import identity_from_document
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_models import QualityAssessment
from paper_scout.state import PaperStore
from test_promotion_gate import fixture, ENV, Models


class ScientificCoverageTests(unittest.TestCase):
    def select(self, pages, budget=180000, **kwargs):
        c, original, _, _ = fixture()
        doc = replace(original, pages=[ExtractedPage(i, text) for i, text in pages], **kwargs)
        return select_assessment_text(c, doc, max_prompt_characters=budget)

    def assert_complete(self, selected):
        self.assertEqual(selected.scope, 'full_text')
        self.assertEqual(validate_assessment_coverage(selected), [])
        self.assertEqual(selected.coverage['omitted_body_characters'], 0)

    def test_actual_star_methods_structure_all_five_pages_retained(self):
        spec = json.loads((Path(__file__).parent/'fixtures/star_methods_structure.json').read_text())
        pages=[]
        for i, count in enumerate(spec['source_page_characters'], 1):
            heading='\n'.join(spec['headings_by_page'].get(str(i), []))
            content=('1. Smith, J. (2020). Citation.\n' if 12 <= i <= 16 else 'Synthetic scientific prose. ')
            text=heading+'\n'+(content*(count//len(content)+1))[:count-len(heading)-1]
            pages.append((i,text))
        selected=self.select(pages, coverage={'source_pages':21})
        self.assert_complete(selected)
        self.assertTrue(set(spec['previously_omitted_pages']) <= set(selected.coverage['selected_pages']))
        methods=[s for s in selected.sections if s.heading=='Star Methods']
        self.assertEqual([s.first_page for s in methods],list(range(17,22)))
        self.assertTrue(all(s.text in selected.text for s in methods))
        limited=self.select(pages,budget=14000,coverage={'source_pages':21})
        self.assertEqual(limited.coverage['status'],'text_coverage_failure')
        self.assertGreater(limited.coverage['omitted_body_characters'],0)
        self.assertTrue(validate_assessment_coverage(limited))

    def test_novel_heading_after_references_is_body_without_vocabulary(self):
        for heading in ['LATENT ORCHESTRATION','Kinetic Routing','Δυναμική Διαδρομή',
                        'Materials and Methods','Experimental Procedures','Method Details',
                        'Study Design','Implementation Details','Experimental Setup',
                        'Technical Appendix','Protocol','Resource Availability',
                        'Quantification and Statistical Analysis']:
            with self.subTest(heading=heading):
                selected=self.select([(1,'Introduction\nProblem.\nReferences\nA citation.'),
                                      (2,heading+'\nDetailed scientific content.'),(3,'Continued scientific content.')])
                self.assert_complete(selected)
                self.assertIn('Detailed scientific content.',selected.text)
                self.assertIn('Continued scientific content.',selected.text)

    def test_unrecognized_prose_after_reference_page_is_retained(self):
        s=self.select([(1,'Introduction\nProblem.\nReferences\n[1] Smith, J. (2020).'),
                       (2,'an unfamiliar lowercase boundary\nDetailed substantive prose without citation markers.')])
        self.assert_complete(s)
        self.assertIn('Detailed substantive prose',s.text)
        self.assertIn(2,s.coverage['scientific_body_pages'])

    def test_long_methods_are_contiguous_not_heading_capped(self):
        pages=[(1,'Introduction\nProblem framing.')]+[(i,('Methods\n' if i==2 else '')+'Method protocol. '*800) for i in range(2,7)]+[(7,'Results\nMeasured result.\nLimitations\nScoped transfer.')]
        s=self.select(pages)
        self.assert_complete(s)
        self.assertGreater(sum(len(x.text) for x in s.sections if x.heading=='Methods'),40000)
        self.assertEqual(s.coverage['selected_pages'],list(range(1,8)))
        limited=self.select(pages,budget=18000)
        self.assertTrue(validate_assessment_coverage(limited))
        method_pages=[x.first_page for x in limited.sections if x.heading=='Methods']
        self.assertEqual(sorted(set(method_pages)),list(range(2,max(method_pages)+1)))
        self.assertIn('Measured result.',limited.text)
        self.assertIn('Scoped transfer.',limited.text)
        self.assertTrue(all(row['omission_reason']=='context_budget' for row in limited.coverage['sections'] if row['omitted_characters']))

    def test_large_references_do_not_displace_methods_or_appendix(self):
        pages=[(1,'Introduction\nProblem.\nMethods\nControlled setup.\nResults\nObserved outcomes.\nLimitations\nScope.'),
               (2,'References\n'+('[1] Smith, J. (2020). Citation.\n'*5000)),
               (3,'A Technical Appendix\nImportant derivation.'),(4,'Continuation of derivation.')]
        s=self.select(pages,budget=4000)
        self.assert_complete(s)
        self.assertNotIn('Citation.',s.text)
        self.assertIn('Important derivation.',s.text)
        self.assertIn('Continuation of derivation.',s.text)

    def test_heading_at_page_end_carries_to_next_page(self):
        s=self.select([(1,'Introduction\nProblem.\nNEURAL ROUTING'),(2,'Protocol and measured results.'),(3,'Limitations\nScoped.')])
        self.assert_complete(s)
        self.assertEqual(next(x for x in s.sections if x.first_page==2).heading,'Neural Routing')

    def test_missing_empty_duplicate_and_truncated_pages_fail(self):
        for pages,kwargs in [([(1,'Methods\nEvidence.'),(3,'Results\nEvidence.')],{}),
                            ([(1,'Methods\nEvidence.'),(2,'')],{}),
                            ([(1,'Methods\nEvidence.')],{'coverage':{'source_pages':2}}),
                            ([(1,'Methods\nEvidence.'),(1,'Results\nEvidence.')],{}),
                            ([(1,'Methods\nEvidence.')],{'complete':False})]:
            with self.subTest(pages=pages):
                s=self.select(pages,**kwargs)
                self.assertTrue(validate_assessment_coverage(s))
                self.assertEqual(s.scope,'partial_full_text')

    def test_front_matter_and_contents_are_technical_failure(self):
        s=self.select([(1,'Title of a book\nAn author'),(2,'Preface\nThis volume introduces ideas.'),
                       (3,'Table of Contents\n1 Introduction ........ 1\n2 Methods ........ 8\n3 Results ........ 20')])
        self.assertTrue(validate_assessment_coverage(s))
        self.assertIn('scientific_body_not_established',s.coverage['failure_reasons'])

    def test_coverage_failure_sends_zero_calls_and_persists_pending(self):
        c,doc,_,seed=fixture()
        for broken in [replace(doc,complete=False),
                       replace(doc,pages=[ExtractedPage(1,c.title+'\nPreface\nFront matter only.')]),
                       replace(doc,pages=[ExtractedPage(1,c.title+'\nMethods\n'+'Protocol. '*20000)])]:
            s=select_assessment_text(c,broken,max_prompt_characters=4000)
            s=replace(s,coverage={**s.coverage,'manuscript_identity':identity_from_document(c,broken)})
            models=Models()
            with patch.dict('os.environ',ENV,clear=True):
                result=assess_promotion(c,s,seed,'llm',http=models)
            self.assertEqual(models.payloads,[])
            self.assertEqual(result.execution['calls'],[])
            self.assertEqual(result.execution['outcome'],'text_coverage_failure')
            self.assertEqual(result.quality_status,'not_assessed')
            self.assertFalse(result.full_text_assessed)
            self.assertNotIn('primary',result.execution)
            self.assertEqual(result.coverage,s.coverage)
            with tempfile.TemporaryDirectory() as d:
                store=PaperStore(Path(d)/'state.sqlite3');store.save_quality_assessment(result)
                self.assertEqual(store.get_current_quality_assessment(result.canonical_id),result)

    def test_utf8_roundtrip_and_input_hash_integrity(self):
        s=self.select([(1,'Introduction\nα β μ ± × ≤ ≥ → é Å.'),(2,'ΚΑΙΝΗ ΜΕΘΟΔΟΣ\nΔυναμική — λ = 1.\nLimitations\nScoped.')])
        self.assert_complete(s)
        self.assertIn('Δυναμική',s.text)
        self.assertEqual(s.text.encode('utf-8').decode('utf-8'),s.text)
        with self.assertRaises(ValueError):validate_assessment_coverage(replace(s,text=s.text+'unrecorded edit'))
        self.assertTrue(validate_assessment_coverage(replace(s,coverage={})))
