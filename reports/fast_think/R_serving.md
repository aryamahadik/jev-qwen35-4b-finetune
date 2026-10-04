# R_serving: making think-mode tokens come out faster

Date: 4 Oct 2026. Desk research only: no Modal, gcloud or paid calls were made.
Scope: think mode = the same Qwen3.5-4B with thinking ON and our LoRA OFF.
Labels: **[M]** = measured by the cited source. **[E]** = my estimate (method shown). "Unknown" = I found no public number.

---

## 0. Bottom line

1. **The speed-up is in the serving stack, not the model.** Moving from HF eager to SGLang or vLLM (CUDA graphs) plus **speculative decoding** gives about **10-50x more tokens/s** than our L4 today.
2. **A ready-made drafter exists for our exact base model.** `z-lab/Qwen3.5-4B-DFlash` (Apache-2.0, about 0.5B) works because think mode runs the base 4B with LoRA off, so the drafter's training target is our target. On one B200 at batch 1, with thinking on and greedy decoding, it measured **1,227-1,637 tok/s vs a 356 tok/s baseline (3.4-4.6x)** on GSM8K, MATH500 and HumanEval [M].
3. **Speculative decoding does not change accuracy.** The output distribution is unchanged in theory, so the GPQA and GSM8K gains from thinking are kept. Quantization is not lossless: FP8 (W8A8) costs ≤1 point, INT4 costs about 1-2 points on average and more on hard math [M].
4. **Expected wall time on one H100 with DFlash** [E]: **~0.4 s for 300, ~1.3 s for 1,000 and ~6 s for 5,000 thinking tokens.** With FP8 added: 0.36 / 1.1 / 5.3 s. On a B200: **0.26 / 0.8 / 3.9 s.** Today on the L4: 12 / 40 / 200 s.
5. **Sub-second math is reachable only if the thinking is short.** That means ≤ ~800 tokens on an H100 or ≤ ~1,200 on a B200 (≤ ~350 tokens without speculation). The "few seconds for hard science" goal needs ≤ ~2,500-4,000 thinking tokens. Shortening the thinking (self-distillation, caps) is a separate track, and the two effects multiply.
6. **Fast-chip providers (Groq, Cerebras, SambaNova) cannot host our 4B today.** None of them lists Qwen3.5. Custom weights are enterprise or private-preview only. Groq's LoRA support covers only Llama-3.1-8B. The serverless hosts that do serve Qwen3.5 small models are *slow*: Together's Qwen3.5-9B measures 93 tok/s [M]. **Self-hosting on an H100 or B200 is the fastest and cheapest path.**
7. **Next step:** a ~$4-8 Modal H100 pilot (owner GO) measuring baseline vs MTP vs DFlash at Qwen's thinking sampling settings. See §8.

---

## 1. Why we are slow today: memory bandwidth

- At batch 1, each new token reads **all the weights once**. Qwen3.5-4B in BF16 is about **8-9 GB** of decoder weights plus LM head [E: 4B params × 2 bytes; the vision tower is not read during decode].
  - **L4:** 300 GB/s, so at most **~35 tok/s**.
  - **H100 SXM:** 3.35 TB/s, so at most ~390 tok/s.
  - **B200:** 8 TB/s, so at most ~950 tok/s.
- In practice small models reach only part of that ceiling because of kernel-launch and scheduling overhead:
  - On an H100, a 7B model reached only **27%** of the bandwidth ceiling without CUDA graphs. CUDA graphs alone gave **1.26x** [M, arXiv 2605.30571]. On an L4 the same change gave only **1.03x**: the L4 is truly bandwidth-bound.
  - On an L4, a 7B model took **62 ms/step in BF16** and **17 ms/step with GPTQ + ExLlamaV2** [M, same paper]. So on the L4 only smaller weights or speculation help.
- **The hybrid design helps long thinking.** Qwen3.5-4B is `8 × (3 × Gated DeltaNet + 1 × Gated Attention)`, with 4 KV heads × 256 dim in the attention layers [M, model card].
  - KV cache ≈ 8 layers × 2 × 4 × 256 × 2 B ≈ **32 KB/token**. 5,000 tokens is only ~160 MB.
  - The DeltaNet state is fixed-size: ~24 layers × 32 heads × 128 × 128 × 4 B ≈ **50 MB**.
  - So **time per token stays almost flat as thinking gets longer** [E from config]. A plain transformer of the same size slows down as its KV cache grows.

## 2. Measured decode speeds, batch 1 (single request)

| Model | GPU | Engine / precision | tok/s (bs=1) | Source |
|---|---|---|---|---|
| **Qwen3.5-4B** (thinking on, greedy, 4K max) | B200 | SGLang, BF16 | **356-360** | [M] z-lab model card |
| Qwen3-4B (MATH500) | B200 | SGLang, BF16 | 316 | [M] DFlash paper, Table 3 |
| Qwen3-8B (MATH500) | B200 | SGLang, BF16 | 230 | [M] DFlash paper |
| Llama-3.1-8B | H100 | SGLang, BF16 | 158 | [M] EAGLE-3 paper |
| Llama-3.1-8B | H100 | vLLM BF16 / INT4 | 146 / 193 | [M] FlashFormer paper |
| Llama-3.1-8B | H100 | FlashFormer whole-model kernel, BF16 / INT4 | 184 / 311 | [M] FlashFormer |
| Qwen2.5-7B | H100 | vLLM 0.25, BF16 vs on-the-fly FP8 | ITL 6.03 ms (166 tok/s) vs **4.11 ms (243 tok/s)**, i.e. 1.47x | [M] h100-fp8 benchmark repo |
| Llama-3.1-8B | H100 | Simplismart (tuned), FP8 | 501 peak / ~350 sustained | [M, vendor claim] |
| Llama-3.2-1B | H100 | Hazy "megakernel" | <1 ms/forward; 2.5x vLLM, 1.5x SGLang | [M] research code, no GDN support |
| **Qwen3.5-4B** | **H100** | SGLang/vLLM BF16 + CUDA graphs | **~250 (200-300)** | **[E]**: B200 356 ÷ ~1.45 (the Qwen3-8B B200 vs Llama-8B H100 gap), and 7B ITL scaled by weight size gives ~3.5-4 ms/token |
| Qwen3.5-4B | L4 | HF eager (ours today) | ~25 (20-30) | [E], consistent with our 35 s - 2 min think latencies |

**Batched (throughput)** [M]:
- Qwen3.5-4B on a B200 at concurrency 32: **7,573 tok/s total (~237 per request)** with no speculation. With DFlash block 8: **19,759 tok/s (~617 per request)**.
- Qwen2.5-7B on an H100 (vLLM, concurrency 64): 5,836 tok/s in BF16 and 8,068 in FP8.
- Llama-3.1-8B FP8 with TensorRT-LLM at max throughput: 26,401 tok/s.

**Lesson:** per-request speed drops ~2-3x under load. Think mode should run at low concurrency. Bulk dev evals should use high concurrency.

## 3. Speculative decoding (lossless; the biggest lever)

| Method | Ready for Qwen3.5-4B? | Measured speed-up | Notes |
|---|---|---|---|
| **DFlash** (block-diffusion drafter, ~0.5B, drafts a whole block in one pass) | **Yes:** `z-lab/Qwen3.5-4B-DFlash` (Apache-2.0, trained at 40K length with sliding-window attention). SGLang `--speculative-algorithm DFLASH`; vLLM ≥0.20 `"method":"dflash"` | **Qwen3.5-4B, B200, bs=1, thinking, greedy:** block 8 = 1,227-1,356 tok/s (3.45-3.76x) on math/code; **block 16 = 1,387-1,637 tok/s (3.9-4.6x)**; accept length 6.7-7.7. At concurrency 32: up to 2.61x (block 8 best) | DFlash paper, Qwen3-4B thinking: ~4.2-4.6x at temp 0 and **~3.7-4.0x at temp 1** (τ 4.6-4.9). In the LMSYS ablation on Qwen3-4B GSM8K, DFlash gave 3.3x vs EAGLE-3 2.1x |
| **Native MTP** (built into Qwen3.5) | **Yes.** vLLM `{"method":"qwen3_next_mtp","num_speculative_tokens":2}`; SGLang `NEXTN`, steps 3, draft tokens 4 (official card) | Same B200 table: **MTP steps 3 = 2.0-2.1x** (739-764 tok/s, τ ≈ 3.3-3.5). Steps 7 ≈ 2.0-2.3x; steps 15 is *slower* (1.5-1.8x) | No extra weights. vLLM issue #47277 found MTP **slower than no-MTP (0.81-0.86x)** in a high-throughput CUDA-graph workload, so we must measure at our own load |
| FastMTP (fine-tune the MTP head on the model's own outputs) | Recipe exists (Red Hat, Sep 2026) | Qwen3.5-9B acceptance per position: 0.897/0.719/0.476 → **0.912/0.776/0.616**; up to 1.25x better ITL | **443 s on 2×H200** with ~5K self-generated GSM8K samples (cost under $1). Allowed under our rules: it uses only our own 4B's outputs |
| EAGLE-3 | No public Qwen3.5-4B head found. Speculators/SpecForge can train one | Llama-3.1-8B, H100 SGLang bs=1: **158 → 373 tok/s (2.36x)**. R1-Distill-Llama-8B GSM8K temp 1: 4.38x, τ 6.10 | DFlash beats it on the same targets |
| Medusa | Older | Paper: Medusa-1 >2.2x, Medusa-2 2.3-3.6x (Vicuna-class 7B) | Superseded by EAGLE-3 and DFlash |
| Quantized target + DFlash (ICML 2026 "Efficient Qwen" contest, **Qwen3.5-4B**, A10G) | Recipe public | INT4-AWQ target alone 2.16x. **+ DFlash drafter 3.32x**, + INT4 drafter 3.55x (ablation). Final entries reached **6.98-7.75x** end-to-end over the contest baseline. Drafter τ: GSM8K 6.28, HumanEval 5.53, average 5.03 | Accuracy after INT4 + QAD: GPQA-D 0.680 → 0.667, MMLU-Pro 0.680 → 0.661 (contest setting, thinking not stated) |

**Caveats:**
- Speculation is lossless only if the sampler is implemented correctly. Qwen's thinking settings use temperature 1.0, top_p 0.95, top_k 20 and **presence_penalty 1.5**.
  - SGLang lists no penalty limitation for DFLASH. It does list one for its UNO mode.
  - Whether presence_penalty is honoured inside spec-decode in vLLM and SGLang for Qwen3.5 is **unknown**. The pilot must check it.
- Speed-ups are smaller at temperature 1 than at greedy: roughly 10-20% lower in the DFlash paper.
- **If think mode later uses a self-distilled (fine-tuned) model**, the drafter must be retrained or fine-tuned on that model's own outputs. Speculators v0.5 and SpecForge both support this; FastMTP is the cheapest option.

## 4. Quantization: speed vs reasoning accuracy

| Format | Decode speed-up at bs=1 | Reasoning accuracy cost | Source |
|---|---|---|---|
| FP8 W8A8 (H100/L4/B200 all support FP8) | 7B on H100 vLLM: ITL 0.68x, i.e. **1.47x**. For a 4B expect **~1.25-1.4x** [E: launch overhead is a larger share] | W8A8 "lossless (≤1%)" on all models down to 1.5B; Qwen3-8B 75.8 → 76.5 | [M] arXiv 2504.04823 |
| INT4 W4A16 (AWQ/GPTQ, Marlin kernel) | Llama-8B H100: vLLM 1.32x, FlashFormer 1.69x over BF16. On an A10G, Qwen3.5-4B INT4 gave 2.16x | **−1.3 (Qwen3-8B), −2.1 (R1-Distill 1.5B and 7B)** average. Hard tasks (AIME) lose up to **4x more** than GSM8K. Smaller models are more sensitive. QAD recovers part of it (contest: GPQA −1.3) | [M] 2504.04823; 2607.04244 |
| W3A16 | — | −6 to −19 points. **Do not use** | [M] 2504.04823 |
| FP8 KV cache | ~no gain for us: the KV cache is only ~32 KB/token | SGLang warns it can hurt reasoning without calibrated scales | [M] SGLang Qwen3.5 cookbook |

- Qwen ships official FP8 checkpoints only for 27B and above. For the 4B we would make FP8 ourselves (llm-compressor FP8_DYNAMIC, or vLLM `--quantization fp8` on the fly) and re-check accuracy on dev items.
- "Quantization inflates reasoning" (arXiv 2606.25519): low-bit (INT4/INT3) models can **write longer chains of thought**, which eats into the speed gain. 2504.04823 says this happens mainly with aggressive low-bit formats on small models.
- **Recommendation:** use FP8 at most. Skip INT4 for think mode, because its whole purpose is accuracy on hard items.

## 5. Engine support for Qwen3.5 (hybrid Gated DeltaNet)

**SGLang**
- Qwen3.5 0.8B-397B are supported, with MTP (`NEXTN`), DFLASH and a Mamba radix cache.
  - Radix cache V2 needs `--page-size 64`.
  - DFLASH disables the overlap scheduler and mixed chunked prefill.
- **Trap:** the built-in Qwen3 thinking-budget logit processor hard-codes Qwen3 think-token ids. On Qwen3.5 tokenizers it **silently does nothing** (issue #166 in Blackwellboy/model-serving-minefield; SGLang issue #25536). Use `--enable-strict-thinking` with `max_thinking_tokens`, or our own splice.

**vLLM**
- Qwen3.5 and native MTP (`qwen3_next_mtp`) are supported. DFlash is supported from **≥0.20**.
- `thinking_token_budget` in SamplingParams exists from **≥0.25**; it needs `--reasoning-parser qwen3`.
- LoRA support for Qwen3.5 was fixed in 0.29.
- Prefix caching for GDN layers uses `mamba_cache_mode` ("align"/"all") and was added in 2026.
- **Known bugs:**
  - **#53912 (open):** prefix caching + MTP on GDN hybrids corrupts ~0.8% of outputs (v0.28).
  - **#57680:** decode throughput fell 3.3x from 0.26 → 0.29 on an H100 (Qwen3.6-35B-A3B-FP8).
  - **Pin a version and benchmark it.**

**TensorRT-LLM**
- `Qwen3_5ForConditionalGeneration` is listed with CUDA graphs and the overlap scheduler. KV-cache reuse = **No**. Chunked prefill = untested. MTP is listed for the MoE variant.
- There are **no published bs=1 numbers for the dense 4B (unknown)** and no DFlash support was found.
- Not worth the integration cost for us now.

**CUDA graphs**
- On by default in vLLM and SGLang. This is the main reason they beat HF eager at bs=1: 1.26x on an H100 for a 7B in the cited paper, and more for small models. They are effectively mandatory.

**Prefix caching**
- Gives little for think mode. The prompt is short (question + one generic think prompt), and prefilling ~500 tokens on an H100 takes ~10-30 ms [E].
- Given bug #53912, **turn prefix caching off on the think server** while speculation is on, unless a pilot shows it is clean.

**Serving layout**
- Run **two processes on one GPU**: (a) the fast path (C1 merged, or the LoRA path) and (b) the base 4B + DFlash drafter for think mode.
- This avoids open questions about LoRA + speculation in the same engine.
- Memory on an H100 (80 GB) is ample: about 9 + 9 + 1 GB of weights.

## 6. Fast-inference providers

| Provider | Small-model speed [M] | Hosts Qwen3.5-4B? | Custom weights / LoRA | Price |
|---|---|---|---|---|
| **Cerebras** | Llama-3.1-8B 1,800 tok/s (AA, 2024). Today AA lists only gpt-oss-120b: **1,764 tok/s, TTFT 0.42 s** | **No** | Dedicated endpoints for enterprise; custom-weight upload is **Private Preview**. The docs name gpt-oss-120b and GLM-4.7 architectures; Qwen3-8B and 1.7B are listed as dedicated models | Not public (dedicated). 8B was $0.10/M (2024) |
| **Groq** | Llama-3.1-8B **634 tok/s, TTFT 0.80 s** (AA); gpt-oss-20b 931 tok/s | **No** (Qwen3-32B and Qwen3.6-27B on the free tier) | LoRA **only on llama-3.1-8b-instant**, ranks 8-64, **enterprise only**; no full custom weights | Llama-8B $0.05/M in, $0.08/M out |
| **SambaNova** | Llama-3.1-8B 1,066 tok/s (2024) | Not found | Custom checkpoints via SambaStack (hosted or on-prem, enterprise); supported architectures not listed (**unknown for Qwen3.5**) | Not public |
| **Together** | **Qwen3.5-9B: 93 tok/s, TTFT 22 s** (AA, reasoning) | Listed on the serverless pricing page (4B and 9B) | Full-weight and LoRA upload to **dedicated endpoints** (Qwen3.5-9B-FP8 is a docs example) | Dedicated H100 **$5.49/h**, B200 $8.99/h. 9B serverless $0.17/M in, $0.25/M out on OpenRouter |
| **Fireworks** | Unknown for Qwen3.5 small | Unknown | Custom-upload architecture list **does not include Qwen3.5**; uploaded LoRAs run on **on-demand only** (no serverless) | ≤4B serverless from $0.10/M |
| Other OpenRouter hosts (DeepInfra, Parasail, Venice, SiliconFlow) | SiliconFlow 9B: 39 tok/s (AA) | 9B only; **4B not on OpenRouter** | No | $0.10-0.25/M out |
| **Modal (self-host)** | As in §2-3 | We control it | Anything | **H100 $3.95/h, H200 $4.54/h, B200 $6.25/h** (per-second billing) |

**Conclusion:** none of the fast-chip vendors can run our 4B (base or LoRA) without an enterprise deal, and that is still unconfirmed for Qwen3.5. Serverless Qwen3.5 hosts are 3-10x slower than a self-hosted H100 with DFlash.

## 7. Expected wall time per thinking path

Formula: **wall time = time to first token (TTFT) + N ÷ decode rate**, at batch 1, temperature 1, excluding network.
- Every rate on an H100 or L4 is **[E]**, built from the measured B200 numbers in §2-3.
- B200 + DFlash is **[M] at greedy decoding**, discounted ~15-20% for temperature 1.
- The final answer after `</think>` adds ~50-100 tokens, i.e. +0.05-0.1 s on the fast paths.

| Path | decode tok/s (range) | 300 tokens | 1,000 tokens | 5,000 tokens |
|---|---|---|---|---|
| L4, HF eager, BF16 (**today**) | 25 (20-30) | 12 s (10-15) | 40 s (34-50) | 200 s (167-250) |
| L4, vLLM/SGLang BF16 + CUDA graphs | 28 (25-32) | 11 s | 36 s | 179 s |
| L4, FP8 + DFlash | 110 (80-150) | 2.9 s (2.2-4.0) | 9.3 s (6.9-12.7) | 46 s (34-63) |
| H100, BF16 + CUDA graphs | 250 (200-300) | 1.24 s (1.0-1.5) | 4.0 s (3.4-5.0) | 20 s (17-25) |
| H100, FP8 | 330 (280-380) | 0.95 s | 3.1 s | 15 s |
| H100, BF16 + native MTP (3 steps) | 450 (350-520) | 0.71 s (0.6-0.9) | 2.3 s (2.0-2.9) | 11 s (10-14) |
| **H100, BF16 + DFlash (block 8-16)** | **800 (650-1,000)** | **0.41 s (0.34-0.50)** | **1.3 s (1.0-1.6)** | **6.3 s (5.0-7.7)** |
| **H100, FP8 + DFlash** | **950 (750-1,150)** | **0.36 s (0.30-0.44)** | **1.1 s (0.9-1.4)** | **5.3 s (4.4-6.7)** |
| **B200, BF16 + DFlash block 16** | **1,300 (1,100-1,500)** | **0.26 s (0.23-0.30)** | **0.80 s (0.70-0.94)** | **3.9 s (3.4-4.6)** |
| *Ref: Groq LPU, Llama-3.1-8B (cannot host us)* | 634 [M] | 1.3 s | 2.4 s | 8.7 s |
| *Ref: Cerebras, gpt-oss-120b (cannot host us)* | 1,764 [M] | 0.59 s | 0.99 s | 3.3 s |
| *Ref: Jev, one pass, no thinking* | — | ~0.17-0.24 s total | | |

Reading the table:
- **Math-like items (target <1 s):**
  - At 300 thinking tokens: 0.3-0.4 s on an H100 with DFlash.
  - At 1,000 tokens: ~1.1-1.3 s on an H100, ~0.8 s on a B200.
- **Hard science (target a few seconds):**
  - At 5,000 tokens: ~5-6 s on an H100, ~4 s on a B200. That meets the target only at the edge.
  - GPQA's 76.2 needs a 32K+ token budget, which would take minutes at any speed, so long thinking also needs length control (other track).
- **Compared with today on the L4:** a **~30x** cut on an H100 and **~50x** on a B200.

## 8. Recommended plan (cheapest first; each paid step needs an owner GO)

1. **Pilot S1 (~$4-8, about 1-2 H100-hours on Modal).**
   - Setup: SGLang (or vLLM ≥0.25, pinned) with Qwen3.5-4B in BF16. Prefix caching off. Qwen thinking sampling: temperature 1.0, top_p 0.95, top_k 20, presence_penalty 1.5.
   - Arms: (a) no speculation; (b) MTP with 2-3 steps; (c) DFlash block 8; (d) DFlash block 16.
   - Workload: ~100 **dev-only** prompts (never Decision Index, OHS-3 or ejs-5 test items) with a 1K and a 4K thinking cap.
   - Log: tok/s, accept length, TTFT, p50/p95 wall time and answer accuracy (arms should match within noise).
   - Also check that presence_penalty and the thinking budget actually take effect with speculation on.
2. **Pilot S2 (~$4, same session if possible).**
   - FP8 dynamic weights + the best speculation arm.
   - Accuracy check on ~300 dev items vs BF16. Keep FP8 only if the loss is ≤1 point.
3. **Optional S3 (~$6, 1 B200-hour).** Run the same best configuration on a B200, to see whether the ~0.8 s / 1K-token tier is worth ~1.6x the price per hour.
4. **Free:** try the L4 with FP8 + DFlash in vLLM, to see whether the free GPU can reach ~100 tok/s for dev work.
5. **Later, only if think mode switches to a self-distilled model:** re-fit the drafter on that model's own outputs.
   - FastMTP head: minutes and under $1.
   - DFlash via Speculators/SpecForge: unknown cost, likely a few GPU-hours.
6. **Side benefit for plan step 3 (dev-fit, ~26-36M generated tokens):**
   - With DFlash at high concurrency, a B200 measured ~19.7K tok/s at concurrency 32 [M].
   - That puts 30M tokens at about **25-50 min (~$3-6)** instead of 6-12 L4-hours [E].

## 9. Unknowns (not found publicly)

- A measured Qwen3.5-4B tok/s on an **H100** at batch 1 (only the B200 is published). All H100 rows above are estimates.
- Whether presence_penalty is applied correctly under DFlash/MTP in each engine for Qwen3.5.
- DFlash and MTP acceptance at **temperature 1 for Qwen3.5-4B specifically** (only greedy is published; the Qwen3-4B temperature-1 figures are used as a proxy).
- FP8 accuracy for Qwen3.5-4B in thinking mode (no published number).
- TensorRT-LLM speed for the dense Qwen3.5 small models, and whether it supports DFlash.
- Custom-weight support for Qwen3.5 at Cerebras, SambaNova and Fireworks (enterprise sales would have to confirm).

## Sources

- Qwen3.5-4B model card (architecture, MTP serving flags, GPQA-D 76.2, sampling): https://huggingface.co/Qwen/Qwen3.5-4B
- z-lab Qwen3.5-4B DFlash card (B200 bs=1 / conc 32 tables, MTP comparison): https://huggingface.co/z-lab/Qwen3.5-4B-DFlash
- DFlash paper (Qwen3-4B/8B, temperature-1 and thinking tables, B200 SGLang): https://arxiv.org/abs/2602.06036 , https://arxiv.org/html/2602.06036
- LMSYS DFlash + Spec V2 blog (Qwen3-4B DFlash vs EAGLE-3 ablation): https://www.lmsys.org/blog/2026-06-15-next-generation-speculative-decoding-dflash-v2/
- Efficient Qwen contest paper (Qwen3.5-4B INT4 + DFlash on A10G, accuracy table): https://arxiv.org/abs/2607.04244 , https://arxiv.org/html/2607.04244v2 ; leaderboard https://d1krc5fcnf73gi.cloudfront.net/
- SGLang Qwen3.5 cookbook: https://lmsysorg.mintlify.app/cookbook/autoregressive/Qwen/Qwen3.5
- SGLang speculative decoding docs: https://docs.sglang.io/docs/advanced_features/speculative_decoding
- FastMTP (Red Hat): https://developers.redhat.com/articles/2026/09/08/optimize-vllm-speculative-decoding-fastmtp-heads
- TreeWY (spec verification on GDN hybrids): https://arxiv.org/abs/2608.20961
- EAGLE-3 paper: https://arxiv.org/abs/2503.01840
- Medusa paper: https://arxiv.org/abs/2401.10774
- FlashFormer: https://arxiv.org/html/2505.22758v2
- Batch-1 bandwidth gap paper: https://arxiv.org/abs/2605.30571
- Hazy Research megakernel: https://hazyresearch.stanford.edu/blog/2025-05-27-no-bubbles
- H100 FP8 vs BF16 (Qwen2.5-7B, vLLM 0.25): https://github.com/sapir-pirski/h100-fp8-quantization-benchmark
- Simplismart Llama-3.1-8B: https://www.simplismart.ai/comparisons/llama-3-1-8b-inference-benchmarks-2026-simplismart-501-t-s-vs-together-ai-bentoml-baseten-on-h100
- Quantization Hurts Reasoning?: https://arxiv.org/html/2504.04823v2
- Quantization Inflates Reasoning: https://arxiv.org/abs/2606.25519
- vLLM issues and PRs: MTP slower than baseline https://github.com/vllm-project/vllm/issues/47277 ; prefix cache + MTP corruption https://github.com/vllm-project/vllm/issues/53912 ; 0.26 → 0.29 regression https://github.com/vllm-project/vllm/issues/57680 ; GDN prefix caching https://github.com/vllm-project/vllm/pull/36649 ; DFlash SWA https://github.com/vllm-project/vllm/pull/40898
- vLLM Speculators v0.5 (DFlash, vllm ≥0.20): https://vllm.ai/blog/2026-05-28-speculators-v050
- vLLM reasoning outputs / thinking budget: https://docs.vllm.ai/en/latest/features/reasoning_outputs/ ; https://github.com/vllm-project/vllm/pull/37112
- SGLang thinking-budget trap: https://github.com/Blackwellboy/model-serving-minefield/issues/166 ; https://github.com/sgl-project/sglang/issues/25536
- TensorRT-LLM supported models: https://nvidia.github.io/TensorRT-LLM/models/supported-models.html ; issue https://github.com/NVIDIA/TensorRT-LLM/issues/12321
- TensorRT-LLM perf overview: https://nvidia.github.io/TensorRT-LLM/performance/perf-overview.html
- Artificial Analysis: Cerebras https://artificialanalysis.ai/providers/cerebras ; Groq https://artificialanalysis.ai/providers/groq ; Qwen3.5-9B providers https://artificialanalysis.ai/models/qwen3-5-9b/providers ; Cerebras 1,850 tok/s Llama-8B https://x.com/ArtificialAnlys/status/1828463912389402896
- Groq LoRA docs: https://console.groq.com/docs/lora
- Cerebras dedicated / custom weights: https://inference-docs.cerebras.ai/dedicated/overview , https://inference-docs.cerebras.ai/dedicated/management-api
- SambaNova: https://sambanova.ai/blog/fastest-inference-best-models , https://docs.sambanova.ai/docs/en/sambastack/service-administration/model-deployment/deploying-models-and-bundles/deploy-custom-checkpoints
- Together: https://www.together.ai/pricing , https://docs.together.ai/docs/custom-models
- Fireworks custom models: https://docs.fireworks.ai/models/uploading-custom-models
- OpenRouter endpoint list (public API, 4 Oct 2026): https://openrouter.ai/api/v1/models/qwen/qwen3.5-9b/endpoints
- Modal pricing: https://modal.com/pricing
