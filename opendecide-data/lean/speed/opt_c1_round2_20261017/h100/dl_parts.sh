#!/usr/bin/env bash
# dl_parts.sh: fetch the 200 MB parts of the two FP8 shards from od-cpu1 (retry per part; an IAP stall only costs one part)
VM=od-cpu1; Z=us-east4-c
DRY=$(gcloud compute ssh "$VM" --zone "$Z" --project system-one-509903 --tunnel-through-iap --dry-run 2>/dev/null); TARGET=${DRY##* }
SSHOPTS=$(echo "$DRY" | sed -E 's#^[^ ]*/ssh ##; s#^-t ##; s# -t ##; s# [^ ]+$##')
RSH="$HOME/.cache/gcp_run/rsh_$VM.sh"
mkdir -p "$HOME/.cache/gcp_run"; printf '#!/bin/bash\nexec ssh %s "$@"\n' "$SSHOPTS" > "$RSH"; chmod +x "$RSH"
D="$(cd "$(dirname "$0")" && pwd)/stage/parts/"
ssh_cmd() { "$RSH" "$TARGET" "$@" 2>/dev/null; }
ssh_cmd 'cd ~/opt_r2/models/c1_fp8_block_parts && sha256sum *' > "$D/parts.sha256" 2>/dev/null
wc -l "$D/parts.sha256"
for f in $(awk '{print $2}' "$D/parts.sha256"); do
  want=$(grep " $f\$" "$D/parts.sha256" | awk '{print $1}')
  for try in 1 2 3 4 5 6 7 8; do
    if [ -f "$D/$f" ] && [ "$(shasum -a 256 "$D/$f" | awk '{print $1}')" = "$want" ]; then break; fi
    rsync -a --partial --timeout=60 -e "$RSH" "$TARGET:opt_r2/models/c1_fp8_block_parts/$f" "$D" > /dev/null 2>&1
  done
  if [ "$(shasum -a 256 "$D/$f" | awk '{print $1}')" = "$want" ]; then echo "ok $f $(date +%T)"; else echo "FAILED $f"; fi
done
echo ALLDONE
