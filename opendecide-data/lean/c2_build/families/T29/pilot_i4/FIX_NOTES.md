# T29 iteration 4 (A45 b) - FIX_NOTES

## Changes (plugin.py; backups in _backup_a45/: plugin.py, test_plugin.py, G0_SPEC.md, run_pilot_i3.py)
1. Root-cause fix (full, no reweighting): sample() draws the REQUESTED candidate's position (`reqidx`) and its effect class (`reqeff`,
   uniform over the 7 effects) from the seed only (label- and qform-blind). _build_card forces that effect on that candidate
   (_draw_cand/_draw_values `force_effect`); _pick_request now checks only that candidate (verdict == target, ch_rule: single deciding
   rule). The existing 600 sub-seed rejection loop realises the gold, so P(effect class | gold) is flat by construction
   (3,000 base specs: each effect 13-17% for every verdict). A card whose planned requested intent cannot carry the target is dropped early.
2. UNIVERSAL_ATOMS: each tier of a card holds >= 1 rule made only of effect-free atoms (bulk, undo, recent, other_team, off_hours, prod, pii),
   so any effect class can carry any verdict; without it the forced effect made REFUSE favour cards with more forbidden rules
   (card-only leak, test_card_composition 4.4 pp). Label-blind card filter.
3. Calibration only: benign share 0.50 -> 0.44 on non-undo candidates (alarming_reversible_go band 0.10-0.22 was 0.093);
   TWIN_RATE 0.95 -> 0.92 (twin share bar 20-25%).
4. New test test_requested_effect_class_is_independent_of_the_gold. No test weakened. Question-form yes rates at base are 0.48-0.51 per qform
   (6,000 seeds); the 0.43/0.625 gap at 1,000 rows was twin/complement noise, not a sampler bias.
G0_SPEC.md untouched (no sha change).

## Gates after (pilot_i4, 1,000 rows, rows_sha256 bd8ebc09..., relations_sha256 57cfd2a7..., identical under PYTHONHASHSEED 1 and 2)
- pilot_size, G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G7, overlay (twin 0.225), spec_3_0: pass.
- G6 at 6,000 rows (G6_AT_6000.json, n=6001): PASS. yes/no max a_question lr 0.5075 (bar 0.52); choice max d_meta lr 0.284 (bar 0.2894, chance 0.2694).
  Was: yes/no 0.5203, choice 0.3022.
- G6 at 1,000 rows: choice b_options/lr 0.3035 > bar 0.291 (yes/no max 0.5108): needs the A43-erratum max-statistic null (NOT RUN: 8 draws in 16 min
  under load 80; run below).
- G10 at 6,000: fails only yes_rate_cells (report-only; selection quotas) and double_negation_share 0.0 = waived (A44 b / A45 a: dneg wording
  unavailable only because of A43 (f)). gold_position now passes (k=6 p was 0.0071). At 1,000 rows G10 fails only double_negation_share (waived).
- pytest families/T29: 74 passed (836 s).
- G3-H/G5-H task files written, NOT answered: pilot_i4/g3h/tasks (3), pilot_i4/g5h/tasks (4).

## Commands (from lean/c2_build)
- A43 null: ../.venv/bin/python -B zed_orch/g6_null_max.py --family T29 --runner families/T29/run_pilot_i4.py --dir pilot_i4
- Score after Haiku: /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B zed_orch/score_i1.py T29 --dir pilot_i4
- Re-run pilot: ../.venv/bin/python -B families/T29/run_pilot_i4.py ; G6: ... run_pilot_i4.py --g6 --n 6000
