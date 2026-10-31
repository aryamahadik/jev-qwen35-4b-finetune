#!/bin/bash
# A30 (B1b): fetch a run from the profile's Volume (free), score it locally (gold never leaves the Mac), and write the
# AFTER ledger lines. Safe to re-run; refuses to score while the driver is still running.
#   bash think/b1b_fetch.sh mahadikarya3 b1b_YYYYMMDD_HHMMSS
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1         # lean/
PY=../.venv/bin/python; M=../.venv/bin/modal; SG=c_build/endgame/spend_guard.py
P=${1:?profile}; RUN=${2:?run}
D=think/runs/$RUN; T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
mkdir -p "$D"
MODAL_PROFILE=$P $M volume get opendecide "think_runs/$RUN" "$T" > /dev/null 2>&1 || { echo "FETCH_FAIL volume get"; exit 1; }
SRC=$(dirname "$(find "$T" -name driver.json | head -1)")
[ -n "$SRC" ] && [ -f "$SRC/driver.json" ] || { echo "NOT_READY no driver.json yet"; exit 1; }
cp "$SRC"/*.json "$D"/
$PY -c "import json, sys; sys.exit(0 if 'done_unix' in json.load(open('$D/driver.json')) else 1)" \
  || { echo "NOT_READY driver still running (partial files copied to $D)"; exit 1; }
$PY think/modal_think.py --b1b-score "$D" | head -30
$PY $SG ledger "$P" "B1b (A30) $RUN: AFTER (driver done; billing lags up to ~1 h, re-check with spend_guard.py bill)" \
  --payer credit > /dev/null
echo "| Phase B: B1b (A30) $RUN AFTER | $(date -u '+%d %b %H:%M') UTC, $P | see the AFTER billing line above (metered delta = actual) | credit |" >> logs/budget_ledger.md
echo "SCORED $D/summary_b1b.json"
