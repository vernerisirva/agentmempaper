# Computer Vision track — implementation and validation, 2026-09-21

Adds `computer_vision` as a fully supported fourth Paper Scout track alongside Agentic
Memory, Deep Research and Engram. Branch `add-computer-vision-track`, PR
[#43](https://github.com/vernerisirva/agentmempaper/pull/43), built against `main` at
`2be5a543b`.

## A. Architecture

The track uses the existing multi-track abstractions; no parallel system was introduced.

| Concern | Mechanism | Change |
| --- | --- | --- |
| Registration | `TRACK_CONFIG_PATHS`, `TRACK_SITES`, `batch_population.TRACKS` | one entry each |
| Configuration | `config/tracks/computer_vision.yaml` | new file, same schema |
| Relevance | `relevance.classify_with_rules` profile dispatch | new profile branch |
| Curation | `config/curation/computer_vision.yaml` | new file, same schema |
| Seeds | `config/seeds/computer_vision.json` + existing `ingest-seeds` | new manifest |
| State | `data/computer_vision/paper_scout.sqlite3` | new path in `STATE_PATHS` |
| Site | `docs/computer-vision/` via `build_site(relevance_profile=...)` | new profile branch |
| Research cards | `structured_cards` profile dispatch | new profile branch |
| Discovery | `query_planner` unchanged; config supplies queries and budgets | config only |
| Operation | `operational_run` / `operational_preflight` unchanged in shape | run ceiling 3 → 4 |

Two things were generalized rather than special-cased, because a per-track branch would
have had to be rewritten for a fifth track:

- **Durable state.** `LEGACY_DATABASE_SETS` replaces the single hard-coded two-track
  legacy set with the list of layouts a snapshot may legitimately be complete for.
- **Topic filter.** `site.TOPIC_FILTERS` is a per-profile table. A track with no entry
  renders no control, so every other library's markup is byte-identical.

One latent defect was found by running the full validation sweep rather than the tests:
`validate-idempotency --track computer_vision` raised `KeyError` because
`validation.py` carried a hard-coded three-track term map. That is not a check failure —
it is an exception that would have taken the workflow's validation step down on the first
scheduled run after merge. Fixtures were added and a test now pins that every registered
track has them.

## B. Track scope

Public title **Computer Vision Paper Library**, at `/computer-vision/`.

Object detection leads: YOLO family, one-stage and anchor-free detectors, DETR and its
real-time descendants, the R-CNN lineage, open-vocabulary, small-object and oriented
detection, detection losses and label assignment, detector training and evaluation,
deployment and latency work.

The surrounding field is covered as the library's breadth: segmentation (semantic,
instance, panoptic, promptable), tracking, pose and keypoints, visual backbones and
representation learning, vision-language work where visual methodology is the
contribution, 3D and depth, and efficient or edge vision.

**The policy the screen turns on is breadth of claim, not application area.** A paper that
runs an existing detector on one dataset is a review candidate because it makes no
general-method claim. A medical, remote-sensing or agricultural paper that contributes a
broadly useful method is a core paper, and a fixture pins exactly that case. Only two
method signals cancel the application downgrade — a stated generality claim, and a
training, matching or loss contribution — because every application paper says it proposes
a framework, and an ablation shows rigour rather than breadth.

A paper with no visual subject at all cannot reach the track. That single gate is what
excludes generic RAG, agent frameworks, recommender systems, text-only language models and
memory-management work without needing a rule per topic.

## C. YOLO emphasis without overfitting

YOLO is first-class but not the whole page:

- `yolo` is a screening tag and a dashboard filter option. A YOLO paper is always tagged,
  even when only the high-confidence pattern matched.
- Three of the five arXiv keyword queries, two of four OpenAlex and two of four Semantic
  Scholar queries are detection-shaped.
- Competing families are seeded and searched deliberately: Faster R-CNN, Mask R-CNN, DETR,
  Deformable DETR, DINO, RT-DETR. The relevance reasons name the family, so
  "DETR-family detection" and "YOLO / real-time detection" read as distinct topics.
- The `cs.CV` category sweep, not the keyword queries, carries segmentation, tracking,
  pose, 3D and efficiency into the track. That is deliberate: keyword budgets go to the
  emphasis, category breadth goes to the field, and the relevance screen filters.

The dashboard's Topic control was verified in a browser: 90 review candidates → 32 under
`yolo`, 7 under `detr`, 12 under `segmentation`, back to 90 under All topics, with search
still composing correctly. (That check ran against the pre-rebuild corpus of 90; the
committed corpus has 89 review candidates after one seed failed to resolve.)

## D. Discovery queries and budgets

| Provider | Budget | Queries |
| --- | --- | --- |
| arXiv | 6 | `object detection`, `"real-time object detection"`, `"YOLO"`, `open-vocabulary object detection`, `vision transformer`, **+ `cat:cs.CV` sweep** |
| OpenAlex | 4 | real-time object detection; YOLO object detector; vision transformer image recognition; image segmentation deep learning |
| Semantic Scholar | 4 | real-time object detection; YOLO detector; open-vocabulary object detection; visual representation learning |

Five arXiv keyword queries plus the sweep fill the budget exactly. A sixth keyword query
would silently displace the sweep, because the planner truncates after appending it; a
test asserts the sweep survives.

Category sweep: `cs.CV` only, `days: 10`, `max_results: 300` — the same single-request
shape the agent-memory sweep already uses, so global request load is unchanged in count.
`cs.CV` is high-volume and one sweep cannot see the full window; truncation is reported as
`incomplete_window` in source diagnostics rather than presented as coverage.

Total: 14 logical queries per run, one page each.

## E. Foundational seeds

Sixteen anchors in the manifest. **Every arXiv identifier was resolved from primary
metadata before it was written** — the arXiv API for ten, OpenAlex (`10.48550/arXiv.<id>`)
as the authoritative fallback for six when arXiv throttled this host. None was recalled
from memory.

YOLO lineage: 1506.02640, 1612.08242, 1804.02767, 2004.10934, 2107.08430, 2207.02696.
Detection: 1506.01497 (Faster R-CNN), 1703.06870 (Mask R-CNN), 2005.12872 (DETR),
2010.04159 (Deformable DETR), 2203.03605 (DINO), 2304.08069 (RT-DETR).
Modern vision: 2010.11929 (ViT), 2103.14030 (Swin), 2304.02643 (SAM), 2304.07193 (DINOv2).

Ingestion result: **15 of 16 ingested, all screened `relevant`.** `1506.02640` (the
original YOLO paper) is `unresolved`: arXiv began refusing this host entirely part-way
through the session, and the OpenAlex DOI fallback returned 404 for that one work. The
manifest entry is correct — the title was verified against the arXiv API earlier in the
same session — and the ingestion reported it rather than fabricating metadata, which is
the intended fail-closed behaviour. The daily workflow bootstraps missing seeds on every
run, so it resolves on the first scheduled run from a runner with a working IP.

A seed's canonical key depends on which provider resolved it: an arXiv lookup keys on
`arxiv:<id>`, the OpenAlex fallback on `doi:10.48550/arxiv.<id>`. Curation notes are
therefore keyed on **both** identifier and title, because identifier-only notes silently
detached when the fallback route was taken. A test pins that every seed's note carries
both.

Seeds carry an identity-level curation note naming the lineage they anchor and nothing
about their findings, because a curation note is displayed with `curation` provenance and
must not assert what was not read. No quality override or suppression field appears in the
curation file. Per §9, seeds stay in normal track data and are distinguished by curation
rather than by new UI machinery; **seeding admits nothing to the main library.**

## F. Initial corpus

One bounded local `run` invocation plus seed ingestion, from empty state.

The track was rebuilt from scratch before this run. An earlier local pass had run
discovery three times on the same date while the relevance rules were still being tuned,
which left a digest whose body mixed classifications from different rule versions. That is
an artifact of local iteration — the daily workflow runs once — but a committed archive
page should be reproducible from one consistent state, so the state, digest, site and
reports were deleted and regenerated in a single pass.

- **Candidate sightings:** 100 fetched.
- **Unique papers:** 108 in the track database (15 seeds + 93 discovered).
- **Relevance:** 38 highly relevant, 57 review candidates, 13 excluded.
- **Provider outcomes:** OpenAlex 4/4 queries succeeded (all reported
  `incomplete_window`, i.e. the 25-record page was full). arXiv 6/6 failed with HTTP 406
  and Semantic Scholar 4/4 failed with HTTP 429.

**This is a host limitation, not a defect.** arXiv rate-limited this machine's IP for
`all:`-prefixed searches throughout the session — a paced retry at 30–45 s intervals with
five attempts per query still returned 406, while an isolated `cat:cs.CV` probe succeeded.
Semantic Scholar returns 429 without an API key, which this host lacks and the workflow
has. The runner has a different IP and both credentials, so production discovery exercises
paths this local corpus could not. **The local corpus is therefore OpenAlex-dominated and
under-represents arXiv preprints.**

## G. Relevance validation

Twenty-one deterministic fixtures, all pinned to an exact decision, all landing where
pinned: precision 1.000, recall 1.000, 0 decision mismatches.

- **Core (10, expect `relevant`):** YOLO-style detector, real-time DETR, semantic
  segmentation, visual backbone, multi-object tracking, self-supervised representation,
  pose estimation, monocular depth, quantized detector deployment, and a *domain* paper
  that states a general method.
- **Hard negatives (6, expect `irrelevant`):** generic RAG, generic agent framework, GPU
  and database memory, text-only LLM, recommender system, image generation only.
- **Borderline (5, expect `maybe`):** medical application of a standard YOLO, remote
  sensing detection application, vision-language model, robotics with cameras,
  synthetic-data pipeline.

The other three profiles were re-evaluated and are unchanged at precision 1.000 / recall
1.000 with no mismatches.

Behaviour on the real corpus was inspected, not just the fixtures. Applied "X-YOLO for
<narrow subject>" papers (SAR aircraft, underwater fish, PPE, weed spraying, traffic
signals) land at `maybe`; canonical detector and backbone papers land at `relevant`; all
sixteen seeds land at `relevant`.

Known imprecision, stated rather than tuned away: a vision-transformer application outside
the named domain list (facial expression, deep-fake detection, copy-move forgery) can still
score as relevant. Relevance is topical only; the scientific gate is the real filter, and
review candidates stay searchable either way.

## H. Quality assessment results

Bounded initial batch through the production path unchanged: Gemini `gemini-3.8-flash`
primary, `deepseek/deepseek-v4-pro-0813` adjudicator via OpenRouter, the existing
acquisition walk, the existing eligibility rules, a `$0.30` reservation ceiling. Five
walks, one paper per walk.

Two batches ran in total, because the track was rebuilt from empty state between them:
five papers reached a model in each, ten overall, which is exactly the §21 cap. The table
below is the surviving batch, on the committed state. Both batches produced the same
outcome — 4 completed, 2 promoted, 2 not, 1 protocol failure — on the same ranking, which
is a useful consistency signal for a gate driven by two independent models.

| Measure | Value |
| --- | --- |
| Candidates walked | 14 |
| Reached a model | 5 |
| Completed scientific decisions | 4 |
| **Promoted** | **2** |
| Not promoted | 2 |
| Technical outcome (retry-eligible) | 1 protocol failure |
| Skipped before any model call | 9 (`manuscript_unavailable`, zero cost) |
| Gemini calls / tokens | 5 / 155,320 in, 5,810 out |
| DeepSeek calls | 4 |
| **OpenRouter spend** | **$0.119522** (first batch: $0.106262; $0.225784 / 10 papers = **$0.0226 each**) |

Promoted: *LD-IoU: A Novel Lorentzian Distance-based Localization Loss for Enhanced
Bounding-box Regression* and *Deadline-Aware Hardening of Real-Time Object Detection
Against Candidate-Inflation Latency*. Not promoted: an XNOR detector accelerator and a
surface-defect segmentation paper, both assessed on full text and both returning
`uncertain`. **The gate discriminates rather than rubber-stamps.** No manual promotion was
performed and no override exists in the curation file.

## I. State migration

`STATE_PATHS` gains `data/computer_vision/paper_scout.sqlite3`. Restore semantics were
generalized, and all four cases are tested:

| Snapshot | Behaviour |
| --- | --- |
| Four-track (current) | restores byte-for-byte, initializes nothing |
| Three-track (pre-Computer-Vision) | installs and verifies all three byte-for-byte, initializes **only** `data/computer_vision/…` |
| Three-track restored again over live state | initializes nothing; existing Computer Vision rows unchanged |
| Missing an established track (e.g. Engram dropped) | **fails closed** — still a partial archive |
| Corrupt fourth database | **fails closed**, nothing on disk mutated |
| Two-track (pre-Engram) | still restores, now initializing both newer tracks |

The v2 manifest's `databases` list is now checked against the archive's own members rather
than against today's `STATE_PATHS`, so a manifest that honestly described an older complete
set is no longer rejected for being old. `LEGACY_DATABASE_SETS` is append-only by contract.

The transport script labels the new database by track (`persist_sha256_computer_vision`,
`restore_sha256_computer_vision`) rather than by a path-derived slug. No public state
storage was reintroduced.

## J. Workflow integration

`.github/workflows/paper-scout.yml`: `evaluate-relevance`, `evaluate-quality`,
`evaluate-discovery` and `validate-idempotency` for the new track; `ingest-seeds` and
`run --track computer_vision --no-llm` in the discovery step; `build-site`; and the fourth
database in the snapshot-preparation step. No live-smoke step was added, matching Engram.

`.github/workflows/paper-scout-backfill.yml`: the fourth path added to snapshot
preparation only. The weekly backfill's scope (agent memory and Engram) is unchanged;
`persist` packs every database, so an unflushed WAL on a track this workflow does not touch
would otherwise refuse the snapshot.

`.github/workflows/paper-scout-checks.yml`: the new track added to the per-track loop.

Retained unchanged: acquisition walk, retry eligibility, Gemini primary, DeepSeek
adjudicator, private state restore/persist, append-only history, and the guarantee that
discovery never receives a scientific credential.

## K. Cost impact

`MAX_PAPERS_PER_RUN` 3 → 4. **`MAX_PAPERS_PER_TRACK` stays 1 and no quota transfers
between tracks**, so the ceiling is exactly one slot per track; a test ties it to
`len(TRACKS)` so a future raise that is not a new track reads as the policy change it is.

**The `$0.30` OpenRouter ceiling was not raised, because four papers fit under it.**

| Basis | Four-paper run | Pre-spend check before the fourth |
| --- | --- | --- |
| Batch 6 measured ($0.0297779/paper) | $0.119 | $0.0894 + $0.05 = $0.139 |
| Conservative estimate ($0.05/paper) | $0.200 | $0.150 + $0.05 = $0.200 |
| **This track's measured batches** | **$0.225784 across 10 papers ($0.0226 each)** | — |

The ceiling first binds at seven papers, so it remains a real guard rather than a
formality. The estimate is also what the exception path charges when a failure occurs after
requests were issued, so the worst case above is genuinely worst-case. No cost limit was
raised silently or otherwise.

## L. Tests and full validation

**666 tests pass** (608 on `main`; 58 added, 57 of them in
`tests/test_paper_scout_computer_vision.py`). No test issues a paid model call or reaches
the network.

Coverage: track registration and default-behaviour preservation; state and output path
isolation; four-way navigation; the pinned relevance fixtures and the three other profiles;
the non-vision gate; the domain-application policy in both directions; competing detector
families; YOLO tagging and the filter-option/tag agreement; metric-name separation; that no
reported number earns relevance; query budgets and sweep survival; discovery fixtures;
idempotency fixtures for every registered track; the seed manifest and seed ingestion
identity check and idempotency; that seeding confers no admission; cross-track identity and
notification isolation; per-track screening of the same paper; research-card relation
field, unextracted fields and topic vocabulary; site build, sidecar schema validation,
navigation, topic filter, About claims, relative-link-only and no-secret guarantees; the
four-track snapshot, three-track migration, repeat migration, partial-archive and
corruption failures, and transport labelling; run/track bounds, no quota transfer, the cost
arithmetic, operational selection and cross-track assessment exclusion; workflow wiring and
the committed-ceiling/code agreement; and that no track-specific string reached any
scientific module. Three of these exist because a check found a real defect rather than
because the area looked risky: every registered track having idempotency fixtures, every
seed note matching by title as well as identifier, and the README's slot arithmetic
matching the planner.

Full sweep, all four tracks:

| Track | Relevance | Quality | Discovery | Idempotency | Build |
| --- | --- | --- | --- | --- | --- |
| agent_memory | 1.000 / 1.000 | 8 fixtures, 0 failures | 6/6 | pass | ok |
| deep_research | 1.000 / 1.000 | 8 fixtures, 0 failures | 4/4 | pass | ok |
| engram | 1.000 / 1.000 | 8 fixtures, 0 failures | 4/4 | pass | ok |
| computer_vision | 1.000 / 1.000 | 8 fixtures, 0 failures | 8/8 | pass | ok |

`check_paper_scout_site.py` (schemas, relative links, exposure, secret scan, workflow
tracks): **0 errors.** `check_generated_file_sizes.py`: pass. `git diff --check`: clean.
PR CI `offline-validation`: pass.

Generated pages were inspected: index shows the two promoted papers under "High-quality
relevant papers", review shows 90 candidates, About carries the scope, metric and coverage
statements, and the Topic control filters as described in section C.

## M. Independent review

Non-Claude reviewer, DeepSeek `deepseek/deepseek-v4-pro-0813` via OpenRouter,
`pr-review --base origin/main`.

**Round 1 — `CHANGES_REQUIRED`.** One blocking finding, one non-blocking, two test gaps.

**Blocking: "Bounded scientific assessment stage omits computer_vision."** Not correct, and
the reviewer flagged it as uncertain itself: 220 of 232 changed files were dropped from its
snapshot for input budget — mostly the generated `docs/computer-vision/` artifacts — so
`paper_scout/cli.py` was never visible to it. Verified two ways: `operational-assess`
accepts no `--track` flag at all (`--help` shows none), and `_operational_assess` builds
`configs = {track: load_config(track_id=track) for track in TRACKS}`. An actual
`operational-assess --dry-run` returns
`selection.tracks = [agent_memory, computer_vision, deep_research, engram]`. The track is in
the daily assessment path.

The reviewer's *suggested guard* was valid and is now implemented, because the workflow
genuinely reads as if the stage might have been missed — every other stage lists its tracks
explicitly. `test_the_daily_assessment_stage_covers_every_registered_track` pins both
halves: the step carries no `--track` narrowing, and a real selection over every registered
track returns a summary for each.

**Non-blocking: "archive and digest publish contradictory per-run counts."** Two separate
things, one of them worth fixing.

The part worth fixing was mine: an earlier local pass ran discovery three times on one date
while the relevance rules were still being tuned, so the digest body mixed rule versions.
The track was rebuilt from empty state in a single pass. The archive now reads *Highly
relevant 38 / Review candidates 57*, which is exactly the store's current classification
and exactly the digest body (38 + 57 = 95 listed items).

The part that remains is pre-existing and deliberately not touched. The Run Summary
(*Relevant 25 / Maybe 62*) counts the 93 papers **that run fetched**; the digest body lists
the **notification-eligible library**, which also contains the 15 seeds ingested outside the
run (two of which the fetch also returned: 25 + 15 − 2 = 38). The same difference is on
`main` for every track — agent_memory's 2026-09-20 digest reports Run Summary 38/64 against
a body of 6/11. Reconciling them means changing the shared digest and archive format for all
four tracks, which is outside this PR's scope.

**Test gaps** — both closed: assessment-stage coverage (above), and the seed/curation
identity gap found while resolving the rebuild
(`test_every_seed_note_matches_by_title_as_well_as_identifier`).

**Round 2 — `CHANGES_REQUIRED`.** Re-run at a 500 KB input budget so source files were not
crowded out by generated artifacts; 39 of 231 files reached it instead of 12. The round-one
blocking finding did not recur. One new blocking finding, two non-blocking.

**Blocking: "generated index cards contradict their own quality assessment."** The symptom
is real — a card badged *Quality reviewed* renders *"Not enough evidence assessed yet"* in
its expanded pane — **and it is pre-existing, already live, and not introduced here.**
Counted on `origin/main`'s committed pages:

| Published page (on `main`) | cards with `quality_status="pass"` | of those, showing "Not enough evidence assessed yet" |
| --- | --- | --- |
| `docs/index.html` | 21 | **17** |
| `docs/deep-research/index.html` | 20 | **15** |
| `docs/engram/index.html` | 6 | 0 |

The cause is in the shared renderer, not in this track. The promotion gate records a
decision as `quality_status="pass"` with `assessment_scope="full_text"` but leaves the
legacy numeric `overall_quality_score` and `recommendation` unset; `_paper_quality_summary`
keys its detail text off those legacy fields and falls back to the no-evidence string when
they are absent. Cards from the older assessor that do carry a numeric score render
correctly, which is exactly why Engram shows none.

Fixing it means changing `paper_scout/site.py` for every track and regenerating three other
libraries' published pages — which §26 forbids this PR from touching and §27 forbids as an
unrelated refactor. It is therefore **filed as separate work** rather than absorbed here or
ignored, including the reviewer's suggestion that `check_paper_scout_site.py` should fail
when a card's rendered quality text disagrees with its sidecar JSON.

**Non-blocking: "README slot budget not updated."** Valid, and mine. The README still said
*"The three normal daily runs use 38 logical search slots combined"*. Corrected to four runs
and 52 slots, with the per-track split, and
`test_the_documented_slot_budget_matches_the_configured_queries` now pins the prose against
the planner so it cannot drift again.

**Non-blocking: counts across digest, archive and latest.** The rule-version half was fixed
by the rebuild (see above). The rest is three different populations by design, on every
track: the Run Summary counts what that run fetched (93), the digest body and archive list
the notification-eligible library including separately ingested seeds (95), and `latest.html`
lists first-seen-this-run papers minus suppressed and insufficient ones (76). Reconciling
them means changing the shared digest, archive and latest formats for all four tracks.

**Round 3 — `PASS_WITH_NOTES`, zero blocking findings.** Two non-blocking notes, one test
gap note.

**Note: "the track's `max_assessments_per_run: 5` may exceed the frozen one-per-track
bound."** A fair reading of a genuinely confusing field, and not a defect. That setting
bounds the discovery-time queue in `paper_scout run`; the daily workflow runs discovery with
`--no-llm`, which disables that queue outright, and assesses through `operational-assess`
under `RunBudget`. The value is inert in the scheduled pipeline, and all four tracks carry 4
or 5. The config now says so at the field, and
`test_no_track_config_can_raise_the_daily_assessment_bound` pins both halves — every
`run --track` line in the discovery step carries `--no-llm`, and the frozen budget is
1 per track and one slot per track overall. The quota is deliberately *not* forced to 1,
because that would change what a manual run does for no gain.

**Note: "the dashboard script dereferences absent quality-filter controls and would throw
`TypeError` on load."** Not correct; the reviewer listed the truncated `index.html` under
its uncertainties. Every access is already guarded (`qualityMinimum ? … : 0`,
`!qualityRecommendation || …`, `.filter(Boolean).forEach`, `if (qualityVisibility)`), and
this is shared pre-existing code that renders the same way on every track. Verified in a
browser rather than by reading: on `index.html`, `latest.html` and `review.html`, all six
quality controls are absent, **the console reports no errors on any of the three**, and
search, sort and the topic filter all work (index: 2 → 2 on "detection", 1 under `yolo`;
latest: 76 → 26 under `yolo`, 16 on "segmentation").

**Test gap: no pre-run live-smoke for this track.** Deliberate, and now stated in the
workflow: Engram has none either, and `check_paper_scout_site.py` actively rejects a
duplicate Engram live smoke. The two existing smokes already exercise every provider this
repository talks to; a third costs 26 more logical search slots against shared throttling
for no new signal, and a provider regression breaks those two first, in the same run, before
the assessment stage.

**Test gap: `paper-scout-checks.yml` does not run `ingest-seeds` for this track.** That
check is the offline PR gate — it builds every track with `--offline` and makes no network
request. `ingest-seeds` performs primary-metadata lookups, so it belongs in the daily
workflow, where it already runs, and not in an offline check.

**Round 4 — `CHANGES_REQUIRED`.** Run on the exact merge candidate after round three's
changes. One blocking finding, and **it was right.**

**Blocking: "a generated HTML detail page is binary."** Confirmed:
`docs/computer-vision/papers/flexxnor-od-…-52fe026d.html` contained **42 NUL bytes**.
`file` reported it as `data`, Git treated it as binary, and a browser may stop parsing at
the first one. The reviewer's guess at the cause was wrong — it is not unsanitized source
metadata. The NULs come from **bounded PDF full-text extraction**: pypdf emits NUL for
glyphs it cannot map, mathematical symbols mostly, and those reach a page through the
scholarly-quality evidence excerpts. The surrounding text on that page is a paper's
throughput equation.

It is pre-existing and was already published. A scan of all generated output found **16
affected files across all four tracks** — 10 under `docs/papers/`, 5 under
`docs/deep-research/papers/`, 1 in this track.

Unlike the round-two renderer finding, this one is fixed here rather than filed, because it
is output corruption rather than presentation, the fix is one choke point, and it changes no
visible content:

- `_page()` strips C0 control characters before the line rstrip, so no generator path can
  bypass it. Stripping *before* `splitlines` matters: that method also breaks on vertical
  tab and form feed, so stripping afterwards would silently turn an unmappable glyph into a
  line break.
- Sidecar JSON is stripped too. `json.dumps` escapes NUL to `\u0000` rather than corrupting
  the file, so that half is data hygiene rather than a correctness fix.
- `check_paper_scout_site.py` now fails on control bytes anywhere in generated output, which
  is the reviewer's suggested guard and covers all four tracks.
- The 15 already-published pages on the other tracks were repaired by applying exactly the
  two steps the generator now performs — strip, then rstrip each line — rather than by
  regenerating them from stale local state. Verified programmatically: every repaired file
  equals that transformation of its committed version, and the visible text is unchanged.

**Non-blocking: "arXiv discovery failed for every query in the committed run."** True, and
already section F and limitation 1. The reviewer asks whether the client sends the same
headers as the existing tracks: it does — same `ArxivFetcher`, same `HttpClient`, same
`paper-scout/0.1` user agent, same query builder. The failures are rate-based rather than
query- or track-specific, which an isolated probe showed directly: a bare `cat:cs.CV`
request from this host succeeded while the identical request through the scout failed
minutes later, and by the end of the session even `id_list` lookups were refused. Degraded
coverage is reported rather than hidden: every failed query is a source warning in the
digest and in `discovery-run-*.json`, and the run's `coverage_complete` is `false`.

**Round 5 — `PASS_WITH_NOTES`, zero blocking findings and zero non-blocking findings.**
Run on the control-byte fix. Three test-gap notes and one uncertainty.

Two of the three test gaps were already closed and invisible to the reviewer through
truncation: legacy two-track and three-track restore/upgrade tests exist in
`test_paper_scout_engram_state.py` and `DurableState` here, and the offline
`computer_vision` build already runs in `paper-scout-checks.yml`. The third — a headless
test of the page script with the quality controls absent — is not added: it needs a browser
dependency this repository does not carry, and the behaviour was verified in a real browser
instead (round three).

One gap was real and is closed. The new control-byte guard was itself untested: every
generated file is clean, so "no file contains control bytes" would pass even if the check
were broken. `test_the_site_check_flags_control_bytes_instead_of_silently_decoding_them`
now feeds it a corrupt file and asserts the flag, the occurrence count, and that tab,
newline and carriage return are not flagged.

**The uncertainty was worth checking and is now pinned.** The reviewer asked whether the
weekly backfill could be asked to snapshot `data/computer_vision/paper_scout.sqlite3` before
it exists. It cannot, but the reasoning spans two modules, so it is now a test rather than
an argument: whichever workflow runs first after this merges restores a snapshot that
predates the track, and `restore_snapshot` initializes the missing database, so the
subsequent `pack_snapshot` — which verifies every path in `STATE_PATHS` — succeeds.
`test_restoring_a_legacy_snapshot_leaves_state_that_can_be_persisted` runs that exact
sequence end to end.

**Verdict for the merge gate: `PASS_WITH_NOTES`, 0 blocking findings, 0 non-blocking
findings.** Two tests were added afterwards; the product code is unchanged from the reviewed
commit, so nothing material is unreviewed.

### Convergence

| Round | Verdict | Blocking | Disposition |
| --- | --- | --- | --- |
| 1 | `CHANGES_REQUIRED` | 1 | Incorrect — the assessment stage does cover the track; the reviewer's snapshot omitted `cli.py`. Its suggested guard implemented anyway. |
| 2 | `CHANGES_REQUIRED` | 1 | Real but pre-existing and already live; fixing it changes the shared renderer and three other libraries, so **filed as separate work**. |
| 3 | `PASS_WITH_NOTES` | 0 | One note valid (README arithmetic, fixed); one incorrect (script guards), disproved in a browser. |
| 4 | `CHANGES_REQUIRED` | 1 | **Correct.** 42 NUL bytes in a published page, pre-existing across 16 files. Fixed at the choke point, guard added, published pages repaired. |
| 5 | `PASS_WITH_NOTES` | 0 | No findings. One real test gap closed, one uncertainty converted into a test. |

No escalation to Kimi or Qwen was needed; DeepSeek converged in five rounds.

## N. Production smoke

Two runs, because the first one failed.

### First attempt — [35594457409](https://github.com/vernerisirva/agentmempaper/actions/runs/35594457409): FAILED

Restore and every validation passed, then the run threw the day away. Two Computer Vision
seeds did not resolve, `ingest-seeds` exited 1, and under `set -e` that aborted the
discovery step — so assessment, the site build, the Pages deploy and the state persist were
all skipped, for all four tracks, because of two papers. No state was lost, because persist
was skipped; the run simply did nothing, and would have repeated daily.

**The merge was premature.** The gate — tests, review, mergeability — was satisfied, and it
was still not enough, because nothing in it exercised the seed bootstrap against live
providers. That is a gap in how the track was validated, not in the gate as written.

Fixed in [#44](https://github.com/vernerisirva/agentmempaper/pull/44): `ingest-seeds` gained
`--allow-unresolved`, which reports unresolved ids as an error annotation and exits 0, and
both workflows pass it. A manual run still exits 1. Engram's bootstrap carried the identical
exposure and had simply never fired, because its four seeds were already in state.

Before merging that fix, the failure path was verified against live providers on isolated
copies of all four databases: exit 0 with the flag, exit 1 without, the wrong paper never
written, the scheduled sequence continuing past the unresolved seed, and the repository's
own databases byte-identical afterwards.

### Second attempt — [35621364675](https://github.com/vernerisirva/agentmempaper/actions/runs/35621364675): SUCCESS

Every step succeeded, and the failure path fired for real: three Computer Vision seeds were
unresolved and the run continued anyway.

| Verification | Result |
| --- | --- |
| Unresolved seeds do not abort the run | 3 unresolved (`1506.02640`, `2005.12872`, `2304.02643`); discovery step **succeeded** |
| Reported loudly | GitHub `failure`-level annotation: *"computer_vision seed bootstrap left unresolved IDs: … Discovery continues; the next run retries them."* |
| All four tracks' discovery continues | agent_memory 417 fetched, deep_research 100, engram 77, **computer_vision 100** — all after the unresolved seed |
| Assessment stage normal | 7 walked, 3 assessed, **2 promoted**, 1 not; one paper each from agent_memory, computer_vision and deep_research |
| Bounds honoured | 1 per track, 3 total ≤ 4; Engram nominated nothing and forfeited its slot rather than lending it |
| Cost | $0.118116 against the unchanged $0.30 ceiling |
| Private state persists | restored manifest v2, persisted manifest v2 — **now carrying `data/computer_vision/paper_scout.sqlite3`** |
| Pages builds and deploys | deploy `success`; `/computer-vision/` returns **HTTP 200** |
| Seeds stay retryable, not wrongly filled | "Micrograph segmentations for DDEVD" appears in **0** published files; all three unresolved anchors absent rather than substituted |

The state transition is the migration completing in production: the restore carried the
three-track snapshot, `computer_vision` was initialized, and the persist wrote all four.

`2304.02643` is the interesting failure. OpenAlex answers that identifier with an entirely
different paper, and the manifest's identity check refused it. The library would rather
leave Segment Anything missing than publish the wrong manuscript under its id — which is
the behaviour worth having, and it is now visible in production rather than theoretical.

## O. Live URL

<https://vernerisirva.github.io/agentmempaper/computer-vision/>

## P. Limitations and backlog

1. **Local discovery was provider-limited.** arXiv returned 406 for every search from this
   host — and by the end of the session for `id_list` lookups too — and Semantic Scholar
   429s without a key, so the initial corpus is OpenAlex-dominated and under-represents
   arXiv preprints, including the `cs.CV` sweep that carries the track's breadth. The first
   scheduled run on a GitHub runner is the first real exercise of those paths.
   **One foundational seed, `1506.02640` (the original YOLO paper), is consequently
   missing** from the committed corpus: arXiv is the only route that can resolve it, since
   OpenAlex genuinely 404s on `10.48550/arXiv.1506.02640` rather than throttling. Twelve
   spaced retries over the session did not succeed. The daily workflow bootstraps missing
   seeds on every run, so this resolves on the first scheduled run; verify it there.
2. **Resolved.** The local corpus never reached production state, as expected; production
   built its own from empty state on run 35621364675 and now publishes 92 papers. The
   committed `docs/computer-vision/` is that production build.
3. **Resolved.** The scheduled run rebuilt all four libraries from restored production
   state, so the Computer Vision navigation link is now live across them.
4. **Screening imprecision, both directions.** Vision-transformer applications outside the
   named domain list can score as relevant, and a survey or an application whose title
   avoids the pattern vocabulary can fall to irrelevant rather than review. The domain list
   is a keyword list and will need occasional extension; it is honest about being one.
5. **The `cs.CV` sweep sees a truncated window.** 300 records in one request cannot cover
   ten days of a category that large. This is reported as `incomplete_window` rather than
   hidden, but raising it means either more requests or accepting the bound. Revisit after
   observing real sweep volume on the runner.
6. **Research-card fields stay largely unextracted.** `key_contribution` and
   `evidence_or_evaluation` are "Not extracted yet" for most papers, as policy requires.
   Detection-specific structured fields — task, datasets, mAP variant, latency evidence —
   would need manuscript extraction, which is a separate change to the card pipeline rather
   than to this track.
7. **No live-smoke step** for this track, matching Engram, so provider reachability is
   only exercised by the daily discovery run itself. Deliberate — the two existing smokes
   cover every provider this repository talks to, and the workflow now says so — but it
   does mean a `cs.CV`-specific arXiv regression would first appear as a discovery warning
   rather than as a pre-run failure.
8. **A pre-existing renderer defect is now documented but unfixed** (round-two blocking
   finding): promoted cards whose assessment carries no legacy numeric score render
   "Not enough evidence assessed yet". It affects 17 of 21 and 15 of 20 promoted cards on
   the two largest live libraries today, and it will affect this track's promoted cards
   identically. Filed as separate work because the fix is in the shared renderer.

---

COMPUTER_VISION_TRACK_READY: YES
COMPUTER_VISION_OPERATIONAL_ASSESSMENT_ENABLED: YES
