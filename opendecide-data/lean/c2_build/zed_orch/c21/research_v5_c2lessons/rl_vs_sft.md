# RL with verifiable rewards after SFT vs SFT alone: small models, decision tasks (research, 18 Oct 2026)

Scope: does GRPO / RLOO / DPO-from-program-gold after SFT improve out-of-distribution (OOD) transfer and calibration for 1-8B models on decision / classification tasks? Then: cost, time and the simplest recipe for a 4B LoRA stage on Modal H100 with 10-30K prompts and 1-token (option) answers.

Method: web search plus page fetch (arXiv abstract/HTML, docs). No model was run, nothing downloaded to the project, no ohs / sealed / quarantine / longbench / jevbench / ejs / Jev-output path was opened, and ~/.claude was not opened (the fetch tool auto-saved three PDFs there; I did not read them and used arXiv HTML or abs pages instead). Project facts are cited as file:line.

Tags: [author-run] = the authors ran it; [independent] = third party; [vendor]; [project] = our own files; DERIVED = my arithmetic or judgement from cited numbers (not a measurement on our model); UNVERIFIED = seen only in a search summary or an unreadable page. "As extracted" = the fetch tool's small model read the table; I re-fetched the key table (Yaldiz Table 4) twice and the two extractions agree.

---------------------------------------------------------------------------------------------------

## 0. Bottom line (read this first)

1. Evidence that RL beats SFT on OOD transfer is real but it is almost all chain-of-thought (CoT) RL against off-policy SFT on teacher traces. The strongest mechanism finding is "on-policy and small KL shift", not "RL" as such. I found NO study of RLVR on direct-answer (no CoT, 1-token) decisions. Our serving path is no-thinking, one-token readout, so the literature transfers only partly. (UNVERIFIED gap: three searches, none found.)
2. On calibration the evidence points the OTHER way. Binary 0/1 RLVR makes small models more overconfident than answer-only SFT: Qwen3 1.7B/4B/8B, 4 decision datasets, GRPO ECE is higher than SFT ECE in 12 of 12 cells (mean 13.3 vs 6.3 points) while accuracy is higher in 11 of 12 (mean 86.0 vs 83.2). [author-run, arXiv 2601.13284]. A 0/1 reward is not a proper scoring rule, so this is expected, not a bug.
3. Adding a Brier-type term to the reward fixes calibration in published work (RLCR: HotpotQA ECE 0.37 -> 0.03, Qwen2.5-7B) but OOD calibration is only partly fixed (OOD ECE 0.46 -> 0.21; still far from in-domain). [author-run, arXiv 2507.16806]
4. For a 1-token answer, sampling rollouts is unnecessary: the policy gradient of the 0/1 reward can be computed EXACTLY from one forward pass over the option logits (it equals the gradient of -p(gold)). Brier loss is exactly "2 x expected 0/1 reward minus a sharpness penalty" (algebra, section 4). So the cheapest "RL" stage costs the same as one SFT pass: about $2.2 (10K prompts) to $6.6 (30K) measured against C2's own s/row (section 6). DERIVED.
5. Real sampled GRPO (TRL, G = 8) trains on G sequences per prompt: DERIVED $18 (10K prompts) to $53-66 (30K prompts) on one H100, plus Qwen3.5-4B stack risk. It does not fit inside the C2.1 $30 training cap next to the $26-28 SFT run. Not recommended for C2.1.
6. Expected benefit over a well-chosen SFT checkpoint is small and not guaranteed: RL usually does not beat the early SFT OOD peak (arXiv 2509.12235), cannot rescue an over-fit SFT checkpoint (arXiv 2501.17161), and cannot fix a label-prior shortcut that the data teaches (C2's T19 "Cannot be determined" collapse). Honest DERIVED range vs the best blended SFT candidate: transfer 0 to +2 pp, ECE neutral if reward is proper-scoring + per-type T, worse if 0/1.
7. DPO / ORPO from program gold: offline, so it behaves like SFT for forgetting (RL's Razor), and DPO is documented to push confidence up. The v3 decision to keep it in NOT ADOPTED stands (C2_1_PLAN_v3.md:1063-1065).

---------------------------------------------------------------------------------------------------

## 1. What C2 taught us, and what an RL stage could and could not touch

C2 facts (task statement plus project files): trained-family dev +12.3 pp; transfer to 2 unseen families -4.8 pp (T19 -11.3: "Cannot be determined" on 76/98 verdicts vs truth 26 and C1 54); ECE C1 4.1% vs C2 13.2% (C2 overconfident); Brier worse +0.0098. Training: LoRA r16 / alpha 32, lr 5e-5 cosine, batch 16, one pass (0.9901 epochs), KD 0.5 on replay, 3,673 steps in 186.0 min, about 3.04 s/step, $13.14 [project, c2_build/C2_REPORT.md:15,44,47].

Mapping of failure to lever:
- Transfer loss from a label-prior shortcut ("Cannot be determined") is a DATA problem (balanced gold, minimal pairs, held-out families, per-family caps), which the v3.2 plan already addresses. RL sharpens whatever the reward admits, so RL on the same rows would sharpen the same shortcut (arXiv 2510.15990: GRPO is a conservative reweighting bounded by the base model's pretrained biases; OOD gains appear only when the target task aligns with them).
- Drift from C1 (forgetting) is where on-policy training has the best evidence (section 2A).
- Overconfidence (ECE 13.2% vs 4.1%) is where plain RLVR is worse than SFT (section 2C). The plan already has per-type temperature scaling (research_v4_levers/calibration.md, lever C2/C10) which fixes the SIZE of confidence, not the ranking.

---------------------------------------------------------------------------------------------------

## 2. Evidence

### 2A. RL vs SFT: generalization and forgetting

| Claim | Setting | Numbers | Source / tag |
|---|---|---|---|
| "SFT memorizes, RL generalizes" | Llama-3.2-Vision-11B; GeneralPoints (card arithmetic), V-IRL navigation; SFT then RL, equal compute | OOD rule variants, change from shared init: GP-L RL +3.5 (11.5 -> 15.0) vs SFT -8.1 (11.5 -> 3.4); V-IRL-L RL +11.0 (80.8 -> 91.8) vs SFT -79.5 (80.8 -> 1.3); V-IRL-VL RL +9.3 vs SFT -33.2; visual GP-VL RL +17.6 vs SFT -9.9 | arXiv 2501.17161v2 (ICML 2025) [author-run], https://arxiv.org/html/2501.17161v2 |
| SFT is needed first, and RL cannot rescue a bad SFT | same | End-to-end RL without SFT fails to improve on GP-L (format not followed); RL cannot recover OOD from an over-fit SFT checkpoint (collapses to the training rule); RL is less effective from extremely under- or over-fit checkpoints | same paper |
| RL transfers, SFT forgets (teacher CoT SFT) | Qwen3-14B, math-only data, 47K problems, RL vs SFT on teacher CoT | Non-reasoning average: base 45.7, SFT-think 21.1, SFT-no-think 29.0, RL 53.2; IFEval 69.2 -> 42.3 / 41.4 (SFT) vs 70.0 (RL); HaluEval 35.7 -> 2.3 / 3.3 vs 40.7 | arXiv 2507.00432v2 (ICLR/ICML 2026) [author-run], https://arxiv.org/html/2507.00432v2 |
| The cause is on-policy data, not RL | Qwen3-8B-Base, same paper Table 4 | Transfer index to non-reasoning tasks: off-policy SFT -40.5; ON-policy SFT +30.2; off-policy RL +4.5; on-policy RL no KL +39.3; on-policy RL with KL +32.4 | same paper |
| RL forgets less because KL shift is smaller | Qwen2.5-3B-Instruct (math, science QA, tool use), OpenVLA-7B, toy MLP | KL on the new task predicts forgetting (R^2 0.71 on LLMs, 0.96 toy); on-policy GRPO and 1-0 REINFORCE reach similar new-task accuracy with smaller KL than offline SFT and SimPO; authors say on-policy data, not negative examples, drives it. Exact retention numbers only in plots | arXiv 2509.04259 "RL's Razor" (ICLR 2026) [author-run], https://arxiv.org/html/2509.04259v1 |
| GRPO changes less than SFT | OLMo-2-7B-Instruct, math | SFT degrades knowledge benchmarks more; GRPO smaller KL and smaller weight change. Confounded: lr 1e-6 (GRPO) vs 5e-5 (SFT), OLMo-2 already RLVR-trained | arXiv 2507.10616 [author-run], https://arxiv.org/html/2507.10616v1 |
| RL heals SFT forgetting but does not beat the early-SFT peak | reasoning checkpoints, ID vs OOD | OOD performance often peaks early in SFT then drops while ID keeps rising; RL "usually does not beat that early peak", it restores OOD lost to late SFT, only from a limited range of SFT checkpoints; tracks singular-vector rotation | arXiv 2509.12235 v3 [author-run], abstract only, https://arxiv.org/abs/2509.12235 |
| RLVR sharpens, it does not expand | math/code pass@k | RL wins at small k, base wins at large k; capability boundary can narrow; entropy collapse R = -a exp(H) + b | arXiv 2504.13837 (Yue et al.), arXiv 2505.22617 (Cui et al.) [author-run], via search summaries (UNVERIFIED in primary) |
| GRPO OOD gains need alignment with pretraining | from-scratch transformers | "OOD improvement emerges only when the target task aligns with the model's pretrained biases" | arXiv 2510.15990 [author-run], abstract only |
| Spurious rewards also "work" on Qwen | Qwen2.5-Math-7B, MATH-500 | RANDOM rewards +21.4 pp vs ground-truth +29.1 pp; effect model-dependent (not on Llama / OLMo) | arXiv 2506.10947 [author-run], https://arxiv.org/abs/2506.10947 |

Reading for us: the OOD benefit is credited to on-policy learning with small KL shift. For a 1-token answer, "on-policy" reduces to a weighting of the prompt (section 4), so most of the benefit can be had without rollouts or with a KL anchor to C1. UNVERIFIED that this holds on a one-token readout.

### 2B. Small-model decision / classification head-to-heads (SFT vs RL)

| Study | Model, task | SFT | RL | Notes |
|---|---|---|---|---|
| Yaldiz et al., arXiv 2601.13284 [author-run] https://arxiv.org/html/2601.13284v1 | Qwen3-1.7B/4B/8B; CommonsenseQA and OpenAI Moderation (in-domain), OpenBookQA and XSTest (OOD); 500 train rows per dataset | answer-only SFT (LoRA r16, 5 epochs, lr 2e-4): mean acc 83.2 | GRPO with 256-token CoT, binary reward, G likely 32, LoRA, lr 1e-3, 20 epochs: mean acc 86.0 | At 4B, GRPO - SFT accuracy: CSQA +2.72, OBQA (OOD) +2.99, Moderation +1.44, XSTest (OOD) +1.56. OOD average over sizes: SFT 85.0, GRPO 87.9. Caveats: best checkpoint chosen on the test set (paper says so), 500 SFT rows is a weak SFT baseline |
| JudgeLRM, arXiv 2504.00050v3 [author-run] https://arxiv.org/html/2504.00050v3 | Qwen2.5-3B / 7B pairwise judge; JudgeLM (in-dist) and PandaLM (OOD); 100K train, GRPO, 4-8 A100 | 3B F1 75.05 / 66.10; 7B 83.06 / 67.98 | 3B 84.61 / 72.12; 7B 84.73 / 75.05 | RL minus SFT: 3B +9.6 / +6.0; 7B +1.7 / +7.1 (F1, JudgeLM / PandaLM). Reasoning (CoT) judge |
| StepGuard, arXiv 2608.24777 [author-run] https://arxiv.org/html/2608.24777 | Qwen3-4B-Instruct agent-action guard; 3K SFT then 4K GRPO | acc 79.7, F1 81.0, safe-unsafe gap 21.8 | GRPO acc 81.5 (gap 13.0); Balance-GRPO acc 82.2, F1 82.1 (gap 8.0) | OOD set of 100 human-verified traces: SFT 67.0, GRPO 75.0, Balance-GRPO 82.0 (n = 100, so wide CI). Data authored by GPT-5.4 (barred for us); output is a structured diagnosis, not one token. Also [project] research_v3/recipe.md:27 |
| eXTC, arXiv 2605.29076v2 [author-run] https://arxiv.org/html/2605.29076v2 | Qwen3-4B text classification (legal NLI, peer review, clinical readmission) | classification-head SFT macro-F1 0.847 / 0.825 / 0.609 | BD-GRPO 0.849 / 0.825 / 0.652 | Essentially a tie on two of three datasets. At G = 8 only about 21.9% of examples had mixed rollouts on ICLR Review (zero-advantage waste); per-class sampling needed, dropping it collapses MIMIC |
| Reasoning-judge GuardReasoner family [project] research_v3/recipe.md:36 | Llama 1B/3B/8B guard | R-SFT | + HS-DPO | HS-DPO added +0.97 / +0.67 / +0.70 average F1 at 1B/3B/8B (full-parameter, generative reasoning); hard pairs come from the model's own samples. Verified by project refuter 18 Oct |

Net: RL after SFT beats SFT by +1.4 to +3.0 pp at 4B on short-decision tasks with CoT (Yaldiz, StepGuard), up to +6-7 pp OOD in judges (JudgeLRM), and ties on label-only classification (eXTC). Every one of these used reasoning output; none is a one-token readout. The SFT baselines are weak or small. Treat +1.5 pp as the optimistic centre, not a promise.

### 2C. Calibration

| Claim | Numbers | Source / tag |
|---|---|---|
| Binary RLVR is overconfident; SFT is better calibrated | ECE (points), 12 cells, mean: Base 18.2, SFT 6.3, GRPO 13.3, GRPO + decision-token CE term ("Ours") 8.5. At 4B: SFT 6.8, GRPO 11.7, Ours 7.7. GRPO ECE > SFT ECE in 12/12 cells. OOD (OBQA, XSTest, all sizes): SFT 6.8, GRPO 11.5, Ours 6.6; OOD accuracy SFT 85.0, GRPO 87.9, Ours 89.0. Mechanism claimed: the decision token is an "extraction step" that carries no confidence | arXiv 2601.13284 [author-run], Table 4 (means computed by me from the table) |
| Brier-in-the-reward fixes calibration (verbalized confidence) | Qwen2.5-7B. HotpotQA-trained: RLVR ID acc 63.0 / ECE 0.37, OOD acc 53.9 / ECE 0.46 (base OOD ECE 0.40); RLCR ID acc 62.1 / ECE 0.03, OOD acc 56.2 / ECE 0.21. Math-trained: RLVR ECE 0.26 ID, 0.49 OOD (base 0.45); RLCR 0.10 ID, 0.25 OOD; SFT + RLCR ID ECE 0.08 but OOD accuracy 43.8 (base 47.8, RLCR 50.9) | arXiv 2507.16806 (ICLR 2026) [author-run], https://arxiv.org/html/2507.16806, as extracted; reward = 1[correct] - (q - 1[correct])^2 |
| Calibration regulariser helps in-domain, OOD gap persists | Qwen2.5-3B K&K logic: GRPO ECE 0.497, Brier 0.405; C2GSPG ECE 0.126, Brier 0.136; Qwen2.5-Math-1.5B math: GRPO ECE 0.501 -> 0.464-0.491 only ("calibration gap between train and test remains relatively large", distribution shift) | arXiv 2509.23129 [author-run], https://arxiv.org/html/2509.23129v1, as extracted |
| RLHF/PPO degrades calibration | Llama3-8B, Mistral-7B: vanilla PPO raises ECE vs SFT while accuracy rises; PPO-M / PPO-C lower ECE | arXiv 2410.09724 (ICLR 2025) [author-run]; numbers not read |
| DPO tends to overconfidence | DPO-aligned Llama3.1-8B overconfident; relative loss leaves absolute probability scale unconstrained | arXiv 2505.01997, arXiv 2601.23096 [author-run], search summaries (UNVERIFIED in primary) |
| Grading that gives no credit for abstaining pushes guessing | Of 10 mainstream benchmarks, 9 give no credit for abstention | Kalai et al., arXiv 2509.04664 [author-run], via summaries |

Project-side calibration context: Jev's independently measured ECE is 0.033 (typed decisions) [project] research_v4_levers/calibration.md (finding 1), so "better calibrated than Jev" needs about 2.5% or lower under the same protocol; a 0/1-reward stage moves the wrong way.

### 2D. Abstention and reward hacking (small models)

| Finding | Numbers | Source / tag |
|---|---|---|
| Ternary reward (+1 correct, abstain r, -1 wrong) on 2B-4B models | Qwen-3-4B MedMCQA (about 100 test rows): base 67.5% correct / 32.5% wrong; RL-only r_abs = 0.3: 48.0 / 10.3 / 41.0% IDK. Granite-3.3-2B: r_abs 0.3 gives 100% IDK; r_abs 0 gives 78% IDK. RL-only did NOT induce abstention on open-ended MATH (base model never says IDK); SFT warm-up did, with accuracy 49.6 -> 35.0. Recipe: TRL GRPOTrainer, vLLM colocate, G = 8, 500 steps, LoRA lr 2e-5, A40/A100, about 24 h per run (1024-token completions) | arXiv 2601.20126 [author-run], https://arxiv.org/html/2601.20126 |
| Penalty lambda sweeps a Pareto frontier; large lambda collapses | Qwen3-1.7B Dr.GRPO on Knights and Knaves (80K): lambda 0 -> 15% wrong, about 0 abstain; lambda 1 -> under 2% wrong, about 60% abstain on hard items, 10% on easy; lambda 10: transient spike to about 90% abstain on easy items near step 80; lambda 20 -> near-universal abstention. Frontier models abstain under 1% with errors above 10% | arXiv 2511.11500 [author-run], https://arxiv.org/html/2511.11500v2 |
| A tiny static refusal reward can be catastrophic | Qwen2.5-7B-Instruct search agent: from-scratch RL with r_ref = 0.05 gives 99.9% refusal, accuracy 0. Cold-start (SFT first) r_ref 0.2: refuse 23.9%, precision 0.649 (0.559 at r = 0), accuracy 0.488 (0.552) | arXiv 2607.10738 [author-run], https://arxiv.org/html/2607.10738 |
| Reasoning RL degrades abstention and raises tool hallucination | "reasoning fine-tuning degrades abstention (by 24% on average)" (relative or points not stated, 20 datasets); RL on non-tool math raises later tool hallucination; DPO fix costs utility | arXiv 2506.09038 (NeurIPS 2025) abstract; arXiv 2510.22977 (ACL 2026) via summary |
| Binary-reward GRPO has no credit for declining | Chow rule: with R_incorrect = 0 abstain iff p < R_abstain / R_correct | arXiv 2609.17686 (position paper) |

Lesson: abstention under RL is learnable but fragile. It needs the ternary reward AND an SFT or cold-start that already shows the behaviour, and the abstain reward must stay small. This is the same trap as C2's over-use of "Cannot be determined" (C2 learned an abstain-like label as a prior). Training a threshold on a calibrated probability is the safer route and is already in the plan (ASK band, coverage-vs-error curve).

### 2E. LoRA is fine for RL

"LoRA Without Regret" (Thinking Machines, Sep 2025) [vendor blog, not peer reviewed], https://thinkingmachines.ai/blog/lora/: LoRA matches full fine-tuning in RL "even with ranks as low as 1" (Llama-3.1-8B GSM8K / MATH; Qwen3-8B-Base DeepMath); optimal LoRA lr about 10x the full-FT lr; argument: policy gradient absorbs about O(1) bit per episode, so 320,000 bits (MATH: 10,000 problems x 32 samples) is far below rank-1 capacity (about 3M parameters). An independent small replication (Qwen3-0.6B, rank 1) found full FT pulls ahead (UNVERIFIED, search summary). For us: 10-30K prompts x G = 8 is at most 240K episodes, so r16 LoRA is not capacity-limited.

---------------------------------------------------------------------------------------------------

## 3. What the evidence says for each candidate method (our setting: 4B, no CoT, 1-token readout, program gold)

| Method | OOD transfer | Calibration | Abstention | Verdict |
|---|---|---|---|---|
| SFT only (cross-entropy, current) | the baseline; C2 -4.8 pp; best OOD is early in training (2509.12235) so use snapshot / alpha / gamma grid | CE overconfident after fine-tuning (C2 ECE 13.2%), fixable in level by per-type T | trained ASK classes only where gold exists | keep as the main run |
| GRPO / RLOO, 0/1 reward, sampled | maybe +1.4 to +3 pp (CoT evidence); not shown for 1-token | WORSE: +2.0 to +8.2 ECE points at 4B (Yaldiz) | no credit for abstain | not recommended |
| GRPO, Brier / ternary reward | RLCR: OOD acc +2.3 vs RLVR (HotpotQA); gains in OOD ECE partial | ID ECE 0.03; OOD 0.21 | collapse risk if abstain reward too high (AWA-RL, RH) | only if the owner wants true RL; cost section 6 |
| Exact-expectation on-policy stage (no rollouts) | same mechanism as on-policy RL with no sampling noise; UNVERIFIED for OOD | proper-scoring term keeps it honest | via ternary matrix, same collapse risk | cheapest RL-like option |
| DPO / ORPO from program gold | offline: forgets like SFT (RL's Razor: SimPO), no exploration | pushes confidence up | none | stays NOT ADOPTED |

---------------------------------------------------------------------------------------------------

## 4. The one-token structure (DERIVED; algebra, but untested on our model)

Let pi(a) be the restricted softmax over the K option tokens at the answer position (exactly the readout the plan uses), g the gold option, reward r(a) = 1[a = g].

1. Exact policy gradient. E_{a~pi}[r(a)] = pi(g) = p. Its gradient is p x grad log p. A sampled GRPO / RLOO estimator with G rollouts is a noisy Monte Carlo estimate of this same quantity. With K <= ~10 options there is nothing to explore and no reason to sample. The exact version needs one forward pass per prompt and zero rollouts.
2. This loss is the "-p" objective of Li et al. (arXiv 2510.00526, ICML 2026): it down-weights examples the model currently gets wrong (low p), is better than NLL when the model's prior is strong and worse when it is weak (math, strong prior: Qwen2.5-Math-7B 22.67 -> 36.51; weak prior: exact match 35.20 -> 0.00 on Qwen2.5-7B figfont). Calibration of -p-trained models was NOT measured there; the authors say prior-leaning objectives reinforce confident predictions. Also in expectation it equals rejection-sampling fine-tuning (train only on correct self-samples).
3. Brier identity. Brier(pi, g) = sum_a (pi(a) - 1[a = g])^2 = 1 - 2 pi(g) + sum_a pi(a)^2. So minimizing Brier = maximizing 2 x (expected 0/1 reward) minus the collision probability sum_a pi(a)^2. The second term is the anti-sharpening penalty that a plain 0/1 reward lacks. This is why a proper-scoring reward (RLCR's 1[correct] - (q - 1[correct])^2 is the same idea with a stated confidence q) repairs the overconfidence of 0/1 RLVR, and why a 0/1 reward is minimized by a one-hot policy (not proper).
4. Ternary reward and abstention. With reward 1 (correct), rho (abstain), -lambda (wrong): answer iff p > (rho + lambda) / (1 + lambda). Example: rho = 0, lambda = 1 gives 0.5; lambda = 4 gives 0.8. This is the Chow rule; a calibrated model plus a threshold reproduces it with no training, which is what the plan's ASK band does.
5. Zero-advantage waste disappears. In sampled GRPO a group where all G rollouts are the same option has zero gradient. With exact expectation every non-one-hot prompt contributes (weight p(1-p) on the logit of the gold option).

Consequence: for this task shape, "RL vs SFT" is mostly "which loss on the option distribution, and with what anchor". That is cheap to test, but it is also why the RL-generalizes literature (CoT exploration) transfers weakly.

---------------------------------------------------------------------------------------------------

## 5. Reward-hacking and failure risks (for any RL stage on program gold)

1. Sharpening / overconfidence with 0/1 reward (2601.13284: 12/12 cells; 2507.16806: RLVR OOD ECE worse than base). Mitigation: proper-scoring term, per-type T after, ECE and Brier as selection terms.
2. Label-prior collapse: rollouts agree, small / imbalanced label space (2605.29076); Balance-GRPO class reweighting closed a 13.0-point safe/unsafe gap to 8.0 (2608.24777). Our analogue: "Cannot be determined" frequency. Mitigation: per-class balanced prompt sampling; report per-class recall (C2's Compliant recall fell 30.8 -> 7.7%).
3. Abstain hacking: 0.05 static reward -> 99.9% refusal from scratch (2607.10738); lambda 20 collapse (2511.11500); Granite r_abs 0.3 -> 100% IDK (2601.20126). Mitigation: no abstain reward on determinate items, cold-start from an SFT that already abstains sensibly, hard cap on abstain share per family, monitor per step.
4. Shortcut exploitation of program-generator artifacts: RL optimizes exactly what the reward admits. Mitigation: held-out families and minimal pairs from the plan; add a NEGATIVE-CONTROL arm with shuffled gold (cheap in the exact version, about $2), motivated by arXiv 2506.10947 where random rewards gave 74% of the real gain on Qwen2.5-Math-7B.
5. Entropy collapse (2505.22617): in TRL set a logged entropy floor (entropy_coef or stop when the option-distribution entropy on dev falls below C1's), and stop on dev ECE, not on training reward.
6. Train / inference mismatch (sampled GRPO with vLLM vs HF kernels): TRL applies an importance-sampling correction by default (`vllm_importance_sampling_correction=True`, clip max 3.0; mode default is shown inconsistently in the docs) [TRL docs]. Not needed in the exact version (no vLLM).
7. Checkpoint selection leakage: Yaldiz selected the best checkpoint on the test set. Our rule (never train or select on test / sealed) applies; select on mixdev and transfer dev only, pre-registered.
8. Serving parity: any RL stage output must be merged and re-checked against the S1 argmax parity bar (99.5%) before use (plan section 6).

---------------------------------------------------------------------------------------------------

## 6. Cost and time on Modal H100 (DERIVED from C2's measured numbers)

Inputs [project]:
- C2 trained 59,340 rows in 186.0 min = 0.188 s/row = 5.32 rows/s for forward + backward + gradient checkpointing on one H100 at $13.14 ($4.24/h effective; the ledger uses $4.09/h wall; Modal list price is $0.001097/s = $3.95/h, https://modal.com/pricing and train/modal_od_c2.py:580). Sources: c2_build/C2_REPORT.md:15,44,47; train/README.md:26.
- That per-row time includes C2's row-length mix (replay plus new families; the plan says block-R rows average up to 800 tokens and the cap is 1,536, C2_1_PLAN_v3.md:972-975 and :919 (row cap in the LoRA block)). If RL prompts are shorter or longer, cost scales roughly with tokens: treat every dollar below as +/- 2x.
- Stack already in use: transformers 5.x, fla-core / flash-linear-attention 0.5.2, Qwen3.5-4B has 24 linear-attention + 8 full-attention layers (train/modal_od_c2.py:43-51; C2_1_PLAN_v3.md:915-916).

| Option | Sequences trained | Time (1 H100) | $ (4.24/h) | Notes |
|---|---|---|---|---|
| A. exact-expectation, 10K prompts, 1 pass | 10K | 31 min | 2.2 | custom loss in existing trainer, no vLLM |
| A. 20K prompts | 20K | 63 min | 4.4 | |
| A. 30K prompts | 30K | 94 min | 6.6 | 2 passes = 13 |
| A. pilot, 2K prompts | 2K | 6 min | 0.44 | |
| B. TRL GRPO, 10K prompts, G = 4, beta = 0 | 40K | 2.1 h | 8.9 | + rollouts and weight sync (UNVERIFIED, minutes) |
| B. 10K prompts, G = 8, beta = 0 | 80K | 4.2 h | 17.7 | |
| B. 20K prompts, G = 8 | 160K | 8.4 h | 35.4 | |
| B. 30K prompts, G = 4 | 120K | 6.3 h | 26.6 | |
| B. 30K prompts, G = 8, beta = 0 | 240K | 12.5 h | 53 | with KL reference forward (LoRA adapter off) about +25%: 66 (UNVERIFIED factor) |
| Screening pass (forward only, keep p(gold) in [0.05, 0.95]) | 30K | 24 min | 1.7 | forward-only is about 1/4 of fwd + bwd with checkpointing (DERIVED); cuts zero-advantage waste for B |

Why B is G times A: TRL trains each (prompt, completion) as a separate sequence; the G completions share the prompt but I found no prompt-prefix sharing in the training pass (UNVERIFIED). Rollout generation itself is nearly free for 1-token answers (prefill only). Reference model: TRL `beta` default is 0.0 and then the reference model is not loaded (TRL docs), which saves the extra forward.

Reality check from a published run: Jha et al. needed about 24 h per run for 500 steps, G = 8, about 8K prompts, 1024-token completions on A40 / A100 (arXiv 2601.20126). Our 1-token completions are far cheaper, which is why B is hours, not days.

Budget fit [project]: C2.1 training cap $30 (R1), SFT projected $26-28 without stage B and $30-32 with it; no raise of the $30 cap (C2_1_PLAN_v3.md:1903-1906). Option A at $2-7 can be shed first or run on the Nov 1 credit; option B at $18-66 cannot be paid from R1 unless the SFT mix shrinks or the owner adds the optional $10-15.

Project observation to check (outside this question, but it moves the budget): C2 trained ONE pass (epochs 0.9901, C2_REPORT.md:44) at $13.14 for 59,340 rows = $0.221 per 1K rows per pass; the plan quotes "$0.23-0.25 per 1K rows at 2 epochs" (C2_1_PLAN_v3.md:969) and "Epochs: 2 over the mix" (C2_1_PLAN_v3.md:919). If the per-row figure is per pass, a 2-epoch C2.1 on about 112.5K rows would be about $52-56, above the $30 cap; if the $26-28 is the 2-epoch figure, C2's per-row cost does not match. The measured-s/step rule on Mon 26 Oct will settle it; I did not resolve it.

Engineering and stack risk for B on Qwen3.5-4B (hybrid Gated DeltaNet):
- vLLM: 0.17.0 release notes list "Full support for the Qwen3.5 model family (#34110) featuring GDN" (https://newreleases.io/project/pypi/vllm/release/0.17.0); a 0.17.1 fix for freed SSM cache blocks is mentioned in a search summary (UNVERIFIED). Unsloth's Qwen3.5 page still says vLLM fast inference is not supported and to use `fast_inference=False` (https://unsloth.ai/docs/models/qwen3.5/fine-tune), probably written against vLLM 0.16.0.
- TRL: docs list Qwen3.5 as a supported model "tested with Qwen3.5-2B" (https://huggingface.co/docs/trl/main/en/grpo_trainer). I found no report of GRPO + vLLM colocate + LoRA + Qwen3.5-4B working end to end (UNVERIFIED). TRL also offers `use_transformers_continuous_batching` (needs transformers >= 5.8.0) as a vLLM-free generator (UNVERIFIED for GDN).
- Any debugging on Modal is itself billable (about $0.44 per 2,000-row pilot at C2's rate). CPU tests cannot cover a vLLM + GDN path.

Time to first result: A can be coded and unit-tested on CPU before the data freeze (about 30 Oct - 2 Nov), pilot on 2K prompts for under $0.50 inside GO #1, and read on dev for about $0.4 per candidate (C2 read 19 models in one H100 job for $7.49, C2_REPORT.md:17). B adds a 1-2 day stack bring-up.

---------------------------------------------------------------------------------------------------

## 7. Simplest viable recipe

### 7A. Recommended if the owner wants an RL-like stage at all: "exact on-policy stage" (cost $2-7)

- Start point: the chosen C2.1 SFT candidate (alpha / gamma blended; pick the early-OOD-peak snapshot, not the last step; 2509.12235). Same Qwen3.5-4B base, new r16 LoRA on top of the merged weights, same target modules as C2 (all-layer MLP plus C2's attention set), then delta-scale and merge as in the plan's gamma arm.
- Prompts: 10-20K train-split rows only, never test / sealed / Jev output. Balanced per class and per family. Pre-screen with a forward-only pass; keep rows with p(gold) in [0.05, 0.95]; keep a fixed share of already-correct rows and of replay (anchor).
- Loss on the restricted option softmax pi (all computed from one forward pass):
  L = w_acc x (-sum_a pi(a) x r(a))  +  w_cal x Brier(pi, gold)  +  beta x KL(pi || pi_ref)
  with r = 1 for gold, -lambda for a wrong determinate option, and no abstain reward on determinate rows (rho only where the program says "undeterminable"). pi_ref = C1 on a replay share (matches the KD-0.5 already used on replay in C2, C2_REPORT.md:44), the SFT candidate elsewhere. Start: w_acc 1, w_cal 1, beta 0.05-0.2, lambda 1. These values are guesses (UNVERIFIED); fix them before any read.
- Optimizer: lr 1e-5 to 2e-5 for r16 LoRA (LoRA lr about 10x full-FT RL lr of 1e-6, per TRL default and Thinking Machines; Jha used 2e-5), cosine, batch 32-64, one pass, 5 snapshots.
- Arms (each about $2-7 plus $0.4 dev read): (1) the loss above; (2) negative control with shuffled gold; (3) -p only without Brier, to see the calibration cost. Reading three arms costs about $10-20; do arm 1 first and the others only if arm 1 moves anything.
- Selection on mixdev and transfer dev only, pre-registered; report ECE after per-type T, Brier, AURC, abstain share on determinate items, per-class recall, flip rate.

### 7B. If true sampled GRPO is wanted anyway (multi-token tool / agent decisions later, C3)

- Library: TRL GRPOTrainer (https://huggingface.co/docs/trl/main/en/grpo_trainer) with `peft_config` r16 and vLLM colocate; alternatives verl, OpenRLHF, Unsloth (see stack risk above).
- Settings: `num_generations` 8 (TRL default; 4 if cost binds), `max_completion_length` 2-8 with a constrained or masked first token (reward -lambda for a non-option token), `temperature` 1.0, `beta` 0.0 (default; Huan et al. found on-policy RL without KL transfers as well as with KL, +39.3 vs +32.4 non-reasoning TI) or 0.001-0.04 if drift shows, `scale_rewards` False (Dr. GRPO: std scaling adds a question-level difficulty bias), `loss_type` dapo or dr_grpo, `epsilon_high` 0.28 (DAPO), `learning_rate` 1e-5 to 2e-5 (LoRA), `num_iterations` 1, `vllm_importance_sampling_correction` True (default; the docs page shows mode default `sequence_mask` in one place and `token_truncate` in another, check the installed version), `mask_truncated_completions` irrelevant.
- Reward: custom function from the program gold; for calibration use the Brier shape on the policy's own option probability (needs a custom loss term, since a sampled reward only sees the chosen option); multi-reward via TRL's "normalize_then_sum" aggregation option (GDPO; exact parameter name UNVERIFIED, check the GRPOConfig page).
- Data: dynamic sampling / pre-screen to drop zero-variance groups (DAPO name; eXTC: only about 21.9% of examples mixed at G = 8), per-class balanced sampling.
- Steps: 300-500 steps of 64-128 prompts x G (Jha: 500 steps, 64 prompts x 8 per step). 10-30K prompts with 1-3 epochs.
- Stop: dev ECE after T, entropy floor, abstain share cap, parity.

### 7C. DPO from program gold (not recommended; cost similar to A)

Pairs (chosen = gold, rejected = a wrong option the model itself ranks highest) are one position, so DPO is a pairwise logistic on the option logits and costs about one SFT pass. It is offline (SimPO behaved like SFT in RL's Razor), gives no calibration control, and DPO-trained models are documented as overconfident (UNVERIFIED primaries). GuardReasoner's +0.67 to +0.97 F1 came from generative reasoning outputs sampled from the model [project, research_v3/recipe.md:36], which a one-token readout lacks.

---------------------------------------------------------------------------------------------------

## 8. Expected effect vs the best SFT-only candidate (DERIVED ranges, to be measured, not promised)

| Metric | 7A exact stage, proper-scoring | 7B sampled GRPO, 0/1 reward | 7B sampled GRPO, Brier / ternary |
|---|---|---|---|
| Trained-family dev | 0 to +1.0 pp | +1 to +3 pp (CoT evidence, optimistic) | +1 to +2 pp |
| Transfer to unseen families | 0 to +2 pp (mostly by staying near C1) | 0 to +2 pp | 0 to +2 pp |
| T19-type label-prior collapse | not fixed unless the data fixes it | sharpened if present | not fixed |
| ECE after per-type T | within +/- 0.5 pt | +2 to +8 pts worse before T; after T the gap shrinks (T fixes size) | neutral to -1 pt |
| Abstain share | controlled by rho / lambda | none | collapse risk if rho too high |

The honest reading: the only cheap, evidence-backed gains for the C2 failure modes are (a) choosing the early OOD-peak snapshot and delta-scale (already in the plan), (b) fixing the label prior in the data, (c) per-type temperature. An RL-like stage is a small add-on whose best case is an extra +1-2 pp, and whose worst case is a calibration regression.

---------------------------------------------------------------------------------------------------

## 9. What I could not verify / caveats

- No paper found for RLVR without CoT on 1-token option decisions (3 searches, incl. extended). All RL-beats-SFT numbers above are CoT RL. UNVERIFIED that they transfer.
- Yaldiz et al. (the closest analogue) selected the best checkpoint on the test set (their own statement), used a 500-row SFT baseline and a CoT GRPO with G likely 32; ECE bin count not stated. Direction (GRPO ECE > SFT ECE in all cells) is large enough to survive that, magnitudes are not clean.
- Table numbers for RLCR, C2GSPG and JudgeLRM are "as extracted" by the fetch tool from arXiv HTML; the RLCR Answer-Probability row had a layout artifact (not used here). PDFs were unreadable (binary); two PDFs auto-saved under ~/.claude were not opened (hard rule).
- Search summaries I did NOT rely on: a claim that "exact policy gradient loses to cross-entropy" (the cited paper, arXiv 2603.14608 "Delightful Policy Gradient", says nothing like it); DPO calibration papers (2505.01997, 2601.23096) are search-summary only; Yue and Cui papers are search-summary only; independent LoRA-rank-1 replication is search-summary only.
- AbstentionBench's "24%" is not stated as relative or absolute in the abstract.
- Cost table assumes RL prompts have C2's average row length and that sequence cost is linear in rows; training-pass prefix sharing, vLLM weight-sync time, and the +25% reference-forward factor are my estimates (UNVERIFIED). Measure s/row on the 2K-prompt pilot before any commitment, as the plan's own MONEY rule requires (C2_1_PLAN_v3.md:1903-1906).
- ECE 13.2% vs 4.1% and the T19 76/98 figures come from the task statement, not re-read from the project files.
- C3 (RL with sandbox rewards) remains NOT ADOPTED for C2.1 in the plan (C2_1_PLAN_v3.md:1063).

---------------------------------------------------------------------------------------------------

## 10. Sources

Papers (arXiv): 2501.17161 (SFT memorizes, RL generalizes); 2507.00432 (math reasoning transfer, on-policy); 2509.04259 (RL's Razor); 2507.10616 (Scalpel vs Hammer); 2509.12235 (RL heals OOD forgetting in SFT); 2510.15990 (can GRPO transcend pretraining); 2504.13837, 2505.22617 (RL sharpening, entropy); 2506.10947 (spurious rewards); 2601.13284 (calibration-aware RL, decision tasks); 2507.16806 (RLCR); 2509.23129 (C2GSPG); 2410.09724 (PPO-M/PPO-C); 2505.01997, 2601.23096 (DPO calibration); 2504.00050 (JudgeLRM); 2608.24777 (StepGuard); 2605.29076 (eXTC); 2601.20126 (intellectual humility RLVR); 2511.11500 (Reinforced Hesitation); 2607.10738 (AWA-RL); 2506.09038 (AbstentionBench); 2510.22977 (Reasoning Trap); 2509.04664 (Why LMs hallucinate); 2510.00526 (-p objectives); 2503.14476 (DAPO); 2503.20783 (Dr. GRPO); 2603.14608 (Delightful PG, only used to correct a summary).

Docs: https://huggingface.co/docs/trl/main/en/grpo_trainer ; https://modal.com/pricing ; https://thinkingmachines.ai/blog/lora/ ; https://unsloth.ai/docs/models/qwen3.5/fine-tune ; https://newreleases.io/project/pypi/vllm/release/0.17.0

Project files (all under /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/): C2_REPORT.md:15,17,44,47; train/README.md:26; train/modal_od_c2.py:43-51,580; zed_orch/c21/C2_1_PLAN_v3.md:78,913-919,969-975,1063-1065,1903-1906; zed_orch/c21/research_v3/recipe.md:27,36,88; zed_orch/c21/research_v4_levers/calibration.md (findings 1-2, levers C2, C6, C10, C11).
