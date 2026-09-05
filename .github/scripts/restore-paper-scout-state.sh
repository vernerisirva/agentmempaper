#!/usr/bin/env bash
# Restore a missing durable snapshot from the final Git-tracked state during
# migration. The named seed also survives an intervening normal commit before
# the first durable state release has been uploaded.
set -euo pipefail

state_paths=(
  "data/paper_scout.sqlite3"
  "data/deep_research/paper_scout.sqlite3"
  "data/engram/paper_scout.sqlite3"
)

seed_ref="${PAPER_SCOUT_STATE_SEED_REF:-HEAD^}"
# A verified durable snapshot needs no migration fetch. Engram may be the only
# newly introduced track; it has no historical Git database to recover.
if [[ -f "${state_paths[0]}" && -f "${state_paths[1]}" ]]; then
  echo "Existing tracks restored; any new Engram state initializes on first use."
  exit 0
fi
if ! git cat-file -e "$seed_ref^{commit}" 2>/dev/null; then
  git fetch --no-tags --depth=1 origin "$seed_ref"
  seed_ref="FETCH_HEAD"
fi

for state_path in "${state_paths[@]}"; do
  if [[ -f "$state_path" ]]; then
    echo "Using restored Paper Scout state: $state_path"
  elif git cat-file -e "$seed_ref:$state_path" 2>/dev/null; then
    mkdir -p "$(dirname "$state_path")"
    git show "$seed_ref:$state_path" > "$state_path"
    echo "::warning::Bootstrapped Paper Scout state from migration seed $seed_ref: $state_path"
  else
    if [[ "$state_path" == "data/engram/paper_scout.sqlite3" ]]; then
      echo "New Engram track; Paper Scout will initialize it on first use."
    else
      echo "::error::Existing track state is unavailable: $state_path; refusing to reset it."
      exit 1
    fi
  fi
done
