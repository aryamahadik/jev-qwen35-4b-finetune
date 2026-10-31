#!/bin/bash
# Independent re-run (QC agent prep5) of the id-only sealed checker on the current out/ files.
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
CHK=/Users/aryamahadik/Documents/jev/opendecide-data/lean/sealed_nd/qc/sealed_check.py
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/public/public-1
for f in public1_rows_r1 public1_reserve public1_mtdev public1_templates; do
  $PY $CHK out/$f.jsonl --id-field id --out qc/sealedqc/$f.sealedqc.jsonl --summary qc/sealedqc/$f.summary.json \
     --structure-fields state,card,instructions,options --workers 4 --fail-on-hit > qc/sealedqc/$f.stdout 2>&1
  echo "$f exit=$?"
done
