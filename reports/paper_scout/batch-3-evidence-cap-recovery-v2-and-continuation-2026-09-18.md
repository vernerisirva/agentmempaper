# Batch 3 evidence-cap recovery-v2 and stopped holdout — 2026-09-18

**The evidence-cap fix is reviewed and merged, and first-paper recovery-v2 passed. The remaining holdout failed after an audit exposed a different, systematic manuscript-selection defect. Execution stopped without patching, resuming or correcting scientific output. Operational readiness remains NO.**

## Immutable history

```text
ORIGINAL_BATCH_3_GENERALIZATION_RESULT = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_CHECK = FAIL
```

The [original Batch-3 failure](batch-3-promotion-gate-evaluation-2026-09-17.md) and [first failed recovery](batch-3-receipt-recovery-and-continuation-2026-09-17.md) retain their reports, timestamps, exact responses, receipts/provenance and costs. A successful later recovery does not retroactively correct either experiment.

Canonical main was fetched and fast-forward verified clean at **`268640c470e05e8455a0501afb9e8f479a9675fd`**. PR #35 was MERGED. The persisted first recovery was one `protocol_failure` assessment with `error_type=ValidationError`. The runtime contained 629 assessments (the original 628 plus that failure). All remaining 15 frozen papers had zero assessment/adjudication records across all three databases. They were not acquired or scientifically inspected during engineering and were absent from the engineering diff and independent reviewer payloads.

## Root cause and complete contract investigation

The exact saved adjudicator response has **26 distinct evidence IDs versus a maximum of 24**. All 26 belong to the correct manuscript/context; none is invented, duplicated, or an identical-text duplicate. Offline `validate_response` reproduces `jsonschema.ValidationError` at `properties.evidence_ids.maxItems`, before receipt completion. No response was edited or replayed as a new scientific result.

The cap was introduced in `paper_scout/promotion_protocol.py::schema` in commit `02a691cee661727ae7601033b52c16b00ae26961`, shared by both scientific roles. No numerical rationale was recorded in that commit, tests, design report or cost manifest. It is a schema/engineering bound, not an established scientific threshold, a model context limit or a UI/database invariant.

The old adjudicator instruction requested its own supplied evidence IDs and counterevidence, but did not state the numerical cap or ask for a minimal sufficient set. The actual original request already used:

```json
{"response_format":{"type":"json_schema","json_schema":{"name":"promotion_adjudicator_v1","strict":true,"schema":{"type":"object","properties":{"canonical_id":{"type":"string","minLength":1},"source_content_hash":{"type":"string","minLength":1},"context_id":{"type":"string","minLength":1},"evidence_ids":{"type":"array","items":{"type":"string","minLength":1},"maxItems":24,"uniqueItems":true},"promotion_decision":{"enum":["pass","uncertain"]},"blocking_reasons":{"type":"array","maxItems":12,"items":{"type":"string","minLength":1}}},"required":["canonical_id","source_content_hash","context_id","evidence_ids","promotion_decision","blocking_reasons"],"additionalProperties":false}}},"provider":{"require_parameters":true,"max_price":{"prompt":3.3,"completion":16.5}}}
```

The response came through Claude Platform on AWS. [OpenRouter documents endpoint-dependent enforcement](https://openrouter.ai/docs/guides/features/structured-outputs); [Claude's native schema subset](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations) excludes array constraints beyond `minItems` 0/1. Thus sending `maxItems` does not establish a hard decoding guarantee on this route. The original request was accepted but the returned array violated it. We preserve the strict schema and runtime cap rather than claim newly added native enforcement, downgrade to generic JSON, switch models, or use response healing.

The 26 cited blocks covered overlapping scientific topics: abstract/introduction contribution statements, results tables plus discussion, and repeated limitations. This is potential semantic redundancy, not proof that specific blocks are dispensable. No human or program selected a replacement subset. The schema has one global evidence list per role and no reusable per-field references; no large redesign was necessary.

## Contract decision and focused fix

Keep **24** and make it a named constant shared by generation and validation. Its explicit engineering rationale is six existing quality dimensions with a planning allowance of four source blocks each (direct support, method detail, comparison/validation and counterevidence). This is a total flexible budget, not per-dimension quotas, minimum citation counts or a new scientific sufficiency rule. A 24-ID array uses about 625 compact JSON bytes; two accepted roles produce at most 48 source blocks, compatible with existing sidecars and the 4,096-output-token/request budget. The number was not enlarged to fit one failed response.

The adjudicator now explicitly requests at most 24 distinct IDs and the smallest sufficient, strongest, non-duplicative evidence set supporting the final decision, blockers and major quality dimensions. The scientific rubric, primary request, models, promotion rule, evidence semantics, relevance rules, manuscript selection and frozen audit sample remain unchanged.

A final-response syntax/schema violation permits **one fresh adjudication**, reconstructed from the same original context and unchanged primary final judgment. The rejected adjudication, its conclusion and any hidden reasoning are never supplied. No slicing, deduplication, manual correction or scientific decision forcing occurs. A valid retry controls the outcome independently; a second violation returns technical protocol failure with no promotion. Primary, transport, returned-model and provenance failures do not retry. Each HTTP request still has one transport attempt; there are at most three model requests per paper.

Runtime validation rejects excess/duplicate/invented/foreign evidence IDs, wrong manuscript/version/context and malformed output. New `adjudicator-contract-retry-v1` receipts retain raw final content, all attempt costs and bindings to run, request, role, model, context, attempt and status. Completed retry receipts revalidate the rejected attempt's contract failure and the final successful response. Historical two-call receipts retain their contract. Checksums prove internal consistency, not provider signatures or completeness of manuscript selection.

## Engineering, review and merge

- Branch: `fix-adjudicator-evidence-cap`.
- [PR #36](https://github.com/vernerisirva/agentmempaper/pull/36); reviewed candidate `3c31f35fc12c968cf9032f7e2097c73a90409af0`.
- Independent `pr-review --base origin/main`: DeepSeek exhausted its fixed completion budget with no accepted verdict; the established bounded Opus 4.6 escalation returned **PASS**, zero blockers, notes, test gaps or uncertainties. All four changed files and full integrity/test dependencies were included without truncation (129,076 request bytes).
- **366 tests pass**, including 24/25/26 boundaries, generation schema, one fresh retry, no third attempt, independent decision changes in both directions, no truncation, duplicates/foreign IDs, rejected-attempt tampering, cost/provenance storage and legacy receipts.
- [Required CI passed](https://github.com/vernerisirva/agentmempaper/actions/runs/35314055877). Clean tree, unchanged base, mergeable reviewed head, no unresolved blockers or material unreviewed changes.
- Automatic merge: **`beee6fcc2d052f952be5d5b59281be0a3f67a896`**, 2026-09-18 06:16:58 UTC. Merge tree equals the reviewed candidate.

A 117-file implementation/configuration/test/workflow/operator inventory was frozen before scientific execution and checked before every request and after execution. No source changes occurred during either phase. The newly discovered selection defect is deliberately **unfixed**.

## First-paper recovery-v2

Phase: **BATCH_3_FIRST_PAPER_RECOVERY_V2**. Same frozen first paper: Causal Path Alignment, `doi:10.24963/ijcai.2026/655`, same cached 13-page manuscript, source SHA-256 `bbd08d38d12ccd97766992bfbb6e3cd58adb1e540d9750aec247549a4db3a7e5`, context `d5aba638083f7fcadacd84049347c421a546017878e3272dbe8e285e4072afac`.

| Check | Result |
|---|---|
| Primary | PASS, 24 evidence IDs |
| Adjudicator attempt 1 | PASS, 24 evidence IDs, schema valid |
| Retry | None; retry evidence count not applicable |
| Receipt / provenance | PASS / PASS; production store round trip validates |
| Scientific result | Promoted by the unchanged dual-pass rule |
| Persistence | One new append; earlier failed recovery retained |
| Manual corrections / truncation | 0 / 0 |
| Cost | $0.12433932 |

Recovery-v2 completed at 06:18:37 UTC and satisfies all seven technical recovery criteria. This is a separate successful recovery, not a fresh unseen experiment. The live retry branch was not exercised; its behavior is supported by deterministic tests only.

## Remaining frozen holdout and mandatory stop

The post-recovery unseen check passed before the first holdout request: all 15 had zero scientific records, none was used in fixtures or reviewer context, and original roster bytes/order were unchanged. Manifest SHA-256 remains `d1dc21c7fb0e0f4575f714331dfd8b5671ef2876da808b5eec55497bc741fc8b`.

**New systematic defect:** the acquired immune-world-model manuscript has 21 pages. Its substantive **STAR METHODS** section occupies pages 17–21, after references. `_detect_sections` does not recognize that heading, keeps `current_heading=References`, and labels **15,196 characters** on those five pages as references. Both scientific roles receive pages 1–12 only, while coverage incorrectly reports `omitted_body_characters=0`; 28,462 characters are labelled excluded back matter. Identity, byte hashes and receipt checks remain valid for the incomplete selected context. This is a general selection/coverage defect, not a response-cap recurrence or ordinary scientific disagreement.

Audit stop was recorded at **06:24:03 UTC**, blocking every subsequent request. The SciHazard primary request already in flight returned at approximately 06:24:09 UTC (199.35 seconds); its response, usage and cost were saved. No SciHazard adjudication was dispatched and no assessment row was fabricated. The existing HTTP socket timeout is not a wall-clock bound. No output or selection was corrected, no code was patched, and execution did not resume.

| Track / frozen position | Paper / canonical ID | Public primary | Public adjudicator | Promoted | Execution / publication state |
|---|---|---|---|---|---|
| agent_memory / 2 | nox-mem: Pain-Weighted Hybrid Memory for LLM Agents · `doi:10.5281/zenodo.22649269` | — | — | No | manuscript_unavailable |
| agent_memory / 3 | Contextualized Reinforcement Learning with Episodic Memory Networks · `doi:10.5281/zenodo.22587729` | — | — | No | manuscript_unavailable |
| agent_memory / 4 | Hierarchical Reinforcement Learning with Memory Networks · `doi:10.5281/zenodo.22623238` | — | — | No | manuscript_unavailable |
| agent_memory / 5 | Delete Names Five Operations: Erasure Semantics for Derived Agent Memory, and Why a State-Level Definition Cannot Be the Auditable One · `doi:10.5281/zenodo.22425280` | — | — | No | manuscript_unavailable |
| agent_memory / 6 | retainkit: context and memory policies for LLM agents, scored by the evidence that survives the token budget · `doi:10.5281/zenodo.22352965` | — | — | No | manuscript_unavailable |
| agent_memory / 7 | Hierarchical Reinforcement Learning with Temporal Abstraction and Memory · `doi:10.5281/zenodo.22336737` | — | — | No | manuscript_unavailable |
| agent_memory / 8 | Who Did It? Sleep, Source Memory, and Action Memory in Human 4-Year-Olds · `doi:10.3390/bs16091578` | — | — | No | manuscript_unavailable |
| deep_research / 1 | An immune world model for multiscale forecasting and therapeutic hypothesis generation · `doi:10.48550/arxiv.2609.14709` | Withheld | Withheld | No | invalid input; attempted assessment internal only |
| deep_research / 2 | AppliedScientist: Automated Scientific Revision Through Iterative AI Reviewing · `openalex:W7213371831` | pass | pass | Yes | success |
| deep_research / 3 | Cracking a 600-Year-Old Mystery with Geometry: The Voynich Manuscript Finally Speaks — An Ô-HAT Cross-Language Phase-Space Analysis · `doi:10.5281/zenodo.21493208` | — | — | No | manuscript_unavailable |
| deep_research / 4 | Artificial Intelligence for Water Sustainability and Climate Adaptation in Small Island States · `doi:10.70593/978-93-7185-684-3` | Withheld | Withheld | No | front matter only; attempted assessment internal only |
| deep_research / 5 | SciHazard: A Benchmark for Measuring Scientific Safety Risks with Decomposed Harm Scoring · `openalex:W7170225285` | Internal only | — | No | interrupted_after_primary |
| deep_research / 6 | PEARL: Auditable Repair for Scientific Reasoning Graph Extraction · `openalex:W7170112970` | — | — | No | not_attempted_after_stop |
| deep_research / 7 | DRNOISE: Benchmarking Deep Research Agents in Misleading Evidence Environments · `openalex:W7170112771` | — | — | No | not_attempted_after_stop |
| deep_research / 8 | Recent Advances in AI for Automated ICD Coding: A Systematic Literature Review · `doi:10.1007/s10916-026-02429-7` | — | — | No | not_attempted_after_stop |

Totals among the 15: **3 completed dual-call attempts**, **8 manuscript-unavailable outcomes**, **1 interrupted after primary**, **3 never attempted**. There is **1 valid promotion**; **2 attempted assessments are withheld from public scientific results because their manuscript representations are incomplete**. A completed call pair or valid receipt is not proof of a valid scientific assessment. Eleven assessment rows were appended. Seven model calls occurred: four primaries and three adjudicators, with **zero contract retries**. No cap violation or transport failure occurred. The methods-selection defect invalidates the batch-level technical/generalization criterion even though individual receipts validated. Unattempted entries are not counted as scientific uncertainty or manuscript unavailability.

## Audit

**All promotions — Causal Path Alignment (recovery-v2): defensible scoped promotion, with a citation-quality caveat.** Canonical B0035–B0037 support the two-stage method; B0038–B0039 the 2,000 edits/five repeats and benchmarks; B0041/B0045–B0051 the comparisons, ablations and transfer; B0073/B0079/B0081–B0082 the latency, zsRE and sequential-edit limitations. The primary's consecutive B0002–B0025 list alone does not trace its detailed later-section claims adequately. The independent adjudicator's actual citations supply the missing method/evaluation/limitations support in the final evidence union. That weakness is preserved, not repaired. The findings support this scoped study, not universal shortcut elimination or independent reproduction of its code.

**All promotions — AppliedScientist (Deep Research / 2): defensible scoped promotion.** B0015/B0022/B0024–B0025 describe the scientist/reviewer separation and revision mechanism; B0028–B0029 specify the 30-paper cohort and fixed-prompt comparison; B0036–B0037 provide external-reviewer trajectory evidence; B0039–B0040 support 128/150 execution weaknesses versus 2/18 idea weaknesses; B0064 explains the compute-limited sample. Circular use of the guiding reviewer and external scoring only of human-initialized trajectories are explicitly acknowledged. These support a limited empirical revision study, not proof of future venue acceptance or independently verified scientific truth. The cited final evidence is from the correct manuscript. Neither promoted judgment relies on author or venue prestige.

**Invalid input — immune world model (Deep Research / 1): pipeline defect; no valid public scientific-quality decision.** Five STAR METHODS pages were silently excluded. The attempted assessment therefore cannot establish scientific quality or justify a scientific rejection. Its exact judgments, unsupported reasoning, receipt and original stored outcome remain unedited in historical/internal state only. The public paper retains its prior `not_assessed` state in the review library. No revised decision was inferred from the omitted methods, and no reassessment occurred.

**Frozen non-promotion sample — Agentic Memory / 5 and / 8:** manuscript unavailable through the frozen source candidates, no scientific calls. These are availability outcomes, not evidence of low quality or excessive scientific conservatism. No alternate manuscript was retrieved solely for audit.

**Frozen sample — SciHazard (Deep Research / 5): `technical_issue` from the global stop, not a completed scientific assessment.** A schema-valid primary response with 24 evidence IDs was preserved internally. No adjudication, completed receipt, production assessment row or public quality decision was created. It remains `not_assessed` and unpromoted.

**Frozen sample — Recent Advances in AI for Automated ICD Coding (Deep Research / 8):** never attempted after the stop, no manuscript inspected and no replacement sample. Scientific quality is not assessable here.

**Incomplete source — water sustainability book (Deep Research / 4): no valid public scientific-quality decision.** The supplied 12-page PDF contains front matter and contents only. Its attempted judgments and the audit of unsupported reasoning remain intact in historical/internal state. Publication also excludes this incomplete-input assessment; the paper retains its prior `not_assessed` state in the review library. Withholding publication is not a scientific rejection or a corrected assessment.

No audited promoted paper shows a demonstrated false-promotion concern, but two observed promotions (only one in the unseen holdout) cannot establish high population precision. The input-loss defect and unsupported non-promotion reasoning prevent a credible operational-readiness claim or a reliable estimate of systematic conservatism. The audit is sufficient to establish **FAIL**, not to rescue the aborted holdout.

## Historical integrity and complete validation

All **629 pre-task assessment rows** are unchanged by canonical row hashes, including all original 628 historical rows and the first failed recovery. Exactly **12** new production rows were appended: eight Agentic Memory (one recovery-v2 plus seven unavailable), four Deep Research, zero Engram. Total readable assessments: **641**. All non-assessment tables are unchanged, and only the expected assessment sequence increments occurred. No current decision outside this execution was replaced.

All **1,488 baselined reports/manifests/original private failure artifacts** retain their hashes. Both frozen-phase inventories match all **117** files. Original request/response/provenance/cost/timestamp artifacts remain untouched. New complete receipts live in append-only runtime history; the interrupted primary's exact request, provider envelope without hidden reasoning, selected context, response, usage and stop record remain in ignored operator storage. It has no misleading completed receipt or fabricated assessment.

Post-execution **366 tests PASS**; relevance, promotion/quality, discovery, idempotency and offline builds PASS across all three tracks. Sidecar schemas, links, exposure/secret scans, workflows/YAML, size guards, three-database snapshot/restore, legacy two-database restore, historical readability and `git diff --check` PASS. Evaluations ran on temporary copies, preserving historical dated reports. These software checks do not override the empirical selection failure.

Runtime snapshot SHA-256: **`156f8278321cf812b024941bb52edd029b951c7afb51d47a2f8d53d9aa5f9553`**.

## Costs

| Phase / role | Calls | Input tokens | Output tokens | USD |
|---|---:|---:|---:|---:|
| Engineering / DeepSeek review (no accepted verdict) | 1 | 11,333 | 16,384 | $0.07972687 |
| Engineering / Opus review (PASS) | 1 | 36,268 | 59 | $0.18281500 |
| **Engineering total** | **2** | **47,601** | **16,443** | **$0.26254187** |
| Recovery-v2 / primary | 1 | 22,041 | 970 | $0.03293532 |
| Recovery-v2 / adjudicator | 1 | 28,028 | 488 | $0.09140400 |
| **Recovery-v2 total** | **2** | **50,069** | **1,458** | **$0.12433932** |
| Remaining holdout / primary | 4 | 64,455 | 4,203 | $0.08034640 |
| Remaining holdout / adjudicator | 3 | 55,910 | 1,785 | $0.19450500 |
| **Remaining holdout total** | **7** | **120,365** | **5,988** | **$0.27485140** |
| Scientific retries | 0 | 0 | 0 | $0 |

New total: **$0.66173259**. All new call charges are reported; unknown/unbilled new inference charges: **none**. The holdout includes the interrupted SciHazard primary's **$0.01862060**, despite there being no assessment row. DeepSeek review metadata inconsistently reports 17,795 reasoning tokens versus 16,384 completion tokens; those raw usage scalars are preserved, and no visible-token count is inferred. All scientific calls report zero reasoning/cache tokens.

Prior charged/reserved **$4.56578098504**, including earlier unknown reservations, plus this task gives **$5.22751357504** under the unchanged **$10** ceiling, leaving **$4.77248642496**. The original Batch-3 $0.10759764 and first recovery $0.10667406804 remain unchanged and separate. Public provider pricing was refreshed before recovery and remained within enforced caps. Approval-review blocks happened before dispatch and cost $0. Read-only public-source evidence resolved the review and first-recovery call blocks. The earlier public runtime-upload attempts were blocked before dispatch; no upload occurred. The publication authorization explicitly prohibits that public database destination, so it will not be used.

## Persistence and publication

Publication is authorized for this Markdown report, its JSON companion and the permitted generated public site artifacts. No assessment/runtime database, archive, raw request/response, receipt store or ignored operator directory is included in the new public commit or Pages artifact.

The public Deep Research build uses a temporary database copy with the immune-world-model and water-sustainability attempted assessments excluded. The original databases are unchanged, including all 641 assessments, their original outcomes and the 629 pre-task rows. Both affected public paper records retain their previous `not_assessed` status and remain outside the main library. The interrupted SciHazard attempt also remains internal and `not_assessed` publicly. This is publication filtering only: no assessment is repaired, no pipeline fix is applied and the failed holdout is not reinterpreted.

Independent public changes remain: the audited Causal Path Alignment recovery-v2 and AppliedScientist promotions, plus eight manuscript-unavailable outcomes (availability records, not scientific-quality rejections). Main-library counts are **5 / 6 / 6**. Timestamp-only file changes are omitted. These legitimate generated changes independently justify a `deploy_only=true` Pages deployment, which skips discovery, assessment and runtime-state upload.

All new requests/responses, stop evidence, audit records and the verified three-database snapshot remain in ignored local storage. Snapshot SHA-256 is `156f8278321cf812b024941bb52edd029b951c7afb51d47a2f8d53d9aa5f9553`; the previous durable asset `18174aa7fc90e90bccc8038b09ae3477aece4e706b26ab988387e598f6a47ee5` is backed up exactly. The established snapshot format and restore mechanism are preserved. However, the configured remote durable-state mechanism is a **public GitHub release**, which the user explicitly prohibits for these databases. No approved private destination is configured, so remote persistence of the new snapshot remains blocked; the existing release asset is unchanged. Local preservation does not constitute completed remote durable persistence.

Publication-specific checks PASS: 32 changed site files and two report files; ten changed paper cards; both incomplete-input paper detail pages/JSON byte-identical to their pre-execution versions; invalid assessment identifiers and substantive judgments absent from Pages; original databases, snapshot hash, 1,488 historical artifacts and frozen implementation unchanged. Schema, link, exposure, workflow, size and diff checks also pass.

Publication completed for permitted artifacts in commit **`76f48b555329a5b96e773cb0864f2aec9a80b1f9`**: this report and its JSON companion plus **32 generated site files**. [Deploy-only Pages run 35316391612](https://github.com/vernerisirva/agentmempaper/actions/runs/35316391612) succeeded for that exact commit. **103 live public artifacts matched the validated local bytes**, including both withheld papers and all changed site files. Runtime restore, bootstrap, discovery/assessment, generated-output commit, snapshot preparation and durable upload steps were all skipped. The existing release asset retained its original ID and SHA-256. No new database or snapshot was uploaded, committed or included in Pages. Remote durable persistence of the new private state remains blocked as described above; publication does not imply that persistence succeeded.

No recurring production quality assessment was started. No Batch 4 was selected. The remaining three unattempted holdout papers remain untouched; SciHazard is now exposed by its primary-only call and must not be relabelled unseen merely because no assessment row exists.

```ini
ORIGINAL_BATCH_3_GENERALIZATION_RESULT = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_CHECK = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_V2_CHECK = PASS
BATCH_3_REMAINING_HOLDOUT_RESULT = FAIL
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE = NO
```
