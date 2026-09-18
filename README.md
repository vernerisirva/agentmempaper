# Paper Scout

Paper Scout is a local-first daily research-monitoring agent for papers related to agentic memory, LLM agent memory, memory mechanisms for long-running or deep-research agents, and Engram-style or parametric-memory mechanisms when they connect to language-model behavior.

It fetches candidates from arXiv, Semantic Scholar, and OpenAlex; deduplicates canonical papers; classifies relevance with deterministic rules by default; stores state in SQLite; and writes Markdown digests under `digests/`.

## Scope

The default config in `config/paper_scout.yaml` tracks:

- agentic memory, persistent memory, episodic/semantic/procedural memory, memory policies, and agent-memory benchmarks;
- deep research agents, autonomous research agents, and literature-review agents;
- Engram, Megatron-LM Engram, parametric memory, model-internal memory, and memory mechanisms.

The Engram/Megatron-LM context is treated as research context, not as proof that Engram-style approaches cannot work.

## Three independent libraries

| Track | Site output | State | Curation |
| --- | --- | --- | --- |
| `agent_memory` (default) | `docs/` | `data/paper_scout.sqlite3` | `config/curation.yaml` |
| `deep_research` | `docs/deep-research/` | `data/deep_research/paper_scout.sqlite3` | `config/curation/deep_research.yaml` |
| `engram` | `docs/engram/` | `data/engram/paper_scout.sqlite3` | `config/curation/engram.yaml` |

Each track has its own relevance, notes, notification history and first-seen timestamps. Bibliographic overlap is allowed. The explicit registry rejects unknown tracks and mismatched config IDs. Existing default commands remain Agentic Memory commands. Navigation derives relative paths for every registered track, including detail pages.

The Engram library concerns memory integrated with language-model computation: conditional memory, learned lookup tables, hashed n-grams, memory readers and gates, frozen-memory transfer, tokenizer-independent addressing, memory grafting, capacity scaling, training, editing and efficient execution. It requires substantive title/abstract evidence and does not require the word “agent”. An Engram mention, generic parametric memory, or a related-work citation alone does not establish relevance. Adjacent neural memory layers, product-key memories, model-memory editing and test-time memory may remain review candidates. Biological engrams, unrelated software, generic RAG/chat history and generic fine-tuning/distillation are excluded. Negative results and memory-table offloading studies are eligible; relevance and methodological quality are separate.

Engram generates the same index, latest, archive, about, JSON/CSV/BibTeX exports, schema and per-paper HTML/JSON cards as the existing libraries. Its intended Pages path after deployment is [the Engram library](https://vernerisirva.github.io/agentmempaper/engram/). The sidecar schema stays `paper-scout-card-v2`; the existing `relation_to_agentic_memory` key has track-appropriate visible wording. Seed curation is explicitly based on primary abstracts, with unsupported architectural/evaluation fields unextracted. Implementation discussions are separate links on About, without automatic GitHub monitoring.

### Engram bootstrap and historical recovery

```bash
python3 -m paper_scout ingest-seeds --track engram
python3 -m paper_scout run --track engram --no-notify
python3 -m paper_scout build-site --track engram
# Explicit one-time historical search; never run automatically each day:
python3 -m paper_scout backfill --track engram --since 2026-01-12 --no-notify
```

`config/seeds/engram.json` declares four foundational arXiv IDs, expected titles and the historical start. `ingest-seeds` reuses canonical metadata ingestion outside the recent-publication window. It validates identity and complete dates/abstract/authors, reports unresolved records, skips known records without metadata requests, and never sends or marks notifications. Initial submission, latest revision and actual entry time remain distinct. The normal daily run may notify an unnotified seed once. A new arXiv version or later bibliographic alias resolves to the existing record and notification history.

The daily and weekly workflows bootstrap missing seeds. Weekly Engram backfill uses 45 days and the existing provider planner/retry store. The explicit `--since` operation uses that same bounded planner over a longer window; it is not an exhaustive sweep, and capped windows remain reported as incomplete. Failed-query retries consume normal query slots. Search terms are relevance/discovery vocabulary, not a request-per-term list.

“New” requires a real first-seen timestamp within 24 hours of the build time. Timezone offsets are normalized and future, malformed or date-only values cannot create a New badge. Foundational publication dates remain historical. Non-arXiv source-update dates are exposed separately and are not described as paper revision dates.

### Incremental Engram budgets

| Operation | Limit |
| --- | --- |
| Logical discovery queries | 4 per provider per daily or weekly run; 12 total, including due failed-query retries |
| Pagination | 1 page per query, up to 25 records; no extra page requests or category sweep |
| HTTP retries | Up to 3 total attempts per request (2 retries), counted separately |
| Metadata enrichment | At most 4 Semantic Scholar → arXiv lookups across the entire run, each within the same retry limit |
| Missing seed ingestion | 4 primary arXiv lookups; at most 4 OpenAlex DOI fallbacks if primary requests fail; no requests for known seeds |
| Quality assessments | Up to 4 per scout run; initial seed bootstrap can add 4 deterministic assessments |
| Model calls | 0 by default for relevance and quality; no new provider or required key |
| Full-text/site enrichment | 0 for Engram by default; rendering uses saved metadata |

Steady-state Engram discovery therefore permits at most 48 HTTP attempts (36 search + 12 metadata) and bootstrap can add at most 24 attempts. Successful no-retry search usually needs 12 requests. Provider throttling is shared by hostname across clients in a process, including arXiv metadata enrichment. The workflows execute tracks sequentially in the existing shared writer-concurrency group; an extra track does not imply a separate account quota. The three normal daily runs use 38 logical search slots combined. The two existing pre-run live-smoke checks add 26 slots; Engram has no duplicate live-smoke step. Quality remains optionally configurable through the existing interfaces; switching to a model-backed mode requires an explicit call budget and the existing provider credentials.

Per-query raw counts, accepted candidates, page limits, truncation, attempts, retries and metadata requests are saved in `reports/paper_scout/engram/discovery-run-<run-id>.json`. These are bounded coverage diagnostics, not estimates of literature recall. Fixed regression results are labeled separately from live retrieval.

### State compatibility and validation

Durable archives now contain a SHA-256 manifest and all three allowlisted SQLite files. Every member and database is checked before restoration. A valid legacy archive containing exactly the two original databases is accepted and initializes only missing Engram state; existing Engram state is preserved. A corrupt, incomplete or unavailable snapshot fails closed. Missing original state cannot silently become an empty library. State stays outside Git and the public Pages artifact.

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -p 'test_paper_scout_*.py'
python3 -m unittest discover -s tests -p '*.py'
for track in agent_memory deep_research engram; do
  python3 -m paper_scout evaluate-relevance --track "$track"
  python3 -m paper_scout evaluate-discovery --track "$track"
  python3 -m paper_scout evaluate-quality --track "$track"
  python3 -m paper_scout validate-idempotency --track "$track"
  python3 -m paper_scout build-site --track "$track"
done
python3 .github/scripts/check_paper_scout_site.py
python3 .github/scripts/check_generated_file_sizes.py digests docs reports/paper_scout
git diff --check
```

`build-site --offline` is available for saved-metadata validation of any track; existing tracks retain online date enrichment by default. See the [Engram implementation validation report](reports/paper_scout/engram/implementation-validation.md) for actual retrieval, limitations and local validation results.

## Setup

Paper Scout requires Python 3.11 or newer. The runtime dependency is `pypdf`, used for bounded open-access full-text extraction. Tests and generated-site validation additionally use `jsonschema` and `PyYAML` from `requirements-dev.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Commands

Run the normal daily scout:

```bash
python3 -m paper_scout run
```

Search without writing state:

```bash
python3 -m paper_scout search --days 7
```

Recover papers missed during provider outages or indexing delays without sending notifications:

```bash
python3 -m paper_scout backfill --track agent_memory --days 45 --no-notify
```

Ingest a researcher-identified paper through the normal deduplication and relevance pipeline:

```bash
python3 -m paper_scout ingest-paper --track agent_memory --arxiv-id 2607.01480
python3 -m paper_scout ingest-paper --track agent_memory --doi 10.48550/arXiv.2607.01480
```

Inspect unresolved provider queries and run fixture-based discovery regression coverage:

```bash
python3 -m paper_scout failed-queries --track agent_memory
python3 -m paper_scout evaluate-discovery --track agent_memory
```

Render a digest from stored papers:

```bash
python3 -m paper_scout digest --date 2026-06-26
```

Evaluate deterministic relevance fixtures:

```bash
python3 -m paper_scout evaluate-relevance
```

Evaluate the separate scholarly-quality rubric and reassess stored papers:

```bash
python3 -m paper_scout evaluate-quality --track agent_memory
python3 -m paper_scout evaluate-quality --track deep_research
python3 -m paper_scout reassess-quality --track agent_memory --days 30
python3 -m paper_scout reassess-quality --track agent_memory --paper-id doi:10.0000/example --force
python3 -m paper_scout reassess-quality --track agent_memory --assessment-version quality-promotion-v1 --rubric-version scholarly-rubric-v1
python3 -m paper_scout reassess-quality --track agent_memory --model your-quality-model --force
python3 -m paper_scout reassess-quality --track agent_memory --no-full-text --no-llm
python3 -m paper_scout reassess-quality --track agent_memory --report-only
```

Validate idempotent notification behavior:

```bash
python3 -m paper_scout validate-idempotency
```

Run a local live-source smoke test without notifications:

```bash
python3 -m paper_scout smoke-live --days 14 --max-results-per-source 25 --no-notify
```

Run CI-mode live-source smoke validation, writing Markdown and JSON reports:

```bash
python3 -m paper_scout smoke-live --days 14 --max-results-per-source 25 --no-notify --ci
```

Build the static reading dashboard:

```bash
python3 -m paper_scout build-site
```

Reports are written under `reports/paper_scout/`.

Paper Scout also supports separate monitoring tracks. Commands without `--track` remain backward compatible and run the `agent_memory` track. The deep research track uses its own search terms, relevance rubric, curation file, SQLite state, reports, digests, and dashboard:

```bash
python3 -m paper_scout run --track deep_research
python3 -m paper_scout build-site --track deep_research
python3 -m paper_scout evaluate-relevance --track deep_research
python3 -m paper_scout validate-idempotency --track deep_research
```

Track config lives in `config/tracks/`. The current agent-memory dashboard remains at `docs/index.html`; the deep research dashboard is generated under `docs/deep-research/index.html`.

## Live Smoke Reports

`smoke-live` is a validation command, not a notification command. It initializes the SQLite schema, fetches live payloads, classifies normalized candidates, runs the idempotency validator in a temporary directory, and writes a human-readable Markdown report.

In `--ci` mode it also writes:

```text
reports/paper_scout/live-smoke-YYYY-MM-DD.json
```

The JSON report includes `run_id`, `date`, `ci`, `sources_attempted`, `sources_succeeded`, `sources_failed`, `total_raw_records`, `total_candidates`, `unique_candidates`, relevance counts, `source_errors`, `state_initialized`, `idempotency_passed`, and per-source details.

Source outcomes are separated so real zero-result responses are not confused with failures:

- success with one sample normalized candidate when available;
- success with zero results;
- HTTP/API error;
- TLS/certificate error;
- timeout/network error;
- parsing/conversion error;
- provider error.

The command does not send email or webhook notifications and does not mark papers as notified.

## Discovery And Recovery

Discovery queries are intentionally separate from the larger relevance vocabulary. Each source receives a small, deduplicated plan with a request budget; arXiv supports phrase, all-terms, and raw query modes. The Agentic Memory track also performs one bounded recent-category sweep over `cs.AI`, `cs.CL`, and `cs.LG`. Every broadly retrieved candidate still passes through the normal conservative relevance classifier.

Failed source queries are persisted in the track's SQLite state with bounded exponential retry timing. Daily runs retry due failures within the source budget. A separate weekly 45-day Agentic Memory backfill workflow recovers papers missed through outages or indexing delays, preserves the publication date, records the actual recovery time as `first_seen_at`, and does not notify by default. That backfill workflow can also be triggered manually.

`evaluate-discovery` writes `discovery-eval-YYYY-MM-DD.md` in the track report directory. It is synthetic regression coverage for known retrieval routes, not an estimate of production discovery recall.

## State Strategy

- Default persistent state: `data/paper_scout.sqlite3`.
- Deep research persistent state: `data/deep_research/paper_scout.sqlite3`.
- Override state with `PAPER_SCOUT_STATE_PATH`.
- Track-specific state can also be overridden with `PAPER_SCOUT_AGENT_MEMORY_STATE_PATH` or `PAPER_SCOUT_DEEP_RESEARCH_STATE_PATH`.
- `data/.gitkeep` keeps the state directory present.
- SQLite sidecar files are ignored: `*.sqlite3-journal`, `*.sqlite3-wal`, and `*.sqlite3-shm`.
- Runtime SQLite state is ignored and never committed. The scheduled daily and weekly workflows restore and replace one `paper-scout-runtime-state` GitHub Release asset after generated outputs have been committed successfully. A release asset is used instead of Actions cache because the state controls deduplication and the complete site library, so cache eviction would be unsafe.
- The migration's first missing release bootstraps state from the explicitly named final Git-tracked commit (`026158c36d109669e16b1c008b69d1031a2a357b`), not merely the current parent. This preserves accumulated state even if another normal commit lands before the first workflow run. The fallback emits a workflow warning and is intended only for recovery; it may not contain work completed after that seed.
- State writers share one queued workflow-concurrency group. Before each durable upload, the workflow verifies SQLite integrity, checkpoints WAL mode into the main database, switches it to rollback-journal mode, and removes sidecars. Do not delete the `paper-scout-runtime-state` release while scheduled workflows are active.
- If the durable-state upload fails after source output has been pushed, the workflow fails loudly. The next run restores the previous durable snapshot and can reprocess recent papers (at-least-once recovery) rather than silently losing them; rerun the failed workflow promptly to minimize duplicate digest entries.
- Before staging generated output, both workflows reject files at or above 95 MiB with a clear diagnostic. Runtime state is explicitly excluded from `git add` and checked again after staging.
- CI live smoke uses a temporary state path so validation does not mutate the daily state file.

Local smoke-test state files that contain no useful real paper data should not be committed.

## Notification Semantics

Paper Scout enforces "not before found" through the `notifications` table:

- canonical identity prefers DOI, then arXiv ID, Semantic Scholar ID, OpenAlex ID, then normalized title + first author + year;
- only papers that are relevant or maybe relevant and not already notified are included in a new digest;
- papers are marked notified only after digest generation succeeds and enabled notifications succeed;
- when email and webhook notifications are disabled, successful digest writing is enough to mark papers notified;
- if email or webhook notification is enabled and fails, papers remain unnotified so the next run can retry;
- rerunning the same fetched data should not duplicate digest entries or notifications.

## Environment Variables

Required: none for deterministic local operation.

Optional source settings:

- `SEMANTIC_SCHOLAR_API_KEY`: raises Semantic Scholar rate limits. In GitHub Actions, add a repository secret with this exact name; the workflow passes it through to both live smoke validation and the daily run.
- `OPENALEX_MAILTO`: polite-pool contact email for OpenAlex.

Optional state/output setting:

- `PAPER_SCOUT_STATE_PATH`: override the SQLite state file.

Optional OpenAI-compatible classifier:

- `PAPER_SCOUT_LLM_API_KEY` or `OPENAI_API_KEY`
- `PAPER_SCOUT_LLM_PROVIDER=auto`
- `PAPER_SCOUT_LLM_MODEL`
- `PAPER_SCOUT_LLM_BASE_URL`, default `https://api.openai.com/v1`
- `PAPER_SCOUT_QUALITY_LLM_MODEL`, optional model override for scholarly-quality validation; it reuses the same provider, API key, and base URL

Optional notifications:

- `PAPER_SCOUT_WEBHOOK_URL`
- `PAPER_SCOUT_SMTP_HOST`
- `PAPER_SCOUT_SMTP_PORT`
- `PAPER_SCOUT_SMTP_STARTTLS`
- `PAPER_SCOUT_SMTP_USERNAME`
- `PAPER_SCOUT_SMTP_PASSWORD`
- `PAPER_SCOUT_EMAIL_TO`
- `PAPER_SCOUT_EMAIL_FROM`

Secrets are never written to smoke reports. If Semantic Scholar returns HTTP 429, Paper Scout treats it as a source warning rather than a run failure. Configure `SEMANTIC_SCHOLAR_API_KEY` for higher rate limits; if rate limits still occur, the run continues with arXiv/OpenAlex and any other available sources.

## Digest Quality

The daily run writes an advisory report:

```text
reports/paper_scout/digest-quality-YYYY-MM-DD.md
```

It flags likely false positives when digest papers mention infrastructure-memory terms such as GPU memory, CUDA memory, memory bandwidth, memory allocation, memory-efficient attention, operating-system memory, or database memory without strong agent-memory terms such as agent memory, LLM agent, autonomous agent, deep research agent, persistent memory, episodic memory, semantic memory, Engram, or parametric memory.

This report does not fail the workflow by default. It is a triage aid for keeping the daily digest useful.

## Scholarly Quality Assessment

Paper Scout separates topical relevance, publication status, and scientific-quality screening across `agent_memory`, `deep_research`, and `engram`.

**Main-library admission:** `relevance_decision == relevant AND scholarly_quality.status == pass`, subject to explicit curation exclusion/suppression. Discovery remains broad. Pinning, a score override, a DOI, peer review, or institutional affiliation cannot bypass this rule. Ranking uses topical relevance and the existing date/New ordering; quality is a gate, not a prestige leaderboard.

The existing versioned `QualityAssessment` and SQLite assessment history are reused. Scientific status is `pass`, `uncertain`, `insufficient`, or `not_assessed`. Additive card-v2 fields retain status, concise rationale, uncertainty, gate version, assessor, timestamp, source hash, full-text scope and URL. Publication status (`peer_reviewed`, `preprint`, `repository_only`, `unknown`) has separate source evidence. Venue metadata is an inference about publication, never a quality pass; DOI registration and repository labels do not demonstrate external review.

A manuscript-based pass requires located evidence of contribution clarity, methods, validation addressing the central claims, appropriate comparisons or a justified absence, claim/evidence alignment, and limitations. Expectations depend on paper type: theory, surveys and conceptual work need suitable scientific argument or synthesis, not necessarily experiments. Public code is helpful, not mandatory. Author identity, affiliation, employer, university, country and prestige are not quality criteria. Strong independent preprints and repository manuscripts can pass; weak institutional or peer-reviewed work can fail. Screening does not prove scientific correctness.

New assessments use `quality-promotion-v1` / `dual-promotion-v2`. The primary assessor
and an independent adjudicator interpret the manuscript. Admission requires high
relevance, primary pass, adjudicator pass, valid canonical provenance and no suppression.
Disagreement or an unsupported overclaim leaves a review candidate; it is not a technical
failure. There is no target pass rate and no obligation to classify every paper.

The assessor returns compact contribution, method, evaluation, alignment, limitations,
rationale and evidence-ID fields. The adjudicator receives the canonical context and
only the primary final structured assessment, independently checking support and
counterevidence. No hidden reasoning is shared or retained. Historical claim parsers,
numeric matching, role keywords and score caps do not control this admission path.

The default pinned pair is `gemini-3.8-flash` as primary assessor, served by Google
through `GEMINI_API_KEY`, and `deepseek/deepseek-v4-pro-0813` as independent adjudicator,
served by OpenRouter through `OPENROUTER_API_KEY`. Each role resolves its own provider,
endpoint and credential, so the two scientific judgments never share an account. A base
URL must match its provider's exact host, which keeps one provider's credential off
another's endpoint. Set `PAPER_SCOUT_QUALITY_LLM_MODEL` and
`PAPER_SCOUT_QUALITY_ADJUDICATOR_MODEL` to configure the pair from the explicit versioned
family allowlist; same-family pairs, rolling aliases and models with no known provider
fail closed. Adding a model requires reviewing its family, provider, capabilities and
price cap. Missing either credential leaves the paper unassessed with zero calls. No
credentials are committed, serialized into receipts or published.

Both providers receive the same contract — temperature 0, strict JSON schema, and no
hidden reasoning requested, returned or persisted — spelled with each provider's own
parameter names, since each rejects the other's. OpenRouter enforces server-side price
caps; Google's endpoint has no equivalent parameter, so Gemini spend is bounded by its
allocation instead and its reported usage carries tokens without a per-call charge.
Such a call records `billing_cost: UNKNOWN` with an explicit allocation basis rather
than a fabricated monetary amount.

Every new receipt records which provider, model and family served each role, and the
stored pair must match the pinned mapping. Because only one provider serves each pinned
model, binding the model in a receipt also binds its provider, and an accidental
cross-provider call is rejected rather than silently accepted. Retired pairs remain
listed, so `dual-promotion-v1` receipts written by the previous
`deepseek/deepseek-v4-pro-0813` and `anthropic/claude-sonnet-4.6` pair stay readable and
auditable under their original configuration. A retired receipt cannot borrow the newer
provenance, and the newer gate cannot omit it. The rubric, response schema, evidence
contract and promotion rule are unchanged by the model switch.

There are at most three calls per paper: one primary and at most two adjudications.
Only an adjudicator final-response syntax/schema violation permits one fresh adjudication
from the original canonical context and primary final assessment. The failed judgment
is never supplied to the retry, repaired, sliced or used to force the retry's conclusion.
An independently valid retry decides promotion normally; another invalid response fails
closed. Primary, transport, returned-model and provenance failures are not retried.
HTTP transport still allows exactly one attempt per call. Each request is
bounded to 300,000 serialized bytes and 4,096 output tokens. OpenRouter provider price
caps are enforced; unsupported schema/price parameters fail closed. The 180-second HTTP
socket timeout is not a total wall-clock deadline. Usage records retain unknown costs as
unknown. Before live work, freeze a manifest and reserve the bounded cost under an
approved batch ceiling, including any retry. The
[original cost manifest](experiments/manifests/quality-promotion-gate-2026-09-17.json)
retains its historical two-call protocol. Current maximum-size per-paper reserves are
$2.6304432 (one primary plus two adjudicators), using one input token per wire byte and
the capped output. This is a conservative reservation, not an expected invoice.

Both response schemas retain a maximum of 24 distinct evidence IDs. The constant was
introduced with the dual gate without a recorded numerical derivation. It is retained
as an engineering budget: six existing quality dimensions times an allowance of four
blocks (direct support, methodological detail, comparison/validation, counterevidence).
These are planning allowances, not per-dimension quotas or scientific sufficiency rules.
At 23 characters per ID, 24 IDs require about 625 compact JSON bytes; the two-role union
has at most 48 source blocks. Existing cards/sidecars store that union without per-field
references, so a larger evidence mapping/schema redesign is unnecessary. There is no
scientific, UI or database requirement for exactly 24, and no evidence-count target.
The adjudicator must select the smallest sufficient set for its decision, blockers and
major dimensions; the scientific rubric and traceability requirements are unchanged.

The same schema supplies generation and runtime validation (`maxItems: 24`,
`uniqueItems: true`, strict JSON output and required provider parameter support).
The adjudicator prompt also states the limit explicitly. Generation enforcement is
endpoint-dependent: [OpenRouter documents varying strictness](https://openrouter.ai/docs/guides/features/structured-outputs),
and [Claude's native schema subset](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations)
does not enforce array constraints beyond limited `minItems`. The observed endpoint
accepted the schema but exceeded the cap. Runtime validation remains authoritative;
no schema downgrade or response-healing plugin is used.

Completed dual-gate judgments use `canonical-response-v1` receipts for both roles.
The boundary is strict JSON parsing → unchanged schema/identity validation → sorted-key,
compact JSON serialized as UTF-8 → SHA-256. JSON layout and object-key ordering are
insignificant; array order, all fields and every string character remain exact. Duplicate
keys, non-JSON constants, invalid Unicode and unsupported fields fail closed. Decision
enums remain exact (`" pass "` is invalid); scientific prose and source excerpts are never
trimmed or Unicode-normalized by the receipt layer. Canonical manuscript excerpts bypass
the legacy optional-display-text trimmer, preserving source hashes and offsets.

Private runtime receipts retain each exact final-response content string and its raw
hash separately from the canonical hash. A further checksum binds that hash to the run,
role, model, context and request hash. New receipts additionally declare
`adjudicator-contract-retry-v1`: each attempt binds its exact raw response hash, sequence,
status, schema/syntax error category, usage, role/model/context and request to the run.
Completed retry receipts revalidate the rejected response as a contract failure, require
one primary success plus a final adjudicator success, and reject a third adjudication.
All attempts and their reported/unknown costs remain private. Historical two-call
receipts retain their original validation contract. Completed non-promotions receive the same checks,
and displayed rationale/limitations must match the recorded judgments. These checks
detect inconsistent data, not malicious replacement of every audit record and checksum;
they are not provider signatures. Hidden reasoning is not retained. Raw content and
receipts are excluded from public cards. Existing historical gate formats remain
unchanged; no successful dual-gate rows predate this receipt contract.

### Scientific manuscript coverage

New production calls require a deterministic `coverage-v2` preflight. Page boundaries,
numbered hierarchy and standalone heading shape define section ranges; heading semantics
only label their roles. Unfamiliar body headings remain visible, and a References label
cannot exclude later prose: only citation prefixes with an author-style start and an
inline bibliographic locator are excluded. Wrapped citations, ambiguous continuations,
and other back matter are retained conservatively. The STAR METHODS regression uses the actual 21-page structure with synthetic
prose; no scientific decisions are embedded in fixtures.

Selection includes all detected scientific body/appendix text when it fits. Under pressure,
round-robin selection balances roles and contiguous section prefixes in source order;
`max_section_characters` bounds selection chunks, not the total inclusion of a method.
References do not consume the body budget. Internal metadata records extracted/missing,
scientific, selected and omitted pages, per-section character accounting and omission
reasons, roles, budgets, versions and the exact input hash.

Any extraction gap, missing page, absent body structure or omitted body text returns
`text_coverage_failure` with public status `not_assessed` before either scientific model
is called. Partial excerpts remain diagnostic only; there is no approved partial-coverage
scientific decision. This conservative technical rule does not infer that a paper lacks
methods, alter the rubric, or relabel historical judgments. Previously stored receipts
retain their original contract and remain readable.

### Historical compatibility and bounded reassessment

Historical assessments, calibration, Batch 2 and both recoveries retain their original
schemas and outcomes. Existing passes are not automatically removed or reassessed.
New decisions append with a run identity; saving the same run is idempotent. A single
manual JSON import cannot earn a new dual-gate pass. The old import/semantic APIs remain
available only under explicitly historical assessment versions for compatibility.

Engram remains deterministic by default. Deterministic runs cannot promote. Explicit
live reassessment requires model configuration, budget and a bounded selection:

```bash
# Read saved assessments without acquisition or calls:
python3 -m paper_scout reassess-quality --track engram --report-only
# At most two deterministic diagnostics, no paid calls:
python3 -m paper_scout reassess-quality --track agent_memory --limit 2 --no-llm
```

Neither Batch 2 nor Batch 3 is run as part of this redesign. The
[Batch-3 protocol](experiments/manifests/batch-3-promotion-protocol-2026-09-17.md)
is prepared without a roster and requires a separate frozen execution task.

Full-text acquisition reuses the bounded downloader and extraction cache: explicit PDF, arXiv, Zenodo file metadata, Semantic Scholar and OpenAlex locations. Network timeout, download size, redirect, page, character and prompt bounds remain enforced. Page continuations and architecture/protocol sections are retained. `--full-text` explicitly enables acquisition for a track such as Engram; `--force` refreshes an existing decision and PDF cache. PDFs/cache/state stay outside Git and public output.

Reports include run assessments and `library-quality-YYYY-MM-DD.json`: relevance-high counts, each scientific status, main admissions, repository-only population/evaluations and reasons for non-admission. Every newly generated research-card sidecar is schema-validated. `jsonschema` is now a runtime dependency (previously test-only).

### Zenodo example

Record [22735829](https://zenodo.org/records/22735829), *Structured Episodic Memory (SEM)* by Berat Araç, was fetched from the public API and its 13-page manuscript inspected on 2026-09-16. The API labels it a preprint, with no creator affiliation; the PDF cover says Independent Researcher. It is classified `repository_only` because no external journal/conference publication is documented. The manuscript supports a scoped scientific pass through explicit methods, numerical paired ablations and limitations; results were not independently reproduced. Small seed counts, engineered Pong tasks and absent conventional RL baselines limit generalization. Topically it is an adjacent Agentic Memory review candidate, and outside Deep Research/Engram. The curation correction is about topical fit, independent of quality and affiliation. The factual fixture retains metadata, file checksum and manuscript evidence, excluding mutable counters.

## User-Friendly Daily Reading

Do not watch individual GitHub Actions run pages for daily reading. Actions are useful for debugging failed runs, but the reading surfaces are, in order:

- GitHub Pages dashboard.
- `digests/latest.md` as a stable Markdown fallback.
- `digests/YYYY-MM-DD.md` for dated Markdown archives.
- `reports/paper_scout/` for validation and digest-quality reports.
- GitHub Actions run pages only for debugging.

Live dashboard:

```text
https://vernerisirva.github.io/agentmempaper/
```

`python3 -m paper_scout build-site` generates:

```text
docs/index.html
docs/review.html
docs/latest.html
docs/archive.html
docs/about.html
docs/data/papers.json
docs/data/latest.json
docs/data/papers.csv
docs/data/papers.bib
docs/style.css
digests/latest.md
```

`python3 -m paper_scout build-site --track deep_research` generates the same static dashboard shape under:

```text
docs/deep-research/
digests/deep_research/latest.md
```

The dashboard is static, readable without JavaScript, and includes a cumulative paper library, latest-run discoveries, compact source warnings, archive links, structured research-card pages, JSON sidecars, and light browser-side search/filter/sort controls. `docs/about.html` and `docs/deep-research/about.html` explain sources, deduplication, relevance screening, and known limitations. The data exports support quick sharing through CSV, BibTeX, and JSON.

Manual dashboard curation is optional. The agent-memory track uses `config/curation.yaml`; the deep research track uses `config/curation/deep_research.yaml`. Curation can pin papers, hide false positives from the static dashboard without deleting SQLite state, add manual research notes, override dashboard relevance scores/tags, and show review statuses such as `unread`, `skimmed`, `read`, `important`, or `thesis_candidate`.

GitHub Pages setup is intentionally simple: in repository settings, open **Pages**, then set **Build and deployment → Source** to **GitHub Actions**. This is preferred over branch-based `main` / `/docs` deployment because daily `docs/` updates are committed by GitHub Actions, and those commits may not reliably trigger a separate branch-based Pages rebuild.

The Paper Scout workflow still commits `docs/` to `main` as a useful artifact, then deploys the same static `docs/` directory with the official Pages Actions: `actions/configure-pages`, `actions/upload-pages-artifact`, and `actions/deploy-pages`.

## GitHub Actions

The workflow in `.github/workflows/paper-scout.yml` runs daily and on manual dispatch.

It first validates:

```bash
python -m paper_scout evaluate-relevance --track agent_memory
python -m paper_scout evaluate-relevance --track deep_research
python -m paper_scout evaluate-quality --track agent_memory
python -m paper_scout evaluate-quality --track deep_research
python -m paper_scout validate-idempotency --track agent_memory
python -m paper_scout validate-idempotency --track deep_research
python -m paper_scout smoke-live --track agent_memory --days 14 --max-results-per-source 25 --no-notify --ci
python -m paper_scout smoke-live --track deep_research --days 14 --max-results-per-source 25 --no-notify --ci
```

Then it runs both daily tracks:

```bash
python -m paper_scout run --track agent_memory
python -m paper_scout build-site --track agent_memory
python -m paper_scout run --track deep_research
python -m paper_scout build-site --track deep_research
```

The live smoke step uses GitHub-hosted Python TLS defaults and a temporary SQLite state path. One failed source is reported but should not fail the workflow; the workflow should fail only if the Paper Scout code crashes unexpectedly. Markdown, JSON, and command logs are uploaded as artifacts, and the live smoke summary is included in the GitHub Actions step summary.

The daily run commits generated Markdown digests, `digests/latest.md`, `docs/` dashboard files, digest-quality reports, and non-smoke validation Markdown reports when they change. It also deploys `docs/` to GitHub Pages through Actions. It never commits SQLite state, caches, PDFs, credentials, or live-smoke JSON artifacts.

## TLS Troubleshooting

Paper Scout uses Python's default TLS verification. It does not globally disable certificate checks and does not use `verify=False`.

If local macOS/Python runs report TLS or certificate failures while GitHub-hosted CI succeeds, common fixes are:

- run the Python.org `Install Certificates.command` for that Python installation;
- upgrade or reinstall `certifi` if your local Python distribution uses it;
- check whether `SSL_CERT_FILE` or `REQUESTS_CA_BUNDLE` points to a stale certificate bundle;
- verify that a corporate proxy or VPN is not intercepting TLS without a trusted local root certificate.

`smoke-live` reports TLS/certificate failures separately from HTTP/API errors, timeouts, parser failures, and true zero-result responses.

## Tests

Run Paper Scout tests:

```bash
python3 -m unittest tests/test_paper_scout_*.py
```

Run all repository tests:

```bash
python3 -m unittest discover -s tests -p '*.py'
```
