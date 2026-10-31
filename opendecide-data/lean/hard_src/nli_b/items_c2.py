"""Part C2: modals continued (deontic vs physical modality, permissions, expectations, authority)."""
from _h import it, L3, L3CARD, FOLLOW, CONSIST, E, C, U, NONE

DEON = ["required", "permitted but not required", "forbidden", "the passage does not settle this"]
DEONCARD = ("- required: the rules say it must be done\n"
            "- permitted but not required: the rules allow it and also allow not doing it\n"
            "- forbidden: the rules say it must not be done\n"
            "- the passage does not settle this: the rules quoted do not fix whether it is required, permitted or forbidden")

S14 = ["Someone propped the stairwell fire door open on Tuesday",
       "The stairwell fire door was locked from the corridor side on Tuesday",
       "A visitor used the stairwell during the Tuesday drill",
       "The stairwell fire door alarm was switched off on Tuesday",
       "Somebody smoked in the stairwell on Tuesday",
       NONE]

ITEMS = [

it("C14", "choice",
   "Which of these statements is ruled out by the building information?",
   """Pellbridge House - Building information for tenants (Level 3 stairwell)

The Level 3 stairwell fire door (door 3F) opens outward from the corridor into the stairwell. Its hardware was replaced in January:
- Door 3F has a push bar on the corridor side and no lock or key cylinder on the corridor side. It cannot be locked from the corridor side by any means; it can only be deadlocked from the stairwell side, using the fire officer's key.
- The door is fitted with a hold-open magnet linked to the fire alarm.

House rules for the stairwell:
- Staff must not prop door 3F open with wedges or furniture.
- Smoking is not allowed anywhere in the building, including the stairwells.
- Visitors should use the lifts rather than the stairs, except in an emergency or a drill.
- The door alarm may be switched off only by the facilities manager.

Facilities log, Tuesday: fire drill at 11:00; building evacuated in 6 minutes. Door 3F checked at 11:20 and found in order.""",
   S14[1], opts=S14,
   card="- Someone propped the stairwell fire door open on Tuesday: door 3F was wedged or held open by a person at some point on Tuesday\n"
        "- The stairwell fire door was locked from the corridor side on Tuesday: door 3F was locked using something on its corridor side on Tuesday\n"
        "- A visitor used the stairwell during the Tuesday drill: at least one visitor used the Level 3 stairs during the drill\n"
        "- The stairwell fire door alarm was switched off on Tuesday: the door 3F alarm was off at some point on Tuesday\n"
        "- Somebody smoked in the stairwell on Tuesday: at least one person smoked in the stairwell on Tuesday\n"
        "- none of these: the building information rules out none of the listed statements",
   diff=3),

it("C15", "choice",
   "Given only the engineering-works notice, what is the status of the statement?",
   """Southmoor Rail - Engineering works notice: Ashby Junction resignalling, weekends in March

What is happening? We are replacing the signalling at Ashby Junction. Work takes place overnight on Saturdays and all day on Sundays in March.

How will my journey be affected? On Sundays in March, trains between Ashby and Carrow may be cancelled at short notice if the work overruns. Replacement buses will run between Ashby and Carrow every 20 minutes when trains are not running. Buses take about 25 minutes longer than the train.

Tickets. Tickets for Ashby-Carrow journeys are valid on the replacement buses. Advance tickets for a cancelled train can be used on the next available service.

Bicycles. Replacement buses cannot carry bicycles, except folding bikes.

Statement: Some trains between Ashby and Carrow were cancelled at short notice on a Sunday in March.""",
   U, opts=L3[0], card=L3CARD, diff=1),

it("C16", "noul",
   "Taking the council's update as accurate, is the statement guaranteed?",
   """Harlow Vale Council - Highways update, Wednesday 11 February

Stepney Road bridge. The Stepney Road bridge has been closed since 26 January for emergency repairs to the bearings. Contractors have now completed the structural work and are resurfacing the deck. The bridge should reopen to all traffic on Friday 13 February, subject to a final inspection on Thursday afternoon.

Diversion. Until the bridge reopens, the signed diversion via Mill Lane and the A614 remains in place. Buses on routes 7 and 7A continue to divert and will not serve the Stepney Road stops.

Pedestrians. The temporary footbridge will be removed once the main bridge reopens.

We thank residents for their patience during the closure.

Statement: The Stepney Road bridge reopened to all traffic on Friday 13 February.""",
   0, card=FOLLOW, diff=1),

it("C17", "choice",
   "Judged against the club rules and the membership record, how should the statement be labelled?",
   """Ravensworth Cricket Club - Club rules (car parking), and a note from the membership secretary

Rule 14.1 Only season-ticket holders may use the members' car park on match days. Season tickets run from 1 April to 30 September and must be displayed on the dashboard.
Rule 14.2 The overflow field may be used by anyone for a donation of 5 pounds on match days.
Rule 14.3 Blue-badge holders may use the disabled bays next to the pavilion on any day.

Note from the membership secretary, 20 June:
"Pieter van Wyk has asked whether he can park in the members' car park for Saturday's match against Hallam. Pieter has been a playing member for twelve years and is on the committee, but he did not renew his season ticket this year and does not hold one. He is happy to use the overflow field if needed."

Statement: Pieter van Wyk is not permitted to use the members' car park for Saturday's match.""",
   E, opts=L3[1], card=L3CARD, diff=2),

it("C18", "noul",
   "Does the statement follow from the finance procedure?",
   """Tamsworth Housing Association - Finance Procedure FP-3: Approval of supplier invoices

3.1 Every supplier invoice over 5,000 pounds must be approved by two directors before payment. Approval by one director and one budget holder is not sufficient.
3.2 Invoices of 5,000 pounds or less need approval by one budget holder.
3.3 Approvals are recorded in the purchase ledger system; email approvals must be attached to the invoice record.
3.4 Invoices must be paid within 30 days of approval.

Example given in the staff training slides: "An invoice for 4,800 pounds for grounds maintenance can be approved by the estates budget holder alone. An invoice for 5,200 pounds for the same work cannot."

Statement: A supplier invoice for 7,200 pounds that has been approved by only one director has not yet met the approval requirement of FP-3.""",
   1, card=FOLLOW, diff=1),

it("C19", "choice",
   "What is the status, under the pool rules, of a six-year-old wearing a swim cap in the diving pool?",
   """Aldbury Aquatics Centre - Swimmer rules (displayed at poolside)

Caps. All swimmers must wear a swim cap in every pool, except children under 8, who may choose whether to wear one. However, children under 8 in the diving pool must wear a cap so that lifeguards can see them easily.

Supervision. Children under 8 must be accompanied in the water by an adult aged 16 or over.

Diving pool. The diving pool is open to swimmers who can swim 25 metres unaided. Diving boards are open only during supervised sessions.

Clothing. Swimwear must be made of swimming material. Cotton T-shirts and shorts are not permitted in any pool.

Jewellery. Please remove all jewellery before swimming.""",
   "required", opts=DEON, card=DEONCARD, diff=2),

it("C20", "noul",
   "Based only on the board paper, is it certain that the statement is true?",
   """Crestway Distribution - Board paper BP-26/14: Warehouse layout project

Purpose: to seek approval for Phase 2 of the Hinckley warehouse layout project.

Background: In Phase 1 (completed in March), the Hinckley pick faces were re-slotted by order velocity. Phase 2 would move the packing benches next to the dispatch doors and introduce a one-way picking loop.

Expected benefits: according to the consultants' simulation model, the full new layout would cut average picking time by 20% and walking distance by 35%. Management considers these estimates optimistic but broadly credible.

Cost: 410,000 pounds, payback 19 months on the consultants' figures.

Recommendation: the Board approves Phase 2, to be delivered over the August shutdown, with a post-implementation review in November.

Statement: The new layout cut average picking time at Hinckley by 20%.""",
   0, card=FOLLOW, diff=2),

it("C21", "choice",
   "Which of these staff members is permitted to approve, alone, the refund on order 55-1904?",
   """Kittering Home Stores - Refund authority matrix (internal), with a case note

Authority rules:
R1. A refund above 500 pounds may be approved only by the store manager of the store where the purchase was made, or by the area manager for that store's area.
R2. A store manager may approve a refund above 2,000 pounds only with the countersignature of their area manager.
R3. Assistant managers may approve refunds of up to 500 pounds.
R4. An area manager may approve refunds of any amount for stores in their own area.

Case note: Order 55-1904, a 1,200-pound sofa bought at store 7 (Wellbrook, North area). Customer returned it with a manufacturing fault.

Staff on duty or reachable today:
- Fenella Rios, store manager, store 7 (Wellbrook).
- Tobias Lange, assistant manager, store 7 (Wellbrook).
- Mariam Chowdhury, store manager, store 12 (Eastgate, North area).
- Dafydd Rees, area manager, South area.
- Gemma Holt, head office customer relations.
- Anand Pillai, store manager, store 3 (Riverside, South area).
- Clémence Adu, finance business partner.""",
   "Fenella Rios",
   opts=["Tobias Lange", "Mariam Chowdhury", "Dafydd Rees", "Fenella Rios", "Gemma Holt", "Anand Pillai", "Clémence Adu", NONE],
   card="- Tobias Lange: the assistant manager of store 7\n"
        "- Mariam Chowdhury: the store manager of store 12\n"
        "- Dafydd Rees: the South area manager\n"
        "- Fenella Rios: the store manager of store 7\n"
        "- Gemma Holt: the head office customer relations contact\n"
        "- Anand Pillai: the store manager of store 3\n"
        "- Clémence Adu: the finance business partner\n"
        "- none of these: no listed staff member may approve this refund alone",
   diff=3, twin=[("Order 55-1904, a 1,200-pound sofa", "Order 55-1904, a 2,400-pound sofa")], twin_gold=NONE),

it("C22", "choice",
   "Taking the HR letter as true, which label fits the statement?",
   """Brightwater Analytics - Human Resources
Private and confidential

Dear Karim,

Flexible working request - outcome

Thank you for meeting with Joanne and me on 3 September to discuss your request. I am pleased to confirm that, from Monday 15 September, you are allowed to work from home on Fridays. On the other four days you will continue to be based at the Leeds office.

This arrangement will be reviewed after six months. Either you or your manager can ask for an earlier review if the arrangement is not working for the team. Please make sure your home workstation assessment is completed before your first home-working day.

Your contract is otherwise unchanged.

Yours sincerely,
Harriet Okonjo, HR Business Partner

Statement: Karim worked from home on Friday 19 September.""",
   U, opts=L3[2], card=L3CARD, diff=1),

it("C23", "noul",
   "Given the job advert, does the statement necessarily hold?",
   """Saltmarsh Wildlife Trust - Job advert: Reserve Assistant (fixed term, 12 months)

About the role: You'll help the site manager look after the Saltmarsh and Fennick Point reserves: habitat work, visitor engagement, and supporting volunteer groups two days a week.

About you: You'll have practical conservation experience (paid or voluntary), a full driving licence, and be comfortable working outdoors in all weathers. Chainsaw and brushcutter certificates are desirable but not essential.

How to apply: Fill in the online application form, which includes a 500-word supporting statement. Applicants need not include a cover letter, but may attach one if they wish. CVs are not accepted in place of the form.

Closing date: Sunday 5 October at 23:59. Interviews will be held at Fennick Point on 14 October.

Statement: Including a cover letter is optional for applicants.""",
   1, card=FOLLOW, diff=1),

it("C24", "choice",
   "How does the operations log bear on the statement?",
   """Hollin Beck Reservoir - Operations log (dam safety)

Standing design note, spillway gates SG-1 and SG-2: the gate actuators are interlocked with the level sensors, so the gates cannot be opened while the reservoir level is below 142.0 m above datum. Operators cannot override the interlock from the control room; it can only be bypassed mechanically by the dam engineer on site, and the bypass is recorded on a separate form, which has never been used.

Log, Sunday 2 November:
- 00:00 Level 141.62 m. Heavy rain continuing, inflow rising.
- 03:00 Level 141.88 m.
- 06:00 Spillway gate SG-1 opened to 20%. SG-2 remains closed.
- 09:00 Level 142.05 m. Outflow via SG-1 steady.
- 12:00 Rain easing.

Log checked by the supervising engineer, 2 November, 14:30.

Statement: At 06:00 on Sunday 2 November, the reservoir level was at least 142.0 m above datum.""",
   E, opts=L3[3], card=L3CARD, diff=3),

it("C25", "noul",
   "Is the statement consistent with the bank's security bulletin?",
   """Farrowdale Savings Bank - Branch security bulletin, Kingsbridge branch

Vault time lock. The Kingsbridge vault door is fitted with a mechanical time lock. From Friday 18:00 until Monday 08:00, and from 18:00 to 08:00 on weekdays, the vault door cannot be opened by anyone, including with both keys and the combination. The time lock cannot be overridden remotely.

Monday opening procedure. The branch manager and one other key holder open the vault together. The vault opening time is written in the opening log.

Incident last Monday. The branch opened late because the manager's train was delayed. The assistant manager and a cashier arrived at 07:30 and waited in the staff room. The manager arrived at 08:55.

Statement: The Kingsbridge vault door was opened at 07:40 last Monday.""",
   0, card=CONSIST, diff=2),

it("C26", "choice",
   "Given only the merger FAQ, what is the status of the statement?",
   """Pinewood Leisure & Ashcroft Fitness - Membership merger FAQ

Q: I'm a Pinewood member. Can I use the Ashcroft clubs?
A: Yes. Since the merger on 1 July, Pinewood members can use any Ashcroft club, at any time, at no extra cost.

Q: I'm an Ashcroft member. Can I use Pinewood?
A: Yes, but Ashcroft members can use Pinewood only at weekends (Saturday and Sunday). This is because Pinewood's weekday classes are already fully booked by existing members.

Q: Will my membership fee change?
A: Not before 1 January. We will write to you at least 30 days before any change.

Q: Can I bring a guest?
A: Guest passes can be used at your home club only.

Statement: Since the merger, Ashcroft members can use Pinewood on Wednesdays.""",
   C, opts=L3[4], card=L3CARD, diff=1),

]
