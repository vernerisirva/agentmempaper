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
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from paper_scout.promotion_protocol import (  # noqa: E402
    DUAL_PROMOTION_GATE_VERSIONS, GATE_ASSESSMENT_VERSIONS, INDEPENDENCE_FIELD,
    INDEPENDENCE_GATE_VERSIONS, PROMOTION_ASSESSMENT_VERSIONS,
    evaluation_independence_error, validate_receipt,
)
from paper_scout.quality_models import QualityAssessment  # noqa: E402

DEFAULT_DATABASES = ('data/paper_scout.sqlite3', 'data/deep_research/paper_scout.sqlite3',
                     'data/engram/paper_scout.sqlite3')
# A broken history should report its shape, not reproduce itself in the terminal. The
# count is always exact; only the listing is bounded, so nothing is silently dropped.
MAX_REPORTED_FAILURES = 50


def payloads(path: Path):
    """Yield one stored payload at a time, or a failure string for an unreadable row.

    A database that is present but is not an assessment history, and a row whose
    payload is not JSON, are both reported like any other unreadable row. Nothing here
    raises: the caller must be able to finish the remaining databases.
    """
    # The path is percent-encoded into the URI, so a database whose name contains
    # '?' or '#' is opened rather than misparsed as URI query or fragment syntax.
    try:
        connection = sqlite3.connect(f'file:{quote(str(path))}?mode=ro', uri=True)
    except (sqlite3.Error, OSError, ValueError) as exc:
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
                payload = json.loads(row[1])
            except (TypeError, ValueError) as exc:
                yield f'{path}: row {row[0]}: unreadable payload ({type(exc).__name__}: {exc})'
                continue
            # Valid JSON is not necessarily a stored assessment. Anything that is not
            # an object is reported like any other unreadable row rather than handed on.
            if not isinstance(payload, dict):
                yield f'{path}: row {row[0]}: unreadable payload (not an object)'
                continue
            yield payload
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
    if (gate in DUAL_PROMOTION_GATE_VERSIONS
            and value.get('assessment_version') != GATE_ASSESSMENT_VERSIONS.get(gate)):
        return f'assessment version {value.get("assessment_version")} on gate {gate}'
    execution = value.get('execution') or {}
    roles = ('primary', 'adjudicator')
    carried = [role for role in roles if INDEPENDENCE_FIELD in (execution.get(role) or {})]
    if carried and gate not in INDEPENDENCE_GATE_VERSIONS:
        return f'gate {gate} carries evaluation independence'
    # A current-gate row is named just as specifically as a legacy one: the dimension
    # is required from every role, and its declared values must hold together. This is
    # the same enum-only predicate the gate applies, and it reads no prose here either.
    if gate in INDEPENDENCE_GATE_VERSIONS and execution.get('outcome') == 'success':
        missing = [role for role in roles if role not in carried]
        if missing:
            return f'{", ".join(missing)} missing evaluation independence'
        if execution.get('independence_contract') is None:
            return 'missing evaluation-independence contract version'
    for role in carried:
        if evaluation_independence_error(execution[role], role) is not None:
            return f'{role} evaluation independence values violate their contract'
    return None


def record(failures: list, counted: list, message: str) -> None:
    """Count every failure, keep the first few verbatim."""
    counted[0] += 1
    if len(failures) < MAX_REPORTED_FAILURES:
        failures.append(message)


def check(path: Path, versions: Counter, failures: list, counted: list) -> int:
    seen = 0
    for value in payloads(path):
        if isinstance(value, str):
            record(failures, counted, value)
            continue
        seen += 1
        # Nothing about one row may end the run, so the whole of its handling is
        # guarded, not only the load. A row is reported, never repaired or rethrown.
        try:
            versions[(value.get('assessment_version'), value.get('quality_gate_version'),
                      value.get('rubric_version'), value.get('quality_status'))] += 1
            assessment = QualityAssessment.from_dict(value)
            if (assessment.quality_gate_version in DUAL_PROMOTION_GATE_VERSIONS
                    and assessment.execution.get('outcome') == 'success'):
                validate_receipt(assessment)
        except Exception as exc:  # noqa: BLE001 - report every bad row, never raise.
            named = None
            try:
                named = diagnosis(value)
            except Exception:  # noqa: BLE001 - a message must never mask the failure.
                pass
            detail = f'{type(exc).__name__}: {exc}' if named is None else named
            record(failures, counted, f'{path}: {value.get("canonical_id", "?")}: {detail}')
    return seen


def main(argv: list[str] | None = None) -> int:
    """Check the named databases, or the default set when none is named.

    This is the function contract: argv=None means no argument and selects the default
    databases, while an empty list means exactly that and checks nothing, so a caller
    can ask for zero databases on purpose. Running the script with no arguments is the
    no-argument case and checks the default set; the command line cannot ask for zero.
    """
    paths = [Path(p) for p in (DEFAULT_DATABASES if argv is None else argv)]
    versions: Counter = Counter()
    failures: list[str] = []
    counted = [0]
    total = 0
    for path in paths:
        try:
            present = path.exists()
        except OSError as exc:
            record(failures, counted, f'{path}: unreadable database ({type(exc).__name__}: {exc})')
            continue
        if not present:
            print(f'skipped (absent): {path}')
            continue
        seen = check(path, versions, failures, counted)
        total += seen
        print(f'{path}: {seen} rows')
    print(f'\n{total} stored assessments')
    for key, count in sorted(versions.items(), key=lambda item: (-item[1], str(item[0]))):
        assessment_version, gate, rubric, status = key
        print(f'  {count:5d}  {assessment_version} / {gate} / {rubric} / {status}')
    if counted[0]:
        print(f'\nstored assessment checks: {counted[0]} errors')
        for failure in failures:
            print(f'  {failure}')
        if counted[0] > len(failures):
            print(f'  ... and {counted[0] - len(failures)} more, not listed')
        return 1
    print('\nstored assessment checks: 0 errors')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:] or None))
