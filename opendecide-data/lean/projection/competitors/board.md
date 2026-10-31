# JevBench v1.5.4 board: the leaders, the small models, and where our 4B would land (30 Sep 2026)

**What this is.** A local, read-only analysis of the official board snapshot
(`bench/v154/leaderboard_v154.json`, 106 ranked systems, 1,624 decisions each: 904 open + 720 sealed). It is combined
with our unofficial public-item run (`bench/v154/RESULTS_30sep.md`, `bench/runs/scores_v154_all.json`) and the OHS-3
projection (`../FINAL_PROJECTION.md`, `../projection.md`).
- Nothing was submitted. There were no paid calls and no GPU use, and no existing file was edited.
- Every number comes from `board_analysis.py`, with output in `board_analysis_out.txt` (seed 0). Both files are in
  this folder.
- **EST** marks a judgement. Gaps are ours − Jev. I = Intelligence (the board's accuracy axis).
- "Sonnet and Vino" in the voice note are read as **Cygnet and Winnow**, the #1 and #2 on the board.

---

## 0. Short answer

1. **Cygnet (#1, Score A 73.70) and Winnow-12B (#2, 73.23)** are joint leaders (a statistical tie). Jev is #3 at 72.13.
   - Both leaders are **Gemma-4-12B** systems, 3× our size.
   - Winnow is the only non-frontier system that beats Jev on accuracy: I 74.4 vs 72.0.
   - Cygnet is just below Jev on accuracy (I 71.1). It wins Score A on speed.
2. **No ≤4B system comes within 10 points of Jev on accuracy.**
   - The best 4B on I is spark-s1-4b-v6 at 62.1. The top-ranked 4B, JevK5 v0.3, is at 56.3.
   - The 4Bs reach #4-#10 on Score A only through speed (≈93) and cost (≈63).
3. **Our 4B on the real board (EST):**
   - *Raw readout, as trained:* I ≈ 53 (49-58), Score A ≈ 69, rank ≈ #11 (#8-#21). It **loses to Jev on both**.
   - *Decisive yes/no readout:* I ≈ 68.5 (63-74), Score A ≈ 73.1, rank ≈ #3 (#1-#7).
     - P(I > Jev) ≈ **0.19**.
     - P(Score A > Jev) ≈ **0.76**, or **0.90** with the band-edge readout (§4.3).
     - P(#1) ≈ 0.3-0.57.
4. **Speed and cost are certain wins on the board.**
   - The evaluator measured Jev at 616 ms (speed axis 83.8). Even our slow L4-eager 110 ms scores 88.6.
   - Cost is about $0.021 vs $0.032 per 1K decisions.
5. **Owner's success** = beat Jev on OHS-3 accuracy AND JevBench accuracy AND consistency, hijack, injection, speed
   and cost. Calibration may lose, and yes/no may be slightly below Jev.

   | Reading of the definition | Joint probability |
   |---|---|
   | Consistency = both endpoints (complement and option order) | ≈ **0.05** |
   | Consistency = complement only | ≈ **0.16** |
   | Complement only, with the hosting lever done | ≈ **0.19** |
   | "JevBench" = the real board, sealed half counted | **0.02-0.05** |
   | If we stopped today (Modal endpoint) | **< 0.01** |

   The details are in §6.
6. **Only hijack is a proven win today**, plus cost on the JevBench formula.
   - Injection is a tie.
   - End-to-end speed is a loss through the Modal endpoint.
   - Option-order consistency is a likely loss.
   - Complement consistency is about a tie.
   - OHS-3 accuracy is a coin flip.

   See §7.
7. **The biggest cheap lever found here** is the band-edge readout for JevBench yes/no. It moves only the answers
   between 0.2 and 0.8 to 0.2 or 0.8.
   - On the public items it raises I from 62.5 to 78.7, and calibration also rises (84.3 → 86.1).
   - It has no free parameter.
   - On the board it is worth about +11 to +16 I for any 4B. Most of the field has not done this.

---

## 1. The leaders: Cygnet, Winnow and Jev

| | Cygnet (#1) | Winnow-12B Q8 (#2) | Jev 1.13.0 (#3) | JevK5 v0.3 (#4, best 4B on Score A) |
|---|---|---|---|---|
| What it is | Frozen Gemma-4-12B-it plus a shim (blockbrain; github.com/blockbrain-ai/cygnet-recipe) | Gemma-4-12B-it LoRA, merged, Q8 GGUF (hf EldanRing/Winnow-12B) | Closed hosted API (TypeSafe) | Qwen3.5-4B fine-tune |
| Score A [95% CI] | 73.70 [72.36, 74.46] | 73.23 [72.02, 73.99] | 72.13 [71.01, 72.61] | 71.90 |
| Intelligence (open / sealed) | 71.1 (72.5 / 69.7) | **74.4** (72.5 / 76.4) | 72.0 (71.5 / 72.5) | 56.3 (61.6 / 50.9) |
| Choice CC (open / sealed) | 82.9 / 80.3 | 77.6 / 82.0 | 85.7 / 87.6 | 80.3 / 74.2 |
| Yes/no (Noul) CC (open / sealed) | 57.9 / 55.7 | 58.6 / 66.1 | 47.8 / 48.6 | 42.3 / **15.0** |
| Score CC (open / sealed) | 76.6 / 73.2 | 81.2 / 81.0 | 81.2 / 81.1 | 62.2 / 63.6 |
| Noul abstention (0.2 < P(yes) < 0.8) | 14% | 13% | 23% | 29% |
| Calibration | 87.0 | 84.1 | 88.0 | 88.3 |
| Speed (raw p50) | 91.0 (40 ms, RTX PRO 6000) | 86.1 (95 ms, RTX 6000) | 83.8 (616 ms, hosted) | 93.6 (16 ms, H100) |
| Cost ($ per 1K) | 56.4 ($0.0283) | 56.6 ($0.0281) | 54.7 ($0.0323) | 63.1 ($0.0170) |
| Public-231 argmax accuracy (v1.4 board) | 0.879 | 0.857 | 0.866 | – (v0.2: 0.853) |

**How we compare with the leaders.**
- On the **same 231 public items** our 4B-E has argmax accuracy **0.883**. That is at or above Cygnet (0.879), Jev
  (0.866) and Winnow (0.857).
  - Only 11 systems on the v1.4 board are higher. They include Plumb-4B (0.896), JevOne and Jev-Omni.
  - Our run of Jev scores 0.8658, which is identical to the board's value, so our Jev runs match the board's.
- **The difference is on unseen items.**
  - The 12B leaders keep their open score on the sealed half: the gap is −4 to +3.
  - The 4B fine-tunes lose 3-12 I, and mostly on yes/no.
  - Winnow is better on sealed than on open.

---

## 2. Extraction: top 10, Jev, and every ≤4B / ~2B system

All systems are ranked with full coverage.
- **Column key:** Io / Is = I_open / I_sealed; gap = Io − Is; C / S / $ = the calibration, speed and cost axes.
- **Per-type columns:** chance-corrected competence (CC) for choice / noul / score.
- **abst** = pooled Noul abstention.
- **p50** = raw median latency before the self-host adjustment (×2 + 0.15 s).
- **Size and hosting** come from the display and underlying fields (the board has no numeric parameter field).

### 2a. Axes and the intelligence split

| # | System | Size | Host | Score A | I | Io | Is | gap | C | S | $ | p50 ms | $/1K |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cygnet | 12B | gpu RTX PRO 6000 | 73.70 | 71.1 | 72.5 | 69.7 | +2.7 | 87.0 | 91.0 | 56.4 | 40 | 0.0283 |
| 2 | Winnow-12B Q8 | 12B | gpu RTX 6000 | 73.23 | 74.4 | 72.5 | 76.4 | −3.9 | 84.1 | 86.1 | 56.6 | 95 | 0.0281 |
| 3 | **Jev 1.13.0** | closed | hosted API | **72.13** | **72.0** | 71.5 | 72.5 | −0.9 | **88.0** | **83.8** | **54.7** | 616 | 0.0323 |
| 4 | JevK5 v0.3 | 4B | gpu H100 | 71.90 | 56.3 | 61.6 | 50.9 | +10.7 | 88.3 | 93.6 | 63.1 | 16 | 0.0170 |
| 5 | Plumb-4B | 4B | gpu H100 | 71.56 | 55.8 | 60.9 | 50.8 | +10.1 | 87.4 | 93.5 | 63.1 | 17 | 0.0170 |
| 6 | Jev-Omni | 12B | gpu RTX 6000 | 71.50 | 70.5 | 70.5 | 70.5 | 0.0 | 82.6 | 84.7 | 56.1 | 113 | 0.0292 |
| 7 | decider-4b v2 | 4B | gpu RTX 5090 | 71.28 | 55.8 | 61.7 | 49.8 | +11.9 | 85.6 | 90.9 | 64.5 | 26 | 0.0152 |
| 8 | Decision 4B v1.2 | 4B | gpu H100 | 70.83 | 53.7 | 56.3 | 51.1 | +5.2 | 88.6 | 93.5 | 63.1 | 16 | 0.0170 |
| 9 | Imajev-4B | 4B | gpu RTX 5090 | 70.39 | 53.5 | 56.2 | 50.7 | +5.5 | 88.1 | 91.1 | 63.3 | 42 | 0.0168 |
| 10 | Decision 4B v1.1 | 4B | gpu H100 | 70.39 | 53.1 | 54.7 | 51.6 | +3.1 | 87.3 | 93.5 | 63.1 | 16 | 0.0170 |
| 12 | SemIf | 4B | gpu RTX 5090 | 68.66 | 51.3 | 54.0 | 48.6 | +5.4 | 84.0 | 90.9 | 63.1 | 39 | 0.0170 |
| 13 | spark-s1-4b-v6 | 4B | gpu RTX 6000 | 68.16 | **62.1** | 62.5 | 61.8 | +0.7 | 69.7 | 85.5 | 60.4 | 128 | 0.0209 |
| 14 | metask-jev-4b | 4B | gpu RTX 5090 | 67.48 | 53.5 | 56.7 | 50.2 | +6.5 | 82.7 | 89.5 | 57.7 | 68 | 0.0256 |
| 15 | Hopper | 4B | gpu A6000 | 67.47 | 49.9 | 48.7 | 51.0 | −2.3 | 87.9 | 87.2 | 62.3 | 122 | 0.0181 |
| 16 | Malkuth-4B | 4B | gpu RTX 5090 | 66.77 | 54.5 | 58.4 | 50.5 | +7.8 | 83.2 | 86.2 | 55.8 | 146 | 0.0297 |
| 18 | reflex 4B | 4B | gpu H100 | 65.24 | 51.5 | 55.2 | 47.8 | +7.4 | 86.8 | 68.8 | 63.1 | 1358 | 0.0169 |
| 21 | Raw Qwen3-4B-Instruct-2507 | 4B | gpu A6000 | 62.14 | 54.1 | 57.4 | 50.7 | +6.7 | 52.9 | 89.2 | 63.4 | 56 | 0.0166 |
| 23 | JevK5 v0.2 | 4B | gpu RTX 5090 | 58.11 | 46.7 | 50.0 | 43.4 | +6.6 | 84.9 | 90.9 | 63.1 | 33 | 0.0170 |
| 27 | Instinct Dual 4B | 4B | demo API | 46.97 | 43.1 | 46.3 | 39.9 | +6.3 | 88.3 | 82.0 | 60.2 | 253 | 0.0212 |
| 30 | **decider-2b** (best 2B) | 1.9B | gpu H100 | 45.10 | 42.3 | 48.8 | 35.9 | +12.9 | 71.5 | 94.4 | 64.9 | 14 | 0.0148 |
| 32 | system-one-open | Gemma-4 E2B | demo L4 | 42.44 | 41.6 | 44.4 | 38.8 | +5.6 | 71.6 | 78.3 | 68.3 | 575 | 0.0114 |
| 37 | kev 4B | 4B | gpu A6000 | 38.07 | 39.9 | 47.1 | 33.2 | +13.9 | 67.6 | 85.5 | 65.8 | 172 | 0.0138 |
| 39 | open-alternative-jev | 4B | gpu RTX 5090 | 33.56 | 37.4 | 42.6 | 32.1 | +10.5 | 76.9 | 91.3 | 63.3 | 36 | 0.0168 |
| 41 | Malkuth-2B | 2B | gpu RTX 5090 | 29.90 | 35.5 | 44.2 | 28.6 | +15.6 | 75.2 | 91.8 | 65.6 | 41 | 0.0141 |
| 44 | local-jev Qwen3.5-4B | 4B | gpu A6000 | 25.82 | 33.7 | 36.7 | 30.8 | +5.9 | 82.4 | 83.7 | 59.3 | 138 | 0.0228 |
| 47 | Decision 2B | 2B | gpu RTX 6000 | 22.52 | 31.3 | 34.6 | 28.0 | +6.7 | 86.2 | 90.4 | 66.4 | 75 | 0.0132 |
| 49 | typecastlm | 4B | gpu RTX 5090 | 21.83 | 31.2 | 23.7 | 38.8 | −15.1 | 76.7 | 92.0 | 64.0 | 38 | 0.0159 |
| 62 | Raw Phi-4 mini | 3.8B | gpu A6000 | 15.22 | 27.6 | 38.3 | 20.0 | +18.3 | 71.4 | 89.2 | 53.2 | 65 | 0.0363 |
| 63 | OpenSourceJev Q4_K_M | 4B | gpu A6000 | 13.25 | 25.8 | 27.9 | 23.7 | +4.2 | 76.0 | 72.5 | 69.1 | 620 | 0.0107 |
| 65 | Open-Jev 2B | 2B | gpu H100 | 9.07 | 33.6 | 38.8 | 28.3 | +10.4 | 73.6 | 75.8 | 33.1 | 429 | 0.1704 |
| 67 | Qwen3-Reranker-4B | 4B | gpu A6000 | 7.06 | 21.0 | 30.3 | 13.4 | +17.0 | 76.3 | 79.6 | 48.4 | 181 | 0.0525 |
| 76 | JevAct | 2B | demo | 1.52 | 11.2 | 19.7 | 3.5 | +16.3 | 62.5 | 76.4 | 68.6 | 401 | 0.0112 |
| 81 | Raw Qwen3-1.7B | 1.7B | gpu A6000 | 0.85 | 9.7 | 12.3 | 7.1 | +5.2 | 21.6 | 90.2 | 68.5 | 66 | 0.0112 |
| 83 | zerank-2 | 4B | gpu A6000 | 0.13 | 4.8 | 10.0 | −0.4 | +10.4 | 81.7 | 80.3 | 48.4 | 161 | 0.0525 |
| 85 | smalljev | 2.5B | gpu A6000 | 0.07 | 3.7 | 10.9 | −3.5 | +14.5 | 73.1 | 86.5 | 60.8 | 150 | 0.0203 |

**Sub-1.5B systems.** There are 30 more, mostly encoders or rerankers of 0.07-0.8B. All have Score A ≤ 8.4 and I ≤ 22.5.
Most of them abstain on over 40% of yes/no items. The full list is in `board_analysis_out.txt` §1.

**Not ranked:**
- Eval Engine Decision-4B: partial, with 74 context overflows.
- mica-v01-4b: a partial run.
- Jobe Qwen3.5-4B: not measured.

classifier.dev (fast) runs *on Jev* and is listed as an honorable mention: Score A 74.66, I 75.8.

### 2b. Per-type competence (CC) and yes/no abstention

| System | Choice open / sealed | Noul open / sealed | Score open / sealed | Noul abstention |
|---|---|---|---|---|
| Cygnet | 82.9 / 80.3 | 57.9 / 55.7 | 76.6 / 73.2 | 14% |
| Winnow-12B | 77.6 / 82.0 | 58.6 / 66.1 | 81.2 / 81.0 | 13% |
| **Jev** | **85.7 / 87.6** | **47.8 / 48.6** | **81.2 / 81.1** | 23% |
| JevK5 v0.3 | 80.3 / 74.2 | 42.3 / 15.0 | 62.2 / 63.6 | 29% |
| Plumb-4B | 80.4 / 73.3 | 43.0 / 16.6 | 59.3 / 62.6 | 28% |
| decider-4b v2 | 80.4 / 77.3 | 42.9 / 18.7 | 61.9 / 53.4 | 27% |
| Decision 4B v1.2 | 80.9 / 73.8 | 20.1 / 16.4 | 67.8 / 63.0 | 37% |
| Imajev-4B | 80.1 / 82.3 | 21.8 / 7.6 | 66.8 / 62.2 | 37% |
| Decision 4B v1.1 | 80.1 / 74.8 | 18.0 / 15.7 | 65.8 / 64.2 | 38% |
| spark-s1-4b-v6 | 72.6 / 73.1 | 50.4 / 46.5 | 64.4 / 65.7 | 13% |
| decider-2b | 52.0 / 53.5 | 35.2 / 5.8 | 59.1 / 48.4 | 22% |

**The 4B pattern.** Against Jev, the top 4Bs trail by:
- about 6 CC on open choice and about 13 on sealed choice;
- about 18 CC on Score;
- 5-30 CC on open yes/no and 30-41 CC on sealed yes/no.

Most of the yes/no loss is **abstention**: P(yes) lands between 0.2 and 0.8, and v1.5 scores that as wrong.

---

## 3. The field's open → sealed relationship

Sample: ranked, full coverage, I_open ≥ 20, n = 75. Below about 20 the numbers are noise around chance.
- **Outliers:** one, kev-0.6b (gap +27.0). It was dropped by the 3 robust-sd rule.
- **OLS, n = 74:** **I_sealed = −16.69 + 1.214 × I_open** (residual sd 5.8, R² 0.93).
  - The slope is above 1: weaker systems lose more on sealed items.
  - At I_open 72 it predicts about 70.7; at I_open 60, about 56.2.
- **Frozen G_med = 5.19.** The overfit penalty starts only when gap − 5.19 > 8, that is, at a gap above 13.2. No
  4B in the top group is penalised.

| Group | n | Median open−sealed gap | Mean residual vs OLS |
|---|---|---|---|
| All (kept) | 74 | +4.1 | 0.0 |
| Qwen3.5-4B-class fine-tunes and readouts | 19 | +6.3 | +0.4 |
| Top-6 4B (ranks 4-10) | 6 | **+7.8** | **−3.6** (below the line) |
| ≤2.5B | 8 | +11.7 | −3.1 |
| ≥9B open weights | 35 | +0.8 | +1.4 |
| Closed APIs (Jev, GPT, Gemini, DeepSeek) | 9 | −1.1 | −1.3 |

**Per-type gap for the top-6 4B (median):** choice +5.7, **noul +19.2**, score +3.1. Jev's gaps are −1.9, −0.9 and
0.0. The 4B open → sealed drop is mostly yes/no abstention on unfamiliar items.

---

## 4. Where our 4B-E would land on the real board

### 4.1 Three ways to estimate I_open, then I_sealed from the field

Inputs:
- Our public-item I: **62.5 raw** and **78.7 decisive**.
- Jev on the same items: 63.2 in our run. Its board I_open is 71.5, so **the public 231 items are 8.4 points harder
  for Jev** than the board's open set.
- The public items were our development set.
  - On the 49 yes/no items the 4B-E committed on, it was right on **all 49**. That is a dev-set signature.
  - EST dev discount: 3-6 I.

| Method | I_open | Board I, sealed via OLS | Board I, sealed via 4B gap 6.3 | Same two, after a −4 dev discount |
|---|---|---|---|---|
| M1 literal: public I taken as I_open, raw | 62.5 | 60.8 | 59.3 | 56.4 / 55.3 |
| M1 literal, decisive | 78.7 | 78.8 | 75.5 | 74.3 / **71.5** |
| M2 Jev-anchored: Jev board I_open + (ours − Jev on public), raw | 70.9 | 70.1 | 67.7 | 65.6 / 63.7 |
| M2 Jev-anchored, decisive | 87.1 | 88.0 | 83.9 | 83.6 / 79.9 |
| **M3 peer-anchored, raw:** 4B-class regression of board I on public argmax accuracy (n = 15, r = 0.39) | – | – | – | **53.1** (resid sd 10.2) |
| **M3 peer-anchored, decisive:** top-6 4B board rows re-scored as if their yes/no abstentions were committed (q = 0.62) | – | – | – | **69.2** (67.4-69.5; 66-72 for q = 0.55-0.70) |

**Why M1 and M2 overstate for the decisive readout.**
- Jev's public yes/no is unusually low: CC 34.0, against 47.8 on the board.
- Our +41.9 CC yes/no edge on the public items is partly dev-set fit, as the 49/49 shows.
- The public set has no judge tier, and its easy and standard items are at ceiling for both systems.
- The 4Bs with *higher* public accuracy than ours (Plumb 0.896) sit at I 55.8 on the board.

**Why M3 is the anchor.**
- Our public accuracy (0.883) is at the top of the 4B class but not above it.
- Our raw yes/no abstention (34%) matches the peers (27-38%).
- So "a top 4B peer, committed" is the most defensible reference.

On the other side, the whole-field regression puts a 0.883 system at I 69.8, and the literal-discounted M1 at 71.5.
Those are the optimistic end.

### 4.2 What committing yes/no is worth: measured on public items, by rescoring our stored runs

| Run | Readout | I | Noul CC | Calib | Noul ECE / Brier |
|---|---|---|---|---|---|
| 4B-E | as returned (T = 1), abstains 34%, q = 0.68 on abstained items | 62.5 | 27.3 | 84.3 | 0.095 / 0.070 |
| 4B-E | full commit (P → 0/1) | 78.7 | 75.9 | 83.4 | 0.108 / 0.108 |
| 4B-E | **band edge** (only 0.2-0.8 answers moved to 0.2/0.8) | **78.7** | 75.9 | **86.1** | 0.067 / 0.082 |
| 2B-I pilot | as returned / commit / band edge | 39.9 / 70.3 / 70.3 | −21.2 / 70.1 / 70.1 | 81.8 / 78.1 / 84.9 | – |
| Jev p1 | as returned / commit / band edge | 63.2 / 73.6 / 73.6 | 34.0 / 65.2 / 65.2 | 81.2 / 76.4 / 81.7 | – |

- **Board peers.** Committing would lift the top 4Bs from 53-56 to **66-72** (EST, q = 0.55-0.70). Jev would go from
  72.0 to about **82**. So if TypeSafe ever ships a committed readout, the bar moves up by about 10.
- **Calibration on the board.** A full commit sets yes/no ECE equal to the error rate. With about 18% error on
  open + sealed, calibration falls to about 77.5 (EST). The band edge keeps it at about 81.5 (EST).

### 4.3 Monte Carlo placement (200K draws; EST inputs)

| Axis | EST input |
|---|---|
| **I, raw** | N(53.2, 3.5) |
| **I, decisive / band edge** | N(68.5, 4.0) |
| **Calibration** | raw 85.5; commit 77.5; band edge 81.5 (sd 2-2.5) |
| **Speed** | Evaluator GPU; raw p50 lognormal, median 30 ms (≈17-55 ms) |
| **Cost** | Our public 817.8 tokens scaled by Jev's board/public token ratio, so ≈687 tokens × $0.03/M = $0.0206 per 1K → 60.6 |

Resulting axes:
- Speed: median 93.5 (91.8-94.7).
- Cost: 60.6. Our layout-E prompt costs about 2.5 cost points against the 4B peers' 63.1.

| Our 4B readout | I (10/50/90) | P(I > Jev 72.0) | Score A (10/50/90) | P(A > Jev 72.13) | P(A > Cygnet 73.70) | Score A rank | I rank |
|---|---|---|---|---|---|---|---|
| Raw (as trained) | 48.7 / 53.2 / 57.6 | **0.00** | 63.7 / 69.3 / 71.2 | **0.02** | 0.00 | #11 (#8-#21) | #45 |
| Decisive (commit) | 63.4 / 68.5 / 73.6 | **0.19** | 71.3 / 73.1 / 74.7 | **0.76** | 0.31 | #3 (#1-#7) | #22 (#13-#26) |
| Band edge | 63.4 / 68.5 / 73.6 | **0.19** | 72.2 / 73.9 / 75.6 | **0.90** | 0.57 | #1 (#1-#3) | #22 (#13-#26) |

**Sensitivity to the I centre** (sd 4):

| I centre | P(I > Jev) | P(A > Jev), decisive | P(A > Jev), band edge |
|---|---|---|---|
| 65.0 | 0.04 | 0.47 | 0.70 |
| 66.5 | 0.08 | 0.60 | 0.80 |
| 68.5 | 0.19 | 0.76 | 0.90 |
| 70.5 | 0.35 | 0.87 | 0.96 |

**Our 2B (EST, not modelled in detail).**
- Public accuracy is 0.840, far above the board's 2Bs (decider-2b 0.710).
- Decisive board I is about 60 (55-65). That would be about 18 I above today's best 2B (decider-2b, 42.3), but
  P(I > Jev) < 0.02.

### 4.4 Axis by axis vs Jev on the board

| Axis | Jev | Our 4B (EST) | Verdict |
|---|---|---|---|
| Intelligence | 72.0 | 53 raw / 68.5 decisive | **Loss likely.** P(win) 0.00 raw, 0.19 decisive |
| Calibration | 88.0 | 85.5 raw / 77.5 commit / 81.5 band edge | Loss (the owner allows it) |
| Speed | 83.8 (616 ms) | 88.6 (L4 eager, measured) to 94.7 | **Win, P ≈ 1.** Break-even is a raw p50 of about 247 ms |
| Cost | 54.7 ($0.0323) | 60.6 ($0.0206) | **Win, P ≈ 1** |
| Score A | 72.13 | 69.3 raw / 73.1 decisive / 73.9 band edge | Win only with a decisive readout |

---

## 5. What the board means for "beat Jev on JevBench accuracy"

There are three different claims. Pick one and write it down before the OHS-3 result.

| Claim | Evidence today | P |
|---|---|---|
| (a) Our run of the 231 public items, decisive readout, vs Jev as returned | 78.7 vs 63.2: **+15.5 [+5.2, +26.9]**, significant. Half B +19.9 [+4.2, +37.9]. **These are our development items.** | 0.88 for the final 4B (a re-run of the new model) |
| (b) Same, vs Jev also committed (the fairest public comparison) | +5.1 [−4.4, +15.0], a tie | about 0.85 point (FINAL_PROJECTION §11); EST about 0.2 significant |
| (c) The real board, with the sealed half (needs a submission, which the owner has not approved) | EST I 68.5 vs 72.0 | **0.19** (P(Score A > Jev) 0.76-0.90) |

---

## 6. Owner's success: joint probability

**Definition used.** All of the following must hold. Calibration is excluded, and yes/no may be below Jev.
- OHS-3 overall accuracy ≥ Jev (point estimate);
- JevBench accuracy ≥ Jev;
- consistency ≤ Jev;
- hijack ASR < Jev;
- injection ASR ≤ Jev;
- median end-to-end speed < Jev;
- cost < Jev.

**Factors used, with sources:**

| Factor | P | Source |
|---|---|---|
| OHS-3 accuracy ≥ Jev | 0.45 | FINAL_PROJECTION (A), reconciled (projection.md: 0.54) |
| JevBench (a), public run, decisive | 0.88 | FINAL_PROJECTION (A) |
| JevBench (c), real board I | 0.19 | this file, §4.3 |
| Complement violations ≤ Jev | 0.70 | FINAL_PROJECTION (A) |
| Option-order drift ≤ Jev | 0.30 | FINAL_PROJECTION (A); never measured for Jev |
| Hijack | 0.97 | FINAL_PROJECTION (A) |
| Injection, point win | 0.70 | FINAL_PROJECTION (A); a significant win is about 0.10 |
| Speed, end to end with direct hosting | 0.75 | FINAL_PROJECTION (A); 0.90 if timed before OHS-3; about 0.10 via Modal |
| Cost, JevBench formula | 0.95 | FINAL_PROJECTION (A) |

**Correlations (Gaussian copula, 400K draws):**

| Pair | ρ | Reason |
|---|---|---|
| OHS-3 accuracy ~ board I | 0.40 | same model quality, different items |
| OHS-3 accuracy ~ public run | 0.20 | |
| Public run ~ board | 0.30 | |
| OHS-3 accuracy ~ complement | 0.30 | violations rise as yes/no falls (projection §10) |
| Complement ~ option order | 0.20 | |
| Hijack ~ injection | 0.20 | |

All other pairs are independent. Speed and cost are independent because cost is token-based.

| Variant | Joint P (copula) | Independent |
|---|---|---|
| **O1:** JevBench (a); consistency = complement AND option order | **0.05** | 0.04 |
| **O2:** JevBench (a); consistency = complement only | **0.16** | 0.13 |
| O3: O1 with JevBench (c), the real board | 0.016 | 0.009 |
| O4: O2 with JevBench (c) | 0.05 | 0.03 |
| O5: O1 with the hosting lever done (speed 0.90) | 0.06 | 0.05 |
| **O6:** O2 with the hosting lever done | **0.19** | 0.16 |
| O7: O1 if we stopped today (Modal endpoint, speed 0.10) | **0.007** | 0.005 |
| O8: O2 with OHS-3 "beat" read as the PREREG "matches" (0.50) | 0.17 | 0.15 |
| O9: O2 with injection needing a *significant* win | 0.02 | 0.02 |
| O10: accuracy only (OHS-3 ≥ Jev AND JevBench (a)) | 0.41 | 0.40 |

**How this relates to FINAL_PROJECTION's figure of 0.21.** That figure uses the PREREG accuracy *tie* (0.50) and
leaves out consistency. Adding complement consistency (× about 0.75 with the correlation) and using "beat" (0.45)
gives about 0.14-0.16, which matches O2.

**The two weakest links are:**
- option-order drift (0.30), which alone cuts success about 3×;
- OHS-3 accuracy (0.45).

---

## 7. What is proven today and what is not

| Metric | Status today | Evidence |
|---|---|---|
| Hijack (jagged ASR) | **Proven win** | Jev 99.4% vs 4B-E 0.6%. The set was used for selection, and the adaptive attack has not been run (EST 0.7-0.9 under it). |
| Cost, JevBench formula | **Proven win (structural)** | Public run $0.0245 vs $0.0384 per 1K. Board EST $0.021 vs $0.0323. Real serving cost has never been measured. |
| Speed, JevBench **board** formula | Win on paper | The evaluator measured Jev at 616 ms → 83.8. Our L4-eager 110 ms scores 88.6. In *our own* public run Jev measured 238 ms → 91.4, so we lost 88.6 vs 91.4 there. |
| Speed, end to end (OHS-3 style) | **Loss today** | Modal web endpoint about 410 ms vs Jev 187-248 ms (same laptop). A direct tunnel for v10 measured 114.6 ms, but 4B-E has not been timed that way. |
| Prompt injection (OPI ASR) | **Tie** | 1.0% vs 1.3%, diff −0.4 [−1.1, +0.1] |
| Complement consistency | **About a tie** | v11c OHS-1 11.31% vs Jev about 10.8%. 4B-E dev 4.81% (Jev not run on dev). |
| Option-order consistency | **Likely loss** | 4B-E dev drift 8.2%, 18.1% at 20+ options. Jev never measured (noise floor 1.4-2.4%). |
| OHS-3 overall accuracy | **Not proven; coin flip** | Projected −0.3 [−3.6, +3.2], P(≥ Jev) 0.45. Best held-out 4B so far: OHS-2 −1.63. |
| JevBench accuracy | Win on dev items only | Public decisive +15.5 (significant); raw −0.7 (tie); vs committed Jev +5.1 (tie). Real board: likely loss. |
| Yes/no (allowed slightly below) | Below | OHS-2 v11c −7.2 [−10.6, −3.8]. OHS-3 projection −1.8 [−9, +4.5]. |
| Calibration (allowed to lose) | Mixed | Public JevBench 84.3 vs 81.2 (win). OHS Brier likely loss (P matches 0.18). |

---

## 8. What we can do

1. **Pre-register a JevBench yes/no readout: band edge, or full commit.**
   - It is a rule from the method text, with no parameter to fit.
   - Check it on dev (the noul ECE and Brier) before any JevBench use. Use it only in the JevBench adapter: OHS-3
     Brier needs the raw probabilities.
   - Value: +16 I on the public items, with calibration slightly higher (84.3 → 86.1); EST +11 to +16 I on the board.
   - It turns Score A from a sure loss (0.02) into a likely win (0.76-0.90).
   - It costs nothing and needs no GPU.
2. **Fix hosting before OHS-3.** Time the 4B on an H100 with CUDA graphs through a direct tunnel. This is projection
   lever 1. It moves end-to-end speed from a loss today to about 0.9, and owner success from 0.16 to 0.19.
3. **Measure option-order drift on dev now,** and test the read that averages normal and reversed option order
   (projection lever 3). This is the single largest cut in the joint probability.
4. **For the real-board accuracy gap:**
   - Against Jev, the 4B class trails by about 18 CC on the **Score** type and about 13 on **sealed choice**. Committed
     yes/no is not the problem.
   - Our public Score result (79.5 vs Jev 72.6) rests on only 18 items and cannot be trusted.
   - Whether the new 500K 4B generalises better can only be seen on held-out data. The best proxy we are allowed is
     OHS-3.
5. **Keep the headline system the 4B,** and keep the "no submission" rule until the owner says otherwise.
   - A submission would show the real board number. The central estimate is Score A #1-#7, with I about 3.5 below Jev.
   - If submitted, our 818-token layout-E prompt costs about 2.5 cost points against the 4B peers. That is minor.

## 9. Caveats

- **The M3 anchor assumes our 4B behaves like the top 4B peers on unseen items.** Our OHS results (about a tie with
  Jev on fresh classification) hint we could do better. The public-set 49/49 hints at dev fit. Neither is JevBench
  sealed evidence.
- **The peers' committed-equivalent numbers use only pooled abstention.** The open/sealed split is assumed (sealed =
  open + 0.10), and q (0.55-0.70) is a judgement.
- **Speed and cost on the board are EST.** They depend on the evaluator's GPU and on our prompt length over the 1,624
  items. Even the worst measured case (L4 eager) beats Jev on speed.
- **The owner probabilities reuse FINAL_PROJECTION's reconciled factors,** which are themselves EST (see their ranges).
  The copula correlations are judgements. The independent column shows they matter little.
- **Jev could adopt a committed readout.** Its board I would then rise to about 82 (EST). The Score A edge above is
  relative to today's Jev row.
