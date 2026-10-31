#!/bin/bash
# v1.1 fix rebuild (raw/ was deleted after v1.0): from the kept tmp/records/ onward. Same steps as rebuild.sh after
# build_records; the deny-list check is re-run (its verdicts do not depend on the rows).
set -e
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
D=/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/public/public-3
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean
$PY c_src/common/denylist.py check --query $D/denylist/query_public3.json --out $D/denylist/verdicts_public3.json \
    --denylist $D/denylist/denylist_public3.json --run public3 --fail-on-taint > $D/logs/denylist_check.stdout 2>&1
$D/run_sealed_records.sh > $D/logs/run_sealed_records.log 2>&1
$PY $D/flag_sealed_records.py > $D/logs/flag_sealed_records.log 2>&1
$PY $D/build_rows.py > $D/logs/build_rows.log 2>&1
$PY $D/assemble.py stage > $D/logs/stage.log 2>&1
$D/run_sealed.sh > $D/logs/run_sealed.log 2>&1
$PY $D/assemble.py final > $D/logs/final.log 2>&1
for p in main reserve mtdev; do f=public3_rows_r1; [ $p = reserve ] && f=public3_reserve; [ $p = mtdev ] && f=public3_mtdev;
  $PY $D/selfcheck.py $D/out/$f.jsonl $D/logs/selfcheck_final_$p.json > /dev/null; done
$PY $D/manifest.py > $D/logs/manifest.stdout 2>&1
$D/run_sealed_final.sh > $D/logs/run_sealed_final.log 2>&1
$PY $D/manifest.py > $D/logs/manifest.stdout 2>&1
$PY $D/g15_check.py > $D/logs/g15_check.stdout 2>&1
echo "rebuild_from_records done"
