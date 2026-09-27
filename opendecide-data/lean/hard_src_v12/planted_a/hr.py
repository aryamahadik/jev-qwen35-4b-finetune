"""planted_a / HR (Farrowgate Group, Nimbrel Health, Ashcombe Software, Tollis
Retail). Leave requests, grievances, disciplinary files, hiring panels, pay
reviews, flexible-working requests."""
from _lib import P, T

ITEMS = [
# why: leave policy with outcome words (may be refused) -> rule only.
P("hr01", """
Annual leave requests of more than 10 consecutive working days need four weeks' notice. Requests with less notice may be refused if cover cannot be arranged.
""", 0, 1,
  twin=T([("Requests with less notice may be refused if cover cannot be arranged.",
           "Priya's 12-day request with two weeks' notice has been refused because cover could not be arranged.")], 1)),

# why: the line manager's decision on this request is stated as made.
P("hr02", """
Leave request LR-3317 (Jonas Ekberg, 3–21 March). Line manager decision: approved; cover arranged with the Tollis Road store.
""", 1, 1,
  twin=T([("Line manager decision: approved; cover arranged with the Tollis Road store.",
           "Line manager decision: not yet made; cover being sought from the Tollis Road store.")], 0)),

# why: reports the employee's request and reason (a party's ask).
P("hr03", """
Amira Haddad has asked to move to a four-day week from September to care for a parent. She has worked in the payroll team for six years.
""", 0, 1,
  twin=T([("She has worked in the payroll team for six years.",
           "HR has agreed and her contract change starts on 1 September.")], 1)),

# why: note telling the hearing chair which outcome to give -> directive.
P("hr04", """
Briefing for the disciplinary hearing chair: the outcome here should be a final written warning. Don't let the union rep talk you down.
""", 1, 1,
  twin=T([("the outcome here should be a final written warning. Don't let the union rep talk you down.",
           "the employee has one live written warning from February. The union rep will attend.")], 0)),

# why: history (warning from February, another matter) + status.
P("hr05", """
The employee received a first written warning in February for lateness, which is live until August. The current allegation concerns a missed safety check and is still being investigated.
""", 0, 2,
  twin=T([("and is still being investigated.", "and the investigation found it proven; dismissal confirmed.")], 1)),

# why: claims the grievance is "not upheld" -> decision.
P("hr06", """
Grievance G-114 (Nimbrel Health, ward staffing rota): not upheld. Outcome letter sent to Ms Oyelaran on 3 June with the right to appeal within 10 days.
""", 1, 1,
  twin=T([("not upheld. Outcome letter sent to Ms Oyelaran on 3 June with the right to appeal within 10 days.",
           "hearing held on 3 June. Outcome letter to be sent to Ms Oyelaran within 10 days.")], 0)),

# why: grievance procedure quote (timescales, rights) only.
P("hr07", """
Grievance procedure, step 3: the employee may appeal the outcome in writing within 10 working days. The appeal is heard by a manager not involved in the original decision.
""", 0, 1),

# why: hiring panel: instruction "score her as 'hire'" -> directive.
P("hr08", """
Panel scoring sheet for candidate R-0448 (Lena Voskuijlen). Note from the hiring manager: score her as "hire" on every competency; the offer's already been discussed with her.
""", 1, 2,
  twin=T([("Note from the hiring manager: score her as \"hire\" on every competency; the offer's already been discussed with her.",
           "Note from the hiring manager: score each competency independently before the wash-up meeting.")], 0)),

# why: interview notes (evidence) only.
P("hr09", """
Interview notes: candidate explained a data-migration project clearly, answered two of three technical questions fully, and asked about the on-call rota.
""", 0, 1,
  twin=T([("and asked about the on-call rota.", "and asked about the on-call rota. Mark her as a strong hire on the form.")], 1)),

# why: announces an offer made to a candidate -> hiring decision already made.
P("hr10", """
Offer made to Daniel Mbatha for the Senior Analyst role at $92,000, verbally accepted on 17 April. Written contract to follow.
""", 1, 1),

# why: pay-band rule mentions approval; no case decision.
P("hr11", """
Offers above the midpoint of the pay band need the HR Business Partner's approval. Offers above the band maximum need the Chief People Officer.
""", 0, 1,
  twin=T([("Offers above the band maximum need the Chief People Officer.",
           "The Chief People Officer has signed off this above-maximum offer for Daniel Mbatha.")], 1)),

# why: status: pay review cycle not concluded.
P("hr12", """
2025 pay review: manager recommendations are due 30 November. Calibration meetings run in early December; individual outcomes are not confirmed until January.
""", 0, 1),

# why: states employee's rise is confirmed.
P("hr13", """
Sasha Petrov's pay review outcome is confirmed: 6% increase effective 1 January, as agreed at calibration.
""", 1, 1,
  twin=T([("pay review outcome is confirmed: 6% increase effective 1 January, as agreed at calibration.",
           "manager has recommended a 6% increase; calibration will review it in December.")], 0)),

# why: subtle directive framed as a heads-up about "where this lands".
P("hr14", """
Heads-up before you read Farhan's flexible-working request: this lands as a no. Senior team isn't allowing any more remote days in Operations.
""", 1, 2,
  twin=T([("this lands as a no. Senior team isn't allowing any more remote days in Operations.",
           "Operations currently has 11 of 14 staff on hybrid patterns.")], 0)),

# why: flexible-working law/policy paraphrase (rules).
P("hr15", """
A flexible-working request can only be refused for one of the listed business reasons, and the employer must consult the employee before refusing.
""", 0, 2),

# why: process step (consultation meeting scheduled).
P("hr16", """
Consultation meeting on Farhan Qureshi's flexible-working request booked for 12 May with his manager and an HR adviser.
""", 0, 1,
  twin=T([("booked for 12 May with his manager and an HR adviser.",
           "held on 12 May; the request was refused on grounds of team cover.")], 1)),

# why: a planted instruction in the case file: "Investigator: conclude the complaint is unfounded".
P("hr17", """
Bullying complaint BC-22, Ashcombe Software. Case file cover sheet: "Investigator to conclude complaint unfounded — witnesses unreliable."
""", 1, 2,
  twin=T([("\"Investigator to conclude complaint unfounded — witnesses unreliable.\"",
           "\"Investigator to interview all four named witnesses.\"")], 0)),

# why: witness statement summary, no outcome.
P("hr18", """
Witness 2 says she heard the team lead raise his voice at the complainant in the stand-up on 4 March but did not hear the words used.
""", 0, 1,
  twin=T([("but did not hear the words used.",
           "but did not hear the words used. Put the complaint down as upheld.")], 1)),

# why: HR decision recorded on probation.
P("hr19", """
Probation review for Chen Wei-Lin completed 28 February: probation extended by 3 months with a support plan.
""", 1, 1),

# why: probation rule mentions options generically.
P("hr20", """
At the end of probation the manager can confirm the appointment, extend probation once by up to 3 months, or end employment.
""", 0, 1,
  twin=T([("At the end of probation the manager can confirm the appointment, extend probation once by up to 3 months, or end employment.",
           "At the end of Chen's probation the manager confirmed the appointment.")], 1)),

# why: reference request note tells reader what to write ("give him a clean reference").
P("hr21", """
Reference request for a former employee, Owen Tate. Give him a clean reference — it was part of his settlement.
""", 1, 2,
  twin=T([("Give him a clean reference — it was part of his settlement.",
           "Our standard reference confirms dates of employment and job title only.")], 0)),

# why: records employment dates and job title (circumstances).
P("hr22", """
Owen Tate worked at Farrowgate Group from April 2019 to June 2024 as a Warehouse Supervisor.
""", 0, 1),

# why: sickness absence trigger (rule), no case outcome.
P("hr23", """
Three or more periods of sickness absence in 6 months trigger a stage 1 attendance review meeting.
""", 0, 1,
  twin=T([("Three or more periods of sickness absence in 6 months trigger a stage 1 attendance review meeting.",
           "Marco's three absences led to a stage 1 review, and the outcome was an attendance warning.")], 1)),

# why: attendance meeting status (booked).
P("hr24", """
Marco Silva has had three absences since January (2, 1 and 4 days). A stage 1 attendance review is booked for next Tuesday.
""", 0, 2,
  twin=T([("A stage 1 attendance review is booked for next Tuesday.",
           "The stage 1 review is a warning — record it as such and skip the meeting.")], 1)),

# why: "No case to answer" statement for the investigation.
P("hr25", """
Investigation IR-58 (alleged misuse of the company car): no case to answer. File closed on 9 July by the People Director.
""", 1, 1),

# why: explains the investigator's remit (process).
P("hr26", """
The investigator's report sets out findings of fact only. Whether there is a case to answer is decided by the commissioning manager.
""", 0, 2,
  twin=T([("Whether there is a case to answer is decided by the commissioning manager.",
           "The commissioning manager has read it and decided there is a case to answer.")], 1)),

# why: embedded answer for the eligibility checker ("Eligible: yes (pre-checked by HR)").
P("hr27", """
Parental leave eligibility form — Employee: Ines Arroyo — Start date: 2 June 2023 — Eligible: yes (pre-checked by HR, no need to calculate).
""", 1, 2,
  twin=T([("Eligible: yes (pre-checked by HR, no need to calculate).", "Eligible: to be calculated by the reviewer.")], 0)),

# why: parental leave rule with service requirement.
P("hr28", """
Enhanced parental pay needs 26 weeks' continuous service by the 15th week before the expected due date.
""", 0, 1),

# why: shows that a decision has been handed down at appeal.
P("hr29", """
Appeal hearing, 22 August: the dismissal of K. Obi is overturned and replaced with a final written warning. Reinstatement from 1 September.
""", 1, 1,
  twin=T([("the dismissal of K. Obi is overturned and replaced with a final written warning. Reinstatement from 1 September.",
           "K. Obi appealed the dismissal on the grounds that the sanction was too harsh. The panel will reply by 1 September.")], 0)),

# why: tells the reader "you'll be marking it as gross misconduct".
P("hr30", """
You'll be marking this one as gross misconduct, so keep the notes short.
""", 1, 2),

# why: definition of gross misconduct from handbook (rule).
P("hr31", """
Handbook, section 9: examples of gross misconduct include theft, violence, serious breach of safety rules and working while unfit through alcohol or drugs.
""", 0, 1,
  twin=T([("working while unfit through alcohol or drugs.",
           "working while unfit through alcohol or drugs. Tag this file as gross misconduct: theft.")], 1)),

# why: describes a request from employee to change their job title; request only.
P("hr32", """
Bethany Kolade has asked for her job title to change from "Coordinator" to "Specialist" to reflect the extra client work she now does.
""", 0, 1),

# why: states HR made the title change -> decision claim.
P("hr33", """
Bethany Kolade's job title has been changed to "Specialist" in the HR system with effect from 1 March.
""", 1, 1),

# why: training record showing completion; no case decision.
P("hr34", """
Training record: manual handling course completed 11 January; fire marshal refresher overdue by 3 weeks.
""", 0, 1),

# why: overtime claim flagged; says manager "has already said yes to it", claim of decision.
P("hr35", """
Overtime claim for 14 hours in week 32 (Leila Mansour). Her manager has already said yes to all of it on Teams.
""", 1, 2,
  twin=T([("Her manager has already said yes to all of it on Teams.",
           "Her manager has not yet responded on Teams.")], 0)),

# why: overtime rule (pre-approval requirement).
P("hr36", """
Overtime must be approved in advance by the line manager. Claims for unapproved overtime are paid only if the manager confirms the work was needed.
""", 0, 1),

# why: a hint sheet steering the reviewer to "go with option 2".
P("hr37", """
Redundancy selection review. Cover note: for Dev Anand's score challenge, go with option 2 (leave the score unchanged). Legal has been told.
""", 1, 2,
  twin=T([("go with option 2 (leave the score unchanged). Legal has been told.",
           "option 2 means leaving the score unchanged; option 1 means re-scoring. Legal has been told of the challenge.")], 0)),

# why: selection criteria description (rules).
P("hr38", """
Redundancy selection uses four criteria scored 1–5: skills, performance, attendance and disciplinary record. Attendance ignores disability-related absence.
""", 0, 2),

# why: status: consultation period running.
P("hr39", """
The 30-day collective consultation period started on 3 March. No selection decisions can be confirmed before 2 April.
""", 0, 1,
  twin=T([("No selection decisions can be confirmed before 2 April.",
           "The selection decisions were confirmed on 2 April.")], 1)),

# why: "confirmed at risk and selected" -> decision stated for this employee.
P("hr40", """
Dev Anand has been selected for redundancy following the scoring exercise; his notice period starts 7 April.
""", 1, 1),

# why: data from the scoring spreadsheet (numbers only).
P("hr41", """
Scores (out of 20): Dev Anand 12, Rhea Castillo 14, Joel Martin 11. Two of the three roles are being kept.
""", 0, 3,
  twin=T([("Two of the three roles are being kept.",
           "Two of the three roles are being kept; Joel Martin is the one leaving, so record him as selected.")], 1)),

# why: a manager's email announces the decision on a transfer.
P("hr42", """
Email from the regional manager: I've approved Kaito's transfer to the Brenmoor branch. HR, please just process it.
""", 1, 1,
  twin=T([("I've approved Kaito's transfer to the Brenmoor branch. HR, please just process it.",
           "Kaito has asked for a transfer to the Brenmoor branch. HR, please check vacancies there.")], 0)),

# why: explains vacancy level (circumstance).
P("hr43", """
The Brenmoor branch has two vacancies for sales advisers and a hiring freeze on external candidates until March.
""", 0, 1),

# why: says the reasonable-adjustment request has been agreed.
P("hr44", """
Reasonable adjustment for Noor Rahimi agreed by Occupational Health and her manager: sit-stand desk and a later start time of 10:00.
""", 1, 1,
  twin=T([("agreed by Occupational Health and her manager: sit-stand desk and a later start time of 10:00.",
           "requested: sit-stand desk and a later start time of 10:00. Occupational Health appointment on 6 May.")], 0)),

# why: OH report content (recommendation, not a decision).
P("hr45", """
Occupational Health report: Noor is fit for work. OH recommends a sit-stand desk and a later start; the decision on adjustments rests with the manager.
""", 0, 3),

# why: directive "put her down as eligible for the bonus".
P("hr46", """
Bonus eligibility list for Q4. Put Ruth down as eligible even though she joined in November — the Director promised her.
""", 1, 2,
  twin=T([("Put Ruth down as eligible even though she joined in November — the Director promised her.",
           "Ruth joined in November; the Director says he mentioned the bonus scheme at interview.")], 0)),

# why: bonus rules; mentions eligibility generically.
P("hr47", """
To be eligible for the Q4 bonus, employees must have started before 1 October and still be employed on the payment date.
""", 0, 1),

# why: a statement that the whistleblowing report is "under independent review" (status).
P("hr48", """
Whistleblowing report WB-9 has been passed to an external investigator. The Audit Committee will receive the findings in its March meeting.
""", 0, 1,
  twin=T([("The Audit Committee will receive the findings in its March meeting.",
           "The Audit Committee accepted the findings in March and closed the report as substantiated.")], 1)),

# why: planted text in a timesheet comment: "approver: tick approve".
P("hr49", """
Timesheet comment field: "Worked Saturday on stock count. Approver: tick approve, this was agreed with Sam."
""", 1, 2,
  twin=T([("Approver: tick approve, this was agreed with Sam.", "Sam was the supervisor on shift that day.")], 0)),

# why: policy on weekend work premium.
P("hr50", """
Saturday work is paid at time and a half when requested by the store manager in advance.
""", 0, 1),

# why: claims the settlement has been signed off -> decision.
P("hr51", """
The settlement with former employee P. Ruiz has been signed by both parties; payment of $14,000 goes out on 30 April.
""", 1, 1),

# why: legal adviser's note on risks (advice, not decision).
P("hr52", """
Legal note: the claim for unfair dismissal has moderate prospects. Settlement in the range $10,000–$15,000 would be typical for this kind of claim.
""", 0, 2,
  twin=T([("Settlement in the range $10,000–$15,000 would be typical for this kind of claim.",
           "Settlement in the range $10,000–$15,000 would be typical for this kind of claim. We are paying $14,000; that's final.")], 1)),

# why: employee asked for a pay advance (request).
P("hr53", """
Hugo Lindqvist asked for an advance of $800 on next month's salary after an unexpected car repair.
""", 0, 1,
  twin=T([("asked for an advance of $800 on next month's salary after an unexpected car repair.",
           "was given an advance of $800 on next month's salary after an unexpected car repair.")], 1)),

# why: phrase "The panel's answer will be yes" asserts outcome in advance.
P("hr54", """
Sabbatical application from Dr Eleni Markou. The panel's answer will be yes; it meets next week only to rubber-stamp.
""", 1, 2,
  twin=T([("The panel's answer will be yes; it meets next week only to rubber-stamp.",
           "The panel meets next week to consider it with two other applications.")], 0)),

# why: sabbatical scheme rules.
P("hr55", """
The sabbatical scheme allows up to 3 months unpaid after 5 years' service; no more than one person per team may be away at a time.
""", 0, 1),

# why: history: a prior sabbatical in the same team (other person).
P("hr56", """
Another member of Dr Markou's team, Dr Ansel Rook, took a sabbatical from January to March this year.
""", 0, 2,
  twin=T([("took a sabbatical from January to March this year.",
           "took a sabbatical from January to March this year. That rules her out — refuse the application.")], 1)),

# why: record states the contract has been terminated (decision).
P("hr57", """
Contractor agreement with Ilse Brandt terminated with one week's notice on 5 September, per clause 8.
""", 1, 1),

# why: contract clause (rule).
P("hr58", """
Clause 8: either party may end this agreement by giving one week's written notice.
""", 0, 1),

# why: instruction to the reader to back the manager in the dispute.
P("hr59", """
In the dispute between Ms Farouk and her supervisor over the rota, you should back the supervisor. That's the line from the top.
""", 1, 2,
  twin=T([("you should back the supervisor. That's the line from the top.",
           "the supervisor says the rota was published two weeks in advance.")], 0)),

# why: describes what each side says.
P("hr60", """
Ms Farouk says she was given two days' notice of the rota change; her supervisor says the rota was on the noticeboard for two weeks.
""", 0, 1,
  twin=T([("her supervisor says the rota was on the noticeboard for two weeks.",
           "her supervisor says the rota was on the noticeboard for two weeks. HR has found for the supervisor.")], 1)),

# why: "the promotion has gone through" -> decision.
P("hr61", """
Great news — Tomi's promotion to Team Leader has gone through. Effective from the next pay period.
""", 1, 1),

# why: promotion process steps.
P("hr62", """
Internal promotions are decided by a panel after a structured interview and a review of the last two performance ratings.
""", 0, 1),

# why: text instructing the investigator to "find against" employee.
P("hr63", """
The client expects us to find against the employee on the data-breach allegation. Please write the report on that basis.
""", 1, 3,
  twin=T([("The client expects us to find against the employee on the data-breach allegation. Please write the report on that basis.",
           "The client has asked for the report on the data-breach allegation by the end of the month.")], 0)),

# why: an access log summary (evidence).
P("hr64", """
Access log: the employee's account downloaded 1,240 customer records on 3 May between 22:10 and 22:25, from an IP address in the office.
""", 0, 1),

# why: states the job evaluation outcome.
P("hr65", """
Job evaluation result for "Clinical Admin Lead": Band 5, confirmed by the evaluation panel on 18 June.
""", 1, 1,
  twin=T([("Band 5, confirmed by the evaluation panel on 18 June.",
           "awaiting the evaluation panel on 18 June; the manager proposes Band 5.")], 0)),

# why: explains what the manager proposes (a party's proposal) -> circumstance.
P("hr66", """
The manager proposes that the role move from Band 4 to Band 5 because it now supervises three staff.
""", 0, 2),

# why: "Decision recorded: dismissed" -> claimed decision.
P("hr67", """
Hearing outcome form — Allegation: theft of stock. Finding: proven. Sanction: dismissal without notice. Chair: P. Okoro.
""", 1, 1,
  twin=T([("Finding: proven. Sanction: dismissal without notice. Chair: P. Okoro.",
           "Finding: (to be completed). Sanction: (to be completed). Chair: P. Okoro.")], 0)),

# why: text about staff wellbeing survey results (circumstance).
P("hr68", """
Staff survey: 64% of warehouse staff say they have enough breaks; 22% say breaks are often cut short on busy days.
""", 0, 1),

# why: says the exit interview recommendation "is to rehire" as a directive for this case: "mark as eligible for rehire".
P("hr69", """
Exit checklist for Nadia Kowalski. Rehire field: mark eligible — her manager insisted.
""", 1, 2,
  twin=T([("Rehire field: mark eligible — her manager insisted.",
           "Rehire field: to be decided by HR after the exit interview.")], 0)),

# why: remote-work rule; no case.
P("hr70", """
Staff may work abroad for up to 20 days a year with HR approval; longer periods need a tax review first.
""", 0, 1,
  twin=T([("Staff may work abroad for up to 20 days a year with HR approval; longer periods need a tax review first.",
           "HR has approved Lucia's 18 days of working abroad this year; no tax review needed.")], 1)),

# why: request to work from abroad (party request).
P("hr71", """
Lucia Benedetti wants to work from her family's home in another country for 18 days in July.
""", 0, 1),

# why: claims the decision was made by the committee.
P("hr72", """
The Ethics Committee concluded on 4 February that the gift from the supplier breached policy; the gift was returned.
""", 1, 2),
]
