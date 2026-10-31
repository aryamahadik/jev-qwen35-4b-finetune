# F3 G0 spec: state tracking and record chains

**XF (3 Oct 2026):** cross-family alignment applied. Earlier sections are edited to match section XF, so each rule is
stated once; if any difference remains, section XF governs.

Family F3, gate G0 only. Spec id `F3.G0.v7`. Date 4 Oct 2026. Written from `C_DATA_SPEC.md` v4 (0-2, 2.1, 2.2 F3,
2.4, 6-11), `C_TRAIN_RECIPE.md` v4 3 and `PREREG_FINAL.md` amendments A15, A16 and A16.1. Status: **G0 final; FROZEN**
(sha256 in `c_src/F3/G0_FROZEN.json`; from the freeze on, this file is read-only for everyone). v2 resolved the first
review (A01-A44, B01-B20, spec conflicts C01-C15; section 8). v3 resolved the round-1 re-review (F3-R1-01 to
F3-R1-22 and spec conflict K1; section 9). v4 resolved the round-2 re-review (F3-R2-01 to F3-R2-11; section 10). v5
resolved the round-3 re-review (F3-R3-01 to F3-R3-07 and spec conflicts F3-R3-C1 and F3-R3-C2; section 11). v6
resolved the remaining round-3 items (F3-R3-08 to F3-R3-10, also in section 11). v7 (final) resolves the round-4
review (F3-R4-01 to F3-R4-04 and spec conflict F3-R4-C1), the cross-family item that names F3 (F3-R4-X3) and ruling
A16.1 (g) on choice rows (F3-R4-05); section 12. F3 has 0 open label-flip ambiguities. Each item has one semantics,
stated where it applies. Where an earlier F3 version and the spec disagreed, the spec wins. Where rows of sections 8,
9, 10, 11 and 12 differ, the later section governs; the earlier rows that v7 touches have been edited to match.

**G14 order.** The sealed suite was frozen first (A15). This file contains no generator code, no data rows, no worked
examples, no domain packs, no style or wording pools and no codebooks. Anything in `<...>` is a placeholder. Domain
packs, wordings and statement paraphrases come from the pack and format agents after the sealed sha256 commit (spec 11,
steps 3-5); no F3 generator runs before this file's sha256 is logged (A16).

**Card semantics are not templates (C10).** The quoted text in section 2 is the meaning each rendered rule must carry.
It is never rendered verbatim. The format agent writes every rendered wording after the sealed sha256 commit. Each
wording passes 7.2 decontamination and the orchestrator's counts-only check against the sealed templates before use.
The G3 statement-id registry maps each wording back to its T id.

**How to read this file (C08).** Sections 1-3 and 5-6 are shared by every F3 generator. Each sampler sheet in section 4
is that generator's one-page G0 spec (spec 8 G0). A sheet gives the sampler's shape, toggles, questions, the T rules its
card states, and the generator rules that are its own. It refers to the shared parts by id.

---

## 1. Skill, sizes and decision forms

**Skill.** Track the state of invented items, holders and document records over 5-40 log entries that include VOID,
CORRECTION, SUPERSEDE, RENAME, MERGE and TRANSFER, and follow ID chains across entries and notices. Every answer is
decidable from the card and the text alone. The gap this targets is pg_multihop (C1 55.3 vs 4B-E 66.7).

| Item | Round 1 | Round 2 (superset) |
|---|---|---|
| Rows (10% of own rows) | 4,500 | 9,000 |
| Cards (spec minimum / F3 target) | >= 80 / 95 | >= 150 / 180 |
| Domain packs used | 95, one per card (spec floor >= 30; R1-11) | 180, one per card (spec floor >= 40) |
| Rows per card | max 128, median about 45 | same |
| Deep items (`meta.deep` true, training rows; depth section) | <= 450 (10%) | <= 900 (10%) |
| Token length | F3 emits no long rows: every row is under 1,900 real tokens, measured with the real tokenizer on the served prompt, which prints `instructions` twice (row layout below; A16.1 (g)); a longer draw is redrawn (R1-19). F13 reuses F3 for long text. Median target 500-900, measured the same way | same |

**Decision forms.**
- **Choice** (about 50% of rows). 2-60 options, in spec 2.1's buckets (2-4: 35%, 5-9: 35%, 10-19: 15%, 20-60: 15%).
  Options are status values, holders, items or record IDs. **No F3 choice row has numeric options (C03).** Quantities
  and counts are asked only as yes/no questions with a T22 threshold. **Every F3 status vocabulary is unordered
  (R2-04):** its values are categories, never the levels of one ordered scale. A pack lint rejects a status list whose
  values carry level numbers or ranks (for example 1 to k, "level 2", "stage B", "tier 3", first / second / third) or
  form a graded scale (low / medium / high and the like). Masked codes (T36) are opaque IDs, never a numbered
  sequence. Holder, item and record options are IDs, not levels. So no F3 row is ordinal under spec 2.4, none carries
  `meta.option_level`, G18 does not apply, and the recipe's A4 row set (`expect_ord_rows`) is unchanged. F3 needs no
  new carve-out from spec 2.4.
- **Yes/no** (45-55% of rows). These are hard 0/1 labels. A yes/no row is made only when the answer is fully decided,
  so a yes/no row never has an abstain gold. Every stem is a question about the domain. It is never a check on an
  answer or option. The G3 grammar rejects any yes/no stem that contains one of the banned words in 2.2 (whole word,
  any case; R1-16) (spec 2.1: the label-check form gets 0 rows; C06).
- **Abstain as gold (display-then-gold, XF01).** Abstain
  appears only as a choice option: `<NEI option>` or `<None option>`. The order is fixed, as in F6 and F10: draw k
  (from the bucket, abstain slots included), then the display, then the gold slot uniformly over the displayed slots;
  then build or reject structures until the gold class matches that slot. A structure whose gold slot is not
  displayed is rejected. Solver B and G15 assert that gold is displayed.
  - An abstain option is shown **only when k >= 3**, and only on rows where it can be gold. No F3 row shows an
    always-wrong abstain option.
  - Open cards: every open-world choice row with k >= 3 shows `<NEI option>` (B11, as amended). Open-world choice
    rows with k = 2 show no abstain option, and their gold is a decided answer. NEI is gold with probability exactly
    1/k on each row that shows it.
  - Closed cards: NEI is never gold, so `<NEI option>` is **never shown** on closed rows. Rows under 2.1 show no
    abstain option (A34).
  - `<None option>` is shown on Q7 rows only, and on every Q7 row (R1-22); Q7 rows have k >= 3. "None of these" is
    gold with probability exactly 1/k on each Q7 row. Q1, Q2, Q3 and Q5 choice rows never show `<None option>`:
    they always list the true answer, except an open-card row whose gold is NEI (it has no single true answer, and
    lists `<NEI option>`).
  - Each abstain option is therefore wrong on 1 - 1/k >= 2/3 of the rows that show it (spec floor 50%), and the
    options-only baseline (G6b) and G7 (p0 = 1/k) sit at chance by construction. G10 checks gold = 1/k +/- 2 pp per
    k bucket and per abstain option, on the selected set, twins included (premise-removal twins that move to NEI are
    counted; the R1-13 quota sampler keeps the band by unit selection, never by relabelling).
  - The family NEI and None shares are now derived counts (sum of 1/k over the rows that show each option) and are
    reported, not tuned. The cross-family ~10% abstain figure is only a mixer count; F3 never tunes toward it.
  - **Gold-NEI ruling (C04, as amended by XF01).** Addendum C5 is not applied in round 1, so F3 never samples a
    per-card gold-NEI rate. Closed cards have 0%, because a complete log decides every question (spec 2.2 F3: "not
    enough information" only when the card says the log may be incomplete). Open cards use 1/k per row, as above.

**Row layout: where the card goes (A16.1 (g); F3-R4-05).** C trains and serves with decoder_io's cygnet style and
`schema_branch_mark` layout (recipe v4; `decoder_io.py` 908c08d7). It prints the card whole on a yes/no row, but on a
choice row it shows only card lines of the form "- `<option text>`: `<definition>`", each on its option's line; every
other card line would be hidden. So every F3 row (base rows and twins, every sampler, 2.1 rows included) is built
through fmt1 `card.render_row_text` (`qtype` "noul" for yes/no, "choice" for choice) and placed as follows:
- **Yes/no rows** (Q1-Q4, Q6, Q8). `card` holds the whole card: every stated T rule, the T36 vocabulary with any
  masked meanings or swapped definitions, illustrations, worked examples, the decision list or rule table. No card
  line begins "- Yes: " or "- No: ".
- **Choice rows** (Q1 and Q2 status choice, Q3, Q5, Q7).
  - `card` holds only option-definition lines from fmt1 `card.render_choice_defs`, named by the exact option text. On
    a masked or swapped card, every status value shown as an option has its line: its T36 code meaning or swapped
    definition. Plain status values and holder, item and record IDs (Q3, Q5, Q7) carry no definition line, so on those
    rows `card` is empty.
  - `instructions` holds everything else the card states, laid out in the card style in the style's instruction
    position order (`render_row_text` moves it there): the task line, every stated T rule (T34's abstain meanings
    included), the T36 value list and the meanings or definitions of status values not shown as options,
    illustrations, worked examples, the decision list or rule table, and on inverted cards the frame sentence (fmt1
    LR15); then the wording and the question.
  - `options` are the option texts exactly as defined. No option text contains ": " or a line break: the pack and wording
    lints reject any status value, masked code, swapped word, ID or abstain-option wording that does.
- **State** (every row) holds only case data: the opening register or snapshot, the entries, notices and ledger tables,
  gap markers and marked note fields. No rule, definition or question text goes in `state`.
- **2.1 rows** follow the same placement. A short card's lines move to `instructions` on choice rows; a no-card row
  has only the wording and the question in `instructions`.
- **Check.** Every row passes fmt1 `card.loader_check` with `card.must_show` (G3 check 8): the decoder_io prompt under
  a random option order shows every card line, rule sentence, definition and example, the gold letter maps back to
  the gold option, and `train_decoder.check_rows` accepts the row. A failure is a generator bug, never a silent drop.
- **Readers of the card text.** The G3 parser reads the card text from the `card` field on yes/no rows and from the
  option-definition lines plus the moved card blocks in `instructions` on choice rows. G6 (a) "question only" and
  (c) "card without question" take the question and the card text as built, before placement, so placement changes
  no G6 input.
- **Length.** `schema_branch_mark` prints `instructions` twice, so moved card text counts twice. Every F3 length
  figure (the < 1,900 cap and redraw, the median, the sidecar `real_tokens`) is the real-tokenizer length of the full
  decoder_io prompt (section 6).

**Entity model (hidden structure; glossary, B01).**

| Kind | Fields | Comes from | Entry types that act on it |
|---|---|---|---|
| holder (3-60; people, units, accounts) | ID only: no status, no balance (A25). Its pack role is a hidden polarity attribute, never a field (R1-05) | named in the register or any entry; exists for the whole log until absorbed | RENAME, MERGE; named by CREATE and TRANSFER |
| item (2-60) | ID; exactly one holder at any time; status (closed list of 3-8 values); optional whole-number quantity >= 0. All items on one card are of one kind (R1-05) | opening register or CREATE | CREATE, SET (status, quantity), ADJUST (quantity), TRANSFER, RENAME |
| document record | ID; its document | the root comes from the register or CREATE; every later record comes from SUPERSEDE | SUPERSEDE |
| entry (5-40) | entry number, date (optional time), type, slots; on S6 also an effective date | the log | - |

"Entity" means any of holder, item or document record. Q1 and Q2 ask about item fields only. Records have no field a
question asks about: Q3 asks only which record is current.

**Item kind and holder role (R1-05).** Each card has exactly one item kind, a plural noun from its pack (for example
`<items>`). Every item on the card, in the register or created later, is of that kind, so `<items>` in Q6 and Q7 means
every item on the card (never a document record). Kind is not a field: no entry sets or corrects it, and no question
asks it. Each holder has a role from the pack. The role is used only for the Q4 and Q8 polarity tag (section 5). No
rule, check or label uses it. When the text describes a holder by its role, no rule mentions roles.

**Entry types.**

| Entry type | What it does | Targets and slots |
|---|---|---|
| CREATE | Creates an item (always names its holder; B16) or a document root record | starting status and quantity may be blank (T9) |
| SET | Sets one field to an exact value | item status or quantity; **never the holder** (A35) |
| ADJUST | Changes a quantity by +n or -n | item quantity |
| TRANSFER | Moves the whole item, with its quantity, from a named sender to a named receiver (B16) | items |
| VOID | Cancels an earlier entry, named by entry number only (R1-02) | SET, ADJUST, TRANSFER, CORRECTION or SUPERSEDE only (not CREATE, RENAME, MERGE, VOID) |
| CORRECTION | Replaces exactly one value in an earlier entry (A11, R1-01). Corrections act per value: of the non-voided corrections to the same value of one entry, the highest-numbered counts; corrections to different values of one entry (a CREATE's starting status and its starting quantity) each apply (T11; R3-01) | Changes only: SET value; ADJUST amount (its size only; the direction stays, R1-08); TRANSFER receiver; CREATE starting status or quantity. Never a date, effective date, sender, item ID, record ID, any holder ID other than a TRANSFER's receiver, or an entry reference. It names its target by entry number only (R1-02) |
| SUPERSEDE | Creates a new record B in A's document; B replaces A | records |
| RENAME | Gives an item or holder a new ID | items, holders |
| MERGE | Holder A is absorbed into holder B | holders only |

**Generator rules.** A program checks these on every row, every twin and every metamorphic variant. A variant that
breaks a rule is skipped and logged, never forced (A41, A42).
1. **Numbering (A04, A14, R1-06, R3-05).** Entry numbers are consecutive integers. On S1-S4 they strictly increase with
   (date, time); on S6 they increase with the recorded date. On S5 the sequence number is the entry number and strictly
   increases with (date, time) too, so sequence order and date order always agree. A VOID or CORRECTION always has a higher number than its target.
   A closed card never has a skipped number. Start points:
   - closed cards, and open explicit-marker or skipped-number cards, start at entry 1 (S4: reference 1). There, a gap
     lies only between two shown entries, never before the first or after the last;
   - only leading-extract cards start at an entry `<N0>` > 1. Their entries from `<N0>` on run with no skipped number
     and no marker: the leading gap is their only gap;
   - on S4, changes inside each notice run `<N>`.1, `<N>`.2, ... with no skips. Gaps are whole notices only.
2. **Times (A05).** Within a card, every entry has a time or none does. S4 and S6 have no times.
3. A void is never voided. VOID and CORRECTION never point at an entry that is missing or not shown.
4. IDs are never reused, and a new ID never equals an earlier one. Look-alike IDs are distinct entities in the
   structure.
5. **Holding, mechanism and marker words (A26, A35, R3-07).** Only a TRANSFER or a MERGE changes an item's holder.
   Status vocabularies never contain a word that implies a change of holder (released, returned, handed over, disposed
   of, lost, moved) or the word "absorbed" (A24). The rule-5 pack lint also rejects any status value, masked code and
   its meaning, swapped word and its definition, item kind, holder or document name, role or ID that, as a whole word in
   any case:
   - equals or inflects an F3 mechanism stem: void, cancel, withdraw, amend, correct, fix, supersede, replace, rename,
     renumber, move, retire, merge, consolidate, absorb, transfer, revert, create, adjust, missing. The lint expands
     each stem to its inflected and derived forms (for example cancelled, canceled, cancellation; withdrawn,
     withdrawal; superseded; replacement; retired, retirement; merged, merger; transferred; reverted, reversal);
   - equals or contains an XF06 marker ("unknown", "not recorded", "none", "no", "0", "null", "false", and the banned
     markers), or the card's `<NEI option>`, `<None option>` or `<gap marker>` wording;
   - contains an entry of the shared negcount lexicon (`c_src/common/negcount.py`, referenced, not edited): an L_core
     token, or any inflection of an implicit-cue verb (lack, fail, deny, refuse, decline, omit, neglect, prevent, rule
     out). So a stem's negcount and its implicit cues come only from the negation cues 2.2 allows, never from a pack
     value (R3-09).
   The swapped-word draw and the masked-meaning draw use the same lint, so no card defines a status by a mechanism
   or marker word (T36).
6. **Transfers (A33, R1-09).** No transfer has the same holder as sender and receiver. This covers two IDs of one
   holder and holds after corrections. With the transfer check off, the sender of every transfer that is not voided
   and names no retired or absorbed ID is the true holder just before it (under alias mode, by either of its IDs),
   after all voids and corrections. The card states this rule (T17), so it binds missing entries on open cards too.
7. **Quantities (A27).** No quantity goes below 0 at any point after voids and corrections.
8. **Supersede (A19).** B is always a fresh record, created by the SUPERSEDE entry. A is the current record of its
   document at that moment. There are no forks, joins, cycles or cross-document edges. A SUPERSEDE may be voided only
   if no other SUPERSEDE of the same document comes between it and the VOID in effect order, with the VOID placed by
   its own order key (rule 10; R2-06). This applies on S6 too.
9. **Renames and merges (A18, A23, R3-02).** Never on S6 cards or open cards. A merge joins two different holders that
   are not absorbed (never two IDs of one holder). No entry renames an absorbed holder. Under either rename mode, no
   entry that takes effect before a rename (after voids and corrections, at its own point) names the new ID that
   rename gives, and no corrected value of such an entry does (rule 10). Rename and merge times decide only whether an entry is valid
   (T14 retire, T15) and which `<items>` a merge passes; in questions, every ID of an entity names its whole history
   (T14).
10. **Corrections and voids (A11, R1-01, R1-02, R1-08).**
    - A VOID or CORRECTION names its target by entry number only (S4: change `<N>`.`<k>`). It never restates the
      target's IDs, values or dates.
    - It acts on its target at the target's own point in effect order (T10, T11, T35). The "an entry that names a
      retired or absorbed ID has no effect" rule (T14, T15) is checked on the corrected target at that point, never on
      the VOID or CORRECTION entry itself.
    - A corrected value must be valid at the target's point in effect order. A new receiver exists there (under either
      rename mode, an ID that a later rename introduces is never used there; rule 9, R3-02), is not retired, not
      absorbed, and not the sender.
    - A CORRECTION that comes after a rename or merge in (date, time, entry number) order never uses, as its new value,
      an ID that is retired or absorbed at its own point. So the new receiver is valid at both points, and no reading
      of T14 or T15 can tell the two points apart.
    - A correction to an ADJUST changes only its size (n >= 1). Its direction stays, and its text restates the
      direction. Rule 7 is checked after the correction.
    - **Order key (R2-06).** A VOID or CORRECTION acts at its target's point (above). Wherever this spec places the
      VOID or CORRECTION entry itself in effect order (rule 8, the decisive entry and its decile, an S6 listing
      sorted by effective date), it uses its own key: S1-S3 (date, time, entry number); S4 (date, reference number,
      change number); S6 (recorded date, entry number), compared with other entries' (effective date, entry number)
      as if the recorded date were an effective date.
11. **Q7 (A30).** Exactly one listed item is held by X at the end, or none when the gold is `<None option>`. Solver B
    checks this.
12. **Options (A21).** Options name each entity by its latest ID only, and no option list names two IDs of one entity.
    Every filler option is named in the row's log: in at least one entry, or in the opening register (an item or
    record listed there, or a holder shown holding an item there) (B09, R2-09).
13. **Abstain options (R1-22, XF01).** `<None option>` appears only on Q7 rows (always there, k >= 3). `<NEI option>`
    appears only on open-card choice rows with k >= 3. Each is gold with probability 1/k (decision forms above).
14. **Item kind (R1-05).** One item kind per card; no entry changes or corrects it.
15. **Query points (R1-03, R1-20, R2-07).** Every question names only items that exist at its query point. Q1 and
    Q2: for "on", "as of", "at the end of" and "at the start of" `<D>`, at that point; for a range, at the start of
    `<D1>`. Q4 "on `<D>`": at the end of `<D>`. Q4 at the end, Q5, and every listed Q7 item (gold and fillers): at the
    end. Q8: its transfer's item exists at the transfer's point (rule 19). On S6, "on", "as of" and "at the end of"
    use `<D>` >= `<D0>`, and "at the start of" and every range start use a date after `<D0>`.
16. **Thresholds (R1-09).** Every threshold `<N>` in Q1, Q2 and Q6 is a whole number >= 1, so no threshold is decided
    by "never below 0" alone.
17. **Inverted cards (R1-12).** Q7 rows occur only on inverted cards, and every row on an inverted card is a Q7 row
    (twins included). Inverted cards are closed, fully stated (never 2.1), and on S1, S2 or S3 only.
18. **One row per problem (R1-18).** The generator emits at most one row per `structure_hash` (section 6). The only
    exception is an attack twin, which shares its clean row's hash.
19. **Creation order (R2-07).** No CREATE names a retired or absorbed ID, so every CREATE takes effect, and its item
    exists from that point to the end of the log (no entry deletes an item). No entry other than an item's CREATE
    names that item earlier in effect order than its CREATE (after voids and corrections, on every twin and variant).
    On open cards, every item the shown text names is in the opening register, is made by a shown CREATE, or (leading
    extracts only) exists before `<N0>`; a missing entry never creates an item the shown text names (solver C's
    CREATE makes only fresh items).
20. **Blanks and markers (XF06; R3-06, R3-C1).** A blank (a field an entry leaves unchanged, or a creation field that
    starts as `<default>`) appears only on rows whose card states its meaning (T8, T9's creation sentence, T42).
    Markdown, CSV, HTML and fixed-width tables write it as an empty cell. JSON, YAML and key-value records write it by
    leaving the key out, and the card's T8 sentence says that a left-out field is a blank. F3 never writes `null`,
    `~`, an empty string or an empty "key:" value, never writes an XF06 unknown marker ("unknown", "not recorded"),
    and never writes "none", "no" or `false` as a field value: in F3 an unknown arises only from open-world gaps (T2). The
    only XF06 marker F3 writes is "0", for a `<quantity>` that is zero (the XF06 zero class; T17, T39). The opening
    register gives every field of every listed `<item>` (all `<items>` on a card have the same fields), so it has no
    blank. A renderer lint rejects each of these, and G3 treats any of them in an F3 row as a parse failure. No-card
    rows contain no blank at all (2.1).

**Card toggles** (they make up the card's stated rule set):
- world: closed or open. Open is 30% +/- 5 of cards, never on S6, with a chronological listing only (A16);
- gap style (open only): explicit marker, skipped numbers, or leading extract;
- rename mode (only on cards whose entries include RENAME): alias or retire;
- transfer check: off or on (closed only);
- lock rule: off or on (closed only). Both may be on, and then T40 replaces T18 and T19 (A01);
- time axis: entry date, or effective date (S6 only);
- times: all entries timed, or none (A05);
- numeric date format (T26);
- listing order (R1-20): chronological (on S6: recorded order); sorted by a stated non-time key (S2 in an S3
  container, S3 only); sorted by effective date (S6 only, stated on the card); or shuffled with timestamps (S3) or
  with both dates (S6);
- status vocabulary: plain, masked codes, or swapped word (T36);
- definition style (below).

**Card distinctness (C11, B06, R1-11).** F3 reads spec 2.1 pairwise, which also meets the looser reading. Every F3
card has its own domain pack: no two F3 cards share a pack, so F3 uses 95 packs in round 1 and 180 in round 2 (above
the spec floors of 30 and 40). In addition, every two F3 cards differ in the stated rule set (the toggles whose
trigger occurs on the card) or in the label schema (the status vocabulary and the set of question types). G11 checks
both conditions over all pairs. A collision is fixed by redrawing one card's toggles or question-type set, never by
editing rows. A toggle whose trigger never occurs on a card is unstated. It never makes two cards distinct, and G11
never counts it.

**Definition styles (C05, A34e).** Spec 2.1 asks for >= 3 styles, with "one-line + 1-2 examples" on about 50% of cards.
G0 also requires that every choice that could flip a label is stated. In F3, "one-line" therefore means a one-line task
definition followed by one line per rule the card's structure triggers.
- **One-line rule list** (about 20% of cards): the task in one line, then each triggered T rule in one line.
- **One-line + 1-2 illustrations** (about 50% of cards): the same, plus 1-2 short illustrations of the riskiest rule
  (for example, how a void acts). The program fills each illustration on a separate mini-structure, solver A checks it,
  and its IDs never appear in the row's log, query or options. Each illustration and worked example sits in a marked
  block that the G3 parser checks against its own mini-structure (R1-17). Illustrations are written only after G14.
- **Decision list or rule table** (about 15-20% of cards): T35, or a table of rule | applies when | effect.
- **Few-shot overlay** (5-10% of cards, on any body style above): 1-3 worked examples. The program draws them from
  separate mini-structures, solver A labels them, and none shares a structure hash with any row or dev item. None
  exist before G14.
- **Short or no card** (about 15% of rows): section 2.1 only.

**Question types** (shares of F3 rows; +/- 3 pp):

| QT | Question | Form | Worlds | Share |
|---|---|---|---|---|
| Q1 | Status of `<item>` at the end; or a `<quantity>` threshold at the end (T22) | status: choice or yes/no; quantity: yes/no only | closed, open | 16% |
| Q2 | Status (or `<quantity>` threshold) on `<D>`; or "at any time between `<D1>` and `<D2>`" | on `<D>`: choice (status only) or yes/no; ranges: yes/no only (A29) | closed | 15% |
| Q3 | Which record of `<document>` is current at the end; or "Is `<R>` the current record of `<document>`?" | choice; yes/no. End of log only (A20) | closed | 15% |
| Q4 | Does `<X>` hold `<Y>` at the end (also asked with "still", and negated with "no longer" inside "Is it true that ...", T31, 2.2 N2); or "Did `<X>` hold `<Y>` on `<D>`?" ("still" and "no longer" only in Q4 end-of-log stems; A32, R3-08) | yes/no | closed; open (end only) | 22% |
| Q5 | Who holds `<Y>` at the end | choice | closed, open | 12% |
| Q6 | Does `<X>` hold at least / at most / more than / fewer than `<N>` `<items>` at the end (distinct items of the card's one kind, T39; `<N>` >= 1) | yes/no only | closed | 5% |
| Q7 | Inverted: which of these `<items>` does `<X>` hold at the end | choice (always with `<None option>`); inverted cards only (R1-12) | closed | 10% |
| Q8 | Did the transfer in entry `<N>` take effect? (S4: change `<N>.<k>`) | yes/no | closed, on cards with the transfer check, lock rule or voids | 5% |

Q1-Q3 supply the choice-to-yes/no balance: Q4, Q6 and Q8 are always yes/no, and Q5 and Q7 always choice.

**Stem words per QT (2.2; R3-08 to R3-10, R4-01 to R4-04).** "Still" and "no longer" appear only in Q4 end-of-log
holding stems, with T31's meaning; no Q1, Q2, Q3, Q5, Q6, Q7 or Q8 stem and no Q4 "on `<D>`" stem uses them. "Between"
appears in a stem only inside "at any time between `<D1>` and `<D2>`" (Q2 ranges, T25). A yes/no stem is negated only
in one of the negated stem forms of 2.2 (N1-N5, and D for double negation), each only in the QTs and stem kinds that
form's row allows, and every card with such a row states T44. The T22 comparator phrases "no fewer than" and "no more
than" are not negation cues of the claim (2.2).

**Inverted cards (R1-12).** An inverted card is a card whose rows are all Q7 rows (with their twins). Q7 appears on no
other card. Two targets are checked separately on the selected set: inverted cards are 10-15% of F3 cards (spec 2.1),
and Q7 rows are 10% +/- 3 of F3 rows.

**Masked and swapped vocabulary (B07, K1).** Masked status codes and swapped status words are properties of a card's
vocabulary. The codes appear everywhere on the row: register, entries, rules and options; their meanings are placed
by the row layout rule above (option-definition lines for codes shown as options on choice rows). The spec 2.1 and 6 quota
counts only **status-option rows**: choice rows whose options are status values (Q1 or Q2 status choice, including on
lock-rule cards). Rows whose options are holders, items or record IDs (Q3, Q5, Q7) never count, even on a masked or
swapped card. Denominator: all F3 choice rows. Masked status-option rows are 10-15% of F3 choice rows; swapped
status-option rows are 5% +/- 1. To make this feasible, about 20-30% of non-inverted cards are masked or swapped, and
on those cards at least 70% of choice rows are status-option rows (planned values; the check is on the selected set).
Other cards lower their status-choice share to keep the QT shares within +/- 3 pp.

**Depth (B02)** = hops on solver B's decisive path:
- 1 to read the writer;
- +1 for each rename or merge alias hop;
- +1 for each supersede hop;
- +1 for each void that removes a candidate writer;
- +1 for each correction applied;
- +1 for each nested transfer check or lock check, plus that check's own hops;
- +1 when the effect order differs from the listing order on the decisive entries.

For Q6 and Q7, depth is the maximum over the items resolved. For a Q2 range, it is the maximum over the snapshots. For
Q8, it is 1 plus the hops needed to decide the transfer's conditions and voids. On NEI rows, depth counts the hops until
the resolver crosses the gap, with the crossing as the last hop. An S4 withdrawal adds +1 only for a VOID it expands to
that removes a candidate writer, never +1 per change in the withdrawn notice (R1-21). The **decisive entry** is the
entry on the decisive path that comes latest in effect order (on NEI rows, the last gap crossed). A VOID or CORRECTION
on the path is placed by its own order key (rule 10), never by its target's point (R2-06). Its **decile** is its rank
in effect order, never its listing position.

**Deep flag (R1-14).** `meta.deep` = (depth >= 5) OR (3-4 unstated additions or subtractions on the decisive path) OR
(a Q6 count over more than 8 candidate items, or with N > 6). A Q6 row's **candidate items** are the items that X
holds at some point in the log under any of X's IDs (opening register or right after any non-voided entry). Depth is
capped at 8, unstated arithmetic at 4 operations, and a deep Q6 count at 20 candidate items with N <= 15. Deep rows
are excluded from the d1-d4 mix and counted only in the <= 10% deep slice.

The default cap is 4. Non-deep mix (rows with `meta.deep` false): d1 15%, d2 30%, d3 30%, d4 25% (+/- 5). Deep rows
are deep training items (<= 10% of F3 rows). The depth sweep's 300 items come from S5 only (B14, C13). Spec 2.1
applies: if more than 30% of rows are hard after the G5 re-read, the cap drops. **Arithmetic (C07):** at most 2
unstated additions or subtractions on the decisive path at default depth, as in F2. At default depth, a Q6 count covers
at most 8 candidate items with N <= 6 (B08).

---

## 2. Semantics table (G0)

Each rule is stated in the card whenever its trigger can occur in that card's items (2.1 rows excepted). Column 3 is the
**card semantics** (normative meaning, not a template; see the header). Wording-pool paraphrases written after G14 are
registered against the T id, and the G3 parser maps each one back to it. "Alt" is the competing reading, written as a
program variant of solver A. The 2.1 check runs these variants.

| # | Topic | Card semantics | Alt (program variant) |
|---|---|---|---|
| T1 | Closed world | "This log is complete: every change to these `<items>`, `<holders>` and `<records>` is listed. Each value stays as it is until a listed entry changes it." | not varied on 2.1 rows (see 2.1) |
| T2 | Open world (A17, A18, B18) | "Some entries are missing from this log. A missing entry could be any entry type this card describes except a rename or a merge, and could concern any `<item>`, `<holder>` or `<record>`. No entry, shown or missing, renames or merges anything: `<holder>` and `<item>` IDs never change, and a superseding record is a new record with its own ID. A value at a point in the log is known if and only if one of these fixes it: (a) the last shown entry at or before that point that sets it to an exact value (a creation, a setting or a transfer, not an increase or decrease), after voids and corrections, comes after every missing entry, and the increases and decreases after that entry are applied to it; (b) it is the holder of an `<item>` just before a shown transfer of that `<item>` that is not voided and comes after every missing entry (the transfer rule in this card names the sender); or (c) it is shown in the `<opening register>` and the point is the opening point, before entry 1 (no entry is missing before entry 1, and no void or correction names the register). Any other value is unknown. If the answer depends on a missing entry, choose '`<NEI option>`'." (R2-08; (c) R3-03: stated on every open card that shows an `<opening register>`, that is explicit-marker and skipped-number cards; leading-extract cards show no register and leave (c) out) Open cards have a chronological listing only and no rename, merge, transfer check, lock rule, Q2, Q3, Q6, Q7, Q8 or S6. Missing entries obey every rule the card states, including T5, T17's open-card sentence and T28 (R1-09). | missing entries only of the shown kinds; NEI only when nothing is said; an increase after the last gap read as a known value |
| T3 | Gap marking (open; A15, A16, R1-04, R1-06) | Explicit: "Entries are numbered from 1. Each '`<gap marker>`' stands for one or more missing entries; entry numbers skip across it. No entry is missing before entry 1 or after the last entry." Skipped: "Entries are numbered in order from 1; each skipped number is one missing entry. No entry is missing before entry 1 or after the last entry." Leading: "This extract starts at entry `<N0>`; earlier entries are not shown, and the state before entry `<N0>` is unknown. Every entry from `<N0>` on is shown." Leading-extract cards show no opening register. Of T9 they state only its creation sentence: "A creation always names the `<item>`'s holder; any other `<field>` it leaves blank starts as '`<default>`'." S4 versions say "notice" and "reference number" for "entry" and "entry number"; gaps are whole notices. The last entry in effect order is always shown. | skipped numbers mean nothing; a blank creation field after a leading gap read as unknown |
| T4 | End of log, "now" (question text only; A06, A07) | "In the question, 'now', 'currently' and 'at the end' mean after every entry in this log has taken effect, not today's date." Cards with a "still" or "no longer" row state T31, whose end point is this one. "Still" and "no longer" appear only in Q4 end-of-log holding stems (2.2; R3-08). | "now" = the last listed entry |
| T5 | Effect order, ties, "at that moment" (A04, A33) | "Entry numbers increase with date and time. Entries take effect in date and time order; entries with the same date and time take effect in entry-number order. The order in which entries are listed does not matter. 'At that moment' means after every entry that takes effect before it." S3 adds T42; S4 uses T41; S6 uses T6. | listing order |
| T6 | Effective dates (S6; A04, A08, A10) | "Each entry takes effect on its effective date, not on the date it was recorded. Entry numbers follow the recorded date, and entries with the same effective date take effect in entry-number order. Voids and corrections have no effective date: they change the entry they name as if it had always read that way. The opening snapshot shows the state at the end of `<D0>`. Every entry takes effect after `<D0>` and on or before `<D_last>`, the last recorded date." | recorded-date order |
| T7 | Retroactive view (A08) | "Answer from the log as it stands now: apply every void and correction, even one recorded after the date you are asked about." S6 adds: "An entry recorded after `<D>` whose effective date is on or before `<D>` counts for `<D>`." | as-recorded view on that date (S6: as known on `<D>`) |
| T8 | Blank fields (XF06; R3-06) | "An entry changes only the fields it names. A blank field means 'no change'." (Creations: T9.) Cards with JSON, YAML or key-value entries add: "A field left out of an entry is a blank field." There a blank is always a left-out key, never `null`, an empty string or an empty "key:" (rule 20). | blank = cleared to `<default>` |
| T9 | Opening state, unset values (B16, B17) | "The `<opening register>` shows the state of every `<item>` and `<record>` before the first entry. A creation always names the `<item>`'s holder; any other `<field>` it leaves blank starts as '`<default>`'." In a closed world, no question asks about a value with no source. | unset = unknown; a blank in a creation = no value |
| T10 | VOID (A02, R1-02) | "A void always names an earlier entry, by its number only. A voided entry counts as never made, no matter when the void was recorded. Every other entry still applies under this card's rules, and every check is made as if the voided entry had never existed." | the void counts only from its own date; later entries apply as written, without re-checking |
| T11 | CORRECTION (A03, A04, A11, R1-02, R1-08) | "A correction always names an earlier entry, by its number only, and changes one value in it: a set value, the size of an increase or decrease (an increase stays an increase, a decrease stays a decrease), a transfer's receiver, or a starting value in a creation. That entry then counts as if it had been recorded with the corrected value, at its own place in the order; the correction's own date does not matter. A correction does not override later entries that set the same field. Corrections act value by value: of the corrections to the same value of one entry that are not voided, the one with the highest entry number counts, and if all of them are voided, that value keeps its original form. Corrections to different values of one entry (a creation's starting `<status>` and its starting `<quantity>`) each apply." (R3-01) | (a) the correction acts as a new latest entry; (b) the latest-dated correction wins (equal under rule 1; still run); (c) when the highest correction is voided, the original value stands; (d) a corrected receiver checked at the correction's own date (never differs by rule 10; still run); (e) per entry, not per value: only the highest-numbered non-voided correction to an entry counts, even when an earlier one changes a different value of it (R3-01) |
| T12 | Void vs correction | "A voided correction has no effect. Correcting a voided entry does not bring it back." | the correction revives the entry; a voided correction still applies |
| T13 | SUPERSEDE (A19, A20) | "When record `<B>` supersedes record `<A>`, `<B>` is a new record of `<A>`'s `<document>`: `<A>` stops being current and `<B>` becomes current. If that superseding entry is voided, it counts as never made: `<B>` never existed, and `<A>` stays current unless another entry supersedes it. Each record is superseded by at most one entry that is not voided. The current record of a `<document>` is the one record in its chain that is not superseded." Q3 asks only about the end of the log. Cards with a Q3 "lack" row add (R3-09): "'Does `<document>` lack `<R>` as its current record?' asks the opposite of 'Is `<R>` the current record of `<document>`?': yes exactly when `<R>` is not the current record of `<document>` at the end of the log, including when `<R>` never existed because the entry that made it was voided." This is Q3's only implicit negation cue. The stem always names one record `<R>`; the G3 stem grammar rejects "lack" in every other form (its declarative "`<document>` lacks `<R>` as its current record" inside a 2.2 D stem is this form), including the document-only "Does `<document>` lack a current record?" (which T13 would make always "no"). A "lack" row is made only on a card that states this sentence (never on a no-card row). | stop one hop early or one hop too far; a voided supersede still counts |
| T14 | RENAME (toggle; A21, A22, A23, R3-02) | Both modes add: "No entry that takes effect before a rename uses the new ID it gives. In questions, every ID of an `<item/holder>` names its whole history in this log, before and after any rename; the date of a rename matters only for which entries are valid." Alias: "A renamed `<item/holder>` keeps its history. Its old and new IDs name the same `<item/holder>` for the whole log, before and after the rename. Entries after the rename, and questions, may use either ID." Retire: "After a rename, only the new ID is valid. An entry that takes effect after the rename and uses the old ID has no effect at all. A corrected entry is checked with its corrected values, at its own place in the order." Under retire, questions never use an old ID. Voids and corrections name only entry numbers, and rule 10 keeps a corrected receiver valid at both the target's point and the correction's point (R1-02). Under both modes, options use only the latest ID (rule 12). Not on S6 or open cards. | (a) the other mode; (b) a new ID names only the history after its rename, so a question that uses it about an earlier point finds no value and no holding there (R3-02); (c) alias only: an old ID names only the history before its rename (R3-02) |
| T15 | MERGE (A24) | "When `<A>` is merged into `<B>`, `<B>` survives. Every `<item>` `<A>` holds passes to `<B>` at that moment, whatever any transfer rule in this card says. After the merge, `<A>` is absorbed: it holds nothing, and an entry that takes effect after the merge and names `<A>` by any of its IDs has no effect. A corrected entry is checked with its corrected values, at its own place in the order." This applies under both rename modes. Not on S6 or open cards. Rule 10 applies as in T14 (R1-02). | the absorbed ID becomes an alias of `<B>`; the merge obeys the transfer check or lock rule |
| T16 | IDs | "IDs must match exactly, character for character. IDs that look alike are different `<items>`, `<holders>` or `<records>`. An ID is never reused." All IDs are written in one case. | IDs within edit distance 2 count as one entity |
| T17 | TRANSFER and holding (A26, B16) | "A transfer moves the whole `<item>`, with its `<quantity>`, from the named sender to the named receiver. Each `<item>` has exactly one holder at any time. Only a transfer or a merge changes who holds an `<item>`; its status never does." Cards whose `<items>` have a `<quantity>` add: "An `<item>` whose `<quantity>` is 0 still exists and still has its holder" (R2-02). With the transfer check off (every open card, and closed cards without T18 or T40), the card adds: "In every transfer that is not voided `<retire or merge cards: and names no retired or absorbed ID>`, the named sender holds the `<item>` just before it." This states rule 6 (R1-09). | an `<item>` with `<quantity>` 0 read as held by no one (Q4, Q5, Q7; R2-02) |
| T18 | Transfer check (check on, lock off; "only if"; A33) | "A transfer takes effect if and only if the named sender holds the `<item>` at that moment. If the sender does not hold it, the transfer changes nothing. Decide this after removing voided entries and applying corrections." Alias cards add: "The sender may be named by any of its IDs." | check ignored; check made on the as-recorded state |
| T19 | Lock rule (lock on, check off; "unless") | "A transfer of an `<item>` takes effect unless the `<item>` has status '`<S>`' at that moment. While its status is '`<S>`', a transfer of it changes nothing." | lock ignored |
| T20 | "unless" (all cards) | Every "A unless B" sentence also states the B case, as T19 does. Reading: A when B is false; not A when B is true. | "unless" read as silent on B |
| T21 | "only if" (all cards) | Every "only if" sentence also states the converse, as T18 does, so it reads "if and only if". | necessary condition only |
| T22 | Thresholds (B12) | "'At least `<N>`' and 'no fewer than `<N>`' include `<N>`. 'At most `<N>`' and 'no more than `<N>`' include `<N>`. 'More than `<N>`' and 'fewer than `<N>`' do not." Used by the Q1, Q2 and Q6 threshold questions. | inclusive and exclusive swapped |
| T23 | "or" (A28) | "'`<X>` or `<Z>`' is true if at least one of them is true." "Or" appears only in questions about one `<item>` at one point in time, and joins two different holders (never two IDs of one holder) or two status values. "Either ... or" is never used. A stem with "or" carries no negation cue and no "still" or "no longer"; its only allowed negation is the outer frame "Is it false that ...", whose scope is the whole claim (2.2). Both disjuncts carry the same polarity tag (section 5) (R2-01). | exclusive or |
| T24 | Date points (A09, A31) | "'On `<D>`', 'as of `<D>`' and 'at the end of `<D>`' mean after every entry dated `<D>` or earlier. 'At the start of `<D>`' means after every entry dated before `<D>` and before any entry dated `<D>`." S6: "dated" becomes "effective", whenever the entry was recorded. No other date phrase is used (2.2). | Each Alt is applied to "on `<D>`" and to "as of `<D>`" (every T24 phrase except "at the end of `<D>`" and "at the start of `<D>`"), in every question type that uses them, Q4 "Did `<X>` hold `<Y>` on `<D>`?" included (R3-04): (a) the phrase = at the start of `<D>`; (b) the phrase = at any time during `<D>`: at the start of `<D>` or right after any entry dated `<D>` (yes/no: true if the claim holds at any of those points; choice: an answer only if every such point gives the same one) (R2-02) |
| T25 | Date ranges (A09, A29, R1-03) | "'Between `<D1>` and `<D2>`' includes both dates. '`<condition>` at any time between `<D1>` and `<D2>`' is true if the condition holds at the start of `<D1>` or right after any entry dated `<D1>` to `<D2>` takes effect, including entries with the same date. A voided entry never counted, not even for a moment, and an entry that changed nothing (a blocked transfer, or an entry naming a retired or absorbed ID) changed no value." The condition is a status value or a `<quantity>` threshold of one `<item>` (Q2 ranges); no question asks a holding range. In question stems, "between `<D1>` and `<D2>`" appears only inside "at any time between `<D1>` and `<D2>`", so every range stem is existential; the G3 stem grammar rejects a bare "between" in a stem (for example a status or threshold "between `<D1>` and `<D2>`" without "at any time"). The bare phrase appears only in this card's inclusivity sentence (2.2; R3-10). S6: "dated" becomes "effective". Range questions are yes/no only. A range stem is negated only by the outer frame "Is it false that ..."; a T22 comparator inside its condition is not a negation of the stem (2.2; R2-01). Under that frame the comparator is "at least", "at most", "more than" or "fewer than", never "no fewer than" or "no more than" (XF10; R3-C2). | (a) end-of-day states only; (b) "between" excludes `<D1>` (the range starts at the end of `<D1>`), excludes `<D2>` (entries dated `<D2>` do not count), or excludes both: three variants (R2-02) |
| T26 | Date format | "Dates are written `<day/month/year \| month/day/year>`." This is required on any card with numeric dates where the day is 12 or less. Other cards use ISO or month-name dates. | the other order |
| T27 | Times | "All times are in the same time zone." No times cross midnight, and there is no daylight-saving change. | - |
| T28 | Rounding, arithmetic (C07, R1-09) | "All `<quantities>` are whole `<units>`; no rounding is needed. No `<quantity>` is ever below 0." Integers only (rule 7). At most 2 unstated additions or subtractions on the decisive path at default depth (as in F2); 3-4 only in deep items. | - |
| T29 | Units | "Each `<quantity>` is in the unit named in its column or entry; no conversion is needed." One unit per field. | - |
| T30 | Ties | Same date and time: T5. Same effective date: T6. Supersede forks cannot occur (rule 8). Counts are exact (T39). F3 asks no "most" or "least" questions (F9 owns argmax with tie rules). | - |
| T31 | "Still / no longer" (A32, R1-07) | "'Does `<X>` still hold `<Y>`?' asks whether `<X>` holds `<Y>` at the end. '`<X>` no longer holds `<Y>`' means `<X>` held `<Y>` at some point in this log but does not hold it at the end. 'At some point' means in the opening state or right after any entry that is not voided takes effect. 'Still' and 'no longer' refer to the end of the log." "Still" and "no longer" are used only in Q4 end-of-log holding stems; the G3 stem grammar rejects them in Q1, Q2, Q3, Q5, Q6, Q7 and Q8 stems, in Q4 "on `<D>`" stems and in "or" stems, so no status, quantity, count, record or transfer question carries them (2.2; R3-08). "Still" never shares a stem with "not" or "n't", and "no longer" stands only inside "Is it true that ..." (2.2 forms N2 and D; R4-01, R4-02). **Generator guard:** a row whose stem contains "still" or "no longer" (base row, neg or dneg twin alike) is made only when `<X>` held `<Y>` in the opening state or at the end of some date, so the presupposition also holds for a reader who uses end-of-day states only; a twin that would fail it is skipped and logged. Under the guard, "`<X>` no longer holds `<Y>`" is the complement of "`<X>` holds `<Y>` at the end", as M9 expects. On open cards, solver A decides the guard from known values (solver A step 4; the opening state is known by T2 (c), R3-03); solver C must confirm it in every possible world on every row made. | "no longer" = "not at the end" (the earlier clause dropped); presupposition failure = no label; end-of-day states only (never differs, by the guard; still run) |
| T32 | Time words inside notices (S4; A07) | "Inside a notice, 'today' means that notice's date." Notices use no other relative time word (2.2). They refer to IDs and to other notices only by explicit number, never by pronoun. | "today" = the end of the log |
| T33 | Notes and injected text (A37) | "Notes and comments inside entries, and notes and postscripts in notices, are not entries; they change nothing." Inert and attack text appears only in a marked note field (S4: a marked note or postscript). It never imitates an entry of a listed type and never parses under the G3 surface grammar. | note text that parses as an entry is applied (never fires by construction; still run) |
| T34 | Abstain options | "'`<NEI option>`' is right exactly when the log, read with these rules, allows more than one answer. '`<None option>`' is right exactly when no listed option is right." (R2-08) | not run on 2.1 rows (no abstain option) |
| T35 | Exception precedence (decision-list style; A43) | "Apply the rules in this order: (1) remove voided entries; (2) apply corrections (of the corrections to the same value of one entry that are not voided, the highest-numbered one counts; corrections to different values of one entry each apply); (3) put the entries in `<date and time \| effective-date>` order, then entry-number order; (4) go through the entries one at a time in that order and apply each one: a creation, setting, increase or decrease, transfer (it takes effect only if every transfer condition this card states holds at that moment), rename, merge or supersede; an entry that names a retired or absorbed ID has no effect; (5) read the value at the time asked." | global passes (all renames and merges first, then all transfers) |
| T36 | Status vocabulary (A44) | "`<field>` takes only these values: `<v1>`, ..., `<vk>`." Masked: "Code `<K>` means `<meaning>`." Swapped: "Here '`<word>`' means `<definition>`." Values are written exactly as listed, with no synonyms. A masked or swapped value's good/bad polarity comes from its card definition, not from the word, and is recorded in the QC sidecar. Every value, code, meaning, swapped word and definition passes the rule-5 lint: none is a mechanism word, an XF06 marker (R3-07) or a negcount lexicon entry (R3-09). | usual word meaning (not run on 2.1 rows: no masked or swapped words there) |
| T37 | Document identity (A19, B01) | "The records of one `<document>` form one chain. It starts with the record in the `<opening register>` or the record a creation makes, and grows only by supersedes. A record belongs to a `<document>` only through its chain." Renames apply to items and holders only, never to records. | - |
| T38 | Entry effect (Q8) | "A transfer took effect if it is not voided and it moved the `<item>` under these rules. A voided transfer never took effect." Cards with a Q8 "fail to take effect" row add: "'Did the transfer in entry `<N>` (S4: change `<N>`.`<k>`) fail to take effect?' asks the opposite: yes exactly when it did not take effect." This is Q8's only implicit negation cue (R3-09); its declarative "the transfer in entry `<N>` failed to take effect" inside a 2.2 D stem is the same form. | voided = took effect, then undone |
| T39 | Counts (A26, R1-05) | "Every `<item>` in this log is a `<kind>`. 'How many `<items>` `<X>` holds' counts every distinct `<item>` `<X>` holds, including any whose `<quantity>` is 0, not their `<quantities>`." (R2-02) | sum of quantities; `<items>` with `<quantity>` 0 not counted (R2-02) |
| T40 | Transfer check and lock rule both on (A01) | "A transfer takes effect if and only if, at that moment, the named sender holds the `<item>` and the `<item>`'s status is not '`<S>`'. Otherwise it changes nothing. Decide this after removing voided entries and applying corrections." | either condition ignored |
| T41 | Notices (S4; A12, A13, A14, R1-06, R1-21) | "Each notice has a reference number and a date. Reference numbers start at 1 `<leading extract: at N0>` and increase with date `<closed: and run with no gaps>`. A notice may hold several numbered changes (`<N>`.1, `<N>`.2, ..., with no gaps); they take effect on the notice's date, in that order. Notices with the same date take effect in reference-number order. 'Withdraw notice `<N>`' is one change; it cancels every change in notice `<N>`. 'Amend `<N>`.`<k>`' changes only that change. A notice never states a date of effect of its own." Open S4 cards add the S4 version of T3: only whole notices are missing. | changes in a notice applied in any order; "withdraw" read as cancelling only one change; a numbering gap read as a missing notice |
| T42 | Ledger tables (S3; A35, A36, B17) | "Change rows use one entry-number sequence across all change tables. 'From' and 'to' name a transfer's sender and receiver. A blank cell means no change; in a creation row it means the starting value '`<default>`'. Rows are listed by `<key>`; they take effect in entry-number order." JSON and YAML arrays add T8's sentence that a left-out field is a blank (rule 20; R3-06). | numbering restarts in each table; listing order |
| T43 | Git-like log (S5, dev only; A38) | "Each line has a date and a sequence number. Sequence numbers increase with date and time, so lines take effect in sequence order, which is also date order, whatever the listing order (lines are listed `<newest first \| oldest first>`). In questions, 'dated' in T24 and T25 means a line's date. A '`<revert verb>`' line cancels the line it names as if that line had never been made; it does not act from its own date. A '`<fixup verb>`' line is a correction (T11). '`<move verb>`' renames an `<item/holder>` (T14); '`<merge verb>`' merges holder `<A>` into holder `<B>` (T15); '`<replace verb>`' is a supersede (T13). Entry hashes are always written in full." The date-order sentences are R3-05. | git's meaning: a revert acts from its own date |
| T44 | Answer convention (yes/no rows with a negation cue; R4-01) | "Each yes/no question asks whether one statement is true. Answer 'yes' exactly when that statement, read with every 'not' and every negative word in it (such as 'no longer', 'lack' or 'fail'), is true; otherwise answer 'no'. In 'Is it true that ...?' the statement is everything after 'that'. 'Is it false that ...?' asks whether the statement after 'that' is false. 'It is not the case that ...' is true exactly when the statement after 'that' is false." Stated on every card that has a yes/no row in a negated stem form of 2.2 (N1-N5 or D), short cards included (2.1); no-card rows carry no negation cue. The 2.2 forms keep every L_core token out of the matrix clause, so no F3 stem is a negative polar question ("Doesn't ...?", "Is it not the case that ...?", "Does `<X>` not ...?"). | agreement reading: a negated stem answered by agreeing with the negated fact, or read as asking to confirm the positive claim (not run: every 2.1 row with a negation cue states T44; 2.1) |

### 2.1 Card-free and short-card rows (about 15% of rows; A34, C05)

- **Which rows.** Rows with no card, and rows on short cards. A short card states the task in one line and leaves out at
  least one rule its structure triggers. Rows on cards that state every triggered rule (one-line rule list or any
  other style) are not 2.1 rows.
- **Blanks (XF06; R3-C1).** A short card never leaves out the meaning of a blank its row shows: it always states T8's
  blank sentence (with its left-out-field sentence in JSON, YAML or key-value containers), T9's creation sentence when
  a creation leaves a field blank, and, in S3 containers, T42's blank-cell sentence. The rule it leaves out is another
  triggered rule. No-card rows show no blank at all: they use only containers whose entries name just what they change
  (prose, bullets or log lines in S1, S2 or S4 shapes; never a table, CSV, JSON, YAML or key-value record, so no S3
  container), and every creation on them states each starting value.
- **Negation (T44; R4-01).** A short card with a yes/no row in a 2.2 negated stem form always states T44 (and T13's or
  T38's sentence on its "lack" or "fail" rows); the rule it leaves out is another triggered rule. No-card rows carry no
  negation cue: no neg or dneg twin is made on a no-card row (skipped and logged).
- **Restrictions.** Closed world; S1-S4 only (no S6); no transfer check, lock rule or gaps; no abstain option (no NEI,
  no None, so no Q7); no masked or swapped status words; no notes or injected text; no dates outside the entries; ISO
  or month-name dates only.
- **Check.** Every Alt in section 2 whose trigger the row's structure touches, and which the restrictions above do not
  ban, is run as a program variant of solver A. The row is kept only if the label is the same under every single
  variant and under every pair of variants. A variant that gives no single answer (for example T24 Alt (b) on a
  choice row, or T17's quantity-0 Alt on Q5) counts as a different label. The Alts include the R2-02 readings: "on
  `<D>`" and "as of `<D>`" each as the start of `<D>` and as any time during `<D>` (T24; both phrases, R3-04),
  "between" excluding an end date (T25), and an `<item>` with `<quantity>` 0 as not held (T17, T39); and the R3
  readings: corrections counted per entry rather than per value (T11 Alt (e); R3-01), and a new ID naming only the
  history after its rename, or under alias an old ID only the history before it (T14 Alts (b) and (c); R3-02). On a
  negated row every Alt is applied to the claim inside the negation, and an Alt that reads a date phrase as several
  points (T24 Alt (b)) is run twice, with the negation outside and inside "at any of those points"; each run is a
  variant (R4-01). The keep and drop counts per variant are logged.
- **Not varied.** T1-T3: the row shows no abstain option and the structure is closed, so the closed reading is the only
  one its options allow (A34a). T34 and T36: the restrictions ban their triggers. T44: every 2.1 row with a negation
  cue states it, and no-card rows carry none (negation bullet above).

### 2.2 Closed phrase lists (G3 grammar; A07, A28, A31, A32, C06)

- **Scope (R1-15).** The date-phrase, end-word, "or" and banned-word lists below apply to question stems and to the
  negation and twin frames around them. Card rule text and log or notice text are governed by the surface-grammar
  registry (G3) instead, so T6 and T7 may say "after `<D0>`" and "on or before `<D>`", and S6 entries may carry
  "effective" dates. The "inside notices" list applies to notice text.
- **Date phrases.** Allowed: "on `<D>`", "as of `<D>`", "at the end of `<D>`", "at the start of `<D>`" (T24), and
  "at any time between `<D1>` and `<D2>`" (T25). "Between" appears in a stem only inside "at any time between": the
  parser rejects a bare "between `<D1>` and `<D2>`" in a stem (R3-10), and every other date phrase, including "by",
  "until", "since", "after", "during", "prior to" and a bare "before `<D>`". (T25's card sentence may still say
  "between `<D1>` and `<D2>`"; card text is outside this list, as the scope bullet says.)
- **End words** (question text only): "now", "currently" and "at the end" (T4) in any end-of-log question. "Still"
  and "no longer" appear only in Q4 end-of-log holding stems, with T31's meaning and guard (R3-08). The parser rejects
  them in Q1, Q2, Q3, Q5, Q6, Q7 and Q8 stems, in Q4 "on `<D>`" stems and in "or" stems.
- **Implicit cues (R3-09).** Each implicit negation cue has one stem form and one T rule: "lack `<R>` as its current
  record" (Q3 only; T13; the stem always names one record, and the document-only "lack a current record" is
  rejected) and "fail to take effect" (Q8 only; T38). Each also appears as the declarative inside a D stem (negated
  stem forms below). The parser rejects "lack", "fail" and every other implicit cue in any other form or QT. The T22
  comparator phrases "no fewer than" and "no more than" are not negation cues: negcount counts them in k_all (XF02),
  but they keep the claim's meaning ("no fewer than `<N>`" = "at least `<N>`"), so they never make a neg or dneg twin
  and never serve as the inner cue of a dneg (R4-04 below).
- **Inside notices:** "today" is the only relative time word. "Now", "currently", "at present", "still", "yesterday",
  "tomorrow" and "this week" are banned there.
- **"Or":** only as T23 allows. "Either ... or" is banned.
- **Yes/no stems (R1-16):** never contain, as a whole word in any case, "answer", "answers", "answered", "option",
  "options", "choice", "choices", "correct", "correctly", "incorrect" or "incorrectly". The match is whole-word, so
  "correction", "corrected", "corrects" and "optional" are allowed. A pack lint keeps these eleven words out of status
  values, item kinds, holder and document names, roles and IDs, so no stem can contain them through a pack value.

**Negated stem forms (G3 stem grammar; XF10's truth-frame form; F3-local rules R4-01 to R4-04, R2-01, R3-C2).** Let C
be a yes/no row's affirmative claim, written as a declarative clause with no negation cue (negcount k_all = 0, apart
from a T22 comparator phrase on an affirmative row): for example "`<X>` holds `<Y>` at the end", "`<X>` held `<Y>` on
`<D>`", "the `<status>` of `<Y>` is `<S>` at the end", "`<R>` is the current record of `<document>`", "the transfer in
entry `<N>` took effect", "`<X>` holds at least `<N>` `<items>` at the end". The **matrix clause** is the stem outside
the declarative that follows "Is it true that" or "Is it false that" (the whole stem when it has no such frame). A
matrix clause never holds an L_core token (negcount: not, n't, no, none, nobody, nothing, nowhere, never, neither,
nor), apart from the "no" of a T22 comparator phrase on an affirmative row (negcount R3: k_syn 0): L_core negation
stands only inside the declarative after "Is it true that". So the G3 stem grammar rejects
fronted negated auxiliaries ("Doesn't ...?", "Isn't ...?", "Didn't ...?", "Wasn't ...?", "Is it not the case that
...?", "Did ... not ...?") and a main-clause "not" or "no longer" ("Does `<X>` not hold `<Y>`?", "Does `<X>` no longer
hold `<Y>`?"). Every yes/no stem has exactly one of these forms, and every card with a row in a form N1-N5 or D states
T44:

| Form | Stem | Allowed on | k_syn / k_all | Relation |
|---|---|---|---|---|
| A | the QT's question ("Does `<X>` hold `<Y>` at the end?", "Does `<X>` still hold `<Y>`?", "Is `<R>` the current record of `<document>`?", "Did the transfer in entry `<N>` take effect?", ...) or "Is it true that C?" | every yes/no QT | 0 / 0 (0 / 1 with a T22 comparator phrase) | base row |
| N1 | "Is it true that C-not?": C with "not" or "n't" on its main verb ("`<X>` does not hold `<Y>` at the end", "the `<status>` of `<Y>` was not `<S>` on `<D>`", "`<R>` is not the current record of `<document>`", "the transfer in entry `<N>` did not take effect") | Q1 and Q2 status claims at one point, Q3, Q4 except "still" stems, Q8; never "or", range or threshold stems | 1 / 1 | complement |
| N2 | "Is it true that `<X>` no longer holds `<Y>`?" | Q4 end-of-log only, under the T31 guard: the complement of "Does `<X>` hold `<Y>` at the end?" and of "Does `<X>` still hold `<Y>`?" | 1 / 1 | complement |
| N3 | "Does `<document>` lack `<R>` as its current record?" (T13); "Did the transfer in entry `<N>` (S4: change `<N>`.`<k>`) fail to take effect?" (T38) | Q3; Q8 | 0 / 1 | complement |
| N4 | "Is it true that it is not the case that C?" | every yes/no QT except "or" stems, range stems and "still" stems | 1 / 1 | complement |
| N5 | "Is it false that C?", C with k_all = 0 | every yes/no QT | 0 / 1 | complement |
| D | "Is it true that it is not the case that C'?", C' the declarative of an N1, N2 or N3 stem ("... that `<X>` does not hold `<Y>` at the end?", "... that `<X>` no longer holds `<Y>`?", "... that `<document>` lacks `<R>` as its current record?", "... that the transfer in entry `<N>` failed to take effect?") | the QTs and stem kinds of N1, N2 and N3 | 2 / 2 over N1 or N2; 1 / 2 over N3 | equiv (same label as A) |

- **"Still" (R4-02).** "Still" never shares a stem with "not" or "n't" (no N1, no N4, no "still not"). A "still" stem
  is negated only by N2 or by N5 ("Is it false that `<X>` still holds `<Y>`?"), and its D twin is D over N2. The T31
  guard binds every row whose stem has "still" or "no longer" (A, N2, N5 and D alike).
- **Threshold stems (R4-03).** A stem whose claim compares a `<quantity>` or a count with `<N>` (Q1 and Q2 quantity
  thresholds, Q6, range conditions) is negated only by a sentence-level operator, N4 or N5 (ranges: N5 only, below).
  "Not" or "n't" never stands on the verb of a threshold claim or next to its comparator or numeral, so no numeral
  scope reading arises ("`<X>` does not hold at least `<N>` `<items>`" is never made). Threshold stems get no D twin
  (skipped and logged).
- **Comparator phrases (R4-04).** "No fewer than" and "no more than" never share a stem with a negation cue. A row
  whose claim uses either phrase gets no neg and no dneg twin (skipped and logged); a negated threshold row uses only
  "at least", "at most", "more than" or "fewer than". The G3 stem grammar rejects either phrase in any stem of forms
  N1-N5 or D.
- **"Or" and range stems (R2-01).** A stem with "or", and a range stem ("at any time between"), is negated only by N5,
  which scopes over the whole claim, and gets no D twin (skipped and logged). "Or" stems also carry no "still" or "no
  longer" (range stems carry neither, as they are not Q4 end stems). The parser rejects "not", "n't", "never", "no
  longer", "it is not the case that" and every implicit cue in these stems, and rejects "at no time between". A range
  condition may keep "no fewer than" or "no more than" only on its affirmative row (R4-04).
- **Frames (XF10; R3-C2).** No stem wraps a claim in a judgement or acceptance predicate ("wrong", "right", "reject",
  "accept", "should/would ... be"). "Is it false that" wraps only an affirmative claim (k_all = 0 inside it, so no
  comparator phrase either) and is never embedded or negated. "It is not the case that" stands only directly after
  "Is it true that", once (N4, D). The G3 stem grammar rejects "Is it false that" over any claim with k_all >= 1, and
  any stem that has none of the forms above.
- **Only these cues.** A stem's only negation cues are those of its form: "not" / "n't" (N1, D), "no longer" (N2, D),
  "lack" and "fail to take effect" (N3, D), "it is not the case that" (N4, D) and "Is it false that" (N5). The parser
  rejects every other negcount lexicon entry in a stem ("never", "none", "nobody", "without", "unless", "other than",
  and the rest), apart from a T22 comparator phrase on an affirmative row. Double-negation rows with k_syn 2 are the
  D rows over N1 or N2 (section 5 negation quota).

---

## 3. Solvers and label checks

**Solver A: forward replay (G2 reference).**
1. Drop voided entries (T10, T12).
2. For each entry and each of its correctable values, apply the corrections to that value that are not voided: the
   highest-numbered one counts; if none is left, keep the original value. Corrections to different values of one entry
   (a CREATE's starting status and starting quantity) each apply (T11; R3-01).
3. Sort by the effect key:
   - S1-S3: (date, time, entry number);
   - S4: (date, reference number, change number);
   - S6: (effective date, entry number);
   - S5: sequence number (the same order as (date, time, sequence number), by rule 1; R3-05).
4. Replay from the opening register. On leading-extract cards, every value starts UNKNOWN, and a CREATE's blank fields
   start as `<default>` (T3's T9 sentence; R1-04).
   - Keep an alias map, the holder map, statuses, quantities and document chains. The alias map built during replay maps
     an entry's IDs to entities and decides whether the entry is valid at its own point (T14 retire, T15); it is never
     used to read a question's IDs. Each ID in the question is mapped to
     its entity through the whole-log rename map (every rename in the log, before or after the query point), so an
     entity's IDs name its whole history (T14; R3-02).
   - At each entry (already corrected in step 2): an entry that names a retired or absorbed ID has no effect. This is
     checked on the corrected entry at its own point; VOID and CORRECTION entries are never checked themselves
     (rule 10; R1-02). Transfer conditions (T18, T19, T40) are read on the current state. A merge passes every item.
     A supersede creates its record.
   - In an open world, a gap sets every value and pointer to UNKNOWN. A later exact setter (CREATE, SET, TRANSFER)
     makes that value known again. An ADJUST applied to UNKNOWN stays UNKNOWN. A value at any point is known if and
     only if T2 (a), (b) or (c) fixes it: its last exact setter at or before that point comes after every gap in the
     log (a missing entry may void or correct an earlier shown entry); or it is the holder just before a shown,
     non-voided transfer that comes after every gap (next bullet) (R2-08); or it is a register value read at the
     opening point, before entry 1, on an explicit-marker or skipped-number card (R3-03). Replay on those cards starts
     from the register with every register value known at the opening point.
   - With the transfer check off, at a shown, non-voided transfer that comes after every gap, the sender is recorded
     as the holder just before it (rule 6, stated by T17; R1-09). This feeds "at some point" checks.
5. Take snapshots at the query points (end of `<D>`, start of `<D1>`, and right after each non-voided entry dated
   `<D1>` to `<D2>` for a range; T25, R1-03), then answer. The T31 guard reads the opening state and every end-of-date
   snapshot.
6. UNKNOWN gives NEI on a choice row. A yes/no row whose answer is UNKNOWN is not made.

**Solver B: backward version-graph resolver (different paradigm, separate module, no shared code).** It runs on the G3
parse.
- Build a pointer graph: void edges, correction edges (one per corrected value), rename edges, timed merge edges,
  supersede edges and gap nodes.
- Map each ID in the query to its entity through the **whole-log** rename closure: every ID that a rename links to it,
  before or after that rename (renames are never voided or corrected). An entity's IDs name its whole history (T14;
  R3-02). Rename and merge times are used only to decide whether a candidate entry is valid at its own point (an old ID
  after a retire-mode rename; an absorbed ID after a merge) and which `<items>` a merge passes, never to narrow the
  query's closure.
- Resolve lazily from the query backwards in effect order, over that entity's whole-log closure:
  - skip each voided candidate writer;
  - for each value of the candidate, apply the highest-numbered non-voided correction to that value (T11; R3-01);
  - under the transfer check or lock rule, call `holder(item, t-)` or `status(item, t-)` recursively (memoized,
    top-down);
  - an entry naming a retired or absorbed ID is skipped. This is checked on the corrected candidate at its own point
    in effect order, never on the VOID or CORRECTION that acts on it (rule 10; R1-02);
  - crossing a gap before the last exact setter is found returns UNKNOWN.
- Q3: walk the effective (non-voided) supersede edges from the document root to its single sink at the end of the log,
  and assert it is a chain.
- Q6 and Q7: resolve each item of the card's one kind separately, then count or filter. Also assert Q7's rule 11.
- Q2 ranges: resolve at the start of D1 and right after each non-voided writer entry of that field dated D1 to D2 (a
  corrected writer counts at its own point), so states between same-date entries are included (T25; R1-03).
- Q8: resolve the transfer's own conditions at `t-` of that entry.
- T31 rows: check the guard (opening state or an end-of-date snapshot) and the end value.

**Solver C: possible worlds (open-world rows only).** Its alphabet matches what the open card allows (T2; A18). It keeps
only the worlds that satisfy every rule the card states (R1-09): the numbering and date order of T3 and T5 (a missing
entry's date lies between its neighbours' dates; each skipped number is exactly one entry, on S4 one notice), rule 6
as stated by T17, rule 7 as stated by T28, T36 (a status is always one of the card's listed values; R2-10), and the
T10 and T11 targets (a missing VOID or CORRECTION names an earlier entry). Each gap is filled with nothing or with one
entry from this alphabet. On skipped-number cards, "nothing" is modelled by an inert entry (a creation of a fresh
item), which pads the gap to its exact count:
- CREATE of a fresh item;
- SET of a status to each listed value (never a fresh status; T36), and of a quantity to each value on the card plus
  one fresh value;
- ADJUST of each quantity by +1 or -1;
- TRANSFER of each item to each holder, plus one fresh holder;
- VOID of each eligible earlier entry;
- CORRECTION of each eligible earlier entry, in each slot T11 allows: a status slot to each listed value only; a
  quantity or receiver slot to each value on the card plus one fresh value;
- SUPERSEDE to a fresh record.

There is no RENAME or MERGE, as the card says. A leading extract is modelled as an opening state in which a holder or
quantity ranges over the card's values plus one fresh value, and a status over its listed values only (T36). If every
world gives the same answer (and, for T31, the presupposition and the T31 guard hold in every world), the row is
"decided". If two worlds differ, the gold is NEI.

**S4 open cards (R2-10).** A gap is a missing notice (a skipped reference number is exactly one notice; an explicit
marker is one or more). A missing notice is dated between its neighbours and holds 1-4 numbered changes from the
alphabet above, except that "withdraw notice `<M>`" replaces VOID (`<M>` is an earlier notice that holds only
voidable changes and withdraws nothing; there is no single-change void on S4), and "amend `<M>`.`<k>`" is the
CORRECTION. Solver C enumerates missing notices of one change each; "nothing" on a skipped reference number is a
notice holding one inert change (a creation of a fresh item). The world filter adds T41's notice order and
numbering.

A Hypothesis property test runs on small structures (<= 8 entries, <= 2 gaps, <= 3 records). It checks that two-entry
fillings never change the verdict from one-entry fillings. Its cases include Q1 on a quantity with an ADJUST after the
last gap (A17), Q4 "no longer", (R1-09) a gap followed by a shown transfer whose sender is inferred as the holder
just before it, and (R2-10) S4 structures whose missing notices hold 2-4 changes, including a withdrawal, which must
never change the verdict from one-change notices, and (R3-03) explicit-marker and skipped-number cards whose T31 guard
rests only on the opening register. It also asserts the one-way property the pipeline relies on:
whenever solver A gives a known answer, solver C gives the same answer in every kept world; whenever solver A gives
UNKNOWN on a choice row, solver C finds two kept worlds that differ. (A yes/no row with UNKNOWN is never made, so solver C may be decided there; this is logged,
not a failure.) If the lemma fails, open-world cards are narrowed and this spec goes back to G0 review.

**G2.** A = B on 100% of rows. On open-world rows, A = B = C on 100%. Any mismatch: stop, fix the generator, and
regenerate the whole generator. A label is never edited by hand.

**G3 round-trip parse.** The parser `parse_f3` is written from this spec plus two registries that the format agent
fills after G14:
- a **statement-id registry**: each paraphrase maps to a T id;
- a **surface grammar registry**: each event phrasing maps to an entry type and its slot order (IDs, dates, values,
  entry references). It enforces the phrase lists and the negated stem forms of 2.2.

The parser never imports renderer code; an import lint enforces this. Container readers: markdown, CSV, HTML,
fixed-width tables, JSON, YAML, log lines, and prose, email or memo by sentence-level grammar match. It enforces the
shared XF06 marker table and rule 20: a left-out key in a JSON, YAML or key-value entry is read as a blank, and a
`null`, `~`, empty string, empty "key:" value or XF06 unknown marker in an F3 row is a parse failure (R3-06). The parser outputs
the canonical structure: register, entries, gaps, stated toggles, query, options, negation count and polarity.

The parser reads the card text where the section 1 row layout puts it: the `card` field on yes/no rows; on choice rows
the option-definition lines in `card` and the card blocks moved into `instructions` (A16.1 (g); R4-05). It marks each
illustration and worked-example block in that card text and parses it into its own mini-structure (R1-17). Those
blocks are never part of the row's structure.

Checks, all at 100%:
1. The parsed `structure_hash` equals the generator's. The hash is spec 7.2's canonical problem (R1-18): the facts
   (opening register, entries, gaps), the rule graph (the stated toggles) and the query. The query is (question type;
   decision form, choice or yes/no; entity references; asked values, that is the status value of a Q1 or Q2 yes/no
   row and each value or holder joined by "or"; threshold comparator and `<N>`; date points; negation count and
   polarity; for Q7, the listed candidate items) (R2-03). Entity names are assigned in a canonical traversal in effect
   order. It is therefore unchanged by listing order, container and consistent renaming (B05). It does not cover the
   answer options of Q1-Q5 (fillers, bucket, whether `<NEI option>` is shown), notes, illustrations or worked
   examples. The program also computes a coarser **`leak_key`** for the 7.2 method-6 leak checks: the same facts and
   stated toggles, with the query cut to question type, entity references and date points (decision form, asked
   values, comparator, `<N>`, negation and Q7 candidates dropped). It matches whenever the hash matches, so the leak
   check is never narrower than the canonical problem.
2. Solver B (and C) on the parse gives solver A's label.
3. Every ID string in the row's log, query and options exists in the row's structure. Look-alike distractor IDs are
   part of the structure. Every ID in an illustration or worked-example block exists in that block's own
   mini-structure, and none appears in the row's structure (R1-17).
4. The parsed toggles equal the card's toggles. Only toggles whose trigger occurs on the card are compared (B06). On 2.1
   rows they are "unstated", and the 2.1 check passed.
5. The parsed negation count and polarity equal the generator's, and the stem has the 2.2 negated stem form (A,
   N1-N5 or D) the generator chose, allowed for its QT and stem kind; a card with an N1-N5 or D row states T44.
6. The parsed option set (entity references and any abstain option) equals the generator's (R1-18).
7. Solver A on each parsed illustration or worked-example mini-structure gives the outcome the block states.
8. fmt1 `card.loader_check` passes with `card.must_show` (section 1 row layout; A16.1 (g), R4-05): the decoder_io
   prompt (cygnet, `schema_branch_mark`, random option order) shows every card line, rule sentence, definition and
   example; on choice rows `card` holds only "- `<option>`: `<definition>`" lines of shown options; the gold letter maps
   back to the gold option; `train_decoder.check_rows` accepts the row. It runs on every row before checks 1-7, and
   the G3 report logs its pass count.

A parse failure is a bug, never a silent drop.

**G4 metamorphic relations.** Each generator must pass 100% on >= 1,000 rows, using Hypothesis. Every variant first
re-passes the section 1 generator rules. A variant that breaks one is skipped and logged (a count per relation in the
G4 report), never forced (A41).

| # | Relation | Expected |
|---|---|---|
| M1 | Insert an inert entry outside the query's dependency closure (taken from B): an entry on another item, or a SET to the value the field has at the insertion point (A40). On open cards, only entries on other items, or entries before the last gap. Renumber so that rule 1 holds | label unchanged |
| M2 | On sorted or shuffled listings (S3, S6), shuffle the listing order with numbers and dates unchanged. On any card, commute two adjacent entries with the same date (and time) that share no ID and are not RENAME, MERGE, VOID or CORRECTION; renumber both and update references | unchanged |
| M3 | Consistent renaming to fresh IDs that do not look alike, everywhere (text, options, question) | unchanged (mapped) |
| M4 | Option shuffle plus container change (table, JSON, log lines) | gold maps |
| M5 | Void the decisive writer. Voidable types only: SET, ADJUST, TRANSFER, CORRECTION, SUPERSEDE (A41) | the label solver B predicts by resolving without that entry (the previous effective writer, the opening value, or a recomputed transfer-check cascade). Solver A must agree |
| M6 | Open world: add a gap before the effective writer (the last exact setter) / add a gap between the writer and the end (never as the last entry) (A39). On leading-extract cards, the first form moves `<N0>` later (still before the writer) and the second form is not applied, since those cards have no inner gaps (R1-06) | unchanged / NEI on choice rows with k >= 3 (k = 2 rows and the yes/no row are dropped; XF01) |
| M7 | No non-voided entry dated D1 to D2 writes the field; a correction counts at its target's point, not its own date (R1-03) | the value at the start of D1 equals the value on D2, and a range question over D1 to D2 has the same label as the same condition asked "at the start of D1" |
| M8 | Inert note or attack text inside a marked note field (S4: note or postscript) | unchanged (`inv`) |
| M9 | Negate the question / double-negate it, only in a negated stem form of 2.2 that the stem's QT and kind allow (N1-N5 / D; R3-08, R3-09, R4-01 to R4-04), on a card that states T44: no L_core token in the matrix clause; "no longer" (N2) only on Q4 end stems and every "still" or "no longer" row under the T31 guard; "still" never with "not" or "n't"; "lack" and "fail to take effect" (N3) only on Q3 and Q8; threshold stems only N4 or N5, with no D; "or" and range stems only N5, with no D; "Is it false that" only over an affirmative claim (k_all = 0); a claim with "no fewer than" or "no more than" gets neither. A form that is not allowed is skipped and logged | NOT label / same label |

---

## 4. Generator sheets (one page each)

The row counts below include twins. Round 2 is the both-round total, so every sampler stays under the 2,500 cap. S6 is
added for two reasons: S1-S4 alone would need 2,250 rows each, with no slack for G5 and G9 losses, and S6 adds a shape
(effective-date order) the others lack (spec 2.1 allows S6+). Every sheet shares sections 1-3 and 5-6. "States" lists the
T rules its card states when their trigger occurs.

### S1 Forward event sequences (r1 1,000 / r2 2,000)
- **Shape.** A chronological activity log as prose, bullets, log lines or key-value records. The opening register is a
  short list, absent on leading-extract cards. Listing order: chronological. Key-value records write a blank as a
  left-out key and are never used on no-card rows (rule 20, 2.1; R3-06, R3-C1).
- **Draw.**
  - 2-12 items, 3-20 holders, 1-3 fields per item (status always; quantity optional; drawn once per card, so every
    item on the card has the same fields; rule 20), 0-3 documents of 1-5 records.
  - Event count by bin: 5-12 30%, 13-24 40%, 25-40 30%.
  - A Markov chain over entry types follows the mechanism mix.
  - One log carries many questions. Queries are enumerated afterwards and kept by stratified acceptance so the
    section 5 targets hold. All rows of one log share its `group_id` (B05).
- **Toggles.** World (open allowed), gap style, rename mode, transfer check, lock rule, times, date format, status
  vocabulary.
- **Questions.** All QTs on closed cards (Q7 only on inverted cards, which hold nothing else; rule 17); Q1, Q4 and Q5
  on open cards.
- **States.** T1 or T2 + T3 (leading extracts: T3 with T9's creation sentence only); T4, T5, T7-T17, T20-T39 as triggered; T18, T19 or T40 when on; T35 on decision-list cards.
- **Mechanisms.** Each mechanism in the section 5 inert list (VOID, CORRECTION, SUPERSEDE, RENAME, MERGE, transfer
  conditions; R2-11) is decisive on 50% +/- 10 of the rows where it appears, so its presence does not signal that it
  matters.
- **Distractors.** E1-E4 and E7-E12. E5 needs a non-chronological listing, and E6 is S6 only.
- **Depth.** Mostly 1-3.

### S2 Target-first (r1 1,150 / r2 2,300)
- **Shape.** Gold first. Choose the question type, gold value, depth d and decisive mechanism path. Build the chain and
  place the decisive entry at a uniform decile of the effect order. Rendered in S1 containers (chronological) or S3
  containers (chronological or sorted).
- **Near misses (>= 2 per row, each one named error).** At least one per row is E4, a distractor event on a look-alike
  ID (spec 2.2 F3; C12). The others come from:
  - E1: a voided entry with a tempting value;
  - E2: the original value of a corrected entry;
  - E3: a correction to an entry that a later SET overrides;
  - E7: an entry dated D-1, D or D+1 around an at-time query;
  - E8: an entry that uses an old ID under the wrong rename mode (entry-level only; old IDs are never options, A21);
  - E9: one hop short of the supersede chain, or a voided supersede.
- **Boundary (B15).** 30% of S2 at-time rows "sit on the boundary": the decisive entry or the tempting distractor is
  dated exactly D (for "at the start of D", dated D). D-1 and D+1 entries count as near-boundary distractors, not as
  boundary rows.
- **Placement (B10).** The tempting distractor comes after the decisive entry on 50% +/- 5 of rows.
- **Toggles.** As S1, plus a sorted listing in S3 containers (closed cards only).
- **Questions.** All QTs (Q7 only on inverted cards; rule 17); open cards as in S1.
- **States.** As S1, plus T42 in S3 containers.
- **Role.** S2 is the main source of deep training items. Wrong options come from E1-E12 (section 5).

### S3 Ledger tables (r1 1,000 / r2 2,000)
- **Shape.** An opening register table plus 1-2 change tables with one entry-number sequence (A36). Columns: entry no.,
  date (and time), item or record, action, field, value, from, to, refers-to, note (A35). A blank cell means no change;
  in a CREATE row it means the default (T42, B17). The holder field is never SET.
- **Listing order.** On >= 50% of rows, rows are sorted by a stated non-time key (for example item ID), so the reader
  must re-order by T5 and T42. Other rows are chronological, or shuffled with timestamps. Open cards are chronological
  only (A16).
- **Containers.** Markdown, CSV, HTML, fixed-width, JSON or YAML arrays. Tables write a blank as an empty cell; JSON
  and YAML arrays write it as a left-out key, never `null` or an empty string (rule 20; R3-06). Every S3 card states
  T42's blank sentence, so S3 rows under 2.1 are short-card rows only, never no-card rows (2.1; R3-C1).
- **Rosters.** 10-60 items or holders. S3 supplies most of the 10-19 and 20-60 option buckets. Every filler is named in
  some entry or in the opening register (rule 12; R2-09).
- **Length cap (R1-19).** On a log that carries 20-60-option rows, the draw has at most 24 entries and at most 70
  register rows plus entries, and options are IDs only. Every row is still measured with the real tokenizer on the
  served prompt, where a choice row's moved card text counts twice (section 1 row layout), and redrawn at >= 1,900
  tokens (section 6). The draw plan reserves enough 20-60-option rows that the 15% bucket holds after redraws.
- **Toggles.** World, gap style, rename mode, transfer check (the from and to columns carry the sender and receiver),
  lock rule, times, date format, listing order, status vocabulary.
- **Questions.** Q1, Q2, Q5 and Q6, or Q7 alone on inverted cards (rule 17) (open: Q1 and Q5).
- **States.** As S1, plus T42.
- **No "old value" column.** It would go stale after voids and corrections and create ambiguity.

### S4 Multi-notice correspondence (r1 850 / r2 1,700)
- **Shape.** 3-12 notices (letters, emails, memos) between named parties. Each has a reference number, a date and 1-4
  numbered changes (`<N>`.1, ... with no skips). A log has 5-40 changes in total, and the event-count bins count
  rendered numbered changes, not notices (A12, B03, R1-21). No times.
- **Changes.**
  - change records;
  - withdraw an earlier notice, or amend one earlier change (CORRECTION of `<N>`.`<k>`). **A withdrawal (R1-21)** is
    one numbered change `<M>`.`<k>`, rendered as one sentence. In the structure it expands to one VOID per change in
    the withdrawn notice. It counts as one change for the event-count bins and the 5-40 limit, and adds depth only as
    the depth section says;
  - renumber (RENAME) or consolidate (MERGE) holders;
  - replace documents (SUPERSEDE).
- **Own generator rules.**
  - A notice that is withdrawn holds only voidable changes.
  - A notice that withdraws something is never withdrawn.
  - A notice never states a date of effect of its own (A13).
  - Closed cards: reference numbers start at 1, are consecutive and increase with date (A14, R1-06). Open cards: gaps
    are whole notices, marked by skipped reference numbers (from 1) or an explicit marker between notices (from 1),
    or the card is a leading extract starting at reference `<N0>` > 1 with no later gap. Changes inside every shown
    notice run .1, .2, ... with no skips.
  - A withdrawal or amendment names only a shown notice or change (rule 3).
  - "Today" is the only relative time word inside notices (T32, 2.2).
  - Inert and attack text goes only in a marked note or postscript (A37).
- **Chains.** On >= 50% of rows the answer needs >= 2 reference hops.
- **Toggles.** World, gap style, rename mode, transfer check, lock rule, date format, status vocabulary.
- **Questions.** Q1, Q3, Q4 and Q5 (open: Q1, Q4 and Q5). Q8 ("Did change `<N>`.`<k>` take effect?", where `<N>`.`<k>`
  is a transfer) on closed cards with the transfer check, the lock rule or a withdrawal (R1-10).
- **States.** T41 (replaces T5), T32, T33, plus the shared rules as triggered.

### S6 Effective-date amendments (r1 500 / r2 1,000; closed world only)
- **Shape.** An opening snapshot at the end of D0, plus amendment entries. Each entry has a recorded date and an
  effective date. Both are after D0, and every effective date is on or before the last recorded date (T6, A10). Entry
  numbers follow the recorded date. VOID and CORRECTION lines carry a recorded date only and act retroactively. No
  times.
- **Banned.** RENAME and MERGE (A23), gaps, and 2.1 rows. The transfer check and lock rule are allowed, with "at that
  moment" read in effect order (T5, T6).
- **Listing order (R1-20).** Recorded order; sorted by effective date (the card states it); or shuffled with both
  dates shown (the card states it). S6 has no sort by a non-time key. In a listing sorted by effective date, VOID
  and CORRECTION lines, which have no effective date, are placed by their recorded date (rule 10 order key; R2-06),
  and the card's sort sentence says so.
- **Order trap.** On >= 50% of rows where it matters, the recorded order differs from the effective order. The
  recorded-order heuristic is right on 50% +/- 10 of those rows.
- **Questions.** Q1, Q2 and Q4 (on D and at the end).
- **Query dates (R1-20, rule 15).** "On", "as of" and "at the end of" `<D>` use `<D>` >= `<D0>` ("on `<D0>`" reads the
  opening snapshot). "At the start of `<D>`" and every range start `<D1>` use a date after `<D0>`.
- **States.** T6, T7 (S6 version), T24 and T25 (S6 versions), plus the shared rules as triggered. Boundary dates follow
  S2's rule (B15).

### S5 Held-out: git-like log syntax (mix-tuning dev only; never a training row)
- **Uses.** 400 items for the spec 10 family set, plus all 300 depth-sweep items (5 depth levels {1, 2, 3-4, 5-6, 7-8} x
  60). The sweep comes from S5 only (B14).
- **Shape.** The same semantics and question types, written as hash-identified lines, each with a sequence number. The
  card states T43, which gives the listing order, makes revert retroactive, and defines move, merge and replace (A38).
  Sequence numbers strictly increase with date and time (rule 1; R3-05), so date order and sequence order agree:
  same-date lines take effect in sequence order, "highest correction" uses the sequence number, and at-time and range
  questions read line dates (T24, T25).
- **IDs.** 12-character invented hex hashes, always written in full. Look-alike hashes share a 7-character prefix
  (B20).
- **Length (B20).** Event-count bins as in training. Median length within 15% of the training median. Results are also
  reported length-matched.
- **Isolation.** Held-out packs and the 50 held-out styles. No real repo text, no commit-dataset rows, no n8n-like terms
  and no commit-size rubric (that skill belongs to the commit block).

---

## 5. Twins, distractors, balance (G10) and shortcut checks

**Twins (XF03).** Rows in a **contrast set** are 20-25% of F3 rows. A contrast set is a base row plus label-flip twins
with their own `call_id`, built by a change to the input text or structure: fact flip (including a boundary move of
the decisive date across D) and premise removal. `neg` (`complement`) and `dneg` (`equiv`) units count **only** toward
the negation quotas, never toward the 20-25%; attack (`inv`, about 5%) and inert units (<= 5%) count only toward their
own quotas (B13). Fact-flip and premise-removal sets are raised so that they alone reach 20-25% of F3 rows.
- **Negation.** `neg` (`complement`) and `dneg` (`equiv`) share one `call_id` with the affirmative row; a unit holds
  <= 3 rows.
- **Fact flip.** Void the decisive entry (voidable types only), change its ID to a look-alike that exists in the
  structure, move its date across D (renumbering so rule 1 holds), or break the transfer check. The variant re-passes
  the generator rules and is kept only if solvers A and B both flip the label. It gets its own `call_id` and the same
  `group_id`.
- **Premise removal (A42).** Closed world: delete the writer, renumber with no skipped numbers, and delete the VOID and
  CORRECTION entries that point at it. The rules are re-checked, and the label is what the solvers compute (as in M5).
  The twin is made only if that label differs from the base label (a contrast set holds label-flip twins only,
  XF03); a removal that keeps the label is logged and dropped (R2-11). Open world: add a gap between the writer and
  the end; the gold becomes NEI (choice rows with k >= 3 only, where NEI is shown; XF01). It gets its own `call_id`.
- **Attack.** An injected instruction goes in a marked note field (S4: note or postscript), and the label stays the
  same. It forms an `inv` pair with a clean row that is not already in a 3-row unit. The wording never matches
  eval_opi or eval_jagged.
- **Negation cue families** (templates come later; abstract here). Every negated row uses one negated stem form of
  2.2, only in the QTs and stem kinds that form allows, on a card that states T44: syntactic "not" / "n't" inside "Is
  it true that ..." (N1); lexical "no longer" inside "Is it true that ..." (N2; Q4 end-of-log holding stems only, under
  the T31 guard); implicit "lack `<R>` as its current record" (N3; Q3 only, T13; always naming one record) and "fail to
  take effect" (N3; Q8 only, T38); the sentence-level "it is not the case that" after "Is it true that" (N4); and the
  outer frame "Is it false that" over an affirmative claim (N5; k_all = 0). A dneg is form D, "Is it true that it is
  not the case that ..." over the declarative of an N1, N2 or N3 stem, never "Is it false that" over a negated claim
  (2.2; XF10, R3-C2, R4-01). "Still" never takes "not" or "n't" (R4-02); threshold stems take only N4 or N5 and no D
  (R4-03); "or" stems and range stems take only N5 and no D (R2-01). The comparator phrases "no fewer than" and "no
  more than" count in k_all (negcount) but are not negation cues: they mean "at least" and "at most" (T22), and a row
  whose claim uses one gets no neg or dneg twin (R4-04). Dev wordings are blocked: "Should the statement that ... be
  rejected?" and the "only non-..." + "be rejected" frame.

**Wrong options.** Each one comes from one named error:
- E1 ignored void;
- E2 ignored correction;
- E3 correction treated as the latest entry;
- E4 look-alike ID;
- E5 listing order;
- E6 recorded date instead of effective date;
- E7 boundary day;
- E8 wrong rename mode or absorbed ID (never an old ID of the gold entity; A21);
- E9 supersede chain one hop short or one hop too far;
- E10 last mention;
- E11 opening value;
- E12 transfer check or lock ignored.

Large option lists are filled from the pack's roster. Every filler is named in an entry or in the opening register
(rule 12; B09, R2-09).

**Polarity per question type (B04).** "Yes = bad outcome" is computed on the claim as asked, negation included. The
packs carry the tags.

| QT | A "yes" is bad when |
|---|---|
| Q1, Q2 on status | the asked value has a bad polarity tag (masked or swapped values: from the card definition; A44) |
| Q1, Q2, Q6 thresholds | the pack tags a high `<quantity>` or a high count of `<items>` as bad, and the claim is "at least" or "more than" (reversed for "at most" or "fewer than") |
| Q4 | the pack tags holding the card's one `<item>` kind as bad for X's `<holder>` role (a hidden pack attribute, never used by a label; R1-05) |
| Q8 | a "yes" means the `<item>` moved to the receiver, so the Q4 tag for the receiver applies |
| Q3 | the pack tags being current as bad for this `<document>` type |
| "Or" stems (T23; R2-01) | made only when both disjuncts carry the same tag (two status values with the same polarity tag, or two holders whose roles carry the same holding tag for the card's `<item>` kind); that shared tag applies as in the rows above |

**Balance targets (G10). Scope (B03, C01):** "family" is checked over all F3 rows, inside the spec's family x wording x
bin x negation-count cells where the spec names them. "Per sampler" is checked within each sampler as well.

**Where the targets are checked (R1-13).** Every F3 target in this section and in section 1 (QT shares +/- 3 pp, the
d1-d4 mix, deep share, deciles, event-count bins, NEI per open card, per-card yes rates, mechanism shares, option
buckets, masked and swapped quota, inverted-card share, abstain bands) is checked on the **final selected set**, after
G9, never only on the generated pool. The procedure:
1. Generate the spec's about 1.5x, plus enough per-cell surplus that every F3 target cell has at least 1.5x its target.
2. G9 scores every candidate and sets bins.
3. Select inside spec 2.1's family x gold label x wording x difficulty-bin cells, as the spec says. Within each cell, a
   quota sampler picks rows so that the F3 targets hold. The selection unit is a whole relation unit with its twin set,
   so no twin or relation unit is split.
4. Check every target on the selected set. If one fails, swap whole units for surplus units from the same G9 cell. If
   no swap fixes it, generate more rows for that cell and rerun steps 2-4. A label is never changed and a row is never
   edited.

Per-card targets on the selected set: abstain gold follows the display-then-gold rule (XF01): on each k bucket and
per abstain option, gold = 1/k +/- 2 pp over the rows that show it (no fixed per-card NEI count).

**Per-card yes rate (R2-05).** A card's drawn rate applies to its **base** yes/no rows (rows with no `twin_of`: the affirmative row of a negation unit
and the base row of a contrast set or attack pair), and their realized rate is within +/- 5 pp of it. All of the
card's yes/no rows, twins included, are in 20-80%. A card with fewer than 10 base yes/no rows (including inverted
cards, which have none) is checked only against 20-80%, when it has any yes/no rows. The aggregate 50% +/- 2 in the
G10 cells counts all yes/no rows, twins included.

| Target | Value | Scope |
|---|---|---|
| Yes rate | per card drawn uniformly from 20-80% and held on base rows (R2-05, above); aggregate 50% +/- 2 over all yes/no rows within family x wording x difficulty bin x negation count | family cells (spec G10) and per sampler |
| Yes/no share | 45-55% of F3 rows | family |
| "Yes = bad outcome" | 50% +/- 5 of yes/no rows (polarity per QT, above) | per sampler |
| Negation (C02, XF02) | counted by the shared `c_src/common/negcount.py`: k_syn >= 1 in >= 10% of yes/no rows; k_all >= 1 in >= 15%; k_syn >= 2 with an affirmative twin in >= 3% (D rows over N1 or N2, 2.2). The G10 negation-count cells use k_all | per sampler |
| Gold letter | uniform per option bucket (chi-square p > 0.01); "longest option is gold" within +/- 2 pp of 1/k | per sampler |
| Option buckets | 2-4 35%, 5-9 35%, 10-19 15%, 20-60 15% (+/- 3) | family |
| Abstain (XF01) | shown only at k >= 3 and only where it can be gold (NEI: open-card choice rows; None: Q7 rows); gold = 1/k +/- 2 pp per k bucket and per abstain option; so each is wrong on >= 2/3 of rows showing it. Family NEI and None shares are reported, not tuned | family |
| World | open-world cards 30% +/- 5 | family |
| Decisive position | uniform over 10 deciles of the effect order (chi-square p > 0.01) | family |
| Event-count bins | 5-12 30%, 13-24 40%, 25-40 30% (+/- 5); S4 counts changes | family |
| Depth | non-deep rows: d1 15, d2 30, d3 30, d4 25 (+/- 5); `meta.deep` rows <= 10% and outside the d1-d4 mix (R1-14) | family |
| Mechanism on the decisive path | VOID, CORRECTION, SUPERSEDE, RENAME, MERGE and plain SET/TRANSFER each >= 8% of rows; yes rate per mechanism 50 +/- 5 | family |
| Mechanism present but inert (R2-11) | for each of VOID, CORRECTION, SUPERSEDE, RENAME, MERGE and the transfer conditions (transfer check and lock rule, counted as one), decisive on 50% +/- 10 of the rows where it appears. An entry mechanism appears when the row's log has an entry of that type, and is decisive when it is a hop on solver B's decisive path (depth section). The transfer conditions appear when the card states T18, T19 or T40 and the decisive path contains a transfer, and are decisive when a stated condition blocks a transfer on that path. Plain SET, TRANSFER and ADJUST are ordinary writers with no inert target | per sampler |
| Masked / swapped vocabulary | status-option rows on masked cards 10-15% of F3 choice rows; on swapped cards 5% +/- 1 (B07, K1) | family |
| Inverted cards | 10-15% of F3 cards, all rows Q7; Q7 rows 10% +/- 3 of F3 rows (R1-12) | family |
| Attack present | uncorrelated with the label | family |
| Difficulty (G9 crowd) | easy <= 25%, medium >= 45%, hard <= 30%, selected inside family x label x wording x bin cells | family |

**Shortcut checks.** These are F3 heuristic baselines. A program computes them on the G6 QC sample (>= 5,000 rows) and
stores them in the QC sidecar, never in row meta. Each heuristic gives a yes/no answer per question type as follows
(B19).

| Heuristic | Choice rows | Yes/no rows |
|---|---|---|
| h1 last mention (spec: recency) | the option named in the last-listed entry about the queried `<item>`, field or `<document>` | Q1, Q2: yes iff that entry's value meets the claim (Q2 on D: last-listed among entries dated at or before D; Q2 range: last-listed among entries dated at or before D2; R1-03); Q3: yes iff R is the last-listed record of the document; Q4: yes iff the last-listed entry about Y names X as receiver or holder; Q6: count using the last-listed entry per item; Q8: yes iff no later-listed entry names entry N |
| h5 most similar ID (spec: ID similarity) | the option most similar to the queried ID | solver A with look-alike IDs (edit distance <= 2) merged into the queried ID |
| h2 ignore voids, h3 ignore corrections, h4 listing order, h6 recorded order (S6) | solver A with that mechanism ignored | the same |
| h7 opening value | the opening value or holder | Q1, Q2, Q4, Q6: the claim read on the opening state; Q3: yes iff R is the root; Q8: not applicable (a constant "yes", covered by the yes-rate check) |
| h8 most frequent value | the value or holder written most often | as h7, with the most frequent value |
| h9 mentioned options (report only) | uniform over options named in an entry about the queried `<item>` | - |

| Heuristic | Pass rule |
|---|---|
| h1, h5 (two-sided; B10) | yes/no 50 +/- 3; choice within 1/k +/- 3 pp |
| h2, h3, h4, h6 | wrong on 50% +/- 10 of the rows where that mechanism appears |
| h7, h8 | choice <= 1/k + 5 pp; yes/no 50 +/- 5 |
| h9 | report the effective k per option bucket (no pass rule) |

G6 (a)-(d) and G7 apply as in the spec. The G6 (d) metadata (read from the QC sidecar) includes sampler, stated toggles,
event count, mechanism counts, decisive decile and ID-pool features. G8 applies with a < 10% predictable share. No
feature such as the count of "void" or "correction" tokens may pass the G7 z-test.

---

## 6. Provenance, isolation, interfaces

- **Row format.** Spec 2.4, unchanged, with:
  - `family` "F3", `spec_id` "F3.G0.v7";
  - `sampler` in {S1, S2, S3, S4, S6}, or S5 for dev only;
  - `licence` "CC0 1.0 (program-generated)", `text_source` null, `persona_seed` from the pack;
  - `twin_kind` in {neg, dneg, fact_flip, premise_removal, attack}.
- **No extra meta keys (C15).** Rows carry only the spec 2.4 keys, so `train_decoder.check_rows` (G15) needs no change.
  F3's own fields go to a QC sidecar, `data/c_parts/qc/F3_sidecar.jsonl`, keyed by row `id`: {world, stated toggles,
  n_events, decisive_decile, mechanisms, qt, polarity, polarity_source, inverted_card, status_option_row,
  neg_form (the 2.2 form: A, N1-N5 or D), real_tokens, leak_key}. G6 (d), G10 and the shortcut checks read it. There is no `option_level` and no `gold_probs`.
- **Length (R1-19; A16.1 (g)).** F3 emits no long rows. The generator measures every row with the real tokenizer (the
  mixer's) on the full decoder_io prompt (cygnet, `schema_branch_mark`), which prints `instructions` twice, so a choice
  row's moved card text counts twice; the sidecar `real_tokens` is this count. It redraws any row at >= 1,900 real tokens, keeping its sampler, QT, option bucket and event-count bin where it can.
  It logs the redraw count per sampler. Logs that carry 20-60-option rows use the S3 length cap. So spec 2.1's 2-row
  long-unit rule never applies to F3.
- **O*NET persona seeds (C14).** Each pack's `persona_seed` is an O*NET main occupation title code (never the
  alternate-titles or SOC direct-match file), drawn by program. The pack declares O*NET as a parent for the 3.H
  deny-list program. O*NET's `no_new_rows` entry passes for this persona-seed parent (spec 2.1). O*NET is credited in
  the notices file. The row licence stays "CC0 1.0 (program-generated)", because seeds are titles inside Claude-written
  packs, not O*NET rows. PersonaHub is never used.
- **IDs (B05, R1-18).** `group_id` is the log: every row from one log, including its twins, shares it.
  `structure_hash` is spec 7.2's canonical problem: facts, stated toggles and query, with the query as G3 check 1
  defines it (decision form, asked values, comparator and `<N>` included; R2-03). So, on one log, a Q1 yes/no row
  asking status value `<A>`, one asking `<B>`, and the Q1 choice row on the same item and point have three hashes.
  G12 and rule 18 use the hash. The 7.2 method-6 leak checks use the coarser `leak_key` (G3 check 1; "Leaks and
  lists" below), which F3 writes to the QC sidecar. Relation units follow spec 2.1. The generator emits at most one
  row per hash (rule 18). G12 keeps exactly one surface form per structure hash; the only exception is an attack twin,
  which shares its clean row's hash. Neg, dneg, fact-flip and premise-removal twins have their own hashes. F3 plans no
  format-variant rows: M4 container variants are G4 test variants and are never emitted.
- **Depth sweep (B14, C13).** Only S5 items. Deep training rows are the <= 10% training slice and never dev items. Dev
  items share no `group_id` or text with any training row (spec 10).
- **Leaks and lists.** The program checks each `leak_key` against the S5 dev items' leak keys. The orchestrator's
  program receives both the hash and the `leak_key` and checks them against the sealed part-P export, counts only; F3
  builders never read that export. Packs, IDs and templates
  go through 7.2 decontamination and the sealed keyword block-list (applied by program; F3 builders never read it). No
  public state-tracking benchmark's format or items are copied.
- **Interfaces** (built after G14 by the pack and format agents; F3 uses them, never edits them):
  - packs (one per F3 card; R1-11): entity pools; one item kind per card (R1-05); holder roles; status lists with
    good/bad polarity tags, the rule-5 lint (holder-change, mechanism and XF06 marker words, and negcount lexicon entries,
    applied to every pack value, masked meaning and swapped word; R3-07, R3-09), the banned-word lint of 2.2 (R1-16) and the unordered-vocabulary
    lint (section 1; R2-04); holding tags per item kind and
    holder role; document types with a "current" polarity tag; high/low tags per quantity; look-alike ID schemes;
    O*NET persona seeds;
  - format styles from the formats-1 pool, rendered only through fmt1 `card.render_row_text` and checked by
    `card.loader_check` (section 1 row layout; R4-05), with the rule-20 renderer lint (no `null`, `~`, empty string,
    empty "key:" or XF06 unknown marker; blanks only where the card states them; R3-06). The pool's 50 held-out styles
    are used only on S5 dev items and never on a training row (S1-S4, S6); training styles are never used on S5;
  - an F3 wording pool of >= 30, with >= 5 per card;
  - the two G3 registries, which enforce 2.2 (phrase lists and negated stem forms).
- **Gates after G0 (C09).** G1-G15 and G17 as in spec 8, with G5 at 300 rows. G15's per-row part is fmt1
  `card.loader_check` on 100% of rows (G3 check 8; A16.1 (g)). G14 (sealed separation) applies to F3's
  generator, packs, style and wording pools and illustrations. G16 is optional and non-blocking (spec decision 11).
  G18 does not apply (no ordinal rows; section 1).

## 7. Points for the G0 ambiguity review (all resolved; details in sections 8-12)

1. **Open-world determinability.** T2's rule (exact setters only, after voids and corrections); no renames, merges,
   transfer check, lock rule or at-time questions on open cards; chronological listing only; VOID and CORRECTION never
   point at a gap and always come after their target; the last entry is always shown. Verified by solver C and its
   lemma test.
2. **A correction to an old entry vs a later SET.** T11: the later SET wins.
3. **A void recorded after the asked date.** T7: it applies retroactively (S6: so does a later-recorded amendment
   effective on or before D).
4. **A voided entry inside a "between" range.** T25: it never counted.
5. **A presupposition in "still" or "no longer".** T31: asked only in Q4 holding stems at the end (never about a
   status, quantity, count, record or transfer; R3-08), and only when the presupposition holds.
6. **An absorbed merge ID vs alias mode.** T15: it is always absorbed.
7. **Same-day entries listed out of order.** Rule 1 and T5: entry numbers follow date and time.
8. **Ambiguous day and month in numeric dates.** T26: the format is stated whenever both readings are valid.
9. **Short or no card.** 2.1: every single variant and every pair must agree.
10. **A note that looks like an entry.** T33: notes never parse as entries (generator rule, G3 grammar).
11. **What "yes" means on a negated stem.** T44 and the 2.2 negated stem forms: no L_core token in the matrix clause
    (no "Doesn't ...?", "Is it not the case that ...?" or "Does `<X>` not ...?"); "still" never with "not"; threshold
    stems negated only at sentence level; no negation together with "no fewer than" or "no more than" (R4-01 to R4-04).
12. **Card text on choice rows.** Section 1 row layout: option-definition lines in `card`, everything else in
    `instructions`, case data in `state`; fmt1 `loader_check` on every row (A16.1 (g); R4-05).

---

## 8. Resolved ambiguities

First review (v2). One semantics per item, as it appears in the card or as a generator rule. "Where" points to the
place in this file that now carries it. Rows A15, B05, B07 and C11 are marked where section 9 refines them; section 9
governs. A = ambiguity that could flip a label; B = ambiguity that cannot flip a label (except B16 and B17);
C = conflict with `C_DATA_SPEC.md` v4, resolved in the spec's favour.

| ID | Resolution | Where |
|---|---|---|
| A01 | Both toggles may be on. A transfer then takes effect iff the sender holds the item and its status is not `<S>` at that moment (T40); T35 step 4 says every stated transfer condition must hold | T40, T35, toggles |
| A02 | T10: every other entry still applies under the card's rules, and every check is made as if the voided entry never existed | T10 |
| A03 | T11: of the non-voided corrections to the same value of an entry, the highest-numbered counts; if all are voided, the original value stands; corrections to different values each apply (R3-01). Solver A step 2 and solver B match | T11, solver A/B |
| A04 | Rule 1: entry numbers increase strictly with (date, time) on S1-S4 and with the recorded date on S6; VOID and CORRECTION are always numbered above their target. The latest-dated reading is added to T11's Alt | rule 1, T5, T6, T11 |
| A05 | Within a card every entry has a time or none does; S4 and S6 have no times | rule 2, toggles |
| A06 | T4: "the end" = after every entry has taken effect in effect order; `<N_last>` dropped | T4 |
| A07 | T4 covers question text only. Inside notices, "today" (= the notice's date) is the only relative time word; all others are banned | T4, T32, 2.2 |
| A08 | S6 version of T7: an entry recorded after D and effective on or before D counts for D | T7 |
| A09 | S6 versions of T24 and T25 use "effective on" | T24, T25 |
| A10 | The S6 snapshot is the state at the end of D0, and every entry takes effect strictly after D0 | T6, S6 sheet |
| A11 | A correction may change only: SET value, ADJUST amount, TRANSFER receiver, CREATE starting status or quantity. Never dates, effective dates, other IDs, sender or entry references | entry-type table, T11, rule 10 |
| A12 | Notices hold numbered changes `<N>`.1, ... that take effect in item order. "Withdraw `<N>`" voids all its changes; "amend `<N>`.`<k>`" targets one. Q8 names `<N>`.`<k>`. Bins count changes | T41, S4 sheet, QT table |
| A13 | S4 notices never state their own date of effect | T41, S4 sheet |
| A14 | Closed-world entry and reference numbers are always consecutive; skipped numbers occur only on open cards | rule 1, T41 |
| A15 | Leading-extract cards show no opening register and state only T9's creation sentence (amended by R1-04) | T3, S1 sheet |
| A16 | Open-world gaps only on chronological listings | T2, toggles, S3 sheet |
| A17 | T2 counts exact setters (creation, setting, transfer), never increases or decreases, which are applied after them; T2 (b) adds the holder just before a shown, non-voided transfer after every gap (R2-08). The lemma test adds a Q1-quantity case | T2, solver C |
| A18 | Open cards state that no entry, shown or missing, renames or merges anything. Solver C's alphabet matches the card exactly | T2, solver C, rule 9 |
| A19 | B is always fresh and created by its SUPERSEDE; A must be current; no forks, joins, cycles or cross-document edges; a supersede is voidable only with no later supersede of that document before the void. T13: "A stays current unless another entry supersedes it"; membership only via the chain | rule 8, T13, T37 |
| A20 | Q3 is asked only at the end of the log | QT table, T13 |
| A21 | Options name each entity by its latest ID only, never two IDs of one entity; old IDs are never options; E8 is entry-level only | rule 12, T14, S2 sheet, E8 |
| A22 | In questions, every ID of an entity names its whole history, under both rename modes (retire: questions use only the new ID; R3-02) | T14 |
| A23 | RENAME and MERGE are banned on S6; "after the rename or merge" means later in effect order | rule 9, T14, T15, S6 sheet |
| A24 | Holders have no status or balance; a merge passes every item regardless of the transfer check or lock; the absorbed holder is "absorbed", a word banned from status lists (with every mechanism and XF06 marker word; R3-07) | entity model, T15, rule 5 |
| A25 | Holder balances dropped | entity model |
| A26 | Q6 counts distinct items (T39); status never changes the holder (T17); release-implying status words banned from packs | T17, T39, rule 5 |
| A27 | Generator rule: no quantity goes below 0 after voids and corrections | rule 7 |
| A28 | "Or" only for one item at one time point, joining two different entities or status values | T23, 2.2 |
| A29 | Range questions are yes/no only | QT table, T25 |
| A30 | Q7: exactly one listed item is held by X at the end (none when the gold is None), checked by solver B | rule 11, solver B |
| A31 | Closed list of date phrases with meanings; every other phrase is banned by the G3 grammar, including a bare "between `<D1>` and `<D2>`" in a stem (only "at any time between" is allowed there; R3-10) | T24, T25, 2.2 |
| A32 | "Still" and "no longer" only in Q4 end-of-log holding stems, never in Q1, Q2, Q3, Q5-Q8 or "on `<D>`" stems (R3-08); the on-date form is "Did X hold Y on D?" | T31, QT table, 2.2 |
| A33 | "At that moment" = after every entry that takes effect before it (T5); the sender may be named by any of its IDs under alias mode; a transfer between two IDs of one holder is a banned self-transfer | T5, T18, rule 6 |
| A34 | 2.1 rows show no NEI or None option and no masked or swapped words; every Alt is a program variant; every single variant and every pair is run; 2.1 covers no-card and short-card rows only | 2.1, section 2 Alt column, definition styles |
| A35 | S3 adds from and to columns; the holder field is never SET (holder changes only by TRANSFER or MERGE) | S3 sheet, T42, entry-type table, rule 5 |
| A36 | S3 uses one entry-number sequence across all change tables, stated in the card | T42, S3 sheet |
| A37 | In S4, inert and attack text goes only in a marked note or postscript, which the card says is not a change | T33, S4 sheet, twins |
| A38 | S5 card (T43): revert is retroactive (it does not act from its own date); move, merge and replace are defined; lines carry sequence numbers for ties and corrections; the listing order is stated | T43, S5 sheet |
| A39 | M6: a gap before the effective writer leaves the label unchanged; a gap between the writer and the end gives NEI on choice rows with k >= 3; k = 2 rows and the yes/no row are dropped (XF01) | M6 |
| A40 | M1 sets the value the field has at the insertion point; on open cards, only other items or entries before the last gap | M1 |
| A41 | Every variant and twin re-passes the generator rules or is skipped and logged; M5's expectation is solver B's recomputation; M5 and fact flips void only voidable types | G4 intro, M5, twins |
| A42 | Premise removal renumbers with no skipped numbers and deletes the VOIDs and CORRECTIONs that point at the deleted entry | twins, rule 1 |
| A43 | T35 step 4 replays entries one at a time in effect order, applying each entry's own rule | T35 |
| A44 | Polarity comes from the card definition, not the word, and is recorded in the QC sidecar | T36, polarity table, section 6 |
| B01 | Glossary: entity = holder, item or document record, with fields and applicable entry types per kind; Q1 and Q2 ask about item fields only | entity model |
| B02 | Depth for multi-item questions, ranges, Q8 and NEI rows is defined; the decisive entry is the latest on the path in effect order; deciles use effect order | depth |
| B03 | Each G10 target is marked family or per sampler; per sampler only for yes rate, polarity, negation, gold letter and mechanism-inert rate | balance table |
| B04 | Polarity is defined per question type from pack tags (status, holding, document "current", quantity direction) | polarity table, section 6 interfaces |
| B05 | `group_id` = the log; `structure_hash` = facts, stated toggles and query, with names assigned in canonical effect order (refined by R1-18) | G3 check 1, section 6 |
| B06 | Only toggles whose trigger occurs on the card are compared in G3 or count toward card distinctness | G3 check 4, card distinctness |
| B07 | Masking and swapping are card-level vocabulary properties. Codes appear in register, entries, rules and options alike. Only status-option rows on such a card count toward the quota (amended by K1) | QT notes, balance table |
| B08 | Q6 has no count options (yes/no thresholds only, C03); at default depth a count covers at most 8 candidate items with N <= 6 | QT table, depth |
| B09 | Every filler is named in an entry or in the opening register (an item or record listed there, or a holder shown holding an item there; R2-09); h9 reports the effective k | rule 12, shortcut table |
| B10 | S2 places the distractor after the decisive entry on 50% +/- 5 of rows; h1 and h5 checks are two-sided | S2 sheet, shortcut table |
| B11 | NEI is shown on every open-world choice row with k >= 3 and never on closed rows or k = 2 rows (XF01) | decision forms |
| B12 | T22 is used by threshold yes/no questions on quantities (Q1, Q2) and counts (Q6) | T22, QT table |
| B13 | Attack twins (about 5%) are a separate quota on top of the 20-25% twin-set share | twins |
| B14 | The depth sweep is S5 only; deep training items are only the <= 10% training slice | depth, S5 sheet, section 6 |
| B15 | "On the boundary" = the decisive entry or tempting distractor is dated exactly D; D +/- 1 entries are near-boundary distractors | S2 sheet, S6 sheet |
| B16 | CREATE always names the holder; transfers move the whole item with its quantity | entry-type table, T9, T17 |
| B17 | A blank cell in a CREATE row starts as `<default>` | T9, T42 |
| B18 | Open cards: holder and item IDs never change; a superseding record is a new record with its own ID | T2 |
| B19 | Each heuristic's yes/no answer is defined per question type | shortcut table |
| B20 | S5 hashes are 12 characters; event bins match training; median length within 15%; length-matched results are reported | S5 sheet |
| C01 | (G10 per-sampler vs sampler design) Targets are checked at family level in the spec's cells; per sampler only for yes rate, polarity, negation, gold letter and mechanism-inert rate | balance table |
| C02 | (Negation quota) Counted by the shared `c_src/common/negcount.py` (XF02): k_syn >= 1 on >= 10% of F3 yes/no rows; k_all >= 1 on >= 15%; k_syn >= 2 with an affirmative twin on >= 3% | balance table |
| C03 | (Ordinal definition) F3 has no numeric choice options: quantities and counts are yes/no thresholds only, and every status vocabulary is unordered (R2-04). No F3 row is ordinal, no carve-out is needed, and the A4 row set is unchanged | decision forms, QT table |
| C04 | (C5 not applied) No sampled per-card gold-NEI rate: closed 0% (by semantics); open rows use gold 1/k per row (XF01). Family NEI and None shares are reported, not tuned | decision forms |
| C05 | (Definition styles) One-line rule list about 20%, one-line + 1-2 illustrations about 50%, decision list or rule table about 15-20%, few-shot overlay 5-10% of cards, short or no card about 15% of rows (2.1) | definition styles, 2.1 |
| C06 | (Label-check form) Yes/no stems are domain questions; the G3 grammar rejects "answer", "option", "choice" and "correct" in stems (whole-word list with inflections: R1-16) | decision forms, 2.2 |
| C07 | (Arithmetic depth) At most 2 unstated additions or subtractions at default depth, as in F2; 3-4 only in deep items; Q6 counts capped | T28, depth |
| C08 | (1-page spec per generator) Each section 4 sheet is that generator's one-page G0 spec; shared sections are referenced by id | header, section 4 |
| C09 | (Gate list) G1-G15 and G17 apply, with G14 named explicitly; G16 optional; G18 not applicable | section 6 |
| C10 | (G14 order) T text is normative semantics, not a template; wordings are written after the freeze and pass 7.2 and the counts-only check before use | header, section 2 intro |
| C11 | (Card definition) Cards differ in pack and in stated rule set or label schema, read pairwise: one pack per card (refined by R1-11); unstated toggles never count | card distinctness |
| C12 | (S2 look-alike IDs) Every S2 row has at least one E4 look-alike-ID distractor event | S2 sheet |
| C13 | (Depth sweep source) Sweep items come from S5 only; training deep items never become dev items | depth, section 6 |
| C14 | (Provenance) Packs declare O*NET as a 3.H parent (`no_new_rows` passes), credit it in the notices file, and use main titles only; the row licence stays CC0 | section 6 |
| C15 | (Row format) No `meta.f3`; F3 fields go to the QC sidecar keyed by row id, so rows carry only the spec 2.4 keys | section 6 |

---

## 9. Resolved ambiguities (G0 re-review, round 1)

One semantics per item, as it appears in the card or as a generator rule. "Flip" = the reviewer marked that the item
could flip a label. K1 is the one spec conflict, resolved in favour of `C_DATA_SPEC.md` v4. Where this table and
section 8 differ, this table governs.

| ID | Flip | Resolution | Where |
|---|---|---|---|
| F3-R1-01 | yes | The CORRECTION cell now matches A11 exactly. A correction changes only a SET value, an ADJUST amount (size only), a TRANSFER receiver, or a CREATE starting status or quantity. It never changes a date, effective date, sender, item ID, record ID, any holder ID other than a TRANSFER's receiver, or an entry reference | entry-type table, T11, rule 10 |
| F3-R1-02 | yes | VOID and CORRECTION name their target by entry number only, restate no IDs, and act on the target at the target's point in effect order. The "names a retired or absorbed ID, no effect" rule is checked on the corrected target at that point, never on the VOID or CORRECTION entry. Generator rule: a corrected receiver is valid at the target's point (an ID from a later rename is never used there, under either mode; R3-02), and a CORRECTION that comes after a rename or merge never uses an ID that is retired or absorbed at its own point. So both readings give the same holder (in the reviewer's example, the correction to W is never generated). Solvers A and B follow the same rule | entry table, rule 10, T10, T11, T14, T15, solvers A and B |
| F3-R1-03 | yes | T25 is generic: "`<condition>` at any time between D1 and D2" is true if the condition holds at the start of D1 or right after any non-voided entry dated D1 to D2 takes effect, same-date entries included. An entry that changed nothing (a blocked transfer, a retired or absorbed ID) changes no value. The condition is a status value or a quantity threshold of one item; no question asks a holding range. Q2 asks only about items that exist at the start of D1 (rule 15). M7, solver A step 5, solver B and h1 (range: last-listed entry dated at or before D2) match | T25, rule 15, M7, solvers A and B, h1 |
| F3-R1-04 | yes | Leading-extract cards state T9's creation sentence only: "a creation always names the holder; any other field it leaves blank starts as '`<default>`'". They still show no opening register. Solver A applies it | T3, solver A step 4, S1 sheet, A15 |
| F3-R1-05 | yes | Option (a): each card has exactly one item kind, so `<items>` in Q6 and Q7 means every item on the card. Kind is not a field and never changes. T39 says "every `<item>` in this log is a `<kind>`". Holder role is a hidden pack attribute used only for the Q4 and Q8 polarity tag, never by a rule or label | entity model, rule 14, QT table, T39, polarity table, section 6 |
| F3-R1-06 | yes | Closed cards and open explicit-marker or skipped-number cards start at entry 1 (S4: reference 1), and their gaps lie only between shown entries. Only leading-extract cards start at N0 > 1, and they have no other gap. On S4, changes in each notice run .1, .2, ... with no skips, and gaps are whole notices only. The card text in T3 and T41 says so. M6 is adapted for leading extracts | rule 1, T3, T41, S4 sheet, M6 |
| F3-R1-07 | yes | T31 defines "at some point" as in T25: in the opening state, or right after any non-voided entry takes effect. Generator guard: "still" and "no longer" rows (Q4 end-of-log holding stems only, twins included; R3-08) are made only when X held Y in the opening state or at the end of some date. On open cards, solver A decides the guard from known values and solver C confirms it in every world. So a reader who uses end-of-day states gets the same label | T31, solver A step 5, solver B |
| F3-R1-08 | yes | A correction to an ADJUST changes only its size (n >= 1). Its direction stays, and its text restates the direction (for example, the decrease in entry `<N>` should be `<n>`). Rule 7 is checked after the correction | entry table, rule 10, T11 |
| F3-R1-09 | no | Solver C keeps only worlds that satisfy every rule the card states. Rule 6 is now stated on every card with the transfer check off (T17: in every non-voided transfer that names no retired or absorbed ID, the named sender holds the item just before it). Rule 7 is now stated (T28: no quantity is ever below 0). Rule 1 order is stated by T3 and T5. Thresholds are >= 1 (rule 16). Solver A records a shown, non-voided transfer's sender as the holder just before it when the transfer comes after every gap. Lemma test: new case for this, plus the one-way property (A known implies C same; A UNKNOWN on a choice row implies C undecided) | T2, T17, T28, rules 6 and 16, solvers A and C, lemma test |
| F3-R1-10 | no | Q8 is on S4: "Did change `<N>`.`<k>` take effect?" for a transfer change, on closed cards with the transfer check, the lock rule or a withdrawal | S4 sheet, QT table |
| F3-R1-11 | no | Spec 2.1 is read pairwise, which also meets the looser reading. Each F3 card has its own domain pack (95 in round 1, 180 in round 2, above the 30 and 40 floors). Every two cards also differ in stated rule set or label schema. G11 checks both conditions over all pairs; a collision is fixed by redrawing a card's toggles or QT set | card distinctness, section 1 table, section 6 |
| F3-R1-12 | no | An inverted card is one whose rows are all Q7 (with twins), and Q7 appears only on inverted cards. Inverted cards are closed, fully stated, and on S1-S3. Inverted-card share (10-15% of cards) and Q7 row share (10% +/- 3) are checked separately | rule 17, QT notes, S1-S3 sheets, balance table |
| F3-R1-13 | no | Every F3 target is checked on the final selected set after G9. Selection stays inside spec 2.1's cells. Within each cell, a quota sampler picks whole relation units with their twin sets. A failed target is repaired by swapping whole units from same-cell surplus, or by generating more for that cell; a label is never changed. Abstain gold is 1/k +/- 2 pp per k bucket and per abstain option (XF01); there is no per-card NEI count. Per-card yes rate: base yes/no rows within +/- 5 pp of the drawn rate, all yes/no rows in 20-80% (cards with < 10 base yes/no rows: band only; R2-05) | decision forms, section 5 |
| F3-R1-14 | no | `meta.deep` = (depth >= 5) OR (3-4 unstated additions or subtractions) OR (Q6 over > 8 candidate items or N > 6). Candidate items are those X holds at some point. Deep rows are outside the d1-d4 mix and inside the <= 10% slice. Caps: depth 8, 4 unstated operations, deep Q6 20 candidates with N <= 15 | depth section, balance table |
| F3-R1-15 | no | The 2.2 date-phrase, end-word, "or" and banned-word lists apply to question stems and their negation and twin frames only. Card rule text and log or notice text follow the surface-grammar registry (so T6, T7 and S6 "effective" dates are valid). The notice list applies to notice text | 2.2 |
| F3-R1-16 | no | Whole-word, case-insensitive ban on answer, answers, answered, option, options, choice, choices, correct, correctly, incorrect, incorrectly in yes/no stems. "Correction", "corrected", "corrects" and "optional" are allowed. A pack lint keeps the eleven words out of status values, item kinds, holder and document names, roles and IDs | decision forms, 2.2, section 6 |
| F3-R1-17 | no | Illustration and worked-example blocks are marked. The parser checks their IDs against their own mini-structures, and solver A checks their stated outcomes (G3 check 7). The row's `structure_hash` and G3 check 3 cover the row's log, query and options only | definition styles, G3 |
| F3-R1-18 | no | `structure_hash` = spec 7.2's canonical problem: facts, stated toggles and query (decision form, asked values, comparator and N, negation count and polarity included; for Q7, the candidate items; R2-03). It excludes Q1-Q5 answer options. The 7.2 leak check matches on the coarser `leak_key`, so it is never narrowed. The options are checked separately (G3 check 6). The generator emits at most one row per hash (rule 18). G12 keeps one surface form per hash, except attack twins. F3 emits no format-variant rows; M4 variants are test-only | G3 check 1 and 6, rule 18, section 6 |
| F3-R1-19 | no | F3 emits no long rows. Every row is measured with the real tokenizer and redrawn at >= 1,900 tokens, with a redraw count logged per sampler. Logs with 20-60-option rows have at most 24 entries and 70 register rows plus entries, with ID-only options. The draw plan keeps the 15% bucket | section 1 table, S3 sheet, section 6 |
| F3-R1-20 | no | S6 listings are recorded order, sorted by effective date (stated), or shuffled with both dates (stated); S6 has no non-time sort. S6 query dates: "on", "as of" and "at the end of" use D >= D0; "at the start of" and range starts use D > D0 | toggles, S6 sheet, rule 15 |
| F3-R1-21 | no | An S4 withdrawal is one numbered change M.k, rendered as one sentence, that expands to n VOIDs in the structure. It counts once for the event-count bins and the 5-40 limit. Depth adds +1 only for an expanded VOID that removes a candidate writer | S4 sheet, T41, depth section |
| F3-R1-22 | no | `<None option>` appears only on Q7 rows (always there; k >= 3 and gold 1/k by XF01). Q1, Q2, Q3 and Q5 choice rows always list the true answer; an open-card row with NEI gold lists `<NEI option>` instead | decision forms, rule 13, balance table |
| K1 | spec conflict | The spec 2.1 and 6 masked and swapped quotas count only status-option rows (Q1 or Q2 status choice, including on lock-rule cards). Q3, Q5 and Q7 rows never count, even on masked or swapped cards. Over all F3 choice rows: masked status-option rows 10-15%, swapped 5% +/- 1. Planned: about 20-30% of non-inverted cards are masked or swapped, each with >= 70% status-option choice rows. Checked on the selected set | QT notes, balance table, B07 |

---

## 10. Resolved ambiguities (G0 re-review, round 2)

One semantics per item, as it appears in the card or as a generator rule, consistent with `C_DATA_SPEC.md` v4 and
section XF. Items written before section XF were checked against it: XF01 settles F3-R2-11 (c) and XF03 settles the
counting part of F3-R2-11 (a); only their F3-specific remainder is resolved here. The round-2 file listed no spec
conflict. Where this table and sections 8 or 9 differ, this table governs; the earlier rows it touches (A17, B09, C03,
R1-13, R1-18) have been edited to match.

| ID | Flip | Resolution | Where |
|---|---|---|---|
| F3-R2-01 | yes | **Negation scope with "or" and ranges.** A stem with "or" carries no negation cue and no "still" or "no longer"; a range stem carries no negation cue (a T22 comparator inside its condition is allowed and is not a cue; R3-09). In both, the only negation is the outer frame "Is it false that ...", which scopes over the whole claim. The parser rejects "not", "n't", "never", "no longer" and implicit cues there, and rejects "at no time between" (no such phrase is added). M9 negates these stems with the outer frame only and makes no dneg variant (skipped and logged). "Or" joins two holders or two status values of one item at one point; an "or" stem is made only when both disjuncts carry the same polarity tag, and that tag applies | T23, T25, 2.2, M9, section 5 negation cues and polarity table |
| F3-R2-02 | yes | **More Alts for the 2.1 check** (the ban alternative is not used). T24 Alt (b): "on `<D>`" (and "as of `<D>`", R3-04) = at any time during `<D>` (start of `<D>` or right after any entry dated `<D>`). T25 Alt (b): "between" excludes `<D1>`, `<D2>` or both (three variants). T17 and T39 Alts: an item with quantity 0 is not held and not counted. A variant with no single answer counts as a different label. Full cards state the reading: T17 adds "An `<item>` whose `<quantity>` is 0 still exists and still has its holder", and T39 counts items "including any whose `<quantity>` is 0" | T17, T24, T25, T39, 2.1 |
| F3-R2-03 | no | **Hash query.** query = (question type, decision form, entity references, asked values including each "or" value, comparator and N, date points, negation count and polarity, Q7 candidates). So the two yes/no rows "status A?" and "status B?" and the choice row on one point are three hashes and may all be emitted. The 7.2 method-6 leak checks use a coarser `leak_key` (facts, stated toggles, question type, entity references, date points), written to the QC sidecar, so they are never narrower than before | G3 check 1, rule 18, section 6 (IDs, sidecar, leaks), R1-18 |
| F3-R2-04 | no | **Unordered status vocabularies.** A pack lint rejects status lists with level numbers or ranks, or a graded scale; masked codes are opaque IDs, never a numbered sequence. So no F3 row is ordinal under spec 2.4, no `option_level`, no G18, and the A4 row set is unchanged | section 1 decision forms, section 6 interfaces, C03 |
| F3-R2-05 | no | **Per-card yes rate.** The drawn rate (+/- 5 pp) applies to base yes/no rows (no `twin_of`). All yes/no rows, twins included, must be in 20-80%. Cards with < 10 base yes/no rows: band only. The G10 aggregate 50% +/- 2 counts all yes/no rows | section 5 per-card targets, balance table, R1-13 |
| F3-R2-06 | no | **Order key of VOID and CORRECTION.** They act at their target's point, but wherever the spec places them in effect order they use their own key: S1-S3 (date, time, entry number); S4 (date, reference number, change number); S6 (recorded date, entry number), compared as if it were an effective date. This fixes rule 8's window (S6 included), the decisive entry and its decile (a CORRECTION on the path uses its own key), and the place of VOID and CORRECTION lines in an S6 listing sorted by effective date (by recorded date; the card's sort sentence says so) | rule 10, rule 8, depth section, S6 sheet |
| F3-R2-07 | no | **Items exist when named.** Rule 15 covers every question that names an item: Q4 "on `<D>`" at the end of `<D>`; Q4 at the end, Q5 and every listed Q7 item at the end; Q8's item at the transfer's point. New rule 19: no CREATE names a retired or absorbed ID; no entry names an item before its CREATE in effect order; on open cards a missing entry never creates an item the shown text names | rules 15 and 19 |
| F3-R2-08 | no | **T2 as "if and only if".** A value at a point is known if and only if (a) its last shown exact setter at or before that point, after voids and corrections, comes after every missing entry (later increases and decreases applied), or (b) it is the holder just before a shown, non-voided transfer that comes after every missing entry (T17's sender rule), or (c) it is a register value at the opening point (added by R3-03). T34 now says "exactly when". Solver A step 4 matches | T2, T34, solver A step 4, A17 |
| F3-R2-09 | no | **Fillers.** Every filler option is named in an entry or in the opening register (an item or record listed there, or a holder shown holding an item there). Rule 12, section 5 and the S3 sheet use this one wording | rule 12, section 5 wrong options, S3 sheet, B09 |
| F3-R2-10 | no | **Solver C on S4.** A missing notice (one per skipped reference number; one or more per marker) is dated between its neighbours and holds 1-4 changes from the alphabet, with "withdraw notice `<M>`" in place of VOID and "amend `<M>`.`<k>`" as CORRECTION. Solver C enumerates one-change notices; the property test adds 2-4-change notices, including withdrawals, and checks the verdict never changes. Fresh values only for quantities and holders, never for status; T36 joins the world filter, and T41 joins it on S4 | solver C, lemma test |
| F3-R2-11 | no | (a) Counting is fixed by XF03 (only label-flip contrast sets count). A closed premise-removal variant whose label does not flip is logged and dropped, never emitted. (b) The inert rule covers VOID, CORRECTION, SUPERSEDE, RENAME, MERGE and the transfer conditions (check and lock as one). An entry mechanism is decisive when it is a hop on solver B's decisive path; the transfer conditions appear when stated and the path has a transfer, and are decisive when a stated condition blocks a transfer on the path. Plain SET, TRANSFER and ADJUST have no inert target. (c) Fixed by XF01: each abstain option is wrong on 1 - 1/k >= 2/3 of the rows that show it (spec floor 50%); there is no separate 80% bar | section 5 twins and balance table, S1 sheet, section 1 decision forms |

---

## 11. Resolved ambiguities (G0 re-review, round 3)

One semantics per item, as it appears in the card or as a generator rule, consistent with `C_DATA_SPEC.md` v4 and
section XF. The two spec conflicts (R3-C1, R3-C2) are resolved in favour of section XF (XF06, XF10), and the earlier
text they touch (2.1, T8, T25, M9, section 5 negation cues, the XF06 and XF10 effect rows) now states one rule. Where
this table and sections 8-10 differ, this table governs; the earlier rows it touches (A03, A22, A24, R1-02, R2-02,
R2-08) have been edited to match. Rows F3-R3-08 to F3-R3-10 (v6) resolve the items left open after v5, all three
label-flipping stem readings; the earlier text and rows they touch (T4, T13, T25, T31, T36, T38, rule 5, the QT
table, 2.2, M9, section 5 negation cues, section 6 interfaces, section 7 point 5, A31, A32, R1-07, R2-01, R3-07,
R3-C2) now state one rule. No spec
conflict was open.

| ID | Flip | Resolution | Where |
|---|---|---|---|
| F3-R3-01 | yes | **Corrections act per value.** A CREATE has two correctable values (starting status, starting quantity). Of the non-voided corrections to the same value of one entry, the highest-numbered counts; if all are voided, that value stays as recorded; corrections to different values of one entry each apply. So in the reviewer's case (entry 6 corrects entry 2's status to `<S>`, entry 9 corrects its quantity) both apply. The per-entry reading is T11 Alt (e) and runs in the 2.1 check | entry-type table, T11 (+ Alt (e)), T35 step 2, solver A step 2, solver B, 2.1, A03 |
| F3-R3-02 | yes | **IDs name the whole history.** Under both rename modes, every ID of an `<item/holder>` names its whole history in questions, before and after any rename; the date of a rename or merge decides only whether an entry is valid (an old ID after a retire-mode rename; an absorbed ID after a merge) and which `<items>` a merge passes. Generator rule (both modes): no entry that takes effect before a rename, and no corrected value at a pre-rename point, uses the new ID that rename gives (rule 9; rule 10's parenthetical now covers both modes). The card says so in T14. Solver A maps question IDs through the whole-log rename map (its replay alias map is used only for entries); solver B's query closure is whole-log, and its timed rename and merge edges only decide entry validity. New T14 Alts for the 2.1 check: (b) a new ID names only the history after its rename; (c) alias only: an old ID names only the history before it. Merges are unchanged: an absorbed ID is never an alias of the survivor (T15) | T14 (+ Alts (b), (c)), rules 9 and 10, solver A step 4, solver B, 2.1, A22, R1-02 |
| F3-R3-03 | yes | **Opening register is known on open cards.** T2 adds (c): a value shown in the `<opening register>` is known at the opening point, before entry 1 (no entry is missing before entry 1, and no void or correction names the register). Stated on explicit-marker and skipped-number cards (the ones with a register); leading extracts show no register and leave (c) out. So T2 agrees with T9, and T31's "at some point" can rest on the opening state. Solver A step 4 starts replay with every register value known at the opening point, so solver A authors make the same rows. The lemma test adds open cards whose T31 guard rests only on the register | T2, T31, solver A step 4, lemma test, R2-08 |
| F3-R3-04 | yes | **T24 Alts cover "as of".** T24 Alts (a) start of `<D>` and (b) any time during `<D>` apply to "on `<D>`" and to "as of `<D>`" (every T24 phrase except "at the end of `<D>`" and "at the start of `<D>`"), in every question type, Q4 "Did `<X>` hold `<Y>` on `<D>`?" included. A 2.1 row whose label differs under either Alt for either phrase is dropped | T24 Alt column, 2.1 check, R2-02 |
| F3-R3-05 | yes | **S5 date order = sequence order.** Rule 1 now covers S5: the sequence number is the entry number and strictly increases with (date, time), so date order and sequence order agree. T43 states it and says that "dated" in T24 and T25 means a line's date. Solver A's S5 key (sequence number) equals (date, time, sequence number) order. The S5 sheet's tie and "highest correction" rule uses the sequence number, consistent with this | rule 1, solver A step 3, T43, S5 sheet |
| F3-R3-06 | yes | **Blank in JSON, YAML and key-value.** An F3 blank there is a left-out key, never `null`, `~`, an empty string or an empty "key:". The card's T8 adds "A field left out of an entry is a blank field" on those containers (T42 adds it for S3 JSON and YAML arrays). New rule 20: F3 writes no XF06 unknown marker and no "none", "no" or `false` field value (unknown comes only from open-world gaps); the only marker it writes is "0" for a zero `<quantity>`; the opening register gives every field, so it has no blank. A renderer lint rejects violations, and G3 treats them as parse failures. The orchestrator-owned marker table (`common/MARKERS.md`, F3 row "Missing key: not specified") is referenced, not edited; F3's missing-key meaning is "a blank, as T8 states" | T8, T42, rule 20, S1 and S3 sheets, G3 parser, section 6 interfaces, XF06 effect row |
| F3-R3-07 | yes | **Mechanism and marker words.** The rule-5 pack lint now rejects any status value, masked code and meaning, swapped word and definition, item kind, holder or document name, role or ID that, as a whole word in any case, equals or inflects a mechanism stem (void, cancel, withdraw, amend, correct, fix, supersede, replace, rename, renumber, move, retire, merge, consolidate, absorb, transfer, revert, create, adjust, missing) or equals or contains an XF06 marker ("unknown", "not recorded", "none", "no", "0", "null", "false", the banned markers) or the card's NEI, None or gap-marker wording. "Moved" joins the holder-change words. The swapped-word and masked-meaning draws use the same lint. So no card defines a status as "void", "cancelled", "retired" and the like, and no Q1 option "unknown" sits next to the NEI option. R3-09 adds a third lint bullet: no negcount lexicon entry (L_core token or implicit-cue verb inflection) in any pack value | rule 5, T36, section 6 interfaces, A24 |
| F3-R3-C1 | spec conflict (XF06) | **Blanks on 2.1 rows.** XF06 allows blanks only where the card states their meaning. A short card always states T8's blank sentence (with its left-out-field form), T9's creation sentence when a creation leaves a field blank, and T42's blank sentence in S3 containers; the rule it leaves out is another triggered rule. No-card rows show no blank: only prose, bullets or log lines (no table, CSV, JSON, YAML or key-value record, so no S3 container), with every creation stating each starting value. S3 rows under 2.1 are short-card rows only | 2.1 (blanks bullet), rule 20, S1 and S3 sheets, XF06 effect row |
| F3-R3-C2 | spec conflict (XF10) | **Negation frames.** "Is it false that ..." is a truth frame and wraps only an affirmative claim (negcount k_all = 0 inside; so under that frame a range comparator is "at least", "at most", "more than" or "fewer than"; a range stem with "no fewer than" or "no more than" gets no neg twin). A dneg is truth-frame double negation, form D of 2.2 as refined by R4-01: "Is it true that it is not the case that ..." over the declarative of an N1, N2 or N3 stem (inner cue "not", "n't", or a cue the stem's QT allows: "no longer" in Q4 end stems, T13's "lack" in Q3, "fail to take effect" in Q8; never a comparator phrase; R3-08, R3-09), never "is it false that" over a negated claim. No judgement or acceptance predicate is used. The G3 stem grammar rejects "Is it false that" over any claim with k_all >= 1. "Or" and range stems stay outer-frame-only with no dneg (R2-01) | 2.2 (negated stem forms: frames, "or" and range stems), T25, M9, section 5 negation cues, XF10 effect row |
| F3-R3-08 | yes | **"Still" and "no longer" only in Q4 holding stems.** They appear only in Q4 end-of-log holding stems ("Does `<X>` still hold `<Y>`?", "`<X>` no longer holds `<Y>`" and their M9 frames), with T31's meaning: "no longer" = held at some point (opening state or right after a non-voided entry) and not held at the end. The G3 stem grammar rejects them in Q1, Q2, Q3, Q5, Q6, Q7 and Q8 stems, in Q4 "on `<D>`" stems and in "or" stems. Q1 and Q3 are negated with "not" / "n't" inside "Is it true that ...", "it is not the case that", the outer frame over an affirmative claim, or (Q3) T13's "lack" stem (R3-09), in the 2.2 negated stem forms (R4-01). So "Is Y's status no longer S?" and "Is R no longer the current record of D?" are never made, and no presupposition reading for statuses or records is needed. T4 no longer lists "still" and "no longer"; their end point comes from T31's card sentence. The T31 guard binds every row whose stem has "still" or "no longer", neg and dneg twins included (a twin that fails it is skipped and logged); under the guard, "no longer" is the complement of "holds at the end", as M9 expects | T4, T31, QT table (Q4 row, stem-words paragraph), 2.2 (end words, negated stem forms), M9, section 5 negation cues, section 7 point 5, A32, R1-07, R3-C2 |
| F3-R3-09 | yes | **Each implicit cue has one stem form and one T rule.** Q3: "Does `<document>` lack `<R>` as its current record?" means NOT (`<R>` is the current record of `<document>` at the end of the log), for any `<R>` the stem names, including a record that never existed because its superseding entry was voided; T13 states it on every card with such a row, and no-card rows never use it. The document-only "Does `<document>` lack a current record?" is rejected by the G3 stem grammar (T13 would make it always "no"). Q8: "Did the transfer in entry `<N>` (S4: change `<N>`.`<k>`) fail to take effect?" means NOT (it took effect); T38 states it. The parser rejects "lack", "fail" and any other implicit cue in any other form or QT. "No fewer than" and "no more than" are T22 comparators, not negation cues: negcount counts them in k_all (XF02), but they mean "at least" and "at most", so they never build a neg or dneg twin and are never a dneg's inner cue. A new rule-5 lint keeps every negcount lexicon entry (L_core tokens and implicit-cue verbs with their inflections, for example "failed", "denied", "lacking") out of pack values, so a stem's negcount and cues come only from its negation cues; the shared `negcount.py` is referenced, not edited | T13, T38, rule 5, T36, section 6 interfaces, QT stem-words paragraph, 2.2 (implicit cues, negated stem forms), M9, section 5 negation cues, R2-01, R3-07, R3-C2 |
| F3-R3-10 | yes | **No bare "between" in stems.** In a question stem, "between `<D1>` and `<D2>`" appears only inside "at any time between `<D1>` and `<D2>`", whose meaning T25 fixes (existential, both dates included). The G3 stem grammar rejects a bare "between" in a stem (for example "Was Y's status S between D1 and D2?"), so no "throughout the range" reading can arise. The bare phrase stays only in T25's card inclusivity sentence (card text is outside the 2.2 stem lists, R1-15) | T25, 2.2 (date phrases), QT stem-words paragraph, A31 |

---

## 12. Resolved ambiguities (G0 final review, round 4; frozen)

One semantics per item, as it appears in the card or as a generator rule, consistent with `C_DATA_SPEC.md` v4,
section XF and `PREREG_FINAL.md` A15, A16 and A16.1. Items: the round-4 review (`G0_OPEN_r3.json`: 4 label-flip
ambiguities and 1 spec conflict), the cross-family item that names F3 (`G0_CROSS_ISSUES_r2.json` item 3) and ruling
A16.1 (g). Where this table and sections 8-11 differ, this table governs; the earlier text and rows it touches (2.1,
2.2, T13, T31, T38, the QT stem-words paragraph, M9, section 5 negation cues, G3, sections 6 and 7, R3-08, R3-09,
R3-C2 and the XF10 effect row) now state one rule. After this round F3 has 0 open label-flip ambiguities, and this
file is frozen (`G0_FROZEN.json`).

| ID | Flip | Resolution | Where |
|---|---|---|---|
| F3-R4-01 | yes | **Answer convention for negated stems.** New T44: "Answer 'yes' exactly when the statement the question asks about, read with every 'not' and every negative word in it, is true", with the meaning of "Is it true that", "Is it false that" and "it is not the case that". The 2.2 negated stem forms keep every L_core token out of the matrix clause, so the G3 stem grammar rejects fronted negated auxiliaries ("Doesn't/Isn't/Didn't/Wasn't ...?", the question "Is it not the case that ...?") and a main-clause "not" or "no longer" ("Does `<X>` not hold `<Y>`?", "Does `<X>` no longer hold `<Y>`?"). L_core negation stands only inside "Is it true that ..." (N1, N2, N4); the outer frame "Is it false that" over an affirmative claim stays (N5); the T13 and T38 implicit stems stay (N3, whose yes meaning those rules state). The dneg is D, "Is it true that it is not the case that ..." over an N1, N2 or N3 declarative. Every card with a negated row states T44, short cards included; no-card rows get no neg or dneg twin (skipped and logged). On negated 2.1 rows every Alt applies inside the negation, and T24 Alt (b) also runs with the negation inside "at any of those points". In the reviewer's example (X does not hold Y at the end), "Doesn't X hold Y?" is never made; F3 asks "Is it true that X does not hold Y at the end?" (yes under T44), and its dneg "Is it true that it is not the case that X does not hold Y at the end?" is no, the label of "Does X hold Y at the end?" | T44, 2.1 (negation bullet, check, not varied), 2.2 (negated stem forms), QT stem-words paragraph, T13, T31, T38, M9, section 5 negation cues and balance table, G3 (parser, check 5), section 6 sidecar `neg_form`, section 7 point 11, R3-08, R3-C2, XF10 effect row |
| F3-R4-02 | yes | **"Still" never with "not".** A "still" stem never carries "not" or "n't": no "Does `<X>` still not hold `<Y>`?" and no N1 or N4 over a "still" claim. It is negated only by N2 ("Is it true that `<X>` no longer holds `<Y>`?", the complement under the T31 guard) or N5 ("Is it false that `<X>` still holds `<Y>`?"), and its dneg is D over N2 ("Is it true that it is not the case that `<X>` no longer holds `<Y>`?"). So the continuative-negative reading ("X went on lacking Y") never arises, and M9's NOT label holds | 2.2 ("still" bullet, form table), T31, M9, section 5 negation cues |
| F3-R4-03 | yes | **Numeral scope in threshold stems.** A threshold stem (Q1 and Q2 quantity thresholds, Q6, range conditions) is negated only by a sentence-level operator: N4 ("Is it true that it is not the case that `<X>` holds at least `<N>` `<items>` at the end?") or N5 ("Is it false that ..."); ranges and "or" stems by N5 only. "Not" or "n't" never stands on a threshold claim's verb or next to its comparator or numeral, so the wide-scope reading ("there are at least `<N>` `<items>` that `<X>` does not hold") cannot arise. Threshold stems get no dneg twin (skipped and logged) | 2.2 (threshold bullet, form table), M9, section 5 negation cues |
| F3-R4-04 | yes | **Comparator phrases under negation.** On every threshold stem, not only ranges, "no fewer than" and "no more than" never share a stem with a negation cue (N1-N5 or D). A row whose claim uses either phrase gets no neg and no dneg twin (skipped and logged); a negated threshold row uses only "at least", "at most", "more than" or "fewer than". The G3 stem grammar rejects either phrase in a negated stem, so the negative-concord reading ("does not have no fewer than 5" read as "does not have fewer than 5") never arises | 2.2 (implicit cues, comparator bullet, "or" and range bullet), M9, section 5 negation cues |
| F3-R4-C1 | spec conflict (XF10) | **XF10's truth-frame form vs F3 2.2.** In XF10's favour. Every F3 negation is written in XF10's truth-frame form (R4-01): no "Does `<X>` not ...", no fronted "n't", no main-clause "no longer". "Is it false that" over an affirmative claim, and "it is not the case that" directly after "Is it true that", are truth frames. The XF10 effect row now reads XF10 as both the judgement-predicate ban and the truth-frame form, and names F3's extra bans as F3-local rules (R4-X3) | 2.2 (negated stem forms), XF10 effect row |
| F3-R4-X3 | cross-family (`G0_CROSS_ISSUES_r2.json` item 3) | **XF10 scope.** F3's XF10 rule text carries the scope sentence: the shared lint bans only outer judgement or acceptance predicates; "Is it true that", "Is it not the case that" and "Is it false that" over an affirmative claim are allowed; a family may ban more on its own, as a family-local rule not cited as XF10. Every F3 frame is compliant: N5 is "Is it false that" over an affirmative claim, and N1, N2, N4 and D sit inside "Is it true that". F3's ban on the question "Is it not the case that ...?" and on every other L_core token in the matrix clause is an F3-local G3 rule (R4-01), not XF10, so a shared lint built to the scope sentence accepts every F3 row, including the D rows that carry the k_syn >= 2 quota. No F3 label changes | XF10 rule and effect row, 2.2 (frames bullet) |
| F3-R4-05 | ruling A16.1 (g) | **Choice rows: card text in `instructions`, option definitions as card lines.** Section 1 row layout: every row is built with fmt1 `card.render_row_text`. Yes/no rows (Q1-Q4, Q6, Q8) keep the whole card in `card`. On choice rows (Q1 and Q2 status choice, Q3, Q5, Q7), `card` holds only "- `<exact option text>`: `<definition>`" lines (the masked code meaning or swapped definition of each status value shown as an option); every other card element (task line, every stated T rule including T34's abstain meanings, the T36 value list and the meanings of values not shown as options, illustrations, worked examples, decision list or rule table, the inverted-card frame) goes to `instructions` in the card style and the instruction position's order; `state` holds case data only. Every row passes fmt1 `card.loader_check` with `card.must_show` (G3 check 8; G15's per-row part). The G3 parser reads the card text where it is placed; G6 inputs are taken before placement. Every length figure is measured on the served prompt, which prints `instructions` twice (< 1,900 cap and redraw, median, sidecar `real_tokens`, S3 length cap). Training rows never use the 50 held-out styles; S5 items use only them. No label changes, and the outer layout is unchanged | section 1 (token length, row layout, masked and swapped vocabulary), S3 sheet, G3 (parser, check 8), section 6 (length, interfaces, gates), section 7 point 12 |

---

## XF. Cross-family alignment (orchestrator fixes, 3 Oct 2026)

The cross-family consistency review (18 issues over F1-F13 and COMMIT) set one rule for every family where families
differed. **This section governs over every earlier section of this file**, including the resolved-ambiguity tables;
the earlier text it changed has been edited to match (round-2 resolver; the XF06 and XF10 effects were completed by
the round-3 resolver, R3-C1 and R3-C2), so no earlier row states a conflicting number
or rule. No label of an existing
row changes, because no C row exists yet (G14). Code named here (`c_src/common/...`) is orchestrator-owned and is
written only after the sealed sha256 commit.

| ID | Rule (same text in every family that carries it) | Effect in F3 |
|---|---|---|
| XF01 | **Abstain gold = 1/k (display-then-gold).** Draw k (abstain slots included), then the display, then the gold slot uniformly over the displayed slots; reject structures whose gold class does not match. An abstain option (NEI, CBD, None, 'none of these', 'no record', tie options) is shown only when k >= 3 and only on rows where it can be gold; no always-wrong abstain display. Each abstain option is gold with probability exactly 1/k; G10 checks 1/k +/- 2 pp per k bucket and per abstain option, so G6(b) and G7 (p0 = 1/k) sit at chance. The ~10% NEI aggregate is only a mixer count; no family tunes toward it. | Section 1 decision forms rewritten: `<NEI option>` on every open-card choice row with k >= 3 (none at k = 2), never on closed rows (v3's 15% always-wrong closed display dropped); `<None option>` on every Q7 row (k >= 3); each gold with probability 1/k. The fixed 20% open-card NEI, the ~10% Q7 None rate and the family bands (NEI 5 +/- 2, None 2 +/- 1) are removed; shares are reported only. Rule 13, M6, the premise-removal twin, the per-card targets, the balance table and rows A39, B11, C04, R1-13, R1-22 are updated. |
| XF02 | **One negation counter.** Every family uses the orchestrator-owned `c_src/common/negcount.py` (not written by any family builder). k_syn = number of F5 L_core tokens in the question (not, n't, no, none, nobody, nothing, nowhere, never, neither, nor). k_all = F5 L_neg surface count (longest match; comparator phrases such as 'no fewer than' and implicit cues included; C_DATA_SPEC 2.2 F5). 2.1 quotas use k_syn: k_syn >= 1 on >= 10% of yes/no rows; k_syn >= 2 with an affirmative twin on >= 2%. G10 yes-rate negation-count cells use k_all. Whether an L_core token inside a matched multiword comparator entry (the 'no' of 'no fewer than') counts toward k_syn is fixed once inside negcount, never per family. A family-local cue list may stay for polarity logic only. | Balance row 'Negation (C02)' now counts with negcount: k_syn >= 1 on >= 10%, k_all >= 1 on >= 15%, k_syn >= 2 with an affirmative twin on >= 3% (F3's own floor, above 2.1's 2%); G10 negation cells by k_all. Row C02 updated to match. |
| XF03 | **Twin-set count.** A row counts toward 2.1's 20-25% only if it sits in a contrast set: a base plus label-flip twins with their own `call_id`, built by a change to the input text or structure (fact, boundary, premise, clause, definition or world flip, or deletion to NEI). `complement`/`equiv` negation units, `inv` attack units and `equiv` inert units count only toward the negation, attack (~5%) and inert (<= 5%) quotas. | Twins paragraph rewritten: only fact-flip (boundary moves included) and premise-removal contrast sets count toward 20-25%, and they are raised to reach it alone; neg/dneg count only toward the negation quotas; attack stays separate (B13). |
| XF04 | **'Yes = bad outcome' denominator.** All yes/no rows of the family. Rows with no polarity are <= 5% of the family's yes/no rows and count as not-bad. No family-chosen subset denominator. | No change: the per-QT polarity table covers every yes/no question type; any no-polarity row (<= 5%) counts as not-bad. |
| XF05 | **Ties never by position.** A tie between equal quantities is never broken by document, listing or table position. A tie rule names a stated stable key (for example 'the lower <ID number>', fixed-width IDs) or the generator makes no ties. 'Tie broken by position' is a wrong reading in the convention checks. Option labels are exempt; card-stated rule precedence (a decision list, an entry-number order) is not a positional tie-break. | No change: same-time entries take effect in entry-number order (T5, a stated stable key); listing order is a named error (E5, h4). |
| XF06 | **Missing-value markers.** One cross-family marker table, orchestrator-owned in `c_src/common/`, enforced by every parser. Unknown: 'not recorded', 'unknown', JSON/YAML null. Zero or absent: '0', 'none', 'no', false. Banned in every family: '-', 'n/a', 'N/A', 'TBD', '?'. Blank cells stay card-defined (a definition-following contrast) and appear only on rows whose card states the blank's meaning. Unknowns on closed or local cards use word markers or null, never blanks, so a blank on a complete record means none/no wherever it appears. | F3 blanks are card-defined ('no change'; '<default>' in a creation; T8, T9, T42) and appear only where the card states them: full cards and short cards always state the blank sentences their rows need, and no-card rows show no blank (2.1, rule 20; R3-C1). JSON, YAML and key-value entries write a blank as a left-out key, which T8 defines; F3 never writes null, `~`, an empty string or an empty "key:" (rule 20; R3-06). Unknown arises only from open-world gaps, never from a marker; the only XF06 marker F3 writes is "0" for a zero `<quantity>`. No pack value is an XF06 marker (rule 5; R3-07). The parser enforces the shared table; '-', 'n/a', 'N/A', 'TBD' and '?' never appear as values. |
| XF09 | **One pack per card.** Within a family, no two cards share a domain pack (round 1 >= 80 packs for >= 80 cards, round 2 >= 150; F12 and F13 follow their own card counts). Different families may use the same pack. | No change: one pack per card (95 / 180). |
| XF10 | **Shared negation-frame lint (from F5).** No question wraps a negated or negatable proposition in an outer judgement or acceptance predicate ('wrong', 'right', 'reject', 'accept', 'should/would ... be'). Negation is written as truth-frame syntactic negation ('Is it true that ... does not ...?'). **Scope (cross-family fix, 3 Oct):** the shared lint bans only these outer judgement or acceptance predicates; the truth frames 'Is it true that', 'Is it not the case that' and 'Is it false that' over an affirmative claim are allowed, and a family may ban more on its own, as a family-local rule that it does not cite as XF10. | Added to the G3 stem grammar (2.2 negated stem forms). F3 writes every negation in XF10's truth-frame form: L_core negation stands only inside the declarative after 'Is it true that' (N1 'Is it true that ... does not ...?', N2 '... no longer ...', N4 '... it is not the case that ...'); the outer frame 'Is it false that' is a truth frame and stays, wrapping only an affirmative claim (N5; negcount k_all = 0 inside it); a dneg is 'Is it true that it is not the case that ... not ...' (D), never 'is it false that' over a negated claim (R3-C2, R4-01). All three truth frames are allowed by XF10's scope sentence (F3-R4-X3). F3's extra bans are F3-local G3 rules, not cited as XF10 (R4-01 to R4-04): no L_core token in the matrix clause (no 'Doesn't/Isn't/Didn't ...?', no 'Is it not the case that ...?' question, no main-clause 'not' or 'no longer'); 'still' never with 'not'; threshold stems negated only by N4 or N5, with no D; no negation together with 'no fewer than' or 'no more than'. T44 states the answer convention on every card with a negated row. No 'wrong/right', 'reject/accept' or 'should/would ... be' frame is generated. |
| XF11 | **F5 interface and cross-family G12.** F5 stays independent (it re-implements the shallow structures it needs and imports no other family's generator). F1 reserves no seed range for F5; F9 has no export for F5 (X4 = no export). The orchestrator adds a cross-family G12 pass: exact text hash plus MinHash over F5 rows against F1, F2, F3, F4 and F9 rows, and over F13 rows against F1, F3, F6 and F9 rows; each near-duplicate pair is dropped from F5 or F13. | F3 rows are a comparison set in the cross-family G12 pass (against F5 and F13); drops fall on the F5 or F13 row, never on F3. |
| XF16 | **F14 exclusion lint.** 'No row poses <F14 task>.' The orchestrator names F14's skill and structure type before step 5 (generator code) and fills in the lint then. Provisional instance (constraint scheduling): no row asks for a feasible slot or assignment for several items under pairwise constraints. The QC agent's F14 builder checks, by structure type, that no C training row matches F14's structure, and logs the result. | Lint added to the G3 grammar and the QC sidecar check: no F3 row poses <F14 task>. |
| XF17 | **G14 and operator lexicons (orchestrator ruling, recommended default).** Closed operator lexicons (meaning-bearing operator phrases only, each mapped to a SEM row, with no domain words, entity names or templates) are G0 semantics and allowed before the sealed freeze. They pass the 7.2 Claude-seed decontamination and the counts-only sealed template compare before any use. If the orchestrator rules the other way, closed lexicons move to step 4 and only the SEM meaning rows stay in G0. | No change: the 2.2 closed phrase lists stay in G0 as operator semantics and pass 7.2 and the counts-only compare before use. |
