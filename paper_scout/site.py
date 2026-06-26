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
    return _page(
        "Paper Scout Dashboard",
        f"""
        <header class="site-header">
          <p class="eyebrow">Paper Scout</p>
          <h1>Daily agent-memory papers</h1>
          <p class="subtle">Latest digest: <strong>{escape(latest.date)}</strong></p>
          <nav><a href="latest.html">Latest</a><a href="archive.html">Archive</a><a href="../digests/latest.md">Markdown fallback</a></nav>
        </header>
        {_summary_grid(latest)}
        {_controls(source_buttons)}
        {_warnings(latest.source_warnings)}
        <section class="paper-section" data-section="relevant">
          <h2>Highly relevant</h2>
          {_paper_cards(highly)}
        </section>
        <section class="paper-section" data-section="maybe">
          <h2>Maybe relevant</h2>
          {_paper_cards(maybe)}
        </section>
        <section class="archive-strip">
          <h2>Archive</h2>
          <div class="archive-links">{''.join(f'<a href="../digests/{escape(item.date)}.md">{escape(item.date)}</a>' for item in reversed(archive))}</div>
        </section>
        {FILTER_SCRIPT}
        """,
    )


def _render_archive_page(archive: list[ParsedDigest]) -> str:
    rows = "\n".join(
        f"""
        <li>
          <a href="../digests/{escape(item.date)}.md">{escape(item.date)}</a>
          <span>{len(item.papers)} papers</span>
          <span>{escape(item.summary.get('Candidates fetched', '0'))} fetched</span>
        </li>
        """
        for item in reversed(archive)
    )
    return _page(
        "Paper Scout Archive",
        f"""
        <header class="site-header">
          <p class="eyebrow">Paper Scout</p>
          <h1>Archive</h1>
          <nav><a href="index.html">Dashboard</a><a href="latest.html">Latest</a><a href="../digests/latest.md">Latest Markdown</a></nav>
        </header>
        <main class="archive-list"><ul>{rows}</ul></main>
        """,
    )


def _page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main class="page">
    {body}
  </main>
</body>
</html>
"""


def _summary_grid(digest: ParsedDigest) -> str:
    cells = [
        ("Candidates fetched", digest.summary.get("Candidates fetched", "0")),
        ("New unique papers", digest.summary.get("New unique papers", "0")),
        ("Relevant", digest.summary.get("Relevant", "0")),
        ("Maybe relevant", digest.summary.get("Maybe relevant", "0")),
        ("Source summary", digest.summary.get("Source summary", "none")),
        ("Digest-quality warnings", str(digest.digest_quality_warning_count)),
    ]
    return "<section class=\"summary-grid\">" + "".join(
        f"<div><span>{escape(label)}</span><strong>{escape(value)}</strong></div>" for label, value in cells
    ) + "</section>"


def _controls(sources: list[str]) -> str:
    source_buttons = "".join(f'<button data-source="{escape(source)}">{escape(source)}</button>' for source in sources)
    return f"""
    <section class="controls">
      <input id="paper-search" type="search" placeholder="Search title, abstract, tags">
      <div class="button-row" id="relevance-filters">
        <button data-decision="all" class="active">All</button>
        <button data-decision="relevant">Highly relevant</button>
        <button data-decision="maybe">Maybe relevant</button>
      </div>
      <div class="button-row" id="source-filters">
        <button data-source="all" class="active">All sources</button>
        {source_buttons}
      </div>
    </section>
    """


def _warnings(warnings: list[str]) -> str:
    if not warnings:
        return '<details class="warnings"><summary>Source warnings (0)</summary><p>No source warnings.</p></details>'
    compact = "\n".join(f"<li>{escape(warning)}</li>" for warning in warnings)
    return f'<details class="warnings"><summary>Source warnings ({len(warnings)})</summary><ul>{compact}</ul></details>'


def _paper_cards(papers: list[ParsedPaper]) -> str:
    if not papers:
        return '<p class="empty">No papers in this section.</p>'
    return "\n".join(_paper_card(paper) for paper in papers)


def _paper_card(paper: ParsedPaper) -> str:
    tags = "".join(f'<span class="badge tag">{escape(tag)}</span>' for tag in paper.tags) or '<span class="badge tag">untagged</span>'
    link = f'<a class="paper-link" href="{escape(paper.url)}">Open paper</a>' if paper.url else ""
    search_text = " ".join([paper.title, paper.abstract_summary, " ".join(paper.tags), paper.source, paper.decision]).lower()
    return f"""
    <article class="paper-card" data-source="{escape(paper.source)}" data-decision="{escape(paper.decision)}" data-search="{escape(search_text)}">
      <div class="card-top">
        <span class="badge source">{escape(paper.source)}</span>
        <span class="badge relevance">{escape(paper.decision)} · {escape(paper.score)}</span>
      </div>
      <h3>{escape(paper.title)}</h3>
      <p class="meta">{escape(paper.authors)} · {escape(paper.date)}</p>
      <p><strong>Reason:</strong> {escape(paper.reason)}</p>
      <p>{escape(paper.abstract_summary)}</p>
      <div class="tags">{tags}</div>
      <div class="card-actions">{link}</div>
      <details class="citation"><summary>Copy citation</summary><textarea readonly>{escape(paper.citation)}</textarea></details>
    </article>
    """


STYLE_CSS = """
:root {
  color-scheme: light;
  --bg: #f6f7f9;
  --panel: #ffffff;
  --text: #17202a;
  --muted: #5f6b7a;
  --line: #d8dee8;
  --accent: #216869;
  --accent-2: #7a4f01;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text); font: 16px/1.55 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.page { width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 32px 0 56px; }
.site-header { padding: 24px 0 18px; }
.eyebrow { margin: 0 0 4px; color: var(--accent); font-weight: 700; text-transform: uppercase; letter-spacing: .08em; font-size: 12px; }
h1 { margin: 0; font-size: 42px; line-height: 1.1; letter-spacing: 0; }
h2 { margin: 32px 0 14px; font-size: 24px; }
h3 { margin: 10px 0 8px; font-size: 21px; letter-spacing: 0; }
nav { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 18px; }
nav a, .archive-links a, .paper-link { color: var(--accent); font-weight: 650; text-decoration: none; }
.subtle, .meta, .empty { color: var(--muted); }
.summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin: 18px 0; }
.summary-grid div, .controls, .paper-card, .warnings, .archive-list { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; }
.summary-grid span { display: block; color: var(--muted); font-size: 13px; }
.summary-grid strong { display: block; margin-top: 4px; font-size: 18px; }
.controls { display: grid; gap: 12px; margin: 20px 0; }
input[type="search"] { width: 100%; border: 1px solid var(--line); border-radius: 6px; padding: 11px 12px; font: inherit; }
.button-row { display: flex; gap: 8px; flex-wrap: wrap; }
button { border: 1px solid var(--line); background: #fff; border-radius: 6px; padding: 8px 10px; font: inherit; cursor: pointer; }
button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.warnings { margin: 18px 0; }
.warnings summary { cursor: pointer; font-weight: 700; }
.warnings ul { max-height: 240px; overflow: auto; padding-left: 20px; }
.paper-section { margin-top: 16px; }
.paper-card { margin: 12px 0; box-shadow: 0 1px 2px rgba(20, 32, 45, .04); }
.card-top, .tags, .card-actions { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.badge { display: inline-flex; align-items: center; border-radius: 999px; padding: 3px 9px; font-size: 12px; font-weight: 700; border: 1px solid var(--line); }
.source { background: #e9f3f3; color: var(--accent); }
.relevance { background: #fff4df; color: var(--accent-2); }
.tag { background: #f0f2f5; color: #394452; }
.citation { margin-top: 12px; }
.citation summary { cursor: pointer; color: var(--muted); }
textarea { width: 100%; min-height: 64px; margin-top: 8px; border: 1px solid var(--line); border-radius: 6px; padding: 8px; font: inherit; }
.archive-strip { margin-top: 30px; border-top: 1px solid var(--line); padding-top: 10px; }
.archive-links { display: flex; flex-wrap: wrap; gap: 12px; }
.archive-list ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }
.archive-list li { display: grid; grid-template-columns: 1fr auto auto; gap: 12px; border-bottom: 1px solid var(--line); padding: 10px 0; }
@media (max-width: 640px) {
  h1 { font-size: 32px; }
  .archive-list li { grid-template-columns: 1fr; }
}
"""


FILTER_SCRIPT = """
<script>
(() => {
  const search = document.querySelector('#paper-search');
  const cards = Array.from(document.querySelectorAll('.paper-card'));
  let decision = 'all';
  let source = 'all';
  function update() {
    const query = (search.value || '').toLowerCase();
    for (const card of cards) {
      const matchesQuery = !query || card.dataset.search.includes(query);
      const matchesDecision = decision === 'all' || card.dataset.decision === decision;
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
  bindButtons('#relevance-filters button', 'decision', value => decision = value);
  bindButtons('#source-filters button', 'source', value => source = value);
})();
</script>
"""
