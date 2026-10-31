# T01 full-generation failure: diagnosis (15 Oct 2026, Sonnet 5.5 code agent; widened by the orchestrator to all families)

Scripts and raw outputs: `c2_build/zed_orch/t01diag/` (`diag_build.py` T01, `diag_fam.py` any family, `exposure.py`,
`compare_gates.py`, `e*_*.json`, `s_pilot_*.json`, `fid_*`, `run_*`, `fix_*`). Backups of the edited tool files: `c2_build/_backup_t01diag/`.
All builds are in memory, `nice -n 10`, at most 3 workers; no commit, no network, no generator edited, no bar changed.

## 1. Verdict

1. **T01 is not a tool failure.** Two independent proofs:
   - The tool build (loader patch + `apply_exclusions`) and the pilot runner's own build (`run_pilot_i3._patched`, no exclusion step)
     at the full-generation QC seed base 3,000,000 give **byte-identical rows** (`rows_digest cb3e6387ba5e`, 6,002 rows) and identical G6 numbers
     (`e1_tool_3000000.json` vs `e3_pilot_3000000.json`).
   - For T01 the exclusion step is a no-op: 177 banned ids match **0** skins (the loader already removed the A43 f forms),
     0 dead question forms, redraw off (T01 is a FALLBACK family).
2. **The kit choiceplan hypothesis does not apply to T01.** T01 never calls `plan_choice`. It draws `K_DRAW = (3, 4)` from the row key, `ordered_k` shrinks k
   to the error range, and `build_options` takes the gold position and rank from `uhash(row_key, ...)`, a pseudo-random draw with no exact balancing in any path.
3. **G6 is a fresh-seed outcome of the generator**, sitting close to the bar. Choice G6 maximum excess over chance (LR, 6,000 rows, G15 off):

   | seed base (pilot path) | choice chance | max cell | excess |
   |---|---|---|---|
   | 900,000 (binding pilot G6_AT) | .342 | d_meta LR .3495 | +0.75 pp |
   | 3,000,000 (the failed QC) | .343 | a_question LR .3754 | **+3.24 pp** (b_options +2.25, c_card +2.60, d_meta +1.83) |
   | 5,000,000 | .343 | c_card LR .3613 | +1.85 pp |
   | 6,000,000 | .349 | b_options LR .3412 | -0.78 pp |
   | 7,000,000 | .347 | b_options LR .3676 | +2.07 pp |

   Mean excess +1.43 pp, SD about 1.7 pp over 5 seed sets: a fresh draw fails the bar (+2.00 pp) about 2 times in 5. Yes/no cells stay at or below +1.3 pp.
   The brief's "choice chance about .362" is wrong: pilot and full-gen both sit at .342-.343, and the option-count mix is the same
   (k=2/3/4 rows: 574/1464/849 at the pilot seed, 551/1503/775 at 3,000,000).
4. **Question forms do not predict the gold slot.** On the 6,000-row QC build gold position is uniform per k (chi-square p .33 / .21 / .32 for k = 2 / 3 / 4) and
   qform x gold-position is independent (p .35 / .59 / .27). `gold_has_kind_vs_expected` shows no length leak (gold is longest +0.26 pp, shortest -0.19 pp).
5. **G10 gold_position / gold_rank (candidate build, 2,000,000) is a statistical artefact of the check, not a balance defect.**
   - The positions are one hash draw per (row key, k) cell, and partner rows (twins, complements) re-use the cell. T01 has 1.49 choice rows per cell
     (T28 1.63, 6,000-row QC build 1.47). The G10 chi-square counts each row, so its variance is inflated by that factor.
   - Simulation of a perfectly hash-uniform generator with T01's cell structure: P(some k fails at p <= .01) = **19%** for gold_position and the same for gold_rank
     (about 34% for either). T28 (six k levels tested): **59%**.
   - Counted per distinct cell, the failing result is not significant: T01 k=2 position 89 / 66 cells, p = .065 (rows 134 / 90, p = .0033);
     T28 per-cell p all >= .039.
   - The pilots passed because 1,000 rows have fewer tested k levels and fewer rows per cell. This is a property of `pilot.g10` (shared, not edited, bar not touched); the orchestrator rules.

**Under A44 / A45 T01's generator is therefore the binding unknown.** I did not re-run T01 on new seeds: a re-draw would be seed shopping on a gate whose pass
probability is about 60% per draw (G6) times about 65% (G10 position + rank).

## 2. The widened question: is the tool the cause for the other families?

### 2.1 Q1: does `gen_full_c2` reproduce each family's latest runner build path?
Yes. Every runner (`run_pilot_i1/i2/i3`) ends in `pilot.run_family`, which is `open_family` + `pilot.build_pilot(kit, n, run_g15)` + gates. The runners add only
loader patches and output-folder redirects: no schedule, weighting, quota, label-first draw or `build_weighted` logic (checked by reading all 15; T21 is not a full-generation family).
Empirical check: `loader_patch` rebuilds at seed base 900,000 / 1,000 rows / G15 on reproduce each binding pilot's `PILOT_REPORT.files.rows_sha256` **exactly** for
T23, T15, T28, T33, T31, T07, T12 (T01 checked through its own runner). So the loader patches are faithful.

### 2.2 Q2: does exclusion / never-draw / redraw shift the mix, gold position or yes rate?
- Candidate builds at the full-generation seed base 2,000,000, runner path (no exclusion) against the tool (`run_*_2000000.json` vs `GEN_REPORT.json`):

  | family | skins removed / dead qforms | runner = tool? | yes/no share runner / tool | failing G10 checks (same in both) |
  |---|---|---|---|---|
  | T23 | 10 / none | identical to 4 decimals | .4375 / .4375 | yes_no_share, yes_rate (+ overlay twin_share .2567) |
  | T31 | 0 / none | identical | .5596 / .5596 | yes_no_share |
  | T12 | 25 / none | identical | .5342 / .5342 | longest_option_gold_pp -2.62, yes_is_bad_share .571 |
  | T07 | 16 / none | identical | .5350 / .5350 | abstain_wrong_share (per-cell) |
  | T28 | 18 / yn_mustnot_syn (never drawn) | small shift | .4926 / .4828 | gold_position (row-level chi-square, see 1.5) |
  | T15 | 29 / yn_dneg_claim, yn_dneg_eligible | small shift | .4726 / .4585 | longest +2.89 / +2.98, yes_rate .527 / .525; G11 ch_outcome wording 2.07% / 2.52% |
  | T33 | 73 / yn_dneg_all_supported, yn_dneg_step_ok | shift | .5272 / **.4854** | longest +2.83 / +2.47; spec_3_0 mean tokens: runner pass, tool **805.7 (> 800)** |

  For T23 / T31 / T12 / T07 the gate failures are the generator's at fresh seeds, not the tool's (zero difference).
- **One genuine tool defect found: the redraw changed the question type.** `Redraw` replaced a dead yes/no draw (an A43 f double-negation form) by a draw from the
  whole sampler distribution, so about half of those draws became choice rows. Yes/no share fell: T33 .527 -> .485 (and mean tokens rose over the 800 bar),
  T25 .466 -> .441 (below the 45% bar), T15 -1.4 pp, T26 / T32 exposed the same way. The yes rate and the gold-position tests were not moved (T33 yes rate .5061 / .5063;
  positions are hash draws from the row key).
- **Fix (in `gen_full_c2.py`, backups in `_backup_t01diag/`):** `Redraw` now rejects on question type: a dead yes/no form is redrawn until a live yes/no form comes up (same for choice),
  same seed + j x REDRAW_STRIDE rule, block position kept. Fixed-tool candidate builds at 2,000,000, same n:

  | family | yes/no share: runner / old tool / fixed tool | other effect of the fix |
  |---|---|---|
  | T33 | .5272 / .4854 / **.5146** | spec_3_0 mean-token fail gone (pass) |
  | T25 | .4656 / .4406 / **.4673** | back inside 45-55% |
  | T15 | .4726 / .4585 / .4585 | no change (its redrawn units were already yes/no on the first redraw) |

  Test: `tests/test_gen_full_seed_bases.py::test_redraw_keeps_question_type_and_block_position` (a stub plugin: yes/no share unchanged, live draws untouched, shadow removed) and
  `test_old_redraw_would_have_shifted_the_mix` (documents the defect). All 9 tests of the file pass.
- **Also added (tool option, defaults unchanged):** `--seed-bases CAND QC MIXDEV` (documented new bases; each divisible by 32, >= 1,000,000 apart, disjoint from the pilot
  range, refused when the family's existing `GEN_REPORT.json` already used one: failed seeds are never re-drawn); the bases are written to `GEN_REPORT.seeds`. Tested
  (valid, bad, reuse refused, reaches `build_pilot` and `build_mixdev` and the report on a T30 dry run).

### 2.3 G6 for T33 and T15 (QC build 6,000 rows at 3,000,000, runner path, no exclusion)
G6 fails there too, so the QC failures are not the tool's: T33 choice c_card_without_question LR .3464 vs .3076 (**+3.88 pp**; tool +4.98 pp, tool also a_question +2.44 and yes/no d_meta GBT +2.87);
T15 choice c_card LR .3702 vs .3333 (**+3.69 pp**; tool +2.31). Both binding pilots' own maximum cell was this same view (T33 +1.46 pp, T15 +1.88 pp at seed 900,000) and
T01's c_card is +2.60 pp at 3,000,000: a small, repeating excess in the choice card view that the pilot seed under-states. Files: `run_T33_qc3000000.json`, `run_T15_qc3000000.json`
(T28 yes/no d_meta: `run_T28_qc3000000.json`, still running when this was written; the tool's value is +2.06 pp).

### 2.4 Q3: which of these are spec gates?
- **`G6_freeform_slice`: report only.** Spec 6.3: "G6 ... on >= 5,000 QC rows, plus a separate report on the free-form slice"; "C2 runs G6 separately on the free-form slice" (the D1 G8-H note, C2_DATA_SPEC.md line 1355).
  The tool's `program_pass` does not count it (T06 and T26 pass with it listed). Nothing to fix.
- **`overlay`: bars are spec 4.1** (minimal-edit twins 20-25% of rows, complement pairs >= 20% of yes/no rows, non-syntactic >= 30% of pairs, equiv twins 5-10%, relation units <= 3 rows;
  attack and premise-removal shares are report only). It is a pilot gate (every pilot verdict lists it) but is **not named** in spec 6.4's step 5 or step 7 gate lists.
  T23 fails twin_share .2567 > 25% (a non-tool failure: identical on the runner path).
- **`spec_3_0`: bars are spec 3.0** (row <= 2,000 rendered tokens, family mean <= 800, Mode F share, deep share, registers, skins). Same status: a pilot gate, not in the step-7 list;
  `mix_c2.py` re-checks "each new block's mean <= 800" and "new yes/no 45-55%" on the selected rows. T33's mean-token fail was the redraw defect and is gone with the fix.
- Whether overlay / spec_3_0 / candidate-level G10 should bind at 1.5x candidate size or only on the selected 1.0x set (which `c2_select` trims, label-balanced) is an orchestrator ruling.

## 3. Exposure by family (`exposure.json`, `compare_gates.py`)

| family | exposed to the old redraw defect | candidate-level status through the exact runner path |
|---|---|---|
| T33 | yes (2 dead yes/no qforms, 73 skins) | fixed: yes/no .5146, spec_3_0 pass; still fails longest_option_gold_pp (+2.57 fixed, +2.83 runner), G6 (runner +3.88 pp) |
| T25 | yes (yn_claim_dneg dead) | fixed: yes/no .4673. New with the A43 f exclusions: syntactic_negation_share and G11 ch_value wordings (2.4%, 2.2%) fail; longest +2.12 |
| T15 | yes (2 dead qforms) | fixed shows no change; fails longest +2.98, yes_rate .525, G11 ch_outcome wording 2.5%; G6 c_card +3.69 (runner) |
| T26 | yes (yn_dneg_apply dead, 28 skins) | pass in the old tool; re-run after the fix changes its mix, so re-check |
| T32 | yes (yn_dneg_broken dead, 9 skins) | queue job, not yet reported |
| T28 | dead qform never drawn, 18 skins | gold_position (clustered chi-square), G6 yes/no d_meta +2.06 |
| T24, T27 | no dead qform (23 / 10 skins removed) | queue jobs; not reported |
| T01, T06, T31, T30, T23, T12, T07 | no (nothing removed that changes the draw, or no dead qform) | T01 / T23 / T31 / T12 / T07 fail identically through the runner path: generator at fresh seeds |

## 4. What the orchestrator needs to rule
1. **No tool fix can make a fresh-seed draw pass.** Families that fail through the exact runner path (T01, T23, T31, T12, T07, T15, T33, T28) fail by seed variance or by a real near-bar excess
   in the generator. A re-run on new seed bases is a new lottery draw; I did not make them (the queue is still running and the choice is yours). `--seed-bases` is ready.
2. **G10 position / rank chi-square counts clustered rows as independent.** Options (a bar-preserving amendment or a seed re-draw): evaluate the test on distinct (row key, k) cells,
   which restores the stated 1% size; or an exact position schedule in each generator (closed under A44).
3. **G6 choice excess +1.4 pp on average with SD 1.7 pp across seeds (T01).** The pass/fail at 6,000 rows is mostly seed noise around a small real excess; the max over 8 cells adds upward bias.
   A43 (a) fixed the bar at the pilot seed only, so full generation on fresh rows is a second look at a quantity measured with about 1 pp noise.
4. After the Redraw fix, T33 / T25 / T26 / T32 (and T15 for completeness) should be re-generated by the orchestrator (new seed bases via `--seed-bases`) before their Haiku reads, because their candidates
   and task files change; T01 / T23 / T31 / T12 / T07 / T28 candidates do not change with the fix.
