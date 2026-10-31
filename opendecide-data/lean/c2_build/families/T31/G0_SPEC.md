# G0-lite T31: authority at time t (delegations, bands, revocations, sub-agent scopes)

C2_DATA_SPEC 2.1 (T31, 1,000 selected rows, wave 2, agent tier) and 3.8; rules for every family in 3.0 and 4.1. One page:
semantics table, card text, samplers, traps, balance, error models, relations, Haiku asks, resolutions. Status: frozen v1.2 (sha256 in plugin.py). v1.1 (archived verbatim: G0_SPEC_v1_1.md, the pool authoring pin) = v1 + the
one Haiku ambiguity pass (task `amb:T31`, 45 points) + one Claude resolution (section 8). v1.2 = v1.1 + fix iteration 1
(14 Oct 2026; pilot/PILOT_VERDICT.json F01-F10, P1-P5; kit choiceplan, cards, polarity): a Claude amendment that moves no
semantics (M2-M5, M7, M8, M11, M13, M14, M16 and the record formats are unchanged); it changes M1, M6, M9, M10, M12, M15
(shares, sizes, two forms), 1.1 (card in 3 styles, rules in row.card on yes/no rows), 2, 4, 6, 7. The Haiku ambiguity
re-pass of the v1.2 card is OPEN (no Haiku ran). Code: plugin.py (solver A), solver_b.py (B), fixtures.py (tests). Samplers
S1-S5 (section 2); "list" and "log" are record styles, "memo" ... "export" skin registers; window = period = "in effect".

## 1. Semantics table (exact; every rule below is printed on the card)

| # | Item | Semantics |
|---|---|---|
| M1 | Tracks | `appr` (who holds the single accountable A role for a request at its time) and `agent` (may the requesting agent, always the deepest agent of the grant chain, use a scope at the request time). Base specs split 55 / 45 (v1.1: 60 / 40: the token mean needs it, F09) |
| M2 | Times | Fixed-offset datetimes in the kit forms only: ISO `2026-03-05T14:05:00+02:00`, ISO `2026-03-05T12:05:00Z` (Z = +00:00), text `5 March 2026, 14:05 (UTC+02:00)`, log `2026-03-05 14:05:00 +0200`. Seconds are always 00 (every time is a whole minute); `Z` and `UTC+hh:mm` are offset labels, never zone names; no DST. Training offsets +00:00, +01:00, +02:00, +03:00, +05:30, +09:00, -03:00, -04:00, -05:00, -08:00 (S5: +05:45, -09:30, +08:45, +10:30). The row offset is the request time's offset. Every other time uses it except at most one (the conversion; never the request time), which is followed by `[same instant: <time in the row offset>]`; every comparison is between instants |
| M3 | Window end (card-level) | `incl`: a delegation or grant covers requests from its start time through its end time, both included. `excl`: from its start time up to but not including its end time. Start is always included. Every window has end > start (no empty or inverted window is generated) |
| M4 | Notice instant | A revocation or override takes effect at the instant it is issued: a request at that exact instant is affected, a request before it is not |
| M5 | Bands | Lexicon comparator clause on an integer-cents bound: `cmp.le` amount <= bound, `cmp.lt` <, `cmp.ge` >=, `cmp.gt` >; only admitted forms whose words say whether the bound is included (section 7). `of any size`: every amount fits. Amounts and bounds are positive whole cents (>= $1.00), printed `$1,234.50`, `1,234.50 USD` or `$1,200` |
| M6 | appr records | RACI matrix of 6-7 roles (sampler S3: 7-8; S5: 6-8): exactly one letter A (the default holder), 1-2 R, rest C / I; the matrix holds at every time. 1-2 delegations from the A holder to distinct other people (window + band). 0-1 notices (S2 and S4: 1; a ch_approver row that shows escalate: one delegation + two overrides or two delegations + one notice, section 4; list style puts both under `Notices:`): a revocation of one delegation (always issued after that delegation's start), or an override naming a person other than the A holder, with a band and no end. The requester is never a matrix person |
| M7 | appr covering | A delegation covers the request iff start <= T, T within its end (M3), no revocation of it issued <= T, amount in band. An override covers iff issued <= T and amount in band. The card defines "covers" in these words |
| M8 | appr precedence | The deciding level is the first level with a covering record: (a) overrides: the person(s) named by the covering override(s) issued at the latest instant; (b) delegations: the delegate(s) of the covering delegations; (c) the matrix A holder. Two different people at the deciding level -> escalate; the same person twice is that person; a lower level never causes escalate. "Latest" is by instant, never by listing order |
| M9 | appr answers | `ch_approver`: key = the person's exact matrix string, or `escalate` (option text "Escalate: no unique approver", quoted on the card). Approver = the A-role holder only (an R person is never the approver). `yn_holder` yes iff holder == CANDIDATE; `yn_holder_dneg` (v1.2: two cancelling syntactic negations, positive polarity) the same; complements `yn_holder_other` ("other than CANDIDATE", implicit) and `yn_holder_not` (syntactic) yes iff holder != CANDIDATE. Yes/no rows are generated only when the holder is unique (never escalate) |
| M10 | agent records | The principal grants AGENT_1 2-5 scopes (sampler S3: 2-6); AGENT_j grants sub-agent AGENT_j+1 2-5 scopes. Depth = grants on the chain = agents, 1-2 (3 only on deep rows, weight 8% on S1 / S3); exactly one grant per agent, each with a window (M3). A grant's BY is the agent's parent (it defines the chain); principal and chain hold at every time. 0-1 revocations (S2: 1): one scope from one agent, or a whole grant, issued by the principal or the agent's parent (the issuer never matters); always issued after the target grant's start. Every record id and agent a line names exists (solver B refuses a dangling one) |
| M11 | agent usable | Scope s is usable by AGENT_j at T iff its grant is in its window at T, lists s, has no whole-grant revocation issued <= T, s has no revocation from AGENT_j issued <= T, and (j >= 2) s is usable by AGENT_j-1 at T (attenuation: the child set is an intersection, never more than its parent; a child never inherits a scope its own grant does not list). The card says "exactly when": necessary and sufficient |
| M12 | agent answers | The request is made by the deepest agent and the question names it (REQ_AGENT). `yn_agent_ok` and `yn_agent_dneg` (two cancelling negations) yes iff REQ_SCOPE is usable at T (permission, not possession). `yn_agent_beyond` ("exceed the agent's authority", antonym), `yn_agent_lacks` ("lack the authority to use", implicit; never "its grant does not list"), `yn_agent_not` (syntactic): yes iff not usable; v1.2: each of the three is also a BASE form (F06), with `yn_agent_ok` as its one complement. `ch_scope` (depth >= 2): "which of these scopes can AGENT use"; exactly one scope of the agent's own grant is usable (generator asserts it); options = that scope + error-model scopes. A scope the agent's grant does not list is not usable |
| M13 | Closed world | CLOSED_WORLD_SENTENCE "The listed records are complete: no other record exists." plus "Listing order and who issued a record (a revocation) do not matter": narrative, attack lines and listing order change nothing, issuer authority is never tested, and every listed record is in force as written |
| M14 | Identity | People, roles, agents, scopes and record ids are exact strings, distinct within a row (no two people share a first or a last name word); exactly one request per row |
| M15 | Depth | appr: 2 unstated tests (time vs records, amount vs band); agent: grants on the chain (1-2); deep = 3 (<= 10% of the family, `meta.deep`). A row has zero or one conversion (S4 40%, others 20%), and a conversion is always restated (M2) |
| M16 | Gold | Solver A (`rule_engine`): one kit rule AST per record (rules.Cmp / And / Not / In / Or over aware datetimes and cents) run by rules.evaluate, then the M8 levels or the M11 chain conjunction. Solver B (`interval_scan`): epoch-minute half-open intervals [start, end + 1) (incl) or [start, end) (excl), cut at the first revocation minute (overrides never close), scanned at the request minute; bands by an integer-cents sign table; set intersection of held scopes down the chain. A third construction table (status flags) steers the samplers and predicts twins; it never sets gold |

### 1.1 Card text (program-written; solver B keeps its own copy and full-matches it; v1.2: three styles)

The rule block is bullet lines (no heading) + the closed-world sentence. Yes/no rows print it in `row.card` (the served
prompt prints the card once; instructions = the question); choice rows keep it at the head of the instructions (blank line,
then the question). Style: label-blind, from seed + sampler + track only, so a twin, a complement and an equiv / inv
partner share it: full 20%, compact 65%, short 15% (spec 3.0); `meta.defs_style` = `rules_in_<card|instructions>_<style>`.
appr, full:

    - A delegation covers the request when the amount is in its band and the request time is from its start
      time {END}, before any revocation of it.
    - An override covers the request when the amount is in its band and the request time is at or after its
      issue time.
    - The first level with a covering record decides the approver (the holder of the accountable (A) role):
      overrides, the person named by the latest issued; delegations, the delegate; otherwise, the person marked
      A in the standing RACI matrix.
    - If that level gives two different people, the answer is "Escalate: no unique approver". {TIMES}
    - Listing order and who issued a record do not matter.
    The listed records are complete: no other record exists.

agent, full: "- Each agent holds one grant. An agent may use a scope at an instant exactly when its own grant lists the
scope, the instant is from the grant's start time {END}, no revocation of that scope from that agent or of the whole
grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its grant) may use the scope at
that instant." + "- {TIMES}" + "- Listing order and who issued a revocation do not matter." + the closed-world sentence.
compact: appr bullets 1-2 are one ("...before any revocation of it; an override, when ..."), "standing" is dropped, the
listing-order bullet and the closed-world sentence share a line; agent "start time" -> "start" and {TIMES} ends the first
bullet. short: appr "Delegation: covers the request if ... Override: covers it if ...", "Approver (holder of the
accountable (A) role): the first level with a covering record decides; ...", "If that level gives two different people:
"Escalate: no unique approver"."; agent "It may use ... its grant lists ... may use the scope then.". The exact texts are
plugin.CARD_TEXT and solver_b._APPR / _AGENT (tests: equal; cards.variant_problems(full, variant) == [] = same slots,
quoted literal, operator words, negation count). {END}: full `incl` "through its end time (the end time is included)",
`excl` "until its end time (the end time is excluded)"; compact / short "through its end time (included)" / "until its
end time (excluded)". {TIMES}: "Compare times as instants." and, only on rows with the conversion, "Compare times as
instants; a time in another offset shows the same instant in square brackets." No digit appears in card text.

### 1.2 Record block (program-written; state = narrative skin + blank line + block [+ blank line + attack line])

Block = `Records:` line ... `End of records.` line. Styles (sampler-level): `list` and `log`. TIME = a datetime in a kit
form (M2), plus ` [same instant: TIME]` on the conversion; BAND = comparator clause or `of any size`. In log style every
line starts with the time the record takes effect, and its verb says which (starts / issued / made).

| Record | list | log |
|---|---|---|
| appr head | `Process: P` / `Standing RACI matrix:` / `- ROLE: PERSON [L]` / `Delegations:` | `process \| P` / `matrix \| ROLE \| PERSON \| L` |
| delegation | `- ID: FROM delegates the A role to TO, from TIME to TIME; amounts BAND.` | `TIME \| delegation ID starts \| FROM -> TO \| ends TIME \| amounts BAND` |
| revocation | `- ID, issued TIME by BY: delegation DID is revoked.` | `TIME \| revocation ID issued \| by BY \| revokes DID` |
| override | `- ID, issued TIME by BY: override, the A role goes to P; amounts BAND.` | `TIME \| override ID issued \| by BY \| A role to P \| amounts BAND` |
| appr request | `Request ID: amount AMT, made at TIME.` | `TIME \| request ID made \| amount AMT` |
| agent head | `Principal: P` / `Grants:` | `principal \| P` |
| grant | `- ID: BY grants [sub-agent ]AG the scopes S1, S2; in effect from TIME to TIME.` | `TIME \| grant ID starts \| BY -> AG \| scopes S1, S2 \| ends TIME` |
| scope revocation | `- ID, issued TIME by BY: scope S is removed from AG.` | `TIME \| revocation ID issued \| by BY \| scope S from AG` |
| grant revocation | `- ID, issued TIME by BY: grant GID is withdrawn in full.` | `TIME \| revocation ID issued \| by BY \| grant GID in full` |
| agent request | `Request ID: at TIME, AG asks to use scope S.` / `... AG is about to act.` (ch_scope) | `TIME \| request ID made \| AG \| scope S` / `... \| AG \| about to act` |

Section lines in `list`: `Notices:` (or `Notices: none.`), `Revocations:` (or `Revocations: none.`). The chain is read from
BY -> AG in both styles (`sub-agent` in list style is a redundant marker).

## 2. Samplers (>= 4 training shapes + held-out S5)

| Sampler | Shape | Style | Notes |
|---|---|---|---|
| S1 | forward: records drawn independently, target outcome reached by rejection | list | 1-2 delegations (mostly 1), 0-1 notices; agent depth 1-3 (depth 3 weight 8%) |
| S2 | label-first near-miss: record times at T-1 / T / T+1 minute, amounts at band bounds | list | each competitor misses by one condition; 1 notice, 1 revocation |
| S3 | config export: larger org (7-8 roles), 1-2 delegations (mostly 2), up to 6 scopes | log | agent depth 1-3 (depth 3 weight 8%) |
| S4 | narrative / transcript: chat, email and transcript skins; conversion on 40% of rows | list | 1-2 delegations, 1 notice |
| S5 | held out (mixdev only): held-out skins and registers (runbook, export), offsets +05:45 / -09:30 / +08:45 / +10:30 | log | never a training row |

Depth 3 is capped by M15 (<= 10% of the family; measured 1.8%). Cards: (sampler, track, card 0-5); the card fixes the
window-end rule (even incl, odd excl) and ONE PACK from the frozen pools_v2 packs (34 appr, 36 agent, ranked by a hash of
their content: the first 24 feed the S1-S4 cards, the next 6 the S5 cards); people from the 320 names: 48 training
cards, about 31 rows per card at 1.5x generation.

## 3. Traps (floors on the family's rows; tags overlap; tags in `meta.edge`; generator check >= 0.75 x target)

| Tag | Target | Construction (pilot_i1, 543 base rows) |
|---|---|---|
| `rev_1min` | 25% | a notice or revocation issued exactly 1 minute before the request (31%) |
| `band_edge` | 20% | request amount equal to a band bound (appr) (19%) |
| `sub_broader` | 20% | a sub-agent's grant lists a scope its parent's grant lacks (32%) |
| `lapsed` | 15% | a delegation or grant whose window ended before the request, or at it under `excl` (25%) |
| `escalate_like` | 10% | two delegations in their window (band ignored), or two overrides issued, at the request: band or level decides whether it is escalate (14%) |
| `inherit_trap`, `notice_after`, `notice_at`, `conversion`, `not_started`, `deep_chain` | report | as named |

Escalate gold is a cap, not a trap: <= 12% of ch_approver rows (section 4). Skins are label-blind; attack lines never change
the gold (M13).

## 4. Balance targets (generator level; c2_select tightens to the spec 3.0 cells)
- Base question forms (share of base specs): ch_approver 36%, yn_holder 15%, yn_holder_dneg 4%, yn_agent_ok 7%,
  yn_agent_dneg 4%, yn_agent_beyond / _lacks / _not 4% each, ch_scope 22%. A double-negation form is drawn only while the
  lexicon admits a polarity-clean wording of it, else it falls back to yn_holder (19%) / yn_agent_ok (11%). With partners
  and twins yes/no is 45-55% of rows (pilot_i1 52%). Gold yes 50% on every yes/no form (label-first target bit = the
  answer, so a negative base form targets "not usable"). Yes = bad outcome 50% (52%): `yes_is_bad` False for yn_agent_ok /
  _dneg, True for the 3 negative forms; yn_holder forms are neutral. Deep rows <= 10%.
- ch_approver, label-first from a c2_kit.choiceplan plan drawn from the row key BEFORE any structure: k = 3 or 4 (the
  escalate option counts), escalate shown on 40% of rows, gold = escalate on 1/k of the rows that show it (about 7.5% of
  all ch_approver rows; binding 5-12%), gold position and gold length rank balanced per block of 32 seeds. The structure is
  drawn until solver A agrees with the plan; nothing is relabelled. Escalate is wrong on >= 67% of the rows that show it in
  every (k, shown) cell. Options are ranked by visible length with the gold at its planned rank, so gold-is-longest is 1/k.
  The other golds: override 33%, delegation 35%, default 32%. ch_scope: the same plan without an abstain option.
- A ch_approver row that shows escalate has no twin (it would dilute the escalate share): the rows that show it are the
  base and its equiv / attack copies. It also has the escalate-like shape whatever its gold, drawn per seed: A (70%) two
  delegations in their window + one notice, B (30%) one delegation + two overrides (a tie = one instant); the band, a
  revocation or the issue times decide. Record counts then say nothing about the escalate option (a G6 d_meta model read
  the gold off them: +16 pp on those rows). A yes/no base has a one-slot flip with probability 0.90 (either answer; seed
  hash), so twins are about as often yes as no (F05: the pilot's twins were 33% yes).
- Length (Qwen3.5-4B tokenizer, mixer.token_counts): row tokens = state + card + 2 x instructions + options. Family mean
  <= 800 (pilot_i1 785.4; v1: 960.7), every row <= 2,000 (max 1,100).

## 5. Error models (every wrong option; spec 3.0)
Kit-shared names (distractors.CATALOG): `ignore_revocation`, `add_exclusive_endpoint` / `drop_inclusive_endpoint` (band and
window ends), `skip_offset_conversion` (wall-clock times), `first_match` / `last_match` (first / last covering record in
listing order). Family names carry `t31_`. ch_approver (solver A with one rule swapped; output = a person; escalate
outputs are dropped, the escalate option is shown only as the plan says): `t31_default_holder`, `ignore_revocation`,
`t31_ignore_window_end`, `t31_future_notice`, the two endpoint models, `t31_ignore_band`, `skip_offset_conversion`,
`t31_earliest_override`, `t31_delegation_beats_override`, `first_match`, `last_match`, `t31_responsible_role` (the first
R), `t31_issuer_as_holder` (the issuer of the latest notice in force). ch_scope: `t31_ignore_attenuation`,
`t31_inherit_parent`, `ignore_revocation`, `t31_future_notice`, `skip_offset_conversion`; each outputs the first scope it
wrongly adds, scanning the deepest grant first (a tie-break only; display order is the plan's gold position).
yn_holder: on a "no" row the CANDIDATE is the person named by the first error model, in an order seeded by (seed, model
name), that names another matrix person; if none does, the case is redrawn. yn_agent "no" rows: no error model; REQ_SCOPE
is drawn label-blind (an own-grant scope made unusable by window, revocation or attenuation; a parent-only scope (inherit
trap); or a scope the agent's grant does not list) and the case is redrawn until the target bit holds.

## 6. Relations (spec 4.1; G-TW 100%)
- Complement on 42% of yes/no base specs: yn_holder -> other (implicit, 60%) or not (syntactic, 40%); yn_holder_dneg ->
  not (k_all 2 vs 1); yn_agent_ok -> beyond (antonym, 30%), lacks (implicit, 30%), not (syntactic, 40%); yn_agent_dneg ->
  not; each negative agent base -> yn_agent_ok. Pilot_i1: 36% of yes/no rows are in a pair, 54% of pairs non-syntactic.
- Minimal-edit twin, proposed for 60% of yes/no base specs and for every ch_approver base that does not show escalate;
  twins are 20-25% of family rows (pilot_i1 22.8%). One input slot moves and flips exactly one condition of one record:
  a revocation or override time T-1 <-> T+1 minute, a delegation or grant end T-1 <-> T+1, a band bound onto the amount
  edge, or one scope slot of a chain grant (in or out). The prediction comes from the status table with that one flag
  flipped (never from solver A). A twin is proposed only when the gold key changes (another person, or yes <-> no),
  never when its gold would be escalate, and never moves a revocation to or before its target's start. A ch_approver
  twin keeps k, display and position and may take another length rank (the planned one first).
- equiv (15% of bases: another skin and register of the same track), inv (10%: one inert attack line of the same track).
- G4 (checked, never emitted): rename the requester (same); shift every time by +97 minutes (same); rewrite the request
  time in another offset (same; a solver check only: the M2 bracket rule does not apply); rename the gold person (the new
  name) or the candidate (same) or the requesting agent (same); rename the gold scope everywhere (ch_scope: the new scope).

## 7. What Haiku writes (after A38; Mode T >= 75%) and the slot list it must keep
- Narrative skins per track: the id carries `appr` or `agent` as a separate part (T31-appr-memo-0007); the plugin picks
  only the row's track (ctx_for), an untagged skin fits both. >= 8 registers: memo, email, chat, ticket, json, yaml, log,
  transcript; held out: runbook, export. Slots: REQUESTER (name, once), ITEM (name, once; narrative only; never
  `{cap|ITEM}`: the 20 such skins are quarantined, F01), optional REQ_ID (id, at most once). They say who raised which
  request; never a record, time, amount, org person, rule, question, outcome or claim ("the setup looks good"). The pick is
  register-first (8 registers, about 12.5% each); each skin feeds <= 6 rows.
- Question wordings (>= 30; pool target about 170 candidates over the 11 forms, each wording <= 2% of family rows):
  lexicon kind "question", sem q.t31.<qform>. Required slots: yn_holder* CANDIDATE; yn_agent* REQ_AGENT and REQ_SCOPE;
  ch_scope REQ_AGENT; optional REQ_ID. Approver words name the accountable (A) role; a wording asks about the request time
  or names no time (never "now" / "currently"); one negation at most (yn_*_not); the two dneg forms exactly two, with the
  explicit outer frame "Is it not the case / true / correct that ... not ..." (dneg_authoring.py). The c2_kit.polarity
  rule (P1-P4, strict frames) holds for every yes/no wording: a negation over a negative predicate (bar, block, exceed ...)
  or a contracted frame is refused (one frozen wording is screened out). G-LEX decoys: possession; an R person; "other
  than the default holder"; the present moment.
- Band paraphrases: lexicon kind "comparator", slot X cents, 2/2 extraction; each form says whether the bound is included
  ("or less", "at most", "up to and including", "less than", "at least", "or more", "more than", "strictly below /
  above"); bare "under", "over", "below", "above", "up to", "within" are not authored.
- Attack lines per track (slot REQUESTER only): an inert note or a fake authority claim, no record, time or amount. Packs (frozen pools_v2, wired): appr = process + 4 items + 12 role titles; agent = 12 scope ids (`resource.action`)
  + 4 tasks + 6 agent ids; 320 invented full names; 34 / 36 packs (24 training + 6 S5 cards per track). G13-seed on the
  pools_v2 pieces is still to run.
- Mode F (<= 25% of rows; 18.8% of the skin pool): free-form text per track with REQUESTER, ITEM and REQ_ID verbatim (ITEM
  never after "a" / "an" or at a sentence start; G-SL fact-lock; G3-H reads ITEM without its article). Screened out: a
  word of the REQUESTER value outside the value, a gendered pronoun, a claim (14 of 116 documents). v1 keeps every record
  line and the card program-written: no precedence or window paraphrases (no 3/3 forms).
G-SL exceptions (EXTENDED words skins may use): `approval`, `grant` name the request and record types, never an outcome.

## 8. Haiku ambiguity pass: resolutions (v1.1; v1.2 changes are marked in the rows above)
Every point is resolved in the body: #1-5 M2, M3, M5, M6, M10, M15, 6 | #6-10, #12 M6-M8, M10, M13 (card) | #11 1.2 | #13-16 M1,
M6, M10, M12 | #17-24 M9, M12, 7 (G-LEX decoys; #23 yes = the negated statement holds) | #25-45 M5, M6, M14, 2-7, spec 3.0 / 6.3.
