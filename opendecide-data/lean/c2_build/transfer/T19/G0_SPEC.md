# G0-lite T19: compliance checklist with scope exclusions and evidence expiry (transfer dev only)

C2_DATA_SPEC 2.2 (T19, 300 items, held out, never trained) and 3.20 (a boolean evaluator plus SQL); rules for every
family in 3.0 and 4.1. It tests transfer of ordered gates (T15), expiry (T23) and abstain (T25, T29).
**Status: FROZEN v1.2 (14 Oct 2026)** = v1.1 (13 Oct: v1 sha256 40ba2f84...1170 + the one blind Haiku ambiguity pass, workflow
c2-data-stage-a, task `amb:T19`, 29 points in haiku/ambiguity/amb_T19_points.json, resolved in section 8) + Stage B pilot fix
iteration 1 (section 9: S16 card placement and styles, S17 evidence kinds first, the 1/3 abstain band, twins, yn_dneg, wording
polarity). No gold rule (S1-S7, S12-S14) changes. The v1.1 text the Haiku task files and pools_v2 were authored under is kept
byte-exact in G0_SPEC.v1_1.md (plugin.T19Plugin.G0_SHA256_AUTHORED). sha256 in plugin.T19Plugin.G0_SHA256, pass id in
G0_HAIKU_TASK. Code: plugin.py (solver A), solver_b.py (solver B, a separate file written from this page), fixtures.py (test
stand-ins), haiku_author.py + authoring_i1.py (Haiku authoring tasks and loaders). Every row is dev-only (meta.dev_only =
true). The T19 rules are this page plus the card (1.2; a test checks it equals plugin.CARD_SPEC and solver_b). Other names (G2-G4,
G-SL, G-TW, G-LEX, G3-H, equiv, inv, the overlay report) are the C2_DATA_SPEC 4.1 and 6.3 gates.

## 1. Semantics table (exact)

Letters: A = the audit date; D = an evidence date; N = a validity in days; E = D + N, the last valid day.

| # | Item | Semantics |
|---|---|---|
| S1 | Facts | A site (name) with a profile of exactly one value per attribute: hosting (cloud / on-premises / hybrid), data handled (public / internal / personal data / payment data), site type (office / warehouse / data centre / store); an auditor (name); 3-5 controls in a listed order; one evidence log line per control, in the same order; the audit date A. Site, auditor and control names come from the card's pack (section 6) |
| S2 | Control | id = two capital letters, a hyphen and a number 1-40 ("AC-7"; unique in a row); a name; a scope: every site, or the sites whose ATTR (one profile attribute) is one of 1-2 listed values; at most one exclusion "except sites whose ATTR2 is V", ATTR2 a profile attribute other than ATTR (any of the three on an every-site control); validity N days, N in {30, 60, 90, 180, 365} |
| S3 | Applies | (every site, or the profile's ATTR value is listed) and not (the profile's ATTR2 value is V). An exclusion turns an every-site control off too |
| S4 | Validity | Calendar days. Evidence dated D valid for N days covers every date from D through E = D + N inclusive: E still counts, E + 1 has expired. Every D is before A (S14 guard; the card says so), so only the window's end can decide. Generated dates lie in Nov 2024 - Dec 2026 and no window holds 29 February, so N = 365 also equals "the same date a year later" |
| S5 | Control result | Not applying: na, a fourth state the fold skips. Applying: dated evidence -> pass iff A <= E, else fail; "no evidence on file" -> fail; "evidence on file, date not recorded" -> unknown |
| S6 | Verdict (as at A) | compliant iff every applying control passes; non-compliant iff at least one applying control fails (whatever else is unknown); otherwise (no fail, some unknown) cannot be determined (key `undetermined`). Every site has an applying control (S14), so no verdict is vacuous |
| S7 | First gap | The first applying control, in checklist order, whose result is fail; asked only when the site is non-compliant and no applying control before it is unknown |
| S8 | Closed world | The card's last line, on every row: "The profile, the checklist and the evidence log are complete: nothing else changes the answer." |
| S9 | yes/no | Asked only on determinable rows. yn_compliant: yes iff compliant. yn_dneg (v1.2): yes iff compliant, two syntactic cues (the frame "is it not the case that" + one "not"); drawn only once a clean wording is admitted; its one partner is yn_not_compliant. Complements, yes iff non-compliant: yn_out_of (antonym, 0 negation cues), yn_not_compliant (syntactic, exactly 1 cue), yn_fails (implicit, exactly 1 implicit cue such as "fail to meet"). Every wording asks about the whole site against the checklist on the audit date and reads with its form's polarity (c2_kit.polarity, R3) |
| S10 | ch_verdict | Options Compliant / Non-compliant / Cannot be determined from the records, all three on every ch_verdict row; no other form shows an abstain option. Each label is gold on 1/3 of the rows (section 3) |
| S11 | ch_gap | Options: every listed control id (the id alone, as printed); gold = S7 |
| S12 | Solver A | rule_engine: per control a scope AST (rules.And / Not / In over the profile slots) run by rules.evaluate3; only when it is True, a pass AST (rules.Cmp(A <= Fn add_days(D, N)); Lit(False) for no evidence) run by evaluate3 (Kleene: an unrecorded date is unknown; exact, as each such date is free before A and sits in one test only, so pass and fail are both reachable). Verdict and gap are folded from na / pass / fail / unknown |
| S13 | Solver B | sql_sqlite (solver_b.py): its own card copy and regexes parse the RENDERED row into sqlite tables profile / control / scope; one CASE query gives every status (EXISTS joins for scope and exclusion; evidence 'none' -> fail, 'unknown' (ev NULL) -> unknown, else date(ev, '+N days') >= A); aggregates give the verdict, ORDER BY ord the gap. A printed E must equal sqlite's date(D, '+N days') and every D must be before A, else ParseError |
| S14 | Guards | Construction _status_c() (set membership, timedelta) = the planned statuses = solver A; ids as S2; ATTR2 != ATTR; every D < A; >= 1 applying control. A failed guard redraws the spec. A solver A / B disagreement or a solver B error fails G2 (bar 100%) and drops the whole relation unit: a row is never kept on solver A's word |
| S15 | Depth | Unstated operations: 2 (scope, validity) when every dated evidence line prints "(last valid day E)", E the computed date (never the text "D + N"); 3 on deep rows, which print no E. Deep is a row flag drawn once per (sampler, seed), i.e. per item: uhash < 0.08 (about 8%; spec 3.0 cap 10%) |
| S16 | Card placement and styles (v1.2) | the card (1.2) is printed once: in `row.card` on a yes/no row, at the head of the instructions (then a blank line and the wording) on a choice row, because the served prompt prints `row.card` once on a yes/no row and the instructions twice (spec 3.0: mean <= 800 rendered tokens; pilot 0 read 1,074.6, the fix about 775). Two styles, drawn from the seed and the sampler only (one per relation unit): full 85%, short 15% (spec 3.0 "a short or no card on about 15% of rows"; no "none" style). The short style words three items more tersely (1.2) and changes no rule. Two items depend on the question form, a visible input (never the gold): [undetermined] only on ch_verdict rows, [gap] only on ch_gap rows. `meta.defs_style` = `rules_in_card_<style>` / `rules_in_instructions_<style>`. H10 (one value per attribute) is shown by the profile block (one line per attribute); its card sentence is dropped |
| S17 | Evidence kinds first (v1.2) | a row draws the evidence KIND of each control (dated .76 / none on file .11 / date not recorded .13; a ch_verdict row always holds one unrecorded date and one dated line) from one distribution for every verdict target, then fits the statuses to the kinds (section 2): the count, length and numbers of the evidence lines carry no verdict (pilot 0 G6: the none / unrecorded lines gave n_numbers + qform 0.59) |

### 1.1 Program text

State: narrative skin (one block, no empty line); blank line; profile block ("Site profile for SITE:" + three
"- attribute: value" lines (S1, S2, S4); a two-column table (S3); an "export site_profile:" block (S5)); blank line;
"Checklist:" + one line per control "- ID NAME: SCOPE[, except sites whose ATTR2 is V3]; evidence valid for N days."
(v1.2; v1.1: "its evidence stays valid for N days after the evidence date.") with SCOPE = "applies to every site" or "applies to sites whose ATTR is V1[ or V2]"
(the exclusion may follow either); blank line; "Evidence log:" + one line per control in checklist order ("- ID:
evidence dated D[ (last valid day E)]" | "- ID: no evidence on file" | "- ID: evidence on file, date not recorded");
blank line; "Audit date: A"; on an inv row, a blank line and one attack line. Rules and question: S16 (card, then on a
choice row a blank line, then the wording). Only the profile block changes with the layout; checklist and evidence log keep one shared
order in every layout, and G4's reversal reverses both. Dates (D, E, A) print in one kit form per row (choose_forms,
label-blind): 2026-03-14, 14 March 2026, March 14, 2026, 14 Mar 2026, Saturday, 14 March 2026 or Saturday, March 14,
2026; never a numeric day/month form. N prints as digits ("365 days").

### 1.2 The card (verbatim; plugin.CARD_ITEMS = solver_b = these blocks; items in order, then the closed-world line)

```text
Rules:
- [scope] A control applies when the profile shows one of its listed values for the named attribute or when it is for every site, unless the profile shows its excluded value.
- [window] Evidence dated D valid for N days covers each calendar date from D through D + N, and has expired from the next day on. Every evidence date is earlier than the audit date.
- [result] An applying control passes when its evidence covers the audit date, fails when that evidence has expired or none is on file, and is unknown when its evidence date is not recorded.
- [verdict] The site is compliant on the audit date when every applying control passes, and non-compliant when at least one fails.
- [undetermined] When none fails but some applying control's result is unknown, compliance cannot be determined.
- [gap] The first gap is the first applying control, in the listed order, that fails.
The profile, the checklist and the evidence log are complete: nothing else changes the answer.
```

The "[..]" tags are not printed. [undetermined] is on ch_verdict rows only, [gap] on ch_gap rows only. Short style (15%) words these items:

```text
- [window] Evidence dated D valid for N days covers each calendar date from D through D + N, and has expired the next day. Every evidence date is earlier than the audit date.
- [result] An applying control passes when its evidence covers the audit date, fails when it has expired or none is on file, and is unknown when its date is not recorded.
- [undetermined] When none fails but some result is unknown, compliance cannot be determined.
```

## 2. Samplers (all dev-only)

S1 forward (list layout); S2 label-first boundaries; S3 profile as a table; S4 auditor's narrative (every S4 row's
narrative is a Mode F text: plugin.ctx_for); S5 held out (export layout, held-out registers regulator_letter and
handover_note, held-out packs; Mode T). S1-S3 and S5 use Mode T skins, so Mode F is about 20% of items (cap 25%).
Evidence and statuses (S17): kinds first, then statuses fitted to the kinds and the target. Compliant: each dated control is pass
(p .65), else na, one pass forced; undetermined: each unrecorded-date control is unknown (p .65) or na, one forced, dated ones as
in compliant; non-compliant: 75% (not ch_gap) one dated fail, no unknown, the other dated controls pass (p .65) or na, else dated
-> pass .45 / fail .25 / na .30, none on file -> fail .6, unrecorded -> unknown .65, one fail forced; ch_gap turns each unknown
before the first fail into na and needs >= 2 applying controls. Each control's scope, exclusion and date are then drawn to
realise its status. Controls per row: 3, 3, 4, 4 or 5 (mean 3.8; v1.1 mean 4.0). Boundary controls: each dated control is one
with probability 0.5 in S2 and 0.25 elsewhere (a per-control draw, no rounding): a passing one ends exactly on A (E = A), a
failing one the day before (E = A - 1).

## 3. Traps and balance

Tags: expiry_boundary (an applying control's E is A or A - 1), exclusion_decides, expired_but_out_of_scope,
unknown_out_of_scope, unknown_with_fail (non-compliant, not undetermined). Base form per item: the seeds of a sampler run in
balance cycles of 72 (plugin.CYCLE; 900000, pilot.SEED_BASE, is a multiple), each holding in a seeded order 14 ch_verdict pairs,
8 ch_gap pairs and 14 yes/no pairs (39 / 22 / 39% of the bases; v1.1: 30 / 15 / 55%). Yes/no: 7 pairs ask yn_compliant (or, once
admitted, yn_dneg for 10% of them), 7 a complement form (one of the three, uniformly, per seed); the two seeds of a pair take
opposite verdicts, so a pair holds exactly one gold yes and one gold no, and polarity 50 / 50 with compliant and non-compliant
ROWS equally many (twin yields matched, section 5) means the question's form alone never predicts the answer (pilot 0 G6
a_question). ch_verdict: the 28 seeds of a cycle take the targets abstain 12 / compliant 8 / non-compliant 8 (c2_kit.choiceplan's abstain plan, exact per cycle; base share .43;
the twins dilute it so the abstain option is gold on 1/3 of the ROWS, as are the other two; measured .342 / .319 / .339 on 3,001
rows), abstain always shown (k = 3), wrong on 2/3 (bar >= 50%). ch_gap is chosen first and its spec redrawn until S7 holds.

## 4. Error models (prefix t19_; each is solver A with one switch)

ignore_scope (every control applies), ignore_exclusion, expiry_exclusive (E already expired), unknown_as_fail,
unknown_as_pass, abstain_on_unknown (any unknown -> undetermined, even beside a fail), first_expired_listed (ch_gap: the
first listed control whose dated evidence has expired by A or that has no evidence on file, scope ignored; "date not
recorded" never counts), last_gap (ch_gap: the last applying control that fails).

## 5. Relations (G-TW 100%)

- Complement: a yes/no base gets a partner row with probability 0.6 (a yn_compliant base -> one complement form; a complement
  base -> yn_compliant; a yn_dneg base -> yn_not_compliant, one cue more or less).
- Minimal-edit twin (own call_id), where one exists. yes/no and ch_verdict: (a) non-compliant with exactly one fail, dated, and no
  unknown (80% of them): its D moves to A - N (E = A) -> compliant, kept with probability .68; (b) compliant: one dated passing
  control, picked by a seeded hash, moves to D = A - N - 1 (E = A - 1) -> non-compliant, kept with probability .56 (thinned so
  compliant and non-compliant rows stay equally many). The abstain gold has no twin. ch_gap (kept .60): (a) a dated passing
  control listed before the first gap moves to E = A - 1 and becomes the gap; else (b) the first gap moves to E = A and the next
  failing control, with no unknown before it, becomes the gap. The prediction comes from the construction; E, tags and depth are
  recomputed (derive); G-TW checks that one input slot changed. Twins are 20-25% of the rows (measured 22.3%).
- equiv 12% (another profile layout and another skin of the same mode), inv 8% (one attack line).
- G4: rename the site; shift every date by 14 days; reverse the checklist and evidence log order (not on ch_gap).

## 6. What Haiku writes (after A38; T19's own registers, never trained); tasks and loaders in haiku_author.py

- Packs: 40 (8 held out, S5 cards only). A pack is an invented organisation that runs audited sites: 4 site names, 4
  auditor (person) names, 8 control names (lower case, 2-4 words). One pack per card, 12 cards per sampler: S1-S4
  cards take the 32 training packs in turn, S5 cards the held-out ones. plugin.validate_pack: no digit, negation,
  label, status, number, time, quantity, quantifier, modal, hedge or operator word; a site name names no profile value.
- Mode T narrative skins: 12 per training register (audit_memo, auditor_email, audit_chat, audit_ticket,
  checklist_note, meeting_notes, report, site_wiki; S1-S3) and 16 per held-out register (regulator_letter,
  handover_note; S5). {SITE} and {AUDITOR} each exactly once per skin; one block, no empty line; G-SL role skin.
- Mode F narratives (S4): 4 per training register, from a facts-only brief (an invented site name and auditor name,
  each kept verbatim); G-SL lint_freeform and G3-H (auditor).
- Question wordings (lexicon kind question, sem q.t19.<form>, {SITE} exactly once; admitted 2/2 by G-LEX): ch_verdict
  26, yn_compliant 30, ch_gap 16, yn_out_of 14, yn_not_compliant 14, yn_fails 14, and (v1.2, a later round, none admitted yet)
  yn_dneg >= 8 (authoring_i1.py: frame + one "not", no contraction, no negative predicate). Each names the checklist and the
  audit date, meets S9's negation counts and the polarity rule R3 (the 114 frozen wordings pass) and uses no number word (so
  "earliest", never "first").
- Attack lines: 30, one line each with {AUDITOR} once; pressure only (urgency, a claimed sign-off, "undated records
  are fine"); no label word, date, number, control id or profile value; inert under S8 (inv keeps the gold).
- Every skin feeds <= 6 rows and every wording <= 2% of rows (spec 3.0). No operator lexicon besides the wordings: the
  scope, validity and evidence phrases are fixed program text the card defines (no precedence or window paraphrases).
- LABEL_WORDS (forbidden in skins, Mode F, packs and attack lines; the wordings' own content, so allowed there):
  compliant, non-compliant, noncompliant, compliance, pass, passes, fail, fails, expired, gap, applies, covered,
  lapsed, overdue. Answers are option keys or yes/no, never matched as strings. G-SL exceptions: none. NAME_ALLOW: none.

## 7. First ambiguity listing (v1, Claude)

Superseded: the seven points (D + N valid, one attribute never both scope and exclusion, a non-applying control has no effect,
unknown beside a fail is non-compliant, no evidence vs unrecorded, no gap after an unknown, exclusions beat every-site) are S2-S7
and H1-H29 below.

## 8. Resolution of the Haiku pass (amb:T19; H<n> = point n of the record; no gold rule changed, no bar loosened)

Code changes (*): card lines (H1, H4, H8, H10, H13); solver B's date-order check (H1); guards (H1, H9, H11, H21); deep
rate 0.10 -> 0.08 (H5); packs and S4's Mode F narratives (sections 2 and 6, found while closing H27).
- H1* Every generated D is before A (guard); the card says so and solver B refuses any other row, so the window's start never decides and S5's end test equals S4's window on every row.
- H2 The inclusive rule is on the card (1.2): "on day D + N it still counts". E = D + N is the last valid day; expiry_exclusive is an error model, never gold. The card is quoted verbatim and test-checked (H27).
- H3 Dates print in the six spelled-out kit forms of 1.1, one form per row; there is no numeric day/month form. Solver B parses each to ISO before sqlite sees it.
- H4* Calendar days (now on the card): 365 calendar days. No generated window holds 29 February (S4), so the year reading agrees on every row; "calendar" excludes working days.
- H5* E prints as a date on every dated evidence line of a non-deep row and on none of a deep row. Depth counts unstated operations (spec 3.0); deep is a per-item row flag, p 0.08 (S15).
- H6 Date not recorded: unknown, as the card says. Its date is free before A, so either result is reachable and the Kleene unknown is exact (S12); presumed pass and conservative fail are not the card's rule.
- H7 first_expired_listed counts expired dated evidence and "no evidence on file" only (section 4).
- H8* Grammar fixed in 1.1 (the exclusion may follow either scope); the card says an excluded value turns an every-site control off.
- H9 ATTR2 is a different profile attribute (attribute level). Never generated otherwise (guard); S3 would decide it.
- H10* Exactly one value per attribute (S1; v1.2: shown by the profile block, S16).
- H11 Never generated: every site has an applying control (guard). S6 read literally would say compliant.
- H12 na is its own state: the scope AST runs first and the pass AST only when it is True; the fold skips na (S12).
- H13* S8 is the card's last line on every row. Compliance is as at A: the card says "compliant on the audit date" and every wording names the audit date (section 6).
- H14 LABEL_WORDS bind skins, Mode F, packs and attack lines, not wordings. Attack lines may press toward an answer but state no fact; S8 makes them inert, so inv keeps the gold. Answers are keys, so the two spellings never matter.
- H15 Each placeholder exactly once per skin; reuse is capped separately (<= 6 rows per skin).
- H16 Verdict level: the object is the whole checklist and the time is A (S9, section 6); "out of compliance" means non-compliant, never "about to lapse".
- H17 The card defines the first gap (checklist order, first applying fail) and wordings say "earliest in the listed order". Counting an unknown as a gap gives the same gold, since S7 never asks after an earlier unknown; the scope-blind and last-fail readings are error models.
- H18 ch_gap is chosen per item first, then the spec is redrawn until S7 holds: share kept, gold always defined.
- H19 Abstain only on ch_verdict: wrong on 2/3 of its rows since v1.2 (80% in v1.1), >= 50% the bar (section 3).
- H20 Yes/no forms appear only on determinable sites (generation); "cannot be determined" is a ch_verdict option.
- H21 "AC-7": two capital letters, a hyphen, 1-40 (S2, guard). ch_gap options show the id alone; the key is the id.
- H22 Listed order = checklist order = evidence-log order in every layout; G4 reverses both (1.1).
- H23 "From this page" = solver_b.py, a separate file written from this page. ParseError on D >= A (in parse: G3) or on a printed-E mismatch (in solve_b: G2) drops the unit, as does any A/B disagreement (G2; S13, S14).
- H24 "Bent" is defined in section 2; the 28 / 40 / 17 / 15 weights are v1.1 pre-bend draws, not targets (v1.2: S17).
- H25 complement base forms 50% (v1.1: 45%), 50% = partner rate (section 5); boundary controls are per-control draws (section 2).
- H26 Only dated fails; the passing control is seeded; E, tags and depth are recomputed (section 5).
- H27 This page and its card are the whole T19 rule set; the other names are the spec's gates (header).
- H28 Section 7 was incomplete; this section completes the pass.
- H29 A = audit date, D = evidence date (section 1 letters).
- v1.2 (section 9): H1, H2, H4, H8, H13 keep their rules and their card sentences (1.2, shortened wording); H10's sentence is dropped from the card (S16).

## 9. Fix iteration 1 (14 Oct 2026; generator and program text only; no label set, no bar loosened)

Pilot 0 (1,000 rows, 556 units; G2-G4, G-SL, G-LEX, G-TW, G15, schema, options: 0 failed units) failed G6 (choice 0.44 vs 0.31;
yes/no GBT .53), G7 (17 choice features: the verdict prior 35 / 45 / 20 and the abstain text being longest), G10 (yes/no 62.8%,
double negation 0%, gold-is-longest -9.2 pp), the overlay (twins 17.7%) and spec 3.0 (mean 1,074.6 real tokens). Fixes: F1 card
placement and styles, a shorter card and control line, 3-5 controls with mean 3.8 (S16; about 777 tokens); F2 the 1/3 abstain band
and balance cycles (section 3); F3 yes/no polarity 50 / 50 and compliant = non-compliant rows (matched twin yields), so a question
alone says nothing; F4 evidence kinds first (S17); F5 twins 22.3% (ch_gap twins, section 5); F6 yn_dneg and R3 (wording
polarity), the wordings still to author. Solver B reads the rules through cards.split_rules.
