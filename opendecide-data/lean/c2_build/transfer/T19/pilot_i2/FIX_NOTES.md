# T19 pilot_i2 (A45 c, transfer-dev; backup: _backup_a45/plugin.py)
Changes (generator only, no relabel, no bar change; plugin.py):
1. _plan: the negative form (`which`) and the double-negation draw are one label-blind draw per yes/no pair (pairkey).
2. render: wording is picked with a PAIR key (seed//2) so the two seeds of a pair (opposite gold) share the wording -> each wording is asked equally with gold yes/no.
3. relations: complement / partner / equiv-inv draws are per pair for yes/no rows (twin stays per seed).
4. ch_gap options: hash order rotated by the row's ch_gap ordinal in its balance cycle (seed-only, twins keep the same list) -> gold position even over k.
Gates after (6,000 rows, seed base 900000, zed_orch/g6_at_size.py): G6 pass: choice max 0.3134 (d_meta/lr) vs bar 0.329 (chance 0.309; was a_question/lr 0.3307); yes_no max 0.5000 vs 0.52. G7 pass.
G10 at 6,000: yes_rate_cells report-only; 10 of 16 cells n>=50 outside 50+/-2 (was 8 of 18), caused by twin asymmetry (twin rate depends on base verdict; twin gold 34/39 on yn_compliant), not fixable without relabel/thinning; selection quotas enforce it. double_negation_share 0.0: waived (A44 b / A45 a) (A43 f quarantine).
1,000-row pilot_i2: G6 yes_no d_meta/gbt 0.5281 (bar 0.52), choice a_question/gbt 0.3307 (bar 0.3296): both just above; A43-erratum null: `zed_orch/g6_null_max.py --family T19 --runner transfer/T19/run_pilot_i2.py --dir pilot_i2` was started in background (diag/null.txt; writes pilot_i2/A43_NULL_MAX.json); 6,000-row G6 passes.
Determinism: rows sha256 9dadd80149ecf0cf469d934c76fef575f7a49fc37f2b714b70b76d85268764a2 identical under PYTHONHASHSEED 1 and 7; relations 21219e3f2884d11ef44a6622996419d1b54639a8ed5884e3ff362e9ff0f36a46. pytest transfer/T19: 160 passed. G2/G3/G4/G-TW/G15 pass.
Files: pilot_i2/g3h, pilot_i2/g5h (tasks + key + manifest; not answered). Score: ../../.venv/bin/python -B zed_orch/score_i1.py T19 --dir pilot_i2
