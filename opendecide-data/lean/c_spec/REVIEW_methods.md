**Skeptic review of C_DATA_SPEC.md and C_TRAIN_RECIPE.md (methods and statistics)**

Bottom line: there are 4 blockers. (1) The public block brings back 5 datasets our own reviewers already rejected. (2) The round-1 rule contradicts the owner's recorded decision. (3) As written, the gate almost never ships a better C, and the expected-value section ignores that. (4) The sealed suite is too close to the training families to serve as the headline test. Two simulations back the gate numbers. Both run on assumptions I chose, so treat those numbers as rough. They are in `/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad/gate_sim.py` and `dev_sim.py`.

## Blockers

**B1. The public list brings back 5 datasets our own reviewers rejected.** The rejections are recorded in `golden_src/*/rejected.json` and in the builder docstrings.
- **ShARC** (C_DATA_SPEC.md:314, and an F5 base at :184). About 15-20% of golds were wrong in roughly 34 hand-checked yes/no rows. The errors cluster on negatively phrased rules (`nli_logic_reasoning/rejected.json`). That is the exact skill F5 is meant to fix.
- **Measuring Hate Speech** (:357, and an F5 base). It is listed in ohs3/used_sources.json as "avoid", and it had an eval_zs role. Three rejected.json files and `build_mhs_hate.py` record this.
- **CAD-SNLI** (:318, and an F5 base). SNLI is "avoid" in used_sources. Its sibling in the same release, `counterfactually-augmented-imdb`, is in forbidden_label_nli.json. The ETHICS-utilitarianism rejection already applied a sibling rule like this.
- **Social IQa** (:348). Rejected twice: about 3 of 30 train golds wrong and about 8 of 30 with a second right answer. It also has no licence in the card or loader, and its contexts come from ATOMIC, whose delta-ATOMIC task is forbidden.
- **CosmosQA** (:349). The licence is only second-hand ("as reported via email"). The Spinn3r blog text has unclear rights, and the train labels were never validated.
- **Sealed candidates.**
  - MultiDoc2Dial was rejected because its licence appears only on the HF card (`intent_business_support/rejected.json`).
  - NLU++ sits in a group that is listed in used_sources (`large_labelsets/rejected.json`).
- **Fix:**
  - Drop all five, about 8K round-2 rows plus their F5 bases.
  - Make every `rejected.json` a deny-list that the program checks.
  - Drop MultiDoc2Dial and NLU++ from the sealed candidates.

**B2. The recipe's R1 rule contradicts the owner's decision.**
- The memory note (3 Oct, about 06:30 UTC) says round 2 runs only if round 1 shows a clear sealed gain: about +2-3 pts, CI lower bound above 0, and no harm to dev, security, calibration or option order.
- R1 in the recipe (C_TRAIN_RECIPE.md:192) is only "K* - REF >= 0" on the select half, where K* is the best of 4 candidates. In my simulation R1 passes about 86% of the time.
- The owner's rule passes only about 28-38% of the time with the current suite size.
- The memory also says the adopted anchor applies "only where confident". The recipe (:101) says "only where right".
- **Fix:**
  - Write the owner's rule into R1, applied to one pre-registered candidate.
  - State P(round 2 runs) in the plan.
  - Align the anchor rule with "where confident".

**B3. The gate as written rarely ships a truly better model, and section 10 assumes C always ships.**
- **P1 (sealed confirm half):** the rule "LB > -1" is the binding one. It needs a point gain of about 1.2-1.7 pp at SE 1.0-1.4 (800 items, 10-15% disagreement between models on far domains). Power at a true +1.5 pp is about 45-60%.
- **D1-D8:** about 10 point-estimate checks.
  - Several are tighter than PREREG_FINAL 3.3:
    - yes/no and choice -0.5 instead of -1.0;
    - Brier +0.003 instead of +0.005;
    - flips +1 pp instead of +2 pp.
  - For a model that is neutral to slightly better on dev, all dev checks pass together only about 20-28% of the time. Under the existing PREREG thresholds the same model passes about 50-67% of the time.
- **P2:** "any of 8 domains below -6 pp" at n = 200 per domain vetoes a good model by chance about 15-25% of the time.
- **Net:** P(ship | true sealed gain above +1 pp) is about 9-14%. The expected shipped gain is about +0.2-0.4 pp.
- **Section 10 consequence:** P(shipped model >= Jev on OHS-3) is about 35-45%, not the roughly 60% the section implies.
- **Fix:**
  - Grow sealed part A to at least 3,200-4,000 items. This costs agent time, not GPU.
  - Keep 1-2 candidates per round and drop K2 and K3. A11, FREEZE finding 5 and Kev all found t < 1 flat or worse.
  - Reuse PREREG_FINAL 3.3's thresholds, or confidence-bound non-inferiority rules.
  - Make D5, D7 and D8 report-only.
  - Change P2 to a lower-bound rule or a -8 pp floor.
  - Calibrate every threshold on the A11 near-null pair (wise090 vs b100 dev reads).
  - Rewrite section 10 around P(ship).

**B4. The sealed suite is not independent enough to be the headline test.**
- **Program-built domains:** 3 of the 8 part-A domains (37.5% of the items) are program-built by a Claude agent. They use the same skill types as F1-F13. That is "same family, new theme", the exact pattern where dev's +2.5 did not transfer to ejs-5.
- **Adjacent real-text domains:** up to 3 of the 5 real-text domains may be adjacent: ASRS and FRA are incident reports, and C1 has 9.8% government incident text.
- **Format styles:** the 50 held-out styles are shared with the mix-tuning dev (:474). They are also built in step 4, after the suite has to be frozen in step 1.
- **Leaked names:** the spec every C builder reads names the candidate domains and the example themes (:590).
- **Label filter:** "zero confirmed wrong golds" by a Claude blind read (:598) would keep only items that LLMs agree with. That biases the suite and shrinks the gains it can show.
- **Label leakage:** NTSB was rejected because narratives state the coded outcome word for word. ASRS and FRA carry the same risk.
- **Fix:**
  - Run P1 on real-text domains only, with at least 4 non-adjacent ones.
  - Make the program-built domains report-only.
  - Give the sealed agent its own format styles.
  - Remove domain names and themes from the shared spec.
  - Use rule-based label filters, not model agreement.

## Should-fix

- **S1. Replay rows where C1 is wrong are mostly label noise.**
  - golden_train is 2.7% wrong and 6.3% ambiguous; legacy replay is about 6% wrong (GOLDEN_CARD.md).
  - Rows C1 still misses after one epoch are where mislabels collect. Cross-entropy pushes hardest on them.
  - Fix: drop or audit replay rows with p_g < 0.2.
- **S2. The anchor softens clean labels.**
  - Fix: anchor only where p_top >= about 0.8. Evidence: softened targets cost Kev 2.0 pp on WANLI; decider's KL replay cost 2.7 pp on the hard tier, and ECE went from 0.046 to 0.147.
  - The A5 targets are two-view averages, so the step-0 KD loss is not zero. Disclose this.
- **S3. The commit block is weighted wrongly.**
  - ejs-5 vs Jev by task: route 0.0, triage -4.7, score -5.0, gate -7.2 (`bench/ejs5/runs/scores_c1_4be.json`). Yet the spec gives route 25% and gate 15%.
  - Fix: about route 10%, gate 30-35%, triage 20%, score 25%, match 10%.
  - Score prompts: show the numstat line. Without it the label needs counting in one pass.
  - Route prompts: hide file headers, or route becomes string matching.
- **S4. The ejs-5 gain is overstated, and ejs-5 now counts as in-domain.**
  - Late rows (n = 268, from 1 June 2026): C1 46.3 vs Jev 45.9. Early rows: about -6.5 (derived from the totals).
  - Jev's base may have seen n8n's history before its cutoff. This is only suggestive (z about 1.9). Commit data from other repos cannot supply that knowledge.
  - The paired SE is about 1.75, not 1.5.
  - Fix: shrink the median gain to about +1. Label ejs-5 "in-domain" in the table. Use the late rows as the cleaner read.
- **S5. The negation evidence is weak.**
  - JevBench hard yes/no is 9/19 vs 11/19, a 2-item gap, on 4B-E's own development set (`bench/v154/RESULTS_30sep.md`).
  - Dev shows no C1 negation weakness: neg 87.6 vs 85.4, dneg 85.1 vs 84.5.
  - The 53% flip rate comes from 60 pairs on one noisy source (hate).
  - Fix: size F5 and the negation quotas from the round-1 probe.
- **S6. F2's 2-6 arithmetic operations conflict with competitor evidence.** "One pass cannot do multi-step arithmetic" (decider, JPT). Rule paragraphs scored 0.24 vs 0.67 for one sentence.
  - Fix: at most 2 operations, or state the intermediate values, with at most 10% deep items as the depth sweep. Specify that sweep; it is referenced but never defined.
- **S7. Only 2 training samplers per family.** This invites the sampler paradox (99.9 → 57.3) and Kev's saturation (+26 pp, then +5).
  - Fix: at least 4 samplers per family, at most about 2,500 rows per sampler.
- **S8. Selecting by C1 difficulty will break yes/no balance.** C1 leans "yes", so gold-"no" rows are harder and the G9 chi-square fails by construction.
  - Fix: downsample within label × wording strata. Add the base 4B and 4B-E as a scoring crowd.
- **S9. The between-round weight update follows noise.** With 200 items per family the SE is 2.5-3.5 pp, and seed noise comes on top.
  - Fix: at least 400 items per family and p < 0.05, or keep the mix uniform.
- **S10. Long relation units can run out of memory.**
  - F13 twins plus permutation twins can reach 24-47K tokens in one micro-batch. `_est_tokens` (chars/3.2) undercounts code and JSON.
  - Fix: a pre-flight check on maximum unit tokens with the real tokenizer, and a smoke run on the largest units.
  - The 30% token cap is likely broken at the planned counts: about 31-34%.
- **S11. The mean P(yes) stop threshold of 0.05 is too loose.** Fix: use 0.02, and log KL(REF‖C) on the old slice.
- **S12. Decontamination method 4 cannot run in blind mode.** Its threshold needs hand-checks. Fix: set the threshold on open sets, then apply it blind.
- **S13. Code and recipe disagree on the dev thresholds.** The D-rule thresholds differ from `gate_dev.py --mode ship`, yet the recipe says it uses the existing machinery. Fix: change the code and its tests, or reuse the existing thresholds.
- **S14. Real-document seeding is missing.**
  - About 67% of new rows are invented-domain Claude text. Li et al. 2023: real data beat zero-shot synthetic by 16.9 pp, and real seeds added 10.3 pp.
  - The sealed real-text domains are code-book classification, which F1-F9 do not train.
  - Fix: add real-text F10/F11 variants: licensed narratives, Claude-written codebooks, program labels.

## Notes

- **N1.** The "-0.6 pp OHS-like" starting gap cannot be traced. The brief gives -3.1 / -1.0, the ledger gives -1.6 to -3.7 for older 4Bs, and `logs/b_wiseft_result.json` is empty (0 bytes).
- **N2.** The 100-row founder audit is about 6-8 rows per family, too few to catch a family-level bug. Claude both writes and blind-reads, so errors correlate. Audit 30 rows per high-risk family instead.
- **N3.** The old slice is C1's own training rows. It measures retention of seen rows, not generalization, which makes D7 weak.
- **N4.** Seed noise (Kev: ±1-2 pp) is not in the item bootstrap. It matters when reading R1 as "breadth works", not for the shipped model.
- **N5.** Use F8's `gold_probs` only for "which outcome will happen" questions. More soft yes/no targets push answers into the band that JevBench v1.5.4 penalizes; keep the band-edge readout.
- **N6.** The batching rule contradicts itself: at most 3 variants per step, but F5 quadruple units hold 4 rows plus permutation twins.
- **N7.** Strict 50% yes everywhere conflicts with the research advice to vary yes/no base rates by card (20-80%).
- **N8.** G6 needs n ≥ 5,000 per family, but round-1 F8, F12 and F13 have 1.6-2.4K rows. Generate separate QC samples.
- **N9.** Gate the exact artifact that will be served. A bf16 merge can shift outputs.
- **N10.** The 2-bits-per-parameter capacity argument is not the right bound. Keep r16 on empirical grounds only.
- **N11.** For QuALITY, Qasper and DocFinQA, check the document-text licence separately from the annotation licence.
- **N12.** e-CARE has only 2 options. EmoBank per-rater labels are mostly neutral. Both are low value.
- **N13.** SQuAD 2.0's unanswerable items are often ambiguous (Platinum). Give this set a strict G5 read.
- **N14.** Add Codebook behavioural tests (generic labels, swapped labels, exclusion pairs) and a leave-family-out dev split as report-only measures.