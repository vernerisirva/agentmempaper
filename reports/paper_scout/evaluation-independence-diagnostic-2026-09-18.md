# Evaluation-independence diagnostic — 2026-09-18

**A blinded, copied-state diagnostic put six already-seen historical papers, selected deterministically for evaluator/optimizer coupling, through the frozen Gemini + DeepSeek gate. The gate handled five of six correctly, including two papers with genuine evaluator dependence that it promoted on the strength of real independent validation. It failed the one paper in the set whose evaluation is clearly circular. PEARL was naturally selected, promoted again with zero blocking reasons, and the miss therefore replicates rather than resolves. `EVALUATION_INDEPENDENCE_DIAGNOSTIC = FAIL`. No implementation code, prompt, rubric, threshold, model or promotion semantic was changed, and production state is byte-identical.**

## A. Canonical state

| Item | Value |
|---|---|
| Branch | `main`, clean working tree, up to date with `origin/main` |
| `DIAGNOSTIC_CODE_SHA` | `b2bb86ca647c71fc6734813cf7f4eb54fdbee89d` |
| HEAD commit | `b2bb86ca6` — "Publish the Batch-5 final generalization evaluation" |
| `git status --short` at start and end | empty |
| Implementation changed | **none** — no file under `paper_scout/`, `tests/`, `config/` or `.github/` was modified |

`git fetch origin` / `git checkout main` / `git pull --ff-only origin main` reported **Already up to date**; HEAD is unchanged from the start of the task.

The host Xcode licence remains unaccepted, so `/usr/bin/git` exits 69. All Git work ran through a Homebrew Git PATH shim. That shim also shadows the project's Python, which produced a spurious 110-test/36-error run until the interpreter was named explicitly; the canonical suite was then run with the correct interpreter. No host setting was changed.

### Credentials

```text
GEMINI_API_KEY:     AVAILABLE   (private interactive shell; not inherited by this session)
OPENROUTER_API_KEY: AVAILABLE   (private interactive shell; not inherited by this session)
```

Neither value was printed, echoed, hashed, partially revealed, stored or committed; availability was tested only by checking that the variable is non-empty. Every live call ran under `zsh -ic`, so values resolve through the user's own shell and reach an HTTPS `Authorization` header only.

## B. Frozen model configuration — recorded, not changed

Read from running code (`paper_scout/promotion_protocol.py`), not assumed:

| Role | Provider | Model | Host | Credential |
|---|---|---|---|---|
| Primary assessor | google | `gemini-3.8-flash` | `generativelanguage.googleapis.com` | `GEMINI_API_KEY` |
| Independent adjudicator | openrouter | `deepseek/deepseek-v4-pro-0813` | `openrouter.ai` | `OPENROUTER_API_KEY` |

```text
GATE_VERSION        = dual-promotion-v2
ASSESSMENT_VERSION  = quality-promotion-v1
RUBRIC_VERSION      = scholarly-rubric-v1          (RUBRIC sha256 fd45081b…2fa8, 1360 chars)
RECEIPT_VERSION     = canonical-response-v1
MODEL_PAIR_VERSION  = model-pair-v1
RETRY_POLICY        = adjudicator-contract-retry-v2
COVERAGE_GATE       = coverage-v2
MAX_EVIDENCE_IDS    = 24
attempt limits      = primary 1, adjudicator 2; total request limit 3
generation          = temperature 0, max_output_tokens 4096, hidden reasoning disabled
```

Promotion rule, read from `promotion_protocol.agreement`:

```python
return (primary['decision'] == 'pass' and adjudicator['promotion_decision'] == 'pass'
        and bool(primary['evidence_ids']) and bool(adjudicator['evidence_ids'])
        and not adjudicator['blocking_reasons'])
```

combined with high relevance, deterministic provenance/integrity PASS, and not suppressed. Every value above is identical to the Batch-5 frozen state. **Nothing was configured, tuned or overridden.**

## C. Deterministic selection rule — frozen before any scan

The rule, including all term lists, was written to disk and hashed **before** the corpus was scanned, so the selection could not be tuned toward a wanted answer:

```text
RULE_SHA256: e9f5a1564a09b898b1223fc9a8c75940b2cba65484d98a8d48162fb859cec39f
rule_id:     evaluation-independence-selection-v1
```

| Step | Rule | Survivors |
|---|---|---:|
| S1 | Papers with ≥1 stored scientific assessment whose **latest** row has `quality_gate_version ≠ dual-promotion-v2`, and whose `source_content_hash` resolves to a locally cached manuscript | 52 |
| S2 | Collapse rows sharing one manuscript `content_hash`, keeping the lexicographically smallest `(track, canonical_id)` | 45 |
| S3 | Cached document `complete == true` **and** the production coverage gate re-run read-only returns `status = complete`, `scope = full_text` | 43 |
| S4 | Pattern filter: `A ≥ 1` **and** `K ≥ 1` | **17** |
| S5 | Rank by `D = A + K − C` descending, then `canonical_id` ascending; take the first 6 | 6 |

where, computed from **manuscript text only**:

- **A** = distinct JUDGE families matched anywhere (LLM-as-judge, automatic judge, model-based reward, self-evaluation, judge-generated labels, scored-by-model, named model as evaluator);
- **K** = distinct LOOP families matched **within ±400 characters of a JUDGE match** — the coupling signal (repair, refine/feedback, reward/RL, selection/filtering, critic/verifier, self-improvement, guided search);
- **C** = distinct VALIDATION families matched anywhere (human evaluation, inter-annotator, agreement statistics, human correlation, judge calibration, alternative/held-out judge, objective metric, external benchmark).

Counting **distinct families rather than raw hits** keeps the index from scaling with manuscript length.

**S1 excludes `dual-promotion-v2` rows deliberately**: those papers have already been through the current frozen gate, so re-running them cannot test it blind. This is the same exclusion the Batch-5 discrimination diagnostic used.

**Forbidden inputs, none of which were used:** historical quality outcome, promotion status, prior rationale or blocking reasons; author, institution or venue; and any manual addition or removal of a specific paper.

17 qualifying papers is comfortably above the §4 floor of 4, so the stop rule did not fire.

### Selected challenge set — frozen before any model call

```text
CHALLENGE_SET_SHA256: 547d380c66100129d210b5778ca31de827c0d74165e53656d90cf9e6dd224e99
```

| # | Track | Canonical id | Title | A | K | C | **D** |
|---|---|---|---|---:|---:|---:|---:|
| 1 | deep_research | `doi:10.65649/ukh4n33x` | A New Paradigm: Agentic AI for Scientific Discovery | 1 | 5 | 2 | **4** |
| 2 | deep_research | `openalex:W7170112970` | PEARL: Auditable Repair for Scientific Reasoning Graph Extraction | 2 | 3 | 1 | **4** |
| 3 | deep_research | `openalex:W7171268386` | AREX: Towards a Recursively Self-Improving Agent for Deep Research | 2 | 4 | 2 | **4** |
| 4 | agent_memory | `doi:10.48550/arxiv.2609.08832` | Closing the Consistency Gap: Self-Evolving Agents | 3 | 2 | 2 | **3** |
| 5 | deep_research | `openalex:W7171268620` | Is Deep Research Reliable? Misleading Knowledge Induces False Conclusions | 3 | 1 | 1 | **3** |
| 6 | deep_research | `openalex:W7213371831` | AppliedScientist: Automated Scientific Revision Through Iterative AI Reviewing | 4 | 2 | 3 | **3** |

**PEARL was selected naturally, at rank 2, by the frozen rule.** It was not added, promoted in the ranking, or substituted in. The next paper below the cut (rank 7, `arxiv:2608.23982`, D = 2) is separated by a clear index gap from the D = 3 tier, so the boundary is not a coin flip between rank 6 and rank 7 — though a set of 6 is a small sample and is treated as such throughout.

## D. Blinding — verified in code, not assumed

`assess_promotion(candidate, selected, seed, mode, http)` builds each request from manuscript-derived content only:

- **Primary payload** (`promotion_gate.request_payload`): `{canonical_id, source_content_hash, context_id, coverage, manuscript}` plus the frozen rubric instruction.
- **Adjudicator payload**: the same, plus `primary_final_assessment` — the *current* primary output, which is the ordinary production contract.

The three `get_current_quality_assessment` lookups in `quality_service.assess_and_store_candidate` govern caching and `--force` semantics only; each short-circuits to `_finalize_assessment(..., cache_hit=True)` and **never reaches a prompt**. With `--force` all three are bypassed.

**No historical quality label, promotion status, prior assessor rationale, prior adjudicator rationale, or any hint that these papers were chosen for judge/evaluation concerns can reach either model.** Both roles received exactly the ordinary production manuscript/evidence context.

## E. Isolation

Every run executed against **copied databases with copied manuscript cache and redirected report output**, so neither a production row nor a committed report artifact was reachable:

- state → `<scratch>/state/{agent_memory,deep_research}.sqlite3` (copies), set both in the redirected config and via `PAPER_SCOUT_<TRACK>_STATE_PATH`;
- full-text cache → a copy, so the production cache could not be written even on `--force` refetch;
- `output.report_dir` and `digest_dir` → scratch, so the committed `paper-quality-2026-09-18.md` was not clobbered.

Production database hashes were captured before the first run and re-checked after the first paper and again at the end; identical each time.

## F. Frozen current-gate outcomes — recorded before any history was retrieved

```text
FROZEN_RESULTS_SHA256: 0f28be3c376cd7b25f6873cdae1f466183eb509dee2274e16eb67a8a668b6c39
```

| # | Paper | Gemini | DeepSeek | Blockers | Promotion | Outcome | Provenance | Calls | Manuscript hash = frozen |
|---|---|---|---|---:|---|---|---|---:|---|
| 1 | A New Paradigm | `uncertain` | `uncertain` | 3 | **not promoted** | success | pass | 2 | yes |
| 2 | PEARL | `pass` | `pass` | 0 | **promoted** | success | pass | 2 | yes |
| 3 | AREX | `pass` | `pass` | 0 | **promoted** | success | pass | 2 | yes |
| 4 | Closing the Consistency Gap | `pass` | `pass` | 0 | **promoted** | success | pass | 2 | yes |
| 5 | Is Deep Research Reliable? | `pass` | `pass` | 0 | **promoted** | success | pass | 2 | yes |
| 6 | AppliedScientist | `pass` | `pass` | 0 | **promoted** | success | pass | 2 | yes |

**Promotions 5 of 6. Retries 0. Manual corrections 0. Technical failures 0.** Every paper: coverage gate `pass`, scope `full_text`, gate `dual-promotion-v2`, assessor `gemini-3.8-flash`, receipt `canonical-response-v1`, `reasoning_tokens = 0`. All six re-acquired manuscripts hashed identically to the hash frozen in the challenge set, so no paper/manuscript mismapping occurred and the audited text is the assessed text.

**Evidence provenance:** 654 context blocks across the six papers, **0 unknown evidence ids**, 6 distinct context ids, and every context `source_hash` equal to both the assessment's `source_content_hash` and the frozen manuscript hash. No fabricated evidence, no cross-paper contamination.

## G. Observational evaluation-independence audit

Each manuscript was inspected directly. No stored output was modified.

### G.1 PEARL — `openalex:W7170112970`

**A. What is optimized/repaired.** LLM-generated scientific reasoning graphs, repaired "toward strict semantic validity": rejected edge types, local inference steps and terminal roots.

**B. What supplies the signal.** An LLM judge under the CG/REA protocol. Verbatim: PEARL "uses matched evidence-grounded **judge feedback** to repair rejected edge types, local inference steps, and terminal roots", and "obtains local **judge decisions** over reasoning units, which separate majority-correct reasoning anchors from evaluator-rejected units".

**C. Is the final evaluation independent of the optimization signal? No — stated three times in the manuscript.**

> repaired … "and then **judged again under the same CG/REA protocol**"
> "evaluator-guided correction over a matched source graph with **final CG/REA re-evaluation**"
> "The repaired graph is **evaluated again under the same protocol**." … "Repair is therefore local and **judge-conditioned**."

The headline claim — strict-gate passes 0/350 → 300/350, average REA 0.339 → 0.906 — is measured in exactly the currency the repair loop optimizes. The ablations (Retained root 130/350, Root only 102/350, full PEARL 300/350) are all scored by the same gate, so they do not break the circularity either.

**D. Independent validation.** *human* — **0 occurrences in the manuscript**. *inter-annotator / kappa / agreement* — **0 occurrences**. No held-out judge, no alternative judge, no judge calibration, no human reference labels. The limitations section is one sentence about schema/modality portability and does not address evaluator dependence.

**E. Do the reported gains risk evaluator circularity? Yes — and the manuscript's own independent measurement fails to corroborate them.** MiniCheck is the single non-CG/REA signal, and the paper explicitly demotes it: "reported as **diagnostics only**", "**not the strict acceptance gate**". Its numbers move the wrong way — support rates across raw extraction, the LLM second-pass graph and the PEARL terminal graph are **.511, .584 and .557**. The one measurement not produced by the optimization target therefore shows PEARL *slightly below* the unrepaired LLM second-pass graph, while the judge-measured metric rises from 0/350 to 300/350.

**F. Does the current promotion acknowledge this? No.** The gate *described* the mechanism accurately — Gemini's `method_assessment` reads "evaluator-grounded local semantic repair before applying a strict acceptance gate (CG=1.0, REA=1.0)" — but recorded it as a design virtue ("cleanly separates structural admissibility from semantic validity", "rigorous methodology", `confidence = high`). Its `evaluation_assessment` credits "comprehensive ablation tests and **external grounding checks**", presenting MiniCheck as corroborating support when the manuscript both restricts it to diagnostics and shows it declining. A scan of the complete stored output for *circular*, *same judge*, *same protocol*, *self-referential*, *inter-annotator*, *kappa*, *human*, *calibration*, *held-out* and *independent judge* returns **zero hits on every term**. DeepSeek returned `promotion_decision = pass` with **zero blocking reasons**.

**Classification: `CLEAR_EVALUATION_CIRCULARITY` — promoted, with no independent corroboration and no acknowledgement.**

### G.2 AREX — `openalex:W7171268386`

Optimized: a deep-research agent, via agentic mid-training and turn-level RL with outcome rewards plus bounded key-step shaping, on **verified synthetic training tasks** built from human-expert templates. Headline evaluation: accuracy / F1 / Item-F1 on **six established third-party benchmarks** — BrowseComp, GAIA, xbench-DeepSearch-2510, DeepSearchQA, WideSearch-en, HLE (with tools) — against frontier and open-source baselines. The word *judge* appears **0 times**. The agent's internal self-verification is machinery inside the system, not the yardstick: success is scored by benchmarks with their own ground truth, entirely separate from the training reward.

**Classification: `INDEPENDENT_EVALUATION_STRONG`. Promotion defensible.**

### G.3 Closing the Consistency Gap — `doi:10.48550/arxiv.2609.08832`

Optimized: retrieved guidelines that reduce run-to-run inconsistency. Signal: a Consistency Analyzer that resamples the same LLM N = 30 at temperature ≤ 0.5 and scores mode concentration (pairwise Jaccard) — a statistical variability measure, not a quality judgment — after which an LLM generator writes guidelines for flagged steps. Headline evaluation: Pass^5 / Mean@5 on the 168-task AppWorld split using "**the standard AppWorld grader**", giving +16 pp Pass^5 same-task and +13 pp similar-task.

Genuine dependence exists and is disclosed: guidelines are generated by "prompting the same model that produced it (**acting as judge on its own scorecard**)", and the same-task condition derives guidelines from a trajectory of the same task. Against that: the reported number comes from an external deterministic grader rather than the analyzer; the analyzer is **calibrated against that grader** (trajectory consistency vs. pass/fail, **AUROC 0.69**, explicitly offered only "where no ground-truth rating is available"); a separate similar-task generalization condition is reported; and the paper is explicit that "consistency is not the same as accuracy". The gate's own uncertainty note independently flags the "inability to verify semantic correctness over pure stability".

**Classification: `EVALUATION_DEPENDENCE_BUT_ADEQUATELY_VALIDATED`. Promotion defensible.**

### G.4 Is Deep Research Reliable? — `openalex:W7171268620`

Measured: the false-conclusion adoption rate (FCAR) of *other* deep-research systems under seeded misleading knowledge. There is no optimization loop against the judge — nothing is trained or repaired to raise the metric — so the structural precondition for circularity is absent. The judge (DeepSeek-V4 Pro) is nevertheless validated directly: "two human annotators, **blinded to the model judgments**, independently evaluated a random sample of 300 final reports", disagreements adjudicated, yielding **99.7 % raw agreement and Cohen's κ = 0.993**, plus 100 %-coverage manual validation of every target false conclusion and per-report manual validity screening.

**Classification: `INDEPENDENT_EVALUATION_STRONG`. Promotion defensible.**

### G.5 AppliedScientist — `openalex:W7213371831`

The hardest case in the set, and the one handled best by its authors. An AI Reviewer both guides revision and scores it — the paper says so plainly: "In a closed revision loop, the reviewer serves both as an evaluator and as the feedback signal", "much as a grader or reward model directs optimization in reinforcement learning. Even a capable scientist can therefore optimize toward the wrong objective when its reviewer is unreliable."

Corroboration is supplied on every limb this diagnostic looks for:

- **Independent evaluator** — every saved version of the human-initialized trajectory is re-scored by **Stanford Reviewer**, "used only for external evaluation and its outputs are never shown to the scientist", which "observes the same upward trajectory … indicating that the improvements … reflect genuine gains in paper quality **rather than optimization towards a single reviewer**".
- **Human calibration of the judge** — 100 sampled papers, four human experts, Spearman **ρ = 0.84**, raw inter-reviewer agreement **92 %**, Cohen's **κ = 0.81**; venue-decision agreement 76.2 %.
- **Control condition** — autonomous self-revision under a fixed prompt, isolating the effect of guidance.
- **Memory control** — the reviewer retains no history, so earlier scores cannot bias later ones.
- **Honest negative result** — 128/150 execution weaknesses resolved (85.3 %) but only 2/18 idea-related (11.1 %), plus manual arXiv verification of 14 idea-related objections.

**Classification: `EVALUATION_DEPENDENCE_BUT_ADEQUATELY_VALIDATED`. Promotion defensible.**

### G.6 A New Paradigm — `doi:10.65649/ukh4n33x`

A narrative review. It makes **no first-person empirical claim** — the patterns `we (evaluate|measure|report)` and `our (experiment|result)` match **0 times** — so it has no evaluator-dependent headline outcome that could be circular; it was screened in because it *discusses* automated judging. It was not promoted, on unrelated and verifiable grounds: no primary validation, no pre-registered protocol or risk-of-bias instrument, and extensive anomalous citation stuffing. One observation worth recording: the review relays, without caveat, that an AI system generated papers "exceeding the acceptance threshold of a top machine learning conference **as judged by the automated reviewer**" — an uncritically repeated circular claim, though the gate withheld the paper anyway.

**Classification: `INDEPENDENT_EVALUATION_STRONG` (vacuously — the four-label scheme has no slot for "no evaluator-dependent claim"). Non-promotion defensible.**

## H. Classification against the frozen gate outcome

| # | Paper | Observational classification | Current gate | Correct? |
|---|---|---|---|---|
| 1 | A New Paradigm | `INDEPENDENT_EVALUATION_STRONG` (vacuous) | not promoted | yes |
| 2 | **PEARL** | **`CLEAR_EVALUATION_CIRCULARITY`** | **promoted, 0 blockers** | **no — miss** |
| 3 | AREX | `INDEPENDENT_EVALUATION_STRONG` | promoted | yes |
| 4 | Closing the Consistency Gap | `EVALUATION_DEPENDENCE_BUT_ADEQUATELY_VALIDATED` | promoted | yes |
| 5 | Is Deep Research Reliable? | `INDEPENDENT_EVALUATION_STRONG` | promoted | yes |
| 6 | AppliedScientist | `EVALUATION_DEPENDENCE_BUT_ADEQUATELY_VALIDATED` | promoted | yes |

`BORDERLINE_EVALUATION_CIRCULARITY`: none. The set separated cleanly into one clear circularity, two well-validated dependences, two independent evaluations and one paper with no evaluator-dependent claim.

**Five of six correct. The one `CLEAR_EVALUATION_CIRCULARITY` paper in the set was promoted.**

## I. Historical outcomes — retrieved only after §F was frozen

| Paper | Historical (latest) | Historical gate | Current | Reading |
|---|---|---|---|---|
| A New Paradigm | `uncertain` | scientific-gate-v1 | not promoted | consistent |
| **PEARL** | **`uncertain`** | **dual-promotion-v1** | **promoted** | **miss replicated** |
| AREX | `uncertain` | scientific-gate-v1 | promoted | current outcome better supported |
| Closing the Consistency Gap | `uncertain` | scientific-gate-v1 | promoted | current outcome better supported |
| Is Deep Research Reliable? | `uncertain` | scientific-gate-v1 | promoted | current outcome better supported |
| AppliedScientist | `pass` | dual-promotion-v1 | promoted | consistent |

The retired pair's PEARL blockers, read only after freezing, name this diagnostic's finding almost word for word:

> "The strict gate (CG=1.0 AND REA=1.0) is defined and enforced by the **same judge-feedback loop used for repair**, meaning the evaluator that drives repair …"
> "The paper does **not report inter-annotator agreement, judge reliability, or any calibration** of the LLM-as-judge against human judgments for the CG/REA …"
> "Limitations … do not address the **circularity of using the benchmark's own evaluation protocol as both the repair signal** …"

Two points of fairness about the historical comparison. First, the retired pair is not a gold standard: its PEARL blockers also include the claim that "GPT-5.2, Gemini 3.1 Pro Preview, Grok 4.1 Thinking, Qwen3.5-397B-A17B" correspond to no released models — the same knowledge-cutoff artifact Batch 5 documented, and this project itself runs `gemini-3.8-flash`. Second, three of the four historical `uncertain` verdicts on papers 3–5 sit alongside recorded `evidence_validation_failure` and `protocol_failure` execution outcomes on the same papers, so those historical labels carry technical noise; my own audit, not the historical label, is the basis for calling the current outcomes on those three well supported.

**On PEARL, however, the historical blocker is substantively correct, independently reconfirmed here from the manuscript alone, and strengthened** by an observation the retired pair did not make: MiniCheck, the only independent measurement in the paper, *declines* for PEARL relative to the unrepaired LLM second-pass graph.

## J. What the pattern across six papers shows

The gate is not blind to judge validity in general. It engaged correctly with evaluator dependence on both papers where dependence is real, and its rationales named the relevant evidence — Batch 5 found the same thing across six of ten papers. The discriminating factor across all six papers here is sharp and worth stating precisely:

> **In every case the gate got right, the manuscript itself supplied explicit validation language** — κ, ρ, ICC, "human annotators, blinded", "independent evaluator", "AUROC", "standard grader", named external benchmarks. **In the case it got wrong, the manuscript is silent**, and the gate read silence as the absence of a problem rather than the absence of evidence.

That is a recognition failure, not a reasoning failure: the gate reports validation when a paper advertises it, and does not itself ask whether an evaluator that supplies the optimization signal can also certify the result. Its rubric already says "Missing or incomplete material means uncertain", and PEARL's manuscript is complete and coverage-passing — so the validation evidence is genuinely absent rather than merely unretrieved, which is exactly the condition the rubric's clause is meant to catch.

One clear circularity case in a six-paper set is **not** a demonstrated systematic defect, and this report does not claim it is. But it is also not noise: the outcome **replicated deterministically** against a fresh blinded run of the current pair, on the one paper in the set where the failure mode could express itself.

## K. Diagnostic verdict

The §10 criterion is conjunctive, and the first limb is violated:

| Criterion | Result |
|---|---|
| No `CLEAR_EVALUATION_CIRCULARITY` paper promoted without meaningful independent corroboration | **FAILED** — PEARL promoted; its only independent measurement disconfirms rather than corroborates |
| Borderline cases receive scientifically defensible outcomes | met (vacuously — no borderline cases arose) |
| No systematic blindness observed | met — 5/6 correct, both adequately-validated dependences promoted correctly |
| No technical defect | met — 0 failures, 0 retries, 0 unknown evidence ids, 444 tests OK |

```text
EVALUATION_INDEPENDENCE_DIAGNOSTIC: FAIL
```

## L. Smallest general requirement that appears missing — reported, not implemented

Derived from the evidence above, not from PEARL alone: it is the single requirement that the two adequately-validated papers already satisfy trivially and that PEARL fails on both limbs.

> **When a manuscript's primary reported outcome is produced by an evaluator, judge or scoring protocol that is also used to generate the optimization, selection or repair signal for the system under study, promotion requires affirmative evidence that the outcome holds independently of that evaluator** — human or expert validation, inter-rater agreement or judge calibration, a held-out or alternative judge, or a non-LLM objective metric — **or explicit treatment of that evaluator dependence as a major limitation. Where the manuscript reports any measurement independent of that evaluator, the assessment must check whether it corroborates the claimed gain; a measurement that does not corroborate is a blocking concern. Absence of such evidence is scientific uncertainty, not a neutral omission.**

The second sentence matters as much as the first: PEARL would likely still have passed a rule that only asked "is validation evidence present?", because Gemini already counted MiniCheck as "external grounding checks". It is the direction of the independent number that is decisive.

**This wording is not implemented and must not be implemented as part of this task.** Any rubric or prompt change is a separate engineering task, which must then be validated on a fresh unseen batch before it can count as resolving this finding. No gate change, no threshold change, no re-run of PEARL under altered semantics was performed.

## M. Cost

Six papers, two calls each, zero retries.

| Provider / model | Calls | Prompt | Completion | Total | Reasoning | Monetary |
|---|---:|---:|---:|---:|---:|---|
| google / `gemini-3.8-flash` | 6 | 235,243 | 5,638 | 240,881 | 0 | **UNKNOWN**, `covered_by_msc_allocation` |
| openrouter / `deepseek/deepseek-v4-pro-0813` | 6 | 215,355 | 2,681 | 218,036 | 0 | **$0.15003843** (`provider_reported`) |

| Item | Value |
|---|---|
| Known money this task (OpenRouter only) | **$0.15003843** |
| Gemini | 235,243 in / 5,638 out — **monetary cost UNKNOWN / MSc allocation** |
| Engineering review | none — no code changed, so none was required |
| Cumulative against the $10 ceiling | $6.84057187 → **$6.99061030** (remaining $3.00938970) |

The Google endpoint reports no charge and this project has not established the allocation's effective rate. Usage is recorded in exact tokens; **no monetary amount is fabricated and Gemini is not assumed to be free.**

Cost guard respected: **6 historical papers, the stated maximum. No unseen paper was consumed. Batch 6 was not run.**

## N. Production-integrity verification

| Check | Result |
|---|---|
| Production DB SHA-256, before vs after | **byte-identical**, all three |
| | `3c25aaf7…6b18` `data/paper_scout.sqlite3` |
| | `414975f3…1b72` `data/deep_research/paper_scout.sqlite3` |
| | `a04493c0…4879` `data/engram/paper_scout.sqlite3` |
| Production assessment rows | 348 / 271 / 48 = **667**, unchanged (Batch-5 end state) |
| Production papers | 18,343 / 2,395 / 306, unchanged |
| Latest production `assessed_at` | `2026-09-18T18:41:55` — the Batch-5 timestamp, unmoved |
| `dual-promotion-v2` rows in production for the six diagnostic ids | **0** |
| Diagnostic rows | exist only in the scratch copies (agent_memory 349, deep_research 276) |
| Production full-text cache | **0** files written during the diagnostic |
| Historical outcomes | unchanged — no row deleted, mutated or appended |
| Public generated files (`docs/`) | `git diff HEAD -- docs/` empty |
| Committed reports | `git status --short reports/` empty before this report was written |
| `git status --short` | clean; HEAD still `b2bb86ca6` |
| Unit suite | **444 tests, OK** (unchanged from Batch 5) |
| Pages deployment | **none required and none performed** |

**No diagnostic result was published as an assessment.** These outcomes exist only on copied state and in this report, and they do not revise any historical or public promotion. In particular, **PEARL's public record is unchanged**: this diagnostic did not promote it in production.

## O. Operational readiness

Batch 5 is untouched and stands: `BATCH_5_GENERALIZATION_RESULT = PASS`, with all twelve of its generalization criteria met, its population manifest reproducing exactly, and its historical state intact.

Readiness nonetheless stays **NO**, and this diagnostic moves it further from YES rather than closer:

1. The PEARL false-promotion concern is **unresolved and now replicated** — a fresh, blinded run of the current pair promoted it again, with zero blocking reasons and `confidence = high`.
2. The one paper in a deliberately enriched challenge set whose evaluation is clearly circular was promoted, and its only independent measurement points the other way. That is precisely the failure mode a conservative curated library must not have.
3. A concrete missing scientific requirement is now identified (§L) but **not implemented**, and implementing it would require a separate engineering task plus a fresh unseen validation batch before it could count as resolved.

Against that, the evidence for a *systematic* blind spot remains limited: 5 of 6 correct here, both genuine evaluator dependences promoted on real independent validation, and Batch 5's finding that the gate engages with judge validity wherever a judge is used. The defect is narrow and specific — not a general inability to reason about judges, but a failure to treat evaluator reuse as requiring affirmative evidence when the manuscript says nothing.

Batch 6 was not run. Recurring production assessment was not enabled.

---

```text
BATCH_5_GENERALIZATION_RESULT = PASS
EVALUATION_INDEPENDENCE_DIAGNOSTIC: FAIL
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
```
