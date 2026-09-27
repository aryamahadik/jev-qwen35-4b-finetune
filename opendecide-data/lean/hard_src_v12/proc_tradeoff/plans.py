"""proc_tradeoff / plans, tiers and tariffs (telecom, cloud, energy, SaaS,
leases, travel classes, storage tiers). All organisations, people and places
are invented."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ pl01
# why: 25 lines, all on one plan type; each line must cover the 90th-percentile usage
# (14 GB); 6 travellers need EU roaming on the plan (day passes not reimbursed).
# Basic 10 GB fails. Plus 20 GB: 25*24 = 600 + roaming add-on on 6 lines 6*5 = 30 ->
# 630. Traveller (15 GB, roaming incl.) 25*26 = 650. -> Plus + add-on.
# Twin: add-on must be enabled on every line -> 25*(24+5) = 725 > 650 -> Traveller.
C("pl01", "Which mobile plan set-up should be ordered for the sales team?",
"""
To: Procurement (telecoms)
From: Colm Ferreira, Sales Operations, Tiller & Hart
Re: Mobile plan renewal — 25 lines

Requirements (from the Mobile Device Standard, MDS-2)
- Every line must have a monthly data allowance at least equal to the team's 90th-percentile monthly usage over the last 12 months. For our team that figure is 14 GB (average usage is 8 GB).
- Staff who travel to the EU for work must have EU roaming on their plan. Personal roaming day passes are not reimbursed.
- The carrier requires all lines on one account to be on the same base plan.
- Choose the lowest total monthly cost that meets these rules.

Carrier offer (Norvane Mobile, business tariffs, per line per month)
- Basic: 10 GB, no roaming, $18.
- Plus: 20 GB, no roaming, $24. EU roaming add-on: $5 per line per month, charged only on lines where it is enabled.
- Traveller: 15 GB, EU roaming included, $26.

Six of the 25 staff travel to the EU for work each quarter.
Handset refresh is handled separately under the device lease and is not part of this decision.
""",
[("basic_plan", "Average usage of 8 GB fits comfortably inside Basic's 10 GB, and Basic is by far the cheapest."),
 ("plus_no_roaming", "Plus alone costs $600 and covers the data need; travellers can buy day passes when abroad."),
 ("plus_with_roaming_addon", "Plus covers the 14 GB need, and adding roaming for only the six travellers makes it cheapest at $630."),
 ("traveller_plan", "Traveller is the cheapest compliant set-up once roaming is costed the way the add-on terms require.")],
"plus_with_roaming_addon", 2,
twin=T([("charged only on lines where it is enabled", "which must be enabled on every line on the account")], "traveller_plan")),

# ------------------------------------------------------------------ pl02
# why: commitments > 12 months need CFO approval (none) -> 3-yr out. Usage 24/7 for
# 12 months = 8,760 h * $0.40 = $3,504 on-demand vs $2,300 one-year reservation ->
# reserve 1 yr (12-month commitment needs no approval).
# Twin: 6 months then off -> 4,380 h * 0.40 = $1,752 < $2,300 -> on-demand.
C("pl02", "Which pricing option should the platform team choose for the new database server?",
"""
Cloud Cost Review — ticket FIN-OPS-311
Workload: analytics database for the Lorne Valley water-quality project. It runs 24/7 for 12 months from 1 October 2026.

Pricing options (one db.x4 instance)
- On-demand: $0.40 per hour, no commitment.
- One-year reservation: $2,300 paid upfront, no hourly charge, 12-month commitment.
- Three-year reservation: $4,200 paid upfront (about $1,400 a year), 36-month commitment.

Cloud Financial Policy
CF-1. Choose the option with the lowest total cost for the planned usage.
CF-2. Any commitment longer than 12 months requires written approval from the CFO before purchase. Commitments of 12 months or less can be approved by the budget holder.
CF-3. Reserved capacity cannot be resold once bought.

Status: the budget holder (Anouk Brevik) has approved spend up to $4,500. No CFO approval has been requested.
Comment from the project engineer: "Three-year is obviously the best deal per year. Let's just buy it."
""",
[("on_demand", "For the planned usage, on-demand costs less than the one-year reservation and needs no commitment."),
 ("reserve_1yr", "For twelve months of round-the-clock use, the one-year reservation costs less than on-demand and needs no CFO approval."),
 ("reserve_3yr", "At about $1,400 a year the three-year reservation has the lowest annual cost, and the budget holder's approval covers it.")],
"reserve_1yr", 2,
twin=T([("It runs 24/7 for 12 months from 1 October 2026.", "It runs 24/7 for 6 months from 1 October 2026 and is then switched off.")], "on_demand")),

# ------------------------------------------------------------------ pl03
# why: needs >= 500 Mbps, SLA >= 99.9%, static IP. FibreLink 500 Mbps (meets >=),
# 99.9%, static add-on $15 -> 210+15 = 225. Corvid 1 Gbps, 99.95%, static incl. $240.
# Harbour 99.5% fails SLA. Cheapest compliant = FibreLink.
# Twin: static add-on $35 -> 245 > 240 -> Corvid.
C("pl03", "Which broadband contract should the office take?",
"""
Brackenridge Surveyors — IT Connectivity Standard (Office sites)
C1. Minimum download bandwidth: 500 Mbps.
C2. Contracted availability (SLA) of at least 99.9%.
C3. A static public IP address is required for the site VPN.
C4. Choose the lowest total monthly cost meeting C1-C3, including any add-ons needed.

Quotes for the new Tanfield Road office (36-month term)
| Provider & plan | Bandwidth | SLA | Static IP | Monthly price |
| FibreLink Business 500 | 500 Mbps | 99.9% | add-on, $15/month | $210 |
| Corvid Net Pro 1000 | 1,000 Mbps | 99.95% | included | $240 |
| Harbour Broadband 800 | 800 Mbps | 99.5% | included | $180 |

Harbour's sales rep wrote: "Our 99.5% is within the usual half-percent tolerance, so it counts as 99.9% for your standard."
The office has 22 staff. Guest Wi-Fi will run on a separate low-cost line already in place.
""",
[("fibrelink_500", "Including its static IP add-on, FibreLink at $225 is the cheapest plan that meets all three requirements."),
 ("corvid_pro_1000", "Once FibreLink's static IP add-on is included, Corvid is the cheapest plan meeting the bandwidth, SLA and static IP rules."),
 ("harbour_800", "Harbour is cheapest and its 99.5% SLA falls within the tolerance the rep described.")],
"fibrelink_500", 1,
twin=T([("add-on, $15/month", "add-on, $35/month")], "corvid_pro_1000")),

# ------------------------------------------------------------------ pl04
# why: 400,000 kWh. Fixed 0.21*400,000 = 84,000 + 1,200 = 85,200. Variable 0.20*400k =
# 80,000 + 2,400 = 82,400 but treasury rule: sites > 300,000 kWh must be fixed ->
# excluded. Green fixed 0.225*400k = 90,000 + 1,200 = 91,200. Renewable rule applies
# to contracts starting on/after 1 Jan 2027; this starts 1 Nov 2026 -> not required.
# Cheapest allowed = Fixed Standard. Twin: start 1 Feb 2027 -> renewable required ->
# Green Fixed (only renewable fixed tariff).
C("pl04", "Which electricity tariff should be signed for the Kelda Road warehouse?",
"""
Energy procurement note — Kelda Road warehouse
Annual consumption (last 12 months): 400,000 kWh. New contract start: 1 November 2026, 24-month term.

Treasury Rule 4: sites consuming more than 300,000 kWh a year must be on fixed-price tariffs.
Sustainability Policy, amendment S-3: electricity contracts starting on or after 1 January 2027 must be 100% renewable supply.
Procurement Rule 9: among tariffs allowed by the rules above, choose the lowest expected annual cost (unit rate x annual consumption + annual standing charge).

Offers from Harrowmere Energy
| Tariff | Type | Unit rate | Standing charge (per year) | Supply |
| Fixed Standard | fixed | $0.210/kWh | $1,200 | grid mix |
| Variable Tracker | variable | $0.200/kWh (expected) | $2,400 | grid mix |
| Green Fixed | fixed | $0.225/kWh | $1,200 | 100% renewable |

Warehouse manager's email: "The sustainability team keeps telling us we're supposed to be green from now on. Surely that means Green Fixed?"
The site's solar panels generated 38,000 kWh last year; this is already netted out of the consumption figure.
""",
[("fixed_standard", "The renewable rule does not yet apply to this contract, and Fixed Standard is the cheapest tariff the treasury rule allows."),
 ("variable_tracker", "Variable Tracker has the lowest expected annual cost at $82,400, and the treasury rule only applies to sites above 500,000 kWh a year."),
 ("green_fixed", "This contract starts after the renewable requirement takes effect, and Green Fixed is the only renewable fixed tariff.")],
"fixed_standard", 2,
twin=T([("New contract start: 1 November 2026, 24-month term.", "New contract start: 1 February 2027, 24-month term.")], "green_fixed")),

# ------------------------------------------------------------------ pl05
# why: tool will hold customer support tickets -> customer data -> SSO required.
# Starter has no SSO. Business $14 + SSO add-on $3 = $17 * 40 = $680. Enterprise $19,
# minimum 50 seats billed -> $950. Cheapest compliant = Business + SSO.
C("pl05", "Which subscription tier should be purchased for the support team?",
"""
Security Policy SP-7 (extract): any SaaS tool that stores customer data must use single sign-on (SSO) through the corporate identity provider.

Purchase request PR-7730 — Helpline ticketing tool "Casewise"
Team size: 40 agents. Use: logging and answering customer support tickets, including customer names, emails and order numbers.
Budget holder: Oona Petrakis. Rule: choose the lowest monthly cost that meets policy.

Casewise pricing (per user per month)
- Starter: $8. No SSO. Up to 50 users.
- Business: $14. SSO available as an add-on at $3 per user per month.
- Enterprise: $19. SSO included. Minimum billing of 50 seats.

Requester's note: "Starter is fine — most of what we store is internal notes, and the team leads can share one admin login."
IT note: Casewise supports our identity provider on Business and Enterprise.
Renewal of the old tool ends on 31 October.
""",
[("starter", "Starter is cheapest, and SSO only matters for tools that hold internal notes."),
 ("business_with_sso", "Business with the SSO add-on meets the SSO rule for $680 a month, less than Enterprise's 50-seat minimum."),
 ("enterprise", "Enterprise is cheaper per user than Business once SSO is included, so even with its 50-seat minimum it is the best value for a 40-person team.")],
"business_with_sso", 1),

# ------------------------------------------------------------------ pl06
# why: capex freeze on purchases > $10,000 unless safety-critical; forklift not
# safety-critical -> buy blocked. 36-month lease 980*36 = 35,280 (operating, allowed);
# rent 1,900*36 = 68,400. Cheapest allowed = lease. Buy $32,000 would be cheapest.
# Twin: safety-critical -> exception -> buy ($32,000 lowest).
C("pl06", "How should the depot acquire the replacement forklift?",
"""
Harrowgate Builders Merchants — Capital Expenditure Notice CX-26-3
From 1 July 2026 until 31 December 2026 no capital purchase above $10,000 may be approved, except items classified as safety-critical by the Health & Safety officer. Operating leases and rentals are not capital purchases and are not affected.
Decision rule for asset acquisitions: choose the lowest three-year total cost among the options the notice allows.

Request AQ-448, Ferris Lane depot
Item: 2.5-tonne counterbalance forklift, needed from 1 October 2026 for at least three years.
Safety classification: not safety-critical (routine replacement).
Options
- Buy outright: $32,000 (capital purchase). Servicing roughly equal for all options.
- 36-month operating lease: $980 per month.
- Short-term rental: $1,900 per month, cancel any time.

Depot manager: "We always bought forklifts outright before; it works out cheapest."
The old forklift is being sold for scrap value, about $1,500.
""",
[("buy_outright", "The purchase qualifies for the freeze exception and has the lowest three-year cost."),
 ("lease_36m", "The freeze blocks the purchase, and the 36-month lease is the cheapest option still allowed over three years."),
 ("rent_monthly", "Leases are also capital commitments under the freeze, so only monthly rental is allowed, even though it costs more over three years.")],
"lease_36m", 2,
twin=T([("Safety classification: not safety-critical (routine replacement).",
         "Safety classification: safety-critical (Health & Safety officer ruling HS-221, brake failure risk on the current unit).")], "buy_outright")),

# ------------------------------------------------------------------ pl07
# why: capacity >= attendees + 10% = 180*1.1 = 198; permanent step-free access.
# Beacon 190 < 198 fails. Cressley not step-free (portable ramp does not count).
# Ashwell 200, step-free, $7,800 -> only compliant.
# Twin: 170 attendees -> 187 -> Beacon (190, step-free, $6,900) cheapest compliant.
C("pl07", "Which venue should be booked for the regional staff day?",
"""
Events Policy (Tarn Valley Health Partnership), section 3
3.1 Room capacity (seated, theatre style) must be at least the expected attendance plus a 10% buffer.
3.2 The venue must offer permanent step-free access to the main room. Temporary or portable ramps do not meet this rule.
3.3 Choose the lowest total hire cost among venues meeting 3.1 and 3.2.

Staff day, 3 December 2026. Expected attendees: 180.

Venues
- Ashwell Hall: seats 200. Step-free (level entrance, lift). Hire $7,800.
- Beacon Rooms: seats 190. Step-free (ground floor). Hire $6,900.
- Cressley Manor: seats 250. Ballroom up six steps; "a portable ramp can be arranged on request". Hire $7,200.

Organiser note: Cressley hosted the staff day in 2024 and 2025 and feedback was good. Catering is quoted separately and is similar at all three.
""",
[("book_ashwell", "Ashwell is the cheapest step-free venue that seats the attendees plus the 10% buffer."),
 ("book_beacon", "Beacon seats attendees plus the 10% buffer and is the cheapest step-free venue."),
 ("book_cressley", "Cressley has space to spare, and a portable ramp on request gives the step-free access the policy needs.")],
"book_ashwell", 1,
twin=T([("Expected attendees: 180.", "Expected attendees: 170.")], "book_beacon")),

# ------------------------------------------------------------------ pl08
# why: 4,000 tx x $50 = $200,000/month. Flat 2.9% = 5,800 + 0.30*4000 = 1,200 -> 7,000.
# IC+ 1.8% = 3,600 + 0.15*4000 = 600 + 250 -> 4,450. Subscription 1.5% = 3,000 +
# 0.10*4000 = 400 + 399 -> 3,799 but 24-month term; any term > 12 months needs board
# approval regardless of value (none) -> excluded. Cheapest allowed = IC+.
C("pl08", "Which card-processing plan should the online shop sign?",
"""
Finance memo — card acquiring for the Fellhouse Outdoor online shop
Volumes: about 4,000 card payments a month, average $50 each.

Contracting Policy
K1. Any contract with a minimum term longer than 12 months requires board approval, regardless of its value.
K2. Choose the plan with the lowest expected monthly cost among plans that can be signed without further approval.
K3. The board next meets on 14 January 2027. The shop migration must be complete by 1 November 2026.

Offers from Tessel Payments
| Plan | Pricing | Minimum term |
| Flat | 2.9% + $0.30 per payment | none |
| Interchange-plus | 1.8% + $0.15 per payment + $250 monthly fee | 12 months |
| Subscription | 1.5% + $0.10 per payment + $399 monthly fee | 24 months |

Sales email from Tessel: "Subscription is our most popular plan for shops your size. The total contract value is under $100,000, so most clients don't need board sign-off."
""",
[("flat_plan", "Flat pricing avoids any minimum term and is the simplest to reconcile, which the policy prefers."),
 ("interchange_plus", "Interchange-plus has the lowest expected cost among plans that need no board approval."),
 ("subscription_plan", "Subscription is the cheapest plan, and its contract value is small enough to sign without the board.")],
"interchange_plus", 2),

# ------------------------------------------------------------------ pl09
# why: flight 7h10. Premium economy for > 4 h; business for > 8 h under amendment
# applying to trips booked on/after 1 Jul 2026 (was > 6 h). Booked 2 Sep 2026 ->
# 8 h rule -> premium economy. Client terms (economy only < 3 h) are not stricter.
# Twin: booked 18 Jun 2026 -> old 6 h rule -> business.
C("pl09", "Which cabin class may be booked for this trip?",
"""
Aldercroft Engineering — Travel Policy TP-3 (air travel)
3.1 Flights with a scheduled flight time of 4 hours or less: economy.
3.2 Flights over 4 hours: premium economy.
3.3 Flights over 6 hours: business class.
3.4 Book the highest class the policy permits for the flight; the traveller may choose a lower one.
3.5 For client-rebillable trips, the client's travel terms apply where they are stricter than this policy.
Amendment TP-3/A (applies to trips booked on or after 1 July 2026): in 3.3, "over 6 hours" becomes "over 8 hours".

Booking record TR-5528
Traveller: Idris Achterberg, principal engineer.
Route: Calder Bay to Port Venn, scheduled flight time 7 h 10 min, overnight.
Booked: 2 September 2026. Travel: 19 October 2026.
Rebillable to client Orla Shipping. Orla's travel terms: economy only for flights under 3 hours; no other limits.

Traveller's note: "On my last trip to Port Venn in 2025 I flew business."
""",
[("economy", "The trip is rebillable, and client-rebillable trips must always be booked in economy."),
 ("premium_economy", "Under the amended 8-hour threshold, a 7 h 10 min flight qualifies only for premium economy."),
 ("business", "The trip was booked before the amendment took effect, so the 6-hour rule makes the flight eligible for business.")],
"premium_economy", 2,
twin=T([("Booked: 2 September 2026.", "Booked: 18 June 2026.")], "business")),

# ------------------------------------------------------------------ pl10
# why: legal-hold data must be retrievable within 24 h -> archive (48 h) out.
# 50 TB: hot 50*20 = $1,000; cool 50*10 = 500 + retrieval 1 TB * $10 = $510.
# Cheapest compliant = cool. Twin: 60 TB retrieved/month -> cool 500+600 = 1,100 > 1,000 -> hot.
C("pl10", "Which storage tier should hold the case-file archive?",
"""
Records Management Standard RM-5 (Castleford & Mayne LLP)
RM-5.2: Data under legal hold must be retrievable in full within 24 hours of a request.
RM-5.4: Choose the storage tier with the lowest expected monthly cost that meets RM-5.2.

Data set: closed litigation case files under legal hold. Volume: 50 TB. Expected retrievals: about 1 TB a month.

Storage tiers (Stratacloud, per month)
| Tier | Storage price | Retrieval time | Retrieval fee |
| Hot | $20 per TB | immediate | none |
| Cool | $10 per TB | up to 1 hour | $10 per TB retrieved |
| Archive | $2 per TB | up to 48 hours | $5 per TB retrieved |

Cool and Archive charge a minimum of 90 days' storage per object; the files will be kept for at least 6 years.
Vendor sales deck: "Archive retrieval is usually done within a day, so it suits most legal-hold data."
IT note: the firm's e-discovery platform connects to all three tiers.
""",
[("hot_tier", "With the expected retrieval volume, cool's fees push it above hot, so hot is the cheapest tier meeting the 24-hour rule."),
 ("cool_tier", "Cool meets the 24-hour rule and costs about $510 a month against $1,000 for hot."),
 ("archive_tier", "Archive is by far the cheapest, and retrieval within a day is usually achieved.")],
"cool_tier", 2,
twin=T([("Expected retrievals: about 1 TB a month.", "Expected retrievals: about 60 TB a month (a monthly full re-scan by the e-discovery platform plus ad hoc pulls).")], "hot_tier")),

# ------------------------------------------------------------------ pl11
# why: limits: volatility <= 12%, fee <= 0.75%. Rank by net return (gross - fee).
# Aldgate 6.4-0.60 = 5.8; Carrick 6.1-0.20 = 5.9; Birchmoor vol 14.2% fails (limit
# applies to the default fund for all members). -> Carrick.
C("pl11", "Which fund should the trustees adopt as the default investment option?",
"""
Pellmore Staff Pension Scheme — Statement of Investment Principles (extract)
SIP 4.1: The default fund must have 5-year annualised volatility of no more than 12%.
SIP 4.2: The total annual fee must not exceed 0.75%.
SIP 4.3: Among funds meeting 4.1 and 4.2, choose the fund with the highest 5-year annualised return net of fees (gross return minus annual fee).
SIP 4.4: The default fund applies to all members who make no choice, of any age.

Shortlist (from the investment consultant, Haldane Row)
| Fund | 5-yr volatility | Annual fee | 5-yr gross return |
| Aldgate Balanced | 10.5% | 0.60% | 6.4% |
| Birchmoor Growth | 14.2% | 0.55% | 8.1% |
| Carrick Global Index | 11.8% | 0.20% | 6.1% |

Consultant's comment: "Birchmoor has been the strongest performer. Many schemes use a lifestyle approach where the volatility limit only bites for members over 55."
Minutes note: the scheme has not adopted a lifestyle approach.
""",
[("aldgate_balanced", "Aldgate has the highest gross return among funds within the volatility and fee limits."),
 ("birchmoor_growth", "Birchmoor has the strongest returns, and the volatility limit only applies to members over 55."),
 ("carrick_index", "Carrick's net return of 5.9% is the highest among funds meeting both limits.")],
"carrick_index", 2),

# ------------------------------------------------------------------ pl12
# why: base rule every 6 months (2 visits/yr); amendment from 1 Jan 2026: buildings
# over 10 floors every 4 months (3 visits/yr). 12-floor office -> Standard (3 visits,
# $3,300). 24-h callout required only for residential care. Premium not required.
# Twin: 9 floors -> 6-month rule -> Basic ($2,400).
C("pl12", "Which lift maintenance plan should the building manager sign?",
"""
Lift Inspection Regulations (Corvane Province), as consolidated
Reg. 5: passenger lifts must be inspected by a certified engineer at least once every 6 months.
Reg. 5A (added by amendment, effective 1 January 2026): in buildings of more than 10 floors, passenger lifts must be inspected at least once every 4 months.
Reg. 8: lifts in residential care buildings must have a 24-hour emergency callout.

Company rule: choose the cheapest plan that meets the regulations.

Building: Arden Quay, 12 floors, offices only. Three passenger lifts.

Plans offered by Summit Lift Services (annual price for all three lifts)
- Basic: 2 inspection visits a year, callout 08:00-18:00. $2,400.
- Standard: 3 inspection visits a year, callout 08:00-18:00. $3,300.
- Premium: 4 inspection visits a year, 24-hour callout. $4,900.

Tenant request: the ground-floor tenant asked for faster lift repairs after a 2-day outage in June.
""",
[("basic_plan", "The building is not over 10 floors, so two inspections a year suffice and Basic is the cheapest compliant plan."),
 ("standard_plan", "At over 10 floors the lifts need an inspection every 4 months, and Standard is the cheapest plan with three visits a year."),
 ("premium_plan", "Any building with public access needs a 24-hour emergency callout under Regulation 8, and Premium is the only plan that includes one.")],
"standard_plan", 1,
twin=T([("Building: Arden Quay, 12 floors, offices only.", "Building: Arden Quay, 9 floors, offices only.")], "basic_plan")),

# ------------------------------------------------------------------ pl13
# why: tier-1 systems need support cover across operating hours 06:00-22:00; cheapest
# covering that = Extended ($1,500). 24x7 not required (only "at least" operating hours).
# Payroll system classified tier-1.
C("pl13", "Which vendor support plan should be bought for the payroll system?",
"""
IT Service Continuity Standard (Ruskin Logistics)
Tier-1 systems: vendor support must cover at least the company's operating hours, 06:00-22:00, seven days a week.
Tier-2 systems: vendor support must cover at least business hours, 08:00-18:00, Monday to Friday.
In all cases, buy the cheapest plan that meets the minimum cover.

System: Paylane payroll platform. Classification (Service Catalogue, reviewed March 2026): tier-1.

Paylane support plans (monthly)
- Business Hours: 08:00-18:00 Mon-Fri. $900.
- Extended: 06:00-22:00, seven days. $1,500.
- 24x7: round the clock. $2,400.

Notes from the renewal meeting
- IT manager: "We always buy 24x7 for anything important."
- Payroll lead: "The payroll team only works office hours, so Business Hours should do."
""",
[("business_hours", "The payroll team works office hours only, so Business Hours cover is enough."),
 ("extended", "As a tier-1 system it needs cover from 06:00 to 22:00 every day, and Extended is the cheapest plan that gives it."),
 ("round_the_clock", "Tier-1 systems must always have round-the-clock support, because an outage outside operating hours would still delay the next payroll run.")],
"extended", 1),

# ------------------------------------------------------------------ pl14
# why: venue contract needs $5M liability cover; risk policy caps deductible at
# $2,500 for all event policies. Stallard $5M/$1,000/$640 ok; Teviot $5M/$5,000 ->
# deductible too high; Umber $2M fails cover. -> Stallard.
# Twin: Teviot deductible $2,500 (meets cap, inclusive) -> cheaper $410 -> Teviot.
C("pl14", "Which event insurance policy should be bought for the craft fair?",
"""
Ferrow Makers' Guild — Craft Fair, 21-22 November 2026, Ellery Exhibition Centre

Venue hire agreement, clause 11: the hirer must hold public liability insurance with a limit of at least $5,000,000 for the event days.
Guild Risk Policy, R4: for any insurance the Guild buys, the deductible (excess) must not be more than $2,500 per claim. R5: choose the lowest premium among policies meeting all requirements.

Quotes
| Insurer | Liability limit | Deductible per claim | Premium |
| Stallard Mutual | $5,000,000 | $1,000 | $640 |
| Teviot Insure | $5,000,000 | $5,000 | $410 |
| Umber Risk | $2,000,000 | $500 | $350 |

Treasurer's note: "The deductible cap is really meant for our building insurance, isn't it?" (R4 applies to all Guild insurance.)
Umber says the venue's own cover would "top up" the difference; the venue has confirmed it will not.
""",
[("stallard_mutual", "Stallard is the only policy with at least $5M cover and a deductible within the $2,500 cap."),
 ("teviot_insure", "Teviot meets the $5M requirement and the deductible cap, and has the lower premium."),
 ("umber_risk", "Umber is cheapest, and the venue's own cover makes up the gap to $5M.")],
"stallard_mutual", 2,
twin=T([("| Teviot Insure | $5,000,000 | $5,000 | $410 |", "| Teviot Insure | $5,000,000 | $2,500 | $410 |")], "teviot_insure")),

# ------------------------------------------------------------------ pl15
# why: required capacity = forecast peak * 1.25 = 1,800 * 1.25 = 2,250 rps. S 1,000,
# M 2,000 fail; L 4,000 ok at $1,200 <= budget $1,500. Clustering small plans not
# approved (single instance). -> L.
C("pl15", "Which hosting plan should be provisioned for the ticket sale?",
"""
Architecture Decision Record ADR-71 — Hosting for the Harbour Festival ticket sale

Constraints
- Forecast peak load: 1,800 requests per second (from last year's sale plus 20% growth).
- Capacity rule (Platform Standard 3.2): provisioned capacity must be at least 25% above the forecast peak.
- Capacity must come from a single instance; clustering several small plans is not an approved pattern for this platform.
- Budget: at most $1,500 per month.
- Choose the cheapest plan meeting all constraints.

Plans (Gantry Cloud)
| Plan | Capacity | Monthly price |
| S | 1,000 rps | $400 |
| M | 2,000 rps | $700 |
| L | 4,000 rps | $1,200 |

Comment from the lead developer: "M covers 1,800 easily, and we can always scale up on the day."
Comment from finance: "Two S boxes would give 2,000 rps for $800."
""",
[("plan_m", "M's 2,000 rps covers the forecast peak of 1,800, and it is cheaper than L."),
 ("plan_l", "Only L covers the forecast peak plus 25% headroom on a single instance within the budget."),
 ("two_plan_s", "Two S instances give 2,000 rps for $800, and clustered capacity counts the same as one plan.")],
"plan_l", 1),

# ------------------------------------------------------------------ pl16
# why: 1 first-aider per 50 staff (rounded up), high-risk sites 1 per 25; call centre
# is not high-risk. 120 staff -> 3 needed. One valid certificate held (to 2028) -> 2
# more. Smallest package covering 2 = Pack-2.
# Twin: certificate expired June 2026 -> 3 needed -> Pack-4.
C("pl16", "Which first-aid training package should be booked?",
"""
Workplace First Aid Rules (company standard WS-2)
WS-2.1 Each site must have at least one first-aider with a valid certificate for every 50 staff, rounded up.
WS-2.2 High-risk sites (construction, chemical handling or heavy machinery) need one for every 25 staff, rounded up.
WS-2.3 Book the smallest training package that brings the site up to the required number.

Site: Linfield contact centre. Staff: 120. Activities: telephone and email customer service.
Current first-aiders: Rosa Keane — certificate valid until March 2028.

Training packages (Beacon First Aid Training)
- Pack-2: 2 trainees, $600.
- Pack-4: 4 trainees, $1,050.
- Pack-6: 6 trainees, $1,450.

Office manager's note: "We have a loading bay for stationery deliveries, so I assumed the high-risk ratio applies."
Fire warden training is separate and was completed in May.
""",
[("pack_2", "Three first-aiders are needed and Rosa already counts as one, so two trainees are enough."),
 ("pack_4", "Three first-aiders are needed and none currently holds a valid certificate, so Pack-4 is the smallest package that covers it."),
 ("pack_6", "The loading bay makes this a high-risk site, which needs five first-aiders.")],
"pack_2", 1,
twin=T([("certificate valid until March 2028.", "certificate expired in June 2026.")], "pack_4")),

# ------------------------------------------------------------------ pl17
# why: trading-desk calls (all, internal and external) must be retained 7 years; may
# be kept in an approved archive. Vaultline approved; export available on Pro and
# above. Pro + export $18 < Compliance $31 -> pro_with_archive_export. Standard can't export.
C("pl17", "Which conference-call plan should the trading desk use?",
"""
Record-keeping Rule RK-11 (Easterly Capital Markets)
RK-11.1 All voice and video calls made or received by trading desk staff, internal or external, must be recorded and retained for 7 years.
RK-11.2 Recordings may be retained natively by the call provider or in an approved company archive.
RK-11.3 Choose the lowest-cost plan that meets RK-11.1 and RK-11.2.

Approved archives register: Vaultline (approved for regulated records, ref AR-17).

Bridgewave plans (per user per month)
- Standard: $12. Recording retained 90 days. No export.
- Pro: $18. Recording retained 1 year. Automatic export to Vaultline available at no extra charge.
- Compliance: $31. Recording retained natively for 7 years.

Desk head's comment: "Most of our calls are internal huddles, so the rule barely applies to us."
""",
[("standard_plan", "Most desk calls are internal and outside the recording rule, so Standard is enough."),
 ("pro_with_archive_export", "Pro's automatic export to the approved Vaultline archive meets the 7-year rule at lower cost than Compliance."),
 ("compliance_plan", "The rule requires the call provider itself to keep recordings for seven years, which only the Compliance plan does natively at any price.")],
"pro_with_archive_export", 2),

# ------------------------------------------------------------------ pl18
# why: 2 travellers -> compact; equipment upgrade of one class allowed with manager
# approval; approval given -> mid-size. Van only for 5+ travellers.
C("pl18", "Which hire-car class should be booked?",
"""
Travel Policy (Quarrington Surveys), section 6: vehicle hire
6.1 Class by number of travellers: 1-2 compact; 3-4 mid-size; 5 or more van.
6.2 Where the trip carries survey equipment, the class may be raised by one step with the line manager's written approval.
6.3 No other upgrades are allowed; loyalty upgrades offered by the hire company may be accepted at no cost.

Booking request VH-2207
Travellers: Nadia Szabo and Kwame Ellery (2).
Trip: site survey at Hollin Moor, 6-8 October 2026.
Equipment: GNSS base station and tripod cases (about 80 kg).
Approval: equipment upgrade approved in writing by Olu Mensah (line manager) on 3 September 2026.

Nadia's note: "Last time we took a compact and the cases barely fitted. A van would be ideal."
""",
[("compact", "Two travellers fit the compact class, and upgrades are not allowed under this policy."),
 ("mid_size", "The approved equipment upgrade moves the two travellers up one class, from compact to mid-size."),
 ("van", "Survey equipment always justifies a van whatever the number of travellers, and the cases barely fitted in a compact last time.")],
"mid_size", 1),

# ------------------------------------------------------------------ pl19
# why: payment amount = invoice + freight = 23,900 + 850 = 24,750 < 25,000 -> ACH
# (bank details on file). Wire only >= 25,000. Cheques only when no bank details.
C("pl19", "Which payment method should accounts payable use for this supplier payment?",
"""
Treasury Payments Procedure (Belvoir Textiles), version 6
P1. Payments of $25,000 or more must be made by wire transfer with dual approval.
P2. Payments below $25,000 are made by ACH to the bank account on file.
P3. Cheques may be used only for suppliers with no bank details on file.
P4. The payment amount is the total due to the supplier under the invoice, including freight and other charges shown on it.

Payment request AP-66120
Supplier: Marlow Yarn Co. Bank details on file: yes (verified 12 March 2026).
Invoice MY-4471: goods $23,900.00; freight $850.00; total due $24,750.00. Due 30 September 2026.

Supplier's 2019 remittance form (still in the vendor file) says: "Payment by cheque preferred."
AP clerk's comment: "This is a big one; shouldn't it go by wire to be safe?"
""",
[("ach", "The total due, including freight, is below $25,000 and bank details are on file, so ACH applies."),
 ("wire_transfer", "With freight included the payment reaches $25,000, so it must go by wire with dual approval."),
 ("cheque", "The supplier's remittance form asks for cheques, and supplier preferences should be honoured.")],
"ach", 1),

# ------------------------------------------------------------------ pl20
# why: per person 13 days/month; client files need lockable storage (locker add-on
# $30 available on day and flex options; dedicated includes one). Hot: 13*25 = 325
# + 30 = 355. Flex: 220 + 3*25 = 295 + 30 = 325. Dedicated 380. -> flex.
# Twin: 8 days -> hot 200+30 = 230; flex 220+30 = 250; dedicated 380 -> hot desk.
C("pl20", "Which coworking membership should the team take?",
"""
Office Services Guidance (Halloran Tax Advisers), satellite offices
G1. Staff who handle client files must have lockable storage at any workspace they use.
G2. Choose the membership with the lowest monthly cost per person that meets G1.

Team: 6 tax advisers, all handling client files. Expected use: 13 days per person per month.

Workhive Tannery Yard — membership options (per person per month)
- Day passes: $25 per day used. Locker add-on: $30 a month.
- Flex 10: $220 for 10 days; extra days $25 each. Locker add-on: $30 a month.
- Dedicated desk: $380, unlimited days, lockable pedestal included.

Team lead's note: "I'd rather have dedicated desks; it feels more professional for client visits." (Client meetings are held in bookable rooms, charged separately for every option.)
""",
[("day_passes", "Paying $25 for each day used plus a $30 locker is the cheapest per-person set-up."),
 ("flex_10", "At the team's usage, a 10-day pack topped up with day passes plus a locker is the cheapest per-person set-up."),
 ("dedicated_desk", "Only dedicated desks include lockable storage, which client files require, so the cheaper day and flex options cannot be used.")],
"flex_10", 2,
twin=T([("Expected use: 13 days per person per month.", "Expected use: 8 days per person per month.")], "day_passes")),

# ------------------------------------------------------------------ pl21
# why: insurer endorsement E4 (amended at renewal 1 Aug 2026): Grade A centre and
# keyholder response within 20 minutes (was 30). Sentry Basic Grade B fails; Sentry
# Plus 30 min fails; Watchpoint Lite 25 min fails; Watchpoint Pro 15 min ok -> Pro.
# Twin: Lite 18 min -> meets both, $60 < $95 -> Lite.
C("pl21", "Which alarm monitoring plan meets the insurer's conditions at the lowest cost?",
"""
Insurance schedule, Pennywick Jewellers, policy PJ-4410
Endorsement E4 (alarm conditions), as amended at the renewal on 1 August 2026:
(a) the intruder alarm must be monitored by an alarm receiving centre certified Grade A;
(b) a keyholder or guard must attend within 20 minutes of an alarm activation (previously 30 minutes).
Failure to meet E4 voids theft cover.

Shop policy: choose the cheapest monitoring plan that satisfies E4.

Monitoring plans quoted
| Plan | Centre grade | Keyholder attendance | Monthly fee |
| Sentry Basic | Grade B | 30 minutes | $45 |
| Sentry Plus | Grade A | 30 minutes | $70 |
| Watchpoint Lite | Grade A | 25 minutes | $60 |
| Watchpoint Pro | Grade A | 15 minutes | $95 |

Owner's note: "Sentry has monitored the shop for eight years without a single problem."
""",
[("sentry_basic", "Sentry Basic is the cheapest plan, and eight years of reliable service show it is good enough."),
 ("sentry_plus", "Sentry Plus uses a Grade A centre, and the 30-minute attendance limit is met."),
 ("watchpoint_lite", "Watchpoint Lite uses a Grade A centre, meets the 20-minute attendance condition and costs less than Pro."),
 ("watchpoint_pro", "Watchpoint Pro is the only plan meeting both the Grade A and the 20-minute attendance conditions.")],
"watchpoint_pro", 2,
twin=T([("| Watchpoint Lite | Grade A | 25 minutes | $60 |", "| Watchpoint Lite | Grade A | 18 minutes | $60 |")], "watchpoint_lite")),
]
