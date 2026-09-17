# Final grounding defects: preflight — 2026-09-17

Scope: body-evidence eligibility and percent orthography only. Baseline main
`3cc24e7fa592bd86c6307f6eeb1b96ffca38d96e` was clean and current. PR #29's existing
rubric, acquisition, context selection, relevance, support verifier and retry
policy remain intact. Batch 2 is not started. The only reassessment targets are
Sci-MMR, Real Science Is Harder, and Conditional Memory, identified exactly in the
[bounded execution manifest](final-grounding-preflight-2026-09-17.json).

## Deterministic reproduction before edits

All three cached manuscripts reproduced the saved source hashes and exact prior
context IDs. The regression fixtures preserve original claim/explanation text,
canonical cited block text, IDs, hashes, headings and pages.

| Paper | Prior technical rejection | Source inspection |
| --- | --- | --- |
| Sci-MMR | `eligible_for`: methodological rigor rejects results-role `Ee289dcbfc19bfb04-B0024` alongside appendix B0050/B0067. | B0024 describes task generation and deterministic filtering; B0050 gives 54%, 17%, 260/235 task counts. They are legitimate method candidates despite the construction heading's results label. This alone does not certify every interpretation in the claim/explanation. |
| Real Science Is Harder | Method rejects Introduction `Edc6e037d47808254-B0013` with Methods B0052. Attributed limitation rejects Methods B0053 with body B0048. | B0013/B0052 describe prompt scope and tested systems/protocols. Those excerpts do not independently establish the claim's multiple independent runs. B0053 explicitly bounds conclusions to the January–March model state; B0048 discusses verification difficulty. Full substantive support still needs the verifier. |
| Conditional Memory | Attributed limitation rejects results-role `Ed88f8e69e24b589c-B0040`. | The block explicitly states non-dominance on every task and possible under-training. The explanation's manuscript-wide absence of a dedicated limitations section is not established by this excerpt alone. |

Sci-MMR also has a separate deterministic `57.2%` rejection in a different item:
B0043/B0105/B0108 contain component rates/counts but not the claimed aggregate
with that unit. The checker does not derive arithmetic; that rejection remains.
The older unsupported >20% complete-evidence-recovery claim remains covered by
the existing regression and is not restored. None of the three technical
rejections is a percent-spelling problem. The shared checker nevertheless
reproduces `95 percent` versus `95%` as unsupported before the fix, consistent
with the recorded earlier Grounding Agent Memory defect. That paper is not
reassessed. No failing example requires a general word-number interpreter.

## Narrow correction and validation boundary

- **A: provenance.** Unknown headings remain `body`. Explicit non-body headings
  (including metadata/front matter) remain ineligible; Abstract retains only its
  attributed high-level contribution exception. Acquisition/selection unchanged.
- **B: compatibility.** Existing compatible section roles remain candidates.
  For unusual or mismatched headings, role-specific cues in the actual block
  can nominate a body passage. Generic other-body text is not globally valid
  for method, evaluation, result, reproducibility and attributed limitation.
  Cues are not an entailment test. The execution audit records the decision basis.
- **C: support.** The unchanged bounded verifier still checks the complete claim
  and explanation against their own sources, including metric, unit, population,
  comparison, direction and scope. Valid IDs/cues cannot grant a scientific pass.
- Percent tokens normalize only digit-based `%`, spaced `%`, `percent` and
  `per cent` spellings. Original text and offsets remain intact. Percentage
  points, basis points, plain numbers and fractional values remain distinct.

The unit suite has 289 tests (273 existing + 16 new), all offline. Regressions
include all four saved eligibility conflicts, both Sci-MMR numeric rejections,
non-body/Abstract restrictions, unrelated conclusions, unknown headings,
percent orthography, distinct numeric concepts and a wrong-metric verifier
rejection. An initial local suite invocation selected Apple's unconfigured Git;
the complete suite passed after explicitly selecting the installed Homebrew Git.

## Bounded authorized continuation

After implementation review and merge, use the normal reassessment pipeline once
per exact target, with new assessment version `quality-grounding-v1`, cached
manuscripts, no `--force`, no output correction, and no other targets. This allows
at most three initial, three shared retry and three verifier calls; no verifier
retry. Historical rows stay unchanged. Protocol/infrastructure failure cannot
become scientific insufficiency.

Start normal `pr-review` with at most two calls; only repeated contradictory or
nonconvergent findings invoke the already authorized independent-review escalation,
with at most two calls. Preserve reports and per-call accounting. Stop if those
bounds cannot produce a reviewed, blocker-free patch.

Current public OpenRouter endpoint pricing was checked 2026-09-17. Conservative
request-byte/output-cap reserves: reassessment **$4.511628**, review including
possible escalation **$3.7913216**, combined **$8.3029496**. These are estimates,
not measured tokenizer usage or invoice amounts. Actual calls/costs will be
reported separately. The model roles and scientific rubric are unchanged.

## Independent review disposition

Normal `pr-review` on `84c0bf80dc505799f304b123bd76590c43ca67bd` returned
**PASS_WITH_NOTES**, no blockers, model `deepseek/deepseek-v4-pro-0813`.
The unchanged downstream verifier is deliberately the substantive support gate;
candidate cues cannot certify a claim. Requiring multiple keywords would be a
new arbitrary heading/content restriction rather than a support guarantee. The
existing new regression already checks a candidate whose universal claim is
unsupported and therefore cannot pass.

Funding and Author Contributions are already excluded by `_section_kind`.
Supplementary Materials correctly retains appendix provenance: supplementary
methods/results are legitimate evidence, subject to claim support verification.
The uncovered compound Copyright and Licensing Information heading is now
excluded, with regression coverage. Fixtures use an explicit three-file list.
These small corrections are submitted for a second independent review. The
reviewer's static uncertainty about constructors/helpers is covered by the
actually executed full unit suite, not a claim that the reviewer ran tests.
