# Final grounding correction and bounded rerun — 2026-09-17

**QUALITY_PIPELINE_READY_FOR_BATCH_2: NO.** Two of the three technical failures
became automatic scientific uncertainty. Real Science Is Harder still has a
claim-candidate failure on a different cited passage. No manual correction,
extra scientific retry, rubric change or batch-2 execution occurred.

## Root causes and correction

| Paper | Prior failure in `eligible_for`, called by `validate_block_quality_response` | Change / final result |
| --- | --- | --- |
| Sci-MMR | Method claim rejected results-role `Ee289dcbfc19bfb04-B0024`, although it describes construction/filtering. A separate 57.2% claim lacked that literal unit/value in its own cited blocks. | Body-content method candidacy now accepts the construction passage; numeric and semantic rejection remain enforced. Automatic scientific uncertainty. |
| Real Science Is Harder | Method rejected Introduction `Edc6e037d47808254-B0013`; limitation rejected Methods B0053. | Those fixtures pass, but the fresh proposal also cites Introduction B0014 for method. That block fails the finite content-cue filter. Automatic evidence grounding failure remains. |
| Conditional Memory | Attributed limitation rejected results-role `Ed88f8e69e24b589c-B0040` despite explicit under-training/scope text. | Legitimate limitation candidacy accepted. Automatic scientific uncertainty because the supplied excerpts do not establish the proposed code-repository claim. |

The patch separates provenance, claim-role candidacy and substantive support.
Unknown headings retain body membership; restricted claims require compatible
section roles or claim-specific body cues. Every accepted claim still needs the
unchanged support verifier. Abstracts remain limited to attributed contribution;
references, acknowledgements, funding, author metadata and copyright/licensing
front matter stay excluded. Supplementary methods/results remain appendix
candidates, not automatic support.

Percent orthography normalizes `95%`, `95 %`, `95 percent` and `95 per cent` on
both sides while preserving the original text. Plain numbers, fractional values,
percentage points and basis points stay distinct. No word-number interpreter,
arithmetic inference, metric substitution or general numerical rewrite was added.
None of the three old eligibility failures required word-number support.

## Remaining blocker: a new cited methodological passage

`Edc6e037d47808254-B0014`, Introduction, pages 2–3, describes the research design:
full and smaller prompts, comparisons across AI frameworks and up to four
independent runs. This is legitimate methodological body text, but it lacks the
finite method-regex cues. Layer A passes; Layer B rejects it; the normal pipeline
therefore withholds the proposal and does not invoke the support verifier.
B0013 is now accepted. This exposes incomplete content-based candidacy beyond
the reproduced fixtures. It is an engineering limitation, not evidence that the
paper is scientifically insufficient. A future reviewed correction should
address compatibility without globally accepting body prose or accumulating
paper-specific keywords. This task does not apply that further correction or
rerun the paper.

## Review and merge

[PR #30](https://github.com/vernerisirva/agentmempaper/pull/30) merged as
`cd97c329062a9a76dae02d83ce4b9c4a64028282`; its tree equals reviewed head
`ce9d8d8cb20dab4a6c3601b1b06c506ccfb64779`.

1. DeepSeek V4 Pro: **PASS_WITH_NOTES** on `84c0bf80d`, no blockers.
2. Compound licensing-heading coverage and explicit fixture enumeration were
   corrected; full validation passed. The second default review exhausted its
   output limit, so no verdict was accepted.
3. Already-authorized Claude Opus 4.6 escalation: **PASS** on the final head,
   no findings. [Final-head CI passed](https://github.com/vernerisirva/agentmempaper/actions/runs/35196490581).

All reviewer reports and rejected-attempt metadata are preserved locally; exact
head/request identifiers and usage are in the JSON report. Review was static;
it did not itself execute tests. No material source changes followed final review.
The final live result reveals the remaining coverage gap despite that review.

## Exactly three automatic reassessments

Model: `deepseek/deepseek-v4-pro-0813`; assessment version:
`quality-grounding-v1`. Existing cached source hashes, normal CLI execution,
normal support verifier and retry policy; no `--force`, no acquisition refresh,
no manual imports. Exact commands/request/response ledgers are preserved in the
ignored local operator artifacts. The three prior statuses were all
`evidence_grounding_failure`.

| Paper | Final category | Accepted evidence roles | Automatic |
| --- | --- | --- | --- |
| Sci-MMR | scientific_uncertainty | Abstract (contribution only), appendix, limitations, related, results | YES |
| Real Science Is Harder | evidence_grounding_failure | None accepted; the method proposal cites Introduction B0013/B0014 | YES |
| Conditional Memory | scientific_uncertainty | body, introduction, methods, related, results | YES |

Sci-MMR's old unsupported complete-evidence-recovery assertion is absent from
accepted claims and rationale; its old pass is not restored. The new accepted
assessor narrative does not assert 57.2%. Untouched verbatim source disclosures
can still contain that percentage; source presence is not an endorsed assessor
claim. New unsupported quantities/interpretations were also withheld. Its
uncertainty is about support in the cited excerpts, not a finding that the paper
itself is scientifically insufficient. The existing numeric-metric regressions
remain intact. Historical proposals and every old assessment remain preserved.

## Original-28 accounting

| Category | Before | After |
| --- | ---: | ---: |
| pass | 15 | 15 |
| scientific_uncertainty | 6 | 8 |
| insufficient | 1 | 1 |
| manuscript_unavailable | 3 | 3 |
| evidence_grounding_failure | 3 | 1 |
| model_protocol_failure | 0 | 0 |
| text_coverage_failure | 0 | 0 |

All 555 previous assessment rows are byte-for-byte unchanged in their logical
records: agent_memory 294, deep_research 215, engram 46. Exactly three automatic
rows were appended (0/2/1). All other 25 original decisions and all non-quality
runtime tables are unchanged. AIM and Grounding Agent Memory were not reassessed.

## Validation

**289 tests pass: 273 existing plus 16 new**, including the four actual prior
role conflicts, unknown headings, non-body/Abstract exclusions, unrelated body,
semantic-support rejection, Sci-MMR unsupported quantities, percent orthography,
and distinct units/metrics. Existing wrong-ID/context, truncation, infrastructure
and backward-compatibility protections pass. This does not claim that the finite
cues cover all real methodological prose; B0014 demonstrably remains a gap.

All three relevance, quality, discovery and idempotency checks, three offline
site builds, sidecar schemas, relative links, exposure/secret and workflow checks,
file-size limits, snapshot/restore, legacy two-database compatibility and
`git diff --check` pass. All 28 calibration sidecars and their HTML titles and
rationales were checked against saved decisions. Source-block hashes match.
Legacy evidence is compared through the existing loader, which strips outer
excerpt whitespace and supplies absent default fields; stored rows are not edited.
The normal all-site regeneration also refreshes generated-at provenance timestamps
on other cards. It does not reassess them. No browser execution is claimed.

Public main-library admissions remain **agent_memory 4 / deep_research 5 /
engram 6**. The three target papers remain outside the main libraries.

## Cost (provider-reported, this task only)

| Work | Calls | Input tokens | Output tokens | USD |
| --- | ---: | ---: | ---: | ---: |
| Initial reassessment | 3 | 141,835 | 6,298 | 0.203187336 |
| Reassessment retries | 0 | 0 | 0 | 0 |
| Support verification | 2 | 38,636 | 1,360 | 0.044655480 |
| Independent review | 3 | 62,473 | 31,144 | 0.256924348 |

Reassessment total **$0.247842816**; review **$0.256924348**; combined
**$0.504767164**. Unknown-cost requests: **0**. The truncated review is included.
Review output usage includes reported reasoning tokens where present. These are
response-reported charges, not independently reconciled invoices.

## Publication

Validated output and durable-state publication are pending. At most one
`deploy_only=true` Pages deployment will be dispatched, without discovery,
assessment or batch-2 execution. Deployment identifiers and restore verification
will be recorded after completion.

## Handoff

The implementation and deterministic regressions improve the reproduced cases,
but the remaining real methodological passage prevents the readiness gate from
passing. Preserve this evidence for the next focused compatibility correction.
No further paid calls or batch selection are part of this handoff.

QUALITY_PIPELINE_READY_FOR_BATCH_2: NO
