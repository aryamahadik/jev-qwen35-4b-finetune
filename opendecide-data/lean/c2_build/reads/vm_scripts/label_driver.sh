#!/bin/bash
# label_driver.sh: read every shard of data/c2_replay_shards with the SGLang fast path; restart the server if it died.
export CUDA_HOME=$HOME/sgl/lib/python3.12/site-packages/nvidia/cu13
export PATH=$HOME/bin:$HOME/sgl/bin:$CUDA_HOME/bin:$PATH
export TORCH_CUDA_ARCH_LIST=8.9
cd ~/reads
N=$(ls ~/lean/data/c2_replay_shards/shard_*.jsonl | wc -l)
for i in $(seq 0 $((N-1))); do
  for try in 1 2 3; do
    if ! curl -s -m 10 -o /dev/null localhost:30000/health; then
      echo "$(date -u +%T) server down, restarting"; ~/reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8 --extra-args "--attention-backend triton" >> ~/jobs/serve_cmd.log 2>&1
    fi
    ~/od/bin/python -B fast_read.py label --shards-dir data/c2_replay_shards --shard $i --reuse ~/jobs/reuse_labels.jsonl --workers 12 --chunk 8 && break
    echo "$(date -u +%T) shard $i try $try failed"
  done
done
echo "DRIVER_DONE $(date -u +%T)"
