"""reason_c / HR leave, payroll and employee expenses (Lindqvist Analytics,
Oakhollow Council, Corrigan & Vale LLP, Petrel Biscuits, Saltmarsh Housing)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ hr01
# why: working day (Tue), journey starts and ends at home -> deduct normal round-trip
# commute 2 x 12 = 24. Total 52 + 30 + 12 = 94 -> 94 - 24 = 70 miles x $0.58 = $40.60.
# YTD 6,200 miles, so all at the first-tier rate.
# Twin: Saturday (not a working day for this employee) -> no deduction -> 94 x 0.58 = $54.52.
C("hr01", "How much mileage should be reimbursed for this journey?",
"""
Lindqvist Analytics — Expenses policy, section 6 (private car use)

6.1 Rate: $0.58 per business mile for the first 10,000 business miles in the tax year; $0.30 per mile after that.
6.2 On a normal working day, when a business journey starts and ends at the employee's home, deduct the employee's normal round-trip commute (home-office-home) from the claimed miles.
6.3 On days the employee does not normally work, no commute deduction applies.
6.4 Parking is reimbursed at cost with a receipt; fines are never reimbursed.

Mileage claim MC-3310
Employee: Farah Adeyemi, works Monday to Friday. Normal commute: 12 miles each way.
Business miles already claimed this tax year: 6,200.
Date: Tuesday 15 September 2026.
Legs: home -> Castell Paper (client) 52 miles; Castell Paper -> Lindqvist office 30 miles; office -> home 12 miles.
Parking at client: $9.00, receipt attached (claimed separately).
""",
[("$21.00", "70 miles at $0.30."),
 ("$33.64", "58 miles at $0.58."),
 ("$40.60", "70 miles at $0.58."),
 ("$47.56", "82 miles at $0.58."),
 ("$54.52", "94 miles at $0.58."),
 ("$28.20", "94 miles at $0.30.")],
"$40.60", 3,
twin=T([("Date: Tuesday 15 September 2026.", "Date: Saturday 19 September 2026.")], "$54.52")),

# ------------------------------------------------------------------ hr02
# why: grandmother = extended family -> 2 days only; request is 4 days -> not fully
# covered -> no. Twin: mother = immediate family -> up to 5 days -> 4 days covered -> yes.
Y("hr02", "Is the whole of this request covered by paid bereavement leave?",
"""
Oakhollow Council — Bereavement leave (HR policy 14)

14.1 Immediate family (spouse or partner, child, parent, sibling): up to 5 working days of paid leave.
14.2 Extended family (grandparent, grandchild, aunt, uncle, parent-in-law, sibling-in-law): up to 2 working days of paid leave.
14.3 Leave must be taken within 30 calendar days of the death.
14.4 Additional days may be taken as annual leave or unpaid leave with manager agreement.

Leave request LR-5102
Employee: Tomasz Wren, Parks Services.
Deceased: his grandmother, died 21 September 2026.
Requested: 4 working days paid bereavement leave, 24-29 September 2026 (Thursday, Friday, Monday, Tuesday).
Manager comment: "Tomasz was very close to her; she raised him for several years."
""",
[("Immediate family", "spouse or partner, child, parent or sibling: up to 5 paid days."),
 ("Extended family", "grandparent, grandchild, aunt, uncle or in-law: up to 2 paid days.")],
0, 2,
twin=T([("Deceased: his grandmother, died 21 September 2026.", "Deceased: his mother, died 21 September 2026."),
        ("\"Tomasz was very close to her; she raised him for several years.\"", "\"Please support Tomasz at this time.\"")], 1)),

# ------------------------------------------------------------------ hr03
# why: 25 x 0.6 FTE = 15 days full-year; start 1 Jul (on/before 15th) -> Jul-Dec = 6
# months -> 15 x 6/12 = 7.5 -> already a half day -> 7.5.
# Twin: start 20 Jul (after 15th) -> Aug-Dec = 5 months -> 15 x 5/12 = 6.25 -> round up
# to the next half day -> 6.5.
C("hr03", "How many days of annual leave is the new starter entitled to for 2026?",
"""
Corrigan & Vale LLP — Annual leave (staff handbook, section 9)

9.1 Full-time entitlement: 25 days per leave year (1 January to 31 December), plus public holidays.
9.2 Part-time staff: entitlement x FTE.
9.3 Starters and leavers: pro-rate by the number of months of service in the leave year. A month counts in full if the employee starts on or before the 15th of that month; if they start after the 15th, that month is not counted.
9.4 Round the result up to the nearest half day.
9.5 Up to 5 days may be bought through the benefits scheme.

New starter record
Name: Ines Carvalho. Role: Paralegal, Commercial team.
Start date: 1 July 2026. Contract: 3 days a week (0.6 FTE), permanent.
Benefits selection: no extra leave purchased.
""",
[("6 days", "six days."), ("6.5 days", "six and a half days."), ("7 days", "seven days."),
 ("7.5 days", "seven and a half days."), ("12.5 days", "twelve and a half days."), ("15 days", "fifteen days.")],
"7.5 days", 3, ordered=True,
twin=T([("Start date: 1 July 2026.", "Start date: 20 July 2026.")], "6.5 days")),

# ------------------------------------------------------------------ hr04
# why: Mon departure 75% = 48, Tue full 64, Wed return 75% = 48 -> 160. Deduct provided
# meals: lunch Tue 18 + lunch Wed 18 = 36 -> 124. Twin: + dinner Tue 30 -> 94.
C("hr04", "What meal allowance is payable for this trip?",
"""
Petrel Biscuits — Travel allowances (UK and EU trips)

- Daily meal allowance: $64 for a full travel day.
- Day of departure and day of return: 75% of the daily allowance.
- Meals provided free (by a conference, client or hotel package) are deducted at: breakfast $12, lunch $18, dinner $30. Deductions apply on any day, including departure and return days.
- Hotel breakfast included in the room rate is not deducted when the room rate is under the hotel cap.
- Alcohol is never reimbursed.

Trip TA-2210
Traveller: Owen Castle, Quality Manager.
Monday 5 October 2026: depart 07:10, arrive Lyonne for the Food Safety Forum.
Tuesday 6 October: full conference day.
Wednesday 7 October: morning session, return flight 18:40.
Meals provided by the conference: lunch on Tuesday and lunch on Wednesday.
Hotel: room-only rate, under cap.
""",
[("$94.00", "ninety-four dollars."), ("$106.00", "one hundred and six dollars."), ("$118.00", "one hundred and eighteen dollars."),
 ("$124.00", "one hundred and twenty-four dollars."), ("$142.00", "one hundred and forty-two dollars."),
 ("$160.00", "one hundred and sixty dollars."), ("$192.00", "one hundred and ninety-two dollars.")],
"$124.00", 3,
twin=T([("lunch on Tuesday and lunch on Wednesday.", "lunch on Tuesday, dinner on Tuesday and lunch on Wednesday.")], "$94.00")),

# ------------------------------------------------------------------ hr05
# why: probation 6 months from 16 Mar ends 15 Sep (day before same date six months
# later). Resignation given 10 Sep -> during probation -> 1 week notice is enough -> yes.
# Twin: given 18 Sep -> after probation -> 4 weeks -> no.
Y("hr05", "Is one week's notice enough for this resignation?",
"""
Saltmarsh Housing — Contract terms for support staff (extract)

Probation: six months from the start date. Probation ends on the day before the same calendar date six months later.
Notice by the employee: during probation, 1 week; after probation, 4 weeks.
Notice is measured from the day it is received in writing by the line manager.
Accrued holiday is paid out on leaving.

HR case note
Employee: Callum Reyes, Tenancy Support Officer. Start date: 16 March 2026.
Resignation letter received by line manager: 10 September 2026 (email with signed letter attached).
Last working day requested: 17 September 2026.
Manager asks whether the requested last day works under the contract.
""",
[("Probation", "the first six months of employment, ending the day before the six-month anniversary date."),
 ("Notice during probation", "one week."),
 ("Notice after probation", "four weeks.")],
1, 2,
twin=T([("received by line manager: 10 September 2026", "received by line manager: 18 September 2026"),
        ("Last working day requested: 17 September 2026.", "Last working day requested: 25 September 2026.")], 0)),

# ------------------------------------------------------------------ hr06
# why: timeliness first: expense 3 Jul, submitted 22 Jul = 19 days <= 60 -> ok.
# Receipt present, attendee list present; wine $48 non-reimbursable -> approve partially.
# Twin: submitted 8 Sep: 3 Jul -> 3 Aug 31, -> 3 Sep 31, +5 = 67 days > 60 -> reject late.
C("hr06", "What should the expense approver do with this claim?",
"""
Corrigan & Vale LLP — Expense review steps (for approvers)

Step 1. Timeliness: a claim submitted more than 60 days after the expense date is rejected without further review.
Step 2. Receipts: any item above $25 needs an itemised receipt. If missing, return the claim for receipts.
Step 3. Client entertainment: an attendee list (names and organisations) is required. If missing, return the claim for the list.
Step 4. Remove non-reimbursable items (alcohol, personal items, fines) and approve the rest; if nothing needs removing, approve in full.

Claim EX-88104, submitted 22 July 2026
Claimant: Benedikt Moor, Senior Associate.
Expense date: 3 July 2026. Client dinner at Harbour Table, $186.00 total.
Itemised receipt: attached. Lines include food $132.00, soft drinks $6.00, bottle of wine $48.00.
Attendees: Benedikt Moor (C&V), Lucia Ferro and Aled Price (Tennant Shipping).
""",
[("approve in full", "every line is reimbursable and all documents are present."),
 ("approve partially", "remove the non-reimbursable lines and pay the rest."),
 ("return for receipts", "an itemised receipt is missing."),
 ("return for attendee list", "the client-entertainment attendee list is missing."),
 ("reject — late submission", "the claim was submitted more than 60 days after the expense.")],
"approve partially", 2,
twin=T([("Claim EX-88104, submitted 22 July 2026", "Claim EX-88104, submitted 8 September 2026")], "reject — late submission")),

# ------------------------------------------------------------------ hr07
# why: paid holiday hours do not count toward 40. Hours worked Mon-Thu 4 x 10 = 40;
# Friday paid holiday -> 40 worked -> not over 40 -> no overtime.
# Twin: Friday worked 6 h -> 46 worked -> 6 h overtime -> yes.
Y("hr07", "Is overtime pay owed to this employee for the week?",
"""
Petrel Biscuits — Hourly staff pay rules (non-exempt)

- Overtime is paid at 1.5x the hourly rate for hours actually worked above 40 in a workweek (Sunday to Saturday).
- Paid time off, sick pay and paid public holidays are paid at the normal rate but do not count as hours worked for the 40-hour test.
- Daily hours above 10 do not trigger overtime on their own.
- Night-shift premium is a separate 10% supplement.

Timesheet — week of Sunday 20 December to Saturday 26 December 2026
Employee: Joss Kinley, line operator, hourly.
Mon 21: 10 h worked. Tue 22: 10 h worked. Wed 23: 10 h worked. Thu 24: 10 h worked.
Fri 25: public holiday, 8 h paid holiday.
Sat 26 and Sun 20: not scheduled.
Total paid hours: 48.
""",
[("Hours worked", "hours actually worked; paid leave and paid holidays are excluded."),
 ("Overtime", "1.5x pay for hours worked above 40 in a Sunday-Saturday workweek.")],
0, 2,
twin=T([("Fri 25: public holiday, 8 h paid holiday.", "Fri 25: 6 h worked (holiday cover shift)."),
        ("Total paid hours: 48.", "Total paid hours: 46.")], 1)),

# ------------------------------------------------------------------ hr08
# why: enhanced needs 12 months' service at leave start: 1 Nov 2025 -> 16 Oct 2026 is
# under 12 months -> no. Statutory needs 26 weeks by leave start: ~50 weeks -> yes ->
# statutory only. Twin: leave starts 9 Nov 2026 -> over 12 months -> enhanced.
C("hr08", "Which parental pay applies to this employee?",
"""
Lindqvist Analytics — Parental leave and pay (policy PL-3)

Leave: every employee may take up to 52 weeks of parental leave from day one of employment.
Pay (the most generous tier the employee qualifies for applies):
 (a) Enhanced company pay — 16 weeks at full salary — requires at least 12 months of continuous service on the day the leave starts.
 (b) Statutory parental pay — requires at least 26 weeks of continuous service on the day the leave starts.
 (c) If neither (a) nor (b) is met, the leave is unpaid.
Keeping-in-touch days: up to 10, paid at the normal daily rate.

HR ticket HR-3381
Employee: Priya Nandakumar, Data Engineer. Continuous service since: 1 November 2025.
Planned leave start: 16 October 2026. Expected due date: 30 October 2026.
Question from employee: "Will I get the company's full-pay leave?"
""",
[("enhanced company pay", "16 weeks at full salary under tier (a)."),
 ("statutory pay only", "statutory parental pay under tier (b)."),
 ("statutory pay, then enhanced pay", "statutory pay at first, switching to enhanced company pay once 12 months' service is reached during the leave."),
 ("unpaid leave", "leave is available but without pay under (c)."),
 ("no leave entitlement", "the employee may not take parental leave.")],
"statutory pay only", 2,
twin=T([("Planned leave start: 16 October 2026. Expected due date: 30 October 2026.",
         "Planned leave start: 9 November 2026. Expected due date: 20 November 2026.")], "enhanced company pay")),

# ------------------------------------------------------------------ hr09
# why: annual cap 20 working days; used 12 + requested 9 = 21 > 20 -> cannot approve.
# 9 consecutive <= 10; notice 14 business days >= 10; country not restricted.
# Twin: used 11 -> 20 -> within cap -> yes.
Y("hr09", "Can this work-from-abroad request be approved under the policy?",
"""
Corrigan & Vale LLP — Temporary work from abroad (policy WA-2)

1. Staff may work from another country for up to 20 working days in total per calendar year.
2. No single trip may exceed 10 consecutive working days.
3. Requests must be submitted at least 10 business days before the first day abroad.
4. Countries on the firm's restricted list (Annex A) are never approved.
5. Client-site travel is business travel and is not counted under this policy.

Request WA-0917
Employee: Maeve Oduya, Associate.
Destination: Portavela (not on Annex A).
Dates: 12-22 October 2026 = 9 working days.
Submitted: 22 September 2026 (13 business days before departure).
Work-from-abroad days already taken in 2026: 12 (April trip, 7 days; July trip, 5 days).
""",
[("Annual cap", "at most 20 working days abroad per calendar year, counting this request."),
 ("Trip limit", "at most 10 consecutive working days per trip.")],
0, 2,
twin=T([("already taken in 2026: 12 (April trip, 7 days; July trip, 5 days)", "already taken in 2026: 11 (April trip, 6 days; July trip, 5 days)")], 1)),

# ------------------------------------------------------------------ hr10
# why: 9 unused at year end. 3 were refused in writing in the HR system -> carry over
# in addition to the cap. The other 6 are capped at 5 -> 5 + 3 = 8 carried (1 lost).
# Twin: refusal was verbal only, not recorded -> does not count -> cap 5 on all 9 -> 5.
C("hr10", "How many leave days carry over into 2027?",
"""
Oakhollow Council — Leave carry-over (HR policy 9.6)

(a) Up to 5 unused days of annual leave may be carried into the next leave year and must be used by 31 March.
(b) Days that the employee requested and the Council refused for service reasons carry over in full, in addition to the 5-day cap. A refusal counts only if it is recorded in the HR system.
(c) Any other unused days are lost on 31 December.
(d) Purchased leave cannot be carried over (none purchased here).

Leave record — Joanna Brisk, Revenue Officer, as at 31 December 2026
Entitlement 2026: 28 days. Taken: 19 days. Unused: 9 days.
Refused requests: 3 days (14-16 December) requested on 2 November and refused by her manager in the HR system on 4 November because of the council-tax billing peak.
""",
[("3 days", "three days."), ("5 days", "five days."), ("6 days", "six days."),
 ("8 days", "eight days."), ("9 days", "nine days.")],
"8 days", 3, ordered=True,
twin=T([("refused by her manager in the HR system on 4 November", "refused verbally by her manager on 4 November, with nothing recorded in the HR system,")], "5 days")),

# ------------------------------------------------------------------ hr11
# why: allegation that a manager asked staff to falsify (backdate) timesheets -> falsified
# records -> Ethics & Compliance (override, even when a manager is involved).
# Twin: rude comments in meetings -> conduct/relationship issue -> Employee Relations.
C("hr11", "Which team should handle this employee report?",
"""
Saltmarsh Housing — People team intake guide

- Pay errors, missing overtime, tax codes: Payroll.
- Pensions, health cover, childcare vouchers: Benefits.
- Complaints about a manager's or colleague's behaviour, bullying, grievances: Employee Relations.
- Accidents, unsafe equipment, near misses: Health & Safety.
- Career, restructures, role changes: HR Business Partner.
- Allegations of fraud, bribery or falsified records: Ethics & Compliance. This applies even when the allegation concerns a manager and would otherwise be a grievance.
- Laptop and system access: IT Service Desk.

Intake form IF-2071 (submitted 28 September 2026)
Reporter: repairs scheduler, Northfield depot (name withheld at their request).
Summary: "Our team manager told three of us to change the dates on our July timesheets so the jobs look like they were done before the grant deadline. The housing grant only pays for work finished by 30 June. I don't want to get in trouble. He also keeps snapping at people in team meetings."
""",
[("Payroll", "pay and tax problems."),
 ("Benefits", "pensions and benefit schemes."),
 ("Employee Relations", "behaviour complaints, bullying and grievances."),
 ("Health & Safety", "accidents and unsafe conditions."),
 ("HR Business Partner", "careers and organisational change."),
 ("Ethics & Compliance", "fraud, bribery and falsified records."),
 ("IT Service Desk", "equipment and system access."),
 ("none of these", "no team fits the report.")],
"Ethics & Compliance", 2,
twin=T([("\"Our team manager told three of us to change the dates on our July timesheets so the jobs look like they were done before the grant deadline. The housing grant only pays for work finished by 30 June. I don't want to get in trouble. He also keeps snapping at people in team meetings.\"",
         "\"Our team manager keeps snapping at people in team meetings and made fun of my accent in front of everyone on Monday. Two colleagues saw it. I don't want to get in trouble for raising it.\"")],
       "Employee Relations")),

# ------------------------------------------------------------------ hr12
# why: absence runs from first sick day to the day before return, all calendar days:
# Thu 17 -> Mon 21 = 5 days > 3 -> certificate needed -> yes.
# Twin: first sick day Sat 19 -> Sat, Sun, Mon = 3 days, not more than 3 -> no.
Y("hr12", "Does the employee have to provide a medical certificate for this absence?",
"""
Petrel Biscuits — Sickness absence procedure

1. Report sickness to your supervisor before your shift starts.
2. The absence period runs from the first day of sickness to the day before you return to work, counting every calendar day, including weekends and days you were not rostered.
3. If the absence period is more than 3 calendar days, a medical certificate is required.
4. For absence periods of 3 calendar days or fewer, complete a self-certification form.
5. Return-to-work interviews are held after every absence.

Absence log — packing hall
Employee: Rosa Linden, rostered Monday to Friday.
First day of sickness: Thursday 17 September 2026 (reported 06:15).
Returned to work: Tuesday 22 September 2026.
Self-certification form: submitted on return.
""",
[("Absence period", "every calendar day from the first day of sickness to the day before return to work."),
 ("Certificate rule", "a medical certificate is required when the absence period is more than 3 calendar days.")],
1, 2,
twin=T([("First day of sickness: Thursday 17 September 2026 (reported 06:15).",
         "First day of sickness: Saturday 19 September 2026 (reported Monday 06:15).")], 0)),

# ------------------------------------------------------------------ hr13
# why: resignation (not redundancy) -> clawback applies. Whole months since payment
# 1 Jun 2025 to leaving 15 Sep 2026 = 15 (to 1 Sep 2026). Remaining 24 - 15 = 9 ->
# 8,000 x 9/24 = $3,000. Twin: leaving 15 Jul 2027 -> 25 months -> none remaining -> $0.
C("hr13", "How much relocation allowance must the employee repay?",
"""
Lindqvist Analytics — Relocation support (policy RS-1)

1. Allowance: $3,000 for a move of 50-150 km; $8,000 for a move of more than 150 km.
2. Clawback: an employee who resigns within 24 months of the payment date repays the allowance pro rata: allowance x (24 - whole months completed since the payment date) / 24.
3. No clawback applies when employment ends through redundancy or ill-health retirement.
4. Removal costs paid directly to a removals firm are not part of the allowance.

Leaver file
Employee: Dmitri Salo, Senior Analyst. Moved 410 km from Varnholm to join the Brisbourne office.
Relocation allowance: $8,000, paid 1 June 2025. Removals firm paid directly: $2,350.
Reason for leaving: resignation. Leaving date: 15 September 2026.
""",
[("$0.00", "nothing to repay."), ("$2,666.67", "two thousand six hundred and sixty-six dollars sixty-seven."),
 ("$3,000.00", "three thousand dollars."), ("$3,333.33", "three thousand three hundred and thirty-three dollars thirty-three."),
 ("$5,000.00", "five thousand dollars."), ("$8,000.00", "the whole allowance.")],
"$3,000.00", 3,
twin=T([("Leaving date: 15 September 2026.", "Leaving date: 15 July 2027.")], "$0.00")),

# ------------------------------------------------------------------ hr14
# why: B+ >= B -> 100% of fee = $2,400, but annual cap $5,250: already $3,100 ->
# room $2,150 < 2,400 -> not full -> no.
# Twin: already $2,600 -> room $2,650 >= 2,400 -> full -> yes.
Y("hr14", "Should the full course fee be reimbursed?",
"""
Oakhollow Council — Tuition assistance scheme

- Reimbursement after the course ends: 100% of the tuition fee for a final grade of B or higher; 50% for a C; nothing below C.
- Maximum reimbursement per employee per calendar year: $5,250 (all courses combined).
- Books, travel and exam resits are not covered.
- Employees who leave within 12 months of a reimbursement repay it in full.

Claim TA-2026-41
Employee: Kofi Mensah, Planning Officer.
Course: Urban Data Analysis (Brenmoor College), tuition fee $2,400, completed 4 September 2026, final grade B+.
Books claimed: $85.
Tuition reimbursements already paid to Kofi in 2026: $3,100 (spring module).
""",
[("Grade rule", "100% for B or higher, 50% for C, nothing below C."),
 ("Annual cap", "total reimbursement per employee per calendar year may not exceed $5,250.")],
0, 2,
twin=T([("already paid to Kofi in 2026: $3,100", "already paid to Kofi in 2026: $2,600")], 1)),

# ------------------------------------------------------------------ hr15
# why: cut-off is the 15th, or the previous business day if the 15th is a weekend.
# 15 Aug 2026 is a Saturday -> cut-off Fri 14 Aug. Submitted Sat 15 Aug -> after
# cut-off -> September payroll. Off-cycle needs company error AND > $500: $320, late
# submission by employee -> no. Twin: submitted Fri 14 Aug -> August payroll.
C("hr15", "In which pay run will this overtime be paid?",
"""
Saltmarsh Housing — Payroll calendar rules

- Salaries are paid monthly on the last business day of the month.
- Cut-off for changes and claims is the 15th of the month; if the 15th falls on a Saturday or Sunday, cut-off is the preceding Friday. Claims approved by cut-off are paid in that month's run; later claims are paid in the next month's run.
- Off-cycle payments are made only when an underpayment is more than $500 and was caused by a Saltmarsh error.
- Pension contribution changes take effect from the next full month.

Overtime claim OT-7713
Employee: Grace Tamsin, Repairs Supervisor. Overtime: 8 hours in July, value $320.
Submitted and approved in the payroll portal: Saturday 15 August 2026, 10:04.
Employee note: "Sorry, forgot to submit this last month."
""",
[("August pay run", "paid on the last business day of August."),
 ("September pay run", "paid on the last business day of September."),
 ("October pay run", "paid on the last business day of October."),
 ("November pay run", "paid on the last business day of November."),
 ("off-cycle payment", "paid immediately outside the monthly run.")],
"September pay run", 2, ordered=True,
twin=T([("Saturday 15 August 2026, 10:04", "Friday 14 August 2026, 10:04")], "August pay run")),

# ------------------------------------------------------------------ hr16
# why: top-up = normal daily pay - court allowance = 240 - 50 = 190 per day, max 10
# working days a year. Used 0 before -> 3 days x 190 = $570.
# Twin: 9 days used earlier -> 1 day left -> $190.
C("hr16", "What jury-service top-up should payroll pay for this period?",
"""
Corrigan & Vale LLP — Civic duties (handbook section 11)

11.1 Jury service: the firm pays the difference between the employee's normal daily pay and the daily allowance paid by the court, for up to 10 working days of jury service per calendar year.
11.2 Beyond 10 days, jury service is unpaid by the firm (the court allowance is still received).
11.3 Employees must give the jury summons to HR within 5 days of receiving it.
11.4 Volunteer reservist training: see 11.6.

Payroll note — October 2026
Employee: Hamish Ogden, Trainee Solicitor. Normal daily pay: $240.
Jury service: 6, 7 and 8 October 2026 (3 working days). Court allowance: $50 per day.
Jury service days already paid under 11.1 in 2026: 0.
Summons given to HR on 14 September 2026 (received 11 September).
""",
[("$0.00", "nothing is paid by the firm."), ("$150.00", "one hundred and fifty dollars."),
 ("$190.00", "one hundred and ninety dollars."), ("$570.00", "five hundred and seventy dollars."),
 ("$620.00", "six hundred and twenty dollars."), ("$720.00", "seven hundred and twenty dollars.")],
"$570.00", 2,
twin=T([("Jury service days already paid under 11.1 in 2026: 0.", "Jury service days already paid under 11.1 in 2026: 9.")], "$190.00")),

# ------------------------------------------------------------------ hr17
# why: rehire check reuse only if rehire start is within 12 months of the leaving date:
# left 30 Sep 2025; 12 months -> 30 Sep 2026; start 5 Oct 2026 is later -> new check
# needed -> yes. Twin: start 28 Sep 2026 -> within 12 months -> no new check -> no.
Y("hr17", "Is a new background check required before this rehire starts?",
"""
Petrel Biscuits — Pre-employment screening standard

S1. Every new hire needs a background check completed before the start date.
S2. Rehires: a former employee's previous check may be reused if the rehire start date is no more than 12 months after their leaving date and they left in good standing.
S3. Roles in the finance team also need a credit check (not relevant to operations roles).
S4. Right-to-work documents are always checked again on day one.

Rehire request RH-208
Candidate: Neil Varga, former line operator. Left in good standing (resigned) on 30 September 2025.
New role: shift team leader, operations. Planned start date: 5 October 2026.
Previous background check: completed 2 February 2022, clear.
""",
[("Reuse rule", "a previous check may be reused for a rehire starting no more than 12 months after leaving, in good standing."),
 ("New check", "a fresh background check completed before the start date.")],
1, 2,
twin=T([("Planned start date: 5 October 2026.", "Planned start date: 28 September 2026.")], 0)),
]
