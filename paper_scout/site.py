from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
import json
from pathlib import Path
import re


@dataclass(frozen=True)
class SiteBuildResult:
    built: bool
    message: str
    latest_date: str | None = None
    output_dir: Path | None = None


@dataclass(frozen=True)
class ParsedPaper:
    title: str
    url: str | None
    authors: str
    date: str
    source: str
    decision: str
    score: str
    reason: str
    tags: list[str]
    abstract_summary: str
    section: str

    @property
    def citation(self) -> str:
        parts = [self.title]
        if self.authors and self.authors != "Unknown authors":
            parts.append(self.authors)
        if self.date and self.date != "unknown":
            parts.append(self.date)
        if self.url:
            parts.append(self.url)
        return ". ".join(parts)


@dataclass(frozen=True)
class ParsedDigest:
    date: str
    summary: dict[str, str] = field(default_factory=dict)
    source_warnings: list[str] = field(default_factory=list)
    papers: list[ParsedPaper] = field(default_factory=list)
    digest_quality_warning_count: int = 0


def build_site(
    digest_dir: Path | str = Path("digests"),
    report_dir: Path | str = Path("reports/paper_scout"),
    docs_dir: Path | str = Path("docs"),
) -> SiteBuildResult:
    digest_path = _latest_digest_path(Path(digest_dir))
    if digest_path is None:
        return SiteBuildResult(False, f"No daily digest files found in {digest_dir}. Run `python3 -m paper_scout run` first.")

    digest_root = Path(digest_dir)
    report_root = Path(report_dir)
    docs_root = Path(docs_dir)
    archive_digests = [_parse_digest(path, report_root) for path in _daily_digest_paths(digest_root)]
    latest = archive_digests[-1]

    docs_root.mkdir(parents=True, exist_ok=True)
    (docs_root / "data").mkdir(parents=True, exist_ok=True)
    (docs_root / "style.css").write_text(STYLE_CSS, encoding="utf-8")
    (docs_root / "latest.html").write_text(_render_latest_page(latest, archive_digests), encoding="utf-8")
    (docs_root / "index.html").write_text(_render_latest_page(latest, archive_digests), encoding="utf-8")
    (docs_root / "archive.html").write_text(_render_archive_page(archive_digests), encoding="utf-8")
    (docs_root / "data" / "latest.json").write_text(json.dumps(_digest_to_json(latest), indent=2, sort_keys=True), encoding="utf-8")
    (docs_root / "data" / "papers.json").write_text(json.dumps([_digest_to_json(digest) for digest in archive_digests], indent=2, sort_keys=True), encoding="utf-8")
    _write_latest_markdown(digest_root, latest.date, digest_path)

    return SiteBuildResult(True, f"Built Paper Scout dashboard for {latest.date} in {docs_root}", latest.date, docs_root)


def _latest_digest_path(digest_dir: Path) -> Path | None:
    paths = _daily_digest_paths(digest_dir)
    return paths[-1] if paths else None


def _daily_digest_paths(digest_dir: Path) -> list[Path]:
    if not digest_dir.exists():
        return []
    return sorted(path for path in digest_dir.glob("*.md") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", path.stem))


def _parse_digest(path: Path, report_dir: Path) -> ParsedDigest:
    lines = path.read_text(encoding="utf-8").splitlines()
    date = _date_from_title(lines[0] if lines else path.stem) or path.stem
    summary: dict[str, str] = {}
    warnings: list[str] = []
    papers: list[ParsedPaper] = []
    current_section: str | None = None
    current_paper: dict[str, object] | None = None

    for line in lines:
        if line.startswith("## "):
            if current_paper is not None:
                papers.append(_paper_from_dict(current_paper))
                current_paper = None
            current_section = line[3:].strip()
            continue
        if current_section == "Run Summary" and line.startswith("- **"):
            key, value = _parse_bold_bullet(line)
            if key:
                summary[key] = value
            continue
        if current_section == "Source Warnings" and line.startswith("- "):
            warnings.append(_redact_secrets(line[2:].strip()))
            continue
        if current_section in {"Highly Relevant", "Maybe Relevant"}:
            if line.startswith("### "):
                if current_paper is not None:
                    papers.append(_paper_from_dict(current_paper))
                title, url = _parse_heading_link(line[4:].strip())
                current_paper = {"title": _redact_secrets(title), "url": _redact_secrets(url) if url else url, "section": current_section}
                continue
            if current_paper is not None and line.startswith("- **"):
                key, value = _parse_bold_bullet(line)
                current_paper[key] = _redact_secrets(value)

    if current_paper is not None:
        papers.append(_paper_from_dict(current_paper))

    return ParsedDigest(
        date=date,
        summary=summary,
        source_warnings=warnings,
        papers=papers,
        digest_quality_warning_count=_digest_quality_count(report_dir / f"digest-quality-{date}.md"),
    )


def _date_from_title(title: str) -> str | None:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", title)
    return match.group(1) if match else None


def _parse_bold_bullet(line: str) -> tuple[str | None, str]:
    match = re.match(r"- \*\*(.+?):\*\* ?(.*)", line)
    if not match:
        return None, ""
    return match.group(1), match.group(2).strip()


def _parse_heading_link(text: str) -> tuple[str, str | None]:
    match = re.match(r"\[(.+?)\]\((.+?)\)", text)
    if match:
        return match.group(1), match.group(2)
    return text, None


def _paper_from_dict(data: dict[str, object]) -> ParsedPaper:
    relevance = str(data.get("Relevance", "unknown (0/100)"))
    decision_match = re.match(r"([a-zA-Z_-]+)\s+\((.+?)\)", relevance)
    decision = decision_match.group(1) if decision_match else relevance
    score = decision_match.group(2) if decision_match else "unknown"
    tags = [tag.strip() for tag in str(data.get("Tags", "")).split(",") if tag.strip() and tag.strip() != "untagged"]
    return ParsedPaper(
        title=str(data.get("title", "")),
        url=data.get("url") if isinstance(data.get("url"), str) else None,
        authors=str(data.get("Authors", "Unknown authors")),
        date=str(data.get("Date", "unknown")),
        source=str(data.get("Source", "unknown")),
        decision=decision,
        score=score,
        reason=str(data.get("Reason", "")),
        tags=tags,
        abstract_summary=str(data.get("Abstract summary", "")),
        section=str(data.get("section", "Maybe Relevant")),
    )


def _digest_quality_count(path: Path) -> int:
    if not path.exists():
        return 0
    match = re.search(r"Likely false positives flagged:\s*(\d+)", path.read_text(encoding="utf-8"))
    return int(match.group(1)) if match else 0


def _redact_secrets(text: str) -> str:
    patterns = [
        r"sk-[A-Za-z0-9_-]{20,}",
        r"sk-proj-[A-Za-z0-9_-]{20,}",
        r"gho_[A-Za-z0-9_]{20,}",
        r"ghp_[A-Za-z0-9_]{20,}",
        r"github_pat_[A-Za-z0-9_]{20,}",
    ]
    redacted = text
    for pattern in patterns:
        redacted = re.sub(pattern, "[REDACTED]", redacted)
    return redacted


def _write_latest_markdown(digest_dir: Path, latest_date: str, latest_path: Path) -> None:
    body = latest_path.read_text(encoding="utf-8")
    latest = digest_dir / "latest.md"
    latest.write_text(
        f"# Latest Paper Scout Digest\n\nLatest daily digest: [{latest_date}]({latest_date}.md).\n\n{body}",
        encoding="utf-8",
    )


def _digest_to_json(digest: ParsedDigest) -> dict[str, object]:
    return {
        "date": digest.date,
        "summary": digest.summary,
        "source_warnings": digest.source_warnings,
        "digest_quality_warning_count": digest.digest_quality_warning_count,
        "papers": [
            {
                "title": paper.title,
                "url": paper.url,
                "authors": paper.authors,
                "date": paper.date,
                "source": paper.source,
                "decision": paper.decision,
                "score": paper.score,
                "reason": paper.reason,
                "tags": paper.tags,
                "abstract_summary": paper.abstract_summary,
                "section": paper.section,
                "citation": paper.citation,
            }
            for paper in digest.papers
        ],
    }


def _render_latest_page(latest: ParsedDigest, archive: list[ParsedDigest]) -> str:
    highly = [paper for paper in latest.papers if paper.section == "Highly Relevant"]
    maybe = [paper for paper in latest.papers if paper.section == "Maybe Relevant"]
    source_buttons = sorted({paper.source for paper in latest.papers if paper.source})
    latest_markdown_url = f"https://github.com/vernerisirva/agentmempaper/blob/main/digests/{escape(latest.date)}.md"
    return _page(
        "Paper Scout",
        f"""
        <header class="briefing-hero">
          <nav class="top-nav" aria-label="Primary">
            <a class="brand" href="index.html">Paper Scout</a>
            <span class="nav-links">
              <a href="archive.html">Archive</a>
              <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/latest.md">Markdown digest</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub repo</a>
            </span>
          </nav>
          <div class="hero-grid">
            <div>
              <p class="eyebrow">Daily agent-memory research briefing</p>
              <h1>Paper Scout</h1>
              <p class="hero-copy">New papers on agentic memory, deep research agents, and memory mechanisms.</p>
              <div class="hero-actions">
                <a class="button primary" href="#highly-relevant">Read latest papers</a>
                <a class="button secondary" href="archive.html">Browse archive</a>
              </div>
            </div>
            <aside class="digest-note" aria-label="Latest digest metadata">
              <span>Latest digest</span>
              <strong>{escape(latest.date)}</strong>
              <a href="{latest_markdown_url}">Open Markdown digest</a>
            </aside>
          </div>
        </header>
        {_summary_strip(latest)}
        {_controls(source_buttons)}
        <section class="paper-section primary-section" id="highly-relevant" data-section="relevant">
          <div class="section-heading">
            <p class="section-kicker">Start here</p>
            <h2>Highly relevant</h2>
            <p>Papers most directly connected to long-running agent memory, deep research agents, and memory mechanisms.</p>
          </div>
          {_paper_cards(highly, "primary")}
        </section>
        <section class="paper-section secondary-section" data-section="maybe">
          <div class="section-heading">
            <p class="section-kicker">Worth a scan</p>
            <h2>Maybe relevant</h2>
            <p>Adjacent work that may be useful after the strongest candidates.</p>
          </div>
          {_paper_cards(maybe, "compact")}
        </section>
        {_warnings(latest.source_warnings)}
        <section class="archive-strip" aria-labelledby="recent-archive-heading">
          <div>
            <p class="section-kicker">Earlier briefings</p>
            <h2 id="recent-archive-heading">Archive</h2>
          </div>
          <div class="archive-links">{''.join(f'<a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/{escape(item.date)}.md">{escape(item.date)}</a>' for item in reversed(archive[:8]))}</div>
        </section>
        {FILTER_SCRIPT}
        """,
    )


def _render_archive_page(archive: list[ParsedDigest]) -> str:
    rows = "\n".join(
        f"""
        <article class="archive-entry">
          <div>
            <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/{escape(item.date)}.md">{escape(item.date)}</a>
            <p>{escape(item.summary.get('Candidates fetched', '0'))} candidates fetched · {escape(item.summary.get('New unique papers', '0'))} new unique papers</p>
          </div>
          <dl>
            <div><dt>Highly relevant</dt><dd>{_section_count(item, 'Highly Relevant')}</dd></div>
            <div><dt>Maybe relevant</dt><dd>{_section_count(item, 'Maybe Relevant')}</dd></div>
            <div><dt>Warnings</dt><dd>{len(item.source_warnings)}</dd></div>
          </dl>
        </article>
        """
        for item in reversed(archive)
    )
    return _page(
        "Paper Scout Archive",
        f"""
        <header class="archive-hero">
          <nav class="top-nav" aria-label="Primary">
            <a class="brand" href="index.html">Paper Scout</a>
            <span class="nav-links">
              <a href="latest.html">Latest</a>
              <a href="https://github.com/vernerisirva/agentmempaper/blob/main/digests/latest.md">Latest Markdown</a>
              <a href="https://github.com/vernerisirva/agentmempaper">GitHub repo</a>
            </span>
          </nav>
          <p class="eyebrow">Daily agent-memory research briefing</p>
          <h1>Archive</h1>
          <p class="hero-copy">Past Paper Scout briefings with quick counts for relevant, maybe-relevant, and diagnostic items.</p>
        </header>
        <section class="archive-list" aria-label="Digest archive">{rows}</section>
        """,
    )


def _page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="Daily Paper Scout briefing for agentic memory, deep research agents, and memory mechanisms.">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <main class="page" id="main-content">
    {body}
  </main>
</body>
</html>
"""


def _summary_strip(digest: ParsedDigest) -> str:
    cells = [
        ("Candidates fetched", digest.summary.get("Candidates fetched", "0")),
        ("New unique papers", digest.summary.get("New unique papers", "0")),
        ("Highly relevant", digest.summary.get("Relevant", "0")),
        ("Maybe relevant", digest.summary.get("Maybe relevant", "0")),
        ("Digest-quality warnings", str(digest.digest_quality_warning_count)),
    ]
    metric_cells = "".join(f"<div><span>{escape(label)}</span><strong>{escape(value)}</strong></div>" for label, value in cells)
    return f"""
    <section class="summary-strip" aria-label="Run summary metrics">
      {metric_cells}
      <div class="source-summary"><span>Source summary</span><strong>{escape(digest.summary.get("Source summary", "none"))}</strong></div>
    </section>
    """


def _controls(sources: list[str]) -> str:
    source_buttons = "".join(f'<button data-source="{escape(source)}">{escape(source)}</button>' for source in sources)
    return f"""
    <section class="reading-controls" aria-label="Reading controls">
      <label class="search-field" for="paper-search">
        <span>Search papers</span>
        <input id="paper-search" type="search" placeholder="Search title, abstract, tags">
      </label>
      <div class="control-group">
        <span>Relevance</span>
        <div class="segmented" id="relevance-filters">
          <button data-decision="all" class="active">All</button>
          <button data-decision="relevant">Highly relevant</button>
          <button data-decision="maybe">Maybe relevant</button>
        </div>
      </div>
      <label class="high-toggle">
        <input id="high-only" type="checkbox">
        <span>Show only highly relevant</span>
      </label>
      <div class="control-group sources">
        <span>Source</span>
        <div class="source-buttons" id="source-filters">
          <button data-source="all" class="active">All sources</button>
          {source_buttons}
        </div>
      </div>
    </section>
    """


def _warnings(warnings: list[str]) -> str:
    if not warnings:
        return '<details class="source-diagnostics"><summary>Source diagnostics <span>0 warnings</span></summary><p>No source warnings.</p></details>'
    compact = "\n".join(f"<li>{escape(warning)}</li>" for warning in warnings)
    return f'<details class="source-diagnostics"><summary>Source diagnostics <span>{len(warnings)} warnings</span></summary><ul>{compact}</ul></details>'


def _paper_cards(papers: list[ParsedPaper], density: str) -> str:
    if not papers:
        return '<p class="empty">No papers in this section.</p>'
    return "\n".join(_paper_card(paper, density) for paper in papers)


def _paper_card(paper: ParsedPaper, density: str) -> str:
    tags = "".join(f'<span class="badge tag">{escape(tag)}</span>' for tag in paper.tags) or '<span class="badge tag">untagged</span>'
    link = f'<a class="paper-link" href="{escape(paper.url)}">Open paper</a>' if paper.url else '<span class="paper-link disabled">No link available</span>'
    search_text = " ".join([paper.title, paper.abstract_summary, " ".join(paper.tags), paper.source, paper.decision]).lower()
    return f"""
    <article class="paper-card {escape(density)}" data-source="{escape(paper.source)}" data-decision="{escape(paper.decision)}" data-search="{escape(search_text)}">
      <div class="paper-main">
        <div class="paper-kicker">
          <span class="badge source">{escape(paper.source)}</span>
          <span class="badge relevance">{escape(paper.decision)} · {escape(paper.score)}</span>
        </div>
        <h3>{escape(paper.title)}</h3>
        <p class="meta">{escape(paper.authors)} · {escape(paper.date)}</p>
        <p class="reason">{escape(paper.reason)}</p>
        <p class="abstract-summary">{escape(paper.abstract_summary)}</p>
        <div class="tags">{tags}</div>
      </div>
      <div class="paper-side">
        {link}
        <details class="citation"><summary>Copy citation</summary><textarea readonly>{escape(paper.citation)}</textarea></details>
      </div>
    </article>
    """


def _section_count(digest: ParsedDigest, section: str) -> int:
    return sum(1 for paper in digest.papers if paper.section == section)


STYLE_CSS = """
:root {
  color-scheme: light;
  --bg: #f4f1ea;
  --paper: #fffdf8;
  --paper-soft: #fbf7ef;
  --text: #191816;
  --muted: #676059;
  --faint: #8b8176;
  --line: #ddd4c8;
  --line-strong: #c8b9a8;
  --accent: #27615d;
  --accent-dark: #174744;
  --amber: #8a5a17;
  --shadow: rgba(64, 48, 32, .09);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background:
    radial-gradient(circle at top left, rgba(39, 97, 93, .09), transparent 28rem),
    linear-gradient(180deg, #f8f5ee 0%, var(--bg) 34rem);
  color: var(--text);
  font: 16px/1.62 ui-serif, Georgia, Cambria, "Times New Roman", serif;
  text-rendering: optimizeLegibility;
}
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: .16;
  background-image: radial-gradient(rgba(25, 24, 22, .16) .55px, transparent .55px);
  background-size: 8px 8px;
}
a { color: var(--accent-dark); text-decoration-thickness: .08em; text-underline-offset: .18em; }
a:hover { color: var(--accent); }
button, input, textarea { font: inherit; }
button, a, input, summary, textarea { transition: background-color .2s ease, border-color .2s ease, color .2s ease, box-shadow .2s ease, transform .2s ease; }
button:focus-visible, a:focus-visible, input:focus-visible, summary:focus-visible, textarea:focus-visible {
  outline: 3px solid rgba(39, 97, 93, .28);
  outline-offset: 3px;
}
.skip-link {
  position: absolute;
  left: 1rem;
  top: .75rem;
  z-index: 2;
  transform: translateY(-160%);
  background: var(--text);
  color: var(--paper);
  padding: .55rem .8rem;
  border-radius: .45rem;
}
.skip-link:focus { transform: translateY(0); }
.page { width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 30px 0 64px; }
.top-nav {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
  padding-bottom: 2.25rem;
}
.brand {
  color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-weight: 760;
  text-decoration: none;
}
.nav-links { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: flex-end; }
.nav-links a {
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .93rem;
  font-weight: 600;
  text-decoration: none;
}
.nav-links a:hover { color: var(--accent-dark); }
.briefing-hero, .archive-hero { padding: 1rem 0 2rem; }
.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(220px, 310px);
  gap: clamp(1.5rem, 4vw, 4rem);
  align-items: end;
}
.eyebrow, .section-kicker, .summary-strip span, .control-group > span, .search-field span {
  margin: 0;
  color: var(--accent-dark);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .72rem;
  font-weight: 760;
  letter-spacing: .13em;
  text-transform: uppercase;
}
h1, h2, h3 { margin: 0; text-wrap: balance; }
h1 {
  max-width: 11ch;
  font-size: clamp(4rem, 14vw, 9.5rem);
  line-height: .82;
  letter-spacing: -.055em;
}
.archive-hero h1 { max-width: 12ch; font-size: clamp(3.4rem, 11vw, 7rem); }
h2 { font-size: clamp(1.95rem, 4vw, 3.2rem); line-height: .95; letter-spacing: -.035em; }
h3 { font-size: clamp(1.35rem, 2vw, 1.95rem); line-height: 1.12; letter-spacing: -.018em; }
.hero-copy {
  max-width: 34rem;
  margin: 1.35rem 0 0;
  color: var(--muted);
  font-size: clamp(1.1rem, 2vw, 1.35rem);
  line-height: 1.5;
  text-wrap: pretty;
}
.hero-actions { display: flex; flex-wrap: wrap; gap: .7rem; margin-top: 1.55rem; }
.button, .paper-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.65rem;
  border-radius: .55rem;
  padding: .72rem 1rem;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .94rem;
  font-weight: 720;
  text-decoration: none;
}
.button.primary, .paper-link {
  background: var(--accent-dark);
  color: #fffdf7;
  box-shadow: 0 12px 28px rgba(23, 71, 68, .18);
}
.button.secondary {
  background: rgba(255, 253, 248, .72);
  border: 1px solid var(--line);
  color: var(--accent-dark);
}
.button:hover, .paper-link:hover { transform: translateY(-1px); }
.button:active, .paper-link:active, button:active { transform: translateY(1px); }
.digest-note {
  background: rgba(255, 253, 248, .76);
  border: 1px solid rgba(200, 185, 168, .76);
  border-radius: .9rem;
  box-shadow: 0 22px 60px var(--shadow);
  padding: 1.15rem;
}
.digest-note span, .digest-note a {
  display: block;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.digest-note span { color: var(--faint); font-size: .82rem; font-weight: 650; }
.digest-note strong {
  display: block;
  margin: .2rem 0 .75rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 1.7rem;
  font-variant-numeric: tabular-nums;
}
.summary-strip {
  display: grid;
  grid-template-columns: repeat(5, minmax(7rem, 1fr));
  gap: 0;
  margin: 1.5rem 0 1.25rem;
  background: rgba(255, 253, 248, .82);
  border: 1px solid var(--line);
  border-radius: .85rem;
  overflow: hidden;
  box-shadow: 0 18px 42px rgba(64, 48, 32, .06);
}
.summary-strip div { padding: .95rem 1rem; border-left: 1px solid var(--line); }
.summary-strip div:first-child { border-left: 0; }
.summary-strip strong {
  display: block;
  margin-top: .15rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 1.15rem;
  font-variant-numeric: tabular-nums;
}
.summary-strip .source-summary {
  grid-column: 1 / -1;
  border-left: 0;
  border-top: 1px solid var(--line);
}
.summary-strip .source-summary strong {
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .98rem;
  font-weight: 650;
}
.reading-controls {
  display: grid;
  grid-template-columns: minmax(18rem, 1.4fr) minmax(16rem, 1fr) auto;
  gap: .9rem;
  align-items: end;
  margin: 1.4rem 0 2.6rem;
  padding: .95rem;
  background: rgba(248, 245, 238, .8);
  border: 1px solid var(--line);
  border-radius: .85rem;
}
.search-field, .control-group { display: grid; gap: .45rem; }
input[type="search"] {
  width: 100%;
  min-height: 2.75rem;
  border: 1px solid var(--line-strong);
  border-radius: .55rem;
  background: var(--paper);
  color: var(--text);
  padding: .7rem .85rem;
}
input[type="search"]::placeholder { color: var(--faint); }
.segmented, .source-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: .35rem;
}
button {
  border: 1px solid var(--line);
  background: rgba(255, 253, 248, .72);
  color: var(--muted);
  border-radius: .48rem;
  padding: .58rem .72rem;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .88rem;
  font-weight: 650;
  cursor: pointer;
}
button:hover { border-color: var(--line-strong); color: var(--text); background: var(--paper); }
button.active { background: var(--accent-dark); border-color: var(--accent-dark); color: #fffdf7; }
.high-toggle {
  display: inline-flex;
  gap: .55rem;
  align-items: center;
  min-height: 2.75rem;
  padding: .58rem .72rem;
  border: 1px solid var(--line);
  border-radius: .55rem;
  background: rgba(255, 253, 248, .66);
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .88rem;
  font-weight: 650;
}
.high-toggle input { accent-color: var(--accent-dark); }
.sources { grid-column: 1 / -1; }
.paper-section { margin-top: 2.5rem; }
.section-heading {
  max-width: 44rem;
  margin-bottom: 1.05rem;
}
.section-heading p:not(.section-kicker) {
  margin: .7rem 0 0;
  color: var(--muted);
  font-size: 1.03rem;
}
.paper-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(11rem, 14rem);
  gap: clamp(1rem, 3vw, 2rem);
  margin: 1rem 0;
  padding: clamp(1.1rem, 3vw, 1.65rem);
  background: var(--paper);
  border-top: 1px solid var(--line-strong);
  border-radius: .75rem;
  box-shadow: 0 18px 46px rgba(64, 48, 32, .055);
}
.paper-card.primary { border-top: 4px solid var(--accent-dark); }
.paper-card.compact {
  background: rgba(255, 253, 248, .68);
  box-shadow: none;
}
.paper-kicker, .tags { display: flex; gap: .45rem; flex-wrap: wrap; align-items: center; }
.paper-card h3 { margin-top: .7rem; }
.meta, .empty {
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.meta { margin: .55rem 0 0; font-size: .95rem; }
.reason {
  margin: 1rem 0 0;
  padding: .85rem .95rem;
  border-left: 3px solid rgba(39, 97, 93, .45);
  background: #f3f8f6;
  color: #244c49;
  border-radius: .35rem .55rem .55rem .35rem;
  font-weight: 600;
}
.abstract-summary {
  max-width: 67ch;
  margin: .95rem 0 0;
  color: #3d3934;
  text-wrap: pretty;
}
.badge {
  display: inline-flex;
  align-items: center;
  border-radius: .35rem;
  padding: .2rem .5rem;
  border: 1px solid var(--line);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .76rem;
  font-weight: 760;
}
.source { background: #e7f0ee; color: var(--accent-dark); border-color: #c9dfdc; }
.relevance { background: #fff1d8; color: var(--amber); border-color: #ecd6ad; }
.tag { background: #f2eee7; color: #574f47; }
.tags { margin-top: .95rem; }
.paper-side {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: .75rem;
}
.paper-link.disabled {
  background: #eee7dc;
  color: var(--faint);
  box-shadow: none;
}
.citation summary {
  cursor: pointer;
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .88rem;
  font-weight: 650;
}
textarea {
  width: 100%;
  min-height: 6rem;
  margin-top: .55rem;
  border: 1px solid var(--line);
  border-radius: .55rem;
  background: var(--paper-soft);
  color: var(--text);
  padding: .7rem;
  resize: vertical;
}
.source-diagnostics {
  margin: 2.6rem 0 0;
  padding: .9rem 1rem;
  background: rgba(255, 253, 248, .58);
  border: 1px solid var(--line);
  border-radius: .65rem;
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.source-diagnostics summary {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  font-weight: 720;
  color: var(--text);
}
.source-diagnostics summary span {
  color: var(--faint);
  font-size: .9rem;
  font-weight: 650;
}
.source-diagnostics ul {
  max-height: 13rem;
  overflow: auto;
  margin: .85rem 0 0;
  padding-left: 1.1rem;
}
.archive-strip {
  display: grid;
  grid-template-columns: minmax(10rem, 16rem) 1fr;
  gap: 1.5rem;
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--line);
}
.archive-strip h2 { font-size: 2rem; }
.archive-links {
  display: flex;
  flex-wrap: wrap;
  gap: .55rem;
  align-content: start;
}
.archive-links a {
  padding: .45rem .6rem;
  border: 1px solid var(--line);
  border-radius: .45rem;
  background: rgba(255, 253, 248, .6);
  color: var(--accent-dark);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: .88rem;
  text-decoration: none;
}
.archive-list {
  display: grid;
  gap: .85rem;
  margin-top: 1.6rem;
}
.archive-entry {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(18rem, 28rem);
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 253, 248, .72);
  border: 1px solid var(--line);
  border-radius: .75rem;
}
.archive-entry a {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 1.1rem;
  font-weight: 760;
  text-decoration: none;
}
.archive-entry p {
  margin: .35rem 0 0;
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.archive-entry dl {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: .55rem;
  margin: 0;
}
.archive-entry dl div {
  padding: .65rem;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: .5rem;
}
.archive-entry dt {
  color: var(--faint);
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: .75rem;
  font-weight: 720;
}
.archive-entry dd {
  margin: .15rem 0 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 1.2rem;
  font-weight: 760;
}
[hidden] { display: none !important; }
@media (max-width: 640px) {
  .page { width: min(100% - 22px, 1180px); padding-top: 18px; }
  .top-nav, .hero-grid, .paper-card, .archive-strip, .archive-entry { grid-template-columns: 1fr; }
  .top-nav { align-items: flex-start; }
  .nav-links { justify-content: flex-start; }
  .summary-strip { grid-template-columns: repeat(2, 1fr); }
  .summary-strip div:nth-child(odd) { border-left: 0; }
  .reading-controls { grid-template-columns: 1fr; }
  .archive-entry dl { grid-template-columns: 1fr; }
  h1 { font-size: clamp(3.4rem, 24vw, 5.3rem); }
}
@media print {
  body { background: #fff; }
  body::before, .reading-controls, .hero-actions, .source-diagnostics, .archive-strip, .top-nav { display: none; }
  .page { width: 100%; padding: 0; }
  .paper-card { break-inside: avoid; box-shadow: none; }
}
"""


FILTER_SCRIPT = """
<script>
(() => {
  const search = document.querySelector('#paper-search');
  const highOnly = document.querySelector('#high-only');
  const cards = Array.from(document.querySelectorAll('.paper-card'));
  let decision = 'all';
  let source = 'all';
  function update() {
    const query = (search.value || '').toLowerCase();
    for (const card of cards) {
      const matchesQuery = !query || card.dataset.search.includes(query);
      const effectiveDecision = highOnly && highOnly.checked ? 'relevant' : decision;
      const matchesDecision = effectiveDecision === 'all' || card.dataset.decision === effectiveDecision;
      const matchesSource = source === 'all' || card.dataset.source === source;
      card.hidden = !(matchesQuery && matchesDecision && matchesSource);
    }
  }
  function bindButtons(selector, attr, setter) {
    document.querySelectorAll(selector).forEach(button => {
      button.addEventListener('click', () => {
        button.parentElement.querySelectorAll('button').forEach(item => item.classList.remove('active'));
        button.classList.add('active');
        setter(button.dataset[attr]);
        update();
      });
    });
  }
  if (search) search.addEventListener('input', update);
  if (highOnly) highOnly.addEventListener('change', update);
  bindButtons('#relevance-filters button', 'decision', value => decision = value);
  bindButtons('#source-filters button', 'source', value => source = value);
})();
</script>
"""
