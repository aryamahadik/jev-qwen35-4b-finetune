"""proc_multihop / community, council and club administration (Hartwell District
Council, Riverside Youth League, Oakmere Libraries, Selby Green Allotments,
Crossfield Academy, Lantern Row Tenants' Association, Hartwell Leisure)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ cv01
# why: income = total income in last filed accounts INCLUDING restricted funds:
# 47,200 + 6,000 = 53,200 >= 50,000 -> ineligible. Previous grant 8 months ago is a bar
# only if its monitoring report is overdue (it was submitted).
# Twin: restricted 2,000 -> 49,200 -> eligible -> award.
C("cv01", "What decision should the grants officer make on application CG-114?",
"""
Hartwell District Council — Community Chest Grants 2026/27

Eligibility
E1. Applicants must be constituted community groups with a bank account in the group's name.
E2. Annual income must be under £50,000.
E3. (Amended May 2026) A group that received a Community Chest grant in the last 12 months is ineligible only if the monitoring report for that grant is overdue.
Awards: up to £2,000.

Guidance note 3 (Definitions): "annual income" means total income shown in the group's most recently filed accounts, including restricted funds and grants.

Application CG-114 — Riverside Youth Football Club
Constitution: adopted 2017. Bank account: Riverside Youth FC (club account).
Most recent filed accounts (year to 31 March 2026):
| Income line | Amount |
| unrestricted (subs, fundraising) | £47,200 |
| restricted (pitch drainage fund) | £6,000 |
Previous Community Chest grant: £1,500, eight months ago. Monitoring report submitted on time.
Amount requested: £2,000 (goalposts and nets).
""",
[("award_grant", "The club is constituted, has its own account, is under the income limit and its earlier grant does not bar it."),
 ("ineligible_income", "Counting restricted funds, the club's annual income is £50,000 or more."),
 ("ineligible_recent_grant", "The club received a grant within the last 12 months.")],
"ineligible_income", 2,
twin=T([("| restricted (pitch drainage fund) | £6,000 |", "| restricted (pitch drainage fund) | £2,000 |")], "award_grant")),

# ------------------------------------------------------------------ cv02
# why: age group by "season age" = age on 31 August at the start of the season. Born
# 15 Sep 2014; on 31 Aug 2026 age 11 -> U12. Age on match day (12) is the mistake.
# Twin: born 15 Aug 2014 -> 12 on 31 Aug 2026 -> U13.
C("cv02", "In which age group should Kit Mendes be registered for the 2026/27 season?",
"""
Riverside Youth League — Registration Rules 2026/27

R1. Players register in the age group matching their season age.
R2. "Season age" means the player's age on 31 August at the start of the season.
R3. Age groups: U11 = season age 10 or under; U12 = season age 11; U13 = season age 12; U14 = season age 13.
R4. Players may not play below their age group. Playing up one age group needs a parent's written consent and the club welfare officer's approval.

Registration form
Player: Kit Mendes
Date of birth: 15 September 2014
Club: Riverside Youth FC
First fixture: Saturday 19 September 2026
Parent note: "Kit wants to stay with his friends in the same group as last season (U11)."
""",
[("register_u11", "He may stay with last season's group so he plays with his friends."),
 ("register_u12", "His season age on 31 August 2026 is 11."),
 ("register_u13", "He will already be 12 by the first fixture, which puts him in U13.")],
"register_u12", 2,
twin=T([("Date of birth: 15 September 2014", "Date of birth: 15 August 2014")], "register_u13")),

# ------------------------------------------------------------------ cv03
# why: adult item 40 days x 20p = £8 -> capped at £6. Children's collection item never
# charged (even on an adult card). Member aged 45 -> no concession. Total £6.
C("cv03", "What overdue charge should Oakmere Libraries apply when these items come back?",
"""
Oakmere Libraries — Charges Policy

C1. Overdue items: 20p per day, up to a maximum of £6 per item.
C2. Items from the children's collection are never charged, whoever borrowed them.
C3. (From April) Concession members (aged 60 or over) pay no overdue charges.
C4. Lost items are charged at replacement cost.
C5. Charges are payable at any branch or online; unpaid charges above £10 block further borrowing.
C6. Items borrowed through the inter-library loan service follow the lending library's charges.

Returned today, member card 4401-2276 (adult, aged 45)
| Item | Collection | Days overdue |
| "The Salt Road" (novel) | adult fiction | 40 |
| "Otter's Big Day" (picture book) | children's | 40 |
""",
[("charge_6", "The novel's charge reaches the £6 cap and the picture book is free."),
 ("charge_8", "The novel is 40 days overdue at 20p a day, and the picture book is free."),
 ("charge_12", "Each item reaches the £6 cap."),
 ("no_charge", "The member qualifies for the concession, so nothing is charged.")],
"charge_6", 1),

# ------------------------------------------------------------------ cv04
# why: priority: (1) tenants who lost a plot to council redevelopment, (2) parish
# residents by application date, (3) non-residents by date. C lost a Moss Lane plot
# when the council redeveloped the site -> C first.
C("cv04", "Who should be offered plot 17 at Selby Green?",
"""
Selby Green Allotments — Letting Rules (Hartwell District Council)

L1. Vacant plots are offered in this order:
 (a) former plot-holders who lost a council plot because the council redeveloped the site;
 (b) residents of Selby Green parish, by date of application;
 (c) non-residents, by date of application.
L2. A former plot-holder whose tenancy was ended for non-payment or neglect has no priority under L1(a).

Waiting list (extract)
| Applicant | Resident of parish | Applied | Note |
| A. Farrant | yes | March 2023 | |
| B. Oduya | no | June 2021 | |
| C. Lisowski | yes | January 2024 | former Moss Lane plot-holder; site closed by the council in 2023 for housing redevelopment |

Plot 17 (half plot) became vacant on 1 April.
""",
[("offer_to_farrant", "Farrant is the longest-waiting parish resident."),
 ("offer_to_oduya", "Oduya has waited longest of anyone on the list."),
 ("offer_to_lisowski", "Lisowski lost a council plot to redevelopment, which puts them first under L1(a).")],
"offer_to_lisowski", 1),

# ------------------------------------------------------------------ cv05
# why: residential trip needs consent from a person with parental responsibility on a
# form dated on or after the trip letter's issue date (10 Feb). Mother has PR, but form
# dated 2 Feb (old form re-used) -> invalid -> obtain valid consent first.
# Twin: dated 12 Feb -> valid -> may attend.
C("cv05", "Can Leo Hartigan go on the Year 8 residential trip on the current paperwork?",
"""
Crossfield Academy — Educational Visits Policy (extract)

5.1 Residential and overseas trips need written consent from a person with parental responsibility (PR).
5.2 Emergency contacts who do not hold PR cannot give consent.
5.3 A consent form is valid only for the trip named on it and only if it is dated on or after the date the trip letter was issued.
5.4 Pupils without valid consent by the deadline cannot attend; the office should first try to obtain valid consent.

Trip letter: Year 8 residential, Ashcombe Outdoor Centre, 23-25 March. Issued 10 February. Consent deadline 6 March.

Pupil file — Leo Hartigan
PR holders: mother (Sarah Hartigan), father (Tom Hartigan)
Emergency contact: grandmother (Joan Price), no PR
Consent form received 3 March: "Year 8 residential, Ashcombe" — signed by Sarah Hartigan, dated 2 February.
""",
[("may_attend", "His mother holds parental responsibility and signed a consent form for this trip."),
 ("obtain_valid_consent", "The form is dated before the trip letter was issued, so it is not valid and a new one is needed before the deadline."),
 ("cannot_attend", "Consent forms with errors mean the pupil is removed from the trip.")],
"obtain_valid_consent", 2,
twin=T([("signed by Sarah Hartigan, dated 2 February.", "signed by Sarah Hartigan, dated 12 February.")], "may_attend")),

# ------------------------------------------------------------------ cv06
# why: PEN needed when people present exceed 499; "people present" includes staff,
# volunteers and performers. 350 + 40 + 12 = 402 -> no PEN. Amplified music ends 22:30,
# before 23:00 -> no noise permit. -> standard notification only.
C("cv06", "Which permit does the Lantern Row summer fair need?",
"""
Hartwell District Council — Outdoor Events Guidance

1. A Premises Event Notice (PEN) is required for any event where more than 499 people will be present at one time.
2. "People present" includes ticket holders, walk-in visitors, staff, volunteers and performers.
3. A noise permit is required for amplified music after 23:00.
4. All other outdoor events on council land need only the standard event notification (5 working days before).

Event plan — Lantern Row Summer Fair (council green)
Expected visitors at peak: 350
Stewards and stallholders: 40
Performers: 12
Amplified music: 18:00-22:30 (DJ tent)
Bar: none
Organiser note: "We had nearly 600 through the gate over the whole day last year, but never more than about 350 at once."
""",
[("standard_notification_only", "Peak numbers including staff and performers stay under 500 and the music ends before 23:00."),
 ("premises_event_notice", "More than 499 people will be present, counting everyone on site."),
 ("noise_permit", "The event has amplified music in the evening, which needs a noise permit.")],
"standard_notification_only", 2),

# ------------------------------------------------------------------ cv07
# why: room sublet allowed with approval, up to 12 months, while away for work/study;
# rent charged to subtenant must not exceed the member's own charge for that room
# (£540). Proposed £620 -> refuse on rent.
C("cv07", "How should the co-op committee decide sublet request SL-09?",
"""
Lantern Row Housing Co-operative — Subletting Rules

S1. A member may sublet their room, with committee approval, for up to 12 months while away for work or study.
S2. Subletting a whole flat is not allowed.
S3. The rent charged to the subtenant must not exceed the member's own monthly charge for that room.
S4. The subtenant must be told in writing that they are not a co-op member.

| Unit | Member | Monthly charge |
| Flat 3, room B | Ade Coker | £540 |

Request SL-09
Member: Ade Coker, Flat 3 room B
Reason: study placement in Veloria, September to April (8 months)
Proposed subtenant: Mina Rahimi, for room B only
Proposed rent to subtenant: £620 per month (includes a £80 "furnishing fee")
""",
[("approve_sublet", "The member is away for study for under 12 months and is subletting only the room."),
 ("refuse_whole_unit", "Subletting any part of a co-op flat counts as subletting the whole flat."),
 ("refuse_rent_too_high", "The subtenant would pay more than the member's own charge for the room.")],
"refuse_rent_too_high", 2),

# ------------------------------------------------------------------ cv08
# why: quorum = lower of 20% of 180 (36) and 30 -> 30; 33 present -> quorate. Spending
# over £1,000 needs two-thirds of votes cast; abstentions not cast. Cast = 20 + 9 = 29;
# 20/29 = 69% -> passes. Twin: 19 for, 10 against -> 19/29 = 65.5% -> fails.
C("cv08", "What is the outcome of motion M4 at the Lantern Row Tenants' Association meeting?",
"""
Lantern Row Tenants' Association — Constitution (extract)

7. Quorum: 20% of members or 30 members, whichever is lower. No decision can be taken at an inquorate meeting.
8. Decisions are by simple majority of votes cast, except that any spending over £1,000 needs at least two-thirds of votes cast.
9. Abstentions are not votes cast.

Minutes — General meeting, 14 May
Members on roll: 180. Members present: 33.
Motion M4: spend £1,500 on new noticeboards and a stairwell mural.
Vote: for 20; against 9; abstain 4.
Chair's comment: "Fewer than two-thirds of the people in the room voted for it, so I think this falls."
""",
[("motion_passes", "The meeting was quorate and the motion won at least two-thirds of the votes cast."),
 ("motion_fails", "The motion did not reach two-thirds support under the constitution's counting rule."),
 ("meeting_inquorate", "Fewer than 20% of the 180 members attended, so no decision could be taken.")],
"motion_passes", 3,
twin=T([("Vote: for 20; against 9; abstain 4.", "Vote: for 19; against 10; abstain 4.")], "motion_fails")),

# ------------------------------------------------------------------ cv09
# why: concession needs a valid card; student cards valid until printed expiry (31 Aug).
# Visit 3 Sep -> card expired -> full adult price (registration irrelevant).
C("cv09", "Which price should reception charge Esme Varga at Hartwell Leisure on 3 September?",
"""
Hartwell Leisure — Swimming Prices and Concessions

1. Adult swim: £5.40. Concession swim: £3.20.
2. Concessions are available to (a) full-time students holding a valid student card, (b) people aged 65 or over, (c) holders of a Hartwell Access Card.
3. A student card is valid until the expiry date printed on it.
4. (From June) Concession cards must be registered at reception once before first use.
5. Children under 4 swim free with a paying adult.

Customer at reception, Wednesday 3 September
Esme Varga, aged 22. Shows Kelbrook College student card, printed expiry 31/08. Card registered at reception in June.
Esme: "I'm starting my second year in a fortnight."
""",
[("concession_price", "She is a full-time student who registered her card at reception in June, so the concession price applies today."),
 ("adult_price", "Her student card expired before today, so she has no valid concession card."),
 ("refuse_entry", "Customers presenting an expired card cannot swim until it is renewed.")],
"adult_price", 1),

# ------------------------------------------------------------------ cv10
# why: overtime charge: £1 per started 15 min beyond 30 min -> 52 min = 22 min over -> 2
# blocks -> £2. Refund if a dock fault at the return station is logged within 5 min of
# the attempted return: attempt 14:05, fault logged 14:07 -> refund £2.
# Twin: fault logged 14:15 -> 10 min -> no refund.
C("cv10", "How should the bike-share helpdesk resolve complaint BS-4471?",
"""
Hartwell Bikes — Charges and Refunds

1. Rides up to 30 minutes are free for members. Beyond 30 minutes, £1 is charged for each started 15-minute block.
2. Overtime charges are refunded if the member tried to return the bike at a dock that failed, and the system logged a fault at that dock within 5 minutes of the attempted return.
3. Refunds are made to the member's account.

Ride record R-99102
Start 13:40, Station 3. End 14:32, Station 9. Duration 52 minutes. Charged: £2.
Member's complaint: "I tried to dock at Station 14 at 14:05 but the dock wouldn't lock, so I had to ride on to Station 9."
App log: attempted return at Station 14, dock 6, 14:05.
Fault log: Station 14 dock 6 "lock failure" logged 14:07.
""",
[("refund_2", "A fault was logged at the dock within 5 minutes of the attempted return, so the overtime charge is refunded."),
 ("refund_1", "Only the first overtime block is refunded because the second came after the failed dock."),
 ("no_refund", "The dock fault was not logged within 5 minutes of the attempted return.")],
"refund_2", 2),

# ------------------------------------------------------------------ cv11
# why: limit 3 parcels in any 6 months; window for request on 12 Jul = 12 Jan to 12 Jul.
# Parcels 2 Jan (outside), 20 Feb, 2 Apr -> 2 in window -> issue. Agency is on the list.
C("cv11", "What should the food bank coordinator do with referral FB-2290?",
"""
Hartwell Community Food Bank — Referral Rules

1. Parcels are issued only on referral from an agency on the Approved Referrers list. Self-referrals are signposted to an approved agency.
2. A household may receive up to 3 parcels in any 6-month period, counted back from the date of the new referral.
3. A referral that would exceed rule 2 goes to a caseworker review instead.

Approved Referrers (extract): Hartwell Citizens Advice; Crossfield Academy family support; Riverside GP practice social prescriber.

Referral FB-2290, dated 12 July
Referrer: Hartwell Citizens Advice
Household: 2 adults, 3 children
Previous parcels: 2 January, 20 February, 2 April.
""",
[("issue_parcel", "Only two of the household's parcels fall within the last 6 months."),
 ("caseworker_review", "The household has already had three parcels, so another needs caseworker review."),
 ("signpost_to_agency", "The referral did not come from an approved agency.")],
"issue_parcel", 2),

# ------------------------------------------------------------------ cv12
# why: household income excludes child benefit: 21,500 + 9,800 = 31,300 < 32,000 ->
# income ok. Residence: moved Aug 2023, application Oct 2026 -> over 3 years -> award.
C("cv12", "Should the Hartwell Futures bursary panel award a bursary to Noor Adeyemi?",
"""
Hartwell Futures Bursary — Eligibility

B1. Household income below £32,000.
B2. The student has lived in Hartwell District for at least 3 years at the application date.
B3. The student is starting a first undergraduate or apprenticeship programme.

Definitions: "household income" means the gross income of the student's parents or guardians in the last complete tax year before the application, excluding child benefit.

Application received 15 October 2026 — Noor Adeyemi
Programme: first-year degree apprenticeship in civil engineering
Address history: moved to Hartwell District in August 2023
Last complete tax year:
| Source | Amount |
| parent 1 salary | £21,500 |
| parent 2 salary | £9,800 |
| child benefit | £1,900 |
""",
[("award_bursary", "Without child benefit, household income is under £32,000, and she has lived in the district for over 3 years."),
 ("ineligible_income", "Total household income across all sources is above £32,000."),
 ("ineligible_residence", "She has lived in the district for less than 3 years.")],
"award_bursary", 2),

# ------------------------------------------------------------------ cv13
# why: keep pitch if attended >= 80% of market days in the quarter; days cancelled by the
# council are not market days. 13 scheduled - 1 cancelled (storm) = 12; attended 10 ->
# 83% -> keep. Twin: no cancellation (the storm day went ahead and she was absent) ->
# 10/13 = 77% -> pitch offered to waiting list.
C("cv13", "What should the market manager decide on Delia Frost's pitch for next quarter?",
"""
Hartwell Market — Regular Trader Rules

M1. A regular trader keeps their pitch for the next quarter if they traded on at least 80% of market days in the current quarter.
M2. Days cancelled by the council (weather, emergencies) are not market days for M1.
M3. A trader below 80% loses the pitch, which is offered to the waiting list.
M4. Traders may not sublet pitches.
M5. Pitch fees are payable monthly in advance.

Quarter summary (Q2)
Scheduled Saturdays: 13
Council cancellations: 1 (7 June, storm warning)

Trader: Delia Frost (pitch 22, bread and cakes)
Saturdays traded: 10
Absences: 7 June; 21 June (family wedding, notified); 12 July (illness, notified)
""",
[("keep_pitch", "Leaving out the council-cancelled day, she traded on at least 80% of market days."),
 ("offer_to_waiting_list", "She traded on fewer than 80% of market days in the quarter."),
 ("issue_warning_only", "Both of her other absences were notified in advance, and absences with notice lead to a warning rather than loss of the pitch.")],
"keep_pitch", 2,
twin=T([("Council cancellations: 1 (7 June, storm warning)", "Council cancellations: none")], "offer_to_waiting_list")),

# ------------------------------------------------------------------ cv14
# why: charity rate 50%, but an event charging admission above £5 is "commercial" for the
# hire tariff whoever runs it -> £8 ticket -> full price.
C("cv14", "Which hire rate applies to the Aldermoor Hospice quiz night booking?",
"""
Hartwell Community Centre — Hire Tariff

T1. Commercial hire: full rate (£42 per hour).
T2. Registered charities: 50% of full rate.
T3. Unregistered community groups: 75% of full rate.
T4. Definitions: an event is "commercial" if it is run for profit or charges admission above £5 per person, whoever organises it.
T5. A refundable damage deposit of £100 is taken for all evening bookings.
T6. Bookings must end by 23:00, and the hall must be cleared by 23:30.

Booking HB-771
Hirer: Aldermoor Hospice (registered charity no. 1109932)
Event: fundraising quiz night, main hall, 19:00-22:30
Tickets: £8 per person, all proceeds to the hospice
""",
[("charity_rate_50", "The hirer is a registered charity and every penny from the tickets goes to the hospice, so the charity rate applies."),
 ("community_rate_75", "Fundraising events count as community activity."),
 ("full_commercial_rate", "Admission above £5 makes the event commercial under T4, whoever organises it.")],
"full_commercial_rate", 2),

# ------------------------------------------------------------------ cv15
# why: notice needed for trees with trunk diameter >= 75 mm measured at 1.5 m above ground.
# 90 mm at 1.5 m -> notice. Dead/dangerous exemption needs written arborist evidence;
# owner's own view is not evidence.
C("cv15", "What must the owner of 12 Mill Lane do before felling the apple tree?",
"""
Hartwell District Council — Trees in Conservation Areas (guidance)

1. Anyone planning to cut down or prune a tree in a conservation area must give the council 6 weeks' written notice, if the trunk diameter is 75 mm or more.
2. Trunk diameter is measured 1.5 m above ground level. For multi-stemmed trees, measure the largest stem.
3. No notice is needed for a tree that is dead or dangerous, if the owner holds written evidence from a qualified arborist.

Enquiry from the owner of 12 Mill Lane (Old Town Conservation Area)
"I want to take down the old apple tree at the back. It measures about 160 mm across at the base and 90 mm at chest height (around 1.5 m). Honestly it's half dead and hardly fruits any more. Do I need to tell anyone?"
""",
[("no_notice_needed", "The owner says the apple tree is half dead and hardly fruits, so it falls under the dead or dangerous tree exemption."),
 ("give_six_weeks_notice", "The trunk is at least 75 mm at 1.5 m and there is no arborist's evidence, so notice is required."),
 ("apply_for_full_consent", "Felling any tree in a conservation area needs full planning consent.")],
"give_six_weeks_notice", 1),

# ------------------------------------------------------------------ cv16
# why: weekly volunteer = not occasional (occasional = no more than 3 sessions in any 30
# days) -> needs a current Harbour Check; valid 3 years; issued 3.5 years ago -> expired ->
# renew before next session. Twin: issued 2 years ago -> current -> continue.
C("cv16", "What should the club welfare lead decide about volunteer Sam Ivers?",
"""
Riverside Youth League — Volunteer Safeguarding Rules

V1. Volunteers working with under-18s need a current Harbour Check (enhanced background check).
V2. A Harbour Check is current for 3 years from its issue date.
V3. Exemption: an occasional volunteer who is always supervised by an adult with a current Harbour Check does not need one. "Occasional" means no more than 3 sessions in any 30-day period.
V4. A volunteer whose check has expired may not volunteer until the renewal is issued.

Volunteer record — Sam Ivers
Role: assistant coach, U10 Saturday training (every Saturday, supervised by head coach)
Harbour Check issued: 3.5 years ago
Head coach: current Harbour Check
""",
[("continue_volunteering", "Sam holds a current Harbour Check, or is exempt as an occasional supervised volunteer."),
 ("pause_until_check_renewed", "Weekly sessions are not occasional, and Sam's check is more than 3 years old."),
 ("exempt_supervised", "Because the head coach supervises every session, Sam does not need a check.")],
"pause_until_check_renewed", 2,
twin=T([("Harbour Check issued: 3.5 years ago", "Harbour Check issued: 2 years ago")], "continue_volunteering")),

# ------------------------------------------------------------------ cv17
# why: a return collection is due only if the bin was presented by 06:30 AND the miss is
# reported within 48 hours. Crew passed 06:50; resident put bin out 06:55 -> not
# presented by 06:30 -> next scheduled collection. Report timing is irrelevant then.
C("cv17", "How should the waste team respond to missed-bin report MB-3150?",
"""
Hartwell District Council — Household Waste Collections

W1. Bins must be presented at the kerbside by 06:30 on collection day.
W2. If a presented bin is missed and the resident reports it within 48 hours, the crew returns within 2 working days.
W3. Bins not presented by 06:30 are emptied at the next scheduled collection. A paid special collection may be booked at £28.

Crew log, Tuesday, round 7
06:50 Ferndale Close, No. 9 — no bin at kerbside.

Report MB-3150, Tuesday 18:10
Resident, 9 Ferndale Close: "My general waste bin wasn't emptied. I put it out just before 7 as I left for work, at about 06:55."
""",
[("schedule_return_collection", "The miss was reported within 48 hours, so the crew must return within 2 working days."),
 ("empty_at_next_round", "The bin was not presented by 06:30, so it waits for the next scheduled collection."),
 ("charge_special_collection", "A missed bin has to be booked as a paid special collection.")],
"empty_at_next_round", 1),

# ------------------------------------------------------------------ cv18
# why: second permit only if 2+ drivers AND no off-street parking; off-street parking
# includes a garage or driveway whether or not used for parking -> garage -> refuse.
C("cv18", "Should the parking team issue a second resident permit to 5 Orchard Walk?",
"""
Hartwell District Council — Zone H Resident Parking

P1. Each household may have one resident permit.
P2. A second permit may be issued if at least two household members hold driving licences and the property has no off-street parking.
P3. Definitions: "off-street parking" means any driveway, garage or parking space belonging to the property, whether or not it is currently used for parking.
P4. Visitor permits (up to 50 days a year) are available to every household.

Application — 5 Orchard Walk
Drivers in household: 2 (both licences checked)
Property: terraced house with a single garage at the rear
Applicant note: "Please ignore the garage, we use it for storage and the bikes."
Existing permits: 1 resident permit.
""",
[("issue_second_permit", "Two drivers live at the property and its garage is not used for parking."),
 ("refuse_second_permit", "The property has a garage, which counts as off-street parking."),
 ("issue_visitor_permits_only", "Households with two drivers must use visitor permits for the second car.")],
"refuse_second_permit", 1),
]
