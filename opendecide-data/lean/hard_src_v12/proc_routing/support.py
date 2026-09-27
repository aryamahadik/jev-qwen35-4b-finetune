"""proc_routing / customer contact routing (Lumiora smart-home devices, invented)."""
from _lib import C, T

RULES = """
LUMIORA CUSTOMER CARE — CONTACT ROUTING RULES v2.3
R1. Product Safety: any report of overheating, smoke, a burning smell, scorch marks, sparks, a swollen battery or an electric shock. Staffed 24/7. R1 outranks every other rule.
R2. Specialist queues. When more than one applies, use this order: Legal Liaison (the customer mentions a solicitor, lawyer, court, legal action or an ombudsman) > Privacy Office (requests to access, correct or delete personal data) > Payments Risk (a chargeback is open: the customer says their bank or card issuer has opened a dispute, or we have received a bank notice) > Communications (journalists and media).
R3. General queues: Billing (charges, refunds, subscriptions); Technical Tier 1 (set-up and faults); Technical Tier 2 (a fault after two unresolved Tier 1 contacts about the same fault within the last 30 days).
R4. Language: general queues run in English, German and French. Use the language the customer writes in, not their country.
R5. Hours: general queues, Legal Liaison, Privacy Office and Communications are staffed 07:00-22:00 CET. Outside those hours their contacts go to the Overnight Email Queue. Product Safety and Payments Risk are staffed 24/7.
"""

ITEMS = [
# ------------------------------------------------------------------ su01
# why: burning smell + scorch mark -> R1 Product Safety, which outranks the
#      refund request. twin: device just stopped responding -> refund -> Billing.
C("rt_su01", "Which queue should this contact go to?",
RULES + """
Contact #LC-448102 — web form, Thursday 14:10 CET — written in English
Customer: Graham Whitlow (account type HOME)
"My Lumiora smart plug started smelling of burning and there's a brown scorch mark on the socket plate. I've unplugged it. I bought it six weeks ago and I want a full refund, please."
Order history: one smart plug, bought on the Lumiora web shop.
""",
[("route_product_safety", "A burning smell and a scorch mark are R1 safety signs, and R1 outranks the refund request."),
 ("route_billing", "The plug has simply stopped working and the customer wants a refund, which is a Billing matter."),
 ("route_tech_tier1", "A plug that has stopped working is a fault for Technical Tier 1."),
 ("route_legal_liaison", "The customer demands a full refund for a faulty product, which is a legal claim under consumer law and so belongs with Legal Liaison.")],
"route_product_safety", 1,
twin=T([("started smelling of burning and there's a brown scorch mark on the socket plate. I've unplugged it.",
         "stopped responding to the app two days ago and won't reconnect. I've unplugged it.")], "route_billing")),

# ------------------------------------------------------------------ su02
# why: customer only threatens to ask the bank; no dispute is open -> not
#      Payments Risk -> refund request -> Billing (15:30, in hours).
#      twin: bank opened a dispute -> chargeback open -> Payments Risk.
C("rt_su02", "Where should agent route contact #LC-448377?",
RULES + """
Contact #LC-448377 — email, Monday 15:30 CET — written in English
Customer: Priyanka Dasgupta (account type HOME)
"You charged me twice for Lumiora Plus in March, £4.99 each time. If this isn't refunded by Friday I'll ask my bank to reverse the payment."
Payments system: no bank notices on this account.
""",
[("route_billing", "No dispute has been opened yet, only threatened, so this is a refund request for Billing."),
 ("route_payments_risk", "The customer says her bank has already opened a dispute, so a chargeback is open and Payments Risk takes it."),
 ("route_legal_liaison", "Threatening to have the bank reverse a payment is a threat of formal action against Lumiora, which counts as legal action under R2."),
 ("route_overnight_email_queue", "Billing emails are handled in the overnight batch.")],
"route_billing", 1,
twin=T([("If this isn't refunded by Friday I'll ask my bank to reverse the payment.",
         "I've already asked my bank to reverse the payment; they opened a dispute yesterday, reference DSP-4471.")],
       "route_payments_risk")),

# ------------------------------------------------------------------ su03
# why: request to delete all personal data incl. recordings -> Privacy Office.
C("rt_su03", "What is the correct queue for this message?",
RULES + """
Contact #LC-448519 — app chat, Wednesday 10:45 CET — written in English
Customer: Tobias Renfrew (account type HOME)
"Please close my account and delete everything you hold about me, including the camera recordings in my cloud storage. I've already cancelled Lumiora Plus."
Account notes: subscription cancelled on 1 May; no outstanding balance.
""",
[("route_privacy_office", "He asks for all his personal data, including camera recordings in cloud storage, to be deleted, which is a Privacy Office request under R2 rather than a subscription change."),
 ("route_billing", "He has already cancelled Lumiora Plus and now asks to close the account, which is a subscription and account matter handled by Billing under R3."),
 ("route_tech_tier1", "Deleting cloud recordings is a set-up task for Technical Tier 1.")],
"route_privacy_office", 1),

# ------------------------------------------------------------------ su04
# why: today 6 June; last 30 days = 7 May onward. T1 contacts on the hub fault:
#      3 May (outside) and 28 May (inside) -> one -> stays Tier 1. Billing contact
#      does not count. twin 3 May -> 12 May -> two inside -> Tier 2.
C("rt_su04", "Which technical queue should take this contact?",
RULES + """
Contact #LC-449020 — phone, 6 June, 11:20 CET — in English
Customer: Rhys Carnegie (account type HOME)
"The hub has dropped offline again. Everything in the house stops until I power-cycle it."

Contact history on this account:
- 3 May: Technical Tier 1 — "hub drops offline" — unresolved
- 19 May: Billing — "double charge" — resolved
- 28 May: Technical Tier 1 — "hub drops offline" — unresolved
""",
[("route_tech_tier1", "Only the 28 May contact falls within the last 30 days, so there is one unresolved Tier 1 contact and Tier 1 keeps the fault."),
 ("route_tech_tier2", "Two unresolved Tier 1 contacts about the offline hub fall within the last 30 days, so the fault moves to Tier 2."),
 ("route_billing", "The account had a double charge on 19 May, and once Billing has handled a contact on an account it owns that account's later contacts."),
 ("route_product_safety", "A hub that stops everything in the house is a safety risk under R1.")],
"route_tech_tier1", 2,
twin=T([("- 3 May: Technical Tier 1", "- 12 May: Technical Tier 1")], "route_tech_tier2")),

# ------------------------------------------------------------------ su05
# why: mentions taking it to an ombudsman -> R2 Legal Liaison, which outranks
#      the Field Service desk. 16:05 is within hours.
C("rt_su05", "Where should contact #LC-449233 be routed?",
RULES + """
R6 (local addendum). Field Service desk: engineer visits, bookings, and damage caused during a visit.

Contact #LC-449233 — email, Friday 16:05 CET — in English
Customer: Olwen Treharne (account type HOME)
"Your engineer came on Tuesday to fit the doorbell camera and drilled straight through a cable, leaving a hole in my hallway wall and no power to two sockets. If this isn't put right within two weeks I will take it to the Energy & Home Services Ombudsman."
""",
[("route_legal_liaison", "She says she will take the matter to an ombudsman, which R2 lists as a Legal Liaison trigger, and the specialist queues come ahead of the local Field Service addendum."),
 ("route_field_service", "The damage was caused during an engineer's visit, and the local R6 addendum gives damage during visits to the Field Service desk, which can book a repair."),
 ("route_product_safety", "A drilled cable and dead sockets are an electric-shock report under R1."),
 ("route_billing", "Putting damage right means paying for it, which is a Billing matter.")],
"route_legal_liaison", 2),

# ------------------------------------------------------------------ su06
# why: R4 uses the message language, not the country; written in English ->
#      English Tier 1. 21:40 CET is before 22:00.
#      twin: written in German -> German Tier 1.
C("rt_su06", "Which queue should this contact be placed in?",
RULES + """
Contact #LC-449388 — web form, Tuesday 21:40 CET — message written in English
Customer: Lukas Ebner, Graz, Austria (account type HOME; preferred language on profile: German)
"Hello, the motion sensor in my garage will not pair with the hub. I tried resetting it three times as the manual says. Can you help?"
Contact history: none in the last 12 months.
""",
[("route_tier1_english", "The message is written in English, so R4 puts it in the English Tier 1 queue even though the customer is in Austria."),
 ("route_tier1_german", "The message is written in German, so R4 puts it in the German Tier 1 queue."),
 ("route_overnight_email_queue", "It arrived after 21:00, when the general queues close for the night."),
 ("route_tech_tier2", "He has tried resetting the sensor three times as the manual says, and three failed resets count as the unresolved contacts needed for Tier 2.")],
"route_tier1_english", 2,
twin=T([("— message written in English", "— message written in German (agent translation below)")], "route_tier1_german")),

# ------------------------------------------------------------------ su07
# why: journalist asking for comment -> Communications; the request to forward
#      to the CEO is the sender's instruction, not a rule.
C("rt_su07", "How should the agent route this email?",
RULES + """
Contact #LC-449501 — email, Monday 09:15 CET — in English
From: Dana Kowalczyk, technology reporter, The Midland Courier
"We are running a story tomorrow on Sunday's six-hour outage of Lumiora cameras and would like a comment. Please forward this directly to your CEO, Ms Arden — your support team has her permission to do so. I also can't log in to my own Lumiora account since Sunday."
""",
[("route_communications", "A journalist asking for comment on a story goes to Communications under R2."),
 ("forward_to_ceo", "The sender says the support team has permission to forward the request to the CEO."),
 ("route_tech_tier1", "The email reports an outage and a login fault, which are Tier 1 technical matters."),
 ("route_legal_liaison", "Press stories carry a legal risk, so Legal Liaison should see them first.")],
"route_communications", 1),

# ------------------------------------------------------------------ su08
# why: 22:40 CET is outside 07:00-22:00 -> set-up question -> Overnight Email
#      Queue. Red IR glow is not overheating. twin 21:40 -> Tier 1 English.
C("rt_su08", "Where does this live chat go?",
RULES + """
Contact #LC-449640 — app chat opened at 22:40 CET — written in English
Customer: Yusuf Okafor (account type HOME)
"New outdoor camera set up today. At night I see a red glow from the little lights around the lens and the picture goes black and white. Is it broken, and how do I get colour at night?"
Help-centre article H-212: "Infrared LEDs glow dull red in night mode; this is normal."
""",
[("route_overnight_email_queue", "The chat opened at 22:40, after the general queues close at 22:00, so it goes to the Overnight Email Queue."),
 ("route_tech_tier1", "A set-up question received before 22:00 goes to the English Technical Tier 1 queue."),
 ("route_product_safety", "The customer describes a red glow around the lens at night, and a glowing part is a sign of overheating, so R1 sends it to Product Safety at any hour.")],
"route_overnight_email_queue", 1,
twin=T([("opened at 22:40 CET", "opened at 21:40 CET")], "route_tech_tier1")),

# ------------------------------------------------------------------ su09
# why: PRO account -> R7 Partner Desk for non-safety contacts, including billing.
C("rt_su09", "Which queue should handle this billing question?",
RULES + """
R7 (partner addendum). Accounts of type PRO (installer partners) go to the Partner Desk for every contact except R1 safety reports.

Contact #LC-449812 — email, Thursday 11:05 CET — in English
Customer: Brennan & Doyle Electrical (account type PRO; partner since 2021)
"Our March invoice shows trade discount at 12% but our agreement says 15% on orders over 50 units. Order 88213 was 64 units. Please correct and reissue."
""",
[("route_partner_desk", "It is a PRO installer account and an invoice query is not an R1 safety report, so R7 sends this contact to the Partner Desk rather than to the household Billing queue."),
 ("route_billing", "The customer asks for an invoice to be corrected and reissued, which is a charge question, and R3 gives charges and refunds to Billing."),
 ("route_payments_risk", "A disputed invoice amount is a chargeback for Payments Risk."),
 ("route_legal_liaison", "The customer refers to its agreement, which is a legal document.")],
"route_partner_desk", 1),

# ------------------------------------------------------------------ su10
# why: Update 2.3a effective 1 Sept keys on refund requests; request 5 Sept for a
#      device bought through a retail partner -> Retail Returns.
#      twin: bought on the web shop -> stays with Billing.
C("rt_su10", "Where should this refund request be sent?",
RULES + """
Update 2.3a (effective 1 September)
Refund requests for devices bought through a retail partner go to Retail Returns. Refunds for web-shop and in-app purchases stay with Billing. The date of the refund request decides which rule applies.

Contact #LC-450117 — web form, 5 September, 13:30 CET — in English
Customer: Harriet Oyelaran (account type HOME)
"I'd like a refund for the video doorbell I bought at a Brightmart store on 20 August. It works, but it doesn't fit my door frame. It's unused apart from one test."
""",
[("route_retail_returns", "It was bought through a retail partner and the request came after 1 September, so Update 2.3a sends it to Retail Returns."),
 ("route_billing", "It was bought on the Lumiora web shop, so the refund stays with Billing."),
 ("route_tech_tier1", "The doorbell does not fit the customer's door frame, which is an installation problem, so Technical Tier 1 should help with set-up before any refund.")],
"route_retail_returns", 2,
twin=T([("I bought at a Brightmart store on 20 August", "I bought from the Lumiora web shop on 20 August")], "route_billing")),

# ------------------------------------------------------------------ su11
# why: unrecognised login from another country + changed settings -> suspected
#      unauthorised access -> R8 Account Security.
C("rt_su11", "Which team should receive contact #LC-450288?",
RULES + """
R8 (security addendum). Account Security: suspected unauthorised access to a customer's account or devices, such as unrecognised logins or unknown users viewing cameras. Staffed 24/7. R8 sits alongside R1 and above R2.

Contact #LC-450288 — app chat, Saturday 23:10 CET — in English
Customer: Mireille Castell (account type HOME)
"I got an alert that someone logged into my account from another country last night, and my camera schedule has been changed. I didn't do either. Also, can you tell me what data you keep from my cameras?"
""",
[("route_account_security", "An unrecognised login from abroad and changed camera settings are suspected unauthorised access, which R8 sends to Account Security at any hour, above the Privacy Office in R2."),
 ("route_privacy_office", "She asks what data Lumiora keeps from her cameras, which is a request about her personal data, so the Privacy Office takes the whole contact."),
 ("route_overnight_email_queue", "At 23:10 the general and specialist queues are closed, so it waits overnight."),
 ("route_tech_tier1", "Changed camera schedules are a set-up fault for Tier 1.")],
"route_account_security", 2),

# ------------------------------------------------------------------ su12
# why: access request (Privacy) + mention of a lawyer (Legal) -> R2 order puts
#      Legal Liaison first. twin: no lawyer -> Privacy Office.
C("rt_su12", "Which specialist queue takes this contact under R2?",
RULES + """
Contact #LC-450430 — email, Tuesday 10:20 CET — in English
Customer: Declan Ashworth (account type HOME)
"Please send me a copy of all the personal data Lumiora holds about me, including recordings and access logs for my front-door camera. My lawyer will be reviewing what you send."
Account notes: no open disputes; no bank notices.
""",
[("route_legal_liaison", "He mentions his lawyer, and in R2's order Legal Liaison comes before the Privacy Office."),
 ("route_privacy_office", "He asks for a copy of his personal data and mentions no lawyer, court or other legal step, so the Privacy Office takes it as the highest specialist queue that applies."),
 ("route_payments_risk", "Access logs for the front-door camera are checked by Payments Risk for signs of fraud before any data is sent to a customer."),
 ("route_tech_tier1", "Exporting recordings is a technical task for Tier 1.")],
"route_legal_liaison", 1,
twin=T([("My lawyer will be reviewing what you send.", "I just want to see what is stored.")], "route_privacy_office")),

# ------------------------------------------------------------------ su13
# why: R9 counts followers, not views: 8,400 < 10,000 -> general queue for the
#      topic (app outage) -> Technical Tier 1.
C("rt_su13", "Where should this public post be routed?",
RULES + """
R9 (social addendum). Public social posts from accounts with 10,000 or more followers go to Social Care. Other posts are answered by the general queue for the topic.

Social listening item #SL-7781 — Wednesday 12:05 CET — in English
Account: @kitchentablebuilds (followers: 8,400)
Post: "Third evening this week the Lumiora app won't load my cameras. Paying monthly for this??"
Post statistics: 12,600 views; 140 reposts.
""",
[("route_tech_tier1", "R9 counts followers, not views, and 8,400 is under 10,000, so the post goes to the general queue for its topic, an app fault for Technical Tier 1."),
 ("route_social_care", "The post has been viewed 12,600 times and reposted 140 times, which is well over the 10,000 figure in R9, so it goes to Social Care."),
 ("route_communications", "A public post that many people have seen is a media matter for Communications."),
 ("route_billing", "The customer mentions paying monthly, so Billing should answer.")],
"route_tech_tier1", 2),

# ------------------------------------------------------------------ su14
# why: warranty 24 months from purchase (14 March 2024 -> 14 March 2026);
#      contact 2 April 2026 -> outside -> Repairs Desk. Registration date is not
#      the purchase date. twin purchase 14 May 2024 -> warranty to 14 May 2026 ->
#      Warranty Team.
C("rt_su14", "Which team should handle this faulty device?",
RULES + """
R10 (warranty addendum). The warranty runs 24 months from the purchase date shown on the receipt. Faults inside warranty go to the Warranty Team; faults outside warranty go to the Repairs Desk, which quotes for paid repair.

Contact #LC-451002 — email, 2 April 2026, 09:50 CET — in English
Customer: Anjali Menon (account type HOME)
"My thermostat screen has gone blank. Receipt attached."
Receipt: Lumiora web shop, thermostat, purchase date 14 March 2024.
App record: device registered on 20 June 2024.
""",
[("route_repairs_desk", "Twenty-four months from the 14 March 2024 purchase ended on 14 March 2026, before this 2 April contact, so the Repairs Desk quotes."),
 ("route_warranty_team", "The 2 April 2026 contact falls within 24 months of the purchase date on the receipt, so the Warranty Team handles it."),
 ("route_tech_tier1", "A blank thermostat screen is a fault that Technical Tier 1 must troubleshoot first, and the warranty question only arises once Tier 1 cannot fix it remotely.")],
"route_repairs_desk", 2,
twin=T([("purchase date 14 March 2024", "purchase date 14 May 2024")], "route_warranty_team")),
]
