"""proc_tradeoff / shipping methods, carriers, routes and logistics choices.
12 Oct 2026 = Monday. All organisations, people, products and places are
invented."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ sh01
# why: standalone Li-ion 160 Wh each -> Air Express refuses standalone > 100 Wh.
# Dispatch Mon 12 Oct; business days after dispatch: Ground Express 3 -> Thu 15 Oct
# (<= Fri 16); Ground Standard 5 -> Mon 19 Oct (late). Cheapest allowed on time =
# Ground Express. Twin: deadline Mon 19 Oct -> Ground Standard ($31) cheapest.
C("sh01", "Which courier service should be booked for the battery parcel?",
"""
Dispatch note DN-60412 — Aerolens Surveys (stores)
Contents: 2 spare lithium-ion batteries for survey drones, 160 Wh each, packed on their own (not installed in any equipment).
Dispatch: Monday 12 October 2026.
Customer requirement: delivery by Friday 16 October 2026.

Shipping rule SR-2: book the cheapest service that is allowed to carry the goods and arrives by the customer's date. Transit times are business days after the day of dispatch.

Skylane Couriers service guide
| Service | Transit | Price | Lithium batteries |
| Air Express | 1 business day | $96 | standalone batteries above 100 Wh not accepted; batteries installed in equipment accepted |
| Ground Express | 3 business days | $54 | accepted |
| Ground Standard | 5 business days | $31 | accepted |

Stores assistant's note: "They're drone batteries, so they count as part of the drone. Air would be safest for the deadline."
Packaging: UN-rated battery box, terminals taped.
""",
[("air_express", "The batteries belong to the customer's drones, so they count as installed and air is allowed and fastest."),
 ("ground_express", "Air refuses these batteries, and Ground Express is the cheapest remaining service that arrives by the deadline."),
 ("ground_standard", "Ground Standard arrives by the customer's date and is the cheapest service allowed to carry the batteries.")],
"ground_express", 2,
twin=T([("Customer requirement: delivery by Friday 16 October 2026.", "Customer requirement: delivery by Monday 19 October 2026.")], "ground_standard")),

# ------------------------------------------------------------------ sh02
# why: A due Wed 14 Oct; B due Fri 16 Oct, B receives Fridays only. Separate LTL:
# 1,450 + 1,050 = 2,500, meets both. FTL Wed ($2,100) delivers B on Wed -> outside
# B's window. FTL Fri -> A late. -> separate.
# Twin: B receives Mon-Fri -> FTL Wed meets both at $2,100 -> consolidate Wed.
C("sh02", "How should the two Deane orders be shipped?",
"""
Transport planning sheet — Westfold Timber, week 42

Orders to the Deane area
- Order A: Hollis Hardware, 6 pallets, must arrive by Wednesday 14 October.
- Order B: Tarn Garden Centre, 4 pallets, must arrive by Friday 16 October. Receiving hours at Tarn: Fridays only, 07:00-12:00.

Planning rules
TP-1. Every delivery must arrive on or before its due date and within the customer's receiving hours. Early delivery is fine only if it falls within those hours.
TP-2. Choose the cheapest option meeting TP-1.

Options quoted by Brannock Haulage
| Option | Cost | Delivery |
| Separate LTL loads | $1,450 (A, Wednesday) + $1,050 (B, Friday) | A Wednesday, B Friday |
| One full truckload on Wednesday | $2,100 | both Wednesday |
| One full truckload on Friday | $2,100 | both Friday |

Sales note: "Tarn are a good customer; I'm sure they'd take it on Wednesday if we ask nicely."
""",
[("separate_ltl", "Tarn only receives on Fridays, so two separate loads are the only way to meet both customers' dates and hours."),
 ("consolidate_wednesday", "A Wednesday full truckload costs $2,100 against $2,500 for two loads, and both customers can receive it on Wednesday."),
 ("consolidate_friday", "A single Friday truck is cheapest and suits Tarn's hours; Hollis's date is only a target.")],
"separate_ltl", 2,
twin=T([("Receiving hours at Tarn: Fridays only, 07:00-12:00.", "Receiving hours at Tarn: Monday to Friday, 07:00-12:00.")], "consolidate_wednesday")),

# ------------------------------------------------------------------ sh03
# why: -18 C throughout; passive packaging must hold for transit + 12 h buffer; arrive
# within 48 h. Gel: holds 24 < 36+12 -> fail. Dry ice: holds 72 >= 48, transit 36 <= 48
# -> ok $180. Reefer: active, transit 60 > 48 -> fail. -> dry ice.
# Twin: arrival within 72 h -> reefer ($140) meets and is cheaper.
C("sh03", "Which cold-chain option should be used for the frozen seafood order?",
"""
Order FS-2208 — Salt & Harbour Seafoods to Ellery Street Kitchen, Vantor
Goods: 180 kg frozen scallops and prawns.

Cold Chain Standard (CCS-3)
- Product must stay at or below -18 C from dispatch to delivery.
- Passive packaging (gel packs, dry ice) must be rated to hold temperature for the planned transit time plus a 12-hour buffer. Actively refrigerated vehicles need no buffer.
- The customer contract requires delivery within 48 hours of dispatch.
- Choose the cheapest option meeting all of the above.

Options
| Option | Temperature control | Planned transit | Price |
| Gel-pack courier | passive, rated 24 h | 36 h | $120 |
| Dry-ice courier | passive, rated 72 h | 36 h | $180 |
| Reefer LTL | active refrigeration | 60 h | $140 |

Dispatcher's note: "Gel packs worked fine on the short Carlow run last week."
""",
[("gel_pack_courier", "Gel packs are cheapest, and the 12-hour buffer rule only applies to air freight, so a 24-hour rating covers this road transit."),
 ("dry_ice_courier", "Dry ice is the cheapest option that holds temperature for transit plus buffer and arrives within the customer's deadline."),
 ("reefer_ltl", "Reefer LTL keeps the load frozen for the whole trip, meets the delivery deadline and costs less than dry ice.")],
"dry_ice_courier", 2,
twin=T([("The customer contract requires delivery within 48 hours of dispatch.", "The customer contract requires delivery within 72 hours of dispatch.")], "reefer_ltl")),

# ------------------------------------------------------------------ sh04
# why: in-store window 21 days from dispatch including 3 days customs. Air 5+3 = 8 ok
# ($12,400); sea-air 16+3 = 19 ok ($7,100); sea 32+3 = 35 > 21 fail ($3,800). Duty
# and insurance equal. Lowest landed cost within window = sea-air. Forwarder's claim
# about expediting customs cannot cut 14 days.
C("sh04", "Which freight mode should be booked for the spring collection?",
"""
Import booking — Loom & Larch, spring homewares collection (1 x 40ft equivalent)
Supplier: Sanhe Textiles, Port Mellin. Ready for dispatch: 2 November 2026.

Import rules (Supply Chain Manual 4.1)
- Goods must be in the distribution centre within 21 days of dispatch. Allow 3 days for customs clearance on top of the freight transit time.
- Choose the mode with the lowest landed cost that meets the window. Landed cost = freight + duty + insurance. Duty and insurance are the same for every mode on this shipment.

Forwarder quotes (Castlemere Forwarding)
| Mode | Transit | Freight cost |
| Air | 5 days | $12,400 |
| Sea-air | 16 days | $7,100 |
| Sea (FCL) | 32 days | $3,800 |

Forwarder's email: "Go sea — we can have customs expedited so you'll make the date, trust me."
Marketing note: in-store launch photography is booked for 25 November.
""",
[("air_freight", "Air is the only mode that fits the 21-day window once customs clearance is added."),
 ("sea_air", "Sea-air arrives within the window including customs and has the lowest landed cost of the modes that do."),
 ("sea_fcl", "Sea has the lowest landed cost, and the forwarder's expedited customs clearance will bring it inside the 21-day window.")],
"sea_air", 1),

# ------------------------------------------------------------------ sh05
# why: on-time threshold >= 95% for the most recent quarter (Q2 2026 here, since Q3
# is not closed). Northway Q2 93% fails (annual 97% irrelevant). Bellwether Q2 96% ok
# $2.35. Cairn 98% ok $2.60. Lowest rate among qualifying = Bellwether.
# Twin: Bellwether Q2 94% -> only Cairn qualifies.
C("sh05", "Which carrier should be awarded the Hollin-Vantor lane?",
"""
Carrier Selection Procedure (Pellbrook Paper Mills), lane award
CS-1. A carrier qualifies only if its on-time delivery rate for the most recent completed quarter is at least 95%. Annual averages are shown for information and are not used for qualification.
CS-2. Among qualifying carriers, award the lane to the lowest rate per mile.
Most recent completed quarter: Q2 2026 (Q3 closes on 30 September).

Performance and rates
| Carrier | On-time Q2 2026 | On-time last 12 months | Rate per mile |
| Northway Freight | 93% | 97% | $2.10 |
| Bellwether Haulage | 96% | 94% | $2.35 |
| Cairn Logistics | 98% | 98% | $2.60 |

Lane: Hollin mill to Vantor print works, about 14 loads a week.
Traffic office note: "Northway have always been reliable for us; their yearly figure proves it."
""",
[("award_northway", "Northway's 97% annual on-time rate clears the threshold, and it has the lowest rate."),
 ("award_bellwether", "Bellwether is the cheapest carrier that meets the 95% threshold for the latest quarter."),
 ("award_cairn", "Cairn is the only carrier meeting the 95% threshold for the latest quarter.")],
"award_bellwether", 1,
twin=T([("| Bellwether Haulage | 96% | 94% | $2.35 |", "| Bellwether Haulage | 94% | 94% | $2.35 |")], "award_cairn")),

# ------------------------------------------------------------------ sh06
# why: flammable liquid = flash point <= 60 C; paint flash point 32 C -> flammable.
# Postal: no flammable liquids. Standard courier: only limited quantities with inner
# packagings <= 1 L; cans are 2.5 L -> no. DG service accepts up to 5 L -> only option.
C("sh06", "Which service can carry the floor paint order?",
"""
Customer order WEB-88317 — Kilnhouse Paints online shop
Contents: 4 cans of solvent-based floor paint, 2.5 litres each. Safety data sheet: flash point 32 C.

Dangerous Goods Shipping Guide (warehouse copy)
- A liquid with a flash point of 60 C or below is a flammable liquid for shipping purposes.
- Ostmark Post Tracked ($14): does not accept flammable liquids.
- Parcelrun Standard ($22): accepts flammable liquids only as limited quantities, meaning inner packagings of 1 litre or less.
- Parcelrun Dangerous Goods ($58): accepts flammable liquids in packagings up to 5 litres, with DG labels.
- Book the cheapest service allowed for the goods.

Warehouse lead's note: "Post has taken paint for us before without any problems."
The customer paid $9.95 for shipping at checkout; the difference is absorbed by the shop.
""",
[("post_tracked", "Paint has gone by post before without incident, and post is the cheapest service."),
 ("parcelrun_standard", "Parcelrun Standard accepts flammable liquids, and the 1-litre limit applies to the outer box rather than to each can inside."),
 ("parcelrun_dg", "The paint is a flammable liquid in 2.5-litre cans, so only the dangerous-goods service may carry it.")],
"parcelrun_dg", 1),

# ------------------------------------------------------------------ sh07
# why: 38 t Euro V truck. Route A: bridge limit 32 t gross -> fail. Route C: LEZ bans
# non-Euro VI HGVs 24 h -> fail. Route B (58 km) legal -> B.
# Twin: LEZ applies 07:00-19:00; truck passes ~06:10 -> C (44 km) legal and shorter
# than B; A still illegal.
C("sh07", "Which route should the planner assign to the 38-tonne load?",
"""
Route plan RP-3309 — Aldermoor Aggregates, Quarry to Selby Road depot
Vehicle: articulated HGV, gross weight loaded 38 tonnes, engine standard Euro V.
Departure: 05:30. Rule: use the shortest route the vehicle may legally take.

Route options
- Route A via Harlan Bridge: 41 km. Harlan Bridge weight limit: 32 tonnes gross vehicle weight.
- Route B via Eastway Ring Road: 58 km. No weight or emission restrictions.
- Route C via Selby town centre: 44 km. The route crosses the Selby Low Emission Zone at about 06:10.

Selby Low Emission Zone rules: HGVs below Euro VI are banned from the zone 24 hours a day. There is no charge-based option for HGVs.

Driver's note: "Harlan Bridge is fine — the limit is per axle and we're nowhere near 32 on any axle."
Fuel cost is roughly proportional to distance.
""",
[("route_a", "The bridge limit applies per axle, and no axle on the truck carries 32 tonnes, so the shortest route is legal."),
 ("route_b", "The bridge and the emission zone both rule out the shorter routes, so the ring road is the shortest legal route."),
 ("route_c", "The truck crosses the emission zone outside its hours of operation, so the town-centre route is the shortest legal one.")],
"route_b", 2,
twin=T([("HGVs below Euro VI are banned from the zone 24 hours a day.", "HGVs below Euro VI are banned from the zone between 07:00 and 19:00.")], "route_c")),

# ------------------------------------------------------------------ sh08
# why: goods over $5,000 must be insured to full value. Laptops $7,400. Carrier
# liability $1,000 only. Annual cargo policy excludes electronics. Declared value
# cover (1% = $74) is the only way to full value.
C("sh08", "How should the laptop shipment be insured?",
"""
Shipment SH-7002 — Brightwater Academy Trust, 20 refurbished laptops to Carrick Primary
Declared value: $7,400.

Logistics Insurance Rule (finance manual 12.3)
Any shipment of goods worth more than $5,000 must be insured to its full value. Use existing cover where it applies before buying additional cover.

Available cover
- Carrier standard liability (Parcelrun): included in the rate, limited to $1,000 per shipment.
- Carrier declared-value cover: 1% of the declared value, covers up to the declared value.
- Annual cargo policy (Harwood Marine): covers up to $10,000 per shipment at no extra cost. Exclusions: electronics, jewellery and cash.

IT technician's note: "The annual policy covers up to $10k, so we're fine without paying extra."
The laptops were wiped and re-imaged before packing.
""",
[("carrier_standard", "The carrier's included liability is insurance already, so no more cover is needed."),
 ("declared_value_cover", "The annual policy excludes electronics, so the carrier's declared-value cover is the way to insure the full $7,400."),
 ("annual_cargo_policy", "The annual policy covers up to $10,000 per shipment, which is more than the laptops are worth, so no extra premium is needed.")],
"declared_value_cover", 1),

# ------------------------------------------------------------------ sh09
# why: total cost = freight + downtime ($400/day x days to arrival). Air 3,200 + 2*400
# = 4,000; Road 1,400 + 6*400 = 3,800; Sea 600 + 20*400 = 8,600 -> road.
# Twin: $600/day -> Air 3,200+1,200 = 4,400; Road 1,400+3,600 = 5,000; Sea 600+12,000
# = 12,600 -> air.
C("sh09", "How should the replacement gearbox be shipped?",
"""
Breakdown report BR-114 — Line 3 extruder, Tolland Plastics
The Line 3 gearbox has failed. The line stays down until the replacement arrives and is fitted (fitting takes the same time whatever the mode).
Downtime cost (agreed by the plant controller): $400 per day of waiting.

Expedite Rule (Operations Manual 7.2): for breakdown spares, choose the shipping mode with the lowest total cost, where total cost = freight cost + downtime cost for the days until arrival.

Supplier quotes (Hessel Drives, gearbox price the same for all modes)
| Mode | Freight | Days to arrival |
| Air | $3,200 | 2 |
| Road | $1,400 | 6 |
| Sea | $600 | 20 |

Purchasing note: "For spares under $5,000 we usually just take the cheapest freight."
Maintenance note: a spare gearbox for Line 4 is not compatible with Line 3.
""",
[("air", "Adding downtime at the stated daily rate, air freight has the lowest total cost."),
 ("road", "Adding downtime at the stated daily rate, road has the lowest total cost."),
 ("sea", "Sea has the lowest freight cost, and spares under $5,000 go by the cheapest freight.")],
"road", 2,
twin=T([("Downtime cost (agreed by the plant controller): $400 per day of waiting.", "Downtime cost (agreed by the plant controller): $600 per day of waiting.")], "air")),

# ------------------------------------------------------------------ sh10
# why: while Faring share < 80%, route to Faring unless Faring has no service meeting
# the delivery requirement. Requirement: next day by 09:00; Faring best is 10:30 ->
# exception -> Swiftline Premium 09:00.
C("sh10", "Which carrier service should the parcel be booked on?",
"""
Parcel routing rules (Maple & Rowe Office Supplies)
R1. Our contract with Faring Parcel requires Faring to carry at least 80% of our parcels each quarter. Faring's share this quarter is currently 76%.
R2. While the share is below 80%, every parcel goes to Faring, unless Faring offers no service that meets the customer's delivery requirement.
R3. When R2's exception applies, use the cheapest other service that meets the requirement.

Parcel P-55870: printer toner and paper for Linford Dental Practice.
Customer requirement (service agreement): delivery next business day by 09:00.

Services
| Carrier | Service | Delivery | Price |
| Faring Parcel | Next Day | by 10:30 | $11 |
| Faring Parcel | Two Day | by 17:00 on day 2 | $7 |
| Swiftline | Premium 0900 | next day by 09:00 | $19 |

Account manager at Faring: "Please route everything to us this quarter; 10:30 is close enough for most customers."
""",
[("faring_next_day", "The contract share is below 80%, so the parcel must go to Faring, and Next Day is Faring's fastest service."),
 ("faring_two_day", "Faring must be used while under 80%, and Two Day is its cheapest service."),
 ("swiftline_premium", "No Faring service meets the 09:00 requirement, so the exception applies and Swiftline Premium is used.")],
"swiftline_premium", 2),

# ------------------------------------------------------------------ sh11
# why: DDP only to countries where the company holds a tax registration (Ostmark
# only). Customer in Vellan -> no DDP -> policy fallback DAP. EXW only for collection by
# the customer's own carrier (not the case). FCA only for sea shipments (this is road).
# Twin: customer in Ostmark -> requested DDP allowed.
C("sh11", "Which delivery term should sales quote to the customer?",
"""
Export Terms Policy (Brandvold Machine Tools), for sales staff
E1. Quote the delivery term the customer requests if the policy allows it.
E2. DDP (delivered duty paid) may be quoted only to countries where the company holds a tax registration. Current registrations: Ostmark.
E3. If DDP is requested but not allowed, quote DAP (delivered at place) instead.
E4. EXW is used only when the customer collects with its own carrier. FCA is used only for sea shipments via our port agent.

Enquiry Q-26-917
Customer: Halloran Precision, Tessel industrial estate, Vellan.
Requested term: DDP. Goods: 2 CNC lathes, delivered by road on our contracted trucks.

Sales manager's note: "EXW keeps all the risk off us, so let's push for EXW."
""",
[("quote_exw", "EXW limits our risk the most, and the policy prefers the lowest-risk term."),
 ("quote_fca", "FCA is the standard term for machinery exports, whatever the transport mode."),
 ("quote_dap", "Without a tax registration in the customer's country, DDP is barred and the policy substitutes DAP."),
 ("quote_ddp", "The customer's country is one where the company holds a tax registration, so the requested DDP can be quoted.")],
"quote_dap", 2,
twin=T([("Customer: Halloran Precision, Tessel industrial estate, Vellan.", "Customer: Halloran Precision, Tessel industrial estate, Ostmark.")], "quote_ddp")),

# ------------------------------------------------------------------ sh12
# why: imported wine held under duty suspension must stay in a bonded warehouse
# (finance rule: duty stays suspended until sale); storage 10-18 C. Kelso not bonded;
# Tollard bonded but no temperature control; Marram bonded + 12-16 C -> Marram.
C("sh12", "Which warehouse should receive the imported wine?",
"""
Inbound plan — Corvane Wine Merchants, container of Ostmark red wine (22 pallets)

Finance rule F-6: duty on imported wine must stay suspended until the wine is sold. Duty-suspended goods may only be stored in a bonded warehouse.
Quality rule Q-2: wine must be stored between 10 C and 18 C.
Choose the cheapest warehouse meeting F-6 and Q-2.

Quotes (per pallet per week)
| Warehouse | Bonded | Temperature control | Price |
| Kelso 3PL | no | 12-16 C | $3.20 |
| Marram Bonded Stores | yes | 12-16 C | $4.10 |
| Tollard Bonded | yes | none (ambient, 4-28 C through the year) | $3.80 |

Kelso's email: "Just pay the duty on arrival and store with us; it'll still work out cheaper."
The container arrives at Port Venn on 9 November.
""",
[("kelso_3pl", "Paying duty on arrival removes the need for bonded storage, which makes Kelso cheapest."),
 ("marram_bonded", "Marram is the only bonded warehouse that keeps the wine between 10 C and 18 C."),
 ("tollard_bonded", "Tollard is the cheapest bonded warehouse, and ambient storage is acceptable for red wine.")],
"marram_bonded", 1),

# ------------------------------------------------------------------ sh13
# why: items over 30 kg need two-person delivery; sofa 42 kg; customer ordered home
# delivery to room of choice -> two-person. Sack truck is not a second person.
C("sh13", "Which delivery option should be booked for the sofa order?",
"""
Order SO-44120 — Linden Home, two-seat sofa, 42 kg boxed
Customer choice at checkout: home delivery, room of choice.

Delivery rules (Linden Home Warehouse Handbook)
D1. Any single item over 30 kg must be delivered by a two-person crew (manual handling rule).
D2. Deliver the service the customer ordered; click-and-collect is only offered at checkout.
D3. Choose the cheapest option meeting D1 and D2.

Options
- Single-driver courier (Parcelrun Large): $45.
- Two-person delivery (Homeway Crew): $95.
- Click-and-collect from the Tanfield store: $0.

Planner's note: "Parcelrun drivers carry a sack truck — that's as good as a second person."
""",
[("single_driver", "A sack truck does the work of a second person, so the single-driver courier is compliant and cheaper."),
 ("two_person_crew", "At 42 kg the sofa needs a two-person crew, and the customer ordered home delivery."),
 ("click_and_collect", "Click-and-collect is free, so it is the cheapest option for the business.")],
"two_person_crew", 1),

# ------------------------------------------------------------------ sh14
# why: control entry TC-6A: thermal cameras with resolution >= 640x480 OR frame rate
# above 9 Hz are controlled. Camera 640x480, 30 Hz -> controlled. Destination Drovia is
# List B -> hold until licence (do not cancel). No research exemption.
# Twin: 320x240 and 9 Hz -> neither threshold met -> not controlled -> cheapest service
# meeting date (standard, 6 days <= 20 days).
C("sh14", "What should the dispatch team do with the thermal camera order?",
"""
Export compliance check — order EX-3318, Quillon Optics
Item: HX-7 thermal imaging camera, resolution 640 x 480, frame rate 30 Hz.
Customer: Institute of Geophysics, University of Karsk, Drovia.
Customer needs the camera within 20 days.

Export Control Procedure
EC-1. Control entry TC-6A: thermal cameras are controlled if their resolution is 640 x 480 or more, or their frame rate is above 9 Hz.
EC-2. Controlled items for List B destinations (Drovia is on List B) must be held until an export licence is granted. Licences for List B are usually decided within 30 days. Orders are not cancelled while a licence is pending.
EC-3. Items that are not controlled ship by the cheapest service that meets the customer's date.

Shipping services: Express 2 days ($140); Standard 6 days ($55).

Sales note: "It's a university — research use is always exempt, isn't it?" (The procedure has no research exemption.)
""",
[("ship_express", "Research use by a university is exempt, so the camera can go by the fastest service."),
 ("ship_standard", "The camera falls below both control thresholds, so no licence is needed and the cheapest service that meets the date applies."),
 ("hold_for_licence", "The camera is controlled and Drovia is on List B, so the order is held until a licence is granted."),
 ("cancel_order", "Controlled items can never go to List B destinations, so the order must be cancelled.")],
"hold_for_licence", 2,
twin=T([("resolution 640 x 480, frame rate 30 Hz.", "resolution 320 x 240, frame rate 9 Hz.")], "ship_standard")),

# ------------------------------------------------------------------ sh15
# why: 14 boxes x 22 kg = 308 kg. Parcels: 14 x $18 = $252. Pallet LTL $210 + tail-lift
# $55 (no dock/forklift at destination) = $265. Dedicated van only needed over 500 kg.
# Cheapest = parcels. Twin: destination has loading dock -> pallet $210 cheapest.
C("sh15", "How should the 14 boxes for the Ferndale branch be sent?",
"""
Shipping request — Corbel Office Supplies, branch replenishment to Ferndale
Consignment: 14 boxes, 22 kg each, 40 x 40 x 60 cm.
Destination: Ferndale branch, high-street shop with no loading dock and no forklift.

Carrier options
- Parcel service (Parcelrun): $18 per box; per-box limit 30 kg.
- Pallet LTL (Brannock Haulage): $210 per pallet (all 14 boxes fit on one pallet). Where the destination has no loading dock, a tail-lift surcharge of $55 applies.
- Dedicated van (Carrow Couriers): $300.

Shipping rule: choose the cheapest option the carriers will accept. A dedicated van is required only for consignments over 500 kg.

Branch manager: "Can we avoid 14 separate deliveries? It's a pain signing for them." (Parcelrun delivers all 14 boxes together in one drop.)
""",
[("parcel_service", "With the tail-lift surcharge added, 14 parcels cost less than the pallet."),
 ("pallet_ltl", "With a loading dock at the branch no tail-lift is needed, so one pallet is cheaper than 14 parcels."),
 ("dedicated_van", "At over 300 kg the consignment needs a dedicated van.")],
"parcel_service", 2,
twin=T([("Destination: Ferndale branch, high-street shop with no loading dock and no forklift.", "Destination: Ferndale branch, retail unit with its own loading dock and forklift.")], "pallet_ltl")),

# ------------------------------------------------------------------ sh16
# why: total = ocean + port congestion surcharge + inland haulage. Ardent 2,400+300+900
# = 3,600; Belling 2,250+650+800 = 3,700; Corran 2,600+0+1,150 = 3,750. All approved
# for dry goods. Lowest = Ardent. Twin: Ardent surcharge 500 -> 3,800 -> Belling 3,700.
C("sh16", "Which port of entry should the container be routed through?",
"""
Routing decision — Tessaly Kitchenware, container TKU-44102 (dry goods, no food)
Routing Rule RR-5: choose the port with the lowest total cost to the Hollin distribution centre, where total = ocean freight + port congestion surcharge + inland haulage to Hollin. All three ports below are approved for this cargo.

| Port | Ocean freight | Congestion surcharge | Inland haulage to Hollin |
| Port Ardent | $2,400 | $300 | $900 |
| Port Belling | $2,250 | $650 | $800 |
| Port Corran | $2,600 | none | $1,150 |

Planner's comment: "Corran is the only port with no surcharge at the moment, so it should be the safe choice."
Transit times differ by less than a day and are not part of RR-5.
""",
[("port_ardent", "Ardent has the lowest total of ocean freight, surcharge and inland haulage."),
 ("port_belling", "Belling has the lowest total once the congestion surcharge and inland haulage are added."),
 ("port_corran", "Corran charges no congestion surcharge, which makes it the lowest-cost port.")],
"port_ardent", 1,
twin=T([("| Port Ardent | $2,400 | $300 | $900 |", "| Port Ardent | $2,400 | $500 | $900 |")], "port_belling")),

# ------------------------------------------------------------------ sh17
# why: termination notice -> clause 17.2 recorded delivery or signed courier; Amendment
# 2 email route excludes termination notices. First-class post not a valid method.
# Cheapest valid = recorded delivery ($3.20).
C("sh17", "How should the termination notice be sent to the supplier?",
"""
Legal team task LT-219 — Serve notice on Varga Office Cleaning under the services agreement dated 4 January 2024.
Notice type: termination notice (termination for convenience, 90 days).

Services agreement, clause 17 (Notices)
17.2 Any notice under this agreement must be in writing and sent by recorded delivery, or by courier with signature on receipt, to the other party's registered office.
Amendment 2 (signed 3 March 2026): notices other than termination notices may also be sent by email to legal@varga-cleaning.example.

Internal rule: use the cheapest method that is valid under the agreement.
Costs: email $0; first-class post $1.20; recorded delivery $3.20; signed courier $24.00.

Paralegal's note: "Amendment 2 lets us use email now, so that's quickest and free."
""",
[("email", "Amendment 2 allows notices to be sent by email to Varga's legal address, which is free and reaches them fastest."),
 ("first_class_post", "Proof of posting from first-class post counts as recorded delivery under clause 17.2."),
 ("recorded_delivery", "Termination notices still need recorded delivery or signed courier, and recorded delivery is the cheaper of the two."),
 ("signed_courier", "A signed courier gives the strongest proof of receipt, so it should be used for any notice.")],
"recorded_delivery", 2),

# ------------------------------------------------------------------ sh18
# why: crates 2.40 m tall; standard container door height 2.28 m (20ft and 40ft);
# high-cube door 2.58 m. LCL max height 2.20 m. Only 40ft HC fits (volume 76 m3 >= 48,
# payload fine) -> 40ft HC.
# Twin: crates 2.10 m -> all fit; costs: 40ft $2,900 < LCL 48*68 = $3,264 < 40HC $3,050?
# (3,050 < 3,264) -> 40ft cheapest ($2,900; 67 m3, 26 t payload >= 14 t) -> one_40ft.
C("sh18", "Which container option should be booked for the machinery crates?",
"""
Export booking — Ferrand Presses, 6 crates of press components
Total volume: 48 cubic metres. Total weight: 14 tonnes. Tallest crate: 2.40 m (crates cannot be tilted).

Container data (Selwood Line)
| Option | Internal volume | Max payload | Door height | Price |
| Two 20ft standard | 2 x 33 m3 | 2 x 21 t | 2.28 m | $1,800 each |
| One 40ft standard | 67 m3 | 26 t | 2.28 m | $2,900 |
| One 40ft high-cube | 76 m3 | 26 t | 2.58 m | $3,050 |
| LCL (shared container) | charged per m3 | - | max cargo height 2.20 m | $68 per m3 |

Booking rule: choose the cheapest option that physically fits the cargo within volume, payload and door height limits.
Shipping clerk's note: "The 40ft standard has more than enough room and weight capacity; it's the obvious pick."
""",
[("two_20ft", "Splitting the crates across two 20ft containers spreads the weight and stays under each payload limit."),
 ("one_40ft", "The crates clear standard door height, and a single 40ft is the cheapest option with enough volume and payload."),
 ("one_40ft_hc", "The crates are too tall for standard doors and for LCL, so the high-cube is the only option that fits."),
 ("lcl", "LCL charges only for the space used, which makes it cheapest for 48 cubic metres.")],
"one_40ft_hc", 2,
twin=T([("Tallest crate: 2.40 m (crates cannot be tilted).", "Tallest crate: 2.10 m (crates cannot be tilted).")], "one_40ft")),

# ------------------------------------------------------------------ sh19
# why: facilitation payments to officials are prohibited, including via agents.
# Meridian's $150 to the port inspector for same-day release is a facilitation
# payment -> excluded. Paxford transit 19 days > 14 required -> excluded. Olwen
# ($2,980, official fees only) -> lowest compliant.
C("sh19", "Which freight forwarder should be appointed for the Qarran shipment?",
"""
Forwarder selection — Hessel Pumps, 3 crates to the Qarran Water Authority
Required delivery: within 14 days of collection.

Anti-Bribery Policy AB-2
AB-2.1 Facilitation payments (small unofficial payments to public officials to speed up routine actions) are prohibited, including when paid by agents or forwarders on our behalf.
AB-2.2 Official fees published in a government tariff are not facilitation payments.
Selection rule: choose the lowest total quote that complies with AB-2 and the delivery requirement.

Quotes
- Meridian Freight: $2,850 total, 12 days. Includes "$150 customs facilitation fee, paid to the port inspector for same-day release".
- Olwen Logistics: $2,980 total, 13 days. Includes official clearance fees per the Qarran customs tariff.
- Paxford Cargo: $2,700 total, 19 days.

Meridian's note: "Everyone pays this fee at Qarran; it's just how the port works."
""",
[("meridian_freight", "The $150 is small and paid by the forwarder rather than by us, so it falls outside the policy."),
 ("olwen_logistics", "Olwen is the cheapest quote that meets the 14-day requirement without any facilitation payment."),
 ("paxford_cargo", "Paxford is cheapest, and the 14-day delivery requirement is only a guide.")],
"olwen_logistics", 1),

# ------------------------------------------------------------------ sh20
# why: returned drill, opened, 2 years old; repair $50 vs replacement $110 = 45.5%.
# Threshold 40% (amended from 50% for assessments from 1 Jul 2026; assessed 15 Sep) ->
# no repair. Refurbish only unopened returns. Manufacturer warranty 1 year -> expired.
# Otherwise recycle.
C("sh20", "What disposition should the returns centre apply to this unit?",
"""
Returns Centre Procedure RC-8 (Fennick Tools)
RC-8.1 Repair the unit if the repair cost is less than 50% of the replacement cost and the unit is under 3 years old.
RC-8.2 Refurbish for resale only if the unit was returned unopened.
RC-8.3 Return to the manufacturer only if the unit is still within the manufacturer's 1-year warranty.
RC-8.4 Otherwise recycle.
Amendment RC-8/2 (for assessments made on or after 1 July 2026): in RC-8.1, "50%" is replaced by "40%".

Assessment AS-90117, made 15 September 2026
Item: 18V cordless drill, customer return, box opened, used.
Age: 2 years (purchased September 2024).
Fault: worn gearbox. Repair quote: $50. Replacement cost: $110.

Technician's note: "Repair is under half the replacement cost, so repair as usual."
""",
[("repair", "The repair costs less than half the replacement price and the unit is under 3 years old, so it qualifies for repair under RC-8.1."),
 ("refurbish_for_resale", "Customer returns made within the retail return period can always be refurbished for resale."),
 ("return_to_manufacturer", "A gearbox fault is a manufacturing defect, so it goes back to the manufacturer."),
 ("recycle", "At about 45% of replacement cost the repair exceeds the amended 40% limit, and no other route applies.")],
"recycle", 2),

# ------------------------------------------------------------------ sh21
# why: daily load 130 kg in one trip <= bike limit 150 kg; heaviest parcel 18 kg
# (bike limit per parcel 25 kg). Costs: bike $180; diesel van 170 + 20 + 15 = $205;
# e-van 170 + 60 = $230 (no congestion charge). Cheapest = bike.
C("sh21", "Which vehicle should run the city-centre delivery round?",
"""
Round planning — Pellow Deli Supplies, City Round 2
Daily load: 130 kg in one trip, 26 drops. Heaviest single parcel: 18 kg.

Round rules
- Cargo bike: maximum 150 kg per trip and 25 kg per parcel.
- Vans pay the city congestion charge of $15 per day, except zero-emission vans, which are exempt.
- Choose the vehicle with the lowest daily cost that can carry the round.

Daily costs
- Cargo bike: rider $180 (no fuel or charge).
- Diesel van: driver $170 + fuel $20 + congestion charge.
- Electric van: driver $170 + lease top-up $60 (exempt from the congestion charge).

Driver's comment: "Anything over 15 kg really needs a van."
""",
[("cargo_bike", "The load and heaviest parcel are within the bike's limits, and at $180 a day it is the cheapest option."),
 ("diesel_van", "Parcels heavier than 15 kg need a van, and the diesel van is the cheaper van."),
 ("electric_van", "The electric van avoids the congestion charge, which makes it the cheapest vehicle for the round once all daily costs are added.")],
"cargo_bike", 1),
]
