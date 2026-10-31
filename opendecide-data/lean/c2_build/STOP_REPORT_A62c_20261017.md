# A62 (c) STOP REPORT — C2 (17 Oct 2026, ~09:45 UTC; orchestrator, Opus)

**What triggered it.** The early OHS-AC check allowed by A64 (f) (drops only), run by the orchestrator with the A64 tools
(g13_c2.py 49f4c795…, a57_hashcheck_ac.py bf58d3f1…; union record freeze_subset_of_final, every export verified; logged in
zed_orch/a64/A64_TOOLS.md): `g13_c2.py candidates --ohsac-only` and `carry --ohsac-only`. Every result: manifest_verified
true, final true, complete true. Two independent implementations agree (C2-side hash compare `ohsac_hash` and the sealed-side
rows checker `ohsac_rows`). Logs: c2_build/logs/acquick_candidates_20261017.log, acquick_carry_20261017.log; records
logs/decontam_counts/acquick_c2_*.json. This early check is not the binding final-mix G13, but the binding run uses the
same targets and methods.

**Measured drops (rows; whole units drop).**

| Block | Rows | Rows dropped | Rows left |
|---|---|---|---|
| F11 | 5,415 | 5,079 | 336 |
| F4 | 5,400 | 4,390 | 1,010 |
| F5 | 5,272 | 5,272 | 0 |
| F6 | 5,375 | 5,375 | 0 |
| GB | 5,537 | 4,590 | 947 |
| GW | 5,443 | 4,427 | 1,016 |
| I10 | 152 | 123 | 29 |
| MD | 10,491 | 4,132 | 6,359 |
| RTW | 0 | 0 | 0 |
| SB5 | 1,039 | 0 | 1,039 |
| T01 | 2,391 | 2,391 | 0 |
| T06 | 1,251 | 1,251 | 0 |
| T07 | 1,179 | 1,179 | 0 |
| T12 | 1,154 | 1,154 | 0 |
| T15 | 1,328 | 1,328 | 0 |
| T23 | 1,057 | 1,057 | 0 |
| T24 | 847 | 847 | 0 |
| T25 | 894 | 894 | 0 |
| T26 (agent core) | 1,857 | 1,857 | 0 |
| T27 | 1,287 | 1,287 | 0 |
| T28 (agent core) | 3,151 | 3,151 | 0 |
| T29 (agent core) | 2,667 | 2,667 | 0 |
| T30 (agent core) | 1,977 | 1,977 | 0 |
| T31 | 1,475 | 1,475 | 0 |
| T32 | 1,057 | 1,057 | 0 |
| T33 (agent core) | 3,213 | 3,213 | 0 |

**Consequence under the adopted rules.** Agent core left: 0 of 6 (A62 c minimum 5).
Program families left with rows: 0 of 15 (minimum 10). A62 (c) / A64 (f): stop and
report; no training. Replay (C1 rows) has not been checked yet.

**Where the hits come from (methods, no item text).** For the 15 program families every unit hits sentence/n-gram methods
(exact_sentence, ngram10/12, exact_seg, tulu8) — the sealed A1 split was built by the same family generators (A42-D 13.1),
so it repeats their rule text, wordings and options. GB, GW, MD, I10 and the F-blocks hit almost only on the `keyword` method
(956 hashes: source identifiers plus every held-out registry/tool/carrier name of ≥ 4 characters; any single token matches).
SB5: 0 hits.

**A64 (b), quoted as A64 requires:**

**(b) The frame question: considered, not adopted.**
>   - **The conflict.**
>     - A42-D 13.1 builds each family's sealed split with that family's own generator (its HELD_OUT_SAMPLERS). Only the listed values are held out, so the split repeats the generator's rule text, wordings, option strings and definitions.
>     - A42-D 3.1 (G-TPL against OHS-AC templates), 3.5 (G13 against OHS-AC, 0 hits after drops) and spec 8.4 ("On any hit: the C2 unit or template is dropped") then drop every training text that repeats that frame.
>   - **A draft reading was rejected.** The draft said that G-TPL and G13 against OHS-AC do not count a family's frozen frame where that frame is shared with the family's own split. It is rejected for three reasons.
>     1. **No pre-registered text says these checks should skip shared frame text.** The texts show only that the split shares the generator's grammar:
>        - A42-D 13.1;
>        - FINAL_PLAN §2 "Ranked list" item 3 (FINAL_PLAN.md:139, wave 1 only). Its stated mitigation is that the sealed split changes the surface ("the sealed split changes registry style"). That is an argument for strictness.
>        - 13.1's A1 sentence says what G-TPL and the sealed-side child enforce for A1 held-out variants. It removes nothing else from their scope, which A42-D 3.1 and 3.5 and spec 8.4 define.
>     2. **A53 already set the limit.** A53 gave a program-literal waiver for the dev targets only and stated: "Sealed, public and every other target are unchanged."
>     3. **No post-result exemptions.** A42-D 3.1 says "No exemption is added after a gate result has been seen" (written for code-body exemptions), and A62 (a) refuses to re-scope a quarantined subset after a result. Both state the house rule. The draft's frame classes were exactly the classes that had hit.
>   - **So G-TPL and G13 against OHS-AC apply as written:** to all model-visible text, with every method.
>     - The literal rule can still be met: a family's training-side text may differ from its sealed frame ((e)). That is also FINAL_PLAN's own mitigation.
>   - **Only the owner can change a pre-registered gate after a result.** The orchestrator does not ask for that change.
>     - The training-GO request, or an A62 (c) stop report if that comes first, quotes this paragraph and the measured per-family drop counts. It is neutral and makes no recommendation.
>     - No family is reopened past the A57 (g) deadline unless the owner says so in words.
>
> 
**Neutral statement of where this leaves C2 (no recommendation, per A64 b/i).** Under the rules as adopted, C2 does not
train. Only the owner can change a pre-registered gate after a result, in words. The data built so far stays on disk
unchanged (drops are records only) and is available to C3. The C1 serving work (no training) is unaffected.
