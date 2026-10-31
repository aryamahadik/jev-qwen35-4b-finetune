#!/usr/bin/env bash
# gcp_run.sh <vm> <command...>   sync code to a GCP VM, run a CPU job there, pull back what it wrote.
#
#   zed_orch/gcp_run.sh od-l4b ".venv_py zed_orch/g6_at_size.py T30 --n 6000 --dir pilot_vm"
#
# <vm> is od-l4 (us-central1-a), od-l4b (us-east4-c) or od-cpu1 (us-east4-c, c3-standard-8, NO GPU: the extra CPU box, made
# 16 Oct from a snapshot of od-l4b; set ZONE=us-east4-a|b if it had to be re-created there). The command runs on the VM inside
# ~/repo/opendecide-data/lean/c2_build (same layout as the Mac), with $PY set to "~/cpu/bin/python -B"
# (use $PY in the command; quote the whole command so your Mac shell does not expand it).
#
# Environment switches:
#   BG=1          run detached (setsid nohup) and return at once; job log ~/jobs/<JOB>.log, exit code ~/jobs/<JOB>.rc
#   JOB=name      job name (default: job-<unix time>); BG status / pull use it
#   ACTION=sync   only sync code (no job)
#   ACTION=status print the tail of ~/jobs/<JOB>.log and its exit code (BG jobs)
#   ACTION=pull   pull the files the job (or the last foreground run) wrote, without running anything
#   ACTION=stop   stop the VM (do it when nothing runs there; a stopped VM costs only its disk)
#   ZONE=...      od-cpu1 only: override the zone (default us-east4-c; set it if the VM was moved)
#   START_TRIES=n od-cpu1 only: start attempts when the C3 pool is exhausted (default 6, 20 s apart)
#   NOSYNC=1      skip the code sync (the tree on the VM is already current)
#   EXTRA_SYNC="families/T30/pools gblock/route_a42d"   more c2_build sub-folders to sync (default set below)
#   STOP_AFTER=1  stop the VM after the (foreground) pull
#
# What is synced (c2_build code + families, lean/c_build, lean/teach1, lean/c_src/common, PREREG_FINAL.md) and what is
# NEVER synced: any name containing ohs/OHS (any case) or jev, sealed_nd, sealed_brief, preread, external_quarantine,
# longbench_v2, decision_index, sealed_hashes*, .git, .venv, __pycache__, and the c2_build folders gblock, replay_screen,
# pilot_runs, t37b, transfer (big, not needed for G6; add one through EXTRA_SYNC if a job needs it). After every sync the
# script checks the VM tree: `find ~/repo -ipath '*ohs*'` must print nothing, else it aborts.
# The G13 decontamination (g13_c2.py) needs the sealed targets and cannot run on a VM; do not try.
set -euo pipefail
VM="${1:?usage: gcp_run.sh <od-l4|od-l4b|od-cpu1> <command...>}"; shift || true
CMD="$*"
P=system-one-509903
GPU=1   # od-l4 / od-l4b hold the project's one L4; od-cpu1 has none (its start needs no GPU quota, only CPU quota)
case "$VM" in od-l4) Z=us-central1-a;; od-l4b) Z=us-east4-c;; od-cpu1) Z="${ZONE:-us-east4-c}"; GPU=0;; *) echo "unknown vm $VM"; exit 2;; esac
LEAN="$(cd "$(dirname "$0")/../.." && pwd)"          # .../opendecide-data/lean
ACTION="${ACTION:-run}"; JOB="${JOB:-job-$(date +%s)}"
RLEAN='~/repo/opendecide-data/lean'; RC2="$RLEAN/c2_build"

EX=(--exclude='*[Oo][Hh][Ss]*' --exclude='*[Jj][Ee][Vv]*' --exclude='sealed_nd' --exclude='sealed_brief' --exclude='preread'
    --exclude='external_quarantine' --exclude='longbench_v2' --exclude='decision_index' --exclude='sealed_hashes*'
    --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' --exclude='.venv' --exclude='.claude' --exclude='claude-501')
C2_SKIP=(--exclude='/gblock' --exclude='/replay_screen' --exclude='/pilot_runs' --exclude='/t37b' --exclude='/transfer')

if [ "$ACTION" = stop ]; then gcloud compute instances stop "$VM" --zone "$Z" --project "$P"; exit 0; fi

# 1. VM up (the project has ONE GPU quota across the GPU VMs: only one of od-l4 / od-l4b can run at a time; od-cpu1 has no GPU)
ST=$(gcloud compute instances describe "$VM" --zone "$Z" --project "$P" --format='value(status)')
if [ "$ST" != RUNNING ]; then
  echo "starting $VM ..."
  if [ "$GPU" = 1 ]; then
    gcloud compute instances start "$VM" --zone "$Z" --project "$P" \
      || { echo "START FAILED (L4 stockout in $Z, or the other VM is running: GPUS_ALL_REGIONS quota is 1). Retry later."; exit 3; }
  else  # CPU-only VM: no GPU quota involved; a failure here is a C3 stockout in the zone (seen 16 Oct right after a stop)
        # or CPUS_ALL_REGIONS (16: od-l4b 8 + od-cpu1 8). Retry START_TRIES times, 20 s apart (default 6).
    ok=; for t in $(seq 1 "${START_TRIES:-6}"); do
      gcloud compute instances start "$VM" --zone "$Z" --project "$P" && { ok=1; break; }
      echo "start try $t failed (c3 stockout in $Z?); retrying in 20 s"; sleep 20
    done
    [ -n "$ok" ] || { echo "START FAILED (c3 stockout in $Z, or CPUS_ALL_REGIONS quota 16 exceeded). Retry later with START_TRIES=30, or move the VM (GCP_RUNBOOK.md, od-cpu1 section)."; exit 3; }
  fi
fi
# 2. ssh command line (rsync -e uses the same key and options)
for i in $(seq 1 30); do
  DRY=$(gcloud compute ssh "$VM" --zone "$Z" --project "$P" --tunnel-through-iap --dry-run 2>/dev/null) && TARGET=${DRY##* } && \
    gcloud compute ssh "$VM" --zone "$Z" --project "$P" --tunnel-through-iap --quiet --command 'true' >/dev/null 2>&1 && break
  echo "waiting for ssh ($i) ..."; sleep 10
done
SSHOPTS=$(echo "$DRY" | sed -E 's#^[^ ]*/ssh ##; s#^-t ##; s# -t ##; s# [^ ]+$##')
# rsync -e needs ONE command: write a tiny wrapper (the dry-run options hold a quoted ProxyCommand for the IAP tunnel)
mkdir -p "$HOME/.cache/gcp_run"; RSH="$HOME/.cache/gcp_run/rsh_$VM.sh"
printf '#!/bin/bash\nexec ssh %s "$@"\n' "$SSHOPTS" > "$RSH"; chmod +x "$RSH"
rssh() { gcloud compute ssh "$VM" --zone "$Z" --project "$P" --tunnel-through-iap --quiet --command "$1"; }

sync_code() {
  rssh "mkdir -p $RLEAN/c2_build $RLEAN/c_build $RLEAN/teach1 $RLEAN/c_src/common ~/jobs"
  rsync -az "${EX[@]}" "${C2_SKIP[@]}" -e "$RSH" "$LEAN/c2_build/" "$TARGET:$RC2/"
  for x in ${EXTRA_SYNC:-}; do
    rssh "mkdir -p $RC2/$(dirname "$x")"
    rsync -az "${EX[@]}" -e "$RSH" "$LEAN/c2_build/$x" "$TARGET:$RC2/$(dirname "$x")/"
  done
  rsync -az "${EX[@]}" -e "$RSH" "$LEAN/c_build/" "$TARGET:$RLEAN/c_build/"
  rsync -az "${EX[@]}" -e "$RSH" "$LEAN/teach1/" "$TARGET:$RLEAN/teach1/"
  rsync -az "${EX[@]}" -e "$RSH" "$LEAN/c_src/common/" "$TARGET:$RLEAN/c_src/common/"
  rsync -az -e "$RSH" "$LEAN/PREREG_FINAL.md" "$TARGET:$RLEAN/PREREG_FINAL.md"
  n=$(rssh "find ~/repo -ipath '*ohs*' 2>/dev/null | wc -l" | tr -d '[:space:]')
  [ "$n" = 0 ] || { echo "ABORT: $n paths containing 'ohs' on the VM tree (must be 0)"; exit 4; }
  echo "synced; VM tree has 0 'ohs' paths."
}

pull() {  # files under c2_build newer than the job's start marker, plus the job log
  rssh "cd $RC2 && find . -newer ~/jobs/$JOB.start -type f ! -path '*/__pycache__/*' | sed 's#^\./##' > ~/jobs/$JOB.files; wc -l < ~/jobs/$JOB.files"
  rsync -az --update -e "$RSH" --files-from=<(rssh "cat ~/jobs/$JOB.files") "$TARGET:$RC2/" "$LEAN/c2_build/"
  rsync -az -e "$RSH" "$TARGET:~/jobs/$JOB.log" "$LEAN/c2_build/zed_orch/logs/gcp_$JOB.log" 2>/dev/null || true
  echo "pulled the files listed in ~/jobs/$JOB.files (log: zed_orch/logs/gcp_$JOB.log)"
}

case "$ACTION" in
  sync)   sync_code; exit 0;;
  status) rssh "tail -n 25 ~/jobs/$JOB.log; echo -n 'rc: '; cat ~/jobs/$JOB.rc 2>/dev/null || echo running-or-none"; exit 0;;
  pull)   pull; exit 0;;
esac

[ -n "$CMD" ] || { echo "no command given"; exit 2; }
[ -z "${NOSYNC:-}" ] && sync_code
# the job as a script on the VM (no nested quoting): runs inside c2_build with $PY = the CPU venv's python
printf '#!/bin/bash\ncd %s\nexport PY="$HOME/cpu/bin/python -B" PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=${OMP_NUM_THREADS:-1}\n%s\n' "$RC2" "$CMD" \
  | rssh "cat > ~/jobs/$JOB.sh; touch ~/jobs/$JOB.start; sleep 1"
if [ -n "${BG:-}" ]; then
  rssh "(setsid nohup bash -c 'bash ~/jobs/$JOB.sh; echo \$? > ~/jobs/$JOB.rc' > ~/jobs/$JOB.log 2>&1 < /dev/null &); echo started job $JOB"
  echo "detached. Check: ACTION=status JOB=$JOB $0 $VM ; fetch: ACTION=pull JOB=$JOB $0 $VM ; stop: ACTION=stop $0 $VM"
else
  t0=$(date +%s)
  rssh "bash ~/jobs/$JOB.sh 2>&1 | tee ~/jobs/$JOB.log; exit \${PIPESTATUS[0]}" || echo "job exited non-zero"
  echo "wall seconds (ssh run only): $(( $(date +%s) - t0 ))"
  pull
  [ -z "${STOP_AFTER:-}" ] || gcloud compute instances stop "$VM" --zone "$Z" --project "$P"
fi
