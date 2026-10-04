# FAST_THINK_PLAN: the fastest honest think mode for OpenDecide

Date: 4 Oct 2026. Desk plan only: no Modal, gcloud or paid calls were made; no sealed or quarantined folders were opened.
Inputs: `R_tokens.md` (fewer thinking tokens) and `R_serving.md` (faster tokens), same folder. Every number below comes from those two reports (URLs there and repeated in §6) or is marked **[E]** = my estimate. "Unknown" = nobody has published it.
Scope: think mode = the **same Qwen3.5-4B, LoRA off, thinking on or short-CoT**, opt-in, for hard knowledge / math / code questions. Fast path (4B + LoRA, one pass) is unchanged.
Goal-flow note: think mode is **not a step in the current /goal (B → OHS-1/2 → C)**. The owner must add it as a numbered step before any paid pilot, and each pilot needs a PREREG amendment + GO.

## 0. TL;DR

1. Think mode is slow for two reasons that multiply: **too many tokens** (Qwen3-4B thinks ~2,175 tokens on GSM8K, ~9,294 on GPQA-D) and **slow tokens** (~25 tok/s on our L4 with HF eager).
2. **Faster tokens (no accuracy loss):** SGLang/vLLM + the ready-made drafter `z-lab/Qwen3.5-4B-DFlash` (Apache-2.0). Measured 3.4-4.6x on Qwen3.5-4B (B200). H100 estimate **~800 tok/s [E]**, i.e. ~30x today.
3. **Fewer tokens:** route only hard items; short CoT (≤300 tokens) for math; thinking budget + DEER early exit for code and science; later a same-4B concise self-distilled LoRA.
4. **What reaches Jev-like speed:** easy items (already ~20-50 ms) and math-like items (**~0.3-0.8 s**). Code ~1-2 s. **Expert science cannot reach ≤1 s** with a real accuracy gain: ~4-6 s for GPQA ~55-62; GPQA 76 needs long thinking (~15-40 s even fully optimized).
5. Cost at 5% routing on one H100: **~$0.15 per 1,000 decisions** at batch 1 (busy GPU) or **~$0.03** batched [E]; an always-warm H100 is a fixed **~$95/day**, which dominates at low volume.
6. Pilot path: free code work → serving pilot (~$4-8) → FP8 check (~$4) → token/router pilot (~$4-8) → two LoRA pilots (~$8-15 each). Total **≤ ~$50**, each step owner GO.

## 1. The design (router + fewer tokens + fast decoding + hardware)

```
request ──► FAST PATH (4B + LoRA, one pass, ~20-50 ms H100 [E])
              │ answer + confidence (existing calibrated probe) + item type
              ▼
        think opt-in?  AND  type ∈ {math, code, science/knowledge}  AND  confidence < τ
              │ no  → return fast-path answer (95% of traffic)
              │ yes (target ≤5%)
              ▼
        THINK SERVER (base Qwen3.5-4B, LoRA off, + DFlash drafter), per type:
          math-like   → thinking OFF, short step-by-step, cap 300 tok, 4 samples, vote
          code        → thinking ON, budget 1,500, DEER early exit, 1 sample
          science     → thinking ON, budget 4,000, DEER early exit, 4 samples, short-m@k vote
          (deep tier) → thinking ON, budget 32K, async only, for callers who accept 15-40 s
```

### 1a. Router (no training)
- **Signals already in hand:** the fast-path answer, its calibrated confidence, and an item-type tag (from the request schema, or a tiny rule/probe classifier on the prompt). τ is set on a dev stream so that **≤5%** of traffic routes.
- **Optional math pre-check (DART-style):** 2 no-think drafts; if both agree with the fast-path answer, skip thinking. Caution: at 4B, DART lost **5 points on MATH-500 (70.5 → 65.5)** because small-model drafts agree on the same wrong answer. Use only if the pilot shows accepted-answer precision does not drop.
- **UX trick (honest):** return the fast-path answer at ~40 ms as "provisional", then send the think-mode answer when ready. This feels fast but does not make the final answer faster.

### 1b. Token reduction, per type
| Type | Mode | Cap | Early exit | Width | Expected tokens (serial) | Evidence |
|---|---|---|---|---|---|---|
| Math-like | thinking OFF, "solve step by step, briefly" | 300 | none (short already) | 4 samples, majority vote | 100-300 | Qwen3-4B short CoT **82.2% at 85 tokens** vs **38.4%** no CoT (trained; SLT paper) |
| Code-reasoning | thinking ON | 1,500 | **DEER** (geometric-mean confidence ≥0.95) | 1 | ~1,000-1,500 | DEER on Qwen3-4B HumanEval: **3,768 → 1,050 tokens, 91.5 → 92.7** |
| Expert science | thinking ON | 4,000 | **DEER** | 4 paths, stop when first 2-3 agree (short-m@k) | ~2,500-3,500 | DEER on Qwen3-4B GPQA-D: **9,294 → 3,275 tokens, 46.5 → 47.5** |
| Deep tier (async) | thinking ON | 32,768 | DEER | 1-4 | ~10-20K [E] | Qwen3.5-4B card: GPQA-D **76.2** at a 32K budget |

- Budget enforcement on Qwen3.5: **SGLang's Qwen3 thinking-budget processor silently does nothing on Qwen3.5** (SGLang #25536). Use `--enable-strict-thinking` + `max_thinking_tokens`, vLLM ≥0.25 `thinking_token_budget`, or our own splice of Qwen's stop string ("Considering the limited time by the user, I have to give the solution based on the thinking directly now.\n</think>.\n\n").
- **Width is cheap at batch 1** (decode is memory-bound, so 4 samples cost little more time than 1). Unmeasured on our stack; BAEE on Qwen3-8B-Think: **+5 points at 63-76% lower latency** (3.6x total tokens).
- **DEER + speculative decoding is an engineering risk:** DEER needs trial-answer probes at "Wait" points. Plan: client-side chunked generation (stop on "Wait"/"\n\n", probe, continue). Each probe re-prefills (~10-50 ms [E]) unless prefix caching is safe. Measure in pilot T1.

### 1c. Decoding stack (lossless parts first)
| Layer | Choice | Gain | Accuracy cost | Notes |
|---|---|---|---|---|
| Engine | **SGLang** (or vLLM pinned, ≥0.25) with CUDA graphs | HF eager → engine: the main bs=1 fix on H100 (CUDA graphs alone 1.26x for a 7B) | none | vLLM: pin the version (0.26 → 0.29 had a 3.3x decode regression, #57680) |
| Speculation | **DFlash** `z-lab/Qwen3.5-4B-DFlash`, block 8-16 | **3.4-4.6x** measured (B200, greedy); ~15-20% less at temperature 1 | none in theory (lossless) | Beats native MTP (2.0-2.1x) and EAGLE-3 (2.1x vs 3.3x on GSM8K). Check presence_penalty 1.5 is honoured under speculation (unknown) |
| Fallback speculation | native MTP, 2-3 steps | 2.0-2.1x measured | none | No extra weights; once measured slower than no-MTP under heavy load (#47277) |
| Weights | **BF16 by default; FP8 only if dev check passes** | ~1.25-1.4x [E] for a 4B | ≤1 point (W8A8, paper 2504.04823) | **No INT4** in think mode: −1.3 to −2.1 avg, up to 4x worse on hard math |
| Prefix cache | **off** on the think server | little (short prompts) | avoids bug #53912 (~0.8% corrupted outputs with prefix cache + MTP on GDN hybrids) | Revisit if DEER probes need it |
| Layout | 2 processes on 1 GPU: fast path (C1 merged / LoRA) + base 4B + drafter | — | — | ~9 + 9 + 1 GB weights on an 80 GB H100; avoids LoRA + speculation in one engine |

If think mode later uses a **self-distilled LoRA (P1)**, the drafter was trained on the base model, so acceptance will drop. Re-fit it: FastMTP head (443 s on 2×H200, under $1) or DFlash via Speculators/SpecForge (cost unknown).

### 1d. Hardware
- **Default: Modal H100** ($3.95/h list in R_serving; we budget $4.09/h), per-second billing, `min_containers=1` for the think server (a cold start would add tens of seconds [E]).
- **Latency tier: B200** ($6.25/h, ~1.6x the price) gives ~1.5x faster decode with DFlash (1,300 tok/s [M, greedy, discounted]). Only if pilot S3 shows the ~0.8 s / 1K-token tier matters to customers.
- **L4: dev only.** It is bandwidth-capped at ~35 tok/s; even FP8 + DFlash only reaches ~110 tok/s [E].
- **Fast-chip providers cannot host us today.** Cerebras: custom weights are enterprise private preview (no Qwen3.5 listed). Groq: LoRA only on Llama-3.1-8B, enterprise only. Fireworks: no Qwen3.5 in the upload list. SambaNova: unknown.

## 2. Latency per question type (batch 1, temperature 1, network not included)

Cell = **wall time · accuracy kept**. Accuracy anchors from our own runs: GSM8K think-off **57** → full think **~88**; GPQA-D think-off **40** → short think **57** → long think **76**. Code: our own number is unknown; proxy = Qwen3-4B HumanEval think 91.5. All H100 / fast-chip times are **[E]** from R_serving §7 rates (H100 + DFlash ~800 tok/s, 650-1,000). Accuracy for the optimized columns is an **[E] transfer from Qwen3 / R1-Distill papers**; nothing is measured on Qwen3.5-4B yet.

| Question type (think tokens) | Today (L4, HF eager, full think) | H100 optimized (engine + DFlash + caps + DEER + router, no training) | H100 + concise-trained (P1b / P1 LoRA) | Fast-chip provider (hypothetical, ~1,800 tok/s, TTFT 0.2-0.45 s) | Jev |
|---|---|---|---|---|---|
| Easy, fast path (0) | ~114 ms p50 raw · 100% (it is the fast path) | **~20-50 ms** · 100% | same | 0.2-0.45 s (TTFT-bound) · 100% — slower than self-host | ~0.2 s (OpenRouter p50 ~170-240 ms) |
| Math-like (today ~2K; opt 100-300) | 10 s-2 min · ~88 | **0.4-0.8 s** · ~75-85 (keeps ~60-90% of the +31 gain) | **0.25-0.5 s** (~100-150 tok) · ~78-86 (proxy: 82.2 @85 tok vs 94 think vs 38 no-CoT = ~79% of gain) | 0.3-0.6 s · same as model | ~0.2 s |
| Code-reasoning (today ~3.8K; opt ~1-1.5K) | ~1-2.5 min [E: 3,768 tok ÷ 25] · full | **1.2-2.0 s** · ~90-100% of think gain (DEER kept 92.7 vs 91.5) | **0.7-1.2 s** (~600-900 tok) · ~85-100% (unmeasured) | 0.75-1.1 s · same | ~0.2 s |
| Expert science (today 9K+; opt ~3K, 4 paths) | short think 57 at ~1-2 min; long think 76 at ~20 min [E: 32K ÷ 25] | **4-6 s** · GPQA ~55-62 (DEER held Qwen3-4B at +1 pt with −65% tokens) | **2.5-4 s** (~2-2.5K tok) · ~55-62 (no GPQA train split; transfer only) | 1.8-2.4 s · same | ~0.2 s |
| Deep science tier (async, 10-20K) | not usable | **15-40 s** · up to ~70-76 (unknown how much survives DEER) | 10-25 s · unknown | 6-12 s · same | n/a |

B200 + DFlash (self-host) instead of H100: multiply the H100 think times by ~0.65 (math ~0.25-0.5 s, code ~0.8-1.3 s, science ~2.7-4 s) [E].
Blended at 5% routing (mix 50% math / 25% code / 25% science) [E]: **mean ~0.13 s** (beats Jev's ~0.2 s), **p95 ~0.05-0.6 s**, **p99 ~4-6 s** (Jev's tail is flat at ~0.2 s).

## 3. What can honestly reach ~0.2-1 s, and what cannot

**Can reach it**
- **Easy items (fast path): yes, already.** ~20-50 ms on an H100 [E] vs Jev ~0.2 s. No think tokens.
- **Math-like items: yes, ~0.3-0.8 s** on an H100 (≤300 short-CoT tokens at ~800 tok/s), ~0.25-0.5 s on a B200 or after the P1b short-CoT LoRA. Price: about **2-12 points below full thinking** on GSM8K-class items (~75-86 vs ~88), still **+18-29 over think-off (57)** [E].
- **Exactly ~0.2 s for math is only possible with ≤~100 tokens on a B200 (or a fast chip we cannot get).** Realistic target: 0.3-0.5 s.

**Borderline**
- **Code-reasoning: ~1-2 s** (H100), ~0.7-1.2 s after concise training or on a B200. Sub-1 s needs both.

**Cannot reach it (be honest in the pitch)**
- **Expert science: no.** Useful GPQA gains need ~2-3K thinking tokens even with DEER + concise training → **~2.5-6 s**, and that level is ~55-62, not 76.
- **GPQA 76 (long thinking): no.** It needs a 32K budget; even at 1,300 tok/s (B200 + DFlash) that is ~15-25 s for typical items. Offer it only as an async "deep" tier.
- **"No visible tokens" (latent CoT):** not ready. Math-only, 7-10 points below short CoT at 3-8B, no GPQA results, and its public data used GPT-4 traces (we would have to regenerate).
- **Fast-chip providers:** cannot host our 4B today; and for short answers their measured TTFT (0.42 s Cerebras, 0.80 s Groq) is already slower than our self-hosted fast path.

**One-line positioning:** "Same speed as Jev on everyday decisions and simple math; a few seconds when you ask it to think hard; minutes-long deep thinking only on request."

## 4. Pilot plan (cheapest first; every paid step = owner GO + PREREG amendment)

**Data rules for all pilots (clean dev sets only):**
- Tuning / selection only on public **train or dev splits**: GSM8K train (held-out slice of 500 as dev-A), MATH train, MBPP train/validation, **GPQA extended-minus-diamond (348 items) as science dev-A**. Licences on dataset cards: GSM8K MIT, MATH MIT, MBPP CC-BY-4.0, GPQA CC-BY-4.0, MMLU-Pro MIT (verify each before use).
- **Confirm sets, run once, never tuned on:** GSM8K test (1,319), MATH-500, HumanEval, GPQA-Diamond (198).
- **Never** Decision Index, OHS-3 or ejs-5 items; run every pool through the existing C deny-list filter first. Skip `data/ohs3*`, `ohs3_parts/`, `sealed_nd/`, `bench/external_quarantine/`.
- No Jev outputs. Teacher = only our own Qwen3.5-4B. Avoid non-commercial sets (e.g. SciQ is CC-BY-NC).

| Step | What | Cost | Needs |
|---|---|---|---|
| **F0** | Free code work on the laptop: router rule + τ picker; Qwen3.5 budget splice; DEER chunked client (MIT code); short-m@k / majority voter; dev/confirm set builder with deny-list check; latency + accuracy logger | **$0** | none |
| **S1** | Serving pilot on Modal H100: arms (a) no spec, (b) MTP 2-3 steps, (c) DFlash block 8, (d) DFlash block 16. Qwen thinking settings (temp 1.0, top_p 0.95, top_k 20, presence_penalty 1.5), prefix cache off, caps 1K and 4K, ~100 dev prompts for speed + 300 dev items for accuracy | **~$4-8** (1-2 H100-h) | GO |
| **S2** | FP8 dynamic weights + best S1 arm; accuracy on 300 dev items vs BF16 | **~$4** (same session if possible) | GO |
| **T1** | Token / router pilot on the S1 server: budgets 256/512/1K/2K/4K per type; DEER on/off; 1 vs 4 samples; router τ for ≤5% routing on a mixed dev stream; DART check for math | **~$4-8** (1-2 H100-h) | GO |
| **P1b** | **Short-CoT self-distilled LoRA for math-like items** (§4b) | **~$8-12** | GO, after T1 |
| **P1** | **Concise self-distilled LoRA for think mode** (code + science), then drafter re-fit if it ships | **~$10-15** (+<$1 FastMTP) | GO, after T1 |
| S3 (optional) | Best config on a B200 to price the 0.8 s / 1K tier | ~$6 | GO |
| Not now | Length-penalty RL (L1 / ThinkPrune / AdaptThink): stronger (−50 to −65% tokens at ~−2 points) but **~$330-1,000+**; latent CoT; fast-chip enterprise deals | — | — |

**Total pilot spend: ~$30-50.**

### 4a. Pre-registered pass rules: serving and no-training steps
Choose settings on dev-A only; run each confirm set **once**; no re-tuning after confirm.
- **S1 (speculation):** ship the fastest arm that meets all of: p50 decode tok/s **≥2.5x the no-spec arm** at temperature 1.0 (~100 dev prompts); accuracy within **±2 points** of no-spec on 300 dev items (paired); thinking cap obeyed in **100%** of runs; presence_penalty visibly active (repeated-n-gram rate within noise of no-spec). If DFlash fails, take MTP if ≥1.6x; else no speculation.
- **S2 (FP8):** keep FP8 only if accuracy loss **≤1.0 point** (paired, 300 dev items) and speed **≥1.15x**. Else BF16.
- **T1 (per type, H100 stack from S1/S2):**
  - Math: p50 **≤1.0 s** and GSM8K-test **≥77** (think-off 57 + 20).
  - Code: p50 **≤2.0 s** and HumanEval pass@1 **≥ full-think − 3** (full think measured in T1 at an 8K budget).
  - Science: p50 **≤6 s** and GPQA-D **≥55** (short-think 57 − 2). Note: 198 items → ±~3.5 points standard error, so this is a coarse gate.
  - Router: routes **4-6%** of a mixed dev stream; non-routed accuracy unchanged (≤0.5-point drop); routed items **+10 points or more** vs fast path.
  - DEER: answers that exit early are right **≥ (full-budget precision − 2 points)** (small models are weak at stopping).

### 4b. P1b: short-CoT self-distilled LoRA (math-like), ~$8-12
- **Data:** GSM8K train (minus the 500 dev-A items) + MATH train levels 1-3. Base Qwen3.5-4B, thinking OFF, prompt "solve step by step in as few words as possible; end with `Answer:`", 16 samples per item, cap 400 tokens. Keep the **shortest correct** sample (exact answer match). Self-only, so it fits the no-bigger-teacher rule (Munkhbat self-only: −26% length at 99.5% relative accuracy).
- **Cost [E]:** ~10K items × 16 × ~200 tok ≈ 32M tokens ≈ 45 min batched H100 (~12K tok/s with DFlash at concurrency 32 [E: B200 19,759 ÷ ~1.6]) ≈ $3; LoRA SFT on ~2M tokens ≈ $1; eval ≈ $2; retry slack → **$8-12**.
- **Pass rule (confirm once):** (1) mean output **≤150 tokens**, p95 ≤300 on GSM8K-test; (2) GSM8K-test **≥80** AND **≥ best T1 math config − 1 point** at ≤ half its tokens (paired bootstrap 95% CI); (3) p50 wall **≤0.5 s** on the H100 stack; (4) MATH-500 (report) ≥ T1 math config − 3. Fail → keep the T1 config; no second try without a new amendment.

### 4c. P1: concise self-distilled LoRA (thinking on: code + science), ~$10-15
- **Data:** MATH train levels 3-5 + MBPP train/validation (+ APPS train if its MIT licence checks out). Base 4B, thinking ON, OPSDC-style prompt "solve concisely and correctly; be direct", budget 4K, 8 samples per item; keep the shortest correct (answer match / unit tests). No science training data exists under our rules (GPQA has no train split), so science gains are **transfer only**.
- **Cost [E]:** ~3K items × 8 × ~2.5K tok ≈ 60M tokens ≈ 1.4 h batched H100 ≈ $6; SFT ≈ $2; eval with DEER ≈ $2-3; FastMTP drafter re-fit <$1 → **$10-15**.
- **Pass rule (confirm once):** (1) thinking tokens **−30% or more** vs base + same budget + DEER on MATH-500, HumanEval and GPQA-D; (2) accuracy within **−2 points** on MATH-500 and HumanEval, **−3** on GPQA-D (paired; 95% CI lower bound ≥ −4); (3) drafter acceptance length ≥70% of base, else re-fit the drafter and re-measure; (4) science p50 **≤4 s** on the H100 stack. Fail → keep base + DEER.

## 5. Cost per 1,000 decisions (think mode at 5% routing)

Assumptions [E]: all 1,000 decisions run the fast path; 50 are routed (25 math, 12.5 code, 12.5 science); deep tier excluded. H100 at **$4.09/h** (our budget rate; Modal list $3.95/h). L4 price is not in our reports; I use ~$0.80/h [E, verify on modal.com/pricing]. "Batch 1" = one request at a time, GPU kept busy back-to-back (GPU-seconds = wall seconds). "Batched" = ~32 concurrent requests (~12K tok/s with DFlash on an H100 [E: B200 measured 19,759 ÷ ~1.6]; per-request speed drops 2-3x).

| Setup | Fast path GPU-s | Think tokens | Think GPU-s | Total GPU-s | $ per 1,000 decisions |
|---|---|---|---|---|---|
| Today: L4, HF eager, full think, 1 sample | 114 (0.114 s each) | ~210K (25×2.0K + 12.5×3.8K + 12.5×9K) | ~8,400 (÷25 tok/s) | ~8,500 (2.4 h) | **~$1.90** [E] |
| H100 optimized, batch 1 | 35 (~0.035 s each) | ~206K (math 4×250, code 1.3K, science 4×3.3K) | ~98 (25×0.6 + 12.5×1.6 + 12.5×5 s) | ~133 | **~$0.15** |
| H100 optimized, batched | ~5-10 | ~206K | ~17 | ~25 | **~$0.03** |
| H100 + concise-trained, batch 1 | 35 | ~140K (math 4×150, code 800, science 4×2.3K) | ~61 | ~96 | **~$0.11** |
| H100 + concise-trained, batched | ~5-10 | ~140K | ~12 | ~19 | **~$0.02** |
| Deep tier, per item (not in the rows above) | — | ~10-20K | ~15-40 | — | **~$0.02-0.05 per deep item** |

What this means:
- **Even at 5% routing, think mode is ~3/4 of GPU time** at batch 1 (98 of 133 s). Keep routing tight.
- **The real cost is keeping a GPU warm:** one H100 24/7 = **~$98/day (~$2,950/month)**. Per 1,000 decisions that is ~$9.80 at 10K decisions/day, ~$0.98 at 100K/day, ~$0.10 at 1M/day (which needs batching: batch-1 capacity is only ~27K decisions/hour).
- Both processes (fast path + think server) share that one GPU, so think mode adds **no extra fixed cost** until traffic needs a second GPU.
- Jev's price per decision is not in our verified facts (unknown), so no price comparison here.

## 6. Risks and unknowns (check in the pilots)
- **No method here has published numbers on Qwen3.5-4B** (Gated-DeltaNet hybrid, no /think soft switch). All token-reduction numbers are transfers from Qwen3-4B / 8B and R1-Distill 1.5-7B.
- **H100 batch-1 speed of Qwen3.5-4B is unmeasured** (only B200: 356 tok/s, DFlash 1,227-1,637 tok/s at greedy). DFlash acceptance at temperature 1 on Qwen3.5-4B is unmeasured (Qwen3-4B proxy: 3.7-4.0x).
- Whether **presence_penalty 1.5** and the **thinking budget** work under speculation in SGLang / vLLM for Qwen3.5: unknown.
- **DEER + DFlash** in one loop has no public implementation; probe overhead unknown.
- **Whether GPQA's 57 → 76 gain survives at ~1-3K tokens: unknown.** No GPQA accuracy-vs-budget curve exists for a 4B.
- Small models stop badly ("reach but don't commit"; DART −5 at 4B). Always report precision of early-exit / accepted answers.
- Any think-mode LoRA lowers drafter acceptance until the drafter is re-fit.
- vLLM: prefix cache + MTP corruption (#53912, open); 0.26 → 0.29 slowdown (#57680). Pin versions.
- Method data that broke our teacher rule as published (Thinkless R1-671B warm-up, ParaThinker gpt-oss-20b, ThreadWeaver GPT-5, latent-CoT GPT-4 traces): use only self-generated versions.

## 7. Sources (full lists in R_tokens.md and R_serving.md)
- Qwen3.5-4B card (GPQA-D 76.2, 32K budget, MTP flags, Apache-2.0): https://huggingface.co/Qwen/Qwen3.5-4B
- DFlash drafter for our base (B200 bs=1: 356 → 1,227-1,637 tok/s): https://huggingface.co/z-lab/Qwen3.5-4B-DFlash ; paper https://arxiv.org/abs/2602.06036 ; LMSYS ablation (3.3x vs EAGLE-3 2.1x): https://www.lmsys.org/blog/2026-06-15-next-generation-speculative-decoding-dflash-v2/
- Efficient Qwen contest (Qwen3.5-4B, INT4 + DFlash 3.3-3.6x, GPQA-D 0.680 → 0.667): https://arxiv.org/abs/2607.04244
- DEER early exit (Qwen3-4B GPQA-D 9,294 → 3,275 tok, 46.5 → 47.5; MIT code): https://arxiv.org/pdf/2504.15895 , https://github.com/iie-ycx/DEER
- Short CoT on Qwen3-4B (82.2% @ 85 tok; 38.4% no CoT): https://arxiv.org/html/2605.25745v1
- Concise self-training (self-only −26% length, 99.5% rel. acc.; SFT 2 min 24 s on one H100): https://arxiv.org/html/2502.20122
- OPSDC (Qwen3-8B MATH-500 −58.8% tokens, +8.9): https://arxiv.org/html/2603.05433v4 ; BIRD (3,099 → 1,115 tok, 86.2 → 92.0): https://arxiv.org/abs/2607.15736
- DART router (Qwen3-4B MATH-500 −5.0): https://arxiv.org/html/2606.23181 ; BAEE parallel probes: https://arxiv.org/html/2604.06613 ; short-m@k: https://arxiv.org/html/2505.17813
- L1 length control (1.5B MATH 70.8 @512, 78.3 @1,024): https://arxiv.org/html/2503.04697 ; ThinkPrune: https://arxiv.org/html/2504.01296
- Quantization vs reasoning (FP8 ≤1 pt; INT4 −1.3 to −2.1): https://arxiv.org/html/2504.04823v2
- FastMTP drafter re-fit: https://developers.redhat.com/articles/2026/09/08/optimize-vllm-speculative-decoding-fastmtp-heads
- SGLang thinking-budget trap on Qwen3.5: https://github.com/sgl-project/sglang/issues/25536 ; vLLM bugs: https://github.com/vllm-project/vllm/issues/53912 , https://github.com/vllm-project/vllm/issues/57680
- Providers: Cerebras https://artificialanalysis.ai/providers/cerebras ; Groq LoRA https://console.groq.com/docs/lora ; Modal pricing https://modal.com/pricing
- Dev / confirm sets (verify licences): https://huggingface.co/datasets/openai/gsm8k , https://huggingface.co/datasets/Idavidrein/gpqa , https://huggingface.co/datasets/google-research-datasets/mbpp , https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro
