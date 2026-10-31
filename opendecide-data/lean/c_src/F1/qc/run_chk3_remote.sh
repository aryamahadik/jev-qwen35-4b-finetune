#!/bin/bash
# check:F1 (c-lanes-v3) round-3 check: G6 (qc_sample), G7 (both pools), G8 spec raw share, G8v3 (A19.1) on candidates
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1/qc
mkdir -p ../tmp/qc
export G8_TORCH_THREADS=4
( python ../../common/g8_aflite.py run --family F1 --pool /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1/out/candidates_r1.jsonl --out $PWD/g8v3_candidates_r1.json --jobs 10 > ../tmp/qc/c3_g8v3.log 2>&1; echo "g8v3 rc=$?" >> ../tmp/qc/c3_status.log ) &
( python g6_r2.py qc_sample yn > ../tmp/qc/c3_g6_yn.log 2>&1 & python g6_r2.py qc_sample ch > ../tmp/qc/c3_g6_ch.log 2>&1; wait; python g6_r2.py qc_sample merge > ../tmp/qc/c3_g6_merge.log 2>&1; echo "g6 rc=$?" >> ../tmp/qc/c3_status.log
  python g7.py qc_sample > ../tmp/qc/c3_g7qc.log 2>&1; python g7.py candidates_r1 > ../tmp/qc/c3_g7cand.log 2>&1; echo "g7 rc=$?" >> ../tmp/qc/c3_status.log
  python g8.py candidates_r1 > ../tmp/qc/c3_g8spec.log 2>&1; echo "g8spec rc=$?" >> ../tmp/qc/c3_status.log ) &
wait
echo CHK3_REMOTE_DONE
