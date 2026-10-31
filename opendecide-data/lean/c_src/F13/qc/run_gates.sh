#!/bin/bash
# F13 gate re-runs on the emitted files (one platform: rrun). Sealed check runs on the Mac (f13_gates.py --only-sealed).
set -e
W=${F13_WORKERS:-32}
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
for n in candidates_r1 qc_sample mixdev_S5; do $PY qc/f13_gates.py $n --workers $W --skip-sealed | tail -c 600; echo; done
$PY qc/f13_g4.py candidates_r1 qc_sample --workers $W | tail -c 800
