#!/usr/bin/env bash
# vm.sh <vm> <command...>  : ssh via the same IAP gcloud transport gcp_run.sh uses (probes + work under ~/opt_r2)
VM="$1"; shift
case "$VM" in od-l4b|od-cpu1) Z=us-east4-c;; *) echo bad vm; exit 2;; esac
gcloud compute ssh "$VM" --zone "$Z" --project system-one-509903 --tunnel-through-iap --quiet --command "$*" 2>&1 \
  | grep -v -e '^Updating project ssh' -e 'WARNING: ' -e 'increasing the TCP' -e 'consider installing NumPy' -e '^please see https://cloud.google.com/iap' -e '^tar: Ignoring' -e '^$'
exit "${PIPESTATUS[0]}"
