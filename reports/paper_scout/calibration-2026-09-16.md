# Manuscript-quality calibration — 2026-09-16

The fixed 28-paper batch produced **1 pass, 27 uncertain, 0 insufficient**. Only Mr.LHDR is newly admitted. This is primarily an acquisition, transport and evidence-grounding calibration; it does not establish that the uncertain papers are scientifically weak. No second batch or paid retries were run.

## Selection and results

The selection was frozen at 2026-09-16T08:52:19+00:00 using the normal site ranking (New/date/relevance), without affiliation or venue selection. Baseline: `48af2f8c2751b54b26dc330743d49282ed93071f`. Original runtime snapshot SHA-256: `cfc3f5d602e306a384d7b5e645c9bd995b407c284d8be467af1815281be1f21c`. The adjacent selection JSON preserves all original IDs, titles and ranking metadata.

| Track | Selected | Pass | Uncertain | Insufficient | Remaining not assessed | Main library |
|---|---:|---:|---:|---:|---:|---:|
| agent_memory | 10 | 0 | 10 | 0 | 1897 | 0 |
| deep_research | 10 | 1 | 9 | 0 | 207 | 1 |
| engram | 8 | 0 | 8 | 0 | 0 | 0 |

Remaining high-relevance unassessed: Agentic Memory 307; Deep Research 120; Engram 0. The other remaining unassessed records are topical review candidates. All selected records now have pass or uncertain status, including conservative fallback records.

## Evidence, cost and failure accounting

- 24 unique PDFs acquired/extracted; all 24 paid invocations reused the PDF cache. No paid invocation downloaded a PDF. There were 19 failed URL attempts during free acquisition, mostly resolved by canonical arXiv/Zenodo links. Thirteen additional PDF downloads were made only for manual visual inspection.
- Four PDFs remained unavailable: AgentKG is a software archive without a manuscript; AutoReplicate exposes a Markdown preregistration rather than a PDF; Closing the Empirical Loop and the nanomaterial survey had inaccessible/non-PDF responses at tested official endpoints. Public XML/registration metadata was inspected separately but was not injected through a new assessment path.
- Assessor: `deepseek/deepseek-v4-pro-0813` through OpenRouter. 24 attempted requests, one per acquired manuscript; 14 responses carried usage. Ten had transport failures (8 incomplete responses, 2 DNS failures); three received invalid model JSON. Ten semantic responses were downgraded by the evidence validator; one passed.
- Known manuscript cost: **$0.4176873506395**. Billing is unavailable for ten failed requests, so the exact total is **unknown**, not $0.42. Reported usage: 222,850 input tokens, 28,757 output tokens, zero reasoning tokens, 512 cached input tokens. The preflight conservative estimate was $3.59 against a $5 ceiling.
- Required code-review work cost $0.04610298676325 for three completed responses, plus one interrupted request with unknown billing. It is separate from manuscript assessment cost.
- Publication metadata: 3 peer-reviewed, 18 preprint, 7 repository-only. These are provenance categories, not quality signals.

## Calibration observations

1. Infrastructure and grounding dominate this batch. Zero insufficient decisions were persisted, and no transport/extraction/JSON failure was turned into scientific insufficiency. The current CLI failure summary can still say `failures=0` after an LLM fallback; the explicit ledger here counts model and transport failures separately.
2. Four conceptual PDFs (Intransitability, Human Supervision, Consolidation Without Weights, AIVORIX) have body sections labeled Abstract by the current heading detector. The validator excludes Abstract anchors, so these cannot earn a supported substantive decision from the current extraction. This is an observed acquisition/segmentation limitation, not evidence against conceptual papers.
3. Other rejections involve non-exact quotations, page/section mismatches, or absent evidence objects. For example, only 3/11 ProtLingo anchors qualify; When to Adapt supplied no usable located model evidence. No quotes were repaired and no decision was overridden to raise the pass rate.
4. As-If Agents explicitly concerns philosophical epistemic standing, making its agent-memory fit adjacent. AgentKG and AutoReplicate show that normal ranking can surface software and registrations alongside manuscripts. Selection and relevance architecture were preserved.
5. Empirical results and baseline comparisons are visibly present in several uncertain Engram papers. Their uncertainty must not be read as a missing-baseline verdict. Legacy deterministic score/keyword diagnostics sometimes conflict with the manuscript; they did not determine admission.
6. Lngram v2 has an ICLR 2027 claim in its PDF header, while available publication metadata establishes only a preprint. No publication upgrade was made from that claim.
7. The research-card quality panel correctly carries manuscript rationale/provenance; other structured research fields may still say Not extracted yet. The site Updated date remains the latest discovery date (September 15), while assessment provenance records September 16. No UI or gate changes were made.

## Manual inspection and card verification

All eight Engram non-passes, the single pass, two Agentic Memory non-passes, and two Deep Research non-passes were inspected against extracted text, selected rendered PDF pages, metadata and rendered cards. Two passes per track could not be sampled: only one pass exists in the entire batch. No substitute passes were manufactured. Browser checks covered all three libraries/review pages and 13 sampled research cards, with no browser errors. Numeric quality scores are absent from the normal quality panel; the separate internal screening score is a relevance diagnostic.

## Validation and persistence

189 unit tests passed. All three quality/relevance/discovery evaluations, offline builds and idempotency checks passed. Schema/link/exposure/workflow checks found zero errors. Database hashes were unchanged by rebuild. The existing snapshot pack/restore path reproduced all assessment payloads exactly, and rebuilding the restored snapshot preserved them. Only the 28 frozen IDs changed current quality assessments; discovery/source rows were unchanged.

The normal GitHub Release runtime-state mechanism stores the SQLite state; git receives only intended generated site, digest and reviewed report files. No database, PDF/cache, credentials, temporary request/response payload or hidden reasoning is committed. PR #24 contains the independently reviewed request-cost fix; the scientific gate was unchanged.

## Per-paper selection, outcome and audit

| Track / rank | Paper and canonical ID | Outcome | Reason |
|---|---|---|---|
| agent_memory / 1 | As-If Agents: Misrecognition and the Ethics of Non-Agentive AI — `doi:10.1007/s44206-026-00290-2` | uncertain | evidence_anchor_rejection |
| agent_memory / 2 | The Intransitability of Hybrid Agents: Operational Memory, Drift Gradients, and the Limits of Agent Portability — `doi:10.5281/zenodo.22750153` | uncertain | evidence_anchor_rejection |
| agent_memory / 3 | AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems — `doi:10.48550/arxiv.2609.12320` | uncertain | evidence_anchor_rejection |
| agent_memory / 4 | Human Supervision as Attractor Stabilization: Indirect Prompt Injection, Longitudinal Object Custody, and the HibriMind Ontology — `doi:10.5281/zenodo.22661593` | uncertain | evidence_anchor_rejection |
| agent_memory / 5 | Consolidation Without Weights: What the Complementary Learning Systems Analogy Licenses in LLM Agent Memory, and Why the Systems That Borrow Its Name Do Not Inherit Its Guarantee — `doi:10.5281/zenodo.22699102` | uncertain | evidence_anchor_rejection |
| agent_memory / 6 | Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents — `doi:10.48550/arxiv.2609.11060` | uncertain | evidence_anchor_rejection |
| agent_memory / 7 | Beyond Agentic Operating Systems A Governance-Centric Architecture for Persistent Enterprise AI Memory, Coordination, and Human Authority AIVORIX OS™ Architectural Research Series — `doi:10.5281/zenodo.22682679` | uncertain | evidence_anchor_rejection |
| agent_memory / 8 | Harness Robotic OS: A Unified Embodied-Agent Runtime for Closed-Loop Quadruped Inspection — `arxiv:2609.11225` | uncertain | incomplete_transport_response |
| agent_memory / 9 | Rank-Bounded Memory: Self-Poisoning and Attribution Laundering in LLM Agents — `doi:10.5281/zenodo.22685081` | uncertain | incomplete_transport_response |
| agent_memory / 10 | AgentKG: Conversational Memory as a Knowledge Graph — `doi:10.5281/zenodo.22682633` | uncertain | no_extractable_pdf |
| deep_research / 1 | Closing the Empirical Loop: Autonomous AI Agents Conduct End‐to‐end Research With Human Participants — `doi:10.1002/advs.76675` | uncertain | no_extractable_pdf |
| deep_research / 2 | Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents — `doi:10.48550/arxiv.2609.11243` | uncertain | invalid_model_json |
| deep_research / 3 | Mr.LHDR: A Benchmark for Multimodal Real-World Long-Horizon Deep Research Agents — `doi:10.48550/arxiv.2609.11318` | pass | pass |
| deep_research / 4 | Auto-RecSys: Harnessing Autonomous Research Agents for Industry-Scale Recommender System — `doi:10.48550/arxiv.2609.10922` | uncertain | evidence_anchor_rejection |
| deep_research / 5 | AI Scientists Need a Theory of Scientific Value — `doi:10.6082/mgmw1-gw451` | uncertain | invalid_model_json |
| deep_research / 6 | AgentIdeaBench: Benchmarking Scientific Ideation in the Agent Era — `doi:10.48550/arxiv.2609.07611` | uncertain | incomplete_transport_response |
| deep_research / 7 | Online Surrogate Repair: Decoupling High-Fidelity Feedback from Search Length in Closed-Loop Discovery — `doi:10.48550/arxiv.2609.07655` | uncertain | incomplete_transport_response |
| deep_research / 8 | Real Science Is Harder Than Benchmarks: Evaluating Advanced AI Frameworks on Published Studies. II. Antibody Properties, Lipid-RNA Interactions — `doi:10.64898/2026.09.03.749176` | uncertain | incomplete_transport_response |
| deep_research / 9 | Do AI Scientists' Results Replicate? Pre-registration of a multi-seed re-execution study of agent-generated empirical claims with matched human baselines and auditor calibration (AutoReplicate) — `doi:10.17605/osf.io/qm2c3` | uncertain | no_extractable_pdf |
| deep_research / 10 | Generative artificial intelligence for nanomaterial discovery and nanoengineering: From data-driven design to autonomous laboratories — `doi:10.1016/j.nxnano.2026.100728` | uncertain | no_extractable_pdf |
| engram / 1 | ProtLingo: Efficient Protein Language Modeling via Conditional Memory and Expert Routing — `arxiv:2609.04793` | uncertain | evidence_anchor_rejection |
| engram / 2 | Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations — `doi:10.48550/arxiv.2609.03426` | uncertain | invalid_model_json |
| engram / 3 | When to Adapt: Conditional Memory Adapters for Retention-Preserving Domain Specialization — `arxiv:2608.29327` | uncertain | evidence_anchor_rejection |
| engram / 4 | Memory Is Not Always Needed: Characterizing Conditional Memory in Scientific Reasoning — `arxiv:2608.23982` | uncertain | incomplete_transport_response |
| engram / 5 | Cross-Model Memory Transfer via Target-Side Reader Adaptation — `doi:10.48550/arxiv.2608.17050` | uncertain | incomplete_transport_response |
| engram / 6 | Tokenizer-Agnostic Engram Module — `openalex:W7172473936` | uncertain | incomplete_transport_response |
| engram / 7 | Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory — `arxiv:2605.20948` | uncertain | dns_failure |
| engram / 8 | Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models — `arxiv:2601.07372` | uncertain | dns_failure |

## Manual notes

### agent_memory-01

PDF p.3 explicitly distinguishes philosophical epistemic agency from engineering agent autonomy. The scoped argument has substance; the track fit is adjacent. Model quotes normalize typography/hyphenation and fail exact matching. Retain uncertain; journal status provides no quality admission.

### agent_memory-02

PDF p.2 visibly has Introduction and named conceptual sections, while the extractor labels the body Abstract. This explains rejection of located evidence. The text is a conceptual portability proposal; do not infer scientific failure solely from absence of experiments. Repository-only status retained.

### deep_research-02

PDF p.3 contains benchmark comparisons and an argument-graph definition. Topical fit is direct. The uncertainty is caused by invalid model JSON, not an observed absence of methods or comparisons. Preprint status retained.

### deep_research-03

Pass manually checked: PDF p.11 Table 4 reports 25 systems and the cited OA/SA differences; the text explicitly says these metrics do not verify retrieval/source grounding. Located excerpts on pp.2,3,5,8,11,12 support all six required dimensions. A scoped benchmark inclusion is reasonable; overlapping intervals, partial extraction, and lack of replication remain explicit. The browser card displays preprint, Quality reviewed, rationale, limitations and provenance.

### deep_research-04

PDF p.4 provides a concrete dual-loop architecture, and the saved review describes a 31-iteration observational reliability analysis. The semantic result failed quote anchors; no finding of scientific insufficiency is established. Direct topical fit; preprint status retained.

### engram-01

PDF p.5 gives backbone, memory insertion, training mixture, benchmarks and a representation-preservation scope; p.12 discusses sampling tradeoffs. This is conditional memory in a protein model, adjacent to language-agent applications. Only 3/11 model anchors qualify. Retain uncertain despite favorable prose; card remains pending/preprint.

### engram-02

PDF p.6 gives semantic readout comparisons, a nuisance baseline and permutation checks. Invalid model JSON caused uncertainty. The PDF header claims ICLR 2027, but external publication provenance is not established; the card conservatively remains preprint. No publication upgrade or quality inference was made from the header.

### engram-03

PDF p.5 defines memory hashing, occupancy masking, gating and a LoRA comparison protocol with explicit data sizes and seeds. The model supplied no usable located evidence, so the gate retained uncertain. Direct conditional-memory fit; pending/preprint card is appropriate.

### engram-04

PDF p.4 contains BioProBench comparisons, routing equations and an experimental setup. Missing model assessment is a transport failure, not evidence that the paper lacks evaluation. Direct conditional-memory fit; pending/preprint card retained. A broader claim audit remains outstanding.

### engram-05

PDF p.6 specifies frozen memory/backbone and trained reader parameters; p.33 explicitly limits scale and generalization. The model request failed in transport. Direct memory-transfer fit; pending/preprint card retained without treating partial extraction as low quality.

### engram-06

PDF p.4 defines tokenizer-agnostic hashing assumptions, a 1-gram tradeoff, backbone choices and benchmarks. The model request failed in transport. The inspected page supports topical fit, but does not establish a full quality pass; pending/preprint card retained.

### engram-07

PDF p.6 compares MoE, vanilla Engram and grafting with controlled trainable-parameter budgets; p.25 explains the missing full distillation comparison and compute scope. DNS failure prevented assessment. Section detection also fell back to beginning/middle/end excerpts. Pending/preprint retained; the unreviewed distillation comparison is not converted into insufficiency.

### engram-08

PDF p.9 reports dense/MoE/Engram comparisons with matched activated parameters and training-token budgets. DNS failure prevented assessment. Direct Engram fit; existing preprint provenance retained. The broad paper has substantive results, but this spot-check does not replace the required evidence assessment.


## Publication verification

The runtime release asset was uploaded, downloaded again through the normal restore script, and verified against the local canonical databases. Release tag: `paper-scout-runtime-state`; asset ID: `567718667`; archive SHA-256: `2d0926f8e19f15f545dfff005bc9564469c80d23f31c071433fa50b67a0e8ef4`. The previous stale local databases were backed up before restoration.

All three generated sites are committed to the normal `docs/` surface. The large generated diff also applies the already-merged manuscript gate to previously stale checked-in pages. No new deployment workflow or daily discovery run was triggered, so this bounded task does not claim the GitHub Pages deployment has refreshed.
