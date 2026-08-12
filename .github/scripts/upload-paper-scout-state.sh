#!/usr/bin/env bash
# Publish a single mutable release asset rather than accumulating immutable
# Actions caches. The calling workflow serializes all state writers.
set -euo pipefail

release_tag="paper-scout-runtime-state"
archive_path="${RUNNER_TEMP:?RUNNER_TEMP is required}/paper-scout-state.tar.gz"
state_paths=(data/paper_scout.sqlite3 data/deep_research/paper_scout.sqlite3)
existing_paths=()

for state_path in "${state_paths[@]}"; do
  [[ -f "$state_path" ]] && existing_paths+=("$state_path")
done

if [[ ${#existing_paths[@]} -eq 0 ]]; then
  echo "::error::No Paper Scout state files were created; refusing to publish an empty durable snapshot."
  exit 1
fi

tar -czf "$archive_path" "${existing_paths[@]}"
if ! gh release view "$release_tag" --json id >/dev/null 2>&1; then
  gh release create "$release_tag" --title "Paper Scout runtime state" --prerelease --notes "Mutable runtime state for Paper Scout. Do not delete while scheduled workflows are active."
fi
gh release upload "$release_tag" "$archive_path#paper-scout-state.tar.gz" --clobber
echo "Published durable Paper Scout state release asset."
