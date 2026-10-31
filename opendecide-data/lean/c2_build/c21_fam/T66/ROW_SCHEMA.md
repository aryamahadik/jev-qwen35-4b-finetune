# T66 (MERGE / SEMVER / MSG, generated slices) row schema and the Solver B contract

Solver B is CODE written by a separate session from the T66 G0-lite (incl. the Opus batch-1b block) and THIS file only. It must not read Solver A (`solver_a.py`, `merge*.py`,
`semver*.py`, `msg_spec.py`, `prog.py`, `tests_gen.py`, `generator.py`) and may import only the standard library and `schema.py`. Python only (JS / Go slices and MSG-REAL are
not built here). Agreement with A: 100% of kept rows (T66-K1); > 1% disagreement in a head returns it to the generator.

## 1. What B receives per row (`schema.b_view(row)`)

```
{ "row_id": str (OPAQUE: `b-` + a hash; the real id's `-a` is the YES / BREAKING member of a pair), "head": "MERGE"|"SEMVER"|"MSG", "sub_block": same,
  "rendered": {"context": str, "question": str, "options_text": str, "text": str},
  "options": [{"letter": "A", "text": ...}, {"letter": "B", "text": ...}],
  "witness_inputs": {"head": ..., "lang": "python"} }
```
No label, no spec, no witness, no meta. Output: `{"status": "ok"|"abstain"|"error", "label": ... | None}`.

## 2. MERGE (YES / NO)

Context: definitions, `Conflict view of <stem>.py:` (git-style markers: ours / base / theirs, one or more conflicts), `Tests of side A (<file>):`, `Tests of side B (<file>):`,
`Proposed resolution of <stem>.py:`. B EXECUTES: writes the resolved file and the two test files in the pinned image (runner.python_isolated) and runs each suite
(3 identical runs); YES iff both suites pass in all runs, NO otherwise (a failing test, an error, an import failure, non-deterministic results = not YES; a non-deterministic
row is dropped by the pipeline, not labelled). The resolutions include: both sides kept in the wrong order, one side lost, a conflict marker left, a duplicated block,
a merge that parses and looks right but breaks a test (semantic break), and correct merges.

## 3. SEMVER (BREAKING / SAFE)

Context: definitions, `Old API (<stem>.py):`, `New API (<stem>.py):`, `Callers written against the old API (<file>):` (a few `test_c<k>` functions), and sometimes
`Declared version bump: patch|minor|major` (a distractor: never the label source). B EXECUTES the callers against the old module (must all pass) and against the new module:
BREAKING iff at least one shown caller fails on the new API, SAFE iff all pass; only the shown callers count. Old module failing a caller = drop (error).

## 4. MSG (YES / NO)

Context: definitions, `Diff:` (a unified diff of one Python file; a group of hunks, some of them trivial: formatting, comment, docstring), `Commit message: <text>`.
YES iff the message describes the one hunk that changes what the code does (the behavioural change); NO iff it is another change's message, or the message of a trivial hunk
only (formatting / comment / docstring). B has no execution: it parses the diff (added / removed lines, AST of old and new function), decides which hunk is behavioural
(the old and new AST differ after dropping comments, docstrings and layout) and checks the message against that hunk's identifiers, verb class and values.

## 5. Row JSON written by Solver A (B never reads these)

`row_id, family="T66", head, sub_block=head, group_id, gold, label, gold_letter, options[{letter,label,text}], question_form, slots, rendered, names, spec, witness_inputs,
meta{template_id, wording_id, construction_id, ladder, tokens, split, pair_id, twin_of, reuse_group, mech, cf, rk, sv, variant, ch, no_kind ...}, manifest{gold_method: execution|construction, witness, strength}, stamp`
`names` = {policy: defs_card.t66.merge|semver|message, tool: [], language: [python], runner: [runner.python_isolated] (MERGE, SEMVER), carrier: per head}.
