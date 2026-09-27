"""proc_longpolicy / clubs, associations, co-ops, universities and member organisations."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ mb01
# why: Terms update (from 1 Mar 2025): freeze without certificate up to 1 month; with a medical
# certificate up to 3 months. Request 12 May 2025 for 3 months with GP letter -> approve 3.
# Twin: no GP letter -> only 1 month allowed.
C("mb01", "What should the membership desk decide on the freeze request?",
"""
IRONBARK FITNESS CLUBS — MEMBERSHIP TERMS AND CONDITIONS

1. DEFINITIONS
1.1 "Membership" means a rolling monthly membership paid by direct debit.
1.2 "Freeze" means a temporary pause of the Membership during which the member may not use the clubs.
1.3 "Medical Certificate" means a letter from a doctor or physiotherapist stating that the member cannot exercise and for how long.
1.4 "Membership Year" means each 12-month period from the member's start date.
1.5 "Home Club" means the club named on the member's agreement.

2. FEES
2.1 The monthly fee is shown on your agreement and collected on the 1st of each month.
2.2 We may increase fees once a year on 30 days' notice.

4. ACCESS
4.1 Members may use any club in their tier. Peak members may use clubs at all times; off-peak members only 10:00 to 16:00 on weekdays and all day at weekends.
4.2 Children under 16 may attend only supervised junior sessions.

6. FREEZING YOUR MEMBERSHIP
6.1 You may Freeze your Membership for up to 2 months in each Membership Year, but only with a Medical Certificate.
6.2 The fee during a Freeze is £5 a month.
6.3 A Freeze starts on the 1st of a month and must be requested at least 7 days before.
6.4 Freeze periods do not count towards any minimum term.

7. CANCELLATION
7.1 You may cancel with one month's notice after any minimum term.

8. CONDUCT
8.1 We may suspend or end the Membership of anyone whose behaviour endangers staff or other members.

9. PERSONAL TRAINING
9.1 Personal training sessions are booked and paid for separately and are not affected by a Freeze.

10. CHANGES TO THESE TERMS
10.1 We may change these terms on 30 days' notice. Changes apply to requests received after they take effect.

TERMS UPDATE — effective 1 March 2025
U1. Clause 6.1 is replaced: "You may Freeze your Membership for up to 1 month in each Membership Year without giving a reason, or for up to 3 months in each Membership Year if you provide a Medical Certificate."
U2. Clauses 6.2 to 6.4 are unchanged.

FREEZE REQUEST — received 12 May 2025
Member: Tomasz Kowalczyk, peak membership, Home Club Riverside, start date 3 September 2023.
Requested: Freeze from 1 June to 31 August 2025 (3 months).
Evidence: letter from his physiotherapist stating he must not exercise for twelve weeks after knee surgery.
No other Freeze in the current Membership Year.
Desk assistant's note: "Most we've ever allowed is two months."
""",
[("approve_3_month_freeze", "The updated clause allows up to 3 months with a Medical Certificate, which he has provided, so the full request can be approved at £5 a month."),
 ("approve_1_month_only", "Without a Medical Certificate only 1 month may be frozen, so the request is approved for June only."),
 ("approve_2_months", "Clause 6.1 caps a medically certified Freeze at 2 months in each Membership Year, so June and July can be frozen at £5 a month but August cannot be."),
 ("refuse_freeze", "Clause 6.3 requires a Freeze to be requested well ahead of its start, and a request on 12 May for 1 June comes too late, so it must be refused.")],
"approve_3_month_freeze", 1,
twin=T([("Evidence: letter from his physiotherapist stating he must not exercise for twelve weeks after knee surgery.",
         "Evidence: none; he says he will be travelling for work over the summer.")], "approve_1_month_only")),

# ------------------------------------------------------------------ mb02
# why: 2025/26 regulations: penalty 10% of the mark achieved per calendar day late, max 7 days;
# extension requests must be made before the deadline. Due Mon 13 Oct 2025, submitted Wed
# 15 Oct = 2 days; extension asked after the deadline -> not valid. 68 - 2 x 6.8 = 54.4 -> 54.
# Twin: extension approved before the deadline to Wednesday -> on time -> 68.
C("mb02", "What mark should be recorded for the student's coursework?",
"""
UNIVERSITY OF MARLHAVEN — ASSESSMENT REGULATIONS (taught programmes)

SECTION 1 — DEFINITIONS
1.1 "Deadline" means the date and time published for submission of an assessment.
1.2 "Extension" means a new Deadline approved by the Extensions Panel.
1.3 "Working Day" means Monday to Friday, excluding university closure days.
1.4 "Raw Mark" means the mark awarded for the work before any penalty.

SECTION 4 — EXTENSIONS
4.1 A student may apply for an Extension of up to 7 days on grounds of illness or other serious circumstances.
4.2 An Extension request must be made before the Deadline. Requests made after the Deadline are treated as claims for extenuating circumstances, which do not remove late penalties.
4.3 The Panel decides within two Working Days.

SECTION 5 — LATE SUBMISSION (2024/25)
5.1 Work submitted after the Deadline loses 5 marks for each Working Day or part Working Day late, for up to 5 Working Days.
5.2 Work submitted more than 5 Working Days late receives a mark of zero.

SECTION 6 — ACADEMIC MISCONDUCT
6.1 Suspected plagiarism is referred to the School Academic Integrity Officer.

SECTION 7 — MARKS AND ROUNDING
7.1 Final marks are rounded to the nearest whole number, with halves rounded up.

SECTION 8 — RESITS
8.1 Resit marks are capped at 40.

SECTION 9 — PROGRESSION
9.1 Students must pass modules worth 100 credits to progress; up to 20 credits may be condoned at marks of 35 to 39.

SECTION 10 — EXTENUATING CIRCUMSTANCES
10.1 Claims are considered by the Board of Examiners and may lead to a deferred assessment, but not to removal of a late penalty.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

REGULATIONS 2025/26 — replacing Section 5 for assessments due on or after 1 September 2025
5.1 Work submitted after the Deadline loses 10% of the Raw Mark for each calendar day or part day late, for up to 7 calendar days.
5.2 Work submitted more than 7 calendar days late receives a mark of zero.

CASE — Module EC2104 (2025/26), essay 2
• Deadline: Monday 13 October 2025, 12:00.
• Submitted: Wednesday 15 October 2025, 10:40.
• Raw Mark: 68.
• The extension request was submitted on Tuesday 14 October, the day after the Deadline, citing a migraine; no Extension was granted.
• Student's email to the module leader: "I only need two days. Please record my 68."
""",
[("record_54", "Two part days late under the 2025/26 rule cost 10% of 68 each, so 68 − 13.6 = 54.4, recorded as 54."),
 ("record_58", "Two Working Days late at 5 marks each takes 68 down to 58."),
 ("record_61", "The Deadline day is not counted, so one day's 10% penalty leaves 61.2, recorded as 61."),
 ("record_68", "An Extension approved before the Deadline covered the Wednesday submission, so no penalty applies.")],
"record_54", 2,
twin=T([("The extension request was submitted on Tuesday 14 October, the day after the Deadline, citing a migraine; no Extension was granted.",
         "The extension request was submitted on Friday 10 October, before the Deadline, citing a migraine; the Panel granted an Extension to Wednesday 15 October, 12:00.")],
       "record_68")),

# ------------------------------------------------------------------ mb03
# why: Amendment (vacancies from 1 Apr 2025) puts under-occupying downsizers first, then
# overcrowded internal transfers, then the external list. June 2025 vacancy -> B.
# Twin: amendment from 1 Sep 2025 -> old order -> A (overcrowded internal transfer).
C("mb03", "To whom should the co-operative offer the vacant two-bedroom flat?",
"""
TANNERY YARD HOUSING CO-OPERATIVE — ALLOCATIONS POLICY

1. DEFINITIONS
1.1 "Internal Transfer List" means the list of existing member households asking to move to another co-op home.
1.2 "Overcrowded" means a household with more people than twice the number of bedrooms in its current home.
1.3 "Under-occupying" means a household with at least two more bedrooms than people.
1.4 "External Waiting List" means the list of non-member applicants, ranked by application date.
1.5 "Occupancy Range" for a two-bedroom flat: two to four people.

2. PRINCIPLES
2.1 Allocations are made by the Allocations Sub-committee in line with this policy and recorded in the minutes.
2.2 Every household offered a home must fall within the home's Occupancy Range.

3. PRIORITY ORDER
3.1 First: households on the Internal Transfer List that are Overcrowded, in order of the date they joined the list.
3.2 Second: other households on the Internal Transfer List.
3.3 Third: the External Waiting List.

4. REFUSALS
4.1 A household that refuses two reasonable offers is moved to the bottom of its list.

5. RENT
5.1 Rents are set by the general meeting each April.

6. DECORATION ALLOWANCE
6.1 Incoming households receive a £250 decoration allowance.

7. MEDICAL PRIORITY
7.1 A household with an urgent medical need assessed by an independent adviser may be placed at the head of its list by the Sub-committee.

8. REVIEWS
8.1 A household may ask the Management Committee to review an allocation within 14 days.
8.2 Changes to this policy apply to vacancies as stated in the change.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

AMENDMENT — agreed at the general meeting on 20 March 2025
Applies to vacancies arising on or after 1 April 2025.
A1. A new first priority is inserted before 3.1: "Households on the Internal Transfer List that are Under-occupying and wish to move to a smaller home."
A2. The existing priorities move down one place.

VACANCY — Flat 14, two bedrooms, became vacant on 6 June 2025
Candidates:
• Household A (internal): three people in a one-bedroom flat; joined the Internal Transfer List in March 2024.
• Household B (internal): two people in a four-bedroom house; joined the Internal Transfer List in May 2025 asking to downsize.
• Household C (external): four people; application date January 2021, the earliest on the External Waiting List.
Secretary's note: "C has waited the longest by far — seems only fair."
""",
[("offer_to_household_b", "Under the amendment an Under-occupying internal household wanting to downsize has first priority, and B fits the flat's Occupancy Range."),
 ("offer_to_household_a", "A is an Overcrowded internal household, which is the top priority under clause 3.1 for this vacancy."),
 ("offer_to_household_c", "Household C applied in January 2021 and has waited longest of all the candidates, and waiting time decides between applicants, so C should be offered the flat."),
 ("refer_to_general_meeting", "Competing internal priorities must go to the general meeting for a vote rather than being decided by the Sub-committee.")],
"offer_to_household_b", 2,
twin=T([("Applies to vacancies arising on or after 1 April 2025.", "Applies to vacancies arising on or after 1 September 2025.")], "offer_to_household_a")),

# ------------------------------------------------------------------ mb04
# why: 2025 amendment cuts registration lead time to 3 days for League matches only; Cup
# matches keep 7 days. Registered 2 Feb, Cup match 8 Feb = 6 days -> ineligible -> rule 9.2:
# match awarded to opponent (plus fine), no discretion. Twin: league match -> 3 days met ->
# result stands.
C("mb04", "What outcome should the league's disciplinary panel apply to Fenmoor's protest?",
"""
EASTRIDING AMATEUR FOOTBALL LEAGUE — COMPETITION RULES (2024/25 season)

RULE 1 — DEFINITIONS
1.1 "League Match" means a fixture in any division of the League.
1.2 "Cup Match" means a fixture in the County Cup, which the League administers under these Rules.
1.3 "Registered" means the player's registration form has been received and approved by the League Secretary.
1.4 "Ineligible Player" means a player who takes part in a match without being Registered in time.

RULE 5 — PLAYER REGISTRATION
5.1 A player must be Registered at least 7 days before a match in which he or she plays.
5.2 Registrations close on 31 March.
5.3 A player may be Registered with only one club at a time.

RULE 6 — KIT AND EQUIPMENT
6.1 Shin guards are compulsory. Home clubs change shirts if the colours clash.

RULE 9 — INELIGIBLE PLAYERS
9.1 A club that fields an Ineligible Player is fined £50.
9.2 In addition, the match is awarded to the opponent by a score of 3–0, or by the actual score if greater. The panel has no discretion to order a replay.
9.3 Protests must be lodged within 48 hours of the match.

RULE 11 — POSTPONEMENTS
11.1 Matches may be postponed for waterlogged pitches on the referee's decision.

RULE 12 — DISCIPLINE
12.1 Five cautions in a season lead to a one-match suspension.

RULE 13 — REFEREES
13.1 Referees are appointed by the Referees' Secretary. Clubs pay match fees on the day.

RULE 14 — APPEALS
14.1 A club may appeal a panel decision to the Appeals Board within 7 days, on a point of rule only.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

MANAGEMENT COMMITTEE AMENDMENT — effective 1 January 2025
"In Rule 5.1, for League Matches only, '7 days' is replaced by '3 days'. Rule 5.1 continues unchanged for Cup Matches."

PROTEST FILE — lodged by Fenmoor Rovers on 9 February 2025
Fixture: County Cup second round, Holmby Town v Fenmoor Rovers, Saturday 8 February 2025. Result: Holmby 2, Fenmoor 1.
Complaint: Holmby's goalkeeper, Callum Reyes, was not Registered in time.
League Secretary's record: Reyes's registration received and approved on Sunday 2 February 2025.
Holmby's response: "An honest mistake, first time it's happened to us. Please just fine us."
""",
[("award_match_to_fenmoor", "Cup Matches still need 7 days' registration and Reyes had 6, so he was an Ineligible Player: the match goes to Fenmoor and Holmby is fined."),
 ("result_stands", "Reyes was Registered at least the number of days before the match that the rules require for this fixture, so the result stands."),
 ("order_replay", "A registration error by the home side should not decide a cup tie on paper, so the panel should order the match to be replayed with eligible players only."),
 ("fine_only_first_offence", "As this is Holmby's first offence, the panel may fine the club £50 under Rule 9.1 and let the 2–1 result stand without awarding the match.")],
"award_match_to_fenmoor", 2,
twin=T([("Fixture: County Cup second round, Holmby Town v Fenmoor Rovers", "Fixture: Division One League Match, Holmby Town v Fenmoor Rovers")], "result_stands")),

# ------------------------------------------------------------------ mb05
# why: amendment (applications submitted on/after 1 Apr 2025) removes deemed approval; an
# undecided application lapses after 45 days and the owner may appeal to the Board. Submitted
# 1 May 2025 -> no deemed approval -> may not build; appeal to Board.
# Twin: submitted 1 Mar 2025 -> old rule -> deemed approved after 45 days (15 Apr).
C("mb05", "Can the owner go ahead and build the fence?",
"""
WILLOWMERE HOMEOWNERS ASSOCIATION — ARCHITECTURAL GUIDELINES

ARTICLE 1 — DEFINITIONS
1.1 "Committee" means the Architectural Review Committee.
1.2 "Application" means a complete request for approval, with plans and materials, filed with the Committee.
1.3 "Rear Fence" means a fence behind the front building line of a lot.

ARTICLE 2 — APPROVAL REQUIRED
2.1 No owner may build or alter any fence, wall, shed or exterior structure without the Committee's written approval.

ARTICLE 3 — FENCES
3.1 Rear Fences may be up to 1.8 m high, in timber or black metal.
3.2 Front fences may not exceed 1.0 m.
3.3 Chain-link fencing is not permitted.

ARTICLE 4 — PROCEDURE
4.1 The Committee decides each Application within 45 days of filing.
4.2 If the Committee does not decide within 45 days, the Application is deemed approved.
4.3 Decisions are sent to the owner in writing.

ARTICLE 5 — ENFORCEMENT
5.1 Unapproved structures may be removed at the owner's cost after 30 days' notice.
5.2 Fines of up to $100 a week may be imposed for continuing breaches.

ARTICLE 6 — COLOURS
6.1 Exterior paint colours must be chosen from the approved palette.

ARTICLE 7 — CONTRACTORS
7.1 Contractors may work only between 8 a.m. and 6 p.m. on weekdays and 9 a.m. and 1 p.m. on Saturdays.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

ARTICLE 8 — AMENDMENTS
8.1 The Board may amend these Guidelines by resolution. A resolution applies from the date it states.

BOARD RESOLUTION 2025-2 — adopted 18 March 2025
Applies to Applications filed on or after 1 April 2025.
R1. Article 4.2 is replaced: "If the Committee does not decide within 45 days, the Application lapses. The owner may appeal to the Board, which will decide within 30 days. No approval is implied by the Committee's silence."
R2. Articles 4.1 and 4.3 are unchanged.

OWNER FILE — Lot 88, 14 Heron Way (owner: Amaka Duru)
• Application for a 1.5 m timber Rear Fence filed on 1 May 2025, with plans and a sample of the stain.
• No response from the Committee. The Committee chair has been abroad since April.
• Today is 30 June 2025.
• Neighbour at Lot 87 emailed the owner: "Sixty days with no answer — you're approved by default, go ahead."
""",
[("no_build_appeal_to_board", "The Application was filed after Resolution 2025-2 took effect, so silence means it has lapsed; the owner should appeal to the Board, not build."),
 ("deemed_approved_may_build", "The Committee failed to decide within 45 days, so the Application is deemed approved and the fence may be built."),
 ("may_build_within_height_limit", "A 1.5 m timber Rear Fence is within Article 3.1, so it needs no approval."),
 ("application_refused", "An Application that the Committee does not decide within 45 days is treated as refused, so the owner must start again with a fresh Application before building.")],
"no_build_appeal_to_board", 2,
twin=T([("filed on 1 May 2025, with plans and a sample of the stain", "filed on 1 March 2025, with plans and a sample of the stain")], "deemed_approved_may_build")),

# ------------------------------------------------------------------ mb06
# why: amended bylaw 8.3 (from 1 Jul 2025): nominations at least 28 days before the AGM.
# AGM 30 Nov 2025; nomination 5 Nov = 25 days -> late -> invalid. Proposer and seconder are
# Full Members of 12+ months. Twin: received 31 Oct = 30 days -> valid.
C("mb06", "Is the nomination for club treasurer valid?",
"""
BRAMBLEHURST ROWING CLUB — BYLAWS (as amended)

PART 1 — DEFINITIONS
1.1 "Full Member" means an adult member with rowing rights who has paid the current subscription. Associate, Social and Junior members are not Full Members.
1.2 "Standing" means continuous Full Membership, counted to the date the nomination is received.
1.3 "AGM" means the Annual General Meeting, held in November.
1.4 "Secretary" means the Honorary Secretary of the Club.

PART 5 — SUBSCRIPTIONS
5.1 Subscriptions are due on 1 April. Members more than 60 days in arrears lose voting rights until they pay.

PART 7 — COMMITTEE
7.1 The Committee comprises the Captain, Secretary, Treasurer and four ordinary members.
7.2 Officers serve for two years and may stand again.

PART 8 — ELECTIONS
8.1 Any Full Member may stand for election to the Committee.
8.2 Each nomination must be signed by a proposer and a seconder, each a Full Member of at least 12 months' Standing, and by the candidate.
8.3 Nominations must be received by the Secretary at least 21 days before the AGM.
8.4 Where only one valid nomination is received for a post, the candidate is elected unopposed.
8.5 Late or invalid nominations cannot be accepted by the AGM.

PART 9 — GENERAL MEETINGS
9.1 Notice of the AGM is given at least 35 days in advance.
9.2 The quorum is 20 Full Members.

PART 10 — BOATS AND EQUIPMENT
10.1 Club boats may be used only by members who have passed the capsize test.
10.2 Damage must be reported to the Boatman within 24 hours.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

PART 11 — AMENDMENTS
11.1 Bylaws may be amended by a two-thirds majority at a general meeting.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

AMENDMENT — passed at a special general meeting, effective 1 July 2025
"In bylaw 8.3, '21 days' is replaced by '28 days'."

ELECTION FILE — AGM on Sunday 30 November 2025
Post: Treasurer. Candidate: Hollis Grant (Full Member since 2019).
Nomination received by the Secretary: 5 November 2025.
Proposer: Rhea Saltonstall, Full Member since 2016.
Seconder: Patrick Dunne, Full Member since March 2022.
Other nominations for Treasurer: none.
Current Treasurer's comment: "Hollis would be excellent. The club's always accepted nominations up to three weeks out."
""",
[("nomination_invalid_late", "The amended bylaw needs nominations 28 days before the AGM, and 5 November is only 25 days before, so the nomination cannot be accepted."),
 ("nomination_valid", "The nomination arrived in time and both signatories are Full Members of more than 12 months' Standing, so it is valid."),
 ("nomination_invalid_seconder", "The seconder has not held Full Membership long enough to sign a nomination."),
 ("refer_to_agm_vote", "Where only one candidate stands for a post, the AGM may vote to accept the nomination despite an irregularity, so the matter should go to the meeting.")],
"nomination_invalid_late", 1,
twin=T([("Nomination received by the Secretary: 5 November 2025.", "Nomination received by the Secretary: 31 October 2025.")], "nomination_valid")),

# ------------------------------------------------------------------ mb07
# why: Council resolution (CPD years from 1 Jan 2025): 35 hours total, at least 15 Structured.
# 2025 log: Structured 12, reading 25 -> total 37 >= 35 but Structured 12 < 15 -> non-
# compliant. Carry-forward counts only toward the total. Twin: Structured 16 -> compliant.
C("mb07", "What is the member's CPD compliance status for 2025?",
"""
INSTITUTE OF APPLIED ACOUSTICS — CONTINUING PROFESSIONAL DEVELOPMENT (CPD) REGULATIONS

1. DEFINITIONS
1.1 "CPD Year" means 1 January to 31 December.
1.2 "Structured CPD" means learning with defined objectives and an organiser, such as courses, conferences, and webinars that include an assessment or reflection record.
1.3 "Unstructured CPD" means self-directed learning, such as reading journals or technical standards.
1.4 "Carry-forward" means hours above the annual total from the previous CPD Year.

2. REQUIREMENT
2.1 Members must complete at least 30 hours of CPD in each CPD Year, of which at least 10 hours must be Structured CPD.
2.2 Up to 5 Carry-forward hours may count towards the annual total, but never towards the Structured CPD minimum.

3. RECORDS
3.1 Members log CPD online by 31 January following the CPD Year.
3.2 The Institute samples 10% of records for audit.

4. EXEMPTIONS
4.1 Members on parental leave, long-term sick leave or career breaks may apply for a reduced requirement.

5. NON-COMPLIANCE
5.1 A member who does not meet the requirement is given 3 months to make up the shortfall before any sanction.

6. FEES
6.1 Annual subscription is payable on 1 January; late payment adds £25.

7. REINSTATEMENT
7.1 Lapsed members must complete 35 hours of CPD, including 15 Structured, before reinstatement.

8. MENTORING
8.1 Hours spent mentoring junior members count as Unstructured CPD.

9. DECLARATIONS
9.1 Members declare compliance when renewing their subscription. A false declaration is a disciplinary matter.

10. CATEGORIES OF MEMBERSHIP
10.1 These Regulations apply to Members (MIAA) and Fellows (FIAA). Retired members are exempt.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

COUNCIL RESOLUTION 2024/9 — applies to CPD Years starting on or after 1 January 2025
R1. In regulation 2.1, "30 hours" is replaced by "35 hours" and "10 hours" is replaced by "15 hours".
R2. Regulation 2.2 is unchanged.

MEMBER RECORD — Dr Selin Aksoy, MIAA
2025 CPD log (submitted 20 January 2026):
• Structured CPD: 12 hours (two-day noise-mapping course, 12 hours with an assessment).
• Unstructured CPD: 25 hours (journal reading and standards review).
• Carry-forward from 2024: 5 hours.
No exemption applied for.
Member's covering note: "42 hours in total including carry-forward — well over the requirement."
""",
[("non_compliant_structured_shortfall", "Under the 2025 rules the total of 37 hours is enough, but 12 Structured hours fall short of the 15 required, so she has a shortfall to make up."),
 ("compliant", "The member met both the total and Structured CPD minimums that apply to the 2025 CPD Year."),
 ("non_compliant_total_hours", "Excluding carry-forward the member logged fewer than 35 hours, so the total requirement is not met."),
 ("compliant_using_carry_forward", "Carry-forward hours can be added to either category, so the 5 hours from 2024 lift the Structured total from 12 to 17, which is above the new 15-hour minimum.")],
"non_compliant_structured_shortfall", 2,
twin=T([("Structured CPD: 12 hours (two-day noise-mapping course, 12 hours with an assessment).",
         "Structured CPD: 16 hours (two-day noise-mapping course, 12 hours with an assessment; two assessed webinars, 4 hours).")],
       "compliant")),

# ------------------------------------------------------------------ mb08
# why: Guest update (from 1 Jun 2025): guests attending a booked meeting room do not count
# toward the 2 free guests. 5 guests, 3 in a booked meeting room -> 2 counted -> free. The
# front-desk instruction is not part of the terms.
C("mb08", "What guest charge, if any, should be applied to the member's visit?",
"""
FOUNDRY LANE COWORK — MEMBERSHIP TERMS

1. DEFINITIONS
1.1 "Member" means a person holding a current resident or flexi membership.
1.2 "Guest" means a person who is not a Member and is signed in by a Member.
1.3 "Meeting Room Booking" means a booking of a meeting room made in the app and paid for or taken from the Member's credits.
1.4 "Day" means one calendar day.

2. ACCESS
2.1 Resident Members have 24-hour access. Flexi Members may use the space 08:00 to 20:00 on weekdays.
2.2 Members must not share access fobs.

3. GUESTS
3.1 Each Member may sign in up to 2 Guests per Day free of charge.
3.2 Additional Guests are charged at £15 per Guest per Day, added to the Member's next invoice.
3.3 Members are responsible for their Guests' behaviour.
3.4 Guests must sign in at the front desk and wear a visitor badge.

4. MEETING ROOMS
4.1 Resident Members receive 8 hours of meeting-room credit a month.

5. KITCHEN AND NOISE
5.1 Phone calls should be taken in the phone booths, not at hot desks.

6. POST
6.1 Post is held at the front desk for 30 days.

7. EVENTS
7.1 Members may host evening events in the lounge with the community manager's approval. Event guests are covered by the event booking, not by clause 3.

8. BILLING
8.1 Charges are invoiced monthly in arrears. Front-desk staff record guests; they do not set charges.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

GUEST POLICY UPDATE — effective 1 June 2025
G1. Guests who attend only a Meeting Room Booking made by the Member do not count towards the 2 free Guests in clause 3.1 and are not charged.
G2. Clause 3.2 applies to other Guests above 2.

VISIT RECORD — Tuesday 8 July 2025
Member: Oriane Dufresne (resident).
Guests signed in: 5.
• 3 Guests attended only her Meeting Room Booking in Room B, 10:00 to 12:00 (booked in the app, paid by credits).
• 2 Guests worked with her at the hot desks in the afternoon.

FRONT DESK MEMO, pinned at reception
"Charge every guest beyond two per member — manager's orders, no exceptions for meeting rooms."
""",
[("no_guest_charge", "Meeting-room Guests do not count under the June update, leaving 2 counted Guests, which are free."),
 ("charge_45", "Five Guests is three more than the free allowance, so three are charged at £15."),
 ("charge_15", "After the meeting-room Guests are set aside, one Guest is above the allowance and is charged £15."),
 ("charge_75", "Every Guest is charged £15 when a Member brings more than two in a Day.")],
"no_guest_charge", 1),

# ------------------------------------------------------------------ mb09
# why: 2026 admissions arrangements (applications for entry in Sep 2026) define Sibling to
# include a step-sibling living at the same address. Applicant's step-brother attends and
# lives at the same address -> criterion 2 (sibling). Twin: step-brother lives at another
# address -> not a Sibling -> falls to distance (criterion 4).
C("mb09", "Under which oversubscription criterion should the application be ranked?",
"""
HALVERN ACADEMY TRUST — ADMISSIONS ARRANGEMENTS FOR ELMSTEAD PRIMARY

1. DEFINITIONS
1.1 "Sibling" means a brother or sister, half-brother or half-sister, or adopted sibling, living at the same address as the applicant and attending the school at the time of admission.
1.2 "Home Address" means the address where the child normally lives on the closing date for applications.
1.3 "Distance" means the straight-line distance from the Home Address to the school's main gate.
1.4 "Catchment Area" means the area shown on the map in Appendix A.

2. PUBLISHED ADMISSION NUMBER
2.1 Reception class: 60 places.

3. OVERSUBSCRIPTION CRITERIA
3.1 Criterion 1: looked-after and previously looked-after children.
3.2 Criterion 2: children with a Sibling at the school.
3.3 Criterion 3: children living in the Catchment Area.
3.4 Criterion 4: all other children, by Distance, nearest first.

4. TIE-BREAK
4.1 Within each criterion, Distance decides; if equal, lots are drawn by an independent person.

5. WAITING LISTS
5.1 Waiting lists are kept until 31 December of the admission year.

6. APPEALS
6.1 Parents refused a place may appeal to an independent panel.

7. IN-YEAR ADMISSIONS
7.1 Applications for other year groups are made directly to the school and decided within 15 school days.

8. EVIDENCE
8.1 The school may ask for proof of Home Address, such as a council tax bill, and may withdraw an offer obtained by a false address.

9. TWINS AND MULTIPLE BIRTHS
9.1 Where one twin is offered a place, the other is admitted even if this takes the school above its admission number.

REVIEW OF THIS DOCUMENT
This document is reviewed at least every two years by its owner. Suggestions for improvement can be sent to the policy team at any time; they do not change the document until formally adopted.

DETERMINED ARRANGEMENTS FOR 2026 ENTRY — applying to applications for entry in September 2026
D1. In the definition of Sibling, after "adopted sibling" insert "or step-brother or step-sister".
D2. The other definitions and criteria are unchanged.

APPLICATION REC-2026-0371 — entry September 2026
Child: Ellie Brandt. Home Address: 22 Farrow Lane (outside the Catchment Area), 1.3 km from the gate.
Connection: step-brother Noah Pike, in Year 3 at Elmstead and expected to still attend in September 2026; he lives at 22 Farrow Lane with Ellie, her mother and his father.
Looked-after status: no.
Admissions officer's note: "Step-siblings never used to count — distance only?"
""",
[("criterion_2_sibling", "The 2026 arrangements count a step-brother at the same address as a Sibling, so Ellie ranks under criterion 2."),
 ("criterion_4_distance", "Ellie has no Sibling as the arrangements for her entry year define it and lives outside the Catchment Area, so she ranks by Distance under criterion 4."),
 ("criterion_3_catchment", "Living 1.3 km from the gate places Ellie within the Catchment Area, criterion 3."),
 ("criterion_1_priority", "Children in blended families are treated as previously looked-after for criterion 1.")],
"criterion_2_sibling", 1,
twin=T([("he lives at 22 Farrow Lane with Ellie, her mother and his father", "he lives with his mother at 5 Cressy Road, not with Ellie")], "criterion_4_distance")),

# ------------------------------------------------------------------ mb10
# why: Rules update (from 1 Mar 2025) requires two non-cultivation notices at least 28 days
# apart, and termination only if the plot is still uncultivated 28 days after the second.
# Only one notice (1 Jun) issued; termination on 20 Jun is premature -> issue second notice.
C("mb10", "What should the allotment committee do about plot 23?",
"""
ASHCOMBE ALLOTMENT SOCIETY — TENANCY RULES

RULE 1 — DEFINITIONS
1.1 "Plot Holder" means the member named on the tenancy agreement for a plot.
1.2 "Cultivated" means at least 75% of the plot is used for growing crops, flowers or fruit, and kept reasonably free of weeds.
1.3 "Non-cultivation Notice" means a written notice from the committee, following an inspection, telling the Plot Holder that the plot is not Cultivated.

RULE 4 — USE OF PLOTS
4.1 Plots may be used only for growing produce for the Plot Holder's household.
4.2 Sheds up to 1.8 m by 1.2 m are permitted without consent.
4.3 Bonfires are not permitted between April and September.

RULE 6 — INSPECTIONS
6.1 The committee inspects all plots in March, June and September.
6.2 Plot Holders are told of the inspection result within 7 days.

RULE 7 — ENDING A TENANCY FOR NON-CULTIVATION
7.1 If a plot is not Cultivated, the committee issues a Non-cultivation Notice.
7.2 If the plot is still not Cultivated 14 days after the notice, the committee may end the tenancy.

RULE 8 — RENT
8.1 Rent is £45 a year for a full plot, due on 1 October.

RULE 9 — WATER
9.1 Hoses are not permitted; water from the troughs by can only.

RULE 10 — APPEALS
10.1 A Plot Holder may appeal a decision to end a tenancy to a panel of three members not on the committee.

RULE 11 — CHANGES TO THE RULES
11.1 These Rules may be changed at an AGM. Changes apply from the date stated.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

RULES UPDATE — adopted at the AGM, effective 1 March 2025
U1. Rule 7.2 is replaced: "If the plot is still not Cultivated, the committee must issue a second Non-cultivation Notice no sooner than 28 days after the first. The tenancy may be ended only if the plot is still not Cultivated 28 days after the second notice."
U2. Rule 7.1 is unchanged.

PLOT 23 FILE — Plot Holder: Gideon Farrell
• June inspection (28 May 2025): about 30% Cultivated; rest overgrown.
• First Non-cultivation Notice issued: 1 June 2025.
• Re-inspection 18 June 2025: no change.
• Committee secretary's draft letter: "Your tenancy ends on 20 June 2025 for failure to cultivate."
• Waiting list: 14 people.
""",
[("issue_second_notice", "The update requires a second notice at least 28 days after the first, so the committee may issue it from 29 June and cannot end the tenancy on 20 June."),
 ("end_tenancy_20_june", "More than 14 days have passed since the Non-cultivation Notice with no improvement, so the tenancy can end on 20 June."),
 ("end_tenancy_29_june", "Under the update the committee must wait 28 days after the first notice, so the tenancy cannot end on 20 June but can be ended on 29 June if the plot is still uncultivated."),
 ("take_no_action", "A plot 30% Cultivated meets the standard in Rule 1.2, so no action is needed.")],
"issue_second_notice", 2),

# ------------------------------------------------------------------ mb11
# why: 2026-season rule change: LOA includes bowsprit. 9.6 + 0.8 = 10.4 m > 10 m berth max ->
# must move to a 12 m berth at £350/m: 10.4 x 350 = £3,640.
# Twin: bowsprit 0.3 m -> LOA 9.9 m -> 10 m berth at £320/m: 9.9 x 320 = £3,168.
C("mb11", "Which berth and annual fee should the harbour office confirm for the 2026 season?",
"""
PORTHALLOW MARINA — BERTH HOLDER REGULATIONS

1. DEFINITIONS
1.1 "LOA" (length overall) means the length of the hull from stem to stern, excluding bowsprits, pulpits, bathing platforms and outboard brackets.
1.2 "Season" means 1 April to 31 March.
1.3 "Berth Class" means the maximum LOA a berth can take: 8 m, 10 m or 12 m.
1.4 "Berth Holder" means the person named on the annual berthing agreement.

2. BERTH ALLOCATION
2.1 A vessel may occupy only a berth whose Berth Class is equal to or greater than its LOA.
2.2 If a vessel does not fit its current Berth Class, the harbour office will move it to the smallest Berth Class it fits.

3. FEES (per metre of LOA per Season)
3.1 8 m berths: £290. 10 m berths: £320. 12 m berths: £350.
3.2 Fees are payable in advance on 1 April; a 3% discount applies to payment by 1 March.

4. INSURANCE
4.1 Third-party insurance of at least £3 million is required.

5. SAFETY
5.1 Gas installations must have a current safety certificate.
5.2 Refuelling at berths is prohibited.

6. LIVE-ABOARD
6.1 Living aboard for more than 60 nights a Season requires the harbour master's consent.

7. MEASUREMENT
7.1 The harbour office may measure any vessel. Measurements are rounded to the nearest 0.1 m.

8. TRANSFERS
8.1 Berths cannot be sold or transferred with a vessel.

ACCESSIBILITY
This document is available in large print, audio and easy-read formats on request. Anyone who needs help to understand it, or to take part in a process it describes, may ask for reasonable adjustments.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

RULE CHANGE — effective from the 2026 Season (1 April 2026)
RC1. In definition 1.1, the words "bowsprits, pulpits, bathing platforms and outboard brackets" are replaced by "pulpits and bathing platforms". Bowsprits and outboard brackets are therefore included in LOA.
RC2. Fees per metre are unchanged.

BERTH HOLDER RECORD — "Kittiwake", berth C-17 (10 m Berth Class)
• Hull length stem to stern: 9.6 m. Fixed bowsprit: 0.8 m beyond the stem. No outboard bracket.
• 2025 Season fee paid: £3,072 (9.6 m × £320).
• Renewal for the 2026 Season requested on 15 February 2026; payment to follow on 1 April.
• Berth holder's email: "Same boat, same berth, same fee as last year please."
""",
[("move_to_12m_berth_3640", "From 2026 the bowsprit counts, making LOA 10.4 m, too long for a 10 m berth, so the boat moves to a 12 m berth at 10.4 × £350 = £3,640."),
 ("keep_10m_berth_3072", "LOA is the hull length of 9.6 m, which fits the 10 m berth at 9.6 × £320 = £3,072."),
 ("keep_10m_berth_3328", "LOA is now 10.4 m, charged at the 10 m rate in the existing berth: 10.4 × £320 = £3,328."),
 ("move_to_12m_berth_3360", "The boat must move to a 12 m berth, charged on the 9.6 m hull: 9.6 × £350 = £3,360."),
 ("keep_10m_berth_3168", "Measured with the bowsprit the boat is 9.9 m, so it fits the 10 m berth at 9.9 × £320 = £3,168.")],
"move_to_12m_berth_3640", 3,
twin=T([("Fixed bowsprit: 0.8 m beyond the stem.", "Fixed bowsprit: 0.3 m beyond the stem.")], "keep_10m_berth_3168")),

# ------------------------------------------------------------------ mb12
# why: tax-year thresholds reset on 6 April. March 2025 (2024/25): 9,700 prior miles -> 300 at
# 45p = 135 + 100 at 25p = 25 -> 160. April journeys (7-28 April) fall in the new 2025/26 Tax
# Year: cumulative resets, new 50p rate: 300 x 0.50 = 150. Total 310.
C("mb12", "How much should the charity reimburse the volunteer for March and April driving?",
"""
CASTLEWELL COMMUNITY TRANSPORT — VOLUNTEER DRIVER EXPENSES POLICY

1. DEFINITIONS
1.1 "Tax Year" means 6 April to the following 5 April.
1.2 "Business Miles" means miles driven in the volunteer's own car on journeys booked by the scheme, including the journey to the first passenger and home from the last.
1.3 "Cumulative Miles" means Business Miles already claimed in the same Tax Year.

2. MILEAGE RATES
2.1 Business Miles are reimbursed at 45p per mile for the first 10,000 Cumulative Miles in a Tax Year and 25p per mile after that.
2.2 A passenger supplement of 5p per mile per passenger is not paid by this scheme.

3. CLAIMS
3.1 Claims are made monthly on the mileage form and must list each journey.
3.2 Claims more than three months old are not paid.

4. PARKING AND TOLLS
4.1 Parking and toll charges are reimbursed at cost with receipts. Fines are never reimbursed.

5. INSURANCE
5.1 Volunteers must tell their insurer that they drive for the scheme. The scheme does not reimburse any premium increase.

6. SAFEGUARDING
6.1 Drivers must hold a current enhanced background check.

7. CHANGES TO RATES
7.1 The trustees review rates each spring. Changes normally take effect from the start of a Tax Year.

8. PAYMENTS
8.1 Claims are paid by bank transfer on the 15th of the month after submission.

ACCESSIBILITY
This document is available in large print, audio and easy-read formats on request. Anyone who needs help to understand it, or to take part in a process it describes, may ask for reasonable adjustments.

REVIEW OF THIS DOCUMENT
This document is reviewed at least every two years by its owner. Suggestions for improvement can be sent to the policy team at any time; they do not change the document until formally adopted.

TRUSTEES' DECISION — 12 March 2025
"From the start of the 2025/26 Tax Year, the rate for the first 10,000 Cumulative Miles in clause 2.1 is 50p. The 25p rate above 10,000 miles is unchanged. Journeys in earlier Tax Years are paid at the old rates."

CLAIM — volunteer driver Wendell Osei, submitted 2 May 2025
• Cumulative Miles in the 2024/25 Tax Year before March: 9,700.
• March 2025 journeys (all between 3 and 31 March): 400 Business Miles.
• April 2025 journeys (all between 7 and 28 April): 300 Business Miles.
• Parking: none.
Scheme coordinator's note: "Wendell's done loads of miles — just pay the new 50p rate on everything to keep it simple."
""",
[("pay_310", "March falls under the old rates: 300 miles at 45p and 100 at 25p make £160; April starts a new Tax Year at 50p, adding £150, total £310."),
 ("pay_330", "March at 45p (£180) and April at 50p (£150) gives £330."),
 ("pay_350", "All 700 miles at the new 50p rate gives £350."),
 ("pay_235", "March gives £160, and because Cumulative Miles passed 10,000 during March, the whole of April's 300 miles is paid at the 25p rate (£75), making £235 in total.")],
"pay_310", 3),

# ------------------------------------------------------------------ mb13
# why: Handbook update (events from 1 Sep 2025): grant up to 60% of costs, max £600;
# applications 14 days before. Event 24 Oct, applied 8 Oct = 16 days -> in time.
# 60% x 900 = 540 <= 600 -> £540. Twin: costs £1,200 -> 60% = 720 -> capped at £600.
C("mb13", "What event grant should the Students' Union award?",
"""
MARLHAVEN STUDENTS' UNION — SOCIETIES HANDBOOK, SECTION 6: FUNDING

6.1 DEFINITIONS
(a) "Eligible Costs" means venue hire, equipment hire, speaker travel and publicity. Food, alcohol and prizes are not Eligible Costs.
(b) "Event Date" means the first day of the event.
(c) "Affiliated Society" means a society that has completed its annual re-affiliation.

6.2 EVENT GRANTS
(a) Affiliated Societies may apply for a grant towards the Eligible Costs of an event open to all students.
(b) The grant is up to 50% of Eligible Costs, to a maximum of £500 per event.
(c) Applications must be received at least 21 days before the Event Date.
(d) Grants are paid on receipt of invoices after the event.

6.3 EQUIPMENT FUND
(a) Societies may apply once a year for up to £300 towards equipment that remains Union property.

6.4 TRAVEL GRANTS
(a) Competitive societies may claim 30% of travel costs to fixtures.

6.5 SPONSORSHIP
(a) External sponsorship must be approved by the Union's commercial team before it is announced.

6.6 CHANGES
(a) Changes to this section apply to events whose Event Date falls on or after the date stated in the change.

6.7 CLAIMS
(a) Invoices must be in the Union's name and submitted within 30 days after the event.
(b) Grants cannot be paid in advance.

6.8 LIMITS
(a) A society may receive no more than three event grants per academic year.

6.9 ACCESSIBILITY
(a) Events funded by the Union must be held in accessible venues.
(b) Accessibility costs, such as interpreters, are Eligible Costs.

ACCESSIBILITY
This document is available in large print, audio and easy-read formats on request. Anyone who needs help to understand it, or to take part in a process it describes, may ask for reasonable adjustments.

REVIEW OF THIS DOCUMENT
This document is reviewed at least every two years by its owner. Suggestions for improvement can be sent to the policy team at any time; they do not change the document until formally adopted.

HANDBOOK UPDATE — approved by the Finance Committee, applying to events on or after 1 September 2025
U1. In 6.2(b), "50%" is replaced by "60%" and "£500" by "£600".
U2. In 6.2(c), "21 days" is replaced by "14 days".

APPLICATION — Astronomy Society (Affiliated Society, re-affiliated September 2025)
Event: public stargazing evening with a visiting speaker, open to all students. Event Date: Friday 24 October 2025.
Application received: Wednesday 8 October 2025.
Eligible Costs: telescope hire and speaker travel, total £900.
Also budgeted: pizza for attendees, £150.
Society treasurer's note: "We're asking for the maximum."
""",
[("grant_540", "The update applies, the application came 16 days ahead, and 60% of £900 Eligible Costs is £540, below the £600 cap."),
 ("grant_450", "The grant is 50% of £900 Eligible Costs, which is £450."),
 ("refuse_late_application", "Clause 6.2(c) requires applications at least 21 days before the Event Date, and the Astronomy Society applied only 16 days before, so the grant must be refused."),
 ("grant_600", "Sixty per cent of the Eligible Costs exceeds the cap, so the grant is limited to £600."),
 ("grant_630", "Sixty per cent of all budgeted costs of £1,050 gives £630.")],
"grant_540", 2,
twin=T([("telescope hire and speaker travel, total £900", "telescope hire and speaker travel, total £1,200")], "grant_600")),
]
