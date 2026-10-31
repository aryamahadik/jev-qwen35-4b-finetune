# T57 row schema and the Solver B contract

Solver B is CODE written by a separate Sonnet session from the G0-lite and THIS file only (Opus ruling G1). It must not read
Solver A (`solver_a.py`, `task.py`, `heads.py`, `facts.py`, `build.py`) and may import only the standard library and this schema. B
recomputes the execution class of every candidate patch, the TESTSEL before/after table and the LOCALISE gold from the module trees
and the hidden suites with its own harness and its own differential enumerator. Agreement with A: 100% of kept rows.

## 1. What B receives per row (`schema.b_view(row, packages)`)

```
{ "row_id", "head": "VERDICT"|"BEST4"|"TESTSEL"|"LOCALISE"|"REASON", "lang", "carriers": {...rendered, no QUESTION_FORM...},
  "b_inputs": { "task_uid", "candidate_files": [ {path: text} ... one tree per shown patch ... ], "options": [...]|null, "visible_case": name },
  "package": <task package of the row's module> }
```
Task package (`schema.task_package(task)`): `reference_files`, `buggy_files` ({path: text}); `go_files` (go.mod, vendor/modules.txt);
`visible_case` and `hidden_cases` (structured, see 2); `differential_points`: list of call lists (each call `{"fn","args"}`) plus
`snapshot` (method called after a point that touches the instance); `class_rules`; `reset_name` (bash state reset), `class_name`.
No label, no expected class, no candidate kind, no TARGET/PASS-TO-PASS tags (derive them by running the buggy tree).

## 2. Structured test cases

A case is `{"name", "steps": [step...], "fn", "kind"}`; a step is `{"op":"eq","fn","args","expect"}` (call must return `expect`),
`{"op":"raises","fn","args","err"}` (call must raise; `err` is an abstract id, the language-visible name is in the module source)
or `{"op":"do","fn","args"}` (call, ignore the result). Methods are called on one fresh instance per case (Go `mk<Class>()`, bash
the reset function). Values are JSON; strings use the characters `[A-Za-z0-9_ :.,/=#-]`.

## 3. Gold B must reproduce

Execution class of a patched tree, first rule that applies: NOFIX (the visible case still fails), REGRESSION (the visible case passes
and a case that passes on the buggy tree now fails), PARTIAL (a case that fails on the buggy tree still fails, or the differential
finds a divergence from the reference over `differential_points`), CORRECT. Differential: run every point on the reference and on
the candidate; equal observables (return value or exception class/exit status per call) at every point = no divergence.
* VERDICT: label `CORRECT` if the class is CORRECT else `INCORRECT`; for INCORRECT also the class (reason head).
* BEST4: the letter of the single CORRECT patch (A-D); the other three must have a class != CORRECT.
* TESTSEL: `options` are hidden case names; run each on the buggy tree and on the (CORRECT) patched tree; the gold is the one that
  fails before and passes after; the other three pass on both.
* LOCALISE: `options` are function names; the gold is the function that differs between the reference and the buggy tree.
* REASON (head rows): options PARTIAL/REGRESSION/NOFIX in the order given by `meta.reason_options`; B outputs the letter of the class.
* Output: `{"row_id", "label": ..., "classes": [per candidate class], ...}`.

## 4. Row JSON written by Solver A (for reference)
`row_id, family="T57", head, lang, label, question_form, wording_id, carriers, prompt_text, names, b_inputs, meta, manifest`.
`meta`: `module_id, base_module, task_uid, norm_hash, tokens, wording_id, variant ("primary"|"with_outputs"), twin_of, pair_id, pair_kind
("nearmiss"|"altfix"), bug_fn, bug_op, multi, cands[{kind, cls_exec, style, comment_kind, decoy}], medoid, options, opt_roles, opt_flags,
gold_index, altfix, perm_copy/perm_of/perm, reason_options/reason_gold, leak_hits`.
`manifest`: `module` (gold-sanity ok, strength record: mutants, decided, killed, undecided, kill_share, T_s, T_s_by_pilot, bug tags),
`cand_classes`, `evidence` (differential equal / failing cases), `reason`, `spec_expectation`, `pins` (PENDING), `solver_a_version`.
