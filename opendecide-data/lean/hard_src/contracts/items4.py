"""Contracts hard items, batch 4: mixed yes/no items and choice items with small and very large option sets."""
from common import C, Y, S, T, MAIN, NEAR

ALL_NEAR = [k for k in NEAR]

ITEMS = [
# ---------------------------------------------------------------- yes/no
Y("yn_lol_sole_remedy",
"""Ardent Cloud Systems - Storage Service Level Addendum

1. Availability Target. Ardent will use commercially reasonable efforts to make Object Storage available 99.9% of each calendar month.
2. Service Credits. If availability falls below the target, Customer will receive a credit of 10% of that month's storage fees for each full 0.1% shortfall, up to 50% of that month's fees.
3. Exclusive Remedy. The Service Credits in Section 2 are Customer's sole and exclusive remedy, and Ardent's entire liability, for any failure to meet the Availability Target.
4. Exclusions. Downtime caused by Customer's own configuration errors does not count against availability.

Contract analyst's task list: "Tag Section 3 of the Addendum; Sections 1, 2 and 4 are done.\"""",
"LOL", 1, 3, t="Section 3"),

Y("yn_ds_law_enforcement",
"""Halden Pay - Privacy Notice, section 11 ("Legal Requests")

"We may disclose your personal information, including your name, account number and transaction history, to law enforcement agencies, courts or regulators when we believe in good faith that disclosure is required by law or by a valid legal order. Where the law allows, we will tell you about the request before we disclose anything."

Privacy engineer's comment in the data inventory: "This one is compelled by law, so I'm not sure it belongs with the other disclosures. Checking it against the definition before I mark the row.\"""",
"DS", 1, 3, t="section 11"),

Y("yn_twc_change_of_control",
"""Reseller Agreement - Lumenfold Inc. (Supplier) and Brightloft Distribution Ltd (Reseller)

"17.4 Supplier may terminate this Agreement on thirty (30) days' written notice if Reseller undergoes a change of control, including any transaction in which a competitor of Supplier acquires more than 25% of Reseller's voting shares."

"17.5 Either party may terminate this Agreement on written notice if the other commits a material breach that remains uncured thirty (30) days after notice."

Reseller's general counsel, preparing a board paper: "I need to tell the board which of Supplier's exit rights let it walk away whenever it likes, and which depend on something happening first.\"""",
"TWC", 0, 3, t="Section 17.4"),

Y("yn_col_cisg_only",
"""International Sales Contract - Kestrel Freight Equipment BV (Seller) and Harbor & Finch Logistics, Inc. (Buyer), General Terms

"18. Title to the Goods passes to Buyer on full payment of the price."
"19. The parties agree that the United Nations Convention on Contracts for the International Sale of Goods shall not apply to this Contract."
"20. All prices are quoted in euros and exclude value added tax."
"21. Any dispute shall be submitted to the courts of Rotterdam."

Paralegal's checklist: clause 19 is the only clause of the General Terms still untagged; each clause gets its own row.""",
"COL", 0, 3, t="clause 19",
twin=T([("The parties agree that the United Nations Convention", "This Contract is governed by the laws of the Netherlands, and the parties agree that the United Nations Convention")], 1)),

Y("yn_arb_adjudication",
"""Construction Subcontract - Oxbow Energy Cooperative (Contractor) and Delacroix Rigging LLC (Subcontractor), clause 41

"41.1 Either party may at any time refer a dispute under this Subcontract to adjudication by an adjudicator nominated by the Tidewater Construction Institute.
41.2 The adjudicator's decision shall be binding on the parties until the dispute is finally determined by legal proceedings or by agreement, and the parties shall comply with it in the meantime.
41.3 Either party may commence legal proceedings in the courts of Cardiff to finally determine the dispute."

Site manager's email to the commercial team: "If we lose the adjudication on the crane delay, is that the end of it?\"""",
"ARB", 0, 3, t="clause 41 as a whole"),

Y("yn_cr_creator_hide",
"""Plover Upload Studio - Help Centre, "Managing comments"

"Creators may hide comments on their own videos. Hidden comments are no longer visible to the public but remain visible to the person who wrote them, who is not notified. Creators can also hold comments containing words from a custom list for manual review before they appear."

Viewer's complaint to Plover support: "My comment on a cooking channel vanished for everyone else but I can still see it. Which rule allowed that?"

Support agent's task: tag the quoted help-centre paragraph using the clause definitions, then reply.""",
"CR", 0, 3, t="the quoted help-centre paragraph",
twin=T([("Creators may hide comments on their own videos.", "Plover may hide comments on any video.")], 1)),

Y("yn_wd_rates",
"""Corvid Payments - International Transfers FAQ (incorporated into the Wallet Agreement)

"Q: Is the exchange rate I see the rate I'll get?
A: Exchange rates shown in the app before you confirm a transfer are indicative only. Corvid does not guarantee that the rate displayed will be the rate applied to your transfer, which is set at the moment the transfer is processed. Corvid's fee for each transfer is shown separately and does not change."

Complaint handler's note: "Customer lost $38 on the difference between the displayed and applied rate. Before replying I need to tag this FAQ answer against the definition.\"""",
"WD", 1, 3, t="the FAQ answer", extra=["LOL"]),

Y("yn_fs_governed",
"""Supplier Code Acknowledgement - Maplecrest Property Management vendors

Vendors must acknowledge the following before the first purchase order is issued:
(a) Vendors will comply with the Maplecrest Supplier Code of Conduct.
(b) Disputes arising from any purchase order shall be governed by the laws of the State of Delaware.
(c) Vendors will not offer gifts worth more than $75 to Maplecrest employees.
(d) Vendors will carry the insurance listed on the purchase order.

Vendor-onboarding analyst's form, field 12: classification of item (b).""",
"FS", 0, 2, t="item (b)",
twin=T([("shall be governed by the laws of the State of Delaware.", "shall be heard in the Court of Chancery of the State of Delaware.")], 1)),

Y("yn_ds_processor",
"""Harbourlight Lettings - Tenant Privacy Notice, section 6 ("Payments")

"Rent payments made through the app are processed by our payment provider, Halden Pay, which receives your name, card number, billing address and payment amount to complete each transaction and to prevent fraud. Halden Pay is not permitted to use this information for its own marketing."

Tenant union volunteer's spreadsheet: one row per section of the notice; column D records whether the section meets the definition below. Row 6 is next.""",
"DS", 1, 2, t="section 6"),

Y("yn_uc_integrations",
"""Quillmark Integrations Terms

"3.1 Quillmark offers optional integrations with third-party services such as calendars, storage drives and e-signature tools ("Integrations").
3.2 Quillmark may add, modify or discontinue any Integration at any time. Discontinuing an Integration does not entitle Customer to a refund.
3.3 Customer is responsible for its accounts with third-party services and for complying with their terms.
3.4 Integrations are provided free of charge and are not part of the Service Levels in the Master Agreement."

Customer success note: "Client is upset that the e-signature integration was dropped mid-contract. Tag 3.2 before the escalation call on Thursday.\"""",
"UC", 1, 2, t="section 3.2",
twin=T([("Quillmark may add, modify or discontinue any Integration at any time.", "Quillmark may modify or discontinue an Integration only with Customer's written approval.")], 0)),

Y("yn_twc_offer_letter",
"""Offer letter - Glasswing Security Ltd to Aiyana Morrow, Senior Detection Engineer

Start date: 2 November. Salary: $168,000 per year, paid semi-monthly.

Employment Relationship. Your employment with Glasswing is at will. Either you or Glasswing may end the employment relationship at any time, with or without cause, by giving two weeks' written notice. Glasswing may pay salary in lieu of notice.

Benefits: medical and dental cover from day one; retirement plan with a 4% match.

Aiyana's message to a friend who works in legal: "Before I sign - what kind of clause is the Employment Relationship paragraph?\"""",
"TWC", 1, 2, t="the Employment Relationship paragraph"),

Y("yn_arb_mediation_neg",
"""Franchise Agreement - Brightloft Stays (Franchisor) and Tidewater Hospitality LLC (Franchisee), section 26

"26.1 Before commencing any legal proceeding, the parties shall submit any dispute to mediation before a mediator they jointly select. The mediator shall have no power to impose a settlement, and either party may end the mediation at any time after the first session.
26.2 If the dispute is not settled within 60 days after the mediator is appointed, either party may bring proceedings in the courts of Denver, Colorado."

Franchisee's adviser: "Tag 26.1 on its own for the franchise disclosure summary.\"""",
"ARB", 0, 2, t="section 26.1", neg=True),

Y("yn_lol_setup_fee_neg",
"""Implementation Agreement - Tandem Payroll and Brightloft Stays

"8.1 Tandem will configure the payroll system described in Schedule 1 for a one-time Setup Fee of $18,500.
8.2 Customer's recovery from Tandem for all claims arising out of the implementation, taken together and whatever the legal theory, is limited to the amount of the Setup Fee.
8.3 The ongoing payroll service is governed by the separate Subscription Terms."

Finance director's note: "We're approving the budget today; legal just needs to tag 8.2 in the register.\"""",
"LOL", 1, 2, t="section 8.2", neg=True),

Y("yn_ar_membership_neg",
"""Harrowgate Museum Members - Membership Terms

"Your membership lasts 12 months from the date of joining and ends on the expiry date printed on your card. About 30 days before it ends, we'll email you a link to renew online. If you don't renew, your membership simply ends and no further payment is taken."

Members get free entry, two guest tickets and 10% off in the shop.

Membership officer, updating the terms register: "Consumer-law guidance says some subscription terms need an extra pre-contract notice. I've been asked to classify this paragraph first.\"""",
"AR", 0, 3, t="the membership paragraph", neg=True),

Y("yn_ds_deletion",
"""Sundial Learning - Account Deletion Policy

"When you delete your account, we delete your personal information, including your learning history and messages, within 30 days. We keep invoices and payment records for 7 years because tax law requires it, and backups containing your information are overwritten within a further 35 days."

Parent's question on the help forum: "After I delete my daughter's account, does anyone else ever get her data?"

Help-centre editor's task: tag the policy paragraph against the definition below before answering.""",
"DS", 0, 2, t="the policy paragraph"),

Y("yn_cr_synthetic",
"""Vellora Media - Terms of Service, section 12 ("Synthetic and Manipulated Media")

"12.1 You must disclose when a realistic image, video or audio clip you post has been generated or materially altered by software.
12.2 We may label, blur, reduce the distribution of, or remove images and videos that our systems or reviewers identify as synthetic or manipulated in a way that could mislead people.
12.3 We may ask you to confirm whether content is synthetic."

Policy analyst's tagging sheet: this row covers section 12.2 only.""",
"CR", 1, 2, t="section 12.2"),

Y("yn_uc_rate_card",
"""Master Services Agreement - Kestrel Freight and Cobalt Crate Packaging, clause 9

"9.1 Core services are charged at the rates in Schedule 2, fixed for the Initial Term.
9.2 Additional Services (such as weekend deliveries and pallet storage) are charged at the rates in the Rate Card at Annex D. Kestrel may revise the Rate Card once per calendar year by giving Customer sixty (60) days' written notice.
9.3 Invoices are payable within 30 days of receipt."

Customer's procurement lead: "Core rates are locked, so we have full price certainty, right? Tag 9.2 so I can check.\"""",
"UC", 1, 2, t="clause 9.2"),

Y("yn_col_seat",
"""Charter Party Addendum - Tidewater Shipping Co. and Oxbow Energy Cooperative

"A-7. Any dispute arising under this Charter Party shall be referred to arbitration before three arbitrators. The seat of arbitration shall be Stockholm, and the proceedings shall be conducted in English.
A-8. Demurrage is payable at USD 18,000 per day or pro rata for part of a day."

Chartering manager's note: "Our clause register tags sentences separately. This row is the second sentence of A-7; the first sentence already has its own row.\"""",
"COL", 0, 3, t="the second sentence of A-7"),

Y("yn_ds_affiliates",
"""Lumenfold Inc. - Customer Privacy Statement, section 6 ("Within our group")

"We may share your contact details and product usage information with other companies in the Lumenfold group, including Lumenfold Analytics GmbH and Lumenfold Services Ltd, so that they can provide support, cross-sell related products, and improve our services."

Section 7 of the statement (not quoted) covers international transfers, and section 8 covers retention.

Customer's data-protection lead, before signing: "List every recipient of our staff's data that the vendor's documents allow. Start with section 6.\"""",
"DS", 1, 2, t="section 6",
twin=T([("We may share your contact details and product usage information with other companies in the Lumenfold group, including Lumenfold Analytics GmbH and Lumenfold Services Ltd, so that they can provide support, cross-sell related products, and improve our services.",
         "Your contact details and product usage information stay with Lumenfold Inc. and are not shared with other companies in the Lumenfold group, such as Lumenfold Analytics GmbH and Lumenfold Services Ltd; Lumenfold Inc. uses them to provide support and improve our services.")], 0)),

Y("yn_twc_plain_neg",
"""Statement of Work Terms - Redfern Labs (Client) and Wren Studio (Agency)

"11. Client may terminate this SOW for convenience at any time on ten (10) business days' written notice. Agency will be paid for work performed up to the termination date, plus any non-cancellable third-party costs it has already committed with Client's approval."

"12. Either party may terminate this SOW immediately if the other party materially breaches it."

Agency's finance lead: "Redfern is our biggest client this year. Tag clause 11 for the revenue-risk report so the partners can see our exposure.\"""",
"TWC", 1, 2, t="clause 11", neg=True),

# ---------------------------------------------------------------- choice
C("wd_forecasts",
"""Brightwell Analytics - Demand Forecasting Service, Order Form rider

"R2. Forecasts. The Service produces statistical forecasts based on the data Customer supplies. Brightwell does not guarantee that any forecast will be accurate or that any particular business result will be achieved. Forecasts are statistical estimates and may differ materially from actual demand."

Customer's category manager, emailing the account team: "Our stores over-ordered by 18% after following the October forecast, and finance wants to know where we stand. Which kind of term is R2?\"""",
["LOL", "WD", "NONE"], "WD", 3, t="rider R2", keep_order=True),

C("fs_county_court",
"""Orchard Lane Tutoring - Terms for Families (UK), section 20

"20. Any claim relating to these Terms must be brought in the county court for the district in which the parent or guardian who signed up lives. This does not affect your right to complain to the Tutoring Standards Ombudsman first."

Section 19 (not quoted) explains how to cancel lessons, and section 21 explains how to contact the company.

Parent's question: "I live in Leeds and the company is in Bristol. What does section 20 actually decide, and what's that kind of clause called?\"""",
["COL", "FS", "ARB", "NONE"], "FS", 2, t="section 20"),

C("tfc_fm_termination",
"""Event Services Agreement - Juniper Row Hotels and Vantage Robotics Summit, clause 18.3

"18.3 If a Force Majeure Event (as defined in clause 18.1) prevents either party from performing its obligations for more than ninety (90) consecutive days, either party may terminate this Agreement by written notice, and the Hotel shall refund all deposits received for dates that fall after the termination date."

Clause 18.1 (not quoted) defines Force Majeure Events and suspends obligations while they last. Tagging instruction: tag 18.3 separately from 18.1.""",
["TWC", "TFC", "AR", "FM", "NONE"], "TFC", 3, t="clause 18.3"),

C("asg_affiliate",
"""Software Subscription Agreement - Quillmark Software, Inc. and Northgate Clinics, clause 23

"23. Provider may assign or transfer this Agreement, in whole or in part, to any of its affiliates or to a successor in connection with a merger, acquisition, or sale of all or substantially all of its assets, without Customer's consent, by giving Customer written notice. Customer may not assign this Agreement without Provider's prior written consent."

Clinic's compliance officer: "Could this put our patient scheduling data in someone else's hands? Tag clause 23 first, then we'll discuss.\"""",
["ASG", "DS", "TWC", "UC", "CONF", "LOL", "COL", "AR", "IND", "EXC", "NONE"], "ASG", 3, t="clause 23"),

C("ns_hire",
"""Consulting Framework - Talvik Advisory LLC and Maplecrest Property Management, clause 15

"15. During the Term and for twelve (12) months afterwards, neither party shall, directly or indirectly, solicit for employment any employee of the other party who worked on the Services, provided that general job advertisements not targeted at those employees, and hiring anyone who responds to them, are not a breach."

HR business partner's question: "We want to hire one of Talvik's analysts who applied through our careers page. Tag clause 15 so legal can advise.\"""",
["NS", "CONF", "EXC", "TWC", "TFC", "ASG", "IND", "LOL", "DS", "UC", "AR", "NONE"], "NS", 2, t="clause 15"),

C("exc_territory",
"""Distribution Agreement - Redfern Labs (Manufacturer) and Brisa Mobility S.L. (Distributor), clause 4

"4.1 Manufacturer appoints Distributor as its distributor for the Products in Spain and Portugal (the "Territory").
4.2 During the Term, Distributor shall purchase the Products only from Manufacturer and shall not sell, market or distribute in the Territory any product that competes with the Products.
4.3 Distributor may appoint sub-distributors with Manufacturer's written consent."

Commercial manager's request to the contracts team: "Tag clause 4.2 for the channel-conflict review.\"""",
["EXC", "NS", "CONF", "ASG", "TWC", "TFC", "AR", "UC", "LOL", "IND", "DS", "PAY", "NONE"], "EXC", 2, t="clause 4.2"),

C("twc_big24",
"""Order Form terms - Ardent Cloud Systems and Harrowgate Museum Trust

"Early Termination. Customer may terminate this Order for convenience at any time on thirty (30) days' written notice, subject to payment of the Early Termination Fee, which equals the fees that would have been payable for the three (3) months following the termination date."

"Suspension. Ardent may suspend the Services if any undisputed invoice is more than 45 days overdue."

Trust finance committee paper, appendix B: each Order Form term is tagged using the full clause taxonomy. This row is the Early Termination term.""",
MAIN + [k for k in ALL_NEAR if k not in ("SLA", "EA", "NOT")] + ["NONE"], "TWC", 2, t="the Early Termination term"),

C("aud_big26",
"""Data Processing Addendum - Tessellate Health Pte. Ltd. (Processor) and Northgate Clinics (Controller), clause 9

"9.1 Processor shall make available to Controller all information reasonably necessary to demonstrate compliance with this Addendum.
9.2 On thirty (30) days' notice, and not more than once in any twelve-month period, Controller or an independent auditor it appoints may inspect Processor's facilities, systems and records relevant to the Processing of Controller Personal Data."

Controller's privacy counsel: "Tag 9.2 in the DPA tracker; 9.1 can wait.\"""",
MAIN + [k for k in ALL_NEAR if k != "SLA"] + ["NONE"], "AUD", 2, t="clause 9.2"),

C("arb_big27",
"""Contract of Affreightment - Tidewater Shipping Co. and Ferrovia Rail Parts GmbH, clause 32

"32. This Contract shall be governed by English law. Any dispute arising out of or in connection with this Contract shall be referred to a tribunal of three members appointed under the Terms of the Tidewater Maritime Association, whose award shall be final and binding, and the parties exclude any right of appeal to the courts on a question of law."

Clause register instruction: each sentence of clause 32 gets its own row. This row is the second sentence.""",
MAIN + ALL_NEAR + ["NONE"], "ARB", 2, t="the second sentence of clause 32"),

C("lol_basis_bargain",
"""Master Services Agreement - Glasswing Security Ltd and Lumenfold Inc., clause 12.6

"12.6 Basis of the Bargain. Customer acknowledges that the fees charged by Glasswing reflect the allocation of risk set out in this Agreement, and that Glasswing would not have entered into this Agreement without the limitations and exclusions in clauses 12.1 to 12.5."

Clauses 12.1 to 12.5 (not quoted) contain the liability cap and the damages exclusions. Tagging instruction for the register: every sub-clause is tagged on its own terms, not by the article it sits in.""",
["LOL", "WD", "IND", "UC", "TWC", "FM", "EA", "NONE"], "NONE", 3, t="clause 12.6"),

C("col_fs_swap",
"""Share Subscription Agreement - Quarry Hill Capital and Lanternmatch Ltd, clause 29

"29. This Agreement and any dispute arising from it are governed by the laws of the Province of Ontario. The courts of Toronto have exclusive jurisdiction over any such dispute."

Deal database instruction: clause 29 is split into one row per sentence. This row is the first sentence of clause 29; the other sentence has a separate row, which a colleague will complete. Use the category definitions exactly as written.""",
["COL", "FS", "ARB", "CAW", "LOL", "ASG", "UC", "NONE"], "COL", 2, t="the first sentence of clause 29",
twin=T([("This Agreement and any dispute arising from it are governed by the laws of the Province of Ontario. The courts of Toronto have exclusive jurisdiction over any such dispute.",
         "The courts of Toronto have exclusive jurisdiction over any dispute arising from this Agreement. This Agreement and any such dispute are governed by the laws of the Province of Ontario.")], "FS")),

C("uc_list_price",
"""Ardent Cloud Systems - Order Form #AC-5520, Commercial Terms

Commit: USD 30,000 per month of compute usage for 24 months.
Committed rate: 22% discount off list price, fixed for the term.
Overage: Usage above the Commit in any month is charged at Ardent's list price in effect at the time of use, as published at ardent.example/pricing, without discount.
Billing: monthly in arrears; invoices payable within 30 days.

FinOps analyst's note: "Tag the Overage line for the contract database before the quarterly cloud review.\"""",
["UC", "AR", "LOL", "TWC", "SLA", "COL", "FM", "NONE"], "UC", 3, t="the Overage line"),

C("twc_bank_close",
"""Quarry Hill Savings - Current Account Terms, section 21 ("Closing your account")

"21.1 You may close your account at any time, and we won't charge you for doing so.
21.2 We may close your account for any reason by giving you at least two months' notice.
21.3 We may close your account immediately if you have seriously or persistently broken these terms, or if we reasonably suspect fraud."

Customer's letter: "You've written to say you're closing my account in two months but you haven't said why. Which section lets you do that?\"""",
["TWC", "TFC", "UC", "CR", "DS", "AR", "DR", "NONE"], "TWC", 2, t="the section the customer is asking about"),

C("cr_storefront",
"""Ember & Oak Marketplace - Seller Performance Standards

"PS-4. If your late-shipment rate exceeds 10% over any rolling 30-day period, we may remove your storefront and listings from search results and category pages for up to 30 days. Your listings will remain reachable by direct link, and existing orders are unaffected.
PS-5. If your late-shipment rate exceeds 25% over any rolling 90-day period, we may close your shop."

Seller's forum post: "My sales dropped to zero overnight and my listings don't show up in search, but my shop still exists and old links work. Which standard is this?\"""",
["CR", "TFC", "TWC", "UC", "LOL", "DS", "PAY", "NONE"], "CR", 3, t="the standard the seller describes"),

C("ds_restaurant",
"""Tablefinch - Diner Terms, section 4 ("When you book")

"When you book a table, we send your name, phone number, party size and any dietary notes you enter to the restaurant so that it can manage your booking. If you opt in, the restaurant may also use your email address to send you its newsletter."

Diner's app-store review: "Two weeks after booking I got texts from the restaurant. Didn't know the app does that."
Editor's task for a consumer guide: tag section 4.""",
["DS", "CONF", "DR", "LIC", "UC", "CR", "NONE"], "DS", 2, t="section 4"),

C("lol_indemnity_cap",
"""Master Services Agreement - Tandem Payroll and Juniper Row Hotels, clause 15.3

"15.3 Each party's total liability under the indemnities in clause 14 shall not exceed two (2) times the fees paid or payable under this Agreement in the twelve (12) months preceding the claim."

Clause 14 (not quoted) contains the mutual indemnities for third-party intellectual property and data breach claims.
Clause 15.1 (not quoted) caps each party's other liability at the fees paid in the prior twelve months.
Contract manager: "Clause 14 is already in the register. Please tag 15.3 next.\"""",
["LOL", "IND", "WD", "FM", "PAY", "NONE"], "LOL", 3, t="clause 15.3"),

C("wd_threats",
"""Glasswing Security - Managed Detection Services Terms, clause 8

"8.1 Glasswing will perform the Services with reasonable skill and care.
8.2 Customer acknowledges that no security service can guarantee protection against all threats. Glasswing does not warrant that the Services will detect every threat, prevent every intrusion, or that Customer's systems will be free of vulnerabilities.
8.3 Glasswing will notify Customer of any confirmed incident within 1 hour."

The customer's cyber-insurance broker asks for every clause of the vendor contract to be tagged. This row is 8.2.""",
["WD", "LOL", "SLA", "IND", "FM", "UC", "TWC", "CONF", "AUD", "NONE"], "WD", 2, t="clause 8.2"),

C("ar_true_up",
"""Nimbus Loop Workspace - Order Form, Seat Terms

"Seat True-Up. If the number of active users in Customer's workspace exceeds the number of purchased Seats on the first day of any month, the additional Seats will be added to this Order automatically and billed pro rata for the remainder of the current Subscription Term at the per-Seat price in this Order."

Customer's IT manager: "Our headcount jumped by about 60 people after the merger, and finance wants to know what we're committed to. Tag the true-up term for our SaaS contract tracker.\"""",
["AR", "UC", "TWC", "LOL", "COL", "DS", "SLA", "NONE"], "NONE", 3, t="the Seat True-Up term"),
]
