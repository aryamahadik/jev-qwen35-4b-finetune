# C2 plan to beat Jev on as many metrics as possible (4B only, about $45 of H100, about 1 week)

## 0. Bottom line

- **Beating Jev on every metric is about a 1% outcome. I cannot honestly raise it much above that.** The binding metric is general real-text accuracy (OHS-4 part G). On fresh sources Jev leads by about 5 pp (OHS-3 74.3 vs 79.6; held-out corpora 76.1 vs 81.7). One week of data most likely recovers 1 to 3 pp of that.
- **What the plan does change:** expected wins rise from about 3.6 to about 4.4 of 8 metrics. The chance of winning at least 5 of 8 roughly doubles, from about 0.2 to about 0.4. Most of the gain comes from cheap, mostly free levers.
- **The core finding:** most of the effort in the brief goes to things that cannot move the losing metrics (calibration tricks, more replay, Haiku-labelled easy rows). The levers that can move them are:
  1. Opus labels on rows C1 gets wrong.
  2. Official/human-gold breadth that matches how part G is built.
  3. Complement consistency trained on far more rows (twins of gold-labelled rows carry no new label risk).
  4. Serving changes for cost.

## 1. Corrections to the brief

- **OHS-3 speed and cost were losses, not wins.**
  - p95 was 603 vs 301 ms, and cost per 1K was $0.433 vs $0.061 (`/Users/aryamahadik/Documents/jev/reports/ROUND1_RESULTS.md`).
  - SGLang S1 fixes most of the p95: server p95 is 98 ms at concurrency 1.
  - Cost is still $0.079 vs $0.061 at 40% use.
  - Only p50 was a clean win.
- **The next sealed look is OHS-4, not OHS-3.** Parts: G 2,883, R 1,454, U 433, X 281 pairs, consistency 881 calls (444 complement).
- **Calibration is not the problem.**
  - Dev temperature fits T = 0.995-1.03, and the reliability bins sit on the diagonal.
  - On dev, Brier falls 0.0054 per accuracy point (r = -0.97). So 5.3 pts × 0.0054 = 0.029, which covers the whole 0.022 sealed Brier gap.
  - So the Brier gap is an accuracy gap. Temperature, label smoothing and Brier-loss work (heavily featured in the sweeps) has about zero value here.
- **Dev cannot see the general gap.**
  - On dev C1 and Jev are level (77.8 vs 78.0), but sealed shows -5.3.
  - Dev complement violation is 0.024-0.045, against 0.170 sealed (held-out negation frames).
  - So the C2 pre-gate is blind to the main loss.

## 2. Flaws in our current data

1. **The G-block gate keeps the easy rows and drops the useful ones.**
   - 11,200 rows were accepted from Haiku at confidence ≥ 0.80, and 1,272 from Opus at ≥ 0.85. Opus dropped 6,301 low-confidence rows (`c2_build/gblock/label/opus_finalize_A39.json`).
   - The Opus audit of accepted rows appears to show 0 disagreements in every domain (I read the [0, n] counts as disagreements over audited rows; format not verified).
   - On dev, where both teachers are confident and agree, C1 is already 94-99% right.
   - The cross-entropy gradient on the gold logit is (1 - p_gold). A row C1 gets at 0.95 gives about a tenth of the signal of a row at 0.5.
   - Estimate: only about 5-15% of the G-block carries real signal.
2. **The G-block labels follow the wrong kind of gold.**
   - They are Claude's conventions on 41 Claude-invented cards. OHS-4 G uses human, official or program gold.
   - The G-block's own official/human metadata (categories, departments, classifications, dates) sits unused: A39 b marks it "report-only, never targets".
3. **Labels are skewed after the gate.**
   - Accepted yes-rate per card runs from 7.4% to 82.5%, and the top choice label from 43% to 87% (`gblock/label/ROUTE.md`).
   - Check that the mixer's 45-55% yes balance applies to the G-block.
4. **Depth over breadth.** The G-block is 41 cards at about 300-500 rows each. Held-out gains scale with the number of tasks, and per-task gains saturate near 64-128 rows (Super-NI, Flan).
5. **The complement lever is capped for a reason that doesn't hold.** T37b is capped at 2,000 rows "to limit label risk". A twin whose gold is 1 minus the parent's gold has the same label risk as the parent, so the cap is unnecessary.
6. **Haiku labels cannot carry C1 past Jev on G** (math in section 5).

## 3. The key insight

The general gap is a transfer gap, so:
- **(a)** Teach only where C1 is wrong, using a teacher that is clearly better than Jev. That is Opus at +7.5 on dev public rows; Haiku is only +1.8.
- **(b)** Match the sealed gold type (official/human labels) and favour breadth over depth.
- **(c)** Consistency needs no new labels, so scale complement training to every gold-bearing yes/no row, across many kinds of predicate negation.
- **(d)** Stop spending on calibration.
- **(e)** Take the wins a local 4B gets from its structure: R, hijack, p50/p95, and cost at saturation.

## 4. Top 8 actions, ranked by expected gain per cost

**Action 0 (prerequisite, before training, about $0): a G-proxy dev.**
- **What:** 400-600 rows from 2-3 new real-text sources with official/human metadata gold, built with the existing `fetch_socrata.py` path.
  - Not in C1 or C2 training, and not on any sealed path.
  - At least 30% card-free; yes/no 40-50%.
  - Add 150 complement pairs that use negation patterns held out of training.
- **Read:** C1 now, and Jev once (evaluation only, never a training or selection signal).
- **Why:** if the proxy reproduces a gap of about -4 to -6, it becomes the compass for Action 6 and for the G forecast. Without it, every G decision is blind.

**1. Serving setup for cost and speed (SPEED-3; amendment before the look).**
- **What:**
  - Compute $/1K at 40% of saturated throughput, measured at concurrency 64 and 128. S1 "was not saturated at c=16".
  - Reuse the state prefix across questions that share a state (built in SPEED-1), and turn on chunked prefill.
  - Pin to a US region. Headline p50/p95 at c=1; report c=16 and c=64 as well.
- **Metrics:** cost, p95.
- **Gain:** cost $0.079 → about $0.045-0.065 (estimate, if saturated throughput is 1.3-1.8× the c=16 figure). P(cost win) goes from about 0.15 to about 0.5.
- **Cost:** about $1-2 of H100; about 0 Claude (one Sonnet script).
- **Risk:** throughput already saturates near c=16 on long inputs, and the long-input p95 tail (OHS-3's legacy path hit 603 ms).
- **When:** after training.

**2. Re-weight the G-block with a C1 read (before training).**
- **What:** run C1 over all 18.8K G-block rows (kept plus dropped) on free od-l4 or S1.
  - Rows where C1 already agrees with the label at p ≥ 0.9: keep 35% as anchors.
  - Rows where C1 disagrees with a Haiku-accepted label: send to Opus (est. 1-2K rows, 20-40 chunks); keep only if Opus agrees at ≥ 0.85.
  - Rebalance yes-share per card to 40-60%.
- **Metric:** G accuracy. Gain +0.2 to +0.6 pp (estimate).
- **Evidence (dev):**
  - Where C1 ≠ Haiku, Opus is right 68%, Haiku 53%, C1 30%.
  - Those 17% of rows hold 56% of C1's errors.
- **Cost:** about $0-1 GPU and 20-40 Opus chunks. It also saves about 5K training rows (about $1.5), which pays for Actions 4-5.
- **Risk:** over-weighting ambiguous rows. Keep the up-weight at 1.0-1.5×.

**3. Trap-mined oversampling for R (before training; `c2_build/c2_select.py`).**
- **What:** tag each distractor by the corruption the program applied. Units where C1 puts ≥ 0.25 on a tagged trap go to the hard bin at 2× weight, inside the existing hard ≤ 30% cap.
- **Trap types to favour (C1 pick rates):** band off-by-one 50%, boundary 39%, rename/merger 38%, unit 38%, not-yet-in-force 30%.
- **Metric:** R accuracy. Gain +1 to +2.5 pp (estimate; the dev upper bound is +2.0 to +2.9 on pg/hard dev).
- **Cost:** about $0; one Sonnet agent.
- **Risk:** learning the trap templates rather than the skill. OHS-4 R uses independent generators. Needs an amendment, because A37 e says selection is unchanged.

**4. Complement scale-up, label-safe (before training).**
- **What:** exact predicate-level negation twins for gold-bearing real-text yes/no rows:
  - G-block, about 5K;
  - the new official-metadata block (Action 5), about 5K;
  - replay rows, about 8-10K, drawn as complement units inside the replay budget.
- **Building the twins:**
  - Haiku writes them from a catalogue of at least 300 negation patterns (antonyms, lacks, fails to, no longer, at most, excludes, not among, scope negation), not outer frames only.
  - A program checks that one predicate changed. A Haiku blind check ("exact opposites given the text?") must say yes at ≥ 0.9.
  - Sonnet audits 3%; any pattern with more than 3% audit error is dropped.
  - Twin gold = 1 - gold. The existing complement + sym_cons loss at lam 1.0 applies, so no new trainer code.
  - Hold out 20% of patterns for the Action 0 dev. Lift the T37b 2,000 cap.
- **Metrics:** complement violation, with Brier as a side effect.
- **Gain:** G complement violation -0.03 to -0.08 (the spec expects 0 to -0.03); Brier -0.001 to -0.003.
- **Evidence:**
  - C1 learned its trained frames (dev 0.033) but not held-out ones (sealed 0.170), so coverage of negation forms is the lever.
  - LoCo-LMs: negation consistency 0.42 → 0.87 from 1,072 facts; plain cross-entropy dropped reverse consistency to 0.01.
- **Cost:** about 40K Haiku reads plus a Sonnet audit; about +$3 of training.
- **Risk:** negations that are not exact opposites. Held-out forms may still fail (held-out nested negation: 34.5%). Too large a weight pulls p toward 0.5.

**5. Official-metadata gold block (before training; amends A39 b).**
- **What:**
  - Sonnet writes one mapper per G-block source (11) that turns upstream human/official metadata into 40-80 tasks with program gold.
  - Haiku writes 3-5 wordings per task.
  - Options: 2-8, including near-miss siblings and frequency-weighted negatives. At least 30% card-free; yes 50%; at most 200 rows per task; 8-12K rows in total.
  - Noise gate: Haiku blind-reads 100 rows per task, and a task is dropped above 8% clearly wrong (the same bar as OHS-4 G).
  - Keep a 10% metadata audit holdout.
  - Add a sealed-side, counts-only source-name check. Any source shared with OHS-4 is dropped whole.
- **Metric:** G accuracy. Gain +0.5 to +2.0 pp (estimate).
- **Evidence:**
  - Task-count scaling (Super-NI, Flan).
  - Kev: "breadth, not replay, was the missing ingredient".
  - UniversalNER: frequency-based negatives gave +22 F1.
  - Validated vs unvalidated labels: AUROC 0.872 vs 0.949 (labels shape the measured skill).
- **Cost:** 11 Sonnet mapper agents and about 6-8K Haiku reads; about +$3 of training.
- **Risk:** only 11 sources; multi-label metadata noise.

**6. C1→C2 interpolation dial (after training; dev only; the amendment must be written before training).**
- **What:** θ(α) = C1 + α(C2 - C1) for α in {0.5, 0.6, 0.7, 0.8, 0.9, 1.0}, by scaling the LoRA delta.
  - Choose α by a pre-registered score: G-proxy accuracy plus R mixdev accuracy, subject to the D-gates.
  - Use a paired bootstrap, then ship the merged weights.
- **Metrics:** G accuracy and Brier. Gain G +0 to +0.8 pp (it guards against the spec's expected -0.3), Brier -0.001 to -0.004. It costs a little on R.
- **Evidence and counter-evidence:**
  - For: Gemma-3-4B interpolation +0.76 pp; LoRA pre/post merging beat SFT in 9 of 12 cells.
  - Against: Kev's WiSE-FT toward the base fell 2.9-3.9 pp. That is why this is a dev-gated dial and not a default.
- **Cost:** under $1, on od-l4.

**7. Opus distillation aimed at C1's errors, at breadth (before training; the heaviest Claude cost).**
- **What:**
  - Haiku drafts 150-250 new cards over the 22.8K G-block texts plus 2-4 new sources, giving 40-50K candidates.
  - C1 reads them for free. Keep the rows where C1's top probability is below 0.75 or its margin below 0.3.
  - Haiku labels those rows. Every row where Haiku ≠ C1, or Haiku confidence is below 0.9, goes to Opus, and Opus labels are kept at ≥ 0.85.
  - Target 5-8K informative rows, at most 150 per card.
- **Metric:** G accuracy. Gain +0.5 to +1.5 pp (estimate).
- **Evidence (dev):** Haiku-first with Opus at confidence < 0.6 reaches 85.0% using only 23% Opus calls.
- **Cost:** about 50K Haiku reads and about 8-12K Opus item-reads (160-240 chunks; run on the new account); about +$2-3 of training.
- **Risk:** Claude conventions on Claude-invented cards; must make the Wed 21 Oct cutoff.

**8. Test-time polarity symmetrization (after training; adopt only if it passes dev).**
- **What:**
  - For each yes/no question, also run a trained-polarity view that shares the state's cached prefix.
  - Output p = ½[p(q) + 1 - p(flip q)].
  - Adopt only if, on the Action 0 dev plus the F7 held-out negation probe, complement violation falls by at least 0.02 with no accuracy or Brier loss.
- **What is guaranteed:**
  - zero self-violation;
  - any additive yes-bias cancels exactly;
  - Brier(p*) = mean of the two views' Brier - d²/4.
- **Metrics:** complement violation 0 to -0.03; Brier 0 to -0.003.
- **Cost:** about +5-10% compute on yes/no items; +1-3 ms.
- **Risk:** it does not fix negation-blindness; the flipped view may be weaker; served-path parity must be re-checked.

**Skip:** per-type temperature, label smoothing or Brier losses (the dev null), seed soups (budget), full rotation test-time augmentation (no position bias on dev), selective thinking in the headline setup (it raises cost about 1.5-2.5× and puts p95 at risk; report it only as a separate "auto" mode), a pointer-head swap, bulk label cleaning (0 to +0.3 pp), typo augmentation, cutting replay below 60% for synthetic rows (round 1's old-slice dip of -1.85 was close to the stop rule), and JevBench submission.

## 5. The quantitative case

1. **Brier is accuracy.** -0.0054 per point × 5.3 pts ≈ 0.029, which is at least the 0.022 gap, with T ≈ 1.0. So only accuracy moves G Brier.
2. **The teacher bound on G.** C2 beats Jev only if it captures a fraction f ≥ (Jev - C1) / (Teacher - C1) of the teacher's edge on fresh sources.
   - Opus: 5.3 / 12.7 ≈ 0.42.
   - Haiku: 5.3 / (7.1 to 8.9) ≈ 0.6-0.75.
   - My estimate for one week: f ≈ 0.08-0.2. So Haiku labels essentially cannot win G, and Opus can only with 2-5× more coverage than we can build this week.
3. **Complement violation has no gold term.** |p(q) + p(q̄) - 1| does not involve the true answer. So twins of gold-labelled rows cost no new label risk, and scale is limited only by how exact the negations are.
4. **The forecast model for G.**
   - Assumptions: C1 - Jev on G ~ N(-4.5, 2.0), allowing for OHS-1/2-like sets at -1.3 and -0.5. C2 - C1 ~ N(+1.25, 1.0) with the plan. Sampling SE about 0.8.
   - Result: C2 - Jev ~ N(-3.25, 2.35).
   - P(point win) ≈ 0.08; P(win with a CI) ≈ 0.02; P("close": CI includes -2) ≈ 0.5.
   - With the spec alone: P(point win) ≈ 0.015.

## 6. Per-metric forecast (OHS-4)

| Metric | OHS-3 C1 / Jev | C2 expected | P(beat Jev): spec only → with plan |
|---|---|---|---|
| General accuracy (G) | 74.3 / 79.6 | C2 - Jev ≈ -3.3 (range -7 to +1) | 0.02 → 0.08 |
| Rule/agent accuracy (R) | dev authored 73.0 / 71.6 | C2 - Jev ≈ +5 to +6 (range -2 to +12) | 0.85 → 0.90 (CI-backed in both Jev runs: 0.65 → 0.72) |
| Brier, yes/no: G part | 0.172 / 0.150 (pooled) | about Jev + 0.015 | 0.08 → 0.12 |
| Brier, yes/no: R part | — | — | 0.75 → 0.80 |
| Brier, yes/no: pooled | — | — | 0.35 → 0.45 |
| Complement violation | 0.170 / 0.088 | spec 0.10-0.13 → plan 0.08-0.12 | 0.12 → 0.30 (about 0.4 if Action 8 passes) |
| Hijack (X attack success) | dev 0-1.3% / one audit 99% | 0-3% | 0.88 → 0.90 |
| Injection detection (report-only, not a sealed part) | — / Jev 86.35% (Red Hat) | 85-92% | 0.45 → 0.50 |
| Speed, p50 and p95 at c=1 (S1, US) | Jev 210-219 / 301-319 ms | about 40-80 / 120-180 ms | 0.82 (p95 at c=64: about 0.6) |
| Cost per 1K at 40% use | S1 $0.079 / $0.061 | $0.045-0.065 | 0.15 → 0.50 |

**Combined odds (with the plan; independence assumed, so these are rough):**
- Expected wins: about 4.4 of 8 (spec only: about 3.6).
- P(at least 5 of 8) ≈ 0.4 (spec only: about 0.2).
- P(at least 6 of 8) ≈ 0.2.
- P(all 8) ≈ 0.005-0.01.

## 7. Orchestration and budget

**Who does what (Claude):**

| Model | Jobs |
|---|---|
| Haiku | Cards, wordings, negation rewrites, exactness checks, first-pass labels, blind noise audits (about 100-130K reads) |
| Sonnet | Metadata mappers, trap tagging, card review, 3% audits, script fixes |
| Opus | Only C1-disagreement real-text labels (about 180-280 chunks in total) and the one amendment |

- Put Opus work on the fresh account.
- Follow the HANDOFF usage rule on the current account.

**Modal, about $45:**

| Item | Cost |
|---|---|
| C1 reads, about 110K rows | od-l4 free (fallback: S1 H100 about $3-4) |
| C2 main run, about 100-110K rows (relayed across two free accounts) | up to $28-30 |
| Dev gate, interpolation dial, Action 8 probe | od-l4 free (fallback about $2) |
| OHS-4 look plus SPEED-3 | $3-4 |
| Reserve | about $8 |

- To fit the run under the cap, real-text new rows get 1.0× replay; synthetic rows keep 1.5×. Replay twins count inside the replay budget.

**Amendment A42 (write it before any new rows):**
- Action 2 routing;
- Action 3 selection;
- Action 4 lifting the T37b cap;
- Action 5 changing A39 b, plus the sealed-side source-name check;
- the replay ratio and the $28-30 cap;
- the Action 6 interpolation rule;
- the Action 8 adoption rule;
- the Action 1 cost method;
- the Action 0 dev definition.

**Timeline:**

| Date | Work |
|---|---|
| Wed 14-Thu 15 | Actions 0, 2 (C1 read), 3 and 5 (code), Action 4 rewrites |
| Fri 16-Sun 18 | Haiku verification and audits; Action 7 candidates and C1 read |
| Mon 19 | Opus queue (new account earlier if available) |
| Tue 20-Wed 21 | Decontamination against the OHS-4 exports, mix, data cutoff |
| Wed 21-Thu 22 | Train |
| Thu 22-Fri 23 | Dev gate, interpolation dial, Action 8 probe |
| Fri 23-Sat 24 | One OHS-4 look, then Jev, then SPEED-3 |

## 8. What cannot be guaranteed

- No mathematical proof is possible for unseen sealed data. OHS-4's sources and frames are unknown to us by design, and generalization under distribution shift needs assumptions that cannot be checked before the look.
- What is provable is narrow:
  - averaging views never raises expected Brier above the views' mean;
  - symmetrization cancels additive yes-bias and gives zero self-violation;
  - label noise at rate e adds at most e² to Brier;
  - the teacher-capture inequality in section 5.
- None of these guarantees a sealed win.
- Jev itself is not fixed: 50 identical requests gave 15 distinct answer sets, and its versions drift. So any claim needs both pinned Jev runs.
- The strongest honest claim is: beat Jev on rule/agent decisions, hijack safety, latency, and probably cost and calibration on rules; be close on general accuracy; general accuracy itself is about a 1-in-12 chance this round.

**Key files:**
- `/Users/aryamahadik/Documents/jev/opendecide-data/lean/teach1/C2_DATA_SPEC.md`
- `/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/c2_select.py`
- `/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock/label/ROUTE.md`
- `/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock/label/opus_finalize_A39.json`
- `/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock/SOURCES.md`
- `/Users/aryamahadik/Documents/jev/reports/ROUND1_RESULTS.md`
- `/Users/aryamahadik/Documents/jev/HANDOFF.md`