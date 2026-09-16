# Evidence semantics preflight — 2026-09-16

Clean canonical main `f9b2e5a17c92873d0543bd74167a8d94f37dd52e` contains PR #28. Exactly five papers are frozen: four grounding failures and Sci-MMR. The other 23 original decisions are outside this reassessment.

## Existing rules

`full_text._section_kind` deterministically classifies headings into abstract/introduction/methods/results/limitations/discussion/conclusion/related/appendix/body/excluded. The addressing layer already retains headings, exact blocks, hashes and pages; it did not expose section roles. In v1, every Abstract block had `gate_evidence=false`, and the resolver rejected it for every dimension, including contribution.

The prompt explicitly said to use non-Abstract blocks, but gave no category-specific candidate list. All four rejected assessments mixed Abstract with valid body evidence. Why the model selected the Abstract is not observable; salient summary placement is a plausible explanation, not an established cause. Exact rejected claim/explanation text was not retained by v1; the original dimensions, IDs, context, blocks and failure reasons were retained. No missing historical wording is reconstructed.

| Paper | Rejected dimensions | Eligible body evidence already supplied |
|---|---|---|
| AIM | Contribution; novelty/value | Introduction plus Related Work; explicit methods, evaluation and appendices also present. |
| Grounding Agent Memory | Contribution; evaluation | Introduction and Table 2 under Adapted Apex (body); method and appendix material present. |
| Real Science Is Harder | Contribution | Introduction describes both applied research projects; methods/results/discussion present. |
| Conditional Memory | Contribution; reproducibility | Introduction and detailed architecture/hyperparameter appendix; methods and evaluation present. |

For the exact high-level claims, the historical rejected wording is unavailable. The cited body passages demonstrably describe the relevant contribution/evaluation/configuration, but their presence does not establish every old claim as true. The rerun must choose and validate fresh claims automatically.

## Sci-MMR

The stored claim says answer accuracy exceeds complete evidence recovery by more than 20%, citing `Eec559f9f72bc68b9-B0028` and `Eec559f9f72bc68b9-B0035`. The first contains Table 2 accuracy and average evidence/claim coverage; the second discusses model accuracy and difficulty effects. Neither establishes the stated >20% complete-recovery quantity. Average coverage and complete recovery are distinct metrics. The exact stored claim and scoped source excerpts are preserved in the regression fixture. No manual correction is made.

## Planned protection

Expose deterministic section roles and category-specific candidate IDs. Abstracts may support attributed contribution/scope statements but not quality adequacy, verified numerical results, methods, evaluation, limitations or reproducibility. Keep source statements distinct from assessor inference.

Check numerical values/units deterministically in cited blocks only. Because metric identity, comparative scope and nonliteral inference are not reliably resolved by numeric occurrence or word overlap, add one bounded claim/evidence verifier call per paper using the same authorized model. It sees only each claim/explanation and its cited blocks; published narrative is checked against the union of those cited blocks. It receives no paper verdict, full manuscript, author or venue metadata. It returns only supported/unsupported/uncertain with brief reasons; it cannot rewrite or generate evidence. No verifier retry or repair. Main-assessment transport behavior remains unchanged.

Any invalid reference/claim-role selection remains technical grounding uncertainty. Unsupported source claims or inferences become scientific uncertainty, with rejected proposals retained only in the audit. A verifier execution failure remains technical, never scientific insufficiency. Legacy decisions are preserved without silent revalidation. New addressing/support semantics will be explicitly versioned.
