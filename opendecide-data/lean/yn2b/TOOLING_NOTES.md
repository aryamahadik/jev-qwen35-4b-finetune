# yn2b tooling: what the other builders need (builder E, 30 Sep 2026)

Every tool's docstring holds its full contract. The tests are in `yn2b/tests/`. Run them with:

`PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider yn2b/tests`

## Tools

| Tool | What it does |
|---|---|
| `assemble_yn2b.py` | Reads the raw files where `mv_core.FamilyBuilder.write()` puts them, converts them with `mv_core.assemble()`, and adds the file-level checks. The raw format is mv_core's; there is no second converter. |
| `check_yn2b.py` | SPEC 7 decontamination on the ASSEMBLED files. |
| `check_unseen.py` | SPEC 7.4 unseen-set check. |
| `build_ab_yn2b.py` | Builds the arm files. |
| `teacher_gate_2b.py` | Option B / arm C. |
| `merge_yn2b.py` | Builds the final 2B file. |
| `ab_readout.py` | The SPEC 11.5 pass rule. |

## assemble_yn2b.py

It adds these checks on top of mv_core:
- the drop list;
- F4(a) base rows checked against golden_train;
- decoder_io card round-trip;
- no latent on both sides of a split;
- SPEC 4.9 unit sizes;
- `train_decoder.check_rows`.

## check_yn2b.py

It reads the assembled files and writes a drop list for `assemble_yn2b.py --drop`.

**OHS-3.**
- OHS-3 is read only inside `ohs3_blind()`.
- The output is counts per family only.
- Dropped units are stored as salted hashes. Never reverse them.

**Optional inputs from the generators.**
- `--names names.json`: `{"gd_gen3_<name>": ["Invented Name", ...]}`, the name pools, for SPEC 7.7.
- `--templates templates.json`: `[{"family", "kind": "instruction"|"plant", "text", "flips": bool}]`.
  - Without it, the rendered instructions and mv_core's `PLANT_TEMPLATES` / `SPOOF_TEMPLATES` are checked instead.
  - Checked on 30 Sep: mv_core's plant templates share no 6-word run with any reference set.

**Answer-flipping rows for the cue-share rule.** A row counts as answer-flipping when:
- `role == "neg"`; or
- `meta.polarity` is odd.

## F4(a): the S units (builder A)

- The S units are in `data/v14_parts/yn2b_ab/yn2b_ab_S_units.jsonl`, one line per merged unit:
  `{"key", "call_ids", "group_ids", "n_rows"}`. There are 44,029 units and 62,999 rows.
- The base row of an F4(a) row must be in an S unit with `n_rows <= 4` (SPEC 5 F4, 4.9).
- `build_ab_yn2b.py` refuses an F4(a) row whose base is outside S.
- `merge_yn2b.py` refuses a merged unit with more than 8 rows or more than 24K state characters.

## Arm files

**Location.**
- The arm files are in `data/v14_parts/yn2b_ab/`.
- `modal_od._data_ignore` skips sub-folders of `v14_parts/`. For a Modal run, the V14_KEEP commit in the 2B worktree
  must copy them to `v14_parts/<name>` or allow the folder.
- On the L4, copy the folder as it is.

**Config patch.**
- `yn2b_ab_<arm>_counts.json` holds `config_patch`: `train_file`, `rel_file`, `epochs`, `expect_kd_targets` and
  `expect_kd_full`.
- `runs/*.json` is never edited here.

## 1 Oct gates run (builder E): new flags and where the files are

Write rules of this run: top-level `data/` takes only `yn2b_dev_iid.jsonl`, `yn2b_dev_holdout.jsonl` and
`yn2b_devx.jsonl` (owner decision on wave-1a issue 6). The assembled train file, its relations and the dev relations
live in `data/v14_parts/yn2b_ab/`. SPEC 8's `logs/yn2b_checks.json` is `yn2b/yn2b_checks.json` here.

| Tool | New flag or behaviour |
|---|---|
| `assemble_yn2b.py` | `--out-dev-iid` / `--out-dev-holdout` (with `--out-dev ''`) split the dev rows by `meta.dev_kind`. `--drop-views key:view` leaves out a whole view with its relations (reported). A yes/no card may carry extra definition lines next to `yes`/`no` (decoder_io prints it whole); only a missing yes or no, or mixed `yes`/`Yes` keys, is refused. |
| `check_yn2b.py` | `--dev` takes a comma list. A yn2b text under 12 words is one whole-text gram only from 4 words up (`row_ghash`): options such as `0`, `5` or `none of these` are not held-out hits. Missing inputs are listed in `inputs_missing`. |
| `gather_names.py` (new) | The SPEC 7.7 name list: pool persons and organisations shown in the rows, the `names_*.json` files, F6 and devx names. A one-word name is checked alone where a row shows it alone, else in its shown two-word form. |
| `build_ab_yn2b.py` | `--kd-file` defaults to the config's `train_file`. `--exclude-ids` (+ `--exclude-groups`) leaves known-bad rows out of every arm after S is chosen (draft A4). Arm C refuses a `--teacher-src` with no teacher in S. |
| `ab_readout.py` | Reads `yn2b_dev_iid` + `yn2b_dev_holdout` when there is no `yn2b_dev`. |
| `write_checks.py` (new) | Writes `yn2b/yn2b_checks.json` and `yn2b/yn2b_summary.json` (SPEC 8 outputs). |

Commands of the 1 Oct run (from `lean/`, `PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python`):
```
yn2b/assemble_yn2b.py --drop data/v14_parts/yn2b_raw/yn2b_drop.json --drop-views gen3_state_track:ladder \
  --out-train v14_parts/yn2b_ab/yn2b_train.jsonl --out-rel v14_parts/yn2b_ab/yn2b_relations.jsonl \
  --out-dev '' --out-dev-iid yn2b_dev_iid.jsonl --out-dev-holdout yn2b_dev_holdout.jsonl \
  --out-dev-rel v14_parts/yn2b_ab/yn2b_dev_relations.jsonl --out-devx yn2b_devx.jsonl
yn2b/check_yn2b.py --train v14_parts/yn2b_ab/yn2b_train.jsonl --dev yn2b_dev_iid.jsonl,yn2b_dev_holdout.jsonl \
  --devx yn2b_devx.jsonl --names yn2b/names_check_1oct.json --report yn2b/check_yn2b_report.json \
  --drop data/v14_parts/yn2b_raw/yn2b_drop.json
yn2b/check_unseen.py --yn2b-file v14_parts/yn2b_ab/yn2b_train
yn2b/build_ab_yn2b.py --arms A,B,C --kd-file v14_parts/train_2b_golden_kd_2view.jsonl --teacher-src q35_4b_E2v \
  --exclude-ids yn2b/label_audit_known_bad_ids.json --exclude-groups gen_numeric_dates_letter_twin_question \
  --gate-exclude yn2b/label_audit_known_bad_ids.json --yn2b v14_parts/yn2b_ab/yn2b_train.jsonl \
  --yn2b-rel v14_parts/yn2b_ab/yn2b_relations.jsonl --overwrite
```
Without F3 in arm B/C (if the owner does not accept the F3 deviation): add `--drop-families gd_gen3_state_track`.
