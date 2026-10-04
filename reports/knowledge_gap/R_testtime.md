# R_testtime: test-time compute to close the 4B-vs-Jev knowledge gap

Researcher: testtime. Date: 3 Oct 2026. Web sources only, no local test data opened, no paid calls.

## TL;DR (simple)

1. **The gap is mostly "thinking", not "knowing."** The same Qwen3.5-4B we fine-tune scores **GPQA Diamond 76.2** when it is allowed to think (official card). C1 gets 39.8 one-pass and Jev gets 78.6. On GPQA, thinking-mode 4B already beats Qwen3-30B-A3B-Thinking-2507 (73.4). Reading-only C1 leaves most of that ability unused.
2. **Thinking does not help everything.** It gives big gains on math, code and science reasoning: GSM8K, GPQA, CRUXEval, CLadder. It gives about 0 to 1 point on pure recall, sarcasm and music (Sprague et al.: about 95% of CoT's MMLU gain comes from questions with an "=" sign). So the remaining MMLU gap (C1 82.5, Jev 92.0, 4B-thinking roughly 88-89) is about 3-4 points of real missing knowledge, and test-time compute cannot fix that part.
3. **Best design: a 3-tier "fast / short / deep" route on one resident 4B.**
   - Tier 1 is the current C1 one-pass readout (20-50 ms) for every item.
   - A free gate (C1's own letter-probability margin, plus a "math/code/science" tag, plus optionally a small probe on a layer about 60-75% deep) escalates only uncertain reasoning items.
   - Tier 2 is base Qwen3.5-4B with the adapter OFF, non-thinking, a short visible CoT of about 200-500 tokens. Use it for grade-school math and code tracing.
   - Tier 3 is base 4B with thinking ON and a capped budget of 1-4K tokens, using Qwen's built-in stop-thinking insert. Use it for GPQA-style items.
   - The answer is always read as letter logits after "Answer:", the same readout as C1.
4. **Closest real evidence (same base model):** litjev's open "System Two" on **Qwen3.5-4B / MMLU-Pro (n=346)** reports fast-only 54.0%, always-think 74.0% at 994 tokens per question, and a learned gate at **53% escalation giving 71.7% at 526 tokens per question**. That is 89% of the gain at 53% of the tokens.
5. **Latency cost is real.** About 1K thinking tokens takes roughly 4-7 s on an H100 and roughly 30-40 s on an L4 in bf16. These are my bandwidth estimates, not measurements. So the deep tier must be opt-in (`effort=auto|deep`), and the default stays one-pass so the speed claim survives.
6. **The LoRA adapter and base thinking can coexist on one copy of the weights.** Use PEFT `with model.disable_adapter():` for tiers 2-3. Do not let the decision-adapter training touch the thinking path. One trap: **vLLM's LoRA loading for Qwen3.5 can silently do nothing** (key-prefix mismatch, see below), so the adapter must be checked after every load.
7. **Expected effect (estimate; the DI cannot be used to tune it):** GSM8K 56.7 → about 85-93 (beats Jev's 79.9). GPQA-D 39.8 → about 60-74 with a capped budget (Jev 78.6). CRUXEval 51.5 → about 65-78 (unknown; Jev 73.0). MMLU 82.5 → about 85-88 (Jev 92.0). Little or no change on POP909, iSarcasm or ChessBench.

---

## 1. Official numbers: thinking vs non-thinking for Qwen 4B-class models

### 1a. Qwen3.5-4B (our base). Official card, thinking mode (the default)
Source: https://huggingface.co/Qwen/Qwen3.5-4B

| Benchmark | Qwen3.5-4B (think) | Qwen3.5-9B | Qwen3-30B-A3B-Thinking-2507 | GPT-OSS-20B | Jev (DI) | C1 one-pass (DI) |
|---|---|---|---|---|---|---|
| MMLU-Pro | 79.1 | 82.5 | 80.9 | 74.8 | – | – |
| MMLU-Redux | 88.8 | 91.1 | 91.4 | 87.8 | (MMLU 92.0) | (MMLU 82.5) |
| SuperGPQA | 52.9 | 58.2 | 56.8 | 48.5 | – | – |
| GPQA Diamond | **76.2** | 81.7 | 73.4 | 71.5 | **78.6** | **39.8** |
| LiveCodeBench v6 | 55.8 | 65.6 | 66.0 | 74.6 | – | – |
| HMMT Feb 25 | 74.0 | 83.2 | 63.1 | 76.7 | – | – |

- The card's settings: 32,768 output tokens for most queries and 81,920 for competition math and code. So these are **large-budget** numbers.
- Recommended thinking sampling: temp 1.0, top_p 0.95, top_k 20, presence_penalty 1.5.
- Thinking is on by default. Turn it off with `chat_template_kwargs={"enable_thinking": False}`.
- The card's language table has **no non-thinking numbers for the 4B**: unknown.
- GSM8K, MATH and CRUXEval are not reported for Qwen3.5-4B: unknown.

### 1b. Thinking deltas measured on siblings (official)

| Model (source) | Benchmark | Non-think | Think | Δ |
|---|---|---|---|---|
| Qwen3-4B (Qwen3 tech report T17/T18, https://arxiv.org/pdf/2505.09388) | MMLU-Redux | 77.3 | 83.7 | +6.4 |
| | GPQA-Diamond | 41.7 | 55.9 | **+14.2** |
| | C-Eval | 72.2 | 77.5 | +5.3 |
| | MATH-500 | 84.8 | 97.0 | +12.2 |
| | AIME'24 | 25.0 | 73.8 | +48.8 |
| | LiveCodeBench v5 | 21.3 | 54.2 | **+32.9** |
| | ZebraLogic | 35.2 | 81.0 | +45.8 |
| | BFCL v3 | 57.6 | 65.9 | +8.3 |
| Qwen3.5-2B (card, https://huggingface.co/Qwen/Qwen3.5-2B) | MMLU-Pro | 55.3 | 66.5 | +11.2 |
| | MMLU-Redux | 69.2 | 79.6 | +10.4 |
| | SuperGPQA | 30.4 | 37.5 | +7.1 |
| | C-Eval | 65.2 | 73.2 | +8.0 |
| Qwen3-4B-2507, Instruct vs Thinking models (https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507, https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507) | MMLU-Pro | 69.6 | 74.0 | +4.4 |
| | MMLU-Redux | 84.2 | 86.1 | +1.9 |
| | GPQA | 62.0 | 65.8 | +3.8 |
| | LiveCodeBench v6 | 35.1 | 55.2 | +20.1 |
| | AIME25 | 47.4 | 81.3 | +33.9 |

Base model with few-shot CoT (Qwen3 report Table 7): Qwen3-4B-Base GSM8K **87.79**, MATH 54.10, CRUX-O 55.00, GPQA 36.87, MMLU 72.99. So even the *base* 4B with plain CoT scores well above Jev's GSM8K 79.9.

**Caveat:** Qwen's "non-thinking" scores still let the model write visible reasoning before it answers. They are **not** the same as C1's zero-token one-pass readout. The real ladder is: one-pass (0 tokens) < non-thinking with a short visible CoT (a few hundred tokens) < thinking (1K to 30K+ tokens). This is why C1's GPQA 39.8 sits below even Qwen3-4B non-thinking (41.7) and Qwen3-4B-Instruct-2507 (62.0).

### 1c. Versus about 30B models
- **4B thinking vs a 30B model, both thinking.** Qwen3.5-4B is about equal to or better than Qwen3-30B-A3B-Thinking-2507 on GPQA (76.2 vs 73.4). It is behind on MMLU-Pro (79.1 vs 80.9), MMLU-Redux (88.8 vs 91.4), SuperGPQA (52.9 vs 56.8) and LiveCodeBench (55.8 vs 66.0). Qwen3-4B-Thinking-2507 ties Qwen3-30B-A3B thinking on GPQA (65.8 vs 65.8).
- **4B thinking vs a 30B model answering without thinking.** Qwen3-30B-A3B non-thinking scores GPQA 54.8, MMLU-Redux 84.1 and MATH-500 89.8 (Qwen3 report T16). 4B thinking beats all three (GPQA 76.2 for Qwen3.5-4B, MATH-500 97.0 for Qwen3-4B). Jev answers in 70-500 ms, so it is very unlikely to do long thinking. **This is the lever where a 4B can beat a ~30B: spend tokens only where reasoning, not memory, is the bottleneck.**
- **Where it does not close.** Pure recall breadth (MMLU, SuperGPQA) still trails by about 2-4 points even when both models think. That is parameter count, and test-time compute will not fix it.

## 2. Which DI gaps test-time compute can and cannot close

Evidence on *which tasks* benefit:
- **Sprague et al., "To CoT or not to CoT?" (ICLR 2025)**, https://arxiv.org/abs/2409.12183. This is a meta-analysis plus experiments. Average CoT gains: symbolic +14.2, math +12.3, logic +6.9. Commonsense, text classification and general knowledge gain under 1. On MMLU, **about 95% of CoT's gain comes from questions or outputs containing "="**, and direct answering matches CoT otherwise. Solvers or tools beat CoT on symbolic tasks.
- **CRUXEval paper** (Table 3), https://arxiv.org/abs/2401.03065. CoT on *output* prediction gives GPT-4 63.4 → 81.9 (+18.5) and GPT-3.5 50.0 → 63.3 (+13.3). Code Llama 13B gains only +0.9 and Code Llama 34B gains +4.9. Gains grow with model quality, and Qwen3.5-4B thinking reaches LCB v6 55.8, which is far above Code Llama.
- **"Thinking to Recall"** (Google, COLM 2026), https://research.google/blog/thinking-to-recall-how-reasoning-unlocks-parametric-knowledge-in-llms/ and https://arxiv.org/abs/2603.09906. Reasoning *does* unlock some closed-book facts through a "computational buffer" and "factual priming" (tested on Qwen3-32B and Gemini-2.5; the blog gives no exact numbers). However, a single hallucinated intermediate fact in the trace sharply lowers final accuracy. Another study, https://arxiv.org/abs/2602.22193, reports only +1.1 (TriviaQA) and +1.3 (NQ) from a "think step-by-step" cue on GPT-OSS-20B. **The recall gain is real but small.**
- **Thinking can hurt** on some tasks. Qwen3.5-0.8B IFEval drops from 52.1 to 44.0 with thinking (card). So routing per category must be decided on dev data.

Per-benchmark estimate. "Slow" means base 4B with thinking or short CoT. These are my estimates from the evidence above, and they must be re-measured on non-DI dev sets:

| DI benchmark | C1 | Jev | Expected with slow route | Why |
|---|---|---|---|---|
| GSM8K | 56.7 | 79.9 | **about 85-93** | 4B-Base few-shot CoT 87.79; one-pass mental arithmetic is the bottleneck; tier-2 short CoT is likely enough (AdaptThink: no-thinking is about equal to thinking on problems at high-school level and below) |
| GPQA Diamond | 39.8 | 78.6 | **about 60-74** (capped 2-4K budget) | 76.2 is the full-budget official number; capping costs some points (s1 and Qwen3 budget curves are monotone); exact capped value unknown |
| CRUXEval | 51.5 | 73.0 | **about 65-78 (unknown)** | output prediction gains most from CoT; no official 4B CRUXEval number |
| MMLU | 82.5 | 92.0 | **about 85-88** | the "=" questions gain; recall questions do not; 4B-thinking MMLU-Redux is 88.8 at full budget |
| CLadder | 65.1 | 72.6 | +2 to +6 (unknown) | causal and formal reasoning, between "logic" and "math" in Sprague's split |
| ChessBench | 11.7 | 17.2 | small or unknown | thinking without a board engine helps little at 4B |
| POP909-CL, iSarcasm | 8.5 / 44.4 | 16.6 / 50.5 | about 0 | not symbolic; do not route |

Index arithmetic (assumption-laden). The gains above add up to roughly +60 to +110 benchmark points, spread over the Knowledge area. If the Knowledge area averages about 10 equally weighted benchmarks, it rises by about 6 to 11 points (gap 17.7), and the 5-area index rises by about 1.2 to 2.2 (gap 4.68). That is under the "auto" effort setting only, and the effect depends on the DI repo's real area membership and weights.

## 3. Test-time methods: what each buys and costs

| Method | Evidence | Gain | Cost | Fit for us |
|---|---|---|---|---|
| **Thinking mode (built in)** | Qwen tables above | GPQA +14 (Qwen3-4B), LCB +33, MMLU-Redux +2 to +10 | 1K to 30K tokens | Core of tier 3 |
| **Budget cap / forcing** | s1 (https://arxiv.org/abs/2501.19393): 32B model, 1K SFT examples, budget forcing AIME24 50 → 57%. Qwen3 report §4.7: performance scales smoothly with budget. Qwen3 has a built-in truncation string: "Considering the limited time by the user, I have to give the solution based on the thinking directly now.\n</think>.\n\n" (emergent, not trained) | Lets us pick a point on the curve | Linear in the budget | Yes. Cap at 1-4K tokens and choose the cap on dev |
| **Self-consistency / majority vote** | DeepConf (https://arxiv.org/abs/2508.15260): Qwen3-8B AIME25 goes 68 → 82% only with 511 extra traces (about 100M tokens); confidence filtering saves 43-79% of tokens vs majority vote at the same accuracy (up to 84.7% in the abstract). short-m@k (https://arxiv.org/abs/2505.17813): short-1@k matches majority vote with up to 40% fewer thinking tokens; short-3@k cuts wall time up to 33% | Large on math, small on MCQ knowledge | k× tokens, but **near-1× wall time** if sampled as a parallel batch (decode is memory-bound) | Optional for math items only, k=4-8, short-3@k stop rule |
| **No-thinking plus parallel sampling** | "Reasoning Models Can Be Effective Without Thinking" (https://arxiv.org/abs/2504.09858): at an equal 700-token budget, NoThinking scores 51.3 vs Thinking 28.9 (ACM23); parallel NoThinking with best-of-N matches Thinking at up to 9× lower latency | Good on easy and medium math | Small | **Tier 2**: GSM8K-type items |
| **PRM-guided search** ("1B beats 405B", https://arxiv.org/abs/2502.06703) | 3B beats 405B on MATH-500 and AIME24 under compute-optimal test-time scaling | Very large on math | Needs a PRM verifier (7B-72B PRMs in the paper), so it **violates the 4B-only rule** | No |
| **Learned when-to-think** | AdaptThink (https://arxiv.org/abs/2505.13417): 1.5B model, −53% length and +2.4 accuracy (GSM8K, MATH500, AIME24). Thinkless (https://arxiv.org/abs/2505.13379): 50-90% less long thinking. Learning-When-to-Think (https://arxiv.org/abs/2608.20256): 1.5B model, MATH500 0.782 vs 0.796 at −41% tokens; GSM8K −76% tokens | Same accuracy, far fewer tokens | Needs RL training of the 4B | Not now (cost and risk); an external gate is cheaper |
| **External router / gate** | Self-Route (https://arxiv.org/abs/2505.20664): hidden states at 60-80% depth, 30-55% fewer tokens, <2% accuracy loss vs always-reason. SynapseRoute (https://arxiv.org/abs/2507.02822): 58% of medical questions are solved by non-thinking; routing reaches 0.839 vs 0.827 always-think, −36.8% time, −39.7% tokens. **litjev System Two on Qwen3.5-4B** (https://github.com/zhengxuyu/litjev/pull/12): MMLU-Pro n=346, fast 0.540 / slow 0.740 at 994 tok/q / gate 0.717 at 53% escalation and 526 tok/q (layer-24 PCA-64 MLP; escalate if P(fast✗, slow✓) − P(fast✓, slow✗) > λ) | 89% of the slow gain at about half the tokens | One logistic or MLP head; trained on dev | **Yes, recommended** |
| **Distill thinking back into one-pass** | "Distilling System 2 into System 1" (https://arxiv.org/abs/2407.06023), Llama-2-70B: works for S2A, Rephrase-and-Respond and Branch-Solve-Merge; **fails for CoT math**: GSM8K CoT 52.77% vs distilled one-pass 7.13% | Maybe small on recall, ~0 on math | Training run | Low priority. The teacher would be our own 4B (within the rule), but math and code will not compress into one pass |

## 4. Recommended design: keep one-pass speed and add a gated slow path

```
request ──► Tier 1: C1 = Qwen3.5-4B + LoRA, one prefill, letter logits      (20-50 ms, every item)
              │  features (free): p_top, margin(top1-top2), entropy over letters,
              │  tag = has "=", digits/units in options, code block, STEM keywords
              │  (+ optional probe on layer ≈ 0.6-0.75 depth, PCA-64, as litjev / Self-Route)
              ▼
            gate:  escalate if  P(slow✓ & fast✗) − P(fast✓ & slow✗) > λ(effort)
              │         effort=fast → never; auto → λ chosen on dev; deep → always for tagged items
              ├─ tag ∈ {grade-school math, code-trace} ─► Tier 2: base 4B (adapter OFF),
              │       enable_thinking=False, "work briefly then answer", ≤512 tokens,
              │       optional k=4-8 parallel samples + vote (short-3@k)
              └─ tag ∈ {science/GPQA-like, hard logic} ─► Tier 3: base 4B (adapter OFF),
                      enable_thinking=True, budget cap B∈{1K,2K,4K}, then Qwen stop-thinking insert
              ▼
            final readout: append "Answer:" and read logits restricted to the option letters
            (same parser as C1; no free-text parsing failures).
            Optional merge: if the slow path's letter prob < τ, average it with C1's distribution.
```

Notes:
- **Default stays one-pass.** The API exposes `effort` and the response reports `tier_used` and latency. DI and JevBench reports show both a **fast** column and an **auto** column, with mean and p95 latency. Never present the auto score as if it came at fast-path speed.
- **Gate training data must be disjoint from DI, OHS-3 and ejs-5.** Run tier 1 and tier 3 on dev items to label (fast✓/✗, slow✓/✗).
  - Candidates: GSM8K *train* split (MIT, 7,473 items).
  - Claude- or program-authored math word problems with computed answers.
  - Program-labelled code-trace items: generate a snippet, execute it, use the real output (this is the right stand-in for CRUXEval, which is test-only).
  - ARC or other commercial-licence MCQ sets after deduping against DI items.
  - Exclude anything non-commercial (for example SciQ, CC BY-NC).
  - Watch out: MMLU-Pro contains questions derived from MMLU, so dedupe against DI's MMLU items by text before using it. GPQA main/extended includes Diamond, so drop the Diamond ids.
- **Choose λ and B on dev** to maximise (accuracy gain) − c·(seconds). Freeze them before any DI report run (fits the A13-style report-only rule).
- **Cost to build:** about 2-5K dev items × about 1-3K tokens is 2-15M generated tokens. My estimate: well under $5 on a Modal H100 with vLLM batching, or a few hours on the free L4. No training is needed except a tiny gate head (CPU).

## 5. Latency budget (estimates; measure before claiming)

- Decode is memory-bandwidth bound at batch 1. Qwen3.5-4B is about 4.7B params (AA page, https://artificialanalysis.ai/models/qwen3-5-4b), which is about 9.4 GB in bf16.
  - L4 (300 GB/s): at most about 32 tok/s, realistically about 25-30.
  - H100 SXM (3.35 TB/s): at most about 350 tok/s, realistically about 150-250.
  - FP8 weights roughly double both.
  - Qwen3.5's hybrid linear attention keeps long-trace decode close to these rates.
- Per escalated item: tier 2 (about 300 tokens) takes about 1.5-2 s on H100 and about 10-12 s on L4. Tier 3 (about 1K tokens, the litjev MMLU-Pro average) takes about 4-7 s on H100 and about 35-40 s on L4. Tier 3 at a 4K cap takes about 16-27 s on H100 and over 2 min on L4.
- Mean latency under "auto" is (1−p)·0.03 s + p·T_slow. With p = 0.2 and T_slow = 5 s, that is about 1 s, versus Jev's 70-500 ms. **So "auto" is a quality mode, not a speed mode.** The fast default keeps the speed story.
- Parallel votes (k=4-8) add little wall time on a GPU at small batch, but they multiply GPU cost by k. Use them only on math items.
- The slow path cannot reuse C1's KV cache (different weights, with the adapter on vs off). The re-prefill of 0.5-2K tokens costs only tens of ms on an H100.

## 6. Can the LoRA decision adapter coexist with base thinking? Yes

- **Option A (recommended): one resident base model, adapter toggled per request.**
  - HF/PEFT: run tier 1 normally and tiers 2-3 inside `with model.disable_adapter():` (https://huggingface.co/docs/peft/en/package_reference/peft_model). Or use `disable_adapters()` / `enable_adapters()`.
  - This keeps the base model's thinking ability bit-identical, so C1 training can never damage it. This matters because Qwen3 thinking degrades when fine-tuned on non-reasoning data. Unsloth advises a 75% reasoning / 25% non-reasoning mix to keep it (https://unsloth.ai/docs/models/tutorials/qwen3-how-to-run-and-fine-tune, https://github.com/unslothai/unsloth/issues/3005).
  - C1 never needs to think, so there is no reason to mix reasoning data into the adapter.
- **vLLM traps for Qwen3.5 + LoRA:**
  - (1) Silent no-op. PEFT saves keys as `base_model.model.model.layers.N...`, but vLLM's Qwen3.5 stack expects `...model.language_model.layers...`. The adapter loads without an error and changes nothing (vLLM 0.29, https://github.com/whilehq/whileai-sdk/issues/588). Fix: rename the keys (header only).
  - (2) LoRA on Qwen3.5-2B crashed in vLLM 0.17 with an IndexError and then a shape mismatch. The issue was closed as stale, not fixed (https://github.com/vllm-project/vllm/issues/36478).
  - Guard: after every server start, compare letter logits on about 10 fixed non-test prompts against the PEFT reference, and fail closed on a mismatch.
- **Option B: two copies** (merged C1 plus the plain base). Together that is about 19 GB bf16. It fits on an L4 (24 GB) only with a small KV budget, or with FP8 weights. It is simpler and avoids LoRA-serving bugs, but uses twice the memory.
- **Option C: a mode token inside one fine-tuned model.** This means training the adapter to keep thinking (mixed data). It costs extra training and risk, and is not needed given Option A.

## 7. Risks and unknowns
- No official numbers exist for Qwen3.5-4B non-thinking (beyond Qwen3.5-2B and Qwen3-4B), for Qwen3.5-4B GSM8K or CRUXEval, or for its thinking accuracy at small (1-4K) budgets. All of these are unknown, so measure them on dev.
- The litjev result is one unreviewed repo with n=346. Treat it as directional.
- The DI harness rules on generation and latency are unknown. The report must disclose the effort mode.
- A hallucinated fact in the reasoning trace can make thinking *worse* on recall items ("Thinking to Recall"). The gate must learn P(fast✓, slow✗), not just "is it hard?".
- Running code to answer CRUXEval-type items (a tool route) would beat CoT (Sprague: solvers beat CoT), but it is a product and fairness decision for the owner, so it is not recommended by default.

## 8. Concrete next steps (each maps to a dev-only experiment; owner OK needed for any GPU spend)
1. Build about 3K dev items (math, code-trace, science MCQ, recall MCQ) disjoint from DI, OHS-3 and ejs-5, with commercial licences.
2. On dev, measure tier 1 (C1), tier 2 (base, non-think, ≤512 tokens) and tier 3 (base, think, B = 1K/2K/4K): accuracy and tokens per category.
3. Fit the gate (margin + tag first, then optionally a layer-~24 PCA probe). Pick λ and B on dev and freeze them.
4. Implement the adapter toggle (PEFT first), plus the logit-equality guard if moving to vLLM.
5. Report-only DI run with fast and auto columns plus latency (A13-style, no selection).
