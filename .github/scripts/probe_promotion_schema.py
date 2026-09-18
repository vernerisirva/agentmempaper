#!/usr/bin/env python3
"""Ask each provider whether it accepts the current promotion response schema.

The strict structured-output subset differs between providers and is not discoverable
statically, so a schema a provider rejects would surface as a protocol failure on the
first real assessment rather than at configuration time. This probe asks the question
directly, with a trivial fixed prompt: no manuscript, no scientific content and no
stored row, so it evaluates nothing and writes nothing.

It makes live calls and therefore costs allocation or money, so it is an explicit
operator step, never part of a run. Use it after any change to the response schema,
and before relying on a new gate version in production.

    python3 .github/scripts/probe_promotion_schema.py            # report the payloads
    python3 .github/scripts/probe_promotion_schema.py --live     # send them

Exits non-zero if a provider rejects the schema or omits a required field.
"""
import argparse
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from paper_scout.promotion_gate import request_payload, settings_from_env  # noqa: E402
from paper_scout.promotion_protocol import (  # noqa: E402
    GATE_VERSION, INDEPENDENCE_CONTRACT, INDEPENDENCE_FIELD, schema,
)

PROMPT = ('Return the required fields for a fictional one-line note. '
          'canonical_id=probe, source_content_hash=probe, context_id=probe, evidence_ids=[].')


def payload(role, settings):
    """The production request shape, with the manuscript replaced by a fixed prompt.

    Generation parameters and the strict schema come from request_payload, so the probe
    cannot drift from what a real call sends. Only the content is substituted.
    """
    body = request_payload(role, settings, _Context(), {}, {'decision': 'pass'}
                           if role == 'adjudicator' else None)
    body['messages'] = [{'role': 'system', 'content': 'Return only structured output.'},
                        {'role': 'user', 'content': PROMPT}]
    return body


class _Context:
    """The smallest context request_payload needs; no manuscript is involved."""

    canonical_id = source_hash = context_id = 'probe'
    text = PROMPT


def send(settings, body):
    request = urllib.request.Request(
        settings.base_url + '/chat/completions', json.dumps(body).encode(),
        {'Authorization': 'Bearer ' + settings.api_key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read())


def probe(role, settings, live):
    body = payload(role, settings)
    declared = body['response_format']['json_schema']
    print(f'{settings.provider:11s} {role:12s} model={settings.model} '
          f'schema={declared["name"]} strict={declared["strict"]}')
    if not live:
        return None
    try:
        response = send(settings, body)
    except urllib.error.HTTPError as exc:
        return f'{settings.provider}/{role}: HTTP {exc.code} {exc.read()[:300]!r}'
    except Exception as exc:  # noqa: BLE001 - a probe reports, it does not raise.
        return f'{settings.provider}/{role}: {type(exc).__name__}: {exc}'
    if response.get('model') != settings.model:
        return f'{settings.provider}/{role}: returned model {response.get("model")!r}'
    choice = (response.get('choices') or [{}])[0]
    if choice.get('finish_reason') != 'stop':
        return f'{settings.provider}/{role}: finish_reason {choice.get("finish_reason")!r}'
    try:
        value = json.loads(choice['message']['content'])
    except Exception as exc:  # noqa: BLE001
        return f'{settings.provider}/{role}: unparsable content ({type(exc).__name__}: {exc})'
    required = set(schema(role)['required'])
    missing = required - set(value)
    dimension = value.get(INDEPENDENCE_FIELD)
    if missing:
        return f'{settings.provider}/{role}: missing {sorted(missing)}'
    if not isinstance(dimension, dict):
        return f'{settings.provider}/{role}: {INDEPENDENCE_FIELD} is not an object'
    absent = set(schema(role)['properties'][INDEPENDENCE_FIELD]['required']) - set(dimension)
    if absent:
        return f'{settings.provider}/{role}: {INDEPENDENCE_FIELD} missing {sorted(absent)}'
    usage = response.get('usage') or {}
    print(f'{"":11s} {"":12s} accepted; all fields returned; usage={usage.get("total_tokens")} tokens')
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true',
                        help='actually send the probes (costs allocation or money)')
    args = parser.parse_args(argv)
    print(f'gate {GATE_VERSION}, contract {INDEPENDENCE_CONTRACT}')
    settings = settings_from_env()
    if settings is None:
        print('no scientific model pair is configured; nothing to probe')
        # Asking for a live probe and getting none is a failure to answer the question,
        # not an answer. Only a dry run is allowed to report nothing and succeed.
        return 1 if args.live else 0
    failures = [f for f in (probe(role, role_settings, args.live) for role, role_settings
                            in zip(('primary', 'adjudicator'), settings)) if f]
    if not args.live:
        print('\nnot sent; pass --live to send these payloads')
        return 0
    for failure in failures:
        print(f'  {failure}')
    print(f'\npromotion schema probe: {len(failures)} errors')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
