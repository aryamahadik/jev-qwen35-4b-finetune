"""proc_routing / warehouse and transport exception routing (Brindlecourt Distribution, invented)."""
from _lib import C, T

SP12 = """
BRINDLECOURT DISTRIBUTION — SITE PROCEDURE SP-12 (rev. 9): INBOUND & EXCEPTIONS ROUTING
E1. Damaged inbound goods: Receiving QA.
E2. Chilled goods (2-8 °C) with a temperature excursion: Cold Chain Controller if the logger shows more than 30 continuous minutes outside the range, or any reading above 12 °C; otherwise receive the goods with a note on the delivery record.
E3. Dangerous goods (any package marked with a UN number): DG Officer, including damaged DG packages. E3 outranks E1.
E4. Shortages: if the missing quantity is more than 5% of the ordered quantity on that order line, Claims Desk; 5% or less, adjust the receipt and note it.
E5. Lost or missing consignments with a declared value of £10,000 or more: Site Security. Under £10,000: Claims Desk.
E6. Night shift (22:00-06:00): only the DG Officer and the Cold Chain Controller are on call. Other exceptions are logged for the day shift.
"""

ITEMS = [
# ------------------------------------------------------------------ lo01
# why: line 2 ordered 480, received 452 -> 28 missing; 28/480 = 5.83% > 5% ->
#      Claims Desk. Consignment-level % (28/1,200) is the wrong base.
#      twin received 460 -> 20/480 = 4.17% -> adjust and note.
C("rt_lo01", "How should this shortage be routed?",
SP12 + """
Goods receipt GR-30918 — Tuesday 10:40, Bay 6
Supplier: Harwood Housewares. Consignment: 3 order lines, 1,200 units ordered in total.
Line 1: tea towels — ordered 400, received 400.
Line 2: ceramic mugs — ordered 480, received 452.
Line 3: oven gloves — ordered 320, received 320.
Condition: all cartons intact; no damage.
Receiver note: "Across the whole delivery we are only 28 units down, which is tiny."
""",
[("route_claims_desk", "Line 2 is 28 units short of 480, which is 5.8% of the ordered quantity, over 5%, so the Claims Desk takes it."),
 ("adjust_receipt_and_note", "The missing quantity is 5% or less of the ordered quantity on the line, so the receipt is adjusted and noted."),
 ("route_receiving_qa", "Short deliveries are inbound problems for Receiving QA."),
 ("route_site_security", "Mugs are missing even though every carton arrived intact, which points to theft before loading, so Site Security investigates the shortage before any claim.")],
"route_claims_desk", 2,
twin=T([("ordered 480, received 452", "ordered 480, received 460")], "adjust_receipt_and_note")),

# ------------------------------------------------------------------ lo02
# why: out of range 09:12-09:37 = 25 min (< 30), peak 9.4 °C (< 12) -> receive
#      with a note. twin 09:12-09:57 = 45 min -> Cold Chain Controller.
C("rt_lo02", "What should the receiver do with this chilled delivery?",
SP12 + """
Goods receipt GR-31002 — Wednesday 09:58, Chilled Dock 2
Supplier: Pennock Dairies. Product: yoghurt multipacks, 18 pallets, required range 2-8 °C.
Trailer logger summary: in range throughout, except 09:12 to 09:37 during the door-open period at the previous drop, when it read above 8 °C.
Peak reading: 9.4 °C at 09:25.
Probe check on arrival: 5.1 °C.
Driver comment: "The customer before you took ages to unload."
""",
[("receive_with_note", "The excursion lasted 25 minutes and peaked at 9.4 °C, within both E2 limits, so the goods are received with a note."),
 ("route_cold_chain_controller", "The logger shows more than 30 continuous minutes outside the range, so E2 sends it to the Cold Chain Controller."),
 ("reject_delivery", "The logger shows readings above 8 °C, and a chilled load that has been outside its 2-8 °C range at any point must be refused at the dock."),
 ("route_receiving_qa", "Temperature problems are a kind of damage for Receiving QA.")],
"receive_with_note", 1,
twin=T([("except 09:12 to 09:37", "except 09:12 to 09:57")], "route_cold_chain_controller")),

# ------------------------------------------------------------------ lo03
# why: UN3480 marking -> dangerous goods -> DG Officer, outranking E1 damage.
#      twin: garden chairs, no UN marking -> damaged inbound -> Receiving QA.
C("rt_lo03", "Who should handle this damaged pallet?",
SP12 + """
Goods receipt GR-31140 — Thursday 14:20, Bay 3
Supplier: Voltaris Power Supplies. One pallet of cartons marked UN3480 (lithium-ion batteries).
Condition: forklift damage on arrival; bottom-corner cartons crushed; no smell, smoke or heat observed.
Receiver note: "Photographed, pallet isolated in the quarantine lane."
""",
[("route_dg_officer", "The cartons are marked UN3480, so they are dangerous goods, and E3 sends damaged DG packages to the DG Officer because E3 outranks the E1 damage rule."),
 ("route_receiving_qa", "It is a damaged inbound pallet with no UN marking, so E1 sends it to Receiving QA."),
 ("route_claims_desk", "The pallet was crushed by a forklift before it reached Bay 3, so this is transit damage caused by the carrier and the Claims Desk recovers the cost."),
 ("route_site_security", "An isolated pallet is a security hold.")],
"route_dg_officer", 1,
twin=T([("One pallet of cartons marked UN3480 (lithium-ion batteries).", "One pallet of cartons of folding garden chairs (no UN marking).")],
       "route_receiving_qa")),

# ------------------------------------------------------------------ lo04
# why: hold reason is sanctions screening -> Trade Compliance.
C("rt_lo04", "Which desk should handle this customs hold?",
"""
Brindlecourt Distribution — Import Exceptions Note IE-4
IE4.1 Customs holds for tariff classification or valuation queries go to the Customs Broker desk (Harlan & Voss), who answer the authority.
IE4.2 Holds for sanctions or export-control screening go to Trade Compliance. The broker must not respond on these.
IE4.3 Physical examinations are booked by the Customs Broker desk.
IE4.4 Delays over five days on any hold are reported to the customer's account manager.

Customs status update — container BDCU 208817-3, Felixport terminal
Consignee: Brindlecourt Distribution for Teodor Marine Supply
Status: HOLD
Hold reason: "Consignee's end customer matched an entry on a sanctions screening list; awaiting compliance clearance."
Days on hold: 2
Broker's email: "We can probably answer this ourselves if you send us the invoices."
""",
[("route_trade_compliance", "The hold is for sanctions screening, which IE4.2 sends to Trade Compliance, not the broker."),
 ("route_customs_broker_desk", "Customs holds are answered by the Customs Broker desk, which has offered to deal with it."),
 ("report_to_account_manager", "Holds are reported to the customer's account manager."),
 ("route_claims_desk", "A container stuck at the terminal is a delayed consignment for the Claims Desk.")],
"route_trade_compliance", 1),

# ------------------------------------------------------------------ lo05
# why: declared value £12,400 >= £10,000 -> Site Security.
#      twin £8,400 -> Claims Desk.
C("rt_lo05", "Where should this missing consignment be reported?",
SP12 + """
Exception EX-5520 — Monday 11:30
Consignment: 1 pallet, laptops and docking stations for Kittering Home Stores
Declared value on the consignment note: £12,400
Status: scanned onto trailer TR-88 at 06:10; not scanned off at the destination hub; not found in a trailer search.
Driver statement: "Trailer seal was intact on arrival."
""",
[("route_site_security", "The declared value on the consignment note is £12,400, which is £10,000 or more, so E5 sends the lost pallet to Site Security rather than the Claims Desk."),
 ("route_claims_desk", "The declared value is under £10,000, so the lost pallet goes to the Claims Desk."),
 ("route_receiving_qa", "The pallet was scanned onto the trailer but never scanned off at the hub, which makes it an inbound receiving discrepancy for Receiving QA.")],
"route_site_security", 1,
twin=T([("Declared value on the consignment note: £12,400", "Declared value on the consignment note: £8,400")], "route_claims_desk")),

# ------------------------------------------------------------------ lo06
# why: delay 14:00 Tue -> 20:00 Wed = 30 h > 24; Halvorsen Marine is Tier B ->
#      Transport Planning. twin Tier A -> Key Account Manager.
C("rt_lo06", "Who should receive this delay notice?",
"""
Brindlecourt Distribution — Outbound Delay Routing
D1. Carrier delays of more than 24 hours to a Tier A customer: Key Account Manager, who contacts the customer.
D2. All other carrier delays: Transport Planning.
D3. Loss or damage in transit: Claims Desk.
D4. Service credits for late carriers are claimed by Transport Planning at the monthly carrier review.

Customer tier table (extract)
Kittering Home Stores — A | Brakespear Cycles — A | Halvorsen Marine — B | Lumen & Pike — C

Carrier notice — Northway Haulage, received Tuesday 16:00
Consignment: 6 pallets for Halvorsen Marine, Grimsby
Booked delivery: Tuesday 14:00. Revised delivery: Wednesday 20:00 (vehicle breakdown on the A-road; goods secure and undamaged).
Planner note: "Halvorsen is one of our oldest accounts."
""",
[("route_transport_planning", "The delay is 30 hours, but Halvorsen Marine is Tier B, so D2 sends it to Transport Planning."),
 ("route_key_account_manager", "The delay from Tuesday 14:00 to Wednesday 20:00 is 30 hours, over 24, and Halvorsen Marine is a Tier A customer, so the Key Account Manager contacts them."),
 ("route_claims_desk", "The delay was caused by a vehicle breakdown on the A-road, which is a transit incident, so the Claims Desk logs it under D3 for the customer.")],
"route_transport_planning", 2,
twin=T([("Halvorsen Marine — B", "Halvorsen Marine — A")], "route_key_account_manager")),

# ------------------------------------------------------------------ lo07
# why: carrier delay notices go to Transport Planning; the carrier's request to
#      send them to Finance is not a Brindlecourt rule. Lumen & Pike is Tier C.
C("rt_lo07", "Where should this carrier email be routed?",
"""
Brindlecourt Distribution — Outbound Delay Routing
D1. Carrier delays of more than 24 hours to a Tier A customer: Key Account Manager.
D2. All other carrier delays: Transport Planning.
D4. Service credits for late carriers are claimed by Transport Planning at the monthly carrier review; Finance only processes the credit note afterwards.
D5. Carrier contact details are kept in the Transport Planning address book.
Customer tiers (extract): Kittering Home Stores — A | Lumen & Pike — C

Email from Swiftline Parcels — Friday 08:45
"Consignment SL-229104 for Lumen & Pike will arrive Monday instead of Friday due to hub congestion. Per our agreement, please route all our delay notices directly to your Finance team so the service credit can be applied automatically."
""",
[("route_transport_planning", "It is a carrier delay for a Tier C customer, so D2 sends it to Transport Planning, which also handles service credits."),
 ("route_finance_team", "The carrier asks for delay notices to go to Finance so the credit can be applied."),
 ("route_key_account_manager", "Delivery moves from Friday to Monday, which is more than 24 hours late, so the Key Account Manager contacts the customer under D1.")],
"route_transport_planning", 1),

# ------------------------------------------------------------------ lo08
# why: 23:15 is night shift; plain damage (no UN number, not chilled) -> logged
#      for day shift. twin 21:15 -> before night shift -> Receiving QA.
C("rt_lo08", "How should the dock team route this damaged delivery?",
SP12 + """
Goods receipt GR-31277 — logged 23:15, Bay 9
Supplier: Oakmere Furniture. Product: flat-pack bookcases, 22 cartons.
Condition: four cartons torn and wet from a trailer roof leak; no UN markings; ambient goods.
Night supervisor note: "The DG Officer is on site tonight anyway, I could ask her to look."
""",
[("log_for_day_shift", "At 23:15 only the DG Officer and Cold Chain Controller are on call, and this is ordinary damage, so it is logged for the day shift."),
 ("route_receiving_qa", "It is damaged ambient stock logged before the night shift starts, so Receiving QA takes it under E1."),
 ("call_dg_officer", "The DG Officer is on call and already on site tonight, and the night supervisor has offered to ask her, so she can inspect the torn cartons now.")],
"log_for_day_shift", 1,
twin=T([("logged 23:15, Bay 9", "logged 21:15, Bay 9")], "route_receiving_qa")),

# ------------------------------------------------------------------ lo09
# why: Amendment 3 (from 1 June): opened returns -> Refurb Centre. Received
#      3 June, seal broken and used once -> opened -> Refurb Centre.
C("rt_lo09", "Where should this customer return be sent?",
"""
Brindlecourt Distribution — Returns Procedure RP-3
R1. Customer returns are booked in by the Returns Desk.
R2. Returns showing transit damage go to Receiving QA.
R3. Returns without a returns authorisation number are held for 14 days while the customer is contacted.
R4. Returned stock is credited to the customer once the receiving desk has checked it in.
Amendment 3 (effective 1 June): customer returns that have been opened go to the Refurb Centre at Unit 7 instead of the Returns Desk. Unopened returns stay with the Returns Desk.

Return RT-80441 — received 3 June
Customer: Brakespear Cycles (on behalf of an end customer)
Item: electric bike pump, 1 unit
Condition: outer seal broken, pump used once; box undamaged; all parts present.
Returns authorisation: RA-55102.
Customer reason: "Too noisy."
""",
[("route_refurb_centre", "It was received on 3 June, after Amendment 3 took effect, and the seal is broken and the pump used, so as an opened return it goes to the Refurb Centre."),
 ("route_returns_desk", "Customer returns are booked in by the Returns Desk under R1."),
 ("route_receiving_qa", "The pump has been used, and a returned item that has been used counts as damaged stock, so it goes to Receiving QA under R2.")],
"route_refurb_centre", 1),

# ------------------------------------------------------------------ lo10
# why: difference 905 - 820 = 85 kg; 85/820 (declared) = 10.4% > 10% -> audit.
#      Using weighed weight as base (85/905 = 9.4%) is wrong.
#      twin 890: 70/820 = 8.5% -> accept and file.
C("rt_lo10", "What routing does this weight discrepancy need?",
"""
Brindlecourt Distribution — Carrier Billing Procedure CB-2
CB2.1 Each inbound consignment is weighed at the gate.
CB2.2 If the weighed weight differs from the declared weight by more than 10% of the declared weight, the consignment is sent to Carrier Billing Audit before the carrier invoice is paid.
CB2.3 Otherwise the gate weight is filed and the consignment is accepted.
CB2.4 Damage found at the gate follows SP-12.
CB2.5 The gate scales are calibrated every six months; the last calibration was on 2 January.
CB2.6 Weight disputes older than 90 days are not raised with the carrier.

Gate record GT-44120 — Thursday 07:50
Carrier: Northway Haulage. Consignment: 2 pallets of floor tiles.
Declared weight: 820 kg. Weighed weight: 905 kg.
Gatehouse note: "Pallets wrapped and intact."
""",
[("route_carrier_billing_audit", "905 kg is 85 kg over the 820 kg declared, which is 10.4% of the declared weight, over 10%, so it goes to Carrier Billing Audit."),
 ("accept_and_file_weight", "The difference is 10% or less of the declared weight, so the gate weight is filed and the consignment accepted."),
 ("route_receiving_qa", "A consignment that weighs more than declared suggests broken or substituted tiles inside the wrap, so Receiving QA inspects it before the invoice is paid.")],
"route_carrier_billing_audit", 2,
twin=T([("Weighed weight: 905 kg.", "Weighed weight: 890 kg.")], "accept_and_file_weight")),

# ------------------------------------------------------------------ lo11
# why: batch L2233 is inside the recalled range L2230-L2235 -> Quarantine &
#      Recall Coordinator, not the Returns Desk.
C("rt_lo11", "Where should returned batch L2233 go?",
"""
Brindlecourt Distribution — Recall Procedure RC-1
RC1.1 Items from batches listed on an open recall notice go to the Quarantine & Recall Coordinator, not the Returns Desk, whatever their condition.
RC1.2 Other customer returns follow the Returns Procedure (Returns Desk, or the Refurb Centre for opened items).
RC1.3 The Quarantine & Recall Coordinator reports recalled units received each week to the brand owner.
RC1.4 Closed recall notices are archived and no longer apply.

Open recall notice RN-88 (issued 12 May): Kittering Home Stores own-brand 1.7 L kettles, batches L2230 to L2235 inclusive — risk of lid hinge failure.

Return RT-80502 — received 20 May
Item: Kittering 1.7 L kettle, batch L2233
Condition: unopened, factory sealed
Customer reason: "Bought two by mistake."
""",
[("route_recall_coordinator", "Batch L2233 lies within the recalled range L2230 to L2235, so RC1.1 sends it to the Quarantine & Recall Coordinator."),
 ("route_returns_desk", "It is unopened, factory sealed and returned because the customer bought two by mistake, so the Returns Desk books it in under RC1.2."),
 ("route_refurb_centre", "Kettles from a recalled product line are refurbished at Unit 7.")],
"route_recall_coordinator", 1),

# ------------------------------------------------------------------ lo12
# why: collision with no injury -> Fleet Team only.
#      twin: driver sprained wrist -> injury -> Fleet + Health & Safety.
C("rt_lo12", "Who must be told about this vehicle incident?",
"""
Brindlecourt Distribution — Vehicle Incident Procedure VI-1
VI1.1 Every vehicle incident is reported to the Fleet Team.
VI1.2 If anyone is injured, the Health & Safety Advisor is also notified within one hour.
VI1.3 If goods are stolen from a vehicle, Site Security is also notified.
VI1.4 Damage to goods follows SP-12 once the vehicle returns.
VI1.5 Photographs of the scene are uploaded to the fleet app before the driver leaves.

Incident report VI-2217 — Friday 15:40
Vehicle: 18-tonne rigid, reg. BD-417
Driver: Kasia Lewandowska
What happened: reversing into Bay 12 at the Harrowgate customer site, the tail-lift clipped a bollard; tail-lift bent, bollard loose. No one was hurt.
Load: delivered in full before the incident.
""",
[("route_fleet_only", "It is a vehicle incident with no injury and no theft, so only the Fleet Team is told."),
 ("route_fleet_and_health_safety", "Someone was injured, so VI1.2 adds the Health & Safety Advisor to the Fleet Team."),
 ("route_site_security", "Damage at a customer site is a security matter.")],
"route_fleet_only", 1,
twin=T([("No one was hurt.", "The driver sprained her wrist on the cab step.")], "route_fleet_and_health_safety")),

# ------------------------------------------------------------------ lo13
# why: seal 4471902 vs bill of lading 4471920 -> mismatch (transposed digits)
#      -> Site Security before the doors open.
#      twin: identical numbers -> proceed to receiving.
C("rt_lo13", "What should happen before this container is opened?",
"""
Brindlecourt Distribution — Container Receipt Procedure CR-2
CR2.1 The seal number on the container is checked against the seal number on the bill of lading before the doors are opened.
CR2.2 Any mismatch, including a single digit, goes to Site Security, and the doors stay closed until Security releases it.
CR2.3 Matching seals: the container proceeds to Receiving.
CR2.4 Customs holds are handled under IE-4.
CR2.5 Seals removed after release are bagged and kept for 30 days.

Container arrival — Bay 14, Monday 07:05
Container: BDCU 552183-0, from Felixport
Seal number read at the gate: 4471902
Seal number on the bill of lading: 4471920
Driver: "Nobody has touched it since the port."
""",
[("hold_for_site_security", "The gate reading 4471902 and the bill of lading 4471920 differ in two digits, so under CR2.2 the container goes to Site Security with the doors kept closed."),
 ("proceed_to_receiving", "The seal on the container matches the bill of lading, so the container proceeds to Receiving."),
 ("route_customs_broker_desk", "The container has come in from Felixport with a discrepancy on the bill of lading, so the Customs Broker desk resolves it under CR2.4.")],
"hold_for_site_security", 2,
twin=T([("Seal number on the bill of lading: 4471920", "Seal number on the bill of lading: 4471902")], "proceed_to_receiving")),

# ------------------------------------------------------------------ lo14
# why: POD signed but GPS stamp 140 m from the address (> 50 m) -> Claims Desk
#      investigation.
C("rt_lo14", "How should this non-delivery claim be routed?",
"""
Brindlecourt Distribution — Proof of Delivery Procedure POD-1
P1. When a customer says a delivery did not arrive, the proof of delivery (POD) is checked.
P2. If the POD is signed and its GPS stamp is within 50 metres of the delivery address, Customer Service sends the POD to the customer.
P3. If the POD is unsigned, or the GPS stamp is more than 50 metres from the delivery address, the case goes to the Claims Desk for investigation.
P4. Driver statements are gathered by the Claims Desk.

Case ND-6091 — Wednesday
Customer: Brakespear Cycles, Unit 4, Fenner Trading Estate
Claim: "Our 3 cartons of inner tubes never arrived."
POD: signed "J. Brook" at 11:42; GPS stamp 140 metres from Unit 4 (outside Unit 7 on the same estate).
Driver note on the handheld: "Left with reception."
""",
[("route_claims_desk", "The POD is signed, but its GPS stamp is 140 metres from Unit 4, more than 50 metres, so P3 sends the case to the Claims Desk for investigation."),
 ("send_pod_via_customer_service", "The POD is signed, so Customer Service sends it to the customer."),
 ("route_site_security", "The cartons were left at Unit 7 instead of Unit 4 and may have been taken by someone there, so Site Security investigates the loss first.")],
"route_claims_desk", 1),
]
