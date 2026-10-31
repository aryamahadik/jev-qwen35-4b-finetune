# C2: final owner summary (Sun 18 Oct, US Eastern)

1. **Verdict: C2 does not ship, C1 stays.** The one OHS-4 look (4:46 PM) failed 3 of 6 ship rules: S1 rule/agent +1.93 points [+0.07, +3.82] (needs +5.0), S3 complement upper bound +2.08 (needs under +1.0), S4 Brier +0.0098 (needs +0.005 or less). General text, security and the dev pre-gate passed.
2. **Your override:** at 3:20 PM you waived pre-gate (b), the transfer rule, after seeing it fail (-4.83 [-8.59, -1.02] on 600 rows; all 18 candidates failed it). That let C2 take its look; it changed no ship rule, and C2 then failed the look.
3. **Against Jev 1.13 (one read, $0.17):** Jev is ahead. On rule/agent by 6.7 points over C2 and 8.6 over C1 (C2 closed 1.9 of the gap); on general text by 2.1 points over both. Jev also has the better Brier on general, rule/agent and security.
4. **Where C2 and C1 beat Jev:** consistency only. Complement violation 8.1% vs Jev 12.4%; option-order drift 6.1% (C1 3.8%) vs 13.4%. Not accuracy, not calibration.
5. **Training:** finished 6:24 AM, 3,673 steps on 59,340 rows, $13.14 free credit. The forgetting check passed (-1.80, -1.15, -0.50 points at 25/50/75%). Left out: T33/T12/T24, T27, RTW, T07, T32, T35/T37b/T46, T40-T45, MD, the DI blocks.
6. **Dev looked better than OHS-4:** +12.3 points on trained-family dev, only +1.9 on OHS-4 rule/agent. On one unseen family (T19) C2 lost 11.3 points, mostly by answering "cannot be determined" on 76 of 98 verdict questions (truth 26; C1 54).
7. **Calibration got worse:** ECE 13.2% vs C1 4.1%. Frozen temperatures: C1 yes/no 1.3, choice 1.25; C2 yes/no 0.8, choice 0.95.
8. **Money:** about $22.0 on Modal (training 13.14, grid 7.49, parity 0.52, L1 0.85; the H100 lines are $8.85 of the $15 cap) plus $0.17 for Jev; billing still lagging, final figure pending. Under the $40 cap, no card used.
9. **Not done, disclosed:** SPEED-3 (no speed/cost claim), symmetrisation, a second Jev read; S3 used R-based pairs only (383; no G-based pairs exist, 61 U pairs out of scope); the J pin string was fixed by a ruling before the look; PREREG is not committed in git.
10. **For C2.1:** track transfer and "cannot be determined" share per family at every checkpoint, fit T on held-out data, consider real data, anti-shortcut checks and early-warning monitors (RL is your call). By the written R14 rule the init is C1; your answer decides.
