#!/usr/bin/env python3
"""Decide whether this run is a duplicate of today's daily Paper Scout run.

The daily run has two triggers. An external scheduler dispatches the workflow at 06:00
Europe/Stockholm with `trigger: daily`, because GitHub's own cron queue starts scheduled
runs four to six hours late. The GitHub cron stays as a fallback for a day the external
trigger does not fire. Both assess, so without this guard a normal day would run the
scientific stage twice and spend twice the frozen per-run bound.

The rule: a daily run (either trigger) skips when another daily run already concluded
`success` on the same Stockholm calendar day. Only completed successes count. A queued run
is not evidence, because under the shared concurrency group every later run is queued
while this one executes, and counting it would make both skip. A failed or cancelled run
is not evidence either, so the second trigger acts as a retry.

Two modes:

* default (the daily-guard job): writes `skip=true|false` to $GITHUB_OUTPUT, so a
  duplicate run skips the scout job cleanly and still shows green.
* `--enforce` (first step of the scout job): exits 1 instead. "Re-run failed jobs" and
  "Re-run job" do not re-run a job that succeeded, so they replay the daily-guard job's
  first-attempt `skip=false`; this check inside the spending job is what stops such a
  re-run from assessing a second time after the other trigger has succeeded.

Any error fails the step, which stops the run: a guard that cannot see history must not
risk a second assessment. Other operator actions stay outside the rule: re-running a
successful run with "Re-run all jobs" before the other trigger has succeeded will assess
again. To redeploy Pages without assessing, dispatch with `deploy_only`.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo

STOCKHOLM = ZoneInfo("Europe/Stockholm")
DAILY_TITLE = "Paper Scout (daily trigger)"


def is_daily_run(run: dict) -> bool:
    return run.get("event") == "schedule" or run.get("display_title") == DAILY_TITLE


def stockholm_day_start(now: datetime) -> datetime:
    day = now.astimezone(STOCKHOLM).date()
    return datetime.combine(day, time(0), tzinfo=STOCKHOLM).astimezone(timezone.utc)


def earlier_success_today(runs: list[dict], current_run_id: int, now: datetime) -> dict | None:
    start = stockholm_day_start(now)
    for run in runs:
        if run.get("id") == current_run_id or not is_daily_run(run):
            continue
        created = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
        if created >= start and run.get("conclusion") == "success":
            return run
    return None


def fetch_runs(repository: str, workflow: str, token: str, since: datetime) -> list[dict]:
    query = urllib.parse.urlencode({
        "created": ">=" + since.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "success",
        "per_page": 100,
    })
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repository}/actions/workflows/{workflow}/runs?{query}",
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["workflow_runs"]


def decide(env: dict, now: datetime) -> tuple[bool, str]:
    if env["IS_DAILY_RUN"] != "true":
        return False, "not a daily run; the guard does not apply"
    runs = fetch_runs(env["GITHUB_REPOSITORY"], "paper-scout.yml", env["GITHUB_TOKEN"],
                      stockholm_day_start(now))
    earlier = earlier_success_today(runs, int(env["GITHUB_RUN_ID"]), now)
    if earlier:
        return True, f"run {earlier['id']} ({earlier['event']}) already succeeded today"
    return False, "no daily run has succeeded yet today"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--enforce", action="store_true",
                        help="fail instead of writing a skip output")
    args = parser.parse_args(argv)
    skip, reason = decide(os.environ, datetime.now(timezone.utc))
    if args.enforce:
        if skip:
            print(f"::error::Refusing a second daily assessment: {reason}. A partial re-run "
                  "reuses the first attempt's guard decision; dispatch with deploy_only to "
                  "redeploy without assessing.")
            return 1
        print(f"daily guard re-check passed: {reason}")
        return 0
    print(f"skip={str(skip).lower()}: {reason}")
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        output.write(f"skip={str(skip).lower()}\n")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
        summary.write(f"### Daily run guard\n{'Skipped' if skip else 'Proceeding'}: {reason}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
