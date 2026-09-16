from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import ipaddress
from io import BytesIO
import json
import logging
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from paper_scout.models import PaperCandidate


LOGGER = logging.getLogger(__name__)
USER_AGENT = "Paper-Scout/1.0 (+https://github.com/vernerisirva/agentmempaper)"


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


def select_assessment_text(
    candidate: PaperCandidate,
    document: FullTextDocument | None,
    max_prompt_characters: int = 60_000,
    max_section_characters: int = 8_000,
) -> SelectedPaperText:
    abstract = " ".join(candidate.abstract.split())
    if document is None or not document.pages:
        content = f"Title: {candidate.title}\n\nAbstract: {abstract}".strip()
        scope = "title_and_abstract" if abstract else "metadata_only"
        return SelectedPaperText(
            text=content[:max_prompt_characters],
            sections=[SelectedSection("Abstract", abstract, None)] if abstract else [],
            scope=scope,
            content_hash=_content_hash(content),
            section_detection_uncertain=False,
            warnings=[] if abstract else ["No abstract or extractable full text was available."],
        )

    logical_xml = "JATS XML: Page labels are logical body-section numbers, not PDF pages." in document.warnings
    detected = ([SelectedSection(page.text.split("\n", 1)[0], page.text.split("\n", 1)[-1], page.page)
                 for page in document.pages] if logical_xml else _detect_sections(document.pages))
    selected: list[SelectedSection] = []
    target_groups = (
        ("abstract", "summary"),
        ("introduction",),
        ("contribution",),
        ("related work", "background"),
        ("method", "methodology", "proposed method", "architecture", "implementation"),
        ("experiment", "experimental setup", "experimental protocol", "evaluation", "results", "ablation"),
        ("limitations", "threats to validity"),
        ("conclusion", "discussion"),
    )
    for aliases in target_groups:
        for match in detected:
            if any(alias in match.heading.lower() for alias in aliases):
                section = SelectedSection(match.heading, match.text[:max_section_characters], match.first_page)
                if section not in selected:
                    selected.append(section)
    # Descriptive numbered headings are real body boundaries even when they do
    # not use the conventional Methods/Results vocabulary. Include them too.
    for match in detected:
        section = SelectedSection(match.heading, match.text[:max_section_characters], match.first_page)
        if section not in selected:
            selected.append(section)
    uncertain = not selected
    if uncertain:
        pages = document.pages
        fallback_pages = [pages[0], pages[len(pages) // 2], pages[-1]]
        seen_pages: set[int] = set()
        for page in fallback_pages:
            if page.page in seen_pages:
                continue
            seen_pages.add(page.page)
            selected.append(SelectedSection(f"Page {page.page} excerpt", page.text[:max_section_characters], page.page))
    prefix = f"Title: {candidate.title}\n\nAbstract: {abstract}\n\n"
    body = "\n\n".join(f"## {section.heading}\n[Page {section.first_page or 'unknown'}]\n{section.text}" for section in selected)
    text = (prefix + body)[:max_prompt_characters]
    covered_chars = sum(len(section.text) for section in selected)
    scope = "full_text" if document.complete and len(prefix + body) <= max_prompt_characters and covered_chars >= min(len(document.text), max_prompt_characters) * 0.65 else "partial_full_text"
    warnings = list(document.warnings)
    if uncertain:
        warnings.append("Section headings could not be detected reliably; beginning, middle, and end passages were selected.")
    return SelectedPaperText(
        text=text,
        sections=selected,
        scope=scope,
        content_hash=document.content_hash,
        section_detection_uncertain=uncertain,
        warnings=warnings,
    )


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
        if index <= max_pages and remaining > 0:
            pages.append(ExtractedPage(index, text[:remaining]))
            remaining -= len(text)
    if not any(p.text.partition("\n")[2].strip() for p in pages):
        raise ValueError("JATS body is empty")
    complete = len(sections) <= max_pages and total <= max_characters
    warnings = ["JATS XML: Page labels are logical body-section numbers, not PDF pages."]
    if not complete:
        warnings.append("JATS extraction was limited by the configured section/character bounds.")
    return FullTextDocument(url, pages, hashlib.sha256(payload).hexdigest(), complete, warnings=warnings)


def _extract_pdf(payload: bytes, url: str, max_pages: int, max_characters: int) -> FullTextDocument:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - dependency presence is checked by workflow/tests.
        raise RuntimeError("pypdf is required for full-text extraction") from exc
    reader = PdfReader(BytesIO(payload))
    pages: list[ExtractedPage] = []
    warnings: list[str] = []
    character_count = 0
    selected_pages = list(reader.pages[: max(1, max_pages)])
    for index, page in enumerate(selected_pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:  # noqa: BLE001 - one malformed page must not abort extraction.
            warnings.append(f"Page {index} could not be extracted: {exc.__class__.__name__}.")
            text = ""
        remaining = max_characters - character_count
        if remaining <= 0:
            break
        text = text[:remaining]
        character_count += len(text)
        pages.append(ExtractedPage(index, text))
    complete = len(reader.pages) <= max_pages and character_count < max_characters
    if len(reader.pages) > max_pages:
        warnings.append(f"Extraction was limited to {max_pages} pages.")
    if character_count >= max_characters:
        warnings.append(f"Extraction was limited to {max_characters} characters.")
    if not any(page.text.strip() for page in pages):
        warnings.append("The PDF contained no extractable text; it may be scanned or malformed.")
        complete = False
    return FullTextDocument(
        source_url=url,
        pages=pages,
        content_hash=hashlib.sha256(payload).hexdigest(),
        complete=complete,
        warnings=warnings,
    )


def _detect_sections(pages: list[ExtractedPage]) -> list[SelectedSection]:
    heading_pattern = re.compile(
        r"(?im)^(?:\d+(?:\.\d+)*\.?\s+)?(abstract|introduction|contributions?|related work|background|method(?:s|ology)?|proposed method|(?:system )?architecture|implementation|experimental setup|experimental protocol|experiments?|evaluation|results(?: and discussion)?|ablation(?: study)?|limitations?|threats to validity|discussion|conclusions?)(?::[^\n]{1,100})?\s*$"
    )
    numbered = re.compile(r"(?m)^\d{1,2}(?:\.\d{1,2})*\.?[ \t]+([A-Z][^\n]{2,110})$")
    sections: list[SelectedSection] = []
    current_heading = None
    for page in pages:
        matches = list(heading_pattern.finditer(page.text))
        # Generic numbered titles terminate a known body section; never infer
        # body evidence merely from an enumerated list inside an abstract.
        body_starts = [m.start() for m in matches if m.group(1).lower() != "abstract"]
        body_start = -1 if current_heading and current_heading.lower() != "abstract" else min(body_starts, default=len(page.text))
        occupied = {m.start() for m in matches}
        matches += [m for m in numbered.finditer(page.text)
                    if m.start() > body_start and m.start() not in occupied
                    and not m.group(1).rstrip().endswith((".", ";", ","))]
        matches.sort(key=lambda m: m.start())
        prefix = page.text[:matches[0].start()] if matches else page.text
        if current_heading and prefix.strip():
            sections.append(SelectedSection(current_heading, prefix.strip(), page.page))
        for index, match in enumerate(matches):
            current_heading = match.group(1).title()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(page.text)
            text = page.text[match.end() : end].strip()
            if text:
                sections.append(SelectedSection(match.group(1).title(), text, page.page))
    return sections


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
                "pages": [{"page": page.page, "text": page.text} for page in document.pages],
            },
            ensure_ascii=True,
        ),
        encoding="utf-8",
    )


def _content_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
