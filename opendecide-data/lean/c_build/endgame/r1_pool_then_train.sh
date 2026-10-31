#!/bin/bash
# Owner-authorised (A34 push): check the whole replay pool + public-3 once with G13 (--final on a superset file),
# drop every hit, re-mix with only clean rows, run the real final-mix G13, then fill_config -> preflight -> r1_chain.
set -u
cd "$(dirname "$0")/../.."
PY=../.venv/bin/python; E=c_build/endgame; D=$HOME/.cache/opendecide_ext/bigpat_full; R=logs/decontam_counts
g13final() { G13_BIGPAT_LOCAL="$D" G13_BIGPAT_STREAM=1 PYTHONUNBUFFERED=1 nice -n 10 $PY c_build/decontam_g13.py --final > "$1" 2>&1; }
ndrops() { $PY -c "import json;print(len(json.load(open('$R/final_mix_r1.json')).get('drop_ids',[])))"; }
mix() { nice -n 5 $PY c_build/mixer.py --final --include F3 F5 F7 public-3 --sealed-sha f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68 --decontam-drops $R/F3.json $R/F5.json $R/F7.json $R/packs.json $R/formats.json $R/sealed_drop_r1.json $R/pool_drops_r1.json > $E/logs/mixer_final_a34b.log 2>&1; grep -q "FINAL written" $E/logs/mixer_final_a34b.log; }
B=data/c_parts/firstpass_$(date +%Y%m%d_%H%M); mkdir -p $B; mv data/c_parts/c_train_r1.jsonl data/c_parts/c_rel_r1.jsonl data/c_parts/c_mix_r1_manifest.json $B/ 2>/dev/null; cp $R/final_mix_r1.json $R/final_mix_r1.firstpass.json
cat data/c_replay_r1_shards/shard_*.jsonl c_src/public/public-3/out/public3_rows_r1.jsonl c_src/public/public-3/out/public3_reserve.jsonl > data/c_parts/c_train_r1.jsonl
echo "POOL_CHECK_START $(date +%H:%M) rows $(wc -l < data/c_parts/c_train_r1.jsonl)"
g13final $R/run/pool_check_r1.log || { echo "POOL_G13_FAILED"; exit 1; }
$PY - <<PYEOF
import json
d=json.load(open('$R/final_mix_r1.json')); ids=sorted(set(d.get('drop_ids',[])))
json.dump({"set":"replay+public3 pool (superset --final run)","drop_ids":ids,"note":"A34 push 9 Oct: protective pool decontamination before re-mix"},open('$R/pool_drops_r1.json','w'))
print("POOL_DROPS", len(ids))
PYEOF
cp $R/final_mix_r1.json $R/final_mix_r1.poolcheck.json; rm -f data/c_parts/c_train_r1.jsonl
for it in 1 2; do
  mix || { echo "MIX_REFUSED it$it"; tail -n 6 $E/logs/mixer_final_a34b.log; exit 1; }
  echo "MIX_OK it$it $(date +%H:%M) $(grep 'FINAL written' $E/logs/mixer_final_a34b.log | cut -c1-80)"
  g13final $R/run/final_mix_r1_it$it.log || { echo "G13_FINAL_FAILED it$it"; exit 1; }
  nd=$(ndrops); echo "G13_FINAL it$it $(date +%H:%M) drop_ids=$nd"
  [ "$nd" = "0" ] && break
  $PY - <<PYEOF
import json
p=json.load(open('$R/pool_drops_r1.json')); f=json.load(open('$R/final_mix_r1.json'))
p['drop_ids']=sorted(set(p['drop_ids'])|set(f.get('drop_ids',[]))); json.dump(p,open('$R/pool_drops_r1.json','w')); print("POOL_DROPS now",len(p['drop_ids']))
PYEOF
done
[ "$(ndrops)" = "0" ] || { echo "STILL_HITS_AFTER_2_ITERATIONS"; exit 1; }
$PY $E/fill_config.py --dry-run > $E/logs/fill_config.log 2>&1 && $PY $E/fill_config.py >> $E/logs/fill_config.log 2>&1 || { echo "FILL_CONFIG_FAILED"; tail -n 5 $E/logs/fill_config.log; exit 1; }
$PY $E/r1_check.py preflight > $E/logs/r1_check_preflight.log 2>&1 || { echo "PREFLIGHT_REFUSED"; tail -n 15 $E/logs/r1_check_preflight.log; exit 1; }
echo "PREFLIGHT_GO $(date +%H:%M)"
nohup bash $E/r1_chain.sh > $E/logs/r1_chain.log 2>&1 &
sleep 180; echo "TRAINING_LAUNCHED $(date +%H:%M)"; tail -n 5 $E/logs/r1_chain.log
