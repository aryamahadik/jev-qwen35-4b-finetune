> **Ruling A62 (draft; 17 Oct 2026; orchestrator, Opus; T27 AGENT-CORE after its A52 (d) fix round; no gate, bar, cap or waiver rule is loosened; nothing is relabelled).**
>
> - **Facts (C2 side, counts only).**
>   - Round 1 of T27's full generation failed G11.
>   - Its one A49 (d) / A52 (d) generator-fix round (round 2) added a balanced wording picker and 19 ch_next + 6 yn_beyond new Haiku wordings (G-LEX 2/2). It regenerated the family, and every binding program gate passed: G11 max 1.50%, and A50 (a) G6 passed (four-build mean).
>   - The binding full-generation G5-H read (A49 c) then ran on 300 rows: readers A and B, file-access audit clean.
>     - 56 templates were quarantined, and 34 rows + 30 controls were queued.
>     - Sonnet flagged 21 rows + 1 control.
>     - Opus confirmed (A43 d) 14 ambiguous and 0 wrong gold. The ambiguous rate is 14/300 = 4.67%, against a bar of ≤ 1% (A42-D 3.1).
>     - `g5h.finalize` returned pass = false. After the template quarantine, rows fell from 2,400 to 1,287 (target 1,600).
>   - Opus's cause note: "bank-details-vs-card and install-vs-download paraphrases left ambiguous; generator equivalence unstated".
>
> - **(a) T27 moves to C3.**
>   - G5-H is a binding full-generation gate (A49 c), and T27 fails it on the ambiguous rate.
>   - A49 (d) gives one generator-fix round per family, and A52 (d) applies it. T27 spent that round on G11. No second round opens: A49 (d) says "one", A43 (e) closed iteration 2 and A44 (a) did not reopen T27, and A48 (a) lists no extra iteration for T27.
>   - This is the same outcome as T31 (A43 f: G5-H ambiguous fail on its final pass leaves C2) and T37b (A52 a).
>   - No other outcome is admissible:
>     - **No admission through the quarantine.** The template-quarantined 1,287-row subset is not admitted. Choosing a subset after a gate result has been seen, and re-reading G5-H on it, would be a new gate evaluation outside the fix loop. It would also be an exemption added after a result (A42-D 3.1 code-body clause, spirit; spec 6.4 step 6).
>     - **No relabel** (A42-D 3.4, 3.6).
>     - **No bar change.** The 1% bar stands.
>     - **No refill.** T27's share is not refilled (spec 5.3, A34 c).
>
> - **(b) Consequences for the C2 mix.**
>   - **Rows.** No T27 row from either round enters the C2 mix, replay, any complement-twin block (item 7) or any other family's pool. The row files stay on disk for C3 diagnosis only and are excluded by `mix_c2.py`'s family list.
>   - **Replay and totals.** Replay is recomputed as floor(1.5 × realised new rows) without T27 (spec 5.3). Every spec 5.2 cap and the A42-D 1.5 agent-tier cap (≤ 55%) are re-asserted on the realised numbers.
>   - **Dev sets.**
>     - T27's mixdev leaves the C2 mixdev, which is "150 per trained family" (spec 7.1). That changes the A42-D 9.3 R-mixdev term and the temperature fit.
>     - T27's mixdev is kept as a report-only read. Its G13 waiver status (A53/A55) is moot for C2.
>   - **Sealed split.** T27's frozen A1 sealed items stay in the OHS-AC manifest unchanged (sha fcf4b384…, A42-D 13.1; same treatment as T31). OHS-AC reports carry them per family, labelled "family not trained in C2". No sealed path is opened, and no manifest is edited.
>
> - **(c) Minimum to train (spec 5.3, 10.4; A49 d).**
>   - Agent core is now 5 of 6 (T26, T28, T29, T30, T33). That is exactly at the minimum, with no margin.
>   - The loss of any one of these five at a later binding gate (final all-block G13, mix-time balance under A49 c) or the cutoff means **stop and report, no training**.
>   - The training-GO request states: "agent core 5/6 (T27 → C3, A62)". It also states the realised program-family count, which must be ≥ 10.
>
> - **(d) C3 follow-up for T27 (recorded now; it binds when T27 is rebuilt).**
>   1. **Equivalence in G0 spec.** The G0 spec gets a recipient/action equivalence table. Each recipient class (for example bank details, card, account number) and each action class (for example install, download, fetch, run) is declared either:
>      - **equivalent:** same gold under every policy, and the generator treats the class as one, or
>      - **distinct:** a written distinguishing condition that the card states explicitly.
>
>      The table is hashed into the G0 spec before any row exists.
>   2. **Generator check.** A program check asserts on every row that no paraphrase moves a recipient or action across an equivalence-class boundary. It also asserts that the options, the state and the requested action never contain two members of one equivalent class with different golds. Solver B re-derives gold from the class table (G2 at 100%).
>   3. **Wording admission.**
>      - Every recipient/action synonym is a G-LEX 2/2 lexicon entry, tagged with its class.
>      - A blind Haiku exactness read must reach ≥ 0.9 per synonym (the A42-D 7.3 standard).
>      - The bank-details-vs-card and install-vs-download pairs are authored as distinct classes with explicit card wording, or merged. They are never left implicit.
>   4. **Quarantine.** The 56 quarantined templates and the 14 confirmed-ambiguous rows' templates are carried to C3 as a deny list. A C3 template that reuses one must pass a fresh G5-H.
>   5. **Gates.** C3 starts from fresh seed bases (the C2 T27 seed ranges are never reused). It runs the full gate kit, including G11, A50 (a) G6, and G5-H at pilot (100) and full generation (300), at unchanged bars.
>
> - **Not changed:** the A42-D block (sha cbdc29d9…), the OHS-AC freeze, every bar, cap and waiver rule, the money caps, and the cutoff (Wed 21 Oct 23:59 UTC).

Notes for the orchestrator:
- PREREG_FINAL.md ends at line 3088 with A59. There is no A60 or A61 text in it, so this draft does not cite them. If they exist somewhere else, check that nothing in them conflicts.
- File read: /Users/aryamahadik/Documents/jev/opendecide-data/lean/PREREG_FINAL.md (lines 2268-3088).
- Spec references come from /Users/aryamahadik/Documents/jev/opendecide-data/lean/teach1/C2_DATA_SPEC.md: lines 810-816 (minimum to train), 1265-1268 (stop rules) and 947 (mixdev).
- No ohs or sealed paths were opened.