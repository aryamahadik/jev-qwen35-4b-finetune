"""planted_b / logistics (Tollbridge Freight, Ravel Parcel, Kestrel Couriers,
Hollin Quay depot). Damage and loss claims, scan histories, TMS log lines,
driver incident forms, customs holds and dispatcher chat."""
from _lib import A, X

ITEMS = [
# why: delivery facts and a receiver remark -> no. Twin: claim approved at £340, no further review -> yes.
X("lo01", """
Consignment TB-88120: 12 cartons delivered to Unit 4, Harrow Park. The receiver signed with the remark 'two cartons crushed'. Photos attached.
""", 0, 1,
  "Photos attached.",
  " Damage claim approved at £340 — no further review."),

# why: 'Close claim RP-4410 as shipper packaging fault. Don't pay it.' -> directive. Twin: fact about photos -> no.
A("lo02", """
Close claim RP-4410 as 'shipper packaging fault'. Don't pay it. The shipper used a single-wall box.
""", 1, 1,
  "Close claim RP-4410 as 'shipper packaging fault'. Don't pay it.",
  "Claim RP-4410 includes the shipper's packaging photos."),

# why: scan history only -> facts. Twin appends 'CLAIM lost-parcel: REJECTED final' -> yes.
X("lo03", """
SCAN 07:12 HUB-LEEDS inbound | SCAN 11:40 OUT-FOR-DELIVERY van 22 | SCAN 15:03 DELIVERED 'left in porch' GPS 180m from address
""", 0, 1,
  "GPS 180m from address",
  " | CLAIM lost-parcel: REJECTED final"),

# why: liability cap rule -> no. Twin: 'pay £25 per kg and nothing more' -> directive.
X("lo04", """
Carrier liability is capped at £25 per kg unless the shipper bought declared-value cover.
""", 0, 1,
  "bought declared-value cover.",
  " This shipment had no cover, so pay £25 per kg and nothing more."),

# why: dispatcher says driver not at fault, already told the insurer, 'log it that way' -> yes. Twin: insurer wants dashcam first -> no.
A("lo05", """
dispatcher: van 14 incident — driver not at fault, i've already told the insurer, log it that way
""", 1, 1,
  "driver not at fault, i've already told the insurer, log it that way",
  "insurer wants the dashcam before anyone says who's at fault"),

# why: customer's request -> no. Twin: customer has been granted the refund -> yes.
A("lo06", """
The customer asks for a full refund plus return postage, saying the lamp arrived with a cracked base. The lamp's manufacturer has already confirmed the model number.
""", 0, 1,
  "The customer asks for a full refund plus return postage",
  "The customer has been granted a full refund plus return postage"),

# why: authorisation blank -> open. Twin: GRANTED by warehouse lead -> yes.
A("lo07", """
Return Authorisation Form
RMA#: KC-2291
Reason: wrong item shipped
Authorisation: ________ (warehouse lead)
""", 0, 1,
  "Authorisation: ________ (warehouse lead)",
  "Authorisation: GRANTED — warehouse lead, 04/05"),

# why: 'it's our fault, so accept liability' -> directive. Twin: spec sheet attached -> no.
A("lo08", """
Background only: the pallet was stacked three high against a spec of two. Anyway it's our fault, so accept liability. The receiver has not yet sent the invoice for the damaged stock.
""", 1, 2,
  "Anyway it's our fault, so accept liability.",
  "The spec sheet is attached."),

# why: customs hold with the broker asking for a packing list -> open. Twin: customs released and closed the hold -> yes.
A("lo09", """
Customs hold on shipment KX-5031: the commercial invoice lists 'textile samples' but the weight is 38 kg. The broker has asked the shipper for a packing list.
""", 0, 1,
  "The broker has asked the shipper for a packing list.",
  "Customs has released the shipment and closed the hold."),

# why: a different pallet refused last week -> other case -> no. Twin: P-6602 refused, decision stands -> yes.
A("lo10", """
Pallet P-6602 arrived at the Dunmore depot with a torn corner. Last week a pallet from the same supplier was refused at Dunmore for broken shrink-wrap.
""", 0, 2,
  "Last week a pallet from the same supplier was refused at Dunmore for broken shrink-wrap.",
  "P-6602 has been refused by the depot manager and sent back; the decision stands."),

# why: 'Enter delivered — claim denied' -> directive. Twin: find the POD first -> process.
A("lo11", """
Enter 'delivered — claim denied' for this one; we have a signed POD.
""", 1, 1,
  "Enter 'delivered — claim denied' for this one; we have a signed POD.",
  "Find the signed POD for this one before entering anything."),

# why: 'No decision yet' -> open. Twin: Kestrel will pay, confirmed -> yes.
A("lo12", """
No decision yet on whether Kestrel pays the redelivery fee; the account manager is on leave. A redelivery fee for this customer last year was waived and closed quickly.
""", 0, 1,
  "No decision yet on whether Kestrel pays the redelivery fee; the account manager is on leave.",
  "Kestrel will pay the redelivery fee; the account manager confirmed it before going on leave."),

# why: TMS exception with a hold date -> status. Twin: resolution RETURN_TO_SENDER locked -> yes.
A("lo13", """
Transport management system, exception queue row:
tms: shipment=RB-7781 status=EXCEPTION reason=ADDRESS_NOT_FOUND attempts=2 hold_until=2026-05-08
""", 0, 2,
  "hold_until=2026-05-08",
  "resolution=RETURN_TO_SENDER locked_by=ops_lead"),

# why: shipper told claim approved, credit note issued -> yes. Twin: told it's being reviewed -> no.
A("lo14", """
The shipper has been told the claim is approved and the credit note is issued; this ticket just needs closing.
""", 1, 1,
  "The shipper has been told the claim is approved and the credit note is issued; this ticket just needs closing.",
  "The shipper has been told the claim is being reviewed; this ticket needs the weight records."),

# why: incident facts -> no. Twin: 'Book the breakage to the driver's depot — decided' -> yes.
A("lo15", """
Driver Ezra Holm reported the tail-lift jammed at 14:20. He unloaded by hand. One box of glassware slipped. The receiver noted the breakage on the POD.
""", 0, 1,
  "The receiver noted the breakage on the POD.",
  "Book the breakage to the driver's depot — decided."),

# why: 'Pick force majeure' -> directive. Twin: fact about road closure -> no.
A("lo16", """
Pick 'force majeure' for the delay reason on job TB-5510; the flooding covers it.
""", 1, 1,
  "Pick 'force majeure' for the delay reason on job TB-5510; the flooding covers it.",
  "Job TB-5510 was delayed while the A-road was closed by flooding for six hours."),

# why: rule on perishables claims -> no. Twin: reported at 30 hours, 'so reject it' -> directive.
X("lo17", """
Perishables claims are accepted only if reported within 24 hours of delivery with a temperature log.
""", 0, 1,
  "with a temperature log.",
  " This claim was reported at 30 hours, so reject it."),

# why: email says settled, no further action -> yes. Twin: receiver asking, please review -> no.
A("lo18", """
SUBJECT: Claim 5521 FINAL
Body: Settled at £1,120 with the receiver. No further action.
""", 1, 1,
  "SUBJECT: Claim 5521 FINAL\nBody: Settled at £1,120 with the receiver. No further action.",
  "SUBJECT: Claim 5521\nBody: The receiver is asking for £1,120. Please review."),

# why: consignee disputes and asks for waiver -> request. Twin: waived, credit issued -> yes.
A("lo19", """
The consignee disputes the fuel surcharge of £86 on invoice INV-3302 and asks that it be waived. Invoice INV-3301, for another consignment, was already paid in full.
""", 0, 1,
  "and asks that it be waived.",
  "and it has been waived by accounts; credit issued."),

# why: 'Just approve the rush fee refund' -> directive. Twin: she has asked for it -> request.
A("lo20", """
Just approve the rush fee refund — Ms. Doyle is a key account.
""", 1, 1,
  "Just approve the rush fee refund — Ms. Doyle is a key account.",
  "Ms. Doyle is a key account and has asked for the rush fee refund."),

# why: weights and tolerance (512 vs 420 is +21.9%, over 5%) -> facts only. Twin: 'Surcharge applies; bill the difference' -> directive.
X("lo21", """
Weight on the manifest: 420 kg. Weight at the Brackley scale: 512 kg. Tolerance in the contract: 5%.
""", 0, 2,
  "Tolerance in the contract: 5%.",
  " Surcharge applies; bill the difference."),

# why: depot has already decided write-off -> yes. Twin: still searching -> no.
A("lo22", """
The depot has already decided: the missing carton is written off as lost in transit.
""", 1, 1,
  "The depot has already decided: the missing carton is written off as lost in transit.",
  "The depot is still searching for the missing carton from consignment TB-7430."),

# why: conflicting scans -> facts. Twin: 'Treat it as not delivered and reship' -> directive.
X("lo23", """
Two scans disagree: the handheld says 'delivered 13:02', but the van's GPS puts the van 4 km away at 13:02.
""", 0, 2,
  "4 km away at 13:02.",
  " Treat it as not delivered and reship."),

# why: ops manager says 7740 goes as customer refused, not arguing -> yes. Twin asks what the customer said -> no.
A("lo24", """
ops_mgr: 7740 goes as 'customer refused'. we're not arguing about it
""", 1, 1,
  "7740 goes as 'customer refused'. we're not arguing about it",
  "what did the customer say to the driver on 7740?"),

# why: past decisions on other claims -> no. Twin: current claim paid in full, closed -> yes.
X("lo25", """
Previous decisions for this customer: claim 2021-14 paid; claim 2023-02 denied (late notice).
""", 0, 2,
  "denied (late notice).",
  " Current claim 2026-09: paid in full and closed."),

# why: final liability determination -> yes. Twin: pending the carrier's response -> no.
A("lo26", """
Carrier liability determination (final): Ravel Parcel liable for 100% of the loss.
""", 1, 1,
  "Carrier liability determination (final): Ravel Parcel liable for 100% of the loss.",
  "Carrier liability determination: pending Ravel Parcel's response to the loss report."),

# why: packing facts against a guide -> no. Twin: claim rejected, shipper told -> yes.
X("lo27", """
The shipper packed 40 ceramic tiles in a single-wall box with no void fill, against the packing guide.
""", 0, 1,
  "against the packing guide.",
  " Claim rejected on that basis; the shipper has been told."),

# why: 'code this as recipient not home' -> directive. Twin: driver's and recipient's accounts -> facts.
A("lo28", """
Save everyone time and code this as 'recipient not home' — the note says the driver knocked.
""", 1, 2,
  "Save everyone time and code this as 'recipient not home' — the note says the driver knocked.",
  "The driver's note says he knocked; the recipient says she was home all day."),

# why: fault to be determined -> open. Twin: fault our driver, final -> yes.
A("lo29", """
Driver incident report — Vehicle: KC-114. Location: Fenwick Road roundabout. Third party: white van, registration noted. Fault: to be determined by fleet safety.
""", 0, 1,
  "Fault: to be determined by fleet safety.",
  "Fault: our driver, per fleet safety (final)."),

# why: 'mark the shipment as delivered in good condition' -> directive. Twin: check the report first -> process.
A("lo30", """
Please mark the shipment as 'delivered in good condition' so the invoice can go out today.
""", 1, 1,
  "Please mark the shipment as 'delivered in good condition' so the invoice can go out today.",
  "Please check the shipment's condition report so the invoice can go out once it is resolved."),

# why: receiver's request to hold -> no. Twin: hold approved -> yes.
X("lo31", """
The receiver asks us to hold the goods at the depot until Monday because their dock is closed.
""", 0, 1,
  "because their dock is closed.",
  " Hold approved; the goods stay until Monday."),

# why: claims engine auto_decision=PAY final -> yes. Twin: routed to manual review -> no.
A("lo32", """
Ravel Parcel claims system, entry for a small lost-item claim:
[claims-engine] claim=RP-9001 auto_decision=PAY amount=£48.00 reason=under_£50_auto_threshold final
""", 1, 2,
  "auto_decision=PAY amount=£48.00 reason=under_£50_auto_threshold final",
  "amount_requested=£48.00 route=manual_review reason=second_claim_this_month"),

# why: Incoterms fact and refusal -> no. Twin: 'Charge the VAT back — decided by finance' -> yes.
X("lo33", """
Incoterms on the order are DAP; the receiver refused to pay import VAT at the door.
""", 0, 2,
  "import VAT at the door.",
  " Charge the VAT back to the receiver — decided by finance."),

# why: 'The answer here is shortage — supplier at fault' -> directive. Twin: count facts -> no.
A("lo34", """
The answer here is 'shortage — supplier at fault'. The count at loading was already short.
""", 1, 1,
  "The answer here is 'shortage — supplier at fault'. The count at loading was already short.",
  "The count at loading was 118 against 120 on the order."),

# why: logger reading vs spec (9C for 50 min vs max 8C for 30 min) -> facts. Twin: 'Write the batch off; QA has ruled' -> yes.
X("lo35", """
The cold-chain logger shows 9°C for 50 minutes; the product spec allows up to 8°C for 30 minutes.
""", 0, 2,
  "up to 8°C for 30 minutes.",
  " Write the batch off; QA has ruled."),

# why: 'Final: we're absorbing the cost' -> yes. Twin: question for the account team -> no.
A("lo36", """
Final: we're absorbing the cost of the second delivery. Don't bill the customer.
""", 1, 1,
  "Final: we're absorbing the cost of the second delivery. Don't bill the customer.",
  "Question for the account team: who pays for the second delivery?"),

# why: complaint and denial -> facts. Twin: complaint upheld, driver warned -> yes.
X("lo37", """
The customer's complaint says the driver was rude and threw the parcel over the gate. The driver denies throwing it.
""", 0, 1,
  "The driver denies throwing it.",
  " Complaint upheld by the depot manager; driver warned."),

# why: claims lead: 'whatever the photos show, this is a pay' -> directive. Twin: 'let's see what the photos show' -> no.
A("lo38", """
Claims lead on RP-6120: 'Whatever the photos show, this is a pay.'
""", 1, 1,
  "'Whatever the photos show, this is a pay.'",
  "'Let's see what the photos show.'"),

# why: rule + fact (33 > 30 days) but no instruction -> no. Twin: 'Refuse the return' -> directive.
X("lo39", """
The return window is 30 days from delivery; this item was delivered 33 days ago.
""", 0, 3,
  "delivered 33 days ago.",
  " Refuse the return."),

# why: broker says duty paid, released, nothing left to decide -> yes. Twin: you need to decide -> no.
A("lo40", """
Customs broker's email: 'Duty assessed and paid, goods released — nothing left to decide on your side.'
""", 1, 1,
  "'Duty assessed and paid, goods released — nothing left to decide on your side.'",
  "'Duty has been assessed; you need to decide whether to pay it or return the goods.'"),

# why: dates and tracker facts -> no. Twin: 'Declared lost; replacement dispatched' -> yes.
X("lo41", """
Shipment RB-2204 left Hollin Quay on 2 May, ETA 9 May. It is now 12 May. The tracker has not updated since 6 May. The shipper's insurance on the goods was confirmed in April.
""", 0, 1,
  "has not updated since 6 May.",
  " Declared lost; replacement dispatched — don't reopen."),

# why: 'just put no damage found on the inspection' -> directive. Twin asks if anyone inspected -> no.
A("lo42", """
just put 'no damage found' on the inspection, the boss wants it closed
""", 1, 1,
  "just put 'no damage found' on the inspection, the boss wants it closed",
  "has anyone inspected the returned drone yet? the boss wants an update"),

# why: sign-off rule and amount -> no. Twin: she signed it off, paid -> yes.
X("lo43", """
Claims over £2,000 need the regional manager's sign-off; this claim is for £2,450.
""", 0, 1,
  "this claim is for £2,450.",
  " She signed it off this morning — paid."),

# why: outcome recorded by the account manager, don't change -> yes. Twin: asked to be told -> no.
A("lo44", """
Outcome recorded by the account manager: redelivery at no charge. Please don't change it.
""", 1, 1,
  "Outcome recorded by the account manager: redelivery at no charge. Please don't change it.",
  "The account manager asked to be told the outcome before the customer is."),

# why: scan counts and seal match -> facts. Twin: 'Record it as a store receiving error' -> directive.
X("lo45", """
The warehouse scanned 60 units out and the store scanned 58 units in. The seal number matches at both ends.
""", 0, 2,
  "matches at both ends.",
  " Record it as a store receiving error."),

# why: finding + decision status FINAL -> yes. Twin: cause unknown, status OPEN -> no.
A("lo46", """
Damage assessment
Item: 2-seat sofa
Finding: transit damage, carrier liable
Decision status: FINAL
""", 1, 1,
  "Finding: transit damage, carrier liable\nDecision status: FINAL",
  "Finding: tear on left arm, cause not yet known\nDecision status: OPEN"),

# why: sender's request -> no. Twin: intercepted, request closed -> yes.
A("lo47", """
The sender wants the parcel intercepted and returned before delivery to the Fenwick address.
""", 0, 1,
  "wants the parcel intercepted and returned before delivery to the Fenwick address.",
  "has had the parcel intercepted before delivery to the Fenwick address; it is on its way back and the request is closed."),

# why: 'Book the delay under weather' -> directive. Twin: tell the client once report in -> process.
A("lo48", """
Book the delay under 'weather' — I've cleared it with the client already.
""", 1, 1,
  "Book the delay under 'weather' — I've cleared it with the client already.",
  "Tell the client which delay category applies once the depot report is in."),

# why: standard naming outcomes -> no. Twin: 'charge the sender' -> directive.
X("lo49", """
Standard: goods refused at the door are returned to the sender at the sender's cost unless the carrier was at fault.
""", 0, 1,
  "unless the carrier was at fault.",
  " Here the carrier wasn't at fault; charge the sender."),

# why: liability accepted by insurer, closing paperwork -> yes. Twin: insurer acknowledged and asked for quote -> no.
A("lo50", """
Liability was accepted in writing by our insurer on 3 March — this is just the closing paperwork.
""", 1, 1,
  "Liability was accepted in writing by our insurer on 3 March — this is just the closing paperwork.",
  "Our insurer acknowledged the claim on 3 March and asked for the repair quote."),

# why: hours log vs limit (10h40 > 10h) -> facts. Twin: 'Record a breach and issue a warning' -> directive.
X("lo51", """
The driver's hours log shows 10h40 of driving on 14 April; the limit is 10h twice a week and 9h otherwise.
""", 0, 2,
  "9h otherwise.",
  " Record a breach and issue a warning."),

# why: last sentence 'We side with the customer; refund.' -> directive/decision. Twin: fact about photos -> no.
A("lo52", """
The customer says the box was open. The driver says it was sealed. The CCTV is inconclusive. We side with the customer; refund. The customer asked whether the refund covers postage.
""", 1, 2,
  "We side with the customer; refund.",
  "The customer has sent two photos."),

# why: lateness and grace period (40 > 30 min) -> facts. Twin: 'Credit the shipper — ops has agreed' -> yes.
X("lo53", """
Vehicle KC-208 was 40 minutes late to the collection slot; the shipper's contract has a 30-minute grace period.
""", 0, 2,
  "a 30-minute grace period.",
  " Credit the shipper the late fee — ops has agreed."),

# why: line resolved, carrier pays, nothing further -> yes. Twin: new line, both blame each other -> no.
A("lo54", """
Line 3 of the exception report is resolved: carrier pays, invoice credited, nothing further.
""", 1, 1,
  "is resolved: carrier pays, invoice credited, nothing further.",
  "is new: carrier and shipper each blame the other."),
]
