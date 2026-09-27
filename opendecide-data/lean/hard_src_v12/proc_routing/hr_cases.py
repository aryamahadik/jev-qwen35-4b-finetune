"""proc_routing / people-services case routing (Castlereagh Retail Group, invented)."""
from _lib import C, T

GUIDE = """
CASTLEREAGH RETAIL GROUP — PEOPLE SERVICES CASE ROUTING (issue 5)
1. Payroll Services: pay, tax codes, deductions, and recovery of overpayments up to £1,000.
2. HR Advice: leave, contracts, policy questions, flexible-working guidance, right-to-work reminders.
3. Employee Relations (ER): formal grievances, disciplinary cases, attendance reviews referred by managers.
4. ER Specialist: allegations of harassment, bullying or discrimination.
5. Speak Up Line (run for the Audit Committee): protected disclosures, meaning reports of wrongdoing in the public interest such as fraud, danger to health or safety, environmental damage, or breach of a legal obligation.
6. HR Director: any complaint about a member of People Services staff.
7. Data Protection Officer (DPO): requests for access to the personal data we hold about the requester.
Conflicts: a case that fits both 3 and 5 goes to the Speak Up Line. A complaint about People Services staff goes under 6 before 3 or 4.
"""

ITEMS = [
# ------------------------------------------------------------------ hr01
# why: manager faking fridge temperature logs = danger to health/safety and a
#      legal breach -> protected disclosure -> Speak Up (beats ER under conflicts).
#      twin: unfair rota -> personal grievance -> ER.
C("rt_hr01", "Where should People Services route this case?",
GUIDE + """
Case PS-20417 — received by email, Tuesday
From: Kerry Mulvaney, Bakery Assistant, Store 214 (Aldwick)
"I want to raise a formal grievance about my manager. He has been writing fridge temperature readings into the food-safety log that were never taken, so the log looks fine when the chillers are breaking down. I've seen him fill in a whole week at once."
Previous cases for this employee: none.
""",
[("route_speak_up_line", "Faked food-safety readings are a danger to health and a legal breach, a protected disclosure, and the conflicts rule sends it to Speak Up over ER."),
 ("route_employee_relations", "She calls it a formal grievance about her own treatment by her manager, so ER takes it."),
 ("route_hr_advice", "Food-safety logging is covered by store policy, and questions about how a policy is applied are HR Advice matters under rule 2 of the routing guide, not grievances."),
 ("route_er_specialist", "Complaints about a manager's behaviour count as bullying for the ER Specialist.")],
"route_speak_up_line", 2,
twin=T([("He has been writing fridge temperature readings into the food-safety log that were never taken, so the log looks fine when the chillers are breaking down. I've seen him fill in a whole week at once.",
         "He keeps giving me the late closing shifts that nobody else wants, and I think it's unfair. I've had five in a row now.")],
       "route_employee_relations")),

# ------------------------------------------------------------------ hr02
# why: complaint about an HR Business Partner (People Services staff) -> rule 6
#      HR Director, ahead of ER; sharing papers is not a DSAR.
C("rt_hr02", "Which route is correct for case PS-20533?",
GUIDE + """
Case PS-20533 — received through the HR portal
From: Tomasz Brzezinski, Warehouse Operative, Dunhill distribution centre
"I want to complain about Lorna Pike, my HR Business Partner. She sent my grievance papers from last month to my shift manager, the person the grievance was about, before the hearing. I did not agree to that."
People Services directory: Lorna Pike — HR Business Partner, North region (People Services).
""",
[("route_hr_director", "Lorna Pike is an HR Business Partner and so People Services staff, and rule 6 sends complaints about People Services staff to the HR Director before ER."),
 ("route_employee_relations", "It is a formal complaint about how his grievance was handled, which is ER work."),
 ("route_dpo", "His grievance papers were shared with the shift manager without his consent, which is a personal-data matter, so the DPO handles it under rule 7."),
 ("route_speak_up_line", "Sharing grievance papers is wrongdoing that belongs on the Speak Up Line.")],
"route_hr_director", 1),

# ------------------------------------------------------------------ hr03
# why: amendment: overpayments over £1,000 -> Payroll Manager. 640 + 450 = 1,090
#      > 1,000. twin April 350 -> 990 -> Payroll Services.
C("rt_hr03", "Who should handle recovery of this overpayment?",
GUIDE + """
Payroll Bulletin 9 (amends rule 1 from 1 May): overpayments totalling more than £1,000 for one employee go to the Payroll Manager, who agrees a repayment plan. Overpayments of £1,000 or less stay with Payroll Services.

Case PS-20611
Employee: Bethan Oduya, Customer Services Supervisor, Store 118
Issue: paid at supervisor rate after stepping down to assistant on 1 March.
Overpayment: March £640; April £450. Stopped from May payroll.
Employee note: "I didn't notice. I can't repay it all at once."
""",
[("route_payroll_manager", "£640 plus £450 is £1,090, over £1,000, so Bulletin 9 sends the recovery to the Payroll Manager."),
 ("route_payroll_services", "The combined overpayment is £1,000 or less, so Payroll Services recovers it under rule 1."),
 ("route_employee_relations", "Recovering money from an employee is a disciplinary matter for ER."),
 ("route_hr_advice", "Bethan says she cannot repay the money at once, and repayment arrangements are a policy question for HR Advice under rule 2.")],
"route_payroll_manager", 2,
twin=T([("April £450", "April £350")], "route_payroll_services")),

# ------------------------------------------------------------------ hr04
# why: appeal against a refused flexible-working request -> Appeals Panel;
#      ER only if a formal grievance is raised.
C("rt_hr04", "Where should this email be sent?",
GUIDE + """
Flexible Working Procedure (extract)
FW4. Requests are decided by the line manager. FW5. An appeal against a refusal goes to an Appeals Panel chaired by a manager not involved in the first decision. ER is not involved unless the employee raises a separate formal grievance.

Case PS-20702 — email to People Services
From: Saoirse Kinsella, Visual Merchandiser, Store 031
"On 3 June my manager turned down my request to finish at 15:00 on Tuesdays and Thursdays. I'm appealing that decision; the reasons given don't match the rota. I don't want to raise a grievance, just have it looked at again."
""",
[("route_appeals_panel", "She is appealing her manager's refusal of a flexible-working request, which FW5 sends to an Appeals Panel chaired by a manager not involved in the first decision."),
 ("route_line_manager", "Flexible-working requests are decided by the line manager under FW4."),
 ("route_employee_relations", "Challenging a manager's decision is a grievance for ER."),
 ("route_hr_advice", "Flexible working appears under HR Advice in rule 2 of the routing guide, so every flexible-working email, including appeals, goes to HR Advice.")],
"route_appeals_panel", 1),

# ------------------------------------------------------------------ hr05
# why: 2 Oct -> 16 Nov = 29 + 16 = 45 days <= 60 -> Compliance.
#      twin 16 Dec = 29 + 30 + 16 = 75 days -> HR Advice diary reminder.
C("rt_hr05", "What should HR Advice do with this right-to-work check?",
GUIDE + """
Right-to-Work Standard RW3: where an employee's permission to work expires within 60 days, HR Advice passes the case to the Compliance team. Otherwise HR Advice sets a diary reminder for 60 days before expiry.

Case PS-20788 — raised by the HR system on 2 October
Employee: Ahmed Siddiqui, Night Shift Team Leader, Dunhill distribution centre
Permission to work: expires 16 November
Note from employee: "My renewal application was sent in August and I'm waiting for the decision."
""",
[("pass_to_compliance", "From 2 October to 16 November is 45 days, within 60, so RW3 sends the case to Compliance."),
 ("set_hr_advice_reminder", "Expiry is more than 60 days away, so HR Advice sets a diary reminder."),
 ("route_employee_relations", "An employee who may lose the right to work faces a disciplinary process under ER."),
 ("no_action_renewal_pending", "His renewal application was sent in August and is still waiting for a decision, so no action is needed until that decision arrives.")],
"pass_to_compliance", 2,
twin=T([("expires 16 November", "expires 16 December")], "set_hr_advice_reminder")),

# ------------------------------------------------------------------ hr06
# why: harassment allegation -> ER Specialist always; the informal-resolution
#      option excludes harassment; the employee's wish does not change routing.
C("rt_hr06", "Which route applies to case PS-20840?",
GUIDE + """
Grievance Policy G2: an employee may ask for a grievance to be resolved informally by their line manager, except allegations of harassment, bullying or discrimination, which always go to the ER Specialist.

Case PS-20840 — email to People Services
From: Leah Brannigan, Checkout Operator, Store 214
"A colleague on my shift keeps making comments about my body and last week he blocked the stockroom door and wouldn't let me out until I 'smiled for him'. Please don't send this to ER — I'd rather my manager just has a quiet word with him."
""",
[("route_er_specialist", "It is an allegation of harassment, and G2 excludes harassment from informal resolution, so it always goes to the ER Specialist whatever informal route Leah asks for."),
 ("resolve_informally_with_manager", "Leah asked for her manager to have a quiet word rather than a formal process, and G2 lets an employee ask for informal resolution by the line manager."),
 ("route_employee_relations", "It is a grievance about a colleague, so ER handles it under rule 3."),
 ("route_speak_up_line", "Blocking a door is a safety danger, which makes it a protected disclosure.")],
"route_er_specialist", 1),

# ------------------------------------------------------------------ hr07
# why: rolling 6 months to 31 July starts 1 February; absences 3 Feb, 14 Apr,
#      20 Jul = 3 -> attendance review referred to ER.
#      twin first absence 23 January -> outside window -> 2 -> record only.
C("rt_hr07", "What routing does this attendance record require?",
GUIDE + """
Attendance Policy AT2: three or more separate absences in any rolling six months, or a single absence longer than four weeks, triggers an attendance review, which the store manager refers to ER. Fewer absences are recorded only.

Case PS-20915 — raised by store manager on 31 July
Employee: Callum Fitzgerald, Stock Replenisher, Store 118
Absences in the six months to 31 July (window starts 1 February):
- 3 February: 2 days (cold)
- 14 April: 1 day (dental)
- 20 July: 3 days (back pain)
Occupational health: no referral requested; longest absence 3 days.
""",
[("refer_er_attendance_review", "Three separate absences fall inside the six months from 1 February, which triggers an attendance review for ER."),
 ("record_only", "Only two absences fall inside the rolling six months, so the absences are recorded only."),
 ("refer_occupational_health", "The latest absence was for back pain, and a musculoskeletal absence needs an occupational health referral before any attendance review can go ahead."),
 ("route_hr_advice", "Absence questions are leave matters for HR Advice under rule 2.")],
"refer_er_attendance_review", 2,
twin=T([("- 3 February: 2 days (cold)", "- 23 January: 2 days (cold)")], "record_only")),

# ------------------------------------------------------------------ hr08
# why: reported 16:20 (after 15:00) but employee cannot pay rent -> hardship ->
#      Emergency Advance by Store Manager at any time.
#      twin: not urgent -> after 15:00 -> queued for Payroll Services next day.
C("rt_hr08", "How should this missing-pay report be routed?",
GUIDE + """
Payroll Procedure P7 — missing pay
P7.1 Reports made before 15:00 on pay day go to the Payroll Urgent line for same-day payment.
P7.2 Reports after 15:00 are queued for Payroll Services on the next working day.
P7.3 Where the employee says they cannot pay for essentials (food, rent, travel to work), the Store Manager may approve an Emergency Advance at any time.

Case PS-21003 — phone call logged at 16:20 on pay day (Friday 28th)
Employee: Nadia Okonkwo, Customer Assistant, Store 031
"My wages haven't arrived. I can't pay my rent, which is due tomorrow."
Payroll check: her new bank details were keyed with one digit wrong.
""",
[("approve_emergency_advance", "She says she cannot pay her rent, an essential, so P7.3 lets the Store Manager approve an Emergency Advance at any time."),
 ("queue_payroll_services", "The report came after 15:00 and nothing makes it urgent, so it is queued for Payroll Services next working day."),
 ("route_payroll_urgent_line", "Missing pay reported on pay day itself always goes to the Payroll Urgent line, which can make a same-day payment to fix the wrong bank digit."),
 ("route_hr_advice", "Bank-detail errors are contract data for HR Advice.")],
"approve_emergency_advance", 2,
twin=T([("I can't pay my rent, which is due tomorrow.", "It's not urgent, I just want to know when it will arrive.")], "queue_payroll_services")),

# ------------------------------------------------------------------ hr09
# why: request for all emails/notes about him = access to personal data -> DPO.
C("rt_hr09", "Which team should receive this request?",
GUIDE + """
Case PS-21077 — email to People Services
From: Ifeanyi Obi, Assistant Store Manager, Store 214
"Please send me copies of all emails and notes where managers discussed my promotion application this year, plus anything else you hold about me. I'd also like a copy of my current contract."
Note: Ifeanyi's promotion application was unsuccessful on 30 April; he has not raised a grievance.
""",
[("route_dpo", "He asks for everything held about him, including managers' emails and notes, which is a request for access to his personal data, so the DPO handles it under rule 7."),
 ("route_hr_advice", "He asks for a copy of his current contract, and HR Advice provides contracts under rule 2, so HR Advice can gather and send everything he asks for in one reply."),
 ("route_employee_relations", "Questions about a failed promotion are a grievance for ER.")],
"route_dpo", 1),

# ------------------------------------------------------------------ hr10
# why: GR6: signed by five or more -> Industrial Relations Lead. Six signatories.
#      Being union members is not submission by a union rep.
#      twin: four signatories -> ER.
C("rt_hr10", "Where does this grievance go?",
GUIDE + """
Grievance Policy GR6: grievances signed by five or more employees, or submitted by a trade union representative on behalf of a group, go to the Industrial Relations Lead instead of ER.

Case PS-21140 — letter handed in at Store 118
"We, the undersigned, object to the new split-shift pattern that starts on 1 September. It leaves a three-hour unpaid gap in the middle of the day. Several of us are members of the retail union, but we are writing for ourselves."
Signed: Joanne Kerr, Ravi Menon, Aoife Dunne, Patrick Lowe, Marta Silva, Hugh Pemberton
""",
[("route_industrial_relations_lead", "Six employees signed the grievance, at least five, so GR6 sends it to the Industrial Relations Lead."),
 ("route_employee_relations", "Fewer than five employees signed and no union representative submitted it on the group's behalf, so GR6 does not apply and it is an ordinary grievance for ER."),
 ("route_hr_director", "A group complaint about the new split-shift pattern challenges a decision made by People Services, so it goes to the HR Director under rule 6.")],
"route_industrial_relations_lead", 2,
twin=T([("Signed: Joanne Kerr, Ravi Menon, Aoife Dunne, Patrick Lowe, Marta Silva, Hugh Pemberton",
         "Signed: Joanne Kerr, Ravi Menon, Aoife Dunne, Patrick Lowe")], "route_employee_relations")),

# ------------------------------------------------------------------ hr11
# why: employee made a Speak Up disclosure -> General Counsel whatever the amount
#      (£12,000 would otherwise be HR Director). twin: no disclosure -> HR Director.
C("rt_hr11", "Who must approve this settlement agreement?",
"""
Castlereagh Retail Group — Settlement Agreements Approval Note
S1. Settlement payments up to £15,000 are approved by the HR Director.
S2. Settlement payments above £15,000 are approved by the Chief Financial Officer.
S3. Any settlement with an employee who has made a protected disclosure through the Speak Up Line is approved by the General Counsel, whatever the amount.
S4. Payments include notice pay in lieu, compensation and legal-fee contributions.

Proposal ST-0419
Employee: Graham Pollitt, Regional Logistics Planner
Terms: compensation £10,500; contribution to legal fees £1,500. Total £12,000.
Background: role removed in the logistics restructure. Graham made a Speak Up disclosure (case SU-2231) in March about falsified tachograph records.
Prepared by: HR Business Partner, North region
""",
[("approve_general_counsel", "Graham made a Speak Up disclosure, so S3 requires the General Counsel whatever the amount."),
 ("approve_hr_director", "The £12,000 total is within the £15,000 limit, and nothing else in the file changes who approves, so the HR Director signs."),
 ("approve_cfo", "Compensation of £10,500 plus the £1,500 legal-fee contribution takes the payment above the HR Director's limit, so it goes to the CFO under S2.")],
"approve_general_counsel", 2,
twin=T([("Graham made a Speak Up disclosure (case SU-2231) in March about falsified tachograph records.",
         "Graham's only previous case was a 2022 holiday-pay query, resolved by Payroll Services.")], "approve_hr_director")),

# ------------------------------------------------------------------ hr12
# why: agency worker, complaint about shift allocation (not discrimination,
#      harassment or safety) -> raised with the agency.
C("rt_hr12", "Where should this agency worker's complaint be routed?",
GUIDE + """
Agency Workers Note AW2: agency workers raise grievances with their agency (Brightstaff Recruitment). Exceptions: allegations of discrimination or harassment go to our ER Specialist, and health and safety concerns go to the site Health & Safety team.

Case PS-21206 — message via the site kiosk
From: Oksana Petrenko, agency picker (Brightstaff), Dunhill distribution centre
"I get offered fewer weekend shifts than the other pickers on my team. When I asked, the planner said weekend shifts go to people who have been here longest. I've been here eight months and want this looked at."
""",
[("refer_to_agency", "She is an agency worker, and a grievance about weekend shifts being allocated by length of service is not discrimination, harassment or safety, so AW2 sends it to Brightstaff."),
 ("route_er_specialist", "Oksana is offered fewer weekend shifts than the other pickers on her team, and being treated less well than colleagues is discrimination for the ER Specialist."),
 ("route_employee_relations", "Shift allocation grievances go to ER under rule 3 for everyone on site.")],
"refer_to_agency", 2),

# ------------------------------------------------------------------ hr13
# why: notice takes effect 1 November; allegation received 30 October -> old
#      rule 4 -> ER Specialist.
C("rt_hr13", "Which team takes this allegation?",
GUIDE + """
People Services Notice 22 (issued 15 October): from 1 November, allegations of harassment, bullying or discrimination go to the new Respect at Work Team instead of the ER Specialist. Cases received before 1 November stay with the ER Specialist until closed.

Case PS-21290 — received through the HR portal on 30 October at 17:45
From: Daniel Achterberg, Pharmacy Counter Assistant, Store 031
"My supervisor has mocked my stammer in front of customers several times this month. On 28 October she imitated me over the tannoy."
Portal note: triage delayed; first opened by People Services on 2 November.
""",
[("route_er_specialist", "The allegation was received on 30 October, before Notice 22 took effect, so it stays with the ER Specialist."),
 ("route_respect_at_work_team", "People Services first opened the case on 2 November, after Notice 22 took effect, so the new Respect at Work Team takes the allegation."),
 ("route_employee_relations", "Mockery by a supervisor is a formal grievance for ER.")],
"route_er_specialist", 2),
]
