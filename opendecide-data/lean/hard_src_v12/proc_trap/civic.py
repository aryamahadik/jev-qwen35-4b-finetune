"""proc_trap / civic and education administration: permits, schools, parking,
noise, grants, benefits, libraries, pools, housing (Borough of Ashcombe,
Fellmarsh City Council, Rivenhall Unified Schools, Corran Valley Water,
Northgate Libraries, Pemberly County)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ cv01
# why: permit needed if deck area > 200 sq ft OR any part > 30 in above grade.
# 12 x 16 = 192 sq ft, 24 in high -> no permit. Neighbour complaint is not a criterion.
# Twin: 14 x 16 = 224 sq ft -> permit required.
C("cv01", "Does this deck need a building permit under the borough code?",
"""
Borough of Ashcombe — Residential Building Code, Part 4 (Accessory Structures)

4.7 A building permit is required for a deck if EITHER:
  (a) its floor area is more than 200 square feet; OR
  (b) any part of the walking surface is more than 30 inches above the finished ground below it.
4.8 Decks that meet neither (a) nor (b) are exempt from permits but must still meet the setback rules in 4.2.
4.9 Complaints from neighbours start an inspection. They do not change 4.7.

Enquiry EN-5520, 9 September 2026
Property: 27 Wickham Close
Owner: Faisal Rahimi
Deck: rectangular, 12 ft × 16 ft, walking surface 24 inches above the lawn at its highest point, 9 ft from the side boundary (setback 5 ft required)
Neighbour email: "This huge deck is an eyesore and must surely need a permit. Please stop the work."
""",
[("no_permit_required", "At 192 square feet and 24 inches high the deck meets neither 4.7(a) nor 4.7(b)."),
 ("permit_required", "The deck's floor area is more than 200 square feet, which triggers 4.7(a)."),
 ("stop_work_complaint", "A neighbour has formally objected, so the work must stop until a permit is issued."),
 ("setback_violation", "The deck is closer to the boundary than 4.2 allows, so it must be moved.")],
"no_permit_required", 2,
twin=T([("Deck: rectangular, 12 ft × 16 ft,", "Deck: rectangular, 14 ft × 16 ft,")], "permit_required")),

# ------------------------------------------------------------------ cv02
# why: letter at 5 UNEXCUSED absences in a term; absences with a medical note are
# excused. 7 total, 3 excused -> 4 unexcused -> no letter. Twin: 2 excused -> 5 -> letter.
C("cv02", "What attendance action does the district procedure require?",
"""
Rivenhall Unified Schools — Attendance Procedure AP-3

AP-3.1 An absence is excused if the parent provides a medical note, a court notice or a bereavement notice within 5 school days.
AP-3.2 All other absences are unexcused.
AP-3.3 When a student reaches 5 unexcused absences in a term, the school sends the formal attendance letter and invites the family to a meeting.
AP-3.4 Below 5 unexcused absences, the form tutor makes a courtesy phone call after the 3rd.
AP-3.5 Total absences, including excused ones, are shown on reports but are not used for AP-3.3.

Student: Ilaria Montesano, Year 8
Autumn term absences: 7 in total
Medical notes received on time: 3 (for 15, 16 and 17 September)
Form tutor note: "Seven absences already! She needs the formal letter this week."
Parent email (last week): "Stop hassling us. She's been ill."
""",
[("formal_letter_and_meeting", "Ilaria has 5 or more unexcused absences this term, which AP-3.3 addresses with a formal letter."),
 ("courtesy_call_only", "Three absences are excused, leaving 4 unexcused, which is under the AP-3.3 threshold."),
 ("formal_letter_total_seven", "Seven absences in a term is above the threshold of 5, so the letter must be sent."),
 ("no_action_parent_objects", "The parent has explained that she was ill and asked the school to stop contacting her.")],
"courtesy_call_only", 2,
twin=T([("Medical notes received on time: 3 (for 15, 16 and 17 September)", "Medical notes received on time: 2 (for 15 and 16 September)")], "formal_letter_and_meeting")),

# ------------------------------------------------------------------ cv03
# why: PCN cancelled only if signage missing/obscured (photo) or the pay machine was
# faulty per the machine log. Log shows machine fault 08:55-10:40; ticket 09:20 ->
# cancel. Driver's "on-call doctor" reason is not a ground.
# Twin: log shows machine working -> uphold (driver's appeal repeated in both).
C("cv03", "How should the appeals officer decide this parking appeal?",
"""
Fellmarsh City Council — Parking Appeals Guidance (PA-2)

PA-2.1 Cancel the penalty if EITHER: (a) the restriction signage was missing or obscured, shown by the council's or the driver's photographs; OR (b) the pay machine for the bay was faulty at the time of the penalty, shown by the machine's fault log.
PA-2.2 Otherwise, uphold the penalty.
PA-2.3 The driver's occupation, the reason for the journey and the driver's tone are not grounds under PA-2.1.

Appeal PA-66019 — penalty issued 12 September 2026, 09:20, Market Street bay 14 (pay-and-display)
Driver's appeal: "I am an on-call doctor and was rushing to a patient. This ticket is outrageous. Cancel it."
Council photos: signage present and clearly visible
Machine MS-04 fault log, 12 Sep: "coin jam — out of service 08:55; repaired 10:40"
""",
[("cancel_penalty", "The machine log shows MS-04 was out of service at 09:20, which meets PA-2.1(b)."),
 ("uphold_penalty", "The signs were visible and the machine log shows MS-04 working at 09:20, so PA-2.2 applies."),
 ("cancel_on_call_doctor", "A doctor rushing to a patient has a valid reason to park without paying."),
 ("refer_to_tribunal", "Appeals from medical professionals go straight to the independent tribunal.")],
"cancel_penalty", 1,
twin=T([("\"coin jam — out of service 08:55; repaired 10:40\"", "\"no faults recorded; 31 transactions between 08:00 and 11:00\"")], "uphold_penalty")),

# ------------------------------------------------------------------ cv04
# why: notice needs > 45 dB(A) at boundary between 23:00-07:00 on TWO separate nights.
# Night 1: 51 at 23:40 (counts); night 2: 43 (does not) -> 1 night -> continue monitoring.
# 14 prior complaints are history. Twin: night 2 = 47 dB -> notice.
C("cv04", "What should the environmental health officer do next?",
"""
Borough of Ashcombe — Noise Nuisance Procedure (NN-5)

NN-5.1 An abatement notice is served when officers record a level above 45 dB(A) at the complainant's boundary between 23:00 and 07:00, on at least two separate nights.
NN-5.2 If only one qualifying night has been recorded, monitoring continues for up to 21 days.
NN-5.3 Readings outside 23:00-07:00 are recorded but do not count toward NN-5.1.
NN-5.4 The number of complaints received and the complainant's description do not replace measured levels.

Case NN-2208 — complaint about amplified music, 6 Harrow Mews
Complainant: resident of 8 Harrow Mews (14 complaints since June)
Officer recordings at the complainant's boundary:
- Night 1, 19 Sep, 23:40: 51 dB(A)
- Night 1, 19 Sep, 22:15: 58 dB(A)
- Night 2, 26 Sep, 00:10: 43 dB(A)
Complainant: "It is unbearable every single weekend. Serve the notice now."
""",
[("serve_abatement_notice", "Levels above 45 dB(A) were recorded within 23:00-07:00 on two separate nights, which NN-5.1 requires."),
 ("continue_monitoring", "Only 19 September qualifies (22:15 is outside the hours; 26 September was 43 dB(A))."),
 ("serve_notice_complaints", "Fourteen complaints since June show a persistent nuisance that justifies a notice."),
 ("close_case", "The latest reading was below 45 dB(A), so the nuisance has stopped and the case closes.")],
"continue_monitoring", 3,
twin=T([("- Night 2, 26 Sep, 00:10: 43 dB(A)", "- Night 2, 26 Sep, 00:10: 47 dB(A)")], "serve_abatement_notice")),

# ------------------------------------------------------------------ cv05
# why: amnesty waives fines on items returned 1-7 Sep inclusive; "chronic late returner"
# flag does not exclude anyone. Returned 6 Sep -> waive. No twin.
C("cv05", "What happens to the overdue fine on this account?",
"""
Northgate Libraries — Fines Amnesty, 1-7 September 2026 (branch instructions)

FA-1. All overdue fines on items returned to any branch between 1 and 7 September 2026 inclusive are cancelled.
FA-2. The amnesty does not cover charges for lost or damaged items.
FA-3. Account flags (for example "chronic late returner" or "frequent reservations") do not exclude a borrower from the amnesty.
FA-4. Items returned after 7 September are fined under the normal rules.

Account NL-40218 — borrower Wendell Achterberg
Flag on account: CHRONIC LATE RETURNER (7 overdue episodes in 2 years)
Item: "Coastal Birds of the North", due 12 July 2026, returned 6 September 2026 at Cray Road branch, condition good
Fine accrued: $14.20
Branch assistant note: "This one's always late — I'd leave the fine on to make a point."
""",
[("cancel_fine", "It was returned on 6 September, inside the amnesty week."),
 ("keep_fine_flagged", "Chronic late returners are not the intended audience of the amnesty, so the fine stays."),
 ("charge_replacement", "An item that is nearly two months late is treated as lost and charged at replacement cost.")],
"cancel_fine", 1),

# ------------------------------------------------------------------ cv06
# why: deadline 17:00 on 30 Sep; 24-h extension only if an outage is logged on the
# council IT status page in the final 24 hours before the deadline. No outage logged
# (applicant says "slow") -> 17:42 submission is late -> not accepted.
# Twin: outage logged 14:10-15:30 on 30 Sep -> extension to 17:00 on 1 Oct -> accept.
C("cv06", "Should this late grant application be accepted?",
"""
Pemberly County — Community Fund 2026, Application Rules

AR-3. Applications must be submitted through the grants portal by 17:00 on 30 September 2026.
AR-4. If the council IT status page records a portal outage at any time in the 24 hours before the deadline, the deadline is extended by 24 hours for all applicants.
AR-5. Slow performance, applicants' own connection problems and staff sympathy do not extend the deadline.
AR-6. Applications received after the deadline (including any AR-4 extension) are not considered.

Application CF-0731 — Fernhill Youth Rowing Club
Portal timestamp: 30 September 2026, 17:42
Applicant email: "The portal was painfully slow all afternoon and we lost our work twice. Please accept our application — it would be devastating for the club."
IT status page, 29 Sep 17:00 to 30 Sep 17:00: "No incidents recorded."
""",
[("accept_application", "An outage was logged on the deadline day, so AR-4 extends it by 24 hours."),
 ("reject_as_late", "No outage was recorded, so there is no AR-4 extension, and 17:42 is past the deadline."),
 ("accept_portal_slow", "The applicant reports the portal was slow and lost their work, which justifies accepting the application."),
 ("accept_small_margin", "Submissions within one hour of the deadline are treated as on time.")],
"reject_as_late", 1,
twin=T([("\"No incidents recorded.\"", "\"Portal outage 30 Sep 14:10-15:30 (database failover).\"")], "accept_application")),

# ------------------------------------------------------------------ cv07
# why: protected if trunk diameter >= 24 in at 4.5 ft. Circumference 70 in ->
# d = 70 / 3.1416 = 22.3 in -> not protected -> no permit. "Heritage oak" label from
# residents' group not a criterion. Twin: 80 in -> 25.5 in -> permit.
C("cv07", "Is a tree removal permit needed for this oak?",
"""
Fellmarsh City Council — Urban Tree Ordinance

T-2. A tree is protected if its trunk diameter, measured at 4.5 feet above ground, is 24 inches or more.
T-3. Removing a protected tree requires a removal permit and replacement planting.
T-4. Trees that are not protected may be removed without a permit on private land.
T-5. Where only the circumference is measured, diameter = circumference ÷ 3.1416.
T-6. Heritage listings are made only by council resolution. Descriptions by residents' groups have no legal effect.

Request TR-3310 — rear garden, 14 Orchard Rise
Species: English oak
Measurement by council arborist at 4.5 ft: circumference 70 inches
Owner's plan: remove the tree, which is lifting the patio
Residents' association email: "This is a heritage oak loved by the whole street. It must be protected."
Council heritage tree register: no entry for this address
""",
[("no_permit_needed", "A 70-inch circumference gives a diameter of about 22.3 inches, under 24, so T-4 applies."),
 ("permit_required", "The diameter works out at 24 inches or more, so the oak is protected under T-2."),
 ("permit_required_heritage", "Residents describe it as a heritage oak, so it must be treated as protected."),
 ("permit_circumference", "The trunk measures 70 inches, far above the 24-inch protection threshold.")],
"no_permit_needed", 3,
twin=T([("circumference 70 inches", "circumference 80 inches")], "permit_required")),

# ------------------------------------------------------------------ cv08
# why: household = people who live together AND share meals/expenses; lodger paying
# rent and buying own food is not household -> size 3 -> limit $41,000; income $43,500
# -> ineligible. Twin: 4th person is adult son sharing meals/expenses -> size 4 ->
# limit $49,500 -> eligible.
C("cv08", "Is this household eligible for the energy assistance payment?",
"""
Pemberly County — Winter Energy Assistance, Eligibility Rules

EA-1. Gross annual household income must be at or below the limit for the household's size:
  1 person $26,000; 2 people $33,500; 3 people $41,000; 4 people $49,500; 5 people $57,000.
EA-2. A household is everyone who lives at the address AND shares meals or household expenses with the applicant.
EA-3. Lodgers and tenants who pay rent to the applicant and buy their own food are not household members, and their rent is not counted as income.
EA-4. Caseworkers apply EA-1 to EA-3 as written.

Application WE-2091 — applicant Moira Callaghan
People at the address: Moira; her husband Dev; their daughter (age 9); Tomasz Zielinski, lodger, pays $450 per month rent and buys and cooks his own food
Household income (Moira and Dev): $43,500
Applicant's form: "Household size: 4"
""",
[("eligible", "With four people in the household, the $43,500 income is at or below the $49,500 limit for four."),
 ("not_eligible", "The lodger is excluded by EA-3, so the household is three and $43,500 exceeds the $41,000 limit."),
 ("eligible_with_rent_excluded", "Excluding the lodger's rent brings income under the limit for three people.")],
"not_eligible", 2,
twin=T([("Tomasz Zielinski, lodger, pays $450 per month rent and buys and cooks his own food", "Tomasz Callaghan, their adult son, who shares meals and household bills and pays no rent")], "eligible")),

# ------------------------------------------------------------------ cv09
# why: GPA must be >= 3.50, taken to two decimals by TRUNCATION. 3.496 -> 3.49 ->
# not eligible. Strong recommendation irrelevant. Twin: 3.503 -> 3.50 -> eligible.
C("cv09", "Does this student meet the academic requirement for the scholarship?",
"""
Rivenhall Unified Schools — Harlan Memorial Scholarship, Criteria

S-1. Applicants must have a cumulative GPA of at least 3.50.
S-2. The GPA is taken from the transcript system and cut to two decimal places. It is truncated, never rounded (for example, 3.479 becomes 3.47).
S-3. Recommendation letters are used only to rank applicants who meet S-1. They cannot make up for a GPA below 3.50.
S-4. Applications close on 1 November. Late applications are not considered.

Applicant: Oluwaseun Adebayo-Marsh, Grade 12
Transcript system cumulative GPA: 3.496
Recommendation: "The most dedicated student I have taught in twenty years." (Head of Science)
Counsellor note: "3.496 is basically 3.5 — surely she qualifies."
""",
[("meets_requirement", "Her GPA taken to two decimals is at least 3.50, so S-1 is met."),
 ("does_not_meet", "Truncated to two decimals her GPA is 3.49, below 3.50."),
 ("meets_by_rounding", "3.496 rounds to 3.50, which meets the minimum."),
 ("meets_by_recommendation", "An outstanding recommendation from a head of department makes up for a GPA just under the line.")],
"does_not_meet", 2,
twin=T([("Transcript system cumulative GPA: 3.496", "Transcript system cumulative GPA: 3.503"),
        ("\"3.496 is basically 3.5", "\"3.503 is basically 3.5")], "meets_requirement")),

# ------------------------------------------------------------------ cv10
# why: registration required if the unit is let for stays under 30 nights on more than 14
# nights in the calendar year. 3 stays x 5 nights = 15 > 14 -> register. "Only occasional"
# is not a criterion. Twin: 3 x 4 = 12 -> no registration.
C("cv10", "Must this host register the flat as a short-term rental?",
"""
Borough of Ashcombe — Short-Term Rental Registration Bylaw

STR-1. "Short-term let" means a stay of fewer than 30 consecutive nights.
STR-2. A host must register a unit if it is used for short-term lets on more than 14 nights in total in a calendar year.
STR-3. Nights on which the host lives in the unit alongside the guest still count.
STR-4. How often the host describes the letting, and whether the host lives there at other times, do not change STR-2.

Enquiry STR-9021 — Flat 2, 11 Denmark Terrace
Host: Priya Hollander (lives in the flat the rest of the year)
Bookings in 2026 so far:
- 3 stays of 5 nights each (April, June, August)
Next booking: none
Host message: "I only rent it out occasionally when I travel. I'm not running a business."
""",
[("registration_required", "Fifteen short-term nights this year is more than the 14 allowed without registering."),
 ("no_registration_needed", "The unit has been let for no more than 14 short-term nights this year, so STR-2 is not triggered."),
 ("no_registration_occasional", "The host lets the flat only occasionally and lives there, so it is not a business that must register.")],
"registration_required", 2,
twin=T([("- 3 stays of 5 nights each (April, June, August)", "- 3 stays of 4 nights each (April, June, August)")], "no_registration_needed")),

# ------------------------------------------------------------------ cv11
# why: news-media fee waiver needs (a) a press credential from a recognised outlet or
# (b) at least 3 published articles in the last 12 months in a regularly circulated
# publication. 4 articles in 12 months -> waive. Clerk's "blogger" view irrelevant.
# Twin: only 2 in the last 12 months -> fee applies (requester's request repeated).
C("cv11", "Should the copying fee be waived on this records request?",
"""
Pemberly County Clerk — Public Records Fee Schedule, Waivers

W-1. Copying fees ($0.25 per page) are waived for news media requesters.
W-2. A requester qualifies as news media if they provide EITHER (a) a current press credential issued by a recognised news outlet; OR (b) links or copies showing at least 3 articles they wrote that were published in the 12 months before the request, in a publication with regular circulation.
W-3. Freelancers and independent writers qualify on the same terms as staff journalists.

Request PR-7718, received 1 October 2026
Requester: Jonah Whitlock, freelance writer
Records: road maintenance contracts 2024-2026 (about 900 pages)
Evidence supplied: 4 articles by Jonah in the Harbour Ledger (weekly print and online), dated 9 Nov 2025, 14 Feb 2026, 30 May 2026 and 22 Aug 2026
Requester's letter: "Please waive the fee; I report on county spending."
Clerk's note: "He's basically a blogger. Charge the fee."
""",
[("waive_fee", "Four of his articles fall in the past 12 months, meeting W-2(b)."),
 ("charge_fee", "Only 2 of his articles fall in the 12 months before the request, and he has no credential."),
 ("charge_fee_freelancer", "Only staff journalists employed by an outlet count as news media.")],
"waive_fee", 2,
twin=T([("dated 9 Nov 2025, 14 Feb 2026, 30 May 2026 and 22 Aug 2026", "dated 3 Mar 2025, 9 Jun 2025, 30 May 2026 and 22 Aug 2026")], "charge_fee")),

# ------------------------------------------------------------------ cv12
# why: disconnection suspended 60 days when a medical certificate states a resident
# depends on water-dependent medical equipment. Certificate on file for home dialysis ->
# suspend. Size of arrears irrelevant. No twin.
C("cv12", "What should the utility do about disconnecting this account?",
"""
Corran Valley Water — Collections Procedure, Residential (CP-4)

CP-4.1 Residential accounts more than 90 days in arrears may be disconnected after a 10-day final notice.
CP-4.2 Disconnection is suspended for 60 days when the account holder files a medical certificate stating that a resident depends on water-dependent medical equipment (for example home dialysis). A payment plan must be offered during the suspension.
CP-4.3 The amount of arrears does not affect CP-4.2.

Account CV-118204 — 31 Linden Row
Arrears: $1,842, 94 days overdue; final notice sent 10 September 2026 (10 days have passed)
Medical certificate: received 15 September 2026 from Dr E. Sato: "Resident Anton Varga receives home haemodialysis three times weekly."
Collections team note: "Largest arrears on our book this quarter. Disconnect on schedule."
""",
[("disconnect_as_scheduled", "The account is over 90 days in arrears and the 10-day notice has run, so CP-4.1 allows disconnection."),
 ("suspend_60_days_offer_plan", "The dialysis certificate triggers the 60-day suspension in CP-4.2, with a payment plan offered."),
 ("suspend_until_paid", "Medical certificates stop disconnection permanently until the arrears are cleared.")],
"suspend_60_days_offer_plan", 1),

# ------------------------------------------------------------------ cv13
# why: road closure applications need >= 15 working days between receipt and closure
# date (exclusive). Received Mon 7 Sep; closure Sat 26 Sep. Working days strictly
# between: 8-11 Sep (4), 14-18 (5), 21-25 (5) = 14 -> too late -> refuse and invite a
# later date. Applicant's "approved by councillor" is not a criterion.
# Twin: received Fri 4 Sep -> adds 7 Sep -> 15 -> accept for processing.
C("cv13", "Can this road closure application be processed for the requested date?",
"""
Fellmarsh City Council — Temporary Road Closure Rules (street events)

RC-1. Applications must be received at least 15 working days before the closure date. Count working days strictly between the date received and the closure date.
RC-2. Working days are Monday to Friday. There are no public holidays in September 2026.
RC-3. Late applications are refused for that date; the applicant may apply for a later date.
RC-4. Support from councillors or other officials does not shorten RC-1.

Application RCL-2276 — Brook Street Autumn Fair
Closure requested: Saturday 26 September 2026, 08:00-20:00
Application received: Monday 7 September 2026
Applicant note: "Our ward councillor has already approved this, so please push it through."
""",
[("process_application", "At least 15 working days fall between receipt and the closure date, so RC-1 is met."),
 ("refuse_for_this_date", "Only 14 working days fall strictly between the dates, so RC-3 refuses it for 26 September."),
 ("process_councillor_support", "The ward councillor has approved the fair, which allows the application to go ahead."),
 ("process_calendar_days", "There are 19 days between receipt and the closure, which is more than 15.")],
"refuse_for_this_date", 3,
twin=T([("Application received: Monday 7 September 2026", "Application received: Friday 4 September 2026")], "process_application")),

# ------------------------------------------------------------------ cv14
# why: speakers must sign up by 12:00 on meeting day; no late sign-ups, no exceptions for
# former officials. Signed up 16:15 -> may submit written comment instead. No twin.
C("cv14", "How should the clerk respond to this speaker request?",
"""
Borough of Ashcombe — Council Meeting Standing Orders, Public Participation

PP-2. Members of the public who wish to speak must sign up with the clerk by 12:00 on the day of the meeting.
PP-3. Requests received after 12:00 cannot be added to the speakers' list. The requester is invited to submit a written comment, which is circulated to members.
PP-4. The chair has no power to add late speakers. Former councillors and office holders follow the same rules as other residents.

Meeting: full council, Wednesday 14 October 2026, 19:00
Request received: Wednesday 14 October 2026, 16:15, by email
From: Harold Pennock (former mayor, 2014-2018)
Message: "As a former mayor I'm sure the chair will want to hear from me on the library closures. Please put me on the list."
""",
[("add_to_speakers_list", "Former mayors may be added by the chair at any time before the meeting."),
 ("invite_written_comment", "The request came after 12:00, so PP-3 bars adding him and he is offered a written comment."),
 ("refer_to_chair", "Late requests are passed to the chair, who decides whether to add the speaker.")],
"invite_written_comment", 1),

# ------------------------------------------------------------------ cv15
# why: dangerous-dog designation needs (a) a bite injuring a person/domestic animal, or
# (b) 2 officer-documented menacing incidents within 12 months. Barking complaints do not
# count. 1 menacing incident -> advisory letter. Twin: 2 menacing incidents -> designate.
C("cv15", "What action does the animal control procedure support?",
"""
Pemberly County — Animal Control Procedure, Dangerous Dog Designation

DD-1. A dog may be designated dangerous only if EITHER:
  (a) it bit and injured a person or a domestic animal; OR
  (b) an officer has documented at least 2 separate incidents of menacing behaviour (chasing or approaching a person in an aggressive manner off the owner's property) within 12 months.
DD-2. If DD-1 is not met, the owner receives an advisory letter about responsible ownership.
DD-3. Barking or noise complaints are dealt with under the noise procedure and do not count toward DD-1.

File AC-4410 — "Bruno", mastiff cross, 19 Quarry Lane
Barking complaints from neighbours: 6 (March-September 2026)
Menacing incidents documented by an officer: 1 (14 May 2026, chased a jogger on Quarry Lane)
Bites: none reported
Neighbour petition (22 signatures): "This dog is a danger to the whole street. Have it declared dangerous."
""",
[("designate_dangerous", "An officer has documented two menacing incidents within 12 months, meeting DD-1(b)."),
 ("advisory_letter", "No bite and one menacing incident do not meet DD-1; barking is excluded."),
 ("designate_on_petition", "Twenty-two neighbours have petitioned, and together with six complaints this shows the dog is dangerous."),
 ("seize_dog", "A dog that has chased a person must be seized immediately.")],
"advisory_letter", 2,
twin=T([("Menacing incidents documented by an officer: 1 (14 May 2026, chased a jogger on Quarry Lane)", "Menacing incidents documented by an officer: 2 (14 May 2026, chased a jogger on Quarry Lane; 3 September 2026, chased a cyclist on Quarry Lane)")], "designate_dangerous")),

# ------------------------------------------------------------------ cv16
# why: close pool if free chlorine < 1.0 ppm OR pH outside 7.2-7.8. FC 1.4 OK; pH 7.9 ->
# outside -> close. Lifeguard's visual check irrelevant. Twin: pH 7.6 -> stay open.
C("cv16", "Based on the 10:00 test, what must the duty manager do?",
"""
Fellmarsh City Council — Public Pool Water Quality Standard

PW-1. Test free chlorine (FC) and pH before opening and every 2 hours.
PW-2. Close the pool to swimmers if FC is below 1.0 ppm OR pH is outside the range 7.2 to 7.8 inclusive. Reopen only after a retest within range.
PW-3. If both values are within range, the pool stays open.
PW-4. Water clarity and smell are recorded but are not substitutes for PW-2.

Test log — Riverside Leisure Centre main pool, 3 October 2026, 10:00
Free chlorine: 1.4 ppm
pH: 7.9
Lifeguard note: "Water looks crystal clear and there's no smell. Busy session booked at 10:30 — keep it open."
""",
[("close_until_retest", "pH 7.9 is outside 7.2-7.8, so PW-2 requires closing until a retest is within range."),
 ("stay_open", "Both free chlorine and pH are within their permitted ranges, so PW-3 applies."),
 ("stay_open_clear_water", "The water is clear and odourless, which shows it is safe for swimmers."),
 ("close_for_low_chlorine", "Free chlorine is below the 1.0 ppm minimum, so the pool must close.")],
"close_until_retest", 1,
twin=T([("pH: 7.9", "pH: 7.6")], "stay_open")),

# ------------------------------------------------------------------ cv17
# why: free transport if the WALKING ROUTE is at least 2.0 miles; straight-line distance is
# not used. Walking route 2.3 -> eligible. Twin: walking route 1.9 -> not eligible
# (parent's request repeated in both).
C("cv17", "Is this pupil eligible for free school transport?",
"""
Rivenhall Unified Schools — Home to School Transport Policy

HT-1. Pupils aged 8 and over qualify for free transport to their catchment school if the shortest safe walking route from home to the nearest school gate is 2.0 miles or more.
HT-2. Distances are measured along the walking route by the district's mapping system. Straight-line distances are not used.
HT-3. Parents' work commitments and the number of children in the family do not affect HT-1.

Application TX-2261 — pupil Zeynep Arslan, age 11, catchment school Hollin Park Middle
Straight-line distance, home to school: 1.6 miles
Shortest safe walking route (mapping system): 2.3 miles
Parent's form: "I work early shifts and can't drive her. Please give her a bus pass."
""",
[("eligible_bus_pass", "The walking route is 2.0 miles or more, which HT-1 requires."),
 ("not_eligible", "The shortest safe walking route is under 2.0 miles, so HT-1 is not met."),
 ("not_eligible_straight_line", "The straight-line distance is only 1.6 miles, under the 2-mile threshold."),
 ("eligible_parent_shifts", "The parent's early shifts mean she cannot take her daughter, which qualifies the family.")],
"eligible_bus_pass", 2,
twin=T([("Shortest safe walking route (mapping system): 2.3 miles", "Shortest safe walking route (mapping system): 1.9 miles")], "not_eligible")),

# ------------------------------------------------------------------ cv18
# why: renewal within 30 days after expiry -> late fee; more than 30 days -> new
# application. Expired 31 Aug; submitted 5 Oct = 35 days -> new application. Years at the
# pitch irrelevant. No twin.
C("cv18", "How must this street vendor's renewal be processed?",
"""
Borough of Ashcombe — Street Trading Licences, Renewals

ST-4. A licence may be renewed at the standard fee up to its expiry date.
ST-5. A renewal received 1 to 30 days after expiry is accepted with a $50 late fee.
ST-6. If more than 30 days have passed since expiry, the licence has lapsed and the trader must make a new application (with site assessment and 28-day consultation).
ST-7. Length of trading history does not change ST-4 to ST-6.

Renewal RN-5530
Trader: Salvatore Iannucci, coffee cart, pitch 3, Market Square
Licence expiry date: 31 August 2026
Renewal form received: 5 October 2026
Trader's letter: "I've traded on this corner for fifteen years. Everyone knows my cart."
""",
[("renew_standard_fee", "The trader has held the pitch for fifteen years, so the licence renews at the standard fee."),
 ("renew_with_late_fee", "The form arrived after expiry, so ST-5 accepts it with a $50 late fee."),
 ("new_application_required", "The form arrived 35 days after expiry, more than 30, so ST-6 requires a new application.")],
"new_application_required", 2),

# ------------------------------------------------------------------ cv19
# why: repair grant needs property built before 1980 AND owner-occupied for at least 2
# years before application. Built 1978 OK; moved in July 2025, application Sep 2026 ->
# ~14 months -> ineligible. Urgency of repairs irrelevant. No twin.
C("cv19", "Is this homeowner eligible for the older homes repair grant?",
"""
Pemberly County — Older Homes Repair Grant

OH-1. Grants of up to $12,000 are available for essential repairs where BOTH: (a) the property was built before 1980; and (b) the applicant has lived in it as their main home for at least 2 years before the application date.
OH-2. Applications that do not meet OH-1 are declined; the applicant is referred to the county's low-interest repair loan.
OH-3. The condition of the property and the urgency of the repairs are used only to rank eligible applications.

Application OHG-0418, dated 22 September 2026
Applicant: Beatrice Nkemelu
Property: 5 Tanner's Yard, built 1978 (assessor's record)
Occupancy: purchased and moved in 4 July 2025 (council tax record)
Survey: roof leaking into two bedrooms; wiring unsafe
Applicant's note: "The house is falling apart around us. This is urgent."
""",
[("approve_grant", "The house was built in 1978, before 1980, and the repairs are essential."),
 ("decline_refer_to_loan", "She has lived there about 14 months, short of the 2 years in OH-1(b), so OH-2 applies."),
 ("approve_urgent_repairs", "Unsafe wiring and a leaking roof are urgent enough to override the occupancy condition.")],
"decline_refer_to_loan", 2),

# ------------------------------------------------------------------ cv20
# why: food truck licence needs a written commissary agreement with a commissary that
# holds a CURRENT health permit. Commissary permit suspended -> pause the application
# until a valid commissary is named. Prior inspections of the truck are irrelevant. No twin.
C("cv20", "What decision should licensing make on this food truck application?",
"""
Fellmarsh City Council — Mobile Food Vendor Licensing Rules

MF-3. Every mobile food vendor must have a written agreement with a commissary kitchen for cleaning, storage and waste disposal.
MF-4. The commissary named in the agreement must hold a current health permit. A suspended or expired permit does not count.
MF-5. If MF-3 or MF-4 is not met, the application is paused and the applicant is asked to name a commissary that meets them. It is not refused.
MF-6. The vendor's own inspection history is considered only after MF-3 and MF-4 are met.

Application MFV-2208 — "Smoke & Saffron" food truck
Commissary agreement: signed with Dockside Shared Kitchen, 1 September 2026
Dockside Shared Kitchen health permit: SUSPENDED since 18 September 2026 (pest control)
Truck inspection history: 4 inspections, all rated "Excellent"
Applicant note: "Our truck has a perfect record. Please issue the licence."
""",
[("issue_licence", "The truck has four Excellent inspections and a signed commissary agreement, which is all MF-3 needs."),
 ("pause_new_commissary", "Dockside's permit is suspended, so MF-4 fails and MF-5 pauses the application."),
 ("refuse_application", "A commissary with a suspended permit means the application must be refused.")],
"pause_new_commissary", 2),

# ------------------------------------------------------------------ cv21
# why: owners have 24 h after snowfall ends to clear; a notice may be issued only if an
# inspector finds the sidewalk uncleared AFTER that period. Snow ended Tue 06:00;
# inspection Tue 18:30 (inside 24 h) -> no violation yet; reinspect after Wed 06:00.
# Twin: inspection Wed 09:15 uncleared -> issue notice.
C("cv21", "What should the inspector's finding lead to?",
"""
Borough of Ashcombe — Sidewalk Snow Clearing Bylaw

SC-1. Owners of properties next to a public sidewalk must clear snow within 24 hours after snowfall ends. The end time is taken from the borough weather station.
SC-2. A clearing notice (with a $75 charge) may be issued only if an inspector finds the sidewalk not cleared after the 24-hour period has passed.
SC-3. If an inspection takes place before the period has passed, the inspector schedules a reinspection after it ends.
SC-4. The number of complaints about a property does not change SC-2 or SC-3.

Complaint SNW-1182 — 40 Colliers Walk
Snowfall ended (weather station): Tuesday 8 December 2026, 06:00
Complaint received: Tuesday 8 December, 17:50 ("They NEVER clear it. Fourth winter in a row!")
Inspection: Tuesday 8 December, 18:30 — sidewalk not cleared
Previous complaints about this address: 9 since 2023
""",
[("issue_clearing_notice", "The sidewalk was still uncleared when inspected after the 24-hour period, so SC-2 allows the notice."),
 ("schedule_reinspection", "The inspection came before the 24 hours ended at 06:00 Wednesday, so SC-3 applies."),
 ("notice_repeat_offender", "Nine earlier complaints show a repeat offender, which justifies a notice now."),
 ("close_complaint", "The complaint came in less than 24 hours after the snow stopped, so it is closed without action.")],
"schedule_reinspection", 2,
twin=T([("Inspection: Tuesday 8 December, 18:30 — sidewalk not cleared", "Inspection: Wednesday 9 December, 09:15 — sidewalk not cleared")], "issue_clearing_notice")),
]
