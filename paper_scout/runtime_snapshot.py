"""Allowlisted runtime archives. Validate every member before installing any DB.

The archive holds the assessment databases, so it is private data and never belongs in a
public release, on Pages or in a tracked file. This module only builds and installs it;
where it is stored is the caller's decision, and .github/scripts/paper_scout_state.py
carries the private destination.

Manifest version 2 adds the provenance a restore needs in order to be audited: when the
snapshot was taken, which workflow and run produced it, and the row counts each database
carried at pack time. Version 1 archives still restore, and a v1 archive is still written
whenever the extra provenance is unavailable, so an older compatible snapshot is never
rejected for missing a field that did not exist when it was packed.
"""
from __future__ import annotations

import argparse
from datetime import UTC, datetime
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tarfile
import tempfile

STATE_PATHS = (
    "data/paper_scout.sqlite3",
    "data/deep_research/paper_scout.sqlite3",
    "data/engram/paper_scout.sqlite3",
)
LEGACY_PATHS = frozenset(STATE_PATHS[:2])
MANIFEST = "paper-scout-state-manifest.json"
SNAPSHOT_SCHEMA = "paper-scout-state-snapshot"
SUPPORTED_MANIFEST_VERSIONS = (1, 2)
CURRENT_MANIFEST_VERSION = 2
#: Tables whose row counts are recorded at pack time and re-checked on restore. A
#: restored database that is structurally valid but has lost rows is the failure mode a
#: bare integrity check cannot see.
COUNTED_TABLES = ("papers", "paper_quality_assessments", "runs")


def row_counts(path: Path) -> dict:
    """Row counts for the audited tables, or -1 for a table this database lacks."""
    counts = {}
    with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as db:
        present = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in COUNTED_TABLES:
            counts[table] = (db.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                             if table in present else -1)
    return counts


def verify_database(path: Path) -> None:
    with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError(f"corrupt state: {path.name}")
        tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {"papers", "runs", "notifications"}.issubset(tables):
            raise ValueError(f"not a Paper Scout state database: {path.name}")


def snapshot_manifest(root: Path = Path("."), source: dict | None = None) -> dict:
    """Build the manifest for the databases currently on disk.

    Every field except sha256 is provenance. The digests are what a restore enforces;
    the rest is what makes a restored snapshot auditable after the fact.
    """
    hashes, counts, sizes = {}, {}, {}
    for name in STATE_PATHS:
        path = root / name
        verify_database(path)  # Missing tracks must be initialized before publishing.
        wal = Path(str(path) + "-wal")
        if wal.exists() and wal.stat().st_size:
            raise ValueError("checkpoint all databases before creating the snapshot")
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        counts[name] = row_counts(path)
        sizes[name] = path.stat().st_size
    return {
        "version": CURRENT_MANIFEST_VERSION,
        "schema": SNAPSHOT_SCHEMA,
        "sha256": hashes,
        "databases": list(STATE_PATHS),
        "row_counts": counts,
        "size_bytes": sizes,
        "created_at": datetime.now(UTC).isoformat(),
        "source": source or _source_from_env(),
    }


def _source_from_env() -> dict:
    """Which workflow and run produced this snapshot, when running in Actions."""
    keys = {"workflow": "GITHUB_WORKFLOW", "run_id": "GITHUB_RUN_ID",
            "run_attempt": "GITHUB_RUN_ATTEMPT", "repository": "GITHUB_REPOSITORY",
            "ref": "GITHUB_REF", "sha": "GITHUB_SHA"}
    return {field: os.environ.get(name, "") for field, name in keys.items()}


def pack_snapshot(archive: Path, root: Path = Path("."), source: dict | None = None) -> dict:
    manifest = snapshot_manifest(root, source)
    encoded = json.dumps(manifest, sort_keys=True).encode()
    archive.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "w:gz") as tar:
        for name in STATE_PATHS:
            tar.add(root / name, arcname=name, recursive=False)
        info = tarfile.TarInfo(MANIFEST)
        info.size = len(encoded)
        tar.addfile(info, io.BytesIO(encoded))
    return manifest


def restore_snapshot(archive: Path, root: Path = Path("."),
                     report: dict | None = None) -> list[str]:
    """Install a verified snapshot, or raise without touching the databases on disk.

    Every check runs against the staged copy before anything is replaced, and the install
    itself is an atomic rename per database. When ``report`` is supplied it receives the
    manifest and the post-install verification, so a caller can log exactly what it
    restored without reopening the archive.
    """
    manifest: dict = {}
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp)
        with tarfile.open(archive, "r:gz") as tar:
            members = tar.getmembers()
            names = [member.name for member in members]
            if len(names) != len(set(names)):
                raise ValueError("duplicate snapshot members")
            allowed = {*STATE_PATHS, MANIFEST}
            if any(not m.isfile() or m.name not in allowed for m in members):
                raise ValueError("unexpected path or non-file member in runtime snapshot")
            database_names = set(names) - {MANIFEST}
            if MANIFEST in names:
                manifest = json.load(tar.extractfile(MANIFEST))
                hashes = manifest.get("sha256", {})
                version = manifest.get("version")
                if version not in SUPPORTED_MANIFEST_VERSIONS:
                    raise ValueError("incomplete or unsupported snapshot manifest")
                if set(hashes) != database_names or database_names != set(STATE_PATHS):
                    raise ValueError("incomplete or unsupported snapshot manifest")
                if version >= 2:
                    # A v2 manifest states its own schema and database list. Both are
                    # checked so a well-formed archive of something else cannot install.
                    if manifest.get("schema") != SNAPSHOT_SCHEMA:
                        raise ValueError("incomplete or unsupported snapshot manifest")
                    if list(manifest.get("databases", [])) != list(STATE_PATHS):
                        raise ValueError("incomplete or unsupported snapshot manifest")
            else:
                # Only the exact known two-track format predates checksums.
                if database_names != LEGACY_PATHS:
                    raise ValueError("incomplete legacy snapshot")
                hashes = {}
            for name in sorted(database_names):
                destination = stage / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("wb") as out:
                    shutil.copyfileobj(tar.extractfile(name), out)
                if hashes and hashlib.sha256(destination.read_bytes()).hexdigest() != hashes[name]:
                    raise ValueError(f"snapshot checksum mismatch: {name}")
                verify_database(destination)
        missing = sorted(set(STATE_PATHS) - database_names)
        for name in STATE_PATHS:
            destination = root / name
            if name in missing and destination.exists():
                verify_database(destination)
            for suffix in ("-wal", "-journal"):
                sidecar = Path(str(destination) + suffix)
                if sidecar.exists() and sidecar.stat().st_size:
                    raise ValueError("refusing to restore over live SQLite journal state")
        # Validation succeeded for the complete archive. Copy to destination
        # filesystems before atomically replacing each closed database.
        pending = []
        try:
            for name in sorted(database_names):
                destination = root / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                temporary = destination.with_name(destination.name + ".restore")
                pending.append((temporary, destination))
                shutil.copyfile(stage / name, temporary)
            for temporary, destination in pending:
                os.replace(temporary, destination)
        finally:
            for temporary, _ in pending:
                temporary.unlink(missing_ok=True)
        initialized = []
        if missing:
            from paper_scout.state import PaperStore
            for name in missing:
                destination = root / name
                if not destination.exists():
                    PaperStore(destination)
                    initialized.append(name)
        verification = verify_restored(root, manifest, database_names)
        if report is not None:
            report.update(manifest=manifest, verification=verification,
                          initialized=list(initialized))
        return initialized


def verify_restored(root: Path, manifest: dict, restored: set[str]) -> dict:
    """Re-check the installed databases against the manifest that described them.

    The staged copy was verified before the rename, so this confirms the bytes that
    actually landed. It raises rather than reporting a failure, because a caller that
    continued past a failed restore would be running on state it cannot account for.
    """
    hashes = manifest.get("sha256", {})
    expected_counts = manifest.get("row_counts", {})
    result: dict = {"databases": {}, "manifest_version": manifest.get("version"),
                    "created_at": manifest.get("created_at"),
                    "source": manifest.get("source", {})}
    for name in sorted(restored):
        path = root / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if hashes and actual != hashes.get(name):
            raise ValueError(f"restored state does not match its manifest: {name}")
        verify_database(path)
        counts = row_counts(path)
        if name in expected_counts and counts != expected_counts[name]:
            raise ValueError(f"restored state lost rows against its manifest: {name}")
        result["databases"][name] = {"sha256": actual, "row_counts": counts}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("pack", "restore"))
    parser.add_argument("archive", type=Path)
    parser.add_argument("--report", type=Path,
                        help="write the manifest and restore verification here as JSON")
    args = parser.parse_args()
    if args.operation == "pack":
        manifest = pack_snapshot(args.archive)
        print(f"Packed snapshot manifest v{manifest['version']}: "
              + ", ".join(f"{name}={manifest['sha256'][name][:12]}" for name in manifest["sha256"]))
        if args.report:
            args.report.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    else:
        report: dict = {}
        missing = restore_snapshot(args.archive, report=report)
        verification = report.get("verification", {})
        print(f"Restored verified runtime snapshot (manifest v{verification.get('manifest_version')}); "
              f"newly initialized paths: {missing}")
        for name, detail in sorted(verification.get("databases", {}).items()):
            print(f"  {name} sha256={detail['sha256'][:12]} rows={detail['row_counts']}")
        if args.report:
            args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
