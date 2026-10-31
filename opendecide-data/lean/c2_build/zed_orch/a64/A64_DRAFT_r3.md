# A64 revision 3

## ruling_text
> **Ruling A64 (17 Oct 2026, ~07:30 UTC draft, revision 3; orchestrator, Opus; OHS-AC against each family's own sealed split: the T43/T45 A57 step-6 stops, keyword hits, AC tool completeness, the export union, A42-D 3.6 iteration counts; no bar loosened; no waiver; nothing relabelled; drops only.)**
>
> **Written after these results were seen:**
> - the A57 step-2 program-text records: T43 (logs/a57_T43_step2_hashcheck.json, 03:34 UTC, 29 of 34 hit), T42 (logs/a57_T42_step2_hashcheck_ac.json, 03:38 UTC, 12 of 15 hit, keyword 7) and T44 (zed_orch/a57/T44_step2_hashcheck.json, 03:40 UTC);
> - the T43 and T45 step-6 records (05:49 UTC);
> - the T44 driver's program-wording hits (5 of 8);
> - unlogged scratch-script output:
>   - kwfind.py was created ~03:39 UTC by a Phase-A T44 driver;
>   - kwruns.py, a1_ac.py, a1_kw.py and a1_kwfull.py were written and run 06:21-06:35 UTC by the Opus agent draft:A64 of this ruling's own workflow;
>   - the output showed A1 units checked against the OHS-AC export, and keyword token runs;
>   - only draft:A64, skeptic1, revise1, skeptic2 and revise2 saw it. The orchestrator has not read it;
>   - draft:A64's prompt lacked the no-probing rule. That is an orchestrator prompt omission, recorded as a deviation ((c)).
>
> For that reason this ruling adopts no reading that admits more text than the literal rules allow.
>
> - **(a) Scope of the step-6 records.**
>   - A57 (b) says A57 "does not cover program text". T43 and T45 have no Haiku pool and no task file (logs/a57_T43_step2_manifest.json: 0 files), so their A57 steps 2-7 are empty.
>   - `logs/a57/T43_step6.json` (sha256 2ec98857…) and `logs/a57/T45_step6_program_text.json` (sha256 b80b41ad…) are therefore not A57 admission records. They are G13 seed-stage records for program templates against the final OHS-AC export. A42-D 3.5 runs the seed stage first for T40-T45, and spec 6.4 step 4 says "a hit quarantines that template only".
>   - The same applies to the T42, T43 and T44 step-2 program-text records and to the T44 wording hits.
>   - The tools that produced these records are defective ((g)). So a record can count as a hit but never as a pass.
>     - Every unit listed as hit is quarantined now (drops only).
>     - For every family still in C2, the seed stage is rerun with the fixed tools before any row of that family is written. The rerun can only add quarantines.
>   - **Erratum to A63 (e).** "Dropped at step 6 / row G13" now reads "dropped at G13: at the seed stage for program templates, at candidates and the final mix for rows". The drop itself is unchanged.
>
> - **(b) The frame question: considered, not adopted.**
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
> - **(c) One rule for every text.**
>   - **Coverage.** The same tools, at the same bars, compare OHS-AC with every model-visible training-side text of every family. Row origin changes nothing.
>     - Texts: candidate, carry, top-up, replay, own-dev and pilot rows; every template and program literal; every Haiku pool item and task file.
>     - Families: the 17 A1 families, T40-T45, T46, SB5 and every replay source.
>   - **Where A1 meets OHS-AC.** A42-D 3 opens with "They apply to each of T40-T45, with the 5.3/6.4 fix loop". So the 3.5 stages (seed, candidates, final mix) bind T40-T45 only. For the 17 A1 families and replay, the pre-registered OHS-AC check is:
>     - the 3.5 registry target ("The target registry adds the OHS-AC sealed-side export") applied at the final-mix G13. Sources: spec 6.4 step 10 ("G13 on the final mix (new targets)"); spec 5.4 (replay is checked only against new targets); A55 ("The final all-block G13 binds");
>     - for later rows, 13.1's A1 sentence: no later training-side row may use an A1 held-out variant (G-TPL plus the sealed-side child of G13).
>   - **A1 has no binding OHS-AC record yet.** Every c2_cand log predates the 02:25 UTC freeze, and g13_c2.py has no OHS-AC path.
>   - **An early A1 and replay check is allowed, not required.**
>     - It runs once, on every A1 candidate and replay unit, after the fixed tools pass their self-tests and the (h) record exists.
>     - It only drops. No G9 selection has run yet (HANDOFF), so nothing is refilled.
>     - It is not "the 3.5 candidates stage", and no text cited here requires it. The final-mix G13 still runs and binds.
>     - A55 (b) holds: G13 drops open no fix round. Top-ups (A55 L2) face the same check.
>   - **When a family counts as lost.** This applies to A62 (c)'s agent core (5 of 6) and to the program-family count (at least 10). A family is lost when, after G13 drops and any A55 L2 top-up, either:
>     - it has 0 rows; or
>     - its remaining rows fail a later binding gate.
>     - A short family that still passes is not lost (A55 b).
>     - If the agent core falls below 5 of 6, or the program families fall below 10, the orchestrator stops and reports (A62 c).
>   - **The scratch scripts.** They are not logged results. They decide nothing, and no number from them is cited.
>     - They are copied unchanged to `c2_build/zed_orch/a64/scratch_record/`, with sha256: kwfind.py 1d2de1c1…, kwruns.py d991d1f7…, a1_ac.py bc8d253d…, a1_kw.py 6be3d7f1…, a1_kwfull.py 02fd2eb4…. Their outputs are not copied, read or cited.
>     - **Deviation.** draft:A64's prompt lacked the no-probing rule. That orchestrator prompt omission is recorded in the PREREG addendum that adopts A64 and in every OHS-AC report ((k)).
>     - **Who is barred.** draft:A64, skeptic1, revise1, skeptic2 and revise2 may not author any fix, overlay, (d) deletion, (f) list, selection or top-up, or a driver prompt for one.
>       - The same bar covers any other agent that ran one of these scripts or any token-to-keyword lookup, including the lookup behind A63's token names.
>       - No fix author receives those outputs or anything derived from them.
>     - **What the scripts shaped.** The early A1 check above and the A1 risk line were first written by agents who had seen the A1-vs-AC output.
>       - The check is kept only for reasons that do not depend on that output: it only drops, the final-mix G13 binds on the same rows anyway, and nothing is refilled.
>       - The risk line gives no estimate.
>       - This revision was written without reading the outputs.
>
> - **(d) Keyword hits.**
>   - Keyword runs on every uncut model-visible field.
>     - A hit on a row drops the row's unit.
>     - A hit on a program template quarantines the whole template, whatever entry it matched (spec 6.4 step 4: "a hit quarantines that template only").
>     - A hit on a task file or Haiku pool item removes the hitting content and never replaces it with a synonym (A63 a, b).
>   - **Bringing an edited template back is a template fix.** It needs a counted A42-D 3.6 iteration ((i)) and follows every rule of (e): one compare, permanent quarantine on a hit, and a full gate rerun by Mon 19 Oct 23:59 UTC. Inside such an iteration, the only edit allowed to a keyword-hit template is deletion:
>     1. A C2-side program matches the template against the union of every family's HELD_OUT_* constants, in identifier and rendered forms. It uses C2 code only, with no sealed lookup.
>     2. Every sentence or list item that contains a held-out literal is deleted, with no replacement. If the meaning of a head, option, register, kind or rule needs that sentence, the whole head, option, register, kind or rule is removed.
>     3. If no held-out literal is found, nothing comes back.
>     - With no iteration left, the template stays removed. Nothing replaces its meaning in any form: no synonym and no paraphrase (A63 a).
>   - No program looks up which token of a hit unit matches a keyword hash. No replacement text is ever tried against any export.
>   - A held-out or sealed-mode-only literal that hit needs no further removal if (f) shows that 0 training-side or dev rows or templates render it. That drop is already in place; it is not an exemption.
>   - **A63 (c) is withdrawn.**
>     - A63 (c) allowed "pure output-format scaffolding" to be reworded. `c2_build/zed_orch/a57/T40_step2_manifest.json` records `scaffolding_reworded`: "one object per item" → "one entry per item".
>     - "object" was one of A63's keyword hits, named by a lookup that was never logged.
>     - The reworded r1 task files were then hash-compared against the final export (logs/a57/T40_taskhash_ac_r1.json, 0 hits).
>     - That is replacement text tried against an export after a token lookup, which this item forbids. The earlier draft's line "A63's outcome was a removal, so it stands" was wrong and is withdrawn.
>     - From now on, a scaffolding line that hits is deleted, never reworded.
>     - The T40 r1 task files have no valid step-2 record. Every answer authored from them is discarded unused and counted.
>     - A63 (a), (b), (d) and (e) (as amended in (a)) stand: they only remove.
>
> - **(e) Shared frame without a keyword hit** (exact, sentence, n-gram, tulu8, MinHash, substring, skeleton, structure or G-TPL hits).
>   - **Quarantine.** The template is quarantined (spec 6.4 step 4). A quarantine is not an iteration.
>     - A family whose quarantines leave it unable to produce the rows a gate needs has failed that gate evaluation.
>     - It may then use a remaining 3.6 iteration, as counted in (i). With none left, it moves to C3.
>     - By (i), only T41 has an iteration left.
>   - **The fix: a training-side text overlay** (generator and templates only), selected for samplers outside HELD_OUT_SAMPLERS.
>     - A C2-side test proves that the sealed-mode text constants are byte-identical to the family's frozen source shas. The shas come from a pre-freeze C2-side record: a code-identity record, a backup or git. Without such a record, no overlay is possible for that family.
>     - G0-lite is updated and sha-logged before the first post-fix row.
>   - **Who writes the new text.** A fresh author, not one of the agents barred in (c).
>     - The author gets the quarantined template ids and the C2 code only.
>     - The author never gets an export, a checker output beyond those ids, scratch output, any overlay-hit id, an earlier overlay file or its diff.
>   - **C2-side pre-check, before any sealed compare.** It mirrors every method that can be computed on the C2 side. It uses the G13 engine's own functions and thresholds (g13_c2, decontam_g13, struct_g13) and G-TPL at min-shared 1, all parts.
>     - Methods:
>       - exact full text (raw, normalised and min-5-words);
>       - sentences of 5 or more words;
>       - exact_short (every option and label string);
>       - substring;
>       - 8-, 10- and 12-grams, with the tulu8 rule;
>       - MinHash;
>       - G-TPL shared 8-grams;
>       - skeleton_line (6-7-token lines), skeleton_state, skeleton_instructions and structure_g13.
>     - It compares against two sources:
>       - every text constant and template that any family's sealed mode can reach, read from the C2 code;
>       - training-mode renders of the frozen generators, which carry the same frame.
>     - No HELD_OUT_SAMPLER is run on the C2 side.
>     - Keyword matching cannot be computed on the C2 side; (f)(ii) covers held-out literals.
>     - A pre-check hit may be rewritten before the sealed compare, because the pre-check uses no sealed information.
>     - The new text restores no content that (d) removed.
>   - **One sealed compare per iteration** (a G13 seed compare against OHS-AC with the fixed tools).
>     - An overlay unit that hits is quarantined permanently. It is never re-authored in any iteration, its template stays quarantined, and no later author receives its id.
>     - **Overlay text is written once per family**, before that family's first overlay compare. A later iteration may remove overlay units or change non-text generator code, but writes no new overlay text.
>   - **Gates rerun.** Every A42-D 3 gate and probe, 3.3, 3.4, G5-H, G-LEX and G3-H reruns on fresh post-fix rows at unchanged bars.
>     - Iteration-2 results are due Mon 19 Oct 23:59 UTC.
>     - Otherwise the family moves to C3. Its frozen items stay in the suite, reported as "family not trained in C2" (A62 b).
>   - **Why first-written overlay text is not the probe that A57 (e)6 bans.**
>     - It is made disjoint from the family's own code, which the C2 side already knows, without using the export. The export is then consulted once.
>     - That reasoning holds only for text written before any OHS-AC result on that family's overlay exists.
>     - The overlay is already disjoint from every sealed-mode frame the C2 side knows. So a hit can only come from sealed text the C2 side does not know: post-freeze surface variants, hijack rewrites, real-text items or keyword sources.
>     - Rewording after such a hit would be exactly the banned probe, so it is not allowed.
>
> - **(f) Held-out check.**
>   - Source: 13.1 ("no training-side or dev row uses a held-out value"), applied across families as A63 (b) did. Binding.
>   - Rows covered: every training-side row and template, and every dev row (own-dev 4.4, mixdev and transfer-dev).
>   - **(i) Ids.** Every covered row's sampler, register, operator, template, fault, domain, pack, layout and wording id lies outside every family's held-out sets. Required: 0 rows inside.
>   - **(ii) Text.** Every covered row and template is compared with the union of all families' HELD_OUT_* literals:
>     - by whole-token, case-insensitive match of their identifier and rendered forms, with snake, camel and kebab forms both split and joined;
>     - plus 8-grams and sentences of 5 or more words for multi-word literals.
>     - Any hit drops the row or removes the template.
>     - A dropped dev row is not refilled from a held-out value. A dev set rebuilt under A55 L1 must pass the same check.
>     - Over-matching of common words is accepted (drops only).
>   - The 1,200-draw tests do not stand in for this check.
>
> - **(g) Tools.** All are program fixes, sha-logged in `c2_build/zed_orch/a64/A64_TOOLS.md` before first use.
>   1. **Computed completeness.** `complete` in a57_hashcheck_ac.py and a57_hashcmp.py is true only if all of these hold; otherwise it is false (exit 3):
>      - the MANIFEST verifies;
>      - check 2 below passes;
>      - the (h) record exists;
>      - every required method ran on every unit.
>   2. **Finality from the addendum.** Finality is decided by the addendum shas read from PREREG_FINAL.md: MANIFEST fadec66f…, suite c2dfefa6…, post-freeze manifest 305356b6… and source manifest fcf4b384…. The MANIFEST stage string is recorded but decides nothing.
>   3. **One way to build units.** Each text is checked both uncut and as template pieces, so that exact_raw and full_text_* always run. rows_src is passed, so that structure_g13, skeleton_state, skeleton_instructions and skeleton_line also run.
>   4. **An OHS-AC path in g13_c2.py** for the seed, candidates and final-mix stages. It runs the hash compare, `g13_ohsac_check --rows` and `gtpl_check_ac --templates --min-shared 1 --parts all`. Every method binds. A53 and A31 (b) never apply to it.
>   5. The (d) held-out-literal matcher, used only inside a counted iteration.
>   6. The (f) checker.
>   7. The (e) byte-identity test.
>   8. The (e) C2-side pre-check.
>   - **Self-tests:** a known hit; a non-final export (complete false); a missing (h) record (complete false); a template unit (exact_raw still runs); a held-out-token fixture; a pre-check fixture for each mirrored method.
>   - **Earlier results.** Every earlier result marked complete true by a57_hashcheck_ac.py or a57_hashcmp.py is void as a pass, and its hits stand as drops or quarantines. Every admission reruns with the fixed tools. This covers:
>     - T40 task files (r0 and r1);
>     - T40, T41, T42 and T44 step 4, including two runs still going: the T44 stage-4 seed run (pid 30028) and the T40 stage-4c run (pid 95072, zed_orch/a57_t40_stage4c.py, since ~06:00 UTC; it imports g13_c2 and calls both sealed checkers);
>     - T42, T43 and T44 step 2;
>     - T43 and T45 step 6.
>   - **Live runs.** Editing the tools in place does not change pid 30028 or pid 95072. g13_c2 is already imported in them, and the engine workers load the unedited decontam_g13.py and check its sha. A64_TOOLS.md records that both runs used the pre-fix code. Their outputs are hit records only.
>   - **Sealed side.** The only new sealed-side work is the (h) record. A fresh sealed agent does it, with an access audit of 0 and counts only.
>
> - **(h) Exports and the union.**
>   - **Three export states have been used:**
>     - the freeze export 27808b0c…;
>     - a post_freeze_partial export a2c95c19… (suite 7ad1747e…), used by the T40 r0 task-file check and the T42, T43 and T44 step-2 records;
>     - the final export fadec66f….
>   - **A57 step 2 ("against the freeze-time export") was never met.**
>     - Every task file used for authoring is rechecked against the union, by its sha.
>     - A file with any hit discards every answer authored from it, unused (counted).
>     - A63's union rerun is still open: T40 r1 was checked against the final export only.
>   - **Which checks need the union record.** `g13_ohsac_check` and `gtpl_check_ac` verify the 14,407-item final suite, which contains the 12,680 frozen items (fcf4b384… verified). The C2-side hash compare has only the export, so for it the union binds. A fresh sealed agent works in this order:
>     1. **Find a copy.** It looks for a byte copy of the freeze export (MANIFEST sha256 27808b0c…) in:
>        - the Mac;
>        - od-cpu1;
>        - od-l4b, where c2_build is synced (families/T43/CODE_IDENTITY_A56.json);
>        - every other project VM;
>        - every c2_build backup tree and VM copy;
>        - other backups and any Time Machine snapshot;
>        - the sealed folders.
>        - A found copy counts only if its MANIFEST sha is 27808b0c… and every file it lists matches the sha256 the MANIFEST gives for it.
>        - The agent then records |freeze \ final| per kind, counts only. If any count is above 0, a union export is built and used.
>     2. **Re-derive it.** If no copy is found, the agent re-derives the freeze export from the 12,680 frozen items. Required inputs:
>        - the freeze-time export code;
>        - the freeze-time keyword sources;
>        - the freeze-time FORMAT.md bytes, whose sha256 the freeze MANIFEST recorded as format_md_sha256.
>        - The current FORMAT.md (final MANIFEST format_md_sha256 81cd6c0c…) was rewritten for the 14,407-item final export, so it cannot be used.
>        - These inputs are searched for in the step-1 places.
>        - The result counts as the freeze export only if its MANIFEST sha reproduces 27808b0c….
>     3. **Stop.** If neither step works, the loss is recorded as a deviation in a PREREG addendum, no hash-compare result admits anything, and the orchestrator stops and reports (as A62 c). The stop is right because the post-freeze addendum makes the union bind every later G13 and admission check.
>   - FORMAT.md's line "contains every hash of the freeze-time export" is the sealed side's claim, not this record.
>
> - **(i) A42-D 3.6 iteration counts (set now, from the build records; no driver recounts).**
>   - **Rule.**
>     - A 3.6 iteration is one recorded round of generator or template change, made after a recorded check of that family failed a gate or probe bar. The check counts at any size, in memory or on rows, before or after the freeze.
>     - Pre-freeze rounds count. 3.6 makes "the first failed gate evaluation" iteration 0 and has no pre-freeze exception. A56 (b) called T43's pre-freeze G0 v1.3 change "a generator fix under A42-D 3.6".
>     - Variants built and discarded inside one recorded round count as that round.
>     - Where a record lists several fixes of measured cues with no round boundaries, they count as 2.
>     - A family at 2 or more has no iteration left.
>     - A family whose record shows a failed gate or probe result at binding size after its second counted round has met 3.6's C3 condition ("still fails any gate or probe after iteration 2").
>     - A spec 6.4 step-4 quarantine is not an iteration. Any edit that brings quarantined text back is one.
>     - This rule is set after the results were seen, so it takes the higher count wherever a record is unclear.
>   - **Counts.**
>     - **T40: at least 3.**
>       - Iteration 0 is the A45 7,001-row check before its fixes (result_base.json).
>       - The rounds are the A45 generator fixes (result_fix1, result_fix3), wave 4 and wave 8.
>       - After wave 4, head C choice d_meta GBT was +2.3 pp at 10,000 rows (bar +2 pp).
>       - So 3.6's C3 condition was met before the freeze. **T40 moves to C3.**
>     - **T41: 1** (the A45 "Generator fix (one)", after the wave-1 pilot-size G6 fail of 0.271 against a bar of 0.270). One iteration is left (iteration 2, due Mon 19 Oct 23:59 UTC).
>     - **T42: 2.** Iteration 0 is wave 1. The rounds are A45 round 1 (still failing at 5,004 rows) and round 2 with the A46 fixes (passing at 10,008 rows). None left.
>     - **T43: 3.**
>       - The rounds are w4 (after the A45 5,202-row check), w8 and w9 (G0 v1.3, A56 b).
>       - After w8 (w8q), the diff-size probe LR was +3.1 pp at 10,206 rows (bar +3 pp).
>       - So the C3 condition was met before the freeze.
>     - **T44: 2,** by the no-boundaries rule. BUILD_NOTES lists "Design facts forced by the probes (each fixed a measured cue)", for example options-only LR 0.42 on 2,500 rows before the fix. Its only later binding check passed (A45, 6,000 rows), so the C3 condition is not met. None left.
>     - **T45: at least 2.** BUILD_NOTES records "Fix round" and "Fix round 2" (orchestrator, 15 Oct, after G6 fails). The backup names _backup_fix2 and _backup_fix3 may mean an earlier fix 1. The A45 10,008-row check then passed. None left.
>     - **T46 and SB5** are not A42-D 3 families, and A59 and A58 give them no fix loop. An OHS-AC hit is a quarantine or drop only.
>     - **A1:** A55 (b) applies; G13 drops open no fix round.
>
> - **(j) Each new family now.**
>   - **T43 moves to C3**, on two grounds:
>     - the 3.6 count ((i));
>     - as built it has 0 rows. The six rules, 17 of the 18 wordings, opt:B and opt:C are quarantined, and every row renders one of the 6 rules. No iteration is left.
>     - Its keyword hits need no (d) work. The 500 sealed calls hit equal T43's whole split, which adds nothing beyond the drops. The earlier draft's multi-token keyword attributions are withdrawn.
>     - Its 500 B-block items stay, reported as "family not trained in C2" (A62 b).
>   - **T45 moves to C3.**
>     - 108 of 395 training units are quarantined, including all 32 rules blocks, both rules templates and all 6 question wordings. Every row needs these, so T45 has 0 rows, and no iteration is left.
>     - The keyword-hit content stays removed and nothing comes back: the report register, the planned db, http and tests kinds, texts.py #42, #43 and #45, and scenarios.py #0, #11, #82, #90, #100, #109, #133 and #328.
>     - Its 400 A2 items stay, reported as "family not trained in C2".
>   - **T40 moves to C3** by the 3.6 count ((i)).
>     - No T40 row, pool item or task file enters C2.
>     - Its recorded hits stand, and A63's memo drop stands.
>     - Its 500 A2 items stay, reported as "family not trained in C2".
>   - **T41** has 1 iteration left. Its step-4 results are void as passes, and their hits stand. Its seed stage reruns with the fixed tools, then (d) and (e) apply.
>   - **T42** has none left. Its step-2 record (12 of 15 program texts hit, keyword 7) is quarantined now, its step 4 is void as a pass, and its seed stage reruns.
>   - **T44** has none left. Its step-2 check (0 hits, partial export) is void as a pass and reruns against the union. Its 5 of 8 hit program wordings are quarantined.
>   - **T42 and T44:** if their quarantines leave them unable to produce the rows a gate needs, or their fresh rows fail any gate, they move to C3.
>   - No pool freeze applies to T43 or T45. Nothing is refilled by hand. A55 L2 top-ups meet the same checks.
>
> - **(k) Disclosure.** Every OHS-AC report states the following, for blocks A1, A2 and B:
>   - each split comes from the family's own generator (sealed mode): new instances plus the listed held-out values;
>   - for each family trained in C2, whether its training text was the frozen frame or an (e) overlay disjoint from the sealed frame. A1 families' frames were trained by C1 before the A1 split was built (13.1);
>   - that G-TPL and G13 against OHS-AC counted all text, with no frame or own-split excusal (A64 b);
>   - that A64 was written after the records named in its header had been seen, together with the scratch-script attribution and the prompt-omission deviation ((c));
>   - the A63 (c) withdrawal and the count of discarded T40 r1 answers;
>   - per family, as counts and classes: the 3.6 count from (i); rows dropped against OHS-AC; templates quarantined; content removed by (d) (register, kind, head or option); iterations used; and whether the family moved to C3, and why;
>   - that Jev and the baselines see each split cold, with the 13.6 definitions.

## decision
No text is admitted under a frame or own-split excusal. G-TPL and G13 against OHS-AC apply literally: every method, uncut text, every family, every row origin. The earlier draft's frame excusal, and its K_core, provenance-audit, kw_span and M1 parts, stay withdrawn.

What happens now:
- All recorded hits stand as quarantines or drops. A hit on a program template quarantines the whole template (spec 6.4 step 4).
- A42-D 3.6 iteration counts are fixed now from the build records. Pre-freeze rounds count, and an unclear record takes the higher count.
  - T40 (at least 3) and T43 (3) still failed a binding check after their second round, so both met 3.6's C3 condition before the freeze.
  - T42, T44 and T45 have none left. T41 has 1 left.
- Moves to C3 now: T40 (by the count), T43 (by the count, and 0 rows as built) and T45 (0 rows as built, none left). Their frozen items stay in the suite, reported as "family not trained in C2".
- T42 and T44 have no iteration left. A quarantine that leaves either unable to produce gate rows, or a failed gate on fresh rows, moves it to C3.
- Bringing an edited template back (a held-out-literal deletion, or an overlay) is a counted 3.6 iteration with one sealed compare and a full gate rerun by Mon 19 Oct 23:59 UTC. Only T41 can do this.
  - An overlay unit that hits is quarantined permanently and never re-authored.
  - Overlay text is written once, before the family's first overlay compare.
  - The C2-side pre-check mirrors every method that can be computed on the C2 side.
- A63 (c) is withdrawn. T40's reworded scaffolding was replacement text tried against an export after a token lookup. Such a line is now deleted, never reworded, and the T40 r1 answers are discarded (counted).
- The held-out check gets a token-level, cross-family text match covering training rows, templates and all dev rows (own-dev, mixdev, transfer-dev).
- A1 and replay: an early OHS-AC check with the fixed tools is allowed (drops only, nothing refilled). It is not the 3.5 candidates stage. The final-mix G13 binds.
  - A family is lost if it is left with 0 rows or its remaining rows fail a later binding gate.
  - A62 (c) and the 10-family floor apply.
- Every earlier complete=true result from a57_hashcheck_ac.py or a57_hashcmp.py is void as a pass, and its hits stand. The live pid 30028 and pid 95072 runs are hit records only.
- No OHS-AC hash-compare result admits anything until a sealed-side union record exists for the freeze export 27808b0c. The search covers od-l4b, the other VMs and the backup trees. Every file must be verified, and the freeze-time FORMAT.md bytes are a required input; otherwise the orchestrator stops.
- The scratch scripts' outputs were seen only by draft:A64, skeptic1, revise1, skeptic2 and revise2, not by the orchestrator. Those agents are barred from authoring any fix, overlay, deletion or selection. The prompt omission is recorded as a deviation.
- Only the owner can change a gate after a result, and the orchestrator does not ask. The training-GO request (or an A62 (c) stop report) quotes A64 (b) neutrally, with the measured counts.
- No pilot-spend GO is created. Pilots stay as A42-D 4.1 sets them.

## per_family
T40: moves to C3.
- 3.6 count at least 3: the A45 generator fixes (result_fix1, result_fix3), wave 4 and wave 8. After wave 4, head C choice d_meta GBT was +2.3 pp at 10,000 rows (bar +2), a binding fail after the second round.
- No T40 row, pool item or task file enters C2. Its 500 A2 items stay, reported as "family not trained in C2".
- Its records are void as passes and their hits stand: the r0 task-file check (partial export a2c95c19), the r1 check (final export only) and step 4.
- The A63 memo drop stands. A63 (c) is withdrawn: the r1 files have no valid step-2 record, and their answers are discarded (counted).
- The stage-4c run (pid 95072) produces a hit record only.

T41: 3.6 count 1 (A45 "Generator fix (one)"), so 1 iteration is left (iteration 2, due Mon 19 Oct 23:59 UTC).
- Step-4 results are void as passes; their hits stand. Rerun with the fixed tools.
- Program templates go through the seed stage, then (d) and (e).
- An overlay or held-out-literal deletion is possible only inside that iteration, by a non-barred author, with the C2-side pre-check, one sealed compare, permanent quarantine on any hit and a full gate rerun.
- It also needs a pre-freeze C2-side record of T41's frozen source shas.

T42: 3.6 count 2 (A45 rounds 1 and 2), so none is left.
- The step-2 record (12 of 15 program texts hit, keyword 7) is quarantined now.
- Step 4 is void as a pass. The seed stage reruns with the fixed tools.
- No overlay and no deletion. If its quarantines leave it unable to produce gate rows, or fresh rows fail any gate, it moves to C3.

T43: moves to C3.
- 3.6 count 3 (w4, w8, w9). After w8 the diff-size probe LR was +3.1 pp at 10,206 rows (bar +3), a binding fail after the second round.
- As built it has 0 rows: all 6 rules, 17 of 18 wordings, opt:B and opt:C are quarantined.
- Its 500 B-block items stay, reported as "family not trained in C2".

T44: 3.6 count 2 (no-boundaries rule: the "Design facts forced by the probes" fixes), so none is left. The C3 condition is not met, because its A45 6,000-row check passed.
- The step-2 check (0 hits, partial export) is void as a pass. Rerun against the union.
- The 5 of 8 hit program wordings are quarantined.
- The stage-4 seed run (pid 30028) produces a hit record only.
- The C3 trigger is the same as for T42.

T45: moves to C3.
- 3.6 count at least 2 ("Fix round" and "Fix round 2", 15 Oct), so none is left.
- 108 of 395 training units are quarantined, including all 32 rules blocks, both rules templates and all 6 wordings. Every row needs these, so it has 0 rows.
- The keyword-hit content (report register, planned db/http/tests, texts.py #42/#43/#45, the 8 scenarios.py literals) stays removed.
- Its 400 A2 items stay, reported as "family not trained in C2". No pool freeze.

A1 (17 families):
- The pre-registered OHS-AC check is the registry target at the final-mix G13 (spec 6.4 step 10, spec 5.4, A55), plus 13.1's A1 sentence for later rows.
- An early check of every candidate and replay unit with the fixed tools is allowed. It only drops, and nothing is refilled because no G9 selection has run.
- A55 (b): drops open no fix round. T24, T25 and T06 get nothing back. Top-ups face the same check.
- A family is lost if it is left with 0 rows, or its remaining rows fail a later binding gate. If the agent core falls below 5 of 6, or the program families below 10, the orchestrator stops and reports (A62 c).

T46, SB5 and every replay source:
- The same coverage applies.
- A59 and A58 give no fix loop, so hits are quarantines or drops only. No family gets an excusal.

## tool_fixes
Every fix is sha-logged in c2_build/zed_orch/a64/A64_TOOLS.md before first use.

1. **Computed completeness.** In a57_hashcheck_ac.py (:153) and a57_hashcmp.py (:61), `complete` is computed, not hard-coded. It is true only when all of these hold; otherwise it is false, exit 3:
   - the MANIFEST verifies;
   - the addendum finality test passes;
   - the union record exists;
   - every required method ran on every unit.
2. **Finality.** It is read from the addendum shas in PREREG_FINAL.md (fadec66f, c2dfefa6, 305356b6, fcf4b384). The MANIFEST stage string (a57_hashcheck_ac.py:98, where "post_freeze" is read as not final) is recorded only.
3. **One way to build units.** Each text is checked uncut and as cut template pieces, so exact_raw and full_text_* always run.
   - Today a57_hashcmp.py:53 and a57_t45_stage6.py:88 cut everything, and a57_t43_step6.py:21 and a57_hashcheck_ac.py:125-140 never cut.
   - rows_src is passed, so structure_g13, skeleton_state, skeleton_instructions and skeleton_line run (g13_c2.py:484-498).
4. **OHS-AC target path in g13_c2.py** for the seed, candidates and final-mix stages: the hash compare, `g13_ohsac_check --rows` and `gtpl_check_ac --templates --min-shared 1 --parts all`. All methods bind. A53 and A31 (b) are never applied to it.
5. **Held-out-literal matcher** for keyword-hit templates, used only inside a counted 3.6 iteration. It uses C2 HELD_OUT_* constants only: no sealed lookup, no kw_span.
6. **Held-out checker** for training rows, templates and own-dev, mixdev and transfer-dev rows. It checks ids, then a whole-token, case-insensitive match of identifier and rendered forms across all families, then 8-gram and 5-word-sentence matches for multi-word literals.
7. **Overlay byte-identity test.** The sealed-mode text constants must equal the family's frozen source shas from a pre-freeze C2-side record. Without such a record, no overlay is possible.
8. **Overlay C2-side pre-check.** It uses the engine's own functions and thresholds to run exact full (raw, normalised, min-5-words), 5-word sentences, exact_short, substring, 8/10/12-grams with tulu8, MinHash, G-TPL 8-grams, skeleton_line, skeleton_state, skeleton_instructions and structure_g13. It compares against sealed-mode-reachable constants and templates (read from code) and training-mode renders of the frozen generators. No HELD_OUT_SAMPLER is run.

**Self-tests** must cover:
- a known hit;
- a non-final export (complete false);
- a missing union record (complete false);
- a template unit (exact_raw still runs);
- a held-out-token fixture;
- one fixture for each mirrored pre-check method.

**Live runs.** pid 30028 (a57_t44_stage4.py seed) and pid 95072 (a57_t40_stage4c.py) are not changed by in-place edits: g13_c2 is already imported, and the engine workers load the unedited decontam_g13.py and check its sha. A64_TOOLS.md records that both runs used the pre-fix code. Their outputs are hit records only.

**Scratch scripts.** Copy them unchanged to zed_orch/a64/scratch_record/: kwfind.py 1d2de1c1, kwruns.py d991d1f7, a1_ac.py bc8d253d, a1_kw.py 6be3d7f1, a1_kwfull.py 02fd2eb4. Their outputs are not copied, read or cited. No tool may run against them.

**Sealed side.** A fresh sealed agent builds only the union record. Access audit 0, counts only.
- It searches for the freeze export 27808b0c in: the Mac, od-cpu1, od-l4b, every other VM, every c2_build backup tree and VM copy, other backups and Time Machine snapshots, and the sealed folders.
- A found copy must have its MANIFEST sha and every listed file's sha verified.
- Otherwise it re-derives the export. That needs the freeze-time export code, the freeze-time keyword sources and the freeze-time FORMAT.md bytes (the freeze MANIFEST's format_md_sha256, not the current 81cd6c0c…).
- It then gives |freeze \ final| per kind.

**Withdrawn from the earlier drafts:** FRAME_SPEC, the frame builder, render provenance, K_core, the provenance audit, kw_span, the undefined A64-M1, and the uncounted (d)1 partial-deletion path.

## risks
Costs of the strict reading (stated, not a reason to admit anything):
- T40, T43 and T45 move to C3 now. T40's move is new in this revision: it follows from the counting rule that problem (2) asked for, because its record shows a binding G6 fail after its second pre-freeze round. A52 (b) found that T40 met the A45 (d) freeze-entry bar. That finding is about entering the freeze, not about iterations left, so this ruling does not contradict it. The frozen items of all three stay in the suite.
- T42 and T44 have no iteration left. Their step-2 quarantines (12 of 15 texts; 5 of 8 wordings) and the seed rerun may leave them unable to produce gate rows, which means C3. Only T41 can use an overlay, and only with a pre-freeze source-sha record.
- The early A1 check against OHS-AC has never run with valid tools. A family left with 0 rows, or failing a later binding gate, counts as lost, and A62 (c) or the 10-family floor may then mean stop and report, with no C2 training. No estimate is given, because the earlier authors of this line had seen A1-vs-AC output.
- The token-level held-out match will over-drop common words, such as memo, journal, registry, tabs and boxed, in training and dev rows. Dropped dev rows are not refilled from held-out values. This is accepted (drops only).
- If the freeze export 27808b0c cannot be found or reproduced to its sha, no OHS-AC hash-compare result admits anything, and the orchestrator stops. Reproducing it needs the freeze-time FORMAT.md bytes, which may be lost.

This round's points, all accepted:
- (6) Attribution corrected in the header and in (c), as verified. What was seen is named. The five agents are barred from any fix, overlay, (d) deletion, (f) list, selection or top-up. The prompt omission is a deviation.
- (4) Overlay: a hit is quarantined permanently; there is no re-authoring and no hit ids go to later authors. Overlay text is written once, before the first compare. The not-a-probe argument is limited to first-written text. The pre-check mirrors every C2-computable method.
- A63: (c) is withdrawn on the facts. The rewording was recorded in c2_build/zed_orch/a57/T40_step2_manifest.json and compared in logs/a57/T40_taskhash_ac_r1.json. The manifest is under zed_orch/a57/, not logs/a57/ as the reviewer wrote.
- (2) The counting rule is set now and counts are stated per family. One reading note: T43's "fix iteration 1 candidates" is the open-items list that w4 then implemented, so I count w4, w8 and w9 as 3 rounds, not 4. The outcome (none left, C3 condition met) is the same either way.
- (1) The partial-deletion path is a counted 3.6 iteration with the full rerun. Otherwise the template stays removed.
- (3) The A1 citation is corrected: 3.5 binds T40-T45. A1's pre-registered exposure is the registry target at the final-mix G13 plus 13.1's A1 sentence. The early check is allowed, not required. The lost-family trigger is defined.
- (f)(ii) Own-dev, mixdev and transfer-dev rows are added to (f)(i) and (f)(ii).
- (5) (h): the search adds od-l4b, other VMs and backup trees. Every file is verified. The freeze-time FORMAT.md is a required input. The stop condition is kept.
- Facts: pid 95072 is added. The live-run note is added. The owner-timing line inviting a frame reading at the training GO is removed.

Earlier rounds' accepted points are unchanged: post-result exemption, citations, frame classes chosen after the hits, internal contradictions, the T43 keyword fix acting as a probe, the token-level held-out check, missing step-2 records and the third export, coercive owner framing, scratch scripts and the GO point, replay and no-round A1 families, and disclosure.

Points rebutted or moot (kept):
- K_core vacuity and the one-sided frame cut are moot. No frame is cut and no K_core is used, so every method runs on uncut text. Instance overlap is caught by the text methods plus structure_g13 and the skeleton kinds now that rows_src is passed.
- A42-D 3.1's "no exemption after a result" sentence is scoped to code-body (G-SL/G3-H) exemptions. The conclusion still holds through the house rule and A53.
- First-written overlay text is not the A57 (e)6 probe: the frame it avoids is our own known code, disjointness is checked without the export, and there is one compare. Text written after any overlay compare is barred.

No pilot GO is created.

Running at 07:23 UTC (the user asked):
- pid 30028: zed_orch/a57_t44_stage4.py seed, in c2_build, up 3h28m. It uses a57_hashcheck_ac, so its output is a hit record only.
- pid 95072: zed_orch/a57_t40_stage4c.py, in c2_build, running since ~06:00 UTC. It imports g13_c2 and calls g13_ohsac_check --rows and gtpl_check_ac --templates. Its output is a hit record only, and T40 moves to C3 anyway.
- Neither run is changed by in-place tool edits. A64_TOOLS.md records that both used the pre-fix code.
- pid 30124: `modal run modal_app.py::session`, in lean/speed/opt_c1_20261017, up 37 min. HANDOFF records the owner's OK (~05:30 UTC) for one H100 session of at most $5 on spare Modal (wf_21cc4913-081), which supersedes the 16 Oct training-only rule for that session. It is not part of A64, and it was no longer listed at ~07:56 UTC.
- pid 69232: gcloud IAP tunnel to od-cpu1, up 2h11m.
- T41 (36138) and T42 (38063), named in the T45 report, are no longer running.
