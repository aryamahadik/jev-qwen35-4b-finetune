#!/bin/bash
# A30 (B1b): FREE volume operations only (no compute) on a free-credit profile's 'opendecide' Volume.
#   bash think/b1b_copy.sh mahadikarya3          (fallback profile: mahadikarya44)
# What B1b needs and how it gets there (B1a on aryamhd did the same):
#   - Base Qwen/Qwen3.5-4B @ 851bf6e8 and drafter z-lab/Qwen3.5-4B-DFlash @ 9a1996cc: NOT copied. sglang.Engine
#     downloads them from the HF Hub into /vol/hf (HF_HOME) at the first engine start and the container commits the
#     Volume (mahadikarya3 and mahadikarya44 already hold the base snapshot 851bf6e8 in /vol/hf).
#   - C1 = q35_4b_main500k: copied from the Mac backup with a read-back sha256 check (507d1c29...). The B1b plan runs
#     no fast path (B1a measured it: p50 14.1 ms), so the launch does not need it; it is copied for the fast path and B2
#     on this profile (HANDOFF Phase B "Accounts"). Only the final files, never snaps/.
#   - Secret 'opendecide-keys' must exist on the profile (checked, not created).
# Last line: COPY_OK <profile> or COPY_FAIL <reason>.
set -uo pipefail
M=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/modal
SRC=/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k
WANT=507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078
DST=models/q35_4b_main500k
FILES="adapter_model.safetensors adapter_config.json chat_template.jinja tokenizer.json tokenizer_config.json train_meta.json"
P=${1:-}
fail() { echo "COPY_FAIL $*"; exit 1; }
case "$P" in mahadikarya3|mahadikarya44) ;; *) fail "profile '$P': free-credit profiles only (mahadikarya3, mahadikarya44)";; esac
[ "$(shasum -a 256 "$SRC/adapter_model.safetensors" | cut -c1-64)" = "$WANT" ] || fail "local backup sha256 != $WANT"
MODAL_PROFILE=$P $M secret list 2>/dev/null | grep -q "opendecide-keys" || fail "secret opendecide-keys missing on $P"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
have() { MODAL_PROFILE=$P $M volume ls opendecide $DST 2>/dev/null | grep -q "adapter_model.safetensors"; }
if ! have; then
  for f in $FILES; do  # no -f: an existing file is never overwritten
    MODAL_PROFILE=$P $M volume put opendecide "$SRC/$f" "$DST/$f" > /dev/null 2>&1 || fail "put $f"
  done
fi
for f in adapter_model.safetensors adapter_config.json; do
  MODAL_PROFILE=$P $M volume get opendecide "$DST/$f" "$TMP/$f" > /dev/null 2>&1 || fail "read-back $f"
  [ "$(shasum -a 256 "$TMP/$f" | cut -c1-64)" = "$(shasum -a 256 "$SRC/$f" | cut -c1-64)" ] || fail "sha256 $f differs on $P"
done
echo "C1 $DST on $P: adapter sha256 $WANT (read back)"
MODAL_PROFILE=$P $M volume ls opendecide hf/hub/models--Qwen--Qwen3.5-4B/snapshots 2>/dev/null | grep -q 851bf6e8 \
  && echo "base 851bf6e8 already in /vol/hf on $P" || echo "base not cached on $P: the first container downloads it (~9 GB, free HF)"
echo "COPY_OK $P"
