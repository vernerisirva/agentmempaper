"""Actual saved failures plus adversarial provenance/compatibility regressions.

Fixtures were rebuilt from unchanged cached manuscript bytes and checked against
all three saved context IDs before implementation. No network calls in tests.
"""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import unittest

from paper_scout.evidence_context import (EvidenceBlock, SourceSpan, build_evidence_context,
                                          resolve_evidence_ids)
from paper_scout.evidence_semantics import (CLAIM_ROLES, eligibility_decision, eligible_for, candidate_for_support,
                                           numerical_support, numeric_mentions)
from paper_scout.full_text import SelectedPaperText, SelectedSection
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_llm import validate_block_quality_response
from test_evidence_context import verified_fixture
from test_paper_scout_scientific_gate import candidate, manuscript
from test_quality_reliability import block_fixture

CASES = [json.loads((Path(__file__).parent / 'fixtures' / name).read_text())
         for name in ('final_grounding_conditional-memory.json',
                      'final_grounding_real-science.json', 'final_grounding_scimmr.json')]


def block(heading, text):
    selected = SelectedPaperText(text, [SelectedSection(heading, text, 1)],
                                 'full_text', 'fixture-hash', False)
    return build_evidence_context('fixture', selected).blocks[0]


def actual_block(source):
    text = source['text']
    return EvidenceBlock(source['id'], 1, text, source['content_hash'],
                         (SourceSpan(text, source['pages'][0], source['section'], 0, 0, len(text)),),
                         True, source['role'])


class FinalGroundingTests(unittest.TestCase):
    def test_all_three_saved_failures_reproduce_specific_body_role_conflicts(self):
        self.assertEqual(len(CASES), 3)
        self.assertEqual(sum(len(c['rejected_items']) for c in CASES), 4)
        for case in CASES:
            for item in case['rejected_items']:
                for source in item['blocks']:
                    with self.subTest(paper=case['canonical_id'], source=source['id']):
                        self.assertEqual(hashlib.sha256(source['text'].encode()).hexdigest(), source['content_hash'])
                        b = actual_block(source)
                        decision = eligibility_decision(b, item['dimension'], item['statement_kind'])
                        self.assertTrue(decision['body_member'])
                        self.assertTrue(candidate_for_support(b, item['dimension'], item['statement_kind']))
                        if source['id'] in item['original_rejected_ids']:
                            self.assertEqual(decision['basis'], 'atypical_body_requires_support')

    def test_scimmr_separate_missing_percentage_still_fails(self):
        case = next(c for c in CASES if c['numeric_rejections'])
        item = case['numeric_rejections'][0]
        result = numerical_support(item['claim'] + '\n' + item['explanation'],
                                   [b['text'] for b in item['blocks']])
        self.assertEqual(result['status'], 'unsupported')
        self.assertIn('57.2%', result['missing_values_or_units'])

    def test_novel_body_heading_is_provenance_eligible(self):
        b = block('The Violet Compass', 'We sample independent trials using a randomized protocol.')
        self.assertEqual(b.section_role, 'body')
        d = eligibility_decision(b, 'methodological_rigor', 'source_claim')
        self.assertTrue(d['body_member'])
        self.assertFalse(d['compatible'])
        self.assertEqual(d['basis'], 'atypical_body_requires_support')

    def test_other_body_does_not_validate_every_claim_role(self):
        b = block('The Violet Compass', 'The contribution concerns a previously unstudied question.')
        self.assertTrue(eligible_for(b, 'contribution_clarity', 'source_claim'))
        for dimension in ('methodological_rigor', 'evaluation_or_validation_strength',
                          'evidence_to_claim_alignment', 'reproducibility_and_transparency',
                          'limitations_and_uncertainty_handling'):
            self.assertFalse(eligible_for(b, dimension, 'source_claim'))

    def test_ordinary_unfamiliar_headings_do_not_erase_body_membership(self):
        for heading in ('Analysis', 'Findings', 'Case Study', 'Observations',
                        'System Design', 'Study', 'Empirical Study', 'A Novel Unlisted Heading'):
            d = eligibility_decision(block(heading, 'The protocol samples trials.'),
                                     'methodological_rigor', 'source_claim')
            self.assertTrue(d['body_member'], heading)
            self.assertNotEqual(d['state'], 'hard_ineligible', heading)

    def test_non_body_provenance_cannot_be_rescued_by_content_cues(self):
        for heading in ('References', '7 References', 'Bibliography', 'Acknowledgements',
                        'Metadata', 'Front Matter', 'Title Page', 'Author Affiliations',
                        'Copyright and License', 'Copyright and Licensing Information',
                        'Licensing Information', 'Funding', 'Author Contributions'):
            b = block(heading, 'Our method uses a protocol and reaches 95% accuracy despite limitations.')
            self.assertFalse(b.eligible, heading)
            for dimension in CLAIM_ROLES:
                self.assertFalse(eligible_for(b, dimension, 'source_claim'), (heading, dimension))

    def test_abstract_is_only_attributed_contribution(self):
        b = block('Abstract', 'A new protocol obtains 95% accuracy but has limited scope.')
        for dimension in CLAIM_ROLES:
            self.assertEqual(eligible_for(b, dimension, 'source_claim'), dimension == 'contribution_clarity')
            self.assertFalse(eligible_for(b, dimension, 'assessor_inference'))

    def test_discussion_supports_limitations_and_combined_results_support_results(self):
        self.assertTrue(eligible_for(block('Discussion', 'Transfer remains uncertain.'),
                                     'limitations_and_uncertainty_handling', 'source_claim'))
        self.assertTrue(eligible_for(block('Results and Discussion', 'Accuracy is 95%.'),
                                     'evidence_to_claim_alignment', 'source_claim'))
        self.assertTrue(eligible_for(block('Discussion and Limitations', 'Scope is limited.'),
                                     'limitations_and_uncertainty_handling', 'source_claim'))

    def test_unrelated_conclusion_is_not_direct_method_evidence(self):
        b = block('Conclusion', 'We hope future work will inspire the community.')
        d = eligibility_decision(b, 'methodological_rigor', 'source_claim')
        self.assertTrue(d['body_member'])
        self.assertFalse(d['compatible'])

    def test_legitimate_body_candidate_still_requires_substantive_support(self):
        selected, _ = manuscript()
        sections = [replace(s, heading='An Unlisted Heading') if i == 1 else s
                    for i, s in enumerate(selected.sections)]
        selected = replace(selected, sections=sections)
        ctx = build_evidence_context('fixture', selected)
        value = block_fixture()
        value['evidence_context_id'] = ctx.context_id
        for item, b in zip(value['evidence'], ctx.blocks):
            item['evidence_ids'] = [b.evidence_id]
        value['evidence'][1]['claim'] = 'The protocol proves universal generalization.'
        self.assertTrue(candidate_for_support(ctx.blocks[1], 'methodological_rigor', 'source_claim'))
        self.assertFalse(eligible_for(ctx.blocks[1], 'methodological_rigor', 'source_claim'))
        seed = assess_quality_deterministically(candidate(), 'fixture', selected)
        result = validate_block_quality_response(value, seed, 'fixture', selected, ctx,
            verification=verified_fixture(value, ctx, {'evidence-1': 'unsupported'}))
        self.assertEqual(result.quality_status, 'uncertain')
        self.assertEqual(result.execution['outcome'], 'scientific')
        self.assertFalse(any(e.paraphrase == value['evidence'][1]['claim'] for e in result.evidence))
        self.assertEqual(result.execution['reference_audit'][1]['eligibility'][0]['basis'], 'atypical_body_requires_support')

    def test_percent_orthography_is_symmetric_and_keeps_original_text(self):
        forms = ('95%', '95 %', '95 percent', '95 per cent', '95 PERCENT')
        for claim in forms:
            for source in forms:
                with self.subTest(claim=claim, source=source):
                    self.assertEqual(numerical_support(claim, [source])['status'], 'requires_semantic_verification')
                    mention = numeric_mentions(claim)[0]
                    self.assertEqual(mention['literal'], claim)
                    self.assertEqual(claim[mention['start']:mention['end']], claim)
                    self.assertEqual(mention['unit'], '%')

    def test_different_numeric_concepts_do_not_collapse(self):
        forms = ('95%', '95 percentage points', '95 basis points', '0.95', '95')
        for i, claim in enumerate(forms):
            for j, source in enumerate(forms):
                self.assertEqual(numerical_support(claim, [source])['status'],
                                 'requires_semantic_verification' if i == j else 'unsupported',
                                 (claim, source))

    def test_percentage_point_and_relative_improvements_are_distinct(self):
        for claim, source in [('5% improvement', '5 percentage-point improvement'),
                              ('5 percentage-point improvement', '5 percent improvement')]:
            self.assertEqual(numerical_support(claim, [source])['status'], 'unsupported')
        self.assertEqual(numerical_support('5 percentage-point improvement',
                         ['5 percentage points improvement'])['status'], 'requires_semantic_verification')

    def test_decimal_percentage_orthography_does_not_change_value(self):
        self.assertEqual(numerical_support('9.5 percent', ['9.50%'])['status'], 'requires_semantic_verification')
        self.assertEqual(numerical_support('9.5 percent', ['95%'])['status'], 'unsupported')
        self.assertEqual(numerical_support('95 percentile', ['95%'])['status'], 'unsupported')

    def test_word_numbers_are_not_silently_interpreted(self):
        self.assertEqual(numeric_mentions('ninety-five percent'), [])
        self.assertEqual(numerical_support('95%', ['ninety-five percent'])['status'], 'unsupported')

    def test_percent_variant_with_wrong_metric_still_requires_verifier(self):
        selected, _ = manuscript()
        ctx = build_evidence_context('fixture', selected)
        value = block_fixture()
        value['evidence'][2]['claim'] = 'Held-out precision is 74 percent.'
        self.assertEqual(numerical_support(value['evidence'][2]['claim'],
                                          [ctx.blocks[2].text])['status'], 'requires_semantic_verification')
        seed = assess_quality_deterministically(candidate(), 'fixture', selected)
        result = validate_block_quality_response(value, seed, 'fixture', selected, ctx,
            verification=verified_fixture(value, ctx, {'evidence-2': 'unsupported'}))
        self.assertEqual(result.quality_status, 'uncertain')
        self.assertFalse(any('precision' in e.paraphrase for e in result.evidence))


if __name__ == '__main__':
    unittest.main()
