"""nli_c / workplace and customer emails."""
from _lib import C, Y, T, NLI3, REL5, ESTABLISH, FACTIVE, PRESUP, IMPLICATIVE, QUANT, EXCEPT, MODAL, COND, REPORTED

ITEMS = [
# ------------------------------------------------------------------ em01
# why: "I regret that the second pallet left ... without the certificates" is factive -> the
#      writer commits to it -> yes. Twin: "I worry that" is non-factive -> not established.
Y("em01", "Does the email establish that the second pallet left the warehouse without its conformity certificates?",
"""
From: Rosalind Achebe <r.achebe@quillmoor-logistics.example>
To: Dispatch Team; Customer Care
Subject: Order 55-2031 (Brightwell Kitchens) — certificates

Hi all,

Quick update on the Brightwell Kitchens order that went out on Tuesday. The order was split across two pallets because the worktop sections arrived from the supplier a day late. Pallet one left at 09:15 with the full paperwork pack, which Callum checked against the order sheet and signed.

I regret that the second pallet left the warehouse on Tuesday afternoon without the conformity certificates for the worktop sections. Brightwell's site manager, Deepa Kaur, needs those before her fitters can install anything, so please treat this as urgent.

Customer Care: could you call Deepa this morning, apologise and let her know that scanned copies will be emailed by 11:00 and the originals will follow by courier tomorrow?

Dispatch: from next week, split orders need a second sign-off on the paperwork before any pallet leaves the yard. I'll bring the new checklist to Friday's team huddle.

Thanks,
Rosalind
Operations Supervisor, Quillmoor Logistics
""",
[ESTABLISH, FACTIVE], 1, 2,
twin=T([("I regret that the second pallet left", "I worry that the second pallet may have left")], 0)),

# ------------------------------------------------------------------ em02
# why: "Everyone in Finance except the two contractors has completed" -> Priya (a permanent
#      Finance employee) has completed -> entailment. Twin: "Nobody in Finance except the two
#      contractors" -> Priya has not completed -> contradiction.
C("em02", 'Hypothesis: "Priya Lenz has completed the data-protection refresher." How does the email relate to it?',
"""
From: Mateo Vance <m.vance@corriebank-group.example>
To: Finance Leadership
Subject: Data-protection refresher — status before the audit

Dear all,

As requested at last week's leadership meeting, here is where the Finance department stands on the annual data-protection refresher ahead of the external audit on 12 October.

Everyone in Finance except the two contractors has completed the refresher module on the learning portal. For reference, the department currently has fourteen permanent staff (including Priya Lenz, Oskar Brandt and the rest of the payables team) and two contractors, Jonah Pike and Adaeze Nwosu, whose contracts end in November.

The auditors have told us that they will sample training records for five people at random, so I'd like the records to be complete before the visit. The portal sends reminders automatically every seven days, but a personal nudge from line managers tends to work better.

The module takes about 35 minutes and can be paused and resumed. If anyone has trouble logging in, the IT service desk can reset portal passwords the same day.

Best regards,
Mateo Vance
Compliance Coordinator
""",
NLI3, "entailment", 2,
twin=T([("Everyone in Finance except the two contractors has completed", "Nobody in Finance except the two contractors has completed")], "contradiction")),

# ------------------------------------------------------------------ em03
# why: the service in March appears only as the landlord's claim; the writer explicitly
#      says she has seen no record -> attributed only. Twin: the writer has the engineer's
#      dated service sheet showing a March service -> entailed.
C("em03", 'Choose the description that fits the email and the hypothesis "The boiler at Flat 4 was serviced in March."',
"""
From: Harriet Mbeki <harriet.mbeki@fastmail.example>
To: Tenancy Advice — Wrenfield Housing Clinic
Subject: Boiler at 4, Tolland Court

Hello,

I rent Flat 4 at Tolland Court and I'm writing for advice. The boiler has cut out four times since the start of September, most recently on Sunday night, when we had no hot water for about fourteen hours.

My landlord, Mr Desmond Frye, claims that the boiler was serviced in March and says the problem must be the way we use the thermostat. I asked him for a copy of the service record on 10 September and again on 17 September, but I haven't received anything, and I have not seen a service sticker on the boiler itself.

My tenancy agreement says the landlord will arrange "an annual gas safety check and boiler service". The last gas safety certificate I was given is dated 2 August last year.

Could you tell me what my options are, and whether I should keep paying rent while this is being sorted out? I have kept a diary of every time the boiler has failed, with dates and times.

Many thanks,
Harriet Mbeki
""",
REL5, "attributed only", 2,
twin=T([("I asked him for a copy of the service record on 10 September and again on 17 September, but I haven't received anything, and I have not seen a service sticker on the boiler itself.",
         "He has since sent me a copy of the engineer's service sheet, which shows the boiler was serviced on 14 March, and the sticker on the boiler gives the same date.")], "entailed")),

# ------------------------------------------------------------------ em04
# why: waiver is conditional on payment by Friday; payment status is outstanding -> the
#      waiver is left unestablished -> yes. Twin: paid on Wednesday (before Friday) -> the
#      condition is met, waiver established -> no.
Y("em04", "Is it left unestablished by the email whether Corran Print will waive the late-payment fee on invoice 7719?",
"""
From: Accounts Receivable <ar@corranprint.example>
To: Linh Okafor <linh@bramblefield-events.example>
Subject: Invoice 7719 — overdue reminder

Dear Linh,

Our records show that invoice 7719 (£2,340.00, printing and delivery of programmes for the Bramblefield Folk Weekend) was due for payment on 31 August.

Payment status: outstanding as of this morning (Tuesday 15 September).

Under our standard terms, a late-payment fee of 8% applies to invoices more than 14 days overdue. As a long-standing customer, if the invoice is paid in full by Friday 18 September, we'll waive the late-payment fee. Payment can be made by bank transfer to the account shown on the invoice or by card over the phone on 01632 960 418.

If you believe this reminder has been sent in error, or if there is a query about the invoice, please reply to this email and we will put the account on hold while we look into it.

Kind regards,
Tamsin Rhodes
Accounts Receivable, Corran Print Ltd
""",
[ESTABLISH, COND], 1, 2, role="neg",
twin=T([("Payment status: outstanding as of this morning (Tuesday 15 September).",
         "Payment status: paid in full on Wednesday 16 September (bank reference CP-8812).")], 0)),

# ------------------------------------------------------------------ em05
# why: meeting moved from Thu 8 Oct to Tue 6 Oct; room booking for the 6th confirmed; agenda
#      goes out Monday 5 Oct, i.e. the day before; Farah joins remotely (not in person); budget
#      sign-off is the week after. Only "agenda goes out the day before" is established.
#      Twin: agenda goes out Friday 2 Oct -> "agenda more than one day ahead".
C("em05", "Which one of the following does the email establish?",
"""
From: Oskar Lindqvist <oskar.lindqvist@marrowgate.example>
To: Regional Leads
Subject: Q4 planning meeting — new date

Hi everyone,

Because the Harbour Road office is closed for rewiring on Thursday 8 October, the Q4 planning meeting will now take place on Tuesday 6 October, 10:00–15:00, in the Lantern Room at the Carvell Street office. The room booking is confirmed and lunch will be provided.

I will send the agenda and the draft regional targets on Monday 5 October. Please read the targets before you arrive; we will not walk through them slide by slide.

Farah has let me know she can't travel that week, so she will join by video for the morning session only. Everyone else has confirmed they can attend in person.

We won't sign off the Q4 budget at this meeting. Finance needs the updated headcount figures first, so sign-off is planned for the following week, once they have been checked.

Travel costs can be claimed in the usual way. If you need a hotel for the Monday night, please book through the travel desk by 25 September.

Thanks,
Oskar
""",
[("meeting stays on 8 October", "The Q4 planning meeting takes place on Thursday 8 October."),
 ("agenda goes out the day before", "The agenda will be sent on the day immediately before the meeting."),
 ("agenda more than one day ahead", "The agenda will be sent more than one day before the meeting."),
 ("everyone attends in person", "Every regional lead will attend the whole meeting in person."),
 ("budget signed off at the meeting", "The Q4 budget will be signed off at the planning meeting."),
 ("Farah attends all day", "Farah will attend both the morning and the afternoon sessions."),
 ("none of these", "The email establishes none of the statements above.")],
"agenda goes out the day before", 2,
twin=T([("I will send the agenda and the draft regional targets on Monday 5 October.", "I will send the agenda and the draft regional targets on Friday 2 October.")], "agenda more than one day ahead")),

# ------------------------------------------------------------------ em06
# why: 25,000 - 18,400 spent - 4,000 deposit = 2,600 < 3,000 -> yes.
#      Twin: spent 17,400 -> 25,000 - 17,400 - 4,000 = 3,600 -> not less than 3,000 -> no.
Y("em06", "Does the email establish that, once the venue deposit is paid, less than €3,000 of the conference budget will remain?",
"""
From: Noor Haddad <noor.haddad@elstree-assoc.example>
To: Conference Working Group
Subject: Budget position — Northern Members' Conference

Hi all,

Ahead of Thursday's call, here is the budget position for the Northern Members' Conference in March.

The committee approved a total budget of €25,000. So far we have spent €18,400, which covers the keynote speakers' fees, the printed programme, the conference app licence and the first instalment for audiovisual hire. All of these invoices have now been paid.

The only commitment still outstanding is the venue deposit of €4,000, which is due on 30 September. There are no other signed contracts yet.

Before we agree to the evening reception quote from Halvard Catering, I'd like us to be clear about what is left once the deposit has gone out. The reception quote is €2,850 for up to 180 guests.

Please also let me know if you are expecting any invoices that I haven't listed above, so that I can update the tracker.

Best,
Noor
Treasurer, Elstree Professional Association
""",
[ESTABLISH, ("Remaining budget", "the approved total minus everything spent and minus the named outstanding commitment.")], 1, 2,
twin=T([("So far we have spent €18,400,", "So far we have spent €17,400,")], 0)),

# ------------------------------------------------------------------ em07
# why: "Dana believes" is non-factive; the writer has not checked -> neutral.
#      Twin: the migration log (writer's own statement) shows completion -> entailment.
C("em07", 'Given the email, is the hypothesis "The customer-database migration finished overnight" entailed, contradicted or neutral?',
"""
From: Kelvin Osei <k.osei@tallowbright.example>
To: Support Leads
Subject: Morning handover — Wednesday

Morning all,

Handover from the overnight shift:

1. Customer-database migration: Dana believes the migration finished overnight, but I haven't been able to open the migration dashboard since 05:00 because of the VPN issue below, so I can't give you a status myself. Please don't tell customers that the new account pages are live until somebody has checked.

2. VPN: the Farnley office VPN has been dropping every 20–30 minutes since about 04:30. Network Ops have a ticket open (NET-40218) and think it's a certificate problem.

3. Queue: 118 tickets open at 06:00, up from 92 yesterday. Most of the increase is password resets from the mobile app.

4. Staffing: Amir is off sick today. Leonie has agreed to cover his chat shift from 09:00 to 13:00.

I'll be back online at 14:00 if anyone needs more detail.

Kelvin
""",
NLI3, "neutral", 2,
twin=T([("Dana believes the migration finished overnight, but I haven't been able to open the migration dashboard since 05:00 because of the VPN issue below, so I can't give you a status myself.",
         "the migration log shows the migration finished overnight at 03:52 with no errors, so it's done, although I haven't been able to open the dashboard since 05:00 because of the VPN issue below.")], "entailment")),

# ------------------------------------------------------------------ em08
# why: "Not all of the returned units were faulty" -> at least one was not faulty -> the email
#      does establish it -> "fail to establish?" = no. Twin: "We don't yet know whether all
#      ... were faulty" -> nothing settled -> yes.
Y("em08", "Does the email fail to establish that at least one of the returned heaters was not faulty?",
"""
From: Bettina Saar <b.saar@kelvora-home.example>
To: Product Quality
Subject: Returns analysis — Kelvora PH-200 patio heater, August batch

Hello team,

As promised, a short summary of the returns analysis for the PH-200 August production batch.

We received 46 returned units between 1 and 21 September, all from customers who reported that the heater switched itself off after a few minutes. Not all of the returned units were faulty. The lab tested each unit for three hours at full output in the test chamber, and the results have been logged in the returns database under batch code AUG26-PH.

The most common cause of the cut-outs was the tilt sensor, which was fitted with the wrong sensitivity setting on part of the batch. We have asked the factory to check the setting on all remaining stock before it ships.

I'd suggest we update the quick-start guide so that it explains the tilt sensor more clearly, since some customers seem to have placed the heater on uneven paving.

Regards,
Bettina
Quality Engineer
""",
[ESTABLISH, QUANT], 0, 2, role="neg",
twin=T([("Not all of the returned units were faulty.", "We don't yet know whether all of the returned units were faulty.")], 1)),

# ------------------------------------------------------------------ em09
# why: the email covers the refund of the deposit, not the cleaning fee; nothing asserts,
#      attributes or conditions a cleaning-fee refund -> not settled.
#      Twin: the writer confirms the cleaning fee has also been refunded -> entailed.
C("em09", 'Hypothesis: "Mr Adeyemi\'s cleaning fee was refunded." Which description fits the email?',
"""
From: Guest Services <stay@lindenhallcottages.example>
To: Samuel Adeyemi
Subject: Your stay at Wren Cottage, 4–11 September

Dear Mr Adeyemi,

Thank you for staying at Wren Cottage and for your feedback about the broken shower thermostat, which our maintenance team replaced on 12 September.

We have now completed the checkout inspection. The cottage was left in excellent condition, and I'm pleased to confirm that your damage deposit of £250 was refunded in full to the card used for the booking on 15 September. Depending on your bank, it can take up to five working days to appear on your statement.

As a gesture of goodwill for the inconvenience with the shower, we have also added a voucher for £60 to your account, which can be used against any future booking made before the end of next year. The voucher code is WREN-60-SA.

We hope to welcome you back to Linden Hall soon.

Warm regards,
Beatrix Molloy
Guest Services Manager, Linden Hall Cottages
""",
REL5, "not settled", 3,
twin=T([("was refunded in full to the card used for the booking on 15 September.",
         "was refunded in full to the card used for the booking on 15 September, together with the £45 cleaning fee.")], "entailed")),

# ------------------------------------------------------------------ em10
# why: "has stopped syncing" presupposes it synced before the June update -> yes.
#      Twin: "has never synced" -> it did not sync before -> not established -> no.
Y("em10", "Does the ticket email establish that the Ferrow Notes app synced the customer's contacts at some point before the June update?",
"""
From: Imogen Tate <imogen.tate@postbox.example>
To: support@ferrownotes.example
Subject: Contacts problem — ticket #FN-77104

Hello,

I'm following up on ticket #FN-77104, which I opened three weeks ago and which is still marked "awaiting customer".

Since the June update (version 8.2), the Ferrow Notes app on my phone has stopped syncing my contacts with the desktop version. Notes and attachments still sync normally in both directions. I have signed out and back in on both devices, reinstalled the phone app, and checked that contacts permission is switched on in my phone's settings.

I use the app for my small physiotherapy practice, so this matters: I attach client contact cards to my appointment notes, and at the moment I'm having to copy phone numbers across by hand.

Phone: Nexa 12, operating system version 17.1. Desktop: Ferrow Notes 8.2.3 on a laptop.

Please let me know whether there is a fix or a workaround, and whether I should expect a refund for this month if it isn't resolved.

Thanks,
Imogen Tate
""",
[ESTABLISH, PRESUP], 1, 2,
twin=T([("Since the June update (version 8.2), the Ferrow Notes app on my phone has stopped syncing my contacts with the desktop version.",
         "I installed the Ferrow Notes app on my phone in July, after the June update (version 8.2), and it has never synced my contacts with the desktop version.")], 0)),

# ------------------------------------------------------------------ em11
# why: "must give at least 60 days' notice" is an obligation; the tenant has not yet given
#      notice -> neutral. Twin: notice given 2 March for 30 June = 120 days -> entailment.
C("em11", 'What is the relation between the email and the hypothesis "Ms Rowe gave at least 60 days\' notice"?',
"""
From: Lettings Desk <lettings@hartfieldhomes.example>
To: Clara Rowe
Subject: Re: Ending my tenancy at 22 Marl Street

Dear Ms Rowe,

Thank you for letting us know that you are thinking about moving out of 22 Marl Street this summer.

Under clause 14 of your tenancy agreement, the tenant must give at least 60 days' notice in writing, and the tenancy must end on the last day of a rental month. Notice can be given by email to this address or by post to our office.

You have told us that you have not yet decided on your moving date and that you will confirm it once your new employer has agreed a start date. At the moment we therefore hold no notice from you, and the tenancy continues as normal.

When the tenancy ends, we will arrange a checkout inspection and return your deposit, less any agreed deductions, within ten days.

Please let us know if you would like a copy of the tenancy agreement.

Kind regards,
Oliver Nkemelu
Lettings Coordinator, Hartfield Homes
""",
NLI3, "neutral", 2,
twin=T([("You have told us that you have not yet decided on your moving date and that you will confirm it once your new employer has agreed a start date. At the moment we therefore hold no notice from you, and the tenancy continues as normal.",
         "We received your written notice by email on 2 March, giving 30 June as your moving-out date, and the tenancy will end on that date.")], "entailment")),

# ------------------------------------------------------------------ em12
# why: 9 applicants; at most 3 shortlisted; interviews for "few, if any" external; Raj is
#      internal; offer "might" be made in October. Established: fewer than half of the
#      applicants will be shortlisted (<=3 of 9). Not established: an offer in October;
#      any external applicant interviewed; Raj shortlisted.
#      Twin: "at most three" -> "at least five" -> more than half will be shortlisted.
C("em12", "Which one of these statements does the email establish?",
"""
From: Yusuf Brennan <y.brennan@calderwick-trust.example>
To: Hiring Panel — Senior Grants Officer
Subject: Shortlisting next steps

Dear panel,

The application window for the Senior Grants Officer role closed on Friday. We received nine applications: two from current Trust staff (Raj Menon and Zoe Hartley) and seven from external candidates.

Given the panel's diaries, we will shortlist at most three applicants for interview. I have attached the scoring grid; please score every application independently and return your grids to me by Wednesday at noon. I will combine the scores and circulate a proposed shortlist on Thursday.

Interviews will be held on 1 and 2 October. If the panel is unanimous after interviews, an offer might be made before the end of October; otherwise we will hold a second-stage task in November.

As a reminder, internal candidates should be scored on the same criteria as external ones, and knowledge of the Trust's systems should not be credited unless it is mentioned in the application.

Many thanks,
Yusuf
HR Business Partner
""",
[("fewer than half shortlisted", "Fewer than half of the nine applicants will be shortlisted."),
 ("more than half shortlisted", "More than half of the nine applicants will be shortlisted."),
 ("Raj will be shortlisted", "Raj Menon will be invited to interview."),
 ("an offer in October", "An offer will be made before the end of October."),
 ("an external interviewee", "At least one external candidate will be interviewed."),
 ("none of these", "The email establishes none of the statements above.")],
"fewer than half shortlisted", 3,
twin=T([("we will shortlist at most three applicants for interview", "we will shortlist at least five applicants for interview")], "more than half shortlisted")),

# ------------------------------------------------------------------ em13
# why: only one person referred to as "she" besides the writer's own voice: Leona Price is
#      the only woman named; "she approved the refund on Monday" -> Leona approved -> the
#      question "not established?" = no. Twin: "she has not yet approved" -> yes.
Y("em13", "Is it not established by the email that Leona Price approved the refund for order 30-9914?",
"""
From: Graham Whitlock <g.whitlock@saltmarsh-outdoor.example>
To: Customer Service Team
Subject: Order 30-9914 — tent return

Hi team,

A note on the return for order 30-9914 (Harrier 4 tent, £389), which has been escalated twice by the customer, Mr Teodor Bakker.

The tent came back to the warehouse on 11 September with a torn inner door. Mr Bakker says the tear was there when the tent arrived; our warehouse lead, Anton Reyes, thinks it happened during use. Because the order is over the £250 limit for team-level refunds, the case went to Leona Price, the returns manager, on Friday. She approved the refund on Monday after looking at the photos from the courier's delivery scan, which show the tent bag already split.

Please make sure the refund is processed today, and send Mr Bakker the standard apology email with a 10% voucher. Anton, can you add the courier photos to the damaged-in-transit log so that we can claim from the courier?

Thanks,
Graham
""",
[ESTABLISH, ("Pronoun reference", "a pronoun refers to the person the passage makes the only suitable antecedent.")], 0, 2, role="neg",
twin=T([("She approved the refund on Monday after looking at", "She has not yet decided on the refund and wants to look again at"),
        ("Please make sure the refund is processed today, and send Mr Bakker the standard apology email with a 10% voucher.",
         "Please don't process anything yet; just send Mr Bakker the standard holding email.")], 1)),

# ------------------------------------------------------------------ em14
# why: dividend payment is stated only under the auditors' sign-off, which is pending ->
#      conditional only. Twin: the CFO "expects" it will be paid -> attributed only.
C("em14", 'Hypothesis: "Pellam Group will pay the interim dividend on 1 December." Choose the description that fits the email.',
"""
From: Investor Relations <ir@pellamgroup.example>
To: Registered Shareholders (email list)
Subject: Interim dividend — timetable update

Dear Shareholder,

We are writing to update you on the timetable for the interim dividend of 6.4 pence per share announced with our half-year results on 3 September.

Provided the auditors sign off the revised half-year accounts, Pellam Group will pay the interim dividend on 1 December to shareholders on the register on 6 November. The revision relates to the classification of lease payments at two of our distribution centres and does not change the group's reported cash position.

The auditors' review is under way and we will write to you again as soon as it is complete.

Shareholders who have registered for the dividend reinvestment plan do not need to take any action. If you would like to change your payment instructions, please contact the share registrar, Colbridge Registrars, before 6 November.

Yours faithfully,
Anya Sorensen
Company Secretary, Pellam Group plc
""",
REL5, "conditional only", 3,
twin=T([("Provided the auditors sign off the revised half-year accounts, Pellam Group will pay the interim dividend on 1 December",
         "Chief financial officer Marcus Webb expects that Pellam Group will pay the interim dividend on 1 December")], "attributed only")),

# ------------------------------------------------------------------ em15
# why: "failed to deliver before noon" -> it did not arrive before noon -> no.
#      Twin: "managed to deliver before noon" -> arrived before noon -> yes.
Y("em15", "Does the email establish that the replacement pump reached the Holm Farm site before noon?",
"""
From: Eilidh Ferguson <eilidh@strathmore-irrigation.example>
To: Holm Farm Partnership
Subject: Replacement pump — delivery on Thursday

Dear Mr and Mrs Holm,

I'm sorry for the trouble with Thursday's delivery of the replacement booster pump for your east field irrigation line.

As you know, we had booked a before-noon delivery with Carrick Freight so that our engineer, Tobias, could fit the pump in the afternoon. I've now had the tracking report from Carrick, and the courier failed to deliver before noon; their driver was held up by the closure of the B782 and the tracking shows a first attempt at your gate at 13:40, by which time Tobias had left for another job.

We won't charge you for the extra visit. Tobias can come on Monday morning at 08:00 to fit the pump, if that works for you.

Please let me know by Friday afternoon, and again, apologies.

Best wishes,
Eilidh Ferguson
Customer Operations, Strathmore Irrigation
""",
[ESTABLISH, IMPLICATIVE], 0, 2,
twin=T([("the courier failed to deliver before noon; their driver was held up by the closure of the B782 and the tracking shows a first attempt at your gate at 13:40, by which time Tobias had left for another job.",
         "the courier managed to deliver before noon despite the closure of the B782; the tracking shows it signed for at your gate at 11:25, but Tobias was held up at another job and could not get to you.")], 1)),

# ------------------------------------------------------------------ em16
# why: €12,480 is €1,520 under the cap -> cap = 14,000 -> entailment.
#      Twin: €1,520 over the cap -> cap = 10,960 -> contradiction.
C("em16", 'How does the email bear on the hypothesis "The procurement cap for the laptop order is €14,000"?',
"""
From: Luca Ferreira <l.ferreira@ambermoor-schools.example>
To: Head Teacher; School Business Manager
Subject: Classroom laptop order — quote received

Dear both,

I've now received the final quote from Brightpath IT for the 24 classroom laptops, including three-year warranties, protective cases and set-up on our network.

The total quote comes to €12,480, which is €1,520 under the procurement cap that the governors set for this order at their July meeting. It is also about €900 less than the cheapest of the other two quotes we received in August.

Brightpath can deliver in the second week of October if we place the order by 30 September. The set-up would be done on a training day so that lessons are not affected.

If you are both happy, I will raise the purchase order on Friday. I have attached the three quotes and a short comparison table for your records.

Best wishes,
Luca Ferreira
IT Coordinator, Ambermoor Primary Schools Federation
""",
NLI3, "entailment", 2,
twin=T([("which is €1,520 under the procurement cap", "which is €1,520 over the procurement cap")], "contradiction")),

# ------------------------------------------------------------------ em17
# why: "is no longer on the approval chain" presupposes Gideon was on it before -> the email
#      does establish it -> "leave unestablished?" = no. Twin: "has been added to the approval
#      chain" -> nothing says he was previously on it -> yes.
Y("em17", "Does the email leave unestablished whether Gideon Ashby was previously on the purchase approval chain?",
"""
From: Procurement Operations <procurement@brookhollow.example>
To: All Budget Holders
Subject: Changes to purchase approvals from 1 October

Dear colleagues,

Please note the following changes to purchase approvals, which take effect on Thursday 1 October.

1. Gideon Ashby, facilities manager, is no longer on the approval chain for purchases over £5,000 in the Estates cost centre. These purchases will be approved by Hana Kowalczyk, deputy finance director.

2. The threshold at which a second quote is required rises from £2,000 to £3,000 for all cost centres.

3. Purchase orders for software subscriptions must now be copied to the IT security team before approval, whatever their value.

The purchasing system will be updated overnight on 30 September. Orders submitted before then will follow the old rules, even if they are approved afterwards.

If you have questions, please contact the procurement helpdesk on extension 4410.

Kind regards,
Procurement Operations
""",
[ESTABLISH, PRESUP], 0, 2, role="neg",
twin=T([("is no longer on the approval chain for purchases over £5,000 in the Estates cost centre. These purchases will be approved by Hana Kowalczyk, deputy finance director.",
         "has been added to the approval chain for purchases over £5,000 in the Estates cost centre, alongside Hana Kowalczyk, deputy finance director.")], 1)),
]
