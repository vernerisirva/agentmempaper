# Batch 6 — final unseen generalization evaluation, 2026-09-19

**Ten unseen papers went through the frozen evaluation-independence gate with zero code, prompt, rubric, schema, model or configuration changes, zero manual corrections, zero retries and zero technical failures. Eight were promoted and two withheld, every promotion is scientifically defensible on audit, and the one paper with genuine material evaluator reuse was promoted on a real external benchmark that moves the right way — the exact case the recovery could not exercise live. `BATCH_6_GENERALIZATION_RESULT: PASS`. Historical state is append-only and byte-identical for all 667 pre-existing rows.**

## A. Frozen canonical state

| Item | Value |
|---|---|
| Branch / working tree | `main`, clean, up to date with `origin/main` |
| `BATCH_6_CODE_SHA` | **`0e7c2387cdcab4406633245abf2ff315629232b3`** |
| Tree SHA | `08cc7bbd42781f220d59e1dfacb707e6e6a01a33` |
| Evaluation-independence merge | `3acca4328` (PR #40), present |
| Recovery report | committed at `0e7c2387c` |
| Batch-6 assessments before start | **0** — no `dual-promotion-v3` row anywhere in production |
| Implementation source changed during Batch 6 | **none** — `git status` over `paper_scout/`, `tests/`, `config/`, `.github/` empty at start and end |

**Recurring production assessment is not running.** The daily workflow (`cron 20 6 * * *`) runs discovery, relevance and site builds. It supplies no `GEMINI_API_KEY`, and the pinned primary assessor resolves its credential from that variable alone, so `settings_from_env()` returns `None` and the gate short-circuits with **zero model calls**. No scheduled job performs scientific assessment. No crontab or launch agent exists.

### Scientific model pair, read from running code

| Role | Provider | Model | Family | Host | Credential |
|---|---|---|---|---|---|
| Primary assessor | google | **`gemini-3.8-flash`** | gemini | `generativelanguage.googleapis.com` | `GEMINI_API_KEY` (MSc) |
| Independent adjudicator | openrouter | **`deepseek/deepseek-v4-pro-0813`** | deepseek | `openrouter.ai` | `OPENROUTER_API_KEY` |

`independent_families = True`. Claude was orchestration only and served neither scientific role.

```text
GEMINI_API_KEY:     AVAILABLE   (private interactive shell; not inherited by this session)
OPENROUTER_API_KEY: AVAILABLE   (private interactive shell; not inherited by this session)
```

Neither value was printed, echoed, hashed, partially displayed, serialized, logged or committed, and no project-local secret file was created.

### Frozen versions

```text
GATE_VERSION             = dual-promotion-v3
ASSESSMENT_VERSION       = quality-promotion-v2
RUBRIC_VERSION           = scholarly-rubric-v2
INDEPENDENCE_CONTRACT    = evaluation-independence-v1
RECEIPT_VERSION          = canonical-response-v1
MODEL_PAIR_VERSION       = model-pair-v1
RETRY_POLICY             = adjudicator-contract-retry-v2
evidence context         = block-evidence-v2      coverage gate = coverage-v2
RUBRIC sha256            = ad7311c2c1a846d7…  (3,235 chars)
primary schema sha256    = 0ede05ae68dc80e9…
adjudicator schema sha256= 1ca6421a45073427…
generation               = temperature 0, max_output_tokens 4096, max_request_bytes 300000
reasoning                = google reasoning_effort=none | openrouter reasoning{enabled:false, exclude:true}
attempts                 = primary 1, adjudicator 2; total request limit 3
MAX_EVIDENCE_IDS         = 24
```

### Evaluation-independence invariant, verified from code before any manuscript

Both roles are required to answer an identical seven-field dimension (`signal_reuse`, `independent_corroboration`, `corroboration_direction`, `concern`, plus the optimization, final-evaluation and corroboration prose), and it is `required` in both role schemas. The frozen behaviour:

| | Case | Declarations the contract permits | Can that role pass? |
|---|---|---|---|
| A | material reuse + no corroboration | `major` only | **No** |
| B | material reuse + contradicting evidence | `major` only | **No** |
| C | material reuse + supporting corroboration | none / moderate / major | **Yes** |
| D | judge used only for final evaluation | none / moderate / major | **Yes** |
| E | independent final evaluation | none / moderate / major | **Yes** |
| — | material reuse + unresolved corroboration | `major` only | **No** |
| — | unresolved reuse, nothing reported | moderate / major | Yes (not `none`) |

Nothing was modified.

## B. Eligible population

Built with the committed `paper_scout batch-population` implementation only, offline, with build time pinned to `2026-09-19T00:00:00` and the Batch-2, Batch-3, Batch-4 **and Batch-5** frozen rosters supplied as exclusions.

| Track | Ranked (high relevance) | Eligible | Excluded | Population SHA-256 |
|---|---:|---:|---:|---|
| agent_memory | 319 | **193** | 126 | `17f81ab77720c74f…` |
| deep_research | 133 | **32** | 101 | `3749a6bc7d02be58…` |
| engram | 8 | **0** | 8 | `e3b0c44298fc1c14…` (empty-set digest) |

```text
BATCH_6_POPULATION_SHA256 (manifest) = 12b782b00ebb72fcba978ec0f091727f6d802c92b3d2ccc5d14d32767cd245c4
```

Exclusions: 234 `prior_assessment` (a persisted assessment row in **any** track, which is what excludes calibration, Batches 2–5 and every diagnostic and recovery paper), 1 `frozen_roster`, 0 `suppressed`. All three tracks were scanned for exclusions; none lacked state.

Eligibility used relevance, prior assessment, prior adjudication, suppression and roster membership only. **No author, institution, company, venue, expected strength or expected pass likelihood entered it, and no scientific quality was inspected.** Manuscript retrievability and coverage are execution eligibility, applied afterwards to the frozen ordered list.

Sanity check: eligible counts fall by exactly 5 per track against Batch 5 (198 → 193, 37 → 32), which is precisely the ten Batch-5 papers becoming `prior_assessment`.

### Exact reproduction

```text
agent_memory   ordered_ids_match=True  population_sha256_match=True  stored=193 rebuilt=193
deep_research  ordered_ids_match=True  population_sha256_match=True  stored=32  rebuilt=32
engram         ordered_ids_match=True  population_sha256_match=True  stored=0   rebuilt=0
self_consistent=True  sources_match=True  reproduced=True
stored  = 12b782b00ebb72fcba978ec0f091727f6d802c92b3d2ccc5d14d32767cd245c4
rebuilt = 12b782b00ebb72fcba978ec0f091727f6d802c92b3d2ccc5d14d32767cd245c4
```

Identical ordered identifiers, counts, exclusions and digest, compared element by element rather than by hash alone.

## C. Frozen roster

Deterministic prefix of the frozen ordered population, filtered by the execution-eligibility walk (production acquisition and coverage gate, read-only, no model call, nothing persisted).

| Track | Eligible | Walked | Acquisition/coverage failed | Selected |
|---|---:|---:|---:|---:|
| agent_memory | 193 | 14 | 9 | **5** |
| deep_research | 32 | 20 | 15 | **5** |
| engram | 0 | 0 | 0 | **0** |

```text
BATCH_6_ROSTER_SHA256 = 047db6e63c6a195ccc15f6291aa21cea769c5444b8fbd22178e00a37398c2678
```

| # | Track | Rank | Canonical id | Title | Manuscript |
|---|---|---:|---|---|---|
| 1 | agent_memory | 54 | `doi:10.48550/arxiv.2609.00237` | Learning What to Retain: Gated-Memory Routing… | `d886bf6edd8f` |
| 2 | agent_memory | 58 | `doi:10.48550/arxiv.2608.30177` | Understanding Stage-Wise Utility-Risk Trade-offs… | `534d19430d42` |
| 3 | agent_memory | 65 | `doi:10.1088/2632-2153/ae9fb7` | An autonomous agentic framework for cross-campaign… | `479f9340406c` |
| 4 | agent_memory | 66 | `doi:10.48550/arxiv.2608.26983` | GraphMemix: Query-Aware Evidence Forests… | `036a0429dfc0` |
| 5 | agent_memory | 68 | `arxiv:2608.26807` | Behavior2Trip: Towards Personalized Travel Planning… | `02594612eab1` |
| 6 | deep_research | 116 | `doi:10.48550/arxiv.2606.31478` | One Reflection Is Not Enough: Self-Correcting… | `a58f10624eab` |
| 7 | deep_research | 117 | `openalex:W7167154310` | Agentic-Ideation: Sample Efficient Agentic Trajectories… | `48ec3219304e` |
| 8 | deep_research | 118 | `openalex:W7167154699` | The Calibration Turn in AI-Assisted Research… | `9e209f7d7e15` |
| 9 | deep_research | 120 | `openalex:W7166902155` | Hephaestus: Toward a Cybersecurity AI Scientist | `afe032b6627d` |
| 10 | deep_research | 121 | `openalex:W7166901874` | DEEPMED Search: An Open-Source Agentic Platform… | `1815fc62c5ce` |

**Prior assessment count, checked under every supported alias (canonical, DOI, arXiv, OpenAlex, Semantic Scholar, normalized title) across all three databases: 0 for all ten.** Prior adjudication count: 0 for all ten.

**Engram has zero eligible papers, so zero Engram papers were selected and no quota was transferred to another track.** No paper was selected, substituted or replaced manually; the roster was immutable from the first scientific call onward.

## D. Frozen audit sample

Frozen before any outcome was observed. Both tracks have five selected papers, so first / middle / last:

```text
agent_memory : doi:10.48550/arxiv.2609.00237  doi:10.1088/2632-2153/ae9fb7  arxiv:2608.26807
deep_research: doi:10.48550/arxiv.2606.31478  openalex:W7167154699          openalex:W7166901874
```

Plus, per protocol, every promoted paper and every model disagreement.

## E. Cost estimate before execution

Basis: Batch 5's ten-paper actuals scaled by the measured v2→v3 gate uplift (the diagnostic and recovery ran identical manuscripts for $0.15003843 and $0.16644656).

| Item | Expected |
|---|---|
| Gemini primary calls / in / out | 10 / 386,126 / 11,705 |
| Gemini monetary cost | **UNKNOWN / MSc allocation** |
| DeepSeek calls / in / out | 10 / 358,182 / 4,969 |
| DeepSeek expected OpenRouter cost | **$0.33102145** |
| DeepSeek worst case (max retries) | $0.49653218 |
| Cumulative known OpenRouter before | $9.26229011 |
| Projected cumulative, worst case | $9.75882229 |
| Authorized ceiling | $20.00 — **proceed** |

## F. Per-paper automatic outcomes

```text
FROZEN_OUTCOMES_SHA256: e4deb031d802f325348c441ff1c67e8e2d4497abededd7c35a1611bb8471d659
```

| # | Track | Gemini | DeepSeek | Blockers | Promotion | Outcome | Calls | Retries |
|---|---|---|---|---:|---|---|---:|---:|
| 1 | agent_memory | `pass` | `pass` | 0 | **promoted** | success | 2 | 0 |
| 2 | agent_memory | `pass` | `pass` | 0 | **promoted** | success | 2 | 0 |
| 3 | agent_memory | `pass` | `pass` | 0 | **promoted** | success | 2 | 0 |
| 4 | agent_memory | `pass` | `pass` | 0 | **promoted** | success | 2 | 0 |
| 5 | agent_memory | `pass` | `pass` | 0 | **promoted** | success | 2 | 0 |
| 6 | deep_research | `pass` | `pass` | 0 | **promoted** | success | 2 | 0 |
| 7 | deep_research | `pass` | `pass` | 0 | **promoted** | success | 2 | 0 |
| 8 | deep_research | `pass` | `pass` | 0 | **promoted** | success | 2 | 0 |
| 9 | deep_research | `uncertain` | `uncertain` | 0 | not promoted | success | 2 | 0 |
| 10 | deep_research | `uncertain` | `uncertain` | 3 | not promoted | success | 2 | 0 |

**Promotions 8/10. Disagreements 0. Retries 0. Technical failures 0. Manual corrections 0.**

Every paper: gate `dual-promotion-v3`, contract `evaluation-independence-v1`, receipt `canonical-response-v1`, assessor `hybrid` / `gemini-3.8-flash`, scope `full_text`, coverage gate `pass`, `provenance_status = pass`, providers google + openrouter, `reasoning_tokens` null or 0. **Manuscript hash identical to the hash frozen in the roster: 10/10.** Evidence provenance: 991 context blocks, 10 distinct context ids, **0 unknown evidence ids**.

### Declared evaluation independence

Primary and adjudicator agreed on **every enum field of every paper (10/10)**, having reached them separately; only prose wording differs.

| # | `signal_reuse` | corroboration | direction | concern | promoted |
|---|---|---|---|---|---|
| 1–4, 6, 7, 10 | `independent` | `present` | `supports` | none | 6 of 7 |
| **5** | **`materially_reused`** | **`present`** | **`supports`** | **none** | **yes** |
| 8, 9 | `not_applicable` | `not_applicable` | `not_applicable` | none | 1 of 2 |

## G. Promotion audit

All eight promotions audited against contribution, method, evaluation, claim/evidence alignment, limitations, overclaiming, evaluation independence and prestige independence. **All eight: `DEFENSIBLE_PROMOTION`. Zero `FALSE_PROMOTION_CONCERN`.**

**#5 Behavior2Trip is the important one.** It is the first live instance of the case the recovery report recorded as covered only by deterministic tests: material evaluator reuse carried by supporting independent corroboration. Both roles identified that GRPO training is rewarded on "user preference constraint satisfaction" and "commonsense constraint checks" while the headline metric is rule-based verification of 32 business-scenario constraints — the same constraint family, correctly declared `materially_reused`. Both then identified genuine independent corroboration: zero-shot cross-benchmark evaluation on the third-party **TravelPlanner** benchmark (9.0% Final Pass Rate versus GPT-4.1's 1.5%), which the adjudicator described as "corroborating the headline gain **outside the training reward's constraint set**". Promotion on that basis is exactly case C and is defensible.

The other seven, in brief:

- **#1 Gated-Memory Routing** — RL against binary ground-truth task reward; headline is held-out benchmark correctness (unit tests, exact match) with FLOPs and wall-clock corroborating the cost claim. Objective ground truth on held-out sets, not a learned judge.
- **#2 MemGauge** — final utility and attack success judged by AgentEvals, validated against **400 trajectories annotated by five human experts, 91% agreement, κ = 0.78**.
- **#3 MOSAN** — optimization on the AutoML training pool; headline is a one-time air-gapped zero-knowledge Lockbox holdout (87.4% across five seeds) plus zero-shot ECG5000 transfer (99.3%).
- **#4 GraphMemix** — frozen-LVLM verification during optimization; headline uses benchmark-native metrics plus a GPT-5-mini judge validated at **97.0% agreement against manual inspection of 200 stratified answers**.
- **#6 SAGE** — an LLM critic drives repair routing; headline combines objective execution recovery (42% → 92%), blind external LLM judges and **blind expert human evaluation by three ML PhDs**.
- **#7 Agentic-Ideation** — oracle-guided synthesis (Qwen3-235B) for training; headline is a four-judge panel, corroborated by a **double-blind human expert study** (+9.88%).
- **#8 The Calibration Turn** — a conceptual perspective with no trained system, correctly `not_applicable`. Promoted on structured comparative analysis across six paradigms plus an illustrative simulation, with claims explicitly bounded and the absence of empirical validation disclosed.

**Prestige independence:** promotions span arXiv preprints, an IOP journal article and OpenAlex-indexed preprints, and include independent and unaffiliated author groups. No promotion rests on venue, institution or author identity.

**#8 is the promotion I scrutinised hardest** and I record it as the weakest in the set: it is a perspective paper carrying no empirical validation. It is nonetheless defensible under the frozen rubric, which requires "meaningful evaluation **or appropriate theoretical/review validation**" scaled to paper type — and the contrast with #9 below shows the gate is not simply passing conceptual work.

## H. Disagreement audit

**Zero disagreements.** Gemini and DeepSeek returned the same decision on all ten papers, and the same evaluation-independence enums on all ten. There is no Gemini-PASS/DeepSeek-non-PASS case and no Gemini-non-PASS/DeepSeek-PASS case to audit.

This is worth stating plainly rather than celebrating: perfect agreement across ten papers gives no evidence about how the adjudicator behaves when it disagrees with the primary. Batch 5 also recorded low disagreement. The dual-model design's independent-check value remains demonstrated mainly by the historical Batch-4 contract recovery and the diagnostic, not by Batch 6.

## I. Non-promotion audit

The frozen audit sample contained exactly one non-promotion (#10). Both non-promotions were audited.

- **#10 DEEPMED Search — `DEFENSIBLE_NONPROMOTION`** (in the frozen sample). Withheld on three manuscript-grounded blockers: evaluation reduced to two isolated accuracy figures with no baselines, sample sizes, variance or structured comparison; the headline "expert-level reasoning" claim unsupported by any clinician validation; and key components (routing heuristics, dynamic thresholds, debate convergence) described too abstractly to reproduce. Its independence fields were `independent / present / supports` — it was **not** withheld on independence grounds, which shows the new dimension did not distort an unrelated judgment.
- **#9 Hephaestus — `DEFENSIBLE_NONPROMOTION`** (audited beyond the frozen sample). A conceptual architecture with, in the primary's words, "no empirical evaluation, experimental testing, or benchmark validation", discussing external systems rather than assessing a prototype. Both roles returned `uncertain`; the adjudicator listed no blocking reason, which is an ordinary non-promotion under the contract.

Zero `POSSIBLE_EXCESSIVE_CONSERVATISM`, zero `CLEAR_EXCESSIVE_CONSERVATISM`, zero `TECHNICAL_ISSUE`.

**The #8 / #9 contrast is the clearest discrimination in Batch 6.** Two conceptual papers in the same track: the one performing structured comparative validation with bounded claims passed; the one presenting an unrealized architecture with validation named as future work was withheld. The gate applied a type-appropriate standard rather than a blanket rule in either direction.

## J. Evaluation-independence analysis

| Category | Papers | Promoted |
|---|---:|---:|
| No evaluator dependence (`independent`) | 7 | 6 |
| Material evaluator reuse (`materially_reused`) | **1** | **1** |
| No adaptation loop / no evaluator-dependent claim (`not_applicable`) | 2 | 1 |
| Unresolved reuse (`uncertain`) | 0 | — |
| Independent corroboration present | 8 | 7 |
| Direction: supports / mixed / contradicts / unavailable / n-a | 8 / 0 / 0 / 0 / 2 | |
| **Major evaluation-independence concerns** | **0** | — |

Model evaluators appear throughout the promoted set — a four-judge panel (#7), GPT-5-mini (#4), AgentEvals (#2), blind LLM judges (#6) — and evaluator signals appear in optimization (#1, #5, #7), selection (#4, #7) and repair (#6). **None of this was penalised as a class.** What the gate asked in each case was whether the headline signal is independent of the adapting signal and, where it is not, whether independent evidence exists and points the right way.

**Two honest limits.** No Batch-6 paper produced `mixed` or `contradicts` corroboration, and none produced a `major` concern, so criterion 8 — contradicting independent evidence treated as a major concern — was **not exercised live in this batch**. It is verified frozen in code (§A) and was demonstrated live in the evaluation-independence recovery, where PEARL was withheld on exactly that limb. Nothing in Batch 6 contradicts it; Batch 6 simply contained no instance. Equally, only one paper exhibited material reuse, so case C rests on a single live example.

## K. Discriminative-power analysis

| Metric | Batch 5 (unseen, v2 gate) | Batch 6 (unseen, v3 gate) |
|---|---|---|
| Papers | 10 | 10 |
| Gemini PASS | 9 / 10 | 8 / 10 (80%) |
| DeepSeek PASS | 9 / 10 | 8 / 10 (80%) |
| Final promotions | 9 / 10 (90%) | **8 / 10 (80%)** |
| Disagreements | low | 0 |
| Technical failures | 0 | 0 |

Across the complete evidence base — Batch 5 unseen (9/10), the failed independence diagnostic (PEARL promoted, the miss), the successful recovery (PEARL withheld, 6/6 correct), and Batch 6 unseen (8/10) — the gate now:

- withholds clearly circular work (recovery, PEARL);
- withholds empirically thin work regardless of framing (#9, #10, and Batch 5's HibriMind);
- promotes evaluator-dependent work where independent evidence actually supports it (#5, and the recovery's validated-dependence papers);
- distinguishes two conceptual papers on the quality of their theoretical validation (#8 vs #9).

No promotion rate was targeted, and the rate was not used to tune anything. The 80% rate reflects a population already filtered to high relevance with a retrievable, coverage-valid manuscript — not the discovery corpus.

## L. Historical integrity

| Check | Result |
|---|---|
| Pre-existing rows byte-identical (row-level payload fingerprint, id order) | **True**, all three tracks |
| agent_memory rows | 348 → **353** (+5) |
| deep_research rows | 271 → **276** (+5) |
| engram rows | 48 → **48** (+0) |
| Total | 667 → **677** (+10) |
| New rows, all `dual-promotion-v3` | 10/10 |
| Papers table | 18,343 / 2,395 / 306 — unchanged |
| Copied-state diagnostic or recovery rows in production | **0** — PEARL still holds exactly one production row, `uncertain` under `dual-promotion-v1` |
| Historical promotion rewritten | none |
| Batch 5 | remains PASS |
| Evaluation-independence diagnostic | remains FAIL |
| Evaluation-independence recovery | remains PASS |

**Append-only holds.**

## M. Technical reliability

Ten papers, two calls each, zero retries, zero contract failures, zero transport failures, zero protocol failures, zero coverage failures, zero integrity failures, zero unknown evidence ids, zero manuscript mismappings (10/10 hash match against the frozen roster), zero manual corrections, zero credential exposure.

**One defect occurred and is recorded.** The first execution-eligibility walk returned zero acquisitions across all 225 candidates. That was a bug in **my orchestration script**, not in the system under test: it passed `config.full_text` where the full-text settings live at `config.quality.full_text`, raising `AttributeError` inside the acquisition loop. It was caught by the implausibility of the result, diagnosed, and fixed in the scratch script only — **no implementation source, prompt, rubric, schema, model or configuration was touched**, and it occurred **before any scientific model call**. After the fix the walk behaved exactly as Batch 5's had (5 of 14 and 5 of 20 walked).

## N. Cost

| Role | Provider / model | Calls | Input | Output | Reasoning | Retries | Monetary |
|---|---|---:|---:|---:|---:|---:|---|
| Primary | google / `gemini-3.8-flash` | 10 | 309,100 | 12,189 | 0 | 0 | **UNKNOWN / MSc allocation** |
| Adjudicator | openrouter / `deepseek/deepseek-v4-pro-0813` | 10 | 292,683 | 6,148 | 0 | 0 | **$0.29777891** |

| Item | Value |
|---|---|
| Batch-6 known money (OpenRouter) | **$0.29777891** (estimate was $0.33102145) |
| Independent PR review during Batch 6 | **$0.00** — no engineering changes authorized, none performed, no review run |
| Cumulative known OpenRouter **before** | $9.26229011 |
| Cumulative known OpenRouter **after** | **$9.56006902** |
| Authorized ceiling | $20.00 — **under ceiling**, headroom $10.43993098 |

The Google endpoint reported no charge on any call, and this project has not established the MSc allocation's effective rate. **Gemini monetary cost = UNKNOWN / MSc allocation**; usage is recorded in exact tokens and no amount is fabricated or assumed to be zero.

## O. Full validation

| Check | Result |
|---|---|
| Unit suite | **505 tests, OK** |
| Relevance, all three tracks | precision 1.000, recall 1.000, 0 FP, 0 FN |
| Quality/promotion fixtures | 8/8 both tracks |
| Discovery recall | 1.000 both tracks |
| Site builds | all three tracks built |
| Site / sidecar schema / relative links / exposure / workflow checks | **0 errors** |
| Stored-assessment integrity check | **677 rows, 0 errors** |
| Idempotency | two consecutive builds differ by **0 non-timestamp lines** |
| Snapshot / restore | `integrity_check=ok`; 353 / 276 / 48 restored |
| Workflows, configs, manifests | all parse |
| `git diff --check` | clean |
| Implementation source changed | **none** |

## P. Publication and deployment

Published: the generated public library artifacts, the Batch-6 population manifest, the Batch-6 roster/protocol and cost-estimate metadata, and this report. **Not published:** any SQLite database, snapshot, raw model execution record, credential or private manuscript cache. `.gitignore` continues to exclude `data/**/*.sqlite3`, `data/cache/` and `*.pdf`. Local private snapshots were verified with `integrity_check=ok` and not uploaded.

| Library | Total | Main library (pass) | New from Batch 6 |
|---|---:|---:|---:|
| Agentic Memory | 1,915 | 20 | **5** |
| Deep Research | 221 | 19 | **3** |
| Engram | 8 | 6 | **0** — intact, no eligible papers |

## Q. Batch-6 PASS criteria

| # | Criterion | Result |
|---:|---|---|
| 1 | Eligible-population manifest reproduced exactly | met — `reproduced=True`, element by element |
| 2 | Roster frozen before any scientific model call | met |
| 3 | No systematic/catastrophic technical defect | met — the one defect was in orchestration, pre-call, and is recorded |
| 4 | Manual corrections = 0 | met |
| 5 | Every audited promotion scientifically defensible | met — 8/8 |
| 6 | No clear false promotion | met |
| 7 | No clear circularity promoted without meaningful independent support | met — the single reuse case carried an external benchmark in the supporting direction |
| 8 | Contradicting independent evidence treated as a major concern | met, **not exercised live in Batch 6** — verified frozen in code, demonstrated in the recovery |
| 9 | Independently validated evaluator-based work not systematically rejected | met |
| 10 | No systematic unsupported-claim pattern | met |
| 11 | No systematic extreme conservatism | met — 8/10, against Batch 5's 9/10 |
| 12 | Receipts and provenance sound | met |
| 13 | Historical state append-only | met |
| 14 | Full repository validation passes | met |

```text
BATCH_6_GENERALIZATION_RESULT: PASS
```

## Readiness

The gate has now been tested on twenty unseen papers across two batches, on a deliberately enriched historical challenge set that exposed a real blind spot, and on the same set again after that blind spot was closed. It withholds clearly circular work, withholds empirically thin work whatever its framing, promotes evaluator-dependent work when independent evidence genuinely supports it, and distinguishes conceptual papers by the quality of their theoretical validation. Technical reliability is 32 papers with zero failures. Historical state is intact and append-only.

Three limits are recorded rather than resolved, none of which is a known screening defect:

1. Batch 6 produced no `mixed` or `contradicts` corroboration and no `major` concern, so the directionality limb was exercised only in the recovery, not here.
2. Case C now has exactly one live example.
3. Gemini and DeepSeek agreed on all ten papers, so Batch 6 adds no evidence about adjudicator behaviour under disagreement.

These argue for continued monitoring of live operation, not for withholding readiness.

---

```text
BATCH_5_GENERALIZATION_RESULT = PASS
EVALUATION_INDEPENDENCE_DIAGNOSTIC = FAIL
EVALUATION_INDEPENDENCE_RECOVERY = PASS
BATCH_6_GENERALIZATION_RESULT: PASS
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: YES
```
