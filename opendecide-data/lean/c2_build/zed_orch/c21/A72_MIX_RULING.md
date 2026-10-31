# A72 draft

DRAFT RULING (Opus, ruling author, for the C2 orchestrator). Scope: what the G9 re-read results mean, and the 16 problems in dry run 2. I decided from adopted text only. No waiver, no bar moved, nothing relabelled, drops only. Disclosure: I wrote this after seeing the G9 results and dry runs 1 and 2. I read only counts, shas and row metadata fields (sampler, source, task_id, domain_pack, qtype, gold). I read no row text and wrote no file.

PART 1. The G9 re-read is binding. Its bar depends on what kind of row it is.
Texts:
- Spec 6.3 G9: "Rows with p_g < 0.05 go to the G5-H re-read."
- A27 (b): "a family still needs QC + crowd + G13 + selection + G9 re-read to pass."
- A27 (c): every p_g < 0.05 row "plus 300 seeded selected rows".
- Spec 6.3 G5-H: "Bar: 0 confirmed wrong golds, ambiguous ≤ 1% ... a confirmed wrong gold is a generator bug. Rows are never relabelled | Reader changes (Haiku, then Claude); bar unchanged."
- The unchanged G5 bar (C spec 8): "A confirmed error is a generator bug ... Public and real-text rows: dataset-level decisions only (drop the dataset if > 8% clearly wrong ...), never row by row."
- C spec 2.3, for F11's real-text codebook rows: "More than 8% clearly wrong drops that dataset's codebook rows (a dataset-level decision, never row by row)."
- For MD:
  - A42-D 8.1: "a program turns them into a task with deterministic gold ... Haiku reads blind and flags only (A37 b)".
  - A37 (b): "A Haiku disagreement can only drop a row or quarantine a template."
  - A42-D 8.4: "A task is dropped if more than 8% are clearly wrong ... Rows are never edited."
- For SB5, A58 step 10: "through the step-6 cascade, drop only". Step 6: "Opus confirms every wrong-gold or ambiguous call; only confirmed rows are dropped."
- A43 (d): "Opus confirms every wrong_gold or ambiguous flag before g5h.finalize."
- A62 (a): a quarantined subset "is not admitted (that would be a new gate evaluation after a result); no refill."

How I read these texts:
- **Program or constructed gold:** 0 confirmed wrong golds, or the generator has a bug. Ambiguous must be ≤ 1%, counting only Opus-confirmed flags.
- **Real-text rows with upstream, human or Claude labels:** only the dataset-level "> 8% clearly wrong" bar applies, never row by row. MD is judged at its own task unit (8.4). SB5 follows A58's drop-only rule.
- **The rate:** computed over all re-read rows (the A27 (c) sample, including the low-p_g rows). This is the stricter basis. Rates on the seeded sample alone are reported only.
- **The reread agent's claim that the bar is "report-only" is rejected.** The G9_RESULT note only says that the scorer changes no data. g9_score.py itself names the bar.

Process gap: g9_score sent only wrong-gold flags to Opus. So every "ambiguous" count is Sonnet's first pass. The one exception is F11's 19 ambiguous verdicts, which Opus gave on wrong-gold flags. Finishing the A43 (d) confirmation is a step the rules already require; it is not a new one.

Outcomes:
- **T07 fails G9.** Its confirmed row (c2_t07:39e629fb…) is a Mode-T choice row from sampler S3: a generator bug.
  - T07 leaves the C2 mix. No subset is admitted and nothing refills (spec 5.3).
  - It could come back only through a counted fix iteration, if its build records show one left (A64 b; the QC record says 1 of 2 used). Every gate would then have to pass again by Mon 19 Oct 23:59 UTC. This mix does not assume it.
- **F11 stays, without MAMS.**
  - All 25 confirmed wrong golds (and all 134 Sonnet flags) sit in sampler S7, the real-text codebook rows.
  - The 353 reads of program samplers S1-S6 show 0 flags, so the program part passes and there is no generator bug.
  - MAMS: 20 wrong of 138 read = 14.5%, above 8%. Every MAMS codebook row leaves (seeded-sample rate 3/59 = 5.1%, reported only).
  - XED English: 5 of 151 = 3.3%. It stays.
- **MD stays, minus 2 tasks.**
  - All 4 confirmed wrong golds are in source ROR: 4 of 64 read = 6.25%, at or under 8%, so ROR stays.
  - They sit in 2 ROR tasks (1 and 3 wrong; 26 candidate rows each). Both tasks are quarantined whole.
  - The other 10 sources show 0 wrong golds.
- **Ambiguity:**
  - Binding on program and constructed-gold rows. No program family has a flag; GW has 1 of 300.
  - Report-only on F11 S7, MD, GB and I10.
  - SB5: Opus confirms the 19 flags, and confirmed rows are dropped with their units. There is no block-level bar.
  - I10 passes (0 clearly wrong). Its 4 flags go to Opus for the record only.

PART 2. Dry-run problems: see per_item_decision.
Basis for the problems ruled report-only:
- A54 (a): pack IDs are compared, "not domain labels (domains are shared by design)".
- A69 (a): for carry pools and blocks (GB GW MD RTW SB5 I10), "Their A49 (c) checks stay report-only". A49 (c) includes the yes rate, the longest-option share and the spec 3.0 token mean.
- Spec 3.0's "(C2) Length" is a build rule for families built under the C2 spec. Spec 3.19 lists the carry pools' re-gates without it.

These stay binding:
- spec 5.2: "Every new row ≤ 2,000 tokens; the mean of new rows ≤ 800" (pooled), and "New yes/no rows are 45-55%";
- A69 (f)(vi): cap_checks stay binding;
- A42-D 5.5;
- E2;
- spec 5.3: replay = floor(1.5 × new).

Fixes come only from adopted text:
- A42-D 5.5;
- A34 (f)(ii) for E2 cells;
- A34 (b), exclusions before selection;
- A34 (e) for short families;
- A42-D 1.5: "those rows are scaled down (seeded, whole units, in proportion across the families). No cap is raised";
- A34 (f)(i): replay follows new, and the remainder lowers the total.

PART 3. Minimum to train:
- **Agent core:** T26, T28, T29 and T30 are unaffected. T33 counts only if its re-selection, after removing every unit on one of its own mixdev packs, passes every check.
- If T33 fails, the core is 4 of 6: stop and report, no training (spec 5.3, A62 c, A69 f iii, A71 b).
- **Program families:** 13 (T07 out), which meets the floor of 10.

PART 4. Expected mix (estimate; the next dry run gives the binding numbers):
- About 31.5-32.5K new rows. The main cut is about 3.5K yes/no rows to meet the pooled 55% cap.
- Replay is floor(1.5 × new), about 47-48.5K, for a total of about 78.5-81K.
- **Money, against T_core = min(34, 32 − 0, 30.96 − 8) = $22.96:**

| Speed model | Cost |
|---|---|
| mix_c2 padded-token projection | about $17.8 |
| A28 speed, 2.92 s/step | about $18.5 |
| Round 1's measured 3.716 s/step | about $23.0 |

- The pre-launch projection fits, so the A42-D 2.3 trim is not used.
- At round-1 speed the A37 (k) / A42-D 2.3 check (projection at steps 100-300 above T_max) is at the edge and would likely ask the owner.
- The 50K floor, the 125K cap and the $40 / $34 caps all hold.

## per_item_decision
G9 RESULTS
- **T07: OUT.** It fails G9: a generator bug. No subset admitted, no refill. Its mixdev becomes report-only. A fix iteration is allowed only if A64 (b) shows one left, and it is not assumed here.
- **F11: STAYS without MAMS.**
  - Program samplers S1-S6: 0 of 353 flagged, so they pass.
  - S7 MAMS: 20 of 138 (14.5%) is above 8%, so every MAMS codebook row leaves (whole dataset).
  - S7 XED: 5 of 151 (3.3%), so it stays.
  - Re-select F11 under A34 (b).
- **MD: STAYS minus 2 ROR tasks.** The 4 confirmed wrong golds are in those 2 tasks; quarantine both tasks whole. ROR as a source is at 6.25%, so it stays.
- **SB5: STAYS.** Opus confirms its 19 flags, and confirmed rows are dropped with their units (A58). It also still needs its A58 step 11 verdict by Mon 19 Oct 23:59 UTC and an A61 8.5 PASS.
- **I10: PASS.** 0 wrong. The 4 Sonnet flags are report-only; Opus confirms them for the record.
- **GB, GW: PASS.**
- **All other families: PASS.** F4's 7 Sonnet wrong-gold flags and T26's 1 were all overturned by Opus.
- **Ambiguity bar:**
  - Binding (Opus-confirmed, ≤ 1%) on program rows. No program family has a flag.
  - Report-only on real-text rows (F11 S7, MD, GB, I10).
  - SB5 is drop-only.
  - The reread agent's "report-only" claim is rejected for program rows.

DRY-RUN 2 PROBLEMS
1. **GB, 7 cards with yes share outside 40-60%: BINDING (A42-D 5.5).** Fix: seeded down-sampling of the over-represented label inside each card, whole units.
2. **c2_seed_T27 log incomplete: REPORT-ONLY.** T27 is out under A62 (b). Keep its existing drop ids; it gates nothing and is never cited as a pass.
3. **E2, 25 replay wording cells outside 50 ± 5: BINDING.** Fix: A34 (f)(ii), seeded down-sampling of the majority label in each failing cell (≥ 50 rows), whole units, rows only removed.
4. **S7 held-out pack overlap:**
   - **T33 (53 rows): BINDING.** These are real pack IDs: 18 of T33's 19 mixdev packs are also used by its training rows. Fix: exclude every T33 pool unit on a mixdev pack (194 units / 250 rows), then re-run T33's selection under A69 unchanged (A34 b). Newly selected rows get a G9 read first. T33 enters under A34 (e) if every check passes; otherwise stop.
     - A plain drop after selection fails: it leaves 91 rows with yes rate 0.44 and longest-option 4.67 pp.
     - Only 53 choice rows are left off the dev packs, which caps T33 at about 115 rows.
   - **T01 (670) and T23 (298): REPORT-ONLY (A54 a).** All of their domain_pack values are labels, not packs: 28 of 28 in T01 are card-slot labels and 10 of 10 in T23 are domain labels. They share 0 group ids, states or structure hashes with dev.
5. **F11 aggregate yes rate: REPORT-ONLY.** It is an A49 (c) check on a carry pool (A69 a). Re-measure after re-selection.
6. **MD hard cell, yes rate 0.542 (n = 72): REPORT-ONLY** (an A49 (c) check on a block, A69 a).
7. **GB longest-option off by 7.58 pp: REPORT-ONLY** (an A49 (c) check on a block, A69 a). GB's own A39 (e) and A42-D 5.5 rules still bind.
8. **F11 mean 1,200 tokens: REPORT-ONLY** (a carry pool, A69 a; spec 3.0 "(C2) Length" applies to C2-built families). Spec 5.2's per-row ≤ 2,000 tokens and pooled mean ≤ 800 bind. The pooled mean is 613.7 in dry run 2 and about 625 expected.
9. **F11 hard share 0.330: BINDING** (spec 5.2 difficulty, G9 bins). Fix: crowd_select's cap pass, which sheds hard-only units until hard ≤ 30%.
10. **F4 mean 1,512 tokens: REPORT-ONLY** (as item 8).
11. **F5 mean 1,222 tokens: REPORT-ONLY** (as item 8).
12. **F6 mean 1,431 tokens: REPORT-ONLY** (as item 8).
13. **New yes/no share 0.594 against 45-55%: BINDING** (spec 5.2, cap_checks under A69 f vi). After the fixes above it is still about 0.595. Fix: the A42-D 1.5 method. Scale down the yes/no units of the blocks whose own yes/no share is above 0.55 by one common factor. Today those are MD, F5, SB5, F6, GB and GW. Remove units seeded, whole and label-balanced, until the pooled share is ≤ 0.55. That is about 3.5K rows. No program family is touched.
14. **GB cards: same issue as item 1, listed twice.** One fix.
15. **Replay short by 409: BINDING** (spec 5.3). It should clear once replay is redrawn to floor(1.5 × about 32K new). If replay is still short, trim new rows by spec 5.5's proportional whole-unit trim (A34 f i). Never pad replay.
16. **New rows 40.18% of the mix: BINDING.** Same cause and fix as item 15.

FLOOR: agent core 5 of 6 only if T33 passes after its re-selection; otherwise stop. Program families: 13.

MIX: about 32K new, about 48K replay, about 80K total. Cost about $17.8 to $18.5, against T_core $22.96. At 3.716 s/step it is about $23.0, so the stop-and-ask is at the edge.

## fix_spec
Order of work. Use seed 20261013 everywhere. Whole units only. Rows are only removed, never relabelled. Every new or changed tool gets a skeptic review and has its sha256 logged in zed_orch/a64/A64_TOOLS.md before first use.

1. **Finish the G9 confirmation (A43 d).**
   - Change zed_orch/g9_reread/g9_score.py:
     - In `adjudicate`, also write Opus confirmation tasks for Sonnet's "ambiguous" verdicts.
     - In `final`, count as ambiguous only what Opus confirms. Report two numbers: all rows read, and seeded-sample rows only (n_sample).
   - Opus confirms these flags:

   | Block | Sonnet ambiguous flags | Why |
   |---|---|---|
   | SB5 | 19 | Decides the drops |
   | I10 | 4 | Record only |
   | GB | 1 | Record only |
   | GW | 1 | Record only |
   | MD | 7 | Record only |
   | F11 | 134 | Record only |

   - Program families have no flags, so nothing else changes.

2. **Apply the G9 outcomes. Build exclusion id lists.**
   - **T07:** run mix_c2 with `--leave-out T07`. Reason: "G9 re-read: 1 confirmed wrong gold (c2_t07:39e629fb…, Mode T, sampler S3) = generator bug (spec 6.3 G5-H; C spec G9)". T07's mixdev becomes report-only.
   - **F11:** exclude every unit of F11's candidates_r1 that holds an S7 row whose text_source dataset is `mams`.
   - **MD:** exclude every unit of the 2 ROR tasks (meta.task_id) that hold the 4 confirmed ids in fam/MD/G9_RESULT.json.
   - **SB5:** exclude every unit holding an Opus-confirmed wrong-gold or ambiguous row from step 1.

3. **S7 held-out packs.**
   - **T33:** exclude every candidate unit whose meta.domain_pack is in T33's out/mixdev_S5.jsonl pack set. Today that is 194 units / 250 rows of the post-G13 pool.
   - **mix_c2 HeldOut check:** build the pack set with g13_c2.a53_pack_id (A54 a). T01 and T23 labels then stop matching, and T33 stays binding.

4. **Re-select with the step 2-3 lists added to `--exclude-ids` (A34 b).** Settings, constants and tool shas stay unchanged.
   - Re-run: T33 (A69 path) and F11 (`c2_select carry`).
   - MD and SB5 get the same exclusions; their selection is otherwise unchanged (A69 a).
   - **G9 read for new rows:** every row that enters a family's A27 (c) read set and was not read before gets the full G9 read (2 Haiku, then Sonnet, then Opus), with unchanged bars:
     - for T33 that means all selected rows, because it has fewer than 300;
     - for F11, any new rows in its seeded 300.
   - **Admission:** under A34 (e) / A69 (f)(ii).
   - **If T33's record fails, stop and report. No training** (A62 c).

5. **mix_c2 problem labels.** Mark these lines report-only instead of problems, citing A69 (a):
   - the per-block token mean for F4, F5, F6 and F11;
   - the per-block G10 aggregate yes rate and yes-rate cells for carry pools and blocks;
   - longest-option for blocks.
   
   Add a binding line for spec 5.2's pooled mean of new rows ≤ 800 tokens. All other lines stay binding, including:
   - rows over 2,000 tokens, difficulty caps, ordinal / soft / dev rows and the Arabic cap;
   - the pooled yes/no share, A42-D 5.5, A42-D 8.2 and A60.

6. **Mix with C = 30.96. Removal-only fixes, in this order:**
   - **(a) GB cards (A42-D 5.5):** down-sample the over-represented label inside each card that is outside 40-60%.
   - **(b) Difficulty:** run crowd_select's cap pass on any block above hard 30% or easy 25% after refill. F11 is the case today.
   - **(c) Pooled yes/no (A42-D 1.5 method):**
     - Find the set B of blocks whose own yes/no share is above 0.55. Program families are never in B.
     - Use one common factor f. Remove the first (1 − f) × yes/no units from each block in B.
     - Order units by h64(20261013, block, "a42d15-yn", first id).
     - Remove yes and no units in the block's own yes:no ratio: within the card for GB, within the task for MD.
     - Use the largest f for which the pooled new yes/no share is ≤ 0.55.
   - **(d) Re-assert block rules:**
     - A42-D 8.2 via fit_block_in_mix(META);
     - A39 (e) and A42-D 5.5 for GB;
     - A60 pooled twin shares;
     - A58 step 8 for SB5;
     - spec 4.1 / A49 (c) for program families.
     
     Remove only, until nothing changes. Then repeat (c).
   - **(e) Replay:**
     - Draw replay to floor(1.5 × new) through replay_sample and E2.
     - After G13 drops and refills, apply A34 (f)(ii) to every E2 cell of 50 or more rows that is outside 50 ± 5.
     - If replay is still below floor(1.5 × new), apply A34 (f)(i): trim new rows by spec 5.5's proportional whole-unit trim until replay = floor(1.5 × new).
   - **(f) Money:** project with A42-D 2.3 against T_core $22.96. Use the trim order only if the projection is above it.

7. **Final checks:**
   - the binding final-mix G13 under the A68 targets;
   - one A61 (f) 8.5 run on SB5_uci293 and the 11 md_* sources;
   - preflight;
   - SB5's A58 step 11 verdict by Mon 19 Oct 23:59 UTC, otherwise SB5 leaves.

8. **The GO #1 request states:**
   - the G9 table per family: confirmed counts, which bar kind applied (program or real-text), and which basis;
   - T07 out; MAMS out; MD's 2 ROR tasks out; SB5's confirmed drops;
   - the T33 realised rows and agent core 5 of 6, under A71 (b);
   - 13 program families;
   - item 7's realised twins;
   - the OHS-AC report-only counts (A68 d), using the required wording;
   - the A61 G-proxy wording;
   - per-family repair results (A69 j);
   - every report-only line and its basis;
   - cost at 2.92 and at 3.716 s/step, with the A37 (k) note.

Files: c2_build/crowd_c2/g9_reread/fam/*/G9_RESULT.json, key/*.json, fam/*/sonnet_flags.json, crowd_c2/select_T33.json, data/c2_parts/{T01,T23,T33}/out/mixdev_S5.jsonl, scratchpad dryrun_2.json.
