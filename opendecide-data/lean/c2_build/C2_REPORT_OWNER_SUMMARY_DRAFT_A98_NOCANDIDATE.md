# C2: owner summary (Sun 18 Oct, US Eastern). DRAFT: the OHS-4 and Jev reads are still pending; your look decision is open

1. **Training:** finished 6:24 AM. 3,673 steps on 59,340 rows (23,736 new, 35,604 replay), $13.14 of free credit; the card was never used.
2. **Data:** 18 blocks went in (10 program families, agent core 4 of 6 under your A80 ruling). Left out: T33, T12, T24 (selection rules), T27 and RTW (QC), T07 (bad gold), T32 (no equiv twins), T35/T37b/T46 (moved to C3), T40-T45 (not ready), MD (source hits), all DI blocks.
3. **Forgetting check passed:** on old skills C2 was 1.80, 1.15 and 0.50 points below C1 at 25%, 50% and 75% (the stop line was 1.5 at both 25% and 50%).
4. **Grid:** 18 blends of C2 and C1 were read on one H100 job with C1 beside them (12:15 to 1:34 PM, $7.49). **No candidate was chosen: none was eligible.**
5. **Pre-gate:** all 18 fail the "transfer to unseen families" check (T19 + T21, 600 rows; needs +3.0 points with CI above 0); 13 fail only that. Final step: -4.83 [-8.59, -1.02]; best blend: -1.33 [-4.26, +1.62]; highest upper bound of any candidate +1.65. Trained families +12.31 [+10.47, +14.15] pass. General dev, pooled 8,143 rows over 9 splits: -0.48 [-1.14, +0.16]; D1 check (n 7,056, without tb_mixtral): -0.60 [-1.31, +0.15]. Both pass.
6. **OHS-4 (S1-S6):** under the rule C2 gets no look, so S1-S6 are not measured. Three independent checks confirmed the result (no candidate stands). The one look has not run: you choose between keeping the rule (it goes to C1 alone) and an override, since it cannot be undone.
7. **Jev comparison:** not yet. Jev is read once, after the C1 look; it will be C1 against Jev only.
8. **H100 path:** all 19 models were read the same way on the H100 ($7.49 of the $15 cap). The one miss in the reference check (max |dp| 0.10 on 1 of 8,143 rows) is the one you accepted; I changed the tools after the reads to allow that single look.
9. **Verdict:** C2 does not ship. It learned what it was taught (+12.3) but did not help general decisions and got worse on one unseen family (T19, -11.3). This follows the rules fixed before the data; no bar was changed.
10. **For C2.1:** judge transfer family by family from the start, because blending toward C1 cannot fix it. Init (R14): the written rule does not cover this case; C2's weights keep +12.3 on trained families, C1 avoids the T19 loss. Your call.
