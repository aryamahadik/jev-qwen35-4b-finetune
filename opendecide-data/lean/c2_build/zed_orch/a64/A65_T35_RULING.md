# A65 (T35) full text

> **Ruling A64 (17 Oct 2026; orchestrator, Opus; T35 final verdict under A45 (b); no bar is waived or relaxed). Number to be confirmed when appended after the last ruling in PREREG.**
> - **(a) T35 moves to C3 (A45 b).** Its final iteration is i4 (A48 a: "T29, T35: 4"). i4 fails G6 at the binding size set by A50 (a): the mean over four 6,000-row builds at seed bases 900000, 11,000,000, 12,000,000 and 13,000,000. The code is `families/T35/plugin.py`, sha256 6d0e9a6b…, the same as `_backup_a45b/plugin.py` (pass 1). The cell choice/c_card_without_question/lr has a mean excess of +2.27 pp against the +2 pp bar (mean accuracy 0.3144, bar 0.3116), and all four builds fail on their own (`pilot_i4/G6_A50_pass1plugin.json`). The pass-3 code (W5, not kept) also fails A50: choice/c_card_without_question/gbt at +2.15 pp (`pilot_i4/G6_A50.json`). The pass-2 and pass-3 changes passed on the pilot seeds only and failed on a fresh dev seed base (`pilot_i4/FIX_NOTES.md`). The 24,000-row diagnostic (A50 b) shows +5.72 pp. Earlier, i3 failed under A44 with a ContractError in S4 (`pilot_i3/PILOT_VERDICT.json`).
> - **(b) G10 is not the reason.** In the i4 pilot, double_negation_share = 0.0 is reported as "waived (A44 b)". A45 (a) and A48 (b) cover T35 by name ("whose only admitted double-negation shape was the A43 (f)-banned negated frame (T29, T35)"). Every other G10 check passes in the i4 pilot.
> - **(c) Nothing is pending.** The G3-H (162 items) and G5-H (100 rows) reads of pilot_i4 are not run: a failed binding gate decides the verdict whatever the reads say. A45 (b): "A family that still fails moves to C3; there is no further iteration." A50 (a): "No other seed base is used." There is no further fix pass, reseed or re-measurement before Mon 19 Oct 23:59 UTC.
> - **(d) Consequences.** T35 enters no C2 training block. It has no candidates on disk (`block_phase_dry.json`: "no candidates on disk"). The training-GO request reports T35 as moved to C3, with the A50 and 24,000-row numbers above, and states the agent-core count as A49 (d) requires. In C3, the i4 FIX_NOTES next step comes first: the no-line rows' near-miss and bait lines must take the gold-line profile mix ("$"-anchored lines are 44-46% of shown lines on no-line rows against 30% on gold lines).

## basis
Every record below was read only; nothing was edited or run.
1. PREREG A45 (b): "One final iteration for T29, T35 and T37b ... Bars unchanged. Verdicts are due Mon 19 Oct 23:59 UTC ... A family that still fails moves to C3; there is no further iteration."
2. A48 (a): "T29, T35: 4" iterations. A48 (b): the double-negation floor waiver applies to "(T29, T35) ... Every other G10 check binds."
3. A50 (a): "G6 binds at the spec size, for pilot verdicts and full generation alike ... four independent 6,000-row QC builds per family ... 900000 for pilot verdicts ... 11,000,000, 12,000,000 and 13,000,000 ... every cell mean ≤ chance + 2 pp ... No other seed base is used." A50 also lists "T35 +2.69 → +5.72".
4. A52 (a) is the precedent: T37b was moved to C3 before the deadline once its final iteration could not meet the bars.
5. No ruling from A53 to A63 mentions T35.
6. `/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/pilot_i4/G6_A50_pass1plugin.json`: plugin_file `_backup_a45b/plugin.py`, verdict fail, failing_cells ["choice/c_card_without_question/lr"], mean_excess_pp 2.27, per_build_G6_verdict_unaveraged all four fail.
7. `pilot_i4/G6_A50.json`: verdict fail, choice/c_card_without_question/gbt at 2.15 pp. This was the W5 code, measured at 23:13, before plugin.py was restored at 23:14.
8. shasum: plugin.py and `_backup_a45b/plugin.py` are both 6d0e9a6b…, so the active code is pass 1.
9. `pilot_i4/PILOT_REPORT.json`: summary.fail ["G10"] with the only failing check double_negation_share 0.0. Every other G10 check passes. G3-H and G5-H are "pending" (Haiku answers absent; the answers/ folders hold only a README). Program gates and pilot-size G6 pass.
10. `pilot_i4/FIX_NOTES.md`: passes 2 and 3 were "NOT FIXED". Their fixes passed on the pilot seeds but failed on dev base 700000 ("A fix that passes one seed base only is not a fix").
11. `pilot_i3/PILOT_VERDICT.json`: FAIL (ContractError in S4).
12. `/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/WAVE3_RESULT.json` T35-i4b: pass 2 did not fix the choice miss.
13. `zed_orch/block_phase_dry.json`: left_out T35, "no candidates on disk".
14. `/Users/aryamahadik/Documents/jev/HANDOFF.md`: line 14 says "Out: T35, T37b (C3)". Line 120 says "T35 has no PREREG ruling (HANDOFF only)". This ruling supplies that missing PREREG ruling.
No bar was waived or relaxed. The only waiver referred to is the double-negation floor that A45 (a) and A48 (b) had already confirmed, and it does not decide the verdict.
