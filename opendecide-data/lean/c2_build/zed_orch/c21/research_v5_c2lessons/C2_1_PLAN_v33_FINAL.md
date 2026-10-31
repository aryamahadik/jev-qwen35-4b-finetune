# C2.1 PLAN v3.3 FINAL: what C2 taught, and what changes (Sun 18 Oct 2026, about 10 PM ET; Opus reviser)
Replaces the draft C2_1_PLAN_v33_AMENDMENT.md (sha256 fba60a6d...) after the rules skeptic (D1-D21) and the completeness critic (gaps 1-5) of workflow wf_71d7151e-431. Amends
C2_1_PLAN_v3.md (v3.2-r, 60b427ef...) and C2_1_BUILD_ORDER.md (99fb177a...) after C2_REPORT.md (0286b4cd...). TRAINING SIDE ONLY: it merges as plan section 16.10, never into
sections 3, 4, 10 or 11, which sealed agents read (D21). Every item adds or tightens a check. No v3.2, spec or PREREG bar is loosened; where this file and v3.2 differ, the stricter
line binds. Only Qwen3.5-4B, no thinking mode, and no test, sealed or Jev data in any training row, temperature fit or selection set. Tags: measured (file:line), DERIVED,
UNVERIFIED. Paths are under opendecide-data/lean/ unless they start with HANDOFF.md (lines as read 18 Oct). Times ET (EDT to Sat 31 Oct, EST from Sun 1 Nov), UTC in brackets. Read:
the draft, the 4 research files, plan sections 0, 3 (rules), 5, 10, 11, 16, the build order, C2_REPORT.md, PREREG A42-D 9.3-9.6, A45-A50, A72, A77-A105, C2_DATA_SPEC.md 2.1-2.2 and
6.3-7.3, HANDOFF.md:1-300 and cited lines. Disclosed reads (D16): this revision opened one file under ~/.claude (the workflow journal the task named); transfer_levers.md:7
discloses one harness spill-file read there. Both go into PREREG. No ohs, sealed, quarantine, longbench, jevbench, ejs, sealed-brief or preread path and no Jev output was opened.

## 1. Where each defect and gap is fixed
| Item | Fix (section) |
|---|---|
| D1 transfer bar | 3: spec 7.2 (b) BINDS as inherited (A42-D 9.4, PREREG:2638). E-T1/E-T2 are ADDITIONS. No waiver path is built or offered |
| D2 G6 | 4: A50(a) as written on every MONITOR, STOP-only and GATE family. T36r/T20r/T07r are new families (G0-lite + Opus ruling) or are dropped |
| D3 money | 10: one table (account, amount, cap, 1.25x). O1 and O3 wait for the Wed 21 No-Fee check. A82 9 holds the $30 training line, O1 included |
| D4 + gap 4 abstention | 3: E-AB two-sided (missed-abstain). 5: trigger B two-sided. 4: held-out ASK family ASK-H. 6: twins keep ALLOW/BLOCK floors; A46 bias log |
| D5 stop path | 5: segment-boundary verdict file on the Volume (fails closed); union false alarm; a STOP ends C2.1 training unless the owner adds money |
| D6 set roles | 4: MONITOR is a TUNING set. GATE gets a C1 baseline read only. Fresh T19r/T21r. Frozen 2b9702a7 is design-exposed and report-only |
| D7 timeline, PREREG | 12, 13: eval rows only after OHS5_FREEZE.json. One global G0 ruling (G11). PREREG v3.3a Fri 23 and v3.3b Tue 27, full list |
| D8-D21 | D8: 2, 6 (929 abstain-gold new rows, not 1,203; F6 not a driver; IND+ASK cap). D9: 2 (lesson 5 is a hypothesis), 6 (CX contrast). D10: 3-5 (group SEs, thresholds). D11: 8 (KD flags). D12-D13: 9. D14: 7, 8, 11. D15-D21: 14 |
| Gaps 1-2 | 4: decay ladder tiers (a)-(d), validated on C2 (E5). 6: D-1 balances cues across every question form; 3: E-T1 also binds on GATE minus T19r |
| Gaps 3, 5 | 4, 5, 9: PROXY-GATE (pg_dev + dev_nc + devzs) in E-2 trigger G and the pilot, advisory go/no-go. 5: B/C error rates, null controls, union. 9: fallbacks FB-1/FB-2 |

## 2. What C2 taught (corrected)
| # | Lesson | Numbers | Source |
|---|---|---|---|
| 1 | Dev gain did not reach independent items | Mixdev +12.31 [+10.47, +14.15] vs OHS-4 R +1.93 [+0.07, +3.82]: d = 0.16, CI about [0.01, 0.31] (DERIVED); 22% of Jev's 8.6-pt R lead closed | C2_REPORT.md:19,42,120 |
| 2 | Transfer harm is wide | T19 -11.3 [-17.2, -5.6], T21 +1.7. On 13 unseen or near-unseen dev sets the mean is -2.3, 8 of 13 negative (pg_routing -7.3, pg_temporal -6.7). All 18 candidates were negative | C2_REPORT.md:121,170; c2_dev_diagnostics.md App. A |
| 3 | Over-abstention grew | T19 CBD answers 54 (C1) -> 64 (alpha 0.5) -> 76 (alpha 1.0) of 98, vs 26 gold. Compliant recall 30.8 -> 7.7%. Precision 34.2% at 84.4% confidence | c2_dev_diagnostics.md:32-33; calibration.md:89 |
| 4 | Abstention is a third of the T19 loss | Of 34 rows lost: 11 verdict, 9 gap-choice (no abstain option), 14 yes/no. The yes-rate did not move | c2_dev_diagnostics.md:34,140-145 |
| 5 | HYPOTHESIS (E1 tests it): cues, not label rates | IND gold is 27.2% of IND-offering rows (T19 truth 26.5%). T19's nearest neighbours T01/T23 (75% of top-20) have no abstain option. Correlational | c2_dev_diagnostics.md:38,412-423 |
| 6 | Blending is one trade-off line | Alpha 0.5 keeps 78% of the gain and 28% of the loss. Last-3 = final (S +0.00 [-0.24, +0.23]) | transfer_levers.md:64-75 |
| 7 | The monitor was blind, and the draft MONITOR too | Old slice -1.80/-1.15/-0.50. C2 on the draft MONITOR families (report-only mixdev): T33 +2.1, T12 -4.7, "Not shown" +9.4 pp. Only trigger C fires (50% bar), which alone does not STOP | C2_REPORT.md:97-99; diagnostics:84,94,436 |
| 8 | Calibration broke out of distribution | OHS-4 yes/no ECE 4.1 -> 13.2%; Brier +0.0098. Frozen T 0.8 vs pooled optimum 1.10 (1.75 on transfer, 3.25 on T19) | C2_REPORT.md:22,31; calibration.md:51-62 |
| 9 | One pass, at a known price | 0.9901 epoch, 3,673 steps, 186 min, $13.14 = $0.221 per 1K row-passes | C2_REPORT.md:74-76 |
| 10 | Process | No PREREG record named the 600-row transfer set; (b) waived after the result (A100); T21 passed on a single-build G6; T20 ran 3 iterations | C2_REPORT.md:169,218; A99 |
| D8 | Counts | Of 1,203 IND/ASK-gold rows (all 59,340), replay holds 274, new rows 929 (T29 361, T30 242, T28 241, T25 84, F6 1). The "70%" is T29+T28+T30 (844). New rows: IND 0.96%, IND+ASK 3.9%; 2.03% / 0.81% are shares of ALL rows | diagnostics:370-391 |

## 3. C2.1 eligibility (binding; paired vs C1; 10,000 group-bootstrap resamples, seed 0; all candidates read in one job)
A candidate is eligible only if every check in (i) and (ii) passes. Then the highest S wins (v3.2). If none is eligible: no OHS-5 look, C1 stays, OHS-5 stays unspent for C2.2, and
the report says so. No waiver code is built and the plan offers none.
- (i) Inherited, binding as written (A42-D 9.4; spec 7.2, C2_DATA_SPEC.md:959-972): (a) C2.1 trained-family mixdev >= +8.0 pp with LB > 0; **(b) pooled GATE C2.1 - C1 >= +3.0 pp
  with LB > 0**; (c1)-(c7); (d) complement; the A42-D 4.3 G-proxy rule. The comparator is C1 (shipped, and the init under O5).
- (ii) Additions. **E-T1:** one-sided 95% LB of C2.1 - C1 > -3.0 pp on GATE, and also on GATE minus T19r (gap 2). **E-T2:** no GATE family with point <= -7.0 pp and UB < 0. **E-AB,
  two-sided:** over-abstention: on each GATE family with an IND or ASK option, predicted/gold <= C1's ratio (target <= 1.5, report-only); under-abstention: missed-abstain rate
  (gold IND/ASK answered with a commit) on pooled T19r + ASK-H gold rows (about 130-160 rows; T19r alone, about 26, if ASK-H is dropped) <= C1's + 5.0 pp, and on gold-ASK rows of
  the T50/T51/T53 mixdev <= C1's + 2.0 pp. **E-C:** on the calibration pool with the leave-one-domain-out T, mean-domain ECE <= C1 + 1.0 pt; confidence rise <= accuracy change +
  1.0 pt; AURC <= C1 + 0.4. C2 fails (b), E-T1, E-T2 (T19), E-AB-over (2.92 vs 2.08) and all of E-C.
- Stats (D10, DERIVED): paired SE about 1.3 pp at 1,200 GATE rows and 1.2 at 1,500. So (b) needs a point >= +3.0 (its LB > 0 holds above about +2.2), and E-T1 needs a point above
  -0.6 to -0.8. A true-zero model fails E-T1 26-35% of the time and E-T2 about 0.9% per family (4.5% over 5). E-AB-over fails a model with C1's true ratio about half the time,
  which is intended: it asks for less over-abstention than C1.
- **Odds (DERIVED): P(any candidate eligible) is about 5-15%**, set by (b) (uniform prior on a true GATE delta of -4 to +3, SE 1.3, 18 correlated candidates).

## 4. Evaluation sets (transfer dev v3; rows built only after the OHS-5 freeze)
| Set | Families (rows) | Used for | Never used for |
|---|---|---|---|
| MONITOR (TUNING set) | T33 600 ("Not shown in the log"); T12 600. Trained in neither C2 nor C2.1 | E-2 P/F/B/C; E-3 T pool; base-E pick; pilot; E-C pool | eligibility |
| STOP-only | T19m 300 (fresh T19 seeds, disjoint from T19r) | E-2 F and B only (C2 fired both on T19) | tuning, T fit, base E, selection |
| PROXY-GATE (exists) | pg_dev 1,049 + dev_nc 1,008 + devzs 800 (C2 final -1.72 / -1.59 / -1.62; pooled -1.65, DERIVED) | E-2 trigger G input, pilot, advisory go/no-go | new eligibility (already pre-gate D1 inputs) |
| GATE | T19r 300, T21r 300, T24 300, ASK-H 300; optional T36r, T07r, T20r (300 each) | (b), E-T1, E-T2, E-AB at the grid and final only; one C1 baseline read before the freeze (aggregates to the SE program; no bar moves) | tuning, T fit, pilot, E-2, any C2.1 read before the grid |
| Frozen 2b9702a7 (T19 + T21) | 600 | report-only at the grid (comparable with C2's -4.83); design-exposed (it drove D-1) | everything else |
| Decay ladder (gap 1) | per trained family: tier (b) 150, tier (c) 100-150 | d_proxy at E5, the pilot and each E-2 state (report, advisory); E-3 pool | eligibility |
- **G6 (D2):** A50(a) as written applies to every eval generator configuration (dev-only wordings and names included): four independent 6,000-row QC builds at seed bases
  B0/11M/12M/13M, every view x model cell mean <= chance + 2 pp. The builds run in memory before Sun 25 only if the row-start guard has a CPU-tested in-memory QC mode (A45(d)
  precedent), else from Sun 25. A failing family is dropped; no iteration beyond its A48(a) cap.
- **New families:** T36 and T20 failed G6, T20 already used 3 iterations against a cap of 2, and T07 had a confirmed wrong gold (A72). So T36r, T20r and T07r each need a new
  G0-lite, an Opus ruling that it is a new design, A50(a) G6 and 0 confirmed wrong gold, or they are dropped (logged).
- **ASK-H (gap 4):** 2 of T59's 8 triggers are held out of every training row (A24-style), subject to an Opus ruling on the T59 G0-lite (Mon 19-Tue 20; no T59 bar moves). If Opus
  refuses, ASK-H is dropped and E-AB-under runs on T19r alone (disclosed).
- **If GATE is short**, substitutes come in this order: T36r, T07r, T20r, then T12 moves from MONITOR to GATE (decided by Tue 27, before any pilot read). FLOOR: GATE >= 4 families
  and >= 1,200 rows at v3.3b. Below it there is no C2.1 training, and the owner is told that day.
- **Build:** existing generators, new seeds, dev-only wordings, >= 100 groups per 300 rows. Rows only after OHS5_FREEZE.json (BO:32-34, L-0 h), through the stamp wrapper. Generator
  ids and seeds go into the Thu 22 registry; row hashes join Mon 26 as delta targets (16.1 step 6). The row-start guard refuses eval family ids, ASK-H triggers and dev-only names
  in training jobs. Dev-only names go names-only to L-S in manifest v1.2 (Fri 23, 8:00 AM [12:00 UTC]).
- **Ladder tiers:** (a) same-generator mixdev; (b) name shift (dev-only namespace, unseen wordings); (c) restatement: a new template grammar written by a clean-room Sonnet that
  reads only the G0-lite semantics, gold from solver A = solver B on the spec. Opus must rule on Mon 19 that D4's no-LLM-dataset rule does not bar (c), else (c) is dropped. (d)
  GATE.
- **E5 validates the ladder on C2** (Mon 26-Tue 27, free L4): C1 and C2 on tiers (b)/(c) of T28, T29, T30, T26, T01 and T06. Tier (c) is a valid proxy only if C2's pooled gain is
  <= +5.0 pp and its CI overlaps OHS-4 R's [+0.07, +3.82]. d_proxy = gain(c)/gain(a) is report-only (GO #1 input). SEs (D10): 2.2-3.0 pp per 300-row family (T21 2.22, T19 2.96)
  until group-bootstrap SEs on the built sets replace them (v3.3b). Cost: $0 Modal, about 3.5 Sonnet-days.

## 5. Early warning E-2: the only stop rule (replaces plan :1055; the old-slice rule stays inside trigger G)
Reads at the saved states at 8.3%, 25% and 50%; 75% is report-only. The 8.3% read binds only if E2 shows that C2's s000918 already had at least half of its final T19 loss and that
B fired there; otherwise it is report-only. Each read takes MONITOR, T19m, PROXY-GATE, the old slice and a 500-row in-family slice (report-only price ratio), paired vs init (C1) on
raw probabilities, with group bootstrap.

| Trigger | 8.3% and 25% | 50% |
|---|---|---|
| P: pooled MONITOR accuracy | point <= -5.0 pp and one-sided UB < 0 | point <= -3.0 pp and UB < 0 |
| F: any of T33, T12, T19m | point <= -9.0 pp and UB < -1.0 | point <= -7.0 pp and UB < -1.0 |
| B+: predicted IND share where offered (T19m verdicts, T33 "Not shown"), minus init | >= +20 pp | >= +15 pp |
| B-: recall on gold IND rows of the same sets, minus init (under-abstention) | <= -20 pp | <= -15 pp |
| C: MONITOR top-label ECE (10 equal-mass bins), minus init | >= +6.0 pt | >= +4.0 pt |
| G: old slice, G-proxy or PROXY-GATE below init - 1.5 pp | at both 25% and 50% (plan rule shape) | |
- **Decision:** at 8.3% (when binding) and 25%, STOP if any of P, F, B+, B- or C fires. At 50%, STOP if two fire, or one fires at its 25% bar. G as in the plan.
- **Error rates (DERIVED, normal approximation, gap 5):** P false alarm 0.3% / 4.3% at 25% / 50% (its -1.3 / -0.65 pessimism is the old slice's, UNVERIFIED for MONITOR). F 0.5% /
  1.6% per family (about 1.5% / 4.7% over 3 families). B+, B- and C: sampling false alarm about 0-1% (UNVERIFIED). Union about 2-4% per binding read. Power on C2: on T19m-type rows
  F (-11.3) and B+ (+22.4 pp) fire at C2's final; on MONITOR alone only C fires (50% bar, no STOP on its own), so E-2 is a coarse guard. E2 dose-matches by steps (C2's s000918 /
  s001836 correspond to C2.1 at about 13% / 26%).
- **Null controls (E3, Mon 26, free L4):** C1 vs a fresh C1 read on the same path; C1 vs merged C1 + 0.1 x (C2 - C1); a group-bootstrap noise copy. They give each trigger's false
  alarm and the correlated union. No bar moves after this. If the union is above 5% per read, the GO #1 packet says so (a false STOP ends training).
- **Execution (D5):** the chain runs the main run in segments that end at each binding read state. After each read the chain uploads VERDICT_<state>.json (CONTINUE or STOP, the
  numbers, the read sha) to the run's Volume. At segment start the trainer refuses to continue without a CONTINUE verdict for the previous state (fails closed). No `modal app stop`
  is needed; if the upload is refused, nothing launches and the owner is asked. Cost: about 3 extra boots ($0.3-0.6, DERIVED) and 1-2 h of wall time (read time UNVERIFIED; E2
  measures it). Before GO #1: CPU tests, a fresh Sonnet skeptic and a conformance record; the GO #1 packet asks the owner to pre-authorise the uploads in their own words.
- **On STOP:** states kept, no candidate; diagnosis by per-family abstain and cue tables; fallback per section 9. A STOP spends about $2.3 (8.3%) to $12.5 (50%) and leaves a bound
  of at most about $22, below the shed-order minimum (about $24-25, section 10), so **any STOP ends C2.1 training unless the owner adds money** (which also needs an A82 9 lift in
  their own words; DERIVED).
- **Consistency (report-only):** complement, option-order and minimal-edit pair reads at every state and in the grid; an S3-type UB < +1.0 needs about 800 pairs (DERIVED).

## 6. Data
**D-1 Commit-vs-abstain twins, through ONE global G0 ruling (G11)** in Opus batch 1 on Mon 19; every addendum cites it, so no 11 separate edits. Every IND- or ASK-gold row gets a
decidable twin by program: same scaffold, options and cue, one fact toggled, commit gold. Twin commit labels follow each family's ALLOW/BLOCK class floors (gates >= 45% ALLOW; T41c
50% benign; D4); twins substitute inside each family's size through the stamp wrapper.
- **Form-complete cue balance (gap 2):** every uncertainty cue (missing, not recorded, expired, out-of-scope unknown) appears both relevant and irrelevant (off-path, gold = commit)
  in every question form (verdict, yes/no, gap/pick), with irrelevant >= relevant rows per cue x form. Gap-order twins cover both orders.
- **Pre-freeze kill gates (CPU):** 100% twin coverage. Cue-only probe held-out AUC <= 0.55 (UB <= 0.60) per form, against IND/ASK, yes/no and gap golds. IND gold <= 33% of
  IND-offering rows per family. IND <= 5% and IND+ASK <= 9% of all new rows (C2 new rows: 0.96% and 3.9%). ASK shares as each approved G0-lite sets them (T59 ASK <= 45%).
- **Evidence and cost:** Bianchi: 2.5-5% refusal rows helped; 9% gave over 50% exaggerated refusals (calibration.md:133). Effect size UNVERIFIED. $0; about 0.5 Sonnet-day per lane;
  due Sat 24, 2:00 PM ET (18:00 UTC).
- **D-2 Replay twins:** the 929 abstain-gold new rows of C2's mix each get a decidable twin from their own generator (new seeds, stamped at creation). Each twin replaces a
  commit-gold replay row of the same family, so the count is unchanged. Twins are NEW rows: OHS-AC binds (R4 does not apply) and there is no KD (D11). The 195 dataset-native
  "unknown" golds (boardgameqa 126, logicinference 36, babi 33) stay. $0; about 1 Sonnet-day, Sun 25-Mon 26.
- **CX contrast (D9):** about 400 T01 and 400 T23 rows where a missing or unrecorded record is decided by the stated rule (IND gold <= 33%). They replace as many T01/T23 replay
  rows and are new, binding and no-KD. Needs a G0 addendum, Opus, A50(a) G6 and G5-H; the kill rule applies.
- **D-3 Block R** (about 24,600 rows, 60-70 sources) is kept, the main breadth lever (Super-NI is log-linear in task count). Each source's abstain-like gold share is measured
  before mixing, ASK-type dialogue sets (ABCD, MultiWOZ, Taskmaster) included. Above 33%, a seeded drop brings it to 33%. No family or source may exceed 8% of non-replay rows. A46
  bias log (gap 4): every screen-drop log shows the abstain-type mix (gold type x top answer type) of dropped vs kept rows per source. A gap above 5 pp goes to Opus before the mix.
  The screen stays drop-only (no row is restored), and the 33% cap runs after it.
- **D-4 Calibration data:** the A29/PR-5 buffer of 200 rows per type and option bucket (never trained, outside the T pool). The A24 held-out sub-families are split item-disjoint
  50/50: half A to the T pool, half B to S and E-C (D20). D-1 twins aim at confidently wrong rows (C2's false CBD answers averaged 0.817).

## 7. Calibration: E-3 temperature protocol (replaces plan :1027-1028 and the L1 median-of-groups rule), and E4
- **Fit:** one T per question type; for choice, one per option bucket, only for buckets with >= 300 pool rows. Pool: MONITOR, D2 (3,847), devzs, dev_nc, A24 half A, ladder tiers
  (b)/(c), and mixdev (at most 1/3 of the weight). Never fitted on GATE, ASK-H, T19m, the frozen file, sealed sets, a single family or medians of sub-100-row groups.
  Domain-balanced NLL over 0.25-10.00 (step 0.05), bounded [1.00, 2.00]; a type at a bound, or a per-domain spread above 2x, goes to Opus.
- **Report:** ECE at T = 1, at the shipped T and at a 5-fold cross-fitted T, plus Brier, NLL, AURC and E-AURC. S's post-T term and E-C use the cross-fitted / leave-one-domain-out
  T, never the shipped T (D20).
- **Measured on C2 dev (D14):** the adopted domain-balanced protocol went 9.18 -> 8.27 (-0.9 pt); pooled-NLL leave-one-domain-out gave -1.4 to -2.5; C1 sits at 6.2-6.6. T19 needs T
  near 3.25, so no scalar T fixes a T19-type collapse.
- **What stays fixed:** a method fix made before any C2.1 result; the 3.5% ship gate and the <= 3.0% claim rule do not change. The claim metric is the plan's aligned ECE (plan
  :790-794), with Brier beside it. Jev's Brier lead over C1 (+0.066 R, +0.036 X) is mostly accuracy (2a(1-a) gives 0.075 / 0.038; DERIVED, rough), so no T closes it.
- **E4 (D17; mandatory; sealed-scope session only; by Thu 22):** re-scores the spent L1 OHS-4 predictions at T = 1 and at the E-3 T (T passed by number only); aggregates only (ECE
  and Brier by part x card/no-card x type), labelled post-hoc report-only. It cannot alter E-3, E-C or any bar. Its one use: if the E-3 T does not lower C2's OHS-4 yes/no ECE vs
  the frozen T, the GO #1 packet says the fix is unvalidated on independent data.

## 8. Training recipe
- **T-1, one pass:** epochs = 1.00 (replaces :919; :969 becomes "per pass"). DERIVED at $0.221 per 1K row-passes: 112.5K rows = 7,031 steps, 5.9 h, $24.9; 125K = 7,812 steps, 6.6
  h, $27.6. Both exceed the one-account bound of $24, so the pre-registered order sheds on the measured Mon 26 projection (R12 stage B first). C2.1 still runs about 1.9x C2's steps
  at the same LR (gap 5); the guards are E-3, E-C, trigger C and base E, not an untested LR change.
- **T-2, optimiser held:** lr 5e-5 cosine, batch 16, r16 / alpha 32 / dropout 0.05, continuing the init adapter (continuing beat fresh, 80.4 vs 65.7). Targets = C2's ACTUAL set:
  MLP in 32 layers, GDN in_proj_*/out_proj in 24, q/k/v/o in 8 (GDN 34.6%). This corrects :922 to match :915 ("same as C2"); the A19 audit asserts it.
- **T-3, replay:** count unchanged (38K at C2 init, 57K at C1 init; a ceiling). KD flag per row source (D11): rows C1 trained on, KD 0.5 to C1 (as C2); rows new in C2, no KD (as
  C2); D-2/CX twins and all C2.1 new rows, no KD (A1 only if the pilot adopts it). Ibrahim (D14): loss falls steeply from 1% to 25% replay (3.56 -> 2.33) and is flat from 25% to
  50% (2.33 -> 2.24); C2.1's 34-46% sits on the flat part.
- **T-4, states:** 12 states, one every 1/12, each exported to the L4 queue.
- **T-5, grid** (18 points; grid sha before any look): 12 alpha/gamma points on the final state F and 4 soups. The 2 last-K points are dropped for base E at alpha 0.8 and 1.0,
  where E = the state at >= 50% of the run with the lowest MONITOR NLL, picked by program.
- **T-6, selection:** section 3 filters first, then the highest S. **T-7:** R12 stage B is unchanged and the first item shed.

## 9. Pilot (O1), fallback recipes, and RL (O2)
- **Pilot design:** two arms of 10,000 rows each, drawn by the full-mix rules from rows that exist by Tue 27. A0 = the pre-registered recipe; A1 = A0 + KD 0.5 to C1 on NEW rows
  (RL's Razor: KL to the base on the new task predicts forgetting, R^2 0.71). Same seed, one pass of about 625 steps, and the same trainer build, so the chain, the state export and
  the verdict gate are tested before the paid run. Reads (free L4): MONITOR, T19m, PROXY-GATE, the calibration pool, the ladder tiers and pilot-family dev; never GATE or ASK-H;
  arms are never candidates. At step 50 of A0, if the projected two-arm cost exceeds the hard stop, both arms shrink equally (floor 5,000 rows each); below the floor the pilot
  stops and is reported. A1's extra teacher passes are counted (D13).
- **Pre-registered uses:** (1) if A0's annealed end state fires any trigger at the **50%-read** bars, one drop-only fix (FB-1 attribution) before the freeze. (2) A1 replaces A0
  only if MONITOR + PROXY-GATE gain >= +1.5 pp with one-sided LB > 0, pilot-family dev >= -1.0 pp, and pool ECE no more than 0.5 pt worse. (3) Measured s/step and $ per row-pass
  replace the projection. (4) A85/A86-type bugs surface before the paid run. (5) **Advisory go/no-go (gap 3):** if the better arm's PROXY-GATE delta vs C1 is at or below C2's
  dose-matched s000918 delta (from E2), or d_proxy is no better than C2's, the GO #1 packet recommends NO-GO and says why; the owner decides at GO #1.
- **Fallback recipes (gap 5), only for a relaunch the owner funds and approves:** FB-1: if the STOP diagnosis puts >= 50% of the trigger excess on one block, that block is dropped
  (drop-only) and nothing else changes. FB-2: otherwise the A1 recipe runs on the same mix. At most one relaunch; GATE is first read at its grid, so there is no second look.
- **O2, RL-like stage (default NO):** if bought, it starts from state F right after stage A, before any grid read; its 2 points sit inside the 18, in the grid sha (D12). Recipe: a
  new r16 LoRA on 10-20K balanced TRAIN prompts with p(gold) in [0.05, 0.95]; loss -E[reward] + Brier + beta x KL (to C1 on replay rows); no abstain reward on determinate rows; lr
  1e-5 to 2e-5. A shuffled-gold control arm is mandatory; a point is adopted only if it is eligible and beats the control by >= 1.0 pp on MONITOR with LB > 0. Cost $2.2-4.4 per arm
  (rl_vs_sft.md:144-146), $4.4-6.6 with the control. Expected transfer 0 to +2 pp; it does not fix a T19-type collapse.

## 10. Money (D3). R1: Modal total <= $35 and training <= $30; A82 9: NO raise of the $30 training line; one account >= 1.25x the projection
| Line | Account | Expected (DERIVED) | Hard cap | Live credit needed | Counts in |
|---|---|---|---|---|---|
| O1 pilot (2 arms) | mahadikarya2, October leftover ($5.97, HANDOFF.md:619; live check first) | $4.4-4.7 (+/-2x row length) | $4.75 (or live / 1.25 if lower) | $5.94 | training $30 |
| Main run (stage A; stage B shed first) | mahadikarya2, 1 Nov renewal ($30 per account, HANDOFF.md:2650) | $24.9 (112.5K rows) / $27.6 (125K), then shed | min($30 - O1 actual, live / 1.25) = $24.00 | $30.00 | training $30 |
| O3 post-training H100 (grid of 19-20 models, parity, the one R9 look) | mahadikarya3, 1 Nov renewal (the relay) | about $10 (C2: $8.86 x about 1.2 rows) | $12.00 | $15.00 | Modal total |
| O2 RL stage (default NO) | mahadikarya2 | $4.4-6.6 with the control | $7.00 | | training: does not fit |
| Jev read (OpenRouter, not Modal) | existing key | about $2.4 | key balance | | outside Modal |
- **Gates:** O1 and O3 run only if the Wed 21 No-Fee terms check does not bar them; O3 also needs it to clearly allow the m2 -> m3 relay, else the free L4 ($0, grid about 33 h,
  +1.5 days). O1 also needs the owner's own words, because R1 puts training on the 1 Nov credit (R15 dropped); it uses credit that lapses at renewal.
- **Totals:** training line = O1 $4.75 + main $24.00 = $28.75 by default, and at most $30.00 on the O4 top-up path, so A82 9 holds. Modal total at caps is $40.75-42.00, over R1's
  $35 by up to $7.00 (O6). Expected about $38.5. The card is never used.
- **Shed-order risk (DERIVED):** at C1 init, after shed steps 1-8, the mix is about 112-115K rows, about $24-25 at C2's per-row rate (per token probably more; Sk 11). Step 9 (ask
  the owner) is likely; O4 covers it.

## 11. Projections vs Jev (DERIVED ranges with formulas)
| Dimension (owner target) | Anchor (measured) | Formula and range | Depends on |
|---|---|---|---|
| Coding/agent (+15 to +20) | OHS-4 R: Jev 1.13 76.00, C1 67.40 (C1 - Jev -8.60 [-11.11, -6.18]), C2 69.33 | C2.1 - Jev = (C1 - Jev) + d x G_dev, with C1 - Jev -8.6 to -2 (UNVERIFIED for coding gates), d 0.01-0.31 (C2's CI), G_dev +10 to +20 (C2 +12.31): **about -8.5 to +4, centre about -3**; each +0.1 of d adds about +1.5 pp; C-transfer at or below this | d: ladder (c) at E5, pilot, E-2 states |
| Headline (plan :773: C2.1 - Jev >= +5 AND C2.1 - C2 >= +3, LB > 0); owner +15 to +20 | as above | Headline: above the supported range (needs d >= 0.35 if Jev leads by 2, >= 0.68 if by 8.6, at G_dev +20). Owner target: needs d x G_dev >= 17-29, i.e. d >= 0.85 at G_dev +20 or G_dev >= 106 at d 0.16: **OUTSIDE the supported range**, 11-16 pp above its top | as above |
| Dev GATE (b) | C2 -4.83; 13-set mean -2.3 | About -4 to +3, centre about -0.5 (D-1 recovers about a third of a T19-type loss: +0.7 on a 5-family mean); (b) needs >= +3.0: odds 5-15% | block R, twins, CX |
| General (within 2-4; ship <= 4.0) | OHS-4 G: Jev - C1 = Jev - C2 = 2.12 [0.66, 3.57] | 2.12 - block-R gain (0 to 1.5, UNVERIFIED) + mix-growth erosion (0 to 1.6; C2 dev_nc -1.59, devzs -1.62) +/- 1 for new G sources: **about 0 to 4.7, centre about 2.2** | public-G panel arms before GO #1 |
| Security (beat Jev) | X acc: Jev 73.84, C1 69.40, C2 68.51; ASR C1 1.04%, C2 0.52% (2/192, 1/191) | K/X non-inferiority (<= max(C2 + 2, 3%)): likely. X accuracy vs Jev about -6 to +2. An ASR win needs about 430 clean pairs per arm (DERIVED); Jev's ASR unread | OHS-5 K/X 1,550 |
| Calibration (beat Jev) | Jev 1.13 aligned ECE 3.2-3.3% (1.14 may differ); OHS-4 yes/no ECE C1 4.1%, C2 13.2% | 3.5% gate: plausible on G (C1 2.78 general dev), uncertain on C (36% transfer; C1 6.9 there even at the oracle T). The claim (<= 3.0% + paired win): unlikely | E-3 (-0.9 measured), D-1, E-C |
| Speed / cost (beat Jev) | C1 p50 14.1 ms server-side (H100, batch 1); Jev 156 ms end to end by our client; Jev $0.042/M input | Not like for like; C1/C2.1 end-to-end latency is unmeasured (D14). Cost wins only above about 59% utilisation | SPEED-3 dry run on C1 by Fri 30 |
- **Plain message:** plausible wins are complement and option-order consistency (C1 and C2 already beat Jev on OHS-4), attack-success non-inferiority, and speed once SPEED-3 runs.
  Staying within 4 pp of Jev on general text is likely. The +5 coding headline is above the supported range, and the owner's +15 to +20 is outside it. With (b) binding, the most
  likely outcome is no eligible candidate, no OHS-5 look, and C1 stays. First evidence: E5, the pilot, and the 8.3% / 25% reads.

## 12. Timeline (ET; UTC in brackets for record times)
| When | Item | Modal $ |
|---|---|---|
| Sun 18 evening - Mon 19 morning | This FINAL. Fresh Opus skeptic, then merge as plan 16.10. One owner message with O1-O6 (O1/O3 conditional on Wed 21; O4/O6 amounts confirmed at GO #1, per A88). Opus batch 1: G11, ASK-H, T36r/T20r/T07r, the tier (c) D4 ruling | 0 |
| Mon 19 after 11:00 AM [15:00 UTC] - Tue 20 | E1 cue audit (CPU, plus an L4 cue-ablation read on the design-exposed file). E2: C2 states s000918/s001212/s001836 and final on the frozen file, T33/T12 mixdev and PROXY-GATE (L4 free after the old grid job ends; read time measured) | 0 |
| Tue 20 - Fri 23 | Eval generators, ladder (b)/(c) and ASK-H code; verdict chain, T fitter, eligibility code, state export and KD flags, each with CPU tests, a fresh Sonnet skeptic and a conformance record; in-memory G6 if the guard allows it; E4 by Thu 22; Wed 21 No-Fee result and L4 queue plan | 0 |
| Fri 23, 8:00 AM [12:00 UTC]; Sat 24 | Fri: PREREG v3.3a (section 13); dev-only names into manifest v1.2. Sat 2:00 PM [18:00 UTC]: D-1/G11 conformance signed; 7:59 PM [23:59 UTC]: OHS-5 freeze target | 0 |
| Sun 25 - Mon 26 | Rows start with twins at creation. Eval rows (MONITOR, T19m, GATE, ASK-H, ladder) generated, then A50(a) G6. D-2 and CX twins. Mon 26: delta stamps, E3 null controls, C1 GATE baseline, E5, measured cost projection | 0 |
| Tue 27, 8:00 AM [12:00 UTC] | PREREG v3.3b (shas, G6, SEs, union false alarm, E2/E5 results, the 8.3% decision); GATE floor check; pilot mix built | 0 |
| Wed 28 | O1 pilot (2 arms, about 1 h of H100) and L4 reads (1-2 h) | <= 4.75 |
| Thu 29, 8:00 AM [12:00 UTC] | Pilot decisions; advisory go/no-go; EARLY or FALLBACK declared | 0 |
| EARLY | Freeze Fri 30, 8:00 AM [12:00 UTC]; GO #1 packet Sat 31; Sun 1 Nov credit check, GO #1, train (6-7 h + 1-2 h of read pauses); grid Mon 2 (H100 about 1.7 h with O3, about 33 h on L4); GO #2 Tue 3 (Wed 4 on L4); R9 Wed 4 (Thu 5); report about Fri 6 - Sat 7 | <= 25.25 + 12 |
| FALLBACK | Freeze Mon 2 Nov, 6:59 PM EST [23:59 UTC]; train Wed 4; grid Thu 5; GO #2 Fri 6; R9 Sat 7; report Mon 9 (L4 grid +1.5 days; latest about Wed 11 - Sat 14). If no candidate is eligible: no R9 look; the report follows the grid by a day | same |
- **Slips, usage:** a Mon 26 sealed slip or L4 contention moves v3.3b to Wed 28 and the pilot to Thu 29 (EARLY then unlikely). The FINAL adds about 6 Sonnet-days, launched only
  under the measured usage projection (BO global 4), never cut by estimate (A47); the addenda campaign (HANDOFF.md:155-163) stays critical.

## 13. PREREG list (D7: every new number registered before any C2.1 row exists)
- **v3.3a, Fri 23, 8:00 AM ET:** (1) eligibility, section 3: (b) inherited; E-T1 pooled and on GATE minus T19r; E-T2; E-AB both sides with 5.0 / 2.0 pp margins; the three E-C bars.
  (2) Eval sets, section 4: roles, isolation, the A50(a) G6 rule, T36r/T20r/T07r and ASK-H conditions, substitution order and floor, ladder tiers and the C2 validity rule. (3) E-2,
  section 5: read points and the 8.3% condition, inputs, every bar, the decision rule, the null-control method, the union notice rule, the verdict-file procedure, STOP
  consequences. (4) E-3 and E4. (5) T-1 to T-7, incl. KD flags and the base-E rule. (6) D-1/G11 gates and caps, the D-2 count, CX, D-3 caps and the A46 bias-log threshold, the D-4
  buffer and A24 split. (7) Pilot design, step-50 rule, use thresholds, advisory rule. (8) FB-1 / FB-2. (9) O2 thresholds. (10) The money table. (11) The disclosures (D16).
- **v3.3b, Tue 27, 8:00 AM ET, before any pilot or C2.1 model read:** eval file shas, G6 results, group-bootstrap SEs, null-control false-alarm rates per trigger and for the union,
  C1 GATE baselines (aggregates), E2 and E5 results, the 8.3% decision, any T12 substitution.

## 14. Notes (D15-D21 and smaller items)
- **D15:** the comparator is Jev 1.14 (plan :767, :886); every Jev 1.13 anchor here (OHS-4 J, Rafe and Das) may differ. **D16:** both disclosed ~/.claude reads go into PREREG with
  v3.3a. **D17:** E4 is in section 7; OHS-4 stays report-only for C2.1 (plan :795).
- **D18:** section 11 shows the formulas, d's CI and the :773 clause (C2.1 - C2 >= +3). The draft's +13 corner (d = 0.5, about 3x the observed 0.16) is dropped as unsupported.
  **D19:** HANDOFF citations re-pointed to the current lines: 155-163 (addenda), 586-589 (L4 pace, credit), 619 (m2 $5.97), 1520 (11 rows/s), 2650 ($30 per account).
- **D20:** cross-fitted T for S and E-C, and the A24 split (section 6). **D21:** merges only into plan 16; O1-O6 go in the owner message and 16.10.
- **Smaller:** the G-proxy is saturated (98.68), so PROXY-GATE joins trigger G. SPEED-3 gets a dry run on C1 by Fri 30. Plan :919, :922, :969, :1027-1028 and :1055 are replaced as
  stated. R14 as written gives init C1 (C2 failed S3 and S4, not only S1; C2_REPORT.md:200).

## 15. OWNER DECISIONS (money and scope only; one message Mon 19; recommended defaults)
| # | Decision | Recommended default | Exact money | Needed by |
|---|---|---|---|---|
| O1 | Pilot fine-tune (2 arms x 10K rows) on mahadikarya2's October leftover, counted inside the $30 training line | YES, if the Wed 21 No-Fee check does not bar it | expected $4.40-4.70; hard stop $4.75 (needs >= $5.94 live, otherwise live / 1.25) | Tue 27 Oct |
| O2 | RL-like stage B, with its mandatory shuffled-gold control | NO in C2.1 (a C2.2 candidate) | $4.40-6.60, cap $7.00; fits only if the owner lifts A82 9's $30 line by up to $7.00 in own words | Thu 29 Oct |
| O3 | Post-training H100 reads (grid of 19-20 models, parity, the one R9 look) on mahadikarya3's 1 Nov renewal | YES, if the No-Fee check clearly allows the relay; otherwise the free L4 (+1.5 days) | expected about $10.00; cap $12.00 (needs >= $15.00 live) | GO #1 |
| O4 | Training line, and the shed-step-9 case | KEEP A82 9 at $30.00 (O1 included). If the measured projection after shed steps 1-8 is $24.00-25.25, top up mahadikarya2 by up to $1.60 so one account holds 1.25x; above $25.25, wait or shed (no lift) | $0, or a top-up of up to $1.60 | GO #1 (about Sun 1 Nov) |
| O5 | R14 init branch | C1, as the rule reads (C2 failed S3 and S4); sets the 57K replay count | $0 | Mon 19 Oct |
| O6 | R1 Modal total, under A88's offered $10-15 (amount named at GO #1) | Raise $35.00 to $42.00 (+$7.00) = training $30.00 + O3 cap $12.00; if NO, O3 runs on the free L4 | +$7.00 of cap (about $38.50 expected) | GO #1 |
- Under the defaults, Modal spend is at most $42.00 (about $38.50 expected), plus about $2.40 OpenRouter for the Jev read. The card is never used. Any E-2 STOP ends C2.1 training
  unless the owner then adds money.

