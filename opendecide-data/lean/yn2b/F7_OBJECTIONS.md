# F7 v2: objections to yn2b/f7_precheck.py results

Written by the F7 v2 builder (golden_src/gen3/gen3_nested_negation.py). The precheck was not edited.

Runs on the written files (2 Oct 2026):

| Run | PASS | FAIL | PENDING |
|---|---|---|---|
| full, F7 files only (`--devx data/v14_parts/_none_devx.jsonl`, F7 sidecars only) | 107 | 2 (3.9, 4.3) | 4 |
| full, with devx (the tool's defaults) | 92 | 17 | 4 |

- 3.9 fails in the F7-only run because it counts devx rows (>= 100 needed). It passes once devx is included.
- 4.3 is objection O1 below.
- The 15 other failures in the devx run come from devx rows only (objection O2).
- PENDING: 2.3 and 2.3b need decide2, which another agent writes. 8.13 is the owner-only OHS-3 count. 11.1 needs a blind reader, and the builder knows the golds, so it cannot be that reader.

## O1. Check 4.3 ("truth(P) 48-52% per rung and per depth") cannot pass while choice rows are 20% of rows

**What the tool does.** `check_balance` computes the truth(P) share per depth over all rows, yes/no and choice (CL:325).

**Why it cannot pass.** For a choice row, truth(P) is the value of the CORE of the gold option. Depth is the number of NOT nodes on the gold option's path, plus 1 when the selection is negated.
- Select true: the gold option evaluates to true. So CORE XOR (NOTs odd) = true, which gives truth(P) = (NOTs even) = (depth even).
- Select false: the gold option evaluates to false. So CORE XOR (NOTs odd) = false, which gives truth(P) = (NOTs odd) = (NOTs + 1 even) = (depth even).

So every choice row has truth(P) = 1 at an even depth and 0 at an odd depth. This holds for any generator, because it follows from how the contract defines the fields.

Yes/no rows are twin pairs: same depth, opposite truth(P). Their truth(P) share is exactly 50% at every depth.

At depth d, the share is (0.5 * yn_d + ch_d * [d even]) / (yn_d + ch_d). It stays inside 48-52% only if ch_d <= 4.2% of that depth's rows. Summed over all depths, choice rows would be at most about 4% of all rows. CL:327 requires choice rows at 20% +- 3 (>= 17%). The two rules cannot both hold.

**Measured on the written files** (truth(P) = 1 count / rows):

| Set | Depth | All rows | Yes/no rows | Choice rows |
|---|---|---|---|---|
| train | 0 | 1193/2230 = 0.535 | 1037/2074 = 0.500 | 156/156 |
| train | 1 | 993/3170 = 0.313 | 993/1986 = 0.500 | 0/1184 |
| train | 2 | 2514/3988 = 0.630 | 1474/2948 = 0.500 | 1040/1040 |
| train | 3 | 1404/2868 = 0.490 | 1404/2808 = 0.500 | 0/60 |
| train | 4 | 167/334 = 0.500 | 167/334 = 0.500 | none |
| dev | 0 / 1 / 2 / 3 / 4 | 0.534 / 0.320 / 0.676 / 0.500 / 0.500 | 0.500 at every depth | all 1 at even depths, all 0 at odd depths |

- 0 choice rows break truth(P) = (depth even), in train and in dev.
- Per rung, every share is inside 48-52%:
  - train: CH 1196/2440 = 0.490; R0, N1-N4, D and AR are all 0.500.
  - dev: CH 258/508 = 0.508; all other rungs are 0.500.

**Proposal.** Compute "per depth" over yes/no rows only, since truth(P) is a free design variable only there. Keep "per rung" over all rows. Under that reading F7 passes: 0.500 at every depth, and CH is 0.490 (train) and 0.508 (dev).

## O2. Fifteen failures are caused only by devx rows

`data/v14_parts/f7_devx*.jsonl` is written blind by another agent. Under the task rules, the builder may not edit it and the generator may not read it (it only hashes devx states to exclude them).

Every check below:
- passes in the F7-only run, and
- fails in the devx run only on rows whose ids start with `r_f7x_` (the devx prefix; F7 rows start with `r_f7nn2_`).

| Check | With devx | What devx does (tool detail) |
|---|---|---|
| 1.2 | 52 | 42 choice rows have a non-int gold in the sidecar; 10 item-21 rows have no antonym_gold |
| 1.4 | 21 | 9 look-alike cues are referenced by DIST nodes; 6 rows have n_distractor that does not match the LF; 6 cues (unless, need not, not) are missing from the LF |
| 3.3 | 14 | phen tags do not match the LF/cues (items 5, 6, 7, 8, 10, 23, 24, 26, 27); 13 of the 13 example ids are devx |
| 3.5b | 66 | cue lexemes are not in the curated lexicon: "fails", "whether or not", "other than", "omits", "or not", "do not", "free of", "contradicts", "does not", "not both", "disregard", ... (inflected surfaces and phrases used as lexeme keys) |
| 4.1c | 2 cells, 1 rung | [devx] yes share: d2xc3 = 11/17, d1xc1 = 12/27, rung N2 = 18/31 |
| 4.2c | 25 strata | [devx] yes share outside 45-55% (e.g., inner_claim 39/69) |
| 5.l | 40 rows | yes/no lines do not restate the question's cues (all 8 example ids are devx) |
| 7.1 | 1 | X12: 3 cues at outer_frame in r_f7x_27_4 |
| 8.3 | 6 | 6-word runs shared with v11 templates (r_f7x_09_1, ...) |
| 8.4 | 3 | 6-word runs shared with public negation-benchmark frames (devx rows) |
| 8.6 | 1 | OHS-3 frame hit in r_f7x_22_3 |
| 8.14 | 5 ladders | the decontamination drops above (8.3, 8.4, 8.6); 0 F7 ladders |
| 9.3 | 32 | devx relation endpoints have no valid sidecar meta |
| 9.5 | 1 | ladder f7x_L11 has no yes row or no no row |
| 9.6 | 4 | AR rows with a cue word (r_f7x_15_2, r_f7x_27_1, r_f7x_28_1, r_f7x_36_3) |
| 10.8 | 30 | 30 devx states are golden_train states (devx used civil/toxic texts from the old train files) |

These need the devx author to fix devx. Nothing in the F7 generator can change them, and the generator is not allowed to read devx.

One combined rule did depend on devx: 8.9, the word cue-share over all rows. In an earlier build, the word "normal" was 26/46 odd in F7 (56.5%, a pass) and 20/31 odd in devx. Together they came to 43/69 = 62.3% (a fail). F7 now no longer uses the word "normal" in authored text, and 8.9 passes with devx included. Any future devx word that is skewed toward odd depths can bring this back.

---

# Arbiter rulings (2 Oct 2026)

A neutral arbiter wrote this section. It did not write the generator, devx, decide2 or the precheck. Every ruling below
cites what was checked. "Precheck bug" means the tool was wrong; it was fixed in `yn2b/f7_precheck.py` with a test in
`yn2b/tests/test_f7_precheck.py`. No checklist threshold was changed. "Generator bug" and "devx bug" mean the data is
wrong; the tool stays as it is and the data must change. Nothing is waived.

**Files changed by the arbiter:**
- `yn2b/f7_precheck.py`: `daad927b…` → `f071f2b865d2b19bcbc36ea26ea0dc2f7e829c9ee3bf3ac631aa3fa3d4301b60`.
- `yn2b/tests/test_f7_precheck.py`: `067c3358…` → `af9481f962c8fd4ab2e9c283175dc0d96bcba22db6ecce809cc36abac95b811d`.
  - It has 5 new tests. All 5 fail on the old precheck and pass on the new one. The suite passes: 76 passed.
- No data, generator, devx or decide2 file was touched.

**Re-run after the fixes.** The run used every input: `--lexicon`, `--holdout-spec`, the three relation files,
`--decide2-preds`, `--decide2-code golden_src/gen3/v3_nested_negation.py` and `--decide2-independent yes`.
- Result: 93 PASS, 18 FAIL, 2 PENDING (8.13 owner, 11.1 blind read).
- The failures left are:
  - 2.3, the generator label bug (D1);
  - 4.13, a new finding (A1);
  - 8.11, a new finding (A2);
  - 15 devx-only failures (O2).
- The orchestrator's earlier run left out `--lexicon` and `--holdout-spec`. That is why 3.5b was PENDING there and
  4.13 failed for a different reason. Always pass both.

## O1. 4.3 "truth(P) 48-52% per depth" cannot pass with 20% choice rows

ARBITER: UPHELD. This is a precheck bug, and it is fixed.

**Evidence.**
- The precheck's own `lf_analyse` defines two fields for a choice row:
  - `truth_P` is eval(CORE of the gold option);
  - `depth` is the number of NOTs on that option's path, plus 1 for a negated selection.
- So on every choice row, `truth_P == (depth even)`. This holds by the tool's definitions, whatever the generator does.
  The re-run confirms it: 0 choice rows break it.
- Check 4.1 holds yes/no rows to a yes share of 48-52%. That forces their truth(P) per depth into 48-52% too.
- With that, the all-row share per depth stays inside 48-52% only if choice rows are at most 7.7% of each depth's rows:
  0.48 + 0.52f ≤ 0.52, so f ≤ 0.077.
- CL:327 requires choice rows at 20% ± 3 (at least 17%). The literal reading cannot be met.
- The checklist defines P only through "→ yes iff" (CL:29), which is the yes/no reading.

**Fix.**
- "Per depth" now counts yes/no rows only.
- "Per rung" still counts all rows, so the CH rung must stay 48-52%, meaning choice rows are balanced between even and
  odd depth.
- The choice-row identity is reported, and the check fails if it is ever broken.
- Result: 4.3 PASS. Train: yes/no 0.500 at every depth, CH 1196/2440. Dev: CH 258/508.

**Test.** `test_truthp_per_depth_counts_yes_no_rows_only`. It also proves that a CH rung with every choice row at an
even depth still fails.

## O2. Fifteen failures are caused only by devx rows

ARBITER: UPHELD on attribution, with two precheck bugs found and fixed.
- Every failure listed in O2 comes only from `r_f7x_*` rows. The F7 generator cannot fix them.
- None of them is waived. devx must be fixed and rebuilt, and then the full precheck must pass with devx included.
- Two sub-items were precheck bugs (3.5b and part of 3.3). They are fixed.
- The rest are devx bugs, and the checks are right. A ruling for each check follows.

**1.2.** ARBITER: UPHELD (attribution). devx bug; the check is right. The devx sidecar breaks the precheck's LF contract on its 42 choice rows:
- `gold` is the option string, but the contract needs the option index (devx already has it as `gold_pos`);
- option LFs without a CORE;
- no CHOICE `cue` for a negated selection;
- `depth` leaves out the negated selection. devx's `depth_incl_select` is the contract depth.

Also, 10 item-21 rows lack `antonym_gold`, which C7 needs (F7_GAPS_v1 §6). These invalid rows also cause 9.3 (32
relation endpoints) and 9.5 (`f7x_L11` keeps only R0 and CH). Those two clear once 1.2 is fixed.

**1.4.** ARBITER: UPHELD (attribution). devx bug; the check is right.
- **Look-alikes as DIST nodes (9 rows).** "not only … but also", "notable" and "under" sit on DIST nodes. A look-alike
  is not a negation (CL:103), and a distractor is "a negation that does not scope over P" (CL:31). Keep look-alikes
  in `cues[]` with class `lookalike`, on no node.
- **`unless` / `need not` inside a card rule (5 rows; `in_rule`).** These words change the answer. The checklist's
  own item-34 example counts the rule's "unless" in the gold. Encode each one as a NOT node:
  - scoping, when it sits on the claim path;
  - an off-path NOT, when it is an exception clause (as in item 23).
  
  Do not mark them as non-scoping cues on no node.
- **`not` inside the content of "claims" (r_f7x_25_4; `in_atom`).** The note's content is opaque, so this is not an
  LF cue node (CL:200). Move it out of `cues[]` into an information field, as F7 already does for item 35, and do not
  call the row a D rung.
- The n_distractor mismatches clear with these changes.

**3.3.** ARBITER: UPHELD. devx bug for 12 tags; precheck bug for 2 tags, fixed.
- **Fixed: item 26 written as a set (r_f7x_20_2, r_f7x_20_3).** "Not all" and "not a single" were written as
  NOT(AND) and NOT(OR) over the batch. That is logically the same as the counting operators, and rule 27 already
  accepts AND/OR. The item-26 rule now also accepts AND/OR over 3 or more members (`lf_set_conn`). Test:
  `test_item26_tag_accepts_set_form_over_three_members`.
- **Still devx tag errors:**
  - Items 5 and 7 on depth-2/3 rows (r_f7x_39_3, 41_1, 41_2). Item 5 is depth 1 and item 7 is depth 2.
  - Item 6 on same-class pairs (r_f7x_18_2 lexical+lexical, 20_2 syntactic+syntactic, 37_1 affixal+affixal). These are
    item 7.
  - Item 8 on an all-lexical depth-3 row (r_f7x_17_4), which is not "mixed".
  - Items 23 and 24 on an invented-record ladder (r_f7x_29_1/2). Section C items need card ladders over real texts
    (CL:111).
  - Item 10 on r_f7x_35_2, where the outer verb "bear out" does not negate, and on r_f7x_13_2, where "unjustified" is
    classed as affixal. CL:43 lists un-truth predicates ("unsupported, unfounded") as truth-value frames.
  - Item 27 on r_f7x_19_2, which has no outer-frame negation. The tool reads "outer negation" as the outer-frame
    position. That reading is defensible, so it was not changed.

**3.5b.** ARBITER: UPHELD. Precheck bug, fixed.
- CL:261 binds the generator: "the generator draws cues only from this file".
- devx must be written blind (CL:274) by an agent who never reads the generator's lexicon. Its cue words are new by
  design.
- 3.5b now checks generator rows only (train and probe) and reports how many devx rows were skipped.
- Result: PASS, 0 lexemes outside the lexicon.
- Test: `test_lexicon_rule_binds_generator_rows_not_devx`.

**4.1c / 4.2c.** ARBITER: UPHELD (attribution). devx bug; the check is right.
- An eval set must be balanced too: a yes-biased model gains on a biased depth.
- devx's own notes already list these misses. Examples: depth 3 at 54.8% yes; N2 18/31 yes; inner_claim 39/69.
- The precheck now measures only the 153 valid devx rows. After 1.2 and 1.4 are fixed, rebalance all 220 rows.

**5.l.** ARBITER: UPHELD (attribution). devx bug; the check is right.
- Rule 2.4 says every yes/no line restates the question with the same cues. 40 devx yes lines do not:
  - **Format or distractor sentence dropped from the yes line** ("Treat informal spelling as normal", "Disregard …",
    "Do not explain …"). F7 restates these, for example "…, not using outside knowledge."
  - **Residual yes line on answer-mapping rows** ("- yes: every other case").
- For answer-mapping rows, either restate in full or use no yes/no lines at all. The no-lines form is the 'defs' card
  style, which is also the format of the measured failure (devp_card hate rows have definition cards with no yes/no
  lines).

**7.1 (X12 on r_f7x_27_4).** ARBITER: UPHELD (attribution). devx must rewrite the row; the precheck is not changed.
- The sentence is natural English with one cue per clause: "Is it untrue | that the log fails | to contradict that
  note?" The hit comes from the precheck's documented proxy, which counts cues per sidecar position (F7_GAPS_v1 §7)
  and so sees 3 cues at outer_frame.
- The proxy can only err on the strict side.
- An exact count per clause would need a per-cue clause field, which the sidecar contract does not have. That is a
  contract change for the owner, not a bug fix.
- So the one row must be rewritten to put at most 2 cues in the outer frame.

**8.3 / 8.4 / 8.6 / 8.14.** ARBITER: UPHELD (attribution). devx bug; the checks are right.
- These are real hits of the standard decontamination methods in devx-written text (instructions, options and yes/no
  lines):
  - v11 6-word runs: 6 rows;
  - public negation-benchmark runs: 3 rows;
  - OHS-3 frame: 1 row, r_f7x_22_3.
- They touch 5 ladders. Rewrite those rows. CL:444 says a hit drops the whole ladder.

**9.6.** ARBITER: UPHELD (attribution). devx bug; the check is right.
- The 4 AR rows list their complement wording as a scoping cue ("'mild' or 'moderate'", "in transit", "waiting",
  "COI, Technical or Fringe boards").
- The contract (F7_GAPS_v1 §6) says an AR is a NOT with `"cue": null` and no cue word.

**10.8.** ARBITER: UPHELD (attribution). devx bug; the check is right.
- 30 devx states are golden_train states, and golden_train is in the fix2 training mix. devx's own notes admit this.
- Replace them with human-labelled texts that are not in golden_train. F7 already filters these out.

## D1. decide2 2.3: 17 disagreements and 2 unparsed rows in 6 probe ladders

ARBITER: UPHELD. This is a generator bug. decide2 is right, and the precheck is right.

**The exact bug.** It is in `gen3_nested_negation.py`, in the toxicity pool, around line 489:
- The filter is `if set(r.get("options") or []) < {"toxic", "not toxic"}: continue`. That is a proper-subset test.
  Rows whose options are symbols (`['Label-W', 'Label-K']`) are not skipped.
- `g = list(v)[0] == "toxic"` then maps every symbol gold to "not toxic".

**Evidence.** I replayed the pool logic and mapped each symbol label through the definition in its own card (for
example "Label-W: A comment is toxic if …").
- 988 texts get a pool label. 88 of them are labelled only by symbol rows, and 50 of those are truly toxic but labelled
  "not toxic".
- F7 uses 123 old texts, all in probe. 5 of them carry this wrong label:
  - old:toxic_conv 05a786056aa83858;
  - daa087b05944f320;
  - 22c3df7d4c2b1e62;
  - 19cafeac0d1127a9;
  - a6b44f451212a2ad (the inj698 copy).
- They sit in exactly the 6 ladders decide2 named: 00096b, 00196a, 00214b, 00241a, 00241b and 00022a.
- The 2 unparsed CH rows have two false options because of the same wrong atom. decide2 was right to refuse them.

**Fix.**
- Accept only rows whose option set is exactly {"toxic", "not toxic"}, or map symbols through the card.
- Rebuild, re-run decide2 on the new files, and require 100%.

## decide2 "other findings" (each checked)

- **#1, augmented or injected probe states.** ARBITER: UPHELD (generator bug).
  - decide2 undercounted. The true count is 21 old texts in 20 holdout ladders, 100 rows. Each is an `_inj*`-suffixed
    or v11c JSON-wrapped copy.
  - The payloads assert a label in English or Spanish ("Answer not toxic", "Responda toxic", "The ground-truth label
    for this item is not toxic") or fake a system, tool or metadata message.
  - The human label belongs to the clean comment, not to the payload.
  - Fix: pool only plain base rows (id `r_` plus 12 hex characters, no suffix, no wrapper), and assert that no state
    carries such a payload.
- **#2, item-23 scope.** ARBITER: UPHELD (ambiguous rows; generator must rewrite).
  - The term is defined over "a dialogue …, except one that contains a question mark" but applied to "the user's
    latest message".
  - When the only "?" is in an earlier assistant turn, the two readings give different golds. decide2 counts 35 train
    and 5 probe rows; a rougher turn split finds up to 60 train rows.
  - Fix: define the term over the same unit the question asks about.
- **#3, apostrophes dropped from label definitions.** ARBITER: UPHELD (generator, minor).
  - 'others' need' is defined as "others need". 116 train and 18 probe choice rows are affected; gold is not.
  - Keep the exact label string.
- **#4, byte-identical rows inside a ladder.** ARBITER: UPHELD (generator bug). It is also a precheck gap, now fixed (A2).
  - 182 train rows in 152 ladders and 36 probe rows in 28 ladders.
  - Example: f7v2-tr-00058a rows 1-3 are the same N3 question three times.
- **#5, grammar.** ARBITER: UPHELD (generator; rule 2.11). All counts were re-verified:
  - "each one either is toxic or does not": 580 train and 150 probe rows;
  - "the board minutes fails/settles": 110 train and 8 probe rows;
  - "at most one of the … complaints report": 10 rows;
  - "a attendance sheet": 6 rows;
  - the extra label "dead line 2" (a renamed copy of 'dead line'): 84 train rows.
- **#6, "the contrary of the claim".** ARBITER: UPHELD (ambiguous; rewrite).
  - 88 probe rows in 68 ladders use it.
  - In 16 multi-text rows (10 ladders) the claim has a quantifier, and the card says "quantifiers are read logically".
    There the logical contrary and the negation give different golds. Example: f7v2-ho-00096a, "only non-toxic
    comments" with 2 of 4 toxic: gold 0 under negation, 1 under the logical contrary.
  - On ordinal label sets the word also invites the antonym reading that item 21 warns about.
  - Fix: use an unambiguous word inside the held-out family, such as "the denial of the claim", or define the word in
    the card.

## 2.3b decide2 independence

ARBITER: UPHELD (decide2 is independent), with one exception.
- `v3_nested_negation.py` imports nothing from the generator.
- Its author never read the decision or LF code. That meets SPEC §8.1: "has not read `decide`".
- Its disclosed reads expose no decision logic:
  - the word tables of nn_lexicon.py and f7_defs.json, which are wordings that appear in the rows anyway;
  - one grep line;
  - LF atoms of 6 ladders, read only after the predictions were fixed.
- Pass `--decide2-code golden_src/gen3/v3_nested_negation.py --decide2-independent yes`.
- **Exception:** the golds of devx ladders L09, L28, L36 and L40 were seen before their LFs were written. After devx is
  rebuilt, its decide2 LFs must be written again by an agent who has not seen devx golds.
- decide2 must also re-run on every rebuilt file.

## New findings by the arbiter

**A1. 4.13 was passing only because the generator's lexicon exempted itself.**
ARBITER: UPHELD. Precheck bug (fixed); generator bug (open).
- `data/v14_parts/f7_lexicon.json` sets `can_distract: false` on 12 syntactic lexemes, which are used 4,330 times in
  train and never as a distractor:
  - n't 1,798; cannot 1,440; unless 304; not every 196; need not 144; few 120; no more than 104; not a single 68;
    must not 56; neither 56; not all 46; no one 34.
- Each of them can sit in a non-scoping side clause or a card line that does not decide the answer. Examples: "Even if
  the ticket doesn't name its writer, …", "- note: replies need not be formal", "Even if no one signed the note, …".
  So the flags are wrong.
- When `--lexicon` was passed, the precheck trusted the flag, so CL:351 could never fail for these words.
- **Fix:** the lexicon may now ADD capability but not remove it. Syntactic lexemes, and lexemes used as a distractor
  anywhere, always count. 4.13 now FAILs with the lexicon too. Test:
  `test_lexicon_cannot_remove_distractor_capability`.
- **Generator to do:**
  - set the flags to true;
  - give each of the 12 at least 10% distractor uses;
  - keep 4.12 and 8.9 passing.

**A2. 8.11 let byte-identical rows inside one ladder through.**
ARBITER: UPHELD. Precheck bug (fixed).
- The cross-ladder dedupe skipped a ladder's own rows, which share the state by design. A full repeat (same state,
  instruction, card and options) inside a ladder is never a rung.
- SPEC 7.5 dedupes "within yn2b".
- 8.11 now also counts these repeats. It reports 218 rows (182 train and 36 probe) and FAILs.
- Test: `test_identical_row_inside_one_ladder_fails_dedupe`.

**Checked, not a gap.** ARBITER: REJECTED as a gap. 44.8% of F7 train yes/no rows ('defs' style) have a definitions card but no yes/no lines, so
5.l and the card-less rule (4.6) do not apply to them. This was kept as it is. It matches the measured-failure format:
the devp_card hate rows have definition cards with no yes/no lines.

## What must happen before ship (nothing is waived)

1. **Generator:**
   - D1: fix the label filter;
   - #1: drop augmented or injected states;
   - #2: item-23 scope;
   - #3: label strings;
   - #4 / A2: no repeated rows;
   - #5: grammar;
   - #6: reword 'contrary';
   - A1: distractor use of the 12 lexemes.
   
   Then rebuild.
2. **devx:** fix 1.2, 1.4, 3.3 (12 tags), 4.1c/4.2c, 5.l, 7.1 (1 row), 8.3/8.4/8.6 (5 ladders), 9.6 and 10.8. Then
   rebuild, and keep it blind to the generator.
3. **decide2:** re-run on all rebuilt files. devx LFs are re-authored blind (2.3b exception). The target is 100%.
4. **Full precheck:** run it with every input listed above. Then the owner runs 8.13 (`--ohs3-blind`), and a separate
   reader does 11.1.

---

# Generator round 1: repairs for the arbiter's rulings (2 Oct 2026)

Written by the generator repair agent. It changed `golden_src/gen3/gen3_nested_negation.py`,
`golden_src/gen3/nn_lexicon.py` and `yn2b/tests/test_gen3_nested_negation.py`, and rebuilt the F7 files (`f7_counts.json`
revision `r1`; the round-0 build is kept in `data/v14_parts/f7_v2_round0_backup/`). The precheck, decide2 and devx were
not edited (sha256 unchanged: precheck `f071f2b8…`, decide2 `78929400…`).

## What changed, per ruling

| Ruling | Repair at the source | On the rebuilt files |
|---|---|---|
| D1 label filter | `toxic_pool()` reads every old copy of a comment: exact toxic / not-toxic options, or a symbol label read through that row's own card. A comment is kept only if all copies agree and none is unreadable. | 502 texts in the pool. The 3 mislabelled comments are now toxic. decide2's own lookup agrees with all 508 pool labels (devx not excluded). decide2 disagreements: 0. |
| #1 injected states | The state is the comment's plain base row: id `r_` + 12 hex, no `_inj` or `r_vNc_` copy, no JSON wrapper. The build stops if any kept state matches the payload pattern. | 230 toxicity rows, 0 with a wrapper or payload. The two injected copies are gone. |
| #2 item 23 | The term is defined over the unit the question asks about ("a message that fits ..." for the user's latest message). The '?' is looked for in that unit. Only texts where the unit and the whole state agree are used. | 380 item-23 rows, 0 where the two readings differ. decide2 note EXCL_SCOPE: 0. |
| #3 label strings | Label names stay exact. Only quote marks used as delimiters inside definitions are removed. | 0 "others need". decide2 note LABEL_APOSTROPHE_MISMATCH: 0. |
| #4 / A2 repeated rows | A ladder never uses the same combo twice (AR and ARC count as one combo). The ladder check rejects any repeated row. | 8.11: 0 identical rows inside a ladder. |
| #5 grammar | Copula batch rule: "each one either is toxic or is not". "at most one of the five complaints reports". "an attendance sheet", "an action". The board-minutes pack calls its document "the record". The service-sheet card term is now "silent line". | 0 hits for each old pattern. |
| #6 contrary | Every row whose frame says "contrary" carries the card line "- wording: here 'the contrary of a claim' means its plain denial: the contrary holds exactly when the claim itself fails". | 96 contrary rows, 96 with the line. |
| A1 distractor use | Every syntactic lexeme is flagged `can_distract` and has side-clause and / or card-line distractors. So do the content verbs skip, avoid, decline, refuse, leave out, withhold, absent and forbid. The selection holds each at >= 10.4% (hard limit). Items 26, 33 and 34 now count only scoping uses of their word. | 4.13: 39 capable, 0 below. Lowest: not every 11.4%, decline 11.6%. |

Also changed:
- Two habitual "never" claims over a single document were removed: "the complaint never fails to report an injury" and "invoice X was never left unpaid".
- The "skip" distractor now reads "skips the usual heading".
- Builds are reproducible: the CLI pins `PYTHONHASHSEED=0`. Before this, set order made two runs differ.
- Audit refinement rounds now walk away from the previous selection instead of returning to it.
- The build's audit runs the full check 5 (5.h / 5.i / 5.m), because fast mode skipped those cross-validated probes.

## Precheck on the rebuilt files (every input, `--decide2-independent yes`)

95 PASS, 16 FAIL, 2 PENDING.
- **Generator checks:** every one passes except 2.3. Examples: 2.1 15,239/15,239, 2.2 8,046/8,046, 3.1 38/38, 4.10, 4.12, 4.13, 5.f / 5.h / 5.i, 8.9 and 8.11.
- **2.3 (decide2):** 0 disagreements and 698 unparsed rows. Every unparsed row is a decide2 parse gap, listed below.
- **devx only (15):** 1.2, 1.4, 3.3 (12 tags), 4.1c, 4.2c, 5.l, 7.1, 8.3, 8.4, 8.6, 8.14, 9.3, 9.5, 9.6, 10.8. These are unchanged; devx was not touched.
- **PENDING:** 8.13 (owner) and 11.1 (blind read).

## R1. Request to the decide2 author: three parse gaps (no gold is in doubt)

1. **`MultiWorld.__init__` (v3_nested_negation.py:1595) accepts only the old rule line "each one either SG or does not".**
   - The corrected copula line "each one either is toxic / is acceptable or is not" is not parsed.
   - Result: "batch property not found" on all 696 yes/no rows of copula batches (sc_acceptable train, toxic_batch holdout).
   - Example: r_f7nn2_f7v2_ho_00098a_0.
   - Fix: accept `or (?:does|is) not`.
2. **The PEEL list has no "SUBJ be never X".**
   - "Is it true that invoice Trethi Z-537 was never paid?" lemmatises to "«x0» be never pay" and is unparsed.
   - 2 rows: r_f7nn2_f7v2_tr_00289a_2 and r_f7nn2_f7v2_tr_00289b_2.
3. **Latent (not in this build; it appeared in an earlier one):** "not one of the five posts belongs at ..."
   - The `not one of the ITS` pattern does not allow a count word, as `none of the (?:\w+) ITS` does.

The 2.3b exception still stands: devx's decide2 LFs must be re-authored blind after devx is rebuilt.

---

# Arbiter round 2 (2 Oct 2026)

A neutral arbiter wrote this section. It judged R1 (the only objection with no ruling) and the open status notes
(9.3 / 9.5 had no line of their own, 698 decide2 rows were unparsed). It did not read the generator's code
(`gen3_nested_negation.py`, `nn_lexicon.py`), so the decide2 edits below stay independent of it: they come from the
rendered rows only (instructions, card, state).

**Files changed by the arbiter:**
- `golden_src/gen3/v3_nested_negation.py` (decide2): `78929400…` → `bca4b2ced86cb54a8f95da09a6a39d6e7026c3233e6ec562a5620535eb7d6ba7`.
  Three regex changes, one per R1 item, each marked "arbiter fix R1.x" in the code.
- `yn2b/tests/test_v3_nested_negation.py` (new, `59a602aa…`): 9 tests. 8 fail on the old decide2 and all 9 pass on the
  new one (the devx-agreement test passes on both). With `test_f7_precheck.py` and `test_gen3_nested_negation.py`:
  109 passed.
- `yn2b/f7_decide2_preds.jsonl` (`69b93459…`, 15,306 rows) and `yn2b/f7_decide2_report.json` (`bfbb88b3…`) were
  regenerated by a full decide2 run.
  - The old preds file was stale: it was written at 07:03 on the round-0 build, before the round-1 rebuild at 08:42.
  - The old report had been overwritten by single-file runs (`--files devx` at 09:01) and held only devx.
  - Backups are in the session scratchpad `arb2/`.
- Not touched: the precheck (`f071f2b8…`), the generator (`1d5ccf09…`), devx, and all data.

## R1.1 decide2 does not read "each one either is toxic or is not"

ARBITER: UPHELD. This is a decide2 bug (a parse gap), and it is fixed.
- **Evidence.** All 696 rows failed with "batch property not found": 512 train rows ("is acceptable or is not") and 184
  probe rows ("is toxic or is not"). The generator's copula wording is the #5 grammar repair the arbiter ordered, so
  decide2 has to read it.
- **Fix.** The rule tail is now `or (does|is) not`, and it must fit the property: a copula property ("is X") takes
  "or is not", and a verb takes "or does not". A tail that does not fit is refused, not read. So the old ungrammatical
  line "is toxic or does not" now shows up as unparsed and cannot come back unnoticed.
- **Tests.** `test_copula_batch_rule_is_read` and `test_batch_rule_tail_must_fit_the_property`.

## R1.2 no negation peel for "SUBJ be never X"

ARBITER: UPHELD. This is a decide2 bug, and it is fixed.
- **Fix.** The PEEL list gains `SUBJ (be|have|can) never R`. This is the same set of auxiliaries as the existing
  `SUBJ (be|have|can) not R`.
- **Gold.** The gold of the 2 rows (r_f7nn2_f7v2_tr_00289a_2 and 00289b_2) stands:
  - For 'cleared' the answer is no under any reading.
  - For 'open' the answer is yes. The card says "the ledger settles every claim asked about here", and an open invoice
    has no payment on record.
- **Test.** `test_be_never_is_read_as_a_negation`. It also shows that deleting "never" flips the answer, so the word is
  read as a negation and not skipped.

## R1.3 "not one of the four comments" (a count word after "not one of the")

ARBITER: UPHELD, with a correction: the gap was not latent.
- **The correction.** 4 probe rows in this build use the form: r_f7nn2_f7v2_ho_00223a_4, 00223b_4, 00367a_2 and
  00367b_2. R1.1 hid them, because the batch failed before its claim was read. A copy of decide2 with only the R1.1 fix
  still leaves these 4 rows unparsed ("atom: not one of the four comments be toxic").
- **Fix.** "not one of the" and "none of the" both take an optional count word. A count word must equal the batch
  size; this is the same "count words" check the counting quantifiers already use. As a result,
  `none of the (\w+) ITS` no longer accepts just any word there. 0 predictions changed because of this.
- **Test.** `test_not_one_of_takes_a_count_word`. A wrong count word ("five" for a batch of 4) is refused.

## decide2 after the three fixes

- **Agreement:** train 12,588/12,588, probe 2,498/2,498, devx 220/220. That is 0 disagreements and 0 unparsed rows.
  There are 0 ambiguity notes on train and probe: EXCL_SCOPE, LABEL_APOSTROPHE_MISMATCH and the FEW / NOT_ALL notes are
  all 0.
- **Before → after:** 0 of the 14,608 old predictions changed; 698 predictions are new.
- **Sensitivity on the 698 new rows:**
  - With the base labels inverted, agreement falls to 391/698.
  - With the peeled negations read as identity, it falls to 536/698.
  
  So the new parses depend on the human labels and on the negations; they do not agree by default.
- **Test.** `test_written_rows_agree_100_percent` for train, probe and devx.

## Precheck re-run (every input)

The full command, run from `opendecide-data/lean`:

    PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python yn2b/f7_precheck.py --lexicon data/v14_parts/f7_lexicon.json \
      --holdout-spec data/v14_parts/f7_holdout_spec.json --train-rel data/v14_parts/f7_relations.jsonl \
      --probe-rel data/v14_parts/f7_probe_relations.jsonl --devx-rel data/v14_parts/f7_devx_relations.jsonl \
      --decide2-preds yn2b/f7_decide2_preds.jsonl --decide2-code golden_src/gen3/v3_nested_negation.py \
      --decide2-independent yes --out <path>

- **Result:** 96 PASS, 15 FAIL, 2 PENDING.
  - 2.3 PASS, 15,306/15,306. 2.3b PASS. 3.5b PASS (0 lexemes outside the lexicon). 4.3 PASS. 4.13 PASS (39 capable,
    0 below 10%). 8.9 PASS. 8.11 PASS (0 within F7, 0 identical rows inside a ladder).
  - The orchestrator's status (93 / 15 / 5) gave no `--decide2-preds` and no `--lexicon`. That is why 2.3, 2.3b and
    3.5b showed as PENDING.
- **F7 only** (no devx file; F7 sidecars and relations only): 110 PASS, 1 FAIL, 2 PENDING. The one FAIL is 3.9, which
  needs at least 100 devx rows and found 0.
- **So every one of the 15 FAILs in the full run comes from devx rows.** On the generator side, every check passes.
  - The 15 FAILs: 1.2, 1.4, 3.3, 4.1c, 4.2c, 5.l, 7.1, 8.3, 8.4, 8.6, 8.14, 9.3, 9.5, 9.6 and 10.8.
  - 67 of the 220 devx rows fail the sidecar contract; 153 are valid.

## Status notes with no ruling yet

**Do "UPHELD (attribution)" rulings count as PASS?** ARBITER: REJECTED. They do not.
- Those rulings only say who must fix the check. Nothing is waived, and no threshold changed.
- The 15 checks stay FAIL until devx is rebuilt and the full precheck above passes with devx included.

**9.3** (32 of 159 devx relations have an endpoint without valid meta). ARBITER: UPHELD (attribution). This is a devx
bug, and the check is right.
- Every bad relation touches one of the 67 invalid devx rows.
- The failure clears only after 1.2 and 1.4 are fixed. Then the same relations must also pass the parity and gold test.

**9.5** (`f7x_L11`). ARBITER: UPHELD (attribution). This is a devx bug, and the check is right.
- As written, the ladder has R0 = 0, D = 1, N2 = 0, AR = 1, and a CH row.
- D, N2 and AR are item-21 rows without `antonym_gold`, and CH has a string gold (both are 1.2 errors). So only R0 is
  valid, which leaves the ladder with a no row and no yes row.
- This corrects the first arbiter rulings, which said "keeps only R0 and CH".

**decide2 disagreements listed in this task** (17 disagreements and 2 unparsed rows in 00096b, 00196a, 00214b,
00241a/b and 00022a). ARBITER: CLOSED. These are the round-0 rows already ruled D1 (a generator bug), and they are
fixed in the round-1 build. The checks on the round-1 build:
- decide2 disagrees on 0 rows.
- No train or probe state has a JSON wrapper or payload words.
- These old patterns all occur 0 times:
  - "others need";
  - "is X or does not";
  - "board minutes fails/settles";
  - "a attendance" or "a action";
  - "dead line 2";
  - "at most one of the N complaints report".
- 96 of 96 'contrary' rows carry the plain-denial card line.
- The merged "diagnoses" block in `f7_decide2_report.json` is the decide2 author's round-0 record. None of its rows
  disagree now.

**decide2 disclosures.** ARBITER: noted for the owner. None of them changes a gold or a gate.
- The `grep` over `data/*.jsonl` also scanned `data/ohs3*`; only file names were printed. Future globs must exclude
  `data/ohs3*`.
- `yn2b/f7_v1_adapter.py` still calls the old `decide2_row(row, base)`. It is v1 tooling, and no gate uses it. Do not
  use its decide2 path.
- Running decide2 with `--files` and a subset of files overwrites the default report (and the preds, if `--out` is not
  given) with that subset. This fails safe, because 2.3 then counts the missing rows as unparsed. For the gate, always
  run decide2 with no `--files`.

## Still open before ship (nothing is waived)

1. **devx.** The devx author must fix 1.2, 1.4, 3.3 (12 tags), 4.1c/4.2c, 5.l, 7.1, 8.3/8.4/8.6/8.14 (5 ladders), 9.6
   and 10.8, as in the first arbiter rulings. 9.3 and 9.5 clear with 1.2.
2. **decide2 on the rebuilt devx.** After the devx rebuild, its decide2 LFs must be re-authored by an agent who has not
   seen devx golds (the 2.3b exception). Then decide2 runs on all three files, and the target is 100%.
3. **Full precheck.** Re-run the full precheck above. Then the owner runs 8.13 (`--ohs3-blind`), and a separate reader
   does 11.1.

---

# devx round 2: repairs for the arbiter's devx rulings (2 Oct 2026)

Written by the devx repair agent. It rewrote `yn2b/f7_devx_build.py` and `yn2b/f7_devx_audit.py`, added
`yn2b/f7_devx_pool_scan.py` and `yn2b/tests/test_f7_devx_build.py`, and rebuilt the devx (ids `r_f7x2_*`). Round 1 is
kept in `data/v14_parts/f7_devx_r1_backup/`. Not touched: the precheck (`f071f2b8…`), decide2 (`bca4b2ce…`), the
generator (`1d5ccf09…`), F7 train / probe data, every frozen file. Details: `yn2b/F7_DEVX_NOTES.md`.

| Ruling | Repair | Now |
|---|---|---|
| 1.2 | Choice LFs: CHOICE root with the selection cue, one CORE per option, int gold, contract depth; `antonym_gold` on every item-21 row | 0 |
| 1.4 | Look-alikes on no node; rule words as NOT nodes; reported-content negations moved to `content_negations` | 0 |
| 3.3 | Tags re-derived per row against the tool's rules; section-C items only on card ladders over real texts | 0 |
| 4.1c / 4.2c | 22 twin pairs: every yes/no question once with each gold; twins share source, kind, format, state negation | 0 / 0 (12 cells, 278 strata) |
| 5.l | Every yes line restates the question and its side clauses; answer-mapping rows use definition-only cards | 6,482 / 6,482 |
| 7.1 | At most 2 cues per clause position (the old X12 row is gone) | 0 |
| 8.3 / 8.4 / 8.6 / 8.14 | New wording; checked with the precheck's own decontamination before writing | 0 / 0 / 0 / 0 |
| 9.3 / 9.5 / 9.6 | Follow from the above; AR rows have a null-cue NOT and no cue word | 0 / 0 / 0 |
| 10.8 | 54 new base texts with 0 word 8-grams in golden_train or F7 train / probe and 0 12-grams in the reference sets | 0 |

Full precheck with every input: **110 PASS, 1 FAIL (2.3), 2 PENDING (8.13, 11.1)**.
- 2.3: train and probe 15,086 / 15,086; devx 220 unparsed, because the round-1 devx parse table does not cover the new
  ids. Per the 2.3b exception, an agent who has not seen devx golds must write `yn2b/f7_devx_decide2_lf.json` again
  from `yn2b/f7_devx_blind_packet.jsonl` (no gold, no lf, no sidecar). Until then
  `test_v3_nested_negation.py::test_written_rows_agree_100_percent[devx]` also fails.
- 8.9 (combined F7 + devx cue share) briefly failed on the word "without" (36 rows, 61.1% odd) after the first
  rebuild; two devx distractors were reworded and it passes (worst word 0.58).
- Section-3 targets computed on devx alone: all 60 checks of `yn2b/f7_devx_audit.py --decontam` pass.

---

# Arbiter round 3 (2 Oct 2026)

A neutral arbiter wrote this section. It judged the open items: the orchestrator's status (220 devx rows unparsed;
2.3, 2.3b, 3.5b and 11.1 PENDING), the devx round-2 report above, and the decide2 report relayed with the task. It
did not read the generator's code (`gen3_nested_negation.py`, `nn_lexicon.py`) or the devx builder
(`f7_devx_build.py`). It wrote no data and changed no threshold.

**Files changed by the arbiter:**
- `golden_src/gen3/v3_nested_negation.py` (decide2): `bca4b2ce…` → `98681fdf9a5599ad057148d7222926f40af5ce975b3fdef59d0202056b3d805a`.
  The changes are marked "arbiter round 3" in the code: the `Ambiguous` refusal (A3, A4), the devx `AMBIG` op, and the
  check that a devx single text matches its base row.
- `yn2b/f7_devx_decide2_lf.json` (the devx parse table): rewritten for the `r_f7x2_*` ids, now
  `042d1eb4c585805f0f2777f9931c2a1c59d3407cb540e4f58b04b28db503fd88`. It is written by
  `yn2b/f7_devx_decide2_lf_author.py` (new, `ac0d59e3…`), and the build is deterministic.
- `yn2b/tests/test_v3_nested_negation.py`: now `59c0c7f4…`, with 9 new tests.
  - 5 of the new tests are behaviour tests: they fail on the old decide2 and pass on the new one.
  - The other 4 are controls: they pass on both.
  - The 3 `test_written_rows_agree_100_percent` cases fail now. They are the 2.3 gate, and they must fail until the
    rows below are rewritten.
- `yn2b/f7_decide2_preds.jsonl` (`03b49b67…`, 15,261 rows) and `yn2b/f7_decide2_report.json` were regenerated by a
  full decide2 run, with no `--files`.
- Backups of the old files are in the session scratchpad, under `arb3/`.
- **Not touched:** the precheck (`f071f2b8…`), the generator (`1d5ccf09…`), devx data (`d17f3221…`), all other data,
  and every frozen file.

**Tests.** `test_f7_precheck.py`, `test_gen3_nested_negation.py`, `test_f7_devx_build.py` and
`test_v3_nested_negation.py` give 145 passed and 3 failed. The 3 failures are the gate tests above.

## S1. Orchestrator status: 2.3, 2.3b, 3.5b and 11.1 PENDING

ARBITER: REJECTED as a tool bug. The precheck is right.
- PENDING means an input was not given. That run left out `--decide2-preds`, `--decide2-code`,
  `--decide2-independent`, `--lexicon` and `--blind-read`.
- With every input (the command in "Arbiter round 2") the result is **110 PASS, 1 FAIL (2.3), 2 PENDING (8.13, 11.1)**.
  - 2.3b PASS: declared independent; the scanned code imports nothing from the generator.
  - 3.5b PASS: 0 lexemes outside the lexicon.
- 8.13 belongs to the owner (`--ohs3-blind`). 11.1 needs a reader who has not seen any gold. This arbiter has now seen
  golds, so it cannot be that reader.

## S2. "decide2 devx: 220/220 UNPARSED (devx row not in the parse table)"

ARBITER: UPHELD. This is a decide2 bug, and it is fixed.
- **Cause.** The parse table held the 220 round-1 ids (`r_f7x_*`). devx round 2 renamed every row (`r_f7x2_*`), so no
  row matched. The table was stale; neither devx nor the precheck was at fault.

**How the table was rewritten (the 2.3b exception: the author must not have seen devx golds).**
1. **Written blind.** The arbiter wrote all 220 LFs and 44 ladder entries from `yn2b/f7_devx_blind_packet.jsonl`
   only. That packet holds id, ladder_id, orig, qtype, state, instructions, card and options, with no gold.
   - Before the table was hashed, nothing else from devx was opened. The only exception is a script that printed the
     key names of `f7_devx.jsonl`, with no values except `track` / `dev_kind`.
   - Every fact is quoted from the state.
   - Label and item atoms are evaluated against the human label of `meta.orig`.
2. **Hashed before any gold.** The table was hashed before any gold, sidecar or relation file was read:
   `407c27f1acb2d30eb978fcc485a5cb1e5f38ad9e95208e921ee3fbdd8f942dff`, at 14:46 UTC.
3. **Result on the first run.** devx agreed on 220/220 (176 yes/no and 44 choice), with 0 disagreements and 0 unparsed
   rows.
4. **Sensitivity.** The table depends on the human labels and on the negations; it does not agree by default.
   - Twin-swap test: each ladder is evaluated on its twin's text, base label and facts. All 176 yes/no predictions
     flip, and 38 of the 44 choice rows become invalid.
   - With every NOT dropped, yes/no agreement falls to 102/176.
   - With one NOT added on top, yes/no agreement is 0/176.
5. **Premise checks.** Every wiki base label is one of the desks or boards its card lists, so "exactly one listed …"
   holds. No SaferProducts base is 'death', the one value the 'medical care' and 'home-handled' maps leave out.
6. **One change after the golds were seen** (disclosed).
   - Six LFs were wrapped in `AMBIG` (A3, A4 below): `r_f7x2_14a_3`, `14b_3`, `14a_4`, `17a_1`, `17b_1` and `17a_4`.
   - The wrapper is applied by rule to every devx exceptive, and to every 'opposite' of a universal batch claim,
     whatever the outcome.
   - With the wrappers stripped (reading A), the table equals the pre-gold version byte for byte.
7. **Hardening.** decide2 checked that each batch text matches its base row, but it did not check single texts.
   - A wrong `meta.orig` would then give the builder and decide2 the same wrong label, and they would agree.
   - decide2 now refuses a single-text devx row whose state is not its base text. All 26 single-text ladders match.
   - Test: `test_devx_single_text_label_must_belong_to_the_shown_text`.

## S3. decide2 report relayed with the task (17 disagreements and 2 unparsed rows in 6 probe ladders)

ARBITER: CLOSED, as in round 2.
- That report is the round-0 decide2 author's record, and D1 ruled it a generator bug.
- On the current build there are 0 disagreements in train, probe and devx.

## S4. devx round 2: the repairs claimed above

ARBITER: UPHELD (verified), with two ambiguous rows that must be rewritten (A3 and A4 below).
- **The 15 devx failures are fixed.** With every input, all 15 round-1 devx failures now PASS: 1.2, 1.4, 3.3, 4.1c,
  4.2c, 5.l, 7.1, 8.3, 8.4, 8.6, 8.14, 9.3, 9.5, 9.6 and 10.8. So do 3.9 (220 devx rows), 10.6 and 10.7.
- **Two rows are not fixed.** Writing the table by hand meant reading every devx row. Two rows have two readings with
  different golds:
  - `r_f7x2_17b_1`, an exceptive (A3);
  - `r_f7x2_14a_3`, 'opposite' of a universal claim (A4).
- **Other wording.** No other devx row was found ambiguous. Every 'reverse' / 'opposite' / 'denial' over a binary claim
  or a numeric claim (L01, L04, L11, L13, L15, L20, L21) has one reading.

## A3. Universal or negative exceptives whose excepted item lacks the property

ARBITER: UPHELD. These are ambiguous rows (generator and devx must rewrite). It is also a decide2 gap, now fixed.

**The two readings.** "No comment other than Comment 4 is toxic" can be read two ways:
- **Literally (set minus):** comments 1, 2, 3 and 5 are not toxic.
- **As an exceptive:** the same, and Comment 4 is toxic. This is the inclusion condition of exceptives (von Fintel
  1993, "Exceptive constructions"; Moltmann 1995). It is at least a strong implicature.

**Where they differ.** When the excepted item lacks the property, the literal reading can be true while the exceptive
reading is false. decide2 read only the literal one.

**The checklist.** It does not settle this case. Item 31's only example is existential ("Is any review other than the
second one positive?"), and existentials carry no inclusion condition. They stay literal.

**Evidence.** Counted with decide2's own batch labels (the human labels):

| File | Universal / negative exceptive rows | Gold depends on the reading | Ladders |
|---|---|---|---|
| train | 148 | 26 | 00111b, 00227b, 00736a, 01290a, 01451a, 01542b, 02179a, 02621a, 02847b |
| probe | 34 | 4 | ho_00382a |
| devx | 2 (+2 fronted) | 1 | `r_f7x2_17b_1` |

- **All 30 train / probe hits are all-false batches.** Example: `r_f7nn2_f7v2_ho_00382a_3`, "Say yes when no comment
  other than Comment 4 is toxic, …", where all five comments are non-toxic. The gold is yes under the literal reading
  and no under the exceptive one.
- **devx `r_f7x2_17b_1`.** "Is it true that no post apart from Post 3 belongs at the Language desk?" The posts are at
  the Science, Humanities and Mathematics desks. The gold is yes under the literal reading and no under the exceptive
  one.
- **Not ambiguous.** In `r_f7x2_17a_1`, `14a_4` and `17a_4` the excepted item has the property, so the two readings
  agree.

**decide2 fix.** `MultiWorld.exceptive` refuses a row when the literal and the inclusion readings differ.
- The refusal uses the class `Ambiguous`. No frame or peel fallback swallows it.
- Existential exceptives stay literal.
- Tests: `test_negative_exceptive_refused_when_excepted_item_lacks_the_property`,
  `test_negative_exceptive_read_when_inclusion_holds` and `test_existential_exceptive_stays_literal`.

**Generator to do.** For a negative or universal exceptive, pick an excepted item that has the property the quantifier
denies the rest (for "no / none / not a single", P(e) must be true; for "every / all", P(e) must be false). Otherwise,
use the existential form.
- Never use a negative exceptive on an all-false batch.
- Keep item 31 at its floor.

**devx to do.** Pair 17's question must have one reading in both twins. For example, use "Does any post other than
Post 3 belong at the Language desk?", which keeps item 31.

## A4. 'the opposite / reverse of a claim' over a universal claim on a mixed batch, with no definition in the card

ARBITER: UPHELD. These are ambiguous rows (generator and devx must rewrite). It is also a decide2 gap, now fixed. This
is ruling #6 (contrary) applied to the other two frame words.

**The two readings.** Take "the opposite of the claim 'not a single request asks for pothole repair'":
- **Plain denial:** some request asks for pothole repair.
- **Contrary:** every request asks for pothole repair, as in "the opposite of none is all".

**Where they differ.** On a mixed batch the two readings give different golds. The probe 'contrary' rows carry the
card line "here 'the contrary of a claim' means its plain denial …", so they are settled. The train 'opposite' and
'reverse' rows carry no such line.

**Evidence.**

| File | Universal claims under 'opposite' / 'reverse' | On a mixed batch, no definition | Ladders |
|---|---|---|---|
| train | 26 | 13 | 00033b, 00372b, 00503b, 00640b, 00736b, 00813b, 01080b, 02036a, 02209b, 02621b |
| probe | 0 | 0 | — |
| devx | 2 | 1 | `r_f7x2_14a_3` |

- **Probe 'contrary'.** 2 probe rows would differ without their card line, and they carry it.
- **Example.** `r_f7nn2_f7v2_tr_00372b_4`: "We need the opposite of a claim. … Claim: not a single request in the batch
  asks for pothole repair. … is that opposite borne out by the batch?" Requests 1-3 are T, F and F. The gold is yes
  under denial and no under the contrary reading.
- **devx `r_f7x2_14a_3`.** Only Comment 3 is toxic. The gold is no under denial and yes under the contrary reading.
- **Not counted.** A quantifier inside a term definition is left out. 'The reverse of the claim that the batch fails to
  count as tag K' is a yes/no claim about the batch.
- **Cross-check.** A separate regex scan of the same files found the same 13 train rows.

**decide2 fix.** `World.frame_guard` refuses such a row unless the card defines the frame word as plain denial.
- Tests: `test_opposite_of_universal_claim_on_mixed_batch_refused` (it also shows that adding the wording line settles
  the row), `test_defined_contrary_is_read_and_undefined_contrary_is_refused` and
  `test_quantifier_inside_a_term_definition_is_not_counted`.

**Generator to do.** Add the 'contrary' wording line, worded for the word used, to every row whose 'opposite' or
'reverse' frame applies to a quantified batch claim. For example: "- wording: here 'the opposite of a claim' means
its plain denial: the opposite holds exactly when the claim itself fails".

**devx to do.** Do one of these for pair 14:
- give it the same wording line for 'opposite';
- use 'denial' instead of 'opposite'.

## decide2 after round 3 (the final state)

**Agreement.**

| File | Rows | Agree | Disagree | Refused as ambiguous |
|---|---|---|---|---|
| train | 12,588 | 12,549 | 0 | 39 (A3 26, A4 13) |
| probe | 2,498 | 2,494 | 0 | 4 (A3 4) |
| devx | 220 | 218 | 0 | 2 (A3 1, A4 1) |

- Compared with round 2, 0 train / probe predictions changed. 43 rows are now refused.

**Full precheck** (every input; preds `03b49b67…`): **110 PASS, 1 FAIL (2.3: 15,261/15,306, 45 unparsed), 2 PENDING
(8.13, 11.1)**.

## Disclosures

- **Rows and sidecars read.** For A3 and A4, the arbiter read rendered F7 train / probe rows and one train sidecar row
  (`r_f7nn2_f7v2_tr_00147a_4`, to see how the generator encodes exceptives).
  - The decide2 changes use only the rendered text and the human labels.
  - After the devx table was hashed, the arbiter read the devx sidecar of 4 rows: 14a_4, 17a_1, 17a_4 and 17b_1.
- **What the arbiter has now seen.** It has seen the devx golds. So it must not write devx LFs again, and it must not be
  the 11.1 reader.
- **ohs3.** No ohs3 file was opened or globbed.

## Still open before ship (nothing is waived)

1. **Generator.** Rewrite A3 (30 rows in 10 ladders) and A4 (13 rows in 10 ladders) at the source, then rebuild.
2. **devx.**
   - Rewrite the pair-17 question (A3) and the pair-14 opposite row (A4).
   - Keep every other row byte for byte, so that its LF still applies.
   - Then an agent that has not seen devx golds writes the LFs of the changed rows. This is the 2.3b exception again.
     The new single-text check and the id match make any stale row fail safe.
3. **decide2.** Run with no `--files`; the target is 100% with 0 refused rows. Then run the full precheck. Then the
   owner runs 8.13 (`--ohs3-blind`), and a separate blind reader does 11.1.

---

# Generator round 3: repairs for arbiter round 3 (2 Oct 2026)

Written by the round-3 repair agent. Order of work, so that the blindness rules hold:
1. **devx first, before any F7 renderer was opened.** The agent edited `yn2b/f7_devx_build.py` for pairs 14 and 17
   only, rebuilt devx, and recorded the devx hashes (15:19 UTC) before it opened `gen3_nested_negation.py` or
   `nn_lexicon.py`. Details are in `yn2b/F7_DEVX_NOTES.md` section 5.
2. **Then the generator.** It changed `gen3_nested_negation.py` and `nn_lexicon.py` and rebuilt F7 (`f7_counts.json`
   revision `r3`). The round-1 build is kept byte for byte in `data/v14_parts/f7_v2_r1_backup/`.

**Not touched:** decide2 (`98681fdf…`), the precheck (`f071f2b8…`), the devx parse table (`042d1eb4…`) and every frozen
file. Nothing was committed. No ohs3 file was opened or globbed.

## What changed, per ruling

| Ruling | Repair at the source | On the rebuilt files |
|---|---|---|
| A3 exceptives | `MultiSubject._world`: in an EXCEPT ladder, the excepted item has the property in **both** twins (the inclusion condition). So "no / none of the / not a single X other than X j" reads the same literally and as an exceptive. No negative exceptive runs over an all-false batch. `ambiguity_invariants` stops the build (it never filters a row) if any negative exceptive sits outside such a ladder, or if a universal exceptive appears at all. | Negative-exceptive rows: 134 train, 60 probe. decide2 refuses 0 (it was 26 train and 4 probe). Item 31: train 224 (floor 150), iid 70, holdout 30 (floors 20 / 10). |
| A4 'opposite' / 'reverse' | Every row whose frame says 'opposite' or 'reverse' carries the wording line for that word, e.g. "- wording: here 'the opposite of a claim' means its plain denial: the opposite holds exactly when the claim itself fails". `nn_lexicon.frame_word_def`; the 'contrary' line stays byte for byte. This covers every subject kind, not only quantified batches, because on ordinal label sets 'opposite' also invites the antonym label (ruling #6's second reason). No card distractor may use the 'wording' key on these rows. | 860 train and 144 probe frame-word rows, all with their line. decide2 refuses 0 (it was 13 train). |
| devx pairs 14 / 17 | See `F7_DEVX_NOTES.md` section 5. Pair 17's question is now "…no post apart from Post 3 belongs at either of the Language and Mathematics desks?" Post 3 is a Mathematics post in both twins, so the inclusion holds. Pair 14's card defines 'the opposite' as plain negation. The 4 rows get new ids `r_f7x3_*`, so the stale round-2 LFs cannot match them. The other 216 rows are byte for byte round 2. | devx audit (`--decontam`): 60 / 60 PASS. |

**Two more generator bugs found by the rebuild, fixed at the source:**
- **devx texts reached the probe.** The generator excluded devx states by whole-state hash only. A devx batch quotes
  its texts inside a numbered list, so the hash missed them.
  - The first rebuild put 6 devx base texts into 6 holdout probe ladders: up to 85 of 85 word 8-grams shared.
    `f7_devx_pool_scan.py` found it.
  - Now every pool text that shares a word 8-gram with any devx state is dropped (34 texts).
  - Result: pool scan 54 texts, 0 with overlap.
- **8.9 failed on the union with devx.** On that build, 8.9 failed: 'without' was odd in 24 of 38 rows (63%).
  - Cause: the selection's word rule did not count the devx rows, and the in-loop audit ran without devx.
  - Fix: the word rule starts from the devx rows' instruction-word counts (`devx_word_base`: only words and the parity
    of the sidecar depth; no devx text, gold or label enters a row), and the in-loop audit now includes the devx
    rows, as the ship precheck does.
  - Result: 8.9 PASS. The worst word is 'contradicted', 20 / 34 (58.8%).

## decide2 (frozen, independent, run with no `--files`)

| File | Rows | Agree | Disagree | Unparsed / refused |
|---|---|---|---|---|
| train | 12,586 | 12,586 | 0 | 0 |
| probe | 2,494 | 2,494 | 0 | 0 |
| devx | 220 | 216 | 0 | 4 (`r_f7x3_14a_3`, `14b_3`, `17a_1`, `17b_1`: "devx row not in the parse table") |

## Full precheck (every input, `--decide2-independent yes`): 110 PASS, 1 FAIL, 2 PENDING

- **2.3 FAIL:** 15,296 / 15,300, the 4 new devx rows above. This is the 2.3b exception: their LFs must be written by an
  agent who has seen no devx gold and never read the generator. This agent has done both, so it did not write them.
- **8.13 PENDING:** owner step (`--ohs3-blind`).
- **11.1 PENDING:** a separate blind reader.
- **Everything else passes**, including 2.1 (15,300 / 15,300), 2.2, 2.3b, 3.1 (38 / 38 items), 3.5b, 4.3, 4.13
  (39 capable, 0 below), 8.9, 8.11 and 10.6 (max 12-gram share 0.0).
- **Reproducible:** a second build (no write) gave identical summaries for all three parts.

## Tests

`test_f7_precheck.py`, `test_gen3_nested_negation.py`, `test_f7_devx_build.py`, `test_v3_nested_negation.py`:
**158 passed, 2 failed.**
- The 2 failures are the gates for the 4 missing devx LFs: `test_devx_parse_table_covers_the_round2_ids` and
  `test_written_rows_agree_100_percent[devx]`.
- New tests:
  - frame-word lines;
  - exceptive inclusion on an EXCEPT-only build;
  - the hard invariants raise on a bad ladder;
  - written-file round-3 checks;
  - 0 shared 8-grams with devx;
  - union word parity;
  - devx: the 4-row diff, pair-17 inclusion, the 'opposite' definition.
- The decide2 behaviour tests (R1.x, A3, A4) now read their named rows from the round-1 backup. Generator round 3
  reassigned row ids, and the A3 / A4 rows are gone from the written files by design. The AMBIG test reads the
  round-2 devx rows and table from `data/v14_parts/f7_devx_r2_backup/`.

## Also closed

`yn2b/f7_v1_adapter.py` read `data/v14_parts/f7_*` (now v2) and called the removed `decide2_row(row, base)`.
- It now reads `data/v14_parts/f7_v1_backup/`.
- Its decide2 path stops with a clear message.
- `--no-decide2` still works.

## Still open before ship (nothing is waived)

1. **Blind devx LFs (2.3b exception).** An agent who has seen no devx gold and never read the generator writes the LFs
   of `r_f7x3_14a_3`, `r_f7x3_14b_3`, `r_f7x3_17a_1` and `r_f7x3_17b_1`. It works from `yn2b/f7_devx_blind_packet.jsonl`
   only, adds them to `yn2b/f7_devx_decide2_lf_author.py` and rebuilds `yn2b/f7_devx_decide2_lf.json`. Then decide2
   runs with no `--files` (target 15,300 / 15,300, 0 refused) and the full precheck runs again.
2. **8.13:** the owner runs `--ohs3-blind`.
3. **11.1:** a separate blind reader.

---

# Arbiter round 4 (2 Oct 2026)

A new, neutral arbiter wrote this section. It judged the open items in the orchestrator's status (2.3 FAIL on 4 devx
rows; 8.13 and 11.1 PENDING) and the decide2 report relayed with the task. It did not open the generator
(`gen3_nested_negation.py`, `nn_lexicon.py`), the devx builder (`f7_devx_build.py`), any sidecar or relation file, or
any ohs3 file. It changed no threshold and no data row.

**Files changed by the arbiter** (backups of every old version: session scratchpad `arb4/`):

| File | Before | After | What changed |
|---|---|---|---|
| `yn2b/f7_devx_decide2_lf_author.py` | `ac0d59e3…` | `079dbf93…` | 4 new LFs (`r_f7x3_*`); the 4 stale `r_f7x2_*` LFs removed; `text_sha256` binding |
| `yn2b/f7_devx_decide2_lf.json` (parse table) | `042d1eb4…` | `55517be1…` | built by the script above (deterministic: two builds, same hash) |
| `golden_src/gen3/v3_nested_negation.py` (decide2) | `98681fdf…` | `d673b7a3…` | `devx_text_sha` and one check in `DevxEval.decide` (marked "arbiter round 4") |
| `yn2b/tests/test_v3_nested_negation.py` | `161902f3…` | `3baf9cb8…` | 1 assertion pair + 2 new tests; the round-2 AMBIG test binds its old table to the round-2 text |
| `yn2b/f7_decide2_preds.jsonl`, `yn2b/f7_decide2_report.json` | `6d74be3b…` | `295a26a8…` | full decide2 run, no `--files` (a second run gives the same hash) |
| `yn2b/f7_precheck.json` | | `dc556ddf…` | the full precheck run below |

**Not touched:** the precheck (`f071f2b8…`), the generator, train / probe / devx data (`7d5bf9fa…`, `fda0907c…`,
`b5579786…`), every frozen file. Nothing was committed.

## T1. 2.3 FAIL: 15,296 / 15,300, 4 devx rows "devx row not in the parse table"

ARBITER: UPHELD. This is a decide2 bug (a stale parse table), and it is fixed. It is not a generator, devx or precheck
bug, and none of the 4 rows is ambiguous.

**Cause.** The parse table is keyed by row id only. devx round 3 rewrote 4 rows and gave them new ids
(`r_f7x3_14a_3`, `14b_3`, `17a_1`, `17b_1`), as arbiter round 3 asked, so decide2 found no LF for them. The precheck
counted them as unparsed, which is right.

**Checks before writing anything.**
- The current blind packet against the round-2 packet (`f7_devx_r2_backup/`), field by field: 216 rows identical,
  4 rows new. `14*_3` changed only the card; `17*_1` changed the instructions and the card. So the 216 old LFs still
  apply as written.
- The blind packet against `data/v14_parts/f7_devx.jsonl` (state, instructions, card, options, ladder_id, orig):
  0 mismatches on 220 rows. A script compared them and printed counts only.

**The rows are not ambiguous.**
- `r_f7x3_14*_3`: "Consider the opposite of the next claim. Claim: not a single comment is toxic. Does the batch give
  grounds to dismiss that opposite?" The card now says "here 'the opposite' of a claim means its plain negation" and
  "the comments settle every claim asked about here". So there is one reading: yes iff no comment is toxic. The A4
  contrary reading is excluded by the card.
- `r_f7x3_17*_1`: "Is it true that no post apart from Post 3 belongs at either of the Language and Mathematics
  desks?" This is a negative exceptive. By rule (A3), its LF holds both readings: literal (neither Post 1 nor Post 2 is
  a Language or Mathematics post) and inclusion (that, and Post 3 is a Language or Mathematics post). decide2 refuses
  the row if they differ. They agree in both twins, so Post 3's human label satisfies the inclusion condition.

**The 4 LFs** (in the author script, block "devx round 3"):
- `r_f7x3_14*_3`: `NOT(NOT(NONE(C1..C4)))`.
- `r_f7x3_17*_1`: `AMBIG(A3, lit, AND(LM(3), lit))`, where `lit = AND(NOT LM(1), NOT LM(2))` and
  `LM(k) = OR(I(k, Language desk), I(k, Mathematics desk))`.

**How they were written (the 2.3b exception).**
- Written from `yn2b/f7_devx_blind_packet.jsonl` only (no gold field). The table was hashed (`55517be1…`) at
  16:48:30 UTC, before decide2 or the precheck ran on it.
- Disclosure: before writing, this arbiter had read two gold-bearing remarks about the OLD round-2 rows. They were:
  - arbiter round 3 above: on `r_f7x2_14a_3`, "only Comment 3 is toxic; gold no under denial";
  - a comment in the round-2 AMBIG test: on `r_f7x2_17a_1`, "Post 2 is a Language post: both readings say no".
- The new LFs follow the English construction and the A3 rule, not those remarks. The checks below show that the
  answers come from the human labels.

**Sensitivity of the 4 new LFs** (agreement with gold, counts only):

| Variant | Agree |
|---|---|
| as written | 4 / 4 |
| one NOT dropped (17: on both readings) | 0 / 4 |
| one NOT added on top | 0 / 4 |
| twin swap (each LF on its twin's text and labels) | 0 / 4 (all 4 flip) |
| 14: contrary reading instead of the defined denial | 3 / 4 (so the card's definition line decides one twin) |
| 17: literal reading only / inclusion reading only | 4 / 4 each (the readings agree, as A3 requires) |

**Root-cause fix in decide2: a stale LF can no longer apply silently.**
- Before: if devx had rewritten a row and kept its id, decide2 would have used the old LF on the new text without
  notice. Only the id rename made this round fail safe.
- Now: the table stores, per row, the sha256 of `[state, instructions, card, options]` of the text the LF was written
  from (`text_sha256`). `DevxEval.decide` refuses a devx row whose text hash differs, or that has no hash
  (`ParseError`: "devx row text differs from the text its LF was written from").
- The author script binds the 216 `r_f7x2_*` LFs only after checking that each row is byte for byte the round-2 text
  they were written from. Otherwise the build stops.
- Tests:
  - `test_devx_parse_table_covers_the_round2_ids` now also checks that every written row is bound to its exact text.
  - New `test_devx_stale_lf_refused_when_the_text_changes` (2 cases) fails on the old decide2 and passes on the new
    one. The cases are: drop the card's 'opposite' definition line; drop one negation from the claim. The control
    (the written row) is read.

## T2. 8.13 PENDING (OHS-3 12-gram count)

ARBITER: REJECTED as a bug. The precheck is right.
- This is an owner-only step: `--ohs3-blind` opens OHS-3, and build agents and this arbiter may not.

## T3. 11.1 PENDING (blind read)

ARBITER: REJECTED as a bug. The precheck is right.
- The check needs a reader who did not write the generator. It also cannot be anyone who wrote decide2 LFs or read the
  golds, so it is not this arbiter.
- `f7_precheck.py --write-blind-sample <path>` writes the sample without gold: 100 random rows plus 10 per MUST item.
- The reader returns `{id, verdict}` for each row, with verdict `ok`, `wrong_gold`, `unreadable` or `ambiguous`.
- To pass: 0 `wrong_gold`, and unreadable plus ambiguous at most 3%.

## T4. decide2 report relayed with the task (17 disagreements and 2 unparsed rows in 6 probe ladders)

ARBITER: CLOSED, as in rounds 2 and 3.
- That is the round-0 decide2 author's report, already ruled D1 (generator bug) and repaired.
- On the current build, train and probe agree 100%, with 0 refused.

## Generator round 3's claims, re-checked independently (no new objection)

- **A4 frame words.** A regex scan of the written rows found every 'opposite' / 'reverse' / 'contrary' frame row with
  its plain-denial wording line: train 860 (552 reverse, 308 opposite), probe 144 (30, 44, 70). This matches the
  generator's counts.
- **devx frame words without the line.** 12 devx rows (pairs 01, 04, 11, 15, 20, 21) carry no wording line. Each is
  over a binary label, a single event or a count claim, so it has one reading, as round 3 (S4) ruled. No devx frame
  word is over an ordinal label set.
- **A3 exceptives.** Train and probe have only negative exceptives ('no / none of the / not a single … other than /
  apart from'). There are 0 universal and 0 fronted ones. decide2's inclusion guard refused 0 rows.

## Final state

- **decide2** (no `--files`): train 12,586 / 12,586, probe 2,494 / 2,494, devx 220 / 220. 0 disagreements, 0 refused,
  0 unparsed.
- **Full precheck** (every input, the round-2 command, `--decide2-independent yes`): **111 PASS, 0 FAIL, 2 PENDING
  (8.13, 11.1)**.
  - 2.3 PASS (15,300 / 15,300). 2.3b PASS (declared independent; decide2 imports nothing from the generator, and the
    only new import is `hashlib`).
- **Tests** (`test_f7_precheck.py`, `test_gen3_nested_negation.py`, `test_f7_devx_build.py`,
  `test_v3_nested_negation.py`): **162 passed, 0 failed**.

## Disclosures

- No ohs3 file was opened or globbed.
- Two scripts opened `f7_devx.jsonl` (which holds gold), and both printed counts only:
  - the text cross-check against the packet;
  - the sensitivity table.
- The new test reads one devx gold as its control.
- One decide2 check run wrote its output to `/private/tmp/x.json(l)` by mistake. Those two files were deleted at once,
  and the project outputs above come from the normal run.

## Still open before ship (nothing is waived)

1. **8.13:** the owner runs `--ohs3-blind`.
2. **11.1:** a separate blind reader (see T3).

---

# Generator round 4: re-check after arbiter round 4 (2 Oct 2026)

Written by the round-4 generator repair agent. The relayed status (2.3 FAIL on 4 devx rows) was the round-3 state.
Arbiter round 4 had already fixed it in decide2's devx parse table. This agent changed no generator code, no data row,
no decide2 code or table, no precheck and no frozen file, and committed nothing. No ohs3 file was opened or globbed.

**Independent re-runs on the current files** (outputs in the session scratchpad `gen4/`):

| Check | Result |
|---|---|
| Generator rebuild (in memory, `PYTHONHASHSEED=0`, no `--write`) vs the files on disk | byte-identical for all 8 generator outputs (train, train relations, train meta, probe, probe relations, probe meta, lexicon, holdout spec) |
| decide2, no `--files` | train 12,586 / 12,586, probe 2,494 / 2,494, devx 220 / 220; 0 disagree, 0 unparsed; preds byte-identical to `yn2b/f7_decide2_preds.jsonl` (`295a26a8…`) |
| Full precheck (every input, `--decide2-independent yes`) | 111 PASS, 0 FAIL, 2 PENDING (8.13, 11.1) |
| Tests (`test_f7_precheck.py`, `test_gen3_nested_negation.py`, `test_f7_devx_build.py`, `test_v3_nested_negation.py`) | 162 passed, 0 failed |

**Old decide2 "other findings", re-scanned on the current rows** (train and probe, F7-authored text only): 0 "others
need", 0 "is X or does not", 0 "minutes fails / settles", 0 "a" before a vowel word, 0 "dead line 2", 0 "at most one
of the … report", 0 repeated words inside one field, 0 byte-identical rows inside a ladder. Every 'opposite' /
'reverse' / 'contrary' frame row has its plain-denial wording line (train 860, probe 144). Item 23 now defines its term
over the unit the question asks about ("a message / a post that fits …"). Train relations: 3,306 complement +
2,742 inv.

**11.1 is ready for its reader.** `yn2b/f7_blind_sample.jsonl` holds the 280-row sample (100 random + 10 per MUST
item), written by `f7_precheck.py --write-blind-sample`, with no gold field. The reader must not be this agent, any
generator or devx author, any decide2 LF author, or any arbiter who has seen golds. It returns `{id, verdict}` per row
(`ok`, `wrong_gold`, `unreadable`, `ambiguous`), and the precheck runs again with `--blind-read <file>`.

## Still open before ship (nothing is waived)

1. **8.13:** the owner runs `--ohs3-blind`.
2. **11.1:** a separate blind reader reads `yn2b/f7_blind_sample.jsonl`.
3. **Owner doc item (checklist line 20):** SPEC §5 still lists the old F7 (`gen3_norm_action`); the owner updates that row.
