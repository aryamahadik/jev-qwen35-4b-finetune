"""Domain B: tenant protections (invented statutes)."""
from _h import it

NONE = "none of these"

ITEMS = [

it("B1", "noul",
   "Is the landlord liable for the double-deposit penalty under §8(3)?",
   """From: Carmen Ruiz-Oyelaran
To: Tenant Rights Clinic, Delford
Subject: Landlord kept my deposit - double penalty?

I moved out of Apt 3C at 17 Marlow Street on March 31. I couldn't get the keys back to the landlord until April 3 because he was away; I handed them to him in person that day. On April 2 I had already texted him my new address. His itemized statement and a cheque for part of my deposit were mailed on April 26.

Clinic intake sheet - Delford Residential Tenancy Act §8:
(1) Within 21 days after the later of (a) the date the tenant vacates or (b) the date the tenant returns the keys, the landlord must mail the tenant the balance of the security deposit with an itemized statement of deductions.
(2) If the tenant has not provided a forwarding address in writing, the 21-day period instead runs from the date a written forwarding address is provided. "Writing" includes email and text messages.
(3) A landlord who fails to comply with (1) or (2) forfeits the right to withhold any part of the deposit and is liable for a penalty equal to twice the deposit.""",
   1,
   card="- deposit deadline under §8: 21 days after the later of move-out or key return (or after a written forwarding address is given, if none was given); missing it triggers forfeiture and a penalty of twice the deposit",
   diff=2, twin=[("until April 3 because he was away", "until April 6 because he was away")], twin_gold=0),

it("B2", "choice",
   "What is the highest monthly rent the landlord may charge Joel from October 1, 2026?",
   """Advice request to the Lirwood Rent Board hotline (transcribed)
Tenant: Joel Amankwah, Apt 2B, 40 Tamsin Road. Current rent: $1,800 per month. The landlord's notice proposes $1,990 from October 1, 2026.

Building facts (from the Board's registry): certificate of occupancy first issued in 2014. Construction was partly funded by a city Workforce Housing grant in exchange for 20 years of income limits on half of the units.

Lirwood Rent Stabilization Ordinance:
§4(a) The annual rent increase for a covered unit may not exceed the lesser of (i) 5% plus the percentage change in the Consumer Price Index or (ii) 10%.
§4(b) For increases taking effect in 2026, the CPI change is 3.2%.
§5(a) Units first issued a certificate of occupancy within the previous 15 years are not covered units.
§5(b) The exemption in §5(a) does not apply to any unit in a building that received a public construction subsidy.""",
   "$1,947.60",
   opts=["$1,890.00", "$1,947.60", "$1,980.00", "$1,990.00", "no cap applies"],
   tpl="the highest lawful monthly rent from October 1, 2026 is {}",
   extra={"no cap applies": "the unit is not a covered unit, so the ordinance sets no limit on the increase"},
   diff=3, twin=[("Construction was partly funded by a city Workforce Housing grant in exchange for 20 years of income limits on half of the units.",
                  "Construction was financed entirely with a private bank loan.")], twin_gold="no cap applies"),

it("B3", "noul",
   "Can the landlord rely on the owner move-in ground against marguerite_64?",
   """Forum: Tenants of Calder County - Q&A board
Posted by marguerite_64

My landlord (he's 58) served me a notice saying he's ending my tenancy so his daughter can move in and live here - he wrote that she'll stay "at least three years". I'm 64 and I've lived in this flat for 11 years. Is he allowed to do this? I always pay on time.

Reply from volunteer moderator, quoting the Calder Just Cause Ordinance:
§6(a) A landlord may recover possession of a rental unit only for a just cause listed in this section.
§6(b)(4) Owner move-in: the owner, or the owner's parent or child, intends in good faith to occupy the unit as a principal residence for at least 36 consecutive months.
§6(c) A landlord may not recover possession under §6(b)(4) from a tenant who is 62 years of age or older and has resided in the unit for at least 10 years, unless the owner is also 62 years of age or older.""",
   0,
   card="- owner move-in protection: owner move-in is unavailable against a tenant aged 62 or older with at least 10 years in the unit, unless the owner is also 62 or older",
   diff=2, twin=[("(he's 58)", "(he's 63)")], twin_gold=1),

it("B4", "choice",
   "What is the minimum notice period that applies to Pier Nine's notice?",
   """Case file note - Harbor Province Tenancy Branch
Tenant: Ellery Dunmore (month-to-month tenancy at 18 Gull Terrace; tenancy began February 1, 2025)
Landlord: Pier Nine Holdings

Pier Nine Holdings served a notice to terminate the tenancy by regular mail. The notice was mailed on January 20, 2026. The landlord does not intend to convert the building to condominiums; it wants to rent the unit to a relative of one of its directors.

Residential Tenancies Act §14:
(1) To end a month-to-month tenancy, a landlord must give written notice of at least
 (a) 30 days, if the tenancy has lasted less than one year;
 (b) 60 days, if the tenancy has lasted one year or more;
 (c) 90 days, if the landlord intends to convert the building to condominium units, regardless of the length of the tenancy.
(2) The length of the tenancy is measured on the date the notice is served.
(3) A notice served by mail is deemed served on the date of mailing, but the minimum notice period is extended by five days.""",
   "35 days",
   opts=["30 days", "35 days", "60 days", "65 days", "90 days", "95 days"],
   tpl="the minimum notice period is {}",
   diff=2),

it("B5", "noul",
   "Did Barry's Thursday entry comply with §21?",
   """Text messages between tenant Anouk Heslin and landlord Barry Cole
Mon 9:12 AM - Anouk: Hi Barry, the kitchen faucet has started dripping. Can you fix it sometime this week?
Mon 9:40 AM - Barry: Will do.
Thu 7:40 AM - Barry: Coming by at 9:30 to fix the faucet.
Thu 9:30 AM - [Barry entered the unit with his key; Anouk was at work.]
Thu 12:05 PM - Anouk: You came in while I was out?? You only texted 2 hours before!

Oakmere Landlord and Tenant Code §21:
(a) Except in an emergency, a landlord may enter a dwelling unit only after giving the tenant at least 24 hours' written notice of the date and approximate time of entry. Text messages are written notice.
(b) "Emergency" means an imminent threat to persons or property, such as fire, flooding, or a gas leak.
(c) A tenant's request for a repair does not waive the notice requirement unless the tenant's request specifies a date and time for the landlord's entry.""",
   0,
   card="- lawful non-emergency entry: at least 24 hours' written notice of date and approximate time, unless the tenant's repair request itself specified a date and time for entry",
   diff=1),

it("B6", "choice",
   "How much may Sione deduct from rent for the water-heater repair?",
   """Tenant clinic intake - Norrby Housing Legal Aid
Tenant: Sione Tapueluelu; monthly rent $1,400.
Issue: the water heater stopped heating properly in late April; water is lukewarm at best. On May 2 Sione emailed the landlord a written repair request, which the landlord acknowledged receiving that day. The landlord did nothing. On May 18 Sione hired a licensed plumber, who replaced the heating element and thermostat for $1,650. This is the first time Sione has used the repair-and-deduct remedy.

Norrby Residential Tenancies Act §11:
(1) If a landlord fails to make a repair required by law within 14 days after receiving the tenant's written notice, the tenant may have the repair done and deduct the cost from rent.
(2) The amount deducted for any one repair may not exceed one month's rent.
(3) A tenant may use this section no more than twice in any 12-month period.""",
   "$1,400",
   opts=["nothing", "$700", "$1,400", "$1,650"],
   tpl="the tenant may deduct {} from rent",
   extra={"nothing": "the tenant may not deduct any amount from rent"},
   diff=2),

it("B7", "noul",
   "Does Nadia's notice meet §19's requirements for early termination?",
   """Letter to Westbrook Housing Advocates
From: Nadia Ferrante, tenant at 9 Lowry Court (lease runs through next March)

My sister Carla has lived with me in the flat for two years, with the landlord's knowledge; she isn't on the lease. In February her ex-partner assaulted her in our building's stairwell. On March 1 a certified victim advocate at the county's family justice centre gave her a signed statement describing the assault. We haven't gone to court for a protective order. On May 15 I gave the landlord written notice that I'm ending my lease in 30 days under the domestic violence provision and attached the advocate's statement. The landlord says it's "not valid". Who's right?

Westbrook Residential Tenancy Act §19:
(1) A tenant may terminate a lease by giving the landlord at least 30 days' written notice if the tenant or a household member is a victim of domestic violence, and the notice is accompanied by either (a) a copy of a protective order, or (b) a signed statement by a qualified third party that is dated no more than 60 days before the notice is given.
(2) "Household member" means any person who lawfully resides in the dwelling unit.
(3) "Qualified third party" means a law-enforcement officer, a licensed health-care provider, or a certified victim advocate.""",
   0,
   card="- valid early-termination notice: at least 30 days' written notice, with a protective order or a qualified third party's signed statement dated no more than 60 days before the notice",
   diff=2),

it("B8", "choice",
   "What is the largest late fee the landlord may lawfully charge for June?",
   """Tenant helpline chat log - Pellworth Rental Housing Office
Tenant: My rent is $2,300, due on the 1st. For June I paid online at 4:10 p.m. on Monday, June 8. My landlord has added a $100 late fee. Is that allowed?
Agent: Let me pull up the rule. June 1 was a Monday and June 6 was a Saturday; there were no public holidays that week.

Pellworth Residential Lease Standards §7:
(a) Rent is not late until the end of the fifth day following its due date. If that fifth day falls on a Saturday, Sunday, or legal holiday, rent is not late until the end of the next business day.
(b) Once rent is late, the landlord may charge a single late fee not exceeding the greater of $50 or 5% of the monthly rent, but in no case more than $100.
(c) Any late-fee clause exceeding these limits is unenforceable to the extent of the excess.""",
   "$0",
   opts=["$0", "$50", "$100", "$115"],
   tpl="the largest lawful late fee for June is {}",
   extra={"$0": "no late fee may be charged for June"},
   diff=3, twin=[("on Monday, June 8", "on Tuesday, June 9")], twin_gold="$100"),

it("B9", "noul",
   "Does the §31(a) presumption of retaliation apply to the landlord's notice?",
   """Hearing memo - Grantley Housing Court, Case 26-LT-0913
Tenant: Ravi Okonjo | Landlord: Fenwick Row Apartments LLC

Timeline:
- Feb 10: the tenant filed a housing-code complaint about mould with the city; an inspector cited the landlord on Feb 24.
- April 1: April rent ($1,250) fell due. The tenant did not pay.
- April 9: the landlord served a notice to pay rent or quit.
- The tenant raises retaliation as a defence; the landlord says nonpayment speaks for itself.

Grantley Tenant Protection Act §31:
(a) If a landlord serves a notice to quit, or a notice of rent increase, within 180 days after the tenant files a complaint with a government agency about the condition of the premises, the notice is presumed to be retaliatory.
(b) The presumption in (a) does not apply to a notice to quit for nonpayment of rent, if the rent was due and unpaid for more than 10 days before the notice was served.""",
   1,
   card="- retaliation presumption: a notice to quit or rent-increase notice within 180 days after a tenant's condition complaint to an agency is presumed retaliatory, except a nonpayment notice served after rent was due and unpaid for more than 10 days",
   diff=2, twin=[("April 9: the landlord served", "April 14: the landlord served")], twin_gold=0),

it("B10", "choice",
   "How much relocation assistance is Sadie's household owed?",
   """From: Sadie Kwan, tenant, 6 Arbor Mews
To: Relocation Assistance Office, City of Tessaly

We have been told we must leave because the owner is withdrawing the building from the rental market (a no-fault eviction). My household: me (40), my son (8), and my father (70), who has lived with us the whole time. We moved in 10 months ago. How much relocation assistance are we owed? The owner's letter mentions "$4,500 per unit".

Tessaly Relocation Assistance Ordinance §3:
(1) A tenant household displaced by a no-fault eviction receives a base payment of $4,500 per unit.
(2) If any member of the household is 62 or older, disabled, or a minor child, the household receives one additional payment of $1,500. No household receives more than one additional payment.
(3) A household that has resided in the unit for less than 12 months receives 50% of the base payment, but the full additional payment under (2).""",
   "$3,750",
   opts=["$1,500", "$2,250", "$3,000", "$3,750", "$6,000"],
   tpl="the household is owed {} in total",
   diff=2),

it("B11", "noul",
   "Does the Code require the landlord to drop the $400 pet deposit for Pip?",
   """Email to the property manager - Quill Street Lofts
From: tenant Bastien Aroyo

I've attached a letter about my emotional support dog, Pip. It's from Hanne Svoboda, LCSW, the licensed clinical social worker who has treated me for anxiety for the past two years. The letter states that I have a disability and that Pip alleviates symptoms of it. Your office still billed me the $400 pet deposit. Please remove it.

Excerpt from the Quill Street Lofts lease and the Vardon Fair Housing Code:
Lease §12: A refundable pet deposit of $400 applies to all animals.
Code §5(1): A housing provider may not charge a pet deposit or pet fee for an assistance animal.
Code §5(2): A housing provider may require reliable documentation of the tenant's disability-related need for the animal. Documentation is reliable if it comes from a health-care professional with personal knowledge of the tenant's condition.
Code §5(3): A certificate or letter obtained solely by purchase from a website, without an individualized assessment by a health-care professional, is not reliable documentation.
Code §5(4): A lease term inconsistent with this section is void to the extent of the inconsistency.""",
   1,
   card="- reliable documentation: a statement from a health-care professional with personal knowledge of the tenant's condition; a letter bought from a website without an individualized assessment does not qualify\n- assistance animal rule: no pet deposit or pet fee may be charged for an assistance animal",
   diff=1),

it("B12", "choice",
   "Which logged reading shows a violation of §27-2?",
   """Inspection worksheet - Varrow City Housing Code, heat complaint
Unit: 5F, 221 Loom Street. Tenant-logged readings verified against the landlord's thermostat logs:
R1 - Oct 3, 2:00 p.m.: indoor 66°F; outdoor 58°F
R2 - Nov 12, 11:30 p.m.: indoor 63°F; outdoor 30°F
R3 - May 20, 7:00 a.m.: indoor 60°F; outdoor 41°F
R4 - Dec 2, 5:30 a.m.: indoor 61°F; outdoor 22°F

Housing Code §27-2 (Heat season):
(a) From October 1 through May 15, the owner must maintain:
 (1) between 6:00 a.m. and 10:00 p.m., an indoor temperature of at least 68°F whenever the outdoor temperature falls below 55°F; and
 (2) between 10:00 p.m. and 6:00 a.m., an indoor temperature of at least 62°F, regardless of the outdoor temperature.
(b) No heat requirement applies outside the heat season.
The tenant's complaint lists every reading below 68°F as a violation.""",
   "R4",
   opts=["R1", "R2", "R3", "R4", NONE],
   card="- R1: the October 3, 2:00 p.m. reading\n- R2: the November 12, 11:30 p.m. reading\n- R3: the May 20, 7:00 a.m. reading\n- R4: the December 2, 5:30 a.m. reading\n- none of these: no logged reading shows a violation",
   diff=2, twin=[("R4 - Dec 2, 5:30 a.m.: indoor 61°F", "R4 - Dec 2, 5:30 a.m.: indoor 62°F")], twin_gold=NONE),

it("B13", "noul",
   "Is the automatic renewal clause enforceable against Imogen?",
   """Clause excerpt and correspondence - Imogen Tarrant, tenant, 3 Sedge Walk
Lease (one-year term ending July 31):
"17. Automatic renewal. This lease renews automatically for a further one-year term unless Tenant gives written notice of non-renewal on or before June 1."
Landlord's reminder email to Imogen, sent May 10: "Reminder: your lease renews automatically on August 1 unless you notify us by June 1 that you will not renew."
Imogen gave written notice of non-renewal on June 20. The landlord says she is bound for another year.

Esterly Residential Lease Act §9:
An automatic renewal clause in a residential lease with a term of one year or more is enforceable against the tenant only if the landlord gives the tenant written notice, not less than 15 days and not more than 30 days before the date by which the tenant must give notice of non-renewal, reminding the tenant of that date and of the automatic renewal.""",
   1,
   card="- enforceable automatic renewal: the landlord sent a written reminder of the renewal and the tenant's deadline no fewer than 15 and no more than 30 days before that deadline",
   diff=2, twin=[("sent May 10", "sent April 20")], twin_gold=0),

it("B14", "choice",
   "What is the maximum total deposit this landlord may lawfully demand?",
   """Posted on the Ferncliff Renters' Association board
Q: My new landlord wants a $4,000 deposit on an unfurnished one-bedroom at $2,000 a month because I have a cat. She owns three rental units in town. Is that legal?

A (from a volunteer, quoting Ferncliff Security Deposit Law §2):
(1) A landlord may not demand a security deposit exceeding one month's rent for an unfurnished unit or two months' rent for a furnished unit.
(2) If the tenant keeps a pet, the landlord may demand an additional deposit of up to one-half month's rent.
(3) A landlord who owns no more than two residential rental units may demand up to two months' rent under (1), whether or not the unit is furnished; (2) still applies.
Hope this helps - check whether she counts as a small landlord.""",
   "$3,000",
   opts=["$1,000", "$2,000", "$2,500", "$3,000", NONE],
   tpl="the maximum lawful total deposit is {}",
   extra={NONE: "no listed amount is the maximum lawful total deposit"},
   diff=2),

it("B15", "noul",
   "Does §12 stop the March 15 termination from taking effect?",
   """Legal aid screening form - Ostrand Eviction Defence Project
Client: Omar Beltane, 14 Heron Street (City of Ostrand)
Notice: no-fault "owner move-in" termination, effective March 15 (the school year runs September to June).
Household: Omar; his wife Leila; their daughter Mina (9), enrolled at Crestfield Elementary in the neighbouring town of Dunmere (they chose it for its language programme). Omar drives a school bus for the Ostrand Unified district; Leila works at a bank.

Ostrand Tenant Protections §12:
(a) A no-fault termination of tenancy may not take effect during the school year if a child under 18 or an educator resides in the unit and the child attends, or the educator works at, a school located in the City of Ostrand.
(b) "Educator" means a person employed at a school as a teacher, classroom aide, counsellor, or administrator.""",
   0,
   card="- school-year protection: a no-fault termination cannot take effect during the school year if a resident child attends, or a resident educator works at, a school inside the City of Ostrand\n- educator: a person employed at a school as a teacher, classroom aide, counsellor or administrator",
   diff=2),

it("B16", "choice",
   "On September 15, what is the legal status of Wes's occupancy?",
   """Letter from the landlord's agent (excerpt) and receipt
Tenant: Wes Harrow. His fixed-term lease for 12 Kiln Lane ended August 31 and he has not moved out. On September 3 he delivered a cheque for $1,500, the old monthly rent. The agent deposited it and issued a receipt that reads: "Received from W. Harrow $1,500 - accepted for use and occupancy only; no new tenancy is created."

Dunmore Tenancy Act §40:
(1) A tenant who remains in possession after the tenancy ends is a holdover and owes, for each day of occupancy, one-thirtieth of the last monthly rent.
(2) If the landlord accepts rent for a period after the tenancy ends, a new month-to-month tenancy is created on the terms of the old lease, unless the landlord states in writing, at the time of acceptance, that the payment is accepted for use and occupancy only.
(3) A fixed-term lease never renews by operation of law.""",
   "holdover occupancy with no tenancy",
   opts=["holdover occupancy with no tenancy", "a new month-to-month tenancy", "the original fixed-term lease continues"],
   card="- a new month-to-month tenancy: acceptance of rent created a periodic tenancy on the old lease terms\n- holdover occupancy with no tenancy: the occupant remains without any tenancy and owes daily use-and-occupancy charges\n- the original fixed-term lease continues: the expired lease is still in force",
   diff=2),

it("B17", "noul",
   "May management lawfully require Mateo to remove the dish?",
   """Building management notice dispute - Coraline Towers, Unit 1204
Tenant Mateo Grau installed a 0.9-metre satellite dish on a weighted tripod on the building's shared rooftop terrace, which all residents may use. Nothing was drilled or bolted into the roof or walls. Management has ordered him to remove it within 7 days. Mateo says federal-style "dish rights" mean they can't touch it.

Aurelian Telecommunications Access Act §3:
(1) A tenant may install a satellite dish of 1 metre or less in diameter, without the landlord's consent, in any area within the tenant's exclusive use or control, such as a private balcony or patio.
(2) A landlord may not prohibit an installation permitted by (1), but may require that it not penetrate exterior walls or the roof.
(3) Nothing in this section entitles a tenant to install equipment in common areas.""",
   1,
   card="- protected dish installation: a dish of 1 metre or less placed in an area within the tenant's exclusive use or control; common areas are not covered",
   diff=1),

it("B18", "choice",
   "What is the total amount the landlord may lawfully deduct?",
   """Deposit dispute worksheet - Halsey County Small Claims mediation
Tenancy: 4 years; tenant Juno Petrakis; deposit $3,000; all rent paid.
Landlord's claimed deductions:
- Carpet replacement: $3,000. The carpet was installed new seven years before move-out; the tenant's dog chewed and stained it beyond repair.
- Cleaning: $150 - oven and bathroom left heavily soiled (photos agreed by both sides).
- Repainting all rooms: $900 - walls showed normal scuffs and fading after four years; no holes or unapproved colours.

Halsey Residential Deposit Rules:
R1. A landlord may deduct only for unpaid rent, cleaning needed to return the unit to its move-in level of cleanliness, and damage beyond ordinary wear and tear.
R2. Fading, minor scuffs, and paint wear from normal use are ordinary wear and tear.
R3. For damaged items with a limited useful life, the tenant is liable only for the remaining useful life, prorated. Carpet has a useful life of 10 years.""",
   "$1,050",
   opts=["$150", "$900", "$1,050", "$1,950", "$3,150", "$4,050"],
   tpl="the landlord may lawfully deduct {} in total",
   diff=3, twin=[("installed new seven years before move-out", "installed new four years before move-out")], twin_gold="$1,950"),

it("B19", "noul",
   "Was Luca's May 10 rescission effective?",
   """Email - Luca Bertin to the Lowtown Tenants' Union
On April 1 I signed a buyout agreement with my landlord: $12,000 to move out of 7 Ferry Street. The agreement had the required notice about my right to talk to a lawyer. I moved out on May 1, returned the keys, and received the money. Now I regret it - the new place is awful - and on May 10 I emailed the landlord to rescind. I'm ready to pay the money back. Is that valid?

Lowtown Buyout Ordinance §4:
(a) A buyout agreement must be in writing and must advise the tenant of the right to consult an attorney.
(b) A tenant may rescind a buyout agreement at any time up to 45 days after signing it by giving written notice to the landlord.
(c) The right in (b) ends once the tenant has vacated the unit.
(d) A tenant who rescinds must repay any buyout money received.""",
   0,
   card="- rescission right: written notice within 45 days after signing a buyout agreement, available only while the tenant has not yet vacated the unit",
   diff=2),

it("B20", "choice",
   "How much must the landlord refund to Tove?",
   """Complaint to the Rennick Consumer & Housing Office
Applicant: Tove Lindgren. Unit: 22 Alder Court, #4.

On March 3 I applied and gave the landlord my portable tenant-screening report, which had been prepared 25 days earlier by an approved agency. The landlord ran his own screening anyway (his agency charged him $32) and charged me a $40 application fee. What refund am I owed?

Rennick Tenant Screening Act §6:
(1) An application fee may not exceed the landlord's actual cost of screening the applicant, and may never exceed $45.
(2) A landlord may not charge any application fee to an applicant who provides a portable screening report prepared within the previous 30 days.
(3) Any amount charged in excess of what this section allows must be refunded.""",
   "refund the full $40",
   opts=["refund nothing", "refund $8", "refund $13", "refund the full $40"],
   card="- refund nothing: the landlord may keep the whole $40 fee\n- refund $8: the landlord must return $8 of the fee\n- refund $13: the landlord must return $13 of the fee\n- refund the full $40: the landlord must return the entire $40 fee",
   diff=2),

it("B21", "noul",
   "Did the September 20 lock change violate §14?",
   """Case summary - Vellan Housing Tribunal
Tenant: Imre Szabo, 3 Pine Yard. Rent $900, due on the 1st; September rent unpaid.
- Sept 1: rent due, not paid.
- Sept 1 (evening): the landlord posted on the door, and emailed, a "Notice of Belief of Abandonment" stating he believed the unit was abandoned.
- Sept 18: Imre emailed back: "I'm in hospital after an accident, I'll be home soon - please don't touch my things."
- Sept 20: the landlord changed the locks and boxed up Imre's belongings.

Vellan Residential Tenancies Act §14:
(1) A landlord may not change the locks of an occupied unit or remove a tenant's belongings except under a court order.
(2) A unit is deemed abandoned, and (1) does not apply, if (a) rent has been unpaid for at least 15 days, (b) the landlord has given written notice of belief of abandonment, and (c) the tenant has not responded in writing within 18 days after that notice was given.""",
   1,
   card="- deemed abandonment: rent unpaid at least 15 days, written notice of belief of abandonment given, and no written response from the tenant within 18 days after that notice",
   diff=2),

it("B22", "choice",
   "On what date does Sgt. Moon's lease termination take effect?",
   """Tenant services ticket - Harbor Province Military Liaison Office
Tenant: Sgt. Delia Moon, 41 Beacon Row. Rent $1,650, due on the 1st of each month.
Sgt. Moon received permanent-change-of-station orders and hand-delivered written notice of termination, with a copy of her orders, to her landlord on August 14. She asks when her lease obligations end and how much rent she will owe.

Service Members' Tenancy Protection Act §5:
(1) A tenant who enters military service or receives permanent-change-of-station orders may terminate a residential lease by delivering written notice and a copy of the orders to the landlord.
(2) For a lease with monthly rent, termination takes effect 30 days after the first date on which the next rental payment is due after the notice is delivered.
(3) Rent is owed through the effective date of termination, prorated daily.""",
   "October 1",
   opts=["August 14", "August 31", "September 1", "September 13", "September 30", "October 1", "October 14", "November 1"],
   tpl="the termination takes effect on {}",
   diff=2),

it("B23", "noul",
   "May Parnell Holdings pass the boiler cost through to tenants?",
   """Rent Board petition summary - Kestrel Park Rent Stabilization
Owner: Parnell Holdings. Building: 90 Ivy Street (24 units).
The owner petitions to pass through the $96,000 cost of a new central boiler, installed this spring, at $33 per month per unit. The boiler has a useful life of 20 years and serves all units. City inspectors cited the building for inadequate heat 14 months before the petition was filed, and the old boiler was replaced in response to that citation.

Rent Stabilization Regulation 8:
(a) A capital improvement cost may be passed through to tenants only if the improvement has a useful life of at least 5 years and primarily benefits the tenants.
(b) The pass-through may not exceed $50 per unit per month and must be amortized over the improvement's useful life.
(c) No pass-through is allowed for work needed to correct a housing-code violation cited within the 2 years before the petition.""",
   0,
   card="- allowable pass-through: an improvement with a useful life of at least 5 years that primarily benefits tenants, capped at $50 per unit per month, and not work needed to correct a code violation cited within the 2 years before the petition",
   diff=1),

it("B24", "choice",
   "Which guest may management treat as an unauthorized occupant?",
   """Lease compliance review - Maple Court Apartments, Unit 7
The lease says: "Any guest staying more than 7 consecutive days is an unauthorized occupant." Management's guest log for the past 12 months:
- Priya (the tenant's sister): longest continuous stay 10 days; 25 days in total.
- Tomasz (the tenant's friend): longest continuous stay 14 days; 28 days in total.
- Wen (the tenant's cousin): longest continuous stay 12 days; 31 days in total.

Vessex Residential Tenancy Act §22:
(1) A landlord may not restrict a tenant's guests from staying up to 14 consecutive days, or up to 30 days in total in any 12-month period.
(2) A lease term that treats a guest as an unauthorized occupant within the limits in (1) is void to that extent.
(3) A guest who exceeds either limit in (1) may be treated as an unauthorized occupant.""",
   "Wen",
   opts=["Priya", "Tomasz", "Wen", NONE],
   card="- Priya: the tenant's sister\n- Tomasz: the tenant's friend\n- Wen: the tenant's cousin\n- none of these: no guest in the log may be treated as an unauthorized occupant",
   diff=2),

it("B25", "noul",
   "Is Esther eligible for the Right to Counsel program?",
   """Eligibility screening - Brightwater Right to Counsel Program
Applicant: Esther Vandermolen, facing eviction from 51 Coral Street.
Household at the address: Esther; her husband Piet; their two children (ages 6 and 11); and a lodger, Kofi, who rents a room from them and is not related to the family.
Annual income: Esther $31,400; Piet $32,500; Kofi $28,000.

Program Rules:
1. An applicant is eligible if household income does not exceed 200% of the poverty guideline for the household size.
2. "Household" means the applicant and all persons related to the applicant by blood, marriage, or adoption who live with the applicant. Only the income of household members counts.
3. Poverty guidelines (annual): 1 person $15,650; 2 persons $21,150; 3 persons $26,650; 4 persons $32,150; 5 persons $37,650.""",
   1,
   card="- household: the applicant plus everyone related by blood, marriage or adoption who lives with the applicant; only their income counts\n- eligibility: household income at or below 200% of the poverty guideline for the household size",
   diff=2),

it("B26", "choice",
   "How much rent can Ruth recover under §15?",
   """Small claims filing summary - Tenant v. Landlord
Tenant Ruth Okwu rented a basement flat at 8 Drayton Close for 20 months at $1,100 a month and paid every month. The basement has no occupancy permit for residential use. Before she signed the lease, the landlord told her in person that "the basement isn't officially permitted, but it's safe." Nothing about the permit status appears in the lease or in any other document. Ruth filed her claim the week after she moved out.

Drayton Borough Housing Code §15:
(1) If a landlord rents a dwelling unit that lacks a required occupancy permit, the tenant may recover all rent paid for the 12 months preceding the claim.
(2) Recovery under (1) is not available if, before the lease was signed, the landlord disclosed in writing that the unit lacked the permit and the tenant acknowledged the disclosure in writing.""",
   "$13,200",
   opts=["$0", "$1,100", "$13,200", "$22,000"],
   tpl="Ruth can recover {}",
   diff=2),
]
