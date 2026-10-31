#!/bin/bash
# check:F1 (c-lanes-v3) round-4 check, part B: G8v3 (A19.1 adopted) on candidates_r1
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1/qc
mkdir -p ../tmp/qc
export G8_TORCH_THREADS=2
python ../../common/g8_aflite.py run --family F1 --pool /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1/out/candidates_r1.jsonl --out $PWD/g8v3_candidates_r1.json --jobs 8 > ../tmp/qc/c5_g8v3.log 2>&1; echo "g8v3 rc=$?" >> ../tmp/qc/c5b_status.log
echo CHK5B_REMOTE_DONE
