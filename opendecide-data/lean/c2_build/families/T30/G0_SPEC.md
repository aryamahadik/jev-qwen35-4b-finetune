# G0-lite T30: clarify or proceed after deduplication (C2 agent tier; C2_DATA_SPEC 2.1, 3.5)

One page (C2_DATA_SPEC 6.2 item 3): a semantics table, one ambiguity listing, one resolution. **v3, FROZEN** on 14 Oct
2026 (pilot fix iteration 1; section 5) on top of v2 (13 Oct 2026, the one Haiku ambiguity pass `amb:T30`, workflow
c2-data-stage-a; 37 points H1-H37, section 4). The sha of
this file is `plugin.T30Plugin.G0_SHA256`; `validate_plugin` refuses the plugin if the file changes, so a later change
is a new version with a new sha and a dated line in section 5. Target 1,400 selected rows (about 2,100 generated),
wave 1. Terms from outside this page: spec 3.0 (Mode T / F, registers, wordings, packs), spec 4.1 (overlay), spec 6.3
(gates G2-G15, G-SL, G-LEX, G-TW, G3-H, G5-H), `c_src/common/negcount.py` (k_all, k_syn), the kit README (relations).

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Facts | record type (12 closed types: 10 training types contact, workspace member, payee, user account, order, file, document, meeting, repository, product listing; 2 held out for S5: ticket, device); a listing of 3-6 entries (G4 adds a 7th), each with a match name, a detail, an identity key and a date; the request: requester USER, action phrase ACTION, requested name REF; the card: letter-case rule NORM (fold or exact), batch limit BATCH_MAX in {1, 2, 3} |
| S2 | Match | an entry matches iff its match field equals REF as a whole string, letter for letter (spaces, hyphens and dots included: titles may hold spaces, keys never do). Nicknames, short or long forms, spelling variants and plurals never match (Kate is not Katherine; `roadmap-old.pdf` is not `roadmap.pdf`). Names are never generated in a second letter case, and NORM never applies to names |
| S3 | Identity | ident(key) = the key in lower case under fold, the key itself under exact. Keys are ASCII, so lower case = casefold. Only contact is email-keyed: its NORM is fixed to fold (not drawn) and its card prints the fold text. No key equals `none` (every key holds `@`, `/` or a digit) |
| S4 | Distinct matches | n = number of distinct idents among the matching entries. Entries with one ident are one record and count once; entries with different idents are different records even when name and detail agree (card: "whatever their other fields say") |
| S5 | Consequence | each pack has 3 low-consequence and 3 consequential action phrases, all quoted in the card's Consequence bullet under their class names; ACTION is one of them verbatim. The class comes from the card only, never from world knowledge |
| S6 | Decision (step) | n = 0: stop (tell the user nothing matched). n = 1: proceed, for either class. n >= 2 and consequential: ask. n >= 2, low and n <= BATCH_MAX: proceed (on all). n >= 2, low and n > BATCH_MAX: ask. n counts distinct records (S4), never entries. BATCH_MAX = 1 means no batching |
| S7 | Never decisive | the dates (a recency decoy), the listing order, the requester, the detail field, the listing container, a note attached to the results |
| S8 | Closed world | every card ends "The search results are complete, and only these rules decide what the agent does." Both the records and the rules are complete; a note adds no record |
| S9 | ch_next | closed pair, always shown: proceed "Go ahead without asking the user", ask "Ask the user which one is meant"; plus stop "Stop and tell the user nothing matched" as the abstain-role option, shown on a label-blind plan draw (SHOW_STOP 0.55 of bases: k = 3, else k = 2) and always when it is gold, gold on 1/k of the rows that show it: over all emitted rows stop 16% (18% of bases), proceed = ask = 42% (each 1/3 of the k = 3 rows, 1/2 of the k = 2 rows). Order: a label-blind permutation of the row key (a twin keeps its base's options in order, G-TW). The texts name the card's three steps: go ahead = on the one match, or on all of them when the batch rule allows; ask = the card's ask step (consequential, or over the limit) |
| S10 | ch_target | gold = the ident of the only distinct match when n = 1, else the abstain key `none` (option text "No single entry: none or several distinct matches"). An option's text is the first listed key surface of its ident. The display is a plan drawn from the row key before the listing (kit choiceplan): k = the number of options shown, abstain included: 3 or 4 (the listing then has >= 5 entries at k = 4); the abstain option is shown on 70% of the rows and always when it is gold; gold is `none` on 1/k of the rows that show it (20.4% of ch_target rows); the gold's visible-length rank among the other options is uniform (kit length_balance). A listing the plan cannot fill is redrawn (up to 400 draws, the plan unchanged) and a twin edit that cannot is skipped; k is never lowered and the abstain option never forced on after a failed build |
| S11 | yes/no forms | predicate proceed: yn_proceed (yes iff proceed), yn_no_hold (yes iff proceed: "need not ask the user and need not stop"), yn_hold (option framing, yes iff ask or stop), yn_not_proceed (syntactic, yes iff not proceed). Predicate ask: yn_ask (yes iff ask), yn_settle (option framing, yes iff proceed or stop). Option framing = one yes/no question that names two steps as alternatives set against the third ("ask the user or stop, rather than go ahead"). Yes/no rows never abstain |
| S12 | Negation counts | negcount on the question wording only (card, options and listing never count): k_all = 0 on every form except yn_not_proceed (k_all = k_syn = 1) and yn_no_hold (k_all = k_syn = 2: two separate cues, never "neither ... nor", which counts once). Pairs: yn_proceed-yn_hold and yn_ask-yn_settle (option framing, 0 / 0); yn_proceed-yn_not_proceed and yn_no_hold-yn_not_proceed (syntactic, one cue apart) |
| S13 | Card (program text) | yes/no rows: the card (box below) is `row.card`, which the served prompt prints once, and the instructions are the question wording alone; choice rows: instructions = the card, one blank line, the question wording (the served prompt prints `row.card` on yes/no rows only). Solver B reads the rules with `cards.split_rules`. Rule constants (no, one, two or more) are rule text, never facts |
| S14 | Listing (program text) | header "Search results for {plural}" + one container of the card's type only: bullet lines ("label: value; ...", one line per entry, no blank line), markdown table, one-line JSON `{"results": [...]}` (field names snake_case), or CSV (S5 only; dates ISO). Other containers write each date in one label-blind form per row. JSON and CSV write keys raw (URL keys always full); bullet and table listings may write an email or path key as code in backticks (same value). S4 adds "Agent step: searching the records for the name in the request." / "Tool output:". An attack twin (kit relation `inv`) appends the attack line as the listing's last line "Note attached to the results: ..." |
| S15 | State layout | state = the request block and the listing block joined by one blank line (S3: listing first). Skins hold no blank line. Choice rows carry their options in the row's option list; the prompt layout is the pinned loader's |
| S16 | Request skin | Mode T only (Mode F is 0% here: REF and ACTION are decisive, so the template parser must read them): {USER}, {ACTION} and {REF} exactly once each, written as "{ACTION} {REF}" (an action phrase ends where the name goes), in any register |
| S17 | Error models (prediction) | ch_next: `dedup_count_entries` (n := entries carrying REF); `dedup_opposite_case_rule` (n under the other NORM); `dedup_nickname_counts` (variants of REF match); `dedup_full_name_match` (REF compared with "first last": types with a last-name detail; no match, so stop); `dedup_ignore_consequence` (class := low); `dedup_ignore_batch_limit` (no limit); `dedup_always_confirm` (ask); `dedup_ask_on_repeated_name` (ask if >= 2 entries carry REF); `dedup_ask_on_no_match` (n = 0: ask); `dedup_guess_most_recent` (n >= 2: proceed); `dedup_guess_on_no_match` (n = 0: proceed); `dedup_stop_on_ambiguity` (n >= 2: stop); `dedup_stop_on_duplicates` (an ident listed twice: stop). ch_target: `dedup_first_listed` / `dedup_last_listed` (ident of entry 1 / of the last entry), `dedup_most_recent_entry` / `dedup_oldest_entry` (ident of the latest- / earliest-dated entry, any name), `dedup_guess_most_recent` (n >= 2: ident of the latest-dated match), `dedup_nickname_counts` (the lone ident when variants count). A model that predicts the gold names nothing. Every wrong ch_target option names >= 1 model; on ch_next the wrong proceed / ask options name one (measured 100%), `stop` is the abstain role, and the rest keep the kit role `closed` |
| S18 | Depth | 2 unstated operations: count the distinct matches (S2-S4), apply the decision (S5-S6). Nothing is printed: the count is the task. No deep rows (`meta.deep`) |
| S19 | Solver A | set algebra: frozenset of casefolded (fold) or raw (exact) keys of the matching entries; one lookup in a decision table keyed by (0 / 1 / 2+, class, n <= limit); a question table maps the step to the answer |
| S20 | Solver B | its own parser (card regex, four container readers, skin template, wording template); sqlite: entries and the card's action table; GROUP BY over `lower(key)` (fold) or `key` with binary-collation name equality; one SQL CASE gives the step |

Card, verbatim (contact pack shown; noun, labels and phrases come from the card's pack, {NORM} from S3):
```
Rules for a request that names a contact:
- Match: an entry matches only if its first name is exactly the name in the request, letter for letter; nicknames,
  short or long forms and spelling variants do not.
- Identity: entries with identical email values, {NORM}, are one contact; entries with different email values are
  different contacts, whatever their other fields say.
- Consequence: low-consequence: "<l1>", "<l2>" and "<l3>". Consequential: "<c1>", "<c2>" and "<c3>".
- Decision: no distinct match: stop and tell the user nothing matched. Exactly one distinct match: go ahead, whatever
  the action. Two or more distinct matches: consequential action: ask the user which one is meant; low-consequence
  action: go ahead on all of them if there are at most {BATCH_MAX} distinct matches, otherwise ask.
- Dates never change the decision.
The search results are complete; only these rules decide what the agent does.
```
(Each bullet is one line in a row.) {NORM} = "with upper and lower case treated as the same" (fold) / "... as different"
(exact); it sits in the Identity bullet only.

## 2. Samplers, shares, traps, balance

- **Shares.** Unless marked "base", a share is of all generated rows of the family (bases, partners and twins), measured
  on generated specs before selection; draws realise them (no rounding rule). "Selected" = the c2_select.py choice from
  the generated rows that pass every gate (G2-G15, G-SL, G3-H, G5-H, G12, G13), inside the spec 3.0 bands (G9, G10).
- **Samplers.** S1 forward (request, listing, card, question). S2 label-first near misses (the target is drawn first, as
  everywhere; every trap probability +0.20). S3 table-first (listing before the request; table or JSON). S4 agent
  transcript (the listing is a tool output). S5 held out: ticket and device types, CSV listing, held-out skins,
  registers and wordings (mixdev only).
- **Cards and packs.** A training card is (sampler S1-S4, c = seed mod 10): type = training type c, pack = pack i of
  that type (i = sampler index 0-3); 40 training cards, about 35-50 rows each. S5: c = seed mod 4, type = ticket (c
  even) or device (c odd), pack c // 2. One pack per card (44 packs >= 25). Per-card yes rate drawn in [0.2, 0.8],
  cards paired antithetically (mean exactly 0.5). Before pools are frozen every card uses its type's built-in pack.
- **Draw order (label-blind first).** Action class (50/50), batch limit (1: 0.15, 2: 0.45, 3: 0.40), listing size (3-6;
  >= 5 at ch_target k = 4; on a low-consequence row >= b + 2, so a listing is never all matches), action phrase,
  letter-case rule (contact: fold, no draw), requester; the choice display plan (S9, S10) from the row key; then the
  target from the plan and a low-discrepancy draw (a 5-dimensional Kronecker sequence: gold, form, display, k, rank);
  then a listing that realises it with exactly two distinct names (one besides REF when it has a match, two when it
  has none; a nickname or near-miss title is one of them when that trap is on), so the number of distinct names
  carries no answer (pilot F4: it gave 60% ask at one or two names, 62% stop at six). Every target is feasible in every
  (class, limit) cell, so the card and request carry no gold signal.
- **Question forms (base rows).** ch_next 42%, ch_target 16%, yes/no 42% (yn_proceed 10, yn_no_hold 3, yn_hold 5,
  yn_not_proceed 5, yn_ask 11, yn_settle 8). After partners, yes/no rows are 45-55% of the family.
- **Gold.** ch_next proceed 42 / ask 42 / stop 16 (S9). ch_target single 79.6 / none 20.4 (S10; none: 40% no match, 60%
  two or three).
  Yes/no 50 +- 2. When a yes/no row's drawn answer makes its predicate false, the step is the other non-stop step 72%
  (predicate proceed: ask; predicate ask: proceed) and stop 28%. "Yes = bad outcome" (spec 3.0) = the share of yes/no
  rows whose form says yes when the agent does not complete the request by itself (yn_hold, yn_not_proceed, yn_ask):
  50 +- 5.
- **Traps (overlapping shares of rows, measured on 2,000 training specs).** Exact duplicates that collapse 31% (the
  duplicate's KEY in another letter case under fold 11%; names never change case); same name, different identity >= 30%
  (52%: every ask row needs n >= 2, so the spec's 30% is a floor), of which same full name, other key 20%;
  low-consequence batch, gold proceed 15%; nickname or near-miss name 14% (35% of no-match rows); case-only key split
  under the exact rule 7%; batch-limit edge (n = limit or limit + 1) 26%. The recency decoy is on every row.
- **Abstain.** The abstain-role option (ch_next stop, ch_target `none`) is gold on 1/k of the rows that show it, in every
  (k, shown) cell, over ALL emitted rows (kit plan_report; wrong on 67%, bar 50%). A twin keeps its base's display: it
  never moves the gold onto an option the base hid (ch_next stop at k = 2; ch_target bases that hide `none` have no
  twin); ch_target twins onto `none` are kept at TWIN_NONE_KEEP = 0.20 (k = 3) / 0.10 (k = 4) (kit abstain_twin_kept).
- **Overlay.** Complement on 40% of yes/no bases (>= 20% of yes/no rows; >= 30% non-syntactic); minimal-edit twin tried
  on yes/no 55% of bases, ch_target 50% of the bases that show `none`, and ch_next by (k, step) with a drawn target step
  (TWIN_NEXT: P -> ask 96% and P -> stop 25% reachable, so the target weights and spawn rates make the twins' gold shares
  equal within each (k, shown) cell); kept when an edit flips the answer and fills the options (20-25% of rows); equiv
  (format twin: same facts, another skin, register and container) 14% of bases; inv (attack twin) 8%. A unit is a base
  row with its complement / equiv / inv partners (<= 3 rows); a twin is its own unit.
- **Relations.** Complement: same state, the partner wording of opposite polarity (S11-S12). Twin (exactly one slot,
  answer predicted from the edited construction): the action across classes; the batch limit to n - 1 or n; a
  duplicate's key to a fresh key (split); a lone match's key (a distinct match listed once) to another match's key with
  the same detail (merge); a non-match's name to REF; a lone match's name to a variant or another name; the letter-case
  rule (not on contact, whose NORM is fixed, nor on ch_target rows, where a case-only split or a NORM flip would give two
  options that differ only by letter case). G4 (answer unchanged): reverse the listing, shift every date by 30 days,
  rename the requester, add an inert entry (a name that is neither REF nor a variant of it, a fresh key with no case-fold
  collision, dated one day after the latest entry), rename REF together with every entry that carries it.
- **Recency.** Dates within a listing are distinct, so "most recent" (largest date) has no ties.
- **Length.** Mean about 770 real tokens (Qwen3.5 tokenizer, instructions twice, row.card once), max about 1,100:
  yes/no rules sit in `row.card` and the card is 25 tokens shorter (S13); the spec 3.0 bounds are 800 and 2,000.

## 3. Haiku tasks (after A38 only; Haiku never sees a question, option or gold; lead files in haiku/author/)

1. **Packs** (4 per training type, 2 per held-out type: 44): noun (singular, plural), four field labels (match, detail,
   identity, date; lower-case words), 3 low + 3 consequential action phrases (lower case; each reads right before the
   name), key format (id pattern with `#` digits, org slugs for email and URL keys, folders for paths), titles and
   near-miss pairs (title types), detail values (team, bank, brand, location types). The type fixes the key kind, the
   match kind (first name or title) and the detail kind; a pack changes surfaces only.
2. **Name seed pools:** first names, nickname or spelling pairs, last names, requester full names.
3. **Request skins** (8 training registers: memo, chat, email, ticket, JSON, YAML, log, form; held out: transcript,
   voicemail): S16 placeholders; add no fact; no blank line; outside the slots none of the G-SL word classes (count,
   date, relative time, quantity, quantifier, modal, hedge, status, operator, negation, name, label word); no urgency,
   target hint ("the usual one", "the new one"), pronoun for the target or doubt word (authoring.SKIN_BANNED); a skin
   works for every type and passes a render / parse probe. Each skin feeds <= 6 rows: >= 350 training skins.
4. **Question wordings** (>= 30 over the 8 forms; each <= 2% of the family's rows; each card's rows use >= 5): no slot;
   the S12 counts; the polarity rule of kit `polarity` (a yes/no wording negates syntactically or uses a negative
   predicate, never both, and has no contracted negative frame); admitted by G-LEX 2/2 extraction to `q.t30.<form>`. Held-out set: a seeded 15% split of each form's
   admitted wordings (>= 3 per form), used by S5 only.
5. **Attack lines** (one line, may use {USER} once): pressure or fake authority that adds no fact about any record, no
   label word, and is original wording (no eval_opi or jagged text: the G13 / G-TPL checks).
6. **Program checks** (families/T30/authoring.py) on pools: names, titles and details hold no digit, brace, comma,
   semicolon, pipe, quote, backtick or colon and no negation cue (negcount, word level: "Nora" passes); no pool name is a
   declared variant of another outside its pair; near-miss titles never appear as titles; action phrases hold no label
   word, CORE quantifier or number word, and none equals another's leading words (word prefix); labels match
   `[a-z][a-z ]*[a-z]`; keys from the format are ASCII, never a negation cue, with a letter-case variant. A failing pack
   is replaced by its type's built-in pack.

## 4. Ambiguity listing

Own points (before the pass): (1) letter case in names; (2) same full name, other key; (3) key case under each NORM,
emails; (4) does N count entries; (5) only a nickname matches; (6) "need not ... need not"; (7) yes/no on a batch row;
(8) ch_target on a batch row; (9) gold key in two cases; (10) an authority note. Haiku pass `amb:T30` (13 Oct; points
verbatim in haiku/ambiguity/amb_T30.json): H1 freeze timing; H2 batch limit vs class; H3 one consequential match;
H4 antecedent of "the list"; H5 class labels of the phrases; H6 card wording on same-name records; H7 contact NORM,
email-keyed types; H8 fold and names; H9 spaces and punctuation in names; H10 "at most N" of what; H11 option texts on
batch rows; H12 does k count abstain; H13 `none` as a key; H14 option framing; H15 k_syn, cues, pairs; H16 which text
negcount reads; H17 card and question placement; H18 "single match"; H19 inv vs inverted, equiv; H20 CSV, glob key,
raw key; H21 most recent, inert; H22 batch weights; H23 duplicates in another case; H24 denominators; H25 "selected";
H26 failing predicate, bad outcome; H27 type count, S5 cards; H28 Mode T / F, name after ACTION; H29 scope of skin
bans; H30 attack line vs inv note; H31 pool checks; H32 error-model predictions; H33 outside terms; H34 generator terms;
H35 "label"; H36 listing types, dates, blank lines; H37 lower vs casefold.

## 5. Resolution (Claude, 13 Oct 2026; code changes: the card text in both solvers, the skin check in `render`,
one built-in phrase "issue refunds to the buyers of" (no quantifier, 3.6); nothing else)

- **v3 (14 Oct 2026, fix iteration 1 after the 1,001-row pilot; PILOT_VERDICT F1-F4, PREREG A37 / A38 / A40, kit
  choiceplan / cards / polarity):** S9 and S10 (display plans, 1/k abstain bands: F1), S13 and the card box (yes/no
  rules in `row.card`, shorter card, new closing sentence: F2), S17 (`dedup_oldest_entry`), section 2 (draw order and
  two distinct names: F4; gold; abstain; twin plan: F3; length). The 2 `yn_not_proceed` wordings that mix a contracted
  frame with "hold off" are quarantined by `polarity.screen` (P1, P3); strict frames (P4) are not adopted. No row of S1-S8,
  S11, S12, S14-S16, S18-S20 changed. The card rules are the v2 rules in fewer words, so the v2 ambiguity pass stands;
  the new wording gets a fresh 100-row two-reader G5-H (pilot_i1).
- Own 1-10: S2-S11 as written. 5: stop (`dedup_guess_on_no_match`, `dedup_ask_on_no_match` are the errors). 9: S10.
- **Card text changed (v2; both solvers):** H2 / H3 / H10: the Decision bullet now says one distinct match goes ahead
  "for a low-consequence or a consequential action" and the limit counts "the number of distinct matches"; the class
  matters only for n >= 2 (S6). H4: the closing sentence names the search results (S8). The box above is the card.
- H1: the freeze takes effect with this v2 (the post-pass text); later points need a new version (header).
- H5, H6: the card quotes the phrases under their class names and says "whatever their other fields say" (box).
- H7: S3 (only contact is email-keyed; NORM fixed to fold, card prints fold). Case twins skip contact and ch_target
  (section 2, Relations: options would differ by case only, and `distractors.build_options` refuses such sets).
- H8, H9: S2 (whole-string match; NORM in the Identity bullet only; titles may hold spaces, keys never do).
  `dedup_full_name_match` compares REF with "first last", so on first-name REFs it predicts no match (stop).
- H11: S9. H12: S10 (k counts every option shown). H13: S3 (no key equals `none`; the option text is a sentence).
- H14, H15, H16: S11, S12 (negcount entries; "need not" = 1 cue; pairs listed; only the question wording counts).
- H17: S13, S15. H18: section 2, Relations ("lone match"). H19: inv = attack twin (kit relation `inv`); equiv = format
  twin; "inverted" (section 5) is the spec 3.0 inverted card, not in v1.
- H20: S14 (CSV only on S5; "glob key" = an email or path key in backticks; raw = the key as stored).
- H21: S17 and section 2 (largest date; dates distinct; inert = neither REF nor a variant, fresh key).
- H22: section 2, Draw order. H23: section 2, Traps (the key changes case). H24, H25: section 2, Shares and Abstain;
  each wording is <= 2% of the family's rows (section 3.4); the 2,000 cap is rendered tokens.
- H26: section 2, Gold (`QuestionForm.yes_is_bad`). H27: S1 (10 + 2 = 12) and section 2, Cards and packs.
- H28: S16 (spec 3.0 modes; "{ACTION} {REF}" adjacent; `render` refuses a skin that writes them apart).
- H29: the bans read the skin's own text (G-SL role "skin"); ACTION phrases are pack text with the section 3.6 checks.
  H30: an attack line is the inv twin's note, last line of the listing; requests never carry one.
- H31: section 3.6 (word-level checks; the id pattern's `#` is filled with digits by the program).
- H32: S17 lists each prediction. H33: header (outside terms named). H34: family = T30; unit and partners: section 2,
  Overlay; label-first: section 2, Samplers; deep: S18; masked-label: spec 3.0, not in v1; twin tried vs kept: Overlay.
- H35: "label-blind" = drawn without the answer; "label word" = a word of an answer option (plugin LABEL_WORDS); "field
  label" = a listing column name. H36: S14 (one type per listing; date form per row; no blank line). H37: S3, S19.

Recorded choices: whitespace in keys is never generated (typed slots carry no spaces), so the card states the case rule
only; the batch rule is a limit (1 = no batching) so card and request carry no gold signal; inverted, few-shot,
masked-label and short-card variants are not in v1 (left to v2 or c2_select).
