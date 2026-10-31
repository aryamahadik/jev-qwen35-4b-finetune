# FACTS_3oct: everything new since the 1 Oct report (input for OpenDecide_Full_Status_3Oct.pdf)

Collected 4 Oct 2026, about 01:00-01:15 UTC (3 Oct, about 9 pm EDT). Read-only. No Modal, gcloud, ssh or paid calls.
Nothing sealed was opened (no `sealed_nd/`, `sealed_brief/`, OHS-3, `prep89/dryrun/`, `external_quarantine/`, LongBench data,
`.env`). The sealed new-domains suite appears here ONLY as counts by domain id (D1..D12), exactly as in PREREG_FINAL A15.

**Cutoff.** The 1 Oct report PDF (`reports/OpenDecide_Full_Status_1Oct.pdf`) was built 2 Oct 21:51 EDT = **3 Oct 01:51 UTC**.
It already covered: the 4B main run, gate job 1 (DO NOT SHIP), the fix research, the F7 v2 + fix2 build, the 2 Oct roadmap.
Everything below happened after that, or finishes a story the old report left open.

**Path aliases.** `L` = `/Users/aryamahadik/Documents/jev/opendecide-data/lean`; `B` = `/Users/aryamahadik/Documents/jev/bench`;
`R` = `/Users/aryamahadik/Documents/jev/reports`; `M` = `/Users/aryamahadik/.claude/projects/-Users-aryamahadik-Documents-jev/memory`;
`J` = `/Users/aryamahadik/Documents/jev`.

**Tags.** `SRC` = read from the named file or commit. `ORCH` = the orchestrator's main log `M/final-goal-30sep.md` (entry time
given). `LIVE` = recomputed or checked by me at collection time. `EST` = an estimate, never a measurement.
Times are UTC unless marked EDT (EDT = UTC - 4 h). Git times are the authority.

---

## 1. Headline (plain words)

1. **The shipped 4B is now C1** (`q35_4b_main500k`), by an owner override (A10, commit 132cd2a, 3 Oct 03:10 UTC). C1 failed one
   consistency rule and the fix pre-check, and this is disclosed. 4B-E is kept only as a reference and as the 2B's teacher. [SRC A10]
2. **The fix top-up (C4) never trained.** Its pre-check (probe-go) said NO GO, so $0 was spent. [SRC A10 A.]
3. **C1 vs Jev, held-out practice sets (OHS-1 + OHS-2):** -1.2 and -0.6 points, both statistical ties; pooled about -1.0.
   Jev's calibration (Brier) is better. [SRC `L/logs/A12_ohs12_result.md`, commit 629a9f4]
4. **C1 vs Jev, ejs-5 (868 software-commit decisions):** 54.1% vs 58.5%, **a loss** (-4.4 [-7.8, -0.9]). Newer rows (from 1 Jun
   2026) tie. [SRC `B/ejs5/runs/scores_c1_4be.json`, commit 32ee1f9]
5. **C1 on JevBench public items (unofficial, our own run):** Intelligence 75.1 vs Jev 63.2 (+11.9 [+3.0, +21.3], better);
   Score A 74.34 vs 68.80. These items were our development set, so this is optimistic. [SRC `B/v154/RESULTS_30sep.md`]
6. **C1 on a 10K Decision Index sample (report-only):** index 54.83 vs Jev's published 59.51 (-4.7). The gap is almost all
   "knowledge" (GPQA, GSM8K, CRUXEval, MMLU). C1 would sit about #4 on that v0.1 board. [SRC `B/decision_index/report_sample10k.json`, 18c024c]
7. **Step B (weight softening) found nothing better than C1.** [SRC `L/logs/b_wiseft_result.json`, 599c513]
8. **New owner direction (3 Oct 04:45 UTC):** 4B only, 2B paused; BEAT or MATCH Jev; up to about $100 Modal; plan "C" = deep
   research -> sealed new-domains test -> expert golden dataset -> training round 1 (round 2 only on a clear win). [ORCH 04:45-06:30]
9. **Done for C so far ($0 Modal):** research (13 studies + 2 skeptic reviews + licence checks), spec/recipe v4, sealed suite v2
   frozen (7,302 items), C plan pre-registered (A16, A16.1), replay draw written (99,069 rows), phase-1 building blocks built
   (332 packs, 400 format styles, 8,575 public rows), all 14 family rule-sheets frozen. [SRC A15/A16/A16.1, c_build, c_src]
10. **Running now:** C1 reading the 99,069 replay rows on the free L4 (about 11-12 h, slower than estimated); the family
    generators being written (no family rows yet); a small research pass on the knowledge gap. Training round 1 needs the
    owner's GO; start EST Mon 5 Oct early morning EDT. [ORCH 19:00, ~00:50 UTC 4 Oct; LIVE `L/c_build/progress_phase2.log`]

---

## 2. Git commits since 2 Oct 00:00 (branch `freeze/4b-main500k`; 14 commits)
Source: `git -C J log --since=2026-10-02 --stat --oneline` [SRC]. UTC = EDT + 4 h.

| Commit | Git time (UTC) | What |
|---|---|---|
| c35de00 | 3 Oct 01:47 | A8' amendment: C4 = `q35_4b_main500k_fix2` top-up, pre-checks, one ship look (79 files, F7 v2 + fix2 data + gate tools) |
| 132cd2a | 3 Oct 03:10 | A10: owner override names C1 the shipped 4B (+ `prereg_drafts/A10_override_C1.md`) |
| 9a04df1 | 3 Oct 04:04 | ejs-5 pre-registration + kit (convert, run, score, 15 tests) |
| 065191c | 3 Oct 04:19 | ejs-5 note: runs on backup L4 od-l4b (od-l4 out of stock); same image, code, adapter hashes |
| 32ee1f9 | 3 Oct 04:38 | ejs-5 results: C1 54.1%, 4B-E 54.5% vs Jev 58.5% (loss); late rows tie |
| c11e4a9 | 3 Oct 04:49 | A11: step B weight softening (a = 0.6-0.9), fixed select/confirm rule |
| 86f59dd | 3 Oct 04:57 | A12: OHS-1+2 Jev yardstick after B (+1 pp stop rule) + B scorer |
| 599c513 | 3 Oct 07:33 | Step B result: no softened C1 passes; keep C1 |
| 629a9f4 | 3 Oct 08:43 | A12 result: C1 vs Jev OHS-1 -1.2, OHS-2 -0.6 (ties); continue with C |
| 8f1a9eb | 3 Oct 14:27 | A13: report-only Decision Index sample run on C1 |
| a79e5d4 | 3 Oct 15:01 | A14: sealed new-domains suite build rules; sealed folders git-ignored |
| 3abd721 | 3 Oct 20:34 | A15: sealed suite v2 frozen (suite + scorer sha256, counts, adjacency by id, isolation incident) |
| 27d8b0a | 3 Oct 20:35 | A16: C round-1 plan (spec/recipe/addendum sha, seed, sizes, deny-list rulings, gate) |
| 18c024c | 3 Oct 23:57 | A16.1: tool versions for A16 rulings (+ EDOS X15, choice-row rule); Decision Index report (54.83 vs 59.51) |

- Note (LIVE, minor): the amendment headers of A14, A15, A16 and A16.1 carry times 11-25 min LATER than their git commit
  times (A14 "15:20" vs 15:01; A15 "20:45" vs 20:34; A16 "21:00" vs 20:35; A16.1 "4 Oct 00:10" vs 3 Oct 23:57). Git is the
  authority. The required order still holds by git: A15 and A16 were committed before the replay draw was written (20:50 UTC),
  and A16.1 before the first generator start (4 Oct 00:28 UTC) [LIVE from `L/c_build/progress_*.log`].
- Uncommitted but pinned (LIVE): `train_decoder.py` and `decoder_io.py` are modified (not committed); `c_spec/`, `c_build/`,
  `c_src/` and `runs/q35_4b_c_r1.json` are untracked. Their sha256 match A16/A16.1 exactly (checked now: spec 4ca12996, recipe
  f4b79150, addendum 0da2e834, config f3bb379e, trainer c2c2d1d6, readout 908c08d7, replay_sample 5735ca3e, denylist e268d566,
  negcount 79368f46). The pre-registration holds by hash, but these files have no git copy.

---

## 3. Owner goal and rule changes (dated)

| When (UTC, 3 Oct) | Owner decision | Source |
|---|---|---|
| ~02:10-03:10 | After probe-go NO GO: "ship c1" (option B, disclosed override). Asked NOT to add the tb_mixtral lineage line to the report; avoid absolute public claims like "no data from larger models" | ORCH 03:10; A10 |
| ~04:00-04:20 | OK to run ejs-5 (C1 + 4B-E) and LongBench v2 once on the free L4. ejs-5 first; then B; then C | ORCH 04:00, 04:12 |
| ~04:10 | Arm D (2B + F7) NOT added (analysis + skeptic agreed) | ORCH 04:10 |
| **04:45** | **Forget the 2B for now; focus on the 4B.** Up to ~$100 of the $141 Modal may be spent. Target: comparable to Jev, ideally +1-2 pts | ORCH 04:45 |
| 05:00 | Overnight authorization: finish B; YES to OHS-1+2 as a secondary Jev yardstick (they become practice sets); stop if >= Jev + 1 pp, else research -> sealed suite -> C data -> round 1 (~$30) -> round 2 (~$60). GO up to ~$100, keep $25 reserve | ORCH 05:00 |
| 05:40 | Drop the "no commit-style data" rule: commit data from OTHER repos allowed (never n8n, never ejs-5 items), disclosed; ejs-5 becomes in-domain. Use TRAINING splits of public eval sets (licence-checked, decontaminated), never test items | ORCH 05:40 |
| 05:45 | Run B, then C "no matter what"; ship only the best after C's gate | ORCH 05:45 |
| 06:00 | Data policy: commercial-licence public train splits only (private sources file); non-commercial = study only; plus our own expert program-labelled families. Data stays private | ORCH 06:00 |
| **06:00** | **CURRENT GOAL (authoritative):** BEAT or MATCH Jev with the 4B on unseen-domain and OHS-3 accuracy (>= Jev; -1 acceptable; target +1-2), and beat Jev on hijack/injection, consistency, speed, cost and JevBench. 2B paused | ORCH 06:00 |
| 06:05 | If B adopts a winner, all of C builds on it (else C1) | ORCH 06:05 |
| 06:10 | Run the whole flow on the agentic loop while asleep; no regression of the shipped model; "take the jump" | ORCH 06:10 |
| 06:20 | Codex review adopted: C skill-based; selective anchor; sealed suite isolated + hashed first; no candidate replaces the incumbent unless it passes the frozen gate; RL only after SFT, as a pilot | ORCH 06:20 |
| **06:30** | **Round 2 is CONDITIONAL** (only on a clear round-1 win, ~+2-3 on the sealed suite, LB > 0, no harm). Commit data: keep the owner's version | ORCH 06:30 |
| 14:35 | Stress: this run is for GENERALIZATION (unseen domains), not tuning to any test | ORCH 14:35 |
| 14:50 | Option "A": Decision Index ~10K sample on C1, report-only | ORCH 14:50; A13 |
| 17:15 | OK to ask Google for GPU quota 1 -> 2. **Auto-denied in seconds** (an earlier request for 4 on 29 Sep was also denied) | ORCH 17:15 |
| 17:25 | **Free L4 only** (no paid Modal L4 for crowd scoring) | ORCH 17:25 |
| 18:05 | Do NOT pause the Decision Index run; accept the ~4-5 h delay | ORCH 18:05 |
| 18:30 | Sealed suite v1: no waiver ("no compromise"); rebuild | ORCH 18:30 |
| ~00:45 4 Oct (log says ~21:15 EDT; file times show ~20:45 EDT) | Small deep research on closing the general-knowledge gap ("there has to be a way a 4B can surpass Jev"). Any knowledge change validated on separate dev sets; DI stays report-only; round 1 (A16) untouched | ORCH last entry |

- Still standing: no teacher bigger than 4B; no Jev outputs as inputs; OHS-3, LongBench and the sealed suite stay sealed;
  never tune on ejs-5 / OHS-3; JevBench submission only on the owner's word; one Mac backup per model. [ORCH 06:00; MEMORY.md]
- The CLI `/goal` hook may still hold older text (owner typed "/ goal"); the memory entry is the source of truth. [ORCH 06:00]

---

## 4. The 4B fix story, finished (3 Oct 01:47-03:30 UTC)

- **A8' committed** c35de00 (01:47 UTC). fix2 data rebuilt without two whole sources that touched OHS-3 (gd_redocred,
  gd_helpsteer3_pref): 42,566 rows, 2,512 steps, ~$9 planned; OHS-3 whole-file check 0 hits. [SRC A8' C.1; ORCH 02:00]
- **Step 0b probe-go = NO GO** (02:10 UTC, od-l4). On 252 held-out nested-negation pairs (F7 probe), C1 flips 87 (34.52%),
  4B-E flips 86 (34.13%): diff +0.40 pp [-5.86, +6.75]; the rule needed >= +3 pp with LB > 0. Probe accuracy (report only):
  C1 74.54, 4B-E 74.05. No C4 trained; **$0 Modal**. [SRC A10 A.; ORCH 02:10]
- Meaning: C1's failed consistency check is narrow (one frame: "only non-hateful content" + outer "be rejected"; C1 flips 29/30
  there, 4B-E 0/30). On general nested negation C1 = 4B-E, and both are weak (~34% flips). On the other 692 pairs C1 flips 35,
  4B-E 41. C1 is more accurate on both rows of the 722 pairs (aff 84.90 vs 83.93; dneg 84.35 vs 82.96). [SRC A10 C.]
- Option D (amend the stop rule and train anyway) was BLOCKED by the auto-mode safety classifier as "security test removal";
  the edit was reverted; nothing trained or committed. D would need explicit owner approval. [ORCH 02:30]
- Flip research (whsz8voaz, CPU): merge of C1 + 4B-E possible but P~0.1-0.15 and dev-picked -> DON'T; 2x ensemble passes (e) but
  costs ~-9 JevBench cost points -> DON'T; only gated route "Fix3" (P pass ~0.15-0.27, ~$12, 1-1.5 days), optional. [ORCH 03:20]
- **A10 committed** 132cd2a (03:10 UTC): C1 = shipped 4B (adapter sha256 507d1c29...). Disclosed: ship look 1 failed (e)
  8.86% vs 5.68% (limit 7.68%); probe-go NO GO. What passed: primary +2.47 [+1.31, +3.70] (83.99 vs 81.52), Brier 0.1099 vs
  0.1184, permutation flips 2.43% vs 3.78%, jagged 0.0% vs 0.6%, OPI 1.3% vs 1.8%, parity 100%. Consequences: C1 is NOT eligible as
  the 2B teacher (the 2B keeps 4B-E's 2-view labels); OHS-3 to be reported with and without 7 overlapping golden_train units;
  no further 4B top-up, merge or ensemble without a new amendment. [SRC A10]

---

## 5. Tests vs Jev since the 1 Oct report

### 5.1 JevBench v1.5.4, 231 public items, C1 (3 Oct ~03:40 UTC, free L4, eager, no CUDA graphs) [SRC `B/v154/RESULTS_30sep.md`; scores `B/runs/scores_v154_c1.json`]

| Run | Intelligence | Calib | Speed | Cost | Score A | Intelligence vs Jev p1 |
|---|---|---|---|---|---|---|
| C1 as trained (T=1) | 61.5 | 83.6 | 88.4 | 58.3 | 70.56 | -1.7 [-9.7, +6.6], tie |
| C1 committed yes/no | 75.1 | 78.4 | 88.4 | 58.3 | 73.36 | +11.9 [+3.0, +21.3], better |
| **C1 band edge (pre-registered)** | **75.1** | **83.1** | 88.4 | 58.3 | **74.34** | **+11.9 [+3.0, +21.3], better** |
| 4B-E band edge | 78.7 | 86.1 | 88.6 | 58.3 | 75.81 | +15.5 [+5.2, +26.9], better |
| Jev p1 | 63.2 | 81.2 | 91.4 | 52.5 | 68.80 | - |

- C1 vs 4B-E: choice 81.8 vs 80.6; yes/no committed 65.2 vs 75.9; hard yes/no tier 47.4 vs 57.9; score 78.4 vs 79.5.
- Caveat: public items were the dev set of 4B-E's lineage; unofficial; no sealed half. Speed axis here: Jev 91.4 vs ours 88.4
  (L4, eager). [SRC same]
- **Official board v1.5.4** (LIVE from `B/v154/leaderboard_v154.json`, 106 ranked): #1 Cygnet 73.70, #2 Winnow-12B 73.23,
  **#3 Jev 1.13.0 72.13** (Intelligence base 72.00: open 71.55, sealed 72.45), #4 jevk5-v0.3-4b 71.90 (best 4B), #5 plumb-4b 71.56,
  #6 jev-omni 71.50, #7 decider-4b-v2 71.28. 4B entries show big open->sealed drops (e.g. jevk5 61.6 -> 50.9). We have NOT submitted.

### 5.2 ejs-5 (868 n8n commit decisions; pre-registered 9a04df1; run once on backup L4 od-l4b; 2-view readout) [SRC `B/ejs5/runs/scores_c1_4be.json`, `B/ejs5/PREREG_ejs5.md`]

| | C1 | 4B-E (report-only) | Jev 1.13 (published) | GPT-5.6 Terra | Opus 5 |
|---|---|---|---|---|---|
| Pooled (868) | **54.15%** | 54.49% | 58.53% | 61.06% | 68.09% |
| Macro (4 tasks) | 60.17% | 60.31% | 64.40% | 66.85% | 74.20% |
| vs Jev, paired over 622 commits | **-4.4 [-7.8, -0.9], LOSS** | -4.0 [-7.3, -0.8], LOSS | - | - | - |
| Late rows (from 1 Jun 2026; 268 rows) | 46.3 vs 45.9: +0.4 [-5.3, +6.0], tie | 44.8: -1.1 [-6.6, +4.2], tie | 45.9 | 50.75 | 61.57 |

- C1 per task vs Jev: route 85.6 vs 85.6 (0.0 [-3.9, +3.9]); triage 66.2 vs 70.9 (-4.7 [-10.8, +1.4]); score/size 32.2 vs 37.2
  (-5.0 [-10.8, +0.8]); gate/risk 56.7 vs 63.9 (-7.2 [-16.1, +1.7]). [SRC]
- Rank 4th of 5 (Opus, GPT-5.6 Terra, Jev, C1; above only the keyword-regex baseline 43.4). [ORCH 04:35]
- Latency on L4 (2-view, batch 1): p50 230 ms, p95 242 ms, 0 errors. [SRC timing]
- My pre-run estimate was 59.6 (80%: 55.4-64.1); the result fell below it -> the estimate was too optimistic. [ORCH 04:35]
- Later analysis: of the ~38-item gap, an estimated ~20-41 items likely come from Jev's edge on early (pre-cutoff) rows; a tie on
  the full ejs-5 set is the realistic best case. [ORCH 15:00; `L/c_spec/RESEARCH_EXTRA_2.md`]
- From C on, ejs-5 is IN-DOMAIN (commit data from other repos is trained), so no "unseen" claim on ejs-5. [ORCH 06:30]

### 5.3 Step B: weight softening of C1 (A11; reads on od-l4b) [SRC `L/logs/b_wiseft_result.json`, 599c513]
- Unseen-source accuracy vs C1 (both halves, paired, n=3,847): a=0.9 +0.05 [-0.30, +0.40]; 0.8 -0.23 [-0.68, +0.23];
  0.7 -0.78 [-1.47, -0.13]; 0.6 -1.12 [-1.88, -0.37].
- a*=0.9 picked on dev-select, then FAILED confirm: unseen 84.33 vs 84.43 (needed +0.5); complement violations 4.47% vs 3.58%.
  Other checks passed. **Verdict: keep C1.** Parity: od-l4b re-read of C1 = od-l4 read, 100% (max |dp| 0). [SRC; ORCH 07:35]

### 5.4 A12: C1 vs Jev on OHS-1 + OHS-2 (now PRACTICE sets) [SRC `L/logs/A12_ohs12_result.md`, 629a9f4]

| Test | C1 micro | Jev micro | C1 - Jev [95% CI] | Macro C1 / Jev | Brier C1 / Jev |
|---|---|---|---|---|---|
| OHS-1 (1,847 base rows) | 80.4 | 81.7 | -1.2 [-2.9, +0.4], tie | 80.1 / 81.5 | 0.140 / 0.114 |
| OHS-2 (1,320 base rows) | 81.0 | 81.5 | -0.6 [-2.2, +1.1], tie | 81.3 / 82.0 | 0.057 / 0.038 |
| Pooled by rows | ~80.65 | ~81.61 | **~ -1.0** | | |

- Better than earlier 4Bs (A12 file: v11b -3.1 on OHS-1, v11c -1.0 on OHS-2; the 1 Oct report's scoreboard had v11c_cal -3.63 on
  OHS-1 and v11c -1.63 on OHS-2 - different readouts). [SRC]
- Stop bar (+1) not met -> C continues from C1. OHS-1/2 are never used for training or for choosing data from now on.

### 5.5 Decision Index ~10K sample, C1 (A13, report-only; od-l4b, started ~15:13 UTC, ~8 h; scored 23:52 UTC) [SRC `B/decision_index/report_sample10k.json`, `README.md`, `progress.log`]
- Harness `flaviusburca/decision-index` pinned 52a69892; suite rebuilt from pinned public sources (36/37 benchmarks identical to
  the lab's; HLE missing, gated, display-only). Sample seed 20260919: 10,001 requests / 82,939 questions / 96,142 reads.
  Checks: harness math reproduces Jev's published 59.51; scorer reproduces a published full run exactly; oracle check 0 mismatches.
- **Result: index 54.83 vs Jev v0.1 published 59.51 (-4.7)**; balanced skill 40.35 vs 46.26; breadth 38.96 vs 44.79. 9,999 ok,
  2 unsupported (over 16,384 tokens, scored wrong). Caveat: our SAMPLE vs Jev's FULL suite, not paired; about +/-1-2 pts.
- Areas (ours vs Jev raw): knowledge 51.2 vs 68.9 (**-17.7**); language 60.5 vs 62.3 (-1.8); retrieval 34.2 vs 37.0 (-2.9);
  tools 73.4 vs 73.4 (-0.05); arts 54.9 vs 56.0 (-1.1).
- Biggest losses: GPQA Diamond -38.8, GSM8K -23.1, CRUXEval -21.5, MMLU -9.5, POP909-CL -8.1, CLadder -7.6, iSarcasmEval -6.1,
  ChessBench -5.5. Wins (sample vs full, noisy): Humicroedit +3.4, BPoMP +2.6, ContractNLI +2.3, ToolRet +1.9, cfcolor +1.3, BFCL +0.3.
- v0.1 board: Jev 59.51, Jevfire 55.74, diffusiongemma 55.56, **C1 54.83 (would be ~#4)**, Decider 35B-A3B 54.34, razorback 51.52, Kev 9B 50.48.
- Disclosures: 285/10,001 sample requests share a 12-gram with C1's training file (MuSR 160/230 = 69.6%, display-only; BRIGHT 57/230;
  ToolRet 23/230; others small). BANKING77 and CLINC150 are C1 TRAINING sources (train splits; Index uses test splits).
- Never used to pick data, families, weights or models (A13). C's data will be decontaminated against every Index test item.
- Context (competitor research): on the newer v0.2.1 board Jev is 57.91 and the best 4B 43.04; MMLU-Pro Jev 82.7 vs best open 4B
  ~51.6. A LoRA cannot add that knowledge. [SRC `L/c_spec/RESEARCH_competitor-lessons.md` §0; recipe v4 §10.3]

### 5.6 Not run (still sealed or pending)
- OHS-3 (sealed; once, at the end, GO). LongBench v2 (kit built, never run; stays sealed). Sealed new-domains suite (no model has
  read it). JevBench sealed (not submitted; $49 fast lane = owner's call). Speed + cost test vs Jev on an H100 (added to the
  roadmap 3 Oct; GO, ~$5-8). [ORCH 15:35; ROADMAP]
- **LongBench flag:** Jev's 52.8% LongBench result was withdrawn, and the longjev repo cites TypeSafe terms that forbid publishing Jev
  benchmark results -> check before ANY public claim about Jev. [ORCH 04:45]

---

## 6. Research for C (3 Oct, CPU only, $0)

**Deep research (workflow w3p3ikjde, launched ~05:50 UTC)** -> files in `L/c_spec/` [SRC titles + §0 of each]:
- 7 web angles: `RESEARCH_competitor-lessons.md`, `RESEARCH_cross-domain-generalization.md`, `RESEARCH_expert-question-design.md`,
  `RESEARCH_licensed-data.md`, `RESEARCH_rl-for-decisions.md`, `RESEARCH_small-model-intelligence.md`, `RESEARCH_weight-preservation.md`;
  plus `LOCAL_GAPS.md` (where C1 fails on dev), 2 skeptic reviews (`REVIEW_methods.md`, `REVIEW_rules.md`: 4 blockers each),
  3 licence checks + `LICENCE_REGISTER.md` (PRIVATE). The final revision step stalled 6x and was redone by focused agents. [ORCH 08:20-15:25]
- Key findings (plain):
  - No open 4B matches Jev on broad unseen tasks; most big 4B wins over Jev are in-distribution. Jev leads most on new task
    families and on knowledge. [competitor-lessons §0]
  - **Breadth beats volume:** count distinct task cards, not rows; gains flatten at ~64 rows per task; <300 distinct instructions
    never generalized, >=1,000 did. Many wordings per task help small models most. [cross-domain §0; small-model §0]
  - Labels must be exact (program labels; two different solvers; models never set a label). LLM-written text has shortcuts;
    decontamination must go beyond n-grams. [expert-question §0]
  - **RL does not help a one-token readout** (no GRPO/PPO); keep cross-entropy/KD. [rl-for-decisions §1]
  - Keep C1's skills with replay (50-60%) + a C1 anchor; old-skill change expected -0.5 to +0.5; weight preservation does not
    create far-domain gains. [weight-preservation §0]
  - Licences: 50 usable commercial datasets; HF licence tags are often wrong (5 mismatches found); C1's replay had licence and
    contamination problems (e.g. Yelp NC, LogiQA 2.0 NC-SA, MuSR = DI test items). [licensed-data §0]
- **Completeness pass (w6191aqn0, done ~15:00 UTC):** `RESEARCH_EXTRA_1-6.md` (ordinal readout; causes of the ejs-5 gap; calibration
  under shift; selection methods; family interference + loss weights; Qwen3.5 hybrid facts) + `ADDENDUM_research.md`. 8 agents,
  0 errors. ADOPT rows: A1 ordinal target lint; A2 balanced end levels; A3 Score T = 1; **A4 mean-E term on ordinal rows (the only
  new loss)**; B1 message-only commit rows (30%); B2 per-rule yes rate 20-80%; B3 yes-share drift alarm (report-only); B4 no test-time
  prior fix; C1-C3 per-type temperature, leave-one-group-out, within [0.8, 1.3]; D1 no LESS/influence selection; E1-E3; F2 rendered-prompt
  sha assert; F3; F4 O*NET personas (never PersonaHub). B6 (ejs-5 gold decomposition) NOT run, to keep ejs-5 clean. [SRC ADDENDUM; ORCH 15:00]

**Spec + recipe v4 (final ~16:30 UTC; pinned in A16)** [SRC `L/c_spec/C_DATA_SPEC.md` v4 §0, `C_TRAIN_RECIPE.md` v4 §0, §4, §10]
- Data round 1 = **150,000 rows**: 90,000 replay of C1's data (60%) + 60,000 new: 45,250 own program-labelled rows (13 families
  F1-F13), 8,750 licensed public human-labelled rows (14 datasets), 6,000 commit decisions from other repos (never n8n).
  Round 2 = 300,000 (superset), only on a clear win. >= 1,050 distinct task cards in round 1 (median ~40 rows/card, max 128).
- Seven rules: breadth beats volume; every label exact; no shortcuts; no leaks; sealed suite built first by a separate agent;
  deny-list from every rejected/avoid entry; no Jev output ever an input.
- Dropped/kept out: ShARC, Measuring Hate Speech, CAD-SNLI, Social IQa, CosmosQA, e-CARE, EmoBank, ConvAbuse, NewsMTSC (and
  607 replay rows), DocFinQA, MultiHiertt, ConvFinQA; CodeReviewer out. 28 replay sources (53,270 rows) "VERIFY or drop" (HF-card-only licence). [SRC spec §0.1; ORCH 15:25]
- **Equal commit shares fix (verifier blocker):** v3 had set commit-type shares 10/20/25/35/10 from the ejs-5 per-task C1-vs-Jev
  gaps. That breaks the owner rule (ejs-5 never chooses anything). v4 uses **equal 20% shares** (route, triage, score, gate, match:
  1,200 rows each in round 1). 30% of gate/triage/route rows are message-only (1,080 in r1). [SRC spec §0.1-0.2; ORCH 16:10]
- Training: start from C1; continue its LoRA (r16/a32, 32.46M trainable); AdamW; **peak LR 5e-5** (C1 7e-5); one pass; ~8,880 steps
  in r1; C1's losses unchanged + `lam_ord` 1.0; base anchor off; C1 anchor only where C1 is right AND confident (p_top >= 0.8) or on a
  protected skill. **One candidate per round** (the final-step adapter; no snapshots, no blends). RL not in the plan.
- Gate: ship only if sealed part-A **confirm** gain over C1 >= +1.0 pp with LB > 0, AND guards D1-D6 + D9 (dev, security, calibration,
  option order, latency) pass. Round 2 only if **select** gain >= +2.0 pp with LB > 0. Looks: S1, (S2), C once; Jev read once after the
  ship verdict. ejs-5, OHS-1/2/3, JevBench, DI and LongBench never choose anything.
- Recipe's own odds (EST, `sim/gate_sim_c.py`): power ~77% at a true +2.0 gain (88% at +2.5); ~2% false ship at a true 0;
  **P(round 2 runs) ~13%; P(C ships) ~22% (14-33%)**; if it ships, true sealed gain ~+2.1; expected shipped gain ~+0.5.
- Cost (Modal H100 at $4.09/h): r1 ~$27.4 + ~$2 = **~$29.5 planning** (+12% s/step sensitivity: ~$33; hard stop if projected > $35);
  r2 ~$57 (trimmed to fit the cap); **expected C spend ~$37**; all C Modal spend <= $100; $25 reserve untouched.
- A16 ruling: addendum D2 (facility-location selection) NOT adopted. [SRC A16]

---

## 7. Sealed new-domains test suite: v1 -> v2 (counts by domain id only)

- **A14** (a79e5d4, rules before any item existed): isolated builder agents read only `sealed_brief/` and write only `sealed_nd/`
  (both git-ignored); orchestrator sees counts by domain id only. Part A >= 5,000 real-text items over 6-10 domains (none > 20%;
  >= 4 non-adjacent domains holding >= 50%); part P 3 x 200 program-built; B1 300 commit items (repos outside CommitChronicle/
  CommitPackFT, never n8n); B2 200 long documents (4-8K tokens). Split by hash: 40% select / 60% confirm. Gold from humans,
  officials or programs, never an LLM. A domain with > 8% clearly wrong gold is dropped. [SRC A14]
- **v1 (~18:30 UTC): NOT READY.** 7,221 items; part A 6,122 over 9 domains; but only 1 of 9 part-A domains was non-adjacent (rule:
  >= 4 holding >= 50%); sealed item text had spilled into shared session folders; B2 had 199 items; 2 B1 near-duplicate pairs.
  **No waiver** (owner: no compromise). v1 was never read by a model. [ORCH 18:30; A15]
- **Isolation incident (disclosed in A15):** sealed text in session temp folders (tool-results, task outputs, scratchpad). With the
  owner's OK: 31 files deleted, sealed transcripts moved into `sealed_nd/`, re-scan (12-gram hashes) found 0 files with >= 3 hits
  outside. C builders may not open `~/.claude/projects/**` or `/private/tmp/claude-501/**`. [SRC A15; ORCH 18:30, 20:55]
- **v2 FROZEN - A15** (3abd721, git 20:34 UTC): suite sha256 `f4ae8637...`, scorer sha256 `953a3363...` (prints aggregates only,
  logs every look, refuses looks not in the plan). [SRC A15]

| Part | Items | Notes |
|---|---|---|
| **A (headline, real text)** | **6,205** in 8 domains | select 2,542 / confirm 3,663; largest domain 16.1% |
| - non-adjacent domains | D1, D10, D11, D12 = 3,446 (55.5%) | rule met (>= 4 holding >= 50%) |
| - adjacent domains | D2, D3, D4, D5 = 2,759 | |
| P (program-built) | 600 (3 x 200) | report-only |
| B1 (commits) | 298 | 2 near-dup groups dropped from 300 |
| B2 (long documents) | 199 | 1 decontamination drop; 4,148-7,718 tokens |
| **Total** | **7,302** | select 2,988 / confirm 4,314; yes/no 46.5% of items (gold yes 50.0%); 58.2% card-free; 2-8 options |

- Decontamination (counts-only, 12-grams vs C1's 501,732 training rows) dropped 43 v1 items + 18 new items (whole groups).
  Noise-floor reads flag-only: at most 1.5% clearly wrong per domain; none dropped. [SRC A15]
- Jev will be read on it ONCE, at the C look, after the ship verdict (OpenRouter spend = owner GO). [SRC A15]

---

## 8. A16 and A16.1 (the C round-1 plan, pre-registered)

- **A16** (27d8b0a, git 20:35 UTC): spec v4 `4ca12996`, recipe v4 `f4b79150`, addendum `0da2e834`; config `runs/q35_4b_c_r1.json`
  `f3bb379e`, **seed 20261003**; trainer `c2c2d1d6`, readout `908c08d7` (all changes default-off; C1 reproduces bit for bit); one
  candidate; ~$30 under GO + smoke <= $0.5; data 150,000 (90,000 replay + 45,250 own + 8,750 public + 6,000 commits); G9 crowd
  scoring on the free L4 only. Deny-list rulings: (a) bare platform words (Wikipedia, Reddit, GitHub...) never match alone; (b) entries
  rejected only for label quality are `no_new_rows`, not `taint` (T-REx; MuSiQue passes); (c) "locked" = "avoid"; (d) the A10 overlap
  handled by dropping gd_redocred + gd_helpsteer3_pref whole; (e) attacked replay rows with C1 p_g < 0.2 are counted as successful
  attacks, not dropped. "neither ... nor" = one syntactic negation. G0 family specs frozen per family with sha logged before the first
  generator run; a generator may not run with any open label-flip ambiguity. [SRC A16]
- **A16.1** (18c024c, git 23:57 UTC): pinned tool versions (denylist v1.2 `e268d566`, aliases v1.1 `40eeb47e`, negcount v1.1 `79368f46`,
  replay_sample `5735ca3e`); 17 sub-entries moved to `no_new_rows`/label_quality; replay writer refuses stale verdicts and needs the
  A15 sha; replay draw written with these (99,069 rows in 20 shards + 2,000-row old slice). (f) EDOS 2-of-3-annotator filter on every
  EDOS row. (g) Choice rows: everything a row needs goes in instructions, state or "- option: definition" lines (the layout shows only
  option-definition card lines on choice rows); `loader_check` on every row; token caps count instructions twice. [SRC A16.1]

---

## 9. Build status

### 9.1 Trainer prep (w0lmz9jm0, READY ~19:00 UTC) [ORCH 19:00; A16]
- A4 ordinal term + F2 rendered-prompt assert added, **default-off**; C1 reproduces bit for bit; 297 + 55 tests pass (1 failure was
  already there before). Draft config `runs/q35_4b_c_r1.json` (sha f3bb379e, LIVE-matched).
- Kernel note: causal_conv1d is missing on both the L4 and the Modal image (fla present); reads are prefill-only, so a fast-kernel
  gain would be only ~1.2-1.5x. [ORCH 17:55]

### 9.2 Replay draw (written 3 Oct 20:50 UTC) [SRC `L/c_build/replay_r1_write.json`, `replay_counts_dryrun.json`]
- Pool: C1's 501,732 rows / 204 sources. **83,807 rows dropped** by licence/deny rules: VERIFY (HF card only) 35,152; VERIFY 14,749;
  A8' OHS-3-hit sources 11,348; DROP 9,085; DROP default 8,607; forbidden list 4,866. Eligible: 414,770 rows / 118 sources (after a
  2,000-row "old slice" held out for forgetting checks).
- **Round-1 draw: 99,069 rows** (90,000 + 10% margin), 85,352 units, 118 sources; hard yes/no 58,139 rows at 49.85% yes; attacked
  rows 6,469; **134,025 C1 reads** needed (A5 readout). Round-2 superset draw: 197,824 rows. L4 estimate 10.7-11.8 h.
- F2 check: the 6 rendered-prompt views on od-l4b are byte-identical to the Mac (LIVE: `f2_l4.json` vs `f2_local_mac.json`, 6/6),
  despite different transformers versions (5.17.0 vs 4.57.6).

### 9.3 Phase 1 (building blocks; launched ~20:55 UTC; all reviewed + fixed to v1.1 by ~22:36 UTC) [SRC `L/c_build/progress_phase1.log`; manifests in `L/c_src/`]
| Block | Result (counts only) |
|---|---|
| Packs (4 builders) | **332 packs**: packs-1 88, packs-2 80, packs-3 80, packs-4 84 (O*NET persona seeds; lint clean; sealed_check 0 blocking) |
| Formats-1 v1.1 | **400 format styles** (350 training, 50 held out for dev only), 77 skins, 12 card styles, 14 containers |
| Formats-2 | 672 family wordings, 98 public wordings, 62 real-text codebooks; record pools for codebook rows |
| Public-1 v1.1 | 3,275 r1 rows (SQuAD2 900, MuSiQue 1,000, 2Wiki 600, QuALITY 775) + reserve 815 + mix-tuning dev 210; 175 rows moved to F13 (Qasper fallback) |
| Public-2 v1.1 | 2,900 r1 rows (HybridQA 1,000, WikiSQL 1,150, DROP 250, UCI Car 200, UCI Nursery 300) + reserve 937 + dev 191 |
| Public-3 v1.1 | 2,400 r1 rows (XED 600, MAMS 750, Sarcasm 350, GHC 350, EDOS 350) + reserve 625 + dev 198 |
| **Public total r1** | **8,575 + 175 moved to F13 = 8,750 (plan)**; deny-list pass, 0 taint; sealed_check 0 blocking |
- Key rule found in phase 1 (now A16.1 (g)): on choice rows the layout shows only "- option: definition" card lines. The mixer must call
  fmt1 `pool.refuse_held_out`. [ORCH ~00:10 UTC 4 Oct]

### 9.4 Phase 2 (families; workflow w9cr58a3r, running) [LIVE `L/c_build/progress_phase2.log`, `L/c_src/*/G0_FROZEN.json`]
- G0 rule sheets did not converge by review (fresh reviewers kept finding ~6-12 new label-flip items per round; after round 2, 338
  open items of which ~98 could flip a label). Plan used: one resolve-only final pass, then freeze; real label guarantees = G2
  (independent solver B by a different agent), G3/G4, G5 blind reads. [ORCH 18:45, 20:55]
- **All 14 G0 specs FROZEN** (F1-F13 + COMMIT), 4 Oct 00:12-00:50 UTC, each with sha256 logged and 0 open label-flip ambiguities.
- Generator code being written for F2, F3, F4, F6, F8 (logged starts 00:28-00:55 UTC); `gen/` folders also exist for F1 and F7.
  **0 family rows produced yet** (all `out/` folders empty at 01:02 UTC).
- Flags from the logs: F13 mean served length ~6.0-6.5K tokens (v4 assumed ~4.6K); F10 risk: card printed twice on choice rows may
  exceed the median length budget (stop-and-report rule applies).
- Still to do after phase 2: mixer (G9 crowd selection, replay + anchor merge, token cap); G9 crowd scoring on the L4 (C1, 4B-E, base
  4B); counts-only decontamination vs OHS-1/2/3, DI test items, JevBench; smoke run (<= $0.5) -> owner GO -> round 1. [ORCH 00:10 4 Oct]

### 9.5 L4 replay read (C1 reading the 99,069 replay rows; od-l4b) [ORCH last entries]
- Started ~00:00 UTC 4 Oct; F2 passes on the L4. ETA ~11-12 h (about noon UTC Sunday). As of ~00:50 UTC: shard 1 not done after
  55 min (slower than estimated); a memory hiccup was recovered; the finish time will be re-estimated after shard 1. Watcher bjrlpd8of.
  Progress is on the VM, not local; LIVE status not checkable without ssh.

### 9.6 Knowledge-gap research (whl9uhvgk, launched ~00:45 UTC 4 Oct; drafts dated 00:58-01:01 UTC) [LIVE `R/knowledge_gap/`]
- **Research running.** No PLAN file yet. 5 researcher drafts exist: `R_testtime.md` (test-time compute), `R_retrieval.md` (RAG),
  `R_tools.md` (tools), `R_training.md` (training-side), `R_measure.md` (honest ceiling + clean dev sets). Synthesis -> skeptic ->
  `PLAN_knowledge_gap.md` pending. Rule: validated on separate dev sets with no DI test overlap; round 1 untouched.

---

## 10. Money (spent and left)

| Item | Value | Tag / source |
|---|---|---|
| Modal credit left, all 7 accounts | **$141.46** at 1 Oct 23:40 UTC (jaypatil-duke 30, arya-mahadik-ai 2.55, aryamhd 3.69, atmosphor 15.22, mahadikarya2/3/44 30 each) | ORCH 1 Oct 23:45 (from billing) |
| Modal spent since the 1 Oct report | **$0** (C4 never trained; B, A12, ejs-5, JevBench public, DI and the replay read all ran on the free Google L4) | ORCH 02:10, 04:35; A10 |
| Modal left now | ~$141.46 (not re-checked: `budget_tracker.py` calls Modal billing) | EST |
| Owner cap for C | up to ~$100 on Modal; keep the $25 reserve ($141.46 - $100 = $41.46 >= $25) | ORCH 04:45, 05:00 |
| C plan spend | r1 ~$29.5 (hard stop $35) + smoke <= $0.5; r2 ~$57 only if it runs; expected ~$37 | recipe v4 §4 |
| OpenRouter (Jev calls) | balance $6.58 of a $10 limit on 30 Sep; no Jev calls since (A12 used saved Jev preds; DI used the published board; ejs-5 used Jev's published answers) -> ~$6.58 | M/keep-openrouter-key.md; EST |
| Planned OpenRouter | one sealed-suite Jev read (GO) + OHS-3 (~4,912 calls, ~$1.2-2.7) | A15; keep-openrouter-key.md |
| Google L4 credit | used for probe-go, JevBench public, ejs-5 (~$0.30-0.40), B, A12, DI (~8 h, ~$5-8), replay read (~11-12 h); balance not in allowed files | EST; ejs5 README; DI README |
| Real money not spent | JevBench sealed fast lane $49 per model (owner's decision); H100 speed/cost test ~$5-8 (GO) | ROADMAP; ORCH 15:35 |

---

## 11. Timeline and projections given to the owner

**Timeline (latest; EDT)** [SRC `R/ROADMAP_2oct.md` "Final timeline"; ORCH 18:05, 19:00]
- Sat 3 Oct: sealed test locked (A15) + C plan (A16) - DONE; DI result - DONE (~7:50 pm EDT); data build started.
- Sun 4 Oct: replay read (~11-12 h) + family build + QC; family-by-family L4 crowd scoring (one free L4; quota 1).
- Honest L4 total for round 1: replay ~11.5 h + crowd ~16-20 h -> **training start ~Mon 5 Oct early morning EDT** (the roadmap's
  earlier "Sun ~11 pm EDT" is superseded). Round 1 training ~7 h (~$30, GO); gate reads after.
- Tue 6 Oct: round-1 verdict. If round 2 runs (only on a clear win): data Wed 7, train Thu 8, verdict Fri 9.
- Finish: **Wed 7 Oct** without round 2 (sealed confirm + Jev read -> OHS-3 once -> speed/cost test -> report); **~Sat 10-Mon 12 Oct**
  with round 2. Up to ~10 days if repairs are needed. [ORCH 06:10]
- Note: the owner was told the weekday slip was corrected (4 Oct = Sunday, 5 Oct = Monday). [ORCH 17:30]

**Projections told to the owner (EST)** and how they compare with later numbers:

| Target | Told to owner (when) | Later evidence / recipe v4 analysis |
|---|---|---|
| OHS-3 vs Jev | **+0.8 median; tie-or-better ~60%; >= +1 ~45%** (05:40; repeated 14:35) | **Recipe v4 §10.3 (after A12):** median observed gap after C **-0.8**; P(>= Jev - 1) 56%; **P(>= Jev) 31%**; P(>= Jev + 1) 14%. It says: "The earlier projection (tie-or-better on OHS-3 about 60%) is not supported after A12." **The PDF must show both and say the lower one is the current best estimate.** |
| New-domains suite | +1.5 over C1 (05:40) | Recipe prior: r2 candidate median +1.0 (80%: -1 to +3); r1 ~0.7 of that; P(C ships) ~22% |
| ejs-5 | ~58-62, in-domain now (05:40) | Recipe: if C ships ~55 (80%: 52-58); P(>= Jev) ~2%; P(within 2 pp) ~7%. Realistic best case: a tie (ORCH 15:00) |
| JevBench sealed | Score A ~72-75 (beat Jev ~65%); Intelligence ~66-72 (beat ~30%) (05:40) | ROADMAP 13:30 EDT: Score A ~74.5 (71-77) vs Cygnet 73.70, Winnow 73.23, Jev 72.13; Intelligence ~69 (61-75) vs Jev 72.0. Method: A = 0.25 x (I + Cal + S + C); official 4B entries S + C ~143, Jev ~128.5 (ORCH 17:30) |
| Decision Index | top-5 on several decision tasks; ~#10-20 overall (05:40) | Measured (sample, v0.1 board): 54.83 vs 59.51, ~#4; wins on 6 tasks, large knowledge losses |
| LongBench | loss (05:40) | not run |
| ejs-5 before the run | 59.6 (80%: 55.4-64.1) (ORCH 04:35) | measured 54.1 -> estimate was too optimistic |
| Honesty line | "Not guaranteed to beat Jev on everything" (14:35) | Recipe: "C is a careful, low-risk step, not a jump"; expect ~+0.5 pp shipped gain on average (+2 when it ships) |

---

## 12. Overall scorecard vs Jev (shipped C1, as of 4 Oct 01:00 UTC)

| Goal axis (3 Oct goal) | Best evidence now | Status |
|---|---|---|
| Unseen accuracy, OHS-1 / OHS-2 (practice now) | -1.2 [-2.9, +0.4] / -0.6 [-2.2, +1.1]; pooled ~-1.0 | TIE (at the "-1 acceptable" edge) |
| Unseen accuracy, OHS-3 | sealed, not run | UNKNOWN |
| Unseen accuracy, sealed new-domains suite | frozen, not read | UNKNOWN |
| Decision Index (report-only, sample) | 54.83 vs 59.51 (-4.7; knowledge -17.7) | LOSS (knowledge) |
| ejs-5 (in-domain from C on) | 54.1 vs 58.5, -4.4 [-7.8, -0.9]; late rows tie | LOSS |
| Calibration (OHS-1/2 Brier) | 0.140 vs 0.114; 0.057 vs 0.038 | LOSS |
| Hijack (jagged ASR, dev saved reads, 1 Oct) | 0.0% vs 99.4% | WIN (carried over) |
| Injection (OPI ASR) | 1.3% vs 1.3% | TIE (carried over) |
| Consistency vs Jev | no new paired data since 1 Oct (C1 dev: complement 3.30%, option-order flips 2.43%) | UNMEASURED vs Jev |
| Speed | JevBench public L4 speed axis 88.4 vs Jev 91.4; 1 Oct H100+graphs axis 94.7 (4B-E, not C1) vs 83.8; L4 p50 230 ms (ejs-5, 2-view) vs Jev 70-500 ms e2e | MIXED; H100 test pending |
| Cost | JevBench formula axis 58.3 vs 52.5 (ours cheaper); real serving cost never measured | WIN on formula only |
| JevBench | public (dev-exposed, unofficial) Intelligence +11.9 [+3.0, +21.3], Score A 74.34 vs 68.80; official sealed not submitted | WIN (public only) |

---

## 13. Open risks (honest)

1. **Projection mismatch:** the owner holds "+0.8 / ~60% tie-or-better on OHS-3"; the recipe's own model after A12 says median -0.8 /
   31%. Must be corrected in the PDF. [ORCH 05:40, 14:35 vs recipe v4 §10.3]
2. **C will most likely not ship:** P(ships) ~22%, P(round 2) ~13% (EST). The likely outcome is C1 stays, at ~-1 vs Jev on OHS-like
   sets. Downside is money (~$37 expected), not a worse model (gate keeps C1). [recipe v4 §10]
3. **Knowledge gap is structural:** DI knowledge -17.7 pp (GPQA -38.8, GSM8K -23.1, CRUXEval -21.5); a LoRA cannot add base-model
   knowledge. Research running; any fix must be validated off DI. [DI report; recipe §10.3; ORCH last entry]
4. **One GPU:** Google GPU quota 1, increase auto-denied (twice). Replay read already slower than estimated -> timeline slip risk;
   owner chose free L4 only. [ORCH 17:15, 17:25, last entry]
5. **Label quality vs time:** G0 specs never converged by review (frozen with 0 open flips, but fresh reviewers kept finding new edge
   cases); reliance on G2/G3/G4/G5. [ORCH 20:55]
6. **Isolation slips happened** (sealed text spill; repeated OHS-3 glob reads by agents on 2-3 Oct: counts/ids/file names only, all
   disclosed). Many agents -> continuing risk. [A15; `M/exclude-ohs3-from-scans.md`]
7. **OHS-3 overlap:** 7 golden_train units share 12-grams with OHS-3 (C1, and maybe 4B-E, trained on them) -> report OHS-3 with and
   without those items. [A10 D.]
8. **C1 shipped by override** with a failed consistency condition and a failed fix pre-check (both weak on nested negation, ~34% flips);
   must be on the model card; C1 cannot teach the 2B. [A10]
9. **Legal:** TypeSafe terms (cited by longjev) may forbid publishing Jev benchmark results -> check before any public claim. [ORCH 04:45]
10. **ejs-5 is no longer unseen** (commit data trained); closing its gap is unlikely (P ~2%). [ORCH 06:30; recipe §10.3]
11. **Calibration:** Jev's Brier is better on OHS-1/2; temperature only via leave-one-group-out within [0.8, 1.3]. [A12; addendum C1-C3]
12. **Length/cost drift:** F13 served length ~6.0-6.5K vs ~4.6K assumed; +12% s/step -> r1 ~$33 (hard stop $35). [phase-2 log; recipe §4]
13. **Code and plan files not in git** (pinned only by sha in A16/A16.1); disk is 96% full (19 GiB free, LIVE `df`). Loss of these files
    would break the C plan's audit trail.
14. **Session/app interruptions:** app quit (~14:30 UTC), usage limit (17:25 EDT); long workflows may die and need relaunch. [ORCH; HANDOFF 3 Oct]
15. **Speed claim not proven:** on the public L4 run Jev's speed axis is higher (91.4 vs 88.4); the H100 direct-hosting test has not run.
16. **2B and cascade paused:** the original 30 Sep goal (final 2B + cascade) is not being worked on. [ORCH 04:45]

---

## 14. Items in the 1 Oct report that are now out of date

- "4B-E stays the shipped 4B / pre-registered fallback" -> **C1 is shipped** (A10 override).
- "fix2 / C4 top-up next (~$9-11), job 3 re-test" -> **probe-go NO GO; C4 never trained; $0.**
- 2 Oct roadmap (26 rows: 2B teacher, 2B A/B, 2B main, cascade, ejs-5 on 2B) -> **replaced** by the 4B-only C flow; 2B paused.
- Scoreboard OHS rows used older 4Bs (v11c: OHS-1 -3.63, OHS-2 -1.63) -> **C1: -1.2 / -0.6** (A12). OHS-1/2 are now practice sets.
- JevBench public row showed 4B-E -> add **C1: 75.1 / 74.34** (band edge).
- Projections section (30 Sep FINAL_PROJECTION: 4B -0.3 [-3.6, +3.2] vs Jev) -> superseded by recipe v4 §10.3 and the A12 start gap.
- Budget: "$113-117 planned, ~$24-28 left" -> now **~$141 left, C cap ~$100, expected ~$37**.

---

## 15. Source index (all allowed files read)

- Git: `git -C J log --since=2026-10-02 --stat --oneline` (14 commits, §2).
- `L/PREREG_FINAL.md`: A8' (lines 525-977), A10, A11, A12, A13, A14, A15, A16, A16.1 (lines 978-1184). No A9 exists (option D blocked).
- `M/final-goal-30sep.md` (main log; entries 3 Oct 01:15 UTC to the last entry, saved 4 Oct 00:51 UTC), `M/MEMORY.md`, `M/keep-openrouter-key.md`,
  `M/exclude-ohs3-from-scans.md`, `M/fair-test-pick.md`.
- `R/ROADMAP_2oct.md`; `J/HANDOFF.md` ("HANDOFF 3 Oct 2026, 17:25 EDT").
- `L/logs/b_wiseft_result.json`; `L/logs/A12_ohs12_result.md`; `L/logs/budget_ledger.md` (no new entries since gate job 1).
- `B/ejs5/README.md`, `B/ejs5/PREREG_ejs5.md` (§5 published table), `B/ejs5/runs/scores_c1_4be.json` (aggregates).
- `B/v154/RESULTS_30sep.md` (3 Oct C1 section), `B/v154/leaderboard_v154.json` (board A order and scores).
- `B/decision_index/report_sample10k.json`, `B/decision_index/README.md`, `B/decision_index/progress.log`.
- `L/c_spec/C_DATA_SPEC.md` v4 (header, §0, §0.1, §0.2, §1), `L/c_spec/C_TRAIN_RECIPE.md` v4 (§0, §4, §10), `ADDENDUM_research.md`
  (header, §0), `RESEARCH_*.md` and `RESEARCH_EXTRA_*.md` (titles + §0/§1), `REVIEW_*.md` (first lines), `LICENCE_REGISTER.md` (title only).
- `L/c_build/replay_counts_dryrun.json`, `replay_r1_write.json`, `f2_l4.json`, `f2_local_mac.json`, `RUNBOOK_replay_reads.md` (grep),
  `progress_phase1.log`, `progress_phase2.log`, `progress_tools.log`, `progress_prep.log` (heads/tails).
- `L/c_src/*/G0_FROZEN.json` (existence), `c_src/packs/*/manifest*.json`, `c_src/formats/formats-1/MANIFEST.json`,
  `c_src/formats/formats-2/manifest.json`, `c_src/public/*/manifest*.json` (counts only).
- `R/knowledge_gap/R_*.md` (titles only; no PLAN yet).
- `R/pdf_build_1oct/build.py` (section titles, scoreboard rows) to set the cutoff and the "out of date" list.
- LIVE checks: sha256 of 9 pinned files (all match A16/A16.1); `git status` of them; `df -h` (19 GiB free); F2 L4 vs Mac (6/6 equal).
