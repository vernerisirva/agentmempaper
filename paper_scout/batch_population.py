"""One committed, deterministic path from frozen state to a reproducible eligible population.

Batch 4 committed to an eligible population that could not afterwards be rebuilt: the
construction lived in an uncommitted analysis script and the commitment stored only a
digest, so neither the count nor the membership could be audited. Everything here is
committed, offline and ordered, and the manifest stores the identities themselves beside
their digest, so a later run rebuilds the same population and compares it element by
element rather than trusting a hash.

Two stages are deliberately separate. Building the eligible population is pure and
offline: it reads committed configuration, the track databases and the digest archive,
and nothing else. Execution eligibility — whether a manuscript can actually be acquired
and passes the coverage gate — consumes the frozen ordered list afterwards and is
recorded as an outcome, so a network result can never silently change the population
a batch committed to.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import json
from pathlib import Path
import sqlite3

from paper_scout.config import ScoutConfig, load_config, validate_track
from paper_scout.deduplication import (
    normalize_arxiv_id, normalize_doi, normalize_openalex_id, normalize_text,
)
from paper_scout.evidence_context import digest
from paper_scout.promotion_protocol import canonical_json
from paper_scout.site import (
    _apply_curation, _apply_quality_presentation, _daily_digest_paths, _infer_arxiv_id_from_text,
    _load_curation, _load_library_papers, _mark_new_papers, _merge_dashboard_duplicates,
    _parse_digest, _refresh_rule_classifications, _site_build_time, _sort_latest_relevant,
)

POPULATION_VERSION = "batch-population-v1"
MANIFEST_VERSION = "batch-population-manifest-v1"
TRACKS = ("agent_memory", "deep_research", "engram")
# A short normalized title is not a usable identity, so the dashboard's existing merge
# policy applies here unchanged: only titles longer than this take part in matching.
# Nothing fuzzy is added — two titles match only when their normalizations are equal.
MIN_TITLE_IDENTITY_LENGTH = 12
# The frozen predicate. Relevance is read from the ranking domain, which is the same
# domain the selection order comes from, so membership and order cannot disagree.
ELIGIBLE_RELEVANCE = "relevant"
IDENTITY_POLICY = {
    "version": "batch-identity-v1",
    "namespaces": ["canonical", "doi", "arxiv", "openalex", "semantic_scholar", "title"],
    "rules": [
        "canonical: the stored canonical key, verbatim",
        "doi: lowercased, with a doi.org/doi: prefix removed",
        "arxiv: version suffix and an abs/pdf URL or .pdf extension removed",
        "openalex: an openalex.org URL prefix removed",
        "semantic_scholar: the stored identifier, stripped",
        "arxiv (derived): an arXiv id parsed out of the url, doi or stored source record",
        f"title: lowercased alphanumeric words, only when longer than {MIN_TITLE_IDENTITY_LENGTH}",
    ],
    "matching": "exact equality of namespaced identity strings; no fuzzy or substring matching",
}
EXCLUSION_SOURCES = [
    "prior_assessment: a persisted quality assessment row in any track database",
    "suppressed: an active quality suppression, or a curation suppress_for_quality directive",
    "frozen_roster: a canonical id listed in a supplied frozen roster manifest",
]


@dataclass(frozen=True)
class Candidate:
    """One ranked paper and every identity it is matched by."""

    canonical_id: str
    track: str
    rank: int
    title: str
    identities: tuple[str, ...]

    def to_dict(self) -> dict:
        return {"rank": self.rank, "canonical_id": self.canonical_id, "title": self.title,
                "identities": list(self.identities)}


@dataclass(frozen=True)
class Exclusion:
    """One ranked paper removed from the population, and exactly why."""

    canonical_id: str
    track: str
    rank: int
    title: str
    reason: str
    matched_identity: str | None
    source: str | None

    def to_dict(self) -> dict:
        return {"rank": self.rank, "canonical_id": self.canonical_id, "title": self.title,
                "reason": self.reason, "matched_identity": self.matched_identity,
                "source": self.source}


@dataclass(frozen=True)
class TrackPopulation:
    track: str
    eligible: tuple[Candidate, ...]
    excluded: tuple[Exclusion, ...]
    ranked_count: int
    latest_digest_date: str

    @property
    def ordered_canonical_ids(self) -> tuple[str, ...]:
        return tuple(candidate.canonical_id for candidate in self.eligible)

    @property
    def population_sha256(self) -> str:
        """SHA-256 over the newline-joined canonical ids in selection order.

        Order is part of the commitment: the same set in a different order is a
        different population, because selection takes a prefix of it.
        """
        return digest("\n".join(self.ordered_canonical_ids))

    def to_dict(self) -> dict:
        return {"ranked_count": self.ranked_count,
                "latest_digest_date": self.latest_digest_date,
                "eligible_count": len(self.eligible),
                "excluded_count": len(self.excluded),
                "population_sha256": self.population_sha256,
                "ordered_canonical_ids": list(self.ordered_canonical_ids),
                "eligible": [c.to_dict() for c in self.eligible],
                "excluded": [e.to_dict() for e in self.excluded]}


@dataclass(frozen=True)
class Population:
    tracks: tuple[TrackPopulation, ...]
    sources: dict = field(default_factory=dict)

    def track(self, track_id: str) -> TrackPopulation:
        return next(t for t in self.tracks if t.track == track_id)


def identities(canonical_id: str, *, title: str = "", doi: str | None = None,
               arxiv_id: str | None = None, openalex_id: str | None = None,
               semantic_scholar_id: str | None = None, url: str | None = None,
               raw: str = "") -> tuple[str, ...]:
    """Every namespaced identity one paper is matched by, sorted and deduplicated.

    Namespacing is what keeps the identity space safe: a DOI can only ever match a DOI
    and a title can only ever match a title, so a shared numeric string in two different
    fields is not a match. A title participates only when its normalization is long
    enough to be distinctive, which is the repository's existing merge policy.
    """
    found = {"canonical:" + canonical_id.strip()}
    prefixes = {"doi:": normalize_doi, "arxiv:": normalize_arxiv_id,
                "openalex:": normalize_openalex_id}
    for prefix, normalize in prefixes.items():
        if canonical_id.startswith(prefix):
            value = normalize(canonical_id[len(prefix):])
            if value:
                found.add(prefix + value)
    if canonical_id.startswith("semantic_scholar:"):
        found.add("semantic_scholar:" + canonical_id[len("semantic_scholar:"):].strip())
    for prefix, value in (("doi:", normalize_doi(doi)), ("arxiv:", normalize_arxiv_id(arxiv_id)),
                          ("openalex:", normalize_openalex_id(openalex_id))):
        if value:
            found.add(prefix + value)
    if semantic_scholar_id and semantic_scholar_id.strip():
        found.add("semantic_scholar:" + semantic_scholar_id.strip())
    # An arXiv identifier carried only by a URL or an arXiv DOI still identifies the
    # same manuscript, so it is parsed out rather than left as an unmatched alias.
    derived = _infer_arxiv_id_from_text(" ".join(str(v or "") for v in (url, doi, canonical_id, raw)))
    if derived:
        found.add("arxiv:" + derived)
    normalized_title = normalize_text(title or "")
    if len(normalized_title) > MIN_TITLE_IDENTITY_LENGTH:
        found.add("title:" + normalized_title)
    return tuple(sorted(found))


def paper_identities(paper) -> tuple[str, ...]:
    """Identities of one ranked library paper."""
    return identities(paper.canonical_id, title=paper.title, doi=paper.doi,
                      arxiv_id=paper.arxiv_id, openalex_id=paper.openalex_id,
                      semantic_scholar_id=paper.semantic_scholar_id, url=paper.url)


def _row_identities(row: sqlite3.Row) -> tuple[str, ...]:
    keys = set(row.keys())
    return identities(str(row["canonical_key"]), title=str(row["title"] or "") if "title" in keys else "",
                      doi=row["doi"] if "doi" in keys else None,
                      arxiv_id=row["arxiv_id"] if "arxiv_id" in keys else None,
                      openalex_id=row["openalex_id"] if "openalex_id" in keys else None,
                      semantic_scholar_id=row["semantic_scholar_id"] if "semantic_scholar_id" in keys else None,
                      url=row["url"] if "url" in keys else None,
                      raw=str(row["raw_json"] or "") if "raw_json" in keys else "")


def _table_exists(db: sqlite3.Connection, table: str) -> bool:
    return db.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
                      (table,)).fetchone() is not None


def excluded_identities(configs: dict[str, ScoutConfig],
                        roster_paths: tuple[Path, ...] = ()) -> dict[str, tuple[str, str]]:
    """Map every excluded identity to the (reason, source) that excluded it.

    Assessment rows and suppressions are read from every track, not only the track being
    built, because one manuscript can be discovered by more than one track and must not
    be reassessed under a second canonical id.
    """
    excluded: dict[str, tuple[str, str]] = {}

    def record(values, reason, source):
        for value in values:
            excluded.setdefault(value, (reason, source))

    for track, config in sorted(configs.items()):
        path = Path(config.sqlite_path)
        if not path.exists():
            continue
        with sqlite3.connect(path) as db:
            db.row_factory = sqlite3.Row
            rows = {str(r["canonical_key"]): r
                    for r in db.execute("SELECT * FROM papers").fetchall()}
            if _table_exists(db, "paper_quality_assessments"):
                for row in db.execute(
                        "SELECT DISTINCT canonical_id FROM paper_quality_assessments").fetchall():
                    key = str(row["canonical_id"])
                    paper = rows.get(key)
                    record(_row_identities(paper) if paper is not None else identities(key),
                           "prior_assessment", f"{track}:paper_quality_assessments")
            if _table_exists(db, "quality_suppressions"):
                for row in db.execute(
                        "SELECT canonical_key FROM quality_suppressions WHERE active = 1").fetchall():
                    key = str(row["canonical_key"])
                    paper = rows.get(key)
                    record(_row_identities(paper) if paper is not None else identities(key),
                           "suppressed", f"{track}:quality_suppressions")
        curation = _load_curation(Path(config.curation_path))
        for rule in [*curation.pinned, *curation.overrides, *curation.excluded]:
            if not rule.suppress_for_quality:
                continue
            record(identities(rule.canonical_id or "", title=rule.title or ""),
                   "suppressed", f"{track}:curation")
    for roster_path in roster_paths:
        for key in _roster_canonical_ids(Path(roster_path)):
            record(identities(key), "frozen_roster", roster_path.name)
    return excluded


def _roster_canonical_ids(path: Path) -> list[str]:
    """Every canonical id named anywhere in a frozen roster manifest."""
    found: list[str] = []

    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "canonical_id" and isinstance(item, str) and item.strip():
                    found.append(item.strip())
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(json.loads(path.read_text(encoding="utf-8")))
    return found


def ranked_candidates(config: ScoutConfig, build_time: str) -> tuple[list, str]:
    """The existing offline research ranking, with nothing that reaches the network.

    This is the same pipeline the published site is ordered by — duplicate merge, rule
    refresh, curation, quality presentation, newness, then the shared sort key — so the
    population and the dashboard cannot drift apart. Date enrichment is deliberately
    skipped: it calls arXiv, and a network answer would make the order unreproducible.
    """
    digests = [_parse_digest(path, Path(config.report_dir))
               for path in _daily_digest_paths(Path(config.digest_dir))]
    if not digests:
        raise ValueError("no digest archive; the ranking domain is undefined")
    latest_date = digests[-1].date
    papers = _load_library_papers(Path(config.sqlite_path))
    if not papers:
        return [], latest_date
    papers = _merge_dashboard_duplicates(papers)
    papers = _refresh_rule_classifications(papers, relevance_profile=config.relevance_profile)
    papers = _apply_curation(papers, _load_curation(Path(config.curation_path)), latest_date,
                             relevance_profile=config.relevance_profile)
    papers = _apply_quality_presentation(papers, config.quality)
    papers = _mark_new_papers(papers, _site_build_time(build_time), latest_date)
    return _sort_latest_relevant(papers), latest_date


def build_population(configs: dict[str, ScoutConfig], build_time: str,
                     roster_paths: tuple[Path, ...] = ()) -> Population:
    """Construct the eligible population for every configured track, in selection order."""
    excluded = excluded_identities(configs, roster_paths)
    tracks = []
    for track in sorted(configs):
        papers, latest_date = ranked_candidates(configs[track], build_time)
        eligible: list[Candidate] = []
        removed: list[Exclusion] = []
        ranked = [p for p in papers if p.decision == ELIGIBLE_RELEVANCE]
        for rank, paper in enumerate(ranked, start=1):
            found = paper_identities(paper)
            match = next(((value, *excluded[value]) for value in found if value in excluded), None)
            if match is None:
                eligible.append(Candidate(paper.canonical_id, track, rank, paper.title, found))
            else:
                identity, reason, source = match
                removed.append(Exclusion(paper.canonical_id, track, rank, paper.title,
                                         reason, identity, source))
        tracks.append(TrackPopulation(track, tuple(eligible), tuple(removed), len(ranked), latest_date))
    return Population(tuple(tracks), sources=_sources(configs, build_time, roster_paths))


def _sources(configs: dict[str, ScoutConfig], build_time: str,
             roster_paths: tuple[Path, ...]) -> dict:
    """Every input the construction read, named explicitly so it can be reread."""
    return {
        "build_time": _site_build_time(build_time).isoformat(),
        "relevance": ELIGIBLE_RELEVANCE,
        "date_enrichment": "disabled (offline; network answers are not reproducible)",
        "tracks": {track: {"state_path": str(config.sqlite_path),
                           "curation_path": str(config.curation_path),
                           "digest_dir": str(config.digest_dir),
                           "relevance_profile": config.relevance_profile}
                   for track, config in sorted(configs.items())},
        "frozen_rosters": [{"path": str(path), "sha256": digest(Path(path).read_text(encoding="utf-8"))}
                           for path in roster_paths],
    }


def population_manifest(population: Population, code_sha: str) -> dict:
    """The manifest, hashed over its reproducible content only.

    code_sha and created_at record who produced the manifest and are kept outside the
    hash, so the same frozen state rebuilds byte-identical content from a later commit
    that does not change ranking, while any change to the population itself is caught.
    """
    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "population_version": POPULATION_VERSION,
        "identity_policy": IDENTITY_POLICY,
        "exclusion_sources": EXCLUSION_SOURCES,
        "sources": population.sources,
        "tracks": {track.track: track.to_dict() for track in population.tracks},
    }
    manifest["manifest_sha256"] = digest(canonical_json(manifest))
    manifest["code_sha"] = code_sha
    manifest["created_at"] = datetime.now(UTC).isoformat()
    return manifest


def manifest_digest(manifest: dict) -> str:
    """Recompute a manifest's digest over the same reproducible content."""
    hashed = {k: v for k, v in manifest.items()
              if k not in {"manifest_sha256", "code_sha", "created_at"}}
    return digest(canonical_json(hashed))


def write_manifest(path: Path, manifest: dict) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


@dataclass(frozen=True)
class Verification:
    """Whether a stored manifest rebuilds identically from the current frozen state."""

    reproduced: bool
    stored_digest: str
    rebuilt_digest: str
    self_consistent: bool
    tracks: dict

    def to_dict(self) -> dict:
        return {"reproduced": self.reproduced, "self_consistent": self.self_consistent,
                "stored_manifest_sha256": self.stored_digest,
                "rebuilt_manifest_sha256": self.rebuilt_digest, "tracks": self.tracks}


def verify_manifest(manifest: dict, configs: dict[str, ScoutConfig]) -> Verification:
    """Rebuild the population from the manifest's own recorded inputs and compare.

    The ordered identifier lists are compared element by element, not only by digest, so
    a manifest that stored a hash over something it no longer contains cannot pass.
    """
    sources = manifest["sources"]
    rosters = tuple(Path(item["path"]) for item in sources.get("frozen_rosters", []))
    rebuilt = build_population(configs, sources["build_time"], rosters)
    rebuilt_manifest = population_manifest(rebuilt, manifest.get("code_sha", ""))
    tracks = {}
    for track in rebuilt.tracks:
        stored = manifest["tracks"].get(track.track, {})
        stored_ids = list(stored.get("ordered_canonical_ids", []))
        rebuilt_ids = list(track.ordered_canonical_ids)
        tracks[track.track] = {
            "ordered_ids_match": stored_ids == rebuilt_ids,
            "population_sha256_match": stored.get("population_sha256") == track.population_sha256,
            "stored_count": len(stored_ids), "rebuilt_count": len(rebuilt_ids),
            "missing": [i for i in stored_ids if i not in rebuilt_ids][:20],
            "unexpected": [i for i in rebuilt_ids if i not in stored_ids][:20],
        }
    stored_digest = manifest.get("manifest_sha256", "")
    rebuilt_digest = rebuilt_manifest["manifest_sha256"]
    return Verification(
        reproduced=stored_digest == rebuilt_digest and all(
            t["ordered_ids_match"] and t["population_sha256_match"] for t in tracks.values()),
        stored_digest=stored_digest, rebuilt_digest=rebuilt_digest,
        self_consistent=manifest_digest(manifest) == stored_digest, tracks=tracks)


def repository_code_sha(root: Path = Path(".")) -> str:
    """The checked-out commit, read from the git directory rather than a subprocess.

    Reading the files directly keeps manifest construction independent of whether a
    usable git executable is on PATH, which is not guaranteed on every host.
    """
    head_path = Path(root) / ".git" / "HEAD"
    if not head_path.exists():
        return "unknown"
    head = head_path.read_text(encoding="utf-8").strip()
    if not head.startswith("ref:"):
        return head
    ref = head.split(":", 1)[1].strip()
    direct = Path(root) / ".git" / ref
    if direct.exists():
        return direct.read_text(encoding="utf-8").strip()
    packed = Path(root) / ".git" / "packed-refs"
    if packed.exists():
        for line in packed.read_text(encoding="utf-8").splitlines():
            if line.endswith(" " + ref):
                return line.split(" ", 1)[0]
    return "unknown"


def track_configs(config_path: Path, tracks: tuple[str, ...] = TRACKS) -> dict[str, ScoutConfig]:
    return {validate_track(track): load_config(config_path, track_id=track) for track in tracks}
