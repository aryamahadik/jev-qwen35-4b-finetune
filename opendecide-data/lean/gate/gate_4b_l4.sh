#!/bin/bash
# 4B ship gate on the Google L4 VM od-l4 (PREREG_FINAL.md sections 2-5; FINETUNE_PLAN.md 4.4-4.5).
# Read gate/RUNBOOK_4B_GATE.md first. Run every phase from anywhere; paths resolve to the lean/ folder.
#
#   Mac phases:  fetch PROFILE [final|sNNNNNN ...]   download the final adapter / snapshots from Modal (volume opendecide)
#                check                               verify the downloaded adapters (gate/check_adapter.py)
#                manifest                            sha256 manifests of code, data, stored REF preds and adapters
#                start | stop                        gcloud compute instances start/stop od-l4
#                push                                adapters + gate/ to the VM, then verify the manifests there
#                launch [job1|job2]                  start the VM job in the background (nohup), returns at once;
#                                                    STOP_BEFORE_SHIP / NO_SHUTDOWN set on the Mac are passed on
#                status                              tail the VM job's event log
#                pull                                preds, looks and logs back to the Mac (merges logs/ship_looks.jsonl)
#   VM phases:   vm-job1                             REF reads -> refparity -> C1, C2 reads -> c3trigger -> choice -> ship look(s)
#                vm-job2                             only after "C3 TRIGGER": C3 + merge checks + re-scored REF and C1
#   Mac (fallback, after "pull" of a job run with STOP_BEFORE_SHIP=1):
#                local-ship [job1|job2]              the choice and the ship look(s) on the Mac instead of the VM
#   any:         plan                                print every command of both jobs; runs nothing
#
# Env: NO_SHUTDOWN=1 keeps the VM up at the end of a VM job; PUSH_FIXES=1 lets "push" overwrite VM code/data files whose
# sha256 differs from the Mac's; STOP_BEFORE_SHIP=1 ends a VM job after its reads, parity look and C3 trigger (the
# choice and the ship looks then run on the Mac with "local-ship"; the 12 training files are then not needed on the VM);
# GATE_SIM=1 + PREDICT_CMD=... is the CPU simulation used by gate/tests/sim_gate.py. ALLOW_DIRTY=1 lets "manifest" run with
# uncommitted gate_dev.py / PREREG_FINAL.md (dry runs only: PREREG needs the amendment committed before job 1).
# Every look (refparity, c3trigger, ship) runs at most once: logs/gate4b/looks/<id>.done blocks a repeat.
set -uo pipefail

P=${GCP_PROJECT:-system-one-509903}; Z=${GCP_ZONE:-us-central1-a}; VM=${GCP_VM:-od-l4}
LEAN=${LEAN:-$(cd "$(dirname "$0")/.." && pwd)}
cd "$LEAN" || exit 1
if [ -z "${PY:-}" ]; then
  if [ -x "$HOME/od/bin/python" ]; then PY=$HOME/od/bin/python; else PY=$LEAN/../.venv/bin/python; fi
fi
PREDICT_CMD=${PREDICT_CMD:-"$PY od_gcp.py predict"}

RUN=q35_4b_main500k          # the main run: C1 = its final adapter
REFA=q35_4b_pxE              # REF adapter (4B-E)
FRESH=${REFA}_fresh          # job-1 fresh REF read (od_gcp predict --tag _fresh); never the stored name
FRESH2=${REFA}_fresh2        # job-2 fresh REF read (only if C3 triggers)
C1=$RUN; C2=${RUN}_c2; C3=${RUN}_c3; C1B=${RUN}_j2; C3W10=${RUN}_c3w10; C3W01=${RUN}_c3w01
SNAPS="s025888 s027411 s028934"   # int(f * 30457) for snap_fracs 0.85 / 0.90 / 0.95 (PREREG_FINAL.md 2, C2)
BASE=Qwen/Qwen3.5-4B
REV=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
LAYOUT=schema_branch_mark
SPLITS9=dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev
STD=$SPLITS9,eval_jagged,eval_opi,eval_redef   # eval_redef is report-only (not in the ship rule)
TRAIN12="v14_parts/golden_train train_v07 train_v08s2 train_v09s3 train_v10s4 train_v11 train_v11b train_v11c train_v13t train_prism_arms train_2b_kd train_2b_rest"
BACKUP=${BACKUP:-/Users/aryamahadik/Documents/jev/backups/modal_models/$RUN}
G=logs/gate4b

ts() { date -u +%FT%TZ; }
ev() { mkdir -p "$G"; echo "$(ts) $*" | tee -a "$G/events.log"; }
die() { local rc=$1; shift; ev "STOP($rc): $*"; vm_shutdown; exit "$rc"; }
jget() { "$PY" -c 'import json,sys; r=json.load(open(sys.argv[1])); v=eval(sys.argv[2], {}, {"r": r}); print(v)' "$1" "$2"; }
nlines() { wc -l < "$1" | tr -d ' '; }
sha_check() { if command -v sha256sum >/dev/null 2>&1; then sha256sum -c --quiet "$1"; else shasum -a 256 -c --quiet "$1"; fi; }
sha_of() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "$@"; else shasum -a 256 "$@"; fi; }
gssh() { gcloud compute ssh "$VM" --zone "$Z" --project "$P" --command "$1"; }
gscp() { gcloud compute scp --zone "$Z" --project "$P" --quiet "$@"; }
stored_ref() { "$PY" -c 'import sys; sys.path.insert(0, "."); import gate_dev; print(gate_dev.STORED_REF["4b"])'; }
vm_shutdown() {
  if [ -n "${NO_SHUTDOWN:-}" ] || [ -n "${GATE_SIM:-}" ] || [ "${PHASE:-}" != vm ]; then return 0; fi
  ev "VM shutdown"; sudo shutdown -h now
}

# ------------------------------------------------------------------------------------------------ reads (od_gcp predict)
out_name() { local n=$1; echo "${n//\//__}$2"; }
predict_cmd() {  # NAME TAG SPLITS PERM -> the exact command line (shared by the reads and "plan")
  local name=$1 tag=$2 splits=$3 perm=$4
  echo "HF_HUB_OFFLINE=1 $PREDICT_CMD --name $name --base $BASE --revision $REV --layout $LAYOUT --splits $splits${tag:+ --tag $tag}${perm:+ --perm-seed $perm}"
}
read_done() {  # OUT SPLITS: every split has the full pred file and its meta
  local out=$1 s
  for s in ${2//,/ }; do
    [ -f "preds_$s/$out.jsonl" ] && [ -f "preds_$s/$out.meta.json" ] || return 1
    [ "$(nlines "preds_$s/$out.jsonl")" = "$(nlines "data/$s.jsonl")" ] || return 1
  done
}
predict() {  # NAME TAG SPLITS PERM
  local out; out=$(out_name "$1" "$2")
  if read_done "$out" "$3"; then ev "READ $out: already complete, skipped"; return 0; fi
  [ -f "models/$1/train_meta.json" ] || die 3 "models/$1/train_meta.json missing (adapter not on the VM?)"
  ev "READ $out START ($3${4:+, perm-seed $4})"
  local t0; t0=$(date +%s)
  if ! env HF_HUB_OFFLINE=1 $PREDICT_CMD --name "$1" --base "$BASE" --revision "$REV" --layout "$LAYOUT" --splits "$3" \
        ${2:+--tag "$2"} ${4:+--perm-seed "$4"} >> "$G/reads.log" 2>&1; then
    die 4 "READ $out FAILED (see $G/reads.log)"
  fi
  read_done "$out" "$3" || die 4 "READ $out incomplete after the run"
  ev "READ $out DONE in $(( ($(date +%s) - t0) / 60 )) min"
}
read_std() { predict "$1" "$2" "$STD" ""; }        # 9 splits + jagged + OPI (+ redef, report only)
read_perm() { predict "$1" "$2" "$SPLITS9" 1; }    # the seeded permuted view (constraint f)
read_9() { predict "$1" "$2" "$SPLITS9" ""; }      # merge checks

materialize() {  # OUT WEIGHTS MEMBERS...
  local out=$1 w=$2; shift 2
  if [ -f "models/$out/train_meta.json" ] && [ -f "$G/built_$out.json" ]; then ev "BUILD $out: exists, skipped"; return 0; fi
  ev "BUILD $out = cat($w; $*)"
  "$PY" gate/materialize_cat.py --force --out "models/$out" --weights "$w" "$@" > "$G/built_$out.json" 2>> "$G/reads.log" \
    || die 5 "BUILD $out FAILED"
  ev "BUILD $out: $(cat "$G/built_$out.json")"
}
c2_members() { local s m=""; for s in $SNAPS; do m="$m models/$RUN/snaps/$s"; done; echo "$m models/$RUN"; }

# ------------------------------------------------------------------------------------------------ looks (gate_dev.py)
look() {  # ID MODE CAND REF: runs once; result JSON at $G/look_<ID>.json, text at $G/look_<ID>.txt
  local id=$1 mode=$2 cand=$3 ref=$4 j="$G/look_$1.json" sz=""
  mkdir -p "$G/looks"
  if [ -f "$G/looks/$id.done" ]; then ev "LOOK $id: already made ($(cat "$G/looks/$id.done")); not repeated"; return 0; fi
  [ "$mode" = ship ] && sz="--size 4b"
  ev "LOOK $id: gate_dev.py $cand $ref --mode $mode $sz"
  "$PY" gate_dev.py "$cand" "$ref" --mode "$mode" $sz --json "$j" > "$G/look_$id.txt" 2>&1
  local rc=$?
  cat "$G/look_$id.txt" >> "$G/looks.log"
  if [ $rc -ne 0 ]; then  # gate_dev stopped before a number (no ledger line): not a look; fix and re-run
    die 6 "LOOK $id: gate_dev.py stopped (exit $rc): $(tail -n 3 "$G/look_$id.txt" | tr '\n' ' ')"
  fi
  echo "$(ts) $mode $cand vs $ref" > "$G/looks/$id.done"
  tail -n 4 "$G/look_$id.txt" | sed 's/^/    /' | tee -a "$G/events.log"
}
parity_gate() {  # ID FRESH: stop unless the parity look passed and counts
  local id=$1 j="$G/look_$1.json"
  if [ "$(jget "$j" 'r["pass"]')" != True ]; then
    die 10 "REF PARITY FAILED for $2 (PREREG_FINAL.md 4): stop and consult the owner before any ship look. No candidate was read in this job after it."
  fi
  if [ "$(jget "$j" 'r["counts"]')" != True ]; then
    die 11 "REF parity passed but does not count: $(jget "$j" 'r["why_not"]')"
  fi
}
verdict_of() { echo "$(jget "$G/look_$1.json" 'r["verdict"]')|$(jget "$G/look_$1.json" 'r["final"]')"; }

# ------------------------------------------------------------------------------------------------ VM preflight
vm_preflight() {
  ev "PREFLIGHT in $LEAN (python $PY)"
  [ -f gate/manifest_4b.sha256 ] && [ -f gate/manifest_adapters.sha256 ] || die 2 "gate/manifest_*.sha256 missing: run 'manifest' and 'push' on the Mac"
  local man=gate/manifest_4b.sha256
  if [ -n "${STOP_BEFORE_SHIP:-}" ]; then grep -v -E "  data/(v14_parts/golden_train|train_)" "$man" > "$G/manifest_noship.sha256"; man=$G/manifest_noship.sha256; fi
  sha_check "$man" > "$G/preflight_sha.txt" 2>&1 \
    || die 2 "code/data/stored-preds sha256 differ from the Mac's (see $G/preflight_sha.txt); push with PUSH_FIXES=1"
  sha_check gate/manifest_adapters.sha256 >> "$G/preflight_sha.txt" 2>&1 \
    || die 2 "adapter sha256 differ from the Mac's (see $G/preflight_sha.txt)"
  local s f
  for s in ${STD//,/ }; do [ -f "data/$s.jsonl" ] || die 2 "data/$s.jsonl missing"; done
  if [ -z "${STOP_BEFORE_SHIP:-}" ]; then
    for f in $TRAIN12; do [ -f "data/$f.jsonl" ] || die 2 "data/$f.jsonl missing: the ship verdict would be NOT FINAL (or use STOP_BEFORE_SHIP=1)"; done
  fi
  for s in $SNAPS; do [ -f "models/$RUN/snaps/$s/train_meta.json" ] || die 2 "models/$RUN/snaps/$s missing (C2 needs it)"; done
  [ -f "models/$RUN/train_meta.json" ] || die 2 "models/$RUN/train_meta.json missing (the final adapter is not on the VM)"
  [ -f "models/$REFA/adapter_model.safetensors" ] || die 2 "models/$REFA missing"
  if [ -z "${GATE_SIM:-}" ]; then
    [ -f "$HOME/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/$REV/config.json" ] \
      || die 2 "base revision $REV is not in the HF cache (HF_HUB_OFFLINE=1 would fail)"
    if pgrep -f "od_gcp.py" >/dev/null; then die 2 "another od_gcp.py job is running on this VM: one job at a time"; fi
    if [ -n "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null)" ]; then die 2 "the GPU is busy"; fi
    local free; free=$(df -Pk . | awk 'NR==2 {print int($4/1048576)}')
    [ "$free" -ge 4 ] || die 2 "only ${free} GB free on disk (need >= 4 GB for C2/C3 folders and preds)"
  fi
  STORED=$(stored_ref) || die 2 "cannot import gate_dev.py"
  ev "gate_dev.py sha256 $(sha_of gate_dev.py | cut -c1-16)...; STORED_REF[4b] = $STORED"
  for s in ${SPLITS9//,/ }; do [ -f "preds_$s/$STORED.jsonl" ] || die 2 "stored REF preds_$s/$STORED.jsonl missing"; done
  # gate_dev's own size check on the stored REF metas: the frozen tool refuses q35_4b_pxE (its metas say Qwen3.5-2B)
  if ! "$PY" - "$FRESH" "$STORED" > "$G/preflight_size.txt" 2>&1 <<'EOF'
import argparse, sys
sys.path.insert(0, ".")
import gate_dev as g
g._MODE = "refparity"
g.resolve_size(argparse.Namespace(cand=sys.argv[1], ref=sys.argv[2], size="4b", splits=g.SPLITS))
print("size check OK")
EOF
  then
    die 2 "gate_dev.py cannot run --mode refparity against $STORED: $(cat "$G/preflight_size.txt"). Adopt prereg_drafts/AMENDMENT_A7_refparity.md first."
  fi
  if [ "$STORED" = "$REFA" ]; then
    ev "WARNING: the stored REF is the in-process read $REFA. The 30 Sep od_gcp predict read of 4B-E (q35_4b_pxE_parity) misses its max |dp| bar (max 0.0986 > 0.05; 3 of 8,143 rows above 0.05); this job will probably stop at the parity look."
  fi
  ev "PREFLIGHT OK"
}

# ------------------------------------------------------------------------------------------------ VM job 1
vm_job1() {
  PHASE=vm; mkdir -p "$G"
  ev "===== JOB 1 START (REF $REFA as $FRESH; C1 $C1; C2 $C2)"
  vm_preflight
  # 1. REF first, ALL of its reads (the parity look fingerprints every REF pred file, _perm included)
  read_std "$REFA" _fresh
  read_perm "$REFA" _fresh_perm
  # 2. parity stop (PREREG 4) before any candidate is read
  look refparity1 refparity "$FRESH" "$STORED"
  parity_gate refparity1 "$FRESH"
  # 3. candidates: C1 then C2 (exact cat average, materialized so it is an ordinary predict read)
  read_std "$C1" ""
  read_perm "$C1" _perm
  materialize "$C2" 0.25,0.25,0.25,0.25 $(c2_members)
  read_std "$C2" ""
  read_perm "$C2" _perm
  # 4. C3 trigger (not a ship look)
  look c3trigger c3trigger "$C1" "$FRESH"
  if [ "$(jget "$G/look_c3trigger.json" 'r["trigger"]')" = True ]; then
    ev "C3 TRIGGER: C1 fails $(jget "$G/look_c3trigger.json" 'r["failed"]') on dev-select. No ship look in job 1; run 'launch job2'."
    summary job1-c3-trigger; vm_shutdown; return 0
  fi
  if [ -n "${STOP_BEFORE_SHIP:-}" ]; then
    ev "STOP_BEFORE_SHIP: reads, parity look and C3 trigger done. Next on the Mac: pull, then local-ship job1"
    summary job1-reads-done; vm_shutdown; return 0
  fi
  # 5. choose one candidate (replacement rule), 6. ship look(s)
  job1_choice
}
job1_choice() { choose_and_look "$G/replacement.json" --c1 "$C1" --alt "$C2"; }

choose_and_look() {  # JSON then the replacement_rule.py arguments
  local j=$1; shift
  ev "CHOICE: gate/replacement_rule.py $*"
  "$PY" gate/replacement_rule.py "$@" --json "$j" > "$G/replacement.txt" 2>&1
  local rc=$?
  sed 's/^/    /' "$G/replacement.txt" | tee -a "$G/events.log"
  [ $rc -eq 3 ] && { summary owner-choice; die 12 "two alternatives qualify: the owner chooses (PREREG does not say)"; }
  [ $rc -eq 0 ] || die 7 "replacement_rule.py failed (exit $rc)"
  local chosen; chosen=$(jget "$j" 'r["chosen"]')
  local ref=$FRESH; [ "$chosen" = "$C3" ] && ref=$FRESH2
  look ship1 ship "$chosen" "$ref"
  local v1; v1=$(verdict_of ship1)
  ev "SHIP LOOK 1: $chosen vs $ref -> ${v1%%|*} (final ${v1##*|})"
  if [ "${v1##*|}" != True ]; then summary not-final; die 13 "ship look 1 is NOT FINAL: it decides nothing; consult the owner"; fi
  if [ "${v1%%|*}" = SHIP ]; then summary "ship:$chosen"; vm_shutdown; return 0; fi
  if [ "$chosen" != "$C1" ]; then
    look ship2 ship "$C1" "$FRESH"
    local v2; v2=$(verdict_of ship2)
    ev "SHIP LOOK 2: $C1 vs $FRESH -> ${v2%%|*} (final ${v2##*|})"
    if [ "${v2##*|}" != True ]; then summary not-final; die 13 "ship look 2 is NOT FINAL: consult the owner"; fi
    if [ "${v2%%|*}" = SHIP ]; then summary "ship:$C1"; vm_shutdown; return 0; fi
  fi
  summary "fallback:$REFA"; vm_shutdown
}

# ------------------------------------------------------------------------------------------------ VM job 2 (C3)
vm_job2() {
  PHASE=vm; mkdir -p "$G"
  [ -f "$G/looks/c3trigger.done" ] && [ "$(jget "$G/look_c3trigger.json" 'r["trigger"]')" = True ] \
    || die 2 "job 2 runs only after job 1's C3 TRIGGER (PREREG_FINAL.md 2)"
  ev "===== JOB 2 START (C3 = 0.75 $RUN + 0.25 $REFA; REF re-read as $FRESH2; C1 re-read as $C1B)"
  vm_preflight
  materialize "$C3" 0.75,0.25 "models/$RUN" "models/$REFA"
  materialize "$C3W10" 1,0 "models/$RUN" "models/$REFA"
  materialize "$C3W01" 0,1 "models/$RUN" "models/$REFA"
  read_std "$REFA" _fresh2
  read_perm "$REFA" _fresh2_perm
  look refparity2 refparity "$FRESH2" "$STORED"
  parity_gate refparity2 "$FRESH2"
  read_std "$RUN" _j2
  read_9 "$C3W10" ""
  "$PY" gate/merge_check.py "$C3W10" "$C1B" --json "$G/merge_check_10.json" 2>&1 | tee -a "$G/events.log"
  [ -f "$G/merge_check_10.json" ] || die 8 "merge check (1,0) did not run (see above)"
  read_9 "$C3W01" ""
  "$PY" gate/merge_check.py "$C3W01" "$FRESH2" --json "$G/merge_check_01.json" 2>&1 | tee -a "$G/events.log"
  [ -f "$G/merge_check_01.json" ] || die 8 "merge check (0,1) did not run (see above)"
  if merge_ok; then
    read_std "$C3" ""
    read_perm "$C3" _perm
  fi
  if [ -n "${STOP_BEFORE_SHIP:-}" ]; then
    ev "STOP_BEFORE_SHIP: job-2 reads, parity look and merge checks done. Next on the Mac: pull, then local-ship job2"
    summary job2-reads-done; vm_shutdown; return 0
  fi
  job2_choice
}
merge_ok() { [ -f "$G/merge_check_10.json" ] && [ -f "$G/merge_check_01.json" ] \
  && [ "$(jget "$G/merge_check_10.json" 'r["pass"]')" = True ] && [ "$(jget "$G/merge_check_01.json" 'r["pass"]')" = True ]; }
job2_choice() {
  if merge_ok; then
    choose_and_look "$G/replacement.json" --c1 "$C1" --alt "$C2" --c3 "$C3" --c3-c1 "$C1B" --c3-ref "$FRESH2"
  else
    ev "MERGE CHECK FAILED: C3 is not a candidate (PREREG 2); the choice is between C1 and C2 of job 1"
    choose_and_look "$G/replacement.json" --c1 "$C1" --alt "$C2"
  fi
}
local_ship() {  # job1|job2, on the Mac after "pull": the same choice and looks, logged to the Mac's ledger
  local j=${1:-job1} f
  [ -f "$G/looks/refparity1.done" ] && [ -f "$G/looks/c3trigger.done" ] || { echo "pull the VM results first"; exit 1; }
  for f in $TRAIN12; do [ -f "data/$f.jsonl" ] || { echo "data/$f.jsonl missing here"; exit 1; }; done
  STORED=$(stored_ref)
  if [ "$j" = job2 ]; then
    [ -f "$G/looks/refparity2.done" ] || { echo "job 2 has not run"; exit 1; }
    job2_choice
  else
    [ "$(jget "$G/look_c3trigger.json" 'r["trigger"]')" = True ] && { echo "C3 TRIGGER: run job 2 first"; exit 1; }
    job1_choice
  fi
}

# ------------------------------------------------------------------------------------------------ summary
summary() {
  "$PY" - "$1" "$G" "$C1" "$FRESH" <<'EOF' | tee -a "$G/events.log"
import json, sys
from pathlib import Path
outcome, G, c1, fresh = sys.argv[1:5]
G = Path(G)
looks = {}
for p in sorted(G.glob("look_*.json")):
    r = json.loads(p.read_text())
    k = p.stem[5:]
    if r["mode"] == "ship":
        looks[k] = {"cand": r["cand"], "ref": r["ref"], "verdict": r["verdict"], "final": r["final"],
                    "primary": {x: r["primary"][x] for x in ("diff", "lo", "hi", "pass")}, "failed": r["failed"],
                    "unmeasured": r["unmeasured"], "not_final": r["not_final"]}
    elif r["mode"] == "refparity":
        looks[k] = {x: r[x] for x in ("fresh", "stored", "pass", "counts", "agree", "mean_dp", "max_dp", "acc_diff")}
    else:
        looks[k] = {x: r[x] for x in ("cand", "ref", "trigger", "failed", "final")}
rep = G / "replacement.json"
decision = {"ship:": "SHIP {}", "fallback:": "FALLBACK: ship REF {} (PREREG 5.7)"}
text = next((v.format(outcome.split(":", 1)[1]) for k, v in decision.items() if outcome.startswith(k)), outcome)
out = {"outcome": outcome, "decision": text, "looks": looks,
       "replacement": json.loads(rep.read_text()) if rep.exists() else None}
if outcome.startswith("ship:"):  # report only: teacher switch rule (PREREG 6 (c)) needs >= +1.0 pp on dev-select
    sys.path.insert(0, ".")
    import gate_dev as g
    shipped = outcome.split(":", 1)[1]
    ref = next((v["ref"] for v in looks.values() if v.get("cand") == shipped and "verdict" in v), fresh)
    rows = g.complete_rows(g.SPLITS.split(","), shipped, ref)
    sel = [x for x in rows if x["half"] == "select"]
    out["teacher_switch_c_dev_select_diff_pp"] = 100 * (sum(x["ok_c"] for x in sel) - sum(x["ok_r"] for x in sel)) / len(sel)
(G / "summary.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"SUMMARY: {text}")
for k, v in looks.items():
    print(f"   {k}: {json.dumps(v)[:300]}")
EOF
}

# ------------------------------------------------------------------------------------------------ Mac phases
mac_fetch() {  # PROFILE [final|sNNNNNN ...]: Modal volume -> $BACKUP (one local copy, models policy)
  local prof=$1; shift
  local items="$*"; [ -n "$items" ] || items="final $SNAPS"
  local M=$LEAN/../.venv/bin/modal stage it f
  stage=$LEAN/handoff/main500k_gate_dl; mkdir -p "$stage" "$BACKUP/snaps"
  for it in $items; do
    if [ "$it" = final ]; then
      mkdir -p "$stage/final"
      for f in adapter_config.json adapter_model.safetensors tokenizer.json tokenizer_config.json chat_template.jinja train_meta.json; do
        MODAL_PROFILE=$prof "$M" volume get opendecide "models/$RUN/$f" "$stage/final/" || { echo "fetch failed: $f"; return 1; }
      done
      "$PY" gate/check_adapter.py "$stage/final" || { echo "final adapter check FAILED (kept in $stage/final)"; return 1; }
      for f in "$stage"/final/*; do mv "$f" "$BACKUP/"; done
    else
      [ -e "$BACKUP/snaps/$it" ] && { echo "$BACKUP/snaps/$it exists, skipped"; continue; }
      MODAL_PROFILE=$prof "$M" volume get opendecide "models/$RUN/snaps/$it" "$stage/" || { echo "fetch failed: $it"; return 1; }
      "$PY" gate/check_adapter.py "$stage/$it" --snapshot "$((10#${it#s}))" || { echo "snapshot $it check FAILED"; return 1; }
      mv "$stage/$it" "$BACKUP/snaps/$it"
    fi
  done
  echo "fetched into $BACKUP"
}

mac_check() {
  local rc=0 s
  "$PY" gate/check_adapter.py "$BACKUP" || rc=1
  for s in $SNAPS; do "$PY" gate/check_adapter.py "$BACKUP/snaps/$s" --snapshot "$((10#${s#s}))" || rc=1; done
  "$PY" -c 'n=30457; print("snapshot steps", sorted(int(f*n) for f in (0.85, 0.9, 0.95)))'
  return $rc
}

mac_manifest() {  # paths relative to lean/ (the same on the VM: ~/lean)
  local stored s f m=gate/manifest_4b.sha256 ma=gate/manifest_adapters.sha256
  # PREREG_FINAL.md: an amendment (and the gate_dev.py it changes) must be COMMITTED before the first candidate read.
  if [ -z "${ALLOW_DIRTY:-}" ] && git -C "$LEAN" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    local dirty; dirty=$(git -C "$LEAN" status --porcelain -- gate_dev.py PREREG_FINAL.md ship_unseen_sources.json \
      tests/test_ship_rule.py tests/test_amendment_A7.py)
    if [ -n "$dirty" ]; then
      echo "uncommitted changes to the pre-registered gate files (commit the amendment first, or ALLOW_DIRTY=1 for a dry run):"
      echo "$dirty" | sed 's/^/   /'; return 1
    fi
    echo "gate files committed (HEAD $(git -C "$LEAN" rev-parse --short HEAD); gate_dev.py $(sha_of gate_dev.py | cut -c1-16)...)"
  fi
  stored=$(stored_ref)
  {
    sha_of gate_dev.py od_gcp.py decoder_io.py prism_x.py writeblock.py ship_unseen_sources.json \
      gate/materialize_cat.py gate/replacement_rule.py gate/merge_check.py gate/check_adapter.py gate/gate_4b_l4.sh
    for s in ${STD//,/ }; do sha_of "data/$s.jsonl"; done
    for s in ${SPLITS9//,/ }; do [ -f "data/${s}_relations.jsonl" ] && sha_of "data/${s}_relations.jsonl"; done
    for f in $TRAIN12; do sha_of "data/$f.jsonl"; done
    for s in ${SPLITS9//,/ }; do sha_of "preds_$s/$stored.jsonl" "preds_$s/$stored.meta.json"; done
  } > "$m" || return 1
  {
    (cd "$BACKUP" && sha_of adapter_config.json adapter_model.safetensors train_meta.json chat_template.jinja) | sed "s|  |  models/$RUN/|"
    for s in $SNAPS; do
      (cd "$BACKUP/snaps/$s" && sha_of adapter_config.json adapter_model.safetensors train_meta.json) | sed "s|  |  models/$RUN/snaps/$s/|"
    done
    if [ -d "models/$REFA" ]; then sha_of "models/$REFA/adapter_config.json" "models/$REFA/adapter_model.safetensors"
    else (cd "${REF_BACKUP:-/Users/aryamahadik/Documents/jev/backups/gcp_models/$REFA}" && sha_of adapter_config.json adapter_model.safetensors) | sed "s|  |  models/$REFA/|"; fi
  } > "$ma" || return 1
  echo "wrote $m ($(nlines "$m") files, stored REF $stored) and $ma ($(nlines "$ma") files)"
}

mac_push() {
  [ -f gate/manifest_4b.sha256 ] && [ -f gate/manifest_adapters.sha256 ] || { echo "run 'manifest' first"; return 1; }
  gscp --recurse "$LEAN/gate" "$VM:~/lean/" || return 1   # tools + manifests first
  if gssh "test -e ~/lean/models/$RUN"; then
    gssh "cd ~/lean && sha256sum -c --quiet gate/manifest_adapters.sha256" \
      || { echo "~/lean/models/$RUN exists on the VM but differs from the Mac's: check it by hand (not overwritten)"; return 1; }
    echo "adapters already on the VM and verified"
  else
    gscp --recurse "$BACKUP" "$VM:~/lean/models/" || return 1   # -> ~/lean/models/$RUN (final + snaps/s0xxxxx)
  fi
  local bad
  bad=$(gssh "cd ~/lean && (sha256sum -c --quiet gate/manifest_4b.sha256; sha256sum -c --quiet gate/manifest_adapters.sha256) 2>&1 | grep -E 'FAILED|No such' | sed 's/:.*//'" | tr -d '\r')
  if [ -z "$bad" ]; then echo "VM manifests OK"; return 0; fi
  echo "files that differ or are missing on the VM:"; echo "$bad" | sed 's/^/   /'
  if [ -z "${PUSH_FIXES:-}" ]; then echo "re-run with PUSH_FIXES=1 to copy the Mac's versions to the VM"; return 1; fi
  local f
  for f in $bad; do
    gssh "mkdir -p ~/lean/$(dirname "$f")" && gscp "$LEAN/$f" "$VM:~/lean/$f" || return 1
  done
  gssh "cd ~/lean && sha256sum -c --quiet gate/manifest_4b.sha256 && sha256sum -c --quiet gate/manifest_adapters.sha256" && echo "VM manifests OK after fixes"
}

mac_pull() {
  local d n
  for d in $(echo "$STD" | tr ',' '\n' | sed 's/^/preds_/'); do
    mkdir -p "$d"
    for n in "$FRESH" "$FRESH2" "$C1" "$C2" "$C3" "$C3W10" "$C3W01"; do
      gscp "$VM:~/lean/$d/$n*" "$d/" >/dev/null 2>&1 || true
    done
  done
  mkdir -p "$G" logs
  gscp --recurse "$VM:~/lean/$G/*" "$G/" || echo "no $G on the VM?"
  gscp "$VM:~/lean/logs/ship_looks.jsonl" logs/ship_looks.vm.jsonl || return 1
  touch logs/ship_looks.jsonl
  "$PY" - <<'EOF'
from pathlib import Path
mac, vm = Path("logs/ship_looks.jsonl"), Path("logs/ship_looks.vm.jsonl")
have = set(mac.read_text().splitlines())
new = [l for l in vm.read_text().splitlines() if l.strip() and l not in have]
with open(mac, "a") as f:
    f.writelines(l + "\n" for l in new)
print(f"logs/ship_looks.jsonl: {len(new)} new look(s) appended from the VM")
EOF
  [ -f "$G/summary.json" ] && jget "$G/summary.json" 'r["decision"]'
}

plan() {
  local stored; stored=$(stored_ref 2>/dev/null || echo "<STORED_REF[4b]>")
  cat <<EOF
# JOB 1 on od-l4 (~/lean, python ~/od/bin/python). Estimated 3.4 L4-hours.
$(predict_cmd "$REFA" _fresh "$STD" "")
$(predict_cmd "$REFA" _fresh_perm "$SPLITS9" 1)
$PY gate_dev.py $FRESH $stored --mode refparity --json $G/look_refparity1.json     # FAIL -> stop, consult owner
$(predict_cmd "$C1" "" "$STD" "")
$(predict_cmd "$C1" _perm "$SPLITS9" 1)
$PY gate/materialize_cat.py --force --out models/$C2 --weights 0.25,0.25,0.25,0.25$(c2_members)
$(predict_cmd "$C2" "" "$STD" "")
$(predict_cmd "$C2" _perm "$SPLITS9" 1)
$PY gate_dev.py $C1 $FRESH --mode c3trigger --json $G/look_c3trigger.json         # TRIGGER -> job 2, no ship look
$PY gate/replacement_rule.py --c1 $C1 --alt $C2 --json $G/replacement.json        # prints CHOSEN
$PY gate_dev.py <CHOSEN> $FRESH --mode ship --size 4b --json $G/look_ship1.json   # look 1
$PY gate_dev.py $C1 $FRESH --mode ship --size 4b --json $G/look_ship2.json        # look 2: only if CHOSEN != C1 and look 1 = DO NOT SHIP
# JOB 2 (only after "C3 TRIGGER"). Estimated 3.7 L4-hours.
$PY gate/materialize_cat.py --force --out models/$C3 --weights 0.75,0.25 models/$RUN models/$REFA
$PY gate/materialize_cat.py --force --out models/$C3W10 --weights 1,0 models/$RUN models/$REFA
$PY gate/materialize_cat.py --force --out models/$C3W01 --weights 0,1 models/$RUN models/$REFA
$(predict_cmd "$REFA" _fresh2 "$STD" "")
$(predict_cmd "$REFA" _fresh2_perm "$SPLITS9" 1)
$PY gate_dev.py $FRESH2 $stored --mode refparity --json $G/look_refparity2.json
$(predict_cmd "$RUN" _j2 "$STD" "")
$(predict_cmd "$C3W10" "" "$SPLITS9" "")
$PY gate/merge_check.py $C3W10 $C1B          # >= 99.5% agreement, mean |dp| < 2e-3
$(predict_cmd "$C3W01" "" "$SPLITS9" "")
$PY gate/merge_check.py $C3W01 $FRESH2
$(predict_cmd "$C3" "" "$STD" "")
$(predict_cmd "$C3" _perm "$SPLITS9" 1)
$PY gate/replacement_rule.py --c1 $C1 --alt $C2 --c3 $C3 --c3-c1 $C1B --c3-ref $FRESH2 --json $G/replacement.json
$PY gate_dev.py <CHOSEN> <$FRESH, or $FRESH2 for C3> --mode ship --size 4b     # then look 2 as in job 1
EOF
}

cmd=${1:-}; shift || true
case "$cmd" in
  fetch) [ $# -ge 1 ] || { echo "fetch PROFILE [final|sNNNNNN ...]"; exit 1; }; mac_fetch "$@" ;;
  check) mac_check ;;
  manifest) mac_manifest ;;
  start) gcloud compute instances start "$VM" --zone "$Z" --project "$P" ;;
  stop) gcloud compute instances stop "$VM" --zone "$Z" --project "$P" ;;
  push) mac_push ;;
  launch) j=${1:-job1}; e="${STOP_BEFORE_SHIP:+STOP_BEFORE_SHIP=1 }${NO_SHUTDOWN:+NO_SHUTDOWN=1 }"
    gssh "cd ~/lean && mkdir -p $G && ${e}nohup bash gate/gate_4b_l4.sh vm-$j > $G/vm-$j.out 2>&1 < /dev/null & echo launched ${e}vm-$j" ;;
  status) gssh "cd ~/lean && tail -n 25 $G/events.log; echo; tail -n 3 $G/reads.log; nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv" ;;
  pull) mac_pull ;;
  vm-job1) vm_job1 ;;
  vm-job2) vm_job2 ;;
  local-ship) local_ship "${1:-job1}" ;;
  plan) plan ;;
  *) sed -n '2,25p' "$0"; exit 1 ;;
esac
