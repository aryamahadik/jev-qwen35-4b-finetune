# T27 fix iteration 1: notes

Iteration 0 (`../pilot/`, untouched): G6, G7, G10 and spec 3.0 failed. This iteration was started by a Claude Code agent
(cut off by its usage limit) and finished here. Backups of the files as they were when this session started:
`../_backup_finish_i1/`; the v1.1 G0 is `../G0_SPEC.v1_1.md`.
Runner: `families/T27/run_pilot_i1.py` (registers the T27 loader from `run_pilot.py` at runtime; `pilot_loaders.py`
untouched). Pilot: `PILOT_REPORT.json`, `rows.jsonl`, `relations.jsonl`, `g5h/` (G5-H task files only; nothing answered).
G3-H: n/a (no Mode F row).

## Changes (generator / template only; no relabel, no bar loosened)

Earlier agent (kept):
- Cards (kit item 2): `CardItem` full / compact / short (70 / 15 / 15% of cards), `place_rules` (yes/no rules go to
  `row.card`), solver B reads rules through `cards.split_rules`, `defs_style` in meta. Mean tokens 1,010 -> 781 (bar <= 800).
- Polarity (kit item 3): `POLARITY_CHECK` and negatives on the plugin, `ctx_for` / render screen, authoring lint.
- Choice balance (kit item 1; closed set of 3 labels, no abstain option, so no abstain share to plan): verdict shares
  1/3 each (were 20 / 52 / 28); gold position from the row key (uniform); label-blind option order; mirrored
  antithetic card pairs; stratified relation draws; ch_next rows built with matched marginals (`_build_choice`).
- Tests updated, G0 raised to v1.2.

This session:
- `run_pilot_i1.py` (new): pilot_i1 runner; `--dry-run --n 6000 --no-g15 --g6-at-size` writes `G6_AT_6000.json`.
- `plugin.py`: `beyond_joint` (new). A continue / stop_ask row now draws its (task, action pair) jointly by iterative
  proportional fitting, so the task marginal, the action-pair marginal and the object / sibling near-miss classes
  equal the do_step rows' (exact to 1e-9). Before, a valid two-action pair was 94% do_step and the action marginals
  differed (chi2 237 over 28 actions; now 82, p = 0.009 with both requests of a row counted).
- `plugin.py`: `P_TWIN_CH` 0.64 / 0.54 / 0.08 -> 0.40 / 0.70 / 0.10 (stop_ask / do_step / continue). With the joint draw,
  stop_ask -> do_step twins became always possible and do_step reached 37%; twin labels are now 0.33 / 0.34 / 0.33.
- `G0_SPEC.md` (173 lines) and `G0_SHA256` re-synced to the plugin (question shares 19 / 10 / 7 / 4 / 60, complement 53%,
  yes/no twin 57%, ch_next twin rates, no TARGET twin, read-only never on ch_next, joint draw, per-class action bars).
- `test_plugin.py`: 4 tests brought to the v1.2 design (no TARGET twin by design; read_only floor 0.05; k_syn read from
  the question only; ch_next content test; action beyond-rate bar per row class). All 147 T27 tests pass.
- Determinism: `PYTHONHASHSEED=1` and `2` give identical `rows_sha256`
  2c57f109ff76394d0a5619b2120e27857b06fa5f60b476ed22a985e2ac8b7869 and `relations_sha256`
  5f40b984c53c76a778df07550a4088f3b8262a8ac8a11b1e0e531669795df297.

## gates_after

pilot_i1 (1,000 rows, 525 units):
- G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options: pass, 0/525 units failed (bar 100%).
- G6 (1,000 rows) FAIL, reported only (A43): yes/no best d_meta/gbt 0.5152 (bar <= 0.52, pass); choice best
  c_card_without_question/lr 0.3866 (bar <= 0.3533).
- G7 pass: 0 fails of 1,065 features (bar 0).
- G10 (1,000 rows) FAIL on one check: longest_option_gold_pp 2.35 (bar +-2; n = 538, SE ~2 pp). Others pass: yes_no_share
  46.2% (45-55), yes_rate 51.5% (50 +-2), yes_is_bad 52.8% (50 +-5), k_syn>=1 31.2% (>= 10%), k_syn>=2 10.2% (>= 2%),
  gold position chi2 pass.
- overlay pass: complement 46.8% of yes/no (>= 20%), non-syntactic 53.7% (>= 30%), twin 24.0% (20-25), equiv 7.4% (5-10),
  attack 5.3% (report).
- spec 3.0 pass: max tokens 1,077 (<= 2,000), mean 785.8 (<= 800), Mode F 0, deep 0, dev rows 0.
- G5-H pending: `g5h/tasks/T27-blind_read-75d872a6-00{0,1}.md`, `T27-blind_read-8d01fb9f-00{0,1}.md` (unanswered).

`G6_AT_6000.json` (A43, in memory, 6,001 rows = 2,865 yes/no + 3,135 choice; bars unchanged):
- G6 FAIL: yes/no best 0.5169 (d_meta/gbt; bar 0.52, pass); choice c_card_without_question/lr 0.4884 (bar 0.3533).
  That is the only failing cell. (Before the joint draw, the same run gave 0.5108.)
- G7 pass: 0 fails of 4,924 features.
- G10 FAIL on `yes_rate_cells` only (20 of 31 cells with n >= 50 outside 50 +-2 pp; enforced later by selection quotas,
  reported, not chased). longest_option_gold_pp -0.03, yes_rate 49.8%, double negation 9.9% (>= 2%), gold position pass.

## Open items

1. G6 choice view c (card + content without the question) is 0.488 at 6,000 rows (bar 0.353). Root cause: a do_step row
   asks only actions on the user's list, so its text holds one set of action phrases; a continue / stop_ask row holds the
   list plus a disjoint set of asked phrases. A bag-of-words reader sees the object words ("attached", "file",
   "two-step", "sign-in", "terms", "account") at about half the rate in do_step rows ("attached": 8% do_step vs 18% /
   20%). This follows from "within the list" vs "beyond it", so matching the action, task and pair frequencies (done)
   does not remove it. Options for the family lead, none applied (each changes G0): (a) a rigid design with equal phrase
   counts (do_step always a two-action task; beyond rows a one-action task plus one repeated asked action, per-action
   presence matched by a linear fit); (b) Haiku-authored non-asking mention lines that use each action's object words,
   added to do_step rows (new `info.<action>` forms: brief, 2/2 G-LEX admission, polarity admission through
   `c2_kit/polarity.py`; no task files written because (a) may suffice); (c) a spec ruling on whether G6 c applies to a rule
   that is a span match by construction.
2. G10 double-negation share is 9.9% (bar >= 2%): no Haiku authoring needed. The 3 pending `yn_dneg_beyond` wordings in
   `pools_v2` still have no reads (freeze_v2 state, unchanged).
3. G10 `yes_rate_cells` at 6,000 rows: 20 cells outside the band (selection quotas).
4. G10 longest-option within +-2 pp fails at 1,000 rows by noise (continue share 35.7%); -0.03 pp at 6,000 rows.
5. read_only_task fell to ~7% of bases (G0 target ~20%, report-only): a read-only task can never be do_step, so it is
   excluded from ch_next; yes/no rows keep it (~15% of yes/no rows).
6. G5-H blind reads and the A43 selection are for the orchestrator.
