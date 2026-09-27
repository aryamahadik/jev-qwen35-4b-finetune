"""proc_multihop / logistics, warehousing and transport (Greyling Fresh Foods,
Marlow & Pike Home, Ostry Cycles, Kestrel Parcel, Hallam Haulage, Duneside
Distribution Centre)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ lg01
# why: excursion time is cumulative across legs (carried on the shipment record).
# Leg 1: 1.5 h at 10 C, leg 2: 2 h at 11 C -> 3.5 h, max reading 11 C (not > 12) ->
# band >2 h to 4 h -> accept with shelf life cut by 1 day.
# Twin: leg 1 2.5 h -> 4.5 h -> reject.
C("lg01", "What should goods-in do with inbound load GR-7731?",
"""
Greyling Fresh Foods — Chilled Receiving Standard CR-4

1. Definitions
1.1 Excursion: any period in which product temperature is above 8 °C.
1.2 Excursion time is cumulative over the product's whole journey from the kitchen, including earlier legs recorded on the shipment record.

2. Decision at receipt
2.1 Any reading above 12 °C: reject the load.
2.2 Cumulative excursion time up to 2 hours: accept.
2.3 More than 2 hours and up to 4 hours: accept, and reduce the use-by date by 1 day.
2.4 More than 4 hours: reject the load.

3. Paperwork: goods-in signs the carrier's delivery note only after the decision.

Shipment record GR-7731 (ready meals, 22 cages)
| Leg | Route | Excursion time | Highest reading |
| 1 | Kitchen to Carden hub | 1.5 h | 10.0 °C |
| 2 | Carden hub to Duneside DC | 2.0 h | 11.0 °C |
Driver comment (leg 2): "Reefer unit faulted on the ring road, fixed at the lay-by."
""",
[("accept_normal", "This leg's excursion was only 2 hours and no reading passed 12 °C."),
 ("accept_reduce_use_by", "Across both legs the excursion totals more than 2 but not more than 4 hours, with no reading above 12 °C."),
 ("reject_load", "The load's total excursion time is more than 4 hours, or a reading passed 12 °C.")],
"accept_reduce_use_by", 2,
twin=T([("| 1 | Kitchen to Carden hub | 1.5 h | 10.0 °C |", "| 1 | Kitchen to Carden hub | 2.5 h | 10.0 °C |")], "reject_load")),

# ------------------------------------------------------------------ lg02
# why: timing: order 20 Nov is in the holiday window (15 Nov - 24 Dec) -> returnable to
# 31 Jan; request 10 Jan ok. But in-ear headphones are a hygiene item, opened, not faulty
# -> not returnable. Twin: over-ear headphones (not on list) -> refund.
C("lg02", "How should customer services decide return request RT-40912?",
"""
Marlow & Pike Home — Returns Policy

1. Items may be returned within 30 days of the delivery date for a full refund.
2. "Delivery date" is the date of the carrier's delivered scan.
3. Holiday extension: orders placed from 15 November to 24 December may be returned until 31 January.
4. Hygiene items that have been opened can be returned only if faulty. The hygiene list is below.
5. Refunds go to the original payment method.

Hygiene list: pierced jewellery; in-ear headphones and earbuds; cosmetics; swimwear without the hygiene strip.

Return request RT-40912
Order placed: 20 November
Delivered scan: 24 November
Request received: 10 January
Item: Aurel in-ear headphones, black
Condition: opened, used a few times, working normally
Reason given: "Changed my mind, they don't suit me."
""",
[("accept_refund", "The request is in time under the holiday extension and no exclusion applies to this item."),
 ("refuse_hygiene_item", "The item is on the hygiene list, has been opened and is not faulty."),
 ("refuse_out_of_time", "The request came more than 30 days after delivery.")],
"refuse_hygiene_item", 2,
twin=T([("Item: Aurel in-ear headphones, black", "Item: Aurel over-ear headphones, black")], "accept_refund")),

# ------------------------------------------------------------------ lg03
# why: Wh = V x Ah; 36 V x 3.2 Ah (3,200 mAh) = 115.2 Wh. Standalone battery > 100 Wh
# and <= 300 Wh -> dangerous goods service. Twin: 2,500 mAh -> 90 Wh -> standard ground.
C("lg03", "Which shipping route does order OC-2291 need?",
"""
Ostry Cycles — Dispatch Rules for Batteries

1. Definitions: a battery's energy rating in watt-hours (Wh) is its nominal voltage (V) multiplied by its capacity in ampere-hours (Ah). 1,000 mAh = 1 Ah.
2. Batteries installed in a bike are covered by the e-bike shipping rules, not this section.
3. Standalone lithium-ion batteries:
 3.1 up to 100 Wh: standard ground service;
 3.2 over 100 Wh up to 300 Wh: dangerous goods (DG) ground service, with DG label and declaration;
 3.3 over 300 Wh: cannot be shipped by parcel; customer collects in store.
4. Air services never carry standalone lithium batteries.

Order OC-2291
Item: spare battery pack for the Ostry City Glide (sold separately, not fitted)
Label on pack: 36 V, 3,200 mAh, lithium-ion
Customer: home delivery, standard ground selected at checkout.
""",
[("standard_ground", "The pack's rating is 100 Wh or less, so standard ground service is fine."),
 ("dangerous_goods_ground", "The pack's rating is above 100 Wh but not above 300 Wh, so it needs DG ground service."),
 ("store_collection_only", "The pack's watt-hour rating is above 300 Wh, so it cannot be shipped by parcel and the customer must collect it in store.")],
"dangerous_goods_ground", 2,
twin=T([("Label on pack: 36 V, 3,200 mAh, lithium-ion", "Label on pack: 36 V, 2,500 mAh, lithium-ion")], "standard_ground")),

# ------------------------------------------------------------------ lg04
# why: customs value = goods + shipping + insurance: 138 + 19 = 157 > 150 -> formal entry
# with duty. Gift relief needs private sender; sender is a company. Twin: shipping 9 ->
# 147 -> low-value entry, VAT only.
C("lg04", "How should the broker declare consignment KP-55810?",
"""
Kestrel Parcel — Import Brokerage Desk Guide

1. Customs value = price of the goods + shipping + insurance to the border.
2. Low-value entry: customs value up to and including €150 — no duty; VAT only.
3. Formal entry: customs value above €150 — duty and VAT.
4. Gift relief: a gift from one private individual to another, customs value up to €45 — no duty, no VAT.
5. The broker uses the commercial invoice for all values.

Commercial invoice — consignment KP-55810
Seller: Lindqvist Outdoor AB (company)
Buyer: private individual
Goods: 1 × trail jacket — €138.00
Shipping: €19.00
Insurance: none
Note on parcel: "Happy birthday Jonas!"
""",
[("low_value_vat_only", "The customs value, including shipping, is €150 or less."),
 ("formal_entry_duty_and_vat", "With shipping added, the customs value is above €150."),
 ("gift_relief", "The parcel is marked as a birthday present, so gift relief applies.")],
"formal_entry_duty_and_vat", 1),

# ------------------------------------------------------------------ lg05
# why: POD clean + packaging intact -> concealed damage -> carrier notice within 5 days of
# delivery. Delivered 3 Jun, found and notified 10 Jun = 7 days -> carrier route closed ->
# loss £1,180 > £250 excess -> cargo insurance. Twin: found 6 Jun (3 days) -> carrier claim.
C("lg05", "Which claim route should the claims clerk use for delivery DL-3318?",
"""
Duneside Distribution Centre — Transit Damage Procedure

1. Definitions
 - Visible damage: damage that can be seen at delivery; it must be noted on the proof of delivery (POD).
 - Concealed damage: damage found after delivery when the packaging was intact and the POD was signed clean.
2. Carrier claims
 2.1 Visible damage noted on the POD: claim against the carrier within 9 months.
 2.2 Concealed damage: the carrier must be notified within 5 days of the delivery date; the claim then follows within 9 months.
3. If the carrier route is closed, claim on our own cargo insurance where the loss exceeds the £250 excess; otherwise write the loss off.

Delivery DL-3318 (Hallam Haulage)
Delivered: 3 June, 14:20. POD signed clean. Outer cartons intact.
10 June: cartons opened for put-away; 4 glass table tops found cracked inside intact cartons.
Carrier notified: 10 June.
Loss at cost: £1,180.
""",
[("claim_against_carrier", "The damage was concealed and the carrier was notified inside the time limit."),
 ("claim_cargo_insurance", "The carrier notice came too late for concealed damage, and the loss is larger than the excess."),
 ("write_off_loss", "Damage found after a clean POD cannot be claimed from anyone.")],
"claim_cargo_insurance", 2,
twin=T([("10 June: cartons opened for put-away;", "6 June: cartons opened for put-away;"), ("Carrier notified: 10 June.", "Carrier notified: 6 June.")], "claim_against_carrier")),

# ------------------------------------------------------------------ lg06
# why: lot code YYDDD-L. 26065-2 = 2026 day 65 = 6 March (31 + 28 + 6), line 2 -> inside
# recall scope (line 2, 3-9 March) -> quarantine; destroy only on written instruction.
# Twin: 26070-2 = 11 March -> outside -> release.
C("lg06", "What should the stock controller do with lot 26065-2 of Crisp Oat Bars?",
"""
Duneside Distribution Centre — Supplier Recall Handling

1. Stock in scope of a recall notice is moved to quarantine location Q1 and blocked in the system, pending the supplier's instruction.
2. Stock is destroyed only on the supplier's written instruction.
3. Stock outside the scope is released for picking.

Lot code format (Harbrook Foods): YYDDD-L, where YY is the year, DDD is the day of the year of production (001 = 1 January) and L is the production line.

Recall notice HF-R-09 (Harbrook Foods), received today
"Crisp Oat Bars 6-pack: all lots produced on Line 2 between 3 March and 9 March 2026 inclusive may contain undeclared sesame. Please isolate affected stock and await our disposal instructions."

Stock on hand — Crisp Oat Bars 6-pack
| Lot | Location | Cases |
| 26065-2 | B-14-03 | 36 |
Picker note: "These look fine, can I pick them for the Tesmond order?"
""",
[("quarantine_lot", "The lot was produced on Line 2 within the recall dates, so it goes to Q1 pending instructions."),
 ("release_lot", "The lot falls outside the recall's line or date range."),
 ("destroy_lot", "The lot is in scope of the recall, so it is destroyed immediately.")],
"quarantine_lot", 2,
twin=T([("| 26065-2 | B-14-03 | 36 |", "| 26070-2 | B-14-03 | 36 |")], "release_lot",
       instructions="What should the stock controller do with lot 26070-2 of Crisp Oat Bars?")),

# ------------------------------------------------------------------ lg07
# why: allocation order: critical-infrastructure customers first (amendment), then tier,
# then earliest order. Customer master: Wexmoor Water is flagged -> order D first.
# Twin: flag "no" -> tier 1 earliest = order C (1 May).
C("lg07", "Which backorder should receive the incoming stock first?",
"""
Marlow & Pike Home — Trade Backorder Allocation Rules

1. Allocate incoming stock to whole orders, one at a time, in priority order.
2. Priority: customer tier (Tier 1 before Tier 2 before Tier 3), then earliest order date.
3. (Amendment, March) Customers flagged as critical infrastructure in the customer master come before all tiers.
4. Partial shipments only where the customer master says partials are accepted.

Customer master (extract)
| Customer | Tier | Critical infrastructure | Partials |
| Beaumont Hotels | 1 | no | yes |
| Corran Interiors | 1 | no | no |
| Wexmoor Water | 3 | yes | no |
| Aldwick Estates | 2 | no | yes |

Backorders — item: commercial dehumidifier DH-40 (incoming: 40 units)
| Order | Customer | Qty | Order date |
| A | Aldwick Estates | 10 | 28 Apr |
| B | Beaumont Hotels | 30 | 3 May |
| C | Corran Interiors | 25 | 1 May |
| D | Wexmoor Water | 20 | 6 May |
""",
[("allocate_order_a", "Aldwick's order is the oldest on the list, so it is served first."),
 ("allocate_order_b", "Beaumont is Tier 1 and its order is the largest."),
 ("allocate_order_c", "Among the customers who come first under the allocation rules, Corran Interiors has the earliest order date on the list."),
 ("allocate_order_d", "Wexmoor Water is flagged as critical infrastructure, which puts it ahead of every tier.")],
"allocate_order_d", 2,
twin=T([("| Wexmoor Water | 3 | yes | no |", "| Wexmoor Water | 3 | no | no |")], "allocate_order_c")),

# ------------------------------------------------------------------ lg08
# why: daily limit 9 h, 10 h allowed twice a week. Mon 10 and Wed 10 already used both
# extensions -> Friday limit 9 h; 7.5 + 2 = 9.5 > 9 -> reassign.
# Twin: Wed 9.0 -> one extension used -> limit 10 h -> 9.5 ok; but driving since last
# break 3 h + 2 h = 5 h > 4.5 h -> needs a 45-min break first -> assign after break.
C("lg08", "Can dispatch give Carys Holt the extra 2-hour run this afternoon?",
"""
Hallam Haulage — Driver Hours Rules (summary for planners)

1. Daily driving: up to 9 hours; may be extended to 10 hours on no more than two days in the same week (Monday to Sunday).
2. Weekly driving: no more than 56 hours.
3. Breaks: after 4.5 hours of driving, a break of at least 45 minutes must be taken before driving on.
4. Planners must not plan a run that breaks rules 1-3; if a driver cannot take it, reassign it.

Carys Holt — driving this week
| Day | Driving hours |
| Mon | 10.0 |
| Tue | 8.0 |
| Wed | 10.0 |
| Thu | 8.0 |

Today (Friday), tachograph so far
06:00-10:30 driving (4.5 h)
10:30-11:15 break
11:15-14:15 driving (3.0 h)
14:15 now at depot. Extra run offered: 2.0 hours' driving, leaving 14:30.
""",
[("assign_run_now", "Her hours today and this week leave room for the run, and her break status allows her to drive it straight through."),
 ("assign_run_after_break", "Today's limit allows the run, but she would pass 4.5 hours since her last break, so she needs a 45-minute break first."),
 ("reassign_to_other_driver", "She has used both of this week's extended days, so the run would take her past today's 9-hour limit.")],
"reassign_to_other_driver", 3,
twin=T([("| Wed | 10.0 |", "| Wed | 9.0 |")], "assign_run_after_break")),

# ------------------------------------------------------------------ lg09
# why: chargeable weight = max(actual, dim); dim = 110*60*50/5000 = 66 kg. 66 kg is in
# 30-70 kg band and longest side 110 <= 120 -> oversize parcel.
# Twin: 110 x 40 x 30 -> 26.4 kg -> chargeable 26.4 <= 30 -> standard.
C("lg09", "Which service should the packing bench book for carton PK-8804?",
"""
Kestrel Parcel — Account Service Rules

1. Dimensional weight (kg) = length × width × height in cm ÷ 5,000.
2. Chargeable weight = the greater of actual weight and dimensional weight.
3. Services
 - Standard parcel: chargeable weight up to 30 kg and longest side up to 120 cm.
 - Oversize parcel: chargeable weight over 30 kg up to 70 kg, or longest side over 120 cm up to 175 cm.
 - Pallet freight: anything larger or heavier.
4. Parcels over 25 kg actual weight carry a two-person lift label.

Carton PK-8804 (flat-pack wardrobe, Duneside DC)
Dimensions: 110 × 60 × 50 cm
Actual weight: 18 kg
""",
[("standard_parcel", "The carton's weight and size both sit within the standard parcel limits."),
 ("oversize_parcel", "Its chargeable weight falls between 30 and 70 kg, and its longest side is under 120 cm."),
 ("pallet_freight", "Its chargeable weight, once the dimensional weight is worked out, is above the 70 kg oversize limit, so it goes as freight.")],
"oversize_parcel", 2),

# ------------------------------------------------------------------ lg10
# why: missed = arrives > 60 min after slot; grace 120 min if delay notified in the portal
# before the scheduled time. Slot 09:00, notice 08:35, arrival 10:40 (100 min) -> within
# grace -> unload today, no fee. Twin: notice 09:20 (after slot) -> 60-min rule -> missed
# -> rebook next day + £85.
C("lg10", "How should the gatehouse handle vehicle HX-17 from Stanrow Logistics?",
"""
Duneside Distribution Centre — Inbound Booking Rules

1. A delivery arriving more than 60 minutes after its booked slot is a missed appointment.
2. (Amended February) If the carrier reports a delay through the booking portal before the booked slot time, the limit in rule 1 is 120 minutes instead of 60.
3. Missed appointment: the load is rebooked for the next available day and an £85 fee is charged.
4. Loads arriving early wait for their slot.

Booking B-22614
Carrier: Stanrow Logistics, vehicle HX-17
Slot: 09:00, door 12
Portal message from Stanrow: 08:35 — "Held at the Carden roadworks, running about 90 minutes late."
Gate arrival: 10:40
""",
[("unload_today", "The delay was reported before the slot, so the 120-minute limit applies and the truck is within it."),
 ("rebook_with_fee", "The truck arrived later than the limit that applies to this booking allows, so the appointment is missed."),
 ("unload_today_with_fee", "The truck may unload but is charged the fee because it arrived late.")],
"unload_today", 2,
twin=T([("Portal message from Stanrow: 08:35 —", "Portal message from Stanrow: 09:20 —")], "rebook_with_fee")),

# ------------------------------------------------------------------ lg11
# why: value = units x standard cost (not retail): 120 x £38 = £4,560 -> band £500-£5,000
# -> Regional Operations Director. Twin: 140 units -> £5,320 -> Finance Director.
C("lg11", "Who must approve stock write-off WO-2026-118?",
"""
Marlow & Pike Home — Stock Write-Off Authority

1. Write-off value = number of units × standard cost from the item master. Retail price is not used.
2. Approval limits
 - up to £500: Site Manager;
 - over £500 up to £5,000: Regional Operations Director;
 - over £5,000: Finance Director.
3. Write-offs caused by a single incident may not be split across requests.

Item master (extract)
| SKU | Description | Standard cost | Retail price |
| LMP-220 | ceramic table lamp | £38.00 | £65.00 |
| RUG-140 | wool rug 140 cm | £52.00 | £120.00 |

WO-2026-118
SKU: LMP-220
Units: 120 (water damage from roof leak, bay C-09, single incident)
Raised by: Site Manager, Duneside
""",
[("site_manager", "The site manager raised the request and write-offs are approved on site."),
 ("regional_operations_director", "At standard cost the write-off is over £500 but not over £5,000."),
 ("finance_director", "The write-off is valued above £5,000.")],
"regional_operations_director", 2),

# ------------------------------------------------------------------ lg12
# why: FEFO, but contract needs >= 60 days' remaining life at dispatch. Dispatch 28 Aug:
# lot A (20 Oct) = 53 days -> excluded; lot B (2 Nov) = 66 days -> pick B.
# Twin: dispatch 18 Aug -> lot A = 63 days -> pick A.
C("lg12", "Which lot should be picked for order SO-7702?",
"""
Greyling Fresh Foods — Ambient Picking Rules

1. Pick first-expiry-first-out (FEFO): the lot with the earliest best-before date that meets rule 2.
2. Customer contracts may set a minimum remaining shelf life at dispatch; lots below it must not be picked for that customer.
3. Remaining shelf life = days from the dispatch date to the best-before date.

Customer contract — Haverley Stores: minimum remaining shelf life at dispatch 60 days.

Order SO-7702
Customer: Haverley Stores
Item: jarred pesto 190 g, 30 cases
Dispatch date: 28 August

Available lots (each holds at least 30 cases)
| Lot | Best before |
| A | 20 October |
| B | 2 November |
| C | 15 December |
""",
[("pick_lot_a", "Lot A has the earliest best-before date and still meets the 60-day minimum at dispatch."),
 ("pick_lot_b", "Lot A falls short of 60 days at dispatch, so the earliest lot that qualifies is B."),
 ("pick_lot_c", "Haverley should get the freshest stock available.")],
"pick_lot_b", 2,
twin=T([("Dispatch date: 28 August", "Dispatch date: 18 August")], "pick_lot_a")),

# ------------------------------------------------------------------ lg13
# why: legal minimum 1 mm, but amendment: steer-axle tyres below 2 mm are dangerous
# defects -> vehicle off road. Front nearside = steer axle (axle table). 1.4 mm < 2 mm.
# Twin: rear offside inner (drive axle) -> 1.4 mm >= 1 mm -> minor? No: rear below 2mm
# is only advisory -> fleet rule: tyres between 1 and 2 mm on other axles are minor ->
# drive and book repair within 7 days.
C("lg13", "What should the transport manager decide after the walkaround check on vehicle RK-24?",
"""
Hallam Haulage — Daily Walkaround Defect Rules

1. Dangerous defects (vehicle off road until repaired): brake faults, steering faults, any tyre with cord exposed, any tyre with tread below 1 mm.
2. (Company rule added 2025) A steer-axle tyre with tread below 2 mm is also a dangerous defect.
3. Minor defects (vehicle may run; repair within 7 days): any tyre with tread from 1 mm to below 2 mm not covered by rule 2, lamp faults, wiper faults.
4. No defect: tread 2 mm or more and no other issue.

Axle layout — RK-24 (6-wheel rigid)
| Axle | Type |
| front | steer |
| rear | drive (twin wheels) |

Walkaround report, 05:40
Driver: A. Kowal
Defect: front nearside tyre, tread measured at 1.4 mm across the centre.
All lamps, wipers and brakes OK.
""",
[("vehicle_off_road", "The worn tyre is on the steer axle and below the company's 2 mm minimum for that axle."),
 ("drive_and_book_repair", "The tread is above the 1 mm legal minimum, so it is a minor defect to fix within 7 days."),
 ("no_defect", "Nothing in the report reaches the defect list.")],
"vehicle_off_road", 2,
twin=T([("Defect: front nearside tyre, tread", "Defect: rear offside inner tyre, tread")], "drive_and_book_repair")),

# ------------------------------------------------------------------ lg14
# why: signature required when declared value >= £250; £320 -> signature parcel ->
# redirect only to an address on the account; workplace not on account -> no redirect;
# attempt 1 only -> second attempt at original address. Twin: £220 -> redirect allowed
# (same postcode area, before 2nd attempt) -> redirect.
C("lg14", "What should the depot do with parcel KP-0093318?",
"""
Kestrel Parcel — Redirection Rules (receiver-requested)

1. Definitions: a "signature parcel" is any parcel with a declared value of £250 or more.
2. A parcel may be redirected before the second delivery attempt to another address in the same postcode area.
3. A signature parcel may be redirected only to an address already saved on the receiver's account.
4. After two failed attempts the parcel is returned to sender.

Parcel KP-0093318
Declared value: £320
Receiver account addresses: 14 Linden Row, Harwick HW3 2PL
Attempt 1: Tuesday, no answer. Card left.
Receiver request (Tuesday evening): "Please send it to my office instead: Unit 5, Fenner Park, Harwick HW3 9TB."
""",
[("redirect_parcel", "The request came before the second attempt and the office is in the same postcode area, so redirection is allowed."),
 ("second_attempt_original_address", "It is a signature parcel and the office is not saved on the account, so it cannot be redirected there."),
 ("return_to_sender", "A failed delivery means the parcel goes back to the sender.")],
"second_attempt_original_address", 2,
twin=T([("Declared value: £320", "Declared value: £220")], "redirect_parcel")),

# ------------------------------------------------------------------ lg15
# why: bonded goods leave only when their own entry number shows released. Pallet label
# says E-5528, which is held for inspection (E-5582 is the released one) -> keep in bond.
# Driver's claim is not evidence. Twin: label E-5582 -> released -> load.
C("lg15", "Can pallet P-3307 be loaded onto the 16:00 trailer?",
"""
Duneside Distribution Centre — Bonded Area Procedure

1. Goods in the bonded area may leave only after customs releases the entry that covers them.
2. The covering entry is the entry number printed on the pallet label. Paperwork in the trailer pack does not replace it.
3. Released entries show status "released" in the customs status screen; any other status means the goods stay in bond.

Customs status screen, 15:40
| Entry | Status |
| E-5582 | released 09:12 |
| E-5528 | held for documentary check |
| E-5601 | released 13:47 |

Pallet P-3307 label: entry E-5528; 40 cartons, bicycle helmets.
Driver (Ostry Cycles collection): "Customs cleared everything this morning, the office told me."
""",
[("load_pallet", "The entry printed on the pallet label shows as released, so the pallet can go."),
 ("keep_in_bond", "The entry printed on the pallet label is not released, so the pallet stays in bond."),
 ("load_with_paperwork_check", "The pallet may be loaded once the trailer pack paperwork has been checked against the customs release the driver was told about.")],
"keep_in_bond", 1),

# ------------------------------------------------------------------ lg16
# why: 12 pallets <= 20; postcode KX9 is zone 4 (islands) -> Isleway (zone 4 carrier).
# Twin: KX7 -> zone 3 -> Hallam (contract carrier zones 1-3).
C("lg16", "Which carrier should the planner book for shipment SH-4411?",
"""
Greyling Fresh Foods — Carrier Selection Rules

1. Shipments of more than 20 pallets go out to spot tender.
2. Otherwise:
 - zones 1 to 3: Hallam Haulage (contract carrier);
 - zone 4 (islands): Isleway Freight.
3. Zone is set by the delivery postcode district (table below).
4. Chilled loads must use a carrier holding a current temperature-control audit; both carriers below hold one.
5. Bookings for next-day delivery close at 14:00.

Postcode zones (extract)
| District | Zone |
| KX1 - KX4 | 2 |
| KX5 - KX8 | 3 |
| KX9 | 4 |

Shipment SH-4411
Pallets: 12
Delivery: Crane Wharf Stores, KX9 1AB
Planner note: "Hallam delivered KX7 last week without issue."
""",
[("book_hallam_haulage", "The delivery postcode is in zones 1 to 3 and the shipment is 20 pallets or fewer."),
 ("book_isleway_freight", "The delivery postcode is in zone 4, so the islands carrier is used."),
 ("spot_tender", "The shipment is large enough to go out to tender.")],
"book_isleway_freight", 1),

# ------------------------------------------------------------------ lg17
# why: damage % is by cases on the pallet per ASN (not units). 3 of 48 cases = 6.25% >= 5%
# -> refuse. Units basis (14 of 576 = 2.4%) is the mistake.
# Twin: 2 damaged cases -> 2/48 = 4.2% < 5% -> accept and claim.
C("lg17", "What should goods-in do with pallet 2 of delivery ASN-66120?",
"""
Duneside Distribution Centre — Damaged Inbound Pallets

1. Damage rate = damaged cases ÷ cases on that pallet according to the ASN (advance shipping notice). Units inside cases are not counted.
2. Damage rate below 5%: accept the pallet, set damaged cases aside and claim for them.
3. Damage rate of 5% or more: refuse the whole pallet.
4. A case counts as damaged if any unit inside it is damaged.

ASN-66120, pallet 2: 48 cases × 12 units (576 units), ceramic mugs.

Check at receipt
Crushed corner; 3 cases affected; broken mugs found: 14 units in total across those cases.
Driver: "It's only 14 mugs out of nearly 600."
""",
[("accept_pallet", "Fourteen broken mugs is a very small share, so the pallet is accepted without a claim."),
 ("accept_and_claim_cases", "The damage rate by cases is under 5%, so the pallet is accepted and the damaged cases claimed."),
 ("refuse_pallet", "Damaged cases make up 5% or more of the cases on the pallet.")],
"refuse_pallet", 2,
twin=T([("Crushed corner; 3 cases affected;", "Crushed corner; 2 cases affected;")], "accept_and_claim_cases")),

# ------------------------------------------------------------------ lg18
# why: to deny a non-delivery claim, the POD needs BOTH a photo and GPS within 50 m of
# the address. GPS 180 m -> fails -> reship (value £60 < £500 so no investigation).
# Twin: GPS 35 m -> both met -> deny.
C("lg18", "How should the claims desk resolve non-delivery claim ND-2208?",
"""
Kestrel Parcel — Non-Delivery Claims

1. A claim is denied only if the proof of delivery (POD) has both (a) a delivery photo and (b) a GPS position within 50 m of the delivery address.
2. If either (a) or (b) is missing or fails, the parcel is reshipped at no cost to the customer.
3. Claims for parcels valued above £500 are also passed to the investigations team.

POD record — parcel KP-1180442
Declared value: £60
Delivery type: safe place (porch)
Photo: yes (parcel on a doorstep, door number not visible)
GPS distance from delivery address: 180 m
Customer statement: "Nothing arrived. That photo isn't my porch."
""",
[("deny_claim", "The POD meets both conditions: a delivery photo and a GPS position within 50 m of the address."),
 ("reship_no_cost", "The GPS position is more than 50 m from the address, so the POD fails and the parcel is reshipped."),
 ("refer_to_investigations", "The customer disputes the delivery photo, and disputed safe-place deliveries have to be passed to the investigations team first.")],
"reship_no_cost", 1),
]
