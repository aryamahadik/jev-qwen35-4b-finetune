#!/bin/bash
# FAM-1 step-0 read on C1 (recipe 5 / 11 step 6; report-only), ON THE VM from ~/lean, after P2 has finished on the
# same GPU (waits for the "P2 status" line of logs/p2_l4/queue.log). Smoke first (tiny groups, no lookahead), then the
# full read. Writes c_build/endgame/fam1/out/{fam1_smoke.json,fam1_step0_c1.json} and fam1/FAM1.end.
set -uo pipefail
cd ~/lean || exit 2
export HF_HUB_OFFLINE=1
PY=$HOME/od/bin/python
F=c_build/endgame/fam1
sha256sum -c --quiet "$F/fam1_inputs.sha256" || { echo "FAM1 INPUTS sha256 FAILED" > "$F/FAM1.end"; exit 3; }
for i in $(seq 1 600); do grep -q "^P2 status" logs/p2_l4/queue.log 2>/dev/null && break; sleep 60; done
while pgrep -f "od_gcp.py predict" >/dev/null; do sleep 30; done
if [ ! -f "$F/out/fam1_smoke.json" ]; then
  $PY "$F/fam1_step0.py" read --smoke > "$F/fam1_smoke.log" 2>&1 || { echo "SMOKE FAILED rc=$?" > "$F/FAM1.end"; exit 4; }
fi
if [ ! -f "$F/out/fam1_step0_c1.json" ]; then
  $PY "$F/fam1_step0.py" read > "$F/fam1.log" 2>&1 || { echo "READ FAILED rc=$?" > "$F/FAM1.end"; exit 5; }
fi
echo "FAM1 DONE $(date -u +%FT%TZ)" > "$F/FAM1.end"
