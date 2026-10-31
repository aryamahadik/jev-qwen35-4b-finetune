# T36 A45 c final iteration (pass 2): FIX NOTES (not closed: G6 choice FAILS at 6,000 rows)

State of plugin.py: identical to the A45 pass-1 state (the pass-1 yes/no wording change kept). My option-value redesign was
tested and REVERTED (it did not lower the leak and broke G7). The attempt is kept for the record, not imported:
`_backup_a45b/plugin_i2_attempt_symmetric_pool.py`. Baseline copy: `_backup_a45b/plugin.py`, `G0_SPEC.md`.

## What was tried (by construction, no relabel, no bar change), all measured on 3,000-row in-memory builds and then 6,000 rows
1. Symmetric pool neighbours (both sides of each bound at major / minor / patch; free numbers in the range's own magnitude
   bucket: `_fw` bucket-consistent, `_up`), t36_listed_0..6 error models (every listed version a candidate), side + level
   coin for the outside versions of a choice listing (`_take_sided`, shares 40/50/10 major/minor/patch, same both sides), and
   `_balanced_wrong`: the wrong options are the set (rank quota of the plan kept) whose signs gold-vs-wrong cancel per
   component (major, minor, last, bucket); lower wrongs sharing the gold's major+minor excluded.
2. Result on the signs (3-number versions, 3,000 rows): lower-wrong-sharing-M.m (gold larger on the last number only) went from
   14% of wrong options to 0; gold>wrong on the major 1.4% -> 15.6% (vs 28% below); last number >/< 50.5/35.5% -> 42/33%.
   Not symmetric (the range forces every higher wrong option to differ at major/minor).
3. G6 at 6,000 rows with it: choice b_options/lr 0.3489 (baseline 0.3362; bar 0.3123; SD of a cell ~0.009: no gain) and G7
   FAILED on the option token "1" (318 gold hits vs 391.5 expected, p 3e-7). Dropping the last-number bucket match was worse
   (b_options/lr 0.3535, gold has the larger last number 57% vs 34%). So the bucket match stays.
4. Reading: the leak is not the sign of the comparison but the marginal of the numbers (small numbers 1, 2, 3 are wrong
   options more often than gold; gold's numbers come from the range's conditional distribution). Per-token lifts are each
   |z| <= 2 (t1 34.6% gold vs 39.7% expected; m1 27%), the LR sums them. Equal signs do not equalise the marginals.

## Yes/no wording change (pass 1, "untested"): TESTED
Stratified negative wording (plugin.py ~line 932). 6,000 rows: yes/no G6 max 0.5163 (a_question/lr; bar 0.52) PASS (before
the edit 0.5109); G7 pass; G10 yes_is_bad / yes_rate pass; G10 fails only `yes_rate_cells` (9 of the 12 cells with n >= 50 lie
outside 50 +/- 2 pp at n 50-65: binomial noise of that bar, same fail before the edit) and `double_negation_share` 0.0 (no
admitted yn_double wording: known, G0 section 3). Family tests: 132 passed (test_plugin, test_pilot_i1, test_g0_v2).

## Gates of the delivered pilot_i2 (plugin = pass-1 state) vs bars
| gate | value | bar | pass |
| G6 yes/no @6,000 | max 0.5163 | <= 0.52 | yes |
| G6 choice @6,000 | b_options/lr 0.3362 (a 0.323, c 0.3341, d 0.3206 all lr) | <= 0.3123 | NO |
| G6 @1,000 pilot | yes/no a_question/lr 0.5312 (n 529) | <= 0.52 | cell above bar: null-max started with --workers 3 but too slow (9 of 200 draws in 18 min; ~9 h), killed, NOT completed; the same cell is 0.5163 at 6,000 rows (pass) |
| G7 @6,000 / pilot | pass / pass | 0 fails | yes |
| G10 | fail: yes_rate_cells, double_negation_share (both as before) | | no |
| G2 G3 G4 G-SL G-LEX G-TW G15 schema options overlay spec_3_0 | pass | | yes |
| determinism | rows_sha256 31925e74... identical under PYTHONHASHSEED 1, 2 and the written run | identical | yes |

## Next lever (not done: needs a frozen table, ~1 more pass)
Adversarial option selection by construction: from a frozen gold-vs-wrong log-odds table of the option numbers (major, minor,
patch value tokens, estimated once on a previous build and stored in the family folder), pick among the plan-feasible wrong
sets the one whose summed score is closest to the gold's (the wrong options look as gold-like as the gold), keeping the rank
quota and the kind / length / bucket match. Pool symmetry (this pass) is a prerequisite and is in the attempt file.

## Files / commands
- Pilot: `run_pilot_i2.py` -> `pilot_i2/` (rows.jsonl, relations.jsonl, PILOT_REPORT.json, G6_AT_6000.json).
- G5-H task files (written, not answered): `pilot_i2/g5h/tasks/`, key `pilot_i2/g5h/key.json`, manifest `pilot_i2/g5h/manifest.json`.
- G3-H task files (written, not answered): `pilot_i2/g3h/tasks/`, key and manifest in `pilot_i2/g3h/`.
- Score after Haiku answers exist: `cd lean/c2_build && ../../.venv/bin/python -B pilot.py score T36` (answers into g5h/answers, g3h/answers;
  pilot.py main(); `pilot.score_family` reads pilot/ by default: point it at pilot_i2 the way score_i1.py (zed_orch) does for i1).
- Determinism: `PYTHONHASHSEED=1 ../../.venv/bin/python -B transfer/T36/run_pilot_i2.py --dry-run` (and 2): same rows_sha256.
- G6 at 6,000: `../../.venv/bin/python -B zed_orch/g6_at_size.py T36 --n 6000 --dir pilot_i2`.
- Null-max: `../../.venv/bin/python -B zed_orch/g6_null_max.py --family T36 --runner transfer/T36/run_pilot_i2.py --dir pilot_i2 --workers 3`.
