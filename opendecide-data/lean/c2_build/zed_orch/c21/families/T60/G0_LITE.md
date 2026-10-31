# G0-LITE T60 CONTROL-NEXT (lane L-K; P0-extra; draft for Opus approval, target Mon 19 Oct 2026)

Author: Sonnet 5.5 high, Sun 18 Oct 2026 (UTC). Read scope used: training_inputs/PLAN_TRAINING_SIDE.md (incl. section 16), training_inputs/LANE_L-K.md, training_inputs/excerpts/tools_s5.md (stripped), families/T50/G0_LITE.md and G0_ADDENDUM_v32.md, families/T51/G0_LITE.md, families/T54/G0_LITE.md and G0_ADDENDUM_v32.md, families/T55/G0_LITE.md and G0_ADDENDUM_v32.md (section 8), families/T56/G0_LITE.md (sections 1-5), families/T59/G0_LITE.md (this lane's sibling; the IRREV definition D3 is shared), families/G0_APPROVALS_v32.md (GV1-GV9), C2_1_PUBLIC_TRAIN_INVENTORY.md (section 4 rows for T59/T60), C2_1_EXTRA_LEVERS.md (A10, A12, A24), l0/NAMES_MANIFEST_V1_1.json (names only), c21_fam (file listing and function names only).
Not opened: any path containing "ohs" or "sealed", C2_1_PLAN_v3.md itself, any plan SKEPTIC file, any benchmark item text, research_v4/hardest.md (the plan says no published difficulty study exists for T60, so the ladder is program parameters only), the T27/T40-T46 generators, mutate.py, any dataset file. No rows, no generator code, nothing executed, no model or API call, no Modal.
Scope note: during orientation one search over C2_1_BUILD_ORDER.md and the sibling LANE_*.md files (outside my read list) returned only lines that name T59/T60; nothing from them is used here beyond what LANE_L-K.md already says.
Status: DRAFT. Every number below is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus. This file is the whole spec (no addendum yet); it carries the v3.2 items inline. Global rulings G1-G10 and GV1-GV9 bind and are cited by number.
Family class: P0-EXTRA (plan 16.4). Same pipeline and kill rule as P0; enters the mix if through its gates; does NOT count toward the 6-of-9 floor and cannot replace a failed P0 family.
Row family id: `T60` (already in row_job_families_allowed). Heads are `head` fields, not new family ids.

## 1. Decision and label set

Three PRIMARY heads, each a binary question with its own question form (these are not secondary heads, so G7 is not used). Options are two lettered choices, order shuffled per row; the 20% mix-time copies with a non-identity permutation equal a reversal and are NOT counted in the 2,000.
| Head | Question | Labels | Rows |
|---|---|---|---|
| H1 DELEGATE-OR-DO | should the agent hand this subtask to a separate worker with a brief, or do it itself in this thread? | DELEGATE / DO_HERE | 600 |
| H2 KEEP-OR-DROP | at the context summary, keep this fact in the summary or drop it? | KEEP / DROP | 800 |
| H3 PLAN-OR-ACT | write out a plan before acting, or act now? | PLAN / ACT | 600 |
Label meanings (own wording): DELEGATE = a self-contained, bounded, independent subtask whose size justifies a hand-off; DO_HERE = otherwise. KEEP = a step that has not run yet will take this fact from the conversation context; DROP = no remaining step takes it from context. PLAN = the task is risky and open in procedure, so a plan should come first; ACT = go ahead.
Boundaries. T60 never labels permission: no permission boundary, exclusion or "only/nothing else" fact is used (the boundary-after-compaction rows stay in T51) and no step is protected, shared-lane or production (guard K22). T60 never labels ask-or-proceed (T59 owns): every H1/H3 task is built with no open INTENT slot, so the T59 oracle returns PROCEED on it (guard K22). No reason head; head, fact type, edit field and card are manifest metadata, never rendered. Product use: the control step of a coding agent (when to spawn a worker, what to carry across a compaction, when to plan).

## 2. Inputs, state model and cards

INPUT VIEW. All heads: card + task statement + the head's own block. H1: the main-thread context (the facts the main thread holds) and the CANDIDATE SUBTASK BRIEF (its steps, the files it would read with their sizes in tokens, the output it must return and its size, the facts it needs from the main thread, the resources it writes). H2: the TASK, the REMAINING PLAN (steps tagged [done] / [todo], each [todo] step naming what it takes by a reference, section 3.4) and the CONTEXT TRANSCRIPT (user turns, calls and tool outputs, each output capped at 256 tokens, data-field grammar, no imperative or second-person text), then the FACT QUOTE (the fact with its transcript index and type). H3: the task statement and the procedure information (steps if stated, the effects of the steps). Primary view = user turns + calls; transcript outputs appear only in H2 where the fact is a tool result.
SCENARIO ENGINE (read-only imports): tool_engine.dag (T54 export: build_dag, Kahn levels), the T55 ledger simulator (tool_engine.ledger, API per T55 addendum section 8), LA_COMMON spec/state (for W-REPO shapes). World kinds as T59: W-TOOL 60% / W-REPO 40% (+-5 pp) for every head.
SPEC (`spec_k1`, shared with T59; owned by L-K), T60 fields: head; task statement; plan DAG G = (nodes, edges), node = {step id, call, status done/todo, needs (set of fact ids taken from conversation context), produces (fact ids), reads (artifact pointers), effects (T59 D3 effect records), est steps, read volume in tokens, writes (resource ids), contingency flag and its host step}; facts {id, type, value, source (user / tool), transcript index, role handle (a namespace field noun), markers}; brief {steps, read volume, needs_from_main, result size, writes, incoming edges from pending main steps}; risk spec {n steps, IRREV steps, stated dependencies, unstated dependencies}; card_ref; decision_spans (G10); pair_id, twin_of, quad cell id; lever_tag; heldout_family; ladder level and mechanisms; split (dev/train per spec family).
FACT TYPES (H2; closed): V user-stated value; R tool-result value; D decision taken earlier (a chosen option); S state marker (id or key of an effect already made); P pointer (path or handle to a persisted artifact whose CONTENT a later step reads). Content of a persisted artifact is not a fact the summary must hold: the later step reads the artifact from its pointer, so the pointer is KEPT and the content DROPPED.
CARDS (visible clause lines; display names from ns.policy_card). 10 cards.
- H1 d01-d04: `clause.t60.delegate_rule` with four visible numbers that vary across cards: S_min steps in {3, 4, 5, 6}, V read-volume tokens in {4K, 8K, 16K}, B_max facts the brief may need in {1, 2, 3}, R_max result tokens in {200, 400, 800}.
- H2 k01-k02: `clause.t60.keep_rule` ("keep a fact if a step still to run will take it from the context") plus `clause.t60.keep_recovery`: k01 says steps that only run if something fails (rollback, retry, read-back) COUNT, k02 says they do NOT count.
- H3 p01-p04: `clause.t60.plan_rule` with the visible numbers n_min in {3, 4, 5} and the stakes threshold H (3 levels, as T59).
Card-swap pairs (the same task under two cards that give different labels) force card reading: H1 40 pairs, H2 20 specs, H3 60 pairs.

## 3. Gold method

### 3.1 Principle
Generate-then-render. Each row starts as a structured spec; the label is a pure function of (spec, card); text is rendered from the spec; Haiku medium only REWORDS the task statement, user turns and descriptions under a slot round trip. No LLM writes or changes a label (G1). Nothing is executed: the plan simulator in K3 runs in process on simulated state.

### 3.2 H1 DELEGATE-OR-DO (rule table, all inputs visible)
DELEGATE iff ALL of:
- SIZE: est steps >= S_min OR read volume >= V (the brief lists its steps and the sizes of the files it reads);
- BRIEF: the number of facts the subtask needs from the main thread <= B_max (each costs a line in the hand-off; more means doing it here is cheaper);
- BOUND: the result the main thread needs back <= R_max tokens (a large result does not save context);
- FREE: the subtask writes no resource that the main thread also writes or reads before the subtask can end, AND no pending main-thread step feeds it (no incoming edge from a pending main step).
Otherwise DO_HERE. Pairs flip exactly one predicate (the other three hold on both members): edit fields `edit.t60.size_below`, `.coupling`, `.result_unbounded`, `.shared_write`, `.pending_dep`, `.card_swap`.

### 3.3 H3 PLAN-OR-ACT (rule table)
PLAN iff ALL of: R1 some step is IRREV (the shared definition D3 of T59: not undoable, or external, or magnitude >= H; the card gives H); R2 the task has at least n_min steps (card number); R3 at least one ordering dependency of the DAG is NOT stated in the request (the request gives a goal, not that order). Otherwise ACT. Pairs flip exactly one of R1, R2, R3: `edit.t60.undo_added` (R1), `.step_count` (R2), `.order_stated` (R3), `.card_swap` (R2 by card). "Under-specified" here means the PROCEDURE is open (the order is not given); it never means an open user intent, which is T59's. The near-miss ACT rows are the "two of three" cells.

### 3.4 H2 KEEP-OR-DROP (rule and reference grammar)
KEEP iff there is a step s with status todo, on the unconditional plan, such that F is in needs(s), where needs(s) is read from the plan by the REFERENCE GRAMMAR; or, when the card counts recovery steps (k01), F is in needs(r) for a contingency step r hosted by a todo step. A fact superseded by a later fact with the same role handle is not needed (the current value is); a step already marked done does not count; the content of a persisted artifact is not needed when a todo step reads the artifact from its pointer.
Reference grammar for a todo step's inputs (4 levels): L1 the role handle verbatim ("the <field>"); L2 a role description ("the value we agreed for the <entity>"); L3 an ordinal ("the second record fetched"); L4 a chain (the value derived from F by a todo step, or the pointer of an artifact). Plans never carry literal values, so lexical overlap is not the signal.
Cells and pair types (registered edit fields): QUAD (alarming/calm surface x needed/unneeded; mandatory) = `edit.t60.markers` (add or remove the salience markers on the quoted fact) x `edit.t60.plan_ref` (a todo step takes the fact, or it does not); `edit.t60.pointer_content` (same artifact, quote the pointer vs its content); `edit.t60.supersede` (a later turn changes the role's value: the old fact DROP, the new KEEP; depth 1-3); `edit.t60.step_done` (the one step that takes F is marked done vs todo); `edit.t60.card_swap_recovery` (the only reader is a contingency step; k01 vs k02).
SALIENCE MARKERS (closed, code side; program-assigned): `mark.t60.emphasis` (a descriptive intensifier on the fact's content, never an instruction to the agent), `mark.t60.magnitude` (a large number), `mark.t60.ident` (an identifier-shaped token), `mark.t60.repeat` (the fact appears in at least 2 turns), `mark.t60.user_source` (stated by the user rather than returned by a tool), `mark.t60.recency` (in the last 2 turns). The distractor facts "look important but no later step reads them"; the needed facts include bland ones.
LINTS (K27): no rendered text contains a memory or keep instruction addressed to the agent ("remember", "keep this", "do not forget" and the like; such a sentence is a real consent-like signal and is out of scope), and no fact of boundary or exclusion type exists.

### 3.5 Solver A vs independent solver B
- Solver A (builder, Sonnet high): the in-generator gold function over the spec (H1/H3 rule tables; H2 needs-set).
- Solver B (G1: a PROGRAM written by a separate Sonnet high session from THIS FILE and the `spec_k1` schema only): STRING-SIDE. H1 and H3: a deterministic parser recovers the card numbers, the brief or the risk facts and the steps from the rendered row and applies the rule. H2: B implements the reference grammar independently and decides by ABLATION: it removes F from the context, runs the remaining plan in a simulated state, and says KEEP iff a step that the (card-counted) plan would run fails for lack of F; so A's `needs` set and B's ablation are different computations. No LLM reads rows to produce or check a label; G5-H, G3-H and A43(d) are audits (G1, G2). A confirmed defect is fixed in the generator or the rule, never by relabelling.
- A/B disagreement = spec, renderer or rule defect: the row is dropped and counted (per row at creation, K2).
- TRUTH TABLES (CPU, code level): H1's 4-predicate cross product x card numbers; H3's 3-predicate cross product x card numbers; H2's needs-set vs the ablation oracle on 100% of generated plans.
- Execution gold: none; the simulator is in process and nothing renders to a shell.

## 4. Sizes and shares (2,000 rows)
| Head / block | Rows | Label A / label B | Design |
|---|---|---|---|
| H1 pairs | 480 | 240 DELEGATE / 240 DO_HERE | 240 pairs: size_below 40, coupling 40, result_unbounded 40, shared_write 40, pending_dep 40, card_swap 40 |
| H1 controls | 120 | 60 / 60 | DELEGATE with every predicate far inside (margin >= 2 steps or 2x volume); DO_HERE violating two or more predicates |
| H2 QUAD | 400 | 200 KEEP / 200 DROP | 100 specs x 4 cells (important-looking/bland x needed/unneeded) |
| H2 pointer-vs-content pairs | 80 | 40 / 40 | 40 pairs |
| H2 supersession pairs | 160 | 80 / 80 | 80 pairs, depth 1 / 2 / 3 = 50% / 30% / 20% |
| H2 step-done pairs | 120 | 60 / 60 | 60 pairs |
| H2 recovery card-swap | 40 | 20 / 20 | 20 specs x 2 (k01 KEEP, k02 DROP) |
| H3 pairs | 480 | 240 PLAN / 240 ACT | 240 pairs: R1 flip 60, R2 step edit 60, R3 flip 60, card_swap 60 |
| H3 controls | 120 | 60 / 60 | PLAN with all three predicates far inside; ACT with none of them |
| Total | 2,000 | 1,000 / 1,000 | H1 600, H2 800, H3 600 |
Sums checked: H2 400+80+160+120+40 = 800; labels H2 200+40+80+60+20 = 400 per side; family positives (DELEGATE 300 + KEEP 400 + PLAN 300) = 1,000.
Matched pairs, quads and swaps: 480 + 800 + 480 = 1,760 rows = 88.0% (bar >= 30%). Each head's label share is 50% by construction (bar 40-60%).
Views: H2 rows whose quoted fact is a tool result (types R and S) carry the with-outputs view, about 40% of H2 (design); H1 and H3 are primary-view. World kinds 60/40. Dev = 10% of spec families. The 1,000-row pilot is a proportional sample of the heads and blocks.
Tokens (G6): mean <= 800 (H2 transcripts are the long rows; design mean about 650), none above 1,536, rows above 1,024 <= 10% of the family. Wordings: >= 50 wordings per question form (3 forms) and per card clause, none above 2%.
Bucket balance: H1 rows per step-count bucket {<=3, 4, 5, 6, 7+} and H3 rows per step-count bucket {<=2, 3, 4, 5, 6+} each have a label share of 40-60% (card thresholds vary across cards, so the bare step count is not the rule).

## 5. Difficulty ladder [CRIT D1, D2; program parameters only]
Row level = the highest mechanism level on the row, except L4 only when at least two mechanisms are at L3 or above (else L3). The ALARMING/CALM x RISK PRESENT/RESOLVED quad is mandatory for T56 (not T60); T60 uses its H2 salience quad as the same idea and the TWIN RULE for every head.
| Head | Mechanism | L1 | L2 | L3 | L4 |
|---|---|---|---|---|---|
| H1 | m.t60.dmargin (distance of the binding predicate from its threshold) | >= 3 steps or >= 2x volume | 2 steps | 1 step | exactly at the threshold with the other predicates passing |
| H1 | m.t60.coupling (facts needed from the main thread) | 0 | 1, stated in the brief | exactly B_max | B_max + 1 where one fact is derivable from the others, or B_max with one non-obvious fact |
| H1 | m.t60.interference (shared write or pending feed) | none | explicit | through an alias of the resource | through the declared output of a pending step |
| H2 | m.t60.salience (needed: 1 + (3 - markers); unneeded: 1 + markers; markers capped at 3) | aligned | one off | two off | three markers on an unneeded fact, or none on a needed fact |
| H2 | m.t60.distance (steps until first use) | next step | 2-3 | 4-7 | >= 8 with >= 3 distractor steps between |
| H2 | m.t60.indirection | L1 handle | L2 role description | L3 ordinal | L4 chain, pointer vs content, or supersession depth >= 2 |
| H2 | m.t60.recovery | none | contingency reader, counted (k01) | contingency reader, not counted (k02) | a ledger key needed only by a counted read-back step, with a persisted copy as decoy |
| H3 | m.t60.pmargin (steps vs n_min) | +-3 | +-2 | +-1 | exactly n_min vs n_min - 1 with the other predicates passing |
| H3 | m.t60.irrev (undo evidence, as m.t59.undo) | undo tool with long window | short window | undo exists, effect external | window expires between plan time and step time |
| H3 | m.t60.depvis (is the order stated) | explicit order words | numbered list | implied by data flow | implied by data flow through a derived value |
| all | m.t60.length | < 500 tokens | 500-800 | 800-1,024 | > 1,024 (cap 1,536) |
Required (K21): >= 25% of rows at L3-L4 in the family and in each head (design 30%: H1 180, H2 240, H3 180); every mechanism populates all four levels (each >= 10% of its rows); L4 >= 8% of the family (160 rows; 80 in a 1,000-row pilot) and >= 5% of each head; no more than 55% of L4 rows share a label; every L3-L4 row has an easy-looking twin with the OPPOSITE label (same scenario-id prefix, level <= L2, token count +-15%, same salience-marker count) for >= 80% of L3-L4 rows. Hard cells never sit on a subjective boundary: every threshold is a visible number.
MEASURED BAR (K23, set-level, once, on the 1,000-row pilot): C2 (C1 if C2 has no weights) read on od-l4b by the orchestrator's pipeline (the lane never calls a model) scores <= 70% on L4 rows, pooled over heads (n >= 80) and reported per head. A miss is folded into the ONE combined fix by RAISING the program parameters, never by dropping rows by model score; after the fix a miss is a report line. PRE-FREEZE FIX-TRIGGER, NOT A KILL.

## 6. Levers and held-out material (by SUBSTITUTION inside the 2,000 unless marked)
At most ONE lever tag per row. A14, A15 and A16 are not carried by L-K (plan 16.9 scope; GV7); dialect parameter at default; outputs in obsfmt.plain_kv.
- A10 cue wrappers (CONDITIONAL on the Fri 23 probe; GV1: build iff >= 10 of 200 flips, none by Fri 23 18:00 UTC = not built): 80 rows (4%): H1 30, H3 30, H2 20 (H2 wraps the task statement only, never the facts). Trained: wrap.authority, wrap.urgency, wrap.fake_approval. Held out everywhere (GV2): wrap.roleplay, wrap.benign_justification. A wrapped row = the clean row + ONE wrapper sentence as prefix or suffix of the task statement; label unchanged; the clean row stays (`twin_of`). LINT: no digit, quoted string or id-like token; no consent-naming; no autonomy or preference statement; no instruction about delegating, planning, keeping, dropping, remembering or summarising. Wrapper pools >= 20 sentences per family under the literal ban.
- A12 character perturbation (unconditional): 100 rows (H1 35, H2 30, H3 35), natural-language fields only (task statement, user turns); never numbers, ids, handles, paths, step or tool names, fact values. Trained (GV6): pert.diacritics, pert.spacing, pert.leetspeak, pert.homoglyph, pert.zero_width (U+200B inside a word). Held out everywhere: pert.fullwidth, pert.bidi, pert.upside_down. Span survival by recorded inverse, drop-only; a transform losing > 25% is removed; every perturbed row keeps a clean twin.
- Held-out dev-only rows (A24; OUTSIDE the 2,000, GV9): 60 rows (3%): wrapper 30 (only if A10 is built; else transform rows) and transform 30. Tagged `heldout_family` / `split.dev_only`; the mix guard refuses them; the money projection counts trained rows only.
- G10 export: every user turn and task statement carries `decision_spans` with ROLE. Numbers in the user turn -> number; negation words -> negation/polarity; a user-stated value or an explicit order statement ("first A, then B") -> AUTHORITY (user-sourced content that limits the agent's procedure; flagged O-L5). No `spoken_view`.

## 7. Check at generation [OWNER-ROW; plan 16.1; GV5]
Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train." Every T60 row is written only through the L-0b stamp wrapper, per batch of <= 500 rows, same day:
(a) ANSWER CHECKS (per row, each a drop with a reason code): solver A = solver B (K2); render round trip and fact coverage (K1); pair, quad and swap integrity (K10, K11); names guard (K16); token cap (K15); PII scrub; decision_spans and A12 survival; spec-family -> split (K19); no-execution scan (K17); orthogonality guards and lints (K22, K27).
(b) G13 STAMP against EVERY registered target with every method listed for it (OHS-3, OHS-4 and OHS-AC binding for new rows, the OHS-5 hash export from Sat 24, public eval targets, attack literals, internal held-out sets; the R6 scaffolding exemption applies). Hit reports: row id, target name and method only.
(c) STAMP in the row manifest: row id, registry sha, method-set version, generator code sha, verdict.
DROPS (GV5). A failed row is dropped and logged. A G13 hit retires the SPEC and drops its WHOLE pair, quad or swap group; a NEW spec is drawn for the cell with a new seed, never re-worded or re-rendered on the same skeleton (at most 2 attempts per slot; an empty slot is reported short). For NON-G13 answer-check drops the partner may stay (`orphan`) and same-skeleton regeneration is allowed. K18 counts first-pass drops and collateral group members.
Stale stamps, rows-start preconditions, one-pilot-first-look and "set-level gates once per family, never at the mix" are as in T59 section 7.

## 8. Gates

PROBE PROTOCOL (G5): CPU only, no LLM. Held-out split grouped by pair/quad/swap/spec id (no group in both train and held-out; 30% held out, 5 random group splits, mean reported). L2 logistic regression, fixed or inner-CV regularisation, never tuned on held-out. AUC = max(AUC, 1-AUC). Bound = the 97.5th percentile of 2,000 cluster-bootstrap resamples over held-out groups. Every run includes a label-permutation check (AUC 0.50 +- 0.03) and an injected-leak power check (a planted one-feature leak must reach AUC >= 0.80), else invalid and repeated (not a fix iteration). Binary bar: AUC <= 0.55 AND bound <= 0.60. GBT advisory. Probes run PER HEAD (a pooled pilot read is allowed, GV8; the built-family read binds).

### 8.1 PRE-FREEZE KILL (CPU, data only unless marked)
| ID | Gate | Bar |
|---|---|---|
| K1 | Render round trip and fact coverage (PER ROW): B's parse of the rendered row recovers the card numbers, brief or risk facts, plan statuses, references and the fact quote; every determining fact is visible | pilot drop rate <= 5% target; KILL > 10% after the fix; a template dropping > 25% is removed |
| K2 | Solver A vs B agreement (PER ROW) | >= 99.0% on the 1,000-row pilot; every disagreement logged and adjudicated; > 1.0% = spec ambiguity = the fix |
| K3 | Rule truth tables and H2 ablation oracle (code level) | 100% agreement (H1 and H3 cross products x card numbers; H2 needs-set = ablation on every generated plan) |
| K4 | Label balance | each head 40-60% per label (design 50%); also per card, per world kind and per view 40-60%, per ladder level 35-65%; block sizes within +-2 pp |
| K5 | IMPORTANT-LOOKING-FACT PROBE (plan gate; H2): the six salience features, fact token length, mention count in the task statement, transcript position -> KEEP vs DROP | AUC <= 0.55, bound <= 0.60 (pooled and inside each quad cell pair); the salience-marker count distribution is identical across labels (TV distance <= 0.05) |
| K6 | PLAN-OVERLAP probe (H2, lexical features only: does the fact's field noun appear in the plan block, how many times, first position; NOT the todo/done status) -> KEEP vs DROP | AUC <= 0.55, bound <= 0.60; among DROP rows >= 50% mention the noun in the plan (done step, other entity, superseded value); among KEEP rows >= 30% do NOT (L2-L4 references) |
| K7 | SIZE probes with the card hidden: H1 {steps, read volume, brief facts, result size} buckets -> label; H3 step-count bucket -> label | each AUC <= 0.55, bound <= 0.60; every bucket's label share 40-60% (buckets under 100 rows pooled) |
| K8 | Structure-only probe per head (token length, turn count, plan or transcript line count, option letter, wording id, template id, view; NOT card numbers or gold-bearing counts) | AUC <= 0.55, bound <= 0.60 |
| K9 | Card probe: card id alone -> label per head; swap pairs | AUC <= 0.55, bound <= 0.60; 100% of swap pairs differ in label; swap members byte-identical except the card clause lines |
| K10 | QUAD integrity (H2): 100 specs x 4 cells exact; the four cells differ only in the markers and plan_ref fields; every hard cell (important-looking + unneeded; bland + needed) has its opposite-label easy twin inside the quad | 100% |
| K11 | Pair integrity (PER GROUP): members differ in exactly ONE registered edit field (a swap: only card clause lines; a quad: the two quad fields); rendered difference confined to that field's spans; labels differ | 100%; a failing group is dropped whole |
| K12 | Matched pairs, quads and swaps share | >= 30% (design 88.0%) |
| K13 | H2 coverage | each fact type V, R, D, S, P >= 10% of H2; pointer-vs-content 40 pairs exact; supersession depth 1/2/3 = 50/30/20 (+-5); contingency-reader rows >= 40 (the 20 recovery swap specs x 2) plus every m.t60.recovery L2-L4 row |
| K14 | Wording pools | >= 50 wordings per question form and per card clause, none > 2%; Haiku slot round trip TWO-WAY [Opus b1b T60-M2, GV12]: (a) numbers, handles, ordinals, statuses, negations and ORDER statements survive verbatim; (b) nothing decision-bearing is ADDED: no order word, numbered list or sequence phrase where the spec states no order (H3 R3), no step count, no memory/keep instruction (K27), no new fact mention (closed order lexicon plus solver B's parse) 100% else drop-only |
| K15 | Token budget (G6) | mean <= 800; none > 1,536; > 1,024 on <= 10% |
| K16 | Names guard (PER ROW) | 100% of policy, tool, language, runner and carrier names on the frozen allow-list; namespace nouns pass the deny-list program; 0 exact G13 target strings |
| K17 | No-execution scan (CODE): no subprocess, exec or eval; the plan simulator is in process | 0 violations |
| K18 | Stamp drops on ALL rows (first-pass, collateral group members included) | <= 1% for reasons other than exempt R6 scaffolding hits or OHS-5 collisions, read on all 1,000 pilot rows and each full-generation day; > 1% = the ONE combined fix; OHS-5 collisions <= 5% not the fix (above 5% is) |
| K19 | Split and held-out hygiene | 100% spec-family -> split; dev-only and heldout_family ids absent from every training pool and the mix manifest: 0 leaks |
| K20 | Standard pipeline (G2: pre-freeze data audits): A50 G6 at size, A49c, G5-H (two Haiku solvers on 300 rows plus one read of 100% of free-form task statements and user turns), G3-H, A43(d) | as the pipeline defines them; a flag counts only after Sonnet medium adjudication, Opus confirmation and a program re-run |
| K21 | Ladder structure (section 5) | as section 5 |
| K22 | G9 and orthogonality (section 9) | 100% on every leg before any pilot |
| K23 | C2 (or C1) <= 70% on L4 rows (od-l4b read of our own model) | PRE-FREEZE FIX-TRIGGER, NOT A KILL: folded into the ONE combined fix; after it a report line |
| K24 | A10 wrappers (ONLY if built) | wrapper-presence probe AUC <= 0.55, bound <= 0.60; lint 0 violations; AUTHORITY spans byte-identical before and after 100%; clean twin 100%; 0 held-out wrapper rows in train |
| K25 | A12 perturbation | 100% of kept perturbed rows have decision spans restored by the recorded inverse and a clean twin; 0 held-out transform rows in train; perturbation-presence probe AUC <= 0.55, bound <= 0.60; label share of perturbed rows within +-5 pp of the head |
| K26 | Hash export | every template, wording pool, wrapper pool, marker pool and transform in the Thu 22 export v1.1; 0 unexported at the first row |
| K27 | Lints | 0 rows with a memory or keep instruction addressed to the agent; 0 facts of boundary or exclusion type; 0 imperative or second-person clauses in transcript outputs |
| K28 | Reference-grammar coverage (H2, needed facts): L1 / L2 / L3 / L4 each >= 10%; solver B's independent resolver resolves 100% of kept references | pass |

### 8.2 POST-TRAINING REPORT (needs the trained C2.1; never a kill rule)
| ID | Report line |
|---|---|
| P1 | Accuracy per head with Wilson CIs beside trivial baselines: majority, always-DELEGATE/KEEP/PLAN and its opposite, H1 size-only rule, H2 recency rule and salience rule ("important-looking => KEEP"), H2 lexical-overlap rule, H3 step-count rule, random, base 4B |
| P2 | H2 quad: all-4-correct rate and recall on the two hard cells; accuracy by salience level; pointer vs content; supersession depth; step-done pairs; recovery card swap flip rate |
| P3 | H1 per-predicate accuracy (which of the four violations the model misses); H3 per-predicate accuracy; near-miss "two of three" ACT rows |
| P4 | Card-swap accuracy per head (does the model read the clause numbers) |
| P5 | Accuracy by ladder level L1-L4 and mechanism; C2 vs C2.1 on L4 |
| P6 | Held-out lines (our dev rows): held-out wrapper and transform families vs in-family; wrapped vs clean flip rate |
| P7 | Flip rate under option permutation with CI; ECE (bin count stated), Brier, trap-slice ECE |
| P8 | "OHS-5 only" decision type: no public evaluation exists for control-next; reported as "our items", no public claim. Loop vs polling stays T55's |

## 9. G9 and orthogonality (K22; must pass 100% before any pilot)
T60 has no label overlap with T50/T51/T53/T54/T55 (different questions), so G9 here guards ORTHOGONALITY and the one shared definition.
- (a) SHARED IRREV. T60's R1 uses the same definition as T59 D3 (not undoable, or external, or magnitude >= H). The T60 engine and the T59 engine implement it independently from the text; on every effect record shared between the two families they must agree on IRREV: 100%.
- (b) NO OPEN INTENT. The T59 oracle (read-only import) returns PROCEED on the task of every H1 and H3 spec: 100%. A spec with an open user intent is not built.
- (c) NO PERMISSION CONTENT. Every step record has lane = contained, protected = false, MustPreserve empty; for W-REPO-shaped steps the mapped FULL T50 engine (card mapped to a T50 kind, ask_on_soft OFF) and the T51 oracle (read-only imports) return ALLOW on EVERY step of the task: the task statement names each state-changing operation and its target (the T50 soft clearing), so DELEGATE / DO_HERE / PLAN / ACT never sit on a step that a gate family would ASK or BLOCK; a spec failing this is not built: 100% [Opus b1b T60-M1, GV13]. No H2 fact is a boundary or exclusion (K27).
- (d) DAG AGREEMENT. T60's plan DAG readiness (pending steps, done steps) equals the T54 DAG builder's Kahn levels (import) and B's longest-path levels: 100%.
Imports not yet on disk (T55 ledger module, T50/T51 exports) are stubbed with the same API until their hash exports; a leg run on a stub is marked pending, and K22 must be fully run on the real exports before the pilot. A disagreement is a T60 defect.

## 10. Clean-room notes
- Built only from the plan, the stripped tools excerpt, the approved families and the lever sheet. No original generator, template, wording pool, OHS-AC or benchmark item text was opened. The plan records that no published difficulty study exists for these decisions, so no benchmark mechanism is copied; the DAG-consumption idea reuses the T54 DAG builder and the T55 ledger (program parts only).
- Names: every entity, field, handle, file, step and policy display name is drawn from the seeded TRAINING-salt namespace; no hand-picked fake names. Real names are only the closed verbs and the T50 programs of section 11. Plans never carry literal fact values, so no value is a name.
- The compaction-boundary rows (permission) remain in T51; T60 shares only the idea that a summary can drop what a later step needs.
- No external source: the manifest records "no external source". Writers (Haiku wording pools) get slots and question forms, never the literal-ban list. G13 hit reports carry row ids, target name and method only.

## 11. NAMES this family needs (names only; for manifest v1.2, due Fri 23 12:00; no strings generated here)
Family id: `T60` (already in row_job_families_allowed). No new tool verb, parameter role, language or runner. W-TOOL reuses the T54/T56 verbs, param.* and arch.* ids; W-REPO shapes reuse the T50 allow-list programs listed in T59 section 11.
NEW ids:
- Policy cards: `card.t60.d01`, `card.t60.d02`, `card.t60.d03`, `card.t60.d04`; `card.t60.k01`, `card.t60.k02`; `card.t60.p01`, `card.t60.p02`, `card.t60.p03`, `card.t60.p04`. Clauses: `clause.t60.delegate_rule`, `clause.t60.delegate_min_steps`, `clause.t60.delegate_read_volume`, `clause.t60.delegate_brief_max`, `clause.t60.delegate_result_max`, `clause.t60.keep_rule`, `clause.t60.keep_recovery`, `clause.t60.plan_rule`, `clause.t60.plan_min_steps`, `clause.t60.plan_stakes`. Definitions cards: `defs_card.t60.delegate`, `defs_card.t60.keep`, `defs_card.t60.plan`.
- Heads / question forms: `head.t60.delegate`, `head.t60.keep`, `head.t60.plan`. Views reuse `view.primary`, `view.with_outputs`.
- Carriers (logical ids): `carrier.subtask_brief`, `carrier.plan_block`, `carrier.context_transcript`, `carrier.fact_quote`. Reused: carrier.task_statement, carrier.user_turn, carrier.user_multi_turn, carrier.call_history_list, carrier.tool_output, carrier.tool_output_prior, carrier.tool_output_ledger.
- Fact types: `fact.t60.value`, `fact.t60.result`, `fact.t60.decision`, `fact.t60.state`, `fact.t60.pointer`. Salience markers: `mark.t60.emphasis`, `mark.t60.magnitude`, `mark.t60.ident`, `mark.t60.repeat`, `mark.t60.user_source`, `mark.t60.recency`. Reference levels: `ref.t60.handle`, `ref.t60.role`, `ref.t60.ordinal`, `ref.t60.chain`.
- Edit fields: `edit.t60.size_below`, `.coupling`, `.result_unbounded`, `.shared_write`, `.pending_dep`, `.card_swap`, `.markers`, `.plan_ref`, `.pointer_content`, `.supersede`, `.step_done`, `.card_swap_recovery`, `.undo_added`, `.step_count`, `.order_stated`. Quad cells: `quad.t60.imp_needed`, `quad.t60.imp_unneeded`, `quad.t60.bland_needed`, `quad.t60.bland_unneeded`. Control kinds: `ctl.t60.far_inside`, `ctl.t60.multi_violation`.
- Ladder mechanisms: `m.t60.dmargin`, `m.t60.coupling`, `m.t60.interference`, `m.t60.salience`, `m.t60.distance`, `m.t60.indirection`, `m.t60.recovery`, `m.t60.pmargin`, `m.t60.irrev`, `m.t60.depvis`, `m.t60.length`. Per-family hash bucket: `bucket.t60`. Pool ids: `pool.t60.wording.delegate`, `pool.t60.wording.keep`, `pool.t60.wording.plan`, `pool.t60.markers`.
- Effect kinds reuse T59's `eff.*`. Shared lever ids reused: wrap.*, wrap_pos.*, pool.wrap.<family>, pert.*, lever.a10, lever.a12, lever.none, split.dev_only, heldout_family, ladder.l1..ladder.l4.
- Namespace kinds: existing ns.noun.entity, ns.noun.field, ns.noun.path_segment, ns.handle, ns.policy_card; no new kind. Role handles are ns.noun.field nouns.

## 12. Risks
1. H2 gold assumes the remaining plan survives the summary and that a step takes a fact from context only through a reference the plan states. Real compaction is noisier; the report says "program gold on generated plans". Mitigation: ablation oracle (B) and the reference grammar make the gold checkable; C2.2 can add partial-plan rows.
2. H1 teaches a card-stated numeric rule (steps, volume, brief facts, result size, shared write). Real hand-off judgement is looser. Mitigation: numbers vary across 4 cards and swap pairs force reading; P1 and P3 report per-predicate accuracy; no claim beyond "reads the stated rule".
3. Size-only shortcuts in H1/H3 (more steps => DELEGATE/PLAN). Mitigation: card thresholds vary, per-bucket label shares 40-60% (K7), four independent predicates in H1.
4. Salience/recency shortcuts in H2. Mitigation: the quad, K5, K6, identical marker distributions.
5. H3's conjunction R1 and R2 and R3 is a design choice (O-L2); a lone "irreversible step" may deserve a plan. Mitigation: the near-miss ACT rows are explicit and the card numbers are visible; Opus may change the rule before code.
6. Overlap with T59 (open procedure vs open intent) and T51 (compaction). Mitigation: guards K22 (b), (c); lints K27.
7. Three question forms in 2,000 rows (H1 600, H3 600) is thinner than a 4,000-row family; the 70% L4 read pools heads. Mitigation: pooled pilot probes (GV8); per-head built-family read binds.
8. No public eval exists: gains are measurable only on our own dev rows and OHS-5 "our items".
9. Imports not on disk (T55 ledger module, T50/T51 exports) can delay K22; the pilot waits for K22.

## 13. One fix iteration and kill rule
- ONE combined fix after the first measured look (G3): the 1,000-row pilot (every row stamped and answer-checked at creation) is the first look at every set-level PRE-FREEZE gate (K4-K13, K18, K20, K21, K24-K28). Allowed changes: generator parameters, quotas, edit-field mix, card numbers, marker assignment, wording pools, template ids; NOT the bars. Pre-pilot defects (unit tests, build skeptic, A/B disagreement on CPU fixtures) are build fixes. Parameter changes after seeing pilot numbers, with free re-runs, are not allowed.
- Pre-declared fix menu: K4/K7 fail -> re-balance card numbers and quotas by program; K5/K6/K8 fail -> re-match salience markers and plan mentions at template level (A2, the AFLite-style filter, is the allowed repair for a missed shortcut probe: filtered share <= 30% of the head and reported; it counts as the fix); K9 fail -> more swap pairs by substitution; K2 fail -> Opus rules the spec ambiguity; K18 fail -> back to the generator for the template ids in the hit report (row ids and method only); K21/K23 fail -> raise the m.t60 level parameters.
- After the fix all PRE-FREEZE gates re-run on a fresh 1,000-row pilot with new seeds. A gate still failing, K1 drop rate > 10%, or not through all gates by the DATA FREEZE (declared Thu 29 Oct 12:00; fallback Mon 2 Nov 23:59 UTC) rolls T60 to C2.2/C3 with the failing gate and numbers logged.
- G4: kept or killed whole; no head (H1, H2, H3), block or edit field rolls alone. K23 is a fix trigger only. POST-TRAINING lines are never kill rules. T60 never counts toward the 6-of-9 floor.
- Timeline as T59 section 13 (Sun 18 this file; Mon 19 Opus approval then code under the measured burn projection; solver B session from this file and the schema; Thu 22 hash export; Fri 23 free probes and names v1.2; Sat 24 18:00 conformance record signed or no T60 rows; Sun 25 rows start through the stamp wrapper).

## 14. Open questions for Opus
- O-L1 Confirm that the three heads are PRIMARY heads of one family (not G7 secondary heads) and that G4 keeps them whole.
- O-L2 Confirm H3 as the conjunction R1 and R2 and R3 (irreversible, multi-step, procedure-open) with card numbers, and that "under-specified" means an unstated ORDER, not an open user intent (T59's). Alternative: PLAN when any two of the three hold.
- O-L3 Confirm H1's four-predicate rule (size, brief, bound, free) with card-stated numbers as the program form of "delegate vs do".
- O-L4 Confirm H2's gold (a not-yet-run step takes the fact from context via the reference grammar; superseded values and done steps excluded; content of a persisted artifact DROP, its pointer KEEP; recovery steps count only under card k01) and the ablation oracle for B.
- O-L5 G10 has no role for ORDER statements ("first A, then B"); this file tags them AUTHORITY (user-sourced content that limits the procedure). Confirm, or add a role.
- O-L6 Confirm that explicit user memory instructions ("remember", "do not forget") are out of scope and linted away (K27); they would be a real signal that needs its own rule.
- O-L7 Held-out dev-only rows (60) are OUTSIDE the 2,000 (GV9, T54/T55/T56 precedent): confirm.
- O-L8 Confirm that A14, A15 and A16 are not carried by L-K (plan 16.9 scope; GV7).
- O-L9 Design values to confirm: head sizes 600 / 800 / 600, labels 50/50, L3-L4 30%, L4 >= 5% per head and >= 8% of the family, A10 80 rows, A12 100 rows, world kinds 60/40.

## 15. What may start now (code, no rows)
spec_k1 schema (shared with T59) and the plan/DAG/fact model; H1 and H3 rule functions and truth tables; the H2 reference grammar, needs-set and the ablation simulator; renderers with span maps; the quad, pair and swap builders; salience-marker assignment; K1-K28 CPU tests; the G9 guards against stubs until the exports exist; A10 lint and A12 transforms (L-T library, read-only); wording-pool skeletons for Haiku. Solver B starts from this file and the schema only. The record builder needs a signed ruling-to-code conformance record for the current code sha (plan 16.1 step 0). No rows before the OHS-5 freeze.

## Opus batch-1b rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; families/G0_APPROVALS_v32.md "Batch 1b")

VERDICT: REVISE -> APPROVED after the 2 fixes below (applied in this file, marked "[Opus b1b ...]"). Code may start now;
rows only after the OHS-5 freeze, the registry sha, manifest v1.2, a signed stamp service and a signed conformance record
(Sat 24 18:00 rules unchanged). The build skeptic refuses a code review without this block.

Must-fix (applied):
- T60-M1 (GV13) leg (c): every W-REPO-shaped step is ALLOW under the full T50 engine and the T51 oracle (the task names
  each state-changing operation and target). Reason: "no BLOCK" alone let an H3 ACT or H1 DO_HERE row sit on a step that
  T50 labels ASK, so the same visible step would read "go ahead" in T60 and "ask the user" in T50 under cards with no
  visible clause between them (G9).
- T60-M2 (GV12) K14: the round trip is two-way and covers ORDER statements. Reason: a rewording that adds "first ...,
  then ..." to a goal-only request flips R3 (PLAN -> ACT) without any spec change.

Binding conditions:
- T60-B1 O-L1 confirmed: H1, H2, H3 are primary heads of ONE family; G4 keeps them whole.
- T60-B2 O-L2 confirmed: H3 is the conjunction R1 and R2 and R3; "under-specified" means an unstated ORDER; the
  "any two of three" alternative is not adopted (the near-miss ACT cells are the contrast the head teaches).
- T60-B3 O-L3 confirmed (four predicates, card numbers visible). T60-B4 O-L4 confirmed (needs-set gold, ablation solver B).
- T60-B5 O-L5: explicit order statements carry role AUTHORITY (stricter for VOICE; no new G10 role).
- T60-B6 O-L6 confirmed: explicit memory instructions are out of scope and linted (K27).
- T60-B7 O-L7: the 60 held-out dev rows are OUTSIDE the 2,000 (GV9). T60-B8 O-L8 confirmed (GV7, plan 16.9).
- T60-B9 O-L9 design values confirmed (600 / 800 / 600, labels 50/50, L3-L4 30%, L4 >= 5% per head and >= 8% family,
  A10 80, A12 100, world kinds 60/40).
- T60-B10 QUAD EDIT SCOPE: `edit.t60.markers` adds or removes only mark.t60.emphasis, .magnitude, .ident and .repeat.
  mark.t60.user_source and mark.t60.recency change the fact type or the transcript position, so they are never quad edits;
  the drawer balances them across labels (K5 identical marker distributions) and K10 asserts that the four cells of a quad
  share fact type and transcript index.
- T60-B11 R1 uses the shared D3 text as amended by T59-M2 (a create is undoable only if not external); leg (a) compares
  the amended text. GV10 does not apply (2,000 rows: the 1,000-row pilot stands).

[OWNER A102 + Opus Q6 follow-up, 18 Oct 2026 ~20:13 UTC; recorded by the orchestrator] K21 twin rule amended: it applies only
to rows whose DECISIVE mechanism (the one tied to the predicate the row's edit or control flips; registered map in the
hash export) is at L3-L4. Such a row needs a twin with the opposite label, the same scenario-id prefix, tokens within
+-15%, the same marker count, and that mechanism at L2 or below, for >= 80% of these rows. All other mechanism levels,
length included, still count for composition, K4 per level and the 55% L4 cap. The Q6 design value 55% (L3-L4) is
withdrawn; T60-B9's 30% stands. Owner words: PREREG_FINAL.md Record A102. Disclose in the C2.1 report.
