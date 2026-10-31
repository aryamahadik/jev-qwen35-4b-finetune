#!/bin/bash
# F6 carry: ORCHESTRATOR-RUN install (needs the two rulings in the return summary). Moves (never deletes) the stale pre-A32 round-1
# crowd inputs of F6 to a backup, puts the v2 C1 one-view shards + labels where c2_select.py carry reads them (data/c_crowd_r1_shards/F6)
# and writes the round-1 selection record select_F6.json for the v2 candidates with a C1-only crowd (A37 e).
# Run from lean/c2_build:  bash zed_orch/f6_carry/install_carry_inputs.sh
set -euo pipefail
cd "$(dirname "$0")/../.."          # lean/c2_build
LEAN=$(cd .. && pwd); B=$LEAN/c2_build/_backup_f6_carry_20261017
[ -d "$LEAN/data/c2_crowd_shards/F6/labels_q35_4b_main500k" ] || { echo "v2 labels missing"; exit 1; }
[ ! -e "$B" ] || { echo "backup folder exists: $B"; exit 1; }
mkdir -p "$B"
mv "$LEAN/data/c_crowd_r1_shards/F6" "$B/c_crowd_r1_shards_F6"
cp -p "$LEAN/c_build/crowd_r1/select_F6.json" "$LEAN/c_build/crowd_r1/g5_reread_F6.json" "$B/"
cp -Rp "$LEAN/data/c2_crowd_shards/F6" "$LEAN/data/c_crowd_r1_shards/F6"
../../.venv/bin/python -B zed_orch/f6_carry/r1_select_c1only.py --install
shasum -a 256 "$LEAN/data/c_crowd_r1_shards/F6/shards.json" "$LEAN/c_build/crowd_r1/select_F6.json"
