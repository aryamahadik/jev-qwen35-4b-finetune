# T24 fix iteration 2: notes

## Cause
Iteration 1 failed G6 at 6,000 rows on choice / c_card_without_question / lr (0.4531, bar 0.4384, chance 0.4184).
The option count k came out of the structure (a condition clause in V1 or V2) and the gold role from a fitted
weight table (OUT2_WEIGHTS). Roles were only approximately 1/k inside each k and drifted by window, so the options
(role-readable outcome names) carried a role prior.

## Changes (generator only; no relabel, no feature dropped, no bar touched)
- `plugin.py` `CELLS`: (k, gold role) is ONE draw from the seed before any structure (5th low-discrepancy dimension,
  `_weyl(..., 4)`): k=2 pos/neg 1/4 each, k=3 pos/alt/neg 1/6 each. Not a hash-block permutation: ch_v2 rows are a
  subsequence of the seeds (qform is dealt on the same seeds) and a block deal would not stay exact there.
- `_edit_joint` / `_pick_edit`: (edit kind, case mode) is drawn given materiality and the dealt (k, role). The joint is
  fitted by iterative proportional fitting so the role marginal is exactly 1/k and the (kind, mode) marginal is the G0
  plan table (alt edits live on k=3 at twice their share). Support: masked -> NEG; a flipping alt edit moves POS<->ALT;
  an untouched alt edit never reaches ALT. P(change | role) stays ~0.5 for every role (hit is independent of role).
- `_docs` / `_construct`: the condition clause is present iff k=3 (a dealt ALT needs it in V2). The dealt role is never
  dropped (the old "drop the V2 target on the last quarter of draws" is gone for ch_v2): 0 sample failures on 3,000 seeds.
  yes/no rows keep the old code path.
- `render` / `_option_order`: option order uses kit `plan_choice(key, closed=k)`'s planned position for the DEALT role
  (a function of the seed). A base row's gold is at the planned position (uniform in each k). G-TW needs twins to show
  the base's option list in the same order, so the order cannot follow the gold; a twin's gold sits where its role
  falls in that order. `build_closed(order="fixed")`, no plan meta.
- Option text unchanged: the options are the pack's outcome names (frozen pool). The kit's `length_balance` exists
  for open sets only, so it is not used. Role words and lengths are not equalised; role cues stop carrying
  information because every role is gold at 1/k in each k (G10 gold-is-longest/length still passes).
- `G0_SPEC.md`: Draw-order paragraph gets one line for the ch_v2 deal (200 lines, the cap); sha re-frozen to
  `04f3cfbe29d55f24cf8dadd59cbb8277db5e9387398784e39f4e02f8a6fc83af` in `plugin.py` (test_plugin checks it live).
- Tests: `test_balance.py` +3 (cell shares within 2 pp, `_edit_joint` marginals, planned position + k), `test_plugin.py`
  folder whitelist. `run_pilot_i2.py` -> `pilot_i2/`. Backups in `_backup_i2/`.

## Results
Tests: 48 passed (`pytest families/T24 --ignore=families/T24/_backup_i2`; the whitelist test was fixed and re-run alone).
Determinism: rows_sha256 f41844c5e0109522..., relations_sha256 99fb5835ecdf2254... identical under PYTHONHASHSEED 1, 5, 777.
Pilot (1,000 rows): PASS (pending G3-H, G5-H). Task files: `pilot_i2/g5h/tasks`, `pilot_i2/g3h/tasks` (not answered).

gates_after, G6 at 6,000 rows (`pilot_i2/G6_AT_6000.json`; bar = chance + 2 pp):
| cell | before (i1) | after (i2) | bar |
|---|---|---|---|
| choice max (n 2,962 / 2,956) | 0.4531 c_card_without_question lr | 0.4283 c_card_without_question gbt | 0.4384 / 0.4347 |
| yes/no max (n 3,040 / 3,044) | 0.5099 a_question lr | 0.5066 c_card_without_question gbt | 0.52 |
G6 pass, G7 pass, G10 pass (yes_rate_cells report-only).

1,000-row pilot choice cells (chance 0.417 -> 0.4136), before -> after:
a_question 0.4268/0.4553 -> 0.4207/0.3902; b_options 0.4715/0.4512 -> 0.3963/0.3821;
c_card 0.4268/0.4512 -> 0.4085/0.3821; d_meta 0.4309/0.4248 -> 0.3699/0.3963 (lr/gbt). Pilot G6 verdict fail -> pass.

## Open
G3-H / G5-H re-reads (Haiku) on the regenerated task files. Not a G0 target change: the ch_v2 role/k rule is stated
in G0 (Draw order) but G0's earlier "Balance" text already required roles uniform within each k.
