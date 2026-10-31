#!/bin/bash
# prod_start.sh <window label> : restart the production server exactly as ~/reads/start_server.sh with the recorded args
# (GCP_RUNBOOK / crowd_driver.sh), verify /health and that server_info equals the pre-window snapshot, log the downtime.
LBL="${1:-window}"
LOG=~/opt_r2/PROD_DOWNTIME.log
# never start production while a trial server of this task still holds the GPU
if [ -f ~/opt_r2/pids/current_trial.pid ] && ps -p $(cat ~/opt_r2/pids/current_trial.pid) >/dev/null 2>&1; then
  echo "trial server still running: stop it first (trial_stop.sh)"; exit 7
fi
~/reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8 --extra-args "--attention-backend triton" >> ~/jobs/serve_cmd.log 2>&1
rc=$?
for i in $(seq 1 120); do
  curl -s -m 5 -o /dev/null localhost:30000/health && break; sleep 3
done
H=$(curl -s -m 5 -o /dev/null -w "%{http_code}" localhost:30000/health)
curl -s -m 30 localhost:30000/server_info > ~/opt_r2/snap/prod_post_$LBL.json
T1=$(date +%s); T0=$(cat ~/opt_r2/snap/prod_stop_ts 2>/dev/null || echo $T1)
echo "START $(date -u +%FT%TZ) $LBL rc=$rc health=$H downtime_s=$((T1-T0))" | tee -a $LOG
python3 ~/opt_r2/snapcmp.py ~/opt_r2/snap/prod_pre_$LBL.json ~/opt_r2/snap/prod_post_$LBL.json | tee -a $LOG
