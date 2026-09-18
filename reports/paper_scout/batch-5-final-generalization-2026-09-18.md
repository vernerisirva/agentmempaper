# Batch 5 — final generalization evaluation and discrimination diagnostic — 2026-09-18

**The promotion gate demonstrated discriminative power for the first time. A blinded diagnostic on three historical non-pass papers withheld the weakest one on substantive grounds, and Batch 5 put ten unseen papers through the frozen gate with zero code changes, zero manual corrections and zero technical failures, promoting nine and withholding one on a verified internal contradiction in the manuscript. `BATCH_5_GENERALIZATION_RESULT = PASS`. Operational readiness stays **NO**: one unresolved false-promotion concern from the diagnostic, where the gate promoted a paper whose headline metric is produced by the same LLM judge it optimises against, with no external validation.**

## A. Canonical and frozen state

| Item | Value |
|---|---|
| `BATCH_5_CODE_SHA` | `3f65d27ba0e4b78c68f0f6bd1c1a99bad3d027a7` |
| Publication commit | `3f65d27ba` — "Publish the Batch-4 contract recovery" |
| PR #39 merge SHA | `8a99babed743f4ade2b23f8ac03b44a4283c6373` (present in history) |
| Working tree at start | clean, `main`, up to date with `origin/main` |
| Implementation changed during this task | **none** — `git status` over `paper_scout/`, `tests/`, `.github/`, `config/` is empty |

The host Xcode licence is still unaccepted, so `/usr/bin/git` exits 69 on every invocation. All Git work ran through a Homebrew Git PATH shim, including the unit suite, which shells out to `git init`. No host setting was changed.

### Credentials

```text
GEMINI_API_KEY:     AVAILABLE   (private interactive shell; not inherited by this session)
OPENROUTER_API_KEY: AVAILABLE   (private interactive shell; not inherited by this session)
```

Neither value was printed, echoed, hashed, partially revealed, stored or committed. Availability was checked only by testing whether the variable is non-empty. Every live call ran under `zsh -ic`, so the values resolve through the user's own shell and reach an HTTPS `Authorization` header only. No project-local secret file was created.

### Frozen model configuration, recorded not changed

| Role | Provider | Model | Credential |
|---|---|---|---|
| Primary assessor | google | `gemini-3.8-flash` | `GEMINI_API_KEY` |
| Independent adjudicator | openrouter | `deepseek/deepseek-v4-pro-0813` | `OPENROUTER_API_KEY` |

```text
GATE_VERSION        = dual-promotion-v2
ASSESSMENT_VERSION  = quality-promotion-v1
RUBRIC_VERSION      = scholarly-rubric-v1
EVIDENCE_VERSION    = block-evidence-v2
COVERAGE_GATE       = coverage-v2
RECEIPT_VERSION     = canonical-response-v1
MODEL_PAIR_VERSION  = model-pair-v1
RETRY_POLICY        = adjudicator-contract-retry-v2
```

The promotion rule is unchanged and was read from running code, not assumed:

```python
agreement = (primary.decision == 'pass' and adjudicator.promotion_decision == 'pass'
             and primary.evidence_ids and adjudicator.evidence_ids
             and not adjudicator.blocking_reasons)
```

combined with high relevance, deterministic provenance/integrity PASS, and not suppressed. **No rubric, prompt, model, threshold, evidence semantic or promotion rule was altered anywhere in this task.**

## B. Discrimination diagnostic

### B.1 Selection, frozen before any call

The persisted representation of a scientific outcome is `quality_status`; `uncertainty_reason` (`scientific_uncertainty` / `text_coverage_failure`) exists only in the live model schema and is **never** stored — verified by walking every one of the 657 payloads. The historical strata are therefore `quality_status = uncertain` (substantive uncertainty) and `quality_status = insufficient`, with technical failures separable by execution outcome.

Taking each paper's **final** historical assessment and excluding `dual-promotion-v2` rows (Batch 4 — already through the new gate), 54 papers have a historical non-pass outcome. The task's preference criteria — complete manuscript, coverage gate PASS, no known technical/input failure — pin the selection down completely, leaving **no selection freedom**:

| Stratum | Rule | Candidates | Selected |
|---|---|---:|---:|
| `scientific_uncertainty` | `uncertain` + coverage `complete` + coverage gate `pass` + execution `success` | exactly 2 | both |
| `insufficient` | final outcome `insufficient` | exactly 1 in the whole corpus | it |

No title, author, venue or expected behaviour entered the choice. The remaining 51 were excluded by their recorded technical status: 18 `manuscript_unavailable`, 3 `protocol_failure`, 1 `text_coverage_failure`, and 29 older rows with no execution receipt.

```text
DIAGNOSTIC_ROSTER_SHA256: eca0edf866dfb5a6af3224456b99399b6932fab18f654b6db15b7c5655108724
```

| # | Track | Canonical id | Title | Historical stratum | Historical gate |
|---|---|---|---|---|---|
| 1 | deep_research | `doi:10.48550/arxiv.2609.14709` | An immune world model for multiscale forecasting and therapeutic hypothesis generation | `uncertain` | dual-promotion-v1 |
| 2 | deep_research | `openalex:W7170112970` | PEARL: Auditable Repair for Scientific Reasoning Graph Extraction | `uncertain` | dual-promotion-v1 |
| 3 | agent_memory | `doi:10.5281/zenodo.22661593` | Human Supervision as Attractor Stabilization (HibriMind) | `insufficient` | scientific-gate-v1 |

**Disclosure.** Paper 1 was already run through the new pair in the bounded integration smoke recorded in the configuration report, where it returned `pass`/`pass`. Its diagnostic outcome is therefore a replication of a known result, not independent evidence. The deterministic selection rule produced it anyway and it was not substituted. Papers 2 and 3 were genuinely unseen by the new gate.

### B.2 Blinding

Verified in code, not assumed. `assess_promotion(candidate, selected, seed, mode, http)` receives the candidate, the selected manuscript text and a seed; the request payload is built from the manuscript-derived evidence context and coverage only. The adjudicator additionally receives the *current* primary output, which is the normal contract. The `get_current_quality_assessment` lookups in `quality_service` govern caching and force semantics only and never reach a prompt. **No historical outcome label, rationale, prior model judgment or promotion status can reach either model.**

### B.3 Isolation

Every diagnostic run executed against **copied databases** with both state *and* report output redirected through temporary configs, so neither a production row nor a committed report artifact was reachable.

```text
production DB SHA-256, before and after the diagnostic — byte-identical
2f0a79bb…19f  data/paper_scout.sqlite3
6243c6b2…bd1  data/deep_research/paper_scout.sqlite3
a04493c0…879  data/engram/paper_scout.sqlite3
git status --short: clean
```

Zero diagnostic rows reached production, confirmed again by row-level comparison after Batch 5 (§K).

### B.4 Current outcomes, frozen before revealing history

| # | Paper | Gemini | DeepSeek | Blockers | Promotion | Technical | Provenance |
|---|---|---|---|---:|---|---|---|
| 1 | Immune world model | `pass` | `pass` | 0 | **promoted** | success, 2 calls | pass |
| 2 | PEARL | `pass` | `pass` | 0 | **promoted** | success, 2 calls | pass |
| 3 | HibriMind | `uncertain` | `uncertain` | 4 | **not promoted** | success, 2 calls | pass |

Paper 3 required two runs, both recorded. Its stored `url` is a Zenodo DOI landing page, so default acquisition returned `manuscript_unavailable` with **zero model calls** — a pure execution-eligibility outcome carrying no scientific information. Its historical full-text assessments had all used an explicitly supplied PDF URL, so it was re-run with that same production `--pdf-url` mechanism, which is a documented CLI flag in the frozen code and changes manuscript acquisition only. Both attempts are reported; nothing was repaired, substituted or hidden.

Evidence provenance across all three: 168 context blocks, **0 unknown evidence ids, 0 excerpt mismatches**, every context hash binding to its assessment and manuscript, `validate_context` OK.

### B.5 Revealed comparison and audit

| Paper | Historical | Current | Reading |
|---|---|---|---|
| Immune world model | `uncertain` | promoted | requires audit |
| PEARL | `uncertain` | promoted | requires audit |
| HibriMind | `insufficient` | not promoted | **sensible** |

**HibriMind — correctly withheld, `DEFENSIBLE_NONPROMOTION`.** Both roles independently returned `uncertain`, and DeepSeek produced four concrete manuscript-grounded blockers: only conceptual definitions without formal grounding, algorithmic implementation or empirical validation; no experimental evaluation or formal analysis behind the central attractor-stabilization claims; broad security assertions supported only by narrative alignment with external literature; and no discussion of scalability, overhead or failure modes. Gemini independently described it as "an opinion or framework essay without verifiable empirical evidence". This is a genuine scientific withholding, not a technical artifact, and it is the **first direct evidence that the new gate can reject weak work**.

**Immune world model — `DEFENSIBLE_PROMOTION` with noted weaknesses.** The retired adjudicator's six blockers were checked individually against the manuscript. Two are real and verifiable: the headline forecasting result ties the trivial condition-mean baseline — the manuscript states plainly that the model "did not improve the global mean over the condition-mean baseline" — and the code, manifests and weights are future-tense ("A versioned software release **will** contain…"), so nothing is reproducible at submission time. Gemini saw the tie and reported it accurately as "matching condition-mean on global gene-delta cosine while showing per-action gains", treating author transparency plus real per-action results as sufficient. That is a defensible reviewer judgment, not an oversight. Several other historical blockers — "baselines dated 2026", "model versions that do not correspond to any publicly released version (DeepSeek V4, Claude S5, Gemini 3.6)" — are very likely **knowledge-cutoff artifacts of the retired `claude-sonnet-4.6` adjudicator**, since this project itself runs `deepseek-v4-pro-0813` and `gemini-3.8-flash`. The retired pair is therefore not a reliable gold standard, and some of its historical conservatism was spurious.

**PEARL — `FALSE_PROMOTION_CONCERN`.** The retired adjudicator's central objection is **confirmed verbatim in the manuscript**. PEARL's headline claim is that strict-gate passes rise from 0/350 to 300/350 and REA from 0.339 to 0.906. Those numbers are produced by an LLM judge under the CG/REA protocol — and the same protocol drives the repair loop: repairs are "judged again under the same CG/REA protocol". A search of the full manuscript for *human annotation*, *inter-annotator*, *held-out judge*, *judge reliability* and *calibration* returns **zero matches**, and the entire limitations section is one sentence ("PEARL targets the ARCHE Peircean SRGE schema and five text-only archives") which does not address the circularity. Gemini reported the numbers and the one-sentence scope note without noting that the evaluator is the optimisation target; DeepSeek passed with **zero** blocking reasons. The paper is not worthless — the contribution is real, the strict gate is conservative, ablations exist and code is released — but promoting a paper whose central metric is self-referential, with no external validation, is a genuine evaluation-adequacy miss for a conservative curated library.

### B.6 Verdict

The criterion is met: the gate did **not** blindly promote all three, at least one was correctly withheld on genuine scientific grounds, and one false-promotion concern on one paper out of two promotions — with a competing explanation for part of the retired pair's conservatism — is not an *obvious systematic* issue at n=3.

```text
DISCRIMINATION_DIAGNOSTIC: PASS
```

The PEARL concern is carried forward and weighed against operational readiness in §O. Mitigating evidence appears in Batch 5 (§G): the gate engaged with judge validity on **every** Batch-5 paper that uses an LLM judge, so the PEARL miss is not a blanket blind spot.

## C. Reproducible eligible population

Built with the canonical committed implementation from PR #39 (`paper_scout/batch_population.py`), pinned build time `2026-09-18T00:00:00+00:00`, with the Batch-2, Batch-3 and Batch-4 frozen rosters supplied as additional exclusion sources. No ad-hoc selection script was used and no scientific field was inspected during selection.

| Track | Ranked | Eligible | Excluded | Population SHA-256 |
|---|---:|---:|---:|---|
| agent_memory | 319 | 198 | 121 | `a133a32027fce6781cdd31ddb1d734e298a5462bee11d84d74164c6933ea4d40` |
| deep_research | 133 | 37 | 96 | `48b9c1a4ccf3db4de9edef3025207647abe82542be1b3cf49293a16a7e06a1ca` |
| engram | 8 | 0 | 8 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty-set digest) |

```text
BATCH_5_POPULATION_SHA256 (manifest): 8ffffc67e9324131d6ed0db47542f266fb8e7934f9ddc766741dd29c6869b262
```

Every excluded candidate records its reason, the matched identity and its source. Exclusions were read from all three tracks: agent_memory removed 120 by its own assessment rows and 1 by a deep_research row; deep_research removed 93 by its own, 2 by agent_memory rows and 1 by the Batch-3 frozen roster.

**Reconstruction reproduces exactly.** `batch-population --verify` rebuilt from the manifest's own recorded inputs:

```text
agent_memory  ordered_ids_match=True population_sha256_match=True stored=198 rebuilt=198
deep_research ordered_ids_match=True population_sha256_match=True stored=37  rebuilt=37
engram        ordered_ids_match=True population_sha256_match=True stored=0   rebuilt=0
self_consistent=True sources_match=True reproduced=True
stored=8ffffc67…262  rebuilt=8ffffc67…262
```

The one difference from the contract-recovery report's figures (deep_research 38 → 37) is fully accounted for: exactly one Batch-3 roster paper that never received an assessment row is now excluded by the supplied roster, which is strictly more conservative.

## D. Frozen Batch-5 roster

Execution eligibility consumed the frozen ordered list afterwards, as the module intends. The walk acquired manuscripts and applied the production coverage gate **read-only**, persisting nothing and making no model call.

| Track | Walked in rank order | Acquisition failed | Coverage gate PASS | Selected |
|---|---:|---:|---:|---:|
| agent_memory | 10 | 5 | 5 | 5 |
| deep_research | 18 | 13 | 5 | 5 |
| engram | 0 | 0 | 0 | 0 |

All 18 acquisition failures were Zenodo, ACM and Nature DOIs with no retrievable open manuscript, plus one arXiv 404 — the same pattern as Batch 4. **Engram has zero eligible papers, so zero Engram papers were used and no substitution was made across tracks.**

```text
BATCH_5_ROSTER_SHA256:       03f6b373cd2d62b2904229b0589e954826ffc9ebd860daac7d47987ff8719835
BATCH_5_AUDIT_SAMPLE_SHA256: 683717cd724f4ab731a5ed7185f470f976d3d19a3232d16bf23d899ac34c16d5
roster file SHA-256:         f5c7770e9f81d91151592a00123b9057e84bfcc5021f6dc005fb8d093536f0af
```

| # | Track | Rank | Canonical id | Title |
|---|---|---:|---|---|
| 1 | agent_memory | 6 | `doi:10.48550/arxiv.2609.01852` | The Memory Trust Gap: Capability-Dependent Failures in Persistent-Memory Agents |
| 2 | agent_memory | 7 | `doi:10.48550/arxiv.2609.00523` | Transferable End-to-End Optimization for Indirect Long-Term Memory Poisoning in LLM Agents |
| 3 | agent_memory | 8 | `doi:10.48550/arxiv.2609.01235` | MutMem-V2: Cryptographically Authorized Mutation in Persistent Agent Memory |
| 4 | agent_memory | 9 | `arxiv:2609.00859` | Reinforcement Learning Enhanced LLM Agents for Complex Vehicle Routing Problems |
| 5 | agent_memory | 10 | `arxiv:2608.30508` | UTILMEM: Benchmarking Evidence Utilization in Long-Term Conversational Memory |
| 1 | deep_research | 7 | `arxiv:2607.10127` | GAE: Graph-Augmented Evolution for Scientific Discovery via Reinforcement Optimization |
| 2 | deep_research | 9 | `openalex:W7168328747` | Toward Auditable AI Scientists: A Hypothesis Evolution Protocol for LLM Agents |
| 3 | deep_research | 12 | `arxiv:2607.04718` | FORGE: Research-Trajectory Hijacking Attacks on Deep Research Agents |
| 4 | deep_research | 13 | `arxiv:2607.04293` | CausalGame: Benchmarking Causal Thinking of LLM Agents in Games |
| 5 | deep_research | 18 | `arxiv:2607.00440` | Minos: A Multi-Agent Collaborative Framework for Provenance-Based Backward Tracking |

Track distribution 5 / 5 / 0, total 10 — the realistic maximum. **Every selected paper was verified never assessed and never adjudicated**, by expanding each to its full namespaced identity set (canonical, DOI, arXiv, OpenAlex, Semantic Scholar, URL-derived arXiv, normalized title) and counting matching rows across all three databases: **0 prior assessments and 0 prior adjudications for all ten.**

The roster was immutable from the first scientific call onward. No paper was substituted or replaced for a scientific outcome.

## E. Frozen audit sample

Frozen **before any outcome was observed**, by the protocol rule (positions 1, ⌊n/2⌋+1, n for n = 5):

| Track | Positions | Canonical ids |
|---|---|---|
| agent_memory | 1, 3, 5 | `doi:10.48550/arxiv.2609.01852`, `doi:10.48550/arxiv.2609.01235`, `arxiv:2608.30508` |
| deep_research | 1, 3, 5 | `arxiv:2607.10127`, `arxiv:2607.04718`, `arxiv:2607.00440` |

All promoted papers were additionally audited, so in practice all ten were audited.

## F. Per-paper results

| Paper | Title | Gemini | DeepSeek | Blockers | Promotion | Outcome/provenance | Calls |
|---|---|---|---|---:|---|---|---:|
| agent_memory #1 | The Memory Trust Gap | `pass` | `pass` | 0 | **promoted** | success/pass | 2 |
| agent_memory #2 | Transferable Memory Poisoning | `pass` | `pass` | 0 | **promoted** | success/pass | 2 |
| agent_memory #3 | MutMem-V2 | `pass` | `pass` | 0 | **promoted** | success/pass | 2 |
| agent_memory #4 | RL-Enhanced LLM Agents for VRP | `pass` | `pass` | 0 | **promoted** | success/pass | 2 |
| agent_memory #5 | UTILMEM | `pass` | `pass` | 0 | **promoted** | success/pass | 2 |
| deep_research #1 | GAE | `uncertain` | `uncertain` | 3 | **not promoted** | success/pass | 2 |
| deep_research #2 | Toward Auditable AI Scientists (HEP) | `pass` | `pass` | 0 | **promoted** | success/pass | 2 |
| deep_research #3 | FORGE | `pass` | `pass` | 0 | **promoted** | success/pass | 2 |
| deep_research #4 | CausalGame | `pass` | `pass` | 0 | **promoted** | success/pass | 2 |
| deep_research #5 | Minos | `pass` | `pass` | 0 | **promoted** | success/pass | 2 |

Every paper: coverage gate `pass`, assessment scope `full_text`, `provenance_status = pass`, receipt `canonical-response-v1` validating against the pinned model pair and both providers, assessor `gemini-3.8-flash`, gate `dual-promotion-v2`, **manuscript hash identical to the hash frozen in the roster (10/10)**. No hidden reasoning was requested, returned or persisted — `reasoning_tokens` is null or zero on every call.

**Promotions: 9 of 10. Retries: 0. Manual corrections: 0. Technical failures: 0.**

## G. Promotion audit

All nine promotions were audited observationally against the acquired manuscript. No stored result was modified.

**Evidence provenance, checked mechanically across all ten papers:** every evidence id cited by either role resolves to a real block of that paper's canonical context (**0 unknown ids across 1,065 context blocks**), every stored evidence excerpt is byte-identical to its canonical block (**0 mismatches**), each context hash equals the assessment's `source_content_hash` and the roster's frozen manuscript hash, all ten receipts revalidate, and all ten context ids are distinct. **No fabricated evidence and no cross-paper contamination.**

Specific factual claims were verified verbatim against the manuscripts: the Memory Trust Gap's bootstrap intervals, RGB/MisBench external benchmarks, Llama-3.2/3.1 family and 8B scaling; the poisoning paper's +19.1 pp figure, AgentEvals judge and human evaluation; MutMem-V2's 72 test vectors, 42/42 conformance corpus and canary testing; the VRP paper's 48 variants, OR-Tools/Gurobi and 62.50% vs 45.83% DRoC comparison; UTILMEM's Mem0/A-MEM/MemOS/EverMemOS systems and >0.84 judge agreement; FORGE's PoisonedRAG/AuthChain baselines, PRISM and RQA and the subtask-transplant design; CausalGame's 30 models and ICC(2,3); and Minos's 0.92 recall, 0.64 precision and DARPA TC/Aurora/OpTC datasets. **Every checked claim is present and correctly stated.**

One term was investigated and cleared: Gemini described an "ablation comparing base LLMs" for the HEP paper, which never uses the word *ablation*. The evidence blocks it cited contain a controlled comparison "when only the base LLM is changed (n=3 runs per LLM)" with hypothesis counts 14.7 → 6.7 → 4.0 and depths 4.7 → 1.7 → 0.7. The characterization is substantively correct, not a fabrication.

| Promotion | Classification | Note |
|---|---|---|
| agent_memory #1 | `DEFENSIBLE_PROMOTION` | Percentile and cluster bootstraps, external benchmarks, independent model family, framing/thinking-mode controls |
| agent_memory #2 | `DEFENSIBLE_PROMOTION` | Three frameworks, four memory systems, eight defenses, ablations, **judge validated against human evaluation** |
| agent_memory #3 | `DEFENSIBLE_PROMOTION` | Dual independent implementations, 72 vectors, 42/42 conformance; assessment itself records that V2 utility was not rerun and there is no third-party replication |
| agent_memory #4 | `DEFENSIBLE_PROMOTION` | 48 variants, two solvers, planner/module/composition ablations, verified SOTA comparison |
| agent_memory #5 | `DEFENSIBLE_PROMOTION` | Dual frontier judges with **verified inter-annotator agreement (Pearson/Spearman > 0.84)** and controlled distractor ablations |
| deep_research #2 | `DEFENSIBLE_PROMOTION` | Three materials-science tasks, controlled base-LLM comparison; limitations **explicitly flag single-agent self-assessment** |
| deep_research #3 | `DEFENSIBLE_PROMOTION` | Causal isolation via subtask transplant cleanly separates hijacking from retrieval volume; defenses benchmarked |
| deep_research #4 | `DEFENSIBLE_PROMOTION` | 30 models, repeated trials with CIs, non-LLM baselines, **ICC(2,3) inter-rater reliability**, failure-mode analysis |
| deep_research #5 | `DEFENSIBLE_PROMOTION` | Five established datasets, 14 scenarios, three baseline families, extensive component ablations |

**`FALSE_PROMOTION_CONCERN` in Batch 5: 0.**

**No prestige, institution or venue bias.** A scan of all ten assessments for reputation markers (university, institute, named labs, venues, "renowned", "top-tier", "affiliation") returned **zero** hits; the only match was the word "authors" in phrases like "the authors acknowledge", which reports author-stated limitations.

**Directly relevant to the diagnostic's open concern:** six of the ten Batch-5 assessments engage explicitly with judge validity — human-evaluation agreement, inter-annotator agreement, ICC, kappa, or self-assessment as a limitation — and the four that do not are papers with no LLM judge (cryptographic verification, solver success rates, bootstrap-based measurement, symbolic regression). The gate therefore engaged with judge validity **wherever a judge was used**, which is evidence against a systematic blind spot and narrows the PEARL miss to a single instance.

## H. Disagreement audit

**There were zero scientific disagreements.** Gemini and DeepSeek agreed on all ten papers: nine `pass`/`pass` and one `uncertain`/`uncertain`. The protocol's disagreement category (Gemini PASS + DeepSeek ≠ PASS) is empty, so it fails closed vacuously.

Unlike Batch 4, this unanimity is **not** uninformative: the pair agreed on a rejection as well as on promotions, and the rejection rests on three specific, verifiable blockers. Agreement here reflects a shared and correct reading of a weak paper, not an inability to diverge. That said, the adjudicator has still never overruled the primary, so the *independent-check* value of the second role remains untested after two batches.

## I. Non-promotion audit

The frozen audit sample contains exactly one non-promotion, `arxiv:2607.10127` (GAE).

**Classification: `DEFENSIBLE_NONPROMOTION`.** Both roles independently returned `uncertain`. DeepSeek's three blockers were each checked against the manuscript:

1. **Internal contradiction — confirmed verbatim.** The paper lists "structurally blind parent selection" as one of three bottlenecks it closes, and states "these components close three bottlenecks: reward sparsity, **uninformed parent selection**, and a static mutation operator". The method section states the opposite: "Parent selection is uniform over the elite archive **in all configurations and is unaffected by any of the three components**", and "a parent α is drawn uniformly at random from the current island; **the reinforcement-learning agent does not select parents**". The paper claims to solve a bottleneck its own method explicitly does not address.
2. **Narrow evaluation — confirmed.** A single synthetic nonlinear harmonic oscillator task from LLM-SRBench, 150 iterations, 1–3 runs, and the word *ablation* appears **zero** times in the manuscript.
3. **SOTA claim on a low-budget comparison — confirmed.** Few runs, no reported uncertainty or statistical testing, with higher-budget Table 1 numbers taken from prior work rather than a shared protocol.

This is a correct, well-evidenced, non-conservative rejection. It is neither `POSSIBLE_` nor `CLEAR_EXCESSIVE_CONSERVATISM`, and it is not a `TECHNICAL_ISSUE` — the gate ran to completion with `outcome = success` and `provenance_status = pass`.

## J. Discriminative-power analysis

| Metric | Batch 5 | Batch 4 |
|---|---:|---:|
| Gemini PASS rate | 9/10 (90%) | 10/10 (100%) |
| DeepSeek PASS rate | 9/10 (90%) | 10/10 (100%) |
| Promotion rate | 9/10 (90%) | 9/10 (90%) |
| Disagreement rate | 0/10 (0%) | 0/10 (0%) |
| Technical failure rate | 0/10 (0%) | 0/10 (0%) |
| Retries | 0 | 0 |
| Non-promotions that are genuine science | **1 of 1** | **0 of 1** (contract artifact) |

No target rate was enforced, and none should be. The material change from Batch 4 is qualitative: Batch 4's single non-promotion was a machinery defect, so the batch produced **no** evidence of rejection ability. Batch 5's non-promotion is a substantive, verifiable scientific rejection, and the diagnostic added a second one on a historically `insufficient` paper.

Across both exercises the gate scientifically evaluated **13 papers and withheld 2**, in both cases for reasons that hold up against the manuscript. Discriminative power is now **demonstrated rather than assumed** — but it is demonstrated on obviously weak work (an evidence-free framework essay; a paper contradicting itself). The unresolved question is calibration on *borderline* work, which is exactly where PEARL sits.

## K. Historical integrity

| Track | Assessments before | after | Δ | Papers | Suppressions |
|---|---:|---:|---:|---|---|
| agent_memory | 343 | 348 | +5 | 18,343 → 18,343 | 0 → 0 |
| deep_research | 266 | 271 | +5 | 2,395 → 2,395 | 0 → 0 |
| engram | 48 | 48 | +0 | 306 → 306 | 0 → 0 |
| **Total** | **657** | **667** | **+10** | | |

Verified by row-level comparison of every pre-existing row's id and payload digest:

- **pre-existing rows deleted or mutated: 0**
- **new rows: 10, every one a frozen Batch-5 roster paper; 0 outside the roster**
- **diagnostic canonical ids appearing as new production rows: none** — the diagnostic never entered production
- Batch-4 reports are byte-unchanged and `BATCH_4_GENERALIZATION_RESULT = FAIL` stands
- the Batch-4 contract recovery results are unchanged

## L. Technical reliability

- 10/10 papers completed with `outcome = success`, `provenance_status = pass`
- 0 adjudicator contract retries, 0 protocol failures, 0 malformed responses
- 10/10 manuscript hashes identical to the frozen roster — **no paper/manuscript mismapping**
- 10 distinct evidence-context ids — **no cross-paper evidence contamination**
- 0 unknown evidence ids and 0 excerpt mismatches over 1,065 context blocks
- 10/10 receipts revalidate; all 28 completed dual-promotion receipts in the corpus revalidate
- population manifest reproduces byte-identically
- no credential, thought signature or hidden-reasoning content persisted anywhere

No stop-rule condition was triggered at any point.

## M. Validation

| Check | Result |
|---|---|
| Unit suite | **444 tests, OK** |
| Relevance, all three tracks | precision 1.000, recall 1.000, 0 FP, 0 FN |
| Quality/promotion fixtures, all tracks | passed, 8/8, 0 failures |
| Discovery, all tracks | recall 1.000 (6/6, 4/4, 4/4) |
| Idempotency, all tracks | passed |
| Site builds | all three libraries built |
| Site/schema/link/exposure/workflow checks | **0 errors** |
| Snapshot/restore | three databases, `integrity_check = ok`, 348/271/48 |
| Legacy compatibility | **667/667 assessments parse**; 28/28 completed receipts revalidate |
| `git diff --check` | clean |
| Implementation source changed | **none** |

A secret scan over every changed tracked artifact matched only ordinary prose — "bearer of", and hyphenation artifacts such as "task-characterization" → "sk-characterization". **No credential, API key, authorization header, thought signature or hidden reasoning is present.**

Two deliberate deviations from a bare production invocation, both recorded rather than smoothed over: diagnostic runs used copied state and scratch report output; Batch-5 runs used **production state** with report output redirected to scratch, so that the committed `paper-quality-2026-09-18.md` — which holds the Batch-4 recovery record — was not overwritten ten times by single-paper reports. Neither redirection touches the gate.

Three papers outside the roster show substantive card changes. All three are **network date-enrichment refreshes** from `build-site` (publication date provenance upgraded from `semantic_scholar` to `crossref`), with **zero** quality or promotion fields touched. The remaining ~1,900 card diffs are the `generated_at` timestamp only.

## N. Cost

### Discrimination diagnostic

| Provider / model | Calls | Prompt | Completion | Total | Cost |
|---|---:|---:|---:|---:|---|
| google / `gemini-3.8-flash` | 3 | 53,783 | 2,492 | 56,275 | **UNKNOWN**, `covered_by_msc_allocation` |
| openrouter / `deepseek-v4-pro-0813` | 3 | 51,052 | 1,161 | 52,213 | **$0.05744500** |

### Batch 5

| Provider / model | Calls | Retries | Prompt | Completion | Total | Cost |
|---|---:|---:|---:|---:|---:|---|
| google / `gemini-3.8-flash` | 10 | 0 | 348,062 | 10,551 | 358,613 | **UNKNOWN**, `covered_by_msc_allocation` |
| openrouter / `deepseek-v4-pro-0813` | 10 | 0 | 322,873 | 4,479 | 327,352 | **$0.29838970** |

### Totals

| Item | Value |
|---|---|
| Batch-5 known money | $0.29838970 |
| Diagnostic known money | $0.05744500 |
| **Task total known money (OpenRouter only)** | **$0.35583470** |
| Pre-execution Batch-5 estimate | $0.35 (actual −14.7%) |
| Gemini | 401,845 in / 13,043 out — **monetary cost UNKNOWN / MSc allocation** |
| Cumulative against the $10 ceiling | $6.48473717 → **$6.84057187** (remaining $3.15942813) |

The Google endpoint reports no charge and this project has not established the allocation's effective rate. Usage is recorded in exact tokens; **no monetary amount is fabricated and Gemini is not assumed to be free.**

## O. Publication

Published: the three regenerated public libraries and their sidecar JSON/CSV, the Batch-5 population manifest, roster, digest file and cost estimate, and this report. All ten Batch-5 outcomes appear correctly in the public data, including the non-promotion rendered with its three blocking reasons. Pages deployment is a single build of all three libraries.

**Not published**, and remaining private local state: the assessment SQLite databases, runtime databases, snapshots and raw private model records — all covered by `.gitignore` (`data/*.sqlite3`, `data/**/*.sqlite3`, `data/cache/`). Verified local private snapshot with `integrity_check = ok` continues. Remote private durable state remains backlog. No credential was committed.

## Assessment of readiness

Batch 5 satisfies all twelve generalization criteria:

1. discrimination diagnostic passed — **yes**
2. population manifest reproduced exactly — **yes**
3. no systematic technical defect — **yes**
4. manual corrections = 0 — **yes**
5. every audited promotion scientifically defensible — **yes** (9/9)
6. no clear false promotion in Batch 5 — **yes** (0)
7. disagreements fail closed — **yes** (vacuously; the one rejection failed closed correctly)
8. no systematic unsupported-claim pattern — **yes**
9. no systematic extreme conservatism in the non-promotion audit — **yes**
10. provenance/receipt integrity sound — **yes**
11. historical state unchanged except Batch-5 appends — **yes**
12. full repository validation passes — **yes**

Operational readiness nonetheless remains **NO**, for one reason stated plainly: **the PEARL false-promotion concern from the diagnostic is unresolved.** The gate promoted a paper whose headline result is generated by the same LLM judge that drives its repair loop, with no human calibration, no inter-annotator agreement and no held-out judge — a self-referential evaluation that the retired adjudicator caught and that is verifiable directly from the manuscript. The mitigating evidence is real (the gate engaged with judge validity on every Batch-5 paper that used a judge), but one documented instance of promoting a self-validating result is exactly the failure mode a conservative curated library must not have, and the gate has now scientifically evaluated only 13 papers and withheld 2 — both obviously weak. Calibration on borderline work is unestablished.

Resolving it does not require changing the rubric. It requires evidence: a further unseen batch, or a targeted diagnostic stratum of papers whose weakness is methodological circularity rather than absent evidence, to establish whether PEARL was a single miss or a reproducible one.

---

```text
DISCRIMINATION_DIAGNOSTIC: PASS
BATCH_5_GENERALIZATION_RESULT: PASS
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
```

No recurring assessment was started. No Batch 6 was selected or run. The rubric was not altered.
