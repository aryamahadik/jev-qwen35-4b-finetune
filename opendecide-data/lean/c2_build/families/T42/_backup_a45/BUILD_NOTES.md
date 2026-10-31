# T42 CODE-EXEC: build notes (14 Oct 2026)

**Status: built and gate-tested in memory; NOT pilot-ready.** All program gates pass on a 3,000-row build; G6, G7 and three probes
still fail (numbers below). No row file, no sealed folder, no Haiku run, no commit, no shared kit file edited.

## What exists (`c2_build/families/T42/`)
| File | Role |
|---|---|
| `G0_SPEC.md` | G0-lite v1.0 (97 lines, frozen: sha in `plugin.T42Plugin.G0_SHA256`) |
| `plugin.py` | sampling (S1-S5), solver A (execution), render, G4 relations, error models; `make_plugin()` -> (plugin, ctx) |
| `executor.py`, `exec_child.py` | hermetic runner: venv CPython 3.12, `PYTHONHASHSEED=0`, fresh subprocess `-S -s -B -P`, 5 s cap, temp cwd, audit hook (no sockets / subprocess / writes), RLIMIT_FSIZE 0, two runs must agree; equivalence grids + 10K fuzz + branch coverage by `sys.settrace` opcode events |
| `gen_out.py`, `mutate.py`, `gen_eq.py` | typed templates (11 training idioms + closure, MRO), 15 AST mutation operators, 17 function-pair skeletons (13 used) |
| `solver_b.py` | independent parser + tree-walking interpreter (closures, defaults, classes with C3 / `super()`, try/finally, comprehension scope) + grid enumeration for equivalence |
| `probes.py` | options-only, formatting-only, diff-size, median-number and medoid probes |
| `run_pilot_i1.py` | pilot driver (`--dry-run`, `--n`, `--no-g15`); registers the loader at runtime |
| `test_plugin.py`, `test_build.py` | pytest (15 + 6 tests); `BUILD_PROBES.json` = metrics of the last build (numbers only) |

Design points that differ from a plain "gold + mutants" family (each was forced by a probe):
- **Star options.** The generator makes a HUB program and its mutants; the shown program is the member at the planned length rank, so
  it is the hub only 1 time in k. Before this, the gold was always the centre: token, number-prior and "most similar option" cues
  gave +8 to +23 pp (medoid probe 0.46 vs 0.23 chance; now 0.222 vs 0.226).
- Options of a row share one shape and one overlap class (negatives, floats and None were distractor-only before); exceptions only in
  exception rows (one class per row, m <= 1 exception option, value texts shorter than `raises X`).
- Equivalence: both functions through `ast.unparse`; token-diff bin drawn from the row key before the label is built.

## Test results (final code)
- `test_plugin.py`: **15 passed** (3:58): contract (only the yes/no complement overlay requirement is open: choice-only family), hermetic
  executor (socket / write / subprocess refused, loop capped, hash seed 0), **A == B on 2,000 specs** (400 per sampler), solver-B bug
  caught, equivalence gold (witness really differs; SAME has 10K fuzz, clean grid, coverage >= 95%), one printer, label-blind diff bins,
  every distractor re-executed twice, plan balance, exception balance, held-out configuration, token budget, **determinism under
  PYTHONHASHSEED 1 and 2**.
- `test_build.py` (3,000 rows through `pilot.build_pilot`, 8 min): **passed** program gates (G2 G3 G4 G-SL G-LEX G-TW G15 schema options:
  0 failed units, 0 dropped units), shares / tokens / cards (25.0% equivalence; mean 501, max 920 real tokens; 410 cards, max 35 rows),
  **reseed audit** (91 rows, another PYTHONHASHSEED and fuzz seed: 0 flips); G10 passes. **Failed:** G6, G7, probes.

## Measured on the last 3,000-row build (`BUILD_PROBES.json`)
| Probe / gate | Result | Bar |
|---|---|---|
| G6 choice (chance 0.2526), best views | a: LR .264 GBT .259 (pass); b options: LR .278 (+2.5, fail) GBT .259; c card-without-question: LR .310 (+5.8) GBT .287 (+3.5); d meta: LR .281 GBT .292 (+3.9) | <= chance + 2 pp |
| G7 | 1 failing feature of 374: `opt:4 5` (gold 87 of 149 rows, expected 62) | 0 |
| options-only, output head (n 2,250, chance .2257) | LR +3.7 pp (fail), GBT +0.6 | +/- 3 pp |
| options-only, equivalence (n 750) | LR -1.2, GBT -1.2 (pass) | +/- 3 pp |
| formatting-only, output head | LR -0.1, GBT +1.9 (pass) | +/- 3 pp |
| formatting-only, equivalence | LR -0.9 (pass), **GBT +14.7 (fail)** | +/- 3 pp |
| diff size: per-metric AUC SAME vs DIFFERS | 0.46-0.50 for token / line / char diff, hunks, gaps (pass) | 0.5 +/- 0.05 |
| diff size: model on all size features | LR acc .636 AUC .549 (pass); **GBT acc .728 AUC .766 (fail)**; majority .645 | acc <= majority + 3 pp, AUC <= .55 |
| median-number / medoid cues | .244 vs .242 / .222 vs .226 (chance) | report |

Reading: the equivalence failures are memorisation of the skeleton's variant strings (absolute lengths identify which typical / edge
near-miss was used; they vanish when cards of one skeleton share a CV fold, and come back when a skeleton is split over folds). The fix is a
larger variant inventory (more skeletons, more A forms, constants and names per skeleton), not a gate change. The output-head residual
(+2.5 to +5.8 pp, LR on tokens) is content priors of the template constants (numbers such as 4 5 / 13 / 14); wider constant ranges
removed the biggest, not all.

## Open items
1. **G6 / G7 / probes** above (bars unchanged, nothing loosened). Next: widen constants and add templates; add skeletons / variants; re-run
   `test_build.py`; then `run_pilot_i1.py`.
2. Overlay: no twins / equiv-format partners / complements / attacks (no input slots; choice rows only). `pilot.overlay` twin_share and
   equiv_share fail by construction; yes/no checks of G10 and the overlay are marked "n/a" by `run_pilot_i1.py` (kit candidate: a
   CHOICE_ONLY flag in `pilot.g10` / `pilot.overlay`; `plugin.FAMILIES` needs T40-T42, registered at runtime here).
3. G-LEX: the 9 question wordings are admitted by program stand-ins (`program:stand-in-N`); the Haiku 2/2 admission is still to run. No Haiku
   authoring files were written: surface text is rules + wordings + layouts only (docstring / comment realism would be a Haiku task).
4. Sampling failures: 0 of 3,000 in the build; about 0.1% of seeds in S5 (held-out buckets) find no structure within 320 attempts.
5. The `sys.settrace` opcode events need one warm-up pass on CPython 3.12.10 (first traced run of a code object emits none); handled in
   `exec_child.coverage` (two passes, the second measured).
6. Equivalence cost: about 0.5 s per SAME pair (10K fuzz, two runs); about 1 s per unit overall (3,000 rows in 8 min).

## Commands (from `c2_build/`; python = `../../.venv/bin/python`)
- Tests: `T42_N_AB=2000 ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T42/test_plugin.py`
  and `T42_BUILD_N=3000 ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T42/test_build.py` (writes `BUILD_PROBES.json`).
- Pilot dry run (in memory): `../../.venv/bin/python -B families/T42/run_pilot_i1.py --dry-run --n 300` (add `--no-g15` to skip G15).
  Real pilot (needs A38, writes `pilot_i1/`): `../../.venv/bin/python -B families/T42/run_pilot_i1.py`.
- Sealed run (a separate sealed agent, later): `plugin.sample(seed, "S5")` for the held-out sampler (closure / MRO buckets, operators
  `swap_args` and `wrong_slice_bound`, layouts `numbered` and `tabs`; equivalence rows 25%), rendered with `make_plugin()`; ~900 items.
