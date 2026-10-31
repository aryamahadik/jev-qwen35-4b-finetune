# yn2b wave 1a status (30 Sep 2026, about 21:05 EDT)

**Short version.** The engine (mv_core) and all the tooling are built and tested. Arm A's control file is built. F2
and F5 are GREEN and their rows are in `data/`. F3 is GREEN only as a fixed build in the scratchpad. The rows in
`data/` are still the old build, which has 10 decide2 disagreements, because the permission system refused the
overwrite. Nothing from F1, F4, F6 or devx exists yet. No check against OHS-3 or decontamination run has been done on
family rows.

Everything is CPU-only. No model was called, and no tracked or frozen file was changed. Since wave 1a started,
`git status` shows only the 6 tracked files that were already modified at the start.

## 1. Verification done for this summary

- **Full yn2b suite:** `PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider
  --basetemp=<scratch> yn2b/tests` was run twice from `lean/`.
  - Result both times: **535 passed, 1 skipped, 0 failed** (about 5 min 20 s).
  - The skip is `test_r2_state_track_review.py:95`: "written rows differ from the gate inputs". This is expected
    until F3's fixed build is written.
- **No writes by the tests:** I took sha256 snapshots of `yn2b/`, `golden_src/gen3/`, `yn2b_raw/`, `yn2b_defs/` and
  `yn2b_ab/` before and after (1,769 files). They are identical, and `git status` is identical. The only file under
  `lean/` that changed during the runs was `logs/main4b_seg2.log`, which belongs to the live 4B relay, not to us.
- **Manifest:** `golden_src/gen3/MANIFEST_yn2b.jsonl` has 83 records. For every path, the latest record's sha256
  matches the file on disk. `yn2b_defs` is a directory record and was not hashed.

| Component | Tests (pass) |
|---|---|
| mv_core | 81 |
| Tools and label audit (builder E) | 44 |
| F2 (generator 31, decide2 106) | 137 |
| F5 (generator 96, R2 review 6, decide2 52) | 154 |
| F3 (generator 58, R2 review 8, decide2 54) | 119 + 1 skipped |
| **Total** | **535 + 1 skipped** |

## 2. Gate table

| Component | Status | Key numbers |
|---|---|---|
| mv_core (engine) | GREEN | 81 tests. decoder_io round trip on 1,000+ toy rows; every card line and option survives; decide2 = gold on 100% of rows; rebuilds are byte-identical. Writes no data |
| Tooling (assemble, merge, build_ab, check_yn2b, check_unseen, ab_readout, teacher_gate) | GREEN | 44 tests. `ab_readout` reproduces the SPEC 11.5 noise table exactly. `merge --validate-only` on the real KD file: kd 449,957, kd_full 238, 74,094 relations valid. `check_unseen` baseline: 0 flags |
| §8.6 label audit + teacher gate (arm C) | GREEN, with 1 flag | 30-row audits by hand: numeric_dates 28/30, evidence_conflict 30/30, tables 29/30 (bar ≥ 27). One generator bug found (section 6, item 3) |
| Arm A file (`q35_2b_yn2bA`) | GREEN (built), conditional on D3 | 62,999 rows; 3,820 steps (section 3) |
| F2 `gen3_tool_guard` | GREEN | Train 5,202 rows (2,758 latents), dev 524 (263 iid + 261 holdout). Yes share 0.50. decide2 5,202/5,202 and 524/524. Blind solve 130/130. Best visible shortcut 54.7%; TF-IDF on dev 51.5% (state + question), 48.9% (question only) |
| F5 `gen3_lead_score` | GREEN | Train 2,160 rows (1,061 latents), dev 200 (100 + 100). decide2 2,160/2,160 and 200/200. Blind 99/100 before fixes (the miss was the solver's slip), then 120/120. Best named solver 54.7%. TF-IDF 56.3% train→dev (only 48 dev rows), 51.8% half→half |
| F3 `gen3_state_track`, rows in `data/` | **RED** | This is the old build (sha `94a9c23d…`). decide2 3,773/3,780 train and 346/349 dev: 10 disagreements |
| F3 `gen3_state_track`, fixed build (scratch) | GREEN, not written | 3,780 train / 349 dev. decide2 3,780/3,780 and 349/349. Blind 100/100. No shortcut above 60%. Sha256 re-checked in scratch: train `bfaa171f…`, dev `5f894a42…`, relations `5bb66624…` / `9f56aef7…` |
| §7 decontamination (`check_yn2b`: 12-gram, 6-gram bans, TF-IDF probes, OHS-3 counts only) | NOT RUN | The tool works, but it has not been run on family rows. F2 ran only `f2_precheck`, which leaves out OHS-3 |
| `check_unseen`, assembly, §8 outputs (`logs/yn2b_checks.json`, `yn2b_summary.json`) | NOT RUN | Waits for the family rows |
| devx (reviewer R) | NOT STARTED | – |
| F1, F4, F6 | NOT STARTED | No `gen3_rule_chain`, `gen3_polarity_ladder` or `gen3_def_literal` file exists yet |

**Rows now in `data/v14_parts/yn2b_raw/`:**

| Family | Train rows | Kinds (yn / choice / JB / score) | Dev rows | Relations (train / dev) | Views (train) |
|---|---|---|---|---|---|
| F2 | 5,202 | 3,625 / 1,062 / 515 / 0 | 524 | 1,431 / 102 | base 2,758, contrast 1,013, format 795, ladder 435, attack 201 |
| F3 (old build) | 3,780 | 1,860 / 1,007 / 150 / 763 | 349 | 879 / 60 | base 1,707, contrast 752, format 409, mirror 292, attack 280, ladder 190, jb 150 |
| F5 | 2,160 | 324 / 0 / 108 / 1,728 | 200 | 481 / 48 | base 1,061, contrast 618, format 321, attack 160 |
| **Total** | **11,142** | | **1,073** | **2,791 / 210** | |

`yn2b_defs/` holds 1,650 content-addressed files.

## 3. Arm A (`q35_2b_yn2bA`, the 4B-E labels)

| Count | Value |
|---|---|
| Rows | 62,999 (choice 22,384, yes/no 40,615) |
| Units | 44,029 of 351,122 (12.54%) |
| kd targets / kd_full | 56,404 / 32 |
| Relations | 9,308: complement 4,694, equiv 236, inv 4,378 |
| Teacher sources | q35_4b_E 47,746; none 12,116; 4B-E clean copy 2,734; human clean copy 403 |
| One pass | 3,820 steps; epochs 0.9701741297480913 (seed 20260925, batch 16, cygnet) |
| sha256 | `yn2b_ab_A.jsonl` `27bce62c…`, `_rel` `a2a3e3cc…`, `S_units` `bceddab4…`, built from KD file `e7b61114…` |

`expect_trainable` still comes from the 2B smoke. The config patch is in `yn2b_ab_A_counts.json`; `runs/*.json` was
not edited.

## 4. Label-audit headline (SPEC 8.6, 4B-E teacher)

- **Share of targets inside 0.2-0.8** (yes/no rows in the gate's scope, 78,923 rows): **36.7% before the teacher
  gate, 14.1% after.** Over all generator yes/no rows it goes from 35.2% to 14.1%.
- **How often the teacher is wrong:** 22.6% of in-scope yes/no rows and 46.5% of in-scope choice rows.

  | Generator | Teacher wrong |
  |---|---|
  | numeric_dates | 41.9% |
  | evidence_conflict | 33.6% |
  | policy_exceptions | 28.8% |
  | tables | 28.4% |

- **What the gate removes:**
  - Full 2B file: 32,317 teachers. kd targets go from 449,957 to 417,640; kd_full stays 238.
  - Arm A's S: 3,949 teachers. kd targets go from 56,404 to 52,455.

## 5. SPEC ambiguities resolved in wave 1a

- **mv_core** (all of them are in `MV_CORE_API.md` §11):
  - Raw yes/no rows keep `["yes","no"]` and string gold; only the assembler makes options null and gold 1/0.
  - Golden ids come from the latent id, not a running index.
  - "45-55% per stratum" means the yes count is within max(5% of n, 1 row) of half.
  - Banned judge words apply to judge rows only.
  - A mirror's option count never depends on whether "none" is gold (this fixes an answer leak).
  - Contrast twins may differ in at most 3 state lines plus the definitions (needed for F6's exclusion twin).
  - Relation files go in `yn2b_raw/relations/` and `yn2b_raw/dev/relations/`.
- **Tools** (all of them are in `TOOLING_NOTES.md` and `label_audit.md`):
  - The gate's scope is taken from SPEC_draft's D1 wording.
  - "Committed" means P(gold) ≥ 0.8 after renormalising over the row's own options.
  - 7.7 "substring" means a whole-word match by default.
  - NR5 caps are fixed at 6.9% / 5.4%.
  - The drop list is stored as salted hashes, so OHS-3 hits cannot be read back.
- **Families:**
  - F2: a prerequisite call by another user in the same session counts (21 rows), and a specific rule beats a class
    rule (46 rows; the policy text says so).
  - F3: unclear rules are now written as rules. Where gold differed from decide2's reading, the generator was changed
    to the literal reading.
  - F5: the gate score is the plain count of gates passed. The unsubscribe penalty is applied after the cap
    (18 rows).

## 6. Open issues (for the owner)

1. **F3's fixed build is not in `data/`.** The permission system refused the overwrite, and it was not worked around.
   To apply it, run these from `lean/` once you approve:
   1. `PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python golden_src/gen3/gen3_state_track.py --write --overwrite`
   2. Check the sha256s: train `bfaa171f…1e68`, dev `5f894a42…3da4`, relations `5bb66624…f0a2` / `9f56aef7…0710`.
   3. `yn2b/r2_state_track_review.py --gate --write`
   4. Optionally `golden_src/gen3/v3_state_track.py --write-report`, which refreshes B's stale agreement file.

   After that, the skipped test should run and pass.
2. **Arm A depends on D3 (the teacher).** Arm A uses the 4B-E labels. If the new 500K 4B passes the ship gate, these
   must be rerun: `build_2b_kd`, `label_audit.py --kd-file … --teacher-src …`, then `build_ab_yn2b.py`. S does not
   change, because it depends only on call_ids and relations, so F4(a) is safe either way.
3. **Generator bug in frozen golden_train (`gen_numeric_dates`).** The choice twins reuse the base row's question,
   which names the wrong city or the wrong instalment. This affects 121 raw rows, 73 rows in the 2B file and 4 in S.
   There are also 12 ambiguous rows from a tables template. The ids are in `yn2b/label_audit_known_bad_ids.json`.
   Pass them with `--exclude-ids` (gate) or `--gate-exclude` (build_ab). The rows themselves cannot be fixed, because
   golden_train is frozen.
4. **The G2 pass rule is noisy.** It fails a harmless addition about half the time: the same-recipe rerun pair gives
   −0.24 in the SPEC's own 11.5 table. It is coded as written. The owner may want to look at it before A1 part 1 is
   committed.
5. **Modal cannot see the arm files where they are.** `modal_od` skips subfolders of `v14_parts`. The 2B worktree's
   V14_KEEP commit must copy the files up or allow the folder.
6. **The dev-file paths conflict.** SPEC 9 says the assembler writes top-level `data/yn2b_dev.jsonl`,
   `data/yn2b_dev_relations.jsonl` and `data/yn2b_devx.jsonl`. The builder brief bans writing top-level
   `data/*.jsonl`. This needs a decision, or the step should run in the 2B worktree, before D3 assembly.
7. **Stale or rewritten decide2 reports.**
   - `v3_lead_score_agreement.json` describes the old F5 data; `_r2` is current.
   - `v3_state_track_agreement.json` describes the old F3 rows that are now in `data/`.
   - F2's decide2 rerun rewrote builder C's `v3_tool_guard_agreement.json`. It is current and recorded in the
     manifest.
8. **Orphan definition files.** F5 left 2 old judge cards that are no longer used. F3's write will add 16 files and
   leave some old ones unused. The assembler must take only the definition files that rows reference.
9. **F2 falls short of the SPEC in two shares.**
   - JB fallback wording: 16.5% of train rows and 14% of dev rows, against 20%.
   - Attack twins: 7.3% of latents, against 8%.

   Some rule texts are also ungrammatical, for example "a every read tool call". The label is unaffected; fixing it
   needs `tg_core` and the decide2 parser changed together.
10. **F3 minor points.**
    - `sim.MACHINES` still has the old behaviour; the fixed subclasses live in `gen3_state_track.py`.
    - 1 dev latent offers impossible 102% / 103% options.
    - In 37 ledger choice rows, the negative-balance option is never gold.
    - On dev, the "artefacts" check fails (correlation 0.058, only 15 JB rows). The builder's notes leave this check
      out on dev.
11. **F5 minor points.**
    - 18 rows depend on reading the unsubscribe penalty as applied after the cap.
    - The overridden-statement trap has no hard-case tag.
    - The §7 checks have not been run on the new card wording.
12. **devx blind solves are still to do.** The 50-row devx blind solves for F2, F3 and F5 wait on reviewer R.

## 7. What wave 1b needs (F1, F4, F6, devx)

**First steps (they block wave 1b or its gates):**
- The owner's OK to write F3's fixed build (issue 1). F4(b) and F3's devx must use the fixed latents.
- Every family builder starts from `mv_core.FamilyBuilder`; `yn2b/tests/toy_family.py` is a worked example. Pick the
  stratum first, then the gold target for it, and make sure every (tier, gold) target is reachable with the family's
  shortcut set. Otherwise the joint balance rule (within 1 row in small strata) makes the sampling loop run forever.

| Piece | Owner (SPEC 13.1) | Size | What it needs |
|---|---|---|---|
| **F1 `gen3_rule_chain`** | D builds the engine, F1a and F1b; E writes decide2 | 4,000 base rows: F1a 3,400 (1,900 yes/no + 1,500 choice, of which 200 JB) + F1b 600 yes/no. Plus 8% attack twins. Dev 200 iid + 200 holdout (school-transport family, contract style). devx 100 | From gen2_long_policy, import only the classes, `evaluate` and `build_state`; no `main()` or `append_manifest()`; never import `lean/pg/*`. "Which clause is decisive": reject items with 0 or 2+ decisive clauses. Ladder views on 30% of yes/no latents. decide2 rebuilds the clause graph from the rendered text |
| **F4 `gen3_polarity_ladder`** | A builds it; C writes decide2 | 1,500 standalone yes/no: (a) 750 on human hard-gold rows in S units; (b) 750 on F1, F2, F3 and F6 train latents. Dev 150 + 150, (b)-type only, 2 held-out frame families | (a): `yn2b_ab_S_units.jsonl` is ready (44,029 units). Apply the exclusions (vote-share and gold_probs teachers, attacked / defswap / neg roles, `gd_gen*`, clinc150, banking77, std_hate, gd_ghc_hate, tb_label_nli). Rows carry `derived_from` / `derived_by`. (b): needs F1 and F6 latents and the fixed F3 latents, so it comes **after** them. Frames: 7 from `robust/ladder_proto.py` + sign_off, compliance_flag, audit_finding. cue_shares ≤ 60%. 6-gram bans vs dialogue_rebuttal, v11 train templates and ship-split instructions |
| **F6 `gen3_def_literal`** | D builds it after F1; A writes decide2 | 1,500: 1,100 yes/no + 400 choice (100 JB). 10% attack twins (`inv`). Dev 75 + 75. devx 100 | 10 packs (customs tariff replaces tribunal evidence). 2 packs and 3 terms held out. The definition goes in the card for yes/no rows. 30% real words with a different definition. No "hearsay" or Federal Rules of Evidence structure. The counter-definition plants must share no 6-gram with eval_redef; mv_core's test of plants vs eval spans covers this |
| **devx** | Reviewer R; then R2 blind-solves 50 rows per family | 500 rows: F1, F2, F3, F5 and F6, 100 each | Use dev_holdout latents only. Write new renderers and question wordings from the latent schema and the SPEC only; never read the training renderers. Labels come from the shared `decide()`, and R's parse-back must agree on 100%. Latent sources: F2 `devx_latents()` is ready; F5 `sample_latents()` changed in R2, so use the current one; F3 `export_latents` (fixed MACH), after issue 1 |

**After wave 1b, for all families:**
1. Run `check_yn2b` (§7, OHS-3 counts only), then `check_unseen`.
2. Run the assembler, and settle issue 6 first.
3. Write the §8 outputs.
4. Build the arm B and arm C files.
5. Freeze the dev and devx sha256 values in A1 part 2, before arm B.

If time runs short, the priority order is F2 → F5 → F3 → F1 → F4 → F6. Only families that pass every gate enter
arm B.

## 8. Key files

- Engine: `golden_src/gen3/mv_core.py`, `yn2b/MV_CORE_API.md`, `yn2b/tests/toy_family.py`
- Tools: `yn2b/assemble_yn2b.py`, `merge_yn2b.py`, `build_ab_yn2b.py`, `check_yn2b.py`, `check_unseen.py`,
  `teacher_gate_2b.py`, `ab_readout.py`, `yn2b_common.py`, `label_audit.{py,md,json}`,
  `label_audit_known_bad_ids.json`, `TOOLING_NOTES.md`
- Families: `golden_src/gen3/gen3_{tool_guard,lead_score,state_track}.py` (+ `tg_*`, `gen3_state_track_sim.py`);
  decide2 `golden_src/gen3/v3_{tool_guard,lead_score,state_track}.py`
- Gates: `yn2b/r2_lead_score_{gate,blind}.json`, `yn2b/r2_state_track_{gate,blind}.json`,
  `yn2b/v3_*_agreement*.json`, `yn2b/F3_STATE_TRACK_NOTES.md`
- Data: `data/v14_parts/yn2b_raw/`, `data/v14_parts/yn2b_defs/`, `data/v14_parts/yn2b_ab/`
- Manifest: `golden_src/gen3/MANIFEST_yn2b.jsonl` (83 records)
