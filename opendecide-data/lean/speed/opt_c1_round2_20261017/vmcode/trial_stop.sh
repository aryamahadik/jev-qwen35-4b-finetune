#!/bin/bash
# trial_stop.sh <name> : stop ONLY the trial server this task started (pid recorded by trial_launch.py)
NAME="$1"; PF=~/opt_r2/pids/$NAME.pid
[ -f "$PF" ] || { echo "no pidfile for $NAME"; exit 1; }
PID=$(cat $PF)
if ps -p $PID >/dev/null 2>&1; then
  kill -TERM -- -$(ps -o pgid= -p $PID | tr -d ' ') 2>/dev/null
  for i in $(seq 1 60); do ps -p $PID >/dev/null 2>&1 || break; sleep 1; done
  ps -p $PID >/dev/null 2>&1 && kill -KILL -- -$(ps -o pgid= -p $PID | tr -d ' ') 2>/dev/null
fi
sleep 3
echo "stopped $NAME; gpu mem now: $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
rm -f $PF ~/opt_r2/pids/current_trial.pid
