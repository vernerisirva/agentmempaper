import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / ".github" / "scripts" / "restore-paper-scout-state.sh"


class PaperScoutStateMigrationTest(unittest.TestCase):
    def _git(self, root: Path, *args: str) -> str:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def test_named_seed_survives_an_intervening_non_state_commit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self._git(root, "init", "--quiet")
            self._git(root, "config", "user.name", "test")
            self._git(root, "config", "user.email", "test@example.test")
            state = root / "data" / "paper_scout.sqlite3"
            deep_state = root / "data" / "deep_research" / "paper_scout.sqlite3"
            deep_state.parent.mkdir(parents=True)
            state.parent.mkdir(exist_ok=True)
            state.write_bytes(b"agent-memory-seed")
            deep_state.write_bytes(b"deep-research-seed")
            self._git(root, "add", "data")
            self._git(root, "commit", "--quiet", "-m", "seed")
            seed_ref = self._git(root, "rev-parse", "HEAD")

            self._git(root, "rm", "--quiet", "data/paper_scout.sqlite3", "data/deep_research/paper_scout.sqlite3")
            self._git(root, "commit", "--quiet", "-m", "stop tracking state")
            (root / "README.md").write_text("intervening commit\n", encoding="utf-8")
            self._git(root, "add", "README.md")
            self._git(root, "commit", "--quiet", "-m", "normal change")

            result = subprocess.run(
                ["bash", str(SCRIPT)],
                cwd=root,
                env={**os.environ, "PAPER_SCOUT_STATE_SEED_REF": seed_ref},
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(state.read_bytes(), b"agent-memory-seed")
            self.assertEqual(deep_state.read_bytes(), b"deep-research-seed")
            self.assertIn(seed_ref, result.stdout)


if __name__ == "__main__":
    unittest.main()
