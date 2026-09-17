# Cross-section compatibility: preflight — 2026-09-17

Goal: let legitimate, atypically located body evidence reach the existing
substantive verifier without making body membership establish claim support.
Scope: claim compatibility and deterministic regressions. Acquisition, selected
manuscript context, rubric, numbers, discovery, relevance, admission and publication
status are unchanged. Done when the reviewed code is merged, exactly Real Science
is automatically reassessed once, all 28 current decisions are audited, and the
readiness criteria and conditional publication are reported. Batch 2 is excluded.

Baseline main `566b6c0a300ee1d678f7910effd1a8d11070ea47` was clean/current and
includes PR #30. A consistent backup preserves 558 historical assessments
(294 / 217 / 47); backup/restore bytes match. The bounded
[execution manifest](../../experiments/manifests/cross-section-2026-09-17.json)
reserves $5.4271976 under the existing approved $10 ceiling.

## Failure reproduced before editing

Cached source SHA-256:
`d2354a02730a0300957fa07f9d72b200e43aaf9addfdf30dbdee65eb3b585651`.
Rebuilt context:
`dc6e037d4780825452a9074c78c1cec2968107d9b981bb57ec765e172912be57`.
Both match the saved assessment exactly. All cited IDs resolve in that context.

The methodological-rigor source claim is: “The evaluation design includes
full-sized and smaller-scope prompts, multiple independent runs, and comparison
with general-purpose AI systems.” Its explanation attributes a structured
comparative methodology to prompt types, frameworks and reproducibility runs.
It cites `Edc6e037d47808254-B0013` and `Edc6e037d47808254-B0014`.

B0014 has Introduction role, pages 2–3, and content hash
`4559d30dd6b1cce9d44f60f5c32532042fe3f4ca6de45a3a78da9cb26c5de9c9`.
The complete canonical snippet, exact spans and original rejection trace are in
[the regression fixture](../../tests/fixtures/cross_section_real_science.json).
Manual source inspection confirms that its figure caption describes a real-life
scientific task, full and smaller prompts, five advanced AI frameworks, and
smaller-scope runs across specialized/general-purpose systems, each up to four
times independently. B0013 supplies the full-sized prompt/general-purpose
comparison context. B0014 also contains extraction carryover from the preprint
footer; that boilerplate is not itself scientific support.

Layer A passed. In `evidence_semantics.eligibility_decision`, Introduction is not
a direct method role, and the finite method regex did not match B0014. The
`body_without_compatible_content_cue` decision returned false. The `all(eligible_for)`
branch in `quality_llm.validate_block_quality_response` raised a reference error.
`assess_with_optional_quality_llm` consequently skipped its verifier. There were
zero verifier calls for that proposal. A separate old presentation explanation
refers to Table 2 without that number in its cited block; the numeric check still
rejects it. This task does not repair or replay the old proposal.

## Three explicit layers

- A: resolve canonical IDs, context/source identity, hashes and manuscript spans.
  Hard provenance failures, excluded sections and prohibited Abstract uses fail.
- B: `hard_ineligible`, `directly_compatible`, or
  `requires_support_verification`. Existing classified Methods/Results/Limitations
  provide direct signals. Atypical body—including unclassified System Design,
  Introduction and Appendix method passages—gets conditional candidacy. No
  section-classifier/context-ID change or keyword accumulation is needed.
- C: the unchanged single batched verifier checks each complete claim/explanation
  against its own canonical snippets, plus the existing narrative union. Every
  accepted claim still needs supported verification. Unsupported/uncertain,
  missing/malformed verification, or deterministic numeric contradiction cannot
  establish support. Quantity/unit matching stays deterministic; metric, context,
  comparison and interpretation remain explicit verifier responsibilities.

`compatible` continues to mean a direct section signal; conditional candidacy
never sets it true. A separate candidate predicate permits Layer C. Audit rows
record fallback requirement, final resolution and acceptance. No new model,
per-claim request, retry or second assessment pipeline is introduced.

## Validation and scope accounting

301 offline tests pass (289 existing, 12 new). New regressions preserve actual
B0014 source/hash/spans, accept supported fallback, reject unsupported/uncertain
fallback, fail closed on verifier errors, test cross-role and hard exclusions,
retain direct roles, reject wrong quantities/metrics, and verify exactly one
batched call for direct and conditional proposals. Earlier cue-based regression
expectations now distinguish candidacy from direct compatibility. All existing
foreign ID/context, percentage normalization and legacy tests pass.

All three relevance, quality, discovery, idempotency and offline build checks,
sidecar/link/exposure/workflow checks, size limits, snapshot/restore, legacy
restoration and unchanged database bytes pass. `git diff --check` passes.

An offline audit of the latest original-28 records finds five v2 records and 50
accepted source blocks with explicit roles; none becomes hard-ineligible. Only
Real Science has reference errors and lacked verification. Holding those stored
proposals fixed, the gate change would allow **one additional batched verifier
call**; already verified records add zero calls, and unavailable/legacy records
are not reassessed. This is a reachability estimate, not a prediction of semantic
outcomes or a replay of all 28. The other 27 decisions and all histories stay fixed.

## Authorized execution boundary

Independent `pr-review --base origin/main` uses at most two DeepSeek calls,
then at most two already-authorized Claude Opus 4.6 calls for nonconvergence or
protocol failure. Each review is bound to its candidate SHA; valid blockers are
fixed and material corrections re-reviewed. Merge only with tests/CI passing,
PASS/PASS_WITH_NOTES, zero blockers and exact reviewed head.

After merge, one normal CLI reassessment targets only
`doi:10.64898/2026.09.03.749176`, model `deepseek/deepseek-v4-pro-0813`, version
`quality-cross-section-v1`, cached unchanged manuscript, no force/refresh and no
manual correction. At most two shared assessment attempts plus one verifier;
no verifier retry. New grounding failure is inspected but not patched again.
Public outputs are built/audited; deploy Pages once only if the target changes.
