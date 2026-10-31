# C2.1 BUILD ORDER (Sun 18 Oct 2026; Opus planner; v3.1 skeptic revision same day; v3.2 merge same day)

v3.2 (Sun 18 Oct ~07:00 UTC): follows plan v3.2 (C2_1_PLAN_v3.md header, sections 0 item 12 and 16). Changes are
marked "v3.2:" with sources [A79], [A82 n], [OWNER-ROW] (check every row when it is made), [LEV An], [INV], [CRIT xn].
New lanes L-R (public train splits), L-K (T59/T60) and L-P (T63/T66/T67). The v3.1 text is kept in
C2_1_BUILD_ORDER_v3_1_SNAPSHOT.md.
v3.2-r (Sun 18 Oct; Opus planner): fixes from C2_1_PLAN_v3_2_SKEPTIC.md, marked "v3.2-r (Sk n)"; response table in plan
16.8; training timeline and money in plan 16.7; the list of G0-lites / addenda to write is plan 16.9. Pre-revision
text: C2_1_BUILD_ORDER_v3_2_PRESKEPTIC_SNAPSHOT.md (sha256 93acc0fa…). L-0 is split into L-0a (sandbox and images)
and L-0b (stamp service, wrapper, mix guard, registry, manifests), each with its own builder (Sk 17).

Companion to C2_1_PLAN_v3.md (the plan; v3.1 fixes are listed in its section 15). Every agent sets `model` explicitly;
never Fable. Effort per ORCHESTRATION_RULES.md. One writer per file set; agents writing overlapping files get worktrees.
v3.1: the sealed brief is re-derived by a fresh sealed Opus inside the sealed directory; OHS5_BRIEF_DRAFT.md is retired
and is NOT an input to any lane (skeptic 7). No agent is given both a training-side and a sealed-side file.

READ SCOPES (v3.1, skeptic 7c; the access audit enforces them)
- Training lanes (L-0, L-A, L-I, L-T, L-C, L-G): plan sections 1, 2, 5, 6, 7, 8, the "PRE-REGISTERED RULES" block of
  section 3, and their own lane block below. Never the rest of section 3, the skeptic file, the sealed directory or any
  path containing "ohs" or "sealed" (program jobs that run G13 are the orchestrator's, not the lane's).
- Sealed lane (L-S): plan section 3, section 4, the section 10 OWNER-RESERVED table, section 11, and the L-S block
  below. Never sections 0-2 or 5-9, the skeptic file, research_v3 family files, or any training generator or pool.
- L-E (eval harnesses): plan section 4 and the L-E block. Never training generators; training lanes never open L-E files.
- L-D (deployment): plan sections 6 and 8 and the L-D block.
- v3.2 L-R, L-K, L-P: the same scope as the other training lanes (plan sections 1, 2, 5, 6, 7, 8, the PRE-REGISTERED
  RULES block of section 3, section 16, and their own lane block). L-R also reads C2_1_PUBLIC_TRAIN_INVENTORY.md
  sections 1, 2 and 6 (licence records), never a dataset's test/dev files.
- v3.2: plan section 16 is training-side; the access audit flags any sealed-side read of it.

GLOBAL ORDER (critical path)
1. C2 first. A C2 step never waits for a C2.1 step. Mac G13 and the od-l4b GPU yield to C2.
2. OHS-5 sealed build (L-S) next. ROWS of any C2.1 family start only after the OHS-5 FREEZE record exists; a program
   check (written in L-0) refuses to start any row job without it, without the G13 target registry sha, and (v3.1)
   for any row whose policy, tool, language, runner or carrier name is not on the frozen names-only allow-list.
3. Generator CODE, solvers, CPU gates and hash exports (no rows) may start on day 1 in every training lane.
4. Usage: run get_usage before every launch of 3 or more agents; record each lane's day-1 burn; shed at 90% in the
   order P1 wave -> voice pool -> general rows -> remaining training lanes (L-S, C2 and GO steps never shed); ping the
   owner at 96%; never cross 98%. Weekly reset Mon 15:00 UTC. v3.2-r (Sk 21): L-R, L-K and L-P builders launch only
   after the measured per-lane day-1 burn gives a weekly projection under the 90% shed line (checked Mon 19 after the
   15:00 reset); a lane that does not fit waits in the usage shed order, it is never started on an estimate.
5. v3.1 names: every identifier in a training row comes from the seeded random namespace with the TRAINING salt; no
   hand-picked fake names (skeptic 3). v3.2-r (Sk 8): L-R and P1-realism rows are EXEMPT (they carry real names);
   their vocabulary is extracted by program into names-only manifest v1.1 / v1.2 before the OHS-5 freeze.
6. v3.2 [OWNER-ROW]: every row is G13-stamped and answer-checked WHEN IT IS MADE (plan 16.1); no unstamped row enters a
   pool or the mix; the C2 replay pool is cleaned ONCE against every target before any mix; the binding G13 is one
   confirming pass (<= 1 h).
7. v3.2 (the A78 lesson): no record builder (stamp, select, mix, L-R mapper) runs without a signed ruling-to-code
   conformance record for its current code sha and ruling sha (plan 16.1 step 0).
8. v3.2 usage shed order (plan section 8): research pass and extra tasksource scouting -> P1 (L-P) -> voice pool ->
   open tier-C L-R datasets -> general rows -> remaining L-R -> remaining training lanes; L-S, C2, the stamp service,
   GO steps and the confirming G13 are never shed.

STANDARD FAMILY PIPELINE (all training lanes)
G0-lite one-pager (Sonnet high; v3.1: marks every gate PRE-FREEZE KILL (CPU, data only) or POST-TRAINING REPORT, and
writes numeric bars: binary probes held-out AUC <= 0.55 with 95% upper bound <= 0.60; k-way <= 1/k + 3 pp, bound
<= 1/k + 6 pp) -> Opus G0-lite approval (Opus high, batched) -> generator code + solver A (lane builder, Sonnet high) ->

## L-I  Injection lane: T41c TAINT (clean-room)

v3.2: this lane has additions in "v3.2 LANE ADDITIONS" (L-I) at the end of this file; they bind where they differ.

| Item | Detail |
|---|---|
| Owners | Builder: Sonnet 5.5 high (clean-room: never opens T27/T40-T46 generators, templates, wording pools or OHS-AC). Solver B: Sonnet 5.5 high. Payload and carrier wording: Haiku 5.5 medium (v3.1: writers never see the literal-ban list; G13 enforces it by program). Opus 5.5 high for G0-lite and the label-table ruling. Skeptic: Sonnet 5.5 high. |
| Inputs | Plan v3 section 1 B.4; the stripped excerpt of research_v3/injection.md section 5.1; T41's recorded C2 status (fixes size 2,000 or 3,000). v3.1: NOT the G13 literal-ban list (skeptic 8b). |
| Outputs | Benign-artifact generators per carrier type; splice engine for minimal pairs; attack-tuple schema; label table; held-out family split definition; source tags inside C2's existing fields; length-tail option; a benign dev split never trained on (the primary Tier-1 AgentDojo threshold source, handed to L-E); rows and gate reports. |
| Gates | Standard pipeline plus (PRE-FREEZE, CPU): format-only probe AUC <= 0.55 (upper bound <= 0.60); held-out-family CPU probe gap <= 5 pp; benign share 50% with >= 30% of benign rows delegated or ambient-helpful; delegated-but-high-risk rows labelled per the action-class rule; zero benchmark attack strings or environment text (G13 pilot). POST-TRAINING report: trained-model in-family vs held-out gap. |
| Day-1 tasks (Sun 18 Oct) | (1) Sonnet high writes the G0-lite with D1-D7, the pinned label table and the gate split. (2) Opus high approves (Mon 19 Oct). (3) Builder starts the benign-artifact generators and the splice engine (code only). |
| Rows | From Sun 25 Oct. |
| Kill rule | Standard. A failed format-only probe after the fix iteration is a kill (the generator leaks format into the label). |

### L-I (T41c) [LEV A6 pool, A10, A12-A14, A16; CRIT C8, D1]
- G0 addendum: A13 benign-worded hijacks + lexical-balance probe; A14 fixed 5% long-input share (only if the Fri 23 probe
  says build); A16 observation formats; A12; A10; difficulty ladder; the Claude-written benign twins for the L-R Gandalf
  and Aya rows (literal ban by program; writers never see it). No direct-injection rows inside T41c.
