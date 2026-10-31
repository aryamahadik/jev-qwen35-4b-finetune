"""Part A2: monotonicity continued (no, at most, any, only, the only, double negation, syllogisms)."""
from _h import it, L3, L3CARD, FOLLOW, CONSIST, E, C, U, NONE

S14 = ["Some Year 9 student who missed the deadline went to Kew",
       "No Year 9 student who missed both deadlines went to Kew",
       "Every Year 9 student who met the deadline went to Kew",
       "No Year 9 student went to Kew",
       NONE]

S25 = ["Most tenors attended the Friday rehearsal",
       "Most members of the chamber group are tenors",
       "Every tenor attended the Friday rehearsal",
       "Some member of the chamber group missed the Friday rehearsal",
       "No tenor missed the Friday rehearsal",
       NONE]

SEN = [f"sentence {i}" for i in range(1, 9)] + [NONE]

ITEMS = [

it("A14", "choice",
   "Which statement must be true if the trip report is accurate?",
   """Hollins Park Academy - Trip report: Year 9 visit to Kew Gardens, Thursday 2 October
Author: Mr. D. Achterberg, trip leader

Numbers. 96 of the 118 Year 9 students came on the trip. Permission slips for Kew were due on 19 September; slips for the separate Science Museum trip (November) were due on 26 September.

Deadline enforcement. As agreed with the head of year, none of the Year 9 students who missed the Kew permission-slip deadline went on the Kew trip; they had a revision day in school with Ms. Horvath. Several students who did return slips on time were absent on the day through illness, and two families withdrew their child the evening before.

Behaviour. Excellent overall. One student was found in the staff-only glasshouse and was spoken to.

Recommendation: keep the same coach company, but move the lunch stop to the Orangery lawn.""",
   S14[1], opts=S14,
   card="- Some Year 9 student who missed the deadline went to Kew: at least one student who missed the Kew slip deadline went on the Kew trip\n"
        "- No Year 9 student who missed both deadlines went to Kew: no student who missed the Kew deadline and also the Science Museum deadline went on the Kew trip\n"
        "- Every Year 9 student who met the deadline went to Kew: each student who returned the Kew slip on time went on the trip\n"
        "- No Year 9 student went to Kew: not a single Year 9 student went on the Kew trip\n"
        "- none of these: none of the listed statements is guaranteed by the report",
   diff=2),

it("A15", "noul",
   "Does the audit note guarantee the statement?",
   """Accounts Payable - Internal Audit Note IA-26-031
Unit: Shared Services Centre, Dunmere
Period reviewed: March invoices (3,412 invoices processed)

Scope: The audit sampled 400 invoices at random and extrapolated to the full population at 95% confidence. Errors were classified as coding errors (wrong cost centre, wrong nominal code, wrong VAT code) or approval errors (approver outside delegated limit, missing second signature).

Findings:
1. At most 10% of the invoices processed in March contained a coding error of any kind. Most coding errors found were wrong cost centres on facilities invoices.
2. Approval errors were rarer; the extrapolated rate is under 2%.
3. Two duplicate payments were identified and have already been recovered.

Management response: the facilities team will receive refresher training on cost-centre selection by 30 May.

Statement: At most 10% of the invoices processed in March contained a wrong VAT code.""",
   1, card=FOLLOW, diff=2,
   twin=[("At most 10% of the invoices processed in March contained a coding error",
          "At least 10% of the invoices processed in March contained a coding error")], twin_gold=0),

it("A16", "choice",
   "Relative to the lab notebook entry, which relation holds for the statement?",
   """Lab notebook - Greenhouse 4, germination trial GT-19
Entry by: Ana Beltran, research technician
Date: 21 April

Tray set C (120 cells, one seed each, cultivar 'Marnie', seed lot 2291) was sown on 7 April under the standard 16/8 light regime at 21 degC. Germination counted as visible radicle at least 2 mm long.

Count today (day 14): almost all of the 120 seedlings in tray set C germinated. The few blanks are clustered along the south edge, where the heat mat cable runs, so I suspect uneven bottom heat rather than seed quality.

Tray set D (same cultivar, seed lot 2304) is running two days behind and will be counted on 23 April.

Action: ask facilities to check the heat mat under the south edge of bench 3 before the next sowing.

Statement: Not all of the seedlings in tray set C germinated.""",
   E, opts=L3[5], card=L3CARD, diff=3),

it("A17", "noul",
   "If the procedure is followed exactly as written, must the statement hold?",
   """THE HARBOURSIDE HOTEL - Front Desk Standard Operating Procedure FD-12
Guest dietary requirements at check-in

Purpose: to make sure the kitchen knows about dietary needs before a guest's first meal.

Procedure:
1. At check-in, ask every guest: "Do you have any dietary requirements or allergies we should know about?"
2. Record the answer in the Notes field of the booking, using the drop-down codes where possible.
3. If a guest reports any allergy, the kitchen is notified through the Allergen Alert form before the guest's first meal, and the guest is given an allergen card for the restaurant.
4. Preferences that are not allergies (vegetarian, no pork, low salt) are recorded but do not trigger an Allergen Alert.
5. Where a guest refuses to answer, record "declined" and do not ask again.

Owner: Rooms Division Manager. Review date: January.

Statement: If a guest reports a nut allergy at check-in, the kitchen is notified before the guest's first meal.""",
   1, card=FOLLOW, diff=1,
   twin=[("3. If a guest reports any allergy, the kitchen", "3. If a guest reports a shellfish allergy, the kitchen")],
   twin_gold=0),

it("A18", "choice",
   "Which of these translators must have used the project glossary?",
   """From: Katrin Oyelaran, Localisation Lead, Brightloom Studios
To: Vendor managers
Subject: Glossary compliance on the Vessel and Orchid projects

Hi both,

Quick summary before Monday's review. The Vessel project (the Portuguese and German builds of the game) had five translators: Hanne Solberg, Mateus Andrade, Gregor Pohl, Liesl Brandauer and Tiago Reis. Of those five, Hanne was the only one who did not use the project glossary; her files are the ones flagged in the QA sheet for the "Warden/Keeper" inconsistency in chapter 3.

The Orchid project (the Italian build) is a different story. Ilse Marino and Dario Fumagalli shared the work, and I have not yet checked their files.

Separately, Noor Haddad did the German voice-over scripts for Vessel, which are outside the glossary scope entirely.

Can you both confirm the rates for the Orchid review?

Katrin""",
   "Mateus Andrade",
   opts=["Hanne Solberg", "Mateus Andrade", "Ilse Marino", "Dario Fumagalli", "Noor Haddad", NONE],
   card="- Hanne Solberg: the Vessel translator singled out in the email\n"
        "- Mateus Andrade: a Vessel project translator\n"
        "- Ilse Marino: an Orchid project translator\n"
        "- Dario Fumagalli: an Orchid project translator\n"
        "- Noor Haddad: the writer of the German voice-over scripts\n"
        "- none of these: the email does not guarantee that any listed person used the glossary",
   diff=2, twin=[("Hanne was the only one who did not use the project glossary", "Hanne was the only one who used the project glossary")],
   twin_gold="Hanne Solberg"),

it("A19", "choice",
   "Assuming the commissioning log is accurate, how should the statement be labelled?",
   """Commissioning log - Fenwick Water Treatment Works, Clarifier Stage 2
Entry 14 (reviewed by the lead commissioning engineer, S. Mbeki)

Pressure testing of the six relief valves on the stage 2 dosing line was carried out on 11 March by the contractor, Tallis Process Ltd, at 1.5 times design pressure.

The contractor's draft report states that none of the relief valves failed the pressure test. Having compared the draft against the raw chart recordings, I record that the claim in the draft that none of the relief valves failed the pressure test is not correct. The contractor has been asked to reissue the report with the chart recordings attached.

The stage 2 dosing line is not to be put into service until the reissued report is accepted. Stage 1 continues on normal operation.

S. Mbeki, 13 March

Statement: At least one of the stage 2 relief valves failed the pressure test.""",
   E, opts=L3[0], card=L3CARD, diff=2,
   twin=[("failed the pressure test is not correct. The contractor has been asked to reissue the report with the chart recordings attached.",
          "failed the pressure test is correct. The contractor has been asked to reissue the report with the chart recordings attached.")],
   twin_gold=C),

it("A20", "noul",
   "Would accepting the audit letter commit a reader to the statement?",
   """Brannock & Weir LLP - Chartered Accountants
To: The Finance Committee, Ellery Foundation
Re: Limited-scope review of the travel ledger

Dear Committee members,

As requested, we carried out a limited-scope review of the Foundation's travel ledger for Q3 of the financial year (1 July to 30 September). The ledger records flights, rail, hotel bookings, per-diem claims and taxi receipts for staff and trustees.

For each ledger line we checked that a receipt or booking confirmation was on file and that the claim was approved by a budget holder other than the claimant. We did not find any unsupported expense in the travel ledger for Q3.

We note, outside the scope of this review, that two per-diem claims from Q2 were approved by the claimant's own line report; we recommend the Committee reviews that approval chain.

Yours faithfully,
Brannock & Weir LLP

Statement: The reviewers did not find any unsupported expense among the September hotel bookings in the Foundation's travel ledger.""",
   1, card=FOLLOW, diff=2,
   twin=[("(1 July to 30 September)", "(1 April to 30 June)")],
   twin_gold=0),

it("A21", "choice",
   "Which numbered sentence of the maintenance summary does the statement contradict?",
   """Tarvik Energy - Standby Power: 2025 maintenance summary (numbered for reference)

(1) Every backup generator at the Oster plant was load-tested in 2025.
(2) Not every generator at the Tarvik plant is a backup generator; two are primary units that run continuously.
(3) Every backup generator at the Tarvik plant was load-tested in 2025.
(4) Some generators at the Tarvik plant were not load-tested in 2025.
(5) No generator at either plant was load-tested more than twice in 2025.
(6) At most one of the Tarvik primary units had its oil changed in 2025.
(7) If a unit failed its load test, it was retested within 30 days.
(8) The Oster plant has more backup generators than the Tarvik plant.

Prepared by: Standby Power Team, 14 January 2026.

Statement: Some of the backup generators at the Tarvik plant were not load-tested in 2025.""",
   "sentence 3", opts=SEN,
   card="\n".join(f"- sentence {i}: the sentence numbered ({i}) in the summary" for i in range(1, 9))
        + "\n- none of these: the statement contradicts none of the numbered sentences",
   diff=2, twin=[("(3) Every backup generator at the Tarvik plant", "(3) Some backup generator at the Tarvik plant")],
   twin_gold=NONE),

it("A22", "noul",
   "Given the tender record, does the statement necessarily hold?",
   """Castlerigg Borough - Procurement: tender record TR-4410
Lot: Disposal of surplus vehicles (lot 3: two 2016 refuse trucks)

Reserve price: set by the fleet manager and sealed before bids opened. Rule applied by the panel: every bid that came in under the reserve price was rejected without further evaluation; bids at or above the reserve were scored on price and on the collection date offered.

Bids received (sealed, opened 10 March):
- Ardmore Salvage: under the reserve, as recorded by the panel secretary.
- Kessel Plant Hire: lower than Ardmore's bid; offered collection within 5 days.
- Venn Brothers: above the reserve; offered collection within 20 days.
- Pellow Recycling: withdrawn before opening.

Outcome: the lot was awarded to the highest-scoring compliant bid. The panel noted that interest in lot 3 was weaker than expected.

Statement: Kessel Plant Hire's bid was rejected without further evaluation.""",
   1, card=FOLLOW, diff=2,
   twin=[("- Kessel Plant Hire: lower than Ardmore's bid;", "- Kessel Plant Hire: higher than Ardmore's bid;")],
   twin_gold=0),

it("A23", "choice",
   "Given only the locksmith's note, the statement is which of these?",
   """Handwritten note left at reception, Cordwainer House, scanned into the facilities ticket FAC-3318

"To the facilities team -

I've finished re-pinning the east stair doors. As agreed, I collected the old keys from the security office this morning. There are supposed to be two master keys for the east stair from the old system (one for the day team, one for the night team). At least one of the two master keys was not returned to the security office, so I can't confirm the old system is fully retired. Until you know where the missing key is, I'd treat the east stair as not secure and keep the new cylinders in.

The invoice will follow by email. I've left the three new masters in the key safe, code as agreed.

Ruth Adebayo, Adebayo Locks"

Ticket status: awaiting facilities review.

Statement: Neither of the two old east-stair master keys was returned to the security office.""",
   U, opts=L3[1], card=L3CARD, diff=2,
   twin=[("At least one of the two master keys was not returned to the security office, so I can't confirm the old system is fully retired. Until you know where the missing key is,",
          "Not one of the two master keys was returned to the security office, so I can't confirm the old system is fully retired. Until you know where the missing keys are,")],
   twin_gold=E),

it("A24", "noul",
   "Is the statement consistent with the operations report?",
   """Loughmere Ferries - Daily operations report, Tuesday
Route: Loughmere - Innisfarne (vehicle ferry MV Corran)

Vessel: MV Corran is certified to carry no more than 60 cars per sailing. Height-restricted vehicles count as one car each.

07:15 sailing: heavy demand because of the Innisfarne cattle market. The deck was loaded to the certified maximum, and 12 cars in the queue were unable to board; they were offered places on the 09:30 sailing, and all 12 accepted. No other vehicles were in the queue.
09:30 sailing: 31 cars, including those carried over.
12:00 sailing: cancelled (engine alarm, cleared by 13:10).
14:45 sailing: 58 cars.

Passenger complaints: 4 (all about the 12:00 cancellation). Staff: full crew on all sailings.

Statement: 73 cars were in the queue for the 07:15 sailing.""",
   0, card=CONSIST, diff=2,
   twin=[("and 12 cars in the queue were unable to board; they were offered places on the 09:30 sailing, and all 12 accepted.",
          "and 13 cars in the queue were unable to board; they were offered places on the 09:30 sailing, and all 13 accepted.")],
   twin_gold=1),

it("A25", "choice",
   "Which of these statements is guaranteed by the choir director's email?",
   """From: Fenella Cartwright, Director of Music, St Aldhelm's Choral Society
To: Section leaders
Subject: Friday rehearsal and the chamber group

Dear all,

Thank you for a productive Friday. For the minutes: every member of the chamber group attended the Friday rehearsal, which I was glad to see before a concert.

On numbers more generally, I have been asked how much overlap there is between the sections and the chamber group. The honest answer is that most of the members of the choir who sing tenor also sing in the chamber group; very few basses do, and the sopranos and altos are somewhere in between.

I have not taken a register for the full choir on Friday, so please send me your section attendance by Tuesday.

With thanks,
Fenella""",
   S25[0], opts=S25,
   card="- Most tenors attended the Friday rehearsal: more than half of the choir's tenors were at the Friday rehearsal\n"
        "- Most members of the chamber group are tenors: more than half of the chamber group sing tenor\n"
        "- Every tenor attended the Friday rehearsal: each tenor in the choir was at the Friday rehearsal\n"
        "- Some member of the chamber group missed the Friday rehearsal: at least one chamber-group member was absent on Friday\n"
        "- No tenor missed the Friday rehearsal: not a single tenor was absent on Friday\n"
        "- none of these: none of the listed statements is guaranteed by the email",
   diff=3, twin=[("every member of the chamber group attended the Friday rehearsal, which I was glad",
                  "some members of the chamber group attended the Friday rehearsal, which I was glad")],
   twin_gold=NONE),

it("A26", "choice",
   "What is the status of the statement, given the panel minutes?",
   """Aldermoor Arts Trust - Grants Panel, minutes of the moderation meeting (extract)

Item 4: Riverside Mural Collective, application AR-118 (requested: 18,400 pounds)

The chair reminded the panel that the budget appendix to AR-118 had been circulated late, on the morning of the meeting. Discussion showed a clear pattern: no reviewer who read the appendix approved the budget as submitted, mainly because the scaffolding line was costed at twice the usual day rate. The chair also confirmed, from the reading log, that every reviewer on the finance sub-panel read the appendix before scoring.

Some reviewers outside the finance sub-panel scored the project highly on artistic merit.

Decision: the panel will offer a reduced award subject to a revised scaffolding quote. The officer will write to the applicant within ten working days.

Statement: No reviewer on the finance sub-panel approved the AR-118 budget as submitted.""",
   E, opts=L3[2], card=L3CARD, diff=2,
   twin=[("that every reviewer on the finance sub-panel read the appendix", "that some reviewer on the finance sub-panel read the appendix")],
   twin_gold=U),

]
