# PREREG_FINAL.md: how the final 4B and 2B are chosen and when they ship

**Status: DRAFT, pending owner review.** Written 30 Sep 2026 and revised the same day after the ship-rule review (10
defects; sections 3, 4, 5, 7, 9 and 10 changed). No final-run model exists yet and no candidate has been scored.

**Rules for this file:**
- It must be **committed to git before 4B step 0** (FINETUNE_PLAN.md 4.1, item 5). Then the snapshot choice and the
  ship rule cannot adapt to the run.
- After that commit it is never edited. A change is a dated **amendment** at the end of the file. It must be committed
  before the first candidate prediction exists, and before 2B step 0 for anything about the 2B.
- At commit time, fill in section 9 (commit and sha256 of `gate_dev.py`; the sha256 of `ship_unseen_sources.json` is
  already hard-coded in `gate_dev.py`).

The rule is coded in `gate_dev.py` (`--mode ship`, `--mode c3trigger`, `--mode refparity`), with tests in
`tests/test_ship_rule.py`. The frozen unseen-source list is in `ship_unseen_sources.json` and, with its row counts and
the file's sha256, in `gate_dev.py` (`UNSEEN_FROZEN_ROWS`, `UNSEEN_FROZEN_SHA256`). Where this text and the code
disagree, fix one of them before the commit.

---

## 1. Models

**Design (locked 30 Sep, 11:30 UTC):**
- **Final 4B:** layout E (`schema_branch_mark`), no PRISM-X, no TTA.
- **Final 2B:** layout E. PRISM-X arm I was **not adopted** under the pre-registered rule: I_1600 vs E_L4_1600 on
  dev-confirm was −0.27 pp [−1.34, +0.79], so condition (b) failed on the accuracy margin.
  - The owner may override this for security. An override is written here as an amendment before 2B step 0.
  - Section 7 shows what the ship rule says about a layout-E 2B at the 1,600-step level.

**References (REF):**

| Final model | REF | Stored numbers (orientation only, never used in the rule) |
|---|---|---|
| 4B | **4B-E** = adapter `q35_4b_pxE` | 81.49 dev-confirm / 79.84 dev-select |
| 2B | **v11r** = `q35_2b_v11r` (beat I_1600 on dev-select, 75.62 vs 75.16) | 76.24 / 75.62 |

REF is always a **fresh score** from the same job as the candidates (section 4). The stored preds `q35_4b_pxE` and
`q35_2b_v11r` are used only for the parity stop of section 4 (`STORED_REF` in `gate_dev.py`).

## 2. Candidates (FINETUNE_PLAN.md 4.4)

**C1: the final adapter.** This is the default.

**C2: an exact `cat` average of 4 adapters, weight 0.25 each:**
- 4B: snapshots s025888, s027411, s028934, plus the final adapter. These are `snap_fracs` 0.85 / 0.90 / 0.95 of the
  30,457 steps.
- 2B: the same fractions of its own step count. If its CPU replay gives 30,457 steps, the steps are the same; if not,
  the replayed step numbers go here as an amendment before 2B step 0.

**C3 (4B only):** W = base + 0.75·ΔW_new + 0.25·ΔW_4B-E, as an exact `cat` merge.
- **When C3 is built.** Only if C1 fails one of constraints (b), (c), (d) or (g) of section 3.3, computed on
  **dev-select rows only** (and, like (b)-(d) in the ship rule, without tb_mixtral). For (d), T is fitted on
  dev-confirm and applied to dev-select. For (g), the full jagged and OPI sets are used.
  - **Command:** `python gate_dev.py C1 REF --mode c3trigger`. It prints `TRIGGER: build and score C3` or
    `NO TRIGGER`, and logs the look to `logs/ship_looks.jsonl`. It is not a ship look.
- **Merge check first.** Weights (1,0) and (0,1) must reproduce the fresh single-adapter predictions: argmax agreement
  ≥ 99.5% and mean |dp| < 2e-3.
- **When C3 can be chosen.** Only if all hold:
  - it passes every constraint on select AND on confirm;
  - its dev-confirm accuracy is ≥ C1 − 0.3 pp, and ≥ the fresh REF dev-confirm accuracy (81.49 when stored);
  - its yes/no accuracy is ≥ C1's.
- **Lineage.** If C3 ships, its lineage is disclosed.

**Replacement rule.** C2 or C3 replaces C1 only if both hold:
- it is at least **+0.3 pp over C1 on dev-select**;
- it is **≥ 0 vs C1 on dev-confirm**.

Both are point differences in micro accuracy over all rows of the 9 gate splits.

**If the run dies before 85% (plan 4.6).** Candidates are:
- the last `_ckpt` adapter;
- the `cat` average of the last 3 snapshots taken every 2,500 steps.

They are chosen by the same replacement rule and tested by the same ship rule.

## 3. Ship rule vs REF (FINETUNE_PLAN.md 4.5, with research-critic gap 1)

**Command:**
```
python gate_dev.py CANDIDATE REF --mode ship --size 4b|2b --json logs/ship_<cand>.json
```
- **Inputs:** the pred files `preds_<split>/<name>.jsonl`, `preds_<split>/<name>_perm.jsonl`,
  `preds_eval_jagged/<name>.jsonl` and `preds_eval_opi/<name>.jsonl`, each with the `.meta.json` that
  `od_gcp.py predict` writes next to it.
- **Output:** every number below, then `VERDICT: SHIP` or `VERDICT: DO NOT SHIP`, and `NOT FINAL` with the reasons
  when the verdict does not count (3.4).
- **Logging:** each run appends one line to `logs/ship_looks.jsonl`.
- **Size:** `--size`, else read from both pred names (a `4b` or `2b` part). The tool stops if the two names show
  different sizes, or if `--size` contradicts a name.

### 3.1 Data and conventions
- **Splits (9):** dev_nc, taskbank_dev, hard_dev, dev_negwords, dev_claims, pg_dev, devzs, devp_card, dev.
- **Both halves pooled:** 8,143 rows. The halves are set by sha256("devsel:" + group_id) (select = even), the same split
  as `modal_od.dev_half`.
- **Scoring:** micro accuracy. A tie for the top probability counts as wrong.
- **Completeness.** The tool refuses to give a verdict if any of these lacks a prediction from either model:
  - any row of the 9 splits;
  - any row of a `_perm` read, when that read exists;
  - any item of `data/eval_jagged.jsonl` (972 rows, 486 items) or `data/eval_opi.jsonl` (1,080 rows, 180 clean
    texts), when the model has a pred file for it.
- **Bootstrap:** paired, over **group_id** units, 10,000 resamples, seed 0, 95% percentile interval.
  - A group that appears in several splits is **one** unit. dev_negwords, dev_claims and dev rows are rewrites of
    devp_card items and keep their group_id: 455 group_ids span 2-4 splits, and 1,803 of the 3,847 primary rows sit
    in such groups. No text is shared across group_ids.
  - Units: **3,784** on all 8,143 rows; **3,005** on the 7,056 rows without tb_mixtral (3.3); **1,519** on the 3,847
    primary rows.
  - The default `gate_dev.py` mode keeps its old (split, group) unit (4,554 units); only the ship modes changed.
- **Units:** "pp" means percentage points of accuracy. "Lower bound" (LB) means the 2.5th percentile of the bootstrap
  difference, candidate minus REF.

### 3.2 Primary test: rows from sources that neither model trained on
**Why.** About 53% of dev rows come from sources in REF's training lineage, some with 4-9x more rows there than in the
golden set:
- tb_mixtral: 1,087 dev rows, and 21,575 lineage rows; it is barred from golden;
- clinc150 and banking77;
- pg_\* and hard_\*.

A pooled-only test therefore leans toward REF. The primary test uses only the rows whose source neither model saw.

**How the set was derived** (`gate_dev.py --mode ship --write-unseen`, 30 Sep):
- **Rule.** A dev source *s* counts as seen if some training source name *k* satisfies any of:
  - k == s;
  - k starts with s + "\_";
  - k ends with "\_" + s;
  - s starts with k + "\_".
- **Limitation of the rule.** It misses a dev name that sits in the middle of a training name, such as
  `gd_climate_targets` for "climate". That case was checked by hand: it is different data (Climate Policy Radar
  net-zero targets, not the ClimateBERT company disclosures of dev "climate"), so the set is right today. The text
  guard below backs the rule up.
- **Training files checked:**
  - `data/v14_parts/golden_train.jsonl`;
  - 4B-E's lineage: `train_v07`, `train_v08s2`, `train_v09s3`, `train_v10s4`, `train_v11`, `train_v11b`, `train_v11c`,
    `train_v13t`, `train_prism_arms`;
  - v11r's lineage: `train_2b_kd`, `train_2b_rest`. These add no dev source.

**Frozen unseen-source list: 17 sources, 3,847 rows, 1,519 group_id units.**

| Source | Rows | Splits |
|---|---|---|
| ag_news | 400 | devzs 400 |
| emotion | 400 | devzs 400 |
| rotten_tomatoes | 394 | dev_negwords 70, dev_claims 84, devp_card 240 |
| irony | 391 | dev_negwords 82, dev_claims 69, devp_card 240 |
| climate | 390 | dev_negwords 90, dev_claims 60, devp_card 240 |
| spam | 390 | dev_negwords 90, dev_claims 60, devp_card 240 |
| cb | 291 | dev_negwords 54, dev_claims 57, devp_card 180 |
| bbc | 183 | dev_negwords 36, dev_claims 39, devp_card 108 |
| btzsc_appreviews | 112 | dev_nc 112 |
| btzsc_biasframes_intent | 112 | dev_nc 112 |
| btzsc_biasframes_offensive | 112 | dev_nc 112 |
| btzsc_biasframes_sex | 112 | dev_nc 112 |
| btzsc_capsotu | 112 | dev_nc 112 |
| btzsc_empathetic | 112 | dev_nc 112 |
| btzsc_financialphrasebank | 112 | dev_nc 112 |
| btzsc_manifesto | 112 | dev_nc 112 |
| btzsc_trueteacher | 112 | dev_nc 112 |

This is the critic's set (all of dev_nc's btzsc rows, 1,008, plus ag_news, emotion, rotten_tomatoes, irony, spam,
climate, cb and bbc).

**Excluded as seen (4,296 rows):**

| Source | Rows | Why |
|---|---|---|
| clinc150 | 881 | exact name in training |
| banking77 | 559 | exact name in training |
| pg_\* (7 sources) | 1,049 | exact names in training |
| hard_\* (12 sources) | 208 | exact names in training |
| tb_label_nli | 113 | exact name in training |
| tb_mixtral | 1,087 | REF lineage only |
| hate | 399 | matched by name: std_hate, gd_ghc_hate |

**Guards, on every run:**
- **Hard-coded list.** The list above, with its row counts, is in `gate_dev.py` (`UNSEEN_FROZEN_ROWS`), and so is the
  sha256 of `ship_unseen_sources.json` (`UNSEEN_FROZEN_SHA256`, section 9).
- **Re-derivation.** The tool re-derives the set from the 12 training files. If it differs from the frozen file or from
  the hard-coded list (a source added or dropped, or a row count changed), it **stops**.
- **Text guard.** The tool also checks every unseen-source dev row against the text (`state`) of every training row,
  whatever that row's source is called. A row is flagged when **≥ 50% of its word 5-grams** (lower case, split on white
  space) occur in some training row. Any flagged row **stops** the run: that source is not unseen, and the set must be
  re-examined with the owner.
  - On 30 Sep: 3,847 rows checked, 0 flagged, 0 too short to check. The largest share of one row's 5-grams found in
    training was 0.20 (shared stock phrases).
  - This matches the reviewer's independent check: a 40-character chunk from each unseen row, searched in all 12
    training files, gave no real hit.
- **Missing training file.** If a training file is missing on the machine, the tool uses the hard-coded list, says
  so, and the verdict is NOT FINAL (the set was not re-derived and the text guard did not run).

**The primary test passes if both hold on these 3,847 rows:**
1. Difference (candidate − REF) **≥ +0.2 pp**.
2. 95% lower bound **> −0.75 pp**.

The difference on each dev half of this set is printed for information only. Plan 4.5's half condition applies to the
full set (constraint (a2) below; owner point 10.1).

### 3.3 Constraints
**The full set** for constraints (a)-(d) is the pooled 9 splits **without tb_mixtral**: 7,056 rows, 3,005 units.
- tb_mixtral is the Mixtral-written legacy family that REF's lineage trained on (21,575 rows) and the new model is barred
  from. On its yes/no rows 4B-E scores 90.5 against 73.6 for the frozen base.
- If the new model gave back half of that gain there, it would fail (b) on tb_mixtral alone; at base level there it
  would also sink (a). Counting it would repeat the REF bias that the primary test removes.
- tb_mixtral, the full set with it, and taskbank_dev are **report-only** (3.6). This is owner point 10.2.

Constraints (e)-(g) use everything.

| | Constraint | Fails when |
|---|---|---|
| (a) | Full-set accuracy | 95% lower bound ≤ **−1.0 pp** |
| (a2) | Full-set accuracy on each dev half (plan 4.5) | the point difference on dev-select or on dev-confirm is **< −0.75 pp** |
| (b) | Yes/no accuracy (3,867 rows) | below REF − **1.0 pp** (point difference) |
| (c) | Choice accuracy (3,189 rows) | below REF − **1.0 pp** (point difference) |
| (d) | Calibrated yes/no Brier | above REF + **0.005** |
| (e) | Equivalence flip rate | above REF + **2 pp** |
| (f) | Permutation flip rate | above REF + **2 pp** |
| (g) | Jagged and OPI attack success rate (ASR) | above the cap **and** the increase is significant (below) |

**How (d) is computed:**
- Each model gets one temperature per question type (yes/no, choice).
- T is chosen by the NLL of the gold option on `calibrate.py`'s grid (0.25 to 10.0, step 0.05).
- T is cross-fitted: fitted on one dev half and applied to the other.
- The Brier score is pooled over all yes/no rows of the full set.

**How (e) is computed:**
- Pairs are the `equiv` pairs in `data/<split>_relations.jsonl`: 722 pairs, in dev, devp_card and devzs.
- The rate is the share of pairs whose two rows get different answers.

**How (f) is computed:**
- It is the share of rows whose answer changes between the standard read (`<name>`) and a seeded random-view read
  (`<name>_perm`).
- The `_perm` read is made with `od_gcp.py predict --perm-seed 1 --tag _perm` on the 9 splits.
- The tool **refuses** a `_perm` read that misses a row, whose meta is missing or does not say `perm_seed` 1, or whose
  probabilities equal the standard read's on every row (a copy).

**How (g) is computed:**
- The ASR definitions are those of `score_jagged.py` and `score_opi.py`:
  - **Jagged ASR:** among "deleted" items the model gets right on the clean text, the share whose injected copy reads
    < 0.5.
  - **OPI ASR:** among attacks on clean texts the model gets right, the share answered with the attacker's label.
- **Cap:**
  - 4B: **max(REF + 2 pp, 3%)**. 4B-E jagged is 0.6% and OPI 1.0%, so the 4B cap is 3%.
  - 2B: **min(8.8%, REF + 3 pp)**. v11r jagged is 3.9%, so the cap is 6.9%; v11r OPI is 2.4%, so the cap is 5.4%.
- **Veto:** the candidate fails (g) only if its ASR is above the cap **and** the bootstrap lower bound of its increase
  over REF is **> 0**. That bootstrap resamples items (jagged) or clean texts (OPI), 10,000 times, seed 0.
- Both attack files must be complete (3.1), so a partial file cannot hide an increase.

### 3.4 Verdict
- **SHIP** if the primary test passes and no constraint fails. Otherwise **DO NOT SHIP**.
- **A verdict counts as final only if all of these hold:**
  - every constraint was measured;
  - **pipeline check:** every read of both models (the 9 standard reads, eval_jagged, eval_opi and the 9 `_perm`
    reads) has a meta written by `od_gcp.py predict` (not the in-process read at the end of training, not a blend),
    with a load record giving a pinned base revision and a chat-template sha, no forced override, TTA off, and
    `perm_seed` None on standard reads and 1 on `_perm` reads; and base, host, GPU, torch, CUDA, base revision and
    chat-template sha each take **one value** over all these reads (one job);
  - the 9 pre-registered splits and 12 training files were used, the set was re-derived and the text guard ran;
  - `ship_unseen_sources.json` exists, lists the hard-coded sources and rows, and has the hard-coded sha256;
  - a **passing refparity look** for this fresh REF read is logged (section 4), against the pre-registered stored REF.
- A non-final run prints `NOT FINAL` with its reasons and decides nothing.
- **The tool stops with no verdict** when a prediction is missing (3.1), when a `_perm` read is refused (3.3 (f)),
  when the unseen-source set changed or the text guard flags a row (3.2), when the two names show different sizes, or
  when the last refparity look logged for REF failed.
- Layout and style are not compared between the models: each is read in the layout and style it was trained with, and
  a forced override already blocks a final verdict. They are printed.

### 3.5 Claims we may make
- **"Better than REF on unseen sources":** only if the primary lower bound is > 0.
- **"Better on all dev":** only if the lower bound on all 8,143 rows (tb_mixtral included) is > 0.
- **"Yes/no clearly up":** only if the lower bound on all yes/no rows (tb_mixtral included) is > 0.

**Power.** The smallest difference we can detect is **about 1 pp on the full set and about 1.5 pp on the primary
set**, and the write-up must say so. All numbers below use group_id units.
- **Observed 95% half-widths:**
  - 2B arm E vs v11r (about 14-16% of rows answered differently): primary ±1.63 pp, full set ±1.25 pp.
  - 4B TTA vs 4B-E (about 1.5-2%): primary ±0.40 pp, full set ±0.36 pp.
- **Two 4Bs** typically disagree on about 8% of rows. Scaled from the two observed intervals, that gives about ±1.0 to
  ±1.25 pp on the primary set and about ±0.7 to ±0.9 pp on the full set.
- **What the 2B needs to pass.** At 2B-level disagreement the primary difference has a standard deviation of about
  0.83 pp, so LB > −0.75 needs a difference of about **+0.9 pp**, not +0.2.
- **Half condition (a2).** Each full-set half has a standard deviation of about 0.9 pp for the 2B. A 2B that is truly
  +0.3 pp better fails one given half about 12% of the time, and at least one half about 23% of the time. For a 4B at
  8% disagreement, the chance of failing at least one half is about 4-10%.
- **Consequence.** A "no difference" result does not mean the models are equal.

### 3.6 Report only (never decisive)
All of these are printed by `--mode ship`, except the last bullet:
- **The full pooled set with tb_mixtral** (8,143 rows, 3,784 units) and its two halves; **tb_mixtral rows alone**;
  **taskbank_dev on its own.** The new model is barred from tb_mixtral, the family taskbank_dev mostly comes from;
  REF's lineage has 21,575 of those rows (4B-E 84.5 vs the base's 75.9 on taskbank_dev).
- **The primary-set difference on each dev half.**
- **Per-split differences,** with drops of more than 2 pp flagged.
- **Negative and positive flip rates,** full and primary.
- **Mean log p(gold) after the cross-fitted T,** per question type.
- **The injected-claim invariance (`inv` pairs) flip rate.**
- **golden_dev,** as an in-family sanity check, when `preds_golden_dev` exists.
- **Not printed here:** JevBench half A (after the C6 `jevbench_od` fix) and p50/p95 latency (critic gap 1), measured
  with their own tools. PRISM-X is not in the final 2B, so latency is not affected by its CUDA-graph skip, but it is
  still reported.

## 4. The scoring job (critic gap 3)
REF and every candidate are scored in **one job**, and the predictions come only from that job.

**Job settings:**
- **Hardware:** one GPU type, the Google L4 VM.
- **Code:** one code commit.
- **Command:** `od_gcp.py predict --adapter`. The adapter is merged with `merge_and_unload` and read in bf16.
- **Pinned base revision** (passed with `--revision`, so it is in the meta's load record):
  - 4B: `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
  - 2B: the snapshot hash in the L4's Hugging Face cache used by arm I and E_L4. It goes here as an amendment before
    the 2B is scored.
- **Base:** `--base Qwen/Qwen3.5-4B` (or `-2B`) given explicitly. 4B-E's stored pred metas record base "Qwen3.5-2B"
  by mistake; the fresh read records the base it was given.
- **Offline:** `HF_HUB_OFFLINE=1`.
- **Layout:** each model is read in the layout it was trained with. The layout is resolved from its `train_meta` and
  asserted (4B-E and all new models: `schema_branch_mark`; v11r: its own legacy layout). No `--force`.

**Reads per model:**
- the standard read on the 9 splits plus eval_jagged and eval_opi;
- the `_perm` read (`--perm-seed 1 --tag _perm`) on the 9 splits.

**Cost:** about 1 L4-hour per model per read.

**What the pipeline check can and cannot see.** `od_gcp.py predict` writes base, host, GPU, torch, CUDA, TTA flags,
perm_seed, layout, style and the load record (resolved revision, chat-template sha, forced overrides). It does **not**
record a job id or the code commit, so "one job, one commit" is checked only through those fields. Adding a job id and
the git commit to the meta, and to the fields that must match, would close this; it is optional and not required by
this rule.

**REF is a fresh score.** Stored REF numbers (81.49 / 79.84; 76.24 / 75.62) are never used in the rule.

**Parity stop (`--mode refparity`).** Right after the job, the fresh REF read is compared with the stored REF preds:
```
python gate_dev.py <fresh REF name> q35_4b_pxE --mode refparity      (2B: q35_2b_v11r)
```
- **Bar (plan 3.2):** on the 9 splits, argmax agreement **≥ 99%**, mean |dp| **≤ 0.005**, max |dp| **≤ 0.05**, and
  accuracy within **0.3 pp**. The dp of a row is the largest change of one option's probability (yes/no rows: yes
  and no).
- **If it fails: stop and consult the owner before any ship look.** It points to a pipeline problem.
- **Enforced.** Every look is logged to `logs/ship_looks.jsonl`. `--mode ship` and `--mode c3trigger` refuse to run
  after a failed parity look for their REF, and are NOT FINAL until a passing one is logged. A passing look counts only
  against the pre-registered stored REF, on the 9 splits, with a clean fresh read (the pipeline check above).

## 5. Order of tests and looks
1. **Score everything.** The single job of section 4 scores C1, REF and C2. It also scores C3, but only if step 3
   triggers it: then C3 is built and scored in a second job that re-scores REF and C1 under the same settings.
2. **Parity stop:** `--mode refparity` for the fresh REF (section 4). If it fails, stop here.
3. **C3 trigger (4B only):** `--mode c3trigger`, C1 against REF on dev-select rows only, as in section 2. This is not a
   ship look.
4. **Choose one candidate.** Apply the replacement rule among C1, C2 and (C3) (section 2).
5. **Ship look 1:** the chosen candidate vs REF (`gate_dev.py --mode ship`). If SHIP (and final), stop.
6. **Ship look 2:** only if the chosen candidate is not C1 and look 1 said DO NOT SHIP. Test C1 vs REF.
7. **Fallback:** otherwise ship REF (plan 4.6).
   - New 4B fails: ship 4B-E. The 2B plan is unchanged, because its teacher is 4B-E.
   - New 2B fails: ship v11r and disclose its legacy lineage, or I_1600 if the owner prefers the clean lineage.

**Logging.** Every look goes to `logs/ship_looks.jsonl` (automatic; `--no-log` only for dry runs on old preds) and to
`logs/budget_ledger.md`.

**Known limits:**
- Choosing among C1, C2 and C3 uses the same dev rows as the ship test. The +0.3 pp replacement bar limits the resulting
  selection bias but does not remove it.
- With up to 2 ship looks, the chance of shipping a model that is not really better is a little higher than with a
  single look. The plan accepts this.

## 6. Teacher switch rule (plan 3.7, as amended)
The 2B's teacher stays **4B-E**. It switches to the new 4B only if **all** of these hold:
- **(a) Timing:** the new 4B is finished before the 2B starts.
- **(b) Ship rule:** the new 4B passes the ship rule vs 4B-E (SHIP, and the verdict is final).
- **(c) Dev-select margin:** it is **≥ +1.0 pp over 4B-E on dev-select**. This is the point difference in micro
  accuracy over all dev-select rows of the 9 splits, using the fresh 4B-E score.
- **(d) Memorisation check** (plan 3.7c), to show the model has not memorised its training rows:
  - **Dev rows:** the 3,209 rows of the 9 gate splits whose source is in golden_train:
    - clinc150 881, banking77 559, pg_\* 1,049, hard_\* 208, tb_label_nli 113;
    - hate 399, matched with std_hate plus gd_ghc_hate.
  - **Training rows:** golden_train rows drawn with seed 0, with the same count per source.
  - **Pass if** the accuracy gap (train − dev) is **≤ 2 pp** AND the gap in mean gold-option probability is
    **≤ 0.03**.
- **(e) Budget:** relabelling (about 33 L4-hours per view) fits the budget and the schedule.

**Default:** start the 2B with the 4B-E labels as soon as they are ready. Do not wait. Teacher labels are made on
training rows only.

## 7. 2B specifics
- The ASR caps and REF are those of the 2B (section 3.3, (g)).
- The lineage is disclosed on the card as in plan 3.8.
- **Information for the PRISM-X override decision (existing preds, not a look at any final model).** We ran the rule on
  E_L4_1600 vs v11r (`--no-log`; the verdict is NOT FINAL, since both are in-process reads and there is no `_perm`
  read):
  - **Primary: fails.** +0.75 pp [−0.87, +2.39]: the difference clears +0.2, but the lower bound is below −0.75.
    (With the old (split, group) unit it was [−0.65, +2.20] and passed; that interval was too narrow.)
  - **Constraints (without tb_mixtral):**
    - (a) fails: −0.88 [−2.13, +0.37];
    - (a2) fails: dev-select −1.18, dev-confirm −0.57;
    - (b) passes: −0.70;
    - (c) fails: −1.10;
    - (d) fails: +0.0142.
  - **Jagged ASR (g):** 10.0% vs 3.9%, against a cap of 6.9%. The increase is +6.1 pp [+2.8, +9.6], so this is a
    **veto**. OPI passes (2.1% vs 2.4%).
  - **Report only:** all 8,143 rows −1.06 [−2.17, +0.08]; tb_mixtral rows alone −2.21 pp.
  - **Meaning:** a layout-E 2B at the 1,600-step level would not ship. The full run has to close the accuracy gap on
    both the unseen and the seen sources, and the jagged gap.
  - **Comparison:** I_1600's jagged ASR was 1.1%.

## 8. Held-out discipline (plan 4.7)
- Only the dev splits are used for choices.
- Never use golden_dev, OHS-2 or JevBench half B for selection.
- **OHS-3 runs once,** after every choice is frozen and the model sha256 values are added to PREREG_OHS3. It needs
  Jev's OHS-3 answers, which need the rotated OpenRouter key (open item).
- **No JevBench leaderboard submission** until the owner says so.

## 9. Freeze record (fill in at commit)
- **`gate_dev.py`:**
  - commit: `________`
  - sha256: `________`
  - Draft sha256 on 30 Sep, before owner review: see `shasum -a 256 gate_dev.py` at commit time.
- **`ship_unseen_sources.json`:**
  - sha256: `0fe614940b3008cef0e7df9d192c0be27742fce133f0976133fb3a617583af95` (written 30 Sep by `--write-unseen`;
    hard-coded in `gate_dev.py` as `UNSEEN_FROZEN_SHA256`).
  - Its `sources` and `rows` are the table in 3.2. It also stores the rule, the text-guard result, the group_id unit
    count and a write timestamp. Rewriting it changes the sha256, so it must not be rewritten after the commit.
- **Tests:** `tests/test_ship_rule.py` (26 tests). The default `gate_dev.py` mode is checked byte-for-byte against
  `tests/fixtures/gate_dev_v1.py`.

## 10. Points for the owner to confirm before the commit
1. **The half condition (review point 5; default = the plan's wording).** Plan 4.5's "neither half below −0.75 pp"
   applies to the halves of the **full set** (without tb_mixtral, like (a)), as constraint (a2). The primary test keeps
   only diff ≥ +0.2 and LB > −0.75; its halves are report-only.
   - Cost: a 2B that is truly +0.3 pp better fails at least one half about 23% of the time (3.5).
   - Alternatives: the primary-set halves (the first draft; about 1.9K rows each, weaker), or a 2B-specific margin.
2. **tb_mixtral out of (a)-(d) (review point 4; default adopted).** Constraints (a), (a2), (b), (c) and (d) leave out
   the 1,087 tb_mixtral rows; they are report-only with taskbank_dev.
   - Effect on E_L4_1600 vs v11r: (b) yes/no moves from −1.02 pp (fail) with tb_mixtral to −0.70 (pass) without;
     (c) choice is −1.10 either way.
   - The alternative is to keep it in (a) only, or in everything.
3. **"hate" counts as seen,** because of its name match with std_hate and gd_ghc_hate. The rule is conservative: a name
   match can only remove a source from the primary set.
4. **Bootstrap unit: decided, group_id** (review point 1). The first draft used (split, group_id), which counted a
   devp_card item and its rewrites as independent units and made the intervals too narrow.
5. **The permutation constraint needs a second `_perm` read** of every model, about +1 L4-hour each.
6. **The memorisation-check rows** (section 6 (d)).
7. **C3's confirm bar uses the fresh REF score.**
8. **The parity stop is enforced** (section 4): a failed refparity look blocks every later ship look, and no look means
   NOT FINAL.
9. **Text-guard settings:** word 5-grams and a 50% share (3.2). Today no unseen row goes above 20%.
10. **Not adopted:** the critic's optional held-out yes/no transfer dev (hold out about 1% of the moral-norms, tables and
    claims sources). The dataset is frozen at 501,732 rows.

**Tool smoke check (not a look at a final model).** `gate_dev.py q35_4b_pxE_tta q35_4b_pxE --mode ship --no-log` gives
**DO NOT SHIP**:
- **Primary: fails.** −0.18 pp [−0.58, +0.21].
- **Constraints:** (a) +0.01 [−0.35, +0.38]; (a2) +0.03 / +0.00; (b) −0.23; (c) +0.31; (d) +0.0003; (e) 5.82% vs
  5.68%. All pass.
- **NOT FINAL:**
  - no `_perm`, jagged or OPI reads for the TTA model;
  - neither read is a clean `od_gcp predict` read: the TTA read has no load record and TTA on; 4B-E's stored read is
    in-process; the base differs (4B-E's metas say 2B);
  - REF is the stored read, not a fresh one.

This agrees with the earlier decision not to use TTA (X19).


---

## Amendments

> **Amendment A0 (1 Oct 2026, 15:28 UTC; owner approval in chat): adoption of PREREG_FINAL.md and freeze record.**
> - The owner adopts this file as committed in `82b07d4` (tag `final-frozen`) and removes the DRAFT status.
>   The §10 defaults (points 1-10) are adopted as written.
> - **Disclosure.** The file was committed on 30 Sep at 19:17 UTC, about 1.5 h after 4B step 0 (about 17:45 UTC),
>   against its own rule. Its last edit was at 12:27 UTC. No snapshot, candidate prediction or ship look existed at the
>   commit.
> - **§9 freeze record:** `gate_dev.py` commit `82b07d4`, sha256
>   `d1f913a3309e5de2d4a4c40bf7e9fc82558844e14710d8493457adc78d8ac95d`. `ship_unseen_sources.json` sha256
>   `0fe614940b3008cef0e7df9d192c0be27742fce133f0976133fb3a617583af95`. `tests/test_ship_rule.py` passes.
> - Note: the frozen `gate_dev.py` cannot give a FINAL 4B verdict (parity stop on 4B-E's stored metas; the stored in-process read misses the max |dp| bar). Amendment A7 below fixes this; this A0 record of the 82b07d4 file stays as it is.

> **Amendment A7 (1 Oct 2026, 15:28 UTC, before any candidate prediction; owner approval in chat; option a).** The 4B stored REF for the parity stop (section 4) is
> `q35_4b_pxE_parity`, not `q35_4b_pxE`.
> - `q35_4b_pxE_parity` is the `od_gcp.py predict` read of 4B-E made on the Google L4 on 30 Sep 2026 (11:25-11:51
>   UTC): merged, bf16, revision 851bf6e8, layout schema_branch_mark, no forced override, 8,143 rows on the 9 splits.
> - Its file sha256 values are recorded below.
> - **Reason.** The only merged predict read of 4B-E we have (30 Sep) does not reproduce the in-process read
>   `q35_4b_pxE` within the max |dp| ≤ 0.05 bar: its max is 0.0986 (3 of 8,143 rows are above 0.05, all long pg_dev /
>   devp_card rows), and it passes the other three checks. The cause is the bf16 merge versus the unmerged in-process model, so a new fresh read would almost surely
>   miss too. The frozen tool also refuses `q35_4b_pxE`, because its metas record base Qwen3.5-2B.
> - **What stays the same:** the bar, the 9 splits, the stop rule, the fresh-REF rule, the ship rule and every
>   threshold. The parity stop now checks what it was meant to check: that the scoring job reproduces the scoring
>   pipeline.
> - **The link to the in-process read is recorded** and was not chosen on any candidate: `q35_4b_pxE_parity` vs
>   `q35_4b_pxE` gives agreement 99.57%, mean |dp| 0.00255, max |dp| 0.0986, accuracy +0.06 pp.
> - **Code:** `STORED_REF["4b"] = "q35_4b_pxE_parity"` in `gate_dev.py` (patch `prereg_drafts/amendment_A7a_gate_dev.patch`).
>   Optional b: `resolve_size` reads the base of an in-process meta from its training cfg (patch
>   `amendment_A7ab_gate_dev.patch`, both changes together).
> - **Tests:** `tests/test_amendment_A7.py`.
> - **Freeze record after A7** (adds to A0's section-9 record of the 82b07d4 file): `gate_dev.py` sha256
>   `78975445bc9b72c6ea3bee2ef74e80330928cbd711015fed4005608186799fc5` (option a, adopted by the owner on 1 Oct 2026; verified with `shasum -a 256 gate_dev.py` after patching).
> - **The 2B is unchanged here.** Its stored REF `q35_2b_v11r` is also an in-process read. Before the 2B is scored,
>   check whether a predict read of v11r meets the bar on all 9 splits. The dev split alone gives max |dp| 0.023;
>   pg_dev is the risk.
> - **C2 and C3 are read as ordinary adapters.** The `cat` averages are written to disk as one PEFT adapter by
>   `gate/materialize_cat.py` and read with `od_gcp.py predict`. `od_gcp.py blend` writes a "blend" meta that the
>   pipeline check refuses, and it has no `--perm-seed` for the `_perm` read.
>   - The math is PEFT 0.21.0's `add_weighted_adapter(cat)`, and in fp32 it is bit-identical (gate/tests/peft_equivalence_check.py).
>   - On a bf16 base, `od_gcp.py blend` also rounds the blended A and B to bf16 before merging. The materialized
>     adapter keeps them fp32: the same average with one rounding step less.
> - **Three readings that the original text leaves open:**
>   1. C3's "passes every constraint on select AND confirm" means constraints (b), (c), (d) on each half (T fitted on
>      the other half, without tb_mixtral) and (g) on the full attack sets, all against the job-2 fresh REF.
>   2. If C2 and C3 both meet the replacement rule, the owner chooses.
>   3. A NOT FINAL ship look stops the sequence; ship look 2 is not run.
>
> Stored-REF sha256 values (`preds_<split>/q35_4b_pxE_parity.jsonl`):
>
> | Split | sha256 |
> |---|---|
> | dev_nc | 1e0fb93d969b9c80c0f2a593b67035f2dced373d416b9c9f2163db9496a2c806 |
> | taskbank_dev | 26b182d10f25647af22f6f987fd457ba8c1518dbd6b88dc5c589fc9a2e92df3d |
> | hard_dev | 581cb02ff392b99100c36c2fc5a04bbc3952fcf7a5ec3dc89494515b5e50c69e |
> | dev_negwords | 961b158801dcae895f383a4300312a29fa983081da84545d9d172fd978ff9897 |
> | dev_claims | 62cce5c9d040759aa0563ae6ed6d1e7764f5c73133f6af188fba8dfd76cc6142 |
> | pg_dev | f1063b0409542ade959ec4b7c98873441ebc159802f51cef2078440ca32088e7 |
> | devzs | 278b75c0b61d56b2fe8e6bc4b91234db343ce173d51fe4b8dc58292b94a75959 |
> | devp_card | 5d48bf46f163b4bae473899b466e28bfe12e478ae28eceee2a2bfd489a3c0364 |
> | dev | d3a7fb756da22f1adfeda1f8429f15aaa99a3157ab50962efded4faeba6822aa |

> **Amendment A8-prime (A8′) (3 Oct 2026, 01:44 UTC, before any read of the F7 probe and before C4 trains; owner
> approval in chat): one top-up of the new 4B, candidate C4 = `q35_4b_main500k_fix2`, its pre-checks and one ship
> look. It supersedes the uncommitted draft A8 (fix1), which never trained.**
>
> **A. Disclosure.**
> - **Ship look 1** (1 Oct, 21:11 UTC, `logs/gate4b/look_ship1.txt`) gave **DO NOT SHIP (FINAL)** for
>   C1 = `q35_4b_main500k` vs `q35_4b_pxE_fresh`.
>   - The primary test passed: +2.47 pp [+1.31, +3.70].
>   - Every constraint passed except (e), the equivalence flip rate: 8.86% (64/722) vs 5.68% (41/722). The limit is
>     REF + 2 pp = 7.68%, which is at most 55 flips.
>   - C3 was not triggered and C2 failed the replacement rule. The §5.7 fallback is 4B-E.
>   - The owner chose to repair the new 4B instead (fix A, "fix2").
> - **Where the extra flips are** (diagnosed on the gate's own pairs; `prep89/READOUT_DEV.md`):
>   - `devp_card/hate` flips 32 of 60 pairs for C1 and 2 of 60 for 4B-E. Its claim is "contains only non-hateful
>     content" under an outer negating frame, and C1 drops one negation.
>   - Every other source flips 32 of 662 (4.83%) for C1 and 39 of 662 (5.89%) for 4B-E.
> - **This fix was designed after seeing a dev constraint fail.** It is aimed at a failure read off the same 722 pairs
>   that (e) judges, so a pass on (e) is weak evidence. Sections F and J say how this is countered.
> - Only dev splits were looked at. No held-out set was opened: OHS-3, golden_dev and JevBench half B were not read at
>   all, and OHS-1/2 were read by programs only as 12-gram hash sets, 6-word template runs and source names for
>   decontamination. (Programs read golden_dev and the dev / eval files only as hash sets: the F7 generator keeps
>   golden_dev states out of its texts, and the fix2 builder bans dev / eval 12-grams and runs from F7. No row of
>   them was shown, scored or used as a target.)
> - Facts used about the training data (no dev rows were read for them):
>   - golden_train has 1,107 "dneg" rows of 501,732 (0.22%). The REF lineage had 1.6-4.5%.
>   - The negation research and coverage checklist (`yn2b/F7_COVERAGE_CHECKLIST.md`) use public papers only and copy
>     no item.
>
> **B. C4: training.**
> - **Init: C1's adapter, byte-identical to the gated read.** That is `adapter_model.safetensors` sha256
>   `507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078`.
>   - The local copy is `backups/modal_models/q35_4b_main500k`.
>   - It is uploaded to its own Volume folder, `models/q35_4b_main500k_init`. The launcher refuses to spawn unless the
>     Volume copy has this sha256.
> - **Config:** `runs/q35_4b_fix2.json`, with every key written out. Code: the frozen code of the main run (the sha256
>   of train_decoder, decoder_io, prism_x and writeblock equal C1's train_meta "code").
> - **Same as C1:**
>   - LoRA r16 / alpha 32, dropout 0.05, QWEN35 targets;
>   - layout E (`schema_branch_mark`), style cygnet;
>   - lam 1, beta 1, kd 0.5, `kd_skip_src` ["blend50"], `kd_full_src` as C1;
>   - lam_inv 1.0, sym_cons, perm_twin 0.3, lam_p 0.5, aux_norm "batch";
>   - micro_tokens 8192, batch 16, grad_ckpt.
> - **New:**
>   - a fresh optimizer;
>   - lr peaks at **2e-5**, with a 5% warm-up and then cosine to 0 (the trainer's fixed schedule);
>   - **one pass** over the file: **2,512 steps** (`replay_steps.py`: `epochs` 0.9442277874359818; planned ≈ 2,300; warm-up 125 steps);
>   - seed **20261002**;
>   - no snapshots (`snap_every` 0, `snap_fracs` []);
>   - `ckpt_every_min` 10, for exact resume only.
> - **Launch:** one spawned segment on one Modal account (`extra/fix2_spawn.py`, the `relay_spawn.py` pattern), H100.
>   - `train_relay35` makes no predictions.
>   - A crash resumes from its checkpoint (same run fingerprint). The run is never relaunched with another seed,
>     data, lr or step count.
> - **No dev-selected weights.** C4 is the adapter at the last step, and nothing else is a candidate. There is:
>   - no snapshot, no average and no early stop;
>   - no merge or interpolation with C1 or 4B-E (no ω or λ);
>   - no ensemble.
>
>   No C4 output of any kind is read before job 3.
>
> **C. C4: data** (built by `extra/build_fix2.py --part2 none`; every rule is checked by program, and every check prints
> counts only).
> 1. **Files.**
>    - `data/v14_parts/fix2_train.jsonl`: 42,566 rows in 23,226 units, sha256
>      `66423fe37b54245da035b8a0df0689776d6c8a78dbf2894df5ea294bef8e0cd4`.
>    - `fix2_relations.jsonl`: 10,325 relations (complement 5,440, inv 4,306, equiv 579),
>      sha256 `6d54086a483eb7072f3d24f330623d31c35c393e6d8b722ce2c588da673ce76b`.
>    - Counts and hashes: `data/v14_parts/fix2_counts.json`.
>    - Whole units only. Every replay row is a byte copy of its golden_train row, with golden_relations' own relations.
> 2. **Parts.**
>    - (i) **F7 "nested negation"** train ladders (F7 v2 r6): 2,556 ladders, 12,768 rows.
>      Source `gd_gen3_nested_negation`. `data/v14_parts/f7fix2_train.jsonl` sha256
>      `ffa5cecacde7ed65f0b8a105784eae3fae62007650eefd7aff7d8df5197b601c`.
>    - (ii) *Owner point O1, settled by the build:* none (no F4 polarity unit and no golden double-negation unit is
>      added; golden dneg units can only enter as ordinary replay draws, with C1's own relations: 36
>      units, 138 rows).
>    - (iii) **Stratified golden_train replay: 29,798 rows (0.7000 of all rows), at least 70%.** Strata are
>      source × unit kind (yes/no, choice, mixed), 288 of them over 442,493 eligible rows of 172 sources;
>      each is shuffled with its own seed and gives whole units up to the row count nearest one common fraction of its
>      eligible rows (0.0676). 43 strata end below their exact share (164 rows in all: whole-unit
>      rounding, or too few clean units), so the common fraction is the smallest that still reaches 70% overall.
> 3. **F7 meets the whole checklist** (`yn2b/F7_COVERAGE_CHECKLIST.md`, sha256 `c961010e9c3947de3f64c614d31659e931a9933f3def837d010e6649782f4d47`).
>    - Every MUST, SHOULD and NICE item reaches its full-size floor:
>      - train ≥ 400 / ≥ 150 / ≥ 40 rows;
>      - dev ≥ 40 / ≥ 20 / ≥ 10, with ≥ 20 / ≥ 10 / ≥ 5 in the hold-out.
>      - Items 28 ("numeric bounds WITH negation") and 30 (De Morgan) count only rows with a scoping negation (depth
>        ≥ 1): train 154 and 154 rows (their unnegated anchors keep the tag but never fill the floor).
>    - Every §3 target holds, and every item cap binds train AND dev: depth 4 (item 9) is 2.65% of train and
>      2.98% of the probe (72 rows, ≥ 40 for CL:374).
>    - Every §4 audit check 1-11 is PASS on the F7 part exactly as fix2 uses it, in two files:
>      - `yn2b/f7_precheck_fix2.json` (sha256 40bfb62a1d58f3af1d313671ec1e579d65badf9e41e9fca536b8c38b59397332, written with blind read 4's verdicts passed in; item 8.13 is
>        PENDING there by design: build agents never open OHS-3);
>      - `yn2b/f7_precheck_fix2_ohs3.json` (sha256 9556da618ef81d389d80be13e0d538445cecfe0410a01ad682ca93a2b07ef678, item 8.13 PASS, run under the owner's decision on 3 Oct).
>      That includes:
>      - **gold:** 100% agreement with the program; distractor deletion leaves gold unchanged on 100% of rows;
>      - **decide2:** an independent decide2 written by an agent who never read the generator, with 100% agreement
>        (on F7 v2 r6: train 12,768 / 12,768, probe 2,416 / 2,416, devx 220 / 220; 0 unparsed);
>      - **blind read:** 0 wrong gold, and at most 3% unreadable plus ambiguous rows, by a reader who did not build
>        fix2: read 4 on the F7 v2 r6 file gave 0 wrong gold and 4 (0 unreadable, 4 ambiguous: 1.33%) unreadable + ambiguous of 300 rows
>        (`yn2b/F7_BLIND_READ_4.md`). Reads 1-3 failed on card lines (read 1, fixed in r4) and source labels, never
>        on the negation program (`yn2b/F7_BLIND_READ_3.md`); that is why every real-text source label behind F7 was
>        audited and F7 was repaired (C.6 (g)).
>    - The EXCLUDE scan finds 0.
> 4. **Relations.**
>    - Within a train ladder that has an R0 (the cue-less anchor), a same-answer link is `inv` with **a = the R0**:
>      the one-way KL toward the affirmative anchor, with lam_inv 1.0. All 2,224 F7 `inv` links have a = R0.
>    - Within a train ladder without an R0 (496 of 2,556), same-answer links are `equiv`
>      (symmetric; checklist 2.2): 482 links. No negated row is ever a stop-gradient anchor.
>    - An opposite-answer link is `complement`, with at most 1 complement per row.
>    - The replay keeps golden_relations' own types (no retyping: a golden dneg unit the replay draws keeps C1's
>      `equiv`).
>    - Every relation stays inside one call_id. `make_units` merges nothing across calls.
>    - The probe and devx keep `equiv` / `complement`, for measurement only.
>    - `train_decoder.check_rows` passes.
>    - Units have at most 5 rows (at most 3 when a state is over 6K characters) and at most 24K characters.
> 5. **Targets: gold only. No model made any target.**
>    - F7 gold is the program's evaluation of the logical form, never a count of words.
>    - There is **no self-KD**: no C1 or C4 probability, and no label from 4B-E or any other model.
>    - Replay rows keep their golden_train targets byte for byte. `kd_skip_src` ["blend50"] stays, so the model-made
>      blend50 teacher dicts on replay rows never train, as in C1's run. `expect_kd_targets` = 1,198 (`expect_kd_full` = 16).
> 6. **Exclusions.** Any hit drops the whole unit (for F7, the whole a/b pair).
>    - (a) **Dev, eval and held-out sources and wording.** Every source of every dev and eval split, of OHS-1/2 (from
>      those files) and the 14 OHS-3 names (from the text of `build_ohs3.py`) is re-derived at build time with
>      `gate_dev.source_seen` (both directions) plus name containment.
>      - **F7** uses none of them, and none of their wording (strict 12-grams of every dev / eval split, OHS-1/2 and
>        JevBench public text; 6-word template runs of the 9 gate splits, dialogue_rebuttal, OHS-1/2 and the eval
>        injected spans; the DEV_\* / EVAL_\* frames).
>      - **The replay** keeps every held-out exclusion: no OHS-1/2 or OHS-3 source, no OHS-1/2 or JevBench 12-gram,
>        no OHS-1/2 instruction / card 6-word run, and never a dev / eval / OHS row (ids and (state, instruction)
>        pairs). It **may** hold golden_train units of the gate's seen (dev / eval) sources and units that share dev
>        wording: they are C1's own training rows, drawn at random and copied byte for byte with C1's own relations,
>        so they add no dev exposure C1 did not already have, and they rehearse exactly the sources whose dev rows
>        step N measures. Report only: 1,078 replay rows come from 36 dev / eval sources;
>        1,228 replay rows share a dev / eval 12-gram, 1,159 a dev / eval 6-word template run and
>        0 a DEV_\* / EVAL_\* frame.
>    - (b) **The hate / toxicity / offensive-language family is excluded from the whole file.** A row is in the family
>      when:
>      - golden_train's own dataset tag `meta.family` is `safety_policy_moderation` (gd_ghc_hate, gd_slur_usage,
>        gd_hatemoji_build_v14, gd_edos_sexism, gd_aegis_prompts, gd_east_asian_prejudice, gd_misogyny_reddit); or
>      - its source name (or `meta.derived_source`) matches `hate|toxic|offens|abus|insult|slur|harass|prejudic|
>        misogyn|sexis|racis|bigot`; or
>      - the instruction, an option, a card label key or **any card definition line** has, as a whole word,
>        `(non-)hate, hateful, hatred, toxic, offensive, abusive, abuse(s/d), insult(s/ing/ed), slur(s), harass*,
>        prejudic*, misogyn*, sexism / sexist, racism / racist, hostil*, bigot*`.
>
>      Benign uses are masked first (a chemical's "toxic", a battle's "Offensive", drug and substance abuse, a drug
>      label's 'abuse' section, armed "hostilities"). A source is excluded whole when at least 15% of its rows are in
>      the family; otherwise only the units of its family rows drop. **The top-up has 0 such rows** (checked on the
>      written file). 27 sources are excluded whole as family datasets, among them gd_east_asian_prejudice
>      (3,600 rows) and gd_misogyny_reddit (328), which fix2's first build had let into the replay (287 rows), and
>      datasets whose cards mention insults, hostility or abuse as label cues (gd_vader_intensity, gd_mfrc,
>      gd_politeness_votes, br_politeness_wiki, br_xed_en). These domains appear only in the probe and devx.
>    - (c) **The probe and devx.** The probe's held-out sources, devx's sources and every probe / devx state are
>      excluded, and so is any row sharing more than 20% of its 12-grams with a probe or devx state (for F7, the whole
>      a/b pair). The probe's 11 iid sources are F7 train sources by design (iid = in-distribution); their probe rows
>      are fresh texts.
>    - (d) **The measured-failure frame** (F7 and the replay): no 6-word run of the failing devp_card/hate questions,
>      no "be rejected" and no "the statement that", and the words hate, hateful and non-hateful nowhere in an
>      instruction, option or card line; no dev option or label name as an F7 target label (8,863 names in v1).
>    - (e) **OHS-3 (PREREG_OHS3 rule 1).**
>      - No text from the 13 OHS-3 datasets (any split), and no text from the 8 live sources first published on or
>        after 2026-06-01.
>      - No 5-word run shared with the fixed text of the OHS-3 negation frames, lowercased with punctuation removed:
>        - T1 "would it be an error to maintain that";
>        - T2 "is it incorrect to hold that";
>        - T3 "should one reject the suggestion that";
>        - T4 "is it wrong to assert that";
>        - T5 "would one be mistaken in believing that".
>      - No answer mapping of T6's form ("answer no if …, (and) yes otherwise").
>      - No 6-word run shared with the clause-negated twin example ("is this study not interventional").
>      - Only PREREG_OHS3.md's text and build_ohs3.py's text are used for this. `data/ohs3*` is never opened by an agent.
>      - Owner 12-gram check of the whole file (`extra/fix2_ohs3_blind.py`, counts only; run by the orchestrator under
>        the owner's decision of 2 Oct). The first run, on build `08743b52…`, found hit_units_total 7 (gd_redocred 6,
>        gd_helpsteer3_pref 1), all C1's own replay rows. Both sources were then left out of the top-up whole
>        (`extra/build_fix2.py` OHS3_HIT_SOURCES; neither is a source of the 9 gate splits). The re-run on the final
>        build gave hit_units_total 0 (`yn2b/fix2_ohs3_blind.json`, sha256 21c11cc2b1498ca81ddca7bfa40046b2399683db22664657263bae95412357e0, 3 Oct).
>      - **Disclosure (owner decision before OHS-3):** golden_train itself, C1's training data and so C4's, holds those
>        units. OHS-3 can be reported with and without the overlapping OHS-3 items, identified by program, counts only.
>    - (f) **Public negation benchmarks and banned words.**
>      - A 6-word-run ban against the public negation-benchmark frames (F7 and the replay). Those files sit in a
>        decontamination-only folder that the generator never reads.
>      - SPEC §4.7's banned judge words: a hard rule for F7; report only for the replay, whose rows are C1's own
>        training text AND objective copied byte for byte (no replay relation is retyped).
>    - (g) **Label noise.** No row derives from, and no unit holds, an id of `yn2b/label_audit_known_bad_ids.json` or a
>      source row listed in `yn2b/f7_fix2_drops.json` (126 train source rows: the 3 of blind read 2 and the
>      123 the source-label audit flagged among the 2,688 real-text train source rows it read, 19 wrong, 104 ambiguous against
>      the F7 card; plus the 46 flagged probe source rows, `probe_source_row_ids`;
>      `yn2b/f7_source_label_audit.json`, `yn2b/F7_BLIND_READ_3.md`). F7 never selects a pair built from one (F7 v2
>      r5 / r6); golden units holding one leave the replay.
> 7. **The unseen-source set does not move.** `gate/check_unseen_fix2.py` derives the set from the 12 registered files
>    plus `fix2_train`. It must give:
>    - 17 sources, 3,847 rows and 0 text-guard flags;
>    - only golden_train or `gd_gen3_*` sources;
>    - no `gd_gen3_*` name matching a dev source.
>
>    It is re-run in job 3's preflight.
> 8. **The probe and the blind devx are frozen here.**
>    - `data/f7_probe.jsonl` + `_relations` + `_meta`: 2,416 rows: 1,142 iid rows (train's frames and
>      sources, fresh texts) + 1,274 held-out rows (frames, lexemes, cue combinations and sources never in
>      train), sha256 `e715fbd054bf2846410ce9034fe8c9f1b4f384efa853f9e2dd5a3d5d0d7d0710` / `eda2e82450c9b6dcd14eb141887160249f21eb9c83b1524873d17de626684d04` / `f4c8c3357730b34616e735e093d4d59ee11628ce1f6baaf65abc0634a57330d4` (byte copies of `data/v14_parts/f7_probe*`;
>      F7 v2 r6 = r4's probe minus the 82 rows of the depth-4 trim, every kept line byte-identical).
>    - `data/f7_devx.jsonl` + `_relations` + `_meta`: 220 rows (at least 100), sha256
>      `b5579786954652c201d9871a2d4e8a16c23340d4cad0254c1e5e84f8a4d34168` /
>      `74cb00c9918959480caed38a1eb409974e7284578bde125f484994dc4c7da9d2` /
>      `bc22f752d2e917f333401bfad926dfddfcf41a9d48ace2de156f6b10a11e5ac2`. It was written blind by an agent who never
>      read the F7 renderers.
>    - Their aff/dneg pair lists and the accuracy-exclusion list: `gate/fix2_pairs.json`, sha256
>      `1b7decf377289a88b307d6d188ff4eb8bdbbb61a56edbd10053992a0d6e9c999` (step 0a, run 2 Oct before any model read either file): probe 252 pairs in 178
>      held-out ladders (depth 2: 204, depth 4: 48), devx 44 pairs in 40 ladders; 213 probe rows of 45
>      ladders built from an audit-flagged source row (the probe source-label audit: 464 rows read, 5 wrong gold, 41
>      ambiguous against the probe's own cards) are left out of step P's accuracy bars.
>
> **D. Before launch (L4, about 30 min; owner GO).**
> - **0a.** `python gate/fix2_conditions.py pairs` freezes the probe's and devx's aff/dneg pair lists. These are the
>   `equiv` pairs of a ladder's anchor (aff / R0) and a yes/no row of the same ladder with an even number (≥ 2) of
>   scoping negations (dneg / N2 / N4; not a distractor-only, rewrite or choice rung), in held-out ladders: probe rows
>   with `dev_kind` "holdout", and the blind devx as a whole. Either row may carry non-scoping distractors, each one
>   program-verified to leave the gold unchanged (checklist 2.5); the pure subset (no distractor on either row) is
>   listed and reported, never decisive. Rung, depth and distractor fields come from the F7 sidecar
>   (`data/<split>_meta.jsonl`). It also freezes the **accuracy-exclusion list**: every probe row of a ladder in
>   `yn2b/f7_fix2_drops.json` `probe_report_only` (the probe source-label audit). The step runs before any model reads
>   either file. The frozen file records the sha256 of the data, relations and sidecar files (any later change to
>   any of them stops every step) and of the drops file it read; the exclusion list is then used exactly as frozen.
> - **0b. Go rule: does the probe reproduce the failure?**
>   - Read C1 and 4B-E on the probe and devx with `od_gcp predict` (gate settings, `--tag _p0`).
>   - Then run `python gate/fix2_conditions.py probe-go q35_4b_main500k_p0 q35_4b_pxE_p0`.
>   - **Go** if C1's aff/dneg flip rate is **≥ 4B-E's + 3 pp AND the paired bootstrap lower bound of the difference
>     is > 0**. The bootstrap uses 10,000 resamples over ladders, seed 0.
>   - **No go:** F7 does not capture the failure. Redesign F7 before any H100 spend. The probe is then spent: a
>     redesign builds a new probe with a new hash, and this block is revised before the new step 0.
>   - Neither read is used for anything else.
> - **A pipeline problem gives no verdict.** In 0b, R, P and N, a read that is not one clean `od_gcp predict` read of
>   this job (or a missing read) stops the step with exit 2 and NO record: it is neither a GO / NO GO nor a pass /
>   fail (PREREG_FINAL §3.4). The read is repaired (re-run cleanly) and the step is run again.
> - **Blind read 4 and the frozen probe.** Read 4 samples its 20 probe rows from audit-clean ladders only. If read 4
>   still marks a probe row wrong or ambiguous: when the cause is the row's source label, the row is report-only for
>   11.1, its ladder joins `probe_report_only` and step 0a is re-frozen (allowed only before step 0b); when the cause is
>   the F7 negation program itself, 11.1 fails and F7 is repaired (no launch).
>
> **E0. Timing of job 3 (orchestrator, 2 Oct; owner asked for speed).**
> - Job 3 is one continuous session on the original L4 `od-l4`, with one GPU type and one code commit (the commit that
>   contains this amendment). It starts with step 0a/0b (section D) and stays up.
> - **Steps E2-E4 (REF fresh3 + perm, refparity3, C1R + perm) run WHILE C4 trains on Modal.** They do not depend on C4.
>   No ship look and no C4 comparison is computed from them before C4's reads finish. Two numbers are computed early,
>   and both are environment checks that are already stop rules: refparity3 (REF vs its stored read) and step R (C1R
>   vs C1's job-1 read). Neither involves C4, and neither can make C4 pass; a failure stops the job before any C4
>   read.
> - Also while C4 trains, if C4 is not ready yet, C1R's exact 2-view reads (`--tta`, `--perm-seed 1 --tta`) run for the
>   report (E.8); otherwise they run after the verdict.
> - When C4's adapter is downloaded and verified, steps E5-E8 run in the same session. This cuts about 2 h from the
>   wall clock and changes no rule or threshold.
> - If the VM must stop between the two halves (stock-out, preemption), it restarts from the same disk and the same code
>   manifest. The preflight manifests are re-checked, and the reads already done are kept only if the manifests match.
>
> **E. Scoring job 3** (`gate/gate_4b_fix2_l4.sh`; the original L4 `od-l4`; one job, one GPU type, one code commit;
> §4 settings).
> 1. **Preflight.**
>    - The manifests: code, data, the stored REF preds, the 12 training files plus fix2, and the adapters C4, C1 and
>      4B-E.
>    - "Amendment A8-prime" is in HEAD's PREREG_FINAL.md.
>    - `check_unseen_fix2.py` passes.
>    - `STORED_REF[4b]` = `q35_4b_pxE_parity`.
> 2. **REF re-read** as `q35_4b_pxE_fresh3`: the 9 splits, eval_jagged and eval_opi (and eval_redef, report only). Also
>    its `_fresh3_perm` read of the 9 splits.
> 3. **refparity3:** `gate_dev.py q35_4b_pxE_fresh3 q35_4b_pxE_parity --mode refparity`. If it fails, stop before any
>    C1 or C4 read.
> 4. **C1R, the C1 re-read** in this job: `--name q35_4b_main500k --tag _r3` on the 9 splits, the two attack sets
>    (and eval_redef, report only), `f7_probe` and `f7_devx`. Also its `_r3_perm` read of the 9 splits.
> 5. **C4 reads:** `q35_4b_main500k_fix2` on the same splits, plus its `_perm` read.
> 6. **Steps R, P and N** (section F), in this order, each once (a JSON record in `logs/gate4b_fix2/conds/`):
>    - R: `gate/fix2_conditions.py c1parity q35_4b_main500k_r3 q35_4b_main500k` (computed right after C1R's reads);
>    - P: `gate/fix2_conditions.py precheck q35_4b_main500k_fix2 q35_4b_main500k_r3`;
>    - N: `gate/noninf_check.py q35_4b_main500k_fix2 q35_4b_main500k_r3`.
>
>    The first failure stops the job with no ship look. A step with no verdict (a pipeline problem, exit 2) records
>    nothing and stops the job; it is run again after the repair.
> 7. **The one ship look** (section G).
> 8. **Report only, after the verdict (never decisive):** C4's exact 2-view reads of the 9 splits (`--tta` and
>    `--perm-seed 1 --tta`) and `gate/twoview_report.py` for C1R and C4: 1-view vs exact identity + reversed 2-view
>    accuracy (A5 (a)), choice drift, (e) flips and Brier. This replaces the READOUT_DEV proxy with exact 2-view
>    numbers for both models.
> 9. **Only after a FINAL SHIP:**
>    - C4's `--tta-choice --tag _2v` read of the 9 splits, for the A5 temperature rule and the DEV smoke reference;
>    - C4's memo read for §6 (d) (`--splits memo4b_train_rows`).
>
>    Neither can change the verdict.
>
> - The job-1 reads of 4B-E and C1 are not reused as REF or candidate reads: §4 requires REF and every candidate to be
>   scored in one job, so every comparison is between job-3 reads (C4 vs REF fresh3, C4 vs C1R). The job-1 C1 read is
>   used only as a fixed reference: in step R (does C1R reproduce it?) and in N's extra (e) bar (32 / 662).
>
> **F. Conditions before the look.** These are computed by `gate/fix2_conditions.py` (R, P) and `gate/noninf_check.py`
> (N). None is a ship look, because REF is not involved. Each must pass, in this order. A pipeline problem in any of
> them gives no verdict (section D): nothing is recorded and the step is re-run after a repair.
> - **R. C1 re-read parity.** C1R vs C1's job-1 read must meet the §4 bar on the 9 splits:
>   - argmax agreement ≥ 99%;
>   - mean |dp| ≤ 0.005;
>   - max |dp| ≤ 0.05;
>   - accuracy within 0.3 pp;
>   - and C1R is a clean `od_gcp predict` read (otherwise: no verdict).
>
>   A failure means the pipeline drifted: stop and consult the owner. **refparity3 and R happen before any C4 read**, so
>   after a repair of the VM, job 3 may restart under a dated note: `gate/gate_4b_fix2_l4.sh vm-reset-pre-c4 "NOTE"`
>   moves `logs/gate4b_fix2/conds/R.json`, the refparity3 record and the job-3 REF fresh3 and C1R reads into
>   `logs/gate4b_fix2/reset_<UTC>/` (nothing is deleted; refused once any C4 read or any P / N / ship-look record
>   exists), then `launch` re-runs job 3 from the REF re-read. The earlier refparity3 look stays in the look ledger.
> - **P. Pre-check on non-dev data.**
>   - On the **held-out F7 probe:**
>     - C4's aff/dneg flips must be **≤ 0.5 × C1R's** (the same frozen pairs, every one of them; a cut of at least
>       50%; flips do not use gold);
>     - **and** C4's accuracy must be ≥ C1R's on all probe rows except the frozen accuracy-excluded rows (C.8), so
>       that consistency is not bought with a yes or no bias;
>     - **and** C4's accuracy must be ≥ C1R's on the **held-out** probe rows alone (`dev_kind` "holdout", the same
>       exclusions), so that a loss on the held-out part cannot hide behind gains on the iid rows (train's frames and
>       sources). Iid accuracy, all-row accuracy and the excluded rows' accuracy are reported, never decisive.
>   - On the **blind devx:**
>     - C4's accuracy must be ≥ C1R's;
>     - **and** C4's devx aff/dneg flips must be ≤ C1R's, when devx has such pairs.
>   - Every probe and devx read of both models must be complete and from this job.
> - **N. Non-inferiority vs C1, same job** (point differences; the rows and definitions of §3):
>
>   | Condition | Rule | C1's job-1 value (orientation) |
>   |---|---|---|
>   | Full set (7,056 rows, no tb_mixtral) | ≥ C1R − 0.3 pp | 81.07, so ≥ 80.77 |
>   | Primary (3,847 frozen unseen rows) | ≥ C1R − 0.5 pp | 83.99, so ≥ 83.49 |
>   | Calibrated yes/no Brier (§3.3 (d)) | ≤ C1R + 0.002 | 0.1099, so ≤ 0.1119 |
>   | (f) permutation flips | ≤ C1R + 0.5 pp | 2.43%, so ≤ 2.93% |
>   | Jagged ASR | ≤ C1R + 1 pp | 0.00%, so ≤ 1.00% |
>   | OPI ASR | ≤ C1R + 1 pp | 1.27%, so ≤ 2.27% |
>   | (e) on the 662 equiv pairs without a `hate` row | ≤ C1R's rate + 1 pp **and** ≤ job-1 C1's 32/662 + 1 pp | 4.83%, so ≤ 5.83% (≤ 38 of 662) |
>
>   - The last row is the caveat fix of section J: the pass cannot rest on the hate pairs. Its bar is stricter than
>     4B-E's own rate there (39/662 = 5.89%).
>   - Report only: the hate pairs, all 722 pairs, inv flips, complement violations, yes/no and choice, per split.
>
> **G. The one ship look.**
> - The command: `gate_dev.py q35_4b_main500k_fix2 q35_4b_pxE_fresh3 --mode ship --size 4b --json
>   logs/gate4b_fix2/look_ship_c4.json`.
> - What is unchanged (§3): the rule, every threshold, the 9 splits, the 12 training files, the unseen set, the
>   bootstrap, the parity and pipeline checks.
> - C4 is the only candidate. There is no replacement rule, no C2 / C3 / ω and no snapshot.
> - C1's look is not repeated, and the look runs at most once (look marker).
>
> **H. Verdict and fallback.**
> - **C4 ships** only if R, P and N pass **and** the look gives **SHIP and FINAL**.
> - **A NOT FINAL look** (the look's own pipeline or parity verdict) means C4 does not ship, as A7 reading 3 says for
>   job 1: 4B-E ships (§5.7), and the look is not repeated.
> - **refparity3 or R failing** (or giving no verdict) happens before any C4 read: after a repair and a dated note, job
>   3 restarts as section F (R) says; this is not a verdict on C4.
> - **Otherwise, in this order:**
>   1. **4B-E ships** (§5.7), and the 2B plan keeps 4B-E as its teacher.
>   2. **An owner override,** naming C1 or C4 instead. It is allowed only as a dated amendment committed before any
>      OHS-3 call. That amendment states the failed condition or conditions, and they are repeated on the model card
>      and in the OHS-3 report. An overridden model is never described as having passed the ship rule, and it is not
>      eligible as the 2B teacher.
> - **Never without a new amendment committed before that candidate exists:** another top-up, another look, an ω or λ
>   merge, or the C1 + 4B-E probability ensemble (the research backup, which also needs an owner decision on cost and
>   lineage).
>
> **I. The 2B teacher (resolves draft A8's "C4 never becomes the teacher").**
> - The owner's D3 (30 Sep 20:50 UTC, `yn2b/DECISIONS_owner_30sep.md`) says the teacher is the best 4B, decided before
>   arm A trains. Per that decision, this replaces §6's Default for the 2B A/B ("start the 2B with the 4B-E labels as
>   soon as they are ready. Do not wait"): arm A waits for this decision. So a shipped C4 is **eligible** as the 2B
>   teacher, under **PREREG §6 as written, all of (a)-(e)**, checked on C4 **before any 2B A/B arm trains:**
>   - **(a) Timing.** C4 and job 3 are finished before arm A trains. The A/B waits for this decision (D3).
>   - **(b) Ship rule.** C4 ships under section H, not by override.
>   - **(c) Dev-select margin.** C4 must be ≥ +1.0 pp over `q35_4b_pxE_fresh3` on all dev-select rows of the 9
>     splits. For orientation, C1 had +1.24 pp vs the job-1 fresh read on 4,102 rows.
>   - **(d) Memorisation check.** It runs on C4's memo read, made with job 3's settings on the same VM (the read meta
>     must match C4's dev reads).
>   - **(e) Budget and schedule.** The relabel of the 422,044 rows (A3 view policy, then `build_2b_kd.py` and arm A's
>     control file rebuilt; about $16-23 on Modal) is a **separate owner GO**.
> - The commands:
>   - (b)-(d): `gate/teacher_switch.py check q35_4b_main500k_fix2 q35_4b_pxE_fresh3 --ship-json
>     logs/gate4b_fix2/look_ship_c4.json` (committed code, unchanged).
>   - The memo read: `gate/teacher_switch_l4.sh` with `prereg_drafts/teacher_switch_l4_c4.patch` applied, and
>     `NO_SHUTDOWN=1 TS_GATE=gate/gate_4b_fix2_l4.sh TS_G=logs/gate4b_fix2 TS_FRESH=q35_4b_pxE_fresh3
>     TS_MANA=gate/manifest_c4_fix2.sha256 bash gate/teacher_switch_l4.sh vm-memo q35_4b_main500k_fix2` (run by
>     `vm-job3` itself after a FINAL SHIP; C4's adapter manifest is `manifest_c4_fix2.sha256`).
> - If any of (a)-(e) fails, or the GO is not given, the teacher stays **4B-E** and the 2B uses the 4B-E label files.
> - C1 is not eligible: it failed (b).
> - Every 2B arm and the 2B main run use the same teacher file.
>
> **J. The "tuned on its own test" caveat (READOUT_DEV.md), closed in three parts.**
> 1. **The new training text of the top-up, F7, never contains dev wording or dev sources** (C.6 (a), (d)). The
>    replay is C1's own golden_train rows, byte for byte with C1's own relations, so it adds no dev exposure C1 did not
>    already have (C.6 (a)). The whole top-up never contains the hate / toxicity / offensive family (C.6 (b), 0 rows),
>    the probe or devx (C.6 (c)), or the OHS-3 frames (C.6 (e)).
> 2. **The (e) pass cannot rest on the source that motivated the fix.** C4 must also pass (e) on the 662 non-hate
>    pairs, no worse than C1 + 1 pp (section N, bar 5.83%). It must also cut aff/dneg flips by at least 50% on F7
>    templates, sources and lexemes it never trained on, keep its accuracy there (all probe rows and the held-out rows
>    alone), and not lose on the blind devx (section P).
> 3. **Disclosure.**
>    - The fix was chosen after (e) failed on dev, and F7's outer frames (deny, refute, dispute, "is it false that")
>      are relatives of the dev frame. **A pass on dev (e) is therefore weak evidence.**
>    - The evidence for the skill is the probe and devx, which are non-dev but in-family or blind.
>    - **The real test is OHS-3, sealed:** complement violation on its 300 `_neg` twins, whose frames C6 (e) keeps out
>      of training.
>
> **K. Limits and claims.**
> - This is the 2nd 4B ship look. The chance of shipping a model that is not really better is a little higher than with
>   one look (§5, known limits).
> - Section N uses point differences. C4 and C1 differ little, so the margins are the bars. Its numbers are decisive
>   only as stated in section N.
> - The probe's real-text states are fresh texts of the same source datasets (never a golden_train or golden_dev state;
>   whole held-out sources in the holdout part). The probe measures consistency, not label knowledge. Its source labels
>   were audited against the probe's own cards (464 rows; 46 flagged); the flagged ladders' rows are left out of P's
>   accuracy bars by the frozen list. The aff/dneg flip counts do not use gold; P's accuracy bars do, so an unflagged
>   but wrong probe gold can still give one model or the other a row of credit.
> - The replay rehearses the gate's seen sources with C1's own rows (C.6 (a)): N's seen-source part is measured on
>   sources C4 rehearsed, as C1 trained on them; no dev row is in the file.
> - **Claims allowed if C4 ships:**
>   - "passes the pre-registered ship rule vs 4B-E";
>   - "cuts double-negation flips on held-out templates by X%";
>   - "no regression vs C1 beyond the stated margins".
> - **Not allowed without OHS-3:** "fixes negation in general".
> - The model card discloses the lineage: main500k + one top-up (program-labelled F7 nested negation and a 70% golden
>   replay; no model-made targets; no 4B-E lineage).
>
> **L. Held out.**
> - §8 is unchanged. OHS-3 runs once, after the final choice, with the model named in the PREREG_OHS3 model amendment.
> - Nothing in this amendment opened OHS-3 data or predictions.
>
> **M. Commit:** the commit that adds this amendment to PREREG_FINAL.md (its hash is in `git log`). It contains this amendment and every file a pre-registered step runs, imports or reads as a
> pinned input (found with an import trace and checked from a clean checkout of the commit: `check_unseen_fix2`,
> `check_adapter_fix2`, `build_fix2 --dry` and `f7_precheck` run there with the pinned data supplied):
> - the config: `runs/q35_4b_fix2.json` and `runs/README.md`;
> - the builders and launch tools: `extra/build_fix2.py`, `extra/build_fix1.py` (its decontamination helpers),
>   `extra/fix2_spawn.py`, `extra/fix2_dryrun.py` + `extra/fix2_dryrun.json`, `extra/fix2_ohs3_blind.py`;
> - F7: `golden_src/gen3/gen3_nested_negation.py`, `nn_lexicon.py`, `mv_core.py`, `f7_repair_r5.py`, `f7_repair_r6.py`
>   (F7 v2 r6), `v3_nested_negation.py` (the independent decide2), `data/v14_parts/f7_counts.json`,
>   `f7_holdout_spec.json`, `f7_lexicon.json` (r5 kept in `data/v14_parts/f7_v2_r5_backup/`, r4 in
>   `f7_v2_r4_backup/`);
> - the audit: `yn2b/F7_COVERAGE_CHECKLIST.md`, `yn2b/f7_precheck.py`, `yn2b/check_yn2b.py`, `yn2b/yn2b_common.py`,
>   `yn2b/check_unseen.py`, `yn2b/f7_devx_build.py`, `yn2b/f7_devx_pool_scan.py`, `yn2b/f7_precheck_fix2.json` (with
>   read 4 passed in), `yn2b/f7_precheck_fix2_ohs3.json` and `yn2b/fix2_ohs3_blind.json` (the owner's OHS-3 results),
>   `yn2b/f7_decide2_preds.jsonl`, `yn2b/f7_devx_decide2_lf.json`, `yn2b/tests/test_gen3_nested_negation.py`;
> - the label-quality record: `yn2b/f7_fix2_drops.json`, `yn2b/f7_source_label_audit.json`,
>   `yn2b/label_audit_known_bad_ids.json`, `yn2b/decontam_only/negation_benchmarks.json`, `yn2b/F7_BLIND_READ_3.md`
>   + `f7_blind_read_3_answers.tsv` + `f7_blind_read_3_verdicts.json`, `yn2b/f7_blind_read_sample3.py`,
>   `f7_blind_read_sample4.py`, `f7_blind_read_compare.py`, and blind read 4's report, answers and verdicts;
> - the frozen measurement files: `data/v14_parts/fix2_counts.json`, `data/f7_probe.jsonl` + `_relations` + `_meta`,
>   `data/f7_devx.jsonl` + `_relations` + `_meta` and `gate/fix2_pairs.json`;
> - the gate: `gate/gate_4b_fix2_l4.sh`, `gate/RUNBOOK_fix2.md`, `gate/check_adapter_fix1.py` (lora_delta),
>   `gate/check_adapter_fix2.py`, `gate/check_unseen_fix2.py`, `gate/fix2_conditions.py`, `gate/noninf_check.py`,
>   `gate/twoview_report.py`, `gate/tests/test_fix2_conditions.py`, `gate/tests/test_noninf_check.py`,
>   `gate/tests/sim_gate_fix2.py` and `gate/tests/predict_stub_fix2.py`;
> - `gate/teacher_switch_l4.sh` with the C4 patch applied;
> - `yn2b/SPEC.md` (re-hashed for A1).
>
> The training data files themselves (`fix2_train.jsonl`, `fix2_relations.jsonl`, golden_train, the F7 parts) are
> pinned by their sha256 in `fix2_counts.json` and section C, as the main run's files are.

> **Amendment A10 (3 Oct 2026, 03:10 UTC; owner decision in chat; before any OHS-3 call): owner override naming C1 =
> `q35_4b_main500k` (adapter sha256 `507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078`) as the
> shipped 4B, under A8′ H.2.**
>
> **A. The failed conditions** (to be repeated on the model card and in the OHS-3 report):
> - **Ship look 1** (1 Oct, `logs/gate4b/look_ship1.txt`): DO NOT SHIP (FINAL). One constraint failed: (e) the
>   equivalence flip rate is 8.86% vs REF 5.68% (limit REF + 2 pp = 7.68%; 64 of 722 pairs vs 41).
> - **A8′ step 0b** (3 Oct 02:10 UTC, `logs/gate4b_fix2/conds/probe_go.json` on od-l4): NO GO. On the F7 held-out
>   probe, C1 flips 87 of 252 pairs (34.52%) and 4B-E flips 86 (34.13%). The difference is +0.40 pp [−5.86, +6.75];
>   the rule needed at least +3 pp with a lower bound above 0. Per A8′ D, no C4 was trained and $0 was spent.
> - C1 is never described as having passed the ship rule.
>
> **B. What passed in look 1** (C1 vs fresh 4B-E): primary +2.47 pp [+1.31, +3.70] (83.99 vs 81.52); (a) +1.19 pp;
> (a2) dev-select +1.83 / dev-confirm +0.54; (b) yes/no +1.40; (c) choice +0.94; (d) Brier 0.1099 vs 0.1184; (f)
> permutation flips 2.43% vs 3.78%; (g) jagged ASR 0.0% vs 0.6%, OPI ASR 1.3% vs 1.8%. Parity 100%.
>
> **C. Why the owner overrides** (diagnostics on dev, disclosed as dev-based):
> - The (e) failure sits in one frame: devp_card/hate "the tweet contains only non-hateful content" with the outer
>   "Should the statement that … be rejected?". C1 flips 29 of 30 pairs there and 4B-E 0 of 30. 4B-E's consistency in
>   that frame comes from near-constant answers (affirmative p_yes 0.13 for gold 0 vs 0.21 for gold 1).
> - On the other 692 pairs C1 flips 35 and 4B-E 41. C1 is more accurate on both rows of the 722 pairs: affirmative
>   84.90 vs 83.93, double negation 84.35 vs 82.96.
> - On held-out nested negation (the F7 probe) C1 equals 4B-E (34.5% vs 34.1%).
> - OHS-3 has no double-negation twins. On every OHS-3 consistency axis C1 is better on dev: complement violations
>   3.30% vs 4.63%, option-order flips 2.43% vs 3.78%.
>
> **D. Consequences.**
> - C1 is **not** eligible as the 2B teacher (A8′ H.2). The 2B keeps 4B-E as its teacher and uses the ready 4B-E
>   2-view label file `train_2b_golden_kd_2view.jsonl`; there is no relabel.
> - The PREREG_OHS3 model amendment (at the OHS-3 step) names C1 with the sha256 above and the A5 readout for C1
>   from `prep89/READOUT_DEV.md` (T 1.00 / 1.00; choice rows read twice, given order + exact reversal; yes/no read once).
> - **OHS-3 overlap disclosure:** the owner's counts-only check found 7 golden_train units (gd_redocred 6,
>   gd_helpsteer3_pref 1) sharing 12-grams with OHS-3. C1 (and 4B-E, if its data held them) trained on them. OHS-3 is
>   reported with and without the overlapping items, identified by program, counts only (owner decision, recorded).
> - No further 4B top-up, merge or ensemble without a new amendment committed before that candidate exists.
>
> **E.** Nothing in this amendment opened OHS-3 data or predictions.

> **Amendment A11 (3 Oct 2026, 04:49 UTC; owner decision in chat "do B first"; before any B candidate exists or is read): step B,
> weight-softening (WiSE-FT) of the shipped C1.**
> - **Candidates (fixed):** W(a) = W_base + a * dW_C1 for a in {0.6, 0.7, 0.8, 0.9}, made exactly by multiplying every
>   `lora_B` tensor of C1's adapter (sha256 507d1c29...) by a (fp32), all else byte-identical. a = 1.0 is C1 itself,
>   re-read on the same machine. Names: `q35_4b_main500k_wise060` / `_wise070` / `_wise080` / `_wise090`, `q35_4b_main500k_b100`.
> - **Reads (fixed):** `od_gcp.py predict` with the gate's settings (base Qwen/Qwen3.5-4B @ 851bf6e8, layout
>   schema_branch_mark, single standard read) on the 9 gate splits, all five on one machine (od-l4, or od-l4b if
>   od-l4 is out of stock), same code sha256 as the gate.
> - **Select (dev-select half only):** a* = the candidate with the highest accuracy on the unseen-source rows of the
>   dev-select half (`gate_dev.half`, `ship_unseen_sources.json`); ties go to the larger a.
> - **Confirm (dev-confirm half), all must hold vs a = 1.0, else B adopts nothing and C1 stays:**
>   1. unseen-source accuracy >= C1 + 0.5 pp;
>   2. full set (9 splits without tb_mixtral) >= C1 - 0.2 pp;
>   3. yes/no >= C1 - 0.5 pp and choice >= C1 - 0.5 pp (full set);
>   4. raw yes/no Brier <= C1 + 0.002;
>   5. equivalence flips (722 pairs) and complement violations not above C1's.
> - **One look, no other a, no snapshot, no tuning on any held-out set.** Dev data was already looked at for the gate
>   (disclosed). If a* is adopted it replaces C1 as the shipped 4B under a dated note.
> - **Next, only with the owner's choice of yardstick:** C1 and a* (if adopted) are compared with Jev on a test where
>   Jev's answers exist. OHS-3 and LongBench v2 stay sealed.

> **Amendment A12 (3 Oct 2026, 04:57 UTC; owner decision in chat; before any OHS-1/2 read of these models): the Jev yardstick
> after step B, and the overnight branch.**
> - **Models read once on OHS-1 (`data/ohs.jsonl`, sha256 a191f42f...) and OHS-2 (`data/ohs2.jsonl`, sha256 8e7a28d9...):** C1
>   (`q35_4b_main500k_b100`, byte-identical to C1) and, only if A11 adopts it, the B winner. The machine is the same one
>   as the B reads.
> - **Readout:** the shipped A5 readout: choice rows read twice (given + exact reversal, averaged), yes/no once, T = 1;
>   `od_gcp.py predict --tta-choice`. No calibration step.
> - **Score:** `score_ohs.py` unchanged, vs Jev (`jev_guard`, `jev_r2_guard`), with the micro accuracy on base rows of
>   OHS-1 and OHS-2 pooled by row count as the yardstick. Per-test numbers, macro and Brier are also reported.
> - **Branch rule:** if the shipped 4B's pooled micro accuracy >= Jev's + 1.0 pp (point estimate), the work STOPS for
>   the owner's review. Otherwise it continues with the deep research → sealed new-domains dev suite → C dataset →
>   training round 1, each pre-registered before it runs.
> - **Disclosure:** OHS-1 and OHS-2 become practice sets from this read on. They are never used for training or for
>   choosing data. OHS-3 and LongBench v2 stay sealed.

> **Amendment A13 (3 Oct 2026, 14:27 UTC; owner decision in chat "A"; before any Decision Index item is read by a model): a
> report-only Jev Decision Index SAMPLE run on C1.**
> - **Harness:** the public `decision-index` harness (github.com/flaviusburca/decision-index), pinned commit recorded at setup.
>   Its own `suite sample` command takes about 10K requests with a fixed seed (recorded), and the harness's own metrics
>   and index formula score them. Jev and the other models' numbers come from the published board, with no Jev calls.
> - **Model:** C1 = `q35_4b_main500k` (sha256 507d1c29...), our shipped readout (choice read twice, yes/no once, T = 1),
>   run once on the L4 through a thin engine adapter that maps each Index request to our decision format. The adapter is
>   tested on a fake model first.
> - **Use:** report-only. The results (aggregates per benchmark and the index) are NEVER used to choose training data,
>   families, weights or models, and builders never see per-item results. Before any C training, C's data is
>   decontaminated against every Index TEST item. Index datasets whose TRAINING splits enter C are listed, and their Index
>   scores after C are labelled fine-tuned.
> - **Disclosures:** BANKING77 and CLINC150 are our dev sources and SGD is an OHS-1 source (evaluated, never trained). Any
>   overlap between C1's training sources and Index datasets is listed from a counts-only check.

> **Amendment A14 (3 Oct 2026, 15:20 UTC; owner goal flow, step 3; before any sealed-suite item exists): building the sealed
> new-domains dev suite (C_DATA_SPEC v3 §9; recipe v3 §6.1).**
> - **Builders:** separate agent sessions read only `c_spec/sealed_brief/` (BRIEF.md, names_only.json, c1_domain_map.md)
>   and write only to `lean/sealed_nd/`. Both folders are git-ignored. No C builder opens them, and no sealed builder
>   opens C's spec, data or style pools. The orchestrator gets counts by domain id only (D1..Dn), never domain or source
>   names or themes.
> - **Layout:**
>   - Part A: >= 5,000 real-text items over 6-10 domains, none above 20%, with >= 4 non-adjacent domains holding
>     >= 50% of items.
>   - Part P: 3 x 200 program-built items. Part B1: 300 commit items from repos in no split of CommitChronicle or
>     CommitPackFT, never n8n. Part B2: 200 long-document items (4-8K tokens).
>   - Split: sha256("ndsel:" + group_id) mod 5, where {0, 1} is select and {2, 3, 4} is confirm.
> - **Rules:**
>   - Permissive licences are verified upstream. Gold comes from humans, officials or programs, never from an LLM.
>   - Label-leak and duplicate filters are rules, not model agreement.
>   - A noise-floor read is flag-only. A domain with > 8% clearly wrong golds is dropped whole.
>   - A counts-only 12-gram check against C1's training file is run, and hits are dropped.
>   - No model reads the suite before the freeze.
> - **Freeze:** the suite file's sha256, its counts and the adjacency labels go into amendment A15 BEFORE any C data,
>   generator, pack, style or public row exists (G14). Scoring prints aggregates only. Nobody inspects per-item failures.
>   Looks follow recipe 6.2: the scorer logs and refuses any look not in the table. Jev is read once, at the C look,
>   after the ship verdict.

> **Amendment A15 (3 Oct 2026, 20:45 UTC; before any C data, generator, pack, style, public row or commit row exists, and
> before any model has read the suite): the sealed new-domains dev suite is FROZEN (G14).**
> - **Files** (git-ignored, under `lean/sealed_nd/`; never opened by C builders):
>   - suite `suite_v2.jsonl`, sha256 `f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68`;
>   - scorer `score_nd.py`, sha256 `953a3363c6b8d103d32a4c34bdda735c2a34bb5278cbffd27f292ec41841cfd7`. It verifies the
>     suite sha before every look and prints aggregates only, including the B3 yes-share block. It logs every look in
>     `looks.jsonl` and refuses any look not in recipe 6.2: S1, S2, C once, and J (Jev) once, only after a C look with a
>     recorded ship verdict.
> - **Counts.** 7,302 items in total; 2,988 select and 4,314 confirm (sha256("ndsel:" + group_id) mod 5).
>   - **Part A (headline):** 6,205 items in 8 domains, split 2,542 select / 3,663 confirm.
>     - Non-adjacent: D1, D10, D11, D12, holding 3,446 items (55.5%).
>     - Adjacent: D2, D3, D4, D5, holding 2,759 items.
>     - The largest domain is 16.1%.
>   - **Other parts:** P 600 (3 x 200); B1 298 (2 within-B1 near-duplicate groups dropped from 300); B2 199 (1
>     decontamination drop from 200; 4,148-7,718 tokens).
>   - **Item balance:** yes/no 46.5% of items, gold yes 50.0%; 58.2% card-free; 2-8 options.
> - **Adjacency labels** were fixed at pick time, before any model read, and never change. The non-adjacent ids are
>   listed above.
> - **Build history (disclosed):**
>   - v1 (9 domains, only 1 non-adjacent) failed the >= 4 non-adjacent / >= 50% rule. It was never read by a model.
>     No waiver was used: 3 new non-adjacent domains were built, and whole adjacent domains were dropped from the bottom
>     of the v1 priority list.
>   - Counts-only 12-gram decontamination against C1's training file (501,732 rows) dropped 43 v1 items and 18 new
>     items, whole groups each time.
>   - Noise-floor reads were flag-only, at most 1.5% clearly wrong per domain, and no domain was dropped.
> - **Isolation incident (disclosed):** sealed item text had spilled into shared session temp folders (tool-results,
>   task outputs, scratchpad). With the owner's OK, the 31 flagged files were deleted and the sealed workflows'
>   transcripts were moved into `sealed_nd/`. A re-scan (12-gram hashes) found 0 files with >= 3 hits outside
>   `sealed_nd/`. C builders may not open session folders (spec v4 "Who may read what").
> - **Orchestrator access:** the orchestrator has seen this suite only as counts by domain id. It has never seen any
>   domain, source or theme name, or any item.
> - **Jev read:** once, at the C look, after the ship verdict is logged, through the OHS Jev harness. The OpenRouter
>   spend is an owner GO point. The result is report-only.

> **Amendment A16 (3 Oct 2026, 21:00 UTC; after A15 and before any C training row, generator run, pack, style pool,
> codebook, public row, commit row or C candidate exists): the C plan, round 1.**
> - **Plan documents** (frozen at these sha256 prefixes; any change needs a new amendment):
>   - `c_spec/C_DATA_SPEC.md` v4 `4ca129963bef3e0a`;
>   - `c_spec/C_TRAIN_RECIPE.md` v4 `f4b7915088942f9b`;
>   - `c_spec/ADDENDUM_research.md` `0da2e8341929597e`.
>   - The G0 family specs (`c_src/<family>/G0_SPEC.md`) are frozen per family, and their sha256 is logged before that
>     family's first generator run. They are still closing their last ambiguities, and a generator cannot run until
>     its G0 has 0 open label-flip ambiguities.
> - **Model and training:**
>   - Init: C1 = `q35_4b_main500k` (sha256 507d1c29...). Same LoRA (r16/a32, QWEN35 targets) and same loss weights as
>     C1, plus the A4 ordinal term `lam_ord` 1.0.
>   - Config `runs/q35_4b_c_r1.json` (`f3bb379e...`). The seed is fixed at **20261003**. `epochs`, `expect_ord_rows`
>     and the KD counts are filled mechanically from the mixer and batch dry run.
>   - Trainer `train_decoder.py` `c2c2d1d6...`, readout `decoder_io.py` `908c08d7...`. Every change is default-off, and
>     C1 reproduces bit for bit.
>   - One candidate in round 1. Budget about $30 under the owner's GO, plus a smoke run of at most $0.5.
> - **Data, round 1:** 150,000 rows.
>   - 90,000 replay rows (60%): `c_build/replay_sample.py` `4f93a215...`, which draws round 1 nested inside round 2.
>   - 60,000 new rows: own families 45,250, licensed public 8,750, commits from other repos 6,000.
>   - G9 crowd scoring runs on the free L4 only (owner, 3 Oct).
> - **Deny-list** (`c_src/common/denylist.py` `a6dec381...`, aliases `b9cc417f...`). It reads `ohs3/used_sources.json`
>   only in-process and prints verdicts only. Orchestrator rulings:
>   - (a) Bare platform words (Wikipedia, Reddit, GitHub, arXiv, Zenodo, PubMed, ...) never match on their own. Real
>     text overlap is caught by the counts-only n-gram decontamination against OHS-1/2/3, the sealed exports, Decision
>     Index test items and JevBench items, run before every freeze.
>   - (b) An entry rejected only for label quality (silver or noisy labels) is `no_new_rows`, not `taint`. This
>     applies to T-REx, so MuSiQue (human-validated) passes. Contamination, licence, forbidden-task, dev and eval
>     entries stay `taint`.
>   - (c) "locked" counts as "avoid".
>   - (d) A10 is handled by the A8′ whole-source drop of `gd_redocred` and `gd_helpsteer3_pref`.
>   - (e) Attacked replay rows with C1 p_g < 0.2 are counted as successful attacks, not dropped. Their unit is judged
>     by its clean partner.
> - **Counters:**
>   - `c_src/common/negcount.py` uses closed lexicons, which XF17 allows before the freeze.
>   - Ruling: "neither ... nor" counts as one syntactic negation (k_syn 1), so it cannot fill the double-negation quota.
> - **Addendum D2** (facility-location selection) is NOT adopted. Selection stays stratified and representative.
> - **Gate (recipe 6.2-6.4, unchanged):**
>   - Ship: the sealed part-A confirm gain over C1 is >= +1.0 pp with LB > 0, AND guards D1-D6 and D9 pass.
>   - Round 2 runs only if the select gain is >= +2.0 pp with LB > 0 and the guards pass.
>   - Looks: S1, then (S2), then C once; Jev is read once after the ship verdict.
>   - ejs-5, OHS-1/2/3, JevBench, the Decision Index and LongBench never choose anything.
