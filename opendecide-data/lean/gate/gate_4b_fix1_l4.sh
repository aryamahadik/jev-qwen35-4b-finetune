#!/bin/bash
# Re-check of the 4B after the top-up: candidate C4 = q35_4b_main500k_fix1 vs a FRESH 4B-E read, on the Google L4 VM
# od-l4 (PREREG_FINAL.md sections 3-5 as amended by A8; the job-1 script gate/gate_4b_l4.sh is not changed or re-run).
# A8 must be COMMITTED before "launch" (the manifest phase refuses otherwise). Paths resolve to the lean/ folder.
#
#   Mac phases:  fetch PROFILE        download the C4 adapter from that Modal account's volume, check it, keep one copy
#                check                gate/check_adapter_fix1.py on the local copy
#                manifest             sha256 manifests (code, data, stored REF preds, the 12 training files + the fix1
#                                     file, adapters C4 and 4B-E); needs A8 committed
#                start | stop         gcloud compute instances start/stop od-l4
#                push                 C4 adapter + gate/ to the VM, then verify both manifests there
#                launch               start vm-job3 in the background (nohup); returns at once
#                status | pull        tail the VM log | preds, looks and logs back to the Mac (merges the ledger)
#                report               after pull, REPORT ONLY (never decisive, no look logged): C4 vs C1 per split
#                                     (C1 = the job-1 read; cross-job) with gate_dev.py --mode confirm
#   VM phase:    vm-job3              REF reads (fresh3 + _perm) -> refparity3 -> C4 reads (+ _perm) -> ship look ship_c4
#   any:         plan                 print every command of job 3; runs nothing
#
# Env: NO_SHUTDOWN=1 keeps the VM up; PUSH_FIXES=1 lets "push" overwrite VM files whose sha256 differs; GATE_SIM=1 +
# PREDICT_CMD=... is the CPU simulation (gate/tests/sim_gate_fix1.py); ALLOW_DIRTY=1 lets "manifest" run without A8
# committed (dry runs only). Every look runs at most once: $G/looks/<id>.done blocks a repeat.
set -uo pipefail

P=${GCP_PROJECT:-system-one-509903}; Z=${GCP_ZONE:-us-central1-a}; VM=${GCP_VM:-od-l4}
LEAN=${LEAN:-$(cd "$(dirname "$0")/.." && pwd)}
cd "$LEAN" || exit 1
if [ -z "${PY:-}" ]; then
  if [ -x "$HOME/od/bin/python" ]; then PY=$HOME/od/bin/python; else PY=$LEAN/../.venv/bin/python; fi
fi
PREDICT_CMD=${PREDICT_CMD:-"$PY od_gcp.py predict"}

C4=q35_4b_main500k_fix1      # the top-up's final adapter (runs/q35_4b_fix1.json); the only candidate of job 3
C1=q35_4b_main500k           # report only (job-1 reads)
REFA=q35_4b_pxE              # REF adapter (4B-E)
FRESH3=${REFA}_fresh3        # job-3 fresh REF read (PREREG 4: REF is re-scored in the job that scores the candidate)
BASE=Qwen/Qwen3.5-4B
REV=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
LAYOUT=schema_branch_mark
SPLITS9=dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev
STD=$SPLITS9,eval_jagged,eval_opi,eval_redef   # eval_redef is report-only (not in the ship rule)
TRAIN12="v14_parts/golden_train train_v07 train_v08s2 train_v09s3 train_v10s4 train_v11 train_v11b train_v11c train_v13t train_prism_arms train_2b_kd train_2b_rest"
FIX1DATA="v14_parts/fix1_train v14_parts/fix1_relations"
BACKUP=${BACKUP:-/Users/aryamahadik/Documents/jev/backups/modal_models/$C4}
G=logs/gate4b_fix1
MAN=gate/manifest_4b_fix1.sha256; MANA=gate/manifest_adapters_fix1.sha256

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
predict_cmd() {
  local name=$1 tag=$2 splits=$3 perm=$4
  echo "HF_HUB_OFFLINE=1 $PREDICT_CMD --name $name --base $BASE --revision $REV --layout $LAYOUT --splits $splits${tag:+ --tag $tag}${perm:+ --perm-seed $perm}"
}
read_done() {
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
read_std() { predict "$1" "$2" "$STD" ""; }
read_perm() { predict "$1" "$2" "$SPLITS9" 1; }

# ------------------------------------------------------------------------------------------------ looks (gate_dev.py)
look() {  # ID MODE CAND REF
  local id=$1 mode=$2 cand=$3 ref=$4 j="$G/look_$1.json" sz=""
  mkdir -p "$G/looks"
  if [ -f "$G/looks/$id.done" ]; then ev "LOOK $id: already made ($(cat "$G/looks/$id.done")); not repeated"; return 0; fi
  [ "$mode" = ship ] && sz="--size 4b"
  ev "LOOK $id: gate_dev.py $cand $ref --mode $mode $sz"
  "$PY" gate_dev.py "$cand" "$ref" --mode "$mode" $sz --json "$j" > "$G/look_$id.txt" 2>&1
  local rc=$?
  cat "$G/look_$id.txt" >> "$G/looks.log"
  if [ $rc -ne 0 ]; then
    die 6 "LOOK $id: gate_dev.py stopped (exit $rc): $(tail -n 3 "$G/look_$id.txt" | tr '\n' ' ')"
  fi
  echo "$(ts) $mode $cand vs $ref" > "$G/looks/$id.done"
  tail -n 4 "$G/look_$id.txt" | sed 's/^/    /' | tee -a "$G/events.log"
}
parity_gate() {
  local id=$1 j="$G/look_$1.json"
  if [ "$(jget "$j" 'r["pass"]')" != True ]; then
    die 10 "REF PARITY FAILED for $2 (PREREG_FINAL.md 4): stop and consult the owner. No candidate was read in this job."
  fi
  if [ "$(jget "$j" 'r["counts"]')" != True ]; then
    die 11 "REF parity passed but does not count: $(jget "$j" 'r["why_not"]')"
  fi
}

# ------------------------------------------------------------------------------------------------ VM preflight
vm_preflight() {
  ev "PREFLIGHT in $LEAN (python $PY)"
  [ -f "$MAN" ] && [ -f "$MANA" ] || die 2 "$MAN / $MANA missing: run 'manifest' and 'push' on the Mac"
  sha_check "$MAN" > "$G/preflight_sha.txt" 2>&1 || die 2 "code/data/stored-preds sha256 differ from the Mac's (see $G/preflight_sha.txt)"
  sha_check "$MANA" >> "$G/preflight_sha.txt" 2>&1 || die 2 "adapter sha256 differ from the Mac's (see $G/preflight_sha.txt)"
  grep -q "Amendment A8" PREREG_FINAL.md || die 2 "PREREG_FINAL.md has no Amendment A8 (commit it before any C4 read)"
  local s f
  for s in ${STD//,/ }; do [ -f "data/$s.jsonl" ] || die 2 "data/$s.jsonl missing"; done
  for f in $TRAIN12 $FIX1DATA; do [ -f "data/$f.jsonl" ] || die 2 "data/$f.jsonl missing (the ship verdict would be NOT FINAL / A8 check)"; done
  [ -f "models/$C4/train_meta.json" ] || die 2 "models/$C4 missing on the VM"
  [ -f "models/$REFA/adapter_model.safetensors" ] || die 2 "models/$REFA missing"
  if [ -z "${GATE_SIM:-}" ]; then
    [ -f "$HOME/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/$REV/config.json" ] \
      || die 2 "base revision $REV is not in the HF cache (HF_HUB_OFFLINE=1 would fail)"
    if pgrep -f "od_gcp.py" >/dev/null; then die 2 "another od_gcp.py job is running on this VM: one job at a time"; fi
    if [ -n "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null)" ]; then die 2 "the GPU is busy"; fi
  fi
  # A8: the unseen-source set must not move when C4's extra training file is added (CPU, read-only, no look)
  "$PY" gate/check_unseen_fix1.py > "$G/preflight_unseen.txt" 2>&1 \
    || die 2 "check_unseen_fix1 FAILED (A8 precondition): $(tail -n 1 "$G/preflight_unseen.txt")"
  STORED=$(stored_ref) || die 2 "cannot import gate_dev.py"
  ev "gate_dev.py sha256 $(sha_of gate_dev.py | cut -c1-16)...; STORED_REF[4b] = $STORED"
  [ "$STORED" = q35_4b_pxE_parity ] || die 2 "STORED_REF[4b] is $STORED, not q35_4b_pxE_parity (A7)"
  for s in ${SPLITS9//,/ }; do [ -f "preds_$s/$STORED.jsonl" ] || die 2 "stored REF preds_$s/$STORED.jsonl missing"; done
  ev "PREFLIGHT OK"
}

# ------------------------------------------------------------------------------------------------ VM job 3
vm_job3() {
  PHASE=vm; mkdir -p "$G"
  ev "===== JOB 3 START (REF $REFA as $FRESH3; C4 $C4)"
  vm_preflight
  read_std "$REFA" _fresh3
  read_perm "$REFA" _fresh3_perm
  look refparity3 refparity "$FRESH3" "$STORED"
  parity_gate refparity3 "$FRESH3"
  read_std "$C4" ""
  read_perm "$C4" _perm
  look ship_c4 ship "$C4" "$FRESH3"
  local v; v="$(jget "$G/look_ship_c4.json" 'r["verdict"]')|$(jget "$G/look_ship_c4.json" 'r["final"]')"
  ev "SHIP LOOK C4: $C4 vs $FRESH3 -> ${v%%|*} (final ${v##*|})"
  if [ "${v##*|}" != True ]; then summary not-final; die 13 "the C4 ship look is NOT FINAL: it decides nothing; consult the owner"; fi
  if [ "${v%%|*}" = SHIP ]; then summary "ship:$C4"; else summary "noship:$C4"; fi
  vm_shutdown
}

summary() {
  "$PY" - "$1" "$G" <<'EOF' | tee -a "$G/events.log"
import json, sys
from pathlib import Path
outcome, G = sys.argv[1], Path(sys.argv[2])
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
text = {"ship:": "SHIP {} (A8: C4 passes the ship rule vs the fresh 4B-E read)",
        "noship:": "DO NOT SHIP {} (A8: fallback stays 4B-E, PREREG 5.7)"}
d = next((v.format(outcome.split(":", 1)[1]) for k, v in text.items() if outcome.startswith(k)), outcome)
out = {"outcome": outcome, "decision": d, "looks": looks}
(G / "summary.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"SUMMARY: {d}")
for k, v in looks.items():
    print(f"   {k}: {json.dumps(v)[:300]}")
EOF
}

# ------------------------------------------------------------------------------------------------ Mac phases
mac_fetch() {  # PROFILE: Modal volume -> $BACKUP (one local copy)
  local prof=$1 M=$LEAN/../.venv/bin/modal stage f
  [ -e "$BACKUP/adapter_model.safetensors" ] && { echo "$BACKUP exists; not fetched again"; return 0; }
  stage=$LEAN/handoff/fix1_gate_dl/final; mkdir -p "$stage"
  for f in adapter_config.json adapter_model.safetensors tokenizer.json tokenizer_config.json chat_template.jinja train_meta.json; do
    MODAL_PROFILE=$prof "$M" volume get --force opendecide "models/$C4/$f" "$stage/" || { echo "fetch failed: $f"; return 1; }
  done
  "$PY" gate/check_adapter_fix1.py "$stage" || { echo "C4 adapter check FAILED (kept in $stage)"; return 1; }
  mkdir -p "$BACKUP"; for f in "$stage"/*; do mv "$f" "$BACKUP/"; done
  echo "fetched into $BACKUP"
}

mac_manifest() {
  local s f stored
  if [ -z "${ALLOW_DIRTY:-}" ] && git -C "$LEAN" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    local dirty; dirty=$(git -C "$LEAN" status --porcelain -- gate_dev.py PREREG_FINAL.md ship_unseen_sources.json \
      tests/test_ship_rule.py tests/test_amendment_A7.py runs/q35_4b_fix1.json gate/gate_4b_fix1_l4.sh \
      gate/check_unseen_fix1.py gate/check_adapter_fix1.py)
    if [ -n "$dirty" ]; then
      echo "uncommitted changes to the pre-registered files (commit A8 first, or ALLOW_DIRTY=1 for a dry run):"
      echo "$dirty" | sed 's/^/   /'; return 1
    fi
    git -C "$LEAN" show HEAD:opendecide-data/lean/PREREG_FINAL.md 2>/dev/null | grep -q "Amendment A8" \
      || { echo "Amendment A8 is not in the committed PREREG_FINAL.md (HEAD)"; return 1; }
    echo "A8 committed (HEAD $(git -C "$LEAN" rev-parse --short HEAD); gate_dev.py $(sha_of gate_dev.py | cut -c1-16)...)"
  fi
  stored=$(stored_ref)
  {
    sha_of gate_dev.py od_gcp.py decoder_io.py prism_x.py writeblock.py ship_unseen_sources.json gate/gate_4b_fix1_l4.sh \
      gate/check_unseen_fix1.py yn2b/check_unseen.py yn2b/yn2b_common.py runs/q35_4b_fix1.json
    for s in ${STD//,/ }; do sha_of "data/$s.jsonl"; done
    for s in ${SPLITS9//,/ }; do [ -f "data/${s}_relations.jsonl" ] && sha_of "data/${s}_relations.jsonl"; done
    for f in $TRAIN12 $FIX1DATA; do sha_of "data/$f.jsonl"; done
    for s in ${SPLITS9//,/ }; do sha_of "preds_$s/$stored.jsonl" "preds_$s/$stored.meta.json"; done
  } > "$MAN" || return 1
  {
    (cd "$BACKUP" && sha_of adapter_config.json adapter_model.safetensors train_meta.json chat_template.jinja tokenizer.json tokenizer_config.json) | sed "s|  |  models/$C4/|"
    if [ -d "models/$REFA" ]; then sha_of "models/$REFA/adapter_config.json" "models/$REFA/adapter_model.safetensors"
    else (cd "${REF_BACKUP:-/Users/aryamahadik/Documents/jev/backups/gcp_models/$REFA}" && sha_of adapter_config.json adapter_model.safetensors) | sed "s|  |  models/$REFA/|"; fi
  } > "$MANA" || return 1
  echo "wrote $MAN ($(nlines "$MAN") files, stored REF $stored) and $MANA ($(nlines "$MANA") files)"
}

mac_push() {
  [ -f "$MAN" ] && [ -f "$MANA" ] || { echo "run 'manifest' first"; return 1; }
  gscp --recurse "$LEAN/gate" "$VM:~/lean/" || return 1
  gssh "mkdir -p ~/lean/yn2b ~/lean/runs ~/lean/data/v14_parts" || return 1
  gscp "$LEAN/yn2b/check_unseen.py" "$LEAN/yn2b/yn2b_common.py" "$VM:~/lean/yn2b/" || return 1
  gscp "$LEAN/runs/q35_4b_fix1.json" "$VM:~/lean/runs/" || return 1
  gscp "$LEAN/data/v14_parts/fix1_train.jsonl" "$LEAN/data/v14_parts/fix1_relations.jsonl" "$VM:~/lean/data/v14_parts/" || return 1
  if gssh "test -e ~/lean/models/$C4"; then
    gssh "cd ~/lean && sha256sum -c --quiet $MANA" || { echo "~/lean/models/$C4 exists on the VM but differs: check by hand"; return 1; }
  else
    gscp --recurse "$BACKUP" "$VM:~/lean/models/" || return 1
  fi
  local bad
  bad=$(gssh "cd ~/lean && (sha256sum -c --quiet $MAN; sha256sum -c --quiet $MANA) 2>&1 | grep -E 'FAILED|No such' | sed 's/:.*//'" | tr -d '\r')
  if [ -z "$bad" ]; then echo "VM manifests OK"; return 0; fi
  echo "files that differ or are missing on the VM:"; echo "$bad" | sed 's/^/   /'
  if [ -z "${PUSH_FIXES:-}" ]; then echo "re-run with PUSH_FIXES=1 to copy the Mac's versions to the VM"; return 1; fi
  local f
  for f in $bad; do gssh "mkdir -p ~/lean/$(dirname "$f")" && gscp "$LEAN/$f" "$VM:~/lean/$f" || return 1; done
  gssh "cd ~/lean && sha256sum -c --quiet $MAN && sha256sum -c --quiet $MANA" && echo "VM manifests OK after fixes"
}

mac_pull() {
  local d n
  for d in $(echo "$STD" | tr ',' '\n' | sed 's/^/preds_/'); do
    mkdir -p "$d"
    for n in "$FRESH3" "$C4"; do gscp "$VM:~/lean/$d/$n*" "$d/" >/dev/null 2>&1 || true; done
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

mac_report() {  # REPORT ONLY: no look is logged (--mode confirm never logs); C1 preds are the job-1 read (cross-job)
  "$PY" gate_dev.py "$C4" "$C1" --mode confirm 2>&1 | tee "$G/report_c4_vs_c1.txt"
}

plan() {
  local stored; stored=$(stored_ref 2>/dev/null || echo "<STORED_REF[4b]>")
  cat <<EOF
# JOB 3 on od-l4 (~/lean, python ~/od/bin/python). 4 reads, about 2.3 L4-hours.
$PY gate/check_unseen_fix1.py                                        # A8 precondition (preflight; no look)
$(predict_cmd "$REFA" _fresh3 "$STD" "")
$(predict_cmd "$REFA" _fresh3_perm "$SPLITS9" 1)
$PY gate_dev.py $FRESH3 $stored --mode refparity --json $G/look_refparity3.json   # FAIL -> stop, consult owner
$(predict_cmd "$C4" "" "$STD" "")
$(predict_cmd "$C4" _perm "$SPLITS9" 1)
$PY gate_dev.py $C4 $FRESH3 --mode ship --size 4b --json $G/look_ship_c4.json        # the one C4 look (A8)
# Mac, after pull (report only, never decisive): $PY gate_dev.py $C4 $C1 --mode confirm
EOF
}

cmd=${1:-}; shift || true
case "$cmd" in
  fetch) [ $# -ge 1 ] || { echo "fetch PROFILE"; exit 1; }; mac_fetch "$1" ;;
  check) "$PY" gate/check_adapter_fix1.py "$BACKUP" ;;
  manifest) mac_manifest ;;
  start) gcloud compute instances start "$VM" --zone "$Z" --project "$P" ;;
  stop) gcloud compute instances stop "$VM" --zone "$Z" --project "$P" ;;
  push) mac_push ;;
  launch) e="${NO_SHUTDOWN:+NO_SHUTDOWN=1 }"
    gssh "cd ~/lean && mkdir -p $G && ${e}nohup bash gate/gate_4b_fix1_l4.sh vm-job3 > $G/vm-job3.out 2>&1 < /dev/null & echo launched ${e}vm-job3" ;;
  status) gssh "cd ~/lean && tail -n 25 $G/events.log; echo; tail -n 3 $G/reads.log; nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv" ;;
  pull) mac_pull ;;
  report) mac_report ;;
  vm-job3) vm_job3 ;;
  plan) plan ;;
  *) sed -n '2,22p' "$0"; exit 1 ;;
esac
