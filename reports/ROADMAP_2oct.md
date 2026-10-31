# OpenDecide roadmap (updated 2 Oct 2026, 11:45 UTC)

Goal: beat Jev (jev-1.13) with the final 4B, the final 2B and the 2B→4B cascade. Sequence agreed with the owner:
4B fix → final 4B → ejs-5 (4B) → 2B → settings → ejs-5 (2B, cascade) → OHS-3 once → JevBench sealed (owner's decision) → report.

| # | Step | Status | Details / if → then | Cost | When (EDT) |
|---|---|---|---|---|---|
| 1 | 4B main run (C1, q35_4b_main500k) | ✅ Done 1 Oct | 30,457 steps, 5 relays, every resume exact; backed up on the Mac | ~$94 | — |
| 2 | Gate C1 vs 4B-E | ✅ Done | +2.47 on unseen dev (84.0 vs 81.5). Failed only double-negation consistency (8.86% vs 5.68%) → DO NOT SHIP | L4 | — |
| 3 | Diagnosis + research | ✅ Done | Drops one "not" (32/60 hate pairs). Owner chose fix A (fix2). Negation checklist of 38 types | free | — |
| 4 | yn2b hard data for the 2B | ✅ Done | 9,130 program-labelled hard yes/no rows, decontaminated | free | — |
| 5 | 4B readout settings + OHS-3 harness | ✅ Done | Dev only: T 1.00/1.00, choice read twice, yes/no once. Dry runs pass | free | — |
| 6 | Security vs Jev (saved reads) | ✅ Done | Hijack 0.0% vs 99.4%; injection 1.3% vs 1.3% | free | — |
| 7 | Fair outside tests chosen | ✅ Done | ejs-5 first (cheap, out-of-domain), then JevBench sealed | free | — |
| 8 | **A1: F7 build + full checks** | ⏳ **Running** (wahbv0n40) | Prep done: audit tool, A8′ rules, 220 blind questions, hosting gaps. Main build started 23:47. Then label check, audit and repairs, blind read, assembly, 3 skeptics, PDF. If a check can't pass → owner chooses | free | done ~5–7 am |
| 9 | A2: show counts → GO | Next | Exact cost quote | — | morning |
| 10 | A3: fix training (C4) | Next | ~2,500 steps, Modal jaypatil-duke, .spawn launcher | ~$10–11 | ~2 h |
| 11 | A4: pre-check | Next | Double-negation errors cut ≥50% AND blind questions not worse → A5; else final 4B = 4B-E | L4 | — |
| 12 | A5: re-test on the original L4 | Next | Passes vs 4B-E AND not worse than C1 anywhere → final 4B = C4; else 4B-E (C1 only by a disclosed owner override) | L4 | midday–afternoon |
| 13 | A6: back up the final 4B | Next | One copy | free | — |
| 14 | B1: JevBench public on the final 4B | Next | Practice set; report only | free (L4) | 2 Oct |
| 15 | B2: **ejs-5 on the final 4B, once** | Next (owner OK) | Settings written first (0.5 yes/no cut, as the author scored Jev); compared item by item with Jev; no changes after | ~$0.5 / free L4 | 2 Oct |
| 16 | C1: 2B teacher | Next | C4 final AND passes teacher checks → re-label (GO); else ready 4B-E labels | ~$23 optional | 2–3 Oct |
| 17 | C2: 2B A/B (L4, GO) | Next | A base / B + hard data (yn2b + F7) / C teacher gate. Adopt only if it passes the rule and choice questions don't drop | L4 | 3 Oct |
| 18 | C3: 2B main (GO) | Next | Budget check: too low → skip the re-label or add an account | ~$74 | 3–4 Oct (~17 h) |
| 19 | C4: 2B re-test | Next | Pass → final 2B; else the best earlier 2B, disclosed | L4 | 4 Oct |
| 20 | D1: 2B + cascade readout on dev | Next | Cascade only if it pays (today: 4B alone wins by 0.25) | free | 4 Oct |
| 21 | D2: speed + cost test, H100 (GO) | Next | Direct hosting | ~$5–8 | 4–5 Oct |
| 22 | D3: pre-register every setting (commit) | Next | Nothing changes after this | free | 5 Oct |
| 23 | E1: ejs-5 on the 2B + cascade, once | Next (owner OK) | Same rules as B2 | ~$0.5 | 5 Oct |
| 24 | E2: **OHS-3, once** vs Jev (GO) | Next | Win = accuracy ≥ Jev (tie OK) + hijack, injection, consistency, speed, cost | ~$3 + GPU | 5 Oct |
| 25 | E3: **JevBench sealed** (owner decides) | Next | Decide after ejs-5 + OHS-3. Fast lane $49 per model (private, 48 h) or free queue (public, 1+ weeks). Headline = sealed choice + score only | $0 or $49+ (real money) | 5 Oct+ |
| 26 | E4: final report | Next | Outside-test win claimed only if ejs-5 and JevBench sealed agree | free | 5–6 Oct |

Money: Modal $141.46 now; plan ~$113–117 → ~$24–28 left (target $25+ reserve). JevBench $49 is real money, not
Modal credit.

## Update 11:45 UTC
- Models in the re-test: 4B-E (`q35_4b_pxE`, the yardstick to beat), C1 (`q35_4b_main500k`, must not get worse; its
  double-negation errors must fall by at least 50%) and C4 (`q35_4b_main500k_fix2`, the candidate).
- Overlap: the L4 reads 4B-E and C1 while C4 trains on Modal (A8′ section E0). After training, only C4 is read.
- Owner GO covers rows 8-12. PAUSE after the re-test and report every number; the owner decides everything after that.
- Row 8 status: the build is done (12,590 train rows, all 38 types), training labels agree 100%, and repair round 1 is
  running (18 audit fails to close).

## Update 3 Oct ~01:30 UTC (2 Oct 9:30 pm EDT)
- Done: F7 v2 r6 (12,768 rows, 38 types); decide2 100%; precheck 112 PASS; blind read 4 on r6 PASS (0 wrong, 1.33%);
  fixer closed 21 skeptic issues. The owner OHS-3 check found 7 replay units (gd_redocred 6, gd_helpsteer3_pref 1), so
  both sources are excluded and fix2 is being rebuilt (re-check must be 0). The original od-l4 is RUNNING.
- Next: fill + commit A8′ → step 0b probe-go on L4 → C4 training on Modal (~2.1 h, ~$8.6) with the L4 reading 4B-E/C1
  → C4 reads → conditions + ship look → PAUSE (ETA ~3-3:30 am EDT 3 Oct).
- Proposed order after the pause (owner to confirm): JevBench public + ejs-5 + LongBench v2 (Jev's exact setup) on the
  final 4B → 2B → settings/speed → ejs-5/LongBench on 2B/cascade → OHS-3 once (with/without overlap items) → JevBench
  sealed → report.

## Update 3 Oct ~04:20 UTC (after the C1 decision)
- Done:
  - 0b NO GO; no C4 was trained ($0).
  - Flip research (Fix3 optional).
  - A10 override committed (132cd2a): C1 is the shipped 4B, and the 2B teacher is 4B-E's ready labels.
  - JevBench public on C1: Intelligence 75.1 vs Jev 63.2 (+11.9, better); Score A 74.34 vs 68.80.
- Running: ejs-5 and LongBench-v2 kits (wh6gody1u, CPU only).
- Next:
  - ejs-5 and LongBench on C1 (owner OK given).
  - 2B A/B (GO) → 2B main ~$74 (GO) → 2B test → 2B/cascade readouts → H100 speed/cost (GO) → pre-register → ejs-5/LongBench/JevBench public on 2B/cascade.
  - OHS-3 once (GO) → JevBench sealed (owner) → report.

## Update 3 Oct ~14:30 UTC: new direction (4B only; the 2B is paused)
- Done:
  - ejs-5: C1 54.1 vs Jev 58.5 (loss), 4B-E 54.5.
  - B (WiSE-FT): no gain, keep C1.
  - A12 OHS-1/2: C1 vs Jev −1.2 / −0.6 (ties).
  - Deep research: 7 reports + gaps + spec + recipe v3.
  - A13 (Decision Index sample, report-only).
- Running: data-spec fix (wse7cvuaa: offline fixer + 3 licence checks → merge → verify) and Decision Index setup (ww5pg91ej).
- Next:
  1. Decision Index ~10K sample on C1 (L4, ~1 h).
  2. Sealed new-domains suite (≥5,000 items; hashed first; Jev read once).
  3. Golden dataset round 1 (~150K: 60% replay + C1 anchor, licensed public train splits, own 13 skill families, commit data from other repos).
  4. Round 1 training (~$30) → gate (sealed suite + dev).
  5. Round 2 (~$60) only if round 1 clearly wins.
  6. Ship the best → OHS-3 once → report.

## Update 3 Oct ~15:25 UTC
- Done:
  - Research completeness pass: 6 extra studies plus an addendum with 14 ADOPT changes.
  - Spec v3 READY (verifier).
  - A14 pre-registered (sealed suite build rules).
- Running:
  - Applying the addendum to spec/recipe v4, with verifiers.
  - Sealed new-domains suite build: isolated agents; the orchestrator sees counts only.
  - Decision Index setup: final checks.
- Next:
  1. Freeze the sealed suite and commit its sha256 (A15).
  2. Decision Index 10K sample on C1 (L4).
  3. Pre-register the C plan, then build the golden data for round 1.
- Added to the end of the flow (it was missing from the C recipe; the recipe only has the D9 latency guard vs C1):
  - **Speed + cost test of the final 4B vs Jev**: direct hosting on an H100, at a GO point, ~$5-8, after SHIP and before the report.
  - Then the final report and model card. JevBench sealed ($49) is the owner's decision.

## Final timeline (3 Oct 13:30 EDT; all times EDT). Correction: 4 Oct is SUNDAY, 5 Oct is MONDAY
- Sat 3 Oct:
  - ~3 pm: sealed test locked (A15) + C plan pre-registered.
  - 3 pm-1 am: data build.
  - ~7:30 pm: Decision Index result, then the fast-kernel test.
- Sun 4 Oct: QC + family-by-family L4 scoring all day (one free L4; GPU quota 1).
- Mon 5 Oct:
  - ~morning: golden dataset round 1 ready.
  - GO → round 1 training (~$30, ~7 h).
  - Evening/night: gate reads.
- Tue 6 Oct: round-1 verdict.
  - If round 2 runs (only on a clear win): data Wed 7, train Thu 8, verdict Fri 9.
- Finish:
  - Without round 2: Wed 7 Oct (sealed confirm + Jev read → OHS-3 once → speed/cost test → report).
  - With round 2: ~Sat 10-Mon 12 Oct.
- Projected JevBench v1.5.4 Score A (official board, IF submitted; owner OK needed): ~74.5 (range 71-77), vs Cygnet 73.70, Winnow 73.23, Jev 72.13. Intelligence ~69 (61-75) vs Jev 72.0.
- 3 Oct 2 pm EDT: owner keeps the DI run going (no pause). Training start ~Sun 11 pm EDT; round-1 result ~Mon noon; finish Wed 7 Oct without round 2, or ~Sat 10 Oct with round 2.

## Update 4 Oct 03:05 EDT (final plan, A17)
- **Phase A (round 1):**
  - Questions done Sun; L4 replay read done ~2:30 pm Sun.
  - Crowd scoring on a Modal H100 (~$15) → GO → training (~$30) Mon morning.
  - Ship-or-keep decision Tue.
- **Phase B in parallel (think mode):** free prep now; B1 H100 session (~$10-15, needs a GO); B2 concise training (~$10-15).
- Final tests once, Wed 7 Oct: OHS-3, the Jev read, Decision Index, speed/cost. Then the report.
- No looped-layer pilot. Round 2 only if round 1 clearly wins.

## ROADMAP v-final (4 Oct 13:40 EDT). Agent work is paused until the owner's weekly Claude reset (R = reset day)
- **Done:**
  - C1 tested on: OHS-1/2, ejs-5, JevBench public, Decision Index, security, Nimble suite (13), Nimble holdout, VitaminC.
  - Research: deep research, knowledge gap, ARC review, fast think mode.
  - FINAL_ARCHITECTURE written. Pre-registered: A14-A18.1.
  - Sealed suite frozen.
  - Round-1 inputs: replay (97,461 rows), G0 x14, packs/styles/public, F1/F2/F3/F6 generated, F3 G2 100%.
- **Phase A (R → R+2):**
  1. Finish the families and their checks.
  2. Mixer.
  3. Modal crowd scoring (~$15, GO).
  4. Decontamination.
  5. Smoke run.
  6. GO, then train (~$30).
  7. Gate.
- **Phase B (parallel, R → R+3):** think-mode prep → B1 H100 (~$10-15, GO) → B2 concise training (~$10-15).
- **Phase C (R+3 → R+4):**
  - Before/after re-test: Nimble suite + holdout, VitaminC (free L4).
  - Final tests once: OHS-3, Jev read, Decision Index.
  - H100 speed/cost.
  - Report.
  - JevBench submission (owner).
- Round 2 (~$60) runs only on a clear round-1 win (+3 days).
