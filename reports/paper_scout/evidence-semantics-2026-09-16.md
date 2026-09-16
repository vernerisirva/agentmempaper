# Claim-aware evidence support — 2026-09-16

**QUALITY_PIPELINE_READY_FOR_BATCH_2: NO**

Exactly five papers were reassessed once through the merged normal pipeline. All decisions are automatic, with no output corrections or extra scientific reruns. The other 23 original decisions and every prior assessment row are preserved. Batch 2 was not started.

## Before and design

Before: four technical grounding failures caused by mixed Abstract/body references, plus Sci-MMR’s automatic pass containing an unsupported >20% complete-evidence-recovery claim. The [preflight report](evidence-semantics-preflight-2026-09-16.md) records the precise references, section roles and diagnostic limits. Old rejected claim wording was not retained, so it is not reconstructed or invented.

- Blocks retain canonical text, manuscript/context identity, source hash, source offsets, pages and deterministic section roles. Context selection and PDF acquisition are unchanged.
- New `block-evidence-v2` eligibility depends on scientific dimension and `source_claim` versus `assessor_inference`. Abstract is allowed only for an attributed high-level contribution/scope statement in `contribution_clarity`. Novelty/value and body-evidence requirements exclude Abstract, including mixed citations. The prompt enumerates eligible candidates per dimension.
- Numerical validation checks values and common units against the item’s own cited blocks. Formatting normalization does not change values or multipliers. Matching a nearby number is insufficient; metric, population, denominator, comparison and meaning also need support.
- One bounded verifier call checks claims and explanations against their own cited blocks, plus the published narrative against the union of eligible cited sources. It supplies no new evidence or corrected claims. Unsupported interpretations become scientific uncertainty; invalid references/eligibility remain technical grounding failures. Verifier execution failure is protocol uncertainty and cannot establish insufficiency.
- The verifier is necessary for nonliteral inference and metric/context alignment that numeric matching cannot establish. It uses the same authorized model in a separate call, with a 250,000-byte input cap, 4096-token output cap and no verifier retry. At most two assessment attempts plus one verifier request are allowed per paper. This is conservative model screening, not a proof of truth; correlated semantic errors remain possible.
- The scientific rubric, six required gate dimensions, relevance/admission rules, publication-status policy, affiliation treatment, transport retry policy, manuscript coverage and discovery are unchanged. Legacy v1/quote-based decisions remain readable without revalidation or rewriting. A new assessment version forces fresh Sci-MMR assessment while reusing the frozen cached manuscript; `--force` was avoided because it would also refresh PDF acquisition.

## Independent review

[PR #29](https://github.com/vernerisirva/agentmempaper/pull/29); initial reviewer `deepseek/deepseek-v4-pro-0813`; after six calls the user authorized a different independent reviewer, `anthropic/claude-opus-4.6`. Verdicts: **CHANGES_REQUIRED → CHANGES_REQUIRED → NO VERDICT (output limit) → CHANGES_REQUIRED → CHANGES_REQUIRED → CHANGES_REQUIRED → PASS**. Exact final reviewed head `53fca91cac364bbf3c7f0f9996dbe0e3b254ed42` passed CI and merged automatically as `e9a6199430f034e803a30e43c7c295c6fc06c443`. Zero unresolved blockers; no material source changes followed final review.

The first review correctly motivated a stricter dimension-level Abstract restriction. Narrative union filtering was added as defense in depth. Claims about broken pass construction, verifier error propagation, byte-limit ordering, uncertain-record hydration and K/M/B collapse were contradicted by code and direct regressions. The proposed mutable-intermediate-input scenario had no reachable trigger; final input-hash revalidation is deliberately retained. Broad body candidates for bounded limitation inference remain permissible because section labels nominate sources, while substantive support is separately required. All findings and dispositions are in the JSON report.

## Five-paper rerun

| Paper | Before | Automatic result | Operative source roles |
|---|---|---|---|
| AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems | evidence_grounding_failure | scientific_uncertainty | appendix, body, introduction, limitations, related |
| Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents | evidence_grounding_failure | scientific_uncertainty | appendix, body, introduction, related |
| Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents | pass | evidence_grounding_failure | none |
| Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. II. Antibody Properties, Lipid-RNA Interactions | evidence_grounding_failure | evidence_grounding_failure | none |
| Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models | evidence_grounding_failure | evidence_grounding_failure | none |

### AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems

Automatic scientific uncertainty with all submitted references eligible. The verifier detects a real model/metric mismatch: the proposal assigns 58.8% strict and 70.5% state-aware operation accuracy to GPT-5.4, while the cited results attribute those values to GPT-5.4-mini. It also rejects unestablished whole-paper release claims and incomplete equation support. Deterministic checks additionally produce conservative representation false negatives where percentages appear in a table header rather than next to each value, or PDF text merges adjacent values. Therefore not every numeric rejection is a substantive scientific flaw. Five supported evidence items remain operative; rejected claims and the original narrative are withheld.

Remaining uncertainty: Scientific support remains unresolved. Cited evidence does not establish numerical values/units: 96.0% The cited sources support synthetic GPT-4o generation, manual validation without reported agreement, single-run LOCOMO comparison, and AIM underperforming Mem0, but the claim about adversarial queries being generated by the same model family and the three-scored-interaction basis Cited evidence does not establish numerical values/units: 7 Cited evidence does not establish numerical values/units: 96.0%, 58.8%, 70.5% Cited evidence does not establish numerical values/units: 96.0%, 96.0% The cited setup and appendix text confirm three trials on MUMBench and a single LOCOMO run, but the supplied excerpts do not state whether code or the MUMBench dataset is released.

### Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents

Automatic scientific uncertainty, but the sole support error is a reproducible numeric-normalization defect: the claim says "95 percent" and both cited canonical blocks say "95%". The semantic verifier supports the claim; the deterministic checker treats bare 95 and 95% as different units. This is a pipeline false rejection, not evidence of scientific insufficiency. Eight supported items remain operative, and the withheld method claim/proposed pass are not manually repaired. All references are valid and eligible; no Abstract selection failure remains.

Remaining uncertainty: Scientific support remains unresolved. Cited evidence does not establish numerical values/units: 95

### Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents

New technical grounding failure. The methodological-rigor item mixes a results-classified benchmark-construction block B0024 with two eligible appendix blocks (B0050/B0067). The results block actually describes task generation and deterministic quality filtering, so a heading-based method restriction rejects relevant body content. The verifier is skipped for the entire proposal. A separate 57.2% numeric check also lacks that literal unit-bearing value in its cited blocks. The old >20% complete-recovery claim is absent from the new proposal and operative card, and the former automatic pass is withdrawn. No scientific pass or insufficiency can be concluded from this execution.

Remaining uncertainty: Scientific support remains unresolved. Support verification unavailable. Cited evidence does not establish numerical values/units: 57.2%

### Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. II. Antibody Properties, Lipid-RNA Interactions

New body-role conflicts preserve a technical grounding failure. The method item combines an Introduction protocol description (B0013) with a Methods block (B0052), while an attributed limitation cites a Methods passage explicitly stating the time-bound scope (B0053) plus a body discussion of verification difficulty (B0048). The compatibility matrix rejects Introduction for method and Methods for attributed limitation, despite relevant content. No Abstract IDs are responsible. The verifier is skipped, so the result is unresolved technical grounding, not an adverse scientific verdict.

Remaining uncertainty: Scientific support remains unresolved. Support verification unavailable.

### Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models

New body-role conflict preserves a technical grounding failure. The attributed limitation cites Experimental Results B0040, which explicitly says Engram-40B does not dominate Engram-27B on every task and attributes this to under-training. The limitation/source_claim rule excludes results-classified blocks; the same relevant passage could have been a candidate for inference, but relabelling the output manually is prohibited. All cited IDs exist; no Abstract ID is responsible. Verifier execution is skipped and no scientific verdict is accepted.

Remaining uncertainty: Scientific support remains unresolved. Support verification unavailable.

## Remaining pipeline defects

The reported two scientific_uncertainty classifications are the unchanged normal-pipeline outputs. Grounding Agent Memory is demonstrably a normalization false rejection, so the label must not be interpreted as a substantive scientific concern. No manual status correction was made.

- The section compatibility matrix rejects substantively relevant body content under results/introduction/methods headings for some claim kinds.
- Spelled percent and symbolic % are not normalized equivalently.
- Unit-in-header tables and merged PDF values can trigger conservative numeric false rejection.

These defects prevent readiness. No output was reclassified or repaired, and no additional paid reassessment was used to obtain more favorable results.

## Sci-MMR numerical integrity

The known unsupported numerical claim was removed from the new proposal rather than newly grounded. Neither the current operative evidence (empty after failed grounding) nor its published rationale asserts that answer accuracy exceeds complete evidence recovery by more than 20%. Sci-MMR is now technical grounding uncertainty, not pass. The historical pass and its exact old claim remain unchanged in assessment history. This satisfies removal of the known false acceptance but does not resolve Sci-MMR end to end.

The historical unsupported proposal remains in assessment history for audit. It is not operative evidence or a current positive claim. No paid output was manually edited.

## Original 28 final totals

| Classification | Before | After |
|---|---:|---:|
| `pass` | 16 | 15 |
| `scientific_uncertainty` | 4 | 6 |
| `insufficient` | 1 | 1 |
| `manuscript_unavailable` | 3 | 3 |
| `evidence_grounding_failure` | 4 | 3 |
| `model_protocol_failure` | 0 | 0 |
| `text_coverage_failure` | 0 | 0 |

The stable insufficient decision for Human Supervision and unavailable manuscripts remain unchanged. Mr.LHDR remains admitted. Main-library counts: agent_memory: 4 / deep_research: 5 / engram: 6.

## Cost

| Stage | Calls | Input tokens | Output tokens | Reported USD |
|---|---:|---:|---:|---:|
| initial | 5 | 240,601 | 10,236 | $0.281099126 |
| retry | 0 | 0 | 0 | $0.000000000 |
| verifier | 2 | 32,723 | 1,491 | $0.028277746 |
| Independent review | 7 | 456,723 | 23,920 | $0.784297401 |

Five-paper assessment/retry/verifier total: **$0.309376872**. Combined with review: **$1.093674273**. Unknown-cost requests: **0**. Earlier phases excluded. Frozen conservative reserve **$9.3050950**, within the approved **$10** ceiling.

## Validation and publication

All 273 unit tests pass, including the real four Abstract cases and Sci-MMR numerical regression. All three relevance/quality/discovery/idempotency checks, offline builds, sidecar schemas, relative links, exposure scans, workflow validation, size checks and diff checks pass. All 28 cards and six library/review pages pass local browser checks. Source disclosures preserve canonical text, subject to the existing HTML writer’s line-end whitespace trimming and browser removal of two PDF-extraction NUL characters in an AIM formula; sidecar source text retains exact canonical bytes.

Snapshot/restore preserves all three databases and all prior assessment rows, adds exactly five rows, and changes exactly five current decisions. Discovery/source rows and all other 23 original assessments are unchanged. Legacy snapshot loading and rebuilds preserve database hashes.

The single Pages deployment and public verification are pending; completion will be recorded here.

## Readiness

- PASS: `text_coverage_failures_zero`
- PASS: `model_protocol_failures_zero`
- FAIL: `four_abstract_failures_resolved`
- PASS: `abstract_cannot_satisfy_body_requirements`
- PASS: `numerical_claims_require_cited_support`
- PASS: `scimmr_known_unsupported_claim_removed`
- PASS: `valid_ids_do_not_prove_support`
- PASS: `inferences_require_support`
- FAIL: `no_new_technical_grounding_failure`
- PASS: `full_validation_passes`
- PASS: `no_manual_correction_required`

```text
QUALITY_PIPELINE_READY_FOR_BATCH_2: NO
```

Batch 2 was not started.

Durable runtime asset published, downloaded and restored with identical database bytes. SHA-256: `bf1fd0ef43bc52a2004b183357daf649e8bbac325c2c5573f47e348db7807f45`.

## Continuation checkpoint

Remaining work is to normalize equivalent percent spellings and make body-evidence eligibility less dependent on heading location while retaining the Abstract and claim-support protections. The JSON report preserves the four rejected body-role items and exact IDs for deterministic regression fixtures. AIM also demonstrates a real model/metric attribution error correctly caught by the verifier. This run made no further model calls after the frozen five-paper execution.
