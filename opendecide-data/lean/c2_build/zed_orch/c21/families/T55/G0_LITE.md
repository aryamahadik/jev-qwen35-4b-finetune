# G0-LITE: T55 RECOVER-ESCALATE (clean-room, 3,000 rows)

Status: DRAFT by Sonnet 5.5 (high), Sun 18 Oct 2026, for Opus G0-lite approval Mon 19 Oct. Design only: no rows, no
generator run, no data, no model call. All numeric bars are written before any pilot. Angle brackets are placeholders.
Sources read: PLAN_TRAINING_SIDE.md (sections 1 B.6, 1 E, 2, 5, 8), LANE_L-T.md, excerpts/tools_s5.md (stripped).

## 0. One-line purpose

After a tool call goes wrong or looks wrong, decide the next move: retry, fix the arguments, switch tool, ask, or stop;
handle writes whose outcome is unknown without duplicating them; spot a result that is well-formed but violates an
invariant; decide deny-and-continue versus escalate after repeated denials; and tell a stuck loop from legitimate polling.

## 1. Decision and label set

One multiple-choice question per row, lettered options shuffled per row (20% extra non-identity-permutation copies at mix
time are not counted). Six sub-blocks.

| Sub-block | Option set (k) | Gold labels used |
|---|---|---|
| B1 CLASSIC (explicit errors) | RETRY / FIX_ARGS / SWITCH_TOOL / ASK / STOP (5) | all five |
| B2 AMBIGUOUS-WRITE | RETRY_KEYED / READ_BACK / RETRY_PLAIN / ASK / NO_RETRY (5) | all five (see 3.3) |
| B3 IMPLICIT-ERROR | ACCEPT / RETRY / FIX_ARGS / SWITCH_TOOL / ASK (5) | all five |
| B4 BLIND-RETRY pairs | RETRY / FIX_ARGS / SWITCH_TOOL / ASK / STOP (5) | FIX_ARGS, SWITCH_TOOL, ASK (STOP and RETRY as distractors; also gold in a minority, see 4) |
| B5 DENY-ESCALATE | CONTINUE_ALT / ESCALATE / RETRY_SAME / STOP (4) | CONTINUE_ALT, ESCALATE, STOP (RETRY_SAME distractor-only) |
| B6 LOOP-POLL | KEEP_POLLING / BREAK_LOOP_ALT / ESCALATE / STOP (4) | all four |

Label meanings (own wording): RETRY = repeat the same call; FIX_ARGS = repeat with corrected arguments; SWITCH_TOOL = use a
different listed tool for the same goal; ASK = hand a question to the user or a human reviewer; STOP = give up on this goal and
report. RETRY_KEYED = repeat the same write with the same idempotency key; READ_BACK = read state to learn whether the write
committed; RETRY_PLAIN = repeat the write as a new attempt; NO_RETRY = the effect is confirmed, do not repeat. ACCEPT = use the
result as is. CONTINUE_ALT = after a denial, take a different permitted path. ESCALATE = stop acting and ask. KEEP_POLLING = the
repeat is legitimate waiting. BREAK_LOOP_ALT = change approach.

Secondary head: none in P0. A reason head is NOT trained.

## 2. Inputs and state model

INPUT VIEW. The error or odd result is the content of the question, so T55 uses the "with tool outputs" view as its primary
view (user messages + tool calls + the relevant tool outputs, each capped at 256 tokens; at most the last 4 turns of outputs).
The tool-outputs-stripped variant exists only for B5 (denial counters are stated in the card state block, not an output) and
is tagged `view.primary`. All outputs are rendered from a data-field grammar: `status class`, `code`, `retry_after`, `field`,
`detail` keys with value slots; NO imperative or second-person clauses (CPU lint, gate P-14); advice-like hints are never
rendered (that content belongs to T41c's taint rules).

SCENARIO ENGINE (shared with T54/T56; module names only): tool_engine.dag, .state, .ledger, .invariants, .perturb, .render,
.wording.
State per scenario:
1. Archetype and namespace nouns (TRAINING salt), a tool list of 3-12 tools with read/write and idempotent flags, equivalence
   groups (SWITCH_TOOL needs an alternative: equivalence group size >= 2 listed), optional idempotency-key parameter, optional
   read tool for the affected fact.
2. A card (section 8) fixing: retry cap per tool call (R_cap in {2, 3}), whether reads may be retried freely, the escalation table
   mapping error classes to ASK or STOP, and denial thresholds for B5.
3. An attempt history: attempt index a, previous outcomes, previous arguments.
4. A LEDGER (B2): the engine knows, hidden from the row, whether the write committed (c in {T, F}); the ledger lists committed
   effects with keys; a read tool returns ledger content when listed.
5. A perturbation manifest on the 2x2 explicit/implicit x transient/permanent plus the ambiguous-write class (section 3.1). The
   transient/permanent split is NEVER a hidden flag: the row must make the cause observable (error class token, retry_after
   field, attempt history, repeated violation), so the label is a function of visible facts only.

## 3. Gold method

### 3.1 Perturbation manifest
| Axis | Values |
|---|---|
| surface | explicit (error status shown), implicit (well-formed success shape, invariant violated), ambiguous (timeout/lost acknowledgement) |
| persistence (visible) | first occurrence, recurrence (attempt history shows the same fault), declared-permanent (error class) |
| error class (explicit) | `transient_unavailable`, `rate_limited` (with retry_after), `auth_denied`, `invalid_named_arg`, `invalid_unnamed`, `unsupported_op`, `quota_exhausted`, `irrecoverable` |
| implicit violation types (NOT named in the card) | `empty_when_count_stated`, `negative_value`, `id_not_in_prior_list`, `parts_total_mismatch`, `duplicate_in_unique_list`, `order_violation`, `scale_mismatch`, `stale_echo` (result echoes earlier arguments, not the current ones) |
The card never lists the implicit violation types. Detection beyond a mined vocabulary is only ~46% in the cited work, so
generation uses types the model is not told about; two violation types are held out of training for a post-training generalisation report.
Message channel mixing: the error class is carried by one, two or three of {code field, phrase, structured hint field}; 30% of
rows use a single channel, so reading is required.

### 3.2 Rule tables (the whole of the gold)
B1 CLASSIC (first match; facts all visible):
1. class in {transient_unavailable, rate_limited} and a < R_cap and (tool is read, or idempotent, or key offered) -> RETRY.
2. same classes and a >= R_cap -> SWITCH_TOOL if an equivalent tool is listed, else ASK.
3. same classes, tool is a non-idempotent write with no key (outcome unclear) -> goes to B2 (not B1); B1 never uses it.
4. invalid_named_arg and the corrected value is available in context -> FIX_ARGS; corrected value NOT available -> ASK.
5. invalid_unnamed -> SWITCH_TOOL if an equivalent tool is listed, else ASK.
6. auth_denied -> ASK (the user can supply authority); never RETRY.
7. unsupported_op -> SWITCH_TOOL if equivalent listed, else STOP if the card marks no user remedy, else ASK.
8. quota_exhausted -> SWITCH_TOOL if equivalent listed, else per card escalation table (ASK or STOP).
9. irrecoverable (target destroyed, goal impossible by declaration) -> STOP.
The card escalation table is a 3-line table shown in the card; it assigns each of {quota_exhausted, unsupported_op} to ASK or STOP.

B4 BLIND-RETRY pairs: same class `invalid_*`, same leading error phrase and code; row X appends a named-argument detail
(rule 4: FIX_ARGS or ASK), row Y has no detail (rule 5: SWITCH_TOOL or ASK). The pair edit touches only the error detail field.
A minority (15%) of pair rows set a_equal to R_cap to make STOP/ASK gold in the unnamed arm when no alternative is listed.

B3 IMPLICIT-ERROR: run the invariant checker (one checker per violation type, over the rendered result and the earlier context).
- no violation -> ACCEPT (>= 30% of B3 rows are valid results with surface oddities that are legitimate: empty list when no count was
  stated, zero quantity, equal parts, to avoid "odd shape means error").
- violation and tool is a READ and first occurrence (a = 1) -> RETRY (stale read).
- violation and tool is a READ and recurrence -> SWITCH_TOOL if equivalent listed else ASK.
- violation of type `id_not_in_prior_list` or `scale_mismatch` or `stale_echo` caused by the call's own arguments (visible: arguments differ from the
  context value) -> FIX_ARGS.
- violation and tool is a WRITE -> ASK (do not retry a write that returned an inconsistent state).
The cause attribute (arg-induced or data-induced) is visible from comparing the call's arguments with context; the engine
asserts observability.

B2 AMBIGUOUS-WRITE (ledger simulation). Worlds consistent with the visible information: W1 = "write committed", W0 = "not committed".
Visible facts: key offered (kf), read path listed (rp), idempotent (I), outcome of a read-back if already done.
- Step 1 (outcome unknown): if I or kf -> RETRY_KEYED (safe in both worlds: exactly one effect); else if rp -> READ_BACK; else ASK.
  RETRY_PLAIN is the duplicating action in W1; NO_RETRY loses the effect in W0.
- Step 2 (after read-back result is shown): committed -> NO_RETRY; absent -> RETRY_PLAIN (safe because the read proved absence).
  Step 2 read-backs are always conclusive in P0 (an inconclusive read-back is not generated; noted for C2.2).
Gold is formally the cheapest action that yields exactly one effect in every world consistent with the visible facts, computed by
simulating all five options against the ledger in both worlds. A CPU test proves the rule table equals this simulation on the full
truth table (gate P-4). Mix: Step 1 75%, Step 2 25% of B2.
Idea source: LIMBO (author-run): ledger grading and the key/read-back finding. We build our own ledger; no code is copied.

B5 DENY-ESCALATE. State block (visible) carries: consecutive denials n_c, total denials n_t in the session, window count n_w (denials among
the last W calls, W = 50 where the card uses a window), card thresholds (K_c consecutive, K_t total, K_w window count), whether an alternative
permitted path exists, and whether the goal itself is blocked by a hard rule.
- n_c >= K_c or n_t >= K_t or (window rule active and n_w >= K_w) -> ESCALATE.
- else goal blocked by hard rule -> STOP.
- else alternative permitted path exists -> CONTINUE_ALT.
- else -> ESCALATE.
Cards vary thresholds: K_c in {2, 3, 4}; K_t in {10, 20, 30} (or none); window rule on in 40% of cards with (K_w, W) in {(10, 50)}.
Two cards reproduce the published settings (3 consecutive / 20 total; 3 consecutive / 10 of the last 50), the others deliberately
differ so the model reads the card. RETRY_SAME (repeating the denied action) is never gold.

B6 LOOP-POLL. Visible: the last n calls (tool, arguments), and the value returned by each (state field `progress`, `status`, `count`).
State-change predicate over a window of m calls (m = 3..6): changed iff `progress` is strictly monotone, or `status` made a
declared transition, or a monotone counter advanced. Card gives the polling budget P_cap and the loop limit L.
- changed and calls_used < P_cap -> KEEP_POLLING.
- changed but calls_used >= P_cap -> ESCALATE.
- not changed for >= L consecutive calls and an alternative approach exists -> BREAK_LOOP_ALT.
- not changed for >= L and no alternative -> ESCALATE; not changed for >= L and the card marks the goal as non-waitable -> STOP.
- not changed for < L -> KEEP_POLLING (still within tolerance).
"Our items" only: no public eval exists; reported on OHS-5 as such. Identical (tool, arguments) is a weak signal alone, so rows include
identical calls with progress (KEEP_POLLING), identical calls without progress (loop), and cosmetically varied arguments without
progress (loop).

### 3.3 Solver A vs independent solver B
- Solver A (builder, Sonnet high): the in-generator gold function over the structured record, including the ledger simulator (all five
  options simulated in W1 and W0).
- Solver B (separate Sonnet high session, written from THIS FILE only): re-implements section 3.2 as a standalone rule evaluator,
  plus an independent EVENT-SOURCED ledger replay (replays the event log to derive effects per option) instead of A's state-machine
  simulator. For B6, B computes the state-change predicate from the rendered values by parsing, A from the record.
- Render-fidelity check: a deterministic parser over the rendered prompt recovers the visible facts; B's label on the re-parsed record
  must equal the label on the record. Mismatches are dropped and counted.
- Agreement: A != B rows dropped and logged; pilot disagreement above 1.0% is spec ambiguity and IS the fix iteration.
- Execution gold: none. No code is run.

## 4. Sizes and shares

Total 3,000 rows.
| Sub-block | Rows | Share | Label mix (of the sub-block) | Matched-pair rows |
|---|---|---|---|---|
| B1 CLASSIC | 900 | 30.0% | RETRY 20 / FIX_ARGS 20 / SWITCH_TOOL 20 / ASK 25 / STOP 15 | >= 40% (class-edit pairs with the same tool list) |
| B4 BLIND-RETRY | 400 (200 pairs) | 13.3% | per pair: X in {FIX_ARGS 80 / ASK 20}, Y in {SWITCH_TOOL 70 / ASK 20 / STOP 10} | 100% |
| B2 AMBIGUOUS-WRITE | 600 | 20.0% | RETRY_KEYED 25 / READ_BACK 25 / ASK 25 / NO_RETRY 12.5 / RETRY_PLAIN 12.5 | >= 60% (visible-fact flips: key, read path, committed) |
| B3 IMPLICIT-ERROR | 500 | 16.7% | ACCEPT 32 / RETRY 16 / FIX_ARGS 18 / SWITCH_TOOL 14 / ASK 20 | >= 50% (valid vs violating twin of the same result shape) |
| B5 DENY-ESCALATE | 300 | 10.0% | CONTINUE_ALT 40 / ESCALATE 45 / STOP 15 | >= 50% (counter flips around threshold: n_c = K_c - 1 vs K_c) |
| B6 LOOP-POLL | 300 | 10.0% | KEEP_POLLING 40 / BREAK_LOOP_ALT 25 / ESCALATE 20 / STOP 15 | >= 50% (identical calls, progress vs none) |
Family-level pairs >= 30% required; design gives about 55%. Perturbation 2x2 coverage: explicit x transient (B1 rules 1-2, B6),
explicit x permanent (B1 rules 4-9, B4, B5), implicit x transient (B3 RETRY), implicit x permanent (B3 other), ambiguous (B2).
Each cell holds >= 8% of the family.
Token budget: mean <= 800; max 1,536 on <= 10% of rows; > 1,024 tokens on <= 10% (reading to be confirmed by Opus).
Wordings: >= 50 wordings per question form, no wording > 2%.
Language mix: not applicable.

## 5. Gates

Bars: binary probes pass at held-out AUC <= 0.55 with 95% upper bound <= 0.60; k-way probes pass at balanced accuracy <= 1/k + 3 pp with
95% upper bound <= 1/k + 6 pp (k = 5: <= 23% / <= 26%; k = 4: <= 28% / <= 31%; k_eff for sub-blocks with fewer gold classes, e.g.
B5 3 gold classes: <= 36.3% / <= 39.3%). Protocol: grouped split by scenario-template id and pair id, 80/20, five repeats, 2,000-resample
cluster bootstrap 97.5th percentile as the bound; model = TF-IDF (1-2 grams, min_df 3) + L2 logistic regression.

### 5.1 PRE-FREEZE KILL gates (CPU, data only)
| ID | Gate | Bar |
|---|---|---|
| P-1 | Solver A vs B agreement (pilot and full) | 100% target; A != B dropped; pilot disagreement > 1.0% = fix iteration |
| P-2 | Sub-block sizes and label mixes | within +-2 pp (family) / +-3 pp (label mix) |
| P-3 | Perturbation manifest coverage: 2x2 cells and the ambiguous class | each cell >= 8% of family; implicit violation types >= 5% each of B3's violating rows; 2 types flagged held-out |
| P-4 | LEDGER GOLD REPRODUCES THE RULE: exhaustive truth table over (I, kf, rp, committed, step) with A's rule table vs the five-option two-world simulation vs B's event-sourced replay | 100% three-way agreement on every cell |
| P-5 | Probe: structure-only features (token length, turn count, tool-list size, option letter, wording id, template id, attempt index excluded) -> label | k=5: balanced acc <= 23% / bound <= 26%; B5/B6 k_eff as above |
| P-6 | Probe: B3 shape-only features (field names, field count, value-shape tokens with digits/words masked, length) -> violation vs valid (binary) | AUC <= 0.55, bound <= 0.60 |
| P-7 | Probe: B6 identical-call fraction alone -> KEEP_POLLING vs not (binary) | AUC <= 0.55, bound <= 0.60 (weak-signal claim checked) |
| P-8 | B4 pair check: identical code and leading phrase in both rows of a pair; only the detail field differs | 100% of pairs |
| P-9 | Channel mixing: single-channel rows share; error class channel combination balance | single-channel 28-32% of explicit-error rows; no channel combination > 40% |
| P-10 | Observability assertion: every label's required facts are visible in the rendered row (solver B parser) | 100% (else dropped; > 2% drop in pilot = fix iteration) |
| P-11 | Gold-letter share per option set | 1/k +-2 pp |
| P-12 | Token budget | mean <= 800; max <= 1,536; > 1,024 on <= 10% |
| P-13 | Wording: >= 50 forms, no wording > 2%, Haiku reword slot round trip (numbers, counters, ids, thresholds, negations survive) | 100% slot survival else drop-only |
| P-14 | Output lint: no imperative or second-person clause, no hint text addressed to the agent, in rendered outputs | 0 violations |
| P-15 | Name guard: 100% of names on the frozen allow-list; 0 exact matches to G13 target strings | 0 violations |
| P-16 | Minimal pairs share | >= 30% |
| P-17 | 200-row G13 pilot (orchestrator, serial) | <= 1% hit; scaffolding-only hits exempt |
| P-18 | Collisions with frozen OHS-5 | dropped row by row; <= 5% not the fix iteration, > 5% is |
| P-19 | Threshold diversity in B5 | each (K_c, K_t, window) card <= 25% of B5 rows; both published settings present |

Standard pipeline gates (A50 G6, A49c, G5-H, G3-H): orchestrator-run, not redefined; FLAG FOR OPUS identical to T54 (data-audit gates that use Haiku
readers; treated as pipeline gates per plan).

### 5.2 POST-TRAINING REPORT (never a kill rule)
| ID | Report line |
|---|---|
| R-1 | Accuracy per sub-block with Wilson CI beside baselines: always-ASK, always-RETRY, majority, keyword baseline on error class token, random, base 4B |
| R-2 | Duplicate-write rate (RETRY_PLAIN where gold is RETRY_KEYED/READ_BACK) and lost-write rate (NO_RETRY where gold is RETRY_PLAIN), separate |
| R-3 | Explicit-minus-implicit recovery gap (B1/B4 accuracy minus B3 accuracy on matched content) |
| R-4 | Held-out violation types: accuracy on the 2 held-out types vs in-family (gap in pp, CI) |
| R-5 | Blind-retry pair accuracy: both-correct rate on B4 pairs |
| R-6 | Flip rate under option permutation; ECE, Brier, trap-slice ECE |
| R-7 | B6 and B5 reported on OHS-5 as "our items" |

## 6. Clean-room notes

- Not built from any benchmark item. LIMBO (ledger and key/read-back idea), ToolMaze (explicit/implicit x transient/permanent
  perturbation idea; DAG enumeration), Outcome-Monitors (violated-property receipts: NOT used, since cards never name violations),
  Fission-GRPO (blind-retry premise): ideas only; no strings, ID patterns or tool names copied. Deny thresholds (3 consecutive / 20
  total; 3 consecutive / 10 of last 50) are public product facts used as card parameters, with product names kept out of rows.
- Names: seeded namespace with TRAINING salt for every tool, entity and field; closed verb and error-class vocabularies in section 8.
  No hand-picked fake names.
- Error classes are generic categories, written in the family's own `status class` field vocabulary; no wording, code table or schema is
  copied from any API reference or benchmark; G13 pilot checks it.
- Haiku rewords prompts and card text only (slot round trip), never labels.
- No external source in P0.
- Builder never opens any T27, T40-T46 generator, template, wording pool or OHS-AC.

## 7. Risks

1. B1/B3 rule tables encode policy choices (read retries are free; writes are not retried after an inconsistent result). A reader may
   prefer a different table; the card states it, but Opus must approve the tables.
2. Class-token shortcut: error class maps to label mostly deterministically in B1 (legit) but a model could ignore attempt/card facts.
   Mitigations: pair flips (attempt index, equivalent-tool presence), channel mixing, card-dependent escalation table.
3. B2 gold equals the simulated-worlds rule by construction: the rule is a policy (prefer keyed retry, then read-back, then ask). Does
   not claim a universally correct action; the card states the preference order.
4. B3 depends on observable invariants; hard types (`parts_total_mismatch`) need arithmetic in the result; token length risk.
5. B5 numeric thresholds are card parameters; risk of memorising the two published settings; P-19 caps their share.
6. STOP has few natural rows; STOP share is small by design (15%); a model might never choose STOP. Reported as per-class recall.
7. Overlap with T54 RESULT_MISSING and T56 ledger_mismatch: separate label spaces; mix-time dedup on scenario id prefix.
8. Haiku reword drift on numbers and counters: slot round trip, drop-only.

## 8. NAMES (names only; for the names-only manifest)

Namespace: `ns.train` (TRAINING salt, value held by L-0), kinds `ns.noun.entity`, `ns.noun.field`; per-family bucket `bucket.t55`;
each noun reused in at most 3 scenarios.
- Policy / escalation cards (6): `card.t55.retry_cap2`, `card.t55.retry_cap3`, `card.t55.escalate_table_ask`, `card.t55.escalate_table_stop`,
  `card.t55.denial_consec_total`, `card.t55.denial_window`. Variants carry numeric parameters (K_c, K_t, K_w, W, P_cap, L).
- Domain archetypes (10): `arch.records`, `arch.schedule`, `arch.messages`, `arch.files`, `arch.jobs`, `arch.inventory`, `arch.accounts`,
  `arch.tickets`, `arch.metrics`, `arch.queue`.
- Tool verbs (closed list, 30): `get`, `list`, `find`, `search`, `count`, `read`, `check`, `create`, `add`, `update`, `set`, `rename`, `move`,
  `copy`, `remove`, `delete`, `cancel`, `close`, `archive`, `restore`, `assign`, `merge`, `send`, `schedule`, `reserve`, `release`, `approve`,
  `export`, `sync`, `lookup`. Surface tool name = `<verb>_<ns.noun.entity>`.
- Error classes (closed list): `transient_unavailable`, `rate_limited`, `auth_denied`, `invalid_named_arg`, `invalid_unnamed`, `unsupported_op`,
  `quota_exhausted`, `irrecoverable`. Rendered through a `status class` vocabulary of our own (surface tokens drawn per row from a
  wording pool; not stored here).
- Implicit violation types (closed list): `empty_when_count_stated`, `negative_value`, `id_not_in_prior_list`, `parts_total_mismatch`,
  `duplicate_in_unique_list`, `order_violation`, `scale_mismatch`, `stale_echo`.
- Output field keys (closed list): `status`, `code`, `retry_after`, `field`, `detail`, `progress`, `count`, `items`, `total`, `key`, `committed`.
- Generic parameter roles: `id`, `key`, `name`, `count`, `limit`, `offset`, `amount`, `quantity`, `status`, `label`, `note`, `reason`,
  `query`, `scope`, `mode`, `target`, `owner`, `version`, `idempotency_key`.
- Carriers: `carrier.tool_output_error`, `carrier.tool_output_odd_success`, `carrier.tool_output_timeout`, `carrier.state_block_counters`,
  `carrier.call_history_list`.
- View tags: `view.with_outputs`, `view.primary`. Sub-block ids: `b1_classic`, `b2_ambig_write`, `b3_implicit`, `b4_blind_retry`, `b5_deny_escalate`, `b6_loop_poll`.
- Languages / runners: none. External sources: none.

## 9. The one fix iteration and kill rule

- One family-level fix iteration (Opus rules first), triggered by ANY failed PRE-FREEZE gate (5.1) on pilot or full generation or a G13 pilot
  above 1%. Pre-declared menu: P-1/P-10 fail -> Opus rules spec ambiguity and the table is amended once; P-4 fail -> ledger simulator or rule
  table corrected (this is a bug, rerun); P-5/P-6/P-7 fail -> re-balance structure/length features by template and regenerate the affected
  sub-block; P-9/P-14 fail -> renderer change; P-17 fail -> remove hit by generator change (row ids and method only).
- After the fix: rerun all PRE-FREEZE gates on a fresh 1,000-row pilot with new seeds. Any failure, or not through all gates by the DATA
  FREEZE (Mon 2 Nov 23:59 UTC), rolls T55 to C2.2/C3 with failing gate and numbers logged. POST-TRAINING lines never kill.
- Open question for Opus: sub-block drop-only alternative (as in T54); default strict family rule.

## 10. Items for Opus approval (checklist)

1. Rule tables B1/B2/B3/B5/B6 as policy choices (risk 1, 3). 2. Escalation-table cards. 3. Observability assertion P-10 and its 2% drop
tolerance. 4. B5 card thresholds (two published settings plus variants). 5. Held-out violation types (two of eight; which two is chosen by
seeded draw recorded before any pilot). 6. Probe protocol with balanced accuracy and k_eff. 7. G5-H/G3-H treatment.


## Opus rulings 18 Oct (appended by the L-T builder from families/G0_APPROVALS.md, word for word; the build skeptic checks the code against this addendum; where the body text above says otherwise, this addendum binds)

### Round 1 decision for this family (verbatim)

### T55 RECOVER-ESCALATE: APPROVE

Binding conditions (gold order fixed now, so solvers A and B cannot read it differently):
- C1 B3 is first-match in this order: (1) no violation = ACCEPT; (2) violation caused by the call's own arguments
  (visible) = FIX_ARGS; (3) violation on a WRITE = ASK; (4) READ, first occurrence = RETRY; (5) READ, recurrence =
  SWITCH_TOOL if an equivalent tool is listed, else ASK.
- C2 B6 is first-match in this order: (1) changed and calls_used < P_cap = KEEP_POLLING; (2) changed and calls_used >=
  P_cap = ESCALATE; (3) not changed for < L calls = KEEP_POLLING; (4) not changed for >= L and an alternative exists =
  BREAK_LOOP_ALT; (5) not changed for >= L and the card marks the goal non-waitable = STOP; (6) otherwise ESCALATE.
- C3 P-4 is widened. The exhaustive truth-table test (rule table = A's evaluator = B's evaluator, 100%) covers B1, B3, B5
  and B6 as well as B2.
Rulings: 1-2 the tables and escalation cards are approved with C1-C3. 3 the observability check P-10 with a 2% pilot drop
tolerance is approved. 4 the B5 thresholds are approved (both published settings present, each card <= 25%). 5 the two
held-out violation types are drawn by seeded draw before any pilot. Their rows are dev-only, outside the 3,000. 6
approved (k_eff bars as written; G5). 7 see G2. Sub-block drop is not adopted (G4). The with-tool-outputs primary view
is accepted, because the error is the content.

### Round 2 (verbatim lines that concern this family)

| T54, T55, T56, T56g, T42c, T57, GEN, VOICE | APPROVE (round 1 stands) | n/a | none new; the round-1 addendum is NOT yet in any of the 8 files (see below) |

- All 8: "Solver B = separate Sonnet high session" means CODE written by that session (G1).
- T55: the section 9 sub-block drop question is not adopted (G4). The C1-C3 gold orders go into 3.2.

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
