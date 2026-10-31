#!/usr/bin/env bash
# pull_results.sh <trial name> : copy ~/opt_r2/results/<name> (+ window log, server log tail) from od-l4b to ./results/<name>
set -e
N="$1"; D="$(cd "$(dirname "$0")" && pwd)"; mkdir -p "$D/results"
gcloud compute scp --recurse --tunnel-through-iap --zone us-east4-c --project system-one-509903 "od-l4b:/home/aryamahadik/opt_r2/results/$N" "$D/results/" 2>&1 | grep -v -e NumPy -e 'please see' -e '^$' || true
"$D/vm.sh" od-l4b "tail -n 400 ~/opt_r2/logs/window_$N.log" > "$D/results/$N/window.log" 2>&1 || true
"$D/vm.sh" od-l4b "grep -v -i 'warn' ~/opt_r2/logs/$N.server.log | tail -n 120" > "$D/results/$N/server_log_tail.txt" 2>&1 || true
ls -la "$D/results/$N"
