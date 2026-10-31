# F3 `gen3_state_track`: notes for decide2 (builder B), devx (reviewer R) and review

**Builder:** C.
**Code:**
- `golden_src/gen3/gen3_state_track.py` builds the rows: formats, views, balance and planning.
- `golden_src/gen3/gen3_state_track_sim.py` holds the machines, the event sampler and the labels (`decide`).

**Tests:** `yn2b/tests/test_gen3_state_track_{sim,render,build}.py`.

This note describes the **rendered surface only**, meaning what a row shows. It does not describe how `decide` is coded.
Every rule a solver needs is printed in the row itself, as numbered and dated rules. For yes/no rows, some rules are
also printed in the card.

## 1. Rows

| | Train (SPEC 3) | dev_iid | dev_holdout |
|---|---|---|---|
| yes/no | 1,700 (about 340 are judge rows) | 85 | 85 |
| choice | 950 (+150 JB-letter) | 47 (+8 JB) | 47 (+8 JB) |
| score | 700 | 35 | 35 |
| attack twins (`inv`) | 280 (8%) | 0 | 0 |

- Train is built from 8 machines: orders, tickets, access, inventory, bookings, ledger, dialogue and agent.
- dev_holdout is built only from the 2 held-out machines: `flags` (feature flags) and `docs` (document versions).
- dev_iid uses the training machines, a new seed stream and a disjoint name pool.
- devx is not built here. R renders it from `gen3_state_track.export_latents("devx", 100)`:
  - the latents are typed worlds of the held-out machines;
  - each comes with a query and its gold from `decide`.

`meta.pack` is the machine name. `meta.n_events` is the number of event lines in the row.

## 2. State layout (16 formats; `meta.fmt`)

Every state holds the same parts, in this order:
1. title;
2. context lines, including `log exported at`;
3. the numbered rules, `R<i> (in force from YYYY-MM-DD) <text>`;
4. the starting state (entities and their fields at the starting time);
5. the events;
6. for judge rows only, the agent record;
7. the notes.

**Notes are an untrusted sub-field.** Attack plants appear only there, as the last note.

Each event has four parts:
- a time;
- an id: `E####`; `M###` for chat messages; `C###` for tool calls;
- a source or actor;
- one line of text.

### How each format prints the events

| fmt | Events appear as | Listing order |
|---|---|---|
| `json`, `json:newest` | `"events": [{"time","id","by","event"}]`. Top-level keys are always: title, context, rules, starting_state, events, agent_record (null if none), notes | time order / newest first |
| `kv` | `events.<n>.time/id/by/event: ...` | time order |
| `markdown`, `markdown:shuffled` | `## Events` bullets: `<time> \| <id> \| <by> \| <text>` | time order / shuffled |
| `log:chrono`, `log:newest`, `log:shuffled`, `log:grouped` | after `Event log:`, lines `<time> [<by>] #<id> <text>`. `grouped` prints `== <by> ==` blocks with lines `<time> #<id> <text>` | as named (grouped: by source, time order inside) |
| `email:chrono`, `email:newest` | after `Message thread:`, blocks with `From: <by>`, `Date: <time>`, `Subject: event <id>`, then the text. Blocks are separated by a line of 10 dashes | time order / newest first |
| `chat` | after `Transcript:`, lines `[<time>] <by> (<id>): <text>` | time order |
| `table:md`, `table:csv`, `table:records` | after `Event table:`, columns time, id, by, event | time order / shuffled / newest first |
| `prose` | after `What happened:`, sentences `At <time>, <by> logged <id>: <text>` (4 per paragraph). A period is added after any text that does not already end in `.`, `?` or `!`, so a structured line reads `... order=SO-4417203.` | time order |

### Times

- Times are ISO (`2026-03-14T09:05:00Z` or with an offset, `+01:00`) or space style (`2026-03-14 09:05 UTC+01:00`).
- In `mixed` worlds, different sources print different UTC offsets. The rules say to compare in UTC.
- All times are unique within a row, so the time order is always recoverable.
- Events take effect in time order whatever the listing order. This is the display-order trap.

**Parse reference.** `events_back()` in `yn2b/tests/test_gen3_state_track_render.py` parses the events back out of
every format. It is test code only, and it is tested on every format.

## 3. Questions, time and answers

**The time.** A question asks about either:
- "at the end of the log", which for dialogue is "... of the chat" and for agent is "... of the session"; or
- "at <ISO time Z>".

Events after that time do not count. An event exactly at that time counts.

**Answer spaces:**

| Question type | Answer space |
|---|---|
| yes/no | options `yes`/`no` in the raw rows; golden `noul` rows get gold 1/0 |
| choice (value) | the observable's option text: a status name, a person, `N units`, a money amount such as `1,234.50 EUR`, a slot value, a folder, a content label, `N%`. The options are 4 to 7 of these. |
| mirror | like choice. 20% of mirrors offer `None of these`, always as the last of exactly 4 options, and it is the gold in 25% of those |
| score | the level texts, in ascending order |
| JB-letter | `[yes-description, no-description]`, or the adapter fallback pair. With the fallback pair (20% of JB rows) the question states the proposition: "Under the numbered rules, does this statement hold? <yes-description>" |

**Choice cards.** A choice card defines option lines only, for example status meanings. The option key is the exact
option text.

**Yes/no cards.**
- A yes/no card says what yes and no mean.
- Dialogue cards also define "same as before" and "not X".

**Question families per machine:**

| Machine | Yes/no | Choice | Score |
|---|---|---|---|
| orders | in status S / can still be cancelled | status | how many listed orders are shipped or delivered (K = n+1) |
| tickets | is <person> the owner / overdue under the SLA | owner | escalation level 0-4 |
| access | can <person> edit / view | access level (no access, viewer, editor, owner, blocked by a deny) | how many tracked people can edit (K = n+1) |
| inventory | at least N units available | available units | availability band |
| bookings | does <person> hold the confirmed booking / is the slot free for a new hold | who holds the confirmed booking | how many listed slots are booked (K = n+1) |
| ledger | available balance at least X | posted balance | available-balance band |
| dialogue | is the slot value V | slot value | – |
| agent (cart) | cart holds at least N of the SKU | quantity | how many listed items have quantity at least 1 |
| agent (files) | file in folder F | folder | how many listed files are in archive |
| flags (held out) | flag on for <person> in production | production rollout % | rollout band |
| docs (held out) | current content is L / current version approved | current content | number of versions |

**Ladder rows.** A ladder row (polarity 1, role `neg`) asks the inverted question: "... other than S", "... unable
to ...", and so on. It is in a `complement` relation with the row that has the same state.

**Judge rows** (`meta.judge` true) carry an agent record: "Agent record (written at <time>)", with 2 or 3 lines of the
form `<label>: <value>`.
- They ask whether the record is consistent with, or supported by, the log under the rules.
- Gold is yes only if every recorded value equals the rules' value at the record time.
- A no record has exactly one controlled error. That error is usually a value a shortcut solver would produce.

## 4. Event language (each line maps to exactly one typed update)

Structured lines are `kind key=value ...`. For example:
- `ship order=SO-4417203`
- `grant role=editor to=... resource=RES-... hours=2`
- `hold sku=SKU-... qty=3 minutes=30`

Language lines use a small fixed set of templates per kind. The rules of each machine list the mapping, for example
"a payment line is pay". The templates are in `TXT` in the sim module.

**Special cases:**
- **agent:** each line is `<tool call>(...) -> ok | error: <reason> | partial: <item> ok, <item> failed, ...`. Only the
  parts reported ok take effect.
- **dialogue:**
  - Customer and Assistant messages; a message's id is `M###`.
  - Messages about "my other booking <ref>" name another booking.
  - Proposals, a "no" to a proposal, and other people's wishes change nothing.
- **Look-alike ids** differ from the queried id by two swapped adjacent digits, for example `SO-4417203` and
  `SO-4417230`. They are either:
  - another listed entity; or
  - an unlisted id, and then the event changes nothing.

## 5. Shortcut solvers (tiers, distractors and checks only; never labels)

`meta.shortcut_hits[name]` is 1 when that solver gives the gold answer on the row.

**A solver abstains (and is absent from `shortcut_hits`) when its trap is absent from the row.** The traps are:

| Solver | Its trap |
|---|---|
| `ignore_guards` | a guard-failing request, a failed tool part, a proposal or someone else's wish |
| `apply_resends_twice` | a redelivered id |
| `display_order` | a listing order that differs from time order (depends on the row's format) |
| `ignore_expiry` | an expiring hold, grant, authorisation, override or lock |
| `fuzzy_entity_id` | an event naming a look-alike id |
| `last_event_wins` | 2 or more events name the queried entity |

This is how SPEC 4.7's "no shortcut above 60%" is measured here: on the rows where the solver's trap is present. A solver
that answers every row would agree with gold wherever its trap is absent. The builder also reports each solver's
accuracy on all rows as a whole.

## 6. SPEC points settled here

1. **Judge rows.**
   - SPEC F3 says "300 of these are judge rows", and SPEC 4.7 says judge is 20% of latents.
   - With the view shares of SPEC 4.2, F3 needs about 1,700 latents, so the judge tier gives about 341 judge rows.
   - I kept the 20% judge tier and the exact yes/no total of 1,700, so judge rows are about 341 instead of 300.
2. **View shares.**
   - Contrast twins: 55% of non-judge latents.
   - Ladder: 30% of the non-judge yes/no latents.
   - Format twins: 30% of non-judge latents.
   - Mirrors: 30% of yes/no and judge latents.
   - Judge latents get no contrast, ladder or format twin, which keeps judge rows near the SPEC's 300.
   - The row totals per question type are exact (§1).
3. **Revert meaning.** Revert meaning is stated per machine in its rules:
   - orders, tickets, bookings and flags **restore** the values before the reverted event;
   - inventory, ledger and agent **undo that event's own change**. Later events keep their effect, and quantities never
     go below 0.
4. **Expiry at the exact boundary.** Holds, grants, authorisations, overrides and locks stop counting AT their end time
   (`hc:boundary_exact` cases exist).
5. **Event exactly at the stated time.** It counts.
6. **Redeliveries.** "Takes effect at most once" means: a later line with an id that already took effect changes
   nothing. Redeliveries are only generated for events that took effect.
7. **Dialogue "not X".** If X was the slot's value, or the slot had none, it takes the single remaining allowed value;
   otherwise it has no value. An item whose queried value is open is rejected.
8. **JB rows** may use a different format from their unit's base row. They are a separate view, and this keeps the JB
   artefact probe balanced per format.
9. **Attack plants** go in the notes (channel `log_note`). F3 has no marker spoofing (SPEC 4.8).
10. **Artefact correlations on dev.** The dev part has 16 JB rows, so |corr| < 0.05 is not a meaningful gate there. The
    report shows the dev correlations; the gate is applied on train.
11. **Held-out wording.** The held-out machines (flags, docs) word the shared rules in their own way; no rule sentence
    is shared with any train state (tested). dev_holdout also uses held-out generic phrasings (`jdg.h`, `jb.h`,
    `jbf.h`) that train and dev_iid never use.
12. **Calendar tool calls** (SPEC lists files, a calendar or a cart) are not built. The agent machine covers the cart
    and file-store tools.
