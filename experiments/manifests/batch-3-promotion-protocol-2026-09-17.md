# Batch 3: unseen high-precision promotion gate protocol (not executed)

Status: PREPARED ONLY. No roster selected, candidate identities inspected for selection,
manuscripts acquired for this experiment, or assessments executed. Execution requires
a separate authorized task after engineering and independent review are complete.

## Freeze and selection

1. Freeze the merged evaluator SHA, dependency lock/environment, configuration, both
   exact model IDs, prompts, response schemas, evidence addressing and price caps.
2. Freeze an input-state snapshot and a global identity exclusion set covering every
   prior assessment and every calibration, Batch-2, recovery, smoke or development paper.
   Resolve all known canonical aliases before exclusion. Exclude any paper whose identity
   or manuscript has influenced engineering. Synthetic fixtures are never candidates.
3. Only after freezing engineering, select up to ten never-assessed high-relevance,
   nonsuppressed papers per track (30 maximum). Order deterministically by SHA-256 of
   `batch-3-dual-promotion-v1\n` plus canonical identity, with canonical ID as tie-breaker.
   Freeze this rule before viewing candidate identities. Do not use predicted quality,
   manuscript availability, institution, venue, dates chosen for likely success, or
   convenience as selection filters. Empty slots remain empty; no replacement papers.
4. Save canonical IDs, alias exclusions, immutable candidate records, configuration and
   roster SHA-256 before acquisition/assessment. Do not select the roster in this task.
5. Before any paid call, refresh endpoint pricing and approve a batch ceiling. Reserve
   each request using its actual wire-byte bound plus output cap; unknown charges retain
   their reserve. Stop before the ceiling; do not silently drop stopped entries.

## Execution

Run the production two-model gate without code/config/prompt changes mid-batch. No
manual response corrections, selective reruns, provider/model substitutions, paper-level
patches or retry calls. At most one assessor and one independent adjudicator call per
available manuscript. Save canonical context, final structured responses, model identities,
request/response hashes, provenance receipts, timing and usage without hidden reasoning.
Preserve every historical row and main-library decision. Freeze all automatic outcomes
before observational audit; an unavailable or technical-pending paper remains in the
intention-to-assess denominator. Disagreement and rejected overclaims are normal scientific
non-promotion, never technical failures. No target admission/pass rate.

## Evaluation and audit

Report primary/adjudicator decisions, promotion, disagreement, scientific uncertainty,
unavailable manuscripts, integrity/protocol/transport failures, acquisition coverage,
calls, costs, latency, and every non-promotion reason by track. Technical failure requires
an observable machinery defect, not a missing method or contested scientific claim.

Audit every promotion against its full manuscript and exact citations. Audit predeclared
first/middle/last roster positions in each populated track and every integrity failure,
without editing outcomes. Record contribution, methods, evaluation, claims, limitations,
source integrity, independence and prestige exclusion. False promotion is the primary
failure of interest; false negatives are acceptable but observable. Any audited unsupported
promotion or cross-paper provenance contamination fails the experiment. Require zero
avoidable recurring technical defects; at most one isolated explained external failure
among 30 (or at most 5% for a smaller roster). A systematic failure cannot be excused by
meeting that rate. Report binomial uncertainty for observed promotion precision and audit
limitations. Zero promotions means precision is unestimated, not demonstrated success.

Separate engineering readiness from empirical generalization. Passing mocks does not
rewrite any historical FAIL. Any engineering response to Batch-3 evidence belongs to a
new version and a later unseen experiment, preserving this frozen Batch-3 result.
