# C2.1 research v5, angle "C2 lessons: levers against negative transfer and forgetting" (Sun 18 Oct 2026, about 5:50 PM ET)

Question: which levers reduce negative transfer and forgetting in LoRA fine-tunes of a small model (replay ratio, learning rate, steps and epochs, rank and targets, weight averaging and merging, multi-task balancing, data diversity, early stop on held-out-family reads), ranked by evidence, with numbers and an early-warning stop rule for the 25% and 50% snapshots.

Tags. [local] = I recomputed it from project files (no model was run, no GPU, nothing written outside this folder). [author-run] / [vendor-run] = the paper's own authors. [second-hand] = taken from an earlier research file in this tree and not re-fetched by me. DERIVED = my arithmetic from the numbers shown. UNVERIFIED = I could not confirm it from a primary text. All URLs accessed 18 Oct 2026.

Rule check. Files read: C2_REPORT.md, HANDOFF.md (grep + sections), C2_1_PLAN_v3.md (grep + sections 5), C2_1_EXTRA_LEVERS.md and research_v3/recipe.md, research_v4_levers/accuracy.md (greps), snap_monitor_c2.py (docstring), train/README.md, models/q35_4b_c2/{train_meta.json, adapter_config.json, adapter_model.safetensors header only}, c2_build/train/grid_h100/results/... preds_c2_transfer_dev/*.jsonl, data/c2_transfer_dev.jsonl, data/c2_parts/c2_train.jsonl (labels and ids only), logs/snap_monitor_c2.jsonl. Directory listings showed some file names containing "ohs"; I opened none of them, and no path containing ohs, sealed, quarantine, longbench, jevbench, ejs, c_spec/sealed_brief, c_build/preread or any Jev output file. One disclosure: the harness spilled the output of my own `cat research_v3/recipe.md` to a tool-results file under ~/.claude/projects/... and I read that spill file with the Read tool (its content is the recipe.md text I could have read from its original path); no memory, settings or other ~/.claude file was opened. A sibling file in this folder (c2_dev_diagnostics.md) was read only for a cross-check of the T19 numbers (section 2.3); they agree with mine.

---

## 1. Bottom line

1. The C2 transfer loss is family-specific, not general forgetting: T19 -11.3 pp, T21 +1.7 pp, general dev -0.48 pp (C2_REPORT.md:170 and the section-1 table). On T19 it has two parts [local, section 2.3]: abstention drift (predicted "Cannot be determined" on 54 of 98 verdict questions for C1, 64 at alpha 0.5, 76 at alpha 1.0; gold 26) and a loss on questions that have no abstain option (yes/no -9.7 pp [-17.2, -2.1]; pick-the-failing-item -15.8 pp [-28.1, -5.3]).
2. Every lever that only scales the update (alpha blend, LR, steps, last-K average) slides along one line. C2's own grid measures the exchange rate: alpha 0.5 keeps 78% of the in-family gain (+9.55 of +12.31) and 28% of the transfer loss (-1.33 of -4.83); the last 30% of the delta (alpha 0.7 to 1.0) buys +0.25 pp in-family for -1.83 pp transfer. The T19 yes/no loss is already -9.0 at alpha 0.5, so blending cannot repair it. The literature says the same (Kalajdzievski: forgetting follows an inverse linear law against fine-tuning performance and cannot be avoided by early stopping).
3. The early-warning gap is the biggest finding. C2's snapshot rule read only the old replay slice (snap_monitor_c2.py:34) and C2.1 plan v3.2 keeps the same rule (plan line 1055). That slice is anchored by KD on replay and sat at 92% accuracy, so it was blind to the T19 failure by construction. The 33% snapshot averaged with the final was no better than the final on T19 (verdict 38.8% vs 45.9%, yes/no 49.0% vs 55.2%), which says the damage was already there by about step 1,212 (inference, UNVERIFIED until the saved snapshots are read, section 6 E2). Other Qwen3.5-4B and LLM evidence agrees that damage shows in the first 100-150 steps.
4. Rank 1: put held-out-family reads into the stop rule (2 monitor families, bars in section 5). Rank 2: fix data, not hyperparameters: decidable twins for every can't-tell row, per-family commit/abstain gates, and a cap on any ASK-type share. Rank 3: breadth over depth (more families and sources, about 600-1,000 rows per family; C2's 8 families with at most 1,000 rows gained +14.9 on average, the 6 with more gained +14.7). Rank 4: one pass, not two (section 2.7 flag F3). Rank 5: KD to the init on new rows as an A/B arm.
5. Keep LR 5e-5 (no higher), r16, alpha 32, dropout 0.05. Evidence for changing rank, alpha or variants is a null result (LoRA variants land within 1-2% of tuned vanilla LoRA); evidence for lowering LR below 5e-5 is weak. Reconcile the plan's "GDN projections are NOT added" with C2's real target set (flag F4: C2's adapter does attach LoRA to the 24 GDN layers).
6. Keep merging as a trade-off device, but make transfer an eligibility term, not an S weight, and drop the 2 last-K grid points (last3 vs final: S gain 0.00 [-0.24, +0.23]).
7. First experiment, free of Modal money: read the 7 saved C2 snapshots (models/q35_4b_c2/snaps) on the 600-row transfer dev on the free L4 to measure when the T19 damage appears (section 6 E2). It decides whether the 25% bar can work.

---

## 2. What C2 did and what the project data show

### 2.1 Recipe actually used (models/q35_4b_c2/train_meta.json lines 4-47; C2_REPORT.md:73)

| Item | Value |
|---|---|
| Start | C1 adapter continued (init_adapter q35_4b_main500k_init), same LoRA kept training |
| LoRA | r16, alpha 32 (alpha/r = 2), dropout 0.05, 32,464,896 trainable parameters |
| Optimiser | lr 5e-5 cosine (last logged lr 5.5e-07), batch 16, 3,673 steps, 0.9901 epoch (ONE pass), seed 20261013 |
| Extras | KD 0.5 on 31,549 replay rows (beta 0.0), symmetric consistency on (sym_cons true, perm_twin 0.3, lam_p 0.5), relations loss 1.0, ordinal 1.0 on 14 rows |
| Mix | 59,340 rows = 23,736 new + 35,604 replay (60% replay), 18 blocks |
| Cost | 186 min, 3.04 s/step, $13.14 = $0.221 per 1K rows per pass; $3.58 per 1K steps |
| Checkpoints | 7 snapshots at 25/33/50/67/75/83/92% plus final, all still on disk (models/q35_4b_c2/snaps: s000918 s001212 s001836 s002460 s002754 s003048 s003379) |

Target modules (adapter header, [local]): MLP in all 32 layers (55.7% of LoRA parameters), GDN linear_attn in_proj_a/b/qkv/z and out_proj in 24 layers (34.6%), full-attention q/k/v/o in 8 layers (9.7%).

### 2.2 The monitor that did not fire

snap_monitor_c2.py lines 11-14 and 34: stop if the old slice is below C1 - 1.5 pp at BOTH 25% and 50%, or mean P(yes) drifts by more than 0.02; snapshots are read ONLY on the old slice (never transfer dev). Observed (C2_REPORT.md:97-99, logs/snap_monitor_c2.jsonl): -1.80 pp (25%), -1.15 (50%), -0.50 (75%); KL(C1 to snapshot) 0.044, 0.030, 0.028; the C1 baseline on that slice is 92.15%. Two properties made it blind to T19 [local reading of the files]: (a) the slice is replay, and replay rows carry the KD anchor, so low KL there is trained in; (b) at 92% the slice has little headroom for a behaviour shift on an unseen family. Each read took about 897 s on the free L4 for 2,000 rows (read_sec in the log), so a stop decision lands about 270 steps (7% of the run) after the snapshot.

### 2.3 Anatomy of the T19 loss (recomputed from the H100 grid reads; totals match C2_REPORT.md:170)

Source: c2_build/train/grid_h100/results/grid_1018_1215/.../models/<model>/preds_c2_transfer_dev, gold from data/c2_transfer_dev.jsonl. T19 has 98 verdict questions (gold: Compliant 39, Non-compliant 33, Cannot be determined 26), 57 pick-the-failing-item questions, 145 yes/no questions. "Decidable" = the 72 verdict questions whose gold is not "Cannot be determined". CIs below are my paired item-level bootstraps (10,000 resamples), slightly narrower than the report's group bootstraps.

| Model | Verdict acc (n 98) | Predicted abstain (of 98; gold 26) | Abstain on the 72 decidable | Decidable acc, abstain masked | Yes/no acc (n 145) | Pick-failing acc (n 57) | T21 acc |
|---|---|---|---|---|---|---|---|
| C1 | 57.1 | 54 | 31 | 72.2 | 64.8 | 68.4 | 75.3 |
| final_a05 | 53.1 | 64 | 40 | 70.8 | 55.9 | 61.4 | 79.7 |
| final_a10 (= C2) | 45.9 | 76 | 50 | 63.9 | 55.2 | 52.6 | 77.0 |
| last3_a10 | 44.9 | 77 | 51 | 63.9 | 56.6 | 52.6 | 77.3 |
| earlylate_a10 | 38.8 | 80 | 55 | 68.1 | 49.0 | 54.4 | 82.0 |

Paired differences vs C1 for final_a10: verdict -11.2 [-20.4, -2.0]; yes/no -9.7 [-17.2, -2.1]; pick-failing -15.8 [-28.1, -5.3]; decidable with abstain masked -8.3 [-18.1, +1.4]. For final_a05: decidable masked -1.4 [-6.9, +4.2], yes/no -9.0 [-15.2, -2.8]. For earlylate_a10: yes/no -15.9 [-23.4, -8.3].

What this says:
- Abstention drift is dose-dependent: predicted abstain share 55.1% (C1), 65.3% (alpha 0.5), 77.6% (alpha 1.0) against a gold rate of 26.5%. C1 already over-abstains at twice the gold rate; C2 adds +10.2 pp at alpha 0.5 and +22.4 pp at alpha 1.0. The sibling file reports the same (c2_dev_diagnostics.md:32-33).
- A loss exists where no abstain option is offered: yes/no and pick-the-failing-item (-9.7, -15.8). The yes/no loss is flat across the path (-9.0 at alpha 0.5, -9.7 at 1.0), i.e. it saturates early on the C1-to-C2 line. This is the "negative transfer" part and blending does not touch it.
- A global abstain-logit offset does not repair C2 (in-sample diagnostic on dev, not a candidate): the best offset lifts C1 from 57.1 to 63.3 (offset -1.5) and C2 from 45.9 to 54.1 (offset -2.0), so the gap moves only from -11.2 to -9.2. Predicted abstains still number 56 of 98 for C2 at the best offset.
- The 33% snapshot averaged with the final (earlylate) is worse than the final on T19 verdict (38.8 vs 45.9), yes/no (49.0 vs 55.2) and abstain count (80 vs 76). If the 33% snapshot had been healthy, a 50/50 average would normally land between healthy and damaged. So it was at least as damaged as the final. UNVERIFIED: averaging is not linear, and the proof is a direct read of snapshot s001212.
- Sibling analysis (c2_dev_diagnostics.md:34) attributes only about a third of the lost T19 rows to the abstain option (11 of 34 verdict rows, 9 gap-choice rows, 14 yes/no rows); that fits the split above.

### 2.4 The alpha curve is concave in gain and convex in loss (C2_REPORT.md:139-151; fractions DERIVED)

| alpha (final) | Mixdev gain | Share of full gain | Transfer | Share of full loss | Loss per pp of gain |
|---|---|---|---|---|---|
| 0.5 | +9.55 | 78% | -1.33 | 28% | 0.14 |
| 0.6 | +10.95 | 89% | -2.67 | 55% | 0.24 |
| 0.7 | +12.06 | 98% | -3.00 | 62% | 0.25 |
| 0.8 | +12.16 | 99% | -2.83 | 59% | 0.23 |
| 0.9 | +12.16 | 99% | -4.17 | 86% | 0.34 |
| 1.0 | +12.31 | 100% | -4.83 | 100% | 0.39 |

So interpolation is WiSE-FT-like in shape (most of the gain at a fraction of the damage) but, with C1 as the zero endpoint, it can never produce positive transfer: all 18 candidates are negative and the highest upper bound is +1.65 (C2_REPORT.md:169, :172). The selection score S (G-proxy + mixdev) rose with alpha (87.71 at final_a05 to 89.47 at final_a10) while transfer fell, so S could not see it (C2_REPORT.md:139-144).

### 2.5 What the training mix teaches about abstaining [local, regex on option text; label counts only]

Regex (case-insensitive): "cannot be determined", "can't tell/cannot tell", "not enough information", "insufficient", "undetermined", "not determinable", "indeterminate", "unanswerable", "cannot determine", word "ask", "need more", "unclear", "not (clearly) specified/stated/mentioned", "cannot be decided/resolved", word "unknown". Applied to option strings of data/c2_parts/c2_train.jsonl (ids starting "r_" = replay).

| Rows | With an abstain-like option | Gold is abstain-like | Share of options-offered rows | Share of all rows in group |
|---|---|---|---|---|
| New (23,736) | 2,396 | 786 | 32.8% | 3.31% |
| Replay (35,604) | 1,495 | 332 | 22.2% | 0.93% |

By block (new rows): T28 241 of 732 offering ASK (33%), T29 218 of 801 (27%), T30 242 of 608 (40%); ASK-type options ("Ask the user first", "Ask the user which one is meant") appear only in T28-T30, plus 11 F6 rows with "Undetermined on this record". Overall abstain-like gold is 1,118 of 3,891 options-offered rows = 28.7%, close to T19's gold rate of 26.5%. So the label FREQUENCY in training is not what makes C2 say "Cannot be determined" on 77.6% of T19 verdicts; the sibling count agrees the mix did not over-supply abstain labels (2.03% of rows, c2_dev_diagnostics.md:38). The cause is conditional (when the model abstains), which is why pairs, not label rates, are the fix (R2). Caveat: the regex is lexical; counts differ slightly from the sibling's typed counts.

### 2.6 Rows per family versus gain (C2_REPORT.md:165 and mix manifest counts; DERIVED)

14 trained families: Spearman correlation of rows with mixdev gain = 0.27. Families with at most 1,000 rows (n 8: T31, T06, T25, T23, F4, F6, T15, F11) averaged +14.9 pp; families with more (n 6: T28, T30, T29, T01, T26, F5) averaged +14.7 pp. T06 (600 rows) +24.0 and T25 (600) +22.7 against F5 (1,362 rows) -1.0 and T26 (1,398) +8.0. Confounded by headroom and difficulty; it only says depth per family is not what bought the gain.

### 2.7 Four flags in plan v3.2 that bear on these levers

- F1. SNAPSHOT STOP (plan line 1055) is the C2 rule: general slice below init - 1.5 pp at both 25% and 50%. It would not have fired on C2 and does not read held-out families. Plan lines 1283-1294 name the G proxy as the first training signal.
- F2. Replay share falls: C2 60% (35.6K of 59.3K) with KD 0.5 on replay; C2.1 at C2 init 38K of 112.5K = 34%, at C1 init 57K of 131.5K = 43% before Opus resizing (plan line 962); new rows rise from 23.7K to about 69.5K (2.9x). Old-slice forgetting in C2 was small at 60% replay (-0.5 to -1.8 pp), so the effect of a lower share is unmeasured.
- F3. Epochs and cost disagree. Plan line 919 says "Epochs: 2 over the mix" and line 969 prices the mix at "about $0.23-0.25 per 1K rows at 2 epochs". C2's own projection for that rate was ONE pass: 59,340 rows, 3,673 steps, projected $14.90 at 2.972 s/step (c2_build/train/logs/c2_check_proj.json), actual $13.14 for 0.9901 epoch. Two passes over 112.5K rows are about 13.9K steps (3.8x C2) and about $50 at $0.221 per 1K rows per pass, above R1 $30; one pass is about 7.0K steps and about $25. By the plan's own rule ("then fewer, stated") the cap forces about 1.0-1.2 passes anyway.
- F4. Targets. Plan line 922: "GDN projections are NOT added". C2's adapter (train_meta.json:36, adapter header) attaches LoRA to linear_attn.in_proj_a/b/qkv/z and out_proj in 24 layers, 34.6% of all LoRA parameters. "Same modules as C2" and "GDN not added" cannot both hold; the CPU attach audit as worded would fail or silently change the recipe.

---

## 3. Evidence by lever

Strength key: HIGH = direct local measurement plus consistent outside evidence; MEDIUM = outside evidence in a nearby setting or a local signal with small n; LOW = indirect or off-domain; NULL = tested and found to do nothing.

### 3.1 Replay ratio

- Pretraining-scale numbers [author-run]. Ibrahim et al. 2024, Table 2 (405M, Pile to German, strong shift), Pile loss: 0% replay 3.56, 1% 2.83, 5% 2.57, 10% 2.46, 25% 2.33, 50% 2.24; German loss 1.11, 1.12, 1.12, 1.13, 1.16, 1.22. Weak shift (Pile to SlimPajama): 1%, 5%, 10% cost nothing on adaptation; 50% costs 0.04 nats. Replay cut forgetting by 0.19 (10B) and 0.21 (405M) nats at 5%. https://arxiv.org/html/2403.08763
- SFT-scale. "Talking to Yourself" (self-generated rehearsal, 5 models, 3B-13B, LoRA r8 alpha 16 lr 2e-4 and full FT): 1:1 mix of rehearsal to task data default; in-domain performance "dropped sharply above r about 1.25"; best in 40 of 50 scenarios; Qwen2.5-7B IFEval 74.1 base, 53.9 / 58.2 task-only (full / LoRA), 68.5 / 73.6 with rehearsal. https://arxiv.org/html/2602.20162v1
- Many-task continual regime (T5, classification). SuRe Table 5, LNT, best variant: 76.12 at replay 1:2 and 69.42 at 1:16 (-6.7). https://arxiv.org/html/2511.22367v1
- Replay can help the target too: Kotha and Liang, generic replay raises target data efficiency up to 1.87x (Flan), 1.49x (FineMath), 1.09x (StarCoder), +4.5% on a web-agent task at 8B. https://arxiv.org/html/2603.04964
- Local: C2 at 60% replay with KD held the old slice within -0.5 to -1.8 pp and general dev at -0.48 pp, yet transfer failed. Replay protects what it covers; it cannot protect a family it does not contain.
- Verdict: MEDIUM that a replay share of 25-50% is on the flat part of the forgetting curve; LOW that more replay would have saved T19. Do not add replay as the transfer fix. Keep generic/Block R share at or above 30% (plan: 34-43%) and choose its composition to look like held-out families (human-labelled sources).

### 3.2 Learning rate

- ICLR 2026, "SFT Doesn't Always Hurt General Capabilities" [author-run, full fine-tuning, Qwen2.5-3B, Qwen3-4B, Gemma3-4B]: raising LR from 1e-6 to 5e-6 moved the three-model mean general score from 0.6924 to 0.3805 (-0.31) while domain rose 0.5339 to 0.5583 (+0.02). Theorem 3.2 (informal): the largest safe LR scales as 1/sqrt(s), s = expected low-probability tokens per example, so label-only SFT, like our one-token readout, tolerates larger LR. No method removes the trade-off. https://arxiv.org/html/2509.20758v3
- LoRA-specific. Biderman et al. TMLR 2024: best LoRA LR is about 10x full FT (5e-4 code, 2e-4 math vs 5e-5 and 1e-5); LoRA has no near-optimal alternative within 90% of its best, so it is more LR-sensitive. https://arxiv.org/html/2405.09673v2 Thinking Machines: LoRA LR about 10x full FT (9.8 fitted), about 15x under 100 steps [second-hand, research_v3/recipe.md:12]. Shuttleworth et al.: higher LR gives more intruder dimensions and more forgetting [second-hand, recipe.md:14]. Ibrahim 2024: peak LR trades adaptation against forgetting, small differences over a 4x range; re-warming the LR forgets even without a shift (Fig 8).
- "Learning Rate Matters": across 0.6B-13B, ranks 4-256, all LoRA variants peak within 1-2% of tuned vanilla LoRA; LR tuning matters more than variant choice (best LR moves 2e-4 to 6.3e-4 to 1.1e-3 as batch goes 16 to 64 to 128). https://arxiv.org/html/2602.04998
- Local: the anchors disagree on what "right" is: 10x the ICLR-2026 full-FT LRs (1e-6 to 5e-6) gives 1e-5 to 5e-5 for LoRA, while 10x a common 1e-5 full-FT value gives 1e-4. C2's 5e-5 sits inside that range, and its in-family gain (+12.3) says it was not LR-starved. Scaling the update down trades in-family gain for transfer at the measured exchange rate in section 2.4.
- Verdict: MEDIUM for "do not go above C2's LR" (the plan's rule), LOW for "go lower". An LR cut is the same axis as the alpha blend and buys the same trade.

### 3.3 Steps and epochs

- Kalajdzievski 2024: with LoRA, forgetting follows a shifted power law in the number of fine-tuned parameters AND in update steps; there is a strong inverse linear relation between fine-tuning performance and forgetting; "cannot be avoided through early stopping or by varying the number of parameters fine-tuned". https://arxiv.org/abs/2401.05605 (no constants on the abstract page).
- Biderman: forgetting generally worsens with training duration; instruction fine-tuning forgets more than continued pretraining. Full FT best at epoch 2 on Tulu-v2-mix, LoRA wants about 4 epochs. https://arxiv.org/html/2405.09673v2
- Gekhman et al. 2024 (PaLM 2-S, closed-book QA): fitting examples the model does not know costs about what fitting known ones gains (linear fit on the share of examples fitted, out of distribution: coefficients +3.2 for known, -3.0 for unknown, R2 0.95); with 50% unknown, accuracy falls from 43.0 at early stopping to 38.8 at convergence. https://arxiv.org/html/2405.05904
- Timing of damage: spurious-forgetting study (Biography task, randomly initialised LM): old-task accuracy fell from about 100% to about 10% within the first 150 optimisation steps of the new task. https://arxiv.org/html/2501.13453 LLM2Jev (Qwen3.5-4B option readout, intent-only data) general benchmark 81.4 to 77.5 at 100 steps and 74.9 at one epoch while validation loss kept falling [second-hand, research_v4_levers/accuracy.md:120; arXiv 2610.02076 not re-fetched]: 60% of the one-epoch drop (3.9 of 6.5) by step 100.
- Local: 3,673 steps at 5e-5, damage inferred (UNVERIFIED) to be present by the 33% snapshot (section 2.3); the plan's 2 epochs would be 3.8x the steps (F3).
- Verdict: MEDIUM-HIGH. One pass; extra compute goes to distinct rows, not repeats. Read transfer early (steps 150-300 are informative), not only at 25%.

### 3.4 LoRA rank, alpha, targets, variants

- Biderman: rank is a knob that moves both curves up-left (more learning, more forgetting); targeting attention only underperforms MLP-only and all modules; alpha = 2r best; weight decay (5e-5, 1e-4) and attention dropout (0.05, 0.1) learned and forgot about as much as full FT, while LoRA r16 learned and forgot least. https://arxiv.org/html/2405.09673v2
- Variants: within 1-2% of vanilla LoRA at tuned LR (above). Capacity does not bind: 32.5M parameters against at most about 2.5e5 bits of label information in the mix [second-hand, accuracy.md:82].
- Subset tuning (multimodal, full FT): attention projections or MLP gate+up gave less forgetting [second-hand, recipe.md:40]. Unknown for LoRA.
- Counter-evidence on LoRA forgetting less: a search summary says a 2026 clinical-guideline paper (arXiv 2605.01077) found LoRA forgot more than full FT; its abstract does not mention it, so UNVERIFIED. Shuttleworth (intruder dimensions) is the supporting primary claim [second-hand].
- Local: C2 targets are MLP + GDN + 8 full-attention layers (flag F4). No local evidence on which module group carries the T19 damage.
- Verdict: NULL for rank and variants; keep r16, alpha 32, dropout 0.05, C2's actual target set. An ablation of GDN modules is possible (34.6% of parameters) but has no outside support.

### 3.5 Weight averaging and merging

- WiSE-FT [author-run, vision]: ensembling zero-shot and fine-tuned weights gave +4 to +6 pp under distribution shift over prior work and +1.6 pp on ImageNet. https://arxiv.org/abs/2109.01903 The same shape appears in C2's grid (2.4), but the endpoint matters: WiSE-FT's zero-shot endpoint is strong out of distribution, C1 on T19 is not (C1 is 63.0% and over-abstains).
- Lin et al. 2023 (OpenLLaMA-3B, Mistral-7B): interpolating pre- and post-RLHF weights gave the best alignment-forgetting Pareto front among the methods compared; layer-wise ratios (HMA) improved on it. https://arxiv.org/abs/2309.06256 (no numbers on the abstract page).
- Delta scaling gamma 0.6 / 0.8 cost 1.07 / 5.27 general points on Qwen3-14B biology [second-hand, recipe.md:38, MemSFT Table 11]. ICLR 2026 table: Wise-FT kept the general score highest (0.7268 at 1e-6) but its domain score fell to 0.1983 against 0.5339 for plain SFT, so averaging bought retention by giving up the gain.
- Merging experts instead of mixing data (Aya 23 8B, six languages): merged models beat the 15%-safety data mix by up to 8% on general quality and 10% on safety (abstract), but with large method dependence (SFT, Linear merge: +8.6 general points vs the mix; TIES on DPO: -7.4 general points; safety effects differed by method). https://arxiv.org/html/2410.10801 [author-run, one setup].
- Sequential LoRA vs joint training (Llama-2-7B-chat, Table 1): sequential LoRA 76.0 / 68.7 / 22.6 vs multi-task 80.9 / 78.1 / 45.2 on 5-task / 15-task / SuperNI benchmarks, so the sequential-minus-joint gap grows with the number of tasks (4.9, 9.4, 22.6 points); initialising from the previous LoRA (80.4 / 74.8 / 37.2) beats fresh zero init (65.7 / 59.6 / 31.1). https://arxiv.org/html/2512.23017v1
- Local: last-3 average = final (S 89.39 vs 89.47; transfer -4.50 vs -4.83; C2_REPORT.md:145); early+late average adds nothing and is worse on T19; alpha curve in 2.4.
- Verdict: MEDIUM as a trade-off device with a known exchange rate, LOW as a transfer fix. Continuing the existing adapter (C2.1 plan: same r16 LoRA) is supported over a fresh LoRA. Training the union (replay + new) is supported over new-only.

### 3.6 KD, self-distillation, KL to the init

- RL's Razor [author-run]: forgetting is predicted by the forward KL between fine-tuned and base policy measured ON THE NEW TASK: R2 0.96 on ParityMNIST, 0.71 for LLMs (Qwen2.5-3B-Instruct); SFT representations drift more (CKNNA to base 0.56 vs RL 0.94 at equal new-task accuracy); an analytic SFT target that minimises KL to the base gave the best trade-off on MNIST. The authors suggest monitoring forward KL on the new task as a label-free forgetting proxy. https://arxiv.org/html/2509.04259
- Self-distillation SFT: using the model's own outputs as targets mitigates forgetting while keeping downstream performance (Llama-2-chat; no numbers on the abstract page). https://arxiv.org/abs/2402.13669 "Talking to Yourself": best forgetting protection in 40 of 50 scenarios (section 3.1).
- Local: C2 used KD 0.5 (beta 0.0) only on 31,549 replay rows; new rows had none. The monitored KL (0.044, 0.030, 0.028) was measured on replay, where KD acts.
- Verdict: MEDIUM-LOW for a one-token readout (evidence is generative or MNIST), but cheap in data and well-motivated; run as an A/B arm (R5) and use KL on held-out-family rows as a monitor (section 5).

### 3.7 Loss reweighting and hard examples

- TALR (weights p(x)^(1/tau), tau = batch median token loss) at LR 5e-6: general +0.121 over plain SFT for -0.017 domain; FLOW +0.069 general for -0.006 domain (ICLR 2026 table, above; means of three models). FLOW alone: -0.8% GSM8K, +5.4% retained [second-hand, recipe.md:38].
- Gekhman: unknown examples are fitted slowly and hurt when fitted (above).
- Plan tension: hard bin gets a 2x weight and trap selection picks C2's errors (plan section 5), the opposite of FLOW/TALR, which down-weight low-probability examples. Prior note flagged the same (recipe.md:96).
- Verdict: LOW-MEDIUM (generative full FT). Arm, not default. Keep the plan's "no hard upweight on general rows" and add: no 2x on rows whose gold gets p < 0.05 under C1 until an A/B shows it does not move held-out families.

### 3.8 Multi-task balancing

- Gradient-surgery and loss-weighting methods did not beat a well-tuned weighted-average baseline on large language and vision benchmarks (Xin et al. 2022). https://arxiv.org/abs/2209.11379 (abstract-level).
- Flan 2022 ablations (T5-XL, Table 1, zero-shot / few-shot): removing mixture balancing cost held-out MMLU -4.9 / -6.6 and BBH -11.1 / -15.0 and held-in -2.6 / -1.7; the weighted mixture beat the equal mixture by +0.8 MMLU but lost 1.3 on CoT (Table 2). https://arxiv.org/html/2301.13688
- FLAN 2021: instruction tuning hurt held-out tasks for models of 8B or less in that study (422M, 2B, 8B), explained as capacity used up by the training tasks; the effect reversed at 68B/137B. https://arxiv.org/html/2109.01652 (2021 LaMDA-PT models; a 4B LoRA is a different regime, LOW relevance).
- Local: C2's two largest blocks (GW 3,696, GB 3,376) are 29.8% of new rows; no per-family cap beyond the mixer's.
- Verdict: MEDIUM that sampling balance matters for held-out tasks; HIGH that fancy gradient methods are not worth the code. Use a written cap rule: no family above 8% of non-replay rows, source-level caps in Block R, balance set before any look.

### 3.9 Data diversity and public human-labelled train splits

- Super-NaturalInstructions (T5, 757 training tasks): held-out performance rises log-linearly with the NUMBER OF TASKS; instances per task saturate at 64; T5-large with 757 tasks (48.0 ROUGE-L) is close to T5-3B with 128 tasks (48.4). https://arxiv.org/html/2204.07705
- Flan 2022 Table 2 (equal-weight mixture): dropping the Flan 2021 source costs -9.6 held-in and -1.6 MMLU; dropping T0-SF costs -2.6 MMLU; dropping Super-NaturalInstructions, CoT, program synthesis or dialog each moved MMLU by 0.5 or less. https://arxiv.org/html/2301.13688
- Kotha and Liang: generic data in the fine-tuning mix raises target data efficiency (above), so Block R is double duty: diversity plus an anchor.
- Noise caution: human-label noise is real (T37b's replay sources carried wrong golds: C2_REPORT.md:88 and the HANDOFF.md pilot table row "T37b (wrong human golds in its replay sources)"); the A46 screen stays.
- Abstain caution: plan line 1769 puts SQuAD 2.0, AmbigQA, Natural Questions and other "Reading / QA / abstain" sources in Block R. Measure each source's abstain-like gold share before mixing and report it beside section 2.5's 28.7%.
- Verdict: MEDIUM (T5-era, classification-like, but the direction is consistent across Super-NI, Flan and the local rows-vs-gain weak correlation).

### 3.10 Abstention-specific evidence

- Refusal is a transferable meta-skill. R-Tuning (OpenLLaMA-3B, LLaMA-7B, -13B): trained on five datasets and tested on unseen HaluEval-QA, AP 73.85 vs 72.11 (3B), 77.17 vs 76.22 (7B), 80.36 vs 75.73 (13B) for refusal-aware vs vanilla; in-domain MMLU answer rates were as low as 5.79% (3B) and 9.56% (7B), a heavy-refusal side effect. https://arxiv.org/html/2311.09677v2
- Small refusal mixes cause over-refusal. Bianchi et al.: about 3% safety examples (a few hundred) improve safety substantially, but more safety data makes models refuse safe look-alikes; the model tuned with 2,000 safety examples answered more than 50% of 50 safe XSTest prompts with exaggerated safety. https://arxiv.org/html/2309.07875v3
- Class mix moves the operating point: doubling the Safe share made Qwen3Guard more permissive [second-hand, recipe.md:20].
- Relabelling unknown training items as "I don't know" kept answered-accuracy at 61.8 while answering 58.7% to 55.6% (Gekhman Table 3).
- Local: ASK/abstain gold is 33%, 27%, 40% of ASK-offering rows in T28/T29/T30, 2.03% of all rows overall. T19 shows the shape of the error: the model abstains when evidence is partial, even when the rule set decides the answer. Hypothesis, UNVERIFIED and testable on CPU: "no evidence on file" cues in new ASK rows teach "missing item means abstain", which T19 violates when the control does not apply. 
- Verdict: MEDIUM for the mechanism. The fix that the evidence and the local rates support is conditional (paired twins, cue-balanced), not a lower overall abstain rate.

### 3.11 Early stop and held-out-family reads

- Direct evidence is thin: a search for papers measuring negative transfer to unseen task families under narrow-mix LoRA, with checkpoint selection rules, found none. Supporting pieces: Gekhman (early stopping at 5-10 epochs vs 50 epochs: 43.0 vs 38.8 at 50% unknown), spurious forgetting (collapse in 150 steps, reversible with small old-task data: 10 rejection-style examples x 10 epochs took safety from 0% to about 99%), Granite Guardian (checkpoint by minimum validation CE; recipe.md:21), RL's Razor (KL on new-task rows as a proxy), Kalajdzievski (early stopping alone cannot avoid forgetting).
- Local: the old-slice rule did not fire although transfer failed; snapshots exist to test a better rule (E2).
- Verdict: the stop rule is a cost cap and a diagnosis trigger, not a repair. HIGH value for money (the read is free on L4; a stop at 25-34% saves 66-75% of a $25-28 pass).

---

## 4. Ranked recommendations

Order = expected value for C2.1 given the evidence above. "Effect" is DERIVED or "no estimate"; nothing here has a measured effect on a C2.1-like mix except the alpha exchange rate.

R1. Transfer-aware early warning and selection (strength HIGH for the need, MEDIUM for the bars). Build the held-out-family set as two groups before the data freeze: MONITOR families (2, never trained, never in the gate) read at 10%, 25%, 50% snapshots, and GATE families (at least 4, at least 1,200 rows in all; HANDOFF.md:137-146 asks the same) read at the grid and final only. Bars and false-alarm math in section 5. Make transfer an ELIGIBILITY term in the grid (pooled non-inferiority with its lower bound above a pre-registered floor) instead of a weight in S; C2's check (b) was a superiority test (+3.0, LB > 0) that no blend could pass, so keep (b) at the final gate as written and add the harm bar for the stop rule. Effect: no change to the model; caps wasted spend; C2 would have been stopped at the 25% or 50% read if the E2 read confirms damage by then. Cost: $0 Modal (free L4), about 13.5 min per 1,800 rows.

R2. Data: contrastive commit/abstain structure and per-family gates (strength MEDIUM-HIGH, effect size unknown). (a) A decidable twin for every ASK / can't-tell row, same surface cues, opposite gold (already in the HANDOFF fix plan). (b) Cue-balance: for each "missing item" cue, an equal-or-greater number of rows where the cue is present and the answer is decidable. (c) Per-family gates before the freeze: record gold abstain share among ASK-offering rows (C2 baseline 27-40%), and require C1's predicted abstain share on each family's dev to be reported next to gold (T19: 55.1% vs 26.5%). (d) Report abstain-like gold share per Block R source (SQuAD 2.0 etc.) before mixing. (e) Test a factorised loss as an A/B arm: binary commit-vs-abstain term with class weights plus a choice term renormalised over decidable options (diagnostic basis: abstain-masked discrimination dropped only -8.3 [-18.1, +1.4] while the unmasked verdict dropped -11.2; no outside evidence, UNVERIFIED).

R3. Breadth over depth (strength MEDIUM). Cap trained families at about 1,000 new rows (C2: n 8 at most 1,000 rows averaged +14.9; n 6 above averaged +14.7; Super-NI saturates at 64 per task) and spend the savings on additional distinct families and Block R sources. Put the sampling cap in writing before any look (3.8): no family above 8% of non-replay rows. Expected effect: no estimate; direction supported by Super-NI (+ number of tasks) and Flan (-11.1/-15.0 BBH without balancing).

R4. One pass, not two (strength MEDIUM-HIGH). Set stage A to one pass over the deduplicated mix (about 7.0K steps for 112.5K rows, about $25), keep the cosine schedule, and treat any second pass as a decision made at the 50% read only if held-out reads are flat. Fix the plan's cost text (F3). Save the compute for the stop rule and the grid.

R5. KD / KL to the init on new rows, as an A/B (strength MEDIUM-LOW). Arms at 5-10% of a pass, same schedule: (A) C2 recipe; (B) KD 0.5 on new rows too (soft target = 0.5 one-hot + 0.5 C1 distribution); (C) B plus R2(e). Read monitor families at the end of each arm; compare arms only with each other (an early snapshot at un-decayed LR is pessimistic: the C2 old slice read -1.80 at 25% and -0.50 at 75%). Cost about $2.5 per arm at 10% (0.1 x 112.5K rows x $0.221/1K), $1.25 at 5%; needs the owner's GO (training money, HANDOFF.md:137-146 option 7). Risk: KD on new rows slows the learning the owner wants; the A/B measures the slope.

R6. Hold the optimiser recipe (strength MEDIUM for "not higher"). LR 5e-5 cosine, batch 16 (do not inherit a larger batch: LR scales with batch, "Learning Rate Matters"), r16, alpha 32, dropout 0.05, C2's actual target set. No rank change, no PiSSA/DoRA/MiLoRA arms. Reconcile F4 in the plan text and the attach audit before the freeze.

R7. Merging: keep as an exchange-rate tool, change the grid (strength MEDIUM/LOW). Drop the 2 last-K points (no gain in C2) and the early+late style points; spend those slots on alpha/gamma 0.7 and 0.85 of the final, each judged by transfer eligibility and S. At C2's measured rates an alpha of 0.7 would have given 98% of the gain at 62% of the loss (still -3.0 on transfer), so merging cannot replace R2/R3. Layer-wise ratios (Lin 2023 HMA) are an option only with a selection set separate from the 600-row gate (overfitting risk at n 600); UNVERIFIED for this model.

R8. Replay: hold the share, change the content (strength MEDIUM for share, LOW for transfer). Keep at least 30% generic/Block R (plan 34-43%). Because C2's replay carried KD and the old slice stayed within -1.8 pp, spend no extra rows on it; make sure replay includes records-checking and rule-application rows from human-labelled sources so T19-like skills have anchors without being the held-out family itself.

R9. Reweighting (strength LOW-MEDIUM). Do not apply the 2x hard weight to rows C1 scores below p 0.05 on gold until an arm shows no held-out harm; consider TALR-style weighting only as an arm.

R10. Staging order for all arms: R1 and E1-E3 (CPU or free L4) first; R5 arms only after the owner's GO; no arm uses sealed, quarantine or Jev data.

---

## 5. Early-warning stop rule (design for 25% and 50% snapshots)

### 5.1 What to read at each snapshot (all forward-only; none is a candidate)

| Read | Rows | Labels | What it catches | Notes |
|---|---|---|---|---|
| Monitor-family accuracy (2 held-out families, never trained) | 2 x 300 or more | yes | negative transfer on unseen families | paired vs init, per family and pooled |
| Behaviour probes on the same rows | same | no | abstain/ASK share, predicted-class distribution, mean P(abstain) | T19 reads: +22.4 pp predicted abstain at alpha 1.0, +10.2 at 0.5 |
| Forward KL(init to snapshot) on monitor-family inputs | same | no | distribution shift on the unseen task (RL's Razor, R2 0.71 LLM) | the C2 KL was on replay, so it was not informative |
| In-family slice (about 500 rows across trained families) | 500 | yes | price ratio (transfer loss per pp of in-family gain) | report-only; C2 final 0.39, alpha 0.5 0.14 |
| Old slice / G proxy (existing rule) | 2,000 / 3,267 | yes | classic forgetting | keep, cannot stand alone |
| Optional early read at 10% (about step 700 of 7K) | monitor rows | yes | damage that appears within 100-300 steps | bars as 25% |

Noise inputs from C2 [local]: paired SE of a 300-row family difference about 2.96 pp (from the T19 CI [-17.2, -5.6]); pooled 600 rows about 1.93 pp; scaling as 1/sqrt(n) gives about 1.36 pp at 1,200 rows. Snapshots at high LR read pessimistic by about 1.3 pp at 25% and 0.65 pp at 50% relative to the end (old slice -1.80 and -1.15 vs -0.50 at 75%).

### 5.2 Triggers (pre-register all numbers before data exist; never loosen after a result)

| Trigger | 25% snapshot (loose) | 50% snapshot (strict) |
|---|---|---|
| P: pooled transfer difference vs init, one-sided 95% upper bound < 0 | point <= -5.0 pp | point <= -3.0 pp |
| F: any monitor family, point and upper bound | point <= -9.0 pp and UB < -1.0 | point <= -7.0 pp and UB < -1.0 |
| B: label-free, predicted ASK/abstain share on monitor verdict items vs init | >= +20 pp | >= +15 pp |
| G: old slice or G proxy below init - 1.5 pp | (existing: both 25% and 50%) | (existing) |
| K: price ratio > 0.25 | report only | report only |

Decision. At 25%: STOP if P or F or B fires. At 50%: STOP if two of P, F, B fire, or if any one fires at the 25% bars; G fires as in the plan. STOP means: halt the run, keep the snapshot, no candidate from this mix; diagnose with the two reads below; change data (R2/R3), not the schedule. The rule is a cost cap, not a repair (Kalajdzievski).

### 5.3 Operating characteristics (normal approximation, DERIVED; assumes independence of triggers and the SEs above, UNVERIFIED for C2.1 families)

| Trigger | False-alarm rate if true change is 0 (with the snapshot pessimism above) | Power if the truth is C2-like |
|---|---|---|
| P at 25%, n 1,200 pooled, bar -5.0 | 0.3% (2.8% at n 600) | 79% for a true pooled -4.8 (72% at n 600) |
| P at 50%, n 1,200, bar -3.0 | 4.3% (9.5% at n 600) | 96% for -4.8 (88% at n 600) |
| F at 25%, n 300, effective bar -9.0 | 0.5% per family, 1.8% any of 4 | 89% for a T19-like -11.3 |
| F at 50%, n 300, effective bar -7.0 | 1.6% per family, 6.2% any of 4 | 95% for -11.3; 71% for -8 |

The 50% rule needs two of three triggers, which lowers the combined false-alarm rate well below the single-trigger figures (no exact value without the correlation structure; UNVERIFIED).

### 5.4 Retrospective check on C2 final numbers

Pooled -4.83 with SE 1.93 (upper bound -1.66): P fires at 50% (bar -3.0), not at 25% (bar -5.0). T19 -11.3 [-17.2, -5.6]: F fires at both. Predicted abstain +22.4 pp over C1: B fires at 25% (+20) and 50% (+15). So the rule would have stopped C2 at the 25% read if T19 was already that damaged then. The earlylate row (33% snapshot averaged with the final: T19 46.7, abstain 80) says it likely was.

### 5.5 Cost and latency

- Reads: free L4 through the existing tool, measured 897.5 s and 896.1 s per 2,000-row read (snap_monitor_c2.jsonl). 1,800 rows (1,200 monitor + 600 in-family) is about 13.5 min, about 270 steps of delay (7% of C2; about 4% of a 7K-step run). So a "25%" read triggers the stop at about 32% of the run, a "50%" read at about 57%.
- Money saved: stop at 32% of a one-pass $25 run leaves about $17 for a corrected mix; a 10% read stops at about 14% and leaves about $21.
- Not re-scored on Modal (owner rule: Modal = training only). If the owner allows one H100 session the read of 1,800 rows costs cents: the C2 grid read 26,191 rows per model at $7.49 for 19 models (about $0.39 per model, boot included).

### 5.6 Governance

- Monitor families are used only for the stop rule; gate families are read only at the grid and final. This keeps the final check (b) from being selected on.
- Snapshots are never candidates (as in C2).
- The stop and its numbers are logged in PREREG before data; changing a bar after a result is a new look and is reported as such.
- Retire the old-slice-only rule as the sole snapshot stop; keep it as trigger G.

---

## 6. First experiments (in order; E1-E3 cost no Modal money)

E1. CPU: abstain-cue audit of the C2 and candidate C2.1 rows. For each ASK/can't-tell row family, count rows with "no evidence/missing" cues by gold; test the "missing means abstain" hypothesis in 3.10 with a cue-ablation on T19 inputs. Output: cue table, no model.
E2. Free L4: read s000918, s001212, s001836 (and the final) on data/c2_transfer_dev.jsonl and the 600 rows' behaviour probes; tabulate T19 accuracy, predicted abstain count, yes/no accuracy by snapshot. This tests "damage by 25-33%" (section 2.3) and calibrates bars 5.2 before they are frozen. Requires the orchestrator to allow a transfer-dev read of C2 snapshots (C2's monitor excluded transfer dev by design; C2 is closed, so it is analysis, not selection). At the measured 0.45 s per row, 600 rows x 4 snapshots is about 18 min of reading; snapshot download and VM preparation were not timed, so budget 20-45 min in all.
E3. CPU/L4: build the MONITOR/GATE families (E1 cost); measure C1 and C2 on them; compute the actual SE per family to replace the section 5.3 assumptions.
E4. After GO: R5 arms at 5-10% of a pass with monitor reads.
What would change the ranking: if E2 shows T19 is healthy at 33% and damaged only late, trigger bars at 25% are useless and R4 (steps) rises above R3; if E2 shows damage by 918 steps, the 10% read becomes worth its cost; if R5 arm B shows no loss of in-family gain, KD on new rows moves to rank 2.

---

## 7. Open questions and UNVERIFIED items

- Damage timing in C2 (section 2.3 inference from the average of two checkpoints).
- Whether C2.1 monitor families will behave like T19/T21 (SE values and bar levels come from n 300 per family).
- Effect size of any data lever on the C2.1 mix: no outside evidence for a one-token readout with program-gold rows; all outside numbers are generative, T5 or vision.
- "Missing-evidence means abstain" mechanism (3.10).
- Whether LoRA forgets more or less than full FT in this regime: Biderman (less) vs a search-summary claim (more) from 2605.01077 that its abstract does not support.
- SuRe's table 5 text vs table mismatch (the page's own caveat); used table values only.
- ICLR 2026 SFT paper: Wise-FT domain scores look unusually low (0.1983 at 1e-6); read as their setup, not a general property of averaging.
- Replay SFT sweep for LoRA classifiers: none found. The 5%-replay SSRN preprint and Dong et al. 2310.05492 remain unverified by me (recipe.md:38).
- Reads of snapshots on L4 may differ slightly from S1 serving (the refparity miss, C2_REPORT.md section 12 item 7, line 215); acceptable for a stop rule, not for a gate.

---

## 8. Sources

Primary (fetched 18 Oct 2026; abstract-only where noted)
- Biderman et al., LoRA Learns Less and Forgets Less: https://arxiv.org/html/2405.09673v2
- Kalajdzievski, Scaling Laws for Forgetting When Fine-Tuning LLMs (abstract): https://arxiv.org/abs/2401.05605
- Ibrahim et al., Simple and Scalable Strategies to Continually Pre-train LLMs: https://arxiv.org/html/2403.08763
- Talking to Yourself (Sa-sft): https://arxiv.org/html/2602.20162v1
- SuRe, surprise-driven replay: https://arxiv.org/html/2511.22367v1
- Kotha and Liang, Replaying pre-training data improves fine-tuning: https://arxiv.org/html/2603.04964
- SFT Doesn't Always Hurt General Capabilities (ICLR 2026): https://arxiv.org/html/2509.20758v3
- Learning Rate Matters: Vanilla LoRA May Suffice: https://arxiv.org/html/2602.04998
- RL's Razor: https://arxiv.org/html/2509.04259
- Self-Distillation Fine-Tuning (abstract): https://arxiv.org/abs/2402.13669
- Spurious Forgetting in Continual Learning of LMs: https://arxiv.org/html/2501.13453
- Merge before Forget (SLAO): https://arxiv.org/html/2512.23017v1
- WiSE-FT (abstract): https://arxiv.org/abs/2109.01903
- Mitigating the Alignment Tax of RLHF (abstract): https://arxiv.org/abs/2309.06256
- Mix Data or Merge Models: https://arxiv.org/html/2410.10801
- Do Current Multi-Task Optimization Methods Even Help (abstract): https://arxiv.org/abs/2209.11379
- Flan Collection (Longpre et al.): https://arxiv.org/html/2301.13688
- FLAN (Wei et al.): https://arxiv.org/html/2109.01652
- Super-NaturalInstructions: https://arxiv.org/html/2204.07705
- Gekhman et al., new knowledge and hallucinations: https://arxiv.org/html/2405.05904
- Safety-Tuned LLaMAs: https://arxiv.org/html/2309.07875v3 (abstract also arxiv.org/abs/2309.07875)
- R-Tuning: https://arxiv.org/html/2311.09677v2
- Not usable: arXiv 2605.01077 (abstract does not support the claim attributed to it by a search summary); 2506.09428 (no ratio sweep; read but not relied on).

Project files (absolute paths under /Users/aryamahadik/Documents/jev/opendecide-data/lean/)
- c2_build/C2_REPORT.md lines 73, 97-99, 139-151, 165, 170-172, 194-196
- models/q35_4b_c2/train_meta.json lines 4-47 and adapter_model.safetensors header (module groups); models/q35_4b_c2/snaps/ (7 snapshots)
- c2_build/snap_monitor_c2.py lines 11-14, 34; c2_build/logs/snap_monitor_c2.jsonl (read_sec, KL)
- c2_build/train/logs/c2_check_proj.json (3,673 steps, 2.972 s/step, $14.90 projected for one pass)
- c2_build/train/grid_h100/results/grid_1018_1215/grid_1018_1215/models/*/preds_c2_transfer_dev/*.jsonl and data/c2_transfer_dev.jsonl (section 2.3)
- data/c2_parts/c2_train.jsonl (section 2.5 label counts only)
- c2_build/zed_orch/c21/C2_1_PLAN_v3.md lines 919, 922, 962, 969, 982, 1055, 1283-1294, 1769
- c2_build/zed_orch/c21/research_v3/recipe.md lines 12-14, 20-21, 38, 40, 96; research_v4_levers/accuracy.md lines 82, 120
- /Users/aryamahadik/Documents/jev/HANDOFF.md lines 137-146 (C2.1 fix plan)
- c2_build/zed_orch/c21/research_v5_c2lessons/c2_dev_diagnostics.md lines 31-39 (cross-check only)
