# T20 pilot_i3 (A45 c, one final iteration) - FIX_NOTES

Backups: transfer/T20/_backup_a45b/ (plugin.py, solver_b.py, G0_SPEC.md, run_pilot_i2.py, test_*.py, fixtures.py). Runner: run_pilot_i3.py. Older pilot folders kept (pilot, pilot_i1, pilot_i2). pilot_i2/FIX_NOTES.md lists what the previous agent did (not redone).

## Cause (pilot_i2: G6 choice c_card_without_question lr 0.3097 vs 0.27)
The record's own tokens named the level: "exposed: yes" meant SEV1 on every card, and each urgency word was a fixed column of tables that were monotone in the SAME urgency order on every card (cosmetic -> SEV3/4, outage -> SEV1/2).

## Fix (generator, template and solver-B reader only; no label, bar or G6 view changed; G0 v4, sha256 93d9770a...c9c31)
- R4 per-card urgency order: MATRICES = 4 monotone base tables x the 6 orders of the urgency columns (24 tables). A wider band is never less severe on any card; the same urgency word maps to a different severity on different cards (each word has the same mean level and level distribution over the 24 cards). The table is drawn stratified inside the class (plan.mx), so it is label-blind.
- R8 per-card exposure rule: "If customer data was exposed[ with wide impact]: SEV1 | SEV2 or more severe | one level more severe." (2 conditions x 3 effects = 6 rules, plugin.XRULES; step applied last as before; a failed condition does nothing). "exposed: yes" is planned on exactly 1 in 8 bases of EVERY class (choice SEV1..SEV4; yes/no form x outcome; plugin._ex_set), the rule of such a row is drawn among those the class can hold (plugin._x_feasible), exposed-yes bases ask for no twin and are never a depth-3 trap base. Exposure is no longer a scenario (weight 0). Program gold stays exact: solver A applies the rule from the card's structure; _sev_c (construction reading) applies it too.
- R20: the exposure step counts toward depth only when exposed is yes AND its condition holds.
- Card text: steps are unnumbered (keeps mean tokens under 800 with the longer exposure line: 788.2). Step 3 wording unchanged.
- Solver B (independent, imports no solver-A code): reads the exposure rule from the printed card with its own regex, applies it in the clock walk's last step. Parsed fact "xrule" = [condition, effect] must equal the generator's (G3).
- G0_SPEC.md v4 (section 11 + R4, R8, 1.1, section 2), 199 lines (kit limit 200). G0_SHA256 updated in plugin.py.

## Gates after (pilot_i3, 1,000 rows, rows sha256 e04ccaa7...f02c8, relations 0bec23dc...c1c83; identical under PYTHONHASHSEED 3, 7, 11)
| Gate | Value | Bar | Result |
|---|---|---|---|
| G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, overlay | 0/542 units failed | 100% | PASS |
| G6 at 6,001 rows (zed_orch/g6_at_size.py T20 --n 6000 --dir pilot_i3) | choice max 0.2636 (a_question lr; c_card_without_question now below it; was 0.3097); yes/no max 0.5091 (d_meta lr) | chance + 2 pp = 0.27 / 0.52, every view and model | PASS |
| G6 at 1,000 rows (pilot cell) | yes/no c_card_without_question lr 0.5273 (> 0.52) | chance + 2 pp | cell above the bar: A43 erratum null-max below |
| G6 null-max (A43 erratum; zed_orch/g6_null_max.py --workers 3), yes/no M = +0.0273 | PARTIAL: 171 of 200 draws, p = 0.398 (68 null draws >= observed; median null 0.0235, q95 0.050); choice M = -0.024 (below chance) | p >= 0.05 | passes on the partial; full 200-draw file NOT written (run starved at load avg 40): rerun the command below (about 15 min on an idle machine). Partial: pilot_i3/A43_NULL_MAX_PARTIAL.json |
| G7 | 0 fails of 653 features (6,001 rows: pass) | 0 at Bonferroni | PASS |
| G10 (1,000 rows) | pass; at 6,001 only yes_rate_cells fails (report-only, unchanged from pilot_i2) | | PASS / report |
| spec 3.0 | mean tokens 788.2, max 1028, deep share 0.012, twin share 0.218 | 800 / 2000 / 10% | PASS |
| Double negation share | 0.0358 | 2% floor (waived by A44 b / A45 a only if short; here above) | PASS |
Tests: test_plugin.py + test_fix_i1.py + test_fix_i3.py (new: urgency symmetry, exposed-yes rate per class, rule printed and read back, rule effects and conditions) + test_haiku_author.py: 88 pass. test_fix_i1/test_plugin edited by construction: matrices are monotone in rows and in a per-card column order; EXPOSED twin kind count >= 1; steps unnumbered.

## Haiku step (not run here; the orchestrator runs Haiku)
G3-H tasks (3 files, extraction of team and reporter): transfer/T20/pilot_i3/g3h/tasks/T20-extract_g3h-e9e931c2-00{0,1,2}.md ; manifest g3h/manifest.json ; answers go to g3h/answers/.
G5-H tasks (2 readers x 2 files, 100 items each reader; 12+ yn_double_neg rows first): transfer/T20/pilot_i3/g5h/tasks/T20-blind_read-6bc933e5-00{0,1}.md (reader A) and T20-blind_read-7a308f25-00{0,1}.md (reader B) ; manifest g5h/manifest.json ; answers go to g5h/answers/. No answer was written.

## Commands
cd lean/c2_build
PYTHONHASHSEED=3 ../../.venv/bin/python -B transfer/T20/run_pilot_i3.py                       # wrote pilot_i3/
PYTHONHASHSEED=7 ../../.venv/bin/python -B transfer/T20/run_pilot_i3.py --dry-run --no-g15    # determinism (also 11): same rows sha256
../../.venv/bin/python -B zed_orch/g6_at_size.py T20 --n 6000 --dir pilot_i3
../../.venv/bin/python -B zed_orch/g6_null_max.py --family T20 --runner transfer/T20/run_pilot_i3.py --dir pilot_i3 --workers 3
../../.venv/bin/python -B zed_orch/score_i1.py T20 --dir pilot_i3          # scoring command, after Haiku answers G3-H / G5-H exist
