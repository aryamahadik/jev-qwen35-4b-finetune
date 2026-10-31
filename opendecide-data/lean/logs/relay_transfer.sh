#!/bin/bash
# Relay the 4B to ANOTHER account: download _ckpt from FROM, verify, upload to TO, re-download, verify, print launch.
# Usage: relay_transfer.sh <from_profile> <to_profile> <prev_seg_log> <new_seg_log> <handoff_tag>
set -euo pipefail
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean
FROM=$1; TO=$2; PREV=$3; NEW=$4; TAG=$5; M=../.venv/bin/modal
N=$(grep -o '"stopped_at_step": [0-9]*' "$PREV" | tail -1 | grep -o '[0-9]*$'); test -n "$N"
echo "previous segment stopped at step $N"
if MODAL_PROFILE=$FROM $M app list 2>/dev/null | grep -qi ephemeral; then echo "an app is still running on $FROM - stop"; exit 1; fi
if MODAL_PROFILE=$TO $M volume ls opendecide models/q35_4b_main500k 2>/dev/null | grep -q .; then echo "target path not empty on $TO - stop"; exit 1; fi
mkdir -p handoff/$TAG handoff/${TAG}_back
MODAL_PROFILE=$FROM $M volume get opendecide models/q35_4b_main500k/_ckpt handoff/$TAG
../.venv/bin/python pilot/compare_relay.py --check handoff/$TAG/_ckpt --step "$N"
MODAL_PROFILE=$TO $M volume put opendecide handoff/$TAG/_ckpt models/q35_4b_main500k/_ckpt
MODAL_PROFILE=$TO $M volume get opendecide models/q35_4b_main500k/_ckpt handoff/${TAG}_back
../.venv/bin/python pilot/compare_relay.py --check handoff/${TAG}_back/_ckpt --step "$N"
USED=$(MODAL_PROFILE=$TO $M billing summary --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["metered_cost"])')
LEFT_STEPS=$((30457 - N))
MIN=$(python3 -c "u=float('$USED'); left=30-u; m=int((left-2.0)/4.09*60); need=int($LEFT_STEPS*2.75/60)+8; print(max(0,min(m,540,need)))")
echo "$TO October used \$$USED; steps left $LEFT_STEPS -> stop-after-min $MIN"
git -C /Users/aryamahadik/Documents/jev diff --quiet final-frozen -- opendecide-data/lean/train_decoder.py opendecide-data/lean/decoder_io.py opendecide-data/lean/prism_x.py opendecide-data/lean/writeblock.py opendecide-data/lean/runs/q35_4b_main.json && echo "frozen files unchanged"
echo "RELAY_FILES_OK step $N"
echo "LAUNCH: MODAL_PROFILE=$TO ../.venv/bin/modal run --detach modal_od.py::relay --config runs/q35_4b_main.json --expect-resume --stop-after-min $MIN > $NEW 2>&1"
