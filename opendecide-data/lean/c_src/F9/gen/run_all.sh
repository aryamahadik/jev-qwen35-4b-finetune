#!/bin/bash
# F9 round-1 full build (A20 a: run under c_build/rrun.py with F9_WORKERS=<cores>): base parts for cand / qc / dev,
# then top-up parts t1, t2 (per-sampler shortfall onto productive cards, 2.1 cap 128 rows per card), then merge.
cd "$(dirname "$0")"
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
LOG=../tmp/logs
mkdir -p $LOG
W=${F9_WORKERS:-2}
run_mode() {  # $1 mode, $2 optional top-up tag
  for ((i = 0; i < W; i++)); do
    if [ -n "$2" ]; then
      $PY f9build.py $1 --shard $i/$W --topup $2 > $LOG/build_$1_$2_$i.log 2>&1 &
    else
      $PY f9build.py $1 --shard $i/$W > $LOG/build_$1_$i.log 2>&1 &
    fi
  done
  wait
}
for mode in ${MODES:-cand qc dev}; do run_mode $mode; done
for tag in t1 t2; do
  for mode in ${MODES:-cand qc dev}; do run_mode $mode $tag; done
done
$PY f9qc.py merge > $LOG/merge.log 2>&1
echo done > $LOG/build_finished.flag
