#!/bin/bash
# FAM-1 step-0 RE-READ on C1 with negative control v2 (fam1_step0.py NEG_CONTROL; blocker B8). Free Google L4, $0 Modal.
# v1 (6 Oct 11:45 UTC) failed its controls: uniform random labels are not a null under C1 (cause written in
# fam1_step0.py before this run). v2 runs ONCE; it is not re-run to make the controls pass.
#   cd lean && nohup bash c_build/endgame/l4/fam1_rerun.sh > c_build/endgame/logs/fam1_rerun.log 2>&1 &
# VM: a RUNNING od-l4b / od-l4 is used as is (global GPU quota 1); else start od-l4b (us-east4-c), on STOCKOUT / quota
# od-l4 (us-central1-a); if both fail, retry every 20 min (max 8 h). Prepare: pinned base snapshot + ~/od python on the
# VM; push C1's adapter (sha 507d1c29...), the FAM-1 inputs and the code when their sha256 differs. Then the smoke and
# the read run detached on the VM; poll every 5 min; fetch the record to logs/fam1_step0_c1.json (v1 kept as
# logs/fam1_step0_c1.v1_randlabel.json); stop the VM (unless another od_gcp job runs on it). Restartable.
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 2          # lean/
P=system-one-509903; E=c_build/endgame; F=$E/fam1; PY=../.venv/bin/python
REV=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a; ASHA=507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078
ADIR=../../backups/modal_models/q35_4b_main500k
CODE="train_decoder.py decoder_io.py prism_x.py writeblock.py shard_golden.py od_gcp.py"
log() { echo "$(date -u +%FT%TZ) $*"; }
g() { gcloud "$@" --project $P 2>&1; }
st() { g compute instances describe "$1" --zone "$2" --format="value(status)" | tail -1; }
ssh_() { gcloud compute ssh $VM --zone $Z --project $P --quiet --command "$1" 2>/dev/null | tr -d "\r"; return ${PIPESTATUS[0]}; }
scp_() { gcloud compute scp --zone $Z --project $P --quiet "$@" 2>&1 | tail -2; }
LSHA=$(shasum -a 256 $F/fam1_step0.py | cut -d' ' -f1)
[ "$(shasum -a 256 $ADIR/adapter_model.safetensors | cut -d' ' -f1)" = "$ASHA" ] || { log "local C1 adapter sha256 mismatch"; exit 2; }
shasum -a 256 -c --quiet $F/fam1_inputs.sha256 || { log "local FAM-1 inputs sha256 mismatch"; exit 2; }
$PY $F/fam1_step0.py selftest > /dev/null || { log "CPU selftest FAILED"; exit 2; }

VM=; Z=; OURS=0; BAD=""
for try in $(seq 1 25); do
  for vz in od-l4b:us-east4-c od-l4:us-central1-a; do
    v=${vz%%:*}; z=${vz##*:}
    [ "$(st $v $z)" = RUNNING ] && { VM=$v; Z=$z; log "VM $v already RUNNING: used as is"; break 2; }
  done
  for vz in od-l4b:us-east4-c od-l4:us-central1-a; do
    v=${vz%%:*}; z=${vz##*:}
    case " $BAD " in *" $v "*) continue;; esac
    out=$(g compute instances start $v --zone $z)
    if [ "$(st $v $z)" = RUNNING ]; then VM=$v; Z=$z; OURS=1; log "VM $v started"; break 2; fi
    if echo "$out" | grep -qiE "STOCKOUT|RESOURCE_POOL_EXHAUSTED|enough resources|QUOTA|Quota"; then
      log "VM $v ($z): STOCKOUT/quota"; else log "VM $v start failed: $(echo "$out" | tail -1 | cut -c1-160)"; fi
  done
  log "no L4 (try $try): retry in 20 min"; sleep 1200
done
[ -n "$VM" ] || { log "GAVE UP: no L4 within ~8 h"; exit 1; }
stopvm() {
  if [ $OURS = 1 ] && ! ssh_ 'pgrep -f "[o]d_gcp.py" >/dev/null'; then
    g compute instances stop $VM --zone $Z | tail -1; log "VM $VM STOPPED"
  else log "VM $VM left running (not started here, or another od_gcp job runs)"; fi
}
for i in $(seq 1 12); do ssh_ "echo ok" | grep -q ok && break; sleep 20; done

# prepare: base snapshot + python, then push what differs (by sha256)
FILES="$(awk '{print $2}' $F/fam1_inputs.sha256) $CODE"
chk=$(ssh_ "mkdir -p ~/lean/$F/out ~/lean/models/q35_4b_main500k ~/lean/runs && cd ~/lean && \
  (ls -d ~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/$REV >/dev/null 2>&1 && echo BASE_OK) ; \
  (test -x ~/od/bin/python && echo PY_OK); sha256sum $FILES models/q35_4b_main500k/adapter_model.safetensors 2>/dev/null")
if ! echo "$chk" | grep -q BASE_OK || ! echo "$chk" | grep -q PY_OK; then
  log "VM $VM lacks the pinned base snapshot or ~/od python: not usable"; stopvm; exit 1
fi
push=""
for f in $FILES; do
  [ -f "$f" ] || continue
  echo "$chk" | grep -q "^$(shasum -a 256 "$f" | cut -d' ' -f1)  $f\$" || push="$push $f"
done
for f in $push; do scp_ "$f" "$VM:~/lean/$(dirname $f)/" > /dev/null; done
echo "$chk" | grep -q "^$ASHA  models/q35_4b_main500k/adapter_model.safetensors" || {
  push="$push adapter"
  scp_ $(find $ADIR -maxdepth 1 -type f) "$VM:~/lean/models/q35_4b_main500k/" > /dev/null; }
scp_ $F/fam1_inputs.sha256 "$VM:~/lean/$F/" > /dev/null
log "VM $VM prepared; pushed:${push:- nothing}"

# launch (once): archive v1 outputs on the VM, smoke, read; FAM1.end says V2
state=$(ssh_ "cd ~/lean/$F && (cat FAM1.end 2>/dev/null || echo NONE); pgrep -f '[f]am1_step0.py read' >/dev/null && echo RUNNING")
if echo "$state" | grep -q "V2 DONE"; then log "v2 already done on the VM"
elif echo "$state" | grep -q RUNNING; then log "a FAM-1 read is already running on the VM: polling it"
else
  ssh_ "cd ~/lean/$F && for x in out/fam1_step0_c1.json out/fam1_smoke.json fam1.log fam1_smoke.log; do \
    [ -f \$x ] && [ ! -f \${x%.*}.v1.\${x##*.} ] && mv \$x \${x%.*}.v1.\${x##*.}; done; rm -f FAM1.end out/fam1_step0_c1.json out/fam1_smoke.json; \
    cd ~/lean && setsid nohup bash -c 'export HF_HUB_OFFLINE=1; F=$F; PY=\$HOME/od/bin/python; \
      sha256sum -c --quiet \$F/fam1_inputs.sha256 || { echo \"V2 INPUTS sha256 FAILED\" > \$F/FAM1.end; exit 3; }; \
      while pgrep -f \"[o]d_gcp.py\" >/dev/null; do sleep 30; done; \
      \$PY \$F/fam1_step0.py read --smoke > \$F/fam1_smoke.log 2>&1 || { echo \"V2 SMOKE FAILED\" > \$F/FAM1.end; exit 4; }; \
      \$PY \$F/fam1_step0.py read > \$F/fam1.log 2>&1 || { echo \"V2 READ FAILED\" > \$F/FAM1.end; exit 5; }; \
      echo \"FAM1 V2 DONE \$(date -u +%FT%TZ)\" > \$F/FAM1.end' < /dev/null > /dev/null 2>&1 &
    echo launched"
  log "v2 smoke + read launched on $VM"
fi

# poll every 5 min (max ~3 h)
for it in $(seq 1 36); do
  s=$(ssh_ "cat ~/lean/$F/FAM1.end 2>/dev/null; tail -c 300 ~/lean/$F/fam1.log 2>/dev/null | tail -1")
  if echo "$s" | grep -q "V2 DONE"; then
    mkdir -p $F/out
    for x in fam1_step0_c1.json fam1_smoke.json fam1.log fam1_smoke.log; do
      [ -f $F/out/$x ] && [ ! -f $F/out/${x%.*}.v1.${x##*.} ] && mv $F/out/$x $F/out/${x%.*}.v1.${x##*.}; done
    scp_ "$VM:~/lean/$F/out/fam1_step0_c1.json" "$VM:~/lean/$F/out/fam1_smoke.json" "$VM:~/lean/$F/fam1.log" \
      "$VM:~/lean/$F/fam1_smoke.log" $F/out/ > /dev/null
    ok=$($PY -c "import json,sys;d=json.load(open('$F/out/fam1_step0_c1.json'));print(int(d['env']['code_sha256']['fam1_step0.py']=='$LSHA' and d.get('neg_control',{}).get('version')==2 and not d.get('smoke')))")
    if [ "$ok" = 1 ]; then
      [ -f $E/logs/fam1_step0_c1.v1_randlabel.json ] || cp $E/logs/fam1_step0_c1.json $E/logs/fam1_step0_c1.v1_randlabel.json
      cp $F/out/fam1_step0_c1.json $E/logs/fam1_step0_c1.json
      log "FAM-1 v2 fetched: $($PY -c "import json;d=json.load(open('$E/logs/fam1_step0_c1.json'));c=d['controls'];print('wall_min',d['wall_min'],'controls_pass',d['controls_pass'],'neg',round(c['neg_push']['push'],3),[round(x,3) for x in c['neg_push']['ci'] or []],'pos_ok',c['pos_ok'],'flags',len(d['flags']))")"
    else log "fetched record is not the v2 code's (sha / version): NOT installed"; fi
    stopvm; log "RERUN END"; exit 0
  fi
  if echo "$s" | grep -q "FAILED"; then
    scp_ "$VM:~/lean/$F/fam1.log" "$VM:~/lean/$F/fam1_smoke.log" $F/out/ > /dev/null
    log "FAM-1 v2 FAILED: $(echo "$s" | head -1)"; stopvm; exit 1
  fi
  [ $((it % 3)) = 1 ] && log "running: $(echo "$s" | tail -1 | cut -c1-120)"
  sleep 300
done
log "POLL TIMEOUT (3 h)"; stopvm; exit 1
