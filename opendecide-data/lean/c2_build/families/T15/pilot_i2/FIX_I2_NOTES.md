# T15 fix iteration 2 (A43 b): depth by construction

## Changes (generator/template only; no relabel, no feature dropped, no bar loosened)
- `plugin.py`: `deep` is now a property of the card drawn from the seed before the target: `structure["deep"]` = a 4-gate card
  (gates) or a 4-person cascade (claimants); `derive()` reads it and never recomputes it from the answer (old structures
  without the key keep the old rule). `depth` stays 2/3 in meta and in G6's metadata view.
  The old deep (decision reached at gate D / third tie-breaker decides) was gold-associated: on a 4-gate card only
  eligible and fail D were deep; a third tie-breaker deciding excluded "nobody".
- `GATE_COUNTS` 2/3/4 = 37/55/8% (was 35/45/20); `PEOPLE_COUNTS` = 30/62/8% (was 30/45/25). Deep rows 8.3% at 6,000 rows
  (limit 10%). Gold within each depth class: unchanged label-first targets (`OUTCOME_ELIGIBLE`/`OUTCOME_W` per gate count,
  `claim_plan` via kit choiceplan; k is drawn before the target), so every label has its normal share in the deep class too
  (new test `test_deep_is_drawn_from_the_seed_not_from_the_answer`).
- Structure check (2,500 seeds x 4 samplers, chi-square within gate count): route listed / skipped-gate count are label-independent
  (p 0.17 to 0.58). Gate count, route, cascade length and line counts do not depend on the gold.
- c-view cue search on the 6,000-row build (per question form): no generalising lexical cue remains. The c LR top weights are
  option-token x number/name memorisation pairs; the d_meta gbt importances are k, clen, deep (= k 4).
- `G0_SPEC.md` v1.4 (S3, S8, S23, Depth line), sha re-frozen in `plugin.py`: a18013761c40b4c417a5d92090180f63501daf5fc46fa7e13d4567c6390a5aff.
  Backups in `_backup_i2/`. `test_plugin.py`: one new test. `run_pilot_i2.py` writes `pilot_i2/`.

## Gates
G6 at 6,000 rows, choice part (chance, bar = chance + 2 pp):
| cell | before (i1, n 3113, chance .3272, bar .3472) | after (i2, n 3102, chance .3316, bar .3516) |
|---|---|---|
| c_card_without_question lr | **0.3611 fail** | 0.3504 pass |
| d_meta gbt | **0.3723 fail** | 0.3366 pass |
| a_question lr / gbt | n/a | 0.3198 / 0.3333 |
| b_options lr / gbt | n/a | 0.3333 / 0.3343 |
| c gbt; d_meta lr | n/a | 0.3317; 0.3295 |
Yes/no max: 0.518 (d_meta gbt, i1) -> 0.5138 (a_question gbt, i2), bar 0.52. G7 pass; G10 yes_rate_cells fails (report only).
The margin of c lr is 0.1 pp.
Pilot (1,000 rows): G6 shows b_options gbt 0.3629 and c gbt 0.3554 above the 1,000-row bar; the permuted-gold null at this size
(20 draws, `work_i2/g6_null.py`) has sd 2.3 pp and max 4.9 to 5.1 pp, so both are within the null. All other pilot gates pass.
Determinism: rows sha d0dbab76... / relations 953649ec... identical under PYTHONHASHSEED 1 and 777 (400 rows, --no-g15).
Tests: 133 passed before the new test; the new test passes. G5-H task files regenerated in `pilot_i2/g5h/`; G3-H n/a (no Mode F rows).
Scratch: `work_i2/` (an.py, strc.py, g6_null.py, logs).
