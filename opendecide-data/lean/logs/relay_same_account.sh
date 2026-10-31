#!/bin/bash
# Continue the 4B on the SAME account after a segment stops (the checkpoint is already on that volume; no transfer).
# Usage: relay_same_account.sh <profile> <prev_seg_log> <new_seg_log>
set -euo pipefail
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean
P=$1; PREV=$2; NEW=$3; M=../.venv/bin/modal
N=$(grep -o '"stopped_at_step": [0-9]*' "$PREV" | tail -1 | grep -o '[0-9]*$'); test -n "$N"
echo "previous segment stopped at step $N"
if MODAL_PROFILE=$P $M app list 2>/dev/null | grep -qi ephemeral; then echo "an app is still running on $P - stop"; exit 1; fi
USED=$(MODAL_PROFILE=$P $M billing summary --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["metered_cost"])')
MIN=$(python3 -c "u=float('$USED'); left=30-u; m=int((left-2.0)/4.09*60); print(max(0,min(m,330)))")
echo "$P October used \$$USED -> stop-after-min $MIN"
test "$MIN" -ge 60
git -C /Users/aryamahadik/Documents/jev diff --quiet final-frozen -- opendecide-data/lean/train_decoder.py opendecide-data/lean/decoder_io.py opendecide-data/lean/prism_x.py opendecide-data/lean/writeblock.py opendecide-data/lean/runs/q35_4b_main.json && echo "frozen files unchanged"
echo "LAUNCH: MODAL_PROFILE=$P ../.venv/bin/modal run --detach modal_od.py::relay --config runs/q35_4b_main.json --expect-resume --stop-after-min $MIN > $NEW 2>&1"
