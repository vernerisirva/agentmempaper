# Evidence grounding and protocol recovery — 2026-09-16

**QUALITY_PIPELINE_READY_FOR_BATCH_2: NO**

Exactly the eight residual technical cases were reassessed once through the merged normal pipeline. Four became automatic passes; four remain technical grounding uncertainty because the assessor cited explicitly ineligible Abstract blocks. No manual corrections, extra scientific reruns or batch 2. All 20 other original decisions and all prior history were preserved.

## Before and implementation

Before: six grounding failures and two output-limit failures. The [preflight inventory](evidence-grounding-preflight-2026-09-16.md) records all eight contexts, finish reasons, usage and exact failed anchors. Both protocol failures were `finish_reason=length` at 8192 output tokens.

- Deterministic ~900-character blocks bind manuscript ID, PDF hash, the entire selected input, addressing version, offsets, eligibility and content hashes. The supplied context exposes these IDs; a reply must echo its full context ID. Invented, foreign, stale, unseen and ineligible references fail closed.
- Paper Scout derives source snippets from canonical blocks and keeps the assessor claim/explanation separately. Each block retains exact source spans, original offsets, sections and pages. Serialization trims only outer whitespace in the legacy aggregate excerpt; authoritative source-block text remains exact.
- Only complete, same-section adjacent physical pages may share a block; selected excerpts, gaps and unrelated headings cannot join. Page-final lexical hyphens are preserved. Both original source spans remain available. Real page-boundary shapes are regression-tested; valid cross-page citations occur in seven of the eight reruns.
- New `block-evidence-v1` / `quality-evidence-v1` assessments use additive optional fields in `paper-scout-card-v2`. Older quote-based assessments continue to load unchanged. All 12 prior passes remain valid. The text-coverage selector, scientific rubric, relevance thresholds, admission policy and discovery budgets are unchanged.
- `length`, `max_tokens` and `max_output_tokens` are detected before parsing. One compact whole-response retry shares the two-request ceiling with transport/non-substantive recovery. No JSON stitching, repair or hidden reasoning. The compact schema retains all dimensions, verdict, rationale, uncertainty, limitations and evidence IDs.

## Independent review

[PR #28](https://github.com/vernerisirva/agentmempaper/pull/28), reviewer `deepseek/deepseek-v4-pro-0813`: **CHANGES_REQUIRED → PASS_WITH_NOTES**, zero unresolved blockers. Exact reviewed head `1f1ec15ee3b5eadb7df0ab6527db07594f7627f5` passed [CI](https://github.com/vernerisirva/agentmempaper/actions/runs/35129344598) and merged automatically as `e558271054c5a0b57e4cd0267a92d71d25192392`. No material source changes followed final review.

Fixed standalone resolver identity checks and separation of rejected model rationale from the final pending rationale; strengthened immediate page-span joining. The initial claim that preamble bytes were unhashed was incorrect: the full selected-text hash already bound them. Explicit hashing and a regression test now make that guarantee clearer. Empty evidence remains schema-valid solely to reach the bounded non-substantive retry. The final extraction-gap concern was checked against actual code: tail markers remain in source spans, gap blocks are ineligible, and partial extraction disables joining. Supplemental multiple-invalid-ID checking also passed. Detailed dispositions are in the JSON report.

## Eight-paper rerun

| Track / rank | Paper | Before | Final automatic status | Evidence items valid/submitted |
|---|---|---|---|---:|
| agent_memory / 1 | As-If Agents: Misrecognition and the Ethics of Non-Agentive AI (`doi:10.1007/s44206-026-00290-2`) | evidence_grounding_failure | pass | 9/9 |
| agent_memory / 3 | AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems (`doi:10.48550/arxiv.2609.12320`) | model_protocol_failure | evidence_grounding_failure | 9/11 |
| agent_memory / 6 | Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents (`doi:10.48550/arxiv.2609.11060`) | evidence_grounding_failure | evidence_grounding_failure | 7/9 |
| deep_research / 2 | Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents (`doi:10.48550/arxiv.2609.11243`) | evidence_grounding_failure | pass | 10/10 |
| deep_research / 8 | Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. II. Antibody Properties, Lipid-RNA Interactions (`doi:10.64898/2026.09.03.749176`) | evidence_grounding_failure | evidence_grounding_failure | 8/9 |
| engram / 1 | ProtLingo: Efficient Protein Language Modeling via Conditional Memory and Expert Routing (`arxiv:2609.04793`) | evidence_grounding_failure | pass | 12/12 |
| engram / 5 | Cross-Model Memory Transfer via Target-Side Reader Adaptation (`doi:10.48550/arxiv.2608.17050`) | evidence_grounding_failure | pass | 9/9 |
| engram / 8 | Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models (`arxiv:2601.07372`) | model_protocol_failure | evidence_grounding_failure | 7/9 |

All four rejected judgments cited real IDs in the correct context, but mixed Abstract blocks with eligible body blocks. The pipeline rejected the entire proposed decision, even where another cited body block might have been usable. It did not drop invalid IDs or promote the model’s proposed pass. This is a remaining avoidable evidence-selection failure, not quotation copying, page-boundary loss, manuscript unavailability or scientific insufficiency.

## Scientific interpretation limits

Reference integrity is deterministic; scientific support remains the assessor’s judgment. A valid address does not certify the claim. Source review found a concrete precision concern in Sci-MMR: one claimed >20% complete-evidence-recovery gap is not established by its cited Table 2/main-results blocks, which report different aggregate metrics. A separate claim-alignment item is supported by the 57.2% error breakdown. The automatic pass has not been manually changed; the report preserves this concern instead of certifying every model interpretation. Its uncertainty text also ends mid-sentence at the 900-character cap despite containing substantive limitations. These observations further argue against readiness.

The other three new automatic passes have source blocks supporting their principal contribution/method/evaluation/related-work and limitation assessments. This audit is not a new scientific assessment or an independent entailment guarantee. No paid output was manually corrected.

## Original 28 final totals

| Classification | Before | After |
|---|---:|---:|
| `pass` | 12 | 16 |
| `scientific_uncertainty` | 4 | 4 |
| `insufficient` | 1 | 1 |
| `manuscript_unavailable` | 3 | 3 |
| `model_protocol_failure` | 2 | 0 |
| `evidence_grounding_failure` | 6 | 4 |
| `text_coverage_failure` | 0 | 0 |

The four prior scientific uncertainties, one insufficient paper and three unavailable manuscripts are unchanged. Human Supervision retains its complete eight-page input and substantive scientific-insufficiency rationale. Mr.LHDR remains admitted.

## Cost

- Assessment recovery: **8 normal calls, 0 retry calls, 8 complete schema-valid responses, 0 transport/protocol failures**. Four judgments passed grounding; four failed grounding. Input **254,248**, output **16,643** tokens. Known cost **$0.235058245**; no unknown-cost calls.
- Independent review: **2 calls**, **$0.13539014**.
- Combined: **$0.370448385**. Earlier phases excluded. Frozen manifest reserved at most **$5.6573814** within the approved **$10** ceiling; maximum 16 scientific requests, zero repair calls. No uncontrolled retry chain.

## Validation and publication

All 241 unit tests, three relevance validations, three quality validations, discovery checks, idempotency, offline builds, sidecar schemas, relative links, exposure scans, workflow/YAML checks, generated-file sizes and diff checks pass. A post-merge test invocation initially used the system Git blocked by its Xcode licence; the complete rerun using Homebrew Git passed. Snapshot/restore reproduces all three databases, preserves every historical assessment and all discovery rows, and changes exactly the selected eight current records. The previous published snapshot loads without rewriting legacy assessments.

Main-library counts: **Agentic Memory 4 / Deep Research 6 / Engram 6**. All 28 cards and all library/review placements are checked. [Pages run 35130807226](https://github.com/vernerisirva/agentmempaper/actions/runs/35130807226) succeeded, deploying `d53d114fab88276b8c58364fd70d35a3841a8abe` with `deploy_only=true`. Exactly one deployment was dispatched; discovery, paid assessment, state-writing and automatic commit steps were skipped. All 28 public calibration JSON cards and all six library/review HTML pages exactly match the audited local files. All 34 public pages passed browser checks.

## Readiness and continuation

Coverage failures and protocol failures are zero, and the new deterministic addressing removes quotation-copying dependence. However, four avoidable ineligible-evidence selections remain and a source-review interpretation concern is documented. Do not treat the mechanical improvements or automatic passes as end-to-end reliability certification. A future explicitly scoped task may address eligibility selection and interpretation/reference precision; this run makes no further source changes or model calls.

```text
QUALITY_PIPELINE_READY_FOR_BATCH_2: NO
```

Batch 2 was not started.

Local browser verification passed for all 28 cards plus six library/review pages (34 total). Expanded source-evidence controls work; all 23 ProtLingo HTML blockquotes match canonical text after the existing HTML writer trims line-end whitespace. Source-block text in the sidecar retains the exact canonical bytes.

Durable runtime asset published, downloaded and restored with identical database bytes. SHA-256: `660455a8cadcfb1dab8f387cadc9c3537e1a35d51b646007b8d9c958d3802f63`.

Public libraries: [Agentic Memory](https://vernerisirva.github.io/agentmempaper/), [Deep Research](https://vernerisirva.github.io/agentmempaper/deep-research/), [Engram](https://vernerisirva.github.io/agentmempaper/engram/). This final verification note changes reports only; no second Pages deployment.
