#!/bin/bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 PYTHONHASHSEED=0
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python; D=zed_orch/t01diag
nice -n 10 $PY -B $D/diag_fam.py --family T25 --variant runner --seed-base 2000000 --n 901 --g15 1 --out $D/run_T25_2000000.json >> $D/jobs2.log 2>&1
nice -n 10 $PY -B $D/diag_fam.py --family T25 --variant tool --seed-base 2000000 --n 901 --g15 1 --out $D/fix_T25_2000000.json >> $D/jobs2.log 2>&1
nice -n 10 $PY -B $D/diag_fam.py --family T15 --variant tool --seed-base 2000000 --n 1350 --g15 1 --out $D/fix_T15_2000000.json >> $D/jobs2.log 2>&1
nice -n 10 $PY -B $D/diag_fam.py --family T33 --variant tool --seed-base 2000000 --n 3601 --g15 1 --out $D/fix_T33_2000000.json >> $D/jobs2.log 2>&1
echo CHAIN2_DONE >> $D/jobs2.log
