# G0-lite T23: governing version under transition clauses

C2_DATA_SPEC 2.1 (T23, 800 selected rows, wave 1, everyday tier) and 3.11; rules for every family in 3.0 and 4.1. Precedence: this page governs T23's
semantics, card and record text, samplers, traps and T23 targets; spec 3.0 / 4.1 govern every cross-family rule and bar (cells, overlay minimums,
gates). T23 targets here are generator-level; c2_select may only drop rows to meet the spec 3.0 cells, never change a gold, a text or a rule. Status:
v4 (14 Oct, Stage B pilot fix iteration 1 of 2, section 11): v2 froze the Haiku ambiguity pass c2-data-stage-a/amb:T23 (48 points), v3 added the pool-review rulings of section 10 (the pools_v2 freeze; the v3 text is G0_SPEC_v3.md); v4 changes the card text and placement (1.1), the yn_version complement (R16, 6), the author-mode and register draw (7) and the wording screen (7, 11). Sha256 in plugin.py G0_SHA256. The text governs; plugin.py (solver A),
solver_b.py (solver B) and the tests implement it and change to match it. Any later change re-freezes this file; rows generated under an older sha are
discarded and regenerated, never kept. Notation: R1-R21 are semantic items (section 1); S1-S5 are samplers (section 2). Versions V_1..V_n oldest
first; S_k is the start of V_k and S_(k+1) the start of the next version (parentheses: never "S_k plus a day"); END_k is a printed end; P, EV, F, DEC
are the purchase-, event-, filing- and decision-role dates; D0 is the default version, G the governing version, K the option count. "+ 1 day" is calendar arithmetic; every date is a calendar date (no time).

## 1. Semantics table (exact; every rule below is printed on the card or in the record)

| # | Item | Semantics |
|---|---|---|
| R1 | Facts | One rule document (DOC) of one domain pack (section 7), in n = 2-4 versions, and one case. All values are typed slots; the pack fixes DOC, TERM_LABEL, QTY_LABEL, the four date labels and the term kind (day count, integer cents, device count) |
| R2 | Versions | Version k: id V_k (distinct; one id format per row, R14), start S_k (strictly increasing; generator gap S_(k+1) - S_k in [45, 320] days, both ends included; S_1 in [2023-01-02, 2024-12-01]), term T_k (a value of the pack's pool, section 7; distinct across versions) and a "replaces" pointer to V_(k-1) (V_1 replaces none). Printed oldest first (list, table) or newest first (log) |
| R3 | Windows (card) | `incl`: in force from S_k through END_k = S_(k+1) - 1 day, both included. `excl`: END_k = S_(k+1) is printed; in force from S_k through S_(k+1) - 1 day, END_k itself excluded. `chain` (log only, no end printed): from S_k until S_(k+1), on which V_(k+1) is in force. V_n is open-ended. Windows tile: exactly one version is in force on every date on or after S_1. No case date lies before S_1 (never generated; solver B refuses such a row) |
| R4 | Case | Four dates P <= EV <= F <= DEC, on or after S_1 and at most 420 days after S_n. Anchor (one per card): the purchase, event or filing date, never DEC. D0 = the version in force on the anchor date; "would govern" in a clause always means D0 (card) |
| R5 | Clauses | At most one clause per row (card), carried by version c and naming it, so its place is layout only (list, log: indented under V_c; table: after the table). Types: grandfather (keep-old, role P), prospective (keep-old, role EV), retroactive, sunset. A clause applies iff its own "if ... would govern" test holds (R6-R8), whatever version it is printed with; foreign = printed but not applying |
| R6 | keep-old (c >= 2) | "if V_c would govern a case whose <role date> is before S_c, the version in force on that <role date> governs it instead". Applies iff D0 = c; fires iff also role date < S_c (equal is not before); target = the version in force on the role date (any older version, possibly two back) |
| R7 | retroactive (c >= 2) | "if a version older than V_c would govern a case whose decision date is on or after S_c, V_c governs it instead". Applies iff S_D0 < S_c (any older version, not only V_(c-1); never a newer one); fires iff also DEC >= S_c; target = c, also when a version newer than V_c is in force on DEC (card) |
| R8 | sunset (c <= n - 1) | SUN in [S_(c+1), S_(c+2) - 1 day], both included ([S_(c+1), S_(c+1) + 400 days] when c + 1 = n). "if V_c would govern a case whose decision date is after SUN, V_(c+1) governs it instead". Applies iff D0 = c; fires iff also DEC > SUN (DEC = SUN does not fire); target = c + 1, also when a newer version is in force on DEC |
| R9 | Governing version | G = the target when the clause fires, else D0. A clause is applied once, after the default (never chained) |
| R10 | Date words | "before" / "after" exclude the date itself; "on or before" / "on or after" include it. "Older" = earlier start date |
| R11 | Outcome | Within the TERM_LABEL iff Q <= T_G (equality is within), outside it otherwise. Q is printed: an input (integer cents or a whole count, never fractional) or a day count = the later minus the earlier date of the pack's pair in calendar days (same day = 0); the reader never recounts. Day counts stay <= 3 x the maximum of the pack's term pool |
| R12 | Claim | Case-record line "claim to check: the TERM_LABEL for this case is X" (yes/no claim forms only). Supported iff X = T_G, contradicted otherwise (a value equal to another version's term is contradicted) |
| R13 | Closed world | CLOSED_WORLD_SENTENCE "Only the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists." The narrative skin paragraph and the attack line (one pasted line after the case record, inv rows only) are inert: they change no fact and no answer |
| R14 | ch_version | Key = V_G's id. K = 2 on every row: the gold plus one distinct wrong version from the error models (section 5). One always exists (n >= 2: newest_version and t23_original_version cannot both return G), so K is never lowered and nothing is filled in; a row whose options could not be built would be dropped (tested: never). ch_version ids are random document codes, one format per row (PFX-123, PFX12 or PFX-12B), so their sort order is random against the version order; other forms use v1.., rev-A.. or PFX-123 ids, one format per row |
| R15 | ch_term | Key = T_G (int). Options as R14; the wrong option shows its version's term (`$1,250.00` for cents; `30 days`, `1 device` for counts) |
| R16 | yn_version | yes iff CANDIDATE (a version id) = V_G. Complement yn_version_not (syntactic): yes iff CANDIDATE != V_G. yn_version_other ("a version other than", implicit: yes iff CANDIDATE != V_G) stays a defined, tested form but is never proposed as a partner (v4, section 11) |
| R17 | yn_claim | yes iff CLAIM = T_G. Complements yn_claim_contra ("contradict", antonym), yn_claim_not (syntactic) |
| R18 | yn_outcome | yes iff Q <= T_G. Complements yn_outcome_out ("outside", antonym), yn_outcome_not (syntactic) |
| R19 | No abstain | Every case has exactly one D0 (R3, R4) and one G (R9), so no option abstains |
| R20 | Depth | version lookup (1) + the clause's applies-test when it applies (1, fired or not; a foreign clause adds 0) + the Q test on yn_outcome forms (1). Deep = 3, <= 10%. Day counts are printed |
| R21 | Gold | Solver A (`rule_engine`): one kit rule AST per version window (rules.Cmp / And over date slots: S_k <= d, d <= or < END_k; chain: d < S_(k+1)) and per clause condition, run by rules.evaluate, then R9; the answer by a Cmp on ids / terms / Q. Solver B (`sql_sqlite`): its own parser loads versions and case dates into in-memory sqlite; a SQL window filter on julianday (END_k + 1 under incl; chain: the start of the version whose "replaces" names it, by a self-join) gives D0; the clause is a separately coded rule; per version the flags default (= D0), released (the clause fires and moves D0 away) and pulled (the clause fires and this version is its target); governs = (default and not released) or pulled, exactly one must hold. G2 = 100%: a mismatch or a solver-B refusal drops the whole relation unit (never "prefer A", never relabelled); a systematic one is a generator bug. A third construction table (start dates, case dates, the clause and SUN, terms and Q; windows from the starts only, never the printed ends or a rule AST) steers the samplers and predicts twins; it never sets gold |

### 1.1 Card text (program-written; solver B keeps its own copy and full-matches it)

v4: a card holds the rules its row needs. Yes/no rows carry it in `row.card` (the served prompt prints it once, under "Definitions:"; the instructions are the question); choice rows carry it at the head of the instructions, then a blank line and the question (printed twice). "Shown when" reads VISIBLE inputs only (clause printed in the record; question form), never the gold. {ANCHOR} is the anchor role's date label slot; {WINDOW} one of three. Card = the lines below in this order, one per line, joined by "\n"; bullets are "- ".

| Line | Shown when | Text |
|---|---|---|
| title | always | Finding the version of the {DOC} that governs a case: |
| default | no clause printed | - The governing version is the version in force on the case's {ANCHOR}. |
| default_clause | a clause is printed | - Default: the version in force on the case's {ANCHOR}; "would govern" in a clause means this default. |
| window | always | - {WINDOW} |
| clause | a clause is printed | - At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default. |
| dates | a clause is printed | - An older version has an earlier start date. "Before" and "after" exclude the date itself; "on or before" and "on or after" include it. |
| within | outcome question (yn_outcome, _out, _not) | - The case is within the {TERM_LABEL} when its {QTY_LABEL} is at most the governing version's value, and outside it otherwise. |
| claim | claim question (yn_claim, _contra, _not) | - A claim about the {TERM_LABEL} is supported when it states the governing version's value, and contradicted otherwise. |
| closed | always | Only the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists. |

{WINDOW}: incl "A version is in force from its start date through its end date, both dates included; an open-ended version stays in force." excl "A
version is in force from its start date through the day before its end date; an open-ended version stays in force." chain "A version is in force from
its start date until the version that replaces it takes effect, and on that start date the new version is in force." (Each card line is one line.)

### 1.2 Record blocks (program-written; state = narrative skin + blank line + versions + blank line + case [+ blank line + attack line])

| Block | Lines |
|---|---|
| list | `Versions of the DOC (end dates included):` (incl) or `(end dates excluded):` (excl) / one line per version, oldest first: `- ID: REP; WIN; TERM_LABEL: T.` with REP = `first version` (V_1) or `replaces PREV`, WIN = `in force from S to END` (k < n) or `in force from S, open-ended` (V_n); the clause line follows its version, indented two spaces |
| table | `Version table of the DOC (end dates included):` or `(end dates excluded):` / `version \| replaces \| in force from \| in force to \| TERM_LABEL` / `ID \| first version or PREV \| S \| END or open-ended \| T`; the clause line follows the table |
| log | `Change log of the DOC, newest entry first:` / `S \| ID takes effect, replacing PREV \| TERM_LABEL: T` ... `S \| ID takes effect as the first version \| TERM_LABEL: T`; no end dates; the clause line indented under its version |
| clause | keep-old `Transition clause of ID: if ID would govern a case whose LABEL is before S, the version in force on that LABEL governs it instead.` retro `Transition clause of ID: if a version older than ID would govern a case whose DECISION_LABEL is on or after S, ID governs it instead.` sunset `Sunset clause of ID: if ID would govern a case whose DECISION_LABEL is after SUN, NEXT governs it instead.` |
| case | `Case CASE_ID:` / `- PURCHASE_LABEL: P` / `- EVENT_LABEL: EV` / `- FILING_LABEL: F` / `- DECISION_LABEL: DEC` / `- QTY_LABEL: Q` / [`- claim to check: the TERM_LABEL for this case is X`] / `End of case record.` |
| values | One form per kind per row, label-blind. Dates: `2025-04-03`, `3 April 2025`, `April 3, 2025`, `3 Apr 2025`, `Thursday, 3 April 2025` or `Thursday, April 3, 2025` (never a numeric 03/04 form). Cents (integer cents): `$1,250.00` or `1,250.00 USD`, always two decimals. Counts: digits plus unit, `1,234 days` or `1234 days` ("plain" = no thousands separator), singular `1 day` / `1 device`, never words. Options: `$` cents / digits + unit |

## 2. Samplers (>= 4 training shapes + held-out S5)

| Sampler | Shape | Style | Notes |
|---|---|---|---|
| S1 | forward: dates drawn in intervals the scenario allows | list | n 2-4; edge pin on 25% |
| S2 | label-first near-miss: the deciding date sits on its boundary (S_k - 1 day / S_k; DEC = SUN / SUN + 1; Q = T_G / T_G + 1, a day count by moving the later date of its pair onto a pool term) | list | n 2-3; edge pin on 90% |
| S3 | config / table first | table | n 3-4 |
| S4 | narrative: email, chat and transcript skins over a pasted change log | log | n 2-3 |
| S5 | held out (mixdev only): held-out skins and registers (notice, export) | table (even card) / log | n 2-4; never a training row |

Cards: (sampler, card 0-5) fix the domain pack, the anchor and the window rule (list / table: even card incl, odd excl; log: chain): 24 training
cards, about 50 rows per card at 1.5x generation (selected median about 33). Edge pin = the sampler pins the deciding date onto its boundary;
label-first = the target answer is drawn before the facts; mixdev = the dev mix of S5 rows and held-out skins, wordings and registers (never trained).

## 3. Traps (tags in `meta.edge`; overlapping; measured on 2,000 specs = seeds 0-399 x S1-S5)

| Tag | Target | Measured | Definition and construction |
|---|---|---|---|
| `newest_wrong` | floor 30% | 50.6% | G != V_n, on the gold (D0 draw weights: newest 0.6, the older ones share 0.4) |
| `foreign_clause` | floor 30% | 30.0% | a clause is printed and its own applies-test fails (scenario foreign 30%): keep-old / sunset printed on c != D0; retroactive printed on c with D0 = V_c or newer (a retro clause on a version newer than D0 applies, so it is never foreign) |
| `clause_decisive` | floor 25% | 31.9% | the clause fires and moves the case (scenario decisive 32%) |
| `boundary` | floor 20% | 43.0% | the anchor at S_k - 1 day or S_k (k >= 2), or, for an applying clause, its date: keep-old role date at S_c - 1 day / S_c; retro DEC at S_c - 1 day / S_c; sunset DEC at SUN / SUN + 1 day |
| `plain` | ceiling 30% | 25.5% | no clause (scenario none 25%) |
| report only | - | see note | `clause_tested` (applies, does not fire) 12.6%; `term_edge` (outcome forms with Q = T_G or T_G + 1 unit: day, cent, device) 5.7%; `future_version` (S_n > DEC) 27.9%; `grandfather` / `prospective` / `retroactive` / `sunset` 20.7 / 12.4 / 24.2 / 17.1% |

Floors are tested at >= 0.9 x target; higher measured shares are accepted. Scenarios (none 25%, decisive 32%, tested 13%, foreign 30%) and clause types (grandfather 30, prospective 25, retroactive 25, sunset 20) are drawn per row; types that cannot realise the row's scenario on its card's anchor
are dropped and the rest renormalised (a decisive keep-old needs its role date before the anchor: grandfather anchor EV or F, prospective F).

## 4. Balance targets (generator level; c2_select tightens to the spec 3.0 cells)
- Base question forms: ch_version 32%, ch_term 24%, yn_version 15%, yn_claim 15%, yn_outcome 14%.
- Gold yes 50% per base yes/no form on base rows: seeds 2k and 2k + 1 share the form and get opposite targets (exact over pairs). Complement partners
  and twins flip their base; the yes rate and the yes/no share (45-55% each) are measured on all emitted rows (base + partners + twins + equiv + inv).
- Gold position uniform per K (kit gold_position, row key only); options are shown in that seeded order, never sorted. Sort rank (ids by string order,
  terms by value): the gold is the higher of the two on 50% +- 4 SE (tested).
- yes = bad (kit QuestionForm.yes_is_bad): unset; no T23 predicate is a harm. Deep rows <= 10%. No abstain (R19).
- Length (Qwen3.5-4B tokenizer, the trained model's): state + the question twice + the rules (once on a yes/no row, twice on a choice row: v4, 1.1) +
  options; family mean <= 800 (v3 pilot 963; v4 pilot in PILOT_REPORT), every row <= 2,000.
- Known content-free cue (report for G6 / G7; gold unaffected): the later-starting of the two ch options is gold on 59.9% of ch rows, and "the candidate
  is not V_1" means yes on 61.9% of yn_version / yn_claim rows (6,000 training specs). A fix (version-position cells at selection) re-freezes this file.

## 5. Error models (every wrong option; spec 3.0)
Each is solver A with one rule swapped and returns a version (shown as its id or term). A model whose answer equals G is unused for that row (the kit
drops an option equal to the gold; never a CANDIDATE / CLAIM); None = no reading (an anchor-date model on the anchor itself; no unique version). Kit
catalogue names (shared, so no prefix): `newest_version` (V_n); `drop_inclusive_endpoint` (incl lookups on d + 1 day, so an end date falls to the
replacing version; retro "on or after" read as "after"); `add_exclusive_endpoint` (excl / chain lookups on d - 1 day, so a start date stays with the
old version; keep-old "before" read as "on or before"; sunset "after" read as "on or after"); each endpoint model swaps its lookup shift and its
clause comparator together. T23-registered (prefix t23_): `t23_original_version` (V_1), `t23_ignore_clause` (D0), `t23_foreign_clause` (the clause
applied without its applies-test), `t23_purchase_date`, `t23_event_date`, `t23_filing_date`, `t23_decision_date` (the default read on another date,
then the clause step). ch rows: the wrong option is a seeded label-blind pick (row key) among the distinct wrong answers; each option records every
model that gives it. yn_version / yn_claim rows: yes rows show CANDIDATE = V_G's id / CLAIM = T_G; no rows show the version (term) named by the first
model, in a seeded order (family, sampler, seed), that names a version other than G; one always exists (R14), so no row is dropped or switched.

## 6. Relations (spec 4.1; G-TW 100%)
- Complement on 60% of yes/no base rows: yn_version -> not (syntactic, 100%; v4); yn_claim -> contra (antonym, 60%) or not (40%); yn_outcome -> out
  (antonym, 60%) or not (40%). An antonym partner adds no negation cue, so a double-negation base wording is never drawn for such a row (v4, section 11).
- Minimal-edit twin (proposed on about 60% of bases, about 22% of rows): one input slot moves (a case date or SUN to the other side of its boundary; a
  version start onto or one day past a case date; Q to T_G / T_G + 1; T_G to Q / Q - 1) so that exactly one entry of the construction table (D0, the
  clause state, Q or the terms) changes; the prediction is that table's answer, the twin is kept only when it flips, and G-TW checks the solvers' gold
  equals it. Moves are tried in a seeded order; a move is skipped unless the twin keeps every semantic invariant (strictly increasing starts, P <= EV
  <= F <= DEC on or after S_1, distinct terms >= 1, SUN inside its bracket, Q >= 0). A twin may leave the generator ranges (gap 45-320, pool, Q <= 3 x
  pool max: 19.0 / 7.8 / 0.6% of twins on 2,000 specs).
- equiv (13% of bases): same facts and question, a skin of another register (every row has a narrative skin, whatever its block style); inv (5%): the
  same row plus one inert attack line.
- G4 (checked, never emitted): rename the customer (same); rename the organisation (same); shift every date by 35 days (same); rename the gold version
  (ch_version: the new id; others: same, as CANDIDATE / CLAIM follow their version).

## 7. What Haiku writes (after A38, the PREREG ruling of 13 Oct 2026 that froze OHS-4) and the slot lock
- Mode T (>= 75% of rows): Haiku writes a slot-locked skin and the program fills every slot. Mode F (<= 25%, target 20%): Haiku writes free text from
  a facts-only brief with CUSTOMER, ORG, ITEM and CASE_ID verbatim (G-SL fact-lock; G3-H re-extraction >= 98% per template; v3 ITEM schema: section 10).
  v4 draw, from the row key only: the author mode first (F with probability 0.20), then the register (S4: email, chat, transcript; S1-S3: weights that keep every register under 15%), then a skin of that mode.
- Narrative skins: registers memo, email, chat, ticket, json, yaml, faq, transcript; held out (S5 only) notice, export. Slots: CUSTOMER, ORG, ITEM
  (names), CASE_ID optional (0-1 use; the case record always prints it). Nothing else: no date, number, count, time phrase ("last year", "next
  month"), recency or change word (new, old, latest, current, updated, effective, in force, applies, replaced), no rule, term, window, limit, clause, question, outcome or label word; G-SL plus the T23 skin word list (haiku_author.py) enforce it.
- Question wordings: lexicon kind question, sem q.t23.<qform> for the 11 forms of R14-R18 (ch_version, ch_term, yn_version, yn_version_other,
  yn_version_not, yn_claim, yn_claim_contra, yn_claim_not, yn_outcome, yn_outcome_out, yn_outcome_not); >= 30 in total, >= 6 admitted per form, each
  <= 2% of family rows. Every wording asks about G ("governs", "the governing version", "the version that governs / decides"), never "in force",
  "current", "effective", "applies", "today", "now", "latest", "newest", a date role, a number or "correct". Claim forms ask whether the governing
  version supports / contradicts the claim to check in the case record (support, never truth in the world); outcome forms ask within / outside the
  TERM_LABEL set by the governing version. Slots: CASE_ID, DOC, TERM_LABEL; CANDIDATE on yn_version forms only. Exact negcount: base and antonym forms
  none ("other than" allowed on _other); _not forms exactly one syntactic negation; no wording negates its question frame (v3, section 10). Double
  negation: >= 3 admitted wordings per positive yn form serve the spec 3.0 quota, each the positive question with two cancelling syntactic negations
  inside the asked clause (v3, section 10; v4: under an explicit outer frame only, section 11). G-LEX: 2/2 blind extractions pick the meaning among the 11 plus 2 decoys (the version in force on a case date before any clause; the version in force today or on the decision date); any other pick rejects the form for good; each read fills the form as a row does (v3, section 10).
- Packs (program expands; 4 per domain asked, >= 25 used, one per card): DOC, TERM_LABEL, QTY_LABEL (input domains), four date labels (each ending in
  " date"), items, organisation and customer names, a 2-letter id prefix. The term kind, pool, Q kind and day-count pair are the domain's (table). A
  day-count QTY_LABEL is program-made, "day count from A to B" with A, B the pair's date labels without " date"; solver B reads the pair from these names.
- Attack lines (inv rows): one line, may use {CUSTOMER}; no digit, date, amount, id, rule sentence or label word; never shaped like a version, clause or case line.
- v1 final for C2: card, window rule, version blocks, clause sentences and case record stay program-written; no window or transition paraphrase is authored (3/3 admission and a record parser would come first: not in C2).

| Domain | Term (kind; pool) | Q | Date labels (purchase / event / filing / decision) |
|---|---|---|---|
| refunds | refund window (days; 7 10 14 21 28 30 45 60 90) | day count purchase -> refund request (F - P) | purchase / delivery / refund request / decision date |
| warranties | warranty period (days; 30 60 90 180 365 730) | day count purchase -> fault (EV - P) | purchase / fault / claim / decision date |
| fees | fee cap (cents; $15 20 25 35 40 50 75) | fee charged (input) | account opening / billing / dispute / decision date |
| leave | paid leave allowance (days; 10 12 15 20 25 30) | leave days claimed (input) | hire / leave start / claim / decision date |
| subscriptions | free cancellation period (days; 3 5 7 14 21 30) | day count sign-up -> cancellation (F - P) | sign-up / renewal / cancellation / decision date |
| shipping | delivery promise (days; 2 3 4 5 7 10 14) | day count order -> delivery (EV - P) | order / delivery / complaint / decision date |
| retention | retention period (days; 30 60 90 180 365 730) | day count closure -> deletion request (F - EV) | record creation / record closure / deletion request / decision date |
| pricing | price cap per unit (cents; $12.50 14.99 19.99 24.00 29.99 35.00) | unit price charged (input) | contract / delivery / invoice / decision date |
| travel | nightly hotel cap (cents; $120 150 175 200 250) | nightly rate claimed (input) | booking / travel / expense claim / decision date |
| licences | device limit (devices; 1 2 3 5 10) | devices registered (input) | licence purchase / activation / support request / decision date |

Input Q (integer cents or a whole count, >= $1.00 or 1) is drawn around the governing term T: non-outcome rows within about [0.17, 3.2] x T (whole
dollars for cents); outcome rows on the targeted side (cents T -+ whole dollars, counts [T/2, T] or T + 1..10, devices T + 1..3), at an edge T or T +
1 unit. G-SL exceptions: none. NAME_ALLOW: FAQ, HR, IT (capitalised words a skin may use that are not names; no fact-lock exception). Terms: kit = c2_build/c2_kit; rules.Cmp = its rule-AST comparison node; gates = c2_build/README.md; plugin.DOMAINS = this table (code stand-ins).

## 8. Ambiguity points written before the pass (v1; all answered above)
The 15 points (inclusive / exclusive / chain bounds; "would govern" = D0; keep-old role date = S_c, target two back; retro any older version, a newer one in force on DEC; sunset DEC = SUN; a non-applying clause = t23_foreign_clause; DEC never the anchor; equality within; printed day counts; exact claim equality; ids = labels) are answered in R3-R12, R14 and R16-R18.

## 9. Resolution of the Haiku ambiguity pass (c2-data-stage-a/amb:T23, 13 Oct 2026; haiku/ambiguity/amb_T23_points.json; H<n> = points[n-1])
H1 precedence, H2 re-freeze (text governs; old-sha rows discarded): header. H3 bounds: R2-R4. H4 symbols: notation (R items vs S samplers; EV, END_k,
K). H5 subscripts: notation, R3, R8 (days, both ends included). H6 excl ends: list / table heads mark "end dates included / excluded" (1.2; solver B
refuses a marker that contradicts the card). H7 "up to": the excl rule says "through the day before its end date"; no Haiku paraphrase of the card
(7). H8 middle version: 1.2. H9 clause place: R5. H10 one clause, H11 own condition, H12 would govern: card, R4, R5. H13 target with a newer version
in force on DEC: card ("even if another version is in force on a later date"), R7, R8, hand test. H14 foreign: section 3 (own applies-test fails). H15
dates, H17 cents, H18 plain: 1.2 values, R15. H16 day counts: R11 (wordings never restate a window in days). H19 pools and inputs: section 7. H20
floor / ceiling / measured on gold, H21 tags, H22 per row: section 3. H23 base vs all rows, H24 sort and display, H25 tokenizer and layout: section 4,
1.2, R14. H26 K = 2: R14 (a distinct wrong version always exists; tested). H27 which model, H28 equal to gold, H29 no rows, H30 names and endpoint
models: section 5. H31 ids: R14. H32 polarity: section 7 (exact negcount; G-LEX 2/2). H33 construction table, H37 disagreement (unit dropped), H38
released / pulled: R21. H34 twin moves, H35 attack / notes / inert / equiv, H36 G4 rename: R13, section 6. H39 depth: R20. H40 skin lock (strict), H41
CASE_ID, H42 wordings ask G (banned words, decoys), H43 claim / outcome wordings, H44 >= 30 total and >= 6 per form, H45 modes / 3/3 / parser / A38
(card and clauses stay program-written), H46 NAME_ALLOW: section 7. H47 items 8, 13, 15: card, R11, R14. H48 labels: notation, sections 2, 7. Code
changed for the v2 freeze: the card (H7, H10-H13), the list / table head marker and solver B's check of it (H6), solver B's day-count pair read from the label (section 7). A flagged skin or wording is rewritten or dropped, never relabelled.

## 10. Pool-review rulings (redo2 of the stage-A pool review B1-B4, 13 Oct 2026; v3; tasks and results in haiku/redo2/)
B1 G-LEX fill. Each read shows the form filled as a row fills it: one pack's DOC and TERM_LABEL (section 7 table), CASE_ID as CASE-dddd, CANDIDATE as a version id (v1, rev-A or PFX-123), no value in two slots, no person's name. The v1 reads (glex-read0/1) showed "Dana Okafor" in every name slot and "INV-20419" in every id slot, so they admit nothing alone: each v1-admitted form that keeps the frame rule (B3/B4) is read again by 2 new blind extractors (glex-r2read0/1; the v1 prompt and the 13 choices unchanged) and stays admitted only if both pick its meaning; a v1 rejection is final and is never re-read.
B2 G3-H ITEM. The ITEM field asks for the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its), which is the brief's ITEM value; the v1 schema ("what the case is about, as written") let 10 of 172 extractors keep the determiner. Every loader-admitted Mode F note is read again under this schema (new qids) and that read replaces its v1 read; the exact compare (g3h.compare) and the 98% bar are unchanged.
B3/B4 frame rule. No wording negates its question frame: no fronted negative auxiliary ("Isn't", "Doesn't", "Wouldn't" ...), no "is it not" / "does it not hold" / "isn't it so", no tag question. A negated frame asks the reader to confirm its clause, so its literal and its confirming readings give opposite golds: v1 G-LEX read "Is it not the case that {CANDIDATE} does not govern ..." as fails-to-govern on 5 of 6 reads, read the same frame literally on yn_claim#485c0a50, and admitted yn_outcome#e4058170 and yn_claim#b0ba2bfe only under the confirming reading. Every negation sits inside the asked clause. The rule is checked on every form before any read; it removes the admitted yn_claim#485c0a50, yn_claim#b0ba2bfe, yn_outcome#e4058170 and yn_outcome_not#e68728cb (and the six v1-rejected double negations).
B3/B4 double negation. A double-negation wording asks the positive form's question under an un-negated frame, with exactly two syntactic negations inside the asked clause that cancel (negcount k_all = k_syn = 2; shapes "it is not the case that X does not ..." and "is X not a version that does not ...") and no antonym or word with a "no" meaning (outside, beyond, exceed, over, above, differ, depart, contradict, conflict, against, other, fail, lack, without): an antonym on top of two negations asks the complement (v1 rejects yn_outcome#961b0c9e, yn_outcome#cfa3f0d3, yn_claim#8c77afd3). New ones are authored under this rule (haiku/redo2/) and admitted only by 2/2 G-LEX reads with the B1 fill. v3 changes no gold, solver, sampler, row or gate bar.

## 11. Stage B pilot fix iteration 1 (14 Oct 2026; v4; PILOT_VERDICT FIX-1 to FIX-4; no bar loosened, no label touched, pools_v2 unchanged)
Wording screen (c2_kit.polarity; plugin.POLARITY_*, NEGATIVE_PREDICATES): every yes/no wording must read with its form's polarity (P1 no syntactic negation over a negative predicate, P2 parity, P3 no contracted frame): all 159 admitted yes/no wordings pass. The v3 shape "is X not a version that does not ..." negates its question frame ("aux + subject + not": a confirming reading reverses the gold, as B3/B4), so P4 quarantines the 13 double negations of that shape (yn_version#2c822bb7 #5b7759ca #8d3f3916 #a716edc2; yn_claim#628c8724 #84f76171 #88ec11aa #9c2bd84c #aba6f0ab; yn_outcome#66b8802b #7b90581b #e737d26e #ea145c1a). 14 stay, all under an explicit outer frame (yn_version 5, yn_claim 4, yn_outcome 5; the quota needs 3). The 28 single-negation _not wordings of the same surface shape stay (one negation inside the asked clause, G-LEX admitted). A double negation is never drawn for a row whose complement is antonym or implicit (ctx_for).
