"""Allowlisted runtime archives. Validate every member before installing any DB."""
from __future__ import annotations

import argparse
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


def verify_database(path: Path) -> None:
    with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError(f"corrupt state: {path.name}")
        tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {"papers", "runs", "notifications"}.issubset(tables):
            raise ValueError(f"not a Paper Scout state database: {path.name}")


def pack_snapshot(archive: Path, root: Path = Path(".")) -> None:
    hashes = {}
    for name in STATE_PATHS:
        path = root / name
        verify_database(path)  # Missing tracks must be initialized before publishing.
        wal = Path(str(path) + "-wal")
        if wal.exists() and wal.stat().st_size:
            raise ValueError("checkpoint all databases before creating the snapshot")
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = json.dumps({"version": 1, "sha256": hashes}, sort_keys=True).encode()
    archive.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "w:gz") as tar:
        for name in STATE_PATHS:
            tar.add(root / name, arcname=name, recursive=False)
        info = tarfile.TarInfo(MANIFEST)
        info.size = len(manifest)
        tar.addfile(info, io.BytesIO(manifest))


def restore_snapshot(archive: Path, root: Path = Path(".")) -> list[str]:
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
                if manifest.get("version") != 1 or set(hashes) != database_names or database_names != set(STATE_PATHS):
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
        return initialized


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("pack", "restore"))
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    if args.operation == "pack":
        pack_snapshot(args.archive)
        print("Prepared checksummed three-track archive.")
    else:
        missing = restore_snapshot(args.archive)
        print(f"Restored verified runtime snapshot; newly initialized paths: {missing}")


if __name__ == "__main__":
    main()
