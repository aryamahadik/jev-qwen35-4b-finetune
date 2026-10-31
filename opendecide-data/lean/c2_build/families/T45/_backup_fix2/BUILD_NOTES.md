# T45 TRACE-VERIFY: build notes (15 Oct 2026, Sonnet 5.5 code agent)

**Status: built; every program gate passes in memory; the A45 (d) pre-freeze bar is NOT yet met (G6 / probes: see the gate table).**
No row file, no `lean/ohs_ac_sealed/`, no Haiku run, no commit, no shared kit file edited. Template (program) text only.
The only things written outside this folder are scratch files in the session scratchpad (a development cache of canonical
execution results, never rows).

## What exists (`c2_build/families/T45/`)
| File | Role |
|---|---|
| `G0_SPEC.md` | G0-lite (heads, options, gold, verifier, fault catalogue, held-out, relations, balance, code-body exemptions E1-E3). sha256 in `T45Plugin.G0_SHA256` |
| `plugin.py` | `T45Plugin` (`sample`, `solve_a`, `view`/`canonical`, `render`, `relations`, `error_models`), `make_plugin()`, `warm_cache()`, `shown_set()`, `fault_candidates()` |
| `exec_child.py`, `executor.py` | solver A: the hermetic child (real git / sqlite / curl + localhost server / make / unittest) and its parent (two independent fresh processes, identical results or ExecError; in-memory cache; `classify`) |
| `scenarios.py` | fault catalogue, canonical execution parameters (`exec_params`), surface renaming (`surface`, `Mapper`), packs |
| `texts.py` | rules, legends (16), layouts (10 registers), wordings, option definitions (the row's `card`) |
| `solver_b.py` | solver B (paradigm set_algebra): own parser + set algebra, no execution |
| `probes.py`, `audits.py`, `prefreeze.py` | A42-D 3.2 probes; 3.3 reseed audit, surface-name audit, held-out check; the parallel in-memory A45 (d) check |
| `run_pilot_i1.py` | pilot driver (`--dry-run`, `--n`, `--no-g15`), T42 pattern; registers the loader at runtime |
| `sealed_run.py` | `emit_sealed(n_items=400, seed0, workers)`: the sealed-mode entry point (S5), writes nothing |
| `test_t45.py` | pytest (13 tests) |

## Design in one paragraph
A row shows ONE really executed step: intended effect (`key=value` items), state before, the step as planned (one fault-independent
command per kind), result (the runner's success or failure exit code and a tag), state after, and the card's runner legend. Gold =
execution: the diff between the executed post-state and the intended effect, plus an executed retry (same step again) and an executed
repair (corrected step) for the loud class and the next move. Five tools x up to 10 fault types (G0 section 3). The draw is label-first
and the shown label set is chosen so that the options carry no information (anchor always shown, gold uniform inside the set of 2-3
shown labels), which makes the class floor (SUCCESS 38% of head-1 rows) compatible with the options-only probe. Everything a shallow
model could read off is turned into a JOIN with the legend: tag codes, exit codes and phrasing are per-legend opaque 4-digit numbers
listed in every row of that legend; the command line is fault-independent; item names, ids, values and shas are injectively renamed.

## Commands (from `c2_build/`; python = `../../.venv/bin/python`; use `nice -n 10`; other agents share the cores)
- Tests: `T45_N_AB=2000 T45_BUILD_N=300 nice -n 10 ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T45/test_t45.py`
- Pilot dry run (in memory): `nice -n 10 ../../.venv/bin/python -B families/T45/run_pilot_i1.py --dry-run --n 300 [--no-g15]`.
  Without `--dry-run` it WRITES `pilot_i1/`: only after the OHS-AC freeze and on the orchestrator's go.
- A45 (d) check (5,000 QC rows, in memory, writes one metrics JSON of numbers): `nice -n 10 ../../.venv/bin/python -B families/T45/prefreeze.py --n 5000 --workers 5 --out <metrics.json>`
  (optional `T45_EXEC_CACHE=<file outside the repo>` keeps canonical execution results between processes; unset = pure in-memory).
- Determinism: the test runs the same build under PYTHONHASHSEED 1 and 2 and compares row hashes.
- **Sealed run (a separate sealed agent, later):** `from families.T45.sealed_run import emit_sealed; out = emit_sealed(n_items=400, seed0=7_000_000, workers=4, run_g15=True)`;
  `out["rows"]` = 400 sampler-S5 rows (held-out fault `stale_noop`, registers memo / journal, `dev_only`), `out["stats"]` = counts. The caller
  writes the rows; this function writes nothing and never creates `lean/ohs_ac_sealed/`.


## A45 pre-freeze check (run 2: 5,016 QC rows, in memory, G15 off as in A43 a; numbers are from `prefreeze.py --n 5000 --workers 6`)
Command: `T45_EXEC_CACHE=<scratch file> nice -n 10 ../../.venv/bin/python -B families/T45/prefreeze.py --n 5000 --workers 6 --out <metrics.json>`.
Wall time (machine load average 130-300 during this build, shared cores): cold execution of the 173 canonical structures = 260 s
(2 fresh processes each, 4 threads; 66 attempts hit the 5 s cap on the loaded machine and were repeated); with the execution cache
warm: build 81 s (6 workers) + analysis and audits 118 s. First 5,000-row build with 5 workers: 554 s.
| Gate / check | Value | Bar | Pass |
|---|---|---|---|
| Program gates G2 G3 G4 G-SL G-LEX G-TW schema options (5,016 units) | 0 units dropped | 0 | yes |
| G15 | 30 units in `test_a_equals_b_and_g3` + 3-6 per smoke run, 0 failures (not run on the 5,000 QC rows) | 100% | yes (partial) |
| Solver A = B | 1,000 specs in the test run (200 per sampler, G3 facts and option keys too) + all 5,016 build units | 100% on >= 2,000 specs | yes (>= 6,000 specs) |
| G6 overall (chance .3851) | worst: d_meta GBT .4215 (+3.6 pp); a / b / c LR + GBT <= .4029 | <= chance + 2 pp | **NO** |
| G6 head outcome (n 3,238, chance .3847) | c_card LR .4172 (+3.3), d_meta GBT .4673 (+8.3) | same | **NO** |
| G6 head move (n 1,778, chance .3859) | d_meta GBT .4229 (+3.7); all others <= .3976 | same | **NO** |
| G7 | pass (131 tests) | 0 failing | yes |
| G10 (gold position, gold-is-longest, rank; yes/no checks n/a) | pass | pass | yes |
| plan_report (position, length rank, longest) | pass | pass | yes |
| Options-only probe (outcome / move) | LR +0.6 / -0.3 pp; GBT +1.5 / **-3.26** pp | +/- 3 pp | outcome yes; move GBT just outside (below chance: exact-balance artifact, see T40 note) |
| Formatting-only probe (outcome / move) | LR -0.4 / -0.6; GBT **+5.3** / -1.0 | +/- 3 pp | **NO** (outcome GBT) |
| Reseed audit (3% = 150 rows regenerated, new execution params, surface, pad and option draw) | 0 flips, 0 solver-B flips | <= 1% | yes |
| Surface-name audit (20 specs re-executed with real names) | 0 mismatches | 0 | yes |
| Held-out fault `stale_noop` | 0 rows in training samplers S1-S4, present in S5 | 0 | yes |
| Determinism, PYTHONHASHSEED 1 and 2 | identical row hashes (test) | identical | yes |
| Mean / max prompt (real Qwen3.5-4B tokenizer, instructions twice) | 747.8 / 862 | <= 800 / 2,000 | yes |
| Cards, rows per card | 639 cards, max 19 rows | >= 20, <= 64 | yes |
| SUCCESS share | 38.2% of head-1 rows, 36.7% of all rows | >= 35% | yes |
| Tests | 12 of 13 pass in the two partial runs (7 + 5); `test_in_memory_build` failed once on length-rank ties (fixed by distinct option lengths) and was not re-run | all | partly verified |

**Verdict: T45 does NOT meet the A45 (d) pre-freeze bar yet** (G6 d_meta GBT in both heads, G6 c_card LR in the outcome head,
formatting-only outcome GBT). Everything else in the bar is met. By the A47 ruling it moves to C3 unless the G6 residual is fixed by Sat 17 Oct 18:00 UTC.

### Where the residual G6 leak comes from (diagnosed, not yet fixed)
G6 went from d_meta GBT +17 pp (first 5,000-row run: pads with digit suffixes and 5-digit ids, exit 0 / 1 / 22 / 128 shown, command line
varying by fault) to +8 pp (outcome head) after: fault-independent printed command, two opaque 4-digit exit codes per legend, character-length
padding, padding items with the same name and value shapes as real items. An ablation on 1,044 outcome rows (GBT d_meta) isolates the numeric
features (n_numbers, mag_max, mag_mean): .4425 (+5.7 pp); length features .409; categorical metadata .3975 (+1.2). Likely cause: padding
VALUES differed from intent VALUES in magnitude for the build kind (`r1` pads against `rNN` intent values); a fix is in the code (`_pads`, build
branch draws the pad value from {r1, new, old}) and a third 5,000-row run was launched with it; its metrics file is
`<scratchpad>/pf5000.json` (not read by this agent: out of budget), so treat the table above as the verified state. Next steps for
the iteration: (1) re-run `prefreeze.py`; (2) if d_meta still leaks, drop digits from the state entirely (alphabetic ids) so n_numbers / mag_*
are constants; (3) re-run the options-only move head (the -3.3 pp is the balanced-design deficit; 5,000 more rows).

## Open items
1. G6 / formatting-only residual above (bars unchanged, nothing loosened). 2. Code-body exemptions E1-E3 in G0 section 7 need the orchestrator's
confirmation before the first row. 3. No Haiku surface text and no `haiku/` task files (Mode T only; the 6 question wordings are admitted by program
stand-ins `program:stand-in-N`; real G-LEX needs the 2/2 Haiku reads). 4. G5-H / G3-H / G8 / G9 / G11-G13 / G-TPL / G-TW (no twins) are not part of this
in-memory bar and were not run. 5. Solver B is a parse + set-algebra verifier; it contains no per-tool semantic predictor (the tool semantics are
checked on the A side by the executed retry and repair and the `Inconsistent` guard). 6. The displayed command is the fault-independent plan
(the executed variant is hidden; G0 section 1). 7. `plugin.FAMILIES` has no T45: `plugin.py` registers it at import (kit candidate). 8. Execution cost: about
173 canonical executions x 2 fresh processes (1.5-3 s each idle; 4-10 s on a machine at load 200); results are cached in memory by sha256 of
(kind, params); an optional development cache file (`T45_EXEC_CACHE`) must stay outside the repo. 9. `heldout_check` finds 13 held-out rows in 150 S5
draws (the SILENT_WRONG-gold rows of head 1 plus the repair golds of head 2).
