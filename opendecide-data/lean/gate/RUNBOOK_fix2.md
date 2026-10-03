# Runbook: 4B top-up fix2 (C4 = `q35_4b_main500k_fix2`) and gate job 3

Draft amendment A8-prime (`prereg_drafts/A8prime.md`) holds every rule. This page is the order of operations, with
the exact commands. Run everything from `opendecide-data/lean` on the Mac unless a step says VM. `PY` below is
`PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python`.

Nothing here is a ship look until step 8 ("the one ship look"), and that look runs at most once.

## 0. Status (2 Oct 2026, CPU work done; rebuilt after the fixer review)

| Piece | State |
|---|---|
| fix2 data `data/v14_parts/fix2_train.jsonl` + `fix2_relations.jsonl` | built: 42,566 rows, 10,325 relations (sha256 in `data/v14_parts/fix2_counts.json`); F7 + a 70% replay of C1's own rows, part (ii) none |
| F7 part (v2 r6) | 12,768 rows, 2,556 ladders; every real-text source label audited (train and probe; `yn2b/f7_source_label_audit.json`) |
| Config `runs/q35_4b_fix2.json` | one pass = 2,512 steps, warm-up 125; CPU dry run OK (`extra/fix2_dryrun.json`) |
| Precheck `yn2b/f7_precheck_fix2.json` | PASS 112, PENDING 1 |
| Blind read 4 (item 11.1) | **NOT DONE: needs a new agent** (step 1) |
| OHS-3 checks (8.13 and the whole file) | **NOT DONE: owner only** (step 2) |
| Step 0a `gate/fix2_pairs.json` | re-frozen on the r6 probe (sha256 1b7decf377289a88b307d6d188ff4eb8bdbbb61a56edbd10053992a0d6e9c999); the r5 freeze is void (`gate/superseded/`) |
| A8-prime | draft; not committed (step 4) |
| Gate job 3 script | `gate/gate_4b_fix2_l4.sh`; CPU simulation `gate/tests/sim_gate_fix2.py`: 39 / 39 checks (11 scenarios); unit tests 30 / 30 |

**Cost and time.** H100 on Modal (account `jaypatil-duke`, $4.09/h): about 2.10 h, about $8.58 at C1's measured
2.72 s/step (2.02 h, $8.27 at the dry run's estimate of 2.610 s/step); the hard stop below caps a runaway at
5 h = $20.45. L4 job 3 on od-l4: about 6.5-7.5 L4-hours with the report reads; the verdict lands about 4 h after
launch. Step 0b alone is about 15 min of L4.

## 1. Blind read 4 (a NEW agent; never the agent that built fix2)

1. `PY yn2b/f7_blind_read_sample4.py --out <its scratch>/blind4` (seed 20261042; prints the train file's sha256;
   excludes every id and ladder of reads 1-3).
   The 20 probe rows come from probe ladders the probe source-label audit did not flag.
2. The reader answers the 15 batches (id, answer, flag ok/amb/unr, reason) into `answers.tsv` before opening any gold.
   It must not open `golden_src/gen3/`, decide2, `yn2b/f7_fix2_drops.json`, `yn2b/f7_source_label_audit.json` or the
   hidden gold file first.
3. `PY yn2b/f7_blind_read_compare.py --dir <its scratch>/blind4`; write `yn2b/F7_BLIND_READ_4.md`,
   `yn2b/f7_blind_read_4_answers.tsv`, `yn2b/f7_blind_read_4_verdicts.json`.
4. `PY yn2b/f7_precheck.py --train data/v14_parts/f7fix2_train.jsonl --train-rel data/v14_parts/f7fix2_relations.jsonl
   --meta data/v14_parts/f7fix2_meta.jsonl data/v14_parts/f7_probe_meta.jsonl data/v14_parts/f7_devx_meta.jsonl
   --decide2-preds yn2b/f7_decide2_preds.jsonl --decide2-code golden_src/gen3/v3_nested_negation.py
   --decide2-independent yes --holdout-spec data/v14_parts/f7_holdout_spec.json --lexicon data/v14_parts/f7_lexicon.json
   --blind-read yn2b/f7_blind_read_4_verdicts.json --out yn2b/f7_precheck_fix2.json`
   - **Pass:** 11.1 PASS (0 wrong gold, unreadable + ambiguous at most 3%) and every other item PASS except 8.13
     (PENDING by design; the owner's `f7_precheck_fix2_ohs3.json` carries it, step 2).
   - **A probe row marked wrong / ambiguous** (A8' D): if the cause is the row's source label, it is report-only for
     11.1; add its ladder to `yn2b/f7_fix2_drops.json` `probe_report_only` (with the reason), move `gate/fix2_pairs.json`
     to `gate/superseded/` and re-run step 0a (only before step 0b). If the cause is the F7 negation program, 11.1
     fails: repair F7.
   - **Fail:** stop. Every flagged source row goes into `yn2b/f7_fix2_drops.json` (with its reason in
     `yn2b/f7_source_label_audit.json`); then, in order: `PY golden_src/gen3/f7_repair_r5.py dump --pool <scratch>/pool.pkl`
     (the r4 pool; about 3 min), `PY golden_src/gen3/f7_repair_r6.py repair --pool <scratch>/pool.pkl --new-out
     <scratch>/rep.json` until it lists 0 unread source rows (read any it lists first), `... repair ... --write
     --overwrite` (about 15 min: the probe trim is recomputed), decide2, re-pin and rerun `extra/build_fix2.py
     --overwrite`, both prechecks, `replay_steps.py` + the config's `epochs` / `expect_kd_*`, `extra/fix2_dryrun.py`,
     step 0a (the probe is unchanged by a train repair, so `pairs` must reproduce the frozen file), and this page's step
     0 numbers; then a fresh reader does read 5 (see `yn2b/F7_BLIND_READ_3.md` section 6).

## 2. OHS-3 checks (OWNER ONLY; agents never open OHS-3)

- `PY yn2b/f7_precheck.py --train data/v14_parts/f7fix2_train.jsonl --train-rel data/v14_parts/f7fix2_relations.jsonl
  --meta data/v14_parts/f7fix2_meta.jsonl data/v14_parts/f7_probe_meta.jsonl data/v14_parts/f7_devx_meta.jsonl
  --only 8 --ohs3-blind --out yn2b/f7_precheck_fix2_ohs3.json` -> 8.13 must be PASS (0 hit units).
- `PY extra/fix2_ohs3_blind.py --i-am-the-owner --out yn2b/fix2_ohs3_blind.json` -> exit 0 and
  `"hit_units_total": 0` (the whole fix2 file: F7 and the replay; counts only).
- Both result files are committed with A8' (section M); their sha256 and the date go into A8' C.3 and C.6 (e).
- Any hit: do not launch; the hit units must leave fix2 first.

## 3. Step 0a: freeze the probe / devx pair lists and the accuracy-exclusion list (before the commit)

`PY gate/fix2_conditions.py pairs` -> `gate/fix2_pairs.json` (put its sha256 into A8-prime C.8). It was re-run on 2 Oct
on the r6 probe (sha256 `1b7decf3…`: probe 252 pairs in 178 held-out ladders, devx 44 pairs in 40
ladders; 213 audit-flagged probe rows left out of P's accuracy bars). The r5 freeze (`gate/superseded/
fix2_pairs.r5_probe_2oct.json`) is void: the probe changed (the depth-4 trim) before any model read it. The file stays
valid only while the probe, devx, their relations and sidecars and the drops file keep their sha256, and the tool
refuses otherwise.

## 4. Commit A8-prime

1. Fill the date / time in the heading, C.3's blind-read numbers and `f7_precheck_fix2.json` sha256 (after read 4),
   and M's commit hash. Every other number is already filled from the builders' prints.
2. From the repository root: `git apply opendecide-data/lean/prereg_drafts/teacher_switch_l4_c4.patch` (checked:
   applies cleanly; env overrides only; with no TS_* variable the job-1 plan is byte-identical).
3. Append the quoted block of `prereg_drafts/A8prime.md` to `PREREG_FINAL.md`.
4. Commit together with every file of block section M (it lists every file the pre-registered steps run, import or
   read as pinned inputs). `gate/gate_4b_fix2_l4.sh manifest` refuses to run while any of them is dirty or untracked
   or HEAD's PREREG_FINAL.md lacks "Amendment A8-prime".
5. Check from a clean checkout of the commit (pinned data supplied, e.g. linked from the Mac's `data/`):
   `PY gate/check_unseen_fix2.py`, `PY gate/check_adapter_fix2.py <C1 backup> --c1 <C1 backup>` (runs; the checks fail
   on C1 itself, as they must), `PY extra/build_fix2.py --dry` (the counts of `fix2_counts.json`) and the
   `yn2b/f7_precheck.py` command of step 1.4.

## 5. L4 part 1: manifests, push, step 0b (owner GO for the L4 time)

```
bash gate/gate_4b_fix2_l4.sh manifest && bash gate/gate_4b_fix2_l4.sh start && bash gate/gate_4b_fix2_l4.sh push
bash gate/gate_4b_fix2_l4.sh launch0          # A8' 0b on od-l4, about 15 min
bash gate/gate_4b_fix2_l4.sh status           # until vm-probe0 has finished
```

- **PUSH_FIXES caution.** If `push` lists files that differ on the VM, look at the list before `PUSH_FIXES=1`. Code
  files (`od_gcp.py`, `decoder_io.py`, `prism_x.py`, `writeblock.py`, `gate_dev.py`) must be the committed versions;
  copy them only after checking that the Mac's copy is the commit's (`git status` clean). Adapters under `models/` are
  never overwritten by the script; a differing adapter is checked by hand. Step R (C1 re-read parity vs job 1) is the
  guard that the pipeline did not drift.
- Read `logs/gate4b_fix2/conds/probe_go.json` (after `pull`, or on the VM). **GO** if C1's aff/dneg flip rate is at
  least 4B-E's + 3 pp and the bootstrap lower bound is above 0. **NO GO:** stop, F7 is redesigned (A8' D), no H100 is
  spent.

## 6. GO: the H100 top-up on Modal, then job 3 at once

```
P=jaypatil-duke
MODAL_PROFILE=$P ../.venv/bin/modal run extra/fix2_spawn.py::fix2_upload_init            # once; idempotent
MODAL_PROFILE=$P ../.venv/bin/modal run --detach extra/fix2_spawn.py::fix2_spawn --stop-after-min 300
bash gate/gate_4b_fix2_l4.sh launch                                                       # job 3 part 1 starts now
```

- `fix2_spawn` refuses to spawn unless: the profile is `jaypatil-duke`; the data sha256 equal `fix2_counts.json`;
  `expect_kd_targets` / `expect_kd_full` match; the step count is one pass; the data mount is exactly the two fix2
  files; the frozen code equals C1's train_meta code; the volume's init adapter is C1 (507d1c29…).
- `--stop-after-min 300` is a cost cap (an absolute end time that survives a Modal restart). The run needs about
  2.27 h, so the cap only stops a runaway. If it ever triggers, resume with `--expect-resume` (same run, same
  checkpoint); never relaunch with other data, seed, lr or steps.
- Logs: `MODAL_PROFILE=$P ../.venv/bin/modal app logs <app id>`. After a preemption Modal restarts the input itself
  and train() resumes from its checkpoint. After a lost input:
  `MODAL_PROFILE=$P ../.venv/bin/modal run --detach extra/fix2_spawn.py::fix2_spawn --expect-resume`.
- Record the spend in `logs/budget_ledger.md`.

## 7. C4 is done: fetch, check, push (vm-job3 continues by itself)

```
bash gate/gate_4b_fix2_l4.sh fetch jaypatil-duke   # Modal volume -> backups/modal_models/q35_4b_main500k_fix2, checked
bash gate/gate_4b_fix2_l4.sh check                 # gate/check_adapter_fix2.py on the local copy
bash gate/gate_4b_fix2_l4.sh manifest-c4           # gate/manifest_c4_fix2.sha256
bash gate/gate_4b_fix2_l4.sh push-c4               # adapter first, manifest last; verified on the VM
```

The checker refuses an adapter whose train_meta step count is not the full pass or that has a snapshot folder, so a
run stopped by the cost cap can never become C4. `vm-job3` waits up to `WAIT_C4_MAX_MIN` (900) minutes for the
manifest. If it timed out, `launch` again: every finished read and condition is kept (look markers and condition
records), nothing is repeated.

## 8. Verdict

`bash gate/gate_4b_fix2_l4.sh status`, then `bash gate/gate_4b_fix2_l4.sh pull`. In order:

| Step | File | Fail means |
|---|---|---|
| refparity3 | `logs/gate4b_fix2/look_refparity3.json` | environment drift: stop, consult the owner; after a repair `bash gate/gate_4b_fix2_l4.sh vm-reset-pre-c4 "<dated note>"` (VM) and `launch` again (A8' F) |
| R (C1 re-read parity) | `logs/gate4b_fix2/conds/R.json` | pipeline drift: stop, consult the owner; after a repair the same reset (only before any C4 read) |
| P (probe / devx pre-check) | `logs/gate4b_fix2/conds/P.json` | no look; 4B-E ships (A8' H) |
| N (non-inferiority vs C1R) | `logs/gate4b_fix2/conds/N.json` | no look; 4B-E ships |
| **the one ship look** | `logs/gate4b_fix2/look_ship_c4.json` | DO NOT SHIP: 4B-E ships (or a dated owner override, A8' H). NOT FINAL: C4 does not ship either (4B-E ships, A7 reading 3); the look is not repeated |

A step that stops with **"no verdict"** (exit 2 of `fix2_conditions.py` / `noninf_check.py`: a pipeline problem or a
missing read) records nothing: it is not a failure of C4. Repair the read (remove the bad pred file and relaunch), and
the step is computed once on the clean reads.

Report only (never decisive): `logs/gate4b_fix2/twoview.json` (exact 2-view reads of C1R and C4) and
`bash gate/gate_4b_fix2_l4.sh report` (= `PY gate_dev.py q35_4b_main500k_fix2 q35_4b_main500k --mode confirm`,
cross-job C4 vs C1).

The VM shuts itself down at the end unless `NO_SHUTDOWN=1`.

## 9. Only after a FINAL SHIP

- vm-job3 has already made C4's `_2v` read (A5 temperature rule, DEV smoke reference) and the memo read for §6 (d).
- Teacher check on the Mac: `PY gate/teacher_switch.py check q35_4b_main500k_fix2 q35_4b_pxE_fresh3 --ship-json
  logs/gate4b_fix2/look_ship_c4.json --json logs/gate4b_fix2/teacher_switch.json`. The relabel of the 2B data is a
  separate owner GO (A8' I (e)).

## 10. Rehearse everything on CPU first

`PY gate/tests/sim_gate_fix2.py <scratch dir>` runs pairs -> manifest -> vm-probe0 -> vm-job3 on a throw-away tree with
a predict stub (scenarios: ok, ship, nogo, noA8, parity_fail, R_fail, wait, P_fail, noverdict, reset, parser). `bash
gate/gate_4b_fix2_l4.sh plan` prints every command of job 3 and runs nothing.
