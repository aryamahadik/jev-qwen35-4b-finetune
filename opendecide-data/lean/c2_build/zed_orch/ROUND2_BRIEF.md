# Fix iteration 2 (the last one; A43 c): brief for each family agent

Read `c2_build/zed_orch/RULES.md` first; it binds you. Then read your family's iteration-1 records:
`pilot_i1/PILOT_VERDICT.json` (when present), `pilot_i1/FIX_I1_NOTES.md` or the `FIX_ITER1_REPORT.json` entry,
`pilot_i1/PILOT_REPORT.json` and `pilot_i1/G6_AT_6000.json`.

**Budget: at most about 50 tool calls.** Read only the code you change. Use targeted greps, not whole files.

## Steps
1. Back up `plugin.py`, `G0_SPEC*.md` and the runner to `<family>/_backup_i2/`.
2. Apply exactly the fixes listed in your task. They are generator/template fixes only; never relabel and never
   loosen a bar. If G0 text changes, re-freeze its sha the way the family already does, and update the tests that pin
   it.
3. Create `run_pilot_i2.py`: a copy of the family's `run_pilot_i1.py` with output folder `pilot_i2`. Keep `pilot/`
   and `pilot_i1/` untouched.
4. Run the family's tests. Check determinism (identical rows/relations sha256 under two PYTHONHASHSEEDs).
5. Run the pilot into `pilot_i2/`, with program gates and G5-H/G3-H task files (not answered).
6. Run A43 G6 on ≥ 5,000 rows into `pilot_i2/G6_AT_6000.json`, with
   `zed_orch/g6_at_size.py <FAM> --dir pilot_i2` or your runner with `--dry-run --n 6000 --no-g15`.
   - G6 must pass at 6,000 rows: every view and model ≤ chance + 2 pp.
   - Any 1,000-row cell above the bar must be within its pilot-size null.
   - G10 yes_rate_cells is report-only, because selection quotas enforce it.

## If your family needs Haiku-authored wordings (double negation etc.)
- Do steps 1-2 for the other fixes, then write the Haiku authoring task files. Use the family's existing brief or
  module and the polarity-aware check (`c2_kit/polarity.py`). Each task file must be self-contained: instructions,
  items, an exact answer contract and the answer-file path, in the same layout as the G5-H task files. Put them under
  `<family>/haiku/dneg_i2/tasks/`.
- Write two scripts and test both on fabricated answers in a temp dir:
  - **`dneg_stage2.py`** admits the authoring answers with the wording/polarity checks, then writes G-LEX task files
    for two independent Haiku reads under `haiku/dneg_i2/glex_tasks/`.
  - **`dneg_stage3.py`** admits the wordings that pass G-LEX 2/2 into a pool supplement and makes
    `run_pilot_i2.py`'s loader read it (no edit to `pilot_loaders.py`). It then runs steps 4-6 above.
    - It runs G13-seed on the new wordings if that takes under 30 CPU minutes. Otherwise it lists them in
      `pilot_i2/G13_PENDING.txt` for the batch run.
- Stop after writing them. The orchestrator runs Haiku and the stage scripts.

## Report
- `pilot_i2/FIX_I2_NOTES.md`: changes, gates_after (number vs bar), and the exact commands for any stage scripts.
- Final reply: at most 100 words.
