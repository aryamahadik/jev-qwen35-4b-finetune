# L-C code lane: T42c CODE-EXEC, T57 PATCH-VERDICT, T56g TEST-GAMING (code only, no rows)

Written Sun 18 Oct 2026 by the L-C builder. Clean-room: no T27 / T40-T46 generator, template, wording pool or earlier mutator, no
benchmark text, no held-out-set path, no model call, no Modal, nothing executed. Every identifier of a generated module comes from
`c21_infra/namespace.py` with the TRAINING salt (module `idents.py`), every policy / tool / language / runner / carrier name is
checked against the frozen allow-list `zed_orch/c21/l0/NAMES_MANIFEST_V1.json` (`names_guard.py`, sha-pinned).

## Layout
```
c21_fam/
  LC_COMMON/   shared: ir.py (language-neutral statement/expression IR + checker), interp.py (reference interpreter = SPEC
               EXPECTATION only), atoms.py + modgen.py (module generator: 14 pure + 5 stateful behaviour atoms, 15 areas),
               lower.py (IR lowering for Go / bash / JS bounds), render_{py,js,go,sh}.py + render.py (module files, witness
               drivers, test files, executor job lines), domain.py + domdriver.py (typed finite domains, unrolled enumerator
               drivers), irmut.py (OUR mutator MUT-01..14, MS-01..04; INJECT vs STRENGTH operator partition), transforms.py
               (EQ-YES-1..5), suites.py (program-generated hidden suites), sandbox_iface.py (Solver A <-> executor; SimExecutor),
               probe.py (G5 probe harness), tokens.py, wording.py, lint.py, provenance.py, plan_utils.py, names_guard.py
  T42c/ T57/ T56g/   config.py, generator modules, solver_a.py, gates.py, build.py, dryrun.py, schema.py, ROW_SCHEMA.md, tests/
```
Run the tests per directory (each has its own pytest.ini): `cd c21_fam && python3 -m pytest LC_COMMON T42c` etc. (one directory per
invocation). Dry run (20 rows in memory only): `python3 -m T42c.dryrun 20`, `python3 -m T57.dryrun 20`, `python3 -m T56g.dryrun 20`.

## What a dry run proves and what it does not
`SimExecutor` predicts every witness from the IR interpreter (and, for the T56g text-level hacks, from a spec-level effect). It
therefore proves the PLUMBING (planner -> generator -> requests -> labelling -> rows -> gates) and exercises every drop rule, but it
cannot find a renderer bug in Go / bash / JS / TS (rendered source has never run) or a runner-naming mismatch. First sandbox smoke
(after the sign-off) must run a corpus of rendered modules through each language and compare to the interpreter: any mismatch is a
renderer bug (yield floor 80% is the only guard until then).

## Open items for L-0 / the orchestrator (found while building; none is guessed away)
1. Executor result records keep only a 200-character stdout preview and no per-test states. T42c needs witness stdout of up to 190
   characters (checked by `observable_len_ok`) and T57 needs per-test states `{test id: passed|failed|...}` from the junit / go-json
   report in the result record (`states`) and the stdout sha256 for domain runs (`stdout_sha256`, already there).
2. `run-batch` reads `will_this_test_fail` for the repeat count (3); the job lines also carry `repeats`: honour it (T42c witnesses = 3).
3. node `--test-reporter=junit` test-id naming (`classname`, `name`) is assumed (`test::<name>`); confirm in the first smoke.
4. The bash "executor-owned driver" protocol used here: `ok <name>` / `not ok <name>` lines and the exit status; T56g visible runs of
   bash use a small `od_run_all.sh` runner generated here.
5. mutmut / cosmic-ray are PENDING wiring: the gate-b mutant pool is our own mutator (operators disjoint from the injection set) for
   all languages; Python rows should additionally report the external score once the CLIs are checked in the image.
6. TypeScript rows (`.mts`, Node type stripping) stay conditional on the self-test; `Planner(ts_ok=False)` folds the share into JS.
7. Toolchain patch versions / image digests are copied into every manifest as `PENDING_L0_IMAGE_RECORD` until the L-0 image record
   exists; no non-Python row before they are appended to the G0-lites.
8. Matched sampling is now in the planners (found by the simulated 900-row builds, not guessed): T56g pairs share one extra-test-file
   decision and are length-matched in chars AND lines; T57 VERDICT / BEST4 / reason rows use std-scaled mean-gap balancers and best-of-k
   candidate choice; T57 LOCALISE modules are single-file with a depth-2 wrapper chain. Simulated builds (SimExecutor, 300-900 rows) still
   show the following gaps, to be taken in the ONE shared fix iteration on the real 1,000-row pilot (n here is too small for the bootstrap
   bound): T57 K6 (BEST4 style cue, acc 0.45-0.55 vs bar 0.28), K5 / K7 / K9 borderline and run-dependent, K12 near-miss share borderline;
   T56g K5 / K6 about 0.55 (bar 0.55, upper 0.60).
9. Design tension in the T56g G0-lite: K6 includes the visible pass/fail state, but a HACK row is VISIBLE_PASS by definition while every
   contradicting-spec honest row (8-12% of rows) and every HONEST-NOTYET row (50 of 600 library rows) fails the visible tests. That alone
   gives an AUC of about 0.55 for the visible flag. Either NOTYET and contradicting-spec honest rows are excluded from K6, or K6 is
   judged on the probe without that flag: needs an Opus ruling before the pilot.
10. Language shares were moved inside the caps (Python 0.72 of rows, JS 0.06, TS 0.04, Go 0.09, bash 0.09) so random drops do not push a
    language under the 8% floor or Python over the 75% cap.

## Build review of 18 Oct (fresh build-review pass; every item below is fixed in place and has a regression test)
1. CHECK AT GENERATION is code now: `checked.py` (`RowChecker`) + `<FAM>/checked.py` (`run_checked`). A row leaves solver A and goes through shape,
   names, token re-count, format probe, solver B (+ B's prose cross-checks for T42c), then the G13 stamp boundary (`tool_engine.row_pipeline.StampHook`;
   no default hook, production needs the row-start-guard pins and a real executor). Order-invariance copies and reason-head rows are stamped too.
2. `suites.step_ok` / SimExecutor: an exception escaping a bare `do` step fails the test in every real runner (the spec ignored it).
3. T42c OUT4 pair rows: the partner may not make an earlier call raise (the earlier calls run bare); SimExecutor models the crashed driver.
4. T42c planner liveness: a coarse cell that fails 30 times in a row is written off with a phantom unit (counted in `skips["STARVED:..."]`).
5. T42c EQV2: a YES row whose two shown programs are textually identical is skipped (it was a pure YES cue).
6. T57 TESTSEL: the shown source now covers every function the four option tests call (15% of specs were unanswerable from the row).
7. T56g F5: offered only when every visible case calls the one wrapped function (the spec claimed visible=pass otherwise).
Not built yet (v3.2 addenda): T42c COMPILE2 head, A10 wrapper rows, A16 views, difficulty ladders, T57/T56g addendum items 2-5 and the L-R feed contracts.
