#!/bin/bash
# Run the id-only sealed checker (as a program; never read its exports) on every staged public-3 output.
set -e
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
CHK=/Users/aryamahadik/Documents/jev/opendecide-data/lean/sealed_nd/qc/sealed_check.py
D=/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/public/public-3
for p in templates dev reserve main; do
  $PY $CHK $D/tmp/stage_$p.jsonl --id-field id --out $D/tmp/stage_$p.sealedqc.jsonl --summary $D/tmp/stage_$p.sealedqc.summary.json \
     --structure-fields state,card,instructions,options --workers 4 > $D/logs/sealed_$p.stdout 2>&1
  echo "$(date -u +%H:%M:%S) done $p"
done
