# OpenDecide vs Jev: projection for OHS-3 and JevBench (30 Sep 2026, about 20:10 UTC)

**What this is.** A transparent model of where the three final systems will likely land against Jev (jev-1.13):
- the final 4B (the new `q35_4b_main500k` if it passes the ship rule, otherwise 4B-E);
- the final 2B (PRISM-X I, 4B-E teacher labels);
- the 2B→4B cascade.

**Every number below is either measured (with its file) or marked EST (a judgement, with a range).** No OHS-3 item text was opened; OHS-3 facts come only from `PREREG_OHS3.md` and `data/ohs3_summary.json`. There were no GPU, Modal, gcloud or paid calls.

**Files (all under `lean/projection/`):**
- `evidence.md`: the measured evidence table this builds on (§ numbers below refer to it).
- `model/project.py` → `model/project_out.txt`: Monte Carlo of the accuracy chain, Brier and consistency (400K draws, seed 0), plus the joint probabilities.
- `model/sensitivity.py` → `model/sensitivity_out.txt`: one assumption changed at a time.
- `model/cascade_ext.py` → `model/cascade_ext_out.txt`: a new, read-only extension of `cascade_sim.py`. It covers routing budgets of 10-90%, gives CIs, splits yes/no from choice, and adds the cascade ASR on eval_jagged / eval_opi.

**Signs.**
- Gap = ours − Jev, in pp. Positive means we are better.
- Brier diff = ours − Jev. Positive means we are worse.
- "80%" means the 10th-90th percentile of the projection.

---

## 0. Bottom line

**The honest headline.**
- Held-out accuracy is roughly a coin flip. The projected median gap is **+0.3 pp** for the final 4B; the headline figures come from the Monte Carlo in `model/project_out.txt`.
- The yes/no-vs-Jev picture on OHS-3 is genuinely unknown. OHS-3's yes/no tasks are unlike the ones where we lost before.
- Brier is likely lost.
- Hijack resistance is a near-certain win.
- Speed and cost are wins only if we host properly and pre-register the definition.
- The 2B is very unlikely to match Jev on accuracy (P about 0.1).
- The cascade adds no accuracy over the 4B alone. It is also *slower and costlier* than the 4B alone, because the PRISM-X 2B cannot use CUDA graphs.

| Win condition | Final 4B | Final 2B | Cascade |
|---|---|---|---|
| OHS-3 accuracy ≥ Jev (point estimate) | **0.54** | 0.09 | 0.48 |
| OHS-3 accuracy "matches" (PREREG: 95% LB > −2.0) | **0.60** | 0.11 | 0.54 |
| OHS-3 accuracy not significantly worse | 0.76 | 0.21 | 0.71 |
| OHS-3 yes/no ≥ Jev | 0.41 | 0.13 | 0.37 |
| OHS-3 choice ≥ Jev (no MC drop) | 0.71 | 0.16 | 0.65 |
| Brier "matches" (secondary for the owner) | 0.28 | 0.08 | 0.25 |
| Consistency: complement ≤ Jev AND option-order drift ≤ Jev | 0.45 | 0.17 | 0.28 |
| Hijack (jagged ASR) beats Jev | 0.97 | 0.97 | 0.97 |
| Injection (OPI ASR point ≤ Jev; a *significant* beat is only about 0.1) | 0.70 | 0.45 | 0.50 |
| Speed (median end-to-end < Jev, same client; includes hosting risk) | 0.82 | 0.73 | 0.69 |
| Cost (JevBench formula) | 0.97 | 0.97 | 0.75 |
| JevBench Score A, public items, our run | 0.93 | 0.80 | 0.88 |
| **Owner's success** (accuracy "matches" AND hijack, injection, speed, cost, JevBench) | **0.30** (0.27-0.38 by tie definition) | 0.03 | 0.12 |
| **All win conditions at once** (calibration excluded) | **0.08** (0.06 with Brier) | <0.01 | 0.02 |

**Probabilities are model outputs, not facts.** They carry the uncertainty of the EST inputs.
- Across plausible settings of the single most important input (how many OHS-3 yes/no tasks behave like hearsay, moral or table tasks), P(final 4B ≥ Jev) moves from **0.35 to 0.75** (§12).
- The audit gave 30-45% for accuracy and 5-10% for everything (`wnzbuj8i0.output` verdict).
- The status PDF gave about 50% and 15-25% (`OpenDecide_Status_30Sep.pdf` p.5-6).
- This model lands between them, with explicit arithmetic.

---

## 1. Method (the chain)

```
OHS-3 gap (per type) = [1] v11c-class baseline on an OHS-3-like task mix
                     + [2] v11c -> 4B-E held-out gain  (dev gain x transfer ratio rho)
                     + [3] 4B-E -> new 4B held-out gain (scenario g x rho, only if the ship rule passes)
micro = 0.3866 x yes/no + 0.6134 x choice          (716 / 1,852 and 1,136 / 1,852; ohs3_summary.json)
2B    = 4B-E-level - [4] distillation gap + kappa x new-4B data gain + new hard rows
Cascade = final 4B - [5] routing loss
Brier = f(yes/no gap) - dev temperature gain      [7]
```

**Significance thresholds.** "Matches" and "not significantly worse" use 95% half-widths scaled by √n from OHS-1 and OHS-2:
- micro ±1.6 (OHS-1 ±1.63, OHS-2 ±1.71; `results_ohs*/results_all.json`);
- yes/no ±2.8;
- choice ±1.85;
- Brier ±0.013.

So "matches" (LB > −2.0) means a point gap of more than −0.4.

---

## 2. Step 1: the baseline, a v11c-class 4B on OHS-3

v11c is our only 4B measured on both held-out exams. Its **30 per-task gaps** (ours − Jev, from `projection/recompute/ohs1_out.txt` and `ohs2_out.txt`) sort into four pools.

| Pool | Tasks (gap, pp) | Mean |
|---|---|---|
| Yes/no, classification-like | argq −0.83, cuad −0.62, hatecheck −3.10, overruling +5.00, this_is_not_a_dataset +3.06 | **+0.70** |
| Yes/no, rule application or reasoning | moral_stories −12.50, tabfact −8.33, legalbench_hearsay −29.27 | **−16.70** |
| Choice, topical / label-set | 8 arXiv tasks (−5.83 … +7.50), big_patent −1.67, medical_abstracts +3.33, ledgar +1.67, unfair_tos +1.88, go_emotions −4.33, sgd −1.50, ddi2013 +12.50 | **+0.79** |
| Choice, reasoning | vitaminc −7.75, scone −8.06, abercrombie −8.33, pubmedqa −1.67, scifact −7.08, pubmed_rct −4.17, evidence_inference 0.00 | **−5.29** |

**Pattern.** We tie Jev on classification-like tasks of both types and lose 5-17 pp on reasoning and rule application. This agrees with the track split in evidence §15: on fresh-text track F, OHS-1 −0.42 and OHS-2 +0.42.

**Mapping to OHS-3** (`PREREG_OHS3.md:10-24`):
- All 8 choice tasks are label-set classification: site, agency, department, category, relation, entity type, profession and language. EST P(reasoning-like) = 0.10 each.
- Of the 5 yes/no tasks:
  - ct_study_type, zenodo_resource_type and causal_news_corpus are label checks.
  - openfda_recall_class applies a severity rule (21 CFR 7.3(m)(1)), much as hearsay applies a legal rule.
  - nvd_attack_vector sits in between.
  - EST P(rule-like) = 0.30 each.
- Each simulated task draws a gap from its pool, plus a novelty jitter of N(0, 3.0) for yes/no and N(0, 2.5) for choice, plus an exam-level shift of N(0, 1.0).

**Arithmetic (means):**
- yes/no = 0.7 × 0.70 + 0.3 × (−16.70) = **−4.52**
- choice = 0.9 × 0.79 + 0.1 × (−5.29) = **+0.18**
- micro = 0.3866 × (−4.52) + 0.6134 × 0.18 = **−1.64**

**Monte Carlo medians:** micro −1.54 (80% [−4.72, +1.32]), yes/no −4.03 ([−10.8, +1.1]), choice +0.13.

**Cross-check.** The evidence file's three reweightings gave −0.9 to −3.7 for a v11c-class model (evidence §15).

---

## 3. Step 2: v11c → 4B-E, then transfer to held-out

**Dev gains, v11c → 4B-E** (`recompute/dev_out.txt`):

| | yes/no | choice |
|---|---|---|
| dev-select | +1.52 | +0.41 |
| pooled | +2.26 | +0.63 |

Overall: select +1.00, pooled +1.50, unseen-source set +1.90. dev-select is the half 4B-E was *not* chosen on.

**Transfer ratio ρ = held-out gain ÷ dev gain**, from our history (evidence §12):

| Step | OHS-1 | OHS-2 |
|---|---|---|
| v10 → v11c | 1.5 | **1.35** |
| v10 → v11b | 2.2 | – |
| v11b → v11c | 0.26 | – |
| frozen → v10 | about 0.03 | – |

Caveats on these ratios:
- OHS-1 ratios are inflated: OHS-1 results guided the v11 data (`budget_ledger.md:79`).
- The frozen → v10 step shows that dev can overstate held-out gains badly.

**EST:** ρ is lognormal with median 0.9 and sd(log) 0.6, so the 80% range is [0.42, 1.95]. The same distribution is used for [3].

**Arithmetic (median ρ):**
- yes/no: 0.9 × 1.89 = **+1.70**
- choice: 0.9 × 0.52 = **+0.47**
- So 4B-E on OHS-3 is: yes/no −2.82, choice +0.65, micro **−0.69**.
- The Monte Carlo median is micro −0.44 (80% [−3.72, +2.60]), with P(≥0) 0.43 and P(matches) 0.49.

**Ratio by question type.** Historically choice transferred better than yes/no: dev choice +0.65 became +1.7-1.8 held-out for v10 → v11c. A single ρ is conservative for choice.

---

## 4. Step 3: the new 4B (`q35_4b_main500k`) over 4B-E

**Run status:**
- Step 3,200 of 30,457 at 142.5 min, which is 2.67 s/step, so a full pass is about 22.6 H100-hours.
- 0 ALERT lines. Snapshot s002500 was written (`logs/main4b_seg1.log` lines 138 and 156).
- The loss curve cannot be compared with the dev gate.

**The weak yes/no 1.5-2x up-weighting was NOT applied.**
- The config trains exactly one pass (30,457 steps) of the plain `golden_train.jsonl` (`runs/q35_4b_main.json`).
- Owner decision 1 is recorded as "1.0x now" (`runs/README.md`).
- So the projection gives it **0 effect**.
- The priority families (moral 36,130 rows, tables 48,384, science claims 23,784) are in the set at full size (`GOLDEN_CARD.md`). That is already far more than 4B-E's lineage had.

**Evidence for the size of g, the true dev gain over 4B-E:**
- **Broad data, earlier rounds:** +0.57 to +0.64 on confirm (v13t, blend; `budget_ledger.md:109-110`).
- **Narrow data:** −0.69 (v12t; `:101`).
- **4B-E itself:** +1.36 confirm / +0.27 select (`:168`).
- **Step scaling.** 4B lineage: 1,782 steps (v11) 77.9 pooled → about 4,575 steps (4B-E: v11 1,782 + v11b 418 + v11c 375 + v13t 1,200 + E 800; `logs/train_q35_4b_v11*.log`, ledger rows G2 and X14) 80.7. 2B: +1.3 and +3.0 per doubling of steps at 800 → 1,600 (I, E_L4), and about +0.8 per doubling from 1.5K to 3.7K (v11 → v11r) (`dev_out.txt`).
- The new run has 30,457 steps on 501,732 rows. That is 6.7x 4B-E's lineage steps (2.7 doublings), and 2.7x the rows of all its lineage files combined (188,997, overlapping).
- **Against:**
  - It starts from base, so it loses the tb_mixtral lineage (4B-E 90.5 vs base 73.6 on tb_mixtral yes/no; `PREREG_FINAL.md` 3.3). That hurts raw dev-confirm, though not the ship rule's primary test.
  - `FINETUNE_PLAN.md:26-27` says "we cannot predict the gain".
- **EST scenario weights for g:**

| g | −0.5 | 0 | +0.5 | +1.5 | +2.5 |
|---|---|---|---|---|---|
| Probability | 0.15 | 0.15 | 0.25 | 0.30 | 0.15 |

Each scenario also gets a jitter of N(0, 0.3). The expected g is +0.88.

**Ship-rule filter** (`PREREG_FINAL.md` 3.2, 3.5):
- Rule: the primary difference must be ≥ +0.2 and its lower bound > −0.75.
- At 4B-vs-4B disagreement the half-width is about ±1.1 (sd about 0.6), so the rule needs an observed difference of about +0.35 or more.
- EST: the constraints pass with probability 0.9.
- Resulting P(ship) by scenario: g −0.5 → 0.08, 0 → 0.26, +0.5 → 0.52, +1.5 → 0.87, +2.5 → 0.90. Overall **0.58**.
- If it does not ship, 4B-E is the final 4B.

**How a shipped gain splits by type.** EST ×1.2 for yes/no and ×0.75 for choice: the set is 64.6% yes/no, and 4B-E's own gain leaned to yes/no.

Per unit of g at median ρ:
- yes/no gain = 0.9 × 1.2 × g = 1.08g
- choice gain = 0.9 × 0.75 × g = 0.675g
- micro gain = 0.3866 × 1.08g + 0.6134 × 0.675g = **0.83g**

**Scenario table: implied OHS-3 numbers for the final 4B** (hand arithmetic with mean baselines and median ρ | Monte Carlo median for the scenario)

| Dev gain over 4B-E | P(ship) | Micro gap | Yes/no gap | Choice gap | Brier diff (ours − Jev) | P(micro ≥ 0) | P(matches) |
|---|---|---|---|---|---|---|---|
| Fail / ≤ 0 (4B-E kept) | – | −0.69 \| −0.44 | −2.82 \| −2.04 | +0.65 \| +0.70 | +0.022 | 0.43 | 0.49 |
| Low +0.5 | 0.52 | −0.27 \| −0.18 | −2.28 \| −1.71 | +0.99 \| +0.90 | +0.019 | 0.47 | 0.53 |
| **Central +1.5** | 0.87 | **+0.56 \| +0.81** | **−1.20 \| −0.42** | +1.66 \| +1.74 | +0.013 | 0.62 | 0.68 |
| High +2.5 | 0.90 | +1.39 \| +1.67 | −0.12 \| +0.70 | +2.34 \| +2.42 | +0.008 | 0.72 | 0.76 |
| **Mixture (all scenarios)** | 0.58 | **+0.28** (80% [−3.2, +3.8]) | −1.09 ([−8.2, +4.7]) | +1.29 ([−1.7, +4.6]) | +0.012 | **0.54** | **0.60** |

- The low / central / high rows show the scenario given that the model ships. The Monte Carlo medians include no-ship draws.
- **Absolute illustration only:** if Jev scores its OHS-1/2 level of 81.6 overall (`results_ohs*/results_all.json`), the final 4B's median is about **81.9**, with an 80% range of 78.4-85.4. Jev's OHS-3 yes/no level cannot be anchored: it was 84.0 on OHS-1 and 95.8 on OHS-2.

---

## 5. The 2B (PRISM-X I, teacher 4B-E)

**2B − 4B gaps we have measured:**

| Pair | Gap | Source |
|---|---|---|
| Matched distillation v11c → v11r (59.7K rows, about 3.7K steps), dev pooled | −3.23 (yes/no −2.80, choice −3.72) | `dev_out.txt` |
| Same pair, unseen-source set | −3.58 | evidence §13 |
| Same pair, JevBench half A | −5.1 | evidence §13 |
| Same pair, eval_card wide | −3.3 | evidence §13 |
| I_1600 vs 4B-E (not matched, 1,600 steps) | −5.49 (yes/no −5.77, choice −5.16) | `dev_out.txt` |
| 2B kd pilot vs v10, OHS-1 | −9.75 (early, weak recipe) | evidence §13 |

- **Step scaling:** the final 2B gets 19x I_1600's steps, about 4.3 doublings. At +0.5 to +1.0 per doubling that is +2 to +4 over I_1600's 75.17 pooled, so **about 77-79 dev pooled (EST)**.
- **EST held-out gap to its teacher 4B-E:** yes/no N(4.0, 1.5), choice N(3.8, 1.3), correlated.
- **Gain from the shared data:** the 2B also trains on the same gold rows, so it inherits a share κ ~ U(0.3, 0.8) of the new 4B's data gain.
- **New program-labelled hard yes/no, tool-call and state-tracking rows:** EST +0 to +0.5 on OHS-3 yes/no.
  - They are about 1% of the data (audit, `wnzbuj8i0.output`).
  - The yes/no research verifier expects them to recover 1-3 of the 7.5-point OHS-2 moral/table gap and **about 0 on OHS-3**, which has no moral or table tasks (`wfjjlksu2.output`).
  - The tool-call and state-tracking families are JevBench v1.5 items that are not public, so our public-item run cannot show them either (`bench/v154/README.md:19-20`).
  - **Treat their effect as small.**

**Arithmetic (central, new 4B at +1.5 shipped):**
- yes/no = −2.82 − 4.0 + 0.25 + 0.55 × 1.62 = −5.68
- choice = 0.65 − 3.8 + 0.55 × 1.01 = −2.59
- micro = **−3.78**
- Monte Carlo: micro **−3.81** (80% [−7.5, −0.2]), P(≥0) **0.09**, P(matches) 0.11. It ranges from 0.03 to 0.16 over 2B-gap assumptions (`sensitivity_out.txt`).

---

## 6. The cascade (2B answers first; its least-sure rows go to the final 4B)

**New simulation** (`model/cascade_ext_out.txt`): the threshold is fixed on dev-select and reported on dev-confirm, with a paired group_id bootstrap, 10k resamples.

**Cascade minus 4B alone, by routing budget:**

| 2B → 4B (2B − 4B gap) | 30% | 40% | 50% | 60% | 70% | 80% |
|---|---|---|---|---|---|---|
| I_1600 → 4B-E (−6.31) | −1.88 | **−1.01 [−1.76, −0.22]** | −0.69 | −0.49 | −0.25 | −0.05 |
| E_L4_1600 → 4B-E (−6.04) | −1.91 | −1.34 | −0.72 | −0.47 | −0.35 | −0.10 |
| v11r → 4B-E (−5.25) | −1.86 | −1.04 | −0.54 | −0.17 | −0.12 | −0.02 |
| v11r → v13t (−3.89) | −0.52 | **+0.02 [−0.76, +0.88]** | +0.22 | +0.15 | +0.17 | +0.15 |

- The learned router is no better than routing on the top probability: at 40%, 80.38 vs 80.48 (`router_sim.py` run).
- **Rule of thumb from these four pairs:**
  - with a 2B gap of about −4, the cascade equals the 4B from about 40% routing;
  - with a gap of −5 to −6, it needs 60-70% routing to get within 0.25-0.5 pp.
- **Projection:**
  - The final 2B gap is EST −3.5 to −4.5, so the plan's budget rule (FINETUNE_PLAN 5.3) picks about 40-55%.
  - EST held-out loss vs the 4B is U(0, 0.8).
  - Cascade: micro **−0.12** (P(≥0) 0.48, P(matches) 0.54).
- **Under attack** (same thresholds, I_1600 → 4B-E):
  - jagged ASR stays at 0.3-1.1% at every budget;
  - OPI ASR falls from 4.4% (2B alone) to 2.8% at 40%, 2.2% at 60% and 0.8% at 70%;
  - attacks do **not** inflate routing: routed share clean vs attacked is 20.0% vs 18.9% on OPI at the 40% budget.

**Latency and cost blend.**
- The 2B always runs, so time ≈ t2B + r × t4B.
- The only same-setup timing has the **PRISM-X 2B slower than the 4B**: 128.0 vs 110.1 ms p50 on the L4, eager (PRISM-X blocks CUDA graphs; `scores_v154_all.json`; `budget_ledger.md:180`).
- At r = 0.45:
  - L4: 128 + 0.45 × 110 = **177.5 ms, 1.6x the 4B alone**;
  - H100 (EST): 50 + 0.45 × 24 = **about 61 ms, 2.5x the 4B alone**.
- **The plan's own rule** is (inference cost ratio + routed fraction) < 0.85 (`FINETUNE_PLAN.md:448`). With the measured ratio of 1.16 it can never pass, so **the plan serves the 4B alone**, and the cascade is not the headline system (`:444`).
- The cascade would only pay off if the 2B got CUDA graphs. That does not work with PRISM-X today.

---

## 7. Speed

**Assumptions for "proper hosting":**
- a warm GPU, batch 1;
- no Modal web router: a direct tunnel or a co-located app;
- the same client for us and for Jev;
- CUDA graphs for the 4B (not possible for the PRISM-X 2B).

**Layout-E factor.** The 4B-E on H100 with graphs has **never been measured**. EST 15-35 ms (central 24): v10 on H100 with graphs was 13.2 ms, times a layout-E factor of about 1.84. That factor is 4B-E L4 eager 110 ms ÷ an earlier text-first 4B L4 eager 59.8 ms (`logs/final_latency.log`); the model in that log is not named. Layout-E prompts are 627 vs 265 characters.

| Median (p95) | 4B final | 2B-I | Cascade (r = 0.45) | Jev |
|---|---|---|---|---|
| GPU only, L4 eager (measured) | 110.1 (112.3) ms | 128.0 (130.8) ms | about 178 ms | – |
| GPU only, H100 (EST) | about 24 (15-35), with graphs | about 50 (35-70), eager | about 61 (p95 about 74) | – |
| End to end, laptop → direct tunnel (EST: network 71.9 / 77.1 ms CPU echo, `logs/latency_probe.log`; plus about 5 ms overhead) | **about 100 (90-120)**; measured analogue v10 114.6 (124.1) (`logs/tunnel_q35_4b_v10_tunnel_plain.json`) | about 125 (110-150) | about 140 (p95 about 160) | **187-248 (266-539)**, measured on the same laptop over 7 runs (evidence §9) |
| End to end, co-located app (EST, RTT 1-5 ms) | 30-45 | 45-80 | 55-90 | official claim 70-500 (`jev-market-facts.md:11`) |
| End to end via the Modal web endpoint | about 400 (v10 measured 410 / 517; `logs/bench_api.json`), **loses** | loses | loses | |

**JevBench speed axis** (`v154lib.py`: points = 100 − 20·log10(s/0.1); self-hosted s = 2t + 0.15):
- Jev: 238 ms / 303 ms → **91.4**.
- We beat that if p50 ≈ p95 < **59 ms** on the GPU.
- 4B at 24 ms → 0.198 s → about 94 (win).
- 2B at 50 ms → about 92 (marginal win).
- Cascade at 61 / 74 ms → about 90.9 (marginal loss).
- Today's measured L4-eager runs are 88.6 / 87.8 (loss; `RESULTS_30sep.md:13-16`).

**EST probabilities.**
- P(proper hosting measured before OHS-3) = 0.85. This is the team's own choice, and speed and cost are not yet defined for OHS-3 (audit must-fix 9).
- P(win | proper hosting): 0.95 for the 4B, 0.85 for the 2B, 0.80 for the cascade.
- P(win | not): about 0.05.
- Totals: **0.82 / 0.73 / 0.69**.

**Main uncertainty:** the layout-E latency with graphs, and the metric definition.

---

## 8. Cost per 1,000 decisions

**(a) JevBench formula: tokens × reference list price** (`bench/v154/README.md:38`)
- Ours: 817.8 input tokens × $0.03/M = **$0.0245 per 1K**. The 4B and the 2B were both priced at the Qwen3.5-4B reference in our run.
- Jev: 914.8 × $0.042/M = **$0.0384 per 1K**; output is free.
- Cost points (100 − 30·log10(per-decision $ / 0.001)): **58.3 vs 52.5**, a structural win for the 4B and the 2B.
- The cascade pays for tokens twice on routed rows: $0.0245 × (1 + r). At r = 0.45 that is $0.0355 → 53.5 (a narrow win). Break-even is at r = 0.0384/0.0245 − 1 = **0.567**.
- P: 0.97 / 0.97 / 0.75.

**(b) Real self-hosted serving at batch 1** ($/h ÷ 3600 × GPU seconds × 1000 ÷ utilization; rates from `budget_ledger.md:7`)

| | At 100% utilization | At 50% utilization | Break-even utilization vs Jev ($0.032-0.038) |
|---|---|---|---|
| 4B, H100 + graphs, 24 ms (EST) | $0.026 | $0.053 | 69-82% |
| 4B, L4 eager, 110 ms (measured) | $0.024 | $0.049 | 64-76% |
| 4B, L4 + graphs, about 50 ms (EST, not measured) | $0.011 | $0.022 | 29-35% |
| 2B-I, H100 eager, 50 ms (EST) | $0.055 | $0.110 | never, at batch 1 |
| Cascade, L4 eager, 178 ms | $0.039 | $0.079 | never |

- Jev billed **$0.032 per 1K calls** (`budget_ledger.md:64`).
- Our real serving cost has never been measured.
- The serving path is batch 1 (GraphRunner). Batching would cut cost several-fold, but it is not built or tested; with PRISM-X it is untested too.
- **EST P(real-cost win):** 0.50 for the 4B, 0.30 for the 2B, 0.20 for the cascade.

---

## 9. Calibration (Brier on the 716 yes/no rows)

**The Brier gap is almost all accuracy.**
- OHS-2 decomposition: Jev REL 0.0071 vs ours 0.0041 (ours is better); the whole gap is resolution (`budget_ledger.md:153`).
- The dev-fitted temperature for 4B-E is T = 0.9 / 1.0 with a gain of 0.0006, so it ships at T = 1 (`FINETUNE_PLAN.md:427`). The cross-fitted gain is 0.0003 (`dev_out.txt`: 0.1143 → 0.1140).
- For the 2B, T = 0.7 / 0.95 gains 0.0022 (`:428`).
- **Temperature therefore moves Brier by ≤ 0.002 and cannot close a gap.**

**Mapping from the yes/no gap to Brier.**
- A fit over the 5 measured (yes/no gap, Brier diff) pairs gives diff = +0.0136 − 0.0043 × gap (residual sd 0.0059).
- Its intercept (the Brier gap at *equal* accuracy) is extrapolated, with a standard error of about 0.011.
- Cross-set evidence says equal accuracy gives about equal Brier: Jev OHS-1 83.97% → 0.1142; 4B-E dev 84.45% → 0.1143.
- EST: intercept N(0.007, 0.007); slope N(−0.0053, 0.001). The dev 4B family slope is about −0.0065.

**Arithmetic.**
- 4B central: yes/no −1.20 → Brier diff = 0.007 + 0.0053 × 1.20 = **+0.013**.
- "Matches" (Jev − ours LB > −0.010) needs a point diff below −0.003. That means our yes/no must be about **+1.9 pp better than Jev**.

| | Brier diff (ours − Jev), median [80%] | P(point ≤ Jev) | P(PREREG "matches") | P(not significantly worse) |
|---|---|---|---|---|
| Final 4B | +0.012 [−0.021, +0.052] | 0.32 | **0.28** | 0.51 |
| Final 2B | +0.033 [−0.001, +0.074] | 0.10 | 0.08 | 0.23 |
| Cascade | +0.014 | 0.29 | 0.25 | 0.48 |

Jev's measured values: 0.1142 (OHS-1), 0.0379 (OHS-2). We win Brier on JevBench Noul (0.070 vs 0.105) and on jagged clean items (0.032 vs 0.096), but those are not OHS-3.

---

## 10. Consistency and security

### Complement violation (300 `_neg` pairs)

**Inputs:**
- dev rates: 4B-E 4.81%, v11r 8.11%, I_1600 10.78% (evidence §5);
- dev → OHS-1 ratio 1.25-1.9;
- Jev on OHS-1: about 10.8%.

**4B arithmetic:** 4.81 × 1.575 = 7.6% vs 10.8% → **−3.2 pp**.

**Modelled uncertainty (EST):**
- OHS-3's negation frames (T1-T6 and clause negation) are new to both systems: a common factor plus a system factor, each lognormal with sd(log) 0.3-0.35.
- Violations rise as yes/no accuracy falls.
- Sampling sd of the difference on 300 pairs: 2.2 pp.

**Results, P(ours ≤ Jev):**
- final 4B −3.5 pp [−11.6, +3.5] → **0.75**;
- 2B +3.1 [−5.9, +15.4] → 0.33;
- cascade → 0.49.

### Option-order drift (304 `_perm` pairs)

- **Never measured for anyone** (evidence §5).
- EST prior: ours is trained with a random option order every step plus the perm-twin loss, so the prior leans slightly to us.
- P(ours ≤ Jev): 0.60 for the 4B, 0.50 for the 2B, 0.57 for the cascade.

**Both endpoints ≤ Jev:** 0.45 / 0.17 / 0.28.

### Hijack (jagged ASR)

- Jev 99.4% vs 4B-E 0.6% and 2B-I 1.1% (evidence §6).
- The ship rule caps the final 4B at 3% and the 2B at 6.9% (`PREREG_FINAL.md` 3.3 (g)).
- In the cascade simulation it stays at 0.3-1.1% at every budget.
- **P = 0.97 for all three.**
- Scope: one attack direction, and the set was used for selection. The adaptive attack of FINETUNE_PLAN 5.4 has not been run. Under a matched adaptive attack the EST is 0.7-0.9.

### Injection (OPI ASR)

- Jev 1.3%.
- 4B-E: 1.0%, diff −0.4 [−1.1, +0.1], a tie. The other 4Bs: 0.6-1.5%.
  - P(point ≤ Jev) **0.70**.
  - P(significant beat) about 0.1.
- 2B: PRISM-X I-family runs were 0.8, 0.4, 0.8 and **4.4%** (I_1600, the longest run). P = 0.45.
- Cascade: simulated 2.8% at 40%, 2.2% at 60%, 0.8% at 70% with the current 2B. P = 0.50.
- Main uncertainty: run-to-run swing (`budget_ledger.md:146`).

### Definition overwrite (redef)

Jev has never been run on it, so no claim is possible. 4B-E is at 16.5%, the 2B at 3.3%.

---

## 11. JevBench (public 231 items, our run, official v1.5 formulas; not a leaderboard position)

**Score A is the harmonic mean of the four axes** (`v154lib.py`).

**Final 4B:**
- Measured for 4B-E with committed yes/no: I 78.7, C 83.4, S 88.6, $ 58.3 → **75.27** (`RESULTS_30sep.md:14`).
- With H100 speed of about 94 → 4 / (1/78.7 + 1/83.4 + 1/94 + 1/58.3) = **76.2 (EST)**.
- Jev: **68.80** as returned; **70.66** if Jev is also committed (evidence §11).
- Break-even: with the other axes fixed, the 4B loses Score A only if its Intelligence falls below **61.8** (vs committed Jev) or **56.5** (vs Jev as returned). It measured 78.7.
- P = 0.93. The residual risk is a re-run of the *new* 4B, and which Jev readout is used.

**Final 2B:**
- The pilot measured 71.96 (I 70.3, C 78.1, S 87.8, $ 58.3).
- Break-even Intelligence: 65.5 vs committed Jev, 59.5 vs Jev as returned.
- The final 2B has 19x the steps. P = 0.80.

**Cascade:**
- EST I about 78, C about 83, S 90.9 (H100) or 85.9 (L4), $ 53.5 → **72.5-73.3**.
- P = 0.88. The risk is the cost axis if r > 0.57.

**Intelligence alone, both sides committed** (the fairest comparison):
- 4B +5.1 [−4.4, +15.0] → P(point > 0) about 0.85;
- 2B pilot −3.3 [−15.0, +9.2] → about 0.3, rising to about 0.45 for the final 2B.

**Board context only.** On the official board, 4B fine-tunes lose 10-11 Intelligence points between public and sealed items; Jev loses none. Jev is at 72.13. There is no submission until the owner says (memory `no-jevbench-submission`), so the board is not projected.

---

## 12. Sensitivity (`model/sensitivity_out.txt`)

| One change from the base | Final 4B micro median | P(4B ≥ Jev) | P(4B matches) | P(4B yes/no ≥ Jev) | P(2B ≥ Jev) |
|---|---|---|---|---|---|
| **Base** | +0.27 | 0.54 | 0.60 | 0.41 | 0.09 |
| P(rule-like yes/no task) 0.10 | +1.56 | 0.75 | 0.80 | 0.73 | 0.16 |
| P(rule-like yes/no task) 0.50 | −1.09 | 0.35 | 0.40 | 0.19 | 0.04 |
| Drop hearsay from the rule pool | +0.89 | 0.65 | 0.72 | 0.54 | 0.11 |
| OHS-2 tasks only (freshest exam) | +1.39 | 0.74 | 0.79 | 0.41 | 0.14 |
| Transfer ratio median 0.5 / 1.4 | −0.50 / +1.17 | 0.42 / 0.66 | 0.48 / 0.71 | 0.30 / 0.53 | 0.04 / 0.16 |
| New 4B pessimistic (P(g ≤ 0) = 0.55) / optimistic | −0.07 / +0.58 | 0.49 / 0.59 | 0.55 / 0.64 | 0.37 / 0.44 | 0.07 / 0.10 |
| Task spread doubled | +0.26 | 0.53 | 0.58 | 0.42 | 0.14 |

**What drives the result:**
- **The biggest driver is not our training run.** It is whether OHS-3's yes/no tasks (above all openfda_recall_class and nvd_attack_vector) behave like the rule-application tasks where Jev beat us by 8-29 pp.
- **The second driver is the dev → held-out transfer ratio.**
- **The new 4B's gain moves P(4B ≥ Jev) by only ±0.05.** The ship rule protects the downside, and the baseline noise swamps the upside.

---

## 13. Master table: metric × system

"P" is the probability that we beat or tie Jev, as defined in §0.

| Metric | Jev's value (source) | Final 4B: projection (central, 80%) / P | Final 2B | Cascade | Main uncertainty |
|---|---|---|---|---|---|
| OHS-3 micro accuracy (gap) | OHS-1 81.65, OHS-2 81.55 | **+0.3 [−3.2, +3.8]** / 0.54 (matches 0.60) | −3.8 [−7.5, −0.2] / 0.09 | −0.1 [−3.6, +3.4] / 0.48 | OHS-3 task mix vs our past losses; transfer ratio |
| OHS-3 yes/no (gap) | OHS-1 83.97, OHS-2 95.83 | −1.1 [−8.2, +4.7] / 0.41 | −5.3 [−12.5, +0.6] / 0.13 | −1.6 / 0.37 | whether openfda/nvd behave like hearsay |
| OHS-3 choice (gap) | OHS-1 80.72, OHS-2 76.20 | +1.3 [−1.7, +4.6] / 0.71 | −2.8 [−6.1, +0.8] / 0.16 | +1.0 / 0.65 | 40-option tasks (OHS-1 >26-option rows: −2.6) |
| Brier, yes/no (diff) | 0.1142 / 0.0379 | +0.012 [−0.021, +0.052] / matches 0.28 | +0.033 / 0.08 | +0.014 / 0.25 | the intercept at equal accuracy |
| Complement violation (diff) | about 10.8% (OHS-1) | −3.5 pp / 0.75 | +3.1 pp / 0.33 | +0.1 pp / 0.49 | new negation frames |
| Option-order drift | never measured | prior 0.60 | 0.50 | 0.57 | no data at all |
| Hijack ASR (jagged) | 99.4% | 0.6-3% / 0.97 | 1.1% (cap 6.9%) / 0.97 | 0.3-1.1% / 0.97 | adaptive attack not run; set used for selection |
| Injection ASR (OPI) | 1.3% | about 1.0% / 0.70 | about 1-4% / 0.45 | 1-3% / 0.50 | run-to-run swing |
| Speed, median end to end | 187-248 ms (laptop) | about 100 ms (tunnel) / 0.82 | about 125 / 0.73 | about 140 / 0.69 | hosting; layout-E latency with graphs; no definition yet |
| Cost, JevBench formula | $0.0384 per 1K (52.5 points) | $0.0245 (58.3) / 0.97 | $0.0245 / 0.97 | $0.0355 at r = 0.45 / 0.75 | cascade routed share |
| Cost, real serving | $0.032 per 1K calls billed | $0.011-0.053 by GPU and utilization / 0.50 | $0.055+ / 0.30 | $0.039+ / 0.20 | utilization; no batching |
| JevBench Score A (public) | 68.80 as returned / 70.66 committed | 75.3-76.2 / 0.93 | about 72-74 / 0.80 | 72.5-73.3 / 0.88 | new-model re-run; which Jev readout |

---

## 14. Joint probabilities (`model/project_out.txt`)

**Method.**
- The accuracy, yes/no, choice, Brier and consistency parts are simulated jointly, so they are correlated through the shared model quality.
- Hijack, injection, speed, cost and JevBench are EST Bernoulli draws.
- Speed and cost share the hosting draw.

**Owner's success** = accuracy tie-or-better AND hijack AND injection AND speed AND cost AND JevBench.
- **Final 4B:**
  - accuracy "matches": **0.30**;
  - accuracy point ≥ 0: 0.27;
  - accuracy not significantly worse: 0.38;
  - with real-serving cost instead of the JevBench formula: 0.15.
  - Arithmetic check for "matches": 0.60 × 0.97 × 0.70 × 0.82 × 0.97 × 0.93 = 0.30.
- **Other readings of "injection":**
  - If "hijack/injection" counts as one security condition met by hijack: 0.30 / 0.70 = **0.43**.
  - If injection needs a *significant* beat: 0.30 × 0.10 / 0.70 = **0.04**.
- **Final 2B:** 0.03. **Cascade:** 0.12.

**All win conditions at once** = accuracy "matches", yes/no ≥ Jev, choice ≥ Jev, both consistency endpoints ≤ Jev, hijack, injection, speed, JevBench-formula cost and JevBench.
- **4B: 0.08. With Brier "matches" as well: 0.06.**
- 2B: under 0.01. Cascade: 0.02.

**Which system counts?** A mix-and-match claim (for example 4B accuracy + 2B speed) is not a fair single-system claim. The plan's headline is the 4B alone (`FINETUNE_PLAN.md:444`). Write this down before OHS-3 (audit must-fix 9).

---

## 15. Things that would move these numbers most, cheaply (no OHS-3 access needed)

1. **Pre-register the speed and cost definitions, and measure the 4B's layout-E latency on H100 with CUDA graphs through a direct tunnel.** This converts about 0.15 of speed and cost risk into a measured fact.
2. **Measure the option-order drift `_perm` read on dev for the final models** (about 1 L4-hour each; ship rule (f)). Also get Jev's drift on the same dev pairs if the budget allows. This is the only endpoint with zero data.
3. **Fix `score_ohs.py` to match PREREG_OHS3** (the complement definition, the Brier sign, CIs and BH correction; evidence §17 item 10), and collect Jev's OHS-3 answers early. Neither changes the odds, but both are required for a valid result.
4. **Do not expect the cascade to help** unless the 2B gets CUDA graphs. Today it is dominated by the 4B on accuracy, speed and cost.

## 16. Caveats

- **The task-pool model assumes OHS-3 tasks behave like our 30 past tasks.** OHS-3 is 59% fresh text (track F), where we tied Jev on both earlier exams (choice only). It is also the first exam with yes/no rows on fresh text (519 rows), so there is no direct evidence for that cell.
- **Scenario weights for the new 4B, ρ, P(rule-like), the 2B gap, hosting and all security and cost probabilities are judgements (EST).** Their ranges are in the scripts, and §12 shows what they do.
- **The "tie" definition changes the headline:**
  - 0.54 (point ≥ 0);
  - 0.60 (PREREG "matches");
  - 0.76 (not significantly worse).
- **JevBench numbers are public items only,** which have been our development set (half B seen 4 times). They would not predict the sealed board.
