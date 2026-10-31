#!/bin/bash
# SPEED-1: put C1's adapter (q35_4b_main500k) from the Mac backup on a FREE-credit profile's 'opendecide' Volume at
# /models/q35_4b_main500k, where hosting/fast_host.py boots it (sha256-pinned there too). Volume operations only: no
# container, no GPU, no compute bill.
#   bash hosting/upload_c1_adapter.sh mahadikarya3          (fallback: mahadikarya2; any other profile is REFUSED)
# Order: profile allow-list -> no MODAL_TOKEN_ID/SECRET override -> local backup holds exactly the 6 expected files ->
# local adapter sha256 == pin -> Volume exists -> `modal volume put` of the adapter dir (no --force: an existing copy is
# never overwritten; if one is there it is only verified) -> verify by listing (all 6 files) and by reading the adapter
# and its config back (sha256 equal to the local files) -> report whether the base snapshot 851bf6e8 is in /vol/hf
# (if not, fast_host downloads it to the container's /tmp at boot: ~9 GB, slower boot, nothing written to the Volume).
# Last line: UPLOAD_OK <profile> or UPLOAD_FAIL <reason>.
set -uo pipefail
M=${FAST_HOST_MODAL_BIN:-/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/modal}  # override: tests only
SRC=/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k
WANT=507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078
VOL=opendecide
DST=/models/q35_4b_main500k
FILES="adapter_config.json adapter_model.safetensors chat_template.jinja tokenizer.json tokenizer_config.json"
FILES="$FILES train_meta.json"  # LC_ALL=C order
P=${1:-}
fail() { echo "UPLOAD_FAIL $*"; exit 1; }
sha() { shasum -a 256 "$1" | cut -c1-64; }

case "$P" in
  mahadikarya3|mahadikarya2) ;;
  *) fail "profile '$P': free-credit profiles only (mahadikarya3, fallback mahadikarya2); never aryamhd/jaypatil-duke";;
esac
[ -z "${MODAL_TOKEN_ID:-}${MODAL_TOKEN_SECRET:-}" ] \
  || fail "MODAL_TOKEN_ID/MODAL_TOKEN_SECRET are set and would override profile $P; unset them"
export MODAL_PROFILE=$P
[ -x "$M" ] || fail "modal CLI not found at $M"
[ -d "$SRC" ] || fail "missing local backup $SRC"
HAVE=$(cd "$SRC" && ls -A | LC_ALL=C sort | tr '\n' ' ' | sed 's/ $//')
[ "$HAVE" = "$FILES" ] || fail "local backup must hold exactly: $FILES (has: $HAVE)"
GOT=$(sha "$SRC/adapter_model.safetensors")
[ "$GOT" = "$WANT" ] || fail "local adapter sha256 $GOT != pin $WANT"
echo "local backup OK: adapter sha256 $WANT"

$M volume ls $VOL / > /dev/null 2>&1 || fail "volume '$VOL' not found on $P (never created here)"
listing() { $M volume ls $VOL $DST 2>/dev/null; }
if listing | grep -qF "adapter_model.safetensors"; then
  echo "$DST already on $P: not overwritten, verifying"
else
  $M volume put $VOL "$SRC" "$DST" || fail "volume put $SRC -> $VOL:$DST on $P"
fi

LS=$(listing) || fail "cannot list $VOL:$DST on $P"
for f in $FILES; do
  echo "$LS" | grep -qF "$f" || fail "listing of $VOL:$DST on $P lacks $f"
done
echo "listing OK: all 6 files in $VOL:$DST on $P"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
for f in adapter_model.safetensors adapter_config.json train_meta.json; do
  $M volume get $VOL "$DST/$f" "$TMP/$f" > /dev/null 2>&1 || fail "read-back of $f from $P"
  [ "$(sha "$TMP/$f")" = "$(sha "$SRC/$f")" ] || fail "sha256 of $f on $P differs from the local backup"
done
echo "read-back OK: adapter sha256 $WANT on $P"
$M volume ls $VOL /hf/hub/models--Qwen--Qwen3.5-4B/snapshots 2>/dev/null | grep -q 851bf6e8 \
  && echo "base 851bf6e8 already in /vol/hf on $P (fast_host reads it offline)" \
  || echo "base 851bf6e8 NOT in /vol/hf on $P: fast_host downloads it to the container's /tmp at boot (~9 GB, free HF)"
echo "UPLOAD_OK $P"
