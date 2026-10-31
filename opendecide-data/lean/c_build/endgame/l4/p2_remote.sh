#!/bin/bash
# P2-L4 (RUNBOOK P2; PREREG A21 d): C1 pre-reads on the Google L4 VM with the canonical od_gcp.py predict.
# Runs ON THE VM from ~/lean (pushed by c_build/endgame/l4/l4_p2_fam1.sh). Resumable: a finished read leaves
# logs/p2_l4/<tag>.done and is skipped. Sealed read: its log stays on the VM; only rc and seconds are recorded.
# After P2 it runs the FAM-1 step-0 read (recipe 5 / 11 step 6) if its inputs are on the VM (c_build/endgame/fam1/READY),
# waiting up to FAM1_WAIT_MIN for them. One GPU job at a time.
set -uo pipefail
cd ~/lean || exit 2
export HF_HUB_OFFLINE=1
PY=$HOME/od/bin/python
C="--name q35_4b_main500k --base Qwen/Qwen3.5-4B --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a --layout schema_branch_mark"
S9=dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev
L=logs/p2_l4; mkdir -p "$L"
SUITE_SHA=f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68

rec() { echo "{\"tag\": \"$1\", \"rc\": $2, \"start\": $3, \"end\": $(date +%s), \"host\": \"$(hostname)\"}" >> "$L/runs.jsonl"; }

run() {  # run <tag> <sealed 0|1> <predict args...>
  local tag=$1 sealed=$2; shift 2
  if [ -f "$L/$tag.done" ]; then echo "skip $tag (done)"; return 0; fi
  local t0; t0=$(date +%s)
  echo "start $tag $(date -u +%FT%TZ)"
  $PY od_gcp.py predict $C "$@" > "$L/$tag.log" 2>&1
  local rc=$?
  rec "$tag" "$rc" "$t0"
  if [ "$rc" = 0 ]; then touch "$L/$tag.done"; echo "done $tag $(( $(date +%s) - t0 ))s";
  elif [ "$sealed" = 1 ]; then echo "FAILED $tag rc=$rc type=$(grep -oE '^[A-Za-z_.]*(Error|Exception)' "$L/$tag.log" | tail -1)";
  else echo "FAILED $tag rc=$rc"; tail -5 "$L/$tag.log"; fi
  return $rc
}

ok=1
run pre 0 --splits $S9,eval_jagged,eval_opi --tag _pre || ok=0
run pre_perm 0 --splits $S9 --perm-seed 1 --tag _pre_perm || ok=0
run pre_served 0 --splits $S9 --tta-choice --tag _pre_served || ok=0
if echo "$SUITE_SHA  data/nd_suite_v2.jsonl" | sha256sum -c --status -; then
  run nd_pre 1 --splits nd_suite_v2 --tta-choice --tag _pre || ok=0      # sealed: never printed
else
  echo "FAILED nd_pre: suite sha256 != A15"; ok=0
fi
[ $ok = 1 ] && echo "P2 ALL DONE" > "$L/ALL.done"
echo "P2 status ok=$ok $(date -u +%FT%TZ)"

# ---- FAM-1 step 0 (report-only), after P2 on the same GPU
F=c_build/endgame/fam1
W=${FAM1_WAIT_MIN:-240}
for i in $(seq 1 "$W"); do [ -f "$F/READY" ] && break; sleep 60; done
if [ -f "$F/READY" ] && [ ! -f "$F/out/fam1_step0_c1.json" ]; then
  t0=$(date +%s); echo "start fam1 $(date -u +%FT%TZ)"
  $PY "$F/fam1_step0.py" read --rows "$F/fam1_rows.jsonl" --rels "$F/fam1_rels.jsonl" --out "$F/out" > "$F/fam1.log" 2>&1
  rc=$?; rec fam1 "$rc" "$t0"; echo "fam1 rc=$rc $(( $(date +%s) - t0 ))s"
fi
echo "QUEUE END $(date -u +%FT%TZ)" > "$L/QUEUE.end"
# backstop: if the Mac never fetches and stops the VM, shut down after 3 h idle (the stop happens on the Mac normally)
sleep 10800; sudo shutdown -h now
