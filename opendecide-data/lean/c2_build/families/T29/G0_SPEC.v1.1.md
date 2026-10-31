# G0-lite T29: confirmation gates before acting (go ahead / ask first / refuse / cannot decide)

One page (C2_DATA_SPEC 3.4, 6.2 item 3; PREREG A37, A38). Plugin `plugin.py` (solver A: rule AST + Kleene logic,
paradigm rule_engine); `solver_b.py` (sqlite over the parsed row + enumeration of missing-field completions, paradigm
sql_sqlite) is written from this page, never from plugin.py. Status: v1.1 FROZEN after the one Haiku ambiguity pass
(section 5: 30 points, each resolved; the rows S4-S16 and S25 below carry the fixes).

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Call | one proposed call: ACTION (id, snake_case action name) on TARGET (id). Catalog entry: EFFECT (closed set: deletes data, changes data, creates data, sends messages, pays money out, exports data, changes access rights) and UNDO_H (count of hours; 0 hours = no undo) |
| S2 | Context | AGENT_TEAM (team set: Finance, Support, Platform, Sales, Legal, Research); ORG_DOMAIN (id; reserved .example / .test host); policy offset OFF (fixed UTC offset; never a zone name, never DST) |
| S3 | Snapshot fields | records affected N (count >= 1; unit record/records); amount paid out AMT (integer cents >= 0); destination domain DEST (id); record owner team OWNER (team set); environment ENV (production, staging, development, sandbox); data class CLS (personal, internal, public); request time NOW (datetime, fixed offset, never missing); last edit by a person LAST (datetime, same offset as NOW) |
| S4 | Printed intermediates | when the card has an off-hours rule and NOW's offset differs from OFF, the snapshot prints "request time at UTC{OFF}" = NOW converted to OFF (the policy clock); the off-hours atom reads that line, else NOW itself (then NOW is already at OFF). When LAST is shown it prints "minutes since that edit" = LAST to NOW in minutes, exact (every time is a whole minute, B1; LAST <= NOW, B2); both "(missing)" when LAST is. Printed values equal the raw fields by construction; solver B re-derives them and a mismatch drops the row |
| S5 | Missing | a field shown as "(missing)" (JSON null) has an unknown value (never "no such value", B2). Whether a row has one is a label-blind draw: every ch_verdict row that shows CANNOT DECIDE has one, other yes/no and ch_verdict rows 12%, ch_rule never. At most one per row and only a snapshot field N, AMT, DEST, OWNER, ENV, CLS or LAST (never NOW, EFFECT, UNDO_H, ACTION, TARGET or a header value, B9). AMT only on calls whose effect is pays money out, DEST only on sends / pays / exports / access calls (B7: EFFECT is always printed; a reader never narrows a missing value by EFFECT). On a row that does not offer CANNOT DECIDE a missing field never changes the verdict (B10) |
| S6 | Atoms (12) | bulk: N {cmp} T. pay: AMT {cmp} T. undo: UNDO_H {cmp} T. recent: minutes since edit {cmp} T. external: DEST != ORG_DOMAIN (whole string; a look-alike is another domain). other_team: OWNER != AGENT_TEAM. prod: ENV = production. pii: CLS = personal. delete / export / grant: EFFECT = deletes data / exports data / changes access rights. off_hours: request time at UTC{OFF} (minute of day, S4) < start, or >= end ("at E or later"), or > end ("after E"). Each atom reads only its own field (B8) |
| S7 | Comparators | lexicon kind comparator, typed forms: cmp.gt (>), cmp.ge (>=), cmp.lt (<), cmp.le (<=). bulk / pay use gt or ge; undo / recent use lt or le. Equality is decisive (A1-A3) |
| S8 | Rules | "R{i} (forbidden): ..." or "R{i} (needs confirmation): ..."; S3 cards may print the same rules as a table "| R{i} | tier | applies when |"; the tier words are exactly "forbidden" and "needs confirmation". A rule is one atom or two atoms joined by " and " over different fields (both must hold); off_hours is one atom and always a rule alone (B17). 3-6 rules, at least one per tier, printed in generation order (tiers interleaved); rule ids R1..Rn follow the printed order. An atom type at most once per tier; it may also sit in the other tier: bulk / pay then need forbidden T > confirmation T, undo / recent forbidden T < confirmation T (both strict on the numbers, whatever the comparators; B16) |
| S9 | Precedence (lexicon kind precedence, sem prec.t29.forbid_confirm_default, 3/3) | REFUSE if a forbidden rule applies; else ASK FIRST if a needs-confirmation rule applies and is not satisfied (S10); else GO AHEAD (default: no rule applies, or every applying needs-confirmation rule is satisfied) |
| S10 | Earlier confirmation | satisfied iff the conversation line holds the user's explicit confirmation (lexicon kind confirmation, sem conf.t29.explicit) naming this ACTION id and this TARGET id exactly (B20). The user is the requester of the narrative (B22). conf.t29.mention (asks about the call) never counts; another action or target never counts; the request itself, the narrative and pressure lines (even when styled as an admin or teammate note, B21) never count; a forbidden rule is never lifted. No conversation line shown = nothing confirmed |
| S11 | Missing -> verdict | the verdict that holds for every value of the missing field; if two values give different verdicts, CANNOT DECIDE (a missing field that does not matter leaves the verdict decided) |
| S12 | Verdict keys | go = GO AHEAD (option "Go ahead now"), ask = ASK FIRST ("Ask the user first"), refuse = REFUSE ("Refuse the call"), cannot = CANNOT DECIDE ("Cannot decide"). Masked cards (about 13% of ch_verdict) add "Answer codes: Kestrel = ..., Marlin = ..., Osprey = ..." (a seeded permutation of the code words over the four verdicts; the line lists exactly the verdicts offered as options, so the CANNOT DECIDE code appears iff CANNOT DECIDE is offered, B23) and the options are the codes |
| S13 | Card text (program) | header "Policy for an agent on the {AGENT_TEAM} team; organisation domain {ORG_DOMAIN}; clock times at UTC{OFF}."; verdict line "Verdicts: GO AHEAD = run now (the default); ASK FIRST = run after the user's explicit confirmation (the request itself is not one); REFUSE = do not run[; CANNOT DECIDE = see missing data]."; "Rules:" + rules; "Precedence: {PREC}"; "Confirmation: only an explicit confirmation of this same action on this same target, in the quoted user line, satisfies needs-confirmation rules; forbidden rules still apply." (printed iff a conversation line is shown); "Missing data: a field shown as (missing) is unknown; if its possible values give different verdicts, the verdict is CANNOT DECIDE, else the verdict they share." (printed, with the bracketed verdict-line suffix, iff a field is missing or CANNOT DECIDE is offered as an option, B23); the header's "; clock times at UTC{OFF}" only with an off-hours rule; optional answer codes; closed-world sentence "Nothing else applies: the policy, catalog entry, snapshot and conversation shown are complete." Then a blank line and the question |
| S14 | Atom text (program) | bulk "the call affects {CMP}" (e.g. "more than 200 records"); pay "the amount paid out is {CMP}"; undo "the undo window is {CMP}"; recent "a person last edited the target record {CMP} before the request time"; external "the destination domain is not {ORG_DOMAIN}" (whole string); other_team "the record owner team is not {AGENT_TEAM}"; prod "the environment is production"; pii "the data class is personal"; delete / export / grant "the effect is deletes data / exports data / changes access rights"; off_hours "the request time at UTC{OFF} is before HH:MM or at HH:MM or later" / "... before HH:MM or after HH:MM" |
| S15 | State blocks (program, blank-line separated) | call block "Proposed call: {ACTION} on {TARGET}" + "Catalog entry: effect {EFFECT}[; undo window {UNDO_H}]."; snapshot as key-value ("State snapshot:" + "- label: value"), table ("State snapshot:" + "| field | value |"), console ("admin-console> show snapshot" + "label = value") or JSON ("State snapshot (JSON):" + one object, fixed snake_case keys); conversation 'Earlier in this conversation the user wrote: "{CONF}"'. Labels: records affected, amount paid out, destination domain, record owner team, environment, data class, request time, request time at UTC{OFF}, last edit by a person, minutes since that edit |
| S16 | Block order | S1 / S2 / S5: narrative, call, snapshot, [conversation]; S3: snapshot, call, narrative, [conversation]; S4: narrative, conversation, call, snapshot. An attack (pressure) line, when present, is the last block. Shown fields: every field an atom reads (+ the request time when the recent rule reads the edit time) + one distractor (never the edit time), in the S15 label order. The clock (header) and the undo window (call block) are printed iff an off-hours / undo rule reads them |
| S17 | yn_go / yn_not_go (syntactic) / yn_go_framed (option framing) | yes iff verdict = go / verdict != go / verdict in {ask, refuse}. Yes/no rows are generated only when the verdict is decided (never cannot) |
| S18 | yn_ask / yn_ask_framed (option framing) | yes iff verdict = ask / verdict in {go, refuse} |
| S19 | yn_refuse / yn_permitted (antonym) / yn_not_forbidden (syntactic) | yes iff verdict = refuse / verdict in {go, ask} / verdict in {go, ask} |
| S20 | ch_verdict | closed set {go, ask, refuse} + cannot when shown, seeded order. CANNOT DECIDE is shown on 60% of base rows (label-blind draw before the gold); base gold is cannot on 5% of them and premise-removal twins (S26) supply the rest, so cannot is gold on about 15% of all ch_verdict rows and wrong on about 80% of the rows that show it. Within each visible partition (shown or not, a field missing or not, conversation kind) the verdicts are near uniform |
| S21 | ch_rule | which rule decides: options "Rule R{i}" for every rule + "No rule applies (default)", seeded order. Generated only when the verdict is decided by exactly one applying rule of the top applying tier (or by no rule), with no field missing and no satisfying confirmation. "No rule applies" is gold exactly on GO AHEAD rows, so the ch_rule target is go at P_RULE_NONE = 0.20 (else ask / refuse evenly), and a twin onto it is kept at TWIN_NONE_KEEP = 0.35: it is gold on about 1 / k of all emitted rows (measured 20.3% vs 20.4%; a uniform verdict made it 36-39%, review fix) |
| S22 | Shares (base rows) | ch_verdict 45%, yes/no 50% (yn_go 50%, yn_ask 25%, yn_refuse 25%: yes = bad outcome on 50%), ch_rule 5%. Yes/no gold yes = the card's rate, cards spread evenly over 20-80% (family mean 50%). Complement partner on 50% of yes/no bases: yn_go -> yn_not_go / yn_go_framed (1:1); yn_ask -> yn_ask_framed; yn_refuse -> yn_permitted / yn_not_forbidden (1:1) |
| S23 | Samplers | S1 forward (values spread over the regions the thresholds cut); S2 label-first near-miss (the deciding rule + 1-2 rules that fail on exactly one atom, values pushed to the boundary); S3 snapshot-table-first (JSON / table / console snapshot first, rules as a table); S4 chat-session-first (chat or transcript skin; a conversation line always: explicit for this call 20% / another action or target 20% / a mention 60%); S5 held out (runbook or agent-plan skins, held-out thresholds, windows and wordings; mixdev only). Other samplers: no line 78%, this call 6%, another 7%, mention 9%. The conversation kind is a seeded draw (halved "this call" on ch_verdict, none on yn_ask) and the target is uniform over the verdicts it allows |
| S24 | Traps (tags; spec target share of base rows; label-blind construction realises about 23 / 11 / 14 / 15 / 10 / 34% on the fixtures; missing_irrelevant is deliberately higher, S5) | threshold_boundary 20% (N vs N+1; 1,439 / 1,440 / 1,441 minutes; window edge +-1 minute; inclusive or exclusive stated); harmless_irreversible 15% (benign action name, undo rule applies); alarming_reversible_go 15% (alarming name, gold go); owner_triggers 15% (other_team atom in the deciding rule); confirm_other_call 10% (explicit confirmation of another action or target); missing_irrelevant 10% (a missing field the verdict does not depend on). A featured atom (other_team 40%, undo 50%, none 10%) and its tier (50/50) are seeded draws that never read the gold; it sits in the deciding rule only when the tiers happen to match. Action tone (benign / alarming) reads only the card (benign 70% when the featured atom is undo, else 50%), never the verdict |
| S25 | Error models (distractor provenance) | first_match; confirm_over_forbid; confirm_lifts_forbid; any_confirmation; mention_as_confirmation; ignore_confirmation; missing_always_abstains; missing_as_false; missing_as_true; add_exclusive_endpoint; drop_inclusive_endpoint; skip_offset_conversion; drop_second_condition; overlook_owner; overlook_undo; judge_by_name. Each is solver A with one stated mistake; on closed sets they annotate the wrong options. Shared (already in the kit's distractor catalog): first_match, add_exclusive_endpoint, drop_inclusive_endpoint, skip_offset_conversion. The other 12 are T29-only and registered as t29_<name> (the catalog is shared by every family) |
| S26 | Relations | complement (S22; same call_id); minimal-edit twin on about 40% of bases (20-25% of rows): one input slot (N, AMT, UNDO_H, DEST, OWNER, ENV, CLS, NOW, LAST, conversation action / target) moved across the boundary of one atom whose field no other atom reads, the new verdict predicted from the base atom truths; premise removal on about 80% of the ch_verdict bases with no missing field where one exists, about 5% of rows (a field of the deciding or near-firing rule removed, gold cannot); equiv (another skin / register) about 14%; inv (one pressure line) about 9%. G4: rename the target (and a confirmation naming it), rename the organisation domain (and an equal destination), shift every time by one day, reverse the rule order (ch_rule: the deciding rule's new id) |
| S27 | Depth | steps = atoms of the deciding rule (go with no applying rule: 1) + 1 if a lower tier also applies under refuse + 1 if a confirmation decides + 1 if a missing field must be resolved. deep = steps >= 3; the generator keeps deep <= 10% |
| S28 | Solvers | A: rules.RuleSet (effect_order: refuse > ask, default go) over a rule AST, rules.evaluate3 (Kleene) for missing fields; exact because a missing field is read by at most one atom per tier and every atom is both satisfiable and falsifiable over its domain. B: sqlite tables (facts, atoms) built from the parsed text; SQL evaluates atoms and rules for every completion of the missing fields over boundary witnesses (N: 1, T-1, T, T+1; AMT and minutes: 0, T-1, T, T+1; categories and domains: the compared value and one other); several verdicts = cannot; its own question table |

## 2. Haiku tasks (after A38 only) and the slots they must keep

- Narrative skins (Mode T, >= 10 registers: memo, chat, ticket, json, email, log, transcript, yaml; held out: runbook,
  plan): must use REQUESTER (name) and REASON (category) exactly once; may use ACTION and TARGET at most once each; no
  blank line; no number, time, quantifier, modal, status or verdict word, negation or operator word outside slots.
- Free-form narratives (Mode F, <= 25%): from a brief with REQUESTER and REASON only; G-SL fact-lock + G3-H.
- Question wordings per question form (lexicon kind question, slots ACTION and TARGET); >= 30 per family.
- Comparator paraphrases (typed: count or cents), precedence paraphrases (3/3 extraction), confirmation phrase bank
  (explicit vs mention, slots ACT and TGT), pressure lines (attack kind; never written as the user; never a
  confirmation), action catalogs (name, effect, tone) and packs (organisation domain, look-alike domains, people,
  target id prefixes). Haiku never sees the policy, the question, the options or the gold.
- `authoring.py` builds these tasks (chunker.make_batch; label words, option texts and the stand-in question strings
  forbidden in every brief) into haiku/author/; the briefs carry the meanings of B15, B20 and B25 verbatim.

## 3. Ambiguity listing (the author's own, written before A38; the Haiku pass is section 5)

A1 "affects more than 200 records" at exactly 200 records? A2 "at least 200 records" at 200? A3 "an undo window of
less than 24 hours" at 24 hours, and does 0 hours mean no undo? A4 "at 18:00 or later" vs "after 18:00" at 18:00?
A5 which clock is compared when the request time has another offset? A6 does a confirmation of the same action on
another target count? A7 does a question or mention count as a confirmation? A8 do a pressure line or an admin note
count? A9 a missing field that cannot change the verdict? A10 may the amount be inferred from the effect when
missing? A11 is a look-alike domain the organisation's domain? A12 "may not run ... straight away": permission or
possibility? A13 when a call is forbidden, must the agent also "ask the user" (yn_ask)? A14 in "which rule decides",
which rule decides when two rules of the top tier apply? A15 does the user's request count as a confirmation?

## 4. Resolution

A1 no (S7, strict). A2 yes. A3 no; 0 hours = no undo and is below every threshold (S1, S7; thresholds >= 1, B14). A4 at E or later
includes E; after E excludes E (S6). A5 the policy clock: the request time at UTC{OFF} (S4, B4). A6 no (S10). A7 no (S10). A8 no (S10). A9 the
verdict stays decided (S11). A10 no; the generator never makes such rows (S5). A11 no, another domain (S6). A12
permission; the wording is admitted only by 2/2 extraction as yn_not_go, else dropped. A13 no: refuse wins (S9, S18).
A14 never generated (S21). A15 no (S10; the verdict line says so). The card prints the rules, precedence,
confirmation and missing-data lines of S12-S15; the semantics it does not spell out are made moot by construction
(B12). GSL_EXCEPTIONS: none. NAME_ALLOW: Agent, User.

## 5. Haiku ambiguity pass and resolutions (B1-B30)

Pass: workflow c2-data-stage-a, task amb:T29 (Haiku, blind; read only this file at sha256 c07d2f6a886e...c9063755;
30 points). Each point is resolved below; code changed only for B23 (plugin + solver B) and B27 (NAME_ALLOW).
- B1 Rounding. Every datetime is a whole minute (seconds are 0: printed ":00" or not printed), so LAST to NOW is an
  exact whole number of minutes; no rounding rule is needed. The printed minutes equal the raw times (S4).
- B2 LAST. Every target record has a last edit by a person at or before NOW (minutes since >= 0; twins and shifts
  keep it so). "(missing)" LAST is unknown, never "no edit"; its values are 0 minutes and up.
- B3 Seconds. NOW has 0 seconds, so the minute-of-day compare is exact (18:00 is minute 1080).
- B4 Clock. "Local" means the policy clock UTC{OFF}: the request time converted to OFF (A5). The card's atom text
  names "the request time at UTC{OFF}"; NOW itself stays in the requester's own offset.
- B5 Offsets. Printed as UTC plus sign, two-digit hours, colon, two-digit minutes (UTC+00:00, UTC+05:30, UTC-05:00);
  whole quarter hours only (generated: +00:00, +01:00, +02:00, -03:00, -05:00, +05:30, +09:00). Datetimes print
  their own offset: ISO "+05:30", log "+0530", text "(UTC+05:30)", or "Z" at +00:00.
- B6 Money. AMT and pay thresholds print as US dollars to the cent ("$1,234.56", "1,234.56 USD", or "$1,234" for a
  whole-dollar value), never as a bare count of cents; "$5,000" = "$5,000.00". "count" / "cents" are slot types.
- B7 AMT / DEST and EFFECT. EFFECT is always printed, so a "(missing)" AMT or DEST reveals nothing new. A call whose
  effect is not pays money out shows amount 0 ($0.00, $0 or 0.00 USD); one that is not send / pay / export / access shows DEST =
  ORG_DOMAIN. These are printed facts, never inferred; missing values are enumerated over their full domain (B11).
- B8 Atoms read their own field only (literal reading). By B7 the literal and the name-implied readings agree on
  every row: a delete call never shows a non-zero amount.
- B9 Only the snapshot fields of S5 can be missing; the catalog line has no "(missing)" form, so S28 holds.
- B10 A missing field on a row without CANNOT DECIDE (yes/no, ch_verdict without it) is always one the verdict does
  not depend on (S11 then gives the shared verdict); CANNOT DECIDE is gold only where it is offered (S20).
- B11 Domains of a missing field: N any whole number >= 1; AMT any amount >= $0.00; minutes since the edit any whole
  number >= 0; DEST any domain; OWNER, ENV, CLS any member of their set. Each printed threshold cuts a domain once,
  so a reader checks each side of each cut; solver B's witnesses are its own technique.
- B12 The card text is not claimed to state S6-S12 verbatim. It prints typed comparator forms (2/2), the precedence
  (3/3), the confirmation and missing-data lines and the closed world; B1, B3, B5, B6 and B7 remove the rest.
- B13 UNDO_H is the catalog length of the period after the call runs in which its effect can be undone, not time
  left at the request. Each card's catalog is its own closed world (another card may differ).
- B14 Zero prints "0 hours" or "zero hours" (= no undo). Every threshold is >= 1 (bulk >= 25 records, pay >= $250.00,
  undo >= 1 hour, recent >= 60 minutes), so 0 hours is below every undo threshold and each atom is satisfiable and
  falsifiable (S28).
- B15 Comparators: gt = strictly more (more than, over, above, in excess of, exceeding); ge = the bound or more (at
  least, X or more, no fewer than, no less than); lt = strictly less (less than, under, below); le = the bound or less
  (at most, X or less, no more than, not more than). Forms with an unclear endpoint (up to, within, around, about)
  are not authored and fail 2/2. "Equality is decisive": at value = T, gt and lt are false, ge and le true.
- B16 S8 thresholds are strict on the numbers; "in both tiers" is a permission. Undo / recent: the narrower window
  is forbidden, the wider needs confirmation (the generator redraws otherwise).
- B17 off_hours is one atom (one condition with an inner "or"), always alone in its rule, counted once (S8, S27).
  Windows: start < end, both 00:00-23:59, never overnight, never 24:00 (generated: 08:00-18:00, 07:00-19:00,
  09:00-17:00, 06:00-22:00, 08:30-17:30; S5 07:30-20:00).
- B18 Rule order: generation order, tiers interleaved; ids R1..Rn as printed; tier words fixed (S8).
- B19 Precedence is fixed on every card (S9). "default" in the sem id names the GO AHEAD default, not a default
  precedence; each card prints one 3/3-admitted paraphrase of this same precedence.
- B20 The conversation line names the action and the target by their exact ids (slots ACT, TGT); no display name.
  Explicit = an unconditional, affirmative go-on of that call: no question, condition or negation. Mention = asks
  about or refers to the call without agreeing. Mixed, conditional or negated lines are not authored and fail 2/2.
  "Earlier in this conversation" places the line before the proposed call in time, whatever the block order.
- B21 "Notes" in S10 = pressure (attack) lines, which may be styled as an admin or teammate note; none counts (A8).
- B22 The user is the requester named in the narrative (one conversation, one user); pressure lines come from others.
- B23 Masked codes list exactly the offered verdicts (CANNOT DECIDE's code iff CANNOT DECIDE is an option); the
  missing-data line and the verdict-line suffix print iff a field is missing or CANNOT DECIDE is offered (S12, S13).
- B24 An unprinted field is read by no rule (S16), so it has no effect; it is not unknown. Closed world as printed.
- B25 Question meanings: yn_go "may the agent run the call straight away, with no further step"; yn_not_go its
  syntactic negation; yn_go_framed names both other outcomes (hold for the user's confirmation, or decline
  outright) and asks if one of them is the result; yn_ask "is holding the call for the user's explicit confirmation
  the required step" (no on refuse, A13); yn_ask_framed names run-straight-away and decline-outright; yn_refuse
  "must the agent decline the call outright"; yn_permitted "does the policy allow the call at all, straight away or
  after confirmation" (antonym, no negation); yn_not_forbidden "is the call not barred" (one syntactic negation).
  "Option framing" = the question text itself names the outcomes. Every wording needs 2/2 extraction to these.
- B26 "No rule applies (default)" = no rule applies, so the default GO AHEAD holds. ch_rule asks for the single
  applying rule of the top applying tier; a lower-tier rule never decides (S21 generates only such rows).
- B27 "Ops" is removed from NAME_ALLOW; skins may capitalise only Agent and User besides sentence starts.
- B28 S25 now names the 4 shared and 12 T29-only error models.
- B29 Patched before freezing; T29Plugin.G0_SHA256 holds this version's sha256.
- B30 Process note on the reader's tooling; no spec change.
Frozen; the sha256 is T29Plugin.G0_SHA256 and validate_plugin() refuses the plugin if this file changes.
