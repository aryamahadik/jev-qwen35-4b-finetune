#!/usr/bin/env bash
# dl_fp8.sh: rsync (resumable) the verified block-FP8 checkpoint from od-cpu1 (a CPU VM, not production) to ./stage/c1_fp8_block
VM=od-cpu1; Z=us-east4-c
DRY=$(gcloud compute ssh "$VM" --zone "$Z" --project system-one-509903 --tunnel-through-iap --dry-run 2>/dev/null); TARGET=${DRY##* }
SSHOPTS=$(echo "$DRY" | sed -E 's#^[^ ]*/ssh ##; s#^-t ##; s# -t ##; s# [^ ]+$##')
RSH="$HOME/.cache/gcp_run/rsh_$VM.sh"
mkdir -p "$HOME/.cache/gcp_run"; printf '#!/bin/bash\nexec ssh %s "$@"\n' "$SSHOPTS" > "$RSH"; chmod +x "$RSH"
D="$(cd "$(dirname "$0")" && pwd)/stage/c1_fp8_block/"
for try in 1 2 3 4 5 6 7 8 9 10 11 12; do
rsync -a --partial --timeout=90 -e "$RSH" "$TARGET:opt_r2/models/c1_fp8_block/" "$D" 2>&1 | grep -v -E "NumPy|increasing the tunnel|^WARNING|iap/docs|^$"
rc=${PIPESTATUS[0]}; echo "try $try rsync exit $rc $(date +%T)"; [ "$rc" = 0 ] && break; sleep 5
done
