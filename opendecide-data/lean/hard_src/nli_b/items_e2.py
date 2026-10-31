"""Part E2: mixed phenomena, long passages and large option sets (continued)."""
from _h import it, L3, L3CARD, FOLLOW, CONSIST, E, C, U, NONE

ROOMS = [f"E{i}" for i in range(1, 13)] + [f"W{i}" for i in range(1, 12)]
RM_OPTS = [f"room {r}" for r in ROOMS] + [NONE]

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]

DEON = ["required", "permitted but not required", "forbidden", "the passage does not settle this"]
DEONCARD = ("- required: the rules say it must be done\n"
            "- permitted but not required: the rules allow it and also allow not doing it\n"
            "- forbidden: the rules say it must not be done\n"
            "- the passage does not settle this: the rules quoted do not fix whether it is required, permitted or forbidden")

S26 = ["No panel member detected cork taint in the 2019 reserve magnums",
       "No panel member detected any fault at all in the 2019 reserve",
       "Some panel member detected cork taint in another vintage",
       "Every panel member tasted the 2019 reserve magnums",
       NONE]

ITEMS = [

it("E14", "choice",
   "Which of these rooms must have been deep-cleaned on Monday evening?",
   """St Wilfrid's Hospital - Outpatients: domestic services report, Monday

Rule for this week (infection-control instruction IC-14): every east-corridor consulting room that was booked on Monday was deep-cleaned on Monday evening, unless it was booked by the Radiology team, whose rooms are cleaned by their own contractor. West-corridor rooms follow the normal weekly schedule, and the report does not say which of them were cleaned.

Monday bookings (from the room-booking system):
- E1: Dermatology (Monday)   - E2: not booked Monday   - E3: Radiology (Monday)
- E4: booking record missing   - E5: Radiology (Monday)   - E6: not booked Monday
- E7: Rheumatology (Monday)   - E8: Dermatology (Tuesday only)   - E9: not booked Monday
- E10: Radiology (Monday)   - E11: booking cancelled on Sunday   - E12: not booked Monday
- W1: Cardiology (Monday)   - W2: Diabetes (Monday)   - W3: not booked Monday
- W4: Radiology (Monday)   - W5: Ophthalmology (Monday)   - W6: not booked Monday
- W7: Urology (Monday)   - W8: not booked Monday   - W9: Dermatology (Monday)
- W10: not booked Monday   - W11: Pain clinic (Monday)

Correction received at 16:40 from the booking office: E1 was booked on Monday by Radiology, not Dermatology; Dermatology used E1 on Tuesday only.

Supervisor: Grace Mbatha""",
   "room E7", opts=RM_OPTS,
   card="\n".join(f"- room {r}: the consulting room numbered {r}" for r in ROOMS)
        + "\n- none of these: the report does not guarantee that any listed room was deep-cleaned on Monday evening",
   diff=3),

it("E15", "choice",
   "In which month did the certification visit take place?",
   """Northmere Fire and Rescue - Training Unit: certification record, Crew 7 (Harlow station)

Rules for the annual breathing-apparatus certification visit:
1. The visit takes place in the first month after the crew's probation period ends in which the regional assessor is available and the visit is allowed.
2. A visit is allowed in a month only if the crew has submitted its training log for the previous month.

Facts on file:
- Crew 7's probation period ended on 31 May.
- The regional assessor, Station Officer Dagny Holm, was unavailable in June (secondment) and in August (annual leave). She was available in every other month of the year.
- Crew 7 submitted its training log for every month of the year except June; the June log was lost when the station laptop failed and was never resubmitted.
- The visit took place in the year the probation period ended, and the crew passed.

Next certification due: twelve months after the visit.""",
   "September", opts=MONTHS,
   card="\n".join(f"- {m}: the visit took place in {m}" for m in MONTHS),
   diff=3),

it("E16", "choice",
   "Given the security review, which inference label applies to the statement?",
   """Kesterton House - Security review of the Level 4 access system (summary for the tenants' committee)

How the system works. Every exit from the building passes through a speed gate. The gate records a swipe-out only if a staff badge is presented; there is no other way to register a swipe-out, and the gates cannot be opened from the inside without one (the fire exits alarm and were not used in the period reviewed).

Finding. For the review week (3-7 March), the security team matched gate records against the Level 4 staff list. None of the Level 4 staff left the building without swiping out on any day that week. Two Level 2 visitors were found to have followed staff through the gates.

Recommendations. Tailgating signs at the gates; a reminder to staff not to hold gates open for others.

Statement: Every Level 4 staff member who left the building during the review week presented a badge when leaving.""",
   E, opts=L3[1], card=L3CARD, diff=2),

it("E17", "choice",
   "Given only the staffing policy and the email, what is the status of the statement?",
   """Hollybank Care Home - Staffing policy (extract)

3.1 Each shift must have at least one member of staff with a current first-aid certificate on duty.
3.2 The shift leader is responsible for checking the rota against the first-aid list at the start of each shift.
3.3 If no first-aider is available, the shift leader must inform the on-call manager immediately.

Email from the deputy manager, Tuesday 6 May:
"Hi all - I'm doing the monthly rota audit. The rota for the night shift of Sunday 4 May was changed three times on the day because of sickness, and the final version wasn't saved to the shared drive. I've asked the night shift leader to tell me who actually worked. Until then I can't confirm whether 3.1 was met. The on-call log for Sunday night is blank. - Beatriz"

Statement: At least one member of staff with a current first-aid certificate worked on the night shift of Sunday 4 May.""",
   U, opts=L3[2], card=L3CARD, diff=2),

it("E18", "choice",
   "Taking the works council update as accurate, how should the statement be labelled?",
   """Works Council - Update for all employees, Rendell Components (Tamworth plant)

Colleagues,

We know that the rumour that the Tamworth plant will close has unsettled many of you, especially after the loss of the Veltra contract in the spring. We raised the rumour directly with the managing director at Tuesday's council meeting.

The managing director told us that no decision about the future of the plant has been taken, that the board is reviewing all three UK sites as part of its annual strategy process, and that the works council will be consulted before any proposal affecting jobs is made. We will hold her to that.

In the meantime, overtime on the brake-calliper line continues as planned, and the apprenticeship intake for September has been confirmed.

Your Works Council representatives

Statement: The Tamworth plant will close.""",
   U, opts=L3[3], card=L3CARD, diff=2),

it("E19", "choice",
   "What is the status of the statement, given the admissions letter extract?",
   """Pencarrow School of Nursing - Admissions: extract from the outcome letters log

Selection rule for the September intake (agreed by the admissions board): every candidate who scored at least 70 on both written papers was offered a place, whatever their interview outcome. Candidates who scored at least 70 on only one paper were offered a place only if their interview score was at least 3 out of 5.

Log entry, candidate 2026-0417, Ms. Rhian Talbot:
- Paper 1 (numeracy): 84
- Paper 2 (written communication): 77
- Interview: not held - the interview on 12 May was cancelled because the panel chair was ill and was not rearranged before the offers deadline.
- Outcome letter: sent 30 May; copy not yet scanned to the file.

The admissions officer has asked for the scanned copy to be added before the audit.

Statement: Ms. Rhian Talbot was offered a place for the September intake.""",
   E, opts=L3[4], card=L3CARD, diff=2),

it("E20", "noul",
   "If everything in the returning officer's note is true, must the statement be true?",
   """Brambleton Allotment Society - Note from the returning officer on the constitutional amendment

The postal ballot on amendment 4 (allowing beehives on half-plots) closed on 30 June. The society has 212 members.

I can report two things with confidence. First, more than half of the members returned a valid ballot paper. Second, more than half of the members who returned a valid ballot paper supported the amendment. I am not able to give exact figures yet, because a number of papers arrived in the same envelope and the committee has asked me to recheck them before the counts are published.

Under the constitution, an amendment passes if more than half of the valid ballot papers returned support it. The amendment therefore passes. The committee will publish guidance on siting hives before the autumn meeting.

Statement: More than half of the society's members supported amendment 4.""",
   0, card=FOLLOW, diff=3),

it("E21", "noul",
   "Does the statement follow from the landlord's reply?",
   """From: Mr. Desmond Arkwright (landlord)
To: Ms. Yewande Obi (tenant), Flat 4, 11 Calder Street
Subject: RE: Fire safety inspection

Dear Ms. Obi,

Thank you for your email. You said you had heard from the tenant in Flat 2 that the fire safety inspector "didn't bother looking at the exits" when she visited on 14 August.

I have spoken to the inspection company and read the inspector's report. It is not true that the inspector failed to check the fire exits: the report lists the two rear exits and the front door, with photographs and a note that the rear exit bar on the ground floor was stiff. I have booked a locksmith to fix that on 2 September.

I will put a copy of the report in the communal hallway.

Kind regards,
Desmond Arkwright

Statement: The inspector checked the fire exits at 11 Calder Street on 14 August.""",
   1, card=FOLLOW, diff=2),

it("E22", "noul",
   "Is the statement consistent with the licensee's incident log?",
   """The Weavers' Arms - Incident log (kept under the premises licence), Saturday 8 November

21:15 A group of six arrived for a birthday. Door staff checked IDs. One member of the group, Tomasz (age 17, provisional driving licence checked), was admitted with the group because the premises allows under-18s until 22:00 when accompanied by adults eating a meal.

21:20 Bar staff briefed: Tomasz is under 18.

21:50 Challenge 25 refusal log: no entries tonight.

22:00 Tomasz left with his father, who confirmed he would collect the rest of the group later.

Licensee's summary for the night: nobody under 18 was served alcohol. No refusals were needed because the under-18 in the group did not try to buy alcohol. No incidents.

Signed: Ruth Callander, Designated Premises Supervisor

Statement: Tomasz was served a soft drink at the bar.""",
   1, card=CONSIST, diff=2),

it("E23", "noul",
   "Based only on the paralegal's email, is the statement guaranteed?",
   """From: Nkechi Ibe, Paralegal, Harwood Linney LLP
To: Oliver Brandauer, Associate
Subject: Completion bundle - Fenwick Road lease

Oliver,

I've finished checking the completion bundle for the Fenwick Road lease against the checklist. Two issues:

1. Not every page of the engrossed lease was initialled by the tenant's director. The lease is 42 pages, and the checklist requires initials on every page. I've flagged the bundle but I haven't yet listed which pages are missing initials - I ran out of time before the courier came.
2. The plan attached to the lease is the April version, not the revised June plan with the corrected car-park boundary.

I can go through the pages page by page first thing tomorrow. The tenant's solicitors have said they can send the director in on Friday to initial any missing pages.

Nkechi

Statement: Page 7 of the engrossed lease was not initialled by the tenant's director.""",
   0, card=FOLLOW, diff=2,
   twin=[("1. Not every page of the engrossed lease was initialled", "1. Not a single page of the engrossed lease was initialled"), (" I've flagged the bundle but I haven't yet listed which pages are missing initials - I ran out of time before the courier came.", " I've flagged the bundle.")], twin_gold=1),

it("E24", "noul",
   "Would accepting the board minutes commit a reader to the statement?",
   """Callander Retail Group - Board meeting, 18 July: minutes (extract)

Item 5: Regional performance, Q2

The Chief Operating Officer presented the regional dashboard. Revenue across the six regional offices was 2% ahead of plan for the quarter, driven by the Glasgow and Bristol offices. The dashboard for the Leeds office had not been updated since May because of the finance system migration.

The board asked whether the Leeds office had missed its Q2 targets, and whether the migration had affected any other office's figures. The COO undertook to provide final Leeds figures by 31 July.

The board noted the strong performance of the Bristol office's new homeware line and asked for a case study at the September meeting.

Action: COO to circulate final Leeds Q2 figures by 31 July.

Statement: The Leeds office missed its Q2 targets.""",
   0, card=FOLLOW, diff=1,
   twin=[("The board asked whether the Leeds office had missed its Q2 targets, and whether", "The board asked why the Leeds office had missed its Q2 targets, and whether")], twin_gold=1),

it("E25", "choice",
   "Under the school's trip policy, what is the status of Mr. Hale accompanying pupils on the April residential trip?",
   """Ashcombe Primary School - Educational Visits Policy (extract), with a note from the Visits Coordinator

4.2 Only staff and volunteers with a current enhanced DBS check may accompany pupils on residential trips. There are no exceptions, including for parents who are also governors.
4.3 On day trips, adults without a current DBS check may help if they are never left alone with pupils.
4.4 Every residential trip must have at least one first-aider among the accompanying adults.

Note from the Visits Coordinator, 10 March:
"For the Year 6 residential to Coniston (14-16 April): Mr. Hale has kindly offered to come again this year and he is a qualified first-aider, which would help with 4.4. However, his enhanced DBS check expired on 2 March and the renewal application has not yet been submitted. Renewals are currently taking about eight weeks."
""",
   "forbidden", opts=DEON, card=DEONCARD, diff=2),

it("E26", "choice",
   "Which of these statements must be true if the tasting report is accurate?",
   """Château Verlaine - Quality panel report: 2019 Reserve (all formats)

Panel: five tasters (cellar master, two winemakers, the quality manager and an external taster). The panel tasted the 2019 Reserve in all three formats held in the cellar - 75 cl bottles, magnums and a single jeroboam - over two sessions in February. The external taster arrived late to the first session, tasted only the 75 cl bottles, and missed the second session.

Findings:
- No member of the panel detected any cork taint in the 2019 Reserve, in any format or session.
- Two tasters noted slight volatile acidity in one of the magnums; this was not confirmed by the lab.
- The 2020 Reserve was also opened at the second session for comparison; notes are in a separate report.

Conclusion: the 2019 Reserve is released for the spring allocation. Magnums will be held back for a further six months pending the VA check.""",
   S26[0], opts=S26,
   card="- No panel member detected cork taint in the 2019 reserve magnums: none of the five tasters detected cork taint in the 2019 Reserve magnums\n"
        "- No panel member detected any fault at all in the 2019 reserve: none of the five tasters detected any fault of any kind in the 2019 Reserve\n"
        "- Some panel member detected cork taint in another vintage: at least one taster detected cork taint in a vintage other than 2019\n"
        "- Every panel member tasted the 2019 reserve magnums: all five tasters tasted the 2019 Reserve in magnum\n"
        "- none of these: none of the listed statements is guaranteed by the report",
   diff=2),

]
