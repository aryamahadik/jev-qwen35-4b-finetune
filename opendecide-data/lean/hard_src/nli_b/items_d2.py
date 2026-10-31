"""Part D2: presuppositions and implicatives continued (filtering, projection from questions, too, the only, no longer)."""
from _h import it, L3, L3CARD, FOLLOW, E, C, U, NONE

S22 = ["The replacement laptop has arrived",
       "Helga's laptop was stolen",
       "Aidan's laptop was stolen",
       "The office alarm was faulty",
       "The police have been told about the break-in",
       NONE]

ITEMS = [

it("D14", "choice",
   "Given only the lab manager's reply, what is the status of the statement?",
   """Forum: Hospital Laboratory Users Group > Microbiology > "Friday C. diff testing at Kellbrook?"

Original post (ward sister, Ward 12): Our registrar says Kellbrook lab used to run C. diff toxin tests on Friday afternoons, and now we can't get results until Monday. Is that right? It's causing isolation-bed problems.

Reply from P. Nwachukwu, Laboratory Manager, Kellbrook:
Thanks for raising this. I've been in post for three weeks, so I'm still piecing together the history. Our analyser records only go back to the migration in June, and they show no Friday-afternoon runs at all. So either the lab never ran the test on Friday afternoons, or the lab has stopped running it on Friday afternoons since the staffing changes in the spring. I'm asking my predecessor which it is. In the meantime, urgent samples can be sent to the Brackton lab, which runs the test seven days a week; please phone ahead.

Statement: The Kellbrook lab used to run C. diff toxin tests on Friday afternoons.""",
   U, opts=L3[4], card=L3CARD, diff=3),

it("D15", "noul",
   "Can the statement be concluded from the committee minutes?",
   """Ashby Community Fund - Grants Committee, minutes (item 6)

Item 6: Concerns raised about the 2025 grant to the Ashby Youth Football League (AYFL)

The chair summarised the anonymous letter received in October, which alleged that part of the 4,000-pound grant for pitch hire had been spent on an end-of-season trip.

Members discussed the letter at length. Nobody on the committee believes that the grant was misspent: the AYFL's end-of-year report shows pitch-hire invoices for the full amount, and the trip was paid for by parents. The treasurer noted, however, that the invoices have not yet been checked against the pitch operator's own records.

Resolved: the treasurer will ask the pitch operator for a statement of account; no further action until that is received. Item to return at the January meeting.

Statement: The 2025 grant to the AYFL was not misspent.""",
   0, card=FOLLOW, diff=2),

it("D16", "noul",
   "Would accepting the email commit a reader to the statement?",
   """From: Siobhan Mercer, Head of Internal Controls, Delaney Retail Group
To: Finance Operations Leads
Subject: Duplicate payment to Corran Packaging - questions before the audit committee

Dear all,

Before I write the paper for the audit committee, I need clear answers to three questions:

1. When did the finance team discover that Corran Packaging had been paid twice for invoice CP-20931?
2. Why did the duplicate-payment check in the payment run not flag it?
3. Has the supplier confirmed in writing that the second payment will be returned, and by what date?

Please send your answers to me by Thursday, with any supporting screenshots from the payment system. If anyone thinks the committee paper should cover other suppliers, please say so in your reply.

Many thanks,
Siobhan

Statement: Corran Packaging had been paid twice for invoice CP-20931.""",
   1, card=FOLLOW, diff=2),

it("D17", "choice",
   "Judged against the insurer's notice, which label fits the statement?",
   """Delacourt Insurance - Important changes to your Home Basic policy

Please read this notice alongside your policy wording.

What is changing? Since 1 July, Delacourt no longer covers flood damage under the Home Basic policy. Flood cover is now available only as an add-on (Flood Plus) or as part of the Home Complete policy. Storm damage, burst pipes and escape of water remain covered under Home Basic.

Why? Claims costs for flood damage have risen sharply in the last three years, and separating flood cover lets us keep the Home Basic price down for customers in low-risk areas.

What do I need to do? If you want flood cover, you can add Flood Plus at any time from your online account. If you do nothing, your Home Basic cover will continue without flood cover.

Statement: Delacourt's Home Basic policy has never covered flood damage.""",
   C, opts=L3[5], card=L3CARD, diff=2),

it("D18", "choice",
   "Which of these applicants must have submitted the bursary form by the deadline?",
   """Tallis College of Music - Bursary Office: notes from the deadline day helpdesk (Friday, deadline 17:00)

- Amara Diallo: the upload page crashed twice, but she managed to submit the bursary form at 16:52.
- Fergus Whitlow: tried to submit the form from his phone at 16:58; we don't yet know whether it went through.
- Keziah Morgan: forgot to submit the form - she thought the deadline was next Friday.
- Leonie Hartmann: was allowed to submit a paper form instead of using the portal, because of her visual impairment.
- Callum Achebe: refused to submit the form, saying the income questions were too intrusive.
- Ravi Sundaram: hesitated to submit the form until his parents had checked the figures.
- Wren Castellano: was about to submit the form when the office phone line cut out.

Portal status reports will be run on Monday, when we will have the full list.""",
   "Amara Diallo",
   opts=["Fergus Whitlow", "Keziah Morgan", "Amara Diallo", "Leonie Hartmann", "Callum Achebe", "Ravi Sundaram", "Wren Castellano", NONE],
   card="- Fergus Whitlow: the applicant who used his phone\n"
        "- Keziah Morgan: the applicant who misread the deadline\n"
        "- Amara Diallo: the applicant whose upload page crashed twice\n"
        "- Leonie Hartmann: the applicant offered a paper form\n"
        "- Callum Achebe: the applicant who objected to the income questions\n"
        "- Ravi Sundaram: the applicant waiting for his parents\n"
        "- Wren Castellano: the applicant whose phone line cut out\n"
        "- none of these: the notes do not guarantee that any listed applicant submitted the form by the deadline",
   diff=2, twin=[("but she managed to submit the bursary form at 16:52.", "but she attempted to submit the bursary form at 16:52.")],
   twin_gold=NONE),

it("D19", "noul",
   "Given the incident report, is the statement guaranteed?",
   """Near-miss report NM-2291 - Welland Street refurbishment
Reported by: site supervisor, Farhan Qureshi

What happened: At 10:15 on Wednesday an electrician's apprentice, working under the supervision of the electrical foreman, began stripping an old lighting circuit on the second floor. The foreman did not know that the cable was live, and the apprentice didn't think it was either, because the circuit had been labelled "dead" on the old distribution board. The apprentice's voltage tester lit up before any conductor was cut, and work stopped immediately. Nobody was hurt.

Cause: the old distribution board labels were wrong; the circuit was fed from a separate board in the basement.

Actions: all old boards to be treated as unlabelled; prove-dead testing on every circuit before work; toolbox talk for all trades on Thursday.

Statement: The cable the apprentice began working on was live.""",
   1, card=FOLLOW, diff=2),

it("D20", "noul",
   "Based only on the reconciliation note, must the statement be true?",
   """Reconciliation note - Fennimore Trust, month-end close (March)

Bank reconciliation for the main operating account showed a difference of 1,450 pounds on 31 March. The assistant accountant, Joel Ramsey, traced it on 2 April to a supplier receipt that had been keyed twice. Before the external auditors could find the error during their April fieldwork, Joel corrected it with a reversing journal (JNL-0412) and attached the evidence to the reconciliation file.

The auditors' fieldwork ran from 8 to 12 April. Their management letter has not been received yet.

The Finance Manager has asked for the double-keying check in the receipts workflow to be switched back on; it had been disabled during the system upgrade in February.

Statement: The external auditors found the double-keying error during their April fieldwork.""",
   0, card=FOLLOW, diff=3),

it("D21", "choice",
   "Given only the rota message, the statement is which of these?",
   """Fenwick Food Bank - Volunteer coordinator's message (WhatsApp group), Wednesday

Hi everyone! Rota update for this Saturday's distribution (10:00-13:00, St Luke's hall):

Marcus is on the rota for Saturday too, so we now have enough drivers for the three home-delivery rounds. Thank you, Marcus!

I still need two people on the welcome desk and one person to help with the tins sort in the back room. If you can help, reply here and I'll add you.

Reminder: last month Priya ran the welcome desk on two Saturdays and wrote a really useful checklist, which is now pinned to the noticeboard in the hall. Please read it if you're new.

Parking at St Luke's is limited on Saturdays because of the market, so please car-share if you can.

Thanks all - Dorota

Statement: Priya is on the rota for this Saturday's distribution.""",
   U, opts=L3[0], card=L3CARD, diff=2),

it("D22", "choice",
   "Which of these statements is the office manager's email committed to?",
   """From: Nell Okafor, Office Manager, Brackwater Design Studio
To: All staff
Subject: Weekend break-in - where things stand

Hi all,

Thanks for your patience on Monday morning. A few things are still open, so here is a list of what I am chasing:

1. Has the replacement for Helga's stolen laptop arrived yet? IT said it would be delivered to reception, but I haven't seen it. If anyone signed for a parcel from Deskline, please tell me.
2. If Aidan's laptop was also taken, I need to know today - he's working from home and says he isn't sure whether he left it in the studio or at his flat.
3. If the office alarm was faulty, the insurer will want the engineer's report, so I've asked the alarm company to send an engineer to test it on Wednesday.
4. Did anyone tell the police about the break-in over the weekend? I've tried to find a crime reference number in our shared inbox and can't see one. If nobody has, I'll report it this afternoon.

Please don't discuss the break-in with clients until we know more. I'll send another update on Thursday.

Thanks,
Nell""",
   S22[1], opts=S22,
   card="- The replacement laptop has arrived: the replacement for Helga's laptop has been delivered\n"
        "- Helga's laptop was stolen: Helga's laptop was taken in the break-in\n"
        "- Aidan's laptop was stolen: Aidan's laptop was taken in the break-in\n"
        "- The office alarm was faulty: the studio's alarm was not working properly\n"
        "- The police have been told about the break-in: someone has reported the break-in to the police\n"
        "- none of these: the email is committed to none of the listed statements",
   diff=3),

it("D23", "noul",
   "Does the statement follow from the council's web page?",
   """Wendlesham Borough Council - Garden waste collection

In April 2024 the council stopped collecting garden waste for free. Since then, garden waste has been collected only for households that subscribe to the garden waste service, at 45 pounds per bin per year. The charge has not been waived for any year since it was introduced, and the council has no plans to return to free collection.

How to subscribe: online, by phone, or at the civic centre. A sticker will be posted to you within 10 working days; put it on the lid of your brown bin.

Collection days: fortnightly, on the same day as your recycling collection, from March to November. There is one collection in December and one in January for Christmas trees.

What can go in the bin: grass cuttings, hedge trimmings, leaves, small branches, weeds and flowers. No soil, rubble, food waste or animal waste.

Statement: In 2025 the council collected garden waste for free.""",
   0, card=FOLLOW, diff=2),

it("D24", "choice",
   "Taking the officer's statement as accurate, how does it bear on the statement below?",
   """Statement of PC 4471 Harriet Fenn, Castleton Constabulary (extract)

On Saturday 22 March at about 23:40 I attended a report of a collision between a taxi and a cyclist at the junction of Bridge Street and Tanner's Row. On arrival I spoke to a witness, Ms. Olena Kravets, who had been waiting at the bus stop opposite.

I wrote down Ms. Kravets's account in my pocket notebook and read it back to her. At the scene, Ms. Kravets refused to sign the witness statement I had written up; she said the wording about the traffic light colour was wrong and that she was too shaken to correct it there.

On Tuesday 25 March Ms. Kravets attended Castleton police station and gave a fresh statement to DC Morrow, which she read and signed.

Statement: Ms. Kravets signed the witness statement that PC Fenn had written up at the scene.""",
   C, opts=L3[1], card=L3CARD, diff=2),

it("D25", "choice",
   "Given the transport coordinator's message, what is the status of the statement?",
   """From: Ruairi Gallagher, Transport Coordinator, Glenmoor Day Centre
To: Centre staff
Subject: Minibus drivers for the Thursday outing

Hello all,

A few of you have asked whether the Thursday outing to Kilbarron Gardens can go ahead if Tobias is off sick again. Good news: Tobias isn't the only volunteer who can drive the minibus. I checked the insurance list this morning, and the list has more than one name on it. I don't have the list in front of me now, though, so I can't tell you who else is on it.

The volunteers who have offered to help on Thursday are Mairead Doyle, Senan Price and Aoife Burke. I will confirm the driver on Wednesday afternoon.

Lunch is booked at the garden café for 12:30. Please make sure every client has their medication packed.

Ruairi

Statement: Mairead Doyle can drive the minibus under the centre's insurance.""",
   U, opts=L3[2], card=L3CARD, diff=3),

it("D26", "noul",
   "If everything in the inspection summary is true, must the statement be true?",
   """Kilnworth Housing - Summary of electrical inspection, 14 Orchard Row (void property)

The property became vacant on 1 September. Before it can be re-let, the electrical installation must be certified as satisfactory.

On 9 September our approved contractor's inspector, Dylan Moss, attended. His brief was to find out whether the wiring was certified as satisfactory at the last periodic inspection in 2021, and to carry out a new inspection. He found out whether the wiring was certified: the 2021 paperwork was in the council's archive, and he has attached it to his report. His new inspection is not yet complete, because the loft could not be accessed safely.

Next steps: the lettings team will not advertise the property until the new certificate is issued. A return visit is booked for 16 September.

Statement: The wiring at 14 Orchard Row was certified as satisfactory at the 2021 periodic inspection.""",
   0, card=FOLLOW, diff=3,
   twin=[("He found out whether the wiring was certified:", "He found out that the wiring was certified:")], twin_gold=1),

]
