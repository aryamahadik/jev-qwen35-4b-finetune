#!/bin/bash
# F9 gates on out/ (A20 a: run under c_build/rrun.py): G2+G3 re-run, G15, G4 per generator (>= 1,000 rows; S5 all 400)
cd "$(dirname "$0")"
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
LOG=../tmp/logs
mkdir -p $LOG ../out/qc
rm -f ../out/qc/g4_*.json
$PY f9qc.py g3 > $LOG/gate_g3.log 2>&1 &
$PY f9qc.py g15 > $LOG/gate_g15.log 2>&1 &
for s in S1 S2 S3 S4 S6; do $PY f9g4.py cand $s --rows 1000 > $LOG/gate_g4_$s.log 2>&1 & done
$PY f9g4.py dev S5 --rows 400 > $LOG/gate_g4_S5.log 2>&1 &
wait
echo done > $LOG/gates_finished.flag
