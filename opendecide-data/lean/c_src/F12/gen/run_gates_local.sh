#!/bin/bash
# F12 gates on the Mac (the rrun image has no jsonschema, which solver B needs): <= 2 workers, nice 10.
# G4: training samplers on 1,000 rows of candidates_r1 + qc_sample; S5 on all 400 mixdev rows.
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F12
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
export PYTHONHASHSEED=0 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
rm -f tmp/GATES_DONE out/qc/g4_*.json
G4="gen/f12g4.py candidates_r1+qc_sample"
( nice -n 10 $PY gen/f12qc.py g3 > tmp/g3.out 2>&1; nice -n 10 $PY gen/f12qc.py quota > tmp/quota.out 2>&1;
  for smp in S1 S2 S3; do nice -n 10 $PY $G4 $smp --rows 1000 > tmp/g4_$smp.out 2>&1; done ) &
( nice -n 10 $PY gen/f12qc.py g15 > tmp/g15.out 2>&1;
  for smp in S4 S6; do nice -n 10 $PY $G4 $smp --rows 1000 > tmp/g4_$smp.out 2>&1; done;
  nice -n 10 $PY gen/f12g4.py mixdev_S5 S5 --rows 400 > tmp/g4_S5.out 2>&1 ) &
wait
echo GATES_DONE > tmp/GATES_DONE
