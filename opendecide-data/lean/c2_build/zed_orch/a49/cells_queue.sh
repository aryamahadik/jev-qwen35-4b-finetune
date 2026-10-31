#!/bin/bash
# per-cell G10 for the 9 existing generations (Mac: needs torch for G15), 2 at a time
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
printf '%s\n' "T23 1200" "T01 2400" "T28 3600" "T24 900" "T31 1500" "T12 1200" "T07 1200" "T06 1350" "T30 2100" | \
xargs -P 2 -L 1 bash -c 'f=$0; nice -n 10 '$PY' -B gen_full_c2.py $f --ext-job --qc-big 0 --seed-bases 2000000 3000000 4000000 --n-cand $1 > zed_orch/a49/logs/cells_$f.log 2>&1; echo $? > zed_orch/a49/logs/cells_$f.rc'
