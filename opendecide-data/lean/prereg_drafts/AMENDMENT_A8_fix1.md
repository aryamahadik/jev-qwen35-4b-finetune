# Draft amendment A8 (for PREREG_FINAL.md): candidate C4 = q35_4b_main500k_fix1

> **SUPERSEDED (2 Oct 2026) by `prereg_drafts/A8prime.md` (A8′, C4 = `q35_4b_main500k_fix2`). Do not commit this
> draft.** Fix1 was never launched and no fix1 model exists. Kept unchanged below for the record.

**Status: DRAFT. It is not in PREREG_FINAL.md yet.**
- Append the quoted block below to the end of PREREG_FINAL.md, then commit it.
- Commit it **before the top-up is launched**. The hard deadline is before the first C4 prediction. Committing before
  the launch also fixes the data, the lr and the step count before any training curve exists.
- `gate/gate_4b_fix1_l4.sh manifest` refuses to run until HEAD's PREREG_FINAL.md contains "Amendment A8".
- Commit in the same commit: `runs/q35_4b_fix1.json`, `extra/build_fix1.py`, `extra/fix1_spawn.py`,
  `extra/fix1_dryrun.py`, `gate/gate_4b_fix1_l4.sh`, `gate/check_adapter_fix1.py`, `gate/check_unseen_fix1.py` and
  `gate/tests/sim_gate_fix1.py`, plus `data/v14_parts/fix1_counts.json` (34 KB: the built files' sha256, which the
  launcher and `gate/check_adapter_fix1.py` read). Then put the commit id in the block.

---

> **Amendment A8 (1 Oct 2026, __:__ UTC, before C4 trains; owner approval in chat): a top-up of the new 4B, candidate C4 = `q35_4b_main500k_fix1`, and one new ship look.**
>
> **Disclosure.**
> - Ship look 1 was made on 1 Oct at 21:11 UTC (`logs/gate4b/look_ship1.txt`). It gave DO NOT SHIP (FINAL) for
>   C1 = `q35_4b_main500k` vs `q35_4b_pxE_fresh`.
>   - The primary test passed: +2.47 pp [+1.31, +3.70].
>   - Every constraint passed except (e), the equivalence flip rate: 8.86% vs 5.68% (n = 722 pairs). The limit is
>     REF + 2 pp = 7.68%.
>   - The extra flips come from the devp_card aff / double-negation pairs: 12.1% vs 4.8%.
> - Under §5.7 the fallback is 4B-E. The owner chose to repair the new 4B instead.
> - **This fix was designed after seeing a dev constraint fail.** Only dev splits were looked at. No held-out set was
>   opened: not OHS-1, OHS-2 or OHS-3, not golden_dev, not JevBench half B.
> - The design used one fact about the training data (no dev rows were read for it). golden_train has 1,107 'dneg'
>   rows out of 501,732 (0.22%). The REF lineage had 1.6-4.5% (train_v11 4.49%, train_prism_arms 2.75%).
>
> **C4: training.**
> - C4 is a continued fine-tune of C1's adapter.
>   - The init adapter is C1, byte-identical to the gated read: `adapter_model.safetensors` sha256 `507d1c29…`.
>   - Config: `runs/q35_4b_fix1.json` (every key written out). It is launched by `extra/fix1_spawn.py`.
>   - The code is the frozen code of the main run (train_decoder / decoder_io / prism_x / writeblock sha256 equal to
>     C1's train_meta "code").
> - **What stays the same as C1:** LoRA r16 / alpha 32 with the QWEN35 targets, layout E (schema_branch_mark, cygnet),
>   and the same loss and kd settings (lam 1, beta 1, kd 0.5, blend50 skipped, lam_inv 1, sym_cons, perm_twin 0.3,
>   lam_p 0.5, aux_norm batch, micro_tokens 8192).
> - **What is new:**
>   - The optimizer is fresh.
>   - lr peaks at 2e-5, with a 5% warm-up and then cosine to 0. That is the trainer's fixed schedule; the mean lr is
>     1.0e-5.
>   - One pass is 1,867 steps at batch 16 (`replay_steps.py`), with seed 20261001.
>   - There are no snapshots.
>
> **C4: data.**
> - The files are `data/v14_parts/fix1_train.jsonl` (31,183 rows, sha256 `6354355b2391dee3…`) and
>   `fix1_relations.jsonl` (7,740 relations, sha256 `1139f722bc1b3997…`). They are built by `extra/build_fix1.py` from
>   whole units, with every row copied byte for byte.
> - The file has three parts:
>   - **yn2b polarity units: 4,914 rows (15.8%).** These are every yn2b latent with a negated view: all of F4, plus the
>     F1 / F2 / F6 ladder latents. The labels come from the programs (gold only, no teacher).
>   - **golden_train double-negation units: 2,880 rows (9.2%).** The main run already trained on these rows.
>   - **Stratified golden_train replay: 23,389 rows (75.0%).** The replay is seeded per source and drawn in proportion
>     to each source's rows.
> - **There is no dev data in the file.** The decontamination covers every row of the file and was re-checked from
>   disk:
>   - **12-gram check:** 0 hits against the 9 gate splits, devzs2, debate_dev, hard12/proc12/planted12_dev, dev_hc, the
>     yn2b dev files, all 8 eval sets, OHS-1/2 and every JevBench public string.
>     - golden_dev and breadth_dev are golden_train's own in-family devs. They are strict for the yn2b rows and
>       report-only for the golden rows.
>   - **6-word template check:** 0 hits against the instructions of the 9 gate splits, the dialogue_rebuttal templates,
>     OHS-1/2 instructions and cards, and the eval injected spans.
>   - **Dev / eval wordings:** 0 rows use any of them (the DEV_* / EVAL_* frames, devp's own wordings and its injection
>     container, NONE_EVAL).
>   - **Ids and texts:** 0 matches with any dev or eval id or (state, instructions) pair.
>   - **What the rule removed:** golden units that share label names, cards or document text with the seen-source dev
>     rows. As a result, 17 sources are missing from the replay, for example pg_\*, some hard_\*, gd_feverous and
>     gd_quartz (731 rows of quota).
>   - OHS-3 was never opened.
>
> **The unseen-source set does not move.**
> - `gate/check_unseen_fix1.py` derives the set from the 12 registered files plus fix1_train. The result is
>   unchanged: 17 sources, 3,847 rows, 0 text-guard flags.
> - Every fix1 source is a golden_train source or a gd_gen3_\* source, and no gd_gen3_\* name matches a dev source.
> - So the frozen 12-file derivation that `--mode ship` uses is valid for C4. The check is re-run in the scoring job's
>   preflight.
>
> **Scoring job 3.**
> - Job 3 runs on the L4 with the §4 settings (`gate/gate_4b_fix1_l4.sh vm-job3`).
> - **REF is re-read** as `q35_4b_pxE_fresh3` (plus `_fresh3_perm`). The parity look runs against
>   `q35_4b_pxE_parity` with the §4 / A7 bar. If it fails, the job stops before C4 is read.
> - Then C4 is read (plus `_perm`).
> - **The job-1 fresh read `q35_4b_pxE_fresh` is not reused.** §4 requires REF and every candidate to be scored in
>   one job, as §5.1 does for C3.
>
> **One ship look:** `gate_dev.py q35_4b_main500k_fix1 q35_4b_pxE_fresh3 --mode ship --size 4b`.
> - The rule, every threshold, the 9 splits, the 12 training files, the unseen set and the bootstrap are unchanged
>   (§3).
> - C4 is the only candidate: no replacement rule, no C2 / C3 variants and no snapshot candidates.
> - **If SHIP and FINAL:** C4 is the final 4B.
> - **If DO NOT SHIP or NOT FINAL:** the fallback is 4B-E (§5.7). No further top-up may run without a new amendment.
>   C1's look is not repeated.
>
> **Limits and claims.**
> - This is the 2nd 4B ship look, so the chance of shipping a model that is not really better is a little higher than
>   with one look (§5, known limits).
> - The fix targets one failed constraint. It was chosen on dev data, so a pass on (e) is weaker evidence than a
>   pre-registered pass.
> - C4 vs C1 comparisons are report-only and never decisive. They use C1's job-1 reads (cross-job).
> - The model card discloses the lineage: main500k + top-up (program-labelled yn2b + golden replay).
>
> **Teacher:** C4 never becomes the 2B's teacher (decision D3; yn2b/SPEC.md §14), so §6 does not apply to it.
>
> **Held out:** §8 is unchanged. OHS-3 runs once, after the final choice.
>
> **Commit:** `________` (this amendment, together with the fix1 config, builder, launcher and gate files).
