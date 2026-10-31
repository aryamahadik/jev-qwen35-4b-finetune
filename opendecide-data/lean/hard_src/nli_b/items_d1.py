"""Part D1: presuppositions and implicatives (stop/start, factives, clefts, filtering, forgot/failed/managed)."""
from _h import it, L3, L3CARD, FOLLOW, E, C, U, NONE

S9 = ["The clinic employs a dermatologist",
      "The Harrow Road branch has a pharmacy counter",
      "Ms. Adeyemi used to receive her repeat prescriptions by post",
      "The practice nurse has changed her working days",
      "The practice has a new phone system",
      NONE]

ITEMS = [

it("D1", "noul",
   "If everything in the statement from the company is true, must the statement below also be true?",
   """Press statement - Hallbrook Mills Ltd, issued Tuesday

Response to local reports about our flour supply

Hallbrook Mills has seen posts on a community forum suggesting that we are cutting off small customers following our new contract with a supermarket group. We want to correct this.

Contrary to the rumour, Hallbrook Mills has not stopped supplying the Tern Street Bakery, and we have no plans to do so. The confusion seems to have arisen because the bakery's Tuesday delivery was delayed last week by a van breakdown.

Our new contract does not change our commitments to independent bakers in the Hallbrook area. We will continue to publish our delivery schedule on our website every Monday.

Media contact: Serena Blackwood, communications manager.

Statement: Hallbrook Mills has supplied the Tern Street Bakery at some point.""",
   1, card=FOLLOW, diff=2,
   twin=[("Hallbrook Mills has not stopped supplying the Tern Street Bakery, and we have no plans to do so. The confusion seems to have arisen because the bakery's Tuesday delivery was delayed last week by a van breakdown.",
          "Hallbrook Mills has not started supplying the Tern Street Bakery, and we have never said we would. The confusion seems to have arisen because a van with our logo was parked near the bakery last week.")],
   twin_gold=0),

it("D2", "choice",
   "Given only the audit summary, which label fits the statement?",
   """Internal Audit - Summary of findings, Northgate Distribution Centre (confidential)

Scope: year-end stock count, 31 December.

1. The count was carried out by warehouse staff over two shifts, with finance observers present on the first shift only.
2. During the reconciliation in January, the lead auditor, Miriam Fosse, realized that the stock count had been inflated by counting the same pallets in racking bay 14 on both shifts. The adjustment is being quantified.
3. Count sheets were not pre-numbered, so it is not possible to confirm that every sheet was returned.
4. Recommendations: pre-numbered count sheets, finance observers on every shift, and a bay-by-bay sign-off.

Management comments are due by 28 February.

Statement: The year-end stock count at Northgate had been inflated.""",
   E, opts=L3[5], card=L3CARD, diff=2,
   twin=[("the lead auditor, Miriam Fosse, realized that the stock count had been inflated by counting the same pallets in racking bay 14 on both shifts. The adjustment is being quantified.",
          "the lead auditor, Miriam Fosse, suspected that the stock count had been inflated by counting the same pallets in racking bay 14 on both shifts. The possible adjustment is being investigated.")],
   twin_gold=U),

it("D3", "choice",
   "How should the statement be labelled, judged against the tribunal decision extract?",
   """First-tier Licensing Tribunal - Decision extract, appeal LT/4471 (Marlow v Kessington District Council)

[14] The appellant, Mr. Anton Marlow, holds a premises licence for a bar on Quay Street. On 3 April he signed an agreement varying the conditions of that licence, including a new closing time of 23:00.

[15] At the hearing, Mr. Marlow told the Tribunal that he did not understand the new closing time. We have considered the recording of the meeting of 3 April with some care. When the licensing officer asked whether he had any questions about the terms, Mr. Marlow pretended that he had read the variation agreement: he said "yes, all fine, I've been through it", turned straight to the signature page, and signed within a minute.

[16] We do not accept that the Council was at fault. The officer offered him time to read the agreement and he declined.

Statement: Mr. Marlow had read the variation agreement before signing it.""",
   C, opts=L3[0], card=L3CARD, diff=2),

it("D4", "noul",
   "Does the statement follow from the procurement email?",
   """From: Oskar Brenner, Purchasing, Valmont Pumps
To: Production planning
Subject: Seal kits for the VX-40 line

Hi all,

An update on the missing seal kits. The supplier, Arcton Seals, claims that the parts were shipped from their Leipzig warehouse on Monday by road freight, and they have given me a consignment number. I have not yet been able to trace that number on the carrier's website, and the carrier's helpline is closed until tomorrow.

If the parts were shipped on Monday, they should be with us on Thursday and the VX-40 line can restart on Friday. If not, we are looking at next week at the earliest, and I will ask Arcton for an air-freight option at their cost.

I'll update you tomorrow by 10:00.

Oskar

Statement: The seal kits were shipped from Arcton's Leipzig warehouse on Monday.""",
   0, card=FOLLOW, diff=1),

it("D5", "choice",
   "Given only the incident timeline, what is the status of the statement?",
   """Incident INC-6620 - Customer database outage, Saturday night (post-incident timeline)

21:40 Primary database node fails its health check. Automatic failover does not complete because the replica is 6 hours behind.
21:52 On-call engineer, Bogdan Mireanu, paged. Decision: restore from last night's backup onto new hardware.
22:30 Backup located and checksum verified.
23:05 Restore started. Estimated duration: 50 minutes.
23:58 The on-call engineer failed to restore the backup before midnight; the restore job stopped at 91% with a storage quota error.
00:40 Quota raised by the infrastructure team.
02:15 Service restored for customers.

Follow-up actions: fix replica lag alerting; pre-provision storage for restores; review quota limits.

Statement: The on-call engineer restored the backup before midnight.""",
   C, opts=L3[1], card=L3CARD, diff=2,
   twin=[("23:58 The on-call engineer failed to restore the backup before midnight; the restore job stopped at 91% with a storage quota error.",
          "23:58 The on-call engineer tried to restore the backup before midnight; the restore job log for the next two hours was not kept.")],
   twin_gold=U),

it("D6", "noul",
   "Taking the security report as accurate, does it follow that the statement is true?",
   """Weekend security report - Ashton Community Centre
Prepared by: G. Farrelly, keyholder

Friday evening: the youth club finished at 21:00. Janelle Okoro, the youth club leader, was responsible for locking up. Janelle forgot to lock the store room on Friday; she locked the main hall and the front door and set the alarm, and she has apologised.

Saturday morning: the cleaner found the store room door closed but unlocked at 07:30. Nothing appears to be missing - the table-tennis equipment, the first-aid kit and the petty-cash tin were all accounted for. The alarm log shows no activations overnight.

Action: I have added "store room" to the lock-up checklist on the back of the front door.

Statement: The store room was not locked by Janelle on Friday.""",
   1, card=FOLLOW, diff=1),

it("D7", "noul",
   "Is the statement guaranteed by the chat thread?",
   """#accounts-receivable (Friday)

Lena (09:05): Tomas, did the Brackley invoice go out? They need it before their month-end, which is today.
Tomas (09:40): Sorry, only just seen this. Yes, I remembered on the train this morning that I had to send the Brackley invoice today - it's on my list. I'm in the supplier review until 13:00.
Lena (09:41): OK. It's the one for the October retainer plus the extra workshop day.
Tomas (09:42): Yep, 8,400 plus VAT. The PDF is in the shared drive.
Lena (16:55): Heading off now. Have a good weekend all.

(No further messages in the channel that day.)

Statement: Tomas sent the Brackley invoice on Friday.""",
   0, card=FOLLOW, diff=2,
   twin=[("Yes, I remembered on the train this morning that I had to send the Brackley invoice today - it's on my list.", "Yes, I remembered to send the Brackley invoice on the train this morning - it's done.")], twin_gold=1),

it("D8", "choice",
   "Which inference label applies to the statement, given the plant supervisor's note?",
   """Tavistone Chemical - Plant 2, supervisor's note to the day shift (Wednesday 06:10)

Morning all,

At 03:20 the operator on Unit 2B found valve V-218 (nitrogen purge to the storage tank) fully open. It should have been closed at the end of the purge sequence yesterday afternoon. There was no release and no alarm, but the tank pressure was higher than normal until it was closed.

I want to be clear on one point, because I have heard the rumours already: it was not the night shift that left the valve open. The valve position is logged every 15 minutes, and the log shows it was already open before the night shift took over.

Please attend the toolbox talk at 07:00 about valve status boards.

Wilhelmina Akande, Plant 2 Supervisor

Statement: Someone left valve V-218 open.""",
   E, opts=L3[2], card=L3CARD, diff=2),

it("D9", "choice",
   "Which of these statements is the practice manager's letter committed to?",
   """Harrow Road Medical Practice
Letter to patients who use the repeat-prescription service

Dear Ms. Adeyemi,

We are writing to let you know about some changes at the practice.

Repeat prescriptions. From 1 March we will no longer send your repeat prescriptions to you by post; they will go electronically to the pharmacy of your choice. If you are not yet registered with a nominated pharmacy, please let reception know.

Skin clinic. If the practice takes on a dermatologist this year, the dermatologist will run a monthly skin clinic here, and we will write to patients who are on the waiting list.

Branch surgery. If the Harrow Road branch has a pharmacy counter, it is only open on weekday mornings.

Nurse appointments. We are considering whether the practice nurse should change her working days, and we will let you know if we decide to.

Phone lines. Our phone lines are busiest between 08:00 and 09:00. Please call later in the day for non-urgent matters.

Yours sincerely,
Imogen Clarke, Practice Manager""",
   S9[2], opts=S9,
   card="- The clinic employs a dermatologist: the practice currently has a dermatologist on its staff\n"
        "- The Harrow Road branch has a pharmacy counter: there is a pharmacy counter at the branch surgery\n"
        "- Ms. Adeyemi used to receive her repeat prescriptions by post: before the change, Ms. Adeyemi's repeat prescriptions were sent to her by post\n"
        "- The practice nurse has changed her working days: the practice nurse now works on different days from before\n"
        "- The practice has a new phone system: the practice has installed a new phone system\n"
        "- none of these: the letter is committed to none of the listed statements",
   diff=3),

it("D10", "noul",
   "Does the statement follow from the operations memo?",
   """MEMO - Tolland Credit Union, Branch Operations
To: Branch managers
Re: Visitor sign-in

As you know, all branches were asked to move from paper visitor books to the tablet sign-in app by the end of Q1. Thank you to the eleven branches that have completed the switch; the data-protection team has confirmed that the tablets store visitor details correctly and delete them after 12 months.

The Harwick branch still uses the paper sign-in book. The tablet for Harwick was delivered in February, but the branch has had no reliable wi-fi in the lobby since the refurbishment. IT expect to fix this by the end of the month.

Until then, the paper book must be locked away at close of business and must not be left on the counter.

Deepa Rahman, Head of Branch Operations

Statement: The Harwick branch currently uses a paper sign-in book for visitors.""",
   1, card=FOLLOW, diff=1,
   twin=[("The Harwick branch still uses the paper sign-in book.", "The Harwick branch no longer uses the paper sign-in book.")],
   twin_gold=0),

it("D11", "choice",
   "Given only the estate agent's note, how does the statement fare?",
   """File note - Carrow & Finch Estate Agents, Lettings
Property: 5 Linnet Court. Prospective tenant: Mr. Julian Pell.
Written by: Amira Haddad, lettings negotiator, Thursday

Julian came in this morning to ask about ending a tenancy early. His situation is complicated: he viewed 5 Linnet Court twice last month, and the landlord's solicitor sent him the lease to sign, but our system does not show whether a signed copy ever came back - the solicitor's office handles that directly and is closed until Monday.

What Julian said about the flat was guarded: "If I signed that lease, I regret signing it - the commute has turned out to be much worse than I thought." He asked what the break clause says.

Action: I will call the solicitor's office on Monday to check the status of the lease and then call Julian back.

Statement: Mr. Pell signed the lease for 5 Linnet Court.""",
   U, opts=L3[3], card=L3CARD, diff=3),

it("D12", "noul",
   "If the site diary is accurate, must the statement be true?",
   """Site diary - Beacon Quay seawall repairs (contractor: Dunmore Marine Civils)

Monday 10 November
07:30 Crew of six on site. Forecast: gale warning from mid-afternoon.
08:00-13:00 Placing rock armour at chainage 120-160. Good progress.
13:15 Site manager instructed crews to start securing the scaffolding on the promenade section and to move plant off the beach.
14:40 The storm reached the coast before the crews could secure the scaffolding; two scaffold bays on the promenade section collapsed onto the footpath. Nobody injured. Area fenced off.
15:10 All staff off site. Excavator left on the upper car park.

Tuesday 11 November
Site closed (storm). Photographs of the collapsed bays sent to the client's engineer.

Statement: The crews secured the promenade scaffolding before the storm reached the coast.""",
   0, card=FOLLOW, diff=2),

it("D13", "choice",
   "Which of these people must have worked at Ardent Foundry at some time?",
   """From: Colette Varga, Heritage Officer, Wynford Museum
To: Oral history volunteers
Subject: Interview list for the Ardent Foundry project

Dear volunteers,

Here's where we are with the interviewee list for the Ardent Foundry exhibition:

- Naomi Brisk: I'm told she didn't stop working at Ardent Foundry when it was sold in 1998. Worth a long interview.
- Rhys Madoc: might start at Ardent's successor company next month, so may be busy.
- Ottilie Crane: claimed in a letter to the local paper to have worked at Ardent for thirty years. We are checking.
- Bram Oyelaran: if Bram worked at Ardent, he'll know about the old kiln; his daughter is asking him.
- Ines Dutra: wishes she had taken the job she was offered at Ardent in 1985.
- Joss Hartley: hasn't started his research placement at the Ardent archive yet.

Please pick two names each by Friday.

Colette""",
   "Naomi Brisk",
   opts=["Rhys Madoc", "Naomi Brisk", "Ottilie Crane", "Bram Oyelaran", "Ines Dutra", "Joss Hartley", NONE],
   card="- Rhys Madoc: the person who might start at the successor company\n"
        "- Naomi Brisk: the person mentioned in connection with the 1998 sale\n"
        "- Ottilie Crane: the person who wrote to the local paper\n"
        "- Bram Oyelaran: the person whose daughter is asking him\n"
        "- Ines Dutra: the person offered a job at Ardent in 1985\n"
        "- Joss Hartley: the person with a research placement at the Ardent archive\n"
        "- none of these: the email does not guarantee that any listed person worked at Ardent Foundry",
   diff=3, twin=[("she didn't stop working at Ardent Foundry when it was sold in 1998",
                  "she didn't start working at Ardent Foundry when it was sold in 1998")],
   twin_gold=NONE),

]
