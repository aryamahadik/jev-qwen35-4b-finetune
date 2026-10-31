# MAP: 1 Oct report → 3 Oct report

Mapper output for the 3 Oct rebuild. It was written on 4 Oct at 01:05 UTC (3 Oct, 9:05 pm EDT).

- **Old report:** `reports/OpenDecide_Full_Status_1Oct.pdf` (62 pages). It was built on 3 Oct at 01:51 UTC, with HEAD at c35de00.
- **Old builder:** `reports/pdf_build_1oct/build.py` (4,309 lines).
- **New output:** `reports/OpenDecide_Full_Status_3Oct.pdf`. Its builder and scratch files go in `reports/pdf_build_3oct/` only.

Verdicts:
- **KEEP**: keep as-is.
- **UPDATE**: update the numbers or labels, keeping the structure.
- **REWRITE**: new content.
- **HISTORY**: condense into a history appendix, or drop.
- **NEW**: a section that does not exist yet.

Line numbers refer to `pdf_build_1oct/build.py`. Page numbers refer to the 1 Oct PDF.

---------------------------------------------------------------------------------------------------------------------

## 0. What changed since the 1 Oct PDF, and why most of it is stale

The 1 Oct PDF stops at "A8′ committed, ready for step 0b". Everything after that is missing from it.

| UTC (3 Oct unless noted) | Event | Source (allowed files) |
|---|---|---|
| 01:47 | A8′ committed | git c35de00 |
| 02:10 | **Step 0b probe-go = NO GO.** C1 flipped 87/252 pairs (34.52%) and 4B-E 86/252 (34.13%), a difference of +0.40 pp [−5.86, +6.75]. The rule needed ≥ +3 pp with LB > 0. No C4 was trained and $0 was spent. | PREREG_FINAL A10 §A (committed text). `logs/gate4b_fix2/` was never pulled to the Mac. |
| 03:10 | **A10: owner override. C1 = `q35_4b_main500k` (sha 507d1c29…) is the shipped 4B.** The failed conditions are disclosed. The 2B keeps 4B-E's 2-view labels, with no relabel. OHS-3 overlap: 7 golden_train units, so OHS-3 is reported with and without those items. | git 132cd2a; PREREG_FINAL A10 |
| ~03:40 | JevBench v1.5.4 public on C1 with the band-edge readout: I 75.1 vs Jev p1 63.2 (+11.9 [+3.0, +21.3]); Score A 74.34 vs 68.80. 4B-E band edge: 78.7 / 75.81. C1 is weaker than 4B-E on hard yes/no (47.4 vs 57.9). | `B/v154/RESULTS_30sep.md` "3 Oct" section; `B/runs/scores_v154_c1.json` |
| 04:04 / 04:38 | ejs-5 pre-registration, then the result. **C1 54.1% vs Jev 58.5%: −4.4 [−7.8, −0.9], a LOSS.** 4B-E (report-only) scored 54.5%. Rows dated 2026-06-01 or later (268): 46.3 vs 45.9, a tie. | git 9a04df1, 065191c, 32ee1f9; `B/ejs5/runs/scores_c1_4be.json` (aggregates only) |
| ~04:45 | **New owner direction.** The 4B only; the 2B is PAUSED. Up to about $100 GO for 4B training, keeping a $25 reserve. Goal: match or beat Jev on unseen-domain accuracy (−1 acceptable, +1-2 target). | ORCH (memory final-goal-30sep.md) |
| 04:49 → 07:33 | A11, step B (WiSE-FT weight softening): **keep C1**. a*=0.9 scored +0.05 [−0.30, +0.40] on unseen rows (select); confirm −0.10 (needed +0.5). | git c11e4a9, 599c513; `L/logs/b_wiseft_result.json` |
| 04:57 → 08:43 | A12, the OHS-1+2 yardstick. **OHS-1: C1 80.4 vs Jev 81.7, −1.2 [−2.9, +0.4], a tie. OHS-2: 81.0 vs 81.5, −0.6 [−2.2, +1.1], a tie. Pooled ≈ −1.0.** Jev has the better Brier. OHS-1 and OHS-2 are now PRACTICE sets. | git 86f59dd, 629a9f4; `L/logs/A12_ohs12_result.md` |
| 05:50 → 16:30 | Plan C research: 7 web angles, local gaps, 2 skeptics, 6 extra studies and an addendum (14 ADOPT rows). Spec and recipe went v3 → v4 FINAL. | `L/c_spec/*.md` (NOT `c_spec/sealed_brief/`) |
| 14:27 | A13: Decision Index SAMPLE on C1 (report-only) | git 8f1a9eb |
| 15:01 | A14: sealed new-domains suite build rules | git a79e5d4 |
| 20:34 | **A15: sealed suite v2 frozen.** 7,302 items: select 2,988 / confirm 4,314. Part A has 6,205 items in 8 domains. The non-adjacent ids D1, D10, D11, D12 hold 55.5%; the adjacent ids are D2-D5. P 600, B1 298, B2 199. v1 failed the adjacency rule. An isolation incident is disclosed. | git 3abd721; PREREG_FINAL A15 (domain IDS only) |
| 20:35 | **A16: C round-1 plan.** 150K rows = 90K replay + 60K new (own families 45,250, public 8,750, commits 6,000). Seed 20261003. Config `runs/q35_4b_c_r1.json`. Ship gate: sealed part-A confirm ≥ +1.0 pp with LB > 0 plus guards D1-D6 and D9. Round 2 only if select ≥ +2.0 with LB > 0. | git 27d8b0a |
| 23:57 | **A16.1 tool pins + Decision Index result: C1 sample index 54.83 vs Jev v0.1 59.51 (−4.7).** Knowledge area −17.65 pp; language −1.79, retrieval −2.85, tools −0.05, arts −1.07. C1 would sit #4 on the v0.1 top-5 board (the sample is not paired). | git 18c024c; `B/decision_index/report_sample10k.json` |
| 4 Oct ~00:00 | Replay read started on od-l4b: 134,582 C1 reads over the 99,069-row draw, ETA about 11-12 h. Memory says it runs slower than the estimate. | ORCH; `L/c_build/f2_l4.json` (F2 check on the L4), `RUNBOOK_replay_reads.md` |
| 4 Oct 00:40-00:55 | Phase 2 family builds. G0 specs are freezing per family (sha logged); generators have started for F2 and F6. | `L/c_build/progress_phase2.log` |
| 4 Oct ~01:15 | Knowledge-gap research is running (whl9uhvgk). Its 5 `R_*.md` files exist; `PLAN_knowledge_gap.md` does NOT exist yet. | `reports/knowledge_gap/` |

Everything in the 1 Oct PDF that rests on the following is now **stale**:
- **The old goal:** beat Jev with 4B + 2B + cascade.
- **The fix2/C4 plan:** fix2/C4 never trained after the 0b NO GO.
- **"Fallback = 4B-E":** C1 now ships by override.
- **The 2B plans:** teacher, relabel, A/B, 2B main ~$74, cascade. All are paused.
- **The 26-row roadmap and the $113-117 budget plan.**
- **The 30 Sep / 1 Oct projections and odds.**
- **Every "next step" or "GO point" line.**

---------------------------------------------------------------------------------------------------------------------

## 1. Section-by-section map

### Front matter

| § | build.py lines | PDF pp | Verdict | Why / what to do | New sources |
|---|---|---|---|---|---|
| Docstring, constants | 1-50 | – | UPDATE | Set `SCR=reports/pdf_build_3oct`, `OUT=…_3Oct.pdf`, `OLD_PDF=…_1Oct.pdf`, plus the doc title, header and subject (4241-4290). Drop `TASKS` (see §3). | – |
| Title + subtitle + tag legend | 1281-1297 | 1 | REWRITE | Title: "status record, 3 Oct 2026 (evening EDT)". Audience: **the founder first** (plain, short sentences), then verifiers. It replaces the 1 Oct record, which is kept unchanged. | – |
| §1 "Where we stand" note | 1299-1318 | 1 | REWRITE | Mostly about fix2 readiness, LEFT/READY_S, the 4B-E fallback and the old budget. It must say: shipped = C1 (A10, failed conditions disclosed); the 4B is the only focus; plan C is in progress. Then one line each for the 3 Oct results: JevBench public win, ejs-5 loss, OHS-1/2 ties, DI −4.7, B no gain. Then: sealed suite frozen, round 1 being built, money and ETA. | §0 table |
| §1 metric table | 1319-1349 | 1 | UPDATE | "Our best measured" should mean the **shipped C1**: OHS-1/2 from A12, not v11c; JevBench public from the C1 band-edge row. Add rows: ejs-5 (LOSS), Decision Index sample (behind −4.7, report-only), OHS-1/2 Brier (Jev better). Keep the LIVE security rows (C1 = `q35_4b_main500k`, unchanged). Drop the "2B PRISM-X I 1.1%" mention. Keep the "dev unseen +2.47" and "(e) 8.86% vs 5.68%" rows, but label them "C1 vs 4B-E, gate job 1 (DO NOT SHIP; overridden by A10)". | A12 md; RESULTS_30sep.md; scores_c1_4be.json; report_sample10k.json |
| "Honest odds" table | 1350-1355 | 2 | REWRITE | Every cell is a 30 Sep or 1 Oct EST (4B/2B/cascade era). Replace with the **3 Oct ORCH EST**. OHS-3: +0.8 vs Jev median, tie-or-better ~60%, ≥ +1 about 45%. New-domains: +1.5 over C1. ejs-5 after C: ~58-62 (in-domain now). JevBench sealed: Score A ~72-75 (beat Jev ~65%), I ~66-72 (beat ~30%). LongBench: likely loss. Recipe power: ~77% at a true +2, ~2% false ship. Mark all of them ORCH EST and add a "track record" row (see NEW-9). | memory 3 Oct 05:40, 14:30 UTC (ORCH); recipe v4 |
| "Right now / next GO points" | 1356-1370 | 2 | REWRITE | Running now: replay read on od-l4b; phase-2 family builds (CPU); knowledge-gap research. Modal: nothing running. Next GO points: Modal smoke ≤ $0.5 → round 1 ~$30 → gate S1 → (round 2 ~$60 only if select ≥ +2.0 LB > 0) → speed + cost test ~$5-8 → sealed Jev read (OpenRouter) → OHS-3 once → report. JevBench sealed $49 is real money and the owner's call. | HANDOFF "3 Oct 17:25 EDT"; ROADMAP_2oct.md updates; A16 |
| §1.1 status snapshot table | 1372-1405 | 3 | REWRITE | Rows to drop: fix research, F7+fix2, yn2b, the "L4 started again for job 3" text. New rows: C1 (shipped, A10); Decision Index (DONE); replay read (RUNNING, od-l4b); sealed suite (FROZEN, A15); C data build (phase 2 RUNNING); knowledge-gap research (RUNNING); 2B (PAUSED); od-l4 (stopped / stockouts); GPU quota 1 (increase denied 3 Oct 17:15 UTC). | ORCH (memory); HANDOFF |
| §1.1 Modal account table + BILL | 1269-1277, 1406-1420 | 3 | UPDATE | Still the last real billing reading (1 Oct 23:40 UTC, $141.46). Relabel it "last reading". Add an ORCH note: no Modal job since; 0b NO GO meant no C4; every 3 Oct read ran on the free Google L4. The "role" column needs: jaypatil-duke = holds the C1 init adapter, planned round-1 account. Keep the `assert` on the sums. | ORCH |
| §1.1 "Where we stand (EST)" table | 1421-1437 | 3 | REWRITE | Rows about fix2 readiness, 4B-E fallback and the $24-28 spare are stale. New rows: execution, the shipped C1 (strengths and weaknesses), proven wins vs Jev (hijack, JevBench public, speed axis, cost formula), losses (ejs-5, DI knowledge, Brier), open items (round 1, OHS-3), budget. | – |
| Reading guide + TOC | 1440-1480 | 4-5 | UPDATE | New "what is new in this edition". New **held-out definition**: OHS-1/2 are PRACTICE since A12. The clean exams are OHS-3, sealed part-A confirm, and LongBench v2 (sealed). DI and ejs-5 are report-only; ejs-5 counts as in-domain once commit data trains. Remove "2 Oct update" bullets. | A12, A13, A15, A16 |

### §2-§4: goal, architecture, data

| § | build.py lines | PDF pp | Verdict | Why / what to do | New sources |
|---|---|---|---|---|---|
| §2.1 Goal | 1484-1489 | 6 | REWRITE | **STALE: "4B + 2B + 2B→4B cascade".** Replace with the 3 Oct goal (ORCH): beat or match Jev with the 4B on unseen-domain and OHS-3 accuracy (≥ Jev; −1 acceptable; +1-2 target). Beat Jev on hijack, injection, consistency, speed, cost and JevBench. The 2B is paused. Flow: B → OHS-1/2 → C (research → sealed suite → golden data → round 1 → gate → conditional round 2) → ship the best that passes → OHS-3 once. | memory 3 Oct ~06:00 UTC (authoritative) |
| §2.2 Win conditions | 1490-1507 | 6 | UPDATE | Keep the PREREG_OHS3 axes table. Drop "which system counts: 4B + 2B + cascade". The candidate is now the shipped 4B (C1 or the C winner). Fill "≥ Jev" with the owner's 3 Oct wording, tagged ORCH (not in a committed file). Add the C ship gate (A16) as the model-selection rule. Speed/cost status unchanged (draft only). Mark `score_ohs3.py` still untracked (LIVE git). | A16; PREREG_OHS3 |
| §2.3 OHS-3 facts | 1508-1515 | 6 | KEEP + 1 line | Keep. Add the A10 overlap disclosure (7 golden_train units share 12-grams with OHS-3; OHS-3 is reported with and without them; counts only). | A10 §D |
| §2.4 Rules | 1516-1526 | 6 | UPDATE | Keep: GO points, no >4B teachers, no Jev outputs, OHS-3 once, no submission, one backup. The rule "frozen code until the 4B run ends" is over; replace it with "A16-pinned trainer, default-off, C1 bit-for-bit". Add: free L4 only (owner 17:25 UTC); training GO ≤ ~$100 with a $25 reserve; pre-register every step; never test items; sealed suite / OHS-3 / LongBench stay sealed; nothing chosen on ejs-5, OHS, JevBench, DI or LongBench; data policy (commercial-licence public TRAIN splits with a private sources file; own program-labelled families; commit data from other repos, never n8n, never ejs-5 items; non-commercial = study only); sealed isolation (builders never open sealed folders or session folders). | memory 3 Oct 05:40-06:30 UTC; A14-A16 |
| §3.1 4B layout E | 1531-1556 | 7 | KEEP (retitle) | Layout E is still the layout of C1 and of C. Retitle it "The 4B layout (C1 and plan C)". X14/X15/X19 can stay. | – |
| §3.2 2B PRISM-X I | 1557-1587 | 7-8 | HISTORY (2B appendix) | The 2B is paused. Keep one short paragraph in a "Paused: the 2B" appendix. | – |
| §3.3 Architecture tests | 1588-1609 | 8 | HISTORY | Mostly 2B arms; condense to 3-4 lines in the appendix. | – |
| §3.4 Serving plan | 1610-1619 | 8 | REWRITE | Cascade and 2B fast tier: stale. Now: the A5 readout is committed for C1 (choice 2-view, yes/no 1 read, T 1.00/1.00; A10 §D, A12, ejs-5 prereg). JevBench uses band edge (pre-registered). Plan C adds per-type T by leave-one-group-out within [0.8, 1.3] (addendum C1-C3). | A10, A12; ADDENDUM_research.md |
| §3.5 Run configs | 1620-1655 | 9 | UPDATE | Show `runs/q35_4b_main.json` (C1) next to **`runs/q35_4b_c_r1.json`** (round 1, sha f3bb379e… = A16 pin; untracked). Drop the 2B config column, or move it to the appendix. The `CFG2` reads (147, 1640-1647) go with it. | A16 |
| §3.6 Code freeze | 1656-1691 | 10 | REWRITE | **The LIVE checks now say MISMATCH (see §3 of this map).** Becomes "Code state". (1) Tag `final-frozen` = C1's code; train_meta matches it (BK_CODE_OK still MATCH). (2) The working copy = A16 pins: train_decoder c2c2d1d6…, decoder_io 908c08d7…. These are default-off changes; C1 reproduces bit-for-bit (ORCH). **They are uncommitted:** HEAD still holds the tag versions. (3) modal_od.py is modified and uncommitted (c25e4f38). (4) gate_dev.py 78975445 is unchanged. (5) Tests: "297 + 55 pass, 1 pre-existing failure" (ORCH, train prep). | A16; LIVE git |
| §4.1 Golden v14 | 1696-1739 | 11 | UPDATE | Still C1's training set and the replay pool for C. Add two things. (a) The A10 OHS-3 overlap (7 units in gd_redocred / gd_helpsteer3_pref); C drops both sources whole (A16 d). (b) This contradicts D4's "0 exact and 0 13-gram overlaps with OHS-3": different n-gram size and scope. Explain it in §11.4. Keep the hashes LIVE. | A10, A16 |
| §4.2-4.5 Teacher labels, 2B files, 2-view, yn2b | 1740-1861 | 11-13 | HISTORY (2B appendix) | The 2B is paused. A10 §D says: the 2B teacher = 4B-E 2-view labels, no relabel. **The relabel (~$23) and "C4 as teacher" are dead.** Keep one table (files, KD counts, hashes) in the appendix. The heavy LIVE scans (kd_count, VIEWCHK, YN/YN2) can be dropped or kept there. | A10 §D |

### §5-§6: history logs

| § | build.py lines | PDF pp | Verdict | Why / what to do | New sources |
|---|---|---|---|---|---|
| §5 Log 28-30 Sep | 1863-1968 | 14-15 | HISTORY (keep as-is) | A correct historical record. Move it to the history appendix. | – |
| §6 heading + §6.0 timeline 1-2 Oct | 1970-2082 | 16-17 | HISTORY + NEW | Keep 1 Oct and 2 Oct as a compact history table. Drop the rows driven by `_L4_RUNNING`, REBUILD, `_ROADMAP_HITS` and GATE2_MAN. **Add a NEW 3 Oct timeline** (§0 above; git times converted to UTC). | git log |
| §6.1 4B main run | 2083-2217 | 18-19 | KEEP (shorter) | This is the provenance of the shipped C1: segments, relays, backup sha 507d1c29 MATCH, loss chart. Keep the LIVE parse and the chart; trim the relay detail. | – |
| §6.2 Gate job 1 | 2218-2332 | 20-21 | KEEP (shorter) | This is the "failed condition" of A10. Keep the ship-look table and the parity line. Drop C3/C2 detail or shorten it. Add: "overridden by A10 (3 Oct 03:10 UTC)". | A10 |
| §6.3 Diagnosis | 2333-2391 | 22 | KEEP (shorter) | It underpins the A10 reasoning (29/30 flips in one frame; C1 more accurate on both rows). Keep the core table and add A10 §C. | A10 §C |
| §6.4 Fix research | 2392-2469 | 23-24 | HISTORY | fix2 was chosen, built, then stopped at 0b. Keep 2-3 lines. | – |
| §6.5 yn2b status | 2470-2505 | 25 | HISTORY (2B appendix) | 2B paused. | – |
| §6.6 Tools | 2506-2544 | 26 | UPDATE (short) | Keep only the tools still used: score_ohs3.py, the OHS-3 harness (prep89 file names only), direct hosting (the speed/cost test), relay_spawn.py. Add the C tools: c_build/replay_sample.py, L4_REPLAY_READ.sh, c_src/common/denylist.py + negcount.py, bench/decision_index/di_tools.py. Drop the fix1/fix2 pipeline rows. | A16.1; DI README |
| §6.7 Owner decisions log | 2545-2573 | 27 | REWRITE | Many rows are stale or "Pending" (OK plan, relabel, 2B pilot). Make a full owner log for 1-3 Oct (see NEW-4). **Do NOT add any tb_mixtral lineage line** (owner instruction, memory 3 Oct ~03:10 UTC). | memory (ORCH); commits |
| §6.8 F7 v2 + fix2 status | 2574-2678 | 27-28 | HISTORY (drop detail) | fix2 is dead: 0b NO GO, no C4. Replace with one short "fix2 / A8′ outcome" box (NEW-3). | A10 §A |
| §6.9 F7 coverage | 2679-2703 | 28 | DROP | fix2 detail. Point to `yn2b/f7_precheck_fix2.json`. | – |
| §6.10 Audit, decide2, blind reads | 2704-2808 | 29-30 | DROP | Same. One line in history: "4 blind reads; read 4 on r6 PASS". | – |
| §6.11 fix2 training file | 2809-2901 | 31-32 | DROP | Same. Keep only the 42,566-row / 2,512-step line in history. | – |
| §6.12 Launch + job-3 plan | 2902-2973 | 32 | DROP | It never ran beyond 0b. | – |
| §6.13 A8′ | 2974-3007 | 33 | HISTORY (3 lines) | Committed c35de00. Its only executed step was 0b (NO GO). Its H.2 clause enabled A10. | – |
| §6.14 Remaining risks / skeptic notes | 3008-3041 | 33-34 | DROP | 18 open / 4 partly closed notes about fix2. Now moot. | – |

### §7: benchmarks

| § | build.py lines | PDF pp | Verdict | Why / what to do | New sources |
|---|---|---|---|---|---|
| §7.1 Scoreboard | 3045-3089 | 35 | UPDATE | Columns stay. Rows: the OHS-1/2 accuracy, yes/no, choice and Brier rows use **C1 via A12** (v11c → history). Add ejs-5, Decision Index (sample, not paired) and JevBench public C1 band edge. "Held out?" becomes "practice" for OHS-1/2. Remove 2B mentions. | A12; scores_c1_4be.json; report_sample10k.json; RESULTS_30sep.md |
| §7.2 Which system was measured where | 3090-3102 | 35 | UPDATE | The C1 row is now: OHS-1 yes (A12), OHS-2 yes (A12), JevBench v1.5.4 public yes, ejs-5 yes, DI sample yes. Add WiSE-FT B candidates (dev only). Mark the 2B rows "paused". | same |
| §7.3 OHS-1 | 3103-3127 | 36 | UPDATE | Add the C1 row: 80.4 vs 81.7, −1.2 [−2.9, +0.4], macro 80.1 vs 81.5, Brier 0.140 vs 0.114. Note "practice set since A12". | A12 md |
| §7.4 OHS-2 | 3128-3151 | 36 | UPDATE | Add the C1 row: 81.0 vs 81.5, −0.6 [−2.2, +1.1], macro 81.3 vs 82.0, Brier 0.057 vs 0.038. Same note. | A12 md |
| §7.5 Dev / dev-confirm | 3152-3191 | 37 | UPDATE | Keep. Add the B (WiSE-FT) results: unseen select a=0.9 +0.05, 0.8 −0.23, 0.7 −0.78, 0.6 −1.12; a*=0.9 confirm −0.10 → keep C1. Add parity od-l4b vs od-l4: 100%. | b_wiseft_result.json |
| §7.6 Consistency | 3192-3208 | 37 | KEEP | Add one line: C1 complement violations 3.30% vs 4.63% (A10 §C). | A10 |
| §7.7 Security | 3209-3264 | 38 | KEEP (LIVE) | Still valid: gate_dev recompute gives jagged C1 0/347 vs jev_guard 344/346; OPI 10/785 vs 10/785 (dry run today). Drop the 2B rows from the "earlier table" or move them to the appendix. | LIVE |
| §7.8 Speed | 3265-3293 | 39 | KEEP + note | No new measurement. Say: C1 has the same size and layout as 4B-E; its H100 speed is not measured (EST similar). The speed + cost test is planned after SHIP (GO ~$5-8). Drop the 2B/cascade speed lines. | ROADMAP_2oct.md 15:25 UTC update |
| §7.9 Cost | 3294-3308 | 39 | KEEP | Same note. | – |
| §7.10 JevBench public | 3309-3356 | 39-40 | UPDATE | Add 4 C1 rows (as trained 70.56; committed 73.36; **band edge 74.34, I 75.1, +11.9 [+3.0, +21.3]**) and the C1 vs 4B-E sub-lines. Move the 2B I_1600 rows to the appendix. Keep the "public items were our dev set, numbers flatter us" warning. | RESULTS_30sep.md lines 45-61; scores_v154_c1.json |
| §7.11 v1.4.2 | 3357-3366 | 41 | KEEP (history) | – | – |
| §7.12 Official board 30 Sep | 3367-3400 | 41 | KEEP | No newer snapshot exists. Label it "snapshot 30 Sep, not re-fetched". | – |
| §7.13 Estimated placement | 3401-3411 | 41 | REWRITE | It was based on 4B-E and board.md (30 Sep). Replace with the 3 Oct ORCH EST for C1 / the C winner (see §8 below). | ROADMAP_2oct.md "Final timeline" last bullet; memory |
| §7.14 Data checks / never measured | 3412-3427 | 42 | UPDATE | "Never measured" was: OHS for the new 4B, Jev on dev and redef, end-to-end speed. OHS-1/2 for C1 is now measured. Still never measured: Jev on redef, C1 speed on H100, real serving cost, adaptive attack. Add the new ones: sealed suite (no model has read it), round-1 model. | – |
| **NEW §7.x** ejs-5 | – | – | NEW | Pooled C1 54.1 vs Jev 58.5, −4.4 [−7.8, −0.9]. Per type: route +0.0, triage −4.7, size −5.0, risk −7.2. Late rows: tie. 4B-E 54.5. Reference models: GPT-5.6 Terra 61.1, Opus 5 68.1, regex baseline 43.4 → C1 is 4th of 5. My pre-run estimate was 59.6 (80%: 55.4-64.1) and the result fell below it; say so. Note: ejs-5 counts as in-domain after the commit data. | scores_c1_4be.json (aggregates); bench/ejs5/README.md. **Never open ejs-5 gold.** |
| **NEW §7.y** Decision Index sample | – | – | NEW | Index 54.83 vs Jev v0.1 59.51 (−4.7). Balanced_skill 40.35 vs 46.26. Areas: knowledge −17.65, language −1.79, retrieval −2.85, tools −0.05, arts −1.07. Top-5 board for context. Caveats: ~10K stratified sample (seed 20260919, sha 70386e7b), Jev = published full suite, not paired, ±1-2 pts; report-only (A13). BANKING77/CLINC150 are dev sources, SGD is an OHS-1 source, MuSR overlap is disclosed. | report_sample10k.json only (aggregates). **Never open `bench/external_quarantine/**`.** |

### §8-§12: projections, competitors, plan, risks, verification

| § | build.py lines | PDF pp | Verdict | Why / what to do | New sources |
|---|---|---|---|---|---|
| §8.0-8.8 Projections | 3428-3567 | 43-45 | REWRITE | All of it is 30 Sep FINAL_PROJECTION + the 1 Oct mixture: 4B vs 2B vs cascade, "final 4B by gain over 4B-E", levers (relabel, cascade), Codex odds. **Stale.** New §8: (a) the 3 Oct projections (ORCH EST) with ranges; (b) **a track record table** (NEW-9); (c) what could move them (DI knowledge gap, yes/no, LongBench). Keep at most one line pointing to FINAL_PROJECTION as history. | memory 3 Oct; ROADMAP_2oct.md |
| §9.1 Leaders and us | 3571-3589 | 46 | UPDATE | "Us" row = C1 public band edge (unofficial). | RESULTS_30sep.md |
| §9.2 Open → sealed | 3590-3597 | 46 | KEEP | – | – |
| §9.3 / §9.3b Projected board | 3598-3645 | 46 | UPDATE | Drop the 2B row (paused) and the "4B-E if the new 4B fails" alternatives. Use C1 / C winner: Score A ~74.5 (71-77), I ~69 (61-75) (ROADMAP), and ~72-75 / 66-72 (memory 05:40). The two disagree; show both or reconcile (§5 of this map). Keep "never submitted". | ROADMAP_2oct.md; memory |
| §9.4 Three claims | 3646-3652 | 47 | UPDATE | Still "pick before OHS-3". Add the fair-test rule: claim an outside win only if JevBench sealed and ejs-5 agree (memory fair-test-pick). ejs-5 is now a loss. | memory |
| §9.5 Lessons + Jev facts | 3653-3664 | 47 | UPDATE | Add: the Decision Index v0.1 board (Jev 59.51; top-5). LongBench: Jev's 52.8% was withdrawn, and the longjev repo cites TypeSafe terms forbidding publication of Jev benchmark results, so **flag before ANY public claim**. Jev market facts stay. | report_sample10k.json; memory |
| §10.1 Roadmap | 3668-3695 | 48 | REWRITE | **STALE**: the 26-row table plus LIVE rows 8-12 about fix2; rows 13-26 are 2B, cascade and relabel. New hand-written table, steps in order. Each row gets: status, cost (EST), ETA (EDT range), GO yes/no. **Done:** A10 (C1), JevBench public, ejs-5, B, A12, DI sample, research + spec v4, sealed suite A15, A16/A16.1. **Running:** replay read, phase-2 families, knowledge-gap research. **Planned:** G9 crowd scoring (free L4), mixer + counts-only decontamination, Modal smoke ≤ $0.5 + GO, round 1 ~$30 (~7 h), gate S1, (S2), round 2 only on a clear win, C look, sealed Jev read once (OpenRouter GO), speed + cost test (GO ~$5-8), OHS-3 once (GO), report; JevBench sealed (owner, $49 real money). Times are EST ranges; give both training-start figures (§5). | ROADMAP_2oct.md "Update 3 Oct" + "Final timeline"; HANDOFF NEXT list; A16 |
| §10.2 Budget | 3696-3720 | 49 | REWRITE | **STALE**: fix2 C4 $8-9, relabel $23, 2B $74, total $113-117, spare $24-28. New: Modal $141.46 (last read 1 Oct 23:40 UTC; ORCH: $0 since). Plan: smoke ≤ $0.5 + round 1 ~$30 + round 2 ~$60 (conditional) + speed/cost ~$5-8 ≈ $36-99, within the owner's ≤ ~$100 GO and the $25 reserve. Google: free L4 only, GPU quota 1 (increase denied). L4 hours: DI ~8 h done; replay ~11.5 h+; crowd ~16-20 h (ORCH EST). OpenRouter: $6.58 (1 Oct); planned Jev reads = sealed suite once + OHS-3 (see the risk in §5). | memory; A15; A16 |
| §10.3 Plan rules | 3721-3744 | 49 | REWRITE | Every row is about the old gate, A8′, fallback 4B-E, the C4 teacher, yn2b arm B and the A5 draft. Replace with the **C rules**: A16 ship gate; round-2 rule; looks S1 / S2 / C once and Jev once (the scorer refuses others); guards D1-D6, D9; one candidate per round; replay 60% + C1 anchor (selective); deny-list rulings (a)-(g); G0 frozen per family before its generator; G2 independent solver; G5 blind reads; nothing chosen on held-out or report-only tests; A10 disclosures carried into the model card. | A16, A16.1; C_TRAIN_RECIPE v4 (§6.2-6.4) |
| §11.1 Open issues | 3748-3778 | 50 | REWRITE | Items 1-1b (fix2), 2 (2B teacher), 3 (fallback C), 4 (second look), 8 (budget spare), 9-11 (2B) are stale. Items to carry forward, updated: 5 (OHS-3 config must name C1 + the A5 readout; the runbook/template still say 4B-E), 6 (PREREG_OHS3 rule-4 amendment for A5), 7 (untracked OHS-3 files), 12 (speed/cost definition not committed), 13 (Jev never run on redef). New issues: G0 non-convergence; replay read slower than the estimate; L4 bottleneck (quota 1); 28 replay sources "VERIFY or drop" (licence); A16-pinned code and C files are uncommitted; DI knowledge gap; ejs-5 loss; Brier behind Jev; OHS-3 overlap; OpenRouter balance; the LongBench ToS flag. | memory; HANDOFF; LIVE git |
| §11.2 30 Sep audit must-fix | 3779-3811 | 50 | HISTORY | Most are DONE or CLOSED. Carry only the still-open items into §11.1 (9a/9b partly, 9c, 9d, 9g). The source `T/wnzbuj8i0.output` is MISSING (session file). | – |
| §11.3 Known risks | 3812-3853 | 51 | REWRITE | Drop the fix2, job 3, 2B and cascade risks. Keep: yes/no gap, drift, hosting speed, laptop network loss (spawn launcher), relay modes, non-held-out security, calibration, dev reuse, label noise, public JevBench = dev. Add: round 1 may not beat C1 (P(ship) about 77% at a true +2 → much lower at a true +1; EST); forgetting/regression (guards D1-D6, D9); sealed-suite isolation (incident disclosed); knowledge gap; OHS-3 overlap. **Lineage bullet:** keep the existing 4B-E history wording unchanged. Do NOT add a new tb_mixtral or lineage line. Soften "(no model labels)" about C1 to the golden-set rule wording; avoid absolute claims like "no data from larger models" (owner, memory 3 Oct ~03:10 UTC). | memory |
| §11.4 Discrepancies | 3854-3935 | 51-52 | UPDATE | Drop the fix2 / F7 / read-4 / skeptic / 2B cost / yes/no-view items, or move them to the appendix. Keep the PREREG DRAFT header and the stale relay_protocol numbers. Add the new ones from §5 of this map. | – |
| §12.1 Identity | 3939-3949 | 53 | UPDATE | Expected HEAD = 18c024c or later. Expected `git log -3` = 18c024c, 27d8b0a, 3abd721. Worktrees: 2 (jev-2b at d86c56e, paused). Add a row: amendment commits found by `git log --grep` (A8′ c35de00, A10 132cd2a, A11 c11e4a9, A12 86f59dd, A13 8f1a9eb, A14 a79e5d4, A15 3abd721, A16 27d8b0a, A16.1 18c024c). | LIVE git |
| §12.2 Hashes | 3950-3970 | 53 | UPDATE | Split into "C1 training code at tag" vs "working copy vs A16/A16.1 pins". Add the pins: spec 4ca12996, recipe f4b79150, addendum 0da2e834, config f3bb379e, replay_sample 5735ca3e, denylist e268d566, aliases 40eeb47e, negcount 79368f46. All MATCH today. modal_od.py expected = c25e4f38 (working copy) or flag it. Keep golden hashes; move the 2B file rows to the appendix. | LIVE |
| §12.3 Commands | 3971-4017 | 53-55 | UPDATE | Drop the fix2 / F7 / job-3 / 2B commands. Add read-only commands for: the A12 table (cat), the B result (json.tool), the ejs-5 aggregate (json.tool on scores_c1_4be.json; never the gold), the DI aggregate (`di_tools.py score` needs the quarantine venv/run, so just print report_sample10k.json), the A16 sha pins (shasum), and `git log --grep Amendment`. Update the rebuild path to pdf_build_3oct. | – |
| §12.4 Verification checklist | 4018-4058 | 55 | UPDATE | Drop the fix2 / F7 / 2-view / 2B rows. Add claim → file → how rows for A10, B, A12, JevBench C1, ejs-5, DI, A15 counts (PREREG text only), and the A16 pins. | – |
| §12.5 File index | 4059-4185 | 56-60 | UPDATE | Remove the `TASKS/*.output` rows (MISSING, session folder) and the fix2 group (or move it to history). Add groups "3 Oct results" and "Plan C (spec, recipe, config, tools)". **Never list `sealed_nd/`, `c_spec/sealed_brief/`, any `*ohs3*` path, `prep89/dryrun/`, `bench/external_quarantine/`, `bench/longbench_v2/`, ejs-5 gold.** The PREREG_FINAL label becomes "A0-A16.1". | – |
| §12.6 ORCH facts | 4186-4213 | 61 | REWRITE | Replace with the 3 Oct ORCH facts: owner decisions and times; billing unchanged since 1 Oct; GPU quota denial; replay read start and ETA; DI timing; data policy; projections. Each gets a corroborating file where one exists. | memory; HANDOFF |
| §12.7 How built | 4214-4239 | 61-62 | REWRITE | Builder = pdf_build_3oct/build.py. Inputs: list them. Rules: add the sealed/session-folder bans. Keep the verification-pass practice. | – |
| Doc class / two-pass build | 4241-4309 | – | KEEP + UPDATE | Change the header string "full status record, 1-2 Oct 2026" and the metadata. Drop the fix2/yn2b stats from the final `print` line (4301-4304). | – |

---------------------------------------------------------------------------------------------------------------------

## 2. New sections to add (suggested order: after §1, before the benchmarks)

- **NEW-1 "In plain words" (page 1 box, for the founder).** 6-8 short sentences. What ships (C1), how it compares with Jev (wins: hijack, JevBench public, cost formula, speed axis on an H100; ties: OHS-1/2; losses: ejs-5, the DI knowledge area, calibration), what we are doing now (plan C round 1), when (EST range), what it costs, and what could go wrong.
- **NEW-2 3 Oct timeline.** The §0 table, with git times in UTC and EDT.
- **NEW-3 fix2 / A8′ outcome** (½ page).
  - What fix2 was.
  - A8′ c35de00, and 0b NO GO with numbers (A10 §A).
  - No C4; $0.
  - Flip research findings (ORCH): the failure sits in one frame, merge and ensemble were rejected, and the gated Fix3 had P ≈ 0.15-0.27. These came from session-scratch files that are gone, so tag them ORCH.
- **NEW-4 A10 override and owner decisions 1-3 Oct.**
  - A10 §A-§D in plain words.
  - Decision log rows (all ORCH unless committed): ship C1; ejs-5 now; B then C; 2B paused; ≤ $100 GO; OHS-1/2 as a secondary yardstick; data policy (commercial-licence public train splits, commit data from other repos); round 2 conditional; free L4 only; DI sample run; do not pause DI; knowledge-gap research. **No tb_mixtral line.**
- **NEW-5 Outside tests on C1** (one table).
  - Tests: JevBench public, ejs-5, OHS-1, OHS-2, DI sample, each with CI, status and "can it choose a model? no".
  - Plus security (LIVE) and dev unseen.
- **NEW-6 Step B (WiSE-FT)**, a small table from b_wiseft_result.json.
- **NEW-7 Plan C**, about 2 pages.
  - (a) Why C: the gap is generalization. Ties on OHS-1/2, an ejs-5 loss, the DI knowledge area.
  - (b) The research: 7 angles plus 6 extra studies; addendum ADOPT rows A1-A4, B1-B4, C1-C3, D1, E1-E3, F2-F4 (names only).
  - (c) **Sealed suite: counts from A15 only, domain IDS only.** Never names, sources or themes.
  - (d) Data plan (A16 numbers), deny-list rulings, licence (28 replay sources "VERIFY or drop", NewsMTSC excluded).
  - (e) Training: init C1, the same LoRA, `lam_ord` 1.0, seed 20261003, one candidate.
  - (f) Gate and looks.
  - (g) Build status: G0 freezes per family (count frozen vs total from `c_build/progress_phase2.log`, counts only), replay read, mixer TODO.
  - (h) Timeline and cost (EST).
- **NEW-8 Knowledge-gap research (running).** One paragraph, plus its rules: validated on separate dev sets with no DI test overlap; DI stays report-only; frozen A16 round 1 untouched. If `reports/knowledge_gap/PLAN_knowledge_gap.md` exists at build time, cite its verdict; otherwise say "running" (ORCH).
- **NEW-9 Track record (projection vs result), for honesty.** Rows:
  - ejs-5: estimate 59.6 (55.4-64.1) vs actual 54.1.
  - DI: projected ~#10-20 overall vs sample #4 on the v0.1 top-5 board, but −4.7 vs Jev.
  - A12 OHS-1/2: 1 Oct P(OHS-3 ≥ Jev) 0.45 vs the measured practice ties (−1.2 / −0.6).
  - B: no gain.
  - 0b: fix2 P(pass) 45-65% EST vs NO GO.
- **Appendix H: History**, condensed: §5 log; 1-2 Oct timeline; 6.1-6.3 detail if trimmed; fix2 in 5 lines; the 30 Sep audit list.
- **Appendix P: Paused 2B**: §3.2, §3.3, §4.2-4.5, §6.5 condensed; teacher = 4B-E 2-view per A10 §D.

---------------------------------------------------------------------------------------------------------------------

## 3. Live checks in the 1 Oct builder that fail or mislead now

The live-check prelude (lines 1-1031) was dry-run on 4 Oct at 01:00 UTC. Two things were changed for the dry run: the owner-only OHS-3 count reader was skipped, and no PDF was written. All results below are real.

| # | Check (lines) | Today | Fix in the 3 Oct builder |
|---|---|---|---|
| 1 | `EXPECT_SHA` frozen-file sha (120-126) used in §3.6 (1656-1691), §12.2 (3950-3967) | **train_decoder.py c2c2d1d6… vs ebdf046d… MISMATCH; decoder_io.py 908c08d7… vs 8ba8ff4f… MISMATCH.** prism_x and writeblock MATCH. | Expected now = A16 pins (working copy). Keep the tag hashes as "C1's code" by checking `git show final-frozen:<file>` (= ebdf046d / 8ba8ff4f today). |
| 2 | `LIVE["frozen_diff"]` (116-118) | Non-empty: 2 files, +519 / −20 vs the tag → "MISMATCH" row | Report as "expected: A16 default-off changes, uncommitted (HEAD = tag versions)". |
| 3 | modal_od.py prefix 8f4bef05 (1683-1687, 3960-3965) | Working copy c25e4f38 (uncommitted) → MISMATCH | Expect c25e4f38 with "uncommitted", or compare HEAD and working copy separately. |
| 4 | `A8P_COMMIT` = `git log -1 -- PREREG_FINAL.md` (573-579) | **Resolves to 18c024c (A16.1), 23:57 UTC, 16 files**; it should be c35de00. That breaks §1, §6.0, §6.8, §6.13, §10.3, §11.1, §12.1. | Find each amendment commit with `git log --grep` (or constants) and verify the text is in HEAD. |
| 5 | §12.1 expected values (3940-3948) | "c35de00, f17f2a1, 9759d31" vs actual 18c024c, 27d8b0a, 3abd721 | Update the expectations. |
| 6 | `RESEARCH = TASKS/w74nvebvo.output` (553); `TASKS/wnzbuj8i0.output`, `wfjjlksu2.output` (4118) | **MISSING** (session files deleted). `hm(None)[7:12]` prints an empty time in §6.0; §1.1 shows "missing"; §12.5 shows MISSING. | Drop all `TASKS` reads. Session folders are off-limits after the A15 isolation incident. |
| 7 | `logs/gate4b_fix2/`, `conds/probe_go.json` (582, 2662) | Do not exist on the Mac (the 0b result stayed on od-l4) | Source 0b from the PREREG_FINAL A10 §A text (regex on the committed block). |
| 8 | `backups/modal_models/q35_4b_main500k_fix2` (2668) | Never existed (no C4) | Drop. |
| 9 | `_L4_RUNNING` = "od-l4 is RUNNING" in ROADMAP_2oct.md (1240) | **True** (the 01:30 UTC update text) → would print "od-l4 started again for job 3": false now | Drop. Machine state is ORCH (od-l4b runs the replay read). |
| 10 | ROADMAP table parser + `_live_status` rows 8-12 (3670-3690) | Parses the old 26-row table; rows 8-12 get fix2 statuses | Replace with a hand-written C roadmap table. ROADMAP_2oct.md's 3 Oct plan is prose, not a table. |
| 11 | `REBUILD` ps scan for build_fix2.py (649-665) | Always empty | Drop (do not scan processes). |
| 12 | `LEFT` / `READY_S` / `_WHY` (686-722, 1260-1268) | fix2 launch readiness: meaningless. It prints "every pre-launch check is done" or lists OHS-3 checks. | Drop. |
| 13 | `SNAPSHOT` (1016-1021) | 03 Oct 01:44 UTC, from fix2-era files only | New inputs: PREREG_FINAL.md, report_sample10k.json, b_wiseft_result.json, A12_ohs12_result.md, scores_c1_4be.json, RESULTS_30sep.md, c_build/progress_phase2.log, replay_r1_write.json. |
| 14 | `PREREG_DRAFT` (475) | True (the header still says DRAFT, though A0 adopted it); the §12.5 label "(DRAFT)" misleads | Label "adopted by A0; amendments A0-A16.1". |
| 15 | `TESTS3 = SCR/tests_3oct.txt` (830) | SCR moves to pdf_build_3oct → the file is absent; the content is fix2 tests | Drop, or re-run C-tool tests into pdf_build_3oct/ (optional). |
| 16 | `_ohs3_counts()` (647-686) reads `yn2b/f7_precheck_fix2_ohs3.json` and `yn2b/fix2_ohs3_blind.json` | Still present (count fields only), but fix2 history | **Drop.** The new builder should open no `*ohs3*` file at all. |
| 17 | `PREDS_OHS3` existence (478) | False (OHS-3 not run) | Keep existence-only (never list or open), or drop. |
| 18 | fix2/F7 scans: FIX2C, FIX2_SHA, fix2_scan, golden_mix, F7_ORPH, `_INFL`, `_refund`, R4CARRY, BR2-4, NOTES (555-1013) | Still compute (FIX2_SHA_OK, A8P_OK True; NOTES 18 open / 4 partly / 2 closed) but are history | Drop (saves time). Keep one line: fix2 file 42,566 rows, sha 66423fe3…, 2,512 steps. |
| 19 | 2B checks: kd_count (151-163, ~12 s over 2×501K rows), VIEWCHK (379-430), YN/YN2/YNR, SP2, NOCKPT, CFG2 | All still pass (kd 449,957 / 450,170; VIEW_OK True) | Move to the 2B appendix, or drop. |
| 20 | Hard-coded `BILL` (1271-1277, assert) | Still the last reading; no newer one | Keep. Retitle "last read 1 Oct 23:40 UTC". |
| 21 | §7.2 row "New 4B: OHS-1 never / OHS-2 never / JevBench planned" (3090-3102) | False now | Update. |
| 22 | §12.5 FILES list (4059-4185) | Prints MISSING for 3 TASKS files | Rebuild the list. Add a forbidden-path guard (§4). |

Still OK today (keep):
- git identity.
- Tag 82b07d4.
- golden_train / relations sha + lines MATCH.
- The 5 segment logs (30,457 steps; last ckpt 30,422).
- Backup adapter sha (507d1c29, a16f4b08, 5433a908, 9fed952c) MATCH; train_meta code/data MATCH.
- Gate look JSONs (DO NOT SHIP; parity PASS).
- REDEF: C1 0.8%, 4B-E fresh 17.3%, 4B-E 16.5%.
- gate_dev 78975445 + SEC: jagged C1 0/347, 4B-E 2/354, jev_guard 344/346, jev 349/349; OPI C1 10/785, 4B-E 14/780, jev_guard 10/785, jev 18/785.
- yn2b line counts.
- The run's loss chart.

New LIVE checks worth adding (all read-only and cheap):
- (a) sha prefixes of the A16/A16.1-pinned files vs the PREREG_FINAL text (regex the backticked prefixes in the A16/A16.1 block). All MATCH today: spec 4ca12996, recipe f4b79150, addendum 0da2e834, config f3bb379e, trainer c2c2d1d6, readout 908c08d7, replay_sample 5735ca3e, denylist e268d566, aliases 40eeb47e, negcount 79368f46.
- (b) `git ls-files` status of each pinned file. Today: c_spec, c_build, c_src, runs/q35_4b_c_r1.json, RESULTS_30sep.md, scores_v154_c1.json, score_ohs3.py and ROADMAP_2oct.md are **UNTRACKED**; the trainer and readout changes are **uncommitted**.
- (c) The amendment list (A0, A7, A8′, A10-A16.1) parsed from the PREREG_FINAL headings, with commit ids from `git log --grep`. **There is no A9** (option D was blocked, never committed).
- (d) A12 numbers parsed from `logs/A12_ohs12_result.md`.
- (e) B verdict from `b_wiseft_result.json`.
- (f) DI index, areas and top-5 from `report_sample10k.json`.
- (g) ejs-5 pooled numbers from `scores_c1_4be.json` (aggregate keys only).
- (h) A15 counts parsed from the PREREG text (never from sealed_nd).
- (i) Replay-draw counts from `c_build/replay_r1_write.json` (99,069 rows / 20 shards; check the file has only counts).
- (j) Count of frozen G0 specs from `progress_phase2.log` lines "G0 FROZEN" (family ids only).

---------------------------------------------------------------------------------------------------------------------

## 4. Safety guards: keep these, add these

**Keep** (all in the 1 Oct builder):

1. **Read-only on the project.** Writes go only to OUT and SCR (the chart PNG). Repoint both to `pdf_build_3oct/` and `…_3Oct.pdf`, and add `assert` lines that OUT ≠ the 1 Oct and 30 Sep PDFs and that SCR is pdf_build_3oct.
2. **Git without index locks**: `GIT_OPTIONAL_LOCKS=0` (73-81). Only read-only git subcommands.
3. **No Modal, gcloud, ssh, OpenRouter or paid calls.** `budget_tracker.py` is never run. Billing figures are hand-entered with a sum `assert` (1271-1277).
4. **gate_dev imported read-only:** `sys.dont_write_bytecode = True` before `import gate_dev`; `SystemExit` caught; the import failure is tolerated (836-882). Commands in §12.3 use `PYTHONDONTWRITEBYTECODE=1`.
5. **Fault-tolerant readers:** `jload`, `mtime`, `birth` and `_txt` return None or empty instead of crashing. Add a `MISSING_INPUTS` list that is printed at the end and shown in §12.
6. **Fonts:** embedded Arial / Courier New TrueType (Type1 rendered blank before). `CMAP` glyph check → `BAD_GLYPHS` warning. `SPLIT_WORDS` cell-width check. Long-cell (>1,500 chars) warning.
7. **`md()` escaping** of `& < >` plus tag colouring (ORCH / LIVE-ORCH / LIVE / EST); `md_code` for mono cells.
8. **Two-pass build** for "Page N of M" (a deferred-page canvas broke bookmarks before), with a page-count equality warning; TOC and outline via `afterFlowable`.
9. **Tags discipline:** every number is either sourced, LIVE, ORCH, LIVE-ORCH or EST.

**Add:**

10. **Forbidden-path guard.** One `safe(p)` helper used by every open, glob, listdir, stat and sha call. It refuses any path matching `sealed_nd|sealed_brief|/ohs3|ohs3_|_ohs3|preds_ohs3|prep89/dryrun|external_quarantine|longbench_v2|ejs5/.*gold|\.env|/private/tmp/claude-501|/\.claude/projects`. The `data/**` glob rule is memory `exclude-ohs3-from-scans`. The guard aborts the build if any such path is touched. This also keeps the builder out of session folders (A15 isolation incident).
11. **Sealed suite = A15 text only:** counts and domain IDS (D1, D10-D12 non-adjacent; D2-D5 adjacent). Never print a domain, source or theme name; never stat or list sealed folders.
12. **Report-only tests stay report-only:** DI and ejs-5 are aggregates only, with no per-item or per-row content; ejs-5 gold is never opened; no DI per-item files.
13. **No new lineage disclosure / no absolute data claims** (owner, 3 Oct ~03:10 UTC). Do not add a tb_mixtral lineage line. Keep the committed PREREG wording untouched. Avoid "no data from larger models"-style claims.
14. **No secrets:** account names only; no keys, tokens or project credentials. The GCP project id is not needed in the PDF.
15. **No public-claim wording on Jev benchmark results without the flag:** LongBench / TypeSafe terms; "unofficial" on JevBench public.

---------------------------------------------------------------------------------------------------------------------

## 5. Discrepancies found while mapping (for §11.4)

1. **Amendment stated times vs git commit times:**

   | Amendment | Stated | Git commit |
   |---|---|---|
   | A14 | 15:20 | 15:01 UTC |
   | A15 | 20:45 | 20:34 |
   | A16 | 21:00 | 20:35 |
   | A16.1 | "4 Oct 00:10" | 3 Oct 23:57 |

   The texts are dated 10-25 min after their commits. A8′ (01:44 stated vs 01:47) and A10-A13 match. Git time is authoritative; say so.
2. **OHS-3 overlap:** golden v14 D4 says "0 exact and 0 13-gram overlaps with OHS-3", while the owner's count-only 12-gram check found 7 units (A10 §D). These are different n-gram sizes and scopes; it is not a contradiction of the earlier check's own result. Say both.
3. **Spec v4 sha:** memory 16:30 UTC says spec `6b4f39ba`; A16 pins `4ca12996`, which is the file on disk now. The polish pass changed it after the note. A16 is authoritative.
4. **Replay draw:** memory 19:00 UTC says 99,073 rows / 134,582 reads; A16.1 says 99,069 rows in 20 shards + a 2,000-row old slice; A16's mix uses 90,000 replay rows. Explain draw vs use (the draw is a superset for crowd/anchor selection; confirm in C_DATA_SPEC v4 before stating it).
5. **Training start ETA** (ROADMAP_2oct.md vs memory):
   - "Mon 5 Oct morning: GO → round 1" (Final timeline);
   - "training start ~Sun 11 pm EDT" (last line);
   - memory 19:00 UTC: "~Mon 5 Oct early morning EDT";
   - the replay read is running slower than its 11-12 h estimate.

   Give a range, tagged EST.
6. **JevBench sealed projection for C1/C:** ROADMAP says Score A ~74.5 (71-77), I ~69 (61-75); memory 05:40 UTC says A ~72-75 (beat ~65%), I ~66-72 (beat ~30%). Show both, or one reconciled range, tagged ORCH EST.
7. **DI rank:** projected "~#10-20 overall" (05:40 UTC) vs the sample at #4 on the v0.1 top-5 (Jev 59.51, Jevfire 55.74, diffusiongemma 55.56, C1 54.83, Decider 54.34). The sample is not paired with the board (±1-2 pts).
8. **OHS-3 runbook / config template** still name 4B-E as the shipped 4B (1 Oct §11.4); since A10 the shipped model is C1. They must be amended at the OHS-3 step (A10 §D says so).
9. **PREREG_FINAL header** still says DRAFT; §1 still says the 2B has no PRISM-X (unchanged; the 2B is paused anyway).
10. **OpenRouter balance risk (EST):** $6.58 / key $7.60 left (1 Oct). Planned Jev reads:
    - OHS-3: 2 runs × 1,852 rows, EST $1.2-2.7 per the runbook;
    - the sealed suite once: 7,302 items including 199 long documents of 4-8K tokens, ≈ 2× OHS-3 calls → EST ~$2.5-5.5 by proportion.

    The total may exceed the balance. Check before the GO.
11. **A9 does not exist:** option D (A9) was blocked by the auto-mode classifier and never committed. The PREREG goes A8′ → A10. Say so, to avoid a "missing amendment" question.

---------------------------------------------------------------------------------------------------------------------

## 6. Allowed source files for the 3 Oct facts (aggregates only)

**Git:** `git log`; `git show --stat` on c35de00, 132cd2a, 9a04df1, 065191c, 32ee1f9, c11e4a9, 86f59dd, 599c513, 629a9f4, 8f1a9eb, a79e5d4, 3abd721, 27d8b0a, 18c024c.

**PREREG and drafts:**
- `L/PREREG_FINAL.md` (A10-A16.1 blocks; A15 has domain ids only);
- `L/prereg_drafts/A10_override_C1.md`.

**Results:**
- `L/logs/A12_ohs12_result.md`;
- `L/logs/b_wiseft_result.json`;
- `B/v154/RESULTS_30sep.md` (3 Oct section) and `B/runs/scores_v154_c1.json`;
- `B/ejs5/runs/scores_c1_4be.json` and `B/ejs5/README.md` (no gold);
- `B/decision_index/report_sample10k.json` and `B/decision_index/README.md`.

**Plan C:**
- `L/c_spec/{C_DATA_SPEC,C_TRAIN_RECIPE,ADDENDUM_research,LICENCE_REGISTER}.md` (never `c_spec/sealed_brief/`);
- `L/runs/q35_4b_c_r1.json`;
- `L/c_build/{replay_r1_write.json, RUNBOOK_replay_reads.md, f2_l4.json, progress_phase2.log}`;
- `L/c_src/common/{denylist.py, negcount.py}` (sha only).

**Status notes:**
- `reports/ROADMAP_2oct.md` (3 Oct updates);
- `HANDOFF.md` §"HANDOFF 3 Oct 2026, 17:25 EDT";
- `reports/knowledge_gap/` (only PLAN_knowledge_gap.md, if it exists).

**ORCH:** memory `final-goal-30sep.md` 3 Oct entries, read by the writer and typed in; the builder does not open `~/.claude/**`.

**Never open:**
- `L/sealed_nd/**` and `L/c_spec/sealed_brief/**`;
- `data/ohs3*`, `data/*ohs3*`, `data/ohs3_parts/`, `L/ohs3/` (including `used_sources.json`), `preds_ohs3*`, `yn2b/*ohs3*.json`;
- `prep89/dryrun/`;
- `bench/external_quarantine/**`, `bench/longbench_v2/` data, ejs-5 gold;
- `.env` and any secret;
- `/private/tmp/claude-501/**` and `~/.claude/projects/**` (from the builder).
