#!/bin/bash
# check:F1 (c-lanes-v3): G8v3 (A19.1 adopted) shared tool on the current candidates pool
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1
python ../common/g8_aflite.py run --family F1 --pool $PWD/out/candidates_r1.jsonl --out $PWD/qc/g8v3_candidates_r1.json --jobs 8 > qc/g8v3_run.log 2>&1
echo G8V3_DONE rc=$?
tail -n 3 qc/g8v3_run.log
