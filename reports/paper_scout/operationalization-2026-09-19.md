# Operationalization — 2026-09-19

**Two defects stood between the validated gate and safe recurring operation, and both are fixed and merged. A technical failure permanently retired a paper: 434 of the 509 papers holding assessment rows had never received a scientific decision yet were already excluded forever. And the runtime state — all three databases, including 18 rows of raw model payloads — answered an unauthenticated request with HTTP 200 from a public release.**

**The cutover ran on 2026-09-19. Private durable state is live and verified end to end, and the public archive is deleted and confirmed unreachable. A first smoke failed on a malformed secret and changed nothing; after the secrets were re-set, the second smoke completed all 22 steps green. Every operational invariant verified — except one: both selected papers had unretrievable manuscripts, so the run made ZERO Gemini and ZERO DeepSeek calls. The scientific path has still never executed in Actions, so recurring assessment stays DISABLED.**

```text
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE = YES   (Batch 6, unchanged)
PRIVATE_DURABLE_STATE_READY:          YES      — seeded, verified, clean-restored, and round-tripped by a real run
OPERATIONAL_QUALITY_ASSESSMENT_READY: PARTIAL  — pipeline proven; the model path itself is still unexercised
FIRST_OPERATIONAL_SMOKE:              PARTIAL  — 22/22 steps green, 0 model calls made
PUBLIC_STATE_ARCHIVE_REMOVED:         YES      — deleted and confirmed unreachable anonymously
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

At the time this work began:

```text
GITHUB_GEMINI_SECRET:     MISSING
GITHUB_OPENROUTER_SECRET: MISSING
PAPER_SCOUT_STATE_TOKEN:  MISSING
PAPER_SCOUT_STATE_REPO:   MISSING  (repository variable)
```

All four were provisioned by the operator later the same day and verified present by name; see §M. One of them carries a malformed value, which is what the smoke failed on.

```text
GITHUB_GEMINI_SECRET:     PRESENT   2026-09-19T16:57:04Z
GITHUB_OPENROUTER_SECRET: PRESENT   2026-09-19T16:57:13Z
PAPER_SCOUT_STATE_TOKEN:  PRESENT   2026-09-19T16:56:39Z   (value malformed — see §M)
PAPER_SCOUT_STATE_REPO:   PRESENT   vernerisirva/agentmempaper-state
```

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

**Run twice.** The first attempt FAILED at its first gate; the second completed all 22 steps green but made no model call, so the result is `FIRST_OPERATIONAL_SMOKE = PARTIAL`. Detail for both is in §M.

First attempt: It stopped on `HTTP 401: Bad credentials` restoring private state, skipped every subsequent step, and changed nothing — no assessment, no commit, no state write. The cause is a repository secret holding the literal value `-`, which is a provisioning error rather than a code defect. Full detail, evidence and the damage-free verification are in §M.

Per policy the run was **not** retried and **not** silently patched, and the schedules stay disabled.

## K. Recurring schedule status

**Disabled**, in both `paper-scout.yml` and `paper-scout-backfill.yml`. The gate list is written into the workflow header beside the commented cron.

| Gate | Status |
|---|---|
| `PRIVATE_DURABLE_STATE_READY` | **YES** — seeded, verified and clean-restored from the private repo |
| `GITHUB_GEMINI_SECRET` | **PRESENT** |
| `GITHUB_OPENROUTER_SECRET` | **PRESENT** |
| `OPERATIONAL_RETRY_ELIGIBILITY_READY` | **YES** |
| `DAILY_COST_GUARD_READY` | **YES** |
| `FULL_VALIDATION` | **PASS** |
| `INDEPENDENT_REVIEW` | **PASS_WITH_NOTES**, 0 unresolved blockers |
| `FIRST_OPERATIONAL_SMOKE` | **PARTIAL** — 22/22 green, 0 model calls; the one open gate |

## L. Known operational backlog

1. **The scientific model path has never executed in Actions.** Preflight proves a credential is present, not that it works. This is the only gate still open before the cron can be enabled.
2. **Throughput at current bounds is well under 2 papers/day.** Acquisition succeeds for roughly a quarter to a third of top-ranked candidates, and selection does not pre-check retrievability. Walking a few candidates per track before giving up, as the Batch-6 roster build did, is the obvious remedy and is an explicit operational decision, not an automatic one.
2. **The public archive is deleted** (§M), but it recorded `downloadCount: 1` and GitHub cannot retract copies already taken. Treat the databases it held as disclosed.
3. **Re-run the smoke once** after the secret is corrected, at exactly the production bounds (1/track, 3 total, $0.30), and only then enable the daily cron and re-enable the weekly backfill.
4. **Consider a cheap credential-only dispatch path** so a bad secret is caught without consuming a full production run. The smoke's fail-closed behaviour is correct but expensive to use as a credential test.
4. **The site stops updating daily** while both schedules are off. This is deliberate and lasts until cutover.
5. **434 papers become eligible again** under the operational policy. At 2 papers/day that backlog is years of work at current bounds; raising the limits is an explicit operational decision based on observed cost, not an automatic one.
6. **15 papers hold only technical failures** and will be retried up to the bounded budget; several are Zenodo records whose manuscripts may be permanently unavailable, and they will settle into `retry_budget_exhausted`.
7. **The ceiling is between papers, not within one** (§F). A provider-side spend limit on the OpenRouter key would close the residual gap.
8. **Fine-grained PAT expiry** is a standing renewal task.
9. **`ESTIMATED_OPENROUTER_USD_PER_PAPER` is calibrated on Batch 6** and should be revisited once real operational runs have their own cost history.
10. **Three Batch-6 scientific limits stand unchanged**: no `mixed`/`contradicts` corroboration was exercised live, case C rests on one live example, and the adjudicator's behaviour under disagreement is still evidenced mainly by the historical recovery. These argue for monitoring live operation, not for withholding readiness.

## M. Cutover, 2026-09-19

Provisioning was completed by the operator: private repository `vernerisirva/agentmempaper-state` (`isPrivate: true`), repository variable `PAPER_SCOUT_STATE_REPO`, and secrets `PAPER_SCOUT_STATE_TOKEN`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`. Verified by metadata only; no secret value was read, printed or logged at any point.

### A–B. Seed and snapshot verification

The private repository was empty, so a release could not be tagged; a README was committed first, stating that the repository must never be made public. The local runtime state was then verified (`integrity_check=ok`, no WAL on any database) and persisted.

| Database | SHA-256 | Rows (papers / assessments / runs) | Bytes |
|---|---|---:|---:|
| `data/paper_scout.sqlite3` | `3b27f9fa545e6b72…` | 18,343 / **353** / 124 | 190,771,200 |
| `data/deep_research/paper_scout.sqlite3` | `5ee3ca54ae0535ca…` | 2,395 / **276** / 87 | 52,854,784 |
| `data/engram/paper_scout.sqlite3` | `a04493c09b9c385d…` | 306 / **48** / 14 | 7,217,152 |

Archive: 49,613,023 bytes, asset digest `sha256:48635237611a7e26…`. Manifest **v2**, schema `paper-scout-state-snapshot`, created `2026-09-19T16:59:51Z`, database list complete. The pre-upload round-trip verification passed for all three databases before anything was uploaded.

**Source metadata is empty** in this snapshot (`workflow`, `run_id`, `sha` all `""`), because the seed was performed locally rather than from Actions. That is expected and will populate on the first successful workflow persist.

### C–D. Clean restore from the private repository

Downloaded fresh from `vernerisirva/agentmempaper-state` into an empty root and verified independently:

| Database | manifest | restored | live | bytes equal | assessments |
|---|---|---|---|---|---:|
| `data/paper_scout.sqlite3` | `3b27f9fa` | `3b27f9fa` | `3b27f9fa` | yes | 353 |
| `data/deep_research/paper_scout.sqlite3` | `5ee3ca54` | `5ee3ca54` | `5ee3ca54` | yes | 276 |
| `data/engram/paper_scout.sqlite3` | `a04493c0` | `a04493c0` | `a04493c0` | yes | 48 |

File sizes matched the manifest and no extra files were present. `STEP_D_VERIFICATION: PASS`.

Privacy proof: unauthenticated requests to the private repository, its releases API and its release asset all return **404**.

### E. Deletion of the public archive

Deleted only after the seed and clean restore both verified. Removed: release `paper-scout-runtime-state` on `vernerisirva/agentmempaper` (created 2026-08-12), its asset `paper-scout-state.tar.gz` (47,313,701 bytes, `sha256:fb54850bbc973321…`), and the tag.

**The asset kept serving for ~90 seconds after deletion.** The API returned 404 immediately, but `github.com/.../releases/download/...` continued issuing freshly signed CDN redirects and served real gzip content to a ranged request. Only a content fetch reveals this; a status-code check alone would have reported success while the data was still public. It cleared on its own, which identifies it as propagation lag rather than a persistent blob.

Final unauthenticated state: the download URL returns a 9-byte `Not Found` with no CDN redirect, the tag, asset id and release page all 404, the releases list is empty, and the repository tree contains no `.sqlite3` or `.tar.gz`. **`PUBLIC_STATE_ARCHIVE_REMOVED: YES`.**

The asset recorded `downloadCount: 1` at deletion. The probes run during this work are the most likely cause, but a third-party fetch cannot be excluded, and GitHub cannot retract copies already taken. Treat the contents as disclosed.

### First operational smoke — FAIL

Run [35456902376](https://github.com/vernerisirva/agentmempaper/actions/runs/35456902376), `workflow_dispatch` on `2d6a0d463` with `run_assessment: true`.

It failed at step 5 of 22, **Restore private Paper Scout state**:

```text
cannot read vernerisirva/agentmempaper-state; check PAPER_SCOUT_STATE_TOKEN scope:
HTTP 401: Bad credentials (https://api.github.com/graphql)
```

Every subsequent step was skipped: integrity verification, validation, discovery, preflight, assessment, site build, commit, snapshot, persist and Pages. **This is the fail-closed design behaving correctly** — the run stopped at its first gate rather than proceeding on state it could not account for.

Nothing was damaged, confirmed after the failure:

| Check | Result |
|---|---|
| Private store | unchanged — digest `sha256:48635237…`, 49,613,023 bytes |
| Local databases | payload fingerprints byte-identical to the pre-run capture |
| Assessment rows | 353 / 276 / 48, `max_id` 356 / 317 / 85 — unchanged |
| Public repository | no commits; `origin/main` still `2d6a0d463` |
| Schedules | still disabled |

**Diagnosis: a repository secret holds the literal value `-`.** GitHub masks secret values in logs, and the smoke's log shows every hyphen replaced by `***` — `bash -e {0}` renders as `bash ***e {0}`, and `--report`, `setup-python` and `agentmempaper-state` are all mangled the same way. A control against run 35430534043, from before these secrets existed, shows `bash -e {0}`, `setup-python` and `upload-artifact` rendering normally, so the masking began with the new secrets. Combined with `401 Bad credentials` on the very first authenticated call, `PAPER_SCOUT_STATE_TOKEN` is the probable holder, though the masking alone cannot distinguish which of the three it is.

This is a provisioning error, not a code defect, and it cannot be diagnosed further without reading a secret value, which was not done.

One robustness observation recorded but **not acted on**: `gh repo view --json` and `gh release view --json` both route through `POST /graphql` rather than REST. That is visible in the error URL. It is not the cause here — a token that is the literal `-` fails against any API — and changing the transport on an unconfirmed theory would add a variable to the next run rather than remove one.

### Second operational smoke — 22/22 green, but the model path was never reached

All three secrets were re-set interactively; timestamps confirmed moved (`16:56:39Z → 17:28:51Z`, `16:57:04Z → 17:29:21Z`, `16:57:13Z → 17:30:31Z`) without reading any value. Run [35458347884](https://github.com/vernerisirva/agentmempaper/actions/runs/35458347884) on `2d51db5cd`, `run_assessment: true`, 17:31:23Z → 17:39:04Z, **conclusion `success`, all 22 steps green.**

The 401 is resolved, which also settles the recorded GraphQL risk: `gh repo view --json` issues `POST /graphql` and a valid fine-grained PAT authenticated against it without trouble. **No transport rewrite is needed**, and the note in §M stands as a recorded non-issue rather than an open risk.

Verified during the run:

| Smoke criterion | Result |
|---|---|
| Private state restored | **yes** — step 5, then integrity verified at step 6 |
| Credential preflight succeeds | **yes** — `credentials_present`, both roles, no value logged |
| Discovery cannot perform scientific assessment | **yes** — `--no-llm`, and no scientific credential in that step's env |
| Eligibility uses completed-assessment semantics | **yes** — engram contributed 0 candidates, all 8 high-relevance papers already decided |
| Technical outcomes stay retry-eligible | **yes, demonstrated live** — both new rows are `manuscript_unavailable`, neither is a completed assessment |
| Candidate bounds respected | **yes** — 1 agent_memory + 1 deep_research, 0 engram, no quota transfer |
| Cost guard respected | **yes**, but trivially — $0.00 of the $0.30 ceiling |
| **Gemini and DeepSeek calls succeed** | **NOT EXERCISED — 0 calls** |
| Assessment history append-only | **yes** — all 353 / 276 / 48 pre-existing rows byte-identical |
| Site generation | **yes** |
| Private snapshot persists and restores | **yes** — `sha256:11d8c33af5a5bc58…`, clean-restored into a fresh root afterwards |
| No database, snapshot or raw payload published | **yes** — 0 tracked `.sqlite3`/`.tar.gz`, 0 public releases, 0 `raw_content`, 0 credential-shaped strings |
| Pages deployment | **yes** — deployed, live site HTTP 200 |

Snapshot provenance is now populated, which it could not be for the local seed:

```json
{"workflow": "Paper Scout", "run_id": "35458347884", "run_attempt": "1",
 "repository": "vernerisirva/agentmempaper", "ref": "refs/heads/main",
 "sha": "2d51db5cd056f103778c4f3aefab532c3ddf0480"}
```

State moved as expected: papers 18,343 → 18,530, 2,395 → 2,437, 306 → 338; assessments 353 → 354 and 276 → 277, engram unchanged at 48.

### Why no model call happened, and why it matters

The two selected papers were `doi:10.5281/zenodo.22837961` (agent_memory rank 1) and `doi:10.64898/2026.09.11.751076` (deep_research rank 1). Both returned `manuscript_unavailable` during acquisition, which happens **before** the gate issues any request, so neither model was contacted.

That is correct behaviour and it exercised the retry design properly — both rows are technical, neither is a completed assessment, and both papers return to eligibility after the 20-hour cooldown. But it leaves the single most expensive assumption untested: **the preflight only checks that a credential is present, not that it works.** A wrong or expired `GEMINI_API_KEY` or `OPENROUTER_API_KEY` would pass preflight exactly as it did here and fail at call time. Enabling the cron now would mean the first real scientific call in production happens unattended.

**This is also an operational throughput finding.** Selection takes the top eligible candidate per track and does not pre-check retrievability, because that needs network acquisition. Batch 6 measured how often acquisition succeeds by walking the same ranking: 5 of 14 for agent_memory and 5 of 20 for deep_research, roughly 25–36%. With one candidate per track per day, **most daily runs will assess nothing**, and each unretrievable paper consumes three daily slots over three runs before parking at `retry_budget_exhausted`. The gate is not broken and no eligibility is lost, but realistic throughput at current bounds is well under two papers a day.

---

```text
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE = YES
PRIVATE_DURABLE_STATE_READY: YES
OPERATIONAL_QUALITY_ASSESSMENT_READY: PARTIAL
FIRST_OPERATIONAL_SMOKE: PARTIAL
PUBLIC_STATE_ARCHIVE_REMOVED: YES
RECURRING_QUALITY_ASSESSMENT_ENABLED: NO
```
