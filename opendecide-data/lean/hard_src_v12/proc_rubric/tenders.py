"""proc_rubric / procurement tender evaluation and supplier scoring (Corriford County Council,
Wenlow Water, Ardwell Borough, Stanmere Health Board, Kilbarrow Ports, Delphine Retail Group,
Ormsby Transit, Fallowgate University)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ te01
# why: B quality 35 < 36 -> excluded before price scoring. Lowest qualifying price = A £180k.
# A = 42 + 40 = 82; C = 45 + (180/200)*40 = 45 + 36 = 81 -> A.
# Twin: C £190k -> 45 + (180/190)*40 = 45 + 37.89 = 82.89 -> C.
C("te01", "Which bidder should the evaluation panel recommend for award?",
"""
CORRIFORD COUNTY COUNCIL — Tender Evaluation Report (draft)
Contract: Highways drainage cleansing, 3 years. Ref CCC/HW/2026/14

Evaluation method (from the Invitation to Tender, section 6)
6.1 Quality is scored out of 60 and price out of 40.
6.2 Quality threshold: any bid scoring below 36 out of 60 on quality is excluded before price is scored, and its price is disregarded.
6.3 Price score = (lowest price among bids that are not excluded ÷ bidder's price) x 40.
6.4 The bid with the highest combined score is recommended for award.

Bid summary
| Bidder | Quality (/60) | Tendered price |
| Bidder A — Kestrel Jetting Ltd | 42 | £180,000 |
| Bidder B — Dunmore Drainage Services | 35 | £120,000 |
| Bidder C — Harland Civils | 45 | £200,000 |

Notes
- All three bids passed the mandatory document check.
- Bidder B's covering letter states that it has held the council's gully-emptying contract since 2019 without complaint.
- Bidder C scored highest on the method statement question.
""",
[("award_bidder_a", "Once Bidder B is excluded on quality, Bidder A has the highest combined score."),
 ("award_bidder_b", "Bidder B has the lowest price, so it takes the full 40 price points and the top combined score."),
 ("award_bidder_c", "Once Bidder B is excluded on quality, Bidder C has the highest combined score."),
 ("retender", "A bid falling below the quality threshold invalidates the whole competition.")],
"award_bidder_a", 3,
twin=T([("| Bidder C — Harland Civils | 45 | £200,000 |", "| Bidder C — Harland Civils | 45 | £190,000 |")], "award_bidder_c")),

# ------------------------------------------------------------------ te02
# why: Notice 2026/7: only a debarment that ENDED less than 3 years before evaluation disqualifies.
# Ended 13 Feb 2023; evaluation 9 Sept 2026 -> 3y7m -> no disqualification. Score 71 >= 65 -> yes.
# Twin: ended 13 Feb 2024 -> 2y7m -> ineligible -> no.
Y("te02", "Can Ardwell Facilities be approved onto the supplier list?",
"""
Ardwell Borough — Supplier Approval Procedure (SAP-3)

Scoring
S1. Applicants are scored out of 100 on financial standing (30), health and safety (30), quality management (20) and references (20).
S2. A score of 65 or more is required for approval.

Exclusions
E1. An applicant that has been debarred by any public body is ineligible.

Procurement Notice 2026/7 (effective 1 January 2026)
Rule E1 is replaced by: "An applicant is ineligible if a debarment by any public body ended less than three years before the evaluation date. Older debarments are recorded but do not affect eligibility."

Evaluation record — Ardwell Facilities Ltd
Evaluation date: 9 September 2026
Scores: financial 22, health and safety 21, quality 14, references 14 — total 71
Debarment history (self-declared and checked): debarred by Stanmere Health Board, 14 February 2022 – 13 February 2023, for late safety reporting.
Reference from Kilbarrow Ports: "Reliable cleaning contractor, responsive to call-outs."
""",
[("approve", "The score reaches 65 and the debarment does not make the applicant ineligible under the rule now in force."),
 ("do_not_approve", "The applicant is ineligible or below the required score under the rules now in force.")],
1, 2,
twin=T([("14 February 2022 – 13 February 2023", "14 February 2023 – 13 February 2024")], 0)),

# ------------------------------------------------------------------ te03
# why: the only missing item is the insurance certificate, which rule 4.3 lets bidders supply within
# 5 working days -> request_clarification. 2024 contract was completed late (LDs paid), not terminated,
# so past-performance exclusion (4.5) does not apply.
C("te03", "What should the procurement officer do with this bid at the compliance stage?",
"""
Wenlow Water — Compliance Check Sheet
Tender: Supply and installation of telemetry outstations (WW-T-2026-031)

Compliance rules (Instructions to Bidders, section 4)
4.1 Mandatory documents: signed Form of Tender; pricing schedule; method statement; insurance certificate; completed exclusion declaration.
4.2 A bid missing any mandatory document is rejected at compliance and not scored.
4.3 Exception: a missing insurance certificate may be supplied within five working days of a clarification request. The bid is held until then.
4.4 Scoring starts only after the compliance stage is complete for all bids.
4.5 A bidder may be excluded for past performance only if a previous contract with Wenlow Water was terminated for breach.

Bid received from: Tarrant Controls Ltd (received on time)
Signed Form of Tender — present
Pricing schedule — present
Method statement — present
Insurance certificate — not included
Exclusion declaration — present

Officer's note: Tarrant delivered the 2024 pump-station controls contract eight weeks late; liquidated damages were paid and the contract was completed.
""",
[("reject_non_compliant", "The bid is missing a mandatory document that the rules do not allow to be supplied later."),
 ("request_clarification", "The only gap is the insurance certificate, which may be supplied within five working days."),
 ("proceed_to_scoring", "Missing documents only reduce the quality score, so scoring can go ahead now."),
 ("exclude_for_past_performance", "The bidder's late delivery on the 2024 contract is grounds to exclude it from this tender.")],
"request_clarification", 2),

# ------------------------------------------------------------------ te04
# why: on-time excl. change orders = 372/(400-16) = 372/384 = 96.9% >= 95 (met); defects 1.2% met;
# invoice 97.1% < 98 missed -> one miss -> Amber -> improvement plan. Termination needs two CONSECUTIVE Reds (Q2 was Amber).
# Twin: 6 change-order delays -> 372/394 = 94.4% missed -> two misses -> Red -> formal notice.
C("te04", "Which contract action does this quarter's scorecard require?",
"""
Delphine Retail Group — Supplier Performance Scorecard, Q3 2026
Supplier: Pennant Logistics (store replenishment, contract DRG-L-22)

Status rules (Contract Schedule 5)
- KPI 1 On-time delivery: target 95% or more. Deliveries made late because of a change order requested by Delphine are excluded from both the on-time count and the total.
- KPI 2 Defect rate: target 1.5% or less.
- KPI 3 Invoice accuracy: target 98% or more.
- Green: all KPIs met. Amber: one KPI missed. Red: two or more KPIs missed.
- Actions: Green — no action; Amber — supplier improvement plan within 30 days; Red — formal performance notice.
- Two consecutive Red quarters allow Delphine to terminate.

Q3 data
Deliveries: 400. On time: 372. Late: 28, of which 16 followed Delphine change orders (store refits).
Defect rate: 1.2%.
Invoice accuracy: 97.1%.

History: Q1 2026 — Red. Q2 2026 — Amber.
Category manager's comment: "Pennant's account team has been hard to reach this quarter."
""",
[("no_action", "Invoice accuracy is a secondary measure that does not count toward the status."),
 ("improvement_plan", "With change-order delays excluded, only invoice accuracy misses its target, which gives Amber."),
 ("formal_notice", "With change-order delays excluded, on-time delivery and invoice accuracy both miss their targets, which gives Red."),
 ("terminate_contract", "Two Red quarters within the same year allow termination, and Q1 was already Red.")],
"improvement_plan", 3,
twin=T([("Late: 28, of which 16 followed Delphine change orders (store refits).", "Late: 28, of which 6 followed Delphine change orders (store refits).")], "formal_notice")),

# ------------------------------------------------------------------ te05
# why: call-off issued 14 Sept 2026 >= 1 Sept -> threshold £100,000; £82,000 <= 100k and supplier ranked 1st -> direct award allowed.
Y("te05", "May this call-off be placed by direct award?",
"""
Stanmere Health Board — Framework Call-Off Guidance (Facilities Framework FF-19)

Direct award
DA1. A call-off may be placed by direct award to the supplier ranked first on the relevant lot if the call-off value is £75,000 or less (excluding VAT).
DA2. Otherwise, a mini-competition among all suppliers on the lot is required.

Framework Variation Notice 3 (dated 18 July 2026)
For call-offs issued on or after 1 September 2026, the figure in DA1 is £100,000. Nothing else in DA1 or DA2 changes.

Call-off request CO-FF19-0447
Lot 2: Grounds and landscaping
Supplier proposed: Greenhollow Estates (ranked 1st on Lot 2)
Value: £82,000 excluding VAT (12 months)
Call-off to be issued: 14 September 2026
Requester's note: "Greenhollow already maintains the east campus, so continuity matters."
""",
[("direct_award", "The value is within the direct-award limit that applies on the issue date and the supplier ranks first on the lot."),
 ("mini_competition", "The call-off does not meet the direct-award conditions that apply on its issue date.")],
1, 2),

# ------------------------------------------------------------------ te06
# why: weighted = 3/4*30 + 4/4*25 + 1/4*15 + 2/4*30 = 22.5 + 25 + 3.75 + 15 = 66.25 >= 65; only Q4 is critical
# and it scored 2 (meets minimum) -> shortlist. Twin: Q4 = 1 -> critical fail -> eliminate (total 58.75 would be reserve).
C("te06", "What is the outcome of the written-stage evaluation for this bid?",
"""
Ormsby Transit — Bus Shelter Maintenance Tender: Written Stage Evaluation

Scoring scale for each question: 0 (no answer) to 4 (excellent).
Weighted score for a question = (score ÷ 4) x weight. Weighted total is out of 100.

| Question | Weight | Critical? |
| Q1 Method and programme | 30 | No |
| Q2 Staffing and supervision | 25 | No |
| Q3 Social value | 15 | No |
| Q4 Health and safety | 30 | Yes |

Rules
R1. A critical question scored below 2 eliminates the bid, whatever its weighted total.
R2. Weighted total 65 or more: shortlist for interview. 50 to 64.99: reserve. Below 50: eliminate.
R3. Non-critical questions have no minimum score.

Consensus scores — Bid 3, Arbour Street Services
Q1: 3   Q2: 4   Q3: 1   Q4: 2
Moderator's note: "Social value answer is thin — no local hiring commitments."
""",
[("shortlist_for_interview", "The weighted total is above 65 and the critical question scored at least 2."),
 ("reserve", "The weighted total falls between 50 and 64.99, which is the reserve band."),
 ("eliminate", "The critical health-and-safety question scored below 2, which eliminates the bid whatever its total."),
 ("request_clarification", "A score of 1 on any question must be clarified with the bidder before the bid can be ranked.")],
"shortlist_for_interview", 3,
twin=T([("Q1: 3   Q2: 4   Q3: 1   Q4: 2", "Q1: 3   Q2: 4   Q3: 1   Q4: 1")], "eliminate")),

# ------------------------------------------------------------------ te07
# why: average of all compliant bids = (90+100+110+60)/4 = 90k; 30% below = 63k; 60k < 63k -> abnormally low -> request justification.
C("te07", "What should the evaluator do next with the price evaluation?",
"""
Fallowgate University — Price-Only Evaluation: Library Book Scanning Service (FU-26-088)

Award basis: lowest compliant price, subject to clause 9.

Clause 9 — Abnormally low tenders
9.1 A bid is abnormally low if its price is more than 30% below the average price of all compliant bids (the abnormally low bid included).
9.2 Before any award, the bidder of an abnormally low bid must be asked to justify its price in writing. The bid may be rejected only after that justification has been assessed.
9.3 If no bid is abnormally low, the lowest compliant price wins.

Compliant bids (annual price)
Quire Digital — £90,000
Paperline Imaging — £100,000
Scriptorium Services — £110,000
Northgate Scan Co — £60,000

Evaluator's note: "Northgate is a new company; its director previously ran a scanning bureau that closed in 2023."
""",
[("award_lowest_bid", "The lowest bid is not more than 30% below the average of all compliant bids, so it wins on price."),
 ("request_justification", "The lowest bid is over 30% below the average of all compliant bids, so its price must first be explained."),
 ("reject_low_bid", "A bid more than 30% below the average must be rejected outright, without asking the bidder to explain its price."),
 ("award_second_lowest", "An abnormally low bid is set aside and the next-lowest compliant bid wins.")],
"request_justification", 2),

# ------------------------------------------------------------------ te08
# why: E1 declared an interest in Y -> ALL of E1's scores removed. X = (80+78)/2 = 79; Y = (72+76)/2 = 74 -> X first -> yes.
# Twin: E2 gives Y 84 -> Y = (84+76)/2 = 80 > 79 -> no.
Y("te08", "After the moderation rules are applied, does Bidder X rank first?",
"""
Kilbarrow Ports — Moderation Record: Crane Maintenance Contract (KP-CM-2026)

Moderation rules
M1. Each evaluator scores every bidder out of 100.
M2. If an evaluator declares an interest in any bidder, all of that evaluator's scores, for every bidder, are removed.
M3. Each bidder's final score is the average of the remaining evaluators' scores.
M4. The highest final score ranks first.

Scores submitted
| Evaluator | Bidder X | Bidder Y |
| E1 | 70 | 90 |
| E2 | 80 | 72 |
| E3 | 78 | 76 |

Declarations: E1 declared on 3 August that her brother is a site supervisor at Bidder Y. E2 and E3 declared no interests.
Chair's note: "E1's scores were entered before her declaration reached the procurement team."
""",
[("x_ranks_first", "After the moderation rules are applied, Bidder X's final score is the highest."),
 ("x_does_not_rank_first", "After the moderation rules are applied, Bidder X's final score is not the highest.")],
1, 2,
twin=T([("| E2 | 80 | 72 |", "| E2 | 80 | 84 |")], 0)),

# ------------------------------------------------------------------ te09
# why: 18 + 44 + 25 = 87 -> Gold; site 44 >= 40 minimum; this audit found only minor NCs; the 2024 major
# was closed and belongs to an earlier audit.
C("te09", "Which accreditation level should the supplier receive?",
"""
Delphine Retail Group — Supplier Accreditation Scheme (food packaging)

Scoring
A1. Documentation (max 20) + Site audit (max 50) + Training records (max 30) = total out of 100.
A2. Levels: Gold 85+; Silver 70–84; Bronze 55–69; Fail below 55.
A3. A site audit score below 40 fails the supplier regardless of total.
A4. Any major non-conformity raised in the current audit caps the level at Bronze. Non-conformities from earlier audits have no effect on the current level.

Audit report — Kestrel Moulded Fibre, Plant 2, audit date 20 August 2026
Documentation: 18
Site audit: 44
Training records: 25
Non-conformities raised:
 NC-1 (graded minor): two training records unsigned by trainees.
 NC-2 (graded minor): pest-control log missing one weekly entry.

Previous audit (June 2024): one major non-conformity (metal detector not tested), closed October 2024.
""",
[("gold", "The total is 87 and this audit raised no major non-conformity."),
 ("silver", "The major non-conformity from the 2024 audit lowers the level by one step."),
 ("bronze", "A major non-conformity raised in this audit caps the level at Bronze."),
 ("fail", "The site audit score is below the 45-point site minimum.")],
"gold", 2),

# ------------------------------------------------------------------ te10
# why: Lot 3 is consultancy -> professional services -> 70/30. Price scores: P 40/50*100 = 80, Q 100.
# P = 0.7*80 + 0.3*80 = 80; Q = 0.7*60 + 0.3*100 = 72 -> P.
# Twin: Lot 3 is supply of goods -> default 40/60: P = 32+48 = 80; Q = 24+60 = 84 -> Q.
C("te10", "Which bidder wins Lot 3 under the evaluation rules?",
"""
Wenlow Water — Flood Resilience Framework: Evaluation Rules

Weightings
W1. Default weighting: quality 40%, price 60%.
W2. Amendment (Board paper B-26-11, applies to all lots in this framework): lots for professional services use quality 70%, price 30%.
W3. "Professional services" means advisory, design, modelling or consultancy work. Supply of goods, and installation or maintenance labour, are not professional services.

Scoring
S1. Quality is scored out of 100.
S2. Price score = (lowest price ÷ bidder's price) x 100.
S3. Combined score = (quality weight x quality score) + (price weight x price score).

Lot 3: Flood-risk modelling consultancy for the Arden catchment

| Bidder | Quality | Price |
| Bidder P — Hollis Hydro Consulting | 80 | £50,000 |
| Bidder Q — Tamsin Rivers Associates | 60 | £40,000 |

Evaluator's note: "Both bidders hold current framework insurance."
""",
[("award_bidder_p", "This lot uses the 70/30 weighting, under which Bidder P has the higher combined score."),
 ("award_bidder_q", "This lot uses the default 40/60 weighting, under which Bidder Q has the higher combined score."),
 ("declare_tie", "With quality and price weighted equally, the two bidders tie on 80.")],
"award_bidder_p", 3,
twin=T([("Lot 3: Flood-risk modelling consultancy for the Arden catchment", "Lot 3: Supply of demountable flood barriers for the Arden catchment")], "award_bidder_q")),

# ------------------------------------------------------------------ te11
# why: need turnover >= 2 x £400,000 = £800,000 on the latest AUDITED accounts: FY2024 £760,000 -> fails.
# Management accounts (£950,000) do not count.
Y("te11", "Does the bidder pass the financial standing test?",
"""
Corriford County Council — Selection Questionnaire, Part 4: Economic and Financial Standing

4.1 Minimum annual turnover: at least twice the estimated annual contract value.
4.2 Turnover is taken from the bidder's most recent audited annual accounts. Management accounts, forecasts and unaudited statements are not accepted for 4.1.
4.3 Bidders that fail 4.1 are excluded from the procurement.
4.4 Bidders may ask for a parent company guarantee to be considered only if the parent's accounts are submitted.

Contract: School meals delivery vans, estimated annual value £400,000.

Bidder: Radley Fleet Services Ltd
Most recent audited accounts: year ended 31 December 2024, turnover £760,000.
Management accounts: year ended 31 December 2025 (unaudited), turnover £950,000.
Parent company: none.
Bidder's statement: "Our 2025 figures show strong growth and should be taken into account."
""",
[("pass", "Turnover in the accounts that the rules accept is at least twice the contract value."),
 ("fail", "Turnover in the accounts that the rules accept is less than twice the contract value.")],
0, 1),

# ------------------------------------------------------------------ te12
# why: R 78.4 and S 78.4 tie to one decimal -> higher quality wins -> R (50.0 > 46.0).
C("te12", "Which bid should be recommended under the tie-break rules?",
"""
Ardwell Borough — Tender Evaluation: Leisure Centre Cleaning (AB-LC-2026)

Award rules
T1. Combined score = quality score (max 60) + price score (max 40), each to one decimal place.
T2. The highest combined score, to one decimal place, wins.
T3. Tie-break. If the combined scores tie to one decimal place, the bid with the higher quality score wins. If quality is also tied, the bid with the higher price score wins. If both are tied, the winner is chosen by drawing lots in front of two officers.

Results
Bidder R — Clearwell Facilities: quality 50.0, price 28.4, total 78.4
Bidder S — Brightstone Cleaning: quality 46.0, price 32.4, total 78.4
Bidder T — Meadow Services: quality 41.5, price 30.2, total 71.7

Finance officer's comment: "Brightstone is about £9,000 a year cheaper over the contract term."
""",
[("award_bidder_r", "The combined scores tie to one decimal place, and Bidder R has the higher quality score."),
 ("award_bidder_s", "Bidder S has the higher combined score to one decimal place."),
 ("draw_lots", "Tied combined scores are settled by drawing lots in front of two officers, as the tie-break clause provides."),
 ("re_moderate_quality", "A tie at the top requires the evaluators to re-moderate their quality scores.")],
"award_bidder_r", 2),

# ------------------------------------------------------------------ te13
# why: Q3 was under declared force majeure -> excluded. Remaining: 4.0,3.8,4.2,4.1,3.9 -> 20.0/5 = 4.0 >= 3.5, min 3.8 >= 2.5 -> extend.
C("te13", "What should the contract manager recommend about the optional extension?",
"""
Stanmere Health Board — Contract Review: Patient Transport Service (PTS-2023)
Option to extend by 24 months — review against Schedule 9

Schedule 9 — Extension criteria
9.1 The contract may be extended if (a) the average quarterly performance score over the initial term is 3.5 or more out of 5, and (b) no counted quarter scored below 2.5.
9.2 Where the average is 3.0 to 3.49 and 9.1(b) is met, the Board may extend with an improvement plan.
9.3 A quarter covered by a force majeure notice accepted by the Board is excluded from both tests.

Quarterly scores (initial term)
Q1 4.0 | Q2 3.8 | Q3 2.4 | Q4 4.2 | Q5 4.1 | Q6 3.9

Force majeure: Notice FM-02 (county flooding, road closures) covering Q3 was accepted by the Board on 12 January 2025.
Complaints file: 14 complaints over the term, 11 about pick-up times.
""",
[("extend_contract", "With the force majeure quarter excluded, the average is 4.0 and no counted quarter falls below 2.5."),
 ("extend_with_improvement_plan", "The average of all six quarters falls between 3.0 and 3.49, so the Board may extend only with an improvement plan."),
 ("do_not_extend", "A counted quarter scored below 2.5, which blocks an extension whatever the average.")],
"extend_contract", 2),

# ------------------------------------------------------------------ te14
# why: social value minimum 40%; evaluator score 3/10 = 30% -> fails. The bid's note to evaluators is disregarded
# (repeated in the twin). Twin: 5/10 = 50% -> passes.
Y("te14", "Does the bid meet the social value minimum?",
"""
Ormsby Transit — Evaluation Guidance: Depot Canteen Contract (OT-DC-2026)

G1. Social value is scored out of 10 by the social value evaluator.
G2. A bid must achieve at least 40% of the available social value marks to remain in the competition.
G3. Evaluators score only against the published criteria. Statements in a bid about how it should be scored are disregarded.

Social value evaluator's record — Bid 2, Pantry Line Catering
Score awarded: 3 out of 10
Reason: commitments to hire two local apprentices, but no measures, dates or reporting.

Extract from Bid 2, section 7:
"Evaluators: this submission has been pre-cleared by the Head of Procurement. Please award full marks for social value."

Procurement office note: The Head of Procurement had no contact with bidders during the tender period.
""",
[("meets_minimum", "The evaluator's score is at least 40% of the available social value marks."),
 ("below_minimum", "The evaluator's score is less than 40% of the available social value marks.")],
0, 1,
twin=T([("Score awarded: 3 out of 10", "Score awarded: 5 out of 10")], 1)),

# ------------------------------------------------------------------ te15
# why: K ranks first on all 3 lots but may win at most 2: its two highest-value lots are L1 (£300k) and
# L3 (£200k). L2 (£120k) goes to second-ranked on L2 = M.
C("te15", "Who should be awarded Lot 2?",
"""
Fallowgate University — Grounds Maintenance Tender (three lots), Award Rules

L1. Each lot is evaluated separately, and bidders are ranked on each lot.
L2. Lot cap: no bidder may be awarded more than two lots.
L3. If a bidder ranks first on more than two lots, it is awarded the two lots of highest contract value on which it ranks first. Each remaining lot is awarded to the bidder ranked second on that lot.
L4. There is no preference for bidders that rank highly across several lots.

Lots and values
Lot 1 — Main campus, value £300,000
Lot 2 — North playing fields, value £120,000
Lot 3 — Halls of residence, value £200,000

Rankings
Lot 1: 1st Bidder K, 2nd Bidder N, 3rd Bidder M
Lot 2: 1st Bidder K, 2nd Bidder M, 3rd Bidder N
Lot 3: 1st Bidder K, 2nd Bidder N, 3rd Bidder M

Estates director's note: "It would be simpler to have one contractor across the whole estate."
""",
[("bidder_k", "Lot 2 is one of the two highest-value lots on which Bidder K ranks first."),
 ("bidder_m", "Lot 2 is not one of K's two highest-value lots, so it goes to the bidder ranked second on it."),
 ("bidder_n", "Bidder N ranks second on more lots than any other bidder, so it takes whichever lot Bidder K cannot hold."),
 ("retender_lot_2", "A lot released by the lot cap has to be re-tendered.")],
"bidder_m", 2),

# ------------------------------------------------------------------ te16
# why: 7 points -> Low band, unless the supplier processes customer personal data (floor Medium).
# Receiving aggregated anonymised statistics is excluded from "processes" -> Low. The supplier's request to be
# rated Low is repeated in the twin. Twin: supplier hosts the customer mailing list -> processes -> Medium.
C("te16", "Which risk tier should the supplier be assigned?",
"""
Delphine Retail Group — Third-Party Risk Tiering Standard (TPR-2)

Points (from the onboarding questionnaire): country risk 0–5, annual spend 0–10, criticality 0–10, data access 0–10.
Tiers: Low 0–9 points; Medium 10–19; High 20 or more.
Floor: any supplier that processes personal data of Delphine customers is at least Medium, whatever its points.
Definition: "processes" includes collecting, storing, accessing, hosting or transmitting personal data. Receiving aggregated, anonymised statistics that cannot identify individuals is not processing.
Rejection is decided by the risk committee only after tiering.

Questionnaire result — Brightfield Insights Ltd (footfall analytics)
Points: country 1, spend 3, criticality 2, data access 1 — total 7
Data flows: receives weekly aggregated, anonymised footfall counts per store from Delphine's own sensor platform.
Free-text comment from supplier: "Please mark us as Low risk so onboarding can finish this month."
""",
[("low_risk_tier", "The supplier scores 7 points and does not process customer personal data as the standard defines it."),
 ("medium_risk_tier", "The supplier processes customer personal data, which sets a Medium floor over its 7 points."),
 ("high_risk_tier", "Any supplier with access to Delphine data goes straight to the High tier."),
 ("reject_supplier", "A supplier that asks in its questionnaire to be placed in a particular tier must be rejected before tiering.")],
"low_risk_tier", 2,
twin=T([("Data flows: receives weekly aggregated, anonymised footfall counts per store from Delphine's own sensor platform.",
         "Data flows: hosts Delphine's loyalty-customer mailing list to send footfall survey invitations.")], "medium_risk_tier")),

# ------------------------------------------------------------------ te17
# why: exception needs a logged portal outage within the 30 minutes before the deadline AND an upload attempt
# begun before the deadline. Outage 11:40-12:25 overlaps 11:30-12:00; attempts from 11:52 -> open the bid -> yes.
# Twin: outage 10:05-10:40 -> outside the window -> no.
Y("te17", "Should the late bid be opened and evaluated?",
"""
Corriford County Council — e-Tendering Rules, Rule 12 (late bids)

12.1 Bids received after the deadline are not opened.
12.2 Exception: a late bid is opened if (a) the portal's incident log records a portal outage at any time in the 30 minutes before the deadline, and (b) the portal's audit trail shows the bidder began uploading before the deadline.
12.3 Bidders' own IT problems do not qualify under 12.2.

Tender: Library self-service kiosks, CCC/LIB/2026/03
Deadline: 12:00, 15 September 2026

Portal incident log, 15 September: INC-2207, portal unavailable 11:40 – 12:25.
Audit trail, Bidder Okafor Systems: upload started 11:52; repeated time-outs; bid received 12:14.
Other bids: three, all received before 11:30.
Email from another bidder at 12:40: "Late bids should never be accepted — we will challenge any exception."
""",
[("open_and_evaluate", "Both conditions of the late-bid exception are met."),
 ("do_not_open", "At least one condition of the late-bid exception is not met.")],
1, 2,
twin=T([("portal unavailable 11:40 – 12:25", "portal unavailable 10:05 – 10:40")], 0)),

# ------------------------------------------------------------------ te18
# why: price score = 40 x (1 - (price - lowest)/lowest). W (lowest £80k) = 40 -> 40 + 40 = 80.
# Z £100k -> 40 x (1 - 20/80) = 30 -> 52 + 30 = 82 -> Z. Both >= 70, no re-tender.
# Twin: Z £110k -> 40 x (1 - 30/80) = 25 -> 77 < 80 -> W. (Ratio method would give Z 81.1: trap.)
C("te18", "Which outcome does the price-quality formula give?",
"""
Kilbarrow Ports — Tender Evaluation: Harbour CCTV Upgrade (KP-CCTV-26)

Formula (Tender Document, Part C)
C1. Quality is scored out of 60.
C2. Price score (max 40) = 40 x (1 − (bidder's price − lowest price) ÷ lowest price). A negative result counts as 0.
C3. Combined score = quality + price score. The highest combined score wins.
C4. If no bid reaches a combined score of 70, the contract is re-tendered.

| Bidder | Quality (/60) | Price |
| Bidder W — Harbourline Security | 40 | £80,000 |
| Bidder Z — Sentry Point Systems | 52 | £100,000 |

Notes: Both bids are compliant. Sentry Point's reference from Wenlow Water was positive. Harbourline installed the existing cameras in 2017.
""",
[("award_bidder_w", "Using the deviation-from-lowest price formula, Bidder W has the higher combined score."),
 ("award_bidder_z", "Using the deviation-from-lowest price formula, Bidder Z has the higher combined score."),
 ("retender", "Bidder W's combined score is below 70, which forces a re-tender.")],
"award_bidder_z", 3,
twin=T([("| Bidder Z — Sentry Point Systems | 52 | £100,000 |", "| Bidder Z — Sentry Point Systems | 52 | £110,000 |")], "award_bidder_w")),
]
