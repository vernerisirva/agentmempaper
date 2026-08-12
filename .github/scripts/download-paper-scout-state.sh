#!/usr/bin/env bash
# Restore the latest durable runtime snapshot. A missing release is expected
# only before the migration's first successful state publication.
set -euo pipefail

release_tag="paper-scout-runtime-state"
archive_path="${RUNNER_TEMP:?RUNNER_TEMP is required}/paper-scout-state.tar.gz"
error_path="${RUNNER_TEMP}/paper-scout-release-view.err"

if gh release view "$release_tag" --json id >/dev/null 2>"$error_path"; then
  gh release download "$release_tag" --pattern "paper-scout-state.tar.gz" --dir "$RUNNER_TEMP"
  tar -xzf "$archive_path"
  echo "Restored Paper Scout state from durable GitHub Release asset."
elif grep -qiE '(not found|http 404)' "$error_path"; then
  echo "No durable Paper Scout state release exists yet; migration bootstrap may seed state."
else
  cat "$error_path" >&2
  echo "::error::Unable to determine whether the durable Paper Scout state release exists."
  exit 1
fi
