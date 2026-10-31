# G0-LITE T59 ASK-OR-PROCEED (lane L-K; P0-extra; draft for Opus approval, target Mon 19 Oct 2026)

Author: Sonnet 5.5 high, Sun 18 Oct 2026 (UTC). Read scope used: training_inputs/PLAN_TRAINING_SIDE.md (incl. section 16), training_inputs/LANE_L-K.md, training_inputs/excerpts/tools_s5.md (stripped), families/T50/G0_LITE.md and G0_ADDENDUM_v32.md, families/T51/G0_LITE.md, families/T54/G0_LITE.md and G0_ADDENDUM_v32.md, families/T55/G0_LITE.md and G0_ADDENDUM_v32.md (section 8 only), families/T56/G0_LITE.md (sections 1-5), families/G0_APPROVALS_v32.md (GV1-GV9, T54-B1), C2_1_PUBLIC_TRAIN_INVENTORY.md (section 4 rows for T59/T60), C2_1_EXTRA_LEVERS.md (A9, A10, A12, A24), l0/NAMES_MANIFEST_V1_1.json (names only, to avoid duplicates), c21_fam (file listing and function names only).
Not opened: any path containing "ohs" or "sealed", C2_1_PLAN_v3.md itself, any plan SKEPTIC file, any benchmark item text, research_v4/hardest.md (no stripped excerpt is in my scope, so the ladder is built from program parameters), the T27/T40-T46 generators, mutate.py, any dataset file. No rows, no generator code, nothing executed, no model or API call, no Modal.
Scope note: during orientation one search over C2_1_BUILD_ORDER.md and the sibling LANE_*.md files (outside my read list) returned only lines that name T59/T60 (headers, the L-K block, the manifest list). Nothing from them is used here beyond what LANE_L-K.md already says.
Status: DRAFT. Every number below is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus. This file is the whole spec (no addendum yet): it carries the v3.2 items inline (check at generation, ladder, levers, G9). Global rulings G1-G10 and GV1-GV9 bind and are cited by number.
Family class: P0-EXTRA (plan 16.4). Same pipeline and kill rule as P0; enters the mix if through its gates; does NOT count toward the 6-of-9 floor and cannot replace a failed P0 family.
Row family id: `T59` (already in row_job_families_allowed). Sub-blocks carry a `block` field, not new family ids.

## 1. Decision and label set

- Question (one form per row): given the policy card, the task, the context so far and the agent's planned next step, should the agent STOP AND ASK THE USER, or CARRY ON WITHOUT ASKING?
- Labels: ASK / PROCEED (binary, two lettered options, order shuffled per row; the 20% mix-time copies with a non-identity permutation equal a reversal and are NOT counted in the 2,000).
- ASK = stop autonomous work and put a question to the user. PROCEED = carry on on its own: take the planned step; or take a safe read that settles a fact; or retry, switch tool or use a stated default; or take the most likely reading WHEN the card says an undoable action may be taken that way. T59 is not a permission decision: there is no BLOCK, and T50/T51 own permission (section 9, K24).
- Two question forms: Q-MID (mid-run, the planned step is the next of several) and Q-EARLY (the early gate: the history holds reads only, and the planned step is the first state-changing step). Same label set and same gold function; the form is a visible header.
- No secondary head (G7 not used). Trigger id, slot kinds, edit field and control kind are manifest metadata and are never rendered.
- Eight triggers (the A9 paired design; each is a program template family, section 3.3): T1 missing parameter, T2 ambiguous spec, T3 conflicting constraints, T4 high stakes, T5 missing capability, T6 tool failure, T7 conflicting evidence, T8 risk appearing mid-run.
- Product use: ASK/PROCEED gate for a coding or tool agent that may stop and question its user. Output stays the label only.

## 2. Inputs, state model and cards

INPUT VIEW. P (primary) = card + task + user turns + earlier tool calls + the planned next step, tool OUTPUTS STRIPPED. W (with outputs) = the same plus tool outputs capped at 256 tokens each, at most the last 4 outputs; REQUIRED when a determining fact exists only in an output (all of T6, T7, T8 and some T1/T2 listings). FACT-COVERAGE rule (program, as T51): every fact the gold needs is tagged with where it is visible (user turn, call, card, tool list, output); a row is built in view P only if no determining fact is output-only. Outputs come from a data-field grammar with no imperative or second-person text (CPU lint; injection-style content belongs to T41c). Design shares: P 65% / W 35% (+-5 pp).

WORLD KINDS. W-TOOL (60%, 1,200 rows): scenarios on the L-T tool engine (tool_engine.state/.dag/.render/.names: archetypes, tools with read/write and idempotent flags, equivalence groups, optional undo tools). W-REPO (40%, 800 rows): scenarios on the L-A shared spec/state model read-only (LA_COMMON: files, git branches, jobs, services, contained lane only; the T51 entity list and admissible-reading sets), with the planned step rendered as a shell or tool call; only programs already on the T50 allow-list are used. All T6 rows are W-TOOL.

SPEC (`spec_k1`, shared by T59 and T60; owned by L-K): spec_id; family; block; trigger_id; form; view; world_kind; card_ref (kind plus slot values); slots[] {slot_id, kind (INTENT / WORLD / CAP), visible candidates (a listing, a user list, a card list, or "open"), sources, constraints}; interpretations I (derived); planned_step; candidate actions A(i) with effect records (kind, target, backup, undo tool and window, external flag, magnitude, created_by_agent); resolver record; delegation lines; history[]; decision_spans[] with ROLE (G10); gold {label}; renderings; split (dev/train, assigned per spec family so all members of a pair, quad or swap group land in one split); lever_tag, heldout_family, ladder level and mechanisms, pair_id, twin_of. Tags are written by the generator, read by the gates, never rendered.

POLICY CARD. 6 cards. c01-c04 are NATIVE-ON: they carry the visible line `clause.t59.undo_proceed` ("proceed with the most likely value when the action can be undone"). c05-c06 are OFF: they carry `clause.t59.ask_on_ambiguity` ("ask when a required value has no source or the request has more than one reading"). Other visible slots, varied across cards: `stakes_threshold` H (a number in the row's noun units; values 3 levels), `defaults_count` (a declared default counts as a source: on/off), `precedence` (an ordered list of which source wins on a conflict, or none), `read_first` (a listed read-only call must be used to settle an open environment fact: on/off), `retry_cap` (2 or 3). ON cards are 75% of rows, OFF 25%. This is the T54-B1 condition: T59's card line is visible, and T54-style cards ("ask when a required value has no source") are a different card.

IMPORTED CARD KINDS (used only by the G9 test, section 9; never rendered in T59 rows): the oracle accepts them as parameter sets.
| Imported kind | mode | defaults_count | read_first | precedence |
|---|---|---|---|---|
| card.t54.strict_ask | OFF | false | false (S1/S3); true for S4 when card.t54.read_before_write is active | none |
| card.t54.defaults_ok | OFF | true | as above | none |
| card.t51.c01-c06 | OFF | false | false | none (R = contained lane, protected false, MustPreserve empty) |
| card.t50.c01-c08 | OFF | false | false | none (R18 specs only) |

## 3. Gold method

### 3.1 Principle
Generate-then-render. Each row starts as a structured spec; the label is a pure function of (spec, card); the text is rendered from the spec; Haiku medium only REWORDS user turns and descriptions under a slot round trip (every decision span survives verbatim). No LLM writes or changes a label (G1).

### 3.2 Definitions (all computed by program from the spec; every input is a visible fact)
- D1 SLOTS. A task has 1-3 open slots. INTENT slot: a value only the user can supply; its source is one of user turn, an earlier tool output named in the call history, card default, a user delegation line, or none. WORLD slot: a fact about the environment (observed true / observed false / unobserved; a conflict between two sources is a WORLD slot with two candidate values). CAP slot: the call or authority the task needs is not available; its substitutes (0 to 2) are listed.
- D2 INTERPRETATIONS. I = the assignments of the open slots that satisfy every visible constraint. Candidates come from a listing, a user list or the card; an INTENT slot with no source and no list is "open" and counts as at least 2 interpretations. k_adm = |I|. A slot is COLLAPSED (one interpretation) by: a user-stated value; a card default when defaults_count is on; a user delegation line naming THAT slot ("either is fine for <slot>": every candidate is acceptable); for a WORLD conflict, a card precedence rule that names a winner.
- D3 EFFECT RECORD AND IRREV. Every candidate action has an effect record: kind in {read, create, update, move, delete, send, publish, reserve, schedule}, target, backup flag, undo tool (listed or none) with remaining window, external flag (the effect reaches a person or system outside the thread), magnitude (a count in the row's noun units), created_by_agent. `read` is never IRREV. A `create` of an agent-made object that is NOT external is UNDOABLE [Opus b1b T59-M2: a create that reaches a person or system outside the thread, e.g. an invite or a published object, is not undoable by deletion]. Otherwise UNDOABLE(c) = (backup OR undo tool listed) AND window remaining >= 1 AND NOT external. IRREV(c) = NOT UNDOABLE(c) OR magnitude(c) >= H. (The magnitude clause is how "high stakes" enters: a costly-to-undo effect counts as non-reversible. Flagged O-K1.)
- D4 CANDIDATE ACTIONS. A(i) = the call (tool canonicalised by equivalence group, canonical arguments) that does the task under interpretation i. DIFF = at least two different A(i).
- D5 ROBUST. True iff at least one of: (R-SAME) every interpretation leads to the same canonical call (NOT DIFF, D4) [Opus b1b T59-M3: the plan's "different actions" clause is now an explicit input of the gold, and the truth table of K3 crosses it]; (R-DEF) every open slot is collapsed (D2); (R-COM) a listed call exists whose mutation set lies inside the intersection of the sets licensed by all interpretations and that makes progress (the common half of a batch, an idempotent write that is right in both worlds); (R-RES) an open WORLD slot is settled by a listed read-only call and the card has read_first on. A resolver NEVER settles an INTENT slot: a read can show what the world is, not what the user meant.
- D6 FORWARD ACTIONS E = the listed calls that could do the task, or a stated substitute, under some interpretation. E empty = no forward move (missing capability with no substitute; authority denied).
- GOLD. Evaluate in order: (1) E empty -> ASK. (2) ROBUST -> PROCEED. (3) card mode OFF -> ASK. (4) card mode ON -> ASK iff there is an interpretation i with IRREV(A(i)); otherwise PROCEED. This is the plan rule "ASK iff the interpretations lead to different actions AND at least one has a non-reversible cost", with the robust-move cases written out so that "different actions" means different NEXT actions.
- TRUTH TABLE (CPU, code level): the rule function equals an independent brute-force oracle that enumerates interpretations and candidate actions and simulates each effect record, on the full cross product of (R-SAME, collapsed, R-COM, R-RES, E empty, any IRREV, mode) and on the imported-kind mappings: 100%.

### 3.3 The eight triggers (program templates; each pair removes exactly ONE detail)
Edit fields (registered ids `edit.t59.*`): e1 value stated; e2 default declared (needs defaults_count); e3 undo path present; e4 magnitude below H; e5 delegation line for the slot; e6 qualifier added to the request; e7 listing shows one match; e8 planned step is the common step (R-COM); e9 constraint loosened; e10 precedence line on the card; e11 external flag cleared; e12 reversible substitute listed; e13 capability present; e14 authoritative re-read listed (needs read_first); e15 sources agree; e16 observation shows no fork; e17 idempotency key offered; e18 read path listed; e19 equivalent tool listed; e20 error detail names the bad argument. Edit fields e3, e4, e11 need an ON card (on an OFF card they would not flip the label).
| ID | Trigger | Slot kinds and how I arises | ASK side | PROCEED side (one edit) | Edit fields (each trigger >= 3 fields, none > 40% of its pairs) |
|---|---|---|---|---|---|
| T1 | Missing parameter | INTENT, open or 2-4 visible candidates | no source; ON: the action is IRREV; OFF: any | e1, e2, e3, e4 or e5 | e1 e2 e3 e4 e5 |
| T2 | Ambiguous spec | INTENT, the request has a qualifier with >= 2 readings over an entity list; readings differ in the affected sets (W-REPO uses the T51 admissible-reading sets) | readings differ, no common step | e5, e6, e7, e8 or e3 | e3 e5 e6 e7 e8 |
| T3 | Conflicting constraints | INTENT, two stated constraints cannot both hold (budget vs required items; exclusion vs the only fix location; deadline vs scope); I = which one yields | conflict, a yielding option is IRREV or OFF card | e9, e10 or e3 | e3 e9 e10 |
| T4 | High stakes | the ambiguity of T1/T2 is kept; the stakes edit decides | magnitude >= H or external | e4, e11 or e3 | e3 e4 e11 (ON cards only) |
| T5 | Missing capability | CAP, substitutes 0-2; I = {substitute acceptable, not acceptable} | no substitute, or the substitute is IRREV, or OFF | e12 or e13 or e3 | e3 e12 e13 |
| T6 | Tool failure | WORLD (did the write commit: worlds W1/W0 from the T55 ledger simulator) and INTENT (corrected value) | see 3.3.1 | e17, e18, e19 or e20 | e17 e18 e19 e20 |
| T7 | Conflicting evidence | WORLD, two sources give different values for a fact the step needs | no precedence, no re-read, IRREV candidate (or OFF) | e10, e14, e15 or e3 | e3 e10 e14 e15 |
| T8 | Risk appearing mid-run | INTENT/WORLD fork created by an observation after step j (a listing now shows a second match, a count differs from the plan) | fork observed, a candidate IRREV (or OFF) | e16, e8 or e3 | e3 e8 e16 |
3.3.1 T6 sub-cases (classes from the T55 closed list; irrecoverable and STOP-card classes are NOT generated here): transient or rate-limited on a read, an idempotent write or a keyed write below retry_cap -> PROCEED (R-COM: the retry is right in every world); at or above retry_cap -> PROCEED if an equivalent tool is listed, else ASK; invalid_named_arg with the corrected value in context -> PROCEED, not in context -> ASK; invalid_unnamed -> PROCEED if an equivalent tool is listed, else ASK; auth_denied -> ASK (E empty); unsupported_op -> PROCEED if an equivalent tool is listed, else ASK; ambiguous write (timeout, lost acknowledgement) with key offered -> PROCEED, with a read path -> PROCEED (R-RES), neither -> ASK (the plain retry duplicates in W1). The error class is always observable (code, phrase or hint field; 30% single-channel).
The user delegation line (e5): a user turn may say that either candidate is fine for a named slot. It collapses ONLY that slot. DECOY delegation lines (naming a different slot) are generated so that the line's presence is not a cue (K31).

### 3.4 Solver A vs independent solver B
- Solver A (builder, Sonnet high): the gold function of 3.2 over the spec, plus the brute-force truth-table oracle (code-level test).
- Solver B (G1: a PROGRAM written by a separate Sonnet high session from THIS FILE and the `spec_k1` schema only, never from A's code): STRING-SIDE. A deterministic parser (slot and regex extraction, no model) recovers slots, candidates, constraints, effect and undo facts, the planned step and the card slots from the RENDERED row (canonical render plus the Haiku-reworded text through the slot round trip), recomputes I, ROBUST, IRREV and the label. No LLM reads rows to produce or check a label; G5-H, G3-H and A43(d) are audits that never set a label (G1, G2). A confirmed defect is fixed in the generator or the rule, never by relabelling a row.
- Any A/B disagreement is a spec, renderer or rule defect: the row is dropped and counted (per row at creation, K2).
- Execution gold: none. Nothing is executed; W-REPO planned steps are PARSED only (tree-sitter-bash, as the T50 validators), never run (K18).

## 4. Sizes and shares (2,000 rows)

| Block | Rows | ASK | PROCEED | Design |
|---|---|---|---|---|
| A TRIGGER PAIRS (Q-MID) | 900 | 450 | 450 | 450 pairs over the 8 triggers; each pair = one base spec and one edit that flips the label |
| B EARLY-GATE PAIRS (Q-EARLY) | 280 | 140 | 140 | 140 pairs over T1, T2, T3, T4, T5, T7 (no failure or mid-run risk exists before the first edit) |
| C CARD-SWAP PAIRS | 140 | 70 | 70 | 70 specs x 2: the same spec under an ON card (all candidates undoable, not robust: PROCEED) and an OFF card (ASK); only the card clause lines differ |
| D CONTROLS (no twin) | 680 | 180 | 500 | D1 unambiguous 240 PROCEED (120 with alarming surface; 80 in Q-EARLY form); D2 settled by default, precedence or resolver 140 PROCEED; D3 ambiguous but all undoable (ON cards) 120 PROCEED; D4 clear ASK 180 |
| Total | 2,000 | 840 (42.0%) | 1,160 (58.0%) | |

PER-TRIGGER TABLE (the quota the generator must hit; the trigger-only probe, K5, needs every trigger's ASK share inside 39-45%):
| Trigger | A rows | B rows | C rows | D rows (ASK / PROCEED) | Total | ASK | ASK % |
|---|---|---|---|---|---|---|---|
| T1 missing parameter | 140 | 60 | 30 | 118 (31 / 87) | 348 | 146 | 42.0 |
| T2 ambiguous spec | 140 | 60 | 30 | 119 (31 / 88) | 349 | 146 | 41.8 |
| T3 conflicting constraints | 100 | 40 | 20 | 82 (22 / 60) | 242 | 102 | 42.1 |
| T4 high stakes | 120 | 50 | 0 | 88 (23 / 65) | 258 | 108 | 41.9 |
| T5 missing capability | 100 | 30 | 20 | 77 (21 / 56) | 227 | 96 | 42.3 |
| T6 tool failure | 110 | 0 | 0 | 57 (15 / 42) | 167 | 70 | 41.9 |
| T7 conflicting evidence | 100 | 40 | 20 | 82 (22 / 60) | 242 | 102 | 42.1 |
| T8 mid-run risk | 90 | 0 | 20 | 57 (15 / 42) | 167 | 70 | 41.9 |
| Total | 900 | 280 | 140 | 680 (180 / 500) | 2,000 | 840 | 42.0 |
Sums checked: A 140+140+100+120+100+110+100+90 = 900; B 60+60+40+50+30+40 = 280; C 30+30+20+20+20+20 = 140 (C specs: T1 15, T2 15, T3 10, T5 10, T7 10, T8 10); D 118+119+82+88+77+57+82+57 = 680; D ASK 31+31+22+23+21+15+22+15 = 180; D PROCEED 87+88+60+65+56+42+60+42 = 500; totals 348+349+242+258+227+167+242+167 = 2,000; ASK 146+146+102+108+96+70+102+70 = 840.
Forms: Q-EARLY 360 rows (B 280 + 80 D1; ASK 140 = 38.9%), Q-MID 1,640 rows (ASK 700 = 42.7%): inside the +-5 pp bar of K4.
Cards: ON c01-c04 75%, OFF c05-c06 25% (500 rows; its ASK share must sit in 36-48%: the 70 swap-pair OFF members are ASK, so the other OFF rows are drawn PROCEED-heavy from D1/D2 and the OFF side of paired edits that collapse an ambiguity).
Matched pairs and swaps: A + B + C = 1,320 rows = 66.0% (bar >= 30%). Dev = 10% of spec families (all members of a group stay together). The 1,000-row pilot is a proportional sample of the blocks and triggers.
Tokens (G6): mean <= 800 (design about 600), no row above 1,536, rows above 1,024 tokens <= 10%. Wordings: >= 50 wordings per question form (Q-MID, Q-EARLY), none above 2% of the family.

## 5. Difficulty ladder [CRIT D1, D2; program parameters only]
No published difficulty study is cited for T59. The inventory names the mechanism families (target certainty, intent clarity, missing slot); the levels below are our own program parameters. A row's level = the highest mechanism level on the row, except that L4 is given only when at least two mechanisms sit at L3 or above (else the row is L3). The quad (alarming/calm x risk present/resolved) is mandatory only for T50, T51, T53, T41c and T56, so T59 uses the TWIN RULE and the alarm-surface parity gate (K11) instead.
| Mechanism | L1 | L2 | L3 | L4 |
|---|---|---|---|---|
| m.t59.certainty (visible candidates) | one | two with distinct names | two or three sharing a prefix or an owner | four or more incl. a near-duplicate and a decoy outside the request's pattern |
| m.t59.intent (how the request states intent) | explicit value | implied by an earlier turn | stated, then partly retracted | scope word with two readings plus a card default that belongs to a different slot |
| m.t59.slot (missing slot) | required value absent | value present for a different role | value derivable only by a declared transformation | value only in an earlier tool output (W) vs absent (pair) |
| m.t59.undo | undo tool listed with a long window | short valid window | undo exists but the effect is external to the thread | undo window expires between plan time and step time (dates visible) |
| m.t59.stakes (magnitude / H) | <= 50% | 51-75% | 76-90% or 111-150% | 91-110% |
| m.t59.resolver | none needed | default declared | read listed for the open WORLD fact | read or default listed for a DIFFERENT slot (decoy) |
| m.t59.length | < 500 tokens | 500-800 | 800-1,024 | > 1,024 (cap 1,536) |
Required (K22): >= 25% of rows at L3-L4 (design 30% = 600 rows); every mechanism populates all four levels (each level >= 10% of the mechanism's rows); each trigger >= 20% L3-L4 (design value); L4 >= 8% of the family (160 rows; 80 in a 1,000-row pilot); no more than 55% of L4 rows share a label; each L3-L4 row has an easy-looking twin with the OPPOSITE label (same scenario-id prefix, level <= L2, token count +-15%, same alarm-word presence) for >= 80% of L3-L4 rows.
MEASURED BAR (K29, set-level, once, on the 1,000-row pilot): C2 (C1 if C2 has no weights), read on od-l4b by the orchestrator's pipeline (the lane never calls a model), scores <= 70% on L4 rows. A miss is folded into the ONE combined fix by RAISING the program parameters, never by dropping rows by model score; after the fix a miss is a report line (difficulty is not validity). PRE-FREEZE FIX-TRIGGER, NOT A KILL.

## 6. Levers and held-out material (all by SUBSTITUTION inside the 2,000 unless marked)
Each row carries at most ONE lever tag. A14 (long input), A15 (dialects) and A16 (observation formats) are not carried by L-K (plan 16.9 scope; GV7); the renderer keeps its `dialect` parameter at the default and outputs stay in obsfmt.plain_kv.
- A10 cue wrappers (CONDITIONAL on the Fri 23 probe; GV1: build iff >= 10 of 200 flips, no result by Fri 23 18:00 UTC = not built): 100 rows (5%): A 60, B 20, C 20. Trained wrapper families: wrap.authority, wrap.urgency, wrap.fake_approval. Held out in every lane (GV2): wrap.roleplay, wrap.benign_justification. A wrapped row = the clean row plus ONE wrapper sentence as prefix or suffix of the final user turn; label unchanged; the clean row stays in the family (`twin_of`). LINT (code): a wrapper has no digit, quoted string or id-like token, no consent-naming, and, extending the L-T lint for this family, no autonomy or preference statement ("just do it", "no need to check", "use your judgement") and no instruction about asking, confirming, retrying, stopping or verifying. Real delegation lines (e5) are NEVER wrapper text and stay byte-identical before and after wrapping (K26). Wrapper pools: >= 20 sentences per family, Haiku medium rewords programme seeds under the literal ban (writers never see the list). If the probe says do not build, the 100 rows stay plain.
- A12 character perturbation (unconditional): 150 rows (A 90, B 30, D 30). Natural-language fields only (user turns, request wording); never numbers, ids, names, paths, tool or parameter names. Trained families (GV6): pert.diacritics, pert.spacing, pert.leetspeak, pert.homoglyph, pert.zero_width (U+200B inside a word; no ZWJ/ZWNJ, no Tags block, no variation selectors). Held out everywhere: pert.fullwidth, pert.bidi, pert.upside_down. Role x transform matrix as the L-T library (negation: at most 1 character changed; entity and AUTHORITY: diacritics or zero_width; number: none). A span that does not survive its inverse is DROPPED (`xform_drop`); a transform losing > 25% of its attempts is removed; every perturbed row keeps a clean twin.
- Held-out dev-only rows (A24; OUTSIDE the 2,000, GV9, the T54 precedent): 80 rows (4% of the family size): wrapper 40 (only if A10 is built; else they become transform rows) and transform 40. Tagged `heldout_family` / `split.dev_only`; the mix guard refuses them and the money projection counts only trained rows (GV9). They feed the leave-one-family-out term of S.
- A9 is this family. G10 export: every user turn carries `decision_spans` with ROLE (negation/polarity, number, entity/path/flag, AUTHORITY). AUTHORITY covers a user-stated value that collapses a slot, a delegation line and a qualifier that limits a reading. No `spoken_view` is built here.

## 7. Check at generation [OWNER-ROW; plan 16.1; GV5]
Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train." Every T59 row is written only through the L-0b stamp wrapper (the only write path), per batch of <= 500 rows, same day:
(a) ANSWER CHECKS (each a per-row drop with a reason code): solver A = solver B (K2); render round trip and fact coverage (K1); pair, swap and group integrity (K14); observability of the irreversibility and robust-move facts (K25); names guard against the closed allow-list (K17); token cap per row (K16); PII scrub; decision_spans export with A12 survival; spec-family -> split (K20); no-execution scan (K18); the orthogonality guard of K24.
(b) G13 STAMP: the row goes to the stamp service (single Mac job) and is checked against EVERY registered target with every method listed for that target (OHS-3, OHS-4 and OHS-AC binding for new rows, the OHS-5 hash export from Sat 24, public eval targets, attack literals, internal held-out sets; the R6 scaffolding exemption applies). Hit reports carry row id, target name and method only.
(c) STAMP written to the row manifest: row id, registry sha, method-set version, generator code sha, verdict.
DROPS (GV5). A failed row is dropped and logged. A pair, swap or control twin that fails drops its WHOLE group when the failure is a G13 hit: the spec is retired, never re-worded, re-rendered or regenerated on the same skeleton, and a NEW spec is drawn for the same cell with a new seed (at most 2 attempts per slot; a slot still empty is reported as short, not back-filled from another cell). For NON-G13 answer-check drops the partner may stay (marked `orphan`) and same-skeleton regeneration is allowed. K19 counts FIRST-PASS drops and collateral group members.
Stale stamps: a change to a template, wording pool, wrapper pool, transform or alarm pool after the Thu 22 hash export means a new export and re-stamped rows (plan 16.1 step 6). No unstamped or failed row ever enters a pool. Rows start only after the OHS-5 freeze, the registry sha, manifest v1.1+, a signed stamp service and a signed ruling-to-code conformance record for this code sha (plan 16.1 step 0; the stamp wrapper refuses to run without it). Set-level gates run ONCE on the 1,000-row pilot (first look) and once on the built family, never at the mix.

## 8. Gates

PROBE PROTOCOL (G5, the one L-0 harness): CPU only, no LLM. Held-out split grouped by pair/swap/spec id (no group in both train and held-out; 30% held out, 5 random group splits, mean reported). L2 logistic regression, fixed or inner-CV regularisation, never tuned on held-out. AUC reported as max(AUC, 1-AUC). Upper bound = the 97.5th percentile of 2,000 cluster-bootstrap resamples over held-out groups. Every run includes a label-permutation check (AUC 0.50 +- 0.03) and an injected-leak power check (a planted one-feature leak must reach AUC >= 0.80), else the run is invalid and repeated (not a fix iteration). Binary bar: AUC <= 0.55 AND bound <= 0.60. k-way: balanced accuracy <= 1/k + 3 pp AND bound <= 1/k + 6 pp. GBT probes are advisory. Pilot-pooled sub-block probes are allowed (GV8); the built-family read binds.

### 8.1 PRE-FREEZE KILL (CPU, data only unless marked)
| ID | Gate | Bar |
|---|---|---|
| K1 | Render round trip and fact coverage (PER ROW): B's parse of the rendered row recovers every slot, candidate, constraint, effect/undo fact, planned step and card slot; every determining fact is visible in the stated view | pilot drop rate <= 5% target; KILL > 10% after the fix; a template or operator dropping > 25% is removed |
| K2 | Solver A vs B agreement (PER ROW) | >= 99.0% on the 1,000-row pilot (creation drops from this cause <= 1.0%); every disagreement logged and adjudicated; > 1.0% = spec ambiguity = the fix |
| K3 | Rule truth table (code level, re-run at every code sha) | 100% agreement of the rule function, the brute-force oracle and the imported-kind mappings |
| K4 | Label and cell balance | PROCEED >= 55% (design 58.0%; accept 55-65%); ASK >= 35%; per trigger ASK 39-45% (design 42%); Q-EARLY and Q-MID ASK within +-5 pp of the family; per card kind, per world kind and per view ASK 36-48%; block sizes within +-2 pp |
| K5 | TRIGGER-ONLY probe (plan gate): trigger id (8 values), form, view, world kind, card kind -> ASK vs PROCEED | AUC <= 0.55, bound <= 0.60 |
| K6 | Request-text-only probe (user turns only, TF-IDF 1-2 grams, min_df 3) -> ASK vs PROCEED | AUC <= 0.55, bound <= 0.60 |
| K7 | Value-span parity and reference parity: counts of value-bearing spans (numbers, ids, quoted strings, dates) in the user turns, ASK vs PROCEED; rows that refer to a value by pronoun or "the same one" | total-variation distance <= 0.05; PROCEED share of reference-phrased rows 45-55% (the reference resolves in a prior turn vs not) |
| K8 | Structure-only probe (token length, turn count, tools listed, slot count, option letter, wording id, template id, form, view; NOT the candidate count, undo facts or card clauses) | AUC <= 0.55, bound <= 0.60 |
| K9 | Card probe: card id alone -> label (family minus block C); swap pairs | AUC <= 0.55, bound <= 0.60; 100% of swap pairs differ in label; swap members byte-identical except the card clause lines |
| K10 | Candidate-count probe: visible candidate count k_vis in {0 (open), 1, 2, 3, 4+} alone -> label | AUC <= 0.55, bound <= 0.60; k_vis >= 2 rows PROCEED share 35-55% |
| K11 | Alarm-surface parity: a closed alarm vocabulary (code side, not shown to writers) in the task or user turn | presence 25-35% inside each label and each trigger; presence-only probe AUC <= 0.55, bound <= 0.60 |
| K12 | Edit-field coverage | every trigger uses >= 3 edit fields, none > 40% of its pairs; e3/e4/e11 only on ON cards; each edit field >= 2% of pairs |
| K13 | Matched pairs and swaps share | >= 30% (design 66.0%) |
| K14 | Pair, swap and group integrity (PER GROUP): the two members differ in exactly ONE registered edit field (a swap: only the card clause lines); the rendered difference is confined to that field's spans (span map); labels differ | 100%; a failing group is dropped whole |
| K15 | Wording pools | >= 50 wordings per question form, none > 2%; Haiku slot round trip TWO-WAY [Opus b1b GV12]: (a) values, counts, negations, names, candidates survive verbatim and (b) no decision-bearing span is ADDED (no new value, candidate, qualifier, delegation line, default, precedence, undo or stakes statement; closed-lexicon scan plus solver B's parse) 100% else drop-only |
| K16 | Token budget (G6) | mean <= 800; none > 1,536; > 1,024 on <= 10% |
| K17 | Names guard (PER ROW) | 100% of policy, tool, language, runner and carrier names on the frozen allow-list; namespace nouns pass the deny-list program; 0 exact G13 target strings |
| K18 | No-execution scan (CODE): no subprocess, exec or eval on a rendered string; parse-only calls | 0 violations (CPU test, re-run at every code sha) |
| K19 | Stamp drops on ALL rows (first-pass, collateral group members included) | <= 1% for reasons other than exempt R6 scaffolding hits or OHS-5 collisions, read on all 1,000 pilot rows and each full-generation day; > 1% = the ONE combined fix; OHS-5 collisions dropped row by row, <= 5% not the fix (above 5% is) |
| K20 | Split and held-out hygiene | 100% spec-family -> split; dev-only and heldout_family ids absent from every training pool and from the mix manifest (mix guard test): 0 leaks |
| K21 | Standard pipeline (G2: pre-freeze data audits): A50 G6 at size, A49c balance, G5-H (two Haiku solvers on 300 rows plus one read of 100% of the free-form user turns), G3-H, A43(d) Opus confirmation | as the pipeline defines them; a flag counts only after Sonnet medium adjudication, Opus confirmation and a program re-run |
| K22 | Ladder structure (section 5) | as section 5 |
| K23 | G9 cross-family consistency (section 9) | 100% label equality on every leg before any pilot |
| K24 | Orthogonality guard (T59 never labels permission) [Opus b1b T59-M1, GV13]: for every W-REPO row, the action the label leads to (ASK rows: the planned step; PROCEED rows: the planned step, or the robust, resolver or substitute call actually taken) is labelled by the FULL T50 engine (T59 card mapped to the imported T50 kind, ask_on_soft OFF) and by the T51 oracle (contained lane, protected false, MustPreserve empty). Pass iff: never BLOCK; ALLOW, or ASK ONLY through T50 R18 / T51 inferred_target, and in that case the T59 label is ASK on an OFF card and may be PROCEED only on an ON card (the visible `clause.t59.undo_proceed` line is the difference, leg (e)). Any other T50 or T51 ASK (opaque construct, unnamed soft destroy, unauthorised lane mutation, ...) means the spec is NOT built | 100% |
| K25 | Observability of the decisive facts: every ON-mode ASK has a visible irreversibility fact; every ON-mode PROCEED that rests on reversibility shows visible undo evidence; every robust-move row shows the robust call in the tool list or card | 100% (solver B recovers them) |
| K26 | A10 wrappers (ONLY if built) | wrapper-presence probe AUC <= 0.55, bound <= 0.60; lint 0 violations; AUTHORITY spans and delegation lines byte-identical before and after wrapping 100%; clean twin present 100%; 0 held-out wrapper rows in train |
| K27 | A12 perturbation | 100% of kept perturbed rows have all decision spans restored by the recorded inverse and a clean twin; 0 held-out transform rows in train; perturbation-presence probe AUC <= 0.55, bound <= 0.60; PROCEED share of perturbed rows within +-5 pp of the family |
| K28 | Hash export | every template, wording pool, wrapper pool, alarm pool and transform in the Thu 22 export v1.1; 0 unexported at the first row |
| K29 | C2 (or C1) <= 70% on L4 rows (od-l4b read of our own model) | PRE-FREEZE FIX-TRIGGER, NOT A KILL: a miss is folded into the ONE combined fix; after it a miss is a report line |
| K30 | Resolver and default coverage | rows settled by default, precedence or resolver (R-DEF, R-RES) 15-25% of PROCEED rows; rows PROCEED by R-COM (common step) >= 8% of PROCEED rows; PROCEED-by-reversibility (ON mode) 25-40% of PROCEED rows |
| K31 | Delegation-line parity | among rows carrying a delegation line: PROCEED share 45-60%; >= 30% of delegation-line rows name a DIFFERENT slot (decoy, label ASK or PROCEED by the other facts); line-presence-only probe AUC <= 0.55, bound <= 0.60 |

### 8.2 POST-TRAINING REPORT (needs the trained C2.1; never a kill rule)
| ID | Report line |
|---|---|
| P1 | PAIRED accuracy (both members of a pair correct) per trigger with cluster-bootstrap CIs, beside trivial baselines: always-PROCEED, always-ASK, majority, request-keyword rule, card-only, random, and the base 4B |
| P2 | Over-ask rate (ASK where gold PROCEED) and under-ask rate (PROCEED where gold ASK), separately, per trigger and per reversible/irreversible stratum |
| P3 | Card-swap accuracy (does the model read the card line): flip rate across the 70 swap pairs and accuracy on each member |
| P4 | Q-EARLY vs Q-MID accuracy; P vs W view; W-TOOL vs W-REPO |
| P5 | Accuracy by ladder level L1-L4 and by mechanism; C2 vs C2.1 on L4 |
| P6 | Held-out lines (our dev rows): held-out wrapper families, held-out transform families vs in-family; wrapped vs clean twin flip rate |
| P7 | Delegation-line slice: accuracy on real vs decoy delegation lines |
| P8 | Flip rate under option permutation with CI; ECE (bin count stated), Brier, trap-slice ECE |
| P9 | "OHS-5 only" decision type: ask-or-proceed has no usable public eval; the report says "our items". The L-R dialogue realism rows (below) are reported by the L-R lane, not here |

## 9. G9 cross-family consistency (K23; must pass 100% before any pilot) [T54-B1; GV; plan 16.4]
The T59 engine is implemented from the text of section 3 independently of the other engines; the test is a real comparison of labels, not one function called twice. The other families' oracles are imported read-only at their hash exports (T54 `t54_label_oracle(record, card) -> label`; the T51 oracle; the T50 R18 engine; the T55 ledger simulator `tool_engine.ledger`; until an export exists the leg runs against a stub with the same API and is marked pending). A disagreement is a T59 defect (the other families are approved and hashed).
- Leg (a) T54. Every T54 S1, S3 and S4 record with gold in {CALL, WRITE, READ_FIRST, ASK} is mapped to a T59 spec (INTENT slot = the required parameter; WORLD slot = the S4 fact; card kind per the imported table) and labelled in OFF mode: CALL, WRITE, READ_FIRST -> PROCEED; ASK -> ASK. T54 labels NO_TOOL, ANSWER, RESULT_MISSING, DONE_NO_CALL and all of S2, S5, S6 are unmapped (T59 has no such action). On a T54 card T59's oracle gives T54's label (T54-B1).
- Leg (b) T51. T51 rows with violation_set in {none, inferred_target} and a non-empty mutation set, contained lane, protected false, MustPreserve empty: none (every mutated entity authorised, including a trajectory-licensed one) -> PROCEED; inferred_target -> ASK. violation_set unauthorised_unprotected (over-reach by a clear request), must_preserve and protected (BLOCK) are unmapped: they are permission questions, not ambiguity.
- Leg (c) T50. R18 INFERRED-TARGET specs: exact target -> PROCEED; glob or fuzzy target resolving beyond the named set -> ASK. T50's other rules are unmapped.
- Leg (d) T55. B1, B2 and B4 records for the error classes of 3.3.1 mapped as: RETRY, FIX_ARGS, SWITCH_TOOL, RETRY_KEYED, READ_BACK, NO_RETRY, RETRY_PLAIN -> PROCEED; ASK -> ASK; STOP unmapped. B3, B5 and B6 are not generated by T59 and are unmapped.
- Leg (e) ON vs OFF coherence: for every swap pair the OFF member's label equals the imported-kind label of the same spec and the ON member differs exactly when all A(i) are UNDOABLE and the spec is not robust.
- The mapping tables are frozen as a hashed file by the builder before the pilot (sha beside the rule hash). The IRREV function is also compared with the T60 engine's (T60 K22): the two implement D3 independently from this text.

## 10. Clean-room notes
- Built only from the plan, the stripped tools excerpt, the approved families and the lever sheet. No original generator, template, wording pool, OHS-AC or benchmark item text was opened. Public benchmarks for under-specified and abstaining agents are cited only as the source of MECHANISMS (target certainty, intent clarity, missing slot, paired single-detail contrast); their item strings, entity names, ID patterns and prompt wording are G13 targets and are never copied. Domains (files, branches, jobs, tickets, accounts) may be the same as public ones; only exact strings are targets.
- Names: every company, repo, host, service, table, ticket, candidate and policy display name comes from the seeded TRAINING-salt namespace; no hand-picked fake names. Real names are only the closed tool verbs and the T50 programs of section 11.
- AgentAbstain, ClarifyBench and the other ask-or-abstain corpora are barred as DATA (plan list); the lever sheet's figures for them are motivation, not claims, and drive no decision.
- Realism slice: the plan's real-dialogue slice (ABCD, MultiWOZ 2.2 system acts, Taskmaster) is block R (LR-17, LR-18, LR-19, family ids LR-dialogue), uses the datasets' OWN act labels through the L-R recast table, is outside the 2,000 and outside every T59 probe. L-K never opens those datasets or their test splits. Whether the L-R recast text reuses the T59 question form is the L-R lane's call (O-K8).
- No external source in T59: the manifest records "no external source". Writers (Haiku wording pools) get slots and question forms, never the literal-ban list. G13 hit reports carry row ids, target name and method only.

## 11. NAMES this family needs (names only; for manifest v1.2, due Fri 23 12:00; no strings generated here)
Family id: `T59` (already in row_job_families_allowed). No new tool verb, parameter role, language or runner. W-REPO planned steps reuse T50 allow-list programs only: prog.git, prog.rm, prog.mv, prog.cp, prog.mkdir, prog.touch, prog.tar, prog.kubectl, prog.psql, prog.sqlite3, prog.scancel. W-TOOL reuses the T54 verbs and parameter roles (verb.get, list, find, read, check, create, add, update, set, rename, move, copy, remove, delete, cancel, restore, send, schedule, reserve, release, archive, export, import, sync, lock, unlock, lookup; param.*) and the arch.* archetypes.
NEW ids:
- Policy cards: `card.t59.c01`, `card.t59.c02`, `card.t59.c03`, `card.t59.c04` (ON), `card.t59.c05`, `card.t59.c06` (OFF). Clauses: `clause.t59.undo_proceed`, `clause.t59.ask_on_ambiguity`, `clause.t59.stakes_threshold`, `clause.t59.defaults_count`, `clause.t59.precedence`, `clause.t59.read_first`, `clause.t59.retry_cap`. Definitions card: `defs_card.t59`.
- Carriers (logical ids): `carrier.planned_step`, `carrier.candidate_list`, `carrier.tool_undo_note`. Reused: carrier.user_turn, carrier.user_multi_turn, carrier.call_history_list, carrier.tool_output, carrier.tool_output_listing, carrier.tool_output_error, carrier.tool_output_ledger, carrier.tool_output_timeout, carrier.shell_exec.
- Triggers: `trg.t59.missing_param`, `trg.t59.ambiguous_spec`, `trg.t59.conflicting_constraints`, `trg.t59.high_stakes`, `trg.t59.missing_capability`, `trg.t59.tool_failure`, `trg.t59.conflicting_evidence`, `trg.t59.midrun_risk`. Forms: `form.t59.mid`, `form.t59.early`. Views reuse `view.primary`, `view.with_outputs`. Slot kinds: `slot.intent`, `slot.world`, `slot.cap`. World kinds: `world.t59.tool`, `world.t59.repo`.
- Edit fields: `edit.t59.value_stated`, `.default_declared`, `.undo_present`, `.magnitude_below`, `.delegation_line`, `.qualifier_added`, `.single_match`, `.common_step`, `.constraint_loosened`, `.precedence_line`, `.external_cleared`, `.substitute_listed`, `.capability_present`, `.reread_listed`, `.sources_agree`, `.no_fork`, `.key_offered`, `.read_path`, `.equiv_tool`, `.arg_detail` (20).
- Control kinds: `ctl.t59.unambiguous`, `ctl.t59.settled`, `ctl.t59.reversible_ambiguity`, `ctl.t59.clear_ask`. Effect kinds: `eff.read`, `eff.create`, `eff.update`, `eff.move`, `eff.delete`, `eff.send`, `eff.publish`, `eff.reserve`, `eff.schedule`.
- Ladder mechanisms: `m.t59.certainty`, `m.t59.intent`, `m.t59.slot`, `m.t59.undo`, `m.t59.stakes`, `m.t59.resolver`, `m.t59.length`. Per-family hash bucket: `bucket.t59`.
- Shared lever ids reused as they are: wrap.authority, wrap.urgency, wrap.fake_approval, wrap.roleplay, wrap.benign_justification, wrap_pos.prefix, wrap_pos.suffix, pool.wrap.<family>, pert.*, lever.a10, lever.a12, lever.none, split.dev_only, heldout_family, ladder.l1..ladder.l4. New pool ids: `pool.t59.alarm`, `pool.t59.wording.mid`, `pool.t59.wording.early`.
- Imported card kinds for the G9 test only (already in the manifest): card.t54.strict_ask, card.t54.defaults_ok, card.t54.read_before_write, card.t51.c01-c06, card.t50.c01-c08.
- Namespace kinds: existing ns.noun.entity, ns.noun.field, ns.handle, ns.ticket, ns.branch, ns.path_stem, ns.context, ns.job_id, ns.policy_card; no new kind. Magnitude units are ns.noun.entity nouns.

## 12. Risks
1. IRREV carries a numeric threshold (magnitude >= H) that is a design choice, not a published one. Mitigation: H is a visible card number, never hidden; stakes levels cluster at 91-110% only at L4; P2 reports over-ask and under-ask by stratum.
2. The ON-card line makes "ambiguity + undoable = PROCEED" the native policy; some products want ASK always. Mitigation: OFF cards (25%) and 70 swap pairs force card reading (K9, P3); the model is not taught one global policy.
3. About 40% of rows share logic with T50/T51/T54/T55. Mitigation: G9 legs (a)-(e); mix-time dedup on skeleton ids; the imported-kind mapping is restricted to the overlapping domain on purpose.
4. Majority baseline: PROCEED 58% rewards a lazy PROCEED. Mitigation: P1 and P2 report the baselines; pair accuracy is the headline; 66% of rows are pairs or swaps.
5. The per-trigger quota (39-45%) needs 180 unpaired clear-ASK rows (D4) that have no twin. Mitigation: they are spread pro rata; if the K5 probe still fails, the fix menu re-balances D4 by program.
6. The trigger probe could still read "T5 or T6" as ASK-heavy through the E-empty cases. Mitigation: E-empty ASK cases are spread over triggers T1, T3, T5, T6 and T7 inside D4, not concentrated in T5/T6.
7. Delegation lines are a real user signal; if they leak ("line present = PROCEED") the model learns a shortcut. Mitigation: decoy lines and K31.
8. Q-EARLY is only 18% of rows; the early-gate skill may be thinly taught. Mitigation: it is a form, not a different rule; P4 reports it.
9. Imports not yet on disk (T55 ledger module, T50/T51 oracle exports) can delay K23; the pilot waits for K23 (pre-pilot gate).
10. Free-form user turns are the main wording risk: G5-H reads 100% of them; slot round trip keeps decision spans verbatim.

## 13. One fix iteration and kill rule
- ONE combined fix after the first measured look (G3): the 1,000-row pilot is the first look at every set-level PRE-FREEZE gate (K4-K12, K19, K21, K22, K26-K31) with every row already stamped and answer-checked at creation. Allowed changes: generator parameters, quotas, edit-field mix, wording pools, template ids, alarm pool; NOT the bars. Defects found before the pilot by unit tests, the build skeptic or A/B disagreement on CPU fixtures are build fixes. Changing parameters after seeing pilot numbers and re-running for free is not allowed.
- Pre-declared fix menu: K4/K5/K12 fail -> re-balance trigger and edit quotas and the D4 allocation by program; K6/K7/K8/K10/K11 fail -> re-match value spans, candidate counts and alarm presence at template level (A2, the AFLite-style filter, is the allowed repair for a missed shortcut probe: filtered share <= 30% of the family and reported; it counts as the fix); K9 fail -> more swap pairs inside the 2,000 by substitution; K2 fail -> Opus rules the spec ambiguity; K19 fail -> back to the generator for the template ids named in the hit report (row ids and method only); K22/K29 fail -> raise the m.t59 level parameters.
- After the fix all PRE-FREEZE gates re-run on a fresh 1,000-row pilot with new seeds. A gate still failing, K1 drop rate > 10%, or not through all gates by the DATA FREEZE (declared Thu 29 Oct 12:00 from measured status; fallback Mon 2 Nov 23:59 UTC) rolls T59 to C2.2/C3 with the failing gate and numbers logged.
- G4: the family is kept or killed whole; no trigger, block or form rolls alone. POST-TRAINING lines are never kill rules. K29 is a fix trigger only. T59 never counts toward the 6-of-9 floor.
- Timeline: Sun 18 this file; Mon 19 Opus approval, then code (builder launch only under the measured burn projection, Sk 21); solver B session starts from this file and the schema; Wed 21-Thu 22 build skeptic, conformance map in a separate fresh session, hash export v1.1 Thu 22 (includes the A10/A12 pools either way); Fri 23 free probes (A10) and names v1.2 12:00; Sat 24 18:00 conformance record signed or no T59 rows; Sun 25 rows start through the stamp wrapper.

## 14. Open questions for Opus
- O-K1 Confirm D3: a magnitude at or above the card threshold H counts as non-reversible even when an undo exists (this is how the "high stakes" trigger enters the plan's rule).
- O-K2 Confirm that the ROBUST clause (R-DEF, R-COM, R-RES) is a faithful reading of "the interpretations lead to different actions" (different NEXT actions), and that a read never settles an INTENT slot.
- O-K3 Confirm the G9 legs (a)-(e) and that the imported-kind mapping is restricted to the overlapping domain (unmapped labels listed in section 9), as T54-B1 asks for T54 and by the same logic for T51/T50/T55.
- O-K4 T6 tool failure re-implements the T55 B1/B2 rules in an ASK/PROCEED label space (leg (d) checks it). Keep, or move T6 entirely to T55?
- O-K5 Confirm the delegation line as an in-scope edit field with decoys (G10 role AUTHORITY), and the extra A10 lint (no autonomy or preference statement in a wrapper).
- O-K6 Confirm the per-trigger ASK quota 39-45% (K5) with 180 unpaired clear-ASK controls, instead of a looser probe bar.
- O-K7 Held-out dev-only rows are OUTSIDE the 2,000 (GV9, T54/T55/T56 precedent): confirm, or move inside.
- O-K8 The L-R dialogue slice stays block R with the datasets' own labels, outside T59's probes; confirm, and say whether the L-R recast question text should reuse T59's `defs_card.t59` wording.
- O-K9 Confirm that A14, A15 and A16 are not carried by L-K (plan 16.9 scope; GV7).
- O-K10 Design values to confirm: PROCEED 58%, P 65% / W 35%, W-TOOL 60% / W-REPO 40%, ON cards 75%, L3-L4 30%, A10 100 rows, A12 150 rows, held-out 80 rows.

## 15. What may start now (code, no rows)
spec_k1 schema and effect/undo model; the rule function and brute-force truth-table oracle; trigger templates and the edit-field library; renderers with span maps; the G9 mappers and frozen mapping tables (against stubs until the exports exist); A10 lint and A12 transforms (L-T library, read-only); K1-K31 CPU tests; the quota solver for the per-trigger table; wording-pool skeletons for Haiku. Solver B starts from this file and the schema only. The record builder (stamp wrapper use) needs a signed ruling-to-code conformance record for the current code sha (plan 16.1 step 0). No rows before the OHS-5 freeze.

## Opus batch-1b rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; families/G0_APPROVALS_v32.md "Batch 1b")

VERDICT: REVISE -> APPROVED after the 3 fixes below (applied in this file, marked "[Opus b1b ...]"). Code may start now;
rows only after the OHS-5 freeze, the registry sha, manifest v1.2, a signed stamp service and a signed conformance record
(Sat 24 18:00 rules unchanged). The build skeptic checks the code against this block and refuses a review without it.

Must-fix (applied):
- T59-M1 (GV13) K24 widened: the action the label leads to must be ALLOW under the full T50 engine and the T51 oracle, or
  ASK only through R18 / inferred_target with the ON-card exception; any other T50/T51 ASK or any BLOCK = spec not built.
  Reason: a W-REPO PROCEED row whose step T50 would ASK for another reason (opaque construct, unnamed soft destroy) gives
  the same visible action two "ask the user" answers under cards that do not differ in a visible line (G9).
- T59-M2 D3: a `create` is UNDOABLE only if not external (an invite or a published object reaches people outside the
  thread). T60 R1 uses the amended text (T60 leg (a)).
- T59-M3 D5: R-SAME (NOT DIFF) is an explicit ROBUST clause and a truth-table input, so the gold carries the plan's
  "lead to different actions" condition by name instead of through R-COM by implication.

Binding conditions (copy into the code review; the conformance map covers each):
- T59-B1 O-K1 confirmed: magnitude >= H (a visible card number) counts as IRREV even with an undo path.
- T59-B2 O-K2 confirmed with M3; a read never settles an INTENT slot.
- T59-B3 O-K3 confirmed: legs (a)-(e) as written, restricted to the overlapping domain; every leg runs the FULL T59 engine
  (GV13); T54-B1 binds (on a T54 card T59's oracle gives T54's label).
- T59-B4 O-K4: T6 stays in T59; T55 is authoritative in its own label space; a leg (d) disagreement is a T59 defect.
- T59-B5 O-K5 confirmed (delegation line in scope, decoys, AUTHORITY role; the extra A10 lint binds).
- T59-B6 O-K6 confirmed (per-trigger ASK 39-45% with the D4 controls; the probe bar is not loosened).
- T59-B7 O-K7: the 80 held-out dev rows are OUTSIDE the 2,000 (GV9).
- T59-B8 O-K8: the L-R dialogue rows (LR-17..LR-19) stay block R, outside T59's probes, and the L-R recast does NOT reuse
  defs_card.t59, the T59 question forms or the T59 wording pools: its question asks what the annotated agent did next (a
  dataset fact), so a dataset act label can never contradict T59's card-dependent gold.
- T59-B9 O-K9 confirmed (A14, A15, A16 not carried; GV7, plan 16.9).
- T59-B10 O-K10 design values confirmed (PROCEED 58%, P 65 / W 35, W-TOOL 60 / W-REPO 40, ON 75%, L3-L4 30%, A10 100,
  A12 150, held-out 80).
- T59-B11 GV12 two-way slot round trip (K15 as amended); GV10 does not apply (2,000 rows: the 1,000-row pilot stands).
- T59-B12 Namespace kinds marked null in manifest v1.1/v1.2 (e.g. ns.noun.entity, ns.ticket, ns.job_id) are filled only after
  L-0 adds the kind to namespace.py (null_kind_rule); the names T59 needs are frozen in manifest v1.2 (section 11 list).
