#!/bin/bash
# fullgen_queue.sh P FAM... : run gen_full_c2.py for each family, P at a time (nice 10); logs in logs/fullgen/<FAM>.log, rc in <FAM>.rc
P=$1; shift
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
printf '%s\n' "$@" | xargs -P "$P" -I{} bash -c 'nice -n 10 ../../.venv/bin/python -B gen_full_c2.py {} > logs/fullgen/{}.log 2>&1; echo $? > logs/fullgen/{}.rc'
