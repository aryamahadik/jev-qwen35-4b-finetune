#!/bin/bash
# window.sh <trial-name> <backend> <phases> [-- extra sglang args]
#   env: TRIAL_MODEL TRIAL_ENV TRIAL_PYPATH PRE_CMD POST_CMD PARITY_CONC TRIAL_PORT
# One trial window: C2 safety check (wait, poll every 5 min) -> stop production -> trial server on 30010 -> r2_trial
# -> stop trial -> restart production exactly as start_server.sh + verify server_info equality + log downtime.
# Production is always restored (trap), and only a server this script started is ever stopped besides production itself.
NAME="$1"; BACKEND="$2"; PHASES="$3"; shift 3; [ "$1" = "--" ] && shift
PORT=${TRIAL_PORT:-30010}
W=~/opt_r2; LOG=$W/logs/window_$NAME.log
exec > >(tee -a $LOG) 2>&1
echo "=== window $NAME $(date -u +%FT%TZ) backend=$BACKEND phases=$PHASES extra=[$*]"
STOPPED=0
cleanup() {
  if [ -f $W/pids/$NAME.pid ] && ps -p $(cat $W/pids/$NAME.pid) >/dev/null 2>&1; then $W/trial_stop.sh $NAME; fi
  if [ "$STOPPED" = 1 ]; then
    if ! curl -s -m 5 -o /dev/null localhost:30000/health; then $W/prod_start.sh $NAME; fi
    STOPPED=0
  fi
  echo "=== window $NAME end $(date -u +%FT%TZ)"
}
trap cleanup EXIT
while true; do
  $W/prod_stop.sh $NAME; rc=$?
  if [ $rc -eq 9 ]; then echo "$(date -u +%T) C2 read job running: waiting 5 min"; sleep 300; continue; fi
  [ $rc -eq 0 ] && STOPPED=1
  break
done
[ "$STOPPED" = 1 ] || { echo "could not stop production cleanly (rc=$rc); abort"; exit 5; }
$W/trial_server.sh $NAME $PORT "$@" || { echo "trial server failed to boot"; exit 6; }
if [ -n "$PRE_CMD" ]; then eval "$PRE_CMD"; fi
if [ -n "$MAIN_CMD" ]; then eval "$MAIN_CMD" || echo "main cmd rc=$?"
else ~/od/bin/python -B $W/r2_trial.py --name $NAME --port $PORT --backend $BACKEND --phases $PHASES --parity-conc ${PARITY_CONC:-16} $R2_EXTRA || echo "r2_trial rc=$?"; fi
if [ -n "$POST_CMD" ]; then eval "$POST_CMD"; fi
$W/trial_stop.sh $NAME
$W/prod_start.sh $NAME; STOPPED=0
