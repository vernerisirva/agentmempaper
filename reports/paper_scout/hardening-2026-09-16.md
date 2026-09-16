# Residual scientific-assessment hardening — 2026-09-16

The reviewed hardening is merged and the bounded residual rerun is complete. Three additional papers pass automatically. The reliability target is **not yet met**: mixed quotation/representation failures and two output-length protocol failures remain. No batch 2 was started.

## Scope and residual inventory

Canonical main started clean at `2282f7990`. The exact residual inventory was 14: 6 text-coverage failures, 4 grounding failures, 1 non-substantive protocol failure, and 3 unavailable manuscripts. Only the 11 acquired residual manuscripts were reassessed. Nine existing passes (including Mr.LHDR), four scientific uncertainties, the stable insufficient result, and the three access-limited records were preserved. No rubric or relevance changes.

The [preflight inventory](hardening-preflight-2026-09-16.md) and [its JSON companion](hardening-preflight-2026-09-16.json) record every source, format, page/section count, extracted/input length, completeness, anchor outcome and prior classification. The [final JSON report](hardening-2026-09-16.json) records all original 28 decisions, input/source hashes, coverage and request/cost ledger.

## Fixes and limits

- Raised the three tracks to bounded 400,000-character extraction and 180,000-character assessment inputs. All 11 acquired residuals now include every extracted source page/logical JATS section and all eligible body/appendix text. PDF table text and captions are included where extractable; no claim of image understanding or perfect table layout is made.
- Removed unconditional per-heading clipping for manuscripts that fit, replaced tail cuts with deterministic representative scientific-group selection, and exposed extraction/selection omissions. Full scope requires complete extraction, known body boundaries and zero eligible-text omission. References cannot consume most of the context.
- Fixed descriptive first body headings, numbered supplements, lettered/glued-uppercase appendices and reference-entry misclassification. Explicit extraction gaps are barriers and are not counted as source content.
- The prompt and validator use the same canonical text. Three strict physical-line-wrap views cover literal spacing, dehyphenation and compound-hyphen preservation. Semantic edits, unseen source-only text and Abstract-only gate evidence remain rejected. No broad fuzzy matching.
- Removed the deterministic seed from the model prompt. Schema-valid seed echoes, refusals, empty rationales and evidence-empty responses receive at most one shared retry; all transport/non-substantive retries together remain capped at two actual requests. No hidden reasoning or JSON repair is requested.
- Missing/selected text and model-declared coverage uncertainty cannot establish scientific insufficiency. The original insufficient manuscript retains all eight pages, six valid anchors and a substantive unsupported-guarantee rationale.
- Thirteen regression tests were added; all 231 tests pass. No dependencies were added.
- The final supported public-source pass found no additional completed manuscript. AgentKG is qualified by the last successful inventory plus current API access failure; OSF still supplies preregistration only; the publisher PDF remains 403.
- Larger extraction limits do not automatically refresh legacy caches. These eleven sources were explicitly reacquired and frozen; known partial legacy coverage remains qualified.

## Independent review

[PR #27](https://github.com/vernerisirva/agentmempaper/pull/27) merged as `91958559084a241021391cd61a871dbe6dc3d78a`. Model: `deepseek/deepseek-v4-pro-0813`. Final verdict: **PASS_WITH_NOTES**, **zero blockers**, reviewed head `f68de87a3dcbcb1ab56ccc57f690f87b4e53f572`; exact-head CI passed.

The first review identified extraction-marker accounting and defensive bounds work, which was fixed and retested. The second review included self-retracted findings and overlooked existing tests/documentation; independent adjudication of the unchanged commit with complete evidence produced the final verdict. Retained notes concern intentional fail-closed model-declared coverage uncertainty, a pre-existing malformed Content-Length case and test/large-report review limits. No source changes followed the final review.

## Original 28 calibration totals

| Classification | Before | After |
|---|---:|---:|
| `quality_pass` | 9 | 12 |
| `scientifically_uncertain` | 4 | 4 |
| `scientifically_insufficient` | 1 | 1 |
| `manuscript_unavailable` | 3 | 3 |
| `model_protocol_failure` | 1 | 2 |
| `evidence_grounding_failure` | 4 | 6 |
| `text_coverage_failure` | 6 | 0 |

Zero text-coverage failures means all eleven rerun inputs contain the complete eligible extracted text. It does **not** mean grounding reliability is solved: representation artifacts can still affect anchors, and incomplete model output is classified separately.

| Track | Pass | Scientific uncertainty | Insufficient | Unavailable | Protocol | Grounding | Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|
| agent_memory | 3 | 2 | 1 | 1 | 1 | 2 | 0 |
| deep_research | 5 | 1 | 0 | 2 | 0 | 2 | 0 |
| engram | 4 | 1 | 0 | 0 | 1 | 2 | 0 |

New automatic passes: **Rank-Bounded Memory**, **Closing the Empirical Loop**, and **Memory Grafting**. Their 11, 12 and 12 model evidence anchors respectively locate in the exact supplied body context. The rationales acknowledge the actual study limitations. No manual correction was imported.

## Every unresolved record

| Track / rank | Title and ID | Final class | Audit |
|---|---|---|---|
| agent_memory / 1 | As-If Agents: Misrecognition and the Ethics of Non-Agentive AI (`doi:10.1007/s44206-026-00290-2`) | `evidence_grounding_failure` | Required claim-alignment quotation rewrites the source opening and omits “I argued”. Eight of nine model anchors locate. This is an unsupported quotation, not a truncation issue. |
| agent_memory / 2 | The Intransitability of Hybrid Agents: Operational Memory, Drift Gradients, and the Limits of Agent Portability (`doi:10.5281/zenodo.22750153`) | `scientifically_uncertain` | Scientific uncertainty, preserved without reassessment. The paper's conceptual contribution is clear, but the absence of empirical or formal validation, limited related work, and unaddressed limitations make it difficult to assess the scientific substance of the claims. The paper may be valuable as a position piece, but its claims are not yet supported by evidence. |
| agent_memory / 3 | AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems (`doi:10.48550/arxiv.2609.12320`) | `model_protocol_failure` | Baidu ended at the 8192-output-token limit (finish_reason=length). The incomplete response is a protocol failure; no scientific decision was inferred and no JSON repair was attempted. |
| agent_memory / 6 | Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents (`doi:10.48550/arxiv.2609.11060`) | `evidence_grounding_failure` | Seven of nine model anchors locate. Claim-alignment quote changes extracted word spacing; related-work quote crosses a page/section-label boundary. Mixed quotation fidelity and cross-page representation problems remain unresolved. |
| agent_memory / 8 | Harness Robotic OS: A Unified Embodied-Agent Runtime for Closed-Loop Quadruped Inspection (`arxiv:2609.11225`) | `scientifically_uncertain` | Scientific uncertainty, preserved without reassessment. The main uncertainty is whether the cognitive-runtime components (voice grounding, hierarchical memory, governed self-evolution) have any empirical support beyond design description. The supplied text repeatedly defers these evaluations to future work or to controlled trials whose numerical values are not yet reported. Additionally, the field metrics in Table 1 are presented without trial counts, repetitions, noise conditions, or statistical intervals, so the strength of the navigation and inspection validation cannot be fully assessed from the available text. The paper type is best classified as systems_or_application rather than survey_or_review, because it describes and evaluates a deployed prototype system. |
| agent_memory / 10 | AgentKG: Conversational Memory as a Knowledge Graph (`doi:10.5281/zenodo.22682633`) | `manuscript_unavailable` | Access uncertainty. The prior successful official inventory exposed software ZIP only. This final lookup could not freshly enumerate the record: timeout then one 504 retry; the landing lookup also failed. No fresh assertion that a manuscript does not exist. |
| deep_research / 2 | Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents (`doi:10.48550/arxiv.2609.11243`) | `evidence_grounding_failure` | Five of nine model anchors locate. Contribution text crosses a page/header boundary; claim-alignment quote inserts word boundaries absent in extraction. Some inline compound hyphens also differ. These are mixed extraction/context and quotation fidelity issues, not proven scientific uncertainty. |
| deep_research / 5 | AI Scientists Need a Theory of Scientific Value (`doi:10.6082/mgmw1-gw451`) | `scientifically_uncertain` | Scientific uncertainty, preserved without reassessment. The manuscript is a preprint and the extracted text appears to omit some sections or tables (e.g., Table 1 is truncated, some section transitions are abrupt), so the assessment may not reflect the complete argument. Because the paper is a position piece, the absence of empirical validation is expected, but the strength of the contribution depends on whether the proposed formal apparatus can be made checkable and useful in practice, which the paper only sketches. |
| deep_research / 8 | Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. II. Antibody Properties, Lipid-RNA Interactions (`doi:10.64898/2026.09.03.749176`) | `evidence_grounding_failure` | Eleven of thirteen anchors locate. The only positive contribution anchor is Abstract-only and is correctly excluded; an additional claim-alignment quotation also changes punctuation spacing. A separate claim-alignment anchor locates, so the decisive gate failure is the unsupported body contribution anchor. |
| deep_research / 9 | Do AI Scientists' Results Replicate? Pre-registration of a multi-seed re-execution study of agent-generated empirical claims with matched human baselines and auditor calibration (AutoReplicate) (`doi:10.17605/osf.io/qm2c3`) | `manuscript_unavailable` | Access uncertainty. Final official OSF archive lookup still exposes a preregistration Markdown file, not a supported completed-study manuscript. |
| deep_research / 10 | Generative artificial intelligence for nanomaterial discovery and nanoengineering: From data-driven design to autonomous laboratories (`doi:10.1016/j.nxnano.2026.100728`) | `manuscript_unavailable` | Access uncertainty. OpenAlex and Semantic Scholar point to the same publisher PDF, which remains HTTP 403. No access controls were bypassed. |
| engram / 1 | ProtLingo: Efficient Protein Language Modeling via Conditional Memory and Expert Routing (`arxiv:2609.04793`) | `evidence_grounding_failure` | Eight of twelve model anchors locate. Contribution and one concern span page-label/header boundaries; the methods quote omits a mathematical domain constraint, and the limitations quote changes a semicolon to a period. No blanket whitespace/fuzzy acceptance was introduced. |
| engram / 5 | Cross-Model Memory Transfer via Target-Side Reader Adaptation (`doi:10.48550/arxiv.2608.17050`) | `evidence_grounding_failure` | The previous non-substantive seed echo is gone. Six of nine substantive anchors locate, but claim alignment is a paraphrase placed in the excerpt field, a reproducibility quote replaces an arrow with a word, and a limitation quote changes an en dash to a hyphen. The paraphrased claim-alignment excerpt is independently disqualifying. |
| engram / 6 | Tokenizer-Agnostic Engram Module (`openalex:W7172473936`) | `scientifically_uncertain` | Scientific uncertainty, preserved without reassessment. The paper's central claim of tokenizer-agnosticism is supported by a single cross-tokenizer transfer experiment with modest and mixed results. The absence of explicit limitations, the small performance differences, and the lack of a direct comparison against a tokenizer-locked baseline for the transfer scenario leave the strength of the contribution uncertain. |
| engram / 8 | Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models (`arxiv:2601.07372`) | `model_protocol_failure` | Alibaba ended at the 8192-output-token limit (finish_reason=length). This is a protocol failure with no scientific decision and no JSON repair. |

The six grounding failures remain technical screening failures. As-If and the decisive Real Science anchor are clearly unsupported quotations; Cross-Model also contains a disqualifying paraphrase. Grounding Agent Memory, Sci-MMR and ProtLingo additionally expose page-boundary/header/spacing issues. These are deliberately not relabelled as scientific uncertainty or silently corrected.

AIM and Conditional Memory reached the 8192-token output limit at Baidu and Alibaba respectively (`finish_reason=length`). Both remain protocol uncertainty. They are not schema-valid non-substantive responses, so the new one-retry rule did not apply; no speculative repair call was made.

## Cost and preservation

- Scientific requests: **11 initial, 0 retry, 0 repair**; nine normal completions and two output-length failures. Known cost **$0.384839706**, no unknown-cost requests.
- Independent review: 3 paid requests, **$0.2931955**. One oversized review was stopped locally before sending any API request.
- Total known cost for this hardening phase: **$0.678035206**. Earlier calibration/recovery costs are excluded.
- Frozen pre-call manifest allowed at most 22 actual scientific requests under a $4.8602136 conservative reserve and the previously approved $10 ceiling. It records exact IDs, source and assessment-input hashes; no new papers were selected.
- Snapshot/restore verifies exactly 11 current assessments changed; all prior assessment-history rows and discovery/source rows are identical. The other 17 original calibration records remain unchanged.

## Validation and publication

Full 231-test suite, all three relevance/quality/discovery checks, idempotency, offline builds, sidecar schemas, links, exposure scan, workflow validation, generated-file sizes, snapshot/restore and diff checks pass. Snapshot restore also rebuilds every track without mutating assessment state. Local browser verification passed for 18 pages, including all three libraries/review lists and the eleven reassessed cards. Public verification follows the single Pages deployment.

Expected main-library counts: **Agentic Memory 3, Deep Research 5, Engram 4**. Admission remains high topical relevance AND scientific pass. Publication is pending the single deployment; the final record will append the verified run and artifact hashes.

## Readiness

Coverage metadata and within-page wrap handling are improved and regression-tested. However, remaining grounding failures are not all proven to be genuinely unsupported independent of representation artifacts, and two provider completions were cut off at the bounded output limit. Further quote-fidelity/cross-page handling and bounded-output reliability work is needed before another batch; the present run does not certify those gaps.

```text
QUALITY_PIPELINE_READY_FOR_BATCH_2: NO
```

No batch 2 was started.

Durable runtime release asset published and downloaded for verification. SHA-256: `0a21a16569369bb711f2f6fbc82fb737cd572f816d090a8ead42328e86e95e59`. All three restored databases are byte-identical to the audited local snapshot.
