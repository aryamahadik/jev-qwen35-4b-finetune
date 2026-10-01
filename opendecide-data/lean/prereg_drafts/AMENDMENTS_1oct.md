# PREREG_FINAL.md amendment drafts (1 Oct 2026, for owner review)

**Status: DRAFT. Nothing here is committed or appended to `PREREG_FINAL.md`.** The owner reviews each block. A block
becomes binding only when it is pasted, dated and committed at the end of `PREREG_FINAL.md` before the step named in
section 0. The text in `>` quotes is meant to be pasted. `[OWNER: …]` marks a choice the owner must make first.

Written 1 Oct, about 04:50 UTC, while the 4B main run `q35_4b_main500k` was at step 14,700 of 30,457
(`logs/main4b_seg3.log`). Everything was done on the CPU. No Modal call (not even billing), no L4, no ssh, no
paid call, no OHS-3 item text was read, and no tracked file was edited (`git status` shows the same 6 modified files
as at the start of the session). Section 8 lists what was tested and what was not.

New files from this job (all in `lean/prereg_drafts/`):
- `AMENDMENTS_1oct.md` (this file);
- `g2_noise.py`, a read-only script that measures how noisy the G2 rule and the NR5 attack rates are on stored dev preds;
- `g2_noise_result.json`, its output.

---

## 0. PREREG_FINAL.md: what is still DRAFT, and what must be committed before which step

**Facts (git and file times):**
- `PREREG_FINAL.md` is committed in `82b07d4` (tag `final-frozen`, 30 Sep 19:17 UTC). Its header still says
  **"Status: DRAFT, pending owner review"**.
- The commit message says it was committed "as it stands (still marked DRAFT), after step 0 of the run". Segment 1
  started at about 17:45 UTC (`logs/main4b_relays.md`).
- The file's last write was 30 Sep 12:27 UTC, before step 0 (`stat`). This is weak evidence. It is a file time, not a
  commit.
- This misses the file's own rule: "committed to git **before 4B step 0**" (PREREG_FINAL lines 6-8, FINETUNE_PLAN 4.1
  item 5). It must be disclosed. It is not fatal, because no snapshot, candidate or prediction of the run existed at
  the commit. `logs/ship_looks.jsonl` does not exist, and there are no `preds_*/q35_4b_main500k*` files.
- `gate_dev.py` sha256 `d1f913a3309e5de2d4a4c40bf7e9fc82558844e14710d8493457adc78d8ac95d` is the same in `82b07d4`
  and on disk now. `ship_unseen_sources.json` is `0fe61494…af95`, equal to `UNSEEN_FROZEN_SHA256`.
- `tests/test_ship_rule.py` and `yn2b/tests/test_ab_readout.py`: **37 passed** (run today).

| Place in PREREG_FINAL.md | What is still open | Text that closes it | Commit before |
|---|---|---|---|
| Header (line 3) | "DRAFT, pending owner review" | **A0** (below): the owner adopts the file as committed in 82b07d4 and discloses that it was committed after step 0 | **The first 4B candidate prediction**, i.e. the L4 scoring job of C1/C2/REF after the run ends (about 17:00 UTC 1 Oct). Rule at lines 9-10 |
| §9 Freeze record | `gate_dev.py` commit and sha256 are `________` | A0 | Same as above |
| §10 points 1-10 | defaults for the half condition, tb_mixtral, "hate", the unit, the `_perm` reads, the memorisation rows, C3's bar, parity enforcement, the text guard, the held-out transfer dev | A0 (confirm or change each point) | Same as above |
| §1 Final 2B "layout E, PRISM-X I not adopted" | overridden by the owner on 30 Sep 12:30 UTC | **A2** | **Arm A** (the first 2B training step; DECISIONS D2, SPEC §12). PREREG line 27 only asks for "before 2B step 0", so A2 meets both |
| §4 2B pinned base revision | "goes here as an amendment before the 2B is scored" | A2 (filled: `15852e8c…`) | Arm A |
| §3.6, last bullet | "PRISM-X is not in the final 2B, so latency is not affected by its CUDA-graph skip" is now wrong | A2 | Arm A |
| §6 teacher switch rule | the owner's D3 (30 Sep 20:50 UTC) changes it | **A1 part 1** item 2 | Arm A |
| §10.10 "frozen at 501,732 rows" | no longer true for the 2B file (yn2b rows, A4 drop) | A1 part 1 + **A4** | Arm A |
| (not in the file) 2-view teacher on choice rows, single view on yes/no | already applied to the 2B file on 30 Sep 22:50 UTC | **A3** | Arm A (the teacher file is an input of every arm) |
| §2 C2 snapshot steps for the 2B | "if the replay differs, the steps go here before 2B step 0" | **A1 part 3** (the replay after yn2b and A4) | **2B step 0** |
| (not in the file) yn2b dev and devx hashes, family counts, decontamination | – | **A1 part 2** | **Arm B, and any A/B read** |
| §8 / PREREG_OHS3 rule 4 | OHS-3 models, checkpoint sha256, readout, T, cascade threshold | **A5** + a PREREG_OHS3 model amendment | **The first OHS-3 run** (and A5's JevBench part before any reported JevBench run of a final model) |
| (not in the file) the optional 4B + yn2b top-up (SPEC §14) | not a pre-registered candidate (§2 lists only C1-C3) | its own amendment (candidate, REF = 4B_main, one look) | its step 0 |
| §4 "job id and git commit in the meta" | optional | not needed | – |

### Draft A0 (suggested; it is not in the job list, but §9 cannot be filled without it)

> **Amendment A0 (<date>): adoption of PREREG_FINAL.md and freeze record.**
> - The owner adopts this file as committed in `82b07d4` (tag `final-frozen`) and removes the DRAFT status.
>   [OWNER: confirm or change §10 points 1-10; the defaults are adopted unless listed here.]
> - **Disclosure.** The file was committed on 30 Sep at 19:17 UTC, about 1.5 h after 4B step 0 (about 17:45 UTC),
>   against its own rule. Its last edit was at 12:27 UTC. No snapshot, candidate prediction or ship look existed at the
>   commit.
> - **§9 freeze record:** `gate_dev.py` commit `82b07d4`, sha256
>   `d1f913a3309e5de2d4a4c40bf7e9fc82558844e14710d8493457adc78d8ac95d`. `ship_unseen_sources.json` sha256
>   `0fe614940b3008cef0e7df9d192c0be27742fce133f0976133fb3a617583af95`. `tests/test_ship_rule.py` passes.
> - [Review note, 1 Oct: the frozen `gate_dev.py` cannot give a FINAL 4B verdict (its parity stop refuses 4B-E's stored
>   metas, and the stored in-process read misses the max |dp| bar). See `prereg_drafts/AMENDMENT_A7_refparity.md`.
>   If A7 is adopted, the scoring job runs the A7 version, whose sha256 is recorded in A7's own text; this A0 record
>   of the 82b07d4 file stays as it is. Commit A0 and A7 together, before gate job 1.]

---

## 1. A2: the PRISM-X I override for the 2B

**Evidence:**
- **The decision:** the owner, 30 Sep 12:30 UTC, recorded in `logs/budget_ledger.md` after row X19 and in
  `yn2b/DECISIONS_owner_30sep.md` (D2).
- **The matched check (ledger X18):** I_1600 vs E_L4_1600 on dev-confirm was −0.27 pp [−1.34, +0.79]. The
  pre-registered gate (+1.3 pp, and a lower bound above −0.75) failed on accuracy.
- **Security:**
  - Jagged hijack 1.1% vs 10.0%, −8.9 pp [−5.7, −12.0].
  - A plain layout-E 2B is vetoed by the 2B ship rule. PREREG §7: jagged 10.0% vs v11r 3.9%, cap 6.9%, increase
    +6.1 pp [+2.8, +9.6].
- **Base revision:** `15852e8c16360a2fea060d615a32b45270f8a8fc`. Its sources are `runs/README.md:41` ("the L4 cache
  snapshot that arm I and E_L4 used") and `runs/q35_2b_main.json`. It was **not** checked against the L4's cache
  today, because that needs the VM. The stored arm metas have no load record.

> **Amendment A2 (<date>): PRISM-X arm I adopted for the final 2B (owner override for security).**
> - The pre-registered accuracy margin for I vs E_L4 failed: −0.27 pp [−1.34, +0.79] on dev-confirm (ledger X18).
> - The owner adopts arm I because a layout-E 2B at 1,600 steps would be vetoed on jagged ASR: 10.0% vs a cap of 6.9%,
>   +6.1 pp [+2.8, +9.6] (§7). I_1600 has 1.1%. Decided 30 Sep 12:30 UTC, before any 2B main-run training.
> - The final 2B config is `runs/q35_2b_main.json` with `"prism_x": "I"` (layout E + authority signal + shadow
>   memory + option-query head), at the default PRISM-X learning rates.
> - **Unchanged:** the ship rule, REF (v11r), the 2B caps (jagged 6.9%, OPI 5.4%) and the fallback (§5.7: v11r, or
>   I_1600 for a clean lineage).
> - **Correction to §3.6.** PRISM-X **is** in the final 2B. PRISM-X models refuse CUDA graphs (`PRISM_X.md:57`), so
>   the 2B is served eagerly. Its latency is measured and reported with PRISM-X on, and it is not yet measured.
> - **2B base revision for training and scoring (§4):** `15852e8c16360a2fea060d615a32b45270f8a8fc`. The scoring job
>   asserts it in the load record.
> - The 2B reads (`od_gcp.py predict`) load PRISM-X from the adapter. A read with PRISM-X off is report-only.

---

## 2. A1 part 1: the yn2b design and A/B pre-registration

Sources: `yn2b/SPEC.md` §11-12, `yn2b/DECISIONS_owner_30sep.md`, `yn2b/WAVE1A_STATUS.md`, `logs/label_check_30sep.md`.

**`<…>` values filled:**
- `<date>`: the commit date. Must be before arm A trains.
- `<sha>` of `yn2b/SPEC.md`: **`dd50cd9f7df6e7c225e1d15a3949c2e207b41f321e49644687137f97ada63b6a`** (1 Oct, 04:50
  UTC). `yn2b/` is **untracked** in git, so SPEC.md (and DECISIONS) must be committed in the same commit. Otherwise
  the hash refers to nothing anyone can check. Re-hash at commit time.
- `DECISIONS_owner_30sep.md` sha256 `76a9d8ccb10f6dc0d53d983bceb2fdab8d29e629602371668770c3e3e4b14f1b`.

**What changed from the SPEC's A1 text, and why:**
- **Item 2 (teacher).** The SPEC text ("stays 4B-E") was replaced by the owner's D3.
- **Item 3 (GPU) is new.** The SPEC says H100 (§11.3), but the owner chose the L4 first.
- **Item 6 (G2) is new.** G2 is the noisy rule; see 2.1.
- **Items 4, 5 and 7 are new.** They cover arm C (D1), the A3 teacher file and the A4 exclusion.

> **Amendment A1 (<date>): program-labelled yn2b rows for the final 2B, and the A/B that decides them.**
> 1. **Design.**
>    - `yn2b/SPEC.md` (sha256 `dd50cd9f…a63b6a`, committed with this amendment), as changed by
>      `yn2b/DECISIONS_owner_30sep.md` (sha256 `76a9d8cc…b14f1b`) and by this amendment.
>    - Up to 8 families `gd_gen3_*`. Wave 2 (F7, F8) enters only if it is green before arm B.
>    - Gold-only targets: 0.95 / 0.05, no teacher on yn2b rows.
>    - The data, arms, reads and pass rule are those of SPEC §11, coded in `yn2b/ab_readout.py` (sha256 `88727a53…d914`
>      at drafting).
>    - golden_train is unchanged, and so is the 4B. If the A/B passes, §10.10's "frozen at 501,732 rows" no longer
>      holds for the 2B's file; A4 also changes it.
> 2. **Teacher (owner decision D3, 30 Sep 20:50 UTC; this replaces the "stays 4B-E" wording of SPEC §10 D3).**
>    - The 2B teacher is the best 4B, fixed **before arm A trains**.
>    - It is the new 4B (the candidate chosen under §5) if it gets a **final SHIP verdict vs 4B-E** under §3.
>      [OWNER: do §6 (c), +1.0 pp on dev-select, and §6 (d), the memorisation check, still apply? See 2.2. Default in
>      this draft: (b) and (d) apply; (c) is dropped by D3.]
>    - Otherwise the teacher is 4B-E.
>    - A new teacher relabels the same 422,044 rows with the A3 view policy, and `build_2b_kd.py` is rerun.
>    - Every arm (A, B, C) and the 2B main run use the same teacher file. Its sha256 goes into A1 part 2.
> 3. **Hardware.**
>    - All arms train on the Google L4 and are read there in one job. If the L4 is stocked out or cannot fit the
>      recipe, all arms move to the Modal H100. The GPU type is never mixed between arms.
>    - One code commit. An infrastructure crash resumes from the checkpoint; it is never re-run with another seed.
>    - Every arm uses `runs/q35_2b_main.json`'s recipe, including `micro_tokens` 16384 and `aux_norm` "micro".
>      Under "micro" the loss depends on `micro_tokens`, so a smaller budget is a different recipe and is not allowed.
> 4. **Arm C** is run (owner D1). It is adopted only under SPEC §11.6 and with the owner's approval.
> 5. **Teacher file and exclusions.**
>    - Each arm's S is built from the A3 teacher file of the chosen teacher.
>    - A4's rows are removed from S in every arm.
> 6. **G2** [OWNER: choose]. (i) As SPEC: pooled dev_negwords + pg_dev + hard_dev, point ≥ 0.0. (ii) **Recommended:
>    point ≥ −1.75 pp**, which is about 1.9 bootstrap SDs, the same multiple as NR1-NR3. Section 2.1 gives the
>    evidence. The gain is reported either way.
> 7. **Disclosure.**
>    - The families were chosen from OHS-1/OHS-2 error analyses (no text copied), dev diagnostics on both halves, and
>      the JevBench v1.5 method text.
>    - No OHS-3 or JevBench half-B information was used.
>    - dev_negwords' held-out frame family stays out of training.
> 8. **Selection bias.** The A/B uses the dev splits for one data choice. That adds a small selection bias to the
>    later ship look, which we accept and disclose.
> 9. **Unchanged:** REF (v11r), the ship rule, the caps, §8, no JevBench submission, and OHS-3 once, blind.

### 2.1 The noisy G2 rule, and a noise-calibrated alternative

**The problem (WAVE1A_STATUS issue 4).** G2 asks for a point difference ≥ 0.0 on 2,057 rows. Rows alone make that
number noisy, so a harmless addition fails G2 about half the time.

**Evidence.** The SPEC §11.5 table (made with `scratchpad/ab_noise.py`, 2,000 resamples) and a re-run today with
`prereg_drafts/g2_noise.py` (gate_dev's `group_boot`, 10,000 resamples, seed 0). Both use the null pair 2B arm E_L4 −
arm E: the same recipe on a different GPU, with different micro-batching.

| Set | Point | 95% CI (today) | SD today (SPEC) |
|---|---|---|---|
| G2 pooled, 2,057 rows, 1,595 units | **−0.24** | [−2.03, +1.53] | **0.91** (0.89) |
| dev_negwords, 800 | −2.50 | [−5.38, +0.25] | 1.43 |
| pg_dev, 1,049 | +0.57 | [−1.91, +3.15] | 1.29 |
| hard_dev, 208 | +4.33 | [−0.45, +8.96] | 2.40 |
| Full set without tb_mixtral, 7,056 | −0.30 | [−1.29, +0.64] | 0.49 |

The points match the SPEC table exactly. The CIs differ by about 0.03 pp, because the SPEC script used 2,000
whole-set group draws. Running `ab_readout.readout()` in memory on this pair (no log written) gives **G2 FAIL**
(−0.24) while NR1-NR4 pass. **The rule as written rejects a same-recipe re-run.**

**Bar choice** (normal approximation, SD 0.91; it covers rows only, so training noise makes every false-fail rate
higher):

| G2 bar | Fails a harmless add (true 0) | Catches a true −2 pp harm | Catches −3 pp |
|---|---|---|---|
| point ≥ 0.0 (SPEC) | **50.0%** | 98.6% | 100% |
| ≥ −1.0 | 13.5% | 86.5% | 98.6% |
| ≥ −1.5 | 4.9% | 70.9% | 95.1% |
| **≥ −1.75 (recommended)** | **2.7%** | 60.9% | 91.6% |
| fail only if the 95% upper bound < 0 | 2.5% | 59.6% | 91.1% |

**Why −1.75.** In bootstrap SDs, NR1-NR3 sit at 1.8-2.3 (NR1 −1.0 / 0.49; NR2 choice −1.0 / 0.56; NR2 yes/no
−1.5 / 0.78; NR3 −1.5 / 0.65). A G2 bar of −1.75 / 0.91 = 1.9 SD makes G2 as strict as the others. It adds about 3%
to the rule's harmless-add failure rate, which is already about 20-25% from NR1-NR3 (SPEC §11.5). G2 still blocks a
clear loss of 3 pp or more on the hard external splits. The SPEC already says this A/B cannot resolve G2 effects
under about 2 pp. Coding it is one constant: `T["G2"]` in `yn2b/ab_readout.py:40`. It is not changed in this draft.

**Related flag (information, no change proposed): NR5 on the same null pair.**
- Jagged ASR is E 5.8% vs E_L4 19.2%, +13.5 pp [+9.6, +17.4]. That is above the 6.9% cap and significant, so NR5
  would **veto a same-recipe re-run** of layout E.
- The arms all carry PRISM-X I. Its family is steadier today: I 5.9%, I_1600 1.1%, I_LS0 5.8%, KI 4.4%, all under the
  cap. Arms that add parts on top of I go to 30-35%: J 30.4%, L 30.9%, O1 35.5%.
- `g2_noise.py` prints this table. A false NR5 veto in the A/B is less likely with PRISM-X I but not ruled out. The
  owner should know this before reading an NR5 FAIL.

### 2.2 Other points to settle before A1 part 1 is committed

1. **D3 vs PREREG §6.**
   - §6 lets the teacher switch only if (a) timing, (b) SHIP, (c) **+1.0 pp over 4B-E on dev-select**, (d) the
     memorisation check and (e) budget all hold.
   - D3 and the "teacher roles" note in `logs/label_check_30sep.md` say only "passes the ship gate".
   - The amendment must say which of (c) and (d) survive. My default keeps (d). It is a CPU check plus an L4 read of
     about 3K training rows; it guards against a memorised teacher. (c) is dropped, because the relabel now costs
     about $23 on Modal instead of 33 L4-hours.
2. **The L4 memory risk at 16384.**
   - The H100 2B smoke peaked at **25.38 GB reserved** (`extra/smoke2b_h100_mt16384.json`). The L4 has 24 GB.
   - Arm I ran on the L4 at 16384, but on `train_prism_arms`, not on golden rows.
   - FINETUNE_PLAN 3.6 asks for a heavy-batch smoke on the L4 before L4 use. It has not run, because of the L4
     stockout on 30 Sep.
   - If the L4 needs a smaller budget, item 3 sends all arms to the H100.
3. **Arm A's file is stale.** It was built 30 Sep from the 1-view KD file `e7b61114…`. The 2B file is now the 2-view
   file `1d44fd63…` (A3). The 4 S rows of A4 are still in it. It must be rebuilt after the teacher is fixed. S itself
   (`yn2b_ab_S_units.jsonl`) does not change.
4. **Cost table.** SPEC §11.7 uses 1.54-1.89 s/step for the 2B. The measured H100 speed is 1.99 s/step
   (`logs/label_check_30sep.md`). See A6 for the updated numbers.
5. **Operational, not pre-registration** (WAVE1A issues 5 and 6):
   - Modal skips `v14_parts` subfolders, so the V14_KEEP commit must handle the arm files;
   - the yn2b dev-file path conflict.

### 2.3 A1 parts 2 and 3: values known today (provisional; do NOT commit yet)

**Part 2** (before arm B and any A/B read). Only wave 1a is verified (`WAVE1A_STATUS.md`).

| Family | Train rows | Dev rows | Status at 04:50 UTC |
|---|---|---|---|
| F2 tool_guard | 5,202 | 524 | GREEN (decide2 100%, blind 130/130) |
| F5 lead_score | 2,160 | 200 | GREEN (blind 120/120) |
| F3 state_track | 3,780 | 349 | GREEN. The fixed build was written at 00:52 UTC (train `bfaa171f…`, dev `5f894a42…`) |
| F1 rule_chain | 4,257 on disk | 441 | wave 1b; I did not verify its gates |
| F6 def_literal | 1,650 on disk | 150 | wave 1b; I did not verify its gates |
| F4 polarity_ladder, devx | – | – | not on disk |

- Decontamination (`check_yn2b`, OHS-3 counts only) and `check_unseen`: **not run yet** on family rows.
- `MANIFEST_yn2b.jsonl` sha, yn2b_dev / devx sha: not final.

**Part 3** (before 2B step 0):
- **Replayed steps:** about 30,452 if only A4's 73 rows are dropped (rows × 0.9712363 / 16). This is an estimate.
  The real number comes from `replay_steps.py`. With yn2b it is about 31.8K.
- **C2 snapshots:** 0.85 / 0.90 / 0.95 of that count.
- **D1:** after the A/B.
- **label_smooth (SPEC §1.8):** `runs/q35_2b_main.json` has no key, so the 661 mnli yes/no rows use eps 0.08, as in
  arm I. [OWNER: confirm "as config".]

---

## 3. A3: the 2-view teacher for choice rows, and a single view on yes/no

Source: `logs/label_check_30sep.md`, sections "2-view teacher labels for choice rows" and "Checks on the 2-view
merge".

**The pre-registered rule (FINETUNE_PLAN 3.2, step 3).** Use 2 views if (TTA ≥ +0.3 pp, OR flips ≥ 3%, OR mean |dp|
≥ 0.05) AND the 2B trains on the H100.

| Rows | Flips | Mean \|dp\| | Accuracy: view / other view / 2-view average | Trigger | What was done |
|---|---|---|---|---|---|
| Choice, all 137,543 (reversed seeded view) | **17.98%** | 0.0393 | 68.05 / 68.08 / **69.51 (+1.46 pp)** | met | **2 views, averaged** |
| Yes/no, 79,666 (shards 10-13 only; letters swapped) | **3.63%** | 0.0236 | 81.16 / 81.14 / 81.25 (**+0.09 pp**) | met (flips ≥ 3%) | **1 view kept: a documented deviation** |

> **Amendment A3 (<date>): teacher views for the 2B.**
> - **Choice rows.** The FINETUNE_PLAN 3.2 trigger was met: flips 17.98% (≥ 3%), and the 2B trains on the H100.
>   - 4B-E's labels on all 137,543 choice rows are the average, in probability space, of the seeded view and its
>     exact reverse, keyed by option text.
>   - Codex's check found 0 key mismatches, 0 non-reversed views, and 0 rows where 2view ≠ (view + rev) / 2.
>   - The file is `data/v14_parts/train_2b_golden_kd_2view.jsonl`, sha256
>     `1d44fd63d43d80d23c17026cc24ac512e7107eefb9052ecd641d131025f9bdc6`, `teacher_src` q35_4b_E2v,
>     `expect_kd_targets` 450,170.
>   - The 1-view file (`e7b61114…`, 449,957 targets) is kept and not used.
> - **Where it ran.** The second view was read on the Modal H100 (aryamhd, September credit, about $10), not on the L4.
>   3.2's "the L4 has time" condition existed only to protect L4 hours, and it was not needed.
> - **Yes/no rows: deviation.**
>   - The flip criterion was met: 3.63% on shards 10-13.
>   - The second view is NOT used, because it changed accuracy by only +0.09 pp (81.16 → 81.25) and the share of soft
>     targets by +0.3 pp (41.5% → 41.8%).
>   - A full yes/no second read would cost about $9 of October credit.
>   - This was recommended on 30 Sep (following Codex) and is confirmed by the owner with this amendment. It rests on
>     training-row labels only and came before any 2B training. No dev or held-out data was involved.
> - **If a new 4B becomes the teacher (A1 item 2),** it reads both views on choice rows and one view on yes/no rows.
>   This is fixed now, whatever the new teacher's flip rates turn out to be.

---

## 4. A4: excluding the gen_numeric_dates bug rows from the 2B

**Source:** `yn2b/label_audit.md` §2, "Findings 1-2", and `yn2b/label_audit_known_bad_ids.json` (sha256
`d4de5ed1…62e5a0`).

**The bug.** `gen_numeric_dates.make_pair` builds the letter question from the base facts (`qs = s.letter_q(base)`) and
reuses it for the fact-flipped twin. The twin's gold then answers a different question:
- `tz_deadline`: all 117 raw letter twins;
- `month_add`: 4 raw twins.

`recheck()` never checks the question text. A scan of all 6,330 raw choice rows found no other schema with this
problem.

**Counted today in `train_2b_golden_kd_2view.jsonl`** (ids only, no text read):
- All 85 listed ids are present: 73 from numeric_dates and 12 from gen_tables.
- **The 73 numeric_dates rows:**
  - 44 choice rows with a fresh 2-view teacher, 2 choice rows with no teacher, 1 choice clean-copy;
  - 26 yes/no near-miss bundle rows with a fresh teacher.
- **Relations among the 73:** 16 (13 complement, 3 inv). **All of their partners are inside the 73**, so dropping the
  rows leaves no orphan relation.
- 4 of the 73 rows are in arm S.
- **There is no drop tool yet.** `merge_yn2b.py` only drops whole families. `teacher_gate_2b.py --exclude-ids` and
  `build_ab_yn2b.py --gate-exclude` only keep these rows away from the arm-C gate; they do not drop them. A small
  filter is needed in the 2B worktree.

> **Amendment A4 (<date>): known generator bug rows left out of the 2B.**
> - **Which rows.** The 73 rows of `data/v14_parts/train_2b_golden_kd_2view.jsonl` listed under
>   `gen_numeric_dates_letter_twin_question` in `yn2b/label_audit_known_bad_ids.json` (sha256 `d4de5ed1…`): 121 raw
>   rows, 73 in the 2B file. They are a confirmed pipeline bug: the question names another city or instalment than the
>   text and the gold.
> - **What happens.** They are removed from every 2B training file (arm files A, B, C and the 2B main file), together
>   with the 16 relations among them. No row is relabelled. golden_train and golden_relations stay frozen and
>   unchanged.
> - **The 12 gen_tables rows** in the same file are a wording ambiguity, not a program error.
>   [OWNER: (a) keep them, the default under FINETUNE_PLAN 3.4 ("never drop rows automatically", "fix only pipeline
>   bugs"), and keep them out of the arm-C gate with `--exclude-ids`; or (b) drop all 85.]
> - **Follow-ups.** `expect_kd_targets`, the relations count and `epochs` are recomputed with `build_2b_kd` /
>   `replay_steps.py`, and they go into A1 part 3.
> - **Deviation, disclosed.** FINETUNE_PLAN 3.4 prescribes "fix the rule and regenerate" for a generator bug. Regenerating
>   would need new rows and new teacher labels (GPU) inside a frozen golden_train. Dropping 0.015% of rows is the
>   smallest change that removes known-wrong golds.
> - **The 4B.** The live 4B (`q35_4b_main500k`) trains on these rows (121 of 501,732 raw rows; 0.02%). This is
>   disclosed and not changed. 4B-E never saw golden_train; its labels on these rows are out of sample.
> - **Not checked:** whether golden_dev holds rows with the same bug. golden_dev is report-only.

---

## 5. A5: readouts fixed before OHS-3

**What already binds.**
- PREREG_OHS3 rule 1: no prompt, threshold, temperature or readout choice on OHS-3, ever.
- Rule 4: one run per model, "in its serving configuration", with the "plain readout with the temperatures already
  fitted on dev" as primary. The models and their sha256 are named in an amendment before the run.
- A5 therefore has to define the serving readout, and it has to do that **before** the first OHS-3 run.

**Drift evidence** (`drift/RESULT_30sep.md`, `drift/drift_result.txt`). 4B-E on the L4, all 3,814 choice rows of 8 dev
splits, no OHS data. The OHS-3 mix is weighted by the twin counts in the PREREG_OHS3 text: 149 reversed, 155 rotated.

| | Single read | 2-view (identity + reversed, averaged) |
|---|---|---|
| Choice accuracy | 76.40 | 76.51 (+0.11) |
| Drift, reversed twins | 8.23% | **0.00% (by construction)** |
| Drift, rotated twins | 7.37% | 3.72% |
| Drift, OHS-3 mix | **7.79%** | **1.90%** |
| Drift at 10+ options | 17.2% | 5.0% |

- Jev's run-to-run disagreement on identical inputs is 1.14-1.98% (OHS-1/2). That is a floor for its drift.
- **Ledger X19 (dev):** 4B-E 2-view on choice rows +0.21 confirm / +0.10 select; on yes/no −0.32 / −0.09. It failed
  FINETUNE_PLAN 5.2's accuracy bar, which is +0.3 pp on choice.

**Cost and speed evidence** (`extra/SPEED_RESULT_30sep.md`, H100, CUDA graphs, 231 public JevBench items):

| Readout | p50 | JevBench speed axis | Cost axis | Tokens per decision |
|---|---|---|---|---|
| 1 read | 16.6 ms | 94.7 | 58.3 | 818 |
| 2-view, one view after the other | 31.6 ms | 93.4 | **49.3 (below the 50 gate)** | 1,636 |

- On the cost formula, 2-view moves us from $0.0245 to about $0.039 per 1K, against Jev's $0.038
  (`drift/RESULT_30sep.md`). **2-view on choice rows can turn the cost win into a tie or a loss** if cost is counted in
  tokens.
- Prefix caching could cut the real compute but not the token count. It is untested.

> **Amendment A5 (<date>, before the first OHS-3 run): readouts of the final models.**
> 1. **Choice rows, OHS-3 and production serving** [OWNER: choose one]:
>    - (a) **2-view:** identity plus reversed option order, averaged in probability space; T applied after the
>      average (`calibrate.scaled`).
>    - (b) **single read.**
>    - (c) **2-view only on rows with ≥ 10 options.** The 10 comes from the dev drift table.
>    - **Recommended: (a) for the 4B,** because consistency is a win condition and (a) roughly reaches Jev's noise
>      floor on dev.
>    - **Disclosed with (a):**
>      - drift on reversed twins is 0 by construction;
>      - (a) failed the FINETUNE_PLAN 5.2 accuracy bar and is adopted for consistency, a different objective;
>      - it costs 2x compute on choice rows (p50 16.6 → 31.6 ms on the H100);
>      - the cost endpoint must be defined in this amendment (item 5).
>    - The identity view is a by-product of the 2-view read, so OHS-3 also reports the single read as a **secondary**
>      configuration, from the same run, at no extra cost.
> 2. **Yes/no rows: single read everywhere.** The evidence is X19 (yes/no −0.32 / −0.09) and A3 (+0.09).
> 3. **JevBench only (the public-item runs; no submission): 1 read on all rows, plus the band-edge yes/no readout.**
>    - **Rule** (`projection/competitors/board_analysis.py:217`): P(yes) in (0.5, 0.8) → 0.8; P(yes) in (0.2, 0.5]
>      → 0.2; otherwise unchanged. Applied after T.
>    - **Why the band.** v1.5 scores P ≥ 0.80 as yes, P ≤ 0.20 as no, and anything between as an abstention counted
>      wrong (`bench/v154/v154lib.py:26`).
>    - **Disclosed:**
>      - it is a scorer-aware readout taken from the method text, with no fitted parameter;
>      - it is never used for OHS-3, whose Brier uses the raw T-scaled probabilities;
>      - the comparison of raw / commit / band edge (I 62.5 / 78.7 / 78.7; calibration 84.3 / 83.4 / 86.1) was made on
>        all 231 public items, **including half B**. JevBench public results are therefore development-set results,
>        not held-out ones.
>    - 2-view is not used on JevBench, because the cost axis falls to 49.3, under the 50 gate.
> 4. **Temperature** (FINETUNE_PLAN 5.1):
>    - one T per question type, fitted by NLL on pooled **dev-select** for each final model's exact serving path
>      (after the choice-row average if (a) or (c));
>    - grid 0.5-2.0;
>    - shipped T ≠ 1 only if dev-confirm pooled yes/no Brier improves by ≥ 0.002 and no split's yes/no Brier worsens by
>      more than 0.003;
>    - never fitted on OHS-1/2/3, golden_dev or JevBench.
>    - The ship rule's cross-fitted T (§3.3 (d)) is separate and unchanged.
> 5. **Before the OHS-3 run, a PREREG_OHS3 amendment names:**
>    - each model and its adapter sha256;
>    - its readout (items 1-2) and T values;
>    - the cascade threshold, if the cascade is run (FINETUNE_PLAN 5.3, set on dev-select; routing on the 2B's served
>      probabilities);
>    - the hosting setup used for the speed number;
>    - the cost formula (token-based, or measured GPU-seconds × price) used for "cost < Jev".

**What is not measured yet for A5:**
- the drift and 2-view accuracy of the **final** 4B (the numbers above are for 4B-E);
- band edge on dev (`board.md` §8 asks for the dev noul ECE / Brier check before any JevBench use);
- prefix caching;
- the 2B's 2-view cost under eager PRISM-X.

The PREREG_OHS3 text states that nearly all OHS-3 choice tasks have 20-40 options, so (a) and (c) would act almost
alike there. That fact must not drive the choice. If it is used, it is disclosed.

---

## 6. A6: budget facts (information for the owner; nothing to pre-register)

| Item | Number | Source |
|---|---|---|
| October Modal credit | 7 accounts × $30; $209 left at 00:08 UTC 1 Oct | memory `final-goal-30sep`; `logs/budget_tracker.py` |
| Real all-in rate | **$4.09/h** (H100 $19.11 + CPU $0.38 + RAM $0.19 over 4.82 h) | `budget_tracker.py:9` |
| October used so far (known) | arya-mahadik-ai $9.30 at 02:11 UTC, plus segment 3 (274 min, about $18.7) | `logs/main4b_relays.md` |
| 4B remaining | step 14,700 at 04:44 UTC; 2.68 s/step in segment 3; 15,757 steps ≈ 11.7 h ≈ **$48-49** with relay overhead; ETA about 16:45-17:00 UTC | computed from `logs/main4b_seg*.log` |
| 2B main (H100) | 1.99 s/step (grad_ckpt on, 16384) × 30,457 ≈ 17.3 h × 1.04 (yn2b) × $4.09 ≈ **$74** ($71 without yn2b) | `label_check_30sep.md`; tracker |
| Hosting test + OHS-3 inference | about $7 | tracker |
| **Essentials** | 4B rest + 2B + hosting/exam ≈ $149-150 (computed at 00:08 UTC) → **reserve about $59-60** | memory; tracker |
| Relabel by a new 4B (1 view + 2nd view on choice) | 5.6 h ≈ **$23** (required by D3 if the new 4B passes) | tracker |
| 4B + yn2b top-up (optional) | about $8 + reads | tracker; SPEC §14 |
| yn2b A/B on the L4 (default) | arm A about 3,820 steps, B and C about 4,450 each, at about 13 s/step → about 46 L4-hours + about 9 L4-hours of reads; Google credit, $0 Modal | SPEC §11.7; WAVE1A §3 |
| yn2b A/B fallback on the H100 | at 1.99 s/step and $4.09/h: A $8.6, B $10.1, C $10.1 → **about $29** (SPEC said $23-26 + $13) | computed |
| Google L4 credit | about $200 of headroom in the plan; last logged spend $20.09 (29 Sep). **Current balance not checked** | FINETUNE_PLAN §6; ledger |

**Points the owner should see:**
1. **Reserve floor.** The plan says the reserve of **$40-60 is untouchable** (`logs/overnight_plan_28sep.md:331`).
   - A new-4B relabel ($23) is required by D3 if the 4B passes. It brings the reserve to **about $36-37, under $40**.
   - The tracker's own alarm thresholds are $20 / $10 (`budget_tracker.py`), not $40. The two rules disagree.
2. **If the L4 is unavailable and the A/B falls back to the H100** (about $29), the reserve drops to **about $7-30**,
   depending on the relabel.
   - Either the optional top-up is cut and an extra $30 account is used, or arm C is skipped (−$10).
   - [OWNER: decide which gives way first.]
3. Under the essentials, segment 3 of the 4B uses most of arya-mahadik-ai's October credit. The relay plan
   (`logs/relay_transfer.sh`) keeps the per-account margin.

---

## 7. Commit order (summary)

1. **Now → before the 4B scoring job (about 17:00 UTC 1 Oct):** A0 (adoption, §9 freeze record, §10 confirmations).
2. **Teacher decision** (ship look 1 of the new 4B, plus D3's extra conditions). Then the relabel, if the new 4B is
   chosen.
3. **Before arm A trains:** A2, A3, A4, A1 part 1. Commit `yn2b/SPEC.md` and `DECISIONS_owner_30sep.md` with them.
   The V14_KEEP commit is in the 2B worktree.
4. **Before arm B and any A/B read:** A1 part 2.
5. **Before 2B step 0:** A1 part 3 (verdict, final file sha, replayed steps, C2 snapshots, D1, label_smooth).
6. **Before the first OHS-3 run:** A5 and the PREREG_OHS3 model amendment (sha256 values, readout, T, cascade, cost
   formula).
7. **Optional 4B top-up:** its own candidate amendment before its step 0.

---

## 8. What was tested and what was not

**Tested (CPU, local, read-only on data and preds):**
- `prereg_drafts/g2_noise.py` on stored dev preds:
  - the G2 and NR noise of the null pair (E_L4 − E) and of I_1600 − E_L4_1600;
  - the bar table;
  - the jagged / OPI ASR of 11 stored 2B reads.
  - Output: `g2_noise_result.json`.
- `ab_readout.readout('q35_2b_armE', 'q35_2b_armE_L4')` in memory, with no log written:
  - G2 FAIL (−0.24);
  - NR1-NR4 pass;
  - NR5 jagged FAIL (+13.5 pp);
  - permutation flips UNMEASURED, because there are no `_perm` reads.
- `pytest tests/test_ship_rule.py yn2b/tests/test_ab_readout.py`: 37 passed.
- The ids of `label_audit_known_bad_ids.json` were counted in the 2-view 2B file, together with the relations among
  them. Only ids and meta fields were read, never text.
- sha256 of every cited file; the git history of `PREREG_FINAL.md` and `gate_dev.py`; that no ship look and no
  candidate prediction exist; the 4B progress from the relay logs.

**Not tested / not verified:**
- **Nothing on a GPU.** No Modal call at all: the budget figures come from logs and memory, not live billing.
- The L4 2B memory at 16384 on golden rows, and the 2B base revision against the L4's HF cache.
- G1 / G1x noise: there are no yn2b preds.
- The A4 drop. No tool exists, and the step count was not replayed (30,452 is an estimate).
- Wave 1b gate results (F1, F6, F4, devx), decontamination and `check_unseen` on family rows.
- Band edge on dev; drift and 2-view accuracy of the final 4B; prefix caching; the 2B's latency with PRISM-X.
- Whether golden_dev has numeric_dates bug rows.
- No amendment was appended, and nothing was committed.
