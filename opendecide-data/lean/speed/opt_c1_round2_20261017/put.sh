#!/usr/bin/env bash
# put.sh <vm> <local file> <remote path>
gcloud compute scp --tunnel-through-iap --zone us-east4-c --project system-one-509903 "$2" "$1:$3" 2>&1 | grep -v -e 'NumPy' -e 'please see' -e '^$'
