#!/bin/bash
# RUN_ORDER.sh: the exact trial windows of Track A, in the plan's order. NOT meant to be run as one script: launch ONE window,
# wait for its job to finish (ACTION=status), pull its results (./pull_results.sh <name>), read the verdict, then the next.
#
# Every window (vmcode/window.sh, on od-l4b) does, in this order:
#   1. C2 safety: pgrep -f 'crowd_driver|fast_read|replay'; if any is running it waits and polls every 5 min (exit 9 path)
#   2. snapshots the production /server_info, appends "STOP" to ~/opt_r2/PROD_DOWNTIME.log, stops the PRODUCTION server
#      (fast_read.py stop = the process group in ~/jobs/sglang.pid, exactly what start_server.sh does before a start)
#   3. boots the TRIAL server on port 30010 (same command as production + the trial's flags; trial pid/log under ~/opt_r2)
#   4. runs the trial (parity 8,143 + batch-1 x2 + c64 + GPU busy), stops ONLY the trial server (its own pidfile)
#   5. restarts production with ~/reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8
#      --extra-args "--attention-backend triton" (the recorded args), checks /health, diffs /server_info against the snapshot,
#      appends "START ... downtime_s=..." and the diff verdict to PROD_DOWNTIME.log. A trap restores production on any failure.
# Launch (from c2_build/):   BG=1 NOSYNC=1 JOB=r2_<name> zed_orch/gcp_run.sh od-l4b '<command below>'
# Status:                    ACTION=status JOB=r2_<name> zed_orch/gcp_run.sh od-l4b
W=/home/aryamahadik/opt_r2
P=$W/r2pypatch
IDS=$W/data/option_ids_union.json

# T0  BF16 baseline twice (T0a = the parity reference, T0b = reboot floor + a second pass at c64 = batching floor)
bash $W/window.sh T0a generate parity,lat,thr,prefix
R2_EXTRA="--extra-parity-conc 64" bash $W/window.sh T0b generate parity,lat,thr,prefix

# T1  diagnostics (metrics, cache report, GC warnings, py-spy on the trial's own processes during a batch-1 loop)
PRE_CMD='(sleep 25; bash '$W'/t1_diag.sh T1 60) &' POST_CMD='curl -s localhost:30010/metrics > '$W'/results/T1/metrics.txt; grep -ci "gc" '$W'/logs/T1.server.log > '$W'/results/T1/gc_lines.txt' \
  bash $W/window.sh T1 generate lat -- --enable-metrics --enable-cache-report --gc-warning-threshold-secs 0.005

# T2  full-graph prefill (pass only if the capture covers the GDN layers with no fallback: see results/T2/graph_log.txt)
POST_CMD='grep -i -E "capture|graph|fallback|breakable|full" '$W'/logs/T2.server.log | tail -60 > '$W'/results/T2/graph_log.txt' \
  bash $W/window.sh T2 generate parity,lat,thr -- --cuda-graph-backend-prefill full

# T4  front end: (a) input_ids + --skip-tokenizer-init, (b) /v1/score, (c) both.  Token-id identity on all 8,143 is already
#     measured on od-cpu1 (results/T4_token_ids.json).
bash $W/window.sh T4a generate parity,lat,thr -- --skip-tokenizer-init
bash $W/window.sh T4b score    parity,lat,thr
bash $W/window.sh T4c score    parity,lat,thr -- --skip-tokenizer-init

# T5  LM-head slice to the 141 option-token rows (fp32, copied rows, embed_tokens untouched)
TRIAL_ENV="R2_LMHEAD_IDS=$IDS R2_REPORT=$W/results/T5/patch_report.jsonl" TRIAL_PYPATH=$P bash $W/window.sh T5 generate parity,lat,thr

# T3  GC fix, ONLY if T1 shows GC pauses (gc warning lines) or py-spy shows GC time on the batch-1 path
TRIAL_ENV="R2_GC_FREEZE=120 R2_REPORT=$W/results/T3/patch_report.jsonl" TRIAL_PYPATH=$P bash $W/window.sh T3 generate lat,thr

# T8  block-FP8 checkpoint ($W/models/c1_fp8_block, built on od-cpu1, verified; copy to od-l4b first)
TRIAL_MODEL=$W/models/c1_fp8_block bash $W/window.sh T8 generate parity,lat,thr -- --quantization fp8
#     then offline (Mac):  python3 r2_report.py parity results/T0a/answers_P.jsonl results/T8/answers_P.jsonl
#                          python3 r2_report.py gate    results/T0a/answers_P.jsonl results/T8/answers_P.jsonl results/T0b/answers_P.jsonl

# T6 / T7  cache-capacity knobs (parity + the R prefix-repeat cached share + c64 throughput)
DROP_FLAGS="--mamba-ssm-dtype" bash $W/window.sh T6 generate parity,lat,thr,prefix -- --mamba-ssm-dtype bfloat16
bash $W/window.sh T7 generate parity,lat,thr,prefix -- --mamba-track-interval 64

# T10  image fast path: native x2 at c1 and c8 first (noise floor), then one flag at a time against native
MAIN_CMD="~/sgl/bin/python -B $W/r2_vision.py --name T10a --port 30010 --arms native:1,native:1,native:8,native:8" bash $W/window.sh T10a generate -
MAIN_CMD="~/sgl/bin/python -B $W/r2_vision.py --name T10b --port 30010 --arms native:1,native:1,native:8" bash $W/window.sh T10b generate - -- --keep-mm-feature-on-device
MAIN_CMD="~/sgl/bin/python -B $W/r2_vision.py --name T10c --port 30010 --arms native:1,native:1,native:8" bash $W/window.sh T10c generate - -- --mm-processor-worker-num 4
MAIN_CMD="~/sgl/bin/python -B $W/r2_vision.py --name T10d --port 30010 --arms exact:1,exact:1,exact:8"   bash $W/window.sh T10d generate -

# T9  live FP8+BF16 cascade: ONLY if T8 or the gate passes on held-out data (router + two servers; not scripted yet)

# T11 exploratory
DROP_FLAGS="--mamba-radix-cache-strategy" bash $W/window.sh T11 generate parity,thr -- --prefill-only-disable-kv-cache --disable-radix-cache
