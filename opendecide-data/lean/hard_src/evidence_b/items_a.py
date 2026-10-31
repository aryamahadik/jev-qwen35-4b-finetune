"""Domain A: licensing requirements (invented statutes)."""
from _h import it

NONE = "none of these"

ITEMS = [

it("A1", "noul",
   "Under the quoted Code provisions, is Odette exempt from the mobile food unit permit requirement for her Saturday sales?",
   """From: Odette Varga <odette@vargafarm.example>
To: Permits Desk, Harlow County Environmental Health
Subject: Do I need a mobile food permit for Saturday tomato sales?

Hello,

I grow heirloom tomatoes on my farm outside Pell's Crossing. Starting next month I'd like to sell them whole, straight from the crates in the bed of my pickup truck. Every Saturday I'd park in the lot of Grace Chapel on Linden Road (the chapel lets the public use it) from 8:00 a.m. to 11:30 a.m., then drive to the Fairmont Plaza lot and sell there from 12:15 p.m. to 3:45 p.m. Nothing is cut, washed, or cooked on site, and I don't sell anything I didn't grow myself.

A neighbour told me that because I'm out selling for more than seven hours, I definitely need the permit. Is that right?

Thanks, Odette

--- Reply draft (Permits Desk), quoting the Code ---
Harlow County Code §7-12(a): A mobile food unit permit is required for any person who sells or offers food from a vehicle or cart located on a public right-of-way or on private property open to the public.
§7-12(b)(2): No permit is required for the sale of whole, uncut produce grown by the seller.
§7-12(c): The exemption in (b)(2) does not apply where the produce is offered from a motorised vehicle that remains at any one location for more than four hours in a single day.""",
   1,
   card="- exemption in §7-12(b)(2): no mobile food unit permit is needed to sell whole, uncut produce grown by the seller\n- exception in §7-12(c): the exemption is lost when the produce is offered from a motorised vehicle that remains at any one location for more than four hours in a single day",
   diff=2, twin=[("from 8:00 a.m. to 11:30 a.m.", "from 7:00 a.m. to 11:30 a.m.")], twin_gold=0),

it("A2", "choice",
   "What is the lowest licence class the Act requires for the work Ibsen contracted to do?",
   """VELLMAR BUILDING TRADES BOARD - Investigator worksheet, File BT-2291
Respondent: Ibsen Remodeling LLC (holds Class C licence no. C-40417)
Complainant: homeowner Priya Castellanos, 88 Wren Hollow Road

Statute excerpt (Building Trades Act §4):
(1) No licence is required for a project with a total contract price under $5,000, unless the work involves structural alteration, gas piping, or an electrical service panel, in which case a Class C licence is the minimum.
(2) Class C: total contract price from $5,000 up to and including $50,000. Class B: over $50,000 up to and including $500,000. Class A: over $500,000.
(3) Total contract price includes materials furnished by the contractor but excludes materials furnished by the owner.
(4) Contracts between the same contractor and the same owner for work on the same property that are signed within 90 days of each other are treated as one project.

Findings:
- Contract 1, signed March 3: kitchen remodel, price $38,000 (includes $12,000 of cabinets Ibsen supplied). Ms. Castellanos separately bought $9,000 of appliances, which Ibsen installed under Contract 1; their cost is not part of the $38,000.
- Contract 2, signed May 20: bathroom tiling at the same property, price $14,500.
- Neither contract involves structural, gas, or service-panel work.
- Ibsen's owner told the investigator that each contract is "well within Class C".""",
   "Class B",
   opts=["no licence required", "Class C", "Class B", "Class A", NONE],
   card="- no licence required: the project falls below every licence threshold\n- Class C: licence for projects from $5,000 up to $50,000, or smaller projects with structural, gas or panel work\n- Class B: licence for projects over $50,000 up to $500,000\n- Class A: licence for projects over $500,000\n- none of these: no listed class correctly states the requirement",
   diff=3, twin=[("Contract 2, signed May 20", "Contract 2, signed June 12")], twin_gold="Class C"),

it("A3", "noul",
   "Can a permit lawfully be issued for the cottage rentals as quietlakehost plans them?",
   """Forum: Brannock Neighbours > Housing & Rentals
Thread: Renting my garden cottage - permit question
Posted by quietlakehost

I've lived in my house on Fenwick Street for 11 years; I'm there roughly 250 days a year. Behind the house, on the same lot, there's a small garden cottage with its own kitchen. I want to put the cottage on a short-term rental site. Realistically, most bookings will be January to March while I'm staying with my daughter in Port Ellery, because that's when I'd like the extra income and the house is empty anyway. A friend will handle check-ins.

I read the ordinance and I think I'm fine because it's my primary residence. Can someone confirm?

Reply from brannock_planner_volunteer (quoting the ordinance):
§3.2 A short-term rental permit may be issued only for a host's primary residence. "Primary residence" means the dwelling in which the host resides for at least 183 days in the calendar year.
§3.4 A dwelling unit located on the same parcel as the host's primary residence (an "accessory unit") may also be permitted, but only if the host occupies the primary residence during every rental stay in the accessory unit.
§3.7 No permit may be issued for a rental arrangement that, as described by the applicant, would not comply with this chapter.""",
   0,
   card="- primary residence: the dwelling where the host lives at least 183 days in the calendar year\n- accessory unit: a dwelling on the same parcel as the host's primary residence; it may be permitted only if the host occupies the primary residence during every rental stay",
   diff=1),

it("A4", "noul",
   "Does Rentwise fall within the §202(c) agent-of-payee exclusion?",
   """INTERNAL MEMO - Rentwise Inc., Compliance
Re: Do we need an Ostrava money transmitter licence?

Our product: tenants pay rent through the Rentwise app; we hold the funds for two business days and then push them to the landlord's bank account, keeping a 1% fee.

Relevant law - Ostrava Money Services Act:
§201. No person may engage in the business of money transmission in this State without a licence issued under this Act.
§202(c). This Act does not apply to a person acting as an agent of a payee, if (i) there is a written agreement between the payee and the agent directing the agent to collect and process payments on the payee's behalf; (ii) the payee holds the agent out to the public as accepting payments on the payee's behalf; and (iii) payment of money by the payer to the agent satisfies the payer's obligation to the payee to the extent of the payment.

Facts gathered:
1. Every landlord signs our Collection Services Agreement, which appoints Rentwise to collect rent on the landlord's behalf.
2. Our standard lease rider, which landlords attach to their leases, tells tenants: "Pay all rent through the Rentwise app."
3. The same rider provides: "Rent is deemed paid only when the funds are credited to Landlord's bank account."
4. About 3% of transfers fail after the tenant pays us (the landlord's bank rejects the deposit); in those cases some landlords have charged late fees.""",
   0,
   card="- agent-of-payee exclusion: applies only if all three conditions hold: a written collection agreement with the payee, the payee holds the agent out to the public as accepting payments, and payment to the agent discharges the payer's obligation to the payee to that extent",
   diff=2),

it("A5", "choice",
   "Which licence category does R.12 place Marisol's daycare in?",
   """Subject: Licence question - my home daycare
To: licensing@dellow-childcare.example

Hi, I'm Marisol Quintero. I run a small daycare out of my home on Pike Lane. Currently I care for 7 children from other families during the day. My own two kids are also home with us: my son Teo (4) and my daughter Lina (7), who comes home from school at 3 p.m. My nephew Rafa (3) also stays with us every weekday because my sister works nights. So on a typical afternoon there are 10 kids in the house. What licence do I need?

Auto-reply attachment - Dellow Child Care Regulations, R.12 (Counting and Categories):
(a) Count all children in care, except children related to the provider (child, stepchild, grandchild, niece, nephew, or sibling of the provider). However, the provider's own children and stepchildren under 6 years old are counted.
(b) 3 or fewer counted children: no licence required.
(c) 4 to 8 counted children: Family Home licence.
(d) 9 to 14 counted children: Group Home licence (a second qualified adult must be present).
(e) 15 or more counted children: Child Care Centre licence.""",
   "Family Home licence",
   opts=["no licence required", "Family Home licence", "Group Home licence", "Child Care Centre licence"],
   card="- no licence required: 3 or fewer counted children\n- Family Home licence: 4 to 8 counted children\n- Group Home licence: 9 to 14 counted children, with a second qualified adult present\n- Child Care Centre licence: 15 or more counted children",
   diff=2, twin=[("my daughter Lina (7), who comes home from school at 3 p.m.", "my daughter Lina (5), who isn't in school yet")], twin_gold="Group Home licence"),

it("A6", "noul",
   "Did Theo's Saturday flight require a commercial operator certificate under Rule 9?",
   """Messages - Theo Brandt and Gil Asante (neighbour), Keswin Territory
Gil: Hey, any chance you could fly your drone over my roof Saturday? The insurance adjuster wants photos of the storm damage and I'm not climbing up there.
Theo: Sure, happy to help.
Gil: Great. I'll cover what it costs to charge your batteries, and I'll take you out for lunch at Mariner's afterwards as a thank-you. Deal?
Theo: Deal, see you at 10.
[Saturday] Theo flew for 20 minutes and sent Gil 46 photos. Gil paid Theo $4 for battery charging and bought him lunch ($23).

Note: Theo holds only a recreational drone registration.

Keswin Aerial Operations Rule 9:
(1) A commercial operator certificate is required for any flight conducted for compensation or hire.
(2) "Compensation" means any payment, goods, services, or reimbursement received in connection with the flight, except (a) reimbursement of actual fuel or battery-charging costs, and (b) a gift that was not agreed or promised before the flight.""",
   1,
   card="- compensation: any payment, goods, services or reimbursement connected with the flight, except reimbursement of actual fuel or charging costs and gifts not agreed or promised before the flight",
   diff=2),

it("A7", "choice",
   "Applying the Act, what is the minimum credential Ms. Okafor needs to do this work in Pellam?",
   """PELLAM DEPARTMENT OF HEALTH - Body Art Inspection Notes
Premises: Lindqvist Dermatology, 12 Cooper Street (physician-owned clinic)
Inspector: R. Adeyemi | Date: 14 May

Observed: Rhea Okafor performing microblading (eyebrows) on a client in Treatment Room 2. Dr. Signe Lindqvist, MD, was on site and states that she personally supervises all cosmetic procedures. Ms. Okafor produced a current Body Art Practitioner licence issued by the State of Arvane. She states she has worked in Pellam on 9 days so far this calendar year (all at this clinic) and is booked for 3 more days next month. No Pellam credential of any kind is on file.

Pellam Body Art Act:
§4 Every person performing body art must hold a Pellam Body Art Practitioner licence, except as provided in §5 and §6.
§5 A practitioner holding a current body art licence from another jurisdiction may instead work under a Guest Permit, for no more than 14 days in any calendar year.
§6 A person performing only permanent cosmetic procedures under the direct supervision of a licensed physician, on the physician's premises, needs no credential under this Act. This section does not apply to microblading.""",
   "a Guest Permit",
   opts=["a Guest Permit", "a Pellam Body Art Practitioner licence", "no credential needed", NONE],
   card="- no credential needed: the work falls within the §6 physician-supervision exemption\n- a Guest Permit: permit for a practitioner licensed elsewhere, valid for up to 14 days per calendar year\n- a Pellam Body Art Practitioner licence: the full local practitioner licence under §4\n- none of these: no listed credential is the minimum required",
   diff=3),

it("A8", "noul",
   "Is Jonah's lockout call covered by the §5(3) exemption?",
   """r/PropertyMaintenance - posted by jonah_fixes
Title: Do I need a locksmith licence for lockouts?

I'm a maintenance tech for Birchline Property Management. Last night a tenant at our Kestrel Court building (Birchline manages it) called because she was locked out. Before opening the door I asked for her photo ID and checked it against the lease file on my phone - name and photo matched. Then I picked the lock. My buddy says I'm basically running an unlicensed locksmith business. Here's the state act as far as I can tell:

Locksmith Licensing Act
§5(1) No person shall perform locksmith services for the public without a locksmith licence.
§5(3) Subsection (1) does not apply to an employee of a property management company who performs locksmith services solely on properties managed by the employer.
§5(4) The exemption in subsection (3) does not apply to opening a lock for a person who is locked out, unless the employee first verifies that person's identity against the tenancy records.

I've never done lock work anywhere other than Birchline buildings. Am I OK?""",
   1,
   card="- §5(3) exemption: a property-management employee doing lock work solely on properties the employer manages; for lockouts, only if the person's identity is first verified against the tenancy records",
   diff=1),

it("A9", "choice",
   "Which single licence type would authorise every sale in Tallow & Tap's plan?",
   """Application pre-check notes - Carrow Beverage Control Board
Applicant: Tallow & Tap Cafe, 410 Quarry Street

Business plan (from applicant): The cafe brews its own beer in a 3-barrel system in the back room. It wants to (1) sell pints of its own beer to customers seated in the cafe, (2) fill 64-oz growlers of its own beer for customers to take home, and (3) offer a short list of wine by the glass and by the bottle for customers to drink in the cafe. No spirits will be sold. Food (sandwiches, pastries) is expected to be about 30% of gross receipts. Children are welcome until 8 p.m.

Board guidance: an applicant receives one licence, and that licence must authorise every planned sale. The licence types are summarised in Schedule 1, reproduced in the card. The Board notes that the applicant describes itself as "a cafe first".""",
   "Brewpub (BP)",
   opts=["Restaurant Full (RF)", "Restaurant Beer & Wine (RBW)", "Tavern (TV)", "Bottle Shop (BS)", "Brewpub (BP)",
         "Event Permit (EP)", "Caterer (CT)", "Tasting Room (TR)", "Club (CL)", "Grocery Beer & Wine (GBW)", NONE],
   card="""- Restaurant Full (RF): spirits, beer and wine for consumption on the premises only; food must be at least 40% of gross receipts
- Restaurant Beer & Wine (RBW): beer and wine for consumption on the premises only; food must be at least 40% of gross receipts
- Tavern (TV): spirits, beer and wine for consumption on the premises only; no food minimum; no one under 21 admitted
- Bottle Shop (BS): sealed containers of any alcohol for consumption off the premises only
- Brewpub (BP): beer brewed on site, sold for consumption on the premises and in sealed or refillable containers to take away; may also sell wine for consumption on the premises; no spirits; no food minimum
- Event Permit (EP): any alcohol at a single event of up to 3 days sponsored by a nonprofit
- Caterer (CT): any alcohol served with food at private events away from the licensee's premises
- Tasting Room (TR): samples of no more than 2 oz of a winery's or distillery's own product
- Club (CL): any alcohol served to members of a nonprofit members-only club
- Grocery Beer & Wine (GBW): sealed beer and wine for off-premises consumption in a store with at least 50% of floor area devoted to food
- none of these: no single listed licence authorises every planned sale""",
   diff=2),

it("A10", "noul",
   "Under §12, was the July 10 Hensley Street work lawful?",
   """From: Paulo Ferreira, Master Electrician
To: Nils (office), Ferreira Electric
Subject: Board letter

Nils - the Board wants to know about the Hensley Street job. Timeline as best I can reconstruct it:
- June 30: my electrical contractor licence expired (I forgot to renew).
- July 10: we wired the Hensley Street garage subpanel.
- July 22: I paid the fee and renewed online; the Board's portal shows the renewal approved that day.
- Separately: on July 15 I received a letter from the Board saying a customer complaint about an unrelated job had been opened against me.

The Board's letter quotes the Electrical Licensing Act:
§12(a) It is unlawful to perform electrical work while the contractor's licence is expired.
(b) A licence renewed within 30 days after its expiration date is treated as having been continuously in force for all purposes.
(c) Subsection (b) does not apply if, before the renewal, the licensee received written notice of a pending disciplinary complaint.

Can you pull the invoices for July? I want to answer them this week.""",
   0,
   card="- continuity rule in §12(b): a licence renewed within 30 days after expiry counts as continuously in force, unless before renewing the licensee received written notice of a pending disciplinary complaint",
   diff=2, twin=[("on July 15 I received a letter", "on July 25 I received a letter")], twin_gold=1),

it("A11", "choice",
   "Which permit arrangement does Rule 14 require for Ines's busking?",
   """City of Marrow Falls - Street Performance Permits (FAQ excerpt, Rule 14)
- Performing in Zone 1 (Old Market Square) requires a Tier 2 permit.
- Performing anywhere else requires a Tier 1 permit, except that any performance using amplified sound requires a Tier 2 permit regardless of zone.
- A performer under 16 must hold a Youth Permit in place of a Tier 1 permit. A Youth Permit cannot be issued for any performance that would require a Tier 2 permit; in that case a parent or guardian must hold the Tier 2 permit on the youth's behalf and be present.
- Performers at events that hold a separate special-event permit need no individual permit.

Email from a parent:
My daughter Ines is 15 and plays violin. She'd like to busk on Saturday afternoons on Canal Street near the library (that's Zone 3, not the square). She plays unamplified. There's no organised event - just her and her open violin case. What permit should we apply for, and in whose name?""",
   "a Youth Permit",
   opts=["no permit needed", "a Tier 1 permit in Ines's name", "a Tier 2 permit in Ines's name", "a Tier 2 permit held by her parent or guardian", "a Youth Permit"],
   card="- no permit needed: the performance requires no individual permit\n- a Tier 1 permit in Ines's name: the standard permit for unamplified performances outside Zone 1\n- a Youth Permit: the permit an under-16 performer holds in place of a Tier 1 permit\n- a Tier 2 permit in Ines's name: the higher-tier permit held by the performer herself\n- a Tier 2 permit held by her parent or guardian: a Tier 2 permit held on the youth's behalf by a parent or guardian who is present",
   diff=2),

it("A12", "noul",
   "Was the October payment to Ms. Moss permitted under Rule 22?",
   """Complaint review - Real Estate Commission, File RC-6630
Licensee: Damaris Kell (salesperson, Hollin Realty)
Recipient of payment: Harriet Moss (not licensed)

Rule 22 (Referral compensation):
(a) No licensee may pay compensation to any person for referring a prospective buyer or seller unless that person holds a real estate licence.
(b) Notwithstanding (a), a licensee may pay a referral fee of $250 or less per transaction to a person who is a current client of the licensee, provided that no more than two such fees are paid to the same person in any 12-month period.

Facts:
- Ms. Moss signed a buyer-representation agreement with Ms. Kell in January to search for a condominium; the agreement is still in effect and she has not yet bought.
- In March, Ms. Kell paid Ms. Moss $200 for referring her cousin, who bought a house through Ms. Kell.
- In October, Ms. Kell paid Ms. Moss $250 for referring a co-worker, who listed and sold a flat through Ms. Kell. This October payment is the subject of the complaint.
- No other payments to Ms. Moss appear in the licensee's records.
- The complainant, a competing broker, argues that "any payment to an unlicensed person for a referral is prohibited".""",
   1,
   card="- permitted referral fee: $250 or less per transaction, paid to a current client of the licensee, with no more than two such fees to the same person in any 12-month period",
   diff=2),

it("A13", "choice",
   "What fee does §9 require the Rotary to pay?",
   """Seasonal food establishment - fee calculation request
From: Treasurer, Lakeshore Rotary Fish Fry (registered nonprofit)

We're applying for the Ember County food establishment permit for our lakeside fish-fry pavilion. It has 90 seats and will operate for 100 days this year (May to August). Last year's volunteer treasurer paid $700, but I can't find how that was worked out. Please confirm this year's fee.

Ember County Fee Ordinance §9:
(1) The annual fee is $400, plus $25 for each seat in excess of 50.
(2) A seasonal establishment (operating no more than 120 days in the permit year) pays 60% of the amount computed under (1). This reduction is applied before the cap in (3).
(3) No establishment pays more than $1,500 after applying (1) and (2).
(4) A registered nonprofit pays 50% of the amount due after applying (1) through (3).""",
   "$420",
   opts=["$420", "$570", "$700", "$750", "$840", "$950", "$1,140", "$1,500"],
   tpl="the permit fee due this year is {}",
   diff=2),

it("A14", "noul",
   "Does §4.3 require the teacher to obtain a home occupation permit?",
   """Neighbourhood list-serv - Ashgrove Heights
Subject: Home piano studio - do I need a permit?

I teach piano from my living room. Over the last four weeks my student visits were: week 1 - 10, week 2 - 7, week 3 - 9, week 4 - 6. My husband, who lives here, sometimes accompanies advanced students. We also get daily deliveries from parcel carriers (sheet music, supplies). A neighbour says the parcel vans plus the students make me a "commercial operation" that needs a permit.

The town code, as posted on the town website:
Home Occupation Code §4.3: A home occupation permit is required if the business
(a) has any employee who does not reside in the dwelling working on the premises; or
(b) receives more than 8 customer or client visits per week, averaged over any 4 consecutive weeks.
Deliveries by parcel or freight carriers are not customer or client visits.

My records cover only these four weeks; the studio opened a month ago.""",
   0,
   card="- home occupation permit trigger: a non-resident employee working on the premises, or more than 8 customer or client visits per week averaged over any 4 consecutive weeks; carrier deliveries are not visits",
   diff=2),

it("A15", "choice",
   "Which one of the persons reviewed needed an auctioneer licence?",
   """Licensing Division - Auctioneer compliance sweep, Quarter 3
Rule: Auctioneer Licensing Act
§2 A licence is required to conduct an auction, except:
 (a) a sale by the owner of the property being sold;
 (b) an auction for a registered charity where the person calling bids receives no compensation of any kind;
 (c) a sale conducted by a sheriff under court order.
§3 The exemption in §2(a) is not available to a person who has conducted more than three auctions of his or her own property in the 12 months preceding the auction.

Persons reviewed (none holds a licence):
1. Deputy Anand Rao - sold 14 seized vehicles under a court order on behalf of the county sheriff.
2. Mirela Constantin - auctioned her late aunt's furniture, which she inherited; her second auction this year.
3. Fr. Tomas Castell - called bids, unpaid, at the St. Ione Hospice gala; the hospice is a registered charity.
4. Gustav Brenner - auctioned his own vintage radios; he had held three earlier auctions of his own property in the preceding 12 months.
5. Lorna Pike - called bids at the Hartwell Food Bank (a registered charity) auction and accepted the $200 honorarium the food bank offered.""",
   "Lorna Pike",
   opts=["Anand Rao", "Mirela Constantin", "Tomas Castell", "Gustav Brenner", "Lorna Pike", NONE],
   card="- Anand Rao: the sheriff's deputy who sold seized vehicles\n- Mirela Constantin: the heir who auctioned her late aunt's furniture\n- Tomas Castell: the priest who called bids at the hospice gala\n- Gustav Brenner: the collector who auctioned his own vintage radios\n- Lorna Pike: the person who called bids at the food bank auction\n- none of these: none of the persons reviewed needed a licence",
   diff=2, twin=[("and accepted the $200 honorarium", "and declined the $200 honorarium")], twin_gold=NONE),

it("A16", "noul",
   "May the city grant Mr. Sadeghi the transfer of TR-118?",
   """Memo to file - Tobacco Retail Licensing Unit, City of Orlow
Applicant: Hamid Sadeghi, buyer of Corner Stop Market, 22 Birch Lane

The prior owner, Edna Paulk, held tobacco retail licence TR-118 for this location. Ms. Paulk closed the store to the public on January 5, 2025 for health reasons. Mr. Sadeghi bought the business, reopened it on June 15, 2025, and applied to transfer TR-118 to himself. The store's nearest public entrance is 850 feet (straight line) from the property line of Orlow Middle School and 1,150 feet from the school building itself.

Tobacco Retail Ordinance §6:
(a) No new tobacco retail licence shall be issued for premises within 1,000 feet of a school, measured in a straight line from the nearest point of the school's property line to the nearest public entrance of the premises.
(b) The renewal of an existing licence, or its transfer to the purchaser of the business, is not the issuance of a new licence.
(c) Subsection (b) does not apply if the premises were closed to the public for more than 180 consecutive days before the renewal or transfer.""",
   1,
   card="- new licence: any licence other than a renewal or a transfer to the buyer of the business; a renewal or transfer counts as new if the premises were closed to the public for more than 180 consecutive days\n- school buffer: no new licence within 1,000 feet of a school, measured from the school's property line to the nearest public entrance",
   diff=3, twin=[("reopened it on June 15, 2025", "reopened it on August 15, 2025")], twin_gold=0),

it("A17", "choice",
   "Which registration obligation applies to the pantry?",
   """Charitable Solicitation - registration inquiry (Commonwealth of Tarrin)
From: Board chair, St. Brigid Parish Food Pantry, Inc.

We are a separately incorporated social-service nonprofit affiliated with St. Brigid Parish. All our fundraising is done by volunteers. Last fiscal year (July-June) we received $19,000 in contributions. This fiscal year, a local newspaper story brought in a wave of gifts, and our running total passed $25,000 on August 14 (we're now at $26,500). We have never registered. Our treasurer thinks we're exempt as a church ministry.

Charitable Solicitation Act:
§3 A charitable organization must register with the Attorney General before soliciting contributions in the Commonwealth.
§4 The following are exempt from §3:
 (a) a religious congregation;
 (b) an organization that received $25,000 or less in contributions in its previous fiscal year and used no paid solicitor, except that such an organization must register within 30 days after the date on which its contributions in the current fiscal year exceed $25,000.
§5 The exemption in §4(a) does not extend to a separately incorporated school, hospital, or social-service agency affiliated with a religious congregation.""",
   "must register within 30 days after contributions exceed $25,000",
   opts=["exempt: no registration required", "must register before soliciting", "must register within 30 days after contributions exceed $25,000"],
   card="- exempt: no registration required: the organisation falls within an exemption that carries no registration duty\n- must register before soliciting: registration is required before any solicitation\n- must register within 30 days after contributions exceed $25,000: the organisation is exempt until its current-year contributions pass $25,000 and must then register within 30 days",
   diff=3),

it("A18", "noul",
   "Is the studio's service exempt from the cosmetology licence requirement?",
   """Customer support ticket #44812 - Board of Cosmetology
From: Adaeze Nwosu, owner, Crown & Coil Studio

I'm opening a studio that offers one service only: attaching human-hair extensions by braiding them into the client's natural hair (knotless braids). No relaxers, no dyes, no flat irons, no heat tools of any kind. Clients pay per session. Do I and my two braiders need cosmetology licences? A friend who owns a salon says anything involving extensions needs a licence.

Board response template, citing the Cosmetology Act:
§2 A cosmetology licence is required to perform any hair service for compensation.
§3(1) Exempt: natural hair braiding, provided no chemical treatments, dyes, or heat-based straightening are applied.
§3(2) "Natural hair braiding" includes twisting, wrapping, weaving, braiding, and locking of natural hair, and the attachment of human or synthetic hair extensions by braiding. It does not include the attachment of extensions by adhesive, bonding agents, or sewing onto a track or weft.""",
   1,
   card="- natural hair braiding: braiding, twisting, wrapping, weaving or locking natural hair, including attaching extensions by braiding; it excludes attaching extensions with adhesive, bonding agents, or by sewing onto a track or weft",
   diff=1),

it("A19", "choice",
   "Under Rule R-3, which classification code applies to Folio & Flame?",
   """KELMONT CITY - Business Licence Tax: classification review
Business: Folio & Flame, 7 Orchard Row (bookshop with a cafe counter and a wine bar)

Prior-year gross receipts (from the owner's filing):
 - new and used books: 40%
 - coffee, tea and pastries: 30%
 - wine sold by the glass for consumption on site: 30%
The shop holds an on-premises alcohol licence.

Classification Rule R-3:
(i) A business is classified under the code for the activity that produced the largest share of its gross receipts in the prior year.
(ii) If that largest share is under 40% of gross receipts, the business is classified as 5999 Miscellaneous retail instead.
(iii) Notwithstanding (i) and (ii), a business holding an on-premises alcohol licence is classified as 5813 Drinking places if receipts from alcohol exceed 30% of gross receipts.

The owner argues that the cafe side makes it an "eating place"; the city auditor's margin note reads "wine bar = 5813".""",
   "5942 Book stores",
   opts=["5411 Grocery stores", "5441 Candy and confectionery", "5461 Bakeries (retail)", "5812 Eating places",
         "5813 Drinking places", "5921 Liquor stores", "5942 Book stores", "5943 Stationery stores",
         "5945 Toy and hobby shops", "5994 News dealers", "5999 Miscellaneous retail", "7231 Beauty shops",
         "7299 Misc. personal services", "7832 Movie theatres", "7911 Dance studios",
         "7991 Physical fitness facilities", "8231 Libraries", "8299 Schools, n.e.c.",
         "8641 Civic and social associations", NONE],
   card="""- 5411 Grocery stores: retail sale of a general line of food for home preparation
- 5441 Candy and confectionery: retail sale of candy, nuts and confections
- 5461 Bakeries (retail): baking and selling bread, cakes and pastries on the premises
- 5812 Eating places: sale of prepared meals, snacks and non-alcoholic drinks
- 5813 Drinking places: sale of alcoholic drinks for consumption on the premises
- 5921 Liquor stores: retail sale of packaged alcoholic beverages
- 5942 Book stores: retail sale of new or used books
- 5943 Stationery stores: retail sale of stationery, office and school supplies
- 5945 Toy and hobby shops: retail sale of toys, games and hobby kits
- 5994 News dealers: retail sale of newspapers and magazines
- 5999 Miscellaneous retail: retail not elsewhere classified, and businesses whose largest activity is under 40% of receipts
- 7231 Beauty shops: hair, nail and skin care services
- 7299 Misc. personal services: personal services not elsewhere classified
- 7832 Movie theatres: exhibition of motion pictures
- 7911 Dance studios: dance instruction and dance halls
- 7991 Physical fitness facilities: gyms and fitness centres
- 8231 Libraries: lending libraries and reading rooms
- 8299 Schools, n.e.c.: instruction not elsewhere classified
- 8641 Civic and social associations: membership clubs and associations
- none of these: no listed code applies""",
   diff=3, twin=[("new and used books: 40%", "new and used books: 39%"),
                 ("for consumption on site: 30%", "for consumption on site: 31%")],
   twin_gold="5813 Drinking places"),

it("A20", "noul",
   "Does the Act require Keanu to hold a dealer licence?",
   """Q&A column - "Ask the Motor Vehicle Division", Brisk Valley Ledger

Reader question: "I'm Keanu Vasquez. In the last twelve months I sold seven cars through online listings. Three of them were family cars that had been registered in my own name for years. The rest I bought at dealer auctions or from private sellers and resold, usually within about two months, after fixing them up in my garage. I don't have a dealer licence. My brother-in-law says anyone who sells more than five cars a year is a dealer. Am I in trouble?"

Columnist's answer (quoting the Motor Vehicle Dealer Act):
§3(1) A person who sells, or offers for sale, more than five vehicles in any 12-month period must hold a dealer licence.
§3(2) A vehicle that was registered in the seller's own name for at least six months before the sale is not counted under subsection (1).
§3(3) A vehicle is counted when the sale is completed, whether or not it was advertised as a private sale.""",
   0,
   card="- counted vehicle: a vehicle the person sells or offers for sale, other than one registered in the seller's own name for at least six months before the sale",
   diff=1),

it("A21", "choice",
   "Which combination of credentials must Sentinel Trace hold to offer all three services?",
   """Compliance intake - Sentinel Trace Ltd. (Province of Doran)
Services Sentinel Trace offers to landlord clients:
1. Remote monitoring: staff in our control room watch live feeds from cameras at client buildings and phone the police or the fire service when they see an intrusion or fire. No staff go to the buildings.
2. Tenant screening reports compiled only from court records and credit bureau data.
3. "Residence verification": at a client's request, a staff member drives to an applicant's current address and watches it over two evenings to confirm the applicant actually lives there, then reports what was observed.

Doran Security Services Act:
§1 "Private investigation" means obtaining, for compensation, information about the identity, conduct, activities, or whereabouts of a person. It does not include the preparation of consumer reports solely from public records and credit bureau data.
§2 A Private Investigator licence is required to conduct private investigation.
§3 "Alarm monitoring" means remotely receiving signals or images from protected premises and dispatching police, fire, or other responders. An Alarm Monitoring registration is required for alarm monitoring.
§4 A Security Guard licence is required only for persons physically present at premises to protect persons or property.""",
   "Alarm Monitoring registration and Private Investigator licence",
   opts=["Alarm Monitoring registration only", "Private Investigator licence only",
         "Security Guard licence and Private Investigator licence", "no licence or registration",
         "Alarm Monitoring registration and Private Investigator licence"],
   card="- Alarm Monitoring registration only: only the registration for remote monitoring and dispatch\n- Private Investigator licence only: only the licence for private investigation\n- Alarm Monitoring registration and Private Investigator licence: both the monitoring registration and the investigator licence\n- Security Guard licence and Private Investigator licence: the on-site guard licence plus the investigator licence\n- no licence or registration: none of the services needs a credential",
   diff=2),

it("A22", "noul",
   "Was Mr. Ruiz required to hold a Master licence for the 9 August trip?",
   """Harbourmaster's incident file - Vessel "Kittiwake", Port Sallow
Operator: Owen Ruiz (owner; holds no Master licence)

On 9 August Mr. Ruiz took eight friends on a day trip to the Skerries aboard Kittiwake. Before the trip the group agreed how to cover the fuel, bait and mooring costs, which came to $900 in total: each of the eight friends paid Mr. Ruiz $100, and he paid the remaining $100 himself. None of the friends acted as crew. A patrol boat stopped Kittiwake near the harbour mouth and questioned whether the trip was an unlicensed charter.

Small Vessel Operators Regulation, reg. 11:
(1) A Master licence is required to operate a vessel carrying more than six passengers for hire.
(2) "Passenger" does not include the owner, a member of the crew, or a person who contributes only a pro-rata share of the actual expenses of the voyage.
(3) A person who pays more than an equal share of those expenses, or pays anything beyond actual expenses, is a passenger for hire.""",
   0,
   card="- passenger for hire: a person carried who is not the owner or crew and who pays more than an equal share of the voyage's actual expenses, or anything beyond actual expenses",
   diff=3, twin=[("each of the eight friends paid Mr. Ruiz $100, and he paid the remaining $100 himself",
                  "each of the eight friends paid Mr. Ruiz $112.50, which covered the whole amount")], twin_gold=1),

it("A23", "choice",
   "Which listed product falls outside the cottage food exemption?",
   """Farmers' market vendor application - Cottage Food review
Vendor: Wren Hollis, "Hollis Kitchen"
Products listed: sourdough loaves; pumpkin bread (a quick bread baked in loaf pans); apple pie (double crust); lemon meringue pie.
Expected annual sales: $18,000, all direct to consumers at the market.

Cottage Food Rule (excerpt):
1. A cottage food operator may sell foods that are not potentially hazardous directly to consumers without a food establishment licence, if gross annual sales do not exceed $50,000.
2. Potentially hazardous foods are those requiring time or temperature control for safety, including: cheesecakes; custard, cream, or meringue-topped pies; cream-filled pastries; cut melons; and garlic-in-oil mixtures.
3. Fruit pies without custard, cream, or meringue fillings or toppings are not potentially hazardous, except pumpkin and sweet-potato pies.
4. Breads, including quick breads made with fruit or vegetables, are not potentially hazardous.""",
   "lemon meringue pie",
   opts=["sourdough loaves", "pumpkin bread", "apple pie", "lemon meringue pie", NONE],
   card="- sourdough loaves: yeast-leavened bread loaves\n- pumpkin bread: a quick bread made with pumpkin and baked in loaf pans\n- apple pie: a double-crust fruit pie\n- lemon meringue pie: a lemon-filled pie with a meringue topping\n- none of these: every listed product may be sold under the cottage food rule",
   diff=1),

it("A24", "noul",
   "Does Rule 5.1 require a special-event permit for the film night?",
   """Email thread - Riverside Park special-event permit
From: Colm Brady (organiser, Riverside Film Night)
To: Parks Permits Office

We're projecting a film in Riverside Park (city land) on 22 August. Ticket sales are capped at 230, and we expect nearly all ticket holders to be there during the screening. We'll also have 12 food and craft vendors (one person staffing each stall), a 6-piece band playing during the interval, and 4 of our own volunteers running the gate and the projector. Everyone - vendors, band and volunteers - will be on site for the whole evening. Since we're under 250, I assume we don't need the special-event permit?

Parks Permits Office reply:
Under Parks Rule 5.1, a special-event permit is required for any event on city park land with an expected attendance of 250 or more persons. Attendance means all persons expected to be present at the event's peak time, including staff, volunteers, vendors, and performers. Please count accordingly and let us know.""",
   1,
   card="- attendance: every person expected to be present at the event's peak time, including staff, volunteers, vendors and performers",
   diff=2, twin=[("12 food and craft vendors", "8 food and craft vendors")], twin_gold=0),

it("A25", "choice",
   "What licensing does Dr. Moreau need for today's consult and prescription?",
   """Case note - Veterinary Board inquiry line
Caller: Dr. Ilse Moreau, DVM (licensed only in the State of Aldera)

Dr. Moreau examined "Biscuit", a 4-year-old spaniel, in person at her Aldera clinic 20 days ago and diagnosed an ear infection. The owners are now on holiday with Biscuit in the State of Brisa. Today they asked for a video follow-up; Dr. Moreau wants to do the consult and prescribe a 10-day course of an oral antibiotic (not a controlled substance).

Interstate Veterinary Practice Compact, Art. 3:
(1) A veterinarian providing care must be licensed in the state where the animal is located at the time of the service.
(2) Despite (1), a veterinarian who has examined the animal in person within the preceding 30 days, and has an existing veterinarian-client-patient relationship, may provide follow-up telehealth care under the licence of the state where that examination took place.
(3) Paragraph (2) does not authorise prescribing a controlled substance; any such prescription requires a licence from the state where the animal is located.""",
   "her Aldera licence is sufficient",
   opts=["her Aldera licence is sufficient", "a Brisa licence is required", "no veterinary licence is required", NONE],
   card="- her Aldera licence is sufficient: she may do the consult and the prescription under her home-state licence\n- a Brisa licence is required: she must hold a licence from the state where the dog now is\n- no veterinary licence is required: this kind of telehealth follow-up needs no licence at all\n- none of these: no listed option states the requirement",
   diff=2),

it("A26", "noul",
   "Did Mr. Lanh need an applicator licence for the 3 June application?",
   """Complaint intake - Department of Agriculture, Pesticide Section
Respondent: Victor Lanh

Mr. Lanh owns a duplex at 5 Sorrel Court. He lives in the upper unit; the lower unit is leased to a tenant under a one-year lease. On 3 June he sprayed a general-use broadleaf herbicide (not a restricted-use product) on the shared front lawn himself, without payment from anyone. The tenant complained about the smell. Mr. Lanh holds no applicator licence and says he "only treated his own grass".

Pesticide Applicator Act:
§7(1) A person must hold an applicator licence to apply any pesticide outdoors, except as provided in subsection (2).
§7(2) No licence is needed for a person applying a general-use pesticide on property that the person owns.
§7(3) The exemption in subsection (2) does not apply to property owned by the applicator that includes any dwelling unit leased to a tenant.""",
   1,
   card="- own-property exemption: no applicator licence is needed to apply a general-use pesticide on property the applicator owns, unless that property includes any dwelling unit leased to a tenant",
   diff=2),
]
