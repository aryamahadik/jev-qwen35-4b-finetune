# yn2b wave 1b status (1 Oct 2026, about 10:00 UTC)

**Short version.** All six wave-1 families are built and checked. The devx set is built, and so are arms A, B and C
(from the 2-view 4B-E teacher file).
- **Five families are GREEN:** F1, F2, F4, F5 and F6.
- **F3 needs an owner decision.** It breaks one SPEC rule whichever way it is built (section 6, decision 1). The
  files on disk use the build that passes decontamination. It misses the yes-share band in 2 small strata.
- **Labels:** decide2 (or R's parse-back for devx) agrees with gold on 100% of rows in every family.
- **Blind solves:** 98-100% in every family.
- **Decontamination:** 0 units dropped. OHS-3: 0 hits (counts only). `check_unseen`: PASS.
- **Nothing is committed.** No GPU or model was used. No tracked file was changed.

Only CPU work. Labels come only from the families' programs.

## 1. Checks I ran for this summary

All of these were read-only, from `lean/`.

**sha256 values.**
- All 22 files listed in `yn2b/yn2b_summary.json` match the disk. That covers the assembled train, dev and devx files,
  the relations, the arm files A/B/C, `S_units` and every report.
- `golden_src/gen3/MANIFEST_yn2b.jsonl` has 237 records (sha256 `50d6e071…`). For each of the 93 paths in it, the
  latest record matches the file on disk; 1 of them is a directory record.

**Row counts.** I counted the rows on disk:

| File | Rows |
|---|---|
| train | 18,359 |
| train relations | 4,958 |
| dev_iid | 958 |
| dev_holdout | 986 |
| dev relations | 491 |
| devx | 500 |
| arm A | 62,995 |
| arm B | 72,125 |
| arm C | 72,125 |
| arm A relations | 9,308 |
| arm B relations | 11,816 |

- Arm B has 9,130 yn2b rows. By family: F2 2,594, F1 2,121, F3 1,785, F5 1,124, F6 782, F4 724.
- No F3 ladder row is in the train file or in arm B.

**Tests.** `PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider --basetemp=<scratch>
yn2b/tests`: **1,231 passed, 1 skipped, 0 failed** (7 min 10 s). The skip is
`test_v3_state_track_written.py:95` ("not the pinned build"): builder B's F3 test is still pinned to the old F3 build.

**No writes.**
- I took sha256 snapshots of `yn2b/`, `golden_src/gen3/`, `yn2b_raw/`, `yn2b_defs/`, `yn2b_ab/` and the 3 top-level
  dev files before and after the tests (8,572 files). They are identical. The only addition is this file, which I
  wrote while the tests ran.
- `git status` still shows only the 6 tracked files that were already modified at the start.

**Hashes for the amendments.**
- `yn2b/SPEC.md` is `dd50cd9f…` and `DECISIONS_owner_30sep.md` is `76a9d8cc…`. Both are unchanged since the A1 draft.
- `yn2b/ab_readout.py` **has changed** since the draft: it was `88727a53…`, it is now `ba0141fc…`, because it now reads
  the split dev files. A1 part 1 must be re-hashed.

## 2. Gate table (all families and devx)

| Family | Train / dev rows | decide2 (train, dev) | R2 review | Blind solve | Shortcuts | Decontamination | Status |
|---|---|---|---|---|---|---|---|
| F1 rule_chain | 4,257 / 441 (206 iid + 235 holdout) | 4,257/4,257, 441/441 | GREEN after 7 generator fixes (first build RED) | 100/100 (100/100 before the fixes too) | TF-IDF 0.50 / 0.50; best named solver 0.28; every cue rule now 25-58% | clean | **GREEN** |
| F2 tool_guard | 5,202 / 524 | 5,202/5,202, 524/524 | GREEN (wave 1a) | 130/130 | best 54.7%; TF-IDF 51.5 / 48.9 | clean | **GREEN** |
| F3 state_track | 3,780 raw → 3,590 assembled / 349 raw → 329 | 3,780/3,780, 349/349 | GREEN on the full build | 99/100 before the fixes, then 100/100 twice | none above 60% | clean **only without the ladder view** | **OWNER DECISION** (section 6, item 1) |
| F4 polarity_ladder | 1,500 / 300 | 1,500/1,500, 300/300 | GREEN after 5 fixes | 98/100 in both rounds; 0 generator bugs (all 4 misses are debatable human labels) | TF-IDF 44.7 / 42.3 (half→half), 56.7 / 52.7 (train→dev); one cue at exactly 60.0% | clean | **GREEN** |
| F5 lead_score | 2,160 / 200 | 2,160/2,160, 200/200 | GREEN (wave 1a) | 99/100, then 120/120 | best named solver 54.7% | clean | **GREEN** |
| F6 def_literal | 1,650 / 150 | 1,650/1,650, 150/150 | GREEN after 5 fixes | 100/100 twice, plus a 30/30 ambiguity hunt | best 54.6%; TF-IDF 50.8 / 50.0 | clean | **GREEN** |
| devx (reviewer R) | 500 (100 each: F1, F2, F3, F5, F6) | R's parse-back 500/500, 0 fact mismatches | – | 250/250 (50/50 per family), **but solved by R, who wrote the renderers** | report-only checks; the tiers check fails by design | clean | **GREEN, with one caveat** (section 7, item 1) |

- **decide2 re-run (1 Oct).** Builder E re-ran every family's decide2 on the current raw rows
  (`yn2b/decide2_rerun_1oct.json`). Every family's report names the current build.
- **Artefact probe on the assembled files** (|corr(gold, x)| < 0.05 for length, format, tier, polarity and card).
  - It passes on train for all 6 families (worst 0.034, F3).
  - On dev it fails only for F3: `table:md` format 0.095, on 150 rows. Dev is report-only.
- **mv_core checks as assembled.** They pass on train and dev for F1, F2, F4, F5 and F6. F3 fails balance on train
  (section 6, item 1). F3's small dev also fails artefacts, balance and cards (report-only).

## 3. Totals

**Train, as assembled** (`data/v14_parts/yn2b_ab/yn2b_train.jsonl`, `48a2bf0f…`):

| Family | Rows | Yes/no | Choice | JB-letter | Score | Latents | Attacked | Yes share | SPEC target |
|---|---|---|---|---|---|---|---|---|---|
| F1 rule_chain | 4,257 | 2,713 | 1,343 | 201 | 0 | 1,938 | 322 | 0.498 | 4,000 + 8% attack |
| F2 tool_guard | 5,202 | 3,625 | 1,062 | 515 | 0 | 2,758 | 201 | 0.500 | 5,000 |
| F3 state_track | 3,590 | 1,670 | 1,007 | 150 | 763 | 1,707 | 280 | 0.501 | 3,500 |
| F4 polarity_ladder | 1,500 | 1,500 | 0 | 0 | 0 | 750 | 0 | 0.501 | 1,500 (750 F4(a) on human rows in S) |
| F5 lead_score | 2,160 | 324 | 0 | 108 | 1,728 | 1,061 | 160 | 0.500 | 2,000 |
| F6 def_literal | 1,650 | 1,250 | 300 | 100 | 0 | 770 | 150 | 0.500 | 1,500 + 10% attack |
| **Total** | **18,359** | **11,082** | **3,712** | **1,074** | **2,491** | **8,984** | **1,113** | **0.4995** | |

**Train relations:** 4,958 (complement 1,303, equiv 2,542, inv 1,113).

**Dev and devx:**

| Family | dev_iid | dev_holdout | devx |
|---|---|---|---|
| F1 | 206 | 235 | 100 |
| F2 | 263 | 261 | 100 |
| F3 | 164 | 165 | 100 |
| F4 | 150 | 150 | – (the SPEC has no F4 devx) |
| F5 | 100 | 100 | 100 |
| F6 | 75 | 75 | 100 |
| **Total** | **958** | **986** | **500** |

| Split | Yes/no | Choice | JB-letter | Score | Yes share |
|---|---|---|---|---|---|
| dev_iid | 628 | 159 | 60 | 111 | 0.500 |
| dev_holdout | 642 | 174 | 59 | 111 | 0.494 |
| devx | 208 | 134 | 50 | 108 | 0.500 |

- **Dev relations:** 491.
- **G1 uses 986 holdout rows.** SPEC 6 expected about 1,075 holdout rows out of 2,150 dev rows; the dev files are
  about 10% smaller.

**Files and sha256:**

| File | sha256 |
|---|---|
| `data/yn2b_dev_iid.jsonl` | `5bf76985…` |
| `data/yn2b_dev_holdout.jsonl` | `5bc63b10…` |
| `data/yn2b_devx.jsonl` | `a011a551…` |
| `data/v14_parts/yn2b_ab/yn2b_relations.jsonl` | `39a56113…` |
| `data/v14_parts/yn2b_ab/yn2b_dev_relations.jsonl` | `2cc384c2…` |

## 4. Decontamination (SPEC 7, final run on the written files)

| Check | Result |
|---|---|
| 7.1: 12-word runs vs held-out text (OHS-1/2/3, eval sets, JevBench public, v1.5.4) | 0 units. OHS-3 was loaded in memory: 0 hits, counts only |
| 7.2: 12-word runs vs every dev and eval split | 0 |
| 7.3: 6-word template clashes (dialogue_rebuttal, v11 templates, ship-split instructions, OHS-1/2, eval injected spans) | 0 |
| 7.3: banned words | 0 |
| 7.3: marker violations | 0 |
| 7.3: cue share (limit 60%) | All pass. Worst: F1 "fail" 48.8%, F6 "definitions" 44.3%, F4 "passage" 41.3% |
| 7.4: `check_unseen` | PASS: 17 sources, 3,847 rows, 0 flags |
| 7.5: exact dedupe (within yn2b and vs golden_train) | 0 |
| 7.6: dev vs train | At most 8.7% shared 12-grams with any single train state (limit 20%). No iid state equals a train state |
| 7.7: names | 32,664 checked, 0 found in JevBench or OHS-1/2, 0 OHS-3 hash hits |
| Units dropped | **0** |
| devx alone (`yn2b/devx_decontam.json`) | ok; at most 0.97% overlap with any train state |

**The check tool was changed after its first run. This must be disclosed in A1 part 2.**
- **Run 1** dropped 90 F3 units as held-out hits (OHS-3: 0).
  - All 90 came from short options ("0", "5", "none of these") that were matched as whole texts.
  - Fix: a text under 12 words now counts as a match only if it has 4 or more words.
- **Run 1 also found 7 F1 organisation stems** in held-out text, with 9 OHS-3 name-hash hits (counts only).
  - The stems are ordinary words: Helix, Heron, Mason, Gaman, Minor and others.
  - No F1 row shows a stem on its own, so names are now checked in the form the rows show (for example "Heron
    Energy").
- No rows were changed for either fix. Runs 1 and 2 are kept as `check_yn2b_report_run{1,2}.json`.

## 5. Arm files (from the 2-view 4B-E teacher file)

- **Teacher file:** `data/v14_parts/train_2b_golden_kd_2view.jsonl` (`1d44fd63…`). `teacher_src` is q35_4b_E2v
  (2-view average on choice rows, a single view on yes/no rows).
- **Excluded from S:** the 73 A4 bug rows (`--exclude-ids`), which removes 4 rows from S. None of the 4 had a
  relation in S.
- **S** is unchanged: 44,029 units, `S_units` `bceddab4…`.

| | A (control) | B (+ yn2b half) | C (B + teacher gate on S) |
|---|---|---|---|
| Rows (choice / yes-no) | 62,995 (22,380 / 40,615) | 72,125 (26,065 / 46,060) | 72,125 |
| Units | 44,029 | 48,304 | 48,304 |
| yn2b rows | 0 | 9,130 (12.7% of the file; 3.6× the production share) | 9,130 |
| kd targets / kd_full | 56,405 / 32 | 56,405 / 32 | 52,536 / 32 |
| Relations (comp / equiv / inv) | 4,694 / 236 / 4,378 | 5,363 / 1,511 / 4,942 | B's file |
| One-pass steps (batch 16, seed 20260925) | 3,820 | 4,358 | 4,358 |
| `epochs` | 0.9702357329946821 | 0.9667660311958406 | 0.9667660311958406 |
| sha256 | `2df0dcd7…` (rel `a2a3e3cc…`) | `5e777c51…` (rel `9baef45e…`) | `fe2761bc…` |

- **The yn2b half per family:** selected latents 48.3-51.6% (rule: ±5% of half). F2 1,368 of 2,758, F1 961 of 1,938,
  F3 852 of 1,707, F5 547 of 1,061, F6 376 of 770, F4 362 of 750.
- **Arm C's gate** removed 3,869 teachers (2,220 yes/no, 1,649 choice). In-scope yes/no targets inside 0.2-0.8 fell
  from 36.3% to 14.0%. One gen_tables known-bad row was kept out of the gate.
- **Config patches** are in `yn2b_ab_{A,B,C}_counts.json`: name, train_file, rel_file, epochs, expect_kd_targets and
  expect_kd_full. Arm C uses B's relations file. `expect_trainable` stays 33,638,400 (the 2B smoke).
- **The old arm A was overwritten.** It was the 1-view build: 62,999 rows, 56,404 kd targets, 3,820 steps.

## 6. Decisions the owner must make

1. **F3 (the blocker for arm B).**
   - **With the ladder view** (190 negated train questions + 20 dev), the 7.3 cue-share rule fails. The words
     "below", "than" and "other" appear only in negated questions: 30, 96 and 68 rows, 100% each, against a 60%
     limit. They do not predict the answer; F3's own gate measured 50%.
   - **Without it** (the files on disk), 2 train renderer strata of 46 rows each fall outside the 45-55% yes-share
     band:
     - `markdown|iso`: 26 of 46;
     - `log:chrono|space`: 19 of 46.
     - The allowed range is 21-25, so they miss by 1 and 2 rows.
   - **Choices:**
     1. Accept the small balance miss (the current files).
     2. Keep the ladder view and waive the cue-share rule.
     3. Rebuild arms B and C without F3 by adding `--drop-families gd_gen3_state_track` (about 15 s). This drops 1,785
        rows, 20% of the new rows.
   - **My recommendation: choice 1.**
     - It is the smallest break: 3 rows across 2 of F3's strata.
     - F3's assembled train probe stays under 0.05 (worst 0.034).
     - Choice 2 waives a decontamination rule.
     - Disclose the choice in A1 part 2.
   - The real fix is in F3's generator, together with builder B's decide2 parser for any new wording. That is a later
     job.
2. **The G2 pass rule** (wave 1a issue 4; draft A1 part 1, item 6).
   - As written (pooled point ≥ 0.0), it fails a harmless addition about 50% of the time. On the same-recipe null pair
     it gives −0.24, a FAIL.
   - The draft recommends a point ≥ −1.75 pp: 1.9 bootstrap SDs, as strict as NR1-NR3, with about 2.7% false fails.
   - If adopted, change `T["G2"]` in `yn2b/ab_readout.py:40` (and its test) before A1 part 1 is hashed and committed.
     The code still has 0.0.
3. **Teacher conditions** (draft A1, item 2). Do PREREG §6 (c) (+1.0 pp on dev-select) and (d) (the memorisation
   check) still apply under D3? The draft keeps (d) and drops (c).
4. **A4: the 12 gen_tables rows.** Keep them (the default; they are already kept out of arm C's gate) or drop all 85.
5. **A0** (adoption of PREREG_FINAL.md and its freeze record). It must be committed before the 4B scoring job, about
   17:00 UTC today.
6. **Hardware fallback.** If the L4 heavy smoke does not fit 16384 tokens, all arms move to the Modal H100 (about
   $28-29). That puts the reserve under the $40 floor if a relabel ($23) is also needed (draft A6). Decide which gives
   way first: the reserve, arm C (−$10), or the optional 4B top-up.
7. **Second L4 VM** (DECISIONS allows one if quota permits). It would cut the A/B from about 45 L4-hours to about
   16 h of wall time.

## 7. Open items (no decision needed; they must be done before A1 part 2 or the 2B run)

1. **devx blind solve is not independent.** R wrote the renderers and also solved the 250 rows. SPEC 8.5(b) wants a
   fresh R2 (no generator code, no gold) to blind-solve 50 devx rows per family. This is CPU only.
2. **Two decide2 programs were edited by the generator side.** That weakens the two-program rule.
   - F4: the F4 builder changed two frame strings in builder C's `v3_polarity_ladder.py`. C should re-check them.
   - F6: the F6 builder changed builder A's `v3_def_literal.py` grammar for the new one-sentence-per-exclusion form.
     A should re-check it. F6's decide2 also shares the `dl_packs` surface data with the generator.
3. **Builder C's F2 decide2 crashes on devx rows** (KeyError `'assistant'`: the devx renderer uses other JSON keys).
   Train and dev are 100%. devx labels are covered by R's parse-back, which is the SPEC 8.1 second program for devx.
4. **One test is skipped:** builder B's F3 test is still pinned to the old F3 build.
5. **Cross-agent test edit.** The F1 builder edited E's `test_v3_rule_chain_written.py`. Its 5 hand-read rows are now
   frozen in `yn2b/tests/f1_brief_rows.json`, because regeneration reused their ids.
6. **`merge_yn2b.py` is not ready for the 2B main file.**
   - It has no `--exclude-ids`, which A4 needs.
   - Its `--yn2b` default is the old path. The assembled file is `v14_parts/yn2b_ab/yn2b_train.jsonl`.
   - `--expect-kd` must be the 2-view (or teacher-gated) count after A4, not 449,957.
   - Fix it in the 2B worktree before the merge.
7. **V14_KEEP** (`modal_od.py:55`) holds only `train_2b_golden_kd.jsonl`.
   - The 2B main config's train file, `train_2b_golden_kd_2view.jsonl`, is not in it.
   - The arm files sit in the `yn2b_ab/` subfolder, which Modal skips.
   - Both are needed for the H100 fallback and for the 2B main run. Fix in the 2B worktree.
8. **Unit size.** 21 golden units in S already exceed the SPEC 4.9 unit size. This predates yn2b and is unchanged.
9. **Paths differ from SPEC 9** (owner decision on issue 6). The train file and the train and dev relations live in
   `data/v14_parts/yn2b_ab/`. Dev is split into `yn2b_dev_iid` / `yn2b_dev_holdout`. The SPEC 8 outputs are
   `yn2b/yn2b_checks.json` and `yn2b/yn2b_summary.json`, not `logs/`.
10. **Small points:**
    - F4(a)'s mix shifted: storm ratings 132 → 28, slur usage 34 → 100, disease 96 → 128. The ladder split is 379/371.
    - F4 dev has small-sample cues: outside rule 87.5% (16 rows), tool output 62.5% (32 rows).
    - F1: 201 rows have a plausible zero quantity.
    - F6: 4 dev rows have a tenant's "child" older than 60, and 8 definitions carry 3 exclusions (SPEC says 0-2).
    - Orphan definition files in `yn2b_defs/` are harmless: the assembler loads only the files rows reference.

**Wave 1a issues, now:**

| # | Issue | Now |
|---|---|---|
| 1 | F3's fixed build not in `data/` | **Closed.** Raw train `bfaa171f…`, dev `5f894a42…`; decide2 100% |
| 2 | Arm A depends on D3 | **Open.** The arms use 4B-E (2-view). A new 4B teacher means relabel + rebuilding A, B and C (S and the yn2b half stay) |
| 3 | gen_numeric_dates bug rows | **Closed for the arm files** (A4 rows left out). Open for the 2B main file (item 6 above) |
| 4 | G2 noisy | **Open:** decision 2 |
| 5 | Modal cannot see the arm files | **Open:** item 7 (the L4 does not need it) |
| 6 | Dev-file paths | **Closed** by the owner decision |
| 7 | Stale decide2 reports | **Closed.** All six reports name the current build |
| 8 | Orphan definition files | Harmless (assembler loads by reference) |
| 9 | F2 shares below SPEC (JB fallback 16.5%, attack 7.3%) | Unchanged; reported |
| 10, 11 | F3 / F5 minor points | Unchanged. F5's §7 checks have now run, and they are clean |
| 12 | devx blind solves | Done (250/250); independence caveat in item 1 |

## 8. Next steps for the A/B on the Google L4

GPU steps need the owner's GO. The order follows SPEC 11-13, DECISIONS and the drafts in
`prereg_drafts/AMENDMENTS_1oct.md`.

**A. CPU, now (no GPU)**
1. Owner decisions 1-5 (section 6).
2. **If F3 choice 3:** rebuild arms with `--drop-families gd_gen3_state_track` (command in `yn2b/TOOLING_NOTES.md`),
   then re-run `write_checks.py`.
   **If choice 2:** re-assemble without `--drop-views`, record the waiver, then re-run `check_yn2b` and rebuild B and
   C.
3. Fresh-agent checks (items 1-2 of section 7): the independent devx re-solve, C on the F4 decide2 strings, and A on
   the F6 decide2 grammar.
4. **Teacher (D3).**
   - The 4B main run was at step 21,200 of 30,457 at about 09:45 UTC, at 2.84 s/step. It should end at about
     17:00-18:00 UTC, after one more relay.
   - Commit A0 first, then run its ship look vs 4B-E.
   - **If it SHIPS** (plus decision 3's conditions):
     - relabel the 422,044 rows on Modal (choice rows twice, about 5.6 h, about $23, GO);
     - run `build_2b_kd` to make the new 2-view file;
     - run the teacher gate / label audit;
     - run `build_ab_yn2b.py --arms A,B,C --kd-file <new file> --teacher-src <new name> …` with the other flags as in
       TOOLING_NOTES;
     - run `write_checks.py`.
   - **Otherwise** the current arm files stand.
5. **Commit to `PREREG_FINAL.md` before arm A:** A2, A3, A4 and A1 part 1.
   - Fill in the G2 and teacher choices.
   - Re-hash `ab_readout.py` (now `ba0141fc…`, or the new hash if G2 changes).
   - Commit `yn2b/SPEC.md` and `DECISIONS_owner_30sep.md` in the same commit, because `yn2b/` is untracked.
   - The relay's frozen-file check covers only `train_decoder.py`, `decoder_io.py`, `prism_x.py`, `writeblock.py`
     and `runs/q35_4b_main.json`, so this commit does not trip it.
6. **Create the 2B worktree** (hard rule 6) at that commit. In it:
   - **Arm configs.** Write `runs/q35_2b_yn2b{A,B,C}.json`: a copy of `runs/q35_2b_main.json` with only the
     `config_patch` keys changed.
   - **A fresh-start launcher for the L4.**
     - `od_gcp.py relay` refuses to run without a checkpoint.
     - `od_gcp.py train` builds its config from flags. Every other key of the arm config would have to go through
       `--arm I --extra '{…}'`: base_revision, dropout, kd_skip_src, kd_full_src, aux_norm, micro_tokens, seed, layout,
       expect_*, ablate_splits, ckpt_every_min and the rest.
     - Either way, a CPU test must show that the resolved config equals the arm config key by key.
     - Train with `--splits ''`. The reads are one separate job.
   - **V14_KEEP:** fix item 7 of section 7, for the fallback and the 2B main run.
7. **Start the L4 VM (GO).**
   - Copy to `~/lean/data/`: the folder `v14_parts/yn2b_ab/` as it is, plus `yn2b_dev_iid.jsonl`,
     `yn2b_dev_holdout.jsonl` and `yn2b_devx.jsonl`.
   - Copy the worktree code.
   - On the VM, check every sha256 against `yn2b/yn2b_summary.json`.
   - Check that the 2B base revision `15852e8c…` is in the VM's Hugging Face cache (A2).
8. **L4 heavy-batch smoke at micro_tokens 16384 (FINETUNE_PLAN 3.6, GO).**
   - Rank the heavy batches on arm B's file (`rank_microbatches.py`).
   - The H100 peak was 25.38 GB reserved; the L4 has 24 GB.
   - If it does not fit: all arms go to the H100 (decision 6). Never use a smaller micro_tokens; that is a different
     recipe (A1 item 3).

**B. GPU (each step needs GO; every arm on the L4, one code commit)**

9. **Arm A** (`q35_2b_yn2bA`): 3,820 steps, about 14 h at about 13 s/step.
10. **Commit A1 part 2 before arm B and before any read.** It holds:
    - the family counts (`yn2b_summary.json`) and the MANIFEST sha256;
    - the dev sha256 values: iid `5bf76985…`, holdout `5bc63b10…`, devx `a011a551…`;
    - decontamination: 0 units dropped, OHS-3 0;
    - `check_unseen` PASS;
    - labels: decide2 100%, blind 98-100%;
    - disclosures: the F3 choice, the check-tool changes of section 4, and the paths.
11. **Arms B and C** (`q35_2b_yn2bB` / `_C`): 4,358 steps each, about 16 h each.
    - On one L4, A, B and C take about 45 h in a row.
    - With a second L4 VM, B and C run in parallel.
12. **Reads: one job for all arms**, on the L4. Use
    `od_gcp.py predict --name q35_2b_yn2b<arm> --base Qwen/Qwen3.5-2B --splits …` on:
    - `dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev`;
    - `eval_jagged,eval_opi,eval_redef`;
    - `yn2b_dev_iid,yn2b_dev_holdout,yn2b_devx`.

    Then read the 9 gate splits again with `--perm-seed 1 --tag _perm`. PRISM-X loads from the adapter. Expect about
    3 L4-hours per arm.
13. **Readout.**
    - Copy the preds back (the pattern of `gcp/score_arm.sh`).
    - Run `../.venv/bin/python yn2b/ab_readout.py --arm-c`. It writes `logs/yn2b_ab.json` and one line in
      `logs/yn2b_ab_looks.jsonl`.
    - One A/B, one verdict. The readout drops any family whose pooled holdout + devx difference is < 0.
14. **After the verdict.**
    - **PASS:** fix `merge_yn2b.py` (section 7, item 6) and merge (plus arm C's gate only if §11.6 holds and the owner
      approves). Then `replay_steps.py`, commit A1 part 3, and GO for the 2B main run.
    - **FAIL:** the 2B main run uses the 2-view plan-of-record file minus the A4 rows, the same day.

**Rough timing.**
- The 4B ship-look reads are also an L4 job, so arm A starts after them: about 1 Oct night at the earliest.
- The ~13 s/step L4 speed is the SPEC's estimate. It has not been measured on these rows.
- With 4B-E as the teacher, the verdict lands about 3 Oct with two VMs, or 4 Oct morning with one.
- A relabel adds about 6-8 h.
- This fits D4: the 2B main run starts about 4 Oct.

## 9. Key files (under `lean/`)

- **Status and checks:**
  - `yn2b/yn2b_checks.json`, `yn2b/yn2b_summary.json`;
  - `yn2b/check_yn2b_report.json` (+ `_run1`, `_run2`);
  - `yn2b/check_unseen_report.json`, `yn2b/decide2_rerun_1oct.json`, `yn2b/names_check_1oct.json`.
- **Family gates:** `yn2b/r2_{rule_chain,def_literal,polarity_ladder,state_track,lead_score}_{gate,blind}.json`,
  `yn2b/v3_*_agreement*.json`.
- **devx:** `yn2b/devx_{report,blind,blind_answers,decontam}.json`, `yn2b/build_devx.py`,
  `golden_src/gen3/dx_*.py`.
- **Data:**
  - `data/v14_parts/yn2b_ab/` (`yn2b_train`, relations, arm files A/B/C, counts, `S_units`);
  - `data/yn2b_dev_iid.jsonl`, `data/yn2b_dev_holdout.jsonl`, `data/yn2b_devx.jsonl`;
  - raw rows in `data/v14_parts/yn2b_raw/`.
- **Tools changed in wave 1b:**
  - `yn2b/assemble_yn2b.py` (accepts yes/no cards with extra definition lines, `--drop-views`, split dev);
  - `check_yn2b.py`, `build_ab_yn2b.py` (`--exclude-ids`), `ab_readout.py` (split dev);
  - new: `gather_names.py`, `write_checks.py`;
  - notes in `yn2b/TOOLING_NOTES.md`.
- **Amendment drafts:** `prereg_drafts/AMENDMENTS_1oct.md`. A0, A2, A3 and A4 are ready to paste once the owner fills
  in their choices. A1 part 1 needs decisions 2-3 and the new `ab_readout.py` hash.
