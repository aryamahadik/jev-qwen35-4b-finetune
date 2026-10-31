"""Contracts hard items, batch 2: termination without cause, choice of law, arbitration (with near misses)."""
from common import C, Y, S, T

ITEMS = [
# 27 termination on notice with no stated reason (twin: tied to SLA misses)
C("twc_convenience_msa",
"""From: Legal Operations, Corvid Payments
To: Vendor Management
Subject: Kestrel Freight courier MSA - termination rights summary

Team, per the vendor review cadence, below is the termination language from Section 16 of the Kestrel Freight Master Services Agreement (signed 2024; current term ends 31 December 2027). Please confirm the tag so the register reflects our exit options.

"16.2 Either party may terminate this Agreement upon ninety (90) days' prior written notice to the other party. Termination under this Section 16.2 shall not relieve Corvid of its obligation to pay for Services performed before the effective date of termination, and no termination fee shall be payable."

For context, Section 16.1 separately covers termination for material breach with a 30-day cure period, and Section 16.3 lets Corvid terminate immediately if Kestrel loses its operating licence.

Thanks,
Ines Arguello""",
["TWC", "TFC", "AR", "UC", "LOL", "ARB", "COL", "NONE"], "TWC", 2, t="Section 16.2",
twin=T([("Either party may terminate this Agreement upon ninety (90) days' prior written notice to the other party.",
         "Either party may terminate this Agreement upon ninety (90) days' prior written notice to the other party if the other party misses the Service Levels in Schedule 3 in any three consecutive months.")], "TFC")),

# 28 termination on insurance lapse, insolvency, change of control
C("tfc_carrier",
"""Kestrel Freight - Carrier Services Agreement (excerpt)

Clause 19.2: Kestrel may terminate this Agreement immediately upon written notice if Carrier (a) fails to maintain the insurance required by Clause 8, (b) becomes insolvent or makes an assignment for the benefit of creditors, or (c) undergoes a change of control without Kestrel's prior written consent.

Clause 19.3: Upon termination, Carrier shall deliver all shipments in transit to their destination and shall be paid at the contract rates for those shipments.

Contract manager's note: "The carrier's new owners asked whether 19.2 lets us walk away whenever we like. Tag 19.2 in the register first, then I'll reply to them.\"""",
["TWC", "TFC", "ASG", "IND", "LOL", "FM", "AR", "NONE"], "TFC", 2, t="Clause 19.2"),

# 29 discretionary closure with an example reason (twin: only on regional exit)
C("twc_discretion_region",
"""Orchard Lane Tutoring - Family Account Terms, section 11 ("Ending your account")

11.1 You can close your family account at any time from the Billing page. Unused prepaid session credits are refunded if you close within 14 days of purchase.
11.2 Orchard Lane may close your family account at our discretion, including where we decide to stop offering tutoring in your region. If we close your account under this section 11.2, we will give you at least 30 days' notice and refund any unused prepaid session credits.
11.3 We may suspend or close your account immediately if any user on it behaves abusively toward a tutor.

Parent's email to support: "Your letter says you're closing our account under 11.2. We haven't done anything wrong. What kind of clause is 11.2 exactly?\"""",
["TWC", "TFC", "CR", "UC", "DS", "AR", "LOL", "NONE"], "TWC", 3, t="section 11.2",
twin=T([("at our discretion, including where we decide to stop offering tutoring in your region.",
         "only if we decide to stop offering tutoring in your region.")], "TFC")),

# 30 inactivity closure (twin: any wallet at any time)
Y("twc_inactivity",
"""Corvid Payments - Consumer Wallet Agreement, Section 13 (Closing Wallets)

13.1 You may close your Wallet at any time by withdrawing your balance and selecting "Close Wallet" in the app.
13.2 Wallets with no login activity for twenty-four (24) consecutive months may be closed by Corvid after 30 days' email notice. Any remaining balance will be returned to the linked bank account or, if none is linked, held for you under our unclaimed funds procedure.
13.3 We may close your Wallet immediately if we are required to do so by law or by a regulator.

Complaint handler's note: "Customer says her Wallet was shut without cause. The closure letter cites 13.2 only. Need the clause type for the response template.\"""",
"TWC", 0, 3, t="Section 13.2",
twin=T([("Wallets with no login activity for twenty-four (24) consecutive months may be closed by Corvid after 30 days' email notice.",
         "Corvid may close any Wallet at any time after 30 days' email notice.")], 1)),

# 31 customer's own cancel-anytime right
Y("twc_customer_cancel",
"""Brightwell Analytics - Self-Serve Subscription Terms

3. Plans. Plans are billed monthly in advance. Upgrades take effect immediately and are prorated.
4. Cancellation. Subscriber may cancel this subscription at any time, for any reason, through the Billing page. Cancellation takes effect at the end of the current monthly billing period, and no early termination fee applies. Fees already paid are not refunded.
5. Suspension for Non-Payment. If a payment fails and is not resolved within 14 days, Brightwell may suspend access until payment is received.

Comment on the vendor assessment from the purchasing team at Halcyon Dental Group: "We track exit rights. Section 4 is our right, not the vendor's - does it still go in that column?\"""",
"TWC", 1, 2, t="Section 4"),

# 32 fixed term that expires (twin: renews unless notice)
C("twc_expiry",
"""Contract abstract worksheet - Wrenfield Insurance Brokers / Halden Print & Mail Ltd
Agreement: Print and Mail Services Agreement dated 1 April 2025

Field 7 - Term clause (verbatim):
"2.1 This Agreement shall commence on the Effective Date and continue for an initial term of two (2) years, after which it shall expire unless the parties execute a written extension."

Field 8 - Termination clause (verbatim):
"14.1 Either party may terminate this Agreement by written notice if the other party commits a material breach that is not remedied within thirty (30) days of notice."

Field 9 - Notes: Wrenfield's print volumes are expected to fall about 40% in 2027 after the move to e-delivery.

Instruction: assign a category to the Field 7 clause.""",
["TWC", "AR", "TFC", "UC", "COL", "FM", "LOL", "NONE"], "NONE", 3, t="the Field 7 clause",
twin=T([("after which it shall expire unless the parties execute a written extension.",
         "after which it shall renew for successive one-year periods unless either party gives written notice of non-renewal at least sixty (60) days before the end of the then-current period.")], "AR")),

# 33 section locator: client may terminate at any time (twin: only if key personnel leave)
S("twc_sections_consulting",
"""Consulting Agreement - Talvik Advisory LLC (Consultant) and Sundial Learning Trust (Client), Article 10 (Term and Termination)

10.1 Term. This Agreement begins on the Effective Date and ends on 30 June 2027 unless terminated earlier under this Article.
10.2 Termination for Breach. Either party may terminate this Agreement if the other party materially breaches it and fails to cure the breach within thirty (30) days after written notice.
10.3 Client Termination Right. Client may terminate this Agreement, in whole or in part, at any time upon fifteen (15) days' written notice to Consultant, in which case Client shall pay for Services performed through the effective date of termination.
10.4 Termination on Insolvency. Either party may terminate this Agreement immediately if the other party becomes insolvent.
10.5 Survival. Sections 7 (Confidentiality) and 9 (Indemnity) survive termination.""",
["Section 10.1", "Section 10.2", "Section 10.3", "Section 10.4", "Section 10.5"], "TWC", "Section 10.3", 2,
twin=T([("at any time upon fifteen (15) days' written notice to Consultant,",
         "upon fifteen (15) days' written notice to Consultant if the Key Personnel named in Schedule A become unavailable,")], "NONE")),

# 34 developer programme: for any reason or no reason
C("twc_developer_program",
"""Saltmarsh Games Developer Program Agreement - Section 11 (Suspension and Termination)

"We may suspend or terminate your access to the Developer Program, the Developer Portal and any SDK at any time, for any reason or no reason, with or without notice. Upon termination, all licenses granted to you under this Agreement will end, and you must delete all copies of the SDK in your possession. Apps you have already published will remain available on the Saltmarsh Store unless we remove them under Section 12 (App Review)."

Post on the developer forum by an indie studio lead: "Legal wants a one-line label for section 11 before we commit two years of work to this platform. Anyone know what they'd call it?\"""",
["TWC", "CR", "TFC", "UC", "LOL", "DS", "LIC", "NONE"], "TWC", 2, t="section 11"),

# 35 brand may end campaign early with a kill fee
C("twc_kill_fee",
"""Creator Partnership Agreement - Vellora Media creator "Juno Aldana" x Ember & Oak Furniture Co. (Brand)
Campaign: "Rooms that Breathe" (autumn), 4 videos and 6 stories
Fee: $22,000, paid 50% on signing and 50% on publication of the final Deliverable

7. Early End of Campaign. Brand may end this engagement early by written notice to Creator at any time. In that event, Brand will pay the fee for Deliverables already published plus a cancellation fee of 25% of the unpaid remainder, and Creator will have no further obligations.
8. Reputation. Brand may end this engagement immediately if Creator publicly engages in conduct that brings Brand into disrepute, in which case no cancellation fee is payable.
9. Usage Rights. Brand may repost the Deliverables on its own channels for 12 months after publication.""",
["TWC", "TFC", "LOL", "LIC", "UC", "AR", "CONF", "NONE"], "TWC", 3, t="clause 7"),

# 36 insolvency trigger (twin: any reason on 60 days' notice)
Y("twc_insolvency",
"""Distribution Agreement - Halcyon Dental Group Supplies (Distributor) and Redfern Labs (Manufacturer)

Section 18. Termination.
18.1 Either party may terminate this Agreement upon written notice if the other party becomes the subject of any bankruptcy, insolvency, receivership or similar proceeding that is not dismissed within sixty (60) days.
18.2 On termination, Distributor may sell off its remaining inventory of Products for ninety (90) days.
18.3 Termination does not affect any rights that accrued before the termination date.

Reviewer checklist, item 6: "List every termination right in the agreement, with its type." Draft entry for 18.1 is pending.""",
"TWC", 0, 2, t="Section 18.1",
twin=T([("if the other party becomes the subject of any bankruptcy, insolvency, receivership or similar proceeding that is not dismissed within sixty (60) days.",
         "for any reason, provided the notice is given at least sixty (60) days before the termination date.")], 1)),

# 37 termination on reasonable belief of spamming
C("tfc_spam",
"""Nimbus Loop Mail - Acceptable Use and Account Terms

4.1 You may not use Nimbus Loop Mail to send unsolicited bulk messages, to spoof sender addresses, or to distribute malware.
4.2 We may terminate your account if we reasonably believe you have used the service to send unsolicited bulk messages. Where practical, we will first give you an opportunity to explain.
4.3 We may delete messages in your Outbox that our filters identify as malware.

Trust and safety log entry: "Account a1-77f2 terminated. Reason code: 4.2."
Auditor's request: categorise the provision cited in the log entry.""",
["TWC", "TFC", "CR", "DS", "UC", "LOL", "WD", "NONE"], "TFC", 3, t="the provision cited in the log entry"),

# 38 section locator: tenant break right among default, casualty, holdover, renewal request
S("twc_lease_break",
"""Lease abstract request - Unit 12, Ferrovia Business Park (Tenant: Plover Studios Ltd)

Clause 7 (Default). If Tenant fails to pay Rent within 14 days of the due date, Landlord may terminate this Lease by notice.
Clause 8 (Break Right). Tenant may terminate this Lease effective on the last day of the 36th month of the Term by giving Landlord at least six (6) months' prior written notice and paying a break fee equal to three months' Base Rent.
Clause 9 (Casualty). If the Premises are destroyed or made unfit for use by fire or another insured risk and are not reinstated within 9 months, either party may terminate this Lease by notice.
Clause 10 (Holdover). If Tenant remains in possession after expiry, it shall pay 150% of the Base Rent for the holdover period.
Clause 11 (New Lease). Tenant may request a new lease for a further 5 years by notice given no later than 12 months before expiry.""",
["Clause 7", "Clause 8", "Clause 9", "Clause 10", "Clause 11"], "TWC", "Clause 8", 3),

# 39 referral agreement: passing members' contact details to an insurer
C("ds_referral",
"""Referral Agreement - Wrenfield Insurance Brokers and Pinebrook Fitness

1. Referrals. Pinebrook will display Wrenfield's brochure at reception and will pass on to Wrenfield the name, phone number and email address of any member who ticks the "Contact me about health cover" box on the member app.
2. Commission. Wrenfield will pay Pinebrook $40 for each referred member who buys a policy.
3. Duration. This Agreement starts on 1 May 2026 and remains in effect until terminated by either party on sixty (60) days' written notice to the other.
4. Governing Law. This Agreement is governed by the laws of the State of Colorado.

Pinebrook's new operations manager is working through the contract register clause by clause; clause 1 is the next row to fill in.""",
["DS", "CONF", "EXC", "NS", "AR", "TWC", "PAY", "NONE"], "DS", 3, t="clause 1"),

# 40 governing law (twin: exclusive courts)
C("col_newyork",
"""Redline comment thread - Software License Agreement, Brightwell Analytics (Licensor) / Maplecrest Property Management (Licensee)

Section 21.1 (current draft):
"This Agreement and any dispute arising out of or relating to it shall be governed by and construed in accordance with the laws of the State of New York, without regard to its conflict-of-laws rules."

Comment [Licensee counsel, K. Oyelaran]: "We are headquartered in Ohio and would prefer Ohio, but we can live with this if 21.2 stays as drafted."

Section 21.2 (current draft):
"Each party waives any right to a jury trial in any proceeding arising out of this Agreement."

Comment [Licensor counsel, B. Tran]: "Accepted.\"""",
["COL", "FS", "ARB", "CAW", "LOL", "AR", "UC", "NONE"], "COL", 2, t="Section 21.1",
twin=T([("shall be governed by and construed in accordance with the laws of the State of New York, without regard to its conflict-of-laws rules.",
         "shall be heard exclusively in the state and federal courts located in New York County, New York, and each party consents to the personal jurisdiction of those courts.")], "FS")),

# 41 exclusive courts, with "jurisdiction" wording
C("fs_dublin",
"""Nimbus Loop - Terms for Business Customers (EMEA), clause 22

"22. Where disputes are heard. Any legal action or proceeding arising under or relating to these Terms must be brought exclusively in the courts of Dublin, Ireland, and each party irrevocably submits to the jurisdiction of those courts. Nothing in this clause prevents either party from seeking urgent injunctive relief in any competent court."

Email from the customer's in-house lawyer (Ferrovia Rail Parts): "Clause 21 already says Irish law governs. What does clause 22 add, and how should we tag it?\"""",
["COL", "FS", "ARB", "TWC", "DS", "UC", "CAW", "NONE"], "FS", 2, t="clause 22"),

# 42 venue clause when forum selection is not an option
C("col_venue_lease",
"""Residential Lease Rider B - Maplecrest Property Management (Landlord) and tenant Sofia Brandt

B-1. Pets. One cat is permitted. A non-refundable pet fee of $300 is due at move-in.
B-2. Parking. Tenant is assigned space 14. Guest parking is limited to 48 hours.
B-3. Disputes. The exclusive venue for any action arising under this Lease shall be the Circuit Court of Marion County, and the parties waive any objection to venue there.
B-4. Smoke Detectors. Tenant shall test smoke detectors monthly and report faults within 24 hours.

Tenant's question to a legal aid clinic: "Does B-3 mean Indiana law applies to my lease, or is it something else?\"""",
["COL", "ARB", "AR", "TWC", "LOL", "UC", "CAW", "NONE"], "NONE", 3, t="Rider B-3"),

# 43 governing-law sentence inside an arbitration clause (twin: arbitrator qualification)
Y("col_in_arbitration",
"""Joint Development Agreement - Tessellate Health Pte. Ltd. and Redfern Labs, Clause 20 (Dispute Resolution)

20.1 The parties shall first refer any dispute to their respective Chief Technology Officers, who shall meet within 15 days.
20.2 Any dispute not resolved under Clause 20.1 shall be finally resolved by arbitration administered by the Halden Chamber of Arbitration under its Rules in force at the time. The seat of arbitration shall be Singapore and the language English. The tribunal shall decide the dispute in accordance with the substantive law of England and Wales.
20.3 Nothing in this Clause prevents a party from seeking interim relief from a court.

Tagging instruction: sentences within a clause may receive separate tags. This row covers only the final sentence of Clause 20.2.""",
"COL", 1, 3, t="the final sentence of Clause 20.2",
twin=T([("The tribunal shall decide the dispute in accordance with the substantive law of England and Wales.",
         "The tribunal shall consist of a single arbitrator qualified to practise law in England and Wales.")], 0)),

# 44 split consumer governing law; learner asks which section decides
C("col_consumer_split",
"""Sundial Learning - Terms of Use (consumer)

25. Which laws apply
If you are a consumer living in the European Union, the laws of your country of residence apply to these Terms. If you live anywhere else, these Terms are governed by the laws of the Province of Ontario and the federal laws of Canada applicable there. Either way, you keep any rights you have under mandatory consumer law where you live.

26. Where to bring a claim
You may bring a claim in the courts of the place where you live or in the courts of Toronto, Ontario.

Help-centre agent's note: "A learner in Lisbon is asking which section decides whether Portuguese or Canadian rules apply to her subscription. Tag that section before replying.\"""",
["COL", "FS", "ARB", "DS", "UC", "TWC", "CAW", "NONE"], "COL", 3, t="the section the learner is asking about"),

# 45 section locator with misleading headings
S("col_misleading_headings",
"""Master Services Agreement - Glasswing Security Ltd and Plover Streaming Inc., Article 18 (General)
Headings in this Agreement are for convenience only and do not affect its interpretation.

18.1 Notices. All notices shall be in writing and delivered by courier or email to the addresses in Schedule 1.
18.2 Jurisdiction. This Agreement, and any non-contractual obligations arising out of or in connection with it, shall be governed by the law of England and Wales.
18.3 Governing Law and Venue. Each party irrevocably agrees that the courts of London shall have exclusive jurisdiction to settle any dispute arising out of this Agreement.
18.4 Assignment. Neither party may assign this Agreement without the other's prior written consent, not to be unreasonably withheld.
18.5 Severability. If any provision is held invalid, the remainder of this Agreement continues in effect.""",
["Section 18.1", "Section 18.2", "Section 18.3", "Section 18.4", "Section 18.5"], "COL", "Section 18.2", 3),

# 46 statutory-rights savings clause mentioning "the laws of the country"
C("col_statutory_rights",
"""Plover Streaming - Terms of Use, section 14 ("Your consumer rights")

"Nothing in these Terms affects any statutory rights that you have as a consumer under the laws of the country in which you live and which cannot be waived or limited by contract. In particular, if you live in the United Kingdom, you may have rights under consumer protection legislation in relation to digital content that is faulty."

Section 15 of the same Terms, not reproduced here, is a separate clause. Reviewer instruction: tag section 14 only, using the category definitions.""",
["COL", "FS", "LOL", "WD", "UC", "ARB", "DS", "NONE"], "NONE", 3, t="section 14"),

# 47 large option set: governing law with CISG exclusion
C("col_big",
"""Clause-by-clause abstraction - Distribution Agreement between Oxbow Energy Cooperative and Brisa Mobility S.L.
Row 31 of 44

Source text (Clause 27): "The validity, construction and performance of this Agreement, and any claim arising from the relationship it creates, shall be determined under the laws of the Commonwealth of Massachusetts, excluding the United Nations Convention on Contracts for the International Sale of Goods."

Rows 30 and 32 (for context only):
Row 30 - Clause 26: "Disputes shall be heard in the state courts of Suffolk County."
Row 32 - Clause 28: "Notices shall be sent by registered mail to the addresses on the signature page.\"""",
["COL", "FS", "ARB", "CAW", "LOL", "UC", "TWC", "CR", "DS", "AR", "IND", "WD", "FM", "ASG", "CONF", "NOT", "SEV", "NONE"],
"COL", 2, t="Clause 27 (row 31)"),

# 48 interpretation clause without a jurisdiction (twin: Oregon law)
Y("col_plain_meaning",
"""Asset Purchase Agreement - Cobalt Crate Packaging (Seller) and Lumenfold Inc. (Buyer), Section 12.9

"12.9 Construction. This Agreement shall be interpreted according to the plain meaning of its terms, and no rule of strict construction shall be applied against either party on the ground that it drafted the relevant provision. References to Sections are to sections of this Agreement, and the words 'including' and 'includes' mean 'including without limitation'."

Buyer's diligence checklist, line 44: "Governing law - see 12.9?" (entered by a junior associate; needs checking by the supervising lawyer).""",
"COL", 0, 3, t="Section 12.9",
twin=T([("shall be interpreted according to the plain meaning of its terms,", "shall be interpreted according to the laws of the State of Oregon,")], 1)),

# 49 "subject to Scots law"
C("col_scots_forum",
"""ExpatLaw Q&A forum > Germany > Housing

Title: My letting agent's app says "Scots law" - I live in Hamburg??

I rent a flat through Harbourlight Lettings, which I think is based in Edinburgh. Their app terms say, in full: "These Terms, and any non-contractual obligations arising out of or in connection with them, are subject to Scots law." That's the only sentence under the heading "Legal". There's nothing about courts, arbitration or anything else in that part.

Does this mean I have to go to Scotland if there's a problem with my deposit? Or is it about something else entirely? I'm trying to understand what this sentence actually does before I call the tenants' association on Monday.""",
["COL", "FS", "ARB", "UC", "DS", "LOL", "CAW", "NONE"], "COL", 2, t="the sentence under the \"Legal\" heading"),

# 50 non-exclusive jurisdiction line in a term sheet
C("fs_nonexclusive",
"""Facility Agreement - term sheet extract, Quarry Hill Capital (Lender) and Talvik Advisory LLC (Borrower)

Amount: USD 4,500,000 revolving facility
Law: English law.
Courts: Each party irrevocably submits to the non-exclusive jurisdiction of the courts of Singapore, without prejudice to the Lender's right to bring proceedings in any other competent jurisdiction.
Arbitration: None.
Transfers: Lender may transfer its commitments to any bank or financial institution.

Credit officer's comment: "Please tag the Courts line in the facility database before the credit committee meets.\"""",
["COL", "FS", "ARB", "CAW", "LOL", "AR", "ASG", "NONE"], "FS", 3, t="the Courts line"),

# 51 arbitration clause with court-judgment language
C("arb_northbridge",
"""Letter of Intent - binding provisions (Section 9), Tessellate Health Pte. Ltd. and Harbor & Finch Logistics, Inc.

"9.3 Any dispute, controversy or claim arising out of or relating to the binding provisions of this Letter shall be finally settled under the Rules of the Northbridge Arbitration Centre by one arbitrator. The seat shall be Toronto, Ontario. Judgment on the award may be entered by any court having jurisdiction."

"9.4 This Letter shall be governed by the laws of the Province of Ontario."

Tag requested for Section 9.3 only.""",
["ARB", "FS", "COL", "CAW", "LOL", "TWC", "CONF", "NONE"], "ARB", 2, t="Section 9.3"),

# 52 negotiation then non-binding mediation then court (twin: binding arbitration)
C("arb_escalation",
"""Service Agreement - Oxbow Energy Cooperative and Glasswing Security Ltd, Section 23 (Dispute Resolution)

23.1 The parties shall attempt in good faith to resolve any dispute arising under this Agreement through negotiation between executives with authority to settle it.
23.2 If the dispute is not resolved within thirty (30) days after either party's written request for negotiation, either party may refer it to non-binding mediation under the Meridian Dispute Resolution Institute Mediation Procedure, and thereafter either party may commence proceedings in any court of competent jurisdiction.
23.3 Each party shall bear its own costs of the negotiation stage.

Tagging note: Section 23 is tagged as a whole, with one tag.""",
["ARB", "FS", "COL", "LOL", "TWC", "UC", "CAW", "NONE"], "NONE", 3, t="Section 23",
twin=T([("non-binding mediation under the Meridian Dispute Resolution Institute Mediation Procedure, and thereafter either party may commence proceedings in any court of competent jurisdiction.",
         "binding arbitration under the Meridian Dispute Resolution Institute Arbitration Rules, and judgment on the arbitral award may be entered in any court of competent jurisdiction.")], "ARB")),

# 53 arbitration only if both later agree (twin: either party may elect)
Y("arb_opt_in",
"""Framework Agreement - Sundial Learning Trust and Ember & Oak Furniture Co. (school furniture), clauses 30-31

"30.1 If both parties agree in writing after a dispute has arisen, the dispute may be submitted to arbitration before a single arbitrator appointed by the President of the Halden Chamber of Arbitration, whose award shall be final and binding. Absent such agreement, disputes shall be resolved in the courts identified in clause 31."

"31. The courts of England and Wales have exclusive jurisdiction over any dispute not resolved under clause 30.1."

School business manager's question: "Does clause 30.1 mean we're stuck in arbitration if the chairs arrive broken?\"""",
"ARB", 0, 3, t="clause 30.1",
twin=T([("If both parties agree in writing after a dispute has arisen,", "At the written election of either party made after a dispute has arisen,"),
        ("Absent such agreement,", "Absent such an election,")], 1)),

# 54 consumer arbitration with small-claims carve-out and opt-out
C("arb_consumer_optout",
"""Sundial Learning - Terms of Use (US), section 19 (Dispute Resolution), abridged

"19.1 You and Sundial agree to resolve any claims relating to these Terms or the Services through final and binding arbitration before a single arbitrator, except that you may assert claims in small claims court if your claims qualify.
19.2 You may opt out of this agreement to arbitrate by mailing a written notice to Sundial within 30 days after you first accept these Terms. If you opt out, section 20 (Courts) will apply to you.
19.3 The arbitrator may award the same individual relief a court could award."

Parent's email: "I signed my son up three months ago and never sent any notice. Which kind of clause is section 19?\"""",
["ARB", "FS", "CAW", "COL", "UC", "TWC", "LOL", "NONE"], "ARB", 3, t="section 19"),

# 55 standalone class-action waiver in court
C("caw_court",
"""Cobalt Crate Marketplace - Seller Terms, section 21 ("How disputes proceed")

"21.1 To the extent permitted by law, any proceeding to resolve or litigate a dispute in any forum will be conducted solely on an individual basis. Neither you nor Cobalt Crate will seek to have any dispute heard as a class action, consolidated action, or representative action.
21.2 Disputes shall be resolved exclusively in the courts identified in section 22."

Seller community post: "So 21.1 is an arbitration clause, right? That's what someone said on the other thread."
Moderator reply: "Please check the definitions rather than guessing.\"""",
["ARB", "CAW", "FS", "COL", "LOL", "UC", "TWC", "NONE"], "CAW", 3, t="section 21.1"),

# 56 section locator: binding tribunal without the word arbitration (twin: non-binding recommendation)
S("arb_sections_tribunal",
"""Share Purchase Agreement - Talvik Advisory LLC (Seller) and Quarry Hill Capital (Buyer), Article 22 (Disputes)

22.1 Senior Negotiation. The parties' senior executives shall meet within 10 business days of a dispute notice to seek a negotiated resolution.
22.2 Earn-Out Calculation. Disputes about the calculation of any Earn-Out Payment shall be referred to an independent accounting firm acting as an expert and not as an arbitrator, whose determination shall be advisory only.
22.3 Other Claims. All other claims arising out of this Agreement shall be finally resolved under the Rules of the Halden Chamber of Commerce by one tribunal member appointed in accordance with those Rules. The tribunal's award shall be final and binding on the parties, and neither party may bring those claims in any court.
22.4 Interim Relief. Either party may apply to any competent court for interim or conservatory measures.
22.5 Governing Law. This Agreement is governed by the laws of the State of Delaware.""",
["Section 22.1", "Section 22.2", "Section 22.3", "Section 22.4", "Section 22.5"], "ARB", "Section 22.3", 3,
twin=T([("The tribunal's award shall be final and binding on the parties, and neither party may bring those claims in any court.",
         "The tribunal's recommendation shall not bind either party, and either party may afterwards bring those claims in any competent court.")], "NONE")),

# 57 plain arbitration clause, negated question
Y("arb_partner_neg",
"""Brisa Mobility - Fleet Partner Agreement (e-scooter charging partners), Section 17

"17. Binding Arbitration. Any claim or dispute between Partner and Brisa arising out of this Agreement, including disputes about fees paid for charging services, shall be resolved by binding arbitration conducted by a single neutral arbitrator under the Commercial Rules of the Meridian Dispute Resolution Institute. The arbitration shall take place in Austin, Texas. Either party may instead bring an individual action in small claims court for disputes within that court's jurisdiction."

Partner onboarding checklist, row 12: clause type for Section 17 = ______""",
"ARB", 1, 2, t="Section 17", neg=True),

# 58 class waiver attached to arbitration
C("arb_with_class_waiver",
"""Kestrel Freight Consumer Shipping Terms, section 20 (capitals as in the original)

"YOU AND KESTREL AGREE THAT EACH MAY BRING CLAIMS AGAINST THE OTHER ONLY IN YOUR OR ITS INDIVIDUAL CAPACITY AND NOT AS A PLAINTIFF OR CLASS MEMBER IN ANY PURPORTED CLASS OR REPRESENTATIVE PROCEEDING. ANY CLAIM THAT CANNOT BE RESOLVED INFORMALLY SHALL BE RESOLVED BY BINDING INDIVIDUAL ARBITRATION BEFORE A NEUTRAL ARBITRATOR, AND NOT IN COURT. THE ARBITRATOR MAY NOT CONSOLIDATE MORE THAN ONE PERSON'S CLAIMS."

Consumer rights clinic intake form: "Client wants to join the lost-parcels class action. Tag section 20 so the supervising attorney can triage.\"""",
["ARB", "CAW", "FS", "COL", "LOL", "TWC", "UC", "NONE"], "ARB", 3, t="section 20"),

# 59 "final and binding" decision by the provider's own board
Y("arb_internal_decision",
"""Ardent Cloud Systems - Service Level Addendum, section 6 ("Credit Disputes")

"6.1 Customer must request any Service Credit within 30 days after the end of the month in which the Downtime occurred.
6.2 Any dispute concerning whether a Service Credit is owed, or its amount, shall be submitted to Ardent's Customer Success Review Board, which will review the Customer's evidence and Ardent's monitoring data. The Review Board's decision shall be final and binding on the parties with respect to Service Credits.
6.3 Service Credits are Customer's exclusive remedy for Downtime."

Question from the customer's IT director: "It says final and binding - so we can't go to court over credits?\"""",
"ARB", 0, 3, t="Section 6.2"),

# 60 informal resolution period only
C("arb_informal_only",
"""Pinebrook Fitness app - Terms of Use, section 18 ("Talk to us first")

"18. Informal Resolution. Before filing any claim against Pinebrook, you agree to contact us at resolve@pinebrook.example and attempt to resolve the dispute informally for at least 60 days. If we cannot resolve it within that time, you may pursue any remedy available to you."

Member's question in the app chat: "I had a billing problem last month and support told me I have to wait 60 days before doing anything else. So by signing up I've agreed to arbitration?"

Agent's internal note: "Tag section 18 in the knowledge base first so the reply macro quotes the right definition.\"""",
["ARB", "FS", "COL", "CAW", "UC", "TWC", "LOL", "NONE"], "NONE", 2, t="section 18"),
]
