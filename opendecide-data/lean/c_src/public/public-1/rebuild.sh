#!/bin/bash
# public-1 v1.1 full rebuild (review-public-1 fixes). Needs raw/ (fetch.py --no-records --only squad2 quality musique
# 2wiki; sha256 pinned in logs/fetch_manifest.json) and tmp/tokenizer.json (Qwen3.5-4B snapshot 851bf6e8).
# Order: golden_train indexes -> 2Wiki slim -> dev phases of the three Wikipedia sets (each writes tmp/devx_<ds>.json)
# -> train phases (read every devx) + QuALITY -> stage -> sealed check -> final -> sealed check on out/ -> QC.
set -e
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/public/public-1
[ -f tmp/golden_index.npz ] || $PY build_golden_index.py > logs/golden_index.stdout 2>&1
[ -f tmp/golden_g10.npy ] || $PY build_golden_grams.py > logs/golden_g10.stdout 2>&1
[ -f tmp/2wiki_cmp_train.jsonl ] || $PY slim_2wiki.py > logs/slim_2wiki.stdout 2>&1
rm -f tmp/devx_*.json tmp/devrows_*.json tmp/cand_*.json
for d in squad2 musique 2wiki; do
  $PY build_$d.py --phase dev > logs/build_${d}_dev.log 2>&1; echo "$(date -u +%H:%M:%S) $d dev"
done
for d in squad2 musique 2wiki; do
  $PY build_$d.py --phase train > logs/build_$d.log 2>&1; echo "$(date -u +%H:%M:%S) $d train"
done
$PY build_quality.py --main 775 > logs/build_quality.log 2>&1; echo "$(date -u +%H:%M:%S) quality"
$PY assemble.py stage > logs/stage.log 2>&1; echo "$(date -u +%H:%M:%S) staged"
./run_sealed.sh; echo "$(date -u +%H:%M:%S) sealed staged"
$PY assemble.py final > logs/final.log 2>&1; echo "$(date -u +%H:%M:%S) final"
./run_sealed_final.sh; echo "$(date -u +%H:%M:%S) sealed final"
$PY qc_fix.py --out-dir out --cards logs/row_cards_final.json --gate --json logs/qc_fix.json > /dev/null 2> logs/qc_fix.err
echo "$(date -u +%H:%M:%S) qc"
