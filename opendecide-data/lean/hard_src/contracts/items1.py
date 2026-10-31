"""Contracts hard items, batch 1: limitation of liability and unilateral change (with near misses)."""
from common import C, Y, S, T

ITEMS = [
# 1 cap with carve-outs; email mentions indemnity, governing law, confidentiality
C("lol_cap_email",
"""From: Priya Ostrander <postrander@brightwell-analytics.example>
To: Procurement Desk
Subject: RE: Tessellate Data Services MSA - ready to sign?

Hi Marcus,

Legal has finished its pass on the Tessellate MSA (v4, redline dated 3 June). Most of our comments were accepted. The indemnity in Section 10 now covers third-party IP claims with no cap, which was our main ask, and they agreed to move the governing law to Illinois.

The one provision I want you to flag to the business owner before signature is Section 11.2, quoted in full below, because it will matter if their pipeline corrupts our warehouse again:

"11.2 EXCEPT FOR A PARTY'S OBLIGATIONS UNDER SECTION 10 (INDEMNIFICATION) AND BREACH OF SECTION 7 (CONFIDENTIALITY), NEITHER PARTY'S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT, WHETHER IN CONTRACT, TORT OR OTHERWISE, SHALL EXCEED THE FEES PAID OR PAYABLE BY CUSTOMER IN THE TWELVE (12) MONTHS PRECEDING THE EVENT GIVING RISE TO THE CLAIM."

In practice a bad data-loss incident gets us roughly $180k back at most, whatever it actually costs us to rebuild. If the business owner is not comfortable with that, we need to push back this week.

Thanks,
Priya""",
["LOL", "IND", "CONF", "COL", "WD", "TWC", "FM", "NONE"], "LOL", 2, t="Section 11.2"),

# 2 exclusion of liability for specified events, no word "limit"
C("lol_gym_property",
"""LedgerLane Community Forum > Consumer Rights > General

Title: Gym says they're not on the hook after my bike was stolen from THEIR rack?

I've been a member at Pinebrook Fitness (Alder Street location) for three years. Last Tuesday my e-bike was cut off the rack that's bolted to their building, inside the fenced area they tell members to use. The front desk shrugged and pointed me to my membership agreement. Here's the line they highlighted, word for word:

"Pinebrook Fitness is not responsible for the loss of, theft of, or damage to any personal property, including property left in lockers, on the exercise floor, in the member parking area, or in the secured bike enclosure, whether or not such property is supervised by staff."

The camera over the enclosure has apparently been broken since spring, which they admitted. I'm not trying to sue anybody, I just want to know what kind of clause this is so I can look up whether it's enforceable in my state. My friend says it's a warranty thing, my brother-in-law says it's basically an indemnity. Anyone know?

Edit: I never signed anything separate about the bike enclosure, it's just in the main membership terms.""",
["LOL", "WD", "IND", "TWC", "UC", "CR", "DS", "NONE"], "LOL", 2, t="the sentence the member quotes"),

# 3 insurance requirement full of liability keywords
C("lol_insurance",
"""Contract review queue - ticket CR-2291
Agreement: Subcontract Agreement between Harbor & Finch Logistics, Inc. (Contractor) and Delacroix Rigging LLC (Subcontractor)
Reviewer: T. Kell | Status: needs clause tag before routing to Risk

Clause to tag (Article 14.1, as drafted by Contractor):

"Subcontractor shall procure and maintain at its sole cost, throughout the Term and for two (2) years thereafter, (a) commercial general liability insurance with limits of not less than $2,000,000 per occurrence and $4,000,000 in the aggregate; (b) automobile liability insurance with a combined single limit of $1,000,000; and (c) workers' compensation insurance at statutory limits. Such policies shall name Contractor as an additional insured and shall be primary and non-contributory to any insurance maintained by Contractor. Subcontractor shall deliver certificates of insurance before commencing work."

Reviewer note: the tagging tool pre-suggested a tag from the words in the clause. Please confirm or override it. Only one tag may be applied to Article 14.1.""",
["LOL", "IND", "WD", "FM", "ARB", "AR", "PAY", "NONE"], "NONE", 3, t="Article 14.1"),

# 4 carve-out that only preserves liability
Y("lol_carveout",
"""Extract from the Framework Services Agreement between Wexcombe Borough Council and Arlo Facilities Ltd (clause 18, as signed)

18.1 Subject to clause 18.3, the Supplier's total liability in respect of all claims arising in any Contract Year shall not exceed 125% of the Charges paid in that Contract Year.
18.2 Subject to clause 18.3, neither party shall be liable for any loss of profit, loss of revenue, or any indirect or consequential loss.
18.3 Nothing in this Agreement shall limit or exclude either party's liability for (a) death or personal injury caused by its negligence; (b) fraud or fraudulent misrepresentation; (c) breach of clause 22 (Data Protection); or (d) any other liability which cannot be limited or excluded by law.
18.4 The Supplier shall maintain the insurances set out in Schedule 7 for the duration of this Agreement.

Margin comment from the council's contract officer: "For the register, each sub-clause gets its own tag. I've done 18.1, 18.2 and 18.4 already - can someone confirm 18.3?\"""",
"LOL", 0, 3, t="clause 18.3"),

# 5 consequential damages exclusion without the word "limitation" (twin: preserves liability)
Y("lol_orderform_consequential",
"""ORDER FORM #NL-20931 - Nimbus Loop Workspace
Customer: Ferrovia Rail Parts GmbH | Plan: Business, 140 seats | Term: 12 months
Fees: EUR 16.80 per seat per month, invoiced annually in advance

Special Terms (these prevail over the online Terms of Service where they conflict):
1. Data residency: Customer Data will be hosted in the Frankfurt region.
2. Onboarding: Nimbus Loop will provide four remote training sessions of up to 90 minutes each during the first 60 days.
3. Damages: In no event will either party be responsible to the other for lost revenues, lost profits, loss of business opportunity, or any special, incidental or punitive damages arising out of this Order, even if advised of their possibility.
4. Invoices: Invoices will reference Customer's purchase order number PO-77-1402.
5. Support: Priority support with a four business-hour first response target.

Signed for Nimbus Loop: D. Whitcombe, Head of Sales EMEA
Signed for Customer: H. Lindqvist, Procurement""",
"LOL", 1, 2, t="Special Term 3",
twin=T([("In no event will either party be responsible to the other for", "Each party remains fully responsible to the other for"),
        (", even if advised of their possibility.", ", and any damages exclusion in the online Terms of Service will not apply to this Order.")], 0)),

# 6 section locator: cap among warranty, disclaimer, indemnity, insurance (twin: no cap)
S("lol_sections_cap",
"""Excerpt - Professional Services Agreement between Quillmark Software, Inc. and Oxbow Energy Cooperative (Article 9, Warranties and Remedies)

9.1 Performance Warranty. Quillmark warrants that the Services will be performed in a professional and workmanlike manner consistent with generally accepted industry standards.
9.2 Disclaimer. EXCEPT AS EXPRESSLY PROVIDED IN SECTION 9.1, QUILLMARK MAKES NO OTHER WARRANTIES, EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.
9.3 Liability Amount. Quillmark's liability for any claim arising under this Agreement shall not exceed the amount Oxbow paid for the Services giving rise to that claim.
9.4 Third-Party Claims. Quillmark will defend Oxbow against any claim by a third party alleging that the Deliverables infringe that party's intellectual property rights and will pay any damages finally awarded.
9.5 Insurance. Quillmark shall carry professional liability insurance with limits of at least $3,000,000 per claim and shall provide evidence of coverage upon request.""",
["Section 9.1", "Section 9.2", "Section 9.3", "Section 9.4", "Section 9.5"], "LOL", "Section 9.3", 2,
twin=T([("shall not exceed the amount Oxbow paid", "shall not be limited to the amount Oxbow paid")], "NONE")),

# 7 exclusive remedy plus excluded loss categories in a freelance agreement
C("lol_designer",
"""Freelance agreement - Wren Studio (Designer) and Cobalt Crate Coffee Roasters (Client)
Project: packaging redesign for the "Night Shift" blend, 3 bag sizes

What's included: two initial concepts, up to three rounds of revisions on the chosen concept, print-ready files (PDF/X-4) and a one-page brand usage sheet.

Timeline: concepts within 10 working days of the kickoff call; final files within 5 working days of sign-off on the last revision round.

Fees: $4,800, with 40% due on signing and 60% due on delivery of final files.

Proofing and Errors: Client is responsible for proofreading all text, barcodes and regulatory marks before final sign-off. If an error in delivered files is Designer's fault, Designer's only obligation is to correct the files at no additional charge; Designer will not reimburse printing, reprinting, shipping, or lost-sales costs, however caused.

Ownership: on full payment, Client owns the final artwork. Designer may show the work in its portfolio after the product launches.""",
["LOL", "WD", "IND", "TWC", "LIC", "PAY", "ASG", "NONE"], "LOL", 3, t="the \"Proofing and Errors\" paragraph"),

# 8 indemnity worded with "liabilities" and "damages"
C("ind_hosting",
"""#legal-ops (internal chat, Lumenfold Inc.)

Rhea Castellanos 10:14
Can someone tag s.12 of the Ardent Cloud customer agreement for the register? Renewal is Friday and it's the last untagged clause. Pasting it here:

"12. Customer Responsibilities for Claims. Customer shall defend, indemnify and hold harmless Ardent, its affiliates, and their respective officers and employees from and against any and all third-party claims, and all resulting damages, liabilities, penalties, and costs (including reasonable attorneys' fees), arising from (a) Customer Data, (b) Customer's or its End Users' violation of the Acceptable Use Policy, or (c) Customer's applications running on the Services. Ardent will promptly notify Customer of any such claim and give Customer sole control of its defense, provided that Customer may not settle any claim that imposes an obligation on Ardent without Ardent's prior written consent."

Jonah Whitlock 10:16
On it. It's only one tag per clause in the register, right?

Rhea Castellanos 10:16
Right, one tag.""",
["LOL", "IND", "WD", "DS", "CR", "TWC", "CONF", "NONE"], "IND", 2, t="section 12"),

# 9 first-party damage responsibility, no cap (twin: adds a cap)
C("lol_hotel_damage",
"""Juniper Row Hotels - Group Sales Agreement (excerpt)
Group: Vantage Robotics Summit 2026 | Dates: 14-17 October | Rooms: 220 at peak night

Clause 11 - Damage to Hotel Property
The Group shall be responsible for any damage to the Hotel's premises, furnishings, or equipment caused by the Group's attendees, exhibitors, or contractors. The Hotel will provide the Group with an itemised invoice for repair or replacement costs within thirty (30) days after departure, together with photographs of the damage. The Hotel shall make reasonable efforts to recover costs from the responsible individual before invoicing the Group.

Clause 12 - Attrition
The Group may reduce its room block by up to 10% without charge until 60 days before arrival.

Event coordinator's question in the shared tracker: "Our risk team files every clause of hotel contracts under one of its standard tags. Which tag fits Clause 11?\"""",
["LOL", "WD", "FM", "UC", "AR", "TWC", "COL", "NONE"], "NONE", 3, t="Clause 11",
twin=T([("caused by the Group's attendees, exhibitors, or contractors.", "caused by the Group's attendees, exhibitors, or contractors, up to a maximum of USD 25,000 in total for the event.")], "LOL")),

# 10 force majeure phrased as "shall not be liable" with a termination right
C("fm_supply",
"""From: Anneke Voss (Supply Chain, Redfern Labs)
To: Carlo Mbeki (Account Manager, Ferrovia Rail Parts)
Subject: Port strike - PO 4471 and 4472

Carlo, thanks for the call. As discussed, before we agree anything about the delayed containers I'd like us both to be reading the same clause. From our Purchase Agreement:

"15.1 Neither party shall be liable for any failure or delay in performing its obligations (other than payment obligations) to the extent caused by events beyond its reasonable control, including fire, flood, epidemic, labour disputes not involving the affected party's own workforce, or acts of government, provided that the affected party notifies the other within five (5) business days and uses reasonable efforts to resume performance. If such an event continues for more than sixty (60) days, either party may terminate the affected Purchase Order on written notice."

The strike started 9 May and you notified us on 12 May, so the notice point is fine. My concern is what happens if it runs past July.

Anneke""",
["LOL", "FM", "TWC", "WD", "ASG", "UC", "SLA", "NONE"], "FM", 2, t="Section 15.1"),

# 11 large option set: backup-based exclusion plus exclusive remedy
C("lol_backup_big",
"""Tender clarification log - RFP 2026-117 (Document management platform), Sundial Learning Trust

Question 23 (from bidder Glasswing Documents Ltd): "Please confirm whether Clause 19.6 of the draft contract is negotiable."

Clause 19.6 (draft):
"The Supplier shall have no liability for any loss or corruption of Authority Data to the extent that the loss would have been avoided had the Authority maintained its own backups in accordance with the Authority Data Policy, and the service credits set out in Schedule 2 shall be the Authority's sole and exclusive remedy for any failure of the Service to meet the Availability Target."

Authority response (draft, not yet issued): "Clause 19.6 reflects the Authority's standard position and is not open for negotiation. Bidders should price accordingly."

Procurement lead's instruction to the evaluation panel: record one category per clause in the clarification log so that the legal team can track which risk positions bidders challenged.""",
["LOL", "UC", "TWC", "COL", "ARB", "CR", "DS", "AR", "FS", "IND", "WD", "FM", "DR", "ASG", "CONF", "NONE"], "LOL", 3,
t="Clause 19.6"),

# 12 photographer: liability limited to refund (twin: refund plus all remedies kept)
Y("lol_photographer",
"""Hi Dana and Theo - congratulations again! Below is the booking agreement for your 12 September wedding. Please read it, sign page 2, and send it back with the 30% deposit to hold the date.

Coverage: 8 hours, two photographers, ceremony at Wexmoor Chapel and reception at the Saltmarsh Boathouse.
Deliverables: at least 500 edited images in an online gallery within 8 weeks; a 40-page linen album if you choose the Album package.
Travel: included within 50 miles of our studio; beyond that, $0.70 per mile.
Equipment Failure: We shoot on dual-card cameras and carry backup bodies. In the unlikely event that images are lost or damaged due to equipment failure or data corruption, our liability is limited to a full refund of the deposit and all fees you have paid.
Rescheduling: one free date change if requested at least 120 days before the wedding.
Image use: we may use a selection of images on our website and social media unless you opt out below.

Warmly,
Imogen Hale, Hale & Harrow Photography""",
"LOL", 1, 2, t="the Equipment Failure paragraph",
twin=T([("our liability is limited to a full refund of the deposit and all fees you have paid.", "we will refund the deposit and all fees you have paid, and you keep every other remedy the law gives you.")], 0)),

# 13 section locator in conditions of carriage
S("lol_parcel_sections",
"""Brisa Mobility Courier - Conditions of Carriage (UK domestic), selected paragraphs

C4. Prohibited Items. We will not carry cash, loose lithium batteries, perishable food, or live animals. Parcels found to contain prohibited items will be returned at the sender's expense.
C5. Delivery Attempts. We will make up to two delivery attempts. After the second failed attempt, the parcel will be held at the nearest Brisa Point for 7 days.
C6. Compensation. Our liability for loss of or damage to a parcel is limited to the declared value on the waybill or GBP 75, whichever is lower, unless you purchased Extended Cover at booking, in which case the limit is the declared value up to GBP 1,000.
C7. Customs. For parcels to the Channel Islands, you are responsible for providing accurate customs information.
C8. Your Data. We use your name, address and phone number to deliver the parcel and to send you tracking updates.""",
["C4", "C5", "C6", "C7", "C8"], "LOL", "C6", 1),

# 14 as-is warranty disclaimer with LOL-style wording
C("wd_asis",
"""Quillmark Beta Program - Participation Terms (section 6)

6. Beta Software. The Beta Features are pre-release and are provided "AS IS" and "AS AVAILABLE". To the fullest extent permitted by law, Quillmark expressly disclaims all warranties, whether express, implied or statutory, including warranties of merchantability, fitness for a particular purpose, title, accuracy, and non-infringement. Quillmark does not warrant that the Beta Features will be uninterrupted, secure, or error-free, or that any data you enter into them will be preserved. Beta Features may never be made generally available.

Product manager's note: participants with questions about this section should contact beta@quillmark.example before enabling any Beta Feature on a production workspace.""",
["LOL", "WD", "UC", "TWC", "DR", "IND", "CR", "NONE"], "WD", 2, t="section 6"),

# 15 continued-use amendment (twin: requires affirmative acceptance)
C("uc_terms_continued_use",
"""Vellora Media - Terms of Service (last updated 2 February 2026)

[...]

17. Changes to These Terms
We may revise these Terms from time to time, for example to reflect new features or changes in law. The current version will always be available at vellora.example/terms, and the date at the top will show when it was last updated. If a revision is material, we will notify you by email or through an in-app banner at least 15 days before it takes effect. By continuing to access or use the Services after a revision becomes effective, you agree to be bound by the revised Terms. If you do not agree to a revision, you must stop using the Services and may delete your account from Settings.

18. Contact
Questions about these Terms can be sent to legal@vellora.example.""",
["UC", "TWC", "AR", "CR", "DS", "COL", "LOL", "NONE"], "UC", 2, t="Section 17",
twin=T([("By continuing to access or use the Services after a revision becomes effective, you agree to be bound by the revised Terms. If you do not agree to a revision, you must stop using the Services and may delete your account from Settings.",
         "A revision will apply to your account only after you accept it by selecting \"I agree\" in the notice; until then, the version you last accepted continues to govern your use of the Services.")], "NONE")),

# 16 discretionary renewal price change (twin: fixed 3% step)
C("uc_renewal_price",
"""Nimbus Loop Master Subscription Agreement - Section 5 (Fees)

5.1 Fees. Customer shall pay the fees stated in each Order Form. Fees are quoted per Seat per month and are billed annually in advance.
5.2 Renewal Pricing. Nimbus Loop may adjust the per-Seat price applicable to any Renewal Term by notifying Customer in writing at least thirty (30) days before that Renewal Term begins.
5.3 Taxes. Fees exclude all sales, use, value-added and similar taxes, which Customer shall pay unless it provides a valid exemption certificate.

Deal-desk comment (Harbor & Finch Logistics, customer side): "We expect this to be a three-year relationship, so flagging 5.2 for the clause register before we countersign.\"""",
["UC", "AR", "TWC", "LOL", "COL", "FM", "ASG", "NONE"], "UC", 3, t="Section 5.2",
twin=T([("Nimbus Loop may adjust the per-Seat price applicable to any Renewal Term by notifying Customer in writing at least thirty (30) days before that Renewal Term begins.",
         "The per-Seat price applicable to each Renewal Term shall be the per-Seat price for the immediately preceding term increased by three percent (3%).")], "NONE")),

# 17 mutual written amendment (twin: supplier may revise specs by notice)
Y("uc_amendment_signed",
"""Supply Agreement between Ferrovia Rail Parts GmbH ("Supplier") and Oxbow Energy Cooperative ("Buyer") - General Provisions

24.1 Entire Agreement. This Agreement, together with its Schedules, constitutes the entire agreement between the parties relating to its subject matter.
24.2 Amendment. No amendment, variation, or modification of this Agreement, including of the Product Specifications in Schedule 1, shall be effective unless it is in writing and signed by authorised representatives of both parties.
24.3 Waiver. No failure or delay by either party in exercising any right shall operate as a waiver of that right.
24.4 Counterparts. This Agreement may be executed in any number of counterparts, each of which is an original.

Paralegal query on the review sheet: "Our playbook flags every unilateral change right. Does 24.2 need the flag?\"""",
"UC", 0, 3, t="Section 24.2",
twin=T([("shall be effective unless it is in writing and signed by authorised representatives of both parties.",
         "shall be effective unless it is in writing and signed by authorised representatives of both parties, except that Supplier may revise the Product Specifications in Schedule 1 at any time by written notice to Buyer.")], 1)),

# 18 game feature/price changes; complaint about a nerfed item
C("uc_game_features",
"""Saltmarsh Games - End User Terms for "Tidebreaker Online" (excerpt)

8. Virtual Items. Gems, skins and other virtual items are licensed, not sold, and have no cash value. They cannot be transferred between accounts or redeemed for money.
9. Game Changes. We are constantly improving Tidebreaker. We may modify, rebalance, or remove any feature, game mode, virtual item, or drop rate, and may change the Gem price of items in the in-game store, at any time. Some changes may reduce the usefulness or value of virtual items you already hold.
10. Player Content. We may remove any player name, guild name or chat message that breaks the Code of Conduct.

Support ticket #88213 from player "kelpie_rogue": "You nerfed my Stormcaller skin two days after I bought it with 2,400 gems. Your terms don't even let you do that, right?"

Support lead's instruction: before replying, tag the ticket with the category of the term the studio relies on for the change the player is complaining about.""",
["UC", "TWC", "CR", "LOL", "WD", "AR", "DS", "NONE"], "UC", 3, t="the term the studio relies on"),

# 19 CPI formula rent escalation
C("uc_cpi",
"""Maplecrest Property Management - Commercial Lease, Unit 4B, Kestrel Business Park
Tenant: Halcyon Dental Group LLC

Article 5 - Rent Adjustment
5.1 Base Rent for the first Lease Year is $6,250 per month.
5.2 On the first day of each subsequent Lease Year, Base Rent shall be adjusted by the percentage change in the Consumer Price Index for All Urban Consumers (the "Index") published for the twelve months ending three months before the adjustment date, provided that no annual increase shall be less than 2% or greater than 5%. Landlord shall deliver a statement showing the calculation at least 30 days before the adjustment date.
5.3 If the Index is discontinued, Landlord and Tenant shall agree in good faith on a comparable replacement index.

Tenant's broker, by email: "Can you confirm how we should tag 5.2 in the lease abstract? I want it filed correctly before the board meeting.\"""",
["UC", "AR", "TWC", "LOL", "FM", "COL", "ARB", "NONE"], "NONE", 3, t="Section 5.2"),

# 20 section locator: AUP updated on posting vs mutual variation (twin: needs approval)
S("uc_aup_sections",
"""Glasswing Security - Managed Detection Services Terms (Clauses 12-16)

12. Service Levels. Glasswing will acknowledge Priority 1 alerts within 15 minutes, 24x7. If it misses this target in any month, Customer will receive a credit of 5% of that month's fees.
13. Suspension. Glasswing may suspend the Services if Customer's systems are being used to attack third parties, and will restore them once the activity stops.
14. Acceptable Use Policy. Customer's use of the Services is subject to the Acceptable Use Policy at glasswing.example/aup, which is incorporated into these Terms. Glasswing may update the Acceptable Use Policy at any time, and updates take effect when posted.
15. Entire Agreement; Variation. These Terms and each Order are the entire agreement between the parties. These Terms may be varied only by a written document signed by both parties.
16. Notices. Notices must be sent by email to the addresses in the Order and are effective on receipt.""",
["Clause 12", "Clause 13", "Clause 14", "Clause 15", "Clause 16"], "UC", "Clause 14", 3,
twin=T([("Glasswing may update the Acceptable Use Policy at any time, and updates take effect when posted.",
         "Glasswing may propose updates to the Acceptable Use Policy, which take effect only once Customer has approved them in writing.")], "NONE")),

# 21 loyalty programme rule changes on notice
Y("uc_loyalty",
"""Juniper Row Rewards - Program Rules (excerpt), as printed on the back of the member welcome letter

R3. Earning. Members earn 10 points per US$1 spent on room rates at participating hotels. Taxes and incidental charges do not earn points.
R7. Redemption. Points may be redeemed for free nights, room upgrades, or partner gift cards, subject to availability.
R9. Program Changes. Juniper Row may change the number of points required for any reward, add or retire reward categories, or change the earning rate, upon sixty (60) days' notice posted on the Rewards page. Points already earned remain in your account but will be redeemable only on the terms then in effect.
R12. Expiry. Points expire after 18 months without any earning or redemption activity.

Member forum post (user "nightowl_travels"): "They just posted that free nights at my usual hotel go from 20,000 to 32,000 points. Surely the 60-day notice means this is just a normal amendment and not something they can simply impose?\"""",
"UC", 1, 3, t="rule R9"),

# 22 streaming price change quoted next to a renewal sentence
C("uc_streaming_price_forum",
"""Plover Community Help Forum
Thread: "Price going up AGAIN - can they do that mid-subscription?"

Original post by mo_greaves:
I'm on the annual Plover Premium plan I bought in January. Just got an email saying the price goes from $119 to $139 "at your next billing date". I checked the terms and found this:

"Plover may change its subscription plans and the price of the service from time to time. Any price change will apply to you no earlier than 30 days after we notify you, and will take effect at the start of your next billing period. If you do not wish to accept the price change, you can cancel your membership before the change takes effect."

Right above it there's a separate bit saying my plan "will continue for successive billing periods until cancelled", and further down there's a paragraph about sharing viewing data with "measurement partners". I only care about the price paragraph. What is that called, legally? Is it the same thing as the renewal bit?

Reply by forum volunteer: "Before anyone answers: please be precise about which paragraph you mean.\"""",
["UC", "AR", "TWC", "DS", "CR", "COL", "LOL", "NONE"], "UC", 2, t="the price paragraph the poster quotes"),

# 23 variable interest rate bullet next to closure and dormancy bullets
C("uc_bank_rate",
"""Quarry Hill Savings - Easy Access Saver: Key Account Terms

- Minimum opening deposit: $1
- Withdrawals: unlimited and free of charge; processed the same business day if requested before 3 pm.
- Interest: variable. The rate on the date you open your account is shown in your welcome pack. We may change the interest rate on your account at any time, for any reason. If we reduce the rate, we will tell you within 30 days after the change takes effect by a message in online banking.
- Closing your account: you can close your account at any time without charge.
- Dormancy: if there is no customer-initiated activity for 5 years, we may transfer the balance to our unclaimed balances scheme.

Compliance tester's worksheet, line 4: "Tag the Interest bullet only.\"""",
["UC", "TWC", "TFC", "PAY", "AR", "LOL", "DR", "NONE"], "UC", 2, t="the Interest bullet"),

# 24 change control needing both signatures (twin: binding when supplier issues it)
Y("uc_change_order",
"""Statement of Work No. 3 - Tandem Payroll implementation for Ember & Oak Furniture Co.

Scope: configuration of payroll for 410 employees across 3 states; data migration from the legacy system; parallel run for two pay cycles; training for 6 payroll administrators.
Milestones: (1) design sign-off - week 3; (2) migration complete - week 7; (3) parallel runs - weeks 8-10; (4) go-live - week 11.
Change Control: Either party may request a change to the scope, timeline, or fees in this SOW. Supplier will respond to any request with a draft Change Order describing the impact. A Change Order becomes binding only when signed by both parties' project sponsors; until then, work continues under the existing SOW.
Fees: fixed fee of $64,000, payable 25% at each milestone.
Assumptions: Customer will provide employee data in the agreed template by week 4.""",
"UC", 0, 3, t="the Change Control paragraph",
twin=T([("A Change Order becomes binding only when signed by both parties' project sponsors; until then, work continues under the existing SOW.",
         "A Change Order becomes binding on both parties when Supplier issues it, and work then continues under the SOW as changed.")], 1)),

# 25 customer email relying on an amendment clause
C("uc_notice_email",
"""Subject: We're updating Quillmark's Terms of Service

Hi there,

We're writing to let you know that we're updating the Quillmark Terms of Service, effective 1 March. The main changes: we're adding terms for our new drafting assistant, clarifying how shared workspaces are billed, and updating our list of sub-processors. You can read the new Terms and a summary of changes at quillmark.example/terms-2026.

You don't need to do anything. If you keep using Quillmark after 1 March, the updated Terms will apply to you.

For reference, the section of our current Terms that allows this update reads:
"16. Amendments. Quillmark may amend these Terms by providing notice through the Service or by email. Amended Terms are effective on the date stated in the notice, which will be at least 14 days after the notice is sent. Your continued use of the Service after that date constitutes acceptance of the amended Terms."

Thanks for using Quillmark,
The Quillmark Team""",
["UC", "AR", "TWC", "DS", "CR", "COL", "ARB", "NONE"], "UC", 1, t="section 16 of the current Terms"),

# 26 most-favoured-customer pricing
C("uc_mfn",
"""Master Purchase Agreement - Redfern Labs (Buyer) and Cobalt Crate Packaging (Vendor), Article 6 (Pricing)

6.1 Prices. Prices for Products are set out in Exhibit B and are fixed for the Initial Term.
6.2 Most Favoured Customer. If, during the Term, Vendor sells substantially similar Products to any other customer in comparable volumes at a lower per-unit price, Vendor shall promptly notify Buyer and offer Buyer the same lower price, effective from the date the lower price was first offered to that other customer.
6.3 Taxes. Prices exclude sales and use taxes, which Buyer shall pay.

Clause register instruction: tag only Section 6.2; one tag per section.""",
["UC", "PAY", "EXC", "AR", "LOL", "TWC", "AUD", "NONE"], "NONE", 3, t="Section 6.2"),
]
