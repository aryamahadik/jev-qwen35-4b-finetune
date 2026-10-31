#!/bin/bash
# check:F9 (c-lanes-v3): G8v3 (A19/A19.1 adopted; shared tool c_src/common/g8_aflite.py) on candidates_r1 (remote, rrun)
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F9/qc
/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python chk_g8v3.py /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F9/out/candidates_r1.jsonl /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F9/qc/g8v3_candidates_r1.json 30 > g8v3.log 2>&1
echo G8V3_DONE rc=$?; tail -n 4 g8v3.log
