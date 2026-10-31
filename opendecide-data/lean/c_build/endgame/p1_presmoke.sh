#!/bin/bash
# RUNBOOK P1: pipeline pre-smoke (A20 d) on jaypatil-duke CREDIT (owner decision 1), hard cap 14 min (= $0.95 at $4.09/h).
#   nohup bash c_build/endgame/p1_presmoke.sh > c_build/endgame/logs/p1_presmoke.log 2>&1 &      (from lean/)
# Runs only if spend_guard says the credit keeps the $12 final-test reserve after the $1 cap and nothing unexplained
# (e.g. rrun) is running there; else prints "P1 REFUSED" and exits 1 with nothing charged. The Modal client is NOT
# detached: spend_guard interrupts it at 14 min and sends `modal app stop`; a dead client also stops the app.
set -uo pipefail
cd "$(dirname "$0")/../.."          # lean/
PY=../.venv/bin/python; M=../.venv/bin/modal; E=c_build/endgame
P=jaypatil-duke
$PY $E/spend_guard.py check $P --cap-usd 1 --reserve 12 || { echo "P1 REFUSED (nothing charged): wait for rrun to stop, or owner"; exit 1; }
cleanup() { rm -f data/c_presmoke_r1.jsonl data/c_presmoke_rel_r1.jsonl; }     # never leave them in data/
trap cleanup EXIT
cp $E/presmoke/c_presmoke_r1.jsonl $E/presmoke/c_presmoke_rel_r1.jsonl data/   # top level: the image uploads it
$PY $E/spend_guard.py ledger $P "P1 pre-smoke (A20 d): BEFORE (cap 14 min, <= \$0.95)" --payer credit
$PY $E/spend_guard.py run --profile $P --what presmoke --cap-min 14 -- \
  $M run modal_od.py::speed --config c_build/endgame/presmoke/q35_4b_c_presmoke.json \
  --micro-tokens 8192 --steps 40 --skip 5 --override '{"log_every": 1}'
rc=$?
cleanup
MODAL_PROFILE=$P $M volume rm -r opendecide models/pilot_speed_h100_mt8192_log_every-1 || true
$PY $E/spend_guard.py ledger $P "P1 pre-smoke (A20 d): AFTER (client exit $rc)" --payer credit
[ $rc -eq 0 ] && echo "P1 DONE" || echo "P1 FAILED (exit $rc; 124 = the 14-min cap fired)"
exit $rc
