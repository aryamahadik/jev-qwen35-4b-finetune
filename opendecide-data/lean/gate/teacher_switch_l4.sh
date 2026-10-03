#!/bin/bash
# PREREG_FINAL.md 6 (d), the memorisation read: the new 4B reads data/memo4b_train_rows.jsonl (3,209 golden_train rows
# drawn with seed 0, the same count per source as the 3,209 seen-source dev rows; gate/teacher_switch.py build) on the L4
# AFTER job 1 of gate/gate_4b_l4.sh, with the gate's own read settings (base, revision and layout are read from
# gate/gate_4b_l4.sh, so they cannot drift). About 9 L4-minutes. (c) and (d) are then computed on the Mac.
# Companion of gate/gate_4b_l4.sh; that script is not changed (its sha256 is in gate/manifest_4b.sha256).
#
#   Mac:  plan [CAND]               print every command; runs nothing
#         push                      the memo rows + gate/teacher_switch.py, this script and the memo manifest -> the VM;
#                                   verifies the rows' sha256 there (gate/gate_4b_l4.sh push also copies gate/)
#         launch [CAND]             start vm-memo on the VM (nohup), returns at once
#         launch-chain              ONE nohup on the VM: job 1 (with NO_SHUTDOWN=1), then vm-memo, then shutdown.
#                                   STOP_BEFORE_SHIP / NO_SHUTDOWN / MEMO_CAND set on the Mac are passed on
#         status                    tail the VM job's event log
#         pull [CAND]               preds_memo4b_train_rows/CAND.* and logs/gate4b/ back to the Mac
#         check [CAND] [REF]        gate/teacher_switch.py check CAND REF -> logs/gate4b/teacher_switch.{json,txt};
#                                   REF default: the REF of CAND's ship look in summary.json, else q35_4b_pxE_fresh
#   VM:   vm-memo [CAND]            the read (od_gcp.py predict --splits memo4b_train_rows), then VM shutdown
#
# CAND: an argument, else MEMO_CAND, else the shipped candidate of logs/gate4b/summary.json ("ship:<name>"). Without an
# explicit CAND, vm-memo reads only when job 1 ended in a FINAL SHIP and the summary's (c) margin is >= +1.0 pp
# (gate/RUNBOOK_4B_GATE.md 8: (d) is needed only if (b) and (c) pass); otherwise it logs why and skips.
# REF: the fresh 4B-E read of CAND's ship look (q35_4b_pxE_fresh; _fresh2 for C3). Env as in gate/gate_4b_l4.sh: NO_SHUTDOWN, GATE_SIM, PREDICT_CMD.
#
# A8-prime (C4 = q35_4b_main500k_fix2, scored in gate job 3): set the TS_* variables so this script reads job 3's
# settings, folder, REF and adapter manifest instead of job 1's. Unset, every default is job 1's (unchanged behaviour).
#   TS_GATE=gate/gate_4b_fix2_l4.sh   the gate script whose BASE/REV/LAYOUT/REFA (and RUN, else C4) are read
#   TS_G=logs/gate4b_fix2             the job folder (events, summary.json, look_ship*.json)
#   TS_FRESH=q35_4b_pxE_fresh3        the fresh 4B-E read of C4's ship look (the default REF of 'check')
#   TS_MANA=gate/manifest_adapters_fix2.sha256   the adapter manifest that lists models/<C4>/
#   TS_RUN=<name>                     optional: the default CAND when the gate script has neither RUN= nor C4=
# Job 3's summary.json has no (c) margin, so pass CAND explicitly (vm-memo q35_4b_main500k_fix2); (c) is computed by
# 'check' (gate/teacher_switch.py) on the Mac.
set -uo pipefail

P=${GCP_PROJECT:-system-one-509903}; Z=${GCP_ZONE:-us-central1-a}; VM=${GCP_VM:-od-l4}
LEAN=${LEAN:-$(cd "$(dirname "$0")/.." && pwd)}
cd "$LEAN" || exit 1
if [ -z "${PY:-}" ]; then
  if [ -x "$HOME/od/bin/python" ]; then PY=$HOME/od/bin/python; else PY=$LEAN/../.venv/bin/python; fi
fi
PREDICT_CMD=${PREDICT_CMD:-"$PY od_gcp.py predict"}

GATE=${TS_GATE:-gate/gate_4b_l4.sh}
gv() { sed -n "s/^$1=\([^ #;]*\).*/\1/p" "$GATE" | head -n 1; }   # a setting of the gate script, as written there
BASE=$(gv BASE); REV=$(gv REV); LAYOUT=$(gv LAYOUT); RUN=${TS_RUN:-$(gv RUN)}; REFA=$(gv REFA)
[ -n "$RUN" ] || RUN=$(gv C4)
[ -n "$BASE" ] && [ -n "$REV" ] && [ -n "$LAYOUT" ] && [ -n "$RUN" ] && [ -n "$REFA" ] \
  || { echo "cannot read BASE/REV/LAYOUT/RUN/REFA from $GATE"; exit 1; }
FRESH=${TS_FRESH:-${REFA}_fresh}
MEMO=memo4b_train_rows
G=${TS_G:-logs/gate4b}
MANA=${TS_MANA:-gate/manifest_adapters.sha256}

ts() { date -u +%FT%TZ; }
ev() { mkdir -p "$G"; echo "$(ts) MEMO $*" | tee -a "$G/events.log"; }
vm_shutdown() {
  if [ -n "${NO_SHUTDOWN:-}" ] || [ -n "${GATE_SIM:-}" ] || [ "${PHASE:-}" != vm ]; then return 0; fi
  ev "VM shutdown"; sudo shutdown -h now
}
die() { local rc=$1; shift; ev "STOP($rc): $*"; vm_shutdown; exit "$rc"; }
nlines() { wc -l < "$1" | tr -d ' '; }
sha_of() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "$@"; else shasum -a 256 "$@"; fi; }
sha_check() { if command -v sha256sum >/dev/null 2>&1; then sha256sum -c --quiet "$1"; else shasum -a 256 -c --quiet "$1"; fi; }
gssh() { gcloud compute ssh "$VM" --zone "$Z" --project "$P" --command "$1"; }
gscp() { gcloud compute scp --zone "$Z" --project "$P" --quiet "$@"; }
frozen_sha() { "$PY" -c 'import sys; sys.path.insert(0, "gate"); import teacher_switch as t; print(t.MEMO_SHA256)'; }
summary_get() {  # KEY: "cand" (the shipped candidate or empty) or "c" (the (c) margin in pp or empty)
  "$PY" - "$G/summary.json" "$1" <<'EOF'
import json, sys
from pathlib import Path
p, key = Path(sys.argv[1]), sys.argv[2]
r = json.loads(p.read_text()) if p.exists() else {}
o = r.get("outcome", "")
if key == "cand":
    print(o.split(":", 1)[1] if o.startswith("ship:") else "")
else:
    v = r.get("teacher_switch_c_dev_select_diff_pp")
    print("" if v is None else f"{v:.6f}")
EOF
}
predict_line() { echo "HF_HUB_OFFLINE=1 $PREDICT_CMD --name $1 --base $BASE --revision $REV --layout $LAYOUT --splits $MEMO"; }
read_done() {  # CAND
  [ -f "preds_$MEMO/$1.jsonl" ] && [ -f "preds_$MEMO/$1.meta.json" ] \
    && [ "$(nlines "preds_$MEMO/$1.jsonl")" = "$(nlines "data/$MEMO.jsonl")" ]
}

# ------------------------------------------------------------------------------------------------ VM
vm_memo() {
  PHASE=vm; mkdir -p "$G"
  local cand=${1:-${MEMO_CAND:-}} auto=""
  if [ -z "$cand" ]; then
    auto=1; cand=$(summary_get cand)
    if [ -z "$cand" ]; then
      ev "no FINAL SHIP in $G/summary.json ($([ -f "$G/summary.json" ] && "$PY" -c 'import json,sys; print(json.load(open(sys.argv[1]))["outcome"])' "$G/summary.json" || echo 'no summary')): (b) fails, the teacher stays 4B-E; memorisation read skipped"
      vm_shutdown; return 0
    fi
    local c; c=$(summary_get c)
    if [ -z "$c" ] || ! "$PY" -c 'import sys; sys.exit(0 if float(sys.argv[1]) >= 1.0 - 1e-9 else 1)' "$c"; then
      ev "SHIP $cand, but (c) dev-select margin ${c:-missing} pp < +1.0: the teacher stays 4B-E; memorisation read skipped (pass CAND to read anyway)"
      vm_shutdown; return 0
    fi
    ev "SHIP $cand and (c) margin $c pp >= +1.0: memorisation read for (d)"
  fi
  ev "===== MEMO READ START ($cand on $MEMO)"
  # preflight
  [ -f "data/$MEMO.jsonl" ] || die 2 "data/$MEMO.jsonl missing: run 'push'"
  local want got; want=$(frozen_sha) || die 2 "cannot import gate/teacher_switch.py"
  got=$(sha_of "data/$MEMO.jsonl" | cut -d' ' -f1)
  [ "$got" = "$want" ] || die 2 "data/$MEMO.jsonl sha256 $got is not the frozen $want"
  [ -f "models/$cand/train_meta.json" ] || die 3 "models/$cand/train_meta.json missing (adapter not on the VM?)"
  local s
  for s in dev_nc taskbank_dev hard_dev dev_negwords dev_claims pg_dev devzs devp_card dev; do
    [ -f "preds_$s/$cand.meta.json" ] || die 2 "preds_$s/$cand.meta.json missing: job 1 has not read $cand (this read follows job 1)"
  done
  if grep -qE "  models/$cand/[^/]+$" "$MANA" 2>/dev/null; then
    grep -E "  models/$cand/[^/]+$" "$MANA" > "$G/memo_adapter.sha256"
    sha_check "$G/memo_adapter.sha256" > "$G/memo_preflight_sha.txt" 2>&1 || die 2 "models/$cand differs from the Mac's manifest"
  elif [ -f "$G/built_$cand.json" ]; then
    ev "models/$cand was materialized by job 1 ($G/built_$cand.json)"
  else
    die 2 "models/$cand is neither in $MANA nor built by job 1"
  fi
  if [ -z "${GATE_SIM:-}" ]; then
    [ -f "$HOME/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/$REV/config.json" ] \
      || die 2 "base revision $REV is not in the HF cache (HF_HUB_OFFLINE=1 would fail)"
    if pgrep -f "od_gcp.py" >/dev/null; then die 2 "another od_gcp.py job is running on this VM: one job at a time"; fi
    if [ -n "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null)" ]; then die 2 "the GPU is busy"; fi
  fi
  # the read: same command shape as the gate's standard reads (no --tag, no --perm-seed, no TTA, no --force)
  if read_done "$cand"; then
    ev "READ $cand on $MEMO: already complete, skipped"
  else
    ev "READ $cand on $MEMO START: $(predict_line "$cand")"
    local t0; t0=$(date +%s)
    if ! env HF_HUB_OFFLINE=1 $PREDICT_CMD --name "$cand" --base "$BASE" --revision "$REV" --layout "$LAYOUT" \
          --splits "$MEMO" >> "$G/reads.log" 2>&1; then
      die 4 "READ $cand on $MEMO FAILED (see $G/reads.log)"
    fi
    read_done "$cand" || die 4 "READ $cand on $MEMO incomplete after the run"
    ev "READ $cand on $MEMO DONE in $(( ($(date +%s) - t0) / 60 )) min"
  fi
  # the memo read must match the candidate's dev reads (the check repeats this on the Mac)
  "$PY" - "$cand" "$MEMO" <<'EOF' | tee -a "$G/events.log"
import json, sys
cand, memo = sys.argv[1:3]
a = json.load(open(f"preds_dev/{cand}.meta.json")); b = json.load(open(f"preds_{memo}/{cand}.meta.json"))
keys = ("base", "host", "gpu", "torch", "cuda", "layout", "style", "perm_seed", "tta", "tta_choice", "tta_noul")
la, lb = a.get("load") or {}, b.get("load") or {}
diff = [k for k in keys if a.get(k) != b.get(k)] + [f"load.{k}" for k in ("revision", "chat_template_sha", "forced") if la.get(k) != lb.get(k)]
print(f"MEMO meta vs preds_dev/{cand}: " + ("same settings" if not diff else "DIFFERENT " + ", ".join(diff)))
EOF
  ev "===== MEMO READ END: on the Mac run 'pull' then 'check'"
  vm_shutdown
}

# ------------------------------------------------------------------------------------------------ Mac
mac_cand() { local c=${1:-${MEMO_CAND:-}}; [ -n "$c" ] || c=$(summary_get cand); [ -n "$c" ] || c=$RUN; echo "$c"; }
mac_push() {
  local want got; want=$(frozen_sha); got=$(sha_of "data/$MEMO.jsonl" | cut -d' ' -f1)
  [ "$got" = "$want" ] || { echo "local data/$MEMO.jsonl sha256 $got is not the frozen $want"; return 1; }
  gscp "data/$MEMO.jsonl" "$VM:~/lean/data/" || return 1
  gscp gate/teacher_switch.py gate/teacher_switch_l4.sh gate/memo4b_train_rows.json "$VM:~/lean/gate/" || return 1
  gssh "cd ~/lean && echo '$want  data/$MEMO.jsonl' | sha256sum -c --quiet && echo 'VM memo rows OK'"
}
mac_pull() {
  local cand; cand=$(mac_cand "${1:-}")
  mkdir -p "preds_$MEMO" "$G"
  gscp "$VM:~/lean/preds_$MEMO/$cand.*" "preds_$MEMO/" || return 1
  gscp --recurse "$VM:~/lean/$G/*" "$G/" || echo "no $G on the VM?"
  echo "pulled preds_$MEMO/$cand.jsonl ($(nlines "preds_$MEMO/$cand.jsonl") rows; data has $(nlines "data/$MEMO.jsonl"))"
}
summary_ref() {  # CAND -> the REF of CAND's ship look in summary.json (q35_4b_pxE_fresh2 for C3), or empty
  "$PY" - "$G/summary.json" "$1" <<'EOF'
import json, sys
from pathlib import Path
p, cand = Path(sys.argv[1]), sys.argv[2]
r = json.loads(p.read_text()) if p.exists() else {}
print(next((v["ref"] for v in (r.get("looks") or {}).values() if v.get("cand") == cand and "verdict" in v), ""))
EOF
}
mac_check() {
  local cand ref; cand=$(mac_cand "${1:-}"); ref=${2:-}
  [ -n "$ref" ] || ref=$(summary_ref "$cand")
  [ -n "$ref" ] || ref=$FRESH
  local looks=() f
  for f in "$G"/look_ship*.json; do [ -f "$f" ] && looks+=("$f"); done
  mkdir -p "$G"
  "$PY" gate/teacher_switch.py check "$cand" "$ref" ${looks[@]+--ship-json "${looks[@]}"} --json "$G/teacher_switch.json" \
    2>&1 | tee "$G/teacher_switch.txt"
  return "${PIPESTATUS[0]}"
}
plan() {
  local cand; cand=$(mac_cand "${1:-}")
  cat <<EOF
# Mac, once (done 1 Oct): the frozen sample and its manifest
$PY gate/teacher_switch.py build --replay           # data/$MEMO.jsonl sha256 $(frozen_sha 2>/dev/null)
# Mac: copy to the VM (after gate/gate_4b_l4.sh push)
gcloud compute scp --zone $Z --project $P --quiet data/$MEMO.jsonl $VM:~/lean/data/
gcloud compute scp --zone $Z --project $P --quiet gate/teacher_switch.py gate/teacher_switch_l4.sh gate/memo4b_train_rows.json $VM:~/lean/gate/
# VM (od-l4, ~/lean), after job 1; ~9 L4-minutes. CAND = $cand (the shipped candidate)
$(predict_line "$cand")
# Mac: results back, then (b) (c) (d)
gcloud compute scp --zone $Z --project $P --quiet "$VM:~/lean/preds_$MEMO/$cand.*" preds_$MEMO/
$PY gate/teacher_switch.py check $cand $FRESH --ship-json $([ -n "${TS_G:-}" ] && echo "$G/look_ship*.json" || echo "$G/look_ship1.json [$G/look_ship2.json]") --json $G/teacher_switch.json
EOF
}

cmd=${1:-}; shift || true
case "$cmd" in
  plan) plan "${1:-}" ;;
  push) mac_push ;;
  launch) c=${1:-${MEMO_CAND:-}}; e="${NO_SHUTDOWN:+NO_SHUTDOWN=1 }"
    gssh "cd ~/lean && mkdir -p $G && ${e}nohup bash gate/teacher_switch_l4.sh vm-memo $c > $G/vm-memo.out 2>&1 < /dev/null & echo launched ${e}vm-memo $c" ;;
  launch-chain) e1="${STOP_BEFORE_SHIP:+STOP_BEFORE_SHIP=1 }"; e2="${NO_SHUTDOWN:+NO_SHUTDOWN=1 }${MEMO_CAND:+MEMO_CAND=$MEMO_CAND }"
    gssh "cd ~/lean && mkdir -p $G && nohup bash -c '${e1}NO_SHUTDOWN=1 bash gate/gate_4b_l4.sh vm-job1; ${e2}bash gate/teacher_switch_l4.sh vm-memo' > $G/vm-chain.out 2>&1 < /dev/null & echo launched job1 then vm-memo" ;;
  status) gssh "cd ~/lean && tail -n 25 $G/events.log; echo; tail -n 3 $G/reads.log; nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv" ;;
  pull) mac_pull "${1:-}" ;;
  check) mac_check "${1:-}" "${2:-}" ;;
  vm-memo) vm_memo "${1:-}" ;;
  *) sed -n '2,23p' "$0"; exit 1 ;;
esac
