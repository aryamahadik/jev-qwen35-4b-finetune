# T20 pilot_i2 (A45 c) - FIX_NOTES

Backups: transfer/T20/_backup_a45/ (plugin.py, G0_SPEC.md, run_pilot_i1.py, test_fix_i1.py). Runner: run_pilot_i2.py.

## Changes (plugin.py, generator only; no label, bar or G6 feature touched)
- plan_of: depth, matrix index and "window printed" are now drawn per class (label x question form) with strat(), so they no longer follow the answer (Plan fields depth, mx, mw; _nuisance()).
  Feasible depths were measured per class: without a printed window every class can only fire depth 1; with one, depth 1-2 (S4 +1 for its two offsets). Depth 3+ needs two of critical/exposure/escalation, each of which rules out SEV4 / "not reaches", so it would name the answer. Window printed on 7 of 10 bases. A small fixed share (1 in 12 windowed bases of a reaching class) keeps the depth-3 order trap (order_matters, G2 error model t20_floor_first).
- sample(): scenario redrawn each try among those that can give the answer (_scenario); planned depth/matrix/window enforced by rejection; matrix freed after 1/4 of the tries, depth after 1/2 (rare).
- twin_choice: prefers an edit that keeps the base's ops depth (depth_of()), falls back to any edit.
- Card: already printed once in pilot_i1 (instructions for choice, row.card for yes/no; 0 rows with a duplicate "Impact:" line). No change needed.

## Gates after (pilot_i2, 1,000 rows, rows sha256 e5c816a4...c9e30ff1c9e9fe8, same under PYTHONHASHSEED 3 and 11)
All program gates pass; G3-H / G5-H pending (Haiku). Double negation share 0.0358 (waived A44 b / A45 a if short).
Tests: test_fix_i1.py + test_plugin.py 56 pass (test_balance_and_traps passes with the order trap kept).
G6 at 6,001 rows: yes/no best d_meta/gbt 0.5139 vs 0.52 PASS (was 0.5878); choice d_meta now within bar (was 0.3478).
**FAIL: choice c_card_without_question / lr 0.3097 vs 0.27 (was 0.3258).**
G10 yes_rate_cells: report-only, unchanged.

## Open: choice c_card_without_question
LR coefficients (3,500-row diagnostic, _diag/lr.py): "exposed: yes" (-> SEV1, 2.9) and the urgency token ("reported cosmetic" -> SEV4 3.6-4.2, "reported outage" -> SEV1/2). Both are the record's own inputs. Tried planning urgency per class and cutting exposure weight 0.09 -> 0.03: accuracy barely moved (train acc 0.76 -> 0.745), reverted (not verified at 6,000). SEV4 needs cosmetic (or a window) in every monotone matrix, and exposure forces SEV1, so a fix needs a design change to what the record prints (e.g. urgency not a card-rule input, or decoy exposure/urgency wording) - an owner/design call; not done.
Next steps if continued: run the max-statistic null (zed_orch/g6_null_max.py) on the 1,000-row cell.

## Commands
cd lean/c2_build
../../.venv/bin/python -B transfer/T20/run_pilot_i2.py            # wrote pilot_i2/
../../.venv/bin/python -B zed_orch/g6_at_size.py T20 --n 6000 --dir pilot_i2
../../.venv/bin/python -B zed_orch/score_i1.py T20 --dir pilot_i2   # after Haiku answers G3-H / G5-H
