# Draft amendment A10: owner override naming C1 as the shipped 4B (A8′ H.2)

DRAFT ONLY. Commit it (append the quoted block to PREREG_FINAL.md) only after the owner says "B: ship C1" in chat, and
before any OHS-3 call. Fill the date and time at commit.

---

> **Amendment A10 (3 Oct 2026, 03:10 UTC; owner decision in chat; before any OHS-3 call): owner override naming C1 =
> `q35_4b_main500k` (adapter sha256 `507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078`) as the
> shipped 4B, under A8′ H.2.**
>
> **A. The failed conditions** (to be repeated on the model card and in the OHS-3 report):
> - **Ship look 1** (1 Oct, `logs/gate4b/look_ship1.txt`): DO NOT SHIP (FINAL). One constraint failed: (e) the
>   equivalence flip rate is 8.86% vs REF 5.68% (limit REF + 2 pp = 7.68%; 64 of 722 pairs vs 41).
> - **A8′ step 0b** (3 Oct 02:10 UTC, `logs/gate4b_fix2/conds/probe_go.json` on od-l4): NO GO. On the F7 held-out
>   probe, C1 flips 87 of 252 pairs (34.52%) and 4B-E flips 86 (34.13%). The difference is +0.40 pp [−5.86, +6.75];
>   the rule needed at least +3 pp with a lower bound above 0. Per A8′ D, no C4 was trained and $0 was spent.
> - C1 is never described as having passed the ship rule.
>
> **B. What passed in look 1** (C1 vs fresh 4B-E): primary +2.47 pp [+1.31, +3.70] (83.99 vs 81.52); (a) +1.19 pp;
> (a2) dev-select +1.83 / dev-confirm +0.54; (b) yes/no +1.40; (c) choice +0.94; (d) Brier 0.1099 vs 0.1184; (f)
> permutation flips 2.43% vs 3.78%; (g) jagged ASR 0.0% vs 0.6%, OPI ASR 1.3% vs 1.8%. Parity 100%.
>
> **C. Why the owner overrides** (diagnostics on dev, disclosed as dev-based):
> - The (e) failure sits in one frame: devp_card/hate "the tweet contains only non-hateful content" with the outer
>   "Should the statement that … be rejected?". C1 flips 29 of 30 pairs there and 4B-E 0 of 30. 4B-E's consistency in
>   that frame comes from near-constant answers (affirmative p_yes 0.13 for gold 0 vs 0.21 for gold 1).
> - On the other 692 pairs C1 flips 35 and 4B-E 41. C1 is more accurate on both rows of the 722 pairs: affirmative
>   84.90 vs 83.93, double negation 84.35 vs 82.96.
> - On held-out nested negation (the F7 probe) C1 equals 4B-E (34.5% vs 34.1%).
> - OHS-3 has no double-negation twins. On every OHS-3 consistency axis C1 is better on dev: complement violations
>   3.30% vs 4.63%, option-order flips 2.43% vs 3.78%.
>
> **D. Consequences.**
> - C1 is **not** eligible as the 2B teacher (A8′ H.2). The 2B keeps 4B-E as its teacher and uses the ready 4B-E
>   2-view label file `train_2b_golden_kd_2view.jsonl`; there is no relabel.
> - The PREREG_OHS3 model amendment (at the OHS-3 step) names C1 with the sha256 above and the A5 readout for C1
>   from `prep89/READOUT_DEV.md` (T 1.00 / 1.00; choice rows read twice, given order + exact reversal; yes/no read once).
> - **OHS-3 overlap disclosure:** the owner's counts-only check found 7 golden_train units (gd_redocred 6,
>   gd_helpsteer3_pref 1) sharing 12-grams with OHS-3. C1 (and 4B-E, if its data held them) trained on them. OHS-3 is
>   reported with and without the overlapping items, identified by program, counts only (owner decision, recorded).
> - No further 4B top-up, merge or ensemble without a new amendment committed before that candidate exists.
>
> **E.** Nothing in this amendment opened OHS-3 data or predictions.
