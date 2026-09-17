# Batch 3: unseen promotion-gate evaluation — 2026-09-17

**The frozen experiment stopped on its first paper after a reproducible production persistence failure.** Both independent models returned `pass`, but `PaperStore.save_quality_assessment` raised `ValueError: invalid dual-promotion receipt` before inserting a row. No paper entered a main library. The remaining 15 frozen entries were not attempted. This is a technical generalization failure, not scientific disagreement or manuscript unavailability.

No source, prompts, models, schemas, rubric, thresholds, evidence semantics, selection logic or automatic outputs were changed. No retry, replacement, manual correction, engineering review, Batch 4 or new recurring assessment was started. The mandatory stop rule superseded completing the remaining scientific calls.

## Frozen protocol

- `BATCH_3_FROZEN_CODE_SHA`: `63605a3a839d84800418d8e4738ab0c6fcad0df9` (clean canonical main after fetch/checkout/fast-forward pull).
- PR #34 merge: `afd1a7018cc6f38a317e340a0a77b86c1078cd63`; actual reviewed implementation: `c737badb6249d4faefe0bf1546da90576f206a35`. The later main commit is report-only.
- Primary: `deepseek/deepseek-v4-pro-0813`; independent adjudicator: `anthropic/claude-sonnet-4.6`.
- Rubric `scholarly-rubric-v1`, assessment `quality-promotion-v1`, promotion `dual-promotion-v1`, canonical evidence `block-evidence-v2`, identity `exact-title-typography-v1`. Coverage `coverage-v1`, selection `representative-v1`, Unicode normalization `canonical-unicode-v2`.
- Temperature 0, reasoning disabled/excluded, no seed, strict JSON schemas, provider parameter support required, at most 300,000 serialized bytes and 4,096 output tokens per call. One total attempt per role: `HttpClient(retries=1)` means zero retries. Primary price caps $1.65/$4.95 and adjudicator $3.30/$16.50 per million input/output tokens.
- The adjudicator runs after each valid primary response, including uncertainty. It receives the identical canonical context and only the unchanged primary final structured judgment; no hidden reasoning. Promotion requires high relevance, both passes, nonempty valid citations, no adjudicator blockers, valid provenance and no suppression. Disagreement fails closed.
- `BATCH_3_MANIFEST_SHA256`: `d1dc21c7fb0e0f4575f714331dfd8b5671ef2876da808b5eec55497bc741fc8b`.
- Protocol recorded before selection; roster frozen at `2026-09-17T19:11:19+00:00`; automatic outcomes frozen at `2026-09-17T19:17:21.733023+00:00` before audit.
- User-prescribed selection supersedes the prepared draft: up to **eight** per track using the existing offline research ranking, not ten by hash. Production duplicate merging, rule refresh, existing curation, quality presentation, newness and `_sort_latest_relevant` are unchanged. The ordering key is newness, high relevance, downrank flag, date bucket/date, combined rank, relevance score, lowercase title.
- Eligibility is high relevance, never assessed/adjudicated globally, not suppressed. All historical assessment identities, the 28 calibration identities and every original Batch-2/recovery identity were excluded, including known DOI/arXiv/title aliases. Eligible pools: **211 / 50 / 0**; selected **8 / 8 / 0**. No availability, quality, author, institution or venue filter, quota transfer or substitution.
- Audit positions frozen before results: **1, 5, 8** in each populated track; Engram has none. Exact IDs are below.

[Execution protocol](../../experiments/manifests/batch-3-execution-protocol-2026-09-17.json) · [Immutable roster](../../experiments/manifests/batch-3-roster-2026-09-17.json) · [Manifest hash](../../experiments/manifests/batch-3-roster-2026-09-17.sha256) · [Pre-call cost estimate](../../experiments/manifests/batch-3-cost-estimate-2026-09-17.json) · [Structured outcomes and reviewed final judgments](batch-3-promotion-gate-evaluation-2026-09-17.json).

## Roster and outcomes

Every entry was high relevance and `not_assessed`, with zero prior assessment identities. Publication/cache/source metadata and complete rank information remain in the immutable roster. `—` means no judgment exists. A stopped entry is not counted as scientific uncertainty, manuscript unavailable, or an observed per-paper failure.

| Track / selected position / research rank | Paper / canonical ID | Primary | Adjudicator | Promotion / technical status |
|---|---|---|---|---|
| agent_memory / 1 / 2 | Causal Path Alignment: Anchoring the Optimization Trajectory for Controllable In-Parameter Knowledge Editing · `doi:10.24963/ijcai.2026/655` | pass | pass | NOT PROMOTED — persistence_failure |
| agent_memory / 2 / 32 | nox-mem: Pain-Weighted Hybrid Memory for LLM Agents · `doi:10.5281/zenodo.22649269` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| agent_memory / 3 / 33 | Contextualized Reinforcement Learning with Episodic Memory Networks · `doi:10.5281/zenodo.22587729` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| agent_memory / 4 / 34 | Hierarchical Reinforcement Learning with Memory Networks · `doi:10.5281/zenodo.22623238` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| agent_memory / 5 / 35 | Delete Names Five Operations: Erasure Semantics for Derived Agent Memory, and Why a State-Level Definition Cannot Be the Auditable One · `doi:10.5281/zenodo.22425280` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| agent_memory / 6 / 36 | retainkit: context and memory policies for LLM agents, scored by the evidence that survives the token budget · `doi:10.5281/zenodo.22352965` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| agent_memory / 7 / 37 | Hierarchical Reinforcement Learning with Temporal Abstraction and Memory · `doi:10.5281/zenodo.22336737` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| agent_memory / 8 / 40 | Who Did It? Sleep, Source Memory, and Action Memory in Human 4-Year-Olds · `doi:10.3390/bs16091578` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| deep_research / 1 / 1 | An immune world model for multiscale forecasting and therapeutic hypothesis generation · `doi:10.48550/arxiv.2609.14709` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| deep_research / 2 / 2 | AppliedScientist: Automated Scientific Revision Through Iterative AI Reviewing · `openalex:W7213371831` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| deep_research / 3 / 86 | Cracking a 600-Year-Old Mystery with Geometry: The Voynich Manuscript Finally Speaks — An Ô-HAT Cross-Language Phase-Space Analysis · `doi:10.5281/zenodo.21493208` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| deep_research / 4 / 87 | Artificial Intelligence for Water Sustainability and Climate Adaptation in Small Island States · `doi:10.70593/978-93-7185-684-3` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| deep_research / 5 / 88 | SciHazard: A Benchmark for Measuring Scientific Safety Risks with Decomposed Harm Scoring · `openalex:W7170225285` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| deep_research / 6 / 89 | PEARL: Auditable Repair for Scientific Reasoning Graph Extraction · `openalex:W7170112970` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| deep_research / 7 / 90 | DRNOISE: Benchmarking Deep Research Agents in Misleading Evidence Environments · `openalex:W7170112771` | — | — | NOT PROMOTED — not_attempted_batch_stopped |
| deep_research / 8 / 91 | Recent Advances in AI for Automated ICD Coding: A Systematic Literature Review · `doi:10.1007/s10916-026-02429-7` | — | — | NOT PROMOTED — not_attempted_batch_stopped |

## Reliability and exact failure

The first paper was Causal Path Alignment. Production acquired its existing arXiv URL once, extracting all 13 pages with no failed source attempt, no unreadable page, no extraction truncation and zero omitted body characters. Both calls completed normally with `finish_reason=stop`, matching pinned model identities and valid response schemas. There were 16 primary IDs, 16 adjudicator IDs, and 17 distinct cited IDs, all belonging to the correct manuscript.

Source SHA-256: `bbd08d38d12ccd97766992bfbb6e3cd58adb1e540d9750aec247549a4db3a7e5`. Context ID: `d5aba638083f7fcadacd84049347c421a546017878e3272dbe8e285e4072afac`. Exact-title acquisition identity passed. The two request bodies contain identical manuscript/context inputs, and the adjudicator receives precisely the saved primary final response. No hidden reasoning was returned (reported reasoning tokens: zero). Different model families and separate calls preserve procedural independence; they do not establish statistical independence.

`QualityEvidence.from_dict` passes `excerpt` through `_optional_text`, which calls `.strip()`. At the persistence boundary, `QualityAssessment.from_dict(assessment.to_dict())` strips one trailing whitespace character from **11 of 17 cited excerpts**, while each canonical `source_blocks[0].text` remains unchanged. `validate_receipt` requires exact equality, so it raises `persisted snippet or citation mapping mismatch`, wrapped as `invalid dual-promotion receipt`. The failure occurs before the SQL insert. No historical row was damaged.

An offline diagnostic replayed the two exact saved final responses through unchanged production functions and asserted byte-equivalent request payload values. It validated the in-memory receipt, then reproduced the same deserialization exception with no HTTP, DB write, output repair or new experimental outcome. The diagnostic is not a model retry or a resumed batch. The general serialization rule makes this a systematic defect risk, not an isolated transient provider failure; execution stopped at **2026-09-17T19:15:14.596620+00:00**.

Outcome persistence was therefore incomplete by design of the frozen failing implementation: **zero Batch-3 assessment rows were inserted**. Actual requests/responses, acquisition, exact evidence, model/provenance metadata, error, cost ledger and stop record are preserved in ignored `data/cache/operator/batch-3-20260917/`. The tracked report records the failed execution; no manually fabricated technical assessment was injected into production storage.

## Promotion audit

**Zero persisted automatic promotions.** The all-promotion audit set is empty, and promotion precision is unestimated. No `FALSE_PROMOTION_CONCERN` is assigned to a nonexistent promotion. Both scientific passes on the attempted paper remain visible as unpersisted judgments and are audited below.

## Frozen non-promotion audit

### agent_memory / 1: Causal Path Alignment: Anchoring the Optimization Trajectory for Controllable In-Parameter Knowledge Editing

Canonical ID: `doi:10.24963/ijcai.2026/655`. Classification: **`technical_issue`**.

Availability: available: 13 pages, fresh acquisition, no body omission. Production serialization invalidated a valid in-memory receipt; no assessment persisted.

**Scientific contribution:** Substantive parametric-memory knowledge-editing method, relevant to the Agentic Memory scope.

**Method:** Two-stage relation anchoring followed by trajectory alignment is supported by sections 4.1–4.2 and canonical B0035–B0037.

**Evaluation:** COUNTERFACT RS and EVOKE across four backbones, 2,000 edits with five repeats, component ablations, mechanistic analysis and MEMIT/AlphaEdit transfer support the scoped empirical contribution. Tables include efficacy trade-offs, and zsRE results limit generalization.

**Claim alignment:** Core method and benchmark claims are supported. The broad root-cause language is the manuscript interpretation, not proof across all agents. The primary latency phrase is ambiguous: about 5 seconds is the increase, whereas Figure 12 gives total CPA times of 9.2 and 20.1 seconds. Neither scientific response was corrected.

**Limitations:** The primary acknowledges weaker zsRE performance, latency and untested sequential lifelong editing. The 5-second increase and sequential-batch limitation lie in B0082, outside both returned evidence-ID lists; B0079 and B0081 cover the first limitation and only the beginning of latency discussion. This is a citation-completeness concern on an unpersisted proposed pass.

**Evidence integrity:** All 17 distinct cited IDs resolve to the correct source/context. Exact title identity and source hash pass; zero body omissions and no cross-paper contamination. Eleven excerpts acquire mismatches solely during storage deserialization because trailing whitespace is stripped.

**Prestige independence:** Neither final response uses authors, institution or venue prestige as quality evidence.

**Conservatism:** Technical withholding of a supported study, not evidence of scientific conservatism; the batch is too incomplete to assess systematic scientific selectivity.

### agent_memory / 5: Delete Names Five Operations: Erasure Semantics for Derived Agent Memory, and Why a State-Level Definition Cannot Be the Auditable One

Canonical ID: `doi:10.5281/zenodo.22425280`. Classification: **`technical_issue`**.

Availability: not attempted; no source URL in frozen metadata. Administrative consequence of the catastrophic batch stop; no individual scientific or acquisition outcome exists. Not a scientific non-promotion or excessive-conservatism observation.

### agent_memory / 8: Who Did It? Sleep, Source Memory, and Action Memory in Human 4-Year-Olds

Canonical ID: `doi:10.3390/bs16091578`. Classification: **`technical_issue`**.

Availability: not attempted; no source URL in frozen metadata. Administrative consequence of the catastrophic batch stop; no individual scientific or acquisition outcome exists. Not a scientific non-promotion or excessive-conservatism observation.

### deep_research / 1: An immune world model for multiscale forecasting and therapeutic hypothesis generation

Canonical ID: `doi:10.48550/arxiv.2609.14709`. Classification: **`technical_issue`**.

Availability: not attempted; known source URL exists. Administrative consequence of the catastrophic batch stop; no individual scientific or acquisition outcome exists. Not a scientific non-promotion or excessive-conservatism observation.

### deep_research / 5: SciHazard: A Benchmark for Measuring Scientific Safety Risks with Decomposed Harm Scoring

Canonical ID: `openalex:W7170225285`. Classification: **`technical_issue`**.

Availability: not attempted; known source URL exists. Administrative consequence of the catastrophic batch stop; no individual scientific or acquisition outcome exists. Not a scientific non-promotion or excessive-conservatism observation.

### deep_research / 8: Recent Advances in AI for Automated ICD Coding: A Systematic Literature Review

Canonical ID: `doi:10.1007/s10916-026-02429-7`. Classification: **`technical_issue`**.

Availability: not attempted; known source URL exists. Administrative consequence of the catastrophic batch stop; no individual scientific or acquisition outcome exists. Not a scientific non-promotion or excessive-conservatism observation.

The five unattempted audit entries were retained exactly. Their `technical_issue` classification denotes the batch-level interruption, not five additional technical-failure observations. No manuscripts were acquired after stopping solely to fill the audit. Scientific defensibility and conservatism for those papers are not assessable.

## Disagreement audit

No primary-PASS/adjudicator-non-PASS case occurred. Both actual judgments were PASS. The frozen implementation requires agreement, but this aborted sample provides no empirical disagreement-handling observation. Neither output was modified.

## Selectivity

| Observable | Agentic Memory | Deep Research | Engram | Overall |
|---|---:|---:|---:|---:|
| Selected | 8 | 8 | 0 | 16 |
| Attempted | 1 | 0 | 0 | 1 |
| Manuscripts available | 1 | 0 | 0 | 1 |
| Primary PASS | 1 | 0 | 0 | 1 |
| Adjudicator PASS | 1 | 0 | 0 | 1 |
| Persisted promotions | 0 | 0 | 0 | 0 |
| Disagreements | 0 | 0 | 0 | 0 |
| Attempted non-promotions | 1 | 0 | 0 | 1 |
| Technical failures | 1 | 0 | 0 | 1 |
| Observed unavailable manuscripts | 0 | 0 | 0 | 0 |
| Not attempted after stop | 7 | 8 | 0 | 15 |

Observed technical failure rate is **1/1 attempted (100%)**, also **1/16 selected (6.25%)** and **1/8 Agentic Memory selected (12.5%)**. The latter rates must not dilute the systematic failure because 15 papers were never attempted. Primary/adjudicator pass rates are 1/1 each among invoked roles; completed promotion rate is 0/1 attempted. Other-track attempted rates and all Engram rates are undefined. Fifteen entries have untested manuscript availability, even where metadata lacks a URL. There is no promotion target, no estimate of false-promotion precision and no credible assessment of systematic scientific conservatism from this aborted sample.

## Cost

Public OpenRouter provider pricing was refreshed before execution and matched the frozen caps ([primary endpoints](https://openrouter.ai/api/v1/models/deepseek/deepseek-v4-pro-0813/endpoints), [adjudicator endpoints](https://openrouter.ai/api/v1/models/anthropic/claude-sonnet-4.6/endpoints)). Eight roster entries had known source URLs, none cached. The pre-call estimate allowed up to eight calls per role, about 800,000 input / 24,000 output tokens and **$2.1912** under typical-size assumptions. The maximum-size byte reserve was **$12.5828736**, not a spending authorization. Incremental byte/output reservations enforced the existing remaining **$5.8384777454** balance before every call.

| Component | Calls | Input tokens | Output tokens | Reported USD |
|---|---:|---:|---:|---:|
| Primary assessor | 1 | 22,040 | 959 | $0.01826664 |
| Independent adjudicator | 1 | 27,937 | 368 | $0.08933100 |
| Retry / recovery | 0 | 0 | 0 | $0.00000000 |
| Batch-3 engineering PR review | 0 | 0 | 0 | $0.00000000 |

**Total Batch-3 scientific inference: $0.10759764.** No unknown-charge calls or cache discounts. One fresh manuscript acquisition, zero cache hits, zero alternate-source recovery. Offline replay has zero inference cost. Primary provider: Sail Research; adjudicator: Claude Platform on AWS.

Prior engineering/recovery costs are excluded from this Batch-3 inference total but remain in the shared ledger. Prior charged/reserved **$4.1615222546** plus Batch 3 gives **$4.2691198946** under the unchanged **$10** ceiling. Prior unknown charges remain reserved; no ceiling was reset.

## Historical integrity and full validation

All **628 historical assessment rows** are logically byte-equivalent by canonical row hash: 328 Agentic Memory, 252 Deep Research, 48 Engram. Every historical current decision is unchanged, including the original 28 calibration papers, original Batch 2, recovery and recovery-v2 outcomes. **Zero rows appended**, because the first insert failed and execution stopped. All other baseline runtime tables and all **1,342 preexisting report/manifest files** are unchanged.

The complete **350-test suite passed**. All three tracks passed relevance, quality/promotion, discovery, idempotency and offline site builds. Sidecar schemas, relative links, exposure/secret scans, workflow/YAML validation, generated-size checks, all-history readability, three-database snapshot/restore, legacy two-database restore and `git diff --check` passed. All 109 frozen implementation/configuration/test/workflow/dependency files match their pre-run hashes. Evaluations ran on copies so historical dated reports were not overwritten.

Runtime snapshot SHA-256: `46486a9d7b9c74920a24792edfff0877503728ccb7cc3bfc2172282aa6ede098`. The snapshot is retained in ignored operator storage and restores to the validated database hashes. Passing software tests does not override the observed receipt/persistence failure.

## Persistence and public site

Publication status: **validated; single deploy-only Pages publication pending**. Only empty production promotion fields and generation timestamps. All prior scientific fields and library admissions unchanged. All tables logically unchanged; validated snapshot retained locally. Existing durable release asset retained without needless overwrite. Pages dispatches: 0.

No runtime DB, API key, PDF cache, raw response envelope or hidden reasoning is committed. Frozen manifests, hash, reviewed outcome summary, audit observations, costs and this report are version controlled. The failing paper remains honestly `not_assessed` in production/search because no row exists; its technical failure is explicitly recorded here, not silently treated as a scientific rejection or repaired in the database.

## Generalization criteria and verdict

| Criterion | Assessment |
|---|---|
| No catastrophic/systematic defect | FAIL — deterministic serialization rejects a valid promotion receipt before persistence. |
| Low isolated explained technical failures | FAIL — first attempt fails; general code path, not an external transient. |
| Zero manual corrections | PASS — none. |
| Every audited promotion defensible | No promotions; precision unestimated. |
| No systematic unsupported claims in promoted papers | No promoted sample; cannot establish. |
| Disagreement fails closed | Required by frozen code; no live disagreement observed. |
| Correct provenance | Correct source/context before storage; exact excerpt mismatch introduced by deserialization. |
| No systematic extreme conservatism | Not assessable from the aborted scientific sample; withholding observed here is technical. |
| Assessor/adjudicator independence | PASS for the one observed pair; no hidden reasoning shared. |
| Historical outcomes unchanged | PASS. |
| Full repository validation | PASS. |

Failure is determined by the reproducible production persistence defect, independently of promotion rate. Operational use is not ready. The defect remains unfixed as required; no patch-and-resume, additional batch or recurring automatic assessment was started.

ORIGINAL_BATCH_2_GENERALIZATION_RESULT = FAIL
BATCH_2_RECOVERY_CHECK = FAIL
BATCH_2_RECOVERY_V2_CHECK = FAIL
QUALITY_PROMOTION_GATE_READY_FOR_BATCH_3 = YES (historical engineering-readiness statement; not operational readiness)

QUALITY_PROMOTION_GATE_GENERALIZATION_CHECK: FAIL

QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
