#!/bin/bash
# Free volume uploads (no compute) + read-back sha256 check. No -f: an existing folder is never overwritten.
set -uo pipefail
M=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/modal
L=/Users/aryamahadik/Documents/jev/opendecide-data/lean
T=$L/c_build/endgame/tmp
V=$T/verify; mkdir -p $V
put() { MODAL_PROFILE=$1 $M volume put opendecide "$2" "$3" > /dev/null 2>&1 && echo "PUT_OK $1 $3" || echo "PUT_FAIL_OR_EXISTS $1 $3"; }
put aryamhd   $T/jd/q35_4b_main500k_init models/q35_4b_main500k_init
put atmosphor $T/ar/q35_4b_pxE            models/q35_4b_pxE
put atmosphor $L/models/q35_4b_base0      models/q35_4b_base0
put aryamhd   $L/models/q35_4b_base0      models/q35_4b_base0
get() { rm -f "$V/$4"; MODAL_PROFILE=$1 $M volume get opendecide "$2/$3" "$V/$4" > /dev/null 2>&1; echo "SHA $1 $2/$3 $(shasum -a 256 "$V/$4" 2>/dev/null | cut -c1-64)"; }
for f in adapter_model.safetensors adapter_config.json; do
  get aryamhd   models/q35_4b_main500k_init $f ar_init_$f
  get atmosphor models/q35_4b_pxE           $f at_pxE_$f
  get atmosphor models/q35_4b_base0         $f at_base0_$f
  get aryamhd   models/q35_4b_base0         $f ar_base0_$f
done
for p in atmosphor aryamhd; do MODAL_PROFILE=$p $M volume ls opendecide models/q35_4b_base0 | sed "s/^/LS $p /"; done
MODAL_PROFILE=atmosphor $M volume ls opendecide models/q35_4b_pxE | sed "s/^/LS atmosphor /"
MODAL_PROFILE=aryamhd $M volume ls opendecide models/q35_4b_main500k_init | sed "s/^/LS aryamhd /"
echo PUT_VERIFY_DONE
