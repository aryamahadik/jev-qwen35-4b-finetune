#!/bin/bash
# check:F13 (c-lanes-v3): G6 (qc_sample), G8v3 (candidates_r1; A19.1 adopted), G7 / G10 / G11 / G12 / G15+G18 on the
# pools (remote, rrun; one platform for every checker gate re-run).
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F13/qc
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
$PY chk_g6.py qc_sample > chk_g6.log 2>&1 &
P6=$!
( for n in candidates_r1 qc_sample mixdev_S5; do $PY chk_g15_g18.py $n; done ) > chk_g15.log 2>&1 &
P15=$!
( for n in candidates_r1 qc_sample; do $PY chk_g7.py $n; $PY chk_g12.py $n; $PY chk_g10.py $n; done; $PY chk_g11.py qc_sample; $PY chk_g11.py mixdev_S5 ) > chk_misc.log 2>&1 &
PM=$!
$PY chk_g8v3.py /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F13/out/candidates_r1.jsonl /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F13/qc/g8v3_candidates_r1.json 32 > chk_g8v3.log 2>&1
echo G8V3_DONE rc=$?
wait $PM; echo MISC_DONE rc=$?
wait $P15; echo G15_DONE rc=$?
wait $P6; echo G6_DONE rc=$?
tail -n 3 chk_g8v3.log; tail -n 2 chk_g6.log; tail -n 8 chk_misc.log | cut -c1-300; tail -n 3 chk_g15.log | cut -c1-300
