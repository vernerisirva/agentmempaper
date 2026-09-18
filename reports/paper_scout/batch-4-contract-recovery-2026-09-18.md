# Batch 4 — adjudicator contract recovery and population reproducibility — 2026-09-18

**Batch 4 stays a FAIL. Two machinery defects it exposed are fixed: an adjudication could pass a paper and return blocking reasons at the same time, and the eligible population could not be rebuilt. The one paper wrongly held back was reassessed under the unchanged gate and promoted on a structurally valid adjudication. Nothing scientific changed — not the rubric, the threshold, the model pair, the coverage gate or the evidence semantics — and no stored row was rewritten.**

## A. The Batch-4 verdict is unchanged

```text
BATCH_4_GENERALIZATION_RESULT = FAIL
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE = NO
```

Batch 4 put ten unseen papers through the frozen gate and one of ten outcomes was wrong through machinery. That is what the batch measured, and recovering the affected paper afterwards does not change what the batch found. The original roster, the stored model responses, the original promotion decision, the audit report, the cost records and the assessment history are all retained exactly as written. Everything here is later recovery evidence beside them, never a replacement.

Recorded in [`batch-4-promotion-gate-evaluation-2026-09-18.md`](batch-4-promotion-gate-evaluation-2026-09-18.md); nothing in that report was edited.

## B. Root cause

The adjudicator returned this, on `arxiv:2609.03727`:

```json
{"promotion_decision": "pass",
 "blocking_reasons": ["No blocking reasons: the manuscript's scoped survey contribution, ..."]}
```

`agreement()` requires `not adjudicator['blocking_reasons']`, so any non-empty array blocked promotion whatever it contained. Both scientific roles had passed the paper; the sentence was the only thing standing between it and the library.

The response was **schema-valid**: `blocking_reasons` was typed as an array of non-empty strings with no relation to `promotion_decision`, so nothing rejected it and no retry fired. Its footprint reached publication as well, because `promotion_gate.py` assigns `base['concerns'] = adjudicator['blocking_reasons']`: the review card's sole stated scientific concern was a sentence saying there were none.

Reproduced against the pre-fix code before anything was changed: schema-valid, accepted by `validate_response`, one adjudicator call, `agreement()` False, and `agreement()` True on the identical response with an empty array. The defect was systematic, not incidental — it recurs whenever the adjudicator phrases "no blockers" as prose.

## C. The structural invariant

```text
promotion_decision == 'pass'  ->  blocking_reasons == []
blocking_reasons != []        ->  promotion_decision != 'pass'
```

`adjudicator_consistency_error()` compares the decision against the array. It reads no prose, matches no phrase list and interprets no English, so the wording of a reason — a "none" sentinel or a real objection — never changes an outcome. `uncertain` with no blocking reasons stays an ordinary non-promotion exactly as before, so no scientific behaviour is altered.

The conditional is not expressible in the strict structured-output subset both providers accept, so it is stated where the model can read it and enforced where it cannot be evaded:

- the adjudicator schema's `promotion_decision` and `blocking_reasons` descriptions,
- the adjudicator instruction and the retry instruction,
- runtime validation in `parse_response`, as its own contract step over the fully validated response.

The instruction says explicitly that this is an output-format requirement that makes promotion neither easier nor harder.

## D. Bounded recovery

A violation is an ordinary output-contract failure, so the existing bounded policy applies unchanged:

| attempt 1 | attempt 2 | result |
|---|---|---|
| consistent | — | used normally |
| contradictory | consistent | attempt 2 used |
| contradictory | contradictory | protocol failure, not promoted |

One fresh adjudication of the original manuscript and primary assessment, never the rejected output fed back, and no third attempt. Nothing is repaired: `blocking_reasons` is never emptied, `pass` is never rewritten to `uncertain`, and the English is never read. Both attempts are retained with their raw content, attempt binding, usage and cost.

## E. Historical rows keep their own contract

`RETRY_POLICY` is versioned to `adjudicator-contract-retry-v2`, and `attempt_binding` now carries the receipt's own policy instead of the current module constant — otherwise bumping the version would have invalidated every stored attempt binding. A receipt written before the contract is reread under the contract that produced it.

Verified against the live databases at the time of the fix, before the recovery added a row: **656 stored assessments parse and all 17 completed dual-promotion receipts revalidate**, including row 343, the contradictory one. After the recovery the figures are 657 and 18.

## F. Public withholding, then restoration

A stored decision whose adjudication violates the contract is withheld from publication rather than rendered. Both halves of such a decision are machinery artifacts: the outcome is wrong and the "reason" blocks nothing.

While withheld, the paper stayed relevant and reviewable, its promotion state published as `not_assessed`, and the contradictory sentence appeared nowhere in the public output. The stored row was never touched, the check reads structure rather than wording, and a valid reassessment publishes normally — which is what has now happened, with no list of ids to maintain.

Exactly one paper was ever affected. A scan of all 656 stored assessments across the three tracks found one contract violation: row 343.

## G. The eligible population could not be rebuilt

Batch 4's second defect: the frozen population commitment did not reproduce for `agent_memory` or `deep_research`. The construction lived in an uncommitted analysis script and the commitment stored only a digest, so neither membership nor count could be audited.

`paper_scout/batch_population.py` is the single committed path that replaces it.

**Ordering** reuses the offline site ranking the published library is ordered by — duplicate merge, rule refresh, curation, quality presentation, newness, then the shared sort key. Network date enrichment is deliberately skipped, because a network answer cannot be reproduced. The build time is pinned explicitly and required, since the newness key reads it.

**Identity** is namespaced, so a DOI only matches a DOI and a title only matches a title:

| namespace | rule |
|---|---|
| `canonical` | the stored canonical key, verbatim |
| `doi` | lowercased, `doi.org/` or `doi:` prefix removed |
| `arxiv` | version suffix, `abs`/`pdf` URL and `.pdf` removed |
| `openalex` | `openalex.org/` prefix removed |
| `semantic_scholar` | the stored identifier, stripped |
| `arxiv` (derived) | parsed out of the canonical id, the DOI or the URL |
| `title` | lowercased alphanumeric, only above the existing length floor |

Matching is exact equality of namespaced strings. No fuzzy or substring title matching is introduced, and identities are derived only from fields that name the manuscript in hand — a raw source record cites other papers, and attributing a neighbour's arXiv id would have dropped an unrelated paper out of the population.

**Exclusions** come from three declared sources — a persisted assessment row in any track, an active suppression or a curation `suppress_for_quality` directive, and any supplied frozen roster — and every removed candidate records its reason, the identity that matched and where that identity came from. Exclusions are always read from **every** track whatever is being built, so restricting a build narrows what the manifest contains, never what it excludes.

## H. The manifest

Persisted before any model call, carrying the ordered identifiers themselves and not only a digest:

- the ordered eligible canonical ids per track, and each candidate's identities
- an exclusion reason, matched identity and source for every removed candidate
- the manifest and population versions, the identity policy and the exclusion sources
- every input: state, curation and digest locations per track, the pinned build time, the tracks scanned for exclusions, any track lacking a database, and each frozen roster by path **and content hash**
- a per-track `population_sha256` over the newline-joined ids in selection order, a `manifest_sha256` over all reproducible content, and the code SHA

`code_sha` and `created_at` sit outside the hash, so the same frozen state rebuilds byte-identical content from a later commit that does not change ranking, while any change to the population itself is caught. Order is inside the commitment, because selection takes a prefix of the list.

`batch-population --verify` rebuilds from the manifest's own recorded tracks, exclusion scope, build time and rosters — none of which can be narrowed from the command line — and compares the ordered ids item by item, the per-track digests, the manifest digest and the source block.

Against the current frozen state:

| track | ranked | eligible | excluded | reproduced |
|---|---:|---:|---:|---|
| agent_memory | 319 | 198 | 121 | yes |
| deep_research | 133 | 38 | 95 | yes |
| engram | 8 | 0 | 8 | yes |

Identical ordered ids, identical per-track digests and an identical `manifest_sha256` on rebuild, including across two different code SHAs.

## I. Tests

Added 40 deterministic tests; **444 total, all pass**. No test makes a live model call.

Adjudication contract: `pass` + `[]` valid; `pass` + non-empty invalid; non-pass + reasons valid; the check is structural across four different wordings; the invariant appears in the schema and both instructions; a contradictory first response costs exactly one fresh retry whose user message is byte-identical and never contains the rejected output; a valid second response is accepted; a second contradictory response is a protocol failure with no promotion; neither attempt is repaired, reinterpreted or discarded; the receipt records both attempts with bindings, providers and cost; a stored contradictory receipt fails closed under the new policy while the identical row under the old one stays readable; `agreement()` is unchanged.

Publication: a known-invalid decision is withheld while the paper stays reviewable and the sentence appears nowhere; a consistent decision publishes normally.

Population: manifest round-trip with identical ordered ids and digest; verification failing on a tampered list, on a digest without its list, on other inputs and on an unverifiable track scope; alias exclusion by canonical id, DOI, arXiv id, OpenAlex id, URL-derived arXiv id and normalized title across tracks; title matching staying narrow; namespaces keeping unrelated fields apart; a cited paper's arXiv id not excluding that paper; a restricted build still honouring another track's assessment; every removed candidate accounted for; and the command end to end through the entry point.

## J. Independent review

Claude Code implemented, so the reviewer was non-Claude throughout. DeepSeek ran first and exhausted its completion budget with no accepted verdict; under the established bounded policy this escalated to **Kimi K3** — not to a Claude model, per the non-Claude requirement.

| round | verdict | blockers |
|---|---|---:|
| 1 | CHANGES_REQUIRED | 1 |
| 2 | CHANGES_REQUIRED | 1 |
| 3–7 | PASS_WITH_NOTES | 0 |

Both blockers were real, reproduced before being fixed, and each fix is covered by a test verified to fail against the previous behaviour:

1. **`batch-population` raised `NameError`** through `python3 -m paper_scout.cli`, because the handler was defined after the entry-point guard. `python3 -m paper_scout` had masked it.
2. **A track-restricted build narrowed its exclusions**, so a manuscript already assessed under a track that was not being built could have been reassessed under a second canonical id.

Notes fixed as well: an empty `canonical:` identity two unrelated curation rules would have shared; `--roster` and `--population-track` silently ignored under `--verify`; an unpinned default build time baking wall-clock into a commitment; an absent exclusion database passed over silently; free-text arXiv inference over a raw source record; curation rules matched by raw string equality; the contract check sitting inside the parse `try`; and an unverifiable manifest failing with a bare `KeyError`.

One note is accepted rather than fixed: an assessment row whose canonical id has no paper row contributes only the identities derivable from that id. There is no further identity to extract without a row, and the manuscript is still matched whenever it exists in any track.

**Merged:** [PR #39](https://github.com/vernerisirva/agentmempaper/pull/39), merge commit `8a99babed743f4ade2b23f8ac03b44a4283c6373`, CI `offline-validation` green, mergeable and clean, reviewed head identical to merged head.

## K. BATCH_4_CONTRACT_RECOVERY

One paper, reassessed after the merge under the same Gemini primary, the same DeepSeek adjudicator, the same rubric and the same promotion gate. No manual correction and no code change during the recovery.

The first attempt returned the stored assessment from cache on a manuscript-hash match without calling either model; the reassessment was rerun with `--force`, which refetched the manuscript.

| | original (row 343) | recovery (row 346) |
|---|---|---|
| assessed at | 2026-09-18T09:50:11Z | 2026-09-18T13:21:19Z |
| retry policy | `adjudicator-contract-retry-v1` | `adjudicator-contract-retry-v2` |
| manuscript hash | `67cd4048…fbfcca92` | `67cd4048…fbfcca92` (**identical**) |
| primary | `pass` | `pass` |
| adjudicator attempt 1 | `pass` + 1 blocking reason | `pass` + `[]` |
| retry | none fired (contract absent) | **none needed** |
| calls | 2 | 2 |
| promotion | **not promoted** | **promoted** |
| receipt | validates | validates |
| provenance | pass | pass |

The recovery ran against the **byte-identical manuscript**, so the two results are directly comparable. The adjudicator returned a structurally consistent response on its first attempt, which means its scientific judgment was `pass` both times: the original non-promotion was entirely an output-format artifact, and no retry was needed to establish that.

Receipt `canonical-response-v1`, run `e7e4507a2f574215af20dc112f6e5414`, primary `gemini-3.8-flash` at google, adjudicator `deepseek/deepseek-v4-pro-0813` at openrouter, model-pair provenance intact, both attempts bound.

## L. Historical integrity

Compared row by row against a snapshot taken before the recovery:

| | before | after | delta |
|---|---:|---:|---:|
| agent_memory | 342 | 343 | +1 |
| deep_research | 266 | 266 | 0 |
| engram | 48 | 48 | 0 |

**No pre-existing row changed, none was removed, and exactly one was added.** Row 343 is byte-identical to its pre-recovery form and still carries both its `pass` and its blocking reason. The other two tracks are untouched. All 657 stored rows parse and every completed dual-promotion receipt revalidates.

## M. Publication

Published: the regenerated three-track site and sidecars, and this report. The review card for `arxiv:2609.03727` now shows the valid recovered outcome — admitted to the main library, promotion `pass`, no concerns — and the contradictory sentence appears nowhere in the public output. The original invalid attempt remains internal and auditable.

The generated diff is large because the previous automated site build ran without the assessment databases and stripped quality data from the public library; this build restores it from stored state alongside the recovery.

Not published, and still excluded by `.gitignore`: the assessment databases, runtime state, snapshots and raw execution records. No credential-shaped string, `thought_signature` or `reasoning_content` appears in any published artifact.

## N. Cost

| item | value |
|---|---|
| Recovery — DeepSeek adjudicator | **$0.05059032** (37,081 in / 415 out) |
| Recovery — Gemini primary | **UNKNOWN**, `covered_by_msc_allocation` (40,123 in / 975 out) |
| Cumulative scientific inference | $6.48473717 → **$6.53532749** (remaining $3.46467251 of $10) |
| Independent engineering review | $0.92860200 over 10 rounds, tracked separately |

The Google endpoint reports no charge and this project has not established the allocation's rate, so the usage is recorded in exact tokens and no monetary amount is invented.

## O. Validation

| check | result |
|---|---|
| Unit suite | **444 tests, OK** |
| Relevance validation, all three tracks | precision 1.000, recall 1.000, 0 FP, 0 FN |
| Quality/promotion fixtures, all three tracks | 8/8 passed |
| Discovery validation | recall 1.000 (6/6, 4/4, 4/4) |
| Idempotency, all three tracks | passed |
| Site builds | all three built offline |
| Site/schema/link/exposure/workflow checks | **0 errors** |
| Generated file sizes | within guard |
| Workflow YAML and manifests parse | 3 YAML, 12 JSON, OK |
| Database integrity | `ok` on all three tracks |
| Legacy compatibility | 657 rows parse; `dual-promotion-v1` and retry-policy-v1 rows readable |
| Population manifest | reproduces exactly, all three tracks |
| Secret scan | 0 credential-shaped strings, 0 `thought_signature`, 0 `reasoning_content` |
| `git diff --check` | clean |

The unit suite needs Homebrew Git on `PATH`: the host's Xcode licence is still unaccepted, so the system Git exits 69 and one test that initialises a temporary repository fails for purely environmental reasons. No host setting was changed.

## P. What is still not established

The gate's **discriminative power remains untested**. Batch 4 had both roles pass all ten papers, and the recovery added a further unanimous pass. Nothing here shows the gate can reject weak work.

This was **not** addressed by making the rubric harsher or by tuning prompts to manufacture disagreements. The rubric, the threshold, the model pair and the evidence semantics are all unchanged, and the only prompt addition states the structural output contract. The absence of observed discrimination is recorded as a scientific validation limitation, to be tested by a future unseen batch against the unchanged gate.

Batch 5 was **not** selected and **not** run. Recurring assessment was **not** started.

## Verdicts

```text
BATCH_4_GENERALIZATION_RESULT = FAIL
BATCH_4_CONTRACT_RECOVERY_CHECK: PASS
BATCH_POPULATION_MANIFEST_REPRODUCIBLE: YES
QUALITY_PROMOTION_GATE_READY_FOR_BATCH_5: YES
QUALITY_PROMOTION_GATE_READY_FOR_OPERATIONAL_USE: NO
```

`READY_FOR_BATCH_5` is a statement about the machinery only: the contradictory contract is fixed and tested, the population is reproducible before any model call, and no known systematic implementation defect remains. It is not a statement about scientific validity.

`READY_FOR_OPERATIONAL_USE` stays **NO**. Operational readiness requires an unseen generalization test passed with no engineering changes during it, and the only such test so far is Batch 4, which failed. Engineering work has happened since, which is precisely why another unseen batch is required rather than optional.

**Private remote durable-state storage remains an unresolved operational backlog item.** The configured mechanism still publishes to a public GitHub release, which is unacceptable for private assessment state, so snapshots are kept and verified locally only. A visible consequence is that automated site builds run without the databases and strip quality data from the published library until a local build restores it.
