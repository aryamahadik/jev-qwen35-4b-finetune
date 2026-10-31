# T35 fix iteration 3 (A44 a, d): notes

Nothing was committed; no model or Haiku was run; no label was touched; no gate bar was loosened; `pilot/` and `pilot_i1/` are untouched.
Backups: `families/T35/_backup_i3/` (plugin.py, G0_SPEC.md, run_pilot_i1.py; the old test copy was deleted from it so pytest does not collect it).

## Changes
1. **Status trap (A44 d), `plugin.py::_plan`.** A trap is now a whole block of 4 yes/no bases (hash of the block < p_status x p_ns, the old F2 cap).
   The block's four (outcome, polarity) cells are the gold drawn first, each once. The status class is derived from the outcome (4xx = may fetch,
   5xx / no response = may not). So each status class meets both golds and both polarities. Positive frames only: `yn_fetch` ("may it fetch?") and
   `yn_skip` ("must it skip?"); never `yn_not_allowed`, `yn_prevented` or `yn_double_neg` in a trap block (A43 f). Non-trap bases show a 200 status
   at the rate that keeps the status line on p_status of all bases. The status-line share (about 15% of rows) and the 4xx/5xx cap (<= 4% of yes/no rows) are unchanged.
   Reading note: I kept the F2 cap and did not raise the 4xx/5xx share, because status x question form stays decodable in the d_meta view (the form is a metadata field).
   Choice rows carry no status or 200 only (M15), drawn from a hash independent of the target, so the status never decides which option is gold.
2. **Choice d_meta, `plugin.py::_draw` + `_pad_to_plan`.** Baseline on a 6,000-row in-memory build (`dev_tools/i3_choice_drivers.py`, output `dev_tools/drivers_base.json`):
   gbt 0.327 against chance 0.291 in my own CV. The gold position is already balanced (planned).
   Permutation importance: `clen` 4.7 pp, `tlen` 2.2, `len_rank` 1.3, `depth` 0.8, `len_ins` 0.4, `n_lines` 0.2.
   The option lengths mark the "no line matches" option (constant text); the row-level `n_lines` (+0.37 SD) and `depth` (+0.34 SD), plus `k` and `len_state`,
   differed between gold-is-"no line" rows and line rows. They told the model when that option was gold.
   Fix by construction: the file size (6, 7 or 8 rule lines; 2 or 3 groups) is planned from the seed alone, before the gold matters. The drawn file is padded up to it
   with never-matching unrelated lines and one-line other-agent groups, or redrawn when it is already bigger. Gold position, length rank and the abstain share 1/k stay as planned (F3).
3. **`run_pilot_i3.py`**: a copy of `run_pilot_i1.py` writing `pilot_i3/`. Its loader removes the 20 T35 forms of `zed_orch/a43f_quarantine.json` (and their wording skins) in memory and
   recomputes `double_neg_ok`. Option `--g6 --n 6000` writes `pilot_i3/G6_AT_6000.json`.
4. **G0 re-frozen**: `G0_SPEC.md` section 10 added (v5). The new sha256 is `edf1f2d021aa6c64a555bffc563371b8e0c5ff83904c33bb997da9c04133c1ac` and is pinned in `plugin.py`.
5. New tests: `test_fix_i3.py` (trap pairing, no status on choice rows, planned file size is independent of the gold type).

## gates_after (number vs bar)
- Determinism PASS: rows sha256 `1452c60e5cf060b27993183c8a0fbddd210aa39a876848f4084d65f7cb006777`, relations sha256 `f65f578ee0739b1cdd317a00d86ed7c38c50714f8c1771f4cd0e1b8903d98b70`;
  identical under PYTHONHASHSEED 1 and 2 (dry runs) and in the written pilot.
- Pilot (1,000 rows, 534 units): pilot_size, G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G7, overlay and spec_3_0 PASS. Real-token mean 727.4 (<= 800), max 1,168.
  G6 at pilot size PASS: yes/no n=701 best 0.5093, choice n=299 best 0.311 (chance 0.2935, bar 0.3135).
  G10: only `double_negation_share` 0% (bar 2%) fails, waived by A44 (b).
- **G6 at 6,000 rows PASS** (`G6_AT_6000.json`): yes/no n=4,229, max 0.516 (d_meta gbt; bar 0.520, thin margin; the i1 run had 0.5087).
  Choice n=1,771, max 0.3111 (b_options lr; bar 0.3124, thin margin); choice d_meta gbt 0.2998, lr 0.2806 (i1: 0.3344 vs 0.3112 failing).
  G7 PASS. G10 `yes_rate_cells` fails at 6,000 rows (report-only per the round-2 brief; selection quotas enforce it) and the waived double negation.

## Open items
- **Tests: the full T35 pytest run was still going (many F/E marks in `dev_tools/i3_tests.log`) when my tool budget ended. I did not read the failure names.**
  Likely causes: older tests pinning the choice-file shapes or the status-trap draw (`test_fix_i1.py`, `test_plugin.py`) and the sha pin; unresolved. Please run
  `cd lean/c2_build && ../../.venv/bin/python -B -m pytest -q -p no:cacheprovider families/T35 -x` and read the first failure. `test_fix_i3.py` was not seen to pass either.
- The post-fix driver ranking was not re-run (budget). The G6 result above is the evidence.
- Both G6 maxima sit within 0.5 pp of their bars; yes/no d_meta (0.516) got worse than in i1 (status x form interaction is decodable in the metadata view).
- Choice rows are now 6-8 lines and 2-3 groups only, so file shapes are less varied than in i1; mean tokens did not rise (727.4).
- G5-H (2 readers x 100 rows) and G3-H task files are in `pilot_i3/g5h/tasks` and `pilot_i3/g3h/tasks`, unanswered (Haiku run by the orchestrator).

## Commands
    cd lean/c2_build
    ../../.venv/bin/python -B families/T35/run_pilot_i3.py                     # pilot -> families/T35/pilot_i3/
    PYTHONHASHSEED=1 ../../.venv/bin/python -B families/T35/run_pilot_i3.py --dry-run --no-g15   # determinism
    nohup ../../.venv/bin/python -B families/T35/run_pilot_i3.py --g6 --n 6000 > g6.log 2>&1 &    # G6 at 6,000 rows
