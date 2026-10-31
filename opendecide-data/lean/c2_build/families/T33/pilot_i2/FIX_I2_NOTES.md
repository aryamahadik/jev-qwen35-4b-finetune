# T33 fix iteration 2: notes (stage scripts written and tested on fabricated answers; pilot_i2 run still to come)

Backups: `families/T33/_backup_i2/` (plugin.py, G0_SPEC.md, run_pilot_i1.py, cardtext.py, solver_b.py, haiku_author.py,
test_cardtext.py, test_i1_fixes.py, test_plugin.py). `pilot/` and `pilot_i1/` are untouched.

## Changes
1. Spec 3.0 length (compact cards, kit `c2_kit/cards.py`):
   - `cardtext.py`: drawn styles are now `compact` 85% and `short` 15% (`full` stays as the reference text, never drawn).
     Every compact/short piece passes `cards.variant_problems` (slots, quoted literals, numbers, operator words,
     negation count); a whole-block test checks rendered blocks against the full block. Log rules and claim rules are
     one line each in compact and short. `place_rules` placement and `defs_style` were already in (iteration 1).
   - `solver_b.py`: own copy of all three styles (`_expected_rules`); `test_cardtext.py`, `test_plugin.py` updated, two
     tests added (whole blocks keep every rule; solver B's copy equals the generator's block in every style).
   - `G0_SPEC.md`: section 2 note, new section 9 (amendment i2); `T33Plugin.G0_SHA256` re-frozen to
     `44e36667424c3b83f51e5b8ab16903108429f5bf2fffafd902f8d9128bcba1ee`.
2. Double negation: `dneg_i2.py` (tasks, supplement, loader), `dneg_stage2.py`, `dneg_stage3.py`, `test_dneg_i2.py`;
   `run_pilot_i2.py` (output `pilot_i2`; loader patched to read the supplement; extra `g6` command).

## Measured (in-memory dry run, 1,000 rows, same seeds as pilot_i1, real tokenizer, instructions twice)
- spec 3.0 mean tokens: 876.4 -> **832.2** (bar <= 800): **STILL FAILS by 32.2**. max 1,365 (<= 2,000 passes).
- All program gates as in iteration 1 (G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G7 pass); G6 at pilot size
  misses on d_meta/gbt (yes/no .5228 vs .52; choice .3418 vs .3266), the same pilot-size lottery as iteration 1
  (A43 decides on the 6,000-row run, not yet repeated for pilot_i2); G10 fails only on double_negation_share (0%).
- Why 800 is not reached by cards alone: after compaction the rules text is at its floor. The pieces that remain are
  numbers (200, 201, 204, 409, 202: digits cost one token each), the claim and tie rules, and the closed-world sentence.
  Rules per row are now about 165-185 tokens (full: about 215-230); the kit's "rules shrink to 0.64" figure was for
  pre-placement rules. Not done (each lowers difficulty or diversity; needs an owner ruling, G0 S18 / O1): steps (2,2,3,3,4)
  about -17 tokens; interim poll 0 plus no markdown container on S4 about -14; 2-hex ids (ik-a3, job-7f) about -10.
  Dropping rules that "the log does not need" was rejected: it would make the card predict the gold (G6 c_card view).

## Double negation: commands (run from `jev/opendecide-data/lean/c2_build`, PY = `../../.venv/bin/python -B`)
1. Authoring task files (4 chunk files, 12 items, 36 candidate wordings per form = 4.5x the 8 admitted wordings per form):
   `PY -m families.T33.dneg_i2 write-tasks` -> `families/T33/haiku/dneg_i2/tasks/` (TASKS.json lists task_file and
   answer_file; one fresh Haiku agent per chunk; each reads only its task file and writes only its answer file).
   The brief is the family's polarity-aware one (explicit outer frame "is it not true / the case that", one `not` on
   meeting the criterion or before every/all, no contracted opening, no word with its own negative meaning) plus an
   angle per item and a G-SL note (found in the fabricated-answer test: the base brief let Haiku write "step {STEP}
   does not meet", and G-SL rejects any word but of/in/on after {STEP}).
2. Stage 2: `PY -m families.T33.dneg_stage2` -> admission (shape, bans, negation count (2,2), polarity P1-P4, lexicon unit
   test, G-SL), G-LEX tasks for two independent reads in `haiku/dneg_i2/glex_tasks/` (TASKS.json), `stage2_report.json`.
   Exit 1 if a form has < 8 candidates left (re-author).
3. Orchestrator: one fresh Haiku agent per `glex_tasks` task file (read0 and read1).
4. Stage 3: `PY -m families.T33.dneg_stage3` -> records the reads, keeps 2/2 wordings (>= 8 per form, else STOP and nothing
   frozen), freezes `pools/dneg_i2_supplement.json` + `pools/DNEG_I2_FREEZE.json` (append-and-freeze; the supplement
   also declares the two question sems the frozen lexicon lacks), writes `pilot_i2/G13_PENDING.txt` (no local G13-seed
   runner: the wordings are listed for the batch run), then runs the family tests, determinism, the pilot into `pilot_i2/`
   (G5-H / G3-H task files, not answered) and the 6,000-row run into `pilot_i2/G6_AT_6000.json`; logs `pilot_i2/stage3_*.log`.
   `--no-run` freezes only; steps can be run alone: `PY families/T33/run_pilot_i2.py run|dry|determinism|g6 --n 6000`.
5. After stage 3: the G5-H re-read needs >= 10 double-negation rows (pilot_i2 has them once the supplement exists).

## Tests
- Fabricated-answer tests (`test_dneg_i2.py`, temp folder under `_scratch_i2/`, removed afterwards): tasks self-contained;
  stage 2 admits good wordings and drops contracted, not-over-negative, positive, no-question-mark and no-{STEP} ones;
  stage 3 freezes 47 of 48 (one form fails its second read), refuses to rewrite or to accept a tampered supplement, STOPs
  when a form has < 8; the merged context builds rows with every gate (G2, G3, G4, G-TW) for both forms.
- See the bottom of this file for the full family test run and determinism result.

## Test and determinism results
- `pytest families/T33`: 77 tests, all pass after the last fix (test_plugin fragments updated to the compact wording).
  Test copies in `_backup_i2/` are renamed `*.bak` so pytest does not collect them.
- Determinism (`run_pilot_i2.py determinism`, PYTHONHASHSEED 1 and 4242): identical; rows sha256
  5a09967916b059432b7bb29e6899eaac59eb1749d634bae681812929f97702ba, relations sha256 478f3e5391cf...; mean tokens 832.2.
- G0_SPEC.md is 190 lines (the family test caps it at 200: sections 4, 5 and 8 were reflowed, no word dropped).
- Not run (by design): Haiku authoring and G-LEX reads, `pilot_i2` itself (stage 3), G6 at 6,000 rows for pilot_i2.
- `families/T33/_scratch_i2/` holds only the scratch scripts and pytest logs of this iteration (safe to delete).

## Orchestrator ruling on spec 3.0 length (applied; supersedes the "STILL FAILS" lines above)
Backup before this step: `families/T33/_backup_i2b/` (plugin.py, G0_SPEC.md, run_pilot_i2.py). G0 section 10 records it.
Levers in order, each measured with `run_pilot_i2.py dry` (1,000 rows, real tokenizer, instructions twice):
1. 2-hex ids (`ik-a3`, `job-7f`; plugin `_entry`): 832.2 -> 819.0 (still above 800).
2. S4 only: `INTERIM_POLL_P_S4 = 0` and S4 formats `("jsonl", "text")` (no md): 819.0 -> 812.0 (still above).
3. Tail cap, every sampler, label-blind (`_cap_tail`, `TAIL_CAP_P`): 4-step draws become 3 with p .40 (about the longest 10%)
   gave 801.8 (not enough); p .60 (4-step share 25% -> 10%, about the longest 15% by steps) gives **799.4 (pass, margin 0.6)**,
   max 1,315. Depth rule and label balance code untouched. The margin is thin: the dneg wordings or a re-seed can move it.
- G0 re-frozen: `G0_SHA256 = aec65eaa39db2829a3617b0bcc67684919a8caf332ab7837f4166617f2508324` (G0_SPEC.md, 198 lines, new
  section 10). The tests read the pinned value from `plugin.G0_SHA256` (no literal copy), so no test text changed.
- `pytest families/T33`: 77 passed (log `_scratch_i2/pytest_i2b.log`).
- The dry-run row/relations sha256 changed (rows 39f8c273..., relations c3efa24e...); rerun `determinism` after stage 3.

## G6 at 6,000 rows after the length changes: FAILS (`pilot_i2/G6_AT_6000.json`, n=6,001)
- Single failing cell: choice / d_meta / gbt = .3402 vs chance .308 + 2 pp = .328 (+3.2 pp; n=2,870). Every other view and model
  is within the bar (yes/no max .5000 b_options lr). G7 pass. G10 fails only on double_negation_share 0% (dneg wordings not yet
  admitted) and one n=51 yes_rate cell (.471, report-only).
- iteration 1 passed at 6,000 (choice max .3274), so the length levers (or the seeds they shift) introduced it.
- Diagnosis (`_scratch_i2/diag_dmeta.py`, gbt on choice d_meta, one numeric feature dropped at a time): no single driver.
  all .3402; drop len_state .3289, len_q .3310, k .3261, n_numbers .3260, depth/deep .3314, n_lines .3280, len_ins .3509,
  mag_max .3418; option-only features .3042 (chance). The signal is spread over card-size features crossed with option
  properties (choice forms: ch_failed_check 1,211, ch_claim_verdict 1,008, ch_bad_claim 651).
- Not fixed in this step (the ruling covered length only; no further lever was authorised). Open for the orchestrator: A43
  allows the 1,000-row cells only within their pilot-size null; the 6,000-row bar is a hard fail as it stands. Candidate
  follow-ups: raise `TAIL_CAP_P` back toward .4 and take a different length lever (re-measure G6 each time), or de-correlate
  the choice option set from episode size. Not tried.

## Dneg authoring task files (written with `python -B -m families.T33.dneg_i2 write-tasks`)
Folder `families/T33/haiku/dneg_i2/tasks/`; each chunk file holds `items`, `instructions`, `answer_format` (the exact contract)
and `answer_file`. Index: `tasks/TASKS.json`. Absolute prefix `/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/`.
| task file (`families/T33/haiku/dneg_i2/tasks/chunks/`) | answer file (`.../tasks/answers/`) |
|---|---|
| `T33-author_wording-9fc39663-000.json` | `T33-author_wording-9fc39663-000.json` |
| `T33-author_wording-9fc39663-001.json` | `T33-author_wording-9fc39663-001.json` |
| `T33-author_wording-9fc39663-002.json` | `T33-author_wording-9fc39663-002.json` |
| `T33-author_wording-9fc39663-003.json` | `T33-author_wording-9fc39663-003.json` |
Stage commands (from `c2_build`, PY = `../../.venv/bin/python -B`): after the four answers exist, `PY -m families.T33.dneg_stage2`;
run the `haiku/dneg_i2/glex_tasks/` files (two reads); then `PY -m families.T33.dneg_stage3` (freezes the supplement, runs
tests, determinism, the pilot and the 6,000-row G6 again). Note: stage 3's G6 will reuse the length changes above, so the
d_meta failure must be resolved first or it will fail again.

## i2c: label-blind card size (fixes the G6 d_meta failure above; supersedes its "not fixed" lines)
Backup: `families/T33/_backup_i2c/` (plugin.py, G0_SPEC.md, run_pilot_i2.py). G0 section 11 records it.
Cause found: sub-form (b) redrew the step count (and the tail cap) inside the attempt loop, so label-specific rejections
(claim counts, a not-shown claim needing a source step, verdict targets) shaped the accepted step counts; the filler step
count was a coin inside the loop; (a) and (b) episodes of a failing check had about half a line and one retry line more
than a pass (ch_failed_check gold "tries": 4.5 try lines vs 3.4).
Changes (plugin.py), every size feature drawn from the row seed (uhash) before any label, same distribution for all labels:
1. `_row_steps`: step count + tail cap, drawn once before the loop; (b) rows get max(count, n_claims). (b) non-forward rows
   pad with neutral filler steps to that count (more entries than the count: attempt rejected). `TAIL_CAP_P` = 1.0
   (4 steps only with 4 claims or in S3); this was needed to keep the mean <= 800 once the count is at least n_claims.
2. Interim poll: one row-level draw (`_interim_on`), p .10, S4 0 (was a per-job coin inside the loop).
3. `LINES_PMF` / `_row_lines`: seed-drawn log-line target per step count (pooled i2b distribution); episode kept only
   if |lines - target| <= attempt // 25.
4. `RETRY_EXTRA_PMF` / `_row_retries` ((a) only): seed-drawn retry-line target; a row listing a tries check starts at R_MAX.
No feature dropped, no relabel, no gate bar changed.
Results (this folder): `G6_AT_6000.json` n=6,000: G6 PASS; yes/no max .5022 (d_meta gbt; bar .52), choice max .3266
(c_card_without_question lr; bar .328; d_meta gbt now below it). G7 pass. G10 fails only double_negation_share
(dneg wordings not yet admitted). Token mean 793.0 (bar 800; was 799.4 / 806.9 at intermediate steps), max 1,279.
G0_SHA256 = ea73985d7e9aaddc00264a187b3c2b913b6f966bf6afd6c0a07dd9298163859a (G0_SPEC.md, 200 lines = test cap).
`pytest families/T33`: 77 passed. Determinism (PYTHONHASHSEED pair): identical, rows sha256 250969859962bd..., relations a8ed516a6257....
Not touched: haiku/dneg_i2/, dneg stage scripts. The dry-run sha changes again after dneg stage 3 (supplement). Margin on the
mean is 7 tokens; dneg wordings can move it. Scratch: `_scratch_i2/diag_*.py`.
