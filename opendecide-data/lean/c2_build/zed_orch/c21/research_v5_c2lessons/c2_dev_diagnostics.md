# C2 vs C1 on non-sealed dev data: accuracy, abstention, calibration, and which training blocks plausibly drove over-abstention

Date: 18 Oct 2026 (US Eastern). Scope: read-only, internal. Only dev splits and their predictions were opened. No path containing ohs, sealed, quarantine, longbench, jevbench, ejs, c_spec/sealed_brief or c_build/preread was opened, no Jev output was opened, and nothing under ~/.claude was opened. Anything stated about the sealed OHS-4 look comes from the task text and is not re-checked here.

## 0. What was computed, and how (read this before the tables)

**Inputs (all under `/Users/aryamahadik/Documents/jev/opendecide-data/lean/`).** Rows: `data/<split>.jsonl`. Predictions: `preds_<split>/<model>.jsonl` (per-row probabilities over the options). Models: C1 = `q35_4b_main500k_c2` (the C1 H100 read), C2 a10 = `q35_4b_c2grid_final_a10` (the chosen C2 candidate: the final step at merge alpha 1.0; byte-identical to the official `q35_4b_c2` read, which gives the same 76/98 CBD answers on T19), C2 a05 = `q35_4b_c2grid_final_a05` (final step at alpha 0.5). Splits: 9 older dev splits (`dev, dev_claims, dev_nc, dev_negwords, devp_card, devzs, hard_dev, pg_dev, taskbank_dev`; 8,143 rows), `c2_t37b_dev` (600), `c2_transfer_dev` (T19 300 + T21 300) and `c2_mixdev` (3,386 rows, 18 families). Not used: `eval_*` splits and `pab_gproxy` (not dev splits; the task named dev data only). Source for the model/alpha definitions: `c2_build/C2_REPORT.md:17,22,77`.

**Integrity checks (all passed).** For all 12 splits x 3 models: no missing, extra or duplicate ids; the probability keys equal the option strings (choice) or {yes, no} (yes/no); every gold string is one of the options; probabilities sum to 1 within 0.02.

**Scoring.** Direct argmax of the row's probabilities against gold. Yes/no rows (`qtype` "noul"): gold 1 = yes, 0 = no; prediction = the larger of P(yes), P(no). Choice rows: gold is the option text; prediction = the option with the largest probability. This reproduces the C2 report: mixdev trained families +12.31 (report +12.31 [+10.47, +14.15]); transfer 64.33 vs 69.17 (report -4.83); hard_dev +0.96, dev +0.83, dev_nc -1.59 and the other per-split deltas in `C2_REPORT.md:133`.

**CIs.** Paired cluster bootstrap on `group_id` (2,000 resamples, seed 7). The C2 report used 10,000 resamples with seed 0, so bounds differ by about 0.05 pp (e.g. mixdev [+10.4, +14.2] here vs [+10.47, +14.15] there).

**ECE.** 10 equal-width bins on the max-probability, weight = bin count, raw model probabilities (no temperature). Reported in percent. Choice rows with k options have max-prob >= 1/k, so the low bins are empty for them.

**Abstain-type options** are classified from the option text (the classifier is mine; a different one would shift small cells):
- **IND** (cannot-determine type): "cannot be determined ...", "not determinable ...", "undetermined", "not enough information ...", "insufficient", "Cannot decide here", "Not shown in the log", and exact "unknown", "not stated", "maybe".
- **ASK**: "Ask the user first", "Ask the user which one is meant", "Ask the user to be more specific", "ask_clarifying_question" (slot questions such as "Ask for the PIN" are not counted).
- Secondary types shown separately: **ESC** ("Escalate ..."), **NOTA** ("None of ...", "No single entry ...", "Stop and tell the user nothing matched").
- Yes/no rows have no abstain option; for them I report the predicted-yes rate against truth and the share of hedged answers (confidence below 0.6) as a proxy.
- "Truth %" = share of rows (among rows that offer the option type) whose gold is that type. "False-abstain" = P(model answers abstain-type | gold is not). "Missed-abstain" = P(model answers non-abstain | gold is abstain-type).

**Training mix** analysed from `data/c2_parts/c2_train.jsonl` (59,340 rows; its sha256 starts cc1d1ff5..., matching `c2_build/mix_c2/config_fill_c2.json:11`). New rows (23,736, sources `c2_*` and `c_f*`) carry hard 0/1 labels only; the C1 anchor/KD (weight 0.5) is on replay rows only (`c2_build/mix_c2.py:26`, `C2_REPORT.md:44`). T19 and T21 are not in the mix.

**Family names.** For `c2_mixdev` and `c2_transfer_dev` the family is `meta.family`; for the older splits it is the `source` field. "Trained" = the 14 blocks that entered C2 (T28, T29, T30, T26, T31, T01, T23, T06, T15, T25, F5, F6, F11, F4). "Not trained" = T33, T12, T24 (left out under A80) and T07 (left out under A72) (`C2_REPORT.md:55-57`).

## 1. Findings (strongest numbers first)

1. **The mixdev gain is real and broad; transfer loss is one family.** Trained mixdev families: C1 67.9 -> a10 80.3 (**+12.3 [+10.4, +14.2]**, n 2,795); 13 of 14 trained families have a lower CI bound above 0, F5 is -1.0 (n.s.). Largest: T28 +28.0, T30 +27.3, T31 +24.7, T06 +24.0, T25 +22.7. Transfer: T19 **-11.3 [-17.5, -5.5]**, T21 +1.7 [-2.7, +6.0]; pooled -4.8 [-8.7, -1.1]. General dev (9 splits, n 8,143): 81.5 -> 81.0, **-0.5 [-1.1, +0.1]**. Not-trained mixdev families pooled: -2.0 [-5.3, +1.0] (T07 -4.0 [-7.7, -1.3] is the only one with a CI below 0).
2. **C2 does not abstain more in general; where it was trained it abstains at the truth rate.** On the 257 trained-family mixdev rows that offer an IND or ASK option: truth 42.0%, C1 52.5%, a10 **42.4%**, a05 44.0%; false-abstain **31.5% -> 4.7%** (C1 -> a10); missed-abstain 18.5% -> 5.6%; accuracy on those rows 69.6 -> 92.2. C1 was the over-abstainer there (T30 70.7% vs truth 44.8%, F4 75.0% vs 33.3%, T25 54.7% vs 35.8%).
3. **On T19 verdict rows (n 98) C2 over-abstains hard.** Truth "Cannot be determined" 26 (26.5%); C1 answers it 54 (55.1%); a10 **76 (77.6%)**; a05 64 (65.3%). False-CBD rate when truth is not CBD: C1 43.1% -> a10 **69.4%** (a05 55.6%). Precision of a CBD answer 42.6% -> 34.2%; Compliant recall 30.8% -> **7.7%**; Non-compliant recall 63.6% -> 48.5%; CBD recall 88.5% -> 100%. a10 gave 50 false-CBD answers, and C1 was right on 16 of those 50.
4. **The over-abstention is amplified C1 behaviour, not new.** C1 already says CBD at twice the truth rate on T19. C2 adds +22.5 pp (a10) or +10.2 pp (a05). Dose-response across the 19 reads (section 6.4): CBD answers rise 54 (C1) -> 64, 67, 68, 72, 75, 76 for final alpha 0.5 ... 1.0, and reach 80 for early+late alpha 1.0.
5. **Over-abstention explains only about a third of the T19 loss.** Of the 34 correct rows lost on T19 (189 -> 155): verdict rows with a CBD option 11 (32%), gap-choice rows (no abstain option) 9 (26%), yes/no rows 14 (41%). On yes/no the yes-rate did not move (truth 49.0%, C1 51.0%, a10 52.4%), so the yes/no loss (-9.7 pp) is a rule-application degradation, not a label bias.
6. **Where the false CBD lives (T19, a10 vs C1):** edge expiry_boundary 50% -> 83%; exclusion_decides 49% -> 73%; unknown_out_of_scope 43% -> 70%; generator sampler S2 36% -> 91% (n 22). Mean confidence of a false CBD answer 0.700 -> 0.817 (median for a10 0.869).
7. **Calibration breaks out of distribution, and improves in distribution.** ECE C1 -> a10: T19 **14.2 -> 31.4** (a05 25.1); T21 12.1 -> 10.2; transfer pooled 13.0 -> 20.8; general dev 2.9 -> 4.6 (choice rows 3.4 -> **7.0**, yes/no 2.6 -> 3.0); trained mixdev 9.9 -> **5.4**; not-trained mixdev 7.0 -> 12.7. C2 is sharper: share of choice rows at confidence >= 0.9 on general dev 46.5% -> 58.4% while precision there falls 95.9% -> 92.5%; on T19 21.3% -> 36.0% with precision 75.0% -> 66.7%. T19 bin 0.8-0.9: 107 rows, confidence 86.1%, accuracy **43.9%**.
8. **A single temperature does not repair it.** Fitting T on trained-family mixdev (my approximation of the L1 recipe, not the L1 code): a10 needs T = 1.10 (yes/no) and 1.05 (choice) and T19 ECE only moves 31.4 -> 29.8; C1 would need T = 1.55 / 1.35 and that T raises C1's general-dev ECE 2.9 -> 7.4. The trained-family mixdev is the wrong set to fit T on for an out-of-distribution target (section 5.3).
9. **The training mix did not over-supply abstain labels.** Across 59,340 rows only 479 have an IND gold (0.81%), 724 an ASK gold (1.22%), 1,203 together (2.03%). Among rows that offer an IND option the IND-gold share is **27.2%** (new 28.5%, replay 26.1%), equal to T19 dev truth (26.5%). So the cause is not a label base-rate shift.
10. **Most plausible drivers (correlational, ranked):** (1) **T29** (361 abstain-gold rows = 18.1% of its block: 143 "Cannot decide here" + 218 "Ask the user first"; a verdict menu closest in shape to T19's Compliant / Non-compliant / Cannot be determined; C2 raised its abstain rate on T29 by +6.5 pp (IND) and +4.7 pp (ASK) over C1 while C1 was below truth), (2) **T25** (84 IND-gold, the highest IND rate of any new block, 35% of its IND-option rows; the only abstain-bearing block among T19's lexical neighbours: 8.9% of T19's top-20 neighbours, 8.8x enriched), (3) **T28 and T30** (241 and 242 ASK-gold rows; they teach "stop and ask when the rules do not settle it"; T28 abstain rate also rose +6.4 pp over C1), (4) replay `gd_boardgameqa` / `gd_logicinference` / `gd_babi_logic` (126 + 36 + 33 "unknown" golds, i.e. 195 of the 251 IND-gold replay rows). Not supported as drivers: F4, F6, T26, T31 (0 to 1 IND/ASK gold rows each). None of this is a causal test (section 7).
11. **An untrained records-checking family shows the same drift in miniature.** T33 (options Supported / Contradicted / Not shown in the log; not in the mix): "Not shown" answers C1 9 of 32 -> a10 12 of 32 (truth 8), false-abstain 8.3% -> 16.7% (n 24 non-gold rows; CI wide; accuracy +2.1 n.s.).
12. **No positional shortcut.** T19's CBD option sits first/middle/last in 32/34/32 of 98 rows; in training T29 it is first/middle/last in 155/244/151 of 550 IND-option rows and T25 in 69/72/97 of 238.

## 2. Accuracy and ECE by split

Accuracy in %, deltas in percentage points, CIs 95% (paired cluster bootstrap). ECE in %.

| Set | n | C1 acc | C2 a10 acc | a10 minus C1 (pp) [95% CI] | C2 a05 acc | a05 minus C1 (pp) [95% CI] | ECE C1 | ECE a10 | ECE a05 |
|---|---|---|---|---|---|---|---|---|---|
| dev | 600 | 89.5 | 90.3 | +0.8 [-0.5, +2.2] | 89.8 | +0.3 [-0.7, +1.3] | 4.9 | 3.4 | 4.4 |
| dev_claims | 750 | 88.3 | 87.3 | -0.9 [-2.9, +0.9] | 87.9 | -0.4 [-1.5, +0.5] | 3.2 | 3.9 | 2.8 |
| dev_nc | 1008 | 76.6 | 75.0 | -1.6 [-3.0, -0.2] | 76.5 | -0.1 [-1.0, +0.9] | 3.3 | 8.2 | 4.9 |
| dev_negwords | 800 | 87.4 | 88.1 | +0.8 [-1.0, +2.5] | 89.0 | +1.6 [+0.5, +2.9] | 3.4 | 3.5 | 4.3 |
| devp_card | 1728 | 86.6 | 86.4 | -0.2 [-1.4, +1.0] | 86.8 | +0.2 [-0.6, +1.1] | 2.8 | 4.2 | 3.7 |
| devzs | 800 | 77.4 | 75.8 | -1.6 [-3.2, +0.0] | 76.5 | -0.9 [-2.0, +0.2] | 6.3 | 10.9 | 9.1 |
| hard_dev | 208 | 79.3 | 80.3 | +1.0 [-2.0, +3.9] | 80.3 | +1.0 [-1.4, +3.4] | 6.1 | 5.3 | 4.5 |
| pg_dev | 1049 | 66.0 | 64.3 | -1.7 [-4.0, +0.7] | 65.4 | -0.6 [-2.3, +1.2] | 1.8 | 5.1 | 3.2 |
| taskbank_dev | 1200 | 82.6 | 83.0 | +0.4 [-0.7, +1.6] | 82.6 | +0.0 [-0.8, +0.9] | 5.6 | 8.6 | 7.4 |
| **General dev, 9 splits pooled** | 8143 | 81.5 | 81.0 | -0.5 [-1.1, +0.1] | 81.5 | +0.0 [-0.4, +0.5] | 2.9 | 4.6 | 3.4 |
|   of which yes/no rows | 4329 | 85.2 | 85.0 | -0.2 [-1.2, +0.7] | 85.6 | +0.4 [-0.2, +1.0] | 2.6 | 3.0 | 3.1 |
|   of which choice rows | 3814 | 77.2 | 76.5 | -0.8 [-1.6, +0.1] | 76.9 | -0.3 [-0.9, +0.3] | 3.4 | 7.0 | 5.1 |
| c2_t37b_dev (not a candidate input) | 600 | 83.7 | 81.8 | -1.8 [-4.5, +0.8] | 83.7 | +0.0 [-2.0, +2.0] | 4.1 | 6.7 | 6.5 |
| c2_transfer_dev T19 | 300 | 63.0 | 51.7 | -11.3 [-17.5, -5.5] | 56.0 | -7.0 [-11.6, -2.3] | 14.2 | 31.4 | 25.1 |
| c2_transfer_dev T21 | 300 | 75.3 | 77.0 | +1.7 [-2.7, +6.0] | 79.7 | +4.3 [+1.0, +7.8] | 12.1 | 10.2 | 8.7 |
| **c2_transfer_dev T19+T21** | 600 | 69.2 | 64.3 | -4.8 [-8.7, -1.1] | 67.8 | -1.3 [-4.2, +1.6] | 13.0 | 20.8 | 16.1 |
| **c2_mixdev, 14 trained families** | 2795 | 67.9 | 80.3 | +12.3 [+10.4, +14.2] | 77.5 | +9.6 [+8.0, +11.1] | 9.9 | 5.4 | 5.0 |
|   of which yes/no rows | 1579 | 73.0 | 82.6 | +9.6 [+7.0, +12.2] | 81.2 | +8.2 [+6.3, +10.2] | 10.9 | 5.9 | 5.0 |
|   of which choice rows | 1216 | 61.3 | 77.2 | +15.9 [+13.4, +18.5] | 72.7 | +11.3 [+9.1, +13.7] | 8.6 | 4.6 | 5.0 |
| c2_mixdev, 4 not-trained families (T33,T12,T24,T07) | 591 | 72.9 | 70.9 | -2.0 [-5.3, +1.0] | 72.6 | -0.3 [-2.7, +2.0] | 7.0 | 12.7 | 9.3 |
| All 12 splits pooled | 12729 | 77.6 | 79.6 | +2.0 [+1.3, +2.7] | 79.7 | +2.1 [+1.6, +2.6] | 3.8 | 5.4 | 4.3 |

Notes: `c2_t37b_dev` is listed for completeness (T37b was moved to C3, `C2_REPORT.md:59`, so the split is not in C2's trained families). The general-dev pooled row (-0.48 [-1.11, +0.13]) is close to the report's D1 full-dev line (-0.60 [-1.31, +0.15], `C2_REPORT.md:110`) but not identical; I did not re-derive D1's exact row set or weighting (UNVERIFIED reason for the 0.1 pp gap). The per-split deltas match `C2_REPORT.md:133-134` to rounding (all 9 splits, both alphas).

## 3. c2_mixdev by family (accuracy and ECE)

| Family | Status | n | n choice | C1 | a10 | a10 minus C1 [CI] | a05 | a05 minus C1 | ECE C1 | ECE a10 | ECE a05 | conf-acc C1 | conf-acc a10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F4 | trained | 150 | 73 | 62.7 | 74.7 | +12.0 [+4.0, +20.0] | 70.7 | +8.0 | 16.2 | 9.7 | 9.1 | 15.9 | 7.1 |
| F5 | trained | 400 | 0 | 84.2 | 83.2 | -1.0 [-5.8, +3.5] | 85.0 | +0.8 | 6.0 | 7.4 | 5.2 | 4.3 | 7.4 |
| F6 | trained | 345 | 145 | 70.7 | 80.6 | +9.9 [+4.9, +15.1] | 76.8 | +6.1 | 8.8 | 4.6 | 6.4 | 8.3 | 2.5 |
| F11 | trained | 400 | 212 | 31.5 | 38.0 | +6.5 [+2.0, +10.9] | 35.5 | +4.0 | 20.2 | 15.0 | 17.2 | 20.2 | 15.0 |
| T01 | trained | 150 | 92 | 66.7 | 78.0 | +11.3 [+1.8, +20.9] | 78.7 | +12.0 | 6.4 | 7.3 | 9.6 | -3.4 | -5.3 |
| T06 | trained | 150 | 84 | 54.7 | 78.7 | +24.0 [+15.4, +32.1] | 69.3 | +14.7 | 14.0 | 7.9 | 7.0 | 13.5 | 1.6 |
| T07 | NOT trained | 150 | 65 | 89.3 | 85.3 | -4.0 [-7.7, -1.3] | 88.7 | -0.7 | 2.7 | 7.8 | 5.0 | 1.1 | 6.5 |
| T12 | NOT trained | 150 | 63 | 55.3 | 50.7 | -4.7 [-11.8, +2.8] | 56.7 | +1.3 | 19.7 | 25.2 | 17.3 | 16.7 | 25.2 |
| T15 | trained | 150 | 75 | 92.7 | 99.3 | +6.7 [+2.5, +11.4] | 99.3 | +6.7 | 6.4 | 4.7 | 5.5 | -1.5 | -4.3 |
| T23 | trained | 150 | 96 | 81.3 | 94.0 | +12.7 [+5.7, +19.7] | 92.0 | +10.7 | 7.9 | 6.7 | 6.7 | 7.9 | -0.8 |
| T24 | NOT trained | 150 | 71 | 73.3 | 72.0 | -1.3 [-8.0, +5.6] | 71.3 | -2.0 | 5.5 | 11.2 | 11.8 | 2.5 | 11.2 |
| T25 | trained | 150 | 83 | 72.7 | 95.3 | +22.7 [+14.0, +31.8] | 89.3 | +16.7 | 9.6 | 4.7 | 8.6 | 8.4 | -2.1 |
| T26 | trained | 150 | 70 | 92.0 | 100.0 | +8.0 [+3.8, +12.7] | 99.3 | +7.3 | 2.1 | 4.1 | 4.9 | 1.0 | -4.1 |
| T28 | trained | 150 | 78 | 58.7 | 86.7 | +28.0 [+19.1, +36.8] | 79.3 | +20.7 | 28.1 | 5.3 | 9.7 | 28.1 | 3.1 |
| T29 | trained | 150 | 78 | 82.7 | 97.3 | +14.7 [+8.2, +22.1] | 95.3 | +12.7 | 5.6 | 4.7 | 4.8 | 3.1 | -3.1 |
| T30 | trained | 150 | 75 | 70.0 | 97.3 | +27.3 [+20.1, +34.9] | 94.7 | +24.7 | 13.6 | 5.2 | 6.2 | 13.6 | -3.4 |
| T31 | trained | 150 | 55 | 60.7 | 85.3 | +24.7 [+16.1, +33.6] | 78.0 | +17.3 | 15.7 | 5.6 | 8.4 | 14.0 | 3.8 |
| T33 | NOT trained | 141 | 70 | 73.8 | 75.9 | +2.1 [-4.3, +9.0] | 73.8 | +0.0 | 5.9 | 11.1 | 8.2 | 3.3 | 7.7 |

conf-acc = mean max-probability minus accuracy (positive = overconfident), in pp. The four not-trained families are report-only. Sizes are 150 per family except F5 400, F11 400, F6 345, T33 141, F4 150.

## 4. Transfer set (T19 compliance/expiry, T21 caps)

### 4.1 Accuracy and ECE by slice

| Slice | n | C1 | a10 | a10 minus C1 [CI] | a05 | a05 minus C1 | ECE C1 | ECE a10 | ECE a05 | mean conf C1 | mean conf a10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T19 choice | 155 | 61.3 | 48.4 | -12.9 [-21.1, -5.4] | 56.1 | -5.2 | 13.2 | 33.6 | 22.4 | 71.8 | 82.0 |
| T19 noul | 145 | 64.8 | 55.2 | -9.7 [-18.2, -0.7] | 55.9 | -9.0 | 19.9 | 28.9 | 27.9 | 82.9 | 84.1 |
| T21 choice | 163 | 66.3 | 69.9 | +3.7 [-2.4, +9.8] | 73.6 | +7.4 | 17.8 | 14.5 | 12.0 | 83.6 | 84.4 |
| T21 noul | 137 | 86.1 | 85.4 | -0.7 [-6.7, +5.4] | 86.9 | +0.7 | 5.4 | 8.9 | 9.5 | 91.4 | 90.4 |
| T19 qform=ch_gap | 57 | 68.4 | 52.6 | -15.8 [-28.3, -3.5] | 61.4 | -7.0 | 8.5 | 31.9 | 18.0 | 69.0 | 82.9 |
| T19 qform=ch_verdict | 98 | 57.1 | 45.9 | -11.2 [-21.2, -2.1] | 53.1 | -4.1 | 23.2 | 35.6 | 25.6 | 73.4 | 81.5 |
| T19 qform=yn_compliant | 81 | 66.7 | 55.6 | -11.1 [-21.0, -1.3] | 56.8 | -9.9 | 17.5 | 30.1 | 27.1 | 83.7 | 83.7 |
| T19 qform=yn_fails | 31 | 71.0 | 61.3 | -9.7 [-25.0, +3.0] | 64.5 | -6.5 | 20.1 | 28.8 | 20.5 | 84.3 | 87.4 |
| T19 qform=yn_not_compliant | 18 | 55.6 | 44.4 | -11.1 [-47.1, +21.1] | 44.4 | -11.1 | 27.6 | 34.5 | 41.9 | 76.5 | 78.9 |
| T19 qform=yn_out_of | 15 | 53.3 | 53.3 | +0.0 [-20.0, +20.0] | 46.7 | -6.7 | 40.5 | 37.9 | 40.5 | 83.7 | 85.8 |
| T19 role=base | 161 | 60.9 | 52.2 | -8.7 [-16.1, -1.9] | 57.1 | -3.7 | 15.1 | 30.5 | 24.5 | 76.0 | 82.7 |
| T19 role=twin | 76 | 64.5 | 52.6 | -11.8 [-21.1, -2.6] | 53.9 | -10.5 | 14.9 | 32.3 | 31.2 | 78.4 | 84.1 |
| T19 role=equiv | 19 | 73.7 | 52.6 | -21.1 [-42.1, +0.0] | 57.9 | -15.8 | 16.4 | 34.9 | 23.0 | 75.1 | 84.2 |
| T19 role=complement | 32 | 56.2 | 43.8 | -12.5 [-25.0, -3.1] | 50.0 | -6.2 | 29.0 | 37.9 | 35.3 | 82.8 | 81.6 |
| T19 role=attack | 12 | 83.3 | 58.3 | -25.0 [-50.0, +0.0] | 66.7 | -16.7 | 26.3 | 29.0 | 20.6 | 73.4 | 82.2 |
| T21 qform=ch_clause | 163 | 66.3 | 69.9 | +3.7 [-2.4, +9.8] | 73.6 | +7.4 | 17.8 | 14.5 | 12.0 | 83.6 | 84.4 |
| T21 qform=yn_capped | 69 | 89.9 | 87.0 | -2.9 [-8.7, +2.8] | 89.9 | +0.0 | 4.0 | 7.7 | 6.1 | 92.2 | 91.3 |
| T21 qform=yn_free_of | 24 | 87.5 | 91.7 | +4.2 [+0.0, +13.6] | 91.7 | +4.2 | 7.0 | 3.5 | 2.9 | 92.0 | 92.0 |
| T21 qform=yn_not_capped | 21 | 76.2 | 81.0 | +4.8 [+0.0, +16.7] | 76.2 | +0.0 | 14.0 | 16.8 | 22.2 | 90.2 | 88.4 |
| T21 qform=yn_uncapped | 23 | 82.6 | 78.3 | -4.3 [-28.0, +15.4] | 82.6 | +0.0 | 11.3 | 12.9 | 15.2 | 89.7 | 88.0 |

### 4.2 T19 verdict rows: gold (rows) by predicted (columns)

Cells are counts of predictions Compliant / Non-compliant / Cannot be determined (CBD).

| Gold (verdict rows, n=98) | C1: pred Compl / Non-c / CBD | C2 a10 | C2 a05 | recall % C1 / a10 / a05 |
|---|---|---|---|---|
| Compl (n=39) | 12 / 5 / 22 | 3 / 3 / 33 | 7 / 4 / 28 | 30.8 / 7.7 / 17.9 |
| Non-c (n=33) | 3 / 21 / 9 | 0 / 16 / 17 | 0 / 21 / 12 | 63.6 / 48.5 / 63.6 |
| CBD (n=26) | 0 / 3 / 23 | 0 / 0 / 26 | 0 / 2 / 24 | 88.5 / 100.0 / 92.3 |
| **predicted total** | 15 / 29 / 54 | 3 / 19 / 76 | 7 / 27 / 64 |  |

C1: 54 CBD answers, 23 right (42.6% precision); C2a10: 76 CBD answers, 26 right (34.2% precision); C2a05: 64 CBD answers, 24 right (37.5% precision).

### 4.3 Where C2 loses T19 rows

| T19 format | n | C1 correct | a10 correct | rows lost (a10) | share of T19 loss | a05 correct | rows lost (a05) |
|---|---|---|---|---|---|---|---|
| choice verdict (has CBD option), n=98 | 98 | 56 | 45 | 11 | 32% | 52 | 4 |
| choice gap (control IDs, no abstain option), n=57 | 57 | 39 | 30 | 9 | 26% | 35 | 4 |
| yes/no (4 forms), n=145 | 145 | 94 | 80 | 14 | 41% | 81 | 13 |
| **T19 total** | 300 | 189 | 155 | 34 | 100% | 168 | 21 |

T19 (n=300): C1 right and a10 wrong 50, C1 wrong and a10 right 16, both right 139, both wrong 95. a10 false-CBD rows: 50; C1 was right on 16 of them. Mean confidence of a false CBD answer: C1 0.700 (n=31), a10 0.817 (n=50), a05 0.799 (n=40).

### 4.4 False-CBD rate by T19 slice (verdict rows whose gold is not CBD)

| Slice type | Value | verdict rows with gold != CBD | C1 says CBD | a10 says CBD | a05 says CBD |
|---|---|---|---|---|---|
| edge tag | unknown_out_of_scope | 69 | 43% | 70% | 57% |
| edge tag | expiry_boundary | 48 | 50% | 83% | 67% |
| edge tag | exclusion_decides | 45 | 49% | 73% | 62% |
| edge tag | expired_but_out_of_scope | 9 | 44% | 67% | 56% |
| edge tag | unknown_with_fail | 3 | 33% | 67% | 33% |
| sampler | S2 | 22 | 36% | 91% | 73% |
| sampler | S1 | 18 | 33% | 44% | 44% |
| sampler | S4 | 17 | 47% | 71% | 53% |
| sampler | S3 | 15 | 60% | 67% | 47% |
| role | base | 38 | 45% | 66% | 53% |
| role | twin | 23 | 48% | 74% | 57% |
| role | equiv | 7 | 43% | 86% | 71% |
| role | attack | 4 | 0% | 50% | 50% |
| format | audit_memo/text | 16 | 50% | 56% | 50% |
| format | auditor_email/text | 14 | 29% | 57% | 43% |
| format | report/text | 11 | 45% | 73% | 45% |
| format | audit_ticket/text | 9 | 56% | 78% | 56% |
| format | audit_chat/text | 8 | 50% | 88% | 75% |
| format | checklist_note/text | 8 | 25% | 75% | 75% |
| format | meeting_notes/text | 3 | 67% | 100% | 100% |
| format | site_wiki/text | 3 | 33% | 67% | 33% |
| depth | 2 | 68 | 41% | 68% | 54% |
| depth | 3 | 4 | 75% | 100% | 75% |

Edge tags overlap (a row can carry several), so the edge rows do not sum to the 72 non-CBD verdict rows. Depth 3 has only 4 rows.

## 5. Abstain-type answers versus truth

### 5.1 c2_mixdev (rows that offer an IND or ASK option)

| Family | Type | n rows with option | truth % | C1 % | a10 % | a05 % | a10 minus truth | false-abst C1 | a10 | a05 | missed-abst C1 | a10 | a05 | acc C1 | acc a10 | acc a05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F4 (trained) | IND | 12 | 33.3 | 75.0 | 41.7 | 58.3 | +8.3 | 62.5 | 25.0 | 50.0 | 0.0 | 25.0 | 25.0 | 58.3 | 75.0 | 58.3 |
| F6 (trained) | IND | 23 | 21.7 | 43.5 | 30.4 | 39.1 | +8.7 | 27.8 | 11.1 | 22.2 | 0.0 | 0.0 | 0.0 | 78.3 | 91.3 | 82.6 |
| T25 (trained) | IND | 53 | 35.8 | 54.7 | 34.0 | 37.7 | -1.9 | 38.2 | 0.0 | 11.8 | 15.8 | 5.3 | 15.8 | 67.9 | 94.3 | 84.9 |
| T28 (trained) | ASK | 47 | 36.2 | 29.8 | 36.2 | 36.2 | +0.0 | 23.3 | 10.0 | 20.0 | 58.8 | 17.6 | 35.3 | 55.3 | 80.9 | 70.2 |
| T29 (trained) | IND | 31 | 45.2 | 35.5 | 41.9 | 38.7 | -3.2 | 5.9 | 0.0 | 0.0 | 28.6 | 7.1 | 14.3 | 80.6 | 96.8 | 90.3 |
| T29 (trained) | ASK | 64 | 35.9 | 32.8 | 37.5 | 34.4 | +1.6 | 9.8 | 2.4 | 2.4 | 26.1 | 0.0 | 8.7 | 81.2 | 98.4 | 93.8 |
| T30 (trained) | ASK | 58 | 44.8 | 70.7 | 43.1 | 44.8 | -1.7 | 46.9 | 0.0 | 3.1 | 0.0 | 3.8 | 3.8 | 69.0 | 96.6 | 91.4 |
| T33 (NOT trained) | IND | 32 | 25.0 | 28.1 | 37.5 | 31.2 | +12.5 | 8.3 | 16.7 | 8.3 | 12.5 | 0.0 | 0.0 | 75.0 | 71.9 | 78.1 |
| mixdev trained (all rows with an IND or ASK option) | IND+ASK | 257 | 42.0 | 52.5 | 42.4 | 44.0 | +0.4 | 31.5 | 4.7 | 12.8 | 18.5 | 5.6 | 13.0 | 69.6 | 92.2 | 84.4 |
| mixdev not-trained | IND+ASK | 32 | 25.0 | 28.1 | 37.5 | 31.2 | +12.5 | 8.3 | 16.7 | 8.3 | 12.5 | 0.0 | 0.0 | 75.0 | 71.9 | 78.1 |
| transfer T19+T21 | IND+ASK | 98 | 26.5 | 55.1 | 77.6 | 65.3 | +51.0 | 43.1 | 69.4 | 55.6 | 11.5 | 0.0 | 7.7 | 57.1 | 45.9 | 53.1 |

Reading: in every trained family C2's abstain share lands within 9 pp of truth (largest gaps F4 +8.3 and F6 +8.7, on n of 12 and 23 rows); false-abstain collapses (T30 46.9% -> 0.0%, T25 38.2% -> 0.0%, F4 62.5% -> 25.0%). Rows with an ESC or NOTA option (secondary types):

| Family | Type | n rows with option | truth % | C1 % | a10 % | a05 % | a10 minus truth | false-abst C1 | a10 | a05 | missed-abst C1 | a10 | a05 | acc C1 | acc a10 | acc a05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F4 (trained) | NOTA | 11 | 0.0 | 18.2 | 0.0 | 9.1 | +0.0 | 18.2 | 0.0 | 9.1 | - | - | - | 54.5 | 90.9 | 72.7 |
| F6 (trained) | ESC | 19 | 36.8 | 36.8 | 36.8 | 36.8 | +0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 89.5 | 94.7 | 89.5 |
| F6 (trained) | NOTA | 8 | 12.5 | 0.0 | 0.0 | 0.0 | -12.5 | 0.0 | 0.0 | 0.0 | 100.0 | 100.0 | 100.0 | 87.5 | 87.5 | 87.5 |
| F11 (trained) | NOTA | 29 | 10.3 | 37.9 | 27.6 | 31.0 | +17.2 | 38.5 | 26.9 | 30.8 | 66.7 | 66.7 | 66.7 | 17.2 | 17.2 | 17.2 |
| T06 (trained) | NOTA | 70 | 42.9 | 12.9 | 28.6 | 15.7 | -14.3 | 5.0 | 2.5 | 0.0 | 76.7 | 36.7 | 63.3 | 51.4 | 75.7 | 62.9 |
| T12 (NOT trained) | NOTA | 10 | 40.0 | 30.0 | 10.0 | 20.0 | -30.0 | 33.3 | 0.0 | 16.7 | 75.0 | 75.0 | 75.0 | 40.0 | 60.0 | 60.0 |
| T15 (trained) | NOTA | 17 | 29.4 | 29.4 | 29.4 | 29.4 | +0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 | 100.0 | 100.0 |
| T26 (trained) | ESC | 49 | 30.6 | 32.7 | 30.6 | 30.6 | +0.0 | 2.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 93.9 | 100.0 | 100.0 |
| T30 (trained) | NOTA | 33 | 33.3 | 21.2 | 33.3 | 30.3 | +0.0 | 4.5 | 4.5 | 9.1 | 45.5 | 9.1 | 27.3 | 75.8 | 93.9 | 84.8 |
| T31 (trained) | ESC | 4 | 0.0 | 0.0 | 50.0 | 25.0 | +50.0 | 0.0 | 50.0 | 25.0 | - | - | - | 50.0 | 50.0 | 75.0 |

### 5.2 Transfer, older dev splits and yes/no

Transfer (T19 is the only transfer family with an abstain-type option; T21 has none):

| Family | Type | n rows with option | truth % | C1 % | a10 % | a05 % | a10 minus truth | false-abst C1 | a10 | a05 | missed-abst C1 | a10 | a05 | acc C1 | acc a10 | acc a05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T19 transfer | IND | 98 | 26.5 | 55.1 | 77.6 | 65.3 | +51.0 | 43.1 | 69.4 | 55.6 | 11.5 | 0.0 | 7.7 | 57.1 | 45.9 | 53.1 |

Older dev splits (abstain-type options are rare there; only rows with at least 10 such rows are shown, so most splits drop out):

| Family | Type | n rows with option | truth % | C1 % | a10 % | a05 % | a10 minus truth | false-abst C1 | a10 | a05 | missed-abst C1 | a10 | a05 | acc C1 | acc a10 | acc a05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dev | NOTA | 150 | 0.0 | 1.3 | 1.3 | 1.3 | +1.3 | 1.3 | 1.3 | 1.3 | - | - | - | 91.3 | 91.3 | 90.7 |
| dev_claims | IND | 27 | 11.1 | 22.2 | 22.2 | 22.2 | +11.1 | 12.5 | 12.5 | 12.5 | 0.0 | 0.0 | 0.0 | 88.9 | 88.9 | 88.9 |
| dev_claims | NOTA | 150 | 0.0 | 0.0 | 1.3 | 0.0 | +1.3 | 0.0 | 1.3 | 0.0 | - | - | - | 94.7 | 93.3 | 94.7 |
| devp_card | IND | 45 | 11.1 | 22.2 | 20.0 | 20.0 | +8.9 | 12.5 | 10.0 | 10.0 | 0.0 | 0.0 | 0.0 | 88.9 | 91.1 | 91.1 |
| devp_card | NOTA | 240 | 0.0 | 0.8 | 1.2 | 0.8 | +1.2 | 0.8 | 1.2 | 0.8 | - | - | - | 90.8 | 91.2 | 90.0 |
| hard_dev | NOTA | 47 | 23.4 | 21.3 | 12.8 | 17.0 | -10.6 | 11.1 | 2.8 | 5.6 | 45.5 | 54.5 | 45.5 | 72.3 | 78.7 | 78.7 |
| pg_dev | IND | 44 | 38.6 | 20.5 | 22.7 | 22.7 | -15.9 | 0.0 | 0.0 | 0.0 | 47.1 | 41.2 | 41.2 | 63.6 | 63.6 | 68.2 |
| pg_dev | ESC | 31 | 45.2 | 38.7 | 35.5 | 38.7 | -9.7 | 17.6 | 17.6 | 23.5 | 35.7 | 42.9 | 42.9 | 71.0 | 61.3 | 64.5 |

Yes/no rows: predicted-yes rate against truth and hedged share (confidence below 0.6). The largest C1-to-a10 shift in predicted-yes rate is 13.8 pp (T12, not trained); C2 moves the trained families toward truth (F11 33.0% -> 43.6% vs truth 51.1%; T06 45.5% -> 53.0%; T25 55.2% -> 41.8% vs 40.3%). On T19 the yes-rate stays near truth (49.0% / 51.0% / 52.4%).

| Family | n yes/no | truth yes % | C1 yes % | a10 yes % | a05 yes % | C1 conf<0.6 % | a10 conf<0.6 % | acc C1 | acc a10 |
|---|---|---|---|---|---|---|---|---|---|
| F4 (trained) | 77 | 58.4 | 48.1 | 51.9 | 46.8 | 11.7 | 7.8 | 66.2 | 70.1 |
| F5 (trained) | 400 | 50.0 | 48.2 | 48.2 | 48.5 | 2.5 | 1.0 | 84.2 | 83.2 |
| F6 (trained) | 200 | 49.5 | 40.0 | 49.5 | 45.0 | 7.5 | 15.5 | 65.5 | 75.0 |
| F11 (trained) | 188 | 51.1 | 33.0 | 43.6 | 34.6 | 14.9 | 18.6 | 51.1 | 57.4 |
| T01 (trained) | 58 | 51.7 | 46.6 | 51.7 | 50.0 | 10.3 | 6.9 | 91.4 | 96.6 |
| T06 (trained) | 66 | 50.0 | 45.5 | 53.0 | 45.5 | 7.6 | 1.5 | 53.0 | 78.8 |
| T07 (NOT trained) | 85 | 47.1 | 45.9 | 47.1 | 47.1 | 1.2 | 2.4 | 96.5 | 90.6 |
| T12 (NOT trained) | 87 | 50.6 | 63.2 | 49.4 | 56.3 | 20.7 | 17.2 | 64.4 | 55.2 |
| T15 (trained) | 75 | 48.0 | 50.7 | 49.3 | 48.0 | 1.3 | 0.0 | 92.0 | 98.7 |
| T23 (trained) | 54 | 44.4 | 44.4 | 51.9 | 46.3 | 3.7 | 1.9 | 88.9 | 85.2 |
| T24 (NOT trained) | 79 | 46.8 | 59.5 | 62.0 | 60.8 | 20.3 | 8.9 | 64.6 | 62.0 |
| T25 (trained) | 67 | 40.3 | 55.2 | 41.8 | 46.3 | 9.0 | 1.5 | 70.1 | 95.5 |
| T26 (trained) | 80 | 52.5 | 45.0 | 52.5 | 52.5 | 1.2 | 0.0 | 92.5 | 100.0 |
| T28 (trained) | 72 | 50.0 | 52.8 | 50.0 | 54.2 | 2.8 | 1.4 | 58.3 | 88.9 |
| T29 (trained) | 72 | 48.6 | 50.0 | 47.2 | 47.2 | 5.6 | 0.0 | 84.7 | 95.8 |
| T30 (trained) | 75 | 53.3 | 50.7 | 53.3 | 52.0 | 9.3 | 1.3 | 65.3 | 97.3 |
| T31 (trained) | 95 | 53.7 | 54.7 | 51.6 | 51.6 | 8.4 | 0.0 | 63.2 | 85.3 |
| T33 (NOT trained) | 71 | 50.7 | 47.9 | 47.9 | 45.1 | 8.5 | 8.5 | 85.9 | 85.9 |
| T19 transfer | 145 | 49.0 | 51.0 | 52.4 | 54.5 | 7.6 | 5.5 | 64.8 | 55.2 |
| T21 transfer | 137 | 48.2 | 50.4 | 49.6 | 51.1 | 0.0 | 0.0 | 86.1 | 85.4 |
| general dev pooled | 4329 | 50.0 | 50.5 | 50.9 | 50.6 | 6.6 | 5.1 | 85.2 | 85.0 |

### 5.3 Calibration detail

Reliability (confidence bins; n, mean confidence, accuracy), C1 vs a10:

**T19 (n=300)**

| conf bin | C1 n | C1 conf | C1 acc | a10 n | a10 conf | a10 acc |
|---|---|---|---|---|---|---|
| 0.3-0.4 | 3 | 36.9 | 33.3 | 0 | - | - |
| 0.4-0.5 | 11 | 47.4 | 36.4 | 4 | 46.4 | 0.0 |
| 0.5-0.6 | 33 | 55.6 | 45.5 | 15 | 54.2 | 40.0 |
| 0.6-0.7 | 42 | 65.0 | 59.5 | 26 | 66.0 | 50.0 |
| 0.7-0.8 | 59 | 75.9 | 64.4 | 40 | 74.8 | 42.5 |
| 0.8-0.9 | 88 | 86.0 | 65.9 | 107 | 86.1 | 43.9 |
| 0.9-1.0 | 64 | 92.3 | 75.0 | 108 | 92.4 | 66.7 |

**mixdev, 14 trained families (n=2,795)**

| conf bin | C1 n | C1 conf | C1 acc | a10 n | a10 conf | a10 acc |
|---|---|---|---|---|---|---|
| 0.0-0.1 | 8 | 8.9 | 0.0 | 4 | 9.7 | 0.0 |
| 0.1-0.2 | 78 | 15.9 | 12.8 | 57 | 15.4 | 10.5 |
| 0.2-0.3 | 55 | 24.9 | 9.1 | 53 | 25.2 | 15.1 |
| 0.3-0.4 | 47 | 36.1 | 25.5 | 52 | 35.4 | 25.0 |
| 0.4-0.5 | 89 | 45.0 | 36.0 | 40 | 44.2 | 37.5 |
| 0.5-0.6 | 243 | 55.0 | 44.9 | 147 | 55.4 | 46.9 |
| 0.6-0.7 | 238 | 64.7 | 50.4 | 144 | 65.1 | 53.5 |
| 0.7-0.8 | 299 | 75.3 | 63.2 | 207 | 75.5 | 61.4 |
| 0.8-0.9 | 617 | 85.7 | 68.7 | 405 | 85.8 | 75.1 |
| 0.9-1.0 | 1121 | 93.8 | 89.0 | 1686 | 94.5 | 96.3 |

**general dev choice rows (n=3,814)**

| conf bin | C1 n | C1 conf | C1 acc | a10 n | a10 conf | a10 acc |
|---|---|---|---|---|---|---|
| 0.0-0.1 | 1 | 9.2 | 0.0 | 0 | - | - |
| 0.1-0.2 | 7 | 17.6 | 14.3 | 3 | 14.8 | 33.3 |
| 0.2-0.3 | 33 | 25.4 | 27.3 | 28 | 27.3 | 25.0 |
| 0.3-0.4 | 171 | 35.6 | 39.8 | 114 | 35.9 | 34.2 |
| 0.4-0.5 | 243 | 45.2 | 43.2 | 174 | 45.5 | 40.2 |
| 0.5-0.6 | 325 | 55.0 | 55.1 | 227 | 55.1 | 52.9 |
| 0.6-0.7 | 299 | 64.9 | 55.5 | 218 | 64.9 | 50.5 |
| 0.7-0.8 | 366 | 75.2 | 65.8 | 288 | 75.2 | 57.6 |
| 0.8-0.9 | 594 | 85.4 | 79.8 | 534 | 85.9 | 64.0 |
| 0.9-1.0 | 1775 | 94.8 | 95.9 | 2228 | 94.8 | 92.5 |

Sharpening (share of rows with confidence >= 0.9 and the accuracy there):

| Set | n | C1 mean conf | C1 acc | C1 share conf>=0.9 | C1 acc at >=0.9 | a10 mean conf | a10 acc | a10 share conf>=0.9 | a10 acc at >=0.9 |
|---|---|---|---|---|---|---|---|---|---|
| general dev yes/no | 4329 | 85.0 | 85.2 | 51.5 | 96.1 | 87.4 | 85.0 | 62.3 | 94.1 |
| general dev choice | 3814 | 79.2 | 77.2 | 46.5 | 95.9 | 83.5 | 76.5 | 58.4 | 92.5 |
| mixdev trained yes/no | 1579 | 84.0 | 73.0 | 44.6 | 89.5 | 86.6 | 82.6 | 61.0 | 95.2 |
| mixdev trained choice | 1216 | 70.0 | 61.3 | 34.2 | 88.2 | 79.2 | 77.2 | 59.5 | 97.8 |
| T19 | 300 | 77.2 | 63.0 | 21.3 | 75.0 | 83.0 | 51.7 | 36.0 | 66.7 |
| T21 | 300 | 87.2 | 75.3 | 64.0 | 90.1 | 87.2 | 77.0 | 61.3 | 92.9 |

ECE by split and question type:

| Split | type | n | ECE C1 | ECE a10 | ECE a05 | acc C1 | acc a10 |
|---|---|---|---|---|---|---|---|
| dev | noul | 450 | 4.7 | 2.8 | 4.5 | 88.9 | 90.0 |
| dev | choice | 150 | 8.5 | 5.7 | 5.6 | 91.3 | 91.3 |
| dev_claims | noul | 450 | 3.8 | 2.7 | 2.3 | 87.8 | 85.8 |
| dev_claims | choice | 300 | 3.1 | 5.8 | 4.3 | 89.0 | 89.7 |
| dev_nc | choice | 1008 | 3.3 | 8.2 | 4.9 | 76.6 | 75.0 |
| dev_negwords | noul | 800 | 3.4 | 3.5 | 4.3 | 87.4 | 88.1 |
| devp_card | noul | 1116 | 2.4 | 4.4 | 3.6 | 86.5 | 85.8 |
| devp_card | choice | 612 | 4.5 | 4.5 | 5.6 | 86.8 | 87.4 |
| devzs | noul | 600 | 4.6 | 8.5 | 6.5 | 80.7 | 78.7 |
| devzs | choice | 200 | 13.5 | 18.6 | 17.1 | 67.5 | 67.0 |
| hard_dev | noul | 100 | 6.3 | 3.2 | 5.5 | 85.0 | 86.0 |
| hard_dev | choice | 108 | 9.3 | 10.9 | 9.7 | 74.1 | 75.0 |
| pg_dev | noul | 303 | 1.6 | 3.5 | 3.0 | 75.2 | 74.6 |
| pg_dev | choice | 746 | 2.8 | 6.4 | 4.4 | 62.2 | 60.1 |
| taskbank_dev | noul | 510 | 8.0 | 4.8 | 6.8 | 84.7 | 86.3 |
| taskbank_dev | choice | 690 | 7.0 | 11.4 | 9.5 | 81.0 | 80.6 |
| c2_t37b_dev | noul | 600 | 4.1 | 6.7 | 6.5 | 83.7 | 81.8 |
| c2_transfer_dev | noul | 282 | 12.9 | 17.3 | 16.0 | 75.2 | 69.9 |
| c2_transfer_dev | choice | 318 | 14.1 | 23.8 | 16.2 | 63.8 | 59.4 |
| c2_mixdev | noul | 1901 | 9.3 | 5.6 | 5.3 | 73.8 | 81.0 |
| c2_mixdev | choice | 1485 | 9.1 | 4.7 | 5.1 | 62.4 | 75.6 |

Temperature check. T is fitted by NLL (grid 0.5 to 4.0, step 0.05) per model and question type on the 2,795 trained-family mixdev rows, then applied unchanged. This is an approximation of the L1 recipe named in `C2_REPORT.md:147`, not the L1 code, and it is not the frozen T of the sealed look.

| Model | T (yes/no) | T (choice) |
|---|---|---|
| C1 | 1.55 | 1.35 |
| C2a10 | 1.10 | 1.05 |
| C2a05 | 1.15 | 1.10 |

| Set | n | ECE raw C1 | raw a10 | raw a05 | ECE after T: C1 | a10 | a05 |
|---|---|---|---|---|---|---|---|
| mixdev trained (fit set) | 2795 | 9.9 | 5.4 | 5.0 | 4.5 | 5.1 | 5.2 |
| mixdev not trained | 591 | 7.0 | 12.7 | 9.3 | 3.5 | 11.3 | 7.0 |
| general dev pooled | 8143 | 2.9 | 4.6 | 3.4 | 7.4 | 4.5 | 3.8 |
| c2_t37b_dev | 600 | 4.1 | 6.7 | 6.5 | 8.8 | 7.4 | 7.1 |
| T19 | 300 | 14.2 | 31.4 | 25.1 | 7.7 | 29.8 | 22.6 |
| T21 | 300 | 12.1 | 10.2 | 8.7 | 9.7 | 12.5 | 9.5 |
| T19+T21 | 600 | 13.0 | 20.8 | 16.1 | 6.4 | 19.2 | 13.6 |

The fit set is in-distribution for C2 and out-of-distribution for C1, so the two models get very different Ts (1.55 vs 1.10). C1's T is wrong for the other sets; a10's T leaves T19 and the not-trained families overconfident. Calibration learned on trained families does not carry to unseen ones.

## 6. Which training blocks plausibly drove the over-abstention

### 6.1 Abstain-type gold in the C2 training mix

Cells are gold-of-that-type / rows-that-offer-that-type (share). Sorted by IND+ASK gold rows. "replay" is all 35,604 replay rows (118 sources: `gd_*`, `pg_*` and similar).

| Training block | rows | choice rows | IND gold / rows with IND option | ASK gold / rows with ASK option | ESC gold / opt | NOTA gold / opt | IND+ASK gold rows | % of block rows |
|---|---|---|---|---|---|---|---|---|
| T29 | 2000 | 1037 | 143/550 (26%) | 218/801 (27%) | 0/0 (-) | 0/0 (-) | 361 | 18.1% |
| replay | 35604 | 12301 | 251/960 (26%) | 23/286 (8%) | 2/4 (50%) | 168/446 (38%) | 274 | 0.8% |
| T30 | 1400 | 770 | 0/0 (-) | 242/608 (40%) | 0/0 (-) | 126/377 (33%) | 242 | 17.3% |
| T28 | 2247 | 1154 | 0/0 (-) | 241/732 (33%) | 0/0 (-) | 0/0 (-) | 241 | 10.7% |
| T25 | 600 | 330 | 84/238 (35%) | 0/0 (-) | 0/0 (-) | 0/0 (-) | 84 | 14.0% |
| F6 | 930 | 389 | 1/11 (9%) | 0/0 (-) | 7/54 (13%) | 3/28 (11%) | 1 | 0.1% |
| T26 | 1398 | 766 | 0/0 (-) | 0/0 (-) | 136/453 (30%) | 0/0 (-) | 0 | 0.0% |
| T31 | 999 | 457 | 0/0 (-) | 0/0 (-) | 31/82 (38%) | 0/0 (-) | 0 | 0.0% |
| T01 | 1600 | 720 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0 | 0.0% |
| T23 | 794 | 421 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0 | 0.0% |
| T06 | 600 | 330 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 80/234 (34%) | 0 | 0.0% |
| T15 | 900 | 489 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 19/97 (20%) | 0 | 0.0% |
| F5 | 1362 | 0 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0 | 0.0% |
| F11 | 552 | 240 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0 | 0.0% |
| F4 | 500 | 270 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 6/37 (16%) | 0 | 0.0% |
| GB | 3376 | 1542 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0 | 0.0% |
| GW | 3696 | 1667 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0 | 0.0% |
| I10 | 100 | 100 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0 | 0.0% |
| SB5 | 682 | 0 | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0/0 (-) | 0 | 0.0% |
| **TOTAL** | 59340 | 22983 | 479/1759 (27%) | 724/2427 (30%) | 176/593 (30%) | 402/1219 (33%) | 1203 | 2.0% |

IND-gold share among rows that offer an IND option: new rows 28.5% (228/799), replay 26.1% (251/960), all 27.2%. T19 dev truth: 26/98 = 26.5%.

Replay sources with the most IND gold (all offer the IND option as the last option in 927 of 960 replay IND-option rows):

| Replay source | rows with IND option | IND gold | share |
|---|---|---|---|
| gd_boardgameqa | 337 | 126 | 37% |
| gd_logicinference | 158 | 36 | 23% |
| gd_babi_logic | 75 | 33 | 44% |
| gd_gen_evidence_conflict | 57 | 16 | 28% |
| gd_gen_tables | 44 | 14 | 32% |
| gd_gen2_json_fields | 36 | 12 | 33% |
| gd_gen_policy_exceptions | 35 | 9 | 26% |
| gd_gen_ranking | 211 | 5 | 2% |

### 6.2 Surface similarity to T19 (TF-IDF, word 1-2 grams, top-20 neighbours per T19 row)

Proxy only (mean top-20 cosine 0.10, so similarity is low everywhere). Neighbours come from training rows of any type.

| Training block | rows | share of mix | share of T19 top-20 neighbours | enrichment | neighbours with IND/ASK gold |
|---|---|---|---|---|---|
| T01 | 1600 | 2.7% | 68.5% | 25.41x | 0.0% |
| replay | 35604 | 60.0% | 11.3% | 0.19x | 0.0% |
| T25 | 600 | 1.0% | 8.9% | 8.80x | 8.1% |
| T23 | 794 | 1.3% | 6.3% | 4.73x | 0.0% |
| T30 | 1400 | 2.4% | 1.5% | 0.64x | 0.0% |
| F4 | 500 | 0.8% | 1.4% | 1.72x | 0.0% |
| T06 | 600 | 1.0% | 1.1% | 1.09x | 0.0% |
| T29 | 2000 | 3.4% | 0.3% | 0.09x | 15.8% |
| GB | 3376 | 5.7% | 0.2% | 0.04x | 0.0% |
| F6 | 930 | 1.6% | 0.2% | 0.12x | 0.0% |

Reading: T19's surface (control IDs, "evidence valid for N days", dates) is closest to T01 and T23 (date and window arithmetic), which carry no abstain option at all. Among blocks that do teach abstention, only T25 is a near neighbour. C2 never saw expiry-window arithmetic paired with a Cannot-be-determined option and a resolvable gold, which is exactly the T19 verdict row. This is an inference from the mix contents, not a measurement.

### 6.3 How the abstain share moved per family against what the mix taught

| Dev family | Type | Training gold/option rows (share) | dev n | dev truth % | C1 pred % | a10 pred % | a10 minus C1 (pp) |
|---|---|---|---|---|---|---|---|
| T29 | IND | 143/550 (26%) | 31 | 45.2 | 35.5 | 41.9 | +6.5 |
| T29 | ASK | 218/801 (27%) | 64 | 35.9 | 32.8 | 37.5 | +4.7 |
| T25 | IND | 84/238 (35%) | 53 | 35.8 | 54.7 | 34.0 | -20.8 |
| T28 | ASK | 241/732 (33%) | 47 | 36.2 | 29.8 | 36.2 | +6.4 |
| T30 | ASK | 242/608 (40%) | 58 | 44.8 | 70.7 | 43.1 | -27.6 |
| F4 | IND | 0/0 (-) | 12 | 33.3 | 75.0 | 41.7 | -33.3 |
| F6 | IND | 1/11 (9%) | 23 | 21.7 | 43.5 | 30.4 | -13.0 |
| T33 | IND | not in mix | 32 | 25.0 | 28.1 | 37.5 | +9.4 |

Where C1 was below truth and the block teaches abstention (T28, T29), C2 moved up (+4.7 to +6.5 pp). Where C1 was above truth (T25, T30, F4, F6) C2 moved down by 13 to 33 pp. The common shape: C2 learned the per-family abstain prior of the trained blocks. C1: Not-shown answers 9 of 32 ; C2a10: Not-shown answers 12 of 32 ; C2a05: Not-shown answers 10 of 32; gold "Not shown" in 8 of 32.

### 6.4 Dose-response over the 19 reads (transfer set)

Candidates are merged-weight blends of C1 and C2 (`C2_REPORT.md:77`): final step, last-3 average, and early+late average (early = checkpoint s001212, about one third of the 3,673 steps), each at alpha 0.5 to 1.0.

| Model (merged-weight alpha x10) | T19 verdict rows answered CBD (of 98; truth 26) | T19 acc | T21 acc | transfer acc |
|---|---|---|---|---|
| C1 (alpha 0) | 54 | 63.0 | 75.3 | 69.2 |
| final_a05 | 64 | 56.0 | 79.7 | 67.8 |
| final_a06 | 67 | 54.7 | 78.3 | 66.5 |
| final_a07 | 68 | 53.0 | 79.3 | 66.2 |
| final_a08 | 72 | 54.0 | 78.7 | 66.3 |
| final_a09 | 75 | 52.0 | 78.0 | 65.0 |
| final_a10 | 76 | 51.7 | 77.0 | 64.3 |
| last3_a05 | 64 | 55.7 | 80.0 | 67.8 |
| last3_a06 | 67 | 54.7 | 78.3 | 66.5 |
| last3_a07 | 69 | 53.0 | 79.7 | 66.3 |
| last3_a08 | 72 | 54.0 | 79.3 | 66.7 |
| last3_a09 | 75 | 52.3 | 77.7 | 65.0 |
| last3_a10 | 77 | 52.0 | 77.3 | 64.7 |
| earlylate_a05 | 69 | 53.7 | 80.3 | 67.0 |
| earlylate_a06 | 72 | 51.7 | 79.7 | 65.7 |
| earlylate_a07 | 73 | 51.0 | 80.3 | 65.7 |
| earlylate_a08 | 78 | 48.7 | 80.3 | 64.5 |
| earlylate_a09 | 80 | 47.3 | 81.0 | 64.2 |
| earlylate_a10 | 80 | 46.7 | 82.0 | 64.3 |

CBD answers rise almost linearly with alpha (54 at alpha 0, 64 at 0.5, 76 at 1.0, i.e. about +2.2 per 0.1 of alpha), in line with the report's note that the trade is nearly linear in alpha (`C2_REPORT.md:143`). The early+late blends are at least as over-abstaining as the final step (80 vs 76 at alpha 1.0), so the shift is already present in the weights by about step 1,212 and does not come from a late-training tail. (Inference: early+late is an average, not an early-only read.)

### 6.5 Ranking and confidence

| Rank | Block | Evidence for | Evidence against | Confidence |
|---|---|---|---|---|
| 1 | T29 | 361 abstain-gold rows (143 IND + 218 ASK); verdict menu shaped like T19; C2 raised its abstain rate +4.7 to +6.5 pp on T29 dev | Dev abstain rate equals truth, so on T29 itself C2 is right | medium |
| 2 | T25 | highest IND-gold rate of any new block (84/238 = 35%); 8.8x enriched among T19's neighbours and the only abstain-bearing one | only 84 IND-gold rows (0.14% of the mix); C2 cut T25 false-abstain 38.2% -> 0.0% | medium-low |
| 3 | T28, T30 | 241 and 242 ASK-gold rows | ASK is not the CBD label; T30 false-abstain fell 46.9% -> 0.0% | low |
| 4 | replay boardgameqa, logicinference, babi_logic | 195 "unknown" golds (3-way proved / disproved / unknown logic) | KD 0.5 to the C1 anchor on replay; C1 already over-abstained before training | low |
| - | F4, F6, T26, T31, T01, T23, T06, T15, F5, F11, GB, GW, I10, SB5 | none | 0 to 1 IND/ASK gold rows; T26/T31 teach ESC only | not supported |

A hypothesis (not tested) that fits all the numbers better than any single block: C1 already over-abstained on T19; training on blocks whose abstain-option rows carry an abstain gold 33% to 45% of the time (T29 45%, T30 40%, T25 35%, T28 33%) sharpened the model's rule-and-verdict machinery without a contrast case that shows a resolvable verdict next to a "missing-looking" fact. The model then reads a lapsed or missing record on a compliance checklist as undetermined. T19's own rule says no evidence on file means the control fails, and only an unrecorded evidence date means unknown, so that reading is wrong.

## 7. Caveats and what is UNVERIFIED

- **UNVERIFIED (causal attribution).** Section 6 is correlation across one training run. There is no ablation (a C2 trained without T29, T25 or the logic replay) and no per-block snapshot read. The cheapest check would be reading the saved snapshots (25%, 33%, 50%, 67%, 75%, 83%, 92%; `c2_build/train/README.md:10`) on the 98 T19 verdict rows, plus one small ablation on the free credit. I did not run either (Modal is training-only per owner rule, and the task was read-only).
- **UNVERIFIED (mechanism).** The reading of a missing or lapsed record as "undetermined" is an inference from the confusion matrix and the edge breakdown (expiry_boundary 83% false-CBD), not from inspecting the model.
- **Small cells.** F4 IND n 12, F6 IND n 23, T33 IND n 32, T19 edge cells 3 to 70 rows. Twins and equivalents are correlated, which is why CIs are cluster-based. Edge-tag rows overlap.
- **Classifier choices.** "Not shown in the log" and "maybe" count as IND; slot-specific "Ask for X" and "Escalate to NAME" do not count as abstain in the headline numbers (ESC and NOTA shown separately). The F4 dev IND option ("cannot be determined from the record") has no counterpart in F4 training (0 IND options there; 37 NOTA), so F4's false-abstain drop 62.5% -> 25.0% came without direct label exposure (n 12).
- **Dev, not sealed.** T19 dev is a 300-row sample (98 verdict rows). The sealed OHS-4 figures quoted in the task (part R +1.93 pp, ECE 4.1% vs 13.2%, Brier +0.0098) were not opened or recomputed. The dev pattern agrees in sign: C2 overconfident out of distribution, better in distribution.
- **Alpha and T19.** Alpha 0.5 removes about 40% of the T19 loss (-7.0 vs -11.3) and keeps 78% of the trained gain (+9.6 vs +12.3 on mixdev), but still answers CBD 64 times and has ECE 25.1 on T19.

## 8. What this implies for C2.1 (data design only; no bar is changed)

1. Add **contrast sets for every abstain label**: same surface, same options, one fact toggled so the gold flips between a resolvable verdict and CBD. Keep CBD gold at about 25% to 30% of rows per family (the mix averages 27.2%, which is right; the problem is cues, not frequency). For T19-style families the toggle is "no evidence on file" (fails) versus "evidence date not recorded" (unknown) versus "evidence expired by one day" (fails). Today T01 and T23 carry date windows with no abstain option, and T25/T29 carry abstain with no windows.
2. Do not add more T29/T28/T30 volume without those contrasts: they already supply 844 ASK/IND-gold rows (70% of all abstain gold in the mix).
3. Put a **held-out-by-structure verdict family** and its ECE into selection. The report already says S cannot see transfer (`C2_REPORT.md:162`). On dev, S-style selection rises with alpha while T19 CBD count and ECE rise with it too.
4. Treat the **ECE jump on choice rows** (general dev 3.4 -> 7.0; 0.8-0.9 bin 85.9% confident, 64.0% accurate) as a separate defect from abstention. It also appears in splits that have no abstain option (dev_nc 3.3 -> 8.2, taskbank choice 7.0 -> 11.4, pg_dev choice 2.8 -> 6.4). Mixdev-fitted temperature will not fix it (section 5.3).
5. Check the yes/no side of any new family: T19 yes/no lost -9.7 pp with no label bias, so a verdict-format fix alone would recover at most about a third of the T19 loss (11 of 34 rows).

## Appendix A. Older dev splits by source (n >= 30)

| Split | Source / family | n | C1 | a10 | a10 minus C1 | a05 | ECE C1 | ECE a10 | ECE a05 |
|---|---|---|---|---|---|---|---|---|---|
| dev | banking77 | 228 | 85.5 | 86.4 | +0.9 | 86.0 | 6.3 | 3.7 | 6.0 |
| dev | clinc150 | 372 | 91.9 | 92.7 | +0.8 | 92.2 | 4.7 | 3.2 | 4.4 |
| dev_claims | banking77 | 117 | 82.9 | 84.6 | +1.7 | 82.9 | 7.9 | 7.9 | 8.2 |
| dev_claims | bbc | 39 | 100.0 | 100.0 | +0.0 | 100.0 | 6.1 | 5.7 | 5.5 |
| dev_claims | cb | 57 | 94.7 | 89.5 | -5.3 | 93.0 | 15.3 | 6.8 | 11.0 |
| dev_claims | climate | 60 | 73.3 | 75.0 | +1.7 | 75.0 | 18.6 | 18.4 | 17.4 |
| dev_claims | clinc150 | 183 | 96.7 | 96.2 | -0.5 | 96.7 | 5.2 | 3.1 | 4.0 |
| dev_claims | hate | 81 | 61.7 | 53.1 | -8.6 | 56.8 | 24.0 | 30.6 | 24.0 |
| dev_claims | irony | 69 | 89.9 | 89.9 | +0.0 | 89.9 | 12.9 | 6.0 | 7.4 |
| dev_claims | rotten_tomatoes | 84 | 94.0 | 95.2 | +1.2 | 95.2 | 4.4 | 2.3 | 2.4 |
| dev_claims | spam | 60 | 100.0 | 100.0 | +0.0 | 100.0 | 7.2 | 5.6 | 6.1 |
| dev_nc | btzsc_appreviews | 112 | 91.1 | 91.1 | +0.0 | 91.1 | 5.9 | 4.6 | 4.4 |
| dev_nc | btzsc_biasframes_intent | 112 | 85.7 | 79.5 | -6.2 | 85.7 | 6.9 | 6.9 | 9.4 |
| dev_nc | btzsc_biasframes_offensive | 112 | 88.4 | 83.9 | -4.5 | 87.5 | 3.7 | 4.9 | 4.5 |
| dev_nc | btzsc_biasframes_sex | 112 | 92.0 | 92.9 | +0.9 | 91.1 | 5.5 | 5.3 | 3.8 |
| dev_nc | btzsc_capsotu | 112 | 70.5 | 72.3 | +1.8 | 70.5 | 6.6 | 9.1 | 8.9 |
| dev_nc | btzsc_empathetic | 112 | 46.4 | 44.6 | -1.8 | 47.3 | 12.4 | 19.0 | 16.1 |
| dev_nc | btzsc_financialphrasebank | 112 | 93.8 | 89.3 | -4.5 | 91.1 | 12.7 | 7.8 | 6.8 |
| dev_nc | btzsc_manifesto | 112 | 42.9 | 44.6 | +1.8 | 43.8 | 16.0 | 28.1 | 26.0 |
| dev_nc | btzsc_trueteacher | 112 | 78.6 | 76.8 | -1.8 | 80.4 | 6.6 | 14.8 | 12.9 |
| dev_negwords | banking77 | 114 | 87.7 | 87.7 | +0.0 | 87.7 | 6.0 | 3.8 | 4.6 |
| dev_negwords | bbc | 36 | 100.0 | 100.0 | +0.0 | 100.0 | 6.4 | 6.0 | 5.9 |
| dev_negwords | cb | 54 | 94.4 | 94.4 | +0.0 | 96.3 | 12.2 | 8.4 | 11.9 |
| dev_negwords | climate | 90 | 75.6 | 78.9 | +3.3 | 80.0 | 4.4 | 8.8 | 7.1 |
| dev_negwords | clinc150 | 186 | 91.9 | 91.9 | +0.0 | 93.0 | 5.6 | 3.2 | 4.9 |
| dev_negwords | hate | 78 | 64.1 | 65.4 | +1.3 | 67.9 | 14.0 | 17.7 | 18.5 |
| dev_negwords | irony | 82 | 84.1 | 84.1 | +0.0 | 86.6 | 8.1 | 7.4 | 7.7 |
| dev_negwords | rotten_tomatoes | 70 | 94.3 | 97.1 | +2.9 | 95.7 | 10.9 | 6.2 | 8.8 |
| dev_negwords | spam | 90 | 97.8 | 97.8 | +0.0 | 97.8 | 5.0 | 3.6 | 4.1 |
| devp_card | banking77 | 100 | 86.0 | 85.0 | -1.0 | 83.0 | 11.6 | 8.9 | 13.7 |
| devp_card | bbc | 108 | 100.0 | 100.0 | +0.0 | 100.0 | 6.1 | 5.6 | 5.4 |
| devp_card | cb | 180 | 93.3 | 93.3 | +0.0 | 92.8 | 12.9 | 8.7 | 11.0 |
| devp_card | climate | 240 | 76.7 | 77.1 | +0.4 | 78.3 | 5.7 | 8.1 | 7.9 |
| devp_card | clinc150 | 140 | 94.3 | 95.7 | +1.4 | 95.0 | 6.3 | 3.6 | 3.9 |
| devp_card | hate | 240 | 64.6 | 65.0 | +0.4 | 65.4 | 17.5 | 18.2 | 16.9 |
| devp_card | irony | 240 | 86.7 | 83.3 | -3.3 | 85.8 | 8.5 | 5.4 | 5.2 |
| devp_card | rotten_tomatoes | 240 | 91.2 | 92.1 | +0.8 | 92.5 | 7.2 | 5.4 | 4.9 |
| devp_card | spam | 240 | 98.3 | 98.3 | +0.0 | 98.3 | 5.7 | 4.2 | 4.7 |
| devzs | ag_news | 400 | 93.2 | 91.2 | -2.0 | 92.0 | 4.0 | 4.9 | 3.3 |
| devzs | emotion | 400 | 61.5 | 60.2 | -1.2 | 61.0 | 15.8 | 20.9 | 19.5 |
| pg_dev | pg_conflict | 150 | 73.3 | 70.0 | -3.3 | 73.3 | 6.7 | 8.6 | 7.2 |
| pg_dev | pg_evidence | 150 | 65.3 | 66.7 | +1.3 | 66.0 | 5.8 | 5.9 | 2.6 |
| pg_dev | pg_multihop | 150 | 56.7 | 58.7 | +2.0 | 60.0 | 8.0 | 18.1 | 13.3 |
| pg_dev | pg_numeric | 150 | 50.7 | 48.0 | -2.7 | 51.3 | 7.5 | 8.3 | 8.0 |
| pg_dev | pg_policy | 150 | 74.0 | 78.7 | +4.7 | 74.7 | 7.5 | 9.0 | 5.5 |
| pg_dev | pg_routing | 150 | 72.0 | 64.7 | -7.3 | 66.0 | 7.4 | 11.0 | 7.0 |
| pg_dev | pg_temporal | 149 | 69.8 | 63.1 | -6.7 | 66.4 | 12.0 | 8.9 | 9.5 |
| taskbank_dev | tb_label_nli | 113 | 71.7 | 73.5 | +1.8 | 70.8 | 9.8 | 11.9 | 10.4 |
| taskbank_dev | tb_mixtral | 1087 | 83.7 | 84.0 | +0.3 | 83.8 | 5.9 | 8.3 | 7.3 |
| c2_t37b_dev | banking77 | 70 | 84.3 | 90.0 | +5.7 | 84.3 | 6.1 | 8.6 | 8.8 |
| c2_t37b_dev | clinc150 | 90 | 88.9 | 86.7 | -2.2 | 88.9 | 10.2 | 11.5 | 11.9 |
| c2_t37b_dev | hate | 44 | 50.0 | 52.3 | +2.3 | 54.5 | 26.5 | 28.2 | 32.8 |
| c2_t37b_dev | irony | 42 | 83.3 | 83.3 | +0.0 | 88.1 | 15.1 | 13.4 | 8.8 |
| c2_t37b_dev | pg_temporal | 30 | 73.3 | 60.0 | -13.3 | 70.0 | 12.8 | 21.4 | 15.3 |
| c2_t37b_dev | rotten_tomatoes | 48 | 93.8 | 93.8 | +0.0 | 93.8 | 8.5 | 7.6 | 8.1 |
| c2_t37b_dev | spam | 62 | 98.4 | 96.8 | -1.6 | 96.8 | 6.0 | 3.0 | 5.7 |
| c2_t37b_dev | tb_mixtral | 82 | 92.7 | 92.7 | +0.0 | 92.7 | 6.7 | 5.8 | 6.9 |

## Appendix B. Reproduction

Scripts are in the session scratchpad (`/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/adbc4a3b-e366-431b-b0e2-96c55904b928/scratchpad/`: `diag.py`, `make_tables.py`, `make_tables2.py`, `nn.py`, `train_scan.py`, `assemble.py`) and are not stored in the project, because this task allowed one output file only. The scratchpad is session-specific and may be cleared. Run with `python3 -I` and numpy 2.3.5, scikit-learn 1.6.1.
