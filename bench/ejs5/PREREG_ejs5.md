# PREREG_ejs5: OpenDecide vs Jev on the ejs-5 benchmark (DRAFT)

Status: **DRAFT, not adopted.** It takes effect only when the owner says so and it is committed. That must happen
before any model reads a benchmark row. Nothing in this draft was chosen by looking at item text, gold labels or any
OpenDecide prediction on these items. Agents have read only code, the README, metadata and counts.

## 1. The test

- **Benchmark:** `github.com/ejs-5/jev-benchmark` (MIT), copied to `bench/external_quarantine/ejs5/`, which is
  git-ignored. It has 868 decisions about commits of one public repo (n8n). The labels are mechanical, taken from git.
  The four tasks are class-balanced by the author.

| Task (file key) | Rows | Question type | Label source (author's build_public_dataset.py) |
|---|---|---|---|
| Route (`route`) | 180 | choice, 2 options (frontend / backend) | which package tree the commit touched |
| Triage (`triage`) | 148 | choice, 4 options (fix / feat / refactor / test) | the conventional-commit prefix |
| Size (`score`) | 360 | 4 ordered levels (tiny / small / medium / large) | lines changed (20 / 100 / 500 cut points) |
| Risk (`gate`) | 180 | yes / no | the commit touched CI, docker, migrations or build config |

- **Rows file:** `convert.py` builds `ejs5_rows.jsonl` with 868 rows over 622 commits. Its sha256 is
  `7128b2b8545913fa263f6f4bbdcd0049b2368e0402d74a6516e51f24197b3a4f`.
  - The task text is taken verbatim from `run_public_bench.py` by AST: the question (`ask`), the criteria and the level
    names.
  - Each row's state is the item text exactly as the author sent it to Jev.
  - Route and Triage options are the criteria keys, each shown with its criterion.
  - Size options are the four level names, each shown with the author's criterion for that level.
  - Risk is a yes/no question with no definitions card. Jev's request had no criteria either.
- **Input sha256** (also in `ejs5_rows.jsonl.meta.json` and in the scorer's JSON output):

| File | sha256 |
|---|---|
| `run_public_bench.py` | `09e7cd23971813253c03e51cf00463045e2c8006d08903a697cff38537de5229` |
| `public_route.json` | `6f4b59d7e7bf287be612ce4196067548cbbd3be196d6c82ed7d49629361f4475` |
| `public_triage.json` | `6ac26bfc5e7117d4d7274dbb9edbe42ec45d3922830a03ed52ce2851efad3c31` |
| `public_score.json` | `0a709163f47af3726326205a74f355968510c8af8dad54f68d6b6914ea38f2e2` |
| `public_gate.json` | `f0d486ef217299fd541e61f57092de4ab5ab474aafc98addb041d5c84969cb43` |
| `commit_dates.json` | `f07180eadc950b2ce49259e01a5b11e4b7291359e660d9e7289dd84c35e15ed0` |
| `public_raw.json` | `170564b41ef1a435c23964bb1f25dbafe979b15758b383baba1f1ec14dd160ba` |
| `public_summary.json` | `e715569c0eb59ed675b29aff7b4e04235b2090c0a0e59c8817d96870fc66c779` |

## 2. Systems (each runs once)

| ID | System | Identity |
|---|---|---|
| **S1 (headline)** | C1 = `q35_4b_main500k`, the shipped 4B (PREREG_FINAL A10) | `Qwen/Qwen3.5-4B` @ `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` + LoRA `adapter_model.safetensors` sha256 `507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078`; layout `schema_branch_mark`, style `cygnet`, no PRISM-X |
| S2 | the shipped 2B (PRISM-X I) | `Qwen/Qwen3.5-2B` @ `<revision>` + adapter `<name>` (sha256 `<…>`) + `prism_x.safetensors` (sha256 `<…>`). **Named by an amendment before its run.** The amendment may only fill in the model the main plan ships; it cannot change anything else in this file. |
| S3 | cascade S2 → S1 | Rule `prep89/ohs3_lib.cascade_answer` (copied in `ejs5lib`; a test checks they are equal). `tau`, `w_big` and `route_on` come from the **dev-only fit of this pair** (`prep89/cascade_rule_fit.py` output, sha256 `<…>`, named by the same amendment). The existing fit `cascade_fit_dev_armI1600_to_pxE.json` is for another pair, so the kit refuses it. The cascade is composed offline from the S1 and S2 runs, with no new model read. |

- **R1, report-only reference:** 4B-E = `q35_4b_pxE` (`Qwen/Qwen3.5-4B` @ `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` + LoRA
  `adapter_model.safetensors` sha256 `1bbd8a79143f7ab5d6fd538c870ded0605120ab777c97d38ca3384b26c31a3f9`), same readout,
  run once. It is a comparison row only.
- **ejs-5 never chooses a model.** The shipped 4B is C1 by A10. Any later 4B candidate (e.g. a weight-softened or topped-up
  C1) is decided only by the dev gate rules; ejs-5 numbers can never be used to pick between models or settings.
- **Jev:** `typesafe/jev-1.13`'s per-item answers as published in `public_raw.json`. There are no new Jev calls.
- **Context only, no claim:** GPT-5.6 Terra and Claude Opus 5, from their published per-item answers.

## 3. Readout (fixed)

- Each row is read in its own forward pass: batch 1, eager, on the L4.
- Probabilities come from `decoder_io.cand_logits` and then `decoder_io.to_probs` at **T = 1**.
- **Choice rows (route, triage, size):** read twice, given order and exact reversal, averaged in probability space
  (`--readout 2view`, the shipped A5 readout). **Yes/no rows (risk):** read once. The identity view is kept as `probs_1v`.
- Nothing else is applied: no temperature, no calibration, no TTA, no prompt change, no tuning of any kind on these
  items.
- The model is loaded with `decoder_io.load(base, adapter=…, revision=…)`, then `merge_and_unload`. This is the same
  load path as od_gcp and ohs3_backends.

> **Owner decision (3 Oct 2026): option b, the shipped A5 readout** (`--readout 2view`): choice rows are read twice
> (given order + exact reversal, averaged in probability space), yes/no rows once, T = 1. This is the readout A10 names
> for C1. The single read of the same run (`probs_1v`) is reported as a secondary number only; it is never used for a
> claim.

**From probabilities to the author's answer** (`ejs5lib.decide`; tests check it against the author's own `jev_pred`):

- **Route, Triage:** the argmax. On an exact tie, the first option wins.
- **Size:** the expected level E = Σ i·p_i over the 4 ordered levels. The answer is
  `LEVELS[max(0, min(3, int(round(E))))]`, the author's rounding and clamping for Jev's Score answer.
- **Risk:** "yes" if and only if P(yes) ≥ 0.5, the author's cut for Jev's yes/no answer.

## 4. Run once

- Each system is run exactly once on all 868 rows, on `od-l4`, after the owner's OK.
- `run_ejs5.py` refuses to run in these cases:
  - a second run under the same name;
  - a second completed run of the same adapter weights under any name;
  - another process is using the GPU;
  - the adapter, `prism_x` or rows sha256 differs from this file;
  - the base revision is missing.
- A run that crashed (started, never completed, nothing scored) may be restarted with `--restart-crashed`. The
  restart is disclosed.
- Partial predictions are never looked at.
- The run script reads no gold label and prints no accuracy. Scoring happens afterwards on the Mac.

## 5. Scoring (`score_ejs5.py`, exactly the author's)

- **Accuracy per task** uses the author's own `summarize()`, compiled from `run_public_bench.py` by AST. It is
  hits / n, and a row with no valid answer counts **wrong**.
- **Self-check, done:** the scorer reproduces all 12 published model × task accuracies (Jev, GPT-5.6 Terra, Opus 5)
  from `public_raw.json` using our rows' gold. 0 stored labels differ from our gold.
- **Published reference on these 868 rows:**

| | Pooled (868) | Macro (mean of 4 tasks) | From 2026-06-01 (268) |
|---|---|---|---|
| Jev 1.13 | 58.53 % (508) | 64.40 % | 45.90 % |
| GPT-5.6 Terra | 61.06 % | 66.85 % | 50.75 % |
| Claude Opus 5 | 68.09 % | 74.20 % | 61.57 % |

## 6. Comparison and claim rule

- **PRIMARY endpoint, per system:**
  - **What is measured:** pooled accuracy over all 868 rows, ours minus Jev.
  - **Interval:** paired bootstrap over the **622 commits**. A commit that appears in several tasks carries all its
    rows. It uses 10,000 resamples with `numpy.random.default_rng(0)` and a percentile 95 % interval.
- **Claim rule:**
  - "Beats Jev on ejs-5" only if the interval's **lower bound > 0**.
  - "Jev is better" if the upper bound < 0.
  - Otherwise it is a **statistical tie**, reported as a tie whatever the sign of the point estimate.
  - For scale: GPT-5.6 Terra − Jev is +2.5 pp [+0.1, +4.9], and Opus 5 − Jev is +9.6 pp [+6.8, +12.4]. A win needs
    roughly +2.5 to +3 pp.
- **Each system is reported:**
  - S1 is the headline.
  - S2 and S3 use the same rule for their own claims.
  - All three are reported; none is selected as the "best of" the three.
- **Secondary results (reported, not headline claims):**
  - per-task differences, with the same bootstrap within the task, labelled secondary (4 comparisons, no multiplicity
    correction);
  - macro accuracy;
  - the **late subset**: the 268 rows (193 commits) whose commit date is on or after 2026-06-01 in
    `commit_dates.json`. One row has no date and is left out of the subset;
  - descriptive paired differences vs GPT-5.6 Terra and Opus 5;
  - the author's confidence bins;
  - model time per row.

## 7. Disclosures

- **Noisy labels.**
  - What sets each label is not in the text: the package tree touched, the commit prefix, the churn bucket and the
    files touched. The model sees only the commit prose, with paths and giveaway terms stripped.
  - The ceilings are well below 100 % for every model. Opus 5 gets 68 % pooled.
- **The Size task is near chance for everyone.**
  - Chance is 25 %. Jev gets 37.2 %, GPT-5.6 Terra 40.0 % and Opus 5 45.8 %. The keyword regex gets 25.3 %.
  - Its 360 rows are 41 % of the pooled endpoint, so macro accuracy is also reported.
- **One domain.** All rows are commit messages of one repository (n8n), in English, from one team's writing style. The
  rows are class-balanced by construction, not at natural rates.
- **Jev's numbers are the author's single run** on the OpenRouter decisions API: one date, jev-1.13. They are not
  re-collected. Jev's 1 unanswered row counts wrong, by the author's rule.
- **Not the same harness.**
  - Jev got the item text with a typed question (choice criteria, the Score criteria list, yes/no instructions).
  - Our models get the same question and criteria text in their trained prompt layout (`schema_branch_mark`, lettered
    options).
  - The frontier models got "name = description" options in a JSON prompt.
- **Overlap.**
  - A counts-only 13-gram and exact-text check of all our train and dev jsonl found **0 of 868** items with any match.
    That covers 640 files and 5.6 M records.
  - 163 records mention "n8n", and 4 contain an 8-hex string equal to a benchmark commit prefix. Neither is a text
    overlap.
  - The Qwen3.5 base models may have seen n8n's public history in pretraining. The late subset is reported as a guard
    for that.
- **No speed claim from this test.**
  - Jev's 411–432 ms medians are end-to-end API times.
  - Our timing is L4 prefill time per row (batch 1, eager), with no network.
- **The author is not neutral.** Their README says so. We did not build the benchmark and we tune nothing on it.

## 8. Frozen code (sha256)

These are the draft's values. Re-check them at adoption; any code edit after adoption needs an amendment.

| File | sha256 |
|---|---|
| `bench/ejs5/convert.py` | `6c63f101f19dac4333a8417c823fa8a0ff14ff7984f798f1f53a3a2ec13409b0` |
| `bench/ejs5/ejs5lib.py` | `c621243a06a410c17d51bf20911efe9427123b79b20c2506ac5f9782690c5962` |
| `bench/ejs5/run_ejs5.py` | `3a8645d35d40adf2b860b79d731faadae331421e0ec9b1fd453d01e94522226b` |
| `bench/ejs5/score_ejs5.py` | `33a4d89fdca7e35ec678eaa15436bca6597a7c25911661ef29f3e2f00e459721` |
| `opendecide-data/lean/decoder_io.py` (tag `final-frozen`, 82b07d4) | `8ba8ff4fb35389c76bb2d0851f66ef4822059d43fe4bef1ca582fcf21c5755cc` |
| `opendecide-data/lean/prism_x.py` | `3c4425bfde62182c997960ef68d43232df65ba28031608acde0b9dc8ba87b4fe` |

The run manifest records the sha256 of every code file actually used on the VM. A VM `decoder_io.py` or `prism_x.py`
that differs from these values voids the run. Check before the run: `sha256sum ~/lean/decoder_io.py ~/lean/prism_x.py`.

Commands and time: see `README.md`.
