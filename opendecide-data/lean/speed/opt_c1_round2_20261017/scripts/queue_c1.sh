#!/usr/bin/env bash
# waits for the SLURP s560 transcripts, then C1 scenario-level (18 options) then intent-level (60 options)
cd ~/opt_r2/voice; export HF_HUB_OFFLINE=1 OMP_NUM_THREADS=${T:-4} MKL_NUM_THREADS=${T:-4}
while [ "$(cat out/asr_slurp_s560.shard*.jsonl 2>/dev/null | wc -l)" != 500 ]; do sleep 20; done
echo asr slurp ready
taskset -c ${CPUS:-0-3} venv/bin/python -B scripts/c1_slurp.py --level scen --asr s560 --n 500 --threads ${T:-4} >> logs/c1_scen.log 2>&1; echo scen rc=$?
taskset -c ${CPUS:-0-3} venv/bin/python -B scripts/c1_slurp.py --level intent --asr s560 --n 120 --threads ${T:-4} >> logs/c1_intent.log 2>&1; echo intent rc=$?
echo C1_QUEUE_DONE
