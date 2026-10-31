# Deployment lane scope: plan sections 6, 8 + the L-D block

# C2.1 PLAN v3 (Sun 18 Oct 2026, ~02:00 UTC; Opus planner; v3.1 skeptic revision same day; v3.2 merge same day)

v3.2 (Sun 18 Oct 2026, ~07:00 UTC; Opus planner): merges owner Records A79 and A82 (PREREG_FINAL.md), the owner's
18 Oct check-at-creation rule (HANDOFF "OWNER feedback 18 Oct ~04:10 UTC"), C2_1_EXTRA_LEVERS.md ADOPT NOW A1-A36,
C2_1_PUBLIC_TRAIN_INVENTORY.md (new lane L-R) and research_v4/CRITIC.md (new families and every gap). Every change is
marked "v3.2:" with its source in brackets: [A79], [A82 n], [OWNER-ROW] (check-at-creation rule), [LEV An] (extra
levers), [INV] (inventory), [CRIT xn] (critic gap id). The detail tables are in the NEW section 16 (training side only).
The v3.1 text approved by A79 is kept byte-for-byte in C2_1_PLAN_v3_1_A79_SNAPSHOT.md (sha256 27a1fb785918d563…,
the sha A79 cites); where v3.2 and v3.1 differ, v3.2 binds only where it implements an owner decision or is stricter.

## 6. serving

BASE PATH (as v2): SGLang S1 serving the merged bf16 model; argmax agreement with the HF adapter >= 99.5% on dev;
identical rendered-prompt sha in trainer, gate and server; any re-render gets a new parity record. v3: the parity check
also asserts thinking is OFF in every rendered prompt (Qwen3.5 thinks by default; disabled via enable_thinking False;
Qwen3.5-4B card, fetched 18 Oct 2026).

LATENCY AND COST TARGETS (as v2, indicative): gate calls 12-20 ms, tool/control 15-25 ms, code 20-35 ms server p50 (H100
batch 1); end-to-end p50 near users about 75-85 ms. v3 CLAIM LIMITS [landscape C7-C8]:
- Compare latency with hosted decision models measured by OUR client under the same conditions (our measured Jev e2e
  156 ms). AA's per-task medians (Celeris 63 ms, Jev 1.13 127 ms) are medians across all four index evals with no stated
  method, so they are context, not a like-for-like bar. Rule engines (CARE 2.3 ms) and DreamGuard (25 ms, author-run) are
  named as faster or similar classes; no "fastest" claim over them.
- Price in the rival's unit: Jev lists $0.042 per M input tokens, output free (docs, verified 18 Oct). Our cost is a
  hosting cost; the earlier C1 measurement found it cheaper than Jev only above about 59% utilisation, so any cost claim
  states the utilisation it assumes.
- Calibration claims name the protocol (Jev 6.0 ECE is our own measurement; Liquid's vendor claim of Jev 2.7 uses a
  different suite). v3.2 [LEV A27]: an independent protocol measured Jev 1.13 at 3.3% / 3.2% on typed decisions; any
  "better calibrated" claim follows the section 3 claim rule (aligned ECE <= 3.0%, paired win).

SPEED CHANGES THAT DO NOT CHANGE ANSWERS (as v2): exact batch-1 bundle; policy-card prefix caching; hosting near users,
keep-alive, warm pool, cheapest host meeting targets.

v3.2 SERVING AND DEPLOYMENT LEVERS (no training; L-D on od-l4b or CPU; never Modal) [LEV A30-A36]: A30 breakable
prefill CUDA graph with a text-only hot-path server (first read the B1a log, which says graph == eager); A31 SGLang
0.5.21 /v1/score with label_token_ids on OUR rendered prompt (never /v1/decisions), short-prefill scheduler flags, chunk
size that never splits a prompt, optional sliced LM head; A32 radix-cache ON vs OFF A/B on the real request mix before
any prefix-cache saving is counted; A33 persistent local sidecar for the coding-agent hook (warm HTTP/2 over a unix
socket, fail-closed fallback; first check how the hook process is spawned); A34 exact-match decision cache keyed by the
rendered-prompt hash + policy version, hashes only; A35 L4 fast-path ms/decision and $/1K curve; A36 hardened chunk
reads for tool outputs above 256 tokens (overlapping windows, contiguity-gated aggregate, view alignment; else ASK).
Every one that touches the served path needs a >= 99.5% argmax parity record, with A31's flip rate measured under
MIXED batches and cold vs cached requests (temperatures refit on the served path if they drift).
v3.2 [A82 10]: margin-gated second read with permuted options for low-margin items: MEASURE on od-l4b dev after GO #2;
adopt only at >= +0.3 pp with p95 under Jev's measured p95; it changes answers, so it joins R8 as dial (e) with its
own parity statement. [A82 12]: confidence API fields (calibrated probability on every primitive incl. yes/no, defined
`confidence`, published ASK thresholds per type, `calibration_version`, reliability diagram per type) are ADDED as
additive fields once the A27-A29 numbers exist. [A82 13]: multi-field single read, 2B student/cascade, paid extra
regions or GPU tiers and a batch pricing tier are NOT in C2.1 (C2.2 design / owner pricing later).

CHANGES THAT CAN CHANGE ANSWERS (OWNER-RESERVED, after measurements; section 10 R8): one read per choice question;
v3.1: FP8 serving only via the R12 FP8-KL-trained weights at >= 99.5% parity (block-FP8 at 98.38% and the FP8 margin
gate are recorded FAILED on C1 and are not re-planned; ALREADY_TESTED_C1_OPT.md); v3 PriDe-style per-letter prior
offset (zero added calls; needs a new S1 parity statement; tested only on untuned models) [recipe 5.4]. v3.1: the
selective-thinking tier is REMOVED (THINK_MODE_MEASURED.md, orchestrator decision 18 Oct: about 0 gain on OHS-1/2,
every think policy failed the A17 B1 "e2e median <= 1 s" rule, about 5-7x average cost).

v3.1 DEPLOYMENT WORK (no training; lane L-D in the build order; skeptic 15): warm pool (no 131 s cold start), hosting
region near users, cheapest GPU that keeps parity (measured on od-l4b; other GPU types cost money and go to the owner
as an R1-type question), batching plan to keep utilisation above about 59%. Never on Modal.

CASCADE PRODUCT (as v2): Stage 1 calibrated p(block); three operating points with FPR/FNR on sealed C-PERM; an ASK band
to a human or the customer's bigger model. v3: ASK is shown with an escalation-vs-risk curve (coverage vs error), not as
free recall (eBay paper: deferral helps only with a strong reviewer). [injection P-J]

INTEGRATIONS (product work, no training): Claude Code PreToolUse hook (allow/deny/ask JSON, reason category, fail-closed
option); adapters for Codex, Cline and OpenHands; an MCP server. v3: the hook's default view matches the training
primary view (user messages plus tool calls; tool outputs stripped).

## 8. orchestration_and_parallel_lanes

MODEL TIERS (v3, from ORCHESTRATION_RULES.md; set `model` on every agent; never Fable)
| Work | Model | Effort |
|---|---|---|
| Orchestrator: plans, rulings, GO packets, 8.5 runs, verifying every agent's numbers | Opus 5.5 (main session) | high |
| Design/judgment: plan synthesis, ruling drafts, plan/ruling skeptics, OHS-5 brief, sealed freeze sign-off, A43(d) confirmations, G0-lite approvals | Opus 5.5 | high |
| All code: generators, solver A, independent solver B, executor, tools, G13/select/mix runs needing judgment, trainer, eval harnesses | Sonnet 5.5 | high (routine runs medium) |
| Code reviews and build skeptics (fresh agent, did not write the code) | Sonnet 5.5 | high |
| Research and research refuters | Sonnet 5.5 | high |
| First-pass adjudication of blind-read disagreements | Sonnet 5.5 | medium |
| Blind reads (G5-H, G9, answerability), wording pools, licence scouting, extraction, counting, running known scripts, log condensing, HANDOFF drafts | Haiku 5.5 | medium (mechanical: low) |
Haiku script-runners stop and report after 2 failed attempts. Any Haiku result that decides a gate is checked by the
next tier. Every prompt carries the no-probing and sealed-access rules; clean-room agents also get "never open the T27
or T40-T46 generators, templates or OHS-AC".

ORCHESTRATION RULES (v3, [ORCH]): critical path C2 > OHS-5 sealed build > C2.1 generator code > C2.1 rows; one writer per
file set (overlapping writers get worktrees); single-resource locks (Mac G13 one job at a time and never overlapping
C2's binding G13; od-l4b GPU one job at a time; Modal training only; execution only on the disposable sandbox); every
build gets an independent skeptic, every ruling an Opus skeptic; blind readers get Read + Write on their own files only;
access audit on every read batch; pipelines by default, loops capped, no silent caps; usage measured with get_usage
before every large launch (ping the owner at 96%, never cross 98%); never idle (prepare the next step's tools while
long jobs run); no placeholder arguments; agents read files, not pasted summaries.

USAGE: measured, currently low. Weekly reset Mon 15:00 UTC (19 Oct, 26 Oct, 2 Nov, 9 Nov). v3 correction: v2 said
07:00 UTC. v3.1 (skeptic 25): the orchestrator records the MEASURED day-1 burn per lane (get_usage before and after
each lane's first launch) and publishes a per-lane weekly projection on Mon 19 Oct. Pre-registered SHED ORDER at 90%
weekly usage: (1) pause wave-C (P1) families, (2) pause the voice pool, (3) pause general rows, (4) pause the remaining
training lanes; L-S, C2 and the GO steps are never shed. At 96% the owner is pinged (memory rule: ping, not stop);
never cross 98%.
v3.2 USAGE SHED ORDER [CRIT I2] (replaces the list above): (1) the optional research pass of CRIT I3 and tasksource
scouting beyond sources already promoted; (2) wave-C (P1) families in L-P and the P1 realism slices; (3) the voice
pool; (4) L-R tier-C datasets whose mechanical check is still open; (5) general rows; (6) remaining L-R datasets;
(7) remaining training lanes. L-S, C2, the G13 service, the GO steps and the confirming G13 are never shed.

MACHINES
- G13: serial on the Mac, alone; never overlapping C2's capture or binding G13.
  v3.2 [OWNER-ROW; CRIT B3]: G13 becomes a long-lived STAMP SERVICE on the Mac (one job, the lock holder) with every
  target pre-indexed once; lanes submit row batches and get back row-level stamps (row id, verdict, target name and
  method only). L-0 measures its throughput on 10,000 rows by Wed 21 Oct; if it cannot keep up with generation, a
  second G13 host is an orchestrator ruling (never sampling). The service never runs while C2's binding G13 runs.
- od-l4b (free L4): heavy agent CPU, all model reads (C2 trap reads, rival reads, base reads), TTS/ASR for voice.
  One GPU job at a time; C2's grid reads go first. v3.1 (skeptic 23): queue priority (1) C2 jobs, (2) C2 reads of
  C2.1 candidate rows, (3) L-E base-4B harness dry runs, (4) voice probe/pilot/pool, (5) L-D deployment measurements.
  L-0 measures throughput per job type (rows/hour) by Wed 21 Oct and publishes a queue plan with expected finish
  dates. C2 reads of C2.1 rows are NOT a kill gate: a family whose C2 reads are queued at the data freeze is still
  "through" if every data gate passed; its trap selection finishes in the Wed 4 Nov window.
- v3 od-sbx1 sandbox (execution gold only) [codeexec 5.4]:
  - Disposable CPU-only GCE VM on free credit, in its own VPC with no peering, NAT, Private Google Access or VPN; no
    external IP; no service account and no scopes; project SSH keys blocked; no data disk; Shielded VM with Secure Boot;
    --max-run-duration with DELETE as the termination action (flags confirmed on the gcloud reference).
  - Egress DENY all (IPv4 and IPv6); ingress only TCP 22 from the IAP range 35.235.240.0/20. Because Google always
    allows VM-to-metadata traffic, the host drops 169.254.169.254 and fd20:ce::254 for every UID except root and the
    guest agent, and every sandbox runs with --network=none.
  - Container runtime gVisor runsc (systrap platform; no nested virtualisation, no Firecracker in P0); one container per
    run (read-only root, cap-drop ALL, no-new-privileges, pids/memory/CPU/fd/file-size limits, nobody user, tmpfs /work);
    timeouts enforced from outside; stdout/stderr capped at 64 KB; 2 runs per execution (3 for will-this-test-fail),
    mismatches dropped and counted.
  - Images built on a separate build VM (od-sbx-build: egress, no data); the sandbox VM never pulls anything; runsc
    installed from the apt repo or tarball (the legacy auto-download path was retired at end of Sep 2026).
  - Data in and out over IAP-tunnelled scp only (the scp flag is UNVERIFIED; test it, fallback = IAP ssh with stdin).
  - Re-imaged per batch (at most one hour or N executions); image id, runsc and kernel versions in every manifest.
  - Executor self-test at every VM start (network, metadata, docker.sock, write-outside-/work, mount/ptrace/unshare,
    fork/memory/disk bombs, infinite loop, 1 GB stdout, a T56 tamper test, determinism, pinned versions); any failure
    aborts the batch. A Sonnet skeptic reviews exactly this list and Opus signs off before first use.
  - Fallbacks: nsjail (Apache-2.0) in the same VM; then rootless podman with crun; Firecracker only after a nested-virt
    machine type is confirmed. Never od-cpu1 or any data host.
  - v3: the sealed side uses a separate VM instance from the same reviewed image (od-sbx-s), with its own scp scope.
    v3.1: plus its own sealed image layer and no training identities on its IAP after handover (section 3).
- Modal: training only.

LANES (details, day-1 tasks and owners in C2_1_BUILD_ORDER.md)
- L-S sealed OHS-5 (separate sessions). L-0 infra. L-A T50/T51/T53. L-I T41c. L-T T54/T55/T56 done-claim. L-C T42c/T57/
  T56g. L-G general rows and voice. v3.1 (skeptic 15): L-E eval harnesses (Tier-1 + V2-lite; eval-side agents never
  write training generators and training lanes never open L-E files) and L-D deployment measurements (free GCP / od-
  l4b only, never Modal).
  v3.2 NEW LANES: L-R public train-split mappers (block R) [INV; CRIT A1]; L-K control lane T59/T60 [CRIT C1]; L-P P1
  repo/config lane T63/T66/T67 [CRIT C3-C7]. Each has one builder (Sonnet high), program solver B written by a separate
  Sonnet high session (G0 ruling G1), Haiku wording/scouting, Opus approvals, a fresh Sonnet skeptic.
- Per family: G0-lite (Opus) -> generator code (no rows) -> template/wording-pool hash export -> [OHS-5 freeze] ->
  1,000-row pilot -> 200-row G13 pilot -> gates (A50 G6, A49c, G5-H, G3-H, family shortcut gates) -> full generation ->
  C2 reads on od-l4b (pipelined) -> one fix iteration if needed -> kill rule.
  v3.2 [OWNER-ROW] REPLACED BY: G0-lite (Opus) -> generator code (no rows) -> ruling-to-code conformance record ->
  hash export -> [OHS-5 freeze] -> 1,000-row pilot WITH every row G13-stamped and answer-checked at generation ->
  set-level gates once on the pilot -> ONE combined fix if anything fails (G3) -> full generation, every row stamped
  at generation -> set-level gates once on the built family -> C2 reads (pipelined; trap selection, A46 screen on L-R
  rows; not a kill gate) -> kill rule. Section 16.1 has the steps.
- Wave C (P1) starts when a lane frees up, on measured progress.
- One binding G13 window, then selection, mix, d2-set, final-mix 8.5, preflight, GO #1.
  v3.2 [OWNER-ROW]: the binding G13 is ONE CONFIRMING PASS over the final mix (target <= 1 h; expected 0 drops because
  every row already carries a current clean stamp; any hit is a drop-only and a defect report on the inline check).

KILL RULE: a family that fails its gates after its one fix iteration, or is not through its gates at the data freeze,
rolls to C2.2/C3 (logged). If the floor (6 of 9 plus one code family) is missed at the freeze, the orchestrator stops
and reports at GO #1.

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

### L-D (deployment) [LEV A11, A30-A36; A82 10, 12, 13]
- A30-A36 measurements on od-l4b / CPU with parity records; A11 canonicaliser in the integration wrapper; A82 10
  margin-gated second read measured after GO #2 (adopt only >= +0.3 pp and p95 under Jev's); A82 12 confidence API
  fields after the A27-A29 numbers exist; A82 13 items not built.
