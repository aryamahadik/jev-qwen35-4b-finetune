"""policy_c / housing co-ops, residents' associations and short-let hosting
(Greystone Row Housing Cooperative, Harrowgate Mews Residents' Association, Burrowly short lets,
Pennard Borough housing register)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ ho01
# why: registration issued Nov 2023 -> grandfathered cap 120. Stayed nights 10+14+21+25+30+12 = 112
# (cancelled 7 do not count). 112 + 6 = 118 <= 120 -> accept. Twin: issued Mar 2024 -> cap 90 -> block.
C("ho01", "What should Burrowly do with the new booking request for listing BW-30918?",
"""
Burrowly Host Compliance — Castlebridge night cap
Castlebridge City rules, as enforced by Burrowly:
• Entire-home listings may be booked for at most 90 nights per calendar year.
• Entire-home listings whose Castlebridge registration was issued before 1 January 2024 are grandfathered at 120 nights per calendar year.
• Hosted listings (a private room where the host lives on site) have no night cap.
• Only nights that were stayed count; bookings cancelled before check-in do not.
• Burrowly blocks any booking that would take the listing past its cap for the year. Listings without a registration number are suspended instead.

Listing BW-30918 — "Sunny two-bed by the Castlebridge canal" — entire home, host lives elsewhere.
Registration: CB-STR-004417, issued 14 November 2023.
2026 stays so far: 10 nights (Jan), 14 nights (Mar), 21 nights (Apr), 25 nights (Jun), 30 nights (Aug), 12 nights (Sep).
Cancelled before check-in: one 7-night booking in May.
New request: 18–24 October 2026 (6 nights), two adults.
""",
[("accept the booking", "the booking keeps the listing within its night cap."),
 ("block the booking — night cap", "the booking would take the listing past its cap for the year."),
 ("suspend the listing — no registration", "the listing lacks a valid registration number."),
 ("treat as hosted — no cap", "the listing is a private room in the host's own home."),
 ("refer to Castlebridge City", "the case is outside what Burrowly can decide and goes to the city.")],
"accept the booking", 3,
twin=T([("issued 14 November 2023", "issued 14 March 2024")], "block the booking — night cap")),

# ------------------------------------------------------------------ ho02
# why: Ferry Lane numbers 1-40 are in Wexley, which has no scheme -> no number needed -> 0.
# Twin: number 59 -> Castlebridge, entire home without a number -> breach -> 1.
Y("ho02", "Does the listing breach the registration-number rule?",
"""
Burrowly — Local Registration Rules (host help centre extract)
Castlebridge City: every entire-home listing must show a valid city registration number in the listing's "Licence" field. Hosted room listings (host lives on site) are exempt. Listings that break this rule are hidden until a number is added.
Wexley District: no registration scheme is in force; no number is required.
Boundary note: Ferry Lane runs along the river boundary. Numbers 1–40 are in Wexley District and numbers 41–90 are in Castlebridge City.

Automated check #RG-5521
Listing: "Riverside loft with balcony" — entire home, sleeps 4
Address on file: Unit 4, 19 Ferry Lane
Licence field: empty
Host: Priyanka S. (host since 2022, 4.92 rating)
Trigger: the listing's map pin sits within 200 m of the Castlebridge boundary, so the system flagged it for manual review.
""",
[("Registration breach", "an entire-home listing in Castlebridge City without a registration number."),
 ("No registration required", "the listing is outside Castlebridge City or is a hosted room.")],
0, 2,
twin=T([("Unit 4, 19 Ferry Lane", "Unit 4, 59 Ferry Lane")], 1)),

# ------------------------------------------------------------------ ho03
# why: Biscuit was grandfathered, but the exemption does not pass to Pepper (26 kg > 20 kg, not an
# assistance dog) -> breach, weight limit. Two pets (dog + cat) is within limit; registered in 5 days.
# Twin: Pepper is a certified assistance dog -> compliant under the assistance exception.
C("ho03", "Which finding should the co-op office record for flat 7C?",
"""
Greystone Row Housing Cooperative — Bylaw 12 (Animals), as amended 1 March 2025
12.1 A household may keep at most two pets. Fish tanks and caged birds are not counted.
12.2 Dogs with an adult weight over 20 kg are not permitted, except assistance dogs trained by a recognised assistance-dog organisation.
12.3 Dogs over 20 kg that were registered with the co-op before 1 March 2025 may stay for the life of that animal. The exemption belongs to the animal and does not pass to a replacement dog.
12.4 Every dog and cat must be registered with the office within 14 days of arrival.

Office file — Flat 7C, member Joy Adebayo
• 2023: registered "Biscuit", Labrador, 29 kg.
• May 2026: Biscuit died (member informed the office).
• 3 August 2026: member adopted "Pepper", a Labrador cross, 26 kg, from Wexley Rescue; registered 8 August 2026.
• Also registered: one cat ("Moth"), since 2021.
Neighbour's note: "Pepper is lovely but she's the size of Biscuit — I thought big dogs weren't allowed any more?"
""",
[("compliant — grandfathered dog", "a dog over 20 kg registered before 1 March 2025."),
 ("compliant — assistance dog", "a dog over 20 kg trained by a recognised assistance-dog organisation."),
 ("breach — dog over the weight limit", "a dog over 20 kg that is neither grandfathered nor an assistance dog."),
 ("breach — too many pets", "more than two counted pets in the household."),
 ("breach — late registration", "a dog or cat registered more than 14 days after arrival.")],
"breach — dog over the weight limit", 2,
twin=T([("a Labrador cross, 26 kg, from Wexley Rescue",
         "a Labrador cross, 26 kg, trained and certified as a hearing dog by Hearing Dogs North, a recognised assistance-dog charity")],
       "compliant — assistance dog")),

# ------------------------------------------------------------------ ho04
# why: substantiated = 12 Jan, 28 Apr, 19 Jul (2 Mar unsubstantiated). 12 Jan -> 19 Jul exceeds 6 months,
# so no 6-month window holds 3 -> no warning (0). Twin: 14 Feb instead of 12 Jan -> 14 Feb..19 Jul
# within 6 months -> 3 -> warning (1).
Y("ho04", "Must the association send the flat 3B household a formal warning letter?",
"""
Harrowgate Mews Residents' Association — House Rule 5 (Noise)
5.1 Quiet hours are 23:00 to 07:00 every day; power tools may be used only 08:00–20:00.
5.2 A complaint is substantiated only if a warden attended and confirmed the noise, or the office reviewed a recording and confirmed it.
5.3 Three substantiated complaints against the same household within any six-month period lead to a formal warning letter. Unsubstantiated complaints are logged but not counted.

Complaint log — Flat 3B (as at 1 August 2026)
– 12 Jan 2026, 00:40: party music — warden attended, confirmed.
– 2 Mar 2026, 23:30: loud bass — no warden available, no recording supplied.
– 28 Apr 2026, 21:15: drilling — recording supplied by flat 2B, reviewed by office, confirmed.
– 19 Jul 2026, 23:50: shouting on balcony — warden attended, confirmed.
Flat 3B's written response: "We've had one party this year and we apologised to everyone."
""",
[("Formal warning letter", "required after three substantiated complaints within a six-month period."),
 ("Logged only", "fewer than three substantiated complaints fall within any six-month period.")],
0, 3,
twin=T([("– 12 Jan 2026, 00:40: party music", "– 14 Feb 2026, 00:40: party music")], 1)),

# ------------------------------------------------------------------ ho05
# why: 19 consecutive nights > 14 -> occupant needing approval; no payment -> not subletting; not advertised.
# Twin: 12 consecutive nights; 12 + 10 = 22 <= 30 in 12 months -> no breach.
C("ho05", "Which Occupancy Rule finding applies to flat 2A?",
"""
Greystone Row Housing Cooperative — Occupancy Rule 8
8.1 Guests: a member may host a guest for up to 14 consecutive nights, and for no more than 30 nights in total in any 12-month period. A guest who exceeds either limit becomes an occupant and must be approved by the committee in advance.
8.2 Subletting: taking any payment (rent, a share of bills, or goods in lieu) from a person for staying in the flat, without committee consent.
8.3 Short-letting: advertising the flat or a room on a booking platform. Always prohibited.

Complaint received 9 September 2026 — Flat 2A, member Tom Ashby
Neighbour: "There's been a young man staying at 2A for weeks. Is he a lodger?"
Member's reply to the office: "He's my cousin Ravi, over from Leicester for a job trial. He's staying 19 consecutive nights, 23 August to 11 September, sleeping on the sofa bed. He doesn't pay me anything — he's family. He also stayed 10 nights last December."
Office check: no advert for flat 2A found on any booking platform.
""",
[("unapproved occupant", "a guest who exceeded the consecutive-night or 12-month limit without prior committee approval."),
 ("unauthorised subletting", "payment taken for the stay without committee consent."),
 ("prohibited short-letting", "the flat or a room advertised on a booking platform."),
 ("nuisance", "behaviour by a member or guest that disturbs neighbours."),
 ("no breach", "the stay is within the guest limits and no other rule is broken.")],
"unapproved occupant", 2,
twin=T([("He's staying 19 consecutive nights, 23 August to 11 September", "He's staying 12 consecutive nights, 30 August to 11 September")],
       "no breach")),

# ------------------------------------------------------------------ ho06
# why: host lives in the flat and shares kitchen and bathroom -> shared-living exception -> no breach (0).
# Twin: entire flat, host lives elsewhere -> sex restriction breaches the policy (1).
Y("ho06", "Does the guest restriction on this listing breach Burrowly's Non-discrimination Policy?",
"""
Burrowly — Non-discrimination Policy (Hosts), section 2
Hosts may not decline, restrict or set different terms for guests based on race, ethnicity, national origin, religion, sex, gender identity, sexual orientation, disability, marital status or age (other than requiring guests to be 18 or older).
Exception 2.4: where the host lives in the property and the guest will share living spaces with the host (such as the kitchen, bathroom or living room), the host may state a preference for guests of a particular sex or gender.

Listing BW-44120 — "Quiet room near Holloway Park"
Description: "Private room in my flat — I live here and we'd share the kitchen and bathroom. Double bed, desk, fast wifi, 6 minutes to the tram. Women guests only, sorry — I'm a woman living alone and that's what I'm comfortable with. No smoking, no parties."
Host: Agnieszka W. · host since 2024 · 38 reviews
Report from a guest: "I tried to book for me and my boyfriend and she refused. Isn't this discrimination?"
""",
[("Discriminatory restriction", "a guest restriction based on a listed characteristic that no exception permits."),
 ("Shared-living preference", "a sex or gender preference allowed because the host lives there and shares living spaces with guests.")],
0, 2,
twin=T([("Private room in my flat — I live here and we'd share the kitchen and bathroom.",
         "Entire flat, fully self-contained — I live across town and only pop by to clean.")], 1)),

# ------------------------------------------------------------------ ho07
# why: 2 days before check-in (<5) would be 50% under Moderate, but a government-declared flood emergency
# covering the destination is an extenuating circumstance -> full refund. Twin: guest's own injury is
# excluded -> host policy -> 50%.
C("ho07", "What refund is the guest owed for booking R-88217?",
"""
Burrowly — Refund rules (Guest Help Centre)
Host cancellation policy "Moderate": full refund of nightly charges if the guest cancels at least 5 days before check-in; 50% of nightly charges if the guest cancels less than 5 days before check-in. Service fees are refunded only on a full refund.
Extenuating Circumstances Policy: when a government declares an emergency, natural disaster or travel ban covering the listing's location, guests with stays during the declared period may cancel for a full refund regardless of the host's policy. Not covered: personal illness or injury, work commitments, transport delays, and weather that has not triggered a government declaration.

Booking R-88217 — cottage in Pellow, Dunmere County, host policy Moderate
Check-in: 12 September 2026 · 4 nights · £520 nightly charges
Guest cancelled: 10 September 2026, 18:05
Guest message: "So sorry — Dunmere County declared a flood emergency last night that covers Pellow, and the council has told people not to travel there."
Dunmere County Council notice, 9 September: state of emergency declared for Pellow and three other towns, 9–16 September.
""",
[("full refund — host policy", "the guest cancelled at least 5 days before check-in."),
 ("full refund — extenuating circumstances", "a qualifying government declaration covers the location and stay dates."),
 ("50% refund", "a late cancellation under the Moderate policy with no qualifying circumstance."),
 ("no refund", "the booking is not eligible for any refund."),
 ("travel credit only", "the guest receives Burrowly travel credit instead of money.")],
"full refund — extenuating circumstances", 2,
twin=T([("Dunmere County declared a flood emergency last night that covers Pellow, and the council has told people not to travel there.",
         "I broke my ankle this morning and can't manage the stairs to the cottage. (Pellow did have a flood warning on the news, not sure if that matters.)")],
       "50% refund")),

# ------------------------------------------------------------------ ho08
# why: rear balcony is the allowed location, but 90 cm > 80 cm limit -> breach (1). Twin: 70 cm -> 0.
Y("ho08", "Is the dish at flat 5D in breach of House Rule 9?",
"""
Harrowgate Mews Residents' Association — House Rule 9 (External fixtures)
9.1 No satellite dish, aerial or air-conditioning unit may be fixed to the street-facing façade.
9.2 A satellite dish may be placed on a rear balcony if its diameter is no more than 80 cm and it is free-standing or clamped to the balcony rail, not drilled into the brickwork.
9.3 Breaches are notified in writing and must be put right within 28 days.

Inspection report — 6 September 2026 — Flat 5D (rear, third floor)
Inspector: M. Oyelaran, building manager
Item: satellite dish on the rear balcony, clamped to the balcony rail; no drilling into brickwork observed.
Measured diameter: 90 cm.
Visible from the street: no.
Resident's comment: "It's the smallest one that gets the Turkish channels. It's clamped, not drilled, and nobody can see it from the road."
Other external fixtures at 5D: none.
""",
[("Breach of Rule 9", "a fixture on the street façade, or a rear-balcony dish that is over 80 cm or drilled into the brickwork."),
 ("Permitted dish", "a rear-balcony dish of 80 cm or less, free-standing or clamped.")],
1, 1,
twin=T([("Measured diameter: 90 cm.", "Measured diameter: 70 cm.")], 0)),

# ------------------------------------------------------------------ ho09
# why: arrears 1,540 / 640 = 2.41 months -> >=2 and <3 -> formal notice. Pending benefit not counted;
# plan offered but not agreed. Twin: 2,050 / 640 = 3.20 months, no plan -> referral.
C("ho09", "Which arrears step applies to member account GR-0417?",
"""
Greystone Row Housing Cooperative — Rent Arrears Procedure
Arrears are measured in months of the member's current monthly rent. Payments are counted only once received; pending payments do not reduce arrears.
• Arrears of at least 1 month: reminder letter.
• Arrears of at least 2 months: formal notice with an offer of a payment plan.
• Arrears of at least 3 months where no payment plan has been agreed: referral to the tenancy committee.
• A member who has agreed a payment plan and is keeping to it is not escalated further.

Account GR-0417 — Flat 11A — statement as at 1 September 2026
Monthly rent: £640
Arrears balance: £1,540
Pending: Universal Credit housing element of £640 expected 15 September (not yet received).
Notes: reminder letter sent 3 July. Payment plan offered by phone on 20 July; the member said she would "think about it" and has not signed or agreed a plan.
""",
[("reminder letter", "arrears of at least 1 but under 2 months."),
 ("formal notice with payment-plan offer", "arrears of at least 2 months, below the referral point."),
 ("referral to the tenancy committee", "arrears of at least 3 months with no agreed payment plan."),
 ("no escalation — keeping to a plan", "the member has an agreed payment plan and is keeping to it."),
 ("no action", "arrears below 1 month.")],
"formal notice with payment-plan offer", 3,
twin=T([("Arrears balance: £1,540", "Arrears balance: £2,050")], "referral to the tenancy committee")),

# ------------------------------------------------------------------ ho10
# why: moving the sink needs a new connection to the shared waste stack -> shared services -> approval needed
# -> "does NOT need approval" is false (0). Twin: sink stays, existing pipe reused -> like-for-like -> 1.
Y("ho10", "Is it true that the works at flat 4B do not need committee approval?",
"""
Greystone Row Housing Cooperative — Alterations Policy
Members must get written committee approval before starting any works that (a) affect the structure (walls, floors, ceilings, beams), (b) connect to, alter or move shared services (gas supply, electrical risers, water risers, the shared waste stack), or (c) change the outside of the building. Internal decoration and like-for-like replacement of fittings in the same position do not need approval.

Application form — Flat 4B — member Sanjay Rao
Works: replace kitchen cabinets and worktops with new units of the same size; tile the splashback; move the sink from the window wall to the opposite wall, which needs a new 2-metre waste pipe connecting into the shared waste stack behind the boxing.
Contractor: Hartley Kitchens Ltd (Gas Safe not needed — no gas work).
Start date requested: 21 September 2026.
Member's note: "It's just a kitchen refit, nothing structural, so I assume I can crack on?"
""",
[("Approval required", "works affecting structure, shared services or the outside of the building."),
 ("No approval needed", "internal decoration or like-for-like replacement in the same position.")],
0, 2, role="neg",
twin=T([("move the sink from the window wall to the opposite wall, which needs a new 2-metre waste pipe connecting into the shared waste stack behind the boxing",
         "replace the sink with a new one in the same position under the window, reusing the existing waste pipe")], 1)),

# ------------------------------------------------------------------ ho11
# why: pushchair in the ground-floor lobby alcove is the carve-out; recycling out Tue after 18:00 for Wed
# collection is allowed -> none. Twin: pushchair on the second-floor landing -> 3.2.
C("ho11", "Which house rule, if any, did the resident of flat 2C break?",
"""
Harrowgate Mews Residents' Association — House Rules (extract)
3.1 Noise — quiet hours 23:00–07:00.
3.2 Communal areas — nothing may be stored in stairwells, landings, corridors or the lobby, except that pushchairs and mobility aids may be left in the ground-floor lobby alcove.
3.3 Refuse — bins may be put out from 18:00 the evening before collection day and must be taken in by 20:00 on collection day. Collection day is Wednesday.
3.4 Smoking — no smoking or vaping in communal areas.
3.5 Pets — dogs must be on a lead in communal areas.
Where more than one rule is broken, record the lowest-numbered rule.

Caretaker's walk-round log, Tuesday 8 September, 21:30
– Flat 2C: pushchair folded and left in the ground-floor lobby alcove.
– Flat 2C: recycling bin put out at the kerb at 19:10.
– Flat 2C resident seen walking her dog, on a lead, through the lobby.
– No noise heard; no smoke smell in the stairwell.
""",
[("3.1 noise", "noise during quiet hours."),
 ("3.2 communal areas", "items stored in a communal area outside the permitted alcove."),
 ("3.3 refuse", "bins out too early or left out too late."),
 ("3.4 smoking", "smoking or vaping in a communal area."),
 ("3.5 pets", "a dog off the lead in a communal area."),
 ("none of these", "no house rule was broken.")],
"none of these", 2,
twin=T([("pushchair folded and left in the ground-floor lobby alcove", "pushchair folded and left on the second-floor landing")],
       "3.2 communal areas")),

# ------------------------------------------------------------------ ho12
# why: vaping counts as smoking, but the bench is 7 m from the entrance (>5 m) and outside -> no breach (0).
# Twin: 3 m -> within 5 m -> breach (1).
Y("ho12", "Did the resident breach the smoke-free rule?",
"""
Greystone Row Housing Cooperative — Smoke-free Rule
Smoking includes cigarettes, cigars, pipes, heated tobacco and e-cigarettes/vapes. Smoking is not allowed (a) inside any communal area, or (b) outdoors within 5 metres of any building entrance. Private flats and private balconies are not covered by this rule.

Complaint #SF-219, received 2 September 2026
"The man from flat 9A vapes on the bench by the front door every evening and it drifts into the lobby. Please do something."
Site check by the estate officer, 3 September: the bench in question is 7 m from the main entrance door and 12 m from the bin-store door. The officer observed the resident vaping there at 19:40. The lobby windows were open.
Resident's comment: "I go outside specifically so I don't bother anyone."
Previous smoke-free complaints about flat 9A: none.
""",
[("Smoke-free breach", "smoking or vaping inside a communal area, or outdoors within 5 metres of a building entrance."),
 ("Outside the rule", "smoking elsewhere outdoors, or inside a private flat or balcony.")],
0, 2,
twin=T([("the bench in question is 7 m from the main entrance door", "the bench in question is 3 m from the main entrance door")], 1)),

# ------------------------------------------------------------------ ho13
# why: checkout 2 Aug, filed 18 Aug = 16 days > 14 -> rejected as late (evidence is fine).
# Twin: filed 12 Aug = 10 days, photos + quote, accidental damage -> approve.
C("ho13", "How should Burrowly Resolutions decide damage claim DC-6604?",
"""
Burrowly — Host Damage Protection (claims rules)
1. A host must file a claim within 14 days of the guest's checkout.
2. The claim must include photos of the damage and a receipt or written repair/replacement quote.
3. Normal wear and tear (gradual deterioration from ordinary use) is not covered.
4. A claim that meets 1–3 is approved up to the quote amount. A claim missing evidence under 2 is paused and the host is asked for it; a late claim or a wear-and-tear claim is rejected.

Claim DC-6604
Listing: "Garden flat, Ellery Road" — host Martin Oduya
Guest checkout: 2 August 2026, 10:00
Claim filed: 18 August 2026, 21:40
Item: glass coffee table top — cracked across the middle
Evidence: 3 photos of the crack; quote from Clearview Glass for £185 replacement
Host statement: "The guests' child was standing on the table in the video from our outdoor doorbell cam — clearly not wear and tear. Sorry for the delay, I was abroad."
Guest response: none within 72 hours.
""",
[("approve the claim", "filed in time, fully evidenced, and not wear and tear."),
 ("reject — filed late", "filed more than 14 days after checkout."),
 ("reject — wear and tear", "the damage is gradual deterioration from ordinary use."),
 ("pause — request evidence", "photos or a receipt/quote are missing.")],
"reject — filed late", 2,
twin=T([("Claim filed: 18 August 2026, 21:40", "Claim filed: 12 August 2026, 21:40")], "approve the claim")),

# ------------------------------------------------------------------ ho14
# why: 22 < 25, one positive review < 3, entire home, 1 night, 8 miles < 25 -> blocked (1).
# Twin: guest aged 26 -> rule does not apply (0).
Y("ho14", "Must Burrowly block this booking under the Party Prevention rule?",
"""
Burrowly — Party Prevention Rule (booking system)
A guest who is under 25 AND has fewer than three positive reviews on Burrowly may not book an entire-home listing for a one-night stay within 25 miles of their home address. They may still book private rooms, or entire homes for two nights or more. Guests 25 and over, and under-25s with three or more positive reviews, are not affected. All guests must be at least 18.

Booking attempt #BA-551903
Guest age: 22
Guest reviews: 1 positive review (2025)
Home address on the verified ID: Wexley
Listing: "Barn conversion with hot tub" — entire home, sleeps 10, 8 miles from Wexley
Stay: Saturday 3 October 2026, one night
Guest message to the host: "Hi! Quiet birthday weekend with my family, my mum is coming too."
""",
[("Blocked booking", "an under-25 guest with fewer than three positive reviews booking an entire home for one night within 25 miles of home."),
 ("Permitted booking", "any booking the Party Prevention rule does not restrict.")],
1, 2,
twin=T([("Guest age: 22", "Guest age: 26")], 0)),

# ------------------------------------------------------------------ ho15
# why: bedroom standard: couple 1; daughter 15 has no same-sex 10-20 partner -> pairs with daughter 8
# (same-sex under-10); son 12 alone -> 3 bedrooms needed, has 2 -> overcrowded -> Band B.
# Twin: three-bedroom flat -> not overcrowded; 6 years in borough -> Band C.
C("ho15", "Which priority band should the Pennard Borough housing register give the Nowak household?",
"""
Pennard Borough — Housing Register Allocation Scheme
Band A: statutorily homeless, or urgent medical need certified by the medical panel.
Band B: overcrowded — the household lacks one or more bedrooms under the bedroom standard.
Band C: local connection (5+ years living or working in the borough), not in Band A or B.
Band D: no local connection, not in Band A or B.

Bedroom standard: one bedroom for each couple; each other person aged 21 or over; each pair of people aged 10–20 of the same sex; each pair of children under 10 of any sex. An unpaired person aged 10–20 shares with an unpaired child under 10 of the same sex if there is one; otherwise they get their own bedroom. Any remaining child under 10 gets their own bedroom.

Application HR-26-3310 — the Nowak household
Current home: a two-bedroom flat, privately rented, Pennard Borough.
Household: Ewa (38) and Piotr (40), married; daughter Zofia (15); son Kuba (12); daughter Lena (8).
Local connection: the household has lived in the borough for 6 years.
Homelessness: not threatened. Medical panel: no application made.
""",
[("Band A", "statutorily homeless, or certified urgent medical need."),
 ("Band B", "overcrowded under the bedroom standard."),
 ("Band C", "local connection and not in Band A or B."),
 ("Band D", "no local connection and not in Band A or B.")],
"Band B", 3, ordered=True,
twin=T([("a two-bedroom flat, privately rented", "a three-bedroom flat, privately rented")], "Band C")),

# ------------------------------------------------------------------ ho16
# why: host asks to cancel and rebook by bank transfer for a discount -> off-platform payment.
# Twin: a parking charge that is disclosed in the listing's Additional charges -> none of these.
C("ho16", "Which Burrowly host standard does this message break?",
"""
Burrowly — Host Standards (messaging review)
H1 Off-platform payment: asking a guest to pay for a stay, or any part of the nightly price, outside Burrowly.
H2 Undisclosed fees: charging any fee that is not shown in the listing's price or "Additional charges" section.
H3 Discrimination: refusing or treating guests differently for a protected characteristic, outside the permitted exceptions.
H4 Recording devices: undisclosed cameras or any camera in a bedroom, bathroom or sleeping space.
Record the lowest-numbered standard that applies.

Message thread #MT-66012 (flagged by keyword filter)
Host (Cedric L.) to guest, 2 days after the guest booked 5 nights:
"Hi Hanna, looking forward to hosting you! Quick one — Burrowly's fees are crazy. If you cancel and send me £410 by bank transfer instead, I'll knock 10% off and you can have the same dates. My details are below. Also, there's a private parking space at the back if you need it."
Listing: "Dockside studio" — Additional charges section lists "Cleaning £30"; no parking charge listed.
""",
[("H1 off-platform payment", "asking for payment for the stay outside Burrowly."),
 ("H2 undisclosed fees", "charging a fee not shown in the listing."),
 ("H3 discrimination", "treating guests differently for a protected characteristic."),
 ("H4 recording devices", "undisclosed cameras, or cameras in private or sleeping spaces."),
 ("none of these", "the message breaks no host standard.")],
"H1 off-platform payment", 2,
twin=T([("If you cancel and send me £410 by bank transfer instead, I'll knock 10% off and you can have the same dates. My details are below. Also, there's",
         "Check-in is from 3pm and the key safe code will come through the app on the day. There's")], "none of these")),

# ------------------------------------------------------------------ ho17
# why: any camera is barred from rooms listed as sleeping space; the living room holds the listed sofa bed
# -> breach even though disclosed (1). Twin: camera moved to the entrance hallway, disclosed -> 0.
Y("ho17", "Does the camera at listing BW-72201 breach Burrowly's recording-device rule?",
"""
Burrowly — Recording Devices Rule
Indoor security cameras are allowed only in entryways and hallways, and only when disclosed in the listing's "Safety & property" section. No camera, disclosed or not, may be placed in a bedroom, a bathroom, or any room listed as a sleeping space. Noise-level monitors that do not record audio are allowed anywhere if disclosed.

Guest report #GR-40917
"There's a camera watching the living room of this flat. We had the kids sleeping on the sofa bed in there. Is this allowed?"
Listing BW-72201 — "Harbourview two-bed"
Sleeping arrangements: Bedroom 1 — double bed; Bedroom 2 — twin beds; Living room — sofa bed (sleeps 2).
Safety & property: "Security camera mounted in the living room above the TV (records video only). Noise monitor in the hallway."
Host response: "It's clearly disclosed and it only records video, never audio."
""",
[("Recording-device breach", "an undisclosed indoor camera, or any camera in a bedroom, bathroom or listed sleeping space."),
 ("Permitted device", "a disclosed camera in an entryway or hallway, or a disclosed non-recording noise monitor.")],
1, 2,
twin=T([("Security camera mounted in the living room above the TV", "Security camera mounted in the entrance hallway above the front door"),
        ("There's a camera watching the living room of this flat. We had the kids sleeping on the sofa bed in there.",
         "There's a camera by the front door of this flat. We had the kids sleeping on the sofa bed in the living room.")], 0)),
# ------------------------------------------------------------------ ho18
# why: photos/description misstate the view and bedroom count -> inaccurate listing; alarms present,
# no fees or cameras involved. Twin: listing accurate but gas boiler with no CO alarm -> safety equipment.
C("ho18", "Which Burrowly Listing Standard applies to guest report GR-51177?",
"""
Burrowly — guest report GR-51177, received 13 September 2026
Listing BW-60233 — "Sea-view 2-bed apartment, Pellow Harbour" — entire home, sleeps 4
Guest (Ruth Adair): "We arrived to find the flat faces the supermarket car park — you can't see the sea from any window. The listing photo of the sea view seems to be from the roof terrace, which we can't get into. It also says two bedrooms, but there's one bedroom and a sofa bed in the lounge. Otherwise it's clean and the host has been polite."
Host (Callum N.): "The sea view photo is from the building, so I don't see the problem."
Inspection by local partner, 14 September: one bedroom plus sofa bed confirmed; no sea view from inside the flat; roof terrace locked, residents only. Smoke alarm and carbon monoxide alarm fitted and working; gas boiler serviced May 2026. No cameras. No charges beyond the listing price were requested. Registration number shown and valid.
""",
[("inaccurate listing", "photos, description or room counts that misrepresent the property."),
 ("undisclosed fees", "charges not shown in the listing price or Additional charges."),
 ("discrimination", "refusing or treating guests differently for a protected characteristic."),
 ("recording devices", "undisclosed cameras, or cameras in private or sleeping spaces."),
 ("off-platform payment", "asking guests to pay for the stay outside Burrowly."),
 ("unlicensed listing", "a listing without a required registration number."),
 ("safety equipment missing", "no working smoke alarm, or no working carbon monoxide alarm where there is a gas appliance."),
 ("cleanliness", "the property was not cleaned to Burrowly's standard before arrival."),
 ("host conduct", "rude, threatening or inappropriate behaviour by the host."),
 ("none of these", "no listing standard is breached.")],
"inaccurate listing", 2,
twin=T([("We arrived to find the flat faces the supermarket car park — you can't see the sea from any window. The listing photo of the sea view seems to be from the roof terrace, which we can't get into. It also says two bedrooms, but there's one bedroom and a sofa bed in the lounge. Otherwise it's clean and the host has been polite.\"\nHost (Callum N.): \"The sea view photo is from the building, so I don't see the problem.\"\nInspection by local partner, 14 September: one bedroom plus sofa bed confirmed; no sea view from inside the flat; roof terrace locked, residents only. Smoke alarm and carbon monoxide alarm fitted and working;",
         "The flat is lovely and exactly like the photos, but there's a gas boiler in the kitchen and I couldn't find a carbon monoxide alarm anywhere. It's clean and the host has been polite.\"\nHost (Callum N.): \"The old CO alarm died and I haven't replaced it yet.\"\nInspection by local partner, 14 September: two bedrooms and sea view confirmed as listed. Smoke alarm fitted and working; no carbon monoxide alarm fitted;")],
       "safety equipment missing")),
]
