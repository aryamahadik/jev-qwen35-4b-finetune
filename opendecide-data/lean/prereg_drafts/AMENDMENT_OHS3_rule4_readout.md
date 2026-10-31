# Draft amendment to PREREG_OHS3 rule 4: the primary readout (A5)

**Status: DRAFT, written 2 Oct 2026. It is not in PREREG_OHS3.md and nothing is committed.**

**Source.** `prep89/READOUT_DEV.md` section (4) ("PREREG_OHS3 rule 4 change needed if read-twice is primary"),
with the A5 values from that file and from `prereg_drafts/AMENDMENTS_1oct.md` section 5.

**Why it is needed.** Rule 4 today says "Primary configuration: plain readout with the temperatures already fitted on
dev". The A5 serving readout reads choice rows twice, so it is not the plain readout. The rule must be amended before
the first OHS-3 run.

**When to commit:**
- Commit it **before the first OHS-3 call of any system**: Jev or OpenDecide, scored or timed.
- Commit it with, or before, the separate PREREG_OHS3 **model amendment**. That amendment names the shipped 4B and
  its adapter sha256 (TBD by gate job 3, `prereg_drafts/A8prime.md`), the config sha256, D1, D2, the endpoint and the
  cost rule.

**Everything here was chosen on dev only.** No OHS-3 item, prediction or score was opened.

**Fill before the commit:**
- `<date>`;
- `<shipped 4B>`;
- the `t_rule_check.py` output (item 3);
- the D1 choice (item 7).

---

> **Amendment to PREREG_OHS3 rule 4 (<date>, before the first OHS-3 run; owner approval in chat): the primary
> readout.**
>
> 1. **Primary configuration: the A5 serving readout.**
>    - **Choice rows are read twice:** in the given option order and in its exact reversal, one forward pass each.
>      - The two probability vectors are averaged per option name, in probability space.
>      - T_choice is applied after the average (`calibrate.scaled`).
>      - This is `decoder_io.predict(tta_choice=True)`. The harness uses `ohs3_lib.a5_read`, which equals it exactly
>        (`prep89/test_ohs3_prep.py` check 3).
>    - **Yes/no rows are read once.**
>    - **Band edge is never used on OHS-3.** The OHS-3 Brier uses the raw T-scaled probabilities.
> 2. **"Exactly once per model" still holds.** The two passes of a choice row are one decision in one run. No row is
>    re-asked, and nothing is chosen between the two passes.
> 3. **Temperatures: T_noul = 1.00 and T_choice = 1.00,** for the primary and for the single read. They come from one
>    fixed rule, fitted on pooled dev-select of the 9 gate splits:
>    - **Fit:** the grid 0.50-2.00 in steps of 0.05; the lowest gold-option NLL, taking the first T on ties.
>    - **Yes/no (A5 item 4):** ship the fitted T only if it is not 1, pooled dev-confirm yes/no Brier improves by
>      ≥ 0.002, and no split's yes/no Brier worsens by more than 0.003. Otherwise 1.00.
>    - **Choice (the READOUT_DEV.md rule, adopted here):** ship the fitted T only if it is not 1, pooled dev-confirm
>      choice NLL improves by ≥ 0.002 nats per row, and no split's choice NLL worsens by more than 0.005. Otherwise
>      1.00.
>    - **Computed by `prep89/t_rule_check.py`**, whose `--json` is the config's `T_fit_log`. It gives 1.00 / 1.00
>      for 4B-E and for C1:
>
>      | Model | Fitted T (yes/no / choice) | Yes/no Brier gain | Choice NLL gain |
>      |---|---|---|---|
>      | 4B-E | 0.90 / 1.00 | +0.0006 | 0 |
>      | C1 (choice from a proxy view) | 0.95 / 1.05 | −0.0002 | −0.0016 |
>
>    - **If C4 ships,** the same rule runs on C4's gate-job-3 standard read and its `--tta-choice` read
>      (`q35_4b_main500k_fix2_2v`) before this amendment is committed. Its output is the T written here.
>    - **The rule decides, not the owner.** If it gives a T other than 1.00, that value replaces 1.00 in this item
>      before the commit.
>    - Result for `<shipped 4B>`: T_noul = ____, T_choice = ____ (`T_fit_log` ____, sha256 ____).
> 4. **Secondary configurations,** from the same run:
>    - **"single read":** the identity-view probabilities with T_single (item 3). `ohs3_lib.a5_read` keeps both views,
>      and the harness writes `<name>_1v` and `<name>_1v_cal` from the same forward passes.
>    - **Batch calibration** (`batchcal.py`, unchanged), applied to the **primary** probabilities. Yes/no rows are
>      unchanged, as rule 4 already says.
> 5. **Drift (option-order twins).**
>    - The 149 reversed `_perm` twins are read in the same two orders as their base rows, so their drift is 0 by
>      construction.
>    - The pre-registered 304-pair endpoint is reported as written.
>    - Drift is also reported separately for the reversed (149) and rotated (155) twins
>      (`ohs3_final_table.drift_by_twin_kind`). The rotated twins are the informative number.
>    - The overlap between this readout and the way the twins were built is disclosed with the result.
> 6. **The speed and cost endpoints are measured with this readout.**
>    - It uses about 1.59× the forward passes of a single read on the OHS-3 call mix, from the counts in this file:
>      (1,016 yes/no + 2 × 1,440 choice) / 2,456.
>    - Its token count is higher than that, because choice prompts are longer. It is measured, not estimated.
> 7. **[D1, fill one]**
>    - **(served_h100)** The only OpenDecide OHS-3 pass is the timed pass on the H100 direct host. Its answers are the
>      scored predictions.
>    - **(L4_batch)** The scored run is the L4 batch run. The H100 timing replay's probabilities are never scored. They
>      are used only for the parity check against the scored L4 run: argmax agreement ≥ 0.99, mean max |Δp| ≤ 0.005,
>      max |Δp| ≤ 0.05.
> 8. **JevBench only (the public-item runs; no submission):** one read on every row, plus the band-edge yes/no
>    readout.
>    - The band edge maps P(yes) in (0.5, 0.8) to 0.8 and P(yes) in (0.2, 0.5] to 0.2. It is applied after T.
>    - It is disclosed as a scorer-aware readout with no fitted parameter.
>    - It is never used on OHS-3.
>    - JevBench public results are development-set results, not held-out ones.
> 9. **Disclosures, stated before the run:**
>    - The 2-view failed FINETUNE_PLAN 5.2's accuracy bar (+0.3 pp on choice; dev +0.10 [−0.48, +0.69]). It is
>      adopted for consistency, a different objective.
>    - On dev, the 2-view brings choice-order flips from 7.37% to 3.72% on rotated orders (4B-E), and the OHS-3-mix
>      drift estimate from 7.79% to 1.90%.
>    - It does not reduce the equivalence or complement flips.
>    - Reading yes/no twice cost accuracy on dev (4B-E −0.28 pp, main run −0.18 pp), so yes/no stays a single read.
>    - The main run's 2-view numbers came from a random second view (a proxy). The exact reversal was measured only for
>      4B-E.
> 10. **Unchanged:** rules 1, 2, 3 and 5, every endpoint, the statistics, "beats" and "matches", and the frozen files.
>     The model or models, with their sha256, are named in the separate model amendment, chosen without OHS-3.
