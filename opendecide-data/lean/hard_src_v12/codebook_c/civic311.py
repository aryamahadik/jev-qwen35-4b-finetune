"""codebook_c / city 311 service requests (Port Calloway 311, invented city)."""
from _lib import C, Y, T

PC = {
    "Road surface repair": "Potholes, sinkholes, and cracked or sunken pavement in a public street or alley.",
    "Sidewalk and curb repair": "Broken, lifted or missing sidewalk slabs, curbs and curb ramps; a sidewalk lifted by a street-tree root is still coded here.",
    "Street lighting": "Streetlights that are out, flickering, cycling, or lit during daylight, and damaged light poles.",
    "Traffic signal fault": "Traffic lights, pedestrian signals and crossing push-buttons that are dark, stuck, unresponsive or mistimed.",
    "Signs and pavement markings": "Missing, damaged, turned or faded street signs, stop and yield signs, lane lines and crosswalk paint.",
    "Collection not completed": "A scheduled household trash, recycling or yard-waste pickup that did not happen on the collection day.",
    "Bulk item pickup": "Scheduling removal of furniture, appliances or mattresses that a resident is putting out from their own home.",
    "Illegal dumping": "Waste left by an unknown or other party on public property: streets, alleys, parks and city-owned lots.",
    "Graffiti removal": "Paint or marker tagging on public property, or on private property visible from the street when the owner has signed the city's removal consent form.",
    "Abandoned vehicle": "A vehicle on a public street that has not moved for more than 72 hours, or that is visibly inoperable (flat or missing tyres, broken windows).",
    "Parking enforcement": "A vehicle currently parked illegally: blocking a driveway, hydrant, crosswalk or bike lane.",
    "Noise complaint": "Ongoing noise from people, parties, businesses, alarms or amplified music; construction noise outside permitted hours is coded Construction and permits.",
    "Construction and permits": "Building work without a posted permit, construction activity outside permitted hours (7 a.m. to 7 p.m. weekdays, 9 a.m. to 5 p.m. weekends), and unsafe construction sites.",
    "Street tree": "Trees in the public right of way: dead, leaning or fallen trees and limbs, and pruning requests.",
    "Water service": "Leaks, breaks or low pressure on the city water system up to and including the meter, and discoloured tap water.",
    "Sewer backup": "Sewage backing up into a building from the city main, or overflowing from a manhole.",
    "Storm drain and flooding": "Blocked storm drains and catch basins, and water pooling in streets after rain or snowmelt.",
    "Rodents and pests": "Rats, mice or insects on public property or outdoors; infestations inside a rental unit are Rental housing conditions.",
    "Rental housing conditions": "Code problems inside or on a rental unit: no heat, mould, leaks from the building's own plumbing or from another unit, pests inside, broken locks.",
    "Animal services": "Stray, injured or dead animals, dog bites and animal cruelty.",
    "Encampment outreach": "Requests for outreach to people living outdoors or in vehicles, and encampments on public property.",
    "Parks maintenance": "Damaged playground equipment, park restrooms and drinking fountains, sports fields and park litter bins.",
    "Utility billing": "Questions, credits and disputes about water, sewer or trash charges on the city utility bill.",
    "none of these": "The request fits none of the other listed categories or is not a city service.",
}


def pc(*names):
    return [(n, PC[n]) for n in names]


RULE = ("Port Calloway 311 coding rule: code each request by the city asset or service that needs action, "
        "not by the caller's words or where the problem was noticed.")

ITEMS = [
# ------------------------------------------------------------------ p01
# why: water rising from the pavement at the meter box, dry weather -> city water system up to the meter -> Water service
#      (the forming pothole is a consequence). twin: after a storm, blocked grate, pooling -> Storm drain and flooding.
C("p01", "Which 311 category should this request be coded under?",
f"""
{RULE}

Request #PC-26-114502   Channel: phone   Agent: T. Okonjo
Location: in front of 18 Linden Terrace

Caller notes (agent summary):
Caller says there has been "a river" running down the gutter in front of her house since about 6 a.m. It has not rained all week. She says the water is bubbling up out of the pavement right beside the small metal meter box at the edge of her front strip, and the asphalt around that spot has started to sink and break apart, so she thinks a pothole is forming. Her own taps have weak pressure. She is worried a car will hit the hole overnight. Neighbour at 20 Linden reports the same low pressure.
""",
list(PC.items()),
"Water service", 2,
twin=T([("It has not rained all week. She says the water is bubbling up out of the pavement right beside the small metal meter box at the edge of her front strip, and the asphalt around that spot has started to sink and break apart, so she thinks a pothole is forming. Her own taps have weak pressure.",
         "It rained hard all night. She says the grate at the corner is packed with leaves and the runoff has nowhere to go, so water is pooling across half the street and over the curb, and she thinks a pothole is hiding under it. Her own taps are fine.")],
       "Storm drain and flooding")),

# ------------------------------------------------------------------ p02
# why: repaired private leak; caller wants the leak-adjustment credit on the bill -> Utility billing (leak words mislead).
#      twin: water spraying from the meter box now -> Water service.
C("p02", "Code this 311 contact using the Port Calloway categories.",
f"""
{RULE}

Request #PC-26-118930   Channel: web form
Location: 4471 Wexford Ave (single-family, owner-occupied)

Resident message:
"Hi. My March statement showed 48,000 gallons, about eight times what we normally use. We found a leak in the supply line under the kitchen sink and our plumber fixed it on March 22 (invoice attached, Halden Plumbing #7719). I read on the city site that there is a one-time adjustment for leaks that are repaired within 30 days. I'm asking for the leak adjustment credit on my account, number 0043-2291-07. The meter reading has been normal since the repair. Thanks, Wendell Achara."
""",
pc("Utility billing", "Water service", "Rental housing conditions", "Sewer backup", "Storm drain and flooding",
   "Construction and permits", "none of these"),
"Utility billing", 2,
twin=T([("I'm asking for the leak adjustment credit on my account, number 0043-2291-07. The meter reading has been normal since the repair.",
         "But now water is spraying out of the city meter box by the sidewalk and the meter dial is spinning even with every tap in the house off. Account 0043-2291-07.")],
       "Water service")),

# ------------------------------------------------------------------ p03
# why: pests inside a rental unit -> Rental housing conditions (the codebook routes indoor rental infestations there).
#      twin: rats on the city-owned lot and sidewalk, not inside -> Rodents and pests.
C("p03", "Which category from the 311 codebook applies?",
f"""
{RULE}

Request #PC-26-120077   Channel: phone (Spanish-language line)   Agent: L. Barrientos
Location: 312 Corliss St, Apt 3B (rented)

Agent summary (translated):
Caller rents apartment 3B. She has seen rats in her kitchen three nights in a row, including one inside the cabinet under the sink where there is a gap around the pipe, and droppings on the counter. She has two small children. She told the building manager a week ago and he said he would "send someone," but nobody has come. She says the rats are inside her unit, and she is asking the city to inspect. She mentions there is a vacant city-owned lot next door with tall weeds.
""",
pc("Rental housing conditions", "Rodents and pests", "Illegal dumping", "Parks maintenance", "Animal services",
   "Construction and permits", "Sewer backup", "none of these"),
"Rental housing conditions", 2,
twin=T([("She has seen rats in her kitchen three nights in a row, including one inside the cabinet under the sink where there is a gap around the pipe, and droppings on the counter. She has two small children. She told the building manager a week ago and he said he would \"send someone,\" but nobody has come. She says the rats are inside her unit, and she is asking the city to inspect.",
         "She has seen rats three nights in a row running between the weeds and the sidewalk, and burrows along the fence line. She has two small children. Her apartment itself is clean and she has seen nothing inside. She says the rats are outside, and she is asking the city to inspect.")],
       "Rodents and pests")),

# ------------------------------------------------------------------ p04
# why: concrete saw at 10:40 p.m. on a weekday is construction outside permitted hours -> Construction and permits (not Noise complaint).
#      twin: a rooftop party with a DJ -> Noise complaint.
C("p04", "Assign the correct 311 category.",
f"""
{RULE}

Request #PC-26-121845   Channel: app   Submitted: Wednesday 22:41
Location: 1419 Harbor Blvd (mixed-use lot)

Resident text:
"It is 10:40 on a Wednesday night and a crew running a concrete saw on the lot at 1419 Harbor has been at it since 9. The whole block can hear it and my kid has school tomorrow. There's a permit sign on the fence but I can't read the details from here. This is the third night this week. Please send someone. — Ophelia Strand, 1422 Harbor, 2nd floor"

Attachments: 1 video (38 s, audio clearly audible).
""",
pc("Construction and permits", "Noise complaint", "Parking enforcement", "Road surface repair", "Sidewalk and curb repair",
   "Street lighting", "none of these"),
"Construction and permits", 2,
twin=T([("a crew running a concrete saw on the lot at 1419 Harbor has been at it since 9. The whole block can hear it and my kid has school tomorrow. There's a permit sign on the fence but I can't read the details from here.",
         "a crowd with a DJ and two big speakers on the roof deck at 1419 Harbor has been at it since 9. The whole block can hear it and my kid has school tomorrow. It's the bar's weekly rooftop night.")],
       "Noise complaint")),

# ------------------------------------------------------------------ p05
# why: a sidewalk slab lifted by a street-tree root is coded Sidewalk and curb repair by definition.
#      twin: a dead limb hanging over the sidewalk -> Street tree.
C("p05", "Which Port Calloway 311 category fits this request?",
f"""
{RULE}

Request #PC-26-123301   Channel: phone   Agent: M. Adeyemi
Location: sidewalk in front of 77 Birchwood Ln

Agent summary:
Caller walks her mother, who uses a walker, past 77 Birchwood every morning. The big city oak planted in the strip between the sidewalk and the street has a root that has pushed up one concrete slab about three inches, so there is a sharp edge across the whole walkway. Her mother nearly fell yesterday. The caller says the tree itself looks healthy and she does not want it cut down; she wants the walkway made safe. Two neighbours have complained about the same spot.
""",
pc("Sidewalk and curb repair", "Street tree", "Road surface repair", "Parks maintenance", "Signs and pavement markings",
   "Construction and permits", "Storm drain and flooding", "none of these"),
"Sidewalk and curb repair", 3,
twin=T([("has a root that has pushed up one concrete slab about three inches, so there is a sharp edge across the whole walkway. Her mother nearly fell yesterday. The caller says the tree itself looks healthy and she does not want it cut down; she wants the walkway made safe.",
         "has a large dead limb, bare of leaves and cracked at the base, hanging over the walkway about ten feet up. A piece fell near her mother yesterday. The caller says the concrete itself is fine; she wants the limb dealt with.")],
       "Street tree")),

# ------------------------------------------------------------------ p06
# why: unmoved for five days with two flat tyres on a public street -> Abandoned vehicle.
#      twin: arrived this morning and blocks a driveway, tyres fine -> Parking enforcement.
C("p06", "Code this request under the 311 codebook.",
f"""
{RULE}

Request #PC-26-125660   Channel: web form
Location: curb outside 902 Tremont St (public street)

Resident message:
"There's a grey sedan with out-of-state plates outside my house. It's been sitting in the same spot since last Friday, five days now, with two flat tyres and a pile of flyers under the wiper. Street sweeping came through Tuesday and went around it. It's not blocking anything, but it's clearly not going anywhere and I'm worried it's stolen. — Kofi Lindgren"
""",
pc("Abandoned vehicle", "Parking enforcement", "Illegal dumping", "Encampment outreach", "Road surface repair",
   "Signs and pavement markings", "none of these"),
"Abandoned vehicle", 2,
twin=T([("It's been sitting in the same spot since last Friday, five days now, with two flat tyres and a pile of flyers under the wiper. Street sweeping came through Tuesday and went around it. It's not blocking anything, but it's clearly not going anywhere and I'm worried it's stolen.",
         "It pulled in at 7 this morning, tyres and everything look fine, and it's parked straight across my driveway apron so I can't get my car out for work. I knocked on doors and nobody on the block knows whose it is.")],
       "Parking enforcement")),

# ------------------------------------------------------------------ p07
# why: tagging on a private garage whose owner has NOT signed the consent form -> Graffiti removal does not apply; nothing else fits -> none of these.
#      twin: owner signed the consent form -> Graffiti removal.
C("p07", "Which category should the 311 agent choose? Pick none of these if no category applies.",
f"""
{RULE}

Request #PC-26-126014   Channel: phone   Agent: R. Tamsin
Location: detached garage behind 55 Quarry Rd, facing the public alley

Agent summary:
Caller owns the house and garage at 55 Quarry Rd. Overnight someone spray-painted large black letters and a crown symbol across the alley side of her garage door, visible to anyone driving down the alley. She wants the city crew to paint over it this week. When asked, she said she has never filled out the city's removal consent form and does not want to sign anything today because her husband handles the property paperwork. She asked whether the police should be called; agent gave her the non-emergency number.
""",
pc("Graffiti removal", "Illegal dumping", "Signs and pavement markings", "Construction and permits", "Parks maintenance",
   "Rental housing conditions", "none of these"),
"none of these", 3,
twin=T([("When asked, she said she has never filled out the city's removal consent form and does not want to sign anything today because her husband handles the property paperwork.",
         "When asked, she said she signed the city's removal consent form last spring after an earlier incident, and the agent confirmed it is on file for this address.")],
       "Graffiti removal")),

# ------------------------------------------------------------------ p08
# why: the resident is putting out her own mattress -> Bulk item pickup.
#      twin: a mattress and tyres left by someone else in the public alley -> Illegal dumping.
C("p08", "Select the 311 category for this request.",
f"""
{RULE}

Request #PC-26-127390   Channel: app
Location: 2208 Orchard Way

Resident text:
"Hi, we just replaced our queen mattress and box spring and the old ones are in our garage. The store wouldn't haul them away. Can the city come get them? I can drag them out to the curb in front of our house the night before whatever day you tell me. They're wrapped in plastic. Also a broken dresser if that's allowed. Thanks! — Priyanka Holt"
""",
pc("Bulk item pickup", "Illegal dumping", "Collection not completed", "Utility billing", "Rodents and pests",
   "Parks maintenance", "none of these"),
"Bulk item pickup", 2,
twin=T([("we just replaced our queen mattress and box spring and the old ones are in our garage. The store wouldn't haul them away. Can the city come get them? I can drag them out to the curb in front of our house the night before whatever day you tell me. They're wrapped in plastic. Also a broken dresser if that's allowed.",
         "someone dumped a queen mattress, a box spring and four old tyres in the public alley behind our house and the library sometime last night. None of it is ours and none of the neighbours know who did it. Can the city come get them?")],
       "Illegal dumping")),

# ------------------------------------------------------------------ p09
# why: a person living in a car in the park lot for weeks; the car moves every few days (so not unmoved 72 h, not inoperable) -> Encampment outreach.
C("p09", "Which category from the 311 codebook fits this report?",
f"""
{RULE}

Request #PC-26-128811   Channel: phone   Agent: D. Ferreira
Location: Kimball Park upper lot

Agent summary:
Caller walks her dog in Kimball Park every morning. For about three weeks a man has been sleeping in a blue minivan in the upper parking lot. The van has blankets over the windows and a camp stove on the ground beside it some mornings. It moves out of the lot every two or three days and comes back the same evening; the tyres and windows look fine. The caller says the man is polite and she is not asking for anyone to be ticketed; she thinks he may need help and wants someone from the city to check on him. She also mentions the lot's litter bin is overflowing.
""",
list(PC.items()),
"Encampment outreach", 2),

# ------------------------------------------------------------------ p10
# why: pedestrian push-button that does nothing -> Traffic signal fault (a signal device), not Signs and pavement markings.
C("p10", "Code this 311 request.",
f"""
{RULE}

Request #PC-26-129204   Channel: web form
Location: intersection of Mercer Ave and 14th St, northeast corner

Resident message:
"The button you push to cross Mercer at 14th hasn't worked for at least a week. You press it, nothing clicks, and the little white walking-person light never comes on, so people just run across when there's a gap. The painted crosswalk lines are fine and the stop line is fine. There's a school two blocks away and kids cross here every afternoon. Please fix before someone gets hurt. — Nadia Bergström"
""",
pc("Traffic signal fault", "Signs and pavement markings", "Street lighting", "Sidewalk and curb repair", "Road surface repair",
   "Parking enforcement", "none of these"),
"Traffic signal fault", 2),

# ------------------------------------------------------------------ p11
# why: a stop sign knocked flat -> Signs and pavement markings, not Traffic signal fault (there are no lights at this corner).
C("p11", "Which Port Calloway category applies to this contact?",
f"""
{RULE}

Request #PC-26-130155   Channel: phone   Agent: S. Whitlock
Location: Harwood Rd at Pell Lane (four-way stop, no traffic lights)

Agent summary:
Caller says a delivery truck backed into the pole on the southeast corner this afternoon and the red octagonal sign is now lying flat in the grass, face down. Drivers coming north on Harwood cannot tell they are supposed to halt and two cars nearly collided while he was watching. There are no traffic lights at this corner. He asks for an urgent fix. The truck left; he did not get a plate number.
""",
pc("Signs and pavement markings", "Traffic signal fault", "Street lighting", "Road surface repair", "Illegal dumping",
   "Sidewalk and curb repair", "Parking enforcement", "none of these"),
"Signs and pavement markings", 2),

# ------------------------------------------------------------------ p12
# why: a dead raccoon in the travel lane -> Animal services (dead animals), not Road surface repair or Illegal dumping.
C("p12", "What 311 category does this request belong to?",
f"""
{RULE}

Request #PC-26-131470   Channel: app   Photo attached
Location: eastbound lane, 600 block of Ferris Parkway

Resident text:
"There's a dead raccoon in the eastbound lane on Ferris, right past the bus stop, next to a big crack in the asphalt. Cars are swerving around it into the bike lane. It's been there since at least yesterday morning and it's starting to smell. Someone also dropped a fast-food bag next to it. Can someone come remove it? — Gideon Marsh"
""",
pc("Animal services", "Road surface repair", "Illegal dumping", "Collection not completed", "Storm drain and flooding",
   "Rodents and pests", "none of these"),
"Animal services", 2),

# ------------------------------------------------------------------ p13
# why: an overflowing toilet in a park restroom building -> Parks maintenance (park restrooms), not Sewer backup
#      (no building backup from the main, no manhole).
C("p13", "Choose the 311 category for this report.",
f"""
{RULE}

Request #PC-26-132008   Channel: phone   Agent: A. Nwosu
Location: Tilden Field, restroom building by the soccer pitches

Agent summary:
Caller is a youth soccer coach. The toilet in the men's side of the restroom building at Tilden Field is clogged and overflowing; dirty water is running out the door onto the concrete path. The manholes in the parking lot look normal, and the women's side is working. About 200 kids have games there Saturday. He is asking for the toilet to be fixed and the building to be cleaned before then.
""",
list(PC.items()),
"Parks maintenance", 3),

# ------------------------------------------------------------------ p14
# why: sewage rising through the basement floor drain of a single-family home -> backup from the city main -> Sewer backup.
#      twin: water from the ceiling comes from the upstairs unit's toilet in a rental -> Rental housing conditions.
C("p14", "Under the Port Calloway codebook, which category fits?",
f"""
{RULE}

Request #PC-26-133516   Channel: phone (after-hours line)   Agent: J. Kaminski
Location: 67 Alder Court (single-family, owner-occupied)

Agent summary:
Caller says dark, foul-smelling water started coming up through the floor drain in his basement about an hour ago and is now two inches deep around the furnace. Nobody in the house has flushed or run water since dinner. His neighbour at 69 Alder has the same thing. It has not rained today. He has shut off the furnace and moved his family upstairs.
""",
pc("Sewer backup", "Storm drain and flooding", "Water service", "Rental housing conditions", "Utility billing",
   "Construction and permits", "none of these"),
"Sewer backup", 2,
twin=T([("Location: 67 Alder Court (single-family, owner-occupied)",
         "Location: 67 Alder Court, Apt 2A (rented; landlord unreachable)"),
        ("Caller says dark, foul-smelling water started coming up through the floor drain in his basement about an hour ago and is now two inches deep around the furnace. Nobody in the house has flushed or run water since dinner. His neighbour at 69 Alder has the same thing.",
         "Caller says dirty, foul-smelling water started dripping through his bathroom ceiling about an hour ago; the toilet in apartment 3A directly above overflowed, and the tenant there confirmed it. His neighbours on the ground floor have no problem."),
        ("He has shut off the furnace and moved his family upstairs.",
         "He has put buckets down and moved his family into the living room.")],
       "Rental housing conditions")),

# ------------------------------------------------------------------ p15
# why: scheduled recycling day passed, carts at the curb on time and still full; neighbours too -> Collection not completed.
C("p15", "Which 311 category should the agent select?",
f"""
{RULE}

Request #PC-26-134022   Channel: web form   Submitted: Wednesday 16:10
Location: 800 block of Dunmore Street

Resident message:
"Our recycling day is Tuesday. I had my blue cart at the curb by 6:30 a.m. Tuesday, lid closed, nothing blocking it, same as every week. It's Wednesday afternoon and every blue cart on the 800 block of Dunmore is still sitting there full. The trash carts were emptied fine. I also want to ask how to get a bigger recycling cart, but that can wait. — Hollis Engstrom"
""",
pc("Collection not completed", "Bulk item pickup", "Illegal dumping", "Utility billing", "Parks maintenance",
   "Rodents and pests", "none of these"),
"Collection not completed", 2),

# ------------------------------------------------------------------ p16
# why: streetlights lit in the middle of the day -> Street lighting (definition includes lit during daylight); not a signal.
C("p16", "Code the request under the city 311 codebook.",
f"""
{RULE}

Request #PC-26-135299   Channel: app   Submitted: Thursday 13:05
Location: poles 14 through 19, Canal Road between Bristow and Keel
Photos attached: 2, timestamped 12:58. Earlier requests at this location: none in 12 months.

Resident text:
"Six of the lamps along Canal Road between Bristow and Keel have been on all day today and yesterday, bright sunshine and all. The traffic lights at Bristow are working normally. Seems like a waste of electricity. Maybe the sensor is broken? — Tamsin Oduya"
""",
list(PC.items()),
"Street lighting", 2),

# ------------------------------------------------------------------ p17
# why: dumping on a neighbour's private yard is not on public property -> not Illegal dumping (no).
#      twin: on the vacant city-owned lot -> public property -> yes.
Y("p17", "Can this report be coded Illegal dumping under the 311 codebook?",
f"""
{RULE}

Request #PC-26-136640   Channel: phone   Agent: B. Castellanos
Location: 41 Whitby Row

Agent summary:
Caller says that over the weekend someone left a stack of broken drywall, paint cans and a torn sofa in the side yard of the privately owned house next door at 43 Whitby, which has been empty since the owner moved to a care home. Nobody lives there and the caller does not know who left the items. He is worried about rats and kids climbing on the pile. He asks the city to haul it away.
""",
[("Illegal dumping", PC["Illegal dumping"]),
 ("Public property", "streets, alleys, parks and city-owned lots; privately owned land is not public property even when vacant.")],
0, 2,
twin=T([("in the side yard of the privately owned house next door at 43 Whitby, which has been empty since the owner moved to a care home. Nobody lives there",
         "on the vacant city-owned lot next door at 43 Whitby, where the city tore down a condemned house last year. Nobody uses the lot")],
       1)),

# ------------------------------------------------------------------ p18
# why: first seen Monday 08:00, call Thursday 07:00 = 71 h (<72) and not inoperable -> not Abandoned vehicle (no).
#      twin: call Thursday 09:00 = 73 h (>72) -> yes.
Y("p18", "Does this vehicle meet the Abandoned vehicle definition at the time of the call?",
f"""
{RULE}

Request #PC-26-137015   Channel: phone   Agent: E. Moravec
Call received: Thursday 07:00
Location: curb outside 1150 Garnet St (public street)

Agent summary:
Caller says a white pickup truck parked outside her house at 08:00 on Monday; she remembers because she was leaving for work. She is sure it has not moved since, because a leaf pile she raked into the gutter is still pressed against its front tyre. The truck's tyres are fully inflated, windows are intact, and the registration sticker is current. It is not blocking her driveway or a hydrant. She wants it removed.
""",
[("Abandoned vehicle", PC["Abandoned vehicle"]),
 ("Time unmoved", "hours from when the vehicle was first seen in the spot to the time of the call.")],
0, 3,
twin=T([("Call received: Thursday 07:00", "Call received: Thursday 09:00")], 1)),

# ------------------------------------------------------------------ p19
# why: jackhammer at 06:15 on a weekday is outside permitted hours (7-19) -> inside Construction and permits -> "outside the category?" no.
#      twin: 08:15 with a posted permit, safe site -> no violation -> outside the category -> yes.
Y("p19", "Does this request fall outside the Construction and permits category?",
f"""
{RULE}

Request #PC-26-138230   Channel: app   Submitted: Tuesday
Location: 2300 block of Varley Ave

Resident text:
"A crew started jackhammering the old driveway at 2310 Varley at 06:15 this morning, Tuesday. There's a city permit posted on the fence, the site is fenced off and the workers have hard hats and cones out, so it looks safe, but the noise woke up my whole house. How is this allowed? — Anneliese Kroft"
""",
[("Construction and permits", PC["Construction and permits"]),
 ("Permitted hours", "7 a.m. to 7 p.m. on weekdays; 9 a.m. to 5 p.m. on weekends.")],
0, 2, role="neg",
twin=T([("at 06:15 this morning, Tuesday", "at 08:15 this morning, Tuesday")], 1)),
]
