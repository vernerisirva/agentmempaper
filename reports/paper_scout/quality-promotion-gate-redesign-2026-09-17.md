# High-precision quality promotion gate redesign — 2026-09-17

## Why redesign was necessary

ORIGINAL_BATCH_2_GENERALIZATION_RESULT = FAIL
BATCH_2_RECOVERY_CHECK = FAIL
BATCH_2_RECOVERY_V2_CHECK = FAIL

Repeated deterministic semantic-validator hardening did not generalize sufficiently.
Frozen recovery v2 remains 0 passes, 10 scientific uncertainties, 6 unavailable
manuscripts and 4 technical failures. Numeric false rejection and verifier behavior
remained; 337 software tests passing did not override those empirical failures.
This redesign is engineering, not a fourth recovery and not evidence of generalization.

Canonical main was freshly fetched and fast-forward checked at
`844a6be7f90d33fe3193049654b3d5fcec0222eb`, clean, with PR #33 merged at
`f073e7f94e84269c8b6834bdf9f8e29864c0d61d`. All three reports were read in full.
No Batch-2 paper was patched/reassessed. No Batch-3 roster was selected or assessed.

## Old and new responsibility

Old: assessor → role/section eligibility and lexical number/URL checks → up to thirteen
isolated claim/narrative verifier calls → required evidence dimensions → admission.
New: manuscript → primary scientific assessor → independent scientific adjudicator →
deterministic integrity validation → conservative promotion. Integrity is also checked
before transport and when passes are loaded/stored. Scientific disagreement is ordinary
non-promotion; corrupt provenance, invalid response schema and interrupted transport
remain technical outcomes. Missing methodology is a scientific question, not missing text.

| Mechanism | Responsibility after redesign |
|---|---|
| Acquisition source URL, canonical identity, manuscript/version SHA-256 | Keep deterministic; exact title match after typography-only normalization is conservative identity evidence, never a quality score. Ambiguity withholds assessment. |
| Context version/hash, ID membership, canonical block text/hash and span mapping | Keep fail-closed; both models receive the same identified context. Persisted passes are revalidated. |
| Schema, returned model identity, finish reason, two completed calls, storage | Keep fail-closed; missing/abnormal finish or malformed JSON is never repaired or promoted. |
| Unicode normalization, exact source text and offsets | Keep; no guessed scientific symbols and no ASCII-only loss. |
| Numeric atoms, percentages, glued numbers, measurement/locator parsing | Retire from new scientific admission. Scientific meaning belongs to the two models. Legacy numeric code remains for audit. |
| Section/claim-role eligibility, required keyword evidence dimensions | Retire from new admission. Existing bounded acquisition/selection labels describe supplied coverage; they cannot veto a valid scientific interpretation. |
| Prose substring anchors, per-claim/explanation/narrative support heuristics | Retire from new admission; no claim-level verifier fan-out. |
| Deterministic scores, paper-type heuristics and score caps | Legacy diagnostics only; cleared from new promotion decisions, never admission criteria. |
| Artifact URL parsing | Models introduce no URLs in prose. Links are factual canonical source text; no link-existence-to-reproducibility inference. Legacy extraction remains unchanged. |

No large cleanup or historical rewrite occurred. `evidence_semantics.py` is marked
legacy; historical quote, role, atom and support functions remain callable under old
versions. The new production default is `quality-promotion-v1` / `dual-promotion-v1`.

## Exact promotion rule

`high relevance AND primary pass AND independent adjudicator pass AND valid provenance
AND nonempty canonical evidence citations AND no adjudicator blockers AND no suppression`
→ main library. All other new results remain review candidates (including unavailable
or technical pending). Ordinary unsupported claims and overclaims produce uncertainty,
not `evidence_grounding_failure`. There is no target pass rate or forced final verdict.

Primary fields: decision, scoped contribution, method, evaluation, claim/evidence
alignment, limitations, quality rationale and evidence IDs, plus manuscript/context
identity. Adjudicator fields: pass/uncertain promotion decision, blocking reasons and
its own evidence IDs, with the same identity. The independent adjudicator receives
canonical manuscript context and only the primary final structured response. It is
instructed to look for counterevidence and independently assess scientific support.
No hidden reasoning is requested, shared or persisted. Different families reduce direct
echoing but do not establish statistical independence or guarantee scientific correctness.

The conservative rubric requires substantive contribution, adequate methods, appropriate
validation/comparisons, scoped claims and compatible limitations. Institutions, author
reputation, famous labs/companies and venue prestige are excluded as quality evidence.
Independent researchers are equally eligible. Publication metadata remains descriptive.

## Models and costs

Primary: `deepseek/deepseek-v4-pro-0813`. Adjudicator: `anthropic/claude-sonnet-4.6`.
Both are explicitly pinned OpenRouter slugs in a reviewed family allowlist. Environment
variables configure the pair; unsupported aliases and same-family pairs fail closed.
No assessment-model settings were present in the task environment/local allowlisted
configuration. OpenRouter publicly advertises structured-output support for both routes.
A credential's private entitlement was not tested by spending inference tokens.

At most two requests, no retries, each at most 300,000 actual serialized bytes and 4,096
output tokens. Provider price caps are enforced. At 50,000 input tokens per call and
2,000/1,000 output tokens, conservative advertised provider rates yield approximately
$2.74 / $5.48 / $8.22 for 10 / 20 / 30 assessable papers. Worst-size one-token-per-wire-byte
reserves are $15.73 / $31.46 / $47.19, not expected bills. Unknown charges are not free.
See the [frozen cost manifest](../../experiments/manifests/quality-promotion-gate-2026-09-17.json)
and [public pricing feed](https://openrouter.ai/api/v1/models). Prices require rechecking
and a separately approved ceiling before future batch execution. Engineering uses mocks;
no paid paper assessment or live smoke has been performed.

## History and persistence

All preexisting reports/manifests and runtime table rows are hash-baselined. Historical
assessments retain original schemas and are not migrated. Existing main-library passes
are returned unchanged during routine assessment. A separate forced reassessment remains
explicit. New runs have an append-only storage identity; re-saving the same run is
idempotent. A single manual review cannot bypass the new gate. Public cards include
both final scientific judgments and model IDs; the full canonical receipt stays in
ignored runtime storage. No raw responses, hidden reasoning or credentials are committed.

## Validation and independent review

In progress; final exact-candidate validation and independent review must pass before
readiness is set to YES. The review uses `pr-review --base origin/main`, a 200 KB request
ceiling, 16,384 completion tokens and a 360-second process bound, with the established
bounded DeepSeek-to-Opus escalation policy. Valid blockers must be fixed and re-reviewed.
PR, reviewer verdict and merge SHA will be recorded after the merge gate completes.

## Next unseen experiment

The [Batch-3 protocol](../../experiments/manifests/batch-3-promotion-protocol-2026-09-17.md)
is prepared but NOT executed. Engineering is frozen before deterministic hash selection;
all previously assessed/development identities are excluded globally, the roster is
frozen before assessment, no likely-success selection or replacements are permitted,
and there are zero code changes or manual output corrections mid-batch. Audit every
promotion. Zero promotions cannot establish positive precision. No candidate roster
has been inspected or selected during this engineering task.

ORIGINAL_BATCH_2_GENERALIZATION_RESULT = FAIL
BATCH_2_RECOVERY_CHECK = FAIL
BATCH_2_RECOVERY_V2_CHECK = FAIL
QUALITY_PROMOTION_GATE_READY_FOR_BATCH_3: NO
