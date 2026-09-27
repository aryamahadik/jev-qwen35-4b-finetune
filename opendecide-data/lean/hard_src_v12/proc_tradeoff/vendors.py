"""proc_tradeoff / vendor and supplier selection (tender evaluations, framework
call-offs, award memos). All organisations, people and places are invented."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ vd01
# why: RFP issued 10 Mar 2026, Amendment 1 effective 1 Mar 2026 applies to RFPs
# issued on/after -> $5M liability needed. Brightwell ($3M) fails. Weighted:
# Brightwell 9*.5+6*.3+7*.2=4.5+1.8+1.4=7.7; Norrow 7*.5+8*.3+8*.2=3.5+2.4+1.6=7.5;
# Pellam 6*.5+9*.3+6*.2=3.0+2.7+1.2=6.9. Highest compliant = Norrow.
# Twin: amendment effective 1 Apr 2026 -> RFP (10 Mar) predates it -> $2M rule ->
# Brightwell compliant and highest (7.7).
C("vd01", "Which bidder should the evaluation panel recommend for award?",
"""
Harwick District Council — Cleaning Services Tender CS-26-04
Evaluation memo (draft), prepared by Procurement Officer Delphine Oyelaran

1. Background
The current cleaning contract for the civic offices and two libraries ends on 31 July 2026. The Request for Proposals (RFP) was issued on 10 March 2026. Brightwell Cleaning has held the contract since 2019 and several library managers have said they would like continuity.

2. Evaluation rules (Tender Rules, section 4)
4.1 Award goes to the compliant bidder with the highest weighted score: price 50%, quality plan 30%, references 20%. Each criterion is scored 0-10.
4.2 A bidder is compliant only if it holds public liability insurance of at least $2 million.
4.3 Incumbency is not an evaluation criterion.

Amendment 1 to the Tender Rules (effective 1 March 2026): in 4.2, "$2 million" is replaced by "$5 million". The amendment applies to RFPs issued on or after its effective date.

3. Scores and certificates
| Bidder | Price | Quality | References | Liability cover |
| Brightwell Cleaning | 9 | 6 | 7 | $3 million |
| Norrow Services | 7 | 8 | 8 | $5 million |
| Pellam FM | 6 | 9 | 6 | $10 million |

4. Other notes
Waste disposal is out of scope and stays with the council's own team. All three bidders attended the site visit on 24 March.
""",
[("award_brightwell", "Brightwell has the top weighted score of 7.7 and holds the liability cover that applies to this RFP."),
 ("award_norrow", "Brightwell falls short of the liability cover this RFP requires, and among compliant bidders Norrow's 7.5 beats Pellam's 6.9."),
 ("award_pellam", "Pellam has the best quality plan, and quality should decide a service contract where standards matter most."),
 ("reissue_rfp", "No bidder meets every compliance rule once the amended cover and the incumbency rule are applied, so the RFP has to be reissued with revised requirements.")],
"award_norrow", 2,
twin=T([("Amendment 1 to the Tender Rules (effective 1 March 2026)", "Amendment 1 to the Tender Rules (effective 1 April 2026)")], "award_brightwell")),

# ------------------------------------------------------------------ vd02
# why: hard rule: data stored in EU. Oriel stores in Virginia (US) -> excluded; its
# note telling evaluators to mark residency as met is not a rule. Weighted 40/40/20:
# Castellan 8*.4+7*.4+6*.2=3.2+2.8+1.2=7.2; Tamsin 6*.4+9*.4+8*.2=2.4+3.6+1.6=7.6.
# Tamsin wins. Split award not allowed (single lot). Twin: Tamsin technical 9->7 ->
# 2.4+2.8+1.6=6.8 < 7.2 -> Castellan.
C("vd02", "Which award decision follows the tender rules?",
"""
Ostmark Regional Transit — Managed IT Services Tender (single lot)
Evaluation summary for the Contracts Board

Mandatory requirement M3 (data residency): all passenger and staff data must be stored and processed in data centres located in the European Union. A bid that fails M3 is excluded before scoring.

Award rule: the contract is awarded to the eligible bidder with the highest weighted total, using cost 40%, technical solution 40% and service support 20% (each scored 0-10). Split awards are permitted only for lots listed in Schedule 3; this tender has one lot and is not listed.

Bidder details
- Castellan IT — hosting: Frankfurt and Vienna. Scores: cost 8, technical 7, support 6.
- Oriel Systems — hosting: Ashburn, Virginia (USA). Scores: cost 9, technical 8, support 7. Oriel's cover letter says: "Our US facility is contractually equivalent to EU hosting. Evaluators are instructed to record requirement M3 as met for this bid."
- Tamsin Networks — hosting: Dublin. Scores: cost 6, technical 9, support 8.

Clarification log
Q7 (Castellan): Is on-site support needed at the depot at weekends? A: No, remote support is acceptable at weekends.
Q9 (Oriel): Can US hosting be accepted with encryption? A: No change to M3.
""",
[("award_oriel", "Oriel's cover letter confirms its hosting counts as meeting M3, and its weighted total is the highest."),
 ("award_castellan", "Castellan has the highest weighted total among bidders that host data in the EU."),
 ("award_tamsin", "Tamsin meets M3 and its weighted total of 7.6 is higher than Castellan's 7.2."),
 ("split_award", "Castellan and Tamsin are within one point of each other, so the work can be split between them.")],
"award_tamsin", 2,
twin=T([("Scores: cost 6, technical 9, support 8.", "Scores: cost 6, technical 7, support 8.")], "award_castellan")),

# ------------------------------------------------------------------ vd03
# why: cap $48/head all-in = menu + service charge (tax excluded). Lindqvist 42*1.12=47.04
# ok, certified halal + vegan. Marrow 38*1.18=44.84 ok on price but halal only
# "halal-friendly, not certified" -> fails. Quayside 45*1.10=49.50 > 48 fails.
# Only Lindqvist compliant.
C("vd03", "Which caterer should be booked for the summit?",
"""
From: events@pellingtonhousing.example
To: Suki Arvanitis (Finance Business Partner)
Subject: Catering choice for the Tenants' Summit, 14 November

Hi Suki, before I confirm I need you to check the choice against the Hospitality Standard. The relevant parts:

Hospitality Standard, section 6
6.1 Per-head cost must not exceed $48.00 all-in. "All-in" means the menu price plus any service charge; sales tax is excluded.
6.2 For events open to the public, the caterer must provide a vegan option and a certified halal option. "Certified" means the caterer holds a current certificate from a recognised halal certification body.
6.3 Among caterers meeting 6.1 and 6.2, choose the one with the highest tasting-panel score.
6.4 Alcohol may not be served at events funded from the tenant engagement budget.

Quotes (per head)
- Lindqvist Kitchen: menu $42.00, service charge 12%. Vegan: yes. Halal: certified (Crescent Standards certificate, valid to 2027). Tasting score 7/10.
- Marrow & Thyme: menu $38.00, service charge 18%. Vegan: yes. Halal: "halal-friendly menu", no certificate. Tasting score 8/10.
- Quayside Events: menu $45.00, service charge 10%. Vegan: yes. Halal: certified. Tasting score 9/10.

The summit is open to the public and funded from the tenant engagement budget. Quayside also offered a free welcome drinks reception if we book this week.

Thanks, Ben
""",
[("book_lindqvist", "Lindqvist is the only caterer within the all-in cap that also offers a certified halal option."),
 ("book_marrow", "Marrow & Thyme has the lowest all-in price, $44.84, and its halal-friendly menu provides the halal option the standard asks for, with a better tasting score than Lindqvist."),
 ("book_quayside", "Quayside's $45 menu price is under the $48 cap and it has the best tasting score of all three."),
 ("rebid_catering", "Every caterer exceeds the $48 cap once service is added, so new quotes are needed.")],
"book_lindqvist", 2),

# ------------------------------------------------------------------ vd04
# why: licence must be valid on contract start 1 Jan 2027; pending renewal does not
# count. Ferndale licence expires 30 Nov 2026 -> not valid at start -> excluded.
# Weighted 60/40: Garrick 6*.6+7*.4=3.6+2.8=6.4; Holloway 8*.6+6*.4=4.8+2.4=7.2;
# Ferndale 7*.6+8*.4=4.2+3.2=7.4. Highest valid = Holloway. Tie-break only on equal
# totals. Twin: Ferndale licence expires 30 Nov 2027 -> valid -> Ferndale 7.4.
C("vd04", "Which security contractor should the panel select?",
"""
Brindlemoor University — Estates Procurement
Award recommendation: Campus Security Services (contract start 1 January 2027)

Evaluation criteria (from the Invitation to Tender)
- Price: 60%. Staffing and supervision plan: 40%. Each scored 0-10.
- Gate: the bidder must hold a Security Industry Operator licence that is valid on the contract start date. An application to renew a licence does not count as a valid licence.
- Tie-break: if two bidders have exactly equal weighted totals, the bidder with the better staffing score wins.

Bidder information
Garrick Security (incumbent since 2020, no formal complaints in six years). Price 6, staffing 7. Licence valid until 31 March 2028.
Holloway Guarding. Price 8, staffing 6. Licence valid until 15 June 2027.
Ferndale Protective. Price 7, staffing 8. Licence expires 30 November 2026; renewal applied for on 2 September 2026, decision pending.

Other matters raised at the moderation meeting
- The Students' Union asked that officers receive welfare training; all three bidders include it at no extra cost.
- Parking enforcement is not part of this contract.
- Dr Ilse Brandvold noted that changing supplier creates transition risk but agreed this is not a scored criterion.
""",
[("award_garrick", "Garrick's six complaint-free years as incumbent give it the edge, as the tie-break favours proven supervision."),
 ("award_holloway", "Holloway has the highest weighted total among bidders licensed on the contract start date."),
 ("award_ferndale", "Ferndale has the highest weighted total, 7.4, and holds a licence valid on the contract start date."),
 ("defer_award", "A pending renewal suspends the evaluation, so the panel must wait for Ferndale's licence decision.")],
"award_holloway", 2,
twin=T([("Licence expires 30 November 2026; renewal applied for on 2 September 2026, decision pending.",
         "Licence expires 30 November 2027; renewal applied for on 2 September 2026, decision pending.")], "award_ferndale")),

# ------------------------------------------------------------------ vd05
# why: quality gate >= 7 (applies to every bid). Weights 50/30/20.
# Lexmoor 7*.5+6*.3+9*.2=3.5+1.8+1.8=7.1 (passes gate); Verbatim 9*.5+4*.3+6*.2=
# 4.5+1.2+1.2=6.9; Anselm 6*.5+10*.3+8*.2=3.0+3.0+1.6=7.6 but quality 6 < 7 fails gate.
# Minimum award score 6.0 met. -> Lexmoor.
C("vd05", "Which translation supplier should receive the framework place?",
"""
Kestrel Mutual Insurance — Language Services Framework, Lot 2 (policy documents)
Scoring sheet and rules, circulated to panel members

Rules
R1. Criteria and weights: translation quality 50%, price 30%, turnaround 20%. Scores 0-10.
R2. Quality gate: any bid scoring below 7 on translation quality is eliminated, whatever its other scores. The gate applies to every bid in Lot 2.
R3. A bid must reach an overall weighted score of at least 6.0 to be awarded.
R4. Lot 2 has one framework place.

Panel scores (moderated)
Lexmoor Translations — quality 7, price 6, turnaround 9
Verbatim House — quality 9, price 4, turnaround 6
Anselm Language Partners — quality 6, price 10, turnaround 8

Budget note from Finance: Lot 2 is expected to cost about $140,000 a year. Anselm's prices are roughly 30% below the other two.

Moderation comment (Rafael Quint): "Anselm's sample had two terminology slips in the exclusions clause. Quality 6 agreed by all three markers."
""",
[("award_lexmoor", "Lexmoor clears the quality gate, and its 7.1 beats Verbatim's 6.9."),
 ("award_verbatim", "Verbatim has the highest quality score and quality carries the largest weight, so it should take the place without a full calculation."),
 ("award_anselm", "Anselm's weighted total of 7.6 is the highest, and the quality gate only matters when a bid misses the 6.0 overall minimum."),
 ("no_award", "No bid reaches an overall score of 8.0, so the lot cannot be awarded.")],
"award_lexmoor", 2),

# ------------------------------------------------------------------ vd06
# why: Amendment 2 (effective 1 Jan 2026) raised off-framework saving threshold
# 10% -> 15%. Kinsale not ErgoMark 2 certified (rule covers seating) -> excluded.
# Dunmore saving (14,400-12,600)/14,400 = 12.5% < 15% -> must buy Corbel.
# Twin: Dunmore $12,100 -> saving 2,300/14,400 = 15.97% >= 15% -> Dunmore.
C("vd06", "Where should the department place the chair order?",
"""
Quenby College — Purchasing Manual, section 3 (furniture)
3.1 Office furniture must be bought from the framework supplier, Corbel Office Ltd, unless an off-framework quote for the same specification is at least 10% cheaper than the framework price.
3.2 All task seating must be certified to ErgoMark 2. This applies to chairs and stools; desks are covered by section 3.4.
3.3 Off-framework purchases under 3.1 need no further waiver.
3.4 Desks must be height-adjustable in teaching offices.

Amendment 2 (effective 1 January 2026): in 3.1, "at least 10% cheaper" is replaced by "at least 15% cheaper".

Request FR-2261 (School of Nursing, submitted 8 September 2026)
Item: 30 task chairs, mesh back, adjustable arms, same specification across all quotes.
Quotes (total, delivered and assembled):
- Corbel Office (framework): $14,400. ErgoMark 2 certified.
- Dunmore Seating: $12,600. ErgoMark 2 certified.
- Kinsale Direct: $11,900. Not ErgoMark certified ("ergonomic design", no certificate).

Requester's note: "We used Kinsale for the library stools in 2023 and they were fine."
""",
[("buy_corbel", "No certified off-framework quote reaches the 15% saving now required, so the chairs come from the framework supplier."),
 ("buy_dunmore", "Dunmore is certified and more than 10% cheaper than Corbel, which meets the off-framework test in section 3.1."),
 ("buy_kinsale", "Kinsale is cheapest, and ErgoMark certification is only needed for desks.")],
"buy_corbel", 2,
twin=T([("- Dunmore Seating: $12,600.", "- Dunmore Seating: $12,100.")], "buy_dunmore")),

# ------------------------------------------------------------------ vd07
# why: risk limit (all contracts > $50k): rating <= 3 and report dated within 180 days
# of evaluation date 21 Sep 2026; stale = ineligible, no commissioning. Brackley risk 4
# -> out. Oakhurst report 2 Feb 2026 = 231 days old -> out. Tellmore 3, 1 Jul 2026
# (82 days) -> eligible. Lowest price among eligible = Tellmore.
# Twin: Oakhurst report 2 Aug 2026 (50 days) -> eligible, $91,500 < $94,200 -> Oakhurst.
C("vd07", "Which waste contractor should be awarded the contract?",
"""
Fenwick Logistics Park — Vendor Risk Policy (extract) and bid summary
Evaluation date: 21 September 2026

Vendor Risk Policy
VR-2. For every contract with an annual value above $50,000, the supplier's financial risk rating must be 3 or better on the 1-5 Credora scale (1 = lowest risk).
VR-3. The rating must come from a Credora report dated no more than 180 days before the evaluation date. A bidder without such a report is ineligible; evaluators do not commission new reports during an evaluation.
VR-4. Among eligible bidders, the lowest annual price wins.

Bids (general and recyclable waste collection, 3 years)
| Bidder | Annual price | Credora rating | Report date |
| Brackley Waste | $86,000 | 4 | 10 Aug 2026 |
| Oakhurst Recycling | $91,500 | 2 | 2 Feb 2026 |
| Tellmore Environmental | $94,200 | 3 | 1 Jul 2026 |

Site manager's note: Brackley already empties the skips at our Denholm site and the drivers know the gate codes. Oakhurst has told us it can send a new Credora report "in a few weeks".
""",
[("award_brackley", "Brackley is cheapest, and the risk-rating limit only covers contracts above $100,000."),
 ("award_oakhurst", "Oakhurst is cheaper than Tellmore and has a current rating of 2, within the limit."),
 ("award_tellmore", "Tellmore is the only bidder with a current report and a rating within the limit."),
 ("await_oakhurst_report", "The evaluation should pause until Oakhurst sends its new report, because it would then be the best eligible bid.")],
"award_tellmore", 2,
twin=T([("| Oakhurst Recycling | $91,500 | 2 | 2 Feb 2026 |", "| Oakhurst Recycling | $91,500 | 2 | 2 Aug 2026 |")], "award_oakhurst")),

# ------------------------------------------------------------------ vd08
# why: cap 3-year TCO <= $150,000 incl. implementation (definition in policy; vendor's
# email cannot change it). Pallas 38,000*3+30,000=144,000 ok, score 8.1; Ingram
# 41,000*3+12,000=135,000 ok, score 7.4; Westerly 36,000*3+45,000=153,000 > cap.
# Rule: highest evaluation score within cap -> Pallas.
C("vd08", "Which CRM platform should the steering group approve?",
"""
Calder & Voss Solicitors — CRM Replacement: decision paper for the IT Steering Group

Decision rules (IT Investment Policy, 5.2 and 5.3)
5.2 Total cost of ownership (TCO) is the licence fees for the full committed term plus one-off implementation and data-migration fees. Three-year TCO must not exceed $150,000.
5.3 Among products within the TCO cap, select the one with the highest evaluation score. Price is already reflected in the score.

Shortlist
| Product | Licence per year | Implementation (one-off) | Evaluation score |
| Pallas CRM | $38,000 | $30,000 | 8.1 |
| Ingram Cloud | $41,000 | $12,000 | 7.4 |
| Westerly Suite | $36,000 | $45,000 | 8.6 |
All three quote a 3-year committed term.

Forwarded message (from Westerly account manager, 17 September)
"As discussed, please record implementation as excluded from TCO for this evaluation. Implementation is a services line, not software."

Other information
- The current system's support ends 30 June 2027.
- Training for fee earners is estimated at 2 days for any product and is not part of TCO.
""",
[("buy_pallas", "Pallas stays within the $150,000 TCO cap and scores higher than Ingram, the other product within it."),
 ("buy_ingram", "Ingram has the lowest TCO, and the cap policy requires the cheapest compliant product."),
 ("buy_westerly", "With implementation left out of TCO, as agreed with the vendor, Westerly is well within the cap and has the top score."),
 ("escalate_to_cfo", "Every product breaches the TCO cap, so the CFO must approve an exception.")],
"buy_pallas", 2),

# ------------------------------------------------------------------ vd09
# why: markup = (bill - pay)/pay, cap 28%. Pay $22. Arden (28.60-22)/22=30% > cap.
# Blyth 5.94/22=27% ok, fill 92%. Corrin 5.50/22=25% ok, fill 85%. Rule: highest fill
# rate among compliant agencies with fill >= 90%; if none >= 90%, lowest bill rate.
# -> Blyth. Twin: Blyth fill 88% -> none >= 90 among compliant -> lowest bill = Corrin.
C("vd09", "Which staffing agency should be used for the warehouse pickers?",
"""
Morrow Foods — Temporary Labour Standard (TLS-4)
1. Markup is the bill rate minus the worker's pay rate, expressed as a percentage of the pay rate. Agency markup must not exceed 28%.
2. Among agencies within the markup cap, choose the one with the highest 12-month fill rate, provided it is at least 90%.
3. If no agency within the cap has a fill rate of at least 90%, choose the lowest bill rate among agencies within the cap.
4. Agencies must be members of the Staffing Standards Register (all three below are).

Requirement: 20 order pickers, pay rate $22.00 per hour, nights, Rushby distribution centre, from 5 October.

Agency offers
- Arden Staffing: bill rate $28.60/hour. 12-month fill rate 95%.
- Blyth Workforce: bill rate $27.94/hour. 12-month fill rate 92%.
- Corrin Talent: bill rate $27.50/hour. 12-month fill rate 85%.

Notes from the shift manager: "Arden supplied our peak cover last Christmas and turned up every night. Their account manager says their markup is only about 23%."
""",
[("use_arden", "Arden's markup is about 23% of its bill rate, inside the 28% cap, and it has the best fill rate."),
 ("use_blyth", "Blyth is within the markup cap and is the only agency within it with a fill rate of at least 90%."),
 ("use_corrin", "No agency within the markup cap reaches a 90% fill rate, so the lowest bill rate, Corrin's, decides.")],
"use_blyth", 2,
twin=T([("12-month fill rate 92%.", "12-month fill rate 88%.")], "use_corrin")),

# ------------------------------------------------------------------ vd10
# why: FY to audit = FY2027; cooling-off covers the five preceding years FY2022-FY2026.
# Harlow audited FY2019-FY2022 -> FY2022 inside window -> ineligible. Quality >= 3:
# Mercer 3 ok ($210k), Dunstan 2 fails, Ellery 4 ok ($220k). Lowest fee among eligible
# & qualified = Mercer.
C("vd10", "Which audit firm should the audit committee appoint?",
"""
Halden Cooperative Bank — Audit Committee paper AC-26-11
Appointment of external auditor to audit the financial year FY2027

Rules (Auditor Independence Charter)
Art. 4: A firm may not be appointed if it audited any of the five financial years immediately preceding the year to be audited.
Art. 6: Only firms scoring at least 3 out of 4 in the committee's audit-quality review may be appointed. This applies to every firm, new or returning.
Art. 7: Among firms meeting Art. 4 and Art. 6, the committee appoints the firm with the lowest proposed fee.

Proposals
| Firm | Proposed fee | Quality score | Past audits of the bank |
| Harlow & Finch | $180,000 | 4 | FY2019-FY2022 |
| Mercer Quint | $210,000 | 3 | none |
| Dunstan LLP | $195,000 | 2 | none |
| Ellery Audit | $220,000 | 4 | FY2011-FY2015 |

Secretary's note: Harlow & Finch's relationship partner has retired and the firm stresses that its FY2022 audit was led by a different team. The Chair asked members to be ready to vote at the October meeting.
""",
[("appoint_harlow", "Harlow & Finch has the lowest fee, and its last audit (FY2022) is more than five years before 2027."),
 ("appoint_mercer", "Mercer Quint has the lowest fee among firms that pass both the quality threshold and the cooling-off rule."),
 ("appoint_dunstan", "Dunstan is the cheapest new firm, and the quality threshold is meant for returning auditors only."),
 ("appoint_ellery", "Ellery has the best quality score and its fee is within 5% of Mercer's, and the committee should prefer quality whenever fees are that close.")],
"appoint_mercer", 3),

# ------------------------------------------------------------------ vd11
# why: minimum: uptime >= 99.95% AND critical response <= 2 h; cheapest meeting both.
# Orbis 99.9% fails. Kestrel 99.95% ok but response 3 h fails. Lumen 99.99%, 2 h ok.
# -> Lumen. Incumbency/meeting remarks are not rules.
C("vd11", "Which support contract should replace the current one?",
"""
Incident follow-up INC-5520 — Ticketing platform outage, 2 September 2026
Action 4: choose a new platform support contract (owner: Priyanka Delacroix)

Support Contract Standard for critical systems (ITS-9)
- Guaranteed monthly uptime of at least 99.95%.
- Response to a critical-severity call within 2 hours, 24/7.
- Among contracts meeting both, pick the lowest monthly fee.

Offers received
| Contract | Uptime guarantee | Critical response | Monthly fee |
| Orbis Support Gold | 99.9% | 1 hour | $4,200 |
| Kestrel Platinum | 99.95% | 3 hours | $5,100 |
| Lumen Care Premier | 99.99% | 2 hours | $6,300 |

Excerpt from the review meeting notes
Harlan (Service Desk): "Orbis has run this platform for four years; switching is risky."
Marguerite (Finance): "99.9 and 99.95 are basically the same thing. Can we just take the cheapest?"
Chair: no decision taken; ITS-9 applies.

Timeline of the outage (for reference): detection 08:12, vendor engaged 08:40, root cause (expired certificate) found 11:05, service restored 11:32.
""",
[("keep_orbis", "Orbis has four years on this platform, and switching supplier after an outage adds risk."),
 ("take_kestrel", "Kestrel is the cheapest contract that meets the 99.95% uptime floor, and a 3-hour response is close enough for a platform with its own service desk."),
 ("take_lumen", "Lumen is the only contract that meets both the uptime floor and the 2-hour critical response.")],
"take_lumen", 1),

# ------------------------------------------------------------------ vd12
# why: exclusion: agencies currently working for a client listed in Annex C (Tessaly
# Foods, Hanlon Dairy). Brightfold works for Tessaly Foods -> excluded. Magpie & Wren
# works for Hanlon Bakery (not listed; different company) -> eligible, score 79 > 75.
# Twin: Magpie client = Hanlon Dairy -> excluded -> Coldharbour.
C("vd12", "Which agency should win the brand campaign pitch?",
"""
Greystone Creamery — Marketing Agency Pitch, evaluation note

Conflict of interest rule (Marketing Procurement Guide, 2.5)
An agency is excluded if it currently holds an account for any company listed in Annex C (direct competitors). Past accounts do not count. The rule applies to every pitch, whenever Annex C was published.

Annex C (competitors, updated May 2026): Tessaly Foods; Hanlon Dairy.

Award rule (2.7): the eligible agency with the highest pitch score wins.

Pitch results
- Brightfold Agency — score 82. Current accounts include Tessaly Foods (snacks) and Pemberton Rail.
- Magpie & Wren — score 79. Current accounts include Hanlon Bakery (a family bakery chain in Orwell, not connected to any dairy) and Castel Opticians.
- Coldharbour Creative — score 75. Current accounts include Lindell Water. It worked for Tessaly Foods until 2024.

Panel chair's comment: "Brightfold's idea was the strongest by a distance. It would be a shame to lose it."
""",
[("award_brightfold", "Brightfold has the highest score, and the conflict rule only affects contracts signed after Annex C was updated."),
 ("award_magpie_wren", "None of Magpie & Wren's current clients is on Annex C, so it is the highest-scoring eligible agency."),
 ("award_coldharbour", "Coldharbour is the highest-scoring agency with no current Annex C client.")],
"award_magpie_wren", 2,
twin=T([("Current accounts include Hanlon Bakery (a family bakery chain in Orwell, not connected to any dairy) and Castel Opticians.",
         "Current accounts include Hanlon Dairy (milk and yoghurt) and Castel Opticians.")], "award_coldharbour")),

# ------------------------------------------------------------------ vd13
# why: amended emissions limit 110 g/km (was 130). Stroud 124 fails. Zero-emission
# required only at Linford city-centre depot; vehicle based at Brackwater -> not needed.
# Cheapest compliant: Vanta $610 < Aurel $690 -> Vanta.
C("vd13", "Which lease offer should fleet services accept?",
"""
Norbury Care Services — Fleet Policy (version 4)
2.1 New lease cars must emit no more than 130 g CO2/km.
2.2 Vehicles based at the Linford city-centre depot must be zero-emission.
2.3 Among compliant offers, choose the lowest monthly lease.
Amendment (Board minute B-114, effective 1 February 2026): in 2.1, "130 g CO2/km" is replaced by "110 g CO2/km".

Replacement request FL-903
Driver role: community support worker, based at Brackwater depot, about 1,400 miles a month.
Lease term: 36 months, maintenance included.

Offers
| Model | CO2 (g/km) | Monthly lease |
| Vanta Hybrid Estate | 98 | $610 |
| Stroud Diesel Estate | 124 | $540 |
| Aurel EV Compact | 0 | $690 |

Driver comment: "I'd prefer the diesel; the last hybrid had a small boot."
Fleet coordinator note: the Aurel EV has a real-world range of about 210 miles; Brackwater depot has two chargers.
""",
[("lease_vanta", "Vanta is the cheapest lease within the amended 110 g/km limit, and no zero-emission rule applies at this depot."),
 ("lease_stroud", "At 124 g/km Stroud is within the fleet policy's 130 g/km limit and it is the cheapest lease."),
 ("lease_aurel", "The policy favours zero-emission vehicles, so the EV should be chosen whatever the depot, especially as Brackwater already has two chargers.")],
"lease_vanta", 1),

# ------------------------------------------------------------------ vd14
# why: requirements: signed DPA + SOC 2 Type II report dated within 12 months of
# evaluation (22 Sep 2026). Quire Type II Jan 2025 -> 20 months old, stale. Tallis
# Type I only -> fails. Norland Type II Mar 2026, DPA signed -> only compliant.
# Twin: Tallis holds Type II (May 2026) -> compliant and cheaper ($6.80 < $7.25) -> Tallis.
C("vd14", "Which payroll provider should be contracted?",
"""
Wexley Architects — Supplier Security Checklist for payroll outsourcing
Evaluation date: 22 September 2026

Mandatory controls (Information Security Policy, 8.4)
(a) A signed Data Processing Agreement (DPA) before any employee data is shared.
(b) A SOC 2 Type II report whose period ended no more than 12 months before the evaluation date. A Type I report does not satisfy this control.
(c) Among providers meeting (a) and (b), choose the lowest per-employee monthly fee.

Provider responses
- Quire Payroll: $6.10 per employee per month. SOC 2 Type II, period ended January 2025. DPA signed.
- Tallis HR Pay: $6.80 per employee per month. SOC 2 Type I, dated May 2026. DPA signed.
- Norland Payroll: $7.25 per employee per month. SOC 2 Type II, period ended March 2026. DPA signed.

Additional notes
Quire says its 2026 report is "in fieldwork" and expected in December. Norland's implementation takes 6 weeks, Tallis's 4 weeks. The practice has 64 employees.
""",
[("contract_quire", "Quire is the cheapest provider and has both a signed DPA and a SOC 2 Type II report."),
 ("contract_tallis", "Tallis holds a SOC 2 Type II report from the last 12 months and a signed DPA, and is cheaper than Norland."),
 ("contract_norland", "Norland is the only provider with a current SOC 2 Type II report and a signed DPA.")],
"contract_norland", 2,
twin=T([("SOC 2 Type I, dated May 2026.", "SOC 2 Type II, period ended May 2026.")], "contract_tallis")),

# ------------------------------------------------------------------ vd15
# why: AFR = incidents x 100,000 / hours; must be < 0.5. Stonebridge 3*100000/500000=0.6
# fails. Harker 2*100000/480000=0.417 ok. Pennock 1*100000/150000=0.667 fails.
# Lowest price among AFR < 0.5 = Harker ($436k).
# Twin: Pennock hours 250,000 -> 0.4 ok -> lowest price $398k -> Pennock.
C("vd15", "Which groundworks subcontractor should the project appoint?",
"""
Tollbridge Homes — Subcontractor Prequalification (Health & Safety), Plot 4 Groundworks

H&S rule HS-12: A subcontractor may be appointed only if its accident frequency rate (AFR) for the last 12 months is below 0.5. AFR = number of reportable incidents x 100,000 / total hours worked.
Commercial rule CR-3: among prequalified subcontractors, appoint the lowest price.

Returns submitted
| Subcontractor | Reportable incidents (12 months) | Hours worked (12 months) | Price |
| Stonebridge Civils | 3 | 500,000 | $412,000 |
| Harker Build | 2 | 480,000 | $436,000 |
| Pennock Groundworks | 1 | 150,000 | $398,000 |

Site manager's comment: "Pennock only had one incident all year, so they're clearly the safest."
Other: all three hold the required public liability cover. Stonebridge's quoted programme is 2 weeks shorter than the others, which is not a scored factor under CR-3.
""",
[("appoint_stonebridge", "Stonebridge's AFR works out at 0.06, well under the 0.5 limit, and its programme is shortest."),
 ("appoint_harker", "Harker is the only subcontractor whose accident frequency rate is below 0.5."),
 ("appoint_pennock", "Pennock's accident frequency rate is under 0.5 and it has the lowest price.")],
"appoint_harker", 2,
twin=T([("| Pennock Groundworks | 1 | 150,000 | $398,000 |", "| Pennock Groundworks | 1 | 250,000 | $398,000 |")], "appoint_pennock")),

# ------------------------------------------------------------------ vd16
# why: matter opened 12 May 2026, before amendment effective 1 July 2026 (applies to
# matters opened on/after) -> $450 cap. Within cap: Ashgrove $440 (rating 5), Beckett
# $395 (3). Calloway $470 over cap; complex-matter exception needs written GC approval,
# none on file. Highest rating within cap -> Ashgrove.
C("vd16", "Which panel firm should be instructed on the lease dispute?",
"""
Solent Harbour Authority — Legal Panel Instruction Form
Matter: LD-0419, dispute with Tarrow Marine over berth lease rent review.
Matter opened: 12 May 2026. Instruction being placed: 23 September 2026.

Panel rules
PR-1. Hourly rates for partners must not exceed $450.
PR-2. Choose the firm with the highest expertise rating for the matter type among firms within the rate cap; if two tie on rating, choose the lower rate.
PR-3. A firm above the cap may be used on a complex matter only with prior written approval from the General Counsel.
Amendment PR-1a (effective 1 July 2026): the partner rate cap is reduced to $400 for matters opened on or after that date. Matters opened earlier keep the previous cap.

Panel firms (property litigation)
| Firm | Partner rate | Expertise rating (1-5) |
| Ashgrove LLP | $440 | 5 |
| Beckett Rowe | $395 | 3 |
| Calloway & Dune | $470 | 5 |

File note: The Head of Estates considers the matter complex. No approval from the General Counsel is on file.
""",
[("instruct_ashgrove", "The matter predates the amendment, so the $450 cap applies and Ashgrove is the top-rated firm within it."),
 ("instruct_beckett", "Under the $400 cap Beckett is the only firm whose rate is within the limit."),
 ("instruct_calloway", "The Head of Estates treats the matter as complex, which lets the authority use Calloway above the cap without waiting for any further approval.")],
"instruct_ashgrove", 2),

# ------------------------------------------------------------------ vd17
# why: section 4 says award follows weighted totals recomputed from criteria scores;
# sheet totals are auto-filled. Weights 40/40/20.
# Tovey 7*.4+8*.4+6*.2=2.8+3.2+1.2=7.2 (sheet wrongly says 8.0); Garland 8*.4+7*.4+9*.2
# =3.2+2.8+1.8=7.8; Rennick 9*.4+5*.4+5*.2=3.6+2.0+1.0=6.6. -> Garland.
# Twin: Garland durability 5 -> 3.2+2.0+1.8=7.0 (sheet updated to 7.0) -> Tovey 7.2 highest.
C("vd17", "Which uniform supplier should receive the award?",
"""
Carrigan County Fire & Rescue — Station Workwear Tender
Section 4 of the tender rules: the award goes to the highest weighted total, computed from the criteria scores using the published weights (price 40%, durability test 40%, delivery performance 20%). The "Total" column in the scoring workbook is filled in by a spreadsheet formula and is for convenience only; where it disagrees with the criteria scores, the criteria scores govern.

Scoring workbook (pasted)
| Supplier | Price | Durability | Delivery | Total |
| Tovey Workwear | 7 | 8 | 6 | 8.0 |
| Garland Uniforms | 8 | 7 | 9 | 7.8 |
| Rennick Apparel | 9 | 5 | 5 | 6.6 |

Notes
- Durability was tested on 20 wash cycles at the county lab.
- Rennick's delivery score reflects two late deliveries on a previous county contract.
- The workbook was last edited by the procurement assistant on 18 September.
- Stations will receive garments in two batches, November and February.
""",
[("award_tovey", "Recomputed from the criteria scores, Tovey has the highest weighted total."),
 ("award_garland", "Recomputed from the criteria scores, Garland's 7.8 is the highest weighted total."),
 ("award_rennick", "Rennick has the best price score, and price is the single heaviest criterion in the published weighting, so its bid should prevail.")],
"award_garland", 3,
twin=T([("| Garland Uniforms | 8 | 7 | 9 | 7.8 |", "| Garland Uniforms | 8 | 5 | 9 | 7.0 |")], "award_tovey")),

# ------------------------------------------------------------------ vd18
# why: local preference: evaluated price = bid x 0.95 for suppliers with registered
# office in Ashby county. Frome (local) 20,800*0.95=19,760; Wexcombe (not local) 19,900;
# Pardew (local) 21,000*0.95=19,950. Lowest evaluated = Frome. Contract price is the
# actual bid. Twin: Frome bid 21,100 -> 20,045 -> Wexcombe 19,900 lowest.
C("vd18", "Which supplier should the cleaning-supplies contract go to?",
"""
Ashby County Schools Consortium — Janitorial Supplies Tender JS-7
Evaluation method

E1. Local supplier preference: for bidders whose registered office is in Ashby county, the evaluated price is the bid price reduced by 5%. The preference is used for comparison only; a local winner is paid its actual bid price.
E2. The contract goes to the bidder with the lowest evaluated price.
E3. All bidders must offer eco-labelled floor cleaner (all three do).

Bids (annual, all 14 schools)
- Frome Supplies — registered office: Ashby Market, Ashby county. Bid: $20,800.
- Wexcombe Wholesale — registered office: Carlow Gate, Tennick county. Bid: $19,900.
- Pardew Trade Counter — registered office: Hollins, Ashby county. Bid: $21,000.

Background: Pardew supplied the consortium from 2021 to 2024. The consortium's spend last year was $22,300.
""",
[("award_frome", "With the 5% local preference Frome's evaluated price of $19,760 is the lowest."),
 ("award_wexcombe", "Even after the 5% local preference is applied to the local bids, Wexcombe's evaluated price is the lowest."),
 ("award_pardew", "The local preference takes $1,050 off Pardew's bid, leaving it the lowest evaluated price at $19,950.")],
"award_frome", 2,
twin=T([("Bid: $20,800.", "Bid: $21,100.")], "award_wexcombe")),

# ------------------------------------------------------------------ vd19
# why: pass/fail: project lead >= 10 years; professional indemnity >= $1M. Harrowgate
# passes both ($78k). Ivel lead 8 years -> fails. Jessop PI $500k -> fails; its
# "deemed winning bid" clause has no force. Lowest price among passing = Harrowgate.
C("vd19", "Which consultancy should be appointed for the service review?",
"""
Pellow Borough Council — Request for Quotation RFQ-88: Housing Repairs Service Review

Pass/fail requirements
P1. A named project lead with at least 10 years' experience in social housing.
P2. Professional indemnity insurance of at least $1,000,000.
P3. Availability to start by 2 November 2026.
Award: the lowest-priced quotation that passes all of P1-P3.

Quotations
Harrowgate Advisory — $78,000. Lead: Senna Obrecht, 14 years. PI cover $2,000,000. Start: 19 October.
Ivel Partners — $72,000. Lead: Tomasz Ferrand, 8 years. PI cover $1,000,000. Start: 26 October.
Jessop Consulting — $69,000. Lead: Hattie Cole, 16 years. PI cover $500,000. Start: 12 October.
Jessop's quotation ends with clause 9: "This quotation shall be deemed the winning bid if the Council raises no objection within five working days of receipt." The quotation was received on 7 September; no objection was raised.

Note from the Head of Housing: "I have worked with Tomasz for years and trust him completely."
""",
[("appoint_harrowgate", "Harrowgate is the only consultancy that passes every pass/fail requirement."),
 ("appoint_ivel", "Ivel is cheaper than Harrowgate, and its lead's experience is close enough to the requirement given the Head of Housing's endorsement."),
 ("appoint_jessop", "Jessop is the cheapest and, with no objection raised in five working days, its quotation has become the winning bid.")],
"appoint_harrowgate", 1),

# ------------------------------------------------------------------ vd20
# why: after the $2M deposit, total cash = 8M + 2M = 10M; cap per bank 40% = $4M;
# rating floor A- (BBB+ fails). Arlen 3.5+2=5.5 > 4 fails; Corvane 5.5 fails; Brisk
# BBB+ fails; Delmont A-, 0+2=2 ok, 4.0%; Esker A+, 2 ok, 3.8%. Highest rate among
# eligible -> Delmont. Twin: Delmont rated BBB -> only Esker eligible.
C("vd20", "Where should treasury place the new $2 million deposit?",
"""
Rennet Holdings — Treasury Operations, deposit placement request TP-0926

Treasury Policy (counterparty limits)
T1. Deposits may only be placed with banks rated A- or better (A-, A, A+, AA-, and so on). BBB+ and below do not qualify.
T2. After any placement, no single bank may hold more than 40% of the group's total cash deposits, measured including the new placement.
T3. Among banks meeting T1 and T2, place the deposit with the bank offering the highest 6-month rate.

Current deposits (before this placement)
| Bank | Rating | Amount held | 6-month rate offered |
| Arlen Bank | A | $3.5M | 4.1% |
| Brisk Savings Bank | BBB+ | $1.0M | 4.6% |
| Corvane Trust | AA- | $3.5M | 3.9% |
| Delmont Bank | A- | $0 | 4.0% |
| Esker Bank | A+ | $0 | 3.8% |
Total currently held: $8.0M. New deposit to place: $2.0M (proceeds of the Harrow Street sale).

Note: Arlen's relationship manager points out that Arlen has held our main deposits since 2015.
""",
[("place_arlen", "Arlen beats Delmont's rate, and the 40% limit applies to each new deposit on its own, not to the bank's total holding."),
 ("place_brisk", "Brisk offers the highest rate, and a BBB+ rating is within the policy's A- floor."),
 ("place_corvane", "Corvane has the strongest rating of the banks already used, so it is the safest home for the deposit."),
 ("place_delmont", "Delmont meets the rating floor, stays under 40% after the deposit, and pays more than Esker."),
 ("place_esker", "Esker is the only bank that meets the rating floor and stays within the 40% limit after the deposit.")],
"place_delmont", 3,
twin=T([("| Delmont Bank | A- | $0 | 4.0% |", "| Delmont Bank | BBB | $0 | 4.0% |")], "place_esker")),

# ------------------------------------------------------------------ vd21
# why: value = day rate x estimated days (contingency excluded, clause 2.3):
# 60 x 780 = 46,800 <= 50,000 -> direct award allowed to highest-ranked AVAILABLE
# supplier. Ottery unavailable until November (start needed 5 Oct) -> Selwood.
# Open tender only above $250,000. Twin: 66 days x 780 = 51,480 > 50,000 -> mini-competition.
C("vd21", "How should the digital team buy the contractor time?",
"""
Mardale Water — Digital Services Framework DSF-3, call-off guidance

2.1 Direct award: permitted when the contract value is $50,000 or less. The call-off goes to the highest-ranked framework supplier that can meet the required start date.
2.2 Mini-competition: required when the contract value is above $50,000, among all framework suppliers.
2.3 Contract value = day rate x estimated days. Contingency allowances are not included in the contract value.
2.4 Open tender is required only for requirements above $250,000.

Request DR-512: data engineer for the smart-meter pipeline
Estimated effort: 60 days. Day rate (framework price, all suppliers): $780. Contingency requested: 10%, held by the project.
Required start: 5 October 2026.

Framework ranking and availability
1. Ottery Digital — no data engineer available until 16 November.
2. Selwood Tech — available from 28 September.
3. Brannock Data — available from 5 October.

Project manager's comment: "Ottery built the first version, so they would be quickest to ramp up."
""",
[("direct_award_ottery", "Ottery is ranked first, and rank alone decides a direct award."),
 ("direct_award_selwood", "The value is within the direct-award limit and Selwood is the highest-ranked supplier that can start on time."),
 ("mini_competition", "The contract value is above the $50,000 direct-award limit, so a mini-competition among framework suppliers is required."),
 ("open_tender", "Specialist data roles must go to open tender whatever their value.")],
"direct_award_selwood", 2,
twin=T([("Estimated effort: 60 days.", "Estimated effort: 66 days.")], "mini_competition")),
]
