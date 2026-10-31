#!/bin/bash
# check:F9 (c-lanes-v3): G8v3 (A19/A19.1 adopted; shared tool) on candidates + G6 on qc_sample (G7 runs locally, < 2 min)
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F9/qc
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
$PY chk_g6.py qc_sample > g6.log 2>&1 &
P6=$!
$PY chk_g8v3.py /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F9/out/candidates_r1.jsonl /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F9/qc/g8v3_candidates_r1.json 14 > g8v3.log 2>&1
echo G8V3_DONE rc=$?
wait $P6; echo G6_DONE rc=$?
tail -n 3 g8v3.log; tail -n 2 g6.log
