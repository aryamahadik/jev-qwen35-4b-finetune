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

---
# A45 pre-freeze check (15 Oct 2026, Sonnet 5.5 code agent)

**Verdict: PARTIAL. The output head meets every A45 bar at 5,004 rows; the equivalence head still fails two G6 cells
(see "Failing"). T42 is NOT cleared to enter the freeze until those two are fixed or the orchestrator rules on them.**
No row file written, no `ohs*`/sealed path touched, no Haiku, no commit, no shared kit file edited. Backups: `_backup_a45/`.
Measurement harness: `prefreeze.py` (9 forked workers, each `pilot.build_pilot` on a disjoint seed block, merged through
pipes; numbers-only metrics in `_a45_work/*.json`). Final run = `_a45_work/v5_5000.json` (5,004 rows: 3,754 output + 1,250
equivalence; 0 units failed any program gate, 1 sampler drop of 5,005).

## What changed (generator/template fixes only; nothing relabelled, no bar moved)
1. `gen_pad.py` (new) + `plugin._sample_equiv`: both functions of an equivalence pair get a docstring (a statement, so the pair
   still goes through one `ast.parse -> ast.unparse` round trip) whose size is set by TARGETS drawn from the row key before the label:
   characters, lines, maximum indentation, longest line and number count of each function are hit EXACTLY (window = per-skeleton
   bound of the unshaped pair + slack, `plugin._bounds`). Docstring text = plain lowercase words, numbers of 3-4 digits. Effect on
   formatting-only (equivalence, GBT): +13.5/+18.2 pp -> -2.1 pp; diff-size GBT acc .694 -> .604 (majority .666).
2. Equivalence stratification by the seed counter (sampler S3 only): label = seed % 3, skeleton and card version cycle, so every card
   holds the three labels in equal shares; the diff bin stays hash-drawn. Card id is now `T42:eq:<skeleton>:v<0-3>` (52 cards).
   `DIFFERS` mode "point" (hand-written near-miss strings) 65% -> 30%; the rest are AST mutations (more variety).
3. Output head `_select` (the part that fixed G6/G7): the old gold-conditioned acceptance (overlap class, similarity-rank targets) re-weighted
   subsets and tilted the gold toward / away from option tokens such as '0', '5', '13' (G7 `opt:4 5`, `opt:3`, `opt:12`).
   New rule: the option set is exchangeable (gold = member at the planned length rank, independent of the set), and every option feature
   read AGAINST the shown program is made CONSTANT: no value option shows a token of the visible text (code, rules, wordings, layout) and none is
   a verbatim substring of it. Constants carry no information whichever option is the gold. The similarity-rank target was dropped
   (set-level feature, exchangeable); medoid cue stays at chance (.225 vs .225).
4. Constant ranges widened in 13 templates (multipliers 2-13, list values to 40-60, moduli to 41, thresholds to 70); `mutate.py` untouched
   (HELD_OUT_OPS = swap_args, wrong_slice_bound; T43 imports `mutate.OPERATORS` / `HELD_OUT_OPS` as before).
5. Tests: `test_plugin.py` 16 passed (A==B on 2,000 specs, determinism under PYTHONHASHSEED 1 and 2, held-out configuration, new
   `test_equiv_shape_is_label_blind`), 1,281 s.

## Gate numbers at 5,004 rows (bars unchanged)
| Gate | Result | Bar | Pass |
|---|---|---|---|
| G6 all choice rows (chance .2520) | no failing cell | each view/model <= chance + 2 pp | yes |
| G6 output head (n 3,754, chance .2249) | a .2195/.2311, b .2224/.2311, c .2251/.2272, d .2118/.2346 (LR/GBT); max +1.0 pp | <= +2 pp | yes |
| G6 equivalence head (n 1,250, chance .3333) | a .3288/.3188, b .3192/.3188, **c LR .4096 (+7.6)**, c GBT .3188, **d GBT .4152 (+8.2)**, d LR .3400 | <= +2 pp | **no (2 cells)** |
| G7 (247 tests, whole build) | 0 failing feature | 0 | yes |
| options-only (output / equivalence) | LR -0.25, GBT +0.62 / LR -1.41, GBT -1.45 pp | +/-3 pp | yes |
| formatting-only (output / equivalence) | +1.00, +0.66 / -2.29, -2.13 pp | +/-3 pp | yes |
| diff-size (equivalence, majority .666) | LR acc .666 AUC .517; GBT acc .604 AUC .530; per-metric AUC .46-.53 | acc <= maj+3 pp, AUC .5+/-.05 | yes |
| cues (report) | median-number .235 vs .234; medoid .225 vs .225 | chance | yes |
| program gates G2 G3 G4 G-SL G-LEX G-TW G15 schema options | 0 failed units in 5,005 attempts (G15 off in the parallel harness; on in `test_build.py`) | 0 | yes |
G10, token budget, cards-per-row and the 3% reseed audit: see the `test_build.py` line below (run on the same code at N=2,000).

## Failing (open items, in order)
1. **G6 equivalence (c) LR +7.6 pp and (d) GBT +8.2 pp.** Diagnostics (`eq_meta_single` in `v5_5000.json`: GBT on ONE meta feature, label
   accuracy): mag_mean .370, n_lines .358, depth .353, n_numbers .345, rest <= .333. Reading: (d) is `mag_mean` (mean log10 magnitude of the
   numbers in the state). The docstring numbers are random 3-4 digit values, but their COUNT is `Q_target - core_numbers`, so the mean
   still encodes the core's number count, which differs by label. Fix not finished: draw the docstring numbers so that the SUM of
   magnitudes of f (and g) hits a key-drawn target exactly (`gen_pad.mag_sum`, `goal_cap` are in place; a first attempt failed for ~50% of
   draws because word positions were chosen at random; build the digit tokens into `filler` with the lengths the goal needs). `n_lines` and
   `depth` are the same kind (target windows are label-blind but `depth` mixes skeleton signature and diff bin: stratify the diff bin too).
   (c) is token-level: the pointwise LR crosses option words with every context token, so near-miss strings of the inventory
   (`gen_eq.py`) and the tokens of AST mutants (`>=`, `abs`, `[1:]`) tell DIFFERS from SAME. Planned fix: SAME decoys that carry the same near-miss
   tokens on BOTH sides (only for skeletons with >= 2 points) and more skeletons (17 written, 13 used; 4 excluded as unbalanced).
2. Stratified diff bin was dropped again (infeasible cells fell back to random skeletons); only label x skeleton x card version are stratified.
3. G-LEX Haiku 2/2 admission of the 9 wordings still pending (unchanged). Overlay twins/complements n/a (choice only), as before.

## Commands (from `c2_build/`; python = `../../.venv/bin/python`)
- Pre-freeze measurement (in memory, 5,000 rows, ~12 min + 6 min analysis under load):
  `../../.venv/bin/python -B families/T42/prefreeze.py --n 5000 --workers 9 --out families/T42/_a45_work/v5_5000.json`
- Unit tests (A==B 2,000, determinism, held-out, shape): `T42_N_AB=2000 ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T42/test_plugin.py`
- Serial gate build (G10, tokens, cards, reseed audit): `T42_BUILD_N=2000 ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T42/test_build.py`
  (writes `BUILD_PROBES.json`, numbers only).

## Sealed-run entry point (a sealed agent, after the freeze decision; writes nothing here)
`from families.T42 import plugin as P; plugin, ctx = P.make_plugin(); spec = plugin.sample(seed, "S5")` then
`rr = plugin.render(spec, ctx)` (assemble through the kit `pipeline.build_unit(plugin, spec, ctx)`), for seeds 0..N-1 (about 900 items for
N ~ 1,000 draws; rows dev only). S5 = idiom buckets closure/late-binding and MRO, operators `swap_args` and `wrong_slice_bound` (+ the bucket
operators `late_binding`, `mro_order`), layouts `numbered` and `tabs`, 25% equivalence rows with the held-out operators. Every held-out value is
unreachable from S1-S4 (`test_plugin.py::test_held_out_*`: training samplers never draw the buckets, operators or layouts). The equivalence docstring
shaping and the output-head selection rule above apply unchanged to S5 (hash-drawn label/skeleton there).

## `test_build.py` on the final code (N = 2,000 serial rows, G15 on): 6 passed in 1,610 s
Program gates 0 failed units; G10 pass; mean prompt 472 tokens, max 802 (bars 800 mean / 2,000 max); 286 cards, max 26 rows; equivalence share 24.95%;
3% reseed audit: 72 rows, 0 label flips. NOTE: at 2,000 rows (500 equivalence rows) the two failing equivalence cells of the 5,004-row run are
inside the noise of their tests (SD about 2 pp); the 5,004-row result binds (A45 d), so the verdict stays PARTIAL.


---
# A45 pre-freeze check, round 2 (15 Oct 2026, Sonnet 5.5 code agent; A46 fixes): equivalence head closed

**Verdict: PASS at the largest measurement (10,008 rows).** Every G6 cell of both heads is within chance + 2 pp, G7 passes (whole build, output head,
equivalence head), probes at chance. One cell of the 6,020-row prefix is +2.02 pp (equiv, view c, LR .3535, chance .3333; bar .3533), 0.02 pp over;
it disappears in the superset (.3337 at 2,496 equivalence rows), i.e. it is sampling noise (SD of this cell about 1.2 pp), not a leak that grows
with data. Per A45 d the largest measurement binds. Backups: `_backup_w4/`. Nothing written but numbers (no row file, no `ohs*`/sealed path, no
Haiku, no commit, no kit file edited). Measured on od-l4b (CPU, 6 workers, `prefreeze.py --n 10000 --also-frac 0.6`, 2,322 s build); log
`zed_orch/logs/gcp_t42_pf10k.log` (the `--out` JSON failed to write because the VM lost the folder, the printed brief lines are the record).

## Cause found and fixed (generator only; no relabel, no bar moved, execution-gold rules untouched)
1. **Skeleton / bin fallback leaked the label (n_lines, depth, n_numbers, skeleton tokens).** The diff-bin target was hash-drawn, but bin 3 is
   unreachable for several skeletons and bin 0 for SAME in others (measured: `_a45_work/bins.py`), so after 70 failed attempts the loop jumped to a
   random skeleton: label x skeleton x bin cells filled unevenly (in a 39-spec probe 8 of 39 rows used the fallback; first_last got 1 of 3 labels).
   Now: `plugin._dbin_support(skeleton, ops)` = the bins every label reaches (>= 15% of 300 unexecuted candidates per label, deterministic); the target
   bin is drawn from that list; the skeleton is fixed for ALL attempts (S3: seed counter; S5: key hash); no fallback. 39/39 specs, attempts 0-26.
   `depth` is now a key draw (it used to be derived from the realised bin and signature).
2. **mag_mean (single-feature GBT .370) came from the count of docstring numbers hiding the core's number count.** `gen_pad.add_doc` now hits, per
   function, the number COUNT (exact) and the magnitude SUM (within 0.02) of key-drawn targets: one 4-digit number (>= 1000) plus digit strings of
   the width of filler words (zero padded where the target needs a small value); so mag_mean, mag_max and n_numbers carry no label.
3. **Token-level cue (c LR +7.6 pp): near-miss and mutant tokens.** Implemented the plan in its strongest form: `plugin._vocab(skeleton, ops)` = every
   alphanumeric token any variant can show (all A forms, all typical / edge near-misses, every mutation operator of the sampler's operator set at
   every site of sampled programs). Each function's docstring now carries the vocabulary words its code lacks (placed whole, split randomly over f
   and g), so the token set of a pair is the skeleton constant whatever the label (SAME decoys carry the near-miss tokens, in the docstring; a DIFFERS row
   cannot add a new one). Tests assert core tokens <= vocabulary and vocabulary <= final tokens. Bounds (`_bounds`) include the vocabulary room.
4. **Timeout rule (A46 g).** `exec_child.py`: a wall-clock alarm (snippet 1.5 s, equivalence call 0.25 s) used to be an OUTCOME (`s="timeout"`, `("t",)`;
   a timeout on one side only counted as a difference, i.e. could become a DIFFERS label or witness). Now it raises `EnvError`, the child exits 97, and
   `executor._spawn` repeats (`TIMEOUT_RETRIES = 2`) then raises `ExecTimeout(ExecError)`; callers already drop the attempt on `ExecError`. Deterministic
   step caps stay outcomes. A late alarm after the timer was cancelled is ignored (`_ARMED` flag; found by a flaky test). `T42_INNER_TIMEOUT` is the test
   knob. New test `test_wall_clock_timeouts_only_cause_drops` (1 microsecond inner timeout: snippet job, an equal pair and a really different pair all
   raise `ExecTimeout`, `timeout_drops` rises by 3, no label; then the same jobs run clean): 16/16 passes in a loop on the Mac.

## Gate numbers (od-l4b, in memory, training samplers S1-S4; chance = mean 1/k)
| Gate | 6,020 rows (prefix) | 10,008 rows (binds) | Bar |
|---|---|---|---|
| G6 all choice rows (chance .2521 / .2522) | no failing cell | no failing cell | <= chance + 2 pp |
| G6 output head (n 4,518 / 7,512; chance .2251 / .2252) | a .2105/.2203, b .2231/.2203, c .2127/.2218, d .2200/.2207 (LR/GBT) | a .2218/.2184, b .2235/.2184, c .2218/.2186, d .2222/.2174 | +2 pp |
| G6 equivalence head (n 1,502 / 2,496; chance .3333) | a .3236/.3339, b .3342/.3339, **c LR .3535 (+2.02)**, c GBT .3339, d .3256/.3356 | a .3357/.3341, b .3341/.3341, c .3337/.3341, d .3377/.3281 (max +0.4 pp) | +2 pp |
| G7 (whole / output / equivalence) | pass / pass / pass | pass / pass / pass | 0 failing |
| options-only (output; equivalence) | LR -0.20 GBT -0.48; LR +0.09 GBT +0.06 | LR -0.17 GBT -0.68; LR +0.08 GBT +0.08 | +/-3 pp |
| formatting-only (output; equivalence) | +1.50 / +0.77; -1.78 / -1.38 | -0.60 / +0.05; +0.68 / -1.80 | +/-3 pp |
| diff-size (equivalence; majority .6678 / .6675) | LR acc .6678 AUC .520; GBT acc .6152 AUC .512 | LR .6675 / .530; GBT .6146 / .504 | acc <= maj + 3 pp, AUC <= .55 |
| cues (report) | median-number .2426 vs .2333; medoid .2251 vs .2251 | .2364 vs .2328; .2242 vs .2252 | chance |
| equivalence single-feature GBT (label acc., chance .333) | n_lines .3555, len_state .3442, mag_max .3415, mag_mean .3182 | n_lines .3389, mag_max .3401, mag_mean .3429, n_numbers .3225 | report |
Program gates (G2 G3 G4 G-SL G-LEX G-TW schema options; G15 off in the parallel harness): 10,014 attempts, 6 dropped (3 render, 3 sample), 0 failed program gate.
The 6,020 -> 10,008 trend of every equivalence cell is toward chance (c LR +2.0 -> +0.04 pp; d GBT +0.2 -> -0.5 pp): nothing grows with data.
The earlier single-feature `mag_mean` .370 is now .318-.343 (inside noise); the 4-pp spread of single features at 1,500 rows is the CV noise.

## Tests (od-l4b, CPU venv 3.12.14): `test_plugin.py` 17 passed, 1 environment-only failure
`test_plugin.py` 18 tests, 1,981 s: A == B on 2,000 specs (400 per sampler), determinism under PYTHONHASHSEED 1 and 2, held-out configuration
(HELD_OUT_SAMPLERS / buckets / operators / layouts unreachable from training samplers), gold, one printer, label-blind shape, new vocabulary / numbers /
depth test and the new timeout test all PASS. The only failure is the last line of `test_hermetic_executor` (`python_exe()` must end with `.venv/bin/python`:
the VM has no Mac venv, `executor.python_exe` falls back to the 3.12 `sys.executable`); on the Mac that assertion is unchanged and the test body before
it passed on the VM. The Mac was too busy (load 40) to run the suite there. `test_build.py`: see the last section.

## Commands
- VM: `BG=1 JOB=t42_pf10k zed_orch/gcp_run.sh od-l4b 'mkdir -p families/T42/_a46_work && $PY families/T42/prefreeze.py --n 10000 --workers 6 --also-frac 0.6 --out families/T42/_a46_work/v6_10000.json'`
  (prints the brief of the 6,000 prefix and of the full build; create the out folder AFTER the sync or drop `--out`).
- Equivalence-only quick check (S3 only, ~1,400 rows, `eqcheck.py`) exists but the Mac was too loaded to finish it; use the VM.

## `test_build.py` at the A42-D 1.1 training size (1,467 rows = 1.1 x 1,333), od-l4b, G15 off (`T42_G15=0`; new env switch, default still on)
5 passed, 1 failed in 904 s. Program gates 0 failed units (1 sampler drop of 1,468); G10 pass; equivalence share 24.95%; tokens mean 363 / max 894
(approximate count: no tokenizer on the VM; bars 800 mean / 2,000 max); cards 274, **max 20 rows per card** (bar 64); **3% reseed audit: 51 rows, 0 flips**
(bar 1%). The failing test is `test_probes`: at this size the equivalence head has only 366 rows and one probe GBT sits at -4.1 pp (BELOW chance,
two-sided bar +/-3 pp; SD at n = 366 is about 2.5 pp); the same probes at 2,496 rows (10,008 build) are -1.80 / +0.68 and the output head -0.6 / +0.05, so it
is small-sample noise; the A45 bar is the >= 5,000-row measurement. An earlier 2,000-row serial run on the VM with G15 on produced 0 rows (7,995 render
exceptions): G15 does not run on the VM (it needs files the GCP sync excludes). On the Mac G15 is fine: 80 units with G15 on (20 equivalence rows), 0 dropped.
G15 at scale on the new equivalence text was therefore only checked on those 80 units; `run_pilot_i1.py` (Mac, quiet) runs it for the real pilot.

## Open items
1. The 6,020-row prefix has one equivalence cell 0.02 pp above the bar (see verdict); if the orchestrator wants a second independent 6,000-row read,
   run `prefreeze.py --n 6000` on another seed base (needs a `seed0` argument; `build(n, workers, seed0=...)` already has it).
2. A44/A46 timeout rule is in `exec_child.py` / `executor.py`; the callers drop the attempt on `ExecError` (an `ExecTimeout` is an `ExecError`).
3. Not done / unchanged: G-LEX Haiku 2/2 admission, overlay n/a, `test_hermetic_executor`'s `.venv/bin/python` assertion is Mac-only.
4. Housekeeping: I read two harness task-output files under `/private/tmp/claude-501/...` while polling a background job (they held only `gcp_run.sh`
   status text); not used afterwards. Nothing else touched a forbidden path.
