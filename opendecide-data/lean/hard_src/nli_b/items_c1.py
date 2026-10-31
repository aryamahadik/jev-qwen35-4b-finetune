"""Part C1: modals (might, may, must, need not, can, cannot; rules vs facts; deontic status)."""
from _h import it, L3, L3CARD, FOLLOW, CONSIST, RULED, E, C, U, NONE

DEON = ["required", "permitted but not required", "forbidden", "the passage does not settle this"]
DEONCARD = ("- required: the rules say it must be done\n"
            "- permitted but not required: the rules allow it and also allow not doing it\n"
            "- forbidden: the rules say it must not be done\n"
            "- the passage does not settle this: the rules quoted do not fix whether it is required, permitted or forbidden")

ITEMS = [

it("C1", "noul",
   "Does the chart note guarantee the statement?",
   """OUTPATIENT DERMATOLOGY - Clinic note
Patient: 34-year-old female, referred by GP (Dr. H. Lindahl) with a widespread itchy rash of 5 days' duration.

History: Started amoxicillin 500 mg three times daily 8 days ago for a dental abscess; course finished yesterday. Also changed laundry detergent roughly 10 days ago. No new foods, no travel, no fever. No personal or family history of eczema.

Examination: Symmetrical erythematous maculopapular eruption on trunk and proximal limbs, sparing face, palms and soles. No mucosal involvement. No blistering.

Assessment: The rash might be a reaction to amoxicillin; it could equally be an irritant or allergic contact dermatitis from the new detergent, although the distribution is less typical for that. Not consistent with a severe cutaneous adverse reaction at present.

Plan: Emollients, oral antihistamine at night. Patch testing in 6 weeks. Advise patient to go back to the old detergent. Record amoxicillin as "possible allergy - under investigation", not as a confirmed allergy.

Statement: The patient's rash is a reaction to amoxicillin.""",
   0, card=FOLLOW, diff=1),

it("C2", "noul",
   "Is the statement consistent with the residents' notice and the complaint?",
   """Tollgate Court Management Company - Notice to residents (on the courtyard noticeboard)

Parking. Each flat may park one vehicle in the courtyard. Visitors must use the street. Bays are not allocated; please do not leave vehicles in front of the bin store.

Bins. Recycling is collected on Tuesdays and general waste on Fridays.

Complaint received by the management company, Monday:
"Several times recently the courtyard has been completely full on Sunday afternoons, and on one of those Sundays I couldn't get my car in at all. I'm not accusing anyone in particular, but it would help if everyone stuck to the rules. - Flat 6"

Management company reply: "Thank you. We will remind all residents of the one-vehicle rule in the next newsletter."

Statement: The occupants of Flat 2 parked two vehicles in the courtyard on a Sunday afternoon last month.""",
   1, card=CONSIST, diff=3),

it("C3", "choice",
   "How should the statement be labelled, taking the dress-code memo as accurate?",
   """From: People Team, Albarino Consulting (Lisbon office)
To: All Lisbon staff
Subject: Dress code - changes from 1 June

Olá a todos,

Following the staff survey, we are updating the dress code for the Lisbon office with effect from 1 June:

1. From 1 June, staff need not wear a tie on client visits. This applies to all grades, including partners.
2. Jackets remain expected for client visits, unless the client has told us their own dress code is casual.
3. Branded fleeces may be worn in the office but not on client visits.
4. Trainers are fine in the office on Fridays.

The Porto and Madrid offices are reviewing their own dress codes and will communicate separately.

Any questions, please speak to Beatriz in the People Team.

Obrigada,
People Team

Statement: From 1 June, Lisbon staff are required to wear a tie on client visits.""",
   C, opts=L3[1], card=L3CARD, diff=2),

it("C4", "choice",
   "Which of these employees is required by the policy to complete the leadership ethics course?",
   """Veridian Water - Learning Policy LP-6 (extract), with HR's list of queries received

LP-6.2 Leadership ethics course
(a) Every manager of a team with more than five direct reports must complete the leadership ethics course by 31 December.
(b) Any other employee may complete the course, and it will count towards their annual learning hours.
(c) Contractors and agency workers cannot enrol.
(d) For this policy, a "manager" is anyone with at least one direct report, whatever their job title.

Queries received by HR this week:
- Ottoline Barre, Head of Design: three direct reports. Asks whether she has to take the course.
- Kwame Asante, Senior Engineer: no direct reports, but chairs the safety committee. Has already completed the course.
- Rosalind Mbatha, Team Lead, Customer Contact: seven direct reports. Asks for a date in November.
- Jurgen Faltz, agency project manager: manages four agency testers. Asks how to enrol.
- Selin Arslan, Graduate Analyst: no direct reports. Would like to take the course for learning hours.""",
   "Rosalind Mbatha",
   opts=["Ottoline Barre", "Kwame Asante", "Rosalind Mbatha", "Jurgen Faltz", "Selin Arslan", NONE],
   card="- Ottoline Barre: the Head of Design\n"
        "- Kwame Asante: the Senior Engineer who chairs the safety committee\n"
        "- Rosalind Mbatha: the Customer Contact Team Lead\n"
        "- Jurgen Faltz: the agency project manager\n"
        "- Selin Arslan: the Graduate Analyst\n"
        "- none of these: the policy does not require any listed employee to complete the course",
   diff=2),

it("C5", "choice",
   "Given only the leisure centre's rules, the statement is which of these?",
   """Millbrook Leisure Centre - Gym conditions of use (members' handbook, page 4)

Age rules
- Anyone aged over 16 may use the gym unsupervised once they have completed a gym induction.
- Juniors aged 14 to 16 may use the gym only during junior sessions (weekdays 16:00-18:00), and only under the supervision of a qualified instructor.
- Children under 14 may not use the gym.

General rules
- Towels must be used on all benches.
- Free weights must be returned to the racks after use.
- Personal trainers who are not employed by the centre may not work in the gym.

Inductions are free for members and take 45 minutes. Book at reception or through the app.

Statement: Anyone aged over 18 who has completed a gym induction may use the gym unsupervised.""",
   E, opts=L3[2], card=L3CARD, diff=2,
   twin=[("Statement: Anyone aged over 18 who has completed", "Statement: Anyone aged over 14 who has completed")],
   twin_gold=C),

it("C6", "choice",
   "Relative to the hotel information sheet, which label applies to the statement?",
   """Welcome to The Glasshouse Hotel, Kinloch Bay

Pool and spa. Hotel guests may use the indoor pool only between 07:00 and 10:00 and between 16:00 and 21:00. Outside those hours the pool is reserved for swimming lessons and for members of the Kinloch Swimming Club. The sauna and steam room are open to guests from 07:00 to 21:00. Children under 12 must be accompanied by an adult in the pool at all times.

Breakfast is served in the Orangery from 07:00 to 10:30, and room service breakfast can be ordered the night before.

Check-out is at 11:00. Late check-out until 13:00 may be available on request, for a fee.

Statement: Hotel guests are permitted to use the indoor pool at 06:30.""",
   C, opts=L3[3], card=L3CARD, diff=1),

it("C7", "noul",
   "If everything on the application page is true, does it follow that the statement is true?",
   """City of Aldmoor - Residents' Parking Permit: How to apply

Who can apply: anyone whose main home is in a residents' parking zone.

Documents. Every applicant must upload:
1. proof of identity: a passport or a national identity card; and
2. proof of address dated within the last three months: a council tax bill, a utility bill, or a tenancy agreement; and
3. the vehicle registration certificate showing the applicant as the registered keeper.

Fees: 60 per year for the first vehicle, 110 per year for a second vehicle. Electric vehicles are free.

Processing takes up to 10 working days. You can park using a temporary e-permit while your application is processed.

Statement: An applicant who uploads a national identity card and no passport meets the proof-of-identity requirement.""",
   1, card=FOLLOW, diff=2),

it("C8", "noul",
   "Would accepting the contract excerpt and the email commit a reader to the statement?",
   """SUPPLY AGREEMENT between Linden Hollow Foods Ltd (Buyer) and Carrick Glassworks Ltd (Supplier) - Schedule 2 (extract)

2.1 The Supplier must deliver the first order of 40,000 jars (330 ml, lug finish) to the Buyer's warehouse at Unit 7, Fenside Estate, by 1 May.
2.2 If the Supplier fails to deliver by 1 May, the Buyer may cancel the first order without penalty.
2.3 Risk passes to the Buyer on delivery.

Email from Carrick Glassworks to Linden Hollow, 28 April, 16:20:
"Good afternoon. Your first order of 40,000 jars left our Carrick plant today on two articulated trailers. The trailers are booked into Fenside for Thursday morning, subject to traffic on the A92 roadworks. Proof of delivery will be emailed to you once the goods are signed for. - Dispatch team"

Statement: Carrick Glassworks delivered the first order to Unit 7, Fenside Estate, by 1 May.""",
   0, card=FOLLOW, diff=2),

it("C9", "choice",
   "Under the site rules, what is the status of a contractor wearing a hard hat inside the site office?",
   """Greystone Wharf Redevelopment - Site Rules (issued by the principal contractor, Harlow & Pike Construction)

PPE
R1. Everyone on site must wear safety boots and a high-visibility vest at all times.
R2. Contractors must wear hard hats on site, except in the site office and the welfare cabins, where they may remove them.
R3. Eye protection must be worn when cutting, grinding or drilling.
R4. Gloves are recommended for material handling.

Welfare
R5. Food and drink may only be consumed in the welfare cabins.
R6. Smoking is forbidden everywhere on site, including vehicles.

Visitors
R7. Visitors must sign in at the site office and be escorted at all times.

Breaches of these rules may result in removal from site.""",
   "permitted but not required", opts=DEON, card=DEONCARD, diff=3),

it("C10", "noul",
   "Can the statement be concluded from the print shop's announcement?",
   """From: Gallowgate Print Co.
To: Our business customers
Subject: New press installed - faster turnaround from Monday

Dear customers,

We're delighted to announce that our new Heidler SX-8 sheetfed press was installed at our Gallowgate works last week and commissioned on Friday. The SX-8 can print 12,000 sheets an hour, more than double the speed of the press it replaces, with inline colour measurement on every sheet.

What this means for you: from Monday, standard litho orders placed before 11:00 can be ready for collection the next working day. Large runs (over 20,000 sheets) will still need two working days.

Our first job on the SX-8 was the Gallowgate Arts Festival programme, which went out on Saturday.

As ever, thank you for your custom.

Gallowgate Print Co.

Statement: The SX-8 printed 12,000 sheets in its first hour of operation.""",
   0, card=FOLLOW, diff=2),

it("C11", "choice",
   "Given only the facilities report, what is the status of the statement?",
   """Facilities report - Brookvale Primary School, week 6

Leak in the Year 3 corridor. Water was found on the Year 3 corridor floor on Monday morning and again on Wednesday. The caretaker, Mr. Olsen, believes the leak must have started in the plant room, where the hot-water cylinder was replaced over half-term; he points out that the plant room is directly above the corridor. The plumbing contractor disagrees and thinks rainwater is getting in through the flat roof over the corridor, which was patched two years ago.

A moisture survey is booked for Friday. In the meantime the corridor is coned off and Year 3 are using the playground entrance.

Other items: the hall projector has been repaired; the staff room fridge is being replaced on Thursday.

Report compiled by: A. Nakamura, School Business Manager

Statement: The leak in the Year 3 corridor started in the plant room.""",
   U, opts=L3[4], card=L3CARD, diff=2),

it("C12", "noul",
   "Is the statement ruled out by the tenancy clause and the landlord's letter?",
   """ASSURED SHORTHOLD TENANCY - 19 Kestrel Way, Flat B (extract)

Clause 11. Subletting and lodgers
11.1 The Tenant cannot sublet the whole or any part of the Property without the Landlord's prior written consent.
11.2 The Landlord will not unreasonably withhold consent to a lodger.
11.3 Short-term holiday lets are treated as subletting for the purposes of this clause.

Letter from the Landlord, Mr. Anselm Greaves, to the Tenant, Ms. Tova Lindgren, 3 August:
"Dear Ms. Lindgren, I have received your request to let the flat on a holiday-let site for three weeks in August while you are abroad. I have considered it carefully and I am not giving consent, because my mortgage lender does not allow holiday lets. I have never given written consent to any subletting of the flat and I do not intend to. Please let me know if you would like to discuss a lodger instead. Yours sincerely, A. Greaves"

Statement: Under the tenancy, Ms. Lindgren is permitted to let the flat on a holiday-let site for three weeks in August.""",
   1, card=RULED, diff=2),

it("C13", "choice",
   "Which relation holds between the tachograph review and the statement?",
   """Haulage Compliance - Tachograph review, driver D. Kowalczyk, vehicle KX71 HRB

Rule applied (company driving-time policy, section 2):
2.1 A driver must take a break of at least 45 minutes after 4.5 hours of driving, unless the journey ends within 15 minutes of reaching 4.5 hours of driving.
2.2 Journeys ending at a customer site count as ending when the engine is switched off in the customer's yard.

Review of Tuesday's record:
- 05:30 departed depot (Castleton).
- 05:30-10:10 continuous driving (4 hours 40 minutes), no break recorded.
- 10:10 engine off in the yard of Brennan Dairy, Fellside - journey ended. Unloading until 11:00.
- 11:00 onward: driver off duty (rest day).

Reviewer comment: "Long first leg. Flagged for the driver to discuss with the transport manager at next check-in."

Statement: On Tuesday, driver D. Kowalczyk broke rule 2.1.""",
   C, opts=L3[5], card=L3CARD, diff=3),

]
