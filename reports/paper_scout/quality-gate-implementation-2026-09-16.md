# Scientific quality gate: implementation and validation

Date: 2026-09-16. Baseline: `a98ec4f16` on canonical main. PR #21 was already merged (`6bf9f6e7eb4ea13c97402f286e4e0eafc9fd360d`); work started with a clean tree on `add-paper-quality-gate`.

## Architecture and admission

The existing shared `QualityAssessment`, versioned SQLite JSON history, deterministic rubric, optional model assessor, bounded PDF acquisition/cache, curation, and card-v2 exports were extended. There is no second quality database or scientific scoring system. Numeric legacy scores remain audit diagnostics and cannot earn admission.

All tracks use `decision == relevant AND quality_status == pass`, with explicit curation exclusion/suppression honored. Pinning and numeric overrides cannot bypass the scientific gate. `maybe` and relevant pending papers remain in `review.html`; insufficient papers remain in exports/direct detail records. Discovery and dated discovery digests remain broad.

The added scientific statuses are `pass`, `uncertain`, `insufficient`, and `not_assessed`; publication metadata separately uses `peer_reviewed`, `preprint`, `repository_only`, or `unknown`. Provenance includes rationale, uncertainty, assessor/model, timestamp, content hash, gate/rubric versions, manuscript scope/URL and publication evidence. Published journal/conference metadata is only contextual evidence, not proof of a review process or quality.

A pass requires a semantic manuscript assessment with located excerpts across contribution, methods, validation, claim alignment, comparisons (or justified absence) and limitations. Excerpts must occur on the supplied manuscript page and in the text actually selected for assessment. Paper-type expectations permit theoretical arguments, surveys, and scoped systems studies. Code is helpful but not mandatory. Abstract-only and deterministic keyword assessments cannot pass. Insufficient requires an actual manuscript-grounded concern; missing evidence produces uncertainty.

Author names are omitted from the model's bibliographic input. Instructions prohibit affiliation, employer, university, country, fame and venue prestige as quality signals, including where identities appear inside manuscript text. Affiliation-invariance tests use identical evidence for university, company and independent authors. These tests validate policy and the deterministic boundary; they cannot guarantee every future model's semantic judgment is bias-free.

## Safe migration and bounded backfill

No historical SQLite payload is rewritten, no paper is deleted, and no legacy score becomes pass. Compatible new assessments survive routine deterministic reassessment. Repeated bounded backfills advance past current-gate entries; explicit targeting/force retries uncertainty. Manual reviews use the existing semantic validator and distinct content-digest identities so revisions retain history.

`reassess-quality` defaults to the track's existing cap and accepts only 1–50 papers. Explicit manuscript import/PDF options require one paper ID. Full-text acquisition retains existing byte, page, time and prompt bounds. Daily caps remain 5 / 5 / 4, with deterministic modes and no new required provider. Engram manuscript acquisition is explicit. A paid backfill must be deliberately configured; none was run here.

The restored 2026-09-15 durable snapshot contained only deterministic historical quality assessments, so every exported record starts `not_assessed`. This deliberately makes the main screened sections empty; each page explains why and links to accessible pending reading candidates. The figures below are post-curation export counts, not all discovered database rows and not benchmark results:

| Track | Exported records | Relevance-high | Pass | Not assessed | Uncertain | Insufficient | Main | Repository-only |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Agentic Memory | 1,907 | 317 | 0 | 1,907 | 0 | 0 | 0 | 237 |
| Deep Research | 217 | 130 | 0 | 217 | 0 | 0 | 0 | 57 |
| Engram | 8 | 8 | 0 | 8 | 0 | 0 | 0 | 0 |

No repository-only record in this snapshot had a compatible scientific assessment. Library reports enumerate non-admission reasons. All database hashes were identical before and after the offline validation builds. The original local runtime databases were not changed. Generated production pages remain owned by the existing daily rebuild/deployment workflow; no stale generated output is committed with this implementation.

## Factual Zenodo example

Public sources retrieved on 2026-09-16: [record API](https://zenodo.org/api/records/22735829), [record](https://zenodo.org/records/22735829), and its open PDF. The fixture retains factual metadata, checksums and short located manuscript excerpts, excluding mutable statistics and owner data.

- Title: **Structured Episodic Memory (SEM)**. API author: **Araç, Berat**; PDF cover: **Berat D. Araç**.
- API affiliation: null. PDF affiliation: **Independent Researcher**. Neither affects scientific assessment.
- DOI: `10.5281/zenodo.22735829`; concept DOI: `10.5281/zenodo.22735828`.
- Depositor resource type: publication / preprint; date: 2026-09-13; version: 1.0.0; language: English.
- No communities, journal or conference metadata was supplied. There is no independent peer-review evidence in the retrieved record/manuscript.
- File: `Structured_Episodic_Memory.pdf`, 621,489 bytes, 13 pages; MD5 `27521c9027d6e8970bc25faf90a1e067`; SHA-256 in the fixture.
- License: CC BY 4.0. Related software: [structured-episodic-memory](https://github.com/berat-arac/structured-episodic-memory), relation `isSupplementTo`.
- Abstract describes a non-neural associative-memory Pong controller, 40 sequential training runs / 2,200 outcomes, a 0.974 frozen mean hit rate on six fresh seeds, paired component ablations and restricted claims.

Publication classification is **repository_only**, retaining the depositor's preprint label as separate context. The actual manuscript's methods, protocol, results, discussion, limitations and appendix were inspected; the numerical-results page was also visually rendered. This supports a **scoped scientific pass** for the systems-study claims: specified associative updates, paired ablations, fresh-seed frozen evaluation and explicit boundaries. It does not establish comparative superiority or scientific correctness. Small seed counts (usually 6–8), one engineered task family, hand-designed features, no tuned conventional RL baselines, and unreproduced results limit confidence.

Topical classification is **Agentic Memory review candidate**, **Deep Research not relevant**, **Engram not relevant**: it does not study LLM agents, autonomous research workflows or language-model-integrated memory. The curation adjustment corrects topical overclassification, not scientific quality. The fixture's manuscript judgment does not silently promote production records; historical SEM records still require a persisted review through the bounded import path. Existing generic research-card metadata remains an automated topical summary, subordinate to the explicit curation note.

## Validation evidence

- Complete unittest suite: **186 passed**, including legacy and new snapshot pack/restore compatibility, state isolation, curation, New/date ordering, structured cards and quality behavior.
- New gate coverage: affiliation/DOI invariance; repository metadata conservatism; eligible independent preprints and repository manuscripts; insufficient institutional work; peer review not forcing pass; missing/abstract/fabricated evidence; six core dimensions; deterministic non-promotion; legacy round trips; all-track admission and curation bypass prevention; duplicate provenance; factual SEM; bounded CLI; extraction continuations; versioned manual reviews; numeric curation cannot manufacture manuscript-review provenance; repeated bounded backfill.
- All three tracks: relevance precision/recall 1.0 on fixed fixtures; eight quality fixtures passed per track; discovery fixtures Agentic Memory 6/6, Deep Research 4/4, Engram 4/4; idempotency first run two / second run zero. These are fixed regression fixtures, not live discovery-recall or scientific-quality benchmarks.
- All three offline sites built from the restored durable snapshot. Every generated sidecar validated against the card-v2 JSON Schema. Site/schema/relative-link/exposure/workflow checker: **0 errors**. Generated-file size checks and `git diff --check` passed.
- Browser inspection covers empty main state, pending search, New labels, navigation and representative research-card provenance, with no captured console errors.
- The new secret-free PR workflow runs the complete offline tests and three-track builds/checks. `jsonschema` moves from test-only to runtime requirements so sidecars are validated at generation.
- Scientific corpus model calls: **0**. Independent code-review model runs and final findings/cost are recorded in the PR, separate from manuscript assessment.

## Limitations and review focus

Quality screening is a reviewable judgment, not proof of correctness. Publication status is conservative metadata inference. Located quotes validate provenance, not the correctness of the semantic judgment. No live model-quality benchmark or reproduction of SEM was run. Existing deterministic queues alone cannot populate the screened main libraries; explicit manuscript reviews are required. Initial empty main libraries are intentional, with review candidates preserving usable access.

Independent review should assess the four-way separation, absence of prestige rules, conservative repository/abstract behavior, preprint eligibility, migration and provenance, server-rendered filtering, bounded costs, regressions and the factual fixture. The standard global review and any subsequent complete-context review must have no unresolved blocking findings before merge.

## Independent review triage

The first accepted complete-patch verdict was CHANGES_REQUIRED. The standard run had returned no verdict after exhausting its output budget. Review findings were checked against the concrete code rather than accepted as assumptions:

1. **Forced revalidation allegedly blocked:** rejected as a reading error; the early-return condition already explicitly includes `not force` and `manual_assessment is None`. Added a regression proving a prior pass is replaced when forced content reacquisition changes the hash; the downloader receives `refresh=True`.
2. **Zenodo fixture allegedly importable as a pass:** rejected. The fixture records a documented, scoped manuscript inspection, not a production assessment. Production import always acquires/selects manuscript text separately, and the fixture lacks the required review fields. Added a test that rejects the entire metadata fixture before database access. No production record is promoted by this fixture. Removing the inspected evidence would contradict the requested factual regression case.
3. **Unvalidated review JSON / injection:** accepted the structural-validation hardening. Imports now validate against the same explicit response schema supplied to the model, before database or acquisition work, then undergo semantic excerpt checks. Invalid statuses, objects, evidence shapes and extra metadata are rejected early. The claimed prompt/code execution path was not present: manual imports are not sent to a model, and HTML fields are escaped. Added a hostile-markup escaping regression.
4. **Venue metadata not proving peer review:** retain the requested publication-status vocabulary and explicit inference caveat; quality never derives from that label. No claim of independent review verification is made.
5. **Insufficient papers missing from normal navigation:** intentional policy requested by the user. Export links are publicly available in each page's Export library disclosure and include these records, with direct research-card paths in JSON; insufficient work is excluded from normal reading views.

A separate local provenance audit fixed numeric curation being mistaken for manuscript inspection and preserves actual semantic-review provenance, including uncertain reviews. Final independent verdict and reported model costs are recorded in the PR after re-review.
