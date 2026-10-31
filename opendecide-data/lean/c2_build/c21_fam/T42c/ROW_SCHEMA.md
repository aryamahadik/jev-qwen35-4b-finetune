# T42c row schema and the Solver B contract

Solver B is CODE written by a separate Sonnet session from the G0-lite and THIS file only (Opus ruling G1). It must not read
Solver A (`solver_a.py`, `out4.py`, `eqv2.py`, `tfail2.py`, `generator`-side modules) and may import only the standard library
and this schema. B re-derives every label from the row alone, with its own harness per language, its own domain enumerator and
its own comparison of observables. Agreement with A (and the spec expectation) must be 100% of kept rows.

## 1. What B receives per row (`schema.b_view(row)`)

```
{ "row_id": str, "head": "OUT4" | "EQV2" | "TFAIL2", "lang": "python"|"javascript"|"typescript"|"go"|"bash",
  "carriers": { ...what a model would see... },
  "witness_inputs": { ... structured inputs, see below ... } }
```
No label, no manifest, no distractor kinds, no generator metadata, no question wording. `QUESTION_FORM` is removed.

### OUT4
* `carriers.SRC_FILE`: `[{"path", "lang", "text"}]` module files in dependency order (Go also `go.mod`).
* `carriers.CALL_SPEC`: the call(s) as source text (last statement is the asked call; for bash the last line prints `$RET`).
* `carriers.OPTIONS`: `["A. <text>", "B. ...", "C. ...", "D. ..."]`.
* `witness_inputs`: `{"calls": [{"fn": str, "args": [json values]}...], "mode": "last", "ret_type": "int|str|ints|strs"}`.
  Run the calls in order on a fresh instance (if any call is a method of the module's class; free functions need none). Earlier
  calls must succeed; the observable is the outcome of the LAST call.
* Output: `{"row_id", "label": "A"|"B"|"C"|"D", "observable": {"ok": value} | {"exc": name}, "runs": 3, "evidence": {...}}`.

Observable of one call: the return value, or the exception CLASS NAME that escaped (Python: `type(e).__name__`; JavaScript:
`e.constructor.name`; Go: the type name of the recovered panic value without the package qualifier; bash: the exit status of
the function as `exit:<n>`). Messages are never compared. Three runs must be byte-identical.

Option text (to match the observable to a letter), per language:
* values: Python repr (`7`, `'abc'`, `[1, 2]`); JavaScript/TypeScript literal (`7`, `'abc'`, `[1, 2]`); Go literal (`7`, `"abc"`,
  `[]int{1, 2}`); bash raw text (`7`, `abc`; booleans `1`/`0`).
* exceptions: Python `raises <Class>`; JavaScript/TypeScript `throws <Class>`; Go `panics with <Type>`; bash `exits with status <n>`.

### EQV2
* `carriers.PROGRAM_PAIR`: `[{"name": "A"|"B", "blocks": [{"path","lang","text"}]}]` two pruned programs (same function, and
  what it needs). `carriers.DOMAIN_DECL`: the declared domain in words.
* `witness_inputs`: `{"function", "mode": "pure"|"seq", "domain": ..., "snapshot": name|null}`.
  `domain` for `pure` is a list of parameter domains, for `seq` a sequence domain:
  - `{"name","t":"int","vals":[...]}`, `{"name","t":"str","vals":[...]}`, `{"name","t":"bool"}`
  - `{"name","t":"ints"|"strs","elem":[...],"maxlen":n}` = every list up to `maxlen` over `elem` (ordered, repeats allowed)
  - sequence: `{"ops":[{"fn","params":[param domains]}], "maxlen":n}` = every call sequence of length 0..maxlen over the operations.
* Procedure: enumerate the WHOLE domain (pure: the cartesian product of the parameter value lists in the given order; seq: every
  sequence, each on a fresh instance, followed by the `snapshot` call). Observable per point = the list of per-call outcomes (each
  guarded: an exception is recorded, the sequence continues) for seq, the single outcome for pure. The programs are observably
  equal iff the observables are equal at every point; 3 identical runs per program. Domain size is 25 to 5,000 points.
* Output: `{"row_id", "label": "YES"|"NO", "distinguishing": <first differing point or null>, "points": n}`.
  YES = equal at every point. NO = a concrete distinguishing point exists; B must report one.

### TFAIL2
* `carriers.SRC_FILE`, `carriers.TEST_FILE` `{"path","text"}`; `witness_inputs`: `{"test_path", "stem"}`.
* Run the test file with the language-native runner (Python: import the module and call every `test_*` function, catching
  `BaseException`; JavaScript/TypeScript: `node --test`; Go: `go test -count=1 -vet=off`; bash: run the script, `ok`/`not ok` lines,
  exit status). Three runs must agree. The test FAILS iff any assertion or any call raises.
* Output: `{"row_id", "label": "YES"|"NO"}` with YES = the test fails.

## 2. Row JSON written by Solver A (for reference; B never reads `label`, `manifest`, `meta`)

`row_id, family="T42c", head, lang, label, question_form, wording_id, carriers, prompt_text, names, witness_inputs, meta, manifest`
* `names`: `{policy, tool, language, runner, carrier}` lists, all on the frozen allow-list.
* `meta`: `module_id, base_module (CV group), norm_hash (AST-normalised, literals kept), trace_steps, trace_bin ("lt10"|"mid"|"gt40"),
  trace_bin_planned, tokens, wording_id, form, layout ("PENDING_L0_MAPPING"), seed, ir {nodes, loops, calls, funcs}, src_lines, slots`
  plus head-specific: OUT4 `exc_gold, custom_exc, distractor_kinds, options[{text,kind,obs}], gold_index, ret_type, perm_copy/perm_of/perm`;
  EQV2 `similarity, len_ratio, edit_ratio, changed_lines, ast_nodes_a/b, construction, mutator_op, hard_no, domain_size, domain_text`;
  TFAIL2 `shape, n_assert, fail_info, program, expected_in_source, mutator_op`; pairs `pair_id, pair_kind ("invariant"|"nearmiss")`.
* `manifest` (K1 completeness): `witness` (gold/option runs + stdout ids; EQV2 domain runs for A and B, distinguishing runs; TFAIL2 test
  evidence), `spec_expectation`, `steps_final` + `bin_final` (instrumented twin run), `distinguishing`, `construction`, `pins`
  (PENDING until the L-0 image record is copied in), `solver_a_version`, `module_norm_hash`.
