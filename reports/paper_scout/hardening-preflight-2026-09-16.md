# Residual assessment hardening preflight — 2026-09-16

Canonical main was clean at `2282f7990`. The exact residual roster has 14 records: six text-coverage failures, four evidence-grounding failures, one model-protocol failure and three unavailable manuscripts. Four scientific uncertainties, nine passes including Mr.LHDR, and one insufficient decision are protected from paid reassessment.

| Track / rank | Paper | Class | Source units | Extracted units before | Extracted / input characters before | Complete extraction before | Model outcome | Anchors |
|---|---|---|---:|---:|---|---|---|---:|
| agent_memory / 1 | As-If Agents: Misrecognition and the Ethics of Non-Agentive AI (`doi:10.1007/s44206-026-00290-2`) | text_coverage_failure | 27 | 27 | 101330 / 60000 | True | scientific | 9 |
| agent_memory / 3 | AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems (`doi:10.48550/arxiv.2609.12320`) | evidence_grounding_failure | 31 | 31 | 87244 / 49972 | True | evidence_validation_failure | 7 |
| agent_memory / 6 | Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents (`doi:10.48550/arxiv.2609.11060`) | evidence_grounding_failure | 25 | 25 | 89363 / 47747 | True | evidence_validation_failure | 5 |
| agent_memory / 9 | Rank-Bounded Memory: Self-Poisoning and Attribution Laundering in LLM Agents (`doi:10.5281/zenodo.22685081`) | evidence_grounding_failure | 31 | 31 | 97933 / 25426 | True | evidence_validation_failure | 2 |
| agent_memory / 10 | AgentKG: Conversational Memory as a Knowledge Graph (`doi:10.5281/zenodo.22682633`) | manuscript_unavailable | None | None | None / None | None | manuscript_unavailable | None |
| deep_research / 1 | Closing the Empirical Loop: Autonomous AI Agents Conduct End‐to‐end Research With Human Participants (`doi:10.1002/advs.76675`) | text_coverage_failure | 11 | 11 | 114855 / 43308 | True | scientific | 8 |
| deep_research / 2 | Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents (`doi:10.48550/arxiv.2609.11243`) | evidence_grounding_failure | 37 | 32 | 120062 / 58820 | False | evidence_validation_failure | 4 |
| deep_research / 8 | Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. II. Antibody Properties, Lipid-RNA Interactions (`doi:10.64898/2026.09.03.749176`) | text_coverage_failure | 12 | 12 | 62543 / 42838 | True | scientific | 6 |
| deep_research / 9 | Do AI Scientists' Results Replicate? Pre-registration of a multi-seed re-execution study of agent-generated empirical claims with matched human baselines and auditor calibration (AutoReplicate) (`doi:10.17605/osf.io/qm2c3`) | manuscript_unavailable | None | None | None / None | None | manuscript_unavailable | None |
| deep_research / 10 | Generative artificial intelligence for nanomaterial discovery and nanoengineering: From data-driven design to autonomous laboratories (`doi:10.1016/j.nxnano.2026.100728`) | manuscript_unavailable | None | None | None / None | None | manuscript_unavailable | None |
| engram / 1 | ProtLingo: Efficient Protein Language Modeling via Conditional Memory and Expert Routing (`arxiv:2609.04793`) | text_coverage_failure | 15 | 15 | 65185 / 60000 | True | scientific | 4 |
| engram / 5 | Cross-Model Memory Transfer via Target-Side Reader Adaptation (`doi:10.48550/arxiv.2608.17050`) | model_protocol_failure | 34 | 33 | 120064 / 60000 | False | scientific | 7 |
| engram / 7 | Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory (`arxiv:2605.20948`) | text_coverage_failure | 25 | 25 | 64159 / 49857 | True | scientific | 9 |
| engram / 8 | Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models (`arxiv:2601.07372`) | text_coverage_failure | 35 | 35 | 99980 / 60000 | True | scientific | 6 |

PDF units are physical pages; Closing the Empirical Loop uses 11 logical JATS body sections, not PDF pagination. Source byte hashes, extracted pages, exact selected pages, character counts, input hashes and exclusions are recorded in the JSON companion. Token usage is only exact when reported by the provider; character counts are not token counts.

## Concrete findings

- Rank-Bounded Memory uses a descriptive first numbered section after the abstract. Requiring a conventional Introduction heading caused most of its 31-page body to remain labelled Abstract.
- Per-heading 8,000-character caps discarded middle and final passages even when they would fit the total context. A 65% coverage heuristic could then label the result full text. Selection omissions often had no warning.
- Sci-MMR originally stopped at page 32 of 37; Cross-Model Memory Transfer stopped partway through page 33 of 34. Refreshed bounded extraction now contains all pages.
- Reference entries were sometimes treated as numbered sections. Explicit reference boundaries now exclude bibliography text, while numbered supplements and lettered/glued-uppercase appendices resume body coverage. ProtLingo implementation details and Lngram appendix limitations are regression fixtures.
- PDF text includes table values and figure captions where extractable. It is not image interpretation or a guarantee of faithful table layout. The acquired residual manuscripts have no empty or failed text pages; their substantive body, methods/results, discussion and detected appendices fit within the 180,000-character input bound.
- All four grounding rejections were checked individually. AIM and Grounding Agent Memory use abstract-only quotations for required body dimensions; Sci-MMR includes a validation quote that does not locate verbatim; Rank-Bounded Memory mixes unsupported/abstract anchors with a genuine body quote omitted by the prior context. These are not retroactively accepted.
- The five audited pass corrections are reproduced deterministically by literal/dehyphenated normalization; a third physical-wrap view additionally preserves genuine compound hyphens (`long-` + newline + `term` → `long-term`). Inline hyphens, words and numbers are unchanged.
- The Cross-Model response repeats the deterministic seed rationale rather than giving a scientific assessment. The seed is no longer sent in the prompt; exact echoes, refusals and evidence-empty schema-valid replies consume at most the one shared retry.
- The stable insufficient manuscript has all eight cached pages, six located anchors and a complete eligible selection. Its corrected rationale concerns an unsupported scientific guarantee, not absent input. It remains unchanged. All nine existing passes also revalidate, including all eight Mr.LHDR anchors.

## Final bounded acquisition pass

OSF still exposes only the preregistration Markdown, without a supported completed-manuscript PDF. OpenAlex and Semantic Scholar identify the same publisher PDF for the nanomaterials review; it remains HTTP 403. AgentKG was previously verified as software ZIP only; this pass could not freshly enumerate files because the official API timed out/returned 504 (one retry). The public landing lookup also failed. No access control was bypassed and no absence of scientific merit is inferred. These three remain manuscript-access uncertainty; the AgentKG observation is explicitly based on the prior successful inventory plus current access failure.

## Validation before paid work

231 unit tests pass. All-track offline relevance, quality, discovery, idempotency, builds, schemas, links, exposure, workflow and size checks pass. Stable database rows remain unchanged. Independent review and merge must complete before paid assessment. No batch 2.
