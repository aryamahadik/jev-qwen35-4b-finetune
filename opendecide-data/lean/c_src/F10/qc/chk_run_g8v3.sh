#!/bin/bash
# check:F10 (c-lanes-v3): G8v3 (A19/A19.1 adopted) shared tool via qc/chk_g8v3.py on the current candidates pool
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F10
/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python qc/chk_g8v3.py $PWD/out/candidates_r1.jsonl $PWD/qc/g8v3_candidates_r1.json 16 > qc/g8v3_remote.log 2>&1
echo G8V3_DONE rc=$?
tail -n 4 qc/g8v3_remote.log
