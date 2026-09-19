#!/usr/bin/env python3
"""Restore and persist Paper Scout runtime state from a PRIVATE remote destination.

The runtime state is the assessment databases. It is private data and must never reach a
public GitHub release, GitHub Pages or a tracked file in the public repository. This
script is the only supported transport, and it refuses to run against the public
repository at all, so a missing configuration cannot silently fall back to the old
public-release behaviour.

Destination
    A dedicated private GitHub repository, named by PAPER_SCOUT_STATE_REPO, holding one
    mutable release asset per snapshot tag. Privacy comes from the repository's own
    access control: an unauthenticated request for a private repository's release asset
    is rejected by GitHub, so the archive is not readable without the token. The token is
    a fine-grained PAT scoped to that one repository with Contents: read and write, and
    nothing else, supplied as PAPER_SCOUT_STATE_TOKEN.

Fail-closed
    Every failure mode here stops the run rather than continuing on state it cannot
    account for. A restore that cannot reach the destination, finds a corrupt or partial
    archive, or fails verification is an error. Empty state is created only when the
    caller explicitly asks for it with --allow-initialize, which the scheduled workflow
    never passes, because initializing empty databases over a real history is the one
    mistake that silently destroys the scientific record.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from paper_scout.runtime_snapshot import (  # noqa: E402
    STATE_PATHS, pack_snapshot, restore_snapshot, snapshot_manifest,
)

#: Each state path's track name. Derived names are not used: the agent_memory database
#: lives at data/paper_scout.sqlite3, whose parent directory is "data", so a path-derived
#: label would publish restore_sha256_data and no consumer keyed on the track would match.
TRACK_FOR_STATE_PATH = {
    "data/paper_scout.sqlite3": "agent_memory",
    "data/deep_research/paper_scout.sqlite3": "deep_research",
    "data/engram/paper_scout.sqlite3": "engram",
}

ASSET_NAME = "paper-scout-state.tar.gz"
DEFAULT_TAG = "paper-scout-runtime-state"
STATE_REPO_ENV = "PAPER_SCOUT_STATE_REPO"
STATE_TOKEN_ENV = "PAPER_SCOUT_STATE_TOKEN"
#: The public repository. Naming it here lets the script refuse it explicitly rather than
#: relying on whoever edits the workflow to remember why the destination has to differ.
#: Compared case-insensitively, because GitHub repository names are.
PUBLIC_REPO = "vernerisirva/agentmempaper"


class StateError(RuntimeError):
    """A state transport failure. Always fatal; never recovered by initializing state."""


def _is_missing_release(stderr: str) -> bool:
    """Whether gh reported an absent release rather than a failure to ask.

    The distinction matters in both directions: reading an access failure as "no snapshot
    yet" is how a healthy history gets replaced by empty databases, and reading it as
    "release missing" on persist hides the real transport error behind a create attempt.
    """
    lowered = (stderr or "").lower()
    if "403" in lowered or "forbidden" in lowered or "unauthor" in lowered:
        return False
    return "not found" in lowered or "404" in lowered


def _run(args: list[str], token: str, check: bool = True) -> subprocess.CompletedProcess:
    """Invoke gh with the state token only, never the workflow's own GITHUB_TOKEN.

    GH_TOKEN is replaced rather than augmented so a inherited workflow token cannot be
    used against the private destination, and the value is never echoed.
    """
    env = {**os.environ, "GH_TOKEN": token, "GITHUB_TOKEN": token}
    return subprocess.run(args, env=env, check=check, capture_output=True, text=True)


def _destination() -> tuple[str, str]:
    repo = (os.environ.get(STATE_REPO_ENV, "") or "").strip()
    token = (os.environ.get(STATE_TOKEN_ENV, "") or "").strip()
    if not repo:
        raise StateError(
            f"{STATE_REPO_ENV} is not set. Private durable state has no destination, and "
            "the public release is not an acceptable fallback for assessment databases.")
    if repo.lower() == PUBLIC_REPO.lower():
        raise StateError(
            f"{STATE_REPO_ENV} points at the public repository {PUBLIC_REPO}. Runtime "
            "state must go to a private destination.")
    if not token:
        raise StateError(
            f"{STATE_TOKEN_ENV} is not set. The private state repository cannot be "
            "reached, and no unauthenticated fallback exists.")
    return repo, token


def assert_private(repo: str, token: str) -> None:
    """Confirm the destination really is private before anything is written to it.

    Checked on every persist rather than once at setup: a repository that is flipped to
    public later would otherwise start publishing the databases silently.
    """
    probe = _run(["gh", "repo", "view", repo, "--json", "isPrivate,visibility"], token, check=False)
    if probe.returncode != 0:
        raise StateError(f"cannot read {repo}; check {STATE_TOKEN_ENV} scope: {probe.stderr.strip()[:400]}")
    try:
        detail = json.loads(probe.stdout)
    except ValueError as exc:
        raise StateError(f"unreadable repository metadata for {repo}") from exc
    if not detail.get("isPrivate", False):
        raise StateError(f"refusing to write runtime state: {repo} is {detail.get('visibility')}, not private")


def restore(tag: str, allow_initialize: bool, report_path: Path | None) -> int:
    repo, token = _destination()
    assert_private(repo, token)
    temp = Path(os.environ.get("RUNNER_TEMP", "/tmp"))
    archive = temp / ASSET_NAME

    view = _run(["gh", "release", "view", tag, "--repo", repo, "--json", "id"], token, check=False)
    if view.returncode != 0:
        if not _is_missing_release(view.stderr):
            raise StateError(f"cannot determine whether private state exists: {view.stderr.strip()[:400]}")
        # No snapshot exists. This is only legitimate on a deliberate first
        # initialization; on any later run it means the state was lost.
        if not allow_initialize:
            raise StateError(
                f"no private state snapshot '{tag}' exists in {repo}. Refusing to continue "
                "with empty state. Pass --allow-initialize only for a deliberate first run.")
        print(f"::warning::No private state snapshot in {repo}; initializing empty state by request.")
        from paper_scout.state import PaperStore
        for name in STATE_PATHS:
            path = Path(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                PaperStore(path)
        if report_path:
            report_path.write_text(json.dumps({"restored": False, "initialized": list(STATE_PATHS)},
                                              indent=2) + "\n")
        return 0

    archive.unlink(missing_ok=True)
    download = _run(["gh", "release", "download", tag, "--repo", repo,
                     "--pattern", ASSET_NAME, "--dir", str(temp)], token, check=False)
    if download.returncode != 0:
        raise StateError(f"private state download failed: {download.stderr.strip()[:400]}")
    if not archive.exists():
        raise StateError("private state asset is missing from the snapshot release")

    report: dict = {}
    try:
        restore_snapshot(archive, report=report)
    except Exception as exc:
        # Corrupt, partial, or manifest-mismatched state. restore_snapshot validates the
        # staged copy before replacing anything, so the databases on disk are untouched.
        raise StateError(f"private state failed verification and was not installed: {exc}") from exc

    verification = report.get("verification", {})
    print(f"Restored private state from {repo}:{tag} (manifest v{verification.get('manifest_version')}, "
          f"created {verification.get('created_at')})")
    for name, detail in sorted(verification.get("databases", {}).items()):
        print(f"  {name} sha256={detail['sha256']} rows={detail['row_counts']}")
    if report_path:
        report_path.write_text(json.dumps({"restored": True, **report}, indent=2, sort_keys=True) + "\n")
    _emit_output("state_restore_manifest_version", str(verification.get("manifest_version", "")))
    _emit_output("state_restore_created_at", str(verification.get("created_at", "")))
    for name, detail in sorted(verification.get("databases", {}).items()):
        _emit_output(f"restore_sha256_{_track_label(name)}", detail["sha256"])
    return 0


def _track_label(state_path: str) -> str:
    """The track a state path belongs to, or a safe slug for an unknown path."""
    return TRACK_FOR_STATE_PATH.get(state_path) or state_path.replace("/", "_").replace(".", "_")


def persist(tag: str, report_path: Path | None) -> int:
    repo, token = _destination()
    assert_private(repo, token)
    temp = Path(os.environ.get("RUNNER_TEMP", "/tmp"))
    archive = temp / ASSET_NAME
    archive.unlink(missing_ok=True)

    # Build and verify the snapshot before it leaves the runner. pack_snapshot refuses a
    # database that fails an integrity check or still has an unflushed WAL.
    manifest = pack_snapshot(archive)
    verify: dict = {}
    # Round-trip the archive into a throwaway root. Publishing a snapshot that cannot be
    # restored is the failure this catches, and it is cheap compared with losing state.
    # The scratch copy holds the assessment databases in the clear, so it is removed on
    # every path out of here, including a failed verification.
    scratch = temp / "paper-scout-state-verify"
    shutil.rmtree(scratch, ignore_errors=True)
    scratch.mkdir(parents=True)
    try:
        restore_snapshot(archive, root=scratch, report=verify)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    view = _run(["gh", "release", "view", tag, "--repo", repo, "--json", "id"], token, check=False)
    if view.returncode != 0:
        # Only an absent release justifies creating one. An auth, network or rate-limit
        # failure must surface as itself rather than as a confusing create error.
        if not _is_missing_release(view.stderr):
            raise StateError(f"cannot determine whether the private state release exists: "
                             f"{view.stderr.strip()[:400]}")
        create = _run(["gh", "release", "create", tag, "--repo", repo, "--prerelease",
                       "--title", "Paper Scout runtime state",
                       "--notes", "Private mutable runtime state. Never publish. "
                                  "Do not delete while scheduled workflows are active."],
                      token, check=False)
        if create.returncode != 0:
            raise StateError(f"cannot create the private state release: {create.stderr.strip()[:400]}")
    try:
        upload = _run(["gh", "release", "upload", tag, f"{archive}#{ASSET_NAME}",
                       "--repo", repo, "--clobber"], token, check=False)
        if upload.returncode != 0:
            raise StateError(f"private state upload failed: {upload.stderr.strip()[:400]}")
    finally:
        # The local archive is a plaintext copy of the databases; do not leave it behind.
        archive.unlink(missing_ok=True)

    print(f"Persisted private state to {repo}:{tag} (manifest v{manifest['version']})")
    for name in manifest["databases"]:
        print(f"  {name} sha256={manifest['sha256'][name]} rows={manifest['row_counts'][name]}")
    if report_path:
        report_path.write_text(json.dumps({"persisted": True, "manifest": manifest,
                                           "roundtrip": verify.get("verification", {})},
                                          indent=2, sort_keys=True) + "\n")
    _emit_output("state_persist_manifest_version", str(manifest["version"]))
    for name in manifest["databases"]:
        _emit_output(f"persist_sha256_{_track_label(name)}", manifest["sha256"][name])
    return 0


def inspect(report_path: Path | None) -> int:
    """Report what a snapshot of the current working state would contain."""
    manifest = snapshot_manifest()
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if report_path:
        report_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return 0


def _emit_output(name: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if path and "\n" not in value:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(f"{name}={value}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("operation", choices=("restore", "persist", "inspect"))
    parser.add_argument("--tag", default=DEFAULT_TAG)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--allow-initialize", action="store_true",
                        help="create empty databases when no snapshot exists; first run only")
    args = parser.parse_args(argv)
    try:
        if args.operation == "restore":
            return restore(args.tag, args.allow_initialize, args.report)
        if args.operation == "persist":
            return persist(args.tag, args.report)
        return inspect(args.report)
    except StateError as exc:
        print(f"::error::{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
