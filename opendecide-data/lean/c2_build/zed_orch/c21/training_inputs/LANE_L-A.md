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

## L-A  Permission lane: T50 SHELL-GATE, T51 SCOPE-BOUNDARY, T53 EGRESS-SECRET

v3.2: this lane has additions in "v3.2 LANE ADDITIONS" (L-A) at the end of this file; they bind where they differ.

| Item | Detail |
|---|---|
| Owners | One builder: Sonnet 5.5 high. Solver B per family: Sonnet 5.5 high (separate sessions). Wording pools: Haiku 5.5 medium. G0-lite approval and A43(d): Opus 5.5 high. Skeptic: Sonnet 5.5 high (fresh). |
| Inputs | Plan v3 section 1 B.1-B.3 and E; the STRIPPED excerpt of research_v3/permission.md section 5 (from L-0; not the raw file); product policy-card format; C2 rendered layout. Clean-room: never AmPermBench/UnderSpecBench item text, entity names or IDs, CARE/AgentTrust code or rules, bashlex. Using the same domains (git, Kubernetes, S3, jobs) is allowed. |
| Outputs | Per family: G0-lite; spec-to-label rule engine; simulated filesystem/git/infra state model; renderer with semantics-preserving operators and our own expander; tree-sitter-bash and mvdan/sh round-trip validators; solver A; solver B; wording pools; template hash export; then rows and gate reports. T53 fake-credential registry (uniform wrong checksums; frequency caps on documented example keys). All names from the training-salt namespace. |
| Gates | Standard pipeline plus: render round-trip agreement (rows where validators disagree with the spec are dropped and counted); opaque-rule check; obfuscated-dangerous and obfuscated-benign in equal numbers; consent-tier pairs present; trivial baselines per class; dev reweighting slices 1:19 and 1:99 with FPR CIs; T51 contrast pairs edit only the user turn; T53 registered-fake check. |
| Day-1 tasks (Sun 18 Oct) | (1) Sonnet high writes the three G0-lite one-pagers with the v3 deltas, the PRE-FREEZE/POST-TRAINING gate marks and numeric bars. (2) Opus high approves in one batch (target Mon 19 Oct). (3) After approval: spec schema and simulated-state model first (shared by the three families; this lane owns it). |
| Rows | From Sun 25 Oct (after the freeze). Order: T50 pilot, T51 pilot, T53 pilot in parallel by one builder with Haiku runners. |
| Kill rule | Standard. T50 counts as failed if the render validator drop rate exceeds 10% after the fix iteration (a generator defect, not data). |

### L-A (T50, T51, T53) [LEV A3-A6, A10, A12, A15; CRIT C8, D1, D2]
- G0 addendum (Sonnet high -> Opus): A3 edit-as-action sub-family (1,500-2,500 rows by substitution; T51 scope
  variants); A4 alias rows (300-500); A5 late-binding rows (150-300); A6 gate-directed injection (with the L-I pool);
  A10 cue wrappers (only if the Fri 23 probe says build); A12 perturbation; A15 dialects of the card body; difficulty
  ladder with the mandatory quad; T53 phishing-link head (G7 head rows). G9 cross-family test extended to edit actions
  and to T67 (L-P).
