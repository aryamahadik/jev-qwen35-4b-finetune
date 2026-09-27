"""proc_longpolicy / employment policies and staff agreements."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ em01
# why: EWC week beginning 8 Mar 2026 -> Qualifying Date = 15 weeks earlier = 23 Nov 2025.
# Service 11 Aug -> 23 Nov 2025 = 104 days (~14.9 weeks). Birth 10 Mar 2026 -> v3 applies
# (13 weeks, 20 weeks full pay) -> enhanced 20 weeks. Twin: EWC 7 Dec 2025, born 9 Dec 2025
# -> v2 applies (26 weeks); QD 24 Aug 2025, 2 weeks' service -> statutory only.
C("em01", "Which parental pay decision should HR record for this employee?",
"""
HOLLINS & FAIRE LTD — FAMILY LEAVE POLICY (version 2, March 2023)

1. DEFINITIONS
1.1 "Expected Week" means the week, beginning on a Sunday, in which the baby is due, as shown on the medical certificate.
1.2 "Qualifying Date" means the last day of the 15th week before the Expected Week, counted back from the Sunday that begins the Expected Week.
1.3 "Qualifying Service" means continuous employment with the Company of at least 26 weeks ending on the Qualifying Date.
1.4 "Statutory Pay" means the parental pay required by law, which the Company pays through payroll.

2. ELIGIBILITY FOR LEAVE
2.1 Every employee may take up to 52 weeks of parental leave, regardless of length of service.
2.2 Leave may start no earlier than 11 weeks before the Expected Week.

3. PAY DURING LEAVE
3.1 An employee with Qualifying Service receives Enhanced Pay of 16 weeks at full basic salary, followed by Statutory Pay for the remainder of any paid period.
3.2 An employee without Qualifying Service receives Statutory Pay only.
3.3 Enhanced Pay is repayable if the employee does not return to work for at least three months after leave, unless the reason is redundancy or ill health.

4. KEEPING IN TOUCH
4.1 Up to ten keeping-in-touch days may be worked during leave and are paid at the normal daily rate.

5. PROBATION
5.1 Parental leave does not extend a probation period unless the employee agrees.

6. SHARED PARENTAL LEAVE
6.1 Where both parents work for the Company, leave may be shared under the statutory scheme; Enhanced Pay is then split in proportion to the weeks each parent takes.
6.2 Notice to share leave must be given at least eight weeks before the first period of shared leave.

7. RETURNING TO WORK
7.1 An employee returning within 26 weeks may go back to the same job. After 26 weeks, the Company may offer a suitable alternative role on no less favourable terms.
7.2 Requests for reduced hours on return are handled under the Flexible Working Policy.

VERSION 3 AMENDMENT — approved by the Board, 20 November 2025
This amendment applies where the child is born, or placed for adoption, on or after 1 January 2026. For earlier births version 2 continues to apply.
V1. In clause 1.3, "26 weeks" is replaced by "13 weeks".
V2. In clause 3.1, "16 weeks" is replaced by "20 weeks".

EMPLOYEE CASE — Chioma Adeyemi, Logistics Planner
• Start date: 11 August 2025. Still in probation (six months).
• Medical certificate: Expected Week beginning 8 March 2026.
• Baby born 10 March 2026. Leave started on the day of the birth.
• HR adviser's working note: "Hasn't been with us 26 weeks, so presumably just statutory."
• Payroll asks for a single recorded decision before the March payroll run.
""",
[("enhanced_20_weeks", "The birth falls under version 3, and service from 11 August to the 23 November Qualifying Date exceeds 13 weeks, so 20 weeks' full pay applies."),
 ("enhanced_16_weeks", "The employee has more than 13 weeks' service by the Qualifying Date, so she qualifies, and clause 3.1 then pays Enhanced Pay of 16 weeks at full basic salary."),
 ("statutory_pay_only", "The employee lacks the Qualifying Service required by the version that governs this birth, so only Statutory Pay is due."),
 ("defer_until_probation_ends", "She is still within her six-month probation, and Enhanced Pay cannot be paid to an employee in probation until it has been passed, so the decision must wait.")],
"enhanced_20_weeks", 3,
twin=T([("Expected Week beginning 8 March 2026.", "Expected Week beginning 7 December 2025."),
        ("Baby born 10 March 2026.", "Baby born 9 December 2025.")], "statutory_pay_only")),

# ------------------------------------------------------------------ em02
# why: amendment from 1 Jul 2025 raises annual cap to 30 days and requires tax sign-off for
# List B. Used 14 + requested 12 = 26 <= 30; Veloria on List B -> approve subject to tax
# sign-off. Twin: used 21 -> 33 > 30 -> refuse on annual cap.
C("em02", "What decision should the People team give on the Remote Work Abroad request?",
"""
ASHDOWN CARTOGRAPHY — WORKING FROM ANYWHERE POLICY
Owner: People team. Applies to employees on UK employment contracts.

1. DEFINITIONS
1.1 "Remote Work Abroad" means working, in any capacity, from a country other than the Employing Country.
1.2 "Employing Country" means the country named in the employee's contract.
1.3 "Working Day" means a day on which the employee is scheduled to work; weekends and public holidays in the Employing Country are not Working Days.
1.4 "Country Lists": List A and List B in the Appendix. Countries on neither list are not approved destinations.

2. ALLOWANCE
2.1 An employee may spend up to 20 Working Days per calendar year on Remote Work Abroad.
2.2 Days are counted across all trips in the calendar year.
2.3 Requests must be submitted at least 15 Working Days before travel.

3. CONDITIONS
3.1 The employee must be reachable during core hours, 10:00 to 15:00 Employing Country time.
3.2 Company laptops must use the VPN at all times while abroad.
3.3 The employee is responsible for their own travel insurance.

4. HOLIDAYS
4.1 Annual leave taken while abroad does not count towards the Remote Work Abroad allowance.

APPENDIX — COUNTRY LISTS (updated July 2025)
List A: Istrana, Merovia, Solbrand, the Calder Isles.
List B: Veloria, Tessaly, Oruna.

5. EXPENSES AND EQUIPMENT
5.1 Travel costs for Remote Work Abroad are not reimbursed.
5.2 Employees must not take Company monitors, docking stations or printers abroad.
5.3 Lost or stolen equipment must be reported to IT Security within 24 hours.

6. REFUSALS AND APPEALS
6.1 The People team decides every request against this policy; a line manager's support is required but is not itself approval.
6.2 An employee may ask the Head of People to review a refusal within five Working Days.

POLICY UPDATE — effective 1 July 2025
U1. In clause 2.1, "20 Working Days" is replaced by "30 Working Days".
U2. New clause 2.4: "Remote Work Abroad in a List B country may be approved only after the Tax team has signed off the trip."
U3. All other clauses are unchanged.

REQUEST — submitted 11 August 2025
Employee: Rafael Lindqvist, Senior GIS Analyst.
Destination: Veloria. Dates: 8 to 23 September 2025, 12 Working Days. Annual leave: none during the trip.
Earlier Remote Work Abroad this year: 14 Working Days in Istrana in March 2025.
Tax team sign-off: not yet requested.
Line manager's comment: "Happy for Rafael to go. He did great work from Istrana."
""",
[("approve_subject_to_tax_signoff", "The 26-day total fits the amended 30-day allowance, but Veloria is on List B, so the Tax team must sign off before approval."),
 ("approve_outright", "The trip keeps the employee inside the annual Remote Work Abroad allowance and the line manager supports it, so the People team can approve it as submitted."),
 ("refuse_annual_limit", "Adding this trip to the earlier days takes the employee past the annual Remote Work Abroad allowance."),
 ("refuse_late_request", "The request was submitted on 11 August for travel starting 8 September, fewer than the 15 Working Days that clause 2.3 requires, so it must be refused.")],
"approve_subject_to_tax_signoff", 2,
twin=T([("14 Working Days in Istrana in March 2025", "21 Working Days in Istrana in March 2025")], "refuse_annual_limit")),

# ------------------------------------------------------------------ em03
# why: pay week Mon 6 - Sun 12 Oct 2025 starts after 1 Oct -> threshold 37.5 h. Weekday 40 h:
# 37.5 x 16 = 600; 2.5 x 24 = 60; Sunday 4 x 32 = 128 (Sunday not in threshold) = 788.
# Old 38 h: 608 + 48 + 128 = 784. Twin: week 22-28 Sep 2025 -> 784.
C("em03", "What gross pay is due for the pay week in question?",
"""
NORTHWAY DISTRIBUTION — COLLECTIVE AGREEMENT ON HOURS AND PAY (2024–2026)
Between Northway Distribution Ltd and the Warehouse Staff Council.

1. DEFINITIONS
1.1 "Pay Week" means Monday 00:00 to Sunday 24:00.
1.2 "Basic Rate" means the employee's contractual hourly rate.
1.3 "Weekday Hours" means hours worked Monday to Saturday.
1.4 "Sunday Hours" means hours worked on a Sunday.

2. NORMAL HOURS
2.1 Normal hours are up to 38 Weekday Hours in a Pay Week.
2.2 Breaks of 30 minutes or more are unpaid and are not counted as hours worked.

3. OVERTIME AND PREMIUMS
3.1 Weekday Hours above the normal hours in 2.1 are paid at 1.5 times the Basic Rate.
3.2 Sunday Hours are paid at 2 times the Basic Rate and do not count towards the normal hours in 2.1.
3.3 Public holiday hours are paid at 2 times the Basic Rate.
3.4 Overtime must be authorised in advance by a shift manager.

4. SHIFT ALLOWANCE
4.1 Night shifts starting after 22:00 attract a flat £12 allowance per shift. Day shifts attract no allowance.

5. SICKNESS
5.1 Company sick pay is paid at the Basic Rate for up to 10 days a year after six months' service.

6. HOLIDAY PAY
6.1 Holiday pay includes average regular overtime over the previous 52 working weeks.

7. PAY PERIODS AND DISPUTES
7.1 Pay is calculated per Pay Week and paid weekly in arrears on Friday.
7.2 Any query about a payslip is raised first with the shift manager and then with Payroll.
7.3 Where a memorandum of agreement changes a rate, the rate applies to Pay Weeks as stated in the memorandum and not to earlier weeks.

PUBLICATION AND EARLIER VERSIONS
A copy of this document is published on the organisation's website. Earlier versions are archived and remain available for reference, together with every amendment and the date from which it applies.

MEMORANDUM OF AGREEMENT No. 4 — signed 15 September 2025
Applies to Pay Weeks beginning on or after 1 October 2025.
M1. In clause 2.1, "38" is replaced by "37.5".
M2. In clause 3.3, "2 times" is replaced by "2.5 times".
M3. Clauses 3.1 and 3.2 are unchanged.

TIMESHEET — Kasia Wren, Picker, Basic Rate £16.00
Pay Week: 6–12 October 2025
Monday to Friday: day shifts of 8 hours each, all authorised; unpaid 30-minute breaks already deducted.
Saturday: rest day.
Sunday: 4 hours, authorised.
No public holidays fell in the week.

PAYROLL QUERY
"The system has calculated a figure but the supervisor thinks it's wrong. Please confirm the correct gross pay for the week."
""",
[("pay_788", "The 37.5-hour threshold applies, so 37.5 × £16 + 2.5 × £24 + 4 Sunday hours × £32 = £788."),
 ("pay_784", "Normal hours are 38, so 38 × £16 + 2 × £24 + 4 × £32 = £784."),
 ("pay_756", "Sunday work is just more overtime, so 37.5 × £16 + 2.5 × £24 + 4 × £24 = £756."),
 ("pay_768", "Overtime starts only after 40 weekday hours, so 40 × £16 plus 4 Sunday hours at £32 gives £768.")],
"pay_788", 2,
twin=T([("Pay Week: 6–12 October 2025", "Pay Week: 22–28 September 2025")], "pay_784")),

# ------------------------------------------------------------------ em04
# why: warning issued 15 May 2025 is after 1 Apr 2025, so it stays live 9 months (to
# 15 Feb 2026); new similar misconduct on 20 Dec 2025 -> next stage = final written warning.
# Twin: warning issued 15 Mar 2025 -> 6 months -> expired 15 Sep 2025 -> fresh first warning.
C("em04", "At which stage of the procedure should the hearing manager place the new misconduct?",
"""
QUAYSIDE CARE GROUP — DISCIPLINARY PROCEDURE
Applies to all non-medical employees. Version 5.

1. DEFINITIONS
1.1 "Live" means a warning that has not yet expired under section 6.
1.2 "Misconduct" means conduct that breaches the Code of Conduct but does not amount to Gross Misconduct.
1.3 "Gross Misconduct" means conduct so serious that it may justify dismissal for a first offence, as listed in Appendix C.
1.4 "Similar" means misconduct falling within the same Appendix B category.

2. INFORMAL ACTION
2.1 Minor lapses are handled first by an informal conversation, recorded in the supervision notes. An informal conversation is not a warning.

5. FORMAL STAGES
5.1 Stage 1: first written warning.
5.2 Stage 2: final written warning, where a first written warning for Similar Misconduct is Live.
5.3 Stage 3: dismissal with notice, where a final written warning is Live.
5.4 Gross Misconduct may lead directly to dismissal without notice.

6. DURATION OF WARNINGS
6.1 A first written warning is Live for six months from the date of issue.
6.2 A final written warning is Live for twelve months from the date of issue.
6.3 Expired warnings stay on file but may not be used to move to a higher stage.

7. RIGHT TO BE ACCOMPANIED
7.1 Employees may bring a colleague or trade union representative to any formal hearing.

8. APPEALS
8.1 An employee may appeal any formal sanction within ten working days to a manager not previously involved.
8.2 The appeal manager may confirm, reduce or withdraw the sanction but may not increase it.

9. SUSPENSION
9.1 Suspension on full pay is a neutral act and is not a disciplinary sanction.

AMENDMENT — agreed with the recognised union, effective 1 April 2025
A1. In clause 6.1, "six months" is replaced by "nine months" for first written warnings issued on or after 1 April 2025.
A2. Warnings issued before 1 April 2025 keep their original duration.

EMPLOYEE FILE — Declan Morrow, Care Assistant, Harbour View Home
• 2023: two informal conversations about late arrival, recorded in supervision notes.
• First written warning for unauthorised absence from a shift (Appendix B, category 2: attendance), issued 15 May 2025.
• 20 December 2025: left a shift two hours early without authorisation (Appendix B, category 2: attendance). Investigation complete; the facts are admitted.
• No other warnings.

HEARING MANAGER'S NOTE
"HR's template says his warning is 'probably spent by now'. Before the hearing I need to know which stage the policy puts us at."
""",
[("final_written_warning", "The May 2025 warning runs for nine months under the amendment, so it is still Live and Similar misconduct moves the case to Stage 2."),
 ("first_written_warning", "The earlier warning is no longer Live, so the procedure restarts at Stage 1."),
 ("dismissal_with_notice", "The file already holds a written warning and two informal conversations, so this new misconduct is the third step and moves the case to Stage 3, dismissal with notice."),
 ("informal_conversation", "Leaving a shift early is a minor lapse of the kind section 2 deals with, so the manager should hold an informal conversation rather than open a formal stage.")],
"final_written_warning", 2,
twin=T([("issued 15 May 2025", "issued 15 March 2025")], "first_written_warning")),

# ------------------------------------------------------------------ em05
# why: probation 3 Mar - 2 Sep 2025 (Tue). Amendment (from 1 Jun 2025): extension notice at
# least five Working Days before the end. Notice Fri 29 Aug: working days before 2 Sep are
# 29 Aug and 1 Sep only -> ineffective -> 4.3 confirms employment.
# Twin: notice Fri 22 Aug -> 22,25,26,27,28,29 Aug, 1 Sep = 7 working days -> valid.
C("em05", "What is the employee's status after the manager's extension email?",
"""
PELLINGHAM COUNCIL SERVICES — PROBATION POLICY
Applies to all new starters on permanent contracts.

1. DEFINITIONS
1.1 "Probation Period" means the first six months of employment. For a start on the 3rd of a month, it ends on the 2nd of the sixth month after.
1.2 "Working Day" means Monday to Friday, excluding public holidays. There were no public holidays between 20 August and 5 September 2025.
1.3 "Written" includes email to the employee's work address.

3. DURING PROBATION
3.1 Managers hold review meetings at months two and four.
3.2 During the Probation Period either party may end employment by giving one week's notice.

4. END OF PROBATION
4.1 Before the Probation Period ends the manager confirms, extends or ends employment.
4.2 The manager may extend the Probation Period once, by up to three months, by Written notice to the employee given before the Probation Period ends.
4.3 If no valid decision is communicated before the Probation Period ends, employment is confirmed automatically.
4.4 After confirmation, the contractual notice period of one month applies.

5. APPEALS
5.1 An employee may appeal an extension or dismissal to a Head of Service within ten Working Days.

6. TRAINING DURING PROBATION
6.1 New starters complete mandatory safeguarding and data-protection modules within their first eight weeks.
6.2 Failure to complete mandatory modules may be taken into account at the end-of-probation decision.

7. RECORDS
7.1 Review notes are held on the HR system and the employee may request a copy.
7.2 A decision to extend must state the reasons and the targets for the extended period.

ACCESSIBILITY
This document is available in large print, audio and easy-read formats on request. Anyone who needs help to understand it, or to take part in a process it describes, may ask for reasonable adjustments.

POLICY UPDATE — effective 1 June 2025
P1. Clause 4.2 is amended so that the Written extension notice must be given at least five Working Days before the Probation Period ends.
P2. Clause 4.3 is unchanged.

CASE — Ellis Ferreira, Housing Officer
• Start date: Monday 3 March 2025.
• Month-two and month-four reviews held; both record concerns about case-note accuracy.
• Manager's extension email, extending probation by three months, sent on Friday 29 August 2025 and read the same day.
• Today is 10 September 2025. The employee has continued working normally.
• Manager's question to HR: "I've got concerns on file — can I still let Ellis go on a week's notice?"
""",
[("employment_confirmed", "The extension email came fewer than five Working Days before probation ended, so it was ineffective and clause 4.3 confirmed employment."),
 ("extension_valid", "The Written extension was given at least five Working Days before the Probation Period ended, so probation runs on for three months."),
 ("dismiss_on_probation_notice", "Probation ended without any written confirmation of employment, so the employee can still be released on one week's notice under 3.2.")],
"employment_confirmed", 2,
twin=T([("sent on Friday 29 August 2025", "sent on Friday 22 August 2025")], "extension_valid")),

# ------------------------------------------------------------------ em06
# why: leave years from 2025 carry up to 8 days (amendment). Three days' sickness in Feb did
# not stop her taking leave, so the sickness exception does not apply -> carry 8.
# Twin: sick 1 Sep - 31 Dec and unable to take leave -> exception: all untaken (11 <= 20).
C("em06", "How many untaken days may the employee carry into 2026?",
"""
BRAMBLEGATE SOFTWARE — ANNUAL LEAVE POLICY

1. DEFINITIONS
1.1 "Leave Year" means 1 January to 31 December.
1.2 "Entitlement" means 25 days of annual leave per Leave Year plus public holidays, pro rata for part-time staff.

2. BOOKING LEAVE
2.1 Leave is booked through the HR portal and approved by the line manager.
2.2 No more than ten consecutive working days may be taken without Director approval.
2.3 The Company may require up to three days to be taken over the winter shutdown.

3. CARRY-OVER
3.1 Up to 5 untaken days may be carried into the next Leave Year and must be used by 31 March; days not used by then are lost.
3.2 Untaken days above the carry-over limit are lost at the end of the Leave Year and are not paid in lieu.
3.3 Exception: an employee who was unable to take leave during the Leave Year because of sickness absence or family leave may carry all untaken days of the Entitlement, to be used within 18 months of the end of that Leave Year.

4. LEAVING THE COMPANY
4.1 Accrued untaken leave is paid on leaving; leave taken in excess is deducted from final pay.

5. BUYING AND SELLING
5.1 Employees may buy up to five extra days each Leave Year through salary sacrifice. Selling leave is not permitted.

6. PUBLIC HOLIDAYS
6.1 Public holidays are in addition to the Entitlement. Part-time staff receive a pro rata allowance.

7. LONG SERVICE
7.1 After five years' service the Entitlement increases by one day, and by a further day after ten years.

8. DISPUTES
8.1 Questions about carry-over are decided by the HR Business Partner, whose decision is final.

AMENDMENT No. 2 — issued 3 December 2024
Applies to Leave Years starting on or after 1 January 2025.
A1. In clause 3.1, "5 untaken days" is replaced by "8 untaken days".
A2. Clauses 3.2 and 3.3 are unchanged.

EMPLOYEE RECORD — Maren Okafor, QA Engineer, full-time
• 2025 Entitlement: 25 days. Taken: 14 days. Untaken at 31 December 2025: 11 days.
• 2025 absence: three days of sickness absence in February.
• Bought leave: none.
• Request to HR, 15 December 2025: "Please carry all 11 days into 2026 — I was off sick this year and couldn't plan properly."
• Line manager: "Maren was very busy on the release in Q4; I'd like to help if the policy allows."
""",
[("carry_8_days", "Short sickness in February did not stop her taking leave, so the ordinary limit applies, which Amendment No. 2 set at 8 days for 2025."),
 ("carry_5_days", "Clause 3.1 limits carry-over to 5 untaken days, and because the February sickness did not stop her taking leave, the exception in 3.3 does not apply."),
 ("carry_all_11_days", "Sickness absence prevented her taking her leave, so the exception in 3.3 lets all 11 untaken days carry over."),
 ("pay_in_lieu_3_days", "She can carry 8 days into 2026, and the remaining 3 untaken days above the limit are paid in lieu at the end of the Leave Year under clause 3.2.")],
"carry_8_days", 2,
twin=T([("three days of sickness absence in February",
         "sickness absence from 1 September to 31 December 2025; her manager records that she was unable to take leave during that time")],
       "carry_all_11_days")),

# ------------------------------------------------------------------ em07
# why: death on 4 Aug 2025 -> amendment (deaths on/after 1 Jul 2025) adds step-parents to
# Close Relative -> 5 paid days; extra travel days are unpaid -> 5 paid days.
# Twin: death 14 Jun 2025 -> old definition -> step-parent not Close Relative -> 1 paid day.
C("em07", "How much paid bereavement leave should the employee receive?",
"""
CRESTLINE FOODS — COMPASSIONATE AND BEREAVEMENT LEAVE POLICY

1. DEFINITIONS
1.1 "Close Relative" means a spouse or partner, child, parent, sibling or grandparent of the employee.
1.2 "Other Relative or Friend" means any person not falling within 1.1.
1.3 "Working Day" means a day the employee is rostered to work.

2. BEREAVEMENT LEAVE
2.1 On the death of a Close Relative, the employee is entitled to 5 Working Days of paid bereavement leave.
2.2 On the death of an Other Relative or Friend, the employee is entitled to 1 Working Day of paid leave to attend the funeral.
2.3 Where the funeral takes place more than 500 km from the employee's home, up to 2 additional Working Days may be taken as unpaid leave.
2.4 Bereavement leave need not be taken in one block but must be used within eight weeks of the death.

3. COMPASSIONATE LEAVE
3.1 Up to 3 Working Days of unpaid compassionate leave a year may be granted for serious illness of a Close Relative.

4. RECORDING
4.1 Managers record bereavement leave in the rota system under code BRV. No evidence of the death is required.

5. SUPPORT
5.1 The Employee Assistance Programme offers free confidential counselling. Managers should mention it in their first conversation.

6. PAY DURING LEAVE
6.1 Paid bereavement leave is paid at normal basic pay, including any regular shift allowance.
6.2 Unpaid days are deducted at the daily rate of basic pay.

7. RETURNING TO WORK
7.1 Managers should hold a short return meeting and consider a phased return where the employee asks for one.
7.2 Any further time off needed after bereavement leave is taken as annual leave or unpaid leave by agreement.

EQUALITY
The organisation applies this document fairly and consistently, without discrimination on the basis of any protected characteristic, and monitors its use to identify any unintended effects.

POLICY CHANGE NOTICE — HR Bulletin 2025/11
Applies to deaths occurring on or after 1 July 2025.
C1. The definition of Close Relative in 1.1 is extended to include a step-parent, a step-child and a parent-in-law.
C2. No other change.

LEAVE REQUEST — Joanna Petrakis, Line Supervisor, Plant 2
• Her stepfather, who raised her from the age of six, died on 4 August 2025.
• The funeral is in Varnholm, 640 km from her home.
• She asks for leave from 6 to 14 August, which covers 7 rostered Working Days.
• Her manager's message: "Given the distance I'd like to pay all 7 days if we can."
""",
[("paid_5_days", "The amended definition makes a stepfather a Close Relative, so 5 days are paid and the 2 travel days are unpaid."),
 ("paid_7_days", "Five days for a Close Relative plus two travel days for a funeral over 500 km away gives 7 paid days."),
 ("paid_1_day", "A stepfather is outside the definition of Close Relative that governs this death, so only the one funeral day is paid."),
 ("unpaid_compassionate_only", "Step-relatives fall under compassionate leave in section 3, which is unpaid.")],
"paid_5_days", 1,
twin=T([("died on 4 August 2025", "died on 14 June 2025"), ("leave from 6 to 14 August", "leave from 16 to 24 June")], "paid_1_day")),

# ------------------------------------------------------------------ em08
# why: Annex 1 as updated 1 Mar 2025 adds outdoor lighting (and removes garden furniture); the
# new employer sells outdoor lighting -> Competitor -> refuse. Paid retail work is not the
# creative exclusion. Twin: new employer sells garden furniture -> not a Competitor; 8 hours
# a week within 12 -> approve.
C("em08", "What decision should the Compliance team make on the secondary employment request?",
"""
FERNHILL OUTDOOR LTD — CONFLICTS OF INTEREST AND SECONDARY EMPLOYMENT POLICY

1. DEFINITIONS
1.1 "Secondary Employment" means any paid work for another person or organisation, including self-employment, but excluding (a) unpaid voluntary work and (b) occasional creative work, such as writing, illustration or music, earning less than £2,000 in a year.
1.2 "Competitor" means any organisation that sells products within the Company's Product Lines.
1.3 "Product Lines" means the categories listed in Annex 1 as in force on the date of the request.

2. SECONDARY EMPLOYMENT
2.1 Employees must obtain written approval from Compliance before starting any Secondary Employment.
2.2 Approval will be given unless (a) the other organisation is a Competitor or (b) the Secondary Employment would exceed 12 hours a week.
2.3 Secondary Employment must not be carried out during working hours or using Company equipment.

3. GIFTS AND HOSPITALITY
3.1 Gifts over £50 from suppliers must be declared within five working days.

4. FAMILY RELATIONSHIPS
4.1 Employees must declare any close family member who works for a supplier or Competitor.

5. SHAREHOLDINGS
5.1 Holdings above 1% of the shares in a supplier or Competitor must be declared.

6. BREACH
6.1 Starting Secondary Employment without approval is Misconduct under the Disciplinary Procedure.
6.2 Approval may be withdrawn if the circumstances change, for example if the other organisation becomes a Competitor.

7. REVIEW
7.1 Compliance decides requests within ten working days; the decision is recorded on the employee's file.

ANNEX 1 — PRODUCT LINES (original, January 2024)
Garden tools; planters and pots; garden furniture; barbecues.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

ANNEX 1 UPDATE — effective 1 March 2025
Garden furniture is removed following the sale of that division. Outdoor lighting is added following the launch of the Glowpath range.
Current list: garden tools; planters and pots; barbecues; outdoor lighting.

REQUEST — submitted 7 April 2025
Employee: Tobias Quennell, Warehouse Team Leader.
Proposed work: Saturday sales assistant at Lumen & Vale, an independent shop in Carrick Mews which sells outdoor lighting and solar lanterns. Paid hourly, about 8 hours a week, outside Fernhill working hours.
Tobias adds: "I also sell the odd pencil drawing online, maybe £300 a year."
Manager's comment: "Tobias is reliable. I don't see any problem with a weekend job."
""",
[("refuse_competitor", "Under the updated Annex 1 the shop sells a Company Product Line, so it is a Competitor and 2.2(a) requires refusal."),
 ("approve_secondary_employment", "The shop sells nothing in the Company's Product Lines and the hours are within 12 a week, so approval must be given."),
 ("no_approval_needed", "Occasional small-scale work falls outside Secondary Employment, so no approval is needed."),
 ("refuse_hours_limit", "Weekend work on top of a full-time role goes over the 12-hour weekly limit in 2.2(b).")],
"refuse_competitor", 2,
twin=T([("which sells outdoor lighting and solar lanterns", "which sells garden furniture and parasols")], "approve_secondary_employment")),

# ------------------------------------------------------------------ em09
# why: paid 1 Feb 2025 -> amended sliding scale applies. Service 1 Feb - 31 Oct 2025 = 9 full
# months; 24 - 9 = 15 months short; 15/24 x 6,000 = 3,750. Resignation is not exempt.
# Twin: made redundant -> exempt -> nothing repaid.
C("em09", "How much of the relocation allowance must be repaid?",
"""
TAMWORTH ORBITAL ENGINEERING — RELOCATION POLICY

1. DEFINITIONS
1.1 "Relocation Allowance" means the lump sum paid to help an employee move home for a new role.
1.2 "Payment Date" means the date the Relocation Allowance is paid through payroll.
1.3 "Full Month" means a complete calendar month of service after the Payment Date; the month in which the Payment Date falls counts if the Payment Date is the 1st.
1.4 "Exempt Leaving" means leaving because of redundancy, dismissal on grounds of ill health, or death.

2. ELIGIBILITY
2.1 Employees who move at least 60 miles at the Company's request may receive a Relocation Allowance of up to £6,000.

3. REPAYMENT
3.1 If the employee leaves within 24 months after the Payment Date, other than by Exempt Leaving, the employee repays: (a) 100% of the Relocation Allowance if leaving within 12 months; (b) 50% if leaving after 12 but within 24 months.
3.2 Repayment is deducted from final pay, with any balance invoiced.

4. TEMPORARY ACCOMMODATION
4.1 Up to eight weeks of temporary accommodation may be booked through the travel desk and is not repayable.

5. TAX
5.1 Qualifying relocation costs up to the statutory limit are paid free of tax; the rest is taxed through payroll.

6. CLAIMS
6.1 Removal costs must be supported by at least two quotations.
6.2 Claims must be submitted within six months of the move.

7. APPROVAL
7.1 Relocation Allowances are approved by the Head of the receiving department and the Reward team.
7.2 The repayment terms in force for an allowance are those set by its Payment Date.

REVIEW OF THIS DOCUMENT
This document is reviewed at least every two years by its owner. Suggestions for improvement can be sent to the policy team at any time; they do not change the document until formally adopted.

REVISED SCHEDULE — for Relocation Allowances with a Payment Date on or after 1 January 2025
R1. Clause 3.1(a) and (b) are replaced: the employee repays 1/24 of the Relocation Allowance for each Full Month short of 24 Full Months of service after the Payment Date.
R2. The Exempt Leaving rule is unchanged.

LEAVER FILE — Nadia Voss, Test Engineer
• Relocated from Kellby to Tamworth at the Company's request (140 miles).
• Relocation Allowance of £6,000 paid on 1 February 2025.
• Nadia resigned; her last day of service is 31 October 2025.
• Temporary accommodation used: six weeks.
• Payroll's draft note: "Left within a year, so full amount back."
""",
[("repay_3750", "The revised schedule applies; nine Full Months served leaves 15 short, and 15/24 of £6,000 is £3,750."),
 ("repay_6000", "She left within 12 months of the Payment Date, so clause 3.1(a) requires the full £6,000."),
 ("repay_2250", "The sliding scale charges 1/24 for each Full Month served, so 9/24 of £6,000 is £2,250."),
 ("repay_3000", "Leaving in the second half of the first year puts her in the 50% band, which is £3,000."),
 ("repay_nothing", "She left for an Exempt Leaving reason, so no part of the allowance is repayable.")],
"repay_3750", 2,
twin=T([("Nadia resigned; her last day of service", "Nadia was made redundant; her last day of service")], "repay_nothing")),

# ------------------------------------------------------------------ em10
# why: week Mon 8 - Sun 14 Sep 2025 -> revised rates from 1 Sep: 5 weekday nights x £35 =
# 175; Sat + Sun x £60 = 120; call-out min 2 h x £28 x 1.5 = 84 -> 379. Ops note to pay
# actual minutes contradicts the policy. Twin: week 25-31 Aug 2025 (old rates): 150 + 120 +
# 1 h x 42 = 312.
C("em10", "What total on-call pay should payroll process for the engineer's rota week?",
"""
GRIDLINE NETWORKS — ON-CALL AND CALL-OUT POLICY

1. DEFINITIONS
1.1 "Rota Week" means Monday to Sunday.
1.2 "Weekday Night" means an on-call period from 18:00 to 08:00 starting Monday to Friday.
1.3 "Weekend Day" means Saturday or Sunday, 00:00 to 24:00.
1.4 "Call-Out" means being required to work while on call, whether remotely or on site.
1.5 "Hourly Rate" means the employee's basic hourly rate.

2. ALLOWANCES
2.1 An employee on call receives £30 for each Weekday Night and £60 for each Weekend Day.
2.2 Allowances are paid in addition to basic pay.

3. CALL-OUT PAY
3.1 Each Call-Out is paid at 1.5 times the Hourly Rate, with a minimum payment of one hour per Call-Out.
3.2 Call-Outs are logged in the incident system and approved by the duty manager.

4. REST
4.1 An employee who works more than three hours on Call-Outs between 00:00 and 06:00 may start late the next day.

5. EQUIPMENT
5.1 On-call staff must carry the company phone and laptop and respond within 15 minutes.

6. SWAPS
6.1 Engineers may swap rota weeks with a colleague by agreement, recorded in the rota spreadsheet before the week starts.
6.2 Allowances follow whoever is actually on call.

7. PUBLIC HOLIDAYS
7.1 A public holiday that falls on a weekday is paid at the Weekend Day allowance instead of the Weekday Night allowance.

8. PAYMENT
8.1 Allowances and Call-Out pay are paid in the month after the Rota Week, based on the approved incident log.
8.2 Only the People team can change the rates in this policy.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

POLICY REVISION — effective for Rota Weeks beginning on or after 1 September 2025
R1. In clause 2.1, "£30 for each Weekday Night" becomes "£35 for each Weekday Night". The Weekend Day rate is unchanged.
R2. In clause 3.1, the minimum payment becomes two hours per Call-Out.

ROTA RECORD — Priyanka Sahni, Network Engineer, Hourly Rate £28
Rota week of 8–14 September 2025: on call for all five Weekday Nights and both Weekend Days.
Call-Outs: one, on Wednesday night, 40 minutes remote fix of a core switch fault; approved by the duty manager.
No public holidays fell in that rota week.

NOTE ATTACHED TO THE ROTA SPREADSHEET
"Payroll: from now on pay call-outs for the actual minutes worked only, per ops lead. Keeps costs down."
""",
[("pay_379", "Revised rates apply: 5 × £35 + 2 × £60 = £295, plus a two-hour minimum Call-Out at £42 an hour = £84, total £379."),
 ("pay_312", "Allowances of 5 × £30 + 2 × £60 = £270 plus a one-hour minimum Call-Out at £42 give £312."),
 ("pay_337", "Revised allowances give 5 × £35 + 2 × £60 = £295, and the Call-Out is paid at the one-hour minimum of 1.5 × £28 = £42, giving £337 in total."),
 ("pay_323", "The revised allowances come to 5 × £35 + 2 × £60 = £295, and the Call-Out is paid for the 40 minutes actually worked at £42 an hour, £28, giving £323.")],
"pay_379", 2,
twin=T([("Rota week of 8–14 September 2025", "Rota week of 25–31 August 2025")], "pay_312")),

# ------------------------------------------------------------------ em11
# why: Completion Date = final assessment 10 Mar 2025 (not the 20 May certificate). Leaving
# 15 Sep 2025 = 6 months 5 days after -> 6-12 month band = 50% of 4,800 = 2,400. Addendum
# covers agreements signed on/after 1 Jan 2025; this one was signed 14 Nov 2024 -> not applied.
# Twin: signed 14 Jan 2025 -> addendum 40% -> 1,920.
C("em11", "What amount should be recovered under the training agreement?",
"""
LANTERNFISH MEDIA — TRAINING COST AGREEMENT (standard terms)

1. DEFINITIONS
1.1 "Course" means the Advanced Broadcast Engineering Diploma run by the Cardew Institute.
1.2 "Course Fee" means the fee paid by the Company to the provider: £4,800.
1.3 "Completion Date" means the date of the final assessment of the Course, whether or not a certificate has yet been issued.
1.4 "Leaving Date" means the employee's last day of employment.

2. COMPANY COMMITMENTS
2.1 The Company pays the Course Fee directly and allows up to ten days' paid study leave.

3. REPAYMENT
3.1 If the employee resigns with a Leaving Date within 18 months after the Completion Date, the employee repays part of the Course Fee:
(a) within 6 months: 100%;
(b) after 6 and within 12 months: 50%;
(c) after 12 and within 18 months: 25%.
3.2 No repayment is due if the employee leaves because of redundancy.
3.3 Repayment may be deducted from final salary with the employee's written consent given in this agreement.

4. FAILURE TO COMPLETE
4.1 If the employee withdraws from the Course without good reason, the full Course Fee is repayable.

5. STUDY LEAVE
5.1 Study leave must be booked at least two weeks in advance and cannot be carried forward after the Completion Date.

6. EXAMINATION RESITS
6.1 The Company pays for one resit of any module. Further resits are at the employee's cost.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

REVIEW OF THIS DOCUMENT
This document is reviewed at least every two years by its owner. Suggestions for improvement can be sent to the policy team at any time; they do not change the document until formally adopted.

7. VARIATION
7.1 These standard terms may be varied by an addendum; an addendum applies only to the agreements it names.

ADDENDUM TO STANDARD TERMS — applies to agreements signed on or after 1 January 2025
AD1. In clause 3.1(b), "50%" is replaced by "40%".
AD2. All other terms continue.

EMPLOYEE FILE — Sam Oduya, Transmission Engineer
• Training agreement signed 14 November 2024.
• Final assessment of the Course: 10 March 2025. Certificate issued by the Cardew Institute: 20 May 2025.
• Sam resigned; Leaving Date 15 September 2025.
• Study leave used: eight days.
• Finance assistant's draft: "Leaving within six months of getting the certificate, so recover the full fee."
""",
[("recover_2400", "Measured from the 10 March final assessment, the Leaving Date falls in the 6–12 month band, and the original 50% rate governs this agreement."),
 ("recover_1920", "The Leaving Date is in the 6–12 month band and the addendum's 40% rate applies to this agreement, giving £1,920."),
 ("recover_4800", "Counting from the date the certificate was issued, 20 May 2025, the Leaving Date of 15 September is within six months, so the full £4,800 Course Fee is repayable."),
 ("recover_1200", "More than six months have passed since the Completion Date, so the 25% rate applies, giving £1,200.")],
"recover_2400", 3,
twin=T([("Training agreement signed 14 November 2024.", "Training agreement signed 14 January 2025.")], "recover_1920")),

# ------------------------------------------------------------------ em12
# why: request received 10 Apr 2025 (on/after 6 Apr) -> Decision Period 2 months -> ended
# 10 Jun 2025; no decision, no agreed extension -> treated as approved on trial.
# Previous request 2 Mar 2024 > 12 months earlier -> valid. Twin: received 2 Apr 2025 ->
# old 3-month period -> ends 2 Jul 2025 -> still within period on 20 Jun.
C("em12", "As of 20 June 2025, what is the status of the flexible working request?",
"""
DUNMORE HOUSING ASSOCIATION — FLEXIBLE WORKING POLICY

1. DEFINITIONS
1.1 "Request" means a written application to change hours, times or place of work.
1.2 "Decision Period" means three months beginning with the day the Request is received, unless the employee agrees in writing to extend it.
1.3 "Decision" means written notice to the employee approving, approving on trial or refusing the Request.

2. MAKING A REQUEST
2.1 Any employee may make a Request from the first day of employment.
2.2 An employee may make no more than one Request in any 12-month period, counted back from the date the new Request is received.

3. HANDLING A REQUEST
3.1 The manager should meet the employee to discuss the Request before refusing it.
3.2 A Request may be refused only for one of the business reasons listed in Appendix 1.
3.3 If no Decision is given within the Decision Period, and no extension has been agreed, the Request is treated as approved for a trial period of three months.

4. APPEALS
4.1 An employee may appeal a refusal within 14 days to a Director.

5. TRIAL PERIODS
5.1 A trial period lets both sides test the arrangement; at its end the manager confirms or ends the arrangement in writing.
5.2 During a trial, either side may end the arrangement on two weeks' notice.

6. RECORD KEEPING
6.1 Managers log each Request in the HR system on the day it is received.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

POLICY UPDATE — effective 6 April 2025
Applies to Requests received on or after 6 April 2025. Earlier Requests continue under the previous wording.
U1. In clause 1.2, "three months" is replaced by "two months".
U2. Clause 3.1 becomes mandatory: a Request may not be refused without a meeting.

CASE — Harriet Bamidele, Income Officer
• Previous Request (compressed hours) received 2 March 2024; approved.
• Current Request (to work Mondays from home) received by the manager on 10 April 2025.
• No meeting has been held and no Decision has been sent. No extension has been discussed.
• Manager's draft email, not yet sent: "I'm minded to refuse because of front-desk cover on Mondays (Appendix 1, reason 4)."
• Today's date: 20 June 2025.
""",
[("treated_as_approved_trial", "The two-month Decision Period for this Request ended on 10 June with no Decision or extension, so clause 3.3 treats it as approved on trial."),
 ("still_within_decision_period", "The Decision Period for this Request has not yet ended, so the manager can still decide it."),
 ("refused_business_reason", "Front-desk cover on Mondays is one of the business reasons listed in Appendix 1, so the manager's stated reason means the Request stands refused."),
 ("invalid_repeat_request", "Clause 2.2 allows only one Request in any 12-month period, and the employee has already made a Request for compressed hours, so this second Request is invalid.")],
"treated_as_approved_trial", 2,
twin=T([("received by the manager on 10 April 2025", "received by the manager on 2 April 2025")], "still_within_decision_period")),

# ------------------------------------------------------------------ em13
# why: amendment (from 1 Jul 2025) extends full pay to the first 10 Working Days of jury
# service; employee has 8 months' service, so no top-up after day 10 (needs 12 months).
# Days 11-15: court allowance only. HR assistant's "top everyone up" note is not policy.
C("em13", "How should payroll treat days 11 to 15 of the employee's jury service?",
"""
KINGSMERE LOGISTICS — PUBLIC DUTIES AND JURY SERVICE POLICY

1. DEFINITIONS
1.1 "Jury Service" means attendance at court following a jury summons.
1.2 "Working Day" means a day the employee is rostered to work.
1.3 "Court Allowance" means the loss-of-earnings allowance paid by the court to jurors.
1.4 "Qualifying Service" means 12 months' continuous employment at the start of Jury Service.

2. TIME OFF
2.1 Employees must be released for Jury Service and must give their manager a copy of the summons as soon as received.
2.2 Employees must return to work on any day, or part day, on which they are not required at court.

3. PAY
3.1 The Company pays full normal pay for the first 5 Working Days of Jury Service.
3.2 After that, the employee claims the Court Allowance directly from the court.
3.3 Employees with Qualifying Service also receive a Company top-up equal to the difference between the Court Allowance and full normal pay.
3.4 Employees without Qualifying Service receive no top-up.

4. OTHER PUBLIC DUTIES
4.1 Up to 12 days' paid leave a year is allowed for magistrates, school governors and reserve forces training.

5. DEFERRAL
5.1 The Company will ask the court to defer Jury Service only where the employee's absence would cause serious harm to the business, and only with the employee's agreement.

6. PAYROLL PROCESS
6.1 The employee submits the court's attendance record each week.
6.2 Payroll applies the policy in force on the first day of Jury Service to the whole period of service.
6.3 Overpayments are recovered from the next salary payment.

EQUALITY
The organisation applies this document fairly and consistently, without discrimination on the basis of any protected characteristic, and monitors its use to identify any unintended effects.

AMENDMENT — effective for Jury Service starting on or after 1 July 2025
A1. In clause 3.1, "5 Working Days" is replaced by "10 Working Days".
A2. Clauses 3.3 and 3.4 are unchanged.

CASE — Lucian Achterberg, Transport Planner
• Start date: 6 January 2025.
• Jury Service from 8 September 2025, lasting 15 Working Days.
• Summons provided to the manager on 12 August 2025.
• Court Allowance claimed from day 11 onwards.

NOTE FROM HR ASSISTANT
"In practice we top everyone up to full pay — it's simpler for payroll and nobody checks service length."
""",
[("court_allowance_only", "Full pay covers the first 10 Working Days, and with only eight months' service there is no top-up, so days 11–15 rely on the Court Allowance."),
 ("top_up_to_full_pay", "After the Company-paid days end, clause 3.3 gives a top-up equal to the difference between the Court Allowance and full normal pay, so pay stays at the normal level."),
 ("full_pay_all_days", "Jury Service is always on full pay, so days 11–15 are paid in full by the Company."),
 ("court_allowance_from_day_6", "The Company pays only the first five Working Days, so days 6–15 are covered by the Court Allowance alone.")],
"court_allowance_only", 1),
]
