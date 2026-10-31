# T26 fix iteration 1: notes

Iteration 0 (`../pilot/`, untouched) failed G6, G7, G10 and spec 3.0. Fix iteration 1 is generator/template only: no label
changed, no bar loosened, no G0 target lowered. Backups: `../_backup_i1b/` (plugin, G0, solver B, authoring_ingest,
test_plugin as they stood when this session started; `plugin_after_f4.py` = after the number budget and the yes/no twin thinning, before the G0 re-pin); the v1.1 originals are
`../G0_SPEC.v1_1.md` and `pilot_runs/T26_i1_work/*_v1_1.*.bak`. Work files: `pilot_runs/T26_i1_work/`.

## Changes

Done by the earlier (cut-off) agent, kept as is:
1. Kit changes adopted (kit_instructions.txt): compact cards (3 styles numbered/compact/short, rules in `row.card` on yes/no
   rows via `cards.place_rules`, solver B reads `cards.split_rules`); wording polarity (`POLARITY_CHECK`, `ctx_for`; all 22
   `yn_dneg_apply` wordings pass the rule, none is quarantined, so no Haiku task is needed); exact abstain share through an
   own slot schedule (G0 S28): ch_verdict triples apply/reject/escalate, ch_failing runs of n+1, so the abstain option is gold
   on exactly 1/k. The kit's `plan_choice` was not used (closed sets with twins must keep one option list).
2. Exact question-form shares per aligned block, trap-share tuning (escalate 0.08, failing weights), twin thinning by
   transition on choice rows, complement/equiv/inv hashed per slot group, tone-balanced skin dealing (G0 v1.2).

Done in this session:
3. **G6 d_meta (choice), by construction.** Cause (5,000 rows: choice d_meta 0.387 and 0.353 against chance 0.31): the
   metadata features `n_numbers`, `mag_mean`, `len_state` and `deep` carried the outcome. An unverifiable record prints no
   value, so the count of numbers fell with the outcome (apply 10.3 > reject 9.4 > escalate 8.5), and `deep` (4 checks with a
   failed and an unverifiable check) forces reject.
   - Number budget (G0 S29): every packet ends its header with one inert line "other open requests: {PAD}" (derived id slot
     `{prefix}-{ddd}-{ddd}-...`). The packet always prints the same number of numbers: the most its shown checks can print
     (NUM_CAP) plus a seeded 1-3. The budget depends on the seed and the shown checks only, never on the gold. Measured on
     3,000 rows: numbers per choice row 14.4 / 13.9 / 14.0 for apply / escalate / reject (sd 4.6). Solver B reads the line
     and ignores it; a twin keeps the base's pad (G-TW).
   - Depth (G0 S30): choice base rows are never deep (`_plan_outcome(shallow=True)`); yes/no rows keep S15.
4. **G6 d_meta (yes/no), by construction.** Cause: minimal-edit twins of yes/no rows were 37-67% yes by form (only some answer
   flips exist), so the question form alone predicted the answer (0.528 at 3,085 rows; d_meta 0.5203 at one probe, over the
   bar). Twins of the plentiful direction are thinned to the supply of the other (`YN_TWIN_KEEP`, supplies measured on 6,000
   seeds per training sampler); attempt rates `P_TWIN_Q` raised in step. Per-form yes rate of the rows now 0.48-0.51; twin
   share 0.214-0.219.
5. **G10 gold position** (chi-square p 0.0053 at k=5 at 1,000 rows; 0.0063 at 6,000): the gold position is scheduled (G0 S28):
   a second, independent permutation per triple/run; the option list is rotated so the slot's base outcome sits at the
   scheduled position (`_rotate_to`; twin and format partners of a seed keep the same list).
6. G0_SPEC.md v1.2 completed and re-pinned (`G0_SHA256 = a9839fa9...`; the v1.1 text the pools were authored under stays
   byte-exact in `G0_SPEC.v1_1.md` and is `G0_SHA256_AUTHORED`): S13, S15, S20, S24, S25, S27 updated, S28-S30 and section 7 R3
   added. `author_tasks.py`, `haiku/redo2/build_redo2.py`, `haiku/redo3/build_redo3.py`, `haiku/redo3/build_reads.py`,
   `freeze_v2.py`, `record_freeze.py` now point at the authored v1.1 sha / text, so the frozen pool artefacts still rebuild
   byte-identically (freeze tests pass).
7. Tests added to `test_plugin.py`: number budget independent of the outcome, choice rows never deep, exact gold positions.
8. `run_pilot_i1.py` (registers the T26 loader at runtime; `pilot_loaders.py` not edited; `--g6-at-size` writes the A43 file).

## gates_after (pilot_i1: 1,001 rows, seed base 900,000, G15 on)

- pilot_size pass: 1,001 rows (588 units); bar >= 1,000
- G2 pass: 0/588 failed; bar 100%
- G3 pass: 0/588 failed; bar 100%
- G4 pass: 0/588 failed; bar >= 3 relations, 100%
- G-SL pass: 0/588 failed; bar 100%
- G-LEX pass: 0/588 failed; bar every form admitted 2/2
- G-TW pass: 0/588 failed; bar 100%
- G15 pass: 0/588 failed; bar 100%
- schema, options pass: 0 failed; bar every row valid, every wrong option from a named model
- G6 pass (1,001 rows): yes/no n=518 best 0.500 (chance 0.5), choice n=483 best 0.288 (chance 0.3085); bar chance + 2 pp
- G6 at 6,000 rows (A43; `G6_AT_6000.json`, in memory, G15 off) pass: yes/no n=3,125 best 0.5059, choice n=2,875 best 0.3277 (c_card_without_question/lr) against chance 0.3118 (limit 0.3318); bar chance + 2 pp
- G6 at another seed base (33,000,000, 6,000 rows, not a pilot file) pass: yes/no d_meta 0.5068, choice d_meta 0.3254 (limit 0.3324)
- G7 pass: 0 fails of 1,423 features (raw, card-adjusted, choice); bar 0 at Bonferroni; also pass at 6,000 rows
- G10 pass at 1,001 rows: yes/no share 0.5175 (45-55), yes rate 0.50 (50 +/- 2), yes_rate_cells none with >= 50 rows, yes-is-bad 0.4614 (45-55; thin), syntactic negation 0.220 (>= 10%), double negation 0.0676 (>= 2%), gold position p 0.81 / 0.96 / 0.92 (> 0.01), gold-is-longest -1.86 pp (+/- 2; thin), abstain wrong 0.706 (>= 50%), attack x label p 1.0
- G10 at 6,000 rows FAIL on `yes_rate_cells` only: 14 wording x negation cells (n = 52-85) lie outside 50 +/- 2 pp (0.42-0.58). Reported, not chased (selection quotas later). Every other G10 check passes at 6,000 rows (gold position p >= 0.60 at the other base)
- overlay pass: complement 0.309 of yes/no (>= 20), non-syntactic 0.625 of pairs (>= 30), twins 0.2188 (20-25), equiv 0.0649 (5-10), unit size max 3
- spec 3.0 pass: max tokens 1,149 (<= 2,000), mean tokens 792.9 (<= 800; thin; 787.5 at 6,000 rows), Mode F 0.189 (<= 25%), deep 0.024 (<= 10%), dev-only rows 0
- determinism pass: rows_sha256 `359226d82d737660...`, relations_sha256 `ab8ea80e778064f6...` identical under PYTHONHASHSEED 3 (written run), 99 and 2024 (dry runs)
- G3-H, G5-H pending: task files regenerated in `g3h/`, `g5h/` (4 + 4 tasks; 32 `yn_dneg_apply` rows in the pilot); not answered

## Open items

- G3-H and G5-H need the Haiku reads (orchestrator). No authoring or admission task files are needed: no wording was quarantined.
- G10 `yes_rate_cells` at 6,000 rows fails (above): left to the later selection quotas.
- Thin margins at pilot size: mean tokens 792.9 against 800 (the pad adds about 20 tokens; fewer cap slots or shorter groups would give room), yes-is-bad 0.4614 against 45%, gold-is-longest -1.86 pp against +/- 2 (-0.8 to -0.9 at 5-6k rows).
- `choiceplan.plan_report` (kit item 1e) still lists "length rank n2/n3" at 5,000-6,000 rows although G10 gold_rank and gold-is-longest pass. Cause not investigated.
- G6 sampling noise is about 0.9 pp per cell against a 2 pp bar. Before the yes/no twin fix one probe reached 0.5203; after the fixes the two probes at 6,000 rows stay within +1.6 pp.
- The pad line is a new visible packet element (G0 S29). The pools were not re-authored (program text), but the extract reads (G3-H) will see it.
