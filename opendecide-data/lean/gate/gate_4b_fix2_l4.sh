#!/bin/bash
# Gate job 3 for the 4B top-up: candidate C4 = q35_4b_main500k_fix2 (draft amendment A8-prime,
# prereg_drafts/A8prime.md), on the ORIGINAL Google L4 VM od-l4 (us-central1-a). The job-1 script gate/gate_4b_l4.sh is
# not changed or re-run. A8-prime must be COMMITTED (HEAD's PREREG_FINAL.md holds "Amendment A8-prime") before
# "manifest". Paths resolve to the lean/ folder. One job, one GPU type, one code commit (PREREG_FINAL 4).
#
#   Mac:  pairs                 A8' 0a: freeze the F7 probe / devx aff-dneg pair lists (gate/fix2_pairs.json), BEFORE
#                               any read of either file and before the A8' commit (the file is part of it)
#         manifest              sha256 manifests: code, data (9 splits + attacks + F7 probe/devx + pair list + the 12
#                               training files + fix2 + memo rows), stored REF preds; adapters C1 and 4B-E
#         start | stop          gcloud compute instances start/stop od-l4
#         push                  code, data, manifests (+ C1 / 4B-E only if missing) -> VM; verify both manifests there
#         launch0               start vm-probe0 on the VM (A8' 0b: C1 and 4B-E read the probe + devx; GO rule)
#         launch                start vm-job3 on the VM (nohup; part 1 runs at once, then it waits for C4)
#         fetch PROFILE         C4 from that Modal account's volume -> check -> the one local copy
#         check                 gate/check_adapter_fix2.py on the local copy
#         manifest-c4           gate/manifest_c4_fix2.sha256 (C4 adapter files)
#         push-c4               C4 + its manifest -> VM, verified there (vm-job3 then continues by itself)
#         status | pull         tail the VM log | preds, logs and looks back to the Mac (merges the look ledger)
#         report                after pull, REPORT ONLY: C4 vs C1 (job-1 read; cross-job) with gate_dev.py --mode confirm
#   VM:   vm-probe0             A8' 0b (no shutdown: the VM stays up for job 3)
#         vm-reset-pre-c4 NOTE  ONLY after refparity3 or R failed (or gave no verdict), BEFORE any C4 read, and after the
#                               VM was repaired (A8' F, H): moves the R / refparity3 records and the job-3 REF fresh3 and
#                               C1R reads into $G/reset_<UTC>/ with the dated NOTE (nothing is deleted); refuses once
#                               any C4 read or any P / N / ship-look record exists. Then 'launch' re-runs job 3.
#         vm-job3               preflight -> REF fresh3 (+perm) -> refparity3 -> C1R (+f7, +perm) -> R ->
#                               C1R exact 2-view reads (report) -> wait for C4 -> C4 (+f7, +perm) -> P -> N ->
#                               the one ship look -> summary -> C4 exact 2-view reads + 2-view report (report only)
#                               -> only after a FINAL SHIP: C4 _2v (--tta-choice) read + the 6 (d) memo read
#   any:  plan                  print every command of job 3; runs nothing
#
# Env: NO_SHUTDOWN=1 keeps the VM up at the end; PUSH_FIXES=1 lets "push" overwrite VM files whose sha256 differs
# (fixed parser: only "<path>: FAILED[ open or read]" lines name files; job 1's "sha256sum:" warning lines no longer
# become bogus copy targets); WAIT_C4_MAX_MIN (default 900) bounds the wait for C4; GATE_SIM=1 + PREDICT_CMD=... is the
# CPU simulation (gate/tests/sim_gate_fix2.py); ALLOW_DIRTY=1 lets "manifest" run without A8' committed (dry runs only).
# Every look runs at most once ($G/looks/<id>.done); every condition step at most once ($G/conds/<id>.json).
set -uo pipefail

P=${GCP_PROJECT:-system-one-509903}; Z=${GCP_ZONE:-us-central1-a}; VM=${GCP_VM:-od-l4}
LEAN=${LEAN:-$(cd "$(dirname "$0")/.." && pwd)}
cd "$LEAN" || exit 1
if [ -z "${PY:-}" ]; then
  if [ -x "$HOME/od/bin/python" ]; then PY=$HOME/od/bin/python; else PY=$LEAN/../.venv/bin/python; fi
fi
PREDICT_CMD=${PREDICT_CMD:-"$PY od_gcp.py predict"}

C4=q35_4b_main500k_fix2      # the top-up's last-step adapter (runs/q35_4b_fix2.json); the only candidate of job 3
C1=q35_4b_main500k           # C1 (re-read here as C1R; also the job-1 reads, for R and the reports)
REFA=q35_4b_pxE              # REF adapter (4B-E)
BASE=Qwen/Qwen3.5-4B
REV=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
LAYOUT=schema_branch_mark
FRESH3=${REFA}_fresh3        # job-3 fresh REF read (PREREG 4)
C1R=${C1}_r3                 # job-3 C1 re-read (A8' R / P / N)
SPLITS9=dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev
STD=$SPLITS9,eval_jagged,eval_opi,eval_redef   # eval_redef is report-only (not in the ship rule)
F7S=f7_probe,f7_devx
TRAIN12="v14_parts/golden_train train_v07 train_v08s2 train_v09s3 train_v10s4 train_v11 train_v11b train_v11c train_v13t train_prism_arms train_2b_kd train_2b_rest"
FIX2DATA="v14_parts/fix2_train v14_parts/fix2_relations"
F7DATA="f7_probe f7_probe_relations f7_probe_meta f7_devx f7_devx_relations f7_devx_meta"
MEMO=memo4b_train_rows
BACKUP=${BACKUP:-/Users/aryamahadik/Documents/jev/backups/modal_models/$C4}
C1_BACKUP=${C1_BACKUP:-/Users/aryamahadik/Documents/jev/backups/modal_models/$C1}
REF_BACKUP=${REF_BACKUP:-/Users/aryamahadik/Documents/jev/backups/gcp_models/$REFA}
G=logs/gate4b_fix2
MAN=gate/manifest_4b_fix2.sha256; MANA=gate/manifest_adapters_fix2.sha256; MANC4=gate/manifest_c4_fix2.sha256
PAIRS=gate/fix2_pairs.json
A8P="Amendment A8-prime"
WAIT_C4_MAX_MIN=${WAIT_C4_MAX_MIN:-900}
ADAPTER_FILES="adapter_config.json adapter_model.safetensors train_meta.json chat_template.jinja tokenizer.json tokenizer_config.json"

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
# the files a sha256 check names as differing or missing: ONLY lines "<path>: FAILED" / "<path>: FAILED open or read"
# (fixes gate_4b_l4.sh's push parser, which also turned "sha256sum: <path>: No such file ..." and "sha256sum: WARNING"
# lines into the bogus path "sha256sum")
failed_paths() { sed -n 's/^\(.*\): FAILED\( open or read\)\{0,1\}$/\1/p'; }

# ------------------------------------------------------------------------------------------------ reads (od_gcp predict)
out_name() { local n=$1; echo "${n//\//__}$2"; }
predict_cmd() {  # NAME TAG SPLITS PERM [EXTRA FLAGS]
  local name=$1 tag=$2 splits=$3 perm=$4; shift 4
  echo "HF_HUB_OFFLINE=1 $PREDICT_CMD --name $name --base $BASE --revision $REV --layout $LAYOUT --splits $splits${tag:+ --tag $tag}${perm:+ --perm-seed $perm}${*:+ $*}"
}
read_done() {
  local out=$1 s
  for s in ${2//,/ }; do
    [ -f "preds_$s/$out.jsonl" ] && [ -f "preds_$s/$out.meta.json" ] || return 1
    [ "$(nlines "preds_$s/$out.jsonl")" = "$(nlines "data/$s.jsonl")" ] || return 1
  done
}
predict() {  # NAME TAG SPLITS PERM [EXTRA FLAGS: --tta | --tta-choice]
  local name=$1 tag=$2 splits=$3 perm=$4; shift 4
  local out; out=$(out_name "$name" "$tag")
  if read_done "$out" "$splits"; then ev "READ $out: already complete, skipped"; return 0; fi
  [ -f "models/$name/train_meta.json" ] || die 3 "models/$name/train_meta.json missing (adapter not on the VM?)"
  ev "READ $out START ($splits${perm:+, perm-seed $perm}${*:+, $*})"
  local t0; t0=$(date +%s)
  if ! env HF_HUB_OFFLINE=1 $PREDICT_CMD --name "$name" --base "$BASE" --revision "$REV" --layout "$LAYOUT" \
        --splits "$splits" ${tag:+--tag "$tag"} ${perm:+--perm-seed "$perm"} "$@" >> "$G/reads.log" 2>&1; then
    die 4 "READ $out FAILED (see $G/reads.log)"
  fi
  read_done "$out" "$splits" || die 4 "READ $out incomplete after the run"
  ev "READ $out DONE in $(( ($(date +%s) - t0) / 60 )) min"
}

# ------------------------------------------------------------------------------------------------ looks and conditions
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
  local j="$G/look_$1.json"
  if [ "$(jget "$j" 'r["pass"]')" != True ]; then
    die 10 "REF PARITY FAILED for $2 (PREREG_FINAL.md 4): stop and consult the owner. No candidate was read in this job; after a repair, 'vm-reset-pre-c4 NOTE' then 'launch' (A8' F)."
  fi
  if [ "$(jget "$j" 'r["counts"]')" != True ]; then
    die 11 "REF parity passed but does not count: $(jget "$j" 'r["why_not"]')"
  fi
}
cond() {  # ID TOOL ARGS...  -> 0 pass / 1 fail; computed once (the JSON is the record); a crash stops the job
  local id=$1 tool=$2; shift 2
  local j="$G/conds/$id.json"
  mkdir -p "$G/conds"
  if [ -f "$j" ]; then
    ev "COND $id: already computed ($(jget "$j" 'r["pass"]')); not recomputed"
  else
    ev "COND $id: $tool $*"
    "$PY" "$tool" "$@" --json "$j.tmp" > "$G/conds/$id.txt" 2>&1
    local rc=$?
    cat "$G/conds/$id.txt" >> "$G/conds.log"
    if [ ! -f "$j.tmp" ] || { [ $rc -ne 0 ] && [ $rc -ne 1 ]; }; then
      die 7 "COND $id: $tool stopped (exit $rc, no verdict): $(tail -n 3 "$G/conds/$id.txt" | tr '\n' ' ')"
    fi
    mv "$j.tmp" "$j"
    tail -n 12 "$G/conds/$id.txt" | sed 's/^/    /' | tee -a "$G/events.log"
  fi
  [ "$(jget "$j" 'r["pass"]')" = True ]
}

# ------------------------------------------------------------------------------------------------ VM preflights
vm_preflight_common() {
  [ -f "$MAN" ] && [ -f "$MANA" ] || die 2 "$MAN / $MANA missing: run 'manifest' and 'push' on the Mac"
  sha_check "$MAN" > "$G/preflight_sha.txt" 2>&1 || die 2 "code/data/stored-preds sha256 differ from the Mac's (see $G/preflight_sha.txt)"
  sha_check "$MANA" >> "$G/preflight_sha.txt" 2>&1 || die 2 "C1 / 4B-E adapter sha256 differ from the Mac's (see $G/preflight_sha.txt)"
  grep -q "$A8P" PREREG_FINAL.md || die 2 "PREREG_FINAL.md has no $A8P (commit it before any probe or C4 read)"
  [ -f "$PAIRS" ] || die 2 "$PAIRS missing: A8' 0a ('pairs') freezes the pair lists before any probe read"
  local s
  for s in $F7DATA; do [ -f "data/$s.jsonl" ] || die 2 "data/$s.jsonl missing"; done
  "$PY" - <<'EOF' > "$G/preflight_pairs.txt" 2>&1 || die 2 "the probe / devx differ from the frozen pair lists: $(tail -n 1 "$G/preflight_pairs.txt")"
import sys
sys.path.insert(0, "gate")
import fix2_conditions as fc
for sp in (fc.PROBE, fc.DEVX):
    pairs, fz = fc.frozen_pairs(sp)
    print(sp, len(pairs or []), "pairs, files unchanged since the freeze")
EOF
  [ -f "models/$C1/adapter_model.safetensors" ] || die 2 "models/$C1 missing"
  [ -f "models/$REFA/adapter_model.safetensors" ] || die 2 "models/$REFA missing"
  if [ -z "${GATE_SIM:-}" ]; then
    [ -f "$HOME/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/$REV/config.json" ] \
      || die 2 "base revision $REV is not in the HF cache (HF_HUB_OFFLINE=1 would fail)"
    if pgrep -f "od_gcp.py predict" >/dev/null; then die 2 "another od_gcp.py job is running on this VM: one job at a time"; fi
    if [ -n "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null)" ]; then die 2 "the GPU is busy"; fi
    local free; free=$(df -Pk . | awk 'NR==2 {print int($4/1048576)}')
    [ "$free" -ge 3 ] || die 2 "only ${free} GB free on disk (need >= 3 GB for the job-3 preds)"
  fi
}

vm_preflight() {
  ev "PREFLIGHT (job 3) in $LEAN (python $PY)"
  vm_preflight_common
  [ -f "$G/conds/probe_go.json" ] || die 2 "A8' 0b has not run (no $G/conds/probe_go.json): run launch0 first"
  [ "$(jget "$G/conds/probe_go.json" 'r["pass"]')" = True ] \
    || die 2 "A8' 0b was NO GO: F7 does not reproduce the failure; redesign F7 (no H100 spend, no job 3)"
  local s f
  for s in ${STD//,/ }; do [ -f "data/$s.jsonl" ] || die 2 "data/$s.jsonl missing"; done
  for f in $TRAIN12 $FIX2DATA; do [ -f "data/$f.jsonl" ] || die 2 "data/$f.jsonl missing (the ship verdict would be NOT FINAL / the A8' unseen check)"; done
  [ -f "data/$MEMO.jsonl" ] || die 2 "data/$MEMO.jsonl missing (the 6 (d) memo read after a FINAL SHIP)"
  grep -q 'TS_GATE' gate/teacher_switch_l4.sh || die 2 "gate/teacher_switch_l4.sh lacks the C4 patch (A8' section M: prereg_drafts/teacher_switch_l4_c4.patch)"
  "$PY" gate/check_unseen_fix2.py > "$G/preflight_unseen.txt" 2>&1 \
    || die 2 "check_unseen_fix2 FAILED (A8' C.7): $(tail -n 1 "$G/preflight_unseen.txt")"
  STORED=$(stored_ref) || die 2 "cannot import gate_dev.py"
  ev "gate_dev.py sha256 $(sha_of gate_dev.py | cut -c1-16)...; STORED_REF[4b] = $STORED"
  [ "$STORED" = q35_4b_pxE_parity ] || die 2 "STORED_REF[4b] is $STORED, not q35_4b_pxE_parity (A7)"
  for s in ${SPLITS9//,/ }; do [ -f "preds_$s/$STORED.jsonl" ] || die 2 "stored REF preds_$s/$STORED.jsonl missing"; done
  for s in ${STD//,/ }; do [ -f "preds_$s/$C1.jsonl" ] || die 2 "job-1 C1 read preds_$s/$C1.jsonl missing (A8' R needs it)"; done
  for s in ${SPLITS9//,/ }; do [ -f "preds_$s/${C1}_perm.jsonl" ] || die 2 "job-1 C1 read preds_$s/${C1}_perm.jsonl missing"; done
  ev "PREFLIGHT OK"
}

# ------------------------------------------------------------------------------------------------ VM: A8' 0b
vm_probe0() {
  PHASE=vm; mkdir -p "$G"
  ev "===== A8' 0b START (C1 $C1 and 4B-E $REFA read the probe + devx with gate settings, tag _p0)"
  vm_preflight_common
  predict "$C1" _p0 "$F7S" ""
  predict "$REFA" _p0 "$F7S" ""
  if cond probe_go gate/fix2_conditions.py probe-go "${C1}_p0" "${REFA}_p0"; then
    ev "A8' 0b: GO. F7 reproduces the failure. Next: owner GO for the Modal top-up, then 'launch' (job 3)."
  else
    ev "A8' 0b: NO GO. F7 does not capture the failure: redesign F7 before any H100 spend (the probe is spent)."
  fi
  ev "===== A8' 0b END (the VM stays up for job 3; 'stop' it on the Mac if job 3 does not follow soon)"
}

# ------------------------------------------------------------------------------------------------ VM: job 3
c4_ready() { [ -f "$MANC4" ] && [ -f "models/$C4/train_meta.json" ] && sha_check "$MANC4" > "$G/preflight_c4.txt" 2>&1; }
wait_c4() {
  local t0; t0=$(date +%s)
  ev "WAIT for C4 ($MANC4 + models/$C4; at most $WAIT_C4_MAX_MIN min)"
  while :; do
    if c4_ready; then ev "C4 present and matches $MANC4"; return 0; fi
    [ $(( ($(date +%s) - t0) / 60 )) -lt "$WAIT_C4_MAX_MIN" ] || die 12 "C4 did not arrive within $WAIT_C4_MAX_MIN min: job 3 stops before any C4 read (re-launch continues: every finished read is kept)"
    sleep "${WAIT_POLL_S:-60}"
  done
}

vm_job3() {
  PHASE=vm; mkdir -p "$G"
  ev "===== JOB 3 START (REF $REFA as $FRESH3; C1R $C1R; C4 $C4)"
  vm_preflight
  # E2-E4: independent of C4 (they run while C4 trains on Modal)
  predict "$REFA" _fresh3 "$STD" ""
  predict "$REFA" _fresh3_perm "$SPLITS9" 1
  look refparity3 refparity "$FRESH3" "$STORED"
  parity_gate refparity3 "$FRESH3"
  predict "$C1" _r3 "$STD,$F7S" ""
  predict "$C1" _r3_perm "$SPLITS9" 1
  cond R gate/fix2_conditions.py c1parity "$C1R" "$C1" \
    || die 20 "A8' R FAILED: the C1 re-read does not reproduce job 1 (pipeline drift). Stop and consult the owner; no C4 read. After a repair: 'vm-reset-pre-c4 NOTE' then 'launch' (A8' F)."
  # report-only exact 2-view reads of C1 (READOUT_DEV proxy caveat): now if C4 is not here yet (idle time), else after
  # the verdict, so they never delay it
  if ! c4_ready; then
    predict "$C1" _r3_tta "$SPLITS9" "" --tta
    predict "$C1" _r3_perm_tta "$SPLITS9" 1 --tta
  fi
  # E5: C4
  wait_c4
  predict "$C4" "" "$STD,$F7S" ""
  predict "$C4" _perm "$SPLITS9" 1
  local outcome=""
  if ! cond P gate/fix2_conditions.py precheck "$C4" "$C1R"; then
    outcome="noship-P:$C4"
  elif ! cond N gate/noninf_check.py "$C4" "$C1R"; then
    outcome="noship-N:$C4"
  else
    look ship_c4 ship "$C4" "$FRESH3"
    local v; v="$(jget "$G/look_ship_c4.json" 'r["verdict"]')|$(jget "$G/look_ship_c4.json" 'r["final"]')"
    ev "SHIP LOOK C4: $C4 vs $FRESH3 -> ${v%%|*} (final ${v##*|})"
    if [ "${v##*|}" != True ]; then outcome="not-final:$C4"
    elif [ "${v%%|*}" = SHIP ]; then outcome="ship:$C4"
    else outcome="noship:$C4"; fi
  fi
  summary "$outcome"
  # REPORT ONLY from here: nothing below can change the verdict
  predict "$C1" _r3_tta "$SPLITS9" "" --tta
  predict "$C1" _r3_perm_tta "$SPLITS9" 1 --tta
  predict "$C4" _tta "$SPLITS9" "" --tta
  predict "$C4" _perm_tta "$SPLITS9" 1 --tta
  "$PY" gate/twoview_report.py --json "$G/twoview.json" \
    --model "C1R:$C1R:${C1R}_tta:${C1R}_perm:${C1R}_perm_tta" \
    --model "C4:$C4:${C4}_tta:${C4}_perm:${C4}_perm_tta" > "$G/twoview.txt" 2>&1 \
    && sed 's/^/    /' "$G/twoview.txt" | tee -a "$G/events.log" || ev "twoview_report failed (report only): $(tail -n 2 "$G/twoview.txt" | tr '\n' ' ')"
  if [ "${outcome%%:*}" = ship ]; then
    predict "$C4" _2v "$SPLITS9" "" --tta-choice
    ev "FINAL SHIP: the 6 (d) memorisation read of C4 (teacher_switch_l4.sh vm-memo with job 3's settings)"
    NO_SHUTDOWN=1 TS_GATE=gate/gate_4b_fix2_l4.sh TS_G="$G" TS_FRESH="$FRESH3" TS_MANA="$MANC4" \
      bash gate/teacher_switch_l4.sh vm-memo "$C4" >> "$G/vm-memo.out" 2>&1 || ev "memo read FAILED (see $G/vm-memo.out)"
  fi
  ev "===== JOB 3 END ($outcome)"
  vm_shutdown
}

summary() {
  "$PY" - "$1" "$G" <<'EOF' | tee -a "$G/events.log"
import json, sys
from pathlib import Path
outcome, G = sys.argv[1], Path(sys.argv[2])
looks, conds = {}, {}
for p in sorted(G.glob("look_*.json")):
    r = json.loads(p.read_text())
    k = p.stem[5:]
    if r["mode"] == "ship":
        looks[k] = {"cand": r["cand"], "ref": r["ref"], "verdict": r["verdict"], "final": r["final"],
                    "primary": {x: r["primary"][x] for x in ("diff", "lo", "hi", "pass")}, "failed": r["failed"],
                    "unmeasured": r["unmeasured"], "not_final": r["not_final"]}
    elif r["mode"] == "refparity":
        looks[k] = {x: r[x] for x in ("fresh", "stored", "pass", "counts", "agree", "mean_dp", "max_dp", "acc_diff")}
for p in sorted((G / "conds").glob("*.json")):
    r = json.loads(p.read_text())
    conds[p.stem] = {"pass": r.get("pass"), "checks": [(c.get("name"), c.get("pass")) for c in r.get("checks", [])]}
text = {"ship:": "SHIP {} (A8': R, P and N pass and the one look is SHIP + FINAL vs the fresh 4B-E read)",
        "noship:": "DO NOT SHIP {} (A8' H: 4B-E ships, PREREG 5.7)",
        "noship-P:": "DO NOT SHIP {} (A8' P failed: no ship look; 4B-E ships)",
        "noship-N:": "DO NOT SHIP {} (A8' N failed: no ship look; 4B-E ships)",
        "not-final:": "NOT FINAL {}: C4 does not ship and the look is not repeated (A8' H; A7 reading 3): 4B-E ships"}
d = next((v.format(outcome.split(":", 1)[1]) for k, v in text.items() if outcome.startswith(k)), outcome)
out = {"outcome": outcome, "decision": d, "looks": looks, "conditions": conds}
(G / "summary.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"SUMMARY: {d}")
for k, v in {**looks, **conds}.items():
    print(f"   {k}: {json.dumps(v)[:300]}")
EOF
}

# ------------------------------------------------------------------------------------------------ VM: restart before C4
vm_reset_pre_c4() {  # NOTE: A8' F / H: refparity3 or R failed (or gave no verdict) BEFORE any C4 read; the VM is repaired
  local note=${1:-}; local s n f
  [ -n "$note" ] || { echo "vm-reset-pre-c4 NOTE: a dated note on the repair is required"; return 1; }
  for s in ${STD//,/ } ${F7S//,/ }; do
    if ls "preds_$s/$C4"*.jsonl >/dev/null 2>&1; then echo "a C4 read exists (preds_$s/$C4*): no reset after any C4 read"; return 1; fi
  done
  for f in "$G/conds/P.json" "$G/conds/N.json" "$G/looks/ship_c4.done" "$G/look_ship_c4.json"; do
    [ -e "$f" ] && { echo "$f exists: no reset after P, N or the ship look"; return 1; }
  done
  local d; d="$G/reset_$(date -u +%Y%m%dT%H%M%SZ)"; mkdir -p "$d/preds" || return 1
  printf '%s\n%s\n' "$(ts) vm-reset-pre-c4 (A8' F / H): job 3 restarts on a repaired VM before any C4 read" "$note" > "$d/NOTE.txt"
  for f in "$G/conds/R.json" "$G/conds/R.txt" "$G/look_refparity3.json" "$G/look_refparity3.txt" "$G/looks/refparity3.done"; do
    [ -e "$f" ] && mv "$f" "$d/" 
  done
  for s in ${STD//,/ } ${F7S//,/ }; do
    for n in "$FRESH3" "$C1R"; do
      for f in "preds_$s/$n"*; do [ -e "$f" ] && { mkdir -p "$d/preds/preds_$s"; mv "$f" "$d/preds/preds_$s/"; }; done
    done
  done
  ev "RESET before any C4 read: records and the REF fresh3 / C1R reads moved to $d ($(head -c 200 "$d/NOTE.txt" | tail -n 1))"
}

# ------------------------------------------------------------------------------------------------ Mac phases
mac_pairs() { "$PY" gate/fix2_conditions.py pairs; }

mac_fetch() {  # PROFILE: Modal volume -> $BACKUP (one local copy), checked first
  local prof=$1 M=$LEAN/../.venv/bin/modal stage f
  [ -e "$BACKUP/adapter_model.safetensors" ] && { echo "$BACKUP exists; not fetched again"; return 0; }
  stage=$LEAN/handoff/fix2_gate_dl/final; mkdir -p "$stage"
  for f in $ADAPTER_FILES; do
    MODAL_PROFILE=$prof "$M" volume get --force opendecide "models/$C4/$f" "$stage/" || { echo "fetch failed: $f"; return 1; }
  done
  "$PY" gate/check_adapter_fix2.py "$stage" --c1 "$C1_BACKUP" || { echo "C4 adapter check FAILED (kept in $stage)"; return 1; }
  mkdir -p "$BACKUP"; for f in "$stage"/*; do mv "$f" "$BACKUP/"; done
  echo "fetched into $BACKUP"
}

mac_manifest() {
  local s f stored
  if [ -z "${ALLOW_DIRTY:-}" ] && git -C "$LEAN" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    # every file the manifest hashes, every file the VM runs or imports, and every pre-registered builder / record
    # (A8' section M): an uncommitted edit to any of them would otherwise be hashed and pushed with PUSH_FIXES
    local dirty; dirty=$(git -C "$LEAN" status --porcelain -- gate_dev.py PREREG_FINAL.md ship_unseen_sources.json \
      od_gcp.py decoder_io.py prism_x.py writeblock.py \
      runs/q35_4b_fix2.json runs/README.md extra/build_fix2.py extra/build_fix1.py extra/fix2_spawn.py \
      extra/fix2_dryrun.py extra/fix2_dryrun.json extra/fix2_ohs3_blind.py \
      gate/gate_4b_fix2_l4.sh gate/check_unseen_fix2.py gate/check_adapter.py gate/check_adapter_fix1.py \
      gate/check_adapter_fix2.py gate/fix2_conditions.py gate/noninf_check.py gate/twoview_report.py "$PAIRS" \
      gate/teacher_switch.py gate/teacher_switch_l4.sh gate/memo4b_train_rows.json gate/RUNBOOK_fix2.md \
      yn2b/check_unseen.py yn2b/yn2b_common.py yn2b/check_yn2b.py yn2b/f7_precheck.py yn2b/f7_precheck_fix2.json \
      yn2b/f7_precheck_fix2_ohs3.json yn2b/fix2_ohs3_blind.json yn2b/F7_COVERAGE_CHECKLIST.md \
      data/v14_parts/fix2_counts.json data/v14_parts/f7_counts.json data/v14_parts/f7_holdout_spec.json \
      data/v14_parts/f7_lexicon.json yn2b/f7_fix2_drops.json yn2b/f7_source_label_audit.json \
      yn2b/label_audit_known_bad_ids.json yn2b/decontam_only/negation_benchmarks.json \
      yn2b/decontam_only/recalled_negation_templates.json yn2b/f7_decide2_preds.jsonl yn2b/f7_devx_decide2_lf.json \
      yn2b/f7_devx_build.py yn2b/f7_devx_pool_scan.py yn2b/f7_blind_read_sample4.py yn2b/f7_blind_read_compare.py \
      gate/superseded/fix2_pairs.r5_probe_2oct.json gate/tests/test_fix2_conditions.py gate/tests/test_noninf_check.py \
      gate/tests/sim_gate_fix2.py gate/tests/predict_stub_fix2.py yn2b/tests/test_gen3_nested_negation.py yn2b/SPEC.md \
      prereg_drafts/A8prime.md \
      golden_src/gen3/f7_repair_r5.py golden_src/gen3/f7_repair_r6.py golden_src/gen3/gen3_nested_negation.py \
      golden_src/gen3/nn_lexicon.py golden_src/gen3/v3_nested_negation.py golden_src/gen3/mv_core.py)
    if [ -n "$dirty" ]; then
      echo "uncommitted changes to the pre-registered files (commit A8' first, or ALLOW_DIRTY=1 for a dry run):"
      echo "$dirty" | sed 's/^/   /'; return 1
    fi
    git -C "$LEAN" show HEAD:opendecide-data/lean/PREREG_FINAL.md 2>/dev/null | grep -q "$A8P" \
      || { echo "$A8P is not in the committed PREREG_FINAL.md (HEAD)"; return 1; }
    echo "A8' committed (HEAD $(git -C "$LEAN" rev-parse --short HEAD); gate_dev.py $(sha_of gate_dev.py | cut -c1-16)...)"
  fi
  [ -f "$PAIRS" ] || { echo "$PAIRS missing: run 'pairs' (A8' 0a) first"; return 1; }
  stored=$(stored_ref)
  {
    sha_of gate_dev.py od_gcp.py decoder_io.py prism_x.py writeblock.py ship_unseen_sources.json gate/gate_4b_fix2_l4.sh \
      gate/check_unseen_fix2.py gate/fix2_conditions.py gate/noninf_check.py gate/twoview_report.py \
      gate/teacher_switch.py gate/teacher_switch_l4.sh gate/memo4b_train_rows.json "$PAIRS" \
      yn2b/check_unseen.py yn2b/yn2b_common.py runs/q35_4b_fix2.json
    for s in ${STD//,/ }; do sha_of "data/$s.jsonl"; done
    for s in ${SPLITS9//,/ }; do [ -f "data/${s}_relations.jsonl" ] && sha_of "data/${s}_relations.jsonl"; done
    for s in $F7DATA; do sha_of "data/$s.jsonl"; done
    for f in $TRAIN12 $FIX2DATA $MEMO; do sha_of "data/$f.jsonl"; done
    for s in ${SPLITS9//,/ }; do sha_of "preds_$s/$stored.jsonl" "preds_$s/$stored.meta.json"; done
    for s in ${STD//,/ }; do sha_of "preds_$s/$C1.jsonl" "preds_$s/$C1.meta.json"; done
    for s in ${SPLITS9//,/ }; do sha_of "preds_$s/${C1}_perm.jsonl" "preds_$s/${C1}_perm.meta.json"; done
  } > "$MAN" || return 1
  {
    if [ -d "models/$C1" ]; then sha_of "models/$C1/adapter_config.json" "models/$C1/adapter_model.safetensors"
    else (cd "$C1_BACKUP" && sha_of adapter_config.json adapter_model.safetensors) | sed "s|  |  models/$C1/|"; fi
    if [ -d "models/$REFA" ]; then sha_of "models/$REFA/adapter_config.json" "models/$REFA/adapter_model.safetensors"
    else (cd "$REF_BACKUP" && sha_of adapter_config.json adapter_model.safetensors) | sed "s|  |  models/$REFA/|"; fi
  } > "$MANA" || return 1
  grep -q "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078  models/$C1/adapter_model.safetensors" "$MANA" \
    || { echo "C1 in $MANA is not the gated C1 (507d1c29...)"; return 1; }
  echo "wrote $MAN ($(nlines "$MAN") files, stored REF $stored) and $MANA ($(nlines "$MANA") files)"
}

mac_manifest_c4() {
  [ -e "$BACKUP/adapter_model.safetensors" ] || { echo "$BACKUP missing: run 'fetch' first"; return 1; }
  "$PY" gate/check_adapter_fix2.py "$BACKUP" --c1 "$C1_BACKUP" > /dev/null || { echo "check_adapter_fix2 FAILED"; return 1; }
  (cd "$BACKUP" && sha_of $ADAPTER_FILES) | sed "s|  |  models/$C4/|" > "$MANC4" || return 1
  echo "wrote $MANC4 ($(nlines "$MANC4") files; C4 adapter $(grep adapter_model "$MANC4" | cut -c1-16)...)"
}

vm_verify() {  # MANIFEST...: names of files that differ or are missing on the VM (empty = all OK)
  local m list=""
  for m in "$@"; do list="$list $m"; done
  gssh "cd ~/lean && for m in $list; do [ -f \$m ] || { echo \"\$m: FAILED open or read\"; continue; }; sha256sum -c \$m 2>/dev/null; done" \
    | tr -d '\r' | failed_paths
}

mac_push() {
  [ -f "$MAN" ] && [ -f "$MANA" ] || { echo "run 'manifest' first"; return 1; }
  gscp --recurse "$LEAN/gate" "$VM:~/lean/" || return 1
  gssh "mkdir -p ~/lean/yn2b ~/lean/runs ~/lean/data/v14_parts ~/lean/models" || return 1
  gscp "$LEAN/yn2b/check_unseen.py" "$LEAN/yn2b/yn2b_common.py" "$VM:~/lean/yn2b/" || return 1
  gscp "$LEAN/runs/q35_4b_fix2.json" "$VM:~/lean/runs/" || return 1
  gscp "$LEAN/PREREG_FINAL.md" "$LEAN/gate_dev.py" "$VM:~/lean/" || return 1
  gscp "$LEAN/data/v14_parts/fix2_train.jsonl" "$LEAN/data/v14_parts/fix2_relations.jsonl" "$VM:~/lean/data/v14_parts/" || return 1
  local s; for s in $F7DATA; do gscp "$LEAN/data/$s.jsonl" "$VM:~/lean/data/" || return 1; done
  gscp "$LEAN/data/$MEMO.jsonl" "$VM:~/lean/data/" || return 1
  if ! gssh "test -e ~/lean/models/$C1/adapter_model.safetensors"; then gscp --recurse "$C1_BACKUP" "$VM:~/lean/models/" || return 1; fi
  if ! gssh "test -e ~/lean/models/$REFA/adapter_model.safetensors"; then gscp --recurse "$REF_BACKUP" "$VM:~/lean/models/" || return 1; fi
  local bad; bad=$(vm_verify "$MAN" "$MANA")
  if [ -z "$bad" ]; then echo "VM manifests OK"; return 0; fi
  echo "files that differ or are missing on the VM:"; echo "$bad" | sed 's/^/   /'
  if [ -z "${PUSH_FIXES:-}" ]; then echo "re-run with PUSH_FIXES=1 to copy the Mac's versions to the VM"; return 1; fi
  local f
  for f in $bad; do
    case "$f" in models/*) echo "adapter file $f differs on the VM: check by hand (never overwritten here)"; return 1 ;; esac
    [ -e "$LEAN/$f" ] || { echo "the Mac has no $f to copy"; return 1; }
    gssh "mkdir -p ~/lean/$(dirname "$f")" && gscp "$LEAN/$f" "$VM:~/lean/$f" || return 1
  done
  bad=$(vm_verify "$MAN" "$MANA")
  [ -z "$bad" ] && echo "VM manifests OK after fixes" || { echo "still differing: $bad"; return 1; }
}

mac_push_c4() {  # the adapter first, its manifest last (vm-job3 polls for the manifest, then verifies it)
  [ -f "$MANC4" ] || { echo "run 'manifest-c4' first"; return 1; }
  if ! gssh "test -e ~/lean/models/$C4"; then gscp --recurse "$BACKUP" "$VM:~/lean/models/" || return 1; fi
  gscp "$MANC4" "$VM:~/lean/$MANC4.pending" || return 1
  local bad; bad=$(vm_verify "$MANC4.pending")
  [ -z "$bad" ] || { echo "C4 on the VM differs from $MANC4: $bad (check by hand; adapters are never overwritten here)"; return 1; }
  gssh "cd ~/lean && mv $MANC4.pending $MANC4" && echo "C4 on the VM matches $MANC4 (vm-job3 continues by itself)"
}

mac_pull() {
  local d n
  for d in $(echo "$STD,$F7S" | tr ',' '\n' | sed 's/^/preds_/') "preds_$MEMO"; do
    mkdir -p "$d"
    for n in "$FRESH3" "$C1R" "${C1}_p0" "${REFA}_p0" "$C4"; do gscp "$VM:~/lean/$d/$n*" "$d/" >/dev/null 2>&1 || true; done
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
# ---- Mac, before the A8' commit
$PY gate/fix2_conditions.py pairs                                          # A8' 0a -> $PAIRS (frozen; part of the commit)
# ---- commit A8' (PREREG_FINAL.md + section M files), then:
bash gate/gate_4b_fix2_l4.sh manifest && bash gate/gate_4b_fix2_l4.sh start && bash gate/gate_4b_fix2_l4.sh push
bash gate/gate_4b_fix2_l4.sh launch0                                         # A8' 0b on od-l4 (about 15 min)
# ---- VM: vm-probe0
$(predict_cmd "$C1" _p0 "$F7S" "")
$(predict_cmd "$REFA" _p0 "$F7S" "")
$PY gate/fix2_conditions.py probe-go ${C1}_p0 ${REFA}_p0 --json $G/conds/probe_go.json   # NO GO -> redesign F7
# ---- GO: owner GO for the H100 top-up (extra/fix2_spawn.py), then at once:
bash gate/gate_4b_fix2_l4.sh launch                                          # job 3 part 1 runs while C4 trains
# ---- VM: vm-job3 (od-l4; about 6.5-7.5 L4-hours with the report reads; the verdict about 4 h after launch)
$PY gate/check_unseen_fix2.py                                              # A8' C.7 (preflight; no look)
$(predict_cmd "$REFA" _fresh3 "$STD" "")
$(predict_cmd "$REFA" _fresh3_perm "$SPLITS9" 1)
$PY gate_dev.py $FRESH3 $stored --mode refparity --json $G/look_refparity3.json   # FAIL -> stop, consult owner
$(predict_cmd "$C1" _r3 "$STD,$F7S" "")
$(predict_cmd "$C1" _r3_perm "$SPLITS9" 1)
$PY gate/fix2_conditions.py c1parity $C1R $C1 --json $G/conds/R.json           # A8' R; FAIL -> stop, consult owner
$(predict_cmd "$C1" _r3_tta "$SPLITS9" "" --tta)        # report only (exact 2-view): while waiting for C4, else after the verdict
$(predict_cmd "$C1" _r3_perm_tta "$SPLITS9" 1 --tta)     # report only (independent 2-view)
# ... waits for C4 (Mac: fetch jaypatil-duke -> check -> manifest-c4 -> push-c4)
$(predict_cmd "$C4" "" "$STD,$F7S" "")
$(predict_cmd "$C4" _perm "$SPLITS9" 1)
$PY gate/fix2_conditions.py precheck $C4 $C1R --json $G/conds/P.json          # A8' P; FAIL -> no look
$PY gate/noninf_check.py $C4 $C1R --json $G/conds/N.json                      # A8' N; FAIL -> no look
$PY gate_dev.py $C4 $FRESH3 --mode ship --size 4b --json $G/look_ship_c4.json        # the one C4 look (A8' G)
# report only (after the verdict):
$(predict_cmd "$C4" _tta "$SPLITS9" "" --tta)
$(predict_cmd "$C4" _perm_tta "$SPLITS9" 1 --tta)
$PY gate/twoview_report.py --model C1R:$C1R:${C1R}_tta:${C1R}_perm:${C1R}_perm_tta --model C4:$C4:${C4}_tta:${C4}_perm:${C4}_perm_tta --json $G/twoview.json
# only after a FINAL SHIP:
$(predict_cmd "$C4" _2v "$SPLITS9" "" --tta-choice)     # A5 temperature rule + OHS-3 DEV smoke reference
NO_SHUTDOWN=1 TS_GATE=gate/gate_4b_fix2_l4.sh TS_G=$G TS_FRESH=$FRESH3 TS_MANA=$MANC4 bash gate/teacher_switch_l4.sh vm-memo $C4
# ---- Mac, after pull: teacher (A8' I) and the report (never decisive)
$PY gate/teacher_switch.py check $C4 $FRESH3 --ship-json $G/look_ship_c4.json --json $G/teacher_switch.json
$PY gate_dev.py $C4 $C1 --mode confirm
EOF
}

cmd=${1:-}; shift || true
case "$cmd" in
  pairs) mac_pairs ;;
  fetch) [ $# -ge 1 ] || { echo "fetch PROFILE"; exit 1; }; mac_fetch "$1" ;;
  check) "$PY" gate/check_adapter_fix2.py "$BACKUP" --c1 "$C1_BACKUP" ;;
  manifest) mac_manifest ;;
  manifest-c4) mac_manifest_c4 ;;
  start) gcloud compute instances start "$VM" --zone "$Z" --project "$P" ;;
  stop) gcloud compute instances stop "$VM" --zone "$Z" --project "$P" ;;
  push) mac_push ;;
  push-c4) mac_push_c4 ;;
  launch0) gssh "cd ~/lean && mkdir -p $G && NO_SHUTDOWN=1 nohup bash gate/gate_4b_fix2_l4.sh vm-probe0 > $G/vm-probe0.out 2>&1 < /dev/null & echo launched vm-probe0" ;;
  launch) e="${NO_SHUTDOWN:+NO_SHUTDOWN=1 }"
    gssh "cd ~/lean && mkdir -p $G && ${e}nohup bash gate/gate_4b_fix2_l4.sh vm-job3 > $G/vm-job3.out 2>&1 < /dev/null & echo launched ${e}vm-job3" ;;
  status) gssh "cd ~/lean && tail -n 25 $G/events.log; echo; tail -n 3 $G/reads.log; nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv" ;;
  pull) mac_pull ;;
  report) mac_report ;;
  vm-probe0) vm_probe0 ;;
  vm-reset-pre-c4) PHASE=vm; vm_reset_pre_c4 "${1:-}" ;;
  vm-job3) vm_job3 ;;
  plan) plan ;;
  *) sed -n '2,30p' "$0"; exit 1 ;;
esac
