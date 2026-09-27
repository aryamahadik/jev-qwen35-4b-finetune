"""proc_longpolicy / council schemes, permits, public services and local charges."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ cv01
# why: amendment (applications from 1 Apr 2025) makes a company car eligible with an employer
# letter confirming exclusive private use; household has one permit, so this is the second
# (limit 2) at £120. Twin: employer letter says pool vehicle -> not exclusive -> not an
# Eligible Vehicle -> refuse.
C("cv01", "What decision should the parking permits team make on the application?",
"""
PELLMORE BOROUGH COUNCIL — RESIDENTS' PARKING SCHEME, ZONE K (terms and conditions)

1. DEFINITIONS
1.1 "Eligible Resident" means a person whose main home is an address inside Zone K.
1.2 "Eligible Vehicle" means a car or small van of up to 3.5 tonnes whose registered keeper is the Eligible Resident at their Zone K address.
1.3 "Household" means all people living at the same address.
1.4 "Permit Year" means 12 months from the date of issue.

2. PERMITS
2.1 A Household may hold up to 2 resident permits at any time.
2.2 The fee for a Household's first permit is £80 a year; for a second permit, £120 a year.
2.3 Permits are virtual and linked to the vehicle registration number.

3. VISITOR PERMITS
3.1 Each Household may buy up to 50 one-day visitor permits a year at £2.50 each.

4. EVIDENCE
4.1 Applicants must provide proof of address dated within the last three months.
4.2 Applicants must provide the vehicle registration certificate.

5. REFUNDS
5.1 Unused whole months are refunded, less £10, if a permit is surrendered.

6. ENFORCEMENT
6.1 Vehicles without a valid permit in a resident bay may receive a penalty charge of £70.

7. CHANGES OF VEHICLE
7.1 A permit may be moved to a replacement vehicle for a £10 fee, on the same evidence as a new application.

8. MISUSE
8.1 A permit obtained with false information will be cancelled without refund.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

AMENDMENT — Cabinet decision, applies to applications received on or after 1 April 2025
A1. The definition of Eligible Vehicle is extended: "It also includes a company or leased car where the registered keeper is the employer or leasing company, provided the Eligible Resident supplies a letter from the employer or leasing company confirming that the car is for the resident's exclusive private and business use."
A2. Clause 4.2 is satisfied by the registration certificate together with that letter.

APPLICATION PK-44120 — received 3 June 2025
Applicant: Lowri Beddoe, 17 Sorrel Street, Zone K (council tax record confirms main home).
Vehicle: company car, registered keeper Fairlight Engineering Ltd, Cheadle Park.
Evidence: tenancy agreement dated 2 May 2025; registration certificate; letter from Fairlight Engineering's fleet manager confirming exclusive private and business use by Ms Beddoe.
Household permits already held: one, for her partner's car.
Previous notes on the account: "2023 — company car application refused, not registered keeper."
""",
[("issue_second_permit_120", "Under the amendment the company car is an Eligible Vehicle with the employer's letter, and as the Household's second permit it costs £120."),
 ("refuse_not_eligible_vehicle", "The car does not meet the Eligible Vehicle definition as it applies to this application, so no permit can be issued."),
 ("issue_permit_80", "The company car qualifies under the amendment, and each Eligible Resident's first permit costs £80 whatever other permits the Household already holds."),
 ("refuse_household_limit", "The Household already holds a permit, so it has reached its limit.")],
"issue_second_permit_120", 2,
twin=T([("confirming exclusive private and business use by Ms Beddoe", "confirming the car is a pool vehicle shared by several staff and kept by Ms Beddoe on some weeknights")], "refuse_not_eligible_vehicle")),

# ------------------------------------------------------------------ cv02
# why: 2025/26 fee schedule: annual £1,320, charged per quarter or part quarter remaining.
# Consent from 10 Aug 2025: Jul-Sep (part), Oct-Dec, Jan-Mar = 3/4 x 1,320 = £990. Standard
# trader, no concession. Twin: registered Community Trader -> 50% -> £495.
C("cv02", "What fee should the licensing team charge for the new street trading consent?",
"""
HARTWICK CITY COUNCIL — STREET TRADING CONSENTS: FEES AND CONDITIONS

1. DEFINITIONS
1.1 "Licensing Year" means 1 April to 31 March.
1.2 "Pitch" means a numbered trading space on a consent street.
1.3 "Community Trader" means a trader registered with the Council as a non-profit organisation trading to raise funds for its objects.
1.4 "Quarter" means April–June, July–September, October–December or January–March.

2. FEES (2024/25)
2.1 The fee for a Pitch consent is £1,200 for a full Licensing Year.
2.2 A consent granted part-way through a Licensing Year is charged pro rata for each month or part month remaining in that year.
2.3 Community Traders pay 50% of the fee otherwise due.

3. CONDITIONS
3.1 Trading hours are 07:00 to 19:00. Gazebos must not exceed 3 m by 3 m.
3.2 Traders must hold public liability insurance of at least £5 million.
3.3 No amplified music.

4. HYGIENE
4.1 Food traders must hold a food hygiene rating of 3 or higher.

5. RENEWAL
5.1 Consents expire on 31 March and must be renewed each year.

6. REVOCATION
6.1 The Council may revoke a consent for breach of conditions after one written warning.

7. PITCH ALLOCATION
7.1 Vacant Pitches are offered in order of application date. A trader may hold no more than two Pitches.

8. WASTE
8.1 Traders must remove their own waste each day and must not use public litter bins.

9. APPEALS
9.1 A refusal or revocation may be appealed to the Licensing Committee within 21 days.

REVIEW OF THIS DOCUMENT
This document is reviewed at least every two years by its owner. Suggestions for improvement can be sent to the policy team at any time; they do not change the document until formally adopted.

FEES SCHEDULE 2025/26 — effective 1 April 2025, replacing section 2
2.1 The fee for a Pitch consent is £1,320 for a full Licensing Year.
2.2 A consent granted part-way through a Licensing Year is charged pro rata for each Quarter or part Quarter remaining in that year, including the Quarter in which it starts.
2.3 Community Traders pay 50% of the fee otherwise due.

APPLICATION ST-2025-061
Trader: Oyelaran Coffee Carts (sole trader). Trader status: standard (not a Community Trader).
Pitch: 4, Brewer's Row.
Consent granted from: 10 August 2025 to 31 March 2026.
Insurance and hygiene rating (5) checked.
Licensing assistant's draft invoice: "8 months × £100 = £800."
""",
[("fee_990", "Under the 2025/26 schedule three Quarters or part Quarters remain from August, so 3/4 of £1,320 = £990."),
 ("fee_800", "Eight months or part months remain, so 8/12 of £1,200 = £800."),
 ("fee_900", "The pro-rata rule now counts Quarters, and three remain from August, but the 2024/25 fee of £1,200 still applies, so 3/4 × £1,200 = £900."),
 ("fee_880", "The new £1,320 fee applies, but the pro-rata rule still counts months, and eight months or part months remain from August, so 8/12 of £1,320 = £880."),
 ("fee_495", "The trader pays half of the pro-rata fee: 50% of 3/4 of £1,320 = £495.")],
"fee_990", 2,
twin=T([("Trader status: standard (not a Community Trader).", "Trader status: registered Community Trader (non-profit, raising funds for a youth charity).")], "fee_495")),

# ------------------------------------------------------------------ cv03
# why: Regulations update (from 1 May 2025) raises the notice threshold to 100 mm stem diameter
# measured at 1.5 m. Birch is 90 mm at 1.5 m (130 mm at ground irrelevant); no TPO -> fell
# without notice. Twin: 110 mm -> six weeks' notice needed.
C("cv03", "What must the owner do before felling the birch tree?",
"""
WESTBRIDGE DISTRICT COUNCIL — TREES IN CONSERVATION AREAS: GUIDANCE NOTE TW-4

1. DEFINITIONS
1.1 "Conservation Area Tree" means any tree in a designated conservation area that is not protected by a Tree Preservation Order.
1.2 "Stem Diameter" means the diameter of the trunk measured at 1.5 m above ground level. For multi-stemmed trees, the largest stem is measured.
1.3 "Section 211 Notice" means written notice to the Council of intended works to a Conservation Area Tree.
1.4 "TPO Tree" means a tree protected by a Tree Preservation Order.

2. WHEN NOTICE IS NEEDED
2.1 Anyone intending to cut down or prune a Conservation Area Tree with a Stem Diameter of 75 mm or more must give a Section 211 Notice at least six weeks before starting.
2.2 Works to trees below that size need no notice.
2.3 During the six weeks the Council may make a Tree Preservation Order.

3. TPO TREES
3.1 Works to a TPO Tree need the Council's written consent, whatever its size.

4. DEAD AND DANGEROUS TREES
4.1 Dead trees and trees that are an immediate danger may be removed with five days' notice, with photographic evidence.

5. REPLANTING
5.1 The Council may ask for a replacement tree where a Conservation Area Tree is felled.

6. PENALTIES
6.1 Works carried out without required notice or consent may lead to prosecution and an unlimited fine.

7. HOW TO GIVE NOTICE
7.1 Section 211 Notices are made online with a sketch plan and a description of the works.
7.2 The Council acknowledges notices within five working days. Silence after six weeks means the works may go ahead.

REVIEW OF THIS DOCUMENT
This document is reviewed at least every two years by its owner. Suggestions for improvement can be sent to the policy team at any time; they do not change the document until formally adopted.

REGULATIONS UPDATE — effective 1 May 2025
"In paragraph 2.1, '75 mm' is replaced by '100 mm'. Paragraph 1.2 is unchanged."

ENQUIRY TW-2025-318 — received 9 June 2025
Property: 6 Chantry Close, Kilnhurst Conservation Area.
Tree: silver birch in the rear garden, planted about eight years ago.
Measurements provided by the owner's gardener: 130 mm at ground level; 90 mm at 1.5 m above ground. Single stem.
TPO search: no Tree Preservation Order on the property.
Reason for works: shading a vegetable bed. Tree is healthy.
Neighbour's email to the Council: "You can't fell anything in a conservation area without permission."
""",
[("fell_without_notice", "Measured at 1.5 m the stem is 90 mm, below the 100 mm threshold now in force, and there is no TPO, so no notice is needed."),
 ("give_six_weeks_notice", "The stem is at or above the size threshold that applies, so a Section 211 Notice is required six weeks before felling."),
 ("apply_for_tpo_consent", "In a conservation area every tree is treated like a TPO Tree, so the owner needs the Council's written consent before any felling, whatever the stem size."),
 ("give_five_days_notice", "A tree causing shading may be removed on five days' notice with photographs.")],
"fell_without_notice", 1,
twin=T([("90 mm at 1.5 m above ground", "110 mm at 1.5 m above ground")], "give_six_weeks_notice")),

# ------------------------------------------------------------------ cv04
# why: Events policy revision (events from 1 Jan 2025): 1,000+ need 12 weeks; 200-999 need 8
# weeks. Expected 650, applied 9 weeks before -> in time -> accept for processing.
# Twin: expected 1,200 -> 12 weeks needed -> late.
C("cv04", "How should the events team treat the application for the Mill Street Summer Fair?",
"""
KESTON TOWN COUNCIL — OUTDOOR EVENTS POLICY

1. DEFINITIONS
1.1 "Event" means an organised public gathering on Council land or a public highway.
1.2 "Expected Attendance" means the peak number of people expected on site at any one time, as stated in the event management plan.
1.3 "Event Date" means the first day of the Event.
1.4 "SAG" means the Safety Advisory Group of the Council and emergency services.

2. NOTICE PERIODS
2.1 Events with Expected Attendance of 500 or more: application at least 12 weeks before the Event Date.
2.2 Events with Expected Attendance of 100 to 499: at least 6 weeks.
2.3 Events under 100: no application needed, but the organiser must notify the Council 14 days ahead.
2.4 Applications received late are rejected and may not be processed.

3. SAG REFERRAL
3.1 Events with Expected Attendance above 5,000 are referred to the SAG.

4. INSURANCE
4.1 Organisers must hold public liability cover of at least £5 million.

5. FEES
5.1 Non-commercial events are free. Commercial events pay £250.

6. NOISE
6.1 Amplified sound must end by 22:00.

7. LITTER
7.1 Organisers must return the site clean within 24 hours.

8. ROAD CLOSURES
8.1 Events on a public highway that need a temporary closure are handled by the highways team once the event application is accepted.

9. FOOD TRADERS
9.1 Food traders at Events must be registered with a local authority and display their hygiene rating.

EQUALITY
The organisation applies this document fairly and consistently, without discrimination on the basis of any protected characteristic, and monitors its use to identify any unintended effects.

POLICY REVISION — approved 25 November 2024; applies to Events with an Event Date on or after 1 January 2025
R1. Paragraphs 2.1 and 2.2 are replaced: "2.1 Events with Expected Attendance of 1,000 or more: at least 12 weeks. 2.2 Events with Expected Attendance of 200 to 999: at least 8 weeks."
R2. Events of 100 to 199 now need 4 weeks. Paragraphs 2.3 and 2.4 are unchanged.

APPLICATION EV-2025-044
Event: Mill Street Summer Fair (non-commercial, run by the Mill Street Traders' Association).
Event Date: Saturday 26 July 2025.
Application received: Saturday 24 May 2025 (9 weeks before).
Expected Attendance: 650 at peak.
Insurance: £5 million public liability, certificate attached.
Events officer's first note: "Anything over 500 needs 12 weeks — looks late?"
""",
[("accept_for_processing", "Under the revision an Event of 650 needs 8 weeks' notice, and 9 weeks was given, so the application can be processed."),
 ("reject_late_application", "The application arrived later than the notice period that applies to an Event of this size, so paragraph 2.4 requires rejection."),
 ("refer_to_sag", "Events of this size must be referred to the Safety Advisory Group before any decision."),
 ("notification_only", "The Event is small enough that only 14 days' notification is needed, so no application is required.")],
"accept_for_processing", 1,
twin=T([("Expected Attendance: 650 at peak.", "Expected Attendance: 1,200 at peak.")], "reject_late_application")),

# ------------------------------------------------------------------ cv05
# why: fares update (from Mon 1 Sep 2025): single £2.20, daily cap £6.50, weekly cap £30.
# Week 8-14 Sep: Mon 4 trips 8.80 -> 6.50; Tue 2 -> 4.40; Wed 5 -> 6.50; Thu 3 = 6.60 -> 6.50;
# Fri 2 -> 4.40; Sat 0; Sun 1 -> 2.20. Sum 30.50 -> weekly cap £30.00.
# Twin: week 25-31 Aug (old fares £2.10 / £6 / £28): 6 + 4.2 + 6 + 6 + 4.2 + 2.1 = 28.5 -> £28.
C("cv05", "What should the rider be charged in total for the week shown?",
"""
TRANSLINK VALEWAY — PAY-AS-YOU-GO FARES AND CAPPING RULES

1. DEFINITIONS
1.1 "Trip" means one bus boarding using a contactless card or TransLink smartcard.
1.2 "Day" means the travel day from 04:30 to 04:29 the next morning.
1.3 "Week" means Monday to Sunday.
1.4 "Cap" means the most a rider pays for all Trips in a Day or a Week using the same card.

2. FARES (all-zone network)
2.1 Each Trip costs £2.10.
2.2 Transfers within 60 minutes of a paid Trip are free and are not Trips.

3. CAPPING
3.1 Daily Cap: £6.00.
3.2 Weekly Cap: £28.00, calculated after Daily Caps have been applied.
3.3 Caps apply automatically when the same card is used for every Trip.

4. CONCESSIONS
4.1 Riders under 19 pay half fares and half Caps with a registered youth smartcard.

5. REFUNDS
5.1 Overcharges are refunded to the card within five working days of a claim.

6. LOST CARDS
6.1 Registered smartcards can be replaced for £5 with the balance transferred.

7. CONTACTLESS AND SMARTCARDS
7.1 Caps work across contactless cards and smartcards only if the same card is used. Mobile wallets count as a separate card from the physical card.

8. PENALTY FARES
8.1 A rider without a valid tap is liable to a £50 penalty fare, reduced to £25 if paid within 21 days.

9. CHANGES
9.1 Fare changes apply to whole Weeks, starting on the Monday named in the update.

10. CONTACT
10.1 Fare questions can be raised through the TransLink app or at any travel centre.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

FARES UPDATE — effective for Weeks beginning on or after Monday 1 September 2025
F1. The Trip fare becomes £2.20.
F2. The Daily Cap becomes £6.50 and the Weekly Cap £30.00.
F3. Capping rules in 3.2 and 3.3 are unchanged.

JOURNEY HISTORY — contactless card ending 4471 (adult, same card throughout, no transfers)
Week: 8–14 September 2025.
• Monday: 4 Trips.
• Tuesday: 2 Trips.
• Wednesday: 5 Trips.
• Thursday: 3 Trips.
• Friday: 2 Trips.
• Saturday: no travel.
• Sunday: 1 Trip.
Rider's complaint: "17 trips — I've been charged over £30. Isn't there a cap?"
""",
[("charge_30_00", "New fares apply; after Daily Caps the Week totals £30.50, so the £30.00 Weekly Cap applies."),
 ("charge_28_00", "After Daily Caps the Week totals £28.50, so the £28.00 Weekly Cap applies."),
 ("charge_30_50", "Daily Caps reduce Monday, Wednesday and Thursday, bringing the Week to £30.50, and the Weekly Cap applies only before Daily Caps, so it does not reduce this further."),
 ("charge_37_40", "Seventeen Trips at £2.20 each come to £37.40.")],
"charge_30_00", 3,
twin=T([("Week: 8–14 September 2025.", "Week: 25–31 August 2025.")], "charge_28_00")),

# ------------------------------------------------------------------ cv06
# why: 2025 round raises the income limit to £150,000 (income £132,000 -> eligible). Grant up
# to 75% of project cost, max £5,000: 75% x 6,000 = 4,500. Match 25% = 1,500 = cash 600 +
# 60 volunteer hours x £15 = 900 -> met. -> award 4,500.
C("cv06", "What should the grants panel award to Fernbank Community Garden?",
"""
ASHWORTH COUNTY COUNCIL — COMMUNITY PROJECTS FUND: GUIDANCE FOR APPLICANTS

1. DEFINITIONS
1.1 "Eligible Organisation" means a constituted non-profit group based in the county with an annual income below £100,000 in its last accounts.
1.2 "Project Cost" means the total eligible cost of the project, excluding VAT that can be recovered.
1.3 "Match Funding" means cash, or volunteer time valued at £15 per hour, contributed to the project by the applicant or others.
1.4 "Round" means an application window announced by the Council.

2. WHAT WE FUND
2.1 Projects that improve shared community spaces, reduce isolation, or support volunteering.
2.2 We do not fund routine running costs or projects already completed.

3. HOW MUCH
3.1 Grants cover up to 75% of the Project Cost, to a maximum of £5,000.
3.2 Applicants must show Match Funding of at least 25% of the Project Cost.

4. MONITORING
4.1 Grantees report on outcomes within 12 months.

5. PAYMENT
5.1 Grants are paid in one instalment after the grant agreement is signed.

6. PUBLICITY
6.1 Grantees must acknowledge the Council's support on signs and websites.

PUBLICATION AND EARLIER VERSIONS
A copy of this document is published on the organisation's website. Earlier versions are archived and remain available for reference, together with every amendment and the date from which it applies.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

7. DECISIONS
7.1 The grants panel decides applications against the guidance for the Round in which they are submitted.

8. PREVIOUS GRANTS
8.1 Organisations that received a grant in the previous Round may apply again only if their monitoring report has been accepted.

9. VOLUNTEER TIME
9.1 Volunteer hours offered as Match Funding must be recorded on a timesheet during the project.

2025 ROUND NOTICE — opens 1 May 2025
N1. For this Round, the income limit in the definition of Eligible Organisation is £150,000.
N2. All other guidance is unchanged.

APPLICATION CPF-2025-117 (2025 Round, received 30 May 2025)
Applicant: Fernbank Community Garden (constituted association). Income in last accounts: £132,000.
Project: accessible raised beds and a covered seating area. Project Cost: £6,000.
Match Funding offered: cash £600 from a local business; 60 hours of volunteer labour.
Grant requested: £5,000.
Panel officer's note: "They're over the usual £100k limit, and the volunteer hours don't count as real money, do they?"
""",
[("award_4500", "The 2025 Round allows income up to £150,000, and 75% of the £6,000 Project Cost is £4,500, with £1,500 Match Funding including volunteer time."),
 ("award_5000", "The group is an Eligible Organisation for the 2025 Round and £5,000 is within the grant maximum, so the panel can award the full amount it requested."),
 ("refuse_income_too_high", "Income of £132,000 is above the £100,000 limit for an Eligible Organisation."),
 ("refuse_insufficient_match", "Volunteer hours are not money, so only the £600 cash counts as Match Funding, which is well below the 25% of the Project Cost that clause 3.2 requires.")],
"award_4500", 2),

# ------------------------------------------------------------------ cv07
# why: from 1 Jul 2025: up to 5 items £35, extra items £7; fridge-freezers count as 2 items;
# 50% concession for Council Tax Support. Items: sofa 1, mattress 1, wardrobe 1, fridge-
# freezer 2, 2 chairs 2 = 7 -> 35 + 2 x 7 = 49 -> half = £24.50. Call-centre script about
# online bookings is not policy.
C("cv07", "What fee should be charged for the bulky waste booking?",
"""
DENHOLM BOROUGH COUNCIL — BULKY WASTE COLLECTION SERVICE: TERMS

1. DEFINITIONS
1.1 "Item" means one piece of household furniture or one appliance. A fridge, freezer or fridge-freezer counts as 2 Items.
1.2 "Concession" means a 50% reduction for households receiving Council Tax Support.
1.3 "Booking" means a request for collection made online or by phone.

2. CHARGES
2.1 Up to 3 Items: £30.
2.2 Each additional Item: £8.
2.3 The Concession applies to the whole charge.

3. WHAT WE COLLECT
3.1 Furniture, white goods, mattresses, carpets (rolled, up to 2 m).
3.2 We do not collect building waste, garden waste, tyres or asbestos.

4. PRESENTATION
4.1 Items must be left outside the property by 07:00 on the collection day.

5. CANCELLATIONS
5.1 Cancellations made at least 2 working days before collection are refunded in full.

6. MISSED COLLECTIONS
6.1 If we miss a collection we return within 5 working days at no extra cost.

7. LIMITS
7.1 A household may book up to 12 Items in one collection and up to four collections a year.

8. ELIGIBILITY FOR THE CONCESSION
8.1 The Concession is checked against Council Tax Support records at the time of Booking, whether the Booking is made online or by phone.
8.2 No other discounts are available.

9. RE-USE
9.1 Items in good condition may be passed to the Council's furniture re-use partner.

10. COMPLAINTS
10.1 Complaints are answered within 10 working days.
10.2 Staff scripts and guidance do not change these Terms.

PUBLICATION AND EARLIER VERSIONS
A copy of this document is published on the organisation's website. Earlier versions are archived and remain available for reference, together with every amendment and the date from which it applies.

REVIEW OF THIS DOCUMENT
This document is reviewed at least every two years by its owner. Suggestions for improvement can be sent to the policy team at any time; they do not change the document until formally adopted.

CHARGES REVIEW — effective for Bookings made on or after 1 July 2025
R1. Paragraphs 2.1 and 2.2 are replaced: "Up to 5 Items: £35. Each additional Item: £7."
R2. Definitions 1.1 and 1.2 and paragraph 2.3 are unchanged.

BOOKING BW-77310 — made online on 20 July 2025
Household: 9 Grayling Walk. Council Tax Support: yes (verified).
Items listed: sofa; double mattress; wardrobe; fridge-freezer; two dining chairs.

CALL CENTRE SCRIPT (version 3), shown on the agent's screen
"Concessions are only available on phone bookings. Online bookings pay the full charge."
""",
[("fee_24_50", "Seven Items at the July rates cost £35 plus 2 × £7 = £49, and the Concession halves it to £24.50."),
 ("fee_49_00", "Seven Items at the July rates cost £35 plus 2 × £7 = £49, and the Concession is not available on an online Booking, so the full £49 is charged."),
 ("fee_31_00", "Seven Items at £30 plus 4 × £8 make £62, halved by the Concession to £31."),
 ("fee_21_00", "Six Items cost £35 plus £7 = £42, halved by the Concession to £21.")],
"fee_24_50", 2),

# ------------------------------------------------------------------ cv08
# why: 2025/26 policy adds a low-income extension: children aged 8-11 eligible for free
# school meals qualify if they attend one of the three nearest suitable schools lying between
# 2 and 6 miles. Age 9, FSM, attends second-nearest at 4.1 miles -> entitled.
# Twin: no FSM -> standard rule: nearest suitable school 2.6 miles < 3 miles -> not entitled.
C("cv08", "Is the pupil entitled to free home-to-school transport for 2025/26?",
"""
LOWESBY COUNTY COUNCIL — HOME TO SCHOOL TRAVEL POLICY

1. DEFINITIONS
1.1 "Walking Distance" means 2 miles for a child under 8 and 3 miles for a child aged 8 or over, measured by the shortest walking route.
1.2 "Nearest Suitable School" means the nearest school with a place available that provides education suitable to the child's age and ability.
1.3 "Low-income Family" means a family whose child is eligible for free school meals, or whose parent receives the maximum amount of working tax credit.
1.4 "Academic Year" means September to July.

2. ENTITLEMENT
2.1 A child is entitled to free transport if they attend their Nearest Suitable School and it is beyond Walking Distance.
2.2 Children who attend a school other than their Nearest Suitable School by parental preference are not entitled, unless another rule in this policy applies.

3. SPECIAL EDUCATIONAL NEEDS
3.1 Children with an education, health and care plan are assessed individually.

4. SPARE SEATS
4.1 Children who are not entitled may apply for a spare seat at £450 a year, if one is available.

5. APPLICATIONS
5.1 Applications for September must be made by 31 May.

6. REVIEWS
6.1 Parents may ask for a review within 20 working days of a decision.

7. BEHAVIOUR ON TRANSPORT
7.1 Transport may be withdrawn for serious misbehaviour after a warning to parents.

8. POST-16 TRANSPORT
8.1 Students aged 16 to 18 may buy a discounted travel pass; there is no free entitlement.

PUBLICATION AND EARLIER VERSIONS
A copy of this document is published on the organisation's website. Earlier versions are archived and remain available for reference, together with every amendment and the date from which it applies.

POLICY FOR 2025/26 ACADEMIC YEAR — additional rule 2.3
2.3 A child aged 8 to 11 from a Low-income Family is entitled to free transport to any of their three nearest suitable schools that lies more than 2 miles but not more than 6 miles from home.

APPLICATION HT-2025-4492 — received 12 May 2025, for September 2025
Pupil: Rhys Adebayo, aged 9 on 1 September 2025.
Family status: Rhys receives free school meals.
Nearest suitable school: St Anselm's Primary, 2.6 miles by walking route.
School attended: Brookfield Primary, the second-nearest suitable school, 4.1 miles by walking route.
Transport officer's draft: "Nearest school is inside 3 miles — not entitled; offer spare seat."
""",
[("entitled_low_income_rule", "Rhys is 9, from a Low-income Family, and attends one of his three nearest suitable schools between 2 and 6 miles away, so rule 2.3 entitles him."),
 ("not_entitled", "The low-income rule does not apply, and his Nearest Suitable School is within Walking Distance, so there is no entitlement."),
 ("entitled_under_8_rule", "Primary pupils are measured against the 2-mile Walking Distance, and his Nearest Suitable School is 2.6 miles away, beyond it, so he is entitled under rule 2.1."),
 ("entitled_nearest_school_only", "Rule 2.3 entitles him to free transport only to St Anselm's, not to Brookfield.")],
"entitled_low_income_rule", 2,
twin=T([("Family status: Rhys receives free school meals.", "Family status: Rhys is not eligible for free school meals, and neither parent receives working tax credit.")], "not_entitled")),

# ------------------------------------------------------------------ cv09
# why: from 1 Jun 2025 Saturday hours are 09:00-13:00; breaker at 08:30 on Sat 14 Jun is a
# breach; previous warning 3 Feb 2025 is within 6 months -> fixed penalty £400.
# Twin: 09:30 -> inside permitted hours -> no breach.
C("cv09", "What enforcement step should the environmental health officer take?",
"""
BRINDLEFORD CITY COUNCIL — CONSTRUCTION SITE NOISE: CODE OF PRACTICE AND ENFORCEMENT POLICY

1. DEFINITIONS
1.1 "Permitted Hours" means the hours in which noisy work may be carried out.
1.2 "Noisy Work" means work audible at the boundary of any occupied property, including breakers, piling and angle grinders.
1.3 "Warning" means a written warning issued by an environmental health officer and recorded on the site file.
1.4 "Fixed Penalty" means a fixed penalty notice of £400.

2. PERMITTED HOURS
2.1 Monday to Friday: 08:00 to 18:00.
2.2 Saturday: 08:00 to 13:00.
2.3 Sundays and bank holidays: no Noisy Work.

3. ENFORCEMENT
3.1 A first breach of Permitted Hours results in a Warning.
3.2 A further breach within 6 months of a Warning results in a Fixed Penalty.
3.3 Persistent breaches may lead to a notice under section 60 of the Control of Pollution Act, specifying conditions for the site.

4. DUST
4.1 Sites must damp down dusty operations and sheet lorries.

5. DELIVERIES
5.1 Deliveries by vehicles over 7.5 tonnes are not permitted before 07:30.

6. EXEMPTIONS
6.1 Emergency work to make a structure safe may be carried out at any time; the contractor must notify the Council within 24 hours.

7. COMMUNITY LIAISON
7.1 Sites expected to last more than three months must write to neighbours with a contact number before work begins.

8. MONITORING
8.1 Officers may install noise monitors at site boundaries. Readings are shared with the contractor.

EQUALITY
The organisation applies this document fairly and consistently, without discrimination on the basis of any protected characteristic, and monitors its use to identify any unintended effects.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

CODE UPDATE — effective 1 June 2025
U1. Paragraph 2.2 is replaced: "Saturday: 09:00 to 13:00."
U2. Paragraphs 2.1, 2.3 and section 3 are unchanged.

SITE FILE — 40 Marlowe Street (contractor: Tanfield Build Ltd)
• 3 February 2025: Warning issued for grinding at 18:40 on a weekday.
• Complaint received: hydraulic breaker in use at 08:30 on Saturday 14 June 2025, breaking out the old patio.
• Officer's visit on the day confirmed the breaker was running and audible at the neighbouring houses.
• No emergency was claimed.
• Site manager's statement: "We've always been allowed to start at eight on Saturdays."
""",
[("issue_fixed_penalty", "Saturday work now starts at 09:00, so the 08:30 breaker was a breach, and it came within 6 months of the February Warning: a Fixed Penalty follows."),
 ("issue_warning", "Each breach of the Code is dealt with on its own, and this is the site's first breach of Saturday hours, so a Warning is the correct first step."),
 ("no_breach", "The works took place within the Permitted Hours for a Saturday, so there was no breach."),
 ("serve_section_60_notice", "With a weekday breach in February and a Saturday breach in June, the contractor's breaches are persistent, so a section 60 notice must be served on the site.")],
"issue_fixed_penalty", 2,
twin=T([("hydraulic breaker in use at 08:30 on Saturday 14 June 2025", "hydraulic breaker in use at 09:30 on Saturday 14 June 2025")], "no_breach")),

# ------------------------------------------------------------------ cv10
# why: withdrawn after the plan check but before any inspection -> inspection charge refunded
# less the admin fee; admin fee £75 for withdrawals from 1 Apr 2025 -> 900 - 75 = 825.
C("cv10", "What refund is due on the withdrawn building control application?",
"""
GARSTON DISTRICT COUNCIL — BUILDING CONTROL CHARGES SCHEME

1. DEFINITIONS
1.1 "Plan Charge" means the charge for checking plans submitted with a full plans application.
1.2 "Inspection Charge" means the charge for site inspections during the work, paid in advance with the application.
1.3 "Plan Check" means the Council's examination of the plans; it is complete when a decision notice or a request for amended plans is sent.
1.4 "Administration Fee" means the Council's fee for processing a withdrawal.

2. CHARGES
2.1 Charges are set out in Table A and depend on the type and size of the work.
2.2 VAT is included in all charges.

3. WITHDRAWALS AND REFUNDS
3.1 If an application is withdrawn before the Plan Check has started, both charges are refunded in full.
3.2 If an application is withdrawn after the Plan Check is complete but before the first inspection, the Inspection Charge is refunded less an Administration Fee of £50. The Plan Charge is not refunded.
3.3 After the first inspection, refunds are at the Council's discretion.

4. REGULARISATION
4.1 Applications for work already carried out are charged at 150% of the standard charge.

5. PAYMENT
5.1 Charges are payable on submission. Applications are not validated until payment clears.

6. DISPUTES
6.1 Disputes about charges are referred to the Head of Building Control.

7. LAPSED APPLICATIONS
7.1 Applications on which no work has started within three years lapse; charges are not refunded.

8. PAYMENT METHODS
8.1 Refunds are made to the card or account used for payment within 20 working days.

9. PARTIAL WITHDRAWAL
9.1 Where only part of the proposed work is withdrawn, charges are recalculated on the remaining work.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

SCHEME REVISION — effective for withdrawals on or after 1 April 2025
"In paragraph 3.2, '£50' is replaced by '£75'. Paragraphs 3.1 and 3.3 are unchanged."

APPLICATION BC/25/0412 — rear extension, 18 Hollin Lane
Charges paid on 12 March 2025: Plan Charge £600; Inspection Charge £900.
Plan Check completed: 2 April 2025 (decision notice approving plans with conditions sent).
Withdrawal received: 29 April 2025. No inspection has taken place.
Applicant's email: "We've decided not to build. Please refund everything we paid."
""",
[("refund_825", "The withdrawal came after the Plan Check but before any inspection, so the £900 Inspection Charge is refunded less the £75 Administration Fee now in force."),
 ("refund_850", "The Inspection Charge of £900 is refunded less the £50 Administration Fee."),
 ("refund_1425", "The application was withdrawn before any inspection took place, so both the Plan Charge and the Inspection Charge, £1,500 in total, are refunded less the £75 Administration Fee."),
 ("refund_nothing", "Once the Plan Check is complete no refund of any charge is due.")],
"refund_825", 1),

# ------------------------------------------------------------------ cv11
# why: from 1 Jan 2025 no overdue fines for under-18s; lost-item charges still apply to all
# borrowers, but the £2 admin fee is waived for under-18s -> £12.99 only.
C("cv11", "What should the library charge the young borrower?",
"""
RAVENSMOOR LIBRARIES — BORROWING RULES AND CHARGES

1. DEFINITIONS
1.1 "Adult Borrower" means a member aged 18 or over.
1.2 "Young Borrower" means a member under 18.
1.3 "Overdue Charge" means a charge for each day an item is kept past its due date.
1.4 "Replacement Charge" means the published replacement cost of a lost or damaged item.
1.5 "Admin Fee" means a fixed £2 fee added to each Replacement Charge.

2. LOANS
2.1 Adults may borrow up to 20 items; Young Borrowers up to 10.
2.2 Loans last 3 weeks and may be renewed twice unless reserved.

3. OVERDUE CHARGES
3.1 Adult Borrowers pay 25p a day per item, up to £5 per item.
3.2 Young Borrowers pay 10p a day per item, up to £2 per item.

4. LOST AND DAMAGED ITEMS
4.1 Borrowers who lose or damage an item pay the Replacement Charge plus the Admin Fee.
4.2 If a lost item is found and returned within 3 months, the Replacement Charge is refunded but the Admin Fee is kept.

5. BLOCKS
5.1 Accounts owing more than £10 are blocked from borrowing until paid.

6. PRINTING
6.1 Printing costs 15p a page for black and white and 50p for colour.

7. RESERVATIONS
7.1 Reservations cost 50p for Adult Borrowers and are free for Young Borrowers.

8. WAIVERS
8.1 Library managers may waive Overdue Charges in cases of hardship. They may not waive Replacement Charges.

9. CHANGES
9.1 Charges are reviewed each year and changes take effect on the date the Cabinet decides.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

CABINET DECISION — effective 1 January 2025
D1. Paragraph 3.2 is deleted: Young Borrowers pay no Overdue Charges.
D2. For Young Borrowers, the Admin Fee in paragraph 4.1 is waived. The Replacement Charge still applies.
D3. Adult charges are unchanged.

ACCOUNT — Young Borrower Kai Mensah, aged 15
• 12 September 2025: returned "Tides of Orrin" 20 days late.
• Same day: reported "The Glass Observatory" as lost. Published Replacement Charge: £12.99.
• No other items on loan.
Library assistant's question: "Do we just clear everything for under-18s now?"
""",
[("charge_12_99", "Under-18s no longer pay Overdue Charges or the Admin Fee, but the Replacement Charge for the lost book still applies."),
 ("charge_14_99", "The lost book costs its £12.99 Replacement Charge plus the £2 Admin Fee."),
 ("charge_16_99", "Twenty days at 10p is £2, and the lost book costs £12.99 plus the £2 Admin Fee."),
 ("charge_nothing", "The Cabinet decision removed all charges for Young Borrowers.")],
"charge_12_99", 1),

# ------------------------------------------------------------------ cv12
# why: 2025/26 levy rules also disregard apprentices under 25; household of one working adult
# plus an apprentice aged 19 -> one counted adult -> 25% single-occupier discount on £1,840
# = £1,380. Twin: apprentice aged 27 -> not disregarded -> two adults -> full £1,840.
C("cv12", "What household levy bill should be issued for 2025/26?",
"""
CARNWORTH UNITARY COUNCIL — HOUSEHOLD LEVY: DISCOUNTS AND DISREGARDS

1. DEFINITIONS
1.1 "Levy Year" means 1 April to 31 March.
1.2 "Counted Adult" means a resident aged 18 or over who is not a Disregarded Person.
1.3 "Disregarded Person" means (a) a full-time student, (b) a resident care worker, or (c) a person with a severe mental impairment certified by a doctor.
1.4 "Band C Levy" means £1,840 for the 2025/26 Levy Year.

2. DISCOUNTS
2.1 Where a home has only one Counted Adult, the levy is reduced by 25%.
2.2 Where a home has no Counted Adults, the levy is reduced by 50%.
2.3 Discounts are applied from the date the circumstances begin.

3. EXEMPTIONS
3.1 Homes occupied only by full-time students are exempt.

4. REPORTING CHANGES
4.1 Residents must tell the Council of any change affecting a discount within 21 days.

5. PAYMENT
5.1 The levy is payable in ten monthly instalments from April.

6. APPEALS
6.1 Disputes about discounts may be appealed to the valuation tribunal.

7. EVIDENCE
7.1 Claims for a disregard must be supported by evidence, such as a student certificate, a care provider's letter or an apprenticeship agreement.

8. PENALTIES
8.1 Failing to report a change that ends a discount may lead to a £70 penalty.

9. BACKDATING
9.1 Discounts may be backdated up to six years where the circumstances are proved.

10. SECOND HOMES
10.1 Homes that are no one's main residence pay a premium of 100% of the levy.

ACCESSIBILITY
This document is available in large print, audio and easy-read formats on request. Anyone who needs help to understand it, or to take part in a process it describes, may ask for reasonable adjustments.

EQUALITY
The organisation applies this document fairly and consistently, without discrimination on the basis of any protected characteristic, and monitors its use to identify any unintended effects.

LEVY RESOLUTION 2025/26 — adopted 26 February 2025, applying from the 2025/26 Levy Year
R1. A new category is added to definition 1.3: "(d) an apprentice under 25 on an approved apprenticeship paying no more than £230 a week."
R2. The discounts in section 2 are unchanged.

ACCOUNT — 31 Alder Rise (Band C)
Residents for the whole of 2025/26:
• Grace Ottley, 46, employed full time.
• Her son Jamie Ottley, aged 19, on an approved plumbing apprenticeship paid £210 a week.
No other residents. No other disregards.
Previous years' bills: full Band C levy, no discount.
""",
[("bill_1380", "The 2025/26 resolution disregards Jamie as an apprentice under 25, leaving one Counted Adult, so the £1,840 levy is reduced by 25%."),
 ("bill_1840", "Two Counted Adults live in the home this year, so no discount applies."),
 ("bill_920", "Jamie is disregarded as an apprentice and Grace is disregarded as the bill payer, so no Counted Adults remain and the 50% discount applies to the £1,840 levy."),
 ("bill_1472", "One resident is disregarded, so the levy is reduced by 20%.")],
"bill_1380", 1,
twin=T([("Her son Jamie Ottley, aged 19,", "Her son Jamie Ottley, aged 27,")], "bill_1840")),

# ------------------------------------------------------------------ cv13
# why: Open Records Policy update (requests from 1 Jul 2025) lowers the cost limit to 15 hours;
# estimate 16 hours exceeds it -> Council may refuse on cost grounds but must offer advice to
# narrow. No fee may be charged for the search.
C("cv13", "How should the council respond to the records request?",
"""
HALDANE CITY COUNCIL — OPEN RECORDS POLICY

1. DEFINITIONS
1.1 "Request" means a written request for recorded information held by the Council.
1.2 "Working Day" means Monday to Friday excluding public holidays.
1.3 "Cost Limit" means 18 hours of staff time spent locating, retrieving and extracting the information, valued at £25 per hour.
1.4 "Advice and Assistance" means help to the requester to narrow the Request so it can be answered within the Cost Limit.

2. RESPONSE
2.1 The Council responds within 20 Working Days of receiving a Request.
2.2 Information already published is answered by providing a link.

3. COST
3.1 Requests that can be answered within the Cost Limit are answered free of charge.
3.2 Where the estimated time exceeds the Cost Limit, the Council may refuse the Request, but must give Advice and Assistance.
3.3 The Council does not charge for staff time on Requests; only photocopying and postage may be charged.

4. EXEMPTIONS
4.1 Personal data about third parties and commercially sensitive information may be withheld.

5. REVIEWS
5.1 Requesters may ask for an internal review within 40 Working Days of a response.

6. PUBLICATION
6.1 Responses of wide interest are published in the disclosure log.

7. VEXATIOUS REQUESTS
7.1 The Council may refuse Requests that are manifestly unreasonable, after consulting the Monitoring Officer.

8. AGGREGATION
8.1 Requests from the same person on the same subject within 60 Working Days may be added together for the Cost Limit.

EQUALITY
The organisation applies this document fairly and consistently, without discrimination on the basis of any protected characteristic, and monitors its use to identify any unintended effects.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

POLICY UPDATE — applies to Requests received on or after 1 July 2025
U1. In definition 1.3, "18 hours" is replaced by "15 hours".
U2. Section 3 is unchanged.

REQUEST OR-2025-0877 — received 14 August 2025 by email
Requester: a local residents' group.
Request: "All correspondence between the Council and any contractor about pothole repairs on Brook Lane since January 2020."
Records team estimate: 16 hours to search three mailboxes and the contracts system.
Records officer's draft: "We could just send them an invoice for the 16 hours at £25 — £400 — and get on with it."
""",
[("refuse_with_advice", "The 16-hour estimate exceeds the 15-hour Cost Limit now in force, so the Council may refuse but must help the group narrow the Request."),
 ("answer_free_of_charge", "The 16-hour estimate is inside the 18-hour Cost Limit in definition 1.3, so the Request must be answered free of charge within 20 Working Days."),
 ("charge_400_and_answer", "The Council may charge £25 an hour for the 16 hours and then answer the Request."),
 ("refuse_without_advice", "A Request over the Cost Limit may simply be refused, with no further help required.")],
"refuse_with_advice", 1),
]
