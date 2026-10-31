#!/bin/bash
# ld_window.sh <label> [--no-trial] -- <command...>        (runs ON od-l4b; NOT run today; needs the orchestrator's window grant)
# One L-D window, same safety contract as the round-2 window.sh (speed/opt_c1_round2_20261017/vmcode):
#   1. wait while a C2 read job runs (prod_stop.sh exits 9; poll every 5 min, give up after WAIT_MAX_S, default 21600);
#   2. snapshot + stop the PRODUCTION server (prod_stop.sh: the same way start_server.sh stops it; nothing else is killed);
#   3. (unless --no-trial) boot a trial server on TRIAL_PORT (default 30010) with the production flags (trial_server.sh);
#   4. run <command> with LD_WINDOW=<label> and TRIAL_PORT exported, under `timeout WINDOW_MAX_S` (default 5400 = 90 min);
#   5. ALWAYS (trap): stop the trial server this script started, restart production (prod_start.sh) and log the downtime.
# Needs on the VM (round-2 files, still in ~/opt_r2 from 17 Oct): prod_stop.sh prod_start.sh trial_server.sh trial_stop.sh snapcmp.py.
# A window is one authorised GPU slot at queue priority 5: the orchestrator opens it only when no C2 job is queued, and C2
# (priority 1-2) may take the box back at the end of the slot. Never run two windows at once.
LBL="$1"; shift
NOTRIAL=0; [ "$1" = "--no-trial" ] && { NOTRIAL=1; shift; }
[ "$1" = "--" ] && shift
[ -n "$LBL" ] && [ $# -gt 0 ] || { echo "usage: ld_window.sh <label> [--no-trial] -- <command...>"; exit 2; }
PORT=${TRIAL_PORT:-30010}; [ "$PORT" = 30000 ] && { echo "refusing port 30000"; exit 2; }
W=~/opt_r2; LOG=$W/logs/ld_window_$LBL.log; mkdir -p $W/logs $W/pids $W/snap
exec > >(tee -a $LOG) 2>&1
echo "=== L-D window $LBL $(date -u +%FT%TZ) trial=$((1-NOTRIAL)) port=$PORT cmd=[$*]"
STOPPED=0; TRIAL=0
cleanup() {
  if [ "$TRIAL" = 1 ]; then $W/trial_stop.sh ld_$LBL; TRIAL=0; fi
  if [ "$STOPPED" = 1 ]; then
    if ! curl -s -m 5 -o /dev/null localhost:30000/health; then $W/prod_start.sh ld_$LBL; fi
    STOPPED=0
  fi
  echo "=== L-D window $LBL end $(date -u +%FT%TZ)"
}
trap cleanup EXIT
T0=$(date +%s)
while true; do
  $W/prod_stop.sh ld_$LBL; rc=$?
  if [ $rc -eq 9 ]; then
    [ $(( $(date +%s) - T0 )) -gt ${WAIT_MAX_S:-21600} ] && { echo "gave up waiting for C2 jobs"; exit 9; }
    echo "$(date -u +%T) C2 read job running: waiting 5 min"; sleep 300; continue
  fi
  [ $rc -eq 0 ] && STOPPED=1
  break
done
[ "$STOPPED" = 1 ] || { echo "could not stop production cleanly (rc=$rc); abort"; exit 5; }
if [ "$NOTRIAL" = 0 ]; then
  $W/trial_server.sh ld_$LBL $PORT || { echo "trial server failed to boot"; exit 6; }
  TRIAL=1
fi
export LD_WINDOW="$LBL" TRIAL_PORT="$PORT"
timeout ${WINDOW_MAX_S:-5400} bash -c "$*"; echo "command rc=$?"
