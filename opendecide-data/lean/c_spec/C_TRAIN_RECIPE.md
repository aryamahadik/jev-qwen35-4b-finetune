# C_TRAIN_RECIPE: how model C is trained, gated and judged (v4)

Date: 3 Oct 2026. Status: recipe only, version 4. Nothing here has run. Version 4 applies the training, readout and gate
rows of `ADDENDUM_research.md` (ADOPT rows, plus its section I orchestrator decisions) and records its CONSIDER and
REJECT rows as such. Version 3 fixed the training and gate items of
`REVIEW_methods.md` and `REVIEW_rules.md` and applied the owner's 3 Oct decisions (memory `final-goal-30sep.md`, 05:40 to
08:20 UTC). Every paid step needs the owner's GO, and the whole plan needs a PREREG_FINAL amendment committed before
any C training row or candidate exists (A10 D: "no further 4B top-up ... without a new amendment").
Companion files: `C_DATA_SPEC.md`, `LICENCE_REGISTER.md`. Code facts were read from `train_decoder.py`, `gate_dev.py`,
`runs/q35_4b_main.json` and `PREREG_FINAL.md` 3.1-3.5. Gate numbers come from two CPU scripts in `sim/`:
`nearnull_calib.py` (measured: dev standard errors and the near-null check, from existing dev preds) and
`gate_sim_c.py` (a Monte Carlo on stated assumptions, not a measurement; v2 kept as `gate_sim_c_v2.py`).

---

## CHANGES (v4)

Source: `ADDENDUM_research.md` (rows below by its IDs; evidence in `RESEARCH_EXTRA_1..6.md`). This recipe does not
edit `C_DATA_SPEC.md`; data rows (A1, A2, B1-B3, C5, E2, F3, F4) belong to the spec owner. ejs-5 figures in the addendum are
aggregate-score context (some gold-scored vs Jev). v3's commit shares had been set from the ejs-5 per-task C1-vs-Jev
gaps in the ejs-5 run scores file (methods S3; a 7.4 path), not from the addendum; v4 replaces them with equal shares
(20% per type, `C_DATA_SPEC.md` 4.2). ejs-5 and OHS-3 choose no setting here.

| # | Addendum row | Change | Where |
|---|---|---|---|
| 1 | A3 (ADOPT) | Score rows are read at **T = 1, always**. Readout code asserts it. Justification: T = 1 is the shipped A5 readout (`prep89/READOUT_DEV.md`), not ejs-5 | 6.0 |
| 2 | A4 (ADOPT, with fallback) | One new loss term on ordinal rows only: `lam_ord` x ((E - y) x 4/(K - 1))^2, `lam_ord` 1.0, on the existing 20% ramp; no variance term. CPU unit test on fixed logits and a finite term in the memory pre-flight are required; if either fails, the term is dropped (`lam_ord` 0) before launch. Ordinal Brier / nRPS on dev is a report-only guard | 0, 3, pre-flight 10-11, 6.4 |
| 3 | A5 (ADOPT, rule) | No T < 1 lever for any type. Keep the shipped 2-view Score readout (given + reversed order, probability mean) | 6.0, 9 |
| 4 | C1 (ADOPT) | Item-13 temperature refined: one T per type for **choice and yes/no only**, fitted leave-one-group-out on the mix-tuning dev's held-out groups (sampler, pack, format, repo, plus F14), chosen by **median-group NLL**, bounded to **[0.8, 1.3]** | 6.0, 6.4, 9 |
| 5 | C2 (ADOPT) | Fixed order: aggregate views, then fit T on the aggregated output of the exact served pipeline, then band edge (JevBench only). D4 Brier uses the view-aggregated output of that pipeline (never a 1-view read) with T exactly as PREREG 3.3 (d) (per type, one dev half fitted and applied to the other, `calibrate.py` grid 0.25-10.0); the leave-one-group-out serving T is reported but never used for D4 | 6.0, 6.4 |
| 6 | C3 (ADOPT) | Report-only Brier and over/underconfidence gap on the **unseen-group** mix-tuning dev | 6.4 |
| 7 | C4 (ADOPT, rule) | Yes/no stays a single read. If yes/no views are ever added: average logits, then refit everything | 6.0 |
| 8 | C6 (ADOPT) | OHS-1 yes/no Brier reconciled on CPU from existing OHS-1 files only (never OHS-3): 0.140 vs 0.114 is the registered `score_ohs.py` endpoint (527 yes/no base rows; Jev = mean of its 2 runs); 0.152 vs 0.133 is all 2,972 yes/no rows including the variant layer. Both are right; the recipe now names the row set | 9 (row 13), 10.3 |
| 9 | D1 (ADOPT, no change) | No LESS, influence, IFD or targeted selection in round 1 or 2; stratified selection and representative replay stay | 3, 9 |
| 10 | E1 (ADOPT step 0; CONSIDER later reads) | FAM-1 monitor, report-only, on the L4: step-0 read (C1) before launch; the 25/50/75% reads run only if the measured step-0 read took <= 50 min | 5 |
| 11 | E3 (ADOPT, rule) | C1's loss weights kept in round 1; no PCGrad, GradNorm or LoRAMoE. At most one change before round 2: halving one flagged term's weight, by amendment | 3, 7.3 |
| 12 | F1 (ADOPT, no change) | `targets` QWEN35 (all 32,464,896 LoRA params), init from C1's adapter | 0, 1 |
| 13 | F2 (ADOPT) | Pre-flight: sha256 of the **rendered** prompt identical in training, dev gate and serving for 3 fixed rows; the `decoder_io.prompt` fallback raises for Qwen3.5; external servers pass `enable_thinking: false` | pre-flight 9 |
| 14 | F5 (REJECT) | No blends, snapshot averages or seed soups as a candidate | 6.2, 9 |
| 15 | A6, D2, E4 (CONSIDER); A7, C7, D3 (REJECT) | Recorded in section 9 as MAYBE (with their conditions) or NO. B6 is not run, so B7 never fires (addendum I) | 9 |
| 16 | Verifier pass (3 Oct, owner rules) | Commit shares equal (20% per type; A4 rows about 4,350); D4 T pinned to PREREG 3.3 (d) cross-fit; ejs-5 late rows and Gate report-only; B3 printed by the sealed scorer from its first version; D2 decided once in the amendment. Fix pass 2: sealed reads and B3 use the 6.0 served pipeline (serving T, Score T = 1; 6.1); the scorer is frozen with the suite, both sha256 in A15 (6.2, 11 step 2) | 3, 6.0, 6.1, 6.2, 6.4, 9, 11 |

---

## CHANGES (v3)

| # | Review item / owner decision | Fix | Where |
|---|---|---|---|
| 1 | Owner (1): step B adopted nothing (a = 0.9: +0.05 [-0.30, +0.40] unseen; failed confirm) | REF = C1 only. Every "or a*" path is removed. The stored REF for the refparity look is C1's `od_gcp` read `q35_4b_main500k` (the od-l4b re-read `_b100` matched it 100%, max abs dp 0) | 0, 1, 6.1 |
| 2 | Methods B2; owner (4): round-2 rule weaker than the owner's | The round-2 rule is the owner's rule, on **one** pre-registered candidate: sealed select set >= +2.0 pp **and** 95% LB > 0, **and** the no-harm guards D1-D6 pass (dev, security, calibration, option order). Its power curve and P(round 2 runs) (about 13%, range 8-22%) are stated | 6.3, 10 |
| 3 | Owner: one pre-registered candidate per round | The candidate of a round is its final-step adapter, as served. K4 (75% snapshot) is dropped. Snapshots are monitors only and are never read on the sealed suite. A run stopped by the stop rule yields no candidate | 2, 5, 6.2 |
| 4 | Methods B3: number of looks | Sealed looks are counted and logged by the scorer: at most one select-set read per round's candidate; exactly one confirm-set read (the finalist), refused a second time; parts B and P are read only at the confirm look | 6.2 |
| 5 | Methods B3: gate rarely ships a better model; sealed suite too small | Sealed part A >= **5,000** real-text items, split **40/60** by sha256 (select >= 2,000, SE about 0.85 pp; confirm >= 3,000, SE about 0.69 pp at 10% disagreement). The realized SE is measured at the round-1 select read and reported before the confirm look. This supersedes `C_DATA_SPEC.md` 9's 3,200-4,000 items and parity halves | 6.1 |
| 6 | Methods B3: ship rule | P1 = confirm set, CAND - REF >= +1.0 pp **and** 95% LB > 0 (C ships only when it is shown better). Ship-stage power: about 77% at a true +2.0 pp, 88% at +2.5, 92% at +3.0; P(ship) about 2% at a true 0. The v2 rule (>= +0.5, LB > -1) shipped a model with no true gain about 5% of the time under the prior; it is dropped | 6.4, 10.2 |
| 7 | Methods B3, S13: dev checks veto good models; thresholds untested | Dev guards re-set from **measured** SEs (C-like 4B pairs): D1 full set LB > -1.5 pp; PREREG (a2) dev-half rule report-only (C never selects on a dev half); D2 a clear-harm veto; (b)-(g) PREREG 3.3 unchanged. Together they pass a dev-neutral model about 85% of the time and block a uniform -1.0 pp dev drop about 86% (-1.5 pp: 99%). PREREG unchanged would pass a dev-neutral model only about 41% | 6.4, 10.2 |
| 8 | Methods B3: calibrate thresholds on the A11 near-null pair | Done on 3 Oct (`sim/nearnull_calib.py`, wise090 vs b100, 9 dev splits): no v3 dev rule fires. (f) and (g) could not be checked: the pair has no `_perm`, jagged or OPI reads | 6.1 |
| 9 | Methods B3: P2 vetoes good models by chance | P2 stays a clear-harm rule (a domain fails only if its whole 95% CI is below -2.0 pp); about 0% false veto for a model with no true domain loss | 6.4 |
| 10 | Methods B4; owner (6): sealed suite independence | Gate preconditions: frozen and sha256-hashed in an amendment **before any C training row is generated**; built by an agent with no access to C data; different source pool and templates; no per-item inspection; MultiDoc2Dial and NLU++ excluded; P1, P2 and the round-2 rule use part A real text only; adjacency labels fixed at freeze; part P report-only | 6.1 |
| 11 | Owner (5); methods B2, S2: anchor rule | KL to C1 (through KD targets) only where C1 is **confident and right** (top answer = gold, p_top >= 0.8) **or** on pre-registered **protected skills** (security and consistency units) where C1 is right. Never on C1's mistakes, never on new rows | 3 |
| 12 | Costs (task facts: $4.09/h, about 2.72 s/step, about 16.9 rows/step) | Round 1 about 8,880 steps, 6.7 h, about $27 (+$2 overhead); round 2 about 17,750 steps, 13.4 h, about $55 (+$2). Expected C spend about $37. Cap $100 of Modal for all of C; no launch may take the Modal balance below the $25 reserve | 2, 4 |
| 13 | Methods B3, N1: section 10 assumed C ships; untraceable "-0.6" start | Section 10 rewritten around P(ship), from the new simulation. Start gap from A12: C1 vs Jev OHS-1 -1.2 [-2.9, +0.4], OHS-2 -0.6 [-2.2, +1.1], about -1.0 pooled (practice sets now). `logs/b_wiseft_result.json` is now populated (2,662 bytes) | 10 |
| 14 | Methods S10, N6: token cap and batching | Pre-flight measures the long-row token share with the real tokenizer and trims to <= 30%; batching is the unit rule (<= 3 rows, <= 2 if long, plus permutation twins); v1's "3 variants per step" is withdrawn | 3 |
| 15 | Methods S1 | Replay rows from human-labelled sources with C1 p_g < 0.2 are dropped before training (`C_DATA_SPEC.md` 5); the mixer's count goes into the config | 3 |
| 16 | Rules S6, N4, N5, N6 | Jev outputs are never inputs to training, selection, thresholds or temperatures; the single sealed Jev read (`C_DATA_SPEC.md` decision 10: once, at the C look, after the ship verdict is logged) is report-only under `sealed_nd/`. ejs-5 is in-domain; JevBench and OHS-1/2 are practice sets; part A and part P are reported separately; temperature refit uses dev or mix-tuning dev only | 6.4 |
| 17 | Owner (7) | All teachers and anchors are 4B (C1; scoring crowd C1 + 4B-E + base 4B). OHS-3 and LongBench v2 stay sealed until after SHIP and an owner GO | 3, 6.4 |

Numbering: "Owner (n)" and "owner decision n" in this file number the owner's 3 Oct decisions as in the table above;
"`C_DATA_SPEC.md` decision n" means that file's section-12 defaults.

Kept from v2 (already fixed there): base anchor off; one pass; selective anchor disclosure (step-0 KD loss is not
zero); memory pre-flight; P(yes) drift stop at 0.02 with KL(REF || C) logged (methods S11); old slice held out by
`group_id` and normalized state (rules S7); served-artifact gating (methods N9); re-derived D2 set (rules S11);
bounded between-round weights with >= 400 items per family and p < 0.05 (methods S9); ejs-5 shrunk to +1 median, SE
1.75 (methods S4); r16 on empirical grounds only (methods N10).

---

## 0. Summary

| Item | Choice |
|---|---|
| Start | REF = C1 (`q35_4b_main500k`, adapter sha256 507d1c29...). Step B adopted nothing |
| How | Continue C1's LoRA adapter with the existing `init_adapter` path (no new init code; the only new trainer code is the A4 ordinal term) |
| LoRA | r 16, alpha 32, dropout 0.05, all `QWEN35` targets; 32,464,896 trainable params (`expect_trainable`); no attention-only variant (addendum F1) |
| Optimizer | AdamW, weight decay 0, clip 1.0, batch 16, `micro_tokens` 8192, fp32 trainable params |
| Schedule | peak LR **5e-5** (C1: 7e-5), 5% linear warm-up, cosine to 0, exactly one pass |
| Losses | C1's losses and weights unchanged (CE + label smoothing, KD 0.5, complement / equiv / inv / perm terms); **one new term: the ordinal mean term `lam_ord` 1.0 on ordinal rows only** (addendum A4; dropped before launch if its unit test or pre-flight fails); base-model anchor **off** (beta 0); C1 anchor through KD targets only where C1 is right **and** confident (p_top >= 0.8), or right on a protected skill |
| Readout | Shipped A5 readout: choice and Score 2 views (given + reversed, probability mean), yes/no 1 read. Score T = 1 always; choice and yes/no T from the leave-one-group-out rule (6.0) |
| Round 1 | 150,000 rows (60% replay), about 8,880 steps, about $27-29 |
| Round 2 | **Only if round 1's candidate passes the owner's rule (6.3).** 300,000 rows, restart from C1, about 17,750 steps, about $55-57, trimmed to fit the $100 cap |
| Candidates | **One per round, pre-registered: the final-step adapter.** No snapshots, no t < 1 blends |
| Gate | Sealed part A real text (5,000+ items; select 40% / confirm 60%) + no-harm guards (dev, security, calibration, option order) set from measured SEs |
| Power | Ship stage: about 77% at a true +2.0 pp sealed gain, 88% at +2.5; about 2% false ship at a true 0 |
| Odds (assumptions in 10.1) | P(round 2 runs) about 13% (8-22%); P(C ships) about 22% (14-33%); if it ships, its true sealed gain averages about +2.1 pp |
| Budget | <= $100 Modal for all of C, $25 reserve untouched; expected spend about $37 |
| RL | Not in this plan (section 8) |

---

## 1. Start model and adapter

**Start.** REF is C1, the shipped 4B. Step B (A11) adopted no weight-softened C1 (a = 0.9: +0.05 pp [-0.30, +0.40] on
the dev unseen set; it failed its confirm rule), so C's init is C1's adapter, the anchor targets are C1's outputs, and
C's gate compares against C1.

**Continue C1's adapter (chosen).** `train_decoder.py` supports `init_adapter`: it loads the adapter with
`PeftModel.from_pretrained(..., is_trainable=True)`. Earlier stage-2 runs (v11b, v11c) used this path. Step 0 is exactly
C1. Trainable params stay 32,464,896, and `expect_trainable` checks that. `targets` stays QWEN35 (all LoRA targets,
including the DeltaNet blocks). An attention-only LoRA is not used: recall does sit in Qwen3.5-4B's 8 attention layers,
but the attention-only gain (+10.2 vs +7.8) comes from a 0.8B model, 1 seed and 128-256 items (addendum F1,
`RESEARCH_EXTRA_6.md`).

**Not chosen for round 1: freeze C1 and add a new r16 adapter.** The literature favours it (O-LoRA table, no replay: a
new LoRA with the old one frozen scored 66.4 vs 43.7 for one continued LoRA). It needs new PEFT multi-adapter code
(`set_adapter` re-marks adapters trainable, and C1's dropout must be 0 in anchor passes). With 60% replay plus the
anchor, the forgetting gap should be small. It stays the fallback if round 1 shows forgetting, by amendment.

**Rank.** Keep r16, on empirical grounds: a competitor's switch from LoRA to full weights on the same data cost 3.0-3.7
pp, and a larger rank adds room to drift.

---

## 2. Learning rate, schedule, steps

| Item | Round 1 | Round 2 |
|---|---|---|
| Rows | 150,000 | 300,000 (or fewer, if trimmed to the budget; section 4) |
| Mean rows per step | about 16.9 (C1: 16.5 = 16 / `epochs` 0.9712; C's relation units are larger). Measured by a CPU dry run of `batches()` on the final file | same |
| `epochs` | 16 / measured rows per step, so each row is drawn exactly once | same |
| Steps (= rows / rows per step) | about 8,880 (8,720-9,090 for 17.2-16.5 rows per step) | about 17,750 (17,440-18,180) |
| Warm-up (5%, fixed in code) | about 444 steps | about 888 steps |
| Peak LR | 5e-5 | 5e-5, or 7e-5 by the rule below |
| Decay | cosine to 0 | cosine to 0 |
| "LR budget" vs C1 (sum of LR over steps; C1 = 30,457 steps at 7e-5) | about 21% | about 42% |
| Seed | new, fixed in the config | new, fixed |
| Snapshots | 25%, 50%, 75% (`snap_fracs`): **monitors only** (section 5), never candidates, never read on the sealed suite | same |

**Why 5e-5.** Lower peak LR means less forgetting and less learning (Ibrahim et al. 2024). The gate allows almost no
regression, so a little below C1's 7e-5. Replay removes most of the need for a very low LR (Marek et al. 2026: 12.5%
replay let small models keep a high LR).

**Round-2 LR rule (pre-registered).** Use 7e-5 in round 2 only if round 1 passed the round-2 rule but the mix-tuning
dev new-family gain was below +3 pp. Otherwise 5e-5.

**One pass only.** Forgetting grows with update steps (Kalajdzievski 2024). Out-of-domain skill can peak before the end
of SFT (arXiv 2509.12235); we still do not pick snapshots, because every extra candidate is an extra look.

---

## 3. Losses, weights and the C1 anchor

Everything is C1's config (`runs/q35_4b_main.json`) except `beta`, `init_adapter`, data files, seed, LR, `snap_fracs`,
the expected counts and the one new term `lam_ord` (addendum A4).

| Term | Setting | Applies to |
|---|---|---|
| Task CE | label smoothing 0.05 (MNLI 0.08), as C1 | every row |
| KD mix | `kd` 0.5: target = 0.5 x smoothed gold + 0.5 x teacher | rows with a dict `meta.teacher` |
| Exact soft targets | `meta.gold_probs` (choice) and `kd_full_src` = ["gd_gen2_probability"] only (as C1) | F8 "which outcome" choice rows use `gold_probs`; F8 yes/no rows are hard labels |
| Complement / equiv | `lam` 1.0, `sym_cons` true (symmetric KL / Jensen-Shannon) | relation pairs |
| Injection invariance | `lam_inv` 1.0, KL(stopgrad(clean) \|\| attacked) | `inv` pairs |
| Permutation twins | `perm_twin` 0.3, `lam_p` 0.5 | 30% of choice rows get a second option order in the same step |
| Ordinal mean term (**new**, addendum A4) | `lam_ord` 1.0: `lam_ord` x ramp x ((E - y) x 4/(K - 1))^2; no variance term | ordinal rows only (`meta.option_level` set): about 4,350 round-1 new rows (F7 3,150 own + commit Score 1,200) plus replay rows with level numbers (mixer count in the config) |
| Ramp | 20% warm-up ramp on all consistency terms and on the ordinal mean term (code) | |
| Base-model anchor | **`beta` 0** (off) | none |
| Aux norm | `aux_norm` "batch" | |

**Why the base anchor is off.** In code, the anchor is KL to the frozen base with the adapter disabled
(`model.disable_adapter()` in the training loop), and `init_adapter` keeps that behaviour. With `beta` > 0 it would pull
C back toward untuned Qwen3.5-4B, the opposite of "stay close to C1". C1 ran with `beta` 1.0.

**The ordinal mean term (addendum A4; the only new trainer-loss term in round 1, addendum I).**
- **What.** On an ordinal row with K levels, E = sum over the shown letters of p(letter) x level(letter), where p is the
  model's softmax over the row's option letters (the same letters the readout uses) and level() comes from
  `meta.option_level` **after** the trainer's option re-shuffle (and on the permutation twin, after its own order).
  y = the gold level index. Term = ((E - y) x 4/(K - 1))^2, so every K is put on TRACT's 1-5 range. Weight `lam_ord`
  1.0 (borrowed from TRACT), times the existing 20% ramp, added to the task loss. No variance term (addendum A7).
- **Why.** Both Score tests read the expected level E, not the top pick (ejs-5 rounds E half-to-even; JevBench v1.5.4
  grades |E - gold| unrounded). Evidence is external: RAFT on Gemma-2 2B, RMSE 0.70 (CE, top pick) -> 0.67 (CE, read
  as E) -> 0.47 (trained on E); TRACT without CoT r 0.557 -> 0.623 at lambda 1; mean-variance loss MAE 3.32 -> 2.51.
  Its effect on our letter readout and off-domain is unknown.
- **Where.** Ordinal rows only: about 4,350 round-1 new rows (F7 3,150 own + commit Score 1,200) plus replay rows that carry
  level numbers. The mixer counts them and the count goes into the config (`expect_ord_rows`); the trainer asserts it.
- **Required before launch (CPU and pre-flight; pre-flight items 10 and 11).** (i) A CPU unit test on fixed logits:
  the term and its gradient match a hand computation for K = 3, 4 and 5, under a shuffled option order and on a
  permutation twin (example: K = 4, uniform p, y = 0 gives E = 1.5 and a term of 4.0). (ii) The term is finite on every
  row of the memory pre-flight dry run and in the smoke run. **Fallback (pre-registered):** if (i) or (ii) fails and the
  fix is not a plain bug fix that then passes, the term is dropped (`lam_ord` 0) and round 1 runs on C1's losses
  alone. The choice is made on these CPU facts before any training step and is written to the look log.
- **Guard.** Ordinal Brier and nRPS on dev ordinal rows are reported for the candidate vs C1 (report-only, 6.4). The
  frozen gate still decides shipping.
- **Risk.** It is a code change in a one-candidate round and untested with a letter readout. It touches only a few % of
  the mix. The A1 target lint in `C_DATA_SPEC.md` (round_half_even(E_target) = gold on every ordinal row) must pass
  first, so the CE target and this term point at the same level.

**Loss weights (addendum E3; rule).** Round 1 keeps C1's loss weights (`lam` 1.0, `lam_inv` 1.0, `lam_p` 0.5,
`perm_twin` 0.3, `kd` 0.5) plus `lam_ord` 1.0. No PCGrad, GradNorm, LoRAMoE or weight sweep (a tuned weighted sum
matches the multi-task optimizers in Kurin 2022 and Xin 2022; a 3-point sweep costs about $85, which the cap cannot
hold). The only allowed change is in 7.3: one flagged term halved, by amendment, before round 2 only.

**Selection (addendum D1; no change).** Own rows and replay keep `C_DATA_SPEC.md` 2.1's stratified selection. No LESS,
influence-function, IFD or other targeted selection in round 1 or round 2 (LESS fell below random at 10-15% budgets in
BIDS; on 1M-row pools no selector beat random). Replay stays representative, keeping the p_g < 0.2 drop below.

**The C1 anchor (owner decision 5: "KL to C1 only where C1 is confident or on explicitly protected skills, so C can fix
C1's mistakes"). No code change.**
- **Mechanism.** It uses the existing KD path. On an anchored row the target becomes 0.5 x smoothed gold + 0.5 x C1's
  probabilities. Its gradient is 0.5 x (p - gold) + 0.5 x (p - p_C1), the same as 0.5 x CE + 0.5 x KL(p_C1 || p):
  the DER++ recipe (labels plus old-model outputs, equal weights). All anchor targets come from C1, a 4B (owner
  decision 7).
- **Where it applies (a program decides, from C1's scoring pass; pre-registered):**
  1. **Confident rows:** any replay row where C1's top answer equals gold **and** C1's top probability is >= 0.8.
  2. **Protected skills:** replay rows in (a) **security** units: `inv` relation units (clean and attacked rows) and
     golden_train's attack-resistant variant rows (`meta.attack_target` set or `role` = "attacked", plus their clean
     partners; 35,214 attacked rows in 121 sources by the `LOCAL_GAPS.md` count; C1's hijack resistance is a Jev win
     condition), and (b) **consistency** units: `equiv` and `complement` relation units. Here the anchor applies
     whenever C1's top answer equals gold, at any confidence, so C1's calibrated uncertainty on these skills is kept.
     The list is fixed in the amendment; adding a skill later needs a new amendment.
- **Where it never applies.**
  - Rows where C1's top answer is wrong, at any confidence. A confident error is exactly a mistake C must be free to
    fix, so "confident" in the owner's rule is read as "confident and right" (methods review B2 and S2 asked for the
    confidence condition; the right-answer condition is what lets C fix C1).
  - New rows (own families, public splits, commits). They exist to change C1. KL(C1 || C) on new rows is logged as a
    monitor, not a loss.
  - Rows with human vote shares or exact-probability targets: they keep their own targets.
- Rows whose only teacher is the old "blend50" model count as having no target and follow the same rule.
- **Disclosure: the step-0 KD loss is not zero.** C1's targets are two-view averages (A5 readout), while the trainer
  reads one random option order (and a random Yes/No letter order in cygnet style). The anchor therefore pulls toward
  C1's order-averaged answer, not toward its single-view logits.
- **Disclosure: protected rows soften labels a little** where C1 is right but unsure. This is deliberate (keep C1's
  behaviour on skills where it already wins); it is limited to the protected list and gated by D4 (Brier) and D5.
- Evidence for: replay with the old model's own outputs gave BWT -0.8 vs -3.0 for gold-only replay at 10% (SSR); DER++
  beat plain replay. Evidence against: a competitor's KL to its previous version on replay rows cost 2.7 pp on its hard
  tier and raised ECE from 0.046 to 0.147. That is why it is selective and why calibration is gated (D4).
- **Spec link.** `C_DATA_SPEC.md` 5 ("REF anchor targets") must carry the protected-skill clause; the mixer writes
  `meta.teacher_src` = "c1_anchor" or "c1_anchor_protected" and reports both counts for `expect_kd_targets`.

**Training inputs the recipe relies on (built by `C_DATA_SPEC.md`, checked here).** Replay rows from human-labelled
sources with C1 p_g < 0.2 are dropped (label noise collects there; methods S1); the old slice is held out by `group_id`
and normalized state; every licence and deny-list rule of the spec has been applied by program.

**Config sketch (round 1).**
```
{"name": "q35_4b_c_r1", "base": "Qwen/Qwen3.5-4B", "base_revision": "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
 "recipe": "A3", "init_adapter": "<C1 adapter dir>", "train_file": "c_parts/c_train_r1.jsonl",
 "rel_file": "c_parts/c_rel_r1.jsonl", "epochs": <16 / measured rows per step>, "lr": 5e-05, "batch": 16,
 "r": 16, "alpha": 32, "dropout": 0.05, "lam": 1.0, "beta": 0.0, "kd": 0.5, "kd_skip_src": ["blend50"],
 "kd_full_src": ["gd_gen2_probability"], "lam_inv": 1.0, "sym_cons": true, "perm_twin": 0.3,
 "lam_p": 0.5, "lam_ord": 1.0, "expect_ord_rows": <from mixer>,
 "aux_norm": "batch", "seed": <new>, "grad_ckpt": true, "style": "cygnet",
 "layout": "schema_branch_mark", "micro_tokens": 8192, "targets": "QWEN35", "snap_every": 2500,
 "snap_fracs": [0.25, 0.5, 0.75], "expect_trainable": 32464896, "expect_kd_targets": <from mixer>,
 "expect_kd_full": <from mixer>, "ckpt_every_min": 10, "log_every": 50, "no_overwrite": true}
```
`lam_ord` and `expect_ord_rows` are new config keys (A4); the trainer's config allow-list and validation must accept
them (`lam_ord` >= 0), and `lam_ord` 0 is the pre-registered fallback.

**Option shuffling.** The trainer re-shuffles choice options every time a row is drawn, and draws a random Yes/No letter
order on yes/no rows (cygnet style). One pass means each row is seen once, under one random order, plus a second order
on the 30% perm twins. Ordinal labels carry their level number, so the order can be recovered. No code change.

**Batching (methods N6).** The unit rule replaces v1's "at most 3 variants per step": a relation unit holds at most 3
rows, at most 2 if any row is over 2,000 tokens; the trainer may add permutation twins on top
(`C_DATA_SPEC.md` 2.1). An F5 negation quadruple is therefore split into two units that share a `group_id`.

**Pre-flight checks (CPU, before any paid step).**
1. `check_rows` passes on both round files (no unscorable rows).
2. The loader round-trip (G15) is 100%.
3. `expect_trainable`, `expect_kd_targets` and `expect_kd_full` match.
4. Every row is at most 7,900 prompt tokens **with the real tokenizer**.
5. **Token cap (methods S10; same rule as `C_DATA_SPEC.md` 6).** With the real tokenizer, rows of 2,000 tokens or more
   are <= 9% of new rows and hold <= 30% of new-row tokens. If not, the mixer drops whole long units from the 6-7.9K
   bin first (F13 and 3B rows), until they do, and records the count.
6. **Memory.** `_micro_groups` packs by `_est_tokens` (characters / 3.2), which undercounts code, diffs and JSON.
   Dry-run `batches()` + `_micro_groups` with the planned seed and compute every micro-batch's real cost (sequences,
   including permutation twins, x padded max length). If any micro-batch exceeds 1.25 x 8,192, set `micro_tokens` to
   6,144 (under `aux_norm` "batch" the objective does not depend on `micro_tokens`). A single unit over the budget
   becomes its own micro-batch in code; the worst case (2 long rows of 7,900 tokens + 2 twins) is about 31.6K tokens.
7. A dry run of `batches()` gives the measured rows per step, and `epochs` is set from it.
8. Smoke run on Modal (about $0.20-0.50): 20 normal steps (step-0 loss, s/step) **plus** forward and backward on the 20
   largest units by real cost. Any out-of-memory error: units with a row over 4,000 tokens become single rows (their
   `equiv` twin moves to its own unit), and the smoke is repeated.
9. **Rendered-prompt identity (addendum F2).** For 3 fixed rows (one choice, one yes/no, one Score), the sha256 of the
   **rendered** prompt string (chat template applied, before tokenization) is identical in the trainer, the dev gate
   path (`od_gcp.py predict` as used by `gate_dev.py`) and the serving path. The `decoder_io.prompt` fallback (the
   `except` branch that folds the system turn into the user turn) must **raise** for Qwen3.5 instead of silently
   rendering a different prompt. Every external server call passes `enable_thinking: false`. Reason: templates alone
   spread results by 1.4 points in Tulu 3, and locally the chat-template prompt moved a frozen model from 0.653 to 0.710.
10. **A4 unit test (CPU).** The ordinal mean term and its gradient match a hand computation on fixed logits (section 3).
11. **A4 finite check.** The term is finite on every row of the memory dry run (item 6) and at every smoke step
    (item 8). If item 10 or 11 fails, the A4 fallback applies (`lam_ord` 0, logged) before any paid training step.

---

## 4. Costs (Modal H100 at $4.09/h)

| Item | Round 1 | Round 2 |
|---|---|---|
| Rows / rows per step | 150,000 / about 16.9 | 300,000 / about 16.9 |
| Steps | about 8,880 | about 17,750 |
| At about 2.72 s/step (C1's measured rate) | 6.7 h, **about $27.4** | 13.4 h, **about $54.9** |
| Start-up, snapshots and checkpoint writes (allowance 0.5 h) | about $2 | about $2 |
| Planning total | **about $29.5** | **about $57** |
| Sensitivity: s/step +12% (C's mean prompt is longer than C1's 742 tokens) | about $33 | about $64 |
| Scoring crowd (C1 on sampled replay; C1 + 4B-E + base 4B on new candidates; about 300K row-reads per round) | free L4 (Google credit), about 20-28 h; never the H100 (`C_DATA_SPEC.md` decision 3) | same |
| Candidate reads (dev 9 splits + `_perm`, jagged, OPI, sealed select set, mix-tuning dev, monitors) | L4 credit | same |
| Hard stop | projected round-1 total > **$35** | projected round-2 total > **$100 minus all C Modal spend so far** |

**Budget rule (owner: C may spend up to about $100 on Modal; keep the $25 reserve).**
- All C Modal spend (smoke, both rounds, an RL pilot if ever asked for) stays <= $100. The scoring crowd runs on the
  free L4, not Modal (`C_DATA_SPEC.md` decision 3).
- No launch may take the Modal balance (all accounts together) below the **$25 reserve**. If both limits cannot hold,
  stop and ask the owner.
- Measure s/step over steps 100-300 of each round. If round 1's projection passes $35, stop and ask the owner.
- Before round 2 launches, its row count is trimmed (keeping the 60/40 split and every family's share) so that its
  projection, at round 1's measured s/step plus the $2 allowance, fits the remaining cap.
- Both rounds at 2.72 s/step cost about $87 with the smoke run; at +12% s/step about $97, so the trim rule may bite.
- **Expected spend**, given that round 2 rarely runs (section 10): about $30 + 13% x $57, so **about $37**.

---

## 5. Monitors and stop rules

- Every log step (code): task loss, consistency terms, gradient norm (the code alerts at 5x the 200-step median for 20
  steps; a non-finite term aborts).
- At the 25%, 50% and 75% snapshots, read on the L4 while training continues:
  - old slice: 2,000 golden_train rows held out of replay **by `group_id` and by normalized state** (accuracy vs C1,
    1->0 and 0->1 flips, mean P(yes), and KL(C1 || C) on the old slice, logged);
  - mix-tuning dev (new families, held-out samplers, packs, formats and commit repos);
  - B3 yes-share alarm (report-only; `C_DATA_SPEC.md` 10), read at a fixed T = 1 stated in advance (C1's 6.0 serving
    T is not yet fitted for snapshots);
  - KL(C1 || C) on a fixed sample of 2,000 new rows (RL's Razor monitor).
- **Snapshots are never read on the sealed suite, the dev gate splits, OHS, ejs-5, JevBench or LongBench, and are never
  candidates.**
- **Stop rule (pre-registered):** stop the run if the old slice is below C1 - 1.5 pp at both the 25% and 50% snapshots,
  or if mean P(yes) on old yes/no rows drifts by more than **0.02**. Keep the last good snapshot for diagnosis only.
  **A stopped run yields no candidate for that round**; the owner reviews, and any re-run needs an amendment.
- The old slice is C1's own training rows. It measures retention of seen rows, not generalization, so it is a monitor
  and stop rule only, never a ship rule.
- **FAM-1 monitor (addendum E1; report-only; L4 on Google credit, $0 Modal; design in `RESEARCH_EXTRA_5.md` 3).**
  Group-gradient affinity onto old and new targets, normalized by split-half reliability; yes-push attribution per
  family and per loss term; positive and negative controls; exact lookahead for the top 3 suspects. Groups: the 13
  families + about 8 replay clusters, 64 rows each, rows capped at 2,000 tokens.
  - **Step-0 read (adopted):** on C1 itself, on the L4, before round 1 launches. Its wall time is measured and logged.
    If one new family already shows rho(X -> T_old) below -0.2, or one yes-push ranks first by a wide margin, it is
    flagged to the owner before launch (report, not a rule change).
  - **25 / 50 / 75% reads (CONSIDER):** run only if the measured step-0 read took <= 50 min; otherwise FAM-1 stops at
    step 0 for this round. They read the snapshots on the L4 while training continues, like the other monitors.
  - The output is invalid for a read if its controls fail. FAM-1 never moves a weight, share or setting by itself, and
    in round 1 it decides nothing. Its only downstream use is the flag rule in 7.3 (and E4's share-cut condition, if
    adopted by amendment).

---

## 6. The gate

### 6.0 Readout and temperature pipeline (fixed now; addendum A3, A5, C1, C2, C4)

Every read of C or C1 (dev, mix-tuning dev, sealed, practice sets) uses the shipped A5 readout, in this order, except
D4 (6.4), which uses the PREREG 3.3 (d) cross-fit T instead of the serving T in step 2:

1. **Views.** Choice and Score rows: 2 views (given order + exact reversal), probability mean. Yes/no rows: a single
   read (C4). If yes/no views are ever added, they are averaged in **logit** space and every temperature below is
   refitted from scratch (C4: in a synthetic test, probability-mean put 33.4% of rows in the 0.2-0.8 band vs 27.4%
   for logit-mean).
2. **Temperature, after aggregation (C2).** Applied to the aggregated output of the exact served pipeline.
   - **Score rows: T = 1, always (A3).** The readout code asserts T == 1 on every Score row and fails the read
     otherwise. Justification: T = 1 is the shipped A5 readout (`prep89/READOUT_DEV.md`). ejs-5 did not choose it
     (addendum I). Context from dev (129 ordinal rows with gold): the NLL-optimal T for C1 is 1.6 (NLL 1.129 ->
     1.075) while nMAE of E barely moves (0.227 -> 0.229), and a T above 1 pulls E toward the middle levels.
   - **No T < 1 lever for any type (A5).** On the same 129 dev ordinal rows, rounded-E accuracy is 48.8 at T = 0.5
     (and at 0.7) vs 51.2 at T = 1.
   - **Choice and yes/no (C1):** one T per type. Fit leave-one-group-out on the mix-tuning dev, where the groups are its
     held-out sampler, pack, format and repo groups plus F14: for each candidate T, compute the NLL on each left-out
     group with T fitted on the others; choose T by the **median-group NLL**; bound it to **[0.8, 1.3]**. Fitted only
     on dev or the mix-tuning dev; never on the sealed suite, OHS-1/2/3, ejs-5, DI, JevBench or LongBench, and never
     with any Jev output. This serving T is not the D4 T (D4 uses the PREREG 3.3 (d) cross-fit T, 6.4). Evidence: in-distribution T fails under shift (Ovadia 2019); a cross-task single T kept
     about 71% of the possible ECE gain (Thermometer, MMLU 0.260 -> 0.119, best 0.062); C1's dev refit is 0.95 / 1.05
     for about 0 gain, so the bound mostly guards against a T driven by one group.
3. **Band edge (JevBench only, disclosed),** applied last: P(yes) in (0.5, 0.8) -> 0.8, in (0.2, 0.5] -> 0.2. Never on
   OHS, sealed or D4 Brier endpoints.

Temperature does not change any argmax, so accuracy endpoints (P1, P2, P3, R1, D1-D3) are the same at any T. On Score
rows T would move E, which is why A3 fixes it at 1. D4 (6.4) is computed on the view-aggregated output of step 1 with
the PREREG 3.3 (d) cross-fit T (not the step-2 serving T), never on a 1-view choice read (Wu & Gales effect: choice 2-view ECE 0.032 -> 0.038).

### 6.1 Sets, sizes and conventions

- **REF:** C1. It is read in the same job as the candidate (PREREG_FINAL 3.4 pipeline check: one job, metas written by
  `od_gcp.py predict`, pinned base revision and chat-template sha). The refparity look compares the fresh C1 read with
  the stored C1 read `q35_4b_main500k` (not 4B-E's `q35_4b_pxE_parity`); the amendment records this.
- **The served artifact is what gets gated.** If serving merges the LoRA into bf16 weights, the gate reads the merged
  bf16 model. A parity check on dev must show argmax agreement >= 99.9% between the adapter read and the merged read.
- **Sealed new-domains suite: preconditions (owner decision 6; methods B4).** The gate refuses to run unless all hold,
  as recorded in the amendment:
  1. It was built by a separate agent session with no access to any C data, spec drafts of C families, or C builders'
     folders, and C builders never had access to it (`C_DATA_SPEC.md` "Who may read what").
  2. Its source pool **and** its templates and format styles differ from every C training source and template
     (name check plus counts-only text and structure hashes, `C_DATA_SPEC.md` 7).
  3. It was **frozen and its sha256 recorded in a PREREG amendment before any C training row was generated** (the
     first C generator run is after that commit; the build log shows the order). Its scorer is frozen with it; both
     sha256 are in A15 (6.2).
  4. MultiDoc2Dial and NLU++ are not in it; no domain is an OHS-1/2/3 source or next to an OHS-3 domain.
  5. Every part-A domain carries an "adjacent" or "non-adjacent" label fixed at freeze, before any model read; part A
     has >= 4 non-adjacent domains holding >= 50% of its items, 6-10 domains, and no domain above 20% of part A.
  6. Scoring prints aggregates only (overall, per part, per set, per domain, per question type). **Nobody inspects
     per-item failures**, for any model, at any time.
- **Sealed sizes (methods B3).**

  | Part | Items | Use |
  |---|---|---|
  | A, real text | **>= 5,000** (target 5,000-6,000) | Select set: sha256("ndsel:" + group_id) mod 5 in {0, 1} (about 40%, >= 2,000 items). Confirm set: mod 5 in {2, 3, 4} (about 60%, >= 3,000 items) |
  | P, program-built | 600 | Report only, read only at the confirm look |
  | B (B1 commits 300 + B2 long documents 200) | 500 | P3 guard, read only at the confirm look (both sets) |

  Every sealed read uses the served pipeline of 6.0 (choice and Score given and reversed order averaged; yes/no once;
  choice and yes/no at that model's 6.0 serving T; Score T = 1 asserted; no band edge), for the candidate and C1 in the
  same job. Accuracy and the B3 mean P(yes) and yes share (6.2) are both computed from this one served output.
  This superseded v2's 3,200-4,000 items and parity halves; `C_DATA_SPEC.md` 9 (v3) now carries the same layout and
  split. Why 40/60: the round-2 rule's +2.0 pp point threshold binds before its LB does at any
  select SE below 1.0, so extra select items buy little; extra confirm items buy ship power.
- **Standard errors (assumptions stated).** SE of the paired difference = cluster factor x sqrt(d / n). Two related 4Bs
  disagree on 5.3-7.0% of dev unseen rows (measured: v11b/v11c vs v11, C1 vs 4B-E); far real-text domains are harder,
  so the plan assumes d = 10% (range 7-14%) and a cluster factor of 1.2 (items share source records).

  | Set | n | SE at d = 7% / 10% / 14% | Smallest point gain with 95% LB > 0 (at d = 10%) |
  |---|---|---|---|
  | Select | 2,000 | 0.71 / **0.85** / 1.00 | 1.67 pp (the round-2 rule's +2.0 binds) |
  | Confirm | 3,000 | 0.58 / **0.69** / 0.82 | 1.36 pp |
  | Part A per domain (both sets) | about 550 | 1.35 / **1.62** / 1.91 | n/a (P2 uses the upper bound) |

  The realized SE comes from the round-1 select read (bootstrap). It is written to the look log and the confirm-stage
  power is re-stated from it **before** the confirm look. The rules do not change. If part A ends below 5,000 items,
  the rules stay and the power is re-stated (at 4,000 items the ship power at a true +2.0 pp falls to about 65-70%).
- **Dev:** the 9 gate splits read by the existing `gate_dev.py --mode ship` machinery (standard read, seeded `_perm`
  read, jagged and OPI). `gate_dev.py` is not changed; its own verdict line (built for dev-improving candidates) is
  printed but does not decide C. **The C verdict comes from a small new wrapper, `gate_c.py`** (CPU, with tests), that
  reads `gate_dev.py`'s JSON and the sealed scorer's JSON and applies only the thresholds in 6.3 and 6.4 (methods S13).
  Its tests: (i) it reproduces the near-null numbers below from the same preds; (ii) every rule at its boundary;
  (iii) it refuses a second confirm look and a candidate that is not the pre-registered final-step adapter (sha256);
  (iv) it refuses missing `_perm`, jagged or OPI reads.
- **Bootstrap:** paired, over `group_id`, 10,000 resamples, seed 0, 95% percentile interval. LB / UB = lower / upper
  bound of CAND - REF. Seed-to-seed training noise (about +/- 1-2 pp in a competitor's runs) is not in the item
  bootstrap; it matters when reading round 1 as "breadth works", not for the shipped model. A "no difference" result
  does not mean equal.
- **Measured dev standard errors (`sim/nearnull_calib.py`, 3 Oct; C-like pairs = stage-2 top-ups v11b, v11c vs v11,
  which answer 7.6-8.3% of dev rows differently).**

  | Dev quantity | SE (pp) |
  |---|---|
  | Full set without tb_mixtral (7,056 rows, 3,005 units) | 0.43-0.46 (C1 vs 4B-E: 0.52) |
  | Each dev half | 0.56-0.67 |
  | Yes/no / choice | 0.62-0.67 / 0.51-0.56 |
  | Dev unseen-source set (3,847 rows, 1,519 units) | 0.49-0.53 |

- **Near-null calibration (methods B3; done).** A11's wise090 vs b100 (C1) on the 9 dev splits: unseen +0.05 [-0.30,
  +0.40]; full +0.01 (LB -0.30); halves +0.08 / -0.06; yes/no -0.05; choice +0.09; calibrated Brier +0.0000;
  equivalence flips 8.45% vs 8.86%. **No v3 dev rule fires.** Limits: wise090 differs from C1 on only 1.4% of dev rows,
  so this checks the rules at small disagreement; the SEs above cover C-like disagreement. (f) and (g) were not
  checkable (no `_perm`, jagged or OPI reads for wise090). Two observations shaped v3: A11's point rule on complement
  violations (4.47% vs 3.58%) vetoed this near-null model, so complement violations stay report-only; and C1 vs 4B-E
  moved equivalence flips by +3.2 pp (8.86% vs 5.68%), so (e) is a real, not a noise, veto and stays decisive.

### 6.2 Candidates and looks (fixed now)

- **One pre-registered candidate per round:** the final-step adapter of that round's run, at full strength, gated as
  served. Its sha256 is written to the look log when training ends, before any read. No snapshot, blend or re-scaled
  adapter is ever a candidate (A11, FREEZE.md finding 5 and a competitor's WiSE-FT all found t < 1 flat or worse).
  Snapshot averages and seed soups are excluded too (addendum F5, REJECT: Tulu 3's seed soup equalled the best seed at
  SFT scale, 60.2 vs 60.1). If a blend is ever wanted later, by amendment, it blends the LoRA products (rank-32
  concatenated adapter or an fp32 merge), never the A and B factors separately.
- **Sealed looks (logged by the scorer in `sealed_nd/looks.jsonl`, which the scorer reads before every run):**

  | Look | When | Reads | Decides |
  |---|---|---|---|
  | S1 | after round 1 | round-1 candidate: part A select set | round-2 rule (6.3) |
  | S2 | after round 2, only if it ran | round-2 candidate: part A select set | finalist choice |
  | C | once, when the owner declares C finished | finalist: part A confirm set + all of part A per domain + parts B and P | ship (6.4) |

  A look not in this table needs an amendment first (for example a changed round 2 after a diagnosis: one more select
  look for its one candidate). The scorer refuses a second C look whatever the candidate. Every look also prints the
  gold-free B3 yes-share alarm (mean P(yes) and yes share per set and domain on yes/no items, from the same 6.0 served
  output as the look's accuracy; `C_DATA_SPEC.md` 9), report-only; it decides nothing. If the frozen sealed scorer
  lacks B3 printing, B3 is dev only (`C_DATA_SPEC.md` 9).
- **Sealed scorer freeze.** The scorer (aggregates only, look log, refusals, B3 printing) is written and CPU-tested on
  dummy predictions with the sealed suite, by the sealed agent, and frozen with it: the orchestrator records the
  sealed scorer's sha256 in amendment A15, alongside the suite sha256, before any C training row exists (11 step 2). `gate_c.py` refuses a scorer whose
  sha256 differs from A15. No later change to the scorer without a new amendment.
- **Finalist:** if round 2 did not run, round 1's candidate. If it ran, the candidate with the better select-set point;
  a gap under 0.3 pp goes to round 2. The confirm set is untouched by both choices.

### 6.3 Round-1 go / no-go (owner rule, 3 Oct about 06:30 UTC)

Round 2 runs **only if all** of these hold for round 1's one candidate:

| Rule | Pass when |
|---|---|
| R1 clear sealed gain | Part A **select set**: CAND - C1 >= **+2.0 pp** and paired 95% **LB > 0** |
| R3 no harm | Guards D1-D6 of 6.4 pass (dev, security, calibration, option order), with the same thresholds |

- **Power of this rule** (select SE 0.85, dev +0.3, no harm elsewhere; `gate_sim_c.py`): P(round 2 runs) is about 1% at
  a true round-1 gain of 0, 11% at +1.0, 26% at +1.5, 47% at +2.0, 67% at +2.5, 82% at +3.0.
- **P(round 2 runs) under the prior (10.1): about 13%** (8% pessimistic, 22% optimistic). Round 1 is the main shot.

Diagnostics (reported, not part of the go rule):
- R2 learning: mix-tuning dev, new-family items, CAND - C1 >= +3.0 pp. If R2 fails, hunt for generator or data bugs
  (G17) first.
- R4 retention: old slice >= C1 - 1.0 pp.
- If R1 or R3 fails: no round 2. The owner reviews a diagnosis first (likely a breadth or transfer problem). A changed
  round 2 needs a new amendment and costs one more select look.

### 6.4 Final ship rule (one confirm look)

C replaces C1 **only if all** hold for the finalist:

| # | Rule | Pass when | Noise-only false veto (no true harm) |
|---|---|---|---|
| P1 | Sealed part A, **confirm set** (>= 3,000 items) | CAND - C1 >= **+1.0 pp** and paired 95% **LB > 0** | n/a: this is the superiority test |
| P2 | Sealed part A, each domain (both sets, about 550 items) | no domain with UB < **-2.0 pp** (flags a point drop of about -5 pp) | about 0% |
| P3 | Sealed part B (B1 + B2 pooled, both sets) | not UB < 0 | about 0% (at an assumed true part-B gain of +2.5) |
| D1 | Dev full set (9 splits without tb_mixtral, 7,056 rows) | 95% **LB > -1.5 pp** (non-inferiority; at SE 0.43-0.46 this needs a point above about -0.6) | about 6% at a true 0 |
| D2 | Dev unseen-source set, **re-derived** with C's training files (`C_DATA_SPEC.md` 7.3) | **not** (point < -1.0 pp **and** UB < 0) (clear-harm veto). The frozen 3,847-row set is reported | about 2.5% |
| D3 | Dev yes/no and choice | PREREG 3.3 (b), (c) unchanged: each point >= C1 - 1.0 pp | about 6% / 3% at a true 0 |
| D4 | Calibrated yes/no Brier with T exactly as PREREG 3.3 (d): per model, per type, fitted on one dev half and applied to the other, `calibrate.py` grid 0.25-10.0 (step 0.05), pooled over all yes/no rows of the full set, applied to the 6.0 view-aggregated output (single yes/no read, no band edge). The 6.0 leave-one-group-out serving T is reported but never used for D4 | PREREG 3.3 (d) unchanged: <= C1 + 0.005 | about 0% |
| D5 | Equivalence flips (722 pairs) and permutation flips (option order) | PREREG 3.3 (e), (f) unchanged: each <= C1 + 2 pp | about 2% / 0% |
| D6 | Jagged and OPI attack success | PREREG 3.3 (g) unchanged: fail only if above max(C1 + 2 pp, 3%) and the increase's LB > 0 | about 0% |
| D9 | Latency p50, single view | <= C1 x 1.05 (same architecture, merged r16 adapter) | 0% |

**Why the dev thresholds differ from PREREG 3.3 (a), (a2) and v2's D2.** PREREG's set was built for candidates whose
target *was* dev. For C, dev is a guard. Measured SEs show PREREG (a) LB > -1.0 needs a point above about -0.1 pp and
(a2) adds two more point tests; together with v2's D2 non-inferiority they pass a truly dev-neutral model only about
41% of the time. All v3 guards D1-D6 together (noise only, no true side harm):

| True uniform dev effect | -1.5 | -1.0 | -0.5 | 0.0 | +0.3 | +0.5 |
|---|---|---|---|---|---|---|
| P(pass) v3 | 1% | 14% | 52% | 85% | 93% | 95% |
| P(pass) PREREG 3.3 unchanged + v2 D2 | 0% | 1% | 10% | 41% | 62% | 73% |

So v3 still blocks a real 1 pp dev drop about 86% of the time and a 1.5 pp drop 99%; yes/no and choice keep PREREG's
own -1.0 pp point rules. (a2) is report-only because C never selects on a dev half (selection uses the sealed select
set), so the risk (a2) guards against, a gain that exists only in the half used for selection, cannot arise.

**Power of the ship gate (methods B3; `gate_sim_c.py`, confirm SE 0.69, finalist with no true harm elsewhere).**

| True sealed gain of the finalist | -1.0 | 0.0 | +1.0 | +1.5 | +2.0 | +2.5 | +3.0 |
|---|---|---|---|---|---|---|---|
| P(ship), dev true +0.3 | 0% | 2% | 28% | 54% | **77%** | **88%** | 92% |
| P(ship), dev true 0.0 | 0% | 2% | 26% | 49% | 70% | 81% | 84% |

The plateau near 92% (84% at dev 0) is the guards' noise-only false veto. At confirm n = 2,000 the +2.0 pp power is
61% (dev +0.3); at n = 2,500, 70%.

**Report only (never decisive):** complement violations; old slice; hard-negation probe; (a2) dev halves; part A's
non-adjacent subset and adjacent subset; part P (program-built, reported separately from part A real text); B1 and B2
separately; the frozen D2 set; dev with tb_mixtral; per-split differences; mix-tuning dev; the F14 hold-out family;
Codebook behavioural tests; ECE; the realized confirm SE; **ordinal Brier and nRPS on dev ordinal rows, CAND vs C1**
(addendum A4's guard on the new term; served pipeline, Score T = 1); **Brier and the over/underconfidence gap (mean
confidence minus accuracy) per type on the unseen-group mix-tuning dev**, CAND vs C1 (addendum C3: C1's miscalibration
flips sign under shift, OHS-1 yes/no +3.2 vs OHS-2 -4.9, which dev-wide D4 cannot see); FAM-1 tables (5); B3
yes-share alarm on sealed looks (`C_DATA_SPEC.md` 9), never decisive.

- **Claims.** P1 passing means the 95% LB is above 0, so a shipped C may say "better than C1 on unseen real-text
  domains (sealed suite)". Public-set gains (for example on DI tasks that share a design with our families) are
  labelled "fine-tuned on related data", never "unseen".
- **Jev outputs (rules S6).** No Jev output (`bench/runs/jev_*`, jagged trial records with `jev_recorded_p_yes`,
  ejs-5 published answers, OHS Jev runs) is ever an input to training, selection, thresholds, temperatures or this
  gate. The single Jev read on the sealed suite (`C_DATA_SPEC.md` decision 10: once, at the C look, after the ship
  verdict is logged; its API spend needs the owner's GO) is stored under `sealed_nd/` and is report-only.
- **After SHIP, once each, in this order, none of which changes the choice:** ejs-5 (PREREG_ejs5 settings; now an
  **in-domain** test, disclosed; report the full set (endpoint), the 268 late rows and Gate (both report-only, spec
  4.4), each as C - Jev and C - C1 with paired 95% CIs. The registered endpoint is unchanged. A tie on the full set is
  the realistic best case (`C_DATA_SPEC.md` 4.4, addendum B5)); OHS-1/2 (practice sets now; report only; C1 vs
  Jev was -1.2 [-2.9, +0.4] and -0.6 [-2.2, +1.1]); JevBench (practice, partly seen; report only; no development on its
  231 items); then OHS-3 (owner GO, once). LongBench v2 stays sealed; a read needs its own owner GO and is report-only
  (Jev's LongBench number may not be published).
- **If the finalist fails:** nothing ships from C, C1 stays, and there is no second confirm look.
- **Temperature refit (calibration only; 6.0):** choice and yes/no only, leave-one-group-out on the mix-tuning dev,
  median-group NLL, bounded to [0.8, 1.3]; Score T = 1. Never fitted on the sealed suite, OHS-1/2/3, ejs-5, DI,
  JevBench or LongBench, and never on a Jev output.
- **No test-time prior fix ships** (batch calibration, EM / BBSE prior adaptation, median cut; addendum B4 and C7).
  Serving is one request at a time, and EM collapsed on C1's ejs-5 probabilities (Gate 100% "no").

---

## 7. Between rounds (only if round 2 runs)

### 7.1 What round 2 changes
Round 2 = all round-1 rows + 150K more (90,000 fresh replay; 45,250 own rows from **new** cards; 8,750 public; 6,000
commits; `C_DATA_SPEC.md` 0), trimmed to the budget if needed. Restart from C1, not from round 1's candidate. Sequential stages compounded
forgetting before (FREEZE.md finding 7), and joint training beat sequential training in every table in the
weight-preservation report.

### 7.2 Bounded family-weight update (pre-registered)
- Measure on the mix-tuning dev (400 items per family): Delta_f = CAND - C1 (paired bootstrap), and headroom h_f =
  C1's error minus about 1% (label and ambiguity floor).
- Weight x 1.5 only if Delta_f >= +5 pp, h_f > 5 pp **and** the bootstrap p < 0.05; x 0.67 only if (Delta_f <= 0 with
  p < 0.05) or h_f < 2 pp; else x 1 (uniform). With 400 items the paired SE is about 1.8-2.5 pp, and seed noise comes
  on top, so most families will stay at x 1.
- F5's round-2 share uses the hard-negation probe in place of its family items, under the same rule.
- Depth caps for round 2 come from the depth sweep (`C_DATA_SPEC.md` 10).
- Clip each family to [0.5/13, 12%] of own rows, renormalize.
- If the overall mix-tuning-dev change is negative, freeze the weights and hunt for a data bug first.
- Never use the sealed suite for weights. No proxy-model mixture search: Aioli found no published method reliably beat
  stratified sampling, and our power (minimum detectable effect 1.4-3.8 pp) cannot separate mixtures.
- **FAM-1 share cuts (addendum E4; CONSIDER, needs an amendment).** If adopted, a family's share may also be cut,
  inside the bounds above, only when its FAM-1 rho(X -> T_old) has a jackknife CI below 0 at >= 2 snapshot reads, the
  exact lookahead agrees in sign, and the old slice points the same way. Gradient evidence alone never moves a share.

### 7.3 Loss weights between rounds (addendum E3; rule)
- Round 2 keeps round 1's loss weights, with **at most one** change: one flagged term's weight is **halved** (for a
  relation term, 1.0 -> 0.5), by amendment, written before round 2 launches. Never two changes at once.
- A term is flagged only by the `RESEARCH_EXTRA_5.md` 4 flag rule at >= 2 of 3 FAM-1 snapshot reads (sign conflict
  with both the new and old targets, or a positive yes-push with P(yes) on old gold-no rows rising). The first
  candidate to watch is relation `lam` 1.0 (R-Drop: a consistency weight of 1.5 was worse on all 4 GLUE tasks shown,
  MNLI best at 0.5).
- If the 25/50/75% FAM-1 reads did not run (step-0 read > 50 min, section 5), no term can be flagged and the weights
  stay as in round 1.

---

## 8. RL: not in this plan

- With a one-token readout, RL is cross-entropy with a different weight per row. Exact REINFORCE on a 0/1 reward
  weights each row by p_g; GRPO by sqrt(p_g / (1 - p_g)). At p_g = 0.01 (a confident error) that is 0.01-0.10 of CE's
  weight. C1's weak spots are exactly such confident errors.
- With vote-share rewards, RL is mode-seeking and throws away the calibration that soft CE keeps.
- The only published 4B text-classification comparison (GTA, Qwen3-4B) had GRPO at 82.3 vs SFT 86.0.
- This matches the adopted rule "RL only after the SFT baseline, as a controlled pilot". If the owner asks for a pilot
  after C's gate: exact-expectation GRPO weights on new hard-label rows only, 3,000 steps (about $9-11, inside the $100
  cap and above the $25 reserve), adopted only if the new-family probe gains >= +1.0 pp with the CI excluding 0, the
  negation probe is not lower, dev is within -0.3 pp and ECE is not worse by more than 1.0. It would need its own
  amendment and could not use the sealed confirm set (already spent). My estimate of passing: about 10%.
- **Reopen only if** a generated-reasoning readout is ever considered (a separate decision; it breaks the 16.6 ms
  latency).

The RL ideas that do transfer are already in the recipe: stay close to the start model (selective C1 anchor), train
where the model fails (crowd-scored selection), pick on out-of-domain data (sealed select set).

---

## 9. Ranked hypothesis table

Effects are my estimates for **sealed part A (real-text unseen domains) accuracy vs C1**, unless stated. Literature
numbers come from different models and tasks. Effects overlap, so they do not add up.

| # | Method | Expected effect | Evidence (numbers) | Cost | Main risk | Verdict |
|---|---|---|---|---|---|---|
| 1 | Task-card breadth: >= 2,000 cards, <= 128 rows per card, 12% family cap, >= 4 samplers per family | +0.5 to +2.0 | Super-NI: log-linear to 757 tasks, flat after about 64 rows per task; Flan 2022: log-linear to 1,836 tasks at 3B; Zhang 2024: < 300 instructions never generalized, >= 1,000 always; Kev: +9.1 pp from breadth | $0 GPU | Template artifacts (sampler paradox 99.9 -> 57.3) | USE |
| 2 | Format and wording variety (>= 5 wordings per card, about 400 styles, 50 held out; few-shot 5-10%; inverted 10-15%; short or no card 15%) | +0.5 to +1.5 mean; more on the worst format | Sclar: 76-point spread from format; Sadrieh and Stefanik: +1.9 to +5.6 at 0.6-8B; Flan: removing inversion cost 8.6 MMLU; PAFT +1.4 to +5.8 | $0 | Low | USE |
| 3 | Real-text codebook variants (30% of F10/F11) + definition reading (masked names, swaps, examples in definitions, invented jargon) | +0.5 to +2.0 | Real beat zero-shot synthetic by 16.9 pp and real seeds added 10.3 pp (Li et al. 2023); GoLLIE 42.3 -> 55.3 F1; Codebook LLMs: 7-12B lean on label names | $0 | Human label noise in the source sets (G5 dataset-level) | USE |
| 4 | Commit decisions from other repos (12K; equal shares, 20% per type, `C_DATA_SPEC.md` 4.2; n8n and OHS guards) | ejs-5 median +1 (80%: -1.6 to +3.6); sealed B1 +3 to +10; part A about 0 | ejs-5 -4.4 with 0 code rows in training; late rows already tie (46.3 vs 45.9), and Jev's base may have seen n8n history (suggestive, z about 1.9), which other repos cannot supply | $0 + its share of steps | Our rubrics differ from ejs-5's; ejs-5 is now in-domain | USE |
| 5 | Natural negation quadruples; double negation 2-5% with twins; P(yes given negation count) = 0.5 | hard-negation probe +2 to +6 (in family); overall 0 to +0.5 | Weak local evidence: JevBench hard yes/no 9/19 vs 11/19; dev neg/dneg show no C1 weakness; one frame holds 29 of 30 flips. CondaQA consistency 42 vs 81 human; negation training +1.8 to +9.1 | $0 | Counting shortcut (blocked by G10) | USE (sized by the probe) |
| 6 | Contrast twins 20-25% + one-attribute distractors | +0.3 to +1.0; +5 to +10 on contrast subsets | Kaushik: +3.6 to +5.1 out of domain (sentiment), about 0 for NLI; contrast sets drop models up to 25% | $0 | Low | USE |
| 7 | Licensed human splits (17.5K from 14 sets, <= 3K per set, soft labels kept; commercial-use licences only) | +0.3 to +1.0 | Li et al. 2023 (above); Laurer: +9.4% held-out from 33 datasets | $0 | Licence or overlap errors (G1, G13) | USE |
| 8 | Weak-primitive families (precedence, record chains, shallow rule arithmetic, ordinal, 20-60-label taxonomies, NEI gold) | in family +5 to +10; far +0.2 to +0.8 | dev: pg_multihop -11.3, pg_policy -10.7 vs 4B-E; event-log family +12.8 (competitor); **against:** A18 narrow hard items gave -0.69 on broad dev | $0 | Gains stay in family | USE (capped at 12% per family) |
| 9 | 60% stratified replay + C1 anchor where C1 is right and confident, or right on a protected skill | Protects; prevents -1 to -5; gain about 0 | LoRA sequential BWT -45.7% vs +2.6% with 10% replay (TRACE); self-output replay -0.8 vs gold -3.0 (SSR); A18: 48% replay still forgot slightly | in the scoring pass | Anchor hurt a competitor's hard tier and ECE (gated by D4) | USE |
| 10 | Crowd-scored, label-stratified selection; drop human-labelled replay rows with p_g < 0.2 | +0.2 to +0.8 | Cartography: 33% most ambiguous beat 100% out of distribution (WSC 87.6 vs 86.0); HLE: model-failed items were 18-29% wrong | L4 credit | Hard rows collect label errors (G5 re-read) | USE |
| 11 | Long documents: 4.5% own (coherent, F13 4.1K) + 1.9K real public (QuALITY, Qasper), 2-7.9K tokens, token cap 30% of new-row tokens | long-doc tasks +1 to +5; overall 0 to +0.3 | C1: 0.39% of rows > 2K tokens; ProLong: synthetic long SFT hurt; competitor: filler cost 22-43 pp and moved real docs +/- 1 | about +15% tokens | Synthetic-long harm (real docs + no filler) | USE (small dose) |
| 12 | Tool and action selection with Claude-written API catalogs | DI tool tasks +2 to +5 (labelled "related design"); overall about +0.1 | C1 has 0.06% tool rows | $0 | DI claim optics (disclosed) | USE |
| 13 | Per-type temperature (6.0): choice and yes/no only (Score T = 1), leave-one-group-out on the mix-tuning dev, median-group NLL, bounded [0.8, 1.3], fitted after view aggregation on the served pipeline | accuracy 0; calibration better under shift (C1's OHS yes/no Brier trails Jev: OHS-1 0.140 vs 0.114 on the registered 527 yes/no base rows, 0.152 vs 0.133 on all 2,972 yes/no rows incl. variants; OHS-2 0.057 vs 0.038, registered) | Kev: ECE 0.059 (in-source fit) vs 0.0085-0.017 (held-out-dataset fit); Thermometer TS-CV 0.260 -> 0.119 (oracle 0.062); Ovadia: in-distribution TS fails under shift | $0 | Few groups (keep the bound) | USE (calibration only) |
| 14 | 75% snapshot as a second candidate (K4) | 0 to +0.5 | Out-of-domain skill peaks early in SFT (arXiv 2509.12235) | reads only | An extra look; owner rule is one candidate per round | NO (monitor only) |
| 15 | Post-hoc t-grid blends {0.5, 0.75}, blends with C1, snapshot averages, seed soups (addendum F5: REJECT) | 0 | FREEZE.md finding 5 (flat on our unseen dev); Kev (failed); A11 on C1: a = 0.9 +0.05, lower a worse; Tulu 3 seed soup 60.2 vs best seed 60.1 | reads only | Extra looks lower P(ship) | NO |
| 16 | Frozen C1 + new stacked adapter | retention 0 to +0.5 | O-LoRA table, no replay: 66.4 vs 43.7 | code + tests + smoke | New PEFT code paths | MAYBE (fallback by amendment) |
| 17 | 4-view test-time readout | choice +0.3 to +1.0 | Cyclic permutations: MMLU 50.8 -> 54.7 (13B); C1 already reads choice twice | 2x choice latency | Latency claim; any yes/no views must be logit-averaged and every T refitted (addendum C4) | MAYBE (report only) |
| 18 | Batch / domain-context calibration, EM+BCTS per-set prior readout, Thermometer-style T predictor, OTTER, weighted conformal (addendum C7: REJECT; B4: no test-time prior fix ships) | 0 to +2 on skewed domains (in-context learning) | Fei et al.: up to +37 macro-F1 (in-context learning); they need test batches or label priors we lack per request; too few groups for a T predictor | $0 | Assumes balanced classes; EM collapsed on C1's gold-free ejs-5 probabilities | NO (was MAYBE in v3) |
| 19 | PriDe letter debias | about 0 | C1 picks the first option 22.9% vs gold first 22.0% (dev) | $0 | None | NO (measure only) |
| 20 | Rationales as an extra training task | -0.5 to +1.5, unknown at 4B | Distilling step-by-step +8 on ANLI (generation models) | code + about $4 | Trainer has no generative loss | NO |
| 21 | RL (GRPO, PPO, RLCR) | -0.5 to +0.3 | Section 8; GTA: GRPO 82.3 vs SFT 86.0 at 4B | $10+ | Starves confident errors | NO (pilot only on request, after C's gate) |
| 22 | Higher rank or full fine-tuning | about 0 | Competitor full weights -3.0 to -3.7 | more $ | More forgetting | NO |
| 23 | Domain-adversarial, IRM, contrastive losses | <= +1 | DomainBed: nothing beat plain training by > 1 point | code | | NO |
| 24 | Curriculum ordering | about 0 | Marginal on standard data | | | NO |
| 25 | Mixture proxies (DoReMi, RegMix) | not measurable | Aioli: none beat stratified reliably; our MDE 1.4-3.8 pp | about $13 | | NO |
| 26 | Training on Decision Index test-set sources (ESCI, GSM8K, HoVer ...), even their train splits | DI up, unseen domains 0 | Contamination optics; the board removes trained-test models; `C_DATA_SPEC.md` 3.G excludes them | | | NO |
| 27 | Replay below 50% | +0.3 to +1.0 on new skills | Ibrahim: 25% enough for a strong shift | | Regression (owner rule) | NO (keep 60%) |
| 28 | Chain-of-thought at inference | +0.7 outside math | "To CoT or not" meta-study | latency x10+ | Breaks the speed win | NO |
| 29 | Ordinal mean term on E, `lam_ord` 1.0 (addendum A4; 3) | Score rows: E error down; sealed part A about 0 (a few % of the mix); off-domain effect unknown | RAFT (Gemma-2 2B) RMSE 0.70 -> 0.47 trained on E; TRACT r 0.557 -> 0.623 at lambda 1; mean-variance MAE 3.32 -> 2.51 | code + CPU test | Untested with a letter readout; lambda borrowed | USE (fallback: drop if unit test or pre-flight fails) |
| 30 | Score temperature T != 1, or any T < 1 (addendum A3, A5) | rounded-E accuracy down (dev: 48.8 at T = 0.5 vs 51.2 at T = 1); T = 1.6 flattens E | dev ordinal rows (6.0) | $0 | Collapses end levels | NO (Score T = 1 asserted) |
| 31 | Ordinal scales only in natural or fully reversed order in training permutations (addendum A6: CONSIDER) | small; view agreement already 89.4% under random shuffles | competitor lesson J | trainer code | Code change in a one-candidate round | MAYBE (round 2 only, by amendment, if round 1's dev ordinal view agreement is below 89%) |
| 32 | Variance term (Pan et al. lambda2), CORAL/CORN "at least level k?" yes/no rows, SORD soft labels (addendum A7: REJECT) | negative on calibration | variance term hurts nRPS / Brier; level-k rows untested for LLMs and add yes/no rows that can feed the yes bias; SORD targets risk failing the A1 lint | | | NO |
| 33 | LESS, RDS+, influence, IFD or other targeted selection; a new selection-target split; LIMO / s1 copies (addendum D1 and D3: REJECT) | about 0 or below random | BIDS: LESS below random at 10-15% budgets (44.4 vs 44.9); no selector beat random on 1M-row pools (2410.09335); LIMO and s1 need bigger teachers and CoT | about 20-30 L4-h | Copies the target's answer format | NO |
| 34 | Facility-location picks of public rows (3A-3E) on C1 hidden states (addendum D2: CONSIDER) | small, mostly worst case (QDIT) | only these pools have a low keep ratio | code in the G9 pass | Must not slow G9 | MAYBE: D2 is decided once, in the C PREREG amendment (before any C row exists). It is adopted for round-1 public rows (3A-3E) only if the G9 L4 pass can log C1's pooled hidden states at no extra time. Otherwise it lapses for C (it cannot be added later) |
| 35 | PCGrad, GradNorm, LoRAMoE, or a loss-weight sweep (addendum E3) | about 0 | Kurin 2022, Xin 2022: a tuned weighted sum matches them; a 3-point sweep costs about $85 | $85+ | Breaks the cap | NO (one halving by amendment only, 7.3) |
| 36 | FAM-1-driven share cuts between rounds (addendum E4: CONSIDER) | unknown | Xin: act on shares, confirm on outcomes | L4 reads | Gradient noise | MAYBE (round 2 only, by amendment, under 7.2's conditions) |
| 37 | Attention-only LoRA targets (addendum F1) | unknown at 4B | +10.2 vs +7.8 from one 0.8B seed on 128-256 items | | | NO (keep QWEN35) |

---

## 10. Expected value: P(ship), and can C close the gap to Jev?

### 10.1 Assumptions (all mine except the measured dev SEs; the simulation is `sim/gate_sim_c.py`)
- True sealed part A gain of round 2's candidate over C1: median **+1.0 pp**, 80% interval -1.0 to +3.0. Round 1's
  candidate gets about 0.7 of that (half the new data), plus noise SD 0.5. (Our history is weak: A18 failed, C1's dev
  gain did not reach ejs-5, and earlier training moved OHS-1 by only +0.3 over the untrained base.)
- Sealed: part A 5,000 items, 40/60 split; disagreement d = 10% (7-14%), cluster factor 1.2, so select SE 0.85 and
  confirm SE 0.69; both candidates read on the same select items (shared noise share 0.6). 9 domains, between-domain
  spread SD 1.5 pp.
- Dev: true full-set effect +0.3 pp, SD 0.6 (C's families target the pg_* and negation dev splits; the stage-2 analogs
  v11b and v11c gained +1.0 and +1.5 on this set). Sub-effects (yes/no, choice) vary around it with SD 0.4; the
  unseen-source effect is 0.4 x it, SD 0.5. Sampling SEs measured (6.1).
- Side effects: true Brier change SD 0.002; equivalence-flip change mean -0.3, SD 1.2 pp; attack harm in 2% of runs.
  Part B true gain +2.5 pp, SD 2.0.
- OHS-like: the finalist's true gain = 0.6 x its sealed gain + noise SD 0.8. C1's start gap = **-1.0** (A12 pooled;
  OHS-1 -1.2, OHS-2 -0.6), with SD 1.0 for set-to-set spread and the practice read's own error, and OHS-3 read SE 1.0.
- ejs-5 (in-domain): true gain if shipped median +1.0, SD 2.0; paired SE 1.75 (from the measured CI -7.8 to -0.9).

### 10.2 What the plan does (prior-averaged)

| Scenario | P(round 2 runs) | P(C ships) | P(ships, finalist true >= +2) | P(ships, finalist true <= 0) | True gain if shipped | Expected shipped gain (0 if not) |
|---|---|---|---|---|---|---|
| **Base** (part A 5,000, 40/60) | **13%** | **22%** | **66%** | **0.3%** | **+2.1** | **+0.47** |
| Part A 5,000, 50/50 split | 13% | 21% | 63% | 0.4% | +2.1 | +0.44 |
| Part A 4,000, 50/50 (v2 maximum) | 13% | 18% | 60% | 0.4% | +2.2 | +0.41 |
| Part A 3,200, 50/50 (v2 minimum) | 14% | 16% | 55% | 0.4% | +2.2 | +0.37 |
| Disagreement 14% | 14% | 19% | 61% | 0.4% | +2.2 | +0.42 |
| Disagreement 7% | 12% | 26% | 68% | 0.3% | +2.0 | +0.52 |
| Pessimistic gain (median +0.3) | 8% | 14% | 65% | 0.3% | +1.8 | +0.26 |
| Optimistic gain (median +1.8) | 22% | 33% | 66% | 0.4% | +2.5 | +0.82 |
| Dev neutral (mean 0.0) | 11% | 19% | 56% | 0.3% | +2.1 | +0.40 |
| Dev effect linked to sealed gain (rho 0.4) | 15% | 24% | 73% | 0.3% | +2.1 | +0.52 |
| PREREG 3.3 dev rules unchanged | 9% | 14% | 42% | 0.3% | +2.0 | +0.29 |
| P1 one-sided 95% instead of two-sided | 13% | 26% | 67% | 0.7% | +2.0 | +0.51 |
| v2's P1 (>= +0.5, LB > -1) | 13% | 38% | 69% | 4.6% | +1.6 | +0.60 |

Plain reading:
- **Blocking regressions:** a finalist with no true sealed gain ships about 0.3% of the time under the prior (about 2%
  at exactly 0, 0% at -1); dev, security, calibration and option-order harms are vetoed by D1-D6 (6.4).
- **Shipping a better model:** a finalist that is truly >= +2 pp better ships about 2 times in 3 under the prior (77%
  at exactly +2.0 and 88% at +2.5 when nothing else is harmed). The remaining losses come from the guards (true side
  harms are vetoed on purpose) and P1's noise.
- **Round 2 will probably not run** (about 13%), because round 1's true gain is most likely below +2 pp. Plan for
  round 1 as the main shot.
- v2's looser P1 shipped more (38%) but shipped a no-gain model 4.6% of the time and could not support a "better"
  claim; v3 trades a little expected gain for a ship decision that is always claimable.

### 10.3 Against Jev

**Where we start.**
- OHS-1 / OHS-2 (A12, 3 Oct; now practice sets): C1 80.4 vs Jev 81.7, **-1.2 [-2.9, +0.4]**; C1 81.0 vs 81.5,
  **-0.6 [-2.2, +1.1]**; about **-1.0 pooled** (ties). Jev's yes/no Brier is better: OHS-1 0.114 vs 0.140, OHS-2
  0.038 vs 0.057 (the registered `score_ohs.py` endpoint: yes/no **base** rows only, 527 on OHS-1; Jev = mean of its
  two runs). On all 2,972 OHS-1 yes/no rows, variant layer included (`_neg`, `_dneg`, `_para`, `_yn`), the same
  preds give 0.133 vs 0.152. Reconciled 3 Oct on CPU from `data/ohs.jsonl` and `preds_ohs/`
  (`q35_4b_main500k_b100_a5`, `jev_guard`, `jev_r2_guard`) only (addendum C6); no OHS-3 file was read. Cite the
  registered pair unless the row set is named.
- ejs-5 (now in-domain): **-4.4 pp** (C1 54.1 vs Jev 58.5; paired 95% CI -7.8 to -0.9). Late rows: tie (46.3 vs 45.9).
- Knowledge-heavy tests (MMLU-Pro, GPQA, HLE): far behind (MMLU-Pro Jev 82.7; best open 4B about 51.6). A LoRA cannot
  add that knowledge. C will not change this.

**After C (the shipped model if C ships, else C1), by the starting OHS-like gap:**

| Target | Start gap | Median observed gap after C | P(obs >= Jev - 1) | P(obs >= Jev) | P(obs >= Jev + 1) |
|---|---|---|---|---|---|
| OHS-like (e.g. OHS-3), base | **-1.0 (A12 pooled)** | **-0.8** | **56%** | **31%** | **14%** |
| OHS-like | -1.2 (OHS-1) | -1.0 | 51% | 27% | 11% |
| OHS-like | -0.6 (OHS-2) | -0.4 | 66% | 41% | 19% |
| OHS-like | -2.2 (older 4Bs) | -2.0 | 27% | 11% | 4% |
| ejs-5 (in-domain) | -4.4 | -4.4 (C1 stays in most runs) | n/a | about 2% | about 1% |

- Without C (C1 as is), the base row's P(obs >= Jev) would be about 24%; C adds about 7 points, all of it from the 22%
  of runs where C ships.
- ejs-5: P(within 2 pp of Jev) is about 7%. If C ships, its expected ejs-5 score is about 55 (80%: about 52-58).
- If C is truly worse than C1, the gate keeps C1, so the downside is money (about $37 expected, $100 at most), not a
  worse model.
- **Plain answer.** C is a careful, low-risk step, not a jump. Expect about +0.5 pp of shipped unseen-domain gain on
  average (+2 pp in the runs where it ships). Matching Jev on OHS-like domains is about a 1-in-3 chance; within 1 pp
  is a little better than even. The earlier projection (tie-or-better on OHS-3 about 60%) is not supported after A12.
  Closing the ejs-5 gap is unlikely with this plan.

**What moves these odds most, and when we learn it.**
1. Round 1's sealed select-set result (and its realized SE): near 0 means breadth is not transferring to real text;
   re-plan before spending more.
2. Sealed part B1 and the held-out commit repos show whether the commit family transfers, before the single ejs-5 read.
3. The hard-negation probe (report) shows whether the negation work helps at all.
4. The single sealed Jev read (`C_DATA_SPEC.md` decision 10; at the C look, after the ship verdict; report-only) shows the real gap on
   new domains before OHS-3.

---

## 11. Order of work and GO points

1. Owner: confirm this plan and the decisions in `C_DATA_SPEC.md` 12; commit the PREREG amendment (C plan, data rules,
   gate rules and thresholds, sealed sizes and the 40/60 split, one candidate per round, look table, anchor and
   protected-skill list, stop rules, budget rule, stored REF; v4: the A4 ordinal term with its fallback, the 6.0
   readout and temperature pipeline, FAM-1 as report-only, the 7.3 weight rule, the ejs-5 report form and B5
   expectation (spec 4.4), the B3 yes-share alarm on dev and sealed looks (spec 9, report-only), the equal commit
   shares (spec 4.2), the one-time D2 decision (spec 0.2, section 9 row 34)) before any C training row or candidate
   exists.
2. Sealed suite and its scorer built by the separate sealed agent (no access to C data). The scorer (aggregates only,
   look log, second-confirm refusal; prints gold-free mean P(yes) and yes share per set and domain on yes/no items from
   the 6.0 served output, spec 9, B3) is tested on CPU on dummy predictions, then both are frozen; the orchestrator
   records the sealed scorer's sha256 in amendment A15, alongside the suite sha256, and commits it (6.2). If the
   frozen scorer lacks B3 printing, B3 is dev only. **No C training row is generated before this commit.** $0.
3. `gate_c.py` written and tested on CPU (it checks the scorer sha256 against A15). $0.
4. C data round 1 built and QC'd (G0-G16). $0 GPU.
5. Scoring crowd pass on the free L4 (`C_DATA_SPEC.md` decision 3; no Modal spend, so no GO point).
6. Selection, mixing (anchor targets, protected-skill flags, ordinal row count), pre-flight checks (incl. token cap,
   memory, the F2 rendered-prompt sha assert and the A4 unit test and finite check; A4 fallback decided here), FAM-1
   step-0 read on the L4 (report-only; its wall time decides whether the 25/50/75% reads run), smoke (about
   $0.20-0.50). **GO** for round 1 (about $27-29; hard stop at $35 projected).
7. Monitors at 25/50/75%; look S1 of round 1's candidate plus its dev, `_perm`, jagged and OPI reads; round-1 go /
   no-go (6.3); realized select SE logged and confirm power re-stated.
8. Only if 6.3 passes: round-2 data (new cards) built and QC'd; bounded weight update; at most one loss-weight halving
   (7.3, by amendment); budget trim. **GO** for round 2
   (about $55-57, trimmed to the cap). Look S2; finalist chosen.
9. Owner declares C finished; the one confirm look (6.4). After the ship verdict is logged: the single Jev read on the
   sealed suite (`C_DATA_SPEC.md` decision 10; **GO** for its API spend; report only).
10. If SHIP: ejs-5 once (in-domain), OHS-1/2 practice report, JevBench report, then **GO** for OHS-3 once.
