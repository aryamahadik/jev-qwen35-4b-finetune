# G0-lite T31: authority at time t (delegations, bands, revocations, sub-agent scopes)

C2_DATA_SPEC 2.1 (T31, 1,000 selected rows, wave 2, agent tier) and 3.8; rules for every family in 3.0 and 4.1.
One page: semantics table, card text, samplers, traps, balance, error models, relations, Haiku asks, resolutions.
Status: frozen v1.1 (sha256 in plugin.py). v1.1 = v1 + the one Haiku ambiguity pass (workflow c2-data-stage-a, task
`amb:T31`, 45 points) + one Claude resolution (section 8). Code: plugin.py (solver A), solver_b.py (solver B),
fixtures.py (test stand-ins). Semantic rows are M1-M16; samplers are S1-S5 (section 2); "list" and "log" are record
styles, "memo" ... "export" are skin registers; window = period = "in effect" (start to end under the M3 rule).

## 1. Semantics table (exact; every rule below is printed on the card)

| # | Item | Semantics |
|---|---|---|
| M1 | Tracks | `appr` (who holds the single accountable A role for a request at its time) and `agent` (may the requesting agent, always the deepest agent of the grant chain, use a scope at the request time). Split 60 / 40 |
| M2 | Times | Fixed-offset datetimes in the kit forms only: ISO `2026-03-05T14:05:00+02:00`, ISO `2026-03-05T12:05:00Z` (Z = +00:00), text `5 March 2026, 14:05 (UTC+02:00)`, log `2026-03-05 14:05:00 +0200`. Seconds are always 00 (every time is a whole minute); `Z` and `UTC+hh:mm` are offset labels, never zone names; no DST. Training offsets +00:00, +01:00, +02:00, +03:00, +05:30, +09:00, -03:00, -04:00, -05:00, -08:00 (S5: +05:45, -09:30, +08:45, +10:30). The row offset is the request time's offset. Every other time uses it except at most one (the conversion; never the request time), which is followed by `[same instant: <time in the row offset>]`; every comparison is between instants |
| M3 | Window end (card-level) | `incl`: a delegation or grant covers requests from its start time through its end time, both included. `excl`: from its start time up to but not including its end time. Start is always included. Every window has end > start (no empty or inverted window is generated) |
| M4 | Notice instant | A revocation or override takes effect at the instant it is issued: a request at that exact instant is affected, a request before it is not |
| M5 | Bands | Lexicon comparator clause on an integer-cents bound: `cmp.le` amount <= bound, `cmp.lt` <, `cmp.ge` >=, `cmp.gt` >; only admitted forms whose words say whether the bound is included (section 7). `of any size`: every amount fits. Amounts and bounds are positive whole cents (>= $1.00), printed `$1,234.50`, `1,234.50 USD` or `$1,200` |
| M6 | appr records | RACI matrix of 6-8 roles (sampler S3: 9-12): exactly one letter A (the default holder), 1-2 R, rest C / I; the matrix holds at every time. 1-3 delegations from the A holder to distinct other people (window + band). 0-2 notices (= revocations and overrides; list style puts both under `Notices:`): a revocation of one delegation (at most one per delegation, always issued after that delegation's start), or an override naming a person other than the A holder, with a band and no end. The requester is never a matrix person |
| M7 | appr covering | A delegation covers the request iff start <= T, T within its end (M3), no revocation of it issued <= T, amount in band. An override covers iff issued <= T and amount in band. The card defines "covers" in these words |
| M8 | appr precedence | The deciding level is the first level with a covering record: (a) overrides: the person(s) named by the covering override(s) issued at the latest instant; (b) delegations: the delegate(s) of the covering delegations; (c) the matrix A holder. Two different people at the deciding level -> escalate; the same person twice is that person; a lower level never causes escalate. "Latest" is by instant, never by listing order |
| M9 | appr answers | `ch_approver`: key = the person's exact matrix string, or `escalate` (option text "Escalate: no unique approver", quoted on the card). Approver = the A-role holder only (an R person is never the approver). `yn_holder` yes iff holder == CANDIDATE; complements `yn_holder_other` ("an approver other than CANDIDATE", implicit) and `yn_holder_not` (syntactic) yes iff holder != CANDIDATE. Yes/no rows are generated only when the holder is unique (never escalate) |
| M10 | agent records | The principal grants AGENT_1 2-5 scopes (sampler S3: 2-6); AGENT_j grants sub-agent AGENT_j+1 2-5 scopes. Depth = grants on the chain = agents, 1-2 (3 only on deep rows); exactly one grant per agent, each with a window (M3). A grant's BY is the agent's parent (it defines the chain); principal and chain hold at every time. 0-2 revocations: one scope from one agent, or a whole grant, issued by the principal or the agent's parent (the issuer never matters); at most one per (agent, scope) and per grant; always issued after the target grant's start. Every record id and agent a line names exists (solver B refuses a dangling one) |
| M11 | agent usable | Scope s is usable by AGENT_j at T iff its grant is in its window at T, lists s, has no whole-grant revocation issued <= T, s has no revocation from AGENT_j issued <= T, and (j >= 2) s is usable by AGENT_j-1 at T (attenuation: the child set is an intersection, never more than its parent; a child never inherits a scope its own grant does not list). The card says "exactly when": necessary and sufficient |
| M12 | agent answers | The request is made by the deepest agent and the question names it (REQ_AGENT). `yn_agent_ok` yes iff REQ_SCOPE is usable at T (permission, not possession). Complements `yn_agent_beyond` ("exceed the agent's authority", antonym), `yn_agent_lacks` ("lack the authority to use", implicit; never "its grant does not list"), `yn_agent_not` (syntactic): yes iff not usable. `ch_scope` (depth >= 2): "which of these scopes can AGENT use"; exactly one scope of the agent's own grant is usable (generator asserts it); options = that scope + error-model scopes. A scope the agent's grant does not list is not usable |
| M13 | Closed world | CLOSED_WORLD_SENTENCE "The listed records are complete: no other record exists." plus "Listing order and who issued a record (a revocation) do not matter": narrative, attack lines and listing order change nothing, issuer authority is never tested, and every listed record is in force as written |
| M14 | Identity | People, roles, agents, scopes and record ids are exact strings, distinct within a row; exactly one request per row |
| M15 | Depth | appr: 2 unstated tests (time vs records, amount vs band); agent: grants on the chain (1-2); deep = 3 (<= 10% of the family, `meta.deep`). A row has zero or one conversion, and a conversion is always restated (M2) |
| M16 | Gold | Solver A (`rule_engine`): one kit rule AST per record (rules.Cmp / And / Not / In / Or over aware datetimes and cents) run by rules.evaluate, then the M8 levels or the M11 chain conjunction. Solver B (`interval_scan`): epoch-minute half-open intervals [start, end + 1) (incl) or [start, end) (excl), cut at the first revocation minute (overrides never close), scanned at the request minute; bands by an integer-cents sign table; set intersection of held scopes down the chain. A third construction table (status flags) steers the samplers and predicts twins; it never sets gold |

### 1.1 Card text (program-written; solver B keeps its own copy and full-matches it)

Instructions = rule block + blank line + question. appr rule block (one line per rule):

    Who holds the accountable (A) role, the approver, for the request at its time:
    - A delegation covers the request when the amount is in its band and the request time is from its start
      time {END}, before any revocation of it.
    - An override covers the request when the amount is in its band and the request time is at or after its
      issue time.
    - The first level with a covering record decides: (a) overrides: the person named by the latest issued;
      (b) delegations: the delegate; (c) otherwise: the person marked A in the standing RACI matrix.
    - If that level gives two different people, the answer is "Escalate: no unique approver". {TIMES}
    - Listing order and who issued a record do not matter.
    The listed records are complete: no other record exists.

agent rule block:

    Whether an agent may use a scope at the time of the request:
    - Each agent holds one grant. An agent may use a scope at an instant exactly when its own grant lists the
      scope, the instant is from the grant's start time {END}, no revocation of that scope from that agent or of
      the whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its
      grant) may use the scope at that instant.
    - {TIMES}
    - Listing order and who issued a revocation do not matter.
    The listed records are complete: no other record exists.

{END}: `incl` "through its end time (the end time is included)"; `excl` "until its end time (the end time is
excluded)". {TIMES}: "Compare times as instants." and, only on rows with the conversion, "Compare times as instants;
a time in another offset shows the same instant in square brackets." No digit appears in card text.

### 1.2 Record block (program-written; state = narrative skin + blank line + block [+ blank line + attack line])

Block = `Records:` line ... `End of records.` line. Styles (sampler-level): `list` and `log`. TIME = a datetime in
a kit form (M2), plus ` [same instant: TIME]` on the conversion; BAND = comparator clause or `of any size`. In log
style every line starts with the time the record takes effect, and its verb says which (starts / issued / made).

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

Section lines in `list`: `Notices:` (or `Notices: none.`), `Revocations:` (or `Revocations: none.`). The chain is read
from BY -> AG in both styles (`sub-agent` in list style is a redundant marker).

## 2. Samplers (>= 4 training shapes + held-out S5)

| Sampler | Shape | Style | Notes |
|---|---|---|---|
| S1 | forward: records drawn independently, target outcome reached by rejection | list | 1-3 delegations, 0-2 notices; agent depth 1-3 (depth 3 weight 15%) |
| S2 | label-first near-miss: record times at T-1 / T / T+1 minute, amounts at band bounds | list | each competitor misses by one condition |
| S3 | config export: larger org (9-12 roles), 2-3 delegations, up to 6 scopes | log | agent depth 1-3 (depth 3 weight 15%) |
| S4 | narrative / transcript: chat, email and transcript skins; conversion on 70% of rows | list | 1-2 delegations, 1-2 notices |
| S5 | held out (mixdev only): held-out skins and registers (runbook, export), offsets +05:45 / -09:30 / +08:45 / +10:30 | log | never a training row |

Depth 3 is capped by M15 (<= 10% of the family; measured 2.5%); the sampler weights only steer it. Cards: (sampler,
track, card 0-5); the card fixes the window-end rule (even incl, odd excl) and its pack (one pack per card, section
7): 48 training cards, about 31 rows per card at 1.5x generation.

## 3. Traps (floors on the family's rows; tags overlap; tags in `meta.edge`; generator check >= 0.75 x target)

| Tag | Target | Construction (measured on 2,000 specs) |
|---|---|---|
| `rev_1min` | 25% | a notice or revocation issued exactly 1 minute before the request (32%) |
| `band_edge` | 20% | request amount equal to a band bound (appr) (22%) |
| `sub_broader` | 20% | a sub-agent's grant lists a scope its parent's grant lacks (25%) |
| `lapsed` | 15% | a delegation or grant whose window ended before the request, or at it under `excl` (34%) |
| `escalate_like` | 10% | two delegations in their window (band ignored), or two overrides issued, at the request: band or level decides whether it is escalate (28%) |
| `inherit_trap`, `notice_after`, `notice_at`, `conversion`, `not_started`, `deep_chain` | report | as named |

Escalate gold is a cap, not a trap: <= 12% of ch_approver rows (section 4). Skins are label-blind; attack lines
(inv twins) never change the gold (M13).

## 4. Balance targets (generator level; c2_select tightens to the spec 3.0 cells)
- Base question forms (share of base specs): ch_approver 39%, yn_holder 21%, yn_agent_ok 22%, ch_scope 18%; with
  partners and twins yes/no is 45-55% of family rows. Gold yes 50% on every yes/no form (label-first target bit;
  generator band 50 +- 3 pp on 2,000 specs).
- ch_approver gold level (share of ch_approver base specs): override 30%, delegation 32%, default 29%, escalate 9%
  (measured 28.5 / 35.2 / 27.6 / 8.7). Binding: escalate gold is 5-12% of all ch_approver rows, partners included
  (measured 6.1%).
- Escalate option: shown on a label-blind 50% of non-escalate ch_approver rows, always when gold; wrong on >= 50% of the
  rows that show it (measured 88%). k = every option shown, escalate included: 3 or 4 by a label-blind draw. A case the
  drawn (k, display) cannot fill is redrawn whole; k and the display are never redrawn (v1 review fix: escalate never
  showed at k = 2). Escalate gold is 16-17% of shown base rows. Gold position uniform per k (kit gold_position).
  ch_scope has no abstain option and no order, so its k may follow the number of distinct wrong scopes (that moves no
  label share).
- Bad outcome = the scope is not usable: `yes_is_bad` False for yn_agent_ok, True for its 3 complements; yn_holder forms
  are neutral. Deep rows <= 10%.
- Length (Qwen3.5-4B tokenizer): row tokens = state + 2 x instructions + options (instructions counted twice by
  convention; the row holds them once). Family mean <= 800 (measured 786); every row <= 2,000.

## 5. Error models (every wrong option; spec 3.0)
Kit-shared names (distractors.CATALOG, no prefix): `ignore_revocation`, `add_exclusive_endpoint` /
`drop_inclusive_endpoint` (band and window ends), `skip_offset_conversion` (compares wall-clock times), `first_match` /
`last_match` (first / last covering record in listing order). Family names carry `t31_`.
ch_approver (solver A with one rule swapped; output = a person; escalate outputs are dropped and the escalate option is
shown only by the label-blind draw): `t31_default_holder`, `ignore_revocation`, `t31_ignore_window_end`,
`t31_future_notice`, the two endpoint models, `t31_ignore_band`, `skip_offset_conversion`, `t31_earliest_override`,
`t31_delegation_beats_override`, `first_match`, `last_match`, `t31_responsible_role` (the first R),
`t31_issuer_as_holder` (the issuer of the latest notice in force).
ch_scope: `t31_ignore_attenuation`, `t31_inherit_parent`, `ignore_revocation`, `t31_future_notice`,
`skip_offset_conversion`; each outputs the first scope it wrongly adds, scanning the deepest grant first (a selection
tie-break only; display order is the kit's label-blind gold position).
yn_holder: on a "no" row the CANDIDATE is the person named by the first error model, in an order seeded by (seed, model
name), that names another matrix person; if none does, the whole case is redrawn. yn_agent "no" rows: no error model;
REQ_SCOPE is drawn label-blind (an own-grant scope made unusable by window, revocation or attenuation; a parent-only
scope (inherit trap); or a scope the agent's grant does not list) and the case is redrawn until the target bit holds.

## 6. Relations (spec 4.1; G-TW 100%)
- Complement on 60% of yes/no base specs: yn_holder -> other (implicit, 60% of its complements) or not (syntactic, 40%);
  yn_agent_ok -> beyond (antonym, 30%), lacks (implicit, 30%), not (syntactic, 40%). Measured: 52% of yes/no rows are in
  a complement pair, 58% of pairs non-syntactic.
- Minimal-edit twin, proposed for 66% of non-ch_scope base specs; twins are 20-25% of family rows (measured 22%). One
  input slot moves and flips exactly one condition of one record: a revocation or override time T-1 <-> T+1 minute, a
  delegation or grant end T-1 <-> T+1, a band bound onto the amount edge, or one scope slot of a chain grant (in or
  out). The prediction comes from the status table with that one flag flipped (never from solver A). A twin is proposed
  only when the gold key changes (another person, or yes <-> no), never when its gold would be escalate (twins never
  raise the escalate share), and never moves a revocation to or before its target's start.
- equiv (11% of bases: another skin and register of the same track), inv (10% of bases: one inert attack line of the
  same track).
- G4 (checked, never emitted): rename the requester (same); shift every time by +97 minutes (same); rewrite the request
  time in another offset (same; a solver check only, so the M2 bracket rule does not apply to it); rename the gold
  person (the new name) or the candidate (same); rename the requesting agent (same); rename the gold scope everywhere
  (ch_scope: the new scope).

## 7. What Haiku writes (after A38; Mode T >= 75%) and the slot list it must keep
- Narrative skins per track: the id carries `appr` or `agent` as a separate part (T31-appr-memo-0007); the plugin picks
  only the row's track (ctx_for), an untagged skin fits both. >= 8 registers: memo, email, chat, ticket, json, yaml,
  log, transcript; held out: runbook, export. Slots: REQUESTER (name, once), ITEM (name, once: the thing requested;
  narrative only, no record uses it), optional REQ_ID (id, at most once). They say who raised which request; never a
  record, time, timestamp, amount, org person, rule, question or outcome. Pool: >= 24 skins per (training register,
  track), >= 12 per (held-out register, track); each skin feeds <= 6 rows, each register <= 15%.
- Question wordings (>= 30; pool target about 170 candidates over the 9 forms, each wording <= 2% of family rows):
  lexicon kind "question", sem q.t31.<qform>. Required slots: yn_holder* CANDIDATE; yn_agent* REQ_AGENT and REQ_SCOPE;
  ch_scope REQ_AGENT; optional REQ_ID. Approver words name the accountable (A) role; a wording asks about the request
  time or names no time (never "now" / "currently"); one negation at most (yn_*_not). G-LEX adds decoy meanings
  (possession: "the agent's own grant lists the scope"; an R person; "other than the default holder"; the present
  moment): a wording any extractor reads as a decoy is rejected for good.
- Band paraphrases: lexicon kind "comparator", slot X cents, 2/2 extraction; each form says whether the bound is
  included ("or less", "at most", "up to and including", "less than", "at least", "or more", "more than", "strictly
  below / above"); bare "under", "over", "below", "above", "up to", "within" are not authored.
- Attack lines per track (slot REQUESTER only): an inert note or a fake authority claim; no record, time, amount or
  other name. Packs: appr = process name + 4 items + 12 role titles; agent = 10-12 scope ids (`resource.action`) + 4
  task items + 6 agent ids; a shared pool of >= 300 invented full names; >= 30 packs per track (24 training + 6 S5
  cards).
- Mode F (<= 25% of rows; about 20% of the skin pool): free-form text per track with REQUESTER, ITEM and REQ_ID verbatim
  (ITEM never after "a" / "an" or at a sentence start; G-SL fact-lock, G3-H). v1 keeps every record line and the card
  program-written: no precedence or window paraphrases (no 3/3 forms).
G-SL exceptions (EXTENDED words skins may use): `approval` and `grant` name the request type and the record type, never
an outcome ("approved", "granted" are CORE and stay banned). Every CORE word stays banned.

## 8. Haiku ambiguity pass: resolutions
Every point is resolved in the body. Map from the pass's point numbers (card = new card text in both solvers' copies;
fmt = record format; gen = generator change; pool = Haiku pools and G-LEX; others are text only):
#1 M2 + 6 (row offset = the request's; the G4 offset rewrite is never emitted) | #2 M2, M5 | #3 M15 | #4 M3
#5 M6, M10, 6 (gen) | #6 M7, M8 (card) | #7 M8 (card) | #8-9 M6, M13 (card) | #10 M6, M10, M13 (card) | #11 1.2 (fmt)
#12 M13 (card) | #13 M6, M10 | #14 M1, M12 | #15 M10 (card) | #16 M10, M12 | #17-18, #22 M12 + 7 (pool: G-LEX decoys)
#19 M9 + 7 (pool) | #20 M9 (card) | #21 7 (pool) | #23 yes means the negated statement holds; one negation (7)
#24 M9 (card) | #25 M5 + 7 (pool) | #26 M5 | #27 M14 | #28 M6 | #29 3 | #30-33 4, 6 | #34 6 (gen) | #35-38 5 | #39 2
#40 header | #41-42 7 | #43 external terms: spec 3.0 (Mode T / F, cards, registers, packs), 6.3 (G-SL, G3-H, G-TW,
G-LEX 2/2 and 3/3), kit README (gold_position, meta.deep / meta.edge, c2_select) | #44 4 | #45 every item of the v1
author list (old section 8) is settled in M1-M16 and sections 2-7.
