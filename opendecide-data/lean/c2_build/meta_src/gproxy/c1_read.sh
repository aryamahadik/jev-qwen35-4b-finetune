#!/bin/bash
# C1 read of the G-proxy through the fast path (A49 f; SGLang S1 on the free L4 od-l4b; A18.2 readout, choice rows 2 views, yes/no 1 read).
# Refuses to start unless data/c2_gproxy/GPROXY_HASH.json exists and every sha256 in it still matches (12.2: the hash comes first).
# It never starts, stops or restarts the VM or the server. One bulk read at a time: `push` and `read` refuse if a fast_read predict/label runs.
# Usage, from lean/c2_build:  meta_src/gproxy/c1_read.sh push | read | status | pull | all
#   push    verify hashes, check the server and that no bulk read runs, scp pab_gproxy.jsonl -> ~/lean/data/, sha256 -c on the VM
#   read    detached: fast_read.py predict --name q35_4b_main500k --splits pab_gproxy --tag _pab  (log ~/jobs/gproxy_c1read.log)
#   status  log tail + health
#   pull    preds_pab_gproxy/q35_4b_main500k_pab.{jsonl,meta.json} -> data/c2_gproxy/c1_read/preds_pab_gproxy/, then c1_score.py
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); BUILD=$(cd "$HERE/../.." && pwd); LEAN=$(cd "$BUILD/.." && pwd)
PY=$LEAN/../.venv/bin/python; D=$LEAN/data/c2_gproxy; VM=$BUILD/reads/vm_scripts/vm.sh
N=q35_4b_main500k; TAG=_pab; SPLIT=pab_gproxy; OUT=$D/c1_read/preds_$SPLIT
guard() { case "$(echo "$1" | tr 'A-Z' 'a-z')" in *ohs*|*sealed*|*preread*|*quarantine*|*longbench_v2*) echo "REFUSED path $1"; exit 2;; esac; }
guard "$D"
busy() { "$VM" ssh 'ps -eo cmd | grep -E "[f]ast_read.py (predict|label|parity)" | cut -c1-120'; }
health() { "$VM" ssh 'curl -s -m 8 localhost:30000/health_generate -o /dev/null -w "%{http_code}"'; }
verify() { (cd "$BUILD" && "$PY" -B meta_src/gproxy/finalize.py verify) || { echo "hash check failed: no read"; exit 2; }; }
do_push() {
  verify
  [ "$(health | tail -1)" = "200" ] || { echo "server not healthy (not restarting it here)"; exit 3; }
  b=$(busy); [ -z "$b" ] || { echo "a bulk read is running: $b"; exit 4; }
  "$VM" scp "$D/pab_gproxy.jsonl" "$D/pab_gproxy.jsonl.sha256" od-l4b:~/lean/data/
  "$VM" ssh 'cd ~/lean/data && sha256sum -c pab_gproxy.jsonl.sha256 && wc -l pab_gproxy.jsonl'
}
do_read() {
  verify
  b=$(busy); [ -z "$b" ] || { echo "a bulk read is running: $b"; exit 4; }
  "$VM" ssh "cd ~/reads && (setsid nohup bash -c 'export CUDA_HOME=\$HOME/sgl/lib/python3.12/site-packages/nvidia/cu13; export PATH=\$HOME/bin:\$HOME/sgl/bin:\$CUDA_HOME/bin:\$PATH; echo START \$(date -u +%T); ~/od/bin/python -B fast_read.py predict --name $N --splits $SPLIT --tag $TAG --workers 12 --chunk 8; echo rc=\$?; echo END \$(date -u +%T)' > ~/jobs/gproxy_c1read.log 2>&1 < /dev/null &) ; sleep 2; head -3 ~/jobs/gproxy_c1read.log"
}
case "${1:-}" in
  push) do_push ;;
  read) do_read ;;
  all) do_push && do_read ;;
  status)
    "$VM" ssh 'tail -c 600 ~/jobs/gproxy_c1read.log; echo; nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader'; health ;;
  pull)
    verify
    mkdir -p "$OUT"
    "$VM" scp "od-l4b:~/lean/preds_$SPLIT/$N$TAG.jsonl" "od-l4b:~/lean/preds_$SPLIT/$N$TAG.meta.json" "$OUT/"
    (cd "$BUILD" && "$PY" -B meta_src/gproxy/c1_score.py) ;;
  *) echo "usage: $0 push|read|status|pull|all"; exit 1 ;;
esac
