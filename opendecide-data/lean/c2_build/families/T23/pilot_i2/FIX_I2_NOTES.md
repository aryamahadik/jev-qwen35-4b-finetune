# T23 fix iteration 2 (pilot_i2)

## Changes (generator fixes only; no relabel, no bar moved, G0_SPEC.md and its sha untouched)
1. `plugin.py` `extract_fields`: ITEM description is now `ITEM_FIELD_DESCRIBE` = G0 section 10 ruling B2 verbatim:
   "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)".
   The article is NOT part of the item. `g3h.compare` and the 98% bar are unchanged.
2. `plugin.py` `item_article` / `agree_item_article`: a/an by the item's first sound. Small table first (an: e-, x-, hour,
   honest, honour/honor, heir, mp3, html, mri ...; a: u-, unit/union/unique/univers/unif, use, usa, eu, one, once ...),
   then the kit's `c2_kit.skin.article`. Root cause of "an laptop" / "a office chair": a Mode F note keeps the article
   it was written with for ITS brief item, and the kit swaps in another item. `render` now rewrites a literal "a"/"an"
   directly before the note's brief ITEM to the article the row's item needs (reads the item only; "the", "my" untouched;
   Mode T `{a|ITEM}` already agreed via the kit). Item sound, not gold, decides: label-blind.
3. `haiku_extract.py` `g3h_batch`: keeps the frozen v1 ITEM text (`V1_ITEM_DESCRIBE`) so it still reproduces the v1 task
   files on disk (test_freeze_v2 pins that).
4. `run_pilot_i2.py` (copy of `run_pilot_i1.py`, output `pilot_i2/`), `test_i2_fixes.py` (27 tests).
Backups: `_backup_i2/` (plugin.py, G0_SPEC.md, run_pilot_i1.py).

## Checks
- Tests: `families/T23` 192 tests; first run 189 pass + 3 `test_freeze_v2` fails (v1 task-file match), fixed by item 3;
  those 9 "real" freeze tests then pass. `test_i2_fixes.py` 27 pass. (The full folder was not re-run after item 3.)
- Determinism, `run_pilot_i2.py --dry-run` under PYTHONHASHSEED=0 and =1: identical.
  rows sha256 `fff7fe8a3b64ff32e0a0aa0f7b901b32a7ff8a83a8a0ec4edd3f7959c7cf1cf3`,
  relations sha256 `6966522ba0de435af3624e5ec8715a1cbc8372a07dff2b75c274a3d0aa0a5f79`.
- Article scan over all 40 pack items in the rendered rows: pilot_i1 259 article-before-item occurrences, 13 mismatches
  (an laptop, a e-bike, a office chair, an washing machine, an grocery order, an camera bag); pilot_i2 259, 0 mismatches.
  So no rendered row has "a <vowel-sound item>" or "an <consonant-sound item>".

## gates_after (pilot_i2, 1,000 rows)
- Program gates pass: pilot_size, G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G7, G10, overlay, spec_3_0.
- G6 at 1,000 rows: FAIL by noise, one cell: yes_no c_card_without_question/gbt 0.5212 vs bar 0.52 (n=520, one-sided
  binomial p vs chance 0.179, within the pilot-size null; i1 was 0.5103 at this size). The edit changes ~13 note texts only.
- G6 at 6,000 rows (`G6_AT_6000.json`): PASS. yes_no n=3120 max 0.5103 (a_question/lr), choice n=2880 max 0.5094
  (d_meta/lr); bar 0.52. G7 pass.
- G10 yes_rate_cells at 6,000: report-only, one n=50 cell (yn_version#4cad73f7, 0 negations) yes=0.420, as in i1 (selection quotas).
- G5-H, G3-H: pending, task files regenerated and not answered.

## Haiku steps for the orchestrator (no new wordings needed)
- G3-H: `pilot_i2/g3h/tasks/T23-extract_g3h-7d2d7b6c-00{0..3}.md` (191 Mode F items, 4 tasks; ITEM text is the B2 wording,
  checked: no task holds the old text). Answers go to `pilot_i2/g3h/answers/`. Then `pilot.py score` / `zed_orch/score_i1.py T23`
  as in i1.
- G5-H: `pilot_i2/g5h/tasks/` (4 tasks, `key.json`, `manifest.json`). The rows moved by the article rewrite are Mode F
  rows only; the i1 G5-H result does not carry over automatically, so re-read it with these files.
- Expected: no ITEM-with-article mismatches; quarantine should empty and Mode F stays near 19.1% (191 rows).
