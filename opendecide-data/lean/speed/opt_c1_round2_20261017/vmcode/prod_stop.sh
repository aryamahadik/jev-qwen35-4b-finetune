#!/bin/bash
# prod_stop.sh <window label> : C2 safety check, snapshot, then stop the PRODUCTION server (the same way start_server.sh does:
# fast_read.py stop = kill the process group recorded in ~/jobs/sglang.pid). Exit 9 = a C2 read job is running: NOT stopped.
LBL="${1:-window}"
LOG=~/opt_r2/PROD_DOWNTIME.log
if pgrep -f '[c]rowd_driver|[f]ast_read\.py (label|predict|parity)|[r]eplay_c2|[r]eplay' >/dev/null; then
  echo "C2_JOB_RUNNING:"; pgrep -af '[c]rowd_driver|[f]ast_read\.py (label|predict|parity)|[r]eplay_c2|[r]eplay' | cut -c1-160
  exit 9
fi
curl -s -m 30 localhost:30000/server_info > ~/opt_r2/snap/prod_pre_$LBL.json || { echo "no prod server_info"; exit 8; }
curl -s -m 5 -o /dev/null -w "pre-health=%{http_code}\n" localhost:30000/health
echo "STOP  $(date -u +%FT%TZ) $LBL" | tee -a $LOG
date +%s > ~/opt_r2/snap/prod_stop_ts
~/od/bin/python -B ~/reads/fast_read.py stop
for i in $(seq 1 40); do
  m=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | tr -d ' ')
  [ "$m" -lt 1500 ] && break; sleep 2
done
echo "gpu mem used after stop: ${m} MiB"
