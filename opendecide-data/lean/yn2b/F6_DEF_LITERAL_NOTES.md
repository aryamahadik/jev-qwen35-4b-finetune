# F6 `gen3_def_literal`: notes for decide2 (agent A), devx (reviewer R) and review

**Builder:** D2. **Code:** `golden_src/gen3/gen3_def_literal.py` (views, balance, writing), `dl_sample.py` (sampler),
`dl_core.py` (the labels: `decide`), `dl_render.py` (surface + the builder's own text re-score), `dl_packs.py` (data
only: packs, attributes, surface templates).

**decide2 rule (SPEC 8.1):** the decide2 author must not read `dl_core.py`, `dl_sample.py` or `gen3_def_literal.py`.
This note and `dl_packs.py` (pure data: every attribute's verb phrase, fact sentence, field label and value format)
are enough. `dl_render.py` holds the builder's own parser; reading it is allowed but an independent parser is better.

This note describes the **rendered surface only**.

**decide2 interface.** Put `decide2_row(raw_row)` in `golden_src/gen3/v3_def_literal.py`. It returns `"yes"` / `"no"`
(yes/no rows) or the option string (choice and JB rows). The builder passes each raw row with an extra `"_defs"` key:
the row's definitions dict (yes/no rows: `{"<Clause n>": <definition>, "yes": ..., "no": ...}`; choice rows: one
entry per option). For written rows the same dict is `mv_core.load_defs("gen3_def_literal", row["meta"]["defs"])`.
`gen3_def_literal.report()` then runs `mv_core.verify_labels` on every train and dev row (SPEC 8.1: 100%).

## 1. Rows

| | Train | dev_iid | dev_holdout |
|---|---|---|---|
| yes/no (incl. judge rows) | 1,100 | 54 | 54 |
| choice | 300 | 15 | 15 |
| JB-letter | 100 | 6 | 6 |
| attack twins (`inv`) | 150 | 0 | 0 |

- `meta.pack` is the pack id. The defined term is in the question and the card.
- dev_holdout uses only the held-out packs `tenancy`, `safety` and the held-out invented terms
  "Class 4 textile fibre" (customs), "Section 4 escape of water" (insurance) and "Framework B bid" (procurement), and
  the held-out question phrasing (template index 4, `meta.tpl` ends in `4`).
- Dev rows always come in gold-balanced pairs: a base row and its contrast twin (`meta.twin_of`), sometimes plus the
  "not" question on both.
- devx is not built here. R renders it from `gen3_def_literal.export_latents("devx", 100)` (section 6).

## 2. The rule every row applies (stated in the definition text itself)

A definition reads:

> `A|An <entity> is <a 'term'> only if all of the following hold: (a) the <entity> <vp>; (b) ...` (AND)
> or `... only if at least one of the following holds: (a) ...` (OR).
> `It is not <a 'term'> if the <entity> <vp>[, unless the <entity> <vp>].` then, for each further exclusion,
> `It is also not <a 'term'> if the <entity> <vp>[, unless the <entity> <vp>].` (0-2 exclusions, optional; 3 when
> the outside rule is written in as an extra exclusion. One sentence per exclusion since the R2 fix of 1 Oct: an
> 'unless' never reaches past its own sentence.)
> `A|An <entity> that|who <vp> also counts as <a 'term'> even if the listed conditions are not met[, provided no
> exclusion applies].` (0-1 deeming clause, optional)
> `A fact the file does not record counts as not established.`

- The term applies iff (the elements hold: all for AND, at least one for OR) or (the deeming clause holds), and no
  exclusion applies.
- An exclusion applies iff its trigger is established and its `unless` part is not established.
- A condition on a value the file does not record ("not recorded" / "The file does not record ...") is not
  established: an element is not met, an exclusion trigger does not apply, an `unless` part does not rescue.
- Everything else in the state is data: everyday-usage statements, true outside facts (botany, food storage), rules
  of other rule books ("Under <rule book>, a <entity> that ... is (not) treated as <a 'term'>."), notes, and attack
  plants in the notes. None of them changes the outcome.
- Items never have two independent sufficient reasons (both AND-paths and the deeming clause, two failing AND
  elements, an element failing and an exclusion applying, ...).
- `<vp>` comes from the attribute's template in `dl_packs.py` (`Attr.vp` with `{op}` and `{x}` for num / date,
  `{list}` for cat; `vp_true` / `vp_false` for flags). Operator words: num `at least` (>=), `more than` (>), `at most`
  or `no more than` (<=, per attribute), `less than` or `fewer than` (<, per attribute); dates `on or before`,
  `before`, `on or after`, `after`. Category lists are `x`, `x or y`, `x, y or z` (membership). Values are integers
  in the attribute's unit format (`dl_packs.UNITS`, or `noun:<singular>|<plural>`); dates are `D Month 2026`.

## 3. Where the definition is

| qkind | Definition | Question | Gold |
|---|---|---|---|
| `yn` | card line `- <Clause n>: <definition>` (printed before `- yes:` / `- no:`) | `is` (base), `not` (ladder), `judge`, `judge_n` templates (`dl_render.Q`) | is: term applies; not: it does not; judge: the recorded classification equals the definition's outcome; judge_n: it does not |
| `choice` | the options: `Requirement - the <entity> <vp>` (one per element; AND only), `Exclusion - the <entity> <vp>[, unless the <entity> <vp>]`, and `Every condition is satisfied` (always last) | `choice` templates | the unique failing condition (an unmet requirement or an applying exclusion), else `Every condition is satisfied` |
| `jb` | the state: file field `governing definition` (json / kv / markdown), sentence `The governing definition is <Clause n> of the <instrument> (in force from <date>): <definition>` (prose) or line `Governing definition, <Clause n> ... : <definition>` (email) | `jb` templates with the family wording; `jbf` templates (claim-stating: `... does the <entity> count as <a 'term'>?`, `Is the <entity> <a 'term'> under the definition in <Clause n>?`, ...) with the fallback pair (R2 fix) | option 0 (`The <entity> is <a 'term'> under <Clause n>.` or `yes, this holds`) iff the term applies |

The judge record: file field `recorded classification: <a 'term'> | not <a 'term'>` (json / kv / markdown), sentence
`The <register> records the <entity> as <...>.` (prose), or an automatic message `Recorded classification for this
file: <...>.` (email).

## 4. State layout (`meta.fmt`: json, markdown, kv, prose, email)

Every state has four parts: the file (reference, opened date, officer, neutral file details, and the JB definition or
judge record when present), the entity (a description, then one field per shown attribute in display order: the
value in the attribute's unit format, `yes`/`no` for flags, or `not recorded`), background (statements the definition
ignores), and notes (the untrusted sub-field; attack plants are appended there).

| fmt | Layout |
|---|---|
| json | `json.dumps(indent=1)` of `{"file": {...}, "<entity>": {"description", <label>: <value>, ...}, "background": [...], "notes": [...]}`; the top-level key set is fixed per pack |
| markdown | `## File`, `## <Entity>` (bullets `- <label>: <value>`), `## Background`, `## Notes` (bullets) |
| kv | `file.<k>: v`, `<entity>.<label>: <value>`, `background.<i>: ...`, `notes.<i>: ...` |
| prose | 4 paragraphs: file sentences; the entity's description sentence and one fact sentence per attribute (`Attr.fact`, `fact_true` / `fact_false`, or `The file does not record <Attr.what>.`); `Background: ...`; `Notes on the file: ...` |
| email | message 1 from the officer (subject `File <ref>`): `Opened on ...`, file details, the JB definition line, the description and one fact sentence per line; optional register message; `Background` message; `File notes` message; an attack plant is a last message (subject `Re: file notes`) |

## 5. Views and relations

- `contrast` (`meta.twin_of`): one decisive atom flips, so gold flips. Element twin: one attribute value changes.
  Exclusion twin (yes/no rows only): the outside rule shown in the background is written into the definition (or
  removed), and the file reference differs.
- `ladder` (complement): the `not` / `judge_n` question on the same state.
- `base` with role `para` and renderer `<fmt>+bg` (equiv): the outside rule appears in the background only; gold stays.
- `format` (equiv): the same latent in another format.
- `attack` (inv; role `attacked`): a counter-definition in the notes ("... '<term>' means a <entity> that <vp> ...");
  50% argue for the gold answer and 50% against it; gold never changes. No marker spoofing in F6.

## 6. devx latents (reviewer R)

`gen3_def_literal.export_latents("devx", 100)` returns dicts with `latent_id`, `split`, `tier`, `facts` (the latent:
pack, term, entity, joiner, elements, exclusions [{trigger, unless}], deem, outside {regime, cond, effect},
r_card, r_facts, values {attr: value | null}, order, usage {text, verdict}, neutral, filler, notes, record,
item / description / officer / ref / clause_no / in_force / opened), `definition_text`, `decisions` (`is`, `not`,
`jb`, `judge` when a record exists, `choice` as a condition tag when defined) and `proposition` / `truth` (also used
by F4(b) for train latents). A condition is `{"attr", "kind", "op", "limit"}` (num / date; dates are day-of-2026
indexes, `dl_packs.day()`), `{"attr", "kind": "cat", "values"}` or `{"attr", "kind": "flag", "want"}`. The outside
rule always holds for the item; `r_card` means it is written into the definition (excl: as an extra exclusion, incl:
as the deeming clause). Labels must come from `decisions` (the shared `decide()`).

## 7. R2 review fixes (1 Oct 2026; yn2b/r2_def_literal_gate.json, r2_def_literal_blind.json)

Labels never changed meaning; every fix closes a reading under which a careful reader could reach the other answer, or
a cue that predicted the answer.

- **One sentence per exclusion.** `It is not T if A, unless B; nor if C` let a reader carry 'unless B' over to C (38
  train + 2 dev rows changed answer under that reading). Definitions now print `It is not T if A, unless B. It is also
  not T if C.` (dl_render.definition_text / parse_definition, v3_def_literal grammar).
- **JB fallback pair needs a claim.** 'yes, this holds' / 'no, this does not hold' under 'Which statement fits ...?'
  left 'this' without a referent (18 train + 4 dev rows). Fallback rows now use `dl_render.Q['jbf']` (meta.tpl
  `jbf<k>`, index 4 held out as before); decide2 rejects the fallback pair under a question that states no claim.
- **Coherent fact patterns** (dl_sample.incoherent; the sampler rejects, twins skip): months at the property and the
  move-in date are never shown together (dl_packs.EXCLUSIVE_ATTRS); club membership <= age - 8; sports residence <= age,
  academy <= age - 6; an occupant under 17 is not on the lease, pays no rent, parks no vehicle and is the tenant's child
  or sibling; months at the property <= 12 x age; working hours lost >= 8 x (days off - 1); no date fact (plus its
  reporting delay) after the day the file was opened (opened is moved after them); filler dates (site visit, review
  start, visit) fall on or after the opening; the JB 'in force from' day precedes every date the pack can state.
- **Deeming clause balanced.** A deeming clause predicted 'the term applies' on 69% of train rows (it came from the
  deem / rincl plans, which are all 'yes'). Items that do not count now carry a failing deeming clause as often
  (dl_sample.DEEM_FALSE): 54% after the fix.
- **No outside-rule echo in choice rows.** A written-in outside rule (rexcl) repeated in the background named the gold
  option (100% on 4.7% of choice rows); choice rows now keep it in the option lines only.
