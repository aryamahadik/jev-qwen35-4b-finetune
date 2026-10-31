# C2.1 BUILD ORDER (Sun 18 Oct 2026; Opus planner; v3.1 skeptic revision same day; v3.2 merge same day)

v3.2 (Sun 18 Oct ~07:00 UTC): follows plan v3.2 (C2_1_PLAN_v3.md header, sections 0 item 12 and 16). Changes are
marked "v3.2:" with sources [A79], [A82 n], [OWNER-ROW] (check every row when it is made), [LEV An], [INV], [CRIT xn].
New lanes L-R (public train splits), L-K (T59/T60) and L-P (T63/T66/T67). The v3.1 text is kept in
C2_1_BUILD_ORDER_v3_1_SNAPSHOT.md.

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
   owner at 96%; never cross 98%. Weekly reset Mon 15:00 UTC.
5. v3.1 names: every identifier in a training row comes from the seeded random namespace with the TRAINING salt; no
   hand-picked fake names (skeptic 3).
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
independent solver B (separate Sonnet high session) -> Sonnet build skeptic (fresh, high) -> template/wording-pool hash
export (Sonnet medium; v3.1: a new export at EVERY later template change) -> [OHS-5 FREEZE] -> 1,000-row pilot (Haiku
low runs the script) -> 200-row G13 pilot (orchestrator queues on the Mac, serial) -> gates: A50 G6 at size, A49c, G5-H
(two Haiku medium solvers on 300 rows + one Haiku read of 100% of free-form rows; Sonnet medium adjudicates
disagreements; Opus high confirms A43(d) flags in one batch per family), G3-H, family CPU shortcut gates -> full
generation -> C2 reads of the family on od-l4b (pipelined; Haiku low runs, Sonnet medium checks; NOT a kill gate) ->
one fix iteration if any gate fails -> KILL RULE.

v3.2 STANDARD PIPELINE [OWNER-ROW] (replaces the chain above from the hash export on; G0 rulings G1-G10 still bind):
G0-lite + v3.2 G0 addendum (ADOPT NOW items of the lane, difficulty ladder, new heads; Sonnet high) -> Opus approval
(batched) -> generator code + program solver A; program solver B by a separate Sonnet high session (G1) -> Sonnet build
skeptic (fresh) -> ruling-to-code conformance record (fresh Sonnet high + Opus sign) -> hash export (every later
template change gets a new one) -> [OHS-5 FREEZE] -> 1,000-row pilot through the STAMP WRAPPER (every row answer-checked
and G13-stamped at creation; Haiku low runs) -> set-level gates ONCE on the pilot (A50 G6, A49c, variety, matched
pairs, difficulty ladder + C2 <= 70% on L4, G5 probe harness, G5-H / G3-H with Sonnet medium adjudication and Opus
A43(d)) -> ONE combined fix if any gate fails (G3) -> full generation through the stamp wrapper -> set-level gates ONCE
on the built family -> C2 reads on od-l4b (pipelined: trap selection, A1 template audit; NOT a kill gate) -> KILL RULE.
v3.1 HIT REPORTS (skeptic 8): any G13 hit report shown to a builder carries row ids, target name and method only, never
the matched text; the literal-ban list is enforced inside G13 and is never shown to writers.

KILL RULE (every family)
- A family that fails any PRE-FREEZE gate after its one fix iteration, or is not through all pre-freeze gates at the
  DATA FREEZE (Mon 2 Nov 23:59 UTC), rolls to C2.2/C3. The roll is logged with the failing gate and numbers.
  POST-TRAINING gates are report lines, never kill rules (skeptic 6). C2 reads still queued at the freeze do not block
  a family (skeptic 23a).
- More than 1% of a 200-row G13 pilot hit by any method sends the generator back; that IS the fix iteration.
  v3.2 [OWNER-ROW]: read on ALL rows of the 1,000-row pilot and of each full-generation day (no 200-row sample). v3.1
  exceptions: (a) a hit traced ONLY to the sha-bound product-format scaffolding is not the fix iteration (owner-
  reserved with R6; skeptic 2d); (b) rows colliding with frozen OHS-5 are dropped row by row, and up to 5% of a
  family's rows this is not the fix iteration (skeptic 22b).
- Lane-level: when all of a lane's P0 families are through or rolled, its builder moves to the next wave-C (P1) family
  in plan order.
- Floor at the data freeze: at least 6 of 9 P0 families through, including at least one of T42c/T57. If missed, the
  orchestrator stops and reports at GO #1; no training.
- v3.2 [CRIT C1]: T59 and T60 (P0-extra) follow the same kill rule but never count toward the floor.
- v3.2 DATA FREEZE: stretch Fri 30 Oct 12:00 UTC; fallback Mon 2 Nov 23:59 UTC. The orchestrator declares on Thu 29
  12:00 which one applies, from measured gate status (plan section 11 "what must go right").

---------------------------------------------------------------------------------------------------------------------
## L-S  Sealed OHS-5 (separate sessions; sealed directory only)

v3.2: this lane has additions in "v3.2 LANE ADDITIONS" (L-S) at the end of this file; they bind where they differ.

| Item | Detail |
|---|---|
| Owners | Brief author: a FRESH sealed Opus 5.5 high that has read nothing on the training side. Brief skeptic: a second fresh sealed Opus 5.5 high. Sealed lead and freeze signer: Opus 5.5 high (fresh; may be the brief author, never the planner). Builder: Sonnet 5.5 high (fresh). Solver B: Sonnet 5.5 high (fresh, different session). Wording: Haiku 5.5 medium. Answerability readers x2: Haiku 5.5 medium (Read + Write on own files only). Skeptic: Sonnet 5.5 high (fresh). Matcher reader: Sonnet 5.5 medium. Sealed image-layer builder: Sonnet 5.5 high (sealed). |
| Inputs | Plan sections 3, 4, the section 10 OWNER-RESERVED table and section 11 (decision-level spec only); training names-only manifest v1 (frozen Mon 19, includes the R5 candidate list); 8.5 matcher source code; training-side hash export (Thu 22) and later exports; C2 mix hash export (from L-0); od-sbx-s instance (from L-0) plus its own sealed image layer. NOT OHS5_BRIEF_DRAFT.md. |
| Outputs | Sealed brief (re-derived); OHS-5 item files (sealed scope only); rule tables; OHS5_FREEZE.json; keyword export (program-filtered); salted hash export; counts manifest; collision and drop reports; access-audit summary; Cloud Audit Log check of od-sbx-s. |
| Gates | Brief skeptic (fresh Opus) and signature; sealed-salt namespace for every identifier; solver A/B agreement; answerability trace; validity audit; reverse pre-check; keyword-export dry run vs C2's mix (<= 0.5% of C2 rows hit, else prune); G excludes every R5 candidate dataset and close siblings; sealed skeptic; freeze checklist. |
| Day-1 tasks (Sun 18 Oct) | (1) Orchestrator creates the sealed directory, sealed worktree and od-sbx-s request. (2) Fresh sealed Opus (high) writes the sealed brief from the decision-level spec only (taxonomy, counts, statistics, metrics; v3.1 sizes: C 4,400 incl. C-transfer 1,600; G about 10,000 from >= 25 sources; K/X target 1,550 + 1,550, floor 950 + 950; deff 2 everywhere; hard stop Mon 26 23:59). (3) Sealed sessions other than the brief author are NOT started until the brief is skeptic-reviewed and signed (target Mon 19 Oct, after the 15:00 UTC usage reset if usage is tight). |
| Day 2-7 | Mon 19: brief skeptic + signature; matcher-code read; G-source shortlist; names picked ONLY after the manifest v1 freeze. Mon 19-Wed 21: C generators incl. C-CODE generator code; G extraction; sealed image layer. Wed 21: R13 decision point (can G reach about 10,000?). Thu 22: C-CODE execution on od-sbx-s after sandbox sign-off; solver A/B; answerability. Fri 23: reverse pre-check; keyword dry run; validity audit. Sat 24: freeze target 23:59. |
| Kill / stop rule | A sub-block below 80% of target at Sat 24 may keep building until the HARD STOP Mon 26 Oct 23:59 UTC; then every sub-block freezes at its achieved size, its SE is recomputed, a sub-block that breaks its resolution rule is report-only, and the owner is told that day. No slip past Mon 26. Any access-audit violation stops the lane. |

---------------------------------------------------------------------------------------------------------------------
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

---------------------------------------------------------------------------------------------------------------------
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

---------------------------------------------------------------------------------------------------------------------
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

---------------------------------------------------------------------------------------------------------------------
## L-T  Tools and control lane: T54 TOOL-NEED/PICK, T55 RECOVER-ESCALATE, T56 DONE-CLAIM (done-claim half)

v3.2: this lane has additions in "v3.2 LANE ADDITIONS" (L-T) at the end of this file; they bind where they differ.

| Item | Detail |
|---|---|
| Owners | One builder: Sonnet 5.5 high (T54 clean-room). Solver B per family: Sonnet 5.5 high. Scenario and wording pools: Haiku 5.5 medium (rewording only). Opus 5.5 high for G0-lites and A43(d). Skeptic: Sonnet 5.5 high. |
| Inputs | Plan v3 section 1 B.5-B.7; the stripped excerpt of research_v3/tools.md section 5 (items 1-15, 20); Claude-authored tool schemas only (no human-written MCP schemas); tool names from the training-salt namespace. |
| Outputs | Shared tool-scenario engine: Claude-authored scenario templates, a tool dependency DAG builder, a simulated state and ledger, a perturbation manifest (explicit/implicit x transient/permanent, plus ambiguous write), invariant checkers; per-family solvers A/B; rows and gate reports. |
| Gates | Standard pipeline plus (PRE-FREEZE, CPU): T54 call/no-call share 40-60% per sub-block and a surface-feature probe AUC <= 0.55 (bound <= 0.60); limit-awareness block present (tool, parameter and result deletions); T55 ledger gold reproduces the key/read-back/escalate rule; T56 claim text identical across true/false pairs and the claim-only probe AUC <= 0.55 (bound <= 0.60). POST-TRAINING report: T54 per-class recall and logit offset of the trained C2.1. |
| Day-1 tasks (Sun 18 Oct) | (1) Sonnet high writes the three G0-lites with the v3 deltas, the gate split and numeric values (share band, probe bars, distractor-count range). (2) Opus high approves (Mon 19 Oct). (3) Builder starts the DAG builder and ledger simulator (code only). |
| Rows | From Sun 25 Oct. |
| Kill rule | Standard. T56 counts as passed for the floor when its done-claim half passes (T56g is in L-C). |

---------------------------------------------------------------------------------------------------------------------
## L-C  Code lane: T42c CODE-EXEC, T57 PATCH-VERDICT, T56g TEST-GAMING (all clean-room; execution on od-sbx1 only)

v3.2: this lane has additions in "v3.2 LANE ADDITIONS" (L-C) at the end of this file; they bind where they differ.

| Item | Detail |
|---|---|
| Owners | One builder: Sonnet 5.5 high (never opens T42/T43 generators, mutate.py, or OHS-AC). Solver B per family: Sonnet 5.5 high. Haiku 5.5 medium for wording; Haiku 5.5 low runs sandbox batches (stops after 2 failures). Opus 5.5 high for G0-lites and A43(d). Skeptic: Sonnet 5.5 high. |
| Inputs | Plan v3 section 1 B.7 (T56g), B.8, B.9; the stripped excerpt of research_v3/codeexec.md sections 5.1-5.3; pinned toolchains; the signed-off sandbox (from L-0, target Wed 21 Oct). v3.1: SWE-smith problem_statement text is barred (LM-written; arXiv 2504.21798v2 section 2.1). |
| Outputs | Application-style multi-file module generator (Python, JS/TS, Go, bash; each non-Python language >= 8%); our own AST mutator; transform library for test-gaming (8 families, registry ids); execution witnesses in each row manifest; mutation-strength scorer wiring (mutmut/cosmic-ray offline); differential input generator; rows and gate reports. |
| Gates | Standard pipeline plus PRE-FREEZE (CPU/execution, data only): T42c witness rule (3 identical runs; equivalence-yes only by construction plus exhaustive domain); each trace-length bin >= 15% of rows and a length-only probe AUC <= 0.55; T57 four-gate gold (gold-sanity, mutation strength threshold from a 50-module pilot, differential, two-solver); style-only probe AUC <= 0.55 (best-of-4: <= 28%); misleading-comment decoys at 15%; T56g CPU hack-family holdout probe (6 of 8 train, 2 held out, rotated: AUC >= 0.70 while a length-only probe stays <= 0.55); physical separation of visible and held-out suites. POST-TRAINING report: per-bin and per-family comparisons against base 4B; the 300-row slice labelled "Claude-authored, prompted (no library)". |
| Day-1 tasks (Sun 18 Oct) | (1) Sonnet high writes three G0-lites (T42c, T57, T56g) with toolchain pins, the gate split and numeric gate values. (2) Opus high approves (Mon 19 Oct). (3) Builder writes the module generator and mutator as code with CPU-only unit tests that do NOT execute generated code (execution waits for the sandbox sign-off). |
| Rows | From Sun 25 Oct, after the sandbox sign-off and the freeze. 50-module mutation pilot runs first (Sun 25 Oct) to fix the T57 strength threshold. |
| Kill rule | Standard. If the sandbox is not signed off by Fri 23 Oct, L-C keeps writing code, the orchestrator reports the risk to the floor, and T42c/T57 rows start the day sign-off lands. |

---------------------------------------------------------------------------------------------------------------------
## L-G  General rows and voice

v3.2: this lane has additions in "v3.2 LANE ADDITIONS" (L-G) at the end of this file; they bind where they differ.

| Item | Detail |
|---|---|
| Owners | Builder: Sonnet 5.5 high. Solver B for general rows: Sonnet 5.5 high. Haiku 5.5 medium for wording; Haiku 5.5 low runs TTS/ASR batches on od-l4b. Opus 5.5 high for the G0-lite. Skeptic: Sonnet 5.5 high. |
| Inputs | Plan v3 section 2 (general rows, voice recipe) and section 7; research_v3/voice.md sections 6-7; the names-only manifest (L-G's general domains are in the Mon 19 freeze). |
| Outputs | General program-gold generators (multi-step arithmetic, logic, causal and temporal reasoning, tables) with no hard upweight; voice pipeline: our number/code verbalizer (spells every code token; the espeak-ng fallback is disabled), Kokoro-82M round trip (voices graded C or better), acoustic chain (MUSAN, simulated RIRs only), pinned Nemotron EN 0.6B in the LOCKED 560 ms + forced-flush mode, the decision-bearing-span survival check, the program confusion-table noiser (LibriSpeech TRAIN splits only; calibrated to the WER bands), per-run reports; about 7K general rows and about 3K kept voice rows, each voice row with its clean text twin. |
| Gates | General: standard pipeline; domains disjoint from OHS-3/4/5 G by the names-only list. Voice: 100-utterance number-form probe; silence-padding and flush measurement at 560 ms; 500-row WER pilot mapping conditions to bands; band shares met; altered rows dropped and logged; voice share <= 8% of new rows; V0 regression (text vs clean TTS-ASR) on dev; 300-utterance dev robustness slice at 160 / 1,120 ms (eval only). Voice rows stay OUT of the mix manifest until the owner answers R11. |
| Day-1 tasks (Sun 18 Oct) | (1) Sonnet high writes the general-rows G0-lite and the voice G0-lite; L-G's domain names go to L-0 TODAY for the manifest draft. (2) Opus high approves (Mon 19 Oct). (3) Builder writes the verbalizer and span-survival checker (CPU code). Day 2: CPU test that misaki/Kokoro runs with the espeak-ng fallback off (if not, R11(d) goes to the owner and voice rows wait). No od-l4b voice jobs until C2's grid reads finish. |
| Rows | General rows from Sun 25 Oct. Voice probe and WER pilot as soon as od-l4b is free of higher-priority jobs (expected from about Mon 26 Oct); voice pool after the pilot. |
| Kill rule | Standard for general rows. Voice: if the span-survival drop rate leaves fewer than 1,500 kept rows by the data freeze, voice ships at the achieved size; if the V0 check shows a clean-text loss on dev, the voice rows are removed from the mix (drop-only). Voice is the second item in the 90% usage shed order. |

---------------------------------------------------------------------------------------------------------------------
## L-E  Eval harnesses (v3.1 NEW; skeptic 15; eval only, never trained on)

v3.2: this lane has additions in "v3.2 LANE ADDITIONS" (L-E) at the end of this file; they bind where they differ.

| Item | Detail |
|---|---|
| Owners | Builder: Sonnet 5.5 high (never writes or opens training generators). Licence scouting: Haiku 5.5 medium, confirmed by Opus 5.5 high. Skeptic: Sonnet 5.5 high (fresh). Dry-run runner: Haiku 5.5 low. |
| Inputs | Plan section 4; Liu's MIT harness (arXiv 2610.03448) and its scripts; public Tier-1 sets (NotInject, ATBench, ATBench-Codex, When2Call AA protocol) and the BFCL v4 decision subset (Tier 2); the V2-lite real-speech record (if consent covers it); L-I's benign dev split (threshold source). |
| Outputs | One harness per Tier-1 item under our one-token protocol with both option orders; AgentDojo primary threshold from our own non-benchmark dev data and the benchmark-split threshold as a labelled secondary; Jev pinning record (OpenRouter model id + read date); rival licence cards (OpenHands critic-4B MIT fetched 18 Oct; AgentDoG 1.5-4B UNVERIFIED; Strands Decider 2B re-check); base-4B dry-run tables. |
| Gates | Row counts match Liu exactly (AD-Clean 339, AD-Matched 585, AD-Shift 975) or the comparison is labelled "not same-protocol"; every set registered as a G13 target before any C2.1 row; no rival read before its licence is confirmed; Sonnet skeptic of each harness. |
| Day-1 tasks (Sun 18 Oct) | (1) Haiku medium scouts licence cards still UNVERIFIED that the plan relies on for eval: BFCL data files, CRUXEval HF card, LiveCodeBench data, ImpossibleBench data, AgentDoG 1.5-4B weights, Strands Decider 2B, Liu harness script-to-set mapping (scripts/ and reproduce.sh); Opus confirms. (2) Haiku medium reads the VOICE_REAL.md consent/source record and reports whether eval-only reuse is covered (Opus confirms by Sun 25). |
| Day 2-10 | CPU harness build Mon 19 - Tue 27 Oct; base-4B dry runs on od-l4b (queue priority 3) by Wed 28 Oct; Tier-1 reads Sat 7 - Sun 8 Nov. |
| Kill rule | A harness that cannot match the published protocol by Wed 28 Oct is reported as "our protocol, not comparable" rather than dropped. |

---------------------------------------------------------------------------------------------------------------------
## L-D  Deployment measurements (v3.1 NEW; skeptic 15; no training, never Modal)

v3.2: this lane has additions in "v3.2 LANE ADDITIONS" (L-D) at the end of this file; they bind where they differ.

| Item | Detail |
|---|---|
| Owners | Builder: Sonnet 5.5 high. Runner: Haiku 5.5 low. Skeptic: Sonnet 5.5 high. |
| Inputs | Plan sections 6 and 8; ALREADY_TESTED_C1_OPT.md (cold start 131 s, 59% utilisation break-even); C1 merged weights on od-l4b. |
| Outputs | Warm-pool design with a measured cold-start and keep-alive cost; region/hosting-near-users latency table from our client; parity of the L4 path (>= 99.5% argmax vs H100 S1 on dev); batching plan that keeps utilisation above about 59% at the expected load; cost script inputs for the GO #2 cost claim. |
| Gates | Every number tagged author-run with n; parity check identical to the S1 rule; any GPU type other than the free L4 is a money question (R1-type) to the owner, never bought by default. |
| Day-1 tasks (Sun 18 Oct) | (1) Sonnet high writes the measurement plan and the scripts (CPU). Runs start only when od-l4b is idle (queue priority 5). |
| Kill rule | None for C2.1 training; unfinished items are reported as "not measured" in the report. |

---------------------------------------------------------------------------------------------------------------------
## Orchestrator (main session, Opus 5.5 high) day-1 checklist

v3.2: superseded from Mon 19 Oct by the v3.2 orchestrator checklist at the end of this file.

1. Keep C2's GO #1 and training moving; nothing below blocks it.
2. Run get_usage; launch L-0 day-1 tasks and the fresh sealed brief author first (sealed scope only), then the five
   G0-lite writers (one Sonnet high each), L-E scouting and L-D planning; record each lane's day-1 burn.
3. Mon 19: batch the Opus G0-lite approvals, then freeze the names-only manifest v1 (closed allow-list, with L-G's
   domains and the R5 candidate list) and hand it to L-S as names only.
4. Mon 19: send ONE owner message with R4, R5, R6 (widened to every G13 target + scaffolding-hit rule), R11, R12, R13,
   each with its default and needed-by date; R14 (init) the day the C2 report lands. No other questions.
5. Thu 22: run the format exposure probe (dummy rows vs OHS-3/4/AC methods) in a short Mac window; publish hit rates
   (row ids, target, method only) and add any matched scaffolding to the R6 request.
6. Sat 24: after handover remove training identities from od-sbx-s IAP; check Cloud Audit Logs at the freeze.
7. Sun 1 Nov: live Modal credit check (single training account >= 1.25x projection); read Modal's No-Fee terms before
   relying on the relay; any money question goes to the owner that day.
8. Verify every number an agent reports before it enters a plan, packet or HANDOFF. Never give one agent both sides.

---------------------------------------------------------------------------------------------------------------------
## v3.2 LANE ADDITIONS (Sun 18 Oct 2026; Opus planner)

### L-S (sealed; decision level only)
- Inputs added: SEALED_DELTA_v32.md (decision types, counts, calibration protocol) and the names-only copy of names
  manifest v1.1 (Mon 19), both copied into the sealed inputs by the orchestrator. Nothing else from v3.2 crosses.
- Before the freeze: re-check C-transfer names against v1.1 (re-pick any collision before the freeze); re-check the G
  source shortlist against the longer v1.1 R5 candidate list at dataset level (R7 / R13 paths as written).
- Freeze target Sat 24 23:59 and hard stop Mon 26 23:59 are unchanged; new decision types follow the achieved-size rule
  with their floors.

### L-0 (infra) [OWNER-ROW; LEV A1, A2, A15, A19-A21; CRIT B1, B3, B6, I1]
| Item | Detail |
|---|---|
| G13 STAMP SERVICE | Long-lived service on the Mac (the single G13 job) with every registered target pre-indexed once; per-batch API returning row-level stamps (row id, registry sha, method-set version, verdict; hits carry target name and method only). Builder Sonnet 5.5 high; fresh Sonnet skeptic; Opus sign-off. Throughput on 10,000 rows measured by Wed 21 (decides a second-host ruling; never sampling). Never runs during C2's binding G13 |
| STAMP WRAPPER | The only write path for rows in every lane: answer checks (program A = program B, family invariants, names guard, token rule G6, PII scrub, span export) + G13 stamp + manifest stamp; drops logged. CPU tests incl. the ohs3 skip |
| REPLAY CLEAN-UP ONCE | Stamp the whole C2 replay pool against every target after the OHS-5 export loads (Sat 24); done by Mon 26; OHS-AC hits on replay published, not dropped (A79 R4); delta pass only for the Mon 26 hard-stop export |
| MIX GUARD | Mix builder refuses any row without a current clean stamp (CPU test); confirming G13 pass tool (<= 1 h target) |
| RULING-TO-CODE CONFORMANCE | Clause-to-code maps + CPU tests for: split_aware_check.py (A79 R5; A82 1 split-scoped release ON with its 3 conditions; A82 2 CC BY-SA allowed + disclosed, today it is refused; A82 7 CDLA-Permissive-2.0; A82 6 catalogue still refused, per-source only), R4, R6, A46 screen, A42-D 6, A49c, A50 G6, G0 rulings G1-G10, the stamp rules, the L-R caps, the money shed order. Fresh Sonnet 5.5 high writes; Opus 5.5 high signs; record builders refuse without it |
| REGISTRY ADDITIONS | CRIT B1 list + every L-R test/dev split + transitive targets + free-probe items + public-G panel items; Haiku dedupe, Opus confirm; registry sha by Thu 22 |
| NAMES MANIFEST v1.1 | Adds new-family names (T59, T60, T63, T66, T67 and the new heads), one record per L-R dataset and per promoted tasksource source, md_worldbank / md_usgs / md_cma, and the longer R5 candidate list. Opus freeze Mon 19; names-only copy to the sealed side |
| TOOLS | A1 template-level gold-bug audit script; A2 AFLite-style filter; A15 batch-by-dialect sampler (unit test + skeptic); A19 attach audit and A20 batch check in preflight; A21 length histogram; 8.5 batching by source group with a per-source timer (orchestrator runs 8.5) |

### L-A (T50, T51, T53) [LEV A3-A6, A10, A12, A15; CRIT C8, D1, D2]
- G0 addendum (Sonnet high -> Opus): A3 edit-as-action sub-family (1,500-2,500 rows by substitution; T51 scope
  variants); A4 alias rows (300-500); A5 late-binding rows (150-300); A6 gate-directed injection (with the L-I pool);
  A10 cue wrappers (only if the Fri 23 probe says build); A12 perturbation; A15 dialects of the card body; difficulty
  ladder with the mandatory quad; T53 phishing-link head (G7 head rows). G9 cross-family test extended to edit actions
  and to T67 (L-P).

### L-I (T41c) [LEV A6 pool, A10, A12-A14, A16; CRIT C8, D1]
- G0 addendum: A13 benign-worded hijacks + lexical-balance probe; A14 fixed 5% long-input share (only if the Fri 23 probe
  says build); A16 observation formats; A12; A10; difficulty ladder; the Claude-written benign twins for the L-R Gandalf
  and Aya rows (literal ban by program; writers never see it). No direct-injection rows inside T41c.

### L-T (T54, T55, T56 done-claim) [LEV A7, A8, A10, A12, A14, A16; CRIT H2, D1]
- G0 addendum: A7 verification-relevance near-misses (T56); A8 smelly descriptions (T54); A16; A12; A10; A14; T55 LIMBO
  citation corrected (class design unchanged); difficulty ladder. The DAG builder and ledger are exported read-only to
  L-K.

### L-C (T42c, T57, T56g) [LEV A10, A16; CRIT C2, D1]
- G0 addendum: T42c compile / type-check head (about 300 rows by substitution; type-checker component-licence check
  first); A16; A10; difficulty ladder. T63 / T66 / T67 move to L-P; L-C only lends the signed-off sandbox.

### L-G (general rows and voice) [LEV A18, A21; CRIT A4, D3, E2; A79 R11]
- General: about 2,000 rows from third-party generators (Reasoning Gym allow-list, DM Math, bAbI; fresh seeds only);
  hard-extension generators with gold by construction only (G1); generic NOTA option built but OUT of the mix.
- Voice: R11 decided (A79): voice rows may enter the mix after gates and Opus confirmation; A18 generator C inside the
  pool after its dictionary-licence check.

### L-E (eval harnesses) [LEV A27-A29; CRIT E1, F1, F2, B5]
- Public-G panel of UNSEEN public sets (none in block R), item ids registered; base 4B, C1, C2 read on od-l4b before
  GO #1; C2.1 and Jev only inside the R9 read. Seen/unseen flag on every public report row.
- Calibration reporting in both protocols (ours; the aligned top-label, 10 equal-mass bins, 5-fold cross-fitted
  temperature, paired cluster bootstrap); A28 AURC tables; A29 conformal guarantees with ASK rate and false-ASK cost.

### L-D (deployment) [LEV A11, A30-A36; A82 10, 12, 13]
- A30-A36 measurements on od-l4b / CPU with parity records; A11 canonicaliser in the integration wrapper; A82 10
  margin-gated second read measured after GO #2 (adopt only >= +0.3 pp and p95 under Jev's); A82 12 confidence API
  fields after the A27-A29 numbers exist; A82 13 items not built.

### L-R (NEW; public TRAIN-split mappers; block R) [INV; CRIT A1-A6, B1-B5, E5; A79 R5; A82 1-9]
| Item | Detail |
|---|---|
| Owners | Builder: Sonnet 5.5 high (one per source group if usage allows). Records: Haiku 5.5 medium scouts, Sonnet 5.5 high verifies. Opus 5.5 high approves each per-dataset recast table and each tier-C check. Skeptic: Sonnet 5.5 high (fresh). Runs: Haiku 5.5 low |
| Inputs | Plan 16.3; inventory sections 1, 2, 6; the G13 registry (names only); manifest v1.1 records; the stamp wrapper |
| Outputs | Per dataset: record (licence quote, URL, fetch date, provenance enum, A61(b) record, 8.5 PASS id); train-only reader with a CPU no-test-id test; recast table; mapper; stamped rows; set-level report; seen and share-alike flags |
| Gates | Plan 16.3 rules 1-7: eligibility, splits, labels, row format, caps, A46-style screen (> 15% loss to Opus), G13 at creation, set-level once per dataset |
| Day 1-2 | Sun 18-Mon 19: records and readers for tier A, B2, C and the A82 sets (no rows); HotpotQA Opus 8.5 ruling request; tasksource per-source scout starts. Tue 20-Thu 29: 8.5 batches by source group. Rows from Sun 25 |
| Kill / stop | A dataset without a PASS by Thu 29 12:00, failing its check, or losing > 15% to the screen without an Opus OK is left out and logged |

### L-K (NEW; control lane: T59 ASK-OR-PROCEED, T60 CONTROL-NEXT; P0-extra) [CRIT C1; LEV A9]
| Item | Detail |
|---|---|
| Owners | Builder: Sonnet 5.5 high. Program solver B: separate Sonnet 5.5 high session. Wording: Haiku 5.5 medium. G0-lites and A43(d): Opus 5.5 high. Skeptic: Sonnet 5.5 high (fresh) |
| Inputs | Plan section 1 B items 10 and 10b; L-A spec/state model and L-T DAG/ledger as read-only libraries; stripped hardest.md excerpt |
| Outputs | Two G0-lites (2,000 rows each), generators, program solvers, stamped rows, gate reports |
| Gates | Standard v3.2 pipeline plus: T59 PROCEED >= 55%, trigger-only probe AUC <= 0.55; T60 per-head label share 40-60%, "important-looking fact" probe AUC <= 0.55; G9 consistency with T50/T51/T54 |
| Day 1-2 | Sun 18: two G0-lites. Mon 19: Opus approval; code starts. Rows from Sun 25 |
| Kill | Standard; never counts toward the 6-of-9 floor |

### L-P (NEW; P1 repo/config lane: T63, T66, T67) [CRIT C3-C7]
| Item | Detail |
|---|---|
| Owners | Builder: Sonnet 5.5 high. Program solver B: separate Sonnet 5.5 high. Licence-ID table: Opus 5.5 high. Skeptic: Sonnet 5.5 high (fresh). Sandbox batches: Haiku 5.5 low |
| Inputs | Plan section 1 C (v3.2 P1 changes); pinned toolchain stdlib symbol lists (from the L-0 image record); od-sbx1 after sign-off; Checkov and squawk as validators only; L-R rows for DataDog and CommitPackFT |
| Outputs | Three G0-lites; generators; offline registry snapshot (seeded names) for EXISTS; Opus licence table; T66 execution heads; T67 rule table aligned with SLT-1 |
| Gates | Standard v3.2 pipeline plus: T67 validator round-trip drop <= 5% (kill > 10% after the fix); G9 test extended to T67; name-shape and diff-length probes AUC <= 0.55; no real third-party package names |
| Day 1-2 | Sun 18-Mon 19: G0-lites and Opus approval; code. Rows from Sun 25 (execution heads after the sandbox sign-off) |
| Kill | Standard P1 rule (enters only if through gates by the data freeze); first in the usage shed order after the research pass |

## v3.2 Orchestrator checklist (from Mon 19 Oct)
1. C2 first (A81 conditions); nothing below blocks it.
2. Mon 19: batch Opus approvals (new G0-lites, all G0 addenda); freeze names manifest v1.1; copy SEALED_DELTA_v32.md and
   the names-only v1.1 copy into the sealed inputs. No owner message (A79 and A82 answered it).
3. Tue 20-Thu 29: 8.5 batches by source group; publish time per source after batch 1.
4. Wed 21: stamp-service throughput; No-Fee terms result; sandbox sign-off; R14 the day the C2 report lands.
5. Thu 22: format exposure probe; registry sha fixed. Fri 23: free probes and the read-twice zero-shot test on C2.
6. Sat 24: read-twice decision by 18:00; check every conformance record is signed before rows start Sun 25.
7. Thu 29 12:00: declare STRETCH or FALLBACK from measured status; draft the GO #1 packet with R15 if stretch.
8. Verify every number an agent reports before it enters a plan, packet or HANDOFF. Never give one agent both sides.
