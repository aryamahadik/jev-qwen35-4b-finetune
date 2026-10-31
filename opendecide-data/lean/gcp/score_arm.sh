#!/bin/bash
# Fetch one PRISM-X arm's predictions from the L4 VM and score them against arm E (and the arm with PRISM-X off).
# Usage: gcp/score_arm.sh H   (run from lean/)
A=$1; N=q35_2b_arm$A; P=system-one-509903; Z=us-central1-a; PY=../.venv/bin/python
for s in dev devzs devp_card dev_nc hard_dev pg_dev taskbank_dev dev_claims dev_negwords breadth_dev eval_jagged eval_opi eval_redef; do
  mkdir -p preds_$s
  gcloud compute scp "od-l4:~/lean/preds_$s/$N*" preds_$s/ --zone $Z --project $P --quiet >/dev/null 2>&1
done
gcloud compute scp "od-l4:~/lean/logs/train_$N.log" "od-l4:~/lean/logs/$N.json" logs/ --zone $Z --project $P --quiet >/dev/null 2>&1
echo "== dev gate vs E (dev-select / dev-confirm, need +1.3 for I; H needs >= -0.5)"
$PY gate_dev.py $N q35_2b_armE 2>&1 | tail -12
echo "== jagged audit (ASR), E / arm / arm-off"
$PY score_jagged.py q35_2b_armE q35_2b_armE $N ${N}_nopx 2>&1 | tail -6
echo "== OPI injection (ASR)"
$PY score_opi.py q35_2b_armE q35_2b_armE $N ${N}_nopx 2>&1 | tail -6
echo "== definition overwrite (ASR)"
$PY score_redef.py q35_2b_armE $N ${N}_nopx 2>&1 | tail -6
echo "== per-split accuracy"
$PY quick_acc.py q35_2b_armE,$N dev_nc,hard_dev,pg_dev,taskbank_dev,breadth_dev,devzs,devp_card,dev 2>&1 | tail -14
echo "== PRISM-X parts at the end of training"
python3 -c "import json; m=json.load(open('logs/$N.json')); print(m.get('prism_x',{}).get('final'), 'minutes', m.get('minutes'))" 2>&1
