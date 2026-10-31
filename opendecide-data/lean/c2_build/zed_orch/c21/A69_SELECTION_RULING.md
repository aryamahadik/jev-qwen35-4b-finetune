> **Ruling A69 (DRAFT 17 Oct 2026 ~17:10 UTC; orchestrator, Opus; PRE-RESULT program fix for G9 selection (spec 6.4 step 9): A42-D 6 trap weighting, plus one drop-only repair step for the binding A49 (c), spec 3.0 / 5.2 and A42-D 1.5 checks. Written before any C2 selection record exists (c2_build/crowd_c2/ holds only crowd_tasks_c2.json) and before any selection, scratch or real, has run under it. No gate, bar, band, cap, target, seed or waiver is loosened. Nothing is relabelled. Rows are only removed, never added.)**
>
> **Why.** A42-D 6 is adopted, but `c2_select.py` (sha256 70cde02dfe21a2c1…) never reads `meta.opt_err`, so G9 would run the pre-A42-D selection. A49 (c) makes the balance checks bind on the selected rows. Yet the only selection-side step, `a49c.swap_balance` (W6 program code, never ruled), moves only three things: yes rate, yes/no share and twin share. Any other failing check makes `mix_c2 --final` refuse. In the provisional dry run (`_dryrun_20261017/partial_checks.json`) those were: T26 token mean 807.7 and longest option −3.26 pp; T06 +3.36, T12 −3.55 and T24 +3.05 longest option; T15 equiv 4.56%; a T01 card with 67 rows. As in A66, a tool that implements adopted text is a PROGRAM FIX. It is recorded here because A37 (e) says "Bins and selection are unchanged".
>
> **Adopted text implemented (verbatim).**
> - A42-D 6, "Trap selection, for the 17 existing program families only (changes A37 (e) "Bins and selection are unchanged")":
>   - 6.2: "A relation unit is trap-flagged if C1 (the G9 C1-only read, A18.2 readout) puts ≥ 0.25 probability on any tagged trap option."
>   - 6.3: "Trap-flagged units go to the hard bin at 2 × selection weight against other hard-bin units. This is a selection weight, never a repeated row (G12). It stays inside the spec 5.2 caps (hard ≤ 30%, easy ≤ 25%). If the flagged units would exceed 30%, the weight is scaled down until it fits."
>   - 6.4: "Trap types C1 picks most are favoured, ordered by the C1 pick rate on the family's own candidates. … The dev pick rates are priors only … No trap type exceeds 35% of a family's trap-flagged units."
>   - 6.5: "Units stay whole. G10, G11, the 2,400-row family cap and the crowd chi-square check still apply. Units without a corruption tag, and all T40-T45 units, are selected as before."
> - A49 (c): "Balance checks bind on the selected rows. … asserted per family on the rows the mix selects (`mix_c2.py`); at candidate stage they are report-only."
> - A49 (f): "C1 reads that are routing or selection signals (crowd bins, trap flags, …)"; "C1 output is never a label or a target."
> - Spec 5.3: "Missing shares lower the total; they are never refilled with lower-quality rows."
> - A34 (e): a family "short of its base target ONLY because G13 removed units enters with its realised rows, when every other selection check passes".
> - A34 (f)(ii): "A wording cell outside its E2/G10 band is fixed by seeded down-sampling of the majority label inside that cell (whole units; rows only removed, never added or relabelled)."
> - A42-D 1.5: "those rows are scaled down (seeded, whole units …). No cap is raised."
>
> **(a) Scope.**
> - Covered: the 15 program families present (T01 T06 T07 T12 T15 T23 T24 T25 T26 T28 T29 T30 T31 T32 T33). Every one carries `meta.opt_err` on every choice row (option text → list of error-model tags; gold is never tagged). The C2 odds analysis says T01 rows have no tags; that is out of date.
> - Not covered: carry pools (F4 F5 F6 F11), blocks (GB GW MD RTW SB5 I10), DI blocks and T40-T46. They are selected exactly as now, with no trap weighting and no repair. Their A49 (c) checks stay report-only.
>
> **(b) Trap weighting (A42-D 6), fixed now. Seed 20261013, key = family id.**
> - **(b1) Flag (6.2).** The flag is computed on the post-G13 pool (A34 b). A unit is flagged if any choice row in it has an option whose tag list is not empty and on which C1's G9 probability is ≥ 0.25. That probability comes from the same label set p_g uses. A row dropped by G13 provides no statistic.
> - **(b2) Pick rate and type order (6.4).**
>   - For each tag: pick rate = (rows whose C1 argmax option carries the tag) ÷ (rows that show an option carrying it), on the post-G13 pool.
>   - Order: rate descending, then rows shown descending, then tag name.
>   - The dev pick rates are reported, not used. No mapping from their names to family tags is pre-registered, and making one now would be a new judgment.
>   - A unit's trap type is its highest-ranked tag among the options C1 put ≥ 0.25 on, so each unit has one type. Several tags on one option name the same wrong answer, so counting a unit once per tag would make shares add to more than 100%. The per-tag count is reported.
> - **(b3) Bins (6.3, "go to the hard bin").** Every row of a treated unit is binned hard. All other rows keep their p_g bin (easy if p_g > 0.97, hard if p_g ≤ 0.30). The record keeps both maps: difficulty_bin is the A42-D 6 bin and pg_bin is the p_g bin.
> - **(b4) Weight (6.3) and favouring (6.4).**
>   - crowd_select's order key h = h64(seed, key, "order", first row id) becomes an exponential race: t = −ln(1 − U)/w, with U = (h + 0.5)/2^64. w = 2 for a treated unit and 1 for any other unit.
>   - Effect: untreated units keep their exact relative order, and a treated unit comes before an untreated one with odds 2:1.
>   - Favouring: the positions that treated units hold in this order are then refilled with the treated units sorted by (type rank, own t).
> - **(b5) Selection.** crowd_select.select runs unchanged: budgets (easy ≤ 25%, hard ≤ 30% of target), label-balanced quotas, A27 (c) reflow, the cap pass and the chi-square. It runs on these bins and this order. In practice this is a verbatim c2_build copy of crowd_select.select with only those two inputs injected; with no unit treated it gives byte-identical results.
> - **(b6) Type cap (6.4).**
>   - The cap is read as a cap on the units that receive the treatment.
>   - After each selection: if a type holds more than 35% of the N selected treated units, the ceil((c − 0.35·N)/0.65) lowest-priority selected treated units of that type lose the treatment. They return to their p_g bin with weight 1 and are "selected as before" (6.5). The selection is then re-run. This repeats until no type is above 35%; the treated set only shrinks, so it ends.
>   - Rejected reading: count every 6.2-flagged unit in the selection. That would remove units the A37 (e) selection keeps, and so work against the trap type C1 picks most, against the first sentences of 6.3 and 6.4. It is reported only.
> - **(b7) "Scaled down until it fits" (6.3).** Treated rows are hard rows, and the hard budget plus the cap pass keep hard ≤ 30% of the realised rows, so this holds by construction. The tool asserts it and records weight 2.0, scaled = false. If the assert ever fails, w is stepped down by 0.1, as far as 1.0; if it still fails, the run refuses.
> - **(b8)** Units stay whole and no row is repeated.
>
> **(c) Swap step (the existing a49c.swap_balance; recorded here, not widened).**
> - Same objective as now (yes rate, yes/no share, twin share). Whole units only.
> - A partner must have the same A42-D 6 bin, the same row count, the same treatment and the same trap type, and must not be an easy-thinned unit.
> - New: a swap is kept only if no check that passed before it fails after it.
>
> **(d) Repair step (drop-only, seeded, whole-unit, same-bin).** It runs after (c), on each family in (a), only when a check in (d1) fails.
> - **(d1) Checks it may repair, in this fixed order.** Each is evaluated by the function that binds it, at its adopted bar.
>   1. Rows per card ≤ 64.
>   2. Token mean ≤ 800 (pinned tokenizer, as mix_c2).
>   3. Free-form share ≤ 25% (T07 and T32 ≤ 40%).
>   4. Yes/no share.
>   5. Yes rate 50 ± 2.
>   6. G10 yes-rate cells (the mixer rule).
>   7. Yes-is-bad 50 ± 5.
>   8. Minimal-edit twins 20-25%.
>   9. Equiv twins 5-10%.
>   10. Complement ≥ 20% of yes/no.
>   11. Non-syntactic ≥ 30% of pairs.
>   12. Longest option within ± 2 pp.
>   13. Abstain wrong ≥ 50%.
>   14. Gold position cells (A49 b).
>   15. Gold rank cells (A49 b).
>   16. The G9 label × bin chi-square (p > 0.01), on both bin maps.
>
>   The functions are a49c.family_checks, mix_c2.cap_checks, mixer.g10_checks and crowd_select.selection_report.
>   The difficulty caps (hard ≤ 30% on the A42-D 6 bins; easy ≤ 25% on both maps) are kept only by the cap pass in (d2).
> - **(d2) A move, and what "same-bin" means.** A move drops one selected unit u. crowd_select's own cap pass then runs: it sheds units that hold hard (or easy) rows and no medium rows, from the end of the priority order, while hard is above 30% (or easy above 25%). No row ever changes bin, and the bin shares stay inside their caps.
> - **(d3) Order (seeded; no new random draw).** Candidates are the selected units in reverse (b4) priority, lowest first.
> - **(d4) Admissible move.** All of these must hold:
>   - Removing u alone strictly lowers the failing check's distance, and so does the whole move.
>   - No check that passes before the move fails after it. This covers every (d1) check, the difficulty caps, the 35% type cap and G11 (no skin or wording above 2% of the selected rows).
>   - No failing check's distance rises.
>   - Total repair loss stays ≤ 25% of the pre-repair rows (a new limit, stricter only).
>
>   The first admissible candidate is dropped, and this repeats until the check passes or no candidate is admissible. Then the next check is repaired. There are at most 3 passes over the list.
> - **(d5)** The repair may stop below target. Nothing refills: after it, no fill, reflow, swap or re-selection runs.
> - **(d6)** Every move is recorded: check, unit first id, rows, bins, treated or not, companion drops, and the distances.
>
> **(e) What the repair may and may not do.**
> - It may only remove whole selected units as in (d), and record them.
> - It may not:
>   - add a unit, except by a (c) swap;
>   - edit any row, label, option, gold, bin, p_g, tag, relation, candidates file, manifest or crowd label;
>   - relabel;
>   - touch replay, any G13 drop list, the A68 split, a target, the seed, or any bar or band;
>   - read anything except candidates, relations, manifests, C1 crowd labels, the binding G13 logs and the pinned tokenizer. That rules out any Jev output, sealed file, dev read or G-proxy;
>   - be run twice with different settings;
>   - have any constant here changed after a scratch or real selection has been seen. Such a change needs its own ruling, disclosed as post-result.
>
> **(f) Admission.**
> - The select record carries the A42-D 6 and A69 blocks. report.checks gains four entries: a49c_and_caps (every (d1) check passes), the chi-square on pg bins, easy ≤ 25% on pg bins, and type cap ≤ 35%. pass needs all of them.
> - mix_c2 changes:
>   - (i) It refuses a program-family record that lacks these blocks, a scratch record, or tool shas other than those pinned in the A69 addendum.
>   - (ii) It accepts a record that is short of target, as under A34 (e), only when total_eq_target is the only failed check, rows_pre_repair − rows_dropped equals the rows selected, rows_dropped ≤ 25% of rows_pre_repair, and the pre-repair selection was at target or A34 (e) / an upper-bound target applies.
>   - (iii) A family whose record fails is left out (spec 5.3). Losing an agent-core family this way means stop and report (A62 c).
>   - (iv) Re-selection (agent-tier cap, budget trim) uses the recorded bins, treatment and type order, and re-runs (b6), (c) and (d).
>   - (v) easy ≤ 25% is also checked on meta.pg_bin.
>   - (vi) a49c_assert and cap_checks on the mixed rows are unchanged and still binding.
>
> **(g) Why nothing is loosened.**
> - Every bar, band, cap and target is unchanged. Each still binds on the final selected rows, through the same function at the same bar.
> - A failing selection can only pass by losing rows. The rows that train are a subset of rows that passed every full-generation gate.
> - Removal only: no refill and no relabel. This follows spec 5.3, A34 (c), (e) and (f)(ii), and A42-D 1.2 and 1.5.
> - The trap weighting stays inside the caps:
>   - Treated rows count as hard, so the hard cap is stricter than on p_g bins.
>   - The one direction that re-binning could make looser is covered: easy is checked on both maps, and so is the G9 chi-square.
> - Seeding: no new seed and no seed search. Every constant comes from adopted text. The things A69 adds — the 25% loss limit, the "no check gets worse" rule and the swap guard — only restrict.
> - Signals: only the C1 crowd read (A49 f) and program metadata. No Jev output, sealed file, dev read or G-proxy.
> - Being short of target is accepted only for exactly recorded repair drops. These stay unchanged:
>   - the 50,000-row floor;
>   - spec 5.3's minimum (≥ 5 of 6 agent core, ≥ 10 program families);
>   - the A62 (c) stop;
>   - the A61 (e) caps;
>   - A68.
> - Fewer new rows mean less replay (floor 1.5×) and less money. A42-D 9 and 10, spec 3.18, 7.x and 9.x are untouched.
>
> **(h) Disclosure.**
> - The readings in (b2), (b6) and (d) were chosen after a counts-only scan of the tags and the C1 ≥ 0.25 flags on the pre-G13 candidates. No selection was run and no gate result was seen.
> - Flagged units / units:
>   - T01 771/1,870; T06 300/1,039; T07 92/898; T12 165/903; T15 76/1,104;
>   - T23 85/846; T24 142/686; T25 62/714; T26 173/1,469; T28 395/2,462;
>   - T29 173/2,066; T30 240/1,544; T31 313/1,127; T32 186/730; T33 357/2,616.
> - Largest one-type share among flagged units (before the cap): T25 81%, T30 80%, T26 66%, T23 57%, T31 51%. Counted per tag, the largest is T30 at 94%, which would make the cap impossible to meet.
>
> **(i) Order of work.**
> 1. Sonnet writes the code and CPU tests to the A69 builder spec.
> 2. A Sonnet skeptic reviews the diff against this text.
> 3. The orchestrator appends an A69 addendum with the sha256s of c2_select.py, a49c.py and mix_c2.py.
> 4. A scratch dry selection runs only under c2_build/staged/p2_select/ (never crowd_c2/ or data/). Its counts are reported, not tuned on.
> 5. The real select runs only on the binding capture-batch G13 logs.
>
> **(j) GO #1** states, per family: treated units, rows dropped by the repair and by which check, short_by, and any family left out under (f)(iii).

## spec_for_builders
A69 BUILDER SPEC: G9 selection, A42-D 6 trap weighting plus the A69 drop-only repair. For the Sonnet build lane and the Sonnet skeptic.

0. HARD RULES FOR THIS LANE (unchanged from the orchestrator)
- Working directory: /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build.
- Python: ../../.venv/bin/python -B, with HF_HUB_OFFLINE=1. CPU only. No Modal, no GPU, no paid call, no git.
- Never run any G13 job, and never run g13_c2.py in any form.
- Never edit:
  - g13_c2.py or decontam_g13.py;
  - c_build/crowd_select.py or c_build/mixer.py (imported, never edited);
  - HANDOFF.md or PREREG_FINAL.md.
- Never write into data/, and never write c2_build/crowd_c2/select_*.json. All scratch output goes to c2_build/staged/p2_select/.
- Never open a path containing:
  - "ohs" (any case). This includes tests/test_g13_c2_ohsac.py; do not open it.
  - "sealed", except c2_build/sealed_hashes*/ through the existing tools.
  - "jev", or anything under ~/.claude.
- Never stop or signal a process you did not start.
- Report counts, ids, paths and shas only, never row text.

1. FILES AND ALLOWED EDITS
- c2_build/c2_select.py (main work):
  - add the trap weighting, select_c2, the cap loop, the repair and scratch mode;
  - wire select_family and reselect.
- c2_build/a49c.py: swap_balance gains two optional parameters, unit_class and guard. With both None, the output must be byte-identical to today's.
- c2_build/mix_c2.py: only the changes in section 7.
- New tests:
  - c2_build/tests/test_c2_select_a69.py
  - c2_build/tests/test_mix_c2_a69.py
- Back up all three files first, into c2_build/_backup_a69/, with their current sha256s:
  - c2_select.py 70cde02dfe21a2c1…
  - a49c.py 5518e577eac09c3b…
  - mix_c2.py 3faaf07a5b40d15c…
- Pinned imports (record their shas in the report): crowd_select.py d41e625753f73a13…, mixer.py b95fc2e65cd1c95f….

2. CONSTANTS. One dict, c2_select.A69. A test asserts every value.
- TRAP_P_MIN = 0.25
- TRAP_W = 2.0
- TRAP_W_STEP = 0.1, TRAP_W_MIN = 1.0 (guard only)
- TYPE_CAP = 0.35
- HARD_MAX = cs.CAP["hard"] (0.30), EASY_MAX = cs.CAP["easy"] (0.25), MED_MIN = cs.MED_MIN (0.45)
- REPAIR_LOSS_MAX = 0.25 (share of the pre-repair selected rows; includes cap-pass companions)
- REPAIR_PASSES = 3
- SEED = c2io.SEED (20261013); key = sel_key(fam) (the family id)
- G11_MAX = 0.02
- DEV_PRIOR_RATES (report only): {"band off-by-one": 0.50, "boundary": 0.39, "rename/merger": 0.38, "unit": 0.38, "not-yet-in-force": 0.30}
- A42D6_FAMILIES = [f for f in c2io.PROGRAM]. Applied only when pg is not None and the family is not in CARRY or BLOCK_TARGETS.
- REPAIR_ORDER = ["rows_per_card", "token_mean", "freeform_share", "yes_no_share", "yes_rate", "g10_cells", "yes_is_bad_share", "twin_share", "equiv_share", "complement_share_of_yes_no", "non_syntactic_share_of_pairs", "longest_option_pp", "abstain_wrong_share", "gold_position_cells", "gold_rank_cells", "chi2_label_x_bin_a42d6", "chi2_label_x_bin_pg"]
- PROTECTED = REPAIR_ORDER + ["difficulty_caps", "trap_type_cap", "g11_selected"]

3. INPUTS (inside select_family; all on the post-G13 pool, after drop_excluded)
- rows, rels and units = cs.units_of(rows, rels). The unit uid is rows[units[u][0]]["id"].
- probs: C1 label dicts {option text or "yes"/"no": prob}, from the same label set as pg. Extend load_c1 to also return probs; one read, one view. pg = cs.p_gold, unchanged.
- Assert for every choice row with meta.opt_err:
  - every opt_err key is one of row["options"];
  - the gold option is never a key with a non-empty tag list;
  - the probs keys equal the options.
  If any fails: SystemExit naming the family and the counts only.
- ntok = dict(zip(ids, mixer.token_counts(ilog, rows))). Same pinned tokenizer and function as mix_c2; compute once per pool.

4. TRAP WEIGHTING
- 4.1 trap_info(rows, units, probs)
  - For each choice row: flagged_opts = options with a non-empty tag list and probs[o] ≥ 0.25. Use the same tolerance as written, a plain >= 0.25.
  - unit flagged iff any of its rows has a flagged option. tags_u = the union of the tags on its flagged options.
  - Pick rate per tag τ over all pool choice rows:
    - shown_τ = rows with an option carrying τ;
    - picked_τ = rows whose argmax option carries τ (argmax ties go to the first option in the row's option order);
    - rate = picked/shown.
  - rank = sorted(tags, key=(-rate, -shown, name)).
  - ptype_u = the tags_u member with the best rank.
  - Return the flagged set, tags_u, ptype_u, the pick_rates table and rank.
- 4.2 bins_a42d6(rows, units, pgbins, treated)
  - Every row of a treated unit is "hard"; every other row keeps pgbins[id], where pgbins[id] = cs.bin_of(pg[id]).
  - Record counts re-binned from medium to hard and from easy to hard.
- 4.3 race_order(rows, units, seed, key, treated, ptype, rank)
  - For each unit: h = cs.h64(seed, key, "order", uid); U = (h + 0.5)/2**64; t = -math.log1p(-U)/w, with w = 2.0 if u is treated, else 1.0.
  - order0 = sorted(units, key=(t, h)).
  - P = positions in order0 that hold treated units. T = treated units sorted by (rank index of ptype, t, h). Put T into P in sequence.
  - Return the order: a permutation of unit indices.
  - With nothing treated, this must equal sorted(range(n), key=h), which is crowd_select's order.
- 4.4 select_c2(rows, units, pg, target, key, seed, bins=None, order=None)
  - A verbatim copy of cs.select's body with exactly two injection points:
    - bins = the bins argument if given, else {id: bin_of(pg[id])};
    - order = the order argument if given, else crowd_select's own hash order.
  - Every helper is still called from cs: stratum, label_class, n_classes, _budgets, easy_thinned, selection_report, CAP, REFLOW_ORDER, REFLOW_ROUNDS.
  - Keep a diff file, c2_build/_backup_a69/select_c2.diff, against crowd_select.select: only those lines may differ.
  - easy_thinned is called with the bins in use.
- 4.5 trap_select(...): the 6.4 cap loop
  - E = set(flagged).
  - Loop:
    - bins6 = bins_a42d6(E); order = race_order(E); res = select_c2(..., bins=bins6, order=order).
    - S = selected units ∩ E; N = |S|; c = Counter(ptype[u] for u in S).
    - over = {τ: c[τ] for τ in c if c[τ] > 0.35*N + 1e-9}. If over is empty, stop.
    - For τ in sorted(over): x = ceil((c[τ] - 0.35*N)/0.65 - 1e-9). Remove from E the x units of S with ptype τ that sit latest in `order`.
    - Record the round.
  - E only shrinks; the round count is bounded by |flagged| + 1.
- 4.6 Guard (6.3): on the final res, assert both:
  - treated rows ≤ hard rows (bins6) ≤ 0.30 × realised rows + 1e-9;
  - easy share on pgbins ≤ 0.25 + 1e-9.
  If the first fails, step w down from 2.0 by 0.1 (TRAP_W_STEP) and re-run 4.3-4.5. If it still fails at w = 1.0: SystemExit. Record weight_used and weight_scaled. Expected: 2.0 and false.

5. SWAP STEP (a49c.swap_balance)
- Call it with:
  - bins = bins6;
  - never_in = cs.easy_thinned(rows, units, bins6, key, seed);
  - unit_class[u] = (u in E_final, ptype[u] or None). The partner key becomes (bin_of(u), size, unit_class[u]).
  - guard = a function new_sel -> bool that returns False if any PROTECTED check passes on the old selection and fails on the new one (section 6.2 evaluator).
- When the best partner fails the guard, try the next-best partner of the same key (by f ascending, then the existing seeded order), up to the existing 80-partner window.
- Record guard_rejections.

6. REPAIR STEP: repair_a69(fam, rows, rels, units, sel, bins6, pgbins, order, E, ptype, ntok, target)
- 6.1 State. S = the set of selected unit indices; R = the rows of S. Evaluate rows with:
  - r["_block"] = fam;
  - meta.difficulty_bin = bins6[id], meta.pg_bin = pgbins[id], meta.crowd_pg = pg[id] (as load_block sets them).
- 6.2 Evaluator: checks(S) → {name: (verdict, distance)}. Verdicts must come only from the binding functions:
  - a49c.family_checks(fam, R, rels_in_S, ntok) gives yes_no_share, yes_rate, yes_is_bad_share, gold_position_cells, gold_rank_cells, longest_option_pp, abstain_wrong_share, token_mean, complement_share_of_yes_no, non_syntactic_share_of_pairs, twin_share, equiv_share.
  - mix_c2.cap_checks(R, ntok, final=True): lazy import inside the function to avoid a circular import. Use only this family's lines:
    - rows_per_card ("a card holds");
    - token_mean ("mean … tokens");
    - freeform_share ("free-form rows");
    - difficulty_caps ("difficulty easy");
    - plus easy ≤ 0.25 on meta.pg_bin.
  - g10_cells: mixer.g10_checks(R, {}, True, side={}). Only lines starting "G10 yes-rate cell outside", "G10 " + "small yes-rate cells", or "G10 aggregate yes rate" count. Pooled lines (attack × label, pooled abstain) and the row-level gold position line (superseded by A49 b) are ignored here; mix still asserts them.
  - chi2_label_x_bin_a42d6: cs.selection_report(rows, units, S, bins6, target, True, pg)["checks"]["chi2_p_gt_0.01"].
  - chi2_label_x_bin_pg: the same call with pgbins.
  - trap_type_cap: max over τ of the selected E-unit share ≤ 0.35 + 1e-9.
  - g11_selected: no meta.c2.skin_id and no meta.wording_id above 2% of R (as gen_full_c2.g11_shares).
  - A verdict of n/a counts as pass.
- Distances, computed by helpers. Each must be 0 exactly when the binding verdict is pass or n/a; assert this on every evaluated state and SystemExit on a mismatch. Use the binding function's own tolerances.
  - rows_per_card: Σ over cards of max(0, n − 64). Cards are mix_c2.card_of; None is ignored.
  - token_mean: max(0, mean − 800).
  - freeform_share: max(0, share − cap). cap = 0.40 for T07 and T32, else 0.25.
  - yes_no_share: max(0, lo − s, s − hi).
  - yes_rate: max(0, |y − .5| − .02).
  - g10_cells:
    - over cells with ≥ 50 rows: Σ max(0, |y − .5| − .02);
    - over cells with < 50 rows and binomial p < 0.01: Σ (min(300, −log10 p) − 2 + 1e-6);
    - cells keyed exactly as in mixer: (block, wording_id, difficulty_bin, negcount.k_all(instructions)).
  - yes_is_bad_share: max(0, |s − .5| − .05).
  - twin_share: max(0, .20 − s, s − .25).
  - equiv_share: max(0, .05 − s, s − .10).
  - complement_share_of_yes_no: max(0, .20 − s).
  - non_syntactic_share_of_pairs: max(0, .30 − s).
  - longest_option_pp: max(0, |d| − 2).
  - abstain_wrong_share: max(0, .5 − overall), plus, over cells with ≥ 30 rows and share < .5, Σ (.5 − share + 1e-6).
  - gold_position_cells, gold_rank_cells and both chi2 checks: over each failing test (p ≤ 0.01), Σ (min(300, −log10 p) − 2 + 1e-6).
  - difficulty_caps: max(0, hard6 − .30) + max(0, easy6 − .25) + max(0, easy_pg − .25).
  - trap_type_cap: Σ over τ of max(0, share − .35).
  - g11_selected: Σ over keys of max(0, share − .02).
- 6.3 Move(S, u)
  - S1 = S − {u}.
  - Then crowd_select's cap rule, verbatim: for b in ("hard", "easy"), walk the units of S1 in reverse `order`. Stop when used[b] ≤ CAP[b] × total + 1e-9. Otherwise drop a unit if it has b rows (bins6) and no medium rows.
  - The units dropped by this rule are the move's companions.
- 6.4 Main loop
  - rows_pre = |R|; units_pre = |S|; loss_max = floor(0.25 × rows_pre).
  - failing_before = the failing REPAIR_ORDER checks.
  - Repeat up to REPAIR_PASSES times:
    - progress = False.
    - For each check c in REPAIR_ORDER:
      - While verdict(c) is fail:
        - Walk the candidates u in reverse `order` (selected units only, lowest priority first). Skip u unless its removal alone strictly lowers distance_c (this pre-filter is exact; incremental statistics are allowed only if they equal the evaluator's).
        - Build the move M = Move(S, u). M is admissible only if all of these hold:
          - distance_c(M) < distance_c(S) − 1e-12;
          - for every p in PROTECTED: if p passes on S, it passes on M; if p fails on S, distance_p(M) ≤ distance_p(S) + 1e-12;
          - rows_dropped_so_far + rows(S − M) ≤ loss_max.
        - Take the first admissible move: record it, set S = M, set progress = True.
        - If no move is admissible: stop this check (reason "no admissible unit" or "loss limit").
    - If not progress: stop.
  - After the loop: no fill, no reflow, no swap and no reselect. Return the final S and the record.
- 6.5 Repair record
  - checks_order, rows_pre_repair, units_pre_repair, loss_max_rows
  - moves: [{check, unit_first_id, unit_rows, rows_by_bin6, treated, ptype, companions: [[first_id, rows]], distance_before, distance_after, changed_distances: {name: [before, after]}}]
  - units_dropped, rows_dropped (companions included), rows_after, passes_run, loss_limit_hit
  - failing_before, failing_after, stop_reason_by_check
  - checks_final: {name: {verdict, distance, value}}
  - g11_selected_report and a spec 3.0 report on the final rows (cards per family vs max(20, rows/45), median rows per card, register shares, max skin rows): report only.

7. SELECT RECORD AND MIX_C2 CHANGES
- 7.1 select_family, for A42D6_FAMILIES, in this order:
  1. drop_excluded (unchanged);
  2. trap_info, then trap_select (4.5) and the guard (4.6);
  3. the swap step (5);
  4. the repair (6);
  5. final report = cs.selection_report(rows, units, S, bins6, target, True, pg); g5 = cs.g5_reread on the final S.
- report.checks gains:
  - a49c_and_caps_pass: every REPAIR_ORDER check passes on the final rows;
  - chi2_p_gt_0.01_pg_bins;
  - easy_le_25_pg_bins;
  - trap_type_cap_le_35.
  report.pass = all(checks).
- New top-level record fields:
  - "a42d6": {rule: "A42-D 6 via A69", trap_p_min, weight_used, weight_scaled, type_cap, pick_rates {tag: {shown, picked, rate}}, type_order, dev_prior_rates_report_only, flagged_units, flagged_rows, cap_rounds, untreated_by_type_cap {tag: n}, treated_final_units, selected_treated_units, selected_treated_rows, selected_treated_type_shares, selected_flagged_6_2_type_shares_report_only, selected_flagged_per_tag_shares_report_only, rebinned_medium_to_hard, rebinned_easy_to_hard, hard_share_a42d6, hard_share_pg, easy_share_pg, treated_unit_first_ids, trap_type_by_unit_first_id};
  - "pg_bin": {id: bin};
  - "difficulty_bin": {id: A42-D 6 bin};
  - "a69": {version: 1, swap: {...existing info, guard_rejections}, repair: {6.5}};
  - "tool_sha256": {c2_select.py, a49c.py, crowd_select.py, mixer.py};
  - "scratch": false.
- Families outside A42D6_FAMILIES (carry, blocks, DI, T4x) keep today's code path and must produce byte-identical records.
- 7.2 c2_select.reselect: for a program family, take bins6 from the rows' meta.difficulty_bin, treatment and type from meta.trap, and the type order from the select record (passed in by mix). Then:
  - run 4.3 (race_order), 4.4, 4.5 (starting with E = the recorded final treated units still present), 4.6, 5 and 6;
  - recompute no pick rate and no flag.
  Return the same reports as now, plus the a42d6 and a69 records per part.
- 7.3 mix_c2.py
  - Add A69_TOOL_SHAS = {} (a placeholder, like OHS4_MANIFEST_SHA256), filled from the A69 addendum after review. --final refuses a program-family select record if any of these hold:
    - the dict is empty;
    - the record's tool_sha256 differs from it;
    - "a42d6" or "a69" is missing;
    - scratch is true.
  - selection_problem: also return None when ALL of these hold:
    - bad == ["total_eq_target"];
    - a69.repair.rows_dropped > 0;
    - len(selected_ids) == rows_pre_repair − rows_dropped;
    - rows_dropped ≤ floor(0.25 × rows_pre_repair);
    - rows_pre_repair == target, or units_removed(exclude_ids) > 0, or at_most.
    Any other shortfall keeps today's verdict.
  - load_block: set meta.difficulty_bin = s["difficulty_bin"][id] (A42-D 6), meta.pg_bin = s["pg_bin"][id] and meta.trap = {"treated": bool, "type": str or None}. Keep s["a42d6"]["type_order"] for apply_targets.
  - cap_checks: add a problem line when the share of meta.pg_bin == "easy" in a block is above EASY_MAX + 1e-9 (rows without pg_bin: skip).
  - apply_targets: pass the a42d6 info to reselect (7.2) and record its a69 output in info[b].
  - A family whose selection fails is already left out by load_block in --final (SystemExit is caught by build). Keep that, and make sure a failing a49c_and_caps_pass reaches it through report.pass.
  - a49c_assert and cap_checks on the mixed rows: unchanged.

8. SCRATCH MODE (the P2 dry test)
- New select flags: --scratch-out DIR and --scratch-drop-ids FILE…
- Refuse unless DIR resolves under c2_build/staged/. Refuse if DIR is under crowd_c2/ or data/. Refuse --scratch-drop-ids without --scratch-out.
- Scratch mode reads only the key drop_ids (or training_ids_to_drop / ids) from each drop file, through LinkGuardedInputLog and the never-open rule. The orchestrator names the batch-4 candidate logs. Scratch mode skips g13_log_problems (the logs are provisional) and marks the record scratch: true, provisional_drop_files: [...].
- Scratch mode writes only DIR/select_<FAM>.json, DIR/g5_reread_<FAM>.json and DIR/select_inputs.json. It writes no progress_c2.log line and nothing in crowd_c2/ or data/.
- Scratch run: all 15 families. Report per family:
  - pool rows, target, rows, short_by;
  - flagged units, treated units, cap rounds;
  - swaps;
  - repair moves and rows by check;
  - failing_before and failing_after;
  - report.pass.
- Target to report (not a bar): T26, T01, T15, T23 and T25 pass.
- Failures are reported, never tuned. Only code-vs-spec bug fixes are allowed, and each is re-reviewed.

9. TESTS (pytest, CPU, synthetic fixtures unless noted; nothing written outside tmp_path)
- 9.1 select_c2 == cs.select: identical sel, bins, budget, reflow and report, with no treatment, on synthetic fixtures. Also on every present family's real candidates plus C1 labels in memory, with nothing written; report only identical true/false.
- 9.2 race_order:
  - nothing treated → crowd_select's order;
  - treated → untreated relative order unchanged;
  - on 10,000 synthetic units, the share of (treated, untreated) pairs with the treated one first is ≈ 2/3 (binomial, p > 0.001);
  - the 6.4 reassignment uses the same positions and is sorted by type rank.
- 9.3 Flags:
  - 0.25 flags and 0.2499 does not;
  - an empty tag list never flags;
  - gold is never tagged (a fixture with a tagged gold → SystemExit);
  - yes/no rows never flag;
  - the flag is unit-level;
  - an opt_err key that is not an option → SystemExit;
  - a G13-dropped row changes neither the flags nor the pick rates.
- 9.4 Re-bin: every row of a treated unit is hard; pg_bin is unchanged; untreated rows are unchanged.
- 9.5 Pick rates and ptype: argmax tie goes to the first option; tie order (rate, shown, name); one type per unit.
- 9.6 Type cap: with an 80% dominant type, the final selected treated share is ≤ 35%; un-treated units can still be selected; E is monotone; the loop terminates.
- 9.7 Guard 4.6: hard ≤ 30% on bins6; easy ≤ 25% on pg bins; weight_scaled false; a forced-violation fixture refuses.
- 9.8 Swap: partners match (bin6, size, treated, ptype); a swap that newly fails a protected check is not made; with unit_class and guard None, output is byte-identical to the pre-A69 a49c.swap_balance.
- 9.9 Drop-only:
  - final ids ⊆ pre-repair ids;
  - rows deep-equal before and after (no field edited);
  - no unit added;
  - no fill, reflow or swap after the repair (spy on select_c2 and swap_balance).
- 9.10 Monotone: replay every recorded move. The target distance falls strictly; no protected check goes from pass to fail; no failing distance rises.
- 9.11 Determinism: two runs give identical record bytes; a different synthetic seed gives different drops.
- 9.12 Loss limit: a fixture needing > 25% stops at the limit, the check still fails, pass=false, loss_limit_hit=true.
- 9.13 One fixture per REPAIR_ORDER check, each failing only that check, ends with that check passing:
  - token mean, with fake ntok;
  - card 67 → ≤ 64;
  - longest option, + and −;
  - equiv below 5%;
  - twin above 25%;
  - yes/no share, low and high;
  - yes rate;
  - one G10 cell;
  - free-form;
  - abstain;
  - gold position;
  - each chi2.
- 9.14 Coupling: where the only helping drops break another check, there is no move; still failing; pass=false.
- 9.15 Pre-filter == brute force (every unit evaluated with the real functions), on 2 synthetic fixtures and on 1 real family in memory: identical moves.
- 9.16 Distance helpers are 0 exactly when the binding verdict passes, on 500 random sub-selections of 2 real families (in memory).
- 9.17 mix:
  - selection_problem accepts exactly the 7.3 arithmetic, and refuses a shortfall larger than rows_dropped, a loss above 25%, a scratch record, a record without a42d6/a69, and a sha mismatch;
  - load_block sets difficulty_bin, pg_bin and trap;
  - cap_checks flags pg-bin easy;
  - apply_targets → reselect keeps bins6 and treatment and re-runs the repair;
  - end to end on a fixture, a49c_assert and cap_checks are empty whenever the record passes.
- 9.18 Scratch guards: refuse an out dir in crowd_c2/, data/ or outside staged/, and --scratch-drop-ids alone.
- 9.19 Carry pools and blocks: select output is byte-identical to before A69.
- 9.20 Constants equal section 2; no path containing ohs, sealed or jev is opened (spy on the ilog).
- Run with: cd c2_build && HF_HUB_OFFLINE=1 ../../.venv/bin/python -B -m pytest tests/test_c2_select_a69.py tests/test_mix_c2_a69.py tests/test_c2_select.py tests/test_mix_c2.py -q. All existing tests must still pass.

10. SKEPTIC CHECKLIST (Sonnet, before any scratch or real select)
1. The select_c2 diff touches only the two injection points.
2. The 9.1 equivalence holds on real families.
3. Race weights: odds 2:1, untreated order unchanged.
4. Cap loop reading as in A69 (b6); per-unit type as in (b2).
5. No refill or reflow after the repair.
6. Admissibility uses binding-function verdicts, and the distance and verdict assert runs.
7. The loss limit counts companions.
8. The mix shortfall arithmetic.
9. The sha pin and the scratch refusals.
10. The never-open rule and the input log.
11. Carry pools and blocks untouched.
12. Every constant matches the ruling.
13. No dev, Jev, sealed or G-proxy input.

Verdict: PASS, or a list of defects. On PASS, report the sha256s of c2_select.py, a49c.py and mix_c2.py for the A69 addendum. A69_TOOL_SHAS is filled only by the orchestrator, after the addendum.

11. RETURN TO THE ORCHESTRATOR
- Changed file paths, with sha256s before and after.
- Backup paths.
- Test counts: passed, failed, skipped.
- The 9.1 identical flags per family.
- The skeptic verdict.
- The scratch-run counts table (section 8).
- No row text.