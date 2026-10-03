# Draft amendment A8′ (A8-prime) for PREREG_FINAL.md: candidate C4 = q35_4b_main500k_fix2

**Status: DRAFT, written 2 Oct 2026 (about 00:30 UTC); rebuilt the same day after the fixer review (about 23:00 UTC):
the hate-family gap closed, the replay rehearses C1's own rows of the gate's seen sources, part (ii) dropped, F7 repaired
to v2 r6 (items 28 / 30 with negation, no negated stop-gradient anchor, depth 4 at most 3% of the probe too), the probe's
source labels audited, step P extended. It is not in PREREG_FINAL.md and nothing is committed.** Every number in the
block is printed by a builder or a check; the only blanks left are the ones that need the owner or a new agent (step
"How to adopt it" below). It supersedes `prereg_drafts/AMENDMENT_A8_fix1.md` (draft A8, "fix1"). Draft A8 was never
committed, its top-up was never launched and no fix1 model exists (no Modal run, no backup, nothing in
`logs/budget_ledger.md`).

## How to adopt it

1. Settle the owner points below (O1 is settled by the build; O2 and O3 keep their defaults unless the owner says
   otherwise).
2. **Blind read 4 by a NEW agent** (checklist item 11.1; `gate/RUNBOOK_fix2.md` step 1) on the F7 part exactly as fix2
   uses it (F7 v2 r6, `data/v14_parts/f7fix2_train.jsonl`, sha256 ffa5cecacde7ed65f0b8a105784eae3fae62007650eefd7aff7d8df5197b601c). Until read 4 passes, C.3 is not true
   and nothing below may be committed or launched. Then fill C.3's blind-read line with read 4's numbers and the sha256
   of `yn2b/f7_precheck_fix2.json` written with read 4's verdicts.
3. **Owner-only OHS-3 checks** (build agents never open OHS-3), both must report 0 and both results are committed:
   - `python yn2b/f7_precheck.py --train data/v14_parts/f7fix2_train.jsonl --train-rel
     data/v14_parts/f7fix2_relations.jsonl --meta data/v14_parts/f7fix2_meta.jsonl data/v14_parts/f7_probe_meta.jsonl
     data/v14_parts/f7_devx_meta.jsonl --only 8 --ohs3-blind --out yn2b/f7_precheck_fix2_ohs3.json` (item 8.13, the
     F7 part);
   - `python extra/fix2_ohs3_blind.py --i-am-the-owner --out yn2b/fix2_ohs3_blind.json` (the whole fix2 file: F7 and
     the replay; counts only).
   Fill their sha256, the date and the result into C.3 and C.6 (e).
4. Step 0a (`python gate/fix2_conditions.py pairs`) was re-run on 2 Oct by the fixer on the r6 probe (it reads no
   model output; the r5 freeze is kept in `gate/superseded/fix2_pairs.r5_probe_2oct.json` and is void); its sha256 is
   in C.8. Re-run it only if `gate/fix2_pairs.json` is missing; the tool refuses if the probe, devx or the frozen
   accuracy-exclusion list changed.
5. Fill the date and time in the heading. Append the quoted block to the end of PREREG_FINAL.md and commit it **before
   step 0b**, which is the first read of the F7 probe by any model. That is also before the top-up is launched and
   before the first C4 prediction. Every rule is then fixed before any probe result, training curve or C4 output
   exists.
6. The fix2 gate script refuses to run until HEAD's PREREG_FINAL.md contains the string `Amendment A8-prime` (the
   fix1 script's "Amendment A8" would also match this block, so the fix2 script uses the longer string).
7. Commit in the same commit every file listed in block section M, with `prereg_drafts/teacher_switch_l4_c4.patch`
   applied to `gate/teacher_switch_l4.sh` (from the repository root: `git apply
   opendecide-data/lean/prereg_drafts/teacher_switch_l4_c4.patch`; it applies cleanly). `gate/gate_4b_fix2_l4.sh
   manifest` refuses while any of them is uncommitted. Then follow `gate/RUNBOOK_fix2.md`.

**Owner points to settle before the commit (the defaults are written into the block):**

- **O1. Mix size vs ~2,300 steps.** The owner's settings cannot all hold at full size:
  - At batch 16, one pass of ~2,300 steps is ~36.8K rows.
  - A replay share of ≥ 70% then leaves room for ≤ 11.0K non-replay rows.
  - The checklist plans F7 at ~2,500 ladders, ~11-12K rows.
  - **Default in the block:** the coverage floors and the ≥ 70% replay share are hard rules. The step count is one
    pass of the file those rules produce. The builder prints the exact count, and the owner's GO quotes it with its
    cost (≤ $0.0044 per H100 step).
  - **Settled by the build (2 Oct, after the fixer review): F7 alone, no part (ii).** The fix1 parts (the F4 polarity
    units and the golden double-negation units) rest on real-text labels that were never audited to F7's bar (346 F4
    rows from ncbi_disease, infotabs_nli, onestop_level, logicinference and wnut17; the golden dneg units from legacy
    qnli / mnli / mrpc / rte / yahoo / massive / boolq rows, about 6% wrong by ledger D5), and in fix2 they were about
    11x up-weighted with a new objective. F7 alone passes the mix-level composition probes the checklist runs on F7
    (C1 0.5227 within 45-55%, C2 0.5761 ≤ 70%, worst depth 0.6831 ≤ 75%), so `extra/build_fix2.py
    --part2 none` (now its default) is used; the replay share stays at 70%. The step count is one pass of that file
    (section B): 2,512 steps.
- **O2. Teacher.** Block section I applies PREREG §6 to C4 in full, (a)-(e). Keeping (c) is the committed text, so
  this is the no-compromise reading.
  - Draft A1 item 2 in `prereg_drafts/AMENDMENTS_1oct.md` drops (c) by default. That file is committed (9759d31), so
    it was not edited here.
  - **When A1 is committed, replace its item-2 bracket** ("[OWNER: do §6 (c) … (c) is dropped by D3.]") with: "§6
    applies as written, all of (a)-(e), checked on the new 4B before arm A trains. For C4 that is a FINAL SHIP under
    amendment A8′ (sections H and I), (c) ≥ +1.0 pp over `q35_4b_pxE_fresh3` on all dev-select rows, and (d) the
    memorisation check (`gate/teacher_switch.py`)."
  - Also re-hash `yn2b/SPEC.md` for A1. Its D3 lines (§0 owner decisions, the R7 row, §10 D3 and the A1 text in §12)
    were rewritten on 2 Oct to state D3 as the owner changed it (`yn2b/DECISIONS_owner_30sep.md`); its §14 teacher line
    points here. The sha256 is now `63cd69f79426b6568c149809ca086372baa40bf5b9821ea39778dd512077c7f4`, not `e0f67b2b…` or `dd50cd9f…`.
- **O3. Fallback override.** If C4 fails, block section H keeps the §5.7 default (4B-E). An owner override, for example
  shipping C1 or C4 anyway, is allowed only as a dated amendment with the failure disclosed.

**What changed from draft A8 (fix1), and why:**

| Draft A8 (fix1) | A8′ | Why |
|---|---|---|
| Data: yn2b polarity units + golden double-negation units + 75% replay | F7 nested negation, built to the whole `yn2b/F7_COVERAGE_CHECKLIST.md` (MUST, SHOULD and NICE items, §3 targets, §4 audit all PASS); no fix1 part; ≥ 70% stratified replay | The research (task w74nvebvo) found fix1 does not cover the failing wording; the fix1 parts' labels were never audited |
| Same-answer pairs `equiv` | In a train ladder with an R0, same-answer links are `inv` with a = R0 (the cue-less anchor); in a ladder without R0 they stay `equiv`; opposite answers `complement`. The replay keeps C1's own relations | One-way on-policy pull toward the affirmative anchor, never toward a negated row; a data-only change (`train_decoder` lam_inv, lines 15 and 358-364) |
| Replay kept 830 rows of the hate / toxicity / offensive-language family | The family is 0 rows of the top-up: golden_train's own `meta.family` tag 'safety_policy_moderation' (7 datasets), the source name, or a family word in the instruction, an option, a card label key or any card definition line. Those domains appear only in the probe and devx | So the fix is never trained on the domain that motivated it (block C, J) |
| Replay drawn from golden_train minus every dev / eval source and every unit sharing dev wording | Replay drawn from all of golden_train except the family, the held-out (OHS) sources, the probe / devx sources and label noise: byte copies of C1's own rows, with C1's own relations, including the gate's seen sources | The fixer review: the old replay gave C4 no rehearsal on the sources behind 34.5% of the gate rows that N measures |
| No check against the OHS-3 negation frames | No shared 5-word run with OHS-3 frames T1-T5, no T6-form answer mapping | F7 v1 has **378 train rows** with "would it be an error to", a 6-word run of OHS-3 frame T1 ("Would it be an error to maintain that {p}?"). That breaks even the OHS-3 build's own 6-word criterion, and PREREG_OHS3 rule 1 bars training on those wordings. **F7 v1 cannot be used as built.** A8′ uses the stricter 5-word rule. |
| Ship look straight after the reads | Steps 0a/0b before launch; steps R, P and N before the look; C1 re-read in the same job | The skeptic review: no ship look without a non-dev pre-check, plus a non-inferiority rule vs C1 |
| "C4 never becomes the 2B teacher" | C4 is eligible only through PREREG §6 (a)-(e), checked before any 2B A/B arm; the relabel is a separate owner GO | Owner D3 (30 Sep 20:50 UTC): the teacher is the best 4B, decided before arm A trains |
| ω merge, if C4 failed a constraint on dev-select (in the research synthesis) | Not adopted: no weight is chosen on dev | The skeptic review: the ω merge double-dips on the dev rows |

**Tools behind the block** (all CPU; none logs a ship look):

| Tool | What it does | Status |
|---|---|---|
| `gate/fix2_conditions.py` | Steps 0a, 0b, R and P, exactly as written below (N is delegated to `noninf_check.py`); a pipeline problem exits 2 with no record | Built. Pair rule for F7 v2 (distractor rows allowed, devx held out as a whole, pure subset report only); the frozen accuracy-exclusion list; P's held-out accuracy bar |
| `gate/noninf_check.py` | Step N (section F table), a pure `decide()` plus the reads; a pipeline problem exits 2 with no record | Built |
| `gate/tests/test_fix2_conditions.py`, `test_noninf_check.py` | Unit tests | 30 / 30 pass (CPU) |
| `gate/twoview_report.py` | Report only: exact identity + reversed 2-view reads of C1R and C4 (A5 (a)), choice drift, flips, Brier | Built |
| `gate/teacher_switch.py` | §6 (b)-(d) for C4 | Committed, unchanged. It takes C4 with new names only |
| `gate/teacher_switch_l4.sh` | The memo read for (d) on the L4 | Needs `prereg_drafts/teacher_switch_l4_c4.patch`: env overrides only. With no TS_* variable set, behaviour is unchanged (the job-1 `plan` output is byte-identical) |
| `prep89/t_rule_check.py` | The A5 temperature rule for whichever 4B ships | Built |
| `extra/build_fix2.py` | Builds fix2 (sections C.1-C.6) and prints every count and hash | Built and run (`data/v14_parts/fix2_counts.json`) |
| `extra/fix2_spawn.py`, `extra/fix2_dryrun.py` | The Modal launcher; the CPU dry run of every launcher check and one pass of the trainer's batching | Built; dry run OK (`extra/fix2_dryrun.json`) |
| `gate/gate_4b_fix2_l4.sh`, `gate/check_adapter_fix2.py`, `gate/check_unseen_fix2.py`, `gate/tests/sim_gate_fix2.py` (+ `predict_stub_fix2.py`) | Job 3 on od-l4; C4 adapter check; C.7; the CPU simulation of job 3 | Built; the simulation passes every scenario (39 / 39 checks: ok, ship, no-go, no A8′, parity fail, R fail, wait, P fail, no verdict, reset before C4, parser) |
| `yn2b/f7_precheck.py`, the blind devx, decide2 | Checklist §4 | Built; PASS 112, PENDING 1 |
| `yn2b/f7_source_label_audit.json`, `yn2b/f7_fix2_drops.json` | Every real-text source label behind F7 train AND behind the probe audited; flagged train rows dropped, flagged probe ladders left out of P's accuracy bars | Done (`yn2b/F7_BLIND_READ_3.md`; the probe section of the audit file) |
| `golden_src/gen3/f7_repair_r5.py`, `f7_repair_r6.py` | F7 v2 r5 (the source-label repair) and r6 (the fixer review: items 28 / 30 with negation, `equiv` in R0-less ladders, the probe's depth-4 trim) | Run; r6 written (`data/v14_parts/f7_counts.json` "revision": "r6") |
| `extra/fix2_ohs3_blind.py` | OWNER ONLY: OHS-3 12-gram counts on the whole fix2 file, saved with `--out` | Built; never run by an agent |

Real-data check of the tool: `gate/noninf_check.py q35_4b_pxE_fresh q35_4b_main500k` (re-run 2 Oct; `fix2_conditions.py
noninf` calls the same code), with 4B-E standing in for C4, reproduces look 1 with the sign flipped:

| Condition | 4B-E (stand-in) | C1 | Result |
|---|---|---|---|
| Full set | 79.88 | 81.07 | FAIL (−1.19 pp) |
| Primary | 81.52 | 83.99 | FAIL (−2.47 pp) |
| Brier | 0.1184 | 0.1099 | FAIL |
| (f) | 3.78% | 2.43% | FAIL |
| Jagged ASR | 0.56% | 0.00% | pass |
| OPI ASR | 1.79% | 1.27% | pass |
| (e) without hate | 39/662 | 32/662 | FAIL (bar 5.83%) |

C1 against itself passes every condition.

---

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

---

## Notes for the builders (not part of the block)

Status on 2 Oct (all done on CPU, nothing committed):
- **F7 was rebuilt (v2) and repaired (r5, r6).** v1's problems are gone: no "would it be an error to" run (C6 (e)
  passes in the build and in precheck 8), an independent decide2 agrees 100%, the blind devx exists (220 rows, 44
  aff/dneg pairs). r6 (the fixer review) adds 18 train pairs so that items 28 and 30 reach their floor with
  negated rows (154 / 154), writes `equiv` instead of a negated `inv` anchor in R0-less ladders (470 of
  r5's links), and trims the probe's depth 4 to 3% (82 rows: 72 depth-4 rows and 10 odd-depth iid rows chosen to keep
  the dev balance checks). Every new train source row was audited (2 more rounds: 80 rows, 3 flagged). Blind read 4 (a new
  agent) is still to do.
- **Replay:** drawn without the hate / toxicity family (0 rows), without the probe and devx sources and states, without
  any unit holding a flagged source row, and WITH the gate's seen sources (C1's own rows; C.6 (a)).
- **Step 0a** was re-run on the r6 probe (`gate/fix2_pairs.json`).
- **Owner-only:** the two OHS-3 checks ("How to adopt it", step 3).
