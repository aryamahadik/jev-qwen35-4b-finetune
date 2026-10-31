#!/bin/zsh
# F9 round-1 build. Local fallback (A20 a, RRUN_READY absent): 2 workers at nice 10. Under rrun: F9_WORKERS=<cores>.
# Resumable per card (out/parts/<mode>/<card>.done.json).
cd "$(dirname "$0")"
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
LOG=../tmp/logs
mkdir -p $LOG
W=${F9_WORKERS:-2}
for mode in ${@:-cand qc dev}; do
  for ((i = 0; i < W; i++)); do
    nice -n 10 $PY f9build.py $mode --shard $i/$W > $LOG/build_${mode}_$i.log 2>&1 &
  done
  wait
done
echo done > $LOG/build_finished.flag
