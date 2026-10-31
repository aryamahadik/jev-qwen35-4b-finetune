#!/usr/bin/env bash
# dl_small.sh: everything except the two big shards (and without touching the edited config.json)
VM=od-cpu1; Z=us-east4-c
DRY=$(gcloud compute ssh "$VM" --zone "$Z" --project system-one-509903 --tunnel-through-iap --dry-run 2>/dev/null); TARGET=${DRY##* }
SSHOPTS=$(echo "$DRY" | sed -E 's#^[^ ]*/ssh ##; s#^-t ##; s# -t ##; s# [^ ]+$##')
RSH="$HOME/.cache/gcp_run/rsh_$VM.sh"
D="$(cd "$(dirname "$0")" && pwd)/stage/c1_fp8_block/"
for try in 1 2 3 4 5; do
  rsync -a --partial --timeout=60 --exclude 'model.safetensors-0000*' --exclude config.json -e "$RSH" "$TARGET:opt_r2/models/c1_fp8_block/" "$D" > /dev/null 2>&1 && { echo "small files ok"; break; }
  sleep 3
done
