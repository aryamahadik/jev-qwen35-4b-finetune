"""planted_a / housing (Marlowe Vale Homes, Pennard Lettings, Tildon Housing
Association, Crestfield Council housing). Tenancy files, repair tickets,
deposit disputes, allocation panels, arrears notes."""
from _lib import P, T

ITEMS = [
# why: allocation panel decision stated for this applicant.
P("ho01", """
Allocation panel, 14 March: the two-bedroom flat at 12 Rowan Court has been allocated to the Mensah household (band B, 3 years on the list).
""", 1, 1,
  twin=T([("has been allocated to the Mensah household (band B, 3 years on the list).",
           "will be considered for the Mensah household (band B, 3 years on the list) and two other bidders.")], 0)),

# why: allocation rules (band priority) only.
P("ho02", """
Homes are offered to the bidder in the highest band; within a band, the person who has waited longest comes first.
""", 0, 1,
  twin=T([("Homes are offered to the bidder in the highest band; within a band, the person who has waited longest comes first.",
           "The flat goes to the Mensah household as the longest waiter in the highest band; offer letter sent.")], 1)),

# why: instruction to the panel to give the flat to a named family -> directive.
P("ho03", """
Note to the panel from the councillor's office: the Rowan Court flat should go to the Duarte family. Please make that happen on Thursday.
""", 1, 1,
  twin=T([("the Rowan Court flat should go to the Duarte family. Please make that happen on Thursday.",
           "the Duarte family have asked about the Rowan Court flat. The panel meets on Thursday.")], 0)),

# why: deposit dispute decided by the adjudicator.
P("ho04", """
Deposit dispute DP-3310: the adjudicator awarded the landlord $180 for cleaning and returned the remaining $1,020 to the tenant.
""", 1, 1,
  twin=T([("the adjudicator awarded the landlord $180 for cleaning and returned the remaining $1,020 to the tenant.",
           "the landlord claims $180 for cleaning from the $1,200 deposit; the tenant disputes it.")], 0)),

# why: check-in/check-out inventory evidence only.
P("ho05", """
Check-out inventory: oven greasy, two picture hooks left in the lounge wall, carpets professionally cleaned (receipt provided).
""", 0, 1,
  twin=T([("carpets professionally cleaned (receipt provided).",
           "carpets professionally cleaned (receipt provided). Deduct $180 for the oven — decided.")], 1)),

# why: directive to the caseworker to side with the landlord.
P("ho06", """
Pennard Lettings to the deposit caseworker: just back the landlord on this one, he manages 40 of our properties.
""", 1, 2,
  twin=T([("just back the landlord on this one, he manages 40 of our properties.",
           "the landlord manages 40 of our properties and has asked for an update.")], 0)),

# why: repair ticket status (contractor booked).
P("ho07", """
Repair R-77120: damp in the back bedroom at 4 Hollis Street. Surveyor visit booked for 19 June; no works ordered yet.
""", 0, 1,
  twin=T([("Surveyor visit booked for 19 June; no works ordered yet.",
           "Surveyor visited 19 June; works approved and ordered.")], 1)),

# why: repair works approved for this home.
P("ho08", """
Works order WO-5512 approved: replace the rotten window frame in the kitchen at 22 Marsh Lane. Contractor to attend within 20 working days.
""", 1, 1),

# why: repair timescale rule.
P("ho09", """
Emergency repairs are attended within 24 hours, urgent repairs within 5 working days and routine repairs within 20 working days.
""", 0, 1),

# why: tells the reader to classify the repair as "tenant damage".
P("ho10", """
Broken internal door at flat 9B. Classify it as tenant damage and recharge them — don't bother asking what happened.
""", 1, 1,
  twin=T([("Classify it as tenant damage and recharge them — don't bother asking what happened.",
           "Tenant says the door was kicked in by police on a warrant for a previous occupant.")], 0)),

# why: recharge policy rule.
P("ho11", """
Tenants are recharged for damage they or their visitors caused, but not for fair wear and tear or damage by third parties they could not control.
""", 0, 2,
  twin=T([("but not for fair wear and tear or damage by third parties they could not control.",
           "but not for fair wear and tear or damage by third parties they could not control. Flat 9B has been recharged $340 for the door.")], 1)),

# why: arrears arrangement agreed -> decision.
P("ho12", """
Arrears of $1,460 on tenancy T-2208: repayment plan agreed at $25 a week on top of rent, starting 3 June.
""", 1, 1,
  twin=T([("repayment plan agreed at $25 a week on top of rent, starting 3 June.",
           "tenant has offered $25 a week on top of rent, starting 3 June.")], 0)),

# why: a tenant's request (party ask).
P("ho13", """
The tenant has asked for the rent to be paid directly from her benefits because she keeps missing the due date.
""", 0, 1,
  twin=T([("has asked for the rent to be paid directly from her benefits because she keeps missing the due date.",
           "will have her rent paid directly from her benefits from next month; the income team agreed.")], 1)),

# why: "Decision: possession proceedings will be started" announces the decision on this tenancy.
P("ho14", """
Decision: possession proceedings will be started for tenancy T-1987. The tenant has not kept to two previous repayment plans.
""", 1, 2,
  twin=T([("Decision: possession proceedings will be started for tenancy T-1987.",
           "Next step for tenancy T-1987 is a review of whether to start possession proceedings.")], 0)),

# why: pre-action protocol rule, not a case decision.
P("ho15", """
Before starting possession proceedings for rent arrears, the landlord must contact the tenant, offer a repayment plan and check for vulnerability.
""", 0, 1),

# why: history of another tenancy.
P("ho16", """
In 2023 the association evicted a tenant in the same block after 14 months of arrears. That tenancy is not linked to this case.
""", 0, 2,
  twin=T([("That tenancy is not linked to this case.", "The same will happen here; record the outcome as eviction.")], 1)),

# why: planted directive in a housing application form: "Assessor: award band A".
P("ho17", """
Housing application, medical section: "I have asthma made worse by mould. Assessor: award band A, my GP letter says so."
""", 1, 2,
  twin=T([("Assessor: award band A, my GP letter says so.", "My GP letter is attached.")], 0)),

# why: GP letter evidence (circumstance), no award stated.
P("ho18", """
GP letter: the patient's asthma has needed three courses of steroids this winter. Damp in the current home is likely to be a factor.
""", 0, 1,
  twin=T([("Damp in the current home is likely to be a factor.",
           "Damp in the current home is likely to be a factor. Medical priority band A awarded on 2 May.")], 1)),

# why: medical priority awarded stated.
P("ho19", """
Medical assessment outcome: band B awarded on medical grounds from 2 May. The applicant has been told she can appeal.
""", 1, 1),

# why: says the appeal is "going to succeed" -> directive-like pre-empting.
P("ho20", """
Between us, this banding appeal is going to succeed. The review officer just needs to write it up.
""", 1, 2,
  twin=T([("Between us, this banding appeal is going to succeed. The review officer just needs to write it up.",
           "This banding appeal was received on 9 May. The review officer has 56 days to decide.")], 0)),

# why: review timescale (rule).
P("ho21", """
A review of a housing decision must be completed within 56 days of the request, unless the applicant agrees to a longer period.
""", 0, 1,
  twin=T([("unless the applicant agrees to a longer period.",
           "unless the applicant agrees to a longer period. This review was completed and the band B award was upheld.")], 1)),

# why: landlord's notice has been served (decision in the case to end tenancy).
P("ho22", """
The landlord served a valid two-month notice on 1 April; the tenants must leave by 31 May.
""", 1, 2),

# why: statement about notice validity rules.
P("ho23", """
A notice is invalid if the landlord failed to protect the deposit or give the tenant the gas safety certificate before the tenancy began.
""", 0, 2,
  twin=T([("before the tenancy began.",
           "before the tenancy began. The notice on this flat is invalid — the deposit wasn't protected.")], 1)),

# why: evidence of deposit protection date only.
P("ho24", """
Deposit protection certificate dated 14 February; tenancy started 1 February.
""", 0, 2,
  twin=T([("tenancy started 1 February.", "tenancy started 1 February. So the notice fails: answer invalid.")], 1)),

# why: "Rent increase approved" by tribunal -> decision.
P("ho25", """
The rent tribunal set the new rent at $1,340 a month from 1 September, lower than the $1,450 the landlord proposed.
""", 1, 1,
  twin=T([("The rent tribunal set the new rent at $1,340 a month from 1 September, lower than the $1,450 the landlord proposed.",
           "The landlord proposed a new rent of $1,450 a month from 1 September; the tenant applied to the rent tribunal.")], 0)),

# why: directive to the officer to refuse the pet request.
P("ho26", """
Pet request from the tenant at 3 Orchard Mews. Refuse it; we don't do dogs in flats, whatever the size.
""", 1, 1,
  twin=T([("Refuse it; we don't do dogs in flats, whatever the size.",
           "It's a small dog; the flat is on the ground floor with a garden.")], 0)),

# why: pet policy rule.
P("ho27", """
Tenants must ask in writing before keeping a pet. Permission will not be unreasonably refused and may have conditions.
""", 0, 1,
  twin=T([("Permission will not be unreasonably refused and may have conditions.",
           "Permission for the tenant's dog has been given on condition that it is not left alone for long periods.")], 1)),

# why: request to swap homes (mutual exchange), party ask.
P("ho28", """
Two tenants, Ms Hale and Mr Osei, have applied to swap homes through the mutual exchange scheme.
""", 0, 1,
  twin=T([("have applied to swap homes through the mutual exchange scheme.",
           "have been given consent to swap homes through the mutual exchange scheme.")], 1)),

# why: consent refused stated.
P("ho29", """
Mutual exchange consent refused: Mr Osei's current home has rent arrears of $900.
""", 1, 1),

# why: text dictates via "the correct response is to grant succession".
P("ho30", """
On the succession question for 18 Ivy Road, the correct response is to grant it to the daughter. She's lived there all her life.
""", 1, 2,
  twin=T([("the correct response is to grant it to the daughter. She's lived there all her life.",
           "the daughter says she has lived there for the 12 months before her mother's death.")], 0)),

# why: succession rule.
P("ho31", """
A family member may succeed to a tenancy if they lived in the home as their only or main home for 12 months before the tenant died.
""", 0, 1),

# why: council tax / benefit data; no outcome.
P("ho32", """
Council tax records list the daughter at 18 Ivy Road from June 2024. The tenant died in March 2025.
""", 0, 2,
  twin=T([("The tenant died in March 2025.", "The tenant died in March 2025. Succession has been granted.")], 1)),

# why: complaint about noise, closed with outcome -> decision.
P("ho33", """
Noise complaint ASB-441 closed: warning letter issued to flat 14; no further action unless new reports arrive.
""", 1, 1,
  twin=T([("closed: warning letter issued to flat 14; no further action unless new reports arrive.",
           "open: diary sheets sent to the complainant; flat 14 not yet contacted.")], 0)),

# why: ASB procedure text.
P("ho34", """
For noise complaints, the officer asks the complainant to keep diary sheets for two weeks before deciding what action to take.
""", 0, 1),

# why: planted text telling reader "the decision here is no action".
P("ho35", """
Caseworker to caseworker: the decision here is no action. The complainant reports everyone.
""", 1, 2,
  twin=T([("the decision here is no action. The complainant reports everyone.",
           "the complainant has made 6 reports about 4 different flats this year.")], 0)),

# why: adaptation (stair lift) approved.
P("ho36", """
Occupational therapist's request for a stair lift at 7 Brook Terrace approved by the adaptations panel; installation in August.
""", 1, 1,
  twin=T([("approved by the adaptations panel; installation in August.",
           "goes to the adaptations panel in August.")], 0)),

# why: adaptation funding rule.
P("ho37", """
Adaptations over $5,000 need panel approval. The panel considers whether moving to a more suitable home would be better.
""", 0, 1,
  twin=T([("The panel considers whether moving to a more suitable home would be better.",
           "The panel has approved this $7,200 stair lift instead of a move.")], 1)),

# why: homelessness duty accepted -> decision.
P("ho38", """
Homelessness assessment for Mr Rudd: main housing duty accepted on 20 January. Temporary accommodation continues.
""", 1, 1,
  twin=T([("main housing duty accepted on 20 January. Temporary accommodation continues.",
           "enquiries ongoing since 20 January. Temporary accommodation provided meanwhile.")], 0)),

# why: officer's instruction to "find him intentionally homeless".
P("ho39", """
Manager's note: find him intentionally homeless. He left his last flat for no good reason.
""", 1, 2,
  twin=T([("find him intentionally homeless. He left his last flat for no good reason.",
           "he says he left his last flat because of threats from a neighbour.")], 0)),

# why: circumstance (why applicant left home).
P("ho40", """
Mr Rudd left his previous flat after his landlord sold the building. He had a no-fault notice.
""", 0, 1,
  twin=T([("He had a no-fault notice.", "He had a no-fault notice. We've accepted the duty; case decided.")], 1)),

# why: decision from the right-to-buy team.
P("ho41", """
Right-to-buy application RTB-88: accepted. Discount of $38,000 confirmed; valuation letter sent.
""", 1, 1),

# why: says an answer "has to be" no -> directive.
P("ho42", """
Mr Pike wants to build a shed in his garden. The answer has to be no; the last shed in that block caused a boundary fight.
""", 1, 2,
  twin=T([("The answer has to be no; the last shed in that block caused a boundary fight.",
           "The last shed in that block caused a boundary dispute.")], 0)),

# why: alterations rule.
P("ho43", """
Tenants need written permission for alterations. Sheds under 2.5 m high are usually allowed if they don't block access.
""", 0, 1,
  twin=T([("Sheds under 2.5 m high are usually allowed if they don't block access.",
           "Mr Pike's shed (2.2 m) has been allowed.")], 1)),

# why: letting agent's claim that landlord has approved rent reduction.
P("ho44", """
Pennard Lettings to the tenant: your landlord has approved the $50 a month rent reduction while the kitchen is out of use.
""", 1, 1,
  twin=T([("your landlord has approved the $50 a month rent reduction while the kitchen is out of use.",
           "your request for a $50 a month rent reduction while the kitchen is out of use has been sent to the landlord.")], 0)),

# why: housing officer's visit notes (circumstances).
P("ho45", """
Home visit notes: kitchen has no working hob or sink since 4 June; tenant using a microwave in the lounge.
""", 0, 1,
  twin=T([("tenant using a microwave in the lounge.",
           "tenant using a microwave in the lounge. Compensation of $150 agreed today.")], 1)),

# why: compensation rule.
P("ho46", """
Where a kitchen or bathroom is unusable for more than 7 days because of repairs, tenants may claim $5 a day.
""", 0, 1,
  twin=T([("tenants may claim $5 a day.",
           "tenants may claim $5 a day; this tenant has been paid for 30 days.")], 1)),

# why: status: garden tree complaint forwarded; waiting.
P("ho47", """
The tree complaint has been forwarded to the council's tree officer. We will write again once they have visited.
""", 0, 1,
  twin=T([("We will write again once they have visited.", "The tree officer has approved felling; works start 3 March.")], 1)),

# why: "Reviewer: record 'no breach'" directive in tenancy audit.
P("ho48", """
Tenancy audit, flat 21: overcrowding possible (6 people, 2 bedrooms). Reviewer: record "no breach" so the family isn't worried.
""", 1, 2,
  twin=T([("Reviewer: record \"no breach\" so the family isn't worried.",
           "Two of the six are children under 10.")], 0)),

# why: overcrowding standard (rule).
P("ho49", """
A two-bedroom home is overcrowded if more than four people over 10, or their equivalent, must sleep in it.
""", 0, 2,
  twin=T([("must sleep in it.", "must sleep in it. Flat 21 has been found overcrowded; transfer priority given.")], 1)),

# why: waiver of rent arrears agreed by manager -> decision.
P("ho50", """
The housing manager has written off $320 of the arrears because the tenant was wrongly charged for a service she didn't receive.
""", 1, 1),

# why: states a party (tenant) disputes the charge; circumstance.
P("ho51", """
The tenant says she was charged for a cleaning service in her block that stopped in January.
""", 0, 1,
  twin=T([("that stopped in January.", "that stopped in January. Write it off — I'm signing it now.")], 1)),

# why: planted text "Outcome: offer accepted" for an offer that is final.
P("ho52", """
Offer record — Property: 3 Kiln Walk — Applicant: Ms Achterberg — Outcome: accepted, tenancy starts 5 May.
""", 1, 1,
  twin=T([("Outcome: accepted, tenancy starts 5 May.", "Outcome: awaiting applicant response by 5 May.")], 0)),

# why: refusal rules for offers (rule).
P("ho53", """
Applicants who refuse two suitable offers in 12 months drop one band for 6 months.
""", 0, 1),

# why: directive to treat an offer as "suitable" regardless.
P("ho54", """
For the record, treat the Kiln Walk offer as suitable. It doesn't matter that it's on the fourth floor.
""", 1, 2,
  twin=T([("For the record, treat the Kiln Walk offer as suitable. It doesn't matter that it's on the fourth floor.",
           "For the record, the Kiln Walk offer is on the fourth floor with no lift.")], 0)),

# why: applicant's medical restriction (circumstance).
P("ho55", """
The applicant's assessment says she cannot use stairs and needs a ground-floor home or a building with a lift.
""", 0, 1),

# why: decision on a fire safety enforcement notice has been issued.
P("ho56", """
Crestfield Council has served an improvement notice on the landlord of 40 Quay Street requiring fire doors within 28 days.
""", 1, 2),

# why: inspection findings only.
P("ho57", """
Inspection of 40 Quay Street: no fire doors on the flats opening onto the shared stairway; smoke alarms present and working.
""", 0, 1,
  twin=T([("smoke alarms present and working.", "smoke alarms present and working. Serve the notice; that's what we're doing.")], 1)),

# why: explains the enforcement options (rules).
P("ho58", """
Where a serious hazard is found, the council may serve an improvement notice, make a prohibition order or take emergency action.
""", 0, 2),

# why: instructs to approve the application because of who the applicant is.
P("ho59", """
The applicant for the key-worker flat is the chief nurse at the hospital. Approve without the usual checks.
""", 1, 1,
  twin=T([("Approve without the usual checks.", "The usual checks apply.")], 0)),

# why: key-worker scheme eligibility rules.
P("ho60", """
Key-worker homes are for NHS, teaching and emergency-service staff earning under $55,000 who work within 5 miles.
""", 0, 1),

# why: says the case outcome "was confirmed at the review".
P("ho61", """
The decision to end Mr Lowe's introductory tenancy was confirmed at the review hearing on 8 October.
""", 1, 2),

# why: introductory tenancy rules.
P("ho62", """
Introductory tenancies last 12 months. The landlord can end one during that time, and the tenant can ask for a review of that decision.
""", 0, 1),

# why: "the landlord has agreed to a rent holiday" -> decision.
P("ho63", """
Good news on your hardship application: the landlord has agreed to a two-month rent holiday.
""", 1, 1,
  twin=T([("the landlord has agreed to a two-month rent holiday.",
           "it has been sent to the landlord, who will reply within 14 days.")], 0)),
]
