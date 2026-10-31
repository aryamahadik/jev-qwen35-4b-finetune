#!/bin/bash
# Independent QC (B4): RUN sealed_nd/qc/sealed_check.py (never opened) on public-2's current out files.
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean
PY=../.venv/bin/python
CK=sealed_nd/qc/sealed_check.py
D=c_src/public/public-2/out
Q=c_src/public/public-2/qc/sealedqc
for f in rows_r1 reserve_r1 dev_mt_r1; do
  $PY $CK $D/$f.jsonl --id-field id --out $Q/$f.sealedqc.jsonl --summary $Q/$f.summary.json --structure-fields state,card,instructions,options --workers 4
  echo "$f exit=$?"
done
for f in wordings cards styles table_hashes; do
  $PY $CK $D/$f.jsonl --id-field id --out $Q/$f.sealedqc.jsonl --summary $Q/$f.summary.json --workers 2
  echo "$f exit=$?"
done
echo DONE
