# Manuscript coverage recovery — 2026-09-18

**Engineering checkpoint: coverage repair and offline development validation are complete locally. The required external `pr-review` is blocked by automatic approval review pending explicit source-export approval. No PR merge, paid scientific recovery, holdout continuation, or deployment has occurred. This report does not claim the requested end-to-end recovery is complete.**

## Canonical state

The working tree was clean on `main`. Fetch, checkout, fast-forward pull, history and ancestry checks verified the actual canonical SHA **`ddfbb96d2d57e72b5261c084dcd929e13ebc0b41`**. The system Git could not run because the host Xcode license was unaccepted; installed Homebrew Git completed the requested commands. No license settings were changed.

All three assessment databases were opened read-only for the inventory. Public sidecars confirm the immune-world-model paper, the water-sustainability book and SciHazard remain `not_assessed`, with `full_text_assessed=false`. The two prior valid promotions and eight availability outcomes remain published. No incomplete-input scientific judgment, raw execution record, assessment database or snapshot was published by this task.

## Exact affected holdout state

This table joins every frozen roster entry to database records, saved per-paper `started`/`done`/call artifacts and public sidecars. Counts are enumerated from those records, not inferred from narrative totals. “Saved calls” is the completed recovery-v2/remaining-holdout phase; Causal Path Alignment's earlier original and first-recovery failures are separate immutable history.

| Track / position | Paper / canonical ID | Exact state | Saved calls | Public status |
|---|---|---|---:|---|
| agent_memory / 1 | Causal Path Alignment: Anchoring the Optimization Trajectory for Controllable In-Parameter Knowledge Editing · `doi:10.24963/ijcai.2026/655` | Valid recovery-v2 promotion; earlier failures preserved | 2 | `pass` |
| agent_memory / 2 | nox-mem: Pain-Weighted Hybrid Memory for LLM Agents · `doi:10.5281/zenodo.22649269` | Manuscript unavailable; zero scientific calls | 0 | `uncertain` |
| agent_memory / 3 | Contextualized Reinforcement Learning with Episodic Memory Networks · `doi:10.5281/zenodo.22587729` | Manuscript unavailable; zero scientific calls | 0 | `uncertain` |
| agent_memory / 4 | Hierarchical Reinforcement Learning with Memory Networks · `doi:10.5281/zenodo.22623238` | Manuscript unavailable; zero scientific calls | 0 | `uncertain` |
| agent_memory / 5 | Delete Names Five Operations: Erasure Semantics for Derived Agent Memory, and Why a State-Level Definition Cannot Be the Auditable One · `doi:10.5281/zenodo.22425280` | Manuscript unavailable; zero scientific calls | 0 | `uncertain` |
| agent_memory / 6 | retainkit: context and memory policies for LLM agents, scored by the evidence that survives the token budget · `doi:10.5281/zenodo.22352965` | Manuscript unavailable; zero scientific calls | 0 | `uncertain` |
| agent_memory / 7 | Hierarchical Reinforcement Learning with Temporal Abstraction and Memory · `doi:10.5281/zenodo.22336737` | Manuscript unavailable; zero scientific calls | 0 | `uncertain` |
| agent_memory / 8 | Who Did It? Sleep, Source Memory, and Action Memory in Human 4-Year-Olds · `doi:10.3390/bs16091578` | Manuscript unavailable; zero scientific calls | 0 | `uncertain` |
| deep_research / 1 | An immune world model for multiscale forecasting and therapeutic hypothesis generation · `doi:10.48550/arxiv.2609.14709` | Incomplete input: STAR METHODS omitted; withheld | 2 | `not_assessed` |
| deep_research / 2 | AppliedScientist: Automated Scientific Revision Through Iterative AI Reviewing · `openalex:W7213371831` | Valid promotion | 2 | `pass` |
| deep_research / 3 | Cracking a 600-Year-Old Mystery with Geometry: The Voynich Manuscript Finally Speaks — An Ô-HAT Cross-Language Phase-Space Analysis · `doi:10.5281/zenodo.21493208` | Manuscript unavailable; zero scientific calls | 0 | `uncertain` |
| deep_research / 4 | Artificial Intelligence for Water Sustainability and Climate Adaptation in Small Island States · `doi:10.70593/978-93-7185-684-3` | Incomplete input: front matter/contents only; withheld | 2 | `not_assessed` |
| deep_research / 5 | SciHazard: A Benchmark for Measuring Scientific Safety Risks with Decomposed Harm Scoring · `openalex:W7170225285` | Interrupted after primary; complete selected scientific input; no assessment row | 1 | `not_assessed` |
| deep_research / 6 | PEARL: Auditable Repair for Scientific Reasoning Graph Extraction · `openalex:W7170112970` | Entirely unattempted | 0 | `not_assessed` |
| deep_research / 7 | DRNOISE: Benchmarking Deep Research Agents in Misleading Evidence Environments · `openalex:W7170112771` | Entirely unattempted | 0 | `not_assessed` |
| deep_research / 8 | Recent Advances in AI for Automated ICD Coding: A Systematic Literature Review · `doi:10.1007/s10916-026-02429-7` | Entirely unattempted | 0 | `not_assessed` |

There are exactly two historical incomplete-input attempts: the immune-world-model paper and the front-matter-only book. Only the former contains the five omitted STAR METHODS pages. SciHazard's primary call was interrupted by the global stop; its supplied scientific context was complete, and no adjudicator call or production assessment row was fabricated. PEARL, DRNOISE and the ICD-coding review have no acquisition/call artifacts or assessment rows; only their existing roster/state metadata was inspected.

## Root cause

Affected manuscript: **An immune world model for multiscale forecasting and therapeutic hypothesis generation**, `doi:10.48550/arxiv.2609.14709`; PDF SHA-256 `78f8323f1123e74bccdc127ad59fe978d99436c2bed18424549321d7f3eb85cb`.

The source PDF had **21 pages**, all **21 extracted successfully**, no unreadable pages and no extraction truncation. Extraction retained 67,780 page-text characters (67,820 including document join separators). Original selection supplied **12 pages: 1–12**, 39,272 source characters in a 39,710-character context. It omitted pages **13–21**. The configured prompt budget was **180,000 characters**, not a token estimate; section sampling bound 8,000 characters, extraction bound 400,000 characters and 80 pages. Selection was not budget-limited. The downstream scientific request limits remain unchanged at 300,000 serialized bytes and 4,096 output tokens.

| Original parser heading | Actual page range | Original classification / selection |
|---|---|---|
| Abstract / front matter | 1 | Abstract; supplied |
| Introduction | 1–2 | Introduction; supplied |
| Results | 2–10 | Results; supplied |
| Discussion | 11–12 | Discussion; supplied |
| References | 12–16 | Excluded back matter; page 12's preceding discussion supplied |
| STAR METHODS, undetected | 17–21 | Inherited References label; all omitted |

The exact omitted methods-page character counts were **17: 3,232; 18: 3,615; 19: 3,288; 20: 3,155; 21: 1,906**, totaling **15,196**. Every one was excluded because the named-heading regex failed to recognize STAR METHODS and `current_heading=References` continued across page boundaries. `_section_kind('STAR METHODS')` itself can recognize the methods role; the heading never reached it. The selector removed all sections labeled References before computing eligible-body coverage. Consequently it falsely reported `omitted_body_characters=0` and counted 28,462 characters as excluded back matter.

The old algorithm supplied all recognized body sections when they fit; otherwise it used role round-robin, spread-ordered chunks and a per-heading cap. Here it took the full recognized-body branch. The defect was **heading/section-boundary detection followed by inherited back-matter exclusion and incomplete coverage accounting**, not PDF extraction, page-range parsing, token pressure, or an actual absence of methods. Baseline diagnostics were captured before source edits; no old context, response or assessment was repaired.

## Coverage architecture

Page boundaries, numbered hierarchy and standalone title shape provide structural boundaries independently of a scientific-name vocabulary. Generic headings and their continuation pages survive. Novel heading source lines are retained, so adjacent structural candidates cannot consume one another. JATS body membership overrides an apparently non-scientific title; an XML body section titled References stays body text.

Only bibliographic prefixes with an author-style entry start and an inline locator on that same physical line are excluded. Exclusion stops at the first locator. Wrapped citations, ambiguous remainders and other back matter are retained conservatively. This avoids extending References or Acknowledgements across an unfamiliar method, including one-word or entirely unheaded continuations. The tradeoff is additional reference text in some contexts. Adjacent spans with the same heading/page are coalesced to avoid formatting overhead on long manuscripts.

All detected body and appendix text is supplied when it fits. Under pressure, deterministic round-robin selection balances method, results, limitations/discussion, contribution, appendix and unfamiliar-body groups. Each logical section receives contiguous prefixes, retained in source order; a long method has no total per-heading cutoff. Partial contexts are diagnostics, not approved scientific inputs.

The `coverage-v2` manifest records total/retained/readable/missing pages, scientific pages, supplied and omitted pages, roles, per-section source/supplied/omitted characters and omission reasons, excluded prefixes, configured character budget, actual chunk size, normalization/structure/selection versions and input hash. Existing evidence provenance is unchanged.

Before either scientific model is called, the new coverage gate checks the current manifest and exact input hash. Missing/extraction-gap pages, absent body structure, front matter/contents only, or any omitted body text yield **`text_coverage_failure`**, public status **`not_assessed`**, zero model calls and no primary/adjudicator judgment. Technical coverage is not converted into scientific uncertainty or insufficiency. Historical receipt validation, prompts, models, rubric, promotion rule, evidence semantics, relevance criteria and publication-status policy are unchanged.

## Tests

The structure-only STAR METHODS fixture preserves the actual 21-page layout and page character lengths using synthetic prose. It proves all five formerly omitted pages are supplied, or explicitly marked incomplete under budget pressure. No live model is used.

General cases cover unfamiliar and Unicode headings, one-word Protocol and unheaded tails, post-reference methods mentioning years/artifact URLs, acknowledgements boundaries, long contiguous methods, balanced budget failure, large references, scientific appendices, missing/empty/duplicate/truncated pages, headings at page boundaries, empty JATS sections, structural XML body membership, UTF-8/hash integrity, zero-call failures and persisted `not_assessed` states. Receipt tests retain their exact scientific bytes and explicitly rebind synthetic input hashes; legacy judgments are unchanged.

**380 unit tests pass.** All three tracks pass relevance, promotion/quality, discovery and idempotency checks plus offline site builds. Schemas, links, exposure scans, workflows, generated-file sizes, snapshot/restore, legacy restore and `git diff --check` pass. All **641** historical assessments remain readable; all runtime tables and **3,352** baselined historical/report/manifest/operator files retain their hashes. Production source/prompt AST comparisons confirm the scientific request builder, model settings and call transport are unchanged, as are the rubric/protocol and evidence modules.

## Engineering

Branch: **`fix-manuscript-scientific-coverage`**. Final source candidate: **`1dbacd6e557f34403edac4f308627cf9d7715d71`**. Canonical base remains the publication commit above.

The first local independent review found two valid blockers: year-count heuristics could still swallow unfamiliar methods, and empty JATS sections could crash bounded selection. Subsequent review exposed one-word/acknowledgements boundary variants. The repair now bounds actual excluded citation prefixes instead of trusting arbitrary inherited back-matter ranges. Regressions preserve each counterexample. Final **local independent Codex subagent review: PASS_WITH_NOTES, zero unresolved blockers** (56 focused coverage/promotion tests, 15 heading/tail variants). Its remaining note is conservative retention of ambiguous bibliography and correct budget rejection. This local verdict does not substitute for the explicitly required external `pr-review`.

Required command: `pr-review --base origin/main`. **Not executed:** automatic approval review rejected the invocation because it would export repository source to DeepSeek/OpenRouter without recognized explicit export authorization. A specific approval request is pending. No review inference charge occurred. The established bounded DeepSeek/Opus escalation and existing shared $10 ceiling remain the intended external-review policy; prior charged/reserved total is $5.22751357504.

PR: not created. External reviewer verdict: unavailable. Merge SHA: none. Automatic merge remains conditional on passing checks, accepted external review, zero blockers, a mergeable PR and no material unreviewed changes. No merge approval will be requested separately once those conditions are met.

## Offline verification

Development verification used **44 known manuscripts**, including **25 prior calibration manuscripts**, existing Batch-2 extracts, the affected inputs and the two valid Batch-3 contexts. **42 are complete**; the front-matter-only book and the already incomplete Mr.LHDR extraction fail technically as expected. This is pre-merge development evidence. The mandatory post-merge offline verification is still pending and must occur before recovery calls.

| Representative input | Pages | Development coverage |
|---|---:|---|
| Immune world model | 21 | Complete; all five methods pages retained |
| Causal Path Alignment | 13 | Complete; prior valid context remains usable |
| AppliedScientist | 16 | Complete; prior valid context remains usable |
| A New Paradigm: Agentic AI for Scientific Discovery | 45 | Complete; long-paper context within 180,000-character budget |
| Sci-MMR | 37 | Complete; long scientific/appendix content retained |
| Conditional Memory via Scalable Lookup | 35 | Complete; prior calibration and appendix content retained |
| Water sustainability book | 12 | Technical failure: only front matter/contents |
| Mr.LHDR | 33 | Technical failure: cached extraction already incomplete |

No scientifically untouched holdout manuscript was acquired or used in these checks. No previous valid Batch-3 context was objectively invalidated. Full per-page diagnostics remain private.

## Recovery scope

The exact two historical incomplete-input papers are established in the status table. The formal **`BATCH_3_INCOMPLETE_INPUT_RECOVERY_SET` is not yet frozen**, because the user requires final determination only after post-merge offline verification. The immune-world-model context is complete in development checks. The book remains blocked by its incomplete source and must not receive a paid scientific call unless valid input becomes available within the authorized source scope.

Valid promotions, eight manuscript-unavailable outcomes, SciHazard's complete-input interrupted primary, and untouched papers are excluded from automatic incomplete-input reruns. SciHazard is not an unseen paper and must not be silently folded into the untouched holdout.

## Recovery

Not run. Scientific model calls and cost for this task: **0 / $0**. No new assessment rows were appended. Original invalid attempts remain historical/internal only. No manual scientific corrections occurred.

## Remaining holdout

PEARL (`openalex:W7170112970`), DRNOISE (`openalex:W7170112771`) and the ICD-coding review (`doi:10.1007/s10916-026-02429-7`) remain entirely unattempted. Continuation has not occurred; it remains conditional on completed incomplete-input recovery without a new systematic defect. No replacements, Batch 4 or recurring production assessment were selected or started.

## History

```text
ORIGINAL_BATCH_3_GENERALIZATION_RESULT = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_CHECK = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_V2_CHECK = PASS
BATCH_3_REMAINING_HOLDOUT_RESULT = FAIL
```

The original calibration/Batch-2/Batch-3 outcomes are not reinterpreted. Existing assessments remain unchanged and readable. Local snapshot/restore verification protects private history; it does not retroactively validate incomplete-input attempts.

## Private durability and publication

**Current remote preservation mechanism is public-release based and therefore not acceptable for private assessment state.** Storage redesign is a separate follow-up. Databases, raw execution records and snapshots remain local/private. No release asset or Pages deployment was created or updated by this task. Generated validation builds use temporary database/output copies; canonical public artifacts remain unchanged.

## Operational readiness

The end-to-end gate remains unapproved while the mandatory external review, merge and post-merge verification are incomplete. Software checks and development coverage results do not establish scientific generalization or operational promotion precision.

```text
MANUSCRIPT_COVERAGE_GATE_READY: NO
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
```
