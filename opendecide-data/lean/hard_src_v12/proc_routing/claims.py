"""proc_routing / insurance claims allocation and settlement authority (Veridane Mutual, invented)."""
from _lib import C, T

GUIDE = """
VERIDANE MUTUAL — CLAIMS ALLOCATION GUIDE (rev. 7, extract)

Part A — Values
A1. "Claim value" means the total initial reserve: repair or replacement, hire vehicle, recovery and storage, and any third-party property damage. VAT is included. The policy excess is not deducted.

Part B — Routing by line and value
B1. Motor, value up to £5,000: Fast Track.
B2. Motor, value £5,000.01 to £50,000: Motor Handlers.
B3. Home and property, value up to £50,000: Property Handlers.
B4. Any line, value over £50,000: Large Loss Unit.
B5. Any claim involving bodily injury to a person: Injury Team, whatever the value.

Part C — Overrides, applied in this order before Part B
C1. Two or more indicators from the Fraud Indicator List: Special Investigations Unit (SIU). C1 overrides every other rule.
C2. Loss within 30 days of policy inception: Underwriting Review before any handler is assigned. Inception is the first start date of the policy with Veridane; renewal dates are not inception.

Fraud Indicator List
(1) notification more than 14 days after the loss; (2) policy address differs from the risk address given at claim; (3) a previous claim declined for non-disclosure; (4) cover increased within 60 days before the loss; (5) no proof of purchase for an item over £1,000; (6) the claimant's chosen repairer is on the Watch List.
"""

ITEMS = [
# ------------------------------------------------------------------ cl01
# why: value = repair 4,650 + hire 420 = 5,070 (excess not deducted) > 5,000 -> B2.
#      One indicator only (notified 20 days after) -> no SIU. "Shaken but unhurt"
#      is not bodily injury. twin hire 280 -> 4,930 -> Fast Track.
C("rt_cl01", "Which team should this motor claim be allocated to?",
GUIDE + """
New claim CLM-M-77120 (motor)
Policyholder: Ruth Adebayo; policy incepted 4 years ago; address matches.
Loss: rear-end collision at a roundabout on 3 March; notified 23 March.
Reserve lines: repair estimate £4,650 (incl. VAT); hire vehicle £420; recovery £0 (car was driven home).
Excess: £250.
Third party: the other driver said she was shaken but unhurt and drove away.
Repairer: Millbrook Motor Works (not on the Watch List).
""",
[("route_motor_handlers", "£4,650 repair plus £420 hire makes £5,070, above the £5,000 Fast Track limit, so B2 applies."),
 ("route_fast_track", "Repair and hire together come to less than £5,000, so the claim stays with Fast Track."),
 ("route_injury_team", "The other driver was shaken by the collision, which counts as bodily injury under B5."),
 ("refer_siu", "It was notified 20 days after the loss, which is a fraud indicator and enough for the SIU.")],
"route_motor_handlers", 2,
twin=T([("hire vehicle £420", "hire vehicle £280")], "route_fast_track")),

# ------------------------------------------------------------------ cl02
# why: cover raised 20 July, loss 1 Sept = 43 days (<60) -> indicator 4; laptop
#      £1,450 without receipt -> indicator 5. Two -> SIU. Phone change and
#      nervousness are not on the list. twin 20 June -> 73 days -> one indicator
#      -> home claim £2,300 -> Property Handlers.
C("rt_cl02", "Where should claim CLM-H-40318 be sent?",
GUIDE + """
New claim CLM-H-40318 (home contents)
Policyholder: Declan Farrow; policy incepted 3 years ago; policy address and risk address both 27 Linnet Close.
Loss: burglary on 1 September; notified 9 September.
Items: road bike £850 (receipt supplied); laptop £1,450 (no receipt; "bought for cash at a market stall").
Claim value: £2,300.
Cover history: contents sum insured raised from £25,000 to £40,000 on 20 July.
Call notes: claimant changed his contact phone number last week; handler felt he "sounded nervous".
""",
[("refer_siu", "Cover was raised 43 days before the loss and the £1,450 laptop has no receipt: two listed indicators, so C1 applies."),
 ("route_property_handlers", "Only one listed indicator is present, so the £2,300 home claim goes to Property Handlers under B3."),
 ("route_fast_track", "At £2,300 the claim is under £5,000, which is the Fast Track band."),
 ("route_underwriting_review", "The contents sum insured was raised from £25,000 to £40,000 shortly before the burglary, so Underwriting Review must look at the cover before a handler is assigned.")],
"refer_siu", 2,
twin=T([("on 20 July", "on 20 June")], "route_property_handlers")),

# ------------------------------------------------------------------ cl03
# why: new customer, inception 3 May, loss 28 May = 25 days -> C2 Underwriting
#      Review. twin: policy since 2021, 3 May is a renewal -> not inception ->
#      value 4,300 + third-party 5,500 = 9,800 -> Motor Handlers.
C("rt_cl03", "What is the correct allocation for this claim?",
GUIDE + """
New claim CLM-M-77388 (motor)
Policyholder: Jonas Ekberg
Policy: new customer; cover started 3 May
Loss: 28 May, reversed into a parked van; notified 29 May.
Reserve lines: own vehicle repair £4,300; third-party van damage £5,500; no hire.
Claim value: £9,800. No injuries. Addresses match; repairer not on the Watch List.
""",
[("route_underwriting_review", "The policy first started on 3 May, 25 days before the 28 May loss, so C2 sends it to Underwriting Review first."),
 ("route_motor_handlers", "The policy has run since 2021 and only the renewal date is recent, so the £9,800 motor claim goes to Motor Handlers."),
 ("route_fast_track", "The claimant's own repair is only £4,300, inside the Fast Track band."),
 ("refer_siu", "A claim made within weeks of the start of cover is itself a fraud indicator, and together with the third-party damage it is enough for the SIU.")],
"route_underwriting_review", 2,
twin=T([("Policy: new customer; cover started 3 May", "Policy: with Veridane since 2021; current annual period began 3 May")],
       "route_motor_handlers")),

# ------------------------------------------------------------------ cl04
# why: passenger's neck pain = bodily injury to a person -> B5 Injury Team at any
#      value. Missing dashcam is not an indicator. twin: passenger unhurt, dog
#      grazed (not a person) -> £3,200 motor -> Fast Track.
C("rt_cl04", "Which team handles claim CLM-M-77502?",
GUIDE + """
New claim CLM-M-77502 (motor)
Policyholder: Sinead Mallory; policy incepted 6 years ago.
Loss: 12 June, clipped a kerb avoiding a cyclist and hit a lamp post; notified 13 June.
Her passenger, Mr Doyle, reported neck pain the next day and saw his GP.
Reserve lines: repair £2,900; recovery £300. Claim value: £3,200.
Notes: the policyholder's dashcam memory card was full, so there is no footage. Addresses match.
""",
[("route_injury_team", "The passenger's neck pain is bodily injury to a person, and B5 sends any claim with bodily injury to the Injury Team whatever its value, so the £3,200 figure does not matter."),
 ("route_fast_track", "No person was hurt, and the £3,200 motor claim is within the Fast Track band."),
 ("route_motor_handlers", "Any injury, however slight, makes a claim too complex for Fast Track, so a £3,200 motor claim with an injury element moves up to Motor Handlers."),
 ("refer_siu", "The missing dashcam footage makes the claim suspicious enough for investigation.")],
"route_injury_team", 1,
twin=T([("Her passenger, Mr Doyle, reported neck pain the next day and saw his GP.",
         "Her passenger, Mr Doyle, was unhurt; her dog was grazed and saw a vet.")], "route_fast_track")),

# ------------------------------------------------------------------ cl05
# why: bulletin keys on NOTIFICATION date; notified 3 July (>= 1 July) -> property
#      threshold £35,000; £42,000 > 35,000 -> Large Loss. Adjuster's refit remark
#      is not a listed indicator. twin notified 29 June -> old £50,000 -> B3.
C("rt_cl05", "Under the guide and the bulletin, where should this claim go?",
GUIDE + """
Claims Bulletin 14 (issued 20 June)
From 1 July, for home and property claims notified on or after that date, the Large Loss threshold in B3/B4 is £35,000 instead of £50,000. Motor thresholds are unchanged.

New claim CLM-H-40502 (home buildings)
Policyholder: Anwen Pryce; policy incepted 8 years ago.
Loss: kitchen fire on 26 June; notified 3 July. Nobody was hurt.
Claim value: £42,000 (kitchen strip-out and refit, smoke cleaning, alternative accommodation).
Loss adjuster's remark: "Kitchen was refitted two years ago, so the quality is high. I would send this to SIU to be safe."
""",
[("route_large_loss", "It was notified on 3 July, after the bulletin's start, so the £35,000 threshold applies and £42,000 is above it."),
 ("route_property_handlers", "It was notified before 1 July, so the £50,000 threshold still applies and £42,000 is below it."),
 ("refer_siu", "The loss adjuster recommends SIU, and a recently refitted high-value kitchen destroyed by fire is the kind of pattern C1 exists for, so the claim should be investigated.")],
"route_large_loss", 2,
twin=T([("notified 3 July", "notified 29 June")], "route_property_handlers")),

# ------------------------------------------------------------------ cl06
# why: Ashcombe's DA suspended from 1 August; claim received 12 August -> no DA ->
#      Part B: motor £8,200 -> Motor Handlers. twin suspension from 1 September ->
#      DA still live on 12 August and £8,200 <= £10,000 -> return to broker.
C("rt_cl06", "How should claim CLM-M-77630 be routed?",
GUIDE + """
Delegated Authority (DA) scheme, section 4
Motor claims up to £10,000 received from brokers on the DA list are returned to the broker to settle under its own authority.

Email from the DA Manager, 25 July
"Ashcombe Partners' delegated authority is suspended from 1 August pending audit. Route their claims under Part B until further notice."

New claim CLM-M-77630 (motor), received from Ashcombe Partners on 12 August
Loss: 9 August, side-swipe in a car park. Claim value: £8,200. No injuries, no indicators.
""",
[("route_motor_handlers", "Ashcombe's delegated authority was suspended from 1 August, before this 12 August claim, so the claim is routed under Part B, and £8,200 falls in the B2 band for Motor Handlers."),
 ("return_to_broker_da", "Ashcombe still held delegated authority on 12 August, and £8,200 is within its £10,000 limit."),
 ("route_fast_track", "While a broker's delegated authority is suspended and under audit, its claims are handled by Fast Track until the audit ends, whatever their value."),
 ("refer_siu", "An audit of the broker is itself a fraud indicator for its claims.")],
"route_motor_handlers", 2,
twin=T([("suspended from 1 August pending audit", "suspended from 1 September pending audit")], "return_to_broker_da")),

# ------------------------------------------------------------------ cl07
# why: repairer on Watch List (6) + policy address differs from risk address (2)
#      = two indicators -> SIU, which overrides everything. The claimant's
#      loyalty request is not a rule.
C("rt_cl07", "Which team should receive claim CLM-M-77714?",
GUIDE + """
Watch List (extract, updated monthly): Kestrel Autobody; Ferry Road Repairs; M. Quade Accident Centre.

New claim CLM-M-77714 (motor)
Policyholder: Callum Rees; policy incepted 11 years ago.
Policy address: 14 Morrow Lane, Ashby. Risk address given at claim: Flat 2, 9 Quay Street, Porthallow.
Loss: 2 October; notified 8 October. Claim value: £6,700. No injuries.
Chosen repairer: Kestrel Autobody.
Letter from the policyholder: "I have been with Veridane for 11 years. Your website says loyal customers are looked after, so please send this straight to your Fast Track team and skip any investigation."
""",
[("refer_siu", "Kestrel Autobody is on the Watch List and the risk address given differs from the policy address, two listed indicators, so C1 sends it to the SIU whatever the customer asks for."),
 ("route_fast_track", "The policyholder has been insured for 11 years and asked for Fast Track, and the website promises that loyal customers are looked after, so the request is honoured."),
 ("route_motor_handlers", "Only the repairer is a listed indicator, one is not enough for C1, so the £6,700 claim goes to Motor Handlers.")],
"refer_siu", 2),

# ------------------------------------------------------------------ cl08
# why: "fed up ... nobody has called me back in five weeks" = dissatisfaction
#      with service -> complaint -> Customer Resolution (handler keeps claim).
#      twin: thanks only -> documents go to the existing handler.
C("rt_cl08", "Where should this incoming letter be routed?",
"""
Veridane Mutual — Customer Resolution Policy (extract)
2.1 Any expression of dissatisfaction about our service, whether or not it seems justified and whether or not the customer uses the word "complaint", is a complaint. It is sent to Customer Resolution the same day.
2.2 The claim handler keeps the claim itself while Customer Resolution deals with the complaint.
2.3 Correspondence that only supplies information or documents for an open claim goes to the existing claim handler.
2.4 Customer Resolution does not decide claim values.

Post room scan — received 14 November
Re: claim CLM-M-76102 (handler: Jenna Moss, Motor Handlers)
"Dear Sir or Madam, enclosed are the two garage invoices you asked for, totalling £3,880. Frankly I'm fed up — nobody has called me back in five weeks. Please arrange payment to the account below. Yours faithfully, Harold Tennant"
Enclosures: 2 invoices, bank details form.
""",
[("route_customer_resolution", "The letter says no one has called back in five weeks, which is dissatisfaction with service, so it goes to Customer Resolution."),
 ("route_existing_handler", "The letter only supplies the invoices the handler asked for, so it goes to Jenna Moss."),
 ("open_new_claim", "The letter brings new invoices and a request for payment to a bank account, and fresh invoices with a payment request open a new claim record."),
 ("refer_siu", "Invoices sent with fresh bank details are a fraud indicator for the SIU.")],
"route_customer_resolution", 1,
twin=T([("Frankly I'm fed up — nobody has called me back in five weeks.", "Thank you to Jenna for explaining so clearly what was needed.")],
       "route_existing_handler")),

# ------------------------------------------------------------------ cl09
# why: loss 2 Feb, notified 21 Feb = 19 days (>14) -> indicator 1; 2022 decline
#      for non-disclosure -> indicator 3. Two -> SIU overrides B4.
#      twin notified 11 Feb = 9 days -> one indicator -> £118,000 > 50,000 -> B4.
C("rt_cl09", "Which unit should handle claim CLM-H-40777?",
GUIDE + """
New claim CLM-H-40777 (home buildings)
Policyholder: Marcus Thorne; policy incepted 5 years ago; addresses match.
Loss: fire destroyed a detached garage and workshop on 2 February; notified 21 February.
Claim value: £118,000.
Claims history: 2022 claim for storm damage declined for non-disclosure of a prior subsidence repair.
Cover history: no changes in the last 12 months.
""",
[("refer_siu", "Notification 19 days after the loss and the earlier non-disclosure decline are two listed indicators, and C1 overrides the Large Loss rule."),
 ("route_large_loss", "Only one listed indicator is present, so C1 does not apply and a £118,000 claim goes to the Large Loss Unit."),
 ("route_property_handlers", "Home and property claims go to Property Handlers under B3."),
 ("route_underwriting_review", "A previous claim declined for non-disclosure means Underwriting Review must check the cover before a handler is assigned, and that check comes before Part B.")],
"refer_siu", 2,
twin=T([("notified 21 February", "notified 11 February")], "route_large_loss")),

# ------------------------------------------------------------------ cl10
# why: 23:10 Tuesday is outside 09:00-17:30 -> OFN logs for morning, unless home
#      uninhabitable. Power/heating work, family stays -> habitable -> log.
#      twin: power off as unsafe, family moved out -> D2 -> dispatch partner.
C("rt_cl10", "What should the overnight team do with this notification?",
"""
Veridane Mutual — Claims Allocation Guide, Section D (out of hours)
D1. Claims notified to the 24-hour line outside 09:00-17:30 Monday to Friday are logged by Overnight First Notification (OFN) and allocated the next working morning under Parts B and C.
D2. Exception: if the insured home is uninhabitable (no safe water, power or heating, or structurally unsafe), OFN dispatches the Emergency Response Partner immediately.
D3. OFN does not set reserves; the allocating team does.
Part B extract: B1 Motor up to £5,000: Fast Track. B3 Home and property up to £50,000: Property Handlers.

Call log — 24-hour line
Time: Tuesday 23:10
Caller: Kofi Mensah, policy HB-551023
"A pipe has burst in the loft. Water came through the kitchen ceiling and the plaster is sagging. I've turned the water off at the stopcock. Power and heating still work and the family are staying at home tonight."
OFN estimate noted for reference: under £5,000.
""",
[("log_for_morning_allocation", "The call came at 23:10, outside 09:00-17:30, and with power and heating working and the family at home the house is not uninhabitable, so OFN logs it for morning allocation."),
 ("dispatch_emergency_partner", "With the power off as unsafe and the family moved out, the home is uninhabitable under D2."),
 ("route_property_handlers", "It is an escape-of-water claim on a home policy, and B3 sends home and property claims up to £50,000 to Property Handlers whenever they are notified."),
 ("route_fast_track", "The estimate is under £5,000, which is the Fast Track band.")],
"log_for_morning_allocation", 1,
twin=T([("Power and heating still work and the family are staying at home tonight.",
         "The electrician says the wiring is now unsafe, so the power is off and the family have gone to a neighbour's.")],
       "dispatch_emergency_partner")),

# ------------------------------------------------------------------ cl11
# why: gadget rule uses the phone's own replacement value (£1,449 <= £1,500) ->
#      Tellsure. Accessories are not part of that test.
C("rt_cl11", "Who should handle this mobile phone claim?",
"""
Veridane Mutual — Gadget Cover Handling Note (extract)
G1. Mobile phone claims are handled by our partner Tellsure when the phone's own replacement value is £1,500 or less.
G2. Phones with a replacement value above £1,500, and all other gadgets, go to Property Handlers.
G3. Accessories claimed with a phone (cases, chargers, screen protectors) follow the phone and do not count towards the G1 value.
G4. Fraud Indicator List and SIU rule (Part C) apply to gadget claims as to any other claim.

New claim CLM-G-11873
Policyholder: Imani Clarke; policy incepted 2 years ago; addresses match.
Loss: phone dropped from a bridge into a river on 4 April; notified 5 April.
Items: phone, replacement value £1,449 (receipt supplied); leather case £60; screen protector £25.
Total claimed: £1,534.
""",
[("route_tellsure", "The phone's own replacement value is £1,449, within £1,500, and accessories do not count, so Tellsure handles it."),
 ("route_property_handlers", "Adding the case and screen protector, £1,449 + £60 + £25 = £1,534 is claimed, which is above £1,500, so G2 sends the claim to Property Handlers."),
 ("route_fast_track", "Any claim under £5,000 is Fast Track work."),
 ("refer_siu", "A phone lost in a river cannot be inspected, which is a fraud indicator.")],
"route_tellsure", 1),

# ------------------------------------------------------------------ cl12
# why: disclosed bereavement = vulnerability -> Section E Specialist Care, since
#      only one indicator (notified 17 days after loss). C1 needs two.
C("rt_cl12", "Where should claim CLM-H-40890 be allocated?",
GUIDE + """
Section E — vulnerable customers
Where a customer tells us about a vulnerability (recent bereavement, serious illness, financial hardship, limited capacity), the claim goes to the Specialist Care team, unless C1 applies.

New claim CLM-H-40890 (home buildings)
Policyholder: Edith Harrowby; policy incepted 19 years ago; policy address matches the risk address.
Loss: storm lifted roof tiles on 1 March; notified 18 March.
Claim value: £7,400.
Call note: "Mrs Harrowby apologised for calling late. Her husband died last month and she has only just found the damage in the back bedroom."
""",
[("route_specialist_care", "She has told us of a recent bereavement and only one fraud indicator applies, so Section E sends the claim to Specialist Care."),
 ("refer_siu", "Notification 17 days after the loss is a fraud indicator, so the claim goes to the SIU."),
 ("route_property_handlers", "It is a home buildings claim for storm damage worth £7,400, which sits in the B3 band, and Part B decides the handling team for home claims."),
 ("route_large_loss", "Storm claims are handled centrally by the Large Loss Unit.")],
"route_specialist_care", 1),

# ------------------------------------------------------------------ cl13
# why: total = 23,400 + 2,100 = 25,500 > H2 limit 25,000 -> Team Leader.
#      2023 schedule is superseded history. twin costs 1,100 -> 24,500 -> H2 own.
C("rt_cl13", "Who must approve this settlement?",
"""
Veridane Mutual — Settlement Authority Schedule (effective 1 January this year)
H1 handler: up to £10,000. H2 handler: up to £25,000. Team Leader: up to £75,000. Claims Manager: above £75,000.
The amount is the total payment: indemnity plus costs, fees and interest.
Previous schedule (2023, withdrawn): H2 handlers could settle up to £30,000.
Payment method: settlements are paid by bank transfer within five working days of approval. Payments to solicitors need the firm's verified bank details on file.
Audit: 5% of settlements approved by handlers are sampled each quarter by the Quality team.

Settlement proposal — claim CLM-M-75501
Handler: Kasia Nowak, grade H2
Indemnity agreed with third-party insurer: £23,400
Third-party solicitor's costs: £2,100
Interest: nil
Handler note: "Agreed after two rounds of negotiation. Ready to pay today."
""",
[("refer_team_leader", "£23,400 plus £2,100 costs is £25,500, above the £25,000 H2 limit, so a Team Leader must approve."),
 ("approve_within_handler_authority", "The total payment, indemnity and solicitor's costs together, stays within the £25,000 H2 limit in the current schedule, so Kasia can approve it herself as an H2 handler."),
 ("refer_claims_manager", "Any settlement that includes a claimant solicitor's costs has to be approved by the Claims Manager, whatever the size of the indemnity."),
 ("approve_under_2023_limit", "Kasia's grade has settled up to £30,000 since 2023, so the payment is within authority.")],
"refer_team_leader", 2,
twin=T([("Third-party solicitor's costs: £2,100", "Third-party solicitor's costs: £1,100")], "approve_within_handler_authority")),

# ------------------------------------------------------------------ cl14
# why: ex-gratia at any amount needs Claims Manager; H1 limit is irrelevant;
#      no complaint exists, so Customer Resolution does not decide it.
C("rt_cl14", "Who is the correct approver for this payment?",
"""
Veridane Mutual — Settlement Authority Schedule (extract)
H1 handler: up to £10,000. H2 handler: up to £25,000. Team Leader: up to £75,000. Claims Manager: above £75,000.
Note 3: Ex-gratia payments (payments made where the policy does not cover the loss) need Claims Manager approval at any amount.
Note 4: Compensation for an upheld complaint is decided by Customer Resolution.
Note 5: Payments are made by bank transfer; cheques only on request.

Payment request — claim CLM-H-39112 (declined: wear and tear, not covered)
Handler: Owen Rudd, grade H1
Proposed payment: £300 ex-gratia towards a new garden fence panel
Reason: "Customer of 22 years, declined claim, small gesture recommended by my team leader."
Customer contact since decline: one call asking about next steps; no complaint recorded.
""",
[("refer_claims_manager", "The £300 is ex-gratia because the wear-and-tear loss is not covered, and Note 3 requires Claims Manager approval for ex-gratia payments at any amount, whatever the handler's limit."),
 ("approve_within_handler_authority", "£300 is far below Owen's £10,000 H1 limit, and handlers approve any payment within their grade limit under the Settlement Authority Schedule."),
 ("refer_team_leader", "The team leader recommended the gesture, so the team leader signs it off."),
 ("route_customer_resolution", "Goodwill payments are complaint compensation, which Customer Resolution decides.")],
"refer_claims_manager", 1),
]
