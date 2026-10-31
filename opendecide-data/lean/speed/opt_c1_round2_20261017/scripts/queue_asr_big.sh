#!/usr/bin/env bash
# larger independent samples (AMI 2000, Earnings-22 1500), s560 bf16, after the fp32 control
cd ~/opt_r2/voice; export HF_HUB_OFFLINE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "scripts/queue_asr_ctl.sh" >/dev/null; do sleep 30; done
P=${P:-4}; K=4
jobs=()
for sh in $(seq 0 $((K-1))); do jobs+=("ami_big s560 $sh bf16 0 -"); done
for sh in $(seq 0 $((K-1))); do jobs+=("earnings22_big s560 $sh bf16 0 -"); done
printf '%s\n' "${jobs[@]}" | xargs -P "$P" -L 1 bash -c "taskset -c 4-7 venv/bin/python -B scripts/asr_run.py --set \$0 --mode \$1 --shard \$2/$K --dtype \$3 --limit \$4 --tag \"\${5/#-/}\" --threads 1 >> logs/asr_\$0_\$1_\$2.log 2>&1; echo done big \$0 \$1 \$2 rc=\$?"
echo BIG_DONE
