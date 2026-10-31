#!/bin/bash
# Free volume copies (no compute): fetch init (jaypatil-duke) and pxE + C1 (aryamhd) + C1 (atmosphor) for sha checks.
set -uo pipefail
M=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/modal
T=/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_build/endgame/tmp
mkdir -p $T/jd $T/ar $T/at
MODAL_PROFILE=jaypatil-duke $M volume get opendecide models/q35_4b_main500k_init $T/jd/ && echo "jd init ok"
MODAL_PROFILE=aryamhd $M volume get opendecide models/q35_4b_pxE $T/ar/ && echo "ar pxE ok"
MODAL_PROFILE=aryamhd $M volume get opendecide models/q35_4b_main500k/adapter_model.safetensors $T/ar/c1_adapter_model.safetensors && echo "ar C1 ok"
MODAL_PROFILE=atmosphor $M volume get opendecide models/q35_4b_main500k/adapter_model.safetensors $T/at/c1_adapter_model.safetensors && echo "at C1 ok"
MODAL_PROFILE=atmosphor $M volume ls opendecide models/q35_4b_main500k > $T/at/c1_ls.txt 2>&1
MODAL_PROFILE=aryamhd $M volume ls opendecide models/q35_4b_main500k > $T/ar/c1_ls.txt 2>&1
echo FETCH_DONE
