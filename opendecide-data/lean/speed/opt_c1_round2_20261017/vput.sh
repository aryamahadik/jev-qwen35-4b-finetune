#!/usr/bin/env bash
# vput.sh <vm> <local path> <remote dir under ~/opt_r2/voice>   (rsync over the IAP ssh wrapper written by gcp_run.sh)
VM="$1"; SRC="$2"; DST="$3"
case "$VM" in od-l4b|od-cpu1) Z=us-east4-c;; *) echo bad vm; exit 2;; esac
DRY=$(gcloud compute ssh "$VM" --zone "$Z" --project system-one-509903 --tunnel-through-iap --dry-run 2>/dev/null); TARGET=${DRY##* }
SSHOPTS=$(echo "$DRY" | sed -E 's#^[^ ]*/ssh ##; s#^-t ##; s# -t ##; s# [^ ]+$##')
RSH="$HOME/.cache/gcp_run/rsh_$VM.sh"
mkdir -p "$HOME/.cache/gcp_run"; printf '#!/bin/bash\nexec ssh %s "$@"\n' "$SSHOPTS" > "$RSH"; chmod +x "$RSH"
rsync -a --partial -e "$RSH" "$SRC" "$TARGET:opt_r2/voice/$DST" 2>&1 | grep -v -E "NumPy|increasing the tunnel|^WARNING|iap/docs|^$"; exit ${PIPESTATUS[0]}
