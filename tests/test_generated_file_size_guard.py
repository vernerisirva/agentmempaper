import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / ".github" / "scripts" / "check_generated_file_sizes.py"


class GeneratedFileSizeGuardTest(unittest.TestCase):
    def test_allows_small_commit_candidate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            candidate = Path(tmpdir) / "docs" / "small.json"
            candidate.parent.mkdir()
            candidate.write_text("{}", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(candidate.parent), "--guard-bytes", "10"],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_near_limit_file_with_clear_path_and_size(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            candidate = Path(tmpdir) / "docs" / "large.json"
            candidate.parent.mkdir()
            with candidate.open("wb") as handle:
                handle.truncate(10 * 1024 * 1024)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(candidate.parent), "--guard-bytes", str(10 * 1024 * 1024)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn(str(candidate), result.stdout)
            self.assertIn("10.00 MiB", result.stdout)
            self.assertIn("GitHub's 100 MiB per-file limit", result.stdout)


if __name__ == "__main__":
    unittest.main()
