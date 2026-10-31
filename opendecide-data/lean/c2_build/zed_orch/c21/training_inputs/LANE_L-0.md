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

## L-0  Infra (sandbox, G13 registry, manifests, audit, row-start guard, C2-reads pipeline, probes)

v3.2: this lane has additions in "v3.2 LANE ADDITIONS" (L-0) at the end of this file; they bind where they differ.

| Item | Detail |
|---|---|
| Owners | Builder: Sonnet 5.5 high. Skeptics: Sonnet 5.5 high (fresh) per tool. Sign-off of the sandbox executor: Opus 5.5 high. Script running and log condensing: Haiku 5.5 low. Research-excerpt strip step: Haiku 5.5 medium, spot-checked by Sonnet. |
| Inputs | Plan v3 sections 2, 4 and 8; codeexec spec (research_v3/codeexec.md 5.4); C2 mix manifest (names and hashes only); public eval list (plan section 4 and EVAL UPSTREAM EXCLUSION). |
| Outputs | (a) od-sbx-build VM and one reviewed base image (runsc from apt/tarball; Python 3.12.x, Node 24.x, Go 1.26.x rootfs by digest; pytest wheels vendored; executor). (b) od-sbx1 (training) and od-sbx-s (sealed) instances from that image, hardened per plan section 8; after handover every training identity is removed from od-sbx-s IAP. (c) Executor + self-test. (d) G13 target registry incl. v3.1 additions (CredLeakBench; only exact AmPermBench/UnderSpecBench item strings, entity names and ID patterns, never generic domain words; V2-lite real-speech set); registry sha. (e) Training names-only manifest v1: families, general domains, policy-card names, tool-catalogue names, languages/runners, carrier formats, external sources, AND the R5 candidate dataset list; frozen as a CLOSED allow-list. (f) C2 mix salted hash export. (g) Access-audit program with the v3.1 read scopes. (h) Row-start guard (refuses row jobs without OHS5_FREEZE.json, the registry sha, or with any name off the allow-list). (i) od-l4b queue (one GPU job at a time; priority C2 > C2 reads of C2.1 rows > L-E dry runs > voice > L-D) and a throughput-per-job-type measurement. (j) Token-histogram and cost tool; CPU prefix-share measurement; Jev price script. (k) A61(b) split-aware check as a pre-result program fix (CPU tests; Opus ruling; adoption is owner-reserved R5). (l) v3.1 seeded namespace generator with a per-side salt (training salt only here; the sealed salt never leaves L-S). (m) v3.1 format-only dummy-row set: about 200 rows in C2's rendered layout with neutral program-filled content, for the Thu 22 exposure probe. (n) v3.1 stripped research excerpts for clean-room lanes (quoted benchmark strings and ID examples removed). Every program skips data/ohs3* and ohs3_parts/ in every data/** glob, with a CPU test (skeptic 30). |
| Gates | Sandbox: Sonnet skeptic reviews exactly the self-test list; Opus sign-off before first execution (target Wed 21 Oct). Registry: Opus spot-check of the upstream list. Audit, row-start guard, namespace generator: Sonnet skeptic + CPU tests. Manifest: Opus freeze. |
| Day-1 tasks (Sun 18 Oct) | (1) Haiku medium compiles the G13 target list and upstreams from plan sections 2/4 into a registry draft; Opus confirms. (2) Sonnet high DRAFTS the names-only manifest v1 (names only) incl. L-G's domains and the R5 candidate dataset list (names from the 17 Oct Decision Index note); it is FROZEN by Opus on Mon 19 after the G0-lite approvals, not today (skeptic 4). (3) Sonnet high starts od-sbx-build and the image recipe (no execution of generated code yet). (4) Sonnet high writes the row-start guard (with the allow-list check), the access-audit program (with read scopes) and the namespace generator, with CPU tests incl. the ohs3 skip. (5) Haiku medium produces the stripped excerpt of research_v3/permission.md section 5 for L-A (and tools/codeexec/injection excerpts on request). |
| Day 2-4 | Mon 19: manifest v1 freeze (Opus) and hand-off to L-S as names only. Image build; self-test; skeptic; Opus sign-off (Wed 21). od-l4b throughput per job type and queue plan (Wed 21). Dummy-row set built (Wed 21). Thu 22: format exposure probe run by the orchestrator in a short Mac window (not overlapping C2). G13 public-target registration (short Mac window); C2 mix hash export; SWE-smith-under-runsc test for P1 (no rows). |
| Kill / stop rule | If runsc fails on the image, fall back to nsjail, then rootless podman with crun (plan section 8); L-C executes nothing until a sandbox has passed self-test and sign-off. Haiku runners stop after 2 failed attempts and report. |

### L-0 (infra) [OWNER-ROW; LEV A1, A2, A15, A19-A21; CRIT B1, B3, B6, I1]
v3.2-r (Sk 17) SPLIT: L-0a (Sonnet 5.5 high builder) owns v3.1 items (a)-(c), (m), (n), the SWE-smith-under-runsc test
and the stdlib symbol-list export for L-P. L-0b (a second Sonnet 5.5 high builder) owns the stamp service, wrapper,
replay clean-up, mix guard, registry (incl. the registry program and registry-only test/dev store, Sk 4), manifests
v1.1 / v1.2, row-start guard, split_aware_check.py fixes and the TOOLS row. Conformance maps are written by SEPARATE
fresh Sonnet 5.5 high sessions (never an L-0 builder) and signed by Opus. v1.1 also lists the DI-TS member sources
(Sk 1), the L-R / P1-realism vocabulary (Sk 8) and T59, T60, T63, T66, T67 in row_job_families_allowed (Sk 24).
| Item | Detail |
|---|---|
| G13 STAMP SERVICE | Long-lived service on the Mac (the single G13 job) with every registered target pre-indexed once; per-batch API returning row-level stamps (row id, registry sha, method-set version, verdict; hits carry target name and method only). Builder Sonnet 5.5 high; fresh Sonnet skeptic; Opus sign-off. Throughput on 10,000 rows measured by Wed 21 (decides a second-host ruling; never sampling). Never runs during C2's binding G13 |
| STAMP WRAPPER | The only write path for rows in every lane: answer checks (program A = program B, family invariants, names guard, token rule G6, PII scrub, span export) + G13 stamp + manifest stamp; drops logged. CPU tests incl. the ohs3 skip |
| REPLAY CLEAN-UP ONCE | Stamp the whole C2 replay pool against every target after the OHS-5 export loads (Sat 24); done by Mon 26; OHS-AC hits on replay published, not dropped (A79 R4); delta pass only for the Mon 26 hard-stop export |
| MIX GUARD | Mix builder refuses any row without a current clean stamp (CPU test); confirming G13 pass tool (<= 1 h target). v3.2-r (Sk 14): the pass = stamp audit + full exact/hash re-run on every mix row + fuzzy only on delta targets; any hit stops the mix. (Sk 22) not signed off by Sat 24 18:00 = row jobs wait. (Sk 16) a program check that a read-twice scaffold is only the R6-exempted strings repeated (needed by Sat 24 18:00) |
| RULING-TO-CODE CONFORMANCE | Clause-to-code maps + CPU tests for: split_aware_check.py (A79 R5; A82 1 split-scoped release ON with its 3 conditions; A82 2 CC BY-SA allowed + disclosed, today it is refused; A82 7 CDLA-Permissive-2.0; A82 6 catalogue still refused, per-source only), R4, R6, A46 screen, A42-D 6, A49c, A50 G6, G0 rulings G1-G10, the stamp rules, the L-R caps, the money shed order. Fresh Sonnet 5.5 high writes; Opus 5.5 high signs; record builders refuse without it |
| REGISTRY ADDITIONS | CRIT B1 list + every L-R test/dev split + transitive targets + free-probe items + public-G panel items; Haiku dedupe, Opus confirm; registry sha by Thu 22 |
| NAMES MANIFEST v1.1 | Adds new-family names (T59, T60, T63, T66, T67 and the new heads), one record per L-R dataset and per promoted tasksource source, md_worldbank / md_usgs / md_cma, and the longer R5 candidate list. Opus freeze Mon 19; names-only copy to the sealed side |
| TOOLS | A1 template-level gold-bug audit script; A2 AFLite-style filter; A15 batch-by-dialect sampler (unit test + skeptic); A19 attach audit and A20 batch check in preflight; A21 length histogram; 8.5 batching by source group with a per-source timer (orchestrator runs 8.5) |
