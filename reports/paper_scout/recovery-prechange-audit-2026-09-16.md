# Original uncertain calibration roster — pre-change audit

| Track | ID | Title | Failure class | PDF | Model call | Parsing | Anchors | Quality |
|---|---|---|---|---|---|---|---|---|
| agent_memory | doi:10.1007/s44206-026-00290-2 | As-If Agents: Misrecognition and the Ethics of Non-Agentive AI | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| agent_memory | doi:10.5281/zenodo.22750153 | The Intransitability of Hybrid Agents: Operational Memory, Drift Gradients, and the Limits of Agent Portability | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| agent_memory | doi:10.48550/arxiv.2609.12320 | AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| agent_memory | doi:10.5281/zenodo.22661593 | Human Supervision as Attractor Stabilization: Indirect Prompt Injection, Longitudinal Object Custody, and the HibriMind Ontology | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| agent_memory | doi:10.5281/zenodo.22699102 | Consolidation Without Weights: What the Complementary Learning Systems Analogy Licenses in LLM Agent Memory, and Why the Systems That Borrow Its Name Do Not Inherit Its Guarantee | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| agent_memory | doi:10.48550/arxiv.2609.11060 | Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| agent_memory | doi:10.5281/zenodo.22682679 | Beyond Agentic Operating Systems A Governance-Centric Architecture for Persistent Enterprise AI Memory, Coordination, and Human Authority AIVORIX OS™ Architectural Research Series | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| agent_memory | arxiv:2609.11225 | Harness Robotic OS: A Unified Embodied-Agent Runtime for Closed-Loop Quadruped Inspection | incomplete_transport_response | acquired | transport_failure | not_reached | not_reached | uncertain |
| agent_memory | doi:10.5281/zenodo.22685081 | Rank-Bounded Memory: Self-Poisoning and Attribution Laundering in LLM Agents | incomplete_transport_response | acquired | transport_failure | not_reached | not_reached | uncertain |
| agent_memory | doi:10.5281/zenodo.22682633 | AgentKG: Conversational Memory as a Knowledge Graph | no_extractable_pdf | unavailable | not_attempted | not_reached | not_reached | uncertain |
| deep_research | doi:10.1002/advs.76675 | Closing the Empirical Loop: Autonomous AI Agents Conduct End‐to‐end Research With Human Participants | no_extractable_pdf | unavailable | not_attempted | not_reached | not_reached | uncertain |
| deep_research | doi:10.48550/arxiv.2609.11243 | Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents | invalid_model_json | acquired | response_received | JSONDecodeError | not_reached | uncertain |
| deep_research | doi:10.48550/arxiv.2609.10922 | Auto-RecSys: Harnessing Autonomous Research Agents for Industry-Scale Recommender System | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| deep_research | doi:10.6082/mgmw1-gw451 | AI Scientists Need a Theory of Scientific Value | invalid_model_json | acquired | response_received | JSONDecodeError | not_reached | uncertain |
| deep_research | doi:10.48550/arxiv.2609.07611 | AgentIdeaBench: Benchmarking Scientific Ideation in the Agent Era | incomplete_transport_response | acquired | transport_failure | not_reached | not_reached | uncertain |
| deep_research | doi:10.48550/arxiv.2609.07655 | Online Surrogate Repair: Decoupling High-Fidelity Feedback from Search Length in Closed-Loop Discovery | incomplete_transport_response | acquired | transport_failure | not_reached | not_reached | uncertain |
| deep_research | doi:10.64898/2026.09.03.749176 | Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. II. Antibody Properties, Lipid-RNA Interactions | incomplete_transport_response | acquired | transport_failure | not_reached | not_reached | uncertain |
| deep_research | doi:10.17605/osf.io/qm2c3 | Do AI Scientists' Results Replicate? Pre-registration of a multi-seed re-execution study of agent-generated empirical claims with matched human baselines and auditor calibration (AutoReplicate) | no_extractable_pdf | unavailable | not_attempted | not_reached | not_reached | uncertain |
| deep_research | doi:10.1016/j.nxnano.2026.100728 | Generative artificial intelligence for nanomaterial discovery and nanoengineering: From data-driven design to autonomous laboratories | no_extractable_pdf | unavailable | not_attempted | not_reached | not_reached | uncertain |
| engram | arxiv:2609.04793 | ProtLingo: Efficient Protein Language Modeling via Conditional Memory and Expert Routing | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| engram | doi:10.48550/arxiv.2609.03426 | Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations | invalid_model_json | acquired | response_received | JSONDecodeError | not_reached | uncertain |
| engram | arxiv:2608.29327 | When to Adapt: Conditional Memory Adapters for Retention-Preserving Domain Specialization | evidence_anchor_rejection | acquired | response_received | parsed | rejected | uncertain |
| engram | arxiv:2608.23982 | Memory Is Not Always Needed: Characterizing Conditional Memory in Scientific Reasoning | incomplete_transport_response | acquired | transport_failure | not_reached | not_reached | uncertain |
| engram | doi:10.48550/arxiv.2608.17050 | Cross-Model Memory Transfer via Target-Side Reader Adaptation | incomplete_transport_response | acquired | transport_failure | not_reached | not_reached | uncertain |
| engram | openalex:W7172473936 | Tokenizer-Agnostic Engram Module | incomplete_transport_response | acquired | transport_failure | not_reached | not_reached | uncertain |
| engram | arxiv:2605.20948 | Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory | dns_failure | acquired | transport_failure | not_reached | not_reached | uncertain |
| engram | arxiv:2601.07372 | Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models | dns_failure | acquired | transport_failure | not_reached | not_reached | uncertain |

Transport evidence: eight `http.client.IncompleteRead` exceptions and two DNS resolution failures. Prior logs show no HTTP 429/5xx or timeout status for these ten requests; the upstream cause of the incomplete bodies was not retained and cannot be assigned to a particular provider.

Protocol evidence: three JSON decoder failures (Sci-MMR line 39/column 14; Scientific Value line 11/column 29; Lngram v2 line 10/column 28). Raw visible responses and finish reasons were not retained, so malformed syntax cannot reliably be distinguished from truncation or surrounding prose retrospectively. No judgment is recovered by guessing.


## Individual evidence-anchor audit

The original model evidence and cached manuscript text were inspected for all ten records. “Mixed” does not retrospectively grant a pass: corrected validators are followed by a fresh same-model assessment.

| Paper | Finding before changes | Conservative action |
|---|---|---|
| As-If Agents | Real body quotations suffer line-end hyphenation, ligatures, typographic quotes and parenthesis spacing; some quotation marks differ. | Normalize typography and physical line-break hyphens only; retain meaningful punctuation/word distinctions. |
| Intransitability of Hybrid Agents | Mixed: several genuine body quotes are mislabelled Abstract after missed numbered headings; other excerpts stitch separate passages together. | Repair section boundaries; reject stitched excerpts. |
| AIM | Mixed: PDF word spacing differs, but several excerpts alter words/formula symbols or join clauses with ellipses. | Require literal contiguous quotes on rerun; no semantic or formula fuzzy matching. |
| Human Supervision as Attractor Stabilization | Seven of eight model excerpts occur in text mislabelled Abstract; the remaining excerpt joins four headings. | Repair numbered headings; reject the composite excerpt. |
| Consolidation Without Weights | Mixed: genuine body text is labelled Abstract; other excerpts summarize or concatenate separated passages. | Repair headings and ligatures; reject noncontiguous summaries. |
| Grounding Agent Memory | Mixed: two normalized body quotes locate; other excerpts have word gluing, composite omissions or changed formula text. | Accept only located exact-normalized text; request verbatim short excerpts. |
| Beyond Agentic Operating Systems / AIVORIX | Fifteen of sixteen excerpts locate in text mislabelled Abstract; one table excerpt omits a trademark token. | Repair headings; preserve omitted-token rejection. |
| Auto-RecSys | Mixed: four body quotes locate; other excerpts change “execution” to “experiment”, omit text, or contain ellipses. | Correct unique page localization only; reject altered words/composites. |
| ProtLingo | Mixed: six quotes locate after basic normalization; some are abstract-only, have glued words, omit citations, or change punctuation. | Exclude abstract; require visible contiguous body text and preserve semantic distinctions. |
| When to Adapt | No model evidence objects were provided. | Correct rejection; no inferred evidence or retrospective pass. |

No edit-distance or semantic fuzzy matching is introduced. Relocation requires one unique eligible body section (or one matching section on the claimed page). Abstract and prompt-truncated text remain ineligible.

## Bounded acquisition audit

AgentKG's Zenodo record exposes only a versioned software ZIP. AutoReplicate's public OSF registration archive exposes only `PREREGISTRATION_v2.md`. OpenAlex points the nanomaterials review to an official ScienceDirect PDF which returns HTTP 403; the public Elsevier response contains metadata, not the article body. These remain access/format uncertainty, not scientific failures.

Closing the Empirical Loop's publisher and Europe PMC PDF routes return 403 (the PMC PDF route serves HTML). Public Europe PMC JATS XML contains the full article body and DOI. A narrowly scoped reader recovers its manuscript evidence using logical body-section numbers, explicitly distinguished from PDF pages. No access control is bypassed.

## Execution contract

Scientific assessor stays `deepseek/deepseek-v4-pro-0813`. Each paper has one initial call and at most one transient retry (two seconds exponential-backoff base; honor a longer Retry-After up to 60 seconds, otherwise stop/defer). Inner HTTP retries are disabled. The ledger preserves call type, failure class, status, response ID, finish reason, content length/hash and allowlisted numeric usage. Unknown billing remains unknown.

Strict structured output plus local schema validation is used. No paid repair call is introduced: the old raw answers were not retained, and malformed output is not enough to prove preservation of the original judgment/evidence. Invalid or truncated answers remain protocol uncertainty without guessed decisions. Scientific evidence-validation failures are recorded separately.

The gate and rubric version are unchanged. The rerun uses the explicit assessment version `quality-recovery-v1` for the frozen 27 IDs only; this retains assessment history and avoids the existing unique-key cache suppressing replacement records. Mr.LHDR is excluded.

The existing Pages workflow gains a deploy-only dispatch switch so this recovery can publish the reviewed committed site once without launching unrelated discovery or model calls.
