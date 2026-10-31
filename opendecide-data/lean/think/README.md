# think/ — A17 phase B1: fast think mode on an H100

Report-only benchmark app. It never trains, never tunes the router, and never reads OHS-1/2/3, Nimble (other than the
100 SQuAD2 items the L4 already answered), the Decision Index, ejs-5, JevBench or the sealed suite.
**Every Modal run is a paid step and needs the owner's GO** (A17 "Paid steps", B1 ~ $10-15 in total).

## Commands (run from `opendecide-data/lean`)

```bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean

# 0. inputs (already built; re-run only if a source file changes) - local, CPU, no model
../.venv/bin/python think/build_bench_inputs.py

# 1. dry run - CPU only, no Modal, no weights (inputs + sha256, engine configs, image pins, prompt identity on all
#    100 items, answer extraction, DEER loop and scoring on a fake engine, cost estimate and caps)
../.venv/bin/python think/modal_think.py --dry-run

# 2. cost estimate only
../.venv/bin/python think/modal_think.py --estimate
../.venv/bin/python think/modal_think.py --estimate --configs bf16_dflash,bf16_nospec

# 3. the B1 benchmark (PAID, owner GO): 4 configs, one H100 container each, one after another
../.venv/bin/modal run think/modal_think.py::bench --max-minutes 25 --max-usd 15

#    cheaper subset (ship candidate + its no-drafter baseline): ~$2.6 expected, $4.5 worst case
../.venv/bin/modal run think/modal_think.py::bench --configs bf16_dflash,bf16_nospec

#    resume a run: same --run name; finished configs are kept (--force re-runs them)
../.venv/bin/modal run think/modal_think.py::bench --run b1_YYYYMMDD_HHMMSS

# 4. re-score a saved run locally (gold never leaves the laptop)
../.venv/bin/python think/modal_think.py --score think/runs/<run>
```

Do not use `modal run ... --dry-run`: `modal run` builds the image first. The dry run is the plain `python` command.

## Files

| File | What |
|---|---|
| `modal_think.py` | Modal app `opendecide-think`: image, engine configs, `run_config` (H100), `bench` entry point, cost estimator and caps, local scoring, `--dry-run` |
| `think_engine.py` | Think path logic, engine-agnostic: same prompt and answer extraction as `bench/think_check/think_run.py` / `think_rows.py`; DEER-style early exit; SGLang adapter; fake engine for CPU tests |
| `fast_timing.py` | C1 fast-path timing (merged LoRA, `decoder_io.GraphRunner`), run inside the container in C1's own Python env |
| `build_bench_inputs.py` | Builds `data/` (local, CPU) |
| `data/squad2_parity100.jsonl` | 100 SQuAD2 items the L4 answered in A17-B0 (row, rendered user message + sha256); goes to Modal |
| `data/squad2_parity100_local.jsonl` | Gold + the L4 results for those items; **local only** (scoring) |
| `data/fast_rows_dev200.jsonl` | 200 rows of `data/dev.jsonl` (a `gate_dev.SPLITS` dev split), no gold; fast-path timing only |
| `data/inputs_manifest.json` | sha256 of sources and outputs; checked before any run |
| `runs/<run>/` | `plan.json`, one `<config>.json` per container, `summary.json` (a copy also goes to Volume `opendecide:/think_runs/<run>/`) |
| `common.py` | Row keys, gold keys, confidence features, jsonl io, 60/40 dev-fit/confirm split |
| `router.py`, `policies.py`, `hf_backend.py`, `clean_sets.py`, `check_overlap_di.py`, `eval_think.py`, `tests/` | Router + policies + clean sets + B1/B2 rules: see the section at the end |

## Serving stack (pinned)

- **Engine: SGLang 0.5.20**, official image `lmsysorg/sglang:v0.5.20-cu130` (index digest `sha256:06e4f2ed21af...`);
  the container refuses to run if `sglang.__version__` differs.
  - Why not vLLM: R_serving lists both, but the drafter's card documents only SGLang `DFLASH`, and the vLLM route
    for this sliding-window drafter (vllm-project/vllm#40898) was closed without merging (checked 5 Oct 2026).
- **Target:** `Qwen/Qwen3.5-4B` @ `851bf6e8` (base, LoRA off), thinking on, BF16 or online FP8 (W8A8).
- **Drafter:** `z-lab/Qwen3.5-4B-DFlash` @ `9a1996cc`, block 16 (its trained block size; `--block 8` for high
  concurrency). Under FP8 the drafter follows the target's quantization (SGLang default). Speculation is lossless,
  so only the target precision can move accuracy.
- **Prefix (radix) cache OFF** (R_serving 5: the prefix-cache + speculative-decoding corruption on GDN hybrids).
  **CUDA graphs ON** (SGLang default; decode graphs up to batch 64). Seed 0.
- **Configs:** `bf16_dflash` (ship candidate; also runs the fast path), `fp8_dflash`, `bf16_nospec`, `fp8_nospec`.
- **Fast path, same H100:** a second Python env `/opt/fastpath` with `modal_od.PINNED35` (torch 2.14, transformers
  5.17, peft 0.21 = C1's stack) runs `fast_timing.py` as its own process while the think engine is loaded
  (R_serving 5 layout: two processes on one GPU; the think engine takes 55% of GPU memory).
  C1 = `/vol/models/q35_4b_main500k` (adapter sha256 `507d1c29...7db078`, checked), merged.

## Think path = the L4 path (bench/think_check/think_run.py)

- Prompt: system `decoder_io.SYSTEM`, user `decoder_io.user_msg(row)` (LAYOUT `schema_branch_mark`, STYLE `cygnet`),
  chat template with `enable_thinking=True`. `decoder_io.Readout(tok)` is built first (> 26 options render). Every
  item's user message is checked against the input file (sha256 in the manifest).
- Think: T 0.6 / top_p 0.95 / top_k 20 (A17-B0/B0b), at most the cap of new tokens, stop at `</think>`.
- Answer: natural end -> `think + "</think>\n\n"`; capped -> `think + "\n</think>\n\n"`; 8 greedy tokens; first
  `\b([A-Z])\b` = the letter; noul rows: the "Yes..." letter -> yes key, any other letter -> no key.
- **DEER-style early exit** (SGLang has no in-engine early exit, so it is done client-side): the think runs in
  chunks that stop at `Wait` or after 128 tokens; after >= 48 new tokens, the trial answer is probed (think so far +
  `"\n</think>\n\n"`, one greedy token, probabilities of the option letters via `token_ids_logprob`). Stop when the
  top letter's probability >= 0.95. Each chunk and probe re-prefills (prefix cache is off); chunk and probe counts
  are logged so the overhead is visible.

## What one config measures (`run_config`)

| Step | What |
|---|---|
| `parity_768` | the 100 SQuAD2 items at the L4's A17-B0 setting (768 tokens), all in one batch |
| `speed_bs1_{300,1024,5000}` | batch 1, 10 items: TTFT, decode tok/s, wall, accept length, wall at the full budget (TTFT + N / rate) |
| `e2e_bs1_cap{300,1024}` | batch 1, 10 items: full think path (think + answer) wall per item |
| `e2e_bs1_deer1024` | same with the DEER exit |
| `fast_path` (bf16_dflash only) | C1 one-pass readout: p50/p95 ms per decision at batch 1; batched 4/8/16 (per call and per decision); per state; graph-vs-eager probability check |
| `parity_1024`, `parity_deer1024` | the 100 items at the A17-B0b budget, with and without DEER |
| `batched_c{8,32}` | 8 and 32 concurrent requests of 1,024 tokens: total and per-request tok/s |

`summary.json` (local scoring) reports per config: accuracy, parse rate, think tokens, cap/exit shares; paired
H100-vs-L4 on the same 100 items (difference, discordant counts, exact McNemar p); FP8 vs BF16 and DFlash vs no
drafter (paired, same items); DEER vs plain 1,024 (accuracy and token ratio); speed-ups; and the B1 checks it can
measure: fast-path p50 <= 50 ms, think-path median <= 1 s per cap, FP8 loss <= 1 pt (**indicative only**: SQuAD2
items, not the clean math sets). The B1 math-set rule (>= 85% of full-thinking accuracy at <= 1 s median) needs a
clean math dev set and is **not** covered here.
Sampling is at T 0.6, so the H100 and L4 answers are not token-identical; parity is judged on paired accuracy.

## Cost and caps

| | Default plan (4 configs) | `bf16_dflash,bf16_nospec` |
|---|---|---|
| Expected H100 time | ~59 min | ~34 min |
| **Expected cost** | **~$4.4** | ~$2.6 |
| Worst case (every container hits the 30-min Modal timeout) | $9.0 | $4.5 |

- Rate $4.09/GPU-hour (our budget rate; Modal list $3.95) x 1.10 for CPU and memory. The estimate is deliberately
  pessimistic: x1.3 safety, every request assumed to run to its full budget, H100 speeds from R_serving 7 [E].
  One-time CPU image build (~15 GB SGLang image + the fast-path env) is extra, about $0.1 [E].
- **Caps:** a container stops starting new steps at `--max-minutes` (default 25, at most 28); Modal kills it at 30
  minutes. The launcher refuses to start when the expected cost **or** the worst case is above `--max-usd`
  (default 15; never above the hard $15 cap).
- Configs run one after another (the first fills the model cache on the Volume), so a GO for this run covers at
  most the worst-case figure above.

## Known risks (not testable without a GPU; each fails one config, not the run)

- Online FP8 on the Gated-DeltaNet layers in SGLang 0.5.20: if the engine refuses, `engine_start` is recorded as an
  error and that config runs nothing.
- DFlash on Hopper uses SGLang's default attention backends (the card's `fa4` / `trtllm_mha` are Blackwell options).
- The image tag could be re-pushed; the in-container version check catches a different SGLang, and `pip freeze` plus
  the resolved server args are saved in every result.
- The fast path shares the GPU with an idle think engine; numbers under concurrent think load are not measured.

## Router, policies, clean sets and the B1/B2 rules (CPU code; nothing here has run on a GPU)

| File | What |
|---|---|
| `router.py` | Router. Features: C1 top prob, margin, entropy, yes/no, option count, card / text / question length, digit density, maths / code / negation / causal / time cues, (1 - top) x maths / code / digits. Target "thinking helps" = (think_ok - c1_ok + 1) / 2 (A17-B0b fallback). Small L2 logistic (IRLS). Threshold = routed share on dev-fit closest to 10%, never a row with expected gain <= 0. **Fit only on the 9 `gate_dev.SPLITS` dev splits** (paths and keys are checked) |
| `policies.py` | `short_cot` (maths-like: 300-token think, 4 tries in one call, majority vote; ties to C1), `capped_think` (1,024 tokens + DEER), `full_think` (8,192, the B1 reference). Prompt and parsing = `think_run.py` (via `think_engine`); unparsed -> C1's answer. Resumable CLI |
| `hf_backend.py` | transformers backend for the L4 (same interface as `think_engine.SGLBackend`) |
| `clean_sets.py` | Clean sets from public TRAIN/validation splits (PLAN_knowledge_gap section 4): `k_mmlu` (val + dev), `k_arc` (train + val), `k_sci` (SuperGPQA train, Science middle/hard, 4 options). `k_sci2` (MMLU-Pro, split named "test") and `k_gsm8k` (GSM8K train, DI-adjacent) are off unless the owner rules them in (`--allow`) |
| `check_overlap_di.py` | Counts-only overlap (13-gram, boilerplate > 20 items ignored, exact normalised match) against `--ref name=path` (public full test sets; any path inside `bench/external_quarantine` is refused, no default); writes our ids to drop + counts. For the orchestrator |
| `eval_think.py` | A17 B1 / B2 pass rules, exact (integer tests at the boundaries); readings R1-R7 in its docstring; aggregates only |
| `tests/` | 31 CPU tests (fake tokenizer / scripted engine / tiny random Llama / stub model; the cached Qwen3.5 tokenizer for the prompt-identity test) |

```bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean
../.venv/bin/python -m pytest -q think/tests                     # CPU, ~10 s

# Router target (free L4, ~6.2 h): 3,181 dev rows = all 2,587 with C1 top < 0.8 + a 10% hash sample of the rest
../.venv/bin/python think/router.py tasks                        # done: data/router/think_tasks_dev.jsonl (sha in tasks_manifest.json)
../.venv/bin/python think/router.py commands                     # the exact gcloud / think_rows.py steps
../.venv/bin/python think/router.py fit --think think/data/router/think_out_dev.jsonl   # after the L4 run
../.venv/bin/python think/router.py route --rows R.jsonl --c1 P.jsonl --out D.jsonl

# Clean sets (A17: overlap counts-only BEFORE any model reads them)
../.venv/bin/python think/clean_sets.py build                    # done: k_mmlu 1,812, k_arc 4,239, k_sci 2,000 candidates
../.venv/bin/python think/check_overlap_di.py --ref public_tests=<git-ignored folder> [--ref ohs=... --ref jevbench=...]
../.venv/bin/python think/clean_sets.py finalize                 # -> data/clean/<set>.jsonl + manifest.json (fit/confirm sha256)

# Policies on rows (L4: --backend hf; H100 timing needs the SGLang backend at batch 1)
../.venv/bin/python think/policies.py --rows R.jsonl --decisions D.jsonl --out O.jsonl [--batch 1]
../.venv/bin/python think/policies.py --rows R.jsonl --decisions D.jsonl --policy full_think --out F.jsonl

# Pass rules
../.venv/bin/python think/eval_think.py b1 --think O.jsonl --full F.jsonl --b1-summary think/runs/<run>/summary.json [--fp8 .. --bf16 ..]
../.venv/bin/python think/eval_think.py b2 --b1 B1.jsonl --b2 B2.jsonl
```

Open points for the orchestrator:
- The clean maths rows are only 720 (k_mmlu 138, k_sci 582), and SuperGPQA maths is graduate level. The plan's primary clean maths set (K-Math, Claude-written) is not built yet: add it with `clean_sets.py build --extra k_math=<file>`.
- There is no DI default (review 5 Oct: the quarantine is never opened, PLAN_knowledge_gap 4). The public full test sets (MMLU test, GPQA, GSM8K test, ...) must be fetched into a git-ignored folder by the orchestrator and passed with `--ref`. The embedding rule (>= 0.92) is not run.
- `policies.py` measures latency only with a timing backend at batch 1 (`--batch 1`). The B1 maths rule needs H100 numbers, so `modal_think.py` would need a policies step (a paid run).

## Session B1b (PREREG A30; free credit; launch held until Mon 12 Oct 07:00 UTC by the owner's "Data first")

```bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean
../.venv/bin/python think/modal_think.py --b1b-dry-run        # CPU: inputs, configs, state budget, all roles on fakes, scoring
bash think/b1b_copy.sh mahadikarya3                            # free: C1 adapter + sha read-back; base/drafter come from HF
bash think/b1b_launch.sh mahadikarya3                          # guarded detached launch -> LAUNCHED ... | REFUSED ...
bash think/b1b_fetch.sh mahadikarya3 b1b_YYYYMMDD_HHMMSS       # after the driver is done: fetch, score, AFTER ledger lines
```
- Roles (one H100 at a time, one 90-min server-side deadline): ref (no spec: speed, short_cot batched, full_think),
  spec_dflash (`bf16_dflash_m16`), spec_mtp (`bf16_mtp`, NEXTN 3/1/4), fp8 (twin of the gold-free pick), deer.
- B1a's DFlash failure: SGLang 0.5.20 reserves GDN speculative states for (max_running_requests + 1) x draft tokens
  (99 GB at 128 x 16); `_m16` caps it at 13 GB. `spec_state_gb()` and the dry run check every config.
- Clean set: `b1b_sets.py` (GSM8K TRAIN 500, overlap counts in `data/clean_b1b/overlap_report.json`; public refs in the
  git-ignored `data/public_refs/`). Rules: `eval_think.rule_math / rule_fp8 / rule_spec_acc / rule_deer`.
- Cost: expected ~$5.1, worst case $7.92, cap $8 per launch; Phase B cumulative <= $30 (launcher checks the ledger).
