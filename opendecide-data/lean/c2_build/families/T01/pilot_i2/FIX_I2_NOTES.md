# T01 fix iteration 2: double-negation wordings (Haiku path). Status: scripts written and tested on fabricated answers; Haiku not run

Failing program gate after iteration 1: G10 `double_negation_share` 0% vs bar >= 2% of yes/no rows. G6 at 6,000 rows passed
(`pilot_i1/G6_AT_6000.json`).
Cause: `pools_v2/` holds no wording for the six `yn_dneg_*` forms, so `T01.dneg_ok` is False and the sampler asks the positive form.

## What exists (all new files; no frozen pool, plugin.py, G0 text, pilot*.py or c2_kit file was edited)
The six forms were already declared (`plugin.DNEG_FORMS`, `QUESTION_FORMS_DNEG`, `fixtures.DNEG_MEANINGS`, G0_SPEC_v4 12.1), so
nothing needed declaring and no G0 sha changed. Reused: `haiku_dneg.py` (polarity-aware brief + `check_wording`: exact negcount
(2, 2), `c2_kit.polarity` P1-P4 in strict frames, word bans) and `extract.py` (G-LEX items, prompt, task text).
`haiku_dneg.py`'s own `haiku/redo4/` was never written; its 12 items per form (1.5x) are replaced by 32 per form (4x the 8 needed).

| file | role |
|---|---|
| `dneg_i2.py` | shared: items (6 forms x 32, each with its own frame x lead-in angle, inner phrasing and slot set), task writer, G-LEX registry/batches, supplement freeze/read/merge, `make_ctx_i2` |
| `dneg_stage2.py` | admission of the authoring answers, then G-LEX task files for 2 independent reads |
| `dneg_stage3.py` | G-LEX 2/2 admission, supplement freeze, G13 list, tests, determinism, pilot, G6 at 6,000 |
| `run_pilot_i2.py` | copy of run_pilot_i1 -> `pilot_i2/`; patches `freeze_v2.make_ctx` with `dneg_i2.make_ctx_i2` (reads the supplement; `pilot_loaders.py` untouched). Modes: `run`, `dry`, `determinism`, `g6 --n 6000` |
| `test_dneg_i2.py` | 6 tests on fabricated answers in a scratch folder (the kit's writers only write under `lean/`): tasks, stage 2 admit and short form, stage 3 admit/freeze/merge/drift, one-read miss, missing reads |

## Paths
- Authoring task files (8, 24 items each): `families/T01/haiku/dneg_i2/tasks/T01-author_wording-6a2c492a-00{0..7}.md`
  (index `haiku/dneg_i2/TASKS.json`). Answer files: `haiku/dneg_i2/answers/<same task id>.json` (one JSON list of `{"qid","text"}`).
- G-LEX task files (written by stage 2): `haiku/dneg_i2/glex_tasks/tasks/*.md`, index `glex_tasks/TASKS.json`, answers `glex_tasks/answers/`.
- Supplement (written by stage 3): `pools_v2/dneg_i2_supplement.json` + `pools_v2/DNEG_I2_FREEZE.json`.
- Stage reports: `haiku/dneg_i2/stage2_report.json`, `stage2_state.json`, `stage3_report.json`.
- Outputs: `pilot_i2/` (PILOT_REPORT.json, rows/relations, g5h/, g3h/ task files, G6_AT_6000.json, G13_PENDING.txt, stage3_*.log).

## Commands (from `jev/opendecide-data/lean/c2_build`; PY = `/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -B`)
1. Haiku authoring: one fresh Haiku agent per authoring task file (reads only its task file, writes only its answer file). 8 agents.
2. `PY -m families.T01.dneg_stage2` -> exit 0 when every form has >= 8 candidates; writes the G-LEX tasks.
3. Haiku G-LEX: one fresh agent per G-LEX task file; reads `glex-i2-r1` and `glex-i2-r2` are different files and must not be given to the same agent.
4. `PY -m families.T01.dneg_stage3` (add `--no-run` to freeze only). It stops (exit 1, nothing frozen) if any form has < 8 wordings with G-LEX 2/2; a missing or invalid read file is no vote.
   Then it runs: `PY -m pytest -q -x families/T01`, `PY families/T01/run_pilot_i2.py determinism`, `PY families/T01/run_pilot_i2.py run`, `PY families/T01/run_pilot_i2.py g6 --n 6000` (-> `pilot_i2/G6_AT_6000.json`).
5. Afterwards: G5-H / G3-H re-reads from `pilot_i2/g5h/`, `pilot_i2/g3h/` (the G5-H sample needs >= 10 double-negation rows).
Re-author a short form: delete nothing, edit nothing; ask for new items for that form only (4x again) and rerun stages 2-3.

## G13-seed
Not run: `g13_c2.py seed` loads the sealed exports, which a family agent never opens. The admitted wordings are listed in
`pilot_i2/G13_PENDING.txt` (written by stage 3) for the batch run, to finish before the G5-H re-read.

## gates_after
Not measured with real wordings (Haiku not run). Fabricated-answer end-to-end check only (scratch, deleted): with 6 forms x 22-32
fabricated wordings frozen into a scratch supplement, `dneg_ok` was True for all six forms and G10 double_negation_share was 6.0%
(1,000 rows) and 7.5% (6,000 rows) vs bar >= 2% (pass). In that fabricated run G6 at 6,000 rows failed by 0.1 pp on ONE cell:
choice / d_meta / lr 0.3621 vs 0.342 + 0.02 (iteration 1: 0.3523); yes/no n=3,119, yes rate 0.504, every yes/no cell within the bar.
Choice rows do not use the new forms, so this looks like the row mix shifting (yes/no quotas now draw dneg bases), not a wording
effect; but it means the real G6 at 6,000 must be checked after stage 3 and may need a look at that cell.
Open items: the real run above; G13-seed; G5-H re-read; G6 cell above.
