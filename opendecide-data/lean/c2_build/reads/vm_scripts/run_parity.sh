#!/bin/bash
cd ~/reads
export PATH=$HOME/bin:$PATH
~/od/bin/python -B fast_read.py parity --split gblock_a42d_c1read --ref preds_gblock_a42d_c1read/q35_4b_main500k.jsonl --n 2000 --seed 20261016 --workers "${1:-12}" --chunk "${2:-8}" --out ~/jobs/parity_${1:-12}_${2:-8}.json --save-preds ~/jobs/parity_preds_${1:-12}_${2:-8}.jsonl
echo rc=$?
