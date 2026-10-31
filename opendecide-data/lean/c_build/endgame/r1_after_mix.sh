#!/bin/bash
set -u; cd "$(dirname "$0")/../.."
PY=../.venv/bin/python; E=c_build/endgame; D=$HOME/.cache/opendecide_ext/bigpat_full; R=logs/decontam_counts; LOG=$E/logs/mixer_final_a34c.log
MIXCMD="nice -n 5 $PY c_build/mixer.py --final --include F3 F5 F7 --sealed-sha f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68 --decontam-drops $R/F3.json $R/F5.json $R/F7.json $R/packs.json $R/formats.json $R/sealed_drop_r1.json $R/pool_drops_r1.json"
for i in $(seq 1 480); do grep -q "FINAL written" $LOG 2>/dev/null && break; sleep 60; done
grep -q "FINAL written" $LOG || { echo "NO_FINAL_MIX_AFTER_8H"; exit 1; }
echo "MIX_OK $(date +%H:%M) $(grep 'FINAL written' $LOG | cut -c1-90)"
for it in 1 2 3; do
  G13_BIGPAT_LOCAL="$D" G13_BIGPAT_STREAM=1 PYTHONUNBUFFERED=1 nice -n 10 $PY c_build/decontam_g13.py --final > $R/run/final_mix_r1_c$it.log 2>&1 || { echo "G13_FAILED it$it"; exit 1; }
  nd=$($PY -c "import json;print(len(json.load(open('$R/final_mix_r1.json')).get('drop_ids',[])))"); echo "G13_FINAL it$it $(date +%H:%M) drop_ids=$nd"
  [ "$nd" = "0" ] && break
  $PY -c "
import json
p=json.load(open('$R/pool_drops_r1.json')); f=json.load(open('$R/final_mix_r1.json'))
p['drop_ids']=sorted(set(p['drop_ids'])|set(f.get('drop_ids',[]))); json.dump(p,open('$R/pool_drops_r1.json','w'))"
  $MIXCMD > $LOG 2>&1; grep -q "FINAL written" $LOG || { echo "REMIX_REFUSED it$it"; tail -n 6 $LOG; exit 1; }
done
[ "$nd" = "0" ] || { echo "STILL_HITS"; exit 1; }
$PY $E/fill_config.py --dry-run > $E/logs/fill_config.log 2>&1 && $PY $E/fill_config.py >> $E/logs/fill_config.log 2>&1 || { echo "FILL_CONFIG_FAILED"; tail -n 5 $E/logs/fill_config.log; exit 1; }
$PY $E/r1_check.py preflight > $E/logs/r1_check_preflight.log 2>&1 || { echo "PREFLIGHT_REFUSED"; tail -n 15 $E/logs/r1_check_preflight.log; exit 1; }
echo "PREFLIGHT_GO $(date +%H:%M)"; nohup bash $E/r1_chain.sh > $E/logs/r1_chain.log 2>&1 &
sleep 180; echo "TRAINING_LAUNCHED $(date +%H:%M)"; tail -n 5 $E/logs/r1_chain.log
