#!/bin/bash
# check:F1 (c-lanes-v3) round-4 check, part A: G6 (qc_sample), G7 (both pools), G8 spec raw share (candidates)
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1/qc
mkdir -p ../tmp/qc
( python g6_r2.py qc_sample yn > ../tmp/qc/c5_g6_yn.log 2>&1 & python g6_r2.py qc_sample ch > ../tmp/qc/c5_g6_ch.log 2>&1; wait; python g6_r2.py qc_sample merge > ../tmp/qc/c5_g6_merge.log 2>&1; echo "g6 rc=$?" >> ../tmp/qc/c5a_status.log ) &
( python g7.py qc_sample > ../tmp/qc/c5_g7qc.log 2>&1; python g7.py candidates_r1 > ../tmp/qc/c5_g7cand.log 2>&1; echo "g7 rc=$?" >> ../tmp/qc/c5a_status.log ) &
( python g8.py candidates_r1 > ../tmp/qc/c5_g8spec.log 2>&1; echo "g8spec rc=$?" >> ../tmp/qc/c5a_status.log ) &
wait
echo CHK5A_REMOTE_DONE
