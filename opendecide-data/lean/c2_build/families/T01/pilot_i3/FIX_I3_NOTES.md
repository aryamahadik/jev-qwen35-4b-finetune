# T01 fix iteration 3 (A44 a): notes (pilot_i3)

Backups: `_backup_i3/` (plugin.py, G0_SPEC.md, G0_SPEC_v4.md, run_pilot_i2.py). `pilot/`, `pilot_i1/`, `pilot_i2/` untouched.
No label relabelled, no bar loosened, no G0 text or sha changed, no pool, `pilot_loaders.py` or kit file edited.

## Cause (iteration 2)
G3-H failed only for mode F: all 200 rows mismatched on a leading "the ". G0 v4 (mode F) writes the passage as "about the <TOPIC>"
and the generator's topic is the bare phrase, but the schema said only "what the message is about, as written", so the reader copied "the ...".

## Changes
1. **G3-H topic describe** (`plugin.py`, `T01.TOPIC_DESCRIBE` = `TOPIC_DESCRIBE_I3`): "what the message is about, as written, WITHOUT the leading word
   "the" (the passage writes "about the ..."; the topic does not include that "the")". It matches G0 (TOPIC after "the"). `extract_fields` reads it.
   The pool-era task files keep the old text (`TOPIC_DESCRIBE_AUTHORED`); the new `families/T01/conftest.py` swaps it in for the modules that rebuild them
   (same approach as T06 / T23 / T25).
2. **`run_pilot_i3.py`**: copy of `run_pilot_i2.py` writing `pilot_i3/`. Its loader (`make_ctx_i3`) reads the dneg supplement minus every T01 form id in
   `zed_orch/a43f_quarantine.json`. All 177 supplement forms are in that list (and none of the 0 base-lexicon forms), so no double-negation wording remains.

## Tests / determinism
`pytest families/T01`: 204 passed. Determinism (PYTHONHASHSEED 1 and 4242, 1,000 rows): identical.
rows_sha256 `93cbc3b7abe5a02cfc356bebd0d92c819a43b21dc9d2a6516b23a4b7b2558469`, relations_sha256 `4eccb1016c00e40e5950ea7796016dbaa8f4f819496d545535d5d424f37f29e9`.

## gates_after (1,000-row pilot, `PILOT_REPORT.json`)
Pass: G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G7, overlay, spec 3.0 (max tokens 765, mean 617.9, mode F 18.8%).
- **G10 double_negation_share = 0.0% (bar >= 2%): fail, WAIVED by A44 b.** All other G10 checks pass except `yes_rate_cells` (report-only).
- G6 at 1,000 rows: yes_no n=513 best a_question/gbt 0.5361 (bar 0.52); choice n=487 best c_card_without_question/lr 0.3758 (bar 0.3564). Both are
  above the bar at pilot size; the binding check is the 6,000-row run and the pilot-size null below.
- **G6 at 6,000 rows (`G6_AT_6000.json`, 6,001 rows, G15 off): pass.** yes_no n=3114 max 0.508 (bar 0.52); choice n=2887 max 0.3495 (bar 0.362). G7 pass.
  G10 fail only on `double_negation_share` (waived) and `yes_rate_cells` (report-only; 5 of 6 cells with n>=50 outside 2 pp).
- A43 permutation null for the 1,000-row cells: observed M yes_no 0.0361, choice 0.0394 (match pilot.g6). Run in the background:
  `python -B zed_orch/g6_null_max.py --family T01 --runner families/T01/run_pilot_i3.py --dir pilot_i3`, log `pilot_i3/g6_null_max.out`,
  result `pilot_i3/A43_NULL_MAX.json` when finished (about 30 min). If it is missing, the run did not finish.
- Pending (Haiku): G3-H (188 mode-F rows, 4 task files in `pilot_i3/g3h/tasks/`) and G5-H (`pilot_i3/g5h/tasks/`); not answered.
  G3-H answers go to `pilot_i3/g3h/answers/`, then `pilot.py score`.

## Commands (from `lean/c2_build`; PY = `/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B`)
- `PY families/T01/run_pilot_i3.py run | dry | determinism | g6 --n 6000`
