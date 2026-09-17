# Batch-2 engineering and recovery — 2026-09-17

ORIGINAL_BATCH_2_GENERALIZATION_RESULT = FAIL

The original unseen holdout is permanently frozen: 20 selected papers, 0 quality passes, 8 scientific uncertainties, 0 scientific insufficiencies, 7 unavailable manuscripts and 5 technical failures (four abstract/code-link eligibility failures and one Unicode failure). Its inference cost was $0.715272136. Engineering based on these failures makes the same 20 papers regression data; this recovery cannot demonstrate generalization. No Batch 3 was started.

[Original report](batch-2-quality-evaluation-2026-09-17.md) · [Unchanged roster](../../experiments/manifests/batch-2-roster-2026-09-17.json) · [Pre-edit inventory](batch-2-recovery-inventory-2026-09-17.md) · [Recovery cost/protocol manifest](../../experiments/manifests/batch-2-recovery-2026-09-17.json).

## Root causes and engineering fixes

- **Four artifact failures:** Closing the Consistency Gap, MeClear, Revoked but Still Authoritative, and Is Deep Research Reliable each cited a real abstract code/data URL as reproducibility evidence. IDs and source provenance were valid, but the scientific section rule rejected the abstract and skipped the entire verifier. `artifact_availability` now stores only exact, source-attributed URL facts with a non-verification disclaimer. It permits paper-associated abstract/front-matter/appendix metadata, rejects invented or foreign URLs and references/gaps, and cannot satisfy a scientific gate criterion or contribute to the scientific narrative source union. The raw model proposal is retained separately in the execution audit; typed artifact display is derived deterministically, not manually corrected. No repository existence or functionality check is claimed.
- **Unicode:** MemForest extraction contained lone UTF-16 high-surrogate code units, which reached `assessment_input_sha256` and failed at UTF-8 encoding before any assessment call. Canonical normalization now combines valid pairs and visibly replaces irrecoverable units with U+FFFD before hashing, evidence IDs, prompt transport, storage and rendering. Scientific Unicode remains intact; coverage records the repair count/version. The raw cache and PDF source hash are preserved. No missing symbol is guessed.
- **Conservatism:** Experiment/table locators and ordered list labels were incorrectly treated as scientific quantities, and extraction such as `a10-user` hid an otherwise exact quantity. Those boundaries are fixed. Missing K=10, an uncited 3x control, ambiguous table columns and a missing positive methodology criterion remain legitimate uncertainty. There is no pass-rate target and no rubric/threshold adjustment.
- **Evidence context:** A scientific claim may request the immediate contiguous neighbors of one primary canonical block, at most three blocks in the same supplied section and role. Windows cannot cross a section, omitted selection or gap; every resolved ID, hash and source span is retained.
- **Overreach:** Claims and explanations receive separate directional support judgments against their exact sources. Both must pass. The verifier checks quantifiers, units, denominator, scope and every clause, rather than topical similarity. Scoped assessor inference remains explicit. Local guards address known external-priority, broad absence and partial-to-universal claims, without treating a supported negative critique as a universal positive. These checks are bounded screening, not proof of truth; the observational audit below determines remaining limitations.

Discovery, relevance, authors/affiliations, publication status, acquisition strategy, the six scientific gate dimensions, main-library admission and historical migration are unchanged. Admission remains high relevance AND scientific quality pass AND not suppressed.

## Independent review and merge

[PR #32](https://github.com/vernerisirva/agentmempaper/pull/32) merged as `d2901416339af5f43b2d48b7d93141d6e49f196a`. Final reviewed candidate: `45d6ea5da8f86320537e66cb512511e907fb9b41`. Exact-candidate CI and all 318 tests passed; zero unresolved blockers and no material unreviewed production changes remained.

| Reviewer | Verdict | Cost |
|---|---|---:|
| deepseek/deepseek-v4-pro-0813 | No verdict: output budget exhausted | $0.116255040 |
| anthropic/claude-opus-4.6 | PASS_WITH_NOTES | $0.222100000 |
| anthropic/claude-opus-4.6 | PASS_WITH_NOTES | $0.243880000 |

The first DeepSeek call used its completion budget on reasoning and returned no visible verdict. The established authorized Opus fallback returned PASS_WITH_NOTES, zero blockers. A supplemental Opus call completed production-code coverage omitted by the default 18 KB per-file collector, keeping the 200 KB request ceiling. The large diagnostic inventory remained partially truncated externally; frozen hashes and all 20 rows were checked locally. Across the two Opus reviews, the only omitted test tail was 82 bytes ending a source literal and an instruction-presence assertion. The optional-field note does not identify a runtime defect: provider strict schemas require fields in new requests, while local legacy fixtures use explicit scientific/empty/false defaults. Independent review was static; tests ran separately.

## Frozen recovery protocol

Evaluator `d2901416339af5f43b2d48b7d93141d6e49f196a`, assessment version `quality-batch2-recovery-v1`, assessor/verifier `deepseek/deepseek-v4-pro-0813`, reasoning off, temperature 0, no fixed seed. Evidence addressing stays `block-evidence-v2`; eligibility is `artifact-purpose-v1`, semantic verification `claim-support-v2`, normalization `canonical-unicode-v2`. Rubric `scholarly-rubric-v1` and gate `scientific-gate-v1` are unchanged.

Exact roster SHA-256: `af89dc0d58a24b3e894a15794447e7af4ff96fde40989b70c7ab5e1b355e6d82`. Recovery outcomes frozen at 2026-09-17T10:50:50.552656+00:00 before audit. The normal production CLI used the same source candidates and immutable candidate records; no replacements, manual corrections or pipeline edits occurred during recovery. At most two assessment calls and one 4096-token verifier call per paper; verifier input cap 250,000 bytes, no verifier retry.

## Original versus recovery

| Outcome | Original overall | Recovery Agent Memory | Recovery Deep Research | Recovery Engram | Recovery overall |
|---|---:|---:|---:|---:|---:|
| quality_pass | 0 | 0 | 0 | 0 | 0 |
| scientific_uncertainty | 8 | 7 | 3 | 0 | 10 |
| scientific_insufficient | 0 | 0 | 0 | 0 | 0 |
| manuscript_unavailable | 7 | 1 | 5 | 0 | 6 |
| evidence_grounding_failure | 4 | 1 | 2 | 0 | 3 |
| model_protocol_failure | 0 | 1 | 0 | 0 | 1 |
| text_coverage_failure | 0 | 0 | 0 | 0 | 0 |
| other_technical_failure | 1 | 0 | 0 | 0 | 0 |

Technical failures / all selected: agent_memory=2/10, deep_research=2/10, engram=0/0, overall=4/20.

Rates use all selected entries: 10 Agent Memory, 10 Deep Research, 0 Engram; no Engram percentage is defined.

| Track / position | Paper / ID | Original → recovery | Original code defect | Accepted claims old → new / changed | Recovery category / explanation |
|---|---|---|---|---|---|
| agent_memory / 1 | MBM-0: Memory Birth Metrics v0 · `doi:10.5281/zenodo.22671447` | manuscript_unavailable → manuscript_unavailable | None identified | 0 → 0 / no | acquisition: No manuscript URL; unchanged acquisition limitation. |
| agent_memory / 2 | Beyond Agent Harnesses: Cross-Substrate Authority for Multi-Agent Systems · `doi:10.48550/arxiv.2609.08472` | scientific_uncertainty → scientific_uncertainty | Yes | 6 → 4 / yes | scientific: Locator handling improved, but citation-fragmentation and a supported-design/evaluative-explanation mismatch remain. |
| agent_memory / 3 | Personalizing LLM Agent Memory Using Biometrics · `doi:10.48550/arxiv.2609.08558` | scientific_uncertainty → scientific_uncertainty | Yes | 6 → 7 / yes | scientific: The extracted a10-user protocol is now accepted; other uncited numeric and broad-absence claims retain uncertainty. |
| agent_memory / 4 | MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging · `doi:10.48550/arxiv.2609.08273` | other_technical_failure → scientific_uncertainty | Yes | 0 → 3 / yes | scientific: Unicode normalization automatically processes malformed surrogate units; normal assessment succeeds, but claim-specific numeric/context support remains unresolved. |
| agent_memory / 5 | What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory · `doi:10.48550/arxiv.2609.08279` | scientific_uncertainty → scientific_uncertainty | None identified | 8 → 8 / yes | scientific: One scoped 3x positive-control claim is accepted with correct sources; another local citation gap and a priority claim keep uncertainty. |
| agent_memory / 6 | Closing the Consistency Gap: Self-Evolving Agents That Learn to Stay on Course · `doi:10.48550/arxiv.2609.08832` | evidence_grounding_failure → model_protocol_failure | Yes | 0 → 0 / no | technical: The real abstract artifact URL now passes eligibility; a provider-terminal verifier error replaces the original grounding failure. |
| agent_memory / 7 | CreaMem: A Scene-Aware Memory Architecture for Personalized Agents · `doi:10.48550/arxiv.2609.08550` | scientific_uncertainty → evidence_grounding_failure | None identified | 6 → 0 / yes | technical: A new citationless optional artifact item withholds the whole verifier; this is technical, not a scientific downgrade. |
| agent_memory / 8 | Graph-Based Personalized Memory for LLM Agents: Representation, Evolution, Retrieval, and Evaluation · `doi:10.48550/arxiv.2609.08599` | scientific_uncertainty → scientific_uncertainty | None identified | 9 → 9 / yes | scientific: All nine structured items survive, but a narrative absence assertion is withheld; audit finds an accepted explanation importing uncited benchmark names. |
| agent_memory / 9 | MeClear: Cooperative Game-Theoretic Attribution and Risk-Aware Memory Clearance for Long-Horizon LLM Agents · `doi:10.48550/arxiv.2609.09115` | evidence_grounding_failure → scientific_uncertainty | Yes | 0 → 4 / yes | scientific: The abstract code link is now accepted as narrow metadata; uncited parameters/results and subgroup claims keep scientific support unresolved. |
| agent_memory / 10 | Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems · `doi:10.48550/arxiv.2609.08258` | evidence_grounding_failure → scientific_uncertainty | Yes | 0 → 4 / yes | scientific: The code link and scoped limitation are accepted; several method/result/narrative details are not established by their own selected citations. |
| deep_research / 1 | A New Paradigm: Agentic AI for Scientific Discovery · `doi:10.65649/ukh4n33x` | scientific_uncertainty → scientific_uncertainty | Yes | 7 → 5 / yes | scientific: Several contribution/table/limitation claims survive; mixed inference and citation issues remain, including accepted explanation overreach. |
| deep_research / 2 | A PRISMA-Aligned Agentic Framework for Medical Systematic Reviews and Evidence Synthesis · `doi:10.64898/2026.07.30.26359375` | manuscript_unavailable → manuscript_unavailable | None identified | 0 → 0 / no | acquisition: No known manuscript URL; unchanged acquisition limitation. |
| deep_research / 3 | Towards Reliable AI Scientists · `doi:10.6082/gep96-ycs43` | manuscript_unavailable → manuscript_unavailable | None identified | 0 → 0 / no | acquisition: No known manuscript URL; unchanged acquisition limitation. |
| deep_research / 4 | Deep Research Agent: An AI-Powered System for Automated Research Paper Analysis and Citation-Based Answer Generation · `doi:10.65890/race.v2i2.204` | manuscript_unavailable → manuscript_unavailable | None identified | 0 → 0 / no | acquisition: No known manuscript URL; unchanged acquisition limitation. |
| deep_research / 5 | When the Instrument Studies Itself: A Systematic Map of Autonomous AI Research Systems (2024-2026), Conducted by a Frontier Language Model · `doi:10.5281/zenodo.21577092` | manuscript_unavailable → manuscript_unavailable | None identified | 0 → 0 / no | acquisition: No known manuscript URL; unchanged acquisition limitation. |
| deep_research / 6 | AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping · `doi:10.5281/zenodo.21523008` | manuscript_unavailable → manuscript_unavailable | None identified | 0 → 0 / no | acquisition: No known manuscript URL; unchanged acquisition limitation. |
| deep_research / 7 | Benchmarking Agents for Proving Theorems in Quantum Algorithms and Quantum Information · `openalex:W7171268496` | manuscript_unavailable → evidence_grounding_failure | None identified | 0 → 0 / no | technical: The same arXiv URL now yields a manuscript; a citationless absence item prevents all semantic verification. |
| deep_research / 8 | Is Deep Research Reliable? Misleading Knowledge Induces False Conclusions · `openalex:W7171268620` | evidence_grounding_failure → scientific_uncertainty | Yes | 0 → 7 / yes | scientific: Both abstract artifact links are accepted. Several scientifically supported quantitative claims are still falsely rejected at glued-word boundaries; other claims genuinely lack adjacent context. |
| deep_research / 9 | LegalCiteTrust: Benchmarking Citation Trustworthiness in Chinese Long-Form Legal Research Reports · `doi:10.48550/arxiv.2607.20872` | scientific_uncertainty → scientific_uncertainty | None identified | 10 → 10 / yes | scientific: Ten claims survive, but narrative and local statistic gaps remain; audit finds a split product URL incorrectly accepted as a shortened link. |
| deep_research / 10 | AREX: Towards a Recursively Self-Improving Agent for Deep Research · `openalex:W7171268386` | scientific_uncertainty → evidence_grounding_failure | None identified | 8 → 0 / yes | technical: New deterministic false rejection: a complete trailing-slash URL is joined to the following Models: label. All three proposed URLs actually occur in the cited block. |

Scientific wording can change across stochastic calls. Count changes alone do not establish a causal engineering benefit. Case-specific audit findings and exact accepted/rejected evidence are retained in the structured report.

## Observational audit

The same predefined positions 1, 6 and 10 in each populated track were audited after freezing all outcomes, together with every recovery pass and insufficient result. Additional defect diagnostics do not replace that sample. No assessment was edited.

### agent_memory / 1: MBM-0: Memory Birth Metrics v0

Inclusion: same_predefined_batch2_sample. Outcome: `manuscript_unavailable`.

- **Topical fit:** Direct fit: agent-memory growth metrics, behavioral impact and an anti-gaming measurement protocol.
- **Manuscript evidence:** No known manuscript source URL; only metadata/abstract was available, exactly as in the original run.
- **Status defensibility:** Manuscript unavailable is defensible. This is not a scientific insufficiency or a completed quality judgment.
- **Evidence grounding:** No manuscript-grounded quality claim was admitted.
- **Limitations:** The abstract describes metrics, but cannot establish their validity, controls or empirical adequacy.
- **Claim calibration:** No benchmark effectiveness or methodological-quality conclusion can be drawn from this entry.
- **False confidence:** No pass and no manuscript-quality claim.
- **Excessive conservatism:** Not diagnosed: acquisition is the limiting condition, not a rejection of supplied scientific evidence.

### agent_memory / 6: Closing the Consistency Gap: Self-Evolving Agents That Learn to Stay on Course

Inclusion: same_predefined_batch2_sample. Outcome: `model_protocol_failure`.

- **Topical fit:** Relevant to self-evolving agents and consistency of reusable agent skills, adjacent to the agent-memory evaluation scope.
- **Manuscript evidence:** Full cached manuscript, no extraction/selection omission; the original abstract repository URL is present in canonical block Eab63d8b945096f8e-B0003.
- **Status defensibility:** The artifact eligibility defect is removed, but the verifier returned a provider-terminal error. The result is a technical protocol failure, not defensible scientific uncertainty.
- **Evidence grounding:** All nine proposed items had valid candidate grounding and the artifact URL passed deterministic presence/role checks. The failed verifier produced no accepted semantic result, so all claims were withheld.
- **Limitations:** The archived proposal also contains uncited numbers and a rationale requiring sources beyond its own cited union; provider failure prevents a completed scientific decision.
- **Claim calibration:** No repository existence/functionality was asserted in an accepted claim, and no unverified scientific proposal was promoted.
- **False confidence:** No false pass: the execution records a failed verifier. The generic uncertainty must be interpreted with that technical outcome.
- **Excessive conservatism:** Technical unavailability of semantic verification dominates. No claim is made that this paper deserves uncertainty or insufficiency on scientific grounds.

### agent_memory / 10: Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems

Inclusion: same_predefined_batch2_sample. Outcome: `scientific_uncertainty`.

- **Topical fit:** Strong direct fit: runtime enforcement of revoked/superseded records in five agent-memory systems.
- **Manuscript evidence:** All 20 PDF pages extracted, no body omission or gap; methods, nine-scenario/nine-model setup, results, guard and appendices supplied.
- **Status defensibility:** The original repository-link failure is fixed. Four of nine claims survive. Uncertainty includes real citation-fragmentation failures: method equations, six defense conditions, matched comparisons and ablation details are not established by the selected IDs for those proposed claims.
- **Evidence grounding:** The contribution uses B0004-B0005; the repository is a narrow attributed artifact in B0003; the uncontrolled scenario-group comparison is explicitly acknowledged in B0045. Exact text/provenance checks pass.
- **Limitations:** The accepted scoped limitation is substantive: rule-carrying/no-rule groups differ in scenario, actions and distractors and were not a controlled comparison.
- **Claim calibration:** The accepted previously-unexamined wording is supported as the paper's own related-work positioning in B0014-B0015, not independent proof of external priority. It should be read with that source attribution; broad novelty is not established externally.
- **False confidence:** No pass. The repository disclaimer and scoped limitation prevent a code link from becoming evidence of scientific adequacy.
- **Excessive conservatism:** Mixed. Several missing details exist elsewhere in the supplied manuscript but not in the claim's citations. That is an evidence-selection/wording problem, not grounds for declaring the underlying study scientifically weak.

### deep_research / 1: A New Paradigm: Agentic AI for Scientific Discovery

Inclusion: same_predefined_batch2_sample. Outcome: `scientific_uncertainty`.

- **Topical fit:** Direct fit: a conceptual review of agentic scientific discovery, literature synthesis, trust and validation.
- **Manuscript evidence:** All 45 PDF pages extracted, 155031 eligible body characters retained, no extraction or selection omission. Table 2 and explicit methodological/evidence/scope limitations are available.
- **Status defensibility:** Uncertainty is reasonable for an unvalidated conceptual workflow with non-preregistered and qualitative review methods. However, it also contains claim-selection and inference-label problems; it is not a clean measure of the paper's quality.
- **Evidence grounding:** Five of nine items survive. Contribution and scope have clear attributed sources. The 42% and 6–18% table values appear in B0072; limitations appear in B0133-B0134. One accepted explanation still cites claims outside its own block: the alignment item cites only B0076 but names execution failures, citation fabrication, structural errors and self-improvement regression from other table blocks.
- **Limitations:** The manuscript explicitly acknowledges non-preregistration, qualitative risk-of-bias handling, heterogeneous evidence, unreviewed preprints, LLM-focused scope and lack of empirical validation for its six-stage workflow.
- **Claim calibration:** The original external-uniqueness overclaim is absent. Residual explanation overreach remains despite separate verification; the displayed limitation claim also ends mid-word at its length limit.
- **False confidence:** No false pass, but an accepted explanation is broader than its own cited source. Claim-scope recovery is therefore incomplete.
- **Excessive conservatism:** Mixed. Some rejected explanation text is an evaluative inference labelled source_claim, while other claims lack the details in their own cited windows. Reasonable conceptual-review caution must be separated from those protocol/wording effects.

### deep_research / 6: AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping

Inclusion: same_predefined_batch2_sample. Outcome: `manuscript_unavailable`.

- **Topical fit:** Direct fit: a multi-agent literature-review architecture with retrieval, parsing, citation mapping and synthesis agents.
- **Manuscript evidence:** No known manuscript source URL; abstract/metadata only, unchanged from original Batch 2.
- **Status defensibility:** Manuscript unavailable is appropriate and must not be read as scientific insufficiency.
- **Evidence grounding:** No manuscript-grounded scientific quality evidence was accepted.
- **Limitations:** The abstract itself distinguishes a worked case study from future benchmark-scale evaluation, but full methods and results cannot be independently assessed here.
- **Claim calibration:** No fabricated benchmark result, broad performance claim or pass is added.
- **False confidence:** No quality pass and no assessment of unseen manuscript methods.
- **Excessive conservatism:** Not diagnosed; missing manuscript access is the reason no scientific judgment is established.

### deep_research / 10: AREX: Towards a Recursively Self-Improving Agent for Deep Research

Inclusion: same_predefined_batch2_sample. Outcome: `evidence_grounding_failure`.

- **Topical fit:** Direct fit: recursively improving deep-research agents and multi-benchmark evaluation.
- **Manuscript evidence:** Full cached manuscript supplied. Canonical B0003 contains the app, homepage and Hugging Face collection links, all three correctly proposed by the assessor.
- **Status defensibility:** This is a new engineering failure, not scientifically defensible uncertainty. URL normalization joins the homepage ending in slash with the following Models: line, so a real source URL falsely fails the membership check.
- **Evidence grounding:** No accepted claims: this reference failure skips the verifier and withholds the other ten candidate claims too. Exact source text and a minimal reproducer are saved in new-url-boundary-defect.json.
- **Limitations:** The manuscript has method/results/compute detail, but no completed scientific assessment survived. Other proposed claims still include a locally uncited 77.5 value and broad absence language.
- **Claim calibration:** The prior unsupported artifact-release interpretation is not emitted; however, correct URL metadata is now rejected by a new parser defect.
- **False confidence:** No false pass; the main risk here is technical failure being mistaken for paper-level scientific uncertainty.
- **Excessive conservatism:** Confirmed engineering false rejection: the full links exist in the exact cited block. The run was not manually corrected or repeated.

## Additional recovery diagnostics

- **deep_research / 10 — new url boundary defect:** A complete trailing-slash URL is concatenated with the next Models: label and URL, causing false rejection of correct artifact metadata. Canonical sources: `Ed069fe16ffa6b527-B0003`.
- **agent_memory / 7 — citationless optional evidence poisoning:** The model emits an optional reproducibility/absence item with zero evidence IDs. The schema accepts the empty list, then reference validation skips verification of every otherwise candidate-valid claim. CreaMem says no URL candidates were supplied; the theorem benchmark infers absence from that metadata.
- **deep_research / 7 — citationless optional evidence poisoning:** The model emits an optional reproducibility/absence item with zero evidence IDs. The schema accepts the empty list, then reference validation skips verification of every otherwise candidate-valid claim. CreaMem says no URL candidates were supplied; the theorem benchmark infers absence from that metadata.
- **deep_research / 8 — residual numeric boundary false rejection:** The correct 0% value is present as FCARwas0%acrosssix; the evidence-side word boundary misses it. Canonical sources: `E5ecf27d3a2ac0fe6-B0034`.
- **deep_research / 8 — residual numeric boundary false rejection:** The exact 40.5% and 44.2% values are present as was40.5%atColdstartand44.2%; the word-boundary check misses them. Canonical sources: `E5ecf27d3a2ac0fe6-B0030`.
- **deep_research / 8 — residual numeric boundary false rejection:** The exact 57.7% value follows the glued word to; a supported quantitative claim is rejected. Canonical sources: `E5ecf27d3a2ac0fe6-B0032`.
- **deep_research / 8 — residual numeric boundary false rejection:** The exact defense ranges are present, but the first endpoints of of60–76% and and15–62% are missed because of glued extraction text. Canonical sources: `E5ecf27d3a2ac0fe6-B0041`.
- **agent_memory / 8 — accepted explanation overreach:** The accepted evaluation explanation names LoCoMo, LongMemEval and PersonaMem, but its own cited blocks contain ActMemEval/ATM-Bench/StructMemEval and metric groups instead. The names exist elsewhere in the manuscript, not in these citations. Canonical sources: `E1e232ee4e35e94c0-B0036`, `E1e232ee4e35e94c0-B0037`.
- **deep_research / 1 — accepted explanation overreach:** The accepted alignment explanation describes multiple Table-2 failure categories not present in its own B0076 citation. The block contains the final SciIntegrity-Bench row and the authors' synthesis; other cited items or the full manuscript cannot silently fill this item's source gap. Canonical sources: `E03ed43c7ff98f799-B0076`.
- **deep_research / 9 — partial url false acceptance:** A product-page URL split after tongyi.aliyun. is accepted and displayed as the incomplete https://tongyi.aliyun. The source continues com/farui/home. This is a source-extraction boundary error; the disclaimer does not make the shortened URL the paper's full link. Canonical sources: `E8f2ff4f303dcf9ed-B0025`.
- **agent_memory / 2 — inference label and verifier conservatism:** The matched-intent protocol states that only the validator changes and attributes the effect to it. The verifier accepts the claim but rejects the strong-internal-validity explanation as evaluative, under source_claim. A scoped assessor_inference would be defensible; this shows remaining assessor labelling/verification conservatism, not unsupported experimental facts. Canonical sources: `E9425c5aacc2c1e14-B0021`, `E9425c5aacc2c1e14-B0022`.

Adjacent windows were requested by 0 recovery evidence items. Their boundaries pass deterministic tests, but this batch provides no live evidence of reduced fragmentation from the optional window feature.

All passes: Zero recovery passes; the all-pass audit set is empty. This is not evidence of correct selectivity.

All insufficient results: Zero scientific-insufficient outcomes; the all-insufficient audit set is empty.

Cross-paper findings: The five original technical defects are addressed at their original failure boundaries. Three original artifact cases now accept narrow metadata; Closing the Consistency Gap passes eligibility but loses its verifier to a provider error. MemForest reaches normal assessment after visible surrogate replacement. The new URL join bug, two zero-ID responses, a provider-terminal verifier error, residual numeric false rejections and accepted explanation overreach prevent readiness. Audit distinctions are preserved; none are manually repaired in stored outputs.

## Reliability

- **acquisition:** unavailable manuscripts = 6; no known source urls = 6; source attempts = 14; failed source attempts = 0; successful manuscripts = 14; cache hits = 13; alternate source recoveries = 0.
- **model:** malformed or schema invalid responses = 1; initial calls = 14; retry calls = 0; truncations = 0.
- **grounding:** metadata only signals not verified claims = 15; proposed = 141; accepted = 61; rejected = 80; grounding failures = 3.
- **verifier all items including narratives:** uncertain = 41; supported = 175; unsupported = 4; technical failures = 1; skipped due to reference failure = 3; calls = 11.
- **coverage:** title and abstract = 6; full text = 14; coverage failures = 0; partial full text = 0; extraction truncated = 0; body selection omission = 0.
- **manual interventions:** 0.
- **latency:** maximum call seconds = 513.4505013329908; median call seconds = 58.13188845801051; calls over 180 seconds = 4; note = The 180-second HTTP setting is a socket timeout, not an overall request deadline. Observed elapsed durations are retained without adding an operator retry..

Fourteen manuscripts acquired, thirteen from cache; the previously failed arXiv retrieval for the theorem benchmark now succeeds on the same URL. Six entries still have no source URL. All fourteen reach assessment. Fourteen initial calls, zero retries, eleven verifiers (three skipped for reference failures; one provider-terminal failure). No manual intervention. Maximum observed request latency is 513.45 seconds; four calls exceed the 180-second socket timeout because it is not a total wall-clock bound.

## Costs

| Type | Calls | Input tokens | Output tokens | Reported USD |
|---|---:|---:|---:|---:|
| Recovery initial | 14 | 552,262 | 37,616 | $0.814769520 |
| Recovery retry | 0 | 0 | 0 | $0.000000000 |
| Recovery verifier | 11 | 215,558 | 12,539 | $0.258689914 |
| Independent engineering review | 3 | 129,526 | 16,902 | $0.582235040 |

Reported recovery inference total: **$1.073459434**. Engineering reviews: **$0.582235040**. Combined reported cost: **$1.655694474**. Charged or conservatively reserved: **$1.655694474**, within the $10 ceiling. Unknown-cost calls: 0. Unknown-charge requests, if any, retain their reservation and are not assumed free. Original Batch-2 inference ($0.715272136) is excluded from these recovery totals.

## History, validation and publication

All 578 original assessment rows remain unchanged, including original Batch-2 results. All 28 calibration decisions and admission fields remain unchanged; non-roster current decisions and non-quality runtime tables are unchanged. No migration or manual result correction occurred. Original roster/protocol/report hashes are unchanged and original FAIL is retained. 20 recovery rows were appended.

318 tests passed. All three tracks passed relevance, quality, discovery, idempotency, offline builds, schema/link/exposure/size checks and workflow tests; `git diff --check`, checksummed three-database snapshot/restore and legacy two-database restore passed. All 598 historical records remain readable. Main-library counts are 4 / 5 / 6.

Visibility findings: all expected interfaces verified.

Runtime snapshot SHA-256: `67cb3bd867413741cc526f88d0e0c782d4a413fd4adf4c912edd18175f92e3ba`.

The ignored `data/cache/operator/batch-2-recovery-20260917/` directory retains immutable request/response artifacts without hidden reasoning, extraction, canonical context, saved rows, cost ledger, audit packets, operator scripts and verification hashes. Original Batch-2 artifacts remain separately preserved. No secrets, databases, PDFs or raw model outputs are committed.

The existing runtime release asset was uploaded, redownloaded and restored with matching archive/database hashes.

| Recovery criterion | Result |
|---|---|
| 1. Original five failure boundaries fixed | PASS |
| 2. No new systematic technical defect | FAIL |
| 3. Automatic Unicode path | PASS |
| 4. Narrow abstract artifact handling without weaker scientific rules | PARTIAL: original four cases pass eligibility, but new URL boundary bugs remain |
| 5. No substantive unsupported claim in an audited pass | NO PASSES: vacuous, not evidence of calibration |
| 6. Claim overreach materially resolved | FAIL |
| 7. Audited uncertainty scientifically defensible, not hidden pipeline failure | FAIL |
| 8. No manual correction | PASS |
| 9. Full validation | PASS |
| 10. Independent code review | PASS_WITH_NOTES |

## Recovery verdict and readiness

Recovery FAIL: four technical failures remain (20% of the unchanged roster), including a new deterministic URL-boundary defect and a repeated empty-ID pattern that disables whole-paper verification.
Claim overreach is not materially resolved: separately verified explanations still import uncited details in the New Paradigm and graph-memory survey cases. A partial product URL is also accepted as a complete artifact link.
Excessive conservatism persists in demonstrably supported glued-number passages and in inference labelling/verification. These are engineering/representation effects, not evidence that the papers themselves are scientifically weak.
The original Unicode and four abstract-link eligibility defects no longer recur, but this does not make the entire recovery successful. No pass/insufficient target was used, no manual corrections occurred, and no Batch 3 is authorized.

Batch 3 remains unstarted. The next engineering work must address the recorded URL boundaries, citationless optional items, numeric extraction boundaries and remaining claim/explanation scope errors before a fresh unseen holdout.

```text
ORIGINAL_BATCH_2_GENERALIZATION_RESULT = FAIL
BATCH_2_RECOVERY_CHECK: FAIL
QUALITY_PIPELINE_READY_FOR_BATCH_3: NO
```
