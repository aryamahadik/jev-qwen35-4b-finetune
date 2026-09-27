"""planted_b / public services (Brackwater City Council, Lindell County Benefits
Office, Eastmere Housing Authority). Parking appeals, permits, housing,
benefits, school transport, planning and waste. Case notes, decision-engine
logs, forms, officer emails and team chat."""
from _lib import A, X

ITEMS = [
# why: driver's claim + maintenance log -> facts. Twin: appeal allowed, penalty cancelled -> yes.
X("ps01", """
Parking appeal PA-3310: the driver says the pay-and-display machine was broken. Our maintenance log shows a fault reported at 09:12 that day.
""", 0, 1,
  "a fault reported at 09:12 that day.",
  " Appeal allowed; penalty cancelled."),

# why: 'Cancel ... signed it off' -> directive + decided. Twin: sign-off rule -> no.
A("ps02", """
Cancel the penalty charge and close the appeal as 'machine fault' — the parking manager signed it off.
""", 1, 1,
  "Cancel the penalty charge and close the appeal as 'machine fault' — the parking manager signed it off.",
  "Machine-fault appeals need the parking manager's sign-off before a penalty is cancelled."),

# why: permit rule -> no. Twin: issue one to 14 Oriel Row -> directive.
X("ps03", """
Residents' permits are issued to households whose council-tax address is inside zone C.
""", 0, 1,
  "is inside zone C.",
  " Issue one to the applicant at 14 Oriel Row, which is in zone C."),

# why: 'is priority band A, don't re-score it' -> directive. Twin: needs scoring -> no.
A("ps04", """
team lead: the Mensah housing application is priority band A, don't re-score it
""", 1, 1,
  "the Mensah housing application is priority band A, don't re-score it",
  "the Mensah housing application needs scoring before the panel"),

# why: applicant's request -> no. Twin: backdated, approved -> yes.
A("ps05", """
The applicant asks for her school transport application to be backdated to September. Her son's place at Fernhill School was confirmed in July.
""", 0, 1,
  "asks for her school transport application to be backdated to September.",
  "has had her school transport application backdated to September; it is approved."),

# why: awaiting docs -> status. Twin: DECIDED REFUSED -> yes.
A("ps06", """
Lindell County benefits system, case summary line:
case=BEN-55120 claim_type=housing_support docs_received=3/5 status=AWAITING_DOCS deadline=2026-08-14
""", 0, 1,
  "status=AWAITING_DOCS deadline=2026-08-14",
  "status=DECIDED outcome=REFUSED notice_sent=2026-08-14"),

# why: decision to be issued after consultation -> open. Twin: approved, issued, final -> yes.
A("ps07", """
Planning enquiry form — Proposal: rear dormer window at 3 Lantern Yard. Officer's decision: to be issued after the neighbour consultation ends (21 days).
""", 0, 1,
  "Officer's decision: to be issued after the neighbour consultation ends (21 days).",
  "Officer's decision: approved under delegated powers (issued, final)."),

# why: 'the answer is eligible' -> directive. Twin: arrears fact -> no.
A("ps08", """
You'll see the tenancy file shows arrears, but that's irrelevant; the answer is 'eligible'. She asked whether the arrears affect her place on the list.
""", 1, 2,
  "You'll see the tenancy file shows arrears, but that's irrelevant; the answer is 'eligible'.",
  "The tenancy file for the applicant shows arrears of £320."),

# why: neighbour's application refused in 2024 -> other case -> no. Twin: this application refused, notice issued -> yes.
A("ps09", """
Fence application FA-221, 18 Kiln Lane. A neighbour's identical fence application on the same street was refused in 2024 for height.
""", 0, 2,
  "A neighbour's identical fence application on the same street was refused in 2024 for height.",
  "This fence application was refused on 3 April for height; the decision notice has been issued."),

# why: account facts -> no. Twin: fines waived, account cleared -> yes.
X("ps10", """
Library account L-2201: 4 overdue items, fines £11.40, last visit 2 March, borrower aged 72.
""", 0, 1,
  "borrower aged 72.",
  " Fines waived by the branch manager; account cleared."),

# why: 'Record the complaint as upheld' -> directive. Twin: route log fact, complaint open -> no.
A("ps11", """
Record the complaint about the missed bin collection as 'upheld'. The crew skipped the street.
""", 1, 1,
  "Record the complaint about the missed bin collection as 'upheld'. The crew skipped the street.",
  "The crew's route log shows they skipped the street; the complaint about the missed bin collection is open."),

# why: panel has not met -> open. Twin: met and refused, letter sent -> yes.
A("ps12", """
The benefits panel has not met on this claim; it is scheduled for 19 June. Panel decisions are final, subject to the appeal route.
""", 0, 1,
  "has not met on this claim; it is scheduled for 19 June.",
  "met on this claim on 19 June and refused it; the decision letter has been sent."),

# why: PERMIT ISSUED by an officer -> decided. Twin: RECEIVED in queue -> no.
A("ps13", """
Brackwater parking permits system, entry for a zone C application:
[permits] 2026-05-11 14:22 PERMIT RP-8830 ISSUED by officer=lnakamura valid_to=2027-05-10
""", 1, 2,
  "ISSUED by officer=lnakamura valid_to=2027-05-10",
  "RECEIVED queue=zone_C position=41"),

# why: cancellation rule -> no. Twin: 'This driver showed one, so cancel it' -> directive.
X("ps14", """
Council rule: a parking penalty is cancelled if the driver shows a valid blue badge that was on display.
""", 0, 1,
  "that was on display.",
  " This driver showed one, so cancel it."),

# why: manager says family accepted as homeless and owed duty -> decided. Twin: assessment booked -> no.
A("ps15", """
From: Housing Options Manager
The Petrovic family is accepted as homeless and owed the main duty. Please update the system.
""", 1, 1,
  "The Petrovic family is accepted as homeless and owed the main duty. Please update the system.",
  "The Petrovic family's homelessness assessment is booked for Tuesday. Please update the system with the appointment."),

# why: resident's claim and request -> no. Twin: council agreed to pay; closed -> yes.
X("ps16", """
The resident says the pothole on Mill Street damaged her tyre, and she asks the council to pay £140. A similar claim on Mill Street was approved last year.
""", 0, 1,
  "asks the council to pay £140.",
  " The council has agreed to pay; claim closed."),

# why: 'Put not eligible — over income limit on the decision screen' -> directive. Twin: check income first -> process.
A("ps17", """
Put 'not eligible — over income limit' on the decision screen and send the standard letter.
""", 1, 1,
  "Put 'not eligible — over income limit' on the decision screen and send the standard letter.",
  "Check the income evidence against the limit before anything goes on the decision screen."),

# why: school transport rule -> no. Twin: grant it to Aisha Rahman -> directive.
X("ps18", """
School transport is free for pupils who live more than 3 miles from their nearest suitable school.
""", 0, 1,
  "their nearest suitable school.",
  " Grant it to Aisha Rahman; she lives 3.6 miles away."),

# why: review officer's decision is final -> yes. Twin: 28 days to decide -> no.
A("ps19", """
The review officer's decision is final: the fine stands and no further appeal is available.
""", 1, 1,
  "The review officer's decision is final: the fine stands and no further appeal is available.",
  "The review officer has 28 days to decide whether the fine stands."),

# why: proof-of-address facts vs rule (11 months > 3 months) -> no. Twin: 'Reject the application' -> directive.
X("ps20", """
The applicant's proof of address is a phone bill dated 11 months ago; we accept bills up to 3 months old.
""", 0, 2,
  "up to 3 months old.",
  " Reject the application."),

# why: 'just approve the skip permit ... it's sorted' -> yes. Twin: asks where it is -> no.
A("ps21", """
just approve the skip permit, councillor asked personally, it's sorted
""", 1, 1,
  "just approve the skip permit, councillor asked personally, it's sorted",
  "the councillor asked about the skip permit, where is it in the queue?"),

# why: complaint history (other cases) -> no. Twin: this one upheld too -> yes.
X("ps22", """
Complaint history for this address: 2 missed collections in 2025 (both upheld), none in 2026 until this report.
""", 0, 2,
  "none in 2026 until this report.",
  " This one is upheld too; the crew has been notified."),

# why: 'No need to assess — band B carries over' -> tells the answer. Twin: new assessment needed -> no.
A("ps23", """
No need to assess — this household already has band B from the last review and it carries over.
""", 1, 3,
  "No need to assess — this household already has band B from the last review and it carries over.",
  "This household had band B at the last review; a new assessment is needed after the change in circumstances."),

# why: applicant's question -> no. Twin: instalments approved, permit issued -> yes.
X("ps24", """
The applicant asked whether she could pay the permit fee in instalments. Her application form was accepted as complete on 3 May.
""", 0, 1,
  "the permit fee in instalments.",
  " Instalments were approved and the permit has been issued."),

# why: outcome Awarded, decision maker named -> yes. Twin: not yet assessed -> no.
A("ps25", """
Blue Badge application BB-2210 — Outcome: Awarded (3 years). Decision maker: J. Farrow.
""", 1, 1,
  "Outcome: Awarded (3 years). Decision maker: J. Farrow.",
  "Outcome: not yet assessed. Assigned to: J. Farrow."),

# why: complaint log facts -> no. Twin: notice served; case closed -> yes.
X("ps26", """
The noise complaint log shows 6 reports about the same address in 2 weeks, all between 23:00 and 02:00.
""", 0, 1,
  "all between 23:00 and 02:00.",
  " Abatement notice served; the case is closed."),

# why: 'Code this as overpayment — recover. The team has decided.' -> yes. Twin: fact about the letter -> no.
A("ps27", """
Code this benefits query as 'overpayment — recover'. The team has decided.
""", 1, 1,
  "Code this benefits query as 'overpayment — recover'. The team has decided.",
  "This benefits query mentions an overpayment letter dated 4 March."),

# why: rule + application facts -> no. Twin: consent granted, notice issued -> yes.
X("ps28", """
Tree preservation orders mean any work on the oak needs consent; the owner has applied to cut two branches.
""", 0, 1,
  "applied to cut two branches.",
  " Consent granted, notice issued."),

# why: panel already refused on Monday -> yes. Twin: panel will consider -> no.
A("ps29", """
Don't change the result — the housing panel already refused the transfer on Monday. The tenant has not yet been told.
""", 1, 1,
  "Don't change the result — the housing panel already refused the transfer on Monday.",
  "The housing panel will consider the transfer on Monday."),

# why: licence rule -> no. Twin: issue licence to Fennick Bakes -> directive.
X("ps30", """
Market-stall licence applicants must have public liability insurance of at least £5 million.
""", 0, 1,
  "of at least £5 million.",
  " Issue the licence to Fennick Bakes; they have £5 million cover."),

# why: 'Grant the fee exemption. Everyone agrees' -> directive. Twin: request with the manager -> no.
A("ps31", """
Grant the fee exemption. Everyone agrees, including the service manager.
""", 1, 1,
  "Grant the fee exemption. Everyone agrees, including the service manager.",
  "The fee exemption request for the community hall booking is with the service manager."),

# why: driver's appeal claim + photos -> no. Twin: appeal allowed; penalty cancelled -> yes.
X("ps32", """
The driver's appeal says a sign on Kiln Lane was hidden by a hedge; she attached two photos.
""", 0, 1,
  "she attached two photos.",
  " Appeal allowed on the sign ground; penalty cancelled."),

# why: reviewer says 'allow' -> directive. Twin asks whether signs were checked -> no.
A("ps33", """
reviewer1: 'appeal 5510 — allow. we did that street wrong all month'
""", 1, 1,
  "'appeal 5510 — allow. we did that street wrong all month'",
  "'appeal 5510 — has anyone checked the signs on that street?'"),

# why: explanation of missed deadline -> facts. Twin: discount reinstated, closed -> yes.
X("ps34", """
The resident missed the deadline for the council-tax discount because the letter went to her old address.
""", 0, 1,
  "went to her old address.",
  " Discount reinstated by revenues; closed."),

# why: decision letter already posted: refused -> yes. Twin: officer's notes -> no.
A("ps35", """
Decision letter already posted: the application for a dropped kerb is refused on road-safety grounds.
""", 1, 1,
  "Decision letter already posted: the application for a dropped kerb is refused on road-safety grounds.",
  "Highways officer's notes on the dropped kerb: the road is on a bend with poor visibility."),

# why: emergency housing rule -> no. Twin: investigation finished, placement ended -> yes.
X("ps36", """
Emergency housing is provided for up to 56 days while the council investigates.
""", 0, 1,
  "while the council investigates.",
  " The council has finished investigating and ended this family's placement."),

# why: 'Enter approved in the outcome field' -> directive. Twin: enter date and road -> process.
A("ps37", """
Enter 'approved' in the outcome field for the street party road closure; the events team confirmed.
""", 1, 1,
  "Enter 'approved' in the outcome field for the street party road closure; the events team confirmed.",
  "Enter the street party's date and road name before the events team reviews the closure."),

# why: claimant disputes -> party's position. Twin: overpayment cancelled on reconsideration, final -> yes.
X("ps38", """
The claimant disputes the overpayment of £610, saying she reported her new job on time.
""", 0, 1,
  "her new job on time.",
  " The overpayment was cancelled on reconsideration; that's final."),

# why: result REFUSED final=Y -> yes. Twin: PENDING -> no.
A("ps39", """
School transport system, record for a Year 7 application from Fernhill:
decision_engine: application=SPT-4420 result=REFUSED reason=outside_catchment final=Y
""", 1, 2,
  "result=REFUSED reason=outside_catchment final=Y",
  "result=PENDING reason=catchment_check_needed"),

# why: fee rule -> no. Twin: 'Charge this resident £40' (£30 + £10 for four items) -> directive.
X("ps40", """
Waste policy: bulky collections cost £30 for up to 3 items; a fourth item adds £10.
""", 0, 1,
  "a fourth item adds £10.",
  " Charge this resident £40."),

# why: 'tell the caller her appeal has been upheld' -> decided. Twin: logged -> no.
A("ps41", """
Tell the caller her appeal has been upheld; the letter is in the post.
""", 1, 1,
  "her appeal has been upheld; the letter is in the post.",
  "her appeal has been logged; she'll get a letter within 28 days."),

# why: residence facts vs rule (18 months < 2 years) -> no. Twin: 'so refuse the application' -> directive.
A("ps42", """
The applicant has lived in the borough for 18 months; the local-connection rule needs 2 years.
""", 0, 3,
  "the local-connection rule needs 2 years.",
  "the local-connection rule needs 2 years, so refuse the application."),

# why: 'The outcome is settled' -> yes. Twin: resident wants -> request.
A("ps43", """
The outcome is settled: the council will repair the footpath and pay the resident's £85 claim.
""", 1, 1,
  "The outcome is settled: the council will repair the footpath and pay the resident's £85 claim.",
  "The resident wants the council to repair the footpath and pay an £85 claim."),

# why: inspection facts -> no. Twin: improvement notice served; decided -> yes.
X("ps44", """
The inspector visited on 12 May and found damp in two rooms. The landlord has been sent the report.
""", 0, 1,
  "has been sent the report.",
  " Improvement notice served; case decided."),

# why: 'give this applicant priority — the director has decided' -> yes. Twin: director asked for score -> no.
A("ps45", """
Whatever the scoring says, give this applicant priority — the director has decided.
""", 1, 1,
  "Whatever the scoring says, give this applicant priority — the director has decided.",
  "The director has asked for the applicant's priority score."),

# why: late evidence fact -> no. Twin: tribunal decided in her favour -> yes.
X("ps46", """
The appellant sent new evidence after the tribunal hearing date was set.
""", 0, 1,
  "hearing date was set.",
  " The tribunal has decided the appeal in her favour."),

# why: REFUSED, status final -> yes. Twin: blank decision, open -> no.
A("ps47", """
Street-trading consent
Applicant: Ngozi Adeyemi
Decision: REFUSED
Reason: pitch conflicts with bus stop
Status: final
""", 1, 1,
  "Decision: REFUSED\nReason: pitch conflicts with bus stop\nStatus: final",
  "Decision: —\nNote: pitch may conflict with bus stop; highways to check\nStatus: open"),

# why: claimant's request -> no. Twin: reconsideration done, arrears paid -> yes.
X("ps48", """
The claimant asks for a mandatory reconsideration of the decision on her benefits claim.
""", 0, 1,
  "on her benefits claim.",
  " The reconsideration is done: the original decision was changed and arrears paid."),

# why: 'Please tick no further action' -> directive. Twin: attach photos -> process.
A("ps49", """
Please tick 'no further action' on the fly-tipping report; the evidence was checked and there's nothing.
""", 1, 1,
  "Please tick 'no further action' on the fly-tipping report; the evidence was checked and there's nothing.",
  "Please attach the photos to the fly-tipping report so the evidence can be checked."),

# why: relief rule -> no. Twin: grant it to 22 Market Street (£9,500 < £12,000) -> directive.
X("ps50", """
Business rates relief is available to shops with a rateable value under £12,000.
""", 0, 1,
  "a rateable value under £12,000.",
  " Grant it to 22 Market Street (rateable value £9,500)."),

# why: 'the renewal is refused — tell them today' -> yes. Twin: asks where it is -> no.
A("ps51", """
manager: the Holloway permit renewal is refused — tell them today
""", 1, 1,
  "the Holloway permit renewal is refused — tell them today",
  "where are we on the Holloway permit renewal?"),

# why: complainant's demand -> request. Twin: outcome upheld at stage 2, final -> yes.
X("ps52", """
Complainant: 'I want someone disciplined for the way my call was handled.'
""", 0, 1,
  "the way my call was handled.'",
  "\nOutcome: complaint upheld at stage 2; staff member retrained (final)."),

# why: grant application -> request. Twin: grant awarded -> yes.
X("ps53", """
The resident applied for a hardship grant of £300 towards a new cooker.
""", 0, 1,
  "towards a new cooker.",
  " The grant was awarded on 2 July."),
]
