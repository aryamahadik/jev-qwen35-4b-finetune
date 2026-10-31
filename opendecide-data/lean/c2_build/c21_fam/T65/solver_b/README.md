# T65 solver B (independent static dataflow analyser)

**What it is.** A program that labels a T65 row from its b-view only (`schema.b_view(rec)`: head, sub_block, rendered context / options, witness_inputs).
It never executes, compiles or imports row code, never reads a file at run time, and imports only the standard library and its own package.

**Method (differs from A).** B parses the rendered Python with `ast.parse` and runs a small *abstract interpreter* (`engine.py`): every variable holds a summary
(`values.py`: attacker-controlled / password-role / weak-digest / predictable-temp flags, the set of classes neutralised on every path, constant fragments, TLS
context handle). Branches are forked and joined (a raw value on any path defeats a neutraliser on another), code after `return` / `raise` is unreachable, helpers
are analysed inline (so a neutraliser two calls away, or a no-op helper, is seen), allow-lists (`x in K`, `x == "c"`) make a value neutral, a neutraliser counts only for
the class it is made for (`rules.py`: basename -> path, shlex.quote -> command, html.escape -> markup, replace quote / newline -> SQL / log, `"/" + x.lstrip("/")` ->
redirect), and a flagged static use counts only if it reaches the function result (G0-lite "its result used"). A is the spec-level taint label plus a sandbox / dry-run
witness; B shares none of that and does not use the spec, the witness or the pair kind.
Anything it cannot model (loops, `with`, `try`, unknown calls on state-bearing values, an unnamed entry) is an **abstain**, never a guess.

**Files.** `rules.py` (tables from the G0-lite), `values.py`, `engine.py`, `parse.py` (context split, source note, lettered options), `solver.py`, `hook.py`
(`solver_b`), `agree.py` (in-memory harness; the only module that touches the generator side), `make_shas.py`, `tests/`, `agreement_log.json` (counts only), `SHAS.json`.

**Run.**
- Wiring: `checked.adapter(solver_b=hook.solver_b)` or `checked.run(total, seed, stamper, standin=True, solver_b=hook.solver_b)`.
- Direct: `from T65.solver_b import hook; hook.solver_b(schema.b_view(rec))` -> `{"status": "ok"|"abstain"|"error", "label": "YES"|"NO"|<class word>|None, "letter": ..., "cls": ..., "reason": ...}`.
- Agreement (from the `c21_fam` folder): `PYTHONDONTWRITEBYTECODE=1 python3 -m T65.solver_b.agree --rows 1200 --seeds 2001,2002 --out $SCRATCH/rep.json [--log agreement_log.json]`
  (`--rows` is the plan total per seed; about 1,170 rows per seed come out).
- Tests (from this folder): `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q`.

**Reading choices (G0-lite sentences B follows).** Credit is by registry class, not by accidental effect (e.g. `html.escape` counts for markup only). An allow-list of
constants is neutral for every class. A string command without `shell=True` and an argv list are not command sinks. For TLS, verification is off when
`verify_mode` may be `CERT_NONE` or `check_hostname` may be `False` on the returned context. Execution witnesses (ROW_SCHEMA section 2, dynamic classes) are NOT run
by B (brief: no execution); A's side carries them.
