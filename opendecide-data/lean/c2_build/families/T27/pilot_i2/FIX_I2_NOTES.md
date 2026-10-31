# T27 fix iteration 2: notes (G6 view c, request overlap)

Backups: `../_backup_i2/` (plugin.py, G0_SPEC.md, run_pilot_i1.py, solver_b.py, test_plugin.py). `pilot/` and `pilot_i1/` untouched.

## Finding (measured on the frozen pools_v2 lexicon; why the fix needs new wordings)

Overlap o of a request = share of its content stems the user's text already holds (task clause + printed allowed list).
Over every (task, task form, action, gate request form):
- in scope: o = 0.0 on 5 of 548 combinations, 0.3 on 4, 0.5 on 50, 0.6-0.8 on 223, 1.0 on 236 (band none 3 / partial 14 / high 36 of 36 task-action pairs);
- beyond: o = 0 on 8,806 of 10,106 combinations (87%); > 0.5 on 42 (0.4%; 6 of 804 task-action pairs).
So the label is readable from overlap by construction: no choice among the ADMITTED forms gives an in-scope request that
paraphrases with disjoint words, nor a beyond request that reuses the user's words (a beyond action is a different action).
Steering form choice alone cannot move the label gap (checked: it keeps in-scope 0.5-1.0 and beyond 0-0.3), and re-drawing the
beyond cells by level breaks the task / action marginals. Both need new FORMS of the existing `req.<action>.<gate|plain>` sems.

## Changes (generator / template only; no relabel, no bar loosened, no pool edited)

- `overlap.py` (new): stems, bands (none 0 / partial <= 0.5 / high), `OverlapModel` (o and form steering over admitted forms), `plan()`.
  A ch_next row has a LEVEL drawn from the seed (`strat(seed, sampler, "ovl")`) before and independently of the label, same shares for every
  label. Shares = band masses of the beyond joint J (a cell with several feasible bands is split evenly), so the per-level beyond cells mix
  back to J exactly (tested to 1e-9: task, action and pair marginals unchanged). do_step keeps its draw and prints task + request forms in
  the band; a beyond row draws its cell from the level's part of J and prints in the same band. Gold stays the action x scope table.
  Task twins keep their base's band (`_ovl_twin_guard`).
- Levels switch on only when every beyond cell and every do_step cell can print in every level with mass (`plan()` else None). With the
  frozen lexicon they cannot, so **levels are OFF and rows are exactly those of iteration 1** (no rng draw moved when off).
- `plugin.py`: `_ovl`, `_ovl_plan`, `_build_choice(..., ovl_u)` returns (slots, level), `_assemble(..., ovl)`, `spec.structure["ovl"]` when on.
- `G0_SPEC.md` v1.3 (181 lines <= 200), `G0_SHA256` 0f5c164f8b41927cd874781996ad44e34389859668d3b8f558265c7732b67655.
- `ovl_author.py` (new): `tasks` / `stage2` / `stage3` for the missing forms (below). Tested on fabricated answers in a temp dir (5 admitted
  by the band check, a high-overlap "partial" candidate rejected, 4 of 5 kept after a split G-LEX read). Stage 3 `--run` not exercised.
- `run_pilot_i2.py`: copy of run_pilot_i1.py, output `pilot_i2`; merges `haiku/ovl_i2/admitted/lexicon_supplement.json` into the lexicon at
  load time when it exists (pools_v2 and pilot_loaders.py untouched).
- `test_overlap.py` (new, 9 tests): text model, steering, plan None / on, mix-back to J, level independent of verdict (fake model that can
  print every band), gold = scope table, twin keeps the band. All pass.

## Open: Haiku authoring (orchestrator runs it; I cannot)

1. `haiku/ovl_i2/tasks/T27-author_ovl-*-000.txt` (8 files, 112 items: 28 actions x gate / plain x band none / partial; 3 gate or 2 plain
   clauses each; the answer path is named in each file, `haiku/ovl_i2/answers/<task id>.json`).
2. `cd lean/c2_build; ../../.venv/bin/python -B families/T27/ovl_author.py stage2` : admits answers (wording + per-task band checks), writes
   `haiku/ovl_i2/glex_tasks/T27-glex_ovl-read{1,2}-NNN.txt` (answers to `haiku/ovl_i2/glex_answers/<same id>.json`, two independent readers).
3. `... ovl_author.py stage3 --run` : keeps forms both reads map to their own sem (`admitted/lexicon_supplement.json`), writes
   `pilot_i2/G13_PENDING.txt` (G13-seed not run here), re-runs the pilot and G6 at 6,000.
Expected: beyond "high" needs echo forms for only ~0.4% of cells; if `plan()` is still None after stage 3, `_ovl_plan` returns None and
the gap is unchanged: check with `plan()` on the merged lexicon which (task, action) cell lacks a band.

## gates_after (pilot_i2 = iteration-1 rows, levels off)

See `PILOT_REPORT.json` and `G6_AT_6000.json` in this folder when the background runs finish (rows sha must equal pilot_i1's
2c57f109ff76394d0a5619b2120e27857b06fa5f60b476ed22a985e2ac8b7869). G6 choice c_card_without_question lr is expected unchanged at 0.4884
(bar 0.3533) because the rows are unchanged: this iteration does not fix G6 until the authored forms exist.

## Iteration 2b (FINAL pass, A43 e): both rulings applied (backups: `../_backup_i2b/`, `../_backup_i2/`)

### Changes
1. Choice view c (`overlap.py`, `plugin._build_choice/_ovl_plan/beyond_joint`)
   - `plan` drops every level that some do_step cell cannot print (`partial`); levels now none ~0.99 / high ~0.01 for S1-S4 (before: plan None, no level).
   - One request-form pool per (action, framing, level) (`OverlapModel.pool`) for both scopes; beyond rows draw from it, filtered by their own task.
     Task form drawn from the forms that print every action of the task's own list at the level, for every label.
   - Level from `strat(seed,...,"ovl")` (seed only, before the label); a do_step row draws its task from the level's beyond-cell task marginal (`Plan.task`).
   - 20 beyond cells (4.2% of J) have no pool form at a level left: removed and J refitted by IPF (`beyond_joint(exclude=...)`), marginals stay exact.
2. Yes/no d_meta (`plugin.sample/_plan_yn/_build/card_style/_twin_candidates`)
   - Task kind (1 or 2 allowed actions, P_TWO 0.40), request count (p2) and card style come from the seed PAIR before the label (pair gold is opposite), so each
     (qform, kind, count, style) cell is exactly half yes. Tasks and request actions are drawn inside the kind. Card style is now Kronecker in k//2.
   - p_readonly = p_zero = 0 on all samplers (no read-only task, no request-free row). Yes/no task twins keep the base's kind and are never read-only.
   - NOT DONE as ruled: "pad content with neutral filler lines". The carrier skins are fixed Haiku-authored templates with declared slots (no filler slot), so padding
     needs new skins (Haiku). Removing the rows whose gold is fixed by their shape (read-only, request-free) gives the same independence by construction.
3. G0_SPEC.md v1.4 (sections 2 and header); new sha `2148eb76f789a906fdfb2d4514d7cf8b3ed9573c306b7bc9055e9b12b5b6ba08` set in `T27Plugin.G0_SHA256` (test pins it).

### Tests (`test_overlap.py`, `test_plugin.py`)
157 passed, 1 failed. Updated to the new invariants (same bars): pool shared across scopes, plan drops levels / cells, task marginal mixes back, read-only and no-request
shares are 0 (were floors), card style per pair (one pair = 2 cards instead of 1.5), action-share test on 3,000 seeds for yes/no (1,500 for ch_next, unchanged code),
new `test_yes_no_structure_is_drawn_from_the_pair_before_the_label`.
FAILING: `test_units_pass_every_program_gate_with_the_overlay_shares`: yes_is_bad share 0.5515 > 0.55 on 250 seeds x 5 samplers (pilot G10 yes_is_bad_share = 0.529, pass).
Not changed (no loosening); cause not isolated (twin availability by qform changed with the same-kind twin rule).

### Determinism
rows_sha256 `88cbc26e0f01b59e2ba602fec6bcb0b2f6b17997d8ad2a84e64847a2ec9183ed`, relations_sha256 `8b035ba7e94afe19bb33363f27e5ddc2f3c2f595deb0bae1eb7764b5ce03f94e`,
identical under PYTHONHASHSEED=0 (written run) and =1 (--dry-run), 1,001 rows.

### Pilot (pilot_i2/, 1,001 rows; run_pilot_i2.py with the ovl supplement)
pass: pilot_size, G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G7, G10, overlay, spec_3_0. pending: G5-H (12 blind-read task files in `g5h/tasks/`, not answered).
G3-H n/a (no Mode F row). G6 at pilot size fails four cells (n=465 yes/no, 536 choice; bar chance+2pp): yes/no a_question gbt 0.5333, d_meta gbt 0.5226;
choice a_question lr 0.3545, d_meta gbt 0.3563. Their pilot-size nulls were NOT computed (budget); the 6,000-row G6 below passes.
G10 pilot: yes_rate 0.5118, yes_is_bad 0.529, all checks pass.

### G6 at 6,000 rows (`G6_AT_6000.json`, --dry-run --n 6000 --no-g15): G6 PASS, G7 PASS
| cell | before (diag, 6,000 rows) | after |
|---|---|---|
| choice, max cell | c_card_without_question lr 0.3965 (bar 0.3533) | c_card_without_question lr 0.3469 (n=3,113) |
| yes/no, max cell | d_meta gbt 0.5344 (bar 0.52) | c_card_without_question gbt 0.5159 (n=2,888); d_meta below that |
G10 at 6,000: only `yes_rate_cells` fails (18 of 31 cells >= 50 rows outside +-2 pp, e.g. 0.610 n=59); report-only per the brief (selection quotas enforce it).

### Overlap checks (work_i2b/diag_after.txt, omax_model.txt; 3,002-row build, 1,563 choice rows)
- Level is label-independent: none n=1,555 stop 0.34 / continue 0.33 / do_step 0.33 (high n=8).
- One-feature accuracy of the MODEL overlap (items excluded, 3 values): 0.346 vs chance 0.333 (o_max=0 on 1,555 rows: 536/511/508). Before: 0.809.
- The diag's `o_max` (item words included) still scores 0.669: it counts the gate item shared with the task (gate on the TARGET = the rule's span match) and the scope
  of each request (scope1/scope2 0.67); that is the rule itself, not a leak, and G6 c at 6,000 passes.

### Remaining
- Fix or justify the one failing unit test (yes_is_bad 0.5515 on 250 seeds).
- G5-H blind reads (orchestrator, Haiku) on `g5h/tasks/`; G13-seed pending list `G13_PENDING.txt` (no new wordings this pass).
- Optional: pilot-size null for the four 1,000-row G6 cells; padding skins (needs Haiku) if read-only / request-free rows are wanted back.
