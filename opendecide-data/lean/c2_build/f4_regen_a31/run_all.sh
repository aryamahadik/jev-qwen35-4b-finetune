#!/bin/bash
# F4 hedge regeneration (A31 seed hedge fix, spec 3.19). Runs on od-cpu1 via zed_orch/gcp_run.sh, inside c2_build.
# Same steps as c_src/F4/tmp/wording/run_build.sh + run_post_a.sh (no sealed_nd step) + run_post_b.sh + run_qc.sh.
# Output root: c2_build/f4_regen_a31/lean/c_src/F4/{out,logs,qc,solverB}. Nothing else is written.
set +e
R="$(cd "$(dirname "$0")" && pwd)"; LEAN="$R/lean"; F4="$LEAN/c_src/F4"
PY="$HOME/od/bin/python -B"
export PYTHONHASHSEED=0 HF_HUB_OFFLINE=1 F4_KEEP_DRAFTS=1 PYTHONDONTWRITEBYTECODE=1
W=${W:-6}
step() { echo "[$(date -u +%FT%TZ)] $*"; }
fail() { step "FAIL $*"; echo "ALL_FAILED $*"; exit 1; }
cd "$F4/gen"; mkdir -p "$F4/logs" "$F4/tmp"
unset F4_DECILE_PASS
step "plan"; $PY build.py plan > "$F4/logs/plan.log" 2>&1 || fail plan
for s in cand qc dev; do
  step "pass1 gen $s"; $PY build.py gen $s $W > "$F4/logs/gen_$s.log" 2>&1 || fail gen_$s
  $PY finalize.py $s > "$F4/logs/finalize_$s.log" 2>&1 || fail fin_$s
done
$PY decile_targets.py cand > "$F4/logs/targets_cand.log" 2>&1 || fail targets_cand
$PY decile_targets.py qc > "$F4/logs/targets_qc.log" 2>&1 || fail targets_qc
export F4_DECILE_PASS=2
cp "$F4/out/candidates_r1.sidecar.jsonl" "$F4/tmp/candidates_r1.sidecar.pass1.jsonl"
cp "$F4/out/qc_sample.sidecar.jsonl" "$F4/tmp/qc_sample.sidecar.pass1.jsonl"
for s in cand qc; do
  step "pass2 gen $s"; $PY build.py gen $s $W > "$F4/logs/gen_$s.log" 2>&1 || fail gen2_$s
  $PY finalize.py $s > "$F4/logs/finalize_$s.log" 2>&1 || fail fin2_$s
done
$PY finalize.py dev > "$F4/logs/finalize_dev.log" 2>&1 || fail fin_dev
wc -l "$F4"/out/*.jsonl
echo BUILD_DONE
unset F4_DECILE_PASS

# chain A: gates, quota, solver B, G15/G18
( cd "$F4/gen"
  for s in cand qc dev; do $PY gates.py $s > "$F4/logs/gates_$s.log" 2>&1; echo "gates $s rc=$?"; done
  $PY quota.py "$F4/out/candidates_r1.jsonl" "$F4/out/candidates_r1.sidecar.jsonl" > "$F4/logs/quota_cand.json" 2>&1; echo "quota cand rc=$?"
  $PY quota.py "$F4/out/qc_sample.jsonl" "$F4/out/qc_sample.sidecar.jsonl" > "$F4/logs/quota_qc.json" 2>&1; echo "quota qc rc=$?"
  $PY quota.py "$F4/out/mixdev_S5.jsonl" "$F4/out/mixdev_S5.sidecar.jsonl" > "$F4/logs/quota_dev.json" 2>&1; echo "quota dev rc=$?"
  $PY "$F4/solverB/solver_b.py" "$F4/solverB/mismatch.json" "$F4/out/candidates_r1.jsonl" "$F4/out/qc_sample.jsonl" "$F4/out/mixdev_S5.jsonl" > "$F4/solverB/run_final.log" 2>&1; echo "solverB rc=$?"
  cd "$F4/qc"
  $PY g15_g18.py candidates_r1 > g15_cand.log 2>&1; echo "g15 cand rc=$?"
  $PY g15_g18.py qc_sample > g15_qc.log 2>&1; echo "g15 qc rc=$?"
  echo POST_A_DONE ) > "$F4/logs/post_a.log" 2>&1 &
# chain B: G4 metamorphic
( cd "$F4/gen"
  for s in cand qc dev; do $PY g4_meta.py $s 1100 3 > "$F4/logs/g4_run_$s.log" 2>&1; echo "g4 $s rc=$?"; done
  echo POST_B_DONE ) > "$F4/logs/post_b.log" 2>&1 &
# chain C: QC scripts (G6 G7 G10 G11 G12), 1 thread
( cd "$F4/qc"; export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 LOKY_MAX_CPU_COUNT=1
  $PY g12.py > g12.log 2>&1; echo "g12 rc=$?"
  $PY g11.py candidates_r1 > g11.log 2>&1; echo "g11 rc=$?"
  $PY g10.py candidates_r1 > g10_cand.log 2>&1; echo "g10 rc=$?"
  $PY g7.py candidates_r1 > g7_cand.log 2>&1; echo "g7 cand rc=$?"
  $PY g7.py qc_sample > g7_qc.log 2>&1; echo "g7 qc rc=$?"
  $PY g6.py qc_sample > g6.log 2>&1; echo "g6 rc=$?"
  echo POST_C_DONE ) > "$F4/logs/post_c.log" 2>&1 &
wait
cd "$F4/gen"; $PY manifest.py > "$F4/logs/manifest.log" 2>&1; echo "manifest rc=$?"
# G8v3 (AFLite-lite), MiniLM from the mirror's own HF cache
step "g8v3"
HF_HOME="$R/hf" $PY "$LEAN/c_src/common/g8_aflite.py" run --family F4 --pool "$F4/out/candidates_r1.jsonl" --out "$F4/qc/g8v3_candidates_r1.json" --jobs 6 > "$F4/qc/g8v3.log" 2>&1; echo "g8v3 rc=$?"
rm -f "$F4"/tmp/rows_*.pkl "$F4"/tmp/drafts_*.pkl      # big, not needed on the Mac
echo QC_DONE
echo ALL_DONE
