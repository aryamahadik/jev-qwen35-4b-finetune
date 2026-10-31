#!/bin/bash
# Item 4 pilot reads on the free Google L4 VM od-l4 (A42-D 4.4; same machinery as gate/gate_4b_fix2_l4.sh, much smaller).
# NOTHING here runs by itself: every step is a subcommand. The VM is billed by Google credit (free for the orchestrator's
# purposes); `plan` prints every command and runs nothing.
#
#   plan FAM                 print the whole sequence for one family
#   start | stop             gcloud compute instances start/stop od-l4
#   fetch FAM                pilot adapter from the Modal volume (profile $PILOT_PROFILE) -> ONE local copy under backups/
#   push FAM OWN GPROXY REL  scp: pilot adapter (+ C1 if missing), own dev, G-proxy rows and relations -> ~/lean on the VM
#   read-c1 [FAM...]         C1 read (A18.2 readout, --tta-choice): 9 gate dev splits + G-proxy + the own dev of each FAM
#   read FAM                 pilot read of the same splits (own dev of FAM, G-proxy, the 9 dev splits); writes adapters.sha256
#   pull FAM                 preds + metas + adapters.sha256 -> pilot_ab/reads/FAM/ (what verdict.py reads)
# Order per family: fetch, start, push, (read-c1 once), read, pull, stop, then verdict.py. C1 is read ONCE for all families
# (its reads are family-independent except the own dev split); rerun read-c1 with the new FAM when a new own dev exists.
# Expected L4 time (single-pass logs/gate4b: the 9 splits took 25 min; choice rows double): model load ~3 min, the 9 splits
# ~40 min, G-proxy (~2,300 rows) ~10 min, own dev (300) ~2 min => about 55 min per adapter; C1 once about 55 min + 2 min per own dev.
set -uo pipefail
P=${GCP_PROJECT:-system-one-509903}; Z=${GCP_ZONE:-us-central1-a}; VM=${GCP_VM:-od-l4}
HERE=$(cd "$(dirname "$0")" && pwd); LEAN=$(cd "$HERE/../.." && pwd)
PY=${PY:-$LEAN/../.venv/bin/python}
C1=q35_4b_main500k; BASE=Qwen/Qwen3.5-4B; REV=851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a; LAYOUT=schema_branch_mark
TAG=_pab; PROFILE=${PILOT_PROFILE:-mahadikarya2}
SPLITS9=dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev
BK=${BACKUPS:-/Users/aryamahadik/Documents/jev/backups/modal_models}
FILES="adapter_config.json adapter_model.safetensors train_meta.json chat_template.jinja tokenizer.json tokenizer_config.json"
gssh() { gcloud compute ssh "$VM" --zone "$Z" --project "$P" --command "$1"; }
gscp() { gcloud compute scp --zone "$Z" --project "$P" --quiet "$@"; }
chk_path() { case "$(echo "$1" | tr 'A-Z' 'a-z')" in *ohs*|*sealed_nd*|*preread*|*quarantine*|*longbench_v2*) echo "REFUSED path $1"; exit 2;; esac; }
pred() { # NAME SPLITS
  echo "cd ~/lean && ~/od/bin/python od_gcp.py predict --name $1 --base $BASE --revision $REV --layout $LAYOUT --splits $2 --tta-choice --tag $TAG"
}
cmd=${1:-plan}; fam=${2:-}
case "$cmd" in
  plan)
    [ -n "$fam" ] || { echo "usage: l4_reads.sh plan FAM"; exit 1; }
    N=q35_4b_pab_$fam
    echo "1. modal train (pilot_ab/modal_pilot.py; see README)         -> /vol/models/$N on profile $PROFILE"
    echo "2. $0 fetch $fam"; echo "3. $0 start"
    echo "4. $0 push $fam <own_dev.jsonl> <gproxy.jsonl> <gproxy_rel.jsonl>"
    echo "5. $0 read-c1 $fam       (once for all families; add each new own dev)"
    echo "6. $0 read $fam"; echo "7. $0 pull $fam"; echo "8. $0 stop"
    echo "9. $PY -B pilot_ab/verdict.py --family $fam --reads-dir pilot_ab/reads/$fam --own-rows <own> --gproxy-rows <gp> --gproxy-rel <rel> [--gproxy-sha256 H]"
    echo "--- the VM commands:"; pred $C1 "pab_own_$fam,pab_gproxy,$SPLITS9"; pred $N "pab_own_$fam,pab_gproxy,$SPLITS9" ;;
  start) gcloud compute instances start "$VM" --zone "$Z" --project "$P" ;;
  stop)  gcloud compute instances stop "$VM" --zone "$Z" --project "$P" ;;
  fetch)
    N=q35_4b_pab_$fam; D=$BK/$N; mkdir -p "$D"
    for f in $FILES; do
      [ -f "$D/$f" ] || MODAL_PROFILE=$PROFILE "$LEAN/../.venv/bin/modal" volume get opendecide "models/$N/$f" "$D/$f" || echo "(no $f)"
    done
    sha256sum "$D/adapter_model.safetensors" 2>/dev/null || shasum -a 256 "$D/adapter_model.safetensors"
    "$PY" -B -c "import json,sys;m=json.load(open('$D/train_meta.json'));print({k:m.get(k) for k in ('steps','n_steps','seed','epochs')})" ;;
  push)
    N=q35_4b_pab_$fam; own=${3:?own dev}; gp=${4:?gproxy}; rel=${5:?gproxy rel}
    for p in "$own" "$gp" "$rel"; do chk_path "$p"; done
    gscp "$own" "$VM:~/lean/data/pab_own_$fam.jsonl"; gscp "$gp" "$VM:~/lean/data/pab_gproxy.jsonl"
    gscp "$rel" "$VM:~/lean/data/pab_gproxy_relations.jsonl"
    gssh "mkdir -p ~/lean/models/$N"
    for f in $FILES; do gscp "$BK/$N/$f" "$VM:~/lean/models/$N/$f"; done
    gssh "test -f ~/lean/models/$C1/adapter_model.safetensors && sha256sum ~/lean/models/$C1/adapter_model.safetensors | cut -c1-16"
    echo "(C1 on the VM must start 507d1c29)" ;;
  read-c1)
    shift; S="pab_gproxy,$SPLITS9"; for f in "$@"; do S="pab_own_$f,$S"; done
    gssh "cd ~/lean && sha256sum models/$C1/adapter_model.safetensors > ~/lean/pab_c1.sha256 && $(pred $C1 "$S" | cut -d'&' -f3-)" ;;
  read)
    N=q35_4b_pab_$fam
    gssh "cd ~/lean && (sha256sum models/$C1/adapter_model.safetensors models/$N/adapter_model.safetensors) > pab_adapters_$fam.sha256 && $(pred $N "pab_own_$fam,pab_gproxy,$SPLITS9" | cut -d'&' -f3-)" ;;
  pull)
    N=q35_4b_pab_$fam; R=$HERE/reads/$fam; mkdir -p "$R"
    for s in pab_own_$fam pab_gproxy ${SPLITS9//,/ }; do
      mkdir -p "$R/preds_$s"
      for n in $C1 $N; do for x in jsonl meta.json; do gscp "$VM:~/lean/preds_$s/$n$TAG.$x" "$R/preds_$s/$n$TAG.$x"; done; done
    done
    gscp "$VM:~/lean/pab_adapters_$fam.sha256" "$R/adapters.sha256"
    echo "pulled to $R" ;;
  *) echo "usage: $0 plan|start|stop|fetch|push|read-c1|read|pull ..."; exit 1 ;;
esac
