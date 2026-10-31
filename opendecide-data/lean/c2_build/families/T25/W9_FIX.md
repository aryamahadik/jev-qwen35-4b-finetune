# T25 A49 (d) fix round (W9, 17 Oct 2026)

Failing binding full-generation gates before the fix (GEN_REPORT of 16 Oct, seeds 33M / 34M / 35M): G7 (choice feature `opt:24`,
28 gold of 40 rows, p 1.0e-6; next `opt:january` 54 of 89, p 4.1e-6) and G11 (five `yn_claim` wordings at 2.1-2.8% of 901 rows).
G6 (A50) passed. No label was changed, no wording or G6 feature dropped, no bar touched.

## Causes (found on a 6,000-row rebuild of the failing QC seeds, dump in pilot_vm/dump_b34000000.jsonl)
1. G7: the `member_value` twin (`_member_values`) offered two FIXED extra values: 2026-01-05 and 2026-07-24 for date packs, the
   first two pool values for cents / count packs. Such a twin's new gold is one of them, and they were never a wrong option, so
   the tokens "24", "january", "2026" (and the first pool values) were gold in the twin rows. Base rows were clean (gold has the
   token 12 of 37 = null); twin rows 21 of 27. Row-level cluster noise did not explain it.
2. G7 near miss (not failing, z = -3.4, base rows -4.0): the error model `t25_first_listed` on `ch_source` always names the
   first-listed source, i.e. Source A when ids are letters: A was shown on 74% of letter-id rows (B 62%) but gold on 15% (B 19%).
3. G11: wording choice was a plain per-row hash draw, so the 34 yn_claim wordings (369 rows, 41% of the family, because the 14
   dneg wordings are all A43 (f) forms and their draws were redrawn as yn_claim) were spread unevenly (max 25 rows = 2.77%).

## Generator fixes (plugin.py; old plugin in _backup_w9/)
1. `_member_values`: extras are label-blind draws like every other value: four dates from a hash of (sampler, seed, member, j)
   uniform over the 540-day value span; for cents / count the whole pack pool. A twin's new gold is now exchangeable with the
   wrong options.
2. `t25_first_listed` returns no answer on `ch_source` (still used on `ch_value`, where the value is not positional).
3. Wording balancing: `_pick_wording` / `_wording_plan`. A base question form (yn_claim, ch_value, ch_source) of a training
   sampler takes the wording its seed is assigned in a 1,024-seed block: the seeds that draw the form, over all training
   samplers in (seed, sampler) order, each go to the admitted wording with the smallest load so far (ties: a hash order), a
   seed's load being the rows its unit is expected to write with that form (1, + 0.8 for a hash-drawn twin, + 1 for a hash-drawn
   equiv / attack partner, which share the base wording). So every wording carries nearly the same number of rows along the
   seeds. Partner forms (yn_claim_not / wrong / other, chosen by the pipeline) and S5 keep the plain hash draw. The plan reads no
   structure and no gold. Check: in 900-row windows of a 6,000-row build the plain draw gave a max wording of 25 rows (2.77%).
4. `BASE_SHARES`: yn_claim_dneg (0.04) moved to yn_claim (0.42): the same effective distribution as before (A43 f made every dneg
   draw a redraw to yn_claim) but without scattered redraw seeds, so the balancing sees the real seed order. test_plugin.py
   (old copy in _backup_w9/) now expects dneg not to be drawn and checks that it still renders and solves.

G0_SPEC.md and its sha are untouched (the spec's semantics, forms and shares of the other forms are unchanged).
