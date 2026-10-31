#!/usr/bin/env bash
# after the big-sample ASR runs: stop the 4-thread intent job, measure idle-machine CPU timings, then run the intent job on all 8 vCPUs
cd ~/opt_r2/voice; export HF_HUB_OFFLINE=1
while pgrep -f "scripts/queue_asr_big.sh" >/dev/null; do sleep 20; done
P=$(ps -eo pid,cmd | grep -E "queue_c1.sh|scripts/c1_slurp.py" | grep -v grep | awk '{print $1}' | tr '\n' ' '); kill $P; sleep 5
echo "idle timing, 1 thread"; OMP_NUM_THREADS=1 taskset -c 0 venv/bin/python -B scripts/timing_idle.py 1 > logs/timing_idle_1t.log 2>&1; echo rc=$?
echo "idle timing, 4 threads"; OMP_NUM_THREADS=4 taskset -c 0-3 venv/bin/python -B scripts/timing_idle.py 4 > logs/timing_idle_4t.log 2>&1; echo rc=$?
echo "intent run"; OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 HF_HUB_OFFLINE=1 venv/bin/python -B scripts/c1_slurp.py --level intent --asr s560 --n ${NINT:-80} --threads 8 >> logs/c1_intent.log 2>&1; echo intent rc=$?
echo POST_DONE
