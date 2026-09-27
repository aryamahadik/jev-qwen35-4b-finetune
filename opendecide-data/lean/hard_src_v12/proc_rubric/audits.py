"""proc_rubric / inspections, audits and assessments scored against rubrics (Brackley District
Council, Tamworth Vale Fire Authority, Lumen Freight, Grayling Hotels Board, Ashdown Organic
Certification, Kerrow Licensing, Norland Water Services, Halden Museums Trust)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ in01
# why: lower is better. Total 10 + 5 + 15 = 30 -> band 21-30 = rating 3; management 15 (>= 15) caps at 2 -> rating 2.
C("in01", "Which food hygiene rating should the inspector issue?",
"""
Brackley District Council — Food Hygiene Rating Scheme: Scoring Guide (local edition)

Three component scores are given at each inspection (lower is better):
 Hygienic food handling: 0, 5, 10, 15, 20 or 25
 Structure and cleaning: 0, 5, 10, 15, 20 or 25
 Confidence in management: 0, 5, 10, 15, 20 or 30

Rating by total score: 0–15 → 5; 16–20 → 4; 21–30 → 3; 31–40 → 2; 41–50 → 1; 51 or more → 0.
Cap: if any single component score is 15 or more, the rating cannot be higher than 2.

Inspection — The Copper Kettle Café, 12 Tanner Row. Date: 3 September 2026.
Hygienic food handling: 10 (probe thermometer not calibrated; raw and ready-to-eat items stored on the same shelf)
Structure and cleaning: 5 (minor wear to floor seals)
Confidence in management: 15 (no written food safety system in use; training records missing for two staff)
Previous rating (2024): 4.
Owner's comment: "We have had a new chef since July and things are much better."
""",
[("rating_4", "Lower scores are better, and the structure score of 5 is the one that sets the rating."),
 ("rating_3", "The total falls in the 21–30 band and no single component reaches 15."),
 ("rating_2", "A component score of 15 or more caps the rating at 2."),
 ("rating_1", "A management score of 10 or more drops a business straight to rating 1.")],
"rating_2", 2),

# ------------------------------------------------------------------ in02
# why: door major 5 + three extinguishers minor 3 + lighting major 5 + escape route critical remedied in the
# inspector's presence -> recorded as major 5 = 18 -> enforcement notice (15-24). No critical as recorded.
# Twin: route not cleared -> critical -> prohibition notice.
C("in02", "Which enforcement outcome does the fire safety audit score require?",
"""
Tamworth Vale Fire Authority — Fire Safety Audit Scoring (Commercial Premises)

Deficiency points: critical 10; major 5; minor 1 (each deficiency is scored separately).
A critical deficiency that the responsible person remedies in the inspector's presence is recorded and scored as major.
Outcome:
 Any critical deficiency as recorded → prohibition notice (use restricted immediately)
 Otherwise, total 0–4 → compliant; 5–14 → action plan within 60 days; 15–24 → enforcement notice; 25+ → prohibition notice.

Audit — Wexley Trade Warehouse, Unit 7, Cobden Park. Date: 26 August 2026.
1. Fire door to stair core wedged open — major.
2. Three extinguishers past their annual service date — minor, one each.
3. Emergency lighting fault in stairwell B — major.
4. Final escape route from the mezzanine blocked by stored pallets — critical. Pallets were moved by the site manager during the audit and the route was checked clear.

Previous audit (2023): compliant.
Site manager's note: "We are moving out of this unit in March anyway."
""",
[("action_plan_60_days", "The three extinguisher items count as a single minor deficiency and the cleared route is not scored, which gives 11."),
 ("enforcement_notice", "The blocked route was cleared during the audit, so it counts as major, which brings the total to 18."),
 ("prohibition_notice", "A critical deficiency that was not put right during the audit requires a prohibition notice.")],
"enforcement_notice", 2,
twin=T([("Pallets were moved by the site manager during the audit and the route was checked clear.",
         "The site manager said the pallets would be moved the following week.")], "prohibition_notice")),

# ------------------------------------------------------------------ in03
# why: needs score >= 80 AND no critical gap. MFA optional on standard accounts that view tickets holding Company data
# -> MFA gap -> critical -> no. Twin: MFA enforced on all accounts -> 84, no gap -> yes.
Y("in03", "Can the vendor be approved to handle confidential data?",
"""
Lumen Freight — Vendor Security Assessment Standard (VSA-3)

V1. Vendors that will handle Lumen confidential data must score at least 80 out of 100 on the security questionnaire.
V2. They must also have no critical gap. Critical gaps are:
 (a) MFA gap: multi-factor authentication not enforced for any account, admin or standard, that can access Lumen data;
 (b) backups of Lumen data stored unencrypted;
 (c) no incident notification commitment within 72 hours.
V3. Vendors that fail V1 or V2 may reapply after remediation.

Assessment — Parcelry Support Ltd (outsourced customer service desk)
Questionnaire score: 84
MFA: enforced for all admin accounts; optional for standard staff accounts. Standard accounts are used by support agents to view and answer customer tickets, which contain Lumen shipment and customer data.
Backups: encrypted at rest (AES-256).
Incident notification: contract clause commits to 24 hours.
Vendor's account manager: "We have never had a breach in eleven years."
""",
[("approve_confidential", "The questionnaire score reaches 80 and no critical gap is present."),
 ("do_not_approve", "The questionnaire score is too low or a critical gap is present.")],
0, 2,
twin=T([("MFA: enforced for all admin accounts; optional for standard staff accounts.", "MFA: enforced for all admin accounts and all standard staff accounts.")], 1)),

# ------------------------------------------------------------------ in04
# why: average (92 + 88 + 58 + 95)/4 = 83.25 -> Silver; Housekeeping 58 < 60 triggers re-audit unless an improvement
# plan for it is open (Q3 2026 amendment). Plan HK-12 closed 30 June -> not open -> re-audit.
C("in04", "What result should the regional safety lead record for this depot audit?",
"""
Lumen Freight — Depot Safety Audit Protocol (DSA-5)

Scoring
S1. Each section is scored as a percentage. The overall score is the simple average of the section scores.
S2. Bands: Gold 90+; Silver 80–89.99; Bronze 70–79.99; Fail below 70.
S3. A section below 60% overrides the band: the depot is recorded as "Re-audit within 30 days".
S4. Amendment (from Q3 2026): a Housekeeping section below 60% does not trigger S3 if the depot has an open improvement plan for housekeeping on the audit date. The low score is still recorded.

Audit — Northfleet Depot, 14 August 2026
Racking and storage: 92%
Forklift operations: 88%
Housekeeping: 58%
Fire safety: 95%
Improvement plans: HK-12 (housekeeping, aisle clutter) — closed 30 June 2026.
Depot manager's note: "Two agency pickers started this week, which explains the clutter."
""",
[("gold", "The average of the four sections is above 90."),
 ("silver", "The section average is 83.25, and the low housekeeping score is covered by an open improvement plan."),
 ("bronze", "A section below 60% lowers the band by one level."),
 ("re_audit_30_days", "A section below 60% without an open improvement plan overrides the band.")],
"re_audit_30_days", 2),

# ------------------------------------------------------------------ in05
# why: 690 >= 650 but 24-hour reception needs a staffed desk or staff physically on site within 5 minutes all night;
# manager on call from home 15 minutes away -> not met -> 3-star (>= 500). Postponement not allowed after the visit.
# Twin: night porter on site 01:00-06:00 -> 4-star.
C("in05", "Which star grading should the assessor award?",
"""
Grayling Hotels Board — Star Grading Scheme 2026 (Hotels)

G1. Four-star: at least 650 quality points AND all four-star mandatory requirements, including 24-hour reception.
G2. Three-star: at least 500 quality points.
G3. Below 500 points: two-star.
Definition: "24-hour reception" means a staffed reception desk, or a member of staff physically on site and able to reach reception within 5 minutes, at all hours.
G4. Once the assessment visit has taken place, the grading cannot be postponed at the operator's request.

Assessment — The Merrow Lodge, visit 2–3 September 2026
Quality points: 690
Reception: desk staffed 06:00–01:00. From 01:00 to 06:00 the duty manager is on call by phone from home, 15 minutes' drive away.
Other four-star requirements: all met (room service, daily housekeeping, en-suite rooms).

Letter from the owner, 4 September: "Please postpone the grading until our new night arrangements start next month."
""",
[("award_four_star", "The points exceed 650 and staff are on site through the night."),
 ("award_three_star", "The points pass 650, but an off-site manager on call does not meet the 24-hour reception rule."),
 ("award_two_star", "Missing any four-star mandatory requirement drops the hotel two levels below the grade its points reach."),
 ("defer_grading", "The owner asked in writing to postpone, and that request must be granted before any grading is issued.")],
"award_three_star", 2,
twin=T([("From 01:00 to 06:00 the duty manager is on call by phone from home, 15 minutes' drive away.",
         "From 01:00 to 06:00 a night porter is on duty in the building and covers the desk.")], "award_four_star")),

# ------------------------------------------------------------------ in06
# why: suspend if 2+ majors or any major repeated from the previous inspection. One major (seed records);
# previous major was buffer zone -> not repeated -> no suspension.
# Twin: previous major was also seed records -> repeated -> suspend.
Y("in06", "Must the operator's certification be suspended?",
"""
Ashdown Organic Certification — Sanctions Rule SR-4

SR-4.1 Certification is suspended if the annual inspection records:
 (a) two or more major non-conformities; or
 (b) any major non-conformity that repeats a major non-conformity recorded at the previous annual inspection.
SR-4.2 Minor non-conformities never lead to suspension on their own; they must be closed within 90 days.
SR-4.3 Otherwise, a corrective action plan is agreed within 28 days.

Annual inspection report — Hollybank Farm (arable and vegetables), 11 August 2026
Major non-conformity: organic seed purchase records missing for spring barley.
Minor non-conformities: (1) field map not updated; (2) cleaning log for the shared drill incomplete; (3) one label missing the certifier code.

Previous annual inspection (August 2025): one major non-conformity — buffer zone next to conventional neighbour narrower than 3 m. Closed October 2025.
Inspector's comment: "The farm manager was cooperative and is new in post."
""",
[("suspend", "A suspension trigger in SR-4.1 is met."),
 ("do_not_suspend", "Neither suspension trigger in SR-4.1 is met.")],
0, 2,
twin=T([("one major non-conformity — buffer zone next to conventional neighbour narrower than 3 m.",
         "one major non-conformity — organic seed purchase records missing for winter wheat.")], 1)),

# ------------------------------------------------------------------ in07
# why: three minors in the lighting system count as one major -> fail. Brakes: 2 minors only.
C("in07", "What test result should the licensing examiner give this taxi?",
"""
Kerrow Licensing Authority — Hackney Carriage Compliance Test

Defect categories
 Dangerous: fail; the vehicle must not be driven until repaired.
 Major: fail.
 Minor: pass, with each minor defect listed as an advisory.
Rule D4: three or more minor defects in the same system are treated as one major defect.
Systems: brakes; steering and suspension; lighting and signalling; tyres and wheels; body and interior.

Test sheet — licence plate KL-0417, 2019 hybrid saloon, 22 September 2026
Brakes: (1) handbrake lever travel slightly excessive — minor; (2) front discs lightly corroded — minor.
Lighting and signalling: (1) number plate lamp dim — minor; (2) rear fog lamp tell-tale inoperative — minor; (3) nearside indicator lens cracked — minor.
Tyres and wheels: no defects.
Body and interior: no defects.
Driver's comment: "This car passed its test with no advisories last September."
""",
[("pass", "Minor defects are not recorded on the certificate, so this is a clean pass."),
 ("pass_with_advisories", "Every defect is minor and no system has three or more of them."),
 ("fail", "Three minor defects in the lighting and signalling system count as a major defect."),
 ("fail_off_road", "Brake defects are always treated as dangerous.")],
"fail", 1),

# ------------------------------------------------------------------ in08
# why: risk = 3 x 2 = 6, rollback documented (no +3) -> standard change (<= 6) -> may run in the freeze -> auto-approve.
# Twin: no rollback plan -> 9 -> normal change; not a P1 fix -> cannot run in the freeze -> defer.
C("in08", "How should the change be handled under the change policy?",
"""
Norland Water Services — IT Change Policy (CHG-2)

Risk score = impact (1–5) x likelihood (1–5). Add 3 if no tested rollback plan is attached.
 Risk 6 or less: standard change — pre-approved, no CAB review.
 Risk 7–14: normal change — needs CAB approval.
 Risk 15 or more: high-risk change — needs CAB approval and Director of IT sign-off.
Change freeze (20–31 December): only standard changes and fixes for a live P1 incident may run. Other changes are deferred until after the freeze.

Change request CR-26-1188
Title: Patch SCADA historian servers to vendor build 7.4.2
Scheduled: 22 December 2026, 02:00–04:00
Impact: 3 (historian read-only for two hours; telemetry buffered)
Likelihood: 2
Rollback plan: attached — snapshot restore, tested in staging on 9 December.
Linked incident: none.
Requester's note: "The vendor says this build fixes a memory leak we have seen twice this year."
""",
[("auto_approve", "The risk score is 6 with a tested rollback plan, so it is a standard change that may run in the freeze."),
 ("cab_approval", "Every change scheduled during a freeze needs CAB approval."),
 ("director_sign_off", "Changes with an impact of 3 or more always need the Director of IT's sign-off."),
 ("defer_until_after_freeze", "Without a rollback plan the score is 9, and changes above 6 that do not fix a P1 cannot run in the freeze.")],
"auto_approve", 2,
twin=T([("Rollback plan: attached — snapshot restore, tested in staging on 9 December.", "Rollback plan: not attached.")], "defer_until_after_freeze")),

# ------------------------------------------------------------------ in09
# why: DPIA needed if 2+ criteria. Badge logs of 6,000 staff (not > 10,000) = systematic monitoring only (1).
# Existing card readers, no biometric data -> no DPIA. Twin: facial recognition -> new technology + special
# category (biometric) + monitoring = 3 -> DPIA required.
Y("in09", "Is a full DPIA required for this project?",
"""
Brackley District Council — Data Protection Impact Assessment Screening (Form DP-1)

A full DPIA is required if the project meets TWO or more of these criteria:
 C1. Large scale: personal data of more than 10,000 people.
 C2. Special category data, including biometric data used to identify people.
 C3. Systematic monitoring of people (for example, logging movements or activity).
 C4. New technology not previously used by the Council for this purpose.
 C5. Automated decisions with legal or similarly significant effects.
If fewer than two criteria are met, the project records its screening result and proceeds.

Project: Building Access Reporting
Scope: monthly reports of door entry times for 6,000 staff across three civic buildings.
Technology: existing proximity-card readers (installed 2019); no new hardware.
Decisions: reports are used for fire-roll accuracy only; no automated decisions.
Project sponsor: "We need this live before the winter fire drills."
""",
[("dpia_required", "Two or more screening criteria are met."),
 ("dpia_not_required", "Fewer than two screening criteria are met.")],
0, 2,
twin=T([("Technology: existing proximity-card readers (installed 2019); no new hardware.",
         "Technology: new facial-recognition cameras at each entrance, matching faces to staff ID photos.")], 1)),

# ------------------------------------------------------------------ in10
# why: applicable = 120 - 12 N/A = 108; 98/108 = 90.74% -> A; no failed critical item.
C("in10", "Which supplier audit grade should be issued?",
"""
Lumen Freight — Packaging Supplier Audit: Grading Rules

A1. The checklist has 120 items worth 1 point each. Items marked "not applicable" are removed from the total available.
A2. Score = points achieved ÷ applicable items, as a percentage.
A3. Grades: A 90%+; B 75–89.99%; C 60–74.99%; D below 60%.
A4. Failing any critical item caps the grade at C.

Audit — Crestline Cartons, Plant 1, 28 July 2026
Items not applicable: 12 (no printed food-contact packaging made on this site)
Points achieved: 98
Failed items: 10 (all non-critical: labelling, housekeeping and document control)
Previous grade (2025): B.
Auditor's comment: "Big improvement in goods-in checks since last year."
""",
[("grade_a", "Against applicable items only, the score is above 90% and no critical item failed."),
 ("grade_b", "Scored against all 120 items, the result falls between 75% and 89.99%."),
 ("grade_c", "A failed critical item caps the grade at C."),
 ("grade_d", "More than five failed items puts the supplier in grade D, whatever its percentage score.")],
"grade_a", 2),

# ------------------------------------------------------------------ in11
# why: odour complaint shares the odour-control unit failure's root cause -> only Cat 2 (28) scored for that event;
# plus late records Cat 4 (0.1) = 28.1 -> band C (10.1-30).
C("in11", "Which compliance band does the site fall into for the year?",
"""
Norland Water Services — Environmental Permit Compliance Scoring (internal replica of the regulator's scheme)

Breach categories and points: Category 1 = 60; Category 2 = 28; Category 3 = 4; Category 4 = 0.1.
Rule 3: where several breaches arise from the same root cause at the same time, only the highest-category breach is scored.
Bands by annual total: A 0; B 0.1–10; C 10.1–30; D 30.1–60; E 60.1–150; F over 150.

Site: Harrowby Sludge Treatment Centre — permit breaches recorded in 2026
1. 3 March: odour control unit fan failed for 36 hours — Category 2.
2. 3–4 March: odour beyond the site boundary (residents' complaints) — Category 3. Investigation IR-26-07 found the cause was the fan failure in item 1.
3. 30 April: monthly monitoring return submitted 6 days late — Category 4.

Site manager: "The fan was 14 years old and replacement was already in the capital plan."
""",
[("band_b", "Only breaches confirmed by sampling count toward the total, which leaves just the late return and band B."),
 ("band_c", "The odour breach shares the fan failure's cause, so only Category 2 and the late return count: 28.1."),
 ("band_d", "The odour breach has its own separate cause, so all three breaches are scored, which gives 32.1 in total."),
 ("band_e", "A Category 2 breach on its own places the site in band E.")],
"band_c", 2),

# ------------------------------------------------------------------ in12
# why: request must be >= 3 months after the inspection AND no request in the previous 12 months.
# 20 Aug 2026 is 3.5 months after 4 May -> ok; previous request 15 Sept 2025 is within 12 months -> no.
Y("in12", "Can the council accept the request for a re-rating visit?",
"""
Brackley District Council — Food Hygiene Re-rating Visits

R1. A business may request one re-rating visit after it has made the improvements set out in its inspection report.
R2. The request can be accepted only if (a) it is made at least three months after the date of the inspection that gave the current rating, and (b) the business has not made another re-rating request in the 12 months before this request.
R3. A fee of £210 is payable; the visit takes place within three months of the request.

Business: Zhou's Kitchen, 44 Market Street
Current rating: 2, from inspection on 4 May 2026
Re-rating request received: 20 August 2026, fee paid
Previous re-rating request: 15 September 2025 (after the 2025 inspection)
Owner's letter: "The officer said at the time we could have a quick revisit whenever we were ready."
""",
[("accept_request", "The request is at least three months after the inspection and no other request was made in the 12 months before it."),
 ("refuse_request", "The request fails the timing rule or the once-in-12-months rule.")],
0, 2),

# ------------------------------------------------------------------ in13
# why: the blocker is in third-party content from a provider chosen in 2023 (before 1 Jan 2026) -> excluded.
# Own content: 0 blockers, 4 serious -> 3-6 serious -> partially accessible.
# Twin: provider chosen March 2026 -> blocker counts -> not accessible.
C("in13", "Which accessibility status should the audit give the website?",
"""
Kerrow Licensing Authority — Website Accessibility Audit Rubric

Statuses
 Accessible: no blockers and at most 2 serious issues.
 Partially accessible: no blockers and 3–6 serious issues.
 Not accessible: any blocker, or more than 6 serious issues.
Third-party content: issues inside embedded third-party content (for example a payment provider's frame) are logged separately and do not count toward the status, unless the Authority chose that provider on or after 1 January 2026.

Audit — licensing.kerrow.example, 10 September 2026
Blockers: 1 — the card payment frame cannot be completed by keyboard alone. Payment provider: Paydock, contracted in May 2023.
Serious issues (Authority's own pages): 4 — missing form labels on two forms; low-contrast link text; one PDF without tags.
Moderate issues: 11.
Web team note: "Paydock says a keyboard fix is on its roadmap."
""",
[("accessible", "Serious issues only count toward the status when there are more than six of them, so the site is accessible."),
 ("partially_accessible", "The blocker is in third-party content chosen before 2026, leaving four serious issues and no blockers."),
 ("not_accessible", "The blocker in the payment frame counts because the provider was chosen on or after 1 January 2026.")],
"partially_accessible", 2,
twin=T([("Payment provider: Paydock, contracted in May 2023.", "Payment provider: Paydock, contracted in March 2026.")], "not_accessible")),

# ------------------------------------------------------------------ in14
# why: gas safety certificate dated 3 Aug 2025; inspection 29 Sept 2026 -> over 12 months -> mandatory item fails -> fail
# regardless of 88 points.
C("in14", "What certification decision follows from the short-let safety inspection?",
"""
Halden Coast Holiday Lettings Scheme — Safety Certification Rules

M1. Mandatory items (any failure means the property fails, whatever its points):
 (a) a working smoke alarm on every floor;
 (b) a carbon monoxide alarm in every room with a fuel-burning appliance;
 (c) a gas safety certificate issued within the 12 months before the inspection date.
P1. Other checklist items give points out of 100.
P2. If all mandatory items are met: 80+ points — certify; 70–79 — certify with conditions (fix within 28 days); below 70 — fail.

Inspection — Gull Cottage, 3 Quay Steps. Date: 29 September 2026.
Smoke alarms: ground floor and first floor, both working.
Gas boiler in kitchen; CO alarm fitted in kitchen, working.
Gas safety certificate: dated 3 August 2025.
Points: 88.
Owner's note: "The gas engineer is booked for next month as usual."
""",
[("certify", "The property scores 88 and every mandatory item is met, including a gas certificate less than 12 months old."),
 ("certify_with_conditions", "An out-of-date certificate can be renewed within 28 days as a condition of certification."),
 ("fail", "The gas safety certificate is more than 12 months old, a mandatory failure whatever the points.")],
"fail", 1),

# ------------------------------------------------------------------ in15
# why: excused only if road closure logged AND under 30 min over: #1 (20 min, logged) and #2 (25 min, logged) excused;
# #3 (50 min, none) and #4 (15 min, not a logged closure) count -> 2/120 = 1.67% <= 2% -> compliant.
# Twin: #1 45 min over -> not excused -> 3/120 = 2.5% -> not compliant.
Y("in15", "Is the operator rated compliant on driver hours?",
"""
Norland County Transport — School Bus Operator Audit: Driver Hours

H1. Limits: no more than 10 hours of duty in a day.
H2. The auditor samples driver-days. The operator is rated compliant if exceedances are 2% or less of sampled driver-days.
H3. An exceedance is excused (not counted) only if it was caused by a road closure recorded in the operator's incident log AND the driver was less than 30 minutes over the limit.

Audit — Greyfriars Coaches, sample of 120 driver-days (April–July 2026)
Exceedances found:
 1. 14 May — 20 minutes over; A-road closure logged (INC-5521)
 2. 2 June — 25 minutes over; bridge closure logged (INC-5610)
 3. 19 June — 50 minutes over; no incident logged
 4. 7 July — 15 minutes over; driver stopped for a pupil taken ill, recorded in the driver's notes only
Operator's statement: "Our drivers always put the children first."
""",
[("compliant", "Counted exceedances are 2% or less of the sampled driver-days."),
 ("not_compliant", "Counted exceedances are more than 2% of the sampled driver-days.")],
1, 3,
twin=T([(" 1. 14 May — 20 minutes over;", " 1. 14 May — 45 minutes over;")], 0)),

# ------------------------------------------------------------------ in16
# why: 100 - 2*2 (harsh braking) - 2*5 (speeding 12 and 15 km/h over; 7 over does not count) = 86; phone event in
# workshop test mode is void -> 86 -> green. Twin: phone event counts -> 76 -> amber.
C("in16", "Which band does the driver's monthly telematics score fall into?",
"""
Lumen Freight — Driver Safety Score (telematics), Fleet Policy FP-11

Score starts at 100 each month. Deductions:
 Harsh braking: −2 per event
 Speeding 10 km/h or more over the limit: −5 per event (readings under 10 km/h over are not counted)
 Handheld phone use while moving: −10 per event
Events recorded while the vehicle is in workshop test mode are void.
Bands: 85 or more — Green; 70–84 — Amber (coaching session); below 70 — Red (vehicle use suspended pending review).

Driver: Jamal Idowu — August 2026
Harsh braking: 14 Aug, 27 Aug
Speeding: 5 Aug (12 km/h over); 19 Aug (15 km/h over); 22 Aug (7 km/h over)
Phone use while moving: 30 Aug, 11:02 — vehicle status: workshop test mode (brake test after service)
Previous month: Amber.
""",
[("green", "The phone event is void as test mode and the 7 km/h reading does not count, which leaves 86."),
 ("amber_coaching", "The phone-use event counts, which brings the score into the 70–84 band."),
 ("red_suspend", "Any phone-use event while moving means vehicle use is suspended pending review, whatever the score.")],
"green", 2,
twin=T([("vehicle status: workshop test mode (brake test after service)", "vehicle status: normal driving (delivery route 14)")], "amber_coaching")),

# ------------------------------------------------------------------ in17
# why: Grade A needs all section minima (security 18, environment 16, fire 14) AND total >= 55.
# Environment 15 < 16; total 19 + 15 + 18 = 52 -> Grade B (45+ without Grade A).
C("in17", "Which facility grade should the lender's registrar assign?",
"""
Halden Museums Trust — Outgoing Loans: Borrower Facility Grading

F1. Sections scored by the registrar from the borrower's facility report: Security (max 20), Environment (max 20), Fire (max 20).
F2. Grade A: Security at least 18, Environment at least 16, Fire at least 14, AND a total of at least 55. Loan approved.
F3. Grade B: total of 45 or more where Grade A is not met. Loan approved only with a Trust courier supervising installation and removal.
F4. Below 45: loan declined.

Facility report — Wyndham Gallery, exhibition "Salt and Silver" (spring 2027)
Security: 19 (24-hour guarding, CCTV, alarmed cases)
Environment: 15 (relative humidity drifts above the agreed range on hot days)
Fire: 18
Previous loans to Wyndham (2019, 2022): returned without incident.
Wyndham's director: "We have always been treated as a Grade A venue."
""",
[("grade_a_approve", "Every section meets its Grade A minimum and the total reaches 55."),
 ("grade_b_with_courier", "The Environment section falls short of its Grade A minimum, and the total is at least 45."),
 ("decline_loan", "Any section scoring below its Grade A minimum means the loan is declined, whatever the total.")],
"grade_b_with_courier", 1),

# ------------------------------------------------------------------ in18
# why: risk = likelihood 3 x severity 4 = 12 -> 8-14 = repair within 14 days, not immediate closure.
Y("in18", "Must the swing be taken out of use immediately?",
"""
Brackley District Council — Play Area Annual Inspection: Risk Actions

Risk score = likelihood (1–5) x severity (1–5)
 15 or more: take out of use immediately and fence off.
 8–14: repair within 14 days; equipment stays open.
 Below 8: monitor at the next routine inspection.

Inspection — Elm Park play area, 17 September 2026
Item 4: two-seat cradle swing — chain links worn at the top shackle (about 30% wear).
Likelihood: 3
Severity: 4
Last year's inspection: same item scored 2 x 4 = 8.
Other items: roundabout bearing noise (2 x 2 = 4); surfacing edge lifted by the slide (2 x 3 = 6).
Inspector's note: "Heavily used after school; parents have raised the chain noise with the parish council."
""",
[("take_out_of_use", "The risk score is 15 or more."),
 ("keep_open", "The risk score is below 15.")],
0, 1),
]
