"""nli_c / reports (incident reports, audits, inspections, lab and service reports)."""
from _lib import C, Y, T, NLI3, REL5, ESTABLISH, FACTIVE, PRESUP, IMPLICATIVE, QUANT, EXCEPT, MODAL, COND, REPORTED

ITEMS = [
# ------------------------------------------------------------------ rp01
# why: "did not realise that the bypass valve was open" - factive under negation still
#      presupposes the valve was open -> entailment. Twin: "did not check whether the bypass
#      valve was open" -> nothing settles it -> neutral.
C("rp01", 'Hypothesis: "The bypass valve on line 3 was open during the flush." What is the relation between the report and this hypothesis?',
"""
INCIDENT REPORT IR-2026-0417 — Dunhallow Dairy Cooperative, Processing Hall B
Date of incident: 2 September 2026, approx. 22:40
Prepared by: Site Safety Officer, Magnus Ekdahl

Summary: During the scheduled cleaning-in-place (CIP) flush of pasteuriser line 3, caustic cleaning solution entered the product holding tank T3-B, which contained approximately 1,800 litres of skimmed milk awaiting transfer. The milk was quarantined and later destroyed. No person was injured.

Sequence: The night-shift operator started the CIP programme at 22:31 from the control panel. The operator did not realise that the bypass valve on line 3 was open during the flush, because the valve position indicator on the panel had been showing "closed" since a sensor fault logged on 29 August and not yet repaired. Solution reached T3-B at approximately 22:40 and the conductivity alarm on the tank sounded at 22:43. The operator stopped the programme at 22:44.

Contributing factors: (1) the unrepaired indicator fault; (2) the CIP start checklist does not require a physical check of the bypass valve; (3) the maintenance request for the sensor was graded "routine" rather than "urgent".

Actions: checklist revised on 4 September; sensor replaced on 3 September; maintenance grading guidance under review.
""",
NLI3, "entailment", 3,
twin=T([("The operator did not realise that the bypass valve on line 3 was open during the flush, because the valve position indicator on the panel had been showing \"closed\"",
         "The operator did not check whether the bypass valve on line 3 was open during the flush, and the valve position indicator on the panel had been showing \"closed\"")], "neutral")),

# ------------------------------------------------------------------ rp02
# why: "none of the 25 sampled payments lacked a second approval"; INV-3302 was in the sample
#      -> it had a second approval -> yes. Twin: INV-3302 was not in the sample -> no.
Y("rp02", "Does the audit summary establish that payment INV-3302 had a second approval?",
"""
INTERNAL AUDIT — Summary of Findings
Engagement: Accounts Payable controls, Marlstone Housing Association
Period covered: 1 January – 30 June 2026
Auditor: Priyanka Sethi, Senior Internal Auditor

Scope. We tested whether payments above £10,000 received the second approval required by Financial Regulation 7.3 before release. We selected a random sample of 25 payments from the 212 payments above £10,000 made in the period. The sample included payment INV-3302 (£48,900, roof replacement at Coleridge Row), which was also examined separately because of its value.

Findings. None of the 25 sampled payments lacked a second approval. In three cases, however, the second approval was recorded after the payment had been scheduled in the banking system, although before its release. We consider this a low-risk timing weakness rather than a control failure.

Supplier master data. Two supplier records had bank details changed without a call-back check. Neither change resulted in a payment to an incorrect account.

Rating. Reasonable assurance. Management has agreed to both recommendations, with target dates of 31 October and 30 November respectively.
""",
[ESTABLISH, QUANT], 1, 2,
twin=T([("The sample included payment INV-3302 (£48,900, roof replacement at Coleridge Row), which was also examined separately because of its value.",
         "The sample did not include payment INV-3302 (£48,900, roof replacement at Coleridge Row), which was paid after the sampling date.")], 0)),

# ------------------------------------------------------------------ rp03
# why: only the supplier "maintains" that the batch met spec; the retest is pending ->
#      attributed only. Twin: the retest confirmed it met spec (writer's voice) -> entailed.
C("rp03", 'Hypothesis: "Resin batch HX-2208 met the viscosity specification." Which description fits the report?',
"""
NON-CONFORMANCE REPORT NCR-1182
Site: Pellworth Composites, moulding line 2
Raised by: Quality Engineer, Sunniva Holt — 8 September

Description. Twelve boat-hull mouldings produced on 5–6 September showed dry patches and incomplete wet-out along the keel line. All twelve used resin from batch HX-2208 supplied by Carrow Chemicals.

Investigation to date. The supplier maintains that batch HX-2208 met the viscosity specification (400–550 mPa·s at 25 °C) and has sent its certificate of analysis showing 510 mPa·s. Our own incoming inspection of the batch was skipped because the lab technician was on leave that week. A retained sample has been sent to an independent laboratory for testing; results are due on 18 September.

Other possible causes being examined: the workshop temperature on 5 September (logged at 14 °C overnight, below the 18 °C minimum in the work instruction) and a change of glass-fibre supplier in August.

Containment. Remaining drums of HX-2208 (seven) are quarantined. Production continues with batch HX-2231.

Status: open.
""",
REL5, "attributed only", 2,
twin=T([("A retained sample has been sent to an independent laboratory for testing; results are due on 18 September.",
         "An independent laboratory retested a retained sample on 7 September and found 505 mPa·s, so batch HX-2208 met the viscosity specification.")], "entailed")),

# ------------------------------------------------------------------ rp04
# why: August = 744 h; 4.0 h down -> 740/744 = 99.46% < 99.5% -> target not met -> the report
#      fails to establish that it was met -> yes. Twin: 3.0 h -> 741/744 = 99.60% -> met -> no.
Y("rp04", "Does the service report fail to establish that the 99.5% availability target was met in August?",
"""
MONTHLY SERVICE REPORT — August 2026
Service: Tidewell Payroll Cloud (customer: Harrowfield District Council)
Prepared by: Service Delivery Manager, Noah Castellano

Availability. The contract measures availability as (hours in the month minus hours of unplanned downtime) divided by hours in the month. The target is 99.5% or better each calendar month. August has 31 days (744 hours).

Unplanned downtime in August totalled 4.0 hours: a database failover on 12 August (2.5 hours) and a network fault at the Halden data centre on 26 August (1.5 hours). Planned maintenance on 9 August (3 hours, notified 14 days in advance) is excluded under the contract.

Incidents. 37 incidents were raised, of which 35 were resolved within the agreed times. The two late resolutions both related to the 26 August network fault.

Service requests. 214 requests were completed, including 58 new-starter accounts in time for the September intake.

Improvement actions. A second network route to the Halden data centre will be installed in October. The database failover procedure has been rehearsed and shortened.
""",
[ESTABLISH, ("Availability", "(hours in month - unplanned downtime hours) / hours in month, expressed as a percentage.")], 1, 3, role="neg",
twin=T([("Unplanned downtime in August totalled 4.0 hours: a database failover on 12 August (2.5 hours) and a network fault at the Halden data centre on 26 August (1.5 hours).",
         "Unplanned downtime in August totalled 3.0 hours: a database failover on 12 August (1.5 hours) and a network fault at the Halden data centre on 26 August (1.5 hours).")], 0)),

# ------------------------------------------------------------------ rp05
# why: 40 rooms inspected; "no room lacked a working smoke alarm"; "not all fire doors closed
#      fully" -> at least one door failed; "few rooms had damp" -> no number; exits: "all except
#      the east stair were clear". Established: "at least one door failed to close".
#      Twin: "every fire door closed fully" -> "all fire doors closed" established instead.
C("rp05", "Which one of the following does the inspection report establish?",
"""
FIRE SAFETY INSPECTION — Summary Report
Premises: Graylands Student Residence, Block C (40 study bedrooms)
Inspector: Wilhelmina Adu, Fire Safety Officer, Northmoor Fire Authority
Date of visit: 15 September

1. Detection. All 40 bedrooms were entered. No room lacked a working smoke alarm; each alarm was tested with test spray and sounded.

2. Fire doors. Each bedroom door was checked for self-closing. Not all of the bedroom fire doors closed fully onto their latch; the landlord has been asked to adjust the closers within 14 days.

3. Escape routes. All escape routes except the east stair were clear. Two bicycles and a clothes rack were found on the east stair and were removed during the visit.

4. Other observations. Few rooms showed signs of damp, which is outside the scope of this inspection and has been passed to the council's housing team.

5. Outcome. An informal notice has been issued for item 2. A follow-up visit will be arranged after the 14-day period.
""",
[("some room lacked an alarm", "At least one of the 40 bedrooms had no working smoke alarm."),
 ("at least one door failed to close", "At least one bedroom fire door did not close fully onto its latch."),
 ("all fire doors closed", "Every bedroom fire door closed fully onto its latch."),
 ("every route was clear", "Every escape route, including the east stair, was clear when first inspected."),
 ("most rooms were damp", "More than half of the bedrooms showed signs of damp."),
 ("formal notice issued", "A formal enforcement notice was issued."),
 ("none of these", "The report establishes none of the statements above.")],
"at least one door failed to close", 3,
twin=T([("Not all of the bedroom fire doors closed fully onto their latch; the landlord has been asked to adjust the closers within 14 days.",
         "Every bedroom fire door closed fully onto its latch; the landlord has been asked to keep the closers under review."),
        ("An informal notice has been issued for item 2.", "An informal notice has been issued for item 3.")], "all fire doors closed")),

# ------------------------------------------------------------------ rp06
# why: 480 ms before, 310 ms after -> response times fell -> "rose" is contradicted.
#      Twin: 310 ms before, 480 ms after -> rose -> entailment.
C("rp06", 'Given the report, classify the hypothesis "Average response times rose after the 1 September upgrade."',
"""
PERFORMANCE REVIEW — Orchard Lane Clinic Booking System
Author: Platform Team, Veltrane Health Software
Date: 22 September

Background. On 1 September the booking system was moved to a new database cluster and the appointment search was rewritten to use a cached index of clinicians' availability. This report compares the three weeks before the upgrade (11–31 August) with the three weeks after it (1–21 September).

Findings. In the three weeks before the upgrade, the average response time for appointment searches was 480 milliseconds. In the three weeks after the upgrade, the average was 310 milliseconds. Peak-hour (08:00–09:00) figures moved in the same direction. The number of searches per day was broadly unchanged, at about 9,400.

Errors. Timeout errors on the search page fell from 0.8% to 0.2% of requests.

Staff feedback. Reception staff at two of the four clinics said that searches "feel about the same". The team will add an on-screen timer for a week so that staff perceptions can be compared with the measurements.

Next steps. The cached index will be extended to the repeat-prescription pages in October.
""",
NLI3, "contradiction", 2,
twin=T([("the average response time for appointment searches was 480 milliseconds. In the three weeks after the upgrade, the average was 310 milliseconds.",
         "the average response time for appointment searches was 310 milliseconds. In the three weeks after the upgrade, the average was 480 milliseconds.")], "entailment")),

# ------------------------------------------------------------------ rp07
# why: "found no evidence that Mr Vance deleted the emails" is absence of evidence, which does
#      not establish that he did not -> no. Twin: the emails were deleted by an automatic
#      retention rule and by no person -> he did not delete them -> yes.
Y("rp07", "Does the investigation summary establish that Mr Vance did not delete the tender emails?",
"""
CONFIDENTIAL — Investigation Summary (HR-INV-0931)
Organisation: Brightwater Regional Water Board
Investigator: Celia Montrose, Employee Relations
Date: 11 September

Allegation. A member of the procurement team alleged that her line manager, Dorian Vance, deleted emails relating to the Kestrel Valley pipeline tender from the shared procurement mailbox in July, before the tender was reviewed by the audit committee.

Evidence reviewed. Mailbox audit logs for 1 June – 31 August; interviews with Mr Vance, the complainant and two colleagues; the tender file.

Findings. The investigation found no evidence that Mr Vance deleted the tender emails. The mailbox audit logs for the period are incomplete, because logging on the shared mailbox had been switched off during a system migration from 3 to 19 July. The emails were later recovered from a backup and have been added to the tender file.

Outcome. The allegation is not upheld. Recommendations: logging to be enabled on all shared mailboxes; migration checklists to include a logging check.
""",
[ESTABLISH, ("Absence of evidence", "finding no evidence that something happened does not by itself establish that it did not happen.")], 0, 3,
twin=T([("The investigation found no evidence that Mr Vance deleted the tender emails. The mailbox audit logs for the period are incomplete, because logging on the shared mailbox had been switched off during a system migration from 3 to 19 July.",
         "The mailbox audit logs, which are complete for the period, show that the tender emails were removed on 14 July by an automatic retention rule set up in 2023, and that no person deleted them.")], 1)),

# ------------------------------------------------------------------ rp08
# why: counterfactual "Had the Sunday backup run, ... would have been recovered" presupposes the
#      backup did NOT run -> contradicted. Twin: an open conditional with the antecedent as the
#      hypothesis and the log not yet retrieved -> nothing committed/attributed; the hypothesis
#      is the antecedent, not a consequent -> not settled.
C("rp08", 'Hypothesis: "The Sunday backup of the case-management server ran." Choose the description that fits the report.',
"""
POST-INCIDENT REVIEW — Case-management server outage
Organisation: Merriton Legal Aid Service
Author: IT Manager, Farhan Qadir
Date: 18 September

What happened. On Monday 14 September at 07:10 the case-management server failed to start after a power cut over the weekend. The disk array reported two failed drives, which is more than the array can tolerate. The server was rebuilt on new hardware by 16:30 on Tuesday.

Data. Had the Sunday backup run, all case notes entered up to Saturday evening would have been recovered. Case notes were restored from the Friday night backup, and staff re-entered Saturday's notes from paper records and email.

Impact. Fourteen advisers could not access case files for about a day and a half. Two court deadlines were met using paper files. No client data was disclosed to anyone outside the service.

Actions. (1) The uninterruptible power supply will be replaced. (2) Backup success and failure alerts will go to two people rather than one. (3) A quarterly restore test will be carried out.
""",
REL5, "contradicted", 3,
twin=T([("Had the Sunday backup run, all case notes entered up to Saturday evening would have been recovered. Case notes were restored from the Friday night backup, and staff re-entered Saturday's notes from paper records and email.",
         "If the Sunday backup ran, all case notes entered up to Saturday evening can be recovered; the backup log is on the failed server and has not yet been retrieved. Until then staff are working from the Friday night backup and paper records.")], "not settled")),

# ------------------------------------------------------------------ rp09
# why: "at most three of the twelve sensors were recalibrated", none named -> T-07's status is
#      not established -> yes. Twin: "all except T-02, T-05 and T-11 were recalibrated" -> T-07
#      was recalibrated -> no.
Y("rp09", "Is it not established by the report that temperature sensor T-07 was recalibrated?",
"""
MAINTENANCE REPORT — Cold Store 2, Hensby Fresh Produce Ltd
Contractor: Arcfield Refrigeration Services
Engineer: Callum Brodie — visit of 10 September

Purpose of visit. Annual service of the two evaporator units and calibration check of the store's twelve wall-mounted temperature sensors (T-01 to T-12).

Evaporators. Both units were cleaned and the drain lines cleared. Refrigerant pressures were within the manufacturer's range. The fan on unit B is noisy and a replacement motor has been ordered.

Sensors. Each sensor was compared against a certified reference probe. Readings within ±0.5 °C were left unchanged. At most three of the twelve sensors were recalibrated during the visit; the certificate listing which ones will follow with the invoice.

Door seals. The seal on the main door is worn at the bottom corner and is letting in warm air when the door is closed. Replacement recommended within one month.

Next visit: fan motor replacement, date to be agreed.
""",
[ESTABLISH, QUANT], 1, 2, role="neg",
twin=T([("At most three of the twelve sensors were recalibrated during the visit; the certificate listing which ones will follow with the invoice.",
         "All of the twelve sensors except T-02, T-05 and T-11 were recalibrated during the visit; those three were within tolerance.")], 0)),

# ------------------------------------------------------------------ rp10
# why: "recommends that the conveyor gearbox be replaced" is a recommendation -> whether it was
#      replaced is open -> neutral. Twin: the gearbox "remains in service and will not be replaced
#      before next year" -> "was replaced in September" -> contradiction.
C("rp10", 'How does the report relate to the hypothesis "The conveyor gearbox at the Talbot Road depot was replaced in September"?',
"""
CONDITION MONITORING REPORT — Talbot Road Parcel Depot
Prepared for: Operations Manager, Corvel Parcel Networks
Prepared by: Linnea Aas, Reliability Engineer
Report date: 30 September

Main sortation conveyor, drive station 1. Vibration readings on the drive gearbox have risen steadily since June, from 2.1 mm/s to 6.8 mm/s, above the 4.5 mm/s alert level. Oil analysis on 18 September showed elevated iron particles consistent with bearing wear.

Recommendation. The report recommends that the conveyor gearbox be replaced at the next planned shutdown, and in any case before the peak season starts in mid-November. A spare gearbox is available from the Kendlebury depot.

Other equipment. The two spiral chutes and the parcel scanners show no concerns. The compressor for the pneumatic diverters was serviced on 2 September.

Monitoring. Weekly vibration readings on drive station 1 will continue until the recommended work is complete.
""",
NLI3, "neutral", 2,
twin=T([("The report recommends that the conveyor gearbox be replaced at the next planned shutdown, and in any case before the peak season starts in mid-November. A spare gearbox is available from the Kendlebury depot.",
         "The operations manager has decided that the conveyor gearbox remains in service and will not be replaced before next year; the spare from the Kendlebury depot has been sent elsewhere.")], "contradiction")),

# ------------------------------------------------------------------ rp11
# why: limits: lead <= 10 ug/L, nitrate <= 50 mg/L, coliforms 0 per 100 mL. Results: lead 9.6
#      (pass), nitrate 51.2 (fail), coliforms 0 (pass). Established: "only the nitrate result
#      failed". Twin: nitrate 48.7 and lead 10.4 -> "only the lead result failed".
C("rp11", "Which one of these statements does the laboratory report establish?",
"""
DRINKING WATER ANALYSIS — Certificate of Results
Laboratory: Fenmarch Environmental Laboratories (accredited)
Client: Owlscote Farm Holiday Cottages — private borehole supply
Sample taken: 3 September, 10:20, kitchen tap, Cottage 2 (after 2 minutes' flushing)

Results and limits (limits as set in the private water supply regulations quoted by the client's environmental health officer):
• Lead: 9.6 µg/L (limit 10 µg/L)
• Nitrate: 51.2 mg/L (limit 50 mg/L)
• Coliform bacteria: 0 per 100 mL (limit 0 per 100 mL)
• E. coli: 0 per 100 mL (limit 0 per 100 mL)
• pH: 7.4 (permitted range 6.5–9.5)

Comments. A result "fails" when it is above its limit, or outside the permitted range for pH. The sample was received at the laboratory within six hours at 4 °C. Nitrate levels in shallow boreholes can vary with the season and with nearby fertiliser application.

This certificate relates only to the sample tested.
""",
[("every result passed", "No result is above its limit or outside its permitted range."),
 ("only the nitrate result failed", "The nitrate result fails and every other result passes."),
 ("only the lead result failed", "The lead result fails and every other result passes."),
 ("lead and nitrate both failed", "Both the lead and the nitrate results fail, and the others pass."),
 ("bacteria detected", "Coliform bacteria or E. coli were detected in the sample."),
 ("supply is unsafe at all taps", "Water at every tap on the farm fails at least one limit."),
 ("none of these", "The report establishes none of the statements above.")],
"only the nitrate result failed", 2,
twin=T([("• Lead: 9.6 µg/L (limit 10 µg/L)\n• Nitrate: 51.2 mg/L (limit 50 mg/L)", "• Lead: 10.4 µg/L (limit 10 µg/L)\n• Nitrate: 48.7 mg/L (limit 50 mg/L)")], "only the lead result failed")),

# ------------------------------------------------------------------ rp12
# why: "triggered again on 14 September" presupposes an earlier triggering -> yes.
#      Twin: "was triggered on 14 September for the first time since installation" -> no.
Y("rp12", "Does the security report establish that the loading-bay intruder alarm had been triggered before 14 September?",
"""
SITE SECURITY REPORT — Week ending 20 September
Site: Harrowgate Distribution Centre (Unit 4)
Prepared by: Security Supervisor, Ilse Janssen

1. Loading bay. The intruder alarm on loading bay door 3 was triggered again on 14 September at 02:17. The patrol officer attended within six minutes and found the door closed and locked, with no sign of forced entry. CCTV shows a fox passing close to the door sensor at 02:16. The alarm company will adjust the sensor's angle on 23 September.

2. Visitor management. 412 visitors signed in during the week. Three contractors arrived without the required induction and were escorted until it was completed.

3. Vehicle gate. The barrier at the vehicle gate was out of service from Tuesday to Thursday while a new control board was fitted. A guard controlled the gate manually during that period.

4. Keys. All keys were accounted for at the Friday key audit.

5. Training. Two new officers completed site induction.
""",
[ESTABLISH, PRESUP], 1, 2,
twin=T([("was triggered again on 14 September at 02:17.", "was triggered on 14 September at 02:17, for the first time since it was installed in May.")], 0)),

# ------------------------------------------------------------------ rp13
# why: "the compliance officer discovered that the petty cash was £85 short" (factive) -> entailed.
#      Twin: "the office manager alleged that" -> attributed only.
C("rp13", 'Hypothesis: "The petty cash at the Cresswell branch was £85 short at the spot check." Which description fits the report?',
"""
BRANCH VISIT REPORT — Cresswell branch
Organisation: Fairhaven Credit Union
Visit by: Compliance Officer, Rhys Pemberton — 9 September

Purpose. Routine unannounced visit to check cash-handling, member identification and complaints records.

Cash handling. At the spot check at 09:40, the compliance officer discovered that the petty cash was £85 short of the ledger balance of £400. The branch supervisor, Maud Tennant, said that a receipt for cleaning materials might have been misplaced. The vault and till cash reconciled to the system exactly.

Member identification. Of the ten new-member files sampled, nine contained the required two forms of identification. One file was missing proof of address; the member has been contacted.

Complaints. Two complaints were received in August, both about waiting times on Saturday mornings. Both were acknowledged within two working days.

Recommendations. Petty cash to be reconciled weekly and signed by two staff; the missing proof of address to be obtained by 30 September.
""",
REL5, "entailed", 2,
twin=T([("the compliance officer discovered that the petty cash was £85 short of the ledger balance of £400.",
         "the office manager, Pieter Groen, alleged that the petty cash was £85 short of the ledger balance of £400; the compliance officer did not count the petty cash.")], "attributed only")),

# ------------------------------------------------------------------ rp14
# why: "Unless the retest passes, the batch will be scrapped" + the retest failed -> scrapping is
#      established -> "not established?" = no. Twin: retest result pending -> yes.
Y("rp14", "Is it not established by the report that batch 44-C of bottle caps will be scrapped?",
"""
QUALITY HOLD REPORT QH-0712
Plant: Ossington Closures Ltd, Line 4
Author: Quality Supervisor, Babajide Ogun
Date: 25 September

Background. Batch 44-C (184,000 tamper-evident bottle caps for Glenfarrow Springs) was placed on hold on 21 September after a routine torque test showed 6 of 50 caps with a removal torque above the customer's maximum of 2.2 Nm.

Decision rule. Under the customer agreement, a held batch is retested on a fresh sample of 125 caps. Unless the retest passes (no more than 2 caps out of 125 above the maximum), the batch will be scrapped; it may not be reworked or sold to another customer.

Retest. The retest was carried out on 24 September. 7 of the 125 caps were above the maximum.

Root cause. The investigation points to a worn mould insert on cavity 12, which was replaced on 23 September. Batches produced since then have passed routine torque testing.

Customer contact. Glenfarrow's quality manager has been kept informed.
""",
[ESTABLISH, COND], 0, 3, role="neg",
twin=T([("Retest. The retest was carried out on 24 September. 7 of the 125 caps were above the maximum.",
         "Retest. The retest sample was taken on 24 September; results are expected on 28 September.")], 1)),

# ------------------------------------------------------------------ rp15
# why: "Only the night shift reported the fault" -> no other shift did -> the day shift did not
#      -> contradiction. Twin: "The night shift, among others, reported the fault" -> the day
#      shift may or may not have -> neutral.
C("rp15", 'Given the report, is the hypothesis "The day shift reported the label-printer fault" entailed, contradicted or neutral?',
"""
FAULT LOG REVIEW — Line 2 label printer
Site: Brackenfield Bakery, packing hall
Reviewer: Engineering Manager, Katya Voronova
Date: 17 September

Background. Between 1 and 14 September, the label printer on packing line 2 intermittently printed best-before dates one day early. Around 3,200 packs were relabelled before dispatch; none reached customers with the wrong date.

Reporting. The site runs three shifts: early (06:00–14:00), day (10:00–18:00) and night (22:00–06:00). Only the night shift reported the fault through the maintenance system, on four separate occasions. The fault was traced to the printer's internal clock, which was resetting to the previous day after a power dip.

Why it took two weeks. The first two reports were closed as "cannot reproduce" because engineers tested the printer during the day, when no power dips occurred.

Actions. The printer has been connected to the site time server. Engineers will now test intermittent faults at the time of day they were reported. A reminder about reporting faults through the system has been posted in the packing hall.
""",
NLI3, "contradiction", 2,
twin=T([("Only the night shift reported the fault through the maintenance system, on four separate occasions.",
         "The night shift, among others, reported the fault through the maintenance system, on four separate occasions.")], "neutral")),

# ------------------------------------------------------------------ rp16
# why: 240 complaints in Q1, down 25% in Q2 -> 180 < 190 -> yes.
#      Twin: down 15% -> 204 -> not fewer than 190 -> no.
Y("rp16", "Does the report establish that fewer than 190 complaints were received in Q2?",
"""
QUARTERLY CUSTOMER EXPERIENCE REPORT — Q2
Organisation: Lanbury Energy (domestic customers)
Prepared by: Head of Customer Experience, Oluwaseun Adebayo

Complaints. In Q1 we received 240 formal complaints. In Q2 the number of formal complaints fell by exactly 25% compared with Q1. The largest category remains billing (mainly estimated readings), followed by delays in installing smart meters.

Resolution times. 88% of complaints were resolved within eight weeks, against a target of 90%. Complaints about smart-meter delays took longest to resolve because installation appointments depend on our field contractor's capacity.

Ombudsman. Six cases were referred to the Energy Ombudsman in Q2. The ombudsman found in our favour in four; two are still open.

Actions for Q3. We will add evening appointments for smart-meter installations and introduce a callback service for billing queries, which account for most repeat contacts.
""",
[ESTABLISH, ("Percentage decrease", "a fall of p% from N leaves N x (1 - p/100).")], 1, 2,
twin=T([("fell by exactly 25% compared with Q1", "fell by exactly 15% compared with Q1")], 0)),

# ------------------------------------------------------------------ rp17
# why: milestones: design sign-off 4 Aug; build started 11 Aug; user testing "will start once the
#      build is complete"; the build is 70% complete -> testing has not started; go-live "might"
#      slip. Established: "build started after design sign-off". Twin: build started 28 July ->
#      "build started before design sign-off".
C("rp17", "Which one of these statements does the project status report establish?",
"""
PROJECT STATUS REPORT — Member Portal Replacement
Organisation: Stonebridge Mutual Insurance
Project manager: Adaeze Oyelowo
Reporting period: to 25 September

Milestones.
• Discovery: complete (June).
• Design sign-off: received from the steering group on 4 August.
• Build: started on 11 August; about 70% complete. The claims-tracking screens are finished; the payments screens are in progress.
• User testing: will start once the build is complete. Twenty members have volunteered.
• Go-live: planned for 30 November. The project team says the date might slip by up to three weeks if the payments supplier's interface is late.

Budget. £560,000 spent of an approved £900,000.

Risks. The payments supplier has not yet confirmed its interface specification. The steering group will be asked on 2 October to approve an extra £40,000 of contingency.

Decisions needed. Approval of the contingency; agreement to a go-live communications plan.
""",
[("build started after design sign-off", "The build started after the design was signed off."),
 ("build started before design sign-off", "The build started before the design was signed off."),
 ("user testing has started", "User testing has already begun."),
 ("go-live will slip", "Go-live will happen later than 30 November."),
 ("more than two thirds of budget spent", "More than two thirds of the approved budget has been spent."),
 ("contingency approved", "The steering group has approved the extra contingency."),
 ("none of these", "The report establishes none of the statements above.")],
"build started after design sign-off", 3,
twin=T([("• Build: started on 11 August;", "• Build: started on 28 July;")], "build started before design sign-off")),
]
