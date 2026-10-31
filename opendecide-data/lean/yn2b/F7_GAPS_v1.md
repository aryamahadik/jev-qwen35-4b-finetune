# F7 v1 against the coverage checklist: gaps

**Bottom line.** F7 v1 does not pass the ship audit. It covers **9 of the 38 checklist items**, covers **12 only
partly** and has **0 rows for 17 items**. The audit gives **63 PASS, 47 FAIL and 3 PENDING** sub-checks. Its labels are
sound: an independent logical-form evaluator agrees with the gold on 11,944 of 11,944 rows. The problems are coverage,
mix, balance and a few wording rules. F7 v2 has to be rebuilt to the checklist; tuning v1 will not get there.

- Audit tool: `yn2b/f7_precheck.py` (tests: `yn2b/tests/test_f7_precheck.py`, 71 pass).
- v1 report: `yn2b/f7_precheck.json` (full run, 145 s, CPU only).
- Inputs: `f7_train.jsonl` (sha256 bb709f39…, 2,030 ladders, 10,150 rows) and `f7_probe.jsonl` (b7ba1b07…, 598
  ladders, 1,794 rows).

**How v1 was read.**
- v1 ships no sidecar. `yn2b/f7_v1_adapter.py` derives one from the v1 rows and `f7_defs.json`. It never imports the
  generator.
- The adapter turns each v1 claim template into negation layers, then builds the logical form (LF), the cues, the rung,
  the depth and the checklist tags.
- Checks that the adapter reading is right:
  - The audit's own evaluator matches the gold on 100% of rows.
  - v1's own decide2 also matches on 100% of rows.
- What the adapter cannot derive is counted as missing. Examples: antonym gold for item 21, a curated lexicon file, a
  devx, a blind read.

**Re-run.**
```
cd opendecide-data/lean
PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/f7_v1_adapter.py --out-dir <dir>
PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/f7_precheck.py --meta <dir>/v1_meta.jsonl <dir>/v1_probe_meta.jsonl \
    --decide2-preds <dir>/v1_decide2_preds.jsonl --decide2-code golden_src/gen3/v3_nested_negation.py --decide2-independent no
```

**Words used below.**
- **dev** = the v1 probe. All 598 of its ladders count as holdout, because v1 has no iid dev.
- **Floors** = train / dev / holdout rows: MUST 400 / 40 / 20, SHOULD 150 / 20 / 10, NICE 40 / 10 / 5.
- **covered** = every floor met and the rows have the structure the item asks for.
- **partial** = some rows exist, but a floor is not met or the form is not what the item asks for.
- **missing** = 0 rows.

## 1. Checklist items 1-38

| # | Item | Priority | Train | Dev (= holdout) | Status | Why |
|---|---|---|---|---|---|---|
| 1 | Depth-0 anchor | MUST | 1,809 | 0 | partial | The probe has no R0 rows |
| 2 | Depth 1, clausal not in a statement frame | MUST | 676 | 85 | covered | |
| 3 | Depth 1, truth-value frame | MUST | 267 | 0 | partial | Train is below 400; dev has none at depth 1 |
| 4 | Depth 1, lexical verb only | MUST | 1,310 | 246 | partial | Counts pass, but no card says "the text settles the claim" (check 2.4: 0 of 1,542 rows) |
| 5 | Depth 1, affixal card label | MUST | 967 | 91 | covered | |
| 6 | Depth 2, two cue classes | MUST | 1,600 | 246 | covered | |
| 7 | Depth 2, same class twice | SHOULD | 270 | 256 | covered | |
| 8 | Depth 3, mixed | MUST | 1,040 | 547 | covered | |
| 9 | Depth 4 | NICE | 0 | 80 | partial | Train has no depth-4 rows |
| 10 | Attributed negated claim | MUST | 2,399 | 1,100 | covered | Same-sentence frames only ("refute the claim that ... does not ...") |
| 11 | Negations split between card and question | MUST | 0 | 0 | missing | No card definition carries a scoping negation |
| 12 | Cross-sentence or distant negator | MUST | 0 | 0 | missing | Every scoping cue is in the same clause or sentence |
| 13 | Answer mapping in the instruction | MUST | 0 | 0 | missing | |
| 14 | Inverted yes/no key | SHOULD | 0 | 0 | missing | |
| 15 | Side-clause distractor | MUST | 3,394 | 558 | covered | 468 of the train rows presuppose a fact (see 2.5) |
| 16 | Scoping cue + distractor | MUST | 2,308 | 558 | covered | |
| 17 | Two distractors, no scoping cue | SHOULD | 340 | 0 | partial | Mostly "Leaving no definition unread"; dev has none |
| 18 | Card-line distractor | SHOULD | 1,702 | 558 | covered | Accidental: negations inside source label definitions, not built on purpose |
| 19 | Negation in the state | SHOULD | 3,050 | 933 | partial | Dev yes share: 45.6% with state negation vs 54.8% without (check 4.15) |
| 20 | Look-alikes | SHOULD | 643 | 0 | partial | Only the accidental "falls under"; dev has none |
| 21 | "Not X" vs the antonym, 3+ labels | MUST | 0 | 0 | missing | No antonym label sets and no antonym gold, so C7 cannot run |
| 22 | Residual labels (other / neither / none of) | MUST | 1,040 | 600 | partial | Residual claims ("labels other than X"), never a residual label |
| 23 | Exclusion clause + negated question | SHOULD | 0 | 0 | missing | |
| 24 | "Only" + negation | MUST | 420 | 360 | partial | "Fits only labels other than X" is used; the asked form "X is the only label that fits" is not |
| 25 | Broader term spelled out as a list | NICE | 0 | 0 | missing | |
| 26 | Not all / none / not every | SHOULD | 630 | 170 | partial | Over program records, not multi-text states; no logic line in the card (X10) |
| 27 | "Only" over a negated set + outer negation | MUST | 375 | 374 | partial | Over single texts and records, not multi-text states |
| 28 | Numeric bounds | SHOULD | 0 | 0 | missing | |
| 29 | Approximate negators | NICE | 0 | 0 | missing | |
| 30 | De Morgan / coordination | SHOULD | 0 | 0 | missing | |
| 31 | Exceptors | SHOULD | 1,040 | 600 | partial | Exceptors over labels, not over multi-text items |
| 32 | Not X but Y | SHOULD | 0 | 0 | missing | |
| 33 | Must not / need not / cannot | SHOULD | 0 | 0 | missing | |
| 34 | Unless / only if | SHOULD | 0 | 0 | missing | |
| 35 | Non-factive scope edit | SHOULD | 0 | 0 | missing | |
| 36 | Choice rows, negated selection | MUST | 0 | 0 | missing | v1 has no choice rows |
| 37 | Choice decoys | SHOULD | 0 | 0 | missing | |
| 38 | Inner-negative polar question | SHOULD | 0 | 0 | missing | |

- **Totals:** 9 covered, 12 partial, 17 missing. By counts alone, 15 items meet every floor (check 3.1); 6 of those
  are marked partial above because their form is not what the item asks for.
- **The 18 MUST items:** 7 covered (2, 5, 6, 8, 10, 15, 16), 6 partial (1, 3, 4, 22, 24, 27), 5 missing (11, 12, 13,
  21, 36).
- Check 3.3 flags 3,189 tag mismatches. All of them are items 26, 27 and 31: the rows exist but are not multi-text.

## 2. EXCLUDE constructions X1-X12

Each count is the number of rows with a hit in an instruction, card or option. Every count must be 0.

| X | Construction | v1 rows | Note |
|---|---|---|---|
| X1 | Outer negative question | 0 | |
| X2 | Litotes on a gradable word | 0 | |
| X3 | Metalinguistic negation | 0 | |
| X4 | may not / might not | 0 | |
| X5 | all ... not | 0 | |
| X6 | Neg-raising | 0 | |
| X7 | Factive under negation | 0 | |
| X8 | Negative concord | 0 | |
| X9 | Free focus | 0 | |
| X10 | Reading that depends on implicature | **119** | "not every" with no "quantifiers are read logically" line in the card |
| X11 | Expletive negation and idioms | 0 | |
| X12 | Ill-formed stacks | **80** | Probe "does not lie outside every listed label except X" puts 3 cues in one clause |

- State text is exempt, but its hits are tagged. In v1 states (real source texts): X6 75, X4 49, X7 28, X11 27, X9 25,
  X1 25, X2 10, X3 5, X8 3.
- The regexes are heuristics. Read the hits before acting on them.

## 3. Section 3 targets

| Target | Checklist | v1 | Status |
|---|---|---|---|
| Train ladders / rows | ≥ 1,000 ladders, ≥ 10K rows | 2,030 / 10,150 | pass |
| Items at their floors | all 38 | 15 | fail |
| Depth mix 0/1/2/3/4 | 18 / 25 / 30 / 24 / ≤ 3% (± 2) | 26.2 / 43.0 / 20.6 / 10.2 / 0 | fail |
| Odd parity | about 50% | 53.2% | pass |
| Yes share per (depth × cue count) cell | 48-52% | 20 of 52 train cells off, 5 of 23 dev cells off | fail |
| Yes share per rung | 48-52% | all rungs pass | pass |
| Yes share per other stratum | 45-55% | 513 of 4,358 train strata off (261 templates, 249 quoted labels); 54 of 232 dev strata off | fail |
| truth(P) per rung and per depth | 48-52% | all pass | pass |
| truth(P) per quoted label | 45-55% | 234 labels off | fail |
| Choice rows | 20% ± 3, 3-5 options, positions ± 3, negated selection 50% | 0% | fail |
| Card-less rows | only "Is it true/false that", same share ± 2 | pass | pass |
| Card style per depth and gold | ± 2 points | 16 groups off | fail |
| Rows with a distractor | ≥ 35%; ≥ 25% at each depth 0-3 | 33.4%; depth 2 20.6%, depth 3 20.6% | fail |
| Parity of all cues ≠ parity of scoping cues | ≥ 30% | 35.3% | pass |
| AR + lexical-only flips | ≥ 15% of odd rows | 37.1% | pass |
| Cue mix: syntactic | 25-35% | 56.3% | fail |
| Cue mix: affixal | 20-30% | 12.3% | fail |
| Cue mix: lexical | 20-30% | 22.4% | pass |
| Cue mix: truth-value frame | 10-15% | 9.0% | fail |
| Cue mix: cross-sentence + answer mapping | 5-10% | 0% | fail |
| "not" + "n't" | ≤ 20% of cue tokens | 32.4% | fail |
| Largest single lexeme | ≤ 10% | "not" 32.4% | fail |
| Rows per train lexeme | ≥ 30 | all 22 lexemes ≥ 89 | pass |
| Odd-parity share per lexeme | 40-60% | 9 of 23 off (e.g. "different from" 100%, "non-" 76%, "free of" 75%) | fail |
| Distractor use of distractor-capable lexemes | ≥ 10% | pass | pass |
| Positions: inner claim | 25-35% | 69.8% | fail |
| Positions: outer frame | 20-30% | 30.2% | fail |
| Positions: card definitions | 15-25% | 0% | fail |
| Positions: separate sentence / answer key / choice options | 5-10% each | 0% each | fail |
| Card-format ladders | ≥ 50% | 53.9% | pass |
| Multi-text ladders | 10-20% | 0% | fail |
| Train frame families | ≥ 12 × ≥ 4 frames | 5 families (4 with ≥ 4 frames) | fail |
| Train lexemes | ≥ 60 | 22 | fail |
| Largest frame / carrier | ≤ 4% / ≤ 3% | a6 8.35% / 0.41% | fail / pass |
| Held-out families | ≥ 3 | 3 | pass |
| Held-out lexemes | ≥ 15, ≥ 20%, ≥ 1 per class | 6, 21.4%, only lexical + truth-value | fail |
| Held-out depth-3 class combinations | ≥ 2 | 4 | pass |
| Held-out whole sources | ≥ 2 | 4 | pass |
| Dev ladders | ≥ 150 iid + ≥ 150 holdout | 0 iid + 598 holdout | fail |
| Dev rows | ≥ 1,300 | 1,794 | pass |
| Dev rows per depth | ≥ 200 at depths 0-3, ≥ 40 at depth 4 | 0 / 518 / 598 / 598 / 80 | fail (depth 0) |
| devx (blind-written) | ≥ 100 rows | 0 | fail |
| Distance bins | all 5 | 2 (same clause, same sentence) | fail |
| Clause-embedding depth | 0-3 | 1 and 2 only | fail |
| Depth × position × class cells | ≥ 30 rows each (45 cells) | 15 of 45 | fail |

## 4. Section 4 audit

| # | Check | v1 result |
|---|---|---|
| 1 | Schema | PASS, but only through the adapter: v1 has no sidecar |
| 2 | Gold | LF = gold 11,944/11,944; distractor deletion 8,849/8,849; decide2 11,944/11,944. FAIL: decide2 is not independent (same author); no bivalence line (0/1,542 rows); 468 "Given that ..." distractors presuppose a fact |
| 3 | Coverage | FAIL: 15 of 38 items at their floors; 15 of 45 cells; 22 lexemes; 5 families |
| 4 | Balance | FAIL: see the cell, stratum, label, choice, distractor, mix and position rows above |
| 5 | Surface probes | (a), (b), (d)-(i) pass (train CV 0.46-0.51, dev 0.49-0.51); \|r\| < 0.05 passes; SPEC 8.4 TF-IDF passes (0.508 / 0.494). FAIL: (c) "not" → no scores 0.603 in the 0-depth, 2-cue stratum (179 rows); (j) has no choice rows; 275 of 6,992 yes/no lines drop the question's distractor (all are the d2 / d4 separate-sentence frames) |
| 6 | Composition | C1 train 0.468, C3 0.517 and C4 0.498 pass; C2 passes on dev (0.634). FAIL: C2 train is 0.647 overall but 0.7502 at depth 2 (limit 0.75); C5 is 0.638 train and 0.622 dev (limit 0.60); the C6 counter that ignores cross-sentence cues scores 0.647 train and 0.634 dev (v1 has no such cues, so it equals C2); C1 on dev is 0.378 (the probe is 62% odd parity); C7 cannot run; the cue share is off for 9 train and 7 dev lexemes |
| 7 | EXCLUDE | FAIL: X10 119, X12 80 |
| 8 | Decontamination | 12-gram strict 0; in-family 0 (5,760 card rows inherit golden_dev contact through golden_train, report-only); dev / v11 6-word runs 0; public negation benchmarks 0 (688,360 runs from 9 local sources); failure frame 0; ids / pairs 0; unseen set unchanged (17 / 3,847); dedupe 0; names 0; dev sources 0. FAIL: OHS-3 frame proximity (378 rows); SPEC 7.3 cue share ("belong" 100% odd, 120 probe rows). PENDING: the OHS-3 12-gram count is an owner step |
| 9 | Ladder integrity | States, sizes, relations (9,316, all parity-consistent), both golds, rung semantics and split all pass. FAIL: R0 in 47.5% of train ladders (target ≥ 80%) and 0% of dev ladders (target 100%) |
| 10 | Hold-out integrity | Frames, families, combinations and sources: 0 train rows. 12-gram share 0. iid = train 0. FAIL: the held-out cue word "outside" appears in 782 train rows (the d2, d4 and d6 distractor frames); hold-out lexicon too small; 894 probe states are golden_train states |
| 11 | Blind read | PENDING: no independent blind read yet. A 100 + 10-per-MUST-item sample without gold can be written with `--write-blind-sample` |

## 5. Findings that need the owner's attention

1. **OHS-3 proximity (check 8.6, 378 rows).**
   - v1 frame n6 "Would it be an error to accept that …" shares the 5-word run "would it be an error" with one of
     OHS-3's six negation frames (`build_ohs3.py` NEG_FRAMES T1).
   - Training on it would inflate OHS-3 results on those negation twins.
   - The precheck reads only the frame text in that code file. It never opens OHS-3 data.
   - Item 13 (answer mapping) must also avoid OHS-3's answer-mapping frame (T6). The precheck bans T6's exact shape.
2. **The probe is not text-held-out for C1 (check 10.8).** 894 probe rows reuse golden_train states, and C1 was trained
   on golden_train. The probe's flip rate still measures negation handling, but its states are not new.
3. **decide2 is not independent.** v1's decide2 was written by the generator's author. Checklist 2.1 and SPEC 8.1 need a
   separate agent.
4. **The checklist conflicts with itself on depth 4.** The dev needs ≥ 40 depth-4 rows (CL:374), and item 9 says at most
   3% of rows (CL:61). For a 1,300-row dev that is 39 rows. The precheck applies the 3% cap to train only.
   **Resolved in F7 v2 r6 (2 Oct, fixer review):** both rules hold at once. The probe keeps 72 depth-4 rows of 2,416
   (2.98%, >= 40), and precheck 3.2 applies every item cap to train AND dev (devx reported). No owner ruling was
   needed (`golden_src/gen3/f7_repair_r6.py`, `prereg_drafts/A8prime.md` C.3).

## 6. What F7 v2 must add to its sidecar

The precheck reads these beyond the base contract:
- `antonym_gold` on item-21 rows (C7 needs it).
- `surface` on each cue (the exact word). It is used by the yes/no-line check and the affix-per-word check.
- Optional: `template_id`, used for the per-template balance; without it the precheck uses the masked instruction.
- Optional: `embed_depth` and `quoted_label`.
- `"cue": null` on a NOT node for the AR rung's cue-less flip.
- `"cue"` on a CHOICE node for a negated selection.
- An optional `mode` / `side` on DIST nodes (vacuous / presupposed / conditional), so the deletion test can see a false
  presupposition.

Pass these to the precheck too:
- `--lexicon`: the curated lexicon file (rule 2.8).
- `--holdout-spec`: the declared held-out items.
- `--decide2-preds` and `--decide2-independent yes`, from a separate agent.
- `--blind-read`, from a separate reader.

## 7. Choices the precheck makes where the checklist is open

- **Share bands** use the project's SPEC 4.6 integer rule from `mv_core.share_ok`: \|k − n·mid\| ≤ max(n·halfwidth, 1).
- **Depth-mix tolerance** is ± 2 points.
- **C6** is a cue counter that skips one class. The scope-aware variant is reported as information only.
- **Held out** means: declared in `--holdout-spec`, plus anything that appears in holdout rows and in no train row.
  Held-out word lexemes are also searched in the F7-written train text, with their inflections.
- **Allowed depth × position × class cells**: the precheck uses its own 45-cell matrix (`ALLOWED_CELLS`).
- **Dev states:** the precheck also requires that no dev state is a golden_train state, because golden_train is in the
  fix2 training mix.
- **OHS-3 frames:** the fixed text of OHS-3's frames is banned at 5-word runs, read from the code text.
- **"Cues per clause"** is counted from the sidecar positions, because a linear text splitter cannot see centre-embedded
  clauses.
