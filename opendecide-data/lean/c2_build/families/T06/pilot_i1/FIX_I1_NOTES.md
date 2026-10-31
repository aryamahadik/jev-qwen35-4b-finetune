# T06 fix iteration 1: notes (pilot_i1)

Iteration 0 (`../pilot/`, untouched) failed G6 (yes/no d_meta gbt 0.551; choice c_card lr 0.367), G10 (gold-is-longest +2.87 pp) and
spec 3.0 (mean tokens 926.8). Generator/template fixes only; no label relabelled, no bar or G0 target lowered, no pool file touched.
A first agent (cut off by a usage limit) did the card, polarity, ch_rule display and ch_end plan work (its scratch probes:
`pilot_runs/T06_i1_scratch/`); this session finished it. State at resume is in `_backup_i1_resume/` (`*.bak`).

## changes
Files: `plugin.py`, `solver_b.py`, `G0_SPEC_v3.md` (new, frozen), `run_pilot_i1.py` (new), `conftest.py` (new), `test_plugin.py`,
`test_freeze_v2.py`, `freeze_v2.py`, `haiku_author.py`, `pool_freeze.py` (G0 pin only). `G0_SPEC.md` (v2) is unchanged.

1. **Compact cards (kit item 2), spec 3.0.** Rules go in `row.card` on yes/no rows (`cards.place_rules`), in the instructions on choice
   rows. Three variants per training row from the row key: full 25% (the frozen v2 text) / compact 60% / short 15% (S5: full only);
   `CardSpec.problems() == []` (tested). `meta.defs_style`. Solver B reads rules with `cards.split_rules` and its own card copy.
2. **ch_rule (kit item 1: abstain share, option balance).** v2 showed all four keys, drew periods before the target, so the coarse facts
   (reason, goods, notice scope) predicted the key. Now: display = the rules the coarse facts leave open (>= 2) + "none"; target
   uniform over the display before any date (every option, "none" included, gold on 1/k); windows label-first: the target's window ends
   on a day drawn from 9..34 after possession, others 1-3 days earlier, each period = its end minus its anchor lag; request in the
   last 4 days of the target's window (first 4 after the last window for "none"). Last measured leak: with periods from one pool the
   gold was the largest period on 96% of rows and the printed day counts alone gave the card view +3 pp (LR 0.345 vs 0.314); now 0.313.
   Twins that move the gold onto "none" are thinned per k (`TWIN_NONE_KEEP` 0.22 at k=3, 0.05 at k=4): "none" is 0.33 / 0.24 of
   emitted rows at k=3 / 4 (was 0.31 / 0.25), gold-is-longest -0.4 pp (ch_rule).
3. **ch_end.** Kit `ChoicePlan` (k 3-4, position, sorted rank). An option equal to a date the record prints (a verbatim cue: gold was
   that option on 55% of such rows) is never used: error models give no output for a printed date (G-TW metamorphic fix), and
   `_end_options` still redraws the structure if one slips through.
4. **Yes/no metadata leak (G6 d_meta).** (a) Printed day counts always digits: the word form exists only for 0..20, so the numeral
   count said how late the request was (n_numbers x qform 0.54). (b) Request day within 4 days of a window end for both labels, so the
   counts' magnitude is the same in both classes (refund rate 0.35 in the top mean-magnitude decile before). Trap tags changed (below).
5. **Polarity (kit item 3).** `POLARITY_CHECK`, `POLARITY_NEGATIVES`, `ctx_for` screen, P4 off. Frozen pool: 0 wordings quarantined;
   double-negation share 6.6% >= 2%, so no Haiku authoring is needed (no task files written).
6. **G0 v3** (`G0_SPEC_v3.md`, 172 lines, sha256 2d97b12f21fe276462f56872fe82137e46f7656c92aa293845e491debca39427; plugin
   `G0_LITE`/`G0_SHA256`). v2 sha 4f6b322a... = `G0_SHA256_AUTHORED`, the text pools_v2 and the Haiku builders were authored against
   (freeze_v2, haiku_author, pool_freeze, test_freeze_v2 pin it; `conftest.py` rebuilds the redo builders under it).
7. `run_pilot_i1.py` registers the T06 loader at runtime (reuses `run_pilot._t06`; `pilot_loaders.py` untouched); `--g6-json` writes
   the g6_at_size fields from an in-memory run.

Tests: `c2_build/families/T06` all pass (test_plugin 50, the rest 104; both run after the final G0 v3 sha).
Test edits: G0 v3 card parse, hand case ("nothing grants"), ch_rule gold uniform per display, trap bands (order 31%, boundary 48%
measured; spec 3.13 lower bounds kept), abstain option is no model's output, five error models (`ignore_exception`,
`t06_absolute_exception`, `t06_ignore_notice`, `t06_notice_any_reason`, `t06_sign_wins`) now only ever give "none" so never an option,
pools_v2 MANIFEST compared without its producer hashes (plugin.py etc. changed; every pool file still byte-identical).

## gates_after
Determinism: PYTHONHASHSEED 0 and 4242 give identical rows_sha256 bc8207193f4a965d... and relations_sha256 cb9e9d74d5c39776...
(1,000 rows; the written `pilot_i1/rows.jsonl` has the same sha).

1,000-row pilot (`PILOT_REPORT.json`):
- G2 pass 0/603 units; G3 pass; G4 pass; G-SL pass; G-LEX pass; G-TW pass; G15 pass; schema pass; options pass (bar 100% each)
- G6 FAIL: yes_no n=542 best d_meta/gbt 0.5387 (bar 0.52); choice n=458 best a_question/gbt 0.3406 (bar 0.3270). Sampling noise
  (SE about 2 pp at these n); same builds at 6,000 rows pass (next block). Reported, not binding (A43).
- G7 pass (0 fails of 1,201 features)
- G10 FAIL on gold-is-longest -3.53 pp (bar +-2; SE about 2 pp at n=458; -0.71 at 6,000). Passing: yes_no_share 0.542, yes_rate 0.485,
  yes_is_bad 0.511, syntactic negation 0.334 (bar >= 0.10), double negation 0.066 (bar >= 0.02), gold_position, gold_rank, abstain_wrong
  0.71 (bar >= 0.5), attack_x_label
- overlay pass (twin 0.211, complement 0.399, equiv 0.057); spec 3.0 pass: mean tokens 775.9 (bar <= 800), max 1,019 (bar <= 2,000)
- G3-H and G5-H pending (task files regenerated in `g3h/`, `g5h/`; not answered)

6,000 rows, G15 off (`G6_AT_6000.json`, A43 size):
- G6 PASS: yes_no n=3202 best c_card gbt 0.5116 (bar 0.5200); choice n=2799 best b_options gbt 0.3162 (bar 0.3265)
- G7 pass (0 of 3,525)
- G10 FAIL, two checks: yes_rate_cells (66 cells, 36 with >= 50 rows; reported, enforced later by selection quotas, not chased);
  gold_position chi-square p = 0.0096 at k=3 [693,617,588] and 0.0157 at k=4 (bar p > 0.01). Passing: gold-is-longest -0.71 pp,
  gold_rank, abstain_wrong, yes_rate 0.492, yes_is_bad 0.507, negation shares as above
- spec 3.0 pass: mean tokens 778.5, max 1,054

## open items
- G10 gold_position at 6,000 rows is borderline and looks like chance, not a leak: base ch_rule gold positions over 10,000 specs (S1-S4) on
  three seed bases give p = 0.07 / 0.43, 0.08 / 0.94, 0.93 / 0.39 (k = 3 / 4); the pilot's counts also include equiv and attack re-renders
  of the same option set (they inflate chi-square). The previous 6,000-row run (before the printed-date model filter) passed it.
  If the verdict wants it clean: adopt `plan_choice(closed=len(display), abstain=True)` for the ch_rule position (changes S10 text, a
  new G0 sha) or enforce position in the selection quotas with yes_rate_cells.
- yes_rate_cells at 6,000 rows: selection quotas (as instructed).
- The 1,000-row G6 / G10 results fail on sampling noise; the binding verdict is the 6,000-row run.
- G3-H and G5-H must be re-read (cards, ch_rule options, ch_end options changed). Haiku wordings: none needed.
- Trap shares moved (G0 v3 section 3, measured on 12,000 specs): boundary day 48%, order date 31%, stricter 27%, conditional 16%,
  generous 16% (all above their spec 3.13 targets). Held-out S5 ch_rule periods are no longer a held-out value set (ends 35..45 days).
- pools_v2 `MANIFEST.json` still records the producer hashes of the pre-fix plugin.py / freeze_v2.py; the pool files are untouched and
  verify. A re-freeze would rewrite it.
