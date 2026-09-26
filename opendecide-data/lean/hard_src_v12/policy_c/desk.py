"""policy_c / customer service desks (Fablight streaming, Quaystone Mobile & Broadband, Parcelwick couriers,
Corriemoor Credit Union, Tollbar Rail, Tarnside Energy)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ de01
# why: bought 3 days ago but 1 h 12 min watched (> 5 min) and no logged fault -> no refund.
# Twin: 3 min watched with logged stream failures -> full refund.
C("de01", "What should the Fablight agent do with the refund request?",
"""
Fablight — Digital Purchases and Rentals: Refund Rules (agent guide)
1. Full refund to the original payment method if the request is made within 14 days of purchase AND playback has not passed 5 minutes AND the title has not been downloaded.
2. Full refund, at any time within 14 days, if our playback logs show a verified technical fault (repeated "stream failed" errors) that stopped the customer watching.
3. If the customer reports a fault that is not shown in the logs, escalate to the Technical Team; do not refund yet.
4. Otherwise, no refund. Agents may not offer credit instead of a refund.

Chat transcript — ticket FL-230984, 23 September 2026
Customer (Ines Carvalho): "Hi, I bought 'The Salt Road' on Sunday for £13.99. Honestly I didn't like it at all, it was slow and nothing like the trailer. Can I get my money back?"
Agent tools — purchase: 20 September 2026, £13.99, HD purchase
Playback log: 1 h 12 min watched on the living-room TV; no errors logged
Downloads: none
""",
[("full refund", "a request that meets rule 1 or rule 2."),
 ("escalate to the Technical Team", "a reported fault that the logs do not show."),
 ("no refund", "the request meets none of rules 1–3."),
 ("offer account credit", "credit given in place of a refund.")],
"no refund", 1,
twin=T([("Honestly I didn't like it at all, it was slow and nothing like the trailer.", "It kept freezing and then saying the stream failed, so I gave up."),
        ("Playback log: 1 h 12 min watched on the living-room TV; no errors logged", "Playback log: 3 min watched on the living-room TV; 14 'stream failed' errors logged")],
       "full refund")),

# ------------------------------------------------------------------ de02
# why: DOB+postcode and last bill passed = 2 factors, but a SIM swap needs one of them to be the PIN or
# the one-time code; PIN failed, no email -> cannot process (0). Twin: PIN correct -> yes (1).
Y("de02", "May the agent process the SIM swap?",
"""
Quaystone Mobile — Identity Verification for Account Changes (agent script, section 3)
Verification factors (each counts once):
(a) the 4-digit account PIN;
(b) the amount of the last bill;
(c) date of birth AND postcode together;
(d) a one-time code sent to the registered email address.
Most account changes need any two passed factors. A SIM swap or port-out needs any two passed factors, at least one of which must be (a) or (d). Never tell the caller which factor failed.

Call log — account 07700 900 318, 24 September 2026, 19:42
Caller says her phone was stolen this afternoon and asks for a SIM swap to a new SIM she bought in store (SIM serial read out).
Checks:
– Account PIN: caller gave 4 digits — did not match.
– Last bill amount: £23.40 — matched.
– Date of birth and postcode: both matched.
– One-time email code: caller says she can't get into her email without her phone; not attempted.
Fraud markers on the account: none.
""",
[("Process the SIM swap", "two passed factors including the PIN or the one-time email code."),
 ("Do not process", "the SIM swap verification rule is not met.")],
0, 2,
twin=T([("– Account PIN: caller gave 4 digits — did not match.", "– Account PIN: caller gave 4 digits — matched.")], 1)),

# ------------------------------------------------------------------ de03
# why: claim on day 5 (within 14), ceramic vase is not excluded, Parcel Protection bought with declared
# value £120 -> pay declared value. Twin: no Parcel Protection -> standard £25 limit.
C("de03", "How should Parcelwick settle claim PW-C-55190?",
"""
Parcelwick — Damage and Loss Claims (customer service rules)
• Damage claims must be made within 14 days of delivery; loss claims within 28 days of the expected delivery date. Later claims are rejected.
• Standard cover: up to £25 per parcel.
• Parcel Protection (bought at checkout): up to the declared value, maximum £500.
• Excluded items (no payment under any cover): cash, gift cards, jewellery, live animals, perishable food.
• Evidence: photos of the item and the packaging are required for any damage claim.

Claim PW-C-55190
Sender: Hollin Ceramics (online shop). Item: hand-thrown ceramic vase.
Service: Parcelwick 48, with Parcel Protection bought at checkout; declared value £120.
Delivered: 14 September 2026. Claim made: 19 September 2026.
Evidence: 4 photos — vase broken in three pieces; box double-walled, two layers of bubble wrap, box undamaged except one crushed corner.
Customer message: "The vase cost £120 and it arrived in pieces."
""",
[("pay up to the declared value", "an in-time, evidenced claim for a non-excluded item with Parcel Protection."),
 ("pay up to the £25 standard limit", "an in-time, evidenced claim for a non-excluded item without Parcel Protection."),
 ("reject — claim too late", "the claim was made outside the time limit."),
 ("reject — excluded item", "the item is on the excluded list."),
 ("pause — request photos", "photos of the item and packaging are missing from a damage claim.")],
"pay up to the declared value", 2,
twin=T([("Service: Parcelwick 48, with Parcel Protection bought at checkout; declared value £120.",
         "Service: Parcelwick 48, standard cover only (Parcel Protection not bought).")],
       "pay up to the £25 standard limit")),

# ------------------------------------------------------------------ de04
# why: threshold = CPI 1.8 + 3.9 = 5.7%; rise 6.0% > 5.7 -> exit right; notice 5 Mar, request 28 Mar =
# 23 days <= 30 -> free exit (1). Twin: request 10 Apr = 36 days -> too late (0).
Y("de04", "Can Mr Obi leave his Quaystone contract without an early termination fee?",
"""
Quaystone Mobile — Price Change Terms, clause 9
9.1 Once a year we may raise your monthly price. If the rise is more than CPI + 3.9 percentage points, using the CPI figure published in the January before the rise, you may end your contract without an early termination fee.
9.2 To use this right you must tell us within 30 days of the date of our price-change notice.
9.3 Rises of CPI + 3.9 points or less do not give a right to leave free of charge.

Case QM-88104 — customer Chidi Obi, SIM-only 24-month plan (month 9 of 24)
Price-change notice sent: 5 March 2026 — monthly price rising from £20.00 to £21.20 (6.0%) from 1 April.
CPI figure published January 2026: 1.8%.
Customer contacted us: 28 March 2026 by web chat — "I want to leave, the price is going up too much."
Early termination fee that would otherwise apply: £165.
""",
[("Free exit", "a qualifying price rise and a request within 30 days of the notice."),
 ("Fee applies", "the rise does not qualify, or the request came too late.")],
1, 3,
twin=T([("Customer contacted us: 28 March 2026 by web chat", "Customer contacted us: 10 April 2026 by web chat")], 0)),

# ------------------------------------------------------------------ de05
# why: son lives in halls Sep-Jun, so not household; watching regularly, not travelling. Standard plan has
# 1 Extra Member slot free -> offer Extra Member. Twin: Basic plan has 0 slots -> upgrade required.
C("de05", "What should Fablight's Household Desk do about the Kowalski account?",
"""
Fablight — Household Sharing Rules
• An account is for one household: the people who live at the account's main address for most of the year.
• Household members may watch anywhere while travelling (short trips away from home).
• Anyone else who uses the account regularly must be added as an Extra Member (£4.99 a month). Extra Member slots: Premium 2, Standard 1, Basic 0.
• If the plan has no free Extra Member slot, the account holder must upgrade the plan before the person can be added.

Household Desk ticket FL-HH-4471
Account holder: Marta Kowalski — Standard plan; main address in Pellow. Extra Members: none.
System flag: a laptop signed in as profile "Jakub" has streamed from Ashcombe (140 miles away) on 64 days in the last 90 days.
Marta's reply to our email: "Jakub is my son. He lives in the university halls in Ashcombe from September to June and comes home in the summer. He's basically just travelling, isn't he?"
""",
[("no action — household member", "the viewer lives at the main address for most of the year."),
 ("no action — travelling", "a household member watching during short trips away."),
 ("offer an Extra Member slot", "a regular non-household viewer and a free Extra Member slot on the plan."),
 ("require a plan upgrade first", "a regular non-household viewer but no free Extra Member slot.")],
"offer an Extra Member slot", 2,
twin=T([("Account holder: Marta Kowalski — Standard plan", "Account holder: Marta Kowalski — Basic plan")], "require a plan upgrade first")),

# ------------------------------------------------------------------ de06
# why: 18+ parcel, recipient looks under 25, a student union card is not acceptable ID -> must not hand over (1).
# Twin: driving licence shows she is 23 -> may hand over (0).
Y("de06", "Must the driver refuse to hand over parcel PW-7730-K?",
"""
Parcelwick — Age-Verified Delivery (driver handbook, section 11)
11.1 Parcels labelled 18+ (knives and bladed items, alcohol) may only be handed to a person aged 18 or over.
11.2 If the recipient looks under 25, the driver must see photo ID. Acceptable ID: passport, photocard driving licence, or a PASS-hologram proof-of-age card. Student cards, bank cards and photos of ID on a phone are not acceptable.
11.3 If acceptable ID is not shown, the parcel must not be handed over, left with a neighbour or left in a safe place. It goes back to the depot.

Driver handheld note — Saturday 26 September 2026, 11:20, 4 Mill Row
Parcel PW-7730-K, label: 18+ — contents: kitchen knife set.
The woman who answered said she was the named recipient, Holly Dent, and looked about 20.
ID shown: a student union card with her photo and name.
She said: "I'm 23, honestly, my licence is at my boyfriend's."
""",
[("Refuse handover", "an 18+ parcel where the rules for handing it over are not met."),
 ("Hand over", "the recipient is shown to be 18 or over by the rules.")],
1, 2,
twin=T([("ID shown: a student union card with her photo and name.\nShe said: \"I'm 23, honestly, my licence is at my boyfriend's.\"",
         "ID shown: a photocard driving licence in her name, date of birth 2 March 2003.\nShe said: \"Sorry, I always get asked.\"")], 0)),

# ------------------------------------------------------------------ de07
# why: charged after a confirmed cancellation of a recurring membership -> cancelled recurring payment.
# Twin: member never signed up, card in wallet -> unauthorised transaction.
C("de07", "Which dispute reason code should the Corriemoor agent choose?",
"""
Corriemoor Credit Union — Card Dispute Reason Codes (choose one)
Agents must pick the code that matches the member's account of what happened and the evidence supplied.

Dispute form CCU-D-6620 — member Rhiannon Price, debit card ending 4471
Merchant: IronHouse Gym, Wexley
Transactions disputed: £34.99 on 1 September 2026; £34.99 on 1 October 2026.
Member's statement: "I cancelled my IronHouse membership on 1 August — I have their email confirming the cancellation 'effective 31 August'. They've taken two more monthly payments since. I've emailed them twice and they haven't replied."
Evidence attached: the IronHouse cancellation confirmation email dated 1 August 2026.
Earlier payments to IronHouse (Feb–Aug 2026): not disputed.
""",
[("unauthorised transaction", "the member did not make or authorise the payment."),
 ("goods or services not received", "the member paid but the goods or service never arrived."),
 ("not as described or defective", "what was received differs from what was sold or is faulty."),
 ("duplicate processing", "one purchase was charged more than once."),
 ("cancelled recurring payment", "a recurring payment taken after the member cancelled it with the merchant."),
 ("credit not processed", "the merchant agreed a refund but has not paid it.")],
"cancelled recurring payment", 2,
twin=T([("I cancelled my IronHouse membership on 1 August — I have their email confirming the cancellation 'effective 31 August'. They've taken two more monthly payments since. I've emailed them twice and they haven't replied.",
         "I have never been a member of IronHouse and never gave them my card details — my card has been in my wallet the whole time. I've never even been to Wexley."),
        ("Evidence attached: the IronHouse cancellation confirmation email dated 1 August 2026.\nEarlier payments to IronHouse (Feb–Aug 2026): not disputed.",
         "Evidence attached: none.\nEarlier payments to IronHouse: none on record.")],
       "unauthorised transaction")),

# ------------------------------------------------------------------ de08
# why: repayments 310 + 85 + 210 + rent 650 = 1,255 / 2,800 = 44.8% > 40% -> fails (1).
# Twin: rent 350 -> 955 / 2,800 = 34.1% -> passes (0).
Y("de08", "Does the loan application fail Corriemoor's affordability rule?",
"""
Corriemoor Credit Union — Personal Loan Affordability Rule
Debt-to-income ratio (DTI) = total monthly debt payments ÷ gross monthly income.
Total monthly debt payments = all existing loan repayments + credit card minimum payments + car or other finance + rent or mortgage + the repayment on the new loan.
Applications with a DTI above 40% fail the affordability rule and are declined. Savings held with the credit union do not change the DTI.

Application CCU-L-3309 — Aled Morgan
Loan requested: £4,000 over 24 months — monthly repayment £210
Gross monthly income: £2,800
Existing commitments: car finance £310/month; credit card minimum payment £85/month; rent £650/month
Utilities and phone: about £190/month
Savings with Corriemoor: £3,100
Purpose: kitchen appliances and a boiler repair.
""",
[("Fails affordability", "DTI above 40%."),
 ("Passes affordability", "DTI of 40% or less.")],
1, 3,
twin=T([("rent £650/month", "rent £350/month")], 0)),

# ------------------------------------------------------------------ de09
# why: one site (60 users) cannot use billing, other sites fine -> whole team/site outage -> P2.
# CFO's title does not raise priority. Twin: all users across every site -> P1.
C("de09", "What priority should the service desk assign to ticket INC-81502?",
"""
Tarnside Energy — IT Service Desk Priority Matrix
P1: complete outage of a service for all users, or any fault affecting a safety system (gas control room, emergency line).
P2: outage affecting a whole team or site; or a single user in a listed critical role (control room operator, emergency line handler) with no workaround.
P3: a single user unable to work, no workaround.
P4: a single user with a workaround, or a service request.
Job title does not change priority unless the role is on the critical list.

Ticket INC-81502, opened 08:07 by the Pellow contact-centre team leader
"None of the 60 agents here can log in to the billing system — error 'session broker unavailable'. We can still take calls but can't see bills. Our CFO is visiting today and wants this fixed now."
Service desk checks: the Harrowfield and Ashcombe offices can log in to billing normally. The gas control room and emergency line use separate systems and are unaffected.
""",
[("P1", "outage for all users, or a safety-system fault."),
 ("P2", "outage for a whole team or site, or a critical-role user with no workaround."),
 ("P3", "a single user unable to work, no workaround."),
 ("P4", "a single user with a workaround, or a service request.")],
"P2", 2, ordered=True,
twin=T([("the Harrowfield and Ashcombe offices can log in to billing normally.", "the Harrowfield and Ashcombe offices, and all remote staff, report the same error — no one can log in to billing.")],
       "P1")),

# ------------------------------------------------------------------ de10
# why: scheduled 14:12, arrived 14:59 = 47 min -> 30-59 band -> 50%. Twin: 15:16 = 64 min -> 100% single.
C("de10", "Which Delay Repay award applies to claim TR-DR-40018?",
"""
Tollbar Rail — Delay Repay
Delay is measured at the destination station, against the scheduled arrival of the train the customer was booked on or took.
• 15–29 minutes late: 25% of the single fare (or 25% of half the return fare).
• 30–59 minutes late: 50% of the single fare.
• 60–119 minutes late: 100% of the single fare.
• 120 minutes or more: 100% of the return fare (or of the single fare for a single ticket).
Claims must be made within 28 days of the journey.

Claim TR-DR-40018 — customer Yvonne Achebe
Ticket: Anytime Single, Harrowfield → Castlebridge, £38.00
Train: 12:40 Harrowfield → Castlebridge, scheduled to arrive 14:12
Actual arrival at Castlebridge: 14:59 (signal failure at Wexley Junction)
Journey date: 12 September 2026. Claim made: 20 September 2026.
Customer note: "I missed my connection to Pellow and got home an hour and a half late."
""",
[("no compensation", "delay under 15 minutes."),
 ("25% of the fare", "delay of 15–29 minutes."),
 ("50% of the fare", "delay of 30–59 minutes."),
 ("100% of the single fare", "delay of 60–119 minutes."),
 ("100% of the return fare", "delay of 120 minutes or more."),
 ("claim out of time", "claim made more than 28 days after the journey.")],
"50% of the fare", 2,
twin=T([("Actual arrival at Castlebridge: 14:59", "Actual arrival at Castlebridge: 15:16")], "100% of the single fare")),

# ------------------------------------------------------------------ de11
# why: clock starts when ID arrives (20 Aug) -> due 20 Sep; no extension notified; sent 24 Sep -> late (1).
# Twin: sent 18 Sep -> on time (0).
Y("de11", "Was Tarnside's response to the subject access request late?",
"""
Tarnside Energy — Subject Access Requests (SAR) procedure
1. We must respond within one calendar month of receiving the request.
2. If we need proof of identity, we ask for it promptly and the one-month period starts on the day we receive the ID.
3. For complex or multiple requests, the deadline may be extended by up to two further months, but only if we tell the customer about the extension, with reasons, within the first month.

SAR log — reference SAR-26-0419, customer Miriam Szabo
Request received by email: 3 August 2026
ID requested: 4 August 2026
ID received (copy of passport and a recent bank statement): 20 August 2026
Extension: none notified to the customer
Response (copy of account records, call recordings and meter history) sent: 24 September 2026
Customer complaint, 25 September: "You took nearly two months to answer me."
""",
[("Late response", "the response was sent after the deadline that applies."),
 ("On-time response", "the response was sent on or before the deadline.")],
1, 3,
twin=T([("sent: 24 September 2026", "sent: 18 September 2026")], 0)),

# ------------------------------------------------------------------ de12
# why: household includes a child under 2 (14 months) -> protected -> no force-fit; offer payment plan.
# Twin: child aged 3 -> not protected; debt £640 > £200 and 40 days >= 28 since final notice -> warrant route.
C("de12", "Which debt step may Tarnside take with account TE-55031?",
"""
Tarnside Energy — Prepayment Meter Installation Rules
1. A prepayment meter may be fitted under warrant only if the debt is over £200 AND at least 28 days have passed since the final notice AND the household is not protected.
2. Protected households: anyone aged 75 or over, a child under 2, or anyone who relies on powered medical equipment at home. For a protected household, the only step is to offer an affordable payment plan; a meter may not be fitted under warrant.
3. If the debt is £200 or less, or 28 days have not passed, send debt-advice information only.

Account TE-55031 — the Farrell household, 18 Quarry Lane
Debt: £640 (electricity)
Final notice sent: 14 August 2026 (40 days ago)
Household (from the vulnerability register, updated July 2026): Kieran Farrell (34), Aoife Farrell (31), and a daughter aged 14 months.
Contact attempts: 3 calls, 2 letters; the customer has not replied.
Collections team note: "No engagement at all — recommend warrant."
""",
[("fit a prepayment meter under warrant", "debt over £200, 28+ days since the final notice, and not a protected household."),
 ("offer a payment plan — protected household", "the household is protected."),
 ("send debt-advice information only", "debt of £200 or less, or fewer than 28 days since the final notice."),
 ("no action", "no debt on the account.")],
"offer a payment plan — protected household", 2,
twin=T([("and a daughter aged 14 months.", "and a daughter aged 3.")], "fit a prepayment meter under warrant")),

# ------------------------------------------------------------------ de13
# why: both fair-use tests met, but surcharges need 14 days after the warning; 2 Sept -> 10 Sept is 8 days
# -> not yet (0). Twin: 20 Sept = 18 days -> may charge (1).
Y("de13", "May Quaystone start charging Nadine the roaming surcharge today?",
"""
Quaystone Mobile — Roam-like-Home Fair Use Policy
Customers can use their allowance in the EU at no extra cost. Over any 4-month period, if a customer (a) spends more days abroad than in the UK AND (b) uses more data abroad than in the UK, Quaystone may send a fair-use warning. If the pattern continues, a surcharge of £2 per GB may be applied, but not until 14 days after the warning was sent.

Account review — Nadine Moreau, 4-month window June–September 2026
Days abroad (France): 71 · Days in the UK: 51
Data used abroad: 38 GB · Data used in the UK: 12 GB
Fair-use warning sent by SMS and email: 2 September 2026
Usage since the warning: still in France, 6 GB used
Today's date: 10 September 2026
Billing team note: "Customer is clearly living abroad — start the surcharge from today."
""",
[("Surcharge may start", "both fair-use tests are met and at least 14 days have passed since the warning."),
 ("Surcharge may not start yet", "a fair-use test is not met, or 14 days have not passed since the warning.")],
0, 2,
twin=T([("Today's date: 10 September 2026", "Today's date: 20 September 2026")], 1)),

# ------------------------------------------------------------------ de14
# why: signature-required parcel cannot go to a safe place or neighbour; customer out -> card and depot.
# Twin: no signature required, safe place nominated -> safe place.
C("de14", "Where should the driver leave parcel PW-6612-B?",
"""
Parcelwick — Missed Delivery Rules (in this order)
1. Parcels marked "signature required" must be signed for by someone at the address. If no one is in, leave a card and take the parcel back to the depot. They may never be left in a safe place or with a neighbour.
2. Otherwise, if the customer has nominated a safe place, leave it there and photograph it.
3. Otherwise, if the sender allows neighbour delivery, leave it with a neighbour and post a card.
4. Otherwise, leave a card and return the parcel to the depot.
Parcels are returned to the sender only after 3 failed attempts or 14 days at the depot.

Driver handheld — Friday 25 September 2026, 13:05, 41 Heron Way
Parcel PW-6612-B — sender: Vellum Phones Ltd — label: SIGNATURE REQUIRED
Customer's nominated safe place: "in the blue shed by the back gate"
Sender allows neighbour delivery: yes
Knocked twice, no answer; neighbour at 43 offered to take it.
Attempt number: 1
""",
[("leave in the nominated safe place", "rule 2 applies."),
 ("leave with the neighbour", "rule 3 applies."),
 ("card and return to the depot", "rule 1 or rule 4 applies."),
 ("return to the sender", "3 failed attempts or 14 days at the depot.")],
"card and return to the depot", 2,
twin=T([("label: SIGNATURE REQUIRED", "label: standard delivery, no signature needed")], "leave in the nominated safe place")),

# ------------------------------------------------------------------ de15
# why: reported Mon 09:00 -> 2 full working days end Wed 09:00; fixed Wed 17:00 -> not restored in time ->
# compensation owed -> "not owed" is false (0). Twin: fixed Tue 16:00 -> not owed -> 1.
Y("de15", "Is it true that Mr Hale is not owed automatic compensation for the broadband fault?",
"""
Quaystone Broadband — Automatic Compensation
If your broadband stops working and is not fixed within 2 full working days of you reporting the fault, you are owed £9.33 for each calendar day after that until it is fixed. Working days are Monday to Friday, excluding bank holidays. A fault caused by the customer's own equipment is not covered.

Complaint CX-44821 — Callum Hale, Pellow
Fault reported: Monday 21 September 2026, 09:00 — no internet connection.
Engineer finding: damaged line in the street cabinet (Quaystone network). Customer's router working normally.
Service restored: Wednesday 23 September 2026, 17:00.
Bank holidays that week: none.
Customer: "I was without internet for most of three days and work from home. I'd like whatever I'm entitled to."
""",
[("Compensation owed", "the fault was not fixed within 2 full working days of being reported and is not the customer's own equipment."),
 ("Not owed", "the fault was fixed within 2 full working days, or was caused by the customer's own equipment.")],
0, 3, role="neg",
twin=T([("Service restored: Wednesday 23 September 2026, 17:00.", "Service restored: Tuesday 22 September 2026, 16:00.")], 1)),

# ------------------------------------------------------------------ de16
# why: DOB 12 Oct 2010, today 26 Sep 2026 -> still 15 -> Junior Saver (no own card yet).
# Twin: DOB 12 Aug 2010 -> 16 -> Young Saver.
C("de16", "Which Corriemoor account can Ella hold today?",
"""
Corriemoor Credit Union — Account types by age (on the day of application)
• Junior Saver: ages 0–15. Operated by a parent or guardian; no card.
• Young Saver: ages 16–17. The member operates it; debit card with a £100 daily limit; no overdraft.
• Adult Current Account: age 18 and over.
All members must live or work in the common bond area (Corriemoor and Pellow districts).

Branch enquiry — Saturday 26 September 2026
Applicant: Ella Brandt, date of birth 12 October 2010, lives in Pellow.
Accompanied by: her father, an existing Corriemoor member.
Ella: "I've just started a Saturday job at the bakery and I want my own card so my wages go straight in."
Staff note: proof of address and school ID seen.
""",
[("Junior Saver", "ages 0–15, operated by a parent or guardian."),
 ("Young Saver", "ages 16–17, operated by the member with a card."),
 ("Adult Current Account", "age 18 or over."),
 ("not eligible", "the applicant does not live or work in the common bond area.")],
"Junior Saver", 2, ordered=True,
twin=T([("date of birth 12 October 2010", "date of birth 12 August 2010")], "Young Saver")),
# ------------------------------------------------------------------ de17
# why: no fraud mentioned; complaint opened 10 July, today 20 Sept = 10 weeks >= 8 -> Escalation wins over
# Billing. Twin: opened 2 Sept (under 3 weeks) -> main issue is a disputed bill -> Billing disputes.
C("de17", "Which Quaystone team should complaint CX-50731 be routed to?",
"""
Quaystone Mobile & Broadband — Complaint Routing Rules (apply in order)
1. Any contact that mentions possible fraud, an unauthorised SIM swap or account takeover goes to Fraud & Security.
2. Any complaint that has been open for 8 weeks or more, or where the customer asks for a deadlock letter to take to the ombudsman, goes to Complaints Escalation.
3. Otherwise, route by the main issue (billing, network, devices, porting, cancellations, data protection or extra support).

Today's date: 20 September 2026
Complaint CX-50731 — customer Ayesha Rahman
Opened: 10 July 2026
Customer's latest message: "I'm still waiting for someone to sort out the £86 of roaming charges on my June bill. I was in Spain and I have Roam-like-Home on my plan, so I shouldn't have been charged at all. I've called three times. Please just fix it."
Account notes: no suspicious logins; no SIM changes in the last 12 months; no deadlock letter requested.
""",
[("Billing disputes", "a disputed charge or bill amount."),
 ("Network and coverage", "signal, speed or outage problems."),
 ("Device repairs and insurance", "faulty, lost or damaged handsets and insurance claims."),
 ("Fraud and Security", "possible fraud, unauthorised SIM swaps or account takeover."),
 ("Accessibility and extra support", "customers who need adjustments or extra help."),
 ("Porting and switching", "moving a number or service to or from another provider."),
 ("Contract cancellations", "ending a contract or disputing early termination fees."),
 ("Data protection", "subject access requests and personal data concerns."),
 ("Complaints Escalation", "complaints open 8 weeks or more, or deadlock letter requests.")],
"Complaints Escalation", 2,
twin=T([("Opened: 10 July 2026", "Opened: 2 September 2026")], "Billing disputes")),
]
