#!/bin/bash
# Run the id-only sealed checker (as a program; never read its exports) on every staged public-1 output.
set -e
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
CHK=/Users/aryamahadik/Documents/jev/opendecide-data/lean/sealed_nd/qc/sealed_check.py
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/public/public-1
for p in templates dev reserve main; do
  $PY $CHK tmp/stage_$p.jsonl --id-field id --out tmp/stage_$p.sealedqc.jsonl --summary tmp/stage_$p.sealedqc.summary.json \
     --structure-fields state,card,instructions,options --workers 4 > logs/sealed_$p.stdout 2>&1
  echo "$(date -u +%H:%M:%S) done $p"
done
