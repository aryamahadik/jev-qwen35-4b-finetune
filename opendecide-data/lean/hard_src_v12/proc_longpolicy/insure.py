"""proc_longpolicy / insurance policy wordings, schedules and endorsements."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ in01
# why: Endorsement E4 (renewal 1 Mar 2025): home is not Unoccupied for the first 60 days of
# absence if heating kept at >= 12°C. Absence from 10 Mar, burst 20 Apr = day 41, heating at
# 15°C -> not Unoccupied -> covered; escape-of-water excess £1,000 -> 8,400 - 1,000 = 7,400.
# Twin: heating switched off -> 30-day rule -> Unoccupied at day 41 -> excluded.
C("in01", "How should the claims handler settle the escape of water claim?",
"""
HEARTHSTONE MUTUAL — HOME INSURANCE POLICY WORDING (edition 7)

DEFINITIONS
"Buildings": the home, its fixtures and fittings, and permanent outbuildings.
"Escape of Water": water escaping from a fixed water or heating installation.
"Unoccupied": not lived in by you or your family for more than 30 consecutive days.
"Excess": the first part of each claim, which you pay.
"Period of Insurance": the period shown in the schedule.

SECTION 1 — BUILDINGS
1.1 We cover loss or damage to the Buildings caused by the insured events below.
1.2 Fire, lightning, explosion or earthquake.
1.3 Storm or flood, but not damage to gates, fences or hedges.
1.4 Escape of Water. We do not cover Escape of Water while the home is Unoccupied.
1.5 Theft or attempted theft involving forcible entry.
1.6 Subsidence, heave or landslip, subject to a £1,000 Excess.

SECTION 2 — CONTENTS
2.1 We cover your household goods and personal belongings in the home against the insured events in Section 1.

GENERAL CONDITIONS
G1. You must tell us about any claim as soon as reasonably possible.
G2. You must take reasonable care to prevent loss, including keeping the home in good repair.
G3. We may appoint a loss adjuster and may repair rather than pay cash.

EXCESSES
Standard Excess: £350 for every claim.
Escape of Water Excess: £1,000, which replaces the Standard Excess for Escape of Water claims.

HOW WE SETTLE CLAIMS
S1. We pay the cost of repair, or of rebuilding if the damage cannot be repaired economically.
S2. We do not pay for wear and tear, or for the cost of repairing the installation that failed, only for the damage the water caused.
S3. Endorsements shown on your schedule change this wording from the date they take effect.

ENDORSEMENT E4 — added at renewal on 1 March 2025
"The definition of Unoccupied is amended: the home is not treated as Unoccupied during the first 60 consecutive days of absence, provided the central heating is kept on at a minimum of 12°C throughout. Where that proviso is not met, the 30-day limit in the definition continues to apply."

CLAIM HX-40291
Policyholder: Rowan Castellane. Period of Insurance: 1 March 2025 to 28 February 2026.
• Mr Castellane was away visiting family from 10 March 2025 and returned on 24 April 2025.
• The central heating was left on at 15°C throughout, confirmed by the smart thermostat log.
• A pipe under the bathroom floor split on 20 April 2025; a neighbour noticed water coming through the ceiling.
• Agreed cost of repairs: £8,400.
• Loss adjuster's note: "Home empty for over 30 days — standard exclusion should apply, surely."
""",
[("pay_7400", "Under Endorsement E4 the home was not Unoccupied on day 41 with heating at 15°C, so the claim is paid less the £1,000 Escape of Water Excess."),
 ("decline_unoccupied", "The home counted as Unoccupied when the pipe split, so the Escape of Water exclusion in 1.4 applies."),
 ("pay_8050", "The damage is covered because the heating was on, and as Endorsement E4 does not mention excesses, the Standard Excess of £350 applies, leaving £8,050."),
 ("pay_8400", "Leaving the heating on shows the policyholder took reasonable care under G2, so the Escape of Water Excess is waived and the full £8,400 is paid.")],
"pay_7400", 2,
twin=T([("The central heating was left on at 15°C throughout, confirmed by the smart thermostat log.",
         "The central heating was switched off for the whole absence, confirmed by the smart thermostat log.")], "decline_unoccupied")),

# ------------------------------------------------------------------ in02
# why: policy issued 4 Jul 2025 -> amendment (policies issued on/after 1 Jun 2025) uses a
# 12-month look-back. Last asthma treatment January 2024 = 18 months before -> not a
# Pre-existing Medical Condition -> covered: 1,240 - 100 excess = 1,140.
# Twin: last prescription November 2024 -> within 12 months -> undeclared PEMC -> declined.
C("in02", "What should the travel insurer decide on the cancellation claim?",
"""
WAYFARER TRAVEL INSURANCE — SINGLE TRIP POLICY WORDING

DEFINITIONS
"Pre-existing Medical Condition": any medical condition for which you received treatment, medication or a prescription in the 24 months before the date your policy was issued.
"Trip": the journey shown on your certificate.
"Close Relative": spouse or partner, parent, child, sibling or grandparent.
"Excess": £100 per person per claim under Sections A and B.

IMPORTANT CONDITIONS
IC1. You must declare every Pre-existing Medical Condition before the policy is issued. We do not cover any claim arising from a Pre-existing Medical Condition that was not declared and accepted by us.
IC2. You must be resident in the Commonwealth of Arvane and have a valid health card.

SECTION A — CANCELLATION
A1. We pay non-refundable travel and accommodation costs if you must cancel the Trip because of the unforeseen illness, injury or death of you or a Close Relative, confirmed by a doctor.
A2. We do not pay if you cancel because you no longer want to travel.
A3. The most we pay is £5,000 per person.

SECTION B — MEDICAL EXPENSES ABROAD
B1. We pay emergency medical treatment abroad up to £10 million.

SECTION C — BAGGAGE
C1. We pay up to £1,500 for lost or stolen baggage, with a single item limit of £300.

SECTION D — TRAVEL DELAY
D1. We pay £25 for each full 12 hours of delay, up to £250.

SECTION E — PERSONAL LIABILITY
E1. We cover your legal liability abroad for injury to others or damage to their property, up to £2 million.

HOW TO CLAIM
H1. Send us the booking invoice, cancellation invoice and a medical certificate within 28 days of cancelling.
H2. We may ask for your GP records for the period relevant to the definition of Pre-existing Medical Condition.

POLICY AMENDMENT — applies to policies issued on or after 1 June 2025
PA1. In the definition of Pre-existing Medical Condition, "24 months" is replaced by "12 months".
PA2. Condition IC1 is unchanged.

CLAIM WT-77120
• Policy issued: 4 July 2025. Trip to the Solvane coast booked for 20 to 30 September 2025.
• No medical conditions were declared on the application.
• GP records: asthma diagnosed 2015; last inhaler prescription issued in January 2024; no treatment or prescriptions since.
• 12 September 2025: admitted to hospital with a severe asthma attack; hospital doctor confirms she was unfit to travel.
• Non-refundable costs of the Trip: £1,240.
• Claims assessor's draft: "Asthma is a long-standing condition she didn't declare — decline under IC1."
""",
[("pay_1140", "Under the amended 12-month look-back the asthma is not a Pre-existing Medical Condition, so cancellation is covered less the £100 Excess."),
 ("decline_pre_existing", "The asthma counts as a Pre-existing Medical Condition under the wording that governs this policy, and it was not declared, so IC1 excludes the claim."),
 ("pay_1240", "Cancellation on a doctor's advice is covered in full, and no Excess applies to hospital admissions."),
 ("decline_not_unforeseen", "Asthma diagnosed in 2015 makes the attack foreseeable, so Section A1 does not respond.")],
"pay_1140", 2,
twin=T([("last inhaler prescription issued in January 2024", "last inhaler prescription issued in November 2024")], "decline_pre_existing")),

# ------------------------------------------------------------------ in03
# why: named driver Mira has Social, Domestic and Pleasure only; driving to a client meeting
# for her employer is business use -> own damage not covered; clause 8.3 means third-party
# claims are met as the law requires and recovered. Twin: trip to a birthday lunch = SDP ->
# covered; Endorsement 2 (from 1 Feb 2025) lowers young-driver age to under 23; Mira is 24 ->
# only the £250 compulsory excess.
C("in03", "How should the motor insurer handle the claim from the collision on 19 June 2025?",
"""
KINGFISHER MOTOR — PRIVATE CAR POLICY

DEFINITIONS
"Social, Domestic and Pleasure" (SDP): use for private purposes, including commuting to one permanent place of work, but not for any business purpose.
"Business Use": use in connection with any business or employment, other than commuting.
"Named Driver": a person shown on the certificate as entitled to drive.
"Own Damage": loss of or damage to the insured car.

SECTION 1 — LIABILITY TO OTHERS
1.1 We cover your legal liability for injury to others and damage to their property arising from the use of the car by a person entitled to drive under the certificate.

SECTION 2 — OWN DAMAGE
2.1 We cover Own Damage caused by accident, fire or theft.
2.2 We may repair the car or pay its market value.

SECTION 8 — EXCLUSIONS AND RIGHTS OF RECOVERY
8.1 We do not cover any claim while the car is used for a purpose not permitted by the certificate.
8.2 We do not cover any claim while the car is driven by someone not entitled to drive under the certificate.
8.3 Where the law requires us to pay a third party despite 8.1 or 8.2, we will do so and may recover what we pay from you. We do not pay Own Damage in those cases.

EXCESSES
Compulsory Excess: £250 on every Own Damage claim.
Young Driver Excess: an additional £300 when the car is driven by anyone under 25.

SECTION 4 — WINDSCREEN
4.1 Windscreen repair or replacement without affecting your no-claims discount, excess £90.

SECTION 5 — NO-CLAIMS DISCOUNT
5.1 A claim where we cannot recover our payment in full will reduce your no-claims discount.

CERTIFICATE (from renewal on 1 February 2025)
Policyholder: Dominic Aldane — SDP and Business Use by the policyholder only.
Named Driver: Mira Aldane (aged 24) — SDP only.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

ENDORSEMENT 2 — effective from renewal on 1 February 2025
"In the Young Driver Excess, 'under 25' is replaced by 'under 23'."

CLAIM KM-58810
• 19 June 2025: Mira Aldane drove the insured car to a client meeting for her employer, Cobbet & Rye Surveyors, and collided with a parked van.
• Third-party van damage: £2,900. Own Damage to the insured car: £4,600.
• Mira holds a full licence with no convictions.
• Dominic's email: "Mira's on the policy, so she's covered for anything. Please just pay both."
""",
[("pay_third_party_recover_decline_own_damage", "The trip was Business Use, which the Named Driver may not do, so Own Damage is declined and only the legally required third-party payment is made, with recovery."),
 ("settle_less_250", "The journey was within the Named Driver's permitted use and she is 23 or over, so the claim is paid subject only to the £250 Compulsory Excess."),
 ("settle_less_550", "The journey was within the Named Driver's permitted use, so the claim is paid less the £250 Compulsory Excess and the £300 Young Driver Excess, as she is under 25."),
 ("decline_all_claims", "Use outside the certificate means the insurer pays nothing at all, including to the van owner.")],
"pay_third_party_recover_decline_own_damage", 3,
twin=T([("drove the insured car to a client meeting for her employer, Cobbet & Rye Surveyors,", "drove the insured car to her sister's birthday lunch")], "settle_less_250")),

# ------------------------------------------------------------------ in04
# why: Denial of Access extension covers a cordon due to an incident within 1 mile; the
# endorsement (from 1 Jan 2025) cuts the Denial of Access waiting period to 24 h. Closed 5
# days: first day excluded -> 4 x 2,000 = 8,000. Twin: incident 1.6 miles away -> outside
# extension; no damage at premises -> BI does not respond.
C("in04", "What should the insurer pay under the business interruption section?",
"""
LANTERN COMMERCIAL — SHOP AND OFFICE COMBINED POLICY

DEFINITIONS
"Premises": the shop at 14 Tanner's Row, Eastholm.
"Damage": physical loss or damage.
"Gross Profit": turnover less the cost of goods sold.
"Waiting Period": the period at the start of an interruption for which no business interruption loss is paid.
"Indemnity Period": the period, up to 12 months, during which results are affected.

SECTION 1 — MATERIAL DAMAGE
1.1 We cover Damage to buildings, stock and contents at the Premises caused by an insured event.

SECTION 2 — BUSINESS INTERRUPTION
2.1 We pay loss of Gross Profit resulting from interruption of the business caused by Damage at the Premises, during the Indemnity Period.
2.2 The Waiting Period is 72 hours.

EXTENSION 2A — DENIAL OF ACCESS
2A.1 Section 2 also covers interruption where access to the Premises is prevented by a police or local authority cordon imposed because of an incident within 1 mile of the Premises, even without Damage at the Premises.
2A.2 The most we pay under this extension is £25,000 per claim.

SECTION 3 — MONEY
3.1 We cover money on the Premises up to £2,500, or £500 overnight outside a safe.

SECTION 4 — EMPLOYERS' LIABILITY
4.1 Cover as required by law, limit £10 million.

CONDITIONS
C1. You must keep proper books of account and let us inspect them.
C2. You must tell us of any interruption within 14 days.

C3. You must take all reasonable steps to minimise the interruption, including trading from temporary premises if practical.
C4. Endorsements change this policy only for the claims they describe.

HOW BUSINESS INTERRUPTION IS CALCULATED
H1. We compare Gross Profit during the interruption with the same period in the previous year, adjusted for trends.
H2. Savings in costs during the interruption are deducted.

ENDORSEMENT 11 — effective 1 January 2025
"For claims under Extension 2A only, the Waiting Period is 24 hours. The Waiting Period for all other claims under Section 2 is unchanged."

CLAIM LC-3318
• On 3 March 2025 a gas main ruptured on Mill Street, 0.4 miles from the Premises. Police set a cordon that closed Tanner's Row.
• The shop was unable to open for 5 full days, 3 to 7 March.
• No Damage occurred at the Premises.
• Accountant's figures: loss of Gross Profit £2,000 per day, constant across the closure.
• Notified to the insurer on 10 March 2025.
""",
[("pay_8000", "The cordon falls within Extension 2A and its 24-hour Waiting Period removes one day, so four days at £2,000 are paid."),
 ("pay_4000", "The 72-hour Waiting Period removes three of the five days, so two days at £2,000 are paid."),
 ("pay_10000", "Denial of Access claims carry no Waiting Period, so all five days at £2,000 are paid."),
 ("decline_no_damage", "No insured Damage occurred at the Premises and the incident falls outside the reach of the Denial of Access extension, so Section 2 does not respond.")],
"pay_8000", 2,
twin=T([("on Mill Street, 0.4 miles from the Premises", "on Mill Street, 1.6 miles from the Premises")], "decline_no_damage")),

# ------------------------------------------------------------------ in05
# why: conversion to lifetime cover on 1 Apr 2025 carries a carve-out: conditions first showing
# signs before conversion stay on the time-limited basis (12 months from first signs). First
# signs February 2024 -> cover ended February 2025 -> June 2025 treatment declined.
# Twin: first signs May 2025 (after conversion) -> lifetime -> 2,200 - 100 = 2,100.
C("in05", "How should the pet insurer settle the June 2025 vet invoice?",
"""
PAWPRINT PET INSURANCE — DOG POLICY WORDING

DEFINITIONS
"Condition": an illness or injury, and any related illness or injury, however many parts of the body are affected.
"First Signs": the date clinical signs of a Condition were first noticed by you or a vet, whether or not diagnosed.
"Policy Year": each 12-month period from the start or renewal date.
"Excess": £100 per Condition per Policy Year.

PLAN: TIME-LIMITED 3000
T1. We pay vet fees for each Condition for up to 12 months from its First Signs, up to £3,000 per Condition.
T2. After 12 months, or once £3,000 is reached, the Condition is no longer covered.

GENERAL EXCLUSIONS
X1. Conditions with First Signs before the policy started or within the first 14 days.
X2. Routine treatment, vaccinations, grooming and neutering.
X3. Bilateral conditions where the other side showed signs before the policy started.

COMPLEMENTARY TREATMENT
CT1. Hydrotherapy and physiotherapy are covered when referred by a vet, within the Condition's limit.

THIRD PARTY LIABILITY
L1. Up to £2 million for injury or damage caused by your dog.

HOW TO CLAIM
H1. Your vet completes the claim form and sends the invoice and clinical history.
H2. We decide which plan applies to each Condition by reference to its First Signs.
H3. We pay the vet directly if you ask us to.

CHANGES AT RENEWAL
H4. We may change the plan, premium or Excess at renewal by giving you 21 days' notice.

ACCESSIBILITY
This document is available in large print, audio and easy-read formats on request. Anyone who needs help to understand it, or to take part in a process it describes, may ask for reasonable adjustments.

RENEWAL ENDORSEMENT — plan conversion effective 1 April 2025
R1. From 1 April 2025 your plan becomes LIFETIME 5000: we pay vet fees up to £5,000 per Policy Year, resetting at each renewal, for as long as the policy continues.
R2. Any Condition with First Signs before 1 April 2025 remains covered on the TIME-LIMITED 3000 basis only.
R3. The Excess is unchanged.

CLAIM PP-20931 — Bramble, Labrador, aged 6. Policy started 3 January 2023.
• Clinical history: lameness in the left hind leg first noticed by the owner in February 2024; diagnosed as partial cruciate ligament rupture.
• £1,850 paid in 2024 for conservative treatment of the left knee.
• June 2025: surgery on the left knee after the rupture became complete. Invoice: £2,200.
• Other claims: ear infection, November 2024, £180 paid.
• Owner's message: "We switched to lifetime cover so this should all be paid now."
""",
[("decline_time_limit_expired", "The knee Condition first showed before the conversion, so it stays time-limited, and its 12 months from First Signs had run out by February 2025."),
 ("pay_2100", "The knee Condition falls under the lifetime plan, so the £2,200 invoice is paid less the £100 Excess."),
 ("pay_2200", "Lifetime cover applies from April 2025, and because the Excess for this Condition was already taken in 2024, nothing more is deducted from the £2,200 invoice."),
 ("pay_1150", "The time-limited plan still has £1,150 left of its £3,000 limit for the knee Condition after the £1,850 paid in 2024, so that balance is paid.")],
"decline_time_limit_expired", 3,
twin=T([("lameness in the left hind leg first noticed by the owner in February 2024; diagnosed as partial cruciate ligament rupture.\n• £1,850 paid in 2024 for conservative treatment of the left knee.",
         "lameness in the left hind leg first noticed by the owner in May 2025; diagnosed as partial cruciate ligament rupture.\n• No earlier treatment of the left knee.")],
       "pay_2100")),

# ------------------------------------------------------------------ in06
# why: renewal schedule (from 1 Jan 2025) specifies the bicycle at £1,500; theft away from
# home covered if locked to an immovable object; bike locked to railings -> pay 1,500 - 100
# = 1,400. Twin: left unlocked -> condition fails -> decline.
C("in06", "How should the contents claim for the stolen bicycle be settled?",
"""
CLOVERLEAF HOME CONTENTS — POLICY WORDING AND SCHEDULE

DEFINITIONS
"Contents": household goods and personal belongings owned by you or your family.
"Single Article Limit": the most we pay for any one item that is not a Specified Item — £1,000.
"Specified Item": an item listed on your schedule with its own sum insured.
"Personal Possessions": Contents you take away from the home.
"Excess": £100 per claim.

SECTION 1 — CONTENTS IN THE HOME
1.1 We cover Contents in the home against fire, flood, storm, escape of water and theft.

SECTION 2 — PERSONAL POSSESSIONS (optional; shown on schedule)
2.1 We cover Personal Possessions anywhere in the world against loss, theft and accidental damage.
2.2 Bicycles are covered away from the home only when locked to an immovable object with a lock. We do not cover theft of a bicycle left unlocked.
2.3 For any item that is not a Specified Item, the Single Article Limit applies.

SECTION 3 — LEGAL EXPENSES (optional)
3.1 Up to £50,000 for consumer disputes and employment disputes.

CONDITIONS
C1. Report theft to the police within 48 hours and give us the crime reference.
C2. Provide proof of ownership and value, such as a receipt or bank statement.

C3. You must take reasonable care of your Personal Possessions and not leave them unattended in a public place.

HOW WE SETTLE
S1. For a Specified Item we pay the replacement cost up to the amount shown on the schedule.
S2. For other items we pay the replacement cost up to the Single Article Limit.
S3. We may replace an item rather than pay cash, using our suppliers.

NO-CLAIMS DISCOUNT
N1. Any claim paid reduces the no-claims discount at renewal by two years.

SEVERABILITY
If any provision of this document is found to be invalid or unenforceable, the remaining provisions continue in full force, and the invalid provision is replaced by a valid one as close as possible to its original intention.

SCHEDULE — renewal effective 1 January 2025
Sum insured, Contents: £45,000. Personal Possessions: included.
Specified Items: Engagement ring £3,200; Road bicycle, Halvard Strada 7, £1,500.

CLAIM CL-6612
• 14 May 2025: the road bicycle was stolen outside the Greenmarket library while locked to the railings with a D-lock; the lock was cut.
• Police crime reference obtained the same day.
• Receipt from 2023 shows purchase price £1,800; current replacement cost £1,850.
• Previous schedule (2024) did not specify the bicycle.
• Policyholder's email: "I'd like the full £1,800 I paid for it."
""",
[("pay_1400", "The bicycle is a Specified Item insured for £1,500 and was locked to an immovable object, so £1,500 less the £100 Excess is paid."),
 ("pay_900", "The bicycle is treated like any other item taken from the home, so the £1,000 Single Article Limit applies, less the £100 Excess, giving £900."),
 ("pay_1700", "The 2023 receipt proves a value of £1,800, which the insurer must pay on a theft claim, less the £100 Excess, giving £1,700."),
 ("decline_bicycle_unlocked", "The bicycle was not locked to an immovable object when it was stolen, so clause 2.2 excludes the theft.")],
"pay_1400", 1,
twin=T([("while locked to the railings with a D-lock; the lock was cut", "while left unlocked against the railings for a few minutes")], "decline_bicycle_unlocked")),

# ------------------------------------------------------------------ in07
# why: claims-made PI; Endorsement 3 moves the Retroactive Date back to 1 Jan 2019 for
# continuity; work done October 2020 is after it; notified 20 days after claim (within 30);
# client complaint first raised after the policy started -> accept.
# Twin: work done October 2018 -> before the Retroactive Date -> decline.
C("in07", "Should the professional indemnity insurer accept the claim?",
"""
ASHLAR PROFESSIONAL INDEMNITY — CLAIMS-MADE POLICY FOR DESIGN CONSULTANTS

DEFINITIONS
"Claim": a written demand for compensation made against you.
"Retroactive Date": the date shown in the schedule. Work carried out before it is not covered.
"Period of Insurance": 1 January 2025 to 31 December 2025.
"Circumstance": an incident likely to give rise to a Claim.

INSURING CLAUSE
1.1 We cover Claims first made against you during the Period of Insurance arising from your professional work carried out on or after the Retroactive Date.

CONDITIONS
2.1 You must notify us of any Claim within 30 days of receiving it.
2.2 You must not admit liability or agree any settlement without our consent.
2.3 You must maintain records of each project for at least 12 years.

EXCLUSIONS
3.1 Any Claim arising from a Circumstance you knew of before the Period of Insurance began and did not disclose.
3.2 Contractual penalties and liquidated damages.
3.3 Fines imposed by a regulator.

LIMIT AND EXCESS
Limit: £2 million any one Claim. Excess: £5,000 each Claim.

DEFENCE COSTS
4.1 We pay defence costs incurred with our consent in addition to the Limit.

ARBITRATION
5.1 Disagreements about the amount payable are referred to an arbitrator; disagreements about cover go to the courts.

RUN-OFF
6.1 If you cease trading we will offer run-off cover for six years on terms we decide.

SCHEDULE
Insured: Pennant Structural Design LLP.
Retroactive Date: 1 January 2022.

ACCESSIBILITY
This document is available in large print, audio and easy-read formats on request. Anyone who needs help to understand it, or to take part in a process it describes, may ask for reasonable adjustments.

ENDORSEMENT 3 — continuity of cover, effective from the start of the Period of Insurance
"Pennant has provided evidence of continuous PI cover with its previous insurer since 2019. The Retroactive Date in the schedule is changed to 1 January 2019."

CLAIM FILE AP-1182
• Project: structural design for a two-storey extension at Wyvern Farm, carried out in October 2020.
• First contact from the client about cracking: letter of claim dated 3 March 2025, received the same day.
• Notified to Ashlar on 23 March 2025.
• Pennant's partners confirm they had no knowledge of any problem before the letter of claim; the proposal form declared no Circumstances.
• Claim value stated: £140,000.
• Underwriter's note: "Retro date on the schedule is 2022. Project is 2020."
""",
[("accept_claim", "Endorsement 3 moves the Retroactive Date to 1 January 2019, the work followed it, and the Claim was notified within 30 days, so it is covered."),
 ("decline_before_retro_date", "The work was carried out before the Retroactive Date that applies, so the insuring clause does not cover it."),
 ("decline_late_notification", "The letter of claim arrived on 3 March and Ashlar heard about it only on 23 March, more than the 14 days allowed, so the notice condition was breached."),
 ("decline_prior_knowledge", "The cracking arose from a 2020 project, so it is a Circumstance that existed before the Period of Insurance and is excluded by 3.1.")],
"accept_claim", 2,
twin=T([("carried out in October 2020", "carried out in October 2018")], "decline_before_retro_date")),

# ------------------------------------------------------------------ in08
# why: Endorsement (events from 1 May 2025) adds yellow warnings for gusts above 50 mph as a
# covered weather trigger; 55 mph -> covered; weather claims carry 20% co-insurance ->
# 80% of £42,000 = £33,600. Twin: 45 mph -> no qualifying warning -> decline.
C("in08", "What should the event cancellation insurer pay the organiser?",
"""
STAGEGUARD EVENT CANCELLATION POLICY — OUTDOOR EVENTS

DEFINITIONS
"Event": the event named in the schedule.
"Weather Warning": a warning issued by the National Weather Office for the Event location.
"Ascertained Net Loss": irrecoverable costs incurred, less savings, as agreed by our loss adjuster.
"Co-insurance": the percentage of each loss that you bear yourself.

INSURING CLAUSE
1.1 We pay your Ascertained Net Loss if the Event is cancelled, abandoned or postponed solely and directly because of a cause beyond your control.

WEATHER
2.1 Cancellation because of weather is covered only if an amber or red Weather Warning for wind, rain or thunderstorms is in force for the Event location on the Event date.
2.2 Every weather claim is subject to 20% Co-insurance.
2.3 Cancelling because of a forecast alone, without a qualifying Weather Warning, is not covered.

EXCLUSIONS
3.1 Lack of ticket sales or financial failure of the Event.
3.2 Non-appearance of any performer, unless the performer is individually insured.
3.3 Cancellation because of communicable disease.

CLAIMS CONDITIONS
4.1 Notify us within 7 days of cancellation.
4.2 Keep all invoices and contracts for our adjuster.

ADJUSTMENT
5.1 The Ascertained Net Loss excludes any profit you expected to make, and any refunds you receive from suppliers.
5.2 Ticket refunds you are legally required to make are part of the Ascertained Net Loss.

DISPUTES
6.1 If we disagree about the amount of the loss, an independent adjuster may be appointed at shared cost.

SCHEDULE
Event: Brackenfield Folk Weekend, Coldharbour Meadows, 7 to 8 June 2025.
Sum insured: £120,000.

RIGHTS OF THIRD PARTIES
No person other than the parties named in this document has any right to enforce its terms, except where the document expressly says otherwise.

ENDORSEMENT 5 — applies to Events taking place on or after 1 May 2025
"Clause 2.1 is extended: a yellow Weather Warning for wind is also a qualifying Weather Warning where it forecasts gusts above 50 mph."

CLAIM SG-9014
• 6 June 2025: the National Weather Office issued a yellow Weather Warning for wind for Coldharbour, forecasting gusts of up to 55 mph on 7 June.
• The organiser cancelled on the evening of 6 June after the safety advisory group met.
• Ascertained Net Loss agreed by the adjuster: £42,000.
• Notified on 9 June 2025.
• Organiser's email: "Please pay the full £42,000 — we had no choice."
""",
[("pay_33600", "The yellow warning forecasting gusts above 50 mph qualifies under Endorsement 5, and the 20% Co-insurance leaves 80% of £42,000 payable."),
 ("pay_42000", "The safety advisory group made the cancellation unavoidable, so it was beyond the organiser's control and the full Ascertained Net Loss of £42,000 is paid."),
 ("decline_warning_level", "No Weather Warning at the level the policy requires was in force, so the cancellation is not covered."),
 ("decline_voluntary_cancellation", "The organiser chose to cancel after a meeting, so it was a voluntary decision rather than a cause beyond its control.")],
"pay_33600", 2,
twin=T([("forecasting gusts of up to 55 mph on 7 June", "forecasting gusts of up to 45 mph on 7 June")], "decline_warning_level")),

# ------------------------------------------------------------------ in09
# why: Endorsement (renewals from 1 Jan 2025) cuts deferred period to 8 weeks; incapacity began
# Mon 3 Mar 2025 while it applied -> 3 Mar + 56 days = 28 Apr 2025. Twin: endorsement from
# 1 May 2025 -> incapacity began before it -> 13 weeks -> 3 Mar + 91 days = 2 Jun 2025.
C("in09", "From what date is income protection benefit payable?",
"""
STEADFAST INCOME PROTECTION — INDIVIDUAL POLICY

DEFINITIONS
"Incapacity": being unable, because of illness or injury, to carry out the material duties of your own occupation, and not doing any other work.
"Deferred Period": the continuous period of Incapacity that must pass before benefit starts. Benefit is payable from the day after the Deferred Period ends.
"Pre-incapacity Earnings": your average monthly earnings over the 12 months before Incapacity began.
"Linked Claim": a new Incapacity from the same cause within 6 months of the end of a previous paid claim.

BENEFIT
1.1 Benefit is 60% of Pre-incapacity Earnings, up to £4,000 a month, paid monthly in arrears.
1.2 The Deferred Period is 13 weeks.
1.3 For a Linked Claim, no new Deferred Period applies.
1.4 The version of the policy that applies to a claim is the version in force on the day Incapacity began.

REHABILITATION
2.1 We may pay for treatment that helps you return to work sooner.
2.2 Proportionate benefit is paid if you return on reduced hours.

EXCLUSIONS
3.1 Incapacity caused by intentional self-injury, or by taking part in a riot.
3.2 Normal pregnancy, unless complications arise.

CLAIMS
4.1 Tell us within four weeks of Incapacity starting; we may reduce benefit if you tell us later.

INDEXATION
5.1 Benefit in payment increases each year on the claim anniversary in line with the retail price index, capped at 5%.

PREMIUMS
6.1 Premiums are payable monthly. If a premium is unpaid for 60 days the policy lapses, and claims for Incapacity beginning after the lapse are not covered.
6.2 Premiums are waived while benefit is being paid.

TERMINATION OF BENEFIT
7.1 Benefit stops when you return to work, reach the policy end age of 65, or die.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

ENDORSEMENT — effective for policies renewed on or after 1 January 2025
"In clause 1.2, '13 weeks' is replaced by '8 weeks'."

CLAIM SIP-3017
• Policyholder: Anouk Delacroix, self-employed landscape architect. Policy renewed on 1 January 2025.
• Incapacity began on Monday 3 March 2025 (back injury; surgery 10 March). Continuous since.
• Previous claims: none.
• Claim notified 20 March 2025.
• Pre-incapacity Earnings: £5,200 a month.
""",
[("benefit_from_28_april", "The 8-week Deferred Period in force when Incapacity began ends after 27 April, so benefit is payable from 28 April 2025."),
 ("benefit_from_2_june", "The 13-week Deferred Period that governs this claim ends after 1 June, so benefit is payable from 2 June 2025."),
 ("benefit_from_3_march", "Surgery within the first week makes this an immediate claim, so benefit runs from the first day of Incapacity."),
 ("benefit_from_26_may", "Twelve weeks after Incapacity began, benefit becomes payable on 26 May 2025.")],
"benefit_from_28_april", 2,
twin=T([("effective for policies renewed on or after 1 January 2025", "effective for policies renewed on or after 1 May 2025")], "benefit_from_2_june")),

# ------------------------------------------------------------------ in10
# why: renewal endorsement raised the buildings sum insured to £500,000 before the loss.
# Value at loss £600,000; 85% = 510,000 > 500,000 -> average applies: 90,000 x 500/600 =
# 75,000. Twin: value £580,000 -> 85% = 493,000 <= 500,000 -> no average -> 90,000.
C("in10", "What amount should the insurer pay for the fire damage?",
"""
MERIDIAN COMMERCIAL PROPERTY — POLICY WORDING

DEFINITIONS
"Sum Insured": the amount shown in the schedule for each item, as amended by endorsement.
"Reinstatement Value": the cost of rebuilding the property as new at the time of loss.
"Average": the proportional reduction of a claim for under-insurance.

BASIS OF SETTLEMENT
1.1 Buildings are insured on a reinstatement basis.
1.2 Average: if, at the time of loss, the Sum Insured is less than 85% of the Reinstatement Value, the amount we pay is reduced in the proportion that the Sum Insured bears to the Reinstatement Value.
1.3 If the Sum Insured is 85% or more of the Reinstatement Value, Average does not apply.

EXCESS
2.1 No excess applies to fire claims. All other claims carry a £1,000 excess.

EXTENSIONS
3.1 Debris removal, up to 10% of the Sum Insured, in addition to the Sum Insured.
3.2 Architects' fees are included within the Sum Insured.

CONDITIONS
4.1 You must keep the premises in good repair and test fire alarms monthly.
4.2 Claims must be notified within 14 days.

VALUATIONS
5.1 You should obtain a professional rebuilding valuation at least every three years. The Sum Insured is not index-linked on this policy.
5.2 Day one reinstatement basis is not operative on this policy.

OUR RIGHTS
6.1 We may enter the premises after a loss and take possession of damaged property.
6.2 We may choose to reinstate rather than pay.

SCHEDULE — policy year 1 October 2024 to 30 September 2025
Premises: Unit 6, Rushford Trade Park. Item 1, Buildings: Sum Insured £400,000.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

ENDORSEMENT 2 — effective 1 February 2025
"Following the valuation survey, the Sum Insured for Item 1, Buildings, is increased to £500,000. Additional premium charged."

CLAIM MC-7702
• Fire on 18 April 2025 damaged the roof and one side wall of Unit 6.
• Loss adjuster's agreed cost of repairs: £90,000 (no debris removal claimed).
• Reinstatement Value of the whole building at the time of loss, per the adjuster's surveyor: £600,000.
• Fire alarm test records are complete.
• Broker's email: "Client was fully insured after the valuation, so we expect £90,000."
""",
[("pay_75000", "The £500,000 Sum Insured is below 85% of the £600,000 value, so Average applies and £90,000 × 500/600 = £75,000 is paid."),
 ("pay_60000", "The £400,000 Sum Insured on the schedule is two-thirds of the £600,000 value, so Average reduces the claim to £90,000 × 400/600 = £60,000."),
 ("pay_90000", "The Sum Insured is at least 85% of the Reinstatement Value, so Average does not apply and the full £90,000 is paid."),
 ("pay_88235", "Average compares the Sum Insured with 85% of the value (£510,000), so the claim is reduced to £90,000 × 500,000/510,000 = £88,235.")],
"pay_75000", 3,
twin=T([("at the time of loss, per the adjuster's surveyor: £600,000", "at the time of loss, per the adjuster's surveyor: £580,000")], "pay_90000")),

# ------------------------------------------------------------------ in11
# why: Endorsement 7 limits the alarm condition to times the Premises are Unattended; two staff
# were in the stockroom -> attended -> theft while open to the public needs no forcible entry
# -> pay 6,200 - 250 = 5,950. Twin: nobody on premises -> Unattended with alarm unset -> decline.
C("in11", "How should the theft claim from the Kelso Street shop be decided?",
"""
BELLWETHER RETAIL INSURANCE — SHOPKEEPERS' POLICY

DEFINITIONS
"Premises": the shop at 22 Kelso Street, Tarnby.
"Business Hours": the hours the Premises are open to the public.
"Unattended": no employee of yours is present anywhere on the Premises.
"Stock": goods held for sale.

SECTION 3 — THEFT
3.1 We cover theft of Stock and contents from the Premises.
3.2 Outside Business Hours, theft is covered only if entry to or exit from the Premises was by forcible and violent means.
3.3 During Business Hours, theft by customers or intruders is covered without forcible entry.

PROTECTIONS CONDITION
P1. The intruder alarm must be fully set whenever the Premises are closed or left without anyone in charge. We will not pay for theft occurring while the alarm is not set.

EXCESS
Theft: £250 each claim.

SECTION 5 — GLASS
5.1 Breakage of fixed glass in shop fronts, excess £100.

SECTION 6 — GOODS IN TRANSIT
6.1 Stock in your own vehicle up to £5,000, if the vehicle is locked.

SECTION 7 — PUBLIC LIABILITY
7.1 Up to £5 million for injury to customers or damage to their property.

CLAIMS CONDITIONS
CC1. Report theft to the police within 24 hours and to us within seven days.
CC2. Keep CCTV footage for at least 30 days after an incident.
CC3. Stock is valued at cost price, not selling price.

ACCESSIBILITY
This document is available in large print, audio and easy-read formats on request. Anyone who needs help to understand it, or to take part in a process it describes, may ask for reasonable adjustments.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

ENDORSEMENT 7 — effective 1 March 2025
"Condition P1 is replaced: 'The intruder alarm must be fully set whenever the Premises are closed or Unattended. We will not pay for theft occurring while the Premises are Unattended and the alarm is not set.'"

CLAIM BR-5540
• Date: Tuesday 6 May 2025, 14:05, during Business Hours.
• Circumstances: two staff members were in the stockroom unpacking a delivery while the front door was open to customers; a person entered and took three boxed coffee machines from the display.
• CCTV confirms the theft. Police reference obtained.
• Alarm: not set at the time.
• Value of Stock taken, at cost: £6,200.
• Claims handler's draft: "Alarm wasn't set — straightforward decline under the protections condition."
""",
[("pay_5950", "Endorsement 7 requires the alarm only when the shop is closed or Unattended; staff were present, so the theft is covered less the £250 excess."),
 ("decline_alarm_not_set", "The Premises were left without anyone present and the alarm was not set, so the protections condition defeats the claim."),
 ("pay_6200", "Theft during Business Hours is covered under 3.3 without any excess, because the excess applies only to break-ins, so the full £6,200 is paid."),
 ("decline_no_forcible_entry", "The thief simply walked in through the open front door, so there was no forcible and violent entry, and without it the theft section does not respond.")],
"pay_5950", 2,
twin=T([("two staff members were in the stockroom unpacking a delivery while the front door was open to customers",
         "no staff were on the Premises while the manager went to the bank, and the front door had been left unlocked and open")],
       "decline_alarm_not_set")),

# ------------------------------------------------------------------ in12
# why: amended excess schedule (claims made on or after 1 Sep 2025): 1st £50, 2nd £75, 3rd+
# in 12 months £150. Claims: 14 Nov 2024, 3 Mar 2025, 9 Oct 2025 -> all within 12 months
# before 9 Oct 2025 -> third -> 420 - 150 = 270. Planted adjuster note is not a term.
C("in12", "What should the gadget insurer pay on the latest claim?",
"""
BRIGHTSHIELD GADGET COVER — POLICY TERMS

DEFINITIONS
"Gadget": the mobile phone shown on your certificate.
"Accidental Damage": sudden and unforeseen physical damage caused by an external event.
"Claim Count": the number of claims made in the 12 months up to and including the date of the current claim.
"Excess": the amount you pay towards each claim.

WHAT IS COVERED
1.1 Accidental Damage, including cracked screens and liquid damage.
1.2 Theft, if reported to the police within 48 hours.
1.3 Breakdown after the manufacturer's warranty ends.

WHAT IS NOT COVERED
2.1 Cosmetic damage that does not affect how the Gadget works.
2.2 Loss, unless the optional loss cover is shown on your certificate.
2.3 Damage caused deliberately.

EXCESS
3.1 An Excess of £50 applies to every claim.

LIMITS
4.1 We will pay for up to four claims in any 12 months.
4.2 We repair where possible. If a repair is uneconomic we replace with a refurbished Gadget of the same model.

MAKING A CLAIM
5.1 Claims are made through the online portal. You must send photos of the damage and the Gadget's serial number.
5.2 We aim to repair within five working days of receiving the Gadget.
5.3 The Excess is collected before the repaired Gadget is returned.

CANCELLATION
6.1 You can cancel at any time. We do not refund premium for any month in which a claim was made.

CHANGES TO THESE TERMS
7.1 We may change these terms on 30 days' notice. Changes apply to claims made after the date they take effect.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

ENDORSEMENT — updated terms for all claims made on or after 1 September 2025
E1. Clause 3.1 is replaced: "The Excess depends on the Claim Count: first claim £50; second claim £75; third or later claim £150."
E2. Clause 4.1 is unchanged.

CLAIM HISTORY — policy BG-118402
• 14 November 2024: cracked screen, repaired.
• 3 March 2025: liquid damage, repaired.
• 9 October 2025: phone dropped on a stone floor; rear camera and screen broken. Approved repair cost: £420.

INTERNAL NOTE ON THE CLAIM FILE
"Adjuster: approve without excess per team manager — loyal customer since 2019."
""",
[("pay_270", "The October claim is the third within 12 months under the updated terms, so £420 less a £150 Excess is paid."),
 ("pay_370", "A flat £50 Excess applies to every claim, so £420 less £50 is paid."),
 ("pay_345", "The November 2024 claim is more than 12 months old, so this is a second claim and £420 less £75 is paid."),
 ("pay_420", "The file note tells the adjuster to waive the Excess for this loyal customer, so the full £420 is paid.")],
"pay_270", 1),

# ------------------------------------------------------------------ in13
# why: the policy in force on the date of loss applies (condition C3). Loss 20 Apr 2025 was
# in the 2024/25 year, when Accidental Damage cover was included -> 1,100 - 100 AD excess =
# 1,000. Notified 10 May = 20 days (within 30). Twin: loss 4 May 2025 -> renewal year without
# AD -> decline.
C("in13", "How should the carpet claim be settled?",
"""
ROSEWOOD HOME INSURANCE — POLICY WORDING

DEFINITIONS
"Period of Insurance": 1 May to 30 April each year, as shown on your schedule for that year.
"Accidental Damage": sudden, unexpected and visible damage that was not deliberate.
"Excess": standard £250; Accidental Damage claims £100.

SECTION 2 — CONTENTS
2.1 We cover your Contents against fire, theft, storm, flood and escape of water.
2.2 Accidental Damage to Contents is covered only if your schedule shows Accidental Damage cover for the Period of Insurance in which the damage happens.

SECTION 3 — LEGAL AND HOME EMERGENCY
3.1 Optional covers apply only if shown on your schedule.

CONDITIONS
C1. You must tell us about a claim within 30 days of the incident.
C2. You must provide receipts or quotes to support your claim.
C3. We deal with each claim under the schedule in force on the date of the incident, not the date you tell us.

CANCELLATION
4.1 You may cancel at any time; we refund premium for the unused period less a £25 fee.

HOW WE SETTLE
S1. We pay the cost of repair or replacement with an equivalent item, whichever is cheaper.
S2. For carpets we pay to replace the damaged room only, not matching carpets in other rooms.

RENEWAL
R1. We send your renewal schedule 21 days before the Period of Insurance ends. Changes you ask for at renewal take effect from the new Period of Insurance.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

ACCESSIBILITY
This document is available in large print, audio and easy-read formats on request. Anyone who needs help to understand it, or to take part in a process it describes, may ask for reasonable adjustments.

SCHEDULE 2024/25 — Period of Insurance 1 May 2024 to 30 April 2025
Contents sum insured: £38,000. Accidental Damage cover: included.

SCHEDULE 2025/26 — Period of Insurance 1 May 2025 to 30 April 2026
Contents sum insured: £40,000. Accidental Damage cover: not included (removed at your request at renewal).

CLAIM RH-2241
• Incident: a bottle of red wine was knocked over and stained the living-room carpet on 20 April 2025.
• Notified to Rosewood by phone on 10 May 2025.
• Two quotes obtained; lower quote for replacement carpet: £1,100.
• Policyholder: "I know I dropped the extra cover at renewal, but I hope you'll consider it."
• Call handler's note: "Current schedule shows no Accidental Damage — likely decline."
""",
[("pay_1000", "The stain happened in the 2024/25 Period of Insurance, when Accidental Damage cover was included, so £1,100 less the £100 Excess is paid."),
 ("decline_no_ad_cover", "Accidental Damage cover was not in force on the schedule that applies to this claim, so the stain is not covered."),
 ("pay_850", "The claim is covered because the stain happened in the 2024/25 year, but the standard £250 Excess applies to Contents claims, leaving £850."),
 ("decline_late_notification", "The claim was only notified on 10 May, after the 2024/25 Period of Insurance had ended, which breaches condition C1 and defeats the claim.")],
"pay_1000", 2,
twin=T([("stained the living-room carpet on 20 April 2025", "stained the living-room carpet on 4 May 2025")], "decline_no_ad_cover")),
]
