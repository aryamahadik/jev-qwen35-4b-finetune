# T06 fix iteration 3 (A44 a): notes

## Changes (generator only; nothing relabelled, no bar changed)
- `plugin.py`: the yes/no gold is drawn label-first. New `_balance(sampler, block)` (4,096-seed blocks, stateless,
  seed-deterministic error diffusion in seed order): a card's running yes count tracks `_card_rate` (20-80%, antithetic pairs) and
  each question form's running yes count tracks half its rows, so every form is 50% yes. It also gives each row its rank within
  (form, yes). New `T06Plugin._balanced_wording`: the wording is a round-robin over that rank in a seeded wording order, so every
  (form, wording) cell of the base rows is 50% yes (+-1 row). `_target(qform, yes)` takes the drawn label (was `u < rate`).
  Choice forms and complement partners keep the seeded hash pick (complement wording cells stay binomial).
- `G0_SPEC_v4.md` section 3 (one sentence added to the Cards bullet, 189 lines): re-frozen, sha256
  `b06daf413e7d26ea4612be00aa5d377c1156a9bb3d4d2114582308a967eef3d9`, set in `T06Plugin.G0_SHA256` (was `84b81c33...`).
  `G0_SHA256_AUTHORED` (v2 pool pin) unchanged.
- `run_pilot_i3.py`: copy of i2, output `pilot_i3/`; the loader drops wording skins whose id or lexicon form id is in
  `zed_orch/a43f_quarantine.json["T06"]` (13 `yn_double` forms). `pilot_loaders.py` untouched.
- Backups: `_backup_i3/` (plugin.py, G0_SPEC_v4.md, run_pilot_i2.py). No new test file was written (budget).

## Checks
- Tests: `test_plugin.py`, `test_freeze_v2.py`, `test_haiku_author.py`: 126 passed.
- Determinism (PYTHONHASHSEED 1 vs 4242, n=300, no G15): identical, rows `c266459a...dc768`, relations `00b6d76e...8b1f6`.
- Pilot into `pilot_i3/` (1,001 rows / 607 units): G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G7, overlay, spec 3.0 pass.

## gates_after
| gate | value | bar |
|---|---|---|
| G6, 1,000 rows | yes/no best c_card_without_question/gbt 0.5349 (n 516); choice best d_meta/gbt 0.2969 (chance 0.3062) | chance + 2 pp: yes/no cell above the bar, excused by the A43-erratum null below |
| A43 max-null (`A43_NULL_MAX.json`, 200 draws) | yes/no M = 0.0349, p = 0.17; choice M = -0.0093, p = 0.975 | p >= 0.05 excuses: PASS (was M 0.0471, p 0.03) |
| G6, 6,000 rows (`G6_AT_6000.json`) | verdict pass; yes/no max 0.5051 (c_card_without_question/lr, n 3,041, chance 0.5); choice max 0.3214 (a_question/lr, chance 0.3062) | <= chance + 2 pp every view and model: PASS |
| G7 (1,000 / 6,000) | pass / pass | 0 fails |
| G10 | `double_negation_share` 0.0 fails: waived by A44 (b) (the 13 quarantined forms were the only double-negation shape). `yes_rate_cells` fails at 6,000 rows: 37 cells with n >= 50, many outside 50 +- 2 pp (yes 0.44-0.58, n 56-71). Other checks pass. | yes_rate_cells report-only (selection quotas enforce) |
| G3-H, G5-H | task files in `pilot_i3/g3h`, `g5h`, NOT answered | pending (orchestrator runs Haiku) |

## Open items
- The wording cells still deviate from 50%: complement partners keep the hash wording pick, and units dropped by gates
  (`drops_outside_gates` ctx 4, render 19) and the unit/twin mix change the cell counts. Base rows alone are balanced by construction.
- The 6,000-row run (`G6_AT_6000.json`) used the in-memory run with `--no-g15`; seconds 757.
- G5-H / G3-H answers from `pilot_i2` are not carried over: the gold labels and wordings of yes/no rows changed.
- Commands: pilot `python -B families/T06/run_pilot_i3.py`; G6 `... --dry-run --n 6000 --no-g15 --g6-json families/T06/pilot_i3/G6_AT_6000.json`;
  null `python -B zed_orch/g6_null_max.py --family T06 --runner families/T06/run_pilot_i3.py --dir pilot_i3 --draws 200`.
