# LC_SOLVER_B: the independent Solver B engine for T42c, T57 and T56g

Written Sun 18 Oct 2026 by the L-C solver-B session (Sonnet), from the three approved G0-lites, the G0 addenda and the three
`ROW_SCHEMA.md` files only (Opus ruling G1: solver B is CODE). Stdlib only. Nothing here executes generated text.

## Method (different from solver A)
Solver A labels from sandbox witnesses; until the sandbox is signed off its `SimExecutor` predicts every witness from the IR
interpreter. Solver B instead PARSES THE RENDERED SOURCE TEXT of each language and interprets it with its own evaluator:

| Language | Parser | Evaluator | Test runner model |
|---|---|---|---|
| Python | stdlib `ast` (parse only) | own tree walker, host values for ints/strs/lists (real Python semantics) | plain (T42c) and a pytest model: collection, skip/xfail marks, raises, conftest hookwrapper + sessionfinish, exit 5 when nothing is collected |
| JS / TS | own tokenizer + Pratt parser, TS type erasure | own evaluator (JS number rules, strict equality identity, undefined, `%` sign of dividend, template strings, classes, closures) | `node --test` model per file: node:test, node:assert/strict as a MUTABLE object (assignments to `assert.*` take effect), `process.on('exit')` |
| Go | own tokenizer (semicolon insertion) + parser | own evaluator (int64 wrap, truncating `/` `%`, slices with Go append growth and aliasing, struct copy, panics with Go type names, defer/recover with named results, per-iteration loop variables) | `go test` model: TestXxx, `t.Fatal*`, `t.Skip*`, TestMain, `init()` + `os.Exit`, plus a compile check (unused import / unused local = build failure, exit 2) |
| bash | line/block parser + word scanner | own evaluator (C-like 64-bit arithmetic, `[ ]`, `[[ ]]` glob patterns, sparse arrays, dynamic scoping of `local`, `$(...)` subshells, printf, `.` sourcing, `trap ... EXIT`) | script run: the verdict is the exit status |

Unmodelled constructs raise `Unsupported` (counted as a refusal, never a label). Step budgets turn loops into `Timeout`.

## Layout
- `common.py` observables, option-text per language (ROW_SCHEMA section 1), refusal types
- `pyeval.py`, `jseval.py`, `goeval.py`, `sheval.py` the four evaluators; `langs.py` the uniform adapter; `diffapply.py` unified-diff applier
- `agreelib.py` tally, G1 lint (`lint_b_files`), batch rule; `shalog.py` writes `SHAS.json` per family
- Family code: `T42c/solver_b`, `T57/solver_b`, `T56g/solver_b` (`solve.py`, `hook.py`, T56g `sigs.py`, T42c `crosschecks.py`) and
  `agree.py` (the ONLY file of each solver_b that imports the generator side)

## Run
```
cd c21_fam
python3 -m pytest LC_SOLVER_B ; python3 -m pytest T42c/solver_b ; python3 -m pytest T57/solver_b ; python3 -m pytest T56g/solver_b
python3 -m T42c.solver_b.agree --rows 500 --seeds 101,102 --out /tmp/t42c.json      # in-memory rows, count-only report
python3 -m T57.solver_b.agree  --rows 300 --seeds 201 --out /tmp/t57.json
python3 -m T56g.solver_b.agree --rows 300 --seeds 301 --out /tmp/t56g.json
python3 -m LC_SOLVER_B.shalog
```

## Generation-time hook (owner rule 18 Oct)
`<FAM>/solver_b/hook.py`: `check_row(row[, packages])` -> keep / drop with a reason class; `check_batch(...)` applies the block rule
(T42c 2%, T57 2%, T56g 3% dropped for disagreement returns the block). Wire it before G13 in the stamp wrapper.

## What this does NOT prove
B agrees with A's SimExecutor labels, i.e. with the IR interpreter and the spec expectations. That checks the RENDERED TEXT against
the IR (a renderer or hack-design bug shows up as a disagreement) but it is not a sandbox run: toolchain-specific behaviour (real
Go vet, real pytest plugins, node version quirks, bash version quirks such as `unset 'a[-1]'` followed by `a+=(x)`) still needs the first
sandbox smoke after sign-off. COMPILE2, A10 wrapper rows and A16 views are not in the generators yet, so B has no solver for them.
