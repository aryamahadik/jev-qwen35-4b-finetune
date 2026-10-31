#!/usr/bin/env bash
# run_all_vm.sh: the T27 G11 fix round 2 full run on the free VM od-l4b (CPU only; the GPU is not touched).
# From lean/c2_build:
#   FINAL    (needs admitted_wordings.json): bash zed_orch/t27_fix_r2/run_all_vm.sh   > zed_orch/t27_fix_r2/logs/run_all_vm.log 2>&1 &
#   INTERIM  (frozen pools, throw-away bases 74M/75M, gen_root_interim, out_a50_interim): MODE=interim bash zed_orch/t27_fix_r2/run_all_vm.sh
# At most 3 CPU jobs of this task at a time: the generation (candidates + QC + mixdev + every gate + G5-H task files) and two A50
# builds (11M, 12M) start together; the 13M build starts when one of the three ends. Output roots are unique to this task;
# nothing is stopped, killed or written outside them.
set -uo pipefail
VM=od-l4b; H=zed_orch/t27_fix_r2; MODE=${MODE:-final}
ENVP=""
if [ "$MODE" = interim ]; then
  ENVP="T27_R2_NO_NEW_WORDINGS=1 T27_R2_ROOT_NAME=gen_root_interim T27_R2_BASES=74000000,75000000,68000000 T27_R2_OUT_A50=out_a50_interim"
else
  [ -f $H/admitted_wordings.json ] || { echo "admitted_wordings.json missing: admit the new wordings first (redo5.py glex-check --record)"; exit 2; }
fi
rc_of() { ACTION=status JOB=$1 zed_orch/gcp_run.sh $VM 2>/dev/null | sed -n 's/^rc: //p' | tail -1; }
done_job() { local r; r=$(rc_of $1); [ -n "$r" ] && [ "$r" != "running-or-none" ]; }
GEN="t27r2_${MODE}_gen"; B11="t27r2_${MODE}_b11"; B12="t27r2_${MODE}_b12"; B13="t27r2_${MODE}_b13"
cmd_b() { echo "$ENVP \$PY zed_orch/t27_fix_r2/g6_a50_r2.py build --seed-base $1"; }
BG=1 JOB=$GEN zed_orch/gcp_run.sh $VM "$ENVP HF_HUB_OFFLINE=1 PYTHONPATH=\$HOME/lean ~/od/bin/python -B zed_orch/t27_fix_r2/gen_t27_r2.py"
BG=1 NOSYNC=1 JOB=$B11 zed_orch/gcp_run.sh $VM "$(cmd_b 11000000)"
BG=1 NOSYNC=1 JOB=$B12 zed_orch/gcp_run.sh $VM "$(cmd_b 12000000)"
started13=0
while true; do
  if [ $started13 = 0 ] && { done_job $B11 || done_job $B12 || done_job $GEN; }; then
    BG=1 NOSYNC=1 JOB=$B13 zed_orch/gcp_run.sh $VM "$(cmd_b 13000000)"; started13=1
  fi
  if [ $started13 = 1 ] && done_job $GEN && done_job $B11 && done_job $B12 && done_job $B13; then break; fi
  sleep 120
done
for j in $GEN $B11 $B12 $B13; do echo "$j rc=$(rc_of $j)"; ACTION=pull JOB=$j zed_orch/gcp_run.sh $VM; done
echo "ALL DONE ($MODE). Next: $ENVP ../../.venv/bin/python -B zed_orch/t27_fix_r2/g6_a50_r2.py agg ; localize_staging.py ; report_gates.py"
