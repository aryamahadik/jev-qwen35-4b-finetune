#!/bin/bash
# A30 (B1b): ONE guarded, detached launch of session B1b on FREE credit. Run from anywhere:
#   bash think/b1b_launch.sh mahadikarya3          (fallback: mahadikarya44; any other profile is REFUSED)
# Order: profile check -> phase-B cumulative cap ($30) -> inputs + CPU estimate vs the per-launch cap -> spend_guard
# check (credit pays cap + $2 reserve, no unexplained app) -> ledger BEFORE + Phase-B line -> launch log -> detached
# `modal run ...::b1b`. The time cap is enforced ON THE SERVER: a CPU driver runs the H100 containers one after
# another under one absolute deadline (launch + CAP_MIN); each container's timeout = min(30 min, time left).
# Prints exactly one last line: LAUNCHED ... or REFUSED ...   Results: bash think/b1b_fetch.sh <profile> <run>
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1         # lean/
PY=../.venv/bin/python; M=../.venv/bin/modal; SG=c_build/endgame/spend_guard.py
P=${1:-}; CAP_MIN=${CAP_MIN:-90}; CAP_USD=${CAP_USD:-8}; PHASEB_CAP=30; B1A_ACTUAL=5.57
refuse() { echo "REFUSED $*"; exit 1; }
case "$P" in
  mahadikarya3|mahadikarya44) ;;
  *) refuse "profile '$P': B1b runs on free credit only (mahadikarya3, else mahadikarya44); never aryamhd / jaypatil-duke";;
esac
mkdir -p think/logs
# 0. owner decision 6 Oct ~20:50 UTC ("Data first, Phase B later", PREREG after A28): no Phase-B launch before the
#    weekly usage reset, Mon 12 Oct 2026 07:00 UTC
[ "$(date -u +%s)" -ge "$(date -u -j -f '%Y-%m-%dT%H:%M:%S' '2026-10-12T07:00:00' +%s 2>/dev/null || echo 1791788400)" ] \
  || refuse "Phase B is paused until Mon 12 Oct 2026 07:00 UTC (owner decision 6 Oct, 'Data first, Phase B later')"
# 0b. A17-B1 / A30 correction: the counts-only overlap vs the A16(a) list (OHS-3, sealed exports, DI test items,
#     JevBench) + ejs-5 must have run (orchestrator) with zero hits in the frozen 500
$PY -c "import json, sys; sys.exit(0 if json.load(open('think/data/clean_b1b/overlap_a16a.json')).get('b1b_math500_hits') == 0 else 1)" 2>/dev/null \
  || refuse "A16(a) overlap check missing or has hits (think/data/clean_b1b/overlap_a16a.json, PREREG A30 correction)"
# 1. phase-B cumulative cap (A17-B1): B1a actual + the cap of every Phase-B launch line already in the ledger + this cap
COMMIT=$($PY -c "
import re; t = open('logs/budget_ledger.md').read()
print(round($B1A_ACTUAL + sum(float(x) for x in re.findall(r'phaseB_cap_usd=([0-9.]+)', t)) + $CAP_USD, 2))") \
  || refuse "cannot read logs/budget_ledger.md"
$PY -c "import sys; sys.exit(0 if $COMMIT <= $PHASEB_CAP else 1)" \
  || refuse "phase-B cap: committed \$$COMMIT (incl. this launch's \$$CAP_USD) > \$$PHASEB_CAP"
# 2. frozen inputs + CPU estimate against the per-launch cap (no Modal call)
$PY think/modal_think.py --b1b-estimate --cap-min "$CAP_MIN" --max-usd "$CAP_USD" > think/logs/b1b_estimate.json 2>&1 \
  || refuse "estimate above the per-launch cap \$$CAP_USD (think/logs/b1b_estimate.json)"
$PY -c "import sys; sys.path.insert(0, 'think'); import modal_think as m; m._check_b1b_inputs()" > /dev/null 2>&1 \
  || refuse "B1b inputs differ from the frozen manifest (think/data/b1b_math500_manifest.json)"
EXP=$($PY -c "import json; print(json.load(open('think/logs/b1b_estimate.json'))['estimate']['usd_expected'])")
# 3. free credit can pay the cap + $2 reserve, and nothing unexplained runs on the profile
$PY $SG check "$P" --cap-usd "$CAP_USD" --reserve 2 > think/logs/b1b_guard.log 2>&1 \
  || refuse "spend_guard on $P: $(tail -1 think/logs/b1b_guard.log | cut -c1-200)"
MODAL_PROFILE=$P $M secret list 2>/dev/null | grep -q "opendecide-keys" || refuse "secret opendecide-keys missing on $P"
RUN=b1b_$(date -u +%Y%m%d_%H%M%S)
# 4. ledger BEFORE (billing numbers now) + the Phase-B line + the launch log (window = cap + image build / boot)
$PY $SG ledger "$P" "B1b (A30) $RUN: BEFORE launch (H100 x1 sequential, server-side cap $CAP_MIN min, <= \$$CAP_USD)" \
  --payer credit > /dev/null || refuse "ledger write failed"
echo "| Phase B: B1b (A30) $RUN | $(date -u '+%d %b %H:%M') UTC, $P, H100 one at a time, deadline $CAP_MIN min | expected ~\$$EXP, cap \$$CAP_USD (phaseB_cap_usd=$CAP_USD); phase-B committed \$$COMMIT of \$$PHASEB_CAP | credit |" >> logs/budget_ledger.md
$PY $SG record "$P" "$RUN" $((CAP_MIN + 20)) 1 || refuse "launch log write failed"
# 5. detached launch
MODAL_PROFILE=$P nohup $M run --detach think/modal_think.py::b1b --cap-min "$CAP_MIN" --run "$RUN" --max-usd "$CAP_USD" \
  > "think/logs/$RUN.log" 2>&1 &
for _ in $(seq 1 36); do  # up to 3 min for the app to exist (the first launch on a profile also builds the image)
  sleep 5
  if grep -q "REFUSED\|Traceback\|Error:" "think/logs/$RUN.log"; then
    refuse "launch failed: $(grep -m1 'REFUSED\|Traceback\|Error:' "think/logs/$RUN.log" | cut -c1-160) (think/logs/$RUN.log)"
  fi
  if grep -q '"launch"\|ap-[A-Za-z0-9]\{10,\}' "think/logs/$RUN.log"; then
    echo "fetch when done (~$((CAP_MIN)) min max): bash think/b1b_fetch.sh $P $RUN"
    echo "LAUNCHED B1b $RUN on $P (server-side cap $CAP_MIN min, <= \$$CAP_USD; expected ~\$$EXP; log think/logs/$RUN.log)"
    exit 0
  fi
done
refuse "no app within 3 min (think/logs/$RUN.log); check 'MODAL_PROFILE=$P modal app list' before any relaunch"
