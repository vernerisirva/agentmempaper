# Batch 3 receipt recovery and continuation — 2026-09-17

**The receipt fix was reviewed and merged; the first-paper live recovery failed on a new adjudicator schema violation. The remaining 15 papers were not run.** No scientific output was repaired, no retry was made, and no implementation changed during execution.

## Immutable original result

ORIGINAL_BATCH_3_GENERALIZATION_RESULT = FAIL

Reason: production receipt validation rejected scientifically accepted output because of whitespace normalization mismatch. The original report, manifest, failed attempt and $0.10759764 cost remain unchanged.

## Canonical state

Clean canonical main: `96c6de8955f782a0239090ef71c3f09b87702099`. At this starting SHA, all 109 implementation/config/test/workflow files matched frozen Batch-3 hashes. Commits after the original execution contained reports, manifests and generated publication artifacts, with no implementation changes. Manifest SHA-256: `d1dc21c7fb0e0f4575f714331dfd8b5671ef2876da808b5eec55497bc741fc8b`.

## Exact root cause

Both saved final responses pass their original JSON schemas. Offline reconstruction before coding matched both original request payloads, validated the in-memory receipt, and reproduced the persistence exception with zero network calls or production writes.

Path: `PaperStore.save_quality_assessment` → `QualityAssessment.from_dict` → `QualityEvidence.from_dict` → `_optional_text` → `str.strip()` → `QualityAssessment.__post_init__` → `validate_receipt`. After model JSON parsing, eleven source excerpts lose exactly one trailing ASCII space (`U+0020`, UTF-8 hex `20`). Canonical `source_blocks[0].text` remains exact. The equality assertion raises `persisted snippet or citation mapping mismatch`, wrapped as `invalid dual-promotion receipt`, before insertion. Scientific content is identical; no decision, rationale or evidence ID differs.

| Evidence suffix | Expected characters | Old deserialized characters | Removed UTF-8 bytes |
|---|---:|---:|---|
| B0002 | 894 | 893 | `20` |
| B0006 | 887 | 886 | `20` |
| B0018 | 895 | 894 | `20` |
| B0019 | 881 | 880 | `20` |
| B0029 | 899 | 898 | `20` |
| B0030 | 899 | 898 | `20` |
| B0036 | 897 | 896 | `20` |
| B0041 | 887 | 886 | `20` |
| B0045 | 899 | 898 | `20` |
| B0049 | 892 | 891 | `20` |
| B0081 | 887 | 886 | `20` |

The complete raw final primary and adjudicator strings, parsed objects, expected receipt, exact expected/actual excerpt strings and UTF-8 hex are preserved privately in `data/cache/operator/batch-3-receipt-recovery-20260917/exact-reproduction.json`. Original provider envelopes and request bodies remain in the untouched original operator directory. Raw responses and manuscript contexts are not committed or exposed through public cards.

Receipt fields before the fix: `outcome`, `calls`, `run_id`, `total_request_limit`, `attempt_limit_per_role`, `primary_model`, `adjudicator_model`, `context`, `manuscript_identity`, `primary`, `adjudicator`, `provenance_status`.

## Engineering representation

`canonical-response-v1`: strict parse → unchanged schema/identity validation → sorted object keys and compact JSON → strict UTF-8 SHA-256. No Unicode normalization or string trimming. Arrays retain order. JSON outer whitespace, indentation, object-key order and escaped/unescaped equivalent Unicode serialize identically. Schema enums are unchanged: `" pass "` remains invalid.

Each call retains exact raw final content, raw-content SHA-256, canonical-response SHA-256 and a binding checksum over the canonical hash plus role/model/context/request/run. Displayed rationale, limitations and concerns must match model judgments. Completed non-promotions use the same contract. Checksums establish internal integrity, not provider signatures or authenticity against coordinated rewriting of all records and hashes. Hidden reasoning is excluded.

Exact canonical excerpts bypass only the legacy optional-display-text trimmer at dual-gate deserialization. Older historical gate formats retain their previous behavior. There are zero historical dual-gate rows; all 628 historical rows use legacy formats.

Seven focused new tests cover the exact first affected excerpt, a real temporary storage round trip, layout/key ordering, raw preservation, Unicode/decomposed Unicode, meaningful whitespace, decisions/evidence/rationale/required/extra fields, array ordering, request/model/run substitutions, duplicate JSON keys and invalid Unicode. Both exact original saved responses also pass a separate offline production store replay without any repair or new scientific outcome.

## PR and independent review

[PR #35](https://github.com/vernerisirva/agentmempaper/pull/35) merged at **`429598aca87160009a57bf3c5ba1116b9225acc2`**, 2026-09-17 20:02:34 UTC. The merge tree exactly equals reviewed candidate `763e92673a5ebde107c095b7de16d70e78473f58`. [Required CI](https://github.com/vernerisirva/agentmempaper/actions/runs/35268228554) passed. The base was unchanged, the tree clean, the PR mergeable, and no material unreviewed change remained.

DeepSeek returned no visible verdict after exhausting its completion budget. The established bounded Opus 4.6 escalation returned **PASS**, zero blockers, zero notes and no reported test gaps. It covered all six changed files plus complete integrity dependencies and test helpers without truncation (110,427 request bytes). No source change followed this review. Final full test count: **357**.

## First-paper recovery

Phase: **BATCH_3_FIRST_PAPER_RECOVERY**. Paper: **Causal Path Alignment: Anchoring the Optimization Trajectory for Controllable In-Parameter Knowledge Editing**, `doi:10.24963/ijcai.2026/655`.

The production service ran once with the same primary `deepseek/deepseek-v4-pro-0813`, adjudicator `anthropic/claude-sonnet-4.6`, scientific schemas, rubric, prompts, model parameters, evidence rules and promotion rule. A frozen inventory of 114 implementation/config/test/workflow/operator files was checked before every request and after execution. No force refresh, retry, model substitution or manual correction occurred.

| Check | Actual result |
|---|---|
| Acquisition | Cached original 13-page arXiv manuscript; zero unreadable pages, zero body omissions, no extraction truncation. |
| Identity/provenance | PASS; original source SHA-256 `bbd08d38d12ccd97766992bfbb6e3cd58adb1e540d9750aec247549a4db3a7e5` and context `d5aba638083f7fcadacd84049347c421a546017878e3272dbe8e285e4072afac`. |
| Primary | Accepted PASS; 18 evidence IDs; canonical response and request/run binding validate. |
| Adjudicator transport | Completed normally; expected model and `finish_reason=stop`. |
| Adjudicator scientific response | Raw decision is PASS, but **not accepted**: 26 evidence IDs exceed the unchanged schema maximum of 24. |
| Full dual receipt | Not completed; strict schema validation rejects the adjudicator before issuing its canonical receipt. |
| Persisted production result | `quality_status=uncertain`, `outcome=protocol_failure`, `error_type=ValidationError`; exactly one append. |
| Promotion | None; review candidate only. |
| Automatic/manual | Entirely automatic; zero output repairs, zero retries, zero post-failure scientific calls. |

The request explicitly used `strict: true`, `provider.require_parameters: true`, and `evidence_ids.maxItems: 24`. The provider nevertheless returned 26 unique IDs. All 26 are in the correct manuscript context, but that does not make the response schema-valid. An offline diagnostic reproduced `ValidationError` at `schema.properties.evidence_ids.maxItems`. It did not remove IDs, relax the schema, substitute a decision or issue a new outcome. Raw final content and raw hashes for both roles remain preserved; the rejected adjudicator has no canonical-response/binding hash falsely marked successful.

Execution stopped at **2026-09-17T20:05:37.364485+00:00**. This is a newly observed provider/schema protocol failure, distinct from the repaired excerpt-trimming bug. Its systematic frequency cannot be estimated from one attempt. The first-paper recovery criterion requires both validated roles, so it **FAILS** regardless of the raw PASS prose. The exact original responses now round-trip offline, but this fresh live attempt did not reach a successful complete dual receipt.

## Remaining frozen 15-paper holdout

**BATCH_3_REMAINING_HOLDOUT_RESULT: NOT_RUN.** The recovery gate remained closed. All fifteen retain zero scientific assessment rows across all three runtime databases; none received primary assessment/adjudication, was acquired or scientifically inspected for this engineering fix, or was used in a fixture or external code review. Only the already-exposed first paper supplied the exact excerpt regression. Original selection positions and the manifest bytes remain unchanged.

| Track / frozen position | Paper / canonical ID | Primary | Adjudicator | Promotion | Technical state |
|---|---|---|---|---|---|
| agent_memory / 2 | nox-mem: Pain-Weighted Hybrid Memory for LLM Agents · `doi:10.5281/zenodo.22649269` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| agent_memory / 3 | Contextualized Reinforcement Learning with Episodic Memory Networks · `doi:10.5281/zenodo.22587729` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| agent_memory / 4 | Hierarchical Reinforcement Learning with Memory Networks · `doi:10.5281/zenodo.22623238` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| agent_memory / 5 | Delete Names Five Operations: Erasure Semantics for Derived Agent Memory, and Why a State-Level Definition Cannot Be the Auditable One · `doi:10.5281/zenodo.22425280` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| agent_memory / 6 | retainkit: context and memory policies for LLM agents, scored by the evidence that survives the token budget · `doi:10.5281/zenodo.22352965` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| agent_memory / 7 | Hierarchical Reinforcement Learning with Temporal Abstraction and Memory · `doi:10.5281/zenodo.22336737` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| agent_memory / 8 | Who Did It? Sleep, Source Memory, and Action Memory in Human 4-Year-Olds · `doi:10.3390/bs16091578` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| deep_research / 1 | An immune world model for multiscale forecasting and therapeutic hypothesis generation · `doi:10.48550/arxiv.2609.14709` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| deep_research / 2 | AppliedScientist: Automated Scientific Revision Through Iterative AI Reviewing · `openalex:W7213371831` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| deep_research / 3 | Cracking a 600-Year-Old Mystery with Geometry: The Voynich Manuscript Finally Speaks — An Ô-HAT Cross-Language Phase-Space Analysis · `doi:10.5281/zenodo.21493208` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| deep_research / 4 | Artificial Intelligence for Water Sustainability and Climate Adaptation in Small Island States · `doi:10.70593/978-93-7185-684-3` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| deep_research / 5 | SciHazard: A Benchmark for Measuring Scientific Safety Risks with Decomposed Harm Scoring · `openalex:W7170225285` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| deep_research / 6 | PEARL: Auditable Repair for Scientific Reasoning Graph Extraction · `openalex:W7170112970` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| deep_research / 7 | DRNOISE: Benchmarking Deep Research Agents in Misleading Evidence Environments · `openalex:W7170112771` | — | — | None | NOT_RUN_RECOVERY_FAILED |
| deep_research / 8 | Recent Advances in AI for Automated ICD Coding: A Systematic Literature Review · `doi:10.1007/s10916-026-02429-7` | — | — | None | NOT_RUN_RECOVERY_FAILED |

No stopped holdout entry is counted as scientific uncertainty, manuscript unavailability or an individually observed technical failure. The exact original roster remains in the [immutable manifest](../../experiments/manifests/batch-3-roster-2026-09-17.json); its SHA-256 remains `d1dc21c7fb0e0f4575f714331dfd8b5671ef2876da808b5eec55497bc741fc8b`.

## Audits

**Promotions:** none. The all-promotions audit set is empty, and promotion precision is unestimated.

**Disagreements:** no accepted primary-PASS/adjudicator-non-PASS scientific disagreement. This is one primary PASS with an invalid adjudicator response, withheld automatically. The raw adjudicator PASS must not be counted as an accepted second PASS or relabeled as scientific uncertainty.

**Frozen sample:** agent_memory positions 1, 5, 8; deep_research positions 1, 5, 8; Engram has no selected paper. Position 1 in Agentic Memory is classified `technical_issue`: correct source/context, accepted primary receipt, but invalid adjudicator array cardinality and no promotion. Its original failed-attempt scientific audit remains unchanged in the [original report](batch-3-promotion-gate-evaluation-2026-09-17.md). No new scientific audit can turn this invalid recovery into a pass. The other five frozen sample entries remain unattempted, with no manuscript inspection solely to fill the audit; no replacement sample was chosen.

The five unattempted sample entries are Delete Names Five Operations, Who Did It?, An immune world model, SciHazard, and Recent Advances in AI for Automated ICD Coding, at their exact frozen IDs above. Scientific defensibility, unsupported-claim patterns and systematic conservatism cannot be estimated from this aborted recovery. The observed withholding is technical. A credible promotion audit and a passing remaining-holdout experiment have not been established.

## Historical integrity and final validation

All **628 prior assessment rows** are unchanged by canonical row hashes: 328 Agentic Memory, 252 Deep Research and 48 Engram. One automatic technical recovery row was appended in Agentic Memory, giving **629** readable assessments. No historical current decision was replaced: the recovered paper had no prior assessment row. Other runtime tables remain unchanged except the necessary, explicitly verified assessment-row sequence increment. All **1,417** baselined reports/manifests/original private failure artifacts match their pre-fix hashes.

Final validation: **357 tests PASS**; relevance, quality/promotion, discovery, idempotency and offline site builds PASS for all three tracks; sidecar schemas, relative links, exposure/secret scans, workflow/YAML validation, generated-size guards, three-database snapshot/restore, legacy two-database restore and `git diff --check` PASS. All 114 frozen files match through the end of recovery. No implementation changed during live execution, and no holdout was executed. Evaluations ran on temporary copies, preserving historical dated reports.

The initial engineering full-suite run hit the preexisting legacy curation row-count assertion (4 versus 2); its isolated rerun, the subsequent full engineering run, CI and the final full run passed without a source/test change. The post-execution validation harness initially expected every SQLite table hash to be unchanged; it was adjusted to verify the single legitimate `sqlite_sequence` increment from the appended failure row. This was an audit-harness bookkeeping correction, not a scientific-pipeline or result change.

Runtime snapshot SHA-256: `18174aa7fc90e90bccc8038b09ae3477aece4e706b26ab988387e598f6a47ee5`.

## Costs

Original Batch-3 inference remains **$0.10759764**, unchanged and separate from this task.

| Engineering review | Calls | Input tokens | Output tokens | USD | Verdict |
|---|---:|---:|---:|---:|---|
| DeepSeek v4 Pro | 1 | 9,951 | 16,384 | $0.0343270224 | No accepted verdict; all completion tokens reported as reasoning, zero visible output. |
| Claude Opus 4.6 | 1 | 30,852 | 56 | $0.1556600000 | PASS; zero blockers. |
| **Engineering total** | **2** | **40,803** | **16,440** | **$0.1899870224** | |

| Scientific phase / role | Calls | Input tokens | Output tokens | USD |
|---|---:|---:|---:|---:|
| First-paper recovery / primary | 1 | 22,427 | 1,032 | $0.01479006804 |
| First-paper recovery / adjudicator | 1 | 28,038 | 518 | $0.09188400000 |
| **First-paper recovery total** | **2** | **50,465** | **1,550** | **$0.10667406804** |
| Remaining holdout / primary | 0 | 0 | 0 | $0 |
| Remaining holdout / adjudicator | 0 | 0 | 0 | $0 |
| Retries / additional recovery calls | 0 | 0 | 0 | $0 |

Both scientific calls report zero reasoning/cache tokens. All new call charges are known. Approval-review blocks occurred before dispatch and incurred no inference charge. New engineering plus scientific costs total **$0.29666109044**, labeled separately above. Previous charged/reserved $4.2691198946 plus this task gives **$4.56578098504** under the unchanged shared **$10** ceiling, leaving **$5.43421901496**. Prior unknown reservations remain included; the budget was not reset. [Public provider pricing](https://openrouter.ai/api/v1/models) was refreshed before recovery and remained within the frozen caps.

## Persistence and publication

Local runtime persistence and complete validation are finished. Durable upload and the single reviewed Pages deployment are pending; this section will be completed with verification evidence.

No recurring operational quality assessment was started. No Batch 4 was selected or run. The stop rule prevented further scientific calls; no bug was patched during recovery and no result was manually altered.

ORIGINAL_BATCH_3_GENERALIZATION_RESULT = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_CHECK: FAIL
BATCH_3_REMAINING_HOLDOUT_RESULT: NOT_RUN
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
