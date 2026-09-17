"""Two bounded scientific calls. Integrity failures fail closed; disagreement is normal."""
from dataclasses import asdict, replace
from datetime import UTC, datetime
import json
import os
from urllib.parse import urlsplit
import uuid

from paper_scout.evidence_context import build_evidence_context, digest
from paper_scout.http import HttpClient, HttpRequestError
from paper_scout.llm import openai_compatible_settings_from_env
from paper_scout.promotion_protocol import (
    ASSESSMENT_VERSION, GATE_VERSION, PRIMARY_MODEL, ADJUDICATOR_MODEL, RUBRIC,
    agreement, schema, source_block, validate_context, validate_pair, validate_response,
)
from paper_scout.quality_models import QualityEvidence
from paper_scout.quality_llm import _reported_usage

MAX_INPUT_BYTES = 300_000
MAX_OUTPUT_TOKENS = 4096
# Ceiling rates checked against public provider endpoints; no tools/cache writes.
PRICE_LIMITS = {PRIMARY_MODEL: (1.65, 4.95), ADJUDICATOR_MODEL: (3.3, 16.5),
                'anthropic/claude-opus-4.6': (5.5, 27.5)}


def settings_from_env():
    settings = openai_compatible_settings_from_env('PAPER_SCOUT_QUALITY_LLM_MODEL')
    if settings is None:
        return None
    primary = os.environ.get('PAPER_SCOUT_QUALITY_LLM_MODEL') or PRIMARY_MODEL
    adjudicator = os.environ.get('PAPER_SCOUT_QUALITY_ADJUDICATOR_MODEL') or ADJUDICATOR_MODEL
    validate_pair(primary, adjudicator)
    # This protocol's model identities and provider price caps are OpenRouter-specific.
    if urlsplit(settings.base_url).hostname != 'openrouter.ai':
        raise ValueError('pinned promotion model pair requires OpenRouter')
    return (replace(settings, model=primary), replace(settings, model=adjudicator))


def request_payload(role, settings, context, coverage, primary=None):
    instruction = RUBRIC
    if role == 'primary':
        instruction += '\nIndependently assess the manuscript. decision is pass or uncertain.'
    else:
        instruction += """\nIndependently adjudicate the proposed promotion from the manuscript.
Do not assume the primary final assessment is correct or treat it as evidence. Check
its cited blocks and look for counterevidence throughout the supplied context. Decide
whether contribution, method, evaluation, limitations, citation support and claim scope
justify admission. Any important unsupported overclaim means uncertain. Report concise
blocking reasons and your own evidence IDs. No hidden reasoning is supplied or requested.
"""
    content = {'canonical_id': context.canonical_id, 'source_content_hash': context.source_hash,
               'context_id': context.context_id, 'coverage': coverage, 'manuscript': context.text}
    if primary is not None:
        content['primary_final_assessment'] = primary
    input_price, output_price = PRICE_LIMITS[settings.model]
    payload = {'model': settings.model, 'temperature': 0, 'max_tokens': MAX_OUTPUT_TOKENS,
               'reasoning': {'enabled': False, 'exclude': True},
               'provider': {'require_parameters': True,
                            'max_price': {'prompt': input_price, 'completion': output_price}},
               'messages': [{'role': 'system', 'content': instruction},
                            {'role': 'user', 'content': json.dumps(content, ensure_ascii=False)}],
               'response_format': {'type': 'json_schema', 'json_schema': {
                   'name': 'promotion_' + role + '_v1', 'strict': True, 'schema': schema(role)}}}
    if len(json.dumps(payload).encode('utf-8')) > MAX_INPUT_BYTES:
        raise ValueError('promotion request exceeds byte budget; no call sent')
    return payload


def call_model(role, settings, context, payload, client, calls):
    call = {'kind': role, 'model': settings.model, 'context_id': context.context_id,
            'status': 'failed', 'usage': _reported_usage({}),
            'request_sha256': digest(json.dumps(payload, ensure_ascii=False, sort_keys=True))}
    calls.append(call)
    raw = client.post_json(settings.base_url + '/chat/completions', payload,
                           headers={'Authorization': 'Bearer ' + settings.api_key})
    response = json.loads(raw)
    if not isinstance(response, dict):
        raise ValueError('invalid response envelope')
    call['usage'] = _reported_usage(response)
    if response.get('error') or response.get('model') != settings.model:
        raise ValueError('provider error or wrong returned model')
    choices = response.get('choices')
    if not isinstance(choices, list) or len(choices) != 1:
        raise ValueError('expected exactly one completion')
    choice = choices[0]
    call['finish_reason'] = choice.get('finish_reason')
    if call['finish_reason'] != 'stop':
        raise ValueError('missing, truncated or abnormal completion')
    message = choice['message']
    if message.get('refusal') or message.get('tool_calls'):
        raise ValueError('refusal or unexpected tool call')
    content = message['content']
    if not isinstance(content, str):
        raise ValueError('non-text completion')
    call['content_sha256'] = digest(content)
    value = validate_response(json.loads(content), role, context)
    call['status'] = 'success'
    return value


def assess_promotion(candidate, selected, seed, mode, http=None):
    receipt = {'outcome': 'not_assessed', 'calls': [], 'run_id': uuid.uuid4().hex,
               'total_request_limit': 2, 'attempt_limit_per_role': 1}
    base = dict(assessment_version=ASSESSMENT_VERSION, quality_gate_version=GATE_VERSION,
                quality_status='uncertain', overall_quality_score=None, recommendation='unknown',
                applied_score_cap=None, applied_score_cap_reason=None, dimension_scores={},
                evidence=[], positive_signals=[], concerns=[],
                assessed_at=datetime.now(UTC).isoformat(), execution=receipt)
    def pending(outcome, reason):
        receipt['outcome'] = outcome
        base.update(quality_status='uncertain', evidence=[], positive_signals=[])
        return replace(seed, **base, quality_rationale=reason, concise_summary=reason,
                       quality_uncertainty='No promotion; review candidates may remain pending indefinitely.')
    if mode in {'off', 'deterministic'}:
        return pending('not_assessed', 'Independent scientific assessments have not been performed.')
    try:
        settings = settings_from_env()
        if settings is None:
            return pending('not_assessed', 'Independent scientific model configuration is unavailable.')
        primary_settings, adjudicator_settings = settings
        receipt.update(primary_model=primary_settings.model, adjudicator_model=adjudicator_settings.model)
        if selected.scope not in {'full_text', 'partial_full_text'}:
            return pending('manuscript_unavailable', 'Manuscript unavailable; no scientific decision.')
        identity = selected.coverage.get('manuscript_identity', {})
        if (identity.get('verified') is not True or identity.get('source_content_hash') != selected.content_hash
                or identity.get('source_url') != seed.full_text_url or not seed.full_text_url):
            return pending('integrity_failure', 'Manuscript identity or acquisition provenance is unverified.')
        context = build_evidence_context(seed.canonical_id, selected)
        validate_context(context, selected)
        if context.source_hash != seed.source_content_hash:
            return pending('integrity_failure', 'Assessment and manuscript hashes differ.')
        receipt.update(context=json.loads(json.dumps(asdict(context))), manuscript_identity=identity)
        base['coverage'] = {**selected.coverage, **context.metadata()}
        base['assessor_type'] = 'llm' if mode == 'llm' else 'hybrid'
        base['assessor_model'] = primary_settings.model
        client = http or HttpClient(timeout_seconds=180, retries=1)
        if type(getattr(client, 'retries', None)) is int and client.retries != 1:
            raise ValueError('promotion client cannot retry calls')
        primary_payload = request_payload('primary', primary_settings, context, selected.coverage)
        primary = call_model('primary', primary_settings, context, primary_payload, client, receipt['calls'])
        receipt['primary'] = primary
        # Both judgments are retained even when primary is uncertain; never up to 13 verifiers.
        adjudicator_payload = request_payload('adjudicator', adjudicator_settings, context,
                                              selected.coverage, primary)
        adjudicator = call_model('adjudicator', adjudicator_settings, context, adjudicator_payload,
                                 client, receipt['calls'])
        receipt['adjudicator'] = adjudicator
        validate_context(context, selected)
        passed = agreement(primary, adjudicator)
        receipt.update(outcome='success', provenance_status='pass')
        ids = set(primary['evidence_ids']) | set(adjudicator['evidence_ids'])
        blocks = [b for b in context.blocks if b.evidence_id in ids]
        base['evidence'] = [QualityEvidence(
            dimension='contribution_clarity', signal_type='positive' if passed else 'concern',
            paraphrase='Canonical source cited in the scientific promotion review.',
            explanation='Source integrity verified; scientific judgments are recorded separately.',
            section=b.spans[0].section, page=b.pages[0] if b.pages else None,
            excerpt=b.text, evidence_ids=[b.evidence_id], context_id=context.context_id,
            pages=b.pages, source_blocks=[source_block(b)]) for b in blocks]
        base['quality_status'] = 'pass' if passed else 'uncertain'
        base['concerns'] = adjudicator['blocking_reasons']
        return replace(seed, **base, confidence='high' if passed else 'low',
                       concise_summary=primary['quality_rationale'],
                       quality_rationale=primary['quality_rationale'],
                       quality_uncertainty=primary['limitations'])
    except HttpRequestError:
        return pending('transport_failure', 'A scientific model call failed; technical review pending.')
    except Exception as exc:
        # No output repair, scientific negative verdict or exposure of provider response/key.
        receipt['error_type'] = type(exc).__name__
        return pending('protocol_failure', 'Scientific response or integrity validation failed; technical review pending.')
