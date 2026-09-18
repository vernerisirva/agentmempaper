from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import ipaddress
from io import BytesIO
import json
import logging
from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from paper_scout.models import PaperCandidate


LOGGER = logging.getLogger(__name__)
USER_AGENT = "Paper-Scout/1.0 (+https://github.com/vernerisirva/agentmempaper)"
EXTRACTION_GAP = "[Extraction gap: source text omitted]"


def _source_characters(text: str) -> int:
    """Exclude synthetic extraction barriers from manuscript character counts."""
    return len(text.replace(EXTRACTION_GAP, ""))


@dataclass(frozen=True)
class ExtractedPage:
    page: int
    text: str


@dataclass(frozen=True)
class FullTextDocument:
    source_url: str
    pages: list[ExtractedPage]
    content_hash: str
    complete: bool
    cache_hit: bool = False
    warnings: list[str] = field(default_factory=list)
    coverage: dict = field(default_factory=dict)

    @property
    def text(self) -> str:
        return "\n\n".join(page.text for page in self.pages if page.text)


@dataclass(frozen=True)
class SelectedSection:
    heading: str
    text: str
    first_page: int | None


@dataclass(frozen=True)
class SelectedPaperText:
    text: str
    sections: list[SelectedSection]
    scope: str
    content_hash: str
    section_detection_uncertain: bool
    warnings: list[str] = field(default_factory=list)
    coverage: dict = field(default_factory=dict)


class FullTextSettings(Protocol):
    cache_dir: Path
    timeout_seconds: int
    max_pdf_megabytes: int
    max_pages: int
    max_extracted_characters: int
    max_prompt_characters: int
    max_section_characters: int


class SafeRedirectHandler(HTTPRedirectHandler):
    def __init__(self, max_redirects: int = 5) -> None:
        super().__init__()
        self.max_redirects = max_redirects

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        count = int(req.headers.get("X-Paper-Scout-Redirects", "0")) + 1
        if count > self.max_redirects:
            raise HTTPError(req.full_url, code, "too many redirects", headers, fp)
        resolved = urljoin(req.full_url, newurl)
        _validate_http_url(resolved)
        redirected = super().redirect_request(req, fp, code, msg, headers, resolved)
        if redirected is not None:
            redirected.add_header("X-Paper-Scout-Redirects", str(count))
        return redirected


def locate_full_text_urls(candidate: PaperCandidate, direct_pdf_url: str | None = None) -> list[str]:
    urls: list[str] = []
    if direct_pdf_url:
        urls.append(direct_pdf_url)
    arxiv_id = candidate.arxiv_id
    if not arxiv_id and candidate.doi and candidate.doi.lower().startswith("10.48550/arxiv."):
        arxiv_id = candidate.doi[len("10.48550/arxiv."):]
    if arxiv_id:
        urls.append(f"https://arxiv.org/pdf/{arxiv_id}")
        urls.append(f"https://arxiv.org/pdf/{arxiv_id}.pdf")
    raw = candidate.raw if isinstance(candidate.raw, dict) else {}
    for item in raw.get("files") or []:
        if isinstance(item, dict) and str(item.get("key") or "").lower().endswith(".pdf"):
            link = (item.get("links") or {}).get("self")
            if link:
                urls.append(str(link))
    if candidate.url and candidate.url.lower().endswith(".pdf"):
        urls.append(candidate.url)
    semantic_pdf = raw.get("openAccessPdf")
    if isinstance(semantic_pdf, dict) and semantic_pdf.get("url"):
        urls.append(str(semantic_pdf["url"]))
    for key in ("best_oa_location", "primary_location"):
        location = raw.get(key)
        if isinstance(location, dict):
            for url_key in ("pdf_url", "landing_page_url"):
                value = location.get(url_key)
                if value and (url_key == "pdf_url" or str(value).lower().endswith(".pdf")):
                    urls.append(str(value))
    locations = raw.get("locations")
    if isinstance(locations, list):
        for location in locations:
            if isinstance(location, dict) and location.get("pdf_url"):
                urls.append(str(location["pdf_url"]))
    result: list[str] = []
    for url in urls:
        try:
            _validate_http_url(url)
        except ValueError:
            continue
        if url not in result:
            result.append(url)
    return result


def fetch_and_extract_pdf(url: str, settings: FullTextSettings, refresh: bool = False) -> FullTextDocument:
    _validate_http_url(url)
    cache_path = _cache_path(settings.cache_dir, url)
    cached = None if refresh else _load_cached_document(cache_path)
    if cached is not None:
        return FullTextDocument(**{**cached.__dict__, "cache_hit": True})
    payload, content_type = _download_pdf(url, settings.timeout_seconds, settings.max_pdf_megabytes)
    if _public_jats_url(url):
        document = _extract_jats(payload, url, settings.max_pages, settings.max_extracted_characters)
    else:
        if not _plausible_pdf(payload, content_type):
            raise ValueError("full-text response was not a plausible PDF")
        document = _extract_pdf(payload, url, settings.max_pages, settings.max_extracted_characters)
    _write_cached_document(cache_path, document)
    return document


def canonical_manuscript_text(text: str) -> str:
    """Canonical typography and valid Unicode shared by prompt and anchors.

    Physical line breaks remain available so line-end hyphens can be interpreted
    conservatively in multiple literal views. No words or numbers are repaired.
    """
    # PDF extractors/caches can contain UTF-16 code units rather than Unicode
    # scalar values. Recombine valid pairs; visibly replace irrecoverable lone
    # surrogates before hashing, addressing, transport or persistence. Never
    # invent the missing scientific symbol. Valid Unicode is unchanged.
    if re.search(r'[\ud800-\udfff]', text):
        text = text.encode('utf-16-le', errors='surrogatepass').decode('utf-16-le', errors='replace')
    text = unicodedata.normalize("NFC", text)
    text = text.translate(str.maketrans(dict(zip("ﬀﬁﬂﬃﬄﬅﬆ", ("ff", "fi", "fl", "ffi", "ffl", "st", "st")))))
    return text.translate(str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "‐": "-", "‑": "-", "\u00ad": None})).replace("\r\n", "\n")


def _section_kind(heading: str) -> str:
    value = heading.casefold()
    if re.fullmatch(r'references|bibliography|acknowledgements?|acknowledgments?|funding(?: statement)?|author contributions?|conflicts? of interest', value.strip()):
        return 'excluded'
    if value.startswith(('appendix', 'supplement')):
        return 'appendix'
    for kind, pattern in (
        ('abstract', r'abstract|front matter'), ('introduction', r'introduction|contribution|problem'),
        ('methods', r'method|architecture|implementation|setup|protocol|training'),
        ('results', r'result|evaluation|experiment|ablation|benchmark|validation'),
        ('limitations', r'limitation|threat|uncertainty'), ('discussion', r'discussion|implication'),
        ('conclusion', r'conclusion|outlook'), ('related', r'related work|background')):
        if re.search(pattern, value):
            return kind
    return 'body'


def _spread_order(items: list) -> list:
    """Beginning, middle and end first, then evenly subdivide the remaining gaps."""
    if not items:
        return []
    indices = list(dict.fromkeys((0, len(items) // 2, len(items) - 1)))
    while len(indices) < len(items):
        ordered = sorted(indices)
        gaps = [(b - a, a, b) for a, b in zip(ordered, ordered[1:]) if b - a > 1]
        _, left, right = max(gaps)
        indices.append((left + right) // 2)
    return [items[i] for i in indices]


def _section_chunks(section: SelectedSection, size: int) -> list[SelectedSection]:
    if size <= 0:
        raise ValueError("chunk size must be positive")
    chunks = []
    start = 0
    while start < len(section.text):
        end = min(start + size, len(section.text))
        if end < len(section.text):
            boundary = section.text.rfind('\n', start + size // 2, end)
            if boundary < 0:
                boundary = section.text.rfind(' ', start + size // 2, end)
            if boundary > start:
                end = boundary
        chunks.append(SelectedSection(section.heading, section.text[start:end], section.first_page))
        start = end
    return chunks


def select_assessment_text(
    candidate: PaperCandidate,
    document: FullTextDocument | None,
    max_prompt_characters: int = 180_000,
    max_section_characters: int = 8_000,
) -> SelectedPaperText:
    if max_prompt_characters <= 0 or max_section_characters <= 0:
        raise ValueError("assessment text budgets must be positive")
    abstract = canonical_manuscript_text(candidate.abstract)
    title = canonical_manuscript_text(candidate.title)
    if document is None or not any(p.text.strip() for p in document.pages):
        content = f'Title: {title}\n\nAbstract: {abstract}'[:max_prompt_characters]
        return SelectedPaperText(content, [SelectedSection('Abstract', abstract, None)] if abstract else [],
            'title_and_abstract' if abstract else 'metadata_only', _content_hash(content), False,
            ['No extractable manuscript text was available.'],
            {'version': 'coverage-v1', 'extraction_complete': False, 'assessment_input_characters': len(content)})

    pages = [ExtractedPage(p.page, canonical_manuscript_text(p.text)) for p in document.pages]
    logical_xml = document.coverage.get('format') == 'JATS' or any('JATS XML:' in w for w in document.warnings)
    detected = ([SelectedSection(p.text.partition('\n')[0], p.text.partition('\n')[2], p.page) for p in pages]
                if logical_xml else _detect_sections(pages))
    # XML body membership is stronger evidence than a title such as References.
    if logical_xml:
        detected = [SelectedSection('Body section: ' + s.heading if _section_kind(s.heading) == 'excluded' else s.heading,
                                    s.text, s.first_page) for s in detected]
    uncertain = not any(_section_kind(s.heading) not in {'abstract', 'excluded'} for s in detected)
    if not detected:
        # Unknown boundaries are visible but cannot supply body evidence.
        detected = [SelectedSection('Abstract / unclassified page', p.text, p.page) for p in pages]
    excluded = [s for s in detected if _section_kind(s.heading) == 'excluded']
    body = [s for s in detected if _section_kind(s.heading) != 'excluded']
    prefix = f'Title: {title}\n\n'
    # The extracted abstract is already in body. Avoid duplicating metadata text.
    if not any(_section_kind(s.heading) == 'abstract' for s in body) and abstract:
        prefix += f'Abstract (metadata): {abstract[:2400]}\n\n'
    def render(s):
        return f'## {s.heading}\n[Page {s.first_page or "unknown"}]\n{s.text}\n\n'
    all_text = prefix + ''.join(render(s) for s in body)
    selected = body
    chunk_size = None
    selected_indices = list(range(len(body)))
    selection_used = len(all_text) > max_prompt_characters
    if selection_used:
        # Round-robin by role, then contiguous logical section. A long method
        # keeps adjacent chunks/pages, without a per-heading cap hiding its tail.
        # This diagnostic partial context is NEVER approved for a paid call.
        chunk_size = max(80, min(max_section_characters, max_prompt_characters // 24, 2000))
        groups = {}
        logical = []
        for i, section in enumerate(body):
            chunks = _section_chunks(section, chunk_size)
            if not chunks:
                continue
            if not logical or logical[-1][-1][1].heading != section.heading:
                logical.append([])
            logical[-1].extend((i, c) for c in chunks)
        for group in logical:
            groups.setdefault(_section_kind(group[0][1].heading), []).append(group)
        order = ('methods', 'results', 'limitations', 'discussion', 'conclusion',
                 'introduction', 'appendix', 'body', 'related', 'abstract')
        chosen = []
        text_length = len(prefix[:max_prompt_characters])
        while any(group for role in groups.values() for group in role):
            for kind in order:
                for group in groups.get(kind, []):
                    if not group:
                        continue
                    i, section = group.pop(0)
                    size = len(render(section))
                    if text_length + size <= max_prompt_characters:
                        chosen.append((i, section))
                        text_length += size
                    else:
                        # Keep each section's prefix contiguous; do not leap over
                        # an omitted chunk to pick an isolated smaller tail.
                        group.clear()
        chosen.sort(key=lambda item: item[0])  # stable chunk/source order
        selected_indices = [i for i, _ in chosen]
        selected = [section for _, section in chosen]
        all_text = prefix[:max_prompt_characters] + ''.join(render(s) for s in selected)
    if len(all_text) > max_prompt_characters:
        raise ValueError("assessment text exceeded its configured budget")
    body_chars = sum(_source_characters(s.text) for s in body)
    selected_chars = sum(_source_characters(s.text) for s in selected)
    warnings = list(document.warnings)
    surrogate_count = sum(len(re.findall(r'[\ud800-\udfff]', p.text)) for p in document.pages)
    if surrogate_count:
        warnings.append(f'Canonical Unicode normalization processed {surrogate_count} UTF-16 surrogate code units; unpaired units are visible replacement characters, not reconstructed symbols.')
    if EXTRACTION_GAP in document.text:
        warnings.append("Extraction gaps are explicit barriers, excluded from source-character counts; omitted extraction text is not available to the assessor.")
    if selection_used:
        warnings.append(f'Representative manuscript excerpts selected: {selected_chars} of {body_chars} eligible characters; omitted passages are unavailable to the assessor.')
    if excluded:
        warnings.append('Structurally bounded citation prefixes excluded; ambiguous back matter, body and detected appendices retained where budget permits.')
    if uncertain:
        warnings.append('Manuscript section boundaries are uncertain; unclassified abstract pages cannot ground a body-text decision.')
    coverage = {**document.coverage, 'version': 'coverage-v2', 'selection_version': 'contiguous-balanced-v2',
        'normalization_version': 'canonical-unicode-v2', 'surrogate_code_units': surrogate_count, 'source_pages': document.coverage.get('source_pages'),
        'page_unit': 'logical XML body section' if logical_xml else 'PDF page',
        'extracted_pages': len(document.pages), 'extracted_page_indices': [p.page for p in document.pages],
        'extracted_characters': len(document.text),
        'retained_source_characters': sum(_source_characters(p.text) for p in document.pages),
        'extraction_gap_markers': document.text.count(EXTRACTION_GAP), 'extraction_complete': document.complete,
        'extraction_truncated': not document.complete,
        'assessment_input_characters': len(all_text), 'assessment_input_sha256': _content_hash(all_text),
        'selected_pages': sorted({s.first_page for s in selected if s.first_page is not None}),
        'selected_characters': selected_chars, 'eligible_characters': body_chars,
        'omitted_body_characters': body_chars - selected_chars,
        'excluded_back_matter_characters': sum(_source_characters(s.text) for s in excluded),
        'selected_instead_of_full_text': selection_used,
        'selected_sections': [{'heading':s.heading, 'page':s.first_page, 'characters':_source_characters(s.text)} for s in selected],
        'warnings': warnings}
    from paper_scout.manuscript_coverage import coverage_manifest
    coverage.update(coverage_manifest(document, pages, body, excluded, selected,
                                     selected_indices, max_prompt_characters,
                                     chunk_size, uncertain))
    coverage["configured_max_section_characters"] = max_section_characters
    coverage['status'] = 'complete' if not coverage['failure_reasons'] else 'text_coverage_failure'
    # Completeness is technical. Missing scientific merit remains the models' job.
    scope = 'full_text' if coverage['status'] == 'complete' else 'partial_full_text'
    return SelectedPaperText(all_text, selected, scope, document.content_hash, uncertain, warnings, coverage)


def _download_pdf(url: str, timeout_seconds: int, max_pdf_megabytes: int) -> tuple[bytes, str]:
    limit = max(1, max_pdf_megabytes) * 1024 * 1024
    opener = build_opener(SafeRedirectHandler(max_redirects=5))
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/xml" if _public_jats_url(url) else "application/pdf"})
    try:
        with opener.open(request, timeout=max(1, timeout_seconds)) as response:
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > limit:
                raise ValueError(f"PDF exceeds the configured {max_pdf_megabytes} MB limit")
            payload = response.read(limit + 1)
            if len(payload) > limit:
                raise ValueError(f"PDF exceeds the configured {max_pdf_megabytes} MB limit")
            return payload, str(response.headers.get("Content-Type") or "")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"full-text download failed: {exc}") from exc


def _public_jats_url(url: str) -> bool:
    parts = urlparse(url)
    return parts.scheme == "https" and parts.hostname == "www.ebi.ac.uk" and bool(
        re.fullmatch(r"/europepmc/webservices/rest/PMC\d+/fullTextXML", parts.path))


def _extract_jats(payload: bytes, url: str, max_pages: int, max_characters: int) -> FullTextDocument:
    """Read public Europe PMC JATS body sections with explicit logical locations."""
    # No entity expansion or external document declarations from remote XML.
    if b"<!DOCTYPE" in payload.upper() or b"<!ENTITY" in payload.upper():
        raise ValueError("JATS declarations are unsupported")
    root = ET.fromstring(payload)
    for element in root.iter():
        element.tag = element.tag.rsplit("}", 1)[-1]
    body = root.find("body") if root.tag == "article" else None
    if body is None:
        raise ValueError("JATS response has no article body")
    sections = list(body.findall("sec"))
    if not sections:
        raise ValueError("JATS response has no body sections")
    pages = []
    remaining = max_characters
    total = 0
    for index, section in enumerate(sections, 1):
        title = section.find("title")
        heading = " ".join(title.itertext()) if title is not None else f"Body section {index}"
        content = "\n".join(" ".join(child.itertext()) for child in section if child is not title)
        text = heading + "\n" + content
        total += len(text)
        pages.append(ExtractedPage(index, text))
    pages = sorted(_spread_order(pages)[:max(1, max_pages)], key=lambda p: p.page)
    if not any(p.text.partition("\n")[2].strip() for p in pages):
        raise ValueError("JATS body is empty")
    pages = _bounded_pages(pages, max_characters)
    omitted_body_text = any(child.tag != "sec" and "".join(child.itertext()).strip() for child in body)
    complete = len(sections) <= max_pages and total <= max_characters and not omitted_body_text
    warnings = ["JATS XML: Page labels are logical body-section numbers, not PDF pages."]
    if omitted_body_text:
        warnings.append("JATS body text outside section elements was omitted; extraction is partial.")
    if len(sections) > max_pages or total > max_characters:
        warnings.append("JATS extraction was limited by the configured section/character bounds.")
    return FullTextDocument(url, pages, hashlib.sha256(payload).hexdigest(), complete, warnings=warnings,
        coverage={"extractor_version":"bounded-v2", "format":"JATS", "source_pages":len(sections),
                  "characters_before_extraction_limit":total, "max_pages":max_pages, "max_extracted_characters":max_characters})


def _retain_page_text(text: str, budget: int) -> str:
    if len(text) <= budget:
        return text
    marker = '\n' + EXTRACTION_GAP + '\n'
    # Each disjoint passage has a visible barrier, so validation cannot silently
    # join text from opposite sides of an extraction gap.
    part = max(0, (budget - 2 * len(marker)) // 3)
    if part < 20:
        return ''
    middle = max(part, (len(text) - part) // 2)
    return text[:part] + marker + text[middle:middle + part] + marker + text[-part:]


def _bounded_pages(pages: list[ExtractedPage], budget: int) -> list[ExtractedPage]:
    allocations = [0] * len(pages)
    remaining = max(0, budget)
    active = list(range(len(pages)))
    while active and remaining:
        share = max(1, remaining // len(active))
        for i in active:
            add = min(share, len(pages[i].text) - allocations[i], remaining)
            allocations[i] += add
            remaining -= add
        active = [i for i in active if allocations[i] < len(pages[i].text)]
    return [ExtractedPage(p.page, _retain_page_text(p.text, n)) for p, n in zip(pages, allocations)]


def _extract_pdf(payload: bytes, url: str, max_pages: int, max_characters: int) -> FullTextDocument:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError('pypdf is required for full-text extraction') from exc
    reader = PdfReader(BytesIO(payload))
    count = len(reader.pages)
    indices = sorted(_spread_order(list(range(count)))[:max(1, max_pages)])
    pages = []
    failed = []
    for index in indices:
        try:
            text = reader.pages[index].extract_text() or ''
        except Exception:  # One failed page cannot silently count as complete.
            text = ''
        if not text.strip():
            failed.append(index + 1)
        pages.append(ExtractedPage(index + 1, text))
    characters = sum(len(p.text) for p in pages)
    retained = _bounded_pages(pages, max_characters)
    complete = len(indices) == count and characters <= max_characters and not failed
    warnings = []
    if len(indices) < count:
        warnings.append(f'Page limit: extracted {len(indices)} of {count} source pages, spread across beginning/middle/end.')
    if characters > max_characters:
        warnings.append(f'Character limit: extracted passages capped at {max_characters} characters with explicit gaps; source text in attempted pages has {characters} characters.')
    if failed:
        warnings.append('Pages without extractable text (blank, image-only or failed): ' + ', '.join(map(str, failed)))
    return FullTextDocument(url, retained, hashlib.sha256(payload).hexdigest(), complete, warnings=warnings,
        coverage={'extractor_version':'bounded-v2', 'format':'PDF', 'source_pages':count,
            'attempted_pages':[i + 1 for i in indices], 'unreadable_pages':failed,
            'characters_before_extraction_limit':characters, 'max_pages':max_pages,
            'max_extracted_characters':max_characters})


def _detect_sections(pages: list[ExtractedPage]) -> list[SelectedSection]:
    heading_pattern = re.compile(
        r"(?im)^(?:\d+(?:\.\d+)*\.?\s+)?(abstract|introduction|contributions?|related work|background|method(?:s|ology)?|proposed method|(?:system )?architecture|implementation|experimental setup|experimental protocol|experiments?|evaluation|results(?: and discussion)?|ablation(?: study)?|limitations?|threats to validity|discussion|conclusions?|references|bibliography|acknowledgements?|acknowledgments?|appendix|supplementary (?:material|details))(?::[^\n]{1,100})?\s*$"
    )
    numbered = re.compile(r"(?m)^\d{1,2}(?:\.\d{1,2})*\.?[ \t]+([A-Z][^\n]{2,110})$")
    sections: list[SelectedSection] = []
    current_heading = None
    abstract_page = None
    from paper_scout.manuscript_coverage import structural_headings, split_reference_spans
    for page in pages:
        matches = list(heading_pattern.finditer(page.text))
        # Generic numbered titles terminate a known body section; never infer
        # body evidence merely from an enumerated list inside an abstract.
        body_starts = [m.start() for m in matches if m.group(1).lower() != "abstract"]
        body_start = -1 if current_heading and current_heading.lower() != "abstract" else min(body_starts, default=len(page.text))
        occupied = {m.start() for m in matches}
        matches += [m for m in numbered.finditer(page.text)
                    if (m.start() > body_start or (current_heading == "Abstract" and abstract_page is not None and page.page > abstract_page)) and m.start() not in occupied
                    and not m.group(1).rstrip().endswith((".", ";", ","))]
        appendix = re.compile(r"(?m)^(?:Appendix[ \t]+)?[A-Z](?:\.\d+)*\.?[ \t]+([A-Z][^\n]{3,100})$")
        matches += [m for m in appendix.finditer(page.text) if m.start() not in {v.start() for v in matches}
                    and not any(c in m.group(1) for c in ",;=")
                    and (m.group(1).isupper() or re.match(r"[A-Z]\.\d", m.group(0))
                         or re.match(r"(?i)(?:implementation|experimental|evaluation|additional|detailed|full benchmark|case study|training|hyperparameter|prompt|per-world|memory samples|limitations|diagnostic|proof|data)\b", m.group(1)))]
        # Typography/position provide boundaries for unfamiliar headings. The
        # classifier is used only AFTER finding a section, never to hide one.
        back_starts = [m.start() for m in matches if _section_kind(m.group(1)) == 'excluded']
        back_start = 0 if current_heading and _section_kind(current_heading) == 'excluded' else min(back_starts, default=None)
        structural = structural_headings(page.text, current_heading is not None or bool(matches), back_start)
        occupied = {m.start() for m in matches}
        matches += [m for m in structural if m.start() not in occupied]
        structural_starts = {m.start() for m in structural}
        matches.sort(key=lambda m: m.start())
        named_starts = {m.start() for m in heading_pattern.finditer(page.text)}
        filtered = []
        in_back_matter = bool(current_heading and _section_kind(current_heading) == 'excluded')
        for match in matches:
            if match.start() in named_starts:
                in_back_matter = _section_kind(match.group(1)) == 'excluded'
            elif match.start() in structural_starts or appendix.fullmatch(match.group(0)):
                in_back_matter = False
            elif in_back_matter:
                continue
            filtered.append(match)
        matches = filtered
        prefix = page.text[:matches[0].start()] if matches else page.text
        if (prefix.strip() and current_heading and _section_kind(current_heading) == 'excluded'
                and current_heading.casefold() not in {'references', 'bibliography'}):
            current_heading = 'Unclassified body after back matter'
        if prefix.strip():
            sections.append(SelectedSection(current_heading or "Abstract / front matter", prefix.strip(), page.page))
        for index, match in enumerate(matches):
            current_heading = match.group(1).strip().title()
            if appendix.fullmatch(match.group(0)):
                current_heading = "Appendix: " + current_heading
            if current_heading == "Abstract":
                abstract_page = page.page
            end = matches[index + 1].start() if index + 1 < len(matches) else len(page.text)
            # Preserve novel heading lines as source too: adjacent structural
            # candidates must not make one another's text disappear.
            start = match.start() if match.start() in structural_starts and match.start() not in named_starts else match.end()
            text = page.text[start : end].strip()
            if text:
                sections.append(SelectedSection(current_heading, text, page.page))
    return split_reference_spans(sections)


def _plausible_pdf(payload: bytes, content_type: str) -> bool:
    return payload.startswith(b"%PDF-") and (not content_type or "pdf" in content_type.lower() or "octet-stream" in content_type.lower())


def _validate_http_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("full-text URLs must be public HTTP or HTTPS URLs without embedded credentials")
    hostname = parsed.hostname.lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("full-text URLs must not target local hosts")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return
    if not address.is_global:
        raise ValueError("full-text URLs must target globally routable hosts")


def _cache_path(cache_dir: Path, url: str) -> Path:
    return cache_dir / f"{hashlib.sha256(url.encode('utf-8')).hexdigest()}.json"


def _load_cached_document(path: Path) -> FullTextDocument | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return FullTextDocument(
            source_url=str(data["source_url"]),
            pages=[ExtractedPage(int(page["page"]), str(page["text"])) for page in data.get("pages", [])],
            content_hash=str(data["content_hash"]),
            complete=bool(data.get("complete")),
            warnings=[str(item) for item in data.get("warnings", [])],
            coverage=dict(data.get("coverage") or {}),
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return None


def _write_cached_document(path: Path, document: FullTextDocument) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "source_url": document.source_url,
                "content_hash": document.content_hash,
                "complete": document.complete,
                "warnings": document.warnings,
                "coverage": document.coverage,
                "pages": [{"page": page.page, "text": page.text} for page in document.pages],
            },
            ensure_ascii=True,
        ),
        encoding="utf-8",
    )


def _content_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
