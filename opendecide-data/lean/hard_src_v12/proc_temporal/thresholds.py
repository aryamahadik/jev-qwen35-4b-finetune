"""proc_temporal / thresholds: explicit inclusive or exclusive boundaries, ages
at a reference date, aggregation windows, quorum and vote shares, rounding before
classification (Skerry Air, Hallam Lido Club, Fenmoor Arts Council, Rendle
Credit Union, Bowcastle Tenants' Association and others)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ th01
# why: 32.0 kg: "above 23.0 and up to 32.0 inclusive" -> overweight fee 60.
# Weights read to 0.1 kg, not rounded. Twin: 32.4 -> over 32.0 -> not accepted as
# checked baggage -> must repack or ship as cargo.
C("th01", "How should the check-in agent handle this bag?",
"""
Skerry Air — Checked Baggage Rules (Economy Light fare)

B1. Allowance: one bag of up to 23.0 kg.
B2. A bag above 23.0 kg and up to 32.0 kg (inclusive) is accepted with an overweight fee of 60.
B3. A bag above 32.0 kg is not accepted as checked baggage. The passenger must repack it or send it as cargo.
B4. The scale reading is taken to one decimal place and is not rounded.
B5. Staff may not waive B3 for any reason, including connecting flights.

Check-in desk 14 — flight SK 218 to Varrow
Passenger: Emeric Obuya, Economy Light
Bag 1 scale reading: 32.0 kg
Passenger: "It's exactly on the limit — surely that's fine with no fee? The last airline let me through."
Supervisor on the radio: "If it's anywhere near 32, just tell him it's refused, we're busy."
""",
[("accept_with_fee_60", "32.0 kg is above 23.0 kg and not above 32.0 kg, so the bag goes in the overweight band."),
 ("refuse_repack_or_cargo", "The bag is above 32.0 kg, so it cannot travel as checked baggage."),
 ("accept_no_fee", "The bag is exactly at the 32.0 kg limit, so no fee is charged."),
 ("refuse_near_limit", "The supervisor told the agent to refuse bags close to 32 kg, and this one is.")],
"accept_with_fee_60", 1,
twin=T([("Bag 1 scale reading: 32.0 kg", "Bag 1 scale reading: 32.4 kg"),
        ("It's exactly on the limit", "It's only just over the limit")], "refuse_repack_or_cargo")),

# ------------------------------------------------------------------ th02
# why: senior rate = aged 65+ on 1 January of the membership year. DOB 14 Mar 1961 ->
# on 1 Jan 2026 aged 64 -> standard rate, even though 65 at the April renewal.
# Twin: DOB 14 Dec 1960 -> 65 on 1 Jan 2026 -> senior.
C("th02", "Which membership rate should the club charge for 2026?",
"""
Hallam Lido Club — Membership Rates, membership year 2026 (1 April 2026 to 31 March 2027)

Rates
Standard adult: 310
Senior: 195 — for members aged 65 or over on 1 January of the calendar year in which the membership year starts
Concession: 150 — for holders of a current Hallam Leisure Card
Family: 520 — two adults and up to three children

Notes
• Age is checked against the date of birth held on file.
• A member who reaches 65 after the reference date pays the senior rate from the following membership year.

Renewal form HLC-2026-0412
Member: Clement Aurelio
Date of birth on file: 14 March 1961
Renewal date: 4 April 2026
Hallam Leisure Card: none
Member's note: "I'm 65 now, so senior rate please."
""",
[("senior_195", "The member was 65 or over on 1 January 2026, the reference date for this membership year."),
 ("standard_310", "The member was 64 on 1 January 2026, the reference date, even though he is 65 at renewal."),
 ("senior_by_renewal_date", "The member is 65 on the renewal date of 4 April 2026, so the senior rate applies."),
 ("concession_150", "Older members qualify for the concession rate, which is lower than the senior rate.")],
"standard_310", 2,
twin=T([("Date of birth on file: 14 March 1961", "Date of birth on file: 14 December 1960")], "senior_195")),

# ------------------------------------------------------------------ th03
# why: eligibility = salary strictly below 38,000 on the day the overtime is worked.
# Raise to 38,000 effective 1 Jul. Overtime worked 24-26 Jun -> salary 36,500 then ->
# eligible -> pay overtime. Twin: overtime 1-3 Jul -> salary 38,000 -> not below ->
# not eligible -> time off in lieu only.
C("th03", "How should this overtime claim be settled?",
"""
Brackmoor Council — Overtime Scheme for Officers (Grade 5 and above)

O1. Officers whose annual basic salary is below 38,000 are paid for approved overtime at time-and-a-half.
O2. Officers whose annual basic salary is 38,000 or more receive time off in lieu (TOIL) instead of overtime pay.
O3. Salary is taken as at the date the overtime is worked, not the date of the claim.
O4. Claims must be submitted within 2 months.

HR record — Wilhelm Ashdown, planning officer
Basic salary: 36,500 until 30 June 2026; 38,000 from 1 July 2026 (annual increment)

Overtime claim OT-26-1148
Hours: 9 approved hours, worked 24–26 June 2026 (planning inquiry preparation)
Claim submitted: 14 July 2026
Payroll clerk's note: "He's on 38,000 now, so it should be TOIL."
""",
[("pay_overtime", "On the days the overtime was worked his salary was 36,500, below 38,000."),
 ("toil_only", "On the days the overtime was worked his salary was already 38,000, which is not below the threshold."),
 ("toil_by_claim_date", "When the claim was submitted his salary was 38,000, so TOIL applies."),
 ("reject_claim_late", "The claim came in after the month in which the hours were worked, so it is out of time.")],
"pay_overtime", 2,
twin=T([("worked 24–26 June 2026", "worked 1–3 July 2026")], "toil_only")),

# ------------------------------------------------------------------ th04
# why: eligibility: income under 250,000 (strictly), where income EXCLUDES capital
# grants. 262,000 - 18,000 capital grant = 244,000 -> eligible. Twin: capital grant
# 8,000 -> 254,000 -> not under -> ineligible.
C("th04", "Is this organisation eligible to apply to the small-grants round?",
"""
Fenmoor Arts Council — Small Grants Round 9: Eligibility

E1. Applicants must be constituted not-for-profit organisations based in the Fenmoor area.
E2. Applicants must have annual income under £250,000 in their most recent audited accounts.
E3. For E2, "annual income" means total income minus capital grants (grants given to buy or build buildings or equipment). Donations, trading income and revenue grants count.
E4. Previous grant holders may apply if their last grant report was accepted.

Applicant: Wickham Street Community Theatre (charity no. 1182044)
Most recent audited accounts: year to 31 March 2026
Total income: £262,000
of which capital grant (Harbourside Trust, for a new lighting rig): £18,000
of which box-office and bar income: £151,000
Previous grant report: accepted, January 2026
Officer's first-pass note: "Income over £250k on the face of the accounts — ineligible?"
""",
[("eligible", "Taking off the £18,000 capital grant leaves £244,000, which is under £250,000."),
 ("ineligible", "Taking off the capital grant still leaves income of £250,000 or more."),
 ("ineligible_total_income", "Total income of £262,000 is over £250,000, so the organisation cannot apply."),
 ("eligible_trading_excluded", "Box-office and bar income are excluded, which brings income well under £250,000.")],
"eligible", 2,
twin=T([("of which capital grant (Harbourside Trust, for a new lighting rig): £18,000", "of which capital grant (Harbourside Trust, for a new lighting rig): £8,000")], "ineligible")),

# ------------------------------------------------------------------ th05
# why: recorded speed = measured - 3 (tolerance for speeds up to 100). 64 - 3 = 61 ->
# 11 over the 50 limit -> band 11-20 -> fine 120. Twin: 63 -> 60 -> 10 over -> warning.
C("th05", "What outcome should the camera office issue?",
"""
Ferrow Road Safety Partnership — Enforcement Guidelines, fixed cameras

G1. Tolerance: for measured speeds up to 100 km/h, 3 km/h is subtracted from the measured speed to give the recorded speed. Above 100 km/h, 3% is subtracted.
G2. Outcome is set by how far the recorded speed is above the posted limit:
    1 to 10 km/h over: warning letter
    11 to 20 km/h over: fixed fine of 120
    21 km/h or more over: fine of 300 and 3 licence points
G3. Previous warnings do not change the band.

Camera event FRSP-CAM-7 / 2026-08-19 07:42
Location: Hollins Lane (posted limit 50 km/h)
Measured speed: 64 km/h
Registered keeper: Tobiah Grealish
Prior history: one warning letter, 2025
Reviewer's note: "14 over the limit, and he's had a warning before — fine plus points?"
""",
[("fine_120", "The recorded speed is 61 km/h after the 3 km/h tolerance, 11 over the limit, which is in the 11 to 20 band."),
 ("warning_letter", "The recorded speed is 60 km/h after the 3 km/h tolerance, 10 over the limit, which is in the 1 to 10 band."),
 ("fine_300_points", "He has a previous warning, so this offence moves up to the fine-and-points band."),
 ("fine_120_measured", "The measured speed of 64 km/h is 14 over the limit, and tolerance applies only above 100 km/h.")],
"fine_120", 1,
twin=T([("Measured speed: 64 km/h", "Measured speed: 63 km/h"), ("14 over the limit", "13 over the limit")], "warning_letter")),

# ------------------------------------------------------------------ th06
# why: report cash of 10,000 or more, aggregating deposits by the same member within
# any 24-hour period. 6,200 Mon 10:05 + 3,800 Tue 09:50 = 23 h 45 min apart -> linked ->
# 10,000 -> meets threshold -> file report. Twin: Tue 10:20 -> 24 h 15 min -> not linked;
# each under 10,000 -> no report.
C("th06", "Must the branch file a large-cash report for these deposits?",
"""
Rendle Credit Union — Cash Handling Manual, chapter 5 (Large cash reports)

5.1 A large-cash report must be filed for any cash deposit of 10,000 or more.
5.2 Cash deposits by the same member within any 24-hour period are added together. If the total is 10,000 or more, a report is filed.
5.3 Deposits more than 24 hours apart are not added together under 5.2.
5.4 Staff must not tell the member that a report is being considered.
5.5 Cheques and transfers are not cash and are not counted.

Branch: Rendle Market Street
Member: Oswin Calder-Pike (member since 2011; runs a farm shop)
Cash deposits:
    Monday 7 September 2026, 10:05 — 6,200.00
    Tuesday 8 September 2026, 09:50 — 3,800.00
Cheque deposit: Tuesday 8 September 2026, 09:51 — 2,400.00
Teller's note: "Two different days, and neither deposit is anywhere near ten thousand."
""",
[("file_report", "The two cash deposits are 23 hours 45 minutes apart, within 24 hours, and together make 10,000.00."),
 ("no_report", "The two cash deposits are more than 24 hours apart, and each is below 10,000."),
 ("file_report_with_cheque", "Cash and cheque deposits on Tuesday make 6,200 plus the Monday cash, well over 10,000."),
 ("no_report_different_days", "The deposits were made on different calendar days, so they are not added together.")],
"file_report", 2,
twin=T([("Tuesday 8 September 2026, 09:50 — 3,800.00", "Tuesday 8 September 2026, 10:20 — 3,800.00"),
        ("Tuesday 8 September 2026, 09:51 — 2,400.00", "Tuesday 8 September 2026, 10:21 — 2,400.00")], "no_report")),

# ------------------------------------------------------------------ th07
# why: quorum = more than half of VOTING members. 23 voting -> need 12. Present: 12
# voting + 2 non-voting (co-opted) -> quorate. Twin: 11 voting + 3 non-voting -> 11 <= 11.5
# -> not quorate.
C("th07", "Is the general meeting quorate?",
"""
Bowcastle Tenants' Association — Constitution (as amended 2024)

7.1 Voting members are tenant members whose subscriptions are paid up to date.
7.2 Co-opted members may attend and speak but may not vote.
7.3 A general meeting is quorate if the number of voting members present is more than half of all voting members.
7.4 If a meeting is not quorate, it must be adjourned to a date at least 7 days later. No decisions may be taken.
7.5 Proxies do not count towards the quorum.

Secretary's attendance sheet — special general meeting, 12 October 2026
Voting members on the register: 23
Present: 12 voting members; 2 co-opted members (housing officer, youth worker)
Proxy forms received: 3
Chair's remark: "Fourteen in the room and three proxies — seventeen out of twenty-three. We're fine."
""",
[("quorate_proceed", "Twelve voting members are present, which is more than half of 23."),
 ("not_quorate_adjourn", "Eleven voting members are present, which is not more than half of 23."),
 ("quorate_with_proxies", "Counting everyone present and the proxies gives 17 of 23, well over half."),
 ("quorate_by_headcount", "Fourteen people are present, which is more than half of the register.")],
"quorate_proceed", 1,
twin=T([("Present: 12 voting members; 2 co-opted members (housing officer, youth worker)", "Present: 11 voting members; 3 co-opted members (housing officer, youth worker, tenancy advisor)")], "not_quorate_adjourn")),

# ------------------------------------------------------------------ th08
# why: special resolution passes with at least 75% of votes cast; abstentions are not
# votes cast. 42 for / (42 + 14) = 42/56 = 75.0% -> passes. Twin: against 15 ->
# 42/57 = 73.7% -> fails. Including abstentions (42/62) would be wrong.
C("th08", "Did the special resolution pass?",
"""
Glassford Allotment Society — Rules, part 9 (Resolutions)

9.1 An ordinary resolution passes with more than half of the votes cast.
9.2 A special resolution (changes to rules, rents above inflation, dissolution) passes with at least 75% of the votes cast.
9.3 Votes cast means votes for plus votes against. Abstentions and spoilt papers are not votes cast.
9.4 The chair has no casting vote on a special resolution.

Minutes extract — AGM, 14 November 2026
Resolution 4 (special): "That annual plot rents rise from £48 to £60 from 1 April 2027."
For: 42
Against: 14
Abstentions: 6
Treasurer's remark: "Forty-two out of sixty-two in the hall is only about two-thirds."
""",
[("passed", "For votes are 42 of 56 votes cast, exactly 75%, which meets the threshold."),
 ("failed", "For votes are 42 of 57 votes cast, under 75%."),
 ("failed_counting_abstentions", "For votes are 42 of 62 members voting or abstaining, about 68%, under 75%."),
 ("passed_simple_majority", "More than half of the votes cast were in favour, which is enough.")],
"passed", 2,
twin=T([("Against: 14\nAbstentions: 6", "Against: 15\nAbstentions: 5")], "failed")),

# ------------------------------------------------------------------ th09
# why: WARNING needs 2 consecutive readings at or above 3.10 m. Readings 3.12 then
# 3.08 -> second below -> no warning; both >= 2.40 -> flood alert.
# Twin: second 3.10 -> two consecutive >= 3.10 -> flood warning.
C("th09", "Which message should the duty officer issue for the Tarrow at Kelling Bridge?",
"""
Tarrow Catchment Flood Duty Manual — Kelling Bridge gauge

K1. Readings are taken every 15 minutes.
K2. Flood alert: the latest reading is at or above 2.40 m.
K3. Flood warning: two consecutive readings are at or above 3.10 m.
K4. Severe flood warning: any reading at or above 3.80 m, or a flood warning in force with the level still rising for 2 hours.
K5. If no threshold is met, no message is issued.
K6. Forecasts do not trigger messages on their own; only gauge readings do.

Gauge log, 21 November 2026
02:15 — 2.96 m
02:30 — 3.12 m
02:45 — 3.08 m

Forecast bulletin 02:40: "Further heavy rain expected after 06:00; peak may exceed 3.5 m."
Colleague's text: "3.12 is over the warning line — send the warning now, don't wait."
""",
[("flood_alert", "The latest reading is at least 2.40 m, but the last two readings are not both at or above 3.10 m."),
 ("flood_warning", "The last two readings are both at or above 3.10 m."),
 ("severe_flood_warning", "The forecast says the river may peak above 3.5 m, so the highest level of message is needed."),
 ("no_message", "The latest reading is below 3.10 m, so no threshold is met.")],
"flood_alert", 2,
twin=T([("02:45 — 3.08 m", "02:45 — 3.10 m")], "flood_warning")),

# ------------------------------------------------------------------ th10
# why: monthly threshold 27,300 / 12 = 2,275.00; repay 9% of pay ABOVE threshold.
# 2,475 - 2,275 = 200 -> 18.00. Twin: pay 2,275.00 -> nothing above -> 0.00.
C("th10", "What study-loan deduction should this month's payslip show?",
"""
Calderon Student Finance — Employer Guide, Plan C deductions

L1. The annual repayment threshold for Plan C is 27,300.
L2. For monthly-paid staff, the threshold is applied monthly: 27,300 ÷ 12 = 2,275.00 per month.
L3. The deduction is 9% of pay above the monthly threshold, rounded down to the whole cent. If pay is at or below the threshold, the deduction is 0.00.
L4. Each pay period is looked at on its own. Pay in earlier months does not change this month's deduction.

Payroll record — Jessamy Varga, September 2026
Plan: C (start notice received 2024)
Gross pay this month: 2,475.00
Year-to-date gross: 16,900.00

Employee's email: "My yearly pay is below 27,300, so I shouldn't pay anything, right?"
Payroll assistant's draft: "9% of 2,475 = 222.75."
""",
[("deduct_18_00", "Pay is 200.00 above the 2,275.00 monthly threshold, and 9% of 200.00 is 18.00."),
 ("deduct_0_00", "Pay this month is at or below the 2,275.00 monthly threshold."),
 ("deduct_222_75", "The deduction is 9% of the whole of this month's gross pay."),
 ("deduct_0_annual", "Her expected yearly pay is below 27,300, so no deduction is taken.")],
"deduct_18_00", 1,
twin=T([("Gross pay this month: 2,475.00", "Gross pay this month: 2,275.00"), ("9% of 2,475 = 222.75.", "9% of 2,275 = 204.75.")], "deduct_0_00")),

# ------------------------------------------------------------------ th11
# why: reorder when on hand + on order <= reorder point (inclusive). ROP = 40 x 6 + 60
# = 300. 220 + 80 = 300 -> reorder. Twin: on order 90 -> 310 > 300 -> no order.
C("th11", "What should the replenishment run do for this item?",
"""
Pentwyn Hardware — Replenishment Standard (warehouse A)

R1. Reorder point = average daily usage × supplier lead time in days + safety stock.
R2. Place an order when stock on hand plus stock already on order is at or below the reorder point.
R3. Order quantity is the standard pack multiple shown on the item card.
R4. Expedite (pay for express freight) only if stock on hand alone would run out before the lead time ends.

Item card — SKU PH-44102, 50 mm galvanised wood screws, box of 200
Average daily usage: 40 boxes
Supplier lead time: 6 days
Safety stock: 60 boxes
Standard pack multiple: 240 boxes
Stock on hand: 220 boxes
Stock on order (PO 7731, due in 4 days): 80 boxes

Buyer's note: "On hand is well under 300 — we're about to run out, expedite."
""",
[("place_standard_order", "The reorder point is 300, and on hand plus on order is 300, which is at the reorder point."),
 ("no_order", "The reorder point is 300, and on hand plus on order is above it."),
 ("place_expedited_order", "Stock on hand alone is under 300, so the item needs express freight."),
 ("no_order_above_safety", "Stock on hand of 220 is above the 60-box safety stock, so no order is needed.")],
"place_standard_order", 2,
twin=T([("Stock on order (PO 7731, due in 4 days): 80 boxes", "Stock on order (PO 7731, due in 4 days): 90 boxes")], "no_order")),

# ------------------------------------------------------------------ th12
# why: approval band decided on the GROSS amount (incl. tax). 23,500 + 20% = 28,200 ->
# over 25,000 -> CFO. Twin: net 20,500 -> 24,600 -> director band.
C("th12", "Who must approve this supplier invoice?",
"""
Mardale Engineering — Delegated Authority Schedule (finance), rev. 7

A1. Invoice approval limits apply to the gross amount payable, including tax.
A2. Bands:
    up to 5,000.00: budget-holding manager
    5,000.01 to 25,000.00: department director
    over 25,000.00: chief financial officer (CFO)
A3. An approver may not approve an invoice raised by a supplier they manage the relationship with; it goes to the next band up.
A4. Tax is charged at 20% on this supplier's invoices.

Invoice MDE-AP-40917
Supplier: Kesteven Hydraulics Ltd
Net amount: 23,500.00
Tax (20%): 4,700.00
Gross amount: 28,200.00
Relationship manager for this supplier: procurement lead (not a director)
Submitter's note: "Net is under 25k — send to the director, please."
""",
[("cfo_approval", "The gross amount of 28,200.00 is over 25,000.00, so the CFO band applies."),
 ("director_approval", "The gross amount is between 5,000.01 and 25,000.00, so the department director approves."),
 ("director_by_net", "The net amount of 23,500.00 is under 25,000.00, so the director approves."),
 ("manager_approval", "The budget-holding manager can approve because the supplier relationship sits with procurement.")],
"cfo_approval", 1,
twin=T([("Net amount: 23,500.00\nTax (20%): 4,700.00\nGross amount: 28,200.00", "Net amount: 20,500.00\nTax (20%): 4,100.00\nGross amount: 24,600.00")], "director_approval")),

# ------------------------------------------------------------------ th13
# why: effective WBGT = reading + 2.0 for impermeable suits. 28.6 + 2.0 = 30.6 ->
# band ">= 30.0 and < 32.0" -> 30 min work / 30 min rest. Twin: normal overalls -> no
# adjustment -> 28.6 -> band ">= 28.0 and < 30.0" -> 45/15.
C("th13", "Which work-rest cycle must the supervisor set?",
"""
Halloway Remediation — Heat Stress Procedure HS-3

H1. Take a WBGT (wet-bulb globe temperature) reading at the work area at the start of each hour.
H2. For crews wearing impermeable chemical suits, add 2.0 °C to the reading to get the effective WBGT. For normal cotton overalls, no adjustment.
H3. Work-rest cycles per hour, by effective WBGT:
    below 28.0: continuous work
    28.0 up to but not including 30.0: 45 min work / 15 min rest
    30.0 up to but not including 32.0: 30 min work / 30 min rest
    32.0 or above: stop work
H4. A crew member's request to "push through" does not change the cycle.

Site log — former tannery, cell 3, 11:00
WBGT reading: 28.6 °C
Crew clothing: impermeable chemical suits (asbestos-contaminated soil)
Crew lead: "We only need another hour to finish the cell. 45/15 is fine."
""",
[("cycle_30_30", "The effective WBGT is 30.6 °C once the 2.0 °C suit adjustment is added, which is in the 30.0 to 32.0 band."),
 ("cycle_45_15", "No clothing adjustment applies, so the effective WBGT is 28.6 °C, which is in the 28.0 to 30.0 band."),
 ("stop_work", "Any reading above 28.0 °C in chemical suits means work must stop."),
 ("continuous_work", "The crew needs only another hour, so continuous work may go ahead.")],
"cycle_30_30", 2,
twin=T([("Crew clothing: impermeable chemical suits (asbestos-contaminated soil)", "Crew clothing: normal cotton overalls (soil already cleared of asbestos)")], "cycle_45_15")),

# ------------------------------------------------------------------ th14
# why: deadline Fri 13:00 UTC; submission Sun 15:00 UTC+1 = 14:00 UTC -> 49 h late ->
# 3 started 24-h periods -> -15 points -> 68 - 15 = 53.
# Twin: Sun 13:00 UTC+1 = 12:00 UTC -> 47 h late -> 2 started periods -> 68 - 10 = 58.
C("th14", "What mark should the module leader record for this late coursework?",
"""
Dunmere College — Assessment Regulations, rule 6 (Late submission)

6.1 The deadline for each assignment is stated in UTC in the course handbook.
6.2 Late work loses 5 marks for each 24-hour period, or part of one, after the deadline.
6.3 Work more than 5 days late receives a mark of 0.
6.4 The submission time is the time stamped by the online system, converted to UTC.
6.5 Extensions must be approved before the deadline.

Assignment: EC2104 Econometrics project
Deadline: Friday 20 March 2026, 13:00 UTC
Submission (system stamp, shown in the student's local time, UTC+1): Sunday 22 March 2026, 15:00
Marked score before penalty: 68
Extension: none
Student's email: "It's barely two days late, so minus ten, surely?"
""",
[("record_53", "In UTC the work arrived at 14:00 on Sunday, 49 hours late, which starts a third 24-hour period: 68 − 15."),
 ("record_58", "In UTC the work arrived at 12:00 on Sunday, 47 hours late, which is within two 24-hour periods: 68 − 10."),
 ("record_48", "Counting in local time, 15:00 is 50 hours after 13:00 Friday, so four periods are started: 68 − 20."),
 ("record_0", "The work was submitted after the deadline without an extension, so it receives 0.")],
"record_53", 3,
twin=T([("Sunday 22 March 2026, 15:00", "Sunday 22 March 2026, 13:00")], "record_58")),

# ------------------------------------------------------------------ th15
# why: night hours 23:00-07:00. Warning if level EXCEEDS 45 dB; fixed penalty if
# EXCEEDS 55 dB. Reading 55.0 at 23:10 -> exceeds 45, not 55 -> warning.
# Twin: 55.3 -> exceeds 55 -> fixed penalty notice.
C("th15", "What enforcement step should the noise team take?",
"""
Lanchester District Council — Night Noise Protocol (domestic premises)

N1. Night hours are 23:00 to 07:00.
N2. Measurements are LAeq over 5 minutes, taken inside the complainant's home with windows closed.
N3. During night hours:
    level exceeding 45 dB: warning notice to the source address
    level exceeding 55 dB: fixed penalty notice (no warning needed first)
N4. Outside night hours, the daytime protocol applies instead.
N5. Previous complaints do not change the thresholds.

Visit record NT-26-0918
Complainant: ground-floor flat, 7 Sackville Terrace
Source: first-floor flat, 7 Sackville Terrace
Measurement: 23:10–23:15, Saturday 19 September 2026
LAeq,5min: 55.0 dB
Previous complaints about this address: 4 (none measured)
Officer's radio note: "Right on 55. With all those past complaints I'd go straight to the penalty."
""",
[("warning_notice", "The level exceeds 45 dB but does not exceed 55 dB, during night hours."),
 ("fixed_penalty_notice", "The level exceeds 55 dB during night hours."),
 ("fixed_penalty_history", "There have been four previous complaints, so the penalty can be issued at this level."),
 ("no_action_daytime", "The measurement was taken before midnight, so the daytime protocol applies.")],
"warning_notice", 1,
twin=T([("LAeq,5min: 55.0 dB", "LAeq,5min: 55.3 dB"), ("Right on 55.", "Just over 55.")], "fixed_penalty_notice")),

# ------------------------------------------------------------------ th16
# why: weekly rent = monthly x 12 / 52 = 1,300 x 12 / 52 = 300. Annual rent 15,600 <
# 50,000 -> cap 5 weeks = 1,500. Deposit 1,560 -> 60 over -> refund 60 excess.
# Twin: deposit 1,500 -> at cap -> compliant, no action.
C("th16", "What should the compliance team do about this tenancy deposit?",
"""
Harrowgate Lettings — Compliance Checklist, item D (Deposits)

D1. Weekly rent = monthly rent × 12 ÷ 52.
D2. The deposit may not be more than 5 weeks' rent where annual rent is under 50,000, or 6 weeks' rent where annual rent is 50,000 or more.
D3. If the deposit is over the cap, refund the excess to the tenant within 14 days. The tenancy is not affected.
D4. A holding deposit is separate and is not counted once it has been credited to the first month's rent.

Tenancy file HL-2026-2241 — 11 Chandlers Walk
Tenant: Florian Adebayo-Kerr
Monthly rent: 1,300
Deposit taken: 1,560
Holding deposit: 300, credited to first month's rent on 1 June 2026
Letting negotiator's note: "Weekly rent is 1,300 ÷ 4 = 325, so the cap is 1,625. We're fine."
""",
[("refund_excess_60", "Weekly rent is 300, so the 5-week cap is 1,500, and the deposit is 60 over it."),
 ("compliant_no_action", "Weekly rent is 300, so the 5-week cap is 1,500, and the deposit does not exceed it."),
 ("compliant_by_4_weeks", "Weekly rent is 1,300 ÷ 4 = 325, so the cap is 1,625 and the deposit is under it."),
 ("refund_excess_360", "The holding deposit is added to the deposit, making 1,860, which is 360 over the cap.")],
"refund_excess_60", 2,
twin=T([("Deposit taken: 1,560", "Deposit taken: 1,500")], "compliant_no_action")),

# ------------------------------------------------------------------ th17
# why: diesel cars comply if Euro 6; with no certificate, first registration on or
# after 1 Sep 2015 is treated as Euro 6. First registered 1 Sep 2015 -> on/after ->
# compliant -> no charge. Twin: 31 Aug 2015 -> before -> non-compliant -> 12.50.
C("th17", "Should this car be charged for entering the clean air zone?",
"""
Branwick City Council — Clean Air Zone (Class C) Charging Rules

Z1. Diesel cars meet the standard if they are Euro 6. Petrol cars meet the standard if they are Euro 4 or later.
Z2. Where no manufacturer's certificate is on file, a diesel car first registered on or after 1 September 2015 is treated as Euro 6, and one first registered before that date is treated as not meeting the standard.
Z3. Cars that do not meet the standard pay 12.50 per day of entry.
Z4. The daily charge period is midnight to midnight.

ANPR entry record CAZ-B-0918-4417
Date: 18 September 2026, 08:14
Vehicle: diesel hatchback
First registration date (from registry): 1 September 2015
Manufacturer's certificate on file: none
Driver's appeal note (sent in advance): "My car is ten years old — I expect you'll charge me, but it runs clean."
""",
[("no_charge", "The diesel car was first registered on or after 1 September 2015, so it is treated as Euro 6."),
 ("charge_12_50", "The diesel car was first registered before 1 September 2015 and has no certificate, so it does not meet the standard."),
 ("charge_12_50_by_age", "The car is about ten years old, and cars that old do not meet the standard."),
 ("no_charge_driver_statement", "The driver states that the car runs clean, which is enough to meet the standard.")],
"no_charge", 1,
twin=T([("First registration date (from registry): 1 September 2015", "First registration date (from registry): 31 August 2015")], "charge_12_50")),

# ------------------------------------------------------------------ th18
# why: final average rounded to 1 d.p. (0.05 rounds up) BEFORE classification.
# 69.95 -> 70.0 -> First. Twin: 69.94 -> 69.9 -> in borderline zone 68.0-69.9 ->
# refer to exam board.
C("th18", "What classification should the degree system record?",
"""
Aldwyck University — Degree Classification Rules (undergraduate)

D1. The final average is calculated from year 2 (weight 40%) and year 3 (weight 60%) module marks.
D2. The final average is rounded to one decimal place before classification. A second decimal of 5 or more rounds up (for example, 59.95 becomes 60.0).
D3. Classes by rounded average: First 70.0 and above; Upper second 60.0 to 69.9; Lower second 50.0 to 59.9; Third 40.0 to 49.9.
D4. A student whose rounded average is 68.0 to 69.9 is a borderline case and is referred to the exam board, which decides between First and Upper second.
D5. The exam board may not look at averages outside D4.

Student record — Oona Castellanos, BSc Marine Biology
Year 2 weighted contribution: 27.38
Year 3 weighted contribution: 42.57
Unrounded final average: 69.95
Programme administrator's note: "69.95 is below 70. Upper second, surely — or refer?"
""",
[("award_first", "The average rounds to 70.0, which is at the First boundary."),
 ("refer_to_exam_board", "The average rounds to 69.9, inside the 68.0 to 69.9 borderline range."),
 ("award_upper_second", "The unrounded average of 69.95 is below 70.0, so it is an Upper second."),
 ("award_first_by_year_3", "The year 3 contribution is the larger part of the average, so the board awards a First.")],
"award_first", 2,
twin=T([("Year 3 weighted contribution: 42.57\nUnrounded final average: 69.95", "Year 3 weighted contribution: 42.56\nUnrounded final average: 69.94"),
        ("69.95 is below 70.", "69.94 is below 70.")], "refer_to_exam_board")),

# ------------------------------------------------------------------ th19
# why: 9 h daily driving limit; may extend to 10 h at most twice in a fixed week
# (Mon 00:00 - Sun 24:00). Extensions this week: Mon 10.0, Thu 10.0, Fri 9.5 ->
# third extension -> infringement. Previous week's Sunday extension does not count.
# Twin: Fri 9.0 -> not an extension (9 h is the limit) -> compliant.
C("th19", "Does this driver's week comply with the driving-time rules?",
"""
Harlow Haulage — Drivers' Hours Policy (mirrors national rules)

DH1. Daily driving must not exceed 9 hours.
DH2. Twice in a fixed week, daily driving may be extended to not more than 10 hours. Any day with more than 9 hours of driving counts as one extension.
DH3. A fixed week runs from 00:00 Monday to 24:00 Sunday.
DH4. A third extension in the same fixed week is an infringement and must be reported to the transport manager.
DH5. Weekly driving must not exceed 56 hours.

Tachograph summary — driver Radomir Petrakis
Previous week, Sunday 13 September 2026: 10.0 h
Monday 14 September: 10.0 h
Tuesday 15 September: 8.5 h
Wednesday 16 September: 7.0 h
Thursday 17 September: 10.0 h
Friday 18 September: 9.5 h
Saturday/Sunday: rest
Weekly total: 45.0 h
Planner's note: "Only two 10-hour days this week, and nowhere near 56."
""",
[("report_infringement", "Monday, Thursday and Friday each had more than 9 hours of driving, a third extension in the fixed week."),
 ("compliant", "Only Monday and Thursday had more than 9 hours of driving, so two extensions were used."),
 ("report_weekly_limit", "Weekly driving went over 56 hours once the previous Sunday is included."),
 ("report_sunday_monday", "The Sunday and Monday 10-hour days were back to back, which is an infringement in itself.")],
"report_infringement", 2,
twin=T([("Friday 18 September: 9.5 h\nSaturday/Sunday: rest\nWeekly total: 45.0 h", "Friday 18 September: 9.0 h\nSaturday/Sunday: rest\nWeekly total: 44.5 h")], "compliant")),

# ------------------------------------------------------------------ th20
# why: threshold 42,000 for households with up to 2 dependants + 6,000 per dependant
# beyond 2. 4 dependants -> 42,000 + 12,000 = 54,000. Income 54,000 is "at or below" ->
# eligible. Twin: income 54,100 -> above -> not eligible.
C("th20", "Does this applicant meet the bursary income test?",
"""
Kestrel Trust Bursaries — Guidance for assessors, 2026 entry

I1. Household income is the total gross income of the applicant's parents or guardians for the tax year ending April 2026.
I2. The income limit is 42,000 for a household with up to 2 dependent children, plus 6,000 for each dependent child beyond 2.
I3. The applicant counts as one of the dependent children.
I4. An applicant meets the test if household income is at or below the limit.
I5. Savings are not assessed.

Application KT-26-0714
Applicant: Seren Mwangi (age 17)
Dependent children in household, including the applicant: 4
Household gross income, tax year ending April 2026: 54,000
Savings: 11,300
Assessor's scribble: "Three siblings plus Seren = five? Limit 60k?"
""",
[("meets_test", "Four dependent children give a limit of 42,000 + 2 × 6,000 = 54,000, and income is at or below it."),
 ("fails_test", "Four dependent children give a limit of 54,000, and income is above it."),
 ("meets_test_limit_60k", "Counting the applicant on top of the siblings gives five children and a limit of 60,000."),
 ("fails_test_savings", "Household savings of 11,300 take the household over the limit.")],
"meets_test", 1,
twin=T([("Household gross income, tax year ending April 2026: 54,000", "Household gross income, tax year ending April 2026: 54,100")], "fails_test")),

# ------------------------------------------------------------------ th21
# why: ban on vehicles OVER 7.5 t maximum authorised mass (plate), not laden weight;
# access exception only for deliveries to premises reached from the restricted road.
# Plated 7.5 t -> not over -> allowed. Twin: plated 7.7 t -> over; through route, no
# access -> penalty notice.
C("th21", "Should the enforcement team issue a penalty for this lorry on Mill Bridge?",
"""
Sedgebury County Council — Traffic Regulation Order 2025/14, Mill Bridge weight limit

Article 2. No vehicle with a maximum authorised mass (the weight shown on its plate) over 7.5 tonnes may use Mill Bridge.
Article 3. Actual laden weight on the day is not relevant to Article 2.
Article 4. Exception: vehicles needing access to premises that can only be reached by crossing the bridge.
Article 5. A vehicle in breach of Article 2, with no exception, receives a penalty notice of 150.

Camera log MB-0923-07 — 23 September 2026, 06:52, northbound
Vehicle: box lorry, operator Fenwick Removals
Plated maximum authorised mass: 7.5 tonnes
Weighbridge estimate on the day: 6.1 tonnes laden
Journey (from operator's tracking): Harlow depot to Stoke Ferris, through route; no stop north of the bridge
Resident's complaint on file: "Lorries this big are wrecking the bridge — fine every one of them."
""",
[("no_penalty", "The plated maximum authorised mass is 7.5 tonnes, which is not over the 7.5-tonne limit."),
 ("issue_penalty_150", "The plated maximum authorised mass is over 7.5 tonnes, and a through journey does not qualify for the access exception."),
 ("no_penalty_laden_weight", "The lorry's laden weight on the day was 6.1 tonnes, below 7.5 tonnes, which is what counts."),
 ("issue_penalty_complaint", "Residents have complained about lorries of this size, so the notice is issued.")],
"no_penalty", 2,
twin=T([("Plated maximum authorised mass: 7.5 tonnes", "Plated maximum authorised mass: 7.7 tonnes")], "issue_penalty_150")),

# ------------------------------------------------------------------ th22
# why: recall if 2+ samples EXCEED 20 cfu/g, or any sample at or above 100. Samples
# 18, 20, 64, 9 -> only 64 exceeds 20 (20 does not exceed 20); none >= 100 -> no
# recall; one exceedance -> hold batch and retest. Twin: 20 -> 21 -> two exceed -> recall.
C("th22", "What should quality assurance do with batch 2611-C?",
"""
Pelham Dairy Co-operative — Microbiology Release Procedure, soft cheese line

Q1. Four samples are taken from each batch. The action limit is 20 cfu/g.
Q2. Recall the batch if two or more samples exceed the action limit, or if any single sample is at or above 100 cfu/g.
Q3. If exactly one sample exceeds the action limit and none is at or above 100 cfu/g, hold the batch and retest with four new samples.
Q4. If no sample exceeds the action limit, release the batch.
Q5. Results are reported as whole numbers by the lab.

Lab report LR-2611-C (batch 2611-C, made 14 September 2026)
Sample 1: 18 cfu/g
Sample 2: 20 cfu/g
Sample 3: 64 cfu/g
Sample 4: 9 cfu/g
Production manager's note: "Three of four are fine — release it, the customers are waiting."
""",
[("hold_and_retest", "Only sample 3 exceeds 20 cfu/g, and no sample is at or above 100 cfu/g."),
 ("recall_batch", "Two samples exceed 20 cfu/g, which triggers a recall."),
 ("release_batch", "Most samples are within the action limit, so the batch can be released."),
 ("recall_single_high", "Sample 3 is more than three times the action limit, which triggers a recall on its own.")],
"hold_and_retest", 2,
twin=T([("Sample 2: 20 cfu/g", "Sample 2: 21 cfu/g")], "recall_batch")),
]
