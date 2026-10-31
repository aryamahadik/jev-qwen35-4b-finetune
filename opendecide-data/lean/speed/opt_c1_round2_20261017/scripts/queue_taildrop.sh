#!/usr/bin/env bash
# ablation: the model-card loop (final partial chunk dropped, no flush) vs our flush, on the same 150 LibriSpeech test-other + 150 TED-LIUM utterances (bf16, s560)
cd ~/opt_r2/voice; export HF_HUB_OFFLINE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
while pgrep -f "scripts/post_intent_more.sh" >/dev/null || pgrep -f "scripts/post_asr.sh" >/dev/null; do sleep 15; done
K=4; jobs=()
for s in ls_other tedlium; do for sh in $(seq 0 $((K-1))); do jobs+=("$s s560 $sh bf16 150 _taildrop"); done; done
printf '%s\n' "${jobs[@]}" | xargs -P 8 -L 1 bash -c "venv/bin/python -B scripts/asr_run.py --set \$0 --mode \$1 --shard \$2/$K --dtype \$3 --limit \$4 --tag \"\$5\" --tail drop --threads 1 >> logs/asr_\$0_\$1_\$2\$5.log 2>&1; echo done taildrop \$0 \$2 rc=\$?"
echo TAILDROP_DONE
