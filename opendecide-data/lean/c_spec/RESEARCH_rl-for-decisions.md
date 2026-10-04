# RESEARCH: RL for decisions (angle: rl-for-decisions)

Date: 3 Oct 2026. Scope: web research plus one read of our own `train_decoder.py`. No GPU, no paid calls, no eval
data opened. Numbers come from the cited papers unless marked "my estimate".

## 1. Verdict (short)

- For C1's readout (one forward pass, softmax over 2-10 candidate letters, no generation), RL is NOT a different
  kind of training. It is cross-entropy with a different per-row weight. The action space is tiny and fully
  enumerable, so there is nothing to explore and nothing to sample.
- The well-known "RL generalizes" results come from setups we do not have: long generated outputs (chain of thought,
  multi-turn), frozen prompt templates, few-shot data, or noisy imitation targets. With a one-token readout, the SFT
  target IS the outcome, so "SFT memorizes the trajectory" cannot happen.
- RL-style weighting would hurt exactly where C1 is weak. It gives the smallest gradient to rows the model gets
  confidently wrong (double negation flips, hard yes/no). Cross-entropy gives those rows the largest gradient.
- RL with a vote-share reward is worse still. It pushes all mass onto the top option and throws away the human
  vote-share calibration in golden_train.
- Do NOT run GRPO, PPO or RLCR for C. Keep cross-entropy / KD as the main loss.
- Take the three ideas from RL that do transfer, at zero or near-zero cost:
  1. Stay close to the starting model (the "RL's Razor" effect). For us this is the KL anchor to C1. **Our code
     currently anchors to the frozen BASE model, not to C1 (see section 4.2). Fix this before the C run.**
  2. Train on the model's own failure zone. Use C1 to pick and audit program-labelled rows (section 4.4).
  3. Pick checkpoints on out-of-domain data, and soften weights (step B). Long SFT erodes OOD skill early.
- An optional pilot (one extra arm, about $9-11) can test the exact RL-equivalent weighting. My expected gain is
  about zero, so run it only if the budget is spare (section 5).

## 2. Why RL equals re-weighted cross-entropy for our readout

Setup: logits z over K candidate tokens, p = softmax(z), gold index g, p_g = probability on gold.

| Objective (per row) | Gradient on logits (ascent) | Weight vs cross-entropy |
|---|---|---|
| Cross-entropy, log p_g (= log-score reward) | e_g - p | 1 |
| Expected 0/1 reward, E[r] = p_g (REINFORCE, exact) | p_g (e_g - p) | p_g |
| GRPO, binary reward, infinite group, no clip/KL | (e_g - p) * sqrt(p_g / (1 - p_g)) | sqrt(p_g / (1 - p_g)) |
| DFT (SFT loss times stopgrad(p)) | p_g (e_g - p) | p_g (same as expected reward) |
| One-Token Rollout, reward +1 gold / c others, in expectation | (1 - c) p_g (e_g - p) | (1 - c) p_g |

Derivations (standard, checked by hand):
- E_a~p[r(a)] = p_g, and d p_g / d z = p_g (e_g - p). So exact REINFORCE = cross-entropy scaled by p_g.
- GRPO normalizes the advantage by the group std sqrt(p(1-p)). Its expected gradient is grad p_g / sqrt(p_g(1-p_g)),
  which is the gradient of 2 * arcsin(sqrt(p_g)). This matches the weight sqrt((1-p)/p) per success shown in
  arXiv 2503.06639.
- MaxRL (arXiv 2602.02710) states it plainly: RL with binary reward optimizes p; maximum likelihood optimizes log p,
  whose gradient is (1/p) grad p.

What the weights mean (computed values):

| p_g (model's prob on gold) | CE weight | Expected-reward / DFT weight | GRPO weight | Share of G=8 groups with zero signal | G=16 |
|---|---|---|---|---|---|
| 0.01 (confidently wrong) | 1 | 0.01 | 0.10 | 92% | 85% |
| 0.10 | 1 | 0.10 | 0.33 | 43% | 19% |
| 0.50 | 1 | 0.50 | 1.00 | 1% | 0% |
| 0.90 | 1 | 0.90 | 3.00 | 43% | 19% |
| 0.99 (already right) | 1 | 0.99 | 9.95 | 92% | 85% |

Plain reading:
- RL spends its gradient on rows the model nearly has. Cross-entropy spends it on rows the model gets badly wrong.
- C1's known weak spots (double-negation flips 8.9%, JevBench hard yes/no 47.4) are confident errors. RL weights
  them 3x to 100x less than cross-entropy.
- Sampled GRPO also wastes most groups: at p_g = 0.01 or 0.99, 92% of 8-sample groups give zero gradient.
- With exact expectation (we can enumerate all K letters), sampling adds only noise. "On-policy" changes nothing,
  because there is no generated prefix for the policy to visit.

Soft targets (our human vote shares). Reward r_k = v_k gives the gradient p_k (v_k - sum_j p_j v_j). Its optimum
puts all mass on argmax v. It is mode-seeking and miscalibrated by design. Cross-entropy with target v has gradient
v - p, and its optimum is p = v. So RL on vote shares would undo the KD calibration we paid for.

Calibration rewards. Log score and Brier score on the output distribution are proper scoring rules. Our output
distribution is a deterministic, differentiable function of the logits, so these "rewards" are just losses. The log
score IS our cross-entropy. RLCR-style RL is needed only when confidence is spoken as generated text after reasoning.
We read probabilities straight from logits, so we do not need it.

Label noise. Expected-reward loss is 1 - p_g, the MAE loss. MAE is known to be robust to noisy labels but to
underfit badly: 38.29% on CIFAR-100 after 2,000 epochs in the GCE paper (Zhang and Sabuncu, NeurIPS 2018).
Program-labelled rows have no label noise, so we do not need this robustness there. Crowd rows already use soft
vote-share targets.

## 3. What the literature says (with numbers)

### 3.1 "SFT memorizes, RL generalizes" and follow-ups

- Chu et al., ICML 2025 (arXiv 2501.17161). Llama-3.2-Vision-11B, multi-turn, outcome reward, generated reasoning.
  OOD rule variants: GeneralPoints-text RL +3.5 (11.5 -> 15.0), SFT -8.1 (11.5 -> 3.4). V-IRL-text RL +11.0
  (80.8 -> 91.8), SFT -79.5 (80.8 -> 1.3). They also found SFT is needed first so RL gets a stable output format.
  Our setup differs: one token out, no reasoning text, very varied prompts.
- Lin et al., "Debunk the Myth of SFT Generalization" (arXiv 2510.00237). SFT failure comes mostly from frozen
  prompts. Sokoban unseen instruction variants (Qwen2.5-7B): frozen-prompt SFT near 0; SFT with prompt diversity
  0.92 / 0.89 / 0.84; RL 0.76 / 0.69 / 0.55. Prompt diversity plus CoT beat RL on harder variants too (0.40 vs 0.10
  on complex Sokoban, Qwen). Our "format variety" plan item is the right fix. It is SFT-side and costs nothing extra.
- "RL Fine-Tuning Heals OOD Forgetting in SFT" (arXiv 2509.12235). OOD skill peaks early in SFT (checkpoint ~140 for
  Llama-3.2-11B, ~120 for Qwen-2.5-7B) and then falls while in-domain loss keeps improving. RL mainly restores that
  lost skill. It does not add new skill. Singular values stay fixed; singular vectors rotate. Lesson for us: pick C's
  checkpoint on out-of-domain data, not on in-domain loss. This is consistent with C1's dev gain not reaching ejs-5.

### 3.2 Forgetting is about distance from the start model, not about RL

- "RL's Razor" (Shenfeld, Pari, Agrawal; arXiv 2509.04259). Qwen2.5-3B-Instruct on math, science QA and tool use;
  OpenVLA-7B; an MNIST toy. Forward KL to the base model on the new task predicts forgetting (quadratic fit
  R^2 = 0.96 on the toy). On-policy methods (GRPO and plain 1-0 REINFORCE) reach the same task score at much smaller
  KL than offline SFT or SimPO. Key fact: **SFT on the KL-minimal "oracle" target forgot even less than RL.** The
  target distribution matters, not the algorithm.
- "Does Math Reasoning Improve General LLM Capabilities?" (arXiv 2507.00432). Over 20 models checked. On Qwen3-14B,
  RL-tuned models transfer to other domains; SFT-tuned ones often lose general skill. SFT shows larger KL and
  latent drift.
- On-policy distillation (Thinking Machines blog, Oct 2025). Qwen3-8B AIME'24: 74.4% with 1,800 GPU-hours vs RL
  67.6% with 17,920 GPU-hours. Using the original model as teacher recovered instruction-following lost after
  document fine-tuning. For a one-token readout, on-policy distillation from C1 equals a plain KL anchor to C1
  (no student-generated prefix exists).
- WiSE-FT (Wortsman et al., CVPR 2022, arXiv 2109.01903). Interpolating fine-tuned and starting weights gave +4 to
  +6 pp under distribution shift, +1.6 pp in-distribution, and +2 to +23 pp on six more shifts. This is the
  weight-space version of "stay close". It backs our step B weight-softening.

### 3.3 RL on classification tasks

- CLS-RL / No-Thinking-RL (arXiv 2503.16188). Qwen2-VL-2B, 4-shot image classification, 11 datasets. Zero-shot
  62.21, SFT 70.65, thinking RL 81.25, no-thinking RL 84.39. Time on ImageNet: SFT 35 min, no-thinking RL 94 min,
  thinking RL 1,587 min. Caveat: 4-shot data. SFT overfits hard in that regime, and the output is a multi-token class
  name. We train on 500K+ rows. Positive lesson: when RL is used for classification, skip the thinking.
- GTA (arXiv 2509.12108). Text classification, Qwen3-4B, answer after a short think. Accuracy SFT vs GRPO: SST-5
  61.67 vs 59.28; MASSIVE 92.57 vs 90.55; Emotion 92.20 vs 84.55; BBC News 97.70 vs 94.90. Mean: SFT 86.0,
  GRPO 82.3 (-3.7). SFT+GRPO hybrid 86.4 (+0.4 over SFT), with extra generated tokens at inference. GRPO converged
  slower even at 10,000 steps (16 rollouts per prompt, 4x L40S nodes).
- Calibration-aware RL for decision LLMs (arXiv 2601.13284). Qwen3-4B; GRPO with reasoning vs answer-only SFT.
  Mean of 4 sets: accuracy SFT 85.7, GRPO 87.9 (+2.2); ECE SFT 6.8, GRPO 11.7 (+4.9, worse). The decision token after
  reasoning carries almost no confidence; probabilities sit near 1. The +2.2 includes the effect of reasoning tokens
  at inference, which we cannot afford at 16.6 ms.
- GRPO-RM (arXiv 2511.15256). DINOv2 ViT-S/14. "Group" = the full class set (exact, no sampling). ImageNet
  76.21 vs 74.48; OOD linear-probe +4.26 on average. Caveats: vision, linear probe, and the reward adds a -p_i
  "uniformity" term, so part of the gain is a regularizer. 15-35% more compute. Weak evidence for us.
- MaxRL (arXiv 2602.02710). In a controlled ImageNet classification test, REINFORCE failed to improve from low
  starting pass rates, while MaxRL tracked exact cross-entropy. GSM8K pass@1 33.2 vs GRPO 29.3. This is direct
  evidence that for a classifier, cross-entropy is the better end of the RL family.

### 3.4 SFT losses inspired by RL (one-line changes)

- DFT (arXiv 2508.05629, ICLR 2026). Scale each token's loss by stopgrad(p). Beats SFT on math, code and multimodal
  tasks. For one token this IS exact expected-reward RL (table in section 2).
- "Beyond Log Likelihood" (arXiv 2510.00526, ICLR 2026). 8 backbones, 27 benchmarks. The -p loss wins where the
  model is already strong (Qwen2.5-Math-7B math: 36.51 vs 22.67 NLL, +13.84). It ties in the middle (medical: -1.34).
  It collapses where the model is weak (figfont puzzles, Qwen2.5-7B: NLL 35.20, -p 0.00). Our new skill families
  target C1's weak spots, so NLL (cross-entropy) is the right loss there.
- ASFT (arXiv 2509.23753, ICLR 2026). DFT drifts far from the start model (high KL). Adding a KL anchor fixes it.
  +4.85 average over SFT on math with 100K samples. The lesson again: the anchor matters.
- One-Token Rollout (arXiv 2509.26313). Samples 256 tokens per position, reward +1 gold / -0.1 others. Qwen3-4B math
  in-domain 36.98 -> 45.61; out-of-domain 30.41 -> 31.57. Almost no extra cost. In expectation it equals
  1.1 x DFT (section 2), so it adds nothing new for our readout.

### 3.5 Calibration

- RLCR (arXiv 2507.16806). Qwen2.5-7B with generated reasoning and spoken confidence; reward = correct - Brier.
  HotpotQA in-domain ECE: RLVR 0.37, RLCR 0.03 (accuracy 63.0 vs 62.1). Out-of-domain ECE: base 0.40, RLVR 0.46,
  RLCR 0.21. Plain RL made calibration worse. RLCR is a fix for a problem our readout does not have.
- "On the effectiveness of reward functions in RL for confidence calibration" (arXiv 2607.04332). The best reward
  scheme depends on the use case. No single winner. Unknown how it maps to logit readouts.

### 3.6 Warnings about RL gains

- Spurious rewards (arXiv 2506.10947). On Qwen2.5-Math-7B, random rewards gave +21.4 on MATH-500 (true reward +29.1).
  The gain came from eliciting a pretrained habit (code-style reasoning). Other families gained little or lost. RL
  gains on Qwen-family models can be elicitation, not learning.
- Yue et al., NeurIPS 2025 (arXiv 2504.13837). RL improves pass@1 but narrows coverage. Base models win at large k
  (about 9 points at pass@128 on Minerva, 32B). RL sharpens what is there. Our readout already reports the full
  distribution, so "sharpening" is just lower temperature, which we can tune after training.

### 3.7 Costs

- Our readout: exact-expectation RL costs the same as SFT. One forward/backward pass, and all K letters scored from
  the same logits. On Modal H100: 2.72 s/step, 16.9 rows/step. 1,000 steps = 0.76 h = about $3.09.
- RL with generated reasoning is far more expensive. CLS-RL: thinking RL took 45x SFT time; no-thinking RL took 2.7x
  (still generating class names). RLCR: 32 samples per prompt, 1,536-4,096 tokens each. GTA: 16 rollouts per
  prompt. It also breaks our 16.6 ms latency if reasoning is kept at inference.
- Small-model RL can be cheap in math ($42 for a 1.5B model, 7,000 samples; arXiv 2503.16219), but that buys
  reasoning, which we do not use.

## 4. What this means for C (actions)

### 4.1 Do not run GRPO / PPO / RLCR for C
The math says it is re-weighted cross-entropy. The weighting starves C1's weak rows. The vote-share version breaks
calibration. The only published text-classification head-to-head at 4B (GTA) has pure GRPO 3.7 points below SFT.

### 4.2 Fix the anchor reference (code finding)
`train_decoder.py` (docstring lines 8-10, and line 908) computes the anchor KL with `model.disable_adapter()`.
That is the frozen Qwen3.5-4B BASE model. Line 726 says it plainly: with `init_adapter` set (stage 2), "the KL anchor
still uses the frozen base". So a C run that starts from C1 and sets `beta > 0` would pull C back toward the
untuned base, not toward C1. That is the opposite of the plan's "stay close to C1" anchor.
Two ways to fix it:
- (a) Offline: run C1 once over the anchor rows. Store its candidate-token probabilities in each row (for example
  `meta.c1_probs`). Use KL(c1_probs || p_student) as the anchor. This is forward-only. My estimate: about 1/3 of a
  training step per batch, so about 90K rows = about 1.3 h = about $5.4.
- (b) Online: load C1's adapter twice, one frozen reference and one trainable copy, and switch adapters for the
  anchor forward pass. This costs the same as today's anchor pass.
C1 is our own 4B model, so this is self-distillation, not a bigger teacher. It is RL's Razor done directly: the
KL-minimal target, without RL.

### 4.3 Keep cross-entropy / KD as the main loss
- Keep the log loss on new families (model-weak end, per arXiv 2510.00526).
- Do not add DFT / -p weighting to new rows.
- Keep the consistency terms (complement / equiv / inv / perm). They are exact, differentiable "rewards" for
  logical consistency. They are a better tool for negation flips than any scalar RL reward.

### 4.4 Take RL's data ideas, not its estimator
RL papers gain a lot from training at the model's edge. Balanced online difficulty filtering gave up to +12% in under
half the GRPO steps (arXiv 2504.03380). Their theory: improvement is lower-bounded by the variance p(1-p). Our
programs label data exactly, so we can do this with plain SFT:
1. Run C1 once (forward only) over candidate program-labelled rows. Record p_g.
2. Downsample rows with p_g > 0.97. C1 already knows them; they add drift with little to learn.
3. Send rows with p_g < 0.05 to a label check before training. Cross-entropy pushes hardest on these. If the program
   or card has a bug, these rows do the most harm. If they are right, they are the most valuable rows.
4. For families where C1 is weak (negated yes/no, long documents), generate more program variants near the failure
   zone (0.05 < p_g < 0.7), then label them by program.
This uses C1 on training candidates only. It never touches eval or sealed data.

### 4.5 Choose checkpoints on out-of-domain data
OOD skill can peak early in SFT and then fall (arXiv 2509.12235). Save checkpoints often (for example every 10% of
the run). Score the dev gate plus a held-out slice of the new families at each. Keep the sealed new-domains suite
for the final pick only. Step B weight-softening (WiSE-FT style) is the parameter-space version of the same fix.

### 4.6 Abstain and soft yes/no: decide at readout, do not learn it with RL
If a benchmark pays +1 for correct, -w for wrong and -a for abstain, the best rule is: answer if max p >= (w - a) /
(1 + w), else abstain. Plug in the benchmark's real payoffs. This needs calibrated p, which cross-entropy plus KD
gives. Fit any temperature on the dev gate, not the sealed suite.

### 4.7 Keep format variety
Prompt diversity was the main reason SFT matched or beat RL on unseen instructions (arXiv 2510.00237). Our plan
already has instruction rewordings, label-definition styles, option shuffles and varied counts. Keep all of them.

## 5. Optional minimal pilot (low priority)

Purpose: one cheap test of the exact RL-equivalent weighting, so the question is closed with our own data.

- Start: C1 (or the step-B model, whichever round 1 uses).
- Data: the first 50.7K rows (3,000 steps) of the round-1 mix, same order, same seed.
- Control (A): the round-1 run itself, checkpoint saved at step 3,000. This is free if round 1 saves it. Arm B must
  use the same schedule length (same `n_steps`, same warm-up ramp) and simply stop at step 3,000. If the script
  cannot stop early, run a matched 3,000-step control too (+$9.3).
- Arm B (exact GRPO, no sampling): the same loss, but on hard-label new-family rows only, multiply the task loss by
  w = stopgrad(clip(sqrt(p_g / (1 - p_g)), 0.1, 3)), normalised to batch mean 1. Replay, KD and anchor rows stay
  unchanged. This is the expected GRPO gradient with zero variance and zero extra compute.
- Readouts: dev gate; a held-out slice of the new families (not trained on); the hard / negated yes/no slice;
  ECE and Brier. Do NOT spend the sealed new-domains suite on this.
- Pre-registered rule: adopt B for round 2 only if B - A >= +1.0 pt on the held-out new-family slice (paired
  bootstrap 95% CI excludes 0) AND the hard/negated yes/no slice is not lower AND the dev gate is within -0.3 AND
  ECE is not worse by more than 1.0 pt. Otherwise close the RL question for C.
- Cost: 3,000 steps x 2.72 s = 2.27 h = about $9.3, plus eval (small; exact amount unknown). About $10-11 total.
- My prior: B ties or loses. It should lose on the negation slice. Chance it passes the rule: about 10% (my
  estimate).

## 6. Expected effects (my estimates, not measured)

| Change | Sealed new-domains accuracy | Risk |
|---|---|---|
| Replace CE with GRPO / expected reward | -0.5 to +0.3 pt (about 0) | Worse on negation; worse ECE if vote-share reward |
| Anchor to C1 instead of base (4.2) | 0 to +1 pt (mostly by avoiding regression) | Small; tune beta |
| C1-in-the-loop row selection and audit (4.4) | +0.5 to +2 pt on targeted slices; far domains unknown | Needs program checks |
| OOD checkpoint pick and step B (4.5) | 0 to +1 pt | Spends dev evaluations |

## 7. Unknowns

- Whether a short reasoning budget could help C. Not tested here. It conflicts with the 16.6 ms latency goal.
- How Jev was trained. Unknown.
- How strongly WiSE-FT-style gains carry from CLIP image models to a LoRA'd 4B decoder. Unknown.
- The exact forward-pass cost of a C1 scoring pass on Modal. Estimated above, not measured.
- Whether `train_decoder.py` can stop early on a longer schedule. Not checked.

## Sources

- SFT Memorizes, RL Generalizes (arXiv 2501.17161): https://arxiv.org/abs/2501.17161
- Debunk the Myth of SFT Generalization (arXiv 2510.00237): https://arxiv.org/abs/2510.00237
- RL Fine-Tuning Heals OOD Forgetting in SFT (arXiv 2509.12235): https://arxiv.org/html/2509.12235v2
- RL's Razor (arXiv 2509.04259): https://arxiv.org/abs/2509.04259
- Does Math Reasoning Improve General LLM Capabilities? (arXiv 2507.00432): https://arxiv.org/abs/2507.00432
- On-Policy Distillation, Thinking Machines: https://thinkingmachines.ai/blog/on-policy-distillation/
- WiSE-FT, Robust fine-tuning of zero-shot models (arXiv 2109.01903): https://arxiv.org/abs/2109.01903
- Think or Not Think / CLS-RL (arXiv 2503.16188): https://arxiv.org/abs/2503.16188
- GTA, supervised-guided RL for text classification (arXiv 2509.12108): https://arxiv.org/abs/2509.12108
- Calibration-aware RL for decision-making LLMs (arXiv 2601.13284): https://arxiv.org/abs/2601.13284
- GRPO-RM (arXiv 2511.15256): https://arxiv.org/abs/2511.15256
- Maximum Likelihood Reinforcement Learning (arXiv 2602.02710): https://arxiv.org/abs/2602.02710
- GRPO effective loss and success amplification (arXiv 2503.06639): https://arxiv.org/abs/2503.06639
- Rewards as Labels / REAL (arXiv 2602.05630): https://arxiv.org/abs/2602.05630
- DFT, On the Generalization of SFT (arXiv 2508.05629): https://arxiv.org/abs/2508.05629
- Beyond Log Likelihood (arXiv 2510.00526): https://arxiv.org/abs/2510.00526
- Anchored SFT (arXiv 2509.23753): https://arxiv.org/abs/2509.23753
- One-Token Rollout (arXiv 2509.26313): https://arxiv.org/abs/2509.26313
- RLCR, Beyond Binary Rewards (arXiv 2507.16806): https://arxiv.org/abs/2507.16806
- Reward functions for RL confidence calibration (arXiv 2607.04332): https://arxiv.org/abs/2607.04332
- Spurious Rewards (arXiv 2506.10947): https://arxiv.org/abs/2506.10947
- Does RL Really Incentivize Reasoning Beyond the Base Model? (arXiv 2504.13837): https://arxiv.org/abs/2504.13837
- RL for Reasoning in Small LLMs (arXiv 2503.16219): https://arxiv.org/abs/2503.16219
- Online Difficulty Filtering (arXiv 2504.03380): https://arxiv.org/abs/2504.03380
- Generalized Cross Entropy (Zhang and Sabuncu, NeurIPS 2018): https://nips.cc/media/nips-2018/Slides/12761.pdf
- Local code read: /Users/aryamahadik/Documents/jev/opendecide-data/lean/train_decoder.py (lines 8-10, 726, 908)
