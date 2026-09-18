# Manuscript coverage recovery — 2026-09-18

**The coverage repair passed external independent review, merged, and post-merge offline verification. The bounded incomplete-input recovery and the frozen holdout continuation were then executed under the unchanged frozen model pair, rubric and promotion rule. Historical failures are preserved unchanged. No Batch 4 was selected and no recurring production assessment was started.**

## A. Canonical state

| Item | Value |
|---|---|
| Starting branch | `fix-manuscript-scientific-coverage` |
| Starting head | `5c3410b0e` (report-only commit on top of the source candidate) |
| Implementation commits | `e26187af5`, `979a6d6d1`, `1dbacd6e5` |
| Final source candidate reviewed | `1dbacd6e557f34403edac4f308627cf9d7715d71` |
| Canonical base before merge | `ddfbb96d2d57e72b5261c084dcd929e13ebc0b41` |
| PR | https://github.com/vernerisirva/agentmempaper/pull/37 |
| External reviewer (configured) | `deepseek/deepseek-v4-pro-0813` — **failed to converge**, no verdict |
| External reviewer (escalation) | `moonshotai/kimi-k3` — **PASS_WITH_NOTES**, 0 blocking findings |
| CI | `offline-validation` pass; PR `MERGEABLE` / `CLEAN` |
| Merge SHA | `db27d9c87daf09a337ea59dde174e621df91d897` |
| Canonical main after merge | `db27d9c87daf09a337ea59dde174e621df91d897` |

The host Xcode license is unaccepted, so the system Git and any `git` subprocess launched through it fail with exit 69. Homebrew Git ran every command, including the reviewer's and `gh`'s subprocesses, via an explicit PATH shim. One test, `test_named_seed_survives_an_intervening_non_state_commit`, fails only under the blocked system Git and passes under Homebrew Git. No license or host setting was changed.

Credential status, reported without reading, printing, hashing or logging any value:

```text
OPENROUTER_API_KEY: AVAILABLE   (not inherited by the session; present in the established private ~/.codex/.env)
GEMINI_API_KEY:     AVAILABLE   (not inherited by the session; present in the private global ~/.zshrc)
```

The reviewer loads `OPENROUTER_API_KEY` itself from `~/.codex/.env`, parsed as data and never sourced. The scientific runs loaded the same key into `PAPER_SCOUT_LLM_API_KEY` inside a Python launcher that never echoes it. No secret was copied into the repository.

### External review scope and redaction

The review was deliberately scoped to the source candidate `1dbacd6e5` in a temporary detached worktree, not to `HEAD`. Those two commits differ **only** by this private-state report, so every source, test and README change was reviewed and no material source change went unreviewed. The exclusion kept the frozen holdout roster, paper identities, PDF hashes and cost figures out of the external transmission.

Transmitted: 11 files — `README.md`, four `paper_scout/*.py`, six test files and one fixture (64,262 request bytes of 120,000). Not transmitted: assessment SQLite databases, durable-state snapshots, runtime state, raw execution records, manuscript PDF caches, `.env`/credential files, and this report. The reviewer additionally omits sensitive filenames and redacts credential-shaped text. No holdout paper identity (`PEARL`, `DRNOISE`, `W7170112970`, `W7170112771`, the ICD-coding DOI) appears in any transmitted file; this was verified by scanning each transmitted file.

### Reviewer non-convergence

The configured DeepSeek reviewer returned HTTP 200 but `finish_reason=length`: reasoning consumed **16,383 of the 16,384** completion tokens, leaving 1 visible token and no parseable verdict. Its documented `effort: low` did not reserve a visible-answer allocation. Escalation went to `moonshotai/kimi-k3`, the only Kimi/Qwen candidate advertising `reasoning_effort` support, which converged in 2,535 completion tokens (1,949 reasoning). No Claude-family model was used as the independent reviewer.

### Review findings triage

Verdict **PASS_WITH_NOTES**, **0 blocking findings**, 2 non-blocking notes, 1 test gap. Each was triaged and checked empirically rather than accepted at face value.

| # | Finding | Classification | Action |
|---|---|---|---|
| 1 | Locator-free citation spans become eligible body text in `split_reference_spans` | **Valid non-blocker** | No change |
| 2 | `at_boundary` blank-line check defeated by leading whitespace | **False positive as stated**; narrow residual is a valid non-blocker | No change |
| 3 | Test gap: wrapped-locator reference lists | Valid non-blocker | Covered empirically by offline verification |

**Finding 2** was disproved by direct execution. `_LINE` anchors at `^`, so `match.start()` is the line start and the leading whitespace falls *inside* the match; `text[:match.start()]` is unaffected by indentation. Four-space-indented and tab-indented title-case headings are detected, as is an indented `STAR METHODS`. The only residual case is a separator line containing whitespace rather than being empty, and a missed structural heading there cannot omit text — it only attributes the text to the preceding heading, which under bounded exclusion is still retained and counted. Direction of failure is role mislabelling, never omission.

**Finding 1** is real and is the intended conservative tradeoff. Its failure direction is fail-closed: over-inclusion can only inflate eligible body characters and trigger an explicit `scientific_context_budget_exceeded` coverage failure, never a silent omission. Across all 44 cached manuscripts it produced **zero** budget-driven failures, with a peak assessment input of 168,607 characters (93.7%) on the 45-page manuscript. The reviewer's suggested fix — excluding citation-shaped spans heuristically after a character limit — would reintroduce precisely the heuristic-exclusion defect class this change removes, and was rejected on that basis.

A concrete observed instance: page 8 of the AppliedScientist manuscript is 700 characters of wrapped bibliography whose locator falls on the following line. It is now retained and, because the `appendix` matcher full-matches the wrapped citation title, labelled `Appendix: …`. This is over-inclusion with a role mislabel, not omission, and it does not alter the rubric, the promotion rule or the evidence contract.

Zero valid blockers means no implementation change was made, so no re-review was required.

## B. Root cause

Affected manuscript: **An immune world model for multiscale forecasting and therapeutic hypothesis generation**, `doi:10.48550/arxiv.2609.14709`; PDF SHA-256 `78f8323f1123e74bccdc127ad59fe978d99436c2bed18424549321d7f3eb85cb`.

The source PDF had **21 pages, all 21 extracted successfully**, with no unreadable pages and no extraction truncation. Original selection supplied **12 pages (1–12)**, 39,272 source characters in a 39,710-character context, and omitted pages **13–21**. The configured prompt budget was 180,000 characters; section sampling bound 8,000 characters. **Selection was not budget-limited.**

| Original parser heading | Actual page range | Original classification |
|---|---|---|
| Abstract / front matter | 1 | Abstract; supplied |
| Introduction | 1–2 | Introduction; supplied |
| Results | 2–10 | Results; supplied |
| Discussion | 11–12 | Discussion; supplied |
| References | 12–16 | Excluded back matter |
| STAR METHODS, undetected | 17–21 | Inherited `References` label; all omitted |

Exact omitted methods-page character counts: **17: 3,232 · 18: 3,615 · 19: 3,288 · 20: 3,155 · 21: 1,906 — total 15,196**, confirmed page by page against the cached extract during this cycle.

The failure chain: the named-heading regex did not recognize `STAR METHODS`; `current_heading=References` therefore continued across the page boundary so pages 17–21 inherited the `References` label; the selector removed every `References`-labelled section *before* computing eligible-body coverage; coverage accounting consequently reported `omitted_body_characters=0` and counted 28,462 characters as excluded back matter. `_section_kind('STAR METHODS')` can itself recognize the methods role — the heading never reached it.

The defect was **heading/section-boundary detection followed by inherited back-matter exclusion and incomplete coverage accounting** — not PDF extraction, page-range parsing, token pressure, or an actual absence of methods.

## C. Coverage implementation

**Section parsing.** Page boundaries, numbered hierarchy and standalone heading shape establish section ranges independently of any scientific-name vocabulary (`manuscript_coverage.structural_headings`). Heading semantics are used only to *label* a role after a section is found, never to hide one. Generic headings and their continuation pages survive; novel heading source lines are retained so adjacent structural candidates cannot consume one another. JATS body membership overrides an apparently non-scientific title, so an XML body section titled `References` stays body text.

**Bounded bibliography exclusion.** Only citation prefixes with an author-style entry start *and* an inline bibliographic locator on that same physical line are excluded, and exclusion stops at the first locator (`_reference_prefix_end`, `split_reference_spans`). Wrapped citations, ambiguous remainders and other back matter are retained conservatively, so a `References` or `Acknowledgements` label can no longer extend across an unfamiliar method, including one-word or entirely unheaded continuations. Adjacent spans sharing a heading and page are coalesced.

**Context selection.** All detected body and appendix text is supplied when it fits. Under pressure, deterministic round-robin across method, results, limitations/discussion, contribution, appendix and unfamiliar-body groups gives each logical section a contiguous prefix in source order; `max_section_characters` bounds selection chunks, not a method's total inclusion. References never displace body or appendix content. Partial contexts are diagnostics and are never an approved scientific input.

**Coverage invariant.** Every detected scientifically material section is either represented in the assessment context, or explicitly recorded as omitted with a reason. The `coverage-v2` manifest records total/retained/readable/missing pages, scientific pages, supplied and omitted pages, roles detected/represented/omitted, per-section source/supplied/omitted characters with omission reasons, excluded prefixes, the configured character budget, actual chunk size, normalization/structure/selection versions and the exact input hash.

**Pre-assessment gate.** `validate_assessment_coverage` runs inside `assess_promotion` **before either scientific model is called** and before any HTTP client is constructed. A missing or legacy manifest, an input-hash mismatch, extraction gaps, missing pages, absent body structure, front-matter/contents-only input, or any omitted body text yields `text_coverage_failure`, public status `not_assessed`, and zero model calls. Technical incompleteness is never converted into `scientific_uncertainty` or `scientific_insufficient`.

**Omission provenance.** Omissions carry an explicit reason (`context_budget`) plus the affected pages and roles. Legacy receipts keep their original contract and remain readable; the gate applies only before new paid calls.

## D. Tests

**380 tests pass** (`unittest`: `Ran 380 tests … OK`; `pytest`: 380 passed, 150 subtests). The dedicated gate suite is 14 tests and 38 subtests.

Regression cases: the actual 21-page `STAR METHODS` layout with per-page character lengths reproduced using synthetic prose; unfamiliar and Unicode headings; one-word `Protocol` and unheaded tails; post-reference methods mentioning years and artifact URLs; acknowledgements boundaries; long contiguous methods; balanced budget failure; large reference lists; scientific appendices; missing, empty, duplicate and truncated pages; headings at page boundaries; empty JATS sections; structural XML body membership; UTF-8 round-trip and input-hash integrity; and persisted `not_assessed` states.

The zero-call guarantee is asserted directly: `test_coverage_failure_sends_zero_calls_and_persists_pending` checks that the stub model receives no payloads, `execution['calls'] == []`, the outcome is `text_coverage_failure`, `quality_status == 'not_assessed'`, no `primary` key exists, and the row round-trips through the store.

## E. Offline verification (post-merge, deterministic, zero model calls)

All **44 cached manuscripts** were re-run through `select_assessment_text` and `validate_assessment_coverage` at the production budget (180,000 / 8,000). **42 pass the coverage gate; 2 fail as technical failures, exactly as intended.** No untouched holdout manuscript was acquired or read.

| Category | Manuscript | Pages | Extracted | Sections | Roles represented | Omitted | Input chars | Gate |
|---|---|---:|---:|---:|---|---:|---:|---|
| A. Affected | Immune world model | 21 | 21 | 44 | body, discussion, introduction, **methods**, results | 0 | 69,357 (38.5%) | **PASS** |
| B. Calibration | AppliedScientist (prior valid promotion) | 16 | 16 | 77 | appendix, body, conclusion, introduction, limitations, methods, related, results | 0 | 68,564 (38.1%) | PASS |
| B. Calibration | Causal Path Alignment (prior valid promotion) | 13 | 13 | 55 | appendix, body, conclusion, introduction, methods, results | 0 | 70,141 (39.0%) | PASS |
| C. Long | 45-page longevity manuscript | 45 | 45 | 132 | body, conclusion, discussion, introduction, limitations, methods, results | 0 | 168,607 (93.7%) | PASS |
| C. Long | Sci-MMR | 37 | 37 | 125 | appendix, body, conclusion, introduction, limitations, methods, related, results | 0 | 161,168 (89.5%) | PASS |
| D. Appendix-heavy | Conditional Memory via Scalable Lookup | 35 | 35 | 85 | appendix, body, conclusion, introduction, methods, related, results | 0 | 102,639 (57.0%) | PASS |
| D. Appendix-heavy | Cross-Model Memory Transfer | 34 | 34 | 74 | appendix, body, conclusion, introduction, methods, results | 0 | 122,934 (68.3%) | PASS |
| E. Technical failure | Water sustainability book | 12 | 12 | 12 | none | 0 | 27,482 | **FAIL** — `scientific_body_not_established`, `front_matter_or_contents_only` |
| E. Technical failure | Mr.LHDR | 33 | 33 | 81 | 8 roles | 0 | 122,352 | **FAIL** — `extraction_incomplete` |

### The five formerly omitted pages

Raw cached page lengths 17–21 are 3,232 / 3,615 / 3,288 / 3,155 / 1,906 = **15,196 characters**, matching the root-cause measurement exactly. Under `coverage-v2` those pages contribute 15,192 source characters after canonical normalization, of which **15,192 are supplied and 0 omitted**.

`Star Methods` is now detected as a section with role **`methods`** on page 17, together with `Data And Study Participant Details`, `Public Immune And Cancer Cohorts`, `Method Details` and `Versioned Evolutionary Scientist Engine`, whose text continues across pages 18–21. Scientific body pages are 1–21, `pages_omitted` is empty, `body_pages_partially_omitted` is empty, scope is `full_text` and status is `complete`. The gate passes with no failure reasons. **The five pages are represented, not merely declared.**

### Invariant checks

Across all 44 manuscripts:

```text
1. gate PASS with omitted/partial/missing pages   : 0 violations
2. omitted body characters without gate FAIL      : 0 violations
3. detected role neither represented nor omitted  : 0 violations
4. gate PASS not recorded as complete/full_text   : 0 violations
```

Two gate-passing manuscripts represent neither a `methods` nor a `results` role because no section in them carries such a name; all of their text is still supplied as `body`. This is the intended separation: the gate certifies technical completeness, and whether a manuscript genuinely lacks methods remains the models' scientific judgment.

## F. Recovery set

Derived independently from the frozen roster, the three assessment databases, and the saved per-paper run artifacts — not from the previous narrative.

**`BATCH_3_INCOMPLETE_INPUT_RECOVERY_SET` = exactly 2 papers.**

| Canonical ID | Title | Why the previous assessment is objectively invalid |
|---|---|---|
| `doi:10.48550/arxiv.2609.14709` | An immune world model for multiscale forecasting and therapeutic hypothesis generation | Row 294 supplied 12 of 21 pages (39,710 chars). Pages 13–21 were never supplied; pages 17–21 are 15,196 characters of `STAR METHODS`. A scientific judgment was produced on a manuscript with its methods section absent. |
| `doi:10.70593/978-93-7185-684-3` | Artificial Intelligence for Water Sustainability and Climate Adaptation in Small Island States | Row 297 was produced from front matter and a contents listing only; no scientific body was ever established. A scientific judgment was produced with no method, evaluation or results text present. |

### Excluded, with reasons

- **`doi:10.24963/ijcai.2026/655` — Causal Path Alignment.** Valid recovery-v2 promotion. Re-derived under `coverage-v2`: scientific pages 1–13 against an old supplied set of pages 1–13; **no page newly covered**; 0 omitted characters. Input was complete.
- **`openalex:W7213371831` — AppliedScientist.** Valid promotion. Re-derivation initially flagged page 8 as newly covered. Direct inspection shows page 8 is **700 characters of wrapped bibliography** (the tail of the reference list), which the old code correctly excluded as back matter. No scientific body page was omitted; the input was complete and the promotion stands.
- **Eight manuscript-unavailable outcomes** (seven `agent_memory` entries and the Voynich paper): zero scientific calls, `title_and_abstract` scope. Excluded by rule.
- **`openalex:W7170225285` — SciHazard.** Its saved artifacts contain `primary-1.request/response/metadata` but **no adjudicator call, no `done.json` and no `stored-row.json`**, and it has no row in any database. Its supplied scientific context was complete, so it is not an incomplete-input invalid assessment and is excluded from recovery. A primary scientific assessment did occur, so it is **also not an untouched holdout paper**. It is reported here as its own category and was neither rerun nor folded into the continuation.

Manuscript identity was pre-checked before any paid call: both recovery manuscripts were re-fetched into a temporary cache and their content hashes are **byte-identical** to the cached extracts (`78f8323f…` and `f6c3bde2…`), so `--force` re-acquisition could not silently substitute a revised version. The original cached extracts were copied aside as evidence beforehand.

## G. Recovery results

Executed with the current frozen production primary assessor, the current frozen independent adjudicator, the same rubric, the same promotion rule and the same evidence/provenance contract. No manual correction, output rewriting or evidence substitution occurred. Every result was appended; no historical row was overwritten.

| Paper | Previous invalid state | Coverage now | Primary | Adjudicator | Promotion | Technical status | Calls | Cost |
|---|---|---|---|---|---|---|---:|---:|
| Immune world model | Row 294: `full_text`, `uncertain`, complete-looking but missing pages 13–21, input 39,710 chars | Row 299: `coverage-v2` **complete**, 21/21 pages, gate **pass**, input 69,436 chars | `pass` | `uncertain` (6 blocking reasons) | **not promoted** | `success` | 2 | $0.15750444 |
| Water sustainability book | Row 297: `partial_full_text`, `uncertain`, front matter/contents only | Row 298: gate **failed** — `scientific_body_not_established`, `front_matter_or_contents_only`, `incomplete_scientific_context` | — | — | **not promoted** | `text_coverage_failure`, `not_assessed` | **0** | $0 |

The immune-world-model recovery reaches the same outcome label as the invalid attempt, but for the first time on a defensible basis. The adjudicator's new blocking reasons engage directly with previously omitted content — the builder-benchmark comparison against named commercial model versions, the resource-availability statement, and the OrthJEPA/SE-PCA nomination procedure — evidence that the restored methods pages actually reached the models.

The book demonstrates the gate's intended behaviour: an invalid scientific judgment on incomplete input is superseded by an explicit technical coverage failure with **zero paid calls** and no scientific decision.

## H. Remaining holdout

After recovery, exactly **three** Batch-3 papers remained genuinely scientifically untouched. Each was verified against state and provenance metadata only; none of their manuscripts was acquired or read to establish this.

| Paper | DB rows | Run artifacts | Cached manuscript | Engineering fixture | Sent to external reviewer |
|---|---|---|---|---|---|
| `openalex:W7170112970` PEARL | none | none | no | no | no |
| `openalex:W7170112771` DRNOISE | none | none | no | no | no |
| `doi:10.1007/s10916-026-02429-7` ICD-coding review | none | none | no | no | no |

No new systematic defect appeared during recovery: the gate passed, both calls succeeded, there were no contract failures and no retries. Continuation therefore proceeded on exactly those three frozen papers. No replacement was selected, no code changed during continuation, and no manual correction occurred.

| Paper | Coverage | Primary | Adjudicator | Promotion | Technical status | Calls | Cost |
|---|---|---|---|---|---|---:|---:|
| PEARL | `complete`, 10 pages, gate **pass**, 7 roles incl. methods | `pass` | `uncertain` (5 blocking reasons) | **not promoted** | `success` | 2 | $0.07833504 |
| DRNOISE | `complete`, 16 pages, gate **pass**, input 58,042 chars | `pass` | `pass` (0 blocking reasons) | **PROMOTED** | `success` | 2 | $0.09990112 |
| ICD-coding review | — | — | — | **not promoted** | `manuscript_unavailable` (publisher URL is not a plausible PDF) | **0** | $0 |

**Holdout continuation result: 3 papers, 2 receiving scientific calls, 1 promotion.** This is continuation evidence only. It does not reinterpret and does not overturn `BATCH_3_REMAINING_HOLDOUT_RESULT = FAIL`.

## I. Audit

Observational only; no outcome was modified.

**Every promotion.**

| Row | Paper | Relevance | Primary / adjudicator | Blocking | Provenance | Confidence | Coverage |
|---|---|---|---|---:|---|---|---|
| 332 | Causal Path Alignment | relevant | pass / pass | 0 | pass | high | complete input (re-derived) |
| 295 | AppliedScientist | relevant | pass / pass | 0 | pass | high | complete input (re-derived) |
| 301 | DRNOISE | relevant, score 91 | pass / pass | 0 | pass | high | `coverage-v2` complete |

The DRNOISE promotion was examined in detail. Method evidence is concrete and specific: a paired clean–noisy corpus intervention, a fixed search-agent harness, a conditional deference metric and controlled ablations across verification prompts, source credibility, retriever, direct-true evidence and oracle full-context. Evaluation evidence is a 100-task benchmark across five models and ten evidence-operation families. Claim/evidence alignment is anchored to named results (Table 3, Figure 1) with mechanism claims traced to retrieval-exposure, trace-taxonomy and oracle analyses. Limitations are genuinely self-critical: a constructed rather than live-web corpus, a deference estimate resting on only 13 clean-correct tasks, and attack-aware prompts reported as upper bounds rather than deployable fixes. Primary cited 10 evidence blocks and the adjudicator independently cited 16, overlapping but not copied. No false confidence was observed, and the `high` confidence is supported by adjudicator agreement with zero blocking reasons.

One observation: DRNOISE's represented roles do not include `methods`, because no section in the manuscript carries a methods-style name. Its benchmark construction is described within body and results sections, all of which were supplied. This is the technical/scientific separation behaving as designed, not a coverage defect.

**Every primary-PASS / adjudicator-non-PASS disagreement.**

| Row | Paper | Blocking reasons |
|---|---|---:|
| 299 | Immune world model | 6 |
| 300 | PEARL | 5 |

Both sets of blocking reasons are specific and scientific rather than procedural. For the immune world model they cover unavailable code and data manifests, unverifiable future-dated baselines, a headline forecasting result that ties a condition-mean baseline, a small-cohort AUC with wide confidence intervals, a builder benchmark referencing model versions that do not correspond to public releases, and an unvalidated therapeutic hypothesis. For PEARL they identify evaluation circularity on a benchmark co-authored by the paper's authors, a judge that both drives repair and determines acceptance, unverifiable model versions, absent judge calibration or inter-annotator agreement, and limitations that do not address the circularity. In both cases the adjudicator surfaced methodological problems the primary missed. This is the dual gate working, not excessive conservatism.

**Frozen non-promotion sample.** The predefined audit sample (`agent_memory` positions 1, 5, 8 and `deep_research` positions 1, 5, 8) remains methodologically valid and was inspected. Position `deep_research/1` is the recovered immune world model, audited above. Positions `agent_memory/5`, `agent_memory/8` and `deep_research/8` are manuscript-unavailable outcomes with zero scientific calls, correctly recorded as `uncertain` with no scientific judgment asserted. Position `deep_research/5` is SciHazard, which has no assessment row at all; there is no outcome to audit, and none was fabricated.

## J. Historical integrity

Total persisted assessments went from **641 to 646** — five appended rows (298, 299, 300, 301, 302) and **zero modifications**. `save_quality_assessment` uses `INSERT OR IGNORE` with a run-scoped storage key, so a new result can never overwrite a prior one. Historical rows 294 and 297 retain their original timestamps, payloads, incomplete coverage metadata and outcomes. All three databases pass `PRAGMA integrity_check`, and every payload in all 646 rows is readable.

The invalid incomplete-input attempts are preserved exactly as historical evidence. No previously recorded failure was reinterpreted as a success.

## K. Private durable-state limitation

**The configured remote preservation mechanism publishes to a public GitHub release and is therefore not an acceptable destination for private assessment state.** No assessment database, runtime database, durable-state snapshot or raw private execution record was uploaded to a public release, to Pages, or into tracked Git during this cycle.

Snapshots were prepared and verified **locally only**: all three databases were checkpointed and verified consistent, with `integrity_check=ok` and readable contents (`agent_memory` 337 assessments / 18,343 papers; `deep_research` 261 / 2,395; `engram` 48 / 306). `.gitignore` excludes `data/**/*.sqlite3`, `data/cache/` and `*.pdf`; the only tracked path under `data/` is `.gitkeep`. Storage redesign was explicitly **not** attempted and remains a separate follow-up.

The manuscript PDF cache, per-paper run artifacts, request/response bodies and cost records remain local and private.

## L. Costs

**Engineering — OpenRouter independent code review**

| Model | Prompt | Completion (reasoning) | Total | Outcome | Cost |
|---|---:|---:|---:|---|---:|
| `deepseek/deepseek-v4-pro-0813` | 15,836 | 16,384 (16,383) | 32,220 | non-convergent, no verdict | $0.08578416 |
| `moonshotai/kimi-k3` | 15,584 | 2,535 (1,949) | 18,119 | PASS_WITH_NOTES | $0.07256745 |
| **Subtotal** | | | | 2 calls | **$0.15835161** |

**Scientific recovery**

| Paper | Role | Model | Prompt | Completion | Cost |
|---|---|---|---:|---:|---:|
| Immune world model | primary | `deepseek/deepseek-v4-pro-0813` | 27,624 | 806 | $0.03965544 |
| Immune world model | adjudicator | `anthropic/claude-sonnet-4.6` | 34,023 | 1,052 | $0.117849 |
| Water book | — | — | 0 | 0 | $0 |
| **Subtotal** | | | | 2 calls, 0 retries | **$0.15750444** |

**Holdout continuation**

| Paper | Role | Model | Prompt | Completion | Cost |
|---|---|---|---:|---:|---:|
| PEARL | primary | `deepseek/deepseek-v4-pro-0813` | 12,288 | 953 | $0.01999404 |
| PEARL | adjudicator | `anthropic/claude-sonnet-4.6` | 15,482 | 793 | $0.058341 |
| DRNOISE | primary | `deepseek/deepseek-v4-pro-0813` | 21,346 | 702 | $0.01702012 |
| DRNOISE | adjudicator | `anthropic/claude-sonnet-4.6` | 25,847 | 356 | $0.082881 |
| ICD-coding review | — | — | 0 | 0 | $0 |
| **Subtotal** | | | | 4 calls, 0 retries | **$0.17823616** |

**Cycle total: 8 calls, $0.49409221.** Scientific calls alone: 6 calls, 136,610 prompt tokens, 4,662 completion tokens, $0.33574060. Prior charged/reserved total was $5.22751357504, giving a cumulative **$5.72160579** against the shared $10 ceiling.

**Unknown or unbilled:** manuscript HTTP acquisitions, including the two pre-flight hash verification downloads, carry no model charge. The water book and the ICD-coding review each made zero model calls and incurred no scientific cost. No provider charge outside the metadata above was observed, and no call was retried.

## M. Model configuration

The merged production configuration pins `PRIMARY_MODEL = deepseek/deepseek-v4-pro-0813` and `ADJUDICATOR_MODEL = anthropic/claude-sonnet-4.6`, and `validate_pair` requires two distinct explicitly pinned families over OpenRouter. **It does not specify Gemini for any scientific role.** The scientific model configuration was therefore left unchanged for this recovery and continuation, and `GEMINI_API_KEY` was not used. The runs set only `PAPER_SCOUT_LLM_API_KEY`, `PAPER_SCOUT_LLM_BASE_URL` and `PAPER_SCOUT_LLM_MODEL`, deliberately leaving `PAPER_SCOUT_QUALITY_LLM_MODEL` and `PAPER_SCOUT_QUALITY_ADJUDICATOR_MODEL` unset so the frozen constants applied. Changing model identity now would have confounded the holdout and recovery.

**Follow-up (not performed here):** moving future *operational* scientific calls to the MSc Gemini allocation is recorded as a separate operational task requiring its own frozen-configuration decision.

## N. Validation

Full repository validation on merged `main` with the new results in place:

- **380 tests pass** (`unittest` and `pytest`).
- All three tracks: relevance precision 1.000 / recall 1.000, 0 false positives, 0 false negatives; quality/promotion fixtures 8/8 passed, 0 failures; discovery recall 1.000; idempotency passed.
- Offline site builds succeeded for `agent_memory`, `deep-research` and `engram`.
- `check_paper_scout_site.py`: **site/schema/link/exposure/workflow checks — 0 errors**.
- `check_generated_file_sizes.py` over `digests docs reports/paper_scout`: clean.
- `git diff --check`: clean. All three workflow YAML files parse.
- Snapshot preparation and restore verification: all three databases `integrity_check=ok`, performed locally with no upload.
- Legacy compatibility: all 646 historical assessments readable; legacy `coverage-v1` receipts retain their original contract.
- Secret scan over every working-tree change: no credential-shaped content introduced. No `.sqlite3`, snapshot, archive or PDF is tracked or staged.

Public artifact review confirmed that substantive changes are confined to the five assessed papers plus the aggregate index, CSV and library-quality files; all other churn is the `generated_at` build timestamp. Published cards expose the scientific decision, evidence IDs, coverage manifest and model identities, and contain no API key, request or response body, token count, cost figure, run identifier or raw execution record.

## O. Operational readiness

The manuscript coverage gate is ready: externally reviewed with zero blockers, merged, verified deterministically against 44 manuscripts with zero invariant violations, proven to represent the five formerly omitted pages, and proven to make zero model calls on known-incomplete input.

The promotion gate is **not** ready for operational use. The Batch-3 roster never produced a usable sample: eight of sixteen papers were manuscript-unavailable, one book has no scientific body, and SciHazard has no valid assessment at all. The continuation covered three papers, of which only two received scientific calls, yielding a single promotion. That is continuation evidence, not demonstrated generalization, and it was collected after a change to the manuscript-selection path. The original failures stand.

## History

```text
ORIGINAL_BATCH_3_GENERALIZATION_RESULT = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_CHECK = FAIL
BATCH_3_FIRST_PAPER_RECOVERY_V2_CHECK = PASS
BATCH_3_REMAINING_HOLDOUT_RESULT = FAIL
MANUSCRIPT_COVERAGE_GATE_READY: YES
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
```
