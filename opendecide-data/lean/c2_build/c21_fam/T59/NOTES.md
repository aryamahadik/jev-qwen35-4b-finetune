# T59 build notes (generator side, solver A)

All entries below are build fixes made BEFORE any pool row and before the pilot (G0-lite section 13); no bar changed. The parameters named here
live in t59_generator.py / t59_build.py and are hashed in HASH_EXPORT.json (tables `gen.*`, `build.*`); the sha is frozen at pilot launch.

## Opus ruling Q2, 18 Oct 2026, before any pool rows
Source: zed_orch/c21/families/RULINGS_T59_T60_T63.md, section Q2. G0-lite 3.3.1 binds for T6 on every card (ON or OFF), whatever the
undo path and the magnitude:
- an ambiguous write (timeout, lost acknowledgement) with neither a key (nor an idempotent write) nor a read path is ASK;
- invalid_named_arg with the corrected value not in context is ASK.
The 3.2 GOLD order still governs T1-T5, T7, T8 and the T6 sub-cases where 3.3.1 and 3.2 agree.

1. t59_solver_a.py: `t6_forced_ask(case)`; gold order (1) E empty, (2) ROBUST, (2b) T6 3.3.1 forced ASK (rule `t6_331`), (3) OFF, (4) ON/IRREV.
   `gold_formula` has a `t6_ask` input. A read path on a card without read_first is refused (SpecError).
2. t59_scene.py `derive_T6`: the case carries `t6` = {cls, key, read_path, corrected_in_ctx}. t59_oracle.py decides the two sub-cases by its own
   simulation; K3 (t59_gates.k3_truth_table) crosses 7 T6 sub-cases x 128 = 896 cases.
3. t59_build.py: no T6 D3 control and no T6 card swap (hard AssertionError); T6 stakes evidence is drawn from `T6_CAUSES` (undo present and small /
   no undo / magnitude >= H) whatever the card mode, class, edit or label; `corrected_in_ctx` is a 50% draw on every card.
4. t59_checked.py K25 checks the `t6_331` rows show their decisive facts; t59_g9.py leg (d) runs every mapped T55 record under OFF and ON cards,
   with and without an undo path (`leg_d_cards` in the frozen MAPPING_TABLES).
5. tests/textcheck59.py (build-skeptic text recompute) follows 3.3.1.

## Opus ruling Q2 follow-up, 18 Oct 2026 (FU1-FU5), before any pool rows
**FU1. D3 = 120 with T4 and T5 weighted double.** `D3_TOTAL = 120`, `D3_WEIGHT_BOOST = {"T4": 2.0, "T5": 2.0}`, `D3_TRIGGERS` = every trigger but T6;
the 120 are split by largest remainder over `D_PROC[t] x boost`: T1 18, T2 18, T3 13, T4 27, T5 23, T6 0, T7 12, T8 9. Design reason (set before
the pilot, not tuned on pilot numbers): T4 / T5 PROCEED rows are ON-reversible by construction, so a D3 row there adds nothing to the K30
reversibility share, a D3 row elsewhere adds one. Per-trigger D totals (`D_PROC`, `D_ASK`) and the ASK shares are unchanged. K30 is read on the
built pilot rows; the bar does not move.

**FU2. The G0-lite numbers bind: D1 240 (80 Q-EARLY, about half with an alarming surface), D2 140, D3 120, D4 180.** The earlier 174 / 226 / 100 and
Q-EARLY 50 were an unrecorded builder deviation and are reverted (`D1_TOTAL, D2_TOTAL, D3_TOTAL, D1_EARLY_TOTAL`). Per trigger (rows at 2,000):

| | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | total |
|---|---|---|---|---|---|---|---|---|---|
| D1 unambiguous | 45 | 45 | 29 | 38 | 33 | 18 | 24 | 8 | 240 |
| of which Q-EARLY | 17 | 17 | 11 | 14 | 12 | 0 | 9 | 0 | 80 |
| D2 settled (`D2_BY_TRIGGER`) | 24 | 25 | 18 | 0 | 0 | 24 | 24 | 25 | 140 |
| D3 reversible ambiguity | 18 | 18 | 13 | 27 | 23 | 0 | 12 | 9 | 120 |

D2 rows use only the mechanisms the K30 count recognises: T1 e2 (default), T3 e10 and T7 e10 (precedence), T6 e18 and T7 e14 (resolver), plus
the common-step case e8 for T2 / T8 (K30 needs R-COM >= 8%). `SETTLED_EDITS` in t59_build.py is restricted accordingly.
To reach the K30 'settled' bar (15%) with D2 = 140 the EDIT-FIELD MIX of the A / B pairs is changed (section 13), inside K12 (>= 3 fields,
none above 40%, each >= 2%; every raised weight is <= 0.38): T1 {e1 .16, e2 .38, e3 .16, e4 .14, e5 .16}; T6 {e17 .20, e18 .38, e19 .21, e20 .21};
T7 {e3 .10, e10 .36, e14 .38, e15 .16}; T3, T2, T4, T5, T8 unchanged. Only e2, e10, e14 and e18 count as 'settled by default, precedence or
resolver' in K30 as coded; e1 (stated) and e5 (delegation) are R-DEF in D5 but not 'default / precedence / resolver', so they were not raised.
Build fix for K4 (found in the same dry runs, also present before): the card of a group is chosen by a share-controlled greedy
(`_assign_cards`, `ASK_TARGET = 0.42`) instead of per-pool cycles, so the restricted pools (defaults / precedence / read_first) no longer leave
c05 / c06 outside the 36-48% per-card ASK band.

**FU3.** ROW_SCHEMA.md carries the T6 3.3.1 pointer line under "What the label is" (added after solver B was written; the B agent notes it in
solver_b/README). ROW_SCHEMA.md and this file are hashed in HASH_EXPORT.json (`extra`).

**FU5. A read path is ANY listed read-only call on the target's noun (list_ or get_), a get_ call that already produced a tool result included.**
Scene flags `tools.read_get`, `tools.read_list`, `tools.read_auth`; `sc.read_path_listed(scene)` is what solver A uses (T6 ambiguous write
`rp`, T7 `resolver`). Consequences built in:
- T6: no T6 row lists list_<noun>; a T6 ambiguous row meant to have no read path shows no read-only call on the noun; get_<noun> only on a read_first
  card as the intended read path (e18 twin). A filler tool on the target's noun is never drawn.
- T7: no list_<noun>; a plain get_ with its result shown as the second source only on a card WITHOUT read_first; on a read_first card a T7 row lists
  none until the e14 edit adds the authoritative get_. A read_first T7 ASK row therefore never shows a read-only call on the noun, and any read_first
  T7 row that does is PROCEED (R-RES). T7 rows without tool output have view `primary`.
- Per-row assert `t59_render.read_path_problems(rec)` (text-based; raised as AssertionError in `generate_group`, a `family_invariants` drop in the
  pipeline): scene flags, solver A's resolver and the rendered tool lines agree; T6 read path only on read_first; T7 ASK on read_first has none.
- T8 is NOT subject to the read-path rule (Opus FU5 note: every T8 fork is an INTENT slot, a resolver never settles INTENT); the assert for T8 is
  that no T8 fork is built as a WORLD slot or with a resolver.

No pool rows existed; the old agreement logs and dry runs are not evidence (rerun after these changes).
