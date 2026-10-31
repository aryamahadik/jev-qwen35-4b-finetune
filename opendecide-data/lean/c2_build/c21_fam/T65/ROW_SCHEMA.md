# T65 (VULN-SYNTH, generated half) row schema and the Solver B contract

Solver B is CODE written by a separate session from the T65 G0-lite (incl. the Opus batch-1b block) and THIS file only. It must not read Solver A
(`solver_a.py`, `specs.py`, `templates.py`, `generator.py`) and may import only the standard library and `schema.py`. Python only in this slice (the Juliet C/Java/C# slice
is L-R and is not here). Agreement with A: 100% of kept rows; a class with > 1% disagreement returns to the generator (plan 16.1 fix trigger).

## 1. What B receives per row (`schema.b_view(row)`)

```
{ "row_id": str, "head": "VULN"|"CWE", "sub_block": "CWEC-22"|...,
  "rendered": {"context": str, "question": str, "options_text": str, "text": str},
  "options": [{"letter": "A", "text": "YES"}, ...],
  "witness_inputs": {"head": "VULN"|"CWE", "class_group": "dynamic"|"static"|None} }
```
No label, no spec, no witness, no meta. `row_id` is OPAQUE (`b-` + a hash; the real id ends in `-a` for the YES member, `-b` for the NO member, `-c` for a CWE head row), and for a CWE head row `sub_block` is `"CWE"` (not the class). Expected output: `{"status": "ok"|"abstain"|"error", "label": "YES"|"NO"|<class word>|None}`.

## 2. VULN head (YES = flawed, NO = sound; options `YES` / `NO`, two letters, shuffled)

`rendered.context` = definitions block, a one-line request note, and `Function (<stem>.py):` + a small Python function (3-12 lines, imports first, no comments).
Label rule = the definitions block: a function is flawed when a value an attacker controls reaches a sensitive operation without a step that neutralises it for THAT
operation, applied to the value that reaches it, on every path before the operation, and its result used.

* Dynamic classes (path traversal, OS command injection, cross-site scripting, SQL injection, log injection, open redirect): B is an EXECUTION harness. It
  imports the module in the pinned image (runner.canary_harness.python), calls the function with a benign input and with the registered canary payload
  of the class (payload list in the L0 image record, hashed before the first dynamic row), 3 identical runs, and says YES iff the canary effect is observed
  (file content of the canary file; a line equal to the canary word in the command output; the canary markup in the HTML; a second row from the canary query;
  a forged extra log line; a redirect whose host is the canary host). It says NO iff the benign call works and the effect is not observed; anything else is `error`.
  The function bodies use only the standard library (os.path, html, shlex, subprocess with echo, sqlite3 in memory, urllib.parse). The harness (`CALLS_RUNNER`) changes into the job directory before the calls; the CWEC-22 job ships the served files as part of the job (`config.FIXTURES`: `srv/files/readme.txt`, `srv/files/guide.txt`, `srv/canary.txt`) and the served root in the function is the relative path `srv/files`; the CWEC-89 function creates and fills its own two-row `users` table inside the function (a fresh in-memory database has none).
* Static-only classes (disabled certificate verification, weak password hashing, insecure temporary file): no execution. B is an independent AST pattern engine:
  YES iff a TLS context has verification switched off for a flagged use, or a password-role value reaches a fast unsalted hash (md5 / sha1 / plain sha256, no pbkdf2/scrypt),
  or a predictable temp path is built / `mktemp` is used instead of an exclusive create. The same call on a non-password value, or with the safe API, is NO.
* Decoys: a neutraliser of the wrong class, applied to a different variable, placed after the operation, discarded, overwritten, or on a short-value branch only is still YES;
  a no-op helper is YES; a helper that really neutralises, an allow-list, a parameterised API, or a constant source is NO.

## 3. CWE head rows (`witness_inputs.head = "CWE"`, 4 options, class WORDS only, never numbers)

`rendered.context` = definitions + `Function (<stem>.py):`; the question asks which weakness the function shows; options are the class word and its three nearest
classes. B gives the class word by the same execution / AST evidence as in 2. Head rows are built from KEPT YES specs only (<= 25% of the YES specs, <= 75 rows).

## 4. Row JSON written by Solver A (B never reads these)

`row_id, family="T65", head, sub_block, group_id, gold, label, gold_letter, options[{letter,label,text}], question_form, slots{fn}, rendered, names, spec, witness_inputs,
meta{template_id, wording_id, construction_id, ladder, tokens, split, pair_id, twin_of, reuse_group, mech, member, pair_kind, edit_lines, ...}, manifest{gold_method, witness}, stamp`
`names` = {policy: defs_card.t65.vuln|cwe, tool: [], language: [python], runner: [runner.canary_harness.python] (dynamic only), carrier: FUNC_CONTEXT, OPTIONS, QUESTION_FORM, SRC_FILE}.
Pair kinds: `plain`, `decoy:DS-1..6`, `ns:NS-1..4`. Twin members share scenario, names and layout; the NO member differs by one token, argument, position or line.
