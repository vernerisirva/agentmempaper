"""Deterministic addresses into the exact text supplied for one assessment.

Addresses prove provenance, not the truth of the assessor's interpretation.
Legacy quote-based assessments do not use or require this protocol.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import re

from paper_scout.full_text import SelectedPaperText, _section_kind, EXTRACTION_GAP

EVIDENCE_VERSION = 'block-evidence-v2'
BLOCK_CHARACTERS = 900


def digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


@dataclass(frozen=True)
class SourceSpan:
    text: str
    page: int | None
    section: str
    section_index: int
    start: int
    end: int


@dataclass(frozen=True)
class EvidenceBlock:
    evidence_id: str
    sequence: int
    text: str
    content_hash: str
    spans: tuple[SourceSpan, ...]
    eligible: bool
    section_role: str

    @property
    def pages(self) -> list[int]:
        return sorted({s.page for s in self.spans if s.page is not None})


@dataclass(frozen=True)
class EvidenceContext:
    version: str
    canonical_id: str
    source_hash: str
    selected_text_hash: str
    context_id: str
    text: str
    blocks: tuple[EvidenceBlock, ...]
    preamble: str

    def metadata(self) -> dict:
        return {'evidence_version': self.version, 'evidence_context_id': self.context_id,
                'evidence_context_sha256': digest(self.text), 'evidence_context_characters': len(self.text),
                'evidence_block_count': len(self.blocks), 'canonical_id': self.canonical_id,
                'source_content_hash': self.source_hash, 'selected_text_sha256': self.selected_text_hash}


def _span_text(spans: tuple[SourceSpan, ...]) -> str:
    """Join only certified adjacent page continuations; keep lexical hyphens.

    A page-final 'long-' followed by 'term' becomes 'long-term'. We do not guess
    whether a lexical hyphen should be deleted, strip headers, or join sections.
    The original text and offsets of both pages remain in SourceSpan.
    """
    result = ''
    previous = None
    for span in spans:
        if not result:
            result = span.text
        elif (previous is not None and previous.page is not None and span.page == previous.page + 1
              and previous.section == span.section and re.search(r'[A-Za-z]-\s*$', previous.text)
              and re.match(r'\s*[a-z]', span.text)):
            result = result.rstrip() + span.text.lstrip()
        else:
            result += '\n' + span.text
        previous = span
    return result


def evidence_section_role(heading: str) -> str:
    """Classify evidence provenance without changing acquisition or selection.

    Unrecognized manuscript headings retain the existing ``body`` role. Explicit
    non-body headings cannot become body candidates through that fallback.
    """
    value = re.sub(r'^\s*(?:\d+(?:\.\d+)*[.)]?|[IVX]+[.)])\s+', '', heading).strip()
    if re.fullmatch(
        r'metadata|front matter|title page|author (?:information|affiliations?)|'
        r'(?:copyright(?: and licen[cs](?:e|ing))?|licen[cs](?:e|ing))'
        r'(?: information| notice| statement)?', value, re.I
    ):
        return 'excluded'
    return _section_kind(value)


def build_evidence_context(canonical_id: str, selected: SelectedPaperText) -> EvidenceContext:
    if not canonical_id.strip():
        raise ValueError('evidence context requires manuscript identity')
    # Every span is derived from an actual supplied section, never unseen source
    # text. No extraction or selection is performed by this addressing layer.
    cursor = 0
    groups: list[list[SourceSpan]] = []
    complete_selection = (selected.scope == 'full_text' and not selected.coverage.get('selected_instead_of_full_text')
                          and not selected.coverage.get('extraction_truncated'))
    previous = None
    for i, section in enumerate(selected.sections):
        offset = selected.text.find(section.text, cursor)
        if offset < 0:
            raise ValueError('evidence section is absent from supplied assessment text')
        cursor = offset + len(section.text)
        # Never merge selected disjoint excerpts or an extraction gap. Full,
        # adjacent physical pages under the identical heading can share a block.
        continuation = bool(complete_selection and previous and previous.heading == section.heading
                            and previous.first_page is not None and section.first_page == previous.first_page + 1
                            and EXTRACTION_GAP not in previous.text + section.text)
        if not continuation or not groups:
            groups.append([])
        start = 0
        while start < len(section.text):
            used = sum(len(s.text) for s in groups[-1])
            space = BLOCK_CHARACTERS - used
            if space < 80:
                groups.append([])
                space = BLOCK_CHARACTERS
            end = min(len(section.text), start + space)
            if end < len(section.text):
                boundary = section.text.rfind(' ', start + space // 2, end)
                if boundary > start:
                    end = boundary + 1
            groups[-1].append(SourceSpan(section.text[start:end], section.first_page, section.heading, i, start, end))
            start = end
            if start < len(section.text):
                groups.append([])
        previous = section
    blocks = []
    for spans in groups:
        if not spans:
            continue
        spans = tuple(spans)
        text = _span_text(spans)
        blocks.append(EvidenceBlock('', len(blocks) + 1, text, digest(text), spans,
                      all(evidence_section_role(s.section) != 'excluded' for s in spans)
                      and EXTRACTION_GAP not in text, evidence_section_role(spans[0].section)))
    # Version, manuscript bytes, selected context, offsets, eligibility and block
    # contents all bind the ID namespace. Same page numbers never imply same IDs.
    preamble = selected.text[:selected.text.find(selected.sections[0].text)] if selected.sections else selected.text
    context_id = _context_digest(EVIDENCE_VERSION, canonical_id, selected.content_hash,
                                 digest(selected.text), preamble, tuple(blocks))
    blocks = tuple(replace(b, evidence_id=f'E{context_id[:16]}-B{b.sequence:04d}') for b in blocks)
    text = _render_context(preamble, blocks)
    return EvidenceContext(EVIDENCE_VERSION, canonical_id, selected.content_hash, digest(selected.text), context_id, text, blocks, preamble)


def _context_digest(version: str, canonical_id: str, source_hash: str, selected_text_hash: str,
                    preamble: str, blocks: tuple[EvidenceBlock, ...]) -> str:
    # selected_text_hash already binds the preamble. Its explicit hash also lets
    # the standalone resolver verify rendered-context integrity without source IO.
    return digest(json.dumps({'version': version, 'canonical_id': canonical_id,
        'source_hash': source_hash, 'selected_text_hash': selected_text_hash,
        'preamble_hash': digest(preamble),
        'blocks': [asdict(replace(b, evidence_id='')) for b in blocks]}, sort_keys=True, ensure_ascii=False))


def _render_context(preamble: str, blocks: tuple[EvidenceBlock, ...]) -> str:
    return preamble + '\n\n'.join(f'[{b.evidence_id}] pages={",".join(map(str,b.pages)) or "unknown"}; section={b.spans[0].section}; section_role={b.section_role}; provenance_eligible={str(b.eligible).lower()}\n{b.text}' for b in blocks)


def resolve_evidence_ids(ids: list[str], context: EvidenceContext, *, expected_context_id: str, artifact_metadata: bool = False) -> tuple[EvidenceBlock, ...]:
    identity = _context_digest(context.version, context.canonical_id, context.source_hash,
                               context.selected_text_hash, context.preamble, context.blocks)
    if (context.version != EVIDENCE_VERSION or context.context_id != expected_context_id
            or identity != context.context_id or _render_context(context.preamble, context.blocks) != context.text
            or any(b.evidence_id != f'E{context.context_id[:16]}-B{b.sequence:04d}' for b in context.blocks)):
        raise ValueError('evidence context integrity mismatch')
    index = {b.evidence_id: b for b in context.blocks}
    if not ids or len(set(ids)) != len(ids):
        raise ValueError('missing or duplicate evidence IDs')
    found = []
    for evidence_id in ids:
        block = index.get(evidence_id)
        if block is None:
            raise ValueError('evidence ID not supplied in this manuscript context')
        if not block.eligible and not (artifact_metadata and artifact_metadata_block(block)):
            raise ValueError('evidence block is excluded back matter or an extraction gap')
        if digest(block.text) != block.content_hash or _span_text(block.spans) != block.text:
            raise ValueError('evidence block content hash mismatch')
        found.append(block)
    return tuple(sorted(found, key=lambda b: b.sequence))


def artifact_metadata_block(block: EvidenceBlock) -> bool:
    """Only supplied front/title metadata, never references or extraction gaps."""
    return (EXTRACTION_GAP not in block.text and all(re.fullmatch(
        r'front matter|title page|metadata|abstract / front matter', s.section.strip(), re.I)
        for s in block.spans))
