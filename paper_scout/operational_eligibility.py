"""What counts as a completed scientific assessment, and when a paper may be retried.

Operational selection has to separate two things the stored history records in the same
table: a *completed scientific assessment*, where the pipeline reached a valid scientific
decision, and a *technically incomplete attempt*, where it did not. A missing credential,
a provider outage, an unreachable manuscript or a malformed response after the bounded
in-run retries are all infrastructure outcomes. None of them is a scientific judgment
about a paper, so none of them may permanently remove the paper from consideration.

Before this module, exclusion asked only whether any row existed for a canonical id, so
a single technical row — or even a pre-gate deterministic placeholder — retired a paper
forever. Two policies are defined here and both are named and versioned, because the
frozen batch manifests were built under the historical one and must keep rebuilding
byte-identically:

``prior_assessment``
    Historical. Any stored row excludes. Reproduces Batch 2-6 populations exactly.

``prior_completed_assessment``
    Operational. Only a completed scientific assessment excludes; a technical attempt
    leaves the paper retry-eligible under a bounded budget.

Nothing here deletes or rewrites a row. Technical rows stay in the history and stay
auditable; they simply stop being read as scientific decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Iterable, Mapping

OPERATIONAL_POLICY_VERSION = "operational-eligibility-v1"

EXCLUSION_POLICIES = ("prior_assessment", "prior_completed_assessment")
#: Manifests written before this module existed carry no policy field. They were built
#: under the historical policy, so that is what a missing field has to mean.
LEGACY_EXCLUSION_POLICY = "prior_assessment"
OPERATIONAL_EXCLUSION_POLICY = "prior_completed_assessment"

#: Execution outcomes that mean no valid scientific decision was reached. The first six
#: are the promotion gate's own technical returns; the next two come from the legacy
#: scientific gate; ``credential_unavailable`` is never persisted and is named here so
#: the set stays the single definition of "not a scientific decision".
TECHNICAL_OUTCOMES = frozenset({
    "not_assessed",
    "transport_failure",
    "protocol_failure",
    "manuscript_unavailable",
    "text_coverage_failure",
    "integrity_failure",
    "evidence_validation_failure",
    "support_verification_pending",
    "credential_unavailable",
})

#: Outcomes that do record a scientific decision. ``success`` is the promotion gate's;
#: ``scientific`` is the legacy gate's; ``None`` belongs to rows written before any
#: execution receipt existed, which are judged on assessor type and scope alone.
SCIENTIFIC_OUTCOMES = frozenset({"success", "scientific"})

#: A deterministic row is a rules-only placeholder, never a scientific judgment.
SCIENTIFIC_ASSESSOR_TYPES = frozenset({"llm", "hybrid", "manual_override"})
SCIENTIFIC_SCOPES = frozenset({"full_text", "partial_full_text"})

#: Bounded operational retry budget. This is a cross-run bound and is deliberately
#: separate from the in-run retry policy (primary 1, adjudicator 2, 3 requests total),
#: which is frozen and unchanged. Once a paper has recorded this many technical
#: attempts it stops being selected automatically and is surfaced for operator review,
#: so a permanently unreachable manuscript cannot be retried every day forever.
MAX_OPERATIONAL_ATTEMPTS = 3
#: A failed attempt is not retried until the cooldown elapses, so one provider outage
#: cannot consume the whole budget inside a single hour.
RETRY_COOLDOWN_HOURS = 20

RETRY_POLICY = {
    "version": OPERATIONAL_POLICY_VERSION,
    "max_operational_attempts": MAX_OPERATIONAL_ATTEMPTS,
    "retry_cooldown_hours": RETRY_COOLDOWN_HOURS,
    "technical_outcomes": sorted(TECHNICAL_OUTCOMES),
    "in_run_retries_unchanged": "primary 1, adjudicator 2, 3 requests total",
}


def _payload(row: Any) -> Mapping[str, Any]:
    """Accept a stored payload mapping or a QualityAssessment-like object."""
    if isinstance(row, Mapping):
        return row
    return {
        "assessor_type": getattr(row, "assessor_type", None),
        "assessment_scope": getattr(row, "assessment_scope", None),
        "quality_status": getattr(row, "quality_status", None),
        "assessed_at": getattr(row, "assessed_at", None),
        "execution": getattr(row, "execution", {}) or {},
    }


def outcome_of(row: Any) -> str | None:
    execution = _payload(row).get("execution") or {}
    outcome = execution.get("outcome") if isinstance(execution, Mapping) else None
    return str(outcome) if outcome is not None else None


def is_completed_scientific_assessment(row: Any) -> bool:
    """True when this row records a valid scientific decision about the manuscript.

    Requires all three of: a semantic assessor, manuscript-derived scope, and an
    execution outcome that is not a technical failure. A row missing any of them is an
    attempt, a placeholder or a legacy artifact — never a decision that should retire
    the paper.
    """
    payload = _payload(row)
    if payload.get("assessor_type") not in SCIENTIFIC_ASSESSOR_TYPES:
        return False
    if payload.get("assessment_scope") not in SCIENTIFIC_SCOPES:
        return False
    outcome = outcome_of(payload)
    if outcome is None:
        # Pre-receipt history: the assessor type and scope are the only evidence, and
        # both already say a semantic assessor read the manuscript.
        return True
    return outcome not in TECHNICAL_OUTCOMES


def is_technical_attempt(row: Any) -> bool:
    """True when this row records a scientific attempt that failed for technical reasons.

    A deterministic placeholder with no execution receipt is not an attempt: nothing was
    tried, so it consumes no part of the retry budget.
    """
    outcome = outcome_of(row)
    return outcome is not None and outcome in TECHNICAL_OUTCOMES


@dataclass(frozen=True)
class RetryState:
    """Why a paper is, or is not, an operational assessment candidate."""

    canonical_id: str
    completed: bool
    attempts: int
    last_attempt_at: str | None
    last_outcome: str | None
    eligible: bool
    reason: str

    def to_dict(self) -> dict:
        return {
            "canonical_id": self.canonical_id,
            "completed_scientific_assessment": self.completed,
            "technical_attempts": self.attempts,
            "last_attempt_at": self.last_attempt_at,
            "last_outcome": self.last_outcome,
            "retry_eligible": self.eligible,
            "reason": self.reason,
            "policy": OPERATIONAL_POLICY_VERSION,
        }


def _parse_time(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def retry_state(canonical_id: str, rows: Iterable[Any], *, now: datetime | None = None) -> RetryState:
    """Decide whether one paper may be assessed on this run.

    Rows may arrive in any order; recency is taken from ``assessed_at`` and ties fall
    back to the supplied order, so a caller that already sorts by row id keeps its order.
    """
    now = now or datetime.now(UTC)
    rows = list(rows)
    completed = any(is_completed_scientific_assessment(row) for row in rows)
    attempts_rows = [row for row in rows if is_technical_attempt(row)]
    attempts = len(attempts_rows)

    last_at: datetime | None = None
    last_outcome: str | None = None
    for row in attempts_rows:
        stamp = _parse_time(_payload(row).get("assessed_at"))
        if stamp is not None and (last_at is None or stamp >= last_at):
            last_at, last_outcome = stamp, outcome_of(row)
    if last_outcome is None and attempts_rows:
        # Every attempt carried an unparseable or absent timestamp. Report the last row
        # in the supplied order rather than nothing; the cooldown simply cannot apply.
        last_outcome = outcome_of(attempts_rows[-1])
    last_attempt_at = last_at.isoformat() if last_at else None

    def state(eligible: bool, reason: str) -> RetryState:
        return RetryState(canonical_id=canonical_id, completed=completed, attempts=attempts,
                          last_attempt_at=last_attempt_at, last_outcome=last_outcome,
                          eligible=eligible, reason=reason)

    if completed:
        # The decisive case: a scientific decision exists, so the paper is done whether
        # it was promoted or not, and re-running it would duplicate a settled result.
        return state(False, "completed_scientific_assessment")
    if attempts >= MAX_OPERATIONAL_ATTEMPTS:
        return state(False, "retry_budget_exhausted")
    if last_at is not None and now - last_at < timedelta(hours=RETRY_COOLDOWN_HOURS):
        return state(False, "retry_cooldown")
    return state(True, "never_assessed" if attempts == 0 else "retry_eligible")


def excludes_from_eligibility(rows: Iterable[Any], policy: str = OPERATIONAL_EXCLUSION_POLICY) -> bool:
    """Whether this paper's stored rows remove it from the eligible population."""
    if policy not in EXCLUSION_POLICIES:
        raise ValueError(f"unknown exclusion policy: {policy}")
    rows = list(rows)
    if policy == LEGACY_EXCLUSION_POLICY:
        return bool(rows)
    return any(is_completed_scientific_assessment(row) for row in rows)
