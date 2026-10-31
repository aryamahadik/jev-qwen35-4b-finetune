# T06 fix iteration 2 (the last one, A43 c): notes (pilot_i2)

Backups: `_backup_i2/` (`*.bak` for plugin, solver_b, run_pilot*, test_plugin; G0_SPEC.md, G0_SPEC_v3.md). `pilot/` and `pilot_i1/` untouched.
No label relabelled, no bar loosened, no pool file touched, no kit file edited.

## Changes
1. **G3-H item describe** (`plugin.py`): `ITEM_DESCRIBE_I2` = "the name of the goods the person bought, as written, without any article or
   possessive before it (leave out the, my, a, an)". G0 v2 section 4 item 2 still has mode F write "the"/"my" before ITEM; the generator's
   item is the bare name, so the schema now says to leave the article out. `c2_kit/g3h.py` and the 98% bar are unchanged. The pool-era G3-H task
   files carry the authored describe, so `conftest.py` / `freeze_v2.authored_g0()` swap `ITEM_DESCRIBE_AUTHORED` in for the pool-era rebuilds.
2. **ch_rule gold position by construction** (S10, G0 v4): k comes from the record's coarse facts; the shown options sit in the key's fixed
   label-blind order (a function of key + display only, so twins show the identical list: G-TW compares lists); the kit ChoicePlan
   (`plan_choice(key, closed=n_rules, abstain=True).pos`) gives the gold position (uniform over k by construction); the target is the option AT that
   position. `_realize_rule(..., key)`, `T06Plugin.rule_order`. Twins, equiv and attack re-renders reuse the base's list.
3. **G0 v4**: `G0_SPEC_v4.md` (189 lines), sha256 `84b81c33c293969c325d88aafb0fa5d4e172d3ccdd4607964884e35e038063d7`, pinned in `plugin.G0_LITE` / `G0_SHA256`
   and `test_plugin.py` (v3 sha 2d97b12f..., v2 sha stays `G0_SHA256_AUTHORED`). Changes: S10, S22, new section 2b (partner cards), section 9.
4. **A42 item 5, all three done as G4 metamorphic relations** (checked by solver A, solver B and every row gate on the partner; never emitted, so G6/G10 rows are unchanged):
   - **rule-swap**: same facts, the notice rule flipped (the posted notice replaces the statute: only a refund it promises is owed); gold flips where the statute alone gave the refund. Partner card `swap`.
   - **rule-deleted**: the withdrawal rule (and its exclusions) removed from the card; the gold becomes no refund (yes/no) or the option "none" (ch_rule) where withdrawal alone gave the refund. A right the card does not state does not exist (closed-world sentence). Chosen over deleting the notice rule because that would leave a posted promise ambiguous.
   - **nonce vocabulary**: customer, store, item and jurisdiction names replaced by invented words; answer unchanged. Limit: the rule and goods vocabulary of the cards is not made nonce (that needs new wordings); this is the entity-level nonce variant only.
   - Mechanism: `spec.structure["rule"]` in {std, swap, nowd}; `card_template(style, variant, rule)`, `solve_a` (rule-aware), `canonical` (`rule`, `n_withdraw` None when deleted), `_grants(no_withdraw=)`, `_rule_relations`; `solver_b._read_card` reads the partner cards with its own copy and returns the mode. Proposed only where the gold really flips. Measured on 1,000 base specs (`test_metamorphic_relations_keep_the_answer`): swap 169 (16.9%), deleted 89 (8.9%), nonce 117 (11.7%) of units; bars 10 / 5 / 5%.
   - Not done: no emitted twin rows of these kinds (G4 only, as the brief asks); no Haiku wordings.

## Tests / determinism
`pytest families/T06`: test_plugin 50 passed (test 6 -> 9 G4 notes), the rest 104 passed. PYTHONHASHSEED 0 and 4242 (1,000 rows) give identical
rows_sha256 `c6af7b858760811392b9e387ac6be4de6c134f15f46292ee842f38d2fecbc4a3`, relations_sha256 `6e67f0c0fe29ad0646c906aa6dac398b96c95720170cebaa4bfed2db89291f95`;
the written `pilot_i2/rows.jsonl` has the same sha.

## gates_after
1,000-row pilot (`PILOT_REPORT.json`): G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options all pass (0/601 units failed); G7 pass; overlay pass (twin 0.214, equiv 0.057);
spec 3.0 pass (mean tokens 776.2, max 1,019). Report cells above the bar at 1,000 rows (sampling noise, SE about 2 pp): G6 yes_no d_meta gbt 0.5471 (bar 0.52),
choice d_meta gbt 0.3159 (bar 0.3263, within it); G10 gold-is-longest -2.29 pp (bar +-2; -0.69 at 6,000). A43 permutation null for the 1,000-row yes_no cell: not run (yes/no rows are untouched by this iteration; the 6,000-row result is the binding G6).
6,000 rows, G15 off, seed base 900000 (`G6_AT_6000.json`):
- G6 **pass**: yes_no n=3196 best d_meta/gbt 0.516 (bar 0.520); choice n=2806 best a_question/lr 0.3247 (bar 0.3263).
- G7 pass (0 of 3,521).
- G10: gold_position pass (was p=0.0096 at k=3), gold_rank, abstain_wrong, gold-is-longest -0.69 pp pass; only `yes_rate_cells` fails (report-only, selection quotas).
Pending (Haiku): G3-H and G5-H, task files regenerated in `pilot_i2/g3h/`, `pilot_i2/g5h/` (not answered). G5-H needs a re-read because the ch_rule option order changed.
No Haiku stage scripts (no wordings needed).

## Commands (from lean/c2_build)
`../../.venv/bin/python -B families/T06/run_pilot_i2.py` (pilot); `... --dry-run --n 6000 --no-g15 --g6-json families/T06/pilot_i2/G6_AT_6000.json` (G6 at 6,000).
