#!/bin/bash
# finish_replay.sh: after the VM label driver is done: pull data/c2_replay_shards/labels_q35_4b_main500k, check every shard
# (shard_golden.shard_done: ids, row count, shard sha256), then run the second pass (c2_build/replay_c2_pg_anchor.json).
# Run from anywhere:  bash c2_build/reads/finish_replay.sh        (it does NOT stop the VM: do that after, if nothing else needs it)
set -euo pipefail
P=system-one-509903; Z=us-east4-c; V=od-l4b
LEAN=/Users/aryamahadik/Documents/jev/opendecide-data/lean
PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python
A="--tunnel-through-iap --zone $Z --project $P"
gcloud compute ssh $V $A --command 'tail -n 2 ~/jobs/label_driver.log | cut -c1-200; ls ~/lean/data/c2_replay_shards/labels_q35_4b_main500k/*.meta.json | wc -l' 2>&1 | grep -v -i "numpy\|increasing_the\|^$\|WARNING"
read -p "driver shows DRIVER_DONE and 17 metas? [y/N] " ok; [ "$ok" = y ] || exit 1
gcloud compute ssh $V $A --command 'cd ~/lean/data/c2_replay_shards && tar czf ~/jobs/c2_labels.tgz labels_q35_4b_main500k && sha256sum ~/jobs/c2_labels.tgz' 2>&1 | grep -v -i "numpy\|increasing_the\|^$\|WARNING"
gcloud compute scp $A $V:~/jobs/c2_labels.tgz /tmp/c2_labels.tgz 2>&1 | grep -v -i "numpy\|increasing_the\|^$\|WARNING" || true
shasum -a 256 /tmp/c2_labels.tgz
tar xzf /tmp/c2_labels.tgz -C $LEAN/data/c2_replay_shards
cd $LEAN && $PY -B - <<'PYEOF'
import sys, json
sys.path.insert(0, '.')
import shard_golden as sg
d = 'data/c2_replay_shards'
p, view = sg.load_labels(d + '/labels_q35_4b_main500k', d, return_view=True)   # raises unless every shard is done
n = sum(1 for s in sg.shard_files(d) for _ in sg.read_jsonl(s))
print('labels', len(p), 'rows in shards', n, 'settings', view['settings'])
assert len(p) == n
PYEOF
cd $LEAN/c2_build/reads && nice -n 10 $PY -B replay_c2.py second-pass
