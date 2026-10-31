"""Part B2: conditionals continued (conditional statements, rules vs facts, clause selection, chains)."""
from _h import it, L3, L3CARD, FOLLOW, E, C, U, NONE

CL = [f"clause {i}" for i in range(1, 11)] + [NONE]

ITEMS = [

it("B14", "choice",
   "Given only the recruitment update, the statement is which of these?",
   """From: Recruitment Team, Carrow & Lisle Engineering
To: Graduate Scheme Steering Group
Subject: 2027 graduate intake - interview stage update

Dear all,

The written test closed last Friday. 412 applicants sat it. As agreed at the last meeting, every applicant who passed the written test was invited to interview - 96 invitations in total so far.

In addition, following the steering group's decision on the accelerated pathway, some applicants who did not pass the written test were also invited to interview because they came through our university partnership programme with a strong project portfolio. We have flagged these candidates on the interview schedule so panels are aware.

Interview days are 3, 4 and 10 November. Please send your panel availability by Wednesday.

Kind regards,
Rosalind Achterberg, Early Careers Lead

Statement: If an applicant was invited to interview, they passed the written test.""",
   C, opts=L3[2], card=L3CARD, diff=2),

it("B15", "noul",
   "Based only on the module handbook, is the statement guaranteed?",
   """Department of Earth Sciences - Module Handbook 2026/27
GEOL2104 Field Mapping (20 credits)

Assessment: a field notebook (40%) and a mapping report (60%). The mapping report is due at 12:00 on Friday of week 9 via the online submission portal.

Late work. Late submissions of the mapping report are accepted only with a medical certificate covering the week before the deadline. Without such a certificate, a late report receives a mark of zero. Extensions are handled separately and must be approved by the module convenor before the deadline.

Academic integrity. Reports are checked for similarity. Field data may be shared within a mapping group, but interpretation and writing must be your own.

Contact: Dr. Amara Kallis (module convenor).

Statement: A late mapping report that comes with a medical certificate covering the week before the deadline is accepted.""",
   0, card=FOLLOW, diff=3),

it("B16", "choice",
   "Assuming the facilities log is correct, how should the statement be labelled?",
   """Ridgeway Data Centre - Facilities log, standby generator G2

System description (from the O&M manual, section 3): generator G2 starts automatically whenever mains power to switchboard SB-2 drops for more than 10 seconds. The start sequence does not depend on any operator action. G2 is test-run manually on the first Monday of each month.

Log entries, February:
- Mon 2 Feb 09:00 - monthly manual test run, 30 minutes, no faults.
- Wed 4 Feb 13:42 - brief flicker reported by the NOC on SB-2 lighting; UPS absorbed it. G2 did not start at any time on 4 Feb (confirmed from the controller event history).
- Fri 13 Feb 22:10 - fuel delivery, tank topped up to 95%.
- Tue 24 Feb 03:15 - G2 started automatically; ran for 41 minutes during the substation fault.

Next service due 12 March.

Statement: On 4 February, mains power to switchboard SB-2 did not drop for more than 10 seconds.""",
   E, opts=L3[3], card=L3CARD, diff=2),

it("B17", "choice",
   "Which clause of the account-control policy, applied to the case facts, guarantees that the Kimura account is frozen?",
   """Solent Crest Bank - Account Control Policy ACP-9 (numbered clauses) and case summary

1. An account is frozen only if it has been flagged by the fraud team.
2. If an account records more than five failed logins within one hour, it is frozen.
3. An account whose sole owner has died is frozen on notification.
4. If an account changes its registered address and then requests a payment above 5,000 pounds within 7 days of the change, it is frozen.
5. An account with two-factor login enabled is never frozen for failed logins alone.
6. A frozen account is unfrozen if the owner verifies their identity in a branch.
7. If the fraud team flags an account and the owner confirms the flagged transaction by phone, the account is not frozen.
8. Accounts holding more than 10,000 pounds are reviewed by a senior analyst before any freeze.
9. If a payment is requested to a new payee in a high-risk jurisdiction, the account may be frozen.
10. Business accounts are frozen only by the compliance team.

Case summary - personal account of Ms. Haruka Kimura:
- Flagged by the fraud team on 3 March.
- Three failed logins on 2 March, all within ten minutes; two-factor login not enabled.
- Registered address changed online on 1 March.
- Payment of 6,200 pounds to a new payee in a high-risk jurisdiction requested on 3 March.
- Balance: 14,800 pounds. Senior analyst review completed on 4 March.
- The owner has not responded to the bank's calls and has not visited a branch.""",
   "clause 4", opts=CL,
   card="\n".join(f"- clause {i}: the clause numbered {i} in policy ACP-9" for i in range(1, 11))
        + "\n- none of these: no clause, applied to the case facts, guarantees that the account is frozen",
   diff=3, twin=[("- Payment of 6,200 pounds to a new payee", "- Payment of 4,200 pounds to a new payee")],
   twin_gold=NONE),

it("B18", "noul",
   "If every sentence of the incident note is true, must the statement be true?",
   """Aurelian Microfab - Clean Room B, visitor incident note (draft)

Rule displayed on the airlock door and in the visitor induction: visitors may not enter Clean Room B unless they are wearing a full gown, hood and overshoes supplied at the airlock. Visitors must be escorted by a trained member of staff at all times.

Note: On Thursday 16 October, Dr. Mireille Pohl from our equipment supplier, Vantrell Systems, was booked to inspect the etch tool. Her escort, process engineer Laszlo Bartok, was delayed in a meeting. Access control records show that Dr. Pohl's temporary badge opened the Clean Room B inner door at 10:05, and she entered the room. Laszlo arrived at 10:12 and found her at the etch tool. Particle counts near the tool rose briefly at 10:07.

This note is being circulated to the site safety committee for discussion; no conclusion has been reached about what happened in the airlock.

Statement: Dr. Pohl was wearing a full gown, hood and overshoes when she entered Clean Room B.""",
   0, card=FOLLOW, diff=3),

it("B19", "choice",
   "What is the status of the statement given the park notice?",
   """Fernleigh Country Park - Notice to regular visitors (posted at the visitor centre)

West gate opening. Since the vandalism in the spring, the west gate (Mill Lane entrance) is unlocked only if a park warden is on duty. The gate is operated by the duty warden and cannot be opened remotely. The main entrance on Fernleigh Road is unaffected and remains open from 7 a.m. to dusk.

Staffing last weekend: a warden was on duty from 9 a.m. to 12 noon on Sunday. On Saturday the rota was fully staffed.

Car park. The Mill Lane car park is being resurfaced from 3 November; please use the main car park during the works.

Dogs. From 1 December dogs must be on leads in the wildflower meadow.

Thank you for your patience - The Fernleigh Ranger Team

Statement: The west gate was unlocked at some point on Sunday.""",
   U, opts=L3[4], card=L3CARD, diff=2,
   twin=[("a warden was on duty from 9 a.m. to 12 noon on Sunday.", "no warden was on duty at any time on Sunday.")],
   twin_gold=C),

it("B20", "noul",
   "Does the booking FAQ guarantee the statement?",
   """Norrland Rail - Booking FAQ (updated 1 September)

Q: Can I cancel my ticket?
A: All tickets bought through the Norrland Rail app come with free cancellation up to 15 minutes before departure. Tickets bought at a station ticket office can be cancelled for a fee of 5 euros. Tickets bought through third-party resellers follow the reseller's own terms, and some of those tickets cannot be cancelled at all.

Q: Can I change the name on a ticket?
A: No. Tickets are personal and not transferable.

Q: Do I need to print my ticket?
A: No, a QR code on your phone is enough.

Q: What if my train is cancelled?
A: You will get a full refund automatically, whatever channel you bought from.

Statement: If a Norrland Rail ticket does not come with free cancellation, it was not bought through the Norrland Rail app.""",
   1, card=FOLLOW, diff=2),

it("B21", "choice",
   "Which of these staff members definitely did not work on Saturday?",
   """From: Nadia Oduya, Duty Manager, The Copper Kettle cafe
To: Payroll
Subject: Weekend hours - please check before the payroll run

Hi,

The weekend timesheets got wet and parts are unreadable, so here is what I can reconstruct for last weekend and Monday:

- The standing rota rule is that if Tamsin works on a Saturday, Idris works the following Sunday (they share the child-care swap).
- Idris never works two days in a row; that's in his contract.
- Idris definitely worked Monday - he opened up and I have his till log.
- Greta worked at least one day over the weekend, but I can't read which.
- Oluwaseun only works on days when Greta is off.
- Bettany was on holiday all weekend and back on Tuesday.

Can you hold the weekend hours for Tamsin, Idris, Greta and Oluwaseun until I have confirmed them with each person?

Thanks,
Nadia""",
   "Tamsin",
   opts=["Idris", "Greta", "Oluwaseun", "Tamsin", NONE],
   card="- Idris: the staff member who opened up on Monday\n"
        "- Greta: the staff member who worked at least one weekend day\n"
        "- Oluwaseun: the staff member who works only when Greta is off\n"
        "- Tamsin: the staff member in the child-care swap with Idris\n"
        "- none of these: the email does not settle that any listed staff member was off on Saturday",
   diff=3),

it("B22", "choice",
   "Taking the event update as true, which inference label applies to the statement?",
   """Brackenfield Village Fete - Update from the organising committee

Dear residents,

As you know, our rule for the fete has always been that it goes ahead even if it rains - we have the marquees - but not if the Met Office wind warning for the area is amber or red, because the marquees are not rated for those winds.

We are sorry to say that the fete did not go ahead on Saturday 13 September. We know many of you had baked, grown and built things for the day, and we share your disappointment. Stallholders will receive a full refund of their pitch fee by the end of the month.

A new date will be announced once we have confirmed the field with the Brackenfield Estate. We will keep the same stall allocations.

With thanks for your understanding,
Priscilla Adeyemi, Chair, Brackenfield Fete Committee

Statement: An amber or red wind warning was in force for the area on Saturday 13 September.""",
   U, opts=L3[5], card=L3CARD, diff=3),

it("B23", "noul",
   "Does the statement follow from the shareholder circular?",
   """Harrowfield Industrial plc - Circular to shareholders (extract)

Dividend policy and audit findings

The Board confirms its policy of paying a final dividend each May. However, as set out in the 2025 Annual Report, if the external auditors identify a material weakness in internal controls, the Board may delay the final dividend until the weakness has been remediated and confirmed by the Audit Committee.

The external auditors, Pemberton Rowe LLP, have identified a material weakness relating to revenue recognition in the Castings division. A remediation plan has been approved by the Audit Committee, and the Board will meet on 28 April to consider the dividend.

Shareholders will be informed of the Board's decision through the usual regulatory channels.

By order of the Board,
T. Wainwright, Company Secretary

Statement: The Board delayed the final dividend.""",
   0, card=FOLLOW, diff=1),

it("B24", "choice",
   "Judged against the library notice and the account screen, how does the statement fare?",
   """Castleford Public Libraries - Loans and renewals (from the library website)

Automatic renewal: loans are renewed automatically on the due date unless another reader has reserved the item. Each item can be renewed automatically up to five times. You will get an email when an item is renewed.

Reservations: you can reserve any item in the catalogue for free. When a reserved item is returned, the next reader in the queue is notified.

Account screen for reader Carys Llewellyn, printed at the Riverside branch on 22 May:
- "The Salt Road" (novel) - due 21 May - status: NOT RENEWED - times renewed: 2 - overdue
- "Knitting Norwegian Patterns" - due 4 June - times renewed: 0
- Messages: none

Staff note: reader says she didn't receive any email about "The Salt Road".

Statement: No other reader had reserved "The Salt Road" when it fell due on 21 May.""",
   C, opts=L3[0], card=L3CARD, diff=2),

it("B25", "noul",
   "Assuming the tribunal rules and the clerk's note are accurate, must the statement be true?",
   """Western Regional Employment Tribunal - Practice direction PD-4 (extract)

4.1 If any member of a hearing panel declares a conflict of interest, the regional chair appoints a substitute member.
4.2 Whenever a substitute member is appointed, the hearing moves to the same day of the following week, so that the substitute has time to read the bundle.
4.3 Parties are told of any move by email at least three working days before the original hearing date.

Clerk's note, case 2206418/2026 (Onyekachi v Tallow Brothers Ltd):
The panel for the hearing listed on Tuesday 10 March was Judge Ferreira, Mr. Obi and Ms. Lindgren. On 2 March Mr. Obi declared a conflict of interest: he had worked with the respondent's HR director at a previous employer. The claimant's representative has asked whether the hearing can go ahead as planned.

Statement: The hearing in case 2206418/2026 moved to Tuesday 17 March.""",
   1, card=FOLLOW, diff=2),

it("B26", "choice",
   "Given the operations rules and the log, what must be true of flight NR211 on Friday?",
   """Northrim Air - Winter operations rules (Station: Tromsdal), and Friday's station log

Rule W-3: If the de-icing queue at departure time is longer than 30 minutes, the flight departs late or is cancelled; it never departs on time.
Rule W-5: If the operating crew runs out of duty hours before departure, the flight is cancelled.
Rule W-7: A flight that is cancelled at Tromsdal is re-accommodated on the next morning's service.

Station log, Friday 16 January:
- 06:10 Snow showers, visibility 1,200 m.
- 06:35 De-icing queue for NR211 (scheduled 07:00) measured at 45 minutes.
- 07:05 Crew duty check: the NR211 crew did not run out of duty hours.
- 09:40 Ops control confirms that NR211 was not cancelled. Passenger count 84.
- 10:15 NR213 on schedule.""",
   "it departed late",
   opts=["it departed on time", "it departed late", "it was cancelled", "the passage does not settle this"],
   card="- it departed on time: NR211 left at its scheduled time\n"
        "- it departed late: NR211 left after its scheduled time\n"
        "- it was cancelled: NR211 did not operate on Friday\n"
        "- the passage does not settle this: more than one of the other answers is consistent with the rules and the log",
   diff=2, twin=[("measured at 45 minutes.", "measured at 25 minutes.")],
   twin_gold="the passage does not settle this"),

]
