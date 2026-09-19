"""Credential preflight and the per-run assessment budget.

Two guards that have to run *before* the scientific path touches a paper.

The first is credentials. The promotion gate resolves each scientific role's credential
from the environment, and when either is absent it returns a ``not_assessed`` result
that the storage layer then persists like any other. Under the historical exclusion
policy that row retired the paper permanently, so a forgotten Actions secret could have
silently consumed a day's candidates without a single model call. Selection is now
filtered on completed assessments rather than on any row, which removes the permanent
damage; this module removes the row as well, by refusing to enter the scientific path at
all when the pair is not fully configured. A run-level reason is recorded instead.

The second is the budget: how many papers one scheduled run may assess, and how much
OpenRouter money it may spend doing it. Both fail closed — an unknown price or an
unparseable ceiling stops the run rather than proceeding on an assumption.

No credential value is read, printed, hashed, logged or returned. Only presence is
reported, and only by environment-variable name.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import os
from typing import Any

from paper_scout.promotion_protocol import MODEL_PROVIDERS, PROVIDERS

PREFLIGHT_VERSION = "credential-preflight-v1"
BUDGET_VERSION = "operational-budget-v1"

#: Conservative initial production bounds. One paper per track per scheduled run, three
#: papers across all tracks. A track with no eligible paper forfeits its slot; its quota
#: is never transferred to another track, so the normal maximum today is two per day.
#:
#: These bound papers that actually reach a model. A candidate rejected by acquisition or
#: the coverage gate never issues a request and costs nothing, so it is bounded separately
#: by MAX_ACQUISITION_WALK below rather than consuming a track's assessment slot.
MAX_PAPERS_PER_TRACK = 1
MAX_PAPERS_PER_RUN = 3

#: How many candidates one track may try before giving up for this run.
#:
#: Selection cannot know whether a manuscript is retrievable without fetching it, and the
#: head of the ranking is dominated by records with no retrievable or coverage-valid PDF.
#: Two production runs on 2026-09-19 took the single top candidate per track and reached a
#: model 0 times out of 4. Batch 6, which walked the same ranking, needed 14 candidates to
#: find 5 acquirable ones in agent_memory and 20 to find 5 in deep_research — roughly a
#: quarter to a third. Six attempts per track makes finding one likely without turning a
#: daily run into an unbounded crawl, and every attempt is recorded, so a permanently dead
#: manuscript still parks at the retry budget instead of being probed forever.
MAX_ACQUISITION_WALK = 6

#: Per-run ceiling on *known* OpenRouter spend, in USD. A maximum, not a target.
DEFAULT_OPENROUTER_RUN_CEILING_USD = 0.30
OPENROUTER_CEILING_ENV = "PAPER_SCOUT_OPENROUTER_RUN_CEILING_USD"

#: Expected OpenRouter cost of one paper's adjudication, reserved *before* the calls are
#: made. Batch 6 measured $0.29777891 across ten papers, or $0.0297779 each; this is
#: rounded up and allows for the bounded adjudicator retry.
#:
#: The ceiling is enforced between papers, not inside one. A single paper's calls are
#: already committed once they are issued, so the guarantee this provides is: the run
#: never *starts* a paper whose expected cost would carry it past the ceiling. With a
#: three-paper maximum and this estimate the worst case is far under $0.30, and the
#: residual exposure is one paper's overrun. Enforcing a true hard cap would require a
#: provider-side spend limit on the OpenRouter key, which is an account setting rather
#: than something this process can impose.
ESTIMATED_OPENROUTER_USD_PER_PAPER = 0.05


@dataclass(frozen=True)
class RolePreflight:
    role: str
    provider: str
    model: str
    credential_env: tuple[str, ...]
    present: bool

    def to_dict(self) -> dict:
        return {"role": self.role, "provider": self.provider, "model": self.model,
                "credential_env": list(self.credential_env), "credential_present": self.present}


@dataclass(frozen=True)
class PreflightResult:
    """Whether the scientific path may run, and why not when it may not."""

    ok: bool
    reason: str
    roles: tuple[RolePreflight, ...]

    @property
    def missing_roles(self) -> tuple[str, ...]:
        return tuple(role.role for role in self.roles if not role.present)

    def to_dict(self) -> dict:
        return {"version": PREFLIGHT_VERSION, "scientific_assessment_permitted": self.ok,
                "reason": self.reason, "missing_roles": list(self.missing_roles),
                "roles": [role.to_dict() for role in self.roles]}


def credential_preflight(primary_model: str | None = None,
                         adjudicator_model: str | None = None,
                         environ: dict | None = None) -> PreflightResult:
    """Report whether both scientific roles have a usable credential.

    Presence only. The value is never read into the result, and an absent credential is
    reported by the environment-variable names that would have supplied it.
    """
    from paper_scout.promotion_gate import ADJUDICATOR_MODEL, PRIMARY_MODEL

    env = os.environ if environ is None else environ
    primary = primary_model or env.get("PAPER_SCOUT_QUALITY_LLM_MODEL") or PRIMARY_MODEL
    adjudicator = adjudicator_model or env.get("PAPER_SCOUT_QUALITY_ADJUDICATOR_MODEL") or ADJUDICATOR_MODEL

    roles: list[RolePreflight] = []
    for role, model in (("primary", primary), ("adjudicator", adjudicator)):
        provider = MODEL_PROVIDERS.get(model)
        if provider is None:
            roles.append(RolePreflight(role, "unknown", model, (), False))
            continue
        names = tuple(PROVIDERS[provider]["credential_env"])
        present = any((env.get(name, "") or "").strip() for name in names)
        roles.append(RolePreflight(role, provider, model, names, present))

    mode = (env.get("PAPER_SCOUT_LLM_PROVIDER", "auto") or "auto").lower()
    if mode in {"", "none", "off", "rules"}:
        return PreflightResult(False, "scientific_provider_disabled", tuple(roles))
    unknown = [role.role for role in roles if role.provider == "unknown"]
    if unknown:
        return PreflightResult(False, f"unknown_scientific_model_provider:{','.join(unknown)}", tuple(roles))
    missing = [role.role for role in roles if not role.present]
    if missing:
        # Both roles are required. One credential is not a usable independence gate, and
        # entering the path on a half-configured pair is what wrote the empty rows.
        return PreflightResult(False, f"missing_credential:{','.join(missing)}", tuple(roles))
    return PreflightResult(True, "credentials_present", tuple(roles))


class CostCeilingExceeded(RuntimeError):
    """Raised when the next paper would carry known spend past the per-run ceiling."""


@dataclass
class RunBudget:
    """Bounded per-run assessment and spend budget.

    Tracks papers per track, papers overall and known OpenRouter money. Gemini usage is
    recorded in tokens only: this project has not established the MSc allocation's
    effective rate, so no monetary amount is inferred for it.
    """

    max_per_track: int = MAX_PAPERS_PER_TRACK
    max_per_run: int = MAX_PAPERS_PER_RUN
    openrouter_ceiling_usd: float = DEFAULT_OPENROUTER_RUN_CEILING_USD
    assessed_per_track: dict[str, int] = field(default_factory=dict)
    openrouter_spend_usd: float = 0.0
    gemini_input_tokens: int = 0
    gemini_output_tokens: int = 0
    gemini_calls: int = 0
    openrouter_calls: int = 0
    stopped_reason: str | None = None

    @classmethod
    def from_env(cls, environ: dict | None = None) -> "RunBudget":
        env = os.environ if environ is None else environ
        raw = (env.get(OPENROUTER_CEILING_ENV, "") or "").strip()
        if not raw:
            ceiling = DEFAULT_OPENROUTER_RUN_CEILING_USD
        else:
            try:
                ceiling = float(raw)
            except ValueError as exc:
                raise ValueError(f"{OPENROUTER_CEILING_ENV} is not a number") from exc
            if ceiling <= 0:
                raise ValueError(f"{OPENROUTER_CEILING_ENV} must be positive")
        return cls(openrouter_ceiling_usd=ceiling)

    @property
    def total_assessed(self) -> int:
        return sum(self.assessed_per_track.values())

    @property
    def remaining_usd(self) -> float:
        return self.openrouter_ceiling_usd - self.openrouter_spend_usd

    def may_assess(self, track: str) -> tuple[bool, str]:
        """Whether one more paper may be assessed on this track."""
        if self.stopped_reason:
            return False, self.stopped_reason
        if self.total_assessed >= self.max_per_run:
            return False, "run_paper_limit_reached"
        if self.assessed_per_track.get(track, 0) >= self.max_per_track:
            return False, "track_paper_limit_reached"
        if self.openrouter_spend_usd >= self.openrouter_ceiling_usd:
            return False, "openrouter_ceiling_reached"
        return True, "within_budget"

    def reserve(self, track: str, projected_usd: float | None = None) -> None:
        """Check the projected cost of the next paper before it is assessed.

        Fails closed: a projection that would carry the run past the ceiling stops the
        run rather than being attempted and reconciled afterwards. The default projection
        is the measured per-paper estimate, so a caller that does not supply one still
        gets a real pre-spend check rather than a no-op.
        """
        if projected_usd is None:
            projected_usd = ESTIMATED_OPENROUTER_USD_PER_PAPER
        allowed, reason = self.may_assess(track)
        if not allowed:
            raise CostCeilingExceeded(reason)
        if projected_usd < 0:
            raise ValueError("projected cost cannot be negative")
        if self.openrouter_spend_usd + projected_usd > self.openrouter_ceiling_usd:
            self.stopped_reason = "openrouter_projection_exceeds_ceiling"
            raise CostCeilingExceeded(self.stopped_reason)

    def record(self, track: str, *, openrouter_usd: float = 0.0, openrouter_calls: int = 0,
               gemini_calls: int = 0, gemini_input_tokens: int = 0,
               gemini_output_tokens: int = 0) -> None:
        """Record one completed attempt's actual usage against the budget."""
        self.assessed_per_track[track] = self.assessed_per_track.get(track, 0) + 1
        self.openrouter_spend_usd += max(0.0, float(openrouter_usd))
        self.openrouter_calls += openrouter_calls
        self.gemini_calls += gemini_calls
        self.gemini_input_tokens += gemini_input_tokens
        self.gemini_output_tokens += gemini_output_tokens
        if self.openrouter_spend_usd >= self.openrouter_ceiling_usd:
            self.stopped_reason = "openrouter_ceiling_reached"

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": BUDGET_VERSION,
            "max_papers_per_track": self.max_per_track,
            "max_papers_per_run": self.max_per_run,
            "papers_assessed_per_track": dict(sorted(self.assessed_per_track.items())),
            "papers_assessed_total": self.total_assessed,
            "openrouter_ceiling_usd": round(self.openrouter_ceiling_usd, 8),
            "openrouter_spend_usd": round(self.openrouter_spend_usd, 8),
            "openrouter_calls": self.openrouter_calls,
            "gemini_calls": self.gemini_calls,
            "gemini_input_tokens": self.gemini_input_tokens,
            "gemini_output_tokens": self.gemini_output_tokens,
            "gemini_monetary_cost": "UNKNOWN / MSc allocation",
            "stopped_reason": self.stopped_reason,
        }
