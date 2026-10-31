#!/bin/zsh
# usage: draws.sh BASE K1 K2 ...   (W8: A50 pooled QC draws, plan seed t37b-i4-b<BASE>-d<K>)
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build
B=$1; shift
for K in "$@"; do
  nice -n 10 /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B -m t37b.run_pilot_i3 --out pilot_i4_b${B}_d${K} --plan-seed t37b-i4-b${B}-d${K} > t37b/_w8/draw_${B}_${K}.out 2>&1
done
