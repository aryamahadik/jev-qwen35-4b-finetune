> **Ruling A55 (DRAFT, 17 Oct 2026, ~00:15 UTC; orchestrator rulings model; G13 batch-4 shortfalls; no bar, gate,
> waiver rule or G13 method is loosened; no relabel; `c_build/decontam_g13.py` and `c2_build/g13_c2.py` unchanged).**
> Evidence: `c2_build/zed_orch/g13_attr/g13_attr.json` (sha256 38b4cf582f8724f2ef3047d790b984ddcf915f5fa3c3b2a7ff9b13628f7c4a6e),
> `g13_attr_units.jsonl` (sha256 60ab76de3b8c9c58f59c693422181e6736169dc8d41e673e239a67449489d8a4), script `g13_attr.py`
> (sha256 2dc91b4c9ce23327ab612ce971d20cdeb378039ce22f62ee5a6f76b6286c1215). The analysis reproduced batch 4's per-method
> binding unit counts exactly for all 16 blocks; it read no sealed file. Batch 4 is diagnostic only: every mixdev
> change below makes every candidates log stale (guard v3), and the one final all-block G13 binds (Mon 19 Oct ~20:00
> UTC). This ruling does not run G13 and does not touch T27 or T32 files.
>
> - **(a) Finding.**
>   - The shortfalls come from the families' **own** S5 mixdevs. The hits are spread over nearly all dev rows (T24
>     149/150, T06 142, T23 118, T07 115), so replacing a few dev rows does not help.
>   - The A53 precondition already holds for every program family except T25. The remaining shared items are of
>     three kinds:
>     - rendered numerals and ids inside program frame lines (A53 (C) tiles words, not numerals);
>     - rule and clause lexicon forms (comparator, window and other kinds), which are never held out (T24 0 of 232);
>     - stock prose.
>   - T25's 320 exact_full units are two program constants. A53 would waive them, but T25's precondition fails on
>     wording (72 of 74 dev wordings are also candidate wordings; 0 held-out question forms).
>   - Sealed-keyword (ohs4_hash) hits come from our own vocabulary lists.
>   - GB and GW hit the GB mixdev. That mixdev is drawn by design from the same cards before routing (A42-D 5.5).
> - **(b) Not a G13 failure; A52's one-fix-round rule.**
>   - G13's bar is 0 hits after drops. A family left short after its drops has **passed** G13. A shortfall is not a
>     failed binding gate, so it opens no A49 (d) fix round for any family.
>   - **The families that already used their last round** are T24 and T25 (A52 d, wave 9) and T06 (A48 a,
>     iteration 3). They get no further generator change.
>   - Every lever below is one of two kinds:
>     - **(L1)** a dev-only mixdev rebuild. It changes no training row (the candidates digest must stay
>       byte-identical), so it is not a fix round;
>     - **(L2)** a top-up of more seeds from the **byte-identical** passing generator. It changes no existing row and
>       no code or pool, so it is not a fix round. It must pass the same gates as the full generation, (e).
> - **(c) The vocabulary filter is NOT used for C2 rows.**
>   - Removing colliding entries from a generator's lists makes a different generator. For C2 that would mean:
>     - the A50 G6 re-run on that generator (4 × 6,000 rows at B0, 11,000,000, 12,000,000 and 13,000,000);
>     - a new G5-H and G3-H on its rows;
>     - **a generator-fix round**, which T24, T25 and T06 no longer have, and which T07, T12, T23, T26 and T28 have no
>       failed gate to open.
>   - Every top-up in (e) therefore uses the unfiltered generator. G13's keyword method keeps dropping the colliding
>     units, as it does now, and the top-up size (e) counts that loss.
>   - **The blocklist is recorded for C3 and for any later regeneration:**
>     - the 43 shared stems;
>     - the drawn entries per family and list (`g13_attr.json` "keyword"), with T07's 40 pool documents that embed
>       them;
>     - the latent entries (T26 40, T23 90, T28 15, T01 3).
>
>     It lists file, list and entry ids only. This ruling never prints the colliding strings, because they would
>     reveal sealed-side content. A C3 regeneration applies the blocklist before its first row and counts as a fix
>     round with the A50 G6 re-run.
> - **(d) L1, dev-only mixdev rebuild (spec 7.1, the A54 method extended).**
>   - **Same as A54:**
>     - the mixdev seed base from GEN_REPORT and 150 rows per family;
>     - the same S5 frames, skins, registers and packs;
>     - the G5-H-quarantined templates stay out;
>     - the old mixdev is backed up as `_superseded_a55` and is never used again as dev.
>   - **Dev-only additions** live in a dev-only overlay (the `a54_heldout_overlay` pattern). The overlay is active only
>     inside the mixdev rebuild tool. It does not edit `pools_v2`, plugin code or any file the sealed mode reads; a
>     sha256 check of those files runs before and after.
>     - If a family's change cannot be done that way, it must be finished before the OHS-AC freeze cut (**Sat 17 Oct
>       16:00 UTC**), and that family's sealed A1 items are rebuilt at the freeze under A54's drift rule.
>     - After 16:00 UTC, only overlay changes are allowed.
>   - **(d1) Dev-only numerals and ids.**
>     - Opaque ids and codes in dev rows come from a dev-only namespace of the same format class. The tool checks that
>       namespace against every id in the family's candidates.
>     - Task-relevant quantities keep the S5 distribution. If a dev row's numeral-bearing state line equals, after
>       whitespace normalisation, a line in the family's candidates, the row's own seeded stream re-draws that line's
>       values (≤ 16 tries). Gold is recomputed. After 16 tries the row stays as drawn, and its hits bind.
>     - The rebuild never reads a G13 log or the binding-unit list. Its only inputs are the candidates file and the
>       pre-declared rule above.
>   - **(d2) Dev-only rule and clause forms.**
>     - For each rule or clause kind used by the family's dev rows, Haiku authors 8 forms and ≥ 4 must be admitted.
>     - Admission takes all of:
>       - the G-LEX unit test;
>       - 2/2 extraction agreement (3/3 for precedence and window);
>       - a form text equal to no pool entry of the family, in training or held out;
>       - 0 hits from `g13_ohs4_check`, run through `g13_c2.run_checker` (counts only; a hit removes the form).
>     - A kind with fewer than 4 admitted forms keeps its training forms in dev, and its hits bind.
>   - **(d3) T25 dev-only question wordings.** Haiku authors 8 wordings per dev question form. Admission is G-LEX 2/2,
>     a wording equal to no T25 pool wording, and 0 run_checker hits. Admitted wordings must reach ≥ 4 per form, and
>     S5 uses only those. Then the A53 precondition holds and the two constants are waived exactly as A53 says.
>   - **Checks after each rebuild:**
>     - **Training digests.** `a54_verify_candidates.py`: the candidates digest is byte-identical, or the rebuild is
>       reverted.
>     - **A53 precondition.** `a54_rebuild_mixdev.py`'s `precondition()` must report 0 shared. If d2 breaks it, d2 is
>       reverted for that family and d1 is kept.
>     - **Dev-row program checks.** G2 (solver B 100%), G3, G-SL and G-TW (where they apply) run on the dev rows.
>     - **Records.** The new mixdev sha256 goes into QC_REPORT (the old one as `mixdev_pre_a55`) and the overlay's
>       sha256 into the A55 addendum.
>   - The rebuilt dev is a learning check that the bar (+8.0 pp, spec 7.2 a) is no easier to pass. It is never
>     trained.
> - **(e) L2, top-up, decided only after measurement.**
>   - **Measure.** Re-run `g13_attr.py` on the rebuilt mixdevs. This is analysis only, not a G13 run; its c2_mixdev
>     counts are exact. It gives E, the point estimate of rows left for each family.
>   - **Size.** The decision is logged before any top-up row exists. A top-up runs only if **E < 1.03 × target**,
>     with **X = ceil((1.06 × target − E) / (s × q))** rows, where:
>     - s = E / candidate rows;
>     - q = the family's full-generation QC keep rate (rows after G5-H, G3-H, G-SL and G12 drops over rows
>       generated).
>
>     X is never raised later. There is no second top-up after the final G13.
>   - **Seed base.** 733,000,000 for every top-up, with the family's redraw stride of 50,000,000. This base is
>     disjoint from every recorded base and redraw class: 0.9M, 2-4M, 11-13M, 39-41M, 46-48M, 127-129M and 250-252M.
>     The tool asserts this against the family's GEN_REPORT and logs. If the base is in use, the pre-declared fallback
>     is 743,000,000.
>   - **Generator identity.** The plugin, pools, quarantine sources and Haiku prompt shas must equal the QC_REPORT
>     record, and a re-derivation of the original candidates must be byte-identical. Otherwise there is no top-up.
>     The top-up rows go into their own candidates part with its own sha256. The original part's digest is unchanged.
>   - **Gates on the top-up rows (spec 6.4 step 7, bars unchanged).** These run on the top-up rows:
>     - G2 100% and G3 100%; G4 relations 100% (the ≥ 1,000-per-sampler count is met by the original build);
>     - G-SL 100% (failing rows dropped) and G-TW 100%;
>     - G3-H ≥ 98% per template on the free-form top-up rows;
>     - G5-H on a seeded min(300, X) rows, plus 100% of free-form rows, plus 30 agreed rows (Sonnet first pass, Opus
>       confirms every flag, A43 d);
>     - G15.
>
>     These run on old plus top-up candidates together:
>     - G7 and G8;
>     - G11 (skin and template ≤ 2%, Self-BLEU and Vendi);
>     - G12 (exact 0; MinHash keeps the existing row).
>
>     Gates that carry over unchanged because the generator is identical:
>     - G6, the A50 four fixed builds;
>     - G13-seed and G-TPL (no new pool or template text);
>     - all template quarantines (G5-H, G3-H, A43 f, G13-seed).
>
>     G10 is report-only here and binds at selection (A49 c). The final all-block G13 checks the top-up rows against
>     every target. G9 C1 crowd reads (od-l4b, A49 f path) run before `select`.
>   - **Failures.**
>     - A top-up that fails a gate is discarded whole, and its seeds are never reused.
>     - A confirmed wrong gold is a generator bug. The top-up is discarded, and a program check over the existing
>       candidates drops (never relabels) every row with that bug's condition.
>     - The family then keeps its current rows, and any shortfall is accepted.
> - **(f) Per family.**
>
>   | Family | Now / target | Lever | Fix round? | Expected E | Who | Re-run |
>   |---|---|---|---|---|---|---|
>   | T24 | 274 / 600 | L1 d1 + d2; L2 only if E < 618 | No (round used in wave 9; L1 and L2 change no existing row or code) | ≈ 677 (ceiling 817) | Haiku authors, Sonnet overlay and checks | digest, precondition, dev G2/G3/G-SL, attribution; L2 gates if triggered |
>   | T25 | 338 / 600 | L1 d3 (constants waived by A53 once the precondition holds); no L2 (a plain top-up has no abstain class) | No (round used) | ≈ 795 | Haiku wordings, Sonnet | same as T24 |
>   | T06 | 738 / 900 | L1 d1 + d2; L2 if E < 927 | No (iteration 3 used) | ≈ 917-929, so L2 is likely | Sonnet; Haiku if L2 | same, plus L2 gates |
>   | T07 | 688 / 800 | L1 d1 + d2 (on its v1+redo2+redo3+heldout_a54 layer stack, sha-checked); L2 if E < 824 | No | ≈ 906 | Haiku forms, Sonnet | same |
>   | T23 | 734 / 800 | L1 d1 (on its A54 patch); L2 if E < 824 | No | ≈ 911 | Sonnet | same |
>   | T26 | 1402 / 1400 | L1 d1 (margin before the T27/T33 mixdevs enter); L2 if E < 1442 | No | ≈ 1567 | Sonnet | same |
>   | T28 | 2430 / 2400 | L1 d1; L2 if E < 2472 | No | ≈ 2519 | Sonnet | same |
>   | T12 | 823 / 800 | L1 d1; L2 if E < 824 | No | ≈ 859 | Sonnet | same |
>   | T01, T15, T29, T30, T31 | above target | none | No | unchanged | none | final G13 only |
>   | GB, GW | 3834 / 15000, 4520 / 9200 (caps; short is fine) | none | No | unchanged | none | final G13 only |
>   | MD | 11405 / 12000 | none (inside the 8,000-12,000 range) | No | unchanged | none | final G13 only |
>
>   - **GB and GW stay short.** Redrawing the GB mixdev after routing would bias dev toward routed (C1-disagree) rows
>     and inflate the learning check, which would loosen it. A redraw before routing shares cards by design and gains
>     nothing. GW's hits are real passage overlaps with GB dev (5 whole-row and 11 state-text duplicates).
>   - After the final G13, every remaining shortfall is accepted through the mixer's reflow: missing shares lower the
>     total, replay = floor(1.5 × realised new rows), and nothing is refilled (A34 c). The training-GO request lists
>     each short family. T27 and T33 are not covered here.
> - **(g) Deadlines (all before the final all-block G13, Mon 19 Oct ~20:00 UTC).**
>   1. **Sat 17 Oct 06:00 UTC:** Haiku authoring tasks out. These are T24, T06 and T07 rule and clause forms (d2) and
>      T25 question wordings (d3).
>   2. **Sat 17 Oct 12:00:** G-LEX votes and run_checker counts done. The admitted lists are frozen and their
>      sha256 logged.
>   3. **Sat 17 Oct 16:00:** cut for any change to a file the sealed mode reads (none is planned).
>   4. **Sun 18 Oct 12:00:** all 8 mixdevs rebuilt and checked under (d). Sonnet runs the rebuild tool; Haiku does no
>      work in this step.
>   5. **Sun 18 Oct 14:00:** `g13_attr.py` re-run. E, the decision whether to top up and X are logged for each family.
>   6. **Mon 19 Oct 16:00:** top-up rows generated (VM), program gates passed, and G5-H and G3-H read (Haiku) and
>      adjudicated (Sonnet, then Opus). A top-up that is not complete by then is dropped whole.
>   7. **Mon 19 Oct ~20:00:** the one final all-block G13. It runs separately and is not part of this ruling.
>   8. **Tue 20 Oct 12:00:** G9 C1 reads of the top-up rows, then `select`. The cutoff (Wed 21 Oct 23:59, A39 g) is
>      unchanged.


---

> **A55 implementation addendum (tools; 17 Oct 2026 ~01:15 UTC; written by the implementing agent for the orchestrator to record; the ruling text above is unchanged; PREREG_FINAL.md not edited; no G13 run; T27 / T32 files untouched).**
>
> - **(i) Tools (all new; no existing code file was edited; `a54_*`, `g13_attr.py`, `g13_c2.py`, `decontam_g13.py` unchanged):**
>   - `c2_build/zed_orch/a55_common.py` sha256 `cff9ed72dc06837ea1663da16202aac12980f20e089c28737219219a3515272e`
>   - `c2_build/zed_orch/a55_overlay.py` sha256 `fb08f710b787d5a6fb4cc2770486250b85a576e83f0a2fb27e467ce82e1a628e`
>   - `c2_build/zed_orch/a55_rebuild_mixdev.py` sha256 `15f6faf72f54e7df02cb065a56050138315b31043962f55e196758646070a76a`
>   - `c2_build/zed_orch/a55_devforms.py` sha256 `d4c68e524bd46f3bf6ae2ce97410a3ad7ede254a09d25349a898151a5a560a5f`
>   - `c2_build/zed_orch/a55_measure.py` sha256 `ad8adfd3873025435957d61c2a065c62210905e5e5165e63c7e2e7f4953c39be`
>   - `c2_build/zed_orch/a55_topup.py` sha256 `9de3dc2f9f0d08763e5e62576afdf86aa0fb46950ab59e68cc4567e97f43d892`
>   - `c2_build/zed_orch/a55_sim_check.py` sha256 `d00ce6637fe551b6e8b7779c0d84e73aa3c495b328d63d716f1daa5158d50e6b`
>   - `c2_build/tests/test_a55.py` sha256 `a59da29394f1ede11f411b5d5d72fc195dbef86db5e9a79429921fb8fc43253f`
>   - The **overlay** (d2/d3) is `a55_overlay.py`: sha256 `fb08f710b787d5a6fb4cc2770486250b85a576e83f0a2fb27e467ce82e1a628e`. It is active only inside `a55_rebuild_mixdev.py`.
>     It reads `families/<FAM>/dev_a55/FROZEN.json` and edits no pool, plugin or sealed-mode file (generator sha256 before / after each
>     rebuild: equal).
> - **(ii) How the ruling was read (the orchestrator confirms or corrects):**
>   1. **d1** runs two tiers, both from the candidates file only. *Declared tier:* a numeral-bearing state line equal (whitespace-normalised) to a
>      candidate line, plus an opaque-id check (id-shaped tokens, `PREFIX-123..`, also in the candidates). *Extension tier (default,
>      `--level item`):* a numeral-bearing A53 item (10-gram, segment, whole option) shared with the candidates that A53 would not waive.
>      The line rule alone hits 0 dev rows of T26 (219 binding units; the id check hits 52 rows, the item tier 62), so it could not give the table's E; `--level line` applies the
>      declared tier and the id check only. A colliding **unit** is redrawn from its own stream (`seed + j x 144,144,000`, j = 1..16; the
>      sampler, seed block position and card are kept); gold is recomputed by the solvers; after 16 tries the unit stays as drawn.
>   2. **Dev-only id namespace** = the family's own id generator, redrawn until no id of the dev rows occurs in the candidates (checked: 0 shared
>      in every rebuilt dev set). A separate namespace would need a plugin edit; `slots.id_slot` cannot be remapped because T26, T28 and T12
>      use ids as logic (domains, tool names, registry numbers).
>   3. **d2 unit = the sem** (a form carries one meaning). 8 forms are authored per sem (T24, T07: 2 items x 4; T06: 8 notices) and a sem needs
>      >= 4 admitted; a kind is reported as the sum of its sems. A sem below 4 keeps its training forms in dev. **d3:** all 7 T25 question
>      forms get 8 wordings (the S5 draw may use any of them).
>   4. **Measure:** `a55_measure.py` (the g13_attr loaders and engine scan, read-only) replaces re-running `g13_attr.py` itself, because that
>      script asserts the batch-4 dev files. With no rebuilt family it reproduces every block's logged rows left exactly (asserted).
>      **q** (QC keep rate) = final candidate rows / (rows written by the build + rows of the units the build dropped, at the build's mean rows per unit).
>   5. **Top-up part:** `data/c2_parts/<FAM>/topup_a55/root/<FAM>/{out,qc}` (the same layout, so `qc_full_c2.py --root` runs on it). `a55_topup.py merge` writes
>      the combined view to a separate root; wiring the final G13 / select / mix to read both parts (or that root) is the orchestrator's step.
>      G8 on old + top-up is not run by any candidate tool (as for every family).
> - **(iii) Done now (no Haiku needed):** mixdevs rebuilt for T12, T23, T26, T28 (d1). A53 precondition 0 shared, dev rows pass solver B / schema / G15 and every
>   unit passed G2 G3 G4 G-SL G-LEX G-TW G15 in the build; candidates digest byte-identical (a54_verify_candidates); the four were written by the rebuild tool as it stood at their write time (later edits: `--dev-root`,
>   the identity-record call, redraw-exception counters, folder path: none is on a code path those four used); generator identity recorded
>   (QC_REPORT `generator_identity_a55`). Old files: `data/c2_parts/<FAM>/out/_superseded_a55/` and `c2_build/zed_orch/g13_attr/_backup/a55/<FAM>/`.
>   Interim measurement (`g13_attr/a55_measure_interim.json`; T24 / T06 / T07 rows use d1-only analysis copies, T25 unchanged):
>
>   | Family | rows left batch 4 / target | c2_mixdev binding units | E (low-high) |
>   |---|---|---|---|
>   | T24 | 274 / 600 | 452 -> 355 | 376 (220-382) |
>   | T25 | 338 / 600 | 433 -> 433 | 338 (338-338) |
>   | T06 | 738 / 900 | 375 -> 288 | 831 (680-836) |
>   | T07 | 688 / 800 | 224 -> 177 | 732 (605-733) |
>   | T23 | 734 / 800 | 254 -> 80 | 946 (726-947) |
>   | T26 | 1402 / 1400 | 219 -> 43 | 1600 (1386-1625) |
>   | T28 | 2430 / 2400 | 120 -> 40 | 2522 (2430-2522) |
>   | T12 | 823 / 800 | 40 -> 3 | 861 (823-862) |
>
> - **(iv) Haiku task files written (not run):**
>   - T24: `c2_build/zed_orch/a55_dev/T24/tasks/T24-author_lexicon-7a7d1456-000.md` (18 items, task sha256 `92d906adf5001ab2`)
>   - T06: `c2_build/zed_orch/a55_dev/T06/tasks/T06-author_lexicon-9fd7f504-000.md` (28 items, task sha256 `9d940998bc3e4b72`)
>   - T06: `c2_build/zed_orch/a55_dev/T06/tasks/T06-author_lexicon-9fd7f504-001.md` (28 items, task sha256 `f610fdd720cbec5e`)
>   - T07: `c2_build/zed_orch/a55_dev/T07/tasks/T07-author_lexicon-8866f20b-000.md` (24 items, task sha256 `404ed88b0561bc3f`)
>   - T25: `c2_build/zed_orch/a55_dev/T25/tasks/T25-author_wording-e5f43041-000.md` (28 items, task sha256 `0d3a4ba0205d6a60`)
>   - T25: `c2_build/zed_orch/a55_dev/T25/tasks/T25-author_wording-e5f43041-001.md` (28 items, task sha256 `4bcdfb778cfb83d5`)
>   The dev-only files live in `c2_build/zed_orch/a55_dev/<FAM>/` (outside the family folders: a first version under `families/<FAM>/haiku/dev_a55/`
>   made T06 `test_freeze_v2` (`test_all_real_answer_files_are_valid`, `test_a_tampered_copy_is_rejected_whole_and_never_edited`) flag its `answers/` as a stray round, and a copy at
>   the top of the family folder breaks T24 `test_tests_write_no_file`'s folder listing; both removed, no family folder holds an A55 file).
>   Next: Haiku writes the answer files named in each task file; then `a55_devforms.py admit FAM`, `glex FAM` (writes the G-LEX read tasks), Haiku reads,
>   `score FAM` (writes `FROZEN.json`; log its sha256), then `a55_rebuild_mixdev.py FAM --write --verify-candidates` for T24 T06 T07 T25, then
>   `a55_measure.py --rebuilt T12 T23 T26 T28 T24 T06 T07 T25 --decide`, then (only if the decision says so) `a55_topup.py check|generate|merge`.
>
> - **(v) Tests (this session; the machine load average was 50-110, so each suite took 14-27 min):** `tests/test_a55.py` 13 passed. Family suites with the A55 files absent from the family folders:
>   T06 154 passed; T26 93 passed; T28 94 passed; T07 213 passed / 3 failed; T24 84 / 3; T25 177 / 4; T23 185 / 7; T12 102 / 1. Every failure is independent of A55 (none touches a file A55 wrote;
>   checked by re-running with the A55 folder removed): `_backup_a54` / `_backup_w9` copies of old tests (T07 2, T24 2 incl. `test_tests_write_no_file`, T25 2),
>   T24 `test_tests_write_no_file` also lists the untracked `FIX_W9_NOTES.md`, T25 `test_every_unit_passes_the_program_gates` (62/645 < 0.1) and `test_ctx_for_leaves_a_failing_wording_out...`,
>   T07 `test_the_verdict_on_disk_equals_the_one_computed_in_memory`, T23 `test_plugin.py` x7 (`LookupError: no wording for T23 (qform=yn_version, held_out=True)` in the stand-in ctx after the A54 patch),
>   T12 `test_card_style_is_label_blind_and_shared_by_a_unit` (0.0407 <= 0.04). Also failing before and after: `tests/test_full_gen_qc.py` x2 (`g13seed` key, T29 now in RUNNER).
>   `tests/test_g13_c2.py`, `test_mix_c2*.py`, `test_gate_c2.py`, `test_c2_select.py` 227 passed.
