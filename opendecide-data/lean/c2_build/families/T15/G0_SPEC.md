# G0-lite T15: eligibility gates and ordered claimant cascades (C2 everyday tier; C2_DATA_SPEC 2.1, 3.14)

**Status: FROZEN v1.4 (14 Oct 2026).** v1.4 = v1.3 + fix iteration 2 (S3, S8, S23: depth drawn from the seed, A43 b; no gold rule or bar changed). v1.3 = v1.2 + pilot fix iteration 1 (section 7: S15-S18, S20, section 2 shares; no
gold rule, bar or pool changed). v1.2 = v1 + the one Haiku ambiguity pass (task `amb:T15`, 46 points H1-H46 in
`haiku/ambiguity/amb_T15_points.json`) + its Claude resolution and the pool rulings R1-R4 (section 6). sha256 in
`plugin.T15Plugin.G0_SHA256`, pass id in `G0_HAIKU_TASK`; `validate_plugin` refuses the plugin if this file changes. A38
(the OHS-4 freeze) is in PREREG_FINAL.md. Target 900 selected rows (about 1,350 generated), wave 2 (C2_DATA_SPEC 5.3).
All programmes, credits, limits and people are invented; no real benefit
value or statute text is used (the US FMLA thresholds, 1,250 hours and 50 employees, are never drawn as limits:
`REAL_LIMITS`, checked at every limit draw and limit twin, H39).

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Tracks, cards | A card is the C2 card: one programme pack x one sampler, card = seed mod 10 (S5: mod 4). Cards 0-5 (S5: 0-1) are gate programmes (household 0-2, work 3-5; S5: 0 household, 1 work), 6-9 (S5: 2-3) credits: gates 60%, claimants 40%. Training samplers take consecutive packs (`T15Plugin.card_pack`), so each of the 40 training cards has its own pack once the pool holds >= 12 household, 12 work and 16 credit packs. The printed rule card of a row (gates, comparators, limits, route; MIN, tie-breaker order) is drawn per row from the seed (H2). Both tracks: PROG (the card's programme name), YEAR (2025-2027; one slot per row, printed on the card, the facts header and step two; the period every fact refers to; it never changes an answer, H13, H40), CASE_ID, WORKER, SUBJECT (gates: the applicant, full name; claimants: the child, first name) |
| S2 | Gate facts | domain household: gross monthly income, net monthly income, countable assets (amounts), time in the service area (months), age (years); domain work: time employed (months), hours worked in the past year (hours), employees at the worksite (employees), gross annual pay, take-home annual pay (amounts). All five are printed on every row of the domain, plus "enrolled in" (a programme name or `none`). Net < gross and take-home < gross pay, always. Amounts are integer cents inside the program and always print as dollars with two decimals ($2,500.00, 2,500.00 USD, 2,500.00; CSV 2500.00 under its USD header); a limit and a fact print in one row's style, so "one cent" is $0.01 (H11). Counts are whole numbers in their unit, compared as printed, never rounded; "one unit" = one month, year, hour or employee (H14). Every fact is the applicant's value as recorded in this case for YEAR; no date arithmetic exists (H13) |
| S3 | Gates | 2-4 gates (37 / 55 / 8%), lettered A-D in listed order; no fact is on two gates (H15). 85% of lists hold an income gate = a gate on the domain's income pair (gross or net monthly income; gross or take-home annual pay); assets are never income (H15) |
| S4 | Comparators | lexicon clauses (G-LEX 2/2), a restriction: amounts are bounded from above only, `cmp.le` (X passes) or `cmp.lt` (X fails); counts from below only, `cmp.ge` (N passes) or `cmp.gt` (N fails). No amount gate has a lower bound and no count gate an upper bound, so "at least $X" or "at most N months" never reach a card; a card prints only admitted forms of the fact's sense; "up to", "within", "between" are never admitted (H6). A gate passes iff fact OP limit |
| S5 | Route | per row: on 50% of gate rows the card prints one route line, "an applicant enrolled in ROUTE skips Gate ..." (1 to k-1 gates; income gates twice as likely). It applies iff the printed enrolment equals ROUTE exactly (both are program-printed copies of one pack name, so case and spacing always agree). Skipped gates count as passed. Enrolment: ROUTE on 50% of route rows; otherwise the route's near-miss decoy (45%, S2 65%, when the route has one; Kestrel Housing Aid / Kestrel Housing Loan) or another listed programme or `none` (H2, H19) |
| S6 | Gate outcome | the first listed gate that applies (not skipped) and fails decides: `fail_X`; none fails: `eligible`. Eligible iff every applicable gate passes (card states both directions) |
| S7 | Gate answers | ch_outcome: the outcome. Predicate eligible: yn_eligible, yn_dneg_eligible (double negation) yes iff eligible; complements yn_ineligible (antonym: the word "ineligible", R3), yn_gate_stops (option framing: "does a gate that applies stop SUBJECT"; "applies" = not skipped, as the card's route line says; with no route line every gate applies), yn_fails (implicit: "fail(s) to qualify", R3), yn_not_eligible (syntactic) yes iff not eligible (H16) |
| S8 | Claimant facts | the child SUBJECT; 2-4 people (30 / 62 / 8%), each: full name "First Last" (first name agrees with the relationship's gender; first names distinct), relationship (mother, father, grandmother, grandfather, aunt, uncle; at most one mother and one father), months the child lived with them in YEAR (0-12; they may overlap), the person's own annual income (amount), filed a claim (yes / no) (H41) |
| S9 | Steps | step one keeps the people who filed a claim; step two those whose months meet MIN_CMP (a count clause: `cmp.ge` / `cmp.gt` against MIN_M in {5, 6, 7} months) |
| S10 | Tie-breakers | parent (mother or father) before anyone else; more months first; higher income first. The card prints all three in one of 6 orders (uniform) as First / Second / Third lines with fixed texts: "a parent comes first, before a grandparent, aunt or uncle", "the person with whom SUBJECT lived for more months comes first", "the person with the higher annual income comes first"; card order = this printed order (H23). Each tie-breaker, in card order, keeps only those still in the running (after steps one and two) who are best on it; the tie-breakers stop when one person is left (H1, H9). A full tie on all three is never generated (H24) |
| S11 | Claimant outcome | the one person left, else `none` ("Nobody may claim the child") when nobody among the listed people passes steps one and two. The list holds every person who asked to claim; S14 closes the world, so nobody else exists (H10) |
| S12 | Claimant answers | ch_claimant: the person's name or `none`. Predicate claims = ASKED (a listed person the question names) is the one person left after the whole cascade (winner only; passing steps one and two is not claiming, H3): yn_may_claim, yn_dneg_claim yes iff ASKED claims; complements yn_barred (antonym), yn_elsewhere (option framing: "pass to a different person from ASKED, or stay unclaimed"; yes when either branch holds, H17), yn_fails_claim (implicit), yn_may_not (syntactic: ASKED "may not claim" / "does not get to claim", R3) yes iff ASKED does not claim |
| S13 | Negation counts | (k_all, k_syn) = what the pinned `c_src/common/negcount.py` returns for the filled question: 0 / 0, except yn_fails, yn_fails_claim 1 / 0; yn_not_eligible, yn_may_not 1 / 1; yn_dneg_eligible, yn_dneg_claim 2 / 2. "barred", "ineligible", "stop", "unclaimed" are not negcount cues. Checked exactly on every wording at load and in test_plugin.py; G-TW checks every pair: syntactic k_all differ by 1, implicit k_all differ by 1 with equal k_syn (yn_eligible / yn_fails), antonym and option framing equal k_all (H18) |
| S14 | Closed world | every card ends "These rules and facts are complete, and only they decide the outcome." |
| S15 | Gate card (program) | "{PROG} eligibility rules for {YEAR}:" / "- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible." / per gate "- Gate X: passed when <fact phrase> <comparator clause>." / optional route line "- Route: an applicant enrolled in {ROUTE} skips Gate ...; for that applicant, skipped gates count as passed, and every other gate still applies." / "- An applicant who passes every gate that applies is eligible; any other applicant is not eligible." / S14 |
| S16 | Claimant card (program) | "{PROG} rules for {YEAR}: who may claim {SUBJECT}." / "- Only one person may claim {SUBJECT}. Work through these steps in order." / steps one, two (S9) and three ("- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.") / First, Second, Third tie-breaker lines (S10) / "- If nobody is left after step two, nobody may claim {SUBJECT}." / "- A parent means the child's mother or father. Different people's months can overlap." (H42: no shared-home fact) / S14. The program TEMPLATE text holds no digit (rule ids are letters and ordinal words); digits reach a card only through typed slots: YEAR, limits, MIN_M (H31) |
| S17 | Facts block (program) | header "Facts for {SUBJECT} ({YEAR}):" (gates) or "People who asked to claim {SUBJECT} ({YEAR}):" (claimants; a listed person may still have "filed a claim: no", so asking is not filing and step one tests the printed field, H12), then one container: bullet lines, markdown table, one-line JSON, CSV (cents `nocomma`, counts `plain`, header "as CSV with amounts in USD") or the interview ("Intake interview with" / "Interview notes for": short fixed program "Caseworker:" questions that carry no fact ("Gross monthly income?", "Annual income?", "Filed a claim for {SUBJECT}?" ...), and answer lines "<name>: <value>." holding the exact slot value, no hedge, H27). Container, first rule that holds (H26): S5 CSV; S4 interview; a JSON register JSON; S3 table; ticket / form / log registers table; else (memo, chat, email, yaml, transcript, voicemail) lines. An inv twin appends one line "Note added to the case: <attack line>" after the container's last line, inside the facts block; the container lines above stay intact and parse alone (H25) |
| S18 | State layout | state = two blocks joined by one blank line: case-note skin, then facts (S3: facts first). Skins hold no blank line. yes/no row: row.card = the card (the definitions block), instructions = the question; choice row: no card, instructions = the card, one blank line, the question (`cards.place_rules`; solver B reads both through `cards.split_rules`). The decoder prompt (decoder_io cygnet) prints the state, then the instructions (twice), and row.card once on yes/no rows, in every sampler (H28) |
| S19 | Case-note skin | Mode T only (C2_DATA_SPEC 3.0: a Haiku-written slot template; the program fills every value): {CASE_ID}, {WORKER} and {SUBJECT} exactly once each and no fact; the same skins serve both tracks. Mode F (free text from a facts-only brief that must pass the fact lock, G-SL and G3-H) is 0% here: no decisive fact lives only in narrative (H29) |
| S20 | Options | ch_outcome: the whole closed set (eligible + one `fail_X` per gate, 3-5 options) in a label-blind order, texts "Eligible" / "Not eligible: Gate X is the reason (<fact label>)", the fact label being the facts-block label; exactly one option is the decisive gate (S6) or eligible (H8); every option is gold on 1 / (gates + 1) of the rows, twins included (the base target is lower: section 7 F2). ch_claimant: open set = the gold plus k - 1 error-model answers (never the whole list), full names as printed; k in {2, 3} counts every option shown, "Nobody may claim the child" included when shown (H21). The display plan (`plugin.claim_plan`, c2_kit.choiceplan) is drawn from the row key "T15\|seed\|sampler\|qform" (no gold input) BEFORE the structure: k uniform on {2, 3}; "nobody" is shown only when k = 3, on 85% of those rows (never at k = 2), and is gold on 46% of the shown base rows (label-first: the sampler draws the target from the plan, then the structure); twins never end in nobody; equiv / inv rows copy the base. A case the plan cannot fill is redrawn with the same target; a twin that cannot is not proposed; k is never lowered and "nobody" never forced on (v1.3, section 7) |
| S21 | Never decisive | the year, the caseworker, the case id, PROG (the card's own programme name; ROUTE and the enrolment are decisive facts under S5, H20), ungated facts, the enrolment when no route is listed, listing order of people, income equal between people a tie-breaker already separated, an attached note |
| S22 | Error models | one construction each, the card otherwise followed (H32). gates: `stop_at_first_gate` (Gate A alone decides, route ignored), `net_vs_gross` (each income gate reads the other fact of its pair), `drop_inclusive_endpoint` (cmp.le / cmp.ge read as lt / gt), `add_exclusive_endpoint` (lt / gt read as le / ge), `t15_ignore_route`, `t15_route_skips_all` (enrolled: eligible), `t15_route_not_enrolled` (route applied without enrolment), `t15_last_failure` (last failing applicable gate), `t15_flip_direction` (every comparator le<->ge, lt<->gt), `t15_flip_gate_a`-`_d` (that gate only), `t15_any_pass` (eligible when any gate passes or is skipped). claimants: `wrong_tiebreak` (printed order reversed, directions kept), `t15_default_order` (parent, months, income), `t15_swap_first_two` (first two printed tie-breakers swapped), `t15_skip_filed_check`, `t15_skip_months_check`, `drop_inclusive_endpoint` / `add_exclusive_endpoint` (the months step only), `t15_income_only` (highest income in the running), `t15_most_months` (most months among all listed), `t15_first_listed` (first listed person in the running), `t15_income_all` (highest income among all listed) and `t15_first_filed` (first listed person with "filed: yes"); the last two are options only |
| S23 | Depth | gates: 2 operations the reader performs (the card states each rule, prints no result): test the gates in order against printed facts; apply the route and the first-failure rule. deep = a property of the card, drawn from the seed BEFORE the target and never read from the answer (v1.4, A43 b): a 4-gate card (gates) or a 4-person cascade (claimants), so each deep class carries every label at its normal share. No intermediate exists to print |
| S24 | Solver A | ordered decision lists (rule_engine): gates = rules.RuleSet first_match of "fail_X" rules (a skippable gate's rule is guarded by "not enrolled in ROUTE"), default eligible, run by rules.resolve; claimants = rules.evaluate filters for steps one and two, then the tie-breakers in card order, each keeping the best |
| S25 | Solver B | its own parser (card line by line, five containers, skin template, wording template, lexicon parse_exact on admitted forms); decision-table enumeration (decision_table): a truth table over all 2^k pass / fail vectors maps the applicable failing gates to the earliest letter (sign tests on fact - limit); claimants: a pairwise duel table over the people still in the running after steps one and two (first differing tie-breaker in card order); the winner wins every duel, and no single winner raises (H34) |
| S26 | Relations | complement on 45% of yes/no bases (partner table `plugin.PARTNERS`); minimal-edit twin tried on 44% of bases, one input slot, answer predicted from the edited construction: a gated fact or a limit moved to the other side (onto the limit or one cent / unit past it), a comparator swapped inclusive <-> exclusive at the limit, the enrolment to / from the route; a person's months across the minimum, filing flipped, income $1.00 over / under the best rival (the highest income among the other listed people), relationship parent <-> same-gender non-parent. An edit that breaks S2, S8 or S10 (net < gross, months 0-12, one mother / father, gender agreement, a positive amount, a full tie, an FMLA limit) is skipped, and every twin passes G2 (A = B) and G-TW (H4). equiv 10% (another skin, register and container), inv 3% |
| S27 | G4 (checked, never emitted) | answer unchanged: change the year, rename the caseworker; gates: rename the applicant, change an ungated fact, move a passing fact further inside its limit, change a non-route enrolment; claimants: rename the child, reverse the order of the people, rename a non-winner, raise the winner's income. A failed check drops the whole relation unit (pipeline.build_unit); the generator moves to the next seed (H44) |

## 2. Samplers, shares, traps, balance

Generator measurements (H35-H37): spec-level shares on the 2,000 training specs (seeds 0-499 x S1-S4); row-level shares
on the 1,500 relation units (seeds 0-299 x S1-S5, 2,594 rows, partners and twins added to their base, never replacing
it). test_plugin.py asserts the bands on these sets. They describe generation, not the 900 selected rows (H38).

- **Samplers.** S1 forward (note, facts; then card, question). S2 label-first near miss: the target is drawn first, as in
  every sampler, and every boundary and trap probability is +0.20 (the largest shifted value is 0.95, so none exceeds 1);
  layout as S1 (H43). S3 table-first (facts before the note; table or JSON). S4 interview transcript. S5 held out:
  held-out programme packs, CSV facts, held-out skins (transcript, voicemail) and wordings (mixdev only).
- **Cards.** 10 per training sampler (40 training cards, one programme pack each) and 4 for S5. The build draws seeds
  0, 1, 2 ... per training sampler until the generated target is met: about 1,350 rows over 40 cards, about 34 rows per
  card (relation rows included). Per-card yes rate in [0.2, 0.8], cards paired antithetically (mean exactly 0.5).
  Display and rule draws come first; then the target answer from a low-discrepancy draw; then facts that realise it.
- **Question forms (base specs, per track).** choice 58%; yes/no 42%: positive 17 + 4 (double negation), complements
  6 / 5 / 5 / 5 (gates) and 5 / 5 / 5 / 6 (claimants). Rows: yes/no 49.0% of all unit rows (49.1% of training rows);
  k_syn >= 1 on >= 10% and k_syn >= 2 on >= 2% of yes/no rows.
- **Gold.** yes 49.6% of yes/no specs (eligible 50.1, claims 48.9); "yes = bad outcome" 50.0%. ch_outcome base
  specs: eligible 22.8 (30.6 / 19.9 / 15.6 on 2 / 3 / 4 gates), fail A 26.3, B 27.7, C 18.9, D 4.3 (fewer cards have C,
  D); over all rows (twins 39% eligible, base 22%) every option is gold on 1/k (eligible 26.9 against a mean 1/k of 26.9;
  letters within 1.5 pp; 9,852 rows) and gold-is-longest is -0.3 pp.
- **Gate traps (share of gate specs).** Gate A passes or is skipped but another gate decides 40%; gross / net swap
  changes the outcome 29%; a gated value exactly at its limit 33% (passing there 22%); a value one cent or unit from a
  limit 57%; missed route changes the outcome 15%; route wrongly applied changes it 12%; two or more applicable gates
  fail 13.5%; route listed 49%, enrolled 25%.
- **Claimant traps (share of claimant specs, choice and yes/no).** Another tie-breaker order picks someone else 50%;
  ignoring the filed claim does 42%; ignoring the months step does 23%; someone exactly at the months minimum 30%; a
  parent in the running loses 15%; equal incomes in the running 6.6%; second tie-breaker reached 15%, third 4.6%.
- **Nobody (H37, v1.3).** Claimant yes/no: 9.3% of the specs answer "ASKED does not claim" because nobody claims
  (P_NOBODY_NO). ch_claimant: gold `none` 20.3% of the specs (1/2 x 85% x 46%); the option is shown on 45.8% of the rows,
  all at k = 3; there it is gold on 33.2% (1/k; twin rows are never nobody) and wrong on 66.8% (bar: >= 50%, per cell).
- **Named options.** Every wrong ch_claimant option names >= 1 model (100%); on the closed ch_outcome set 85.7% do; the
  rest keep the kit role `closed` (section 5).
- **Overlay (unit rows).** Complement 47.9% of yes/no rows, 70.7% of pairs non-syntactic (v1.2 measurement; the
  complement code is unchanged); twins 23.5% of rows; equiv 5.9%; inv 1.4% (2,605 rows in 1,500 units, v1.3).
- **Depth.** deep = 8% of gate specs (4-gate cards), 8% of claimant specs (4 people), at most 10% of rows (meta.deep; v1.4).
- **Length.** Real Qwen3.5-4B tokens (instructions twice, row.card once): v1.2 pilot mean 812.5 (bar 800); v1.3 blocks
  (seeds 100032, 300032) 687.7 and 680.9, max 1,143. Haiku skins are capped at 120 characters, wordings at 25 words.
- **Selection (H38).** `c2_select.py` keeps whole units by the C1-only crowd bins (easy <= 25%, hard <= 30%) with
  label-balanced quotas per stratum; spec 3.0 balance bars are re-checked on the selected rows by `gate_c2.py`.

## 3. Haiku tasks (after A38; Haiku never sees a question, option or gold) -> `haiku_author.py`, `haiku/author/`

1. **Case-note skins**: 8 training registers (memo, chat, email, ticket, json, yaml, log, form) x 40 asked, held out
   (transcript, voicemail) x 30. Keep `{CASE_ID}`, `{WORKER}`, `{SUBJECT}` exactly once each; fit an adult applicant and
   a child; <= 120 characters; no blank line, no facts-block head; no fact (number, date, amount, programme, relationship,
   enrolment, month or income word), outcome word, modal, quantifier, hedge, status word, negation or capitalised name.
   Each skin feeds <= 6 rows: >= 225 training skins must pass G-SL.
2. **Question wordings**: 178 asked over the 14 forms + 44 held out (S5). The 2% cap is per wording over all family
   rows, so >= 50 admitted are needed (H5); admission target per form = ceil(1.25 x row share / 2%), at least 3: 78 in
   all (ch_outcome 20, ch_claimant 13, yn_eligible 8, yn_may_claim 6, yn_ineligible 4, 3 for each other form). Slots
   {SUBJECT}, {PROG} (+ {ASKED} on claimant yes/no) once each; exact S13 counts; G-LEX 2/2 to `q.t15.<form>`. R3: the
   briefs name the surface each complement needs (S7, S12): "ineligible", never "disqualified"; "fail(s) to qualify",
   never "fail to be eligible"; "may not claim" / "does not get to claim", never "is not the person who".
3. **Gate paraphrases**: 12 per comparator meaning (cmp.le, cmp.lt on {X}; cmp.ge, cmp.gt on {N}); they must read after
   the card's frames ("... is", "... are", "... for", "... has"); lexicon unit test plus G-LEX 2/2. R2: plain everyday
   phrasings (the commonest card wording) are asked for too; a Haiku text that equals a fixture text may be admitted.
4. **Attack lines**: 24 + 8 held out; one line, `{WORKER}` at most once; pressure or a fake sign-off that adds no fact
   and states no outcome (no label word, no status word such as approved or entitled, H30); never eval_opi strategy
   strings or the jagged injected line (G13 method 8 checks).
5. **Packs**: 60 programme packs (18 household, 18 work: programme, two route programmes each with a one-word near-miss
   decoy, two other programmes, the first also a route with no decoy; 24 credits: programme), 10 held out; name pools
   (female, male and neutral first names, last names, child names, caseworkers). Checks: no digit, comma, colon,
   semicolon or pipe; no negation cue; no name in two pools; a decoy differs from its route by one word. They drive
   the plugin through `T15Plugin(packs=..., names=...)`.

## 4. Ambiguity listing written before the Haiku pass

1. "at most $X" / "X or less" at exactly $X: passes (S4). "below / under / less than $X" at $X: fails.
2. "more than / over 6 months" at exactly 6 fails; "at least / no fewer than 6 months" at 6 passes (S4).
3. A gate on gross income while net income is also printed: the named one (S2, S15).
4. Several gates fail: the first listed gate that applies (S6).
5. An enrolled applicant fails a skipped gate: still eligible (S5).
6. Enrolled in a near-miss programme, or `none`: no route (S5).
7. yn_gate_stops: same as not eligible; skipped gates do not apply (S7).
8. Months that sum past 12 across people: allowed; the card says months can overlap (S8, S16).
9. A tie-breaker on which everyone left ties removes nobody (S10).
10. A grandparent, aunt or uncle is not a parent (S10, S16).
11. A person who did not file cannot win: step one removes them (S9).
12. yn_elsewhere when nobody can claim: yes (S12).
13. Two people tie on all three tie-breakers: never generated (S10, H24).
14. "eligibility rules for 2026" with facts "(2026)": one YEAR slot, never disagrees (S1).

## 5. Resolution

The fourteen points of section 4 are fixed by S2-S16, and the card states each rule an answer needs (no generated
row needs a tie rule, H24). One accepted, recorded issue that is not among them (H22): on the closed ch_outcome set
14.3% of wrong options are produced by no single named error model; they keep the kit role `closed`
(`distractors.build_closed`: a label of the family's natural closed set that no model outputs). Recorded choices: Mode
F, inverted, few-shot, masked-label and short-card variants are not in v1 (every decisive value and rule stays program
text); fail C / D answers are rarer because fewer cards have those gates; at most one route line per printed card
(per row, H2); incomes are whole cents, never rounded.

## 6. Resolution of the Haiku pass (amb:T15; H<n> = point n of the record; no gold rule changed; no bar loosened)

H1 early stop covers only the tie-breakers: step three now says "the tie-breakers stop" (S16; code: card text in
plugin and solver B). H2 per row: S1, S5, section 5. H3 winner only (S12); wordings must ask whether ASKED is the one
person who may claim; a wording readable as "passes steps one and two" is not admitted; choice wordings ask which
person, if any, may claim (section 3, haiku_author.py). H4 S26. H5 section 3 (>= 50, plan 78). H6 restriction (S4). H7
intended (S20): options are the row's answer set and gold is always among them; abstention is trained on the shown rows
(79.3% wrong). H8 option text now "Not eligible: Gate X is the reason (<label>)" (S20; code: plugin outcome_text and
solver B OUTCOME_OPTION); a skipped gate passes (S5), so its option is false. H9 running set (S10, S16 new wording).
H10 S11. H11 S2. H12 S17. H13 S1, S2, S8. H14 S2. H15 S3. H16 S7. H17 S12; wordings name both branches. H18 S13. H19
S5. H20 S21. H21 S20. H22 section 5. H23 S10. H24 sampling rejects a full tie (`plugin.Tie`), twins skip one, and both
solvers refuse one (G2 drops the unit; test_a_full_tie_is_refused_by_both_solvers). H25 S17. H26 S17. H27 S17. H28
S18. H29 S19. H30 section 3 item 4 (loader check). H31 S16. H32 S22. H33 S23. H34 S25. H35 S1 + section 2. H36
section 2 (partners and twins are added rows; 49.0% measured). H37 section 2. H38 section 2. H39 header (code: the
limit twin now skips REAL_LIMITS too). H40 S1: each card prints its whole rule set, so the year selects nothing the
card does not state. H41 S8, S20. H42 S16 (the shared-home sentence is gone; code: card text in plugin and solver B).
H43 section 2. H44 S27. H45 this section is the one re-freeze (v1.1), made by the family lead before any pool or row;
any later change is a new version and sha, made before rows of the changed kind are generated, never during a run.
H46 terms: A38 = the PREREG ruling freezing OHS-4; wave 2 = C2_DATA_SPEC 5.3; G-LEX 2/2 = two blind Haiku extractions
pick the form's meaning (c2_kit/lexicon.py); kit role = Option.role (gold, error, abstain, closed); MIN_CMP / MIN_M =
the step-two clause and its month count (S9); mixdev = the held-out dev mix (spec 7.1); eval_opi / jagged = the
retention eval sets of spec 4.1 and 7.2; G4 = S27; inv / equiv twin = attack / format twin (spec 4.1); deep = S23;
`plugin.PARTNERS`, `test_plugin.py` = files in this folder; label-first = S2; one slot = one input slot differs
(G-TW); best rival, fact label = S26, S20; countable assets = an invented household amount fact (S2).

**v1.2 pool rulings (14 Oct 2026, family lead; after the freeze-v1 pools of `pools/MANIFEST.json`, before any row;
H45; no gold rule changed, no bar loosened; builder and tasks in `haiku/redo2/`).**
R1 G-LEX 2/2 is a per-form bar. A form authored or re-entered after freeze-v1 gets its own two independent blind reads
(the v1 prompt and the closed meaning lists of `fixtures.py`); v1 reads, admissions and rejections stay final (no
re-vote: a replacement is a new text under a new item id). A new form must pass its unit test in the full v1 registry
(every v1 form, admitted or not) and break no v1 form's unit test, else it is dropped. Freeze-v1 files are never
rewritten: the merge is a supplement, freeze-v2 (`pools/redo2/`), counted against the unchanged section 3 targets.
R2 `fixtures.py` texts are in-memory test stand-ins, never pool items. A Haiku-authored text equal to a fixture text is
a valid candidate under every other load check (G-SL, shape, exact S13 counts, dedup inside the pool), its unit test and
G-LEX 2/2; the v1 loader's fixture-copy drop does not apply to freeze-v2. Plain comparator phrasings are asked for.
R3 S7, S12 and section 3 item 2 name the complement surfaces. The v1 rejections they explain ("disqualified" read as
yn_fails, "fail to be eligible" as yn_not_eligible, "is not the person who" as yn_fails_claim / yn_elsewhere) stay.
R4 G-LEX items of redo2 reads fill each slot with a distinct value of its role (applicant full name, child first name,
programme name, $2,500.00, 6 months) instead of the kit's one shared sample (`lexicon._samples`, unchanged). The 239
v1-admitted forms keep their v1 reads: a program role check (each placeholder in its role position,
`haiku/redo2/plan/role_check_v1.json`) flags none of the 194 admitted question forms; comparators hold one slot each.

## 7. v1.3: pilot fix iteration 1 (14 Oct 2026, family lead; C2_DATA_SPEC 6.4 step 6; `pilot/PILOT_VERDICT.json` FIX-1 to FIX-3)

The v1.2 pilot failed G6 / G7 choice, G10 longest option and the spec 3.0 mean (812.5 > 800) on generator causes. No gold
rule, bar or label changed. Calibrations ran on seeds 100000 to 800000, never on the pilot block 900000.
F1 (ch_claimant abstain, S20). "Nobody" was shown on 70% of rows and always when gold, so it was gold on 23% of the rows
that show it (chance 1/2 or 1/3) and was the longest, only non-name option: "never pick Nobody" scored 0.54 against 0.42.
The plan is drawn from the row key before the structure; the gold share is 1/k in the one cell that shows the option. k = 2
never shows it: a k = 2 cell sits on the spec 3.0 bar (gold 1/2, wrong >= 1/2) and holds about 45 rows at pilot size, so
the G10 per-cell bar would be a coin flip. Twins never end in nobody (they dilute the base rows' 46% to the cell's 1/3:
cell share 0.32 to 0.35 on 7,174 rows).
F2 (ch_outcome). "Eligible" is the shortest option and was gold on 36 / 33 / 31% of the 3 / 4 / 5-option rows (1/k: 33 / 25 /
20%). A base target of 1 / (gates + 1) is not enough: the twins (28% of the ch_outcome rows) end in eligible or an early gate
more often (39% eligible against 22% of base rows), which left eligible 2.2 pp high over all rows (G6 meta +2 to +3 pp at
5,000 rows, G7 kind:neg p 1e-3) and fail D 3 pp low. `OUTCOME_ELIGIBLE` 0.270 / 0.205 / 0.166 (2 / 3 / 4 gates) and the
decisive-gate weights `OUTCOME_W` (yes/no rows keep a uniform gate) solve (1 + eps) q + tau T q = uniform on the measured
twin transitions T (5 iterations of 15,000 to 38,000 specs per gate count).
F3 (length). Step three and the first gate bullet are shorter (58 -> 38 and 39 -> 28 tokens; H1, H9 and the first-failure
rule keep their wording), the interview questions are short forms, and yes/no rows carry the card in row.card (S18).
F4 (polarity). The plugin opts in to c2_kit.polarity (`POLARITY_CHECK`): the 133 frozen yes/no wordings read with their
forms' polarity (0 failures; no strict frames). F5 (full-run driver): rows per skin <= 6 and per wording <= 2% by a
label-blind usage counter passed as `exclude=` to `ctx.pick`.
