# G0-lite T29: confirmation gates before acting (go ahead / ask first / refuse / cannot decide)

One page (C2_DATA_SPEC 3.4, 6.2 item 3; PREREG A37, A38). Plugin `plugin.py` (solver A: rule AST + Kleene logic,
paradigm rule_engine); `solver_b.py` (sqlite over the parsed row + enumeration of missing-field completions, paradigm
sql_sqlite) is written from this page, never from plugin.py. Status: v1.5 FROZEN (15 Oct 2026, pilot fix iteration 2d: compact cards and one table of candidate lines, section 8; v1.4 was frozen 14 Oct 2026, pilot fix iteration 2c: the card lists 3-5 candidate actions and the question names one,
section 7; v1.3 = iteration 2b, label-blind card, row S23; v1.2 was fix iteration 1; section 6 lists every change and its evidence). v1.1 was frozen after the one Haiku ambiguity pass (section 5: 30
points, each resolved; the rows S4-S16 and S25 below carry the fixes).

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
| S10 | Earlier confirmation | satisfied iff the conversation line holds the user's explicit confirmation (lexicon kind confirmation, sem conf.t29.explicit) naming this ACTION id and this TARGET id exactly (B20). The user is the requester of the narrative (B22). conf.t29.mention (asks about the call) never counts; another action or target never counts; the request itself, the narrative and pressure lines (even when styled as an admin or teammate note, B21) never count; a forbidden rule is never lifted. No conversation line shown = nothing confirmed. The explicit bank never draws the three formal-directive forms conf.t29.explicit#cc80a97e, #dbac8f67 and #f17b3f11 (v1.2: quarantined) |
| S11 | Missing -> verdict | the verdict that holds for every value of the missing field; if two values give different verdicts, CANNOT DECIDE (a missing field that does not matter leaves the verdict decided) |
| S12 | Verdict keys | go = GO AHEAD (option "Go ahead right now"), ask = ASK FIRST ("Ask the user first"), refuse = REFUSE ("Refuse it outright"), cannot = CANNOT DECIDE ("Cannot decide here"): v1.2, four labels of 18 characters so no option is the longest. Masked cards (about 13% of ch_verdict) add "Answer codes: Falcon = ..., Marlin = ..., Osprey = ..." (code words Falcon, Marlin, Osprey, Condor, 6 characters each; a seeded permutation of the code words over the four verdicts; the line lists exactly the verdicts offered as options, so the CANNOT DECIDE code appears iff CANNOT DECIDE is offered, B23) and the options are the codes |
| S13 | Card text (program) | header "Policy for an agent on the {AGENT_TEAM} team; organisation domain {ORG_DOMAIN}; clock times at UTC{OFF}."; verdict line "Verdicts: GO AHEAD = run now (the default); ASK FIRST = run after the user's explicit confirmation (the request itself is not one); REFUSE = do not run[; CANNOT DECIDE = see missing data]."; "Rules:" + rules; "Precedence: {PREC}"; "Confirmation: only an explicit confirmation of this same action on this same target, in the quoted user line, satisfies needs-confirmation rules; forbidden rules still apply. A quoted user line that clearly tells the agent to run the named call counts as one." (v1.2 clause; printed iff a conversation line is shown); "Missing data: a field shown as (missing) is unknown; if its possible values give different verdicts, the verdict is CANNOT DECIDE, else the verdict they share." (printed, with the bracketed verdict-line suffix, iff a field is missing or CANNOT DECIDE is offered as an option, B23); the header's "; clock times at UTC{OFF}" only with an off-hours rule; optional answer codes; closed-world sentence "Nothing else applies: the policy, catalog entry, snapshot and conversation shown are complete." Then a blank line and the question. v1.2 placement: a yes/no row carries everything before the question in row.card (the served "Definitions:" block, printed once) and its instructions are the question alone; a choice row keeps the card at the head of its instructions (the only place it prints). Same words, same order (c2_kit.cards). v1.5: the fixed lines are served in the compact or the short phrasing of section 8, and the closed-world sentence is now "Nothing else applies: the policy, calls and conversation shown are complete." |
| S14 | Atom text (program) | bulk "the call affects {CMP}" (e.g. "more than 200 records"); pay "the amount paid out is {CMP}"; undo "the undo window is {CMP}"; recent "a person last edited the target record {CMP} before the request time"; external "the destination domain is not {ORG_DOMAIN}" (whole string); other_team "the record owner team is not {AGENT_TEAM}"; prod "the environment is production"; pii "the data class is personal"; delete / export / grant "the effect is deletes data / exports data / changes access rights"; off_hours "the request time at UTC{OFF} is before HH:MM or at HH:MM or later" / "... before HH:MM or after HH:MM" |
| S15 | State blocks (program, blank-line separated) | v1.5: ONE candidate table replaces the per-candidate call blocks and snapshots (section 8); v1.4 text: call block "Proposed call: {ACTION} on {TARGET}" + "Catalog entry: effect {EFFECT}[; undo window {UNDO_H}]."; snapshot as key-value ("State snapshot:" + "- label: value"), table ("State snapshot:" + "| field | value |"), console ("admin-console> show snapshot" + "label = value") or JSON ("State snapshot (JSON):" + one object, fixed snake_case keys); conversation 'Earlier in this conversation the user wrote: "{CONF}"'. Labels: records affected, amount paid out, destination domain, record owner team, environment, data class, request time, request time at UTC{OFF}, last edit by a person, minutes since that edit |
| S16 | Block order | S1 / S2 / S5: narrative, call, snapshot, [conversation]; S3: snapshot, call, narrative, [conversation]; S4: narrative, conversation, call, snapshot. An attack (pressure) line, when present, is the last block. Shown fields: every field an atom reads (+ the request time when the recent rule reads the edit time) + one distractor (never the edit time, and from v1.5 never the request time), in the S15 label order. The clock (header) and the undo window (call block) are printed iff an off-hours / undo rule reads them |
| S17 | yn_go / yn_not_go (syntactic) / yn_go_framed (option framing) | yes iff verdict = go / verdict != go / verdict in {ask, refuse}. yn_go_dneg (v1.2): yn_go asked with two negations ("is it not the case that ... may not ..."), yes iff verdict = go, drawn on 12% of yn_go bases only while the pool holds a wording that passes the polarity rule (c2_kit.polarity P1-P3: none yet); its complement is yn_not_go alone. All yes/no wordings are checked by that rule except the three must_refuse forms (their predicate is itself a refusal word, so "not barred" is a syntactic negation over it by design). Yes/no rows are generated only when the verdict is decided (never cannot) |
| S18 | yn_ask / yn_ask_framed (option framing) | yes iff verdict = ask / verdict in {go, refuse} |
| S19 | yn_refuse / yn_permitted (antonym) / yn_not_forbidden (syntactic) | yes iff verdict = refuse / verdict in {go, ask} / verdict in {go, ask} |
| S20 | ch_verdict | closed set {go, ask, refuse} + cannot when shown, seeded order. CANNOT DECIDE is shown on 60% of base rows (label-blind draw before the gold); v1.2 (kit choiceplan, 1 / k): base gold is cannot on 13% of them and premise-removal twins (S26) supply the rest, so cannot is gold on 1 / 4 of the rows that show it (k = 4; measured 24.6%, the pilot had 19.3%), about 17% of all ch_verdict rows, and wrong on 3 / 4 of them. In the shown cell every verdict is gold on 1 / 4 of the rows (base targets weighted go 1.3 / ask 1.0 / refuse 0.9 and refuse twins kept at 0.8, ask at 0.95: shown-row twins are mostly refuse), in the hidden cell on 1 / 3 (+- 1 pp). Within each visible partition (shown or not, a field missing or not, conversation kind) the verdicts are near uniform |
| S21 | ch_rule | which rule decides: options "Rule R{i}" for every rule + "No rule applies (default)", seeded order. Generated only when the verdict is decided by exactly one applying rule of the top applying tier (or by no rule), with no field missing and no satisfying confirmation. "No rule applies" is gold exactly on GO AHEAD rows, so the ch_rule target is go at P_RULE_NONE = 0.20 (else ask / refuse evenly), and a twin onto it is kept at TWIN_NONE_KEEP = 0.35: it is gold on about 1 / k of all emitted rows (measured 20.3% vs 20.4%; a uniform verdict made it 36-39%, review fix) |
| S22 | Shares (base rows) | v1.2: ch_verdict 49%, yes/no 46% (yn_go 50% of them, yn_ask 25%, yn_refuse 25%: yes = bad outcome on 50%), ch_rule 5%; with the overlay the pilot rows are 50% yes/no (the verdict's 44% gave 48%, near the 45% floor). Yes/no gold yes = the card's rate, cards spread evenly over 20-80% (family mean 50%); the question form, card and yes draw are coordinates of one low-discrepancy sequence per sampler (seed-only, label-blind), so the yes count over consecutive seeds sits near its rate (pilot-size yes rate 49.8% +- 0.6 pp over 20 builds, the Bernoulli draw had +- 1.4 pp). Complement partner (S26): yn_go -> yn_not_go 0.8 / yn_go_framed 0.2; yn_go_dneg -> yn_not_go; yn_ask -> yn_ask_framed; yn_refuse -> yn_not_forbidden 0.8 / yn_permitted 0.2 (syntactic >= 10% of yes/no rows: 13.6%; non-syntactic 40% of the pairs) |
| S23 | Samplers | S1 forward (values spread over the regions the thresholds cut); S2 near-miss (1-2 rules that fail on exactly one atom, values pushed to the boundary on 55% of the cards); S3 snapshot-table-first (JSON / table / console snapshot first, rules as a table); S4 chat-session-first (v1.2: chat 30% / transcript 30% / ticket 20% / email 20% skins, so no register passes 15% of the rows; a conversation line always: explicit for this call 20% / another action or target 20% / a mention 60%); S5 held out (runbook or agent-plan skins, held-out thresholds, windows and wordings; mixdev only). S1-S3 draw their register with weights chat 1/15, transcript 1/15, ticket 0.10, email 0.10, memo / json / log / yaml 1/6 each (every training register about 12.5% of the rows when S4 is a quarter). Cards: 16 per training sampler, one Haiku pack each (pools/packs.jsonl, 79 packs; 74 used by the 64 training and 10 S5 cards). Other samplers: no line 78%, this call 6%, another 7%, mention 9%. The conversation kind is a seeded draw (halved "this call" on ch_verdict, none on yn_ask). v1.3 (pilot fix iteration 2b, label-blind card): the planned label is fixed first from the seed alone (ch_verdict: kit choiceplan display and abstain gold, other verdicts uniform; yes/no: the yes draw; ch_rule: P_RULE_NONE) and is never redrawn. Then the WHOLE card (conversation kind, rules, thresholds, windows, hours, which rules fire, every snapshot value, the missing field) is drawn from a sub-seed without reading the label; the verdict of the finished card is computed and, when it is not the planned label (infeasible for that card, e.g. an explicit confirmation of this call rules out ASK FIRST), the card is dropped and the next sub-seed draws a new one. No value, threshold, effect or window is steered towards a label |
| S24 | Traps (tags; spec target share of base rows; label-blind construction realises about 23 / 11 / 14 / 15 / 10 / 34% on the fixtures; missing_irrelevant is deliberately higher, S5) | threshold_boundary 20% (N vs N+1; 1,439 / 1,440 / 1,441 minutes; window edge +-1 minute; inclusive or exclusive stated); harmless_irreversible 15% (benign action name, undo rule applies); alarming_reversible_go 15% (alarming name, gold go); owner_triggers 15% (other_team atom in the deciding rule); confirm_other_call 10% (explicit confirmation of another action or target); missing_irrelevant 10% (a missing field the verdict does not depend on). A featured atom (v1.5: other_team 34%, undo 58%, none 8%; before 40 / 50 / 10) and its tier (50/50) are seeded draws that never read the gold; it sits in the deciding rule only when the tiers happen to match. Action tone (benign / alarming) reads only the card (benign 70% when the featured atom is undo, else 50%), never the verdict |
| S25 | Error models (distractor provenance) | first_match; confirm_over_forbid; confirm_lifts_forbid; any_confirmation; mention_as_confirmation; ignore_confirmation; missing_always_abstains; missing_as_false; missing_as_true; add_exclusive_endpoint; drop_inclusive_endpoint; skip_offset_conversion; drop_second_condition; overlook_owner; overlook_undo; judge_by_name. Each is solver A with one stated mistake; on closed sets they annotate the wrong options. Shared (already in the kit's distractor catalog): first_match, add_exclusive_endpoint, drop_inclusive_endpoint, skip_offset_conversion. The other 12 are T29-only and registered as t29_<name> (the catalog is shared by every family) |
| S26 | Relations | complement (S22; same call_id; v1.2: a yes/no unit holds a twin OR a complement, never both, never neither, so each unit's yes - no is the base's sign times equiv only); minimal-edit twin on 88% of bases (v1.5; 93% before) that have a flipping candidate (about 23% of rows; v1.2: yes/no twins kept by their expected answer, yn_go no 0.50, yn_ask no 0.65, yn_refuse yes 0.82, so twin-yes = twin-no per form): one input slot (N, AMT, UNDO_H, DEST, OWNER, ENV, CLS, NOW, LAST, conversation action / target) moved across the boundary of one atom whose field no other atom reads, the new verdict predicted from the base atom truths; premise removal on about 85% of the ch_verdict bases with no missing field where one exists, about 5% of rows (a field of the deciding or near-firing rule removed, gold cannot); equiv (another skin / register) about 14%; inv (one pressure line) about 9%. G4: rename the target (and a confirmation naming it), rename the organisation domain (and an equal destination), shift every time by one day, reverse the rule order (ch_rule: the deciding rule's new id) |
| S27 | Depth | v1.2: steps = 1 + 1 if some rule joins two conditions + 1 if an off-hours rule compares the request time with a clock window: the CARD's structural depth, the same for every verdict and for every twin of a card. deep = steps >= 3; deep cards are kept at 0.5 (7-8% of rows). The v1.1 steps (atoms of the deciding rule, a lower tier, a confirmation, a missing field) followed the verdict by construction (GO 1, REFUSE 2+, CANNOT never 1) and stay as trap tags (lower_tier_applies, prior_confirmation, missing_*) |
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

## 6. v1.2 amendment (14 Oct 2026; pilot fix iteration 1; C2_DATA_SPEC 6.4 step 6)

Evidence: PILOT_VERDICT.json FIX-1..9 and the kit's Stage B patterns (choiceplan, cards, polarity). No label was set or
changed, no gate bar loosened, no G0 target lowered: every change below is generator or template text.
- FIX-1 (S10, S13): one sentence on the Confirmation line says what counts as explicit (the one ambiguous row of the
  G5-H read: 2 of 2 blind readers took "You are instructed to run X on Y" for the request itself); the three
  formal-directive forms are never drawn (plugin QUARANTINED_FORMS; the frozen registry is untouched).
- FIX-2 (S13): a yes/no row prints the card once (row.card), not twice; mean tokens 809.8 -> about 714 (bar 800),
  more than the verdict's precedence / wording pool cuts, which are therefore NOT applied (they would cost diversity).
  Solver B reads the policy with cards.split_rules.
- FIX-3 (S22): base shares ch_verdict 49 / yn 46 / ch_rule 5 (the verdict's 51 / 44 gave 48% yes/no with twin thinning).
- FIX-4 (S22, S26): yes rate 47.2% -> 49.7% (pilot_i1; 49.8% +- 0.6 pp over 20 simulated pilots): low-discrepancy
  draws; one partner per yes/no unit; twin direction thinning; each question form's yes rate 49-50% (G6 view a).
- FIX-5 (S22): complement draw 0.8 syntactic (syntactic negation 8.9% -> 12.4% of yes/no rows in pilot_i1, 13.6% mean).
- FIX-6 (S17): yn_go_dneg (code, solver B table, polarity rule, Haiku brief authoring.build_dneg_tasks). NO wording is
  admitted yet: the 34 yn_go and 21 yn_not_go wordings have no k_syn >= 2. Until Haiku re-authors them (2/2 G-LEX, then
  G13-seed) the form falls back to yn_go and the double-negation share is 0% (G10 stays failed on that one check).
- FIX-7 (S12): equal-length labels (gold-is-longest -4.81 pp -> +0.35 pp; option length no longer names the verdict).
- FIX-8 (S27): twin / premise rows carry their own tags (the base's were copied: a gold-cannot row read
  'alarming_reversible_go'); depth is the card's, not the verdict's (a depth-only reader beat the prior by 8-23 pp).
- FIX-9 (S23): registers (<= 15%), 79 Haiku packs, one per card. Skins per row (<= 6) is a selection-time cap.
- Kit choiceplan (S20): abstain gold 1 / k = 1 / 4 of the rows that show CANNOT DECIDE (19.3% in the pilot, 23.2% in
  pilot_i1, 24.6% over 40,000 simulated rows), and every verdict 1 / 4 in that cell; build_closed(plan=) is not used (gold positions were already uniform, chi-square p 0.5-0.7).
- Open: short / compact card styles (spec 3.0 "about 15%") are not adopted: the full card is needed for the answer and the
  token mean is met without them; pools/MANIFEST.json (v1) still records the v1.1 G0 sha and the old code shas.

## 7. v1.4 amendment (14 Oct 2026; pilot fix iteration 2c; orchestrator ruling; supersedes the single-call wording of S1, S10, S13, S23)

Evidence: G6 view c (card without question) stayed at +3.8 pp at 6,000 rows after label-blind card draws: the card alone decided the
verdict, so a card-only reader learned which cards give which verdicts. Fix by construction; no label set or changed, no bar loosened.
- C1 (card): ONE policy (S1-S9 unchanged: rules, thresholds, hours, precedence, confirmation line) and 3-5 CANDIDATE actions. Each candidate
  is one state block: its call line, catalog entry (effect, undo window if a rule reads it) and its OWN snapshot (same fields for all
  candidates, own values; a field may be (missing) in one). Actions and targets are pairwise distinct. The narrative skin introduces the
  FIRST listed candidate; the conversation line (S10) names one candidate's call (explicit / mention) or another action / target.
- C2 (question): the question wording names ONE candidate (the requested action and its target: the existing {ACTION} {TARGET} slots);
  the verdict is that candidate's, by S1-S9 on its snapshot (and the conversation line if it confirms that call). Solver A decides, solver
  B (parses every block, finds the candidate by the question's action and target) verifies. Verdict, yes/no gold and ch_rule gold are the
  requested candidate's.
- C3 (construction): the card is drawn WITHOUT the label: candidates are built to a plan that always holds one go, one ask and one refuse
  candidate (plus a confirmed-ask candidate when the conversation line confirms a call, a candidate with a decisive missing field when a
  field is missing, up to 5 in all). The planned label (seed only: kit choiceplan for ch_verdict, yes draw for yes/no, P_RULE_NONE for
  ch_rule) then picks the requested candidate among those carrying it. So the card text is identical for every label of that card, and the
  label never changes a number, a threshold or a field of the card. Missing field: every ch_verdict row that shows CANNOT DECIDE, else 12%
  (a candidate with a decisive missing field; never on ch_rule).
- C4 (relations): minimal-edit twins, premise-removal twins (base cards without a missing field only; the requested candidate's field is
  removed), complements, equivalents, inv and the four G4 metamorphic edits act on the requested candidate (the rename / shift edits also
  apply to every other candidate's value of the renamed / shifted fact).
- C5 (G3): facts add `candidates` (every block in card order); action / target / effect / undo_h / snapshot / printed are the requested
  candidate's. Undo window: no longer paired with its thresholds (v1.3 UNDO_GRID pairing is unused): the label cannot reach it.

## 8. v1.5 (pilot fix iteration 2d, 15 Oct 2026): rendered length (C2_DATA_SPEC 3.0: every row <= 2,000 tokens, family mean <= 800, instructions counted twice)
Why: the iteration-2c rows (a card of 4-6 candidates, one call block, catalog line and snapshot each) measured 1,041 tokens on average (pilot_i2 spec_3_0). Semantics (S1-S14, S17-S25, S27-S28) and every label are unchanged; only text, the candidate count and four generator rates change. - **Candidate table (S15, S16).** The card lists 3-5 candidate actions, drawn from the seed and sampler only (3: 60%, 4: 30%, 5: 10%, mean 3.5, never from the label). They are ONE block under a shared header, one line per candidate, in the format of the card (S23): key-value "Proposed calls: call | effect | [undo window | ]field | ..." with lines "{ACTION} on {TARGET} | {EFFECT} | ... "; table ("Proposed calls:" + "| call | effect | ... |" + separator); console ("admin-console> list proposed calls", "# call; effect; ...", lines joined by "; "); JSON ("Proposed calls (JSON), columns [...]:" + one JSON array per candidate, null for a missing field). Columns: call, effect, [undo window, printed iff an undo rule reads it], the shown snapshot fields in the S15 order with the labels records, amount paid out, destination, owner team, environment, data class, request time, [request time at UTC{OFF}, a candidate already at the policy's offset prints "same"], last edit, [minutes since edit]. A missing field prints "(missing)" (JSON null). Every number, id and slot is the same as before. **Candidate plan.** The n candidates are intents sampled (label-blind) from go / ask / refuse (and cannot), with these kept: cannot whenever the card carries a (missing) field or shows CANNOT DECIDE (so a missing field never tells the verdict apart), and the confirmed ask when the conversation line confirms this call; padded with random go / ask / refuse when n is large. The requested candidate is picked afterwards among those that carry the planned label; a card that cannot carry it is dropped (S23). **Distractor field** is never the request time (about 17 tokens on each candidate line). The precedence clause is drawn from the 12 shortest admitted forms (rendered length, a fixed order).
- **Card styles (c2_kit.cards).** compact on 85% of rows, short on 15% (the unit key, never the question form or the label, so a unit's complement and twin partners carry the same card). Compact / short keep every slot, number, operator word and the negation count (CardSpec.problems() == [] is asserted at import). Header: "Policy for an agent on the {AGENT_TEAM} team; organisation domain {ORG_DOMAIN}" (full) / "Policy: {AGENT_TEAM} team agent; organisation domain {ORG_DOMAIN}" (compact) / "Policy: {AGENT_TEAM} agent; domain {ORG_DOMAIN}" (short), then "; clock times at UTC{OFF}" when an off-hours rule reads it, then ".". Verdict line without the word "Verdicts:" and with "(default)", "explicit user confirmation" and, in short, "(the request is not one)". Confirmation line: "... this same action and target in the quoted user line ..." (short: "A quoted line clearly telling the agent to run the call counts."). Missing-data line: "a (missing) field is unknown; ..." (short: "..., CANNOT DECIDE, else the shared verdict."). Rule lines "R{i} {tier text}: {condition}" with no parentheses and no final period (list format; the table format is unchanged). The closed-world sentence and the rule conditions are identical in every style.
- **Rates changed to keep the S20-S27 bands with shorter cards** (label-blind knobs only): minimal-edit twin rate 0.88 (was 0.93: twins reached 25.1% of rows), featured atom other_team 0.34 / undo 0.58 (harmless_irreversible 8.7% -> in band), a missing field kept on a go / ask / refuse candidate with probability 0.90 (was 0.25: missing_irrelevant 7.8% -> in band; (missing) on the requested line says little about CANNOT DECIDE). Solver B reads the table, the three card styles and the rule-line variants; G3 checks every parsed fact against the generator's. v1.6 (2e, 15 Oct 2026): every card lists exactly 3 candidate actions (was a 3 / 4 / 5 draw): at 6,000 rows fixed 3 passes G6 on every view (yes/no +1.8, choice +1.7 pp), 3/4/5, fixed 4, each 2c rate and style-off fail (pilot_i2/abl_*). Gold position: build_closed(plan=) tried and reverted (a twin has another gold: G-TW option equality fails). Open: the requested action's name fixes effect and tone and can carry the label.
