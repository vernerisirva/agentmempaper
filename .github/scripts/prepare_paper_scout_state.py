#!/usr/bin/env python3
"""Verify a complete SQLite snapshot and fold any WAL contents into it."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def prepare_database(path: Path) -> None:
    if not path.exists():
        print(f"State file does not exist yet; it will not be included in this snapshot: {path}")
        return
    db = sqlite3.connect(path)
    try:
        mode = str(db.execute("PRAGMA journal_mode").fetchone()[0]).lower()
        if mode == "wal":
            db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        integrity = str(db.execute("PRAGMA integrity_check").fetchone()[0])
    finally:
        db.close()
    # SQLite cannot always switch journal mode while the connection that
    # checkpointed WAL is still open. Reopen after the checkpoint so the main
    # database becomes a self-contained release asset.
    if mode == "wal":
        db = sqlite3.connect(path)
        try:
            final_mode = str(db.execute("PRAGMA journal_mode=DELETE").fetchone()[0]).lower()
        finally:
            db.close()
        if final_mode != "delete":
            raise RuntimeError(f"could not switch {path} from WAL to rollback-journal mode: {final_mode}")
    if integrity.lower() != "ok":
        raise RuntimeError(f"SQLite integrity check failed for {path}: {integrity}")
    for suffix in ("-journal", "-wal", "-shm"):
        path.with_name(path.name + suffix).unlink(missing_ok=True)
    print(f"Prepared consistent SQLite state snapshot: {path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args(argv)
    for path in args.paths:
        prepare_database(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
