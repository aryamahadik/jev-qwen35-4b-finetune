#!/bin/bash
# F12 G4 on the Mac (solver B needs jsonschema): one worker, nice 10. Training samplers on 1,000 rows of
# candidates_r1 + qc_sample (candidates alone hold < 1,000 per sampler), S5 on all 400 mixdev rows.
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F12
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
export PYTHONHASHSEED=0 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
rm -f tmp/G4_DONE
for smp in ${@:-S1 S2 S3 S4 S6}; do nice -n 10 $PY gen/f12g4.py candidates_r1+qc_sample $smp --rows 1000 > tmp/g4_$smp.out 2>&1; done
nice -n 10 $PY gen/f12g4.py mixdev_S5 S5 --rows 400 > tmp/g4_S5.out 2>&1
echo G4_DONE > tmp/G4_DONE
