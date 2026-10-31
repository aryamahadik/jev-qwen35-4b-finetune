#!/bin/bash
# pull_stage.sh: copy ONLY zed_orch/T33_fix_r2 (gen_root, out, logs; no .py) from the VM od-l4b into the same Mac folder.
# Never touches data/c2_parts. Run post_pull.py afterwards (VM paths -> this Mac, manifest hashes, staged A50 aggregate).
set -euo pipefail
VM=od-l4b; Z=us-east4-c; P=system-one-509903
HERE="$(cd "$(dirname "$0")" && pwd)"
DRY=$(gcloud compute ssh "$VM" --zone "$Z" --project "$P" --tunnel-through-iap --dry-run 2>/dev/null); TARGET=${DRY##* }
RSH="$HOME/.cache/gcp_run/rsh_$VM.sh"
[ -x "$RSH" ] || { echo "no rsh wrapper $RSH: run ACTION=sync zed_orch/gcp_run.sh $VM once"; exit 2; }
rsync -az --exclude='*.py' --exclude='__pycache__' --exclude='*.pyc' -e "$RSH" \
  "$TARGET:~/repo/opendecide-data/lean/c2_build/zed_orch/T33_fix_r2/" "$HERE/"
echo "pulled zed_orch/T33_fix_r2 from $VM"
