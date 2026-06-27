from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from paper_scout.deduplication import canonical_key
from paper_scout.dates import publication_date
from paper_scout.models import ClassificationResult, DigestPaper, PaperCandidate


class PaperStore:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def start_run(self, days: int) -> int:
        with self._connect() as db:
            cursor = db.execute(
                "INSERT INTO runs(started_at, status, days, fetched_count, new_count, notified_count) VALUES(datetime('now'), 'running', ?, 0, 0, 0)",
                (days,),
            )
            return int(cursor.lastrowid)

    def finish_run(self, run_id: int, fetched_count: int, new_count: int, notified_count: int, status: str = "ok") -> None:
        with self._connect() as db:
            db.execute(
                """
                UPDATE runs
                SET finished_at = datetime('now'), status = ?, fetched_count = ?, new_count = ?, notified_count = ?
                WHERE id = ?
                """,
                (status, fetched_count, new_count, notified_count, run_id),
            )

    def upsert_paper(self, candidate: PaperCandidate, classification: ClassificationResult) -> str:
        candidate = _with_publication_metadata(candidate)
        key = canonical_key(candidate)
        with self._connect() as db:
            db.execute(
                """
                INSERT INTO papers(
                    canonical_key, title, authors_json, abstract, source, source_id, doi, arxiv_id,
                    semantic_scholar_id, openalex_id, url, published_date, publication_year,
                    publication_date_precision, publication_date_source, publication_date_confidence, updated_date, raw_json,
                    relevance_score, relevance_decision, relevance_reason, tags_json, abstract_summary,
                    first_seen_at, last_seen_at
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                ON CONFLICT(canonical_key) DO UPDATE SET
                    title = excluded.title,
                    authors_json = excluded.authors_json,
                    abstract = CASE WHEN excluded.abstract != '' THEN excluded.abstract ELSE papers.abstract END,
                    source = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.source ELSE papers.source END,
                    source_id = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.source_id ELSE papers.source_id END,
                    doi = COALESCE(papers.doi, excluded.doi),
                    arxiv_id = COALESCE(papers.arxiv_id, excluded.arxiv_id),
                    semantic_scholar_id = COALESCE(papers.semantic_scholar_id, excluded.semantic_scholar_id),
                    openalex_id = COALESCE(papers.openalex_id, excluded.openalex_id),
                    url = COALESCE(excluded.url, papers.url),
                    published_date = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.published_date ELSE COALESCE(papers.published_date, excluded.published_date) END,
                    publication_year = COALESCE(papers.publication_year, excluded.publication_year),
                    publication_date_precision = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.publication_date_precision ELSE COALESCE(papers.publication_date_precision, excluded.publication_date_precision) END,
                    publication_date_source = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.publication_date_source ELSE COALESCE(papers.publication_date_source, excluded.publication_date_source) END,
                    publication_date_confidence = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.publication_date_confidence ELSE COALESCE(papers.publication_date_confidence, excluded.publication_date_confidence) END,
                    updated_date = COALESCE(excluded.updated_date, papers.updated_date),
                    raw_json = excluded.raw_json,
                    relevance_score = excluded.relevance_score,
                    relevance_decision = excluded.relevance_decision,
                    relevance_reason = excluded.relevance_reason,
                    tags_json = excluded.tags_json,
                    abstract_summary = excluded.abstract_summary,
                    last_seen_at = datetime('now')
                """,
                (
                    key,
                    candidate.title,
                    json.dumps(candidate.authors),
                    candidate.abstract,
                    candidate.source,
                    candidate.source_id,
                    candidate.doi,
                    candidate.arxiv_id,
                    candidate.semantic_scholar_id,
                    candidate.openalex_id,
                    candidate.url,
                    candidate.published_date,
                    candidate.publication_year,
                    candidate.publication_date_precision,
                    candidate.publication_date_source,
                    candidate.publication_date_confidence,
                    candidate.updated_date,
                    json.dumps(candidate.raw),
                    classification.score,
                    classification.decision,
                    classification.reason,
                    json.dumps(classification.tags),
                    classification.abstract_summary,
                ),
            )
        return key

    def record_sighting(self, run_id: int, canonical_key: str, candidate: PaperCandidate, search_term: str) -> None:
        with self._connect() as db:
            db.execute(
                """
                INSERT INTO sightings(run_id, canonical_key, source, source_id, search_term, seen_at)
                VALUES(?, ?, ?, ?, ?, datetime('now'))
                """,
                (run_id, canonical_key, candidate.source, candidate.source_id, search_term),
            )

    def get_unnotified_digest_papers(self) -> list[DigestPaper]:
        with self._connect() as db:
            rows = db.execute(
                """
                SELECT p.*
                FROM papers p
                LEFT JOIN notifications n ON n.canonical_key = p.canonical_key
                WHERE n.canonical_key IS NULL
                  AND p.relevance_decision IN ('relevant', 'maybe')
                ORDER BY p.relevance_decision = 'maybe', p.relevance_score DESC, p.published_date DESC
                """
            ).fetchall()
        return [_row_to_digest_paper(row) for row in rows]

    def get_notified_for_date(self, digest_date: str) -> list[DigestPaper]:
        with self._connect() as db:
            rows = db.execute(
                """
                SELECT p.*
                FROM papers p
                JOIN notifications n ON n.canonical_key = p.canonical_key
                WHERE n.digest_date = ?
                ORDER BY p.relevance_decision = 'maybe', p.relevance_score DESC, p.published_date DESC
                """,
                (digest_date,),
            ).fetchall()
        return [_row_to_digest_paper(row) for row in rows]

    def mark_notified(self, canonical_keys: list[str], digest_date: str) -> None:
        with self._connect() as db:
            for key in canonical_keys:
                db.execute(
                    """
                    INSERT OR IGNORE INTO notifications(canonical_key, digest_date, notified_at)
                    VALUES(?, ?, datetime('now'))
                    """,
                    (key, digest_date),
                )

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def _init_schema(self) -> None:
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS papers(
                    canonical_key TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    authors_json TEXT NOT NULL,
                    abstract TEXT NOT NULL,
                    source TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    doi TEXT,
                    arxiv_id TEXT,
                    semantic_scholar_id TEXT,
                    openalex_id TEXT,
                    url TEXT,
                    published_date TEXT,
                    publication_year TEXT,
                    publication_date_precision TEXT,
                    publication_date_source TEXT,
                    publication_date_confidence TEXT,
                    updated_date TEXT,
                    raw_json TEXT NOT NULL,
                    relevance_score INTEGER NOT NULL,
                    relevance_decision TEXT NOT NULL,
                    relevance_reason TEXT NOT NULL,
                    tags_json TEXT NOT NULL,
                    abstract_summary TEXT,
                    first_seen_at TEXT NOT NULL,
                    last_seen_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS sightings(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    canonical_key TEXT NOT NULL,
                    source TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    search_term TEXT NOT NULL,
                    seen_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS runs(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    status TEXT NOT NULL,
                    days INTEGER NOT NULL,
                    fetched_count INTEGER NOT NULL,
                    new_count INTEGER NOT NULL,
                    notified_count INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS notifications(
                    canonical_key TEXT PRIMARY KEY,
                    digest_date TEXT NOT NULL,
                    notified_at TEXT NOT NULL
                );
                """
            )
            _ensure_column(db, "papers", "publication_year", "TEXT")
            _ensure_column(db, "papers", "publication_date_precision", "TEXT")
            _ensure_column(db, "papers", "publication_date_source", "TEXT")
            _ensure_column(db, "papers", "publication_date_confidence", "TEXT")


def _row_to_digest_paper(row: sqlite3.Row) -> DigestPaper:
    return DigestPaper(
        canonical_key=row["canonical_key"],
        title=row["title"],
        authors=json.loads(row["authors_json"]),
        abstract=row["abstract"],
        source=row["source"],
        url=row["url"],
        published_date=row["published_date"],
        score=row["relevance_score"],
        decision=row["relevance_decision"],
        reason=row["relevance_reason"],
        tags=json.loads(row["tags_json"]),
        abstract_summary=row["abstract_summary"],
        publication_year=row["publication_year"],
        publication_date_precision=row["publication_date_precision"],
        publication_date_source=row["publication_date_source"],
        publication_date_confidence=row["publication_date_confidence"] if "publication_date_confidence" in row.keys() else None,
    )


def _with_publication_metadata(candidate: PaperCandidate) -> PaperCandidate:
    published = publication_date(
        candidate.published_date,
        candidate.publication_date_source or candidate.source,
        candidate.publication_year,
    )
    return PaperCandidate(
        **{
            **candidate.__dict__,
            "published_date": published.value,
            "publication_year": published.year,
            "publication_date_precision": candidate.publication_date_precision or published.precision,
            "publication_date_source": candidate.publication_date_source or published.source,
            "publication_date_confidence": candidate.publication_date_confidence or _publication_confidence(candidate.publication_date_precision or published.precision, candidate.publication_date_source or published.source),
        }
    )


def _publication_confidence(precision: str | None, source: str | None) -> str | None:
    if not precision or precision == "unknown":
        return None
    if precision == "year":
        return "low"
    if source in {"arxiv", "ssrn"}:
        return "high"
    if source and source.startswith(("crossref-created", "crossref-deposited")):
        return "low"
    if source and source.startswith("crossref"):
        return "medium"
    return "medium"


def _ensure_column(db: sqlite3.Connection, table: str, column: str, definition: str) -> None:
    columns = {row["name"] for row in db.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in columns:
        db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
