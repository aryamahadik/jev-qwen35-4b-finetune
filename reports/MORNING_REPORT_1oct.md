# Morning report, 1 Oct 2026 (written overnight; updated at each event)

## Decisions needed from you (before ~1 pm EDT, when the 4B finishes)
1. **Approve amendment A7 (the 4B gate fix). Recommended: option (a).**
   - Problem: as frozen, the gate can never give a FINAL verdict.
     - 4B-E's stored reference file is mislabelled as a 2B, so the tool stops.
     - Even with the label fixed, the stored reference fails the max-difference bar: 0.099 vs a limit of 0.05, on 3 of
       8,143 rows. The cause is bf16 rounding in an old reading method.
   - Fix (a): use the clean 30 Sep reference read (q35_4b_pxE_parity), which was made exactly like the gate's own reads.
     The bar stays the same, and the rule is decided before any new-4B result exists, so it is fair.
   - Draft: lean/prereg_drafts/AMENDMENT_A7_refparity.md (patch and tests ready: 31 passed, 1 skipped).
   - Also commit A0, which adopts PREREG_FINAL.md as written (it is still marked DRAFT).
2. Later (not urgent): amendments A1-A5 (the 2B pilot rule, PRISM-X override, 2-view teacher, the 121 bad date rows,
   readout settings). They are drafted in lean/prereg_drafts/AMENDMENTS_1oct.md and must be committed before the 2B
   pilot (A1-A4) and before OHS-3 (A5).

## What was prepared overnight (free)
- 4B gate: runbook and L4 script (gate/), about 3.5 L4-hours. Full simulation: 27/27 checks pass.
- OHS-3 scorer matching the pre-registration: score_ohs3.py, 21 tests pass.
- Direct-hosting speed test script (hosting/), about $1-2.5 when you say GO.
- 2B hard data wave 1b: F6 done, F1 in review (see the yn2b status files).

## 4B relay log
See lean/logs/main4b_relays.md. Every switch is verified: exact step, all checks, LR formula.

### Relay updates (overnight)
- 02:11 UTC: segment 2 → 3 on the same account (arya-mahadik-ai). Resumed at step 11,290; all checks and the LR
  formula match.
- 06:47 UTC: segment 3 → 4, transferred to aryamhd. Step 17,428; the checkpoint was verified both ways, all checks
  match, and the LR formula matches exactly.
- Next: about 13:40 UTC, segment 4 → 5 to a fresh account (atmosphor). The 4B should finish about 17:00 UTC (1 pm EDT).
- Budget tracker at 06:47 UTC: essentials leave a $61 reserve, or $30 with both optional steps.

## 2B hard data (yn2b), goal step 4: built (details in lean/yn2b/WAVE1B_STATUS.md)
- **18,359 training rows** in 6 families:
  - F1 rule chains 4,257;
  - F2 tool-call guardrails 5,202;
  - F3 state tracking 3,590;
  - F4 polarity ladder 1,500;
  - F5 lead scoring 2,160;
  - F6 literal definitions 1,650.
- **Dev sets:** iid 958, holdout 986, unseen-template devx 500.
- **Checks:**
  - a second independent program agrees on 100% of labels;
  - blind solves 98-130 per 100-130 rows;
  - decontamination clean (OHS-3 0 hits, counts only; 0 dev overlaps);
  - 1,231 tests pass.
- **2B pilot files built from the 2-view teacher:**
  - arm A (control) 62,995 rows / 3,820 steps;
  - arm B (+yn2b) 72,125 / 4,358;
  - arm C (B + teacher gate) 72,125 / 4,358.
- **Pilot on one L4:** about 45 h for 3 arms + reads (verdict about 4 Oct morning), or about 3 Oct with 2 L4 VMs.

### Decisions for you (2B pilot; can wait until after the 4B gate)
1. **F3 small balance miss.** Accept it (recommended; it misses by 3 rows), or drop F3.
2. **G2 pass rule.** It is too noisy as written (it fails harmless data about 50% of the time). Recommended: point
   ≥ −1.75.
3. **Teacher rules §6 (c)/(d).** Recommended: keep (d) and drop (c).
4. **12 gen_tables rows.** Keep them (default).
5. **If the L4 can't fit the 2B (24 GB vs a 25.4 GB peak):** move the pilot arms to the H100 (about $28-29), or another
   option.
6. **A second L4 VM** to halve the pilot time.

### yn2b final checks (about 10:45 UTC)
- A fresh reviewer blind-solved 250 unseen-template (devx) rows: **250/250 correct**, 50/50 in every family.
- F4 and F6 edits re-checked by independent decide2: 100% agreement on 1,500+300 and 1,650+150 rows. F2 devx decide2
  was fixed: 100/100.
- Merge tool fixed. If yn2b passes the pilot, the 2B main file will be 520,018 rows, 450,099 KD targets, 31,551 steps
  (dry run). The fallback file (no yn2b) is 501,659 rows.
- 2B pilot prep is in a separate code copy (/Users/aryamahadik/Documents/jev-2b, branch 2b/yn2b-ab): arm configs A/B/C
  checked key by key (36/36), and the L4 launcher dry-run passes. It runs only after your GO.

### 13:16 UTC incident and recovery
- The laptop lost internet at 9:16 am EDT, and Modal cancelled segment 4 (aryamhd). Its emergency save worked: the
  checkpoint at step 25,682 was verified complete, so only about 40 steps were lost.
- At 9:39 am EDT the final segment was moved to atmosphor with a new launcher that keeps running even if the laptop
  goes offline. It runs to the end: about 4,775 steps, about 3.6 h, about $15. ETA about 1:20 pm EDT.
