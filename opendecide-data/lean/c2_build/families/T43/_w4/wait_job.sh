#!/bin/bash
# wait_job.sh JOB : polls the VM until ~/jobs/JOB.rc exists
until gcloud compute ssh od-l4b --zone us-east4-c --project system-one-509903 --tunnel-through-iap --quiet --command "test -f ~/jobs/$1.rc" >/dev/null 2>&1; do sleep 120; done
echo done $1
