import hashlib
import io
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tarfile
import tempfile
import unittest

from paper_scout.models import PaperCandidate, ClassificationResult
from paper_scout.runtime_snapshot import STATE_PATHS, MANIFEST, pack_snapshot, restore_snapshot
from paper_scout.state import PaperStore

ROOT = Path(__file__).resolve().parents[1]


class EngramStateTests(unittest.TestCase):
    def make_state(self, root, names=STATE_PATHS):
        for i, name in enumerate(names):
            store = PaperStore(root / name)
            paper = PaperCandidate(f"Track {i} memory", [], "Synthetic state test", "fixture", str(i))
            key = store.upsert_paper(paper, ClassificationResult(90, "relevant", "Synthetic test"))
            store.mark_notified([key], "2026-09-04")
            store.record_failed_query(name, "arxiv", "query", 20, "timeout")

    def fingerprint(self, root, names=STATE_PATHS):
        return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}

    def test_three_track_round_trip_preserves_papers_notifications_and_retry_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_state(root)
            archive = root / "state.tar.gz"
            pack_snapshot(archive, root)
            with tarfile.open(archive) as tar:
                self.assertEqual(set(tar.getnames()), {*STATE_PATHS, MANIFEST})
            fresh = root / "fresh"
            self.assertEqual(restore_snapshot(archive, fresh), [])
            self.assertEqual(self.fingerprint(root), self.fingerprint(fresh))
            for name in STATE_PATHS:
                store = PaperStore(fresh / name)
                self.assertEqual(store.paper_count(), 1)
                self.assertEqual(len(store.get_notified_for_date("2026-09-04")), 1)
                self.assertEqual(len(store.failed_queries(name)), 1)

    def test_older_two_track_snapshot_initializes_only_engram(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_state(root, STATE_PATHS[:2])
            archive = root / "legacy.tar.gz"
            with tarfile.open(archive, "w:gz") as tar:
                for name in STATE_PATHS[:2]:
                    tar.add(root / name, arcname=name)
            fresh = root / "fresh"
            self.assertEqual(restore_snapshot(archive, fresh), [STATE_PATHS[2]])
            self.assertEqual(self.fingerprint(root, STATE_PATHS[:2]), self.fingerprint(fresh, STATE_PATHS[:2]))
            self.assertEqual(PaperStore(fresh / STATE_PATHS[2]).paper_count(), 0)
            # Reusing a legacy snapshot must preserve existing Engram records too.
            self.make_state(fresh, STATE_PATHS[2:])
            before = self.fingerprint(fresh, STATE_PATHS[2:])
            restore_snapshot(archive, fresh)
            self.assertEqual(self.fingerprint(fresh, STATE_PATHS[2:]), before)

    def test_corrupt_missing_or_unexpected_archive_never_mutates_existing_tracks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_state(root)
            before = self.fingerprint(root)
            archive = root / "invalid.tar.gz"
            for defect in ("corrupt", "missing_legacy", "missing_modern", "checksum", "path", "symlink"):
                with self.subTest(defect=defect):
                    with tarfile.open(archive, "w:gz") as tar:
                        names = STATE_PATHS[:1] if defect == "missing_legacy" else STATE_PATHS[:2]
                        for name in names:
                            content = b"corrupt" if defect == "corrupt" and name == names[-1] else (root / name).read_bytes()
                            member = tarfile.TarInfo(name)
                            member.size = len(content)
                            tar.addfile(member, io.BytesIO(content))
                        if defect in {"missing_modern", "checksum"}:
                            hashes = {n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in STATE_PATHS}
                            if defect == "checksum":
                                content = (root / STATE_PATHS[2]).read_bytes()
                                info = tarfile.TarInfo(STATE_PATHS[2]); info.size = len(content)
                                tar.addfile(info, io.BytesIO(content))
                                hashes[STATE_PATHS[0]] = "bad"
                            content = json.dumps({"version": 1, "sha256": hashes}).encode()
                            info = tarfile.TarInfo(MANIFEST); info.size = len(content)
                            tar.addfile(info, io.BytesIO(content))
                        if defect in {"path", "symlink"}:
                            info = tarfile.TarInfo("../escape" if defect == "path" else STATE_PATHS[2])
                            if defect == "symlink":
                                info.type = tarfile.SYMTYPE; info.linkname = "/tmp/escape"
                            tar.addfile(info, io.BytesIO())
                    with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                        restore_snapshot(archive, root)
                    self.assertEqual(self.fingerprint(root), before)

    def test_snapshot_upload_requires_every_track_and_prepared_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_state(root, STATE_PATHS[:2])
            with self.assertRaises(sqlite3.OperationalError):
                pack_snapshot(root / "snapshot.tar.gz", root)
            self.make_state(root, STATE_PATHS[2:])
            Path(str(root / STATE_PATHS[2]) + "-wal").write_bytes(b"uncheckpointed")
            with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                pack_snapshot(root / "snapshot.tar.gz", root)

    def test_download_permission_error_fails_instead_of_claiming_new_track(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = root / "gh"
            fake.write_text('#!/bin/sh\necho "HTTP 403: unavailable" >&2\nexit 1\n')
            fake.chmod(0o755)
            result = subprocess.run(["bash", str(ROOT / ".github/scripts/download-paper-scout-state.sh")],
                                    cwd=root, env={**os.environ, "RUNNER_TEMP": str(root), "PATH": str(root) + os.pathsep + os.environ["PATH"]},
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unable to determine", result.stdout)
            self.assertFalse((root / "data").exists())
