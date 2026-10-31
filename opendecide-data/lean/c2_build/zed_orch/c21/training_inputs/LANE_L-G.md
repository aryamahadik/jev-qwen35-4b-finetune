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

### L-G (general rows and voice) [LEV A18, A21; CRIT A4, D3, E2; A79 R11]
- General: about 2,000 rows from third-party generators (Reasoning Gym allow-list, DM Math, bAbI; fresh seeds only);
  hard-extension generators with gold by construction only (G1); generic NOTA option built but OUT of the mix.
- Voice: R11 decided (A79): voice rows may enter the mix after gates and Opus confirmation; A18 generator C inside the
  pool after its dictionary-licence check.
