#!/usr/bin/env bash
# L4_REPLAY_READ.sh: C1 A5 read of the C round-1 replay draw on od-l4b (free L4, Google credit; not a GO point).
# Made from c_build/RUNBOOK_replay_reads.md sections 4-7 and 9 for the orchestrator. The C builder did not run gcloud.
#
# VM od-l4b, zone us-east4-c, project system-one-509903. Every gcloud call spells out --zone and --project.
# Run from the Mac, inside lean/:   bash c_build/L4_REPLAY_READ.sh <step>
# Steps, in order. Each one is safe to repeat:
#   local     Mac only, no gcloud: every pushed file against c_build/L4_REPLAY_READ.sha256
#   start     start the VM
#   preflight VM checks: GPU idle, no od_gcp.py job, python env, base snapshot, C1 adapter sha256, disk
#   push      copy shards + code + config + the remote driver, then re-check all 31 sha256 on the VM
#   f2        F2 rendered-prompt record on the VM (CPU, about 1 min); fetch it; compare it with the Mac record
#   launch    start the read in the background (setsid nohup; resumable per shard; refuses if a label job runs)
#   status    log tail + shards done (20 round-1 + 1 old slice when finished)
#   fetch     pull both label folders and the log; check them on the Mac (every shard done, one view, template)
#   stop      stop the VM (only after fetch)
# Resume after a stop or preemption: start, then launch again. Finished shards are skipped.
# Expected time: about 11-12 L4 hours for round 1 (99,069 rows, 134,025 forward reads), plus about 15 min for the
# 2,000-row old slice (RUNBOOK 2). After fetch, the Mac second pass (RUNBOOK 7; A16 ruling e is the amendment):
#   ../.venv/bin/python c_build/replay_sample.py --second-pass data/c_replay_r1_shards/labels_q35_4b_main500k \
#       --pg-rule-amendment A16
#
# Pinned (round-1 write, 3 Oct 2026, 20:50 UTC; c_build/replay_r1_write.json):
#   data/c_replay_r1_shards/shards.json  sha256 3f96d3edda41b15d810cba9023567ada3147b5b5ee551e0d85f02a0bfbfa62e2
#     (99,069 rows, 20 shards; ids 5ab3ef30..., rows 91f2dd77...)
#   data/c_old_slice_shards/shards.json  sha256 9118d6b58466d301da0bb2dd5a197d164dcc933154e16d2dfcc9e555e3fa63d8
#     (2,000 rows, 1 shard)
#   C1 adapter models/q35_4b_main500k/adapter_model.safetensors
#                                          sha256 507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078
#   base Qwen/Qwen3.5-4B @ 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a; chat template sha a4aee8af... (C1's stored reads)
#   code: train_decoder.py c2c2d1d6..., decoder_io.py 908c08d7..., runs/q35_4b_c_r1.json f3bb379e... (A16); every
#   pushed file is listed with its sha256 in c_build/L4_REPLAY_READ.sha256
set -euo pipefail
cd "$(dirname "$0")/.."           # lean/

case "${1:-}" in
local)
  shasum -a 256 -c c_build/L4_REPLAY_READ.sha256 | grep -v ': OK$' || echo "all 31 files OK"
  shasum -a 256 -c --status c_build/L4_REPLAY_READ.sha256
  ;;

start)
  gcloud compute instances start od-l4b --zone us-east4-c --project system-one-509903
  ;;

preflight)
  gcloud compute ssh od-l4b --zone us-east4-c --project system-one-509903 --command '
    cd ~/lean || { echo "NO ~/lean on od-l4b"; exit 2; }
    if pgrep -f "od_gcp.py" >/dev/null; then echo "BUSY: an od_gcp.py job is running"; else echo "idle: no od_gcp.py job"; fi
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv
    ~/od/bin/python -c "import torch, transformers, peft; print(\"torch\", torch.__version__, \"transformers\", transformers.__version__, \"peft\", peft.__version__, \"cuda\", torch.cuda.is_available())"
    ls -d ~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a || echo "BASE SNAPSHOT MISSING (label runs offline)"
    echo "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078  models/q35_4b_main500k/adapter_model.safetensors" | sha256sum -c - || echo "ADAPTER MISSING OR DIFFERENT"
    df -h ~ | tail -1'
  echo "Launch only if: idle, cuda True, base snapshot present, adapter OK (one job at a time on the VM)."
  ;;

push)
  shasum -a 256 -c --status c_build/L4_REPLAY_READ.sha256
  gcloud compute ssh od-l4b --zone us-east4-c --project system-one-509903 --command 'mkdir -p ~/lean/data ~/lean/runs ~/lean/logs ~/lean/c_build'
  gcloud compute scp --recurse --zone us-east4-c --project system-one-509903 \
    data/c_replay_r1_shards data/c_old_slice_shards od-l4b:~/lean/data/
  gcloud compute scp --zone us-east4-c --project system-one-509903 \
    od_gcp.py decoder_io.py shard_golden.py train_decoder.py prism_x.py writeblock.py od-l4b:~/lean/
  gcloud compute scp --zone us-east4-c --project system-one-509903 runs/q35_4b_c_r1.json od-l4b:~/lean/runs/
  gcloud compute scp --zone us-east4-c --project system-one-509903 \
    c_build/l4_replay_read_remote.sh c_build/L4_REPLAY_READ.sha256 od-l4b:~/lean/c_build/
  gcloud compute ssh od-l4b --zone us-east4-c --project system-one-509903 --command 'cd ~/lean && \
    sha256sum -c --quiet c_build/L4_REPLAY_READ.sha256 && echo "VM: all 31 files OK"'
  ;;

f2)
  # recipe v4 pre-flight 9 (RUNBOOK 9): this machine's F2 record on the C round-1 config with the C1 adapter (CPU)
  gcloud compute ssh od-l4b --zone us-east4-c --project system-one-509903 --command 'cd ~/lean && \
    HF_HUB_OFFLINE=1 ~/od/bin/python train_decoder.py f2 --config runs/q35_4b_c_r1.json \
    --adapter models/q35_4b_main500k --where od-l4b-gate --out logs/f2_l4.json'
  gcloud compute scp --zone us-east4-c --project system-one-509903 od-l4b:~/lean/logs/f2_l4.json c_build/f2_l4.json
  # L4 vs Mac now. Before the GO, the full check adds the Modal smoke record (RUNBOOK 9) and must print
  # "f2_cross": "pass":
  #   ../.venv/bin/python train_decoder.py f2cmp c_build/f2_l4.json logs/pilot/f2_<smoke tag>.json c_build/f2_local_mac.json
  ../.venv/bin/python train_decoder.py f2cmp c_build/f2_l4.json c_build/f2_local_mac.json
  ;;

launch)
  gcloud compute ssh od-l4b --zone us-east4-c --project system-one-509903 --command 'cd ~/lean && \
    if pgrep -f "od_gcp.py label" >/dev/null; then echo "BUSY: a label job is running; not launching"; exit 3; fi; \
    mkdir -p logs && setsid nohup bash c_build/l4_replay_read_remote.sh >> logs/c_replay_r1_label.log 2>&1 < /dev/null & \
    sleep 5; tail -n 5 ~/lean/logs/c_replay_r1_label.log; echo launched'
  ;;

status)
  gcloud compute ssh od-l4b --zone us-east4-c --project system-one-509903 --command 'cd ~/lean && \
    (pgrep -fa "l4_replay_read_remote.sh|od_gcp.py label" || echo "no read job running"); \
    tail -n 6 logs/c_replay_r1_label.log; \
    echo "round-1 shards done: $(ls data/c_replay_r1_shards/labels_q35_4b_main500k/*.meta.json 2>/dev/null | wc -l) of 20"; \
    echo "old-slice shards done: $(ls data/c_old_slice_shards/labels_q35_4b_main500k/*.meta.json 2>/dev/null | wc -l) of 1"'
  ;;

fetch)
  gcloud compute scp --recurse --zone us-east4-c --project system-one-509903 \
    od-l4b:~/lean/data/c_replay_r1_shards/labels_q35_4b_main500k data/c_replay_r1_shards/
  gcloud compute scp --recurse --zone us-east4-c --project system-one-509903 \
    od-l4b:~/lean/data/c_old_slice_shards/labels_q35_4b_main500k data/c_old_slice_shards/
  mkdir -p logs
  gcloud compute scp --zone us-east4-c --project system-one-509903 \
    od-l4b:~/lean/logs/c_replay_r1_label.log logs/c_replay_r1_label_od-l4b.log
  # every shard done, one view with C1's A5 settings, C1's chat template
  ../.venv/bin/python - <<'EOF'
import json, sys
from pathlib import Path
import shard_golden as sg
TPL = "a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715"
REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
bad = 0
for d in ("data/c_replay_r1_shards", "data/c_old_slice_shards"):
    lab = Path(d) / "labels_q35_4b_main500k"
    probs, view = sg.load_labels(lab, d, return_view=True)   # raises if a shard is missing, incomplete or another view
    s = view["settings"]
    ok = (s["name"] == "q35_4b_main500k" and s["revision"] == REV and s["layout"] == "schema_branch_mark"
          and s.get("tta_choice") and not s.get("tta_noul") and s.get("perm_seed") is None and s.get("merged"))
    t = {json.loads(p.read_text()).get("load", {}).get("chat_template_sha") for p in lab.glob("shard_*.meta.json")}
    print(d, "rows", len(probs), "settings", "OK" if ok else f"WRONG {s}", "template", "OK" if t == {TPL} else f"WRONG {t}")
    bad += (not ok) or t != {TPL}
sys.exit(1 if bad else 0)
EOF
  ;;

stop)
  gcloud compute instances stop od-l4b --zone us-east4-c --project system-one-509903
  ;;

*)
  sed -n '2,35p' "$0"
  exit 2
  ;;
esac
