# Paper Scout

Paper Scout is a local-first daily research-monitoring agent for papers related to agentic memory, LLM agent memory, memory mechanisms for long-running or deep-research agents, and Engram-style or parametric-memory mechanisms when they connect to language-model behavior.

It fetches candidates from arXiv, Semantic Scholar, and OpenAlex; deduplicates canonical papers; classifies relevance with deterministic rules by default; stores state in SQLite; and writes Markdown digests under `digests/`.

## Scope

The default config in `config/paper_scout.yaml` tracks:

- agentic memory, persistent memory, episodic/semantic/procedural memory, memory policies, and agent-memory benchmarks;
- deep research agents, autonomous research agents, and literature-review agents;
- Engram, Megatron-LM Engram, parametric memory, model-internal memory, and memory mechanisms.

The Engram/Megatron-LM context is treated as research context, not as proof that Engram-style approaches cannot work.

## Commands

Run the normal daily scout:

```bash
python3 -m paper_scout run
```

Search without writing state:

```bash
python3 -m paper_scout search --days 7
```

Render a digest from stored papers:

```bash
python3 -m paper_scout digest --date 2026-06-26
```

Evaluate deterministic relevance fixtures:

```bash
python3 -m paper_scout evaluate-relevance
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

## State Strategy

- Default persistent state: `data/paper_scout.sqlite3`.
- Deep research persistent state: `data/deep_research/paper_scout.sqlite3`.
- Override state with `PAPER_SCOUT_STATE_PATH`.
- Track-specific state can also be overridden with `PAPER_SCOUT_AGENT_MEMORY_STATE_PATH` or `PAPER_SCOUT_DEEP_RESEARCH_STATE_PATH`.
- `data/.gitkeep` keeps the state directory present.
- SQLite sidecar files are ignored: `*.sqlite3-journal`, `*.sqlite3-wal`, and `*.sqlite3-shm`.
- `data/paper_scout.sqlite3` is explicitly not ignored because the daily GitHub Actions workflow may intentionally commit persistent state.
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

The daily run may commit the persistent SQLite state, Markdown digests, `digests/latest.md`, `docs/` dashboard files, digest-quality reports, and non-smoke validation Markdown reports when they change. It also deploys `docs/` to GitHub Pages through Actions. It does not commit live-smoke JSON artifacts.

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
