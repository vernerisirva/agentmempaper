# Batch 4 — promotion-gate generalization evaluation — 2026-09-18

**Ten unseen papers ran through the frozen Gemini + DeepSeek promotion gate with zero code changes, zero manual corrections and zero technical failures. Nine were promoted and every promotion is scientifically defensible against its manuscript. The batch nevertheless FAILS generalization: a systematic contract defect in the gate turned one unanimous pass into a non-promotion, and that wrong outcome is stored and published as if it were a scientific concern.**

## A. Frozen protocol

| Item | Value |
|---|---|
| `BATCH_4_CODE_SHA` | `7622fccd25abdef904d678e10a603f8e17a95b4f` |
| Protocol file | [`experiments/manifests/batch-4-protocol-2026-09-18.json`](../../experiments/manifests/batch-4-protocol-2026-09-18.json) |
| Protocol SHA-256 | `66a2c272187ccc8d78f2d14bc1fa69ea43da0b98e16d406b2b527b60145b3ad7` |
| Protocol unchanged | Yes — single commit `7622fccd2`, byte-identical before and after the batch |
| Working tree at start | clean, `main`, up to date with `origin/main` |

The only commit after the protocol's `frozen_code_sha` (`40a203ee`) is `7622fccd2`, which added the configuration report and the protocol manifest and touched **no implementation file**.

### Production configuration, recorded not changed

| Role | Provider | Model | Family | Credential |
|---|---|---|---|---|
| Primary assessor | google | `gemini-3.8-flash` | gemini | `GEMINI_API_KEY` |
| Independent adjudicator | openrouter | `deepseek/deepseek-v4-pro-0813` | deepseek | `OPENROUTER_API_KEY` |

`GATE_VERSION = dual-promotion-v2`, `ASSESSMENT_VERSION = quality-promotion-v1`, `RUBRIC = scholarly-rubric-v1`, `RECEIPT_VERSION = canonical-response-v1`, `MODEL_PAIR_VERSION = model-pair-v1`, `RETRY_POLICY = adjudicator-contract-retry-v1`, evidence context `block-evidence-v2`, coverage gate `coverage-v2`.

Generation: `temperature 0`, `max_tokens 4096`, `max_request_bytes 300000`, strict `json_schema`, hidden reasoning disabled — expressed as `reasoning_effort: 'none'` for Google and `reasoning {enabled:false, exclude:true}` for OpenRouter, exactly as established during integration testing. Call budget 1 primary + up to 2 adjudicator, 3 total. Receipts bind the canonical response, each attempt, the model pair and both providers. No value was changed and no Claude-family model occupied either scientific role.

```text
GEMINI_API_KEY:     AVAILABLE   (private interactive shell; not inherited by this session)
OPENROUTER_API_KEY: AVAILABLE   (private interactive shell; not inherited by this session)
```

Neither value was printed, logged, hashed, partially revealed or copied, and no project-local secret file was created.

## B. Eligible population

The frozen predicate is: high relevance **AND** never scientifically quality-assessed **AND** never adjudicated **AND** not explicitly suppressed **AND** a retrievable manuscript **AND** coverage gate PASS. Manuscript availability is an execution-eligibility condition, not a quality filter, and no scientific field was inspected during selection.

**The exclusion set reproduces exactly.** Unioning the four documented sources — every canonical id with a persisted assessment row in any track database (477), the frozen Batch-3 roster (16), the Batch-1 calibration identities (28) and the `all_prior_assessed_ids` manifest (462) — gives **478** ids, matching the protocol's `exclusion_set_size` exactly. All 478 resolve to real paper rows. A scan of every per-paper operator run record found 21 canonical ids, all already inside those 478, so operator artifacts contributed nothing further.

**The population commitment hashes do not reproduce.** This is reported rather than smoothed over:

| Track | Protocol count | Recomputed (stored-relevance level) | Protocol commitment reproduced |
|---|---:|---:|---|
| agent_memory | 526 | 535 | no |
| deep_research | 113 | 114 | no |
| engram | 0 | 0 | **yes** (empty-set digest) |

Under identifier alias closure (canonical/DOI/arXiv/OpenAlex, and identifiers parsed out of `url`, which is stricter than the protocol's wording) the recomputed counts are 535 and 114. Additionally excluding papers whose manuscript a prior run had already acquired into the track full-text cache reproduces agent_memory's 526 **exactly**, but takes deep_research to 105 rather than 113. No combination of the protocol's stated exclusion sources reproduces both tracks, and the previous task saved neither its population script nor its id lists, so the commitment is not independently verifiable. The protocol's own text ("every canonical id with saved operator run artifacts, including a started primary call with no stored row") is not defined precisely enough to reproduce.

The protocol's "high relevance" counts (657 / 254 / 11) are raw stored-relevance counts, whereas its selection ordering is defined over the offline site pipeline, which merges duplicates and refreshes rule classifications. These are two different domains; the ranking domain is what determines selection.

**Selection therefore used the conservative reading**: the union of every exclusion any reading supports. In the ranked (pipeline) domain that gives **203 / 40 / 0** eligible papers. Because selection takes only the leading papers in deterministic order, and because every selected paper was then exhaustively verified to have zero prior assessments, the discrepancy does not affect experimental validity — but it does mean the frozen population commitment is **not auditable**, which is a defect in the protocol, not in the run.

### Acquisition and coverage filtering

| Track | Walked in rank order | Acquisition failed | Coverage gate PASS | Selected |
|---|---:|---:|---:|---:|
| agent_memory | 8 | 3 | 5 | 5 |
| deep_research | 11 | 6 | 5 | 5 |
| engram | 0 | 0 | 0 | 0 |

All nine acquisition failures were Zenodo and ACM DOIs with no retrievable open manuscript. Engram has **zero** eligible papers, so no Engram sample was manufactured.

## C. Frozen roster

Frozen **before any model call** in [`experiments/manifests/batch-4-roster-2026-09-18.json`](../../experiments/manifests/batch-4-roster-2026-09-18.json).

```text
BATCH_4_ROSTER_SHA256:       f9ba9748b3a662961b366b0bf4937b2449a584769fd914ef3ebc715d893b3360
BATCH_4_AUDIT_SAMPLE_SHA256: 9e5d1b14c13bf23d8efb97fde08219663483dc6016b4ce8ab31f3fb1cdcb876c
roster file SHA-256:         d2fa2d398d7768407fbbadeaa11a49be1e2247b9311639fca2e6740ff0df6956
```

| # | Track | Rank | Canonical id | Title |
|---|---|---:|---|---|
| 1 | agent_memory | 45 | `doi:10.48550/arxiv.2609.03467` | When Users Don't Ask: Benchmarking Context-Driven Memory Retrieval in Conversational Agents |
| 2 | agent_memory | 46 | `arxiv:2609.03871` | Bioinfoysis Technical Report |
| 3 | agent_memory | 47 | `arxiv:2609.03632` | Dynamic probabilistic decision networks |
| 4 | agent_memory | 49 | `arxiv:2609.03727` | Proactive Service Agents: A Unified Decision Framework, Methods, and Evaluation |
| 5 | agent_memory | 50 | `doi:10.48550/arxiv.2609.02265` | CAPTURE: Disentangling Preference Drift from Memory Poisoning in Personalized LLM Agents |
| 1 | deep_research | 94 | `openalex:W7169633615` | Analogical Deep Research: Retrieving and Integrating Historical Analogies for Foresight Analysis |
| 2 | deep_research | 98 | `openalex:W7169633509` | FinResearchBench II: A Deep Research Benchmark with Consensus-Derived Gold Rubrics |
| 3 | deep_research | 99 | `openalex:W7168432559` | Are LLMs Ready for Scientific Discovery? A Capability-Oriented Benchmark for AI Scientists |
| 4 | deep_research | 101 | `openalex:W7168433647` | NVAITC AI Scientist: A Governed End-to-End Research System — A Hypertension GWAS Case Study |
| 5 | deep_research | 102 | `openalex:W7168434034` | Distributed Denial of Science: How Indirect Data Poisoning Can Industrialize Scientific Fraud |

Track distribution 5 / 5 / 0, total 10 — the protocol's expected maximum. Every roster entry records track, canonical id, title, ranking and selection position, relevance status, manuscript source and hash, coverage-gate status, and `prior_scientific_assessment_count = 0` / `prior_adjudication_count = 0`.

**Every selected paper was verified never assessed and never adjudicated**, by expanding each to its full identity across all three databases (canonical, DOI, arXiv, OpenAlex, url-derived arXiv and normalized title), collecting every sibling record sharing any of those identities, and counting assessment rows for all of them: **0 prior rows for all 10 papers, and none present in the 478-id exclusion base.**

The roster was immutable from the first scientific call onward. No substitution was made and no paper was replaced for a scientific outcome.

## D. Frozen audit sample

Frozen before any outcome was observed, by the protocol rule (positions 1, ⌊n/2⌋+1 and n in each populated track, n = 5):

| Track | Positions | Canonical ids |
|---|---|---|
| agent_memory | 1, 3, 5 | `doi:10.48550/arxiv.2609.03467`, `arxiv:2609.03632`, `doi:10.48550/arxiv.2609.02265` |
| deep_research | 1, 3, 5 | `openalex:W7169633615`, `openalex:W7168432559`, `openalex:W7168434034` |

## E. Per-paper results

| Paper | Title | Gemini primary | DeepSeek adjudicator | Blockers | Promotion | Outcome/provenance | Calls |
|---|---|---|---|---:|---|---|---|
| agent_memory #1 | When Users Don't Ask | `pass` | `pass` | 0 | **promoted** | success/pass | 1+1 |
| agent_memory #2 | Bioinfoysis Technical Report | `pass` | `pass` | 0 | **promoted** | success/pass | 1+1 |
| agent_memory #3 | Dynamic probabilistic decision networks | `pass` | `pass` | 0 | **promoted** | success/pass | 1+1 |
| agent_memory #4 | Proactive Service Agents | `pass` | `pass` | 1 | **not promoted** | success/pass | 1+1 |
| agent_memory #5 | CAPTURE | `pass` | `pass` | 0 | **promoted** | success/pass | 1+1 |
| deep_research #1 | Analogical Deep Research | `pass` | `pass` | 0 | **promoted** | success/pass | 1+1 |
| deep_research #2 | FinResearchBench II | `pass` | `pass` | 0 | **promoted** | success/pass | 1+1 |
| deep_research #3 | SDABench / Are LLMs Ready | `pass` | `pass` | 0 | **promoted** | success/pass | 1+1 |
| deep_research #4 | NVAITC AI Scientist | `pass` | `pass` | 0 | **promoted** | success/pass | 1+1 |
| deep_research #5 | Distributed Denial of Science | `pass` | `pass` | 0 | **promoted** | success/pass | 1+1 |

Every paper: coverage gate `pass`, manuscript identity verified, `provenance_status = pass`, receipt `canonical-response-v1` validating against the pinned model pair and both providers, assessor model `gemini-3.8-flash`, gate `dual-promotion-v2`. No hidden reasoning was requested, returned or persisted.

**Promotions: 9 of 10.**

## F. Promotion audit

All nine promotions were audited observationally against the acquired manuscript. No stored result was modified.

**Evidence provenance, checked mechanically across all ten papers:** every evidence ID cited by either role resolves to a real block of that paper's canonical context (0 unknown IDs across 1,179 context blocks), every stored evidence excerpt is byte-identical to its canonical block (0 mismatches), each context hash equals the assessment's `source_content_hash`, and each equals the manuscript hash frozen in the roster. **No fabricated evidence and no cross-paper contamination.**

Specific factual and numeric claims were verified verbatim against the manuscripts: LoCoMo-Conv's five compared memory systems and variance bound; Bioinfoysis's BixBench/LAB-Bench 2 results, four ablations and cross-model range; the decision-network paper's validation against Kahneman–Tversky's 18 lotteries and Murphy–ten Brincke's 67-lottery, 134-decision-task set; FinResearchBench II's 104 queries, 1,040 reports, 4,052 human-validated instances, 98.67% agreement and κ = 0.9733; SDABench's 527 real and 6,000 synthetic instances and five-stage error taxonomy; NVAITC's 286,422-individual biobank GWAS, replicated loci FGF5/ATP2B1/CNNM2/FTO/GRB14 and AUC 0.842; and the poisoning paper's 49.56% attack success, 6.0% detection and κ ≥ 0.758. **Every checked claim is present and correctly stated.**

| Promotion | Classification | Note |
|---|---|---|
| agent_memory #1 | `DEFENSIBLE_PROMOTION` | Benchmark with controlled ablations, seed-variance analysis, author-stated limitations |
| agent_memory #2 | `DEFENSIBLE_PROMOTION` | Four ablations, cross-model consistency, substantive limitations section; mild promotional prose, no scientific overclaim |
| agent_memory #3 | `DEFENSIBLE_PROMOTION` | Complete theoretical model validated without fitting parameters on two published lottery datasets. **Weakness:** the manuscript contains no limitations statement at all; the `limitations` field holds the assessor's own accurate scope characterisation rather than an author-acknowledged limitation |
| agent_memory #5 | `DEFENSIBLE_PROMOTION` | Strongest of the batch: adaptive white-box attacker, human red-teamers, Holm-adjusted paired tests, declared falsification criteria; assessment explicitly records where the method's advantage disappears |
| deep_research #1 | `DEFENSIBLE_PROMOTION` | Assessment itself flags the modest 15-event benchmark and LLM-judge reliance |
| deep_research #2 | `DEFENSIBLE_PROMOTION` | Two genuine sensitivity analyses. Minor imprecision: described as "split-half", actually a leave-three-out held-out-systems split over 120 combinations |
| deep_research #3 | `DEFENSIBLE_PROMOTION` | Programmatic ground truth, 15 models, five-stage failure analysis, author-stated limitations |
| deep_research #4 | `DEFENSIBLE_PROMOTION` | Assessment correctly bounds the claim to locus replication rather than novel discovery, and to single-institution deployment |
| deep_research #5 | `DEFENSIBLE_PROMOTION` | Staged propagation measurement with inter-annotator validation of the judge |

**`FALSE_PROMOTION_CONCERN`: 0.** No promotion depended on author, institution or venue prestige; none of the nine assessments references reputation, and two promoted papers are from small or non-Anglophone groups with no prestige signal. The assessments are specific and manuscript-grounded rather than generic, and several volunteer real weaknesses — evidence against simple pass-bias.

## G. Disagreement audit

**There were zero scientific disagreements.** Gemini returned `pass` on 10 of 10 and DeepSeek returned `promotion_decision: pass` on 10 of 10. The protocol's disagreement category (Gemini PASS + DeepSeek ≠ PASS) is empty.

This is itself a material result. On this sample the independent adjudicator never once diverged from the primary, so **Batch 4 provides no evidence that the dual gate has discriminative power**. The two roles agreed unanimously on every paper. Because the ten papers were all independently confirmed substantive, unanimous agreement is consistent with correct behaviour — but it does not demonstrate the gate can reject weak work, and that capability remains untested after Batch 4.

### The one non-promotion is a machinery defect, not science

`agent_memory #4` (Proactive Service Agents) was **not promoted although both scientific roles passed it**. The adjudicator returned `promotion_decision: "pass"` and placed a single string in `blocking_reasons`:

> "No blocking reasons: the manuscript's scoped survey contribution, formal decision framework, critical evaluation protocol, and explicit limitation handling are well supported by the supplied evidence."

`agreement()` in `paper_scout/promotion_protocol.py:228` requires `not adjudicator['blocking_reasons']`, so any non-empty array blocks promotion regardless of content. Re-evaluating the recorded response with an empty array returns `True`; every other conjunct already held. **The sole cause of the non-promotion is a prose sentence stating that there are no blocking reasons.**

The defect is systematic rather than incidental: the schema (`maxItems 12`, `minLength 1` strings) permits a "none" sentinel, nothing detects it, and no retry fires because the response is schema-valid. It will recur whenever the adjudicator phrases "no blockers" as prose.

Its footprint is not confined to the decision. `promotion_gate.py:275` assigns `base['concerns'] = adjudicator['blocking_reasons']`, so the sentinel is stored as a scientific concern and rendered on the **public review page** as the paper's sole concern — a card held out of the main library whose stated concern is that it has none. The wrong outcome is therefore invisible as a defect and indistinguishable from a genuine scientific reservation.

Per the stop rule this was **not** patched and the batch was **not** interrupted: it is not in the catastrophic list (no wrong manuscript, no contamination, no broken receipts, no state corruption, no secret exposure, no configuration drift) and it fails closed, never promoting anything wrongly.

## H. Frozen non-promotion audit

The frozen audit sample (six papers) contains **zero non-promotions** — all six were promoted — so the sample yields no non-promotion classifications, and no evidence of systematic excessive conservatism was available from it.

The batch's only non-promotion, `agent_memory #4`, is outside the frozen sample but is audited here because the protocol requires auditing every primary-pass outcome that did not promote:

| Paper | Classification |
|---|---|
| agent_memory #4 | **`TECHNICAL_ISSUE`** — not scientific conservatism; both roles passed, and the block was a contract-semantics artifact |

No stored result was changed.

## I. Reliability

| Measure | Value |
|---|---|
| Papers executed | 10 / 10 |
| Primary calls | 10 (budget 10) |
| Adjudicator calls | 10 (budget 20) |
| Contract retries | 0 |
| Transport failures | 0 |
| Protocol failures | 0 |
| Output-limit failures | 0 |
| Invalid evidence IDs | 0 |
| Receipt failures | 0 |
| Provenance failures | 0 |
| Persistence errors | 0 |
| Manual corrections | **0** |
| Code changes during the batch | **0** |
| Outcomes wrong through machinery | **1 of 10** |

Transport and protocol reliability were perfect. The single wrong outcome came from contract semantics, not from the transport, schema, receipt or persistence layers.

## J. Historical integrity

| Track | Assessments before | After | Delta | New `dual-promotion-v2` |
|---|---:|---:|---:|---:|
| agent_memory | 337 | 342 | +5 | 5 |
| deep_research | 261 | 266 | +5 | 5 |
| engram | 48 | 48 | 0 | 0 |
| **Total** | **646** | **656** | **+10** | **10** |

Every pre-existing row (`id ≤ 339 / 302 / 85`) is byte-identical to its pre-batch digest across id, canonical id, assessed-at, recommendation and payload length. **No historical promotion decision changed, no Batch-3 outcome was reinterpreted, and no prior row was rewritten.** The ten new rows are exactly the ten roster papers and nothing else — no smoke-test row leaked into production. All 656 stored rows parse, 489 current assessments load, and the 18 stored `dual-promotion-v1` rows (15 of them still the current assessment for their paper) remain readable beside the new ones. All ten new receipts pass `validate_receipt`.

## K. Cost

### Gemini primary (Google)

| Item | Value |
|---|---|
| Calls | 10 |
| Retries | 0 |
| Input tokens | 382,184 |
| Output tokens | 9,982 |
| Monetary cost | **UNKNOWN**, `covered_by_msc_allocation` |

The endpoint reports no charge and this project has not established the allocation's effective rate. The usage is recorded in exact tokens; **no monetary amount is fabricated and it is not assumed to be free.**

### DeepSeek adjudicator (OpenRouter)

| Item | Value |
|---|---|
| Calls | 10 |
| Retries | 0 |
| Input tokens | 353,760 |
| Output tokens | 4,302 |
| Cost | **$0.40381710** |

### Total scientific inference

| Item | Value |
|---|---|
| Known monetary cost | **$0.40381710** |
| Unknown / allocation-backed | Gemini 382,184 in / 9,982 out |
| Pre-execution estimate | $0.3134568 (actual +28.8%, from longer manuscripts than the smoke sample) |
| Cumulative against the $10 ceiling | $6.08092007 → **$6.48473717** (remaining $3.51526283) |

No prior engineering-review cost is mixed into this figure; it is Batch-4 scientific inference only.

## L. Validation

| Check | Result |
|---|---|
| Unit suite | **404 tests, OK** |
| Relevance validation, all three tracks | precision 1.000, recall 1.000, 0 FP, 0 FN |
| Quality/promotion fixtures, all three tracks | 8/8 passed |
| Discovery validation | recall 1.000 (6/6, 4/4, 4/4) |
| Idempotency, all three tracks | passed |
| Site builds | all three built offline |
| Site/schema/link/exposure/workflow checks | **0 errors** |
| Workflow YAML + all manifests parse | 3 YAML, 11 JSON, all OK |
| Snapshot/restore | three databases, `integrity_check=ok` |
| Legacy compatibility | 656 rows parse; 18 `dual-promotion-v1` rows readable |
| `git diff --check` | clean |
| Implementation source changed | **none** (`paper_scout/`, `tests/`, `config/` all unmodified) |
| Secret scan | 0 credential-shaped strings; 0 `thought_signature`; 0 `reasoning_content` |

The unit suite requires Homebrew Git on `PATH`: the host's Xcode licence is still unaccepted, so the system Git exits 69 and one test that initialises a temporary repository fails through no fault of the code. No host setting was changed.

## M. Publication and deployment

Public generated output changed because nine papers were promoted. Published: the regenerated three-track site and sidecars, the Batch-4 roster, cost-estimate and this report. The 1,920 changed paper sidecars are `generated_at` timestamp churn from the rebuild, not content changes.

Not published, and still excluded by `.gitignore`: the SQLite assessment databases, runtime state, snapshots and raw execution records. Verified durable-state snapshots are kept **locally only**, all three with `integrity_check=ok`.

The public library correctly reflects the stored decisions: nine papers admitted to `main`, one to `review`. **One publication defect is recorded honestly:** the review card for `arxiv:2609.03727` displays the sentinel string from section G as its only concern. This was not hand-corrected, because manual correction of a stored scientific output is forbidden by the protocol and the underlying defect must not be patched under the Batch-4 designation.

## Assessment against the generalization criteria

| # | Criterion | Met |
|---|---|---|
| 1 | No systematic/catastrophic implementation defect | **NO** — the `blocking_reasons` sentinel defect is systematic and reproducible |
| 2 | Manual scientific corrections = 0 | yes |
| 3 | All audited promotions scientifically defensible | yes — 9/9 |
| 4 | No systematic unsupported-claim pattern | yes |
| 5 | Disagreements fail closed | yes (vacuously — there were none) |
| 6 | Provenance/receipt integrity sound | yes |
| 7 | No systematic extreme conservatism in the frozen sample | no evidence available — the frozen sample contained no non-promotions |
| 8 | Technical reliability acceptable | **NO** — 1 of 10 outcomes wrong through machinery |
| 9 | Historical assessments unchanged | yes |
| 10 | Full repository validation passes | yes |

Zero promotions would not have meant failure, and nine promotions do not mean success. The scientific behaviour was sound: every promotion is defensible, every claim checks out against its manuscript, and no prestige signal influenced any decision. The batch fails on the machinery, not the science — and on a defect whose stored form is indistinguishable from a scientific judgment, which is precisely the failure mode an operational gate must not have.

Two further limits on what Batch 4 established, neither of which is itself a failure:

- The gate's **discriminative power is untested**. Both roles passed all ten papers; no paper was rejected on scientific grounds, so nothing here shows the gate would reject weak work.
- The frozen **population commitment is not reproducible**, so the claim that Batch 4 drew from a specific pre-committed population cannot be independently audited. Selection validity was preserved instead by verifying each selected paper individually.

## Verdicts

```text
BATCH_4_GENERALIZATION_RESULT: FAIL

QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
```

The gate is not ready for operational use because a systematic implementation defect remains: a schema-valid "no blockers" sentinel in `blocking_reasons` silently converts a unanimous scientific pass into a stored and published non-promotion carrying a fabricated-looking concern. Until that is fixed and retested on a fresh unseen batch under a new designation, promotion precision on this pair is established only for the nine papers audited here, and the gate's ability to reject weak work is not established at all.

Recurring daily quality assessment was **not** started and Batch 5 was **not** selected.

```text
GEMINI_PRIMARY_GATE_READY: YES
QUALITY_PROMOTION_GATE_READY_FOR_BATCH_4: YES (consumed)
MANUSCRIPT_COVERAGE_GATE_READY: YES
ORIGINAL_BATCH_3_GENERALIZATION_RESULT = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_CHECK = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_V2_CHECK = PASS
BATCH_3_REMAINING_HOLDOUT_RESULT = FAIL
```

**Private remote durable-state storage remains an unresolved operational infrastructure backlog item.** The configured remote preservation mechanism still publishes to a public GitHub release, which is unacceptable for private assessment state; snapshots continue to be kept and verified locally only.
