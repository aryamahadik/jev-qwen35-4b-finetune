#!/bin/bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 PYTHONHASHSEED=0
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
D=zed_orch/t01diag
run_one() { line="$1"; args=$(echo "$line" | sed "s# --out # --out $D/#"); nice -n 10 $PY -B $D/diag_fam.py $args >> $D/jobs.log 2>&1; }
export -f run_one; export PY D
rm -f $D/jobs.log
cat $D/jobs.txt | xargs -P ${1:-2} -I{} bash -c 'run_one "{}"'
echo JOBS_DONE >> $D/jobs.log
