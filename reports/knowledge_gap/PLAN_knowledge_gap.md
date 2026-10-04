# PLAN: closing the 4B knowledge gap to Jev

3 Oct 2026. Revised the same day after R_skeptic.md. The "Corrections log" at the end lists every change, and every correction that was changed or turned down, with the reason.

This plan combines six reports in this folder: R_testtime, R_retrieval, R_tools, R_training, R_measure and R_skeptic. It also uses the committed Decision Index (DI) aggregates in `bench/decision_index/report_sample10k.json` and `check_index_math.json`. These files hold only scores, not test items.

No runs were made, no paid calls were made, and no held-out files were opened. Every number marked "estimate" is a projection. It must be measured on clean dev sets, never on the DI.

## 0. In plain words

1. **The gap is mostly a "no thinking time" gap, not a "missing facts" gap.**
   - C1 has to answer in one quick read.
   - Our own base model, Qwen3.5-4B, scores **76.2 on GPQA Diamond when allowed to think** for up to 32K-82K tokens. Jev scores 78.6 and C1 scores 39.8. Source: https://huggingface.co/Qwen/Qwen3.5-4B
   - With short thinking caps the score is much lower. The exact value is unknown until we measure it.
2. **Best way:**
   - Keep today's fast one-pass answer as the default.
   - Add an optional "auto" mode. A small learned gate sends hard items to the **same 4B with thinking on and our LoRA off**.
   - Every routed item gets **one generic think prompt**, with no per-benchmark branches.
   - No new teacher and no training. C1 stays unchanged.
3. **Expected result (estimate; middle value with range):**

   | | Ours now | Ours with auto mode | Jev |
   |---|---|---|---|
   | Knowledge area | 51.2 | **64.1 (58.0-69.9)** | 68.9 |
   | Index, other areas unchanged | 54.83 | **57.4 (56.2-58.6)** | 59.51 |
   | Index, if the gate spills into other areas | 54.83 | 57.4 (55.0-59.0) | 59.51 |

   - Chance that auto mode matches Jev's knowledge area: **about 10-15%**.
4. **What this cannot do (honest limit):**
   - Fixing knowledge alone cannot win the index. The other four areas trail Jev by 1.15 index points.
   - To beat 59.51 with the other areas unchanged, knowledge would have to reach **74.6**, about 6 points above Jev.
   - MMLU (Jev 92.0) cannot be matched at 4B.
   - GPQA can only be matched with long, slow thinking.
5. **Tools add almost nothing to honest claims.**
   - Running CRUXEval's own code copies its answer key, which was made by running that same code. This is the same reason the chess engine is banned.
   - Both move to a "reference only" column.
   - A 4B-written maths program adds only about +1 on GSM8K.
   - So the "with tools" row is about the same as the pure row: knowledge **64.3**, index **57.4**.
6. **Cost and timing:**
   - **$0** on the free L4: about **20-55 L4-hours** and about **7-10 days** of agent work.
   - Optional: about $5-15 on a Modal H100 for the DI run, which needs GO.
   - The frozen C round-1 plan (A16) does not change.
7. **Speed:**
   - Fast mode is unchanged.
   - Routed items take **seconds** (L4: 10-20 s for a short answer, 35 s to over 2 min for thinking).
   - We have **not yet shown** that even fast mode beats Jev on speed with our L4 numbers (see section 1).

## 1. Facts this plan rests on (checked)

### How the index is built

- **The DI v0.1 knowledge area has 6 benchmarks with equal weight.** These are MMLU, GPQA Diamond, GSM8K, ChessBench, CRUXEval and CLadder.
  - `check_index_math.json` has `"n": 6`, and recomputing the harness math reproduces Jev's 59.51.
  - Check: C1 307.3/6 = 51.2, and Jev 413.3/6 = 68.9.
- So:
  - 1 point on one knowledge benchmark = 1/6 of an area point = **0.033 index points**.
  - The whole knowledge gap is 17.65 area points = **3.53 index points**, which is 75% of the 4.68 gap.
  - To beat Jev with nothing else changed, knowledge must reach **≥ 74.6** (297.55 − 222.91 = 74.64).
  - The other four areas trail by 5.76 area points = **1.15 index points**.
- **Correction to R_measure.** Its claim of "14 knowledge benchmarks / 142 missing points" does not hold for v0.1.
  - ARC-E, ARC-C, WinoGrande, HellaSwag, MuSR, SATA-Bench and SimpleBench are **display-only** in v0.1 (`in_index: false`).
  - They are still DI test items, so their test splits stay off-limits for dev.
- **DI's own rule** (README, Rules): "No prompt tuning … one fixed rendering for every benchmark. Per-benchmark prompts, few-shot examples or label-aware tricks are not part of the benchmark." This plan follows it. See section 3.

### Per-benchmark scores

C1 was scored on a 10K sample. Jev's numbers come from its full published v0.1 run.

| Benchmark | C1 | Jev | Gap | Index points if fully closed | C1 sample n | C1 standard error |
|---|---|---|---|---|---|---|
| GPQA Diamond | 39.8 | 78.6 | -38.8 | 1.29 | 196 | ±3.5 |
| GSM8K (4- and 10-option tracks) | 56.7 | 79.9 | -23.1 | 0.77 | 460 | ±2.3 |
| CRUXEval | 51.5 | 73.0 | -21.5 | 0.72 | 229 | ±3.3 |
| MMLU (subject-macro) | 82.5 | 92.0 | -9.5 | 0.32 | 230 | ±2.5 |
| CLadder | 65.1 | 72.6 | -7.6 | 0.25 | 229 | ±3.1 |
| ChessBench | 11.7 | 17.2 | -5.5 | 0.18 | 230 | ±2.1 |

### Noise and speed

- **Noise.** The knowledge area has a standard error of about **±1.2 points** (√48.7/6 = 1.16), which is about ±0.25 index points.
  - Gaps under about 6 points (ChessBench, and CLadder at the edge) are only about 2 standard errors.
- **Speed today.**
  - C1's DI median on knowledge items was **242-262 ms** for MMLU, GPQA, GSM8K, CRUXEval and CLadder, and **625 ms for ChessBench**.
  - This was measured on the L4, through the harness, with two reads per choice question. Elsewhere, BFCL was 750 ms and ToolRet about 8 s.
  - Jev's OpenRouter median is **168 ms including the network** (reported by R_skeptic, not re-checked here). Market notes give 70-500 ms end to end.
  - **So "faster than Jev" is not shown by our L4 numbers.** Claim speed only from a measurement on the target GPU with a comparable network path, and publish p50/p95.

## 2. Options, ranked

### Summary table

All gains are estimates, after the R_skeptic corrections.
- The knowledge area starts at 51.2 and the index at 54.83.
- Options 1, 3 and 4 overlap, so 3 and 4 are shown on top of 1.

| # | Option | Moves | Knowledge area gain | Index gain | Added latency (routed items only) | $ | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | **Gated think route** on the same 4B, adapter off, one generic prompt, learned gate | GPQA, GSM8K, CRUX, CLadder, MMLU | **+6.7 to +18.6 (mid +12.9)** | **+1.3 to +3.7 (mid +2.6)** | short answer: ~2-3.5 s on H100 / 10-20 s on L4; thinking at a 1K cap: 4-7 s on H100 / 35-40 s on L4; 4K cap: 16-27 s on H100 / over 2 min on L4 | $0 (free L4) | **Do first** |
| 2 | Forgetting check plus LoRA-scale probe (report-only) | MMLU, GPQA, fast mode | 0 to +2 (unknown) | 0 to +0.4 | 0 | $0 | **Do** (free diagnostic) |
| 3 | Run the item's own code in a sandbox | CRUXEval | +2.2 to +5.8 on top of #1 | +0.4 to +1.2 | 20-60 ms | $0 | **Reference only, no claims.** It copies the answer key |
| 4 | Program-of-thought: the 4B writes Python for numeric word problems, and we run it | GSM8K (about +1 over #1) | about +0.2 on top of #1 | about 0 | about the same as a short answer; 20-60 ms to run | $0 | **Optional, later.** Tools row only; it adds about nothing to claims |
| 5 | Self-distill: train the one-pass model on its own gold-checked thinking answers | fast-mode GPQA, MMLU, CLadder | +1 to +3 | +0.2 to +0.6 | 0 | 3-6 L4-hours plus a $10-30 LoRA round | **Later** (after C). Claude-written or program-made prompts only |
| 6 | Chess: one-pass fine-tune on Stockfish-labelled positions | ChessBench, 11.7 → unknown (18-30 is a guess) | +1 to +3 | +0.2 to +0.6 | 0 | labels free on CPU; train inside #5's round | **Later, optional** |
| 7 | CLadder: parse the question to a causal query, then solve it with a program | CLadder, 80-90 | +1.3 to +3 on top of #1 | +0.3 to +0.6 | 2-4 s on L4 | needs a parser training round | **Later, tools row** (must be a general tool, not a CLadder-only branch) |
| 8 | Retrieval (BM25 over Wikipedia) | MMLU (small) | +0.5 to +1.7 | +0.1 to +0.3 | 50-200 ms on every routed item | $0-3 | **Skip for now** |
| 9 | Chess engine as a tool | ChessBench, 60-95 | +8 to +14 | +1.6 to +2.8 | 100-300 ms | $0 | **Reference only, no claims.** It copies the answer key |
| 10 | Reinforcement learning (GRPO) or fact-injection LoRA | none | ~0 to +1 | ~0 | none | $40+ | **Skip** |

**Forbidden by the owner rules, so excluded:**
- distilling from bigger models;
- reward-model search with 7-72B verifiers (the "1B beats 405B" style);
- training on Jev outputs;
- non-commercial data, or data written by bigger models. This covers SciQ, Cosmopedia and NuminaMath solutions, and also MMLU-Pro and SuperGPQA **as training data**: MMLU-Pro has GPT-4-written distractors, and SuperGPQA was built with LLM screening;
- FineWeb-Edu without an owner ruling, because its quality filter was trained on labels from a 70B model.

### Fit with the owner rules

| Rule | #1 | #2 | #3 / #9 | #4 / #7 | #5 / #6 | #8 |
|---|---|---|---|---|---|---|
| Model stays Qwen3.5-4B | yes | yes | no: the program decides, not the 4B | yes (the 4B writes the program) | yes | yes |
| No teacher bigger than 4B | yes (same model) | yes | n/a | yes | yes (same 4B; Stockfish is a program) | yes |
| No Jev outputs | yes | yes | yes | yes | yes | yes |
| Commercial-licence data only | yes (dev sets: section 4) | yes | Stockfish GPL-3: never ship it inside the on-prem package | CLadder generator MIT | Lichess CC0; Claude-written or program-made prompts only | Wikipedia CC BY-SA (attribution and share-alike duties) |
| Never tune on DI / OHS-3 / ejs-5 | yes (gate fit on dev only; "DI-informed design" label) | yes | n/a (no claims) | yes | yes (chess: exclude all March 2023 Lichess games) | yes, but needs a counts-only dedup against the DI |
| Speed stays a selling point | yes (opt-in auto, fast default) | yes | n/a | yes | yes (one-pass) | partly (+50-200 ms) |
| Small budget | $0 | $0 | $0 | $0 | $15-35 later, needs GO | $0-3 |

### Option 1: gated think route (recommended core)

**What.** The same Qwen3.5-4B, with our LoRA switched off, thinks before answering, but only on the items the gate picks.

**How it works.**
- **Tier 1 (every item):** C1 one-pass, unchanged and bit-identical.
- **Gate:** generic signals only, with no per-benchmark branches (details in section 3).
- **Two effort levels.** Each uses **one generic prompt** for every item it gets:
  - *Short:* base model, thinking off, a worked answer of up to 512 tokens.
  - *Long:* base model, thinking on, capped at B tokens, with B from {1K, 2K, 4K} chosen on dev. When the cap is hit, insert Qwen's stop-thinking text (Qwen3 report §4.7), then read the answer.
  - The learned gate picks the level from predicted gain and latency. Content type never picks it.
- **Readout:** read option probabilities using **od_engine's own option labels**, not an A-Z assumption.
- **Accept rule:** use the routed answer when its confidence is at least kappa. Otherwise blend it with C1's answer.
- **Fallback:** on a crash or an unmappable answer, return C1's answer.
  - The cap is defined in **tokens**. A wall-clock timeout exists only as a crash guard, and fallback counts are reported.
  - Nothing is ever left unanswered, because the DI scores unanswered items as zero.

**Why the base model.**
- The base model's thinking stays untouched by our fine-tuning.
- It can be served as a plain model. This avoids the vLLM bug where a Qwen3.5 LoRA loads without any error and then does nothing (whileai-sdk issue #588; vllm issue #36478).
- It works with whatever adapter C ships. Only the gate is refit.

**Evidence.**
- **Thinking vs no thinking (Qwen3 tech report, https://arxiv.org/abs/2505.09388, Tables 17-18):**

  | Qwen3-4B | No thinking | Thinking |
  |---|---|---|
  | GPQA Diamond | 41.7 | 55.9 |
  | MMLU-Redux | 77.3 | 83.7 |

- **Qwen3.5-4B card, thinking mode:** GPQA Diamond 76.2, MMLU-Redux 88.8, MMLU-Pro 79.1.
  - These are **full-budget, sampled** numbers: 32,768 output tokens (81,920 for hard queries), temperature 1.0, presence_penalty 1.5.
  - The card gives no non-thinking scores.
- **Where chain-of-thought helps (Sprague et al., https://arxiv.org/abs/2409.12183):**
  - +12.3 on math, +14.2 on symbolic tasks, +0.7 on everything else.
  - On MMLU, the gain sits almost entirely on questions that contain "=".
  - GSM8K gains reach up to +66.9 for some models. That is the largest gain, not a typical one. The often-quoted "Llama-3.1-8B 20.1 → 86.4" could **not be verified**.
- **Gating on the same base model (litjev, https://github.com/zhengxuyu/litjev/pull/12; Apache-2.0, not Jev-affiliated):** Qwen3.5-4B on 346 MMLU-Pro questions.

  | Setup | Accuracy | Thinking tokens per question |
  |---|---|---|
  | Fast path only | 54.0 | 0 |
  | Always think (about a 1K cap) | 74.0 | 994 |
  | Gated by a learned probe (thinks on 53% of items) | 71.7 | 526 |

  - At about a 1K cap, the model loses **about 5 points** against the card (74.0 vs 79.1).
  - A 512-token budget truncates 98.5% of the thinking traces.
  - This is one unreviewed repo, so read it as a direction, not proof.
- **Routing keeps most of the gain, but only with learned routers:**
  - Thinkless (https://arxiv.org/abs/2505.13379): an RL-trained router on R1-Distill-1.5B, math only. It thinks on 25.9% of items and scores 0.946, vs 0.958 when always thinking.
  - Self-Route (https://arxiv.org/abs/2505.20664): a hidden-state probe, with under 2% accuracy loss and 30-55% fewer tokens.
  - None of these tests a confidence-margin-only gate. That is why this plan uses a learned probe.

**Projected per-benchmark effect (estimates, corrected):**

| Benchmark | C1 | Auto, pure 4B | Basis |
|---|---|---|---|
| GPQA Diamond | 39.8 | **45-68 (mid 57)** | 76.2 is a full-budget number. A 1K cap cost about 5 points on MMLU-Pro (litjev), and GPQA needs longer reasoning. The ≤1.5K average-token budget pushes toward short caps, and with no thinking it is 41.7 (Qwen3-4B). Qwen3-4B-Thinking-2507 scores 65.8 at 32K. |
| GSM8K | 56.7 | **82-92 (mid 88), medium confidence** | Qwen3-4B-Base with 4-shot chain-of-thought: 87.8 (a different checkpoint and setup). Qwen3.5-4B with no thinking: unknown |
| CRUXEval | 51.5 | **65-82 (mid 73)** | Qwen2.5-Coder-7B-Instruct with chain-of-thought: 65.9 (3B: 56.0). Qwen3.5-4B with thinking: unknown |
| CLadder | 65.1 | **62-78 (mid 70)** | CDCR-SFT paper: Llama-3.1-8B CoT-SC 72.88, R1-Distill-Llama-8B 74.29, Mistral-7B 59.60, all with several samples. A single-sample 4B is likely lower |
| MMLU | 82.5 | **82-87.5 (mid 85)** | Redux with thinking: 88.8 at full budget. A cut-off thinking answer can be worse than C1's. The remaining gap is capacity, plus MMLU label noise |
| ChessBench | 11.7 | 11.7 | Not routed: the items have more than 10 options (see the section 3 limits) |
| **Knowledge area** | 51.2 | **64.1 (58.0-69.9)** | |
| **Index** (other areas unchanged) | 54.83 | **57.4 (56.2-58.6)** | |

**Risks.**
1. **Accuracy under a token cap is the biggest unknown.** Measure caps of 1K, 2K and 4K on dev before projecting further.
2. **Gate misses.** C1 can be confidently wrong, which a margin cannot see. A learned probe catches part of this.
3. **A cut-off thinking answer can be worse than the one-pass answer.** Hence the kappa accept/blend rule.
4. **Spill-over into other areas.** A gate that cannot see the benchmark name will also route low-margin items outside knowledge. Examples: iSarcasm, ContractNLI, BFCL, cfcolor, and the per-candidate yes/no relevance reads in ToolRet and BRIGHT (about 7.4K reads each in the sample). On BFCL, ContractNLI and cfcolor, our LoRA is the reason C1 wins, and the route switches it off. Hence the generic limits, the K-Skip set and the all-areas row (sections 3 and 4).
5. **Speed.** A 4K cap takes 16-27 s on an H100 and over 2 min on the L4. So the default stays fast, and the slow route is opt-in (`effort=auto|deep`).
6. **Run-to-run variation.** Qwen's recommended thinking settings sample at temperature 1.0, so answers vary between runs. Fix the seeds, record the decoding settings in the DI `latency`/`provenance` fields, and run dev-confirm with 2 seeds.
7. **Serving stack.**
   - The DI engine today uses HF transformers. Without `flash-linear-attention` and `causal-conv1d`, Qwen3.5's Gated DeltaNet layers fall back to slow reference PyTorch code.
   - Neither vLLM nor SGLang implements Qwen's `thinking_budget`. It must be built as a two-pass splice or a logits processor.
   - HF `generate` has no presence_penalty.
   - Both stacks must fit in 24 GB on the L4.
   - Add 1-2 days for this work (Step 2).

### Option 2: forgetting check (free)

- **What.** Run each of the following one-pass on dev sets:
  - the base model;
  - C1;
  - C1 with the LoRA scaled to 0.5 and 0.75;
  - the base model with thinking, as a ceiling.

  Also log the KL divergence between base and C1 (RL's Razor, https://arxiv.org/abs/2509.04259).
- **Why.** If C1 lost knowledge relative to the base model, scaling the LoRA could recover some of it for free. R_training estimates at most about 2 points.
- **Rule.** This is **report-only for now.** Changing the scale would make a new model. That can only happen after C's verdict, under its own amendment, judged on dev and the sealed-suite guards.

### Options 3, 4 and 7: exact program tools

- **#3, running the item's own code (CRUXEval): reference only.**
  - DI's CRUXEval answers came from running the code (https://arxiv.org/abs/2401.03065). The wrong options are codellama-7b outputs, and chance is 0.370 (DI docs/suite.md).
  - Running that code reproduces the answer key, the same way Stockfish does for ChessBench. CRUXEval exists to test code reasoning *without* running the code.
  - It may appear only in the reference column, never in a claim.
- **The tools row allows only general tools the model drives itself.**
  - The model may call **one general Python tool on any item**. There is no hard-coded "if the state contains code, run it".
  - If the 4B uses that tool to run CRUXEval's own code, the executed score still counts as reference only. In the tools row, CRUXEval is counted at its pure-4B value.
- **#4, program-of-thought (GSM8K).**
  - The program's answer must match exactly one option. Otherwise use the routed think answer or C1.
  - Qwen2.5-Math scores about the same with step-by-step reasoning and with Python (7B: 95.2 vs 94.6; 1.5B: 84.8 vs 83.7; https://arxiv.org/abs/2409.12122). So the gain is about +1 on GSM8K.
  - The real advantages are exact arithmetic and shorter outputs.
- **#7, CLadder solver.** It is allowed only as part of the same general tool, never as a CLadder-only branch.
- **Sandbox.** Code from the item and code the 4B writes are both untrusted:
  - never run it inside the main process;
  - use nsjail or bubblewrap, with no network and a read-only empty file system;
  - set a 2 s CPU limit, 256-512 MB of memory, no new processes and an output cap;
  - start a fresh worker after every call;
  - expect about 20-60 ms per call.
  - nsjail and bubblewrap need Linux user namespaces, which are often unavailable on Modal (gVisor) and on locked-down customer hosts. Check before relying on them. If they are unavailable, the tools row is off on that host.
- **Fairness.**
  - Jev's CRUXEval score of 73.0 suggests it runs no code (inference).
  - Any tools row is a separate disclosed row. Only the pure-4B row can say "beats Jev" without a qualifier.

### Options 5, 6 and 8-10 in brief

- **#5 Self-distillation (later).**
  - Sample the base model about 4 times with thinking on. Keep the rows whose majority answer matches gold. Train the one-pass head on the vote shares.
  - **Prompts come only from Claude-written or program-made items** (K-Math, K-Code and K-Causal style). MMLU-Pro and SuperGPQA stay evaluation-only.
  - The evidence is mixed. Compressing chain-of-thought into one pass failed for Phi-3 on GSM8K (0.28 → 0.31, vs 0.74 with chain-of-thought), but Mistral-7B went 0.38 → 0.51 with the same method (https://arxiv.org/abs/2405.14838). Expect about +1 to +3 on the knowledge area, which is unmeasured.
  - This is a training round. It must wait for C's verdicts and needs its own amendment.
- **#6 Chess fine-tune (later).**
  - Labels come from Stockfish 16 at 50 ms on Lichess CC0 positions.
  - **Exclude all March 2023 Lichess games.** DI's ChessBench test set is 11K games from that month. Also dedup against the test FENs.
  - Evidence is weak:
    - DeepMind's "56-63% best-move with about 10M games" could **not be verified**. The paper's full-data table reports puzzle accuracy and Elo, and gives action accuracy only in its 1M-game ablations (https://arxiv.org/abs/2402.04494).
    - The "7-8B LMs reach 25-30%" figure is **puzzle accuracy** from models trained on OpenAI o3 traces (https://arxiv.org/abs/2507.00726), so it is the wrong metric and a banned method.
  - Any later DI ChessBench result must be labelled "trained against the key's labeller".
- **#8 Retrieval (skip).**
  - Published MMLU gains for 4-8B models are +2 to +4, and they shrink as the model gets stronger. Qwen3-4B with MassiveDS goes 66.0 → 68.9, from a weak no-retrieval baseline (https://arxiv.org/html/2507.20059v1).
  - GPQA is "Google-proof": GPT-4 scores 38.8 on Diamond with and without search (https://arxiv.org/abs/2311.12022).
  - Expect +0 to +2, plus 50-200 ms of latency. A Wikipedia datastore also brings CC BY-SA duties.
- **#9 Chess engine (reference only).** DI's answer key is Stockfish 16's best move at 50 ms, so the engine copies the key. Never use it in the headline, and never ship Stockfish (GPL-3) inside the on-prem package.
- **#10 Reinforcement learning or fact LoRA (skip).**
  - The Qwen3 report says general RL "do[es] not bring significant improvements" on knowledge.
  - A LoRA can hold under 1% of the base model's fact capacity (Physics of LMs 3.3).
  - New facts are learned slowly and raise hallucination (https://arxiv.org/abs/2405.05904).
  - The earlier "General-Reasoner 4B GPQA 42.9" argument is dropped. That run started from Qwen3-4B-*Base*, so the comparison was unfair.

## 3. Best combined plan: "fast by default, think when it pays"

```
request ──> Tier 1: C1 one-pass (unchanged; DI median 242-262 ms on L4, ChessBench 625 ms)
              │  effort=fast (default) → return C1 answer
              │  effort=auto:
              ▼
           Generic limits (published; never read task/benchmark/catalog fields):
              - single-answer choice item, ≤ 10 options
              - not a per-candidate score/relevance request (if the request type says so)
              - otherwise → C1 answer
              ▼
           Learned gate: C1 top-2 margin (normalized by option count)
                         + small probe on C1's hidden state
                         (litjev style: one layer, PCA-64, small MLP, CPU-trained)
              ├─ predicts no gain           → C1 answer
              ├─ predicts gain, short level → base 4B, thinking off, ≤512 tokens, ONE generic prompt
              └─ predicts gain, long level  → base 4B, thinking on, cap B tokens, ONE generic prompt
           Readout with od_engine's option labels. Accept if confidence ≥ kappa, else blend with C1.
           Crash or unmappable → C1 answer. Cap in tokens; wall clock = crash guard only.
           Margin threshold, probe, B, kappa: fit on dev-fit only, then frozen in A17.1.
           Tools row only: one general Python tool the model may call on any routed item.
```

- **No option-pattern heuristics.** DI's GSM8K distractors put the right answer at the centre of a ±1/2/5/10, ×2, ×10, //2 pattern. Any rule that picks the "middle" option is a label-aware trick, and A17 bans it. A test checks this (section 4).
- **The gate's feature list is published** with the results.

### Projected DI v0.1 per area

All values are estimates.
- The other areas are shown at C1's values, with an unmeasured spill-over range of −1.5 to +0.5 area points each. That range assumes the generic limits and the K-Skip guard work.
- C round 1 may change the other areas, and that is not counted here.

| Area | Jev | C1 fast (now) | **Auto, pure 4B** | Auto + model-driven tools (disclosed) | Reference only: + item-code execution + chess engine |
|---|---|---|---|---|---|
| Knowledge | 68.88 | 51.23 | **64.1 (58.0-69.9)** | 64.3 (58.1-70.0) | 79.8 (71.2-86.8) |
| Language | 62.28 | 60.49 | 60.49 (−1.5 to +0.5) | same | same |
| Retrieval | 37.01 | 34.16 | 34.16 (−1.5 to +0.5) | same | same |
| Tools | 73.43 | 73.38 | 73.38 (−1.5 to +0.5) | same | same |
| Arts | 55.95 | 54.88 | 54.88 (−1.5 to +0.5) | same | same |
| **Index, other areas unchanged** | **59.51** | **54.83** | **57.4 (56.2-58.6)** | **57.4 (56.2-58.6)** | 60.5 (58.8-62.0) |
| Index, with spill-over range | | | 57.4 (55.0-59.0) | 57.4 (55.0-59.0) | 60.5 (57.6-62.4) |
| Share of the 4.68 index gap closed | | 0% | 55% (29-80%) | 56% (29-80%) | above Jev at mid |

### Projected per benchmark

| Benchmark | Jev | C1 | Auto, pure | Auto + model-driven tools | Reference only |
|---|---|---|---|---|---|
| MMLU | 92.0 | 82.5 | 85 (82-87.5) | same | same |
| GPQA Diamond | 78.6 | 39.8 | 57 (45-68) | same | same |
| GSM8K | 79.9 | 56.7 | **88 (82-92)** | **89 (83-93)** | same as tools |
| CRUXEval | 73.0 | 51.5 | 73 (65-82) | 73 (no execution credit) | 98 (95-99.5) with execution |
| CLadder | 72.6 | 65.1 | 70 (62-78) | same (80-90 with #7 later, unmeasured) | same |
| ChessBench | 17.2 | 11.7 | 11.7 (not routed) | same | 60-95 with the engine |

### Reporting rules

- Publish **two DI columns, fast and auto-pure**. A tools column is added only if #4 or #7 is built. The reference column is a paper projection and is never run as a claim.
- Label the auto columns **"DI-informed design"**. The DI's per-benchmark gaps shaped which dev sets were built (see section 4).
- With each column, publish:
  - the share of items routed, per area;
  - the fallback count;
  - p50/p95 latency per effort level;
  - the decoding settings and seeds.
- **Speed claims:** fast mode only, and only from a measurement on the target GPU with a comparable network path. Auto mode on routed items takes seconds.

## 4. Clean validation sets and protocol (pre-registered)

**Rules.**
- Never use any DI test item. That includes the display-only benchmarks: ARC test, HellaSwag val, WinoGrande dev, MuSR, SATA-Bench and SimpleBench.
- Never use OHS-1/2/3, ejs-5, JevBench, the sealed suite or LongBench.
- Use only data whose licence allows commercial use.
- **DI-adjacent splits are for evaluation only, never training**, and only with an owner ruling. Their DI scores are disclosed as "dev-tuned on adjacent split". The C spec already treats GSM8K as DI-adjacent.

| Set | Stands in for | Size | Licence | Role |
|---|---|---|---|---|
| **K-Math**: Claude-written word problems, answers computed by a program, 4- and 10-option versions. Wrong options use a recipe different from DI's (the right answer is not centred) | GSM8K | 2,000 | ours | primary (clean) |
| **K-Code**: Claude-written short Python functions, answers from execution, mutated wrong options. Dedup against all 800 CRUXEval items | CRUXEval | 1,500 | ours | primary (clean) |
| **K-Causal**: CLadder generator with new seeds plus new Claude-written stories, one story template held out. Template-aware dedup against all 10,112 released items (see below) | CLadder | 2,000 | MIT | primary; adjacent (owner ruling) |
| **K-Sci**: SuperGPQA sample (hard and middle science), **subsampled to 4 options** (gold + 3 distractors, fixed seed) to match GPQA | GPQA | 2,000 | ODC-BY (attribution) | paired comparisons only (Qwen reports SuperGPQA 52.9, so it is likely seen) |
| **K-Sci-2**: MMLU-Pro, non-MMLU parts only (drop the 6,810 items taken from MMLU test). 10 options | GPQA / MMLU | 2,000 | MIT | paired comparisons only (Qwen reports MMLU-Pro 79.1) |
| **K-MMLU**: MMLU validation + dev, scored per subject | MMLU | 1,816 | MIT | paired, no-harm guard; adjacent |
| **K-ARC**: ARC-C and ARC-E, train + dev splits only | MMLU / ARC | ~4,200 | CC-BY-SA-4.0 | paired, no-harm guard |
| **K-Skip**: items where a low margin does **not** mean thinking helps. Covers our certified internal dev sets for tool calls, NLI, retrieval relevance and style (files listed in A17), plus ~1,000 Claude-written sarcasm items (labels = author intent) | other-area spill-over | ~3,000 | ours | guard; teaches the gate to skip |
| **Product-mix dev**: certified internal dev sets (files listed in A17) | everyday traffic | existing | ours | guard; routing share |
| **K-Chess** (only if #6 is chosen): Lichess positions excluding all March 2023 games, Stockfish 16 at 50 ms. Dedup against ChessBench test | ChessBench | 2,000 | CC0 | adjacent (owner ruling) |

- Chess and chord (POP909-style) items need no skip set, because the generic ≤10-option limit already keeps them out of routing.
- **Certify every internal file.** A17 lists each internal file the gate is fit on and certifies that it contains no Jev-labelled rows, JevBench, OHS-1/2/3, ejs-5 or sealed-suite items. Fitting the gate counts as tuning.
- **Do not use:**
  - MMLU-Redux, MMMLU, GSM-Plus, GSM-Hard, GSM-Symbolic, MGSM or CRUXEval-X (all derived from DI test sets);
  - SciQ (non-commercial);
  - OpenBookQA, PIQA or TriviaQA (licence listed as "unknown");
  - GPQA extended minus Diamond, unless the owner rules otherwise (same pool as Diamond).
- **Decontamination (counts only).** Compare against the **public full test sets**, so the existing quarantine never needs opening:
  - MMLU test, all 546 GPQA items, GSM8K test, CRUXEval 800, CLadder 10,112, ChessBench test, ARC test, HellaSwag val, WinoGrande dev, MuSR and SATA-Bench.
  - Keep these downloaded copies in a **new git-ignored quarantine-style folder**. Only the counts-only tool touches them, never where builders or agents read dev data. GPQA's authors ask that its items not be posted in plain text.
  - Drop a candidate on an exact match after normalizing the text, a shared 13-word sequence, or embedding similarity ≥ 0.92.
  - **For K-Causal:** ignore n-grams that appear in more than 20 released items, as the DI overlap tool already does. Then dedup on the (graph, query type, numbers, story) tuple. Otherwise the template sentences would drop almost every generated item.
  - Then run the existing counts-only n-gram tool (A16(a)) against OHS-1/2/3, ejs-5, JevBench and the sealed exports. Log the drop counts.
- **Leakage note.** Qwen3.5 has probably seen MMLU val, ARC, GSM8K train, SuperGPQA and MMLU-Pro. Use those only to compare two versions of our system. The program-made sets (K-Math, K-Code, K-Causal) are the only clean absolute measures.
- **Splits.** Each set is split 60/40 into **dev-fit** and **dev-confirm**. Both sha256 hashes are frozen in the amendment before any model reads them.
- **Protocol** (draft amendment **A17**, written before any measurement):
  1. **Fixed candidates:**
     - caps B ∈ {1K, 2K, 4K} tokens;
     - margin thresholds on a fixed grid;
     - the probe architecture fixed in advance;
     - acceptance threshold kappa on a fixed grid.
  2. **Fit on dev-fit only.**
     - The objective is macro accuracy over the reasoning sets, with **equal weight per set, pre-registered**.
     - Constraints:
       - at most **10% routed** on product-mix dev;
       - an average of ≤ 1.5K added tokens per routed item;
       - a K-Skip routing share at a pre-registered limit.
  3. **Confirm once on dev-confirm, with 2 fixed seeds.** Ship auto mode only if all of these hold on both seeds (paired bootstrap):
     - **Per-set rule:** each reasoning set (K-Math, K-Code, K-Causal, K-Sci, K-Sci-2) has a gain LB ≥ 0 vs C1, and the macro gain is ≥ **+5**.
     - **Long-thinking level:** it ships only if K-Sci gains **≥ +5 with LB > 0** at the chosen cap. Otherwise that level is switched off and auto ships with the short level only.
     - **No-harm guard:** pooled K-MMLU + K-ARC (about 2,400 items; paired SE about 0.6) has LB > −1.0.
     - **Product-mix and K-Skip:** LB > −0.5 each, with power recomputed on the real dev-confirm sizes and frozen before the run.
     - **p95 latency** per effort level is under the pre-registered limits, measured on the L4.
     - Unrouted outputs are bit-identical to C1, and nothing is left unanswered.
     - **Routing invariance:** blanking the task, benchmark and catalog fields leaves routing unchanged.
     - **Distractor test:** on DI-format synthetic items (K-Math style), accuracy does not change when the distractors are re-drawn off-centre.
  4. **DI run, report-only: exactly one look per shipped adapter.**
     - Same seed 20260919 and the same 10K sample. Columns: fast and auto-pure (plus tools, only if built).
     - The DI never changes a threshold afterwards. If the DI disagrees with dev, report it; do not retune.
  5. **Disclosure in A17.**
     - The owner saw the DI per-benchmark gaps, and that is why this direction was researched and why the reasoning dev sets mirror GSM8K, CRUXEval and CLadder.
     - Thresholds, caps and the probe are chosen only on dev.
     - The auto columns therefore carry the label **"DI-informed design"**. They do **not** fully keep A13's "DI never chooses" rule.
- **Power.**
  - Dev-confirm is 40% of each set: about 800 items per reasoning set and 726 for K-MMLU.
  - With about 8% of answers changed, the paired SE is about 1.05 points on K-MMLU alone. On that set alone, a guard of "LB > −0.5" would need a mean gain of about +1.6. That is why the guard is pooled with K-ARC.
  - GPQA Diamond's 196 items carry about ±3.5, so any "matched Jev on GPQA" claim needs a margin of about ±7.

## 5. What can and cannot beat Jev at 4B (honest)

| Target | Fast mode (one pass) | Auto, pure 4B | Auto + model-driven tools |
|---|---|---|---|
| GSM8K (79.9) | no (one-pass ceiling ~55-65) | **yes, medium confidence (82-92)** | yes |
| CRUXEval (73.0) | no | **tie at best** (65-82) | same; executing the item's code is reference only |
| CLadder (72.6) | no | **tie at best** (62-78, mid 70) | maybe with #7 (later, unmeasured) |
| GPQA Diamond (78.6) | no | **no at short caps** (45-68). A tie needs long thinking: 76.2 at a 32K+ budget, minutes per item | same |
| MMLU (92.0) | no | **no** (82-87.5). The best 4B result measured is 88.8 on the cleaner Redux, at full budget; the rest is capacity | no |
| ChessBench (17.2) | maybe with #6 (unknown; 18-30 is a guess) | same (not routed) | the engine copies the key, so it does not count |
| Knowledge area (68.9) | no (~52-55 even with #2, #5, #6) | **unlikely** (58-70; about 10-15%) | **unlikely** (58-70; under 15%) |
| DI index (59.51) | no | **no on knowledge alone** (56.2-58.6) | no (56.2-58.6) |
| Speed vs Jev | not yet shown on L4 (242-262 ms vs Jev's 168 ms p50); measure on the target GPU | **no** on routed items (seconds) | no |

**Bottom line.**
- With thinking, a 4B can clearly beat Jev on **GSM8K**, and roughly tie it on **CRUXEval and CLadder**.
- It cannot match Jev's **stored-fact** breadth (MMLU), and it cannot match GPQA quickly.
- Realistically, auto mode closes **about half** of the index gap (55%, range 29-80%).
- Beating Jev's **index** also needs about 1.15 index points from the other four areas. Candidates are a general music tool for POP909 (+0.9 to +2.1, tools row, R_tools) and the language and retrieval gaps. Those are outside this plan.

## 6. Build plan (does not disturb A16)

**Not touched:**
- `train_decoder.py`, `decoder_io.py`, `runs/q35_4b_c_r1.json`;
- any C data, replay draw, deny-list, gate or seed;
- the pinned `bench/decision_index/od_engine.py`.

**Rules for this work:**
- All new code lives in new files: `lean/route/` and `bench/decision_index/od_engine_auto.py`.
- The L4 is shared with C's G9 crowd scoring, and **G9 always goes first**.
- The route uses the plain base model, so it works with whatever adapter C ships.
- There is no training in Steps 0-7.

| Step | What | Time | $ | Machine | GO needed? |
|---|---|---|---|---|---|
| 0 | Owner rulings (section 7) and the A17 draft committed. A17 includes the DI rule quote, the "DI-informed design" label, the ban on option-pattern heuristics, the certified file list and the one-look rule | 0.5 day | 0 | laptop | owner OK on A17 |
| 1 | Build dev sets: K-Math, K-Code, K-Causal, K-Sci (4-option), K-Sci-2, K-MMLU, K-ARC, K-Skip (and K-Chess only if #6). Set up the git-ignored decontamination folder, decontaminate, split, freeze sha256 | 1.5-2 days | 0 | laptop CPU | no |
| 2 | **Serving stack:** vLLM or SGLang with Qwen3.5 kernels, the stop-thinking splice, presence_penalty, both models in 24 GB, and a parity test against HF tier 1. **Route code:** generic limits, probe, two effort levels, readout with od_engine labels, blend, fallback. **Tests:** CPU tests with a fake model, routing invariance, the distractor re-draw test, and parity (tier 1 == `decoder_io.predict`). Also check whether C1's DI run saved per-item probabilities for reuse | 2-4 days | 0 | laptop + L4 VM | no |
| 3 | Dev-fit measurement: C1, base one-pass, LoRA 0.5/0.75 (#2), the short level, and the long level at a 4K cap. The 1K and 2K results come from cutting the 4K trace and re-reading, so the long run happens once. About **26-36M generated tokens**. Halve this by running the long level on a fixed ~4K-item subsample | ~6-12 L4-hours with vLLM batching (throughput unmeasured; several times longer on HF) | 0 (free credit); or ~$5-8 on a Modal H100 | L4 | no on L4; GO if Modal |
| 4 | Fit the margin threshold, probe, B and kappa on dev-fit only, then freeze them in A17.1 | 0.5 day | 0 | laptop (probe trains on CPU) | no |
| 5 | Dev-confirm once, with 2 seeds, against the ship rule | ~4-6 L4-hours | 0 | L4 | no |
| 6 | Optional speed check: p50/p95 per effort level on an H100, bf16 vs FP8, and fast mode vs Jev on a comparable path | 1 hour | ~$1-2 | Modal | **yes** |
| 7 | DI report-only run, the single look for C1: fast (reused from C1's run) and auto-pure. The harness runs one request at a time, so routed knowledge items alone are about 0.85-2.4M tokens. Add other-area items the gate routes | **~8-27 L4-hours** if tier-1 outputs are reused; ~14-36 if not; +2-5 for a tools column | 0; or ~$5-15 on a Modal H100 | L4 | owner OK (new DI look under A17); GO if Modal |
| 8 | After C ships: refit the margin threshold and probe on dev-fit for the shipped adapter, re-confirm, then **one** pre-registered DI look for that adapter (mandatory, not optional) | ~15-40 L4-hours | 0 | L4 | owner OK |
| 9 | Later, separate amendment, after the C round-1 (and round-2) verdicts: fast-mode training (#5 self-distill with Claude-written or program-made prompts only, plus #6 chess and #7 parser if chosen). Same gate style as C recipe 6.2-6.4, with no-regression guards on the sealed suite | ~1 week | ~$15-35 | L4 + Modal | **yes** |

**Totals.**
- Steps 0-7: about **7-10 days** of work and about **20-55 free L4-hours**, at **$0**.
- Instead of the free L4, Steps 3 and 7 could run on Modal for about $10-25, which needs GO.
- Step 9 comes later and costs about $15-35.
- None of this uses C's $30 round-1 budget.

## 7. Owner decisions needed

1. Add a "K-route" step to the goal flow, after the C round-1 steps it runs beside.
2. **Tools policy.**
   - Executing the item's own code (CRUXEval) and the chess engine: **reference only, never in claims**? (Recommended: yes.)
   - Model-driven Python tool (#4, #7): build now, or later? (Recommended: later. It adds about +0.2 to the knowledge area.)
3. **DI-adjacent dev splits** (MMLU val/dev, CLadder generator; Lichess with Stockfish only if #6): allowed for **evaluation only**?
4. Approve A17, including:
   - the "DI-informed design" label;
   - one DI look per shipped adapter (Steps 7 and 8);
   - the certified internal file list.
5. Product surface: is it acceptable that `effort=auto` takes seconds on routed items, with fast mode as the default?

## 8. Key unknowns (measure on dev, never on DI)

- Qwen3.5-4B accuracy at 1-4K thinking caps, and with thinking off.
- Qwen3.5-4B on GSM8K, CRUXEval and CLadder.
- How much C1 forgot relative to the base model.
- How well the probe catches items C1 gets confidently wrong, and how much it spills into other areas.
- Whether the DI renders retrieval items as score requests that the generic limits can skip.
- Real vLLM/SGLang throughput for Qwen3.5 on the L4, and real latency per effort level on the L4 and the H100.
- Whether C1's DI run saved per-item probabilities that tier 1 can reuse.
- Whether sandboxes work on Modal and on customer hosts (only matters for a tools row).
- Jev's size, and whether it uses retrieval or tools. Its CRUXEval and ChessBench scores suggest no code runner and no chess engine.

## Corrections log (from R_skeptic.md)

**Accepted:**
1. Corrected projection: MMLU 85 (82-87.5), GPQA 57 (45-68), GSM8K 88 (82-92, medium confidence), CLadder 70 (62-78). This gives knowledge 64.1 (58.0-69.9) and index 57.4 (56.2-58.6). The match chance is about 10-15%.
2. Executing CRUXEval's own code moves to the reference-only column with the chess engine. The tools row drops to about 64.3 / 57.4, with a match chance under 15%.
3. The format-shaped gate branches are replaced by one generic think prompt, a learned probe and one general Python tool. The DI "No prompt tuning" rule is cited.
4. "DI-informed design" label. The claim that A13 is kept is withdrawn. The DI gets one look per shipped adapter, and the "optional" re-run is dropped.
5. Spill-over into other areas: an all-areas row with ranges, generic routing limits and the K-Skip guard set.
6. Readout uses od_engine's option labels, and only items with ≤10 options are routed (stricter than the suggested ≤26).
7. Costs:
   - Step 7 runs one request at a time (8-27 L4-hours per auto column, with tier 1 reused);
   - Step 3 is 26-36M tokens;
   - the serving stack adds 1-2 days;
   - 2 seeds on dev-confirm;
   - the cap is in tokens, and the timeout is a crash guard only;
   - the sandbox takes 20-60 ms;
   - the short level takes 10-20 s on the L4.
8. Speed: "faster than Jev" is not shown on the L4. The median on knowledge items is 242-262 ms (ChessBench 625).
9. Rules and licences:
   - #5 uses only Claude-written or program-made prompts;
   - #6 excludes all March 2023 Lichess games and carries the "key's labeller" label;
   - the public test-set copies sit in a git-ignored folder;
   - internal files are certified;
   - Stockfish stays out of the product;
   - sandbox namespaces must be checked;
   - Wikipedia's CC BY-SA duties are noted.
10. Protocol:
    - per-set ship rules, plus a K-Sci ≥ +5 rule for the long level;
    - power recomputed on the 40% split;
    - template-aware K-Causal dedup;
    - 4-option K-Sci;
    - learned probe instead of a margin-only gate;
    - ban on option-pattern heuristics, with a distractor re-draw test;
    - K-Sci and K-Sci-2 used for paired comparisons only.
11. Citations:
    - chess 25-30% is puzzle accuracy from o3-trained models;
    - chess 56-63% is unverified;
    - Llama 20.1 → 86.4 is unverified (+66.9 is the largest gain);
    - CLadder 7-8B numbers do exist (with self-consistency);
    - the General-Reasoner argument is dropped;
    - Deng et al.'s Mistral 0.38 → 0.51 is added;
    - litjev's 1K cap costs about 5 points;
    - Thinkless and Self-Route use learned routers.

**Changed, not taken as written (with reason):**
1. *"Weight the dev mix by product traffic."* Changed. We have no measured product traffic distribution yet (pre-launch). The plan uses **pre-registered equal weights per dev set**, plus the product-mix and K-Skip guards and the "DI-informed design" label. Revisit when real traffic exists.
2. *"Expose tools as one general Python tool."* Accepted for the product. But a general tool would still run CRUXEval's own code. So for claims, CRUXEval is always counted at its pure-4B value, and the executed score goes to the reference column.
3. *"Budget 30-70 L4-hours for Step 7."* Kept as the upper bound for two auto columns with no reuse. The plan cuts it by design: run one auto column in the first look (tools only if built) and reuse C1's tier-1 outputs if they were saved. That gives 8-27 hours, or 14-36 without reuse.
4. *"Add skip sets for chess positions and chord labels."* Not needed. The generic ≤10-option limit already keeps ChessBench (up to about 151 options) and POP909 (about 120) out of routing. K-Skip covers only the ≤10-option types: sarcasm, NLI, tool calls and relevance. This also avoids building a Stockfish-adjacent set unless #6 is chosen.
5. *"K-Sci ≥ +5 as a condition for shipping all of auto mode."* Narrowed. Failing it switches off only the long-thinking level. The short level can still ship on its own per-set rules.
6. *"Jev's OpenRouter p50 is 168 ms."* Used as reported by R_skeptic, not re-verified here. The corrected speed rule does not depend on the exact number.

**Rejected outright:** none.

## Sources

- **Qwen model cards:**
  - Qwen3.5-4B: https://huggingface.co/Qwen/Qwen3.5-4B
  - Qwen3.5-2B: https://huggingface.co/Qwen/Qwen3.5-2B
  - Qwen3-4B-Instruct-2507: https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507
  - Qwen3-4B-Thinking-2507: https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507
- **Model reports:**
  - Qwen3 technical report: https://arxiv.org/abs/2505.09388 (Tables 7, 17, 18; §4.7 stop-thinking text)
  - Qwen2.5-Math: https://arxiv.org/abs/2409.12122
  - Qwen2.5-Coder: https://arxiv.org/abs/2409.12186
- **Benchmarks:**
  - Decision Index: https://github.com/flaviusburca/decision-index (pinned 52a6989: README Rules, docs/suite.md, decision_index/runner.py)
  - GPQA: https://arxiv.org/abs/2311.12022
  - CRUXEval: https://arxiv.org/abs/2401.03065
  - ChessBench: https://arxiv.org/abs/2402.04494
  - CLadder: https://arxiv.org/abs/2312.04350 and https://github.com/causalNLP/cladder
  - SuperGPQA: https://huggingface.co/datasets/m-a-p/SuperGPQA
  - MMLU-Pro: https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro
- **Thinking and routing:**
  - Sprague et al.: https://arxiv.org/abs/2409.12183
  - s1: https://arxiv.org/abs/2501.19393
  - Thinkless: https://arxiv.org/abs/2505.13379
  - Self-Route: https://arxiv.org/abs/2505.20664
  - SynapseRoute: https://arxiv.org/abs/2507.02822
  - NoThinking: https://arxiv.org/abs/2504.09858
  - litjev: https://github.com/zhengxuyu/litjev/pull/12
- **Training into one pass:**
  - Deng et al.: https://arxiv.org/abs/2405.14838
  - System 2 to System 1 distillation: https://arxiv.org/abs/2407.06023
- **Forgetting and new facts:**
  - RL's Razor: https://arxiv.org/abs/2509.04259
  - Gekhman et al.: https://arxiv.org/abs/2405.05904
  - General-Reasoner (Base start): https://github.com/TIGER-AI-Lab/General-Reasoner
- **Tools:**
  - CDCR-SFT: https://arxiv.org/abs/2508.12495
  - Program of Thoughts: https://arxiv.org/abs/2211.12588
  - LLM chess RL (puzzle accuracy, o3 traces): https://arxiv.org/abs/2507.00726
- **Retrieval:**
  - Retrieval gains by model size: https://arxiv.org/html/2507.20059v1
  - MassiveDS: https://arxiv.org/html/2407.12854v1
- **Serving:**
  - Thinking budget in local engines: https://zolotukhin.ai/blog/2026-05-18-qwen3-thinking-budget-local-engines-still-fake/
  - Qwen3.5 slow fallback without fla/causal-conv1d: https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/qwen3_5.md
  - vLLM LoRA issues: https://github.com/vllm-project/vllm/issues/36478 and https://github.com/whilehq/whileai-sdk/issues/588
- Full source lists are in R_testtime.md, R_retrieval.md, R_tools.md, R_training.md, R_measure.md and R_skeptic.md.
