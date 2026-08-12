#!/usr/bin/env python3
"""Reject generated commit candidates that approach GitHub's file-size limit."""

from __future__ import annotations

import argparse
from pathlib import Path


GITHUB_FILE_LIMIT_BYTES = 100 * 1024 * 1024
DEFAULT_GUARD_BYTES = 95 * 1024 * 1024


def candidate_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file())
    return files


def format_size(size: int) -> str:
    return f"{size / 1024 / 1024:.2f} MiB"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Files or directories that will be passed to git add.",
    )
    parser.add_argument(
        "--guard-bytes",
        type=int,
        default=DEFAULT_GUARD_BYTES,
        help="Fail for files at or above this size (default: 95 MiB).",
    )
    args = parser.parse_args(argv)

    if args.guard_bytes <= 0 or args.guard_bytes > GITHUB_FILE_LIMIT_BYTES:
        parser.error(f"--guard-bytes must be between 1 and {GITHUB_FILE_LIMIT_BYTES}")

    oversized = sorted(
        ((path, path.stat().st_size) for path in candidate_files(args.paths) if path.stat().st_size >= args.guard_bytes),
        key=lambda item: item[1],
        reverse=True,
    )
    if not oversized:
        return 0

    print(
        "Refusing to stage generated files that approach GitHub's 100 MiB per-file limit. "
        f"The workflow guard is {format_size(args.guard_bytes)}."
    )
    for path, size in oversized:
        print(f"  - {path} ({format_size(size)})")
    print("Move runtime/binary state out of the commit candidates, then rerun the workflow.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
