#!/bin/bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
for B in 900000 7000000; do
  nice -n 10 $PY -B transfer/T36/g6_seedbase.py --seed-base $B --n 6000 --out transfer/T36/_w5/g6/g6_${B}_$1.json > transfer/T36/_w5/g6/g6_${B}_$1.log 2>&1
done
echo done > transfer/T36/_w5/g6/done_$1
