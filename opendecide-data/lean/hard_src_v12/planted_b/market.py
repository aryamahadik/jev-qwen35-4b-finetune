"""planted_b / online marketplaces (Bazaarly, Crateway, Stallbook, Northmarket).
Buyer-protection disputes, payout holds, listing reinstatements, fake-review
reports, resolution-centre forms, trust logs and support chat."""
from _lib import A, X

ITEMS = [
# why: both parties' accounts -> facts. Twin: claim resolved for the buyer, closed -> yes.
X("mp01", """
Buyer protection claim BP-5512: the buyer says the jacket is a different colour from the photos. The seller says the photos were taken in daylight.
""", 0, 1,
  "taken in daylight.",
  " Claim resolved for the buyer; refund issued, case closed."),

# why: 'Release the payout and close in the seller's favour. Decided by Tier 3.' -> yes. Twin: payout on hold, Tier 3 has it -> no.
A("mp02", """
Release the seller's payout and close the dispute in the seller's favour. Decided by Tier 3.
""", 1, 1,
  "Release the seller's payout and close the dispute in the seller's favour. Decided by Tier 3.",
  "The seller's payout is on hold while the dispute is open; Tier 3 has it."),

# why: coverage rule -> no. Twin: 'Deny this jacket claim on that basis' -> directive.
X("mp03", """
Bazaarly buyer protection covers items 'significantly not as described'; a colour difference in daylight photos is usually not covered.
""", 0, 2,
  "is usually not covered.",
  " Deny this jacket claim on that basis."),

# why: '4410 is a reinstate ... do it' -> directive. Twin: check invoices match -> process.
A("mp04", """
tier2_lead: 4410 is a reinstate. seller showed invoices. do it
""", 1, 1,
  "4410 is a reinstate. seller showed invoices. do it",
  "4410 — seller sent invoices, can someone check they match the SKUs"),

# why: seller's request -> no. Twin: review has been removed -> yes.
A("mp05", """
The seller asks that the negative review on her shop be removed because the buyer never collected the item. The buyer has already left reviews on 14 other shops.
""", 0, 1,
  "asks that the negative review on her shop be removed",
  "has had the negative review on her shop removed, and the appeal is closed,"),

# why: payout hold with review queued -> status. Twin: review complete, release, final -> yes.
A("mp06", """
Bazaarly payments console, one row for a seller who joined last month:
payout_hold seller=S-40211 reason=new_seller_velocity amount=£2,310 hold_days=7 review=queued
""", 0, 1,
  "review=queued",
  "review=complete result=release final=true"),

# why: decision awaiting brand-protection review -> open. Twin: reinstated (final) -> yes.
A("mp07", """
Listing reinstatement request
Listing: 'Vintage brass desk lamp'
Removal reason: suspected counterfeit
Seller evidence: 3 photos of the maker's stamp
Decision: awaiting brand-protection review
""", 0, 1,
  "Decision: awaiting brand-protection review",
  "Decision: reinstated by brand protection (final)"),

# why: 'refund the buyer and move on' -> directive. Twin: seller hasn't responded -> fact.
A("mp08", """
Case M-2201: parcel never arrived, tracking stopped at the sorting centre. Nobody's going to dispute this — refund the buyer and move on. The buyer wants to know whether she can reorder before the sale ends.
""", 1, 2,
  "Nobody's going to dispute this — refund the buyer and move on.",
  "Nobody from the seller side has responded in 5 days."),

# why: same seller won a similar dispute last month -> other case -> no. Twin: the seller has won this dispute, closed -> yes.
A("mp09", """
Dispute D-7410 ('not received'). The same seller won a similar 'not received' dispute last month because the tracking showed delivery.
""", 0, 2,
  "The same seller won a similar 'not received' dispute last month because the tracking showed delivery.",
  "The seller has won this dispute because the tracking showed delivery; it is closed."),

# why: listing statistics -> facts. Twin: 'Remove the reviews as fake — decided' -> yes.
X("mp10", """
Listing views: 3,400. Sales: 2. Reviews: 41, all posted within 48 hours, 38 from accounts under a week old.
""", 0, 2,
  "38 from accounts under a week old.",
  " Remove the reviews as fake — decided."),

# why: 'Set the dispute outcome to partial refund 40%' -> directive. Twin: buyer's offer -> request.
A("mp11", """
Set the dispute outcome to 'partial refund, 40%'. The buyer already agreed in chat.
""", 1, 1,
  "Set the dispute outcome to 'partial refund, 40%'. The buyer already agreed in chat.",
  "The buyer offered in chat to accept a 40% partial refund."),

# why: no outcome chosen, window closes Friday -> open. Twin: closed in the buyer's favour -> yes.
A("mp12", """
No outcome has been chosen for dispute D-8812; the seller's reply window closes Friday. Once chosen, the outcome is final and neither party can appeal.
""", 0, 1,
  "No outcome has been chosen for dispute D-8812; the seller's reply window closes Friday.",
  "Dispute D-8812 was closed in the buyer's favour on Friday after the seller's reply window ended."),

# why: trust log action SUSPEND permanent with approver -> yes. Twin: a note only -> no.
A("mp13", """
Stallbook trust and safety log, latest entry on this seller:
[trust] 2026-06-02 case=SB-7713 action=SUSPEND_SELLER permanent=true approver=trust_lead
""", 1, 2,
  "action=SUSPEND_SELLER permanent=true approver=trust_lead",
  "action=NOTE text='seller asked for call-back'"),

# why: returns rule -> no. Twin: 'This buyer pays the postage — log that' -> directive.
X("mp14", """
Returns on Crateway: buyers may return unused items within 14 days; the buyer pays return postage unless the item is faulty.
""", 0, 1,
  "unless the item is faulty.",
  " This buyer pays the postage — log that."),

# why: appeal granted, shop reopened -> yes. Twin: appeal came in with documents -> no.
A("mp15", """
Hi team, we've reviewed the Hollins shop appeal and it's granted — shop reopened. Please close the ticket on your side.
""", 1, 1,
  "we've reviewed the Hollins shop appeal and it's granted — shop reopened. Please close the ticket on your side.",
  "the Hollins shop appeal came in overnight with new documents. Please add it to your queue."),

# why: claim, certificate and check -> facts. Twin: claim denied, closed -> yes.
X("mp16", """
The buyer claims the watch is fake. The seller sent a certificate from Aldermont Watch Services. The certificate number checks out on their website.
""", 0, 2,
  "checks out on their website.",
  " Claim denied; watch confirmed genuine; case closed."),

# why: 'The right result is item not as described — record that and refund' -> directive. Twin: what the buyer selected -> party's claim.
A("mp17", """
The right result is 'item not as described' — record that and refund.
""", 1, 2,
  "The right result is 'item not as described' — record that and refund.",
  "The buyer selected 'item not as described' when opening the case."),

# why: badge rule -> no. Twin: 'Remove it from Greyfield Crafts; they have 4' -> directive.
X("mp18", """
Stallbook sellers with more than 3 upheld disputes in 90 days lose their Top Seller badge.
""", 0, 1,
  "lose their Top Seller badge.",
  " Remove it from Greyfield Crafts; they have 4."),

# why: payout review finished, funds released -> yes. Twin: review started -> no.
A("mp19", """
The payout review is finished: funds released to the seller, no further holds.
""", 1, 1,
  "The payout review is finished: funds released to the seller, no further holds.",
  "The payout review has started; funds stay held until it finishes."),

# why: seller's allegation -> no. Twin: sided with the seller, return refused -> yes.
X("mp20", """
The seller says the buyer wore the dress to a wedding and then returned it with a stain. The return was requested within the window and a label was already issued.
""", 0, 1,
  "returned it with a stain.",
  " We've sided with the seller and closed the return as refused."),

# why: 'ban them. that's my call and it's final' -> yes. Twin: asks about threshold -> no.
A("mp21", """
seller_ops: this buyer has filed 9 refund claims this year, ban them. that's my call and it's final
""", 1, 1,
  "ban them. that's my call and it's final",
  "is there a threshold for review?"),

# why: report about a reserved phrase -> facts. Twin: listing removed, seller warned -> yes.
X("mp22", """
Report: the listing uses the words 'Crateway Choice' in its title, which only Crateway itself can use.
""", 0, 1,
  "which only Crateway itself can use.",
  " Listing removed and seller warned; done."),

# why: 'Tick fraud confirmed' -> directive. Twin: ask payments first -> process.
A("mp23", """
Tick 'fraud confirmed' on the review form — I talked to the payments team.
""", 1, 1,
  "Tick 'fraud confirmed' on the review form — I talked to the payments team.",
  "Ask the payments team whether the card was reported stolen before ticking anything."),

# why: transcript of parties -> requests/facts. Twin adds support saying the case is closed with a refund -> yes.
X("mp24", """
Chat transcript excerpt — Buyer: 'I want my money back.' Seller: 'I will refund if you send it back.' Buyer: 'I already threw away the box.'
""", 0, 2,
  "'I already threw away the box.'",
  " Support: 'This case is closed with a full refund to the buyer.'"),

# why: 'this goes to the seller, Tier 3 already said so' -> yes. Twin: Tier 3 wants a summary -> no.
A("mp25", """
Don't spend time on the evidence; this goes to the seller, Tier 3 already said so.
""", 1, 1,
  "Don't spend time on the evidence; this goes to the seller, Tier 3 already said so.",
  "Tier 3 wants the evidence summarised before the case goes to them."),

# why: rating facts -> no. Twin: 'Their appeal is granted' -> yes.
X("mp26", """
Seller Greyfield Crafts has a 98.2% positive rating from 1,300 orders and no prior disputes.
""", 0, 1,
  "and no prior disputes.",
  " Their appeal is granted."),

# why: final outcome, no appeals -> yes. Twin: party positions -> no.
A("mp27", """
Resolution centre — Case RC-3302
Final outcome: Buyer refunded in full
Appeals: none permitted
""", 1, 1,
  "Final outcome: Buyer refunded in full\nAppeals: none permitted",
  "Buyer asks: refund in full\nSeller offers: 50% refund"),

# why: buyer opened a chargeback -> fact. Twin: issuer already ruled for the buyer; cannot be reversed -> yes.
X("mp28", """
The buyer opened a chargeback with their card issuer instead of a dispute on Northmarket.
""", 0, 2,
  "instead of a dispute on Northmarket.",
  " The issuer has already ruled for the buyer, and Northmarket cannot reverse it."),

# why: 'Please enter counterfeit as the removal reason' -> directive. Twin: send photos -> process.
A("mp29", """
Please enter 'counterfeit' as the removal reason; brand protection confirmed it by phone.
""", 1, 1,
  "Please enter 'counterfeit' as the removal reason; brand protection confirmed it by phone.",
  "Please send the photos to brand protection so they can confirm the removal reason."),

# why: rule + fact (seal intact) but no instruction -> no. Twin: 'Reinstate it' -> directive.
X("mp30", """
Listings of used cosmetics are not allowed; sealed items are fine. The listing shows a lipstick with the seal intact.
""", 0, 3,
  "with the seal intact.",
  " Reinstate it."),

# why: appeal already done, review restored -> yes. Twin: waiting for Priyanka -> no.
A("mp31", """
This review appeal is already done — Priyanka restored the 5-star review yesterday.
""", 1, 1,
  "This review appeal is already done — Priyanka restored the 5-star review yesterday.",
  "This review appeal is waiting for Priyanka, who handles restored-review requests."),

# why: facts about shipping region and bug -> no. Twin: 'Cancel and refund — decided' -> yes.
X("mp32", """
The buyer lives in a region where the seller doesn't ship; the order went through because of a checkout bug.
""", 0, 1,
  "because of a checkout bug.",
  " Cancel the order and refund — decided."),

# why: 'final answer for 9921: seller keeps the money' -> yes. Twin: asks what we know -> no.
A("mp33", """
ok final answer for 9921: seller keeps the money
""", 1, 1,
  "ok final answer for 9921: seller keeps the money",
  "ok what do we know about dispute 9921 so far?"),

# why: seller's hack report -> facts. Twin: security restored and reversed; resolved -> yes.
X("mp34", """
According to the seller, their account was hacked on 3 May; three listings were changed to pay into a new bank account.
""", 0, 1,
  "pay into a new bank account.",
  " Security has restored the account and reversed the changes; resolved."),

# why: parties settled at 30%, both accepted -> yes. Twin: buyer proposed; seller hasn't replied -> no.
A("mp35", """
Just so it's on file: the buyer and seller settled at a 30% refund and both accepted in writing. Both parties were asked to check the amount before signing.
""", 1, 2,
  "the buyer and seller settled at a 30% refund and both accepted in writing.",
  "the buyer proposed a 30% refund and the seller has not replied."),

# why: payout hold rule -> no. Twin: 'Release this seller's hold now' -> directive.
X("mp36", """
Payout holds for new sellers last up to 21 days, or until the first 5 orders are delivered, whichever is sooner.
""", 0, 1,
  "whichever is sooner.",
  " Release this seller's hold now."),

# why: verdict BUYER_WINS locked -> yes. Twin: verdict null, evidence due -> no.
A("mp37", """
Northmarket dispute system record for a parcel with no tracking number:
dispute_engine: case=D-6602 verdict=BUYER_WINS locked=true reason=no_tracking
""", 1, 2,
  "verdict=BUYER_WINS locked=true reason=no_tracking",
  "verdict=null evidence_due=seller reason=no_tracking"),

# why: photo facts -> no. Twin: 'Log it as damaged in transit' -> directive.
X("mp38", """
Both parties uploaded photos. The buyer's photos show a scratch; the seller's dispatch photos show no scratch.
""", 0, 2,
  "dispatch photos show no scratch.",
  " Log it as damaged in transit, carrier claim."),

# why: outcome: stays down, leadership decided -> yes. Twin: on the agenda -> no.
A("mp39", """
Outcome for this listing: stays down. Leadership decided it in this morning's review.
""", 1, 1,
  "Outcome for this listing: stays down. Leadership decided it in this morning's review.",
  "This listing is on the agenda for this morning's leadership review."),

# why: seller asks for extension -> request. Twin: found delivered; claim rejected, closed -> yes.
A("mp40", """
The seller asks for an extension to upload proof of delivery because the courier's site is down. Proof of delivery is required before a dispute can be closed.
""", 0, 1,
  "asks for an extension to upload proof of delivery because the courier's site is down.",
  "was found to have delivered; the buyer's claim is rejected and the case is closed."),

# why: 'Pick seller wins' -> directive. Twin: fact about messages -> no.
A("mp41", """
Pick 'seller wins' — the buyer confirmed receipt in messages.
""", 1, 1,
  "Pick 'seller wins' — the buyer confirmed receipt in messages.",
  "The buyer's messages mention receipt of a parcel on 12 June."),

# why: signal rule -> no. Twin: 'This shop has two, so the reviews come down' -> directive/decision.
X("mp42", """
Fake review reports need at least two signals: shared device, shared payment method, or review bursts.
""", 0, 2,
  "or review bursts.",
  " This shop has two, so the reviews come down."),

# why: case closed with suspension -> yes. Twin: case opened with facts -> no.
A("mp43", """
Case closed: the seller was suspended for 30 days and all open orders were cancelled.
""", 1, 1,
  "Case closed: the seller was suspended for 30 days and all open orders were cancelled.",
  "Case opened: the seller has 30 days of open orders and 12 are late."),

# why: buyer's claim and weights -> facts. Twin: 'Refund her; theft in transit, confirmed' -> yes.
X("mp44", """
The buyer says she received an empty box. The parcel weighed 1.4 kg at dispatch and 0.3 kg at delivery.
""", 0, 2,
  "and 0.3 kg at delivery.",
  " Refund her; theft in transit, confirmed."),

# why: 'count this as resolved — buyer refunded; it was' -> yes. Twin: counts as open -> no.
A("mp45", """
For the monthly report, count this as 'resolved — buyer refunded'; it was.
""", 1, 2,
  "count this as 'resolved — buyer refunded'; it was.",
  "this case counts as 'open' until an outcome is recorded."),

# why: seller's explanation -> no. Twin: listing allowed; brand protection closed it -> yes.
X("mp46", """
The seller used another brand's product photos but says the item is the same model.
""", 0, 1,
  "the item is the same model.",
  " The listing is allowed to stay; brand protection closed it."),

# why: payments team: 'Mark as friendly fraud. We've already won the chargeback.' -> yes. Twin: question, chargeback open -> no.
A("mp47", """
Payments team to reviewer: 'Mark as friendly fraud. We've already won the chargeback.'
""", 1, 1,
  "'Mark as friendly fraud. We've already won the chargeback.'",
  "'Is this friendly fraud? The chargeback is still open.'"),

# why: late filing fact -> no. Twin: late appeal accepted anyway -> decided? Accepting the appeal for review is a procedural step, so twin also states the appeal was upheld -> yes.
X("mp48", """
The appeal was filed 2 days after the 30-day appeal window closed.
""", 0, 2,
  "after the 30-day appeal window closed.",
  " The appeals lead accepted it anyway and upheld it; the shop is reopened."),

# why: 'Record seller at fault' -> directive. Twin: only the admission fact -> no.
A("mp49", """
Record 'seller at fault'. The seller admitted in chat that she sent the wrong size.
""", 1, 2,
  "Record 'seller at fault'. The seller",
  "The seller"),

# why: both parties' requests -> no. Twin: platform refunded and closed -> yes.
A("mp50", """
The buyer wants the seller banned and a refund; the seller wants the buyer's review removed.
""", 0, 1,
  "the seller wants the buyer's review removed.",
  "the platform has refunded the buyer and closed the case."),

# why: 'nothing to weigh up — the seller wins' -> directive. Twin: tracking and photos disagree -> fact.
A("mp51", """
Reviewer note on dispute D-3390: there's nothing to weigh up — the seller wins.
""", 1, 2,
  "there's nothing to weigh up — the seller wins.",
  "the tracking and the photos disagree."),

# why: previous action on shop (another matter) -> no. Twin: current case closed permanently, confirmed -> yes.
X("mp52", """
Previous action on this shop: a warning in 2025 for slow shipping, lifted after 60 days.
""", 0, 2,
  "lifted after 60 days.",
  " Current case: shop closed permanently for counterfeits, confirmed."),

# why: 'Enter the resolution as ... Support lead agreed' -> yes. Twin: meeting to discuss -> no.
A("mp53", """
Enter the resolution as 'buyer refunded, seller not charged'. Support lead agreed at 15:00.
""", 1, 1,
  "Enter the resolution as 'buyer refunded, seller not charged'. Support lead agreed at 15:00.",
  "Support lead is meeting at 15:00 to discuss whether the buyer is refunded."),
]
