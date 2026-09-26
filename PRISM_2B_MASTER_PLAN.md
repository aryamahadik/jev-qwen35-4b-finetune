# PRISM-2B master plan

Date: 2026-09-26. Built from four design notes (privilege separation, decision head and calibration, accuracy, efficiency) and one hostile red-team review. Where the review corrects a design, this plan follows the review. Appendix A lists every correction and what it changed.

Tags: **[M]** measured in this repo · **[D]** derived from measured numbers or exact math · **[S]** speculative (a prior or an assumption with a test attached).

---

## 1. Summary

**In plain words.** PRISM-2B is a small open model (Qwen3.5-2B plus a LoRA adapter) that returns a probability for each allowed option without generating text. It does one shared backbone read of the evidence, followed by parallel lightweight question branches. That takes about 10 ms of GPU time for short single-decision requests. Long evidence, many questions or wide 255-option cards take longer (§3.7, §7). Untrusted text cannot directly overwrite or decay the protected recurrent memory that stores trusted instructions. It can still influence the decision through the read path, the other heads, the attention layers and the MLPs (§4). It trains on our existing decision dataset, newly Claude-authored examples, and soft targets from our 4B teacher; no larger model is used as a teacher. (Legacy rows from rounds v0.6–v0.8 that Qwen3-235B helped write are listed in §5 and are removed or disclosed.)

**Thesis.** A single-pass readout, a consistency-trained loss and a write-protected memory for trusted instructions can make a 2B model that is much harder to hijack, faster and cheaper than Jev. The same design cannot make a 2B more accurate or better calibrated than Jev while its only teacher (our 4B v0.11c) is itself behind Jev on both. That follows from the numbers, not from pessimism. On the fresh test OHS-2, v0.11c scores 79.9 vs Jev's 81.5, and its yes/no Brier is 0.083 vs 0.038 **[M]**. A student usually keeps only about 0.90 of its teacher's accuracy **[M]**.

**The goal, re-scoped.** "Beats Jev on every metric" has about **0.2%** probability (red team). This plan therefore sets two tiers.
- **PRISM-2B** is expected to beat Jev on hijack resistance, speed and steady-state cost, and possibly on complement consistency. It is expected to lose on accuracy (about −6.5 pp) and on yes/no Brier. Its public claims will say exactly that.
- **Any "beats Jev on accuracy" claim is attempted with the 4B**, after one cheap teacher round (v0.12-4B). That round is also the only lever that raises the 2B's ceiling.

**What "beating Jev" means.** All endpoints are pre-registered on a new test, **OHS-3**, before any model is run on it. Jev's version is pinned (`typesafe/jev-1.13-20260917`), and Jev is run twice with the two runs averaged.

| Metric | Test set | "Beats Jev" means | "Matches Jev" means |
|---|---|---|---|
| Accuracy on new data (primary) | OHS-3 micro and macro accuracy (Holm across the 3 primary endpoints) | 95% paired group-bootstrap CI of (ours − Jev) entirely above 0 | CI lower bound above −2.0 pp |
| Calibration (primary) | OHS-3 yes/no Brier | CI of (Jev − ours) entirely above 0 | CI lower bound above −0.010 |
| Consistency (secondary) | Complement violation, paraphrase flip rate and option-order drift on OHS-3 twins | CI of the difference favours us, for each metric separately | – |
| Hijack resistance (secondary) | Held-out black-box attack suite in both directions, plus best-of-N adaptive attack; over-defence set | Attack success (ASR) lower by ≥ 20 pp with the CI excluding 0, **and** over-defence accuracy no more than 2 pp below Jev | – |
| Speed | End to end from the same client, warm server, p50 and p95, on a pre-registered request mix (short, 3k-token evidence × 5 questions, 255-option cards) | Lower p50 **and** p95 on the mix, with every scenario class also reported | – |
| Cost | $ per 1,000 decisions at measured batch-1 latency and a pre-registered utilisation ρ = 0.7 | Cheaper at ρ = 0.7. The idle-inclusive cost at current traffic is also reported | – |

**Minimum detectable effect (MDE) on OHS-2 (n = 1,320).** Measured from the OHS-2 predictions, the paired standard error of (v0.11c − Jev) accuracy is **0.89 pp**, with discordant items at 11% **[M]**. With 80% power at two-sided α = 0.05:

$$\mathrm{MDE}=(z_{0.975}+z_{0.80})\cdot SE=2.80\times0.89\approx\mathbf{2.5\ pp}\quad(2.9\text{ pp at Holm's first step, }\alpha=0.05/3).$$

- A 2B disagrees with Jev more often. At about 16% discordance, SE ≈ √(0.16/1320) ≈ 1.1 pp, so the MDE is about **3.1 pp** (3.6 with Holm) **[D]**.
- Yes/no Brier on 360 rows: paired SE **0.0085** **[M]**, so the MDE is **0.024** (0.027 with Holm).
- **Meaning.** On a test of OHS-2's size, a true tie cannot be told apart from a ±2.5 pp difference. A true edge of about 3 pp is needed for a win to be detected reliably.
- **OHS-3 sizing.** OHS-3 should therefore have about 2,000 items, including at least 600 yes/no items. That gives an accuracy MDE of about 2.0 pp (4B) or 2.5 pp (2B), and a Brier MDE of about 0.018 **[D]**. Building it is CPU work, and running models and Jev on it costs cents.

---

## 2. Architecture (the refined hybrid)

**In plain words.** One fixed prompt layout serves every component. Trusted text goes first and can be cached. Untrusted evidence comes next. Each question then gets a short trusted "branch" that repeats the question and option labels just before the answer. In every recurrent layer a quarter of the memory heads (the "policy heads") stop writing once trusted text ends, so the evidence cannot overwrite or fade them. Components marked [conditional] ship only if their gate in §6 passes.

```
API REQUEST  (trust comes from WHICH FIELD the text arrived in; the model never guesses it from the text)
  system, instructions, all questions,
  options + definitions ...................... T  trusted   positions 1..m      (cacheable across calls)
  state: user text, documents, tool output ... E  untrusted positions m+1..m+n
  per question j: question j + option labels . B_j trusted branch, repeated AFTER E
  answer cue ................................. A_j readout position

TOKEN LAYOUT (one call, N questions; segments are tokenised separately and concatenated,
              in training AND serving, so no token merges across a boundary)

  [ sys | Q1..QN | options + definitions ][ evidence ............ ]--+--[ Q1 + labels | A1 ]
  |<--------------- T ------------------->|<--------- E --------->|  +--[ Q2 + labels | A2 ]
         prefix cache: 18.6 MiB + 12 KiB/token                       +--[ QN + labels | AN ]
                                           fork here: copy DeltaNet state + conv state (18.6 MiB each),
                                           share attention KV read-only; the N branches run as one batch

QWEN3.5-2B BACKBONE: 24 layers = 6 x [ GDN, GDN, GDN, ATTN ], hidden 2048, LoRA r32 on all projections

  Gated DeltaNet layer (18 of them), 16 heads, d_k = d_v = 128, conv1d width 4, fp32 state
  +------------------ 12 data heads -------------------+ +------ 4 policy heads (p = 0.25) [conditional] --+
  | normal delta rule on T, E, B, A                    | | write on T only: beta_t = g_t = 0 for all t > m |
  | carry the evidence                                 | | state frozen at S_m, exactly                    |
  +----------------------------------------------------+ +-------------------------------------------------+
        -> gated RMSNorm -> out_proj(concat of all 16 heads) -> residual -> MLP (6144)

  Full-attention layer (6 of them): causal, 8 query / 2 KV heads, head_dim 256, sigmoid output gate
        (unchanged; no policy KV group)

  Baseline for the separation test [conditional]: one learned trust-segment vector e_E added to every
        evidence token's embedding ("datamarking"; 2,048 parameters)

READOUT AT A_j
  h_A --> letter logit  z_i = logsumexp_{t in tokens(label_i)} u_t . h_A                       (current, <= 255 options)
       +  slot residual w . MLP([h_A ; v_i ; h_A * v_i]), v_i = mean-pool of label i's span in B_j,
          w zero-initialised                                                               [conditional]
       --> p = softmax(z / T_dev) over the option set
       --> optional selective mode: answer only if c(x) >= lambda_hat (risk-certified threshold)
```

**Why this layout** **[D]**.
- **Separation needs trusted-first.** In the current cygnet layout (state → instructions → options), the trusted tokens after E write into every head from inputs that already contain evidence.
- **The branch fixes the "attacker speaks last" problem.** In a plain trusted-first layout the attacker's text sits right before the answer cue, and a fake `Options:` block would be the most recent one. Here the real question and labels always come after E.
- **The branch makes the slot head evidence-aware.** Option spans in B_j come after E, so v_i has read the evidence. In a plain trusted-first layout the slot head would be blind to the evidence, the weakness §3.4 argues against.
- **The fork gives one shared backbone read of the evidence per call, followed by parallel lightweight question branches** (a two-stage computation, not one monolithic forward pass). Each question's branch sees T and E but not the other branches, so answers do not depend on branch order. They still depend on the order of questions inside T, which is handled by a trained consistency term, not guaranteed.
- **Governance.** This layout replaces the cygnet layout that `FREEZE.md` froze. The change is logged as a deliberate deviation and is kept only if gate L (§6) passes. If it fails, we keep cygnet, drop separation (which cannot work in cygnet), and serve with the cygnet evidence-first fork instead.

---

## 3. The math

### 3.1 Gated DeltaNet recurrence and the write block

This is Qwen3.5's exact form. The state is $S\in\mathbb R^{d_k\times d_v}$, and $\hat q,\hat k$ are L2-normalised.

$$\alpha_t=e^{g_t},\quad g_t=-e^{A_{\log}}\,\mathrm{softplus}(a_t+\delta_{dt})\le0,\qquad\beta_t=\sigma(b_t)$$

$$S_t=\alpha_t\,(I-\beta_t\hat k_t\hat k_t^\top)\,S_{t-1}+\beta_t\,\hat k_tv_t^\top,\qquad y_t=w\odot\mathrm{RMSNorm}\!\big(S_t^\top\hat q_t/\sqrt{d_k}\big)\odot\mathrm{silu}(z_t).$$

**Block.** For each policy head $h\in P_l$ and every position $t>m$ (all of E, B and A; 1-indexed, with T at positions $1..m$), set $\beta_t=0$ and $g_t=0$. Then $\alpha_t=1$ and $S_t=S_{t-1}$, so $S_t=S_m$ for all $t\ge m$.

**Why block $g$ as well as $\beta$.** If only β is blocked, $S_{m+n}=\big(\prod_{t\in E}\alpha_t\big)S_m$. The evidence controls $a_t$, so it could shrink the trusted memory toward zero. The gated RMSNorm removes a scalar scale only until the state reaches its ε-floor.

**Why it matters for the delta rule.** If an evidence token has $\hat k_\pi^\top\hat k_0=1$ and $\beta_\pi=1$, it replaces the stored association: $S'^\top\hat k_0=v_\pi$. Linear attention can only add to a stored association; the delta rule can overwrite it. The block sets that overwrite strength to exactly 0 on policy heads.

**Head allocation.** $p=0.25$ means 4 of 16 heads in every DeltaNet layer, 72 of 288 DeltaNet heads, and **0 of the 48 attention heads**. Three selection rules are compared in Phase 0 by forward passes only: first heads, lowest evidence-write ratio $r_{l,h}=\|S_{m+n}-cS_m\|_F/\|S_{m+n}\|_F$, and random heads.

### 3.2 Readout

$$z_i=\log\!\!\sum_{t\in\mathcal T(\ell_i)}\!e^{u_t^\top h_A}\;+\;w^\top\mathrm{MLP}\big([h_A;v_i;h_A\odot v_i]\big),\qquad p_i=\mathrm{softmax}_i(z/T).$$

- $w=0$ at initialisation, so step 0 equals the current readout.
- $T$ is fitted on dev-select by NLL: $T^\star=\arg\min_T\sum_x-\log\mathrm{softmax}(z(x)/T)_{y}$.

### 3.3 Training loss

**Target.** For gold rows, the smoothed gold is $\tilde y=0.95\,e_g+\frac{0.05}{K}\mathbf 1$ (yes/no: $y=(1-2\epsilon)g+\epsilon$). The target is

$$q_i=(1-\kappa_i)\,\tilde y_i+\kappa_i\,p_{T}(\cdot\mid x_i),\qquad \kappa_i=\begin{cases}0.5 & \text{gold rows where gold still wins in }q_i\\ 0 & \text{gold rows where the teacher would make a wrong label win (36 rows in train\_2b\_kd)}\\ 1 & \text{transfer rows with no gold}\end{cases}$$

Here $p_T$ is the chosen 4B teacher (v0.12-4B if gate T passes, else v0.11c), single view, on the clean input. The teacher never sees an attacked input.

**Total loss** for a batch $B$ with relation pairs $R$ (the v0.11c loss plus the changes marked ★):

$$\boxed{\;\mathcal L=\underbrace{\tfrac1{|B|}\sum_{i}H\big(q_i,p_\theta(x_i)\big)}_{\text{task + distillation}}+\underbrace{\tfrac1{|B|}\sum_{i\in\text{twins}}H\big(q_{c(i)},p_\theta(\tilde x_i)\big)}_{\bigstar\text{ attacked twins}}+r(s)\Big[\lambda_c\,\overline{\ell}_{\text{cons}}+\lambda_{\text{inv}}\,\overline{\ell}_{\text{inv}}+\lambda_p\,\overline{\ell}_{\text{perm}}\Big]+\beta\,\overline{\ell}_{\text{anchor}}\;}$$

| Term | Formula (mean over pairs or rows) | What it is for |
|---|---|---|
| Task + distillation | $H(q_i,p_\theta(x_i))=(1-\kappa)\mathrm{CE}(\tilde y,p_\theta)+\kappa[\mathrm{KL}(p_T\|p_\theta)+H(p_T)]$ | Learn the answer. Get the teacher's knowledge of which wrong options are close |
| ★ Attacked twins | $H(q_{c(i)},p_\theta(\tilde x_i))$: the attacked input gets the **clean** row's target | Answer correctly even with a planted instruction or claim in E |
| Complement | $\mathrm{symKL}\big(p(\cdot\mid q),\ \mathrm{swap}(p(\cdot\mid\neg q))\big)$ | $P(\text{yes}\mid q)+P(\text{yes}\mid\neg q)=1$ |
| Equivalence | $\mathrm{JS}(p_a,p_b)$ across paraphrases, option orders and ★ question orders inside T | Same meaning gives the same answer. This term owns **paraphrase consistency** |
| Perm twin | $\mathrm{JS}(p^{\pi_1},p^{\pi_2})$ after un-permuting (30% of choice rows) | No letter or position bias |
| Invariance | $\mathrm{KL}(\mathrm{sg}\,p_\theta(x_i)\,\|\,p_\theta(\tilde x_i))$ | The attacked twin must match the clean view, with no gradient through the clean side |
| ★ Anchor | $\mathrm{KL}(p_{T}(x)\,\|\,p_\theta(x))$ on the 6.2% anchor rows, target changed from the frozen 2B to the teacher | Keep general behaviour. The frozen 2B (78/118 on JevBench A) is a weak anchor next to the teacher (107/118) **[M]** |

- $\overline\ell_{\text{cons}}$ pools complement and equivalence pairs, as in `train_decoder.py`.
- $r(s)$ is the 20% linear warm-up. The anchor is not ramped.
- Weights: $\lambda_c=1$, $\lambda_{\text{inv}}=1$, $\lambda_p=0.5$, perm-twin fraction 0.3, $\beta=1$ (v0.11c values **[M]**).
- The anchor is never applied to attacked twins.
- **Removed:** the contrastive term. As written, it left the positive pair out of the denominator, so it had no lower bound. It also moves no metric against Jev.
- Separation adds **no loss term**. It is a fixed mask from step 0. The slot residual and trust vector are trained by the same loss.

### 3.4 Why the joint readout stays primary (short)

A bi-encoder scores each option from a state vector $s$ computed without seeing that option's definition. It cannot look up the evidence features a definition asks for, and it cannot contrast options. On OHS-2's task mix the estimated loss is **−3.7 to −10.0 pp (centre −6.9)** **[S]**, so the joint readout stays primary and no bi-encoder test is run. Retrieval for more than 255 options is product scope and deferred: no benchmark has more than 255 options.

### 3.5 Calibration: what can move Brier

**Murphy decomposition** on OHS-2 yes/no (n = 360):

| | Brier | REL | RES |
|---|---|---|---|
| v0.11c | 0.0831 | 0.0041 | 0.172 |
| Jev | 0.0377 | 0.0071 | 0.220 |

- The difference in REL is **not significant**: 95% CI [−0.008, +0.006].
- The gap is resolution, i.e. accuracy and discrimination.
- Post-hoc remapping can remove at most REL, so we expect at most **0.005** from it.
- The best in-sample monotone map (per-task isotonic fitted on OHS-2) only reaches 0.062. That is a diagnostic ceiling, not a method.

**Brier by outcome.** With $e$ the error rate, $b_r$ the Brier per correct answer and $b_w$ the Brier per wrong answer:

$$\mathrm{BS}=(1-e)\,b_r+e\,b_w .$$

To reach Jev's 0.038 at $b_r=0.016$:
- if wrong answers are confident ($b_w\approx0.5$): $e\le4.5\%$, i.e. **95.5%** yes/no accuracy;
- if wrong answers are hedged ($b_w\approx0.30$): **92.3%**.

The 4B is at 88.6% on OHS-2, and the 2B pilot was at 72.5% on OHS-1 **[M]**. So we track **$b_w$ (confidence when wrong)** and yes/no accuracy as the calibration levers. REL and ECE are secondary, reported with CIs.

### 3.6 Selective answering (product feature, not a Jev metric)

A correctness score $c(x)=\sigma(\psi^\top\phi(x))$ is trained leave-one-task-out on dev-select. Its features φ are entropy, margin, log K, length and a 16-d projection of $h_A$. The threshold is chosen by Learn-then-Test: step down the grid while the Clopper–Pearson bound satisfies $U_\delta(\lambda)\le\alpha$.

- Guarantee: $P(\text{risk}\le\alpha)\ge1-\delta$, **only under exchangeability**.
- Certifying α = 2% at δ = 0.05 needs at least about 150 accepted items with zero errors.
- On new tasks (the OHS setting), exchangeability fails. So "certified mode" means the customer labels 300–1,000 items of their own label set.

### 3.7 Serving cost and latency

- **Latency.** $t(T)\approx a+bT$, with $a=6.45$ ms and $b=0.0153$ ms/token for the 2B ($R^2=0.995$), and $a=7.28$, $b=0.0297$ for the 4B **[M]**. The fork takes two stages: $t\approx 2a+b\,T_{\text{fork}}$.
- **Tokens computed per call.** With the prefix cached: $T_{\text{fork}}=E+N\,(\bar q_B+\ell)$. Without the cache, add $s_0+\sum_j q_j$.
- **Cost per decision** at batch 1: $\text{cost}=t_{\text{server}}\cdot\$1.097\times10^{-3}/\text{s}\,/\,\rho$. The 2B at 9.4 ms costs $1.03\times10^{-5}$ vs Jev's $1.65\times10^{-5}$, so it is **1.6× cheaper at ρ = 1 and breaks even at ρ ≈ 0.62** **[D]**. The earlier cost tables that assumed 65k tokens/s were wrong for this server.
- **Prefix cache size.** $M(P)=18.6\text{ MiB}+12\text{ KiB}\cdot P$. Pad tokens must get β = g = 0 in **all** heads, or they corrupt the cached state.

### 3.8 Statistics used at every gate

- **Paired group bootstrap.** Resample whole `group_id`s, so relation twins and multi-question calls stay together. Stratify by task. 10,000 draws.
- **Standard error.** For 0/1 differences, $SE\approx\sqrt{D/n}$, where $D$ is the discordance rate. Power is planned at realistic $D$: 10–16% for 2B-vs-2B arms (not 6%), and 25% for student vs teacher.
- **Thresholds are set above their SE.** Where they cannot be, the gate is reported as "underpowered", not "passed".
- **Seed noise.** Only one seed per arm is affordable. Arm differences smaller than about 1 pp are treated as ties.
- **Two dev splits.** Dev is split by group into **dev-select** (60%, about 2.8k clean rows and 900 attack rows), used for every choice, and **dev-confirm** (40%, about 1.9k and 600), opened only at gates T and F.

---

## 4. What is guaranteed and what is empirical

| Guaranteed by math or by construction (given correct trust labelling by the caller and a passing T0a implementation check) | Empirical only (must be measured; can fail) |
|---|---|
| **Causality (G1).** Every hidden state of the trusted prefix is the same for any evidence. This holds in *any* causal layout, with or without the block. It is not a separation result | Accuracy, Brier, all consistency metrics |
| **Policy memory freeze (G2).** Policy-head states equal $S_m$ after E, B and A. The result is bitwise for fully blocked chunks and fp32-rounding-level (~1e-6 relative) otherwise. Evidence cannot overwrite or decay them, whatever its length | That the model *uses* the protected memory (reliance test T6) |
| **Output channel.** The output is a probability vector over a fixed option set: no free text, no tool calls. It is **not** "8 bits per call": the full probability vector is returned, which is also an oracle for adaptive attackers | Attack success on held-out, adaptive and white-box attacks. No certified bound exists |
| **Fork equivalence.** A branch's answer equals the answer from the full concatenated sequence (bf16 numerics, about 1e-3), and does not depend on the other branches | Question-order invariance *inside T* (trained, not guaranteed) |
| **Prefix-cache equivalence.** Same as the fork, given pad blocking and the conv state taken from the last 3 real tokens | Latency and cost numbers, utilisation, cold starts |
| **Selective risk (LTT).** Risk ≤ α with probability ≥ 1−δ, under exchangeability only | Selective risk on new tasks (exchangeability fails) |

**What the block does NOT do** **[D]**.
- At the answer, a policy head outputs $w\odot\mathrm{RMSNorm}(S_m^\top\hat q_A)\odot\mathrm{silu}(z_A)$. Both $\hat q_A$ and $z_A$ are computed from inputs that include the evidence.
- So the evidence chooses **which** trusted association is recalled. If $\mathrm{erank}(S_m)$ is near 128, it can reach any output direction.
- The evidence can also **silence** the head by driving silu(z_A) toward 0. "No erasure" is true of the stored state only.
- The 12 data heads per layer, all 6 attention layers and the MLPs carry evidence at full strength. A planted "the answer is B" can still be read.
- Semantic attacks that look like real evidence cannot be stopped by architecture.

This is **defence in depth**: 25% of DeltaNet heads keep an incorruptible copy of what the question and options mean. It is not immunity.

---

## 5. Data plan

**In plain words.** Claude writes every new item. Our own 4B supplies soft labels. Nothing comes from any test set or from any dataset a test set was built from, and nothing comes from a model bigger than our 4B.

**Rules (checked before every training run).**
1. **Sources.** Claude-authored text, the existing 2B mix (`data/train_2b.jsonl`, 59,723 rows **[M]**) and teacher labels from our 4B.
   - Before any run, an audit confirms that no row carries labels or text from the 9B, 27B or 35B-A3B probes (ledger row A1, `bench/runs/t_q35_9b_A`). The audit greps `meta.teacher`/provenance fields and records the result in the ledger.
   - **Audit result (26 Sep 2026).** No 9B/27B/35B probe output is in any training file. The legacy rounds v0.6–v0.8, however, used **Qwen3-235B** (via OpenRouter), and about 9,000 of the 59,723 rows in the 2B mix (~15%) involve it:
     - 1,518 LAH items (source `lah_*`): items and golds written by Qwen3-235B, second-verified by gpt-oss-120b.
     - 1,500 `meta_*` rows: planted-authority messages written by Qwen3-235B.
     - ~5,960 v0.7-core rows whose card definitions came from `compile_cards.py` (Qwen3-235B, from label names only). Their golds are the datasets' human labels.
   - These rows are dropped from every future training mix and replaced with Claude-written equivalents (for example `reason_c` covers the LAH families; cards are re-written by Claude). Models trained before this (v0.8 to v0.11c, and the 2B A12/A13 distilled from v0.11c) keep that lineage, and any claim about them discloses it.
2. **Excluded sources.** No OHS-1, OHS-2, OHS-3 or JevBench half-B items. None of the OHS source corpora either: arXiv, TabFact/Wikipedia tables, PubMed-derived sets, SciFact, Moral Stories/Social-Chem, CPC patents, DDI, stance and AfD sources used in tests.
3. **Decontamination.** `decontam.py` at 13-grams against OHS-1, OHS-2, OHS-3 and JevBench B for every new row.
4. **OHS-3 comes first.** OHS-3 is built and pre-registered **before** any new data family is finalised. Its task types exclude the four families below that were chosen from OHS-2 losses. Families (a)–(d) are logged as an OHS-2-informed deviation, and OHS-2 results on those tasks are reported as optimistic.

**Families** (train / dev sizes; dev goes to dev-select and dev-confirm by group):

| Family | Label source | Relations | Size |
|---|---|---|---|
| (a) Table fact-checking (TabFact definition, closed world) | **Executed program** (pandas) over Claude-written tables | complement, paraphrase | 1,500 / 300 |
| (b) Science claims (SciFact guideline: S/R/NEI) | Controlled edits of Claude-written abstracts; blind double pass | label-mapped negation (small code change), paraphrase | 1,200 / 250 |
| (c) Everyday moral norms (non-contested) | Minimal-edit action pairs; blind double pass | perm twin, complement | 1,000 / 200 |
| (d) Clinical sentence roles (NLM sections) | **By construction** (the section it was written for) | paraphrase | 1,200 / 250 |
| (e) Taxonomy routing (MSC2020, JEL, ACM CCS, top MeSH; not arXiv or CPC) | Intended class; blind double pass | perm twin, wide options up to 60 | 1,500 / 300 |
| Attacked twins | Clean row's target. Planted-claim mix is **45% wrong / 45% agreeing with gold / 10% neutral** (the audit found 68/32, which caused the echo gap); both yes/no directions 50/50 | inv | ~6,000 twins of ~3,000 rows |
| Over-defence rows | Legitimate authority (a court ruling, a lab result) and instruction-as-object ("does this email try to make the reader act?"); gold depends on the evidence | ordinary rows | ~600 |
| Multi-question rows | Several questions in T with question-order permutation twins | equivalence | ~1,000 |
| Transfer inputs | Claude-written decision inputs across domains; κ = 1 teacher labels, no gold needed | – | **≤ 10,000** (not 40k) |

**Held out from training entirely** (eval only): letter-remap and fake-delimiter/JSON-verdict attacks, the jagged third-party wording and its mirror, families C/D, non-English authority. Note that jagged holds out the wording, not the domain: 1,394 training rows come from the same Wikipedia AfD domain **[M]**.

**Verification** (the red team noted that several Claude passes make correlated errors):
1. Programs or construction give the labels for (a) and (d). An audit checks faithfulness on 5%, and must reach ≥ 98%.
2. For (b), (c) and (e): pass A writes the item, and a fresh pass B labels it blind. Keep only agreements. If a family's keep rate is below 80%, rewrite its spec.
3. **Human audit.** The founder labels 100 random kept items across families. At least 95% agreement is required, or the family is rewritten.
4. The 4B is never used as a filter, because that would delete exactly the items it gets wrong.

**Cost.** GPU cost is $0, but authoring 7k family items, 10k transfer inputs and verification is real work. Transfer inputs are the first thing cut if time runs short.

---

## 6. Experiment sequence with go/no-go gates

**In plain words.** Measure what we have first. Test the cheap, risky ideas with forward passes only. Then run small warm-start comparisons, one final training run and one final test. Every gate has a number that can fail.

**Budget rules.**
- Keep **$5 unspent** at all times (`FREEZE.md`; billing lags by about an hour).
- Add 25% contingency to every estimate.
- The current account is for **evaluation only, at most about $3**.
- Step cost: 2B at 1.8 s/step = $0.00198 per step (measured 1.6–1.63 s/step on A12/A13); 4B at 3.5 s/step = $0.0038 per step; plus about $0.2 per job for load.

### Account 1: now (after A13 finishes; hard stop $28)

| Step | Work | Go / no-go (falsifiable) | $ |
|---|---|---|---|
| G-0 | `modal billing report`; new ledger section; compliance audit (§5.1); split dev into select/confirm; **build and commit OHS-3 + `PREREG_OHS3.md`** (endpoints of §1, Jev pinned, run once) | Spendable = (28 − billed) − 5. If < $1, skip to account 2 | 0 |
| E0 | **Measure A13** (`q35_2b_v11r`) on dev-select: accuracy, top-1 disagreement D with the teacher, yes/no Brier and b_w, JevBench A, attack suite both directions + echo + over-defence, wide-option dev (27–255), paraphrase flip rate | Decides what the final run needs: **twins needed** if pooled held-out ASR > 10% or any direction > 15%; **slot head needed** if K = 100 accuracy < 60%; **round 2 needed** if D > 0.18 or the dev_nc gap to the 4B > 4 pp (A12 was −5.8 **[M]**) | 1.0 |
| P0 | **Separation, forward passes only**, on the frozen 2B and A13: T0a mechanism ($\max\|\Delta S\|_\infty/\|S_m\|_\infty\le10^{-5}$ over 200 (T, E, E′) triples; T hidden states equal within 1e-3); T0b the wrapper fires on the fla kernel path used in training and graphs; **β-only / g-only / both** ablation; erank(S_m); first vs low-write vs random heads | **GO** if T0a and T0b pass **and** A13 with the untrained block at p = 0.25 (best rule) loses ≤ 10 pp clean dev-select accuracy. Otherwise separation is dropped and reported as a negative result | 0.8 |
| K0 | Install `causal_conv1d` and refit a, b; fork and prefix-cache equivalence in the new layout on the frozen 2B (causal identity, no training needed); pad-blocking fix | Keep the conv if b drops ≥ 5% or a drops ≥ 0.5 ms with max\|Δp\| ≤ 1e-3. Fork passes if argmax agreement ≥ 99.5% and p99 \|Δp\| ≤ 5e-3; measured cache bytes within ±5% of $M(P)$ | 0.6 |
| | **Total (priority order E0 > P0 > K0; stop when spendable runs out)** | | **2.4 (3.0 with contingency)** |

### Account 2: the ~$30 top-up (usable $25 after the buffer)

| Step | Work | Go / no-go (falsifiable) | $ |
|---|---|---|---|
| T | **Teacher round v0.12-4B.** Warm start from v0.11c, about 400 steps on families (a)–(e) ×2, twins at 45/45/10, and v0.11c replay | **GO** if dev-confirm micro ≥ v0.11c + 1.3 pp with group-bootstrap lower bound > 0 (SE ≈ 0.65 pp at 8% discordance), yes/no Brier not worse by > 0.005, and ASR not worse by > 2 pp. Else keep v0.11c | 2.6 |
| R | **Relabel** the 2B mix and the new rows with the chosen teacher (single view; the 4-view labels are cut) | Only the new rows (~$0.4) if gate T fails | 1.5 |
| A | **Warm-start arms from A13**, 500 steps each, same data, same seed. R1 cygnet + twins. R2 PRISM layout + twins. R3 R2 + trust vector (datamarking). R4 R2 + block p = 0.25 (only if P0 GO) | See gates L, D and S below | 6.0 |
| F | **Final PRISM-2B run.** From A13 (or the best arm), about 1,800 steps: relabelled mix + families + twins + over-defence + multi-question rows; every component that passed; anchor to the teacher | **Ship** if on dev-confirm: accuracy ≥ A13 + 2.0 pp, yes/no Brier ≤ A13's, paraphrase flip ≤ 0.08, pooled ASR ≤ 15%. Else ship the best of A13 and the arms, and report the failure | 3.9 |
| C | Temperature on dev-select; LOTO correctness head; LTT threshold (features from one pass) | Selective mode kept if LOTO mean \|confidence − accuracy\| ≤ 0.05 and coverage at ≤ 2% risk ≥ 10% on dev-confirm. Else customer-certified mode only | 0.3 |
| S | **Serving validation**: fork and cache with the trained model; p50/p95/p99 and cold start; wide cards; sustained throughput with bucketed batching. FP8 only if contingency remains | Speed claim only if the pre-registered mix beats Jev at p50 **and** p95. Cost claim only if $/decision at ρ = 0.7 < Jev's | 1.5 |
| O | **OHS-3, once**: PRISM-2B, the chosen 4B, Jev × 2 (API ~$0.2); attack suite and best-of-200 adaptive attack (100 items) on ours and Jev; OHS-2 reported with the contamination flag | The pre-registered endpoints of §1, whatever the outcome | 1.5 |
| | **Planned total** | | **17.3** |
| | Contingency 25% | | 4.3 |
| | Buffer (never spent) | | 5.0 |
| | **Total** | | **26.6 of 30** |

**Gates inside step A** (dev-select, group bootstrap). The arms are warm-started from a cygnet-trained A13, which **favours R1**. A 500-step null is weak evidence against separation, and is reported that way.
- **Gate L (layout): R2 vs R1.** Pass if clean Δacc ≥ −1.0 pp (point) with lower bound ≥ −2.5 pp, **and** pooled held-out ASR of R2 ≤ R1 + 3 pp. Fail means: keep cygnet, drop separation, and serve with the cygnet evidence-first fork.
- **Gate D (datamarking): R3 vs R2.** Keep the trust vector if ASR falls ≥ 20% relative with McNemar p < 0.05 on items both arms get right when clean, and clean Δacc ≥ −1.0 pp.
- **Gate S (separation): R4 vs R3, the stronger baseline.** All of the following must hold:
  1. ASR$_{R4}$ ≤ 0.8 × ASR$_{R3}$ with McNemar p < 0.05;
  2. clean Δacc ≥ −1.0 pp (point);
  3. over-defence accuracy drop ≤ 3 pp (about 2 SE on 400 items);
  4. reliance test T6: zeroing the policy readouts costs ≥ 3 pp, and swapping $S_m$ between option sets makes ≥ 30% of decisions follow the swap.

  If ASR$_{R3}$ < 8%, the test is underpowered: report it and do not fold the block in.

**Cut from all designs** (they move no metric against Jev, or are unaffordable): the contrastive arm, GCG-lite white-box attacks (so we make **no** white-box robustness claim), weight soups, consensus self-distillation, 4-view teacher labels, K = 4 multi-view serving, a second seed, the bi-encoder test, the >255-option retrieval test, early exit, the L4 test. The MLX-on-Mac test is free and optional.

---

## 7. Expected results and probabilities

The probabilities come from the red-team review wherever it gave one; they replace the designers' more optimistic numbers. Estimates marked [plan] are this plan's own and are not validated.

| Metric | Jev | PRISM-2B expected (80% range) | P(PRISM-2B beats Jev) | Designer claim corrected |
|---|---|---|---|---|
| Accuracy, OHS-3 micro | ~81–82 (OHS-2: 81.5) | **75 ± 2**, gap about −6.5 (−9 to −4) | **0.02** (point estimate ≥ Jev); significant win **< 0.005** | Accuracy design said 76.3 on OHS-2, counting +0.9 from OHS-2-chosen families, +0.5 multi-view and +0.4 soups; the scaling table was also optimistic (+0.7 not +1.1 from 24k→56k) |
| Accuracy, OHS-2 (flagged, optimistic) | 81.5 | 75–77 | ~0.01 | – |
| Yes/no Brier | 0.038 (OHS-2), 0.114 (OHS-1) | 0.09–0.14 on a fresh set; post-hoc gain ≤ 0.005 | **0.02** | "REL better than Jev" is noise (CI [−0.008, +0.006]) |
| Complement violation | 0.097 (OHS-1) | 0.07–0.12 (4B: 0.080) | ~0.45 [plan] | – |
| Paraphrase flip rate | ~0.026 | 0.06–0.10 (pilot 0.112) | ~0.03 [plan]; a probable loss | Was unowned; now owned by the equivalence loss (§3.3) |
| Hijack ASR, black-box held-out, both directions | 99–100% | 5–25% | **0.85** (from training, not separation) | Separation's extra relative reduction: **0–15%** centre, not 25%; separation is never credited with the win over Jev |
| Over-defence accuracy | not measured | risk of −1 to −4 pp | – (a failure mode, not a win) | – |
| Speed, end to end p50 / p95 | 194 ms (p50), flat in length | ~95–120 ms typical; ~140 ms at 3k evidence × 5 questions with the fork; **~200 ms with 255 × 30-token cards** (server ~124 ms) | **0.90** | Wide-card latency was underestimated 2–3× |
| Cost per decision | $1.65e-5 | $1.03e-5 at ρ = 1 (1.6×), break-even ρ ≈ 0.62; 2–5× with fork or batching at high use | **0.65** at pre-registered ρ ≥ 0.7; **0.15** idle-inclusive at current traffic | Earlier tables used 65k tokens/s; batch-1 serving reaches only 18–29k on short calls. A warm H100 costs $95 a day |
| Speed and cost together | – | – | **0.60** | – |
| **Every metric at once** | – | – | **≈ 0.002** | "Beats Jev on every metric" is re-scoped (§1) |

**The 4B reference** (v0.12-4B if gate T passes) [plan, not red-team]: OHS-3 gap about −2.5 to +1 pp; P(point estimate ≥ Jev) ≈ 0.15; P(significant win) ≈ 0.02. A 2B at ρ ≈ 0.90 of its teacher would need a teacher of about 84 on OHS-2-like data (+4.4 over v0.11c) to reach Jev. Nothing measured suggests that is within reach.

**Honest public claims if the plan works.** "Open 2B decision model. Several times harder to hijack than Jev on pre-registered black-box attacks. About 2× faster end to end from a remote client, and cheaper at steady high utilisation. About 4–8 pp less accurate on fresh data." Never "10× faster and 10× cheaper": 10× speed needs co-location, and 10× cost holds only for recurring, definition-heavy schemas.

---

## 8. Risks and fallbacks

| Risk | Sign it is happening | Fallback |
|---|---|---|
| Budget overrun or billing lag | `modal billing report` shows less than planned | Priority order E0 > P0 > K0 now; T > F > O > S > A on the top-up. Arms go first when cutting. The $5 buffer is never touched |
| A13 is weak (like A12: dev_nc 68.5 vs gate 71.3 **[M]**) | E0 | Still the base for step F; the claims shift further toward speed, cost and hijack |
| The new layout hurts accuracy or helps attackers | Gate L fails | Keep cygnet, drop separation, cygnet fork for efficiency |
| The block collapses clean accuracy (0.8B: 45 → 10 untrained **[M]**) | P0 or gate S | Try p = 0.25 with the best head rule only. Otherwise report the negative result |
| The model ignores the protected channel | T6 fails | No separation claim even if ASR falls |
| Over-defence ("ignore anything that sounds like authority") | Over-defence set drops > 3 pp or echo shift grows | Raise over-defence and echo-agreeing rows; lower λ_inv |
| The teacher round does not help | Gate T fails | Keep v0.11c; spend its share on contingency |
| Claude label errors (correlated passes) | Human audit < 95% | Rewrite that family's spec; program-labelled families first |
| Overfitting to the dev set (many choices on ~4.7k rows) | dev-select gains vanish on dev-confirm | Only dev-confirm results gate shipping |
| OHS-3 contamination or targeting | Decontam hits; tasks overlap the families | Drop the hit items before pre-registration; never add targeted task types |
| Jev changes version | Version string differs | Pinned version; if unavailable, report both versions |
| Wide cards make us slower than Jev | Step S | Report per scenario. Cache definitions in T so per-call tokens scale with E, not with the card |
| Serving bugs (pads corrupt cached state; kernel path skips the block) | K0 or T0b | Pad blocking in all heads; call counter on the kernel |
| Compliance (bigger-model outputs leak into data) | Audit in G-0 | Remove affected rows before any run |

---

## 9. What would count as a research breakthrough, and what would not

**Would count** (each needs pre-registration, dev-confirm or OHS-3, and group-bootstrap CIs):
1. **Architectural separation that works beyond training.** A write-protected delta-rule memory (gate S) lowers held-out and best-of-N adaptive attack success by ≥ 20% relative against an equally trained, equally fed **datamarking** baseline. It must also cost no clean accuracy, show no over-defence, and pass the reliance test, which shows the effect runs through the protected state. To our knowledge that would be the first causal evidence for privilege separation inside a hybrid recurrent model.
2. **A 2B matching a closed decision API on fresh data**, i.e. OHS-3 non-inferiority within 2 pp. This is not expected (P ≈ 0.02–0.05), which is why it would matter.
3. **Selective answering with certified risk on new label sets** at useful coverage (≥ 20% at ≤ 2% risk) with only a few hundred customer labels.
4. **A 4B that beats Jev on OHS-3 accuracy with the CI above 0**, under the no-bigger-teacher rule.

**Would not count:**
- Beating Jev on hijack resistance. Jev is undefended (99–100% ASR), and training alone already gets 11% on the 4B **[M]**.
- Speed and cost wins. These are deployment advantages (self-hosted, near the caller), not model properties.
- G1 "trusted prefix is evidence-independent". That is causality, true of any decoder.
- Gains on OHS-2 tasks that the data families were chosen for, and JevBench half-A wins (a dev set).
- Point estimates inside their confidence interval, or dev-select gains that do not survive dev-confirm.
- Any robustness claim against white-box attackers. We do not run them, and PRISM-2B's weights will be public.

---

## Appendix A. Red-team corrections applied

| # | Correction | What changed in the plan |
|---|---|---|
| 1 | A 2B student of a 4B that trails Jev cannot win on accuracy or calibration | Goal re-scoped (§1). The accuracy claim moves to the 4B. A cheap teacher round (gate T) comes first. The 2B ships with honest claims |
| 2 | Components assumed incompatible layouts | One layout for everything: trusted schema → evidence → per-question branch → answer (§2). Gate L tests it against cygnet with twins, on clean and attack data |
| 3 | Budget did not fit ($10–13 asked from about $3 usable, and $23–35 from $30) | Account 1 is evaluation-only (≤ $3). The top-up funds one combined run + OHS-3 + 25% contingency + the $5 buffer. Many arms and tests cut |
| 4 | Measure A12/A13 before designing fixes | Step E0 decides whether twins, the slot head and round 2 are needed |
| 5 | Build and pre-register OHS-3 first; OHS-2-informed choices are deviations | G-0 builds OHS-3 before families are finalised. Families (a)–(d) are logged as deviations. OHS-2 is reported flagged |
| 6 | Separation claims overstated: G1 is causality, the read side can be steered or silenced, "8 bits" is false, the contrastive loss is malformed, the g argument used init values, off-by-one | §3.1 and §4 rewritten. Contrastive arm cut. P0 adds the β/g ablation. Block defined for t > m. p = 0.25. Datamarking baseline R3. Separation never credited with the win over Jev |
| 7 | The Brier gap is accuracy and resolution; the REL "win" is noise | Calibration target is yes/no accuracy + $b_w$. Post-hoc expected ≤ 0.005. The 95.5% target is shown to depend on $b_w$ (92.3% at 0.30). Complement ensembling dropped (no negation writer) |
| 8 | Accuracy numbers optimistic; κ claim false; the anchor pulls toward a weak model | OHS-3 prior 75 ± 2. κ = 0 on the 36 rows where the teacher would make a wrong label win. Anchor target changed to the teacher. Scaling, multi-view and soup gains removed |
| 9 | Cost used the wrong throughput; wide cards are slow | Cost at batch-1 latency, pre-registered ρ = 0.7, idle-inclusive also reported. Wide-card latency (~124 ms server) in the expected results. p95/p99 and cold starts required |
| 10 | Statistics too loose | Group bootstrap, realistic discordance (10–25%), dev-select vs dev-confirm, thresholds above SE, underpowered results labelled as such, 25% contingency, paraphrase consistency owned by the equivalence loss |
| – | Factual fixes | Jev at exactly 1.0 on 28% of OHS-2 items, not ≥ 50%. Bi-encoder loss range −3.7 to −10.0 (centre −6.9). The slot-head baseline is A12/A13, which already has 774 wide rows. The L1 fork is exact only when segments are tokenised separately. The compliance audit of the 9B/27B/35B probe outputs was added |
