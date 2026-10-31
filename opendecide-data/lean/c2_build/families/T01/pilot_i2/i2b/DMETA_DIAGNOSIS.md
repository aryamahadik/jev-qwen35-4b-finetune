# T01 iteration 2: choice d_meta lr 0.3621 (bar 0.3620) at 6,000 rows: diagnosis

No plugin.py, G0 or pool file was edited. Stage 3 was NOT re-run: nothing changed, the build is deterministic, and the
diagnostic build below reproduced the failing cell exactly (lr 0.3621, gbt 0.3444, n = 2,883 choice rows, chance 0.3420).

Scripts (all in `families/T01/`, read-only analysis; data in this folder):
`i2b_dmeta_diag.py build|rank` -> `choice_rows.json`, `DMETA_DRIVERS.json`; `i2b_dmeta_ablate.py` -> `DMETA_ABLATION_choice_rows.json.json`;
`i2b_dmeta_null.py` -> `DMETA_NULL.json`.

## What the d_meta LR can actually use
Row-level numerics (len_state, len_ins, mag_*, ...) are constant across a row's options, so they add the same amount to every
option's score and cannot change the argmax. Only these vary within a row: option tokens (o:/o2:), the option features
(clen, tlen, len_rank, is_longest/shortest, has_digit; abstain/neg/verbatim are ~0), and the crosses
`m:<cat>=<value>|neg|abs|lr<bucket>` (a row-level category x the option's length-rank bucket). T01 options in the date forms
have equal text length, so len_rank is the display position (stable sort).

## Univariate association with the gold role (all within noise)
- Gold position / length rank, by k: uniform (k=3: 513/466/483; k=4: 216/231/193/207; chi2 2.2 for k=3).
- Gold is longest / shortest vs the label-blind expectation: -0.26 pp / -0.33 pp. Abstain, neg, verbatim: 0.
- Pick-by-feature accuracy vs chance 0.342: longest 0.333, shortest 0.332, first 0.352, last 0.340.
- Position by (qform, k): only ch_first_day|k4 (p 0.009; [44,51,30,25]) and ch_days|k4 (p 0.04; n 42) dip, out of 13 cells.
- Row-level categories vs gold position, stratified by (qform, k) and de-duplicated by (card, options, gold): wording chi2/dof 1.4,
  skin 1.3, register 1.5 (unit partners share wording, skin and position, which inflates chi2), pack 1.2, sampler 0.7, qform 0.7.
- Closed set ch_cash_which gold labels (n 353; expected 88): both 84, neither 97, withdrawal 97, deposit 75; chi2 4.0, dof 3, p 0.26.
  They come from `_draw(rng.random(), CASH_TARGETS)` (an i.i.d. draw), so a dealt label would reduce variance, not remove a bias.

## Leave-one-group-out of the d_meta LR (full 0.3621)
without option tokens 0.3517; without option features 0.3562; without cat:wording 0.3489; cat:pack 0.3583; cat:author_mode 0.3590;
numerics 0.3614; sampler/skin/register/qform/format_style/defs_style/attack 0.3635-0.3646.
Only option features 0.3396; + tokens 0.3486; + wording cross 0.3614; + sampler cross 0.3618.

## The cell is noise-dominated
Permutation null (gold position re-drawn uniformly per row, same folds, 6 draws): 0.3493 0.3177 0.3528 0.3285 0.3365 0.3541;
mean 0.3398, SD 0.0148. The data has 56 cards (51 rows per card), so the card-grouped 5-fold CV is very noisy. 0.3621 is +1.5 SD
above the null mean; iteration 1 was 0.3523. A real signal of about +1 pp may exist (option tokens + wording crosses), but I found
no feature whose gold-role imbalance is above sampling noise, so there is nothing to balance by construction that I can defend.
A kit-choiceplan change would be a no-op here (position and rank are already drawn label-blind from the row key); any change that
re-rolls the rows would move this cell by about +-1.5 pp at random, which would be luck, not margin.

## Options for the orchestrator
1. Deal the ch_cash_which label (and the rank/position) in stratified blocks instead of i.i.d. draws (small variance reduction; honest, cheap).
2. Judge G6 for this cell against its permutation null (SD 1.5 pp at 6,000 rows with 56 cards): the bar (chance + 2 pp) stays as is.
3. Add cards to the 6,000-row sample (more groups, less CV noise) if the pools allow it.
