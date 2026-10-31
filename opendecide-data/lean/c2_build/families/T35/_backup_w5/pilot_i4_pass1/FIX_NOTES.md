# T35 final iteration (A45 b), pilot_i4: notes

No commit, no model, no label touched, no bar loosened. Backups: `families/T35/_backup_a45/` (plugin.py, G0_SPEC.md, run_pilot_i3.py, old tests as *.py.bak).

## Changes
1. Cause (traced with `dev_tools/i4_none_branch.py`): the five failing S4 seeds are ch_line rows, not status rows. `_pad_to_plan` returned None on every one of 1000 tries (planned 2 groups; S4 draws applying + conflict + 1-2 other-agent groups).
2. `plugin.py::_draw`: a ch_line file with more groups than planned has the surplus dropped (extra other-agent groups, then the non-applying conflict group; never the applying group; plan and order only, never the gold). `RELAX_AFTER = 0` (relaxing only after 300 tries was tried: choice b_options lr 0.337, worse).
3. `plugin.py::sample` + `_assert_target`: every row asserts decide(spec) == plan target (yes/no allowed; choice nomatch/line effect), status rows included. Status rows keep the lines' own outcome independent of the status (deriving it from the outcome would make lines repeat the status).
4. 4xx/5xx share lowered toward the G0 aim of 2-3% (cap 4%): S4 p_ns 0.13 -> 0.09, status twin of a 200 base 0.20 -> 0.10. Reason: yes/no d_meta gbt read status x form: 0.5212 vs bar 0.520 (`dev_tools/i4_g6_attempt1.json`). Status-line share (about 15%) unchanged.
5. G0_SPEC.md: sections 9-11 merged into one section (the kit's one-page limit is 200 lines; i3's 218 lines had broken `test_contract_is_met_strictly`); sha re-pinned in plugin.py.
6. Tests: `test_fix_i3.py` trap test pinned an impossible cell (4xx x "may it fetch?" with gold no); now each class meets both forms and both golds and vice versa; trap count bar > 40. New `test_fix_i4.py` (5 seeds, every spec decides its plan, assert rejects a wrong plan). `run_pilot_i4.py` writes pilot_i4/.

## Gates after (number vs bar)
- Tests: 143 passed (full run 142 + the trap test fixed afterwards, rerun passed). Determinism PASS: rows sha256 `8086d6b094cb582f490604bb71a449f7e7ba56113ba67debe1b4c11b4c0e3258`, relations `69cc8f559edaba6ba3023a222a4cf9cc4c4a2eb0662be5c34159834e1fc06c6f` under PYTHONHASHSEED 1, 2 and the written pilot.
- Pilot: 1000 rows, no seed dropped, all program gates PASS incl. G6 at pilot size (yes/no best 0.500, choice best 0.2895 vs bar 0.3125), G7, overlay, spec_3_0 (mean tokens 729.3). G10: only double_negation_share 0% fails: waived (A44 b / A45 a).
- G6 at 6,000 rows (`G6_AT_6000.json`): yes/no max 0.5111 (d_meta lr) vs bar 0.520 PASS. Choice max 0.3181 (d_meta gbt) vs bar 0.3112 (chance 0.2912 + 2 pp) FAIL by 0.7 pp (n=1,809; one SE about 1.1 pp). G7 PASS. G10 yes_rate_cells report-only.
- Why choice fails now: pilot_i3's passing 6,000-row G6 (0.3111) silently skipped the ~4% hard S4 seeds; with them included, the choice rows carry a shape signal (driver ranking `dev_tools/i4_drivers.json`: clen, k, len_state, len_rank). Not fixed within this iteration's budget.
- Attempts: `dev_tools/i4_g6_attempt1.json` (trim only, old 4xx rate: yes/no 0.5212, choice 0.3149), `i4_g6_attempt3_relax300.json` (choice b_options lr 0.3374).

## Commands
    cd lean/c2_build
    ../../.venv/bin/python -B zed_orch/score_i1.py T35 --dir pilot_i4
    ../../.venv/bin/python -B families/T35/run_pilot_i4.py            # pilot -> pilot_i4/
    ../../.venv/bin/python -B families/T35/run_pilot_i4.py --g6 --n 6000
G5-H / G3-H tasks: families/T35/pilot_i4/g5h/tasks and pilot_i4/g3h/tasks (unanswered).

## Pass 2 (A45 c, choice d_meta gbt 0.3181): NOT FIXED, plugin.py left as pass 1 (restored from `_backup_a45b/plugin.py`)
Finding: the drivers clen/k/len_state/len_rank are not a plain shape-marginal gap (k, len_state, n_lines, mean/gold clen are balanced across gold kinds and
samplers; `dev_tools/i4b_stats.py`). The real option cue is the SURFACE PROFILE of the shown lines of "no line" rows (`dev_tools/i4b_prof.py` on a 6,000-row
build): "$"-anchored lines 44% of the lines of gold-"no line" rows against 30% of gold lines and 31% of wrong lines of line rows; file-ending 16% vs 24%;
Allow 46% vs 50%; profile TV distance 0.28. The shown lines of a "no line" row are 2-3 error-model candidates (near-miss / bait lines, `dev_tools/i4b_cands.py`),
with no freedom to pick a reference, so the gap lives in the file structure (`_applying_lines` nomatch branch + `bait_lines`), not in `matched_models`.
Also the length gaps differ slightly (k=3 gap between the 2 lines 8.2 chars on "no line" rows vs 6.5-7.1 on line rows; `i4b_rows*.pkl`).
Tried (kept out of plugin.py; code in `dev_tools/i4b_plugin_attempt_NOT_ACTIVE.py`): (1) "no line" row lines built like a line row (reference at a
virtual rank, neighbours below / above): pilot-seed G6 at 6,000 passed on the knife edge (max 0.3112 a_question lr vs bar 0.3114; `i4b_g6_virtualrank_attempt.json`)
but a fresh dev seed base 700000 FAILED (b_options lr 0.3248, c lr 0.3136, bar 0.3123), so it is not a fix; (2) reference profile drawn from a gold-profile table:
no effect (too few candidates); (3) near-line profile pick in the nomatch branch: no effect ("$" share still 44.8%).
Next step (by construction): make the nomatch file's near-miss and bait lines carry the gold-line profile mix (the typed near-miss generator `near_miss_typed`
and `bait_lines` produce "$"-anchored variants about 1.5x too often), i.e. draw the line's profile from the gold-line mix first, then build the near-miss of that
profile; then rerun the 6,000-row G6 on the pilot seeds AND one dev base (`dev_tools/i4b_dev.py SEED_BASE 6000`). Gates unchanged from pass 1: choice d_meta gbt 0.3181 vs 0.3112 FAIL; everything else as listed above.
