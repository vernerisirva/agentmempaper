import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / ".github" / "scripts" / "prepare_paper_scout_state.py"


class PaperScoutStateSnapshotTest(unittest.TestCase):
    def test_wal_database_is_checkpointed_and_verified_before_snapshot(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "paper_scout.sqlite3"
            db = sqlite3.connect(state_path)
            try:
                self.assertEqual(db.execute("PRAGMA journal_mode=WAL").fetchone()[0].lower(), "wal")
                db.execute("CREATE TABLE papers (id INTEGER PRIMARY KEY, title TEXT)")
                db.execute("INSERT INTO papers(title) VALUES ('Persistent Memory')")
                db.commit()
            finally:
                db.close()

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(state_path)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with sqlite3.connect(state_path) as db:
                self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                self.assertEqual(db.execute("PRAGMA journal_mode").fetchone()[0].lower(), "delete")
                self.assertEqual(db.execute("SELECT title FROM papers").fetchone()[0], "Persistent Memory")
            self.assertFalse(state_path.with_name(state_path.name + "-wal").exists())
            self.assertFalse(state_path.with_name(state_path.name + "-shm").exists())

    def test_missing_optional_track_state_does_not_fail_snapshot_preparation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = Path(tmpdir) / "missing.sqlite3"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(missing)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("does not exist yet", result.stdout)


if __name__ == "__main__":
    unittest.main()
