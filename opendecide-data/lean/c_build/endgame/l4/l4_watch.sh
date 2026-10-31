#!/bin/bash
# Mac-side watcher for the free L4 job on od-l4b (us-east4-c): P2-L4 C1 pre-reads (RUNBOOK P2) + FAM-1 step 0 (B8).
# Polls every 5 min (max 10 h). When P2 ends: fetch the pre-reads (dev -> c_build/preread/preread_c1/, sealed ->
# c_build/preread/sealed_preread_c1/, never printed), check every file's sha256 against the VM, write
# PREREAD_MANIFEST.json (RUNBOOK P2 snippet) and logs/p2_l4_record.json. When FAM-1 ends: fetch its record to
# c_build/endgame/logs/fam1_step0_c1.json. Then stop the VM (after a FAM-1 failure it waits 90 min for a re-run).
#   cd lean && nohup bash c_build/endgame/l4/l4_watch.sh > c_build/endgame/logs/l4_watch.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 2          # lean/
VM=od-l4b; Z=us-east4-c; P=system-one-509903
PY=../.venv/bin/python; E=c_build/endgame; PR=c_build/preread
ssh_() { gcloud compute ssh $VM --zone $Z --project $P --command "$1" 2>/dev/null; }
scp_() { gcloud compute scp --zone $Z --project $P --quiet "$@" 2>&1 | grep -v "^$" | tail -2; }
log() { echo "$(date -u +%FT%TZ) $*"; }
p2_done=0; f_done=0; f_fail_at=0
for it in $(seq 1 120); do
  st=$(ssh_ 'cd ~/lean && (grep "^P2 status" logs/p2_l4/queue.log || echo P2-RUNNING); (cat c_build/endgame/fam1/FAM1.end 2>/dev/null || echo FAM1-PENDING)')
  [ -z "$st" ] && { log "ssh failed (VM down?)"; sleep 300; continue; }
  if [ $p2_done = 0 ] && echo "$st" | grep -q "^P2 status"; then
    log "P2 ended: $(echo "$st" | grep '^P2 status')"
    ssh_ 'cd ~/lean && ls preds_*/q35_4b_main500k_pre* | grep -v "^preds_nd_suite_v2/" > /tmp/p2_dev.list && tar cf /tmp/p2_dev.tar -T /tmp/p2_dev.list && sha256sum $(cat /tmp/p2_dev.list) > /tmp/p2_dev.sha256 && sha256sum preds_nd_suite_v2/q35_4b_main500k_pre.jsonl preds_nd_suite_v2/q35_4b_main500k_pre.meta.json > /tmp/p2_nd.sha256; wc -l < /tmp/p2_dev.list'
    mkdir -p $PR/preread_c1 $PR/sealed_preread_c1/preds_nd_suite_v2 $E/logs/p2_l4
    scp_ $VM:/tmp/p2_dev.tar $VM:/tmp/p2_dev.sha256 $VM:/tmp/p2_nd.sha256 $E/logs/p2_l4/
    tar xf $E/logs/p2_l4/p2_dev.tar -C $PR/preread_c1/ && rm $E/logs/p2_l4/p2_dev.tar
    scp_ "$VM:~/lean/preds_nd_suite_v2/q35_4b_main500k_pre.jsonl" "$VM:~/lean/preds_nd_suite_v2/q35_4b_main500k_pre.meta.json" $PR/sealed_preread_c1/preds_nd_suite_v2/
    scp_ "$VM:~/lean/logs/p2_l4/runs.jsonl" "$VM:~/lean/logs/p2_l4/queue.log" "$VM:~/lean/logs/p2_l4/pre.log" "$VM:~/lean/logs/p2_l4/pre_perm.log" "$VM:~/lean/logs/p2_l4/pre_served.log" $E/logs/p2_l4/
    devok=$( (cd $PR/preread_c1 && shasum -a 256 -c --status ../../../$E/logs/p2_l4/p2_dev.sha256) && echo 1 || echo 0)
    ndok=$( (cd $PR/sealed_preread_c1 && shasum -a 256 -c --status ../../../$E/logs/p2_l4/p2_nd.sha256) && echo 1 || echo 0)
    log "fetched: dev files $(wc -l < $E/logs/p2_l4/p2_dev.sha256) sha_ok=$devok; sealed sha_ok=$ndok"
    $PY - "$devok" "$ndok" <<'EOF'
import hashlib, json, pathlib, sys, time
r = pathlib.Path('c_build/preread')
fs = sorted(p for p in r.rglob('*') if p.is_file() and p.name != 'PREREAD_MANIFEST.json')
m = {str(p.relative_to(r)): hashlib.sha256(p.read_bytes()).hexdigest() for p in fs}
json.dump({"rule": "PREREG A21 (d): sealed until the gate; sha256 only; no score computed", "files": m,
           "complete": any('sealed_preread_c1' in k for k in m) and sum(k.endswith('.meta.json') for k in m) >= 21},
          open(r / 'PREREAD_MANIFEST.json', 'w'), indent=1)
runs = [json.loads(l) for l in open('c_build/endgame/logs/p2_l4/runs.jsonl') if l.strip()]
rec = {"what": "P2-L4 C1 pre-reads (RUNBOOK P2; PREREG A21 d), od_gcp.py predict on the Google L4; sealed, sha256 only",
       "vm": "od-l4b", "zone": "us-east4-c", "project": "system-one-509903", "adapter": "q35_4b_main500k",
       "adapter_sha256": "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078",
       "base": "Qwen/Qwen3.5-4B", "revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "layout": "schema_branch_mark",
       "tags": {"pre": "_pre (9 splits + eval_jagged + eval_opi)", "pre_perm": "_pre_perm (--perm-seed 1, 9 splits)",
                "pre_served": "_pre_served (--tta-choice, 9 splits)", "nd_pre": "nd_suite_v2 _pre (--tta-choice; sealed)"},
       "runs": [{k: v for k, v in x.items()} | {"min": round((x["end"] - x["start"]) / 60, 1)} for x in runs],
       "fetch_sha_ok": {"dev": sys.argv[1] == "1", "sealed": sys.argv[2] == "1"},
       "files": len(m), "metas": sum(k.endswith('.meta.json') for k in m),
       "manifest_sha256": hashlib.sha256((r / 'PREREAD_MANIFEST.json').read_bytes()).hexdigest(),
       "complete": json.load(open(r / 'PREREAD_MANIFEST.json'))["complete"] and sys.argv[1] == "1" and sys.argv[2] == "1",
       "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
pathlib.Path('c_build/endgame/logs/p2_l4_record.json').write_text(json.dumps(rec, indent=1))
print("manifest", len(m), "files; metas", rec["metas"], "complete", rec["complete"])
EOF
    p2_done=1
  fi
  if [ $f_done = 0 ] && echo "$st" | grep -q "^FAM1 DONE"; then
    mkdir -p $E/fam1/out
    scp_ "$VM:~/lean/c_build/endgame/fam1/out/fam1_step0_c1.json" "$VM:~/lean/c_build/endgame/fam1/out/fam1_smoke.json" "$VM:~/lean/c_build/endgame/fam1/fam1.log" "$VM:~/lean/c_build/endgame/fam1/fam1_smoke.log" $E/fam1/out/
    cp $E/fam1/out/fam1_step0_c1.json $E/logs/fam1_step0_c1.json
    log "FAM-1 fetched: $($PY -c "import json;d=json.load(open('$E/logs/fam1_step0_c1.json'));print({k:d.get(k) for k in ('wall_min','controls_pass')}, 'flags', len(d.get('flags') or []))")"
    f_done=1
  elif [ $f_done = 0 ] && echo "$st" | grep -qE "FAILED"; then
    if [ $f_fail_at = 0 ]; then
      f_fail_at=$it; log "FAM-1 failed: $(echo "$st" | grep FAILED)"
      mkdir -p $E/fam1/out
      scp_ "$VM:~/lean/c_build/endgame/fam1/fam1_smoke.log" "$VM:~/lean/c_build/endgame/fam1/fam1.log" $E/fam1/out/
    fi
    if [ $((it - f_fail_at)) -ge 18 ]; then f_done=2; log "no FAM-1 re-run within 90 min"; fi
  elif echo "$st" | grep -q "^FAM1 DONE"; then :; else f_fail_at=0; fi
  if [ $p2_done = 1 ] && [ $f_done != 0 ]; then
    gcloud compute instances stop $VM --zone $Z --project $P 2>&1 | tail -1
    log "VM STOPPED; WATCH END p2_done=$p2_done fam1=$f_done"; exit 0
  fi
  sleep 300
done
log "WATCH TIMEOUT (10 h); VM left as is"
