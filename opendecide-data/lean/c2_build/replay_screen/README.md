# A46 replay-wide label-noise screen

Spec: `PREREG_FINAL.md` Ruling A46 (15 Oct 2026), with the A43 (d) cascade. Scope: every row that can enter the C2 replay
draw (`c_build/replay_sample.py`, spec 5.4) whose gold is an upstream human label, in any answer format. Program-gold and
execution-gold rows are out of scope. Drop only; no row is ever relabelled; a row that only Haiku disputes stays.

**This unified screen covers the T37b hate-speech and table-fact replay sources too. It supersedes any replay-source
task files the T37b agent writes under `c2_build/t37b/`** (A45 b's T37b "replay-source noise screen" is the narrow
version of this one). Do not run both: run this one and give T37b the same `REPLAY_DENY_A46.json`.

Nothing here runs a model. The orchestrator runs the Haiku, Sonnet and Opus reads from the task files and puts the answer
files at the listed paths.

## Files

| file | what |
|---|---|
| `draw.py` | runs `replay_sample.py` (unchanged, in-process) with the C2 seed 20261013 and captures the exact draw; writes only under `pool/` |
| `pool.py` | classifies the gold origin of every eligible source; writes `POOL_MAP.json`, `POOL_MAP.md`, `pool/population.jsonl.gz` |
| `screen.py` | `tasks`, `score`, `adjudicate`, `confirm`, `finalize`, `report`, `coverage` |
| `tests/test_screen.py` | pytest on fabricated fixtures |
| `reads/tasks/*.md`, `reads/TASKS.json`, `reads/answers/` | Haiku blind reads (reader A and B); TASKS.json lists every task file with its answer path |
| `reads/keys/` | opaque-id key and answer-normalisation table: **orchestrator only, readers never see it** |
| `adjudicate/`, `confirm/` | Sonnet first-pass and Opus confirmation tasks (same layout) |
| `REPLAY_DENY_A46.json` | the deny list: confirmed wrong_gold or ambiguous row ids only |
| `REPLAY_UNSCREENED_A46.json` | rows without a complete pair of reads (must be re-read or dropped) |
| `REPORT.json`, `REPORT.md` | per-source read / flagged / Sonnet-called / confirmed / dropped counts for the GO request |

## Run order (from `c2_build/replay_screen`, `PY=/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python`)

```
nice -n 10 $PY -B draw.py --r1 75000 --r2 150000      # the provisional draw (size fallback of A46), ~15-30 min under load
nice -n 10 $PY -B pool.py map                          # POOL_MAP + the screening population
nice -n 10 $PY -B screen.py tasks                      # Haiku task files (both readers)
# orchestrator: run every reads/TASKS.json task with Haiku (answers -> the listed answer_file)
$PY -B screen.py score                                 # flag list -> reads/SCORE.json (re-run the incomplete tasks first)
$PY -B screen.py adjudicate                            # Sonnet tasks: flagged + 30 agreed controls per source
# orchestrator: run adjudicate/TASKS.json with Sonnet
$PY -B screen.py confirm                               # Opus tasks: every Sonnet wrong_gold / ambiguous call
# orchestrator: run confirm/TASKS.json with Opus
$PY -B screen.py finalize                              # REPLAY_DENY_A46.json (+ REPLAY_UNSCREENED_A46.json)
$PY -B screen.py report                                # per-source counts
$PY -B screen.py coverage --rows <final replay shards dir>   # no unscreened human-label row in the final draw
```

## Rules implemented

- **Flag:** both reads disagree with the gold, or one disagrees and the other abstains or is missing. One disagreeing
  read with an agreeing read: the row stays. Two abstains: the row stays (read, no signal).
- **Reads:** two independent blind reads per row. Reader A and B get different seeds, band partitions, chunk splits,
  opaque ids and orders. Files hold at most 50 items (40 for rows of 1,500-5,000 characters, 20 above). No gold, no
  meta, no row id. Answer contract `{qid, answer, confidence}` with `abstain` allowed. Each task lists
  `allowed_read` / `allowed_write` for the file-access audit (`c2_kit.audit`).
- **Cascade:** Sonnet first pass on flagged rows plus 30 seeded agreed controls per source (mixed and shuffled, read
  order seeded). Opus confirms every wrong_gold or ambiguous call (it sees the first-pass call; it may overturn).
  Confirmed = Opus says wrong_gold or ambiguous. Controls the cascade condemns are real finds and are dropped; the
  control call rate per source estimates the Haiku miss rate.
- **Incomplete reads:** a row with a missing or invalid read that is not flagged is "incomplete". `finalize` refuses
  until none is left, or lists them in `REPLAY_UNSCREENED_A46.json` under `--allow-incomplete`. A46: the final draw takes
  no unscreened human-label row. Rows whose text trips the chunker's never-open-path check are in `reads/REFUSED.json`
  (also unscreened).

## How the mixer loads the deny list (no edit to `mix_c2.py` or `replay_sample.py` is needed)

`replay_sample.py` has no row-id input: its only deny-list input is the per-source verdict file. The row-level form the
C2 mixer consumes is the G13 drop list, `{"set", "drop_ids", "note"}` (as `logs/decontam_counts/pool_drops_r1.json`):
`mix_c2.py --decontam-drops <files>` -> `mixer.decontam_drop_ids` reads the key `drop_ids` and drops the **whole relation
unit** of every listed id, then refills from the margin and trims replay to floor(1.5 x new). So pass

```
mix_c2.py ... --decontam-drops c2_build/replay_screen/REPLAY_DENY_A46.json   (pool_drops_r1.json is added automatically)
```

and, if the unscreened list is not empty, `c2_build/replay_screen/REPLAY_UNSCREENED_A46.json` the same way. These two files
are NOT accepted by `c2_select.py --exclude-ids`, and neither is `pool_drops_r1.json`: that option has always required
`complete` true (and `incomplete_why` empty) of every file that is not a C2 G13 log, and these three lists hold no `complete`
key, so it refuses them ("G13 log is not complete"). An earlier version of this note said they "also fit" `--exclude-ids`;
that was wrong, and no exemption was kept for them (opening that gate takes an owner decision, not a code edit). They are not
G13 logs (their `tool` is not `c2_build/g13_c2.py`, they carry no g13_c2 record and they are not named `c2_*.json`), so
`mix_c2.py --decontam-drops` reads them as before, without any completeness or staleness check. Only a C2 G13 log is checked
for being guarded and not stale (its recorded candidates / dev-file sha256s must still be the files on disk), by the one
function both tools call (`c2_select.g13_log_problems`). The deny list drops by row id, so it stays valid for any final draw
made from the screened shards; `screen.py coverage` proves the final shards hold no unscreened human-label row.

## Assumptions the orchestrator should know

- The provisional draw is `replay_sample.py --dry-run --r1 75000 --r2 150000 --margin 0.10` with `SEED = 20261013`
  (`c2io.SEED`), the sampler's own code path; 75,000 = floor(1.5 x 50,000) (new rows at most 40% of the 125,000 cap).
  If the real C2 draw uses another size, the final draw is a different set; run `coverage` on it and screen the gap.
- Rows in relation units that hold a `pool_drops_r1.json` id leave replay in the mixer, so they are not screened.
- `gd_boardgameqa` is classed program (MANIFEST: "Program-generated defeasible reasoning with exact labels"); the
  sampler's own program list does not include it. Flip it with `pool.PROGRAM_EXTRA` if the owner disagrees.
- `gd_tatqa`, `gd_tathqa` (and `gd_finqa`, dropped by the sampler as VERIFY) have human yes rows and program-built wrong
  answers as no rows; both are screened.
