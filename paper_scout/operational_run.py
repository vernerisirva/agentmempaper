"""Daily operational candidate selection and the run record it leaves behind.

Ordinary daily operation does not use the batch-manifest experiment structure: there is
no frozen roster, no pinned build time and no population digest to commit to. What it
does keep is enough provenance to reconstruct, later, why each paper was selected — the
rank it held, the policy versions in force, the retry state that made it eligible, and
what the budget allowed at the moment it was chosen.

Selection is the canonical deterministic eligibility logic, in one place:

    high relevance
    AND not suppressed
    AND no completed scientific assessment
    AND retry-eligible under the bounded operational policy
    AND within the per-track and per-run paper budget

Manuscript retrievability and the coverage gate are deliberately *not* evaluated here.
They require network acquisition, they are already enforced inside the promotion gate,
and a candidate that fails them is a technical outcome rather than a selection error. The
selector therefore nominates candidates and the gate remains the only thing that decides
whether a manuscript can actually be assessed.
"""
from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass, field
from datetime import UTC, datetime
import json
from pathlib import Path
import sqlite3

from paper_scout.batch_population import ranked_candidates
from paper_scout.config import ScoutConfig
from paper_scout.operational_eligibility import (
    OPERATIONAL_POLICY_VERSION, RETRY_POLICY, RetryState, retry_state,
)
from paper_scout.operational_preflight import (
    BUDGET_VERSION, MAX_PAPERS_PER_RUN, MAX_PAPERS_PER_TRACK, PREFLIGHT_VERSION, RunBudget,
)

OPERATIONAL_RUN_VERSION = "operational-run-v1"
ELIGIBLE_RELEVANCE = "relevant"


@dataclass(frozen=True)
class OperationalCandidate:
    """One selected paper and the complete reason it was selected."""

    canonical_id: str
    track: str
    rank: int
    title: str
    retry: RetryState

    def to_dict(self) -> dict:
        return {"canonical_id": self.canonical_id, "track": self.track, "rank": self.rank,
                "title": self.title, "selection": self.retry.to_dict()}


def _stored_assessments(path: Path) -> dict[str, list[dict]]:
    """Every stored assessment payload for one track, grouped by canonical id."""
    if not Path(path).exists():
        return {}
    grouped: dict[str, list[dict]] = {}
    with closing(sqlite3.connect(path)) as db:
        db.row_factory = sqlite3.Row
        exists = db.execute("SELECT 1 FROM sqlite_master WHERE type='table'"
                            " AND name='paper_quality_assessments'").fetchone()
        if not exists:
            return {}
        for row in db.execute("SELECT canonical_id, payload_json"
                              " FROM paper_quality_assessments ORDER BY id"):
            try:
                payload = json.loads(row["payload_json"])
            except (TypeError, ValueError):
                payload = {}
            grouped.setdefault(str(row["canonical_id"]), []).append(payload)
    return grouped


def _suppressed(path: Path) -> set[str]:
    if not Path(path).exists():
        return set()
    with closing(sqlite3.connect(path)) as db:
        exists = db.execute("SELECT 1 FROM sqlite_master WHERE type='table'"
                            " AND name='quality_suppressions'").fetchone()
        if not exists:
            return set()
        return {str(row[0]) for row in
                db.execute("SELECT canonical_key FROM quality_suppressions WHERE active = 1")}


@dataclass
class TrackSelection:
    track: str
    ranked: int = 0
    high_relevance: int = 0
    suppressed: int = 0
    already_assessed: int = 0
    retry_blocked: int = 0
    candidates: list[OperationalCandidate] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"ranked": self.ranked, "high_relevance": self.high_relevance,
                "suppressed": self.suppressed,
                "completed_scientific_assessment": self.already_assessed,
                "retry_blocked": self.retry_blocked,
                "selected": [c.to_dict() for c in self.candidates]}


def select_operational_candidates(configs: dict[str, ScoutConfig], build_time: str,
                                  budget: RunBudget | None = None,
                                  now: datetime | None = None,
                                  assessment_sources: dict[str, Path] | None = None
                                  ) -> tuple[list[OperationalCandidate], dict[str, TrackSelection]]:
    """Choose at most one paper per track, up to the per-run total.

    Stored assessments are read from *every* configured track, not only the track being
    selected for, because one manuscript can be discovered under more than one track and
    must not be assessed twice under two canonical ids.

    Tracks are walked in sorted order and each contributes at most ``max_per_track``. A
    track with nothing eligible simply contributes nothing: its slot is never handed to
    another track, so the usual daily maximum is below the per-run ceiling by design.
    """
    budget = budget or RunBudget()
    now = now or datetime.now(UTC)

    sources = assessment_sources or {track: Path(config.sqlite_path)
                                     for track, config in configs.items()}
    stored: dict[str, list[dict]] = {}
    for path in sources.values():
        for canonical_id, payloads in _stored_assessments(Path(path)).items():
            stored.setdefault(canonical_id, []).extend(payloads)
    suppressed: set[str] = set()
    for path in sources.values():
        suppressed |= _suppressed(Path(path))

    selected: list[OperationalCandidate] = []
    summaries: dict[str, TrackSelection] = {}
    # Selection reserves slots in its own counter. The caller's budget records what was
    # actually spent, and the two must not be conflated: a selected paper that later
    # fails acquisition consumed a selection slot but no money and no eligibility.
    reserved: dict[str, int] = {}

    def slot_available(track: str) -> bool:
        if sum(reserved.values()) >= budget.max_per_run:
            return False
        return reserved.get(track, 0) < budget.max_per_track

    for track in sorted(configs):
        summary = TrackSelection(track)
        summaries[track] = summary
        papers, _ = ranked_candidates(configs[track], build_time)
        summary.ranked = len(papers)
        ranked = [p for p in papers if p.decision == ELIGIBLE_RELEVANCE]
        summary.high_relevance = len(ranked)
        for rank, paper in enumerate(ranked, start=1):
            if not slot_available(track):
                break
            if paper.canonical_id in suppressed:
                summary.suppressed += 1
                continue
            state = retry_state(paper.canonical_id, stored.get(paper.canonical_id, []), now=now)
            if state.completed:
                summary.already_assessed += 1
                continue
            if not state.eligible:
                summary.retry_blocked += 1
                continue
            candidate = OperationalCandidate(paper.canonical_id, track, rank, paper.title, state)
            selected.append(candidate)
            summary.candidates.append(candidate)
            reserved[track] = reserved.get(track, 0) + 1
    return selected, summaries


@dataclass
class OperationalMetrics:
    """Everything one scheduled run should report, in one serializable record."""

    started_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    papers_discovered: int = 0
    high_relevance_candidates: int = 0
    assessment_candidates: int = 0
    papers_attempted: int = 0
    papers_successfully_assessed: int = 0
    promoted: int = 0
    non_promoted: int = 0
    technical_failures: int = 0
    retry_eligible_failures: int = 0
    unavailable_manuscripts: int = 0
    coverage_failures: int = 0
    credential_skipped: int = 0
    gemini_calls: int = 0
    gemini_input_tokens: int = 0
    gemini_output_tokens: int = 0
    deepseek_calls: int = 0
    deepseek_input_tokens: int = 0
    deepseek_output_tokens: int = 0
    deepseek_cost_usd: float = 0.0
    unknown_cost_calls: int = 0
    unattributed_calls: int = 0
    state_restore_sha256: dict = field(default_factory=dict)
    state_persist_sha256: dict = field(default_factory=dict)
    pages_deployment: str = "not_attempted"
    preflight: dict = field(default_factory=dict)
    budget: dict = field(default_factory=dict)
    tracks: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "version": OPERATIONAL_RUN_VERSION,
            "policy_versions": {
                "operational_eligibility": OPERATIONAL_POLICY_VERSION,
                "credential_preflight": PREFLIGHT_VERSION,
                "operational_budget": BUDGET_VERSION,
            },
            "retry_policy": RETRY_POLICY,
            "limits": {"max_papers_per_track": MAX_PAPERS_PER_TRACK,
                       "max_papers_per_run": MAX_PAPERS_PER_RUN},
            "started_at": self.started_at,
            "completed_at": datetime.now(UTC).isoformat(),
            "discovery": {"papers_discovered": self.papers_discovered,
                          "high_relevance_candidates": self.high_relevance_candidates},
            "selection": {"assessment_candidates": self.assessment_candidates,
                          "tracks": self.tracks},
            "assessment": {
                "papers_attempted": self.papers_attempted,
                "papers_successfully_assessed": self.papers_successfully_assessed,
                "promoted": self.promoted,
                "non_promoted": self.non_promoted,
                "technical_failures": self.technical_failures,
                "retry_eligible_failures": self.retry_eligible_failures,
                "unavailable_manuscripts": self.unavailable_manuscripts,
                "coverage_failures": self.coverage_failures,
                "credential_skipped_without_row": self.credential_skipped,
            },
            "cost": {
                "gemini_calls": self.gemini_calls,
                "gemini_input_tokens": self.gemini_input_tokens,
                "gemini_output_tokens": self.gemini_output_tokens,
                "gemini_monetary_cost": "UNKNOWN / MSc allocation",
                "deepseek_calls": self.deepseek_calls,
                "deepseek_input_tokens": self.deepseek_input_tokens,
                "deepseek_output_tokens": self.deepseek_output_tokens,
                "deepseek_cost_usd": round(self.deepseek_cost_usd, 8),
                # Calls the provider did not price, and calls whose provider could not be
                # attributed. Both mean the money figure above is a lower bound.
                "unknown_cost_calls": self.unknown_cost_calls,
                "unattributed_calls": self.unattributed_calls,
            },
            "state": {"restore_sha256": self.state_restore_sha256,
                      "persist_sha256": self.state_persist_sha256},
            "pages_deployment": self.pages_deployment,
            "preflight": self.preflight,
            "budget": self.budget,
        }
