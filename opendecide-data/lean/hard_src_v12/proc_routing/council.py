"""proc_routing / municipal service-request routing (Harrowfield Borough Council, invented)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ co01
# why: carriageway defect 45 mm deep and 350 mm wide -> both Category 1 tests met
#      -> Highways Emergency. Cover is 2 m away (> 150 mm) -> not utility.
#      twin 35 mm -> Category 2 routine list.
C("rt_co01", "How should the contact centre route this report?",
"""
Harrowfield Borough Council — Highways Inspection Manual (extract)
4.2 Carriageway defects that are 40 mm deep or more AND wider than 300 mm are Category 1: made safe within 24 hours by the Highways Emergency crew.
4.3 Footway defects are Category 1 at 20 mm deep or more.
4.4 All other defects are Category 2 and are added to the routine inspection list.
4.5 Defects in or within 150 mm of a utility cover are passed to the utility company that owns the cover.
4.6 Reports about private roads are answered with the private-roads letter.

Report HW-88213 — online form, Monday 08:40
Location: Carver Street, eastbound carriageway outside no. 42 (adopted highway)
Reporter's measurements with photo and tape: 45 mm deep, 350 mm wide
Reporter note: "Two cyclists have swerved round it this morning. There's a water company cover about 2 metres further along."
Previous report at this location: Category 2 pothole repaired in January.
""",
[("dispatch_highways_emergency", "At 45 mm deep and 350 mm wide on the carriageway it meets both Category 1 tests, so the Highways Emergency crew makes it safe within 24 hours."),
 ("add_to_routine_inspection", "The carriageway defect is shallower than 40 mm, so it is Category 2 for the routine list."),
 ("refer_to_utility_company", "A water company cover sits about 2 metres along from the pothole, so under 4.5 the defect is passed to the utility company that owns the cover rather than repaired by the council."),
 ("send_private_roads_letter", "The earlier repair shows the council has already dealt with this stretch, so the reporter gets the standard letter.")],
"dispatch_highways_emergency", 1,
twin=T([("45 mm deep, 350 mm wide", "35 mm deep, 350 mm wide")], "add_to_routine_inspection")),

# ------------------------------------------------------------------ co02
# why: damp inside the flat of a private tenant -> Private Sector Housing even
#      though the council owns the freehold (only communal areas are Housing Repairs).
C("rt_co02", "Which service should take this housing complaint?",
"""
Harrowfield Borough Council — Housing Contact Routing (extract)
H1. Council tenants: all repairs, inside the home and in communal areas, go to Housing Repairs.
H2. Leaseholders of council blocks: communal-area repairs go to Housing Repairs; repairs inside the flat are the leaseholder's own responsibility.
H3. Private tenants (renting from a private landlord, including a leaseholder who lets out a flat in a council block): disrepair inside the home goes to the Private Sector Housing team, which can inspect and require the landlord to act. This applies whoever owns the freehold.
H4. Anti-social behaviour on council estates goes to the Estates team.

Contact HS-40231 — phone, Wednesday 11:15
Caller: Precious Nwosu, Flat 9, Linden House (council-owned block)
"I rent this flat from Mr D. Castle, who bought it from the council years ago. There's black mould spreading across the bedroom wall and the window frame is rotten. He hasn't answered my texts for a month."
Housing record: Flat 9 is leasehold (leaseholder: D. Castle). Council freehold.
""",
[("route_private_sector_housing", "She rents from a private leaseholder, so disrepair inside her flat goes to Private Sector Housing under H3, whoever owns the freehold."),
 ("route_housing_repairs", "Linden House is a council-owned block and the council holds the freehold, so repairs to any flat in it are routed to Housing Repairs under H1 and H2."),
 ("advise_leaseholder_responsible", "Repairs inside a leasehold flat are the leaseholder's own job, so the caller is told to chase Mr Castle."),
 ("route_estates_team", "An unresponsive landlord on a council estate is an estates matter.")],
"route_private_sector_housing", 2),

# ------------------------------------------------------------------ co03
# why: out-of-hours noise service runs Fri/Sat nights only; Wednesday 23:30 ->
#      logged for the EH day team. twin Saturday 23:30 -> OOH noise team.
C("rt_co03", "Where should this noise complaint go?",
"""
Harrowfield Borough Council — Environmental Health, Noise Service
N1. The out-of-hours noise team operates on Friday and Saturday nights, 22:00 to 03:00. It can visit and witness noise during a complaint.
N2. At all other times, noise complaints are logged for the Environmental Health day team, which sends diary sheets and may install recording equipment.
N3. Where the caller reports violence, threats or a fight, they are told to call the police; the council does not attend.
N4. Noise from licensed premises is also copied to the Licensing team.

Complaint EH-73019 — phone, Wednesday 23:30
Caller: Martin Oyelowo, 14 Pelham Road
"The house next door has had music on at full volume since ten. It's a party, maybe thirty people in the garden. Nobody is fighting, it's just really loud and I have work at six."
Premises: private house (not licensed).
""",
[("log_for_eh_day_team", "Wednesday is not an out-of-hours noise night, so the complaint is logged for the Environmental Health day team."),
 ("dispatch_ooh_noise_team", "The complaint comes in on a Friday or Saturday night between 22:00 and 03:00, so the out-of-hours noise team can attend."),
 ("refer_to_police", "A party of around thirty people in a garden late at night is a public-order matter, so the caller is told to call the police instead."),
 ("copy_to_licensing", "A party with thirty guests is an event that needs a licence.")],
"log_for_eh_day_team", 1,
twin=T([("Complaint EH-73019 — phone, Wednesday 23:30", "Complaint EH-73019 — phone, Saturday 23:30")], "dispatch_ooh_noise_team")),

# ------------------------------------------------------------------ co04
# why: request for internal emails (unpublished recorded information) -> FOI ->
#      Information Governance. Tone of the email does not make it a complaint.
C("rt_co04", "Which team should handle this request?",
"""
Harrowfield Borough Council — Information Requests Procedure
IR1. A Freedom of Information (FOI) request is a written request for recorded information that the council holds and has not already published. FOI requests go to Information Governance, which logs them against the 20-working-day limit.
IR2. Requests for documents that are already published (strategies, minutes, published reports) are business as usual: the service sends the link.
IR3. A complaint is an expression of dissatisfaction about a council service. Complaints go to the service's Stage 1 handler.
IR4. A request can be both; if so, both processes run.

Email to info@harrowfield.example — Tuesday
From: Oliver Jessop
"Please provide all emails between the Parking Services Manager and Kerbline Contracts Ltd between 1 January and 30 April about the pay-and-display machine tender. Your tender process stinks and I intend to show it."
""",
[("route_information_governance_foi", "He asks for unpublished internal emails, which is recorded information the council holds and has not published, so it is an FOI request for Information Governance under IR1."),
 ("route_parking_team_bau", "The tender relates to Parking Services, so the service answers it as business as usual."),
 ("route_complaints_stage1", "He says the tender process stinks, which is an expression of dissatisfaction with Parking Services, so under IR3 it goes to the service's Stage 1 complaints handler."),
 ("route_legal_services", "He threatens to expose the council, which Legal must handle.")],
"route_information_governance_foi", 2),

# ------------------------------------------------------------------ co05
# why: sent by a councillor on a resident's behalf -> Member Enquiries.
#      twin: sent by the resident with the councillor copied in -> service
#      directly -> Waste Services.
C("rt_co05", "How should this email be routed?",
"""
Harrowfield Borough Council — Correspondence Routing Note
M1. Member Enquiries: every enquiry sent by a councillor, including enquiries made on behalf of residents, is logged by the Member Enquiries team, which allocates it to the service with a 10-working-day deadline.
M2. Where a resident writes and copies a councillor in, the service handles the email directly and copies its reply to the councillor.
M3. Missed bin collections are handled by Waste Services.
M4. Complaints about a councillor's conduct go to the Monitoring Officer.

Email received Thursday 09:12
From: Cllr Rana Okoye (Ward: Eastmoor)
To: contact@harrowfield.example
Subject: Missed bins — Hawthorn Close
"My constituent Mr Paul Hendry at 6 Hawthorn Close tells me his recycling has been missed three weeks running. Please could this be looked into and the collection put right."
""",
[("route_member_enquiries", "The email was sent by a councillor on a resident's behalf, so M1 sends it to Member Enquiries."),
 ("route_waste_services", "The resident wrote himself and only copied the councillor in, so under M2 Waste Services handles the missed bins directly and copies its reply to the councillor."),
 ("route_monitoring_officer", "Emails from councillors are handled by the Monitoring Officer."),
 ("route_complaints_stage1", "Missing the same household's recycling three weeks running is a service failure, so it is logged as a complaint for the Stage 1 handler.")],
"route_member_enquiries", 1,
twin=T([("From: Cllr Rana Okoye (Ward: Eastmoor)\nTo: contact@harrowfield.example",
         "From: Mr Paul Hendry, 6 Hawthorn Close\nTo: contact@harrowfield.example\nCc: Cllr Rana Okoye (Ward: Eastmoor)"),
        ("\"My constituent Mr Paul Hendry at 6 Hawthorn Close tells me his recycling has been missed three weeks running.",
         "\"My recycling has been missed three weeks running.")],
       "route_waste_services")),

# ------------------------------------------------------------------ co06
# why: Stage 1 response issued 3 March; request on 10 March is within 20 working
#      days and no Stage 2 yet -> Stage 2 with the Complaints Team.
C("rt_co06", "Where should this complaint correspondence go?",
"""
Harrowfield Borough Council — Complaints Procedure (extract)
C1. Stage 1: the service area responds within 10 working days.
C2. Stage 2: a complainant unhappy with the Stage 1 response may ask the Complaints Team for a Stage 2 review within 20 working days of the Stage 1 response.
C3. After a Stage 2 response, the complainant is signposted to the Local Services Ombudsman; the council does not open a further stage.
C4. New issues raised during a complaint start their own Stage 1.

Complaint file CF-2210
Subject: delayed disabled facilities grant assessment
Stage 1: response issued 3 March by Adult Social Care (upheld in part; apology given)
Stage 2: not yet requested
Letter received 10 March from the complainant, Mrs Irene Bagshaw:
"Your 3 March reply accepts the delay but does not tell me when the assessment will happen. I am not satisfied and want this looked at again, please."
""",
[("escalate_stage2_complaints_team", "She is unhappy with the 3 March Stage 1 response and wrote on 10 March, well within 20 working days, and no Stage 2 has been held, so the Complaints Team opens Stage 2."),
 ("signpost_ombudsman", "Stage 2 is complete, so C3 signposts her to the Local Services Ombudsman."),
 ("return_to_service_stage1", "Asking when the assessment will actually happen is a new issue that the Stage 1 reply did not cover, so under C4 it starts its own fresh Stage 1."),
 ("route_adult_social_care", "Adult Social Care wrote the first reply, so it answers her letter too.")],
"escalate_stage2_complaints_team", 1),

# ------------------------------------------------------------------ co07
# why: wall leaning over a public footpath with widening cracks -> risk of
#      collapse onto a public space -> Building Control out-of-hours on-call.
#      twin: leaning into the caller's own garden away from paths/buildings ->
#      logged for next working day.
C("rt_co07", "What is the correct routing for this call?",
"""
Harrowfield Borough Council — Out-of-Hours Emergency Line, Building Control
B1. The Building Control on-call surveyor attends dangerous structures out of hours: a structure at risk of collapse onto a highway, footpath, public space or occupied building.
B2. Other structural concerns are logged for Building Control on the next working day.
B3. Fallen trees and debris blocking a road go to the Highways Emergency crew.
B4. Gas smells: the caller is given the gas network's emergency number.

Call log OOH-5521 — Sunday 21:30
Caller: Denise Okafor, 3 Mill Lane
"The old brick wall at the end of my neighbour's garden is leaning over the public footpath on Mill Lane. The cracks have got wider since this afternoon and bits of mortar are dropping onto the path. People walk their dogs along there all evening."
Weather: high winds forecast overnight.
""",
[("page_building_control_oncall", "The wall is at risk of falling onto a public footpath, so B1 calls out the Building Control on-call surveyor."),
 ("log_building_control_next_day", "The wall threatens no highway, footpath, public space or occupied building, so it is logged for the next working day."),
 ("route_highways_emergency", "Debris on a footpath is a highways matter under B3."),
 ("advise_neighbour_civil_matter", "The wall stands at the end of the neighbour's own garden, so it is the neighbour's property and a private civil matter rather than one for the council.")],
"page_building_control_oncall", 1,
twin=T([("is leaning over the public footpath on Mill Lane. The cracks have got wider since this afternoon and bits of mortar are dropping onto the path. People walk their dogs along there all evening.",
         "is leaning into my own back garden, well away from any path or building. The cracks have got wider since this afternoon and bits of mortar are dropping onto my lawn.")],
       "log_building_control_next_day")),

# ------------------------------------------------------------------ co08
# why: suspected asbestos (anywhere) -> Environmental Health Contaminated Land,
#      overriding the private-land landowner route.
#      twin: garden-waste bags on private land -> landowner advice.
C("rt_co08", "Which team should deal with this fly-tipping report?",
"""
Harrowfield Borough Council — Fly-tipping Routing
F1. Fly-tipping on public land (roads, verges, parks, council car parks): Waste Enforcement, which clears it and investigates.
F2. Fly-tipping on private land: the landowner is responsible; the council sends the landowner an advice letter.
F3. Suspected asbestos, on any land: Environmental Health (Contaminated Land) gives specialist removal advice. F3 applies before F1 and F2.
F4. Abandoned vehicles are covered by the Abandoned Vehicles procedure.

Report FT-66012 — online form, Friday 16:10
Location: field gateway on Brook Farm, Coldharbour Lane (private farmland; owner Mr G. Elwood)
Description: "About ten grey corrugated sheets, broken edges, that look like old asbestos garage roofing, dumped across the gateway overnight."
Photo attached. Reporter: passing cyclist.
""",
[("route_eh_contaminated_land", "The sheets are suspected asbestos, and F3 sends asbestos on any land to Environmental Health before the landowner rules."),
 ("send_landowner_advice", "The waste is on private farmland and is not suspected asbestos, so the landowner gets an advice letter under F2."),
 ("route_waste_enforcement", "The sheets were dumped across a gateway beside Coldharbour Lane, and anything dumped beside a lane is public-land fly-tipping for Waste Enforcement under F1."),
 ("route_abandoned_vehicles", "Garage roofing belongs with the Abandoned Vehicles procedure.")],
"route_eh_contaminated_land", 1,
twin=T([("About ten grey corrugated sheets, broken edges, that look like old asbestos garage roofing, dumped across the gateway overnight.",
         "About ten black bin bags of garden waste and hedge cuttings, dumped across the gateway overnight.")],
       "send_landowner_advice")),

# ------------------------------------------------------------------ co09
# why: tree blocking both lanes of a carriageway -> Highways Emergency 24/7,
#      regardless of who owns the tree.
C("rt_co09", "How should the out-of-hours line route this call?",
"""
Harrowfield Borough Council — Trees: Contact Routing
T1. Council-owned trees (streets, parks, council land): Arboriculture team, routine inspection.
T2. Any tree or large branch blocking a carriageway: Highways Emergency crew, 24 hours, whoever owns the tree.
T3. Private trees not blocking a carriageway: a civil matter; the caller is sent the private-trees advice leaflet.
T4. Trees on railway land: referred to the rail operator.

Call log OOH-5602 — Tuesday 02:05
Caller: taxi driver, name withheld
"A big tree has come down from the garden of one of the houses on Station Road and it's lying right across the road, both lanes blocked. Cars are turning round."
Location check: Station Road is an adopted highway; the tree stood in the front garden of no. 18 (privately owned).
""",
[("dispatch_highways_emergency", "The fallen tree is lying across both lanes of Station Road, a carriageway, so T2 sends the Highways Emergency crew at any hour, whoever owned the tree."),
 ("send_private_trees_leaflet", "The tree grew in the front garden of a privately owned house, so under T3 it is a civil matter and the owner is sent the private-trees advice leaflet."),
 ("route_arboriculture", "Trees along streets are handled by the Arboriculture team."),
 ("refer_to_rail_operator", "Station Road leads to the station, so the rail operator deals with it.")],
"dispatch_highways_emergency", 1),

# ------------------------------------------------------------------ co10
# why: unauthorised windows on a Grade II listed house -> Conservation &
#      Heritage (priority); the caller's family link to a councillor is not a
#      routing rule and he is not a councillor.
C("rt_co10", "Which team should receive this enforcement report?",
"""
Harrowfield Borough Council — Planning Enforcement Intake
P1. Suspected unauthorised building works or changes of use: Planning Enforcement.
P2. Works to a listed building, or in a conservation area: Conservation & Heritage team, handled as a priority case.
P3. Enquiries sent by a councillor go through Member Enquiries.
P4. Dangerous structures: Building Control.

Report PE-31905 — online form, Monday 10:20
From: Neil Carrow, 16 Abbey Row
"Number 14 Abbey Row has had all its original sash windows ripped out and replaced with white plastic ones this weekend. My cousin is Councillor Blake, so I expect this to be dealt with first."
Records check: 14 Abbey Row is a Grade II listed house. No listed building consent on file.
""",
[("route_conservation_heritage", "14 Abbey Row is Grade II listed, so P2 sends works to it to Conservation & Heritage as a priority case; the reporter's cousin being a councillor changes nothing."),
 ("route_planning_enforcement", "Replacing windows without permission is unauthorised building work for Planning Enforcement."),
 ("route_member_enquiries", "The reporter says his cousin is Councillor Blake, so the enquiry has a councillor connection and should be logged through Member Enquiries under P3."),
 ("route_building_control", "Removing original windows can weaken the frame, which is a Building Control matter.")],
"route_conservation_heritage", 1),

# ------------------------------------------------------------------ co11
# why: illness reported by two separate households linked to the same premises
#      -> outbreak route: Food Team leads and Health Protection liaison notified.
C("rt_co11", "How should this food complaint be routed?",
"""
Harrowfield Borough Council — Environmental Health, Food Complaints
FC1. Complaints about food premises or food bought from them go to the EH Food Team.
FC2. Outbreak route: where illness is reported by two or more separate households linked to the same premises, the Food Team leads and the Health Protection liaison officer must be notified the same day.
FC3. Complaints about labelling, weights or prices go to Trading Standards.
FC4. Complaints about staff rudeness are passed to the business.

Complaint EH-74410 — phone, Monday 09:30
Caller: Mrs Funmi Adeyemi, 3 Ferry Lane
"We had a takeaway from the Golden Lantern on Saturday night and my husband and I were both sick all Sunday. My neighbours the Carrs at 18 Holt Street, a separate household, ate from the same takeaway and they were ill too. Also the menu said king prawns but they were tiny."
""",
[("route_food_team_outbreak", "Two separate households linked to the same takeaway reported illness, so FC2's outbreak route applies with the Health Protection liaison notified."),
 ("route_food_team", "Only one household reported illness, so it is an ordinary food complaint for the Food Team."),
 ("route_trading_standards", "The caller also says the menu promised king prawns but the prawns were tiny, which is a description and labelling matter that FC3 sends to Trading Standards."),
 ("pass_to_business", "Complaints about a takeaway's food are passed to the business to resolve.")],
"route_food_team_outbreak", 2,
twin=T([("My neighbours the Carrs at 18 Holt Street, a separate household, ate from the same takeaway and they were ill too.",
         "Nobody else who lives with us, and no one else we know, ate from it.")], "route_food_team")),

# ------------------------------------------------------------------ co12
# why: private owner-occupier, rats in own garden -> paid Pest Control booking.
C("rt_co12", "Which route applies to this pest report?",
"""
Harrowfield Borough Council — Pest Control Routing
PC1. Council tenants: pest treatment is arranged through Housing Repairs at no charge.
PC2. Private residents (owner-occupiers and private tenants): the paid Pest Control service is booked, with concessions for residents on qualifying benefits.
PC3. Pests on public land such as parks: the Parks team.
PC4. Pests at food businesses: Environmental Health Food Team.

Contact PS-2071 — web chat, Thursday 14:00
Resident: Alan Whitcombe, 27 Rosemount Avenue
"We've seen rats by the compost bin in our back garden three evenings running. We own the house. Can someone come out?"
Council records: 27 Rosemount Avenue is privately owned; no council tenancy.
Note from caller: "Linden Park is at the end of our road, if that matters."
""",
[("book_paid_pest_control", "He is a private owner-occupier with rats in his own garden rather than on public land, so PC2 books the paid Pest Control service, with a concession only if he is on qualifying benefits."),
 ("route_housing_repairs", "He is a council tenant, so the treatment goes through Housing Repairs free of charge."),
 ("route_parks_team", "The caller mentions that Linden Park is at the end of the road, and rats near a park are treated as pests on public land for the Parks team under PC3."),
 ("route_food_team", "Rats near a compost bin are a food hygiene matter.")],
"book_paid_pest_control", 1),

# ------------------------------------------------------------------ co13
# why: badge appears to be a colour photocopy, hologram missing -> suspected
#      copied badge -> Counter Fraud. twin: genuine badge used with holder absent
#      -> misuse -> Parking Enforcement.
C("rt_co13", "Where should this Blue Badge report be sent?",
"""
Harrowfield Borough Council — Blue Badge Enforcement Routing
BB1. Misuse of a genuine badge (for example used when the badge holder is not travelling in the vehicle): Civil Parking Enforcement.
BB2. Suspected forged, altered or copied badges: Counter Fraud Team.
BB3. Questions about eligibility or renewals: Blue Badge administration.
BB4. Dangerous or obstructive parking without any badge issue: Civil Parking Enforcement.
BB5. Reports should include the location, time and, where safe, a photo; officers do not approach drivers.

Report BB-1188 — online form, Wednesday
Location: disabled bay, Market Square car park
"The badge in the silver hatchback looked like a colour photocopy — flat paper, no hologram, and the expiry date looked written over. The driver, a young man, walked off alone into the shops."
Photo attached (badge front, partial).
""",
[("route_counter_fraud", "Flat paper, no hologram and a written-over expiry date point to a copied or altered badge, which BB2 sends to the Counter Fraud Team rather than Parking Enforcement."),
 ("route_parking_enforcement", "The badge looked genuine but was used without the holder present, which is misuse for Civil Parking Enforcement."),
 ("route_blue_badge_admin", "The expiry date on the badge appears to have been written over, which is a renewal question, so Blue Badge administration checks whether it is still valid.")],
"route_counter_fraud", 1,
twin=T([("\"The badge in the silver hatchback looked like a colour photocopy — flat paper, no hologram, and the expiry date looked written over.",
         "\"The badge in the silver hatchback looked genuine, with the hologram, but the photo on it is of an elderly woman.")],
       "route_parking_enforcement")),

# ------------------------------------------------------------------ co14
# why: on a public road with plates missing AND windows broken (two signs) ->
#      abandoned -> council Abandoned Vehicles team.
#      twin: plates present, intact, tax lapsed 5 weeks (< 3 months, one sign
#      does not reach two) -> untaxed only -> report to NVLA.
C("rt_co14", "How should this vehicle report be routed?",
"""
Harrowfield Borough Council — Abandoned Vehicles Procedure
AV1. A vehicle on a public road showing two or more of these signs is treated as abandoned and goes to the council's Abandoned Vehicles team: no number plates; broken windows; flat tyres; burnt out; untaxed for three months or more.
AV2. A vehicle on a public road that is untaxed but not abandoned under AV1 is reported to the National Vehicle Licensing Agency (NVLA) online; the council takes no action.
AV3. Vehicles on private land are the landowner's responsibility; the landowner is sent advice.

Report AV-2290 — online form, Tuesday
Location: Hobb Lane, near the entrance to the allotments (adopted highway)
Vehicle: blue estate car. Number plates missing; two side windows broken; tyres inflated.
Reporter note: "It's been there about three weeks."
""",
[("route_abandoned_vehicles_team", "On a public road with missing plates and broken windows, two AV1 signs, the car is treated as abandoned."),
 ("refer_to_nvla", "The car shows fewer than two AV1 signs and is simply untaxed, so it is reported to the NVLA under AV2."),
 ("advise_landowner", "The car is parked near the entrance to the allotments, and allotments are private land, so the landowner is sent advice under AV3."),
 ("route_waste_enforcement", "A car left for three weeks is fly-tipping.")],
"route_abandoned_vehicles_team", 1,
twin=T([("Number plates missing; two side windows broken; tyres inflated.",
         "Number plates present; windows and tyres intact; road tax expired five weeks ago.")],
       "refer_to_nvla")),
]
