# V_other: checking the "other" claims in the OpenDecide-4B ARC proposal (verifier B)

Date: 4 Oct 2026. Planning only: no Modal, gcloud or paid calls were made. No forbidden folder was opened
(bench/external_quarantine/, data/ohs3*, lean/ohs3/, prep89/, sealed_nd/, sealed_brief/). The local facts come from
`opendecide-data/lean/train_decoder.py`, `opendecide-data/lean/decoder_io.py`, `opendecide-data/lean/logs/budget_ledger.md`
(X12, X14, X15), `bench/decision_index/report_sample10k.json` + `preflight_sample10k.json`, and
`reports/knowledge_gap/R_measure.md`.

## The short answer (plain words)

- None of the six claims touch the main reason we lose the Decision Index (DI). The DI gap is 4.68 points
  (54.83 vs 59.51). The knowledge area alone makes up **3.53** of them: (51.2 - 68.9) / 5. That area covers GPQA, GSM8K,
  CRUXEval, MMLU, ChessBench and CLadder. Typed heads, two-stage top-k, calibration RL, replay and option-query heads do
  not add knowledge or reasoning. At most they work on the other **1.15** points and on Brier.
- Our own data already answers two of the claims. (a) The option-query head (PRISM-X) did not help the 4B
  (X15: +0.59 select, -0.59 confirm, so about 0). (b) Our calibration is already better than Jev's where we measured it
  (OHS-2 yes/no reliability 0.0041 vs Jev 0.0071). The Brier gap there comes from accuracy, not calibration.
- What is real and cheap: (1) a **Brier term in the supervised loss** (no RL needed), (2) a **forgetting check before
  any replay**, (3) a **per-option-count breakdown** of DI errors before building a two-stage chooser.

| # | Claim | What the source really shows | Evidence strength (for OUR setting) | Expected gain for us |
|---|---|---|---|---|
| 1 | Generic pretraining replay: "up to 1.87x data efficiency" | Real paper (Kotha & Liang, Stanford, Mar 2026). 1.87x is the **validation LM loss** of a **150M** model with **full** fine-tuning on Flan (4M target tokens). At 8B: +4.5 pts web navigation, +2 pts Basque, full fine-tuning, no error bars | Strong in its own setting, **weak** for LoRA letter-classification. No LoRA, no classification, no 4B tests | DI 0 to +0.3 index; OHS about 0. Only matters if C1 has forgotten something, and that is unmeasured |
| 2 | Calibration-aware decision RL | RL with Brier/log rewards fixes **verbalized** confidence after reasoning (Qwen2.5-7B, Llama-3.1-8B). Accuracy roughly flat (-1.6 to +2.3) | Strong for verbalized confidence, **not needed** for logit readouts. With a finite output read in one pass, a supervised proper-scoring loss (CE = log score, + Brier) optimizes the same target exactly | Brier -0.000 to -0.005; accuracy 0. Risk: softer outputs cost points under the JevBench v1.5 abstain rule |
| 3 | Typed heads (sigmoid yes/no with complement rule; ordinal thresholds) | A sigmoid yes/no is **mathematically the same** as our 2-way Yes/No softmax. The complement rule is **already in our loss**. CORAL/CORN gains are on images and LSTMs; on text they sit inside the noise; no LLM test found | Weak | 0 to +0.5 on yes/no; ordinal about 0 (our A4 term already is the LLM-tested TRACT-style loss) |
| 4 | Two-stage top-k for 100+ options | Strong for **tool selection** with long tool docs in generative LLMs (13.62% -> 43.13%; 87.1 -> 93.1). TypeSafe does it only **above** 255 options and tells users to send full lists | Moderate in general, weak for DI | DI at most about +0.6 index, even if POP909-CL and ChessBench gaps closed fully; likely +0.0 to +0.2 |
| 5 | Permutation-equivariant option heads replace letter logits | Set-LLM (NeurIPS 2025, LoRA): +1.5 to +2.8 vs a single ordering at 3B, but **about equal to permutation averaging at 7-8B**. Our 4B A/B: about 0 | Moderate (outside), **strong negative** (ours, same model) | 4B accuracy 0 (+-0.6). Real gains: fewer definition overwrites (10.2% vs 16.5%) and 1 read instead of 2 on choice rows |
| 6 | TypeSafe statements on Jev | Verified quotes: "new model architecture, parallel sampler ... RLCD"; up to 255 options; "2 stage-system of scoring independently then making an explicit choice"; Score levels "judged on its own". Size, reward and architecture are unknown | Primary source, but marketing; nothing measurable | Not a gain. It is a hint that Jev scores each option on its own |

---

## 1. Generic pretraining replay ("up to 1.87x")

**Paper found.** Suhas Kotha and Percy Liang, "Replaying pre-training data improves fine-tuning", arXiv 2603.04964,
5 Mar 2026. Links: https://arxiv.org/abs/2603.04964 and https://arxiv.org/html/2603.04964v1. The authors' thread
(https://x.com/kothasuhas/status/2029983689988542742) names Percy Liang (Stanford).

**What the 1.87x is**
- Abstract: "generic replay increases target data efficiency by up to 1.87x for fine-tuning and 2.06x for
  mid-training".
- Setup: **150M**-parameter models, **4M target tokens**, **4B total tokens**, C4-style generic data. Full fine-tuning
  with its own cosine schedule and the optimizer reset. Metric: **validation LM loss** on the target domain. The
  authors chose it because "downstream accuracy is not better than random chance at our pre-training scale".
- The gain depends on the target domain: **1.87x** for Flan (instructions), **1.49x** for FineMath, **1.09x** for
  StarCoder (code, the domain furthest from C4). With a two-stage mid-training schedule the paper reports 1.53x, 2.49x and
  **4.80x**.
- When it fails: "when we keep 75% of the target data for pre-training, replay is no longer helpful". So replay helps
  most when the target domain is **rare** in pretraining.
- 8B tests: **Llama 3.1 8B Instruct**, full fine-tuning (LoRA is never mentioned). Web navigation (WebLINX): 32.86%
  baseline, "up to 4.5%" better with instruction-data replay (OpenHermes/UltraChat). Basque (200M Latxa tokens,
  COPA-style QA): "up to 2%" better with SlimPajama replay. No seeds and no error bars are reported. The paper does not
  give one best replay fraction: "a non-zero replay fraction minimizes the loss" for each domain, and "a large range of
  replay fractions" helps. **The "~20%" in the proposal is not a number from this paper.**

**Does it apply to us (LoRA r16, letter-logit classification)?**
- Different regime. We train **32.5M LoRA parameters**, not all weights. LoRA already "learns less and forgets less"
  (Biderman et al., TMLR 2024, https://arxiv.org/abs/2405.09673). Their tests were code and maths, 7B models,
  about 100K instruction pairs and 20B tokens.
- Different loss. Our target is cross-entropy on a few answer tokens, not LM loss on whole documents. Generic-text
  replay would train a different head (next-token prediction on all tokens).
- **We already do a form of replay.** The trainer's `anchor` term is a KL to the frozen base model on "breadth rows"
  (docstring: "learning-without-forgetting / self-distillation"). This is replay in function space, not in data space.
- Is there anything to protect? R_measure.md says a 4B read in one pass with no chain-of-thought scores "roughly where
  C1 is now (about 40)" on GPQA. Qwen3-4B non-thinking scores 41.7; C1 scores 39.8. There is **no measured evidence that
  C1 forgot knowledge**. The knowledge gap is mostly missing thinking time, not forgetting.

**Expected gain for us:** DI 0 to +0.3 index points, OHS about 0. This is my estimate and the evidence for it is weak.
**Cheap first step:** score the base Qwen3.5-4B and C1 on the same non-DI knowledge dev items (e.g., the SuperGPQA or
MMLU-Pro-non-MMLU sets listed in R_measure.md) with the same letter readout. If C1 >= base, replay has nothing to
recover.

## 2. Calibration-aware decision RL

**Papers (all use generative models with verbalized confidence):**

| Paper | Model | Reward | Calibration result | Accuracy result |
|---|---|---|---|---|
| RLCR, "Beyond Binary Rewards" (Damani et al., arXiv 2507.16806, https://arxiv.org/abs/2507.16806) | **Qwen2.5-7B** | correctness + Brier on a verbalized `<confidence>` | HotpotQA ECE 0.37 (RLVR) -> **0.03**, Brier 0.37 -> 0.21; math ECE 0.26 -> **0.10**, Brier 0.28 -> 0.17; OOD ECE 0.46 -> 0.21 and 0.49 -> 0.25 | HotpotQA 63.0 -> 62.1; math 72.9 -> 72.7; OOD 53.9 -> 56.2 and 52.5 -> 50.9 |
| Rewarding Doubt (Bani-Harouni et al., arXiv 2503.02623, https://arxiv.org/abs/2503.02623) | Llama-3.1-8B | log scoring rule on stated confidence | ECE 0.0256 vs 0.2771 (verbalize baseline), AUROC 0.879 vs 0.677 (numbers from a secondary summary, https://www.alphaxiv.org/overview/2503.02623v1; not checked in the PDF) | not reported in the abstract |
| Taming Overconfidence in RLHF (Leng et al., arXiv 2410.09724, https://arxiv.org/abs/2410.09724) | Llama3-8B, Mistral-7B | PPO-M / PPO-C | lower calibration error (exact numbers not extracted) | "comparable to standard PPO" |
| DCPO (Ma et al., ICML 2026, arXiv 2603.09117, https://arxiv.org/abs/2603.09117) | not extracted | decoupled confidence advantages | finds an "accuracy-calibration gradient conflict" in RLVR; "superior calibration" | "comparable" |
| Tan et al., arXiv 2607.04332 (https://arxiv.org/abs/2607.04332) | not extracted | several confidence rewards | warns of "confidence reward hacking"; the best reward differs by dataset | - |
| Turtel et al., arXiv 2505.17989 (https://arxiv.org/abs/2505.17989) | 14B reasoning model | forecasting outcomes | "greatly improving probabilistic calibration" vs frontier models | matches o1 |

**Takeaways**
- In all of these, the confidence is **sampled text written after reasoning**. RL is needed because the number is not
  a differentiable function of the weights. RLCR also beat supervised post-hoc classifiers, but those were separate
  heads trained after RLVR, which is not our case.
- **Accuracy does not reliably go up** (-1.6 to +2.3 points). The gain is calibration.
- **Supervised vs RL when the outputs are finite (our case).** We read a full probability vector from one forward
  pass. The expected Brier or log reward is then a closed-form, differentiable function of those probabilities, so its
  exact gradient is available. Policy-gradient RL would estimate the same gradient with noise. Cross-entropy on gold
  labels **is** the log score, a strictly proper scoring rule (Gneiting & Raftery 2007,
  https://doi.org/10.1198/016214506000001437), and a Brier term can be added as a plain loss. RL only helps when the
  reward depends on something sampled or non-differentiable: a chain-of-thought, a thresholded metric (e.g., the
  JevBench v1.5 abstain band), or set-level "case-exact" scores. That is my reasoning, not a published head-to-head;
  I found **no paper** comparing RL against a supervised proper-scoring loss for a one-pass logit readout.
- **Our numbers say calibration is not our gap.** Ledger X12 (OHS-2 yes/no): Jev Brier **0.037**, reliability (REL)
  **0.0071**; our 4B Brier **0.083**, REL **0.0041**. Brier = REL - resolution + uncertainty (Murphy decomposition), so
  perfect calibration could remove at most our 0.004 REL, about **9%** of the 0.046 gap. The rest is resolution, which
  means accuracy. For the DI Brier (0.140 vs 0.114) the split between the two is **unknown**. Decomposing it is free if
  per-item predictions were saved; whether they were is unknown (only aggregates are in `bench/decision_index/`).
- **Risk.** JevBench v1.5 counts a yes/no answer with 0.2 < P(yes) < 0.8 as an abstention, scored as wrong (memory
  note, 30 Sep). A Brier-optimal model gives more middle probabilities on hard items, which costs points there.

**Expected gain:** Brier -0.000 to -0.005; accuracy about 0. Use a supervised Brier/CE term plus the existing
temperature fit; there is no case for building an RL loop.

## 3. Typed heads (sigmoid yes/no with complement; ordinal thresholds)

**Sigmoid yes/no.** softmax([l_yes, l_no])_yes = sigmoid(l_yes - l_no). Our Yes/No readout is already a sigmoid
head, so this change gives zero gain.

**Complement rule s(not x) = -s(x).** This is **already in our loss**. `train_decoder.py`: "complement (pA + pB - 1)^2"
and, with `sym_cons`, "symmetric KL between p_a and p_b with yes/no swapped". A hard version would need the "not x"
question at inference: read twice, then average p(x) and 1 - p(not x). That doubles the cost of yes/no reads, which
are 84% of DI questions. Outside evidence:
- CCS (Burns et al., arXiv 2212.03827, https://arxiv.org/abs/2212.03827) uses this exact negation-consistency idea
  for unsupervised probes: "+4% on average" over zero-shot, 6 models, 10 datasets. This is not fine-tuning.
- ConCoRD (Mitchell et al., EMNLP 2022, https://arxiv.org/abs/2211.11875): "+5% absolute" on ConVQA with LXMERT,
  using NLI factor graphs.
For a 4B model already fine-tuned with a consistency loss, expect **0 to +0.5**.

**Ordinal threshold heads (CORAL/CORN).**
- CORN (Shi, Cao, Raschka, Pattern Analysis and Applications 2023, https://arxiv.org/abs/2111.08851), MAE:
  - Images: MORPH-2 CE 3.73 / CORAL 2.99 / CORN 2.98; AFAD 3.28 / 2.99 / 2.81.
  - **Text (LSTM)**: TripAdvisor CE 1.10+-0.09 vs CORN 1.07+-0.05; Coursera 1.02+-0.13 vs 0.95+-0.12. These
    differences are **inside the noise**, and CORAL had the best RMSE.
- **No paper found that puts CORAL/CORN on an LLM readout.** The LLM evidence is for regression-aware losses instead:
  - RAFT (Lukasik et al., ICLR 2025, https://proceedings.iclr.cc/paper_files/paper/2025/file/ae3bb0adcdce28afb5f7e86a79b6cffa-Paper-Conference.pdf).
  - TRACT (Chiang, Lee, Lukasik, arXiv 2503.04381, https://arxiv.org/abs/2503.04381), Mistral-7B, mean Pearson:
    CE+decode **0.557** -> RAFT+RAIL **0.623** -> TRACT **0.650**.
  - Our A4 `lam_ord` term **is** TRACT's squared error on the expected level.
- TypeSafe's Score type is **not** a threshold head: "each level is judged on its own against the state", "The model
  doesn't see a level's number or its neighbours", and at most 10 levels
  (https://docs.typesafe.ai/primitives/score.md).
- Ordinal rows are about 4,350 of the 501,732 training rows (<1%), and DI scores mostly accuracy, not MAE.

**Expected gain:** ordinal about 0 on DI and OHS. Not worth a new head.

## 4. Two-stage top-k for 100+ options

**Outside evidence (all tool selection with generative LLMs):**
- RAG-MCP (Gan & Sun, arXiv 2505.03275, https://arxiv.org/abs/2505.03275): retrieving first raised tool-selection
  accuracy from **13.62% to 43.13%** and cut prompt tokens by more than half.
- Meta, "How Many Tools Should an LLM Agent See?" (arXiv 2605.24660, https://arxiv.org/html/2605.24660v1):
  - BFCL (370 tools): 90.3% coverage at K = 7.4, against a fixed list needing K = 50 for 90.8%.
  - With a Claude Sonnet chooser: adaptive short lists **93.1% vs 87.1%** with a fixed 5 (76.8 vs 60.9 on medium
    queries).
- Infer-Retrieve-Rank (D'Oosterlinck et al., arXiv 2401.12178, https://huggingface.co/papers/2401.12178): state of
  the art on extreme multi-label classification with thousands of labels.
These gains come from **prompt bloat** (long tool docs, thousands of options). In our case the options are short and
there are at most 151.

**TypeSafe:**
- "Jev supports a cardinality up to 255. For the higher cardinality choices, we do a 2 stage-system of scoring
  independently then making an explicit choice" (https://typesafe.ai/blog/introducing-system-one-models-and-jev).
- The docs say: "A Choice question accepts up to 255 options ... give the model the full list ... rather than a
  shortlist" (https://docs.typesafe.ai/primitives/choice.md).

**Our DI facts (local preflight + report):**
- The DI maximum is **151 options**, and no request is over 255. Our readout already covers up to 255 (two-letter
  single tokens after Z, `decoder_io.WIDE`). ToolRet and BRIGHT are already split by the harness into per-candidate
  yes/no questions.
- Benchmarks with more than 26 options, ours vs Jev:
  - CLINC150 (151 options; not in the index): 81.2 vs 89.3.
  - **POP909-CL** (129; in the index): 8.7 vs 18.1.
  - BANKING77 (77; not in the index): 78.9 vs 79.7, a near tie.
  - API-Bank (53; not in the index): 63.5 vs 88.2.
  - **ChessBench** (53; in the index): 11.7 vs 17.2.
- The near tie at 77 options shows that the **number of options alone is not the cause**.

**Expected gain:** closing the full POP909 and ChessBench index gaps would be worth about +0.6 index at most. A
two-stage chooser would plausibly get +0.0 to +0.2. **Cheap first step (CPU, free):** bucket C1's existing DI errors
by option count (2-4, 5-26, 27+), if per-item predictions are available.

## 5. Permutation-equivariant option scoring vs letter logits (4B)

**Outside evidence**
- Selection bias is real for zero-shot letter readouts. Zheng et al. (ICLR 2024, https://arxiv.org/abs/2309.03882)
  tested 20 LLMs and traced the bias to the "token bias" on option IDs. Wang et al., "Look at the Text" (COLM 2024,
  https://arxiv.org/abs/2404.08382), found first-token probabilities less robust than text answers once mismatch is high.
  Both look at **un-fine-tuned** readouts. We fine-tune with shuffled options every draw and a permutation-twin JS loss.
- Set-LLM (Egressy & Stuhmer, NeurIPS 2025, https://arxiv.org/abs/2505.15433) is the closest test: LoRA r8,
  fine-tuned per benchmark, random-order accuracy on PIQA / ARC-C / CSQA / SIQA.

| Model | Single run, causal | Majority vote over all orders | Set-LLM (one run) |
|---|---|---|---|
| Llama 3.2 3B | 86.92 / 74.16 / 81.32 / 77.54 | 86.83 / 76.37 / 81.57 / 77.99 | **88.41 / 75.85 / 83.29 / 80.30** |
| Gemma 7B | 92.82 / 83.52 / 85.45 / 80.93 | 92.66 / 85.58 / 85.75 / 81.10 | 92.98 / 83.45 / 84.93 / 81.12 |
| Llama 3.1 8B | 90.81 / 83.04 / 83.96 / 80.77 | 90.75 / 85.32 / 84.11 / 81.12 | 91.62 / 84.13 / 85.34 / 81.47 |

  At 3B, Set-LLM gains +1.5 to +2.8 over a single ordering. At 7-8B it roughly equals averaging over orderings: about
  -0.5 points on average for Gemma 7B and +0.35 for Llama 8B. C1 already averages 2 orders (given + reversed) and flips
  on only 2.4% of items.
- "Likelihood Ranking doesn't Scale Like Prompting in LLMs" (arXiv 2609.29390, https://arxiv.org/abs/2609.29390; 95
  models, 0.1-100B): scoring the option **text** improves much less with scale than prompted answering. This is a
  warning against replacing letters with per-option text scoring that has no fine-tuning.

**Our own evidence (strongest, same model):**
- Ledger X15, 4B with PRISM-X I against 4B-E, both 800 steps on the same recipe: **+0.59 [-0.10, +1.25] select,
  -0.59 [-1.21, +0.02] confirm**. Yes/no 85.4 vs 85.8, choice 75.7 vs 76.6.
- Definition-overwrite rate 10.2% vs 16.5%: better for PRISM-X.
- On the 2B, PRISM-X gave +2.1. This matches the Set-LLM pattern: gains at small size that fade by 4-8B.
- `bench/v154/README.md` notes that CUDA graphs are "not possible for PRISM-X", so it would cost latency.

**Expected gain:** 4B accuracy 0 (+-0.6). Possible side gains: definition-overwrite resistance, and dropping the
second read on choice rows (16% of DI questions). **Do not replace letter logits on the 4B** unless a new A/B beats
X15's result.

## 6. TypeSafe's public statements on Jev (verified 4 Oct 2026)

| Topic | Exact public wording | Source |
|---|---|---|
| Stack | "a new model architecture, parallel sampler for maximum efficiency, and training method we call Reinforcement Learning for Calibrated Decisions (RLCD)" | https://typesafe.ai/blog/introducing-system-one-models-and-jev |
| Sampler | "Generates all outputs in a single query. Incredibly efficient and hardware-aware." | same |
| Typed outputs | "Possible outputs and structure are defined in advance ... The model never makes type errors." Three types: Choice, Score (up to 10 levels), Noul (P(yes)) | blog; https://docs.typesafe.ai/primitives.md, /primitives/score.md |
| 255 / two-stage | "Jev supports a cardinality up to 255. For the higher cardinality choices, we do a 2 stage-system of scoring independently then making an explicit choice." Docs: "A Choice question accepts up to 255 options" | blog; https://docs.typesafe.ai/primitives/choice.md |
| Isolation | "Every question is evaluated in parallel and in isolation against the same state in one go." Score: "each level is judged on its own"; "The model doesn't see a level's number or its neighbours" | https://docs.typesafe.ai/ ; /primitives/score.md |
| RLCD | "trains TypeSafe to return decisions and calibrated probabilities instead of generated text"; contract: "The model does not generate text. It returns decisions and probabilities." | https://docs.typesafe.ai/introduction/machine-learning-primer.md |
| Model | "the same weights serve every account", "not fine-tuned or LoRA-adapted with customer data"; 64k context (32k state + longest question) | https://docs.typesafe.ai/models.md |
| Unknown | parameter count, backbone, RLCD reward/algorithm, sampler design, any paper | dsebastien.net: "TypeSafe hasn't published how RLCD works" (https://www.dsebastien.net/reinforcement-learning-for-calibrated-decisions-rlcd/). HN: a TypeSafe account says RLCD probabilities are optimized "against outcomes" and a paper "may" come (from our 25 Sep notes, not re-checked: https://news.ycombinator.com/item?id=49717558) |

**What this tells us:** the clearest public hint is that Jev **scores each option or level on its own** and then picks.
That is per-option, order-free scoring, close to an option-query head rather than letter logits or CORAL thresholds.
But "parallel sampler" refers to questions answered in parallel, not latent recurrence. Nothing public mentions replay,
latent thoughts, halting or an error head. Jev's GPQA Diamond score of **78.3** (DI sample; 78.6 in the full report) in
one pass suggests a much larger model than our 4B. Size is undisclosed; the memory note estimates <= 30B active.

## What this means for the ARC plan

1. Keep the letter readout on the 4B (our A/B plus Set-LLM at 7-8B). Option-query heads are a 2B tool.
2. Replace "calibration RL" with an optional **supervised Brier term** on top of CE. Decompose the DI Brier first.
   Keep the JevBench abstain band in mind.
3. Drop the new typed heads: sigmoid = what we have, complement = already in the loss, ordinal = A4 already.
4. Two-stage top-k only if the free option-count breakdown shows that 27+-option items drive the losses.
5. Replay only if the free forgetting check shows that C1 is below base on non-DI knowledge items.
6. The knowledge area (3.53 of the 4.68-point DI gap) needs the separate knowledge-gap plan
   (`reports/knowledge_gap/`), not these components.

Any Modal test of items 1-5 must be a dev-only, 800-step L4 A/B like X14/X15, map to a numbered /goal step, and leave
the frozen A16 round-1 plan untouched.
