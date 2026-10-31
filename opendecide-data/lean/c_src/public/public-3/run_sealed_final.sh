#!/bin/bash
# Re-run the id-only sealed checker on every FINAL public-3 output (rows, templates, split file, claims, allocation,
# G5 ids, manifest); --fail-on-hit. JSON documents are wrapped one per line as {"id": name, "doc": ...} in tmp/.
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
CHK=/Users/aryamahadik/Documents/jev/opendecide-data/lean/sealed_nd/qc/sealed_check.py
D=/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/public/public-3
mkdir -p $D/logs/sealed_final $D/tmp/sealed_wrap
for j in public3_class_allocation public3_g5_sample_ids; do
  $PY -c "import json,sys; d=json.load(open('$D/out/$j.json')); open('$D/tmp/sealed_wrap/$j.jsonl','w').write(json.dumps({'id':'$j','doc':d})+'\n')"
done
$PY -c "import json,sys; d=json.load(open('$D/manifest_public3.json')); open('$D/tmp/sealed_wrap/manifest_public3.jsonl','w').write(json.dumps({'id':'manifest_public3','doc':d})+'\n')"
for f in $D/out/public3_templates.jsonl $D/out/public3_mtdev.jsonl $D/out/public3_reserve.jsonl $D/out/public3_rows_r1.jsonl \
         $D/out/public3_split_3e.jsonl $D/out/public3_record_claims.jsonl \
         $D/tmp/sealed_wrap/public3_class_allocation.jsonl $D/tmp/sealed_wrap/public3_g5_sample_ids.jsonl \
         $D/tmp/sealed_wrap/manifest_public3.jsonl; do
  b=$(basename $f .jsonl)
  extra=""
  case $b in public3_rows_r1|public3_reserve|public3_mtdev|public3_templates) extra="--structure-fields state,card,instructions,options";; esac
  $PY $CHK $f --id-field id --out $D/logs/sealed_final/$b.sealedqc.jsonl --summary $D/logs/sealed_final/$b.summary.json \
     $extra --workers 4 --fail-on-hit > $D/logs/sealed_final/$b.stdout 2>&1 \
     && echo "$(date -u +%H:%M:%S) $b exit=0" || echo "$(date -u +%H:%M:%S) $b exit=$?"
done
