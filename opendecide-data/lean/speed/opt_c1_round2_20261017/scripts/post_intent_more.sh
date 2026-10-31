#!/usr/bin/env bash
cd ~/opt_r2/voice; export HF_HUB_OFFLINE=1
while pgrep -f "scripts/post_asr.sh" >/dev/null; do sleep 15; done
OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 venv/bin/python -B scripts/c1_slurp.py --level intent --asr s560 --n ${NINT:-150} --threads 8 >> logs/c1_intent.log 2>&1; echo intent2 rc=$?
echo INTENT_MORE_DONE
