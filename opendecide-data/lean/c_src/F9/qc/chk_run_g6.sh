#!/bin/bash
# check:F9 (c-lanes-v3): G6 on qc_sample (remote, rrun; CPU only). G15/G18, G12, G11 were run locally (each < 2 min).
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F9/qc
/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python chk_g6.py qc_sample > g6.log 2>&1
echo G6_DONE rc=$?
tail -n 3 g6.log | cut -c1-400
