# Batch 2: frozen quality-pipeline evaluation — 2026-09-17

**QUALITY_PIPELINE_GENERALIZATION_CHECK: FAIL**

The frozen pipeline failed on 5 of 20 selected papers (25%): four evidence-grounding failures share the abstract/code-release reproducibility pattern, and one Unicode encoding failure prevented assessment storage. This exceeds the predeclared technical tolerance and is not explained by manuscript unavailability.
The scientific audit also found numeric-format/locator conservatism and accepted explanations extending beyond their canonical snippets. Uncertain outcomes therefore mix legitimate unresolved support with pipeline friction; they do not establish clean generalization.
The failure judgment is independent of the zero pass rate. No manual repair occurred, all 559 historical rows and original 28 decisions are intact, no catastrophic cross-paper/provenance/state-loss defect was found, and all required software/site/state checks passed.

## Protocol

Frozen evaluator: `82ecd6b577a420e14a569225b0442d9d679a0a08`. No source, configuration, prompt, rubric, eligibility, threshold or manual assessment-output changes occurred. No PR reviewer was used and Batch 3 was not started.

Assessor and verifier: `deepseek/deepseek-v4-pro-0813` through OpenRouter, temperature 0, reasoning disabled, no seed. Assessment `quality-cross-section-v1`; rubric `scholarly-rubric-v1`; gate `scientific-gate-v1`; evidence `block-evidence-v2`; eligibility `cross-section-support-v1`. Strict JSON and provider parameter support are required. Assessor output cap 8192 tokens, at most two shared attempts; verifier output cap 4096, one batched call and no retry, 250,000-byte input cap. The normal production acquisition, extraction, deterministic selection, provenance and numerical safeguards were unchanged.

[Frozen protocol](../../experiments/manifests/batch-2-protocol-2026-09-17.json) · [Frozen roster](../../experiments/manifests/batch-2-roster-2026-09-17.json) · [Preflight](batch-2-preflight-2026-09-17.md).

Roster SHA-256: `af89dc0d58a24b3e894a15794447e7af4ff96fde40989b70c7ab5e1b355e6d82`. Selected at 2026-09-17T09:02:11+00:00; outcomes frozen at 2026-09-17T09:29:04.874183+00:00 before observational audit.

Selection: take the first up to ten per track in the existing offline research ranking after unchanged relevance, duplicate, curation and quality presentation rules. Require high relevance, `not_assessed`, nonsuppressed and never previously assessed. Exclude all 28 calibration IDs and every prior-assessment identity globally. No PDF-availability, prestige or predicted-pass selection and no replacements. Eligible pools were 220 / 58 / 0; selected 10 / 10 / 0. Every high-relevance Engram entry had prior history. Empty slots remain empty.

Predeclared technical criterion: zero avoidable grounding, protocol or coverage failures; no manual correction; unchanged history. At most one explained isolated external technical failure among 20 (5%), with no shared pattern. Scientific uncertainty, insufficiency and unavailability are legitimate outcomes; there is no target pass rate.

## Outcomes and selectivity

Rates use all selected entries in the track, including unavailable and technical failures. Engram percentages are undefined because n=0. Each paper appears in exactly one category.

| Outcome | Agent Memory (10) | Deep Research (10) | Engram (0) | Overall (20) |
|---|---:|---:|---:|---:|
| quality_pass | 0 (0%) | 0 (0%) | 0 (n/a) | 0 (0%) |
| scientific_uncertainty | 5 (50%) | 3 (30%) | 0 (n/a) | 8 (40%) |
| scientific_insufficient | 0 (0%) | 0 (0%) | 0 (n/a) | 0 (0%) |
| manuscript_unavailable | 1 (10%) | 6 (60%) | 0 (n/a) | 7 (35%) |
| evidence_grounding_failure | 3 (30%) | 1 (10%) | 0 (n/a) | 4 (20%) |
| model_protocol_failure | 0 (0%) | 0 (0%) | 0 (n/a) | 0 (0%) |
| text_coverage_failure | 0 (0%) | 0 (0%) | 0 (n/a) | 0 (0%) |
| other_technical_failure | 1 (10%) | 0 (0%) | 0 (n/a) | 1 (5%) |

| Technical failures, combined | Agent Memory | Deep Research | Engram | Overall |
|---|---:|---:|---:|---:|
| Count / rate | 4 / 40% | 1 / 10% | 0 / n/a | 5 / 25% |

No pass-rate target was used. Zero admissions alone does not imply excessive strictness. Here the failed generalization judgment rests on repeated technical failures, imperfect claim-boundary checking and mixed scientific/technical sources of uncertainty. Seven unavailable manuscripts (35%) remain legitimate acquisition outcomes. Engram has no held-out observations, so no Engram generalization inference is made.

## Frozen roster and final outcomes

All entries were `not_assessed` before execution. A missing stored assessment remains missing; the evaluation ledger records its technical failure without injecting a manual result.

| Track / position | Paper | Canonical ID | Pre-assessment | Final outcome |
|---|---|---|---|---|
| agent_memory / 1 | [MBM-0: Memory Birth Metrics v0](../../docs/papers/mbm-0-memory-birth-metrics-v0-6173b79a.html) | `doi:10.5281/zenodo.22671447` | not_assessed | manuscript_unavailable |
| agent_memory / 2 | [Beyond Agent Harnesses: Cross-Substrate Authority for Multi-Agent Systems](../../docs/papers/beyond-agent-harnesses-cross-substrate-authority-for-multi-agent-systems-eb3be139.html) | `doi:10.48550/arxiv.2609.08472` | not_assessed | scientific_uncertainty |
| agent_memory / 3 | [Personalizing LLM Agent Memory Using Biometrics](../../docs/papers/personalizing-llm-agent-memory-using-biometrics-0729931b.html) | `doi:10.48550/arxiv.2609.08558` | not_assessed | scientific_uncertainty |
| agent_memory / 4 | [MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging](../../docs/papers/memforest-efficient-agent-memory-management-via-eventtree-partitioning-and-progressi-1ccca021.html) | `doi:10.48550/arxiv.2609.08273` | not_assessed | other_technical_failure |
| agent_memory / 5 | [What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory](../../docs/papers/what-eviction-destroys-a-restore-counterfactual-audit-of-forgetting-in-agent-memory-2bb4c7e1.html) | `doi:10.48550/arxiv.2609.08279` | not_assessed | scientific_uncertainty |
| agent_memory / 6 | [Closing the Consistency Gap: Self-Evolving Agents That Learn to Stay on Course](../../docs/papers/closing-the-consistency-gap-self-evolving-agents-that-learn-to-stay-on-course-0db8679f.html) | `doi:10.48550/arxiv.2609.08832` | not_assessed | evidence_grounding_failure |
| agent_memory / 7 | [CreaMem: A Scene-Aware Memory Architecture for Personalized Agents](../../docs/papers/creamem-a-scene-aware-memory-architecture-for-personalized-agents-b41a150f.html) | `doi:10.48550/arxiv.2609.08550` | not_assessed | scientific_uncertainty |
| agent_memory / 8 | [Graph-Based Personalized Memory for LLM Agents: Representation, Evolution, Retrieval, and Evaluation](../../docs/papers/graph-based-personalized-memory-for-llm-agents-representation-evolution-retrieval-an-68b0fd87.html) | `doi:10.48550/arxiv.2609.08599` | not_assessed | scientific_uncertainty |
| agent_memory / 9 | [MeClear: Cooperative Game-Theoretic Attribution and Risk-Aware Memory Clearance for Long-Horizon LLM Agents](../../docs/papers/meclear-cooperative-game-theoretic-attribution-and-risk-aware-memory-clearance-for-l-d338c80c.html) | `doi:10.48550/arxiv.2609.09115` | not_assessed | evidence_grounding_failure |
| agent_memory / 10 | [Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems](../../docs/papers/revoked-but-still-authoritative-an-empirical-study-of-revocation-enforcement-in-agen-a34dde4e.html) | `doi:10.48550/arxiv.2609.08258` | not_assessed | evidence_grounding_failure |
| deep_research / 1 | [A New Paradigm: Agentic AI for Scientific Discovery](../../docs/deep-research/papers/a-new-paradigm-agentic-ai-for-scientific-discovery-93f54fc3.html) | `doi:10.65649/ukh4n33x` | not_assessed | scientific_uncertainty |
| deep_research / 2 | [A PRISMA-Aligned Agentic Framework for Medical Systematic Reviews and Evidence Synthesis](../../docs/deep-research/papers/a-prisma-aligned-agentic-framework-for-medical-systematic-reviews-and-evidence-synth-58121bec.html) | `doi:10.64898/2026.07.30.26359375` | not_assessed | manuscript_unavailable |
| deep_research / 3 | [Towards Reliable AI Scientists](../../docs/deep-research/papers/towards-reliable-ai-scientists-0fbfa2f6.html) | `doi:10.6082/gep96-ycs43` | not_assessed | manuscript_unavailable |
| deep_research / 4 | [Deep Research Agent: An AI-Powered System for Automated Research Paper Analysis and Citation-Based Answer Generation](../../docs/deep-research/papers/deep-research-agent-an-ai-powered-system-for-automated-research-paper-analysis-and-c-3dbe41de.html) | `doi:10.65890/race.v2i2.204` | not_assessed | manuscript_unavailable |
| deep_research / 5 | [When the Instrument Studies Itself: A Systematic Map of Autonomous AI Research Systems (2024-2026), Conducted by a Frontier Language Model](../../docs/deep-research/papers/when-the-instrument-studies-itself-a-systematic-map-of-autonomous-ai-research-system-b433242d.html) | `doi:10.5281/zenodo.21577092` | not_assessed | manuscript_unavailable |
| deep_research / 6 | [AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping](../../docs/deep-research/papers/autoresearch-a-multi-agent-ai-system-for-automated-literature-review-paper-summariza-1a31e108.html) | `doi:10.5281/zenodo.21523008` | not_assessed | manuscript_unavailable |
| deep_research / 7 | [Benchmarking Agents for Proving Theorems in Quantum Algorithms and Quantum Information](../../docs/deep-research/papers/benchmarking-agents-for-proving-theorems-in-quantum-algorithms-and-quantum-informati-40e5dee1.html) | `openalex:W7171268496` | not_assessed | manuscript_unavailable |
| deep_research / 8 | [Is Deep Research Reliable? Misleading Knowledge Induces False Conclusions](../../docs/deep-research/papers/is-deep-research-reliable-misleading-knowledge-induces-false-conclusions-bca45ce7.html) | `openalex:W7171268620` | not_assessed | evidence_grounding_failure |
| deep_research / 9 | [LegalCiteTrust: Benchmarking Citation Trustworthiness in Chinese Long-Form Legal Research Reports](../../docs/deep-research/papers/legalcitetrust-benchmarking-citation-trustworthiness-in-chinese-long-form-legal-rese-8ff075eb.html) | `doi:10.48550/arxiv.2607.20872` | not_assessed | scientific_uncertainty |
| deep_research / 10 | [AREX: Towards a Recursively Self-Improving Agent for Deep Research](../../docs/deep-research/papers/arex-towards-a-recursively-self-improving-agent-for-deep-research-55755800.html) | `openalex:W7171268386` | not_assessed | scientific_uncertainty |

## Technical findings

- Four evidence_grounding_failure outcomes (Agent Memory positions 6, 9, 10; Deep Research position 8) all cite a code/data-release sentence in abstract block B0003 for reproducibility together with body/appendix evidence. Correct-source provenance passes, but the frozen role policy marks the abstract hard-ineligible. One ineligible reference prevents the entire batched verifier, withholding all proposed claims for that paper. This is a repeated pipeline selection/eligibility failure, not four scientifically weak papers.

- MemForest (Agent Memory position 4) acquired a manuscript but failed before a model call: the normal path raised a UTF-8 encoding error for surrogate U+D835 at position 12534. No assessment row was stored. The technical outcome, acquisition metadata and error log remain preserved; no text repair or manual replacement assessment was introduced.

- There were no malformed model envelopes/schema results, output-limit truncations, assessor retries, transport failures, executed-verifier failures or stored text-coverage failures. Four verifiers were skipped because of reference failures; skipped calls are not counted as failed verifier requests.

- Post-freeze inspection of all eight scientific uncertainties found both legitimate snippet-support gaps and avoidable conservatism. Examples include numbered contribution bullets and an Experiment 1 locator being treated as numerical claims, and a10-user extraction defeating the number boundary check. The biometric paper also has a genuine uncited K=10 detail; these mixed cases are not silently promoted or reclassified as successful assessments.

- The graph-memory survey has all nine proposed evidence items accepted, but lacks a supported positive methodological-rigor item. Its concern about absent search/inclusion criteria makes withholding a pass defensible; the generic final uncertainty message is less informative than the underlying audit.

## Observational scientific audit

Predefined positions 1, 6 and 10 in both populated tracks were frozen before model calls. All passes and all scientific-insufficient results are added automatically. This audit inspected saved manuscript text and canonical evidence after the complete automatic batch was frozen. It made no corrections.

### agent_memory / 1: MBM-0: Memory Birth Metrics v0

Audit inclusion: predefined_first_middle_last. Outcome: `manuscript_unavailable`.

- **Topical fit:** Sensible from title and abstract: a measurement protocol for agent-memory birth, survival, activation and behavior impact is directly on topic.
- **Manuscript evidence:** No manuscript source URL was present in the frozen candidate. No manuscript acquisition or model call occurred; title/abstract only.
- **Status defensibility:** Manuscript unavailable is appropriate. The abstract alone cannot establish validation of the six proposed metrics.
- **Evidence grounding:** No accepted evidence claims; no full-text scientific judgment was implied.
- **Limitations:** The explicit no-manuscript/no-semantic-assessment statement bounds the result. Whether the metrics resist gaming or predict utility remains unassessed.
- **Claim calibration:** The pipeline withholds a scientific judgment; it does not treat the proposal as validated.
- **False confidence:** No pass and no manuscript-level confidence.
- **Excessive conservatism:** No demonstrated structural conservatism; this is an acquisition limitation. No replacement URL or paper was supplied.

### agent_memory / 6: Closing the Consistency Gap: Self-Evolving Agents That Learn to Stay on Course

Audit inclusion: predefined_first_middle_last. Outcome: `evidence_grounding_failure`.

- **Topical fit:** Sensible: episodic guidelines derived from trajectory instability are an agent-memory mechanism with repeatability and transfer evaluation.
- **Manuscript evidence:** The title matches. All nine PDF pages extracted; methods, AppWorld evaluation, discussion/limitations and appendix were available, with no body omission or extraction truncation. The manuscript compares repeated runs and distinguishes stability from correctness.
- **Status defensibility:** This is an evidence-grounding failure, not scientific uncertainty about the paper. Withholding a scientific judgment is safe, but useful manuscript content did not produce an assessment.
- **Evidence grounding:** All eight proposed claims were withheld. The reproducibility item cited Eab63d8b945096f8e-B0003 (abstract code URL) together with B0029 (experimental setup). The abstract source is hard-ineligible for this role, so the verifier never ran. The IDs are from the correct manuscript; this is a role/selection failure, not cross-paper evidence.
- **Limitations:** The manuscript discusses uncontrolled platform nondeterminism, stability versus correctness, limited agent/model coverage, admitting unvalidated guidelines and roughly 30-fold resampling cost. These were available but no scientific evidence survived the reference failure.
- **Claim calibration:** The proposed method/results claims included values absent from their exact snippets. Those proposals remain audit data; none is promoted to accepted evidence.
- **False confidence:** No false pass; the safety gate withheld the proposed pass.
- **Excessive conservatism:** A real code URL located immediately below the abstract triggered an all-or-nothing role exclusion. The same abstract/reproducibility pattern appears in four papers; it is a systematic pipeline reliability limitation.

### agent_memory / 10: Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems

Audit inclusion: predefined_first_middle_last. Outcome: `evidence_grounding_failure`.

- **Topical fit:** Strong fit: revoked versus current memory, retrieval enforcement, unsafe actions, write-back and propagation directly stress knowledge supersession.
- **Manuscript evidence:** The title matches. All 20 pages extracted; methods, nine-scenario/nine-model evaluation, defense conditions, guard design, appendices and compute accounting were present. No body omission or truncation was recorded.
- **Status defensibility:** Evidence-grounding failure is the correct top-level category. It cannot be counted as a scientific negative result or an insufficient paper.
- **Evidence grounding:** All nine proposals were withheld. E5950c57d2c67485e-B0003 contains the abstract code-release statement; B0063/B0064 contain compute costs. The former is hard-ineligible for reproducibility, preventing the batched verifier. All sources belong to this manuscript.
- **Limitations:** The manuscript distinguishes natural from controlled direct write-back, limits the guard to exposed facts/marks and reports compute costs. Broader system coverage and deployment generalization require caution. The stored failure does not provide a scientific limitations synthesis.
- **Claim calibration:** The compute text supports 44,550 calls for the main grid and $79.08 total across experiments, rather than $79.08 for the main grid alone. These remain proposed claims. Another proposal referenced 44.2% outside its exact cited snippets.
- **False confidence:** No pass; unsupported or unverified proposals did not become accepted evidence.
- **Excessive conservatism:** A genuine code-release sentence in the abstract plus substantive appendix evidence was rejected by the same shared role rule. No manual evidence relocation was performed.

### deep_research / 1: A New Paradigm: Agentic AI for Scientific Discovery

Audit inclusion: predefined_first_middle_last. Outcome: `scientific_uncertainty`.

- **Topical fit:** Sensible: the review concerns autonomous scientific workflows, literature synthesis, verification and research agents.
- **Manuscript evidence:** The title and DOI match the 45-page manuscript. All pages extracted and useful body/supplement-style content was selected. Whitespace and heading detection are noisy, but there is no recorded body omission or truncation. Definitions, workflow, evidence tables and limitations are present.
- **Status defensibility:** Uncertainty is defensible for the cited claim set. The exact snippets do not establish every domain/prior-system name asserted in the proposed narrative. This is not manuscript unavailability. It also should not be read as disproving those statements elsewhere in the paper.
- **Evidence grounding:** Seven accepted claims were checked against their saved snippets. The four characteristics, six-stage workflow, stated failure rates and explicit methodological limitations are present. A qualification remains: the novelty explanation says this synthesis is unavailable in a single source elsewhere; the cited table cannot establish that external uniqueness claim. PRISMA adherence is the authors' statement, not an independently verified search audit.
- **Limitations:** Accepted evidence represents non-preregistration, qualitative risk-of-bias assessment, database restrictions, preprint dependence, heterogeneous evidence, narrow LLM scope and lack of empirical validation of the workflow. These are meaningful scientific limitations.
- **Claim calibration:** Most claims are manuscript-attributed and bounded, but the accepted external-uniqueness explanation is stronger than its canonical support. Reported rates were checked as statements in this manuscript, not independently replicated facts.
- **False confidence:** No false pass. This accepted explanation is still a grounding/calibration concern despite the uncertain final status.
- **Excessive conservatism:** Some rejected text has genuine snippet-selection gaps; the numeric check also rejects a Table 2 locator/year when absent from the cited blocks. These mixed causes mean the uncertainty is not a clean measure of scientific weakness.

### deep_research / 6: AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping

Audit inclusion: predefined_first_middle_last. Outcome: `manuscript_unavailable`.

- **Topical fit:** Sensible: the abstract describes a multi-agent literature-review, extraction, synthesis and citation-mapping architecture with memory and a worked case study.
- **Manuscript evidence:** No known manuscript URL in the frozen record; no manuscript or model call. The metadata itself says benchmark-scale quantitative evaluation is future work.
- **Status defensibility:** Manuscript unavailable is appropriate. The future-evaluation statement is not converted into scientific insufficiency without the manuscript.
- **Evidence grounding:** Three retained deterministic metadata signals are not verifier-accepted scientific claims. The abstract explicitly states the contribution and mentions evaluation; the heuristic concern that no review-selection methodology was detected is limited to available text.
- **Limitations:** The public no-manuscript/no-semantic-assessment rationale is the main bound. The abstract's stated lack of completed benchmark-scale evaluation is visible in metadata but remains unaudited scientifically.
- **Claim calibration:** No main-library admission. Auxiliary heuristic scores/signals must not be interpreted as manuscript-verified methodological findings.
- **False confidence:** No pass and full_text_assessed is false.
- **Excessive conservatism:** No demonstrated format penalty; manuscript acquisition was unavailable from the stored source candidates.

### deep_research / 10: AREX: Towards a Recursively Self-Improving Agent for Deep Research

Audit inclusion: predefined_first_middle_last. Outcome: `scientific_uncertainty`.

- **Topical fit:** Strong fit: recursive deep research, constraint-wise verification, context updating and multi-stage training directly address long-horizon research workflows.
- **Manuscript evidence:** The AREX title matches the acquired manuscript. All 20 pages extracted; framework, data construction, training, experimental setup, tables, ablations and conclusion were selected. References were excluded; no body omission or extraction truncation was recorded.
- **Status defensibility:** Uncertainty is defensible for the exact submitted evidence set. The six-benchmark statement and comparator value 77.5 exist in the full manuscript, but were not established by the snippets selected for the relevant claims/narrative. This is evidence selection friction, not proof that the experiment lacks six benchmarks.
- **Evidence grounding:** Eight accepted claims were checked. Inner/outer loop descriptions, novelty positioning and the BrowseComp ablation values 59.6, 71.4 and 82.5 are supported. Some explanation details are broader than the cited passages: the reproducibility claim mentions model links, yet cites training-data paragraphs rather than the front-matter links. Global absence-of-release/section claims require the broader manuscript, not just a local paragraph.
- **Limitations:** The audit confirmed no dedicated related-work or limitations section in the supplied manuscript. The assessment notes unreleased training artifacts and open step-utility/credit-assignment questions. Presence of a future-work sentence is weaker than a full failure-mode or robustness analysis.
- **Claim calibration:** Numerical ablation claims are appropriately scoped to BrowseComp. Paper-wide absence inferences and uncited model-link details should be treated cautiously; the public uncertain status avoids a confident endorsement.
- **False confidence:** No false pass. The accepted model-link/detail mismatch is an evidence-boundary concern.
- **Excessive conservatism:** The six-benchmark and 77.5 claims are supported elsewhere in the manuscript, so selected-snippet conservatism contributes. No evidence IDs were repaired and no proposal was rerun.

All-pass inspection: Zero passes: there were no pass records to inspect, no new library admissions and no observed false pass. This provides no positive evidence that the pipeline can generalize successful admission; absence of false passes is not treated as success.

All-insufficient inspection: Zero scientific_insufficient outcomes: no unavailable, failed or truncated assessment was mislabeled as scientific insufficiency.

Cross-paper observations: All 12 initial scientific proposals were pass, but the frozen pipeline retained none. The four eligibility failures share a concrete cause. Of the eight scientific uncertainties, seven have rejected claims/narratives and one lacks a required positive method criterion. The two predefined audited scientific full-text records retain useful evidence and limitations, but both contain accepted explanation details beyond their own canonical snippets. Numeric spelling/layout and evidence-window selection also contribute conservatism. This audit cannot estimate general pass precision or Engram performance because neither has observations here.

## Reliability

- **acquisition:** unavailable manuscripts = 7; no known source urls = 6; source attempts = 14; failed source attempts = 1; successful manuscripts = 13; cache hits = 0; alternate source recoveries = 0.
- **model:** initial calls = 12; retry calls = 0; truncations = 0; malformed or schema invalid responses = 0.
- **grounding:** metadata only signals not verified claims = 19; proposed = 109; accepted = 60; rejected = 49; grounding failures = 4.
- **verifier all items including narratives:** supported = 81; uncertain = 9; skipped due to reference failure = 4; calls = 8; unsupported = 0; technical failures = 0.
- **coverage:** title and abstract = 7; full text = 12; coverage failures = 0; partial full text = 0; extraction truncated = 0; body selection omission = 0.
- **manual interventions:** 0.

Scientific grounding counts exclude 19 deterministic title/abstract signals retained in unavailable-manuscript records. There were 109 model-proposed evidence items, 60 accepted and 49 withheld: 4 hard-ineligible references, 31 other items blocked by those reference failures, 12 numeric-guard rejections and 2 other semantic rejections. Verifier item counts include two narratives per executed call; supported verifier judgments can still be rejected by the deterministic numeric guard. Thirteen manuscripts were acquired; twelve reached a full-text stored assessment and one failed UTF-8 encoding before a model call. Zero recorded coverage failures means zero dedicated coverage-gate outcomes, not flawless extraction. No output was repaired.

Verifier breakdown: claim supported = 69, narrative supported = 12, claim uncertain = 5, narrative uncertain = 4.

## Batch-2 inference costs

Only requests made for these 20 frozen entries are included. Provider-reported costs are used; all unrelated development, review and calibration costs are excluded.

| Call type | Calls | Input tokens | Output tokens | Reported USD | Unknown-cost calls |
|---|---:|---:|---:|---:|---:|
| initial | 12 | 455,916 | 25,725 | $0.554727020 | 0 |
| retry | 0 | 0 | 0 | $0.000000000 | 0 |
| verifier | 8 | 119,652 | 5,477 | $0.160545116 | 0 |

Total Batch-2 inference cost: **$0.715272136**. Unknown-charge requests: 0. The $10 ceiling was respected. Initial + retry rows form assessment costs; retry is listed separately to avoid double counting. Verifier cost includes its claim and narrative checks.

## Historical integrity and validation

All **559 prior assessment rows** remain byte-equivalent by canonical row hash; all previous current decisions and non-quality runtime tables are unchanged. All original 28 calibration decisions and admission fields remain unchanged, with zero overlap and no prior-assessment contamination. New stored rows: agent_memory=9, deep_research=10, engram=0.

Complete unit suite: **301 passed**. All three relevance, quality, discovery, idempotency and offline-build checks passed, as did sidecar schemas, local links, exposure scans, workflow checks, file-size guards and `git diff --check`. Three-database snapshot/restore and legacy two-database restore passed. All 578 saved quality records remain readable; accepted evidence compatibility checks passed.

Main library counts: 4 / 5 / 6. Batch-2 review/main visibility checks: all expected interfaces verified.

## Persistence and publication

Manifests, hash sidecars, this report, structured evaluation JSON and normal generated cards are version controlled. Raw request/results, extraction, canonical snippets, acquisition records, stored rows, ledgers, audit packets, hashes and operator scripts are retained in the ignored `data/cache/operator/batch-2-20260917/` directory. No secrets, hidden reasoning, runtime databases, PDFs or raw model payloads are committed. Failed execution without a stored assessment is preserved in the run ledger and this report.

Validated runtime snapshot SHA-256: `2d7f756f2867c453a794ada7aea3a80e8eb9fa64afa17ba635393673e580478a`.

Runtime state published to the established `paper-scout-runtime-state` release asset, then downloaded and restored with identical snapshot and database hashes.

One deploy-only Pages dispatch is planned after persistence.
