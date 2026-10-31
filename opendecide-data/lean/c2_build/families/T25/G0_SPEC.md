# G0-lite T25: source reliability conflict with tie-abstain

C2_DATA_SPEC 2.1 (T25, 600 selected rows, wave 2, C2 data block "everyday") and 3.17; rules for every family in 3.0 and 4.1. One page: semantics table, card text, samplers, traps, balance, error models, relations, Haiku asks, ambiguity points.
Status: FROZEN v4 (14 Oct 2026). v2 froze the one Haiku ambiguity pass (c2-data-stage-a/amb:T25, 39 points H1-H39, resolved in place and mapped in section 9; record haiku/ambiguity/amb_T25_points.json); v3 adds the pool-review rulings of section 10 (kept as G0_SPEC_v3.md: the pool freeze pins it); v4 is the pilot's fix iteration 1 (section 11: option display plan, card text and placement, 28 cards, wording polarity).
sha256 in plugin.T25.G0_SHA256, pass id in G0_HAIKU_TASK. Every rule on this page is binding; any later change re-freezes it (new sha) and reruns the tests. Code: plugin.py (solver A), solver_b.py (solver B), fixtures.py (test stand-ins), haiku_author.py (Haiku authoring tasks + answer loaders).
Names (H37): S1-S13 are the semantics items of section 1; samplers are always written "sampler S1" ... "sampler S5"; G alone is the top
group (gates always carry a suffix: G2, G4, G-SL ...); "tier" alone is a reliability tier. Outside references: glossary in section 9.

## 1. Semantics table (exact; every rule below is printed on the card)

| # | Item | Semantics |
|---|---|---|
| S1 | Facts | One attribute ATTR (a pack label, section 7) of one organisation ORG, asked about by ASKER, and a bundle of n = 3-5 sources. Listing order: one seeded shuffle per bundle, kept for the row and by all its partners and twins (H7). Source i: id (letters A, B, C ... handed out in listed order, or distinct random codes `S-dd`; an id is a label that stays with its source and never carries meaning: G4 moves sources with their ids; error models use listed positions, never ids; H6), name (a neutral pack noun; it never sets the tier), tier (one of the card's three tier names), date (the source's dated field: a calendar date, no time; H9), origin (`independent`, or copied from another listed source), and the value it states (integer cents, a date, or a count with a section 7 unit) |
| S2 | Tier scheme | Card-level: three distinct names ranked on the card "most reliable first: {RANK_1}; then {RANK_2}; then {RANK_3}" (rank 1 = most reliable). Stand-in schemes: official/trade/community, gold/silver/bronze, primary/secondary/tertiary, high/medium/low, blue/green/grey, alpha/beta/gamma. Only the card's order counts |
| S3 | Copies (bundle invariants) | A copy names exactly one listed independent source (its original), states exactly the original's value and is dated on or after it. Copies of copies never occur. Every bundle has >= 2 independent sources and >= 2 distinct independent values; ids and names are distinct |
| S4 | Resolution | Copies are ignored, whatever their tier or date. T* = the most reliable tier held by an independent source; D* = the most recent dated date among the independent sources of tier T*; the top group G = the independent sources with tier T* and date D*. \|G\| = 1: its value v is the answer (H10). \|G\| >= 2 and every member states v: v. Otherwise: not determinable (key `undetermined`). Dates compare as calendar days among the listed dates only: no as-of date; D* - 1 and D* + 1 cross month and year ends as the calendar does (H34) |
| S5 | No tie-breaks | Tier before date: a less reliable independent source never joins or beats G, even when dated D* or later. Lower tiers, older dates, listing order and majorities never break a disagreement in G |
| S6 | Closed world | CLOSED_WORLD_SENTENCE "The listed sources are complete: no other source, tier or rule applies." The card line "Only the listed sources count ..." (1.1) covers the text around the block (narrative skins of every register), notes, messages, attack lines, the claim line and outside knowledge of the attribute: none is a source. "Correct" means equal to the S4 value from the listed sources, never real-world truth (H8, H11) |
| S7 | ch_value | Key = v (cents int, ISO date, count int) or `undetermined`. k = the number of options shown, counting the abstain option "Not determinable from reliable sources" when it is shown; k = 3 on every ch_value row (no draw; H1). The abstain option is shown on 66% of the rows by a label-blind plan and is the gold on 1 / k of the rows that show it, 22% of all rows (section 11); a shown value gold lists gold + 1 error value + abstain, an abstain gold abstain + 2 error values, a hidden row 3 values. Error values are distinct canonical answers of the section 5 models, never the gold or the abstain key (None, the gold and `undetermined` give no option), picked by a label-blind hash of the row key; their printed texts must also differ (casefold), else the spec is resampled (H2). A spec the plan cannot fill is resampled and a twin that cannot is not proposed; k is never lowered after a failed build (v1 lowered it: abstain gold 0% at k = 2, 39% at k = 4) |
| S8 | ch_source | Asked only when \|G\| = 1 or G disagrees. Key = the id of the single member of G, or `undetermined`. Options "Source {id}" from error models + "No source: not determinable from reliable sources" (when shown). k (counting the abstain option, as S7) = a label-blind draw of 3 or 4 from the row key (n + 1 >= 4 >= k), never lowered; the abstain option is shown on 66% of the k = 3 rows and 88% of the k = 4 rows and is the gold on 1 / k of the rows that show it (22% of all; section 11); a hidden row lists k sources, so a hidden k = 4 row needs n >= 4 and a smaller bundle is resampled |
| S9 | yn_claim (positive) | Asked only on determinable bundles; the state ends with the claim line. yes iff v = CANDIDATE |
| S10 | Complements of S9 | Exact negcount (k_all, k_syn) per wording: yn_claim_wrong (0, 0; an antonym of "correct": wrong, mistaken, incorrect, inaccurate, untrue; lexical, not a negation cue; H14), yn_claim_not (1, 1: one "not" / "n't"), yn_claim_other (1, 0: "other than", whose subject is the value the rules settle on, never a source; H13): yes iff v != CANDIDATE. yn_claim_dneg (2, 2; positive): yes iff v = CANDIDATE, read logically, not(not correct) = correct (H12). ch_value, ch_source, yn_claim: (0, 0) |
| S11 | CANDIDATE | Same kind as the values. yes target: v. no target: the ch_value reading of the first error model, in the order of uhash(T25, "cand", sampler, seed, model name) (label-blind), that is a value != v; none: the spec is resampled (H3). So CANDIDATE is always a value some source states (twins keep this) |
| S12 | Gold | Solver A (`rule_engine`): rules.Or / And / Cmp AST "t outranks s" = rank(t) < rank(s), or the same rank and date(t) > date(s); run by rules.evaluate on every ordered pair of independent sources; G = the sources no one outranks; then S4. Solver B (`sort_group`): own parser; independent sources sorted by rank ascending, then date descending (newest first), grouped by (rank, date) with itertools.groupby; the first group is the head group and decides (H5). G2: A = B on 100% of rows; a disagreement drops the whole relation unit and is a generator bug, fixed in code, never by a label; B never overrides A (H4) |
| S13 | Depth | 2 unstated steps (rank the independent sources by tier then date; check agreement in G); no arithmetic, nothing to print. deep = 5 sources with 2 copies and a top tie: capped at 10% of the family (spec 3.0; measured 2.7%; c2_select drops deep units above it) and reported separately (H36) |

### 1.1 Card (program text; solver B reads it by a full regex match of its own copy, slots as groups)

    How to settle the {ATTR} from the listed sources:
    - Tiers, most reliable first: {RANK_1}; then {RANK_2}; then {RANK_3}.
    - A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.
    - The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source
      states). A less reliable source never wins.
    - Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the {ATTR} not
      determinable from reliable sources.
    - Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.
    The listed sources are complete: no other source, tier or rule applies.

(Each "- " item is one line.) Placement (v4; c2_kit.cards.place_rules, solver B reads both through cards.split_rules): a yes/no row prints the card as
row.card and its instructions are the question wording; a choice row opens its instructions with the card, a blank line, then the question; meta.defs_style
rules_in_card_full / rules_in_instructions_full; no short or no-card style (the answer needs every rule; spec 3.0's short card stays with section 4).
Options: "Not determinable from reliable sources" (ch_value), "No source: not determinable from reliable sources" (ch_source), "Source {id}" (ch_source),
values in the row's value form; the abstain options only on the rows that show them (S7, S8). Answers (spec 2.4, H32): a yes/no row's gold is 1 (yes) or 0
(no); a choice row's gold is one text of its option list, shown by the formats-1 loader. Question texts are admitted Haiku wordings (7).

### 1.2 Source blocks (program text; state = narrative skin + blank line + block [+ blank line + claim] [+ blank line + attack line])

| Layout | Lines (origin wording fixed per layout, H31: list `independent.` / `copied from Source {id}.`; the others `independent` / `copied from {id}`) |
|---|---|
| list | `Sources on the ATTR:` / `- Source ID: NAME; tier TIER; dated DATE; independent. It states the ATTR is VALUE.` |
| table | `Source table for the ATTR:` / `source \| name \| tier \| dated \| origin \| stated value` / `ID \| NAME \| TIER \| DATE \| independent \| VALUE` (origin cell `copied from ID`) |
| excerpt | `Excerpts on the ATTR:` / `[ID] NAME, tier TIER, dated DATE, independent: "The ATTR is VALUE."` |
| keyed | `Source records for the ATTR:` then per source `source ID` / `  name: NAME` / `  tier: TIER` / `  dated: DATE` / `  origin: independent` / `  states: VALUE` |
| claim | `Claim to check: the ATTR is CANDIDATE.` (yes/no rows only) |
| forms | One form per kind in a row, chosen label-blind (H33). Cents: `$` + comma-grouped dollars + two-digit cents (1,250 cents = `$12.50`) or `12.50 USD`; never whole dollars, so distinct values never print alike. Counts: comma-grouped digits (`1,250 days`) or plain digits (`1250 days`), never number words; unit singular for 1, else plural (person / people). Dates: one of `2026-03-05`, `5 March 2026`, `March 5, 2026`, `5 Mar 2026`, or those with a weekday; every date of a row (dated fields, date values, CANDIDATE) alike. Keys: ISO dates, integer cents, integer counts |

## 2. Samplers (>= 4 training shapes + held-out sampler S5)

| Sampler | Shape | Layout | n |
|---|---|---|---|
| S1 | forward: G planned first, rivals and copies around it | list | 3-5 |
| S2 | label-first near miss: rival gaps concentrated on 0 / 1 day (same-tier rival one day older, less reliable rival one day newer or same day, copies at D* or D* + 1) | list | 4-5 |
| S3 | source table first | table | 4-5 |
| S4 | narrative skin (registers email, chat, transcript, memo, ticket, faq; picked by row key) over program-written excerpts; no Haiku excerpt frames in v1 (H30) | excerpt | 3-4 |
| S5 | held out (mixdev only): keyed records, held-out skins and registers (wiki_talk, audit_note) | keyed | 3-5 |

Cards: (sampler, card 0-6) fix the attribute pack, the tier scheme and the id style: 28 training cards + 7 S5 cards (35 pool packs, one per card). Once the Haiku pools
are admitted, each card gets its own pack (>= 25 packs, spec 3.0); until then the stand-ins in plugin.PACKS. Allocation (H22): training seeds
are split equally over samplers S1-S4; about 900 rows (1.5 x 600, partners and twins included) are generated; the card is a uniform draw per
seed (about 21 selected rows per training card, <= 64); c2_select keeps 600 by whole units. Selection and the mixer only drop whole units,
never add or relabel; where they and this page's generator shares differ, they win.
Construction: G (tier T*, date D*) first: clear = \|G\| = 1; tie = \|G\| >= 2 (2 members; 3 with probability 0.15 when >= 4 sources are
independent), all members planned at (T*, D*); tie_agree / tie_disagree = one / several values in G (H19). Rivals: same tier and older, less
reliable and newer, less reliable and same-day-or-older; copies: outrank (would win if counted), false_tie (tier T*, date D*, another value),
of_winner, inert. Listing order is the S1 seeded shuffle. A construction-only reading (`_top_c`, a plain max over the plan) tags traps and
predicts twins; a guard refuses any spec where it and solver A disagree.

## 3. Traps (share of base specs; overlapping; tags in `meta.edge`; measured on 2,000 specs in the tests)

| Tag | Target | Meaning |
|---|---|---|
| `newest_loses` | >= 30% | t25_newest_first (date before tier) gives an answer, a value or `undetermined`, other than gold; no single answer: not counted (H35) |
| `copy_trap` | >= 25% | counting copies changes the answer (t25_count_copies) |
| `false_tie` | >= 3% | counting copies turns a determinable bundle into a disagreeing tie |
| `tie_agree` / `tie_disagree` | ~13% / ~12% | ties ~25% of bundles, about half agreeing (spec 3.17) |
| `majority_wrong` | >= 15% | a unique most-stated value exists (copies counted) and is not the answer; no unique majority: not counted (H35) |
| `same_day_tiers` | >= 10% | a less reliable independent source is dated D* |
| `near_miss` | >= 20% | a same-tier rival at D* - 1, a less reliable rival at D* + 1, or a copy at D* / D* + 1 |
| `top_t1` / `top_t2` / `top_t3` | 50 / 35 / 15% | the tier of G (the top tier is not always rank 1) |
| `date_separates` | report | same-tier independent sources disagree but dates separate them (reading the tier alone over-abstains: t25_tier_only) |
| `clear`, `first_listed_wrong`, `deep` | report | as named (deep also capped, S13) |

## 4. Balance targets (generator level; c2_select tightens to the spec 3.0 cells and wins on conflict, H22)

- Base forms: ch_value 40%, ch_source 18%, yn_claim 38%, yn_claim_dneg 4%; with partners and twins yes/no is 45-55%.
- Seeds 2k and 2k + 1 share the question form only; each draws its own card, scenario and bundle; their yes/no targets are opposite, so gold
  yes is 50% exact per base form over seed pairs (H21).
- Scenarios: yes/no clear 82 / tie_agree 18 (a hash draw); a choice row's scenario follows its display plan (section 11): an abstain gold is a disagreeing tie, any other gold
  a determinable bundle (ch_value clear 62 : tie_agree 16, ch_source clear). `undetermined` is gold on 22% of choice rows (spec 3.17: 15-25%) and on 1 / k of the rows
  that show it, so it is wrong on 67% (k = 3) / 75% (k = 4) of them (bar >= 50%), overall and in every (k, shown) cell.
- Gold option position uniform per option count (kit), balanced along the seeds (section 11). The listed position of G is a seeded shuffle (uniform).
- Syntactic negation (k_syn >= 1) on >= 10% of yes/no rows; double negation (k_syn >= 2: yn_claim_dneg) on >= 2%.
- yes = bad outcome: no T25 predicate is a harm (yes_is_bad unset). Per-card yes rates are 50% by seed pairs; the spec 3.0 per-card
  20-80% draw, inverted / few-shot / short cards and masked labels are left to v2 or c2_select.
- Length (H20): tokens of the trainer's tokenizer (C1's Qwen3.5 tokenizer, as mix_c2 counts them) over state + options + the instructions
  counted twice and row.card once (yes/no rows hold the card in row.card, so it counts once there and twice on choice rows; 1.1): family mean <= 800, every row <= 2,000. Generation pre-checks
  with rows.approx_tokens (3 characters per token, conservative).

## 5. Error models (every wrong option; family names carry the prefix `t25_`)

Seven are solver A with one rule swapped (H17): `t25_newest_first` (date before tier), `t25_count_copies` (copies counted as independent),
`t25_tier_reversed` (the card's ranking read backwards), `t25_oldest_in_tier` (the oldest date wins inside the top tier), `t25_tier_only`
(dates ignored: every independent source of the top tier is in G), `t25_tie_first_listed` / `t25_tie_last_listed` (a disagreeing G broken by
listing order: the over-answer). Three are standalone shortcut readings: `t25_majority` (the value most sources state, copies counted; no
unique majority: None), `t25_first_listed` (the first listed source, copy or not), `t25_newest_any` (the most recent source of any tier or
origin; several with different values: None). Each answers ch_value / ch_source (None when it gives no single answer). Over-abstain readings
answer `undetermined` only when their group disagrees: `t25_tier_only` when the top-tier independent sources (all dates) disagree, else
their common value (H18); `t25_count_copies` on a false tie. Abstain is never an error option: it is shown by the display plan of S7 / S8, always when it is the gold.

## 6. Relations (spec 4.1; G-TW 100%)

- Complement on 60% of yes/no base rows; the partner form is drawn among that 60% (H16): yn_claim -> wrong 40% / other 20% / not 40% (24 /
  12 / 24% of yn_claim bases); yn_claim_dneg -> not. gold(Q) = 1 - gold(not-Q) under the closed-world sentence.
- Minimal-edit twin (proposed on 42% of bases): one input slot moves and the answer is predicted from the edit:
  rival_newer (a same-tier rival dated D* + 1: G' = {rival}), rival_tie (dated D*: G' = G + rival), rival_promote (a less reliable rival
  dated any day after D* raised to tier T*: G' = {rival}) / rival_tie_promote (dated D*: G' = G + rival), member_back / member_forward /
  member_demote (a member of a tie moved to D* - 1 / D* + 1 / the tier ranked next below T*; never offered when T* is rank 3; H24),
  member_value (a member of G states another value), claim (yes/no only, last resort: CANDIDATE := another independent bundle value, the
  first in sorted order that flips the answer). The answer of G' is read from the edited slots (never from solver A). Kept only when the
  gold key changes (`undetermined` -> `undetermined` is no flip), S3 still holds, and the twin stays askable: determinable on yes/no;
  \|G'\| = 1 or a disagreeing G' on ch_source (an agreeing tie is never asked; H23). Same skin, wording and forms.
- equiv (12% of bases: another skin and register; half also another layout; same facts), inv (5%: one inert attack line; gold kept by S6).
- G4 (checked, never emitted): rename the asker; rename the organisation; shift every source date by 35 days; swap the tier scheme (same
  order); reverse the listing order (ids move with their sources); drop a copy; rename the deciding source (ch_source: the new id; others: same).

## 7. What Haiku writes (after A38: OHS-4 frozen) and the slots it must keep (tasks: haiku/author/, haiku_author.py)

- Narrative skins, Mode T (registers memo, email, chat, ticket, json, yaml, faq, transcript; held out wiki_talk, audit_note; equal pools
  per register, so each register is <= 15% of rows). Slots kept verbatim, each exactly once per skin: {ASKER} (name), {ORG} (name), {ATTR}
  (name); an attack line is a separate template, so a row with one shows {ASKER} twice (H25). Never (H26): a digit or number word, a date, an
  amount, a tier-scheme word (every stand-in or Haiku scheme name), a source fact (a source's name, id, count, tier, date, origin or stated
  value; the plain words "the sources" pointing at the block may appear), a copy, reliability or recency word, a verdict, a claim, a rule, a
  question, or a program block head. JSON / YAML keys follow the same bans.
- Mode F (H29): the narrative of a row is picked label-blind from the row key among the admitted skins of its register; Mode F skins (free text
  from a facts-only brief holding the three values verbatim; G-SL fact-lock lint_freeform, G3-H on asker, organisation and attribute) are
  <= 20% of each register's admitted pool, so <= 25% of rows (Mode T >= 75%), checked per family at the pilot.
- Question wordings (>= 30 admitted, >= 4 per form, each <= 2% of the family): lexicon kind `question`, sem q.t25.<qform>; slot {ATTR} once
  or none; every wording names the stated rules or the listed sources (H11) and never uses "above", "below" or "here"; yes/no wordings name
  "the claim to check". Exact negcount per form (S10); a yes/no wording reads with its form's polarity (c2_kit.polarity P1-P3, v4); admitted 2/2 (H15). yn_claim_dneg: both negations are "not" (k_syn = k_all = 2), no
  contracted or tag-question opener; a wording any extractor reads rhetorically is rejected for good; with < 2 admitted, a re-authored batch
  runs before the pilot and no dneg row exists without one (H12).
- Packs (program expands them): >= 30 attribute packs (label, value kind, count unit from the closed list kilogram, day, week, month, year,
  hour, minute, night, person (people), seat, item, ticket; 6-8 pool values, dates drawn by the program), >= 40 neutral source nouns, >= 8
  tier schemes (three one-word names, most reliable first), organisations, askers. LABEL_WORDS and every tier-scheme word are banned in every
  Haiku- or pack-written string except question wordings: skins, Mode F, attack lines, attribute labels, source nouns, organisations, askers
  (H27). Attack lines (inert, H28): one line, {ASKER} exactly once; no digit, date, amount, id, tier-scheme word, source name, verdict word or
  "copy", "copied", "independent", "tier", "source"; they may press a shortcut in general words (recency, repetition, urgency); S6 keeps gold.
  v1 keeps the card, the source blocks and the excerpt sentences program-written. Stand-in packs (plugin.PACKS):

| Pack | ATTR | Value kind (unit: singular / plural) |
|---|---|---|
| filing_fee / deposit / membership / withdrawal | late filing fee / booking deposit / monthly membership price / daily withdrawal limit | cents |
| deadline / opening / entries | application deadline / market opening date / closing date for entries | date |
| baggage / notice / group / age / pickup | checked bag allowance / cancellation notice period / maximum group size / minimum age for the course / parcel pickup window | count (kilogram / kilograms, day / days, person / people, year / years, hour / hours) |

G-SL exceptions: none. NAME_ALLOW: none. LABEL_WORDS (never in a skin): VERDICT_WORDS (plugin: determinable, undetermined, indeterminable,
undeterminable, decides, decisive, wins, winner, outranks, overrides, ignore, correct, wrong, mistaken, reliable, unreliable, trustworthy,
authoritative) plus the decisive-fact words copy / copied / independent / tier / official / newest / latest / recent (record blocks state
facts with copied, independent and tier; they never carry a verdict word). Program text (card, blocks, options) is exempt.

## 8. Ambiguity points written before the Haiku pass (Claude; all settled in the text above)

1 T* over independent sources only (S4). 2 a copy never decides; a copy of the decider changes nothing (S3, S4). 3 an agreeing tie's value stands; ch_source is never asked then (S4, S8). 4 same date, different tiers: tier decides (S5). 5 a lower tier agreeing with one member of a disagreeing G: still `undetermined` (S5). 6 majorities never outweigh tier then
date (S5). 7 "most recent" = the dated field (S1, card). 8 only the card's ranking counts (S2). 9 names never set tiers (S1). 10 claim, notes, attack lines are not sources (S6). 11 same-day copies, codes vs letters, a copy listed before its original (S1, S3). 12 yn_claim_other (S10, H13). 13 yn_claim_dneg (S10, section 7, H12).

## 9. Resolution of the Haiku ambiguity pass (c2-data-stage-a/amb:T25, 13 Oct 2026; H<n> = points[n-1] of the record)

H1 k: S7, S8 (k counts the abstain option; ch_value k = 3 fixed). H2 distinct values: S7. H3 no-target CANDIDATE: S11. H4 A/B disagreement and "full match": S12, 1.1. H5 sort direction: S12. H6 ids: S1. H7 listing order: S1. H8 narrative: card line, S6. H9 dated field: card, S1. H10 lone winner: card, S4. H11 outside knowledge: card, S6, section 7 wordings.
H12 dneg: S10, section 7. H13 "other than": S10. H14 antonym: S10. H15 "admitted 2/2" = two independent blind Haiku G-LEX extractions both pick the form's meaning (one other pick rejects it for good); k_syn / k_all as in the glossary. H16 complement denominators: section 6. H17-H18 error models: section 5. H19 tie / clear: section 2. H20 length: section 4.
H21 seed pairs: section 4. H22 allocation and precedence: sections 2, 4. H23 twin keep rules: section 6. H24 member_demote, rival_promote: section 6. H25 slot counts: section 7. H26 skin bans: section 7. H27 LABEL_WORDS scope: section 7. H28 inert: section 7. H29 Mode T / F: section 7. H30 S4 skins: section 2. H31 origin wording: 1.2. H32 answers and
question texts: 1.1, section 7. H33 display forms: 1.2. H34 dates: S4. H35 trap counting: section 3. H36 deep cap: S13. H37 names: header. H38 status: header (all binding; section 8 settled). H39 outside references: this glossary, binding as written.
Code changed for this freeze: card lines (dated field, lone winner, only listed sources count) in plugin.CARD and solver_b._CARD; sampler S4 registers widened to six (the 15% register cap); the count units of section 7 in solver_b.UNITS; G0_SHA256 / G0_HAIKU_TASK. Golds, error models, shares and solvers' logic are unchanged.
Glossary (binding): G2 solver B = solver A on 100% of rows; G3 parse of the rendered row = canonical facts; G4 metamorphic checks (never emitted); G-SL slot lint and fact-lock (kit gsl: CORE + EXTENDED words + LABEL_WORDS; Mode F lint_freeform); G-TW twins and complements (kit relations); G3-H Haiku re-extraction of Mode F facts (>= 98% per template); G-LEX
lexicon admission (kit lexicon); G5-H two blind Haiku reads + Claude adjudication; k_syn / k_all = c_src/common/negcount.py v1.1 (k_syn: the L_core words not, n't, no, none, nobody, nothing, nowhere, never, neither, nor; k_all: every F5 negation surface incl. implicit cues such as "other than", "fail to", "false"); F5 = the round-1 negation family whose
lexicon negcount uses; T26 = the sibling provenance family (same dneg reading); Mode T = slot template, Mode F = free form (spec 3.0); partners = the complement / equiv / inv rows of a relation unit (<= 3 rows); mixdev = the held-out dev mix (sampler S5 rows, held-out skins and registers; never trained); A38 = the PREREG ruling freezing OHS-4 (no C2 data
before it); c2_select = the C2 crowd and selection step (drops whole units only); _top_c, rules.evaluate, uhash = plugin.py / kit functions named above.

## 10. Pool-review rulings (v3, 13 Oct 2026: the stage-A review of the stage-6 pool freeze, B1-B3; tasks and records written by haiku/redo2/build_redo2.py)
B1 noun cross-lint (H26, H27). Every skin, Mode F document and attack line is linted against every admitted source noun and every tier word (stand-in and admitted Haiku schemes), as haiku_author.check_skin / check_freeform / check_attack do when given nouns= and tier_words= (the stage-6 freeze passed neither). That lint finds one conflict: the noun "memo" is the memo register's own word (36 of 37 memo skins, 9 of 12 memo Mode F documents); no tier word, other noun (stand-ins included) or attack line conflicts. A noun that an admitted narrative piece names leaves the noun pool, never the register or its pieces: "memo" is quarantined (source nouns 94 -> 93, >= 40), so no narrative names a source and the 8 training registers stay; the lint with the ruled pool rejects nothing.
B2 order-free lexicon (G-LEX). No admitted form's pattern may fully read another admitted form's rendering (kit sample fills and every admitted attribute label in {ATTR}): the kit scan then credits whichever form was registered first, so a unit test passes or fails with the build order. Of such a pair the form whose pattern reads the other's text (the more general one) is quarantined (both if mutual): q.t25.yn_claim#3fab6dc5 ("... the same value for the {ATTR} the listed sources settle on?") reads q.t25.yn_claim#adb8f647 ("... for the {ATTR} that the listed sources settle on?") with {ATTR} = "<label> that", so #3fab6dc5 goes (yn_claim 35 -> 34, forms 139 -> 138) and #adb8f647 stays. The rest passes every unit test in every build order (form id, reversed, stage 6, 20 seeded shuffles) and reads every fill back to its own form; every re-freeze reruns this check.
B3 pool-stage G3-H. Each frozen Mode F document gets one blind G3-H read before any row (kind extract_g3h; fields asker, org, attr with the names and kinds of plugin.extract_fields; the describes ask for the name alone, without a title, a leading article or a possessive; the expected values are the document's brief facts, orchestrator side). The template is the document (a kit skin): with one read per document the >= 98% bar admits it only when g3h.compare matches all three fields exactly, and a mismatch quarantines it for good (no re-read). Then the section 7 cap: each register keeps at most floor(its Mode T skins / 4) admitted documents (Mode F <= 20% of its admitted pool), lowest uhash(T25, "mode_f_cap", document id) first (label-blind); if all 84 pass, 23 are cut (memo 3, email 3, chat 2, ticket 3, faq 4, transcript 4, wiki_talk 2, audit_note 2). With no admitted document T25 ships Mode T only. Row-level G3-H at the pilot and full generation is unchanged. v3 changes no gold, solver, sampler, card, error model, share, wording meaning or gate bar (code: G0_SHA256 only); the pool re-freeze applies B1-B3 and logs each drop in QUARANTINE.json.

## 11. Pilot fix iteration 1 (v4, 14 Oct 2026; spec 6.4 step 6, generator only: no gold, solver, error model, bundle rule or gate bar changes)
F1 display plan (S7, S8; c2_kit.choiceplan). Pilot: the abstain option was on every choice row and always the longest, gold on 22% of them against 1 / k = 33%, so "never take the longest" beat chance (G10 -7.9 pp, G6 choice, G7). Now k, the abstain display, the abstain gold and the gold position are drawn from the row key BEFORE any structure (label-blind) and balanced along the seeds (blocks of 1,024 per sampler and form: every k consecutive rows of a (k, shown) cell hold one abstain gold, every k consecutive rows of a k every position); shown on 66% (k = 3) / 88% (k = 4) of the rows, gold on 1 / k of the shown rows, never gold on a hidden row; a twin whose new gold is the abstain key shows it (plan.for_gold). The sampler redraws STRUCTURE under the fixed plan, never the plan, never a label.
F2 length: the 1.1 card is the shorter text and yes/no rules sit in row.card (printed once): mean 855 -> about 700 rendered tokens (bar 800). F3: 7 cards per sampler. Polarity (T35 G5-H): plugin.NEGATIVE_PREDICATES; haiku_author.check_wording and T25.ctx_for screen every yes/no wording (the frozen pool loses none); a failing wording is quarantined, never a row relabelled. G5-H template quarantine of pilot 0 (spec 6.3 rule, one reader error on each, adjudicated gold_ok): skin T25-SK-yaml.021 and wording q.t25.yn_claim_dneg#90841882 leave the pool in T25.ctx_for.
The pool freeze (freeze_v2.py, pools_v2/) stays bound to G0_SPEC_v3.md: v4 changes no pool piece. Not applied: skin / wording / register caps (generation driver or c2_select, G11); short or no-card styles (4).
