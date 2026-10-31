#!/bin/bash
# check:F1 (c-lanes-v3): G6 on qc_sample, yes/no and choice parts in parallel, then merge
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1/qc
mkdir -p ../tmp/qc
python g6_r2.py qc_sample yn > ../tmp/qc/r2_g6_yn.log 2>&1 &
python g6_r2.py qc_sample ch > ../tmp/qc/r2_g6_ch.log 2>&1 &
wait
python g6_r2.py qc_sample merge > ../tmp/qc/r2_g6_merge.log 2>&1
echo G6_DONE
