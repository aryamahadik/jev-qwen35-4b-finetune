#!/bin/bash
# C2 training chain (PREREG A37 i/k, A42-D 2, 9.1). From lean/ :
#   nohup bash c2_build/train/c2_chain.sh start [--ack-pending]  > c2_build/train/logs/c2_chain.log 2>&1 &   # mahadikarya2
#   bash c2_build/train/c2_chain.sh copy                          # when it printed RELAY: run P2 -> P3, free, no compute
#   nohup bash c2_build/train/c2_chain.sh resume mahadikarya3     > c2_build/train/logs/c2_chain_p3.log 2>&1 &
#   nohup bash c2_build/train/c2_chain.sh resume mahadikarya2 ... (crash relaunch, only with the owner's OK)
# Only the OWNER's GO (train/OWNER_GO_C2.txt, A37 l) starts `start`. MODAL_PROFILE is exported on EVERY modal call; the
# profile must be mahadikarya2 or mahadikarya3 (free credit first; the card account is never launched from here).
# Each launch runs only if the check before it exits 0. Every segment has a SERVER-SIDE time cap (relay
# --stop-after-min is an absolute end time that survives a preemption restart):
#   seg1 steps 0-100   cap 30 min    seg2 steps 100-300  cap 35 min   (log_every 1 / 10)
#   proj (c2_check.py): A37 (k) with A42-D 2.3: STOP and ask when the steps-100-300 projection is above T_max
#   seg3.. to the end: each cap = min(T_max budget left, free credit left on the account, 540 min) from c2_check.py
#   proj / seg / resume. When the credit is the binding cap and the account has < 10 min left: RELAY (exit 3).
# Ledger lines before and after every segment: lean/logs/budget_ledger.md (spend_guard) and logs/c2_ledger.md (C2 cap
# $40, T_max, training spent). Segment wall times: logs/c2_segments.jsonl (counted as spend while billing lags).
# The snap monitor (c2_build/snap_monitor_c2.py, A37 k stop rule) must be ALIVE before seg3 and is re-checked before
# every segment; a dead monitor, a fired rule or an escalation ends the chain with NO candidate.
set -uo pipefail
cd "$(dirname "$0")/../.."          # lean/
PY=${C2_PY:-../.venv/bin/python}; M=${C2_MODAL:-../.venv/bin/modal}; T=c2_build/train; L=$T/logs; CB=c2_build
CFG=runs/q35_4b_c2.json; NAME=q35_4b_c2; ENTRY=$T/modal_od_c2.py::relay
SEGLOG=$CB/logs/c2_seg.log; MONLOG=$CB/logs/snap_monitor_c2.log; MONPID=$CB/logs/snap_monitor_c2.pid
STOPF=$CB/logs/snap_monitor_c2_stop.json; ESCF=$CB/logs/snap_monitor_c2_escalation.json; DEADF=$L/c2_monitor_dead.json
FINAL=logs/relay_${NAME}_final.json
MON_START_S=${C2_MON_START_S:-45}; MON_POLL_S=${C2_MON_POLL_S:-60}; MAXSEG=${C2_MAXSEG:-6}
mkdir -p $L $CB/logs
CMD=${1:-}; shift || true
P=mahadikarya2
case "$CMD" in
  start) P=mahadikarya2;;
  resume) P=${1:-}; shift || true;;
  copy) P=mahadikarya2;;
  *) echo "usage: c2_chain.sh start [--ack-pending] | copy | resume <mahadikarya2|mahadikarya3>"; exit 2;;
esac
case "$P" in mahadikarya2|mahadikarya3) ;; *) echo "REFUSED: profile '$P' (free credit only: mahadikarya2, mahadikarya3)"; exit 2;; esac
export MODAL_PROFILE=$P
chk() { $PY -B $T/c2_check.py "$@"; }
led() { [ -n "${C2_TEST_NO_LEDGER:-}" ] && { echo "LEDGER (CPU test): $1"; return 0; }
        $PY c_build/endgame/spend_guard.py ledger $P "C2 training: $1" --payer "free credit" || true
        chk ledger "C2 training: $1" --profile $P > /dev/null || true; }
stop() { echo "CHAIN STOPPED: $1"; led "STOPPED: $1"; exit 1; }
seg() {  # seg <name> <relay args...>: records the open line and the wall time; returns the client's exit code
  local name=$1; shift; local s; s=$(date +%s)
  printf '{"seg":"%s","profile":"%s","start":%s,"open":true,"args":"%s"}\n' "$name" "$P" "$s" "$*" >> $L/c2_segments.jsonl
  MODAL_PROFILE=$P $M run --detach $ENTRY --config $CFG "$@" > >(tee -a $SEGLOG > $L/c2_$name.log) 2>&1
  local rc=$?
  printf '{"seg":"%s","profile":"%s","start":%s,"end":%s,"rc":%s,"args":"%s"}\n' "$name" "$P" "$s" "$(date +%s)" "$rc" "$*" \
    >> $L/c2_segments.jsonl
  return $rc
}
# ---- snap monitor liveness (A37 k stop rule): rc 0 = all reads done / clean end, 3 = rule fired, 4 = escalated, else DEAD
SMPID=; SMRC=
mon_reap() { if [ -n "$SMPID" ] && [ -z "$SMRC" ] && ! kill -0 "$SMPID" 2>/dev/null; then wait "$SMPID"; SMRC=$?; fi; }
mon_ok() { mon_reap; [ -z "$SMPID" ] || [ -z "$SMRC" ] || [ "$SMRC" = 0 ]; }
mon_dead() { [ -f $DEADF ] && return 0
  printf '{"unix":%s,"pid":"%s","rc":"%s","during":"%s"}\n' "$(date +%s)" "$SMPID" "$SMRC" "$1" > $DEADF
  echo "SNAP MONITOR NOT RUNNING ($1; rc=$SMRC; see $MONLOG): stop rule unwatched; no new segment"
  led "snap monitor not running ($1, rc=$SMRC): stop rule unwatched; chain launches no new segment; owner decides"; }
mon_gate() { [ -z "$SMPID" ] && return 0
  if [ -f $DEADF ] || ! mon_ok; then mon_dead "before $1"; stop "snap monitor not running before $1: segment NOT launched"; fi
  echo "snap monitor pid $SMPID alive before $1"; }
mon_start() {  # (re)start the monitor on the CURRENT profile; a monitor of another profile is stopped first
  rm -f $DEADF
  if [ -f $MONPID ] && kill -0 "$(cat $MONPID)" 2>/dev/null; then echo "stopping the running monitor $(cat $MONPID)"; kill "$(cat $MONPID)"; sleep 3; fi
  [ -f $CB/snap_monitor_c2.py ] || stop "no snap_monitor_c2.py: seg3 NOT launched (no owner waiver exists for C2)"
  nohup $PY -B $CB/snap_monitor_c2.py watch --profile $P --name $NAME --seg-log $SEGLOG > $MONLOG 2>&1 &
  SMPID=$!; SMRC=; sleep "$MON_START_S"
  if ! mon_ok || ! grep -q '"ev": "start"' $MONLOG; then mon_dead "${MON_START_S} s after start"
    stop "snap monitor not running after ${MON_START_S} s (see $MONLOG; on mahadikarya3 it needs PROFILES extended in snap_monitor_c2.py): segment NOT launched"; fi
  echo "snap monitor pid $SMPID (alive) on $P"; }
check_stops() {  # $1 = where; the rule driver's records end the chain
  [ -f $STOPF ] && stop "A37 (k) stop rule fired ($STOPF) $1: NO candidate; owner reviews"
  [ -f $ESCF ] && stop "snap monitor ESCALATED ($ESCF) $1: NO candidate until the owner decides"
  [ -f $DEADF ] && stop "snap monitor died ($DEADF) $1: stop rule unwatched; no candidate until the owner decides"; return 0; }
post300() {  # post300 <first segment number>: segments until `final`, a RELAY, or a STOP. c2_stop_after_min.txt is set.
  local K=0 SN MIN LIM rc
  while :; do
    K=$((K + 1)); SN=seg$(( $1 + K - 1 ))_$P
    [ "$K" -le "$MAXSEG" ] || stop "more than $MAXSEG post-300 segments in this invocation: owner decides"
    MIN=$(sed -n 1p $L/c2_stop_after_min.txt 2>/dev/null); LIM=$(sed -n 2p $L/c2_stop_after_min.txt 2>/dev/null)
    rm -f $L/c2_stop_after_min.txt            # one cap per segment: the next comes only from a GO check
    [[ "$MIN" =~ ^[0-9]+$ ]] && [ "$MIN" -ge 10 ] && [ "$MIN" -le 540 ] || stop "bad stop_after_min '$MIN' before $SN"
    check_stops "before $SN"
    led "$SN to the end/cap: BEFORE (cap $MIN min, limited by $LIM)"
    echo "== $SN cap $MIN min ($LIM) $(date -u)"
    mon_gate $SN
    seg $SN --expect-resume --stop-after-min "$MIN" & local SEGPID=$!
    while kill -0 "$SEGPID" 2>/dev/null; do
      sleep "$MON_POLL_S"; mon_ok || [ "$SMRC" = 3 ] || [ "$SMRC" = 4 ] || mon_dead "during $SN"
    done
    wait "$SEGPID"; rc=$?
    led "$SN: AFTER (client exit $rc)"
    check_stops "after $SN"
    [ $rc = 0 ] || stop "$SN client exit $rc (the app may still run to its cap: $M app list with MODAL_PROFILE=$P)"
    [ -f $FINAL ] && return 0
    echo "== $SN stopped at its cap without final: next cap from the budget $(date -u)"
    chk seg --profile $P; rc=$?
    if [ $rc = 3 ]; then led "RELAY NEEDED after $SN: free credit on $P is used up"
      echo "RELAY: run 'bash $T/c2_chain.sh copy' then 'resume mahadikarya3' (checkpoint kept on $P)"; exit 3; fi
    [ $rc = 0 ] || stop "seg check STOP after $SN (projection above T_max, rest does not fit, no progress, or spend unknown): owner decides"
  done; }
finish() {
  if [ -n "$SMPID" ]; then echo "== waiting for the snap monitor to read every snapshot $(date -u)"
    mon_reap; [ -n "$SMRC" ] || { wait "$SMPID"; SMRC=$?; }
    check_stops "on a late read"; [ "$SMRC" = 0 ] || stop "snap monitor ended rc=$SMRC without reading every snapshot: stop rule unchecked; no candidate"; fi
  [ -f $FINAL ] && { led "C2 FINAL"; echo "C2 TRAINING FINAL on $P: fetch the checkpoints (README step 5), then merge_avg.py"; exit 0; }
  stop "ended without final"; }

if [ "$CMD" = copy ]; then   # P2 -> P3: free volume copy of models/q35_4b_c2 (_ckpt, snaps), hash-checked
  [ ! -f $FINAL ] || { echo "REFUSED: final exists"; exit 1; }
  NAPPS=$($PY -B -c "
import json,subprocess,os
r=subprocess.run(['$M','app','list','--json'],capture_output=True,text=True,env={**os.environ,'MODAL_PROFILE':'mahadikarya2'})
a=json.loads(r.stdout[r.stdout.index('['):]) if '[' in r.stdout else None
print(-1 if a is None else sum(1 for x in a if str(x.get('State') or x.get('state') or '').lower()!='stopped' and (int(x.get('Tasks') or x.get('tasks') or 0)>0 or 'ephemeral' in str(x.get('State') or '').lower() or 'detached' in str(x.get('State') or '').lower())))")
  [ "$NAPPS" = 0 ] || { echo "REFUSED: $NAPPS app(s) running on mahadikarya2 (or app list unreadable)"; exit 1; }
  D=$T/tmp/relay_copy; rm -rf $D; mkdir -p $D
  MODAL_PROFILE=mahadikarya2 $M volume get opendecide models/$NAME $D/ || { echo "REFUSED: volume get failed"; exit 1; }
  $PY -B $T/c2_check.py verify-copy $D/$NAME || { echo "REFUSED: copied _ckpt failed its manifest check"; exit 1; }
  MODAL_PROFILE=mahadikarya3 $M volume put opendecide $D/$NAME models/$NAME || { echo "REFUSED: volume put failed (exists?)"; exit 1; }
  MODAL_PROFILE=mahadikarya3 $M volume ls opendecide models/$NAME/_ckpt | tee $L/c2_copy_ls.txt | head -20
  grep -q state.pt $L/c2_copy_ls.txt || { echo "REFUSED: state.pt not on mahadikarya3 after the put"; exit 1; }
  rm -rf $D; led "run copied mahadikarya2 -> mahadikarya3 (free): hash-checked"; echo "COPIED. Next: resume mahadikarya3"; exit 0
fi

if [ "$CMD" = start ]; then
  echo "== preflight $(date -u)"
  $PY -B $T/preflight_c2.py --fix-tmax "$@" || { echo "CHAIN STOPPED: preflight not GO (nothing launched, nothing charged)"; exit 1; }
  rm -f $L/c2_stop_after_min.txt $L/c2_check_seg.json $DEADF
  led "seg1 0-100: BEFORE (cap 30 min)"
  chk cap --min 30 --profile $P || stop "cap check for seg1 not GO"
  echo "== seg1 $(date -u)"
  seg seg1 --stop-at-step 100 --log-every 1 --stop-after-min 30 || stop "seg1 client exit $? (see $L/c2_seg1.log)"
  led "seg1: AFTER"
  echo "== first100 $(date -u)"
  chk first100 --profile $P || stop "first100 ABORT (A37 k: non-finite loss, or the chain guards); owner review"
  chk cap --min 35 --profile $P || stop "cap check for seg2 not GO"
  echo "== seg2 $(date -u)"
  seg seg2 --expect-resume --stop-at-step 300 --log-every 10 --stop-after-min 35 || stop "seg2 client exit $? (see $L/c2_seg2.log)"
  led "seg2 100-300: AFTER"
  echo "== proj $(date -u)"
  chk proj --profile $P; rc=$?
  [ $rc = 0 ] || { [ $rc = 3 ] && stop "proj RELAY at step 300 (credit): copy then resume mahadikarya3"; stop "proj STOP: the steps-100-300 projection is above T_max (A37 k) or the rest does not fit: ASK THE OWNER"; }
  mon_start
  post300 3
  finish
fi

if [ "$CMD" = resume ]; then
  rm -f $L/c2_stop_after_min.txt
  [ ! -f $FINAL ] || { echo "REFUSED: final exists"; exit 1; }
  check_stops "before resume"
  echo "== resume on $P $(date -u)"
  chk resume --profile $P; rc=$?
  [ $rc = 0 ] || stop "resume check not GO (rc $rc): owner decides"
  mon_start
  post300 $(( $(ls $L/c2_seg*.log 2>/dev/null | wc -l) + 1 ))
  finish
fi
