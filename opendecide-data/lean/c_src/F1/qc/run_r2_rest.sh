#!/bin/bash
# check:F1 (c-lanes-v3): G7, G8 (spec + null + shared A19 tool), G10, G11, G12, G15/G18 on the current pools
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1/qc
mkdir -p ../tmp/qc
O=/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1/out
export G8_TORCH_THREADS=6
( python g8.py candidates_r1 > ../tmp/qc/r2_g8.log 2>&1; python g8_null.py > ../tmp/qc/r2_g8null.log 2>&1; python g11.py > ../tmp/qc/r2_g11.log 2>&1 ) &
( python ../../common/g8_aflite.py run --family F1 --pool $O/candidates_r1.jsonl --out $PWD/g8v2_candidates_r1.json --jobs 6 > ../tmp/qc/r2_g8v2.log 2>&1 ) &
( python g7.py qc_sample > ../tmp/qc/r2_g7qc.log 2>&1; python g7.py candidates_r1 > ../tmp/qc/r2_g7cand.log 2>&1 ) &
( python g10.py candidates_r1 > ../tmp/qc/r2_g10cand.log 2>&1; python g10.py qc_sample > ../tmp/qc/r2_g10qc.log 2>&1; python g12.py > ../tmp/qc/r2_g12.log 2>&1; python g15_g18.py > ../tmp/qc/r2_g15.log 2>&1 ) &
wait
echo REST_DONE
