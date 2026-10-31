"""Part A1: monotonicity with quantifiers (restrictor vs scope, numbers, only, neither/nor)."""
from _h import it, L3, L3CARD, FOLLOW, RULED, E, C, U, NONE

ITEMS = [

it("A1", "noul",
   "If everything in the email is true, must the statement be true?",
   """From: Building Services <services@marlowcourt.example>
To: All residents, Marlow Court
Subject: East lot enforcement, Friday 14 March

Residents,

As announced in February, the east lot is reserved after 9 p.m. for the night-shift staff of the clinic next door. On Friday our security contractor, Ardent Patrol, walked the lot at 9:40 p.m. and again at 11:15 p.m.

Every fourth-floor resident whose car was in the east lot at the 9:40 p.m. walk received a written warning. Residents from other floors were handled separately, and some of them were only spoken to. Warnings carry no fee this time, but a second occurrence within six months will be towed at the owner's expense.

If you think you were warned in error, reply to this email with your bay number and a photo of your permit.

Building Services

Statement: Every fourth-floor resident whose car was in the east lot at both the 9:40 p.m. and the 11:15 p.m. walks received a written warning.""",
   1, card=FOLLOW, diff=2,
   twin=[("Every fourth-floor resident whose car was in the east lot at the 9:40",
          "One fourth-floor resident whose car was in the east lot at the 9:40")], twin_gold=0),

it("A2", "choice",
   "Judged against the deviation report, which label fits the statement?",
   """Deviation report DR-2291 - Quellin Biobank, Cold Chain Unit
Prepared by: T. Asante, QA technician

Summary: Freezer F-7 alarmed at 02:14 on 4 June after a door-seal failure. Samples from three incoming batches (received 1 June, 2 June and 3 June) were moved to backup unit F-9 by 02:40. F-9 stayed within its 2-8 degC specification for the whole transfer window.

Samples from the 1 June and 2 June batches had been placed on the top shelf of F-7, nearest the failed seal; logger probe P3 on that shelf peaked at 14.9 degC before transfer. Samples from the 3 June batch sat on the bottom shelf.

Conclusion recorded by QA after reviewing every probe trace: no sample from the batch received on 3 June was stored above 8 degC at any point. The 1 June and 2 June batches are quarantined pending a stability review; the 3 June batch is released to the study team.

Statement: No sample from the 3 June batch was stored above 12 degC at any point.""",
   E, opts=L3[0], card=L3CARD, diff=2,
   twin=[("stored above 12 degC at any point.", "stored above 5 degC at any point.")], twin_gold=U),

it("A3", "noul",
   "Does the post guarantee the statement?",
   """#product-research - thread: "Layout v3 survey, first cut"

Maren Oduya (UX research): Posting the headline numbers before the full deck. The in-app survey closed Sunday with 1,212 complete responses. 640 respondents told us they use the app daily; the rest split between weekly and "a few times a month". We asked everyone to rate the new layout from 1 (much worse) to 5 (much better).

Headline: most of the respondents who use the app daily rated the new layout 4 or 5. Weekly users were more mixed - roughly a third gave it a 2 or lower, mostly complaining that the budget tab moved. We have not cut the data by age, plan type or sign-up date yet; that comes Thursday.

Juno Park (PM): Nice. Can we say daily users like it in the release notes?

Maren Oduya: I'd rather wait for the cuts, but the headline stands.

Statement: Most of the respondents who use the app daily rated the new layout 3 or higher.""",
   1, card=FOLLOW, diff=2,
   twin=[("who use the app daily rated the new layout 3 or higher",
          "who use the app daily and signed up this year rated the new layout 3 or higher")], twin_gold=0),

it("A4", "choice",
   "Taking the memo as accurate, how should the statement be labelled?",
   """INTERNAL MEMO - Pellworth Construction, Site Security
Re: Access badges, Hallam Road site

The Hallam Road site closed on 30 June. Contractors worked there in two waves: the groundworks wave (March-April) and the fit-out wave (May-June); a few firms were present in both.

Status as of this morning:
- Every contractor who worked on the Hallam site in May has returned their access badge; the fit-out firms were very good about this.
- Not every contractor who worked on the Hallam site has returned their access badge. Deactivated badges are still badges, and we need them back for the audit.

Please chase your own subcontractors. Unreturned badges will be charged at 40 pounds each against the final invoice.

R. Okafor, Site Security Lead

Statement: Some contractor who worked on the Hallam site did not work there in May.""",
   E, opts=L3[1], card=L3CARD, diff=3,
   twin=[("Every contractor who worked on the Hallam site in May has returned",
          "At least one contractor who worked on the Hallam site in May has returned")], twin_gold=U),

it("A5", "choice",
   "According to the inspection summary, how many of the five level-B fire doors failed the latch test?",
   """Brightwater Hospital - Estates Department
Annual fire-door inspection, Level B (summary for the compliance file)

Inspector: Colm Hardacre, Hardacre Fire Safety Ltd
Doors in scope: B1, B2, B3, B4, B5 (all FD60 with self-closers)

Findings:
1. At most two of the five level-B doors failed the latch test.
2. Door B3 failed the latch test: the latch did not engage on three of five releases.
3. Doors B1 and B2 are the pair on the north corridor and share a single hold-open magnet circuit; for that reason they were tested together and, as recorded on the test sheet, they either both passed or both failed.
4. Doors B4 and B5 passed the latch test. B5 has a scuffed intumescent strip, which is a separate finding (see item 6).
5. All five doors passed the gap test.
6. Remedial works: replace the B5 strip within 30 days; repair any failed latch within 7 days.

Signed off by the Estates Manager on 12 September.""",
   "exactly one",
   opts=["none", "exactly one", "exactly two", "three or more", "the passage does not settle this"],
   card="- none: no level-B fire door failed the latch test\n"
        "- exactly one: one level-B door failed the latch test and the other four passed\n"
        "- exactly two: two level-B doors failed the latch test and three passed\n"
        "- three or more: at least three level-B doors failed the latch test\n"
        "- the passage does not settle this: more than one of the other answers is consistent with the summary",
   diff=3, twin=[("At most two of the five level-B doors", "At most three of the five level-B doors")],
   twin_gold="the passage does not settle this"),

it("A6", "noul",
   "Accepting every line of the minutes, does the statement follow?",
   """Orchard Lane Allotment Association - Minutes of the AGM, 9 February
Present: 41 plot holders. Chair: Bettina Kroll. Minutes: Sami Adeyemi.

1. Apologies from four plot holders.
2. Levy. The treasurer reported that 38 of the 45 plot holders have paid the 2026 levy. Ines Marchetti asked why the levy rose by 6 pounds and said she thought the increase had not been properly notified; the chair agreed to publish the notice again on the gate board.
3. Vote on the new water-butt scheme. Only plot holders who had paid the 2026 levy voted on the motion. The motion passed 31 to 7. Ines Marchetti voted against and asked for her objection to be minuted.
4. Any other business: the hedge on the east boundary is to be cut in March.

Meeting closed at 20:45.

Statement: Ines Marchetti had paid the 2026 levy.""",
   1, card=FOLLOW, diff=2,
   twin=[("Only plot holders who had paid the 2026 levy voted", "All plot holders who had paid the 2026 levy voted")],
   twin_gold=0),

it("A7", "choice",
   "Given only the dispatch log, what is the status of the statement?",
   """Corvel Freight - Depot 3 dispatch log, Tuesday 18 November (night supervisor notes)

18:05 Gate rule reminder posted: no shipment leaves Depot 3 without a signed manifest. Guard Petrov confirmed the gate scanner blocks any trailer whose manifest is unsigned.
18:40 Shipments 44-H and 44-J loaded and signed off; both left at 19:10.
19:25 Shipment 44-K loaded on trailer T-118. Driver Aldana waiting on customs paperwork.
21:50 Customs paperwork for 44-K received by email. The manifest for shipment 44-K was never signed; the shift lead went home sick at 21:30 and nobody else holds signing rights tonight.
22:30 Trailer T-118 moved to bay 9 to free the loading dock.
23:59 End of log. Rule held all night: no shipment left Depot 3 on Tuesday without a signed manifest.

Statement: Shipment 44-K left Depot 3 on Tuesday.""",
   C, opts=L3[2], card=L3CARD, diff=2),

it("A8", "noul",
   "Must the statement be true if the editor's email is accurate?",
   """From: Dr. Halvard Emsley, Handling Editor, Journal of Coastal Hydrology
To: Dr. Rukmini Sato
Subject: Decision on manuscript JCH-2026-0412

Dear Dr. Sato,

Thank you for your patience. Your manuscript "Tidal pumping in perched beach aquifers" received five reviews. I will be frank about the spread: fewer than three of the reviewers recommended rejection, and at least one reviewer recommended acceptance without changes. The remaining reports asked for revisions of varying size, mostly about the boundary conditions in section 4.

Given that spread, I am not able to accept the paper in its current form, but I am inviting a major revision. Please respond to every point in every report, including the ones that recommended rejection.

The revised version is due within 90 days.

Best wishes,
Halvard Emsley

Statement: At most two of the five reviewers recommended rejection.""",
   1, card=FOLLOW, diff=1,
   twin=[("fewer than three of the reviewers recommended rejection", "fewer than four of the reviewers recommended rejection")],
   twin_gold=0),

it("A9", "choice",
   "Which of these paramedics must have completed the sedation module by 30 April?",
   """Northfold Ambulance Service - Clinical Education Bulletin, 5 May

Procedural sedation module (mandatory): compliance update

Every paramedic on B-shift except those rostered to the airport unit completed the new sedation module by 30 April. A-shift compliance is still being collated and will be reported next week. Airport-unit staff were given until 31 May because of the terminal refit.

Staff mentioned in this bulletin (shift and unit as rostered for April):
- Oskar Lindqvist - A-shift, city unit. Led two of the practical sessions as a facilitator.
- Priya Venkataraman - B-shift, airport unit. Asked for the module slides to be shared.
- Tomasz Wrona - B-shift, city unit. Moved to the training desk on 1 May.
- Adaeze Nwosu - A-shift, airport unit.
- Leila Farouk - C-shift (relief), city unit. Has asked to join the June cohort.
- Hamish Doyle - B-shift, airport unit. Was on leave for most of April.

Queries to education@northfold-ambulance.example.""",
   "Tomasz Wrona",
   opts=["Oskar Lindqvist", "Priya Venkataraman", "Tomasz Wrona", "Adaeze Nwosu", "Leila Farouk", "Hamish Doyle", NONE],
   card="- Oskar Lindqvist: the A-shift city-unit paramedic who facilitated sessions\n"
        "- Priya Venkataraman: the B-shift airport-unit paramedic who asked for the slides\n"
        "- Tomasz Wrona: the B-shift paramedic who moved to the training desk on 1 May\n"
        "- Adaeze Nwosu: the A-shift airport-unit paramedic\n"
        "- Leila Farouk: the C-shift relief paramedic\n"
        "- Hamish Doyle: the B-shift airport-unit paramedic who was on leave\n"
        "- none of these: the bulletin does not guarantee completion for any listed paramedic",
   diff=2, twin=[("- Tomasz Wrona - B-shift, city unit.", "- Tomasz Wrona - B-shift, airport unit.")],
   twin_gold=NONE),

it("A10", "choice",
   "Which inference label applies to the statement, given the incident review?",
   """Subject: Incident review - private dining room, Saturday 7 June
From: Ottilie Brandt, General Manager, The Salt Loft
To: Kitchen leads; Front-of-house leads

Team,

Following the complaint from the Varga party (32 covers, private dining room), I have gone through the ticket log and the pass timestamps with Chef Imani.

What the log shows: the party pre-ordered from a set menu with three mains - the hake, the mushroom risotto and the lamb shoulder. Every guest who ordered the hake or the risotto was served their main before 8:30 p.m. The lamb was the problem: the second shoulder went into the oven late, and the last lamb plates went out at 9:05 p.m., which is what the host complained about.

Actions: lamb shoulders for private parties go in at the same time from now on, and front of house will tell the host if any course is running more than 15 minutes behind.

Ottilie

Statement: Every guest in the Varga party who ordered the hake was served their main before 8:30 p.m.""",
   E, opts=L3[3], card=L3CARD, diff=2),

it("A11", "noul",
   "Based only on the change record, is the statement guaranteed?",
   """CHANGE RECORD CHG-77120 - Harrowgate Mutual IT Operations
Title: Emergency patch KB-5561 (VPN client) - rollout status
Owner: Desktop Engineering

Scope: 212 corporate laptops across Finance, Claims, Underwriting and HR.

Status at close of window (Sunday 23:00):
- Claims and Underwriting: installed and verified on all devices.
- HR: installed on 18 of 19 devices; one device was powered off and will receive the patch at next check-in.
- Finance: the patch was not installed on any of the finance laptops. The finance fleet runs an older client build that the vendor package rejects; the vendor has promised a compatible package on Wednesday.

Risk note: devices without the patch remain exposed to the VPN credential-replay issue. Finance staff have been asked to use the virtual desktop until the patch lands.

Statement: None of the finance laptops has the patch installed.""",
   1, card=FOLLOW, diff=1,
   twin=[("the patch was not installed on any of the finance laptops", "the patch was not installed on all of the finance laptops")],
   twin_gold=0),

it("A12", "choice",
   "Given only the newsletter, the statement is best labelled as which of these?",
   """Kestrel Vale District Council - Community Newsletter, Autumn edition

Recycling Challenge: results

Thank you to the 1,840 households who signed up to this summer's Recycling Challenge. Households weighed their sorted recycling at the depot each Saturday from June to August, and the scales printed a running total on each household's card.

Every household that recycled at least 20 kg over the summer received a 15-pound voucher for the Vale market, and every household that recycled at least 60 kg was also entered into the draw for a compost bin. The median household total was 34 kg. The top household - a family of six on Ashby Crescent - recycled 212 kg.

Vouchers not collected by 30 November will be donated to the food bank.

Statement: Every household that recycled at least 30 kg over the summer received a 15-pound voucher for the Vale market.""",
   E, opts=L3[4], card=L3CARD, diff=2),

it("A13", "noul",
   "Is the statement ruled out by the quarterly summary?",
   """Tessaline Group - Talent Operations: Q2 summary for the regional leadership call

Hiring. Group-wide we closed 146 of the 170 roles planned for Q2 (86%). Neither the Oslo nor the Lyon office met its Q2 hiring target. Oslo lost two senior offers to counter-offers late in June; Lyon's engineering pipeline was strong, and the Lyon team made more offers than any other office, but its acceptance rate fell to 61%.

Retention. Voluntary attrition was 2.1% for the quarter, down from 2.6% in Q1. Lyon had the lowest attrition in the group.

Onboarding. The new 30-60-90 checklist is live everywhere except Oslo, where it launches on 1 August.

Asks for leadership: approve two additional recruiter contracts for Q3 and agree the revised referral bonus.

Statement: The Lyon office met its Q2 hiring target.""",
   1, card=RULED, diff=2,
   twin=[("Neither the Oslo nor the Lyon office met its Q2 hiring target.",
          "Not both the Oslo and the Lyon office met their Q2 hiring targets.")], twin_gold=0),

]
