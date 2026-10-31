# C2.1 PLAN v3.3 AMENDMENT: what C2 taught, and what changes (Sun 18 Oct 2026, about 9 PM ET; Opus designer)

Amends C2_1_PLAN_v3.md (v3.2-r, sha256 60b427ef...) and C2_1_BUILD_ORDER.md (99fb177a...) after C2_REPORT.md (0286b4cd...). TRAINING SIDE ONLY
(like plan section 16): sealed-side agents never read it. Every item ADDS or TIGHTENS a check. No v3.2 or PREREG bar is loosened, and where this file
and v3.2 differ, the stricter line binds. Every new number goes into a PREREG record before any C2.1 row exists (rows start Sun 25 Oct).
Tags: measured (file:line), DERIVED (my arithmetic), UNVERIFIED. Paths are under opendecide-data/lean/ unless they start with HANDOFF.md.
Read: the plan (sections 0-2, the section 3 PRE-REGISTERED RULES block, sections 4-16), the build order, C2_REPORT.md, HANDOFF.md:1-260 + 554-558 +
1488-1490, teach1/C2_DATA_SPEC.md (family rows, G6), PREREG_FINAL.md (grep "A50" only), the C2 adapter_config/train_meta, and the four
research_v5_c2lessons files. Not opened: any ohs, sealed, quarantine, longbench, jevbench or ejs path, any Jev output, or ~/.claude.

## 1. What C2 taught (numbers)

| # | Lesson | Numbers | Source |
|---|---|---|---|
| 1 | Dev gain did not become independent gain | Trained-family mixdev +12.31 [+10.47, +14.15] (n 2,795) vs OHS-4 part R +1.93 [+0.07, +3.82] (n 1,454). Only 16% of the gain reached independent items (DERIVED d = 0.16), closing 22% of Jev's 8.6-pt R lead | C2_REPORT.md:19,42,120,198 |
| 2 | Transfer harm: one family, every candidate | Pooled -4.83 [-8.59, -1.02] (n 600); T19 -11.3 [-17.2, -5.6]; T21 +1.7. All 18 candidates were negative (best -1.33, highest UB +1.65) | C2_REPORT.md:121,169-172 |
| 3 | C1's over-abstention got worse | T19 verdicts answered "Cannot be determined": 54 (C1) -> 64 (alpha 0.5) -> 76 (alpha 1.0), vs 26 gold. Compliant recall 30.8% -> 7.7%. Precision of those answers 34.2% at 84.4% mean confidence | c2_dev_diagnostics.md:32-33; calibration.md:89 |
| 4 | ...but that is only a third of the T19 loss | Of 34 rows lost: 11 verdict, 9 gap-choice (no abstain option), 14 yes/no. The yes-rate did not move (49.0% truth vs 52.4%), so most of the loss is in applying the rules | c2_dev_diagnostics.md:34,140-145 |
| 5 | The cause is cues, not label rates | IND gold is 27.2% of the rows that offer an IND option (T19 truth 26.5%) and 2.03% of all rows. T29/T25/T28/T30 hold 70% of the abstain gold. On trained families C2 abstains at the true rate (42.4% vs 42.0%) | c2_dev_diagnostics.md:31,38-39,491 |
| 6 | Blending is a single trade-off line | Alpha 0.5 keeps 78% of the gain and 28% of the loss. Going from alpha 0.7 to 1.0 buys +0.25 pp in-family for -1.83 pp transfer. Last-3 equals the final (S +0.00 [-0.24, +0.23]). S rose with alpha while transfer fell | transfer_levers.md:64-75; C2_REPORT.md:109,139-158 |
| 7 | The forgetting monitor was blind | It read only the KD-anchored replay slice (C1 92.15%): -1.80 / -1.15 / -0.50 at 25 / 50 / 75%, and never fired. The damage was likely present by about step 1,212 (UNVERIFIED until E2) | C2_REPORT.md:93-101; transfer_levers.md:15,61 |
| 8 | Calibration broke out of distribution, and the T rule made it worse | OHS-4 yes/no ECE 4.1% -> 13.2%; Brier +0.0098 (bar +0.005). Dev ECE: general 2.78 -> 5.46 (confidence +3.3 pp at accuracy -0.48 pp), transfer 13.34 -> 21.20, in-family 9.23 -> 6.27. Frozen T was 0.8, the clip floor (median over 138 small groups); the pooled optimum is 1.10 on the same rows and 1.75 on transfer. On dev transfer this T turned a +4.8-pt gap into +12.2 pts | C2_REPORT.md:22,27,31; calibration.md:39-45,51-62,76-85 |
| 9 | One pass, at a known price | 0.9901 epoch, 3,673 steps, 186 min, $13.14 = $0.221 per 1K row-passes = $3.58 per 1K steps. Plan v3.2's "Epochs: 2" would cost about $50 at 112.5K rows | C2_REPORT.md:74-76; C2_1_PLAN_v3.md:919,969 |
| 10 | Process | The 600-row, 2-family transfer set was never named in PREREG (T20 and T36 were dropped after G6). Check (b) was waived after the result (A100) | C2_REPORT.md:7,169,218 |

## 2. Changes (evidence, cost = Modal $ / Claude work, time, bar served)

The bars served are: E-T1, E-T2, E-AB and E-C (new eligibility, 2.3); STOP (2.2); the ECE ship gate (plan :789); the calibration claim (plan :790-794);
the G ship rule (plan :779); and the C-transfer headline (plan :773).

### 2.1 Data

**D-1 Commit-vs-abstain twins, in every C2.1 family.** Any row whose gold is an abstain answer gets a decidable twin, built by program:
- *Which rows:* gold of IND-type ("cannot be determined", unknown, not shown) or ASK-type (ask the user; the ASK in ALLOW/ASK/BLOCK; the ASK in T59).
- *The twin:* same scaffold, same options, same uncertainty-looking cue (a missing, expired or unstated record), but with one fact toggled so the
  gold becomes a commit answer. Twins substitute inside each family's size (within its G0-lite class-share bars) via the stamp wrapper. This extends the ladder-twin rule
  already being coded (plan :407-413).
- *Pre-freeze kill gates (CPU; plan :427 bars):* 100% twin coverage. A cue-only probe scores held-out AUC <= 0.55 (UB <= 0.60). IND gold is <= 33%
  of the IND-offering rows per family and <= 5% of all new rows (C2: 0.81%). ASK shares follow each G0-lite and are reported.
- *Evidence:* lesson 5. Bianchi: 2.5-5% refusal rows helped, but 9% gave over 50% exaggerated refusals (calibration.md:133). R-Tuning: refusal
  transfers. The effect size for a one-token readout is UNVERIFIED.
- *Cost and time:* $0; about +0.5 Sonnet-day per lane, inside the addenda campaign (540 items, 134 done; HANDOFF.md:147-151). Due Sat 24, 2:00 PM ET.
- *Bars:* E-AB, E-T1, E-T2, C-transfer, the ECE gate.

**D-2 Twins for the C2-mix replay.**
- *Why:* at C1 init (the O5 default), the 57K replay ceiling is nearly all of C2's mix. That includes its 23,736 family rows and their 1,203
  IND/ASK-gold rows, the rows that taught the T19 drift.
- *Fix:* build about 1,200 decidable twins of the abstain-gold rows of T25, T28, T29, T30 and F6, from their own generators (new seeds, stamped at
  creation). Each twin replaces a commit-gold replay row of the same family, so the count is unchanged.
- *Left as is:* the 195 dataset-native "unknown" golds (boardgameqa, logic, bAbI). Manifest v1.1/v1.2 must allow these family ids.
- *Cost and time:* $0; about 1 Sonnet-day, Sun 25-Mon 26.
- *Bars:* E-AB, E-T1.

**D-3 Block R (plan 16.3; about 24,600 public human-labelled TRAIN-split rows from 60-70 sources)** is kept. It is the main lever for G and for
breadth: in Super-NI, held-out score is log-linear in the number of tasks (it saturates at 64 instances per task), and in Flan, dropping mixture
balancing cost -11.1 / -15.0 on BBH (transfer_levers.md:167-175).
- *Added:* (a) each source's abstain-like gold share (SQuAD 2.0, AmbigQA, CondaQA, FEVER / VitaminC NEI) is measured before mixing; above 33%, a
  seeded program drops that source's abstain rows down to 33%. (b) No family or source may exceed 8% of non-replay rows.
- *Cost:* $0. *Bars:* G ship rule, E-T1.

**D-4 Calibration-aware data:** (a) the A29/PR-5 buffer, 200 rows per question type and option-count bucket, never trained and outside the T pool;
(b) the A24 held-out sub-families double as a calibration domain; (c) the D-1 twins aim at the confidently-wrong rows (C2's false "Cannot be
determined" answers averaged 0.817 confidence; c2_dev_diagnostics.md:35). Cost $0. Bars: ECE gate, calibration claim.

### 2.2 Evaluation: transfer dev v2 and early warning

**E-1 Transfer dev v2**, built before training. Its files and shas go into PREREG by Fri 23 Oct, 8:00 AM ET (12:00 UTC).

| Set | Families (rows) | Used for | Never used for |
|---|---|---|---|
| MONITOR | T33 600 (claims vs tool logs; has "Not shown in the log"); T12 600 (three-way match with ordered exceptions). Neither was trained in C2 (C2_REPORT.md:84) | E-2 stop rule, E-3 T pool, T-5 base E, the 2.5 pilot | gate, selection |
| GATE | T19 300 + T21 300 (the frozen C2 file, sha 2b9702a7..., comparable with C2); T24 300 (revision materiality); T36r 300 (npm / PEP 440 ranges, coding-shaped); a fifth family, T07r or T20r, 300. Designed as held-out (C2_DATA_SPEC.md:138-141,1311-1313) | E-T1, E-T2 and E-AB, at the grid and the final only | states, the T fit, the pilot, any earlier read |

- *Build:* from the existing C2 generators, with new seeds and dev-only wordings, through the stamp wrapper.
- *G6:* each family must pass G6 at its eval size (partial-input baselines <= chance + 2 pp; C2_DATA_SPEC.md:890). A family that fails is replaced by
  the next of T36r, T07r (after its A72 gold-bug fix) and T20r.
- *Floor:* 4 gate families and 1,200 rows by Fri 23. Below the floor there is no C2.1 training, and the owner is told that day.
- *Isolation:* these families are G13 targets in the Thu 22 registry, and the row-start guard refuses their ids.
- *Baselines:* C1 and C2 are read on the free L4 (11 rows/s; HANDOFF.md:1489).
- *Paired SE (DERIVED; transfer_levers.md:237):* about 2.96 pp per 300-row family, 1.36 pp pooled at 1,200 rows, 1.22 pp at 1,500.
- *Cost:* $0 Modal; about 1.5 Sonnet-days. *Bars:* E-T1, E-T2, E-AB, STOP.

**E-2 Early warning.** This becomes the only stop rule, replacing plan :1055 (the old-slice rule stays as trigger G).
- *When:* at the saved states at 8.3% (about step 590 of 7,031), 25% and 50% of the run. The 75% read is report-only.
- *What is read:* MONITOR (1,200 rows), a 500-row in-family slice, and the old slice / G-proxy, each paired against init (C1) on raw probabilities.

| Trigger | 8.3% and 25% | 50% |
|---|---|---|
| P: pooled MONITOR accuracy | point <= -5.0 pp and one-sided 95% UB < 0 | point <= -3.0 pp and UB < 0 |
| F: either MONITOR family (n 600) | point <= -9.0 pp and UB < -1.0 | point <= -7.0 pp and UB < -1.0 |
| B: predicted IND/ASK share where offered, minus init (needs no labels) | >= +20 pp | >= +15 pp |
| C: MONITOR top-label ECE (10 equal-mass bins), minus init | >= +6.0 pt | >= +4.0 pt |
| G: old slice or G-proxy below init - 1.5 pp | plan rule | plan rule |

- *Decision:* at 8.3% and 25%, STOP if any of P, F, B or C fires. At 50%, STOP if two fire, or if one fires at its 25% bar.
- *Error rates (DERIVED, normal approximation, C2 snapshot pessimism -1.3 / -0.65 pp, n 300 so conservative at 600; transfer_levers.md:253-258):* P false
  alarm 0.3% / 4.3% (25% / 50%), power 79% / 96% for a C2-like -4.8 pp; F 0.5% / 1.6% per family, power 89% / 95% for -11.3 pp. On C2's final numbers,
  F, B and C fire at both bars and P at 50% (transfer_levers.md:264; calibration.md:45). The 8.3% read is kept only if E2 shows damage by step 918.
- *Lag and cost:* $0 (free L4); each read takes 15-30 min (UNVERIFIED), about 300-600 steps; a stop near 31% saves about $17 of a $25 pass. On STOP:
  halt, keep the states, no candidate; diagnose with per-family abstain and cue tables; a relaunch needs a pre-registered drop-only fix and an owner GO. *Bars:* STOP (guards the money behind every bar).

**E-3 Temperature protocol.** This replaces plan :1027-1028 ("fit on mixdev, [0.8, 1.3]") and the L1 median-of-groups rule.
- *What is fitted:* one T per question type. For choice, one per option-count bucket, but only for buckets with >= 300 pool rows.
- *Pool:* MONITOR, D2 unseen-source dev (3,847), devzs, dev_nc, the A24 sub-families, and mixdev (capped at 1/3 of the weight).
- *Fit:* domain-balanced NLL over a 0.25-10.00 grid (step 0.05), bounded to [1.00, 2.00]. A clip audit sends any type that sits at a bound, or a
  per-domain spread above 2x, to Opus.
- *Never fitted on:* GATE, sealed sets, a single family, or medians of sub-100-row groups.
- *Reported:* ECE at T = 1, at the shipped T and at a 5-fold cross-fitted T, plus Brier, NLL, AURC and E-AURC.
- *Evidence:* a leave-one-domain-out T cut C2's mean-domain ECE from 10.64 to 8.09 (C1: 6.20; calibration.md:64-74). Out-of-distribution T is
  about twice the in-distribution value (Desai and Durrett), and temperature scaling fails under shift (Ovadia; Tomani).
- *What stays fixed:* this is a method fix made before any C2.1 result. The 3.5% gate and the <= 3.0% claim rule do not change.
- *Cost and effect:* $0. Measured -1.4 to -2.5 pt on C2 dev. It cannot fix a T19-type collapse (T19 alone needs T of about 3.25). *Bars:* ECE gate, claim, Brier.

**E-4 Free checks before the bars freeze (Mon 19-Thu 22):** E1 abstain-cue audit (CPU); E2 read C2 states s000918 / s001212 / s001836 and the final
on the 600-row transfer dev (L4, about 1 h: when did the damage start?); E3 read C1 and C2 on MONITOR and GATE (may move E-2 bars before the freeze only
to keep false alarms <= 5% per read); E4 (optional, sealed-scope session only) re-score the L1 OHS-4 predictions at T = 1 and the E-3 T, post-hoc and
report-only, no verdict changes (calibration.md:85).

### 2.3 Selection eligibility (new pass/fail filters, never weights; S stays as v3.2)

A candidate is eligible only if the existing pre-gate passes AND all four filters below pass.

| Filter | Rule | How C2 did |
|---|---|---|
| E-T1 | Pooled GATE (n >= 1,200): one-sided 95% LB of C2.1 - C1 > -3.0 pp (at SE 1.36, a point above about -0.8; DERIVED) | All 18 candidates fail (best -1.33) |
| E-T2 | No GATE family with a point <= -7.0 pp and a paired 95% UB < 0 (false fail at a true 0: about 0.9% per family; DERIVED) | T19 fails at alpha 1.0 (-11.3) and alpha 0.5 (-7.0 [-11.6, -2.3]) |
| E-AB | On each GATE family with an IND option: predicted/gold IND <= C1's ratio (target <= 1.5, report-only) | T19: C1 2.08; C2 2.92 and alpha 0.5 2.46 fail |
| E-C | On the calibration pool with a leave-one-domain-out T: mean-domain ECE <= C1 + 1.0 pt; confidence rise <= accuracy change + 1.0 pt; AURC <= C1 + 0.4 (calibration.md:164-170) | Fails all three: +1.9; +3.3 vs -0.5; +0.69 |

**Relation to C2's check (b)** (+3.0 pp, LB > 0). That was a C2 rule (C2 spec 7.2); v3.2 has no C2.1 transfer pre-gate, so E-T1 and E-T2 are
new. If the conformance map (plan 16.1 step 0) finds binding C2.1 text that carries (b), then (b) binds as well. "GATE >= +3.0 with LB > 0" is
printed as "positive transfer shown". If no candidate is eligible, there is no OHS-5 look and the report says so. No waiver path is built.

### 2.4 Training recipe

**T-1 One pass:** epochs = 1.00 (replaces plan :919). Forgetting grows with steps (Kalajdzievski; Biderman), and NLL keeps raising confidence
after accuracy saturates (Guo; Chen). Cost (DERIVED at $0.221 per 1K row-passes): $24.9 for 112.5K rows (7,031 steps, about 5.9 h at 3.04 s/step);
$27.7 for the 125K C1-init cap (6.6 h). Two passes would cost about $50-55, which R1 does not allow. The Mon 26 measured projection binds
(plan :972-977). Bars: money, ECE.

**T-2 Optimiser held:** lr 5e-5 cosine, batch 16, r16 / alpha 32 / dropout 0.05, continuing the init adapter. Continuing beat a fresh LoRA,
80.4 vs 65.7 (transfer_levers.md:146). There are no rank or variant arms. The target set is C2's ACTUAL set: MLP in 32 layers, GDN
in_proj_*/out_proj in 24, and q/k/v/o in 8 (adapter_config.json regex, checked; GDN is 34.6% of the parameters). This corrects plan :922, and the
A19 audit asserts it.

**T-3 Replay:** the count is unchanged (38K at C2 init, 57K at C1 init; a ceiling), with KD 0.5 on replay and the content per D-2. Evidence: 1-25%
replay sits on the flat part of the forgetting curve (Ibrahim: 3.56 / 2.83 / 2.33). C2's 60% replay held the old slice within -1.8 pp but cannot
protect a family it does not contain. No study ties the replay ratio to ECE (calibration.md:138). Bars: G floor, G ship rule.

**T-4 States:** save 12 LoRA states, one every 1/12 of the run, each exported to the L4 queue during the run.

**T-5 Grid** (still 18 points, in the grid sha before any look): the 12 alpha/gamma points on the final state F and the 4 soups stay; the 2 last-K
points (A22) are dropped (C2: last-3 gave S +0.00 [-0.24, +0.23], ECE -0.2) for base E at alpha 0.8 and 1.0, where E = the state at >= 50% of the run
with the lowest MONITOR NLL, picked by program (OOD often peaks early; arXiv 2509.12235, abstract only, UNVERIFIED).

**T-6 Selection:** the 2.3 filters run first, then the highest S wins; T is frozen per E-3.

**T-7 R12 stage B:** unchanged, and still the first item shed.

### 2.5 Optional stage A: pilot fine-tune (owner money: O1)

- *Design:* 10,000 rows drawn by the full-mix rules from rows that exist by Tue 27 Oct (family pilots, first block-R sets, cleaned replay). Arm A0 =
  the pre-registered recipe; arm A1 = A0 plus KD 0.5 to C1 on NEW rows too (RL's Razor: KL to the base on the new task predicts forgetting, R^2 0.71;
  transfer_levers.md:152,210). Same seed, one pass, same trainer build. Reads (free L4): MONITOR, calibration pool, pilot-family dev; never the GATE;
  arms are never candidates.
- *Pre-registered uses:* (1) if A0 fires any 25%-level E-2 trigger, one drop-only fix of the driver block(s) before the freeze; (2) A1 replaces A0
  only if its MONITOR gain is >= +1.5 pp, pilot-family dev >= -1.0 pp, and pool ECE no more than 0.5 pt worse; (3) measured s/step and $ per row-pass
  replace the projection; (4) trainer and state-export bugs (A85/A86-type in C2) surface before the paid run.
- *Cost, time, limits:* about $4.4 (DERIVED, +/-2x for row length); hard stop $4.75 so the 1.25x rule fits mahadikarya2's $5.97 October leftover
  (HANDOFF.md:558; live check first). About 1 h of H100 plus 1 h of L4: Wed 28 on the EARLY path, decided Thu 29 8:00 AM ET; without October money,
  Sun 1 Nov (+1 day). At about 625 steps it sees only early damage; the power of use (2) is UNVERIFIED.

### 2.6 Optional stage B: RL with verifiable rewards after SFT (owner money: O2)

- *Evidence for:* in chain-of-thought studies RL beat SFT out of distribution (V-IRL +11.0 vs -79.5; Qwen3-4B decisions +1.4 to +3.0 pp).
- *Evidence against:* the driver was on-policy data with a small KL shift, not RL as such (on-policy SFT +30.2 vs off-policy -40.5); no study covers
  no-CoT one-token decisions; GRPO's ECE was above SFT's in 12 of 12 cells (13.3 vs 6.3); a 0.05 refusal reward gave 99.9% refusals; and RL neither beats the
  early SFT OOD peak nor fixes a label prior the data taught (rl_vs_sft.md:13,18,40-69,84).
- *Recipe if bought (exact expectation, no rollouts):* from the GO #2 S-winner, a new r16 LoRA on 10-20K balanced TRAIN prompts with p(gold) in
  [0.05, 0.95]; loss -E[reward] + Brier + beta x KL (to C1 on replay rows); no abstain reward on determinate rows; lr 1e-5 to 2e-5, one pass. A
  shuffled-gold control arm is mandatory (random rewards gave 74% of the real gain on Qwen2.5-Math). Enters as 2 pre-registered grid points; adopted only
  if it passes 2.3 and beats the control by >= 1.0 pp on MONITOR.
- *Cost:* $4.4-6.6, cap $10; +1 day after GO #2. Sampled TRL GRPO is not recommended: about $18-53 (DERIVED), and the stack is untested on Qwen3.5
  (rl_vs_sft.md:142-166).
- *Expected (DERIVED):* transfer 0 to +2 pp, ECE within +/-0.5 pt; it does not fix a T19-type collapse (rl_vs_sft.md:202-210).

### 2.7 Plan text to correct in v3.3 (no bar moves)

:919 -> 1.00 epoch; :969 -> "per pass"; :922 -> C2's actual targets; :1027-1028 -> E-3; :1055 -> E-2. Section 16.7 "grid reads (18 candidates,
od-l4b)" cannot run in a day: the L4 pace was about 1.7 h per model (HANDOFF.md:556), 32-34 h in all, while the H100 read 19 models in 98 min for $7.49
(C2_REPORT.md:106) -> O3. R14 as written gives init = C1, because C2 failed S3 and S4, not only S1 (C2_REPORT.md:200) -> O5.

## 3. Projections vs Jev (DERIVED ranges; no probabilities claimed)

| Dimension (owner target) | Measured anchor | C2.1 range | Depends on |
|---|---|---|---|
| Coding/agent (+15 to +20) | OHS-4 R: Jev 76.00, C1 67.40, C2 69.33 (C2_REPORT.md:42); d = 0.16 | C-total (home field), C2.1 - Jev: about -6 to +13, centre about +2. C-transfer (the headline needs >= +5 with LB > 0): about -8 to +6, centre about 0. Formula: (C1 - Jev) + d x G_dev, with C1 - Jev from -8.6 to -2 (UNVERIFIED for coding), d 0.16-0.5, G_dev +15 to +30 (C2's families: +6.7 to +28.0) | Whether d rises above 0.16 (twins, ladder, block R), first visible in MONITOR at the pilot and at 8.3% / 25%. Jev's level on coding gates is unknown until R9. The +15-20 target is above the top of the range |
| Dev transfer GATE (E-T1) | C2 -4.83; alpha 0.5 -1.33 | about -4 to +3 pp; E-T1 needs a point above about -0.8 | Twins fix at most a third of a T19-type loss, so there is a real risk that no candidate is eligible |
| General (within 2-4; ship <= 4.0) | OHS-4 G: Jev 79.95 vs C1 = C2 77.84 (gap 2.12 [0.66, 3.57]); text side-bench 79.3 vs 77.6 | Jev - C2.1: about 1 to 5 pp, centre about 3 | Block R's gain at 4B (first read: the public-G panel before GO #1), the -1.0 G floor, and the mix of OHS-5 G sources |
| Security (beat Jev) | OHS-4 X accuracy: Jev 73.84, C1 69.40, C2 68.51. Attack success: C1 1.04%, C2 0.52% | Attack success <= max(C2 + 2, 3%): likely. X accuracy vs Jev: about -5 to +4. C-PERM and C-SEC are home field | T41c / T50 / T53 and A6 / A12 / A13. Jev's attack success on our K/X has not been read |
| Calibration (beat Jev) | Jev 1.13 aligned ECE 3.2-3.3% (arXiv 2610.00346). OHS-4 yes/no ECE: C1 4.1%, C2 13.2% | Pooled G about 2.5-5%, pooled C about 3-8%. The 3.5% gate is plausible on G and uncertain on C. A claimed win (<= 3.0% with a paired win) is unlikely | E-3, D-1, E-C. C1 is 2.78 on general and 6.9 on transfer even at the oracle T |
| Speed (beat Jev) | C1 p50 14.1 ms per decision (H100, batch 1; git 01d67c5). Jev end-to-end 156 ms by our client | Server p50 12-35 ms (C2 D9 30.9 vs C1 31.6 ms). End to end: a likely win if hosted near users | The SPEED-3 / L-D suite, which never ran for C2 (C2_REPORT.md:176) |
| Cost (beat Jev) | Jev $0.042 per M input. C1 is cheaper only above about 59% utilisation (plan :1083) | A win only at a stated utilisation, or with the A35 L4 host | L-D measurements |

**Plain message.** Plausible wins over Jev are speed, the per-call permission and secret gates (home field), and attack success. Staying within
4 pp of Jev on general text sits near the middle of the range. A +15 to +20 lead on coding/agent decisions, and a calibration win, are not supported
by any measurement. The first real evidence will come from the pilot (O1) and the 8.3% and 25% MONITOR reads.

## 4. Timeline (ET; UTC in brackets for fixed plan times)

| When | Item | Modal $ |
|---|---|---|
| Sun 18 - Mon 19 | This amendment, then a fresh Opus skeptic, then merge into v3.3. One owner message with O1-O5 | 0 |
| Mon 19 after 11:00 AM (15:00 UTC reset) | E1 and E2 (L4, about 1 h). The transfer-dev builder starts (Sonnet high, within the measured usage projection) | 0 |
| Tue 20 - Thu 22 | MONITOR and GATE built (G6, stamps) and added to the Thu 22 G13 registry. E3 reads (L4, about 30 min) | 0 |
| Tue 20 - Sat 24, 2:00 PM | D-1 rule and probe added to every G0 addendum. The stop reader, T fitter, eligibility code, state export and KD flag each get CPU tests, a fresh Sonnet skeptic and a conformance record | 0 |
| Fri 23, 8:00 AM (12:00 UTC) | PREREG v3.3: transfer-dev shas, E-2 bars, 2.3 filters, E-3, T-1, T-5 | 0 |
| Sun 25 - Mon 26 | Rows start, with twins at creation. D-2 replay twins. The measured cost projection sets the shed level | 0 |
| Tue 27 - Wed 28 | O1 pilot: mix built Tue; 2 H100 arms Wed (about 1 h); L4 reads (about 1 h) | about 4.4 |
| Thu 29, 8:00 AM (12:00 UTC) | Pilot decisions; EARLY or FALLBACK declared | 0 |
| EARLY | Freeze Fri 30, 8:00 AM. Train Sun 1 Nov (5.9-6.6 h; stop reads at 8.3 / 25 / 50%). Grid Mon 2 (H100 1.7 h with O3; about 33 h on L4 without). GO #2 Tue 3. R9 Wed 4 (Thu 5 with O2). Report about Fri 6 - Sat 7 | training + O3 |
| FALLBACK | Freeze Mon 2 Nov, 6:59 PM EST (23:59 UTC). Train Wed 4, grid Thu 5, GO #2 Fri 6, R9 Sat 7, report Mon 9. An L4 grid adds about 1.5 days; O2 adds 1 day. Latest about Wed 11 - Sat 14 | same |

The critical path is still the addenda campaign: 250 of 540 items were missing at 19:35 UTC (HANDOFF.md:147-151). This amendment adds about 4-5
Sonnet-days, launched only within the measured usage projection (build order, global item 4).

## 5. Owner decisions (money and scope only; one message on Mon 19)

| # | Decision | Default (recommended) | Money | Needed by |
|---|---|---|---|---|
| O1 | Stage A pilot fine-tune (2.5) | YES: 2 arms x 10K rows, hard stop $4.75, on mahadikarya2's October leftover (one account, no relay, live check first) | about $4.4 | Tue 27 Oct |
| O2 | Stage B RL-like stage (2.6) | NO in C2.1; a C2.2 candidate. Expected +0 to +2 pp, with calibration and abstention risk, +1 day | $4.4-6.6, cap $10 | Thu 29 Oct |
| O3 | Grid and calibration reads in one H100 session instead of the free L4 | YES, cap $10 (C2: $7.49 for 19 models). Payer named by the owner (A88 precedent: mahadikarya3) | about $8-9 | GO #1 |
| O4 | Main-run cap: keep A82 9 (training <= $30; one account at 1.25x, about $24 at a $30 renewal), or allow up to +$8 so that the full C1-init mix (125K rows, $27.7) plus stage B ($4.1) fits | KEEP A82 9; shed only on the measured Mon 26 projection | 0 or +$8 | Sun 1 Nov |
| O5 | R14 init branch | C1, as the rule reads (C2 failed S3 and S4, not only S1). This sets the 57K replay count | 0 | Mon 19 |

Money under the defaults: the main run (<= $30) plus O1 (about $4.4) plus O3 (about $8.5) is about $43 on Modal, about $8 over R1's $35 total
(up to about $14 at the hard caps), which the owner's optional $10-15 would cover. The card is never used. Every other item in this file costs $0 of Modal.

## 6. Sources

Project: C2_REPORT.md:7,19-31,42-46,74-76,84-101,106,109,120-129,139-172,176,198-201,213,218; C2_1_PLAN_v3.md:407-413,427,773-794,913-977,
1024-1055,1083,1631-1639,1698-1782,1858-1920; C2_1_BUILD_ORDER.md:30-96,329-358; HANDOFF.md:137-151,554-558,1488-1490; teach1/C2_DATA_SPEC.md:109,118,
121-122,138-141,890,1310-1313; models/q35_4b_c2/adapter_config.json (r16/alpha 32/dropout 0.05; regex includes out_proj, in_proj*) and train_meta.json
(epochs 0.9901, lr 5e-5, batch 16, KD 0.5); research_v5_c2lessons/{transfer_levers,calibration,rl_vs_sft,c2_dev_diagnostics}.md.
External (arXiv, as fetched in those files on 18 Oct 2026): 2401.05605, 2405.09673, 2403.08763, 2509.04259, 2512.23017, 2204.07705, 2301.13688,
2309.07875, 2311.09677, 1706.04599, 2211.00151, 2003.07892, 1906.02530, 2012.10988, 2610.00346, 2501.17161, 2507.00432, 2601.13284, 2507.16806,
2607.10738, 2506.10947, 2509.12235 (abstract only, UNVERIFIED).
