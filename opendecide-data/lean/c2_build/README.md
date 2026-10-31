# c2_build: code for the C2 training data (C2_DATA_SPEC 6.2; PREREG_FINAL A37)

**Status: code only.** A37 (f): no C2 Haiku pool, pack, template, generator run or row may exist before OHS-4 is frozen
in amendment A38. Every writer in the kit calls `paths.require_a38()` first and refuses until PREREG_FINAL.md holds a
"Ruling A38" block. The unit tests build a few rows in memory and write nothing.

This folder holds spec 6.2 items 1, 2 and 5: the shared kit, the operator lexicon registry and the new gate code.
Family plugins (item 4), G0-lite specs (item 3) and `c2_select.py` / `mix_c2.py` / `gate_c2.py` (item 6) come next,
built on this kit.

## Layout

```
c2_build/
  README.md                this file
  c2_kit/
    paths.py               never-open guard (spec 6.5), A38 data guard, guarded writers
    slots.py               typed slots: date, UTC-offset datetime, integer cents, count, category, id, glob, url,
                           name, clause; forms that render and parse back exactly
    skin.py                slot-locked skins: renderer with grammar agreement ({a|X}, {N|sg|pl}, ...), spans,
                           JSON / YAML escaping, the template-guided parser used for G3
    rules.py               rule AST + interpreter + precedence policies P1-P5           (solver-A side)
    globsem.py             glob semantics; glob_a.py token matcher (A side), glob_b.py regex matcher (B side)
    brute.py               enumeration helpers for solver B (completions, day lists, epoch minutes, integer cents)
    lexicon.py             operator lexicon registry: form -> semantic id, unit tests, 2/2 or 3/3 admission (G-LEX)
    distractors.py         options from named error models; label-blind gold position and rank; abstain checks
    choiceplan.py          choice-row display plan drawn at SAMPLING time from the row key: k, abstain display,
                           abstain gold 1/k, gold position, gold length rank; realize(); plan_report()
    polarity.py            yes/no wording polarity rule P1-P4 (negations incl. negative predicates; contracted
                           frames); screen(ctx, plugin); pipeline G-LEX safety net (opt in: POLARITY_CHECK)
    cards.py               compact rule cards: place_rules (yes/no -> row.card), CardSpec / CardItem variants with
                           variant_problems, draw_style (short <= G0 share), split_rules, token_report
    plugin.py              THE PLUGIN CONTRACT + validate_plugin() + check_independence()
    rows.py                row assembly (spec 2.4 + meta.c2), validate_row(), G15 bridge (formats-1 loader_check)
    relations.py           relation emitter (complement, minimal-edit twin, equiv, inv, premise removal) + G-TW
    gsl.py                 G-SL slot lint / fact-lock
    g3h.py                 G3-H LLM round-trip comparison
    g5h.py                 G5-H two blind reads + Claude adjudication queue
    chunker.py             Haiku task chunks (TEACH-0 pattern: gold-free, opaque ids, <= 50 items)
    audit.py               file-access auditor for Haiku task agents
    pipeline.py            build_unit(): one relation unit through G2, G3, G4, G-SL, G-LEX, G-TW, G15 in memory
    reference/             R00, the complete reference plugin (kit example: never written, never trained)
      r00.py  r00_solver_b.py  r00_fixtures.py  G0_LITE_R00.md
    tests/                 unit tests (in memory only)
```

Reused read-only (never edited): `c_src/common/negcount.py` (negation counts for G-SL, G-TW and Mode F),
`c_src/formats/formats-1` (`fmt1.card.loader_check` for G15, which runs the pinned `decoder_io.py` and
`train_decoder.check_rows`).

## Run the tests

```
cd lean
../.venv/bin/python -m pytest -q c2_build/c2_kit/tests
```

## The plugin contract (what every family agent implements)

One module subclasses `c2_kit.plugin.C2Plugin`; a **separate** solver-B module holds `parse` and `solve_b`.
Copy `reference/r00.py` + `reference/r00_solver_b.py`.

### Class attributes

| Attribute | Meaning | Checked by `validate_plugin` |
|---|---|---|
| `FAMILY` | `"T28"`, ... (registry in `plugin.FAMILIES`) | in the registry, tier matches |
| `TIER` | `agent` / `everyday` / `transfer_dev` | equals the registry tier |
| `G0_LITE`, `G0_SHA256` | path of the frozen one-page G0-lite spec and its sha256 | file exists, <= 200 lines, sha matches; strict: frozen |
| `SAMPLERS`, `HELD_OUT_SAMPLERS` | `("S1".."S4"[, "S6"..], "S5")`, `("S5",)` | >= 4 training samplers + held-out S5 |
| `PARADIGM_A`, `PARADIGM_B` | from `plugin.PARADIGMS` | both valid, different |
| `SOLVER_B_MODULE` | dotted path, e.g. `"c2_t28.solver_b"` | imports; has `parse`, `solve_b`; imports no solver-A code (below) |
| `QFORMS` | `{qform: QuestionForm}` | ids match; every complement form has a positive form; strict: >= 1 complement form, >= 1 non-syntactic |
| `LABEL_WORDS` | gold-label words (never in skins) | non-empty |
| `CLOSED_WORLD_SENTENCE` | printed on every card that carries complements | non-empty; G-TW checks it is in both rows |
| `REGISTERS`, `HELD_OUT_REGISTERS` | >= 8, of which >= 2 held out | strict |
| `GSL_EXCEPTIONS` | `{word: reason}`: EXTENDED lint words the G0-lite spec allows | never a CORE (spec-listed) word |
| `NAME_ALLOW` | capitalised non-name words skins may use (pack glossary) | |

`QuestionForm(qform, qtype, predicate="", polarity=1, complement_kind=None, yes_is_bad=None, answer_set="closed",
abstain=False)`: `qtype` is `"noul"` (yes/no) or `"choice"`; a yes/no form names its `predicate`; a complement form
has `polarity=-1` and `complement_kind` in `syntactic | antonym | option_framing | implicit`; yes/no never abstains.

### Methods

| Method | Contract |
|---|---|
| `__init__(self, lexicon=None)` | keep the family's frozen `LexiconRegistry` (sample() draws admitted forms from it) |
| `sample(self, seed: int, sampler: str) -> Spec` | draw structure, typed slots and the question form; every display choice label-blind (seeded from the seed, never from the gold); call `self.derive(spec)` before returning |
| `solve_a(self, spec) -> answer` | solver A. Yes/no: `1` or `0`. Choice: the option KEY (canonical value: ISO date, rule id, verdict id) |
| `canonical(self, spec) -> dict` | JSON-able facts a correct parse of the rendered row returns (the G3 target) |
| `canonical_for(self, spec, author_mode) -> dict` | optional: the G3 target for a Mode F row (narrative-only facts move to G3-H). Default: `canonical(spec)` |
| `render(self, spec, ctx, *, skin=None, wording=None, forms=None, attack=None) -> RenderedRow` | build state / instructions / card with `rows.TextBuilder` from `skin.fill(...)` pieces and program templates; options with `distractors.build_options` / `build_closed`; finish with `rows.assemble_row(...)`. `skin` / `wording` None: `ctx.pick(...)` (label-blind); `forms` None: `plugin.choose_forms(spec, key)` |
| `relations(self, spec) -> [RelationProposal]` | overlay and G4 proposals (below) |
| `error_models(self) -> {name: ErrorModel}` | every wrong option comes from one of these; names from `distractors.CATALOG` or `register_name(name, describe)` |
| `derive(self, spec) -> Spec` | optional: recompute printed intermediates (`spec.derived`, `spec.derived_deps`) after an input changed |
| `extract_view(spec)`, `extract_fields(spec)` | Mode F families: the facts G3-H must recover and their `g3h.Field` schema |

Solver-B module (`SOLVER_B_MODULE`):

| Function | Contract |
|---|---|
| `parse(row: dict, ctx: KitCtx) -> dict` | read the RENDERED row back into `canonical_for(spec, mode)` (own regexes for program text; `skin.parse_skin` / `skin.match_template` for skins; `ctx.lexicon.parse_exact(..., admitted_only=True)` for clauses). On choice rows also return `"options"`: the key of every option text, in row order |
| `solve_b(view: dict) -> answer` | the gold in another paradigm, from the parsed view only |

`check_independence` refuses a solver-B module that imports the plugin's module, `c2_kit.rules` or `c2_kit.glob_a`, or
uses the names `solve_a`, `fill`, `fill_freeform`, `render`, `evaluate`, `evaluate3`, `resolve`. It reads the B
module's own source (direct imports); keep B in its own file.

### Data classes

- `Spec(family, sampler, seed, card_id, qform, slots, structure={}, derived={}, derived_deps={}, closed_world=True,
  depth=0, deep=False, tags=(), pack=None, persona_seed=None)`. `slots` are the input facts (`{name: Slot}`);
  `structure` is JSON-able and refers to slots by name; `spec.with_slot(name, slot)` makes a twin (None removes a
  premise); `spec.replace(...)`; `spec.env()`; `spec.structure_hash()`.
- `RenderedRow(row, spans, forms, option_set, skin_id, wording_id, attack_id, register, regions)`; `rr.answer` is the
  gold key.
- `RelationProposal(kind, spec=None, qform=None, changed_slot=None, expect=None, register=None, attack=None, note="")`:
  - `complement`: `qform` = the partner question form (same predicate, opposite polarity);
  - `twin`: `spec` = the twin spec (exactly one input slot changed), `changed_slot`, `expect` = the predicted answer
    **from the construction** (never from `solve_a`);
  - `premise_removal`: `spec` without `changed_slot`, `expect` = the abstain key;
  - `equiv`: optional `register` (or `spec` with the same facts);
  - `inv`: optional `attack` skin id;
  - `metamorphic` (G4, never emitted): `spec`, `expect` = `"same"` or the predicted answer.
  A relation unit (complement / equiv / inv partners plus the base) holds at most 3 rows.
- `KitCtx(skins={id: Skin}, lexicon=LexiconRegistry)`; `ctx.pick(family, kind, row_key, register=, qform=,
  exclude=, held_out=)`.

### Slots, skins and lexicon in one paragraph

Every value, name, date, number and lexicon clause reaches text through a typed `Slot` (`slots.date_slot`,
`datetime_slot` (fixed UTC offset only), `cents_slot` (int), `count_slot(n, unit)`, `category_slot(key, set)`,
`id_slot`, `glob_slot`, `url_slot` (reserved hosts), `name_slot`, and `lexicon.clause(form_id, bind)`). Skins are
`skin.make_skin(id, family, text, {SLOT: kind}, kind="skin"|"wording"|"attack"|"program", register=, escape=,
author_mode="T"|"F", counts=, qform=, brief=, haiku_task_id=, haiku_prompt_sha=, lexicon_ids=, held_out=)`. The
program picks forms label-blind (`choose_forms`: one style per kind per row, free forms only); a template pins context
forms (`{AMT:int_cents}`, `{N:adj}`). Question wordings are admitted lexicon forms of kind `question` with sem
`lexicon.question_sem(family, qform)`.

## Stage B pilot fixes at kit level (14 Oct 2026; STAGE_B_PILOT_REPORT "patterns across families")

All three are opt in: a family that calls nothing new gets byte-identical rows (checked on 5 pilots).

**1. Abstain gold and option balance: `choiceplan` + `build_options(plan=...)`.** The abstain / "none" option was
gold far below 1/k (T35 24/184 vs 54; T30 49/387 vs 129; T36 48/331 vs 97), failing G6 options-only, G7 and G10
longest-option. Draw the plan first, from the row key, then build structure to reach it (label-first; gold from
solver A; never relabelled):

```python
from c2_kit.choiceplan import plan_choice, realize, plan_report, PlanMismatch
plan = plan_choice(row_key, ks=(3, 4), abstain=True)            # open set; closed sets: closed=len(labels)
# sample(): target outcome = abstain iff plan.gold_abstain; draw structure until solver A agrees and the options fit
spec, _ = realize(plan, draw, solve=self.solve_a, abstain_key=NONE_KEY,
                  fits=lambda s, g: build_options(s, g, models, plan=plan, ...) is not None)
# render(): same row key -> same plan
os_ = build_options(spec, gold, models, plan=plan, row_key=row_key, render_key=..., abstain=(NONE_KEY, NONE_TEXT),
                    length_balance=True, strict_plan=<base row>)   # twins / premise removal: strict_plan=False
```

Abstain gold is 1/k in every (k, shown) cell, the gold position and its visible-length rank are uniform, and
gold-is-longest is 1/k whatever the abstain text's length. `abstain_slot="last"` keeps the abstain option last with
every position still 1/k. `plan_report(option_sets)` measures the same views the pilot gates do.

**2. Length: `cards`.** The served prompt prints `row.instructions` twice and `row.card` once (yes/no rows only). Put
yes/no rules in `row.card` with `place_rules`, add compact phrasings (`CardItem.compact`, checked by
`variant_problems`), and a short style on <= the G0's share (`draw_style`). Solver-B parsers read the rules with
`split_rules(row)`. `token_report(rows)` gives the mean, the mean after placement and the rules ratio still needed.

**3. Wording polarity: `polarity`** (T35 G5-H: 3 wrong golds from "is it not the case that they do not bar ...").
Set `POLARITY_CHECK = True` and `POLARITY_NEGATIVES` (the family's negative / antonym predicates); call
`polarity.form_problems(plugin, qform, text)` in the wording admission check and `polarity.screen(ctx, plugin)` from
the plugin's `ctx_for`; `pipeline.check_rendered` then reports any failing wording that reaches a row as G-LEX.

## Gates in this folder

| Gate | Code | Bar |
|---|---|---|
| G2, G3, G4, G15, schema | `pipeline.build_unit` / `check_rendered` | 100% (a failure drops the whole unit) |
| G-SL | `gsl.lint_template` (Mode T, by role), `gsl.lint_freeform` (Mode F), `gsl.lint_values`; `gsl.check_row` per row | 100% |
| G-LEX | `lexicon.LexiconRegistry.unit_test`, `record_extraction`, `status`, `gate`; `pipeline.lex_problems` per row | every used form admitted (2/2; 3/3 for precedence and window) |
| G-TW | `relations.RelationEmitter` (`complement`, `twin`, `equiv`, `inv`, `premise_removal`, `finalize`) | 100% |
| G3-H | `g3h.extraction_item`, `compare`, `template_report` | >= 98% per template, else quarantine; mismatches dropped |
| G5-H | `g5h.make_reads`, `score`, `adjudication_items`, `finalize` | 0 confirmed wrong golds; ambiguous <= 1%; > 3% template disagreement quarantines |

`pipeline.overlay_report(units, plugin)` measures the spec 4.1 shares (complement >= 20% of yes/no rows, >= 30%
non-syntactic, twins, equiv, attack), the yes rate, abstain and gold positions.

## Haiku task flow (after A38 only)

1. Build items (gold-free): `g5h.read_item(row)`, `g3h.extraction_item(text, fields)`, `reg.lexicon_items()`, or an
   authoring brief.
2. `chunker.make_batch(kind, family, [(internal_id, item)], seed=, prompt=, forbid_strings=LABEL_WORDS + questions)`:
   <= 50 items per chunk, opaque `q...` ids, whitelisted fields per kind, no forbidden keys, no internal ids, no
   never-open paths.
3. `paths.write_files(root, batch.files())` (refuses before A38); one fresh agent per chunk; the agent may read only
   `batch.allowed(root, task_id)`.
4. `audit.audit_jsonl(transcript, allowed_read=..., allowed_write=...)`: a failed audit discards that agent's answers.
5. `chunker.load_answers(batch, {task_id: answers})`, then the gate: `reg.record_extraction` (G-LEX), `g3h.compare`
   (G3-H), `g5h.score` -> Claude adjudication -> `g5h.finalize` (G5-H). Haiku answers only flag: they never set a label.

## Writing rows (after A38 only)

`pipeline.build_unit` returns `UnitResult(ok, rows, rels, problems)`. Write passed units only, through
`paths.write_jsonl` (rows) and the relation file in `train_decoder`'s format (`{"a", "b", "type"}`). Rows with
`meta.dev_only` (S5, held-out skins / wordings / registers) feed mixdev and transfer dev only;
`rows.validate_row(row, training=True)` refuses them.

## Known limits (by design)

- `check_independence` reads the solver-B module's direct imports and names; it cannot prove two paradigms are
  different in spirit. The G0-lite spec names both paradigms and the reviewer reads them.
- `rules.evaluate3` (Kleene) is sound, not complete: exact "cannot decide" golds use `brute.completions` over stated
  domains.
- Approximate token count (`rows.approx_tokens`, 3 characters per token) is conservative; the mixer re-checks with the
  real tokenizer.
- YAML skins may not use flow mappings with capitalised keys (`{Key: v}` reads as a placeholder); block style only.
- `article()` reads letters one by one for all-capital words (an SLA, a URL); acronyms read as words (NASA) are rare
  in generated values.
