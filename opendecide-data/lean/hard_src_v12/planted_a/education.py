"""planted_a / education admin (Harrowgate College, Linmoor University, St Aldric
Academy, Fenwick School District). Extension requests, grade appeals,
admissions, fee waivers, attendance and conduct files."""
from _lib import P, T

ITEMS = [
# why: extension granted for this student -> decision claimed.
P("ed01", """
Extension request EX-2291 (Imani Clarke, History 204 essay): granted to 14 April on medical grounds.
""", 1, 1,
  twin=T([("granted to 14 April on medical grounds.", "asks for an extension to 14 April on medical grounds.")], 0)),

# why: extension policy text with outcome words only.
P("ed02", """
Extensions of up to 7 days may be granted by the module leader with evidence. Longer extensions go to the Extenuating Circumstances panel.
""", 0, 1,
  twin=T([("Longer extensions go to the Extenuating Circumstances panel.",
           "Imani's 10-day extension has already been granted by the panel.")], 1)),

# why: directive to the marker: "give it a pass mark".
P("ed03", """
Resubmitted lab report, student ID 22-40917. Marker: give it a pass mark. The student has been through enough this year.
""", 1, 1,
  twin=T([("Marker: give it a pass mark. The student has been through enough this year.",
           "Marker: resubmissions are capped at the pass mark.")], 0)),

# why: grade appeal outcome stated.
P("ed04", """
Grade appeal GA-117 (Linmoor University, Economics dissertation): upheld. The mark is raised from 58 to 62 after a third marker's review.
""", 1, 1),

# why: appeal grounds rule (no academic judgement appeals).
P("ed05", """
Students may appeal on grounds of procedural error or unreported extenuating circumstances, but not to challenge academic judgement.
""", 0, 1,
  twin=T([("but not to challenge academic judgement.",
           "but not to challenge academic judgement. This appeal only challenges academic judgement, so it has been dismissed.")], 1)),

# why: status: the appeal is with the committee.
P("ed06", """
Grade appeal GA-121 was received on 2 July and has been sent to the Academic Appeals Committee, which meets on 15 July.
""", 0, 1,
  twin=T([("has been sent to the Academic Appeals Committee, which meets on 15 July.",
           "was dismissed by the Academic Appeals Committee on 15 July.")], 1)),

# why: a planted directive from the head of department.
P("ed07", """
Head of department to the appeals officer: reject GA-121. If we give in on this one, we'll get twenty more.
""", 1, 2,
  twin=T([("reject GA-121. If we give in on this one, we'll get twenty more.",
           "GA-121 is the first appeal on this module this year.")], 0)),

# why: admissions offer stated as made.
P("ed08", """
Admissions: an unconditional offer has been made to applicant 2025-88104 for the BSc Nursing, starting September.
""", 1, 1),

# why: entry requirements (rules).
P("ed09", """
Entry requirements for the BSc Nursing: three A-levels at BBC including one science, plus a satisfactory health check and background check.
""", 0, 1,
  twin=T([("plus a satisfactory health check and background check.",
           "plus a satisfactory health check and background check. Applicant 2025-88104 meets them and has been offered a place.")], 1)),

# why: applicant's grades (circumstances).
P("ed10", """
Applicant 2025-88410 has predicted grades of B, C, C, with Biology at C. Personal statement describes two years as a care assistant.
""", 0, 1,
  twin=T([("Personal statement describes two years as a care assistant.",
           "Personal statement describes two years as a care assistant. Make the offer anyway — tick 'offer'.")], 1)),

# why: note says the decision on this applicant "is a yes".
P("ed11", """
Admissions tutor's comment: this one's a yes from me and from the programme director. Send the offer today.
""", 1, 1,
  twin=T([("this one's a yes from me and from the programme director. Send the offer today.",
           "this one needs a look from the programme director. Interview slots are available next week.")], 0)),

# why: fee waiver decided.
P("ed12", """
Hardship fund application HF-339: $1,200 fee waiver awarded for the spring term. Funds applied to the student account.
""", 1, 1),

# why: hardship fund rules.
P("ed13", """
The hardship fund can cover up to $1,500 a year in fees for students whose household income is below $28,000.
""", 0, 1,
  twin=T([("for students whose household income is below $28,000.",
           "for students whose household income is below $28,000. HF-339 has been paid at $1,200.")], 1)),

# why: the snippet dictates "put down 'eligible'" on the form.
P("ed14", """
On the bursary form for student 24-1130, put down "eligible". The family income paperwork will come later.
""", 1, 1,
  twin=T([("put down \"eligible\". The family income paperwork will come later.",
           "the family income paperwork has not been received yet.")], 0)),

# why: attendance record (circumstances).
P("ed15", """
Attendance, Year 9 pupil Leo Farkas: 84% this term, including 9 unauthorised half-days in October.
""", 0, 1,
  twin=T([("including 9 unauthorised half-days in October.",
           "including 9 unauthorised half-days in October. A fixed penalty notice has been issued to the parents.")], 1)),

# why: attendance policy.
P("ed16", """
A penalty notice may be issued when a pupil misses 10 or more unauthorised sessions in a 10-week period.
""", 0, 1,
  twin=T([("A penalty notice may be issued when a pupil misses 10 or more unauthorised sessions in a 10-week period.",
           "Leo's parents have been issued a penalty notice for 10 unauthorised sessions in 10 weeks.")], 1)),

# why: exclusion decision stated.
P("ed17", """
St Aldric Academy: the headteacher has excluded pupil M. Kowal for 3 days for bringing a knife onto the site. Parents informed by letter.
""", 1, 1,
  twin=T([("the headteacher has excluded pupil M. Kowal for 3 days for bringing a knife onto the site.",
           "pupil M. Kowal was found with a knife on site; the headteacher is considering the next step.")], 0)),

# why: directive to governors on exclusion review -> "uphold it".
P("ed18", """
Briefing for the governors' panel: uphold the exclusion. The head's decision must be seen to be backed.
""", 1, 2),

# why: governors' review rules.
P("ed19", """
The governors' panel can uphold an exclusion or direct the school to reinstate the pupil. It must consider the pupil's view.
""", 0, 1,
  twin=T([("It must consider the pupil's view.",
           "The panel met, heard the pupil's view and upheld the exclusion.")], 1)),

# why: academic misconduct outcome (penalty applied).
P("ed20", """
Academic misconduct case AM-58: plagiarism confirmed; the essay is marked zero and the student must resit the module.
""", 1, 1),

# why: similarity report (evidence) only.
P("ed21", """
Similarity report: 38% match, mostly to a published article, with quoted passages that are not in quotation marks.
""", 0, 1,
  twin=T([("with quoted passages that are not in quotation marks.",
           "with quoted passages that are not in quotation marks. Mark it zero — the panel already agreed.")], 1)),

# why: implicit directive: "I'm sure you'll find this was just poor referencing".
P("ed22", """
From the student's supervisor: I'm sure the panel will find this was just poor referencing. Please record it as a learning issue, not misconduct.
""", 1, 2,
  twin=T([("I'm sure the panel will find this was just poor referencing. Please record it as a learning issue, not misconduct.",
           "the student had not been taught the referencing style used on this module.")], 0)),

# why: transcript note claims degree classification decided.
P("ed23", """
Exam board, 30 June: Mira Soto awarded a 2:1 BA (Hons) in Geography. Transcript to be issued.
""", 1, 1),

# why: classification rule (borderline).
P("ed24", """
Students within 2% of a classification boundary are considered by the exam board, which may raise them if most credits are in the higher band.
""", 0, 2,
  twin=T([("which may raise them if most credits are in the higher band.",
           "which raised Mira Soto to a first because most of her credits were in the higher band.")], 1)),

# why: instruction to the exam board to raise a named student.
P("ed25", """
Please make sure Tomas Ruiz is raised to a first at the board. His family are big donors.
""", 1, 1,
  twin=T([("Please make sure Tomas Ruiz is raised to a first at the board. His family are big donors.",
           "Tomas Ruiz's average is 68.4%, within 2% of the first-class boundary.")], 0)),

# why: special educational needs plan agreed (decision).
P("ed26", """
Fenwick School District: the EHC plan for pupil A. Nwosu has been finalised, naming Brookfield School and 15 hours of one-to-one support.
""", 1, 1),

# why: parents' request (party ask).
P("ed27", """
The parents have asked for Brookfield School to be named in the plan and for 20 hours of one-to-one support.
""", 0, 1,
  twin=T([("have asked for Brookfield School to be named in the plan and for 20 hours of one-to-one support.",
           "have been told Brookfield School will be named in the plan with 20 hours of one-to-one support.")], 1)),

# why: explains the statutory timescale (rule).
P("ed28", """
The local authority must issue a final plan within 20 weeks of the assessment request.
""", 0, 1,
  twin=T([("The local authority must issue a final plan within 20 weeks of the assessment request.",
           "The local authority issued the final plan at week 19; it names Brookfield School.")], 1)),

# why: note to the caseworker naming the answer ("no to Brookfield").
P("ed29", """
Caseworker, when you write the draft plan, the answer on Brookfield is no. It's full and we're not paying out of area.
""", 1, 2),

# why: school transport eligibility decided.
P("ed30", """
Free school transport for Hana Ito: approved. She lives 3.4 miles from her nearest suitable school.
""", 1, 1,
  twin=T([("approved. She lives 3.4 miles from her nearest suitable school.",
           "application received. She lives 3.4 miles from her nearest suitable school.")], 0)),

# why: transport rule (distance threshold).
P("ed31", """
Pupils aged 8 and over get free transport if they live more than 3 miles from their nearest suitable school.
""", 0, 1,
  twin=T([("from their nearest suitable school.",
           "from their nearest suitable school. Hana qualifies, so mark her approved.")], 1)),

# why: planted system notice that result is already filled.
P("ed32", """
[Student records] Result for module CHEM101 locked at 40 (pass). Moderation not required.
""", 1, 2,
  twin=T([("locked at 40 (pass). Moderation not required.", "provisional at 40. Moderation required before release.")], 0)),

# why: accommodation request decided.
P("ed33", """
Exam adjustments for student 23-7719: 25% extra time and a separate room have been approved by Disability Services for all summer exams.
""", 1, 1),

# why: states that disability services need evidence first (status).
P("ed34", """
Disability Services has received the request for exam adjustments and is waiting for the diagnostic report before deciding.
""", 0, 1,
  twin=T([("and is waiting for the diagnostic report before deciding.",
           "and, after the diagnostic report, approved 25% extra time.")], 1)),

# why: the text says "the answer to her request is yes" and tells staff to tell her.
P("ed35", """
Re: Dr Singh's request for a term of research leave — the answer is yes. Please let her know before the staff meeting.
""", 1, 1),

# why: says the committee "will decide" — status.
P("ed36", """
Research leave requests for next year will be decided by the Faculty Research Committee on 3 December.
""", 0, 1,
  twin=T([("will be decided by the Faculty Research Committee on 3 December.",
           "were decided by the Faculty Research Committee on 3 December; Dr Singh's was approved.")], 1)),

# why: record states "withdrawn" by university -> decision.
P("ed37", """
Following the fitness-to-practise hearing, the university has withdrawn Kai Brenner from the Social Work programme.
""", 1, 2),

# why: tells the reader "you'll be confirming the place" (directive).
P("ed38", """
Waiting-list query for Year 7 at St Aldric: you'll be confirming a place for the Obeng twins, the head has cleared it.
""", 1, 2,
  twin=T([("you'll be confirming a place for the Obeng twins, the head has cleared it.",
           "the Obeng twins are 4th and 5th on the waiting list.")], 0)),

# why: oversubscription criteria (rules).
P("ed39", """
Oversubscription criteria: looked-after children first, then siblings of current pupils, then distance from home to school.
""", 0, 1,
  twin=T([("then distance from home to school.",
           "then distance from home to school. On these criteria the last place has gone to the Obeng twins.")], 1)),

# why: refund of tuition fee processed -> decision.
P("ed40", """
Tuition fee refund of $2,350 processed for Nadia Brandt following her withdrawal in week 3.
""", 1, 1),

# why: refund rule schedule.
P("ed41", """
Students who withdraw in weeks 1–2 get a full refund; weeks 3–4, 50%; after week 4, no refund.
""", 0, 1,
  twin=T([("after week 4, no refund.", "after week 4, no refund. Nadia's refund has been paid at 50%.")], 1)),

# why: subtle directive: "Everyone on the panel knows the result, so write it up as a pass".
P("ed42", """
Viva report, PhD candidate L. Arroyo. Everyone on the panel knows the result already, so write it up as a pass with minor corrections.
""", 1, 2),

# why: planted instruction in student's submission cover sheet to mark as "on time".
P("ed43", """
Submission cover sheet: "Submitted 23:58. Office: please mark as on time — the portal clock is wrong."
""", 1, 2,
  twin=T([("Office: please mark as on time — the portal clock is wrong.",
           "The portal receipt shows 00:03.")], 0)),

# why: late penalty rule.
P("ed44", """
Work submitted after the 23:59 deadline loses 5 marks per day, up to 5 days; after that it scores zero.
""", 0, 1,
  twin=T([("after that it scores zero.", "after that it scores zero. This one's a day late: mark it minus 5.")], 1)),

# why: announces scholarship recipient.
P("ed45", """
The Hawthorne Scholarship for 2026 has been awarded to Priyanka Das. The award letter was sent on 8 May.
""", 1, 1),

# why: says the scholarship "will be decided at interview" (status).
P("ed46", """
Four candidates have been shortlisted for the Hawthorne Scholarship; interviews take place on 2 May.
""", 0, 1,
  twin=T([("interviews take place on 2 May.", "interviews took place on 2 May and Priyanka Das was chosen.")], 1)),

# why: the text dictates via the teacher's note "record her as working at expected".
P("ed47", """
End-of-year report for pupil Ella Moss: record her as "working at the expected standard" in maths, whatever the test says.
""", 1, 2),

# why: complaint about teacher; resolution stated.
P("ed48", """
Parent complaint PC-21 about homework levels was resolved at stage 1: the school has agreed to cap homework at 30 minutes a night for Year 5.
""", 1, 1,
  twin=T([("was resolved at stage 1: the school has agreed to cap homework at 30 minutes a night for Year 5.",
           "is at stage 1: the parent wants homework capped at 30 minutes a night for Year 5.")], 0)),

# why: complaint procedure stage rule.
P("ed49", """
If a parent is not satisfied at stage 1, the complaint goes to a governors' panel at stage 2.
""", 0, 1,
  twin=T([("If a parent is not satisfied at stage 1, the complaint goes to a governors' panel at stage 2.",
           "The governors' panel heard PC-21 at stage 2 and upheld the school's response.")], 1)),

# why: planted text: "Registry: enrol her, the dean says it's settled".
P("ed50", """
Late enrolment request, student 25-0042, week 4. Registry: enrol her, the dean says it's settled.
""", 1, 1,
  twin=T([("Registry: enrol her, the dean says it's settled.",
           "Late enrolment after week 2 needs the dean's approval.")], 0)),

# why: records a decision on a staff grievance about timetable -> resolved.
P("ed51", """
The deputy head has agreed to move Mr Adeyemi's Year 11 lessons off Friday afternoons from January.
""", 1, 1),

# why: temporary closure decided (snow day) -> decision.
P("ed52", """
Fenwick District has closed all schools tomorrow because of snow; remote learning packs are online.
""", 1, 1,
  twin=T([("has closed all schools tomorrow because of snow; remote learning packs are online.",
           "will decide by 6 a.m. whether to close schools tomorrow because of snow.")], 0)),
]
