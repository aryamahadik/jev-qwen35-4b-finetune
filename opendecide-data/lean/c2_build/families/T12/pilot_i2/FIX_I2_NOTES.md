# T12 fix iteration 2 (the last): notes

## Change (generator only; nothing relabelled, no bar changed)
- `plugin.py`: the yes label of a yes/no base row is no longer an independent per-row Bernoulli draw
  (`uhash(FAMILY, "yes", ...) < _rate`). New `_yes_table(samplers, b0)` (+ `_card_idx_of`, `T12Plugin._yes_of`) draws it
  label-first, stratified by (question form, card): stateless error diffusion over the seeds of each 4,096-seed block in
  (seed, sampler) order. A card's running yes count tracks r (n + 1); each (form, sampler) running yes count tracks half its
  rows. Every form's yes rate is 50% (+- 1 row per run) whatever the card mix; card rates stay inside 20-80%
  (measured 0.244-0.757). Complements keep the opposite yes of their balanced base, twins unchanged. `_rate` is now cached.
- `G0_SPEC_v2_2.md`: R20 and the section 7 F4 note updated (no line added, 200-line cap holds). Re-frozen:
  sha256 `65892dd9a9561c20ca8c418353eb4f3f01094160c527e942fdfeff16f6e482c6` (was `da876f58...`), set in `T12Plugin.G0_SHA256`;
  `test_the_g0_pages_are_pinned` reads the pin from the plugin and passes. `G0_SPEC.md` (v2.1, authored sha) untouched.
- Backups: `_backup_i2/` (plugin.py, G0_SPEC.md, G0_SPEC_v2_2.md, run_pilot_i1.py).
- New: `run_pilot_i2.py` (copy of i1, output `pilot_i2/`), `test_i2_fixes.py` (form yes rate 50 +- 1.5 pp, card rates in
  20-80%, stateless).

## Checks
- Tests: `test_i2_fixes.py`, `test_i1_fixes.py`, `test_plugin.py`, `test_authoring.py`, `test_freeze_v2.py`: 99 passed (+ the
  new tests), with ONE test deselected, see below.
- Determinism (PYTHONHASHSEED 1 vs 4242): identical. rows sha256 `a7f776ce...8042`, relations `24a3732b...3874`,
  task files `4841196c...2cf4` (`determinism.json`).
- Pilot: 1,001 rows / 552 units, `pilot_i2/PILOT_REPORT.json`; G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options 0/552 failed.

## gates_after
| gate | value | bar |
|---|---|---|
| G6, 1,000 rows | yes/no best c_card_without_question/lr 0.5107; choice best d_meta/gbt 0.2828 (chance 0.2854) | chance + 2 pp: pass |
| G6, 6,000 rows (A43) | yes/no max 0.5000 (b_options/lr; n 3,090, chance 0.5) (was 0.5223 lr / 0.5207 gbt); choice max 0.2969 d_meta/lr (chance 0.2853) | <= chance + 2 pp, every view and model: PASS, `G6_fails` = [] |
| G7, 1,000 / 6,000 rows | 989 features, 0 fails / pass | 0 fails: pass |
| G10, 1,000 rows | yes_rate 0.4893, yes_no_share 0.5125, yes_is_bad 0.5361, all pass | spec 3.0 / 6.3: pass |
| G10 yes_rate_cells, 6,000 rows | report only: 9 of 13 cells with n >= 50 are outside 50 +- 2 pp, all yn_release wordings, yes 0.389-0.560, n 50-59; no small cell with binomial p < 0.01 | report-only (selection quotas enforce); this makes the script's `G10_verdict` read "fail" |
| overlay / spec 3.0 | complement 0.4639, non-syntactic 0.6471, twins 0.2308, equiv 0.0649; max_tokens 1187, mean 756.0 | pass |
| G3-H, G5-H | task files regenerated, NOT answered (orchestrator runs Haiku): `pilot_i2/g3h/`, `pilot_i2/g5h/` | pending |

## Open items
- The yn_release wording x label cells: the wording is a round-robin pick separate from the yes draw, so wording cells
  carry binomial noise (n ~ 55). Report-only; handled at selection by the wording x bin quotas.
- `test_i1_fixes.py::test_card_style_is_label_blind_and_shared_by_a_unit` FAILED once (gap in short-card share between gold
  yes and gold no 0.0407 vs the test's 0.04; n ~ 800 per gold at 400 seeds x 4 samplers, so the gap is ~2 sigma of noise).
  The yes draw changed, so that fixed sample changed. Independence checked on 36,000 rows over seeds 0-19,999 (short
  share 0.1514 for yes vs 0.1574 for no; gap 0.006). I did not edit the test. A tolerance of 0.05 or a larger seed range
  would remove the flake.
- G5-H / G3-H answers, and the old `pilot_i1` verdict files, are not carried over: gold values of yes/no rows changed.
