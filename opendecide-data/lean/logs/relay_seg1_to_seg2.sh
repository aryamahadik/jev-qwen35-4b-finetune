#!/bin/bash
# Relay 4B main run: segment 1 (jaypatil-duke) -> segment 2 (arya-mahadik-ai). Stops on the first failure.
set -euo pipefail
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean
M=../.venv/bin/modal
N=$(grep -o '"stopped_at_step": [0-9]*' logs/main4b_seg1.log | tail -1 | grep -o '[0-9]*$')
echo "segment 1 stopped at step $N"
test -n "$N"
mkdir -p handoff/main_s1 handoff/main_s1_back
MODAL_PROFILE=jaypatil-duke $M volume get opendecide models/q35_4b_main500k/_ckpt handoff/main_s1
../.venv/bin/python pilot/compare_relay.py --check handoff/main_s1/_ckpt --step "$N"
echo "--- target path must be empty on arya-mahadik-ai:"
if MODAL_PROFILE=arya-mahadik-ai $M volume ls opendecide models/q35_4b_main500k 2>/dev/null | grep -q .; then echo "NOT EMPTY - stop"; exit 1; fi
MODAL_PROFILE=arya-mahadik-ai $M volume put opendecide handoff/main_s1/_ckpt models/q35_4b_main500k/_ckpt
MODAL_PROFILE=arya-mahadik-ai $M volume get opendecide models/q35_4b_main500k/_ckpt handoff/main_s1_back
../.venv/bin/python pilot/compare_relay.py --check handoff/main_s1_back/_ckpt --step "$N"
echo "RELAY_FILES_OK step $N"
