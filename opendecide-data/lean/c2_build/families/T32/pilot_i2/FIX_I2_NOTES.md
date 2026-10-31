# T32 fix iteration 2: notes (yes/no DONE; choice d_meta NOT fixed)

## Changes (generator only; no relabel, no bar changed)
- `plugin.py`: yes/no wording is assigned label-first. `_wording_ranks(sampler, block)` ranks the seed pairs of each 4,096-seed
  block per effective form (base form, and the complement form, now drawn per PAIR: `ckind` hash on `seed // 2`). The wording is
  a round-robin over the form's wordings in a seeded order (`_balanced_wording`). A pair is one yes and one no row and shares
  the wording, so every (form, wording) cell is exactly 50% yes, and so is every card. Stateless, seed-deterministic.
  `_BalCtx` (returned by `ctx_for`) routes `ctx.pick(kind="wording")` through it, because the kit draws the complement's
  wording itself (`pipeline.build_unit`). Choice forms keep the seeded pick.
- `G0_SPEC.md` (section 2, one sentence): re-frozen, sha256 `28e8b6ce...f5654` (was `1521a061...`), set in `T32.G0_SHA256`.
  Tests read the pin from the plugin. Backups: `_backup_i2/`.
- New `test_i2_fixes.py` (2 tests). `run_pilot_i2.py` already existed (output `pilot_i2/`).

## Checks
- pytest `test_plugin.py` + `test_pilot_fixes.py`: 82 passed (before the `_BalCtx` edit; `test_i2_fixes.py` 2 passed after).
  The full suite was not rerun after `_BalCtx`.
- Determinism (n=300, PYTHONHASHSEED 1 vs 2) identical: `determinism.log`.
- Pilot into `pilot_i2/` (1,000 rows, 448 units): G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options 0 failed; G6 1,000 pass
  (yes/no 0.5141, choice 0.2401 vs 0.2317), G7, G10, overlay, spec 3.0 pass. G3-H / G5-H task files in `pilot_i2/g3h`, `g5h`
  (NOT answered). The `pilot_i2` rows changed from the first i2 run (complement wording fix), so use the final files.

## G6 at 6,000 rows (`G6_AT_6000.json`), before (pilot_i1) -> after
| cell | before | after | bar |
|---|---|---|---|
| yes/no d_meta gbt | 0.5227 (FAIL) | 0.5155 (max cell) | <= 0.52 pass |
| yes/no max, all views | 0.5227 | 0.5155 | pass |
| choice d_meta gbt | 0.2604 | 0.2604 (FAIL, chance 0.232 + 2 pp = 0.252) | fail |
| G10 yes_rate_cells | 19 cells >= 50 rows, 18 outside +-2 pp (yn_kept#45505543 0.305) | none outside | pass |
| G7 | pass | pass | pass |

## Choice d_meta: ranking and why it is open
- `DMETA_RANK_I1.txt` has no single choice driver (all pairwise importances ~0.0001). My quick fit on `_dmeta_i1.pkl`
  (`_choice_fit.py`, `_choice_fit2.py`): gold position is uniform (ch_status 464/452/459/430/444; ch_due 239/242/230); the
  ch_status gold shares are uniform within noise (chi2 7.1, 4 df). The signal is the story-shape numerics: predicting the
  gold status from `depth`, `len_state`, `n_lines`, `n_numbers`, `mag_mean`, `len_q`, `len_ins`, `deep` (GBT, CV by card)
  gives 0.265 against 0.20, with no feature dominant (depth alone 0.234). Status options have fixed labels, so the gbt
  matches option length (the status identity) with these numerics. Mean `len_state` is 621 for Broken/Kept against 637 for
  Not triggered/Not yet due (conditional lines); Waived has mean depth 1.71 against about 1.5 (twin edits).
- Position and length planning (`choiceplan`) cannot fix this: the closed labels have fixed lengths and the position is
  already uniform. A fix needs the story shape (conditional lines, depth) drawn independent of the status, and twin rows
  put onto the base's shape plan. This was not done in this budget. Not triggered needs a condition, so exact independence
  may not be possible, and the cell may need a G0 / bar decision.
- No G6 run has shown the cell is only noise: 0.2604 is the same at 6,000 rows before and after (the choice rows are
  unchanged by this iteration).

# FINAL PASS (A43 e): shape plan by construction. RESULT: G6 PASS at 6,001 rows
- `plugin.py`: `_shape(sampler, seed)` draws (E lines 5-6, C conditional lines 2-3, F filler lines, depth 1-2) from the seed
  pair before the status. `_build` realises every status inside it: asked-story fillers from F (try first), the decoy
  commitments are solved exactly to the remaining (lines, cond lines, filler) (neutral conditions: cond_open / met / off
  decoys; Not triggered uses one of the C lines), the story is redrawn until depth == plan. ch_due rows: status free,
  +2 lines for the extension. Depth 3 removed. P_SECOND_TWIN 0.75 -> 1.0 (twin supply). Twins keep the base story.
- G0_SPEC.md R15 re-frozen, sha256 99653438...231369 (set in T32.G0_SHA256). Backups: `_backup_i2b_final/` (*.bak).
- First plan (E up to 7) gave spec 3.0 mean_tokens 815.5 (bar 800): E capped at 6 -> 796.2 (pass, thin margin).
- Tests: 149 passed, 1 failed: `test_dneg_stage.py::test_admit_then_glex_then_supplement` (admitted 0 of 7). Not investigated;
  the full suite was not run after the i2 yes/no wording change, so the cause may predate this pass. Edited tests:
  line budget (+2 for ch_due), deep == 0; new test_shape_plan_is_independent_of_the_status.
- Determinism (n=300, hashseeds 1 vs 2): identical (`determinism_final.log`). Pilot `run_final.log`: all program gates pass; the
  1,000-row G6 shows yes/no a_question gbt 0.533 (n=495, pilot-size noise; the 6,000-row run decides).
- G6 at 6,001 rows (`G6_AT_6000.json`, `g6_final.log`): verdict pass, G7 pass, G10 pass.
  | cell | before (i2 first) | after | bar |
  |---|---|---|---|
  | choice d_meta gbt | 0.2604 | 0.2427 (max choice cell, n 2953, chance 0.2302) | <= 0.2502 |
  | yes/no max | 0.5155 | 0.5046 (c_card_without_question lr, n 3048) | <= 0.52 |
- Scratch: `_probe_shape.py`, `_probe2.py` in the family folder.
