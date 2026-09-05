# Engram track — implementation and local validation

Validated 2026-09-05 on branch `add-engram-paper-track`, created from freshly
fetched `origin/main` at `62a455ba5`. The starting checkout was clean. No feature
branch was merged, and no push, PR, deployment, remote workflow or notification
was performed. GitHub runtime-state access was read-only.

## Implemented scope

The third track uses `config/tracks/engram.yaml`, independent curation and SQLite
state, `digests/engram/`, `reports/paper_scout/engram/` and `docs/engram/`. It reuses
the existing query planner, canonical ingestion, failed-query recovery, backfill,
quality interfaces and shared static renderer. Unknown tracks/config mismatches
fail explicitly. Default commands remain compatible.

Relevance requires substantive title/abstract evidence of model-integrated
conditional memory, hashed n-grams or learned lookup tables, with architectural
study/reader evidence. Transfer/grafting vocabulary alone is insufficient.
Engram name collisions, citation-only mentions, biological engrams, generic
RAG/chat history, fine-tuning and distillation do not qualify automatically.
Concrete adjacent neural memory mechanisms remain review candidates. Efficiency,
offloading and negative-result studies are eligible. Relevance is independent of
methodological quality; deterministic quality uses no credentials or model calls.

Shared navigation reaches all three libraries from the main and detail pages.
The single paper list, search, sorting, New-only control, primary Open paper link,
secondary Research card link, collapsed metadata/diagnostics and shared style are
preserved. Newness uses actual timestamps, normalizes offsets and rejects future,
malformed and date-only evidence. Revision/source-update metadata is additive;
`paper-scout-card-v2` remains compatible. The pre-existing relation key is retained
with Engram-specific visible wording. Curation identifies abstract-level evidence
and unsupported structured fields remain unextracted.

## Live seeds and discovery

All four primary arXiv records were actually retrieved on 2026-09-04 UTC using
normal TLS verification. These are live recovery results, separate from fixtures.

| arXiv ID | Primary title | Initial submission | Latest revision | Final screening |
| --- | --- | --- | --- | --- |
| [2601.07372](https://arxiv.org/abs/2601.07372) | Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models | 2026-01-12 | 2026-07-12 | Highly relevant |
| [2605.20948](https://arxiv.org/abs/2605.20948) | Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory | 2026-05-20 | 2026-05-20 | Highly relevant |
| [2607.29065](https://arxiv.org/abs/2607.29065) | Tokenizer-Agnostic Engram Module | 2026-07-31 | 2026-07-31 | Highly relevant |
| [2608.17050](https://arxiv.org/abs/2608.17050) | Cross-Model Memory Transfer via Target-Side Reader Adaptation | 2026-08-17 | 2026-08-19 | Highly relevant |

Unresolved seeds: **0**. A repeated `ingest-seeds` invocation used saved state,
made zero metadata requests and preserved entry/notification history. The current
[seed report](seed-ingestion.json) labels this cache-only verification. During
implementation the transfer paper exposed a cross-sentence evidence miss; the
generic rule was corrected and its actual saved metadata re-screened without
changing first-seen time or introducing a bibliographic special case.

One bounded live daily discovery run (`run --track engram --no-notify`, run ID 1)
produced these actual provider outcomes:

| Provider | Logical queries | Raw records | In-window sightings | Unique stored identities | HTTP attempts | Outcome |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| arXiv | 4 | 73 | 6 | 4 | 4 | Success; two additional core papers |
| OpenAlex | 4 | 76 | 76 | 72 | 4 | Three windows truncated at 25 records; no additional included paper |
| Semantic Scholar | 4 | 0 | 0 | 0 | 12 | HTTP 429 on every query, including two HTTP retries each |

Total: **82 candidate sightings, 76 unique discovery candidates, 20 HTTP
attempts including 8 retries**. There were no extra pagination or metadata
requests in this live run. Seven incomplete/failed queries remain in the retry
store. Raw failures are not treated as successful source coverage merely because
the CLI completed. Per-query evidence is in
[discovery-run-1.json](discovery-run-1.json).

The resulting Engram database holds **80 candidates: 6 highly relevant, 0 review
candidates and 74 excluded**. All six included records are from arXiv. In addition
to the four seeds, the library includes:

- [When to Adapt: Conditional Memory Adapters for Retention-Preserving Domain Specialization](https://arxiv.org/abs/2608.29327), submitted 2026-08-29.
- [Lngram v2: Latent N-Gram Memory with Interpretable Discrete Representations](https://arxiv.org/abs/2609.03426), submitted 2026-09-03.

Six deterministic quality records exist. Total model calls and notifications
sent during this task: **0**. No full-text/PDF extraction was performed for Engram.

## Budgets and limitations

The steady-state increment is four logical discovery slots per provider (12
combined), one page of at most 25 records per query, up to two HTTP retries per
request, and at most four extra metadata lookups across the whole run. This caps
steady-state discovery/enrichment at 48 HTTP attempts. Failed-query retries
consume those same slots. Missing seed bootstrap adds up to four primary lookups
and four DOI fallback lookups, each with at most three attempts; known seeds add
zero requests. Quality is capped at four deterministic assessments per scout run
and four additional initial seed assessments; default model-call increment is
zero. Engram site generation performs no network enrichment.

The existing provider throttles now share hostname timing across clients in a
process. Account quotas still span the sequential tracks; normal daily plans total
38 logical queries, plus 26 from the two pre-existing live-smoke steps. No extra
Engram smoke or category sweep was added.

The historical `backfill --track engram --since 2026-01-12 --no-notify` operation is
supported and fixture-tested but **was not run live**. It remains bounded and
cannot establish complete historical coverage. Single-page caps, query wording,
index delays and Semantic Scholar throttling limit recall. The default recent
search follows providers' existing publication-window behavior; it does not
promise to rediscover every revision of an old paper. Direct revised-ID ingestion
is deduplicated. Abstract-based quality is triage, not full-paper review. The
original library builds retained their existing date-enrichment behavior and
reported a Crossref 404 and SSRN 403; no dates were invented in response.

## Durable state

Daily and weekly workflows include Engram seed bootstrap, discovery/backfill,
validation, rendering, report collection and snapshot preparation/upload. The
archive allowlist contains all three database paths and a SHA-256 manifest.
Restore validates every file before replacing state; unexpected paths, links,
corruption, missing required files, checksums and unavailable release access fail
closed. The exact older two-database format remains accepted and initializes only
missing Engram state. Existing Engram data is preserved during legacy restores.

A real older release snapshot restored the two original databases while keeping
local Engram state. A subsequent real **three-track fresh-runner round trip
matched database bytes exactly**, including these counts:

| Database | Papers | Notifications | Failed-query rows |
| --- | ---: | ---: | ---: |
| Agentic Memory | 16,432 | 2,515 | 13 |
| Deep Research | 2,104 | 342 | 9 |
| Engram | 80 | 0 | 7 |

Databases, caches, PDFs, credentials, temporary files and SQLite sidecars stay
outside Git and the public Pages artifact. All workflow writers retain the shared
concurrency group and generated-output-only staging policy.

## Validation

- `python3 -m unittest discover -s tests -p 'test_paper_scout_*.py'`: **158 passed**.
- `python3 -m unittest discover -s tests -p '*.py'`: **160 passed**.
- All three tracks: `evaluate-relevance`, `evaluate-discovery`, `evaluate-quality`,
  `validate-idempotency`, and `build-site`: **passed**.
- Default commands without `--track`: relevance, discovery, quality, idempotency,
  and a saved-metadata site build: **passed**.
- Engram relevance fixtures: **20 fixed regression examples**, including the four
  primary-record fixtures; precision/recall 1.000 and no exact decision mismatches.
  These numbers are regression-set results, not measured production recall.
- Discovery fixtures: Agentic Memory 6/6, Deep Research 4/4 representative query
  routes, Engram 4/4 including explicit seed-manifest routes. Direct-ID capability
  alone is not counted as actual Engram seed discovery.
- Quality regression: 8/8 for each track, using the existing shared rubric.
- Idempotency: first mock run 2 entries, repeated run 0 for each track; seed,
  revised-ID, DOI alias and backfill notification tests also pass.
- All **1,928 generated sidecars** validate against the published schema. All
  relative HTML links, exports and workflow configuration checks pass.
- Generated-output secret/private-path/runtime scan, file-size guard, shell syntax
  checks and `git diff --check`: **passed**.
- Browser inspection verified shared styling, search, New-only filtering and
  explicit publication sorting; no browser console errors were observed.
- Rebuild preservation: Agentic Memory stays at **1,729** public records and Deep
  Research at **193**, with identical membership, titles, relevance decisions,
  publication dates, first-seen timestamps and curation notes versus the base.
  Rebuilding the root also leaves both nested tracks' files intact in tests.

## Changed files and example cards

Principal additions are `config/tracks/engram.yaml`, `config/curation/engram.yaml`,
`config/seeds/engram.json`, `config/fixtures/engram-seeds.json`,
`paper_scout/engram.py`, `engram_evaluation.py`, `ingestion.py`, `seeds.py`,
`runtime_snapshot.py`, three Engram test modules, the generated-site validation
script and `requirements-dev.txt`. Shared config/CLI, discovery/relevance
evaluation, fetcher diagnostics, HTTP accounting, state identity, site/card
rendering, workflow and snapshot scripts were extended. README and
`docs/decisions.md` document scope and operations. Runtime requirements are
unchanged; `jsonschema` and `PyYAML` are explicit validation-only dependencies.

Generated changes span all three `docs/` trees because navigation and additive
date exports apply to existing paper pages too. The new digest and reports are
track-isolated. No original library's membership or screening was relabeled.

Example Engram cards:

- `docs/engram/papers/conditional-memory-via-scalable-lookup-a-new-axis-of-sparsity-for-large-language-mod-800bec78.html` and `.json`
- `docs/engram/papers/cross-model-memory-transfer-via-target-side-reader-adaptation-f71b90ae.html` and `.json`
- `docs/engram/papers/tokenizer-agnostic-engram-module-ab1608f7.html` and `.json`

The local implementation is ready for review. Publishing remains a separate,
explicit action.
