# G0-lite T40: CALL-GATE (tool selection and tool-call validity)

G0-lite, about 2 pages (C2_DATA_SPEC 6.2 item 3; FINAL_PLAN section 3 row 1, A42). Agent tier, wave 1. Target: about 2,000 C2 rows, at least 40% VALID on head A, 500 sealed items later. Code: `plugin.py` (sampler, solver A glue, rendering, relations), `resolver.py` + `schema.py` + `edit.py` (gold), `solver_b.py` (verifier), `world.py` + `pools.py` (registry generator), `fixtures.py` (program-authored wordings and headers, never a pool).

## 1. Decision and options (every option has a one-line definition; the same text is printed on the row's card)

| Head | Question | Option | Definition (first rule that fits, in this order) |
|---|---|---|---|
| A | Is a proposed tool call valid against a stated registry, menu, request and earlier results? | NONEXISTENT_TOOL | the name (or `provider::name`) is listed by no tool in the registry |
| | | AMBIGUOUS_PROVIDER | a bare name is listed by two providers (a call must resolve by itself, whatever the request says) |
| | | OFF_MENU | the tool is listed, but its menu flag is `no` |
| | | BORROWED_SIGNATURE | at least one argument, none is a parameter of this tool, and all argument names belong to one other listed tool |
| | | BAD_ARGS | a required argument is missing, or an argument name is not a parameter of this tool |
| | | TYPE_VIOLATION | a value breaks its parameter's JSON-schema type, range, enum, format or id pattern |
| | | UNGROUNDED_VALUE | a value is stated by neither the request clauses nor an earlier result (slot ledger) |
| | | VALID | none of the above |
| B | What should the agent do with the request? | CANNOT_ANSWER | no tool on the menu has the purpose the request asks for (unlisted purpose, or the tool is off the menu) |
| | | ASK_FOLLOWUP | a tool fits, but two providers list it and the request names none, or a required value is not available (stated as `label: value`, or an earlier result field named like the parameter) |
| | | CALL | otherwise: the agent calls the tool now |
| C | Does a proposed `str_replace` edit on a small Python file apply? | NO_MATCH | old_str occurs nowhere in the file (exact characters) |
| | | MULTIPLE | old_str occurs more than once (non-overlapping count) |
| | | BREAKS_SYNTAX | old_str occurs once, but the edited file no longer parses (`ast.parse`) |
| | | APPLIES_ONCE | old_str occurs once and the edited file still parses |

Closed world: "The listing above is complete: no other tool, file, rule or fact applies." (every row; the complement pairs rely on it).

## 2. Gold (solver A) and verifier (solver B)

- **A, paradigm rule_engine** (`resolver.py`): the registry is JSON-schema per tool (`schema.py`: type, required, enum, format email / date, pattern, minimum / maximum, items, additionalProperties; own validator, no jsonschema). Head A applies the ordered rules of section 1; structural schema errors (`required`, `additionalProperties`) give BAD_ARGS, value errors TYPE_VIOLATION. The slot ledger of grounding is the set of values of the request clauses, the provider clause and every earlier-result field value (exact token equality). Head B: tools whose purpose equals the request purpose and whose menu is yes, filtered by the provider clause; two providers left = ASK_FOLLOWUP; a required parameter is available when its label is a clause of the request or its name is the key of an earlier-result field. Head C: the REAL run (`edit_exec.py`, subprocess, `python -I -B`, `PYTHONHASHSEED=0`, temp dir as cwd, 5 s cap, no network; `str.count`, `str.replace`, `ast.parse`).
- **B, paradigm sql_sqlite** (`solver_b.py`, written from this page): parses the rendered state with its own regexes into SQLite tables (tools, params, args, known values, clauses, result keys); resolution, menu, borrowed signature, missing / unknown arguments by anti-joins; types by `json_type`, ranges by BETWEEN, enums by `instr`, formats and id patterns by a `regexp` user function, dates by `date()`; grounding by `NOT IN`. Head B by `instr(lower(request), lower(purpose))`; head C by `re.finditer` (non-overlapping) and `compile(..., PyCF_ONLY_AST)`.
- Gold is never a model output. A draw whose solver-A label differs from the design target is redrawn (label-first; never relabelled).

## 3. Registries, samplers, held out

Registries are generated from typed parameter templates (`pools.py`): 16 domains x 5 tool templates (types city, email, date, path, slug, text pools, int/num ranges, enum, id prefix), 3 providers each, 8 naming styles (snake / camel / pascal / kebab, verb-noun and noun-verb, dotted namespaces). A registry excerpt has 3-8 tools; a target tool is drawn, duplicates (same name, other provider), off-menu tools and earlier results are added with label-neutral rates (a feature a label forces is drawn at the same overall rate on the others).

| Sampler | Shape |
|---|---|
| S1 | 3-4 tools, one request, few earlier results |
| S2 | 4-6 tools, earlier results supply id values (chaining) |
| S3 | 6-8 tools, other-domain tools, many collisions and menu flags |
| S4 | 5-6 tools, near-miss siblings; head C identical across S1-S4 except the file vocabulary pack |
| S5 (HELD OUT, `dev_only`) | held-out domains (shipping, astronomy, veterinary, library), held-out naming styles (camel noun-verb, dotted noun.verb, kebab), held-out code vocabularies (orbits, kennel, harbor), held-out syntax-break operators (unterminated_string, stray_keyword), held-out header registers (transcript, form) |

Training: 12 domains, 5 styles, 8 code packs, 4 break operators (drop_colon, drop_paren, bad_indent, dup_operator), 7 registers. Head C: 2-4 functions from 7 role templates; old_str is a fragment of the file picked at a label-blind target length; NO_MATCH by identifier typo (a slot), indentation or operator flip; BREAKS_SYNTAX by the break operators.

## 4. Question forms, cards, balance, budget

- Yes/no (45-55% of rows): per head one positive form (yes iff the good label: VALID / CALL / APPLIES_ONCE), one double-negation form (k_syn 2, same meaning), one antonym complement and one syntactic complement (yes iff not good). Choice (closed sets shown whole, one label-blind position per row): ca_diag (8), cb_action (3), cc_edit (4). 15 forms, 38 program-authored wordings (Haiku adds more, `haiku/`). Card = rules of section 1: in `row.card` on yes/no rows, in the instructions on choice rows.
- Balance by design groups (`plugin.design`, 128-seed blocks): yes/no groups are 2 seeds with opposite gold and the same wording, overlay and register, so the yes rate per wording x negation cell is exact; choice groups hold every label once with a permuted gold position, so labels and positions are exact. Head A: yes/no 78%, so VALID is at least 40% of head A rows; faults are uniform on choice rows. Twin / equiv / complement presence is decided per group.
- Relations (G4 and overlay): complement (yes/no pair, same state), minimal-edit twin of one slot (call argument, call name, argument name, menu flag, or old_str identifier; the flipped label comes from the construction), equiv (other register), G4 metamorphic: rename the user; reverse the registry order; reverse the request clauses (A, B); rename an identifier everywhere; append a comment line (C). No attack lines.
- Budget: prompts mean <= 800 tokens (measured about 680 by the 3-characters-per-token estimate), max 2,000; <= 64 rows per card (card = sampler x head x pack); 2,000 C2 rows, 500 sealed (S5 only).
