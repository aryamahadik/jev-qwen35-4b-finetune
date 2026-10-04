# R_skeptic: corrections to PLAN_knowledge_gap.md

3 Oct 2026. Sources: web checks (URLs below), the public Decision Index (DI) repo at the pinned commit 52a6989 (README, docs/suite.md, decision_index/runner.py), and the committed DI aggregates (`report_sample10k.json`, `check_index_math.json`; scores only). I made no runs and no paid calls, and I opened no held-out or quarantined files.

## Verdict
- **The direction holds.** An opt-in think route on the same Qwen3.5-4B, with fast mode as the default, fits the owner rules. Nothing in it needs a bigger teacher or Jev outputs.
- **Six things are wrong or overstated:**
  1. The projection is too high, mostly on GPQA, MMLU and CLadder.
  2. The "with tools" row relies on running CRUXEval's code. That copies the answer key the same way the banned chess engine does.
  3. Other areas will not stay unchanged. A content gate also routes items in the other four areas.
  4. The DI run (Step 7) costs about 10× more than stated, because the harness runs requests one at a time.
  5. The "faster than Jev" claim is not supported by our L4 numbers.
  6. The format-shaped routes conflict with DI's own "No prompt tuning" rule.
- **Corrected estimate (pure auto mode):** knowledge about **64 (58-70)** and index about **57.4 (56.2-58.6)**, before any effect on other areas. Once CRUXEval execution moves to the reference column, the tools row is about the same as the pure row. The chance of matching Jev's knowledge area is about 10-15% in pure auto mode, and under 15% with tools. The plan said about 25% and about 60%.

## A. Numbers checked against sources

| Plan claim | What the source says | Status |
|---|---|---|
| Qwen3.5-4B: GPQA-D 76.2, MMLU-Redux 88.8, MMLU-Pro 79.1 | Card: same numbers. Thinking is on by default. Output length is 32,768 tokens for most queries and 81,920 for hard ones. Sampling at temperature 1.0 with presence_penalty 1.5. The card gives no non-thinking scores. | OK, but these are **full-budget, sampled** numbers |
| Qwen3-4B: GPQA 41.7 → 55.9, Redux 77.3 → 83.7 | Qwen3 report, Tables 17 and 18 | OK |
| Qwen3-4B-Base GSM8K 87.8 | 87.79, measured **4-shot CoT on the base checkpoint** | OK, but it is not the Qwen3.5-4B no-think number. That number is unknown. |
| Sprague: +12.3 math, +14.2 symbolic, +0.7 other; MMLU gain only on "=" questions | Confirmed | OK |
| Llama-3.1-8B GSM8K 20.1 → 86.4 ("+66") | The paper says GSM8K gains are "as large as 66.9". I could not find 20.1/86.4 on the pages I read. | **Unverified.** "+66" is the largest gain, not a typical one, so do not use it as a basis. |
| litjev, Qwen3.5-4B on MMLU-Pro: 54.0 / 74.0 / 71.7 | Confirmed (PR #12, Apache-2.0, independent and not Jev-affiliated). The slow path ran at about a **1K cap** (994 tokens per question), and "512-token budgets truncate 98.5%". | OK. It also shows that a **1K cap costs about 5 points** against the card (74.0 vs 79.1). |
| Thinkless: thinks on 25.9%, 0.946 vs 0.958 | Minerva Algebra, R1-Distill-**1.5B**, router trained with RL | OK, but it is math-only with a **learned** router, not a margin gate |
| Self-Route: <2% loss, 30-55% fewer tokens | Uses a **hidden-state probe**, not answer margins | OK, but it does not support the margin gate the plan uses |
| Qwen2.5-Coder-7B CRUX-O CoT 65.9 | Confirmed; free-form answers. The 3B model scores 56.0. | OK |
| CLadder: "no published 3-9B thinking numbers" | CDCR-SFT paper: Llama-3.1-8B **CoT-SC 72.88**, R1-Distill-Llama-8B 74.29, Mistral-7B 59.60 | **Wrong.** Numbers exist, and they use self-consistency (several samples). A single-sample 4B is more likely about 65-73. |
| CDCR-SFT 95.33 on Llama-3.1-8B, data from DeepSeek-R1 | Confirmed | OK (the data is unusable for us) |
| Qwen2.5-Math-7B GSM8K: CoT 95.2 vs TIR 94.6 | Confirmed (1.5B: 84.8 vs 83.7) | OK |
| Deng et al.: Phi-3 0.28 → 0.31 vs 0.74 | Confirmed. But Mistral-7B went **0.38 → 0.51** with the same method. | Picks the worst case. #5 is still unmeasured. |
| GPQA: GPT-4 38.8 with and without search | Confirmed (Diamond; main set 39.7 → 41.0) | OK |
| MassiveDS: Qwen3-4B 66.0 → 68.9 | Confirmed, but 66.0 is a weak no-retrieval baseline for this model | OK, weak evidence |
| General-Reasoner 4B GPQA 42.9 < Qwen's 55.9 | It started from **Qwen3-4B-Base** (GPQA 26.3) | Unfair comparison. Drop it as an argument. |
| Chess: "7-8B LMs top out around 25-30%" | arXiv 2507.00726 measures **puzzle accuracy**, and uses SFT traces **from OpenAI o3** | **Wrong metric** for best-move accuracy, and the method breaks our teacher rule |
| ChessBench: "56-63% best-move with about 10M games" | The full-data table in the paper gives puzzle accuracy and Elo. Action accuracy appears only in the 1M-game ablations. | **Unverified** |
| ChessBench key = Stockfish 16 at 50 ms | Confirmed. The test set is 11K Lichess games from **March 2023**. | OK |
| "C1 median on knowledge items 242-262 ms" | DI report: MMLU 242, GPQA 262, GSM8K 248, CRUX 244, CLadder 245, **ChessBench 624.5** | Fix to **242-625 ms** |
| Index arithmetic (74.6 needed; 1.15 index points from other areas; ±1.2 noise) | Recomputed: 297.55 − 222.91 = 74.64. Other areas are 5.76 area points behind = 1.15 index points. SE = √48.7/6 = 1.16. | OK |

## B. Overstated gains: corrections

1. **GPQA 55-70 (mid 63) is too high under the plan's own limits.**
   - No source gives Qwen3.5-4B accuracy at a 1-4K cap.
   - The only same-model data point (litjev) shows a 1K cap costing about 5 points on MMLU-Pro. MMLU-Pro needs much shorter reasoning than GPQA.
   - The fit rule allows on average ≤1.5K added tokens per routed item. That pushes the science route toward a 1-2K cap.
   - Qwen3-4B with no thinking scores 41.7, so a short cap can land close to that.
   - **Use 45-68, mid about 57**, until measured on K-Sci.
2. **"GSM8K 85-92, high confidence" contradicts section 8,** which lists Qwen3.5-4B GSM8K as unknown.
   - The 87.8 anchor is a few-shot base-model number.
   - Tier 2 runs with thinking off and a 512-token cap; 512 tokens cut 98.5% of MMLU-Pro thinking traces.
   - Restate as **82-92, medium confidence**.
3. **CLadder mid 72 → about 70 (62-78).**
   - Published 8B numbers (72.9, 74.3) use self-consistency.
   - A 4B with a single sample is likely lower. Any tie with Jev's 72.6 is inside the ±3.1 noise.
4. **MMLU low end 84 assumes routing never hurts.**
   - A cut-off thinking answer can be worse than C1's answer, and the plan's own Risk 3 says so.
   - The plan also ignores MMLU's label noise.
   - **Use 82-87.5, mid about 85.**
5. **The tools row is inflated by CRUXEval execution, and the policy is inconsistent.**
   - DI's CRUXEval gold came from running the code. DI's options are gold plus codellama-7b's wrong outputs (docs/suite.md; chance 0.370).
   - Running the item's own code copies the answer key. That is the same reason the plan bans the chess engine (#9). CRUXEval also exists to test code reasoning without running the code.
   - **Move "run the item's code" to the reference-only column** together with the chess engine.
   - Keep only tools the model drives itself, such as the 4B writing a GSM8K program, in the tools row.
   - The tools-row knowledge then drops from 70.0 to **about 64.3**, and the index to about **57.4**. The "likely (about 60%)" match with tools becomes **unlikely (<15%)**.
6. **"Other areas held at C1's values" is wrong for a content gate.**
   - The gate routes any item with a low C1 margin or a science/"=" tag. By rule it cannot know the benchmark, so it also routes items outside knowledge:
     - ChessBench (C1 is near chance, so margins are low on almost all 230 items);
     - POP909-CL (about 120 chord options, C1 at 8.5);
     - iSarcasm;
     - low-margin yes/no candidates in ToolRet and BRIGHT (about 7.4K questions each in the sample, scored by nDCG);
     - BFCL, ContractNLI and cfcolor, where the LoRA is what makes C1 win, and the route switches the LoRA off.
   - **Corrections:**
     - Add an "all areas" row with a ± for each area.
     - Restrict routing generically (for example, only single choice questions with ≤10 options, never per-candidate yes/no relevance items).
     - Add dev sets where a low margin does **not** mean thinking helps (chess positions, chord labels, sarcasm, retrieval relevance), so the gate can learn to skip them.
     - Without such sets, the gate cannot learn to skip ChessBench or POP909.
7. **Readout breaks above 26 options.**
   - "Read the letter after Answer:" assumes A-Z.
   - DI has items with up to 151 options (ChessBench move lists, POP909).
   - The routed readout must reuse od_engine's own option labels, or route only items with ≤26 options (a rule written into the gate).
8. **Corrected projection** (my estimates, pure auto, other areas unchanged):

   | Benchmark | Plan | Corrected |
   |---|---|---|
   | MMLU | 86 (84-87.5) | 85 (82-87.5) |
   | GPQA | 63 (55-70) | 57 (45-68) |
   | GSM8K | 88 (85-92) | 88 (82-92) |
   | CRUXEval | 73 (65-82) | 73 (65-82) |
   | CLadder | 72 (65-80) | 70 (62-78) |
   | ChessBench | 11.7 | 11.7 (or lower if routed) |
   | Knowledge | 65.6 (61.0-70.5) | **64.1 (58.0-69.9)** |
   | Index | 57.7 (56.8-58.7) | **57.4 (56.2-58.6)** |

## C. Rule problems

1. **DI's own rule: "No prompt tuning. … one fixed rendering for every benchmark. Per-benchmark prompts, few-shot examples or label-aware tricks are not part of the benchmark."** (DI README, Rules)
   - The gate's branches match DI formats almost one to one:
     - "all-numeric options + word problem" → GSM8K;
     - "code in state + Python-value options, then execute" → CRUXEval;
     - "given probabilities + yes/no" → CLadder.
   - Each branch gets its own prompt, tier or tool. That is per-benchmark handling keyed on content.
   - Blanking the benchmark name does not fix this.
   - **Correction:**
     - Use **one generic think prompt** for every routed item.
     - Route on generic signals: margin plus a learned hidden-state probe (as in litjev and Self-Route), trained on the mixed dev pool.
     - Expose the tools as one general Python tool that the model may call on any item. Drop hard-coded "if code in state, run it".
     - Publish the gate's feature list.
2. **A13 "DI never chooses" is only partly kept.**
   - The DI per-benchmark gaps chose the dev-set mix: K-Math, K-Code and K-Causal are named as stand-ins for GSM8K, CRUXEval and CLadder.
   - That mix sets the gate thresholds. So the DI shaped a model-facing setting.
   - The plan says this "keeps A13's never-chooses rule", which overstates it.
   - **Correction:**
     - A17 should say "DI-informed design".
     - The auto-mode DI columns should carry that label.
     - Weight the dev mix by product traffic, not by DI benchmark.
3. **Known GSM8K distractor artifact.**
   - The plan notes that DI's GSM8K distractors put the gold at the centre of a ±1/2/5/10, ×2, ×10, //2 pattern.
   - Any fallback that picks the "middle" option is a label-aware trick.
   - **Correction:**
     - Ban option-pattern heuristics in A17.
     - Add a test: on DI-format synthetic items, accuracy must not change when the distractors are re-drawn off-centre.
4. **#5 self-distillation prompts.**
   - If the prompts come from MMLU-Pro (10 options, GPT-4-written distractors per its card) or SuperGPQA (built with LLM-assisted screening), the training data contains bigger-model-written text. The plan excludes exactly that.
   - **Correction:** #5 trains only on Claude-authored or program-generated prompts (K-Math, K-Code, K-Causal style). MMLU-Pro and SuperGPQA stay evaluation-only.
5. **Chess (#6).**
   - The labels come from the same generator as the answer key (Stockfish 16 at 50 ms), on the same source as the test set (Lichess).
   - **Correction:**
     - Exclude **all March 2023 Lichess games**, not only matching FENs.
     - Label any later DI ChessBench result "trained against the key's labeller".
6. **Decontamination copies of DI test sets.**
   - The plan downloads MMLU test, all of GPQA, GSM8K test and the rest in plain text. GPQA's authors ask that it not be posted in plain text.
   - **Correction:**
     - Keep these copies under a git-ignored quarantine-style folder.
     - Touch them only through the counts-only tool.
     - Never place them where builders or agents read dev data.
7. **Extra DI looks.**
   - Step 7 runs three columns and Step 8 adds an "optional DI re-run". Several looks invite picking the best one.
   - **Correction:** fix in A17 exactly one DI look per shipped adapter, publish every column, and drop "optional".
8. **Where the product-mix dev comes from.**
   - The gate is fit on "our existing internal dev sets".
   - **Correction:** list the exact files in A17 and certify that none contains Jev-labelled rows, JevBench, OHS-1/2/3, ejs-5 or sealed-suite items. Fitting the gate counts as tuning.

## D. Latency and speed claims

1. **"Faster than Jev" is not shown, even for fast mode.**
   - C1's DI medians on the L4 are 242-262 ms (ChessBench 625, BFCL 750, ToolRet about 8 s).
   - Jev's OpenRouter p50 is 168 ms, and that includes the network.
   - **Correction:** claim speed only from measurements on the target GPU with a comparable network path, and publish p50/p95.
2. **Routed-latency figures are bandwidth estimates that assume a vLLM-class engine.**
   - The DI engine today is HF transformers (od_engine.py).
   - Without `flash-linear-attention` and `causal-conv1d`, Qwen3.5's Gated DeltaNet layers fall back to the slow reference PyTorch code.
   - Neither vLLM nor SGLang implements Qwen's `thinking_budget`. It has to be built as a two-pass splice or a logits processor.
   - Tier 2 is capped at 512 tokens, not 300, so on the L4 it can reach about 17-20 s.
3. **The timeout is undefined.**
   - The DI runner has no timeout, so the engine must set one.
   - On the L4, a 4K cap takes over 2 minutes, so any sane wall-clock timeout turns tier 3 into C1 fallbacks, and the result then depends on machine load.
   - **Correction:** in A17, define the cap in tokens. Keep a wall-clock timeout only as a crash guard, and report fallback counts.
4. **Sandbox latency of "1-50 ms" is too optimistic.**
   - A fresh nsjail or bubblewrap process plus CPython startup takes about 20-60 ms. The CPU limit is 2 s.

## E. Licences and tools
- Commercial terms are confirmed for: SuperGPQA ODC-BY (attribution required), MMLU-Pro MIT, CLadder repo MIT, MMLU MIT, ARC CC-BY-SA-4.0, Lichess CC0, Qwen3.5-4B Apache-2.0 and litjev Apache-2.0. All are evaluation-only in this plan.
- **MMLU-Pro** adds 5,222 new items: TheoremQA, SciBench and **scraped "STEM websites"**. Its distractors were written by GPT-4. Use it for evaluation only; it is never training data (see C4).
- **Stockfish GPL-3:** running it as a separate process for labels is fine. **Shipping it inside an on-prem package** brings GPL distribution obligations, and on-prem is our wedge. Keep it out of the product (#9 is reference-only anyway).
- **Sandbox:** nsjail (Apache-2.0) and bubblewrap (LGPL) need Linux user namespaces. These are often unavailable in gVisor-style containers (Modal) and in locked-down customer hosts. Check before relying on the tools row in the product.
- **Wikipedia (CC BY-SA)** in a datastore brings attribution and share-alike duties. #8 is skipped, but note it.
- **Contamination:** the Qwen3.5-4B card reports SuperGPQA (52.9) and MMLU-Pro (79.1), so Qwen evaluated against both. K-Sci and K-Sci-2 are not "clean absolute" sets; use them for paired comparisons only.

## F. Hidden costs and protocol gaps

1. **Step 7 (the DI run) is understated by about 10×.**
   - The harness runner is a strict one-request-at-a-time loop (runner.py).
   - Routed knowledge items alone, at about 300-4K tokens each, come to about 0.85-2.4M generated tokens. That counts GSM8K 460, CRUX 229, CLadder 229, GPQA 196, about 100 MMLU items, and ChessBench 230 if the gate routes it.
   - At the plan's own 25-30 tokens/s on the L4, that is **about 8-27 hours per auto column**. It excludes display-only and other-area items, and it excludes the 6-9 hour tier-1 pass if that is not reused.
   - **Correction:** budget **about 30-70 L4-hours**, or about 1-4.5 H100-hours per column (≈$5-15 on Modal, which needs GO). Alternatively, reuse cached tier-1 probabilities, keyed by run_id, from the existing C1 run.
2. **Step 3 is undercounted.**
   - Dev-fit is about 9.3K items (60% of 15.5K) plus the product-mix set.
   - A 4K tier-3 run on every item a margin gate might route, at about 2.5-3.5K average tokens, plus tier 2, comes to **about 26-36M tokens**, not 20M.
   - That fits in 6-8 L4-hours only with vLLM batching. With HF transformers it takes several times longer.
3. **A new serving stack is not in the plan:**
   - vLLM or SGLang with Qwen3.5 kernels;
   - the stop-thinking splice;
   - presence_penalty, which HF `generate` does not offer;
   - both stacks in 24 GB on the L4;
   - a parity test between the HF tier 1 and the new stack.
   - Add about 1-2 days.
4. **Determinism.**
   - Qwen3.5's recommended thinking sampling is temperature 1.0 with presence_penalty 1.5. Routed answers therefore vary from run to run, and GPQA has only 196 items.
   - **Correction:**
     - Fix the seeds and record the decoding settings in the DI `latency`/`provenance` fields.
     - Run dev-confirm with 2 seeds and report the spread.
5. **The K-Causal deduplication conflicts with the plan's own rule.**
   - CLadder generator text reuses template sentences. The plan's "shared 13-word sequence" rule would drop almost every generated item.
   - **Correction:** ignore n-grams that appear in more than 20 released items, as the DI overlap tool already does, and dedup on the (graph, query type, numbers, story) tuple.
6. **Option-count mismatch.**
   - K-Sci has 4-10 options and K-Sci-2 has 10. DI's GPQA has 4.
   - Margin thresholds fit on 10-option items will not transfer. Subsample to 4 options (gold plus 3 distractors) for the GPQA-like slice, or normalize the margin by option count.
7. **Power is overstated.**
   - The "about 2,000 items gives SE about 0.9" figure uses the full set. Dev-confirm is 40%: about 800 items, and 726 for K-MMLU.
   - With about 8% of answers changed, the paired SE on K-MMLU is about 1.05. The guard "lower bound > −0.5" then needs a mean of about **+1.6** to pass, so it can fail on noise alone.
   - Resize the sets or loosen the guard, and pre-register which.
8. **The ship rule is too easy.**
   - K-Math alone, at about +30, lifts the macro average of 5 sets past +5. The rule therefore passes even if the science route does nothing.
   - **Correction:**
     - Use per-set rules: each reasoning set's lower bound ≥ 0, and K-Sci gains ≥ +5 at the chosen cap.
     - Add a p95 latency limit per route.
9. **The gate design does not match its evidence.**
   - The plan uses a margin + keyword gate. The cited gating evidence (litjev, Self-Route, Thinkless) all uses **learned** routers.
   - Either adopt a small probe (litjev: layer-24, PCA-64 MLP, trained on CPU) or lower the "keeps most of the gain" claim.

## G. Edits to make in PLAN_knowledge_gap.md (short list)
1. Replace the tables in §0, §2 and §3 with the corrected projection (B8). Add an all-areas ± row, and lower the match chances to about 10-15% (pure) and under 15% (tools).
2. Move CRUXEval item-code execution to the reference-only column with the chess engine. Keep only model-driven tools in the tools row.
3. Replace the format-shaped branches with one generic think prompt and a learned probe. Exclude per-candidate yes/no items and items with more than 26 options (or use od_engine labels). Cite DI's "No prompt tuning" rule in A17.
4. A17: "DI-informed design" label, exactly one DI look per adapter, no "optional" re-run, a ban on option-pattern heuristics, and a certified list of product-mix files.
5. Fix the Step 7 cost (about 30-70 L4-hours or about $5-15 H100), the Step 3 tokens (26-36M), and add the serving-stack work (1-2 days).
6. Restate the speed claim (fast mode is not shown faster than Jev on the L4) and the knowledge median latency (242-625 ms). Define the cap in tokens and the timeout only as a crash guard.
7. Fix the citations: chess 25-30% is puzzle accuracy from o3-trained models; chess 56-63% is unverified; Llama 20.1 → 86.4 is unverified; CLadder 7-8B numbers exist (72.9 and 74.3 with self-consistency); General-Reasoner started from the Base model.
8. #5 prompts come only from Claude-authored or program-generated items. #6 excludes March 2023 Lichess games.
9. Keep the decontamination copies in a git-ignored quarantine. Use template-aware dedup for K-Causal. Match option counts for K-Sci. Use per-set ship rules and recompute power on the 40% split.

## Sources
- Qwen3.5-4B card: https://huggingface.co/Qwen/Qwen3.5-4B
- Qwen3 report: https://arxiv.org/html/2505.09388 (T7, T17, T18, §4.7; stop-thinking string)
- litjev PR #12: https://github.com/zhengxuyu/litjev/pull/12 ; repo: https://github.com/zhengxuyu/litjev
- DI repo (README Rules, docs/suite.md, decision_index/runner.py @52a6989): https://github.com/flaviusburca/decision-index
- Sprague et al.: https://arxiv.org/html/2409.12183
- Thinkless: https://arxiv.org/html/2505.13379 ; Self-Route: https://arxiv.org/abs/2505.20664
- Qwen2.5-Coder: https://arxiv.org/html/2409.12186 ; Qwen2.5-Math: https://arxiv.org/html/2409.12122
- CDCR-SFT: https://arxiv.org/html/2508.12495
- Deng et al.: https://arxiv.org/html/2405.14838
- GPQA: https://arxiv.org/html/2311.12022
- Retrieval by size: https://arxiv.org/html/2507.20059v1
- ChessBench: https://arxiv.org/html/2402.04494 ; LLM chess RL: https://arxiv.org/html/2507.00726v1
- General-Reasoner: https://github.com/TIGER-AI-Lab/General-Reasoner
- SuperGPQA: https://huggingface.co/datasets/m-a-p/SuperGPQA ; MMLU-Pro: https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro ; CLadder: https://github.com/causalNLP/cladder
- Thinking budget in local engines: https://zolotukhin.ai/blog/2026-05-18-qwen3-thinking-budget-local-engines-still-fake/
- Qwen3.5 slow fallback without fla/causal-conv1d: https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/qwen3_5.md
- vLLM LoRA issues: https://github.com/vllm-project/vllm/issues/36478 ; https://github.com/whilehq/whileai-sdk/issues/588
