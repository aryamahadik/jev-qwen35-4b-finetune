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

### L-R (NEW; public TRAIN-split mappers; block R) [INV; CRIT A1-A6, B1-B5, E5; A79 R5; A82 1-9]
| Item | Detail |
|---|---|
| Owners | Builder: Sonnet 5.5 high (one per source group if usage allows). Records: Haiku 5.5 medium scouts, Sonnet 5.5 high verifies. Opus 5.5 high approves each per-dataset recast table and each tier-C check. Skeptic: Sonnet 5.5 high (fresh). Runs: Haiku 5.5 low |
| Inputs | Plan 16.3; inventory sections 1, 2, 6; the G13 registry (names only); manifest v1.1 records; the stamp wrapper |
| Outputs | Per dataset: record (licence quote, URL, fetch date, provenance enum, A61(b) record, 8.5 PASS id); train-only reader with a CPU no-test-id test; recast table; mapper; stamped rows; set-level report; seen and share-alike flags |
| Gates | Plan 16.3 rules 1-7: eligibility, splits, labels, row format, caps, A46-style screen (> 15% loss to Opus), G13 at creation, set-level once per dataset |
| Day 1-2 | Sun 18-Mon 19: records and readers for tier A, B2, C and the A82 sets (no rows); HotpotQA Opus 8.5 ruling request; tasksource per-source scout starts. Tue 20-Thu 29: 8.5 batches by source group. Rows from Sun 25 |
| v3.2-r Day 1-3 (binds over the row above) | Sun 18-Mon 19: LICENCE RECORDS ONLY (URL, quote, fetch date, provenance enum incl. "selection-rule"; no download, no reader code, Sk 5); tasksource records quote the UPSTREAM licence (Sk 26); Gandalf ignore-instructions recorded DENY (Sk 7). Tue 20-Fri 23: S-pre 8.5 batches in the pre-registered source-group order (Sk 17); a source's reader and train-only download only after its S-pre PASS. Sun 25-Thu 29 12:00: S-post batches; B2 full-train-split G13 (strict, Sk 3); rows of a source only after its S-post PASS (and, for B2, 0 whole-split hits). Last source addition Fri 23 12:00 (Sk 19). One builder first; a second only from the measured time per source after batch 1 (Wed 21) |
| Kill / stop | A dataset without a PASS by Thu 29 12:00, failing its check, or losing > 15% to the screen without an Opus OK is left out and logged. v3.2-r (Sk 23a): > 1% stamp drops outside exemptions = Opus; > 5% = left out (logged). (Sk 25) a failing span-position / length probe after one re-sample = left out |
