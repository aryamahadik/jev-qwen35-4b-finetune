# A64 draft, revision 2 (unreviewed)

## ruling_text
> **Ruling A64 (17 Oct 2026, ~07:30 UTC; orchestrator, Opus; OHS-AC against each family's own sealed split: the T43/T45 A57 step-6 stops, keyword hits, AC tool completeness, the export union; no bar loosened; no waiver; nothing relabelled; drops only.)**
>
> **Written after these results were seen:**
> - the A57 step-2 program-text records: T43 (logs/a57_T43_step2_hashcheck.json, 03:34 UTC, 29 of 34 hit), T42 (logs/a57_T42_step2_hashcheck_ac.json, 03:38 UTC, 12 of 15 hit, keyword 7) and T44 (zed_orch/a57/T44_step2_hashcheck.json, 03:40 UTC);
> - the T43 and T45 step-6 records (05:49 UTC);
> - the T44 driver's program-wording hits (5 of 8);
> - the orchestrator's unlogged scratch scripts (file times: kwfind.py 03:39, kwruns.py 06:21, a1_ac.py 06:29, a1_kw.py 06:30, a1_kwfull.py 06:35 UTC).
>
> For that reason this ruling adopts no reading that admits more text than the literal rules allow.
>
> - **(a) Scope of the step-6 records.**
>   - A57 (b) says A57 "does not cover program text". T43 and T45 have no Haiku pool and no task file (logs/a57_T43_step2_manifest.json: 0 files). So their A57 steps 2-7 are empty.
>   - `logs/a57/T43_step6.json` (sha256 2ec98857…) and `logs/a57/T45_step6_program_text.json` (sha256 b80b41ad…) are therefore not A57 admission records. They are G13 seed-stage records for program templates against the final OHS-AC export: A42-D 3.5 runs the seed stage first, and spec 6.4 step 4 says "a hit quarantines that template only".
>   - The same applies to the T42, T43 and T44 step-2 program-text records and to the T44 wording hits.
>   - The tools that produced these records are defective ((g)). So a record can count as a hit but never as a pass.
>     - Every unit listed as hit is quarantined now (drops only).
>     - The seed stage is rerun with the fixed tools before any row of that family is written. The rerun can only add quarantines.
>   - **Erratum to A63 (e).** "Dropped at step 6 / row G13" now reads "dropped at G13: at the seed stage for program templates, at candidates and the final mix for rows". The drop itself is unchanged.
>
> - **(b) The frame question: considered, not adopted.**
>   - **The conflict.**
>     - A42-D 13.1 builds each family's sealed split with that family's own generator (its HELD_OUT_SAMPLERS). Only the listed values are held out, so the split repeats the generator's rule text, wordings, option strings and definitions.
>     - A42-D 3.1 (G-TPL against OHS-AC templates), 3.5 (G13 against OHS-AC, 0 hits after drops) and spec 8.4 ("On any hit: the C2 unit or template is dropped") then drop every training text that repeats that frame.
>   - **A draft reading was rejected.** The draft said G-TPL and G13 against OHS-AC do not count a family's frozen frame where it is shared with that family's own split. It is rejected for three reasons.
>     1. **No pre-registered text says these checks should not count shared frame text.** The texts show only that the split shares the generator's grammar:
>        - A42-D 13.1;
>        - FINAL_PLAN §2 "Ranked list" item 3 (FINAL_PLAN.md:139, wave 1 only). Its stated mitigation is that the sealed split changes the surface ("the sealed split changes registry style"). That is an argument for strictness.
>        - The A1 sentence of 13.1 says what G-TPL and the sealed-side child enforce for A1 held-out variants. It removes nothing else from their scope. A42-D 3.1 and 3.5 and spec 8.4 define that scope.
>     2. **A53 already set the limit.** A53 gave a program-literal waiver for the dev targets only and stated: "Sealed, public and every other target are unchanged."
>     3. **No post-result exemptions.** A42-D 3.1 says "No exemption is added after a gate result has been seen" (written for code-body exemptions), and A62 (a) refuses to re-scope a quarantined subset after a result. Both state the house rule. The draft's frame classes were exactly the classes that had hit.
>   - **So G-TPL and G13 against OHS-AC apply as written:** to all model-visible text, with every method.
>     - The literal rule can still be met: a family's training-side text may differ from its sealed frame ((e)). That is also FINAL_PLAN's own mitigation.
>   - **Only the owner can change a pre-registered gate after a result.** The orchestrator does not ask for that change.
>     - The training-GO request, or an A62 (c) stop report if that comes first, quotes this paragraph and the measured per-family drop counts. It is neutral and makes no recommendation.
>     - No family is reopened past the A57 (g) deadline unless the owner says so in words.
>
> - **(c) One rule for every text.**
>   - **Coverage.** The same tools, at the same bars, compare OHS-AC with every model-visible training-side text of every family. Row origin changes nothing.
>     - Texts: candidate, carry, top-up, replay, own-dev and pilot rows; every template and program literal; every Haiku pool item and task file.
>     - Families: the 17 A1 families, T40-T45, T46, SB5 and every replay source.
>   - **A1 has no binding OHS-AC record.** Every c2_cand log predates the 02:25 UTC freeze, and g13_c2.py has no OHS-AC path.
>     - The A42-D 3.5 candidates stage against OHS-AC runs first, once the fixed tools pass their self-tests and the (h) record exists. It covers every A1 candidate and replay unit.
>     - A55 (b) holds: G13 drops open no fix round. Top-ups (A55 L2) face the same check.
>     - If the result takes the agent core below 5 of 6 (A62 c), or the program families below 10, the orchestrator stops and reports.
>   - **The scratch scripts were seen but are not logged results.** They decide nothing, and no number from them is cited.
>     - They are copied unchanged to `c2_build/zed_orch/a64/scratch_record/`, with sha256: kwfind.py 1d2de1c1…, kwruns.py d991d1f7…, a1_ac.py bc8d253d…, a1_kw.py 6be3d7f1…, a1_kwfull.py 02fd2eb4….
>     - Some of them printed which C2 token runs match keyword hashes, and the orchestrator records that it saw that output.
>     - No fix author receives that output, and no removal, wording or selection may use it.
>     - A63's token names came from a lookup that was not logged. A63's outcome was a removal, so it stands.
>
> - **(d) Keyword hits** (A63 (a), applied to program text).
>   - Keyword runs on every uncut model-visible field. A hit drops the row's unit or quarantines the template, whatever entry it matched.
>   - A fix only removes content and never adds words. For a template that hit keyword:
>     1. A fixed C2-side program matches the template against the union of every family's HELD_OUT_* constants, in identifier and rendered forms. It uses C2 code only, with no sealed lookup.
>        - If a held-out literal is found, every sentence or list item that contains it is deleted, with no replacement.
>        - If the meaning of a head, option, register, kind or rule needs that sentence, the whole head, option, register, kind or rule is removed.
>     2. Otherwise the whole template is removed from training-side rendering. Nothing replaces its meaning in any form: no synonym and no paraphrase (A63 a).
>   - No program looks up which token of a hit unit matches a keyword hash. No replacement text is ever tried against any export.
>   - A held-out or sealed-mode-only literal that hit needs no further removal if (f)(i) and (f)(ii) show that 0 training-side rows and templates render it. That drop is already in place; it is not an exemption.
>
> - **(e) Shared frame without a keyword hit** (exact, sentence, n-gram, tulu8, minhash or G-TPL hits).
>   - **Quarantine.** The template is quarantined.
>     - A family whose quarantines leave it unable to produce the rows a gate needs has failed that gate evaluation.
>     - It may use a remaining A42-D 3.6 fix iteration. The count comes from the family's build record and is logged before the iteration opens. With none left, the family moves to C3.
>   - **The fix: a training-side text overlay** (generator and templates only), selected for samplers outside HELD_OUT_SAMPLERS.
>     - A C2-side test proves that the sealed-mode text constants are byte-identical to the frozen file shas (T43 texts.py a9ce9bce…).
>     - G0-lite is updated and sha-logged before the first post-fix row.
>     - **Who writes the new text.** The author gets the quarantined template ids and the C2 code only. The author never gets an export, a checker output beyond ids, or scratch output.
>     - **What the new text must meet:**
>       - it shares no 8-gram and no sentence of 5 or more words with any sealed-mode-reachable text of any family; this is checked on the C2 side, before any sealed compare;
>       - it restores no content that (d) removed.
>   - **One compare per iteration.** Each iteration gets one G13 seed compare against OHS-AC with the fixed tools. A hit is quarantined and is not reworded in that iteration.
>   - **Gates rerun.** Every A42-D 3 gate and probe, 3.3, 3.4, G5-H, G-LEX and G3-H reruns on fresh post-fix rows at unchanged bars.
>     - Iteration-2 results are due Mon 19 Oct 23:59 UTC.
>     - Otherwise the family moves to C3. Its frozen items stay in the suite, reported as "family not trained in C2" (A62 b).
>   - **Why this is not the probe that A57 (e)6 bans.** The frame being avoided is the family's own code, which the C2 side already knows. The new text is made disjoint from it without the export, and the export is consulted once per iteration, inside 3.6's limit of 2 iterations.
>
> - **(f) Held-out check.**
>   - Source: 13.1 ("no training-side or dev row uses a held-out value"), applied across families as A63 (b) did. Binding.
>   - **(i) Ids.** Every row's sampler, register, operator, template, fault, domain, pack, layout and wording id lies outside every family's held-out sets. Required: 0 rows inside.
>   - **(ii) Text.** Every training-side row and template is compared with the union of all families' HELD_OUT_* literals:
>     - by whole-token, case-insensitive match of their identifier and rendered forms, with snake, camel and kebab forms both split and joined;
>     - plus 8-grams and sentences of 5 or more words for multi-word literals.
>     - Any hit drops the row or removes the template. Over-matching of common words is accepted (drops only).
>   - The 1,200-draw tests do not stand in for this check.
>
> - **(g) Tools.** All are program fixes, sha-logged in `c2_build/zed_orch/a64/A64_TOOLS.md` before first use.
>   1. **Computed completeness.** `complete` in a57_hashcheck_ac.py and a57_hashcmp.py is true only if all of these hold; otherwise it is false (exit 3):
>      - the MANIFEST verifies;
>      - (2) passes;
>      - the (h) record exists;
>      - every required method ran on every unit.
>   2. **Finality from the addendum.** Finality is decided by the addendum shas, read from PREREG_FINAL.md: MANIFEST fadec66f…, suite c2dfefa6…, post-freeze manifest 305356b6… and source manifest fcf4b384…. The MANIFEST stage string is recorded but decides nothing.
>   3. **One way to build units.** Each text is checked both uncut and as template pieces, so that exact_raw and full_text_* always run. rows_src is passed, so that structure_g13, skeleton_state, skeleton_instructions and skeleton_line also run.
>   4. **An OHS-AC path in g13_c2.py** for the seed, candidates and final-mix stages. It runs the hash compare, `g13_ohsac_check --rows` and `gtpl_check_ac --templates --min-shared 1 --parts all`. Every method binds. A53 and A31 (b) never apply to it.
>   5. The (d) held-out-literal remover.
>   6. The (f) checker.
>   7. The (e) byte-identity test.
>   - **Self-tests:** a known hit; a non-final export (complete false); a missing (h) record (complete false); a template unit (exact_raw still runs); a held-out-token fixture.
>   - **Earlier results.** Every earlier result marked complete true by a57_hashcheck_ac.py or a57_hashcmp.py is void as a pass, and its hits stand as drops or quarantines. Every admission reruns with the fixed tools. This covers:
>     - T40 task files (r0 and r1);
>     - T40, T41, T42 and T44 step 4, including the T44 stage-4 seed run now in progress;
>     - T42, T43 and T44 step 2;
>     - T43 and T45 step 6.
>   - **Sealed side.** The only new sealed-side work is the (h) record. A fresh sealed agent does it, with an access audit of 0 and counts only.
>
> - **(h) Exports and the union.**
>   - **Three export states have been used:**
>     - the freeze export 27808b0c…;
>     - a post_freeze_partial export a2c95c19… (suite 7ad1747e…), used by the T40 r0 task-file check and the T42, T43 and T44 step-2 records;
>     - the final export fadec66f….
>   - **A57 step 2 ("against the freeze-time export") was never met.**
>     - Every task file used for authoring is rechecked, by its sha, against the union.
>     - A file with any hit discards every answer authored from it, unused (counted).
>     - A63's union rerun is still open; T40 r1 was checked against the final export only.
>   - **Which checks need the union record.** `g13_ohsac_check` and `gtpl_check_ac` verify the 14,407-item final suite, which contains the 12,680 frozen items (fcf4b384… verified). The C2-side hash compare has only the export, so for it the union binds. A fresh sealed agent works in this order:
>     1. It looks for a byte copy whose MANIFEST sha256 is 27808b0c…, on od-cpu1, in backups and in the sealed folders. If one is found, it records |freeze \ final| per kind, counts only. If any count is above 0, a union export is built and used.
>     2. If there is no copy, it re-derives the freeze export from the frozen items with the freeze-time export code and keyword sources. The result counts as the freeze export only if its MANIFEST sha reproduces 27808b0c….
>     3. If neither works, the loss is recorded as a deviation in a PREREG addendum, no hash-compare result admits anything, and the orchestrator stops and reports (as A62 c).
>   - FORMAT.md's line "contains every hash of the freeze-time export" is the sealed side's claim, not this record.
>
> - **(i) T43 and T45 now.**
>   - **T43.**
>     - The six rules, 17 of the 18 wordings, opt:B and opt:C are quarantined. Every row renders one of the 6 rules, so as built T43 has 0 rows.
>     - The keyword hits (all 6 rules, loc_line:0-2, loc_line_n:0-2 and opt:C) follow (d). Unless held-out literals explain them, each one is removed with no replacement. No head would then have a rule, and T43 moves to C3.
>     - Any part that survives goes to (e), if a 3.6 iteration remains. A56 (b) used one; the driver logs the count.
>     - The 500 sealed calls hit equal T43's whole split. This adds nothing beyond the drops.
>     - The earlier draft's multi-token keyword attributions are withdrawn.
>   - **T45.** 108 of 395 training units are quarantined.
>     - Keyword hits:
>       - layout.report.0 and layout.report.all: the report register is removed (8 training registers become 7).
>       - planned.db, planned.http and planned.tests, plus texts.py #42, #43 and #45 (the same strings): those 3 planned-command kinds are removed (5 become 2), unless (d)1 finds a held-out literal, in which case only its sentences are deleted.
>       - scenarios.py #0, #11, #82, #90, #100, #109, #133 and #328 go through (d)1 and (f). If any training render uses them, they are removed from it and those rows drop.
>     - All other hits are quarantined and go to (e) if an iteration remains: the 32 rules blocks and the 2 rules templates, the 6 wordings, the card lines, the label definitions, the group phrases and the texts.py literals. Frame text and instance text are treated alike.
>     - The 12 memo and journal layout units have 0 hits and are sealed-mode only. (f) verifies this.
>     - No pool freeze applies.
>     - Nothing is refilled by hand. A55 L2 top-ups meet the same checks.
>
> - **(j) Disclosure.** Every OHS-AC report states the following, for blocks A1, A2 and B:
>   - each split comes from the family's own generator (sealed mode): new instances plus the listed held-out values;
>   - for each family trained in C2, whether its training text was the frozen frame or an (e) overlay disjoint from the sealed frame. A1 families' frames were trained by C1 before the A1 split was built (13.1);
>   - that G-TPL and G13 against OHS-AC counted all text, with no frame or own-split excusal (A64 b);
>   - that A64 was written after the records named in its header had been seen;
>   - per family, as counts and classes: rows dropped against OHS-AC, templates quarantined, content removed by (d) (register, kind, head or option), iterations used, and whether the family moved to C3;
>   - that Jev and the baselines see each split cold, with the 13.6 definitions.

## decision
Do not admit any text under a frame or own-split excusal. G-TPL and G13 against OHS-AC apply literally: every method, uncut text, every family, every row origin. The earlier draft's (b)/(d)1 frame excusal and its K_core, provenance-audit, kw_span and M1 parts are withdrawn: no pre-registered text says these checks should not count shared frame text, A53 kept sealed targets unchanged, and the frame classes were picked after the hits.

What happens now:
- All recorded hits stand as quarantines or drops.
- Keyword hits are fixed only by removing content, never by adding words. The hit content is first matched against our own HELD_OUT_* constants. If that does not explain it, the whole template is removed. No token lookup against the sealed hashes.
- Shared frame without a keyword hit can be fixed only by a training-side overlay under A42-D 3.6, while a fix iteration remains:
  - the sealed-mode text stays byte-identical;
  - the new text is disjoint from the sealed frame, checked on the C2 side first;
  - one OHS-AC compare per iteration;
  - full gate rerun by Mon 19 Oct 23:59 UTC; otherwise the family moves to C3.
- The held-out check gets a token-level, cross-family text match.
- The A1 candidates stage against OHS-AC (never run) goes first with the fixed tools. A62 (c) applies to its result.
- Every earlier complete=true result from a57_hashcheck_ac.py or a57_hashcmp.py is void as a pass; its hits stand.
- No OHS-AC hash-compare result admits anything until a sealed-side union record exists for the freeze export 27808b0c.
- The owner can change a gate after a result; the orchestrator does not ask. The training-GO request (or an A62 (c) stop report) quotes A64 (b) neutrally, with the measured counts.
- No pilot-spend GO is created. Pilots stay as A42-D 4.1 sets them.

## per_family
T43:
- Quarantined now: all 6 rules, 17 of 18 wordings, opt:B and opt:C. Every row renders a rule, so T43 has 0 rows as built.
- Keyword hits (6 rules, loc_line:0-2, loc_line_n:0-2, opt:C): removal only. Unless our own HELD_OUT_* literals explain them, each is removed, no head keeps a rule, and T43 moves to C3.
- Anything that survives may use its last 3.6 iteration, if one remains (A56 (b) used one; the driver logs the count). Its 500 B-block items stay, reported as "family not trained in C2".

T45: 108 of 395 training units quarantined.
- The report register is removed (8 training registers become 7).
- planned db, http and tests (texts.py #42/#43/#45, the same strings) are removed (5 kinds become 2), unless a held-out literal explains the hit.
- The 8 scenarios.py keyword literals go through the held-out match and the (f) check. Any training render of them is removed.
- All rules blocks, wordings, card lines, label definitions, group phrases and the hit texts.py literals are quarantined. They can come back only through a training-side overlay under a remaining 3.6 iteration, with a full gate rerun by Mon 19 23:59 UTC. Otherwise C3.
- The memo/journal layouts (0 hits) are sealed-mode only; (f) verifies.
- No pool freeze.

T40:
- Task files: the r0 check ran against the partial export a2c95c19, and r1 (0 hits) against the final export only. Both are void as passes. Rerun against the union (A63).
- Step-4 results are void as passes; their hits stand. Rerun.
- The memo register stays dropped (A63 b).
- Program templates: the G13 seed stage against OHS-AC runs with the fixed tools, then (d)/(e).

T41: step-4 results void as passes, hits stand, rerun. Program templates go through the seed stage, then (d)/(e).

T42:
- The step-2 record (12 of 15 program texts hit, keyword 7) is quarantined now.
- Step 4 is void as a pass. Then (d)/(e).

T44:
- The step-2 check (0 hits, partial export) is void as a pass. Rerun against the union.
- The 5 of 8 hit program wordings are quarantined.
- The stage-4 seed run now in progress (pid 30028) uses a57_hashcheck_ac. Its result is a hit record only.

A1 (17 families):
- First OHS-AC comparison: the candidates stage, plus replay units, with the fixed tools, run first.
- A55 (b): drops open no fix round. T24, T25 and T06 get nothing back. Top-ups face the same check.
- If the agent core falls below 5 of 6, or the program families below 10: stop and report (A62 c).

T46, SB5 and every replay source: same rule. No split, no excusal for any family.

## tool_fixes
Every fix is sha-logged in c2_build/zed_orch/a64/A64_TOOLS.md before first use.

1. **Computed completeness.** In a57_hashcheck_ac.py (:153) and a57_hashcmp.py (:61), `complete` is computed, not hard-coded. It is true only when all of these hold; otherwise false, exit 3:
   - the MANIFEST verifies;
   - the addendum finality test passes;
   - the union record exists;
   - every required method ran on every unit.
2. **Finality.** Read from the addendum shas in PREREG_FINAL.md (fadec66f, c2dfefa6, 305356b6, fcf4b384). The MANIFEST stage string (a57_hashcheck_ac.py:98, "post_freeze" read as not final) is recorded only.
3. **One way to build units.** Each text is checked uncut and as cut template pieces, so exact_raw and full_text_* always run (a57_hashcmp.py:53 and a57_t45_stage6.py:88 cut everything; a57_t43_step6.py:21 and a57_hashcheck_ac.py:125-140 never cut). rows_src is passed, so structure_g13, skeleton_state, skeleton_instructions and skeleton_line run (g13_c2.py:484-498).
4. **OHS-AC target path in g13_c2.py** for the seed, candidates and final-mix stages: the hash compare, `g13_ohsac_check --rows` and `gtpl_check_ac --templates --min-shared 1 --parts all`. All methods bind. A53 and A31 (b) are never applied to it.
5. **Held-out-literal remover** for keyword-hit templates. It uses C2 HELD_OUT_* constants only: no sealed lookup, no kw_span.
6. **Held-out checker.** Ids, plus a whole-token, case-insensitive match of identifier and rendered forms across all families, plus 8-gram and 5-word-sentence matches for multi-word literals.
7. **Overlay byte-identity test.** The sealed-mode text constants must equal the frozen file shas (T43 texts.py a9ce9bce…).

**Self-tests** must cover: a known hit, a non-final export (complete false), a missing union record (complete false), a template unit (exact_raw still runs), and a held-out-token fixture.

**Scratch scripts.** Copy unchanged to zed_orch/a64/scratch_record/: kwfind.py 1d2de1c1, kwruns.py d991d1f7, a1_ac.py bc8d253d, a1_kw.py 6be3d7f1, a1_kwfull.py 02fd2eb4.

**Sealed side.** A fresh sealed agent builds only the union record (find, or reproduce to the sha, the freeze export 27808b0c; give |freeze \ final| per kind). Access audit 0, counts only.

**Withdrawn from the earlier draft:** FRAME_SPEC, the frame builder, render provenance, K_core, the provenance audit, kw_span and the undefined A64-M1.

## risks
Costs of the strict reading (stated, not a reason to admit anything):
- T43 probably goes to C3.
- T45 loses its report register, 3 of 5 planned kinds and its whole frame unless an overlay passes every gate by Mon 19 23:59 UTC, which is tight.
- The A1 candidates check against OHS-AC has never run. It could take the agent core below 5 of 6, and then A62 (c) means stop and report, with no C2 training.
- The token-level held-out match will over-drop common words such as memo, journal, registry, tabs and boxed. That is accepted (drops only).
- If the freeze export 27808b0c cannot be found or reproduced to its sha, no OHS-AC hash-compare result admits anything, and the orchestrator stops.

Reviewer points accepted: post-result exemption (1), citations (2), frame classes chosen after the hits (3), internal contradictions (6), T43 keyword fix acting as a probe (7), token-level held-out check (8), missing step-2 records and the third export (9), coercive owner framing, scratch scripts and the GO point (10), replay and no-round A1 families (11), and disclosure (12).

Points rebutted or moot:
- (4) K_core vacuity and (5) the one-sided frame cut are moot. No frame is cut and no K_core is used, so every method runs on uncut text, and instance overlap is caught by the text methods plus structure_g13 and the skeleton kinds now that rows_src is passed.
- A42-D 3.1's "no exemption after a result" sentence is scoped to code-body (G-SL/G3-H) exemptions. The reviewer's conclusion still holds through the house rule and A53.
- The (e) overlay is not the reword-and-rerun probe that A57 (e)6 bans. The frame it avoids is our own known code, disjointness is checked without the export, and there is one compare per iteration within 3.6's cap of 2.
- A63's token naming came from a lookup that was never logged. Its outcome was a removal, so it stands. Going forward, no token lookup is allowed.

Owner timing:
- If the owner prefers a frame reading at the training GO, the T40-T45 pilot verdicts (Mon 19) will already be decided.
- No pilot GO is created.

Running at 07:23 UTC (the user asked):
- pid 30028: zed_orch/a57_t44_stage4.py seed, in c2_build, up 3h28m. It uses a57_hashcheck_ac, so its output is a hit record only.
- pid 30124: `modal run modal_app.py::session`, in lean/speed/opt_c1_20261017, up 37 min. The owner's 16 Oct rule says Modal is for training only, so check that this run was authorised.
- pid 69232: gcloud IAP tunnel to od-cpu1, up 2h11m.
- T41 (36138) and T42 (38063), named in the T45 report, are no longer running.
