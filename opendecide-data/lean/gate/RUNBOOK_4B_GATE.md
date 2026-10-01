# Runbook: the 4B ship gate on the L4 (q35_4b_main500k vs 4B-E)

Written 1 Oct 2026, ~05:30 UTC, while the 4B was still training (it finishes ~17:00 UTC). Everything here was prepared
and tested on CPU only.
- Script: `gate/gate_4b_l4.sh`.
- Rules: `PREREG_FINAL.md` sections 2-5 and `FINETUNE_PLAN.md` 4.4-4.5.
- VM: `od-l4`, us-central1-a, project system-one-509903, folder `~/lean`, python `~/od/bin/python`.

## 0. Blocker: decide amendment A7 before job 1

As frozen, the gate **cannot give a FINAL verdict**. Details and patches: `prereg_drafts/AMENDMENT_A7_refparity.md`.
1. **The tool refuses the parity look.** `gate_dev.py <fresh> q35_4b_pxE --mode refparity` stops at once, because
   4B-E's stored metas say base Qwen3.5-2B. Every ship look against `q35_4b_pxE` stops the same way.
2. **The bar fails even with that fixed.** The 30 Sep `od_gcp predict` read of 4B-E (`q35_4b_pxE_parity`, same L4,
   same pipeline) fails the max |dp| ≤ 0.05 bar against the stored in-process read: max 0.0986 (one pg_dev row; 3 of
   8,143 rows are above 0.05, all long pg_dev / devp_card rows). The other
   three checks pass (agreement 99.57%, mean |dp| 0.0026, accuracy +0.06 pp). The new fresh read will almost surely
   fail too, and PREREG 4 then says stop.

**Recommended: option a.** The stored REF becomes `q35_4b_pxE_parity`, a one-line change. It must be committed before
the first candidate read exists, that is before `launch job1`.
- The script checks this in its preflight. With the frozen `gate_dev.py` it stops with exit 2 before reading anything.
- With option b alone it stops at the parity look, before any candidate is read.

## 1. What the gate reads and decides

**How 4B-E's reference reads were made** (from `preds_*/q35_4b_pxE*.meta.json`):

| Read | How it was made | Usable by the ship rule? |
|---|---|---|
| `q35_4b_pxE` (stored REF; 9 splits + eval_jagged/opi/redef + breadth_dev) | The **in-process** read at the end of `od_gcp.py train` on the L4: an unmerged PEFT model, torch 2.14.0+cu130, CUDA 13.0. The meta has no load record and says base "Qwen/Qwen3.5-2B" by mistake (train.cfg: 4B, layout schema_branch_mark, r32/a64, no base_revision in the cfg) | No: in-process reads always fail the pipeline check |
| `q35_4b_pxE_parity` (9 splits) | `od_gcp.py predict --name q35_4b_pxE --base Qwen/Qwen3.5-4B --revision 851bf6e8… --layout schema_branch_mark`. Merged (`merge_and_unload`), bf16, L4, `forced: []`, chat_template_sha a4aee8af…, perm_seed None, TTA off, 1,560 s for 8,143 rows. 30 Sep 11:25 UTC | Yes, a clean read. This is the amendment-a stored REF |
| `q35_4b_pxE_tta` (9 splits) | An older predict read with `--tta`. No load record | No |

**Reads the gate makes**, all from one scoring setup:
- `HF_HUB_OFFLINE=1 od_gcp.py predict --base Qwen/Qwen3.5-4B --revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
  --layout schema_branch_mark`, with no `--force` and no TTA.
- The adapter is merged in bf16 on the L4.

| Name | Model | Splits | Why |
|---|---|---|---|
| `q35_4b_pxE_fresh` | 4B-E (`--tag _fresh`) | the 9 splits + eval_jagged + eval_opi (+ eval_redef, report only) | The REF is always a fresh read (PREREG 4). It must **not** be named `q35_4b_pxE`, or it would overwrite the stored preds |
| `q35_4b_pxE_fresh_perm` | 4B-E (`--tag _fresh_perm --perm-seed 1`) | the 9 splits | Constraint (f), permutation flips |
| `q35_4b_main500k` | C1, the final adapter | the 9 splits + attack sets | Candidate |
| `q35_4b_main500k_perm` | C1 (`--tag _perm --perm-seed 1`) | the 9 splits | (f) |
| `q35_4b_main500k_c2` (+ `_perm`) | C2 = cat average 0.25 each of s025888, s027411, s028934 and the final adapter | as C1 | Candidate. It is materialized by `gate/materialize_cat.py` so it can be read with `od_gcp.py predict` (a `blend` read can never be FINAL) |

- **Snapshots:** s025888, s027411 and s028934 are `int(f × 30457)` for snap_fracs 0.85, 0.90 and 0.95. These are the
  names `train_decoder` writes.
- **The other snapshots** (every 2,500 steps) are used only if the run dies before 85% (section 7).

**Looks, in PREREG 5 order.** Each one is logged to `logs/ship_looks.jsonl` and runs at most once (markers in
`logs/gate4b/looks/`).
1. **REF parity:** `gate_dev.py q35_4b_pxE_fresh <STORED_REF> --mode refparity`.
   - It runs after ALL the fresh-REF reads, because the look fingerprints them, `_perm` included.
   - It runs before any candidate is read. If it fails, the job stops (exit 10) and you consult the owner.
2. **C3 trigger:** `gate_dev.py q35_4b_main500k q35_4b_pxE_fresh --mode c3trigger`. If it says TRIGGER, job 1 ends and
   job 2 is needed (section 5).
3. **Choice** (`gate/replacement_rule.py`): C2 replaces C1 only if it is ≥ +0.3 pp on dev-select AND ≥ 0 on
   dev-confirm. Both are micro point differences over all 8,143 rows.
4. **Ship look 1:** `gate_dev.py <chosen> q35_4b_pxE_fresh --mode ship --size 4b`.
   - SHIP, and FINAL → done.
   - NOT FINAL → stop and consult the owner.
5. **Ship look 2:** only if the chosen model is C2 and look 1 said DO NOT SHIP. It tests C1 vs REF.
6. **Otherwise:** fall back to 4B-E (PREREG 5.7). The 2B plan is unchanged, because its teacher is 4B-E.

## 2. Time and cost (L4)

The per-split times come from the 30 Sep parity read (1,496 s for the 9 splits; 0.057 s/row + 0.10 s per 1K
characters). The attack sets are estimated at about 12 min.

| Step | L4 time |
|---|---|
| One standard read (9 splits + jagged + OPI + redef) | ~38 min |
| One `_perm` read (9 splits) | ~26 min |
| **Job 1:** REF, C1 and C2, each with a standard and a `_perm` read | **~3.4 L4-hours** (wall clock ~3.5 h after launch) |
| **Job 2, only if C3 triggers:** REF re-read (std + perm), C1 re-read (std), 2 merge-check reads (9 splits), C3 (std + perm) | **~3.7 L4-hours** |
| Gate CPU work (preflight hashes 1.6 GB; each ship look ~25 s) | a few minutes |

- **Cost:** about $1 per L4-hour (Google credit, not Modal), so ~$3.5 for job 1 and ~$3.7 more for job 2.
- **Transfer:** about 0.7 GB of adapters goes Mac → VM. If the VM lacks `data/v14_parts/golden_train.jsonl`
  (1.2 GB), see section 6.

## 3. Step by step

Run from `~/Documents/jev/opendecide-data/lean` on the Mac. `G=gate/gate_4b_l4.sh`.

```
# 0. Before ~17:00 UTC: owner decides amendment A7 (prereg_drafts/AMENDMENT_A7_refparity.md), patches, tests, commits.
bash $G plan                                   # every command of both jobs, nothing runs

# 1. After the 4B finishes (train_meta.json exists on the last account's volume; see logs/main4b_relays.md):
#    final adapter from the LAST relay account; each snapshot from the account whose segment covered its step
bash $G fetch <last_profile> final
bash $G fetch <profile_with_step_25888> s025888      # repeat for s027411, s028934 (same or other accounts)
#    -> ~/Documents/jev/backups/modal_models/q35_4b_main500k/{., snaps/s0xxxxx} (the one local copy, backup policy)
bash $G check                                  # r16/a32, 496 fp32 tensors, cfg == runs/q35_4b_main.json, steps 30457,
                                               # snapshot steps, chat template a4aee8af..., no PRISM-X
bash $G manifest                               # gate/manifest_4b.sha256 + gate/manifest_adapters.sha256
                                               # (refuses if gate_dev.py / PREREG_FINAL.md / the A7 test are not committed)

# 2. VM
bash $G start
bash $G push                                   # adapters -> ~/lean/models/q35_4b_main500k, gate/ -> ~/lean/gate, verify
#   if push lists files that differ (e.g. gate_dev.py after the amendment, or a missing training file):
#   BUT if od_gcp.py or decoder_io.py differ, diff the VM copy against the Mac's first: the 30 Sep parity read was
#   made with the VM's code of that morning, so a changed prompt/readout path makes the parity look fail.
PUSH_FIXES=1 bash $G push
bash $G launch job1                            # nohup on the VM; the VM shuts itself down at the end
bash $G status                                 # any time (needs the VM up): event log tail + GPU use

# 3. Results (the VM has shut down)
bash $G start && bash $G pull && bash $G stop  # preds, logs/gate4b/, ship JSONs; merges logs/ship_looks.jsonl
cat logs/gate4b/summary.json                   # decision + every look
#   then add the looks to logs/budget_ledger.md by hand (PREREG 5: every look goes to the ledger too)
```

**The exact copy commands** inside `push` and `pull` (gcloud, zone us-central1-a, project system-one-509903):
```
gcloud compute scp --zone us-central1-a --project system-one-509903 --quiet --recurse \
    ~/Documents/jev/backups/modal_models/q35_4b_main500k od-l4:~/lean/models/
gcloud compute scp --zone us-central1-a --project system-one-509903 --quiet --recurse \
    ~/Documents/jev/opendecide-data/lean/gate od-l4:~/lean/
gcloud compute ssh od-l4 --zone us-central1-a --project system-one-509903 --command \
    "cd ~/lean && sha256sum -c --quiet gate/manifest_4b.sha256 && sha256sum -c --quiet gate/manifest_adapters.sha256"
# back to the Mac, per pred dir d in preds_{dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev,eval_jagged,eval_opi,eval_redef}:
gcloud compute scp --zone us-central1-a --project system-one-509903 --quiet "od-l4:~/lean/$d/q35_4b_main500k*" $d/
gcloud compute scp --zone us-central1-a --project system-one-509903 --quiet "od-l4:~/lean/$d/q35_4b_pxE_fresh*" $d/
gcloud compute scp --zone us-central1-a --project system-one-509903 --quiet --recurse "od-l4:~/lean/logs/gate4b/*" logs/gate4b/
gcloud compute scp --zone us-central1-a --project system-one-509903 --quiet od-l4:~/lean/logs/ship_looks.jsonl logs/ship_looks.vm.jsonl
```

**What the VM job checks before reading** (preflight, exit 2 on any failure):
- The sha256 of the code, the data, the 12 training files and the stored REF preds match the Mac's manifest.
- The adapters match their manifest, and the three snapshots and the final adapter are present.
- The base revision is in the HF cache.
- No other `od_gcp.py` job is running and the GPU is idle.
- There is at least 4 GB of free disk.
- `gate_dev.py`'s own size check accepts the stored REF. This is where the frozen tool stops.

## 4. Reading the outcome (`logs/gate4b/summary.json`, `logs/gate4b/events.log`)

| Exit / outcome | Meaning | Next |
|---|---|---|
| `ship:q35_4b_main500k` or `ship:q35_4b_main500k_c2` | FINAL SHIP | New 4B ships. Teacher switch: see section 8 |
| `fallback:q35_4b_pxE` | FINAL DO NOT SHIP (look 2 too, if it ran) | Ship 4B-E; the 2B plan is unchanged |
| `job1-c3-trigger` | C1 fails (b), (c), (d) or (g) on dev-select | `bash $G start && bash $G push && bash $G launch job2` (section 5) |
| exit 10 | The REF parity look FAILED | **Stop and consult the owner.** No candidate was read in this job |
| exit 11 | Parity passed but does not count (wrong stored REF, splits, or an unclean fresh read) | Fix the setup; the look is logged |
| exit 12 | C2 and C3 both meet the replacement rule | The owner chooses (PREREG is silent) |
| exit 13 | A ship look is NOT FINAL | Decide nothing; read `logs/gate4b/look_ship1.txt` (the NOT FINAL reasons) |
| exit 2-8 | Preflight, read, build or tool error | Read `logs/gate4b/events.log` and `reads.log`. Fix, then `launch` again: finished reads are skipped and made looks are not repeated |

## 5. Job 2 (only after "C3 TRIGGER")

1. **Builds:** C3 = cat(0.75 × final + 0.25 × 4B-E), plus the merge-check adapters (1,0) and (0,1). All three are
   materialized.
2. **REF re-read:** 4B-E is re-read as `q35_4b_pxE_fresh2` (std + `_perm`), and its own parity look follows.
3. **C1 re-read:** C1 is re-read as `q35_4b_main500k_j2` (std).
4. **Merge checks** (PREREG 2), on the 9 splits:
   - (1,0) vs `_j2` and (0,1) vs `_fresh2`;
   - each needs ≥ 99.5% agreement and mean |dp| < 2e-3.
   - If either fails, C3 is out, and the choice is C1 vs C2 of job 1.
5. **C3 reads:** C3 is read (std + `_perm`).
6. **Choice** among C1, C2 and C3.
   - Extra conditions for C3:
     - every constraint passes on select AND on confirm (see note 1 below);
     - its confirm accuracy is ≥ C1 − 0.3 pp and ≥ the fresh REF's;
     - its yes/no accuracy is ≥ C1's.
   - **Note 1:** "every constraint" is read here as (b), (c), (d) and (g), as in the C3 trigger. Amendment A7 asks the
     owner to confirm this.
   - The ship look for C3 is against `_fresh2`; C1 and C2 use job 1's REF.

## 6. Fallback: ship looks on the Mac

Use this if the VM lacks a training file and uploading 1.2 GB is slow, or if you simply want the looks on the Mac.
```
STOP_BEFORE_SHIP=1 bash $G launch job1        # the flag is passed to the VM job
# ... when the VM has shut down:
bash $G start && bash $G pull && bash $G stop && bash $G local-ship job1
```
- In this mode the VM still makes the parity look and the C3 trigger. It does not need the training files.
- The pulled ledger carries the parity look; the pred files are byte-identical, so its fingerprint still matches.
- The choice and the ship looks then run on the Mac and are logged to the Mac's ledger.

## 7. Other cases

- **The run dies before 85%** (plan 4.6). The candidates become:
  - the last `_ckpt` adapter;
  - the `cat` average of the last 3 every-2,500 snapshots.

  Same rule. The script does not automate this case; use `gate/materialize_cat.py` and the same read and look commands
  (`plan` prints them).
- **The run dies after 85% but before the end.** PREREG is silent. The relay can resume, so finish the run rather than
  improvise.
- **The VM is busy** (2B A/B or labels). The preflight refuses to share the GPU. Every read and every model must come
  from one setup, so do not split the gate across machines.
- **Mid-run snapshot check** (plan 4.3): not part of this gate.

## 8. Teacher switch (PREREG 6): not automated

The 2B teacher switches to the new 4B only if all of these hold:
- (b) a FINAL SHIP;
- (c) ≥ +1.0 pp over the fresh 4B-E on dev-select. `summary.json` reports this as `teacher_switch_c_dev_select_diff_pp`
  when the outcome is SHIP;
- (d) the memorisation check;
- (e) budget and schedule.

(d) needs one more read of the new 4B on a seed-0 sample of golden_train rows, with the same count per source as the
3,209 seen-source dev rows. That is about 10 L4-minutes. It is not prepared here; build it only if (b) and (c) pass.

## 9. Tested on CPU, and not tested

**Tested (1 Oct, Mac, nothing paid, nothing written outside `gate/`, `prereg_drafts/` and the scratch folder):**
- **Ship-mode dry runs on the real 9 splits** (`--no-log`):
  - `q35_4b_pxE_parity` vs itself: diff 0, primary FAIL, NOT FINAL (no `_perm` or attack reads, no parity look).
  - `q35_4b_pxE_tta` vs `q35_4b_pxE_parity`: primary −0.21 [−0.59, +0.17], DO NOT SHIP, NOT FINAL.
  - Any look against the stored `q35_4b_pxE` stops with the base error. This is defect 1.
- **Refparity with the b fix** (scratch copy, `--no-log`): `q35_4b_pxE_parity` vs `q35_4b_pxE` gives PARITY FAIL,
  max |dp| 0.0986. This is defect 2.
- **`gate/tests/sim_gate.py`: 27/27 checks pass.** It runs the whole script (`manifest` then `vm-job1` / `vm-job2` /
  `local-ship`) in throw-away trees. They use real data, real stored preds, real main-run snapshots (s002500 and s005000
  stand in for the final adapter and the late snapshots) and a stub in place of `od_gcp predict` (copied
  probabilities). Scenarios:
  - frozen tool → stops in preflight;
  - b only → parity FAIL, no candidate read;
  - a → full job: all 9 constraints measured, FINAL verdicts;
  - re-run → nothing repeated;
  - SHIP path;
  - STOP_BEFORE_SHIP + local-ship;
  - C3 trigger → job 2 (builds, merge checks, choice of C3, two ship looks).
- **`gate/materialize_cat.py`:**
  - on the real snapshots: ΔW exact to 6e-16 relative;
  - with 4B-E for C3: 4e-8 relative;
  - against PEFT 0.21.0 `add_weighted_adapter(cat)` (`gate/tests/peft_equivalence_check.py`, tiny random model):
    bit-identical in fp32. In bf16, the blend path rounds A/B to bf16 first (a difference of one bf16 ulp). (1,0)
    reproduces the member exactly.
- **Inputs to `od_gcp.py predict`:**
  - every `predict` command line parses with `od_gcp.parser()` and gives the intended output names;
  - `decoder_io.resolve_prompt` resolves 4B-E, a main-run snapshot and the materialized C2 and C3 with `forced: []`.
- **`gate/check_adapter.py`:** passes both real snapshots and rejects 4B-E and a snapshot posing as the final adapter.
- **Ship-rule tests with the amendment applied** (scratch copies): `tests/test_ship_rule.py` plus
  `prereg_drafts/test_amendment_A7.py` give 31/31 for a (1 skip) and 32/32 for a + b.

**Not tested** (needs the GPU, the VM or the network; these are the first things to watch):
- any real `od_gcp predict` read;
- whether a fresh 4B-E read reproduces `q35_4b_pxE_parity` within the bar (it depends on the VM's software being
  unchanged since 30 Sep 11:25 UTC; the preflight's code sha check covers our code, not pip packages);
- the read speed of a rank-64 (C2) or rank-48 (C3) merged adapter (merged, so it should be the same);
- the `modal volume get` file-to-folder behaviour in `fetch`;
- every gcloud command (start, stop, scp, ssh, nohup launch) and the VM's `sudo shutdown`;
- whether the VM already has the 12 training files and identical code and data (`push` reports this);
- the real time per read (the estimates come from the 30 Sep log).

## 10. Files
- `gate/gate_4b_l4.sh`: the script (every phase; `plan` prints all commands).
- `gate/materialize_cat.py`: the exact `cat` average written as one PEFT adapter (C2, C3 and the merge-check adapters),
  with a `--verify` mode.
- `gate/replacement_rule.py`: the choice among C1, C2 and C3.
- `gate/merge_check.py`: the C3 (1,0) / (0,1) check.
- `gate/check_adapter.py`: the check on downloaded adapters.
- `gate/tests/sim_gate.py`, `gate/tests/predict_stub.py`, `gate/tests/peft_equivalence_check.py`: the CPU tests.
- `prereg_drafts/AMENDMENT_A7_refparity.md`: the amendment, with the patches `amendment_A7a_gate_dev.patch` and
  `amendment_A7ab_gate_dev.patch` and the tests `test_amendment_A7.py`.
