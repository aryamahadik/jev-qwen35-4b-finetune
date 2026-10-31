# yn2b label audit (SPEC 8.6) and the teacher gate (D1, arm C)

**Date:** 30 Sep 2026. **Builder:** E. **Status:** done for the 4B-E labels. If the owner's D3 (30 Sep) swaps the
teacher to the new 4B, the numbers must be recomputed. The command is
`label_audit.py --kd-file <new KD file> --teacher-src <new name>`.

**Inputs (read only).**
- `data/v14_parts/train_2b_golden_kd.jsonl`, sha256 `e7b61114…ae83f`. This is build_2b_kd's output on the merged
  `data/v14_label_shards/labels_q35_4b_pxE`.
- `data/v14_parts/raw/gen_*.jsonl`, the generator raw files.
- `golden_src/gen/*`. The code is only imported. No `main()` is called and nothing is written.

**Outputs.**
- `yn2b/label_audit.json`: every number below, plus the per-row program checks.
- `yn2b/label_audit_manual.json`: the verdict from reading each audited row.
- `yn2b/label_audit_known_bad_ids.json`: the rows whose gold is wrong or ambiguous. It holds ids only.

**Tools.**
- `yn2b/label_audit.py` recomputes everything.
- `yn2b/teacher_gate_2b.py` makes the arm-C file.

## 1. Teacher error and the abstain zone, per generator

**Definitions.**
- *Wrong* means the teacher is on the wrong side of the program gold.
  - Yes/no rows: p(yes) ≥ 0.5 is not the same as gold = yes.
  - Choice rows: the unique argmax is not the gold option (ties count as wrong).
  - This is `build_2b_kd.gives_gold`.
- *raw* is the 4B-E read (`meta.teacher4b`). *trained* is the teacher the 2B trains on, after complement
  symmetrisation.
- *Mid* is the share of 2B yes/no targets inside JevBench's abstain zone (0.2, 0.8). The target is
  0.5 × (0.95 / 0.05 gold) + 0.5 × teacher.
  - The "before" column uses the teacher as it is.
  - The "after gate" column drops the teacher on the wrong rows.

**Scope.** The gate's scope is rows with a fresh q35_4b_E teacher from these sources:
- gd_gen_*;
- gd_gen2_json_fields, gd_gen2_long_policy and gd_gen2_tool_selection;
- gd_gen2_probability, choice rows only.

pg_*, hard_* and proc_* rows carry no teacher (they are in-sample for 4B-E), so they are out of scope.

| Source (yes/no) | Fresh teachers | Wrong, raw | Wrong, trained | Mid before | Mid after gate |
|---|---|---|---|---|---|
| gd_gen_numeric_dates | 8,242 | 41.8% | 41.9% | 80.0% | 38.2% |
| gd_gen_evidence_conflict | 7,700 | 33.8% | 33.6% | 50.9% | 17.3% |
| gd_gen_policy_exceptions | 8,356 | 28.8% | 28.8% | 39.6% | 10.8% |
| gd_gen_tables | 8,538 | 28.7% | 28.4% | 52.9% | 24.5% |
| gd_gen_ranking | 3,966 | 29.7% | 30.2% | 51.2% | 21.0% |
| gd_gen_constraints | 4,072 | 23.6% | 23.2% | 34.4% | 11.2% |
| gd_gen_msn_consent | 4,796 | 23.0% | 23.0% | 28.6% | 5.6% |
| gd_gen_msn_fault | 5,752 | 22.9% | 22.9% | 36.4% | 13.4% |
| gd_gen_msn_rules | 7,672 | 13.1% | 13.1% | 19.6% | 6.5% |
| gd_gen_routing | 4,084 | 8.1% | 8.2% | 12.8% | 4.6% |
| gd_gen_logic_negation | 10,685 | 7.1% | 7.1% | 11.2% | 4.2% |
| gd_gen_nlr_heuristics | 4,532 | 4.5% | 4.5% | 6.8% | 2.3% |
| gd_gen2_json_fields | 380 | 14.5% | 14.5% | 26.6% | 12.1% |
| gd_gen2_long_policy | 148 | 39.9% | 39.9% | 75.0% | 35.1% |
| **All yes/no in scope** | **78,923** | **22.7%** | **22.6%** | **36.7%** | **14.1%** |

**All generator yes/no rows, with or without a teacher (84,418).**
- Mid falls from **35.2% to 14.1%**.
- The SPEC's figures were 35.8% and 13.7%, measured on one account's shards only. These numbers are on the merged
  labels.
- The 332 gd_gen2_probability yes/no rows train on their exact probability through kd_full. They are out of scope
  on purpose; 53% of their targets are mid-zone by design.

**Choice rows in scope: 31,146 fresh teachers, 46.5% wrong (raw and trained).**

| Choice source | Wrong |
|---|---|
| numeric_dates | 69.0% |
| gen2_long_policy | 65.1% |
| ranking | 53.8% |
| gen2_probability | 52.7% |
| tables | 52.4% |
| evidence_conflict | 52.0% |
| constraints | 43.1% |
| policy_exceptions | 38.1% |
| routing | 34.4% |
| gen2_tool_selection | 28.6% |
| gen2_json_fields | 5.9% |

**What the gate does to the 2B file.** It is a dry run on the whole KD file; nothing was written.

| Measure | Without the exclusion list | With `--exclude-ids label_audit_known_bad_ids.json` |
|---|---|---|
| Teachers removed | 32,317 (17,846 yes/no + 14,471 choice) | 32,266 |
| kd targets | 449,957 → **417,640** | 449,957 → **417,691** |

Also:
- kd_full stays 238.
- The complement / inv consistency rules forced 0 extra rows.

**On arm A's S (dry run).**

| Measure | Without the exclusion list | With it |
|---|---|---|
| Gated rows | 3,949 | 3,946 |
| kd targets | 56,404 → **52,455** | 56,404 → **52,458** |
| Yes/no mid | 36.3% → 14.0% | 36.3% → 14.0% |

## 2. The 30-row audits (FINETUNE_PLAN 3.4 applied to three generators)

**Sample.**
- 30 teacher-vs-gold disagreements per generator: 20 yes/no + 10 choice. The seed is 20261001.
- Base rows only: role aff / choice with id `r_gd_<key>_<k>`. Near-miss bundles, definition swaps and attacked
  twins stay out (3.4).
- The pools the rows were drawn from:

  | Generator | Yes/no disagreements | Choice disagreements |
  |---|---|---|
  | numeric_dates | 2,799 | 1,640 |
  | evidence_conflict | 1,968 | 1,561 |
  | tables | 2,068 | 1,161 |
  | policy_exceptions | 2,004 | 855 |

**(a) Program re-derivation.** Each golden row is traced to its raw row (`raw/<key>.jsonl` line k). The text and gold
must match. The gold is then recomputed by the generator's own second implementation:
- **numeric_dates:** the schema's preds / preds2 / val2 / catv2 on `meta.orig_label.facts`, as in
  `gen_numeric_dates.recheck`.
- **evidence_conflict:** `ec_verify.independent_gold` plus `check_text`.
- **tables:** the generator is replayed in memory with seed 20261140. All 24,380 replayed rows were byte-equal to the
  raw file. `tab_verify.check_row` then re-parses the rendered table.
- **policy_exceptions:** the generator is replayed in memory. All 25,000 rows were equal to the raw file. Its
  `recheck` (outcomes2) then runs.

**(b) Reading.** I (Claude) read each row and derived the answer by hand. This is verification only; labels stay
program-made.

| Generator | Program re-derivation | Reading: gold right | §8.6 bar (≥ 27/30) | 3.4 action rule (≥ 15/30 wrong) |
|---|---|---|---|---|
| gd_gen_numeric_dates | 30/30 | **28/30** (2 wrong: one generator bug, below) | pass | not triggered |
| gd_gen_evidence_conflict | 30/30 | **30/30** | pass | not triggered |
| gd_gen_tables | 30/30 | **29/30** (1 ambiguous wording, below) | pass | not triggered |
| gd_gen_policy_exceptions (extra; named in SPEC 2.6) | 30/30 | 12/12 read | – | – |

**Verdict under SPEC 8.6: arm C may run.**
- Each of the three generators has at least 27/30 labels right.
- In the sampled disagreements the teacher, not the gold, is wrong in 28-30 of 30.
- So on these sources the teacher error rates in section 1 are real teacher errors, not label noise.

### Findings (confirmed with the generator code, and counted over the whole raw file)

**1. Generator bug in gen_numeric_dates (choice "letter" twins).**
- **What happens.** `Builder.make_pair` builds the question once, from the base facts
  (`qs = s.letter_q(base)`), and uses it for both rows of the pair.
  - When the flipped fact appears in the question, the twin's gold answers a different question.
  - `tz_deadline`: all 117 raw letter twins. The twin's zone is flipped, so the question names the base city while the
    text and gold use the twin's city.
  - `month_add`: 4 raw letter twins, where the instalment number is flipped.
- **Examples.** Audited rows r_gd_gen_numeric_dates_21641 and _571.
  - In both, the gold is the local time of the city in the text, but the question names another city.
  - The literal answer is not derivable from the text.
- **Why it slipped through.** `recheck()` re-derives gold from the facts but never checks the question. The yes/no
  modes build their question per row, so they are not affected. A scan of all 6,330 raw choice rows found no other
  schema with the problem.
- **Size.** 121 raw rows become **73 rows in the 2B file**:
  - 44 choice twins;
  - 26 near-miss yes/no bundle rows built on them;
  - 3 attacked copies.

  Of these, 70 have a fresh teacher and 4 sit in S.
- **Action.** Under FINETUNE_PLAN 3.4, "fix only confirmed bugs". golden_train is frozen and outside yn2b, so this is
  **flagged to the owner, not fixed here**.
  - The fix is small: build the letter / cat question per row, then regenerate.
  - The gate's `--exclude-ids yn2b/label_audit_known_bad_ids.json` keeps the gate from replacing a possibly-right
    teacher with the wrong gold on these rows.
  - Recommended for arm C and for any gated 2B file.

**2. Wording ambiguity in gen_tables.**
- **What happens.** Some claims are worded "The table gives X as the …" about a blank or Pending cell, under the
  refuted / enough / choice3 questions.
  - The generator treats the cell as unknown, so its golds are: not refuted / not settled / not enough information.
  - Read literally, the table does not give X, so the claim is refuted.
- **Size.** 19 raw rows become 12 rows in the 2B file. They are included in the exclusion list.
- **Example.** The audited case is r_gd_gen_tables_2311.
- This is a template wording issue, not a program error.

**Other observations (not errors).**
- **evidence_conflict.**
  - Negative reports worded in the future tense ("will no longer be within the reference range") count as a
    current negative report.
  - Value paraphrases (for example "not safe to drink without boiling" = a boil-water advisory) count as the same
    value.
  - Both are consistent with the cards.
- **policy_exceptions.** Some outcomes are counter-intuitive but literal. For example, deliberate damage is paid
  because the flood-cover exception lifts the covered-cause requirement. That is by design.

## 3. The teacher_gate tool (arm C)

**`yn2b/teacher_gate_2b.py`.** It makes the arm-C variant of any 2B training file and never modifies its input. The
rule, scope and consistency handling are in the module docstring. The rule is SPEC_draft 11 D1, carried into SPEC 10
D1.

- Unchanged rows are copied byte for byte.
- On gated rows, `meta.teacher` and `meta.teacher_src` are deleted. `meta.teacher4b` is kept, and
  `meta.teacher_gate = "dropped_wrong_side"` is set.
- It prints the kd-target count, which becomes `expect_kd_targets` of arm C, and the unchanged kd_full count.
- `build_ab_yn2b.py --arms B,C [--gate-exclude yn2b/label_audit_known_bad_ids.json]` applies it in memory to B's
  rows.

**Default: OFF (D1).** The owner said on 30 Sep: "RUN arm C, adopt only under the SPEC 11.6 rule".
