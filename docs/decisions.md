# Paper Scout decisions

## 2026-09-05 — Separate Engram track

Add `engram` as a separately screened library in the existing multi-track system.
Use declarative foundational IDs, title/abstract evidence, independent SQLite
state and curation, and the shared renderer/schema. Keep adjacent neural-memory
mechanisms distinguishable and include negative/efficiency studies on their
scientific topic merits. Public context uses primary papers and implementation
reference links only.

Use four discovery slots per provider with the existing single-page fetchers,
report incomplete windows, and cap incremental metadata enrichment at four
lookups per run. The historical search is an explicit bounded operation from
2026-01-12, not a daily sweep. Engram's default relevance and quality paths make
zero model calls and its site renderer uses saved metadata.

Accept the exact legacy two-database snapshot format, initialize only the new
track, and require checksummed three-track snapshots for subsequent writes.
Preserve fail-safe restoration and exclude runtime state from Git and Pages.

Validation lesson: live primary metadata caught an evidence rule that missed
cross-model transfer described across multiple sentences. Regression checks also
caught dropped revision dates, timezone-insensitive New badges, and nested-track
digest links. Fixes preserve both existing libraries' membership and screening.
