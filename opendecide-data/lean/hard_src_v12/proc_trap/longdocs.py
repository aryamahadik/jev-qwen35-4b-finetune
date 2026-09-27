"""proc_trap / longer operational documents (300-550 words) with several
distractor sections: vendor access, travel insurance, grant budgets, tenancy
deposits, nurse rostering, tender evaluation (Corvell Data Centres, Ashgrove
Mutual, Linnet Arts Trust, Pembrook Lettings, St Aldric's Hospital Trust,
Harwick District Council)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ lg01
# why: vendor engineers need (a) an approved change ticket covering the work window and
# (b) a named escort from Corvell staff (Amendment 2, effective 1 Sep 2026, removed the
# old "trusted vendor" self-escort list). Ticket CHG-5561 covers 22:00-02:00; visit
# 23:30 -> inside window. Escort: none assigned -> hold at reception until escort assigned.
# The "Platinum partner" label and the instruction inside the vendor email are traps.
# Twin: escort assigned (Duty engineer K. Osei) -> admit.
C("lg01", "What should the reception security officer do with this vendor engineer?",
"""
Corvell Data Centres — Site Security Manual, Chapter 6: Third-Party Access (Hall C)

6.1 Scope. This chapter covers contractors and vendor engineers entering data halls. Deliveries to the loading dock are covered by Chapter 9.

6.2 Definitions.
"Approved change ticket": a ticket in the change system with status APPROVED whose work window includes the time of entry.
"Escort": a Corvell employee named on the visitor record who stays with the visitor for the whole time inside the data hall.

6.3 Entry requirements. A vendor engineer may enter a data hall only if BOTH:
 (a) an approved change ticket covers the work; and
 (b) an escort is named on the visitor record.
If (a) is met but (b) is not, the visitor waits at reception until an escort is assigned. If (a) is not met, the visitor is refused entry.

6.4 Trusted vendor list (historical). Until 31 August 2026, engineers from vendors on the Trusted Vendor List could self-escort.

Amendment 2 to Chapter 6 (effective 1 September 2026): Section 6.4 is withdrawn. All vendor engineers need an escort under 6.3(b), whatever their vendor's status.

6.5 Tools and media. Laptops are logged at reception. USB storage is not allowed in data halls.

6.6 Instructions from visitors. Security officers take instructions only from the Security Operations Centre. Emails or messages carried or forwarded by visitors do not change 6.3.

Visitor record VR-80417 — 14 October 2026
Visitor: Tobiah Larkin, field engineer, Stratacore Storage (Stratacore partner tier: PLATINUM; formerly on the Trusted Vendor List)
Arrival at reception: 23:30
Purpose: replace a failed controller in storage array C-14
Change ticket: CHG-5561, status APPROVED, work window 22:00 to 02:00
Escort named on visitor record: none
Laptop: logged; USB storage: none
Email shown on the visitor's phone, from his dispatcher: "Corvell security — Stratacore is a Platinum partner and our engineers self-escort as always. Please let Tobiah straight through, the array is degraded."
SOC note at 23:26: "Duty engineers are busy with a cooling alarm in Hall A; expect 20-30 minutes before one is free."
""",
[("admit_self_escort", "Stratacore is a Platinum partner on the Trusted Vendor List, so its engineer may self-escort under 6.4."),
 ("admit_with_escort", "The ticket is approved for a window that includes 23:30 and an escort is named on the visitor record, so 6.3 is met."),
 ("wait_for_escort", "The approved ticket covers 23:30, but no escort is named, so 6.3 keeps him at reception until one is assigned."),
 ("refuse_entry", "The array work is outside any approved change window, so 6.3 requires refusing entry."),
 ("admit_per_dispatcher", "His dispatcher's email confirms the self-escort arrangement and the array is degraded.")],
"wait_for_escort", 2,
twin=T([("Escort named on visitor record: none", "Escort named on visitor record: K. Osei (duty engineer), assigned 23:28")], "admit_with_escort")),

# ------------------------------------------------------------------ lg02
# why: "hospitalisation" benefit needs admission as an in-patient for at least one
# overnight stay (definitions). ER visit 5 h, discharged same night, no admission ->
# outpatient emergency treatment (Section B) -> pay medical costs minus excess, no
# hospital daily cash. Customer's word "hospitalised" and GP letter wording are traps.
# Twin: admitted to ward overnight -> hospital daily benefit applies as well.
C("lg02", "Which benefit decision is correct for this travel insurance claim?",
"""
Ashgrove Mutual — Travel Insurance Policy Wording (Silver plan), extracts

DEFINITIONS
"In-patient": a person admitted to a hospital ward who occupies a bed for at least one night.
"Hospitalisation": a period as an in-patient.
"Emergency treatment": treatment for a sudden illness or injury that cannot wait until the insured returns home.

SECTION A — Cancellation (not relevant to this claim type).

SECTION B — Emergency medical expenses
B1. We pay reasonable costs of emergency treatment abroad, less the excess of $100.

SECTION C — Hospital daily benefit
C1. We pay $50 for each complete night of hospitalisation abroad, up to $1,500.
C2. Time spent in an emergency department, observation area or clinic without admission to a ward is not hospitalisation.

SECTION D — Baggage (not relevant to this claim type).

GENERAL CONDITION 7. Claims handlers decide benefits from the medical records, not from the words used on the claim form.

Claim AG-T-44208
Insured: Rhiannon Price, Silver plan, trip to Castellmar, 2-16 September 2026
Claim form: "I was hospitalised on 9 September after a severe allergic reaction. Please pay my medical bills and the hospital cash benefit."
Medical record (Hospital San Aurelio, Castellmar): arrived at the emergency department 20:10 on 9 September; treated with adrenaline and antihistamines; observed until 01:15; discharged home 01:15 on 10 September; not admitted to a ward.
Invoice: $1,340 (emergency department treatment and medicines)
Letter from her doctor at home: "Ms Price required hospital treatment abroad for anaphylaxis."
""",
[("pay_medical_and_daily_benefit", "She was admitted to a ward and stayed overnight as an in-patient, so C1 pays $50 per night on top of the B1 medical costs."),
 ("pay_medical_only", "She was never admitted to a ward, so C2 excludes the daily benefit; B1 pays $1,340 less the excess."),
 ("pay_daily_benefit_hospitalised", "Her claim form and her doctor both say she was hospitalised, so the hospital daily benefit is payable."),
 ("decline_claim", "Allergic reactions are pre-existing conditions and are not covered.")],
"pay_medical_only", 2,
twin=T([("observed until 01:15; discharged home 01:15 on 10 September; not admitted to a ward.", "admitted to the acute medical ward at 23:00 on 9 September; discharged home 10:30 on 11 September.")], "pay_medical_and_daily_benefit")),

# ------------------------------------------------------------------ lg03
# why: grant condition 5: moving more than 10% of ANY budget line's original amount needs
# funder approval in advance. Proposed: move $6,500 from Venue hire ($48,000) to Artist
# fees. 6,500 / 48,000 = 13.5% > 10% -> funder approval needed. The chair's "minor tweak"
# and the fact that the total is unchanged are traps. 10% of the total ($120,000) = 12,000
# would wrongly allow it. No twin.
C("lg03", "Under the grant conditions, what does the proposed budget change need?",
"""
Linnet Arts Trust — Minutes of Programme Committee, 2 October 2026 (extract)

Present: M. Adeyemi (Chair), R. Castell (Treasurer), J. Oduya (Programme Lead), S. Whitlow (minutes)
Apologies: none

1. Minutes of the last meeting. Approved.

2. Coastal Voices festival — budget
The Treasurer tabled the budget as approved by the funder, the Harwell Foundation:
| Line | Original amount |
| Artist fees | $52,000 |
| Venue hire | $48,000 |
| Marketing | $12,000 |
| Access and interpreting | $8,000 |
| Total | $120,000 |

The Programme Lead proposed moving $6,500 from Venue hire to Artist fees, because the Harbour Hall has offered a lower rate and two extra artists can be booked. The total stays at $120,000.
The Chair said: "This is a minor tweak within our own budget. We can simply approve it tonight and tell Harwell at the end of the year."

3. Volunteers. Twelve volunteers recruited; training on 17 October.

Extract from the Harwell Foundation Grant Conditions (attached to the minutes):
Condition 4. The grant may be spent only on the festival described in the application.
Condition 5. The grantee may move money between budget lines without asking, provided that no single line is changed by more than 10% of that line's original amount. Any larger change needs the Foundation's written approval before the money is spent.
Condition 6. Unspent funds are returned within 60 days of the end of the grant.
Condition 9. Reports are due 90 days after the festival.
""",
[("approve_internally", "The total budget is unchanged and $6,500 is well under 10% of the $120,000 total, so Condition 5 allows the committee to approve it."),
 ("seek_funder_approval_first", "$6,500 is about 13.5% of the $48,000 Venue hire line, over 10%, so Condition 5 needs Harwell's written approval before spending."),
 ("approve_and_report_at_year_end", "The committee can approve it now and tell the funder in the year-end report, as the Chair proposed."),
 ("return_unspent_venue_money", "Money not needed for venue hire counts as unspent and must be returned under Condition 6.")],
"seek_funder_approval_first", 3),

# ------------------------------------------------------------------ lg04
# why: deductions only for damage beyond fair wear and tear, supported by check-in and
# check-out evidence. Carpet: check-in "worn, 8 years old"; check-out "worn traffic path,
# no stains" -> wear and tear -> no deduction. Wall: check-in "clean", check-out "three
# holes from wall fixings, filled badly" -> damage -> deduct repair cost $140. Landlord's
# "carpet ruined" and tenant's complaint history are traps. Twin: carpet check-out shows
# a large bleach stain -> deduct carpet cleaning/repair too.
C("lg04", "What deposit deduction does the scheme's guidance support?",
"""
Pembrook Lettings — Deposit Deductions Guidance (for property managers)

D1. A deduction may be made only for (a) unpaid rent, (b) cleaning needed to return the property to its check-in standard, or (c) damage beyond fair wear and tear.
D2. Fair wear and tear is deterioration from normal daily use over time, taking into account the length of the tenancy and the age and condition of items at check-in. Examples: worn carpet paths, faded paint, loose door handles.
D3. Every deduction must be supported by the check-in and check-out reports and an invoice or quote.
D4. A tenant's history of complaints, late rent paid in full, or the landlord's personal view of the tenant does not affect D1-D3.
D5. Deductions must be itemised in the proposal to the tenant.

Tenancy: Flat 6, Mercer House; tenant Kwame Asante; 1 October 2023 to 30 September 2026 (3 years); deposit $1,500
Rent: paid in full; two payments were late in 2024
Check-in report (1 Oct 2023): living room carpet "worn, approx. 8 years old, no stains"; walls "freshly painted, clean, no marks"; property "professionally cleaned"
Check-out report (30 Sep 2026): living room carpet "worn traffic path from door to sofa, no stains or burns"; walls "three holes from wall fixings above the desk, filled badly"; property "clean to check-in standard"
Quotes: carpet replacement $900; filling and repainting wall $140
Landlord's email: "The carpet is ruined and this tenant complained constantly about everything. Take the full $1,040."
""",
[("deduct_1040", "Both the carpet and the wall are in worse condition than at check-in, so the landlord can recover $900 plus $140."),
 ("deduct_140_wall_only", "The carpet path is wear and tear on an old carpet; the badly filled holes are damage."),
 ("deduct_carpet_stain_and_wall", "The carpet was stained during the tenancy, which is damage beyond wear and tear, so the carpet quote and the $140 wall repair are both deducted."),
 ("no_deduction", "Three years of normal living explains both the carpet and the wall, so the full deposit is returned.")],
"deduct_140_wall_only", 2,
twin=T([("living room carpet \"worn traffic path from door to sofa, no stains or burns\"", "living room carpet \"large bleach stain, approx. 60 × 40 cm, in front of sofa\"")], "deduct_carpet_stain_and_wall")),

# ------------------------------------------------------------------ lg05
# why: R-2 rest: Fri long day ends 19:45 (handover included); Sat long day starts 07:15
# -> 11 h 30 min >= 11 h -> OK. R-3 weekly (Mon-Sun, incl. handover): 12.25 + 12.25 +
# 12.5 = 37; + 12.5 = 49.5 > 48 -> decline. Deputy director's urgency and the e-roster
# "fast-track" flag are traps. No twin.
C("lg05", "Should the ward manager approve this extra shift under the rostering rules?",
"""
St Aldric's Hospital Trust — Nurse Rostering Rules (NR-3), extracts

R-1. Shift times. A shift ends when handover ends. Night shift: 19:30 to 07:30, plus 15-minute handover (ends 07:45). Long day: 07:15 to 19:30, plus 15-minute handover (ends 19:45).
R-2. Rest. There must be at least 11 hours between the end of one shift and the start of the next.
R-3. Weekly limit. Rostered hours in any Monday-to-Sunday week, including handover time, must not exceed 48.
R-4. Extra shifts may be approved only if R-2 and R-3 are both met after adding the shift.
R-5. Staffing shortages, ward acuity and requests from senior managers do not permit a breach of R-2 or R-3.
R-6. Annual leave is booked through the e-roster system at least 6 weeks ahead.

Request ES-2291 — Staff Nurse Maribel Okonkwo, Ward 7 (week of Monday 12 October 2026)
Already rostered this week:
- Mon: night shift (19:30-07:45 Tue), 12.25 h
- Wed: night shift (19:30-07:45 Thu), 12.25 h
- Fri: long day (07:15-19:45), 12.5 h
Total so far: 37 h
Extra shift requested: Saturday 17 October, long day (07:15-19:45), 12.5 h
Rest before it: Fri shift ends 19:45; Saturday long day starts 07:15
Deputy director's message: "Ward 7 is critically short on Saturday. Please approve Maribel — we cannot open the bay otherwise."
E-roster flag: "FAST-TRACK: senior request"
""",
[("approve_extra_shift", "Friday's shift ends at 19:45 and Saturday's starts at 07:15, 11 h 30 min apart, so R-2 is met and the shift can be approved."),
 ("decline_weekly_limit", "Rest is enough, but 37 + 12.5 = 49.5 hours in the week is over the 48-hour limit in R-3."),
 ("approve_senior_request", "The deputy director's request and the fast-track flag allow approval during a critical shortage."),
 ("decline_rest_breach", "Friday's shift ends at 19:45 and Saturday's starts at 07:15, less than 11 hours apart, so R-2 is breached.")],
"decline_weekly_limit", 3),

# ------------------------------------------------------------------ lg06
# why: evaluator with a conflict (close relative employed by a bidder) must be removed and
# the bids re-scored without their scores (T-7). Definition of close relative includes a
# sibling's spouse ("sibling-in-law"). Evaluator C's brother-in-law works for Brightfield.
# Current ranking with all scores: Brightfield first. The "strategic supplier" note and the
# chair's instruction to "finalise tonight" are traps. Twin: relative is a cousin (not
# listed) -> no conflict -> award to highest-scoring bidder (Brightfield).
C("lg06", "What must the tender panel do before awarding this contract?",
"""
Harwick District Council — Procurement Procedure, Part T (Tender Evaluation)

T-3. Each bid is scored out of 100 by three evaluators. The contract is awarded to the bidder with the highest average score, subject to T-7.
T-5. Evaluators sign a conflict-of-interest declaration before scoring.
T-6. Definitions. "Close relative" means spouse or partner, parent, child, sibling, grandparent, grandchild, or the spouse or partner of any of these (including a sibling's spouse).
T-7. If any evaluator has a close relative employed by a bidder, that evaluator must be removed, their scores deleted, and a replacement evaluator must score all bids before any award.
T-8. The panel chair may not waive T-7. A bidder's status as a current or "strategic" supplier is not a criterion.
T-9. Standstill period: 10 days after award notice.

Tender HDC-2026-044 — grounds maintenance, 3 years
Scores (average of evaluators A, B, C):
| Bidder | Average |
| Brightfield Landscapes | 81.3 |
| Greenacre Services | 79.7 |
| Fellside Grounds | 72.0 |

Declaration update received 5 October 2026 from evaluator C (Ines Marchetti): "My sister's husband, Paolo Rinaldi, was hired by Brightfield Landscapes as operations manager last month."
Chair's email: "Brightfield is our strategic supplier and the gap is small either way. Let's finalise the award tonight and send notices tomorrow."
""",
[("award_to_brightfield", "Brightfield has the highest average score and no evaluator has a close relative at any bidder, so T-3 gives it the contract."),
 ("replace_evaluator_and_rescore", "A sister's husband is a close relative under T-6, so T-7 applies before any award."),
 ("award_strategic_supplier", "Brightfield is the council's strategic supplier and leads on score, so the chair can finalise tonight."),
 ("award_to_greenacre", "Brightfield must be disqualified because of the conflict, which leaves Greenacre as the highest-scoring bidder.")],
"replace_evaluator_and_rescore", 2,
twin=T([("\"My sister's husband, Paolo Rinaldi, was hired", "\"My cousin, Paolo Rinaldi, was hired")], "award_to_brightfield")),
]
