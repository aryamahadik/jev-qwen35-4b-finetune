"""reason_c / insurance claims handling (Harrowfield Mutual, Stonebridge General,
Quayside Pet Cover, Arlow Life & Disability, Northfen Dental Plan)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ cl01
# why: laptop 1,900 (no limit); ring is a valuable not on the schedule -> capped at
# 1,500; bicycle locked -> covered 700. 1,900 + 1,500 + 700 = 4,100 - excess 250 = 3,850.
# Twin: ring specified at 2,600 -> 1,900 + 2,600 + 700 = 5,200 - 250 = 4,950.
C("cl01", "What should Harrowfield pay on this theft claim?",
"""
Harrowfield Mutual — Home Contents policy wording (extract)

Section 3 Theft. We cover theft following forced entry, less the policy excess.
Limits:
 3.1 Valuables (jewellery, watches, precious metals): $1,500 per item unless the item is listed on the schedule as a specified valuable, in which case its specified value applies.
 3.2 Bicycles: covered only if locked to a fixed object or kept in a locked building.
 3.3 Cash: $300 in total.
Excess: $250 per claim.
Section 7 Legal expenses — not relevant to theft claims.

Claim HM-66230
Insured: Colette and Bram Visser. Forced entry through rear door on 2 September 2026, police reference BR/26/40187.
Items stolen (agreed replacement values):
 - laptop: $1,900
 - diamond engagement ring: $2,600
 - bicycle, kept in a locked garden shed that was also forced: $700
Specified valuables on schedule: none.
""",
[("$3,100.00", "three thousand one hundred dollars."), ("$3,600.00", "three thousand six hundred dollars."),
 ("$3,850.00", "three thousand eight hundred and fifty dollars."), ("$4,100.00", "four thousand one hundred dollars."),
 ("$4,950.00", "four thousand nine hundred and fifty dollars."), ("$5,200.00", "five thousand two hundred dollars.")],
"$3,850.00", 3,
twin=T([("Specified valuables on schedule: none.", "Specified valuables on schedule: diamond engagement ring, $2,600.")], "$4,950.00")),

# ------------------------------------------------------------------ cl02
# why: premium due 1 Aug; grace ends 31 Aug (30 days after due). Loss 20 Aug is in
# the grace period and premium was paid 25 Aug (within grace) -> covered -> yes.
# Twin: paid 3 Sep -> after grace -> policy lapsed from the due date -> no.
Y("cl02", "Is the loss covered despite the late premium?",
"""
Stonebridge General — Monthly premium terms (commercial vehicles)

a) Each monthly premium is due on the 1st of the month.
b) A grace period runs until 30 days after the due date. Cover continues during the grace period.
c) If the premium is paid within the grace period, a loss that occurred during the grace period is covered.
d) If the premium is not paid by the end of the grace period, the policy lapses with effect from the due date, and no loss after the due date is covered.
e) Reinstatement after lapse requires a new application.

File note, claim SG-30914
Policyholder: Denholm Couriers (van registration DC24 KLM).
August premium: due 1 August 2026; paid 25 August 2026.
Loss: van rear-ended while parked, 20 August 2026; reported 21 August 2026.
Underwriter query: "Premium was late — do we have cover for this one?"
""",
[("Grace period", "the 30 days after a premium due date, during which cover continues."),
 ("Lapse", "cancellation of cover back to the due date when the premium is not paid by the end of the grace period.")],
1, 2,
twin=T([("paid 25 August 2026", "paid 3 September 2026")], 0)),

# ------------------------------------------------------------------ cl03
# why: gastroenteritis = illness -> 14-day waiting period from start 1 Sep; day 1 = 1 Sep
# so waiting period covers 1-14 Sep; onset 18 Sep is after -> pay less excess.
# Ear infection history irrelevant (different condition). Twin: onset 12 Sep -> inside
# waiting period -> decline.
C("cl03", "What decision should the pet claims handler make?",
"""
Quayside Pet Cover — Claims handbook, section 2

2.1 Waiting periods run from the policy start date (day 1 = start date):
  - accidents: 2 days;
  - illnesses: 14 days;
  - cruciate ligament conditions: 180 days.
  Conditions whose first signs appear within the waiting period are never covered.
2.2 Pre-existing conditions: any condition with signs before the policy start date is excluded.
2.3 Covered claims are paid less the $99 excess.
2.4 If the vet history for the 12 months before start has not been received, request it before deciding.

Claim QP-11820
Pet: Juniper, 4-year-old spaniel. Policy start: 1 September 2026.
Vet history (Maple Street Vets, Aug 2025 - Aug 2026): received; one ear infection, treated March 2026, resolved.
Claim: vomiting and diarrhoea, first signs 18 September 2026. Vet diagnosis: gastroenteritis (illness). Invoice $412.
""",
[("pay less excess", "the claim is covered and paid minus the $99 excess."),
 ("decline — waiting period", "first signs appeared within the waiting period."),
 ("decline — pre-existing condition", "the condition showed signs before the policy started."),
 ("request vet history", "the required vet history is missing."),
 ("refer to senior handler", "the handbook does not settle the claim.")],
"pay less excess", 2,
twin=T([("first signs 18 September 2026", "first signs 12 September 2026")], "decline — waiting period")),

# ------------------------------------------------------------------ cl04
# why: $3,900 -> Standard adjuster band, but two red flags -> SIU overrides.
# Flag 1: policy incepted 20 days before loss (< 30). Flag 2: reported 16 days after
# loss (> 14). Cash purchase has a receipt -> not a flag. Twin: reported 3 days after ->
# one flag only -> Standard Adjuster.
C("cl04", "Which claims unit should this claim be assigned to?",
"""
Harrowfield Mutual — Claims triage rules

Step 1 (check first): count the red flags below. Two or more red flags -> Special Investigations Unit (SIU).
  RF1 policy incepted fewer than 30 days before the loss;
  RF2 loss reported more than 14 days after it happened;
  RF3 high-value items bought in cash with no receipt;
  RF4 claimant changed address within 30 days before the loss.
Step 2 (otherwise, by estimated value):
  up to $2,500 with no injury -> Fast Track;
  $2,500.01 to $25,000 -> Standard Adjuster;
  over $25,000 -> Major Loss Unit.
Any claim involving bodily injury -> Injury Claims team (after Step 1).

Claim HM-67104
Policy incepted: 14 August 2026. Loss: accidental damage to a TV and sound system, 3 September 2026.
Reported: 19 September 2026.
Estimate: $3,900. Items bought 2025 for cash; shop receipts supplied.
Claimant address: unchanged since 2019. No injuries.
""",
[("Fast Track", "small claims without injury, settled on documents."),
 ("Standard Adjuster", "mid-value claims handled by an adjuster."),
 ("Major Loss Unit", "claims above $25,000."),
 ("Special Investigations Unit", "claims with two or more red flags."),
 ("Injury Claims", "claims involving bodily injury."),
 ("none of these", "no unit fits.")],
"Special Investigations Unit", 2,
twin=T([("Reported: 19 September 2026.", "Reported: 6 September 2026.")], "Standard Adjuster")),

# ------------------------------------------------------------------ cl05
# why: cancellation reason = work commitments -> listed exclusion -> no.
# Twin: made redundant (listed insured reason) -> yes.
Y("cl05", "Is this trip cancellation covered?",
"""
Stonebridge General — Travel policy, section B (cancellation)

We pay irrecoverable travel costs if you have to cancel your trip because of one of these insured reasons:
 B1 death, serious injury or illness of you, a travelling companion or a close relative;
 B2 you are called for jury service or as a witness;
 B3 you are made redundant (with at least 2 years' service);
 B4 your home is made uninhabitable by fire, flood or burglary within 7 days before departure.
We do not pay for cancellation because of: not wanting to travel, financial circumstances (other than B3), or work commitments or being refused leave by your employer.

Claim SG-T-4471
Insured: Mireille Honoré. Trip: Castaldo Islands, 14-24 October 2026. Irrecoverable cost: $2,180.
Cancelled on: 22 September 2026.
Reason given: "My company moved the launch of our new product to 16 October and my director said I have to be there. I've been with the company 6 years."
""",
[("Insured reason", "one of the reasons B1-B4 listed in the policy."),
 ("Excluded reason", "a reason the policy says it does not pay for.")],
0, 2,
twin=T([("\"My company moved the launch of our new product to 16 October and my director said I have to be there. I've been with the company 6 years.\"",
         "\"My company told me on 21 September that my role is redundant. I've been with the company 6 years.\"")], 1)),

# ------------------------------------------------------------------ cl06
# why: repair 8,900 / market value 12,000 = 74.2% > 70% -> total loss; pay market value
# less excess 500 = 11,500 (owner not retaining salvage). Twin: repair 8,100 = 67.5% ->
# repair; pay 8,100 - 500 = 7,600.
C("cl06", "How should this motor claim be settled?",
"""
Stonebridge General — Motor settlement guide

1. Total loss: if the repair estimate is more than 70% of the vehicle's pre-accident market value, the vehicle is a total loss. We pay the market value less the excess. If the owner keeps the wreck, we also deduct the salvage value.
2. Otherwise we authorise the repair and pay the repair cost less the excess.
3. Excess: $500 (comprehensive, driver over 25).
4. Hire car: up to 14 days while the claim is open (paid separately).

Claim SG-M-2208
Vehicle: 2021 Aurel Sportline, owner Hektor Brandt (age 41).
Pre-accident market value (valuation service): $12,000.
Repair estimate (approved repairer): $8,900.
Salvage value: $1,800. Owner's choice: does not want to keep the vehicle.
""",
[("repair — pay $7,600", "authorise repair, pay repair cost less excess ($7,600)."),
 ("repair — pay $8,400", "authorise repair, pay repair cost less excess ($8,400)."),
 ("total loss — pay $9,700", "total loss, owner keeps the wreck: market value less excess and salvage."),
 ("total loss — pay $11,500", "total loss: market value less excess."),
 ("total loss — pay $12,000", "total loss: full market value."),
 ("refer to engineer", "the file lacks a valuation or repair estimate.")],
"total loss — pay $11,500", 3,
twin=T([("Repair estimate (approved repairer): $8,900.", "Repair estimate (approved repairer): $8,100.")], "repair — pay $7,600")),

# ------------------------------------------------------------------ cl07
# why: 60-day notification: loss 4 Jul; 4 Jul -> 4 Aug 31 days, -> 4 Sep 31, +1 = 63
# days on 5 Sep -> late. No hospitalisation. -> no.
# Twin: loss 10 Jul -> 21 (to 31 Jul) + 31 (Aug) + 5 = 57 days -> in time -> yes.
Y("cl07", "Was this claim notified within the policy time limit?",
"""
Harrowfield Mutual — Landlord policy, general condition 4

4.1 You must tell us about any event that may lead to a claim within 60 days of the date of the event. Days are counted from the day after the event.
4.2 If you were in hospital during that period, the 60 days are extended by the number of days you were in hospital.
4.3 Late notification allows us to decline the claim.
4.4 Rent guarantee claims have their own notification rule (condition 9).

First notification of loss FNOL-50912
Insured landlord: Yusuf Kaya. Property: 14 Mill Lane, Ashcombe.
Event: tenant reported a ceiling collapse after a slow leak from the flat above, 4 July 2026.
Notified to Harrowfield: 5 September 2026 by phone.
Hospital stays in 2026: none.
""",
[("Notification period", "60 days counted from the day after the event, extended by any days in hospital."),
 ("Late notification", "notice given after the notification period ends.")],
0, 2,
twin=T([("after a slow leak from the flat above, 4 July 2026.", "after a slow leak from the flat above, 10 July 2026.")], 1)),

# ------------------------------------------------------------------ cl08
# why: crown = major -> 50%; deductible $50 not yet met -> (1,200 - 50) x 0.5 = 575.
# Annual max 1,500, used 1,120 -> 380 left -> pay 380.
# Twin: used 620 -> 880 left -> pay 575.
C("cl08", "How much does the plan pay for this procedure?",
"""
Northfen Dental Plan — Summary of benefits (individual plan)

Coinsurance: preventive (cleanings, check-ups, X-rays) 100%; basic (fillings, extractions) 80%; major (crowns, bridges, dentures) 50%.
Deductible: $50 per calendar year, applies to basic and major services only, and is taken off the fee before coinsurance.
Annual maximum: $1,500 of plan payments per calendar year; the plan never pays beyond what remains.
Orthodontics: separate lifetime maximum (not relevant here).

Claim ND-21077
Member: Sunniva Hart. Date of service: 22 September 2026.
Procedure: porcelain crown, lower left molar. Fee: $1,200.
Deductible met in 2026: no (this is the first basic or major service this year).
Plan payments already made in 2026: $1,120 (cleanings and a root-canal referral benefit).
""",
[("$0.00", "nothing is payable."), ("$380.00", "three hundred and eighty dollars."),
 ("$520.00", "five hundred and twenty dollars."), ("$575.00", "five hundred and seventy-five dollars."),
 ("$600.00", "six hundred dollars."), ("$1,150.00", "one thousand one hundred and fifty dollars.")],
"$380.00", 3,
twin=T([("Plan payments already made in 2026: $1,120", "Plan payments already made in 2026: $620")], "$575.00")),

# ------------------------------------------------------------------ cl09
# why: disability began 10 Jun = day 1. June 10-30 = 21 days, July -> 52, Aug -> 83,
# Sep 7 = day 90. Benefit payable from 8 Sep. 5 Sep is not payable -> no.
# Twin: began 1 Jun: June 30 days, July -> 61, Aug 29 = day 90 -> payable from 30 Aug ->
# 5 Sep payable -> yes.
Y("cl09", "Is a disability benefit payable for 5 September 2026?",
"""
Arlow Life & Disability — Group income protection, benefit rules

- Elimination period: 90 consecutive days of disability. The first day of disability is day 1.
- Benefit is payable from the day after the elimination period ends, at 60% of pre-disability salary.
- If the member returns to work for 5 days or fewer during the elimination period, those days are ignored and the period continues.
- Partial return-to-work benefits are covered in rule 7.

Claim AL-D-8843
Member: Graham Ostby, warehouse supervisor, employer Keelan Logistics.
First day of disability: 10 June 2026 (spinal surgery complication).
Continuous disability since then; no return to work.
Employer asks whether benefit covers the pay period ending 5 September 2026, specifically whether 5 September itself is a benefit day.
""",
[("Elimination period", "90 consecutive days of disability, with the first day of disability as day 1."),
 ("Benefit day", "any day of disability after the elimination period ends.")],
0, 3,
twin=T([("First day of disability: 10 June 2026", "First day of disability: 1 June 2026")], 1)),

# ------------------------------------------------------------------ cl10
# why: a customer (member of the public) slipped in the shop -> General Liability
# (public liability). Twin: an employee slipped at work -> Employers' Liability.
C("cl10", "Under which section of the business policy should this claim be registered?",
"""
Stonebridge General — Retail Business Combined policy, sections

A Property: damage to buildings, stock and contents.
B Business Interruption: lost gross profit after insured property damage.
C General (Public) Liability: injury to members of the public or damage to their property caused by the business's activities or premises.
D Product Liability: injury or damage caused by products the business sold, after they leave the premises.
E Employers' Liability: injury or illness suffered by the business's own employees in the course of their work.
F Cyber: data breaches and systems extortion.

Incident report — Florin's Delicatessen, 26 September 2026
At 11:40 a customer, Mrs Adaeze Bello, slipped on olive oil spilled from a broken bottle in aisle 2 and fractured her wrist. The spill had been reported by another customer about ten minutes earlier; no warning sign was placed. An ambulance took her to Harwell General. The broken bottle was from our own shelf stock.
""",
[("A Property", "damage to the insured's own property."),
 ("B Business Interruption", "lost profit following insured damage."),
 ("C General Liability", "injury or damage to members of the public from premises or activities."),
 ("D Product Liability", "harm caused by sold products after they leave the premises."),
 ("E Employers' Liability", "injury or illness of the insured's employees at work."),
 ("F Cyber", "data and systems incidents.")],
"C General Liability", 2,
twin=T([("a customer, Mrs Adaeze Bello, slipped", "our shop assistant, Adaeze Bello, slipped while restocking")], "E Employers' Liability")),

# ------------------------------------------------------------------ cl11
# why: water damage: the dated, signed endorsement (1 Mar 2026) overrides the schedule
# -> water excess $2,500; broker email has no effect. 7,200 - 2,500 = $4,700.
# Twin: kitchen fire -> endorsement is for water only -> schedule excess $1,000 -> $6,200.
C("cl11", "What amount should be paid on this claim?",
"""
Harrowfield Mutual — Commercial property file, Lanterne Bakery Ltd

Document hierarchy (policy wording, clause 1.3): a signed endorsement overrides the schedule for the matters it covers; a later signed endorsement overrides an earlier one. Quotes, drafts and emails do not change the policy.

On file:
 - Schedule (issued 1 January 2026): standard excess $1,000 for all claims.
 - Endorsement E1 (signed, dated 1 March 2026): excess for escape-of-water claims is $2,500. All other excesses unchanged.
 - Email from broker Pilar Moss, 20 March 2026: "I've asked them to put the water excess back to $500, should be sorted."
 - No further endorsements.

Claim HM-C-3090
Loss date: 11 September 2026. Cause: burst supply pipe under the proving room floor (escape of water). Agreed loss: $7,200.
""",
[("$3,700.00", "three thousand seven hundred dollars."), ("$4,700.00", "four thousand seven hundred dollars."), ("$6,200.00", "six thousand two hundred dollars."),
 ("$6,700.00", "six thousand seven hundred dollars."), ("$7,200.00", "seven thousand two hundred dollars.")],
"$4,700.00", 3,
twin=T([("Cause: burst supply pipe under the proving room floor (escape of water).", "Cause: fire in the fryer extraction duct (fire and smoke damage).")], "$6,200.00")),

# ------------------------------------------------------------------ cl12
# why: 300,000 / 380,000 = 78.9% < 85% -> average applies -> yes.
# Twin: replacement 340,000 -> 88.2% >= 85% -> no reduction -> no.
Y("cl12", "Will the average clause reduce this payout?",
"""
Stonebridge General — Buildings policy, condition 11 (average)

If, at the time of the loss, the sum insured is less than 85% of the full rebuilding cost of the building, we will pay only the proportion of the loss that the sum insured bears to the rebuilding cost. If the sum insured is 85% or more of the rebuilding cost, the average clause does not apply.
Index-linking: the sum insured is increased each renewal in line with the building-cost index (already reflected below).

Claim SG-B-7415
Insured: Weir Cottage Holdings. Loss: storm damage to roof and gable, 27 August 2026, agreed at $46,000.
Sum insured at the loss date: $300,000.
Rebuilding cost (loss adjuster's desktop valuation at the loss date): $380,000.
""",
[("Average clause", "a proportional reduction when the sum insured is below 85% of the rebuilding cost."),
 ("Rebuilding cost", "the full cost of rebuilding the property at the date of the loss.")],
1, 2,
twin=T([("at the loss date): $380,000", "at the loss date): $340,000")], 0)),

# ------------------------------------------------------------------ cl13
# why: SI 300,000 / value 400,000 = 75% < 85% -> average; 40,000 x 0.75 = 30,000, then
# deduct excess 1,000 -> 29,000. (Excess-first would give 29,250 - wrong order.)
# Twin: value 340,000 -> 88.2% -> no average -> 40,000 - 1,000 = 39,000.
C("cl13", "What is the settlement amount for this claim?",
"""
Harrowfield Mutual — Commercial contents, settlement steps

1. Agree the loss amount.
2. Under-insurance: if the sum insured is below 85% of the replacement value of all contents at the time of loss, multiply the loss by (sum insured / replacement value).
3. Deduct the excess of $1,000 from the result of step 2.
4. Payments above $50,000 need a second sign-off (not needed here).

Claim HM-C-4122 — Pellow Print Studio
Loss: accidental sprinkler discharge damaged presses and paper stock, agreed loss $40,000.
Contents sum insured: $300,000.
Replacement value of all contents at the time of loss (adjuster's inventory): $400,000.
""",
[("$29,000.00", "twenty-nine thousand dollars."), ("$29,250.00", "twenty-nine thousand two hundred and fifty dollars."),
 ("$30,000.00", "thirty thousand dollars."), ("$39,000.00", "thirty-nine thousand dollars."),
 ("$40,000.00", "forty thousand dollars.")],
"$29,000.00", 3,
twin=T([("(adjuster's inventory): $400,000", "(adjuster's inventory): $340,000")], "$39,000.00")),

# ------------------------------------------------------------------ cl14
# why: protected NCD allows up to 2 at-fault claims in any 5-year period without loss.
# At-fault claims in the 5 years to renewal: 2021 falls outside (renewal Nov 2026 ->
# window from Nov 2021; claim Feb 2021 out), Mar 2024 and this Sep 2026 -> 2 -> keeps
# full NCD -> yes. Twin: extra at-fault claim Jan 2023 -> 3 -> loses -> no.
Y("cl14", "Does the customer keep the full no-claims discount at renewal?",
"""
Stonebridge General — No-claims discount (NCD) rules, private car

- Each at-fault claim normally reduces the NCD by 2 years at the next renewal.
- Protected NCD: the NCD stays in full if there have been no more than 2 at-fault claims in the 5 years before the renewal date. A third at-fault claim in that period removes the protection for that renewal.
- Claims for windscreen only, or where we recover all our costs from another party, are not at-fault claims.

Customer file — Tamsin Ellery, renewal date 12 November 2026, NCD 9 years, protected.
Claims history:
 - February 2021: at-fault (reversed into a bollard).
 - March 2024: at-fault (rear-ended another car at lights).
 - June 2025: windscreen chip repair.
 - September 2026: at-fault (scraped a parked van).
""",
[("At-fault claim", "a claim where costs are not fully recovered from another party, excluding windscreen-only claims."),
 ("Protected NCD", "full NCD is kept if there are no more than 2 at-fault claims in the 5 years before renewal.")],
1, 3,
twin=T([(" - June 2025: windscreen chip repair.", " - June 2025: at-fault (clipped a gatepost).")], 0)),

# ------------------------------------------------------------------ cl15
# why: 8 weeks = 56 days. Complaint 3 Jul + 56 = 28 Aug (Jul 3 + 28 = Jul 31, + 28 =
# Aug 28). Today 2 Sep, no final response -> may refer to the ombudsman now.
# Twin: complaint 10 Jul + 56 = 4 Sep -> on 2 Sep still inside -> wait.
C("cl15", "What is the customer's correct next step on 2 September 2026?",
"""
Arlow Life & Disability — Complaints procedure (customer leaflet)

- We acknowledge complaints within 5 business days.
- We send a final response within 8 weeks (56 calendar days) of receiving the complaint.
- If you have not had a final response after 8 weeks, or you disagree with our final response, you may refer the complaint to the Insurance Ombudsman Service.
- You must refer it within 6 months of the date of our final response.
- Complaints about a financial adviser go to the adviser's firm first.

Customer message, 2 September 2026
"I complained on 3 July 2026 about how my critical illness claim was handled (reference CMP-7720). You acknowledged it on 7 July. I still haven't had any answer. What can I do now?"
Case system: no final response issued. No adviser involved.
""",
[("wait for the final response", "the 8-week period is still running; the customer should wait."),
 ("refer to the Insurance Ombudsman Service", "the customer may take the complaint to the ombudsman now."),
 ("complain to the adviser's firm", "the complaint is about an adviser."),
 ("time-barred", "the deadline for referring to the ombudsman has passed."),
 ("resubmit the complaint", "the complaint must be raised again under a new reference.")],
"refer to the Insurance Ombudsman Service", 2,
twin=T([("\"I complained on 3 July 2026", "\"I complained on 10 July 2026"), ("You acknowledged it on 7 July.", "You acknowledged it on 14 July.")],
       "wait for the final response")),

# ------------------------------------------------------------------ cl16
# why: wind lifted tiles (storm) and rain came through the storm-damaged roof -> storm
# cover, which expressly includes rain through storm damage -> covered -> yes.
# Twin: river overtopped its banks -> flood (rising water from a watercourse) -> excluded.
Y("cl16", "Is this damage covered under the policy?",
"""
Harrowfield Mutual — Home Buildings, perils (extract)

Storm: damage caused by wind of 55 mph or more, heavy rain, snow or hail. This includes rain entering the building through an opening made by the storm.
Flood — EXCLUDED on this policy (the property is in flood zone 3 and flood cover was declined at quotation): damage by water rising from, or escaping from, rivers, streams, lakes or the sea.
Wear and tear, and gradual damage: excluded.
Subsidence: covered, excess $1,000.

Claim HM-B-9981
Insured: Oona Radley, The Old Mill, Riverside Lane.
Date: 14 September 2026 (met service recorded gusts of 63 mph locally).
Loss adjuster: "Wind lifted a section of roof tiles over the rear bedroom. Rain came in through the opening overnight and brought down the bedroom ceiling. The nearby river stayed within its banks. Roof timbers otherwise sound, no sign of prior neglect."
""",
[("Storm damage", "wind, rain, snow or hail damage, including rain through an opening made by the storm."),
 ("Flood", "water rising from or escaping from rivers, streams, lakes or the sea; excluded on this policy.")],
1, 2,
twin=T([("\"Wind lifted a section of roof tiles over the rear bedroom. Rain came in through the opening overnight and brought down the bedroom ceiling. The nearby river stayed within its banks.",
         "\"The river behind the property overtopped its banks overnight and water rose 40 cm through the ground floor, soaking the walls and ruining the floor. The roof was intact.")], 0)),

# ------------------------------------------------------------------ cl17
# why: closed 10:00 Mon 7 Sep -> reopened 10:00 Mon 14 Sep = 168 h. Minus 72 h
# waiting = 96 h = 4 days x $1,200 = $4,800.
# Twin: reopened 10:00 Thu 10 Sep = 72 h -> nothing beyond the waiting period -> $0.
C("cl17", "How much business interruption should be paid?",
"""
Stonebridge General — Business interruption section (café and restaurant scheme)

- Cover follows insured damage that forces the premises to close.
- Time excess: the first 72 hours of closure are not covered.
- Loss of gross profit is paid at the agreed daily rate for each full 24 hours of closure after the time excess.
- Maximum indemnity period: 12 months.
- Losses caused by staff shortages or supplier failure are not covered.

Claim SG-BI-0558 — Bramble & Fig Café
Insured damage: kitchen fire (property claim SG-P-0557 accepted).
Closed: 10:00 Monday 7 September 2026.
Reopened: 10:00 Monday 14 September 2026.
Agreed daily gross profit rate: $1,200.
""",
[("$0.00", "nothing is payable."), ("$3,600.00", "three thousand six hundred dollars."),
 ("$4,800.00", "four thousand eight hundred dollars."), ("$6,000.00", "six thousand dollars."),
 ("$8,400.00", "eight thousand four hundred dollars.")],
"$4,800.00", 3,
twin=T([("Reopened: 10:00 Monday 14 September 2026.", "Reopened: 10:00 Thursday 10 September 2026.")], "$0.00")),

# ------------------------------------------------------------------ cl18
# why: bag stolen from a locked hotel-room safe, reported to police within 24 hours
# with a written report -> none of the listed exclusions applies -> none of these.
# Twin: bag left on a café chair while the insured went to the counter -> unattended
# in a public place -> "unattended property".
C("cl18", "Which exclusion, if any, applies to this baggage claim?",
"""
Stonebridge General — Travel policy, section D (personal belongings) — exclusions

We do not pay for:
 D1 unattended property: belongings left unattended in a public place or out of your sight and reach;
 D2 unreported theft: theft not reported to the police within 24 hours, or with no written police report;
 D3 valuables in checked luggage: jewellery, cameras or electronics in checked-in baggage;
 D4 wear and tear or gradual deterioration;
 D5 breakage of fragile items (glass, china) unless caused by fire or theft;
 D6 confiscation by customs or other officials;
 D7 cash above the $250 cash limit;
 D8 sports equipment while in use;
 D9 losses already paid by the airline or hotel.

Claim SG-T-5120
Insured: Yannick Albers. Hotel Castellan, Mirrow, room 412.
Loss: a camera and a watch taken from the room safe, which was locked; hotel security found the safe forced on 11 September 2026 at 18:30.
Police: report made at 20:10 the same day, written report ref MRW-26-8841 supplied.
Hotel's position: liability declined, nothing paid.
""",
[("D1 unattended property", "exclusion D1 applies."),
 ("D2 unreported theft", "exclusion D2 applies."),
 ("D3 valuables in checked luggage", "exclusion D3 applies."),
 ("D4 wear and tear", "exclusion D4 applies."),
 ("D5 breakage of fragile items", "exclusion D5 applies."),
 ("D6 confiscation", "exclusion D6 applies."),
 ("D7 cash above the limit", "exclusion D7 applies."),
 ("D8 sports equipment in use", "exclusion D8 applies."),
 ("D9 already paid by a third party", "exclusion D9 applies."),
 ("none of these", "no exclusion applies to the loss.")],
"none of these", 2,
twin=T([("Loss: a camera and a watch taken from the room safe, which was locked; hotel security found the safe forced on 11 September 2026 at 18:30.",
         "Loss: a camera and a watch in a shoulder bag taken from a café terrace on 11 September 2026 at 18:30, while the insured was queuing inside at the counter and the bag was on his outside chair."),
        ("Hotel Castellan, Mirrow, room 412.", "Staying at Hotel Castellan, Mirrow."),
        ("Hotel's position: liability declined, nothing paid.", "No payment from any third party.")],
       "D1 unattended property")),
]
