# T45 TRACE-VERIFY: build notes (15 Oct 2026, Sonnet 5.5 code agent)

**Status (fix round 2, 15 Oct): the last open cell is closed. At 10,008 QC rows every G6 cell (overall and per head), both probes, G7, G10 and plan_report pass; pytest 17/17. The outcome-head view-c LR no longer grows with data (-1.4 pp at 6,000 rows, -0.1 pp at 10,008).**
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

## Fix round 2 (orchestrator, 15 Oct): the last open cell, by construction
**Mechanism (measured).** With only RARE context tokens kept (document frequency < 10) the view-c LR scored +14.9 pp (all tokens +7.4, common tokens +0.2); rows that share a rare token do not share a label, no single cross is significant (max |z| 3.1 over 4,384 crosses), and the signal needs the intent, before and after lines together. G6's cross features are L2-normalised, so the scale of a pair depends on the NUMBER of distinct context tokens; that number followed the label because a real item repeats the intent's tokens while a disguised or padding item brought fresh ones (SUCCESS: fresh tokens in the before line only; LOUD: in both lines; NEUTRAL: none). Fresh 6-digit ids (first try) changed nothing; the bar needs the count itself to be label-blind.

**Construction (plugin.view).** A state line shows the real keys that were there before, ONE disguised item per intent key not set in that state, and padding items. A disguised or padding item is its template intent key with every variable word replaced by a word of the same length (same separators: same character length, punctuation, digits), carrying the template's value (a padding value is a spare word). Padding (one item per intent key, split label-blind between the two lines) fixes the row's own word list; disguises only recombine words of that list (padding words plus the row's intent words), so they add NO new token. Hence the number of distinct tokens, item count, character length and punctuation of a line cannot depend on the executed variant. Real ids of db and http items and git tag names are rare composite pseudo-words, so no tiny vocabulary can carry a count. Unchanged from round 1: letter-only codes, digit-free values, constant 7-digit runner build number (caps `mag_max`), fault-independent printed command, hidden new non-intent keys. Rare fallbacks (a key needing one letter of length slack, or a new word) are counted in `plugin.DIAG` and were used in well under 1% of keys; 2 of 10,010 units were dropped at render ("no disguised key found"), and those were redrawn, not relabelled.
Not done: matched-group construction (b) and question variation (c) were not needed.

## A45 pre-freeze check (run 15: 10,008 QC rows in memory, G15 off as in A43 a, 3 workers, warm execution cache)
Command: `T45_EXEC_CACHE=<scratch file outside the repo> nice -n 10 ../../.venv/bin/python -B families/T45/prefreeze.py --n 10000 --workers 3 --out <metrics.json>` (6,000 rows: `--n 6000`).
Wall time: cold execution of the 183 canonical structures 86 s (3 threads, 2 fresh processes each); with the cache warm: build 452 s (3 workers, loaded machine), analysis and audits 147 s.
| Gate / check | 6,000 rows | 10,008 rows | Bar | Pass |
|---|---|---|---|---|
| **G6 view c (card without question), LR, outcome head** (chance .3849) | .3711 (-1.4 pp) | **.3838 (-0.1 pp)** | <= chance + 2 pp and no growth with data | yes |
| G6 overall, worst cell (chance .384) | c LR .3762, d_meta GBT .3916 | b/c GBT .3847, d_meta LR .3843 | <= chance + 2 pp | yes |
| G6 outcome head, worst | d_meta GBT .3829 | d_meta GBT .3909 | same | yes |
| G6 move head, worst | d_meta LR .3900 | d_meta LR .3924 (chance .3827) | same | yes |
| G7 / G10 / plan_report | pass / pass / pass | pass / pass / pass | pass | yes |
| Options-only probe (outcome / move) | LR -0.4 / -1.0, GBT +0.3 / -2.3 pp | LR -0.7 / -1.1, GBT -0.9 / -0.8 pp | +/- 3 pp | yes |
| Formatting-only probe (outcome / move) | LR -0.5 / -2.6, GBT +1.2 / **-3.25** | LR -0.4 / +0.5, GBT -0.0 / -1.3 pp | +/- 3 pp | 6,000: move GBT 0.25 pp outside (balanced-design deficit with a small sample); 10,008: yes |
| Program gates (G2 G3 G4 G-SL G-LEX G-TW schema options) | 0 dropped | 2 render drops in 10,010 units (redrawn) | 0 failures | yes |
| Reseed audit (3%) | 0 flips of 180 | 0 flips of 300 | <= 1% | yes |
| Name audit (20 specs with real names) | 0 mismatches | 0 mismatches | 0 | yes |
| Held-out fault `stale_noop` | not in S1-S4 | not in S1-S4 | 0 | yes |
| Prompt tokens mean / max | 716.9 / 839 | 717.0 / 839 | <= 800 / 2,000 | yes |
| Cards, max rows per card | 640 / 20 | 640 / 28 | >= 20 / <= 64 | yes |
| SUCCESS share (head 1 / all rows) | 37.7% / 36.3% | 39.1% / 37.0% | >= 35% | yes |
| pytest (N_AB 2000, BUILD_N 1500) | 17 / 17 | | all | yes |
Earlier rounds, same cell: +3.2 pp (3.9k outcome rows), +7.3 pp (7.8k rows): it grew with data; it does not now.

## Open items
1. No `haiku/` task files (Mode T only; the 6 question wordings are admitted by program stand-ins `program:stand-in-N`; real G-LEX needs the 2/2 Haiku reads). 2. G5-H / G3-H / G8 / G9 / G11-G13 / G-TPL / G-TW (no twins) are outside this in-memory bar and were not run; a Haiku reader will see composite pseudo-word ids and near-miss decoy keys. 3. Solver B is a parse + set-algebra verifier with no per-tool semantic predictor; tool semantics are checked on the A side (executed retry and repair, `Inconsistent`). 4. The printed command is the fault-independent plan; new non-intent keys written by the step are not shown (G0 section 1). 5. The move-head formatting-only GBT sits 1-3 pp below chance at small n (balanced-design deficit, as T40 reported). 6. `plugin.FAMILIES` has no T45 (registered at import; kit candidate). 7. Execution cost: 183 canonical structures x 2 fresh processes, cached in memory by sha256 of (kind, params); the optional development cache `T45_EXEC_CACHE` must stay outside the repo. 8. `_backup_fix2/` and `_backup_fix3/` hold pre-fix copies (no git history for these folders). 9. Re-freeze: G0 sha256 `390822984da2d51dc42c1f44eeafee7fc5daa7f816827486cc72232ac3030725` is pinned in `T45Plugin.G0_SHA256` and by `test_contract_and_independence`.
