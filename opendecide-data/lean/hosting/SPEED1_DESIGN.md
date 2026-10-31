# SPEED-1 design: faster, cheaper C1 serving (no retraining)

Owner GO: 12 Oct 2026 ("do it perfectly"). This is goal step **SPEED-1** in HANDOFF.md START HERE.
Measurement happens only in SPEED-2, under amendment A35, which is written before any timing.

## Goal and hard rules
- **Model:** C1 = `Qwen/Qwen3.5-4B` @ `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` + LoRA `q35_4b_main500k`, adapter sha256
  `507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078`. It is merged in BF16 with `merge_and_unload`,
  exactly as `hosting/modal_direct_host.boot_gpu` does.
- **Answers must stay C1's (A5 readout):**
  - choice = "2view": read the given order and the exact reversal (`perm = list(range(n))[::-1]`), then average in
    PROBABILITY space per option;
  - noul = a single read;
  - T = 1.0 / 1.0;
  - per-letter logit = logsumexp over the candidate token ids of `dio.Readout.cand(row)`, computed in fp32 from the
    last real token's hidden state: `h.float() @ head.weight[flat].float().T`.
  - References: `decoder_io.predict(tta_choice=True)` (decoder_io.py:688-695), `to_probs` (:611-620), and
    `prep89/t_fit_q35_4b_main500k.json` "ship".
- **Parity bars** (gated in SPEED-2 against a same-session H100 baseline; stored L4 reads are reported as context):
  - argmax agreement ≥ 99.5%;
  - |accuracy diff| ≤ 0.3 pt (≤ 1.0 pt for FP8 arms).
- **Files:**
  - NEW files only, under `lean/hosting/` (code) and `lean/speed/` (outputs).
  - Never edit the pinned `lean/*.py` files (decoder_io.py, prism_x.py, writeblock.py, gate_dev.py, ...). Import them
    read-only or subclass them.
  - Do not edit `hosting/modal_direct_host.py`, `client_bench.py` or `modal_direct_server.py`; import them as `core`.
- **Protected paths, never opened:**
  - any path with "ohs3" in its name (including `prep89/*ohs3*`, `results_ohs3/`, `data/ohs3*`);
  - `preds_ohs*/`, `data/ohs1*`, `data/ohs2*`, `bench/external_quarantine/`, `bench/longbench_v2/`, `sealed_nd/`
    (data), `c_spec/sealed_brief/`, `c_build/preread/`.
  - `prep89/load_test_c1.py` imports `ohs3_lib`, so COPY its pure helpers and never import it.
- **Money:**
  - payer: free Modal credit on **mahadikarya3** only. It has the base model in its Volume hf cache and needs C1's
    adapter uploaded. mahadikarya2 is the fallback.
  - never use aryamhd (card) or jaypatil-duke.
  - one container (`max_containers=1`), an idle shutdown, and a hard function timeout.
  - Every launcher refuses any other profile.

## Why C1 is slow today
Measured or read from code:
- **One request at a time:** a global lock means no cross-request batching (modal_direct_host.py `Decider.lock`).
- **2view runs as one batch of 2:**
  - graphs cover batch 2 only up to 1024 tokens;
  - 36.7% of dev choice rows with 10+ options are over 1024 tokens, and 29.5% are over 2048, which is beyond even the
    batch-1 graphs, so they run eagerly;
  - two sequential batch-1 reads took 31.6 ms vs 56.5 ms for an eager batch of 2 (`extra/SPEED_RESULT_30sep.md`).
- **Private CUDA-graph pools** cost about 0.48 MB per padded token per graph, so longer graphs ran out of memory.
- **Network floor:** about 72 ms from the laptop through the `modal.forward` tunnel.

## Shared HTTP API (both engines; v1)
- **`POST /decide`** (header `Authorization: Bearer <token>`).
  - Request:
    `{"id"?: str, "state": str, "questions": {name: {"type": "noul"|"choice", "instructions": str,
    "options"?: [str] (choice, 2..255), "card"?: str}}}`
  - Limits: at most 16 questions. `card` is the raw definitions card exactly as in dev rows, allowed on noul and choice.
  - The host builds the decoder_io row `{"state","instructions","qtype","options","card"}`. Its prompt text must be
    byte-identical to `dio.Readout(tok).prompt(dev_row, perm)` for the same dev row.
  - Response: `{"answers": {name: A}, "usage": {"input_tokens", "routed_rows": 0}, "timing": {"tokenize_ms",
    "queue_ms", "model_ms", "total_ms"}, "server_ms", "engine": "hf"|"sglang", "path", "batch_rows"}`.
    - noul: `A = {"type":"noul","noul":p_yes,"probabilities":{"yes","no"}}`.
    - choice: `A = {"type":"choice","choice","confidence","probabilities":{opt:p}}`.
    - every A also has `"usage": {"input_tokens", "input_tokens_first_view", "views"}`.
- **`GET /health`:** `{"ok","engine","model","adapter_sha256","base","revision","readout","flags","config_sha256",
  "graphs","gpu","region","boot_s", ...}`.
- **`POST /admin/config {"flags": {...}}`:** changes runtime flags without a reboot. It returns the new `/health`.
- **`POST /admin/flush`:** clears any prefix cache (a no-op if there is none).
- **`POST /shutdown`.**

## Arms
| Arm | Engine | What changes | Boot |
|---|---|---|---|
| A0 | HF | Legacy behaviour: one request at a time, 2view as one batch of 2, only legacy graph shapes (B 1,2,4,8 ≤ 1024; 3,5,6 ≤ 512; B1 ≤ 2048), eager otherwise | HF-BF16 (flag `legacy=true`) |
| A1 | HF | 2view as two batch-1 items; graphs from the new plan (B1 to 4096); tokenization outside the GPU lock; no cross-request batching | same boot, flags |
| A2 | HF | A1 + cross-request opportunistic batching (length-bucketed, no forced wait by default) | same boot, flags |
| A3 | HF | A2 with FP8 rowwise body linears (lm_head, embeddings, in_proj_a/b, conv1d kept BF16) | second HF boot |
| S1 | SGLang 0.5.20 | merged BF16, `--enable-fp32-lm-head`, hybrid radix prefix cache on, prefill-only scoring, no speculation | SGLang boot |
| S2 | SGLang | S1 + `--quantization fp8` | second SGLang boot |

- **HF prefix cache:** not built in SPEED-1. It is 4-6 days of custom work, and on dev it saves little because dev
  rows shuffle option order. S1 measures what prefix reuse is worth on repeated-schema traffic. We build it only if
  SGLang fails parity AND S1 shows a large gain.

## New graph plan (HF arms A1-A3)
- **Bucket ladder:**
  - 64-token steps up to 1024;
  - 128-token steps up to 2048;
  - 256-token steps up to 4096.
- **Batch coverage:**

  | Batch size | Up to |
  |---|---|
  | B=1 | 4096 |
  | B=2 | 2048 |
  | B=4, B=8 | 1024 |
  | B=16 | 512 |
- **Memory:** all graphs share ONE memory pool, captured largest first. Static input/output buffers are allocated
  outside the pool and before capture, and outputs are cloned right after replay. The earlier shared-pool corruption
  (decoder_io.py:474-475) must be ruled out by a per-shape graph-vs-eager self-check at boot. If that fails, fall
  back to private pools with a reduced plan.
- **Warm-up:** run eager warm-up over every shape before capture, so no Triton/fla autotune happens during a request.
- **Above 4096 tokens:** eager.

## Workloads (dev only, in SPEED-2)
- **Parity set P:** all 8,143 rows of the 9 gate dev splits, each row once, one question per call. Reference:
  `preds_<split>/q35_4b_main500k_pre_served.jsonl` (2view) and `_pre.jsonl` (identity view).
- **Speed set S:** unique rows, sampled without replacement.
  - all 387 dev choice rows with ≥ 10 options, plus 273 noul rows (seed 0);
  - so 660 calls, matching the 1440:1016 call mix in `load_test_c1.PREREG_CALL_MIX`.
- **Natural set N:** 660 dev rows, uniform without replacement (seed 1).
- **Repeated-schema set R:** dev tasks with ≥ 20 rows sharing (instructions, option set), with option order made
  canonical per task. No stored reference exists, so answers are compared live with A0. This is the prefix-reuse
  workload.
- **Load levels:** concurrency 1 (latency p50/p95/p99), then 2, 4, 8 and 16 closed-loop for sustained decisions/hour.
  - flush caches between levels;
  - log cached-token share.
- **Jev:** the same S requests at concurrency 1 through OpenRouter, for latency and answers on dev only. This is
  report-only, and Jev outputs are never used for training.
- **Cost:** $/1K = rate × region_mult / sustained decisions per hour × 1000. Report it at 100% and at 0.4
  utilisation, at both the 'any' and the 'us-east' rate. The Modal H100 base rate is $3.95/h (`modal billing rates`,
  12 Oct).
