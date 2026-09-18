#!/usr/bin/env python3
"""Read-only integrity check over every stored scientific assessment.

Loads each row of every assessment history, revalidates completed promotion receipts
under the gate version that produced them, and reports the version combinations held.
Nothing is written, migrated or repaired: a row that cannot be read is reported, not
rewritten, because stored assessments are historical records.

The databases are private and are not committed, so this is an operator check rather
than a CI gate: a database that is absent is skipped and reported as such. Run it after
any change to assessment versioning, receipt validation or the promotion schema.

    python3 .github/scripts/check_stored_assessments.py [database ...]

Exits non-zero if any stored row fails to load or revalidate.
"""
from collections import Counter
import json
from pathlib import Path
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from paper_scout.promotion_protocol import (  # noqa: E402
    DUAL_PROMOTION_GATE_VERSIONS, INDEPENDENCE_FIELD, INDEPENDENCE_GATE_VERSIONS,
    PROMOTION_ASSESSMENT_VERSIONS, validate_receipt,
)
from paper_scout.quality_models import QualityAssessment  # noqa: E402

DEFAULT_DATABASES = ('data/paper_scout.sqlite3', 'data/deep_research/paper_scout.sqlite3',
                     'data/engram/paper_scout.sqlite3')


def payloads(path: Path):
    """Yield one stored payload at a time, or a failure string for an unreadable row.

    A database that is present but is not an assessment history, and a row whose
    payload is not JSON, are both reported like any other unreadable row. Nothing here
    raises: the caller must be able to finish the remaining databases.
    """
    try:
        connection = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    except sqlite3.Error as exc:
        yield f'{path}: unreadable database ({type(exc).__name__}: {exc})'
        return
    try:
        cursor = connection.execute(
            'SELECT id, payload_json FROM paper_quality_assessments ORDER BY id')
        while True:
            try:
                row = cursor.fetchone()
            except sqlite3.Error as exc:
                yield f'{path}: unreadable row ({type(exc).__name__}: {exc})'
                return
            if row is None:
                return
            try:
                yield json.loads(row[1])
            except (TypeError, ValueError) as exc:
                yield f'{path}: row {row[0]}: unreadable payload ({type(exc).__name__}: {exc})'
    except sqlite3.Error as exc:
        yield f'{path}: unreadable database ({type(exc).__name__}: {exc})'
    finally:
        connection.close()


def diagnosis(value: dict) -> str | None:
    """Name the invariant a row breaks, for a message the model layer does not phrase.

    This explains a rejection; it never decides one. The model layer is the only
    authority on whether a stored row is valid, so every row is loaded through it
    regardless of what this says, and these predicates mirror its named constants.
    """
    gate = value.get('quality_gate_version')
    if (value.get('assessment_version') in PROMOTION_ASSESSMENT_VERSIONS
            and value.get('quality_status') == 'pass'
            and gate not in DUAL_PROMOTION_GATE_VERSIONS):
        return f'{value.get("assessment_version")} pass on legacy gate {gate}'
    if (any(INDEPENDENCE_FIELD in (value.get('execution') or {}).get(role, {})
            for role in ('primary', 'adjudicator'))
            and gate not in INDEPENDENCE_GATE_VERSIONS):
        return f'gate {gate} carries evaluation independence'
    return None


def check(path: Path, versions: Counter, failures: list) -> int:
    seen = 0
    for value in payloads(path):
        if isinstance(value, str):
            failures.append(value)
            continue
        seen += 1
        canonical_id = value.get('canonical_id')
        versions[(value.get('assessment_version'), value.get('quality_gate_version'),
                  value.get('rubric_version'), value.get('quality_status'))] += 1
        try:
            assessment = QualityAssessment.from_dict(value)
            if (assessment.quality_gate_version in DUAL_PROMOTION_GATE_VERSIONS
                    and assessment.execution.get('outcome') == 'success'):
                validate_receipt(assessment)
        except Exception as exc:  # noqa: BLE001 - report every bad row, never raise.
            named = diagnosis(value)
            detail = f'{type(exc).__name__}: {exc}' if named is None else named
            failures.append(f'{path}: {canonical_id}: {detail}')
    return seen


def main(argv: list[str]) -> int:
    paths = [Path(p) for p in (argv or DEFAULT_DATABASES)]
    versions: Counter = Counter()
    failures: list[str] = []
    total = 0
    for path in paths:
        if not path.exists():
            print(f'skipped (absent): {path}')
            continue
        seen = check(path, versions, failures)
        total += seen
        print(f'{path}: {seen} rows')
    print(f'\n{total} stored assessments')
    for key, count in sorted(versions.items(), key=lambda item: (-item[1], str(item[0]))):
        assessment_version, gate, rubric, status = key
        print(f'  {count:5d}  {assessment_version} / {gate} / {rubric} / {status}')
    if failures:
        print(f'\nstored assessment checks: {len(failures)} errors')
        for failure in failures:
            print(f'  {failure}')
        return 1
    print('\nstored assessment checks: 0 errors')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
