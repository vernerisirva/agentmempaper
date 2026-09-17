# Batch-2 evidence architecture and recovery v2 — 2026-09-17

ORIGINAL_BATCH_2_GENERALIZATION_RESULT = FAIL

BATCH_2_RECOVERY_CHECK = FAIL

This is **BATCH_2_RECOVERY_V2**, a recovery/regression run on the same exposed 20 papers. It cannot establish generalization or revise either earlier failure. Batch 3 was not started. Scientific outcomes below are the automatic stored outcomes; the audit makes no manual corrections.

[Original evaluation](batch-2-quality-evaluation-2026-09-17.md) · [First recovery](batch-2-recovery-2026-09-17.md) · [Pre-edit inventory](batch-2-recovery-v2-inventory-2026-09-17.md) · [Frozen manifest](../../experiments/manifests/batch-2-recovery-v2-2026-09-17.json) · [Structured comparison and audit](batch-2-recovery-v2-2026-09-17.json).

## Canonical state and inventory before edits

The clean canonical `main` was `dadef795eebeb5d4abe30fd26bf94bf6b921c278`; PR #32 was confirmed merged. Both historical reports were read in full. The original roster was recovered without selection or replacement: ten Agent Memory papers, ten Deep Research papers, zero Engram papers. Its SHA-256 remains `af89dc0d58a24b3e894a15794447e7af4ff96fde40989b70c7ab5e1b355e6d82`.

Before coding, the complete local inventory captured 40 execution/paper records and 250 claim audits, including raw canonical blocks, whitespace-normalized diagnostic text, exact evidence IDs, source/context hashes, stages, support scope and technical-versus-claim classifications. Its SHA-256 is `a3654a89c3babca4fdbb3db364de238be117e244aad8c40f597bf07d8b5fada2`.

| First-recovery failure | Exact failure boundary | Correct interpretation |
|---|---|---|
| Agent Memory / 6, Closing the Consistency Gap, `doi:10.48550/arxiv.2609.08832` | The verifier returned provider `finish_reason=error` after nine candidate claims passed reference processing. | Genuine technical failure; there is no scientific verdict to salvage. |
| Agent Memory / 7, CreaMem, `doi:10.48550/arxiv.2609.08550` | An optional artifact item had no evidence IDs and withheld all twelve candidates. | Reject the unsupported item; valid independent claims must remain assessable. |
| Deep Research / 7, quantum theorem benchmark, `openalex:W7171268496` | An optional absence claim had no evidence IDs and withheld all nine candidates. | Claim-level rejection, not proof of artifact absence or paper-level infrastructure failure. |
| Deep Research / 10, AREX, `openalex:W7171268386` | A homepage ending `/` joined the following `Models:` line; all three claimed links actually occurred in B0003. | Deterministic URL-boundary failure, distinct from the paper's scientific quality. |

Additional concrete cases were inventoried: LegalCiteTrust's `tongyi.aliyun.\ncom/farui/home` was shortened into a false partial URL; glued `FCARwas0%`, `was40.5%atColdstartand44.2%`, `to57.7%`, `of60–76%`, and `and15–62%` hid real numeric support; graph-memory and New Paradigm explanations imported facts from blocks outside their own citations; a matched-intent explanation was assessed as a source claim despite being an inference. Earlier locator/list-label, `a10-user`, and MemForest surrogate cases remain fixtures. Missing metrics, absent parameters, uncited comparisons and genuinely broad claims are not classified as harmless formatting problems.

## Evidence architecture

Canonical blocks remain the source of truth. `typed-evidence-v1` derives text-span, URL and numeric-quantity atoms with original text, comparison representation, raw offsets, block ID/hash, manuscript hash, context ID/hash/version, pages, sections and source spans. Comparison normalization does not overwrite source text.

URLs use deterministic extraction and source membership. Prose delimiters are separated from balanced URL path parentheses, query characters and structural line-wrap continuation. The AREX `Models:` line is not a URL continuation; the LegalCiteTrust hostname/path continuation is. A verified source URL supports an attributed artifact-availability fact only. It neither proves that the endpoint works nor satisfies a scientific gate dimension or reproducibility judgment. Abstract/front-matter artifact eligibility does not weaken scientific method/evaluation restrictions.

Numeric atoms normalize equivalent percentage spellings and spacing, preserve percentages versus percentage points, and handle explicit units at glued OCR boundaries and range endpoints. They do not infer decimal-to-percent conversions. Deterministic presence is a necessary screen; the semantic verifier still checks metric, entity, task/dataset, direction, denominator, comparison and relative-versus-absolute meaning against the exact cited context. A matching number alone cannot establish a scientific assertion.

`isolated-claim-support-v3` supplies each scientific claim and its separately checked explanation only the exact source set assigned to that item. Items may share a request only when their source sets are identical. Explanations are scoped assessor inferences; prose verification returns compact supported/unsupported/uncertain decisions. Narrative verification uses the eligible scientific source union, excluding artifact-only facts. No hidden reasoning is requested or retained. At most twelve scientific source groups plus one narrative group are allowed, with no verifier retries.

`claim-rejection-v2` separates unsupported or ineligible individual items from corrupted machinery. Empty citations, invalid URL facts and unsuitable optional evidence are rejected while remaining valid claims continue. Unknown evidence IDs, broken provenance/context mapping, verifier/provider failure and unprocessable responses remain technical outcomes. Evidence-eligibility exceptions are typed separately from corruption errors. Rejected optional items no longer veto an otherwise complete assessment.

Passing still requires positive grounded evidence across all six existing gate dimensions, adequate confidence and a supported narrative. Losing a required dimension yields uncertainty, not an optimistic replacement claim. `insufficient` requires a manuscript-grounded scientific concern; infrastructure failure cannot directly produce it. The scientific rubric, gate, discovery, relevance, ranking, affiliation/publication policies, roster and admission rule are unchanged: high relevance AND quality pass AND not suppressed.

Existing small adjacent evidence windows are retained without expansion; only supplied, contiguous, same-section neighbors can be used. The inventory did not justify a new broad-window mechanism. Canonical Unicode normalization and explicit UTF-8 boundaries are retained through text, hashes, requests, JSON, persistence and generated output, including the representative scientific-symbol round-trip regression. No paper-specific prose-rule table was added; the former expanding `scope_issues` table was removed.

## Engineering review and merge

[PR #33](https://github.com/vernerisirva/agentmempaper/pull/33), branch `simplify-quality-evidence-model`, merged as `f073e7f94e84269c8b6834bdf9f8e29864c0d61d`. The final reviewed candidate was `d009f10400a86ea860e2cd628c4e423a14d38783`. [Exact-candidate CI](https://github.com/vernerisirva/agentmempaper/actions/runs/35216987733) and 337 offline tests passed before reassessment. The merge gate recorded PASS_WITH_NOTES, zero unresolved blockers, a mergeable PR and no material unreviewed changes.

| Independent reviewer | Result | Reported cost |
|---|---|---:|
| DeepSeek v4 Pro | No verdict within the bounded 360-second review window; charge unknown | Unknown; $0.411100800 retained as a reserve |
| Claude Opus 4.6, complete review 1 | PASS_WITH_NOTES | $0.238730000 |
| Claude Opus 4.6, complete review 2 | PASS_WITH_NOTES on final candidate | $0.207090000 |

The established escalation was used once DeepSeek failed to return a bounded verdict. The first Opus pass covered production code and actual-source fixtures; the second covered all executable code and tests, with only unchanged fixtures omitted by the total collector limit. Both used the existing reviewer schema and request ceiling. The diagnostic for fixture-pool exhaustion was clarified, and the maximum-thirteen-verifier regression was added. A final note claiming `SequenceHttp` lacked `verifier_payloads` was disproved by its existing initializer and passing tests. No valid blocker was bypassed.

Automatic approval initially rejected exporting potentially private source to DeepSeek. The repository was verified public, the authorized branch was pushed, and the collector was inspected to contain only public source/README diff, with no runtime data, secrets or environment values; the same review then received approval. This did not require or cause assessment-data export.

## Frozen execution

The merged evaluator above was frozen with all evaluator/configuration hashes before the first call. Assessment version is `quality-batch2-recovery-v2`; assessor and verifier are `deepseek/deepseek-v4-pro-0813`, reasoning disabled, temperature zero, no fixed seed. The same source candidates and candidate-record hashes were enforced, with two track workers, one initial plus at most one assessment retry, and at most thirteen verifier requests per paper. Output caps are 8192 assessment / 4096 verifier tokens. Request caps are 300,000 / 250,000 serialized UTF-8 bytes. There were no selective reruns or evaluator changes during execution.

Outcomes were frozen at **2026-09-17T12:13:44.824631+00:00** before the observational audit. All twenty entries completed and the evaluator/configuration/roster hashes remained unchanged.

## Three-execution results

**Recovery v2: 0 passes, 10 scientific uncertainties, 0 scientific insufficiencies, 6 unavailable manuscripts and 4 technical failures.** The four technical outcomes are two verifier schema failures, one request-preflight failure and one disputed text-coverage classification. The latter is the automatic stored category, not an audit-confirmed extraction failure.

| Outcome | Original | Recovery v1 | V2 Agent Memory | V2 Deep Research | V2 overall |
|---|---:|---:|---:|---:|---:|
| quality_pass | 0 | 0 | 0 | 0 | 0 |
| scientific_uncertainty | 8 | 10 | 6 | 4 | 10 |
| scientific_insufficient | 0 | 0 | 0 | 0 | 0 |
| manuscript_unavailable | 7 | 6 | 1 | 5 | 6 |
| evidence_grounding_failure | 4 | 3 | 0 | 0 | 0 |
| model_protocol_failure | 0 | 1 | 2 | 1 | 3 |
| text_coverage_failure | 0 | 0 | 1 | 0 | 1 |
| other_technical_failure | 1 | 0 | 0 | 0 | 0 |

Technical outcomes are 3/10 Agent Memory, 1/10 Deep Research, 4/20 overall. Engram has no selected papers and no defined rate. The protocol-failure bucket includes the pre-HTTP request failure; it does not imply a provider was called.

The following table preserves every paper and all three outcomes. `U` = scientific uncertainty, `M` = manuscript unavailable, `G` = grounding failure, `P` = protocol/verification failure, `C` = coverage failure, `T` = other technical failure. Claim counts are accepted/nonaccepted in original → v1 → v2 order. Nonaccepted includes technical withholding; it must not be equated with a scientific refutation.

| Track / position | Paper and canonical ID | Original → v1 → v2 | Claims A/N: original → v1 → v2 | Explanation of changes |
|---|---|---|---|---|
| agent_memory / 1 | MBM-0: Memory Birth Metrics v0 · `doi:10.5281/zenodo.22671447` | M → M → M | 0/0 → 0/0 → 0/0 | Unchanged: no known manuscript URL in any execution. Metadata metrics do not establish scientific quality. |
| agent_memory / 2 | Beyond Agent Harnesses: Cross-Substrate Authority for Multi-Agent Systems · `doi:10.48550/arxiv.2609.08472` | U → U → U | 6/4 → 4/7 → 8/3 | Uncertain in all runs. Eight claims now survive, including the matched-intent inference previously rejected because of its label. The narrative and alignment item remain unresolved; B0029 contains much of the claimed table chain, so the verifier objection is partly conservative. |
| agent_memory / 3 | Personalizing LLM Agent Memory Using Biometrics · `doi:10.48550/arxiv.2609.08558` | U → U → U | 6/2 → 7/2 → 4/4 | Uncertain in all runs. The 10-user protocol remains accepted. Benchmark names imported from other blocks, missing K=10, and a manuscript-wide absence claim are properly withheld. Plural table locators are still counted as measurements; the missing 5.24 cell lies outside the selected table fragments. |
| agent_memory / 4 | MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging · `doi:10.48550/arxiv.2609.08273` | T → U → U | 0/0 → 3/8 → 6/3 | Original Unicode failure became uncertainty in v1 and remains uncertainty. Six claims now survive, including the source URL, method and scoped compression limitation. Missing baseline rows genuinely limit two comparisons, while treating Tables 3 and 4 as quantities falsely rejects the ablation item. |
| agent_memory / 5 | What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory · `doi:10.48550/arxiv.2609.08279` | U → U → P | 8/1 → 8/2 → 0/11 | Both earlier scientific uncertainties become a verifier protocol failure. A 284-character reason violates the 280-character response schema after nine successful verifier calls; all eleven claims are withheld. This is a technical regression, not a scientific downgrade. |
| agent_memory / 6 | Closing the Consistency Gap: Self-Evolving Agents That Learn to Stay on Course · `doi:10.48550/arxiv.2609.08832` | G → P → U | 0/8 → 0/9 → 6/3 | Original abstract-link grounding failure and v1 provider error no longer block assessment. Six of nine claims survive. The no-Mean@5-degradation generalization is correctly rejected against a hard-task regression; AUROC0.699 is wrongly missed by numeric extraction. |
| agent_memory / 7 | CreaMem: A Scene-Aware Memory Architecture for Personalized Agents · `doi:10.48550/arxiv.2609.08550` | U → G → U | 6/3 → 0/12 → 7/2 | The v1 citationless optional-item failure becomes scientific uncertainty, with seven accepted and two rejected claims. Missing local backbone/related-work details remain. The narrative verifier incorrectly objects to BertScore leadership; the table supports the listed accuracy-metric leads. Broad all-metrics wording should be read as those named accuracy metrics, not token efficiency. |
| agent_memory / 8 | Graph-Based Personalized Memory for LLM Agents: Representation, Evolution, Retrieval, and Evaluation · `doi:10.48550/arxiv.2609.08599` | U → U → C | 9/0 → 9/0 → 0/9 | Both earlier uncertainties become text_coverage_failure. All eight pages were extracted, with no omitted body characters; the assessor treats absence of a survey search protocol as missing input and semantic verification is skipped. This taxonomy is not justified by extraction metadata and is retained unchanged as a failed run outcome. |
| agent_memory / 9 | MeClear: Cooperative Game-Theoretic Attribution and Risk-Aware Memory Clearance for Long-Horizon LLM Agents · `doi:10.48550/arxiv.2609.09115` | G → U → P | 0/9 → 4/5 → 0/12 | Original artifact eligibility failure became uncertainty in v1, then verifier protocol failure in v2. A 286-character reason exceeds the 280-character schema after six successful verifier calls; twelve claims are withheld. No scientific downgrade is inferred. |
| agent_memory / 10 | Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems · `doi:10.48550/arxiv.2609.08258` | G → U → U | 0/9 → 4/5 → 6/3 | Original abstract-link failure remains resolved. Six claims now survive versus four in v1. Method and guard-release assertions still cite incomplete sources; scoped limitations and main result counts survive. Uncertainty concerns the proposed evidence mapping, not proof the study is scientifically inadequate. |
| deep_research / 1 | A New Paradigm: Agentic AI for Scientific Discovery · `doi:10.65649/ukh4n33x` | U → U → P | 7/2 → 5/4 → 0/0 | Both earlier uncertainties become an operator request-preflight failure. The reconstructed payload is 360598 bytes, exceeding the declared 300000-byte limit before any HTTP call. The v1 payload was already 360360 bytes; v2 newly enforces that limit. No scientific judgment was produced. |
| deep_research / 2 | A PRISMA-Aligned Agentic Framework for Medical Systematic Reviews and Evidence Synthesis · `doi:10.64898/2026.07.30.26359375` | M → M → M | 0/0 → 0/0 → 0/0 | Unchanged manuscript unavailable: no known manuscript source URL; no scientific decision. |
| deep_research / 3 | Towards Reliable AI Scientists · `doi:10.6082/gep96-ycs43` | M → M → M | 0/0 → 0/0 → 0/0 | Unchanged manuscript unavailable: no known manuscript source URL; no scientific decision. |
| deep_research / 4 | Deep Research Agent: An AI-Powered System for Automated Research Paper Analysis and Citation-Based Answer Generation · `doi:10.65890/race.v2i2.204` | M → M → M | 0/0 → 0/0 → 0/0 | Unchanged manuscript unavailable: no known manuscript source URL; no scientific decision. |
| deep_research / 5 | When the Instrument Studies Itself: A Systematic Map of Autonomous AI Research Systems (2024-2026), Conducted by a Frontier Language Model · `doi:10.5281/zenodo.21577092` | M → M → M | 0/0 → 0/0 → 0/0 | Unchanged manuscript unavailable: no known manuscript source URL; no scientific decision. |
| deep_research / 6 | AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping · `doi:10.5281/zenodo.21523008` | M → M → M | 0/0 → 0/0 → 0/0 | Unchanged manuscript unavailable: no known manuscript source URL; no scientific decision. |
| deep_research / 7 | Benchmarking Agents for Proving Theorems in Quantum Algorithms and Quantum Information · `openalex:W7171268496` | M → G → U | 0/0 → 0/9 → 9/2 | The same URL became available in v1, whose citationless absence item blocked the assessment. V2 completes with nine accepted and two rejected claims. Single recorded runs, unmatched access conditions and targeted rather than universal semantic audits support caution; there is no invented artifact-absence conclusion. |
| deep_research / 8 | Is Deep Research Reliable? Misleading Knowledge Induces False Conclusions · `openalex:W7171268620` | G → U → U | 0/9 → 7/5 → 8/2 | Original artifact failure remains resolved. The previously false-rejected 0% control is now accepted. Two real percentage-point statements still fail at glued/shared-unit or hyphenated-unit boundaries; additional uncited judge/statistical claims keep the narrative unresolved. |
| deep_research / 9 | LegalCiteTrust: Benchmarking Citation Trustworthiness in Chinese Long-Form Legal Research Reports · `doi:10.48550/arxiv.2607.20872` | U → U → U | 10/1 → 10/1 → 9/3 | Uncertain in all runs. The split URL extracts correctly offline and no shortened URL is accepted in v2. Nine claims survive. Some missing scoring details are genuine local citation gaps; the 0.5 multiplication coefficients are falsely mismatched as units. The proposed final-score wording also omits parentheses, so the whole item is not certified correct by finding that numeric false rejection. |
| deep_research / 10 | AREX: Towards a Recursively Self-Improving Agent for Deep Research · `openalex:W7171268386` | U → G → U | 8/1 → 0/11 → 4/5 | V1 URL-boundary grounding failure becomes scientific uncertainty. All three source links are accepted as narrow artifact facts. Four claims survive; unrelated ablation/training details and broad absence claims are rejected. The exact 82.5/22.9-point result and bounded inference in B0061 are excessively conservatively rejected. |

All three full claim lists and their citations are preserved in the ignored operator `comparison.json`; the tracked structured report records every v2 item disposition and ID. Wording and outcome changes are not isolated causal estimates of engineering: prompts/support versions and stochastic proposals differ, even at temperature zero. There is no desired pass rate.

## Same frozen scientific audit

The original predefined positions 1, 6 and 10 in both populated tracks were audited after freezing all twenty outcomes. All accepted and rejected items in those packets were checked against their assigned canonical text; additional checks cover the inventoried defect families and remaining technical outcomes. No output was repaired. The all-pass and all-insufficient sets are both empty; that provides no positive evidence of calibrated selectivity.

### agent_memory / 1: MBM-0: Memory Birth Metrics v0

Automatic outcome: `manuscript_unavailable`; 0 accepted, 0 rejected/withheld.

- **Fit:** Direct agent-memory measurement relevance.
- **Evidence and decision:** No known manuscript URL, no manuscript-grounded accepted claims; unavailable is appropriate.
- **Scope:** The metadata description is not promoted into a quality judgment.
- **Limitations:** Metrics, controls and empirical adequacy cannot be audited from the abstract.
- **Conservatism:** Acquisition limitation, not an evidence-validator false rejection.
- **Confidence:** No pass or completed scientific judgment.

### agent_memory / 6: Closing the Consistency Gap: Self-Evolving Agents That Learn to Stay on Course

Automatic outcome: `scientific_uncertainty`; 6 accepted, 3 rejected/withheld.

- **Fit:** Relevant to consistent self-evolving agents and episodic guidelines.
- **Evidence and decision:** Six of nine claims survive: contribution, empirical gap, related-work positioning, limitations, artifact and presentation. The required method/evaluation/alignment support is incomplete. Full manuscript and exact IDs/hashes are preserved.
- **Scope:** B0031 supports no Mean@5 degradation for same-task evaluation; B0034 reports -0.8 percentage points on hard similar tasks. Rejecting the broad no-degradation claim is correct. The repository is only an attributed link fact.
- **Limitations:** B0043 explicitly covers platform nondeterminism, confidently wrong decisions and roughly 30x token cost.
- **Conservatism:** Confirmed: evidence-4 cites B0036, which explicitly states AUROC0.699 on 50 tasks, but the bare-number extractor misses 0.699. N=30 and temperature0.5 are also present in B0030 yet falsely missed; the wider method claim separately overreaches about cosine scoring.
- **Confidence:** No false pass. The uncertainty mixes real scope problems with deterministic numeric false rejection and cannot be called purely scientific.

### agent_memory / 10: Revoked but Still Authoritative: An Empirical Study of Revocation Enforcement in Agent-Memory Systems

Automatic outcome: `scientific_uncertainty`; 6 accepted, 3 rejected/withheld.

- **Fit:** Direct knowledge-supersession/revocation evaluation relevance.
- **Evidence and decision:** Six of nine claims survive. Exact sources support 44.2% and 42.1% unsafe-action rates, 0/1620 under filtering, the matched-pair comparisons, related-work positioning, code-link fact and explicit limitations.
- **Scope:** The six-defense count exists elsewhere but not in the method item citations. Guard placement/code release are likewise absent from their assigned blocks. Rejection of those complete compound claims is defensible. Prior-work novelty remains manuscript-attributed, not independently proven.
- **Limitations:** B0045 says the rule/no-rule scenario groups are not controlled; B0069 bounds the matched-pair test power and explicitly disclaims identity of the systems.
- **Conservatism:** The surviving audit is mainly constrained by the assessor citation choices. Better source selection might permit a fuller judgment; the present uncertainty does not show the underlying study is weak.
- **Confidence:** No pass. Accepted result claims are bounded by the described direct-insertion setup and should not be generalized to every deployment.

### deep_research / 1: A New Paradigm: Agentic AI for Scientific Discovery

Automatic outcome: `model_protocol_failure`; 0 accepted, 0 rejected/withheld.

- **Fit:** Direct conceptual synthesis of agentic scientific discovery.
- **Evidence and decision:** All 45 pages were acquired; 155031 body characters were retained. The 360598-byte serialized request exceeds the frozen 300000-byte cap. The observer raises AssertionError before HTTP; zero verified claims and zero provider charge for this entry.
- **Scope:** The prior accepted explanation overreach cannot be reevaluated in a completed v2 assessment. Nine retained deterministic fallback signals have no semantic acceptance and are not counted as accepted claims.
- **Limitations:** No v2 scientific conclusion about the conceptual review is established.
- **Conservatism:** Confirmed infrastructure limit; the previous payload was already 360360 bytes. This is not manuscript unavailability or scientific uncertainty.
- **Confidence:** No pass, and the stored protocol-failure outcome is retained. The generic technical rationale must not be interpreted as a scientific critique.

### deep_research / 6: AutoResearch: A Multi-Agent AI System for Automated Literature Review, Paper Summarization, and Citation Mapping

Automatic outcome: `manuscript_unavailable`; 0 accepted, 0 rejected/withheld.

- **Fit:** Direct multi-agent literature-review use case.
- **Evidence and decision:** No known manuscript URL; unavailable remains appropriate and no manuscript-grounded claim is admitted.
- **Scope:** Abstract architecture and promised evaluation are not treated as validated results.
- **Limitations:** No full methods/results available for quality judgment.
- **Conservatism:** Acquisition limitation, not validator conservatism.
- **Confidence:** No pass or inferred scientific insufficiency.

### deep_research / 10: AREX: Towards a Recursively Self-Improving Agent for Deep Research

Automatic outcome: `scientific_uncertainty`; 4 accepted, 5 rejected/withheld.

- **Fit:** Direct recursively improving deep-research agent relevance.
- **Evidence and decision:** Four of nine items survive: contribution, related work, artifact availability and metric presentation. Exact B0003 now yields all three correct links, including the homepage trailing slash.
- **Scope:** Rejection of an explanation importing later ablations into B0006-B0007 is correct. B0070-B0071 cannot establish manuscript-wide absence of limitations. The public display does not claim that the linked artifacts work or reproduce results.
- **Limitations:** No adequately supported limitations criterion survives. Incomplete table/recipe citations weaken the proposed method/evaluation items.
- **Conservatism:** Confirmed semantic false negative: B0061 explicitly states AREX improves with another recursive round and gives 82.5 accuracy, 22.9 points above neither component. The verifier nevertheless rejects the bounded alignment inference as not stated.
- **Confidence:** No false pass. The uncertainty includes real citation gaps and verifier conservatism; it is not a clean scientific-quality conclusion.

## Residual defects and successful boundaries

- **URLs:** AREX B0003 now yields the app, trailing-slash homepage and model collection as three distinct links, and the live artifact item is accepted. The original LegalCiteTrust B0025 split hostname normalizes to the full `https://tongyi.aliyun.com/farui/home`; no shortened link is accepted in v2. These are source-presence facts, not independent checks of artifact functionality. No Abstract scientific eligibility was relaxed.
- **Numeric false rejection remains:** Closing B0036 contains `AUROC0.699` and 50 tasks but evidence-4 is rejected for missing 0.699. B0030 contains `N= 30at temperature0.5`; both quantities are falsely missed, although that compound method claim also imports uncited cosine-scoring detail. MemForest B0042/B0047 contain the cited ablation tables, but the phrase `Tables 3 and 4` in its explanation becomes a pair of required quantities even though source-side table labels are ignored. These are representation failures.
- **Percentage-point boundaries remain:** Is Deep Research Reliable B0030 explicitly gives 45.0 and 41.3 percentage points, but the glued first value is missed. B0033 gives a 23.5-percentage-point gap with a line-wrapped unit; both the value and unit are falsely rejected. The earlier exact percent/range fixtures now pass, and the live 0% control in B0034 is accepted, but the defect family is not fully resolved.
- **Operators versus units:** LegalCiteTrust B0021 uses `0.5×` as an arithmetic coefficient; numeric matching treats the multiplication sign as a quantity unit and rejects the bare 0.5 coefficient. This does not certify the entire proposed formula: its wording also loses parentheses from `(Coverage + Support) × Trust`.
- **Semantic conservatism remains:** AREX B0061 explicitly links another recursive round to improvement and gives 82.5 accuracy / 22.9 points. The bounded alignment inference is still rejected. Beyond Agent Harnesses B0029 contains the three-experiment chain the verifier says is not shown; some stronger whole-paper wording remains broader than that fragment. CreaMem's narrative verifier incorrectly says BertScore is not best: Table 1 has CreaMem 85.30/85.36 against lower listed baselines. This is an inaccurate verifier objection, not a confirmed accepted accuracy overclaim. Other unsupported narrative assertions still make rejecting the complete narrative defensible.
- **Overreach is caught in concrete cases:** Closing's same-task no-degradation claim cannot be extended to similar-task Hard performance; AREX cannot cite introduction-only blocks to establish later ablations or conclusion-only blocks to establish manuscript-wide absence; biometrics and revocation items cannot import details from other citations. These fail at claim level. The two prior accepted-explanation leakage cases, New Paradigm and the graph survey, lack completed v2 semantic assessments, so this run cannot establish full empirical resolution of those cases.
- **Optional bad claims no longer poison reference validation:** CreaMem and the theorem benchmark now complete with surviving scientific claims. The explicit citationless-optional-item regression preserves a complete valid assessment, while a missing required dimension yields uncertainty. Their live proposals differ from v1, so this is recovery evidence rather than a clean one-factor causal test.

### Technical failures are not scientific verdicts

1. **New Paradigm:** 360,598 serialized request bytes exceed the frozen 300,000-byte ceiling. All other payload preflight conditions pass. An `AssertionError` occurs before budget reservation or HTTP, and the general assessor exception path stores `protocol_failure`. The first-recovery request was already 360,360 bytes; the new operator enforces the formerly unenforced declared ceiling. This is an operator/manifest preflight defect, not a model refusal, manuscript absence or scientific judgment. No request was replayed.
2. **What Eviction Destroys:** one verifier reason has 284 characters against a 280-character schema limit. Nine verifier calls had succeeded; the invalid response prevents an accepted verification result, withholding all eleven items. No verifier retry is authorized in the frozen protocol.
3. **MeClear:** the same schema-length failure occurs at 286 characters after six successful verifier calls, withholding twelve items. Both responses finish normally and contain parseable JSON; this is schema noncompliance, not truncated output or a transport timeout. Providers are NextBit and Phala respectively. Compact explanations should not be confused with scientific support failure.
4. **Graph-memory survey:** the assessor marks `text_coverage_failure` because it cannot find a dedicated survey selection protocol. All eight pages were extracted, no body characters were omitted, and no extraction gap/truncation is recorded. That supports a question about the paper's survey methodology, not the assertion that supplied input is incomplete. The early coverage branch skips verification and withholds nine items. The stored result is preserved without manually reclassifying it.

The post-run aggregation script initially tried to resolve unverified deterministic fallback signals on New Paradigm as accepted block evidence. The reporting script was corrected to exclude those signals on technical outcomes; canonical context identities and all source hashes then passed. No evaluator, assessment row or public scientific claim was changed by that reporting correction.

## Reliability and cost

Fourteen manuscripts were acquired, all from cache, with no failed source attempt or alternate-source recovery. Six entries have no known source URL. All fourteen have full-text selection, zero omitted body characters and no extraction truncation. Thirteen actual initial assessment calls and zero retries were made; the oversized request was blocked before HTTP. There were 116 actual verifier calls and zero verifier retries.

Of 129 structured candidate items, **67 were accepted, 30 were rejected on completed scientific assessments, and 32 were withheld on technical outcomes** (11 + 9 + 12). The 24 deterministic/metadata fallback signals are not verified claims. Verifier item decisions total 194 supported, 44 uncertain and 6 unsupported, including explanations/narratives and intermediate decisions from failed overall verifications; these are not accepted-claim counts. Two verifier responses fail schema validation, and the graph survey skips verification for its coverage declaration. No source-ID/provenance grounding failure occurs.

Maximum observed request latency was 233.58 seconds; median was 4.44 seconds, with three calls over 180 seconds. The socket timeout is not a total request deadline. No extra operator retries or manual interventions occurred.

| Cost component | Calls | Input tokens | Output tokens | Reported USD |
|---|---:|---:|---:|---:|
| V2 initial assessment | 13 | 415,849 | 33,249 | $0.4902910478 |
| V2 assessment retry | 0 | 0 | 0 | $0.0000000000 |
| Support verifier | 116 | 286,148 | 17,152 | $0.3809451328 |
| Independent review — two completed Opus calls | 2 | 85,924 | 648 | $0.4458200000 |
| Independent review — timed-out DeepSeek call | 1 | Unknown | Unknown | Unknown; $0.4111008000 reserved |

V2 inference reported cost: **$0.8712361806**. V2 plus engineering review, known reported cost: **$1.3170561806**; including the unresolved review reserve: **$1.7281569806**. Missing usage is not zero and a reserve is not an invoice.

Including the previous recovery/reviews ($1.655694474), cumulative known recovery cost is **$2.9727506546**, or **$3.3838514546 charged or reserved**, within the established shared $10 ceiling. The original Batch-2 inference ($0.715272136) is outside that recovery ledger and remains separately reported; all three executions plus recovery reviews total $3.6880227906 known, plus the same unresolved reserve.

## Validation, history and publication

All 337 offline tests passed. All three relevance evaluations, all three quality evaluations, discovery validation, idempotency and offline site builds passed. Sidecar schemas, links, exposure scans, workflow/YAML checks, generated-file sizes and `git diff --check` passed. Three-database snapshot/restore and legacy two-database restore matched. All 618 frozen-run assessments remain readable; the reconciled runtime additionally preserves ten concurrent scheduled assessments (628 total). 397 accepted source blocks with explicit roles passed hash/eligibility checks.

All 598 prior assessment rows, the original 28 calibration outcomes, original Batch-2 outcomes, first recovery outcomes, original report/manifest hashes, non-roster current decisions and unrelated runtime tables are preserved. Twenty v2 rows were appended. The site audit verifies all 20 current Batch-2 cards against stored outcomes and all 28 calibration cards unchanged in scientific quality/admission. Main-library counts remain 4 / 5 / 6, with no visibility discrepancy. No public card was manually corrected.

The ignored `data/cache/operator/batch-2-recovery-v2-20260917/` directory retains the frozen protocol, raw/normalized evidence inventory, request/response artifacts without hidden reasoning, extracted documents, canonical contexts, typed-atom audits, saved rows, all three claim comparisons, costs, diagnostics, operator scripts and validation/publication hashes. Earlier operator directories remain separate. No database, PDF, secret or raw response envelope is committed.

A delayed pre-existing scheduled [daily run](https://github.com/vernerisirva/agentmempaper/actions/runs/35217328457) started during recovery and committed generated outputs at `86f04aef021343da4b4ae71246ad6039819bbb13`. Its ten new assessments are deterministic, outside this frozen experiment, and not Batch 3. It also deployed Pages independently. The publication guard detected its newer runtime asset and stopped before any overwrite. Append-only reconciliation preserved all scheduled rows and other tables, then appended the exact twenty frozen payloads with a recorded row-ID mapping. The evaluator, evidence, decisions and costs were not changed; no new model call occurred. Combined history is 328 / 252 / 48 rows, 628 total. Site and snapshot/legacy validation were repeated after reconciliation. The recovery publication below is the sole Pages dispatch issued by this task, distinct from that scheduled deployment.

Runtime snapshot SHA-256: `bb1505870d8901a18618308c5a701b099c2df778a100bb4e966b44aaee65fde7`.

The existing runtime release asset was uploaded once, redownloaded, restored and verified against archive and database hashes.

Pages deployed **once** via [run 35221878575](https://github.com/vernerisirva/agentmempaper/actions/runs/35221878575) at `6c299f4c4a812606ec29fee126113d559eff1d41`, with `deploy_only=true`. Acquisition, discovery, inference and runtime-mutating workflow steps were verified skipped.

All 48 Batch-2/calibration JSON cards, 48 HTML detail pages and six library/review pages match the validated local bytes.

## Recovery-v2 verdict and readiness

| Required criterion | Result |
|---|---|
| Known URL boundaries | PASS for exact fixtures; AREX live links accepted; LegalCiteTrust split hostname normalized correctly offline, no v2 partial link accepted. |
| Numeric false rejections resolved | FAIL: bare glued values, shared/hyphenated percentage-point units, plural table locators and multiplication coefficients still falsely fail. |
| Overbroad claims rejected | PARTIAL: observed overbroad no-degradation and manuscript-wide absence claims are rejected. The two prior accepted-explanation leakage cases lack completed v2 semantic assessments, so full empirical resolution is unestablished. |
| Bad claim does not automatically cause technical failure | PASS for observed independently rejected claims and deterministic optional-item regressions; CreaMem and theorem benchmark now complete scientifically. |
| Scientific uncertainty defensible without hidden engineering effects | FAIL: sampled Closing and AREX include confirmed false rejections; graph coverage classification is not supported by extraction metadata. |
| Every pass grounded | NO PASSES; audit set empty, not evidence of calibrated selectivity. |
| Insufficient remains scientific | NO INSUFFICIENT RESULTS; deterministic infrastructure/insufficient regressions pass. |
| Technical failures detectable | PARTIAL: protocol failures are visible and costed, but graph survey coverage failure confuses missing survey methodology with missing text. |
| No manual corrections | PASS: zero corrections, replacements or selective reruns. |
| Full validation | PASS: 337 tests and complete offline/site/history/snapshot checks. |
| Independent engineering review | PASS_WITH_NOTES; final code reviewed, exact-candidate CI green, zero unresolved blockers. |

Recovery-v2 fails because uncertainty still incorporates confirmed representation and semantic-verification errors, the coverage classification is unreliable, and known explanation-scope cases have not completed semantic reassessment. Passing engineering tests and review does not override the empirical failures. Future engineering must address these saved defects under a new reviewed protocol; this run is not repaired or selectively repeated. Batch 3 remains unstarted.

ORIGINAL_BATCH_2_GENERALIZATION_RESULT = FAIL
BATCH_2_RECOVERY_CHECK = FAIL
BATCH_2_RECOVERY_V2_CHECK: FAIL
QUALITY_PIPELINE_READY_FOR_BATCH_3: NO
