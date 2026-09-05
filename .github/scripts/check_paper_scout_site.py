#!/usr/bin/env python3
"""Validate published schemas, local links, workflow tracks, and runtime exclusion."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from paper_scout.config import TRACK_CONFIG_PATHS, load_config
from paper_scout.runtime_snapshot import STATE_PATHS


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in {"a", "link", "script", "img"}:
            self.links.extend(value for key, value in attrs if key in {"href", "src"} and value)


def validate_site(root: Path) -> list[str]:
    errors = []
    for track in TRACK_CONFIG_PATHS:
        config = load_config(ROOT / TRACK_CONFIG_PATHS[track], env={})
        site = root / config.docs_dir
        schema_path = site / "data/paper-card.schema.json"
        if not schema_path.exists():
            errors.append(f"missing schema for {track}")
            continue
        validator = jsonschema.Draft202012Validator(json.loads(schema_path.read_text()))
        for path in (site / "papers").glob("*.json"):
            errors.extend(f"{path.relative_to(root)}: {e.message}" for e in validator.iter_errors(json.loads(path.read_text())))
        for path in [*site.glob("*.html"), *(site / "papers").glob("*.html")]:
            links = Links()
            links.feed(path.read_text())
            for link in links.links:
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.exists():
                    errors.append(f"broken local link: {path.relative_to(root)} -> {link}")
    forbidden = re.compile(r"(?:\.sqlite3(?:-wal|-shm|-journal|\.restore)?$|\.pdf$|(?:^|/)\.env(?:\.|$)|(?:^|/)(?:cache|__pycache__)/|\.pyc$)", re.I)
    secret = re.compile(r"(?<![A-Za-z0-9])(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----|/Users/[^/\s]+/)")
    for base in (root / "docs", root / "digests", root / "reports/paper_scout"):
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if forbidden.search(str(path.relative_to(root))):
                errors.append(f"runtime file in generated outputs: {path.relative_to(root)}")
            text = path.read_text(encoding="utf-8", errors="replace")
            if secret.search(text):
                errors.append(f"possible secret/private local path: {path.relative_to(root)}")
    return errors


def validate_workflows(root: Path) -> list[str]:
    errors = []
    for name in ("paper-scout.yml", "paper-scout-backfill.yml"):
        path = root / ".github/workflows" / name
        text = path.read_text()
        workflow = yaml.safe_load(text)
        if not isinstance(workflow.get("jobs"), dict):
            errors.append(f"missing workflow jobs: {name}")
        steps = [step for job in workflow["jobs"].values() for step in job["steps"]]
        commands = "\n".join(step.get("run", "") for step in steps)
        for track in (TRACK_CONFIG_PATHS if name == "paper-scout.yml" else ("agent_memory", "engram")):
            for command in (("run", "build-site") if name == "paper-scout.yml" else ("backfill", "build-site")):
                if f"{command} --track {track}" not in commands:
                    errors.append(f"{name} missing {command} for {track}")
        if any(state not in commands for state in STATE_PATHS):
            errors.append(f"{name} missing snapshot preparation path")
        if "smoke-live --track engram" in commands:
            errors.append(f"{name} duplicates Engram live search")
        if "git add -- digests docs reports/paper_scout" not in commands or "Refusing to commit Paper Scout runtime state" not in commands:
            errors.append(f"{name} missing generated staging guard")
        if any("ingest-seeds --track engram" in s.get("run", "") and "PAPER_SCOUT_WEBHOOK_URL" in s.get("env", {}) for s in steps) and name != "paper-scout.yml":
            errors.append(f"{name} exposes notification credentials to backfill")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate_site(args.root) + validate_workflows(args.root)
    for error in errors:
        print(error)
    print(f"site/schema/link/exposure/workflow checks: {len(errors)} errors")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
