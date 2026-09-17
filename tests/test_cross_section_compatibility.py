"""Conditional body compatibility reuses one bounded verifier, never certifies support."""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from paper_scout.evidence_context import EvidenceBlock, SourceSpan, build_evidence_context
from paper_scout.evidence_semantics import (CLAIM_ROLES, HARD_INELIGIBLE, DIRECTLY_COMPATIBLE,
    REQUIRES_SUPPORT_VERIFICATION, candidate_for_support, eligibility_decision, evidence_guidance)
from paper_scout.full_text import SelectedSection
from paper_scout.quality import assess_quality_deterministically
from paper_scout.quality_llm import assess_with_optional_quality_llm, validate_block_quality_response
from test_evidence_context import verified_fixture
from test_evidence_semantics import StrictHttp
from test_final_grounding_defects import block
from test_paper_scout_scientific_gate import candidate, manuscript
from test_quality_reliability import block_fixture, envelope, ENV

CASE = json.loads((Path(__file__).parent / 'fixtures/cross_section_real_science.json').read_text())


def proposal(heading='Introduction', text='A question motivates this work.', index=1):
    selected, _ = manuscript()
    sections = list(selected.sections)
    sections[index] = SelectedSection(heading, text, index + 2)
    selected = replace(selected, text='\n'.join(s.text for s in sections), sections=sections)
    ctx = build_evidence_context('fixture', selected)
    value = block_fixture()
    value['evidence_context_id'] = ctx.context_id
    for e in value['evidence']:
        i = next(i for i, old in enumerate(block_fixture()['evidence']) if old['dimension'] == e['dimension'])
        e['evidence_ids'] = [b.evidence_id for b in ctx.blocks if b.spans[0].section_index == i]
    value['evidence'][index].update(claim='The sources establish the specified criterion.',
                                    explanation='This is a scoped claim about the cited passage.')
    return selected, ctx, value


def validate(selected, ctx, value, status='supported', index=1):
    verification = verified_fixture(value, ctx, {f'evidence-{index}': status})
    seed = assess_quality_deterministically(candidate(), 'fixture', selected)
    return validate_block_quality_response(value, seed, 'fixture', selected, ctx, verification=verification)


def wire_verification(value, ctx, status='supported', index=1):
    v = verified_fixture(value, ctx, {f'evidence-{index}': status})
    return json.dumps({'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps({'items': v['items']})}}]})


class CrossSectionTests(unittest.TestCase):
    def test_actual_b0014_preserves_hash_spans_and_is_conditional_method_evidence(self):
        item = CASE['rejected_items'][0]
        source = next(b for b in item['blocks'] if b['id'].endswith('-B0014'))
        b = EvidenceBlock(source['id'], 14, source['text'], source['content_hash'],
            tuple(SourceSpan(**s) for s in source['spans']), True, source['role'])
        self.assertEqual(b.evidence_id, 'Edc6e037d47808254-B0014')
        self.assertEqual(hashlib.sha256(b.text.encode()).hexdigest(), b.content_hash)
        self.assertEqual(b.text, '\n'.join(s.text for s in b.spans))
        self.assertEqual(b.pages, [2, 3])
        self.assertTrue(item['provenance_valid'])
        self.assertFalse(item['eligibility_valid'])  # Saved pre-fix failure.
        self.assertIn('each run up to 4 times independently', b.text)
        d = eligibility_decision(b, item['dimension'], item['statement_kind'])
        self.assertTrue(d['body_member'])
        self.assertFalse(d['compatible'])
        self.assertEqual(d['state'], REQUIRES_SUPPORT_VERIFICATION)

    def actual_proposal(self):
        item = CASE['rejected_items'][0]
        # Preserve exact source text in a new inspectable test manuscript context;
        # original context/ID provenance is separately frozen above and in preflight.
        selected, ctx, value = proposal(text='\n'.join(b['text'] for b in item['blocks']))
        value['evidence'][1].update(claim=item['claim'], explanation=item['explanation'])
        return selected, ctx, value

    def test_actual_claim_accepts_supported_fallback(self):
        selected, ctx, value = self.actual_proposal()
        result = validate(selected, ctx, value)
        self.assertEqual(result.quality_status, 'pass')
        row = result.execution['reference_audit'][1]
        self.assertTrue(row['requires_support_fallback'])
        self.assertEqual(row['fallback_resolution'], 'accepted')
        self.assertTrue(row['accepted'])
        self.assertEqual(next(e for e in result.evidence if e.dimension == 'methodological_rigor').paraphrase,
                         CASE['rejected_items'][0]['claim'])

    def test_actual_claim_rejects_unsupported_and_uncertain_fallback(self):
        for status in ('unsupported', 'uncertain'):
            selected, ctx, value = self.actual_proposal()
            result = validate(selected, ctx, value, status)
            self.assertEqual(result.execution['outcome'], 'scientific')
            self.assertEqual(result.quality_status, 'uncertain')
            self.assertFalse(result.execution['reference_audit'][1]['accepted'])
            self.assertEqual(result.execution['reference_audit'][1]['fallback_resolution'], 'not_established')
            self.assertFalse(any(e.dimension == 'methodological_rigor' for e in result.evidence))

    def test_direct_roles_remain_direct(self):
        for heading, dimension in [('Methods', 'methodological_rigor'),
                                  ('Results', 'evidence_to_claim_alignment'),
                                  ('Limitations', 'limitations_and_uncertainty_handling')]:
            self.assertEqual(eligibility_decision(block(heading, 'Some body evidence.'), dimension,
                                                 'source_claim')['state'], DIRECTLY_COMPATIBLE)

    def test_cross_role_candidates_require_semantic_support(self):
        for heading, index, status in [('Introduction', 1, 'unsupported'), ('Appendix', 1, 'supported'),
                                     ('System Design', 1, 'supported'),
                                     ('Results', 5, 'supported'), ('Discussion', 2, 'supported'),
                                     ('Discussion', 3, 'unsupported')]:
            selected, ctx, value = proposal(heading, index=index)
            result = validate(selected, ctx, value, status, index)
            row = result.execution['reference_audit'][index]
            self.assertTrue(row['requires_support_fallback'])
            self.assertEqual(row['accepted'], status == 'supported')

    def test_hard_exclusions_cannot_be_rescued_even_by_supported_mock(self):
        for heading in ('Abstract', 'References', 'Acknowledgements', 'Front Matter', 'Copyright and License'):
            for kind in ('source_claim', 'assessor_inference'):
                b = block(heading, 'A protocol with independent trials and careful controls.')
                self.assertEqual(eligibility_decision(b, 'methodological_rigor', kind)['state'], HARD_INELIGIBLE)
                self.assertFalse(candidate_for_support(b, 'methodological_rigor', kind))
            selected, ctx, value = proposal(heading)
            result = validate(selected, ctx, value)
            self.assertEqual(result.execution['outcome'], 'evidence_validation_failure')
            self.assertFalse(result.execution['reference_audit'][1]['accepted'])
            self.assertFalse(any(e.dimension == 'methodological_rigor' for e in result.evidence))

    def test_soft_numeric_contradiction_cannot_be_rescued_by_supported_mock(self):
        selected, ctx, value = proposal(text='Accuracy is 95 percent.')
        value['evidence'][1]['claim'] = 'Accuracy is 96%.'
        result = validate(selected, ctx, value)
        row = result.execution['reference_audit'][1]
        self.assertTrue(row['requires_support_fallback'])
        self.assertEqual(row['support_verification']['status'], 'supported')
        self.assertEqual(row['numeric_check']['status'], 'unsupported')
        self.assertFalse(row['accepted'])

    def test_soft_wrong_metric_is_rejected_by_same_semantic_gate(self):
        selected, ctx, value = proposal(text='Recall is 95 percent.')
        value['evidence'][1]['claim'] = 'Accuracy is 95%.'
        result = validate(selected, ctx, value, 'unsupported')
        row = result.execution['reference_audit'][1]
        self.assertNotEqual(row['numeric_check']['status'], 'unsupported')
        self.assertFalse(row['accepted'])

    def test_guidance_distinguishes_direct_soft_and_excluded_without_leaking_ids(self):
        selected, ctx, value = proposal()
        guide = evidence_guidance(ctx)
        for dimension in CLAIM_ROLES:
            direct = set(guide['body_candidate_ids_by_dimension'][dimension])
            soft = set(guide['support_verification_candidate_ids_by_dimension'][dimension])
            self.assertFalse(direct & soft)
            for b in ctx.blocks:
                d = eligibility_decision(b, dimension, 'source_claim')
                self.assertEqual(b.evidence_id in soft, d['state'] == REQUIRES_SUPPORT_VERIFICATION)
                self.assertEqual(b.evidence_id in direct, d['body_member'] and d['state'] == DIRECTLY_COMPATIBLE)

    def test_direct_and_fallback_use_same_single_batched_call(self):
        for heading in ('Methods', 'Introduction'):
            selected, ctx, value = proposal(heading)
            client = StrictHttp([envelope(value), wire_verification(value, ctx)])
            with patch.dict('os.environ', ENV, clear=True):
                result = assess_with_optional_quality_llm(candidate(), selected,
                    assess_quality_deterministically(candidate(), 'fixture', selected), 'llm', http=client)
            self.assertEqual(result.quality_status, 'pass')
            self.assertEqual([c['kind'] for c in result.execution['calls']], ['initial', 'verifier'])
            self.assertEqual(len(client.payloads), 2)
            items = json.loads(client.payloads[1]['messages'][1]['content'])['items']
            self.assertEqual(len(items), 2 * len(value['evidence']) + 2)
            self.assertEqual(items[2]['sources'][0]['text'], ctx.blocks[1].text)
            self.assertNotIn('manuscript', items[1])

    def test_hard_exclusion_prevents_verifier_call(self):
        selected, ctx, value = proposal('Abstract')
        client = StrictHttp([envelope(value)])
        with patch.dict('os.environ', ENV, clear=True):
            result = assess_with_optional_quality_llm(candidate(), selected,
                assess_quality_deterministically(candidate(), 'fixture', selected), 'llm', http=client)
        self.assertEqual(result.execution['outcome'], 'evidence_validation_failure')
        self.assertEqual(len(client.payloads), 1)

    def test_failed_verifier_does_not_establish_fallback(self):
        selected, ctx, value = self.actual_proposal()
        client = StrictHttp([envelope(value), 'not json'])
        with patch.dict('os.environ', ENV, clear=True):
            result = assess_with_optional_quality_llm(candidate(), selected,
                assess_quality_deterministically(candidate(), 'fixture', selected), 'llm', http=client)
        self.assertEqual(result.execution['outcome'], 'protocol_failure')
        self.assertEqual(result.quality_status, 'uncertain')
        self.assertEqual(len(client.payloads), 2)
        self.assertFalse(result.execution['reference_audit'][1]['accepted'])
