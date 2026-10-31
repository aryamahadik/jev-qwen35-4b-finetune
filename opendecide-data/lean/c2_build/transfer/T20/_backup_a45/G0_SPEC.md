# G0-lite T20: incident severity with override precedence and timed escalation (transfer dev only)

C2_DATA_SPEC 2.2 (T20, 300 items, held out, never trained) and 3.20 (a matrix plus an escalation counter, twice in
integer minutes). T20 rows are ordinal (SEV1-SEV4); C2 trains no new ordinal rows (spec 5.2) and T20 is never trained:
every row is dev-only. Status: **frozen v3** (sha256 in plugin.T20Plugin.G0_SHA256) = v2 + fix iteration 1 of the pilot
verdict (F1-F6, section 10); v2 = v1 + the one Haiku ambiguity pass (workflow c2-data-stage-a, task `amb:T20`, 31 points;
plugin.T20Plugin.G0_HAIKU_TASK), resolved in section 8. The severity semantics (R3-R9, R11, R17-R19) did not change
in v3: the card text and its placement, the base mix, the twin rule and the question forms did. Code: plugin.py (solver A), solver_b.py (solver B), fixtures.py
(test stand-ins), haiku_author.py (Haiku pools), roles.py (Mode F reporter role), quarantine.py (pool templates not
rendered).
Names: R1-R21 are semantics rows; S1-S5 are samplers only; "card" = the printed rules (1.1); "floor" = R6 only.

## 1. Semantics table (exact; the card prints every rule a reader needs, R1-R16)

| # | Item | Semantics |
|---|---|---|
| R1 | Facts | Incident id; service, one of payments, login, search, checkout, reports, email, storage, chat; users affected (integer count); reported urgency (outage / degraded / cosmetic); customer data exposed (yes / no); opened; acknowledged (a time or "not acknowledged"); check time; a critical list of two services; a maintenance window (start, end) or "none declared"; team and reporter (names from the card's pack, R21). Every time is a whole minute (seconds 00) with a fixed UTC offset |
| R2 | Domain | opened < check; when acknowledged, opened < ack <= check; window start < end; users >= 0; the critical list is two distinct services of the eight. The generator draws only this domain (plugin.in_domain guards every draw); solver B refuses any other row (ParseError, so G2 drops it). Edge rows (check before opening, an empty window, ack at or before opening) are never generated and have no answer |
| R3 | Impact band | wide if users >= U2; partial if U1 <= users < U2; minimal if users < U1. (U1, U2) is one of (25, 250), (50, 500), (100, 1000), (200, 2000); the card prints "wide if U2 or more users, partial if U1 or more but fewer than U2, otherwise minimal" (inclusive; U1, U2 unitless counts) |
| R4 | Base severity | The card's 3 x 3 matrix: rows = impact (wide, partial, minimal), columns = urgency (outage, degraded, cosmetic), printed as one sentence "Base severity (outage, degraded, cosmetic): wide a, b, c; partial ...; minimal ..."; one of the four variants in plugin.MATRICES, each monotone (a wider band or a harsher urgency is never less severe). SEV1 is the most severe |
| R5 | Step 1 (window) | Opened inside the window (start <= opened < end, compared as instants): one level less severe, capped at SEV4. Judged on opened only; the window has no other effect: escalation due times never move, and an incident opened before the window gets no Step 1 |
| R6 | Step 2 (floor) | Service on the critical list (exact lower-case match) and severity SEV3 or SEV4: set to SEV2 |
| R7 | Step 3 (escalation) | Step j >= 1 is due at opened + j x STEP (STEP one of 15, 20, 30, 45, 60 minutes); it applies iff due <= check (the card says "due at or before the check time") and the incident was not acknowledged at or before the due time; each applying step makes it one level more severe, capped at SEV1 |
| R8 | Step 4 (exposure) | Customer data exposed: SEV1 |
| R9 | Order | Steps 1, 2, 3, 4 in that order (a critical service inside the window ends at SEV2, not SEV3) |
| R10 | Time anchor | Every question asks about the severity at the check time (every wording names the check time: a program check on Haiku wordings, true of the program wordings; the card's step 3 horizon is the check time; v3 no longer repeats the sentence on the card). A step due after the check never applies; nothing after the check counts |
| R11 | Reaches, direction | Severity reaches L iff its number <= L's number (L or more severe): SEV1 reaches SEV2. "More severe" = a smaller number; the card and this spec never use above / below / raise / lower for levels, only more / less severe |
| R12 | Yes/no forms | L in {SEV2, SEV3}, drawn label-blind. yn_reaches ({LEVEL} = L): yes iff it reaches L. yn_double_neg (positive, polarity +1; {LEVEL}; two syntactic negations, negcount (k_all, k_syn) = (2, 2): the outer frame "Is it not the case / true that" plus "does not reach"): yes iff it reaches L; its complement partner is yn_not_reaches (one cue fewer, G-TW). Complements, yes iff it does NOT reach L: yn_below (option framing = a yes/no question about the complementary range, "at {LEVEL_NEXT} or less severe", LEVEL_NEXT = one level less severe than L: SEV3 for SEV2, SEV4 for SEV3); yn_not_reaches ({LEVEL}; one "not" / "n't" over reach); yn_fails ({LEVEL}; "fail(s) to reach", literal: no expected or target level is implied) |
| R13 | ch_sev | No level slot. Closed set SEV1, SEV2, SEV3, SEV4 printed in that fixed order; gold = the severity at the check time; no "cannot tell" option |
| R14 | Answers | The row format (spec 2.4) fixes the tokens: yes/no rows answer yes or no and never abstain; ch_sev rows answer one printed option text (SEV1-SEV4) |
| R15 | Times | Fixed offsets only (no zone names, no DST). One-offset rows: every time shares one offset, and the record prints "minutes from opening to the check" (always) and "minutes from opening to the acknowledgement" (only when acknowledged), exact integer differences printed as unitless counts (no rounding can arise, R1). Two-offset rows (sampler S4, the deep scenario, G4's conversion): opened and the window keep the base offset, the check and the acknowledgement both move to one other offset, and no minute line is printed |
| R16 | Closed world | Printed on every card: "The incident record, the critical list, the maintenance window and these rules are complete: nothing else changes the answer." The narrative skin and an attack line are never record facts (section 6) |
| R17 | Solver A | matrix_counter (plugin.py): band by comparisons, a dict lookup in the matrix, the steps in order; escalation steps = max(0, floor(min(check, ack - 1) / STEP)) on integer minute differences from opening (no ack: floor(check / STEP)); floor division; the max never binds inside R2 |
| R18 | Solver B | simulator (solver_b.py, written from this spec, imports no solver-A code): U1, U2, STEP and the matrix read from the printed card (the style and the variants the record implies, found with cards.split_rules); band by scanning; the clock walked minute by minute on epoch minutes (brute.epoch_minutes), one level more severe at each due step not yet acknowledged; refuses rows outside R2 and printed minutes that disagree with the printed times |
| R19 | Gold | Gold = solver A; G2 needs solver B equal on 100% (a disagreement drops the whole unit; no other tie-break). Construction _sev_c(): a step loop over the record plus the generator's planned window and critical flags (generator intent); it predicts twins; a draw where it, or the planned window flag, disagrees with solver A is redrawn. Haiku output never sets or changes a gold |
| R20 | Depth | 1 (matrix) + active overrides (Steps 1, 2 and 4 whose condition holds, even when a cap or the level means no change) + 1 if any escalation step applies + 1 for two offsets. Override = Step 1, 2 or 4 (the non-escalation steps). deep = depth >= 4, at most 10% of rows (spec 3.0 cap; measured 6.6% of 3,000 draws, each sampler <= 9%) |
| R21 | Packs | One pack per card (12 cards per sampler); a pack holds 3 team names and 4 reporter names (plugin.check_pack); S1-S4 cards use training packs, S5 cards held-out packs. Services are never in a pack (R1) |

### 1.1 Program text

State: narrative skin (Mode T or F); blank line; "Incident {INC_ID} on {SERVICE}:" then "- opened:", "- users affected:", "- urgency reported:", "-
customer data exposed:", "- acknowledged:", "- check time:" [the R15 minute lines], then "Critical services: A, B" and "Maintenance window: S to E"
(both endpoints printed with their offset, the base offset) or "none declared". Layouts: list (S1, S2, S4), two-column table (S3), "export incident:"
block (S5). An inv row adds one attack line after the record, after a blank line. **Rules (F4).** The card sits in `row.card` on a yes/no row (the
served prompt prints it once; instructions = the question) and at the head of the instructions on a choice row (card, blank line, question; printed
twice): cards.place_rules; solver B reads both with cards.split_rules. The card is a cards.CardSpec (plugin.CARD; solver_b.PARTS is the separate
copy): a head line, then the items that apply to the record, one per line (no bullets, no indent: every token counts, spec 3.0), the R16 sentence
last. Styles (structure["card"], drawn from the seed alone, so complement, twin and equiv partners print the same card): full 85%, short 15% (spec
3.0: about 15%); the short style keeps every item (cards.variant_problems) with terser connectives. Items (values in braces; `when` reads only the
record and the question type, never the gold or a slot a twin edits):

    SEV1 is the most severe, SEV4 the least.
    Impact: wide if {U2} or more users, partial if {U1} or more but fewer than {U2}, otherwise minimal.
    Base severity (outage, degraded, cosmetic): wide {MX_W_O}, {MX_W_D}, {MX_W_C}; partial ...; minimal ....
    Then, in order:                                   [steps_window: when a maintenance window is declared]
    1. If opened inside the maintenance window (start included, end excluded): one level less severe, never less severe than SEV4. The window has no other effect.
    2. If the service is on the critical list and less severe than SEV2: SEV2.
    3. A step falls due at each full {STEP} after opening. Each step due at or before the check time: one level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.
    4. If customer data was exposed: SEV1.            [steps_no_window: the same without item 1, items renumbered]
    Times are whole minutes at fixed UTC offsets, compared as points in time.   [when no minute lines are printed]
    An incident reaches a level when its severity is that level or more severe. [when the form is yes/no]
    <the R16 closed-world sentence>

Short style: "SEV1 most severe, SEV4 least.", "In order:", "...; no other effect." (all else as above).

## 2. Samplers and scenarios (all dev-only)

S1 forward; S2 label-first boundaries (users at a threshold or one below it, the acknowledgement exactly at a step's
due time, a window starting exactly at opening); S3 record as a table; S4 on-call narrative with the check and
acknowledgement at another offset; S5 held out (export layout, held-out registers customer_report and exec_summary,
held-out packs). Scenarios are exclusive, one per draw: plain 22, escalation 28, maintenance (window only) 14, floor
(critical only) 12, both (window + critical) 8, exposure 9, deep (escalation + one override, Step 1 or Step 2, and two
offsets) 7 (%). Yes/no draws use these weights; a draw that must not reach L cannot be exposure, floor or both (they always
reach), so it draws among the other four at their weights renormalized (v3; v2 moved them to maintenance, which put a window on 43% of the
non-reaching rows and made the window predict the label, G6). ch_sev draws its gold level first (section 3), then a scenario by the same weights restricted to those
that can give that level. After 300 failed tries a draw falls back to plain. A stray window that misses the opening (it ends at
or before opened, or starts after it) is added to 35% of the draws with no planned window.

## 3. Traps and balance (F3, F1, F2: a stratified plan; the realised shares are measured on ROWS)

Tags: band_boundary, ack_at_step, window_misses, window_start, order_matters (R9 decides), two_offsets. Every outcome
below is drawn BEFORE any structure, from the seed's place in its sampler's stream (plugin.slot_of / strat: each value
exactly once per block, a seeded permutation per block; label-blind); the sampler then draws structure until solver A's
gold agrees (label-first, never a relabel).
- Base kind: 11 of every 20 seeds are ch_sev bases, 9 yes/no bases (yes/no rows 51-53% of ROWS; spec 3.0 band 45-55%;
  the old 40 / 60 mix of specs gave 64.7% of rows, the complement partners being yes/no only).
- ch_sev: the gold level is exactly uniform over SEV1-SEV4 (once per 4 choice bases); the gold position is the level.
- Yes/no: of every 20 bases yn_reaches 10, yn_double_neg 1, yn_below 3, yn_not_reaches 3, yn_fails 3 (polarity +1: 55%).
  Inside each form, reaches / does not reach is exactly 50% and L (SEV2 / SEV3) is exactly 50% of each, so every form's
  yes rate is 50% by construction (G6: no question-form cue). The complement relation (section 5) adds a partner to 50%
  of yes/no bases: a different quantity from the base share.

## 4. Error models (prefix t20_)

band_exclusive ("or more" read as "more than"), skip_maintenance, skip_floor, skip_escalation, skip_exposure,
ignore_ack (escalation continues after the acknowledgement), ack_boundary (an acknowledgement exactly at the due time
does not stop the step), floor_first (R9 order swapped), window_end_inclusive. Each is solver A with one switch.

## 5. Relations (G-TW 100%)

- Complement on 50% of yes/no bases (positive -> below / not / fails, uniform; a complement base -> positive;
  yn_double_neg -> yn_not_reaches, the one exact syntactic partner: one negation cue fewer).
- Minimal-edit twin (F1, F2): 2 of every 5 bases of a class (ch_sev: of a gold level; yes/no: of a form and outcome)
  ask for a twin, so twins are about 22% of rows and, for yes/no, as often a reaching base as a non-reaching one (the
  twin of a reaching base does not reach: twin rows are 50% reaching). A twin changes exactly one input slot of
  plugin.twin_edits: USERS (U1 - 1, U1, U2 - 1, U2), URGENCY (each other value), EXPOSED (flipped), CHECK (onto a step's
  due time or one minute before it), ACK (onto a step's due time or one minute after it; only on a row that has one).
  A premise is never added or removed, the window and the critical list never move, the planned flags stay, so _sev_c
  stays the construction reading; every twin stays in the R2 domain. One edit KIND is drawn uniformly among the kinds
  that give the planned outcome, then one edit of it. yes/no: the answer flips. ch_sev: the twin's level is drawn from
  its own key, uniform over the three levels other than the base's (exactly one of each per 3 twins of a level).
  The planned twin is label-first: the base is redrawn until a single-slot edit with that outcome exists.
  Prediction from _sev_c.
- equiv 12% (another record layout), inv 8% (one attack line; the gold never changes).
- G4 (never emitted): rename the team; shift every time by 7 days; write the check and acknowledgement at +03:00
  (dropping the minute lines, so the card then carries the times sentence).

## 6. Haiku pools (after A38; haiku_author.py; Haiku never sees a record, card, question, option or gold)

1. **Packs** (38 requested: 30 training, 8 held out; admitted >= 25 and >= 6): 3 team names (2-3 ASCII words, the first
   capitalised) and 4 reporter names (first and last); check_pack refuses label words, service names, record words, G-SL
   CORE words, digits, negation cues and a name inside another.
2. **Mode T narrative skins**: training registers pager_alert, oncall_chat, status_page, incident_ticket,
   postmortem_draft, incident_email, runbook_note, handoff_log (4 items x 6 each); held out customer_report,
   exec_summary (4 x 6 each); admitted >= 8 per register. {TEAM} and {REPORTER} each exactly once in every skin text.
   Haiku sees status_page as "status_update" (the chunker's label-word check matches "page" in the register name).
3. **Mode F notes** (author_freeform; facts = one reporter and one team name, each verbatim exactly once): training
   24 x 2, held out 8 x 2; G-SL lint_freeform plus the 6.6 bans; admitted F skins are capped at 20% of each skin pool
   (training, held out), so Mode F stays <= 25% of rows (spec 3.0). **Reporter role (F6, roles.py):** REPORTER is "the
   person who reported it" (G3-H), so the sentence or line holding the name must state that role (raised, reported,
   spotted, flagged, noticed, sent, a "from" label or message / alert from, or a speaker label "<name>:"); an author,
   adder, filer or forwarder, or "note from <name>", is dropped. The extraction schema is not weakened to fit the notes.
4. **Question wordings** (author_wording; lexicon kind question, sem q.t20.<form>): requested ch_sev 30, yn_reaches 30,
   yn_below 12, yn_not_reaches 12, yn_fails 12, yn_double_neg 18 (a new task, word-c; F5); admitted >= 18 / 18 / 6 / 6 /
   6 / 6 (>= 54; spec 3.0: >= 30, each <= 2%). Slots: {INC_ID} once; {LEVEL} once on every yes/no form but yn_below;
   {LEVEL_NEXT} once on yn_below; no level
   slot on ch_sev. Each is one line ending in ?, <= 30 words, and says "at the check time" or "as of the check time".
   yn_reaches uses the verb reach with {LEVEL} as its object or "{LEVEL} or more severe"; yn_below keeps "{LEVEL_NEXT}
   or less severe". Negation counts (k_all, k_syn): yn_not_reaches (1, 1), yn_fails (1, 0, "fail(s) to reach"),
   yn_double_neg (2, 2), others (0, 0). **Polarity (c2_kit.polarity, strict frames):** a yes/no wording reads with its
   form's polarity: no negation over a negative predicate (P1: "falls short of", "stays below", "misses"), parity (P2), no
   contracted negative frame (P3), no "aux + subject + not" frame ("Does incident X not reach ...?", P4) except the
   explicit outer frame "Is it not the case / true that". yn_double_neg: that frame, "not" once more on reach, no other
   negative word; until the pool holds an admitted wording that passes, four PROGRAM wordings (plugin.
   PROGRAM_DN_WORDINGS; solver_b.PROGRAM_DN) are program text, not lexicon forms (no G-LEX; meta.program_wording). Never: exactly, only, just, precisely, ever, eventually, final, finally, still, yet, already, now,
   currently, expected, target, goal, supposed, should. G-LEX 2/2 blind extraction against the five meanings plus
   decoys (exactly the level; reaches it at any time after the check; strictly more severe; the base severity before
   the steps; misses an expected level).
5. **Attack lines** (author_skin, kind attack; 8 x 5 requested; admitted >= 12): one line, 6-25 words, {REPORTER}
   exactly once; pressure or claimed authority only (they may push a vague verdict, such as "keep it at the top").
6. **Scope of the bans.** LABEL_WORDS (severe, severity, escalated, escalate, critical, urgent, minor, major, page,
   paged, reaches, sev; every word form, whole word, any case) apply to Haiku state text only: narrative skins (T and
   F), attack lines and pack names. They never apply to program text (card, record) or to question wordings, which
   need levels and "reach" and are admitted by G-LEX instead. G-SL exceptions: none, so pager_alert skins avoid page,
   pages, paged, paging. Outside the slots a skin, note or attack line carries no time (any temporal expression: clock
   values, dates, weekdays, months, now, ago, this morning, minutes, hours ...), no count or number word, no level (a
   SEV token or a ranking word: high, low, top, worst ...; attack lines excepted for vague ranking words), no service
   name, no record fact (acknowledgement, check, window, maintenance, users, urgency or impact, data exposure) and no
   verdict word (a LABEL_WORDS form, or any word judging how serious or pressing the incident is).
7. The card is program-written in two copies: no precedence or window paraphrases (no 3/3 forms).
8. **Quarantine** (quarantine.py; never relabelled, pools/ not edited): 13 Mode F templates (G3-H 10 by rule, 3
   borderline), the G5-H skin T20-ski-3b2dda71f3 and wording T20-wor-38f9393e8c (reader error, gate not loosened), and
   every wording that fails the polarity rule above (3 yn_not_reaches wordings with the strict frame).

## 7. Own ambiguity points (v1, Claude) and resolution

1. Users exactly at a threshold: the higher band (R3 "or more"). 2. Acknowledged exactly at a step's due time: that step does not apply (R7). 3. Opened exactly at
the window's end: outside; exactly at its start: inside (R5). 4. Critical service inside the window: less severe first, then the floor: SEV2 (R9). 5. Escalation past
SEV1, lowering past SEV4: capped (R5, R7). 6. Times at two offsets: compare instants (R15, card). 7. "Reaches SEV2" when the severity is SEV1: yes (R11). These seven
were not the whole list: section 8 settles the rest.

## 8. Haiku ambiguity pass amb:T20 (31 points verbatim in haiku/ambiguity/amb_T20_points.json; sha256 79bbc7dcb0fde14b9461eecb899b3aa652515614ec2d61e447cf414096fee913)

Map from the pass's point numbers to the resolution (card = new card text in both solvers' copies; gen = generator change; pool = Haiku pools and their program
checks): #1 time anchor: R10 (card) | #2 ack at or before opening: R2 (never generated; solver B refuses), R17 (max(0, .)) | #3 whole minutes: R1, R2 (card) | #4
rounding: R15, R17 (integer minutes, floor division never sees a fraction) | #5 window offsets, empty window: 1.1, R2, R5 | #6 window vs escalation: R5 (card: "no
other effect") | #7 attack lines: R16, 6.5, 6.6 (never facts; program bans) | #8 LEVEL_NEXT: R12 (one level less severe), R13 | #9 reaches: R11 (card), 6.4 (wording
must use reach or "or more severe"; G-LEX decoy "exactly") | #10 option framing: R12 (a yes/no question; answer yes or no) | #11 not / fails: R12, 6.4 (negation
counts; no expectation words; decoy) | #12 answer tokens: R13, R14 | #13 floor: R6 (floor = Step 2; the SEV4 and SEV1 limits are caps) | #14 override, active: R20 |
#15 monotone, orientation: R4 (gen: variant 3 made monotone, one cell) | #16 U1, U2, STEP, card: R3, R7, 1.1 (card verbatim; R17-R19 are never printed) | #17
services: R1, R6 | #18 LABEL_WORDS scope: 6.6 | #19 verdict word, time: 6.6 | #20 each once: 6.2 (per skin text) | #21 deep share: R20 (gen: ch_sev scenarios
weighted; 10% is the cap, 7% the scenario weight) | #22 complement shares: 3 | #23 scenarios: 2 | #24 gold: R19 | #25 offsets: R15 | #26 label collisions: header (R
= rules, S = samplers) | #27 outside terms: section 9 | #28 twin counts: 5 | #29 domain edges: R2 | #30 completeness: section 7 now points here | #31 direction
words: R11 (card says only more / less severe).

## 9. Outside terms (spec 3.0, 4.1, 6.3; none changes an answer)

G2: solver A = solver B; G3: the rendered row parses back to the generator's facts; G4: metamorphic invariance; G-TW: twin and complement checks (exactly one slot
differs, the gold flips as predicted); G-SL: the slot lint and fact lock on Haiku text; G-LEX: lexicon admission by blind extraction (2/2); G3-H: Haiku round-trip
extraction of Mode F facts; A38: the OHS-4 freeze, before any C2 data. Spec 3.0 rules used here: >= 8 registers with >= 2 held out; each skin <= 6 rows; each
register <= 15% of rows; >= 30 wordings, each <= 2%; Mode T >= 75%; fixed UTC offsets, no named zones; deep <= 10%. Spec 4.1: the overlay shares and the closed-world
sentence. They govern text and mix, not semantics.

## 10. Fix iteration 1 (pilot verdict F1-F6; no gate or bar changed, no label moved, no frozen pool edited)

F1/F2 twins (section 5); F3 base mix, stratified plan, shares measured on rows (section 3); F4 card: terse text, the reaches / times / Step 1 items only where they
apply, row.card on yes/no rows, short style 15% (1.1; v3 dropped the repeated "one level less / more severe" clauses, "Escalation:", the sentence "The question is
about the severity at the check time", whose job R10 gives to the wordings); F5 yn_double_neg (R12, section 6); F6 reporter role and quarantine (section 6). F7 (a
load-balanced skin / wording pick, kit level) is not a T20 change. Mean tokens are measured with the pinned tokenizer by pilot spec_3_0.
