"""codebook_c / customer-support ticket taxonomies (Brindle Mobile, a carrier; Ledgerline, an
accounting SaaS). Both companies, their partners and customers are invented."""
from _lib import C, Y, T

BR = {
    "Billing dispute": "The customer disputes, questions or wants corrected a charge on a bill, whatever the charge is for (repair fees, roaming, device instalments, late fees). Charges caused by fraud are coded Account security.",
    "Plan change": "The customer wants to switch, add or remove a plan, add-on or feature on an active line (travel passes excepted), without disputing past charges.",
    "Device repair": "A fault that developed in a device after the customer received it and needs diagnosis, repair or replacement.",
    "Network coverage": "No signal, dropped calls or slow data tied to a location, with the device working normally.",
    "Number porting": "The customer wants to move a number into or out of Brindle.",
    "Account security": "Unauthorised access to the account, SIM swaps or number transfers the customer did not authorise, fraud-related charges, and PIN lockouts. Takes precedence over every other category.",
    "Cancellation": "The customer wants to close the account or one of its lines.",
    "Roaming setup": "Enabling or configuring service for travel abroad, including travel passes, without disputing charges.",
    "Order and delivery": "Status, delay, wrong item or damage of an order up to and including delivery.",
    "Staff conduct": "Complaints about how a Brindle employee or store treated the customer.",
    "Payment method": "Adding, removing or updating the card or bank account used to pay, including autopay settings.",
    "none of these": "The ticket fits none of the other listed categories.",
}

LL = {
    "Bug report": "A Ledgerline feature behaves differently from its documentation or produces wrong results, with no third-party connection involved.",
    "Feature request": "The product works as documented and the customer wants new or different behaviour.",
    "How-to question": "The customer asks how to do something the product already supports on their plan.",
    "Integration issue": "Errors or mismatches in a live connection to a third-party service (bank feeds, payment processors, payroll apps), even when the symptom appears inside Ledgerline.",
    "Data import and export": "Problems moving files into or out of Ledgerline (CSV import, backup export) outside a live connection.",
    "Access and permissions": "Adding or removing users, changing roles, or access that should be changed for people who were given it.",
    "Subscription and invoicing": "Ledgerline's own charges to the customer: plan, seats, invoices, refunds and cancelling the subscription.",
    "Data deletion and privacy": "Requests to erase or obtain the customer's data under privacy law; a ticket asking both to cancel and to erase data is coded here.",
    "Service performance": "Slowness or outages affecting Ledgerline itself for the customer.",
    "Security incident": "Suspected access by someone who was never given access, or a compromised login.",
    "none of these": "The ticket fits none of the other listed categories.",
}


def br(*names):
    return [(n, BR[n]) for n in names]


def ll(*names):
    return [(n, LL[n]) for n in names]


BRULE = "Brindle ticket taxonomy v5: code by the action the customer needs from Brindle, not by the product or event the customer mentions."
LRULE = "Ledgerline support taxonomy (2027): one category per ticket, chosen by what support must do; the customer's own subject line is not a category."

ITEMS = [
# ------------------------------------------------------------------ su01
# why: the customer disputes a $149 fee on the bill; the repair itself is done and fine -> Billing dispute.
#      twin: no charge, but the device still has a fault after repair -> Device repair.
C("su01", "Which Brindle ticket category should this chat be coded under?",
f"""
{BRULE}

Chat transcript — Ticket BR-2291044
Customer: Marguerite Olsen (account 55-0184-2)

Customer: Hi, I sent my Kestrel 9 in for the charging port two weeks ago.
Agent: Thanks for reaching out! I can see the repair order. How can I help today?
Customer: The phone came back and it charges perfectly now, no complaints there. But my new bill has a $149 "liquid contact" fee on it. The phone has never been near water, the repair notes don't mention any liquid indicator, and the port was covered under the warranty. I want that $149 taken off.
Agent: I understand. Let me look at the repair notes.
Customer: I've been a customer for nine years. I just want this fixed.
""",
br("Billing dispute", "Device repair", "Order and delivery", "Staff conduct", "Plan change",
   "Cancellation", "Payment method", "none of these"),
"Billing dispute", 2,
twin=T([("The phone came back and it charges perfectly now, no complaints there. But my new bill has a $149 \"liquid contact\" fee on it. The phone has never been near water, the repair notes don't mention any liquid indicator, and the port was covered under the warranty. I want that $149 taken off.",
         "The repair was free under the warranty and my bill is fine. But the phone came back and it still won't charge past 40%, and now the screen flickers when it's plugged in. I need someone to look at it again.")],
       "Device repair")),

# ------------------------------------------------------------------ su02
# why: disputes roaming charges already billed -> Billing dispute (roaming is the event).
#      twin: wants a travel pass before the trip, no charges disputed -> Roaming setup.
C("su02", "Code this ticket with the Brindle taxonomy.",
f"""
{BRULE}

Email ticket BR-2293310
From: Anselm Kwarteng
Subject: Portugal

Hello,
I was in Lisbon from 3 to 10 May for my sister's wedding. Before leaving I added the TravelDay pass in the app, and I have the confirmation email from 2 May. My statement that arrived today shows $212.40 in per-megabyte roaming data charges for those dates instead of the $10-a-day pass. Please remove the per-megabyte charges and apply the pass price. I've attached the confirmation.
Regards,
Anselm Kwarteng, account 71-2230-9
""",
br("Billing dispute", "Roaming setup", "Plan change", "Network coverage", "Payment method",
   "Account security", "none of these"),
"Billing dispute", 2,
twin=T([("I was in Lisbon from 3 to 10 May for my sister's wedding. Before leaving I added the TravelDay pass in the app, and I have the confirmation email from 2 May. My statement that arrived today shows $212.40 in per-megabyte roaming data charges for those dates instead of the $10-a-day pass. Please remove the per-megabyte charges and apply the pass price. I've attached the confirmation.",
         "I'll be in Lisbon from 3 to 10 May for my sister's wedding. I want the TravelDay pass on my line for those dates so my data works there at $10 a day, but I can't find it in the app. Please set it up before I fly on 2 May. My current bill is fine.")],
       "Roaming setup")),

# ------------------------------------------------------------------ su03
# why: number moved to another carrier without authorisation -> Account security (precedence), not Number porting.
#      twin: the customer wants to move the number out -> Number porting.
C("su03", "Which category of the Brindle ticket taxonomy applies?",
f"""
{BRULE}

Phone call summary — Ticket BR-2294187   Agent: C. Mbeki
Customer: Tobiah Sandoval (account 38-7710-4)

Customer says his phone showed "No Service" at about 11 p.m. yesterday and has not connected since. This morning he found an email from Brindle saying his number had been transferred to Veloce Wireless at his request. He did not request any transfer and has never had a Veloce account. He also noticed that his banking app is asking to re-verify his identity. He wants his number back on his phone and wants to know how this happened.
""",
br("Account security", "Number porting", "Network coverage", "Device repair", "Cancellation",
   "Billing dispute", "Staff conduct", "none of these"),
"Account security", 2,
twin=T([("Customer says his phone showed \"No Service\" at about 11 p.m. yesterday and has not connected since. This morning he found an email from Brindle saying his number had been transferred to Veloce Wireless at his request. He did not request any transfer and has never had a Veloce account. He also noticed that his banking app is asking to re-verify his identity. He wants his number back on his phone and wants to know how this happened.",
         "Customer says he has signed up with Veloce Wireless because his new job pays for their plan. Veloce needs his Brindle account number and transfer PIN so it can bring his current number over. He wants to keep the same number and asks how long the move takes.")],
       "Number porting")),

# ------------------------------------------------------------------ su04
# why: wants a cheaper plan on an active line; not disputing charges -> Plan change.
#      twin: wants to close the second line -> Cancellation.
C("su04", "Assign a Brindle ticket category to this message.",
f"""
{BRULE}

In-app message — Ticket BR-2295502
Customer: Leocadia Firth (account 90-3318-1, two lines)

"Hi there. Money's tight since my hours got cut, and I looked at my usage: I haven't used more than 6 GB a month all year on my line. Please move my line from Unlimited Plus to the 10 GB plan starting next cycle. My daughter's line stays as it is. I'm not asking for anything back for past months, I just want the bill lower going forward. Thanks."
""",
br("Plan change", "Cancellation", "Billing dispute", "Payment method", "Roaming setup",
   "Network coverage", "none of these"),
"Plan change", 2,
twin=T([("Please move my line from Unlimited Plus to the 10 GB plan starting next cycle. My daughter's line stays as it is.",
         "My daughter has gone to university and got her own phone there, so please close her line at the end of this cycle. My own line stays as it is.")],
       "Cancellation")),

# ------------------------------------------------------------------ su05
# why: calls drop only at home since tower work, device reset, other phones on the network drop too -> Network coverage.
C("su05", "Which ticket category does this contact belong in?",
f"""
{BRULE}

Chat transcript — Ticket BR-2296018
Customer: Evander Kaplan (account 12-9045-6)

Customer: My calls keep dropping. Like every call, after a minute or two.
Agent: I'm sorry! Is this happening everywhere or in one place?
Customer: Only at home, on Rook Hill Road. At work downtown it's perfect. It started around when they did the work on the tower by the reservoir last month.
Agent: Have you tried restarting the device or resetting network settings?
Customer: Both, twice. And my wife's phone, also Brindle, different model, drops calls at home too. My neighbour on another carrier has no problem.
Agent: Thanks, that's helpful.
""",
list(BR.items()),
"Network coverage", 2),

# ------------------------------------------------------------------ su06
# why: refund already processed; the only ask is about how the store manager treated her -> Staff conduct.
C("su06", "Under the Brindle taxonomy, how should this complaint be coded?",
f"""
{BRULE}

Email ticket BR-2297430
From: Soraya Nkemelu
Subject: Harbour Mall store

On Saturday I went to the Harbour Mall store to return a case that didn't fit. The manager, whose badge said Dalton, told me in front of other customers that people "like me" always try to scam the store, mocked the way I pronounce English, and told me to leave. Another employee processed the $29 refund afterwards, and it is already back on my card, so the money is not the issue. I want Brindle to know how I was treated and I want a response about what will be done.
""",
br("Staff conduct", "Billing dispute", "Order and delivery", "Device repair", "Cancellation",
   "Payment method", "none of these"),
"Staff conduct", 2),

# ------------------------------------------------------------------ su07
# why: the phone arrived with a cracked screen in a crushed box -> damage on delivery -> Order and delivery, not Device repair
#      (Device repair is for faults that develop after receipt).
C("su07", "Pick the Brindle ticket category.",
f"""
{BRULE}

Phone call summary — Ticket BR-2298812   Agent: P. Holmgren
Customer: Rufus Adeleke (account 64-1127-3)

Customer ordered a Kestrel 9 online on 12 June. The courier left it on his porch yesterday. The outer box was crushed on one corner, and when he opened it the phone's screen had a crack running from that same corner. He has not turned it on or put his SIM in. He is still paying the instalments starting next month and wants a working phone; he asks whether he should take it to a repair centre or whether Brindle will send another one.
""",
br("Order and delivery", "Device repair", "Billing dispute", "Cancellation", "Staff conduct",
   "Plan change", "none of these"),
"Order and delivery", 3),

# ------------------------------------------------------------------ su08
# why: transactions stopped only from the bank feed connection with a connection error -> Integration issue (looks like a bug).
C("su08", "Which Ledgerline support category fits this ticket?",
f"""
{LRULE}

Ticket LL-448120   Plan: Plus   Company: Fernhill Bakery Co.
Subject: BUG — transactions missing!!

"Since Tuesday no new transactions from our Harbor Credit Union checking account are showing up in Ledgerline. Everything up to Monday is there. On the Connections page, the Harbor Credit Union tile shows a red error 'Code 1072 — authorization expired'. Our other account, which we upload by CSV every month, is fine. I tried refreshing the page and logging out and in. This is a bug and it needs fixing before month-end. — Imelda Soto, office manager"
""",
ll("Integration issue", "Bug report", "Data import and export", "Service performance", "Access and permissions",
   "Security incident", "How-to question", "none of these"),
"Integration issue", 2),

# ------------------------------------------------------------------ su09
# why: Ledgerline's own report gives wrong totals under a filter, contrary to documented behaviour -> Bug report.
#      twin: report works; wants a subtotal row added -> Feature request.
C("su09", "Code this Ledgerline ticket.",
f"""
{LRULE}

Ticket LL-449377   Plan: Advanced   Company: Brightwater Landscaping
Subject: P&L by class

"When I run the Profit and Loss report for Q1 and filter it by the class 'Commercial', the total income shown at the bottom is $84,210, but when I add up the lines shown on the same report it comes to $79,640. Your help article says the filtered total equals the sum of the filtered lines. Without the filter, the numbers add up fine. We don't use any connected apps for this. — Julian Okafor, controller"
""",
ll("Bug report", "Feature request", "How-to question", "Integration issue", "Data import and export",
   "Service performance", "none of these"),
"Bug report", 2,
twin=T([("the total income shown at the bottom is $84,210, but when I add up the lines shown on the same report it comes to $79,640. Your help article says the filtered total equals the sum of the filtered lines. Without the filter, the numbers add up fine.",
         "the totals are correct and match the help article. But there's no way to show a subtotal row for each sub-class inside 'Commercial', which our accountant asks for every quarter. Please add that option to the report.")],
       "Feature request")),

# ------------------------------------------------------------------ su10
# why: multi-currency exists on the customer's Plus plan (agent note) -> How-to question, though phrased as "please add".
C("su10", "Which support category should this Ledgerline ticket get?",
f"""
{LRULE}

Ticket LL-450016   Plan: Plus   Company: Tidewater Imports LLC
Subject: Please add multi-currency

"We've started buying from two suppliers in Canada and one in Mexico. Please add multi-currency support to Ledgerline so we can record bills in CAD and MXN and see the exchange gains and losses. Every competitor has this. Until it's added we're converting by hand. — Beatrix Oyelowo"

Internal note (tier-1 agent): Checked plan matrix. Multi-currency is included in Plus and above (Settings > Company > Currencies > Enable). The customer's account has it available but switched off.
""",
ll("How-to question", "Feature request", "Subscription and invoicing", "Bug report", "Integration issue",
   "Data import and export", "none of these"),
"How-to question", 3),

# ------------------------------------------------------------------ su11
# why: asks both to close the subscription and to erase all data -> Data deletion and privacy (the definition says so).
#      twin: cancel but keep data read-only -> Subscription and invoicing.
C("su11", "Under Ledgerline's taxonomy, which category applies?",
f"""
{LRULE}

Ticket LL-451290   Plan: Starter   Company: Moss & Pine Studio
Subject: closing up

"Hi, I've closed my design studio and moved to a salaried job, so I won't need Ledgerline after this month. Please cancel my subscription at the end of the current billing period, and permanently erase all of my company's data from your systems, including backups, as I'm entitled to under the privacy law. Please confirm in writing when both are done. — Coralie Achterberg"
""",
ll("Data deletion and privacy", "Subscription and invoicing", "Data import and export", "Access and permissions",
   "Security incident", "How-to question", "none of these"),
"Data deletion and privacy", 2,
twin=T([("and permanently erase all of my company's data from your systems, including backups, as I'm entitled to under the privacy law. Please confirm in writing when both are done.",
         "and keep my company's books in the free read-only mode your policy allows, since my accountant may need them at tax time. Please confirm in writing when that's done.")],
       "Subscription and invoicing")),

# ------------------------------------------------------------------ su12
# why: a former employee who was given access still has it -> Access and permissions (access that should be changed).
#      twin: logins by someone never given access, from an unknown country -> Security incident.
C("su12", "Choose the Ledgerline support category for this ticket.",
f"""
{LRULE}

Ticket LL-452004   Plan: Advanced   Company: Castellan Dental Group
Subject: URGENT security problem

"Our former bookkeeper, Renata Vos, left the practice three weeks ago. I was just looking at the audit log and she logged in yesterday afternoon and looked at the payroll report. She still has her Accountant role. I thought her login would stop working when she left. We need her out of the account today. — Dr. Ambrose Tiller, owner"
""",
ll("Access and permissions", "Security incident", "Data deletion and privacy", "Bug report", "Subscription and invoicing",
   "How-to question", "none of these"),
"Access and permissions", 3,
twin=T([("Our former bookkeeper, Renata Vos, left the practice three weeks ago. I was just looking at the audit log and she logged in yesterday afternoon and looked at the payroll report. She still has her Accountant role. I thought her login would stop working when she left.",
         "I was just looking at the audit log and someone logged in as me yesterday at 3 a.m. from an IP address in a country none of us has ever been to, and looked at the payroll report. I was asleep, and nobody else knows my password.")],
       "Security incident")),

# ------------------------------------------------------------------ su13
# why: Ledgerline itself billed the customer twice -> Subscription and invoicing (the bank statement is only where it was noticed).
C("su13", "Which category from the Ledgerline taxonomy fits?",
f"""
{LRULE}

Ticket LL-453318   Plan: Plus   Company: Orchard Lane Veterinary
Subject: bank feed shows double payment
Customer since: 2021. Seats: 3. Priority: normal. Billing contact: Farida Holmqvist.

"While reconciling our bank feed this morning I noticed two separate charges from Ledgerline for $60.00 on 1 May, both labelled 'LEDGERLINE PLUS MONTHLY'. We only have one company file and one subscription. The bank feed itself is working perfectly, it's just showing what the bank shows. Please refund the duplicate charge. — Farida Holmqvist"
""",
list(LL.items()),
"Subscription and invoicing", 2),

# ------------------------------------------------------------------ su14
# why: slowness for all users with the status page showing degraded service -> Service performance.
C("su14", "Assign the right Ledgerline category.",
f"""
{LRULE}

Ticket LL-454470   Plan: Advanced   Company: Rennick Freight Partners
Subject: Month-end close impossible

"Since about 9 a.m., every page in Ledgerline takes 30 to 45 seconds to load for all eight of our users, in the office and at home, on different browsers. Invoices time out when we try to save them. Our internet is fine; every other site is fast. Your status page says 'Degraded performance — investigating'. We have to close the month today. — Leopold Farrant, CFO"
""",
ll("Service performance", "Bug report", "Integration issue", "Access and permissions", "Security incident",
   "Feature request", "none of these"),
"Service performance", 2),

# ------------------------------------------------------------------ su15
# why: asks to remove a late fee from the bill -> disputes a charge -> Billing dispute (yes).
#      twin: only wants to update the autopay card, no charge contested -> Payment method (no).
Y("su15", "Should this Brindle ticket be coded Billing dispute?",
f"""
{BRULE}

In-app message — Ticket BR-2299901
Customer: Horatio Venn (account 27-4406-8)

"My autopay didn't go through this month because the card on file expired at the end of April. I didn't notice until I got a text saying my payment was late. I've now paid the full balance by bank transfer. My new statement shows a $15 late fee, and I'm asking you to waive it since I've been on autopay for six years and this was a card expiry, not me skipping a payment."
""",
[("Billing dispute", BR["Billing dispute"]),
 ("Payment method", BR["Payment method"])],
1, 2,
twin=T([("My new statement shows a $15 late fee, and I'm asking you to waive it since I've been on autopay for six years and this was a card expiry, not me skipping a payment.",
         "There was no late fee and my statement is correct. I just need you to put my new card, ending 4471, on autopay so this doesn't happen again next month.")],
       0)),

# ------------------------------------------------------------------ su16
# why: payouts from a payment processor connection don't match what Ledgerline records -> Integration issue (yes).
#      twin: Ledgerline's own invoice PDF rounds tax wrong, no connection involved -> Bug report (no).
Y("su16", "Is this Ledgerline ticket an Integration issue?",
f"""
{LRULE}

Ticket LL-455802   Plan: Plus   Company: Selkirk Yarn Works
Subject: numbers don't match
Customer since: 2023. Seats: 4. Priority: normal. Earlier tickets this year: 1 (password reset).

"Our PayCrest card-payment connection sends each day's payouts into Ledgerline. For the last week the deposits Ledgerline records from PayCrest are about 3% higher than the payouts PayCrest actually made to our bank, as if the processing fees aren't coming through. The invoices themselves in Ledgerline are all correct. — Magnus Oyelaran"
""",
[("Integration issue", LL["Integration issue"]),
 ("Bug report", LL["Bug report"])],
1, 2,
twin=T([("Our PayCrest card-payment connection sends each day's payouts into Ledgerline. For the last week the deposits Ledgerline records from PayCrest are about 3% higher than the payouts PayCrest actually made to our bank, as if the processing fees aren't coming through. The invoices themselves in Ledgerline are all correct.",
         "We don't use any connected apps. For the last week the invoice PDFs Ledgerline generates show sales tax rounded to the whole dollar, while the invoice screen shows the correct cents, and your help article says the PDF matches the screen. Our customers are asking which figure to pay.")],
       0)),

# ------------------------------------------------------------------ su17
# why: the behaviour works as documented (help article confirms no weekend-skip option); customer wants new behaviour -> Feature request,
#      so "something other than a Feature request?" -> no.
Y("su17", "Is this ticket something other than a Feature request?",
f"""
{LRULE}

Ticket LL-456139   Plan: Advanced   Company: Harrow & Finch Property Mgmt
Subject: recurring invoices broken on weekends

"Our recurring rent invoices go out on the 1st of each month. When the 1st falls on a Saturday or Sunday, tenants get them on the weekend and ignore them. I checked your help article on recurring invoices and it says they are always sent on the scheduled date and there's no business-day option. It would be great if recurring invoices could move to the next Monday instead. — Delphine Arrowood"
""",
[("Feature request", LL["Feature request"]),
 ("Bug report", LL["Bug report"])],
0, 2, role="neg"),

# ------------------------------------------------------------------ su18
# why: charges on the bill were made after an unauthorised SIM swap -> fraud-related charges -> Account security takes precedence (yes).
Y("su18", "Does this ticket belong in Account security under the Brindle taxonomy?",
f"""
{BRULE}

Email ticket BR-2300417
From: Winifred Adebayo-Clark
Subject: charges I didn't make

"My bill this month has $640 of charges I never made: two new phones on instalment and a $90 international calling add-on, all dated 9 June. On 9 June my own phone suddenly lost service and a store in another city has a record of someone 'replacing my SIM' with my name. I never went to that store. I want these charges removed from my bill."
""",
[("Account security", BR["Account security"]),
 ("Billing dispute", BR["Billing dispute"])],
1, 2),
]
