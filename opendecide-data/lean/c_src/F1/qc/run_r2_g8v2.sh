#!/bin/bash
# check:F1 (c-lanes-v3): shared G8v2 tool (A19, report-only until A19_ADOPTED) on the current candidates pool
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1
mkdir -p tmp/qc
python ../common/g8_aflite.py run --family F1 --pool $PWD/out/candidates_r1.jsonl --out $PWD/qc/g8v2_candidates_r1.json --jobs 14 > tmp/qc/r2_g8v2.log 2>&1
echo G8V2_DONE rc=$?
