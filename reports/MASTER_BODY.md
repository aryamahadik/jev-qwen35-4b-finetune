# Abstract
OpenDecide is an open, self-hosted decision model built to match or beat TypeSafe's closed decision model **Jev**
(jev-1.13). A decision model reads a text and answers a fixed question about it: a label, a yes/no or a choice among
options. Jev is a commercial API. Ours runs on one GPU.

We fine-tune open Qwen3.5 models with LoRA:
- **4B:** Qwen3.5-4B, the accuracy model.
- **2B:** Qwen3.5-2B, the fast model and the base for our own architecture, **PRISM**.

**Rules we kept:**
- Claude writes the training data. We never use a bigger model as a teacher and never train on Jev's outputs.
- Every claim is checked on test sets that were fixed and hashed before any model saw them.

**Results so far:**
- On a fresh, pre-registered exam (OHS-2, 1,320 questions, 13 tasks), our **4B scores 79.9 vs Jev 81.6**. The gap
  of -1.6 points is not statistically significant, so it is a **tie**.
- Our models are far harder to hijack than Jev: a planted "the answer is B" attack succeeds **1-4% of the time on
  ours vs 100% on Jev**.
- They answer about **25x faster** (9 ms vs 239 ms).
- They score higher on the public JevBench half we use for development.
- Jev still leads on **calibration** (yes/no Brier 0.038 vs 0.083) and on **consistency when a question is
  reworded**.

**PRISM** is our proposal for a secure decision architecture. The trusted rules and question are kept separate from
the untrusted text inside the network itself.
- The prompt-layout part is validated: layout E keeps accuracy and resists attacks.
- A first "protected memory" design (test F) failed on accuracy (-5.9 points) but proved the model can learn to rely
  on protected memory.
- The current design, **PRISM-X**, adds a trusted control plane on top of the model and takes nothing over:
  - an authority signal at every layer;
  - write-protected shadow memory;
  - trusted option queries;
  - a latent decision loop;
  - a learned confidence temperature.
- PRISM-X is coded and verified: at step 0 it gives exactly the old model's answers (difference 0.0). Its first
  training runs (arms H, I, J, K) are running tonight on a Google L4.

**Honest verdict:** the 4B is statistically level with Jev on accuracy and ahead on security, speed and cost. We have
**not yet beaten Jev on fresh-data accuracy or calibration**, and no claim of "beating Jev" is justified yet.

# 1. Executive summary (one page)
| Question | Answer |
|---|---|
| What are we building? | An open decision model that matches or beats Jev on accuracy, calibration, consistency, hijack resistance, speed and cost. |
| Best model today | **4B q35_4b_v11c** (Qwen3.5-4B + LoRA r16). The newer candidates v13t and blend50 are better on some practice sets, but neither has passed our +1.3-point bar. |
| Best 2B today | **q35_2b_v11r**. The best PRISM-layout 2B is **arm E**: 800 steps, clean data. |
| Fresh exam vs Jev | 4B **79.9 vs 81.6**, -1.6 [-3.3, +0.1], Holm p = 0.14, **a tie**. The 2B has not taken it (my estimate is about 74). |
| Where we clearly win | Hijack resistance (1-4% vs 100%), speed (9 ms vs 239 ms), cost (one GPU, open weights), public JevBench (dev set), complement and double-negation consistency, many-option questions. |
| Where Jev clearly wins | Calibration (Brier 0.038 vs 0.083), paraphrase consistency (flip 2.4% vs 5.7%). |
| Current best architecture | **PRISM-X** (Section 6): layout E + authority signal + shadow memory + option queries + decision loop + confidence temperature. Coded, tested and verified; results pending. |
| Money spent | About $140 of free and trial credit this month: Modal about $113, Google about $20, OpenRouter $3.42. |
| Next | H, I, J, K results, a longer PRISM-X run, a stronger 4B teacher, a clean final 2B, then the one-time OHS-3 exam. |

# 2. The goal, the opponent and the rules
**Jev** (TypeSafe, jev-1.13) is a closed decision model sold as an API. TypeSafe says it uses a new architecture,
parallel sampling and RLCD training for calibrated decisions. Its internals are not public.

**What "beating Jev" means for us.** Being better on each of these:
- fresh-data accuracy;
- calibration: yes/no Brier, and how well the confidence matches reality;
- consistency: complement, double negation, paraphrase and option order;
- hijack and injection resistance;
- speed and cost;
- JevBench.

**Integrity rules**, set by the user and kept throughout:
1. **No bigger teachers.** Only our own 4B may teach the 2B. Claude (Opus) writes the training data. No 9B, 27B or
   235B model is used as a teacher or baseline. Legacy data that was touched by bigger models (Qwen3-235B, Mixtral)
   is being removed, and its lineage is disclosed.
2. **Never train on Jev's outputs.**
3. **Never tune or choose on held-out tests:** OHS-1, OHS-2, OHS-3 and JevBench half B. Choices are made on
   **dev-select**, confirmed on **dev-confirm**, and a final exam is used once.
4. **No JevBench leaderboard submission and no public uploads** until the user says so.
5. **Secrets stay in `.env` files.** The OpenRouter and Vultr keys were pasted in chat and must be rotated.

**Glossary:**
- **LoRA:** a small add-on that fine-tunes a big model cheaply.
- **dev-select / dev-confirm:** two halves of our practice tests; we choose on one and confirm on the other.
- **Brier score:** how far the predicted probability is from the truth; lower is better.
- **ASR:** attack success rate.
- **Bootstrap CI:** a range of plausible values for a difference.
- **OHS:** our own held-out exams.

# 3. Timeline: everything we built and tried
| When | Round | What | Result |
|---|---|---|---|
| Early Sep | v0.1-v0.6 | GLiClass-style and first decoder models; JevBench harness; the "od" prompt | Learning the task; first comparisons (`reports/OpenDecide_v05_vs_Jev.md`) |
| mid Sep | v0.7 | Qwen3.5-4B, cygnet prompt (lettered options, one-letter answer), core mix | New base format |
| mid Sep | v0.8 | + LLM-written items (legacy: Qwen3-235B author, gpt-oss-120b checker) | Accuracy up; lineage now being removed |
| mid Sep | v0.9 | + "judge the response" rows | Fixed "too lenient" errors |
| mid Sep | v0.10 (q35_4b_v10) | + Wikipedia deletion debates; CUDA graphs for serving | JevBench all 231: 203 vs Jev 200. OHS-1: 76.1 vs 81.7 (lost) |
| 26 Sep | v0.11 / v11b | Task bank with Claude definitions, Claude hard items, binary fixes | v11 failed the gate; v11b OHS-1 77.9 vs 81.7 |
| 26 Sep | **v11c** | + 882 Claude standard-doctrine items | **OHS-2: 79.9 vs 81.6, a tie**; JevBench half A 107/118 vs 103 |
| 26 Sep | 2B v11, v11r | Distilled from v11c (kd 0.5), r32 | v11r: JevBench-A score 76.85 vs Jev 72.51; dev_nc 68.2 (gate 71.3: fail) |
| 26 Sep | E0 / P0 | Attack suites; untrained write-block checks | Jagged ASR Jev 100% / 4B 1.1% / 2B 3.9%; P0 GO |
| 27 Sep | v12t (4B) | Narrow Claude hard items | Gate fail (-0.69 on dev-confirm); in-family scores up 7-18 points |
| 27 Sep | v13t (4B, Google L4) | Breadth corpus (23 human-labelled datasets) + Claude items + replay | +0.64 (gate fail); **first calibration gain** (Brier -0.005); breadth_dev 76.8 → 80.5 |
| 27 Sep | blend50 | Weighted blend 0.5 v11c + 0.5 v13t | +0.57 (fail); 59,617 teacher labels made |
| 27 Sep | PRISM layout arms A-E (2B, 800 steps) | Prompt order and trust markers | **E passes**: equal accuracy, jagged 5.8%, OPI 2.3% |
| 27 Sep | Test F | E + protected memory (4 of 16 heads write-blocked) | **Failed**: -5.9 points; reliance proven (switch-off → 99.7% hijack); best OPI 1.1% |
| 28 Sep | **PRISM-X** | Additive control plane (H, I, J, K) | Coded, reviewed, CPU tests 58/58, GPU smoke passed; H-K running |

# 4. Measured results against Jev (all numbers are real runs)
## 4.1 Fresh exams
| Exam | Jev | Ours | Gap | Verdict |
|---|---|---|---|---|
| **OHS-2** (fresh, pre-registered, 1,320 questions, 13 tasks; used once) | 81.6 | 4B v11c **79.9** (80.5 with batch calibration) | -1.6 [-3.3, +0.1], p_holm 0.14 | **tie** |
| OHS-2, yes/no Brier | **0.038** | 0.083 | Jev better (p < 0.001) | Jev wins |
| OHS-1 (1,847 questions; it guided data choices, so it is **not clean**) | 81.7 | v11b 77.9, v10 76.1 | -3.7 / -5.5 | lost |
| 2B on the fresh exam | – | not tested (user's choice) | my estimate is about -7 | unknown |

The contamination check re-run on 28 Sep found **0 of 1,320** OHS-2 texts in any of about 198,000 training rows, and
none of the 13 OHS-2 datasets in the training data.

## 4.2 Security, speed and consistency
| Metric | Jev | 4B v11c | 2B v11r | Winner |
|---|---|---|---|---|
| Hijack audit (planted answer), ASR | 100% | 1.1% | 3.9% | **ours** |
| Prompt injection (OPI, with Jev's guard prompt), ASR | 1.3% | 1.0% | 2.4% | tie |
| Many options (eval_card) | 86.3 | 89.8 | 86.5 | **ours** |
| Speed, p50 per decision | 239 ms | – | **9 ms** | **ours** (about 25x) |
| JevBench half A (public, a dev set), questions right | 103/118 | 107/118 | 101/118 | 4B |
| JevBench half A, score v14 | 72.51 | 74.80 | **76.85** | **ours** |
| Complement consistency (lower is better; OHS-1) | 0.097 | 0.080 | – | **ours** |
| Double negation drift (OHS-1) | 0.162 | 0.101 | – | **ours** |
| Reworded question: answer flips (OHS-1) | **2.4%** | 5.7% | – | Jev |
| Reworded question: answer shifts (OHS-1) | **0.031** | 0.041 | – | Jev |

# 5. What we learned (the lessons that shaped the plan)
1. **Narrow hard data does not transfer.**
   - v12t raised its own test families by 7-18 points but lost 0.7 on broad dev.
   - Breadth (v13t) transferred better and gave the first calibration gain.
2. **Small gains are within noise.** Three 4B rounds each gave about +0.6 points. Our +1.3 bar (lower bound above 0)
   stopped us from fooling ourselves.
3. **Layout matters for security.**
   - Putting the untrusted text last before the answer invites hijacks (arm B: 65%).
   - Markers alone halve that. Markers plus a repeated trusted question fix it (arm E: 5.8%).
4. **Taking capacity from the model hurts; adding capacity is the way forward.**
   - Test F took over 4 of 16 memory heads and lost 5.9 points.
   - With its protection switched off, the trained F model was hijacked 99.7% of the time. So the network *can* learn
     to route its defence through protected memory. That is the key finding behind PRISM-X.
5. **Earlier "wins" were sometimes artefacts:** unequal prompts, bf16 ties, a helper that undercounted Jev. Every
   claim now uses a fixed Jev guard prompt, paired intervals and pre-registration.
6. **Honest calibration is Jev's strongest edge.** Its 0.038 Brier is far below ours. It is the hardest gap and the
   target of arm K.

# 6. Current best architecture: PRISM-X
## 6.1 The idea in one sentence
Keep **control** (the trusted rules, question and option definitions) separate from **data** (the untrusted text)
inside the network. Let trusted control decide how the untrusted evidence is read. **Add** this as a control plane on
top of the pretrained model and never take any of it over.

## 6.2 Prompt (layout E, validated)
The prompt is in this order:
1. **Trusted schema:** definitions, question, and the options with their definitions.
2. **The untrusted text,** between `<<<UNTRUSTED TEXT START>>>` and `<<<UNTRUSTED TEXT END>>>`, followed by a note
   that it is data.
3. **The trusted question repeated,** with short options.
4. **The answer letter.**

Every token gets a role:
- SYS (system prompt), SCHEMA (the trusted schema): trusted;
- DATA (the text): untrusted;
- QUESTION (everything after the text).

Roles never go back down along the sequence, so the text cannot mint a trusted token, not even by typing chat special
tokens.

## 6.3 The parts (every one starts at zero, so at step 0 the model is exactly arm E)
| Arm | Part | How it works | Zero-init |
|---|---|---|---|
| H1 | **Authority signal at every layer** | At the input of each of the 24 decoder layers, add A[layer, role] x RMS(h). ISE adds a role embedding once; we re-add it at every layer so it cannot fade. | A = 0 |
| H2 | **Shadow memory** | In each of the 18 Gated DeltaNet layers, 2 extra memory heads, copied from the heads that forget slowest. They write only during the trusted prefix: write strength beta and decay g are set to 0 afterwards, so the text can read them but never write, overwrite or erase them. Output is added through a gate tanh(gamma). All 16 original heads stay. | gamma = 0 |
| I | **Option-query head** | Each option's line in the schema (with its definition) plus the question gives a trusted query. It attends over the text tokens and a small scorer adds a score to that option's letter logit. The text cannot steer which evidence is looked for. | last layer = 0 |
| J | **Latent decision loop** | The per-option decision state z is refined 1-4 times: re-query the text, compare options (self-attention across options), residual update. Training draws the depth per step; inference uses 4 or stops early once confident. | via the zero scorer |
| K | **Confidence temperature + loop ensemble** | Per question, tau = exp(0.75 tanh(w.f)) divides the logits, learned to calibrate. At inference the probabilities of all loop steps are averaged. Aimed at Jev's Brier lead. | w = 0, so tau = 1 |

Size: about 51 million new parameters for arm J on the 2B, about 2% of the model. Speed: the head and loop work on the
final hidden states and the shadow heads add about 12% to each memory layer, so latency should stay near 10 ms (to be
measured).

## 6.4 The math (short)
**Shadow head** (per layer and head):
- State update: S_t = exp(g_t) S_(t-1) + beta_t k_t (v_t - S_(t-1)^T k_t)^T, with beta_t = g_t = 0 after the
  trusted prefix, so S is frozen after the prefix.
- Output: o_t = S_t^T q_t, gated-RMS-normed, multiplied by tanh(gamma) and projected back into the model.

**Authority signal:** h_l ← h_l + A_l[role] ⊙ RMS(h_l).

**Final logit** for option i: (letter logit_i + s_i(z_i^T)) / tau.

**Training** keeps the proven loss unchanged:
- soft-label cross-entropy with the teacher (kd 0.5);
- consistency terms (complement, equivalence, invariance to attacked twins, option-order twins);
- a KL anchor to the base model.

## 6.5 What is guaranteed and what is not
- **Guaranteed (by construction):**
  - The text cannot write into shadow memory.
  - The option queries are computed only from trusted tokens (causality).
  - At step 0 the model equals E exactly. Measured: log-probability difference **0.0** on Modal H100 and on the
    Google L4.
- **Not guaranteed:**
  - What is *read* from shadow memory depends on a query that has seen the text.
  - The final decision still reads the text as evidence.
  - So PRISM-X lowers the risk but is not a proof like CaMeL's symbolic separation. Accuracy gains are hypotheses
    until H to K report.

## 6.6 Verification done (28 Sep)
| Check | Result |
|---|---|
| Independent code review (read-only) | 5 real issues found, all fixed |
| CPU tests | **58/58 pass** (prompt spans, roles, zero-init, head gradients, shadow slicing, presets, all old loss tests) |
| Modal H100 smoke (arm J, 6 steps) | self-check 0.0; every hook fired; losses finite; 48/48 predictions valid; reload from disk matches 48/48 |
| Google L4 smoke (arm J, 8 steps, batch 16) | self-check 0.0; peak memory 7.2 GB of 22; parts learning |

# 7. Tonight's experiments (running while this document was made)
- **Where:** Google Cloud L4 (VM od-l4), one GPU; the quota is 1.
- **What:** arms H, I, J and K run in a queue, each matched to arm E: same data (59,617 clean rows with blend-teacher
  labels), same seed, 800 steps, same loss and same 13 test sets, plus a switch-off comparison.
- **Speed:** about 18 s per step, so about 4.5 h per arm including tests.
- **Timing:** H started 03:31 UTC and its results are expected about 08:30 UTC, followed by I, J and K.

| Arm | Pass bar (fixed in advance) |
|---|---|
| H | dev-confirm at least -0.5 points vs E; OPI at most 1.3%; jagged at most 8.8% |
| I | dev-confirm at least +1.3 points vs E, with the interval's lower bound above 0 |
| J | better than I on hard_dev and breadth_dev; no loss on dev-confirm |
| K | Brier better than J and than E; accuracy not below J by more than 0.3 |
| Follow-up | best arm (by dev-select) re-trained at 1,600 steps: the arms are under-trained, about -3 points vs v11r |

**Also pre-registered for later: counterfactual evidence scoring.** The model answers once more with the untrusted
text removed and learns, per question, how much of that no-evidence guess to subtract. It is a learned version of the
batch calibration that gave +0.6 on OHS-2.

# 8. Infrastructure, credits and safety
| Resource | State |
|---|---|
| **Google Cloud** (project system-one-509903) | L4 VM od-l4; quotas: 1 GPU, 12 CPUs (a 4-GPU request is not approved). Budget kill switch: at $250 it deletes VMs, at $285 it unlinks billing. About $280 credit left. Disk snapshot od-l4-snap kept as a backup. |
| **Modal** (4 accounts: mahadikarya2, mahadikarya3, mahadikarya44, atmosphor) | About $7 left in total (1.62 / 1.01 / 1.30 / about 2.95). The $30 monthly refill is expected 1 Oct (unconfirmed). |
| **OpenRouter** (Jev API calls only) | $6.58 left of $10 |
| **Azure** | $200 credit, locked by a deny-all policy and a budget (no GPU quota; MFA needed). The free credit likely expires 30 days after sign-up. |
| **Vultr** | About $300 credit; big GPUs locked; the API key is IP-restricted |
| **Keys to rotate** | OpenRouter and Vultr (both were pasted in chat) |

# 9. Roadmap to beat Jev
1. **Finish the PRISM-X ladder** (H, I, J, K, then the 1,600-step follow-up): about 1-2 days on the L4, about
   $20-30. Freeze the best PRISM-X design.
2. **Stronger 4B teacher:**
   - a large, selected dataset (100-150k rows built from the 12.8k-row mistake list, with paraphrase and
     soft-label twins);
   - one strong 4B run with a +2-point gate;
   - add the PRISM-X parts that won (H is cheap to add).
3. **Calibration and paraphrase work:**
   - the confidence head (arm K) and counterfactual scoring;
   - the paraphrase gate;
   - post-hoc temperature and batch calibration.
4. **Clean final 2B:** trained from base on a clean mix (no legacy 235B or Mixtral rows), distilled from the new 4B,
   using the frozen PRISM-X design.
5. **OHS-3 final exam, once,** after a pre-registration amendment naming the models and their checkpoint hashes.
   Report everything, whatever the direction.
6. **Only then**, and only with the user's OK: a JevBench submission and public release.

**Compute need** for the full plan: about 70-90 H100-hours; the lean version about 15-20. Options:
- the Modal refill (about $120 a month over 4 accounts, about 1 day);
- the Google L4 (about 3 days, about $65);
- Lambda GH200 at $2.29/h;
- Vultr GH200 at $1.99/h (needs an unlock);
- Azure spot A100 at $0.77/h (needs quota).

# 10. Honest verdict
**How good is it really?**
- **Credible achievement.** With about $140 of free credits, a student team built an open 4B decision model that:
  - **statistically ties** a commercial closed decision model on a fresh, pre-registered, contamination-checked exam;
  - is **far harder to hijack** (1-4% vs 100%);
  - answers **about 25 times faster**;
  - scores higher on the public JevBench development half.

  The method is research-grade: fixed held-out exams, paired bootstraps, pre-registered gates, and every negative
  result reported.
- **Not yet a win.**
  - Jev is still ahead on fresh-data accuracy by 1-1.6 points (not significant, but in its favour).
  - Jev is clearly ahead on calibration and on paraphrase consistency.
  - The 2B has never taken a fresh exam.
  - **Nobody can honestly say "we beat Jev" today.**
- **PRISM.**
  - The layout finding (E) is solid.
  - The protected-memory idea has a real positive signal: the model learns to rely on it.
  - PRISM-X is a principled, verified design, but it has **no accuracy results yet**.
  - Claims of a "breakthrough" must wait for H to K and a fresh exam.

**My probability estimates** (judgement, not measurement):

| Outcome | Chance |
|---|---|
| 4B at least ties Jev on the final exam | high |
| 4B clearly beats Jev on fresh accuracy after the stronger-teacher round | about 50% |
| 2B matches Jev's fresh accuracy | about 1 in 3 |
| We beat Jev on security, speed and cost | about 100% (already true) |
| We beat Jev on calibration within this plan | below 50% |

**Bottom line:** we are level with Jev where it is hardest (accuracy) and far ahead where it is weakest (security,
speed, cost). The remaining work is the stronger teacher round, calibration, and one honest final exam.

# Appendices (full project records, converted from the working documents)
The following parts reproduce every project document so that nothing is lost:
- the handoff;
- the complete run ledger with every run and its cost;
- the PRISM-X guide and the overnight plan;
- the PRISM-2B master plan and the freeze plan;
- the three exam pre-registrations;
- the design documents and scouting reports;
- the research notes;
- the benchmark documentation and results;
- the earlier reports.

The earlier PDFs (Progress Report, 27 Sep; OpenDecide handoff) are attached at the end.
