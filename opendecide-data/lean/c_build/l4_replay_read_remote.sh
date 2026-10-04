#!/usr/bin/env bash
# C round-1 replay read: C1 (q35_4b_main500k) A5 read of the round-1 replay shards + the old slice, ON the L4 VM.
# Copied to the VM at the same path (~/lean/c_build/l4_replay_read_remote.sh) by c_build/L4_REPLAY_READ.sh (push) and started there under nohup
# (launch). Never run on the Mac.
#
# Readout = the shipped A5 readout (RUNBOOK_replay_reads.md 1): choice rows given order + exact reversal, averaged;
# yes/no rows one read; T = 1; merged adapter; bf16; no --perm-seed  ->  od_gcp.py label --tta-choice (no --tta-noul).
#
# Resumable per shard: od_gcp.py label writes each shard's labels atomically with its meta LAST, and on (re)start it
# skips every shard whose labels are complete (same ids, same row count, same shard sha256) and refuses a shard
# labelled with other settings. This driver retries the whole set up to 3 times in one launch; a later launch (after
# a stop or preemption) resumes the same way. One job at a time on the VM: it exits if another label job runs.
set -u
cd "$HOME/lean" || exit 2
PY="$HOME/od/bin/python"
NAME=q35_4b_main500k
REV=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
DIRS="data/c_replay_r1_shards data/c_old_slice_shards"
ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }

if pgrep -f "od_gcp.py label" >/dev/null; then
  echo "$(ts) BUSY: another od_gcp.py label job is running; not starting"
  exit 3
fi
export HF_HUB_OFFLINE=1

not_done() {  # prints the number of shards (both dirs) whose labels are not complete
  "$PY" - <<'EOF'
import sys
sys.path.insert(0, ".")
import shard_golden as sg
from pathlib import Path
bad = 0
for d in ("data/c_replay_r1_shards", "data/c_old_slice_shards"):
    out = Path(d) / "labels_q35_4b_main500k"
    for s in sg.shard_files(d):
        if not sg.shard_done(s, *sg.label_paths(out, s)):
            bad += 1
print(bad)
EOF
}

echo "$(ts) start: host $(hostname); code sha256:"
sha256sum od_gcp.py decoder_io.py shard_golden.py models/$NAME/adapter_model.safetensors
for attempt in 1 2 3; do
  for D in $DIRS; do
    echo "$(ts) attempt $attempt: label $D"
    "$PY" od_gcp.py label --name "$NAME" --base Qwen/Qwen3.5-4B --revision "$REV" \
      --layout schema_branch_mark --shards-dir "$D" --tta-choice
    rc=$?
    echo "$(ts) attempt $attempt: label $D exited $rc"
  done
  left=$(not_done)
  echo "$(ts) attempt $attempt: shards not done: $left"
  if [ "$left" = "0" ]; then
    echo "$(ts) DONE: every round-1 and old-slice shard is labelled"
    exit 0
  fi
done
echo "$(ts) STOPPED with shards not done after 3 attempts; launch again to resume"
exit 1
