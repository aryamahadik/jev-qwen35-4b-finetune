#!/usr/bin/env bash
# fp32 control for the two sets (AMI, Earnings-22) whose bf16 s560 estimate sits outside the card +-0.5 pt: same 500 utterances in fp32
cd ~/opt_r2/voice; export HF_HUB_OFFLINE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "scripts/queue_asr_ext.sh" >/dev/null; do sleep 30; done
P=${P:-4}; K=4
jobs=()
for sh in $(seq 0 $((K-1))); do jobs+=("earnings22 s560 $sh fp32 500 _fp32chk"); done
for sh in $(seq 0 $((K-1))); do jobs+=("ami s560 $sh fp32 500 _fp32chk"); done
printf '%s\n' "${jobs[@]}" | xargs -P "$P" -L 1 bash -c "taskset -c 4-7 venv/bin/python -B scripts/asr_run.py --set \$0 --mode \$1 --shard \$2/$K --dtype \$3 --limit \$4 --tag \"\$5\" --threads 1 >> logs/asr_\$0_\$1_\$2\$5.log 2>&1; echo done ctl \$0 \$1 \$2 rc=\$?"
echo CTL_DONE
