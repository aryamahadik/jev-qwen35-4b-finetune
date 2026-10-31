#!/bin/bash
# build the block-FP8 checkpoint on od-cpu1 (CPU only) from the merged BF16 C1 there; sha of the sources first
cd ~/opt_r2
SRC=~/models/q35_4b_main500k_merged
echo "sha256 of source shards (od-cpu1):"; sha256sum $SRC/model.safetensors-0000*.safetensors | cut -c1-16,65-
mkdir -p ~/opt_r2/models
HF_HUB_OFFLINE=1 ~/od/bin/python -B build_fp8_block.py $SRC ~/opt_r2/models/c1_fp8_block
echo "build rc=$?"
ls -la ~/opt_r2/models/c1_fp8_block | head -30
du -sh ~/opt_r2/models/c1_fp8_block
