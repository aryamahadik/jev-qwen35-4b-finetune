#!/bin/bash
# GPU stages for the vision bench, run on od-l4b. Does NOT stop or start any C2 process: it refuses to run unless the GPU is free.
# usage: nohup bash ~/vision_bench/harness/gpu_chain.sh > ~/vision_bench/logs/chain.log 2>&1 &
set -u
cd ~/vision_bench/harness || exit 1
mkdir -p ~/vision_bench/logs ~/vision_bench/results ~/vision_bench/triton_cache
used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
if [ "$used" -gt 6000 ]; then echo "GPU busy ($used MiB used): not running"; exit 3; fi
export PYTHONPATH=$HOME/vision_bench/pylib HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TRITON_CACHE_DIR=$HOME/vision_bench/triton_cache
PY=$HOME/od/bin/python
date -u +"start %F %T"
for m in c1 base; do
  $PY -B run_vision.py smoke --model $m --out ~/vision_bench/results > ~/vision_bench/logs/smoke_$m.log 2>&1 || { echo "smoke $m failed"; tail -5 ~/vision_bench/logs/smoke_$m.log; exit 4; }
  tail -3 ~/vision_bench/logs/smoke_$m.log | head -1
done
# stop here if a smoke check failed (probabilities must sum to 1, not be constant, shared-ViT path must match the stock path,
# the C1 LoRA must be provably applied, and C1 must NOT answer like the base model: identical answers mean the adapter is not applied)
$PY - <<'PYEOF' || exit 5
import json, os
R = {m: json.load(open(os.path.expanduser(f"~/vision_bench/results/smoke_{m}.json"))) for m in ("c1", "base")}
for m in ("c1", "base"):
    c = R[m]["checks"]
    print(m, c)
    assert c["probs_sum_to_one"] and c["not_constant"] and c["max_prob_diff_shared_vit_vs_stock"] < 0.02, c
c1 = R["c1"]["checks"]
assert c1["adapter_effect_max_logit_diff_on_vs_off"] > 1e-3, c1
ck = c1["adapter_check"]
assert ck["n_lora_B"] == 248 and ck["n_lora_B_nonzero"] == 248 and ck["n_no_home"] == 0 and ck["n_unequal_to_file"] == 0, ck
a = {it["id"]: it for it in R["c1"]["items"]}
b = {it["id"]: it for it in R["base"]["items"]}
assert a.keys() == b.keys() and len(a) == 10
conf_diff = [abs(a[k]["conf"] - b[k]["conf"]) for k in a]
print("smoke c1 vs base: mean |conf diff|", sum(conf_diff) / len(conf_diff), "max", max(conf_diff))
assert sum(conf_diff) / len(conf_diff) > 0.005, "C1 and base are near identical on the smoke items: the adapter is not applied"
PYEOF
for m in c1 base; do
  $PY -B run_vision.py eval --model $m --out ~/vision_bench/results > ~/vision_bench/logs/eval_$m.log 2>&1 || { echo "eval $m failed"; tail -8 ~/vision_bench/logs/eval_$m.log; exit 6; }
  date -u +"eval $m done %T"
done
date -u +"end %F %T"
