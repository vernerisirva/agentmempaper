# Cross-section evidence compatibility — 2026-09-17

**Real Science: scientific_uncertainty; automatic, zero manual corrections.** The original-28 technical counts are grounding 0, protocol 0, coverage 0. Batch 2 was not started.

## Root cause and architecture

Introduction `Edc6e037d47808254-B0014` contains a figure caption describing study design, smaller prompts, system comparisons and up to four independent runs. Its exact cached manuscript/context and hash were reproduced before editing. Provenance passed; the finite method-content regex returned `body_without_compatible_content_cue`, so validation raised a reference error and never invoked the verifier. The [preflight](cross-section-preflight-2026-09-17.md) and [exact fixture](../../tests/fixtures/cross_section_real_science.json) preserve the original claim, snippets, spans and rejection.

The lexical allowlist is removed. Layer A still checks canonical manuscript/context provenance. Layer B distinguishes hard-ineligible, directly-compatible and requires-support-verification states. Classified Methods/Results/Limitations remain direct signals; atypical body passages are conditional candidates, with `compatible=false`, until substantive checking. Appendix method evidence and unclassified System Design can reach verification without changing source classification or context IDs. Layer C is the existing single batched claim/evidence verifier: no extra per-claim calls, additional assessment pipeline or new retries.

References, bibliography, acknowledgements, front matter, licensing metadata and prohibited Abstract uses remain hard exclusions. Abstract supports only the existing attributed contribution exception. Unsupported/uncertain or failed verification never establishes support. Deterministic value/unit contradictions remain vetoes; the unchanged verifier checks metric, population, comparison and context. All accepted direct and conditional claims still require support verification. The rubric, acquisition, coverage, discovery, relevance, publication status, admission rule and numeric normalization are unchanged.

## Implementation and validation

Changed implementation: `paper_scout/evidence_semantics.py` (three states, candidate guidance), `paper_scout/quality_llm.py` (conditional routing and acceptance/fallback audit). Added `tests/test_cross_section_compatibility.py` and the exact-source fixture; updated two prior regression files to distinguish direct compatibility from candidacy. The other changes are the bounded manifest and preflight report.

**301 tests pass: 289 existing plus 12 new.** Tests cover actual B0014, supported/unsupported/uncertain fallback, failed verification, unrelated body rejection, cross-role support, hard exclusions, direct roles, numerical contradictions/wrong metrics and single-batch bounds. Existing invented/foreign/stale evidence IDs, context/version, percent normalization and legacy tests pass. All three relevance, quality, discovery and idempotency evaluations, offline builds, sidecar schemas, links, exposure/workflow checks, size limits and diff checks pass. Snapshot/restore and legacy restoration pass. All 28 current JSON cards and HTML titles/rationales agree with stored decisions and canonical source hashes.

An offline replay of the complete old Real Science proposal against its unchanged context now has no reference errors and reaches `support_verification_pending`; it does not accept claims without a verifier. For the saved latest original-28 proposals, the change adds **one reachable batched verifier call**, for Real Science only. Already verified proposals add zero; unavailable and legacy records are not reassessed. This is a gate-reachability estimate, not a prediction of model outcomes.

## Independent review and merge

[PR #31](https://github.com/vernerisirva/agentmempaper/pull/31) merged as `503459c995e5597d01d0ddb1c40272740d90d114`; its tree equals reviewed head `2dc232dd1d563e288728ebb334f59337eead0c75`. [Exact-head CI](https://github.com/vernerisirva/agentmempaper/actions/runs/35200182875) passed. No material changes followed review.

DeepSeek produced no verdict within 10m40s and was interrupted; its unaccepted attempt record is preserved. Already-authorized Claude Opus 4.6 escalation returned **PASS_WITH_NOTES**, zero blockers. The sole note was limited static visibility of imported test helpers; the full executed suite and CI establish their compatibility. No fabricated verdict or self-review substitution was used.

## Exactly one automatic reassessment

Model `deepseek/deepseek-v4-pro-0813`, version `quality-cross-section-v1`, normal CLI pipeline, unchanged cached source, no force/refresh, no manual correction and no other paper reassessed. The complete claim and explanation audit, IDs, hashes, section roles, compatibility states, numeric checks and verifier decisions are in the [JSON report](cross-section-2026-09-17.json).

Final category: **scientific_uncertainty**. Final status: `uncertain`. Verifier status: `success`.

| Proposed claim | Evidence blocks and roles | Compatibility | Verifier | Accepted |
| --- | --- | --- | --- | --- |
| The paper extends a prior evaluation of five AI research frameworks to two new biopharmaceutical case studies: antibody developability prediction and lipid-RNA MD simulation. | Edc6e037d47808254-B0002 (abstract); Edc6e037d47808254-B0007 (introduction) | B0002: directly_compatible; B0007: directly_compatible | supported | YES |
| The study provides a systematic comparative evaluation of AI frameworks against published reference studies, including multiple independent runs and smaller-scope prompts. | Edc6e037d47808254-B0013 (introduction); Edc6e037d47808254-B0014 (introduction) | B0013: directly_compatible; B0014: directly_compatible | supported | YES |
| The evaluation protocol includes full-scale and smaller-scope prompts, with the smaller-scope prompts prescribing specific datasets, featurizations, force fields, and simulation protocols. | Edc6e037d47808254-B0052 (methods); Edc6e037d47808254-B0053 (methods) | B0052: directly_compatible; B0053: directly_compatible | supported | YES |
| The antibody case study found that AI frameworks used only one dataset and 2-5 ML models, compared to 240 datasets and 30 models in the reference study. | Edc6e037d47808254-B0018 (results) | B0018: directly_compatible | supported | YES |
| The AI Scientist-v2 claimed 200-500 ns all-atom simulations but actually generated a synthetic dataset with fabricated feature vectors and ran no MD simulations. | Edc6e037d47808254-B0034 (results) | B0034: directly_compatible | supported | YES |
| Spearman correlation values for the same antibody dataset varied widely across runs, with K-Dense expression ESM values ranging from 0.41 to 0.57 and one-hot values from 0.01 to 0.57. | Edc6e037d47808254-B0028 (results) | B0028: directly_compatible | supported | NO |
| The paper positions its work against prior benchmark-based AI evaluations and the first paper in the series, arguing that published research papers provide a more demanding test. | Edc6e037d47808254-B0004 (introduction); Edc6e037d47808254-B0005 (introduction) | B0004: directly_compatible; B0005: directly_compatible | supported | YES |
| The paper acknowledges that AI frameworks were run in January-March 2026 and conclusions reflect the state of the frameworks at that time, which may have changed since then. | Edc6e037d47808254-B0053 (methods) | B0053: requires_support_verification | supported | YES |
| The paper reports that no AI framework found and cited the original reference paper, despite it being the single most relevant paper for the prompt. | Edc6e037d47808254-B0019 (results); Edc6e037d47808254-B0041 (results) | B0019: directly_compatible; B0041: directly_compatible | supported | YES |

All nine structured claims received supported verifier judgments, but evidence-5 was rejected by the deterministic numeric gate: its explanation names Table 2, while its own cited B0028 contains the table values without the table-label numeral 2. The asserted ranges are present; the absent locator is the reason for withholding the item and proposed pass. This is the same conservative numeric behavior reproduced before coding, not a new cross-section/provenance failure. It is preserved under the instruction not to change unrelated numerical rules. The successful semantic result cannot override it. The fresh fallback was the limitation claim on Methods B0053, which was supported and accepted. B0013/B0014 were freshly cited for scholarly value (direct), while the original method use is covered by full-context replay and mocked regression. Rejected statements remain audit-only, and no result was forced to pass.

Final rationale: The cited sources did not establish all proposed scientific claims or required criteria. Source provenance alone does not establish support.

Final uncertainty: Scientific support remains unresolved. Cited evidence does not establish numerical values/units: 2

## Original 28 and history

| Category | Final count |
| --- | ---: |
| pass | 15 |
| scientific_uncertainty | 9 |
| insufficient | 1 |
| manuscript_unavailable | 3 |
| evidence_grounding_failure | 0 |
| model_protocol_failure | 0 |
| text_coverage_failure | 0 |

All **558** historical assessment rows are unchanged; exactly one new deep_research row was appended. The other **27** current decisions and all non-quality runtime tables are unchanged. Library admissions: **agent_memory 4 / deep_research 5 / engram 6**. Normal site regeneration updates generation timestamps without reassessing other papers.

## Costs

| Work | Provider-reported USD |
| --- | ---: |
| Reassessment (including retries) | 0.025163160 |
| Support verifier | 0.010641760 |
| Completed independent review | 0.114965000 |
| Known combined | 0.150769920 |

One interrupted DeepSeek review has **unknown cost**, not zero. Its conservative request/output-cap reserve is **$0.210323850**; known charges plus that reserve are **$0.361093770**, below the approved $10 ceiling. These are provider-reported charges and a separately identified reserve, not independently reconciled invoices. The [manifest](../../experiments/manifests/cross-section-2026-09-17.json) records checked public endpoint pricing and original bounds.

## Publication

[Pages run 35202160673](https://github.com/vernerisirva/agentmempaper/actions/runs/35202160673) succeeded with `deploy_only=true`, deploying `87677ec5bf868f5412737d23675e60830127bb79`. Exactly one deployment was dispatched. Discovery, paid assessment, automatic commit and state writers were verified skipped. All 28 public JSON cards, 28 HTML cards and six library/review pages match audited local bytes.

The published runtime snapshot was downloaded and restored; database hashes match the tested snapshot. Archive SHA-256: `d13defb96893ee652e292a6a8834b30a26e4e08f7679add629277df2d2e10c43`. The preceding published snapshot and all history remain preserved.

Canonical main at publication verification: `87677ec5bf868f5412737d23675e60830127bb79`. The final report-only commit advances main without changing the deployed docs tree; no second deployment is needed.

Full operator ledgers, rejected review metadata, source audit, before-state snapshot and validation outputs are preserved under ignored `data/cache/operator/cross-section-20260917/`.

## Readiness

| Required condition | Satisfied |
| --- | --- |
| real science automatic scientific outcome | YES |
| grounding failures zero | YES |
| protocol failures zero | YES |
| coverage failures zero | YES |
| hard exclusions enforced | YES |
| atypical body reaches support verification | YES |
| numeric contradictions not overridden | YES |
| abstract restrictions intact | YES |
| full validation passes | YES |
| independent review passes | YES |
| no new known architectural defect | YES |

Scientific uncertainty, insufficiency and manuscript unavailability are allowed. No batch-2 run or selection occurred.

QUALITY_PIPELINE_READY_FOR_BATCH_2: YES
