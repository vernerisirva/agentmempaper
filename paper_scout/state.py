from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from paper_scout.deduplication import canonical_key
from paper_scout.dates import publication_date
from paper_scout.models import ClassificationResult, DigestPaper, PaperCandidate
from paper_scout.quality_models import QualityAssessment


@dataclass(frozen=True)
class FailedQuery:
    track: str
    source: str
    normalized_query: str
    requested_days: int
    failure_type: str
    attempt_count: int
    first_failure_at: str
    latest_failure_at: str
    next_retry_at: str


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
                            CASE excluded.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.source ELSE papers.source END,
                    source_id = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.source_id ELSE papers.source_id END,
                    doi = COALESCE(papers.doi, excluded.doi),
                    arxiv_id = COALESCE(papers.arxiv_id, excluded.arxiv_id),
                    semantic_scholar_id = COALESCE(papers.semantic_scholar_id, excluded.semantic_scholar_id),
                    openalex_id = COALESCE(papers.openalex_id, excluded.openalex_id),
                    url = COALESCE(excluded.url, papers.url),
                    published_date = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.published_date ELSE COALESCE(papers.published_date, excluded.published_date) END,
                    publication_year = COALESCE(papers.publication_year, excluded.publication_year),
                    publication_date_precision = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.publication_date_precision ELSE COALESCE(papers.publication_date_precision, excluded.publication_date_precision) END,
                    publication_date_source = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) THEN excluded.publication_date_source ELSE COALESCE(papers.publication_date_source, excluded.publication_date_source) END,
                    publication_date_confidence = CASE
                        WHEN (
                            CASE excluded.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
                        ) > (
                            CASE papers.publication_date_precision WHEN 'exact' THEN 3 WHEN 'day' THEN 3 WHEN 'month' THEN 2 WHEN 'year' THEN 1 ELSE 0 END
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

    def get_unnotified_digest_papers(self, exclude_quality_suppressed: bool = False) -> list[DigestPaper]:
        suppression_clause = "AND qs.canonical_key IS NULL" if exclude_quality_suppressed else ""
        with self._connect() as db:
            rows = db.execute(
                f"""
                SELECT p.*, qa.payload_json AS quality_payload_json,
                       CASE WHEN qs.canonical_key IS NULL THEN 0 ELSE 1 END AS quality_suppressed
                FROM papers p
                LEFT JOIN notifications n ON n.canonical_key = p.canonical_key
                LEFT JOIN paper_quality_assessments qa ON qa.id = (
                    SELECT current_qa.id FROM paper_quality_assessments current_qa
                    WHERE current_qa.canonical_id = p.canonical_key
                    ORDER BY current_qa.assessed_at DESC, current_qa.id DESC LIMIT 1
                )
                LEFT JOIN quality_suppressions qs ON qs.canonical_key = p.canonical_key AND qs.active = 1
                WHERE n.canonical_key IS NULL
                  AND p.relevance_decision IN ('relevant', 'maybe')
                  {suppression_clause}
                ORDER BY p.relevance_decision = 'maybe', p.relevance_score DESC, p.published_date DESC
                """
            ).fetchall()
        return [_row_to_digest_paper(row) for row in rows]

    def get_notified_for_date(self, digest_date: str) -> list[DigestPaper]:
        with self._connect() as db:
            rows = db.execute(
                """
                SELECT p.*, qa.payload_json AS quality_payload_json,
                       CASE WHEN qs.canonical_key IS NULL THEN 0 ELSE 1 END AS quality_suppressed
                FROM papers p
                JOIN notifications n ON n.canonical_key = p.canonical_key
                LEFT JOIN paper_quality_assessments qa ON qa.id = (
                    SELECT current_qa.id FROM paper_quality_assessments current_qa
                    WHERE current_qa.canonical_id = p.canonical_key
                    ORDER BY current_qa.assessed_at DESC, current_qa.id DESC LIMIT 1
                )
                LEFT JOIN quality_suppressions qs ON qs.canonical_key = p.canonical_key AND qs.active = 1
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

    def paper_exists(self, candidate: PaperCandidate) -> bool:
        key = canonical_key(candidate)
        with self._connect() as db:
            return db.execute("SELECT 1 FROM papers WHERE canonical_key = ?", (key,)).fetchone() is not None

    def paper_count(self) -> int:
        with self._connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM papers").fetchone()[0])

    def save_quality_assessment(self, assessment: QualityAssessment) -> int:
        payload = json.dumps(assessment.to_dict(), sort_keys=True)
        with self._connect() as db:
            db.execute(
                """
                INSERT OR IGNORE INTO paper_quality_assessments(
                    canonical_id, assessment_version, rubric_version, assessor_type,
                    assessor_model, source_content_hash, assessed_at, overall_quality_score,
                    recommendation, confidence, assessment_scope, paper_type, payload_json
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    assessment.canonical_id,
                    assessment.assessment_version,
                    assessment.rubric_version,
                    assessment.assessor_type,
                    assessment.assessor_model or "",
                    assessment.source_content_hash,
                    assessment.assessed_at,
                    assessment.overall_quality_score,
                    assessment.recommendation,
                    assessment.confidence,
                    assessment.assessment_scope,
                    assessment.paper_type,
                    payload,
                ),
            )
            row = db.execute(
                """
                SELECT id FROM paper_quality_assessments
                WHERE canonical_id = ? AND assessment_version = ? AND rubric_version = ?
                  AND assessor_type = ? AND assessor_model = ? AND source_content_hash = ?
                """,
                (
                    assessment.canonical_id,
                    assessment.assessment_version,
                    assessment.rubric_version,
                    assessment.assessor_type,
                    assessment.assessor_model or "",
                    assessment.source_content_hash,
                ),
            ).fetchone()
            return int(row["id"])

    def get_current_quality_assessment(
        self,
        canonical_id: str,
        assessment_version: str | None = None,
        rubric_version: str | None = None,
        source_content_hash: str | None = None,
    ) -> QualityAssessment | None:
        clauses = ["canonical_id = ?"]
        params: list[object] = [canonical_id]
        for column, value in (
            ("assessment_version", assessment_version),
            ("rubric_version", rubric_version),
            ("source_content_hash", source_content_hash),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                params.append(value)
        with self._connect() as db:
            row = db.execute(
                f"SELECT payload_json FROM paper_quality_assessments WHERE {' AND '.join(clauses)} ORDER BY assessed_at DESC, id DESC LIMIT 1",
                params,
            ).fetchone()
        return QualityAssessment.from_dict(json.loads(row["payload_json"])) if row else None

    def list_current_quality_assessments(self) -> list[QualityAssessment]:
        with self._connect() as db:
            rows = db.execute(
                """
                SELECT qa.payload_json FROM paper_quality_assessments qa
                WHERE qa.id = (
                    SELECT current_qa.id FROM paper_quality_assessments current_qa
                    WHERE current_qa.canonical_id = qa.canonical_id
                    ORDER BY current_qa.assessed_at DESC, current_qa.id DESC LIMIT 1
                )
                ORDER BY qa.canonical_id
                """
            ).fetchall()
        return [QualityAssessment.from_dict(json.loads(row["payload_json"])) for row in rows]

    def quality_candidates(self, days: int | None = None, paper_id: str | None = None) -> list[tuple[str, PaperCandidate, str]]:
        clauses = ["relevance_decision IN ('relevant', 'maybe')"]
        params: list[object] = []
        if days is not None:
            clauses.append("first_seen_at >= datetime('now', ?)")
            params.append(f"-{max(0, days)} days")
        if paper_id:
            clauses.append("canonical_key = ?")
            params.append(paper_id)
        with self._connect() as db:
            rows = db.execute(
                f"SELECT * FROM papers WHERE {' AND '.join(clauses)} ORDER BY first_seen_at DESC",
                params,
            ).fetchall()
        return [(str(row["canonical_key"]), _row_to_candidate(row), str(row["relevance_decision"])) for row in rows]

    def set_quality_suppression(self, canonical_id: str, assessment_id: int, reason: str, active: bool = True) -> None:
        with self._connect() as db:
            db.execute(
                """
                INSERT INTO quality_suppressions(canonical_key, assessment_id, reason, active, first_suppressed_at, updated_at)
                VALUES(?, ?, ?, ?, datetime('now'), datetime('now'))
                ON CONFLICT(canonical_key) DO UPDATE SET
                    assessment_id = excluded.assessment_id,
                    reason = excluded.reason,
                    active = excluded.active,
                    updated_at = datetime('now')
                """,
                (canonical_id, assessment_id, reason, int(active)),
            )

    def clear_quality_suppression(self, canonical_id: str) -> None:
        with self._connect() as db:
            db.execute("UPDATE quality_suppressions SET active = 0, updated_at = datetime('now') WHERE canonical_key = ?", (canonical_id,))

    def record_failed_query(
        self,
        track: str,
        source: str,
        normalized_query: str,
        requested_days: int,
        failure_type: str,
    ) -> None:
        now = datetime.now(UTC).replace(microsecond=0)
        with self._connect() as db:
            row = db.execute(
                "SELECT attempt_count FROM failed_queries WHERE track = ? AND source = ? AND normalized_query = ? AND requested_days = ?",
                (track, source, normalized_query, requested_days),
            ).fetchone()
            attempts = int(row["attempt_count"]) + 1 if row else 1
            delay_hours = min(24 * 7, 2 ** min(attempts - 1, 7))
            next_retry = now + timedelta(hours=delay_hours)
            db.execute(
                """
                INSERT INTO failed_queries(
                    track, source, normalized_query, requested_days, first_failure_at,
                    latest_failure_at, failure_type, attempt_count, next_retry_at, resolved_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
                ON CONFLICT(track, source, normalized_query, requested_days) DO UPDATE SET
                    latest_failure_at = excluded.latest_failure_at,
                    failure_type = excluded.failure_type,
                    attempt_count = excluded.attempt_count,
                    next_retry_at = excluded.next_retry_at,
                    resolved_at = NULL
                """,
                (
                    track,
                    source,
                    normalized_query,
                    requested_days,
                    now.isoformat(),
                    now.isoformat(),
                    failure_type,
                    attempts,
                    next_retry.isoformat(),
                ),
            )

    def resolve_failed_query(self, track: str, source: str, normalized_query: str, requested_days: int) -> None:
        with self._connect() as db:
            db.execute(
                """
                UPDATE failed_queries SET resolved_at = datetime('now')
                WHERE track = ? AND source = ? AND normalized_query = ? AND requested_days = ? AND resolved_at IS NULL
                """,
                (track, source, normalized_query, requested_days),
            )

    def retryable_failed_queries(self, track: str, limit: int = 10, include_not_due: bool = False) -> list[FailedQuery]:
        due_clause = "" if include_not_due else "AND next_retry_at <= ?"
        params: list[object] = [track]
        if not include_not_due:
            params.append(datetime.now(UTC).replace(microsecond=0).isoformat())
        params.append(limit)
        with self._connect() as db:
            rows = db.execute(
                f"""
                SELECT * FROM failed_queries
                WHERE track = ? AND resolved_at IS NULL {due_clause}
                ORDER BY next_retry_at, latest_failure_at LIMIT ?
                """,
                params,
            ).fetchall()
        return [
            FailedQuery(
                track=row["track"], source=row["source"], normalized_query=row["normalized_query"],
                requested_days=row["requested_days"], failure_type=row["failure_type"],
                attempt_count=row["attempt_count"], first_failure_at=row["first_failure_at"],
                latest_failure_at=row["latest_failure_at"], next_retry_at=row["next_retry_at"],
            )
            for row in rows
        ]

    def failed_queries(self, track: str, include_resolved: bool = False) -> list[sqlite3.Row]:
        resolved_clause = "" if include_resolved else "AND resolved_at IS NULL"
        with self._connect() as db:
            return db.execute(
                f"SELECT * FROM failed_queries WHERE track = ? {resolved_clause} ORDER BY latest_failure_at DESC",
                (track,),
            ).fetchall()

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

                CREATE TABLE IF NOT EXISTS failed_queries(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    track TEXT NOT NULL,
                    source TEXT NOT NULL,
                    normalized_query TEXT NOT NULL,
                    requested_days INTEGER NOT NULL,
                    first_failure_at TEXT NOT NULL,
                    latest_failure_at TEXT NOT NULL,
                    failure_type TEXT NOT NULL,
                    attempt_count INTEGER NOT NULL,
                    next_retry_at TEXT NOT NULL,
                    resolved_at TEXT,
                    UNIQUE(track, source, normalized_query, requested_days)
                );

                CREATE TABLE IF NOT EXISTS paper_quality_assessments(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    canonical_id TEXT NOT NULL,
                    assessment_version TEXT NOT NULL,
                    rubric_version TEXT NOT NULL,
                    assessor_type TEXT NOT NULL,
                    assessor_model TEXT NOT NULL DEFAULT '',
                    source_content_hash TEXT NOT NULL,
                    assessed_at TEXT NOT NULL,
                    overall_quality_score INTEGER,
                    recommendation TEXT NOT NULL,
                    confidence TEXT NOT NULL,
                    assessment_scope TEXT NOT NULL,
                    paper_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    UNIQUE(canonical_id, assessment_version, rubric_version, assessor_type, assessor_model, source_content_hash)
                );

                CREATE INDEX IF NOT EXISTS idx_quality_assessments_current
                ON paper_quality_assessments(canonical_id, assessed_at DESC, id DESC);

                CREATE TABLE IF NOT EXISTS quality_suppressions(
                    canonical_key TEXT PRIMARY KEY,
                    assessment_id INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    active INTEGER NOT NULL DEFAULT 1,
                    first_suppressed_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )
            _ensure_column(db, "papers", "publication_year", "TEXT")
            _ensure_column(db, "papers", "publication_date_precision", "TEXT")
            _ensure_column(db, "papers", "publication_date_source", "TEXT")
            _ensure_column(db, "papers", "publication_date_confidence", "TEXT")


def _row_to_digest_paper(row: sqlite3.Row) -> DigestPaper:
    quality = _quality_from_row(row)
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
        quality_score=quality.overall_quality_score if quality else None,
        quality_recommendation=quality.recommendation if quality else None,
        quality_confidence=quality.confidence if quality else None,
        quality_scope=quality.assessment_scope if quality else None,
        quality_summary=quality.concise_summary if quality else None,
        quality_strengths=quality.positive_signals if quality else [],
        quality_concerns=quality.concerns if quality else [],
        quality_assessment_version=quality.assessment_version if quality else None,
        quality_assessed_at=quality.assessed_at if quality else None,
        quality_suppressed=bool(row["quality_suppressed"]) if "quality_suppressed" in row.keys() else False,
    )


def _quality_from_row(row: sqlite3.Row) -> QualityAssessment | None:
    if "quality_payload_json" not in row.keys() or not row["quality_payload_json"]:
        return None
    return QualityAssessment.from_dict(json.loads(row["quality_payload_json"]))


def _row_to_candidate(row: sqlite3.Row) -> PaperCandidate:
    return PaperCandidate(
        title=str(row["title"]),
        authors=json.loads(row["authors_json"]),
        abstract=str(row["abstract"] or ""),
        source=str(row["source"]),
        source_id=str(row["source_id"]),
        doi=row["doi"],
        arxiv_id=row["arxiv_id"],
        semantic_scholar_id=row["semantic_scholar_id"],
        openalex_id=row["openalex_id"],
        url=row["url"],
        published_date=row["published_date"],
        publication_year=row["publication_year"],
        publication_date_precision=row["publication_date_precision"],
        publication_date_source=row["publication_date_source"],
        publication_date_confidence=row["publication_date_confidence"],
        updated_date=row["updated_date"],
        raw=json.loads(row["raw_json"] or "{}"),
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
