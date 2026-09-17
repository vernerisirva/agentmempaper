"""Bounded context and typed artifact facts; neither grants scientific quality."""
from __future__ import annotations

import re
from paper_scout.evidence_atoms import url_mentions

from paper_scout.evidence_context import EvidenceContext, EvidenceEligibilityError, resolve_evidence_ids

SCIENTIFIC = 'scientific_claim'
ARTIFACT = 'artifact_availability'
ARTIFACT_EXPLANATION = ('The URL is stated in the supplied manuscript. Repository existence, '
                        'contents and functionality were not independently checked.')


def source_urls(text: str) -> list[str]:
    return list(dict.fromkeys(u['normalized'] for u in url_mentions(text)))


def resolve_claim_blocks(item: dict, context: EvidenceContext, expected_id: str):
    artifact = item.get('evidence_purpose', SCIENTIFIC) == ARTIFACT
    blocks = resolve_evidence_ids(item['evidence_ids'], context,
        expected_context_id=expected_id, artifact_metadata=artifact)
    if not item.get('include_adjacent_context', False):
        return blocks
    if artifact or len(blocks) != 1:
        raise EvidenceEligibilityError('a context window requires one scientific primary block')
    primary = blocks[0]
    selected = {primary.sequence: primary}
    # At most the immediate left/right block, with contiguous offsets within
    # the SAME supplied section. Never cross a section, selection or gap barrier.
    for neighbor in context.blocks:
        if abs(neighbor.sequence - primary.sequence) != 1 or not neighbor.eligible:
            continue
        left, right = sorted((primary, neighbor), key=lambda b: b.sequence)
        end, start = left.spans[-1], right.spans[0]
        if (end.section_index == start.section_index and end.end == start.start
                and neighbor.section_role == primary.section_role):
            selected[neighbor.sequence] = neighbor
    ids = [b.evidence_id for _, b in sorted(selected.items())]
    return resolve_evidence_ids(ids, context, expected_context_id=expected_id)


def effective_claim(item: dict, blocks) -> dict:
    """Artifact fields are typed metadata, not free-form quality interpretations.

    Preserve the model proposal in the execution audit. Stored artifact display
    is derived from verified URLs; never promote its free-form claim/explanation.
    Scientific claims keep their actual text and require directional verification.
    """
    purpose = item.get('evidence_purpose', SCIENTIFIC)
    if purpose == SCIENTIFIC:
        if item.get('artifact_urls'):
            raise ValueError('artifact URLs require artifact_availability purpose')
        return item
    if (purpose != ARTIFACT or item['dimension'] != 'reproducibility_and_transparency'
            or item['statement_kind'] != 'source_claim' or item['signal_type'] != 'positive'
            or item['support_status'] != 'supported'):
        raise ValueError('artifact facts must be positive attributed reproducibility metadata')
    urls = item.get('artifact_urls', [])
    available = {u for b in blocks for u in source_urls(b.text)}
    if not urls or any(u not in available for u in urls):
        raise ValueError('artifact URL is not present in the cited manuscript sources')
    return {**item, 'claim': 'The paper provides these artifact links: ' + ', '.join(urls),
            'explanation': ARTIFACT_EXPLANATION}
