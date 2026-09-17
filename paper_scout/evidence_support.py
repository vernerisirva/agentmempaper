"""Bounded context and typed artifact facts; neither grants scientific quality."""
from __future__ import annotations

import re
from urllib.parse import urlsplit

from paper_scout.evidence_context import EvidenceContext, resolve_evidence_ids

SCIENTIFIC = 'scientific_claim'
ARTIFACT = 'artifact_availability'
ARTIFACT_EXPLANATION = ('The URL is stated in the supplied manuscript. Repository existence, '
                        'contents and functionality were not independently checked.')


def source_urls(text: str) -> list[str]:
    # Join an explicit URL slash continuation only, preserving its source block.
    text = re.sub(r'(?<=/)\s*\n\s*(?=[A-Za-z0-9])', '', text)
    urls = []
    for match in re.finditer(r'https?://[^\s<>"\[\]]+', text):
        url = match.group().rstrip('.,;:)')
        try:
            parsed = urlsplit(url)
            _ = parsed.port
            if parsed.hostname and not parsed.username and not parsed.password:
                urls.append(url)
        except ValueError:
            continue  # Malformed source URLs are not artifact candidates.
    return list(dict.fromkeys(urls))


def resolve_claim_blocks(item: dict, context: EvidenceContext, expected_id: str):
    artifact = item.get('evidence_purpose', SCIENTIFIC) == ARTIFACT
    blocks = resolve_evidence_ids(item['evidence_ids'], context,
        expected_context_id=expected_id, artifact_metadata=artifact)
    if not item.get('include_adjacent_context', False):
        return blocks
    if artifact or len(blocks) != 1:
        raise ValueError('a context window requires one scientific primary block')
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


def scope_issues(claim: str, explanation: str, texts: list[str]) -> list[str]:
    """Necessary fail-closed guards for known nonlocal inferences, not entailment."""
    text = claim + '\n' + explanation
    issues = []
    if re.search(r'(?:not available|unavailable|no (?:other|single) (?:source|work|study)).{0,80}(?:elsewhere|other source|single source)|'
                 r'(?:first|only) (?:ever |existing )?(?:study|work|paper|system)\b', text, re.I):
        issues.append('External priority/uniqueness is not established by local manuscript excerpts.')
    if re.search(r'(?:paper|manuscript|authors?|survey)\s+(?:does? not|do not|lacks?|never|fails? to).{0,65}'
                 r'(?:section|release|releas\w+|report|discuss|describ|provide|includ)', text, re.I):
        issues.append('Manuscript-wide absence requires more than local excerpts; scope the observation to the cited material.')
    # A source excerpt can support scoped synthesis, but an explicit partial
    # result cannot establish universal success even if a verifier says so.
    universal = re.search(r'\b(?:all|every) (?:evaluated )?(?:tasks?|benchmarks?|datasets?)\b|\bconsistently (?:improves?|outperforms?)', text, re.I)
    # This guard only rejects positive universal assertions. Negative/scoped
    # critiques still go through exact semantic verification.
    negated = re.search(r'\b(?:not|never|cannot|no|unsupported|inconsistent)\b|fails? to', text, re.I)
    if universal and not negated:
        if any(re.search(r'\b(?:two of three|2 (?:of|out of) 3|some but not all|fails? on|worse on)\b', s, re.I) for s in texts):
            issues.append('The cited evidence includes partial or contrary outcomes; universal improvement is not established.')
    return issues
