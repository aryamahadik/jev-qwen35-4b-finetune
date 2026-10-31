#!/usr/bin/env bash
# ASR job queue on od-cpu1 pinned to vCPUs 4-7 (C1 uses 0-3). Resumable: re-running skips finished utterances.
# s560: ls_clean fp32 (500), the other sets bf16/AMX (500), plus a bf16 re-run of 150 ls_clean utts as a dtype check.
# offline: fp32 (500).  s160: bf16, first 150 utts of the seeded shuffle per set (CPU budget).
cd ~/opt_r2/voice; export HF_HUB_OFFLINE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
P=${P:-4}; K=4
jobs=()
for sh in $(seq 0 $((K-1))); do jobs+=("ls_clean s560 $sh fp32 0 -"); done
for s in ls_other tedlium ami earnings22; do for sh in $(seq 0 $((K-1))); do jobs+=("$s s560 $sh bf16 0 -"); done; done
for sh in $(seq 0 $((K-1))); do jobs+=("ls_clean s560 $sh bf16 150 _bf16chk"); done
for s in ls_clean ls_other tedlium ami earnings22; do for sh in $(seq 0 $((K-1))); do jobs+=("$s offline $sh fp32 0 -"); done; done
for s in ls_clean ls_other tedlium ami earnings22; do for sh in $(seq 0 $((K-1))); do jobs+=("$s s160 $sh bf16 ${N160:-150} -"); done; done
printf '%s\n' "${jobs[@]}" | xargs -P "$P" -L 1 bash -c "taskset -c 4-7 venv/bin/python -B scripts/asr_run.py --set \$0 --mode \$1 --shard \$2/$K --dtype \$3 --limit \$4 --tag \"\${5/#-/}\" --threads 1 >> logs/asr_\$0_\$1_\$2\${5/#-/}.log 2>&1; echo done \$0 \$1 \$2 \$3 rc=\$?"
echo QUEUE_DONE
