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
python3 -m paper_scout reassess-quality --track agent_memory --assessment-version quality-v2 --rubric-version scholarly-rubric-v2
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

Topic relevance and scholarly quality are separate. Relevance decides whether a paper belongs in an Agentic Memory or Deep Research library. The optional quality layer asks how strongly the available material supports the paper's contribution. A paper can therefore be highly relevant but weakly validated, or only moderately relevant but methodologically strong.

The feature is configured per track under the `quality:` section of `config/tracks/agent_memory.yaml` and `config/tracks/deep_research.yaml`. Supported modes are:

- `off`: no quality assessment;
- `deterministic`: paper-type-aware evidence rules only;
- `llm`: use the configured OpenAI-compatible model, with deterministic fallback;
- `hybrid`: deterministic assessment plus model validation;
- `auto`: hybrid when credentials are available, deterministic otherwise.

Each versioned assessment stores an optional 0-100 score, confidence, recommendation, paper type, assessment scope, per-dimension scores, positive and negative signals, evidence references, missing information, assessor/model provenance, content hash, timestamp, rubric version, and any applied score cap. Null scores mean **not enough evidence**, not zero quality. Abstract-only assessments are low confidence and are never hidden automatically.

The deterministic rubric first classifies the paper as empirical, systems/application, methods, theoretical, survey/review, position/conceptual, dataset/benchmark, case study, replication, or unclear. It then applies type-appropriate expectations. Surveys are not penalized for lacking experiments, and theoretical papers can be validated through formal reasoning. Systems papers that only combine a familiar PDF/RAG/vector/graph/UI stack without comparative evidence receive explicit integration-only and functionality-only concerns and a score cap.

Full-text enrichment is optional and bounded. Paper Scout tries, in order, an explicitly supplied open-access PDF URL, arXiv PDF, Semantic Scholar `openAccessPdf`, and OpenAlex open-access locations. Downloads require public HTTP(S), use normal TLS verification, validate PDF content, follow at most five safe redirects, and enforce configured timeout, size, page, extraction-character, section, and prompt limits. Extracted text is cached under `data/cache/`; PDFs and cache files are ignored by Git and never committed. Scanned or malformed PDFs degrade to partial/abstract evidence without failing the daily scout.

Cached content is reused for routine runs. `reassess-quality --force` bypasses the extracted-text cache and is the explicit way to check for a changed PDF at the same URL; a new assessment version, rubric version, model, or content hash creates a new immutable assessment record.

Quality-aware ranking supports `ignore`, `annotate`, `downrank`, and `hide`. Unknown quality is neutral. The configured default uses relevance as the larger signal and quality as a confidence/scope-weighted secondary signal. Human curation in `config/curation.yaml` or `config/curation/deep_research.yaml` can set `quality_score_override`, `quality_recommendation_override`, `quality_note`, `include_despite_quality`, or `suppress_for_quality`; pinned and explicit-include decisions override automated suppression.

Daily quality diagnostics are written to:

```text
reports/paper_scout/paper-quality-YYYY-MM-DD.md
reports/paper_scout/quality-eval-YYYY-MM-DD.md
reports/paper_scout/deep_research/paper-quality-YYYY-MM-DD.md
reports/paper_scout/deep_research/quality-eval-YYYY-MM-DD.md
```

The static dashboard, paper detail JSON, library JSON, and CSV expose quality provenance and evidence. Advanced quality filters remain collapsed by default. Automated quality assessment is advisory triage, not peer review, and does not use venue prestige, author identity, institution, citation count, or paper age as quality signals.

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
