# Sealed-side child checkers for C2

Two programs inside the sealed folder compare C2 data with the frozen final test suite. The C2 side RUNS them and
reads only their result; it never opens, lists or copies `lean/ohs4_sealed/`. Each program reads the suite itself,
checks its sha256 against the freeze manifest (exit 3 if it changed) and prints / writes only counts and C2 ids. No
test text, test id or per-item detail ever comes back.

CPU only, no network, $0. Run from `lean/` with `../.venv/bin/python` (numpy). Both import
`lean/c_build/decontam_g13.py` read-only (its normalisation, n-gram, MinHash and structure functions); its sha256 is
in every result, so keep that file in place.

## 1. Rows / units: `g13_ohs4_check.py`

```
cd lean
../.venv/bin/python ohs4_sealed/tools/g13_ohs4_check.py --rows <c2_rows.jsonl> --out <result.json>
../.venv/bin/python ohs4_sealed/tools/g13_ohs4_check.py --selftest     # built-in controls; exit 0 = all pass
```

Input: JSONL, one object per line (blank lines skipped, other fields ignored).

| field | meaning |
|---|---|
| `id` | required; the id reported back on a hit |
| `state`, `instructions` | strings |
| `card` | a string, or a mapping (its sorted-key JSON and every string leaf are compared) |
| `options` | a list of strings, or null |
| `call_id` | optional; rows that share a `call_id` form one unit and a hit marks every row of the unit |

Methods (decontam_g13 style: the suite is the eval side, your rows the training side; any method is a hit):

| method | hit when |
|---|---|
| `exact_full` | a suite text of >= 5 words equals one of your texts (normalised) |
| `exact_seg` | a suite sentence / line of >= 5 words equals one of your sentences / lines |
| `exact_short` | a suite state under 5 words equals one of your texts (never your options) |
| `substring` | a suite text of >= 5 words occurs inside one of your texts (word boundaries) |
| `ngram10`, `ngram12` | any shared word 10-gram / 12-gram (n-grams stay inside one text) |
| `tulu8` | more than 50% of a suite text's words lie in 8-grams shared with ONE of your texts |
| `minhash` | word 5-gram MinHash (100 perms, 20 x 5 bands) confirmed by 5-gram Jaccard >= 0.8 and word edit similarity >= 0.8 |
| `structure_g13` | `struct_g13(state, options)` equal (names abstracted, options as a set; see FORMAT.md) |

Normalisation is `words()` in FORMAT.md (NFKC, lower case, letter / digit runs).

Output (`--out` file; without `--out` the same JSON goes to stdout; with `--out` stdout gets only `counts` and
`complete`):

```json
{"tool": "g13_ohs4_check", "version": 1, "suite": "frozen", "manifest_verified": true,
 "suite_sha256": "<hex>", "g13_sha256": "<hex>", "input_sha256": "<hex>", "params": {}, "methods": [],
 "counts": {"c2_rows": 0, "c2_units": 0, "c2_texts": 0, "hit_units": 0, "hit_rows": 0, "ohs4_calls_hit": 0,
            "by_method": {"<method>": {"c2_units": 0, "c2_rows": 0, "ohs4_calls": 0}},
            "hit_units_by_c2_field": {"<state|instructions|card|option|state+options>": 0}},
 "hit_ids": ["<your row id>"],
 "hit_ids_by_method": {"<method>": ["<your row id>"]},
 "complete": true, "wall_s": 0.0}
```

Exit codes: 0 = no hit; 4 = hits (result written); 2 = input or usage error (stdout
`{"error": "input", "detail": "input line N: ..."}` or `{"error": "<class name>"}`); 3 = the suite no longer matches the
freeze manifest. Rows are streamed: about 13 s and 0.7 GB RAM for 50,000 rows (150,000 texts) on the Mac.
Action: drop every row listed in `hit_ids` (whole units).

## 2. Templates: `gtpl_check.py`

```
cd lean
../.venv/bin/python ohs4_sealed/tools/gtpl_check.py --templates <c2_templates.jsonl> --out <result.json> \
    [--min-shared 1] [--parts R,U]
../.venv/bin/python ohs4_sealed/tools/gtpl_check.py --selftest         # built-in controls; exit 0 = all pass
```

Input: JSONL, one template per line: `{"id": <required>, "text": <template>}`. Placeholders use Python format style:
`{name}`, `{0}`, `{}`, `{name:spec}`, `{name!r}`, `{a.b}`, `{a[0]}`; `{{` and `}}` are literal braces; a brace
group that starts with a quote or a space (inline JSON such as `{"Effect": "Allow"}`) is text, not a slot. A row whose
`text` is not a string is counted and skipped.

Method: the text is cut at every placeholder into pieces (an n-gram never spans a slot); a word glued to a
placeholder with no space between (`{n}th`, `{x}abc`) is dropped from its piece; each piece is normalised with
`words()` (FORMAT.md) and every word 8-gram inside it is compared with every word 8-gram inside one field (state,
instructions, card, each option) of the suite's R and U items, including their paired renderings. `--parts all` adds
the general part; `--parts R` or `--parts U` narrows the scope. A template hits when it shares at least
`--min-shared` distinct 8-grams (default 1).

Output:

```json
{"tool": "gtpl_check", "version": 1, "suite": "frozen", "manifest_verified": true,
 "suite_sha256": "<hex>", "g13_sha256": "<hex>", "input_sha256": "<hex>", "ngram": 8, "scope_parts": ["R", "U"],
 "counts": {"templates": 0, "templates_with_8gram_piece": 0, "pieces": 0, "hit_templates": 0,
            "shared_8grams_total": 0, "min_shared": 1},
 "hit_ids": ["<template id>"], "shared_8grams_by_id": {"<template id>": 0},
 "complete": true, "wall_s": 0.0}
```

Exit codes as above. Runs in about 1 s. Action: reword every hit template, then run again.

## Rules

- Run only. Read only the result JSON; never open the sealed folder or the checkers' source.
- Feed real C2 rows and templates only. Do not send crafted probe text to learn what the suite contains.
- Hash-level checks you can run yourself: the files next to this one (see FORMAT.md).
