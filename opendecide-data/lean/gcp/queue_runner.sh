#!/bin/bash
# PRISM-X job queue on the Google L4 (v2). Swapped in while a run is going, so experiments can be added overnight.
# logs/px_queue.txt lines: NAME|PRISM_X_JSON|EPOCHS[|EXTRA_JSON]
#   e.g.  q35_2b_armI|"I"|0.2147          q35_2b_armE_L4|null|0.2147|{"layout": "schema_branch_mark"}
# Every run is matched to arm E (same data, seed, loss, teacher, splits); only prism_x, the step count and EXTRA differ.
# Finished names go to logs/px_done.txt. A failed run is logged and the queue moves on. When the queue is empty the
# VM shuts itself down (unless logs/px_no_shutdown exists). First waits for any training already running and records
# its outcome.
cd ~/lean || exit 1
PY=~/od/bin/python
Q=logs/px_queue.txt; D=logs/px_done.txt; LOG=logs/prismx_chain.log
SPLITS=dev,devzs,devp_card,dev_nc,hard_dev,pg_dev,taskbank_dev,dev_claims,dev_negwords,breadth_dev,eval_jagged,eval_opi,eval_redef
touch $Q $D
while pgrep -f "od_gcp.py train" >/dev/null; do sleep 60; done
for NAME in $(grep -oE "^START [^ ]+" $LOG | awk '{print $2}'); do  # outcome of runs whose runner was swapped out
  N=$NAME; [ "$N" = H ] && N=q35_2b_armH
  grep -qE "^(DONE|FAIL|INTERRUPTED) ($NAME|$N) " $LOG && continue  # INTERRUPTED: the queue re-runs it (resumes)
  if [ -f "preds_eval_redef/$N.jsonl" ]; then echo "DONE $N $(date -u +%FT%TZ)" >> $LOG
  else echo "FAIL $N $(date -u +%FT%TZ) (see logs/train_$N.log)" >> $LOG; fi
  grep -F "$N|" $Q >> $D
done
while true; do
  line=$(grep -v '^[[:space:]]*$' $Q | grep -vxF -f $D | head -1)
  [ -z "$line" ] && break
  IFS='|' read -r NAME PX EPOCHS EXTRA <<< "$line"
  if [ -f "preds_eval_redef/$NAME.jsonl" ]; then echo "$line" >> $D; continue; fi
  EX=$(python3 -c 'import json,sys; e={"lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.3, "lam_p": 0.5, "micro_tokens": 16384, "ablate_splits": ["eval_jagged", "eval_opi", "eval_redef", "dev_nc"], "prism_x": json.loads(sys.argv[1])}; e.update(json.loads(sys.argv[2] or "{}")); print(json.dumps(e))' "$PX" "$EXTRA")
  echo "START $NAME $(date -u +%FT%TZ) prism_x=$PX epochs=$EPOCHS extra=$EXTRA" >> $LOG
  if $PY od_gcp.py train --name "$NAME" --base Qwen/Qwen3.5-2B --r 32 --batch 16 --lr 1e-4 --lam 1.0 --beta 1.0 \
       --kd 0.5 --epochs "$EPOCHS" --style cygnet --log-every 25 --train-file train_prism_arms.jsonl \
       --rel-file train_prism_arms_relations.jsonl --splits $SPLITS --extra "$EX" >> "logs/train_$NAME.log" 2>&1; then
    echo "DONE $NAME $(date -u +%FT%TZ)" >> $LOG
  else
    echo "FAIL $NAME $(date -u +%FT%TZ) (see logs/train_$NAME.log)" >> $LOG
  fi
  echo "$line" >> $D
done
echo "CHAIN END $(date -u +%FT%TZ)" >> $LOG
[ -f logs/px_no_shutdown ] || sudo shutdown -h now
