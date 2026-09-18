# Gemini promotion-gate configuration — 2026-09-18

**The scientific promotion gate now runs a Gemini primary assessor against an independent DeepSeek adjudicator, merged after independent non-Claude review, with a bounded integration smoke on copied state only. Batch 4 is prepared but NOT executed, no production row changed, and no public promotion changed.**

## A. Canonical starting state

| Item | Value |
|---|---|
| Starting branch | `main`, clean working tree |
| Starting canonical SHA | `04bf6b125716e203911a3a557c8dbfab94ea9133` |
| Implementation branch | `configure-gemini-quality-gate` |
| Preserved history | Batch 3 not rerun, reinterpreted or touched |

The host Xcode license is still unaccepted, so the system Git and every `git` subprocess launched through it fail with exit 69. Homebrew Git ran all Git work, including `gh` and the reviewer's subprocesses, through an explicit PATH shim. No host setting was changed.

## B. Old scientific model pair

| Role | Model | Family | Provider |
|---|---|---|---|
| Primary assessor | `deepseek/deepseek-v4-pro-0813` | deepseek | OpenRouter |
| Independent adjudicator | `anthropic/claude-sonnet-4.6` | claude | OpenRouter |

Both roles shared one endpoint, one credential and one account. Gate version `dual-promotion-v1`. Price caps were enforced server side by OpenRouter for both roles.

Before coding, the existing abstraction was documented: a single `settings_from_env()` returning one settings object per role differing only by model string; an OpenAI-compatible `POST {base_url}/chat/completions` with bearer auth; strict `json_schema` structured output; `_reported_usage` allowlisting numeric billing telemetry; `HttpClient(retries=1)` meaning exactly one attempt; canonical response, attempt and receipt bindings in `promotion_protocol`; and persisted model identity through `primary_model` / `adjudicator_model`.

## C. New scientific model pair

| Role | Model | Family | Provider | Credential |
|---|---|---|---|---|
| Primary assessor | **`gemini-3.8-flash`** | gemini | Google | `GEMINI_API_KEY` |
| Independent adjudicator | **`deepseek/deepseek-v4-pro-0813`** | deepseek | OpenRouter | `OPENROUTER_API_KEY` |

Endpoints: `https://generativelanguage.googleapis.com/v1beta/openai` and `https://openrouter.ai/api/v1`.

No Gemini model was configured or documented anywhere in this project, and the only Gemini setting in the environment was the credential itself. Rather than invent an identifier, the 41 models visible to the MSc credential were enumerated and the four realistic pinned candidates were put to the user, who selected `gemini-3.8-flash`. It is a stable, version-pinned release rather than a preview or a rolling `*-latest` alias, so a frozen Batch-4 roster cannot be invalidated by a preview withdrawal mid-experiment.

### Provider contract, verified live before implementation

Google's OpenAI-compatibility layer was probed with the production schema and a trivial prompt, no manuscript and no scientific content:

- returns HTTP 200 and echoes `model` as exactly `gemini-3.8-flash`, satisfying the existing returned-model equality check;
- returns exactly one choice with `finish_reason: "stop"` and a string `content`, with no refusal or tool call;
- accepts the unchanged strict `json_schema`, including `additionalProperties: false`, `enum`, `maxItems`, `uniqueItems` and `minLength`, and returns all eleven required fields;
- rejects OpenRouter-only keys: `provider` and `reasoning` both fail with `400 Unknown name`;
- returns `404` for an unknown model id;
- with `reasoning_effort: 'none'`, reports `total_tokens == prompt_tokens + completion_tokens` exactly, so no thinking tokens are billed invisibly. Without it, the baseline probe billed 367 unreported tokens.

`message.extra_content` carries only an opaque `thought_signature`; only `message.content` is ever persisted.

### Per-role isolation

Each role resolves its own provider, endpoint and credential, so the two scientific judgments no longer share an account. A configured base URL must match its provider's exact host, which keeps one provider's credential off another's endpoint. A model with no known provider fails closed, and missing either credential leaves the paper unassessed with zero model calls. `PAPER_SCOUT_LLM_API_KEY` and `PAPER_SCOUT_LLM_BASE_URL` still resolve the OpenRouter role so existing runbooks keep working.

Both providers receive the same contract — temperature 0, strict JSON schema, and no hidden reasoning requested, returned or persisted — expressed with each provider's own parameter names, because each rejects the other's. OpenRouter retains its server-side price caps; Google's endpoint has no equivalent parameter, so Gemini spend is bounded by its allocation instead.

## D. Credential handling

```text
GEMINI_API_KEY:     AVAILABLE   (private ~/.zshrc; not inherited by this session)
OPENROUTER_API_KEY: AVAILABLE   (private ~/.zshrc and ~/.codex/.env; not inherited)
```

Neither value was printed, logged, hashed, partially displayed or copied. Both are shell command substitutions rather than literals, so they resolve only through the user's own interactive shell; every live call in this task ran under `zsh -ic` with the value reaching the process environment and an HTTPS `Authorization` header only. No project-local secret file was created and no credential was committed. A dedicated test asserts that neither key, the string `Authorization`, the provider thought signature, nor a hidden-reasoning marker appears in a serialized assessment.

## E. Assessment and promotion versioning

`GATE_VERSION` moved to **`dual-promotion-v2`**, so Batch 4 is identifiable as the Gemini + DeepSeek configuration. `ASSESSMENT_VERSION` stays `quality-promotion-v1` and the rubric stays `scholarly-rubric-v1`, because the rubric, response schema and evidence contract genuinely did not change — only the model pair and its providers did.

Both versions are recognized everywhere a dual-promotion row is handled: receipt validation, append-only storage keys, public card rendering, routine reassessment filtering and mode matching. A naive constant bump would instead have made every historical `dual-promotion-v1` pass fall through to the retired `scientific-gate-v1` branch and become unreadable; that was found and avoided.

Each new receipt records the provider, model and family that served each role. Because exactly one provider serves each pinned model, binding the model also binds its provider. `validate_receipt` requires the recorded `model_pair`, the per-call `provider` **and** the receipt's own `primary_provider` / `adjudicator_provider` to match the pinned mapping. A retired receipt may carry none of them, and the current gate may omit none. Same-family pairs, rolling aliases and models with no known provider are rejected by `validate_pair`.

**All 646 stored assessments still load**, including the 18 `dual-promotion-v1` rows. Because the assessment and rubric versions are unchanged, routine reassessment still excludes every historical row: of the 9 historical v1 rows checked, **0** would be picked up by a run without `--force` or `--paper-id`.

## F. Tests and validation

**404 tests pass** (`unittest`: `Ran 404 tests … OK`). Twenty-four are new and deterministic, with no live model calls:

- Gemini pass + DeepSeek pass is eligible for promotion; disagreement in either direction and mutual uncertainty are not promoted.
- A provider outage on either role is a technical outcome with the expected call count, never a scientific rejection.
- Each role receives only its own credential, and neither key appears in the other's request.
- Provider-specific generation parameters, with each provider's keys absent from the other's payload.
- Model-pair identity, providers and generation parameters persisted; ten provenance-tamper mutations each rejected.
- Legacy receipts remain readable; a retired receipt cannot borrow the newer provenance.
- A new-version row stores beside an old one without mutating it, and history appends.
- Per-provider usage and billing accounting, including the `UNKNOWN` / allocation basis.
- An adjudicator contract retry keeps provider provenance across all three calls.
- A stale endpoint override fails closed with zero calls; a returned-model alias fails closed.
- Credentials, thought signatures and hidden reasoning are never serialized.
- Existing receipt, binding and coverage-gate checks remain intact.

Full repository validation on merged `main`: 404 tests; all three tracks passing relevance (precision 1.000, recall 1.000), quality/promotion fixtures 8/8, discovery recall 1.000 and idempotency; offline site builds for all three libraries; `check_paper_scout_site.py` reporting **0 errors** across site, schema, link, exposure and workflow checks; generated file-size checks; `git diff --check` clean; all three workflow YAML files and the new protocol manifest parsing; three-database snapshot preparation with `integrity_check=ok`; 646 historical assessments readable; and no credential-shaped content in any change.

## G. PR and independent review

| Item | Value |
|---|---|
| PR | https://github.com/vernerisirva/agentmempaper/pull/38 |
| CI | `offline-validation` pass; `MERGEABLE` / `CLEAN` |
| Configured reviewer | `deepseek/deepseek-v4-pro-0813` — **failed to converge**, no verdict |
| Escalated reviewer | `moonshotai/kimi-k3` — three rounds, all **PASS_WITH_NOTES, 0 blocking findings** |
| Reviewed candidate | `2f92b3d2d32be30c9cf5915a1afdf73ba8979304` (equals merged HEAD) |
| Merge SHA | **`40a203eeeca232d076054ad569093bc0f974b1ad`** |
| Final canonical main | `40a203eeeca232d076054ad569093bc0f974b1ad` |

No Claude-family model reviewed this change. DeepSeek consumed all 16,384 completion tokens on reasoning and returned zero visible tokens, the same mechanism that blocked it in the previous cycle.

Round one raised two valid notes, both fixed rather than accepted: provider fields were recorded but never validated, and the tamper test silently skipped exactly that mutation, making it vacuous. Round two's notes were checked against running code — the "crash on stale endpoint" concern is a **false positive**, since a host mismatch fails closed as a technical `protocol_failure` with zero calls and no credential stored, unchanged from the previous configuration; the retired-pair mode mismatch is real but bounded, with 0 of 9 historical rows reachable by a routine run. Both are now regression-tested. Round three's remaining notes are cosmetic: the billing dict carries `billing_cost` only when the cost is genuinely unknown, which is the deliberate marker, and base-URL overrides are validated by hostname because that is the property determining where a credential is sent. **Unresolved blockers: 0.**

## H. Bounded integration smoke

Three already-seen historical papers, chosen for complete cached manuscripts, known prior evidence and three genuinely different prior outcomes. **Every run executed against copied databases**, with each track's state redirected by `PAPER_SCOUT_*_STATE_PATH`, so no production row was reachable.

| Paper | Prior outcome | Gemini primary | DeepSeek adjudicator | Smoke result | Calls |
|---|---|---|---|---|---:|
| Causal Path Alignment | valid promotion | `pass` | `pass` | pass | 2 |
| Immune world model | disagreement, not promoted | `pass` | `pass` | pass | 2 |
| Water sustainability book | technical coverage failure | — | — | `text_coverage_failure`, `not_assessed` | **0** |

Verified end to end: Gemini authentication; valid primary structured output against the unchanged strict schema; independent DeepSeek adjudication; `canonical-response-v1` receipts with `provenance_status=pass`; provider and `model_pair` provenance with `independent_families=true`; persistence under `dual-promotion-v2` appended beside the existing `dual-promotion-v1` rows without mutating them; and per-provider token and cost accounting. The coverage gate still fires **before** any Gemini call, so the front-matter-only book consumed zero model calls.

These are technical integration checks, **not scientific re-evaluations and not evidence about historical truth**. One observation is recorded honestly: on the immune-world-model manuscript the new pair agreed on `pass` where the retired pair disagreed. That is a single unreplicated technical observation on copied state; it does not revise, and must not be read as revising, the historical outcome. It is also a reason to treat the new pair's calibration as unestablished until an unseen batch runs.

**No historical outcome was changed. No public promotion changed.** Production database hashes are byte-identical to their pre-smoke baseline, production still holds 646 assessments, and production contains **0** `dual-promotion-v2` rows. Smoke rows exist only in the scratch copies.

## I. Cost estimate for Batch 4

Per assessable paper, from the two smoke papers that made calls:

| Role | Input tokens | Output tokens | Monetary |
|---|---:|---:|---|
| Gemini primary (Google) | 32,355 | 1,007 | **UNKNOWN**, `covered_by_msc_allocation` |
| DeepSeek adjudicator (OpenRouter) | 29,760 | 447 | **$0.03134568** |

| Batch size | Gemini in / out | DeepSeek in / out | DeepSeek cost | Gemini cost |
|---|---|---|---:|---|
| 5 papers | 161,773 / 5,033 | 148,800 / 2,235 | **$0.1567284** | UNKNOWN, allocation |
| 10 papers | 323,545 / 10,065 | 297,600 / 4,470 | **$0.3134568** | UNKNOWN, allocation |
| 15 papers | 485,318 / 15,098 | 446,400 / 6,705 | **$0.4701852** | UNKNOWN, allocation |

Expected total monetary outlay is the DeepSeek column; Gemini usage is recorded in tokens against the MSc allocation. The endpoint reports no charge and this project has not established the allocation's effective rate, so **no monetary amount is fabricated and the usage is not assumed to be free**. The projection excludes adjudicator contract retries, which add at most one further adjudication per paper. Given the eligible population, the realistic maximum is 10 papers, so roughly **$0.31** of DeepSeek adjudication plus the Gemini allocation.

### This task's costs

| Component | Calls | Cost |
|---|---:|---:|
| DeepSeek review, non-convergent | 1 | $0.08903532 |
| Kimi review round 1 | 1 | $0.0736632 |
| Kimi review round 2 | 1 | $0.0763182 |
| Kimi review round 3 | 1 | $0.0576062 |
| **Engineering review subtotal** | 4 | **$0.29662292** |
| Smoke, DeepSeek adjudications | 2 | $0.06269136 |
| Smoke, Gemini primaries | 2 | UNKNOWN, allocation (64,709 in / 2,013 out) |
| Provider contract probes, Gemini | 8 | UNKNOWN, allocation (tiny fixed prompts) |
| Model listing | 1 | no charge (metadata) |

Known monetary total for this task: **$0.35931428**. Prior charged/reserved was $5.72160579, giving a cumulative **$6.08092007** against the shared $10 ceiling. Gemini charges are unknown rather than zero and are attributed to the MSc allocation.

## J. Batch-4 eligible population

Batch 4 evaluates the population the system can genuinely assess:

> high relevance **AND** never scientifically quality-assessed **AND** never adjudicated **AND** not suppressed **AND** a complete manuscript can be acquired **AND** the manuscript coverage gate returns PASS.

The exclusion set is 478 canonical ids, unioned across every record proving a paper was already seen: all persisted assessment rows in all three databases, the frozen Batch-3 roster whether attempted or not, the Batch-1 calibration identities, the `all_prior_assessed_ids` manifest, and every id with saved operator run artifacts — which correctly excludes papers whose primary call started but stored no row. DOI, arXiv and OpenAlex aliases are excluded across tracks.

| Track | High relevance | Not suppressed | **Metadata-eligible** |
|---|---:|---:|---:|
| agent_memory | 657 | 657 | **526** |
| deep_research | 254 | 254 | **113** |
| engram | 11 | 11 | **0** |
| **Total** | | | **639** |

The population is frozen by commitment hash over each track's sorted eligible ids, so it is verifiable later without selecting or exposing any identity: `agent_memory` `ca72f229…`, `deep_research` `bf6731a8…`, `engram` `e3b0c442…` (the empty-set digest).

**Full-manuscript availability is an explicit execution eligibility condition, not a scientific-quality filter.** It is deterministic, uses no model and inspects no scientific quality. A paper failing acquisition or the coverage gate is recorded as **outside** the Batch-4 evaluation population and replaced by the next eligible paper in deterministic order, rather than consuming a roster slot as "unavailable" — the failure mode that left Batch 3 with 8 of 16 slots spent on unavailable manuscripts.

Consequently, **Batch-4 generalization claims will apply to "high-relevance papers with retrievable, coverage-valid manuscript evidence"**, not to all discovered papers, and say nothing about papers whose manuscripts cannot be acquired.

## K. Batch-4 protocol — prepared, NOT executed

Frozen in [`experiments/manifests/batch-4-protocol-2026-09-18.json`](../../experiments/manifests/batch-4-protocol-2026-09-18.json) against code SHA `40a203ee`.

- Maximum **5 papers per track**, **15 total**; given the population the realistic maximum is 10.
- Selection is deterministic from the eligible population using the existing offline research ranking, then the acquisition and coverage filter, taking the first papers that pass. No likely-success selection, no availability-biased reordering, no author/institution/venue filter, no quota transfer, no replacement for scientific outcomes.
- The roster freezes **before any model call**; the audit sample freezes **before any outcome**.
- No code changes and no manual output corrections mid-batch. No target promotion rate.
- The promotion rule is unchanged: high relevance AND primary PASS AND independent adjudicator PASS AND deterministic provenance/integrity PASS AND not suppressed. Disagreement or technical failure means not promoted.

**No identity was selected, no manuscript was acquired and no scientific field was inspected during this preparation.** Batch 4 was not run, and no recurring production assessment was started.

## L. Private durable-state backlog

Unchanged and not addressed here, by instruction. The configured remote preservation mechanism publishes to a public GitHub release and remains unacceptable for private assessment state. Snapshots were prepared and verified **locally only**, all three with `integrity_check=ok`. No database, snapshot or raw execution record was committed, uploaded to a release, or published to Pages; `.gitignore` continues to exclude `data/**/*.sqlite3`, `data/cache/` and `*.pdf`. Private remote durable-state storage remains a separate operational backlog item.

No Pages deployment occurred in this task and no public artifact changed, because no production assessment was created: public output is identical to the state published by the previous cycle.

## Readiness

The gate is wired, reviewed, merged and verified end to end against both live providers, with provenance that makes the model pair auditable and a coverage gate that still blocks before any paid call. What has **not** been established is scientific calibration: the new pair has never run on an unseen population, and the one smoke divergence on the immune-world-model manuscript is a reason for caution rather than confidence. Batch 4 is the experiment that would test it, and it has deliberately not been run.

```text
GEMINI_PRIMARY_GATE_READY: YES
QUALITY_PROMOTION_GATE_READY_FOR_BATCH_4: YES
```

These state that the configuration is ready to execute the frozen Batch-4 protocol. They do not assert promotion precision, scientific correctness or operational readiness, which remain unestablished.

```text
ORIGINAL_BATCH_3_GENERALIZATION_RESULT = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_CHECK = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_V2_CHECK = PASS
BATCH_3_REMAINING_HOLDOUT_RESULT = FAIL
MANUSCRIPT_COVERAGE_GATE_READY: YES
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
```
