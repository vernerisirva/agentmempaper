"""Structural coverage accounting. No scientific merit or evidence interpretation."""
from collections import Counter
import hashlib
import re


# A heading's shape/position establishes a boundary. Its name need not occur in
# a scientific vocabulary. Reject prose punctuation and contents dotted leaders.
_LINE = re.compile(r'(?m)^[ \t]*([^\n]{3,110}?)[ \t]*$')
_FRONT = re.compile(r'(?i)^(?:preface|table of contents|contents|copyright|about the author|title page)$')


def structural_headings(text, established):
    result = []
    for match in _LINE.finditer(text):
        title = match.group(1).strip()
        words = title.split()
        if not 1 <= len(words) <= 12 or any(c in title for c in '.,;=!?'):
            continue
        if not title[0].isalpha() or not title[0].isupper():
            continue
        at_boundary = not text[:match.start()].strip() or text[:match.start()].endswith('\n\n')
        title_case = all(w[0].isupper() or w.casefold() in {'and', 'of', 'the', 'in', 'for', 'to', 'with', 'on'} for w in words)
        if _FRONT.fullmatch(title):
            # Front matter is a structural boundary but not proof of body text.
            continue
        if established and (title.isupper() or (at_boundary and title_case)):
            result.append(match)
    return result


def reference_continuation(text):
    """Positive bibliography signals, never just an inherited page label.

    Ambiguous text is retained, which can add citations to context but cannot
    silently throw away a page of novel scientific prose.
    """
    return bool(re.search(r'(?m)^\s*(?:\[\d+\]|\d+[.)])\s+\S+.*(?:,|\b(?:19|20)\d{2}\b)', text)
                or len(re.findall(r'\b(?:19|20)\d{2}[a-z]?\b', text)) >= 3)


def coverage_manifest(document, pages, body, excluded, selected, selected_indices,
                      character_budget, chunk_characters, uncertain):
    from paper_scout.full_text import _section_kind, _source_characters, EXTRACTION_GAP
    # Old cached extracts have no source-page count. Their retained sequence is
    # the only available bound; gaps/empty pages still fail closed.
    source_pages = document.coverage.get('source_pages') or max((p.page for p in pages), default=0)
    indices = [p.page for p in pages]
    readable = sorted(p.page for p in pages if p.text.strip())
    missing = sorted(set(range(1, source_pages + 1)) - set(readable))
    usage = Counter()
    for i, section in zip(selected_indices, selected):
        usage[i] += _source_characters(section.text)
    rows = []
    for i, section in enumerate(body):
        count = _source_characters(section.text)
        rows.append({'section_index': i, 'heading': section.heading,
                     'role': _section_kind(section.heading), 'page': section.first_page,
                     'source_characters': count, 'supplied_characters': usage[i],
                     'omitted_characters': count - usage[i],
                     'omission_reason': 'context_budget' if usage[i] < count else None})
    scientific = [r for r in rows if r['role'] != 'abstract']
    omitted = [r for r in rows if r['omitted_characters']]
    reasons = []
    if not document.complete or missing or document.coverage.get('unreadable_pages') or EXTRACTION_GAP in document.text:
        reasons.append('extraction_incomplete')
    if len(set(indices)) != len(indices) or any(p < 1 or p > source_pages for p in indices):
        reasons.append('invalid_page_sequence')
    if uncertain or not scientific:
        reasons.append('scientific_body_not_established')
    if omitted:
        reasons.append('scientific_context_budget_exceeded')
    # Dotted-leader lists describe absent sections. They do not supply the body
    # of a chapter, even when individual titles look like scientific headings.
    contents_pages = [p.page for p in pages if len(re.findall(r'\.{4,}\s*\d+', p.text)) >= 3]
    body_pages = sorted({r['page'] for r in scientific if r['page'] is not None})
    if contents_pages and not set(body_pages) - set(contents_pages):
        reasons.append('front_matter_or_contents_only')
    roles = {r['role'] for r in scientific}
    supplied_roles = {r['role'] for r in scientific if r['supplied_characters']}
    return {'structure_version': 'page-sections-v2', 'source_pages': source_pages,
            'successfully_extracted_pages': readable, 'missing_page_indices': missing,
            'scientific_body_pages': body_pages,
            'pages_omitted': sorted(set(indices) - {s.first_page for s in selected}),
            'body_pages_partially_omitted': sorted({r['page'] for r in omitted if r['page'] is not None}),
            'section_roles_detected': sorted(roles), 'section_roles_represented': sorted(supplied_roles),
            'section_roles_omitted': sorted({r['role'] for r in omitted}),
            'character_budget': character_budget, 'selection_chunk_characters': chunk_characters,
            'budget_unit': 'characters (no tokenizer estimate)', 'sections': rows,
            'excluded_sections': [{'heading': s.heading, 'page': s.first_page,
                                   'characters': _source_characters(s.text), 'reason': 'explicit_back_matter'} for s in excluded],
            'failure_reasons': reasons}


def validate_assessment_coverage(selected):
    """Require a current manifest and complete supplied scientific context.

    Legacy receipts remain readable; this applies only before NEW paid calls.
    No threshold claims that an arbitrary fraction suffices for scientific merit.
    """
    c = selected.coverage
    if c.get('version') != 'coverage-v2':
        return ['coverage_manifest_missing_or_legacy']
    if c.get('assessment_input_sha256') != hashlib.sha256(selected.text.encode('utf-8')).hexdigest():
        raise ValueError('coverage manifest does not describe the supplied text')
    reasons = list(c.get('failure_reasons', []))
    if (c.get('status') != 'complete' or selected.scope != 'full_text'
            or c.get('extraction_complete') is not True or c.get('omitted_body_characters') != 0
            or c.get('body_pages_partially_omitted') or c.get('missing_page_indices')
            or not c.get('scientific_body_pages')):
        reasons.append('incomplete_scientific_context')
    return list(dict.fromkeys(reasons))
