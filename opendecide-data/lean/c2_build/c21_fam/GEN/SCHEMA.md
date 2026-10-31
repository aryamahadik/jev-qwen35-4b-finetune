# GEN row schema (for solver B and the wording-pool authors). Written by the solver-A builder, 18 Oct 2026.

Solver B (a separate session) receives the GEN G0-lite, the Opus rulings addendum and THIS file only. It never receives
solver A's code, the wording pool or any generated row's `spec`. B works from `stem` + `options` alone, and returns for
each candidate row (1) the answer option text and (2) a parse-back object (below).

## 1. Row fields (JSON, one object per row)

| field | type | meaning |
|---|---|---|
| schema | str | "gen-row-1" |
| row_id | str | `<FORM>-<split>-<index>` (pair partner has suffix `b`) |
| family | str | "GEN" |
| sub_block, form, k | str, str, int | ARITH / LOGIC / CAUSAL / TEMPORAL / TABLE; one of the 20 form ids; option count (2, 3 or 4) |
| split | str | "train" or "dev" (dev rows come only from domains D23/D24 and wording group 9) |
| domain_id, carrier | str | domain id (D01-D24); carrier id from the frozen allow-list (TXT-* for fact blocks, TBL-* for tables) |
| stem | str | the self-contained question text. This is what B reads. Options are NOT inside it |
| options | list[str] | option texts, already shuffled |
| label, label_letter | int, str | index of the correct option (0-based) and its letter A-D |
| answer_text | str | text of the correct option |
| option_meta | list | per option `{text, trap_type, correct}`; trap_type is null for the correct option |
| spec | object | generator world state (A's input to its solver). NOT given to B |
| render_map | list | `{slot, value, start, end, role, kind}` character spans inside `stem` |
| decision_spans | list | `{text, start, end, role, kind}`; role in {number, entity, negation} (G10); no AUTHORITY in GEN |
| voice_eligible | bool | AR-F1, AR-F2, TM-T1, TM-T2 prose stems of at most 60 words |
| wording | object | `{key, idx, group}`: question wording pool key, index, group (idx mod 10; group 9 is dev only) |
| pair_id, pair_role | str/null | minimal pair id and "a" / "b" |
| difficulty | object | `{bin, score}`, bin in easy / mid / hard, by program only |
| tokens_est | int | conservative token estimate (digits one token each) |
| names | object | row-start-guard names block: `{policy:[], tool:[], language:[], runner:[], carrier:[<one id>]}` |
| name_provenance, name_seed, namespace_fingerprint, provisional_names | | how every identifier was drawn (namespace.py, TRAINING salt) |
| weight | float | always 1.0 (no hard-bin upweight on GEN) |
| pool_sha, pool_testonly, spec_sha, seed | | provenance |

## 2. Question semantics B must implement (from the G0-lite)

All questions are closed-world: only the stem text and the declared unit conversions / calendar rules.
- ARITH: quantities have exact decimal values (at most 2 decimals) and units. Ops: add, sub (always a minus b), min, max,
  mul (by an integer), div (exact), pct ("p percent of"), split (ratio r1 to r2, first or second share), conv (unit
  conversion by the fixed factors: kilogram 1000 gram, kilometre 1000 metre, minute 60 s, hour 60 min, day 24 h, week 7 d),
  round (four stated rules: nearest whole number halves up, one decimal halves up, down to whole, up to whole).
  AR-F1: value of the final quantity (option text = number plus unit). AR-F2: threshold test with comparator at least / at
  most / more than / less than. AR-F3: a worked solution; each line shows `name = expression = value`; the answer is the first
  line whose expression differs from the stated step or whose value is not what its stated inputs give (later lines follow
  through from the earlier wrong value and are not wrong).
- LOGIC: facts and rules over named entities and unary predicates (and one optional binary relation). Rule bodies are
  conjunctions of positive atoms; heads are one literal (positive or negative). Entailed = true in every model of the stated
  facts and rules; Contradicted = its negation is entailed; Undetermined otherwise. LG-L2: exactly one option is entailed.
  LG-L3: items in positions 1..n, constraints before / immediately before / position equals / position not / adjacent / not adjacent;
  exactly one option satisfies all. LG-L4: yes iff entailed.
- CAUSAL: every variable is a whole number 0..7. CA-C1: forced value (do) with the stated functions and stated root values.
  CA-C2: functions plus "its own hidden input, mod 8" and a full record; abduct the hidden inputs from the record, then force
  the variable. CA-C3: role by DIRECT arrows (confounder Z->T and Z->O; mediator T->Z and Z->O; collider T->Z and O->Z; else none).
  CA-C4: valid backdoor adjustment set (no member is a descendant of T; every path from T to O starting with an arrow into T
  is blocked). CA-C5: yes iff X and Y are d-separated given the listed variables.
- TEMPORAL: proleptic Gregorian, 24-hour clock, fixed UTC offsets. TM-T1: apply the offsets in order; month step uses the stated
  clamp / roll-over rule; business days exclude the stated weekend days and holidays and do not count the start day.
  TM-T2: duration between two timestamps in absolute time, in the stated format. TM-T3: half-open intervals; relations are
  disjoint with a gap / touching end to start / partial overlap / one contains the other. TM-T4: plan = tasks with durations and
  prerequisites, unlimited parallel workers, feasible iff all work can finish inside the window; or two bookings overlap
  (half-open).
- TABLE: serialised tables (carrier id in `carrier`). B1 aggregate over filtered rows (avg rounded to 2 decimals half up); B2 the
  entry ranked first by the stated aggregate per group (no ties exist); B3 inner join of the two tables on the stated key then
  filter and aggregate (dimension values repeat per joined row); B4 True / False of the stated claim.

## 3. Parse-back object (gate G-A2)
B returns, for each row, an object equal to `canon.canonical_spec(row.spec)` (see `canon.py` docstring): a name-keyed form of
the world state with no generator ids. Keys per form family:
- ARITH `{form, count_noun, bases:[{name,value,unit}], steps:[{out,op,args,param}], final, [f2:{cmp,thr}], [f3_lines:[{out,op,args,param,value,unit}]]}`
- LOGIC `{form, entities, preds, rel, facts:[{atom,sign}], rules:[{kind,body,head:{pred,sign}}], query | options}`; L3 `{form, items, constraints:[{t,a,[b],[pos]}]}`
- CAUSAL C1/C2 `{form, vars, functions:{var:{parents,kind,...}}, do:{var,val}, target, roots | observed}`; C3-C5 `{form, vars, edges (sorted), ...}`
- TEMPORAL and TABLE: as in `canon.py` (timestamps `{date,hm,off}`, tables with column names/types and rows).
Numbers are strings in canonical row format (integers without decimals, otherwise at most 2 decimals, no trailing zeros except one).

## 4. Option text formats (so B can match its answer)
AR-F1 `<number> <unit plural>` (count units use the row's count noun); AR-F2 Yes / No; AR-F3 `Line <n>`; LG-L1 Entailed / Contradicted / Undetermined;
LG-L2 `<Entity> is [not ]a <predicate>`; LG-L3 comma list of items in position order; LG-L4 `Yes, it follows` / `No, it does not follow`;
CA-C1/C2 a digit 0-7; CA-C3 a role word; CA-C4 `{a, b}` with names sorted, `{}` for the empty set; CA-C5 Yes / No;
TM-T1 ISO date; TM-T2 `<d> days <h> hours <m> minutes` | `<h> hours <m> minutes` | `<m> minutes` (singular at 1);
TM-T3 one of the four relation words; TM-T4 Yes / No; TB-B1/B3 number; TB-B2 a group or entity value; TB-B4 True / False.
Agreement is compared after `builder.norm_option` (lower case, single spaces, numbers re-printed canonically).

## 5. Wording pool interface (for the Haiku authors; the generator code does not write wordings)
A pool is `{key: [template, ...]}`. A template uses `{slot}` fields only, with no other braces. Every template must contain ALL the
slots listed for its key (checked by `gen_common.check_pool`). Question keys need at least 56 entries (at least 50 TRAIN wordings in
groups 0-8 plus at least 1 dev-group wording; entry i is in group i mod 10, group 9 is dev only). Recommended 64 train + 6 dev for
every question key and 70 train for AR-F1 and TB-B1, because the per-wording cap of 2 percent is applied on rows and minimal pairs
reuse one wording twice. Wordings must be original, plain, must not follow any recorded A61(a) source frame, and must state the
slot content exactly as given (no rephrasing of numbers, names or dates).

| key | required slots | min entries |
|---|---|---|
| q.AR-F1 | final | 56 |
| q.AR-F2 | final, cmp, thr | 56 |
| q.AR-F3 | n | 56 |
| q.LG-L1 | query | 56 |
| q.LG-L2 | (none) | 56 |
| q.LG-L3 | (none) | 56 |
| q.LG-L4 | query | 56 |
| q.CA-C1 | target, do_var, do_val | 56 |
| q.CA-C2 | target, do_var, do_val | 56 |
| q.CA-C3 | z, t, o | 56 |
| q.CA-C4 | t, o | 56 |
| q.CA-C5 | x, y, zset | 56 |
| q.TM-T1 | start, offset | 56 |
| q.TM-T2 | t1, t2, fmt | 56 |
| q.TM-T3 | iv1, iv2 | 56 |
| q.TM-T4 | (none) | 56 |
| q.TM-T4.overlap | b1, b2 | 56 |
| q.TB-B1 | agg, col, cond | 56 |
| q.TB-B2 | rank_phrase | 56 |
| q.TB-B3 | agg, col, cond | 56 |
| q.TB-B4 | claim | 56 |
| scene.D01 | (none) | 4 |
| scene.D02 | (none) | 4 |
| scene.D03 | (none) | 4 |
| scene.D04 | (none) | 4 |
| scene.D05 | (none) | 4 |
| scene.D06 | (none) | 4 |
| scene.D07 | (none) | 4 |
| scene.D08 | (none) | 4 |
| scene.D09 | (none) | 4 |
| scene.D10 | (none) | 4 |
| scene.D11 | (none) | 4 |
| scene.D12 | (none) | 4 |
| scene.D13 | (none) | 4 |
| scene.D14 | (none) | 4 |
| scene.D15 | (none) | 4 |
| scene.D16 | (none) | 4 |
| scene.D17 | (none) | 4 |
| scene.D18 | (none) | 4 |
| scene.D19 | (none) | 4 |
| scene.D20 | (none) | 4 |
| scene.D21 | (none) | 4 |
| scene.D22 | (none) | 4 |
| scene.D23 | (none) | 4 |
| scene.D24 | (none) | 4 |
| ar.base | name, qty | 4 |
| ar.step.add | out, args | 4 |
| ar.step.sub | out, a, b | 4 |
| ar.step.mul | out, a, p | 4 |
| ar.step.div | out, a, p | 4 |
| ar.step.pct | out, a, p | 4 |
| ar.step.split | out, a, r1, r2, which | 4 |
| ar.step.min | out, args | 4 |
| ar.step.max | out, args | 4 |
| ar.step.conv | out, a, unit | 4 |
| ar.step.round | out, a, rule | 4 |
| ar.f3.line | n, text | 6 |
| lg.rules_only | (none) | 2 |
| lg.fact.pos | e, pred | 4 |
| lg.fact.neg | e, pred | 4 |
| lg.rel.fact | e1, rel, e2 | 4 |
| lg.rule.pos | body, head | 4 |
| lg.rule.neg | body, head | 4 |
| lg.rule.rel | body, head | 4 |
| lg.l3.intro | items | 4 |
| lg.l3.c.before | a, b | 4 |
| lg.l3.c.imm_before | a, b | 4 |
| lg.l3.c.pos_eq | a, pos | 4 |
| lg.l3.c.pos_neq | a, pos | 4 |
| lg.l3.c.not_adjacent | a, b | 4 |
| lg.l3.c.adjacent | a, b | 4 |
| ca.intro | vars | 4 |
| ca.edge | a, b | 4 |
| ca.root | v, val | 4 |
| ca.fn | v, fn | 4 |
| ca.fn.noise | v, fn | 4 |
| ca.obs | v, val | 4 |
| ca.indep | (none) | 2 |
| ca.def_roles | (none) | 2 |
| ca.model_closed | (none) | 2 |
| tm.calendar_rule | (none) | 2 |
| tm.rule.clamp | (none) | 2 |
| tm.rule.roll | (none) | 2 |
| tm.weekend | days | 2 |
| tm.holidays | dates | 2 |
| tm.no_holidays | (none) | 2 |
| tm.iv.def | (none) | 2 |
| tm.interval | name, start, end | 4 |
| tm.task | name, dur, after | 4 |
| tm.task.noafter | name, dur | 4 |
| tm.window | start, end | 2 |
| tm.booking | name, start, end | 4 |
| tm.ts | name, ts | 4 |
| tb.intro | tables | 4 |
| tb.table_label | label | 2 |
| tb.rounding | (none) | 2 |

Fact sentences are chosen at random from their key; question wordings are assigned by least-used with a per-wording cap.


## 6. Skeptic additions (18 Oct 2026; the build skeptic of lane L-G)

- STEM CONTRACT. A stem starts with exactly ONE scene sentence that carries no data (no digit, no `=`, no inner full stop); solver B drops it as the
  scene. The legacy test tag "Scene D07-3." is read the same way. Everything after the scene is facts, then the question sentence(s) last.
- QUESTION READING. Solver B reads the question with the question wording templates (`solver_b/question_templates.json`, a copy of the question half
  of the wording pool made by `export_question_templates.py`; a test fails when it is stale). Each template is matched at the END of the stem at a
  sentence start; the slot values come out of the match; two readings with different slots are refused (`ambiguous_question`). The facts are read by
  B's own frames. Slot shapes: names are letters / digits / underscore; `cmp` one of "at least / at most / more than / less than"; `thr` "<number> <unit>";
  `offset` "<n> <unit>[, then <n> <unit>]"; `fmt` one of three phrases; `zset` "nothing" or a name list; `query` "<Entity> is [not] a <predicate>".
- PREDICATES. `pred_source` in the spec is "ns" (nonsense stems from the TRAINING namespace) or "vocab" (a closed per-domain role phrase from
  `pools/predicate_vocab.json`, hyphen and apostrophe allowed, none of the words is, a, an, and, not, to, that, it, if, then, something, anything).
  About half of the LG-L1 / L2 / L4 rows use the vocabulary. Vocabulary phrases are not namespace names; `builder.spec_names` leaves them out.
- TRAP TYPES. A trap type ending `+slip` is a compound slip (the base error model plus a small independent miscount on the form's own lattice: one to
  seven days, five to 120 minutes). Added so that no wrong option shares a fixed offset or residue with the correct one.
- NO NEGATED RELATION FACT. A relation fact is stated positively only (`lg.rel.fact` has no negative wording); a spec with a negated relation fact is
  refused by the renderer. (A pair edit used to flip one, so the stem said the opposite of the spec.)
- CHECK AT CREATION. Rows leave the generator only through `row_check.build_checked` (see its docstring): A = B on the text, parse-back, spans, format
  and shortcut probes, guards, pair closure, G13 hook, stamp record. `pad_invariance` and the A21 length tiers are NOT BUILT; a row that carries a `pad`
  field is refused.
- ADVERSARIAL FILTER. In rows mode the builder screens every 4-option candidate (all forms except CA-C3 and TM-T3, whose four option texts are the same
  in every row) against two detectors trained on the candidates seen so far (`adversary.py`; features `heuristics.option_features`, the same function the
  option-only probe uses). It only accepts or rejects an item; it never edits a label or an option.
- STATED ASSUMPTIONS. Two assumptions that decide the gold used to be unstated. Every TM-T4 plan stem now says tasks may run in parallel (`tm.parallel`,
  2 wordings; B refuses a plan stem without it), and every TB-B3 stem says which columns are joined (`tb.join`, 2 wordings; B reads the key from the
  sentence instead of inferring it). TB-B4 claims are printed inside double quotes (the claim has its own "is").
- TEMPLATE METADATA (A1). Every row stores `template_id` ("<form>|<carrier>|<question key>"), `wording_id` ("<question key>#<index>"), `operator_ids`
  (sorted operator / mechanism ids from the spec), `error_model_ids` (the trap types of the wrong options) and `level` / `length_tier` (both null: the ladder
  and the A21 padding are not built).
