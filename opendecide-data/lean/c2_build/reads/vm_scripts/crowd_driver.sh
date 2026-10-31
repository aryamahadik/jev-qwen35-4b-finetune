#!/bin/bash
# crowd_driver.sh: C1 one-view crowd read (A37 e) of data/c2_crowd_shards/<FAM>, fast path, resumable (done shards are skipped).
export CUDA_HOME=$HOME/sgl/lib/python3.12/site-packages/nvidia/cu13
export PATH=$HOME/bin:$HOME/sgl/bin:$CUDA_HOME/bin:$PATH
export TORCH_CUDA_ARCH_LIST=8.9
cd ~/reads
echo "DRIVER_START $(date -u +%T)"
for FAM in "$@"; do
  N=$(ls ~/lean/data/c2_crowd_shards/$FAM/shard_*.jsonl | wc -l)
  echo "FAM_START $FAM shards=$N $(date -u +%T)"
  for i in $(seq 0 $((N-1))); do
    for try in 1 2 3; do
      if ! curl -s -m 10 -o /dev/null localhost:30000/health; then
        echo "$(date -u +%T) server down, restarting"; ~/reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8 --extra-args "--attention-backend triton" >> ~/jobs/serve_cmd.log 2>&1
      fi
      ~/od/bin/python -B fast_read.py label --shards-dir data/c2_crowd_shards/$FAM --shard $i --views 1 --workers 12 --chunk 8 && break
      echo "$(date -u +%T) $FAM shard $i try $try failed"
    done
  done
  echo "FAM_DONE $FAM $(date -u +%T)"
done
echo "DRIVER_DONE $(date -u +%T)"
