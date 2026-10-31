# rrun: cloud CPU runner for family jobs (PREREG_FINAL A20 a)

`c_build/rrun.py` runs a family's generator, solver-B or QC command **unchanged** in a Modal CPU container
(profile `jaypatil-duke`, app `od-rrun`, no GPU), then copies the outputs back to the Mac. It changes no data, no
gate and no training math: same code, same absolute paths, same package versions as the venv.
This file follows the `rrun.py` docstring (the code is the reference if they ever differ).

## What runs where

| Item | Remote |
|---|---|
| Python | 3.12.10 (= venv) |
| Packages | exact venv versions of the packages the c_src scripts import, plus their linux dependency closure (`pins()`); torch = venv version, CPU wheel |
| Models | `sentence-transformers/all-MiniLM-L6-v2` @ 1110a243 and the `Qwen/Qwen3.5-4B` tokenizer files @ 851bf6e8, baked into the image's HF cache; sha256 of every file checked against the Mac's HF cache at build; `HF_HUB_OFFLINE=1` |
| Paths | everything sits at the Mac's absolute paths (`/Users/aryamahadik/Documents/jev/opendecide-data/...`); `.venv/bin/python` is a symlink to the image's python |
| Uploaded | `c_src/<FAM>` + `c_src/{common,formats,packs,public,COMMIT}` + c_src top-level files (all families with `--all-fams`), **including `*/tmp/**`** (drop big unused inputs with `--exclude`); `__pycache__`, caches and `*.npz` are skipped. Also `lean/{decoder_io,train_decoder,prism_x,writeblock}.py`, `PREREG_FINAL.md`, `c_spec/{C_DATA_SPEC,C_TRAIN_RECIPE,LICENCE_REGISTER}.md`, and `--in` / existing `--out` paths |
| Never uploaded | **nothing under `lean/sealed_nd/`**. Each `sealed_nd/qc/*.py` (names listed, never opened) is replaced remotely by a stub that exits 97 and marks the run FAILED, so a sealed check can never pass in the cloud: run sealed checks on the Mac. Never-open names are refused: `sealed_brief`, `prep89`, `bench` (as path parts), `ohs3`, `preds_ohs` and `jev` **anywhere** in a path (any case), `RESEARCH_`/`REVIEW_`/`LICENCE_CHECK_` files, `ADDENDUM_research.md`, `..`, symlinks |

Uploads use Modal's content-hashed mounts: only new or changed files are sent (a local hash cache keyed on size,
mtime, ctime and inode skips re-hashing unchanged files). A preflight walks exactly what will be uploaded and refuses
the whole run if any path is a never-open name or a symlink (fail closed). The mounts land under `/rrun_stage` and are
copied (`cp -a`) to the real paths at container start, so the job can write anywhere. `--need` is obsolete (accepted,
ignored), since `tmp/**` is uploaded by default.

## Sync back (three-way, sha256)

- Synced roots: files the job created or changed under `c_src/<FAM>` (only the `--sync-back REL ...` relpaths if
  given) and under each `--out` path. Changes elsewhere are listed as WARN and not copied back.
- The container records the sha256 of every file in the synced roots before the command runs (= the uploaded copy).
  On return, for each changed file:
  - local file still equals the uploaded copy -> overwritten in place;
  - local file already equals the remote result -> left alone;
  - the job created the file and no local file appeared meanwhile -> written in place;
  - anything else (local file edited or deleted after the upload, or created locally during the job) -> written as
    `<name>.remote` next to it, with a WARN; the local file is never touched.
- **Failed job** (rc != 0, killed at its time budget, a sealed stub called, or stdout held by an orphan process):
  every file lands as `<name>.remote`, and its `progress_phase2.log` lines stay in the run log only. `--sync-on-fail`
  syncs a failed job's files by the normal rule.
- New `c_build/progress_phase2.log` lines from a successful job are appended to the local log (file lock).
- Local mtimes are the sync time (never backdated). Deleted files are not mirrored. `--sync-to DIR` writes under
  `DIR/<absolute path>` instead (tests, comparisons), still judged against the real local files.

## Cost guard

- **Hard limits = request:** the container runs with `cpu=(c, c)` and `memory=(m, m)`. Without a limit Modal lets a
  container use up to request + 16 cores (seen: 2 -> 18 ... 16 -> 32 in `os.cpu_count()`) and more memory than
  requested, and bills max(request, use). With the limits, billing is the request, so a job that needs more memory
  than `--mem` is OOM-killed (FAILED, nothing synced in place) instead of being billed more.
- Rates: CPU $0.0000131 per core-second + memory $0.00000222 per GiB-second (16 cores + 32 GiB is about $1.01 per
  hour; 2 cores + 4 GiB about $0.13 per hour). Estimate = rate x the remote call's wall time.
- **Reservation:** before launch rrun takes a file lock, sums settled runs + every open reservation, and writes this
  run's reservation = rate x (container timeout + 60 s), the true worst case. The container timeout is
  min(`--timeout`, what is left under $15). The run row closes the reservation when it settles.
- The guard also reads the real od-rrun spend (`modal billing report`, cached in `c_build/rrun_billing.json`) and uses
  max(ledger, billing + open reservations). No launch once that would pass **$15**.
- Ledger: one reservation row and one run row per launch in `c_build/rrun_ledger.jsonl` (fam, cmd sha256, cpu, mem,
  limits, seconds, est cost, rc, Modal app id). A run log with the output tail goes to `c_build/rrun_logs/<run_id>.log`.
- `logs/budget_ledger.md` holds **one** `| rrun running total |` row, fixed width, rewritten in place on every settle
  (so other writers' appended lines are never lost and the row is never duplicated). It is the rrun spend figure;
  the `| rrun milestone $5 |` and `| rrun milestone $10 |` marker rows are not additive.
  `rrun.py --budget-row` refreshes the row and the billing cache without running anything.
- Check real spend: `.venv/bin/modal billing report --for "this month" --json --profile jaypatil-duke`.

## Adoption test (A20 a): PASSED, re-run on the current code 6 Oct 01:14-01:23 UTC

Record: `c_build/RRUN_ADOPTION.json` (rrun.py sha256 `226aaafb3392...`; earlier runs listed there too).

| Test | Local | Remote (current code, hard limits) | Verdict |
|---|---|---|---|
| 1. Deterministic gate: F5 `qc/g10.py candidates_r1` | 7 s wall | 2.2 s run, 12 s launch-to-done (2 cores) | byte-identical JSON `59625ced8714...` (= the family's own file) |
| 2. Seeded learner gate: G8v2 `g8_aflite.py run --family F5` | 643 s (jobs 2, cached embeddings; lane's run) | 391 s run (jobs 16, 16 cores: 211 s single-thread embedding + 174 s AFLite) | both pass; real share 0.1497 vs 0.1491 (2 x seed sd = 0.013); acc 0.4613 both; remote JSON identical to the previous remote run except timing |
| 3. Generator build: F5 `python -m gen.build --set smoke` | 5.0 s (17:32 run) | 6.4 s run, 16 s launch-to-done | rc 0, 118 rows, 34 bases, 6 files synced (to a scratch dir), progress line kept; no trainer swap needed any more |

Billing check after the fix: Modal billed the G8 run's CPU and memory in exactly the 16-core : 32-GiB request ratio
(CPU $0.0610, memory $0.0206), and `os.cpu_count()` in the container now equals the request (2, 4, 8, 16), so
billing = request. Each billed amount was at or below the ledger estimate.

## Usage

Run a family's heavy generator, solver-B or QC job with
`/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_build/rrun.py --fam F5 [--cpu 16] [--mem 32] [--timeout 3h] -- <command>`.
The command is exactly what you would type in `c_src/F5` (one quoted string for shell syntax such as `&&` or `>`).
Files it creates or changes in the family folder come back in place by the three-way rule. Anything that changed
locally meanwhile comes back as `<name>.remote`. Use `--out <lean-relative path>` for outputs outside the family
folder (for example a G8v2 report under `c_build/g8v2/`), `--in <lean-relative path>` for other inputs, and
`--exclude` to skip big unused inputs. Start it with `nohup ... > log 2>&1 &`, **with the log outside `c_src/`**
(e.g. under `c_build/` or your scratchpad), and poll the log; the last line is `RRUN_RESULT {...}` and the exit code
is non-zero for any failure. `--plan` prints the upload and the cost bound without running. Sealed checks
(`lean/sealed_nd/`) must run on the Mac. Use one platform per family for all gate re-runs (A20 a). Cost is about $1.0
per hour at 16 cores + 32 GiB; small single-thread jobs (G10, G12, smoke builds) are fine with `--cpu 2 --mem 4`.

## Notes and known issues

- **Hard limits change speed, not results.** Before the fix a container could use request + 16 cores; now it gets
  exactly `--cpu`. The G8 AFLite step took 174 s on 16 limited cores against 87 s when it could burst to 32. Ask for
  the cores you want to pay for (e.g. `--cpu 32 --mem 32` for G8v2 with `--jobs 32`) and pass the job count
  explicitly; set it to `--cpu` so threads do not oversubscribe.
- **Logs inside the upload:** rrun never uploads its own stdout/stderr file. Another job's `*.log`/`*.out`/`*.err`
  being written during the upload used to abort the launch (Modal: "... was modified during build process", $0). rrun
  now skips that file and retries (up to 3 times, WARN, recorded as `not_uploaded_live_logs` in the ledger row). Any
  other file changing during the upload still aborts the launch: the input snapshot would not be consistent.
- G8v2 sets 1 BLAS thread, so its first-time embedding is single-threaded (about 210-240 s for 9,026 F5 texts). The
  embedding cache (`c_build/g8v2/cache/*.npz`) is not uploaded, so every remote G8 run re-embeds. This costs time,
  not quality.
- **Trainer blocker: resolved.** During the first adoption runs the working-tree `lean/train_decoder.py` was an
  uncommitted edit (sha 1dbfe7806597), so the formats-1 card loader check refused every row. Re-checked 6 Oct 01:11
  UTC: the file is sha256 `c2c2d1d623cc...` = git HEAD, git status clean (mtime 00:56:45 UTC), and the remote smoke
  build passed with the live file (no swap).
- **Early runs uploaded the sealed_nd/qc program directory.** Five launches of the first adoption tests (t1, t2, t3,
  t3b and t3b's failed first try, 6 Oct 00:10-00:17 UTC) used an earlier rrun.py that mounted the whole
  `lean/sealed_nd/qc/` directory into the jaypatil-duke Modal workspace (as mounts of those ephemeral apps; logs in
  `c_build/rrun_adopt/t1_g10_remote.log`, `t2_g8_remote.log`, `t3_smoke_remote.log`, `t3b_smoke_remote*.log`). The
  current code uploads nothing under `sealed_nd`.
- Deleted files are not mirrored back; `.remote` copies need a manual merge.
