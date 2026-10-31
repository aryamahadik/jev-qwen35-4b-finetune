#!/bin/bash
# PRISM-X arms H -> I -> J on the Google L4, matched to arm E (same data, seed, 800 steps, loss, teacher; PRISM_X.md).
# Resumable: finished arms are skipped and an interrupted arm resumes from its 15-minute checkpoint.
# The VM shuts itself down at the end (or on the first failure), so billing stops.
cd ~/lean || exit 1
PY=~/od/bin/python
LOG=logs/prismx_chain.log
SPLITS=dev,devzs,devp_card,dev_nc,hard_dev,pg_dev,taskbank_dev,dev_claims,dev_negwords,breadth_dev,eval_jagged,eval_opi,eval_redef
EX='{"lam_inv": 1.0, "sym_cons": true, "perm_twin": 0.3, "lam_p": 0.5, "micro_tokens": 16384, "ablate_splits": ["eval_jagged", "eval_opi", "eval_redef", "dev_nc"]}'
mkdir -p logs
for ARM in ${ARMS:-H I J}; do
  if [ -f "preds_eval_redef/q35_2b_arm${ARM}.jsonl" ]; then echo "SKIP $ARM (done) $(date -u +%FT%TZ)" >> $LOG; continue; fi
  echo "START $ARM $(date -u +%FT%TZ)" >> $LOG
  if $PY od_gcp.py train --name "q35_2b_arm$ARM" --arm "$ARM" --base Qwen/Qwen3.5-2B --r 32 --batch 16 --lr 1e-4 \
       --lam 1.0 --beta 1.0 --kd 0.5 --epochs 0.2147 --style cygnet --log-every 25 \
       --train-file train_prism_arms.jsonl --rel-file train_prism_arms_relations.jsonl --splits $SPLITS \
       --extra "$EX" >> "logs/train_q35_2b_arm$ARM.log" 2>&1; then
    echo "DONE $ARM $(date -u +%FT%TZ)" >> $LOG
  else
    echo "FAIL $ARM $(date -u +%FT%TZ) (see logs/train_q35_2b_arm$ARM.log)" >> $LOG
    break
  fi
done
echo "CHAIN END $(date -u +%FT%TZ)" >> $LOG
[ -n "$NO_SHUTDOWN" ] || sudo shutdown -h now
