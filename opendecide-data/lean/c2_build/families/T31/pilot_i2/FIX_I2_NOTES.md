# T31 fix iteration 2: Haiku-wording path for G10 `double_negation_share` (notes)

Status: **task files written, stage scripts written and tested on fabricated answers. No Haiku run, no pilot run yet.**
`gates_after`: not measured yet. Iteration 1 left G6 at 6,000 rows passing and G10 `double_negation_share` at 0.0% (bar >= 2%).
The pilot and the G6 run are done by `dneg_stage3.py`.

## What changed
- No generator, plugin, G0 or frozen-pool change. Backups: `_backup_i2/` (plugin.py, G0_SPEC.md, G0_SPEC_v1_1.md, run_pilot_i1.py, dneg_authoring.py).
- New (all in `families/T31/`):
  - `dneg_i2.py`: shared code. Authoring tasks, stage-2/3 logic, supplement writer and loader merge. CLI `write-tasks`.
  - `dneg_stage2.py`: admits the authoring answers and writes the G-LEX tasks.
  - `dneg_stage3.py`: G-LEX 2/2 admission, supplement, then the pilot steps.
  - `run_pilot_i2.py`: copy of `run_pilot_i1.py` writing to `pilot_i2/`.
    - Its loader `_t31_i2` is installed by `install_loader()` into `PL.LOADERS["T31"]`; `pilot_loaders.py` is not edited.
    - Flags: `--dry-run`, `--g6 --n 6000`, `--score`, `--supp-dir`, `--out-dir`, `--no-g15`.
  - `test_dneg_i2.py`: 4 tests on fabricated answers (4 passed, 224 s). The temp dir is created inside `c2_build/` because the kit's writers only write under `lean/`; it is removed afterwards.
- Authoring: 32 candidates per form = 4 x 8 wanted admitted wordings, 64 items in 4 task files (16 items each). Each item pins one of 3 outer frames, the place of the second `not` and a style. The two styles that put text before the frame are dropped. Every task file has an exact answer contract.
- Admission (stage 2): `dneg_authoring.wording_problems` (shape, placeholders, (2, 2) negation profile, polarity P1-P4, G-SL, label words), the REQ_ID rule, exact-text dedup against the other candidates and against every frozen form, lexicon add and unit test.
- Stage 3: records the 2 reads (extractor ids `d2read0`, `d2read1`; 2/2 admits) and runs `wording_problems` again. It adds the forms to a fresh pools_v2 registry and requires that no frozen form stops being admitted. It writes the supplement `pools_v2_dneg/` (sha256-checked on load). A shortfall is fewer than 6 admitted wordings in a form (exit 2, no pilot unless `--allow-short`).
- G13-seed is **not run**: `g13_c2.py seed` is a whole-block pass that reads `families/T31/pools/` only. Stage 3 lists the admitted wordings in `pilot_i2/G13_PENDING.txt` for the batch run.

## Exact paths
Task files for the orchestrator's Haiku (one agent per task; each may read only its task file and write only its answer file). The `qform` of each task is in `TASKS.json`.
```
T31/haiku/dneg_i2/tasks/T31-author_wording-a78da6e7-000.md   -> answers/T31-author_wording-a78da6e7-000.json
T31/haiku/dneg_i2/tasks/T31-author_wording-a78da6e7-001.md   -> answers/T31-author_wording-a78da6e7-001.json
T31/haiku/dneg_i2/tasks/T31-author_wording-be7b67b5-000.md   -> answers/T31-author_wording-be7b67b5-000.json
T31/haiku/dneg_i2/tasks/T31-author_wording-be7b67b5-001.md   -> answers/T31-author_wording-be7b67b5-001.json
```
(prefix `jev/opendecide-data/lean/c2_build/families/`; absolute paths, allowed read/write and prompt shas are in `haiku/dneg_i2/TASKS.json`)

## Commands (run from `jev/opendecide-data/lean/c2_build`; PY = `/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python`)
1. (orchestrator) Haiku writes the 4 authoring answer files above.
2. `PY -B families/T31/dneg_stage2.py --check` (optional dry look), then `PY -B families/T31/dneg_stage2.py`
   - Writes `haiku/dneg_i2/glex_tasks/tasks/*.md` (2 reads x ~2 files), `glex_tasks/TASKS.json` (answer paths), `admitted_candidates.json`, `QUARANTINE_AUTHORING.json` and `STAGE2_REPORT.json`.
   - Exit 0 = OK, 2 = shortfall or a problem to read, 1 = stop.
3. (orchestrator) Two independent Haiku agents, one per read (`d2read0`, `d2read1`), answer every `glex_tasks/tasks/*.md` of their read into `glex_tasks/answers/<task_id>.json`.
4. `PY -B families/T31/dneg_stage3.py --no-pilot` (admission and supplement only), then `PY -B families/T31/dneg_stage3.py` (runs the supplement step and then 5-7).
   - The second command refuses an existing supplement unless you add `--force`.
   - Stage 3 runs: pytest (`families/T31`, `c2_kit/tests`); determinism (`run_pilot_i2.py --dry-run` under PYTHONHASHSEED 1 and 2, compare rows and relations sha256); the pilot into `pilot_i2/`; G6 at 6,000 rows into `pilot_i2/G6_AT_6000.json`.
   - Outputs: `pools_v2_dneg/` (`MANIFEST.json`, `lexicon_dneg.json`, `wordings_dneg.json`, `QUARANTINE.json`), `pilot_i2/G13_PENDING.txt`, `pilot_i2/STAGE3_PILOT_STEPS.json`, `pilot_i2/PILOT_REPORT.json`, `pilot_i2/FIX_I2.json`, `pilot_i2/G6_AT_6000.json`.
   - Exit 0 only if tests, determinism, pilot, G6 (verdict pass) and `double_negation_share` (pass) all hold.
5. Separate runs of the pilot steps if needed:
   - `PY -B families/T31/run_pilot_i2.py`
   - `PY -B families/T31/run_pilot_i2.py --g6 --n 6000`
   - `PYTHONHASHSEED=1 PY -B families/T31/run_pilot_i2.py --dry-run` (and 2)
6. G5-H / G3-H: task files are written to `pilot_i2/g5h/tasks/` and `pilot_i2/g3h/tasks/` (listed in `STAGE3_PILOT_STEPS.json` under `g5h_g3h_tasks`), answers to `pilot_i2/g5h/answers/` and `pilot_i2/g3h/answers/`. After they are answered: `PY -B families/T31/run_pilot_i2.py --score`.

## Open items
- G13-seed on the new wordings (batch run, `pilot_i2/G13_PENDING.txt`); a hit means removing that wording from the supplement (re-run stage 3 with `--force`) and re-running the pilot.
- G5-H needs double-negation rows in its 100-row sample. Stage 3 reports the dneg row count (`dneg_rows`); check that the sample holds some before reading.
- The G-LEX read has to tell a double-negation wording from `yn_holder_not` / `yn_agent_not`. Rejections there are expected; that is what the 4x oversampling is for.
- A shortfall after the 2/2 read would need a second authoring round, which this iteration does not provide.
