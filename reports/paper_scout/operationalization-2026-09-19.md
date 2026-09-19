# Operationalization — 2026-09-19

**Two defects stood between the validated gate and safe recurring operation, and both are fixed and merged. A technical failure permanently retired a paper: 434 of the 509 papers holding assessment rows had never received a scientific decision yet were already excluded forever. And the runtime state — all three databases, including 18 rows of raw model payloads — answered an unauthenticated request with HTTP 200 from a public release. Recurring assessment remains DISABLED, because the private state destination and both scientific secrets are not yet provisioned.**

```text
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE = YES   (Batch 6, unchanged)
PRIVATE_DURABLE_STATE_READY:        NO    — implemented and tested; destination not provisioned
OPERATIONAL_QUALITY_ASSESSMENT_READY: NO  — blocked only on credentials and state
RECURRING_QUALITY_ASSESSMENT_ENABLED: NO
```

| Item | Value |
|---|---|
| Canonical base SHA | `e87c4abaa08456ef9e9177c33e15d7b6da3fcf20` |
| Merged SHA | **`48f3088fcbb6a47c911fa1a50d250696075dbe46`** (PR #41) |
| Branch | `operationalize-quality-promotion-gate`, merged and deleted |
| Scientific rubric / prompts / models / thresholds | **unchanged** |
| New validation batches created | **none** |

## A. Validated scientific readiness

Carried forward unmodified. Nothing in this cycle touched the rubric, the assessor or adjudicator prompt, the Gemini or DeepSeek model, the promotion threshold, evaluation-independence semantics, evidence semantics, manuscript-coverage semantics or relevance thresholds.

```text
BATCH_5_GENERALIZATION_RESULT      = PASS
EVALUATION_INDEPENDENCE_DIAGNOSTIC = FAIL
EVALUATION_INDEPENDENCE_RECOVERY   = PASS
BATCH_6_GENERALIZATION_RESULT      = PASS
```

Frozen versions still in force: `dual-promotion-v3`, `quality-promotion-v2`, `scholarly-rubric-v2`, `evaluation-independence-v1`, `canonical-response-v1`, `model-pair-v1`, `adjudicator-contract-retry-v2`, `block-evidence-v2`, `coverage-v2`.

**The frozen Batch-5 and Batch-6 population manifests still rebuild to the same digests as the unmodified base code** — `a9e07aa3e745ed59…` and `4580f6aed4a78938…`, compared against a worktree at `e87c4abaa` reading the same databases. The exclusion-policy change is exactly neutral for them. (Both differ from the digests *stored* in those manifests, by −5 eligible papers per track; that is pre-existing drift from Batch 6's own ten assessments now being in the database, present identically before this cycle.)

## B. The eligibility defect, and what it had already cost

`assess_promotion` returns `not_assessed` when its credentials are absent. `quality_service._finalize_assessment` persisted that like any other result, and `batch_population.excluded_identities` excluded on `SELECT DISTINCT canonical_id` — **any** row. Production config is `quality.enabled: true`, `mode: auto`, `max_assessments_per_run: 5`, so the scheduled workflow already reached that path; only the absent key stopped it.

Measured against committed state before the fix:

| | agent_memory | deep_research | engram | total |
|---|---:|---:|---:|---:|
| Papers holding ≥1 assessment row | 294 | 204 | 11 | **509** |
| With a completed scientific decision | 34 | 33 | 8 | **75** |
| **Excluded but never scientifically assessed** | 260 | 171 | 3 | **434** |
| Holding *only* technical failures | 8 | 7 | 0 | 15 |

Most of the 434 are 444 pre-gate `deterministic` / `quality-v1` placeholder rows that were never scientific assessments at all.

## C. Private durable-state architecture

Destination: a **dedicated private GitHub repository**, `PAPER_SCOUT_STATE_REPO`, holding one mutable release asset. Privacy is the repository's own access control — GitHub rejects an unauthenticated request for a private repository's release asset. Credential: a fine-grained PAT scoped to that one repository with `Contents: read and write` and nothing else, as `PAPER_SCOUT_STATE_TOKEN`.

Rejected on verification, not assumption:

- **GitHub Actions artifacts** — on a public repository anyone can download them from the run page.
- **Actions cache** — fork pull requests get read access to base-branch caches, and entries evict after 7 days of inactivity. Fails privacy *and* durability.
- **Reusing an existing private repo** — 17 exist; none purpose-built, and a PAT for one would over-scope.
- **Encrypted blob in the public release** — ciphertext stays permanently public and third-party-archivable; ranked last by the operator and not used.

Transport (`.github/scripts/paper_scout_state.py`) guarantees:

- refuses the public repository by name, compared case-insensitively;
- re-checks `isPrivate` on **every** write, so a repository later flipped public stops the run instead of publishing;
- no unauthenticated fallback and no fallback to the public release, at all;
- restore verifies the installed bytes against the manifest and the recorded row counts, and raises rather than reporting;
- an access failure (403/forbidden/unauthorized) is **never** read as "no snapshot yet";
- empty state is created only under an explicit `--allow-initialize`, a default-false dispatch input on both workflows;
- persist round-trips the archive into a scratch root before uploading, and removes the scratch copy and the plaintext archive on every path out, including failure;
- the PAT is declared on the two transport steps only, never at workflow or job level, so it is not handed to `actions/checkout`, `setup-python`, `upload-artifact` or `deploy-pages`.

Snapshot manifest v2 carries schema name, version, the database list, SHA-256 per database, row counts, byte sizes, creation timestamp and the source workflow/run/attempt/ref/SHA. v1 archives still restore.

**Verified on the real data:** a 250 MB three-database round-trip produced a 49.6 MB archive; digests and row counts matched exactly on restore (353 / 276 / 48 assessments, matching Batch 6).

## D. Credentials and secrets status

Checked by metadata only. No value was read, printed, hashed, logged or committed.

```text
GITHUB_GEMINI_SECRET:     MISSING
GITHUB_OPENROUTER_SECRET: MISSING
PAPER_SCOUT_STATE_TOKEN:  MISSING
PAPER_SCOUT_STATE_REPO:   MISSING  (repository variable)
```

The only repository secret is `SEMANTIC_SCHOLAR_API_KEY`. No repository variables exist. The `github-pages` environment holds no secrets.

Per §11 no credential transfer was performed. The operator elected to provision both the repository and the token themselves. The required actions:

```bash
gh repo create vernerisirva/agentmempaper-state --private --description "Private durable runtime state for Paper Scout. Not for publication."
```

Then a fine-grained PAT scoped to **only** `agentmempaper-state` with **Contents: Read and write**, and:

```bash
gh variable set PAPER_SCOUT_STATE_REPO --repo vernerisirva/agentmempaper --body "vernerisirva/agentmempaper-state"
gh secret set PAPER_SCOUT_STATE_TOKEN --repo vernerisirva/agentmempaper
gh secret set GEMINI_API_KEY --repo vernerisirva/agentmempaper
gh secret set OPENROUTER_API_KEY --repo vernerisirva/agentmempaper
```

Fine-grained PATs expire within a year, so renewal is a standing operational task.

## E. Retry-eligibility semantics

`paper_scout/operational_eligibility.py`, policy `operational-eligibility-v1`.

A row is a **completed scientific assessment** only with all three of: a semantic assessor (`llm`, `hybrid`, `manual_override`), manuscript-derived scope (`full_text`, `partial_full_text`), and an execution outcome that is not technical. Technical outcomes are `not_assessed`, `transport_failure`, `protocol_failure`, `manuscript_unavailable`, `text_coverage_failure`, `integrity_failure`, `evidence_validation_failure`, `support_verification_pending`, `credential_unavailable`.

- A completed decision — promoted **or** not — ends eligibility permanently. A non-promotion is a decision.
- A technical attempt leaves the paper retry-eligible: **3 attempts maximum, 20-hour cooldown**, then `retry_budget_exhausted` for operator review. This cross-run bound is new and separate from the frozen in-run policy (primary 1, adjudicator 2, 3 requests), which is unchanged.
- A pre-gate deterministic placeholder is neither a decision nor an attempt, so it consumes no budget.
- A missing credential writes **no row at all**, so it consumes nothing.

The exclusion policy is **versioned, not replaced**. `prior_assessment` (any row excludes) remains the default so the frozen manifests keep rebuilding byte-identically; daily operation opts into `prior_completed_assessment`. A manifest with no policy field is rebuilt under the historical one. No row was deleted or rewritten; technical history stays auditable and is reported in the selection record.

## F. Cost guard

| Bound | Value |
|---|---|
| Per-run OpenRouter ceiling | **$0.30** (`PAPER_SCOUT_OPENROUTER_RUN_CEILING_USD`) |
| Pre-spend reservation per paper | $0.05 (Batch 6 measured $0.0297779/paper; rounded up for the bounded retry) |
| Gemini | tokens only — **UNKNOWN / MSc allocation** |

The ceiling is enforced **between papers, not inside one**: a run never *starts* a paper whose expected cost would carry it past the ceiling, but one paper's calls are committed once issued. A true hard cap would need a provider-side spend limit on the OpenRouter key. This is stated in the code rather than implied. With three papers at the estimate the worst case is $0.15, half the ceiling.

Calls the provider did not price are counted in `unknown_cost_calls` rather than as $0.00, and calls whose provider cannot be attributed from the pinned model map are counted in `unattributed_calls`, so the money figure is explicitly a lower bound. An assessment that raises mid-call charges the estimate, because the provider may already have been billed for a receipt that never returned. An unparseable ceiling, a negative projection or a non-numeric value stops the run.

**Review spend this cycle: $0.622657.** Cumulative known OpenRouter: $9.56006902 → **$10.18272602** of the $20.00 ceiling.

## G. Workflow architecture

Both schedules are **disabled**, so exactly one writer owns the durable state during cutover. `paper-scout.yml` is `workflow_dispatch` only, with `deploy_only`, `run_assessment` and `allow_state_initialize` inputs; `paper-scout-backfill.yml` likewise, with `allow_state_initialize`.

Order: restore private state → verify integrity → validation suite → discovery (`--no-llm`, **no scientific credentials in that step's env**) → credential preflight → bounded assessment → build site → schema/link/exposure checks → refuse-to-publish guard → commit public output → snapshot → verify → persist privately → deploy Pages → record state hashes.

The preflight **gates** the assessment step rather than failing the job. A failed job skips the `if: success()` persist step, so a missing secret would have cost the run's discovery as well as its assessment; the run is still annotated with `::error::`. Discovery cannot enter the scientific gate by two independent mechanisms: `--no-llm`, and the scientific credentials being absent from that step's environment.

The three public-release transport scripts are **deleted**, so the old behaviour cannot be reintroduced by accident.

## H. Tests and validation

| Check | Result |
|---|---|
| Unit suite | **579 tests, OK** (505 at base; +74) |
| Relevance, all three tracks | precision 1.000, recall 1.000, 0 FP, 0 FN |
| Quality/promotion fixtures | 8/8 all tracks |
| Discovery recall | 1.000 all tracks |
| Idempotency | **0 non-timestamp differing lines** (4,288 diffs, all `generated_at`) |
| Site / schema / relative links / exposure / workflow | **0 errors** |
| Stored-assessment integrity | **0 errors** |
| Snapshot round-trip on the real 250 MB state | digests and row counts match |
| Frozen manifest reproduction vs unmodified base | **identical** |
| Every workflow step under `bash -n` | 0 syntax errors |
| `git diff --check` | clean |
| CI `offline-validation` | SUCCESS |

New regression coverage includes: the completed-assessment predicate over every outcome class; retry eligibility, cooldown, budget exhaustion and the no-duplicate-success-loop invariant; missing Gemini key, missing OpenRouter key, both missing, blank credential, disabled provider; primary auth failure, adjudicator failure and protocol failure all leaving the paper retry-eligible; a successful assessment ending eligibility; historical technical rows staying auditable; per-track and per-run bounds; cost-ceiling projection and unpriced/unattributed call accounting; snapshot corruption, partial archive, wrong manifest hash, hostile member, v1 compatibility, unflushed WAL, and non-empty state never replaced by an unverified one; public-destination refusal, missing repo/token, 403-vs-404 discrimination, download failure, explicit initialize, scratch cleanup on failure; and workflow invariants for schedule-disabled, credential scoping, preflight gating and ordering.

**No test makes a paid call.** All model interaction uses the offline double. Credential tests assert presence only.

Live behavioural check against the real databases: a run with no credentials exits 1, prints the loud error, and writes **0 rows** to all three databases. A dry run selects 2 papers — one agent_memory, one deep_research, and **zero for engram, whose quota is not transferred**.

## I. Independent review

Non-Claude reviewer via `pr-review --base origin/main`.

DeepSeek (`deepseek/deepseek-v4-pro-0813`) was tried first per policy and **exhausted its completion budget during reasoning, returning no content** — the known failure mode. Escalated to `moonshotai/kimi-k3`, which converged over six rounds.

| Round | Verdict | Blocking | Non-blocking |
|---|---|---:|---:|
| 1 | PASS_WITH_NOTES | 0 | 2 |
| 2 | PASS_WITH_NOTES | 0 | 4 |
| 3 | PASS_WITH_NOTES | 0 | 2 |
| 4 | PASS_WITH_NOTES | 0 | 5 |
| 5 | PASS_WITH_NOTES | 0 | 2 |
| 6 | PASS_WITH_NOTES | 0 | 3 |
| 7 | PASS_WITH_NOTES | 0 | **1**, a confirmable non-issue |

```text
INDEPENDENT_REVIEW  = PASS_WITH_NOTES
UNRESOLVED_BLOCKERS = 0
```

Eighteen findings were raised and seventeen were fixed. The most valuable: the state PAT sitting in a workflow-level `env` block, handing a private-repo credential to every third-party action in the job; the preflight failing the whole job and thereby skipping the persist step; the cost ceiling checked with a zero projection so it could only stop the paper *after* the overspending one; unpriced calls counted as free, which could let the guard pass while money was spent; and `cat | head || echo`, whose fallback never ran because the pipeline's status is `head`'s.

One finding was **not** accepted: that the `None` return from `assess_and_store_candidate` leaves a reservation consumed. `reserve()` is a pure pre-check that never touches `openrouter_spend_usd`, and the `None` path is reached only before any call is issued. The reviewer had flagged that file as one the per-request input budget prevented it from seeing. The resolution was to make the semantics explicit at the call site and pin them with four tests, not to change behaviour.

The final round's single finding asked to confirm that `payload_json` is guaranteed by the schema — it is `payload_json TEXT NOT NULL` in the one schema definition and present in all three live databases, so it resolves as "no issue remains" by the reviewer's own criterion.

A structural limit is recorded rather than solved: an 18 KB per-file cap and a 120 KB request budget meant 7–11 changed files were omitted from every round, so `operational_preflight.py`, `operational_run.py`, `runtime_snapshot.py` and the test modules were never reviewed directly. Several rounds' uncertainties are that limit, not the code, and they are permanently unanswerable through this tool.

## J. Production smoke

**Not run.** It requires the private state destination and both scientific secrets, none of which exist yet. `FIRST_OPERATIONAL_SMOKE = NOT_RUN`.

## K. Recurring schedule status

**Disabled**, in both `paper-scout.yml` and `paper-scout-backfill.yml`. The gate list is written into the workflow header beside the commented cron.

| Gate | Status |
|---|---|
| `PRIVATE_DURABLE_STATE_READY` | **NO** — implemented and tested; destination not provisioned |
| `GITHUB_GEMINI_SECRET` | **MISSING** |
| `GITHUB_OPENROUTER_SECRET` | **MISSING** |
| `OPERATIONAL_RETRY_ELIGIBILITY_READY` | **YES** |
| `DAILY_COST_GUARD_READY` | **YES** |
| `FULL_VALIDATION` | **PASS** |
| `INDEPENDENT_REVIEW` | **PASS_WITH_NOTES**, 0 unresolved blockers |
| `FIRST_OPERATIONAL_SMOKE` | **NOT_RUN** |

## L. Known operational backlog

1. **The public state archive is still exposed.** `paper-scout-runtime-state` still carries a 47,313,701-byte `paper-scout-state.tar.gz`, anonymously downloadable. It is deliberately retained as the only recoverable state until a private snapshot verifies, per the operator's decision; deletion will be re-confirmed first. GitHub cannot retract copies already taken, and the databases inside should be treated as disclosed.
2. **Provision the private destination and the three secrets** (§D). Nothing downstream can proceed first.
3. **Seed the private store** from current state, then run one manual smoke with `run_assessment: true` at exactly the production bounds (1/track, 3 total, $0.30), and only then enable the daily cron and re-enable the weekly backfill.
4. **The site stops updating daily** while both schedules are off. This is deliberate and lasts until cutover.
5. **434 papers become eligible again** under the operational policy. At 2 papers/day that backlog is years of work at current bounds; raising the limits is an explicit operational decision based on observed cost, not an automatic one.
6. **15 papers hold only technical failures** and will be retried up to the bounded budget; several are Zenodo records whose manuscripts may be permanently unavailable, and they will settle into `retry_budget_exhausted`.
7. **The ceiling is between papers, not within one** (§F). A provider-side spend limit on the OpenRouter key would close the residual gap.
8. **Fine-grained PAT expiry** is a standing renewal task.
9. **`ESTIMATED_OPENROUTER_USD_PER_PAPER` is calibrated on Batch 6** and should be revisited once real operational runs have their own cost history.
10. **Three Batch-6 scientific limits stand unchanged**: no `mixed`/`contradicts` corroboration was exercised live, case C rests on one live example, and the adjudicator's behaviour under disagreement is still evidenced mainly by the historical recovery. These argue for monitoring live operation, not for withholding readiness.

---

```text
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE = YES
PRIVATE_DURABLE_STATE_READY: NO
OPERATIONAL_QUALITY_ASSESSMENT_READY: NO
RECURRING_QUALITY_ASSESSMENT_ENABLED: NO
```
