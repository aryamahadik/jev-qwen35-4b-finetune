# T36 final pass (w5, 15 Oct 2026): FIX NOTES. NOT CLOSED: G6 choice fails on the pilot seed base

Backups: `_backup_w5/` (plugin.py, G0_SPEC.md, run_pilot_i2.py, pilot_i2_before/). Work files: `_w5/`.

## The lever as run (a construction rule fixed before measurement)
Choosing wrong options among the error-model outputs has no freedom: on 9,000 build rows 80% of the wrong picks are forced (candidates ==
quota; `_w5/plugin_selection_attempt_forced_picks.py` is that first version, not imported). So the frozen table acts on the STRUCTURE the
sampler keeps (sample(): a ch_pick structure that reaches the seed's plan is kept with chance min(1, exp(score - accept_c)), else drawn
again; plan, gold, k, position, rank unchanged; gold stays program gold; nothing relabelled).
- score = sum_f w_f r_f, r_f = [gold shows f] - m_f/k over the option features f (number tokens, adjacent-number pairs, major / minor /
  patch values): a row's contribution to the G7 count condition. The table is the max-entropy tilt that zeroes the mean of every r_f.
- Table `option_table.json`, sha256 `21d5121ed80802b07dc9823759b6143c451996ceaf46b2aebac952e03c1ab1a5` (checked on load; constant
  `TILT_SHA256` in plugin.py), 698 weights, accept_c 0.5753, mean acceptance 0.50. Fitted ONCE with `fit_option_table.py` on build seed
  base 3,000,000 (9,600 choice seeds x 8 proposals). Held-out check on build base 4,000,000 (3,600 seeds): mean z^2 of the accepted
  feature means 1.69 -> 0.26 (1.0 = noise). No G6 / G7 measurement seed was used to fit; nothing was tuned after the table was frozen.

## Measured (6,000 rows, G15 off, `g6_seedbase.py`; bars: chance + 2 pp)
| seed base | choice b_options/lr | choice max cell | yes/no max | G7 | G6 |
|---|---|---|---|---|---|
| 900,000 (pilot) | 0.2971 (was 0.3362) | c_card_without_question/lr 0.3235 vs 0.3123 FAIL | 0.5048 (bar 0.52) | pass | FAIL |
| 7,000,000 (fresh dev) | 0.3009 | c_card_without_question/lr 0.3099 vs 0.3119 | 0.5147 | pass | pass |
The b_options leak that was the open item is closed on both bases. The residual is the c view (card without question): its excess comes
from the option-token x card-token cross features (build base 3,000,000, 2,870 rows: full 0.3209, without the cross features 0.3003,
only the cross features 0.3209; `_w5/diag_ablate.py`). Per-pair z-scores of those crosses show no single driver (max |z| 4.4 over 6,900
pairs, mean z^2 1.42): a diffuse relation between the option numbers and the card. The table cannot reach it (it sees the option only).
A fix that passes on one seed base only is not a fix: T36 fails G6 choice (pilot base 0.3235 vs 0.3123).

## pilot_i2 re-run (1,000 rows) and checks
G2 G3 G4 G-SL G-LEX G-TW G15 schema options overlay spec_3_0 G7 pass. G6 fail: yes/no a_question/lr 0.5312 (n 529, unchanged rows);
choice best 0.2791. G10 fail: double_negation_share 0.0 (waived A44 b / A45 a); yes_rate_cells at 6,000 rows (binomial noise, as before).
Determinism: rows_sha256 b65db3c5... identical under PYTHONHASHSEED 1, 2 and the written run. Family tests: 132 passed.
G5-H / G3-H task files rewritten (4 tasks each; not answered): `pilot_i2/g5h/`, `pilot_i2/g3h/`.
The 1,000-row yes/no cell a_question/lr 0.5312 (n 529): A43 erratum max-statistic null, 200 draws on od-l4b (VM left running): observed M 0.0312, null median 0.0217, p 0.25 (50 of 200 null M >= observed), so the cell is excused; pilot choice M -0.0127, p 0.995. File `pilot_i2/A43_NULL_MAX.json`.
