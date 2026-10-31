#!/bin/bash
# F13 full round-1 builds (run from c_src/F13 via c_build/rrun.py; W workers). Outputs in tmp/full/.
set -e
W=${F13_WORKERS:-32}
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
mkdir -p tmp/full
b() { $PY gen/f13_build.py --split "$1" --samplers "$2" --per_card "$3" --workers $W --out "tmp/full/$4.jsonl" --salt "$5" > "tmp/full/$4.log" 2>&1; tail -c 400 "tmp/full/$4.log"; echo; }
b cand S1 80 cand_S1 r1
b cand S2 85 cand_S2 r1
b cand S3 85 cand_S3 r1
b cand S4 110 cand_S4 r1
b cand S6 80 cand_S6 r1
b s5 S1 30 s5 r1
b qc S1 105 qc_S1 qc1
b qc S2 118 qc_S2 qc1
b qc S3 118 qc_S3 qc1
b qc S4 125 qc_S4 qc1
b qc S6 150 qc_S6 qc1
echo "[F13] $(date -u +%H:%M) full builds done (tmp/full)" >> /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_build/progress_phase2.log
