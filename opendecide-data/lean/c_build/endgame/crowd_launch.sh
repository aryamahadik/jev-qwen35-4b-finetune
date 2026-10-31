#!/bin/bash
# RUNBOOK A0-A3: one guarded crowd-read launch (3 H100 apps: C1, 4B-E, base 4B) on a FREE-CREDIT profile.
#   bash c_build/endgame/crowd_launch.sh atmosphor F3 F10        (from lean/; prints GO lines or REFUSED and exits 1)
#   MODELS="q35_4b_pxE" bash c_build/endgame/crowd_launch.sh atmosphor F3   (relaunch only the model the cap stopped;
#                                                                           the cap is still sized for 3 containers)
# Every step stops the script on failure (set -e; REFUSED exits 1 before any upload or launch). The time cap is
# enforced ON THE SERVER (modal_crowd.py --max-min: function timeout + absolute deadline), not by a Mac-side sleep.
# Spend is logged in logs/budget_ledger.md before the launch and the launch in c_build/endgame/logs/launches.jsonl.
set -euo pipefail
cd "$(dirname "$0")/../.."          # lean/
PY=../.venv/bin/python; M=../.venv/bin/modal; E=c_build/endgame
P=${1:?profile}; shift
FAMS="$*"; [ -n "$FAMS" ] || { echo "usage: crowd_launch.sh <profile> F1 [F2 ...]"; exit 2; }
FL=$(echo $FAMS | tr ' ' ','); TAG=$(echo $FAMS | tr ' ' '_')
case "$P" in atmosphor|mahadikarya44) ;; *) echo "REFUSED: crowd reads run on atmosphor or mahadikarya44 free credit only (owner decisions 1 + 7 Oct 01:10 UTC); other payer = owner"; exit 1;; esac

# A1. shards (CPU) + estimate; keep a copy of the task file per launch
$PY c_build/crowd_select.py tasks --write-shards --fam $FAMS
cp c_build/crowd_r1/crowd_tasks_r1.json $E/logs/crowd_tasks_$TAG.json
# cap (exit 1 = REFUSED: the credit cannot pay, or an unexplained app is running) -> stop here, nothing uploaded
CAP_MIN=$($PY $E/crowd_cap.py $P) || { echo "REFUSED: crowd $FL on $P -> owner decides (spill to aryamhd card or wait)"; exit 1; }
echo "CAP_MIN=$CAP_MIN per container (3 x H100 at \$4.09/h <= \$$($PY -c "print(round(3*$CAP_MIN/60*4.09,2))"))"

# A2. upload shards (free)
for f in $FAMS; do MODAL_PROFILE=$P $M volume put -f opendecide data/c_crowd_r1_shards/$f crowd_r1_shards/$f; done

# A3. ledger (before), launch log, three detached reads with the server-side cap
$PY $E/spend_guard.py ledger $P "crowd $FL: BEFORE launch (cap $CAP_MIN min x 3 H100)" --payer credit
MODELS=${MODELS:-q35_4b_main500k q35_4b_pxE q35_4b_base0}
$PY $E/spend_guard.py record $P "crowd_$TAG" $CAP_MIN $(echo $MODELS | wc -w | tr -d ' ')
for m in $MODELS; do
  MODAL_PROFILE=$P nohup $M run --detach c_build/modal_crowd.py::crowd --name $m --fams $FL --max-min $CAP_MIN \
    > $E/logs/crowd_${TAG}_$m.log 2>&1 &
done
echo "LAUNCHED crowd $FL on $P: [$MODELS], each stops by itself within $CAP_MIN min (logs: $E/logs/crowd_${TAG}_*.log)"
