# T44 SEQ-CHECK: build notes (15 Oct 2026)

Workflow routing over a random tool algebra (typed predicates, negative preconditions, add / remove effects). Two heads, both choice:
head 1 plan verdict (INVALID / STEP_k_NOT_APPLICABLE / GOAL_NOT_REACHED / VALID), head 2 next call (1 of 4, must start a shortest
sequence to the goal). Program gold only. Semantics, samplers, held-out configuration, error models, relations: `G0_SPEC.md`
(50 lines, sha in `T44Plugin.G0_SHA256`). **Status: A45 (d) pre-freeze bar met in memory; no row file, no sealed folder, no Haiku run, no commit,
no shared file edited.** Surface text is template (program) text only.

## Files (`c2_build/families/T44/`)
| File | Role |
|---|---|
| `G0_SPEC.md` | G0-lite |
| `plugin.py` | sampler (label-first, key-fixed display parameters), solver A glue, render, G4 relations, error models, `make_plugin()` |
| `world.py` | domains (4 dev tool libraries + 3 fictional vocabularies; held out: registry, observatory, bakery), algebra generators, forward executor (`verdict`), layered BFS with first-move sets (`explore`) |
| `solver_b.py` | independent parser of every layout + BACKWARD REGRESSION (weakest preconditions); imports only `texts.py` |
| `texts.py` | rules, wordings, 9 tool-block layouts (7 training, held out: hoare, colon) shared by renderer and parser |
| `probes.py`, `t44_prefreeze.py` | options-only / formatting-only probes; the in-memory A45 driver (writes only numbers) |
| `run_pilot_i1.py` | `--dry-run`, `--n`, `--no-g15`; registers the loader at runtime |
| `test_t44.py` | 14 pytest tests (about 80 s) |
| `A45_CHECK_6000.json` | numbers of the last 6,000-row in-memory build |
| `haiku/` | NOT written: template text is enough; an optional realism step would be Haiku-written one-line tool descriptions (needs a G3-H fact lock); not run |

## A45 pre-freeze check (6,000 rows in memory, final code, `A45_CHECK_6000.json`)
| Gate | Result | Bar |
|---|---|---|
| G0-lite | 50 lines, sha frozen in plugin | exists |
| HELD_OUT_SAMPLERS | S5: held-out domains (all tool / predicate / type / object names disjoint from training, tested), plan lengths 7-8 (head 2: prefix + d, d <= 5), layouts hoare / colon; S1-S4 never reach them (tested on 2,000 rendered rows) | implements A42-D 13.1 |
| Solver A == B | 2,000 sampled specs (400 per sampler, render + parse + G3 facts + every option read back) and 3,000 random plans with garbage steps and negative goals (forward simulation vs regression): 0 mismatches; injected bug caught | >= 2,000 |
| Program gates G2 G3 G4 G-SL G-LEX G-TW schema options | 0 failed units of 6,057 attempts; G15: 0 of 500 rows (slice); 57 sampler failures (0.9%; S4 3.2%) counted as drops | 0 |
| G6, 6,000 rows (pooled; per head: verdict 3,029, next 2,971) | pooled views <= .2597; verdict head <= .2664; next head <= .2649 (chance .25) | <= chance + 2 pp |
| G7 | 510 tests, 0 failing | 0 |
| G10 | pass (yes/no checks n/a: choice only) | pass |
| Options-only probe (chance = majority share of the eval split) | verdict LR -0.3 / GBT -1.6 pp; next LR +0.7 / GBT +1.5 pp | +/- 3 pp |
| Formatting-only probe | verdict LR -0.5 / GBT +1.1 pp; next LR -0.6 / GBT +2.4 pp | +/- 3 pp |
| Reseed audit (3% = 170 rows re-drawn from an independent stream, same cell) | 0 verdict label flips; 0 A != B on the redrawn rows; 0 B != original gold | <= 1% |
| Determinism | rows_sha256 identical under PYTHONHASHSEED 1 and 2 (run_pilot_i1 and the pytest row hash) | equal |
| Tokens | mean 715, max 884 real Qwen3.5 tokens (instructions twice) | mean <= 800, max <= 2,000 |
| Cards | 280 cards (domain x algebra index), 10-33 rows per card | <= 64, >= 20 |
| Algebras | 280 distinct ids, 3,198 distinct tool lists in 6,000 rows | >= 150 |
| Balance | verdict labels 25.0% each; STEP printed k independent of the label; gold position and (length, text) rank uniform; heads 50.5 / 49.5% | G0 |
| Diff-size probe | n/a (not a coding family) | |

`pilot.overlay` twin_share and equiv_share fail by construction (no input slots, no yes/no; same as T42); G3-H n/a (Mode T only).

## Design facts forced by the probes (each fixed a measured cue)
- Head 2 tool names are shuffled among the algebra's tools per row: entry tools (build_image, lock, freeze) were gold 40-50% of the time they appeared; options-only LR was 0.42 on 2,500 rows before.
- The 4 options share one parameter-type signature (arity and object-type cues), never repeat a printed call (verbatim-in-text cue) and the gold's (length, text) rank is planned. Forbidding length ties made gold the only tie-free option (cue); ties are left free.
- Replacement steps keep the replaced step's arity and are picked tool-first (binary tools have many more ground calls: comma count leaked STEP); goal swaps keep sign and arity; object counts and start-fact count come from the row key (an op that is feasible only for small starts leaked GOAL_NOT_REACHED).
- Printed STEP k is a decoy on non-STEP rows (drawn from the key, same law as the true k).

## Open items
1. Haiku: nothing authored (tool names are template text; optional descriptions). Wordings (8) are admitted by program stand-ins (`program:stand-in-N`); the Haiku 2/2 admission is still to run. Spec 3.0 per-wording share (8 wordings, 12.5% each of a family; bar 2% per wording) needs the Haiku pool of >= 50 wordings.
2. G5-H blind reads, G13, G9 crowd, 5% blind re-derivation: orchestrator / Haiku, not run.
3. Dev domains with permuted tool names read as arbitrary verbs (head 2 only); realism trade-off recorded.
4. Sampler failures 0.9% overall (S4 longer totals 3.2%, S2 0.5%): seeds dropped, never relabelled. Per-sampler cell shares were not re-balanced.
5. Speed: about 7 rows/s on a free CPU (6,000 rows in 9-14 min with the gates). Next-head S5 rows are slower (BFS to depth 5).
6. Kit candidates: `CHOICE_ONLY` flag for `pilot.g10` / `pilot.overlay` (T42 has the same runner patch); `plan_report` length rank counts ties as below (use (length, text) order).

## Commands (from `c2_build/`, `PY=../../.venv/bin/python`)
```
$PY -m pytest -q -p no:cacheprovider families/T44/test_t44.py                  # 14 tests, ~80 s (T44_N_AB=2000)
$PY -B families/T44/t44_prefreeze.py 6000 families/T44/A45_CHECK_6000.json     # the A45 numbers above (in memory)
$PY -B families/T44/run_pilot_i1.py --dry-run --n 1000 [--no-g15]              # pilot gates in memory
PYTHONHASHSEED=1 $PY -B families/T44/run_pilot_i1.py --dry-run --n 200 --no-g15   # compare rows_sha256 with PYTHONHASHSEED=2
$PY -B families/T44/run_pilot_i1.py                                            # real pilot, AFTER the OHS-AC freeze: writes pilot_i1/
```
## Sealed-run entry point (a sealed agent, after the A45 freeze is ordered; never run here)
```
from families.T44.plugin import make_plugin
from c2_kit import pipeline
plugin, ctx = make_plugin()                       # ctx.pick(held_out=True) draws the hoare / colon layouts for S5
spec = plugin.sample(seed, "S5")                  # N items: seeds from a sealed range whose start is a multiple of 4
unit = pipeline.build_unit(plugin, spec, ctx)     # render + G2 / G3 / G4 / G-SL / schema; rows are dev_only
```
S5 draws the head 50 / 50 (hash of the seed), 7-8 steps (head 1) or 7-8 calls in total (head 2, d <= 5), the held-out domains registry,
observatory and bakery, and the held-out layouts. Head-1 labels are exact per block of 4 seeds, so ask for a multiple of 4 verdict seeds
per block; ~400 items need ~1.5% extra seeds for sampler failures. The oracle code shared with the sealed mode is `world.verdict` /
`world.explore` (a later fix that changes them means a sealed re-run and drop of changed items).
