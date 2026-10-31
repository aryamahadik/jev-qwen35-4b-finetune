#!/usr/bin/env bash
# waits for the main ASR queue, then extends s560 (bf16) on the two sets whose 500-utt WER sits outside the card's +-0.5 pt (AMI, Earnings-22)
cd ~/opt_r2/voice; export HF_HUB_OFFLINE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "scripts/queue_asr.sh" >/dev/null; do sleep 30; done
P=${P:-4}; K=4
jobs=()
for sh in $(seq 0 $((K-1))); do jobs+=("ami s560 $sh bf16 ${NAMI:-2000} -"); done
for sh in $(seq 0 $((K-1))); do jobs+=("earnings22 s560 $sh bf16 ${NE22:-1500} -"); done
printf '%s\n' "${jobs[@]}" | xargs -P "$P" -L 1 bash -c "taskset -c 4-7 venv/bin/python -B scripts/asr_run.py --set \$0 --mode \$1 --shard \$2/$K --dtype \$3 --limit \$4 --tag \"\${5/#-/}\" --threads 1 >> logs/asr_\$0_\$1_\$2\${5/#-/}_ext.log 2>&1; echo done ext \$0 \$1 \$2 rc=\$?"
echo EXT_DONE
