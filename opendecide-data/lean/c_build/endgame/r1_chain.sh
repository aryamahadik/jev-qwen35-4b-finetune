#!/bin/bash
# RUNBOOK D1-D5: round 1 on aryamhd (card), fully gated. From lean/:
#   nohup bash c_build/endgame/r1_chain.sh > c_build/endgame/logs/r1_chain.log 2>&1 &
# Each launch runs ONLY if the check before it exits 0 (GO); any REFUSED / ABORT / STOP / failed segment ends the chain
# with a ledger line and nothing more is launched. Every segment has a SERVER-SIDE time cap (relay --stop-after-min is
# an absolute end time that survives a preemption restart), so a sleeping Mac or a dead client cannot overspend:
#   D2 seg1 steps 0-100    cap 30 min  (<= $2.05)
#   D4 seg2 steps 100-300  cap 35 min  (<= $2.39)
#   D5 seg3, seg4, ... to the end (PREREG A28: hard stop $55, was $35). The ~12 h rest is longer than the 10 h Modal
#      function timeout (modal_od.py train_relay35), so it runs as relay segments that each resume from the checkpoint
#      the last one saved at its cap (--expect-resume; the trainer resumes exactly, RUN_KEYS are not part of the run's
#      identity). Each cap = min(budget left, 540) min, budget left = floor((55 - spent so far - 2) / 4.09 x 60):
#      seg3's from `r1_check.py proj`, each later one from `r1_check.py seg` (spend so far re-read; the D4 checks
#      re-run on the rest; STOP if it no longer fits). 540 = 600 min timeout - 60 min margin. Total <= $55.
# Billing + one ledger line before and after every segment (spend_guard.py ledger). Segment wall times go to
# logs/r1_segments.jsonl (proj counts them as spend so far, with the billing delta; the larger one is used).
# A28 R2: seg() writes an open line before each launch, and `r1_chain.sh relaunch` (D5 crash relaunch) launches
# through the same seg(), so every launch is in r1_segments.jsonl and every cap counts it. A28 R3: the relaunch is
# REFUSED while the chain's stop records exist or the snap monitor is neither running nor done, and watches it.
set -uo pipefail
cd "$(dirname "$0")/../.."          # lean/
PY=../.venv/bin/python; M=../.venv/bin/modal; E=c_build/endgame
P=aryamhd; CFG=runs/q35_4b_c_r1.json
MON_START_S=${R1_MON_START_S:-45}; MON_POLL_S=${R1_MON_POLL_S:-60}   # overridable only for the CPU test
led() { $PY $E/spend_guard.py ledger $P "round 1 (C r1): $1" --payer card || true; }
seg() {  # seg <name> <relay args...>; returns the client's exit code; records wall time
  local name=$1; shift
  local s; s=$(date +%s)
  # A28 R2: an OPEN line first: if this script dies mid-segment, r1_check.py counts the launch to its cap
  printf '{"seg":"%s","start":%s,"open":true,"args":"%s"}\n' "$name" "$s" "$*" >> $E/logs/r1_segments.jsonl
  MODAL_PROFILE=$P $M run --detach modal_od.py::relay --config $CFG "$@" > $E/logs/r1_$name.log 2>&1
  local rc=$?
  printf '{"seg":"%s","start":%s,"end":%s,"rc":%s,"args":"%s"}\n' "$name" "$s" "$(date +%s)" "$rc" "$*" \
    >> $E/logs/r1_segments.jsonl
  return $rc
}
if [ "${1:-}" = relaunch ]; then
  # RUNBOOK D5 crash relaunch (A28 R2; the owner's OK first), from lean/:
  #   nohup bash c_build/endgame/r1_chain.sh relaunch > c_build/endgame/logs/r1_relaunch.log 2>&1 &
  # ONE segment through the same seg() record as the chain (open line, then start/end/rc in logs/r1_segments.jsonl),
  # so the next `cap` / relaunch counts its wall time while billing still lags (~75 min). Its cap comes from
  # `r1_check.py relaunch` (= `cap`, after: no final, no app running on aryamhd, the app list itself OK, and the
  # recipe 5 stop rule driver clear). Never relaunch with `modal run` by hand: that segment would be invisible to the
  # next cap. Run this again only while the owner's OK holds.
  # A28 R3: REFUSED while the chain's stop records exist (snap_monitor_stop.json = rule fired, NO candidate this
  # round; snap_monitor_escalation.json; r1_monitor_dead.json) or the snap monitor is neither running
  # (logs/snap_monitor.pid) nor done (25/50/75% read); `r1_check.py mon` is polled every MON_POLL_S while the
  # segment trains (a monitor that dies is recorded in r1_monitor_dead.json, as the chain does) and once after it.
  STOPF=$E/logs/snap_monitor_stop.json; ESCF=$E/logs/snap_monitor_escalation.json; DEADF=$E/logs/r1_monitor_dead.json
  RN=$(grep -c '^{"seg":"relaunch[0-9]*","start":[0-9]*,"open":true' $E/logs/r1_segments.jsonl 2>/dev/null)
  SN=relaunch$(( ${RN:-0} + 1 ))
  rm -f $E/logs/r1_stop_after_min.txt
  [ -f $STOPF ] && { echo "RELAUNCH REFUSED: recipe 5 stop rule fired ($STOPF): NO candidate this round; owner reviews (nothing launched)"; exit 1; }
  [ -f $ESCF ] && { echo "RELAUNCH REFUSED: snap monitor ESCALATED ($ESCF): NO candidate until the owner decides (nothing launched)"; exit 1; }
  [ -f $DEADF ] && { echo "RELAUNCH REFUSED: snap monitor died ($DEADF): stop rule unwatched; owner decides (nothing launched)"; exit 1; }
  $PY $E/r1_check.py relaunch || { echo "RELAUNCH REFUSED: r1_check.py relaunch not GO (nothing launched)"; exit 1; }
  MIN=$(cat $E/logs/r1_stop_after_min.txt 2>/dev/null); rm -f $E/logs/r1_stop_after_min.txt
  [[ "$MIN" =~ ^[0-9]+$ ]] && [ "$MIN" -gt 0 ] && [ "$MIN" -le 540 ] || { echo "RELAUNCH REFUSED: bad stop_after_min '$MIN'"; exit 1; }
  rstop() { echo "RELAUNCH STOPPED: $1"; led "D5 $SN STOPPED: $1"; exit 1; }
  rdead() {  # once: the monitor stopped running before reading every snapshot (rule unwatched)
    [ -f $DEADF ] && return 0
    printf '{"unix":%s,"pid":"%s","rc":"","during":"%s"}\n' "$(date +%s)" "$(cat $E/logs/snap_monitor.pid 2>/dev/null)" "$1" > $DEADF
    echo "SNAP MONITOR NOT RUNNING ($1; see $E/logs/snap_monitor.log): recipe 5 stop rule unwatched"
    led "snap monitor not running ($1): stop rule unwatched; no further relaunch; owner decides"
  }
  led "D5 $SN (crash relaunch, owner OK; resumes at its checkpoint): BEFORE (cap $MIN min)"
  echo "== D5 $SN cap $MIN min $(date -u)"
  seg $SN --expect-resume --stop-after-min "$MIN" & SEGPID=$!
  while kill -0 "$SEGPID" 2>/dev/null; do   # re-check the monitor every MON_POLL_S while the segment trains
    sleep "$MON_POLL_S"
    $PY $E/r1_check.py mon > /dev/null; [ $? = 1 ] && rdead "during $SN"   # 3/4: it stopped the app itself
  done
  wait "$SEGPID"; rc=$?
  $PY $E/r1_check.py mon > /dev/null; [ $? = 1 ] && rdead "after $SN"
  led "D5 $SN: AFTER (client exit $rc)"
  [ -f $STOPF ] && rstop "recipe 5 stop rule fired ($STOPF; relay stopped by snap_monitor): NO candidate this round; owner reviews"
  [ -f $ESCF ] && rstop "snap monitor ESCALATED ($ESCF; relay stopped): NO candidate until the owner decides"
  [ -f $DEADF ] && rstop "snap monitor not running during $SN ($DEADF): stop rule unwatched; no candidate until the owner decides"
  if [ -f logs/relay_q35_4b_c_r1_final.json ]; then
    echo "== waiting for the snap monitor to read every snapshot $(date -u)"
    while :; do $PY $E/r1_check.py mon > /dev/null; mc=$?; [ $mc = 2 ] || break; sleep "$MON_POLL_S"; done
    case $mc in
      0) echo "ROUND 1 FINAL after $SN (snap monitor done, rule not fired; gate_c check_stop_rule re-checks it): go to RUNBOOK D6"; exit 0;;
      3) rstop "recipe 5 stop rule fired on a late read ($STOPF): NO candidate this round; owner reviews";;
      4) rstop "snap monitor ESCALATED on a late read ($ESCF): NO candidate until the owner decides";;
      *) rdead "after final"; rstop "snap monitor ended without reading every snapshot (mon $mc): stop rule unchecked; no candidate until the owner decides";;
    esac
  fi
  echo "RELAUNCH $SN ended without final (client exit $rc: cap reached or crash): owner decides; another one only via"
  echo "  'r1_chain.sh relaunch' (its cap counts this segment)"; exit 1
fi
rm -f $E/logs/r1_stop_after_min.txt $E/logs/r1_check_seg.json   # written only by a GO proj / seg of this chain
MAXSEG=4                              # A28: post-300 segments (2 expected); a guard, the $55 budget binds first
stop() { echo "CHAIN STOPPED: $1"; led "STOPPED: $1"; exit 1; }
# ---- snap monitor liveness (recipe 5 stop rule). SMPID is set once the monitor is started; SMRC once it exited.
# rc 0 = all 25/50/75% reads done, rule not fired (a clean end, also while seg3 still trains); 3 = rule fired (app
# stopped); 4 = escalated after 3 failed reads of one snapshot (app stopped); anything else = DEAD (rule unwatched).
SMPID=; SMRC=; STOPF=$E/logs/snap_monitor_stop.json; ESCF=$E/logs/snap_monitor_escalation.json
DEADF=$E/logs/r1_monitor_dead.json; rm -f $DEADF
mon_reap() { if [ -n "$SMPID" ] && [ -z "$SMRC" ] && ! kill -0 "$SMPID" 2>/dev/null; then wait "$SMPID"; SMRC=$?; fi; }
mon_ok() { mon_reap; [ -z "$SMPID" ] || [ -z "$SMRC" ] || [ "$SMRC" = 0 ]; }
mon_dead() {  # log once (chain log + ledger + record): the chain launches no new segment after this
  [ -f $DEADF ] && return 0
  printf '{"unix":%s,"pid":"%s","rc":"%s","during":"%s"}\n' "$(date +%s)" "$SMPID" "$SMRC" "$1" > $DEADF
  echo "SNAP MONITOR NOT RUNNING ($1; rc=$SMRC; see $E/logs/snap_monitor.log): recipe 5 stop rule unwatched; no new segment"
  led "snap monitor not running ($1, rc=$SMRC): stop rule unwatched; chain launches no new segment; owner decides"
}
mon_gate() {  # before every segment once the monitor was started
  [ -z "$SMPID" ] && return 0
  if [ -f $DEADF ] || ! mon_ok; then mon_dead "before $1"; stop "snap monitor not running before $1: segment NOT launched"; fi
  echo "snap monitor pid $SMPID alive before $1"
}

echo "== D1 preflight $(date -u)"
$PY $E/r1_check.py preflight || { echo "CHAIN STOPPED: preflight not GO (nothing launched, nothing charged)"; exit 1; }
led "D2 seg1 0-100: BEFORE (cap 30 min)"
echo "== D2 seg1 $(date -u)"
mon_gate seg1
seg seg1 --stop-at-step 100 --log-every 1 --stop-after-min 30 || stop "seg1 client exit $? (see $E/logs/r1_seg1.log)"
led "D2 seg1: AFTER"
echo "== D3 first100 $(date -u)"
$PY $E/r1_check.py first100 || stop "first100 ABORT (A21 c); _ckpt kept for diagnosis; owner review"
echo "== D4 seg2 $(date -u)"
mon_gate seg2
seg seg2 --expect-resume --stop-at-step 300 --stop-after-min 35 || stop "seg2 client exit $? (see $E/logs/r1_seg2.log)"
led "D4 seg2 100-300: AFTER"
echo "== D4 proj $(date -u)"
$PY $E/r1_check.py proj || stop "proj STOP (projection > \$55 (A28), or the rest does not fit the cap, or spend unknown); ask the owner before D5"
MIN=$(cat $E/logs/r1_stop_after_min.txt)
[[ "$MIN" =~ ^[0-9]+$ ]] && [ "$MIN" -gt 0 ] || stop "bad stop_after_min '$MIN'"
# recipe 5 stop rule (25% / 50% snapshots): its driver runs beside seg3 and stops the app when the rule fires
# (contract in RUNBOOK D5; preflight refused unless it exists + is CPU-tested, or the owner waived it)
# The monitor must be ALIVE before seg3 launches (it can die at start: OldSlice sha, lock, state of another run), and
# the chain waits for it after seg3: a rule that fires on late reads, or a monitor that did not read every snapshot,
# means NO candidate (recipe 5). Liveness: checked 45 s after start, right before every segment launch (mon_gate) and
# every 60 s while seg3 trains; a dead monitor is logged once (chain log, ledger, logs/r1_monitor_dead.json) and the
# chain launches no new segment and stops when seg3 ends. A monitor that ESCALATED (3 failed reads of one snapshot)
# stopped the relay app itself (snap_monitor.py READ_FAIL_CAP). Without snap_monitor.py only the owner's snapmon waiver lets seg3 run unwatched.
if [ -f $E/snap_monitor.py ]; then
  nohup $PY $E/snap_monitor.py watch --profile $P --name q35_4b_c_r1 > $E/logs/snap_monitor.log 2>&1 &
  SMPID=$!
  sleep "$MON_START_S"
  if ! mon_ok || ! grep -q '"ev": "start"' $E/logs/snap_monitor.log; then
    mon_dead "45 s after start"
    stop "snap monitor not running after 45 s (see $E/logs/snap_monitor.log): recipe 5 stop rule unwatched; seg3 NOT launched"
  fi
  echo "snap monitor pid $SMPID (alive)"
elif ! grep -qE '^[> *-]*OWNER-WAIVER r1-preflight snapmon:' PREREG_FINAL.md; then
  stop "no snap_monitor.py and no owner snapmon waiver: seg3 NOT launched"
fi
K=0
while :; do                     # A28: post-300 segments seg3, seg4, ... until `final`
  K=$((K + 1)); SN=seg$((K + 2))
  [ "$K" -le "$MAXSEG" ] || stop "more than $MAXSEG post-300 segments without final: owner decides"
  MIN=$(cat $E/logs/r1_stop_after_min.txt 2>/dev/null)
  rm -f $E/logs/r1_stop_after_min.txt  # one cap per segment: the next one comes only from a GO `r1_check.py seg`
  [[ "$MIN" =~ ^[0-9]+$ ]] && [ "$MIN" -gt 0 ] && [ "$MIN" -le 540 ] || stop "bad stop_after_min '$MIN' before $SN"
  [ -f $STOPF ] && stop "recipe 5 stop rule fired ($STOPF) before $SN: NO candidate this round; owner reviews"
  [ -f $ESCF ] && stop "snap monitor ESCALATED ($ESCF) before $SN: NO candidate until the owner decides"
  if [ "$K" = 1 ]; then led "D5 seg3 to the end: BEFORE (cap $MIN min)"; else
    led "D5 $SN (A28 relay segment $K, resumes at its checkpoint): BEFORE (cap $MIN min)"; fi
  echo "== D5 $SN cap $MIN min $(date -u)"
  mon_gate $SN                  # re-checked right before launch (it can die after the start check)
  seg $SN --expect-resume --stop-after-min "$MIN" & SEGPID=$!
  while kill -0 "$SEGPID" 2>/dev/null; do   # re-check the monitor every 60 s while the segment trains
    sleep "$MON_POLL_S"
    mon_ok || [ "$SMRC" = 3 ] || [ "$SMRC" = 4 ] || mon_dead "during $SN"   # 3/4: it stopped the app itself
  done
  wait "$SEGPID"; rc=$?
  [ -f $STOPF ] && stop "recipe 5 stop rule fired ($STOPF; relay stopped by snap_monitor): NO candidate this round; owner reviews"
  [ -f $ESCF ] && stop "snap monitor ESCALATED ($ESCF: a snapshot failed 3 reads; relay stopped): NO candidate until the owner decides"
  [ -f $DEADF ] && stop "snap monitor died during $SN ($DEADF): stop rule unwatched; no new segment; no candidate until the owner decides"
  [ $rc = 0 ] || stop "$SN client exit $rc (the app may still run to its cap: $M app list; D5 'if the local client dies')"
  led "D5 $SN: AFTER"
  [ -f logs/relay_q35_4b_c_r1_final.json ] && break
  echo "== D5 $SN stopped at its cap without final: next segment from the budget left $(date -u)"
  $PY $E/r1_check.py seg || stop "seg STOP after $SN (projection > \$55 (A28), the rest no longer fits the cap, no progress, or spend unknown): checkpoint kept; owner decides"
done
if [ -n "$SMPID" ]; then
  echo "== waiting for the snap monitor to read every snapshot $(date -u)"
  mon_reap; [ -n "$SMRC" ] || { wait "$SMPID"; SMRC=$?; }
  [ -f $STOPF ] && stop "recipe 5 stop rule fired on a late read ($STOPF): NO candidate this round; owner reviews"
  [ -f $ESCF ] && stop "snap monitor ESCALATED on a late read ($ESCF): NO candidate until the owner decides"
  [ "$SMRC" = 0 ] || stop "snap monitor ended rc=$SMRC without reading every snapshot (logs/snap_monitor.jsonl): stop rule unchecked; no candidate until the owner decides"
fi
if [ -f logs/relay_q35_4b_c_r1_final.json ]; then echo "ROUND 1 FINAL: go to RUNBOOK D6"; else
  stop "D5 ended without final (hit the \$55 time cap, or crashed): owner decides; no relaunch without a new cap"; fi
