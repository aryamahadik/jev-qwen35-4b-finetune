#!/bin/bash
# regen_queue.sh : A49 (e) regenerate T33 T25 T15 T26 T32 through the fixed tool, new seed bases, 2 at a time (Mac, nice 10)
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
printf '%s\n' "T33 30000000 31000000 32000000" "T25 33000000 34000000 35000000" "T15 36000000 37000000 38000000" \
  "T26 39000000 40000000 41000000" "T32 42000000 43000000 44000000" | \
xargs -P 2 -L 1 bash -c 'f=$0; nice -n 10 '$PY' -B gen_full_c2.py $f --seed-bases $1 $2 $3 > zed_orch/a49/logs/regen_$f.log 2>&1; echo $? > zed_orch/a49/logs/regen_$f.rc'
