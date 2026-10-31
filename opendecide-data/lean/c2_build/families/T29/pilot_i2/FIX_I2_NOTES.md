# T29 fix iteration 2e (FINAL pass, A43 e): G6 at 6,000 rows PASSES with fixed 3 candidates - STATUS: G6@6000 pass; spec 3.0 pass; gold-position fix NOT done; tests/G6@1000/G10 open
Backups: `_backup_i2d/`. G0 v1.6 (section 9 folded into the last G0 line: the 200-line page limit), `G0_SHA256 = 35a6a72b...b299` (`set_g0_sha.py`). No Haiku, no commit, no bar loosened, no label changed.
- Ablation at 6,000 rows (`ablate_g6.py ARM KEY=VALUE`, outputs `abl_*/G6_AT_6000.json`, one change at a time from the 2d build; base reproduces 2d): fixed 3 candidates PASS (yes/no a_question gbt +1.82 pp, choice c_card lr +1.66 pp); fixed 4 fails (choice a_question lr +2.78); TWIN_RATE 0.93 (choice +2.1), FEATURE_P (0.40,0.50) (choice d_meta gbt +2.14), P_DROP_IRRELEVANT 0.25 (3 choice cells fail, +2.2): fail; style draw off: identical to 2d (fail). Kept: `N_CANDS_W = ((3, 1.0),)`; the three rates and the style draw stay as in 2d.
- Final cells (`G6_AT_6000.json`, 6,000 rows, `dneg_stage3.py`, log `stage3_2e.out`): G6 pass: yes/no max 0.5182 (a_question gbt) vs 0.5 (+1.82 pp); choice max 0.2868 (c_card lr) vs 0.2702 (+1.66 pp). G7 pass. G10 fails at 6,000: {'yes_rate_cells': 'fail'}.
- Pilot (`PILOT_REPORT.json`, 1,002 rows): G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G7, overlay pass; spec_3_0 pass: mean 761.1 (bar 800), max 1282, deep 5.5%; twin share 22.1%. G6 at 1,000 rows FAIL: yes/no a_question gbt 0.5435 (n=517), choice d_meta lr 0.2948 (n=485): pilot-size null check (zed_orch/g6_null_max.py) NOT run. G10 at 1,000 rows fail: yes_is_bad_share 0.5513 (bar 50 +/- 2?). Determinism: rows sha 1eb852e3...4b89 / relations 5940321b...8b91 identical under PYTHONHASHSEED 1 and 2.
- Gold position: tried kit `build_closed(plan=plan_choice(...), strict_plan=False)` (ch_verdict closed=3+abstain, ch_rule closed=len(rids)); REVERTED: the plan puts the gold at the planned slot, so a twin (other gold, same row key) gets another option order and G-TW "closed option set differs" failed on every twin (test_relation_units_pass_every_gate, 244 units). A by-construction fix needs the planned order stored in the base spec structure and copied by twins and premise partners (custom OptionSet build). Not done. At 6,000 rows the final run's gold_position verdict: see G10 fails above.
- Question wording: the requested action's name fixes its effect and tone (ACTIONS table) and so can carry the label via the rules' effect atoms; requested-action wording by label was NOT measured and nothing was re-drawn (open item).
- Tests (stage 3 runs `pytest -x`): stopped at the first failure, `test_plugin.py::test_relation_units_pass_every_gate` (1 failed, 32 passed); the remaining tests were not run on the final code. The earlier full run on the plan-edit variant had 6 failures (not the final code). The pre-2e baseline (`pytest_i2d.out`) already had failing tests (strict contract, double-negation declaration, others).

# T29 fix iteration 2d (compact cards + one-line candidates): spec 3.0 PASSES, G6 at 6,000 rows FAILS - STATUS: OPEN
Backups: `_backup_i2c/` (G0_SPEC.v1.4.md, plugin.v1.4_before_2d.py, solver_b.v1.4_before_2d.py). G0 v1.5 (section 8), `G0_SHA256 = 1caa7bcb...3213` (`set_g0_sha.py`). No Haiku, no commit, no bar loosened, no label changed.
- Changes: ONE candidate table under a shared header (4 layouts), 3-5 candidates drawn from the seed (60/30/10, mean 3.5), cards.CardSpec compact (85%) / short (15%) lines (header, verdict, confirmation, missing-data; rule lines without parentheses and final period), closed-world sentence shortened, precedence from the 12 shortest forms, distractor field never the request time. Knobs retuned to keep the old test bands: TWIN_RATE 0.93->0.88, FEATURE_P (0.40,0.50)->(0.34,0.58), P_DROP_IRRELEVANT 0.25->0.90. Solver B reads the table, styles and rule variants (G2, G3, G4, G-TW pass).
- Run: `dneg_stage3.py` (tests, determinism, pilot_i2, G6@6000): `stage3_2d.out`. spec_3_0 mean 783.8 (max 1389; bar 800), G10 at 1,000 rows pass, overlay pass.
- G6 at 6,000 rows (`G6_AT_6000.json`): FAIL: yes/no a_question gbt 0.5208 vs 0.5 (+2.08 pp); choice a_question lr 0.299 vs 0.270 (+2.9 pp). G10 at 6,000: yes_rate_cells (report-only) and gold_position chi2 (k=4 p 0.0375, k=6 p 0.0036) fail. 1,000-row G6: yes/no a_question lr 0.5214 (p 0.18), choice d_meta gbt 0.3066 vs 0.2721 (max-null check not run).
- Not isolated: which of n_cands / the three knobs / the style draw moved the question-only view (iteration 2c passed at +0.3 / +1.0 pp). Next: ablate each knob at 6,000 rows (`run_pilot_i2.py --g6 --n 6000`).

# T29 fix iteration 2c: question-carried choice (orchestrator ruling) - STATUS: G6 at 6,000 rows PASSES on every view and model

Backup of the 2b files: `_backup_i2c/`. No Haiku wordings, `haiku/dneg_i2/` untouched, no commit, no bar loosened, no label changed.
- Design (G0 v1.4, section 7 of G0_SPEC.md; `G0_SHA256 = ece82e56...bcb`, `set_g0_sha.py`): one policy + 3-5 candidate actions, each its own
  call line, catalog entry and snapshot; the question names ONE (the existing {ACTION}/{TARGET} slots). `plugin.py`: `_build_card` (label-blind,
  plan go/ask/refuse/cannot[+confirmed-ask][+extras], `_draw_cand` per intent), `_pick_request` (the planned label from the seed picks the
  candidate), `_make_spec`/`_cand_view`/`_pre` (requested candidate = unprefixed slots, others `C<j>_`), `_card_missing`. The cannot slot on
  a card without a missing field is replaced by a go/ask/refuse candidate (card length must not tell CANNOT DECIDE). Premise twins on depth>=2
  cards kept at 0.78; benign tone 0.85 on undo cards; TARGET_W_SHOWN now 1.0. Solver B (`solver_b.py`) parses every candidate block and finds the
  requested one by the question's action/target; G3 canonical adds `candidates`.
- gates_after (`G6_AT_6000.json`, 6,000 rows, `zed_orch/g6_at_size.py T29 --dir pilot_i2`): G6 pass. yes/no max 0.5027 (c, gbt) vs 0.5 (+0.3 pp);
  choice max 0.2791 (a_question lr) vs chance 0.269 (+1.0 pp), bar +2. c_card_without_question was +3.8 pp. G7 pass. G10 fails only on
  `yes_rate_cells` (report-only) and `double_negation_share` (until stage 3). Solver A == B and G3 on 5,000 specs: pass (test_plugin). 
  Determinism: `run_pilot_i2.py --dry-run --n 300` identical rows/relations sha256 under PYTHONHASHSEED 1 and 2 (rows 9ee2a041...).
  Label balance on 18,000 rows: ch_verdict k3 go 870 / ask 844 / refuse 856; k4 cannot 1499 / refuse 1417 / ask 1413 / go 1367 (cannot 26.0%).
- Tests: updated `test_plugin.py` (`_visible`: confirmation seen as none/mention/explicit, card-level missing). Still failing (pin old
  single-call/target-first properties, kept failing, see `pytest_i2c.out`): see the final reply. Not run: the full `run_pilot_i2.py` pilot (program gates,
  G5-H/G3-H task files) and G13: open items. The old 2b text below is history.

# T29 fix iteration 2: notes (status: G6 NOT cleared at 6,000 rows: c-view +3.8 pp vs bar +2; double-negation authoring task files written)

## (0) Iteration 2b: label-blind `sample()` (orchestrator ruling) - result and open items
Backup of the previous plugin/G0/runner: `_backup_i2b/`. No Haiku/model run, no commit, no bar loosened, no label changed.
- `plugin.py sample()` rebuilt: qform / card id / display / planned label come from the seed only (ch_verdict: kit `plan_choice(closed=3,
  abstain=True, show_rate=0.60, abstain_share=CANNOT_SHOWN)`; go/ask/refuse weighted as before; yes/no: the yes draw; ch_rule: P_RULE_NONE).
  Then for sub-seed 0..599 `_blind_card()` draws the WHOLE card (conversation kind, rules, thresholds, hours, which rules fire, all snapshot
  values, the missing field) without reading the label, and the verdict of the finished card is the only place the label is read; an
  infeasible card is dropped and the next sub-seed draws a new one. The label is never redrawn. Solver A/B agreement and the G4 relations
  are untouched (solver A is asserted against the planned label in sample()). Removed: `_plan`, `_draw_card`, `_attempt`.
  0 construction failures on 1,500 specs; 3.6 s for 1,500 specs. Determinism: identical sha256 of 600 specs + relations under
  PYTHONHASHSEED 1 and 2.
- G0 re-frozen as v1.3 (row S23 and the status line); `G0_SHA256 = 295dc06a8424b31ac7e3fd797f03fffc8d7d5bb90803cecef2d71f5d9442eb80`
  (`set_g0_sha.py`; the plugin constant equals the file's sha256). The dneg authoring task files record this sha.
- Choice base abstain share: the planned base share is `CANNOT_SHOWN` (0.13), NOT 1/k, because premise-removal twins (S26) add the rest of
  the cannot golds; over all emitted rows balance_sim (6,000 rows) gives cannot|shown 24.8%, mix go 782 / ask 722 / refuse 744 / cannot 461,
  ch_rule none 19.0%, yes 50.0%. If the orchestrator wants a literal 1/k on base rows the premise-twin rate must be cut instead.
- **G6 at 6,000 rows (`zed_orch/g6_at_size.py T29 --dir pilot_i2`, `G6_AT_6000.json` = the kept generator, per-rule fire chance FIRE_P)**:
  choice c_card_without_question LR 0.3079 vs chance 0.2700 = **+3.8 pp (bar +2): FAIL** (was +4.9 to +5.0 pp); choice a_question LR 0.2958
  = +2.6 pp (FAIL, borderline; passed in iteration 1 and in the variant below, so it may be fold noise); every other view/model passes
  (yes/no max 0.5063 vs 0.5). G7 pass. G10 fail only on `yes_rate_cells` (report-only) and `double_negation_share` (until stage 3).
  A variant that makes exactly one rule per tier fire (count-independent) was worse: c-view 0.3192 vs 0.2689 = +5.0 pp, a_question passes
  (`G6_AT_6000_v2_fireq.json`; code reverted). `G6_AT_6000_v1_firep.json` = copy of the kept result.
- What is left is the card's natural label dependence, now measured with every steering removed: depth by verdict (depth-1 share go 26%
  vs cannot 33%), the number of two-condition rules, the effect/atom couplings (an explicit confirmation of this call rules out ASK FIRST).
  Tests that pin the old target-first construction fail for exactly these reasons (kept failing, not loosened; 70 pass, 3 fail in
  `pilot_i2/pytest_i2b.out`, run with the kept generator): `test_fix_iteration1::test_depth_is_the_same_for_every_verdict` (spread 6.6 pp vs
  6), `test_plugin::test_label_balance_on_2000_specs` (harmless_irreversible 8.8% vs >= 10%), `test_plugin::test_card_composition_is_label_blind`
  (atom_tier delete/confirm -> refuse 24% vs 30%). The FIRE_Q variant: 9.95% / n_pairs go 30.5% vs 35.3%.
- Not run: `run_pilot_i2.py` pilot (program gates, G5-H/G3-H task files), because G6 is not cleared; the other pilot gates are unmeasured.
- Options for the orchestrator (a ruling is needed; nothing more was tried in this budget): (a) raise P(go) rejection structure-wise is NOT
  allowed; (b) a structure-matched design: draw the card's rules / thresholds / hours label-blind, then give the SAME structure to all
  planned labels by trying several value draws per structure (fixes rule counts, depth and pairs, but values still carry the verdict);
  (c) accept the natural leak and re-state the c-view bar for a gold that is a function of the card (a spec question).

## (0b) Dneg authoring task files written (exact paths)
`lean/c2_build/families/T29/haiku/dneg_i2/tasks/T29-author_wording-5bb519ab-000.md` and
`.../T29-author_wording-8bd08861-000.md` (manifest `haiku/dneg_i2/manifest`, `TASKS.json`). Answers go to `haiku/dneg_i2/answers/<task_id>.json`.
Stage commands (from `lean/c2_build`, `PY=../.venv/bin/python`): wrote with `$PY -B families/T29/dneg_stage2.py --write-author`; after Haiku
answers: `$PY -B families/T29/dneg_stage2.py`, then Haiku reads `haiku/dneg_i2/glex_tasks/tasks/*.md`, then `$PY -B families/T29/dneg_stage3.py`
(`--no-pilot` to stop after the supplement). Details in section (2) below.

No Haiku or model run, no commit, no bar loosened, no label changed, no pinned file edited. Backups: `_backup_i2/`.

## (1) G6 c_card_without_question (choice), diagnosis on a 6,000-row in-memory build (2,970 choice rows)
Tools: `g6_cue.py` (build + pickle), ablations of the pilot's own c-view features (option-token x card-token crosses, LR,
GroupKFold by card). Baseline: c-view +5.03 pp over chance.
- The signal is NOT the abstain display or option text. Per-part ablation: catalog + call lines alone give +5.07 pp, rules alone
  +2.0, snapshot alone +2.0.
- Main single cue: the **undo window number** in the catalog line ("undo window 96 hours"; chi-square vs gold p 1e-11). "undo < t" is
  true when the window is the smaller number, and the window was drawn on the side the verdict needed, so 0-6 hours meant
  REFUSE/ASK and 24-48 meant GO.
- Fix applied (plugin.py `_undo_pair`, `UNDO_GRID`): the window and every undo threshold are drawn from ONE shared grid as an
  exchangeable pair and only the atom truth is checked (boundary rows use the grid's +-1 neighbours). The unordered bag of numbers
  a token reader sees then carries no truth. Zero-hour windows keep 5% of the all-true rows (A3; this keeps a small leak).
  Nothing dropped; S5 untouched. G0 text not changed.
- Result on a fresh 6,000-row build: catalog-only view +5.07 -> +3.08 pp. **The full c-view is still +4.90 pp (bar +2.00)**: a diffuse
  residual remains. Removing digits, the effect phrase and the action name from the card still leaves +3.6 pp. Effect vs gold
  (p 2.5e-4 at k=4) and many small atom/value cues all come from the target-first construction (atom truths and the effect/values
  they force depend on the gold, and rejection redraws values until they fit).
- What would clear it (not done; needs a re-architecture of `sample`/`_draw_card`, beyond this budget): draw the card (rules,
  thresholds, effect, field values or their truth pattern) label-blind first, keep the card only if every target the cell needs is
  feasible, then pick the gold uniformly among feasible targets, and for numeric atoms draw the exchangeable pair as above. Atoms
  `bulk`, `pay`, `recent` (gt/ge and lt/le comparators in one direction) have the same number-side cue.
- The real G6 (pilot.g6, all 14 views) was not re-run on the new generator: the numbers above are my replication of the c-view.
  `run_pilot_i2.py --g6 --n 6000` does the real run.
- Tests: the 94 T29 tests pass with the change (`pytest families/T29 --deselect test_dneg_i2.py`).

## (2) Double negation: files and commands (orchestrator runs Haiku between the steps)
Code: `dneg_i2.py` (shared), `dneg_stage2.py`, `dneg_stage3.py`, `run_pilot_i2.py` (loader `with_dneg`), `test_dneg_i2.py` (2 tests, pass:
authoring task files; stage 2 -> fabricated G-LEX reads -> stage 3 admit with one wrong read rejected, supplement written, G13 list).
From `lean/c2_build`, with `PY=../.venv/bin/python`:
0. `$PY -B families/T29/dneg_stage2.py --write-author` writes `haiku/dneg_i2/tasks/*.md` (2 tasks: dneg-train 6 items x 8, dneg-held
   1 item x 6; polarity-aware brief of `authoring.DNEG_PROMPT`). Answers: `haiku/dneg_i2/answers/<task_id>.json`.
   (Not yet written: the orchestrator's GO is needed.)
1. Haiku answers the 2 authoring tasks.
2. `$PY -B families/T29/dneg_stage2.py`: `wording_problems()` (2/2 negation profile, polarity, G-SL), dedup, merged lexicon (v1 + redo2,
   `declare_dneg` first), unit tests, writes 2 independent G-LEX reads to `haiku/dneg_i2/glex_tasks/tasks/*.md` (answers in
   `glex_tasks/answers/`), `stage2_state.json`, `STAGE2_REPORT.json`.
3. Haiku answers the 2 G-LEX reads.
4. `$PY -B families/T29/dneg_stage3.py`: records the reads, admits 2/2 (+ `wording_problems` again), writes `pools/dneg/`
   (`wordings.jsonl`, `lexicon_merged.json`, `MANIFEST.json`, `quarantine.jsonl`), lists the wordings in `pilot_i2/G13_PENDING.txt`
   (G13-seed is a whole-block eval pass, not run here), then tests, determinism (PYTHONHASHSEED 1/2), the pilot into `pilot_i2/`
   (G5-H / G3-H task files, unanswered) and `G6_AT_6000.json`; report `pilot_i2/STAGE3_PILOT_STEPS.json`. Use `--no-pilot` to stop after
   the supplement. Exit 2 = fewer than 8 admitted training wordings.
- Not tested: `with_dneg` against a real `pools/dneg/` (would write into the real pools folder), and `pilot_steps` (about 25 min).
  The no-supplement path of `run_pilot_i2.py` works (`--dry-run --n 150`).
- G5-H must read >= 10 double-negation rows of the re-pilot (about 4% of yes/no rows at P_DNEG 0.12).

## gates_after
Not measured by the real runner. Last known (iteration 1): G6 choice c_card_without_question LR 0.3125 vs bar 0.2878 (fail);
G10 double_negation_share 0.0% vs >= 2% (fail until stage 3). pilot_i2/ holds no pilot output yet.
