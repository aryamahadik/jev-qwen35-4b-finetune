#!/bin/bash
# t1_diag.sh <trial-name> <seconds> : py-spy (sudo) on the TRIAL server's own processes only (its process group), raw stacks
# + one dump each, written under ~/opt_r2/results/<name>/pyspy. Never touches a process outside the trial's process group.
NAME="$1"; SECS="${2:-60}"
PID=$(cat ~/opt_r2/pids/$NAME.pid) || exit 1
PGID=$(ps -o pgid= -p $PID | tr -d ' ')
OUT=~/opt_r2/results/$NAME/pyspy; mkdir -p $OUT
PY=~/opt_r2/tools/py_spy-0.4.2.data/scripts/py-spy
ps -o pid,args --no-headers -g $PGID | cut -c1-110 > $OUT/procs.txt
for P in $(ps -o pid= --no-headers -g $PGID); do
  A=$(ps -o args= -p $P | cut -c1-60)
  case "$A" in
    *sglang::scheduler*) TAG=scheduler;;
    *sglang.launch_server*) TAG=main;;
    *sglang::detokenizer*) TAG=detok;;
    *) continue;;
  esac
  sudo -n $PY dump -p $P > $OUT/${TAG}_$P.dump.txt 2>&1
  (sudo -n $PY record -p $P -d $SECS -r 100 -f raw -o $OUT/${TAG}_$P.raw --nonblocking > $OUT/${TAG}_$P.rec.log 2>&1 &)
done
echo "py-spy recording $SECS s for group $PGID"
