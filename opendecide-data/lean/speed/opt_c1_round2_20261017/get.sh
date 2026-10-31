#!/usr/bin/env bash
# get.sh <vm> <remote path> <local path>
gcloud compute scp --tunnel-through-iap --zone us-east4-c --project system-one-509903 "$1:$2" "$3" 2>&1 | grep -v -e 'NumPy' -e 'please see' -e '^$'
