# Batch 2: frozen out-of-sample protocol — 2026-09-17

Goal: evaluate whether the already calibrated scientific-quality screening
pipeline generalizes to previously unassessed high-relevance papers without
human repair. This is an observational evaluation, not an engineering loop.
Done when all frozen entries have outcomes, the predeclared sample and every
pass/insufficiency are audited, full validation and historical-integrity checks
finish, and changed public output is deployed once. Batch 3 is out of scope.

## Freeze

Evaluator: `82ecd6b577a420e14a569225b0442d9d679a0a08`, main, clean and current.
No source, configuration, prompt, rubric, eligibility or threshold edits are
permitted during this batch. All evaluator/configuration bytes are hashed in
[the protocol](../../experiments/manifests/batch-2-protocol-2026-09-17.json).
The same source tree passed 301 tests and full three-track validation in the
preceding completed task. This task makes no implementation change and will
not run `pr-review` to approve scientific data decisions.

The exact 28 calibration IDs and all 438 previously assessed canonical IDs are
excluded globally, with DOI/arXiv/title identity aliases also checked. Every
prior assessment is excluded, including metadata-only legacy assessments; none
is treated as a fresh unseen scientific subject. A consistent baseline preserves
559 assessment rows (294 / 218 / 47), their full payloads, the current 28 decisions
and all other runtime tables. Snapshot/restore bytes match.

## Deterministic selection

Use the existing offline research-library sequence: merge dashboard duplicates,
refresh the unchanged relevance rules, apply existing curation and quality
presentation, mark new papers at the fixed timestamp, and call
`_sort_latest_relevant`. Take the first up to ten per track with high relevance,
`not_assessed`, no explicit suppression and no prior-assessment identity. Ranking
uses the existing newness/relevance/date/score/title order. No source enrichment,
new discovery, venue/author judgment, PDF-availability filter or predicted-pass
selection is performed.

The frozen [roster](../../experiments/manifests/batch-2-roster-2026-09-17.json)
contains **10 agent_memory / 10 deep_research / 0 engram**, 20 distinct papers.
There are 220 / 58 / 0 eligible candidates respectively. Every high-relevance
Engram paper has prior assessment history; its missing slots remain empty.
All selected records are also high relevance in stored state. None has a manual
quality directive. None has cached manuscript text. Known manuscript URLs were
recorded only after ranking/selection; missing URLs never cause replacement.

Roster SHA-256:
`af89dc0d58a24b3e894a15794447e7af4ff96fde40989b70c7ab5e1b355e6d82`.
The exact UTF-8 file bytes are hashed; the separate `.sha256` file records the
digest. Roster, protocol and audit positions are persisted before assessment.

## Execution and costs

Production `reassess-quality` is called once per exact selected ID, with the same
LLM/full-text execution settings as final calibration:
`deepseek/deepseek-v4-pro-0813`, `quality-cross-section-v1`,
`scholarly-rubric-v1`, `scientific-gate-v1`, `block-evidence-v2`,
`cross-section-support-v1`, temperature 0, reasoning off and strict JSON schema.
No seed is supplied. No force, PDF override, manual import or output correction.
The normal acquisition/source order, extraction/selection, provenance, numerical
checks, conditional compatibility and one batched support verifier are unchanged.

Existing limits remain two shared assessor attempts and one verifier attempt,
without verifier retry. Output caps are 8192/4096; verifier input cap 250,000 bytes;
socket timeout 180 seconds. Up to two independent track workers may overlap.
Observer wrappers save requests/results, acquisition, selected text, canonical
context, call ledgers and rows while delegating unchanged to production functions.
They check the frozen files/roster and source association, and enforce at-most-once
execution. No hidden reasoning is retained. Raw payloads/cache/snapshots stay ignored.

Using checked same-day maximum endpoint token rates and planning assumptions of
60,000 input/3,000 output assessor tokens and 20,000/1,000 verifier tokens, all
20 assessable papers would cost approximately **$3.036**, or **$5.313** with a
shared assessor retry on every paper. These are estimates, not worst-case
promises. The existing **$10 operating ceiling** is enforced through a shared
reservation ledger before requests. Unknown-charge attempts keep their reserve.
Only Batch-2 inference is counted; no earlier development/review costs are included.

## Predeclared audits and decision criteria

Sample positions are **1, 6, 10** (first, floor(n/2)+1, last) for each populated
track; all papers when fewer than three, and none for empty Engram. These six
IDs/titles are fixed in the roster before any results are seen. After all automatic
outcomes are frozen, inspect this sample plus every pass and every insufficiency.
The audit is observational: topical fit, useful manuscript content, defensible
status, accepted claim grounding, numerical/context support, limitations,
calibration, false confidence and excessive conservatism. It cannot edit decisions.

There is no target pass rate. Technical success requires zero avoidable grounding,
protocol or coverage failures, zero manual corrections and unchanged history.
At most one explained isolated external technical failure among 20 (5%) may be
considered acceptably low, with no shared cause or systematic pattern; the
scientific audit can still fail the batch regardless of rate. A serious false
pass or systematic unsupported-claim pattern fails the evaluation. Manuscript
unavailability, genuine scientific uncertainty and genuine insufficiency are
valid outcomes, separately reported.

Isolated technical failures remain data and execution continues. Only a
catastrophic manuscript/provenance/input association, state-loss or secret issue
stops the batch. No patch-and-resume under this protocol is permitted. Budget
exhaustion pauses before another charge rather than silently dropping entries.

## Checkpoints

1. Persist exact implementation, baseline, exclusions, roster hash, cost bounds
   and audit sample. Verify all selected entries are genuinely unseen.
2. Execute the frozen production path. Preserve every outcome and concise
   provenance; freeze result hashes after completion. No output-driven tuning.
3. Audit the sample and all passes/insufficiencies, classify every entry, and
   aggregate selectivity, reliability and costs with explicit denominators.
4. Run complete tests, all three relevance/quality/discovery/idempotency checks,
   builds, sidecars, links, exposure/workflows, snapshot/restore, legacy checks
   and diff checks. Verify admission/review visibility and all prior histories.
5. Publish reports/state and deploy changed Pages once; verify public bytes and
   record exactly one PASS/FAIL generalization decision. Do not begin Batch 3.
