# score_ohs3.py: where PREREG_OHS3.md is silent (draft for the owner, 1 Oct 2026)

`score_ohs3.py` follows `PREREG_OHS3.md` (lines 118-156). Where the text leaves a choice open, the scorer makes the
choice below. The choices were made without looking at any OHS-3 data or result. To make them binding, commit them as a
PREREG_OHS3 amendment **before** the first OHS-3 run, or change the code first.

| # | Open point | What score_ohs3.py does | Why |
|---|---|---|---|
| 1 | Which tests are in the Benjamini-Hochberg family | 25 tests: accuracy on track F and on track U; accuracy on >26 options; complement violation; option-order drift; micro, macro and Brier with batch calibration; accuracy on each of the 13 tasks; accuracy on OHS-A and on OHS-S; exact McNemar against each Jev run. Not in the family (reported with a CI and a raw p): the "also reported" values (mean \|P+P-1\|, accuracy on `_neg` rows, TV distance, accuracy on `_perm` rows), each Jev run's own numbers, and run-to-run agreement. | The PREREG lists these under "Secondary endpoints". The "also reported" values read as description. |
| 2 | Verdicts for secondary endpoints | For the 3 batch-cal primaries, the PREREG beats/matches rule, using the BH q in place of the Holm p. For the others: `od_better` if the CI is above 0 and q < 0.05; `jev_better` if the CI is below 0 and q < 0.05; otherwise `no_clear_difference`. | The PREREG defines beats/matches only for the primaries. It gives no margin for the consistency endpoints. |
| 3 | "Matches" when the whole CI is below 0 (example: [-1.5, -0.2] pp) | Label `matches`, as written: beats, then matches, then "Jev is better". The flag `ci_below_0` is also printed. | Follows the written order of the rule, without hiding that Jev is ahead. |
| 4 | Jev's Brier, given "mean of the two runs, computed per row" | Each run's Brier on the row, averaged over the 2 runs. This is not the Brier of the averaged P(yes), which would be lower. | The PREREG averages the score per row, not the prediction. |
| 5 | Jev's consistency values | Each pair is scored inside each run, then averaged over the 2 runs. | Same rule as #4, applied to pairs. |
| 6 | Missing answers in the "also reported" values | A missing P(yes) scores \|P+P-1\| = 1. A missing or all-zero option vector scores TV = 1. | Missing answers count as the worst case, as in the Brier rule ("no probability scores Brier 1"). |
| 7 | The TV probability vectors | Each vector is restricted to the row's options, matched by option name, and renormalised. Keys that are not options, such as Jev's `_raw_sum`, are ignored. | Has no effect on well-formed predictions. Guards against stray probability mass. |
| 8 | What counts as "missing" | No prediction record. On yes/no, no `yes` key. Or any probability that is not a finite number. On choice rows, an option missing from the record gets 0. If every option is 0, the row is a tie. | Matches how `run_jev.py` writes predictions. |
| 9 | Tie test | Exact float equality: equal top probabilities, or P(yes) == 0.5 exactly. | This is what the PREREG says. |
| 10 | Per-half and per-track accuracy | Estimated within the one shared bootstrap: only the rows of that half or track count, out of each resample of all groups. `--half S` instead filters the rows first and bootstraps only S, as `score_ohs.py` did. | "Same bootstrap". The two methods differ only in variance detail. |
| 11 | Differences exactly 0 in a resample | A resampled difference within 1e-9 of 0 is recomputed in exact fractions. An exact 0 then counts in both tails of p. | The PREREG's p formula counts ties on both sides. Floating-point noise in the macro mean broke that in `score_ohs.py` (see the OHS-2 check). |
| 12 | McNemar | Base rows only. OD's correctness against one Jev run's correctness. Exact binomial test, two-sided. It ignores the 31 near-duplicate clusters. | This is the test the PREREG names. |
| 13 | Jev run-to-run agreement | Two values. **Decision**: both runs give the same answer, not a tie and not missing. **Correctness**: both runs right, or both wrong. Correctness is `score_ohs.py`'s old number. | The PREREG does not define it. |
| 14 | Duplicate ids in a prediction file | The last record wins, as in `score_ohs.py`. Duplicates are counted in the output. | |
| 15 | Batch calibration inputs | Not changed by the scorer. Note: `batchcal.py` estimates each label set's prior from **every** row of the split, including the 304 `_perm` twins. Those twins have the same option set as their base rows. | The PREREG says "from unlabeled inputs", and the twins are unlabeled. Flagged so the owner can decide before the run. |
| 16 | Speed and cost | Not scored. The PREREG defines neither. See `speed_cost_definition.md`. | |

Hard stops for `--split ohs3`: the frozen sha256 of `ohs3.jsonl` and `ohs3_relations.jsonl` must match; the PREREG counts
must match (2,456 rows, 1,852 base, 13 tasks, 1,806 groups, 716 yes/no, 284 rows with >26 options, 300 `_neg`, 304
`_perm`); there must be exactly 2 Jev runs; and a missing prediction file is an error. `--allow-deviation` turns the
first three into deviations recorded in the output. Never use it for the reported run.
