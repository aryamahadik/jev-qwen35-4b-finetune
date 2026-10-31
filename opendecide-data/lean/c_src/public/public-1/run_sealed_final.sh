#!/bin/bash
# Re-run the id-only sealed checker on the FINAL out/ files (confirms 0 hits after drops / refills / option order).
set -e
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
CHK=/Users/aryamahadik/Documents/jev/opendecide-data/lean/sealed_nd/qc/sealed_check.py
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/public/public-1
for f in public1_templates public1_mtdev public1_reserve public1_rows_r1; do
  $PY $CHK out/$f.jsonl --id-field id --out logs/sealed_final/$f.sealedqc.jsonl --summary logs/sealed_final/$f.summary.json \
     --structure-fields state,card,instructions,options --workers 4 --fail-on-hit > logs/sealed_final/$f.stdout 2>&1 \
     && echo "$(date -u +%H:%M:%S) $f exit=0" || echo "$(date -u +%H:%M:%S) $f exit=$?"
done
