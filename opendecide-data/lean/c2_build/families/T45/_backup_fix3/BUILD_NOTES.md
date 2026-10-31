# T45 TRACE-VERIFY: build notes (15 Oct 2026, Sonnet 5.5 code agent)

**Status (fix round, 15 Oct): timeouts can no longer become labels; every program gate passes in memory; G6 passes overall and in the move head; ONE cell still misses the A45 (d) bar: G6 view c (card without question) LR in the outcome head, +3.2 pp (bar +2.0).**
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
| `test_t45.py` | pytest (17 tests: 13 + no wall clock in the child, inner timeouts only drop, labels stable under CPU load, rules block is a program template) |

## Design in one paragraph
A row shows ONE really executed step: intended effect (`key=value` items), state before, the step as planned (one fault-independent
command per kind), result (the runner's success or failure exit code and a tag), state after, and the card's runner legend. Gold =
execution: the diff between the executed post-state and the intended effect, plus an executed retry (same step again) and an executed
repair (corrected step) for the loud class and the next move. Five tools x up to 10 fault types (G0 section 3). The draw is label-first
and the shown label set is chosen so that the options carry no information (anchor always shown, gold uniform inside the set of 2-3
shown labels), which makes the class floor (SUCCESS 38% of head-1 rows) compatible with the options-only probe. Everything a shallow
model could read off is turned into a JOIN with the legend: tag codes and the two exit codes are per-legend opaque 4-LETTER codes (no digit) listed in every row of that legend; the command line is the fault-independent plan; item names, ids, values and shas are injectively renamed (values and shas digit-free); a state line shows the real keys that were there before, one DISGUISED pseudo-word item of the same shape, length and digit count per intent key that is not set, and 1-3 padding items; each rules block carries a constant 5-digit runner build number.

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


## Fix round (orchestrator, 15 Oct): what changed and why
1. **Timeouts are never labels (blocker).** `exec_child.run()` no longer returns `(124, "", "timeout")`: any wall-clock timeout of a tool call, the HTTP/sqlite readbacks, and any exit status no catalogue tool produces (killed, not found; allowed sets: git 0/1/128, curl 0/22, make 0/2, python 0/1/5) raise `EnvError`; the child exits 97, `executor._spawn` repeats the WHOLE spec (the 5 s parent cap included) up to 4 more times and then raises `ExecTimeout` (STATS `timeouts`, `timeout_drops`); `plugin.sample` counts it (`DIAG["timeout_drops"]`) and redraws the same fault with other parameters, so a drop is by structure, never by label. `db_read` no longer turns an OperationalError into an empty state. Audit of the other paths: sqlite `timeout=0.0` is deterministic (the lock is held by the harness in the same child, taken after the before-readback and released before the after-readback); the HTTP server is bound and listening before the thread starts (no start race), the port is ephemeral per spec and printed as 8080; make mtimes are set with explicit `os.utime`; the git "busy" hook and the flaky test use counter / flag files; no `time`, `sleep` or `datetime` in the child (a test greps for it). Tests: `test_inner_timeouts_only_cause_drops` (patched 0.5 ms inner timeout: all 43 catalogue structures raise `ExecTimeout`, `timeout_drops` rises by exactly 43) and `test_labels_stable_under_cpu_load` (reference results from unloaded runs; re-executed with 2 x cores busy loops: each result identical to the reference or dropped as a timeout). In the 6,000-row QC build: 0 timeout drops (3 repeated attempts in the earlier 5,000-row run).
2. **The earlier third run** (padding tweak for the build kind) never wrote its metrics file (the process died with the previous session); its question is superseded by the diagnosis below.
3. **G6 leak diagnosis (ablations, all measured on in-memory rows):** (a) git intents held 1 item for most faults and 2-3 for `swallowed` (tags): intent size predicted the label (fixed: every git intent holds the branch and 1-2 tags); (b) `mag_mean` (mean log10 of all numbers) decoded the shown 4-digit exit and tag codes (+6.3 pp in the move head; fixed: codes are 4-letter, definitions say "reported success / failure"); (c) real ids were the smallest of m + 12 sorted draws (fixed: unsorted, one distribution with padding ids); (d) real and padding items differed in shape and padding adapted to the real items (formatting-only +5 to +8 pp, c-view LR +3 to +5 pp): now a state line shows the real keys, one disguised pseudo-word item of the same kind, character length and digit count per unset intent key, and 1-3 padding items; (e) git tag items carried a tiny version vocabulary (v1..v3, digits 0-8) whose presence followed the number of disguised tags: tags are now `release-<4-digit>`; (f) `mag_max` followed the number of FRESH random numbers (real items repeat the intent's numbers, disguises do not): each rules block states a constant 5-digit runner build number that is larger than any state number. Rejected after measurement: dashes as placeholders for unset keys (G6 all pass, but the formatting-only probe reads the dash count: +31 to +41 pp).
4. **Exemptions:** E1 and E2 confirmed as written, E3 confirmed on three conditions (15 Oct ~19:40 UTC); recorded in G0 section 7. The rules and legend block is now registered as role `program` skins `T45-RULES-<head>` (placeholder lint only; `test_rules_block_is_a_program_template_without_row_facts` lints them and checks byte identity per (head, legend)). G0 re-frozen: sha256 `fe1694bb1be6d94ebb6b3e21b9ac099756b6b3239c5c1946b31bd4b0c97acda8` (`T45Plugin.G0_SHA256`; `test_contract_and_independence` pins it).

## A45 pre-freeze check (run 11: 6,000 QC rows in memory, G15 off as in A43 a, 3 workers, warm execution cache)
Command: `T45_EXEC_CACHE=<scratch file outside the repo> nice -n 10 ../../.venv/bin/python -B families/T45/prefreeze.py --n 6000 --workers 3 --out <metrics.json>`.
Wall time (machine load average 50-130): cold execution of the 183 canonical structures = 79 s (3 threads, 2 fresh processes each); with the cache warm: build 7.6 s (3 workers), analysis and audits 41 s. Earlier cold-machine builds: 554 s for 5,000 rows at load 200.
| Gate / check | Value | Bar | Pass |
|---|---|---|---|
| Program gates G2 G3 G4 G-SL G-LEX G-TW schema options (6,000 units) | 0 dropped | 0 | yes |
| G15 | 30 + 14 units in tests and smoke runs, 0 failures (not run on the QC rows) | 100% | yes (partial) |
| Solver A = solver B | 2,000 specs in the test run (400 per sampler incl. S5, facts and option keys) + all 6,000 build units | 100% on >= 2,000 | yes |
| G6 overall, all 4 views x LR / GBT (chance .3841) | worst: c LR .3915 (+0.7), d_meta GBT .3783 | <= chance + 2 pp | **yes** |
| G6 move head (n 2,090, chance .3825) | worst: d_meta GBT .3981 (+1.6), c LR .3890 | same | **yes** |
| G6 outcome head (n 3,910, chance .3849) | c_card LR **.4171 (+3.2)**; d_meta GBT .3918 (+0.7); a / b <= .399 | same | **NO (one cell)** |
| G7 | pass | 0 failing | yes |
| G10 (gold position, gold-is-longest; yes/no checks n/a) | pass | pass | yes |
| plan_report (position, length rank, longest) | pass | pass | yes |
| Options-only probe (outcome / move) | LR +1.4 / -1.0, GBT -0.3 / -2.25 pp | +/- 3 pp | yes |
| Formatting-only probe (outcome / move) | LR -0.3 / -2.6, GBT +0.6 / -2.0 pp | +/- 3 pp | yes |
| Reseed audit (3% = 180 rows regenerated: new execution parameters, surface, padding, option draw) | 0 flips, 0 solver-B flips | <= 1% | yes |
| Surface-name audit (20 specs re-executed with real names) | 0 mismatches, 0 errors | 0 | yes |
| Held-out fault `stale_noop` | 0 rows in S1-S4, present in S5 | 0 | yes |
| Determinism, PYTHONHASHSEED 1 and 2 | identical row hashes (test) | identical | yes |
| Mean / max prompt (real tokenizer, instructions twice) | 716.5 / 849 | <= 800 / 2,000 | yes |
| Cards, rows per card | 640 cards, max 20 | >= 20, <= 64 | yes |
| SUCCESS share | 37.7% of head-1 rows, 36.3% of all rows | >= 35% | yes |
| pytest (`families/T45/test_t45.py`, N_AB 2000, BUILD_N 1500) | 17 / 17 (the 16 others in one run, `test_in_memory_build` re-run at 1,500 rows) | all | yes |

### The open cell: G6 view c (card without question), logistic regression, outcome head
It grows with data (+3.3 pp at 3.9k rows, +7.3 pp at 7.8k rows before the last fixes) and is spread over kinds (git +2, db +4, http +3, build +2, tests +1 at 1.5k rows each). Not a single (option token, context token) cross is significant (4,384 crosses tested at 10.4k rows, max |z| 3.1, noise level), the generator is independent of the label where it should be (gold uniform inside the shown set, chi2 p = .81; legend, pack, sampler p > .19; kind p = .03), and the signal needs the three state lines together (intent + before + after +3.4 pp; any single line or the instructions and card alone <= 0). So it is an aggregate of many weak token-presence effects of the real evidence, not one cue. Next candidates (not tried): give the disguised and padding items the SAME small-vocabulary tokens as real items in label-blind proportions (e.g. build every non-set key from the real items' own name and value tokens with a different pairing), or move item values to a closed vocabulary shared by real and padded items; then re-run `prefreeze.py`. Everything else in the bar is met.

## Open items
1. The c-view LR cell above (bars unchanged; nothing loosened). If it cannot be closed by Sat 17 Oct 18:00 UTC, T45 moves to C3 under A47. 2. No `haiku/` task files (Mode T only; the 6 question wordings are admitted by program stand-ins `program:stand-in-N`; real G-LEX needs the 2/2 Haiku reads). 3. G5-H / G3-H / G8 / G9 / G11-G13 / G-TPL / G-TW (no twins) are outside this in-memory bar and were not run. 4. Solver B is a parse + set-algebra verifier with no per-tool semantic predictor; tool semantics are checked on the A side (executed retry and repair, `Inconsistent`). 5. The printed command is the fault-independent plan; new non-intent keys written by the step are not shown (other keys never matter): G0 section 1. 6. The `ch_move` options-only / formatting-only GBT sit 2-3 pp below chance (balanced-design deficit, as T40 reported); they pass but are close to the -3 pp edge. 7. `plugin.FAMILIES` has no T45 (registered at import; kit candidate). 8. Execution cost: 183 canonical structures x 2 fresh processes (1-3 s each idle; 4-10 s at load 200), cached in memory by sha256 of (kind, params); the optional development cache `T45_EXEC_CACHE` must stay outside the repo and is not rows. 9. Execution under heavy load can drop specs (ExecTimeout); drops are by structure and redrawn within the same fault, so they cannot bias labels, but a very loaded machine lowers throughput.
