# G0-LITE: T54 TOOL-NEED/PICK (clean-room, 4,000 rows)

Status: DRAFT by Sonnet 5.5 (high), Sun 18 Oct 2026, for Opus G0-lite approval Mon 19 Oct. Design only: no rows, no
generator run, no data, no model call. Every numeric bar below is written BEFORE any pilot and is fixed once Opus approves.
Sources read: PLAN_TRAINING_SIDE.md (sections 1 B.5, 1 E, 2, 5, 8), LANE_L-T.md, excerpts/tools_s5.md (stripped).
Text in angle brackets such as <slot> is a design placeholder, never a data string.

## 0. One-line purpose

Teach the one-token readout to decide, for a tool-using agent turn: call a tool, ask the user, say no tool fits, or answer
directly; and to pick the right tool among distractors, ground the arguments it supplies, notice when a tool, a parameter
or a tool result is missing, notice when a write is already satisfied, and tell what may run in parallel.

## 1. Decision and label set

Every row is one multiple-choice question with lettered options (options shuffled per row; 20% extra copies with a random
non-identity permutation are made at mix time and are NOT counted in the 4,000). Six sub-blocks, each with its own label set.

| Sub-block | Question | Labels (gold space) | k |
|---|---|---|---|
| S1 NEED4 | What should the agent do next? | CALL / ASK / NO_TOOL / ANSWER | 4 |
| S2 PICK | Which listed tool (with its argument skeleton) is the right call? | one of 4 shortlisted candidates | 4 |
| S3 LIMIT | Same question as S1 after a deletion (see 3.3) | CALL / NO_TOOL / ASK / RESULT_MISSING | 4 |
| S4 PRECOND | Is the write needed, given what is known? | WRITE / READ_FIRST / DONE_NO_CALL / ASK | 4 |
| S5 ARGGROUND | Is every value in the proposed call grounded in context? | GROUNDED / UNGROUNDED | 2 |
| S6 PARSEQ | Which set of calls may be issued together in the next step? | one of 4 candidate sets | 4 |

Label meanings (our own wording, not borrowed from any benchmark):
- CALL: all required arguments have a source (user turn, earlier tool output, or a default the active card allows) and a
  listed tool fits. NO_TOOL: no listed tool can do the job (tell the user, do not improvise). ASK: a listed tool fits but a
  required argument has no source. ANSWER: the question needs no tool (answerable from context or general knowledge the card
  allows). RESULT_MISSING: the next call needs a value that an earlier tool result should have supplied, and that result is
  absent from context (say so; never invent the value).
- WRITE / READ_FIRST / DONE_NO_CALL / ASK in S4: write now; call a read tool first; the wanted state is already established,
  so no write; ask.

Secondary head: none in P0 (T54 stays a single-readout family). A reason string is NOT trained.

## 2. Inputs and state model

INPUT VIEW. Primary = system tool-use card + tool list + user messages + earlier tool calls, tool OUTPUTS STRIPPED.
Labelled variant "with tool outputs" (outputs capped at 256 tokens each) is REQUIRED for the rows whose gold depends on an
output: S3-RESULT rows and S4 rows with observed state; they carry the variant tag in the header. Tool outputs are rendered
from a data-field grammar only (no sentences addressed to the agent); the T41c taint rule applies: a CPU lint refuses any output
text containing an imperative or second-person clause (family hands injection-style content to T41c, not here).

SCENARIO ENGINE (shared with T55/T56; module names only): tool_engine.dag, tool_engine.state, tool_engine.render,
tool_engine.perturb, tool_engine.wording. The engine builds, per scenario:
1. An archetype (section 8 NAMES) and a seeded namespace of entity nouns (TRAINING salt).
2. A tool set: N tools = 1 target + D distractors; each tool has verb, entity noun, typed parameters (required/optional,
   default or not), a read/write flag, an idempotent flag, and an equivalence-group id (used ONLY for dedup of options).
3. A knowledge state K per parameter value and per world fact: source in {user_turn, prior_tool_output, card_default,
   none}; world facts in {observed_true, observed_false, unobserved}.
4. A dependency DAG over the calls the request implies (S6): node = call, edge = "argument consumes another call's output".
5. A perturbation: none, or one deletion {tool, parameter, result} or a null-deletion control (an irrelevant element removed).
6. The active card (section 8) which fixes how defaults, read-before-write and batching are treated.

DISTRACTOR COUNT is a free design parameter chosen here (no public benchmark sets it): D in [1, 24], N = D + 1 in [2, 25].
| N bin | share of rows | purpose |
|---|---|---|
| 2-3 | 20% | trivial, anchors |
| 4-6 | 30% | |
| 7-10 | 25% | |
| 11-16 | 15% | |
| 17-25 | 10% | stress; the 10% allowed to reach the 1,536 cap |
Hard negatives (S2 and all CALL rows): >= 40% of rows with N >= 4 carry >= 1 SAME-NAMESPACE hard negative (same entity noun,
different verb, near-identical description) and >= 20% carry a SAME-VERB hard negative (different entity noun). Parameter-name
overlap distractors in >= 15% of rows. These shares are CPU-checked (gate P-9).

## 3. Gold method

### 3.1 Principle
Generate-then-render. Each row starts as a structured scenario record; the label is a pure function of the record; text is
rendered from the record; Haiku (later, medium) only REWORDS prompts under a slot round-trip check. No LLM writes a label.

### 3.2 Rule tables (deterministic; the whole of the gold)
S1 NEED4, evaluated in order, first match wins, under the active card:
1. if no listed tool fits the intent (target tool absent from the list) -> NO_TOOL (only when the intent is a tool-shaped task);
2. else if the intent is non-tool-shaped (information already in context or definitional) -> ANSWER;
3. else if any required parameter has source none, and the card does not allow its default -> ASK;
4. else CALL.
Card effect: card.t54.strict_ask never uses defaults (rule 3 fires for any required parameter with source none, even if the
parameter has a declared default); card.t54.defaults_ok lets declared defaults count as a source. The same scenario under the
two cards yields a gold flip in a controlled slice (section 4, pair type C).
Intent type (tool-shaped vs not) is a scenario attribute set by the template, and the template must make it observable (the
request asks for an action or fetch vs asks about something already stated or definitional). Near-miss ANSWER rows carry a
tool list containing a tool that could be called but is not needed because the answer is in context.

S2 PICK: gold = the tool whose (verb, entity, parameter schema) satisfies the request spec; exactly one listed tool satisfies
it (the generator asserts uniqueness via the equivalence-group id; two satisfying tools -> row rejected). Options are 4
shortlisted tools: gold + 3 chosen from the candidate pool (>= 1 same-namespace hard negative in >= 50% of rows).

S3 LIMIT (deletion): start from an intact S1-CALL scenario and delete one element.
- TOOL deleted: the target tool is removed from the list (distractors stay) -> NO_TOOL.
- PARAMETER deleted: the source of one required parameter is removed from the request (value never stated, not derivable) -> ASK.
- RESULT deleted: an earlier call that should have supplied a required value is shown with its output absent (call present,
  output missing from context) -> RESULT_MISSING.
- Intact twin: the same scenario with the element present -> CALL.
- Null-deletion control: an element NOT on the path of the intent is removed (an unused distractor tool, an optional
  parameter, an unneeded earlier output) -> still CALL.
Idea credited to CAR-bench (removal idea only; we copy no item, tool name, schema or wording).

S4 PRECOND (state K from section 2; write tool W, read tool R_W, idempotent flag I):
- world fact observed_true -> DONE_NO_CALL
- observed_false -> WRITE (if all required arguments sourced, else ASK)
- unobserved and W idempotent -> WRITE
- unobserved, W not idempotent, a read tool for that fact is listed -> READ_FIRST
- unobserved, W not idempotent, no read tool -> ASK
The card card.t54.read_before_write is active on all S4 rows; the three non-trivial branches are shuffled across archetypes.

S5 ARGGROUND: for the proposed call, each supplied value has a provenance label from the engine. GROUNDED iff every supplied
value is one of: stated in a user turn, present in an earlier tool output (same role/field, not merely the same string in
another role), or a card-allowed default, or a declared transformation of a grounded value (case, whitespace, ordinal word <->
digit, a unit conversion the card declares). UNGROUNDED iff >= 1 supplied value has no source or has a source of the wrong role
(a value that appears only as a different entity's field). Argument grounding of supplied values stays OUR OWN metric
(no public claim).

S6 PARSEQ: gold = the set of calls that are READY at the current step, i.e. nodes whose argument inputs consume no
not-yet-obtained output (topological level 0 of the remaining DAG), with substitutable tools (equivalence groups) canonicalised
to their group id. Options: the correct ready set; a too-small set (serialises independent calls); a too-large set (includes
a call that consumes a missing output); a set with a wrong-but-ready member. The generator asserts that exactly one option
equals the ready set after canonicalisation (no two correct options).

### 3.3 Solver A vs independent solver B
- Solver A (builder, Sonnet high): the gold function inside the generator, reading the structured record.
- Solver B (separate Sonnet high session, written from THIS FILE only, never from generator code): re-implements the rule
  tables from section 3.2 as a standalone module over the serialised record (not the rendered prompt). For S6 it computes
  levels by a different algorithm from A (A = Kahn's levels; B = memoised longest-path depth).
- Render-fidelity check: B also runs a deterministic parser over the RENDERED prompt (regex/slot extraction, no model) to
  recover the record fields the rules need; rows where the re-parsed record changes the label are dropped and counted.
- Agreement rule: rows with A != B are dropped and logged. Pilot disagreement above 1.0% of rows means the spec is
  ambiguous: that is the family's fix iteration (Opus rules on the spec change).
- Execution gold: none needed (no code is run); all gold is program-computed from the record.

## 4. Sizes and shares

Total 4,000 rows. Shares are exact targets; tolerance +-2 pp of the family unless stated.
| Sub-block | Rows | Share | Label mix (of the sub-block) | Matched-pair rows |
|---|---|---|---|---|
| S1 NEED4 | 1,000 | 25.0% | CALL 48 / ASK 17 / NO_TOOL 17 / ANSWER 18 | >= 50% |
| S2 PICK | 800 | 20.0% | gold letter uniform (25% each, +-2 pp); gold tool position uniform within N bin | >= 40% (hard-negative swaps) |
| S3 LIMIT | 800 | 20.0% | deleted 360 (TOOL 120 / PARAM 120 / RESULT 120), intact twins 320, null controls 120; CALL 55% | 80% (paired) |
| S4 PRECOND | 500 | 12.5% | WRITE 28 / READ_FIRST 24 / DONE_NO_CALL 28 / ASK 20 | >= 60% |
| S5 ARGGROUND | 500 | 12.5% | GROUNDED 50 / UNGROUNDED 50 | >= 70% |
| S6 PARSEQ | 400 | 10.0% | gold letter uniform; ready-set size 1 / 2 / 3+ = 30 / 40 / 30 | >= 30% |
Family-level minimal pairs >= 30% required; design gives about 60%. Pair types: A = request edit (value stated vs omitted,
length and span-count matched), B = tool-list edit (target present vs deleted), C = card edit (strict_ask vs defaults_ok on
the same scenario), D = state edit (observed vs unobserved fact), E = provenance edit (value appears vs not).
Non-Python / language mix: not applicable (no code).
Call/no-call definition: a row is call-bearing iff gold is CALL, WRITE or READ_FIRST (S1, S3, S4). S2, S5, S6 have no no-call
arm and carry their own balance gates (P-7).
Token budget: mean <= 800, hard cap 1,536 on <= 10% of rows (cap rows are the N 17-25 bin), rows above 1,024 tokens <= 10%.
Wordings: >= 50 wordings per question form (a form = sub-block x card x variant tag), no wording above 2% of the family.

## 5. Gates

Bars (written now, before any pilot). Binary probes pass at held-out AUC <= 0.55 with 95% upper bound <= 0.60. k-way probes
pass at balanced accuracy <= 1/k + 3 pp with 95% upper bound <= 1/k + 6 pp (balanced accuracy = mean per-class recall,
because labels are not uniform in S1, S3, S4). Protocol for every probe: grouped split (all members of a pair and all
rows of a scenario-template id stay together), 80/20, five repeats with different group seeds; mean score reported; the 95%
bound is the 97.5th percentile of a 2,000-resample cluster bootstrap over held-out groups (stricter than one-sided).
Probe model: TF-IDF (1-2 grams, min_df 3) + L2 logistic regression, C chosen by inner CV on the train groups.

### 5.1 PRE-FREEZE KILL gates (CPU, data only)
| ID | Gate | Bar |
|---|---|---|
| P-1 | Solver A vs B agreement on the 1,000-row pilot and on full generation | 100% target; rows A != B dropped; pilot disagreement > 1.0% = fix iteration |
| P-2 | Sub-block sizes and label mixes vs section 4 | within +-2 pp (family) / +-3 pp (label mix) |
| P-3 | Call/no-call share per sub-block (S1, S3, S4) | each 40-60% call-bearing; also each (sub-block x card x N-bin) cell with >= 100 rows within 35-65% |
| P-4 | Limit-awareness block present | S3 = 20.0% of family; TOOL, PARAM, RESULT deletions each 33.3% +-3 pp of deleted rows; each deleted row has an intact twin in >= 85% of cases; null controls = 15% of S3 |
| P-5a | Probe: request-only text -> call-bearing (binary), on S1, S3, S4 each | AUC <= 0.55, bound <= 0.60 |
| P-5b | Probe: tool-list/card text only (request removed) -> call-bearing (binary) | AUC <= 0.55, bound <= 0.60 |
| P-5c | Probe: structural counts (token length, N, D, parameter count, option-letter, turn count, wording id, template id) -> label | binary AUC <= 0.55 / bound <= 0.60; 4-way balanced acc <= 28% / bound <= 31% |
| P-5d | Probe on S5: request+context text -> GROUNDED (binary), length and span-count matched pairs | AUC <= 0.55, bound <= 0.60 |
| P-5e | Probe on S2: option text only (no request) -> gold option (4-way) | balanced acc <= 28% / bound <= 31% |
| P-6 | Value-bearing span count (numbers, quoted strings, ids, dates in the request) histogram, call-bearing vs no-call | total-variation distance <= 0.05 |
| P-7 | Gold-letter share (k=4 sub-blocks) and S5 yes-rate | letters 25% +-2 pp; S5 yes 45-55%; S2 gold position per N bin within +-5 pp of 1/N (N<=8) or within +-3 pp per decile (N>8) |
| P-8 | Resolvable-reference parity: rows whose request refers to a value only by pronoun/"the same one" and the value IS in context (gold CALL) vs is NOT (gold ASK) | share of reference-phrased rows within 45-55% CALL |
| P-9 | Distractor design: N-bin shares, same-namespace and same-verb hard-negative shares, parameter overlap | within +-2 pp of section 2 |
| P-10 | Token budget | mean <= 800; max <= 1,536; > 1,024 tokens on <= 10% of rows |
| P-11 | Wording: >= 50 forms, no wording > 2%, no template > 2%; Haiku reword slot round trip (every slot value, number, id, negation survives) | 100% slot survival else drop-only |
| P-12 | Minimal pairs share | >= 30% (design ~60%) |
| P-13 | Name guard: 100% of tool, parameter, card, carrier, archetype names in rows are on the frozen allow-list; namespace nouns not on the deny-list program; 0 exact matches to G13 target strings | 0 violations |
| P-14 | Output lint: no imperative/second-person text in rendered tool outputs | 0 violations |
| P-15 | 200-row G13 pilot (orchestrator, serial on the Mac) | <= 1% of rows hit by any method; a hit traced ONLY to sha-bound product-format scaffolding is exempt |
| P-16 | Collisions with frozen OHS-5 | dropped row by row; <= 5% of the family is NOT the fix iteration, > 5% is |

STANDARD PIPELINE gates (A50 G6 at size, A49c balance, G5-H blind reads, G3-H) are orchestrator-run and not redefined here.
FLAG FOR OPUS: G5-H/G3-H use Haiku readers on the DATA (label audits), not the trained C2.1. Read literally, "no model-based
gate is a kill rule before the data freeze" could make them report-only; the plan lists them as pipeline gates that can send
a family to its fix iteration. This G0-lite treats them as data-audit gates per the plan and asks Opus to confirm.

### 5.2 POST-TRAINING REPORT (needs the trained C2.1; never a kill rule)
| ID | Report line | Pre-registered comparison |
|---|---|---|
| R-1 | CALL/NO-CALL BIAS on a held-out balanced set: per-class recall for call-bearing and no-call; logit offset between the two option groups | floor: each class recall >= 80% and not more than 2 pp below the init model; margin: |recall_call - recall_nocall| <= 8 pp; offset (mean log-odds shift that equalises recall) <= 0.50 nats. Fixed here before any pilot; Opus may adjust before approval |
| R-2 | Accuracy per sub-block with Wilson CI, next to baselines: always-CALL, always-ASK, majority label, keyword baseline (request-token rules), random, and the base 4B | each reported, never a bare accuracy |
| R-3 | Per N bin accuracy (distractor-count curve), and hard-negative slice accuracy | report |
| R-4 | Flip rate under random non-identity option permutation, with CI | report; 1% dev target is a metric, not a claim |
| R-5 | ECE (bin count stated), Brier, trap-slice ECE | report |
| R-6 | Over-calling rate (CALL where gold is ASK/NO_TOOL/ANSWER) and under-calling rate separately | report |
| R-7 | S5 argument grounding appears only on OHS-5 as "our items" | no public claim |

## 6. Clean-room notes

- Builder never opens any T27, T40-T46 generator, template or wording pool, OHS-AC, or any benchmark item text. This file was
  written from the plan and the stripped excerpt only.
- Names: every tool, parameter-entity, entity, archetype-entity and card title in a row is drawn from the seeded random
  namespace with the TRAINING salt; no hand-picked fake names. The only fixed vocabulary is the closed verb list and the
  closed generic parameter-role list in section 8 (generic English words, listed in the manifest).
- Idea credits (ideas only; no strings, schemas, ID formats or wording copied): CAR-bench (removal of tool/parameter/result),
  ToolMaze (DAG levels as parallel gold), LIMBO is T55's. When2Call is NOT used as data and its label wording is not reused; the
  four-answer idea is generic. BFCL, tau/tau2, MCP-Atlas, MCP-Bench, MCP-Universe, ToolHop, CAR-bench tool names, ToolMaze
  trajectories: G13 targets; domain archetypes here are generic structural kinds, not those benchmarks' domain names.
- Tool schemas are Claude-authored from engine parameters; no human-written MCP schema is used.
- Haiku only rewords prompts and card text, never writes labels or schemas.
- No external source in P0: manifest entry "no external source".
- Scenario templates are Claude-authored by the builder under G13 literal ban enforced by program; writers never see the ban list;
  hit reports carry row ids, target name and method only.

## 7. Risks

1. Surface cues in the request (vagueness, missing detail) predict ASK: mitigated by span-count matching (P-6), resolvable-
   reference rows (P-8), request-only probes (P-5a). If P-5a fails the fix is a template-level span-matching change.
2. S1 uses 4 labels with CALL at 48%, so a lazy CALL bias is rewarded; R-1/R-6 report it, and S3 pairs force the contrast.
3. Cards: if the active card is not read, strict_ask vs defaults_ok pairs look identical; pair type C (about 6% of rows) forces
   card sensitivity. Risk: model ignores the card; reported as card-flip accuracy in R-2.
4. Token budget: N up to 25 with schemas can overshoot; mitigated by a compact schema render (one-line description, typed
   parameters) and the 10% bin limit. If P-10 fails, the fix is to shrink the render, not drop the bin.
5. S4 "unobserved" branches depend on a rule (idempotent writes are written directly) that is a policy choice stated in the card;
   a reader could reasonably prefer READ_FIRST for any write. The card text states the rule; ambiguity risk flagged for Opus.
6. S6 canonicalisation: substitutable-tool groups must be invisible in options; a bug yields two correct options (generator
   assertion + solver B check).
7. Term overlap with benchmark-style tool verbs: closed verb list is generic; G13 pilot decides.
8. Overlap with T55 (RESULT_MISSING) and T56: separate label spaces; mix-time dedup on scenario id prefix.

## 8. NAMES (names only; for the names-only manifest; every item is an identifier, no rows)

Namespace: `ns.train` (seeded, TRAINING salt; value held by L-0, not written here). Surface nouns: pseudo-words from the
namespace, kinds `ns.noun.entity`, `ns.noun.field`; each noun reused in at most 3 scenarios; per-family disjoint hash bucket
`bucket.t54`.
- Policy / tool-use cards (4): `card.t54.strict_ask`, `card.t54.defaults_ok`, `card.t54.read_before_write`, `card.t54.parallel_ok`.
- Domain archetypes (12; structural kinds, verbalised through namespace nouns): `arch.records`, `arch.schedule`,
  `arch.messages`, `arch.files`, `arch.jobs`, `arch.inventory`, `arch.accounts`, `arch.tickets`, `arch.metrics`,
  `arch.directory`, `arch.queue`, `arch.catalogue`.
- Tool verbs (closed list, 36): `get`, `list`, `find`, `search`, `count`, `read`, `check`, `create`, `add`, `update`, `set`,
  `rename`, `move`, `copy`, `remove`, `delete`, `cancel`, `close`, `open`, `archive`, `restore`, `assign`, `merge`, `send`,
  `schedule`, `reserve`, `release`, `approve`, `reject`, `export`, `import`, `sync`, `lock`, `unlock`, `tag`, `lookup`.
  Surface tool name = `<verb>_<ns.noun.entity>`.
- Generic parameter roles (closed list, 24): `id`, `key`, `name`, `count`, `limit`, `offset`, `date_from`, `date_to`, `when`,
  `amount`, `quantity`, `status`, `label`, `note`, `reason`, `query`, `scope`, `mode`, `target`, `source`, `destination`,
  `priority`, `owner`, `version`. Entity parameters = `<ns.noun.entity>_id`, `<ns.noun.field>`.
- Carriers (request/context carriers): `carrier.user_single`, `carrier.user_multi_turn`, `carrier.tool_output_prior`,
  `carrier.card_default_note`.
- Variant tags: `view.primary`, `view.with_outputs`.
- Perturbation ids: `perturb.none`, `perturb.del_tool`, `perturb.del_param`, `perturb.del_result`, `perturb.null_del`.
- Sub-block ids: `s1_need4`, `s2_pick`, `s3_limit`, `s4_precond`, `s5_argground`, `s6_parseq`.
- Languages / runners: none (no code, no execution).
- External sources: none.
- Engine modules (code names, not manifest names): `tool_engine.dag`, `.state`, `.render`, `.perturb`, `.wording`.

## 9. The one fix iteration and kill rule

- Fix iteration (one, family-level, Opus rules before it starts): triggered by ANY failed PRE-FREEZE gate in 5.1 on the pilot or
  full generation, or by a 200-row G13 pilot above 1%. Pre-declared fix menu (one change set per failed gate, no new ideas after
  the fact): P-5/P-6/P-8 fail -> re-match request length/spans at template level and regenerate the affected sub-block only;
  P-3/P-7 fail -> change sub-block label mix by program reweighting; P-10 fail -> compact schema render; P-1 fail -> Opus rules the
  spec ambiguity; P-15 fail -> back to the generator to remove the hit (method and row ids only).
- After the fix: all PRE-FREEZE gates rerun on a fresh 1,000-row pilot with new seeds. Any failure, or not through all gates by the
  DATA FREEZE (Mon 2 Nov 23:59 UTC), rolls T54 to C2.2/C3 with the failing gate and numbers logged.
- POST-TRAINING lines (5.2) never kill.
- Open question for Opus: the plan's kill rule is family-level. A proposed alternative (NOT adopted here) is to drop only a
  failing sub-block (drop-only) when the rest of the family passes and keeps >= 60% of rows. Default: strict family rule.

## 10. Items for Opus approval (checklist)

1. Cards and S4 rule on idempotent writes (risk 5). 2. R-1 floor/margin numbers. 3. Treatment of G5-H/G3-H (section 5.1 flag).
4. Call-bearing definition (S2/S5/S6 excluded from P-3). 5. Probe protocol (balanced accuracy for non-uniform k-way). 6. Token
reading ("> 1,024 tokens on <= 10%"). 7. Sub-block drop alternative.


## Opus rulings 18 Oct (appended by the L-T builder from families/G0_APPROVALS.md, word for word; the build skeptic checks the code against this addendum; where the body text above says otherwise, this addendum binds)

### Round 1 decision for this family (verbatim)

### T54 TOOL-NEED/PICK: APPROVE

Binding condition C1 (gold must be program-checkable): ANSWER gold only when the answer content is present in the
rendered context or card, and a program locates it (a span or fact id in the record). Delete "general knowledge the card
allows" from the label meaning. A "definitional" ANSWER must point to a card or context span.
Rulings: 1. the idempotent-write rule (S4: unobserved + idempotent = WRITE) is approved as a card-stated policy. 2. R-1
floor and margin are approved as written (recall >= 80% per class, <= 2 pp below init, |gap| <= 8 pp, offset <= 0.50
nats; post-training report). 3. see G2. 4. the call-bearing definition is approved (S2, S5 and S6 use their own balance
gates). 5. see G5 (already compliant). 6. see G6 (already compliant). 7. sub-block drop is not adopted (G4).

### Round 2 (verbatim lines that concern this family)

| T54, T55, T56, T56g, T42c, T57, GEN, VOICE | APPROVE (round 1 stands) | n/a | none new; the round-1 addendum is NOT yet in any of the 8 files (see below) |

- All 8: "Solver B = separate Sonnet high session" means CODE written by that session (G1).
- T54: the ANSWER meaning "general knowledge the card allows" (section 1) is deleted (C1). The section 9 / item 7

### Global rulings that bind every family (verbatim)

## Global rulings (bind every family; each family addendum cites them by number)

G1 SOLVER B IS A PROGRAM. In every family, "solver B = separate Sonnet session" means CODE written by a separate Sonnet
high session from the G0-lite (and the row schema) only. No LLM reads rows one by one to produce or check labels. LLM
reads (G5-H, G3-H, A43(d)) are audits: they never set or change a gold label. A confirmed defect is fixed in the generator
or the rule table, never by relabelling a row.

G2 DATA-AUDIT GATES ARE PRE-FREEZE. A50 G6, A49c, G5-H, G3-H and A43(d) read data, not a trained C2.1 model, so they are
PRE-FREEZE gates under the standard pipeline. Skeptic 6 bars only gates that need the TRAINED model. A G5-H flag counts
only after Sonnet medium adjudication and Opus A43(d) confirmation, and (where the family has a program solver) after a
program re-run reproduces it. Their bars are the values in the A50/A49c/G5-H/G3-H records, supplied by L-0. (Answers T50
O4, T51 O3, T53 O4, T41c O6, the T54/T55/T56 flag, GEN point 2, VOICE V-H1.)

G3 NO FREE PILOT TUNING. The 1,000-row pilot is the first measured look at every PRE-FREEZE gate. Run the family's CPU
gates and its 200-row G13 pilot on that first pilot, then make ONE combined fix if anything fails: that is the fix
iteration. Changing generator parameters after seeing pilot gate numbers and "re-running for free" is not allowed. Before
the pilot, defects found by unit tests, the build skeptic or solver A/B disagreement on CPU test fixtures are build fixes.
The plan's two exemptions stay (scaffolding-only G13 hits; OHS-5 collision drops up to 5%). (Answers T42c (d), T57 (f),
T56g (f).)

G4 KILL GRANULARITY. P0 families are killed or kept as a whole (plan section 8). The only split the plan names is T56
(done-claim half) / T56g. No sub-block or head "rolls alone" in C2.1. If an orchestrator wants that, it is a plan change
for the orchestrator, not a G0-lite choice. GEN (not a P0 family, no floor) may roll sub-blocks alone (GEN point 3
approved). VOICE keeps its lane rule. (Answers T54 item 7, T55, T56, T57 (g).)

G5 ONE PROBE HARNESS. L-0 builds one CPU probe harness for all families, and every family uses it with its own features
and groups:
- grouped split by the family's pair/spec/module/task group (no group in both train and held-out);
- L2 logistic regression with fixed or inner-CV regularisation (never tuned on held-out);
- AUC is reported as max(AUC, 1 - AUC);
- the upper bound is the 97.5th percentile of 2,000 cluster-bootstrap resamples over held-out groups (the stricter
  reading of "95% upper bound"; T50, T51 and T53 change from the one-sided 95th percentile);
- k-way probes use balanced accuracy (mean per-class recall) against 1/k + 3 pp and 1/k + 6 pp;
- every probe run includes a label-permutation sanity check (AUC 0.50 +- 0.03) and an injected-leak power check (as T41c
  K7: a planted one-feature leak must reach AUC >= 0.80), else the run is invalid and is repeated (not a fix iteration).
GBT probes are advisory in every family except GEN, where both probe models count as written (a GEN gate passes only if
both pass). The GEN/VOICE "confirm rule" (one re-run on a fresh sample twice the size, and the re-run decides) is
approved for GEN and VOICE only, because they run about 40 probes each. It is recorded and is not a fix iteration.

G6 TOKEN RULE READING. Mean <= 800 tokens per family; no row above 1,536; rows above 1,024 tokens <= 10% of the family.
T50 and T41c change their 1,000 line to 1,024.

G7 SECONDARY HEADS. The loss is on option letters and C2's layout is kept (plan section 5). A secondary head (T50
reason+tier, T53 reason+tier, T56 reason, T57 reason) is built as HEAD ROWS: the same rendered context with a separate
question form and its own lettered options, gold from the same rule table, in the same split as its primary row. Head
rows are extra copies outside the family size and come from at most 25% of the family's specs per head. They get the
family's k-way probe bars. If L-0 finds that C2's layout cannot carry a second question form, the head stays a manifest
field plus a report line. No new output token or suffix field is added. T51 violation_set stays metadata only (O1).

G8 SHARED NAMES. L-0 keeps ONE host-TLD list and ONE raw-IP pool in the names-only manifest, used by T50, T51, T53 and
T41c alike: reserved TLDs plus a generic list, and documentation/private IP ranges, with the deny-list collision check
against real brands and registered names. T41c moves from its reserved-only list to the shared list. This keeps the
families from showing a "which family am I" cue.

G9 CROSS-FAMILY LABEL CONSISTENCY. The same action in the same state under the same card must get the same label in
every family. L-A owns ONE shared effects-to-label table (in T50/G0_LITE.md section 3) that T51 and T53 cite instead of
restating their own rule. A CPU test runs every T50 spec whose effect class overlaps T51 (shared/production-lane mutation)
or T53 (egress) through the other family's engine and asserts equal labels. It must pass 100% before any pilot. T41c is a
carrier-directive decision, not an action gate, so it is not in this test, but its HARD/SOFT list must not contradict the
shared table (spot-checked by the L-I build skeptic).

G10 VOICE METADATA EXPORT. Every family with a natural-language user utterance (T50, T51, T53, T41c, T54, T55, T56 task
statements, GEN voice-eligible forms) exports `decision_spans` with a ROLE per span. Roles: negation/polarity, number,
entity/path/flag, and AUTHORITY. AUTHORITY marks any span whose presence in the user turn creates or limits permission:
consent naming, scope declarations, boundaries, delegation pointers, values whose source is the user turn. Families also
export `spoken_view` where they have one. L-0 routes this. It is a code requirement, not a gate.
