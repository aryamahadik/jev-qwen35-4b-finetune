# VM notes (od-l4b, project system-one-509903, zone us-east4-c)

## Idle SGLang server (C2 crowd-read leftover) - STOPPED by the vision bench job
- Written 2026-10-16 ~20:05 UTC, BEFORE stopping it.
- What it was: SGLang 0.5.20 serving the merged C1 checkpoint, pid 369128 (process group leader, session of its own),
  started 2026-10-16 00:32:27 UTC by `~/reads/start_server.sh` -> `~/od/bin/python -B fast_read.py serve` (C2 tooling), listening
  on 127.0.0.1:30000. It held ~20.2 GB of the L4's 23 GB (mem-fraction-static 0.8), so a second 4B model cannot fit next to it.
- Why it was safe to stop (evidence taken at 19:40-20:05 UTC): 0 established connections to port 30000 in repeated samples
  (6 samples over 30 s, then again just before the stop), GPU utilisation 0 %, server log untouched since 17:47 UTC,
  no fast_read.py client process running, the C2 HANDOFF says "SGLang server left up and idle on od-l4b" after the early crowd
  reads finished (18:25 UTC). The generator jobs that were running (t32_gen.py, t27_gen.py, g6_a50_full.py build) are CPU
  jobs and do not mention port 30000 or sglang.
- Exact command line of the server (from /proc/369128/cmdline):
  /home/aryamahadik/sgl/bin/python -m sglang.launch_server --model-path /home/aryamahadik/models/q35_4b_main500k_merged
  --host 127.0.0.1 --port 30000 --dtype bfloat16 --enable-fp32-lm-head --context-length 16448
  --mamba-radix-cache-strategy extra_buffer --mamba-ssm-dtype float32 --linear-attn-backend triton
  --linear-attn-prefill-backend triton --max-running-requests 32 --max-mamba-cache-size 128 --random-seed 0
  --sampling-defaults openai --log-level warning --mem-fraction-static 0.8 --attention-backend triton
  env: SGLANG_RETURN_ORIGINAL_LOGPROB=1 (plus the exports in ~/reads/start_server.sh: CUDA_HOME, g++-12 shims, TORCH_CUDA_ARCH_LIST=8.9)
- How it was stopped: `cd ~/reads && ~/od/bin/python -B fast_read.py stop` (C2's own stop command: SIGTERM to the pid group in
  ~/jobs/sglang.pid).
- How to restart it (what C2 does): `bash ~/reads/start_server.sh` (stops any old one, TRUNCATES ~/jobs/sglang_server.log, then
  `fast_read.py serve` with default args = the command line above; boot ~3 min). To keep the old log, run the same
  script lines minus the `: > ~/jobs/sglang_server.log` line.
- The vision bench job restores the server after its last GPU use (see "Current state" below).

## Things the vision bench added on the VM (all under ~/vision_bench)
- pylib/: Pillow 12.3.0 and torchvision 0.29.0 wheels unpacked (the od venv has neither); used with PYTHONPATH only.
- data/, harness/, results/, qwen35_processor/ (official preprocessor_config.json of the pinned base revision), triton_cache/.
- Nothing outside ~/vision_bench was written (the HF cache, ~/od, ~/lean, ~/repo were only read).

## Current state
(updated at the end of the run)

## UPDATE 2026-10-16 ~20:10 UTC: the stop was NOT done
- The permission layer denied the command that would have run `fast_read.py stop` on the idle SGLang server (pid 369128).
  Nothing was stopped, killed or restarted on the VM. The server is still up (20.2 GB of the L4 held), so no GPU stage has run.
- Everything that needs no GPU was prepared (see the final report). To run the GPU stages the owner either stops that server
  (command above) or tells the job it may.

## Final state at hand-over (2026-10-16 ~20:50 UTC)
- SGLang server pid 369128: still running, untouched, 20474 MiB on the L4, GPU util 0 %. No GPU stage of the vision bench ran,
  so no GPU time was used and nothing needs restoring.
- CPU-only checks on the VM ran at nice 10-19 (tokenizer + image preprocessing, no model): check_prompts.py, prep_all.py.
  No vision_bench process is left running on the VM.
- To run the GPU stages: first get the GPU free (the owner stops the server with the command above, or allows it), then
  `nohup bash ~/vision_bench/harness/gpu_chain.sh > ~/vision_bench/logs/chain.log 2>&1 &` (it refuses to start if >6 GB is in use),
  then pull ~/vision_bench/results/* to the Mac results/ and run `.venv/bin/python -I harness/score_vision.py`.
  Afterwards restart the C2 server as described above.

## Fix round 2026-10-16 ~21:00-21:30 UTC (review fixes; still no GPU use)
- SGLang server pid 369128: still up, untouched (20474 MiB, GPU util 0 %). The earlier denial of the stop stands; it was NOT retried
  and no other way of stopping it was tried. Nothing was stopped, killed or restarted. The reviewer's CPU-only check (bash pid 1835257,
  nice 19, 1 thread, no GPU) was started by the reviewer, not by this job, and was left alone.
- Added on the VM under ~/vision_bench only: harness/ replaced by the fixed version (old one kept as harness_v1/), tests/ (4 CPU tests),
  vb_push2.tgz, tests/vm_adapter_keys.py, and later (created by the GPU run itself) adapter_c1_renamed/ (a renamed COPY of the C1 adapter,
  ~/lean untouched).
- CPU-only work on the VM this round: tests/test_real_adapter_names.py was started at nice 19 / one thread / CUDA_VISIBLE_DEVICES empty,
  got 9 s of CPU in 22 min (load average 18 on 8 cores) and was killed by this job (its own process, pid 1846155). Replaced by a
  header-only read of the real adapter file (tests/vm_adapter_keys.py, nice 10, no torch): sha256 507d1c29, 496 tensors, 248 lora_B,
  all float32, all keys in the text-only layout, no vision keys, r 16 alpha 32. The same names are checked against the real architecture
  by tests/test_real_adapter_names.py on the Mac (meta device).
- To run the GPU stages (needs the GPU free, i.e. the C2 server stopped by the owner or with the owner's leave):
  `nohup bash ~/vision_bench/harness/gpu_chain.sh > ~/vision_bench/logs/chain.log 2>&1 &`, then pull ~/vision_bench/results/* to the Mac
  results/ and run `.venv/bin/python -I harness/score_vision.py`. Restart the C2 server afterwards (commands above).
