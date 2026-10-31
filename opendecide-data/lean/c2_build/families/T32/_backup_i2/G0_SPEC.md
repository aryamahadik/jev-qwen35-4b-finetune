# G0-lite T32: commitment ledger in chat (kept / broken / not yet due / not triggered / waived)

C2_DATA_SPEC 2.1 (T32, 800 selected rows, wave 2, agent tier) and 3.9. One page: semantics, card text, samplers, traps,
balance, error models, relations, Haiku asks, ambiguity resolutions.
Status: frozen v3 (14 Oct 2026; Stage B pilot fix iteration 1 of at most 2, pilot/PILOT_VERDICT.json F1-F8). v3 changes
only the card (1.1: three styles, placement), the ch_status shares, the twin rates, the ch_due status date, the line
budgets, the pack wiring and how a yn_dneg_broken wording is asked (R14, sections 1.1, 2, 4-7); no rule, gold semantics,
gate or bar changed. v2 followed the Haiku ambiguity pass amb:T32 (H1-H45, haiku/ambiguity/amb_T32.json, section 8;
H43); v2.1 added the Mode F wording note (R13, section 7). The sha256 is T32.G0_SHA256 in plugin.py and
validate_plugin() refuses the plugin if this file changes; a later change needs a new sha, a full test rerun and a note.
Precedence (H44): C2_DATA_SPEC (3.0 rules for every family, 4.1 overlay, 6.3 gates) and PREREG A37 / A38 bind; this
file adds the T32 rules and may only be stricter; c2_select may tighten a share to the spec 3.0 cells, never loosen it.
Names: gates G2-G15, G-SL, G-LEX, G-TW, G3-H, G5-H as in spec 6.3 and c2_build/README.md; mixdev = held-out dev rows;
Mode T / F = spec 3.0 authoring modes; qform = question form id; meta.deep = the depth flag. Rule rows are R1-R16;
samplers are S1-S5 (H45). Code: plugin.py (solver A), solver_b.py (solver B), packs_v2.py (the 30 frozen packs both
solvers read), vocab.py + fixtures.py (stand-ins for the unit tests), authoring.py (the Haiku authoring tasks).
## 1. Semantics table (exact; R9's order and every status rule are printed on the card)
| # | Item | Semantics |
|---|---|---|
| R1 | Row | state = narrative skin + blank line + chat block [+ blank line + one attack note]. rule card and question: a yes/no row has the card in row.card and the question in instructions, a choice row has card + blank line + question in instructions (1.1). Every fact the gold needs is in the program-rendered chat block; each message body is exactly ONE admitted lexicon form (kind `other`, sem `chat.*`, R4) |
| R2 | People | 2-4 members (single-token first names, distinct), printed `Members: A, B, C`; every sender and addressee is a member (solver B refuses otherwise; H32). AUTH: an optional pinned authority (a member) on cards 0-3; it may be any member, also the asked commitment's maker, and then it adds nobody for that commitment ("never the maker" wins; H1) |
| R3 | Time | Calendar dates only (no time of day, no time-zone offset). Lines are listed in sending order, dates non-decreasing; on one date the listing order is the sending order, so "before", "after", "first", "last" and "latest" always mean listing order (H11). The status date ASOF is in the question; a line counts iff its date <= ASOF. "By D" includes day D. A due date D has passed iff ASOF > D (strict: ASOF = D has not passed; H27). The only dates in a message are its DUE / NEW_DUE slots, in the row's one free kit form, absolute with the year (2026-03-05, 5 March 2026, March 5, 2026, 5 Mar 2026, or one of these with the weekday; v3: on 60% of the rows that drew a dearer form (ISO, month first, weekday) it is 5 March 2026 or 5 Mar 2026): never numeric day/month, never relative ("Friday", "in ten days"); message forms carry no time, day, week, month or number word (lint_message_form; H9, H10) |
| R4 | Events | sem {slot signature}: `chat.commit` {TASK, DUE} the sender commits to do TASK by DUE; `chat.commit_if` {COND, TASK, DUE} the same, depending on event COND; `chat.try` {TASK, DUE} not a commitment; `chat.done` {TASK} the sender says the task is done; `chat.ext_ask` {TASK, NEW_DUE} the sender asks to move the due date to NEW_DUE; `chat.ext_yes` {TASK, NEW_DUE} says yes to NEW_DUE; `chat.ext_no` {TASK} says no; `chat.cond_met` {COND} the event is going ahead; `chat.cond_off` {COND} the event is called off; `chat.release` {TASK} lets the maker off the task; `chat.retract` {TASK} the sender takes the commitment back; `chat.remind` {TASK}, `chat.ack` {} no effect. Only `ext_yes` agrees a new date and only `release` lets the maker off; an ack ("noted, thanks") agrees to nothing and only directly follows the asked commitment line (H15) |
| R5 | Addressee | A commitment is made to the one member its line addresses: `@Name` (chat style) or the `to` column (log style). Every commitment line addresses one member other than its sender (never a group, never itself; H2, H16); `group` in the to column marks a line that addresses nobody (event, remind, ack, half the tries). Addressing on other lines has no effect (H17) |
| R6 | Asked commitment | The unique `chat.commit` / `chat.commit_if` line with TASK = QTASK in the whole chat; its sender is WHO and it is dated <= ASOF (else the row is invalid: never generated, solver A raises, solver B refuses; H13). Its sender is the maker, its addressee the promisee |
| R7 | Allowed | Allowed to say yes to a new date or to let the maker off: the promisee, plus AUTH when pinned, minus the maker (H1) |
| R8 | Due in force | DUE, replaced by NEW_DUE from the listed moment of a counted `chat.ext_yes` on the task from an allowed person (time-indexed; under R10 this equals reading the history at ASOF, as every reply is dated <= the due date in force; H4, H5). An `ext_no`, an unanswered `ext_ask` or a yes from someone not allowed changes nothing (H7); with one ask and one reply at most (R10) no later line withdraws a yes |
| R9 | Status | The first rule that holds (H3, H26): (1) `not_triggered`: commit_if and no counted `chat.cond_met` for its COND (also while pending and after the due date); (2) `waived`: a counted release from an allowed person, dated <= the due date in force, listed before any done (a release then an on-time done is waived; also after a retract); (3) `kept`: a counted done by the maker dated <= the due date in force; (4) `broken`: a counted retract, or ASOF > the due date in force (a counted late done implies it); (5) `not_yet_due`: otherwise. "Let off" always means rule (2) (H28) |
| R10 | Invariants | The generator never breaks these and solver B refuses a row that does: the asked commitment's DUE is later than its line's date (H14); done, retract and ext_ask on the asked task only from the maker; release never from the maker; done / release / retract only after the trigger (the commit line; for a commit_if its cond_met line; H12); the asked event's cond line is listed after the commitment and dated before its first DUE (H12); at most one of done, retract per task, at most one release (after a done: none); at most one ext_ask and one reply on the asked task: the ask's NEW_DUE later than the due date in force, the reply after the ask, dated <= the due date in force, a yes repeating the asked date (H6, H8); releases dated <= the due date in force; at most one cond line per COND; each task names one story: one commitment (with its maker's earlier try for the asked one) or one decoy try (H18); COND events distinct per chat |
| R11 | Card (program text; solver B keeps a copy of all three styles) | See 1.1. `{ADDRESS}` = "the person it @-mentions" (chat) / "the person in its to column" (log); `{AUTH_PART}` = ", and {AUTH} (pinned rule)" or "" |
| R12 | Closed world | CLOSED_WORLD_SENTENCE "The chat is complete: no other message, agreement or event exists.": the listed lines are every line there is; lines after ASOF are listed and do not count, and nothing unlisted happened by ASOF (H29). Only chat-log lines count: the narrative skin and the attack note (no date, no sender, after a blank line) are not chat lines and change nothing (H30, H31) |
| R13 | Narrative skin | Slots TOPIC (category, pack topics) and OWNER (name, a member: the member who saved, exported or shared the chat; a Mode F intro states that role in words, as the G3-H read extracts it, and naming OWNER only as a participant fails it). Mode T >= 60%; Mode F <= 40% (Haiku intro from a brief of TOPIC and OWNER; G-SL fact-lock + G3-H on those two). The skin is background only: it names no task, event, date, promise, agreement or outcome (brief + G-SL; H30) |
| R14 | Questions | `ch_status`: choice over the closed 5 (Kept / Broken / Not yet due / Not triggered / Waived), all five on every row in a label-blind shuffle per row; a wrong option records the error models that give it, else role `closed` (H25). `ch_due`: a 3-option choice of dates (answer set "open": dates, not a label set; never free text), gold = the due date in force at ASOF, options in the row's ASOF date form, gold position uniform (H19). `yn_broken` yes iff broken, complements `yn_not_broken` (syntactic) and `yn_other_than_broken` (implicit, "a status other than broken"); `yn_dneg_broken` (polarity +1, a logical double negation asked as a truth evaluation, "Is the following statement true: it is not the case that X has not broken ...?": yes iff broken; H23, F8; not drawn, yn_broken instead, while no admitted wording has that frame); `yn_kept` yes iff kept, complement `yn_not_kept` (syntactic); `yn_kept_vs` (yes/no, yes iff kept: "kept, rather than broken, waived, not triggered or not yet due") with complement `yn_unkept_vs` (option framing: yes iff one of the four others, "rather than kept"); "rather than" excludes, and the four names are exactly the rest of the closed set (H24). Yes/no never abstains; no abstain option exists |
| R15 | Depth | Counted lines on the asked commitment among: its cond line, its ext reply (yes or no, allowed or not; one at most), its done / retract / release (1 each). deep iff >= 3 (<= 10%, `meta.deep`; H33). Nothing is computed beyond one date comparison per event. v3: the target depth of a spec (not ch_due) is drawn from the seed, 1 (52%), 2 (42%), 3 (6%; Not triggered at most 2), and the story is drawn again until it has that depth, so depth does not predict the status (G6 d_meta) |
| R16 | Solvers | A (`event_sourcing`, plugin.py `_fold`): the counted lines in listing order folded through a state machine (none -> waiting (commit_if) / active -> retracted -> terminal); the due date passing is a transition: a counted line dated after the due date in force turns an active or retracted commitment broken first, and at the end ASOF > due does (R3 strict; H34). B (`sql_sqlite`): the parsed messages loaded into sqlite, each fact one aggregate query (first counted done, release, retract, latest allowed yes), the status one SQL CASE in R9 order; it enforces R10. A construction table (story plans) steers samplers and predicts twins; it never sets gold |
### 1.1 Card text (the rule card; v3: three styles of the same rules)
    Count only chat lines sent on or before the question's date, in the order listed.
    - A commitment: the sender says they will do a task by a date (that day included), made to {ADDRESS}; saying
      they will try is not one.
    - Its due date: that date, replaced by a new date once someone allowed says yes to it.
    - Status: the first of these that fits.
    - Not triggered: it depends on an event that no line says is going ahead.
    - Waived: someone allowed lets the maker off by the due date, before the maker says it is done.
    - Kept: its maker says it is done by the due date.
    - Broken: the maker took it back, or its due date is before the question's date.
    - Not yet due: none of the above.
    - Allowed to say yes to a new date or let the maker off: the person it was made to{AUTH_PART}, never the maker.
    The chat is complete: no other message, agreement or event exists.

One line per rule in the row; the wrapping above is for this page only ("The due date" is always the due date in force,
H4; the status lines are in R9 order, H3). This is the full style (the v2 text). compact = full with: "chat " dropped and
"in the order listed" -> "in listed order"; "A commitment" -> "Commitment", ", made to" -> " to", "that day included" -> "day
included", "saying they will try is not one" -> "trying is not one"; "Its due date" -> "Due date" and "to it" dropped; "the
first of these" -> "the first"; "an event that no line" -> "an event no line"; Waived / Kept: "says it is done" -> "says done";
Broken: "its due date" -> "the due date". short = compact with: "sent " dropped; "it depends on" -> "depends on"; the last
rule "Allowed to say yes or let off: the person it was made to{AUTH_PART}, never the maker." The style is a label-blind draw
from the sampler and seed alone (a row and its partners print the same style): full 10%, compact 75%, short 15% (spec 3.0).
Placement: a yes/no row has the card in row.card (the served prompt prints it once) and only the question in instructions;
a choice row has it at the head of its instructions (printed twice; the only place a choice row prints rules). Solver B
reads both layouts (cards.split_rules) and keeps its own copy of the three texts.

### 1.2 Chat block (program text)
`Members: P0, P1[, P2[, P3]]`, then `Chat log (oldest first):` + lines `[DATE] SENDER: [@TO ]MESSAGE` (chat style; a
commitment line always carries `@TO`) or `Chat export (date | from | to | message):` + lines `DATE | SENDER | TO-or-group
| MESSAGE` (log style; a commitment line always names a member). DATE is pinned (chat `5 Mar 2026`, log ISO); dates
inside messages take the row's free date form (R3). Addressed lines: commit, ext_ask, done, retract (to the promisee);
ext replies and releases (to the maker); try (to another member, half the time). An attack note (inv twins) follows
after a blank line (R12).
## 2. Samplers (>= 4 training shapes + held-out S5)
| Sampler | Shape | Style | Notes |
|---|---|---|---|
| S1 | forward: story plan for the asked commitment + 1-2 decoy commitments | chat | 2-4 members, <= 6 lines |
| S2 | label-first near-miss: boundary dates (done / ASOF at due or due + 1), one-condition misses (allowed vs not) | chat | 3-4 members, <= 6 lines |
| S3 | export-first: 1-2 decoy commitments, more members | log | <= 7 lines |
| S4 | transcript-heavy: more try / remind / ack lines, after-ASOF lines | chat | 3-4 members, <= 7 lines |
| S5 | held out (mixdev only): held-out skins and registers, year 2027, both styles | log / chat | never a training row |

Cards: (sampler, card 0-5), 30 cards (24 training + 6 S5). A card fixes AUTH presence (cards 0-3), a setting (card
index: home, rental, freelance, team, club, family) and its own pack: card (S<i>, c) uses the i-th pack (by id) of
setting c in pools_v2/packs.jsonl, 30 distinct packs (>= 25, spec 3.0 one pack per card; H39; F7); its narrative skins and
Mode F intros are the ones tagged with setting c (drawn register first, setting-specific registers weighted 3, universal ones 0.8: each register <= 15%); the 6 stand-in packs of vocab.py serve the unit tests only. About 50 rows are GENERATED per training card (1.5 x 800 = 1,200 over 24 cards); selected
rows per card <= 64 (H38). Yes/no seed pairs share qform and card (gold balanced by pair).
## 3. Traps (floor shares of specs; overlapping; tags in `meta.edge`)
The tests measure each tag's share of 2,000 specs (seeds 0-399 x S1-S5; a spec counts for every tag it carries) against
0.8 x floor, bounds inclusive (H36). Tags are computed from the story; `latest_misleads` compares t32_latest_message
with the gold (H35).

| Tag | Floor | Construction |
|---|---|---|
| `latest_misleads` | 25% | the last counted line on the task points to another status (late done, not-allowed release, retract then a not-allowed release) |
| `boundary` | 30% | done dated on the due date or the day after; ASOF on the due date or the day after |
| `conditional` | 30% | the asked commitment depends on an event (met, called off, or unresolved) |
| `extension` | 25% | a request for more time on the task (yes from allowed, yes from not allowed, no, unanswered) |
| `unallowed_move` | 20% | a release or a yes to a new date from a member who is not allowed |
| `try_decoy` | 20% | the maker first said they would try, with another date |
| `after_asof` | 12% | a decisive line (done, release, event going ahead) dated after ASOF |
| `retract` | 10% | the maker took it back (then released or not) |
| `late_done` | 5% | the maker reports it done after the due date in force (broken) |
| `auth_third` | 4% | the pinned AUTH (not the promisee) releases or agrees a date |

Skins are label-blind: the same skins, wordings and message forms serve every status. Attack notes never change gold.

## 4. Balance targets (generator level; bands inclusive, on the same 2,000 specs; c2_select tightens to spec 3.0)
- Base question forms: ch_status 40%, ch_due 13%, yn_broken 12%, yn_kept 20.5%, yn_kept_vs 10.5%, yn_dneg_broken 4% (v3: fitted
  so that yes/no is 45-55% of the rows, with partners, and twins are 20-25% (choice twins only)).
- Gold yes 50% on every yes/no base form (seed pairs); generator band 50 +- 3 pp.
- ch_status gold: the EMITTED rows (base + twin + equiv / attack) are 20% each (F3): "Not triggered" is the unique longest
  label, so another share moves gold-is-longest and lets a status prior predict the gold. Base shares kept 25.5%, broken
  12.5%, not yet due 19%, not triggered 27.5%, waived 15.5% (each in 12-30%) with the twin thinning of section 6 were fitted
  on 10,000 specs (emitted 19.6-20.4%); refit when the twin supply moves.
- ch_due gold: extended date 50%, original date 50% (band 40-60%); every ch_due spec has an ext_ask whose date is >= 2
  days after the original (H21). Gold position uniform per option count; gold sorted rank uniform over 0..2.
- yes = bad outcome: yn_broken / yn_dneg_broken / yn_not_kept / yn_unkept_vs (yes) vs the rest. Deep rows <= 10%.
- Length (H37): tokens of the 4B model's tokenizer (Qwen3.5-4B tokenizer.json), state + 2 x instructions (card and
  question) + options; family mean <= 800 (v3: card styles, rules in row.card on yes/no rows, <= 6 / 7 lines, message forms at or under the per-sem median length, 60% day-month-year dates); every row <= 2,000 tokens
  (the kit's 3-characters-per-token estimate checks each row); the mixer re-checks with the Haiku forms, so Haiku
  pieces stay short (messages mostly 5-10 words, skins and Mode F intros <= 25 words). Deep rows come from a
  condition plus an extension together; v3: 6% of the specs by the depth plan (R15), and a deep spec gets no equiv or attack partner.
## 5. Error models (every wrong option; spec 3.0; family names carry the prefix `t32_`)
Solver A with one rule swapped: `t32_latest_message` (status read off the last counted line on the task),
`t32_try_as_commitment` (the earlier try date is the due date), `t32_ignore_condition` (a commit_if counts as
unconditional), `t32_anyone_may_agree` (a release or yes from any member counts), `t32_ignore_extension` (allowed yes
ignored), `t32_unaccepted_extension` (the requested date applies whatever the reply), `t32_ignore_status_date` (lines
after ASOF count), `t32_late_done_counts` (a done after the due date counts as kept), `t32_retraction_releases` (taking
it back counts as waived), `drop_inclusive_endpoint` ("by D" read as before D), `t32_wrong_commitment` (answers for
the commitment line nearest the asked one in listing position, the later one on a tie; H22). ch_status shows the closed
set (R14); ch_due shows k = 3 on every row: gold, the asked commitment's other date (ignore / unaccepted extension) and
the neighbouring due date (wrong commitment). In ch_due specs all decoy commitments' due dates fall in one region drawn
per spec (1/3 each): before the original date, strictly between the two asked dates, or after the requested date, never
equal to either (equal option texts drop the spec), so the gold's sorted rank is uniform; the try date is a text trap
only (rank-cue fix; never a lowered k). The status date of a ch_due spec is redrawn from the seed (F4): it equals none of the
three option dates and the gold is the nearest, middle or farthest option 1/3 each (among the ranks the story allows).

## 6. Relations (spec 4.1 overlay; G-TW 100%)
- Complement on EVERY yn_broken (other_than 65%, not 35%), yn_kept (not) and yn_kept_vs (unkept_vs) base (v3: without it
  the chat's status alone predicted the yes/no gold, 65% for a reader of the chat; a pair is balanced per status); same
  state, opposite gold under the closed-world card.
- Minimal-edit twins (F2), mostly on choice rows (v3: a yes/no twin moves the status with the gold, the same shortcut: a yes/no
  seed pair gets its twins together, p = 0.25 when both bases have one, about 10% of the yes/no bases): every ch_status base with an edit gets one, a second with probability 0.75 (ch_due: always, two), a ch_status edit kept with
  probability .58 / .35 / .82 / .89 / 1 when it lands on broken / not yet due / not triggered / waived / kept (thinning
  fitted with the base shares, section 4). One input slot; the prediction is the construction table on the edited story,
  never solver A: `asof` (ASOF to the due date, the day after, or the day before a decisive line), `done_date` (done dated on
  the due date <-> the day after), `release_by` (release sender allowed <-> not), `yes_by` (sender of a yes to a new date
  allowed <-> not; the due date flips), `auth` (the pinned AUTH reassigned to another member; never removed, as the card
  fixes AUTH presence; H42), `cond_flip` (the event line going ahead <-> called off, only with no done / release / retract
  on the task). `asof` is drawn only 30% of the time when another kind exists and never for ch_due (F4). A twin is kept
  only if the row's answer changes and the edited story keeps every R10 invariant.
- Equiv (14%): another container style and another skin, same facts. Inv (8%): one inert attack note. None for a deep spec
  (F5); a yes/no seed pair draws them together.
- G4 metamorphic (checked, never emitted): rename a member everywhere; shift every date by 7 days (ch_due gold +7);
  swap the asked task for an unused task of the pack.

## 7. Haiku asks (after A38 only; Haiku never sees questions, options or gold; authoring.py writes the tasks)
- Message forms: >= 12 admitted casual one-line chat messages (<= 14 words) per sem (13 sems; 24 requested, 36 for the
  three commitment sems), each with exactly its R4 slot signature; Haiku sees DUE / NEW_DUE as {DATE} / {NEW_DATE} ("due"
  is a label word; renamed back on load). No name, number, date, time / day / week word, status word or label word
  outside the slots. Try forms never read as firm promises; ack forms agree to nothing. Admitted by the lexicon unit
  test (no form of another sem matches) + 2/2 blind extraction: two independent Haiku reads in separate chunks each pick
  the form's own meaning from the closed list of 13 (any other pick rejects it; H41). A row draws among the forms at or
  under the sem's median literal length (F6).
- Packs: 30 frozen (5 per setting, one per card; 42 requested): >= 8 task phrases (bare infinitive verb phrases),
  >= 5 events that "go ahead" or "are called off", >= 3 chat topics; every surface unique across the pool. Requested in
  authoring.py (28 tasks): 348 message forms, 42 packs, 168 skins, 120 Mode F intros, 143 wordings, 40 attack notes.
- Narrative skins (Mode T, G-SL): 9 training registers and 2 held-out registers, >= 6 skins each (spec 3.0 caps a skin at
  6 rows, so about 170 are requested), each tagged with the settings it fits (so a card's pack and its skin agree). Mode F
  intros from a brief of a sample TOPIC and OWNER used verbatim (swapped at fill; fact-lock + G3-H). v2.1: each brief
  states OWNER's role and every intro says it in words (OWNER next to saved / exported / shared / posted ...) and is the
  intro itself, not a description of one; a redo round (redo2.py) adds stricter lint before G3-H (the intro read as a Mode
  T skin, a role lint) and draws no sample value that a fixed check refuses (the swap-probe owner, a topic with a
  skin-banned word). G3-H template = register within a round (98%); quarantines stand.
- Question wordings: >= 3 admitted per question form over all ten forms (6 base + 4 partners): >= 30 (H40); spec 3.0 caps
  a wording at 2% of rows, so about 140 are requested, weighted by form share. Slots WHO, QTASK, ASOF. ch_due wordings ask
  for the date by which the task has to be done as of ASOF, counting any agreed change (never the first or the requested
  date; H20). Every yes/no wording reads with its form's polarity (c2_kit.polarity; F1: the yn_other_than_broken wordings
  on "apart from" / "besides" have no negation cue and are left out); a yn_dneg_broken wording is asked as a truth
  evaluation (F8; authoring.REAUTHOR_FORMS; the five v1 wordings are left out until clean ones are admitted).
- Attack notes: inert notes with the OWNER slot (fake authority, "everything is agreed" claims), no label word.
## 8. Ambiguity points and their resolutions
v1 points (all kept): 1. "By D" and a done dated D (kept) or D + 1 (broken) (R3, R9). 2. ASOF = due date: not yet due, not
broken (R3). 3. "I'll try" vs a firm commitment (R4; G-LEX 2/2 on every try form). 4. Retract then release by an allowed
person: waived; retract alone: broken even before the due date (R9). 5. Release or yes from a third member who is neither
promisee nor AUTH: no effect (R7, R8). 6. Unresolved condition after the due date: not triggered (R9). 7. Lines dated
after ASOF are listed but ignored (R3). 8. A late done still makes the commitment broken (R9). 9. The double-negation
wording read as a positive-bias question: logical reading binds (R14); v3 asks it as a truth evaluation (F8). 10. "a
status other than broken" and the "rather than" framings name exactly the closed set (R14). 11. A done claim is taken at
face value (R4); nobody in the chat disputes it (R10).
Haiku pass amb:T32 (H1-H45, in the reader's order; each resolved where named; code changes marked *):
H1 R2, R7 | H2 R5, R10 | H3 R9, card* | H4 R8, card* | H5 R8 | H6 R10 (void, refused) | H7 R8, R10* | H8 R10* |
H9 R3, lint* | H10 R3 | H11 R3 | H12 R10* | H13 R6 | H14 R10* | H15 R4, card* | H16 R5 | H17 R5, 1.2 | H18 R10 |
H19 R14 | H20 section 7 | H21 section 4 | H22 section 5 | H23 R14 | H24 R14 | H25 R14 | H26 R9, card* | H27 R3 |
H28 R9, card* | H29 R12 | H30 R12, R13 | H31 R12 | H32 R2 | H33 R15 | H34 R16 | H35 section 3 | H36 sections 3, 4 |
H37 section 4 | H38 section 2 | H39 section 2 | H40 section 7 | H41 section 7 | H42 section 6 | H43 header |
H44 header | H45 header (rule rows renamed R1-R16).
Code (v2): the card prints R9's order and the due date in force; solver B refuses R10 breaks; tests for H1-H4, H7, H8, H12, H14.

## 9. Resolution and freeze
All points above are fixed by R1-R16, the card (1.1) and sections 2-7. Point 9 follows the sibling families'
double-negation wording and is a G5-H watch item (400 blind reads for T32, quarantine <= 3%). G-SL exception: `yet`
(the status name "not yet due" in yn_kept_vs / yn_unkept_vs wordings). Frozen v3 (v2.1 + the pilot fixes); the sha256
is T32.G0_SHA256 in plugin.py, with the Haiku task id of the pass in T32.G0_AMBIGUITY_PASS.
