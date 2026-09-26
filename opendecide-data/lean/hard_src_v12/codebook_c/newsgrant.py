"""codebook_c / newsroom desk routing (Harbourline Courier) and foundation grant categories
(Fennwick Community Foundation). Both organisations, and everyone named, are invented."""
from _lib import C, Y, T

NW = {
    "Metro": "Local government, neighbourhoods, local transit and development inside the metro area, including city council votes on any subject.",
    "Statehouse": "The state legislature, the governor and state agencies while a bill or action is being proposed, debated or passed; once a law is in effect, stories about its impact go to the subject desk.",
    "Courts and public safety": "Crime, fires, crashes, policing, and any story whose news is a court proceeding (a filed lawsuit, criminal charges, a trial, a verdict), whatever its subject.",
    "Business": "Companies (including hospital systems and universities as employers), markets, jobs, layoffs and the economy.",
    "Education": "Schools, school boards, universities as places of learning, students and teachers.",
    "Health": "Medicine, patient care, public health, health research, and the impact of health laws on patients and providers.",
    "Climate and environment": "Weather extremes, climate, pollution, wildlife and conservation.",
    "Sports": "Teams, games, athletes and coaching news.",
    "Arts and culture": "Music, theatre, film, museums, books and food culture.",
    "Obituaries": "News of a death where the person's life is the story; a death caused by crime, fire or a crash goes to the desk covering that event.",
    "Opinion": "Op-eds, letters to the editor and other submissions arguing a point of view.",
    "Corrections": "Reader reports of a factual error in something the Courier published.",
    "Reader services": "Subscriptions, delivery, logins and the paywall.",
    "none of these": "The item fits none of the other listed desks.",
}

FN = {
    "Early childhood": "Programs whose primary outcome is development, care or school readiness of children from birth to age 5, including parent-child programs.",
    "Youth development": "Out-of-school programs for ages 6 to 18: mentoring, after-school, summer and youth sports programs.",
    "Workforce and adult education": "Job training, apprenticeships, adult literacy, English classes for adults and high-school equivalency for people 18 and over.",
    "Food security": "Food banks, pantries, meal programs and growing or distributing food for people who lack it.",
    "Housing stability": "Eviction prevention, rental assistance, shelters and housing case management.",
    "Health access": "Clinics, insurance enrolment help, mental-health counselling and health screenings, for any age group.",
    "Arts and culture": "Performances, exhibitions, public art and arts education delivered by an eligible organisation.",
    "Environment and parks": "Habitat restoration, native planting, tree canopy, clean water and park stewardship.",
    "Civic engagement": "Voter registration, civic education, community organising and participation in local government, excluding lobbying for specific legislation.",
    "Organizational capacity": "Funds the applicant organisation itself (general operating support, staff training, technology, fundraising or strategic planning) rather than program delivery.",
    "Capital projects": "Any request where more than 50% of the requested amount is for buying land or buildings, construction or renovation, whatever the program.",
    "none of these": "Ineligible or uncategorised requests, including grants to individuals, religious worship, lobbying for specific legislation and projects outside Fennwick County.",
}


def nw(*names):
    return [(n, NW[n]) for n in names]


def fn(*names):
    return [(n, FN[n]) for n in names]


NRULE = "Courier routing guide: route every pitch, tip or reader email by what the news (or request) is, not by who is in it."
FRULE = ("Fennwick grants manual, section 2: assign one category per request, by the primary outcome the grant money buys, "
         "not by the population served or the type of applicant. Section 2.4 (the Capital test) is applied first.")

ITEMS = [
# ------------------------------------------------------------------ nw01
# why: the news is a filed lawsuit -> Courts and public safety, whatever the subject (schools).
#      twin: parents rally before a board vote, nothing filed -> Education.
C("nw01", "Which Courier desk should this tip be routed to?",
f"""
{NRULE}

Tip form — received 08:12 via tips@harbourlinecourier
From: Ottoline Brandvold (parent, Keel Street Elementary PTA)

"Keel Street Elementary is set to close in June under the district's consolidation plan, and the kids would be bused 40 minutes to Marsh Road. This morning fourteen families, with help from the Coastal Families Legal Project, filed a lawsuit in Harbourline County Superior Court asking a judge to block the closure, arguing the district skipped the required public hearing. I have a copy of the complaint and can put you in touch with the lead parent. Our PTA president will speak on the record."
""",
nw("Courts and public safety", "Education", "Metro", "Statehouse", "Opinion",
   "Business", "Corrections", "none of these"),
"Courts and public safety", 2,
twin=T([("This morning fourteen families, with help from the Coastal Families Legal Project, filed a lawsuit in Harbourline County Superior Court asking a judge to block the closure, arguing the district skipped the required public hearing. I have a copy of the complaint and can put you in touch with the lead parent.",
         "Tonight about two hundred families plan to rally outside the district office before Thursday's school board vote on the closure, arguing the district skipped the required public hearing. I have a copy of the petition and can put you in touch with the lead parent.")],
       "Education")),

# ------------------------------------------------------------------ nw02
# why: a death in a highway crash -> the crash desk (Courts and public safety), not Obituaries, per the Obituaries rule.
#      twin: died at home after illness; her life is the story -> Obituaries.
C("nw02", "Route this item to the correct Courier desk.",
f"""
{NRULE}

Newsroom slack — #tips
From: night editor Dmitri Salonen, 23:48

"Heads up: Rosalind Achebe-Farr, 71, who ran Marisco's on the waterfront for thirty years and won the Coastal Chef award twice, died tonight when her car was struck by a wrong-way driver on Route 9 near the Pell exit. State patrol says the other driver has been arrested on suspicion of driving under the influence. Two others were taken to Mercy General. Her family has asked for privacy tonight but her son says he'll talk tomorrow about her life and the restaurant."
""",
list(NW.items()),
"Courts and public safety", 3,
twin=T([("died tonight when her car was struck by a wrong-way driver on Route 9 near the Pell exit. State patrol says the other driver has been arrested on suspicion of driving under the influence. Two others were taken to Mercy General.",
         "died tonight at home, surrounded by family, after a long illness. She trained a generation of the city's cooks and fed the waterfront crews for free during the 1998 strike. Nobody else is involved.")],
       "Obituaries")),

# ------------------------------------------------------------------ nw03
# why: a reader reports a factual error (wrong figure) in a published story -> Corrections, not Metro.
#      twin: the reader submits an argued essay for publication -> Opinion.
C("nw03", "Which desk should handle this reader email?",
f"""
{NRULE}

To: readers@harbourlinecourier
From: Cassius Holloway-Nair
Subject: Fenner Street bridge story (Tuesday)
Received: Wednesday 09:14. Reader location: Fenner Heights. Story slug: BRIDGE-0611, bylined Aurelio Pike.

"Your Tuesday story on the Fenner Street bridge reopening says the repair cost $40 million. The city's own project page and the council minutes from 3 March both say $4.0 million. Somebody added a zero. That's a big difference when people are already angry about city spending. I've pasted links to both documents below."
""",
nw("Corrections", "Metro", "Opinion", "Reader services", "Statehouse",
   "Business", "none of these"),
"Corrections", 2,
twin=T([("Your Tuesday story on the Fenner Street bridge reopening says the repair cost $40 million. The city's own project page and the council minutes from 3 March both say $4.0 million. Somebody added a zero. That's a big difference when people are already angry about city spending. I've pasted links to both documents below.",
         "Your Tuesday story on the Fenner Street bridge reopening got the facts right, including the $4.0 million cost. But I think the city should never have repaired it at all, and I've written a 650-word piece arguing it should be turned into a footbridge. I'd like you to publish it; it's pasted below.")],
       "Opinion")),

# ------------------------------------------------------------------ nw04
# why: a city council vote (on stadium bonds) -> Metro by definition, not Sports or Business.
#      twin: the team names a new head coach -> Sports.
C("nw04", "Using the routing guide, which desk gets this pitch?",
f"""
{NRULE}

Pitch from reporter Ingrid Salazar-Mott to the assigning editors:

"The Harbourline Gulls want a new $310 million ballpark on the Pier 40 site. Tonight the city council votes on whether to issue $120 million in bonds backed by a new hotel-room charge to pay for part of it. I've got the vote count (it looks like 5-4), the team president's letter to council, and a union leader who says the construction would mean 1,800 jobs. I'd like to file tonight after the vote."
""",
nw("Metro", "Sports", "Business", "Statehouse", "Courts and public safety",
   "Opinion", "none of these"),
"Metro", 2,
twin=T([("Tonight the city council votes on whether to issue $120 million in bonds backed by a new hotel-room charge to pay for part of it. I've got the vote count (it looks like 5-4), the team president's letter to council, and a union leader who says the construction would mean 1,800 jobs. I'd like to file tonight after the vote.",
         "But tonight's news is that the team is naming Teodora Vance, the Ridgeport pitching coach, as its new manager at a press conference at the old ballpark. I've got her record, the team president's statement and two players on the record. I'd like to file tonight after the press conference.")],
       "Sports")),

# ------------------------------------------------------------------ nw05
# why: a bill passing the legislature -> Statehouse (hospitals are the subject).
#      twin: one year after the law took effect, its impact on patients -> Health.
C("nw05", "Which Courier desk should this story go to?",
f"""
{NRULE}

Story budget line — submitted by Jonah Albrecht

"HOSPITAL PRICES: The state senate passed the Hospital Price Transparency Act 22-17 this afternoon, sending it to the governor, who has said she will sign it. The bill would require every hospital to post cash prices for 300 common procedures and bar collections against patients if a hospital hasn't complied. I have floor quotes from both sides and the hospital association's statement. 700 words, ready by 6 p.m."
""",
nw("Statehouse", "Health", "Business", "Courts and public safety", "Metro",
   "Opinion", "none of these"),
"Statehouse", 2,
twin=T([("The state senate passed the Hospital Price Transparency Act 22-17 this afternoon, sending it to the governor, who has said she will sign it. The bill would require every hospital to post cash prices for 300 common procedures and bar collections against patients if a hospital hasn't complied. I have floor quotes from both sides and the hospital association's statement.",
         "One year after the Hospital Price Transparency Act took effect, a Courier review of 41 hospitals finds that patients now pay 18% less on average for MRIs and knee replacements, while nine hospitals still post no prices. I have patient interviews and the hospital association's statement.")],
       "Health")),

# ------------------------------------------------------------------ nw06
# why: a hospital system cutting 400 administrative jobs -> a company as employer / layoffs -> Business, not Health.
C("nw06", "Identify the Courier desk for this tip.",
f"""
{NRULE}

Tip — voicemail transcribed by the news assistant

"Hi, this is a nurse at Kestrel Health, the big hospital system. I don't want my name used. Management told the billing and scheduling departments this morning that 400 administrative jobs across all four Kestrel hospitals will be cut by August and moved to an outsourcing company. They said no nurses or doctors are affected and patient care won't change. There's a memo; I can send a photo of it."
""",
nw("Business", "Health", "Metro", "Courts and public safety", "Statehouse",
   "Opinion", "none of these"),
"Business", 2),

# ------------------------------------------------------------------ nw07
# why: a subscriber locked out by the paywall -> Reader services (the story topic is irrelevant).
C("nw07", "Which desk should receive this message?",
f"""
{NRULE}

To: newsroom@harbourlinecourier
From: Ezekiel Moncrieff
Subject: Can't read your wildfire coverage

"I've been a digital subscriber since 2019 and I pay every month (last charge 1 June, $12.99). Since last night, every time I click on your wildfire stories or anything else, I get the 'You've reached your free article limit' screen, even though I'm logged in. I've cleared cookies and tried my phone. Your climate reporting is the reason I subscribe, so please fix this."
""",
nw("Reader services", "Climate and environment", "Corrections", "Opinion", "Business",
   "none of these"),
"Reader services", 2),

# ------------------------------------------------------------------ gr01
# why: Capital test first: construction $180,000 of $240,000 = 75% > 50% -> Capital projects (a food bank's program is the setting).
#      twin: construction $90,000 of $240,000 = 37.5% -> not capital; primary outcome is food distribution -> Food security.
C("gr01", "Which Fennwick grant category should this request be assigned?",
f"""
{FRULE}

Application FCF-27-0144 — Tri-Valley Food Bank
Request: $240,000 over 12 months

Project summary: Tri-Valley distributes 3.1 million pounds of food a year to 64 pantries. Our warehouse cannot store enough frozen protein, so we turn down donated meat every month.

Budget:
- Construction of a walk-in freezer addition to the warehouse: $180,000
- Refrigerated truck lease (12 months): $36,000
- Driver wages: $24,000
Total: $240,000
""",
fn("Capital projects", "Food security", "Organizational capacity", "Health access", "Housing stability",
   "Environment and parks", "none of these"),
"Capital projects", 3,
twin=T([("- Construction of a walk-in freezer addition to the warehouse: $180,000\n- Refrigerated truck lease (12 months): $36,000\n- Driver wages: $24,000",
         "- Construction of a walk-in freezer addition to the warehouse: $90,000\n- Refrigerated truck lease (12 months): $66,000\n- Driver wages and food purchases for partner pantries: $84,000")],
       "Food security")),

# ------------------------------------------------------------------ gr02
# why: English classes for adults at a library -> Workforce and adult education (the library/culture setting misleads).
#      twin: parent-toddler story time for under-5s -> Early childhood.
C("gr02", "Assign the Fennwick grant category.",
f"""
{FRULE}

Application FCF-27-0171 — Friends of the Ashby Branch Library
Request: $38,000

Project summary: Ashby's newest residents, many from Central America and Afghanistan, ask our staff every week for help reading forms, leases and job postings. This grant pays two certified instructors to run evening English conversation and reading classes for adults, three nights a week in the library's community room, with free childcare during class. We expect 90 adult learners. No construction or equipment is requested; the Library already provides the room and books.
""",
fn("Workforce and adult education", "Early childhood", "Arts and culture", "Civic engagement", "Youth development",
   "Organizational capacity", "none of these"),
"Workforce and adult education", 2,
twin=T([("This grant pays two certified instructors to run evening English conversation and reading classes for adults, three nights a week in the library's community room, with free childcare during class. We expect 90 adult learners.",
         "This grant pays two certified early-literacy specialists to run bilingual story, song and play sessions for children aged 0 to 4 with a parent, three mornings a week in the library's community room. We expect 90 families.")],
       "Early childhood")),

# ------------------------------------------------------------------ gr03
# why: an after-school soccer program for ages 12-17 -> Youth development; nutrition talks are an add-on, not the outcome.
C("gr03", "Which category from the grants manual applies to this request?",
f"""
{FRULE}

Application FCF-27-0203 — Eastgate Futbol Club (registered nonprofit)
Request: $52,000

Project summary: Eastgate Futbol Club runs free after-school soccer practices and weekend matches for 180 young people aged 12 to 17 in the Eastgate neighbourhood. This grant pays coaches' stipends, field rental and uniforms for the school year. Once a month a volunteer dietitian from the county health department gives a 20-minute talk on eating well before training; no health services are provided. Our outcome measures are attendance, mentoring hours and school-year retention in the program.
""",
list(FN.items()),
"Youth development", 2),

# ------------------------------------------------------------------ gr04
# why: a new donor database and a development director fund the organisation itself -> Organizational capacity (a shelter's mission misleads).
#      twin: two case managers paying rent arrears for families -> Housing stability.
C("gr04", "Which grant category should the program officer record?",
f"""
{FRULE}

Application FCF-27-0219 — Harbor Light Family Shelter
Request: $95,000 over 18 months

Project summary: Harbor Light houses 40 families a night and has a waiting list of 60. Our income depends on a single government contract that ends in 2029. This grant would pay for a donor management database and 18 months of salary for our first development director, who will build an individual-giving program so the shelter can survive the contract's end. No shelter beds, rent payments or client services are funded by this request.
""",
fn("Organizational capacity", "Housing stability", "Capital projects", "Early childhood", "Food security",
   "Health access", "Civic engagement", "none of these"),
"Organizational capacity", 2,
twin=T([("This grant would pay for a donor management database and 18 months of salary for our first development director, who will build an individual-giving program so the shelter can survive the contract's end. No shelter beds, rent payments or client services are funded by this request.",
         "This grant would pay 18 months of salary for two case managers who will pay overdue rent for families about to be evicted and negotiate with their landlords, so the families never need a shelter bed. No technology or fundraising staff are funded by this request.")],
       "Housing stability")),

# ------------------------------------------------------------------ gr05
# why: voter registration and civic education for high-school seniors -> Civic engagement (not Youth development).
#      twin: lobbying the legislature to pass one specific bill -> excluded -> none of these.
C("gr05", "Code this request with the Fennwick grant categories.",
f"""
{FRULE}

Application FCF-27-0236 — Fennwick Youth Vote Project
Request: $27,500

Project summary: Only 31% of Fennwick County 18-year-olds voted in the last county election. The Project will visit all nine public high schools in the spring to pre-register seniors to vote, run a 45-minute class on how county government and the ballot work, and send reminders before the November election. Outcome measures: registrations completed and turnout among registrants.
""",
fn("Civic engagement", "Youth development", "Workforce and adult education", "Arts and culture", "Organizational capacity",
   "none of these"),
"Civic engagement", 2,
twin=T([("The Project will visit all nine public high schools in the spring to pre-register seniors to vote, run a 45-minute class on how county government and the ballot work, and send reminders before the November election. Outcome measures: registrations completed and turnout among registrants.",
         "The Project will bring high-school seniors to the state capitol in the spring to lobby legislators to pass Senate Bill 88, which would lower the voting age in county elections to 16, and will run phone banks urging legislators to vote yes. Outcome measure: passage of SB 88.")],
       "none of these")),

# ------------------------------------------------------------------ gr06
# why: garden produce where 90% of the harvest goes to the pantry -> primary outcome is food for people who lack it -> Food security.
#      twin: native prairie restoration and invasive removal -> Environment and parks.
C("gr06", "What is the correct grant category for this application?",
f"""
{FRULE}

Application FCF-27-0258 — Millbrook Neighbours Association
Request: $18,000

Project summary: The Association has a five-year licence to use a vacant county lot on Tanner Street. With this grant we will build raised beds, install drip irrigation (under $4,000 of the request), and pay a part-time garden coordinator. Volunteers will grow vegetables through the season, and 90% of the harvest will be delivered each week to the Millbrook Community Pantry, which serves 300 households. Neighbours will also enjoy the green space.
""",
fn("Food security", "Environment and parks", "Capital projects", "Civic engagement", "Health access",
   "Youth development", "none of these"),
"Food security", 2,
twin=T([("With this grant we will build raised beds, install drip irrigation (under $4,000 of the request), and pay a part-time garden coordinator. Volunteers will grow vegetables through the season, and 90% of the harvest will be delivered each week to the Millbrook Community Pantry, which serves 300 households.",
         "With this grant we will remove invasive buckthorn, plant 40 species of native prairie grasses and wildflowers (under $4,000 of the request), and pay a part-time site steward. Volunteers will monitor pollinators through the season, and nothing grown on the lot will be harvested.")],
       "Environment and parks")),

# ------------------------------------------------------------------ gr07
# why: the applicant is an individual painter, and grants to individuals are ineligible -> none of these (not Arts and culture).
#      twin: applicant is a registered nonprofit arts collective -> Arts and culture.
C("gr07", "Which Fennwick category applies? Choose none of these if the request is ineligible.",
f"""
{FRULE}

Application FCF-27-0277
Applicant: Solveig Arendt, painter (applying in her own name; no fiscal sponsor)
Request: $12,000

Project summary: I will paint a 90-foot mural of the Millrace River's history on the retaining wall at Carver Park, with the city's written permission. Twenty local teenagers will help paint under my supervision over the summer. The budget covers paint, scaffolding rental and my fee for four months of work. The finished mural will be dedicated at the Carver Park summer festival.
""",
fn("Arts and culture", "Youth development", "Environment and parks", "Capital projects", "Civic engagement",
   "none of these"),
"none of these", 3,
twin=T([("Applicant: Solveig Arendt, painter (applying in her own name; no fiscal sponsor)",
         "Applicant: Millrace Mural Collective, a registered nonprofit (lead artist Solveig Arendt)"),
        ("I will paint a 90-foot mural", "We will paint a 90-foot mural"),
        ("under my supervision", "under our lead artist's supervision"),
        ("and my fee for four months of work", "and the lead artist's fee for four months of work")],
       "Arts and culture")),

# ------------------------------------------------------------------ gr08
# why: counselling sessions for teens = mental-health counselling -> Health access "for any age group" (not Youth development).
C("gr08", "Assign one grant category to this request.",
f"""
{FRULE}

Application FCF-27-0290 — Bayview Counseling Collaborative
Request: $64,000

Project summary: Bayview's licensed therapists will provide free weekly one-on-one counselling sessions for 120 students aged 13 to 18 at Northshore and Fennwick Central high schools, during the school day, in private rooms the schools provide. Students are referred by school counsellors for anxiety, depression or grief. Outcomes are measured with standard symptom scales at intake and after 12 sessions.
""",
fn("Health access", "Youth development", "Early childhood", "Workforce and adult education", "Organizational capacity",
   "Civic engagement", "none of these"),
"Health access", 2),

# ------------------------------------------------------------------ gr09
# why: renovation $52,000 of $110,000 = 47.3% -> not more than 50% -> not Capital (no).
#      twin: renovation $62,000 of $120,000 = 51.7% -> Capital (yes).
Y("gr09", "Does this request meet the Capital projects test in section 2.4?",
f"""
{FRULE}

Application FCF-27-0312 — Northgate Adult Learning Center
Request: renovation of two classrooms plus program costs

Budget:
- Renovation of two classrooms (walls, wiring, accessible entrance): $52,000
- Instructor salaries for GED classes (12 months): $38,000
- Laptops and course licences: $20,000
Total requested: $110,000

Narrative excerpt: "The renovated rooms will let us double evening GED classes from 40 to 80 learners."
""",
[("Capital projects", FN["Capital projects"]),
 ("Share test", "capital share = (land + buildings + construction + renovation) / total requested; it must be more than 50%.")],
0, 3,
twin=T([("- Renovation of two classrooms (walls, wiring, accessible entrance): $52,000",
         "- Renovation of two classrooms (walls, wiring, accessible entrance): $62,000"),
        ("Total requested: $110,000", "Total requested: $120,000")],
       1)),

# ------------------------------------------------------------------ nw09
# why: an administrative health-inspection fine, no charges or court case -> not Courts and public safety (no).
#      twin: the owner is charged with a felony and arraigned -> criminal charges -> yes.
Y("nw09", "Should this tip go to the Courts and public safety desk?",
f"""
{NRULE}

Tip form — received 14:30
From: anonymous (former employee)

"The Gilded Anchor on Quay Street was fined $4,500 by the county health department this week after inspectors found mice droppings in the kitchen and a walk-in cooler at 52 degrees. It's the third inspection they've failed this year. The inspection reports are public on the county website. The owner, Lysander Pratt, told staff to keep quiet about it. The restaurant is still open."
""",
[("Courts and public safety", NW["Courts and public safety"]),
 ("Court proceeding", "a filed lawsuit, criminal charges, a trial or a verdict; an administrative fine from an inspector is not one.")],
0, 2,
twin=T([("The Gilded Anchor on Quay Street was fined $4,500 by the county health department this week after inspectors found mice droppings in the kitchen and a walk-in cooler at 52 degrees. It's the third inspection they've failed this year. The inspection reports are public on the county website.",
         "The owner of the Gilded Anchor on Quay Street was charged this week with felony tax evasion for hiding $600,000 in cash sales, and he was arraigned in county court on Monday. The charging documents are public on the court website.")],
       1)),

# ------------------------------------------------------------------ nw10
# why: the reader alleges a misattributed quote = factual error in a published story -> Corrections -> "outside Corrections?" no.
#      twin: the reader only disagrees with the editorial's argument, no factual error -> outside Corrections -> yes.
Y("nw10", "Is this reader email outside the Corrections desk's remit?",
f"""
{NRULE}

To: readers@harbourlinecourier
From: Philippa Oduya-Strand
Subject: Sunday editorial on the transit levy
Received: Monday 07:52. Reader account: print and digital subscriber since 2011. Earlier emails on file: 2, both about delivery.

"Sunday's editorial on the transit levy quotes Councilor Hemsworth saying 'buses are a luxury this city can't afford.' Hemsworth never said that. It was Councilor Brisco, at the 12 May meeting; the video is on the city website at 1:14:20. Hemsworth voted for the levy. Please look into this."
""",
[("Corrections", NW["Corrections"]),
 ("Opinion", NW["Opinion"])],
0, 2, role="neg",
twin=T([("quotes Councilor Hemsworth saying 'buses are a luxury this city can't afford.' Hemsworth never said that. It was Councilor Brisco, at the 12 May meeting; the video is on the city website at 1:14:20. Hemsworth voted for the levy. Please look into this.",
         "argues that the levy is too expensive for working families. Every fact in it checks out, but I think the argument is wrong: the levy costs less than one bus pass a year and would add night service. Please consider this letter for publication.")],
       1)),
]
