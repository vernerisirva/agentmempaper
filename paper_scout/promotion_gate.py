"""Two scientific roles with one bounded adjudicator contract retry; fail closed."""
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
import json
import logging
import os
from urllib.parse import urlsplit
import uuid

from paper_scout.evidence_context import build_evidence_context, digest
from paper_scout.http import HttpClient, HttpRequestError
from paper_scout.promotion_protocol import (
    ASSESSMENT_VERSION, GATE_VERSION, INDEPENDENCE_CONTRACT, PRIMARY_MODEL,
    ADJUDICATOR_MODEL, RUBRIC, RECEIPT_VERSION, agreement, canonical_json, parse_response,
    response_binding, MAX_EVIDENCE_IDS, MODEL_PROVIDERS, PROVIDERS, RETRY_POLICY,
    ResponseContractError, attempt_binding, model_pair_provenance, schema, source_block,
    validate_context, validate_pair,
)
from paper_scout.quality_models import QualityEvidence
from paper_scout.manuscript_coverage import validate_assessment_coverage
from paper_scout.quality_llm import _reported_usage

LOGGER = logging.getLogger(__name__)

MAX_INPUT_BYTES = 300_000
MAX_OUTPUT_TOKENS = 4096
# Ceiling rates checked against public provider endpoints; no tools/cache writes.
# OpenRouter enforces these server side. Google's endpoint has no equivalent
# price-cap parameter, so Gemini spend is bounded by its own allocation instead.
PRICE_LIMITS = {'deepseek/deepseek-v4-pro-0813': (1.65, 4.95),
                'anthropic/claude-sonnet-4.6': (3.3, 16.5),
                'anthropic/claude-opus-4.6': (5.5, 27.5)}


@dataclass(frozen=True)
class RoleSettings:
    """One scientific role's provider, pinned model and credential."""

    provider: str
    model: str
    api_key: str
    base_url: str


def role_settings(model):
    """Resolve one role's provider endpoint and credential, or None if unconfigured.

    Each role reads its own provider credential, so the primary assessor and the
    independent adjudicator do not share an account or an endpoint.
    """
    provider = MODEL_PROVIDERS.get(model)
    if provider is None:
        raise ValueError('unknown scientific model provider')
    spec = PROVIDERS[provider]
    api_key = next((os.environ[name] for name in spec['credential_env']
                    if os.environ.get(name, '').strip()), None)
    if not api_key:
        return None
    base_url = next((os.environ[name] for name in spec['base_url_env']
                     if os.environ.get(name, '').strip()), spec['base_url']).rstrip('/')
    # An exact host match keeps one provider's credential off another's endpoint.
    if urlsplit(base_url).hostname != spec['host']:
        raise ValueError('pinned scientific model requires its own provider host')
    return RoleSettings(provider=provider, model=model, api_key=api_key, base_url=base_url)


def settings_from_env():
    mode = os.environ.get('PAPER_SCOUT_LLM_PROVIDER', 'auto').lower()
    if mode in {'', 'none', 'off', 'rules'}:
        return None
    primary = os.environ.get('PAPER_SCOUT_QUALITY_LLM_MODEL') or PRIMARY_MODEL
    adjudicator = os.environ.get('PAPER_SCOUT_QUALITY_ADJUDICATOR_MODEL') or ADJUDICATOR_MODEL
    validate_pair(primary, adjudicator)
    pair = (role_settings(primary), role_settings(adjudicator))
    # Both scientific roles must be configured; one credential is not a usable gate.
    return pair if all(pair) else None


def request_payload(role, settings, context, coverage, primary=None, *, retry=False):
    if retry and role != 'adjudicator':
        raise ValueError('only adjudication has a contract retry')
    instruction = RUBRIC
    # Both roles answer evaluation_independence from the manuscript themselves. The
    # structural consequences below are output-format requirements over the values each
    # role declares; they change no scientific standard and set no pass-rate target.
    instruction += """
Answer evaluation_independence from the manuscript: what signal shaped the system under
study, what signal established the headline outcome, whether they are materially
independent, what evaluator-independent measurement is reported, and whether it supports
the headline claim. Keep each prose field to one or two sentences. Report a corroboration
direction only when independent corroboration is present, and always report one when it
is. Declare concern major when the evaluator is materially reused with no independent
corroboration, or when independent evidence contradicts the headline claim under reused
or unresolved signals; a major concern cannot accompany your pass. Where reuse is
unresolved and no corroboration is reported, concern is not none.
"""
    if role == 'primary':
        instruction += '\nIndependently assess the manuscript. decision is pass or uncertain.'
    else:
        instruction += """\nIndependently adjudicate the proposed promotion from the manuscript.
Do not assume the primary final assessment is correct or treat it as evidence. Check
its cited blocks and look for counterevidence throughout the supplied context. Reach your
own evaluation_independence judgment from the manuscript; never inherit, copy or defer to
the primary's. Decide whether contribution, method, evaluation, limitations, citation
support and claim scope justify admission. Any important unsupported overclaim means uncertain. Report concise
blocking reasons and your own evidence IDs. No hidden reasoning is supplied or requested.
The decision and blocking_reasons must agree structurally. When promotion_decision is
pass, return blocking_reasons: [] and write nothing in it; never state in prose that
there are no blocking reasons. When one or more blocking reasons exist, list each of
them and promotion_decision cannot be pass. This is an output-format requirement and
changes no scientific standard: it does not make promotion easier or harder.
"""
        instruction += f"""Return at most {MAX_EVIDENCE_IDS} distinct evidence IDs.
Cite the smallest sufficient set of supplied blocks supporting the promotion decision,
blocking reasons and major quality dimensions. Prefer strongest, directly relevant,
non-duplicative evidence; do not enumerate every remotely relevant block. Preserve
support for all material judgments; this budget does not relax the scientific rubric.
"""
        if retry:
            instruction += f"""This is the one permitted fresh adjudication after an output
contract failure. Independently adjudicate the original manuscript and primary final
assessment again. Return at most {MAX_EVIDENCE_IDS} distinct evidence IDs and obey the
response schema, including the structural rule that a pass has an empty blocking_reasons
array and that any blocking reason means the decision is not pass, and the
evaluation_independence rules stated above.
Select only evidence necessary to justify your final decision.
No previous adjudication is supplied; do not infer or preserve its conclusion.
"""
    content = {'canonical_id': context.canonical_id, 'source_content_hash': context.source_hash,
               'context_id': context.context_id, 'coverage': coverage, 'manuscript': context.text}
    if primary is not None:
        content['primary_final_assessment'] = primary
    payload = {'model': settings.model, 'temperature': 0, 'max_tokens': MAX_OUTPUT_TOKENS,
               'messages': [{'role': 'system', 'content': instruction},
                            {'role': 'user', 'content': json.dumps(content, ensure_ascii=False)}],
               'response_format': {'type': 'json_schema', 'json_schema': {
                   'name': 'promotion_' + role + '_v2', 'strict': True, 'schema': schema(role)}}}
    # Both providers express the same contract: no hidden reasoning is requested,
    # returned or persisted. They spell it with different parameter names, and
    # each rejects the other's, so the switch is by provider, not by model string.
    if settings.provider == 'openrouter':
        input_price, output_price = PRICE_LIMITS[settings.model]
        payload['reasoning'] = {'enabled': False, 'exclude': True}
        payload['provider'] = {'require_parameters': True,
                               'max_price': {'prompt': input_price, 'completion': output_price}}
    elif settings.provider == 'google':
        payload['reasoning_effort'] = 'none'
    else:
        raise ValueError('unknown scientific provider')
    if len(json.dumps(payload).encode('utf-8')) > MAX_INPUT_BYTES:
        raise ValueError('promotion request exceeds byte budget; no call sent')
    return payload


def _billing(provider, usage):
    """Record what the provider actually reported; never invent a monetary cost.

    OpenRouter reports a per-call charge. Google's endpoint reports tokens only,
    so the charge is attributed to the allocation rather than guessed.
    """
    if usage.get('cost_usd') is not None:
        return {'source': provider, 'basis': 'provider_reported', 'cost_usd': usage['cost_usd']}
    return {'source': provider, 'cost_usd': None,
            'basis': 'covered_by_msc_allocation' if provider == 'google' else 'unknown',
            'billing_cost': 'UNKNOWN'}


def call_model(role, settings, context, payload, client, calls, run_id):
    call = {'kind': role, 'model': settings.model, 'provider': settings.provider,
            'context_id': context.context_id,
            'attempt': 1 + sum(c['kind'] == role for c in calls),
            'status': 'failed', 'usage': _reported_usage({}),
            'request_sha256': digest(json.dumps(payload, ensure_ascii=False, sort_keys=True))}
    call['billing'] = _billing(settings.provider, call['usage'])
    calls.append(call)
    raw = client.post_json(settings.base_url + '/chat/completions', payload,
                           headers={'Authorization': 'Bearer ' + settings.api_key})
    response = json.loads(raw)
    if not isinstance(response, dict):
        raise ValueError('invalid response envelope')
    call['usage'] = _reported_usage(response)
    call['billing'] = _billing(settings.provider, call['usage'])
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
    # Preserve the exact final response, never provider hidden-reasoning fields.
    call['raw_content'] = content
    try:
        value = parse_response(content, role, context)
    except ResponseContractError as exc:
        call.update(status='contract_failure', contract_error=exc.reason)
        call['attempt_binding_sha256'] = attempt_binding(call, run_id)
        raise
    call['canonical_response_sha256'] = digest(canonical_json(value))
    call['response_binding_sha256'] = response_binding(call, run_id)
    call['status'] = 'success'
    call['attempt_binding_sha256'] = attempt_binding(call, run_id)
    return value


def assess_promotion(candidate, selected, seed, mode, http=None):
    receipt = {'outcome': 'not_assessed', 'calls': [], 'run_id': uuid.uuid4().hex,
               'receipt_version': RECEIPT_VERSION,
               'retry_policy': RETRY_POLICY,
               'total_request_limit': 3, 'attempt_limit_per_role': {'primary': 1, 'adjudicator': 2}}
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
        receipt.update(primary_model=primary_settings.model, adjudicator_model=adjudicator_settings.model,
                       primary_provider=primary_settings.provider,
                       adjudicator_provider=adjudicator_settings.provider,
                       model_pair=model_pair_provenance(primary_settings.model, adjudicator_settings.model),
                       independence_contract=INDEPENDENCE_CONTRACT,
                       generation={'temperature': 0, 'max_output_tokens': MAX_OUTPUT_TOKENS,
                                   'hidden_reasoning': 'disabled', 'max_request_bytes': MAX_INPUT_BYTES})
        if selected.scope not in {'full_text', 'partial_full_text'}:
            return pending('manuscript_unavailable', 'Manuscript unavailable; no scientific decision.')
        identity = selected.coverage.get('manuscript_identity', {})
        if (identity.get('verified') is not True or identity.get('source_content_hash') != selected.content_hash
                or identity.get('source_url') != seed.full_text_url or not seed.full_text_url):
            return pending('integrity_failure', 'Manuscript identity or acquisition provenance is unverified.')
        coverage_failures = validate_assessment_coverage(selected)
        base['coverage'] = selected.coverage
        if coverage_failures:
            receipt['coverage_gate'] = {'version': 'coverage-v2', 'status': 'failed',
                                        'reasons': coverage_failures}
            result = pending('text_coverage_failure',
                             'Scientific manuscript coverage is incomplete; no scientific decision or model call.')
            return replace(result, quality_status='not_assessed')
        receipt['coverage_gate'] = {'version': 'coverage-v2', 'status': 'pass', 'reasons': []}
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
        primary = call_model('primary', primary_settings, context, primary_payload, client,
                             receipt['calls'], receipt['run_id'])
        receipt['primary'] = primary
        # Both judgments are retained even when primary is uncertain; never up to 13 verifiers.
        for attempt in range(2):
            # Fresh original inputs only. Never slice IDs or feed the rejected output back.
            adjudicator_payload = request_payload('adjudicator', adjudicator_settings, context,
                                                  selected.coverage, primary, retry=bool(attempt))
            try:
                adjudicator = call_model('adjudicator', adjudicator_settings, context, adjudicator_payload,
                                         client, receipt['calls'], receipt['run_id'])
                break
            except ResponseContractError:
                if attempt == 1:
                    raise
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
        LOGGER.warning('Promotion protocol failure: %s', json.dumps({
            'canonical_id': seed.canonical_id, 'error_type': type(exc).__name__,
            'call_count': len(receipt['calls'])}))
        return pending('protocol_failure', 'Scientific response or integrity validation failed; technical review pending.')
