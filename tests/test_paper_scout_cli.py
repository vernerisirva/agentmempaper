import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from paper_scout.cli import main


class PaperScoutCliTest(unittest.TestCase):
    def test_smoke_live_accepts_ci_flag(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "missing.yaml"
            with patch("paper_scout.cli.run_live_smoke") as run_live_smoke:
                run_live_smoke.return_value = {
                    "candidate_count": 0,
                    "unique_count": 0,
                    "source_failures": [],
                    "report_path": str(Path(tmpdir) / "reports" / "live-smoke-2026-06-26.md"),
                }

                with redirect_stdout(io.StringIO()):
                    exit_code = main(
                        [
                            "--config",
                            str(config_path),
                            "smoke-live",
                            "--days",
                            "14",
                            "--max-results-per-source",
                            "25",
                            "--no-notify",
                            "--ci",
                            "--date",
                            "2026-06-26",
                        ]
                    )

            self.assertEqual(exit_code, 0)
            self.assertTrue(run_live_smoke.call_args.kwargs["ci"])
            self.assertEqual(run_live_smoke.call_args.kwargs["days"], 14)
            self.assertEqual(run_live_smoke.call_args.kwargs["max_results_per_source"], 25)


if __name__ == "__main__":
    unittest.main()
