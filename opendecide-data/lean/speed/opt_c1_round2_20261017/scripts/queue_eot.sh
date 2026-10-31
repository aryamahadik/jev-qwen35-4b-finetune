#!/usr/bin/env bash
cd ~/opt_r2/voice; export HF_HUB_OFFLINE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
printf '%s\n' "slurp 0/2 500" "slurp 1/2 500" "ami 0/2 500" "ami 1/2 500" "ls_clean 0/1 100" | xargs -P "${P:-5}" -L 1 bash -c 'venv/bin/python -B scripts/eot_run.py --set $0 --shard $1 --n $2 --threads 1 >> logs/eot_$0_$(echo $1|tr / _).log 2>&1; echo done eot $0 $1 rc=$?'
echo EOT_QUEUE_DONE
