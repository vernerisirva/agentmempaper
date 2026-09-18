# Evaluation-independence recovery — 2026-09-18

**A general evaluation-independence dimension was added to the scientific promotion gate, reviewed to convergence by a non-Claude reviewer, merged, and rerun blind against the same frozen six-paper challenge set that the diagnostic failed. PEARL — the one paper in that set whose headline result is measured by the evaluator that drives its repair loop — is now withheld, and both scientific roles independently named the mechanism and the contradicting independent measurement. The four papers that should pass still pass, three of them evaluator-based. `EVALUATION_INDEPENDENCE_RECOVERY: PASS`. Production state is byte-identical, no unseen paper was consumed, and Batch 6 was not run.**

## A. The permanent prior result

This does not change and is not reinterpreted:

```text
BATCH_5_GENERALIZATION_RESULT = PASS
EVALUATION_INDEPENDENCE_DIAGNOSTIC = FAIL
```

The diagnostic report was untracked when this task began. It was read, left unaltered, and committed **first**, as `b5e68495e`, before any rubric change existed — so the FAIL is fixed in history ahead of the fix, and cannot later be reread as a PASS. Nothing in it was edited, softened or re-scored.

The rerun below is `EVALUATION_INDEPENDENCE_RECOVERY`. It is **not** a retroactive diagnostic pass. The diagnostic failed against the gate as it stood; that remains true permanently.

### Canonical state

| Item | Value |
|---|---|
| Starting canonical SHA | `b2bb86ca647c71fc6734813cf7f4eb54fdbee89d` — confirmed clean, `Already up to date` |
| Implementation branch | `add-evaluation-independence-gate` |
| Merge SHA | **`3acca4328276b1e33ae6075a8fbdf8f6cb275d40`** |
| Reviewed candidate | `e4654595b0adbd893288509eb24c89fec062c353` — equals the merged tree |
| `git status --short` at end | empty |

The host Xcode licence is still unaccepted, so `/usr/bin/git` exits 69; all Git work ran through a Homebrew Git shim containing **only** `git`, which avoids the Python shadowing that has previously made the suite look broken. No host setting was changed.

```text
GEMINI_API_KEY:     AVAILABLE   (private interactive shell; not inherited by this session)
OPENROUTER_API_KEY: AVAILABLE   (private interactive shell; not inherited by this session)
```

Neither value was printed, logged, hashed or partially revealed, and no project-local secret file was created.

## B. The scientific defect

Stated generally, not as a property of any one paper:

> A paper may optimize, train, select, repair, reward or otherwise adapt the system under study using an evaluator that is also materially reused to measure its headline outcome. The reported gain is then expressed in the currency it was optimized for, and the evaluator cannot independently certify the result it helped produce.

The mechanism is not specific to an LLM judge. A reward model, learned evaluator, automated grader, self-evaluation, heuristic score, synthetic labeller or model-generated validation criterion can serve either role.

The diagnostic's own reading of why the gate missed it is the sharpest statement of the defect:

> In every case the gate got right, the manuscript itself supplied explicit validation language — κ, ρ, "blinded", a named external grader. In the case it got wrong, the manuscript is silent, and the gate read silence as the absence of a problem rather than the absence of evidence.

The gate described the mechanism accurately and recorded it as a design virtue. It was a recognition failure, not a reasoning failure.

## C. The general requirement now implemented

Both roles answer an `evaluation_independence` dimension from the manuscript, independently:

| Field | Values |
|---|---|
| `optimization_signal` | prose, one or two sentences |
| `final_evaluation_signal` | prose, one or two sentences |
| `signal_reuse` | `independent` / `materially_reused` / `uncertain` / `not_applicable` |
| `independent_corroboration` | `present` / `absent` / `uncertain` / `not_applicable` |
| `corroboration_summary` | prose, one or two sentences |
| `corroboration_direction` | `supports` / `mixed` / `contradicts` / `unavailable` / `not_applicable` |
| `concern` | `none` / `moderate` / `major` |

Corroboration may be blinded human or expert assessment, inter-rater agreement, evaluator calibration against independent labels, a held-out or separately calibrated judge, an objective external metric, an established external benchmark, or another genuinely independent measurement. **The principle is independence, not a technology.** No evaluation technology is banned, and nothing requires human evaluation in every paper.

Three shapes are explicitly *not* circular, and are stated in the rubric so ordinary judge-based work is not pushed toward non-promotion:

- an evaluator used only to report a final outcome, with nothing optimized against it;
- an optimization loop whose headline outcome is established objectively — judged on that objective outcome;
- a paper with no adaptation loop and no evaluator-dependent headline claim.

Silence is handled explicitly: where the manuscript does not report the validation needed, the claimed independence is **unestablished**, which is scientific uncertainty and never evidence that no problem exists.

## D. Directionality — the limb that actually decides

The rubric requires each role to judge the *direction* of any evaluator-independent measurement, not merely its presence. A measurement that fails to corroborate the headline gain, or moves against it, is a major concern rather than supporting evidence.

This is the decisive limb, and the diagnostic said so in advance:

> PEARL would likely still have passed a rule that only asked "is validation evidence present?", because Gemini already counted MiniCheck as "external grounding checks". It is the direction of the independent number that is decisive.

The recovery confirms this exactly. Both roles declared PEARL's `independent_corroboration = present` — a presence-only rule would have cleared it. They then declared `corroboration_direction = contradicts`, and that is what withheld it. **The presence limb alone would have reproduced the original miss.**

Partial support is treated the same way as silence rather than as support: under reused or unresolved signals, `concern` may be `none` only when corroboration is both present and supporting.

## E. Rubric, schema and version changes

| Version | Before | After |
|---|---|---|
| `GATE_VERSION` | `dual-promotion-v2` | **`dual-promotion-v3`** |
| `ASSESSMENT_VERSION` | `quality-promotion-v1` | **`quality-promotion-v2`** |
| `rubric_version` | `scholarly-rubric-v1` | **`scholarly-rubric-v2`** |
| `INDEPENDENCE_CONTRACT` | — | **`evaluation-independence-v1`** |
| `RECEIPT_VERSION` | `canonical-response-v1` | unchanged, deliberately |
| Promotion rule (`agreement`) | Gemini PASS ∧ DeepSeek PASS ∧ evidence ∧ no blockers | **unchanged** |

The rubric and the response schema both changed, so the assessment and rubric versions moved with them. `RECEIPT_VERSION` did not, because the receipt *envelope* did not change and `response_binding` hashes that constant — moving it would invalidate the stored binding of every earlier receipt.

**Deterministic code decides no science.** `evaluation_independence_error` reads only the enum values a role declared. No manuscript text, prose field, keyword list or phrase match is consulted; a test varies the prose across "circular self-evaluation", "no concerns at all" and "." and asserts the outcome never moves. What the code enforces is that a role is held to the consequences of its own declared values:

- material reuse with corroboration anything other than present → `major`;
- independent evidence that contradicts, under reused or unresolved signals → `major`;
- reuse present or unresolved, without present-and-supporting corroboration → not `none`;
- a corroboration direction is reportable exactly when corroboration is present;
- **`major` cannot accompany that role's pass.**

The last rule is how the new dimension reaches promotion: through each role's own decision and the *unchanged* agreement rule, not by modifying it.

### Historical integrity

Rows written under `dual-promotion-v1` and `dual-promotion-v2` must not carry the dimension or its contract version, and are reread under the schema and contract that produced them. Their stored decisions are historical records and are never reinterpreted. Each gate wrote exactly one response schema, so the assessment version a row claims is now bound to its gate — a row can no longer borrow a newer schema version onto an older scientific contract, a gap the review found and which had been open.

All **667 stored rows** across the three databases load and revalidate; none carries the new dimension; all keep `scholarly-rubric-v1`.

### One consequence recorded rather than hidden

Because the rubric moved, a routine `reassess-quality` run no longer treats a historical **non-pass** row as current: **13 rows** across all tracks (12 `uncertain`, 1 `not_assessed`). **Zero stored passes** are affected — those remain excluded on their own. Per-run volume is unchanged and still bounded by `max_assessments_per_run` (5, or 4 for engram). Recurring assessment was **not** enabled.

Two read-only operator scripts were added, neither part of any run:

- `check_stored_assessments.py` — loads every stored row, revalidates completed promotion receipts under the gate that produced them, names the invariant a bad row breaks, and reports rather than repairs. Against the three real databases: **667 rows, 0 errors.**
- `probe_promotion_schema.py` — asks each provider whether it accepts the current strict schema, using a fixed prompt with no manuscript, evidence ID or content hash. A live run under `dual-promotion-v3` reports **0 errors**: both providers accept the nested dimension and return all seven fields.

## F. Tests

**505 tests pass** (444 before this task; no live model call in any of them). The §10 scenarios are covered explicitly:

| | Scenario | Covered by |
|---|---|---|
| A | clear circularity, no independent validation | not `none`/`moderate`; forced `major`; not promoted |
| B | same evaluator both sides | `major` surfaced; cannot accompany a pass |
| C | dependent evaluator + supporting blinded human validation | may pass |
| D | dependent evaluator + contradicting independent metric | forced `major`; not promoted |
| E | independent evaluator / external benchmark | no concern forced |
| F | evaluator only at final evaluation | not automatically circular |
| G | evaluator in the loop, objective headline outcome | judged on the objective outcome |
| H | missing information | never `none`; fail-closed, not assurance |
| I | historical schemas remain readable | v1 and v2 receipts load and revalidate |
| J | old stored assessments remain valid records | stored decisions survive reload unchanged |

Plus: the contract reads no prose; both roles carry an identical dimension; the adjudicator is instructed never to inherit; an earlier gate cannot borrow the contract and the current gate cannot omit it; an assessment version cannot be borrowed across gates; a pending technical outcome carries the contract with no role response; a contract violation costs exactly one fresh adjudication; the shipped track configs all resolve to the current versions; and the real `reassess-quality` selection path.

## G. PR, reviewer and merge

| Item | Value |
|---|---|
| PR | https://github.com/vernerisirva/agentmempaper/pull/40 |
| CI | `offline-validation` pass; `MERGEABLE` / `CLEAN` |
| Configured reviewer | `deepseek/deepseek-v4-pro-0813` — **failed to converge** |
| Escalated reviewer | `moonshotai/kimi-k3` — 17 calls, 16 verdicts |
| Final verdict | **PASS_WITH_NOTES, 0 blocking findings** |
| Unresolved blockers | **0** |
| Merge SHA | `3acca4328276b1e33ae6075a8fbdf8f6cb275d40` |

No Claude-family model reviewed this change. DeepSeek consumed all 16,384 completion tokens on reasoning and returned zero visible tokens — the same documented failure mode as the previous two cycles — so the established escalation applied.

Review converged over sixteen Kimi verdicts. Two rounds returned **CHANGES_REQUIRED**; both were resolved:

- **Round 10** — that `config/tracks/engram.yaml` might still pin the retired versions. **Verified false positive**: engram pins neither value and inherits the bumped defaults. Rather than answer in prose, every shipped track config is now asserted to resolve to the current versions, so a stale pin fails a test.
- **Round 11** — a real defect in the operator check added earlier in the cycle: a payload that was valid JSON but not an object escaped the handler and aborted the run. Fixed and tested.

Substantive findings fixed rather than accepted:

1. material reuse with *unresolved* corroboration was unconstrained while the weaker case was not;
2. **mixed** independent support was treated more leniently than silence — it now is not;
3. unresolved corroboration under admitted reuse escaped the major rule;
4. an assessment version could be borrowed across admission gates;
5. the dimension's normative text was stated twice in one system message, costing tokens and inviting drift.

Findings declined, with reasons: the reviewer twice suggested weakening or removing the widened legacy-gate guard, and once suggested moving or trimming the committed diagnostic report. The guard was kept and its basis made runnable rather than asserted in a comment. The report stays: it is the permanent record this task exists to answer, and it holds credential variable names and availability only, never a value.

**Honest limitation.** `paper_scout/promotion_protocol.py` exceeds the reviewer's 18 KB per-file cap and was truncated in every round, so `validate_receipt` was never directly visible to the reviewer. The oversized test module was split into three so that side could be read in full, but the protocol file could not be without distorting its design. The properties the reviewer could not verify are pinned by tests instead — each gate version revalidates under its own response shape, in both directions — and were checked directly here. This is a genuine limit on review coverage and is recorded as one.

One non-blocking note remains open by choice: the probe conflates a returned-model alias with a schema rejection in its *message* (the fail-closed behaviour is correct and matches the production gate). Fixing it would have meant merging a tree the reviewer had not seen; the merged tree is exactly the reviewed candidate `e4654595b`.

## H. The blinded six-paper recovery

The **same** frozen set, taken verbatim from the diagnostic — none added, removed, reordered or substituted. All six resolved in the copied state carrying their historical labels exactly as the diagnostic recorded them, and all six re-acquired manuscripts produced **654 context blocks**, identical to the diagnostic's count.

### Blinding

Unchanged and structural, not promised. Each request is built from manuscript-derived content only. No historical quality label, promotion status, prior rationale, prior blocking reason, diagnostic classification, or any hint that these papers were selected for evaluator concerns can reach either model. No paper name or special case appears in any production prompt — asserted by a test that scans the rubric for paper, system and dataset names. The adjudicator receives the primary's current output, which is the ordinary production contract, and is explicitly instructed never to inherit its independence judgment.

### Isolation

Copied databases, copied full-text cache, and report and digest output redirected into scratch. Production hashes were captured before the first call and rechecked after the first paper and at the end.

### Frozen outcomes, recorded before any history was retrieved

```text
FROZEN_RECOVERY_SHA256: 4a9483430ae856d1320254f81193fe95c15159c74a1974f24c7b8ea9abf98c80
```

| # | Paper | Gemini | DeepSeek | Blockers | Promotion | Outcome | Calls |
|---|---|---|---|---:|---|---|---:|
| 1 | A New Paradigm | `uncertain` | `uncertain` | 4 | **not promoted** | success | 2 |
| 2 | **PEARL** | **`uncertain`** | **`uncertain`** | **3** | **not promoted** | success | 2 |
| 3 | AREX | `pass` | `pass` | 0 | promoted | success | 2 |
| 4 | Closing the Consistency Gap | `pass` | `pass` | 0 | promoted | success | 2 |
| 5 | Is Deep Research Reliable? | `pass` | `pass` | 0 | promoted | success | 2 |
| 6 | AppliedScientist | `pass` | `pass` | 0 | promoted | success | 2 |

**Promotions 4 of 6. Retries 0. Manual corrections 0. Technical failures 0.** Every paper: coverage `pass`, provenance `pass`, gate `dual-promotion-v3`, contract `evaluation-independence-v1`, `reasoning_tokens = 0`. **654 context blocks, 0 unknown evidence ids, 6 distinct context ids**, every context hash equal to the assessment's source hash and to the acquisition identity.

### What the two roles declared

| Paper | `signal_reuse` | corroboration | direction | concern |
|---|---|---|---|---|
| A New Paradigm | `not_applicable` | `not_applicable` | `not_applicable` | none |
| **PEARL** | **`materially_reused`** | **`present`** | **`contradicts`** | **major** |
| AREX | `independent` | `present` | `supports` | none |
| Closing the Consistency Gap | `independent` | `present` | `supports` | none |
| Is Deep Research Reliable? | `independent` | `present` | `supports` | none |
| AppliedScientist | `independent` | `present` | `supports` | none |

Primary and adjudicator agreed on every field of every paper, having reached them separately.

The adjudicator's PEARL blocking reasons, unedited:

> 1. The headline strict-gate gains are established by the same CG/REA judge protocol that conditions the iterative semantic repair loop, so the reported improvement is measured in the currency it was optimized for.
> 2. The only reported independent measurement, MiniCheck source-grounding, does not corroborate the headline gain: support rate falls from 0.584 to 0.557 and no-evidence rate rises from 0.141 to 0.184 after repair.
> 3. The manuscript does not report blinded human or expert assessment, inter-rater agreement, judge calibration against independent labels, or another genuinely independent measurement supporting the strict-gate improvement.

Reason 2 is the directionality limb, reached from the manuscript alone, reproducing the `.584 → .557` movement the diagnostic identified as decisive.

## I. Scientific audit

The same four-label observational classification, against the recovery outcome:

| # | Paper | Observational classification | Diagnostic gate | Recovery gate | Correct now? |
|---|---|---|---|---|---|
| 1 | A New Paradigm | no evaluator-dependent claim | not promoted | not promoted | yes |
| 2 | **PEARL** | **`CLEAR_EVALUATION_CIRCULARITY`** | **promoted — miss** | **not promoted** | **yes** |
| 3 | AREX | `INDEPENDENT_EVALUATION_STRONG` | promoted | promoted | yes |
| 4 | Closing the Consistency Gap | `EVALUATION_DEPENDENCE_BUT_ADEQUATELY_VALIDATED` | promoted | promoted | yes |
| 5 | Is Deep Research Reliable? | `INDEPENDENT_EVALUATION_STRONG` | promoted | promoted | yes |
| 6 | AppliedScientist | `EVALUATION_DEPENDENCE_BUT_ADEQUATELY_VALIDATED` | promoted | promoted | yes |

**Six of six. The single miss is corrected and nothing else moved.** PEARL was treated exactly like any other selected paper: same protocol, same blinding, same prompts, no special case.

Three observations recorded honestly rather than smoothed over:

1. **A bookkeeping difference on the two validated-dependence papers.** The diagnostic classified AppliedScientist and Closing the Consistency Gap as evaluator-*dependent* but adequately validated. Both roles instead declared `signal_reuse = independent`, on the grounds that the headline signal is a held-out or external measurement — the Stanford Reviewer "never exposed to the scientist during revision" (5.50 → 6.15), and the standard AppWorld grader. Both readings are defensible and both reach the same outcome, but they differ on the reuse limb, and the consequence is that the `materially_reused + present + supports` cell — dependence carried by supporting corroboration — **was never exercised in this set**. Scenario C is covered by deterministic tests, not by live evidence here.
2. **No over-conservatism appeared, but the set cannot prove its absence.** Four of six promoted, three of them evaluator-based, including one whose optimization signal is a model evaluator. Only the paper that should have changed did.
3. **Six papers remain a small sample**, enriched for evaluator coupling by construction. This establishes that the targeted blind spot is addressed on the data that exposed it. It does not establish generalization.

## J. Production integrity

| Check | Result |
|---|---|
| Production DB SHA-256, before vs after | **byte-identical**, all three |
| Production assessment rows | 348 / 271 / 48 = **667**, unchanged |
| Production papers | 18,343 / 2,395 / 306, unchanged |
| Latest production `assessed_at` | `2026-09-18T18:41:55` — the Batch-5 timestamp, unmoved |
| `dual-promotion-v3` rows in production | **0** |
| Recovery rows | exist only in the scratch copies (1 agent_memory, 5 deep_research) |
| Production full-text cache | **0** files written |
| Public generated files | `docs/` rebuild changes `generated_at` only; no published record rewritten |
| Committed daily quality report | unchanged; all runs redirected |
| Unit suite | **505 tests, OK** |
| Relevance, all three tracks | precision 1.000, recall 1.000 |
| Quality/promotion fixtures | 8/8 both tracks |
| Discovery recall | 1.000 both tracks |
| Site / schema / link / exposure / workflow | **0 errors** |
| Stored-assessment check | 667 rows, **0 errors** |
| Snapshot / restore | `integrity_check=ok`, 348 / 271 / 48 restored |
| Workflows, manifests, configs | all parse |
| `git diff --check` | clean |
| Pages deployment | **none performed** |

**No recovery result was published as an assessment.** PEARL's public record is unchanged: this recovery did not withhold it in production any more than the diagnostic promoted it there. Both exist only on copied state and in these reports.

## K. Cost

### Engineering review

| Item | Calls | Cost |
|---|---:|---:|
| DeepSeek review, non-convergent | 1 | $0.06471914 |
| Kimi K3 reviews (16 verdicts, 1 contract failure) | 17 | $2.03903650 |
| **Engineering review subtotal** | **18** | **$2.10375564** |
| Provider schema probes (captured) | 4 | $0.00147761 |

### Recovery diagnostic

| Provider / model | Calls | Prompt | Completion | Reasoning | Monetary |
|---|---:|---:|---:|---:|---|
| google / `gemini-3.8-flash` | 6 | 238,261 | 6,720 | 0 | **UNKNOWN**, `covered_by_msc_allocation` |
| openrouter / `deepseek/deepseek-v4-pro-0813` | 6 | 220,866 | 3,885 | 0 | **$0.16644656** (`provider_reported`) |

| Item | Value |
|---|---|
| Known money this task (OpenRouter only) | **$2.27167981** |
| Gemini | 238,261 in / 6,720 out — **monetary cost UNKNOWN / MSc allocation** |
| Prior cumulative | $6.99061030 |
| **Cumulative against the $10 ceiling** | **$9.26229011** (remaining **$0.73770989**) |

One later live probe call pair was not separately captured; it is bounded by the captured per-probe pair above (~$0.0015), so the cumulative figure is accurate to well under a cent. The Google endpoint reports no charge and this project has not established the allocation's effective rate, so **no monetary amount is fabricated and Gemini is not assumed to be free.**

**The engineering review dominated this task at $2.10 across 18 calls — roughly thirteen times the recovery run itself.** Sixteen review rounds was more than the change warranted; the last several returned only cosmetic notes on operator tooling added in response to earlier notes. A future cycle should cap review rounds explicitly. **Remaining headroom is $0.74, which is not enough for a Batch 6 of any size** — that budget must be raised or replenished before an unseen batch can run.

Cost guard respected: **6 historical papers, the stated maximum. No unseen paper was consumed. Batch 6 was not run.**

## Readiness

The targeted scientific blind spot is addressed on the data that exposed it. The gate now reasons explicitly about evaluation independence, both roles reach that judgment separately, the direction of independent evidence decides rather than its presence, and the one clearly circular paper in a set enriched for this failure mode is withheld with its mechanism named. Judge-based work is not rejected as a class: three of the four promotions rely on a model evaluator somewhere.

What is **not** established is generalization. This is six already-seen papers, selected by a rule built to surface exactly this coupling. The new rubric has never run on an unseen population, the `materially_reused + present + supports` case has no live evidence, and one bookkeeping difference against the diagnostic's own reading is recorded above. A fresh unseen Batch 6 under `dual-promotion-v3` is required before any of this counts as generalization — and it was deliberately not run.

Recurring production assessment was not enabled.

---

```text
BATCH_5_GENERALIZATION_RESULT = PASS
EVALUATION_INDEPENDENCE_DIAGNOSTIC = FAIL
EVALUATION_INDEPENDENCE_RECOVERY: PASS
QUALITY_PROMOTION_GATE_READY_FOR_BATCH_6: YES
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
```
