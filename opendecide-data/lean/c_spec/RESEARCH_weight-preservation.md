# RESEARCH: keeping C1's skills during the C top-up (weight preservation)

Date: 3 Oct 2026. Scope: web research plus reading our own run config (`runs/q35_4b_main.json`, `train_decoder.py`, PREREG_FINAL A11/A12). CPU only. No paid calls, no eval or test data opened.

## 0. Bottom line (the recipe in 12 lines)

1. **Do not keep training C1's adapter. Add a new adapter on top of C1 and freeze C1.** The new adapter is r16, alpha 32, with B = 0 at the start, so step 0 is exactly C1.
2. **Replay 50% old rows** (owner plan says ~60%; 60% is also safe, see section 3). Sample them from golden_train, stratified by source and question type. Keep relation pairs together. No row twice.
3. **Anchor every replay row to C1:** add `1.0 * KL(p_C1 || p_C)` over the candidate tokens, T = 1. Keep C1's normal loss on those rows too (DER++ style: labels plus old-model outputs).
4. **New rows get C1's normal loss only** (CE + vote-share KD + relation losses). No C1 anchor on them.
5. **Optimizer:** same as C1 (AdamW, wd 0, batch 16, clip 1.0, 5% warmup, cosine to 0), but **peak LR 5e-5** (C1 used 7e-5). One pass. No extra epochs.
6. **Round 2 restarts from C1** with the 300K superset. Do not chain round 2 on top of round 1.
7. **No EWC, no O-LoRA, no InfLoRA, no on-policy SDFT.** Reasons in section 5.
8. **After training: one pre-registered WiSE grid** on the new adapter only: C(t) = C1 + t * dC, t in {0.5, 0.75, 1.0}. Select on a select half, confirm on a confirm half (same rule shape as A11).
9. **Ship** C1 + new adapter as one exact rank-32 adapter (concatenate A and B). Latency change is negligible.
10. **Monitor** anchor KL on replay rows, flips (1->0 and 0->1) vs C1 on a held-out slice of the training pool, and KL(C1 || C) on new-family rows.
11. **Cost:** round 1 about $31 (8,876 steps + anchor forwards), round 2 about $62. Optional 3-arm pilot about $6.
12. **Expected effect:** old-skill change about -0.5 to +0.5 pp with replay + anchor. Without replay, published LoRA top-ups lose 4 to 46%. Weight preservation does not create far-domain gains. Those must come from the new data.

---

## 1. Our setting (facts that change the answer)

- C1 = Qwen3.5-4B + LoRA r16/a32, dropout 0.05, 32,464,896 trainable params, LR 7e-5, batch 16, about 0.97 epoch of ~502K rows = 30,457 steps. Schedule: 5% linear warmup, cosine to 0. AdamW, weight decay 0, clip 1.0 (source: `runs/q35_4b_main.json`, `train_decoder.py` lines 726-761).
- The loss is on **one answer token** (yes/no or option letter). A row carries at most log2(26) = 4.7 bits of label information. 300K rows carry at most about 1.4M bits. A r16 adapter has 32.5M params. At the ~2 bits/param figure cited by Thinking Machines, that is ~65M bits. **Rank is not the bottleneck.** Higher rank only adds room to drift.
- The new data is the **same task** (decisions) with new skill families and new formats. This is not classic continual learning with unrelated tasks. Old and new data overlap a lot. We **have all old data.** So joint replay is possible, and joint training is the upper bound in every paper below.
- The code already has: a KL anchor `beta * KL(p_base || p_student)` over candidate tokens on rows with `meta.anchor`, computed with the adapter disabled (line 908); `init_adapter` to continue an adapter (line 726). **The anchor today points at the base model, not at C1.** To anchor to C1 we need a small change (section 6).
- The gate is strict: A11 confirm rules allow only -0.2 pp on the full set and -0.5 pp on yes/no or choice. So we need near-zero forgetting, not "small" forgetting.

## 2. Measured forgetting numbers (what happens with and without protection)

| Study | Model, setup | No protection | With protection |
|---|---|---|---|
| TRACE (Wang et al. 2023) | LLaMA-2-7B-Chat, 8 sequential tasks | LoRA seq. FT: OP 12.7, **BWT -45.7%**; full seq. FT: OP 48.7, BWT -8.3% | **Replay 10%: OP 55.5, BWT +2.6%** |
| SSR (Huang et al. ACL 2024) | Llama-2-7b, LoRA r8 (q,v), LR 2e-4, 5 SuperNI tasks | BWT **-42.4** | Replay 1%: -4.0; replay 10%: -3.0; **replay with the model's own outputs: -0.8** (MTL AR 53.05 vs 52.16) |
| O-LoRA paper (Wang et al. 2023) | T5-large, standard CL benchmark, avg acc | Same LoRA continued (SeqLoRA): 43.7; SeqFT: 28.5 | New LoRA per task, old frozen (IncLoRA): **66.4**; Replay 57.8; EWC 50.3; LwF 52.3; O-LoRA 75.8; **joint (MTL) 80.0** |
| O-LoRA paper | LLaMA-7B Alpaca-LoRA, MMLU | 37.5 -> 23.3 after seq. LoRA | inc-LoRA 28.6; O-LoRA 33.6 |
| SDFT (Yang et al. ACL 2024) | Llama-2-7b-chat, LoRA r8, LR 1e-4 | GSM8K FT: jailbreak-safe 88.9 -> 54.8; AlpacaEval 66.0 -> 23.4 | Self-distilled targets: 65.6 and 66.7 |
| SDFT on-policy (Shenfeld et al. 2026) | Qwen2.5-7B-Instruct, prior-skill avg 65.5 | SFT: 53.4 / 56.0 / 60.2 (3 tasks) | SDFT: 64.5 / 65.4 / 65.4 |
| Retaining by Doing (Chen et al. 2025) | Llama 3.1 8B, IFEval target | SFT: gain 25.2, **drop 27.8%** | GRPO: gain 18.4, drop 3.4% |
| LoRA Learns Less (Biderman et al. 2024) | Llama-2-7B, Magicoder IFT, "forgetting avg" (higher = better) | Full FT: 0.595 (1 ep) -> 0.512 (4 ep) -> 0.414 (16 ep) | LoRA r16: 0.653 -> 0.652 -> 0.609 |
| Luo et al. 2023 | BLOOMZ 1.1B -> 7.1B, no replay | Domain-knowledge forgetting 9.5 -> 18.4 (grows with size, 1-7B) | - |
| DMT (Dong et al. ACL 2024) | LLaMA-7B, math then general | Sequential: GSM8K 31.4 | Tiny replay (1/256 of math data): 41.9; **joint: 47.5** |
| Ibrahim et al. 2024 | 405M, Pile -> German, Pile val loss | 3.56 | 1%: 2.83; 5%: 2.57; 25%: 2.33; 50%: 2.24 (union-trained: 2.26) |
| I-LoRA (Ren et al. 2024) | Llama-2-7B, 8 domain tasks, BWT | ER on MedMCQA -18.2, JEC-QA -14.8 | I-LoRA (EMA of LoRA + replay) -2.2, -2.3 |

What this says for us:
- A LoRA trained further **without replay** loses a lot (-24% to -46% BWT).
- **Replay alone** brings it to about -3 to +3%.
- **Replay with the old model's own outputs** brings it to about -0.2 to -0.8 (SSR). That is the closest analogue to a KL anchor to C1.
- **Joint training on everything** is always best. Replay plus an anchor is our cheap version of it.

## 3. Replay: how much is enough?

Published "enough" values:

| Source | Shift type | Replay that was enough |
|---|---|---|
| Bethune et al. ICML 2025 (Apple), models up to 1.3B | Pretraining data during fine-tuning | **1%** "prevents forgetting the pretraining set". Without it, small models lose up to 95% of pretraining progress. Large ones lose 20%. |
| Scialom et al. EMNLP 2022 (T0 3B, 8 new tasks) | New instruction tasks | **0.25%** gave "almost perfect stability". 1% was used for CT0. |
| Ibrahim et al. TMLR 2024 | Weak shift / strong shift | **5%** weak (Pile -> SlimPajama), **25%** strong (English -> German). 50% hurt adaptation: German loss 1.22 vs 1.12 at 5%. |
| TRACE 2023 | Sequential LLM tasks | **10%** gave positive BWT (+0.2 to +2.6%) on 5 models. |
| Marek et al. 2026 | Small LMs, new language | **12.5%** replay let them keep a high LR. Getting the same retention by cutting LR cost 38x more compute. |
| Production CPT (cited by Ibrahim) | Annealing / domain CPT | Zamba: 60%. DeepSeek-Coder-V2: 30%. |

So the literature says 5-25% replay stops most forgetting. Why go to 50%?
- Our gate allows almost no regression. Those papers accept 1-4% loss.
- LoRA forgets more than full fine-tuning when trained in sequence (TRACE: -45.7% vs -8.3%).
- Our new data changes the format (new rewordings, label styles). That is a "strong shift" for the readout. Ibrahim used 25% for a strong shift.
- C1's 173 sources must each keep some exposure. At 75K replay rows, each source keeps about 15% of its rows.

Why not more than 50%?
- Above ~50% the new data learns slower (Ibrahim). Round 1 at 60% gives 60K new rows. At 50% it gives 75K (+25%).
- The KL anchor does most of the retention work per row (SSR -0.8 with self-outputs vs -3.0 with gold at 10%; DER++ beats plain replay; Marek: KL beats plain next-token replay).

**Recommendation:** 50% replay plus the C1 anchor. 60% (owner plan) is also fine. It costs ~15K new rows in round 1 and nothing else. The minimum the evidence supports with an anchor is about 25%. Do not go below that.

How to sample the replay:
- Stratify by source and by qtype (yes/no vs choice), in C1's proportions. Put a floor of 100 rows per source so no source vanishes.
- Keep relation partners (complement, equiv, inv) together, so the relation losses still fire.
- Shuffle new and old rows together from step 0. No blocks of one family. (Spurious-forgetting paper: the first ~150 steps on a new task are where old task alignment breaks.)
- Random within strata is fine. Ibrahim saw no gain from reshuffling. SSR saw a small gain from k-means picks (-3.6 vs -4.0 at 1%). SuRe (2025) reports +5 points from replaying the highest-loss rows, but we do not have per-row C1 losses for 500K rows. Round 1's anchor forwards will log C1's probabilities on its replay rows for free. Round 2 may tilt toward low-margin rows if we pre-register it.
- Watch the yes-rate. New families with skewed yes/no labels shift the yes bias on old data. Balance new families or match C1's training yes-rate. Monitor mean P(yes) on old rows.

## 4. Anchoring to the previous model (KL, self-distillation)

Evidence:
- **DER / DER++** (Buzzega et al. NeurIPS 2020): replay the old model's logits, not just labels. S-CIFAR-10 class-IL, buffer 500: plain replay 57.7, DER 70.5, DER++ (logits + labels) 72.7. With a big buffer (5,120) the gap is smaller: 82.5 vs 85.2. Weights alpha = beta = 0.5 were "stable". We have a huge buffer, so expect a small but real gain, mostly in calibration (DER also reports lower calibration error).
- **SSR** (above): replaying inputs with the model's own outputs beat replaying gold labels (-0.8 vs -3.0 BWT).
- **Marek et al. 2026:** a KL penalty on replay data beat plain next-token loss on the same data. They used lambda = 10 for maximum retention.
- **SDFT** (Yang et al. 2024): train on targets rewritten by the model itself. It works for generated text. For our single-token readout, "the model's own targets" is just C1's probability vector. So SDFT reduces to a KL to C1.
- **RL's Razor** (Shenfeld et al. ICLR 2026): forgetting is predicted by forward KL between new and old model **on the new task's inputs**. R^2 = 0.96 (toy) and 0.71 (Qwen 2.5 3B). Weight-change measures predict much worse (Fisher-weighted L2: R^2 0.58; L1: 0.34). Lesson: **regularize outputs, not weights.**
- **Retaining by Doing** (Chen et al. 2025): RL forgets less because of on-policy data, not because of its KL penalty. For us the answer is a full distribution over 2-26 tokens, computed exactly. There is no sampling, so "on-policy" adds nothing beyond a KL to C1.

Settings:
- Term: `beta_c1 * KL(p_C1 || p_C)` over the candidate tokens, same displayed option order as the student. Teacher first (forward KL), as the current base anchor does.
- beta_c1 = **1.0** per replay row, with the normal loss at weight 1. Equal weights follow DER++. C1 already used beta = 1.0 for its base anchor, so the loss scale is known.
- T = 1. C1's probabilities are its calibration. Brier is a gate rule. A temperature would change it.
- Where the gold label and C1 disagree on a replay row, the two terms pull against each other. That is intended: keep C1 unless the gold says otherwise.
- **No anchor on new rows.** Their job is to change C1 where C1 is wrong (for example double negation, 8.9% flips today). Use KL(C1 || C) on new rows as a monitor (RL's Razor), not a loss.
- The base-model anchor: C1 already contains it. Turn it off (beta = 0) for C, unless we deliberately mark some new breadth rows with `meta.anchor`.

Rejected variants:
- **On-policy SDFT** (Shenfeld et al. 2026): needs generation and in-context learning. At 3B it was **3.3 points worse than SFT** on the new task (it only wins from 7B up: +4.0 at 7B, +6.9 at 14B).
- **Dense on-policy self-distillation** (Denser != Better, 2026): in sequential training it collapsed (Math 56.4 -> 34.4; with a moving teacher, 0.00 on all benchmarks).

## 5. Parameter-space methods: EWC, O-LoRA, InfLoRA, OPLoRA

| Method | What it does | Evidence | Verdict for C |
|---|---|---|---|
| EWC | Fisher-weighted L2 pull toward old weights | T5-large CL: 50.3 vs replay 57.8 vs joint 80.0 (O-LoRA paper). Gemma2-2B CPT needed a lambda sweep over 0 to 1e12. Fisher-L2 predicts forgetting poorly (R^2 0.58 vs KL 0.96, RL's Razor). | **No.** With a stacked adapter it becomes plain weight decay toward zero on the new adapter. |
| O-LoRA | New LoRA kept orthogonal to old LoRA's A (lambda1 = 0.5) | T5-large: 75.8 vs joint 80.0. Built for distinct tasks without replay. | **No.** Our new data refines C1's own skills. Forcing orthogonality blocks that. We have the data, so joint replay is available. |
| InfLoRA | New LoRA in a subspace that does not interfere with old tasks' inputs | ViT-B/16 ImageNet-R 10 tasks: 75.65 vs joint 81.14 (vision, class-incremental). | **No.** Same reasons. No LLM decision results. |
| OPLoRA (2025) | Keep updates out of the top-k singular directions of frozen weights | Protects base knowledge. Not C1's adapter skills. | **No.** Wrong target. |
| Freeze bottom layers (spurious forgetting, ICLR 2025) | Do not train the lowest layers | Helped in 4 CL settings | **Optional only.** Our new formats may need low-layer change. Not in the main recipe. |

## 6. Continue C1's adapter, or add a fresh one?

Options:
1. **Continue C1's adapter** (`init_adapter`, already in the code). Same 16 dimensions must now hold old and new. O-LoRA's table: continuing one LoRA (SeqLoRA) 43.7 vs adding a new LoRA with the old one frozen (IncLoRA) 66.4. That was without replay; with replay the gap will be smaller. Also the code's anchor would still point at the base, not C1.
2. **Freeze C1 and add a new r16 adapter (recommended).** Step 0 equals C1 exactly (B = 0). C1's weights cannot be overwritten. The new rank adds room for new families. The anchor to C1 is one adapter toggle away. Post-hoc WiSE is just scaling the new adapter's B. Chain of LoRA (COLA) uses the same "freeze, then new LoRA" idea and reports +6.47% relative (OPT-1.3B, WSC) and up to +4.4% relative (Llama-2-7B) over a single LoRA.
3. **Fresh LoRA from base on everything.** Joint training is the upper bound, but it costs about 3-4x (650-800K rows) and loses C1's exact behaviour. Not in budget.

Do not merge C1 into bf16 base weights to make option 2. bf16 keeps about 3 significant digits. LoRA deltas are small next to the weights, so rounding can eat part of the delta. Keep C1 as a separate frozen adapter instead (exact). If a merge is ever needed, merge in fp32 and check prediction agreement first.

Implementation notes (needs a code change; flag it in the PREREG):
- Load C1 adapter as "c1" (frozen, **dropout 0**), add adapter "c" (r16, alpha 32, dropout 0.05, same target modules). Both active in the training forward.
- Anchor forward: only "c1" active, `torch.no_grad()`, bf16 autocast. Then switch back.
- **PEFT gotcha:** `set_adapter` marks the active adapters trainable. Re-freeze "c1" after every switch. Assert `trainable == 32,464,896` each time (the existing `expect_trainable` check catches a doubled count).
- **Dropout gotcha:** with C1's dropout left at 0.05 in train mode, the anchor targets would be noisy. Set C1's dropout to 0.
- Step-0 self-check (like `_px_selfcheck`): student logits must equal C1 logits on a few rows (max |diff| <= 1e-3), so anchor KL starts at ~0.
- If A11 adopts a* < 1, the frozen "c1" adapter is C1 with lora_B scaled by a*.
- Shipping: one rank-32 adapter, A = [A_c1; A_c], B = [B_c1, B_c], alpha 64 (scale 2, the same as both parts). Exact.
- Fallback if the multi-adapter change is judged risky: continue C1's adapter (option 1) at peak LR 3.5e-5, and give replay rows a precomputed C1 target. Mixing C1's probabilities into the soft target with weight w gives the same gradient as w * KL(C1 || C). The current `kd` mixing works the same way, but needs a per-row weight.

## 7. Learning rate, warmup, steps, batch

Evidence:
- Lower peak LR -> less forgetting, less adaptation (Ibrahim et al.). Warmup length (0.5-2%) "does not appear impactful".
- LR x steps is roughly constant for a fixed target loss. Lowering LR just costs steps. Replay removes the need for a low LR (Marek et al.: 38x compute saved).
- Forgetting grows as a power law in update steps. Early stopping does not avoid it (Kalajdzievski 2024). LoRA r16 forgetting avg drops from 0.652 to 0.609 between 4 and 16 epochs (Biderman et al.).
- LoRA's best LR is ~10x full fine-tuning and nearly independent of rank (within 2x from r4 to r512). LoRA tolerates large batches worse than full FT (Thinking Machines, "LoRA Without Regret"). Biderman et al.: best LoRA LRs 5e-5 to 5e-4 on Llama-2-7B.
- Bethune et al. fine-tuned at 1/30 of peak pretraining LR. That was for a converged base model, not a LoRA top-up.

Choices:
- **Peak LR 5e-5** (0.7x C1's 7e-5). The new adapter starts at B = 0, so it needs a real LR to learn, but the strict gate argues for a little less than C1. Round 1's "LR budget" (sum of LR over steps) is about 21% of C1's. Round 2 is about 42%.
- Warmup 5% (444 steps in round 1, 888 in round 2). Both are well past the ~150-step danger window. Same as C1.
- Cosine to 0, as C1. Batch 16, micro_tokens 8192, clip 1.0, wd 0. Same as C1.
- **Exactly one pass.** No second epoch over new rows.
- Change LR in round 2 only by a pre-registered rule: if round 1 underfits new families (held-out new-family loss still falling steeply at the end) and shows no old-skill loss, use 7e-5.

## 8. After training: WiSE-FT and merging

Evidence for interpolation:
- WiSE-FT (Wortsman et al. CVPR 2022): +4 to +6 pp under distribution shift and +1.6 pp in-distribution on ImageNet. alpha = 0.5 was near optimal across experiments.
- Model averaging (Lin et al. EMNLP 2024, OpenLLaMA-3B): best trade-off of all methods tested. Replay with up to 4x the RLHF data still lost to averaging on 2 of 3 benchmarks. Averaging low layers helped most.
- Dang et al. (COLM 2025): 1/2 early SFT checkpoint + 1/2 late one kept Pass@1 and restored Pass@k.
- LiNeS (ICLR 2025): scale updates down in shallow layers. Kept 99.8% of fine-tuned accuracy and 97.9% of control-task accuracy (CLIP ViT-B/32).
- Intruder dimensions (Shuttleworth et al. 2024): LoRA adds new large singular directions that cause forgetting. Scaling them down cut forgetting with little task loss. alpha = 2r (what C1 uses) gives fewer of them.

Evidence against relying on it:
- Harmon et al. 2025: merging two post-training checkpoints "does not reliably mitigate forgetting".

So: **one cheap, pre-registered grid.** C(t) = C1 + t * dC, made by multiplying the new adapter's lora_B by t, t in {0.5, 0.75, 1.0}. Pick t on the select halves (dev gate unseen-source + sealed new-domains suite select half). Confirm on the confirm halves. Ties go to the larger t. Only reads, no training. LiNeS-style depth scaling stays a backup idea, not a candidate, to keep the comparison count small.

## 9. Exact recipe

Round 1 (150K rows):

| Item | Value |
|---|---|
| Start point | C1 adapter (or a* x lora_B if A11 adopts it), frozen, dropout 0 |
| New adapter | r 16, alpha 32, dropout 0.05, targets as C1 (`QWEN35`), B = 0 at start |
| Mix | 75K new + 75K replay (50/50), shuffled together |
| Replay sampling | golden_train, stratified by source x qtype, floor 100/source, relation partners kept, no repeats |
| Loss, replay rows | C1's loss (task CE + label smoothing, kd 0.5 vote share, relation terms) + 1.0 x KL(p_C1 \|\| p_C), T = 1 |
| Loss, new rows | C1's loss terms; no anchor |
| Base anchor | off (beta = 0) |
| Optimizer | AdamW, wd 0, peak LR 5e-5, 5% warmup, cosine to 0, batch 16, micro_tokens 8192, clip 1.0, fp32 trainable params |
| Length | 1 pass = 8,876 steps |
| Snapshots | 85/90/95% for diagnostics only; ship the final step |
| Post-hoc | WiSE grid t in {0.5, 0.75, 1.0}, pre-registered select/confirm |
| Ship | one rank-32 adapter (exact concatenation) |

Round 2 (300K rows): restart from C1 (not from round 1's C). Same recipe. 150K new (superset of round 1's new rows) + 150K replay. 17,751 steps. Round 1's C stays the fallback. Reason: training in a chain adds intruder dimensions and steps, and joint training beats sequential training in every table above.

Cost (Modal H100 at $4.09/h, 2.72 s/step at 16.9 rows/step):

| Run | Steps | Train time | Anchor forwards (~0.04 s/row, estimate) | Total |
|---|---|---|---|---|
| Round 1 | 8,876 | 6.71 h | 75K rows, ~0.84 h | ~7.6 h, **~$31** |
| Round 2 | 17,751 | 13.41 h | 150K rows, ~1.68 h | ~15.1 h, **~$62** |
| Optional pilot | 3 x 600 | ~1.4 h | ~0.2 h | **~$6** |

The anchor forward estimate assumes one no-grad forward is ~1/4 of a training step per row (gradient checkpointing). Unknown until measured. C1's 2.72 s/step already included some base-anchor forwards.

Optional pilot (pre-register before it runs): three arms, 600 steps each: (50% replay, beta 1.0), (50% replay, beta 0), (25% replay, beta 1.0). Ibrahim et al. found replay differences show "very early in training". Read only training-pool held-out slices (not the gate, not the sealed suite). It tells us if the anchor matters and if 25% would do.

## 10. Monitors and stop rules

- Every log step: mean anchor KL on replay rows. Expect ~0 at step 0. Alert if it passes 0.05 nats after warmup, or rises in 3 logs in a row. (For scale: P(yes) moving 0.8 -> 0.7 is a KL of 0.026.)
- Every 1,000 steps, on 2,000 held-out old rows from the training pool (not the gate):
  - accuracy vs C1;
  - 1->0 flips and 0->1 flips vs C1 (Harmon et al.: count flips, not averages; averages hide trades);
  - mean P(yes) drift vs C1.
- Every 1,000 steps, on 2,000 held-out new-family rows: loss, accuracy, and KL(C1 || C) (RL's Razor predictor).
- Stop rule: if old-slice accuracy is below C1 - 1.0 pp at two checks in a row after 30% of steps, stop, keep the last good snapshot, inspect. Pre-register this.

## 11. Risks and unknowns

- No paper tests our exact case (a 4B single-token decision readout with 173 sources). All numbers above transfer by analogy. Our own monitors are the real test.
- The anchor keeps C1's mistakes on replay rows where gold is missing or noisy. The CE term on gold limits this.
- Weight preservation protects the 84% dev skill. It does not fix the ejs-5 gap (-4.4 vs Jev). That needs new data. Too much preservation (high replay, t < 1) can also hold back far-domain gains. That is why t is chosen on the sealed suite's select half, not only on the old dev gate.
- PEFT multi-adapter code is new for this repo. Self-checks in section 6 are required, not optional.
- Anchor cost is an estimate (+12 to 14%). Measure it in the first 100 steps.

## Sources

- Ibrahim et al. 2024, Simple and Scalable Strategies to Continually Pre-train LLMs: https://arxiv.org/abs/2403.08763
- Bethune et al. 2025, Scaling Laws for Forgetting during Finetuning with Pretraining Data Injection: https://arxiv.org/abs/2502.06042
- Scialom et al. 2022, Fine-tuned Language Models are Continual Learners: https://arxiv.org/abs/2205.12393
- Huang et al. 2024, Self-Synthesized Rehearsal (SSR): https://arxiv.org/abs/2403.01244
- Wang et al. 2023, TRACE benchmark: https://arxiv.org/abs/2310.06762
- Wang et al. 2023, O-LoRA: https://arxiv.org/abs/2310.14152
- Liang and Li 2024, InfLoRA (CVPR): https://openaccess.thecvf.com/content/CVPR2024/papers/Liang_InfLoRA_Interference-Free_Low-Rank_Adaptation_for_Continual_Learning_CVPR_2024_paper.pdf
- Buzzega et al. 2020, Dark Experience Replay (DER/DER++): https://arxiv.org/abs/2004.07211
- Yang et al. 2024, Self-Distillation Bridges Distribution Gap (SDFT, ACL): https://aclanthology.org/2024.acl-long.58/
- Shenfeld et al. 2026, Self-Distillation Enables Continual Learning: https://arxiv.org/abs/2601.19897
- Denser != Better: Limits of On-Policy Self-Distillation for Continual Post-Training (2026): https://arxiv.org/abs/2607.01763
- Shenfeld et al. 2025/ICLR 2026, RL's Razor: https://arxiv.org/abs/2509.04259
- Chen et al. 2025, Retaining by Doing: https://arxiv.org/abs/2510.18874
- Marek et al. 2026, Forgetting in Language Models: Capacity, Optimization, and Self-Generated Replay: https://arxiv.org/abs/2605.26097
- Biderman et al. 2024, LoRA Learns Less and Forgets Less: https://arxiv.org/abs/2405.09673
- Kalajdzievski 2024, Scaling Laws for Forgetting When Fine-Tuning LLMs: https://arxiv.org/abs/2401.05605
- Shuttleworth et al. 2024, LoRA vs Full Fine-tuning: An Illusion of Equivalence: https://arxiv.org/abs/2410.21228
- Zheng et al. 2025, Spurious Forgetting in Continual Learning of LMs (ICLR): https://arxiv.org/abs/2501.13453
- Luo et al. 2023, Empirical Study of Catastrophic Forgetting in LLMs: https://arxiv.org/abs/2308.08747
- Dong et al. 2024, SFT Data Composition / DMT (ACL): https://arxiv.org/abs/2310.05492
- Ren et al. 2024, I-LoRA: https://arxiv.org/abs/2402.18865
- SuRe 2025, Surprise-Driven Prioritised Replay: https://arxiv.org/abs/2511.22367
- Šliogeris et al. 2025, EWC for Gemma2 continual pretraining: https://arxiv.org/abs/2505.05946
- Xiong et al. 2025, OPLoRA: https://arxiv.org/abs/2510.13003
- Wortsman et al. 2022, WiSE-FT: https://arxiv.org/abs/2109.01903
- Lin et al. 2024, Mitigating the Alignment Tax of RLHF (EMNLP): https://arxiv.org/abs/2309.06256
- Dang et al. 2025, Weight Ensembling Improves Reasoning (COLM): https://arxiv.org/abs/2504.10478
- Wang et al. 2025, LiNeS (ICLR): https://arxiv.org/abs/2410.17146
- Harmon et al. 2025, Mapping Post-Training Forgetting at Scale: https://arxiv.org/abs/2510.17776
- Xia et al. 2024, Chain of LoRA (COLA): https://arxiv.org/abs/2401.04151
- Thinking Machines 2025, LoRA Without Regret: https://thinkingmachines.ai/blog/lora/
