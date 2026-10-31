# T27 iteration 2: G6 diagnosis at 6,000 rows (no generator change made yet)

Scratch code and raw output: `families/T27/work_i2b/` (`build_infos.py`, `diag.py`, `chk_plan.py`, `yn_chk.py`, `diag_before.txt`,
`infos_before.pkl` = the 6,000-row in-memory build with the run_pilot_i2 setup, 3,135 choice + 2,865 yes/no).
Reproduced: choice c_card_without_question lr 0.3965 (bar 0.3533); yes/no d_meta gbt 0.5344 (bar 0.52).

## (1) c view, choice (ch_next): the driver is request/task word overlap, and the levels are still OFF

- `structure["ovl"]` is None on all 3,135 choice rows. `plugin._ovl_plan(...)` returns None for S1-S4 even with the 180 admitted forms
  (751 admitted forms, 105 of them supplement gate forms). So the rows are drawn without a level; "drawn before the label" is not in effect.
- Why `plan()` is None: beyond cells are all feasible (954 cells; band masses none 0.823, partial 0.169, high 0.009), but 16 of 52 do_step
  cells cannot print at `partial`. Missing partial gate forms (no (task form, request form) pair gives 0 < o <= 0.5; bands = high, none only):
  download.companion_app (task.app), purchase.class_place (task.book), purchase.premium_bundle (task.buy), download.attached_file
  (task.download, task.dlshare), enter_credentials.partner_portal (task.portal), change_settings.public_profile (task.public),
  save_payment.card_account (task.renew, task.savecard), send.contact_details (task.senddetails). Stage 2 rejected the partial candidates
  of these 8 actions.
- Overlap is read straight from the label: one-feature CV accuracy (chance 0.333): o_max 0.809, o_mean 0.806, band_max 0.738.
  band_max = none -> continue 0.92 / do_step 0.08 / stop 0.00; partial -> stop 0.59, do 0.24, cont 0.17; high -> do 0.87.
  Mean o by class: stop_ask 0.204, continue 0.030, do_step 0.360. Same-kind request vs task kind: do_step 0.76 vs 0.12 for beyond rows.
- A row-level multinomial n-gram LR (context uni+bigrams, min_df 30) scores 0.526; top n-grams are verb/object phrases of the request forms
  and task clauses (continue: "this account", "account on", "kind of", "send this", "share this", "to public", "newsletter", "partner";
  do_step: "affiliate mailing", "your accountant", "your card", "replying to", "unlocked after"; stop_ask: "<item> will" (size/date/fee/
  sample will ...), "the new", "accountant", "attached"). A linear model on word presence reads redundancy: when the request is in scope its
  words repeat the task's, so fewer distinct content words are present.
- Not drivers (class mix flat, one-feature CV <= 0.36): the verb pair (each pair 0.30-0.40 per class), layout/format_style, position of the
  request lines (pos1 0.48, pos2 0.71 in every class), request length (13.0 tokens in every class), imperative markers (0.08-0.10), number of
  requests (always 2, both gate forms), info line kind, task and action identity. Gate = target: stop 0.65, continue 0.00, do 0.35 (the rule
  itself; each row holds exactly two distinct item phrases, so presence-only features cannot see it).
- So verb identity is not the leak: action marginals are equal by beyond_joint. The leak is the realised overlap (in scope: o 0.5-1.0 on
  459 of 548 combinations; beyond: 0 on 87%), which the level mechanism exists to cancel.

## Fix design (by construction; not yet applied, backups of the earlier state are in `../_backup_i2/`)

1. `overlap.plan`: when a do_step cell cannot print at an active level, drop that level (re-split each beyond cell's mass over the remaining
   feasible bands) instead of returning None. With `partial` dropped the levels are none 0.99 / high 0.01, every do_step cell supports both
   (checked: all 52 have none and high), so levels turn on without new Haiku wordings. Return None only if some beyond cell has no band left.
2. `overlap.steer`: one request-form pool per (action, level) for BOTH scopes. Pool = forms in band L against every (task, task form) that
   allows the action; a beyond row draws from the same pool, filtered by its realised band against its own task. The supplement forms then
   appear in beyond rows at the same rate as in-scope rows (today an in-scope row at none can use only supplement forms, a beyond row at none
   also uses the 0-overlap originals: a new form-identity cue). Task form: draw from the task forms feasible for the in-scope cell, for every label.
3. Re-run pilot + G6 at 6,000 and read c lr again; the n-gram table above is the check.

## (2) d_meta, yes/no: card length, state length and line count carry task kind and request count

- `meta_drivers`: len_card+qform 0.561, len_state+qform 0.530, len_ins 0.515, len_q 0.515 (G6 gbt 0.5344, lr 0.5068).
- Yes rate by structure, which meta features read through the printed allowed list and the number of content lines:
  - read-only task (allowed list = "reading the content" only, shorter card): yn_beyond yes 0.820 (n=172) vs 0.456 otherwise; yn_within 0.000
    (n=96) vs 0.541; yn_not_beyond 0.309 vs 0.546.
  - number of allowed actions (card length): yn_beyond 1 -> 0.548, 2 -> 0.425; yn_within 1 -> 0.417, 2 -> 0.591; yn_dneg_beyond 0.571 / 0.394.
  - number of requests (n_lines, len_state): zero requests gives no (beyond forms, n=52) or yes (yn_not_beyond, n=45); two requests tilt
    yn_not_beyond / yn_within to no (0.41).
  - card style (len_card): full cards yes 0.58 on yn_beyond inline, 0.50 elsewhere (a card-level yes rate 0.2-0.8 meets a style Kronecker draw).
- Fix by construction (needs a decision, see below): draw (task kind: read-only / one allowed action / two allowed actions, number of
  requests, card style) from the seed BEFORE the label and give each the same label distribution inside every qform: read-only tasks only with
  qforms whose gold is not forced (drop read-only from yn_within, or add no-request rows with a neutral filler line so state length does not
  move), and pad the content so len_state / n_lines do not depend on the request count.
  This changes sampler weights (p_readonly, p_zero) and the skin's filler count, so it moves G0 numbers and G10 cells: not applied in this pass.
