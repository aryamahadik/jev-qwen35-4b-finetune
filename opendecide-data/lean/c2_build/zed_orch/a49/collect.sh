#!/bin/bash
# pull VM ext jobs and merge each family once its ext json (and, for the nine, cells json) exists
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
FAMS="T01 T06 T07 T12 T23 T24 T28 T30 T31 T33 T25 T15 T26 T32"
for it in $(seq 1 400); do
  for J in a49_ext9 a49_ext_regen a49_ext_t26 a49_ext_t32 a49_ext_t01; do ACTION=pull JOB=$J NOSYNC=1 zed_orch/gcp_run.sh od-l4b >/dev/null 2>&1; done
  n=0
  for f in $FAMS; do
    [ -f zed_orch/a49/merged_$f ] && { n=$((n+1)); continue; }
    if [ -f zed_orch/a49/${f}_ext.json ]; then
      case $f in T33|T25|T15|T26|T32) ok=1;; *) [ -f zed_orch/a49/${f}_cells.json ] && ok=1 || ok=0;; esac
      if [ $ok = 1 ]; then nice -n 10 $PY -B gen_full_c2.py $f --merge-a49 > zed_orch/a49/logs/merge_$f.log 2>&1 && touch zed_orch/a49/merged_$f && n=$((n+1)); fi
    fi
  done
  echo "$(date +%H:%M) merged $n/14"
  [ $n -ge 14 ] && break
  sleep 120
done
