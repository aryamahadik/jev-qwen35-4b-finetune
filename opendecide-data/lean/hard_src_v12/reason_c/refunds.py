"""reason_c / retail returns, refunds and warranties (Corvane Electronics,
Brightwell Home, Fennick & Rowe Appliances, Tallis Auto Supply, Pellmark Outdoor)."""
from _lib import C, Y, T

RETURN_OUT = [
    ("full refund", "refund the full price paid to the original payment method."),
    ("refund less restocking fee", "refund to the original payment method minus the restocking fee."),
    ("store credit only", "issue store credit for the price paid, less any fee that applies; no refund to the payment method."),
    ("exchange only", "the item may be swapped for the same or another item; no refund or credit."),
    ("decline the return", "the request falls outside every return route; nothing is refunded, credited or exchanged."),
    ("refer to warranty service", "the item is outside the return routes but may be covered by the manufacturer's warranty."),
]

ITEMS = [
# ------------------------------------------------------------------ rf01
# why: delivery Tue 1 Sep = day 0; request Thu 1 Oct = day 30 (Sep has 30 days)
# -> inside the 30-day window. Opened, works (not defective) -> 15% restocking fee.
# Twin: Fri 2 Oct = day 31 -> falls in the day 31-45 band -> store credit only.
C("rf01", "Which return outcome applies to this request?",
"""
Corvane Electronics — Returns Procedure RP-3 (rev. June 2026)

1. Window. Count calendar days from the delivery date, which is day 0.
   (a) Day 0 to day 30: refund to the original payment method.
   (b) Day 31 to day 45: store credit only.
   (c) After day 45: no return; direct the customer to the manufacturer's warranty if the item is faulty.
2. Restocking. Opened items that are not defective carry a 15% restocking fee under 1(a) or 1(b). Unopened or defective items carry no fee.
3. Gift cards and downloadable software are non-returnable once activated.
4. Loyalty points earned on a returned purchase are reversed automatically.

Case CR-55180
Customer: Idris Okonjo. Item: Halden 27-inch monitor, paid $319 by debit card.
Delivered: Tuesday 1 September 2026 (carrier scan 14:12).
Return request opened: Thursday 1 October 2026 via web form.
Customer note: "Works perfectly, the colours are fine, I just find it too big for my desk. I opened the box and used it for a couple of weeks. All accessories are here."
Agent check: power-on test passed, no dead pixels, box opened, all accessories present.
""",
RETURN_OUT, "refund less restocking fee", 2,
twin=T([("Thursday 1 October 2026", "Friday 2 October 2026")], "store credit only")),

# ------------------------------------------------------------------ rf02
# why: purchase 14 Mar 2024. Registration 20 May 2024 = 17 days left in March
# (14->31) + 30 (April) + 20 = 67 days > 60 -> no extension; base 24 months ends
# 14 Mar 2026; claim 2 Sep 2026 is after -> not within warranty.
# Twin: registered 7 May 2024 = 17 + 30 + 7 = 54 days -> 36 months -> to 14 Mar 2027 -> within.
Y("rf02", "Is this claim within the warranty period?",
"""
Fennick & Rowe Appliances — Warranty Desk ticket WD-20931

Warranty terms (dishwashers, model years 2023-2025):
- Standard cover: 24 months from the date of purchase shown on the receipt.
- Extended cover: 36 months from the date of purchase if the product is registered online within 60 days of purchase (the purchase date itself is not counted; day 1 is the day after purchase).
- Delivery and installation dates do not change the start of cover.
- Cover is transferable to a new owner of the same property.

Customer record
Name: Maren Castell. Product: F&R QuietLine 45 dishwasher, serial QL45-88120.
Receipt: purchased 14 March 2024, $689, Fennick & Rowe Harrowgate store.
Delivered and installed: 26 March 2024.
Online registration timestamp: 20 May 2024 09:41.
Claim opened: 2 September 2026. Fault: drain pump does not run, error E4.
Customer comment: "I registered it as soon as I found the card in the manual, so I should have the long warranty."
""",
[("Standard cover", "24 months from the purchase date."),
 ("Extended cover", "36 months from the purchase date, available only when the product was registered within 60 days after purchase."),
 ("Within warranty", "the claim date falls inside the cover that applies to this product.")],
0, 2,
twin=T([("20 May 2024 09:41", "7 May 2024 09:41")], 1)),

# ------------------------------------------------------------------ rf03
# why: arrived damaged -> Carrier Claims normally, but footnote: reported more
# than 7 days after delivery -> Returns Desk. Delivered Thu 3 Sep, reported Sat 12 Sep
# = 9 days after -> Returns Desk. Twin: reported Tue 8 Sep = 5 days -> Carrier Claims.
C("rf03", "Which team should this contact be routed to?",
"""
Brightwell Home — Contact routing sheet (customer care, v7)

| Reason on contact | Route to |
| Item arrived damaged (box or product) | Carrier Claims* |
| Wrong item or wrong colour received | Fulfilment Errors |
| Parts or hardware missing | Parts Desk |
| Stopped working within 30 days of delivery | Returns Desk |
| Stopped working after 30 days, product under warranty | Warranty Service |
| Charged twice, wrong amount, refund not received | Billing Support |
| Delivery not received | Delivery Tracing |

*Carrier cut-off: carriers accept damage claims only within 7 days after delivery. If an arrived-damaged contact is made more than 7 days after the delivery date, route it to the Returns Desk instead.

Assembly service bookings go to Home Services; they are not handled by care.

Contact #BH-771402 (chat transcript extract)
Customer (Saturday 12 September 2026): Hi, my glass-top coffee table was delivered on Thursday 3 September. I only unpacked it today because we were away. The outer box has a crushed corner and the glass top has a long crack right across it. All the legs and screws are in the bag. Can you help?
Agent: I'm sorry about that. Can you send photos of the box and the crack?
Customer: Sent.
""",
[("Carrier Claims", "damage-in-transit claims filed against the delivery carrier."),
 ("Fulfilment Errors", "orders where the wrong product, size or colour was sent."),
 ("Parts Desk", "missing parts or hardware sent separately."),
 ("Returns Desk", "returns, refunds and replacements handled by the store, including late-reported damage."),
 ("Warranty Service", "faults after the first 30 days on products still under warranty."),
 ("Billing Support", "charges, double payments and missing refunds."),
 ("Delivery Tracing", "parcels or deliveries that never arrived."),
 ("Home Services", "assembly and installation bookings."),
 ("none of these", "no team on the routing sheet fits the contact.")],
"Returns Desk", 2,
twin=T([("Customer (Saturday 12 September 2026)", "Customer (Tuesday 8 September 2026)"),
        ("I only unpacked it today because we were away.", "I unpacked it this morning.")], "Carrier Claims")),

# ------------------------------------------------------------------ rf04
# why: plan $180/yr = $15/month. Start 1 Feb 2026, cancel 1 Aug 2026. Used months
# Feb, Mar, Apr, May, Jun, Jul = 6 (cancellation takes effect on the 1st, so
# August is unused). Unused = 12 - 6 = 6 -> 6 x 15 = $90, less $20 admin = $70.
# Twin: a claim was paid -> rule 3: no refund -> $0.
C("rf04", "How much should be refunded on the cancelled protection plan?",
"""
Corvane CareShield — Cancellation terms (annual plans bought outright)

1. Cancelling within 30 days of the plan start: full refund, no fee.
2. Cancelling after 30 days: refund = (monthly value x whole unused months) - $20 administration fee. Monthly value = annual price / 12. A month counts as used if any day of it fell before the cancellation effective date. The refund is never below $0.
3. If any claim has been paid under the plan, no refund is due on cancellation.
4. Monthly-billed plans simply stop at the end of the current billing month (not relevant to annual plans).

Cancellation request — CS-40277
Plan: CareShield Annual for Vesta X9 laptop. Price paid: $180, one payment.
Plan start: 1 February 2026. Term: 12 months.
Cancellation effective date: 1 August 2026 (customer sold the laptop).
Claims history: No claims have been made on the plan.
Customer: "I only used it for half a year so I expect half back."
""",
[("$0.00", "no refund is due."),
 ("$55.00", "refund fifty-five dollars."),
 ("$70.00", "refund seventy dollars."),
 ("$75.00", "refund seventy-five dollars."),
 ("$90.00", "refund ninety dollars."),
 ("$180.00", "refund the whole plan price.")],
"$70.00", 3,
twin=T([("No claims have been made on the plan.", "One claim (keyboard replacement, $64) was paid under the plan in April.")], "$0.00")),

# ------------------------------------------------------------------ rf05
# why: purchase 10 Sep; 14 calendar days after (purchase day not counted) ends 24 Sep;
# request 24 Sep -> in time. New price $219 is a regular weekly promotion, not a flash
# sale or clearance -> eligible. Twin: price is a flash sale -> excluded -> no.
Y("rf05", "Does the customer qualify for a price adjustment?",
"""
Pellmark Outdoor — Price Adjustment Policy (stores and online)

If Pellmark lowers its own price on an item within 14 calendar days after you buy it (the purchase day is not counted), we refund the difference on request. The request must be made within the same 14 days.
Not eligible: flash sales (sales lasting 48 hours or less), clearance prices ending in .97, bundle prices, and competitors' prices. One adjustment per item.
Rain checks for out-of-stock sale items are covered by a separate policy.

Store ticket PA-3302
Customer: Soraya Lind. Item: Kestrel 2-person tent, SKU 40-1182.
Bought: 10 September 2026, $249.00, card ending 7714.
New price seen: $219.00 from 22 September 2026, shown in the weekly promotion flyer (runs 22-28 September).
Request made: 24 September 2026 at the Dunmore store customer desk.
Previous adjustments on this item: none.
Note from desk: customer showed the receipt and the flyer page.
""",
[("Price adjustment", "a refund of the difference when Pellmark lowers its own price within the allowed period."),
 ("Flash sale", "a sale lasting 48 hours or less, which is excluded from price adjustments.")],
1, 2,
twin=T([("shown in the weekly promotion flyer (runs 22-28 September)", "shown in a 24-hour online flash sale (22 September only)")], 0)),

# ------------------------------------------------------------------ rf06
# why: precedence: signed amendment > standard trade terms > emails. Amendment
# A-2 gives a 60-day window and 5% restocking for undamaged stock returns. Delivered
# 3 Aug, request 21 Sep: Aug 3->Sep 3 = 31 days, +18 = 49 days <= 60 -> accept with 5%.
# The rep's 90-day email does not override. Twin: request 5 Oct = 31+30+2 = 63 > 60 -> decline.
C("rf06", "How should the trade return request be handled?",
"""
Brightwell Trade — Return request TR-1188 (hospitality account: Harbourline Hotels)

Sources on file:
(1) Standard Trade Terms, clause 9: stock returns accepted within 30 days of delivery; undamaged returns carry a 10% restocking fee.
(2) Signed Amendment A-2 to the Harbourline supply agreement (signed by both parties, 12 January 2026): clause 9 is replaced for this account: returns accepted within 60 days of delivery; undamaged returns carry a 5% restocking fee.
(3) Email from account rep Jonas Pelt to Harbourline, 3 March 2026: "Don't worry, for you guys returns are basically fine up to 90 days, no fee."
Precedence rule (Trade Terms, clause 1.4): a signed amendment prevails over the Standard Trade Terms; emails and verbal statements do not vary the agreement.

Request
Goods: 40 bedside lamps, model Orla, undamaged, original cartons.
Delivered: 3 August 2026.
Return requested: 21 September 2026.
Reason: design change in the refurbishment plan.
""",
[("accept with full credit", "take the goods back and credit the full invoice value."),
 ("accept with 5% restocking fee", "take the goods back and credit the invoice value less 5%."),
 ("accept with 10% restocking fee", "take the goods back and credit the invoice value less 10%."),
 ("decline — outside return window", "the request was made after the applicable return window closed."),
 ("refer to account manager", "the terms on file do not settle the request, so the account manager decides.")],
"accept with 5% restocking fee", 3,
twin=T([("Return requested: 21 September 2026.", "Return requested: 5 October 2026.")], "decline — outside return window")),

# ------------------------------------------------------------------ rf07
# why: gift-receipt returns go to store credit or exchange; refund to the original
# card needs the original purchaser with the purchase receipt. Presenter is a gift
# recipient -> the refusal is correct -> yes (negatively framed question).
# Twin: the purchaser brings the full receipt and the card -> refusal not required -> no.
Y("rf07", "Should the store refuse to refund this return to the original card?",
"""
Brightwell Home — Store Operations Manual, section 4.2 (gift returns)

4.2.1 A return made with a gift receipt is settled as store credit or an exchange.
4.2.2 A refund to the original payment card is only made when the original purchaser presents the full purchase receipt (not a gift receipt) together with the same card used for the purchase.
4.2.3 Items bought with a Brightwell gift card are always refunded to a new gift card.
4.2.4 Seasonal decorations bought after 1 December follow the Holiday Returns notice.

Till log — Hawes Road store, 29 September 2026
Presenter: Alba Resende. Item: Fenwick 4-slice toaster, unused, boxed.
Document shown: gift receipt GR-601-22, which shows the purchase date (9 September 2026) but no price.
Original payment: Visa card ending 3021, held by Thomas Resende (the presenter's uncle).
Presenter request: "My uncle said to put the money back on his card, he told me it's fine."
Thomas Resende is not present; no purchase receipt is shown.
""",
[("Gift receipt", "a receipt without prices given to a gift recipient; returns on it settle as store credit or exchange."),
 ("Card refund conditions", "the original purchaser, the full purchase receipt and the same card must all be presented.")],
1, 2, role="neg",
twin=T([("Presenter: Alba Resende.", "Presenter: Thomas Resende."),
        ("Document shown: gift receipt GR-601-22, which shows the purchase date (9 September 2026) but no price.",
         "Document shown: full purchase receipt 601-22-0914 dated 9 September 2026, $54.99, card ending 3021, plus the card itself."),
        ("Presenter request: \"My uncle said to put the money back on his card, he told me it's fine.\"",
         "Presenter request: \"Please put the money back on my card.\""),
        ("held by Thomas Resende (the presenter's uncle).", "held by Thomas Resende."),
        ("Thomas Resende is not present; no purchase receipt is shown.", "The presenter is the card holder.")], 0)),

# ------------------------------------------------------------------ rf08
# why: repair $210 vs 60% of retail $329 = $197.40 -> repair exceeds -> replace.
# Earlier repair was a different fault (door seal) so the 3rd-failure rule does not
# apply. Twin: estimate $190 < $197.40 -> repair.
C("rf08", "What remedy does the warranty procedure require for this unit?",
"""
Fennick & Rowe — In-warranty remedy procedure (refrigeration)

Step 1. Get the authorised repair estimate (parts + labour).
Step 2. If the estimate is more than 60% of the current retail price of the same model, replace the unit with the same model.
Step 3. If the model is discontinued and no successor exists, refund the purchase price less 2% per full month since purchase.
Step 4. Otherwise repair. Exception: the third failure of the same fault within the warranty period is always replaced, regardless of cost.
Step 5. Cosmetic damage and damage from power surges are not covered (see exclusions).

Case WD-21766
Product: F&R Coolbay 300 fridge-freezer, bought 11 November 2025, still under 24-month warranty.
Current retail price of the Coolbay 300: $329 (model in production).
Fault: compressor does not start; engineer confirmed failed start relay and compressor.
Authorised repair estimate: $210.
Service history: one earlier repair on 2 June 2026 (door seal replaced).
""",
[("repair the unit", "the authorised engineer repairs the fault under warranty."),
 ("replace with the same model", "a new unit of the same model is supplied."),
 ("refund less depreciation", "the purchase price is refunded less 2% per full month since purchase."),
 ("decline — excluded damage", "the fault falls under a warranty exclusion."),
 ("request more information", "the case lacks something the procedure needs to choose a remedy.")],
"replace with the same model", 2,
twin=T([("Authorised repair estimate: $210.", "Authorised repair estimate: $190.")], "repair the unit")),

# ------------------------------------------------------------------ rf09
# why: waiver needs BOTH unopened AND returned within 14 days of delivery.
# Delivered 8 Sep; returned 24 Sep = 16 days -> fee not waived -> no.
# Twin: returned 20 Sep = 12 days -> waived -> yes.
Y("rf09", "Is the restocking fee waived on this return?",
"""
Fennick & Rowe — Large appliance returns (policy LA-2)

- Large appliances (washers, dryers, ranges, fridges, dishwashers) may be returned within 30 days of delivery.
- A 15% restocking fee applies to every large-appliance return.
- The fee is waived only when the appliance is still sealed in its original packaging AND the return pick-up is completed within 14 days of delivery (count calendar days from the day after delivery).
- Haul-away of old appliances is non-refundable once performed.

Return record RA-9052
Product: F&R Tempo 9 kg washer, $749.
Delivered: Tuesday 8 September 2026.
Packaging: sealed, factory tape intact (driver photo attached).
Return pick-up completed: Thursday 24 September 2026.
Reason: customer's laundry niche is 2 cm too narrow.
Haul-away: not booked.
""",
[("Restocking fee", "15% of the price, charged on large-appliance returns."),
 ("Fee waiver", "applies only if the appliance is sealed in original packaging and picked up within 14 days of delivery.")],
0, 2,
twin=T([("Return pick-up completed: Thursday 24 September 2026.", "Return pick-up completed: Sunday 20 September 2026.")], 1)),

# ------------------------------------------------------------------ rf10
# why: cash refunds: amount including tax. $459 x 1.09 = $500.31 > $500 -> head-office
# cheque. Twin: $449 x 1.09 = $489.41 <= $500 -> cash at the register.
C("rf10", "How must this refund be paid out?",
"""
Corvane Electronics — Refund tender rules (store staff)

R1. Card purchases are refunded to the same card.
R2. Cash purchases: refunds up to and including $500.00 (tax included) are paid in cash at the register. Cash refunds above $500.00 are paid by cheque from head office within 10 business days.
R3. Purchases paid with a Corvane gift card are refunded to a new gift card.
R4. Split-tender purchases are refunded to each tender in proportion.
R5. Refunds without a receipt are issued as store credit (see Receiptless Returns).

Return at Kilnworth store, 25 September 2026
Item: Soundmere S7 soundbar, price $459.00, sales tax 9%.
Receipt: yes, dated 19 September 2026. Paid in cash (receipt shows "CASH TENDERED $520.00, CHANGE").
Item condition: unopened. Refund due: price plus tax.
""",
[("refund to the card", "refund to the card used for the purchase."),
 ("cash at the register", "hand the refund over in cash at the till."),
 ("cheque from head office", "head office posts a cheque within 10 business days."),
 ("new gift card", "load the refund on a new Corvane gift card."),
 ("store credit", "issue store credit for the refund amount."),
 ("none of these", "no tender rule covers the refund.")],
"cheque from head office", 2,
twin=T([("price $459.00", "price $449.00")], "cash at the register")),

# ------------------------------------------------------------------ rf11
# why: bought 29 Oct -> standard window 30 days -> last day 28 Nov (Oct 29 + 30).
# Holiday extension covers purchases 1 Nov-24 Dec only, so not extended. Return on
# 5 Dec is after 28 Nov -> not returnable. Twin: bought 2 Nov -> holiday window ->
# returnable until 15 Jan 2027 -> 5 Dec is fine -> yes.
Y("rf11", "Can the customer still return this item for a refund?",
"""
Pellmark Outdoor — Holiday returns notice 2026

Standard rule: unused items may be returned for a refund within 30 days after the purchase date.
Holiday extension: items purchased from 1 November 2026 to 24 December 2026 inclusive may be returned for a refund until 15 January 2027.
Exclusions: personalised items, opened fuel canisters, and swimwear with the hygiene strip removed.
Gift receipts: see the gift returns section of the store manual.

Customer email received 5 December 2026
"Hello, I bought the Arden down jacket (size M, $189) at your Castleford store on 29 October 2026. It's unworn with the tags still on, but my partner bought me the same one. I've got the receipt. I was told returns were extended for the holidays, so I'm hoping I can get my money back. Thanks, Petra Voss"
""",
[("Standard window", "30 days after the purchase date."),
 ("Holiday extension", "purchases made 1 November to 24 December 2026 are returnable until 15 January 2027.")],
0, 2,
twin=T([("store on 29 October 2026", "store on 2 November 2026")], 1)),

# ------------------------------------------------------------------ rf12
# why: third-party battery replacement voids cover for the battery only; the fault
# is battery swelling -> not covered: unauthorised repair. 18 months from 3 Feb 2026
# not expired. Twin: third party replaced screen glass -> battery still covered ->
# covered repair.
C("rf12", "What is the warranty decision for this device?",
"""
Corvane Mobile — Limited warranty, service guide extract

Cover: 18 months from purchase, manufacturing defects only.
Exclusions:
 E1 Accidental damage (drops, cracks, crush).
 E2 Liquid damage (indicator tripped).
 E3 Repairs or part replacements by anyone other than Corvane or an authorised partner void cover for the replaced or repaired component and any fault arising in it. Other components stay covered.
 E4 Cosmetic wear.
Remedy: covered faults are repaired; replacement only if repair is impossible.

Service ticket MS-60411
Device: Corvane Aero 12, purchased 3 February 2026.
Reported fault: battery swelling, back panel lifting (checked in on 21 September 2026).
Liquid indicator: white (not tripped). No cracks or dents.
Technician note: "Internal inspection shows a third-party shop replaced the battery (non-Corvane cell, label 'PX-Cell 4410'). Customer confirms a kiosk at Lowmarket Centre replaced the battery in July. The swelling is in that battery."
""",
[("covered — repair", "the fault is a covered defect and is repaired free."),
 ("covered — replace device", "the fault is covered and the device cannot be repaired, so it is replaced."),
 ("not covered — accidental damage", "exclusion E1 applies."),
 ("not covered — liquid damage", "exclusion E2 applies."),
 ("not covered — unauthorised repair", "exclusion E3 applies to the faulty component."),
 ("not covered — outside warranty period", "the 18-month cover has ended."),
 ("request more information", "the ticket lacks facts needed for a decision.")],
"not covered — unauthorised repair", 2,
twin=T([("a third-party shop replaced the battery (non-Corvane cell, label 'PX-Cell 4410'). Customer confirms a kiosk at Lowmarket Centre replaced the battery in July. The swelling is in that battery.",
         "a third-party shop replaced the screen glass (non-Corvane part). Customer confirms a kiosk at Lowmarket Centre replaced the glass in July. The battery is the original Corvane cell and is the part that is swelling.")],
       "covered — repair")),

# ------------------------------------------------------------------ rf13
# why: bought 15 Mar 2024, failed 20 Sep 2026. Full months 15 Mar 2024 -> 15 Sep 2026
# = 30; the part month (15-20 Sep) counts as a full month -> 31 months in service.
# Past the 18-month free period. Credit = 210 x (60-31)/60 = 210 x 29/60 = 101.50.
# Twin: failed 12 Sep 2026 -> 29 full months (to 15 Aug) + part month = 30 ->
# 210 x 30/60 = 105.00.
C("rf13", "What credit is the customer owed under the battery warranty?",
"""
Tallis Auto Supply — Battery warranty card (Tallis Gold 60)

Free replacement period: first 18 months in service.
Pro-rata period: months 19 to 60. Credit toward a new battery = original price x (60 - months in service) / 60, rounded to the cent.
Months in service: count whole months from the purchase date; any part month counts as a full month.
Not covered: batteries damaged by incorrect charging, cracked cases, or commercial fleet use.
Keep this card with your receipt.

Counter record — Tallis Auto Supply, Brennock branch
Customer: Ruari Doyle. Battery: Tallis Gold 60, serial G60-339104.
Original purchase: 15 March 2024, price $210.00 (receipt produced).
Returned as failed: 20 September 2026. Load test: failed (dead cell). Case intact; private car.
""",
[("$0.00", "no credit is due."),
 ("$98.00", "credit of ninety-eight dollars."),
 ("$101.50", "credit of one hundred and one dollars fifty."),
 ("$105.00", "credit of one hundred and five dollars."),
 ("$108.50", "credit of one hundred and eight dollars fifty."),
 ("free replacement", "a new battery at no charge.")],
"$101.50", 3,
twin=T([("Returned as failed: 20 September 2026.", "Returned as failed: 12 September 2026.")], "$105.00")),

# ------------------------------------------------------------------ rf14
# why: receiptless cap $150 in the 12 months before the return (30 Sep 2025 -
# 29 Sep 2026). Prior: $60 on 3 Nov 2025 and $55 on 14 Feb 2026 are both inside ->
# 60 + 55 + 40 = 155 > 150 -> refused -> no. Twin: first prior on 3 Sep 2025 is outside
# the 12 months -> 55 + 40 = 95 <= 150 -> yes.
Y("rf14", "Can the store accept this receiptless return?",
"""
Brightwell Home — Receiptless returns (policy RR-1)

When no receipt, gift receipt or card lookup can be found, a return may be accepted as store credit if the customer shows photo ID and the customer's receiptless returns in the 12 months before today, plus this return, total no more than $150.00. Returns that exceed the limit are refused. The limit is tracked by ID number.
Items over $100 always need a receipt.
Card lookups: if the item was paid by card, the till can search for the transaction; a found transaction counts as a receipt.

Till record — Wexford Lane, 30 September 2026
Item: Linnet ceramic table lamp, current price $40.00. Customer paid cash (no card to search). No receipt.
ID shown: driving licence ending 4471.
Receiptless history for ID 4471:
- 3 November 2025: $60.00 (bath towels)
- 14 February 2026: $55.00 (cushion set)
""",
[("Receiptless return", "a return with no receipt, gift receipt or card-lookup match, settled as store credit."),
 ("Receiptless limit", "at most $150.00 of receiptless returns, including this one, in the 12 months before the return.")],
0, 3,
twin=T([("- 3 November 2025: $60.00 (bath towels)", "- 3 September 2025: $60.00 (bath towels)")], 1)),

# ------------------------------------------------------------------ rf15
# why: listing says "Sold by Nordvik Trading, shipped by Brightwell"; routing
# footnote: any item sold by a marketplace partner goes to Marketplace Seller Support
# regardless of who shipped it. Twin: sold and shipped by Brightwell, defect in
# 12 days -> Returns Desk.
C("rf15", "Where should the agent route this case?",
"""
Brightwell Home — Online order routing (customer care, v7.2)

- Faulty within 30 days of delivery -> Returns Desk
- Faulty after 30 days, in warranty -> Warranty Service
- Wrong item received -> Fulfilment Errors
- Damaged on arrival, reported within 7 days -> Carrier Claims
- Price or charge query -> Billing Support
Footnote M: Items sold by a marketplace partner (the product page reads "Sold by [partner]") are handled by Marketplace Seller Support for every reason above, even when Brightwell stored and shipped the item.
Footnote P: Contacts from press or social media go to Communications first.

Ticket #BH-782210 (email, 26 September 2026)
Order 5520-1981, delivered 14 September 2026.
Product: Aldersey 3-speed stand fan. Product page line: "Sold by Nordvik Trading, shipped by Brightwell".
Customer: "The fan's oscillation motor makes a grinding noise and stopped turning after a week and a half. The blades still spin. I'd like a replacement or refund."
""",
[("Returns Desk", "store-handled returns, refunds and replacements for faults in the first 30 days."),
 ("Warranty Service", "faults after the first 30 days on products under warranty."),
 ("Fulfilment Errors", "wrong items sent."),
 ("Carrier Claims", "damage-in-transit claims."),
 ("Billing Support", "charge and price queries."),
 ("Marketplace Seller Support", "every contact about items sold by a marketplace partner."),
 ("Communications", "press and social-media contacts."),
 ("none of these", "no route fits.")],
"Marketplace Seller Support", 2,
twin=T([("\"Sold by Nordvik Trading, shipped by Brightwell\"", "\"Sold and shipped by Brightwell\"")], "Returns Desk")),

# ------------------------------------------------------------------ rf16
# why: the item is final-sale (clearance price ending .97) -> no return or exchange
# EXCEPT defective items, which get exchange only. Customer says it's the wrong
# size, not defective -> decline. (No twin.)
C("rf16", "What should the store do with this return?",
"""
Pellmark Outdoor — Returns Policy, clause 6 (final sale)

6.1 Clearance items (price ending in .97) and items marked "Final Sale" cannot be returned, refunded or credited.
6.2 A final-sale item that is defective may be exchanged for the same item; if none is in stock, store credit is issued.
6.3 Items bought at full price follow clause 2 (30-day refund).
6.4 Membership fees are refundable within 14 days of joining.

Return desk note, Dunmore store, 19 September 2026
Customer: Oskar Hale. Item: Tarn trail shoes, size 44, paid $59.97 on 12 September 2026 (receipt shows "CLEARANCE").
Reason given: "They're half a size too small. I wore them round the house once, there's nothing wrong with them."
Staff inspection: soles clean, no faults found.
Same shoe in size 44.5: in stock.
""",
RETURN_OUT, "decline the return", 2),

# ------------------------------------------------------------------ rf17
# why: request 40 days after delivery (Jul 20 -> Aug 29: 11 + 29 = 40) -> past the
# 30-day return route; fault appeared -> manufacturer warranty 12 months -> refer to
# warranty service. Twin: request at day 25 (14 Aug) -> within 30 days, defective ->
# full refund (defective items carry no fee).
C("rf17", "Which outcome does the returns procedure give?",
"""
Corvane Electronics — Returns Procedure RP-3 (summary card for chat agents)

- Within 30 days of delivery (delivery day = day 0): full refund for defective items; 15% restocking fee for opened, working items.
- Day 31 to day 35: store credit only (opened working items also carry the 15% fee).
- After day 35: returns are closed. If the item has a fault and is within the manufacturer's 12-month warranty, send the customer to Warranty Service; otherwise decline.
- Clearance and open-box items: see clause 7 (not relevant here unless tagged).

Chat CR-60233 (29 August 2026)
Customer: My Brisa air fryer, delivered on 20 July, has stopped heating. The display comes on but the basket stays cold.
Agent: Order 88-40912, full price $129, no open-box tag. Delivery confirmed 20 July 2026.
Customer: Can I send it back for my money?
""",
RETURN_OUT, "refer to warranty service", 2,
twin=T([("Chat CR-60233 (29 August 2026)", "Chat CR-60233 (14 August 2026)")], "full refund")),

# ------------------------------------------------------------------ rf18
# why: the sheet covers customer contacts only; this is a supplier chasing payment of
# its own invoice to Brightwell (accounts payable matter) -> no team on the care
# routing sheet fits -> none of these. "Billing Support" handles customers' charges and
# refunds, not supplier invoices. Twin: a customer whose refund has not arrived ->
# Billing Support.
C("rf18", "Under the care routing sheet, where should this contact go?",
"""
Brightwell Home — Customer care routing sheet (v7.3). This sheet covers contacts from retail customers only.

| Contact reason | Team |
| Item arrived damaged, reported within 7 days | Carrier Claims |
| Wrong item, size or colour | Fulfilment Errors |
| Missing parts | Parts Desk |
| Faulty within 30 days | Returns Desk |
| Faulty after 30 days, in warranty | Warranty Service |
| Customer charged twice, wrong amount, refund not received | Billing Support |
| Parcel never arrived | Delivery Tracing |
| Assembly or installation booking | Home Services |
| Gift card balance or activation | Gift Card Team |
| Loyalty points missing | Loyalty Desk |
| Order placed through a marketplace partner | Marketplace Seller Support |

Email received 23 September 2026, subject "Overdue payment — invoice CW-2207"
"Good afternoon, I'm the credit controller at Corwen Woodcraft. We supplied 120 oak side tables to your Kettering distribution centre in July under your purchase order 4471-0932. Our invoice CW-2207 for $14,640 was due on 31 August and remains unpaid. Please let me know when payment will be made. Regards, Imogen Dacre"
""",
[("Carrier Claims", "damage-in-transit claims for customers."),
 ("Fulfilment Errors", "wrong items sent to customers."),
 ("Parts Desk", "missing parts."),
 ("Returns Desk", "customer returns and refunds for early faults."),
 ("Warranty Service", "faults after 30 days under warranty."),
 ("Billing Support", "a customer's charges, double payments and missing refunds."),
 ("Delivery Tracing", "customer parcels that never arrived."),
 ("Home Services", "assembly and installation bookings."),
 ("Gift Card Team", "gift card balances and activation."),
 ("Loyalty Desk", "loyalty points queries."),
 ("Marketplace Seller Support", "orders placed through marketplace partners."),
 ("none of these", "no team on the customer care sheet fits the contact.")],
"none of these", 3,
twin=T([("subject \"Overdue payment — invoice CW-2207\"", "subject \"Refund still not received — order 7720-1144\""),
        ("\"Good afternoon, I'm the credit controller at Corwen Woodcraft. We supplied 120 oak side tables to your Kettering distribution centre in July under your purchase order 4471-0932. Our invoice CW-2207 for $14,640 was due on 31 August and remains unpaid. Please let me know when payment will be made. Regards, Imogen Dacre\"",
         "\"Good afternoon, I returned an oak side table (order 7720-1144) to your Kettering store in July and was told the $122 refund would reach my card within 10 days. It still hasn't arrived and my bank can't see it. Please let me know when it will be paid. Regards, Imogen Dacre\"")],
       "Billing Support")),
]
