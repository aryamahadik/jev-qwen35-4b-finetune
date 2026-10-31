#!/bin/bash
# F12 round-1 build (remote via rrun or local): shards in parallel, then merge.
set -e
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F12
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
export PYTHONHASHSEED=0 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
J=${J:-16}
rm -rf out/parts && mkdir -p out/parts tmp
: > tmp/build.log
{ for i in $(seq 0 $((J-1))); do echo "cand $i/$J"; echo "qc $i/$J"; done; for i in 0 1 2 3 4 5; do echo "dev $i/6"; done; } \
  | xargs -P $J -L 1 sh -c '$0 gen/f12build.py $1 --shard $2' $PY
ls out/parts/*.done | wc -l
$PY gen/f12qc.py merge
# gates (G2/G3 solver B needs jsonschema, absent from the rrun image) run on the Mac: gen/run_gates_local.sh
echo BUILD_DONE
