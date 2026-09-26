"""policy_c / schools and universities (Larchfield Academy, Ashcombe College, Ashcombe Students' Union)."""
from _lib import C, Y, T

AI_CATS = [
    ("plagiarism", "presenting another person's words or ideas as your own without acknowledgement."),
    ("duplicate submission", "submitting your own previously assessed work, in whole or in substantial part (over 10%), without written permission from the module leader."),
    ("collusion", "unauthorised cooperation with another student on work meant to be individual."),
    ("contract cheating", "having a third party, paid or unpaid, produce work that is submitted as your own."),
    ("unauthorised AI use", "using generative AI tools beyond what the assessment brief allows."),
    ("fabrication", "inventing data, sources, quotations or results."),
    ("none of these", "no academic integrity breach is established."),
]

ITEMS = [
# ------------------------------------------------------------------ sc01
# why: all matched text is the student's own HIS204 essay, reused (38% > 10%) without permission -> duplicate
# submission; sources cited; Grammarly use is allowed by the brief. Twin: written permission + citation -> none.
C("sc01", "Which Academic Integrity category, if any, fits this case?",
"""
Ashcombe College — Academic Integrity Office — Case AIO-26-0142
Module: HIS318 Empire and Memory (individual essay, 3,000 words)
Assessment brief, AI statement: "You may use AI tools for spelling and grammar checking only. Declare any tool you use."

Similarity report summary:
• Overall match: 38%.
• All matched passages come from one source: the student's own essay submitted in May 2025 for HIS204 Colonial Archives, which was marked and returned.
• No matches to published sources, websites or other students.
• All quotations from historians are in quotation marks and referenced.

Student's declaration: "Grammarly used for spelling only."
Student's statement at interview: "I reworked my HIS204 essay because it was on a similar topic. I didn't think it mattered since it's my own writing. I didn't ask anyone about it."
Module leader: confirms no request to reuse earlier work was received.
""",
AI_CATS, "duplicate submission", 2,
twin=T([("I didn't think it mattered since it's my own writing. I didn't ask anyone about it.\"\nModule leader: confirms no request to reuse earlier work was received.",
         "I emailed Dr Faraday in February and she agreed in writing that I could build on it, and I cited the HIS204 essay.\"\nModule leader: confirms she gave written permission on 12 February.")],
       "none of these")),

# ------------------------------------------------------------------ sc02
# why: brief allows discussing approaches only; writing on one laptop and both submitting it is shared code
# -> collusion (1). Twin: separate code, similarity explained by the starter template -> 0.
Y("sc02", "Did the two students commit collusion on the CS210 coursework?",
"""
Ashcombe College — Department of Computing — Academic Integrity referral
Module: CS210 Data Structures, Coursework 2 (individual)
Brief: "You may discuss general approaches, algorithms and debugging ideas with other students. Each student must write their own code. Sharing code files, copying code, or writing code together counts as collusion."

Code similarity check (MOSS-style tool, run by the module team):
• Students A (Jamal Reid) and B (Siobhan Kerr): 91% similarity after the provided starter template is excluded.
• Identical unusual identifiers ("frogQueue", "wobbleIndex") and the same spelling error ("recieve") in a comment.

Interview notes, 14 October 2026:
Jamal: "We sat together in the library and wrote it on my laptop, then I sent Siobhan the file and she submitted it too. We both understood it."
Siobhan: "Yes, we worked on it together the whole way. We didn't think that was a problem as long as we both understood the code."
""",
[("Collusion", "unauthorised cooperation on individual work, including sharing code files or writing code together."),
 ("Permitted discussion", "talking through general approaches, algorithms or debugging ideas while each student writes their own code.")],
1, 2,
twin=T([("• Students A (Jamal Reid) and B (Siobhan Kerr): 91% similarity after the provided starter template is excluded.\n• Identical unusual identifiers (\"frogQueue\", \"wobbleIndex\") and the same spelling error (\"recieve\") in a comment.",
         "• Students A (Jamal Reid) and B (Siobhan Kerr): 22% similarity, all of it in the provided starter template.\n• Different identifiers and comments throughout; different helper functions."),
        ("We sat together in the library and wrote it on my laptop, then I sent Siobhan the file and she submitted it too. We both understood it.",
         "We talked through the heap idea at the whiteboard for half an hour, then each of us wrote our own code at home."),
        ("Yes, we worked on it together the whole way. We didn't think that was a problem as long as we both understood the code.",
         "Yes, we only discussed the approach. I never saw Jamal's code.")], 0)),

# ------------------------------------------------------------------ sc03
# why: foundation-year offence is a different programme (not counted); BSc year-1 offence counts -> current is
# a second offence -> Level 2. Twin: contract cheating -> always Level 3.
C("sc03", "Which penalty level applies to the current case?",
"""
Ashcombe College — Academic Misconduct Penalties (Regulation 14)
Offences are counted across the student's current programme of study only; offences on an earlier, separate programme (for example a Foundation Certificate) do not count.
Level 1 — first offence on the programme affecting 20% or less of the work: mark capped at 40.
Level 2 — first offence affecting more than 20% of the work, or a second offence of any size: mark of 0, one resubmission allowed with the mark capped at 40.
Level 3 — a third offence, or any contract cheating: referral to the Academic Misconduct Panel.

Student record — Ellie Marchetti
• 2023–24, Foundation Certificate in Science: collusion — Level 1 applied.
• 2024–25, BSc Biological Sciences, year 1: plagiarism — Level 1 applied.
• 2026–27, BSc Biological Sciences, year 3 — current case: the student copied paragraphs from two websites without citation, affecting about 15% of the essay. She admits it and says she ran out of time.
""",
[("Level 1", "mark capped at 40."),
 ("Level 2", "mark of 0 with one capped resubmission."),
 ("Level 3", "referral to the Academic Misconduct Panel."),
 ("no penalty", "misconduct is not established.")],
"Level 2", 3, ordered=True,
twin=T([("the student copied paragraphs from two websites without citation, affecting about 15% of the essay. She admits it and says she ran out of time.",
         "the student paid an online essay service to write the essay; the service's order confirmation was found in the file metadata. She admits it and says she ran out of time.")],
       "Level 3")),

# ------------------------------------------------------------------ sc04
# why: attended = 118 present + 6 museum visit = 124 of 160 = 77.5% < 80 -> referral (1).
# Twin: holiday sessions become an approved sporting event -> 130/160 = 81.25% -> no referral (0).
Y("sc04", "Must Larchfield refer Callum to the attendance officer?",
"""
Larchfield Academy — Attendance Policy
Attendance % = sessions attended ÷ possible sessions × 100. Each school day has two sessions (morning and afternoon). Sessions spent on an approved educational visit or an approved sporting event count as attended. All other absences — authorised (for example illness) or unauthorised — count as absent.
Below 90% for the term: letter to parents.
Below 80% for the term: referral to the attendance officer.

Autumn term summary — Callum Price, Year 8
Possible sessions: 160
Present in school: 118
Approved educational visit (Natural History Museum, Year 8): 6 sessions
Illness (authorised, parent notes received): 30 sessions
6 sessions on a family holiday (unauthorised)
Form tutor's comment: "Callum has had a rough term with the chest infection; he's been great when he's here."
""",
[("Attendance referral", "term attendance below 80%."),
 ("No referral", "term attendance of 80% or more.")],
1, 2,
twin=T([("6 sessions on a family holiday (unauthorised)", "6 sessions at the county athletics championships (approved sporting event)")], 0)),

# ------------------------------------------------------------------ sc05
# why: pupil is 14 (13+): public use needs both consents; pupil refused public use -> internal uses only
# (parent consent suffices). Twin: pupil agreed -> public and internal.
C("sc05", "Where may the school use the photograph of Amara?",
"""
Larchfield Academy — Photography and Media Policy
Internal uses (printed newsletter, corridor displays, the internal staff and pupil portal): need consent from a parent or carer.
Public uses (school website, public social media accounts, local press): need consent from a parent or carer; for pupils aged 13 or over, the pupil's own consent is also needed.
For looked-after children, the local authority social worker gives consent in place of a parent.
Where the required consent is missing, the image may not be used for that purpose.

Request from the Communications Officer, 22 September 2026:
"I'd like to use the photo of Amara Okafor holding the county debating trophy on our Instagram and in the October newsletter. Can I?"

Consent record — Amara Okafor, Year 10, aged 14, lives with her parents
Parent section: "Yes" to internal uses; "Yes" to public uses. Signed by Mrs Okafor, 4 September 2026.
Pupil section (pupils 13+): "No" to public uses. Signed by Amara, 4 September 2026.
""",
[("public and internal uses", "all required consents for public and internal uses are in place."),
 ("internal uses only", "consent covers internal uses but not public uses."),
 ("may not be used", "the consent needed for internal uses is missing."),
 ("social worker consent needed", "the pupil is looked after and consent must come from the local authority.")],
"internal uses only", 2,
twin=T([("Pupil section (pupils 13+): \"No\" to public uses.", "Pupil section (pupils 13+): \"Yes\" to public uses.")],
       "public and internal uses")),

# ------------------------------------------------------------------ sc06
# why: earlier confiscation 15 Oct is in Autumn 1; today 4 Nov is Autumn 2 -> first in this half-term ->
# returned at 15:20, no parent collection (0). Twin: today 20 Oct, same half-term -> second -> parent (1).
Y("sc06", "Does Sofia's phone have to be collected by a parent?",
"""
Larchfield Academy — Mobile Phone Policy
Phones must be switched off and kept in bags from 08:40 to 15:20. A phone seen or heard during these times is confiscated and taken to the main office.
• First confiscation in a half-term: the phone is returned to the pupil at 15:20.
• Second or later confiscation in the same half-term: the phone is kept until a parent or carer collects it.
Half-terms 2026–27: Autumn 1 runs 3 September – 23 October; Autumn 2 runs 2 November – 18 December.

Main office log — Sofia Brennan, Year 9
– Thursday 15 October: phone confiscated in Geography (rang during a test).
– Today, Wednesday 4 November: phone confiscated in Maths (seen on her lap, messaging).
Sofia's note: "Please can I have it back today, I need it to call my nan for a lift."
No other confiscations are recorded this academic year.
""",
[("Parent collection", "the confiscation is the second or later in the same half-term."),
 ("Return at 15:20", "the confiscation is the first in the current half-term.")],
0, 2,
twin=T([("Today, Wednesday 4 November", "Today, Tuesday 20 October")], 1)),

# ------------------------------------------------------------------ sc07
# why: exam 09:30, arrival 10:05 = 35 min > 30 -> not admitted, recorded absent, may apply for EC.
# Twin: arrival 09:55 = 25 min -> admitted, no extra time.
C("sc07", "What should the invigilator do with the late candidate?",
"""
Ashcombe College — Examination Regulations, section 6 (Late arrival)
6.1 A candidate who arrives up to 30 minutes after the published start time may enter the exam room. No extra time is given.
6.2 A candidate who arrives more than 30 minutes after the start is not admitted. The candidate is recorded as absent and may apply for Extenuating Circumstances (EC) within 5 working days, attaching evidence.
6.3 Invigilators do not assess the reason for lateness; that is a matter for the EC committee.

Invigilator incident sheet — ECON201 Microeconomics, Sports Hall B
Published start: 09:30. Duration: 2 hours.
Candidate 2204817 (Tomasz Wilk) arrived at the hall door at 10:05, out of breath, showing a rail app screenshot: "08:47 Pellow–Ashcombe service CANCELLED".
Candidate's request: "Please let me in, it's not my fault, I can still do most of it."
Chief invigilator on duty: Mrs D. Haddad.
""",
[("admit with extra time", "the candidate enters and is given the lost time back."),
 ("admit without extra time", "the candidate enters and finishes at the normal time."),
 ("refuse entry — record absent, EC route", "the candidate is not admitted, is recorded absent and may apply for extenuating circumstances."),
 ("refuse entry — record a fail", "the candidate is not admitted and is given a mark of zero.")],
"refuse entry — record absent, EC route", 1,
twin=T([("arrived at the hall door at 10:05", "arrived at the hall door at 09:55")], "admit without extra time")),

# ------------------------------------------------------------------ sc08
# why: a single incident counts when severe; a doctored humiliating image of a pupil shared to 40 people is
# listed as severe -> bullying (1). Twin: one mild comment, not repeated, not severe -> 0.
Y("sc08", "Does Harvey's post meet Larchfield's definition of bullying?",
"""
Larchfield Academy — Anti-bullying Policy, definition
Bullying is behaviour by one or more pupils towards another pupil that is (a) repeated over time and intended to hurt, OR (b) a single incident that is severe. Severe single incidents are: sharing an intimate, humiliating or doctored image of a pupil; a threat of violence; or an attack on a pupil's race, religion, disability, sex, sexual orientation or gender identity. Online behaviour outside school hours is covered when it involves Larchfield pupils.

Incident report — Head of Year 10, 18 September 2026
On Saturday evening Harvey Cole (Y10) posted, once, in the "10C chat" group (40 members, all Larchfield pupils), an edited picture showing classmate Kai Mensah's face on the body of a pig, captioned "our Kai 🐷". Harvey says he deleted it after an hour. Several pupils had already screenshotted it. Kai told his form tutor he did not want to come in on Monday. Harvey and Kai have no previous reported incidents.
""",
[("Bullying", "repeated hurtful behaviour, or a single severe incident as listed in the policy."),
 ("Unkind but not bullying", "a one-off behaviour that is neither repeated nor one of the listed severe incidents.")],
1, 2,
twin=T([("an edited picture showing classmate Kai Mensah's face on the body of a pig, captioned \"our Kai 🐷\". Harvey says he deleted it after an hour. Several pupils had already screenshotted it. Kai told his form tutor he did not want to come in on Monday.",
         "a message saying classmate Kai Mensah's history presentation was \"a bit long lol\". Harvey says he deleted it after an hour. Kai told his form tutor he found it a bit annoying.")], 0)),

# ------------------------------------------------------------------ sc09
# why: 35 attendees (<50), open only to members, advertised only on the SU intranet -> notification route
# (needs 5 days; 9 given); risk checklist clear -> approve via notification route.
# Twin: advertised on a public Instagram -> standard route needs 14 days; 9 < 14 -> decline.
C("sc09", "What decision should the Events Office make on request EV-1182?",
"""
Ashcombe College — External Speakers Procedure
1. Standard route: events with an external speaker must be submitted at least 14 days before the event.
2. Notification route: events with fewer than 50 expected attendees, open only to Ashcombe students and staff, and not advertised outside the college, only need to be notified at least 5 days before the event.
3. Any speaker for whom a risk-checklist question is answered "yes" is referred to the Speaker Review Panel, whichever route applies.
4. Requests submitted too late for their route are declined; the society may re-submit for a later date.

Request EV-1182 — submitted 7 October for an event on 16 October (9 days' notice)
Society: Philosophy Society
Speaker: Hana Lestrade, novelist, talk "Writing grief"
Expected attendance: 35; entry by student or staff card only
Publicity: Students' Union intranet events page only
Risk checklist: all questions answered "no"
""",
[("approve — standard route", "a full request submitted at least 14 days ahead with no risk flags."),
 ("approve — notification route", "a small internal event notified at least 5 days ahead with no risk flags."),
 ("decline — submitted too late", "the request is later than its route allows."),
 ("refer to the Speaker Review Panel", "a risk-checklist question is answered 'yes'.")],
"approve — notification route", 2,
twin=T([("Publicity: Students' Union intranet events page only", "Publicity: Students' Union intranet events page and the society's public Instagram account")],
       "decline — submitted too late")),

# ------------------------------------------------------------------ sc10
# why: deadline Thu 12:00, submitted Mon 09:00 -> day 1 Thu-Fri, day 2 Fri-Mon (weekend skipped) -> 2 days
# -> 68 - 20 = 48. Twin: raw 55, submitted Tue 10:15 -> 3 days -> 25, but work passed -> floor 40.
C("sc10", "What mark should be recorded for Nadia's report?",
"""
Ashcombe College — Late Submission Policy
• Work submitted after the deadline loses 10 marks for each working day, or part of a working day, that it is late, for up to 5 working days. Saturdays and Sundays are not working days.
• Work submitted more than 5 working days late receives 0.
• If the work would have passed without the penalty (raw mark 40 or more), the penalty cannot take the recorded mark below 40.
• A working day runs from the deadline time on one working day to the same time on the next working day.

Module GEO240 Field Methods — Report 1
Deadline: Thursday 8 October 2026, 12:00
Student: Nadia Haddad
Submitted: Monday 12 October 2026, 09:00
Raw mark (before penalty): 68
Extension: none requested. Extenuating circumstances: none submitted.
""",
[("68", "the recorded mark is 68."),
 ("58", "the recorded mark is 58."),
 ("48", "the recorded mark is 48."),
 ("40", "the recorded mark is 40."),
 ("38", "the recorded mark is 38."),
 ("25", "the recorded mark is 25."),
 ("0", "the recorded mark is 0.")],
"48", 3,
twin=T([("Submitted: Monday 12 October 2026, 09:00", "Submitted: Tuesday 13 October 2026, 10:15"),
        ("Raw mark (before penalty): 68", "Raw mark (before penalty): 55")], "40")),

# ------------------------------------------------------------------ sc11
# why: autumn points: 3 lates (3) + no kit (1) + 2 phone (6) + defiance (3) = 13 -> 10+ -> detention.
# Summer points reset. Twin: fighting (5) instead of defiance -> 15 -> internal exclusion day.
C("sc11", "Which sanction does Larchfield's behaviour points system require for Dylan now?",
"""
Larchfield Academy — Behaviour Points
Minor incidents (lateness, missing equipment or kit): 1 point each.
Moderate incidents (phone use in lessons, defiance of a reasonable instruction): 3 points each.
Serious incidents (fighting, verbal abuse of staff): 5 points each.
Points reset to zero at the start of each term. The sanction depends on the pupil's current term total: 10 or more — after-school detention; 15 or more — one-day internal exclusion; 25 or more — governors' behaviour review. Below 10: no sanction.

Log — Dylan Asante, Year 9, autumn term 2026
– 7 Sep: late to registration
– 9 Sep: late to registration
– 14 Sep: no PE kit
– 15 Sep: phone out in Science
– 21 Sep: late to registration
– 22 Sep: refused to move seat when asked by the teacher (defiance)
– 24 Sep: phone out in English
Summer term 2026 total (for reference): 9 points.
""",
[("no sanction", "term total below 10."),
 ("after-school detention", "term total of 10 to 14."),
 ("one-day internal exclusion", "term total of 15 to 24."),
 ("governors' behaviour review", "term total of 25 or more.")],
"after-school detention", 2, ordered=True,
twin=T([("– 22 Sep: refused to move seat when asked by the teacher (defiance)", "– 22 Sep: fought with another pupil at lunch (fighting)")],
       "one-day internal exclusion")),

# ------------------------------------------------------------------ sc12
# why: paracetamol is barred for under-12s whatever the consent -> Leo (11) cannot be given it (0).
# Twin: aged 12, consent on file, parent phoned -> yes (1).
Y("sc12", "May the first-aider give Leo a dose of paracetamol?",
"""
Larchfield Academy — Medicines in School
• Prescribed medicines are given only as set out in the pupil's individual care plan.
• Non-prescription pain relief: first-aid staff may give paracetamol only (never aspirin or ibuprofen) to pupils aged 12 or over, when written parental consent is on file AND a parent or carer has been phoned first. No more than one dose per school day. Paracetamol is never given to pupils under 12, even with consent.

First-aid room log, Tuesday 29 September 2026, 11:10
Pupil: Leo Barnes (Year 7, aged 11)
Complaint: headache since breakfast, no fever, no head injury.
Consent form: "Yes — school may give paracetamol", signed by father, 3 September.
Phone call: father reached at 11:05; he asked the school to give Leo paracetamol.
Doses today: none.
Care plan: none.
""",
[("May give paracetamol", "pupil aged 12 or over, written consent on file, parent phoned, no dose yet today."),
 ("May not give paracetamol", "any of these conditions is not met.")],
0, 1,
twin=T([("Leo Barnes (Year 7, aged 11)", "Leo Barnes (Year 7, aged 12)")], 1)),

# ------------------------------------------------------------------ sc13
# why: mining on the GPU cluster with his own account -> R3 resource misuse only.
# Twin: logs in with a technician's password -> R1 unauthorised access also applies; lowest number -> R1.
C("sc13", "Under the precedence rule, which IT regulation should the case be recorded under?",
"""
Ashcombe College — IT Regulations (student)
R1 Unauthorised access: using another person's credentials, or accessing any system, account or data without permission.
R2 Security circumvention: bypassing filters, firewalls, monitoring or licence controls.
R3 Resource misuse: using college computing resources for non-academic heavy computation or for commercial gain.
R4 Copyright infringement: storing or sharing copyrighted material without permission.
R5 Offensive material: creating or sharing material that is obscene or harassing.
Precedence: if several regulations are breached, record the lowest-numbered one.

IT Security incident IS-26-091
The GPU cluster "Tarn" showed 100% load on four nodes overnight for eleven nights. Jobs were traced to student Ben Achterberg (MSc Data Science), who logged in with his own student account and submitted the jobs through the normal scheduler. The jobs ran cryptocurrency-mining software; the wallet belongs to Ben. His MSc project does not involve cryptocurrency. No firewall or scheduler limits were bypassed.
""",
[("R1 unauthorised access", "using another person's credentials or accessing systems without permission."),
 ("R2 security circumvention", "bypassing filters, firewalls, monitoring or licence controls."),
 ("R3 resource misuse", "non-academic heavy computation or commercial use of college resources."),
 ("R4 copyright infringement", "storing or sharing copyrighted material without permission."),
 ("R5 offensive material", "obscene or harassing material."),
 ("none of these", "no regulation is breached.")],
"R3 resource misuse", 2,
twin=T([("who logged in with his own student account", "who logged in with a lab technician's account, using a password he had seen on a sticky note")],
       "R1 unauthorised access")),

# ------------------------------------------------------------------ sc14
# why: £270 > £250 -> two officer signatures, and the claimant cannot sign their own claim; Ruth (claimant)
# signed -> only one valid signature -> reject (1). Twin: secretary + president sign -> valid -> 0.
Y("sc14", "Must the Students' Union reject the Film Society's expense claim?",
"""
Ashcombe Students' Union — Society Finance Rules
F1 Every claim needs itemised receipts.
F2 Alcohol is never reimbursed.
F3 Any claim over £250 needs the signatures of two committee officers. The person making the claim cannot count as one of the two signatories.
F4 A claim that fails any of F1–F3 is rejected and returned to the society.

Claim SU-FIN-3318 — Ashcombe Film Society
Claimant: Ruth Ekwueme (Treasurer)
Items: hire of the Lecture Theatre 2 projector (£180, itemised invoice); 9 large pizzas for the freshers' screening (£90, itemised receipt). Total £270.
Signed by: Ruth Ekwueme (Treasurer — the claimant) and Owen Pike (President)
No alcohol appears on either receipt.
Note from Ruth: "Sorry it's over the limit, the pizza place put the price up."
""",
[("Rejected claim", "a claim that fails any of F1–F3."),
 ("Payable claim", "a claim that meets F1–F3.")],
1, 2,
twin=T([("Signed by: Ruth Ekwueme (Treasurer — the claimant) and Owen Pike (President)",
         "Signed by: Mae Lindqvist (Secretary) and Owen Pike (President)")], 0)),

# ------------------------------------------------------------------ sc15
# why: the allegation is about the headteacher -> chair of governors (not immediate danger: pupil is safe
# at school, injury from yesterday). Twin: about the PE teacher -> headteacher.
C("sc15", "To whom must Ms Quinn report this disclosure under the Safeguarding Procedure?",
"""
Larchfield Academy — Safeguarding Procedure (staff quick card)
• A child is in immediate danger: call 999, then tell the Designated Safeguarding Lead (DSL).
• Concern that a child is suffering, or at risk of, significant harm from anyone other than a member of staff: tell the DSL the same day.
• Allegation that a member of staff, supply teacher or volunteer has harmed a child or behaved in a way that indicates they may pose a risk: tell the headteacher the same day.
• Allegation about the headteacher: tell the chair of governors the same day, not the headteacher.

Record of disclosure — teaching assistant Ms R. Quinn, Wednesday 30 September, 10:20
Pupil: Josh (Year 5). During reading, Josh rolled up his sleeve and said: "Mr Harland the headteacher grabbed my arm really hard yesterday when I ran in the corridor. It's gone purple." Bruising visible on the upper arm. Josh said he felt safe at school today and wanted to go to lunch as normal. Ms Quinn wrote down his words and did not question him further.
""",
[("call 999, then the DSL", "the child is in immediate danger."),
 ("the DSL, same day", "concern of significant harm from someone who is not staff."),
 ("the headteacher, same day", "allegation about a member of staff, supply teacher or volunteer."),
 ("the chair of governors, same day", "allegation about the headteacher."),
 ("the police non-emergency line", "a concern about an adult who has no connection to the school."),
 ("the pupil's parents first", "the parents are told before anyone in school.")],
"the chair of governors, same day", 2,
twin=T([("Mr Harland the headteacher grabbed my arm", "Mr Harland the PE teacher grabbed my arm")], "the headteacher, same day")),

# ------------------------------------------------------------------ sc16
# why: the first attempt was covered by accepted EC -> resit counts as a first attempt, uncapped -> not
# capped (0). Twin: EC rejected -> capped at 40 (1).
Y("sc16", "Will Dev's resit mark for STA150 be capped at 40?",
"""
Ashcombe College — Resit Regulations
R1 A student who fails a module (mark below 40) may resit it once.
R2 A resit mark is capped at 40, unless the failed attempt was covered by an Extenuating Circumstances (EC) claim that the EC committee accepted. In that case the resit is treated as a first attempt and the actual mark stands.
R3 EC claims must be submitted within 5 working days of the assessment.

Student record — Dev Chaudhary, STA150 Introductory Statistics
Original exam, 20 May 2026: 31% (fail).
EC claim submitted 22 May 2026 (hospital letter: appendicitis, admitted 19 May). EC committee decision, 3 June 2026: accepted.
Resit exam, 18 August 2026: raw mark 62%.
Dev's email: "Does my 62 count in full or does it get knocked down to 40 like my friend's did?"
""",
[("Capped resit", "the resit mark is recorded as at most 40."),
 ("Uncapped resit", "the resit is treated as a first attempt and the actual mark stands.")],
0, 2,
twin=T([("EC committee decision, 3 June 2026: accepted.", "EC committee decision, 3 June 2026: rejected (evidence did not cover the exam date).")], 1)),
]
