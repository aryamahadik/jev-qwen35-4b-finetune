# T60 NOTES (generator side, solver A)

## Opus ruling Q1 (Sun 18 Oct 2026), applied before any pool rows
Source: zed_orch/c21/families/RULINGS_T59_T60_T63.md, section Q1 (T60 H2 same-value supersession). No T60 pool row existed when this was applied.

Ruling: a supersession whose later statement repeats the SAME value is outside the spec (G0-lite 18, 50, 52, 53 give no label for it). Rule line 50
keeps its plain meaning for a later statement with a DIFFERENT value. The generator must never build the other case.

Generator changes (t60_build.py, t60_generator.py, t60_checked.py):
1. `draw_revision_value`: every revision value of a chain is drawn different from every earlier value of the same handle and entity, so the chain
   values are pairwise distinct (A -> B -> A at depth 2 / 3 is ruled out too). One draw when there is no collision, so rows without a collision
   are unchanged; a collision only redraws (CHAIN_REDRAWS), else the group is rejected as a SceneReject.
2. Safety net, per row at creation: `supersede_row_problems(scene)` -> `supersede_same_value` when a later statement with the same handle and
   entity repeats the quoted fact's value, or the chain values are not pairwise distinct. `generate_group` drops the group on that code,
   counts the member rows in `ctx.drops["supersede_same_value"]` (its own counter; `t60_checked.run` adds it to the summary as `family_drops`)
   and regenerates it with the next attempt (not a G13 drop, G0-lite 112). `family_invariants` repeats the check on the finished record.
3. Guard: `assert_no_repeat_on_chain` (an assert, raised as AssertionError, not a drop): no `mark.t60.repeat` on any fact of a chain. It runs at the end
   of `build_h2`; `family_invariants` also refuses an "As a reminder" turn on a supersede row.
Not changed: solver A's rule table, the oracle, the gates, the bars (K13 depth shares are unchanged; replacement draws fill the cells), the wording
pools. Solver B is a separate program (the hard abstain on "the later statement repeats the SAME value" is on its side).

Measured (CPU, main plan of 2,000, 5 seeds x 77 supersession groups):
- before: 23 of 385 chains (6.0%) repeated a value (depth 1: 4, depth 2: 9, depth 3: 10);
- after: 0 of 385; `supersede_same_value` drops 0 (rate 0.0); rows per sub-block identical to before (1,889 per seed);
- the safety net alone on the old draws would have dropped 3.8% to 9.4% of supersede rows per seed (48 rows over the 5 seeds).

Re-run needed after this change (old logs are not evidence): the solver-A / solver-B agreement harness, the K3 tests, the dry run, leg checks.

## Dry-run gate read (18 Oct 2026, CPU, main plan 2,000 and 1,000 row samples; no pilot exists): K4, K6, K21, K28
All four are G0-lite 8.1 PRE-FREEZE KILL gates (set-level; first read = the 1,000-row pilot; ONE combined fix; a gate still failing after it rolls
T60 to C2.2/C3). None is a POST-TRAINING report line. Gate code: t60_gates.py (unchanged, bars unchanged).
- K28 (L1..L4 each >= 10% of KEEP rows): was L4 9.9% (38 of 384, pointer pairs only). Cause: a step-done pair drawn at indirection L4 fell back to an L1
  handle reference. Fix (t60_build.py): that pair now uses the pointer form (a real L4 reference, no handle noun). Now L4 13.5%, L1 41%, L2 29%, L3 16%
  on every seed and size (indirection is balanced per H2 entry at plan level, t60_generator._assign_levels). The "solver B resolves 100%" half needs B.
- K6 (DROP rows naming the noun >= 50%, KEEP rows not naming it >= 30%): was 51.6% / 29.9%. Cause: chain quads (L4 draw) took the fact by handle, so
  every KEEP chain row named it. Fixes: the chain's first step takes the fact by role description (L2); a done decoy chosen to name the noun now names it;
  the share of quad / step-done groups with that decoy is fixed at plan level (MENTION_P = 0.46, exact share). Now 55-59% / 33-38% (24 seeds at 1,000 and
  2,000 rows, min 0.55 / 0.325). The AUC half (G5 probe harness) is not run in a dry run: the gate returns ok = None with "skipped".
- K4 (label share 35-65% per ladder level): FAILS on the ladder part only (head, card, world kind and view shares pass). H1 L2 76% / L3 27% DELEGATE,
  H2 L4 78% KEEP, H3 L2 70% PLAN. NOT fixed here, see below.
- K21: FAILS: H1 L4 4.3% (bar 5%), H3 L4 1.2% (bar 5%), L4 label share 69.8% (bar 55%); family L4 10.0% and L3-L4 63.8% pass. NOT fixed here.
Cause of K4 / K21 (listed for an Opus ruling, no generator change made): the row level is REALISED from each scene (t60_render.realised_levels), and the
planned mechanism levels are honoured only for H1 dmargin (size_below pairs), H3 pmargin (step_count), H2 indirection / distance and the quad salience.
Everything else is emergent and label-dependent: (1) the violating member of an H1 pair gets interference L3 / larger coupling, its twin does not;
(2) H2 salience is 1 + (3 - markers) for a needed fact and 1 + markers for an unneeded one, and only quads carry markers, so in every other H2 pair
KEEP = L4 and DROP = L1; (3) several mechanisms never populate all four levels (H1 interference L2/L4 0%, length L3/L4 0%; H2 salience L2/L3 0%,
recovery L2/L3 0%; H3 irrev L4 0%, depvis L2/L4 0%), which the K21 text asks for (>= 10% each) but the gate code does not check; the twin rule is not
checked either. A fix needs a design choice (markers on quoted facts of pair kinds, pair-level level matching, honouring coupling / interference /
irrev / depvis), so it is a combined-fix item, not a build fix.

## Opus ruling Q6 and its follow-up, with OWNER Record A102 (18 Oct 2026): ladder design for K4 / K21, implemented before any pool rows (no bar and no gate loosened)
Sources: zed_orch/c21/families/RULINGS_T59_T60_T63.md ("Q6 T60 ladder design for K4 and K21" and the follow-up), the note at the end of T60/G0_LITE.md, PREREG_FINAL.md Record A102.

DESIGN VALUE. The Q6 design value "L3-L4 = 55% of the family" is WITHDRAWN (A102). T60-B9's design value (L3-L4 = 30%; bars: >= 25% in the family and in each head,
L4 >= 8% family / >= 5% per head) stands. DISCLOSURE: the REALISED composition is NOT 30%. Measured on 2,000 rows: L3-L4 84% (H1 64%, H2 93%, H3 92%), L4 41%.
Causes: (1) depvis is scored on every row (Opus follow-up, no "focal" scoring) and the table scores an unstated order as `implied by data flow` = L3, so every PLAN row
and every ACT row of an R1 / R2 / card pair is at least L3 (H3 cannot be below ~90%); (2) the bar "every mechanism populates all four levels (each >= 10%)" plus
the rule that a mechanism the edit does not touch sits at the SAME level on both members forces the high mechanism levels onto many rows (stacked on the KEEP member in H2).
All bars are lower bounds and pass; nothing was cut to reach 30%. Opus Q6 batch 2 (B2-2): 30% is a design value, not a target with a tolerance; the binding requirement is the bar (>= 25% in the
family and in each head); a realised 84% fails no bar; the overshoot is forced by the text (H3 about 80% or more whatever the generator does; the fill rule pushes H1 and H2 up). Reducing H1 / H2
stacking is optional and was NOT done (it would have to keep K21 fill and floors, K4 per level, the 55% L4 cap and the A102 twins). No owner decision is needed. Realised shares to
quote in the conformance record and the C2.1 report: H1 64%, H2 93%, H3 92% (family 84%, L4 41%).

A102 (K21 twin rule). The rule applies only to rows whose DECISIVE mechanism (the one tied to the predicate the row's edit or control flips) is at L3-L4. Such a row needs
a twin with the opposite label, the same scenario-id prefix, tokens within +-15%, the same marker count and that mechanism at L2 or below; required for >= 80% of these rows.
All other mechanism levels (length included) still count for composition, K4 per level, the fill bar and the 55% L4 label cap.
- Registered map: `t60_levels.DECISIVE` (key = head:edit | head:ctl | head:card_swap:<size|brief|bound>), e.g. h1:size_below / result_unbounded / card_swap:size|bound -> dmargin,
  h1:coupling / card_swap:brief -> coupling, h1:shared_write / pending_dep -> interference, h2:quad -> salience, h2:pointer_content / supersede -> indirection, h2:step_done -> distance,
  h2:card_swap_recovery -> recovery, h3:undo_added -> irrev, h3:step_count / card_swap -> pmargin, h3:order_stated -> depvis. The control singles (far_inside, multi_violation, all
  heads) are registered with "-" (no decisive mechanism, so no twin is required; the length-L4 carriers are among them). Every built row carries `decisive` and `scenario_id`
  (= the group id; twins are searched by scenario id). The map is a table of HASH_EXPORT (`tables["levels.DECISIVE"]`); a test checks that it covers every (head, edit / control)
  the plan can produce and that its values are mechanisms of the head.
- Gate: `t60_gates.k21_twin_rule(rows)` returns (rate, rows without a twin, rate by head, number of subject rows); `k21_ladder` fails below 80% and also checks the fill bar
  (each mechanism level >= 10% of its rows: head mechanisms over the head, length over the family), L3-L4 >= 25%, L4 >= 8% / 5%, L4 label share <= 55%.

BUILD (files: t60_levels.py, t60_recipes.py, t60_ballast.py new; t60_build.py, t60_generator.py, t60_render.py, t60_rule.py, t60_oracle.py, t60_model.py, t60_gates.py,
t60_checked.py, t60_hash_export.py changed):
- t60_levels.py: realised level of every mechanism of a built row; row level = highest mechanism, L4 only if >= 2 mechanisms are >= 3 and one is 4. DEPVIS_SCOPE and the
  non-focal edit list are gone: depvis is scored on every row.
- t60_recipes.py: a RECIPE per group at plan time (`g["rc"]`: length level, spec per member, planned level per mechanism per member, hard member). The generator asserts
  planned == realised per row (`level_mismatch` / `length_no_fit` are dropped and the group regenerated; both counters are in `family_drops`); no row is filtered by its realised
  level or label. Untouched mechanisms get the same level on both members; the label of the hard member alternates by balanced draws.
- Length: identical neutral "Background notes" on every member (no digit, order word or step / plan / fact vocabulary; the vocabulary hash is exported). Length L4 = exactly
  10% of the rows at 1,100-1,440 tokens (K15: > 1,024 on exactly 10%). The L4 carriers are the control singles plus the step-count pairs. H1 carriers are HALF far-inside
  (DELEGATE) and HALF multi-violation (DO_HERE): with all of them DELEGATE the single-feature tokens AUC of H1 was 0.57; it is 0.48-0.50 now. H3 carriers are the multi-violation
  ACT rows (this offsets the structural PLAN-is-longer signal: H3 tokens AUC 0.53; the pairs alone give 0.54).
- H2: markers on the quoted fact(s) of every pair kind, same count on both members, m and 3 - m equally frequent inside each pair kind, never `repeat` on a supersession chain;
  distance / indirection / recovery are scored for the quoted fact when it is needed (1 when no step uses it). Recovery modes: k1 (counted contingency star, recovery L2),
  k2 (uncounted star on the DROP cells of a quad, L3), ledger (a state key read only by a counted read-back step, persisted copy as decoy, L4 on KEEP). Supersession depth
  1 / 2 / 3 is assigned as an EXACT 50 / 30 / 20 share of the supersede groups (largest remainder, shuffled), not one draw per group (K13 +-5 failed on 3 of 5 seeds before).
- H1: dmargin = tighter of the size and the bound margin; coupling closeness (L4 = a derivable fact); interference by the form of the relation (explicit L2, alias L3, a
  pending step's declared output L4) with near-miss DELEGATE forms. H3: irrev L2 short window, L3 external or over the stakes threshold although undo exists, L4 the window
  expires before the step runs; depvis L1 words, L2 numbered, L3 data flow, L4 derived value; the "two of three" ACT rows are the ACT members of the R1 / R2 pairs.
- H3 card swaps share a form that is hard on BOTH members (expired window or magnitude, derived order more often), so the ACT member is L4 too: together with the half / half H1
  carriers this lowers the L4 label share to 52.6-54.4% (53.3-55.3% before) at the price of H3 L3 going from 56% to 60% (bar 65%).
- Gate code, tests (84), ROW_SCHEMA.md (rendered-grammar additions for solver B), HASH_EXPORT / CODE_SHAS regenerated.

MEASURED (CPU dry run through the pipeline with test doubles and the seed pool, approx_tokens; 2,000-row plan = 1,880 main + 117 lever rows; 1,000-row pilot shape in brackets):
K3 ok; K4 ok (per head / card / world / view, per ladder level); K10, K11, K13 (D 17%, depth 39/23/15 = 51/30/19%), K15 (mean 702, > 1,024 on 10.0%), K19, K27, K28 ok;
K6 data part ok (DROP rows naming the noun 58% [55%], KEEP rows not naming it 44% [47%]); K21 ok: decisive-twin rate 99.9% over 753 subject rows [99.7% over 379]
(H1 99.6%, H2 100%, H3 100%), fill problems none (every mechanism level >= 10%; tightest: H3 depvis L1 / L2 10.1%, H3 pmargin L3 10.1%, H2 recovery L4 11.3%, H2 indirection L3 / L4 11.6%, H1 interference 11.1-12.2%),
L3-L4 84% [84%], L4 41% [40%] (H1 16%, H2 52%, H3 50%), L4 label share 53.6% [53.2%] (bar 55%). Over 11 seeds (5 x 2,000, 6 x 1,000) and both pools: no gate problem,
L4 label share 52.6-54.4%, no group lost to a build rejection. Thin margins (deterministic, balanced draws; seed-to-seed spread ~0.5 point): H2 ladder L4 label share 63-65% (bar
65%), H3 L3 60%, L4 label share up to 54.4% at the 1,000 shape.
NOT CHECKABLE IN A DRY RUN (need the G5 harness): K5, K6 AUC half, K7-K9. Single-feature AUCs (not the probe) for the K8 reader: tokens H1 0.48, H2 0.50, H3 0.53; lines H1 0.54,
H2 0.50, H3 0.65 (the PLAN member has more lines by construction, as in the G0-lite R2 text).
NOT BUILT: the near-miss "a main-thread write after the subtask can end" (needs a timing tag). Solver B must re-run agreement after this landing (the rendered grammar changed).

## Opus ruling Q6 batch 2, B1 (18 Oct 2026): an ordinal reference never lands on a superseded record
Rule (B2-1): the gold rule is the CURRENT value (a superseded fact maps to the latest fact with the same handle and entity); the generator AVOIDS the case, because the rendered row never
states the replacement rule while an L3 ordinal ("the second record fetched by a get call") literally names the old record.
- Builder (`t60_build.build_h2`): the L3 ordinal of a supersede group's star step names the CURRENT record of the chain (the latest one). Superseded records of the chain still count as
  positions among the fetched records. Before the fix every supersede row with an L3 ordinal (36 of 1,880 rows at 2,000; 14 of 940 at 1,000) named the oldest, superseded record. L1 handle and
  L2 role-description references are unaffected (they resolve to the current record). Levels are unchanged (the indirection level is the reference level), so the plan and the fill are as before.
- Per-row assert (`t60_build.ordinal_superseded_problems`, applied to every H2 scene, every step, in `generate_group`): a breaking row is dropped with its own counter
  `ordinal_on_superseded` (a non-G13 drop, shown in `family_drops`) and regenerated on the same skeleton; the same check is in `t60_checked.family_invariants`. It never fires (0 drops) because the
  builder names the current record. Solver B abstains if it ever meets the case.
