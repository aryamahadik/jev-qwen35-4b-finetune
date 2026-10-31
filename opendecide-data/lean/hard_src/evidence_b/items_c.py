"""Domain C: consumer refund rights (invented statutes)."""
from _h import it

NONE = "none of these"


def dates(month, a, b):
    return [f"{month} {d}" for d in range(a, b + 1)]


ITEMS = [

it("C1", "noul",
   "Was Ingrid's cancellation given within the §22 period?",
   """From: Ingrid Solheim
To: Consumer Protection Office, Province of Arvel
Subject: Did I cancel in time?

A salesman from BrightRoof Solar knocked on my door and I signed a $14,800 contract at my kitchen table on Friday, October 9. I changed my mind and mailed a cancellation letter (registered post) on Wednesday, October 14. BrightRoof says the cooling-off period was already over because five days had passed. For what it's worth, Monday, October 12 was Harvest Day, which is a public holiday here.

Arvel Consumer Contracts Act §22:
(1) A consumer who enters into a contract for $25 or more at a place other than the seller's permanent place of business may cancel it by giving written notice within 3 business days after the day the contract is signed.
(2) "Business day" means any day other than a Sunday or a public holiday.
(3) Notice of cancellation sent by mail is given when it is mailed.
(4) This section does not apply if the consumer requested the seller's visit to make emergency repairs and signed a separate statement waiving the right to cancel.""",
   1,
   card="- business day: any day other than a Sunday or a public holiday\n- cooling-off right: written cancellation within 3 business days after the day an off-premises contract of $25 or more is signed; mailed notice counts when mailed",
   diff=3, twin=[("Monday, October 12 was Harvest Day, which is a public holiday here.",
                  "Monday, October 12 was an ordinary working day here.")], twin_gold=0),

it("C2", "choice",
   "Which items can the customer validly withdraw from and have refunded?",
   """Customer email to Norvik Outfitters (online store)
Order #88213 was placed on February 25 and contained: (1) a rain jacket, (2) wireless earbuds sold in a sealed hygiene pack, and (3) a wristwatch engraved with my initials at my request. The jacket and earbuds arrived on March 1; the watch arrived separately on March 10. I opened the earbud pack to try them. On March 20 I sent you notice that I am withdrawing from the whole order. Please refund everything.

Distance Sales Regulation (Consumer Code, Part 4):
4.1 A consumer may withdraw from a distance contract within 14 days after delivery of the goods. Where goods ordered together are delivered separately, the period runs from delivery of the last item.
4.2 The right of withdrawal does not apply to (a) goods made to the consumer's specifications or clearly personalised, or (b) sealed goods unsuitable for return for health or hygiene reasons that were unsealed after delivery.""",
   "the jacket only",
   opts=["the jacket only", "the jacket and the earbuds", "the jacket and the watch", "all three items", "none of the items"],
   card="- the jacket only: withdrawal is valid for the rain jacket alone\n- the jacket and the earbuds: withdrawal is valid for the jacket and the earbuds\n- the jacket and the watch: withdrawal is valid for the jacket and the engraved watch\n- all three items: withdrawal is valid for the whole order\n- none of the items: the withdrawal is not valid for any item",
   diff=2),

it("C3", "noul",
   "Is dominika_r entitled to cancel under the §9 relocation provision?",
   """Forum: Rosvik Consumer Help > Contracts
Posted by dominika_r

I'm moving from Eastgate to Holloway for work. My gym, IronWorks Fitness, has two clubs: the Elm Street club where I train, and a Riverside club that IronWorks opened in 2024. My new flat is 31 miles from Elm Street but only 18 miles from Riverside. My contract runs another 16 months. IronWorks says I can't cancel. I thought moving away lets you out?

Reply quoting the Rosvik Health Club Services Act §9:
(1) A member may cancel a health club contract if the member moves their residence to a location more than 25 miles from every facility operated by the health club or its affiliates, and provides proof of the new address.
(2) The club may charge a cancellation fee of no more than $50 under this section.""",
   0,
   card="- relocation cancellation right: the member moves to a residence more than 25 miles from every facility the club or its affiliates operate, with proof of the new address",
   diff=1),

it("C4", "choice",
   "What refund is StreamCrate required to give?",
   """Support chat transcript - StreamCrate annual plan
Customer: I was charged $240 on January 1 for another year. I cancelled on February 20. I want my money back for the rest of the year.
Agent: Our renewal reminder email went out on December 28. Our policy is no refunds after 14 days.
Customer: Look up the law.

Vandor Automatic Renewal Act:
§3 For a subscription with an annual term that renews automatically, the business must send the consumer a renewal reminder not less than 15 days and not more than 45 days before the renewal date.
§4 If the business fails to comply with §3, a consumer who cancels within 60 days after the renewal date is entitled to a refund of the fee attributable to each full calendar month of the term remaining after the month in which the consumer cancels.
§5 Independently of §4, a consumer who cancels within 14 days after any renewal is entitled to a full refund.""",
   "$200",
   opts=["$0", "$180", "$200", "$220", "$240"],
   tpl="StreamCrate must refund {}",
   extra={"$0": "StreamCrate owes no refund"},
   diff=3, twin=[("went out on December 28", "went out on December 5")], twin_gold="$0"),

it("C5", "noul",
   "Under §14, does the seller carry the burden of proving the laptop was not faulty at delivery?",
   """Consumer tribunal file - Case CT-4471
Buyer: Rafael Oduya. Seller: Kelm Electronics.
Laptop delivered: February 3. Screen failure first became apparent and was reported to the seller: August 2 of the same year. The seller refused a repair, saying the buyer "must show it was faulty from the start". The buyer says he has done nothing to the laptop beyond normal use.

Glenmoor Sale of Goods Act §14:
(1) Goods must conform to the contract at the time of delivery.
(2) If a lack of conformity becomes apparent within six months after delivery, it is presumed to have existed at delivery, unless the seller proves otherwise.
(3) If a lack of conformity becomes apparent after six months but within two years after delivery, the buyer must prove that it existed at delivery.
(4) The seller must repair, replace, or refund non-conforming goods.""",
   1,
   card="- presumption of non-conformity: a fault that becomes apparent within six months after delivery is presumed to have existed at delivery unless the seller proves otherwise",
   diff=2),

it("C6", "choice",
   "What restocking fee, if any, may ValuVolt keep?",
   """Receipt dispute - Halden Consumer Affairs mediation notes
A customer bought a 65-inch television at ValuVolt for $1,200, opened the box at home, found it worked fine but was too big for the wall, and returned it unused within 7 days. ValuVolt deducted a 15% restocking fee ($180). The in-store shelf tag and the checkout screen made no mention of any restocking fee; the fee policy was printed only on the paper receipt handed over after payment.

Halden Retail Returns Code §5:
(1) A retailer may charge a restocking fee on a returned item only if the fee was disclosed conspicuously to the consumer before the purchase was completed.
(2) Where permitted, a restocking fee may not exceed 15% of the price for opened items and may not be charged at all for unopened or defective items.""",
   "no restocking fee",
   opts=["no restocking fee", "up to 10% of the price", "up to 15% of the price", "up to 25% of the price"],
   card="- no restocking fee: ValuVolt may not keep any restocking fee\n- up to 10% of the price: ValuVolt may keep at most 10% of the price\n- up to 15% of the price: ValuVolt may keep at most 15% of the price\n- up to 25% of the price: ValuVolt may keep at most 25% of the price",
   diff=1),

it("C7", "noul",
   "Could the $20 card lawfully expire after 90 days?",
   """Post on the Seabury Shoppers' Forum
"Last November Tillman's Department Store ran a deal: spend $100 and get a free $20 gift card. I got one. The back of the card says 'Expires 90 days after issue.' When I tried to use it in March, the clerk said it had expired. My sister says gift cards can't expire for five years here. Who's right?"

Seabury Gift Card Act:
§2 A gift card may not have an expiration date earlier than five years after the date it was issued or last loaded with funds.
§3 A dormancy or inactivity fee may be charged only after 12 months of inactivity and only if disclosed on the card.
§4 Sections 2 and 3 do not apply to a card issued as a promotion or reward for which the consumer gave no money or other value specifically for the card, if the expiry date is disclosed on the card.""",
   1,
   card="- promotional card exclusion: a card given as a promotion or reward, for which the consumer paid nothing specifically for the card, with its expiry date disclosed on the card, is outside the five-year rule",
   diff=2),

it("C8", "choice",
   "How much must Solace Tours refund?",
   """Complaint letter - to Solace Tours Ltd.
I booked your "Amber Coast" package (flights, hotel, guided tours) for $3,200. On April 2, 45 days before departure, I cancelled by email because my employer refused my leave request; your office acknowledged it the same day. Nothing unusual was happening at the destination. You have refused any refund at all. Please apply the Package Travel Regulations.

Mervale Package Travel Regulations reg. 12:
(1) A traveller may cancel a package at any time before departure, subject to the following cancellation charges, measured from the date the organiser receives the cancellation:
 (a) more than 60 days before departure: 10% of the package price;
 (b) 30 to 60 days before departure: 50% of the package price;
 (c) fewer than 30 days before departure: 100% of the package price.
(2) No cancellation charge applies if unavoidable and extraordinary circumstances occurring at or near the destination significantly affect the performance of the package.
(3) Refunds are due within 14 days of cancellation.""",
   "$1,600",
   opts=["$0", "$320", "$1,600", "$2,880", "$3,200"],
   tpl="Solace Tours must refund {}",
   extra={"$0": "Solace Tours owes no refund"},
   diff=1),

it("C9", "noul",
   "Is the customer entitled to the $10 credit for the salmon?",
   """Customer complaint - Orwell Fresh Market, store #12
I bought a salmon fillet at the fish counter. The sign said $18.99/kg and the counter clerk weighed it at 0.6 kg, but at checkout I was charged at $21.99/kg. The cashier corrected the price but refused the $10 credit under the scanning code. The code is posted right at the entrance and says "Overcharged? Get $10!" Am I owed the $10?

Tarlow Price Accuracy Code:
1. If the price charged at checkout for an item is higher than its displayed shelf price, the consumer is entitled to the item at the displayed price and a $10 credit, limited to one credit per transaction.
2. The credit in paragraph 1 does not apply to goods priced by weight, volume, or length at the point of sale, although the consumer remains entitled to the displayed price.""",
   0,
   card="- $10 overcharge credit: available when the checkout price exceeds the displayed shelf price, one per transaction, but not for goods priced by weight, volume or length at the point of sale",
   diff=1),

it("C10", "choice",
   "How much must MealMate refund?",
   """Letter of complaint - Dellmont Consumer Rights Bureau
I signed up for MealMate's monthly meal box on MealMate's website. Its terms say cancellations are accepted "by phone only". On March 3 I emailed MealMate's published customer-service address: "Please cancel my subscription effective immediately." MealMate kept charging my card $35 on March 15, April 15 and May 15. I finally got through by phone and cancelled on May 20. How much am I owed?

Dellmont Subscription Fairness Act §6:
(1) A business that allows a consumer to enrol online must allow the consumer to cancel online.
(2) If a business does not comply with (1), any clear request to cancel that the consumer communicates by any reasonable means is effective when received, and the business must refund all charges made after that date.
(3) Email to the business's published customer-service address is a reasonable means.""",
   "$105",
   opts=["$0", "$35", "$70", "$105"],
   tpl="MealMate must refund {}",
   extra={"$0": "MealMate owes no refund"},
   diff=2),

it("C11", "noul",
   "Does Zofia qualify for a buyback or replacement under §4?",
   """Arbitration summary - Keldon Motor Vehicle Warranty Board
Consumer: Zofia Marsh. Vehicle: new "Aster SE" sedan.
Recurring defect: transmission slipping.
Repair history (all for the same defect, all at the selling dealer):
 1. Month 4, odometer 5,200 miles: out of service 12 days.
 2. Month 9, odometer 11,900 miles: out of service 10 days.
 3. Month 17, odometer 18,400 miles: out of service 9 days.
The defect persists. The consumer seeks a buyback, pointing to 31 days out of service.

Keldon Lemon Law §4:
(1) A consumer is entitled to a replacement or refund if, during the protection period, (a) the same defect has been subject to repair four or more times, or (b) the vehicle has been out of service for repair for a cumulative total of 30 or more days.
(2) The protection period is the first 18 months after delivery or the first 18,000 miles, whichever occurs first.
(3) Only repair attempts and days out of service within the protection period are counted.""",
   0,
   card="- lemon-law qualification: within the first 18 months or 18,000 miles (whichever comes first), four or more repairs of the same defect, or 30 or more cumulative days out of service",
   diff=3, twin=[("odometer 18,400 miles", "odometer 17,600 miles")], twin_gold=1),

it("C12", "choice",
   "What is the last day on which the store's refund would still be on time?",
   """Return log and query - Fallowmere Home Goods (online)
A customer withdrew from an order of bedding within the withdrawal period. She shipped the goods back on May 3 and, on May 4, emailed the store a photo of the courier's tracking receipt. The store's warehouse received the parcel on May 9. The customer asks by what date the store must refund her; the store's policy page says "refunds within 14 days of receiving your return".

Fallowmere Consumer Code, Distance Sales Rule 9:
(1) The trader must refund all payments received from the consumer without undue delay and no later than 14 days after the earlier of (a) the day the trader receives the goods back, or (b) the day the consumer supplies evidence of having sent the goods back.
(2) Evidence of sending includes a courier's or post office's tracking receipt.""",
   "May 18",
   opts=dates("May", 5, 31) + ["June 1"],
   tpl="the refund is on time if made on or before {}",
   diff=2, twin=[("and, on May 4, emailed the store a photo of the courier's tracking receipt",
                  "and kept the courier's tracking receipt but never sent it to the store")], twin_gold="May 23"),

it("C13", "noul",
   "Is Callum obliged to make the blender available for collection?",
   """Email to Callum Reyes from "KitchenPro Direct"
"Dear Customer, a VitaBlend 900 blender was delivered to your address in error on June 2. It was ordered by R. Mendes of 14 Alder Row; you live at 41 Alder Row. Our courier will collect it at our expense any weekday this month - please reply with a convenient day."
Callum replied that he considers it an unsolicited gift and intends to keep it.

Lanmark Unsolicited Goods Act:
§1 A person who receives goods that he or she did not order may treat them as an unconditional gift, and is not liable to pay for or return them.
§2 Section 1 does not apply to goods delivered to the wrong recipient by mistake when they were ordered by another person. The recipient must make them available for collection at the sender's expense within a reasonable time after being asked.""",
   1,
   card="- misdelivered goods: goods ordered by someone else and delivered to the wrong recipient by mistake; the recipient must make them available for collection at the sender's expense",
   diff=1),

it("C14", "choice",
   "What is the smallest refund Dorrit's may lawfully give on cancellation?",
   """Layaway cancellation - customer query to Dorrit's Furniture
I put a $120 bookshelf on layaway and have paid $80 so far. I want to cancel. How much do I get back? The store says it keeps a "standard $15 cancellation charge" on every layaway, no matter the price.

Pembury Layaway Act §3:
(1) A consumer may cancel a layaway plan at any time before final payment.
(2) On cancellation, the seller must refund all payments made, less a cancellation charge not exceeding the lesser of $15 or 10% of the price of the goods.
(3) Any cancellation charge above the limit in (2) is void, and the seller must refund the excess.""",
   "$68",
   opts=["$65", "$68", "$72", "$80"],
   tpl="Dorrit's must refund at least {}",
   diff=2),

it("C15", "noul",
   "Is the cardholder's dispute notice timely under §11?",
   """Letter from cardholder to Harbour Crest Bank
I ordered a desk from DeskHaus online for $640 and paid with my Harbour Crest card; it never arrived and DeskHaus has stopped answering. The charge first appeared on my statement dated June 5. I'm writing today, July 30, to dispute it.

Bank's reply (excerpt) citing the Carrow Credit Card Act §11:
(1) A card issuer must investigate and credit a disputed charge for goods not delivered if the cardholder sends the issuer written notice of the dispute no later than 60 days after the date of the first periodic statement on which the charge appeared.
(2) The issuer may not require the cardholder to first seek a refund from the merchant.
(3) Notice is sent on the date the cardholder posts or emails it.""",
   1,
   card="- timely dispute: written notice sent to the issuer no later than 60 days after the date of the first statement showing the charge",
   diff=2, twin=[("I'm writing today, July 30,", "I'm writing today, August 8,")], twin_gold=0),

it("C16", "choice",
   "What is the minimum refund GuardAll must pay?",
   """Service plan cancellation - customer letter to GuardAll Protection Plans
I bought a 3-year GuardAll plan for my washing machine for $360. It has now been exactly 12 months. No claims have been made under the plan. I'd like to cancel. GuardAll says it will refund the unused portion minus a $75 cancellation fee.

Service Contract Act (Territory of Oskar) §8:
(1) A holder may cancel a service contract within 30 days of purchase for a full refund.
(2) After 30 days, the provider must refund the unearned portion of the price, calculated pro rata by months remaining, and may deduct a cancellation fee of no more than $50.
(3) If any claim has been paid under the contract, the provider need not refund anything under (2).""",
   "$190",
   opts=["$0", "$165", "$190", "$240", "$360"],
   tpl="GuardAll must refund at least {}",
   extra={"$0": "GuardAll owes no refund"},
   diff=2),

it("C17", "noul",
   "Was Solveig entitled on March 15 to cancel and recover her full deposit?",
   """Messages summary - Solveig Arnesen and Hearthwood Custom Furniture
- Jan 10: Solveig orders a custom sofa and pays a $2,000 deposit. Written promised delivery date: March 1.
- Feb 1: Solveig asks to change the fabric to a different weave. Hearthwood agrees and notes in writing that the change will delay delivery by 21 days.
- March 15: the sofa has not been delivered. Solveig emails that she is cancelling and demands her full deposit back.

Merrow Consumer Deposits Act §4:
(1) If a seller fails to deliver goods by the delivery date it promised in writing, the consumer may cancel the contract and receive a full refund of any deposit.
(2) If no delivery date was promised, the seller has 30 days after the order.
(3) Where a delay is caused by the consumer's change to the order, the delivery date is extended by the length of that delay.""",
   0,
   card="- late-delivery cancellation right: the consumer may cancel for a full deposit refund once the seller misses its written delivery date, as extended by any delay caused by the consumer's own change to the order",
   diff=2),

it("C18", "choice",
   "What is the last day on which the buyer can cancel under §7?",
   """Buyer's question to the Coral Isles Real Estate Commission
I signed a timeshare purchase contract at the Palm Reach resort on Thursday, July 2, 2026. The resort's public offering statement was not handed to me then; a courier delivered it to my home on Thursday, July 9. What is the last day I can cancel?

Coral Isles Timeshare Act §7:
(1) A purchaser may cancel a timeshare contract, without penalty, by delivering written notice to the developer within 10 calendar days after the later of (a) the date the contract is signed or (b) the date the purchaser receives the public offering statement.
(2) If the last day of the cancellation period falls on a Sunday or a legal holiday, the period is extended to the next day that is neither a Sunday nor a legal holiday.
(3) The only legal holiday in July 2026 is Monday, July 20 (Founders' Day).""",
   "July 21",
   opts=dates("July", 10, 31) + dates("August", 1, 3),
   tpl="the last day to cancel is {}",
   diff=3, twin=[("on Thursday, July 9", "on Wednesday, July 8")], twin_gold="July 18"),

it("C19", "noul",
   "Does §5 require ShopSquare to refund the buyer?",
   """Help thread - ShopSquare Buyer Community
I found a used camera listed on ShopSquare for $480. The seller messaged me through ShopSquare offering a $30 discount if I paid by direct bank transfer instead of through ShopSquare's checkout, so I did. The camera never came. I complained about the seller through ShopSquare's complaint form on May 1 and have heard nothing since. ShopSquare refuses to refund me.

Ellison Online Marketplaces Act §5:
(1) An online marketplace must refund a consumer the price paid for goods bought from a third-party seller on the marketplace if (a) the goods were not delivered, (b) the seller has not resolved the consumer's complaint within 7 days after the consumer reported it through the marketplace, and (c) the consumer paid through the marketplace's own checkout or payment service.
(2) The marketplace may recover the amount from the seller.""",
   0,
   card="- marketplace refund duty: goods not delivered, complaint reported through the marketplace and unresolved after 7 days, and payment made through the marketplace's own checkout or payment service",
   diff=1),

it("C20", "choice",
   "How much must the resort refund?",
   """Guest complaint - Dunmoor Bay Resort (3-night stay)
The booking site showed $189 per night. After I paid, the confirmation page said in small print: "A mandatory resort fee of $35 per night will be collected at check-in." At checkout I was charged $105 in resort fees and $75 for valet parking ($25 a night), which I chose to use. I'd like my money back for both.

Alvor Hospitality Pricing Act §2:
(1) Any mandatory fee not included in the advertised nightly price must be disclosed clearly before the consumer completes the booking.
(2) A mandatory fee not disclosed as required by (1) may not be collected, and if collected must be refunded.
(3) This section does not apply to optional services the consumer chooses to purchase.""",
   "$105",
   opts=["$0", "$75", "$105", "$180"],
   tpl="the resort must refund {}",
   extra={"$0": "the resort owes no refund"},
   diff=1),

it("C21", "noul",
   "May the shop lawfully collect the full $900?",
   """Consumer complaint - Brightwell Auto Repair
Written estimate for brake repair: $800. Final invoice: $900. The shop says the customer authorised the extra cost by phone. The invoice carries this note: "Extra $100 authorised by phone by customer Mrs. Anja Holt, 14 March." The note does not record the time of the call, which took place before the extra work was done.

Tarrow Motor Vehicle Repair Act §6:
(1) A repair shop must give a written estimate for any repair expected to cost more than $100.
(2) The shop may not charge more than the estimate by more than 10% or $50, whichever is less, unless the customer authorises the additional amount before the work is done.
(3) Oral authorisation is valid only if the shop records on the invoice the date and time of the authorisation and the name of the person who gave it.""",
   0,
   card="- valid oral authorisation: given before the work is done and recorded on the invoice with the date, the time and the name of the person authorising",
   diff=2, twin=[("14 March.\" The note does not record the time of the call, which took place before the extra work was done.",
                  "14 March, 11:20 a.m.\" The call took place before the extra work was done.")], twin_gold=1),

it("C22", "choice",
   "What refund is the ticket holder entitled to?",
   """Ticket-holder email to Tillbury Arena
I paid $138 for a concert ticket: $120 face value plus $18 in service fees. The show on June 6 has been rescheduled to July 21 at the same arena. I received the organiser's notice of the new date on May 30 and asked for a refund on June 9. The organiser offered only $120. I want the whole $138.

Marden Event Ticketing Act §4:
(1) If an event is cancelled, the ticket holder is entitled to a full refund, including all fees.
(2) If an event is rescheduled to a date more than 30 days after the original date, the ticket holder may request a refund of the face value within 21 days after receiving notice of the new date.
(3) Fees are refundable under (2) only if the event is also moved to a different city.""",
   "$120",
   opts=["$0", "$18", "$120", "$138"],
   tpl="the ticket holder is entitled to {}",
   extra={"$0": "the ticket holder is entitled to no refund"},
   diff=2),

it("C23", "noul",
   "Is the mover barred from collecting the extra $300?",
   """Moving dispute - Lindqvist Removals, binding estimate
Customer: Omar Haddad. Binding estimate: $2,400 (signed April 2).
On moving day the customer asked the crew to also take an upright piano that wasn't in the estimate. The crew loaded and delivered it. After unloading, the foreman presented a written addendum adding $300 for the piano, which the customer signed. The company then billed $2,700.

Weston Household Goods Carriers Act §12:
(1) A mover that gives a binding estimate may not collect more than the estimated amount, except for additional items or services the customer requests after the estimate is given.
(2) Charges for additional items or services may be collected only if they are set out in a written addendum signed by the customer before the additional items are loaded.""",
   1,
   card="- collectible extra charge: a charge for items or services the customer added after the binding estimate, set out in a written addendum the customer signed before those items were loaded",
   diff=2),

it("C24", "choice",
   "What is the minimum amount Larkspur Barn must refund?",
   """Email to the Holmfirth Consumer Advice Service
We booked Larkspur Barn for our wedding: total price $20,000. We paid $14,000 when we signed, 11 months before the date. We've had to cancel, and we told the venue 60 days before the wedding date. The venue hasn't rebooked the date and says we get nothing back. What does the law say?

Holmfirth Advance Payments Act §5:
(1) If a consumer cancels a contract for services more than 180 days before the scheduled date, the business must refund all advance payments, less a cancellation fee of no more than 10% of the amount paid.
(2) If the consumer cancels 90 to 180 days before the scheduled date, advance payments are refundable only to the extent the business rebooks the date.
(3) If the consumer cancels fewer than 90 days before the scheduled date, advance payments are not refundable, except that any amount paid more than 90 days before the scheduled date in excess of 50% of the total price must always be refunded.""",
   "$4,000",
   opts=["$0", "$1,400", "$4,000", "$12,600", "$14,000"],
   tpl="Larkspur Barn must refund at least {}",
   extra={"$0": "Larkspur Barn need not refund anything"},
   diff=3, twin=[("we told the venue 60 days before", "we told the venue 200 days before")], twin_gold="$12,600"),

it("C25", "noul",
   "Was Brisco required to offer a rain check?",
   """Complaint to the Ashby Trading Standards Office
Brisco Supermarkets' weekly flyer advertised "Olive oil 1L - $6.99, this week only, limited quantities". I went on the first day of the offer at 9 a.m.; the shelf was empty and staff said it had sold out. They refused to give me a rain check, pointing to "limited quantities" in the flyer.

Ashby Advertised Specials Rule:
1. A retailer that advertises a sale item and does not have it available in reasonable quantity must offer a rain check allowing purchase at the advertised price within 30 days.
2. Paragraph 1 does not apply if the advertisement clearly states the minimum quantity available per store (for example, "at least 20 per store").""",
   1,
   card="- rain-check duty: owed when an advertised sale item is not available in reasonable quantity, unless the advertisement clearly stated the minimum quantity available per store",
   diff=1),

it("C26", "choice",
   "What refund does the academy owe?",
   """Refund request - Loom & Lyric Online Academy
I bought the 10-module "Songwriting Foundations" course for $300 on September 1. At checkout I ticked a box saying "I want immediate access to the course." Nothing on the page said anything about losing a right to withdraw. On September 2 I streamed modules 1 to 3. On September 9 I emailed that I was withdrawing. The academy offered $210 (a refund for the 7 unwatched modules).

Sallow Digital Content Regulations:
r.4 A consumer may withdraw from a contract for digital content within 14 days after the contract is made.
r.5 The right in r.4 is lost once supply of the content has begun, but only if the consumer gave express consent to supply beginning during the withdrawal period and acknowledged that the right of withdrawal would be lost.
r.6 If r.5 does not apply and the consumer withdraws, the consumer is not liable to pay for any content supplied during the withdrawal period.""",
   "$300",
   opts=["$0", "$90", "$210", "$300"],
   tpl="the academy owes a refund of {}",
   extra={"$0": "the academy owes no refund"},
   diff=2),
]
