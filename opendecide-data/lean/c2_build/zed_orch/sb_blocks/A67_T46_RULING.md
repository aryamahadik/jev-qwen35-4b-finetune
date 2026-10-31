# A67 (T46) full text

Ruling A67 (draft; 17 Oct 2026; orchestrator ruling author, Opus; T46 DISPOSITION-GATE under A59 (e). No gate, bar, cap or waiver is loosened. Nothing is relabelled. Drops only.)

(a) The count. A59 (e) allows one fix iteration after iteration 0, on the generator and templates only. It uses A42-D 3.6's terms: the first failed gate evaluation is iteration 0, and every later change to the generator, templates or pools is a counted fix. The method is A64 (b)'s: rounds before a pass count, and an unclear record takes the higher count. A59 step 5 also sends pre-row check failures into the same single round. The records show:
- E0, 04:19 UTC, in memory, stand-in pools: 6,000-row G6 failed at seed base 3,000,000 (choice/c_card_without_question/lr +3.26 pp; b_options/lr +2.51) and at 12,000,000 (+3.42). A "v2" generator followed at 04:46 UTC. Files: scratchpad t46/g6_out1.txt 30427b5f…, g6_out_12000000.txt ddfb70b4…, g6_v2_3M.txt e42581ca….
- 06:32 UTC dry run (pools 4dd4c79b): G6 and G10 failed (t46_dry.json 63b0c9f7…).
- r6, 06:46 UTC: a full generation through gen_full_c2 (dry=False, written). 1,800 candidates at base 2,000,000, QC base 3,000,000, G0 b02171fd, candidates sha 5ca5cbed…. The A50 mean FAILED: choice/c_card_without_question/lr +2.385 pp and choice/d_meta/gbt +2.14 pp. The G0-lite targets were not met: 1 of 6 workflows, 4 label sets, 0 Arabic rows, 12 cards, 232 rows on one card.
- r7a, 07:06 UTC: a full generation after the pools were re-frozen (bfed79c6). 1,801 candidates, sha b8770766…. The A50 mean passed (worst +0.58 pp). The binding G0-lite (A59 c) was not met: 5 of 6 workflows (no hr) and 6 label sets, below the 8 required.
- r8a, 07:29 UTC: a full generation after the pools were re-frozen again (54b336b6), tables.py changed and G0 was re-pinned to bb739b2c. 1,802 candidates, sha 543a7009….
- r8b, 07:48 UTC: a full generation after plugin.py changed (length-rank gold) and G0 was re-pinned to 77c3b241. 1,800 candidates, sha 0c9ef306….
The least strict count, using full-generation rounds only: iteration 0 = r6, fix 1 = r7a, fix 2 = r8a, fix 3 = r8b. The strict count, which includes pre-row evaluations: iteration 0 = E0, then 5 or more fixes. The higher count binds. Both counts are above 1.

(b) r8a was a binding full-generation evaluation, but it was not the first: r6 and r7a were full generations with the same tool and the same seed bases. Its binding results passed: the A50 mean (B0 + the scratch a50_r8a builds) had worst cell choice/b_options/gbt +0.48 pp. Its G10 longest-option miss (2.11 vs 2.0 pp) is report-only on candidates (A49 c; A59 e: G10 binds on the selected rows). So r8a opened no fix round. r8b is not a legitimate counted fix round, for two reasons: no iteration was left, and it answered a non-binding result.

(c) T46 moves to C3 now (A59 e; A42-D 3.6). Its last allowed iteration was r7a under the least strict count, and r7a failed the binding G0-lite. Under the strict count, the round was used before any real-pool row. A49 (d) / A52 (d) give the same answer: r6 failed a binding gate, r7a was the one fix round, and r7a failed. The Mon 19 Oct 12:00 UTC gate deadline and the 23:59 UTC pilot verdict no longer matter. For the record only: the r8b A50 mean would pass (worst choice/d_meta/gbt +1.30 pp with B0 = 3,000,000, +1.34 pp with B0 = 900,000). This admits nothing.

(d) The G0 amendment 77c3b241 (section 1, gold drawn by label-length rank) changes the generator, not a bar. The G10 bar (±2 pp of 1/k) is unchanged. It is still not confirmable for C2:
- it came after a gate result, and that result was report-only;
- it is a counted fix, and none was left;
- A59 (c) requires the orchestrator to confirm G0 before the first row. The 77c3b241 rows (r8b) and the bb739b2c rows (r8a) existed before any confirmation, and no confirmation record was found for b02171fd either.
It may be kept only as a C3 draft. Report: the change moved the choice/d_meta/gbt mean from −0.15 pp (r8a) to +1.30 pp (r8b), and it was positive in all 4 builds.

(e) What follows. All of it is drop-only.
- No T46 row, replay unit, own dev or Arabic row enters C2. T46-ar = 0 under the 1,500 cap. data/c2_parts/T46 stays absent: t46_install.py is not run.
- No A50 aggregate is written to a T46 QC record. No G5-H, G3-H, 3.4, G9, selection or pilot runs for T46; the $0.30 pilot is not spent.
- T46 leaves the G13 seed command. The JOB3 probe stays a report-only C2-side G13 dev target (A59 g).
- The A59 (i) bench labels are not applied.
- mix_c2 re-runs its asserts without T46.
- GO #1 states, neutrally: "T46 → C3 (A59 e: fix count ≥ 3 against 1 allowed; iteration 1 failed G0-lite)".

(f) Records and program fixes (tool fixes that implement pre-registered rules):
- The QC records' fix_iterations = 1 is a constant taken from gen_full_c2 RUNNER, not a count. Any T46 record must state ≥ 3 and pass=false.
- mix_c2 FIX_MAX_BY_FAMILY lacks "T46": 1, so the default of 2 applies. Add it, with a test.
- The r6, r7a and r8a per-cell A50 files in zed_orch/a50_vm_t46/ were overwritten. The r7a and r8a outputs exist only in the session scratchpad (a50_old 4906c1ed…/f99096f4…/f8e652ac…, a50_r7a_stale 6f425376…/1d5d6ab2…/0f2169be…, a50_r8a ccbfed75…/c5d6c9ef…/b2f3a1a3…, T46_r7a GEN_REPORT 70d958cf…, T46_r8a GEN_REPORT d33b09c8…). Copy them into c2_build with a sha log.
- HANDOFF lines 104-106 ("r8a FAILED → fix") need correcting by the orchestrator.

(g) C3 follow-up:
- fresh seed bases;
- all pool admission finished before a recorded G0 confirmation, and that confirmation made before any row;
- the d_meta signal from the length-rank draw;
- the yes/no a_question G6 view, which is 8-11 pp below chance in every build (inverse artifact under GroupKFold by card);
- the realised conflict share, 11.6% against the 15% target;
- the G3-H "not applicable" claim, confirmed in G0;
- the full A59 (e)/(f) gate kit at unchanged bars.

(h) Unchanged: A42-D and A43-A66, every bar and cap, the $40 and $34 caps, both GO points, and the never-open rules.

## basis
A59 (e), full text sha256 e4146694… (it matches PREREG): "At most one fix iteration after iteration 0, on the generator and templates only. This is stricter than A42-D 3.6's two, and matches A49 (d) and A52." It names G0-lite and G6 per A50 (a) as binding, and says G10 is "report-only on candidates, binding on the selected rows, per A49 c". A59 step 5: "On any failure: one fix iteration (generator or templates only, same seed bases), then T46 moves to C3 if it still fails." A59 (c): "the orchestrator confirms G0 before the first row", with targets of 6 workflows and at least 8 label sets. A42-D 3.6: "The first failed gate evaluation is iteration 0; fixes are iterations 1 and 2 … A family that still fails any gate … moves to C3." A64 (b): iteration counts come from build records, pre-freeze rounds count, and an unclear record takes the higher count. A49 (c)/(d) and A52 (d): one fix round after a failed binding full-generation gate. A50 (a): the mean of four 6,000-row builds binds, and a single build does not. A62 (a): no new gate evaluation after a result. A64 (i): only the owner changes a gate after a result. Precedents: A62 (T27), A65 (T35), A52 (a) (T37b). Evidence I read or computed (read-only):
- The r6/r7a/r8a/r8b logs and GEN_REPORTs: spec_id per row (b02171fd ×2 rounds, bb739b2c, 77c3b241), pool manifests 4dd4c79b → bfed79c6 → 54b336b6, and workflow, label-set and card counts per round from meta.t46.
- A50 means recomputed from B0 plus the 11M/12M/13M build files of each round. The 900,000 skeptic build also gives the r8b mean.
- gen_full_c2 RUNNER["T46"] = ("run_pilot_i1", 1) is hard-coded.
- mix_c2 FIX_MAX_BY_FAMILY has no T46 entry.
I opened no ohs or sealed path. I did not read the a1_* scratch outputs.

## conditions
This is binding for C2. T46 is out, and every condition below is drop-only bookkeeping.
1. Do not run t46_install.py. Do not create data/c2_parts/T46. Do not run the A50 aggregate --write, G5-H, G3-H, 3.4, the crowd read, selection or the A59 (f) pilot for T46.
2. Take T46 out of `g13_c2.py seed --ohsac-only --block …`. Keep the JOB3 probe as a C2-side G13 dev target. Its C1 read stays report-only in the next free od-l4b window; nobody stops the VM for it.
3. mix_c2: re-run every A59 (h) assert without T46. T46 replay unit = 0 rows (check that tag_replay_unit handles 0). The Arabic cap total is SB4 0 + SB5 + T46 0.
4. Program fixes, each with a test and a skeptic review before use:
   - add FIX_MAX_BY_FAMILY["T46"] = 1;
   - no T46 QC record may say fix_iterations 1 or pass=true. Any record written states ≥ 3 and pass=false, with reasons.
5. Copy the scratchpad records (a50_old, a50_r7a_stale, a50_r8a, T46_r7a_vm_out_stale, T46_r8a_stale, t46_dry.json, t46/g6_*.txt) into c2_build with a sha log before the scratchpad is cleaned. The orchestrator corrects HANDOFF lines 104-106.
6. GO #1 reports the A67 (a) count table, the r8b A50 numbers marked as a report, and "T46 → C3". The System One Bench disposition suites are not labelled in-family after C2.
7. C3 only: G0 77c3b241 and pools 54b336b6 are an unconfirmed draft. They need fresh seed bases, a recorded G0 confirmation before the first row, the (g) items examined, and the full gate kit at unchanged bars.
