# Eval-harness lane scope: plan section 4 + the L-E block

# C2.1 PLAN v3 (Sun 18 Oct 2026, ~02:00 UTC; Opus planner; v3.1 skeptic revision same day; v3.2 merge same day)

v3.2 (Sun 18 Oct 2026, ~07:00 UTC; Opus planner): merges owner Records A79 and A82 (PREREG_FINAL.md), the owner's
18 Oct check-at-creation rule (HANDOFF "OWNER feedback 18 Oct ~04:10 UTC"), C2_1_EXTRA_LEVERS.md ADOPT NOW A1-A36,
C2_1_PUBLIC_TRAIN_INVENTORY.md (new lane L-R) and research_v4/CRITIC.md (new families and every gap). Every change is
marked "v3.2:" with its source in brackets: [A79], [A82 n], [OWNER-ROW] (check-at-creation rule), [LEV An] (extra
levers), [INV] (inventory), [CRIT xn] (critic gap id). The detail tables are in the NEW section 16 (training side only).
The v3.1 text approved by A79 is kept byte-for-byte in C2_1_PLAN_v3_1_A79_SNAPSHOT.md (sha256 27a1fb785918d563…,
the sha A79 cites); where v3.2 and v3.1 differ, v3.2 binds only where it implements an owner decision or is stricter.

## 4. benchmarks_to_report

RULES (as v2): never trained on; all registered as G13 targets with upstreams excluded before any C2.1 row; version,
date and protocol stated; rival numbers are published numbers, cited and tagged; we read only C1, C2, C2.1, base 4B,
Jev, and the v3 same-size rivals; safety results show precision, recall, FPR, TPR at a fixed FPR and the "always unsafe"
baseline, never F1 alone; both option orders read; every Tier-1 result is published. v3: the AA board moves daily, so
every "#1" sentence carries a date stamp and the board is re-pulled on publication day. [landscape 4.3]

v3 BASE ROW: every Tier-1 table gets an untuned Qwen3.5-4B row under OUR one-token protocol; the honest effect size is
gain over base. [landscape 5.3]

v3.2 SEEN FLAG [A82 1; CRIT B5]: every public-benchmark report row carries "train split seen" or "unseen". Headline
claims rest only on OHS-5 and on unseen sets.
v3.2 PUBLIC-G PANEL [CRIT F1, E1] (L-E; report-only; never trained on): a panel of UNSEEN public general sets (no
training dataset, no sibling) with item ids registered as G13 targets. Before GO #1 it measures base 4B, C1 and C2
(od-l4b) as the early G signal and the input to the honest G-gap projection; C2.1 and Jev are read on it inside the
one R9 read, never before. v3.2-r (Sk 10): the projection's training-side arms are in section 16.7.
v3.2 PER-DECISION-TYPE PUBLIC EVAL [CRIT F2]: decision types with no usable public eval say "OHS-5 only"; public
report-only sets are used where their licences allow. No public number is invented. v3.2-r (Sk 10): the per-type
list moved to section 16.7 (training side).
v3.2 CALIBRATION REPORT [LEV A27]: every calibration table names its protocol; the comparison with Jev uses the
protocol-aligned ECE (section 3); "Jev 6.0" is OUR protocol's number and is never quoted alone.

TIER 1 (v3 list; the claim gate on public data)
1. When2Call MCQ, AA protocol (3,423 of 3,652 items; 229 "ask for more info" removed; four shuffled replies; argmax).
   Bar: Celeris-1 84 and GLiDE 84 (AA article 13 Oct 2026, independent, rounded); Jev 1.13 81 (same). d1-ultra 92.6 is
   aggregator-only and conflicts with other reports: UNVERIFIED, drives nothing. We read Jev 1.14 ourselves. v3 claim:
   "ahead of Jev 1.14 under the AA protocol, measured by us, with CI"; we do not forecast #1. Note the label-noise
   ceiling (paper: question quality 82-92% by section, author-run). [landscape 5.4; tools C1-C2]
2. AgentDojo as a detector, our pre-registered protocol built with Liu's MIT harness (arXiv 2610.03448, independent,
   single-author preprint): AD-Matched and AD-Shift reported separately; score = 1 - P(ALLOW) - P(ALLOW_BENIGN) (ASK
   counts as flagged; P(BLOCK)-only is the pre-registered secondary); v3.1 (skeptic 16): the PRIMARY 1%-FPR threshold
   is frozen from OUR OWN non-benchmark injection dev data (a benign dev split never trained on), matching OHS-5's rule;
   the threshold fit on a task-disjoint benign split of AgentDojo's own pools is a labelled SECONDARY ("benchmark-split
   threshold"); pre-registered tie rule; also the default-threshold numbers, AUROC, task-level block rate, and the
   "same-set threshold" number labelled favourable (Liu's method).
   Row counts must match Liu's exactly (AD-Clean 339/97 tasks, AD-Matched 585/432, AD-Shift 975/720) or the comparison
   is not same-protocol. Best published point: Horizon-Labs guard-base 82.2 / 87.9 (independent; trained on agent data;
   weights changed 2 Oct 2026). Realistic comparators: Prompt Guard 2 86M 69.4 / 78.8; 7-8B task-aware judges 55-64.
   No forecast range (v2's 55-80 had no support). To beat 82.2 our paired LB needs a point near 86%+ (DERIVED).
   [injection 5.2 P-A to P-D]
3. "InjecAgent as detector", defined as Liu's TB-Matched construction (62 InjecAgent attacker instructions in tau-bench
   product names; 584 injected / 1,533 benign); labelled "our protocol", never "the InjecAgent benchmark". Horizon 100.0
   on it cannot be beaten, so this is a report line, not a #1 candidate. [injection P-F]
4. NotInject (339 benign, MIT, eval only): over-defence accuracy and FPR in user-turn framing (published comparators)
   and tool-result framing (ours, no comparator); Wilson 95% upper bound; per trigger-word subset. Best published:
   Horizon 94.4 / FPR 5.6% (vendor, v2.2 card). Claim "FPR below 5%" needs at most 9 false positives of 339; beating
   Horizon's 5.6% point needs at most 10 (DERIVED). [injection P-G; landscape 4.1]
5. ATBench-Codex (500; Apache-2.0): accuracy bar 84.4 (AgentDoG 1.5 unified 4B, author-run, paper text); F1 bar 83.8
   (AgentDoG v1); base Qwen3.5-4B 78.0 acc under AgentDoG's protocol (author-run). Pre-registered compaction (user turns
   plus the last N calls, <= 1,536 tokens) and a chunked full-trajectory read (max p(unsafe) over windows). [landscape
   C3]
6. ATBench (1,000): F1 bar 77.7 (AgentDoG 1.5 unified 4B), then GPT-5.4 76.7, AgentDoG 1.5-4B 74.3 (all author-run,
   same table). Report against the best row, not the weaker one. Honest expectation: a per-call gate may lose to a
   trajectory judge on whole-trajectory labels. [landscape C2; sealed C-licence note]
CLAIM RULE (as v2): "#1 among models with published numbers on <benchmark, protocol>" only if our paired 95% LB is above
the best published point estimate; otherwise we state our rank.

TIER 2 (report only, own framing, never in a "#1" claim)
- v3: BFCL v4 decision categories (relevance, irrelevance, live_irrelevance, miss_func, miss_param) on an item subset we
  read and found clean; Epoch rated BFCL v4 "Flawed" (24 of 50 sampled items defective, independent); n=16 relevance
  items in the third-party Jev run allows no CI. [tools C3; landscape C9]
- v3: CARE-style protocol on our own held-out commands, labelled "not comparable" (CARE's 549-command split is not
  released). [landscape C5]
- MCP-Atlas public 500: v3 scored only on steps whose next tool is uniquely forced by data flow (the trajectory is one
  valid path, not the only one). [tools C4]
- CRUXEval-O/I as multiple choice; v3 EquiBench Python pairs; gated against base 4B, not generative numbers.
- v3 AgentProcessBench: reference replaced by the author table (best Gemini-3-Flash-Preview-Thinking 81.6 StepAcc;
  Qwen3-4B 55.9; humans agree 89.1%); the "79.1 vs 66.8" figure appears nowhere in the paper. [tools C5]
- v3 SteerBench-Work (106 scenarios; runner MIT, scenarios CC BY 4.0). [permission 5.19]
- v3 MSB (MCP signature/response carriers; MIT). [injection P-H]
- v3 Impossible-LiveCodeBench / Impossible-SWEbench item-level ("can this be passed honestly?"), only if a data licence
  is stated by the report date; otherwise skipped and said so. [codeexec T56-5]
- Saber harm rate; fresh SWE-bench-Live/SWE-rebench patch verdicts (labels inherit weak-suite error rates); Jev Decision
  Index Tools area; JevBench coding topic sanity only, no submission.
- v3 WildGuardTest (AA subset 835, ODC-BY) as a one-line report because it is 25% of the AA index. [landscape 4.1]
NOT REPORTED: AmPermBench, R-Judge, TraceSafe (NC or unclear licence; decided, no owner question); end-to-end tau2,
Terminal-Bench, SWE-bench; AuthGateBench (no data licence); TRACE (share-alike, not needed); UnderSpecBench, OverEager,
CARE split (unreleased).

UNVERIFIED NUMBERS DRIVE NO DECISION: d1-ultra 92.6; all BenchLM-mirror rows (Jev 1.14 80.8 / 78 ms, Microsoft-Decision-
1); "Jev let 3 of 30 through"; the eBay Jev injection numbers are independent but prompt-specific (one fixed prompt, no
CIs) and are quoted only as "a third party measured Jev on a pooled cohort". [landscape; injection 1.2]

v3.1 JEV PINNING (skeptic 32): the OpenRouter model id and the read date are recorded before the read, and every claim
reads "Jev 1.14 as served on <date>". If the served model changes before Sat 7 Nov, the change is recorded and Jev is
still read once only (no second read).

v3.1 RIVAL LICENCES (skeptic 31): no rival is read before its weight licence is confirmed (Haiku scouts, Opus
confirms). Status 18 Oct: OpenHands critic-4B: MIT (https://huggingface.co/OpenHands/openhands-critic-4b-v1.0, fetched
18 Oct 2026, vendor card). AgentDoG 1.5-4B: UNVERIFIED (the HF page returned HTTP 401 to an anonymous fetch, 18 Oct
2026). Strands Decider 2B: Apache-2.0 per research_v3/landscape.md, re-checked by L-E before the read.

CLAIM WORDING (as v2): "#1 measured on X among published numbers (date)"; "beats Jev 1.14 by X (CI) on OHS-5
C-transfer"; never "beats every model". v3: say "no published coding-gate numbers with n >= 100" rather than "rivals
publish none" (CLM-8B and Strands publish small or example-only numbers). [landscape C10]

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

### L-E (eval harnesses) [LEV A27-A29; CRIT E1, F1, F2, B5]
- Public-G panel of UNSEEN public sets (none in block R), item ids registered; base 4B, C1, C2 read on od-l4b before
  GO #1; C2.1 and Jev only inside the R9 read. Seen/unseen flag on every public report row.
- Calibration reporting in both protocols (ours; the aligned top-label, 10 equal-mass bins, 5-fold cross-fitted
  temperature, paired cluster bootstrap); A28 AURC tables; A29 conformal guarantees with ASK rate and false-ASK cost.
