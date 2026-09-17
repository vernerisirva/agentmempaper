"""Typed facts derived from canonical blocks; never substitutes for entailment.

Raw text and offsets are immutable. Comparison normalization belongs to atoms,
not manuscript text. Numeric context is retained, not guessed from keywords.
"""
from __future__ import annotations

from dataclasses import asdict
from decimal import Decimal
import re
from urllib.parse import urlsplit

from paper_scout.evidence_context import EvidenceBlock, EvidenceContext, digest

ATOM_VERSION = 'typed-evidence-v1'


def url_mentions(text: str) -> list[dict]:
    out = []
    for match in re.finditer(r'https?://[^\s<>"\[\]]+', text):
        raw = match.group()
        end = match.end()
        # Join only a structural continuation (hostname fragment plus path, or
        # path with an internal slash). A prose label such as Models: is not one.
        tail = re.match(r'[ \t]*\n[ \t]*([A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*/[^\s<>"\[\]]+)', text[end:])
        if raw.endswith(('/', '.')) and tail:
            raw += tail.group(1)
            end += tail.end()
        url = raw.rstrip('.,;')
        # Preserve balanced parentheses inside paths; remove only unmatched
        # closing prose delimiters. Query operators, fragment and percent escapes
        # remain untouched. Never percent-decode or alter case/path identity.
        while url.endswith(')') and url.count(')') > url.count('('):
            url = url[:-1]
        try:
            parsed = urlsplit(url)
            _ = parsed.port
            if not parsed.hostname or any((parsed.username, parsed.password)):
                continue
            if parsed.hostname.endswith('.'):
                continue
        except ValueError:
            continue
        # Offsets include line-wrap normalization but exclude prose punctuation.
        trimmed = len(raw) - len(url)
        out.append({'literal': text[match.start():end-trimmed], 'normalized': url,
                    'start': match.start(), 'end': end-trimmed})
    return out


_VALUE = r'[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'
_UNIT = r'percentage[\s-]+points?\b|basis[\s-]+points?\b|per\s+cent\b|percent\b|%|×|[xX](?!\w)|[kKmMbB](?!\w)'
# Explicit units can border glued OCR words. Bare quantities still require
# lexical boundaries, so model names do not become scientific measurements.
_EXPLICIT = re.compile(r'(?<![\d.])(?P<value>'+_VALUE+r')(?P<unit>\s*(?:'+_UNIT+r'))', re.I)
_BARE = re.compile(r'(?<![\w.])(?P<value>'+_VALUE+r')(?!\w|\.\d)')
_RANGE = re.compile(r'(?<![\d.])('+_VALUE+r')\s*[–—-]\s*('+_VALUE+r')\s*('+_UNIT+r')', re.I)


def _unit(value: str) -> str:
    value = value.strip().casefold().replace('x', '×')
    if re.fullmatch(r'percent|per\s+cent', value):return '%'
    if re.fullmatch(r'percentage[\s-]+points?', value):return 'percentage_point'
    if re.fullmatch(r'basis[\s-]+points?', value):return 'basis_point'
    return value


def numeric_mentions(text: str) -> list[dict]:
    ignored = [m.span() for m in re.finditer(r'\b(?:Table|Figure|Fig\.|Section|Sec\.|Appendix|Experiment|Proposition|Theorem|Equation|Eq\.)\s+\d+(?:\.\d+)*\b', text, re.I)]
    ignored += [(m['start'],m['end']) for m in url_mentions(text)]
    labels = list(re.finditer(r'(?<!\w)\((\d+)\)(?=\s+[A-Za-z])',text))
    if len(labels)>=2 and [int(m.group(1)) for m in labels]==list(range(1,len(labels)+1)):
        ignored.extend(m.span() for m in labels)
    out=[]
    def add(start,end,value,unit,literal=None):
        if any(a<=start and end<=b for a,b in ignored):return
        if re.search(r'[A-Za-z_]\w*-$',text[:start]):return
        if value.startswith(('-', '+')) and start and text[start-1].isalnum():return
        if any(n['start']<=start<n['end'] for n in out):return
        out.append({'literal':literal or text[start:end], 'value':str(Decimal(value.replace(',','')).normalize()),
                    'unit':_unit(unit),'start':start,'end':end})
    for m in _RANGE.finditer(text):
        for n in (1,2):add(m.start(n),m.end(n),m.group(n),m.group(3))
        ignored.append(m.span())
    for m in _EXPLICIT.finditer(text):add(m.start(),m.end(),m.group('value'),m.group('unit'))
    for m in _BARE.finditer(text):add(m.start(),m.end(),m.group('value'),'')
    # A number followed by a count noun after an indefinite article is an OCR
    # boundary, not a model identifier. Kept as a structural count form.
    for m in re.finditer(r'\b(?:a|an)(\d+)(?=-[A-Za-z]+\b)',text,re.I):add(m.start(1),m.end(1),m.group(1),'')
    return sorted(out,key=lambda n:n['start'])


def atoms_for_block(block: EvidenceBlock, context: EvidenceContext) -> list[dict]:
    if block not in context.blocks or digest(block.text)!=block.content_hash:
        raise ValueError('atom source is not a canonical block')
    base={'version':ATOM_VERSION,'evidence_id':block.evidence_id,'canonical_id':context.canonical_id,
          'manuscript_hash':context.source_hash,'evidence_version':context.version,
          'context_id':context.context_id,'context_hash':digest(context.text),
          'block_hash':block.content_hash,'pages':block.pages,'section':block.spans[0].section,
          'source_spans':[{k:v for k,v in asdict(s).items() if k != 'text'} for s in block.spans]}
    values=[{'kind':'text_span','raw':block.text,'normalized':re.sub(r'\s+',' ',block.text).strip(),'start':0,'end':len(block.text)}]
    values += [{'kind':'url','raw':u['literal'],'normalized':u['normalized'],'start':u['start'],'end':u['end']} for u in url_mentions(block.text)]
    values += [{'kind':'numeric_quantity','raw':n['literal'],'normalized':{'value':n['value'],'unit':n['unit']},
                'start':n['start'],'end':n['end'],'context':block.text[max(0,n['start']-80):n['end']+80],
                'semantic_fields':'metric, entity, task/dataset, direction, comparison and relative/absolute meaning require scoped semantic verification'} for n in numeric_mentions(block.text)]
    return [{**base,**v,'atom_id':digest(context.context_id+block.evidence_id+str(i)+ATOM_VERSION)[:24]} for i,v in enumerate(values)]
