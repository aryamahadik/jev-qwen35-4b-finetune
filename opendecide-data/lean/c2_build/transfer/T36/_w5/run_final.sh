#!/bin/bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
W=transfer/T36/_w5
nice -n 10 $PY -B transfer/T36/run_pilot_i2.py > $W/pilot_run.out 2> $W/pilot_run.err
for H in 1 2; do PYTHONHASHSEED=$H nice -n 10 $PY -B transfer/T36/run_pilot_i2.py --dry-run > $W/det_$H.out 2> $W/det_$H.err; done
nice -n 10 $PY -B -m pytest -q -x transfer/T36/test_plugin.py transfer/T36/test_pilot_i1.py transfer/T36/test_g0_v2.py > $W/pytest.out 2>&1
echo done > $W/final_done
