#!/bin/bash
# fix v1.1: run the id-only sealed checker (as a program; exports never read) on public-3's own parsed records
# (tmp/records/<scheme>.jsonl: the record text after redaction / placeholders + human annotation). Every blocking hit is
# flagged sealed_drop in tmp/records and in out/public3_split_3e.jsonl (fix_records.py), so no round-1 or round-2 row and
# no F10/F11 consumer of the split file can use it. Output: tmp/records_sealed/ (ids, hit kinds and counts only).
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
CHK=/Users/aryamahadik/Documents/jev/opendecide-data/lean/sealed_nd/qc/sealed_check.py
D=/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/public/public-3
mkdir -p $D/tmp/records_sealed
for s in ghc edos mams_acsa mams_atsa sarcasm_v2 xed; do
  $PY $CHK $D/tmp/records/$s.jsonl --id-field id --out $D/tmp/records_sealed/$s.sealedqc.jsonl \
     --summary $D/tmp/records_sealed/$s.summary.json \
     --skip-fields norm_sha256,loose_sha256,text_orig_norm_sha256,flags,file,part,dataset,scheme,record_id,eligible \
     --workers 4 > $D/tmp/records_sealed/$s.stdout 2>&1
  echo "$(date -u +%H:%M:%S) $s exit=$?"
done
echo "$(date -u +%H:%M:%S) all done"
