"""Items 25-44: does a named exception apply? (yes/no). Gold 1 = yes."""

ITEMS = [
dict(n=25, j="M", rules=["M801", "M802", "M803_2"], d=2,
q="Is Bexley's answer admissible under the excited-utterance provision, section 803(2)?", gold=1,
doc="""Morrow Vale County Court - Estate of Orla Bexley v. Martin and Dee Halloran (dog attack)
Agreed chronology and disputed evidence

At 7:05 pm on 2 September, Orla Bexley, aged 71, was knocked down and bitten on the forearm by a large dog on Tamsin Lane. The dog ran off.

Her neighbour, Idris Maun, a retired schoolteacher, heard her screaming and reached her about eight minutes later. She was sitting on the pavement, bleeding and shaking. Maun asked, "Orla, what happened?" She answered, crying: "The Hallorans' mastiff got out of their gate and went straight for me."

Bexley died of unrelated causes before trial. The Hallorans deny that their dog was loose that evening. The estate offers Maun's testimony of Bexley's answer to prove that it was the Hallorans' mastiff that attacked her.""",
twin=dict(rep=[("Her neighbour, Idris Maun, a retired schoolteacher, heard", "Constable Idris Maun, who was on foot patrol nearby, heard")],
          gold=0)),

dict(n=26, j="M", rules=["M801", "M802", "M803_2"], d=2,
q="Can Hale's words to the site clerk come in under section 803(2)?", gold=1,
doc="""Morrow Vale High Court - Brannock v. Kestrel Crane Hire Ltd
Witness summary: Ada Moreno, site clerk, Wharf Road development

At 10:40 am a pallet of roofing slate fell from a crane hook and crushed the forklift cab in which Joel Brannock was sitting, injuring him badly. The fall of the pallet was the end of the incident; nothing further happened after 10:40.

Brannock's colleague, Petrus Hale, had been standing beside the forklift and was showered with broken slate. Hale walked to the site office, sat down, pale and sweating, and kept repeating that he could have been killed. At 11:02 am, still trembling so badly that he could not hold a cup of water, he said to me, without being asked anything: "The rigger never locked the hook latch. I saw it swinging open before the lift."

No police officer was present at any point. Hale has since returned to his home country and will not testify. Brannock offers my evidence of Hale's words to prove that the hook latch was not locked.""",
twin=dict(rep=[("At 11:02 am, still trembling", "At 11:22 am, still trembling")], gold=0)),

dict(n=27, j="A", rules=["A801", "A802", "A803_2"], d=2,
q="Is Wyn's statement to Ormond admissible as an excited utterance under Rule 803(2)?", gold=1,
doc="""Arvell v. Lorne Tebbit (arson of a dwelling) - prosecution witness statement of Firefighter Bess Ormond (extract)

"At about 1:10 am on 17 January fire broke out at 14 Quarry Row. The occupants had got out before we arrived. At about 2:00 am, fifty minutes after the fire started, I found nine-year-old Wyn Sayers in the back of a neighbour's car, wrapped in a blanket. She was sobbing, had soot on her face and hands, and kept asking whether her dog had got out. I had not asked her anything. She suddenly said: 'Uncle Lorne was pouring the stuff from the red can on the stairs and then it went whoosh.' She then started screaming for her dog again."

Tebbit is Wyn's uncle. Wyn, now ten, has been found unable to testify about the night of the fire. The prosecution offers Ormond's evidence of Wyn's words to prove that Tebbit poured an accelerant on the stairs."""),

dict(n=28, j="A", rules=["A801", "A802", "A803_2"], d=2,
q="Does Oake's statement to her daughter qualify under the excited-utterance exception?", gold=0,
doc="""Estate of Marit Oake v. Jonas Fell - Arvell Circuit Court
Plaintiff's deposition summary: testimony of Signe Oake (daughter)

Pedestrian Marit Oake, aged 64, was clipped by a cyclist on the Linnet Bridge path at 9:15 am on 5 May and fell, grazing both knees. She was shaken, took a taxi home, took two painkillers, slept until about 12:30 and then made herself lunch.

At 1:10 pm her daughter Signe phoned. According to Signe, her mother was speaking in "her normal chatty voice - she even laughed about her ruined shopping." In the course of the call Marit said: "The cyclist was going flat out, he didn't ring his bell, and he was looking at his watch."

Marit Oake died in an unrelated accident before trial. Her estate wishes Signe to repeat the statement to prove that the cyclist, Fell, was riding carelessly."""),

dict(n=29, j="C", rules=["C20", "C30a"], d=2,
q="Is the recording admissible as a contemporaneous description under Article 30(a)?", gold=1,
doc="""COLDMERE EMERGENCY SERVICES - CALL TRANSCRIPT, ref. 23-88142

[23:14:05] Caller (gives name as Pim Rostova): Police please. There's a man in a grey coat climbing over the fence of the Farrier Road bus depot - right now, I'm watching him from my balcony.
[23:14:19] Operator: Can you describe him?
[23:14:22] Caller: Tall, grey coat, black beanie... he's got a crowbar. He's at the side door of the workshop now, he's levering it... it's open, he's going inside.
[23:14:40] Operator: Officers are on their way. Stay on the line.

Note for the file: At the trial of Ansel Weir for burglary of the depot workshop, Rostova cannot be traced. The prosecution offers the recording of the call to prove that the intruder carried a crowbar and forced the workshop door.""",
twin=dict(rep=[("There's a man in a grey coat climbing over the fence of the Farrier Road bus depot - right now, I'm watching him from my balcony.",
                "A man in a grey coat climbed over the fence of the Farrier Road bus depot - I watched him from my balcony, and he's gone now."),
               ("he's got a crowbar. He's at the side door of the workshop now, he's levering it... it's open, he's going inside.",
                "he had a crowbar. He levered the side door of the workshop open, went inside, and ran off toward the canal about a minute ago.")],
          gold=0)),

dict(n=30, j="M", rules=["M801", "M802", "M803_1"], d=3,
q="Is the message admissible as a present sense impression under section 803(1)?", gold=0,
doc="""Morrow Vale County Court - Ferris (a minor) v. Halcrow Aggregates Ltd
Evidence summary prepared for the case management hearing

At 17:32:10 on 4 April, Liesel Grau, waiting at the Pell Road and 4th Street lights, dictated a voice-to-text message to her husband: "Stopped at the Pell & 4th lights. A white cement truck just ran the red, nearly took out a kid on a scooter."

The junction's signal log and Grau's phone records show that the message was sent 40 seconds after the lights on the truck's approach turned red. The claimant, the scooter rider, was knocked off the scooter as the truck passed.

Grau died in March. The claimant offers the message to prove that the Halcrow truck entered the junction against a red light. No other person who saw the truck will testify: the claimant never saw the truck coming, remembers nothing of the collision and will not give evidence, and no camera covers the junction.""",
twin=dict(rep=[("No other person who saw the truck will testify: the claimant never saw the truck coming, remembers nothing of the collision and will not give evidence, and no camera covers the junction.",
                "Grau's passenger, her son Tobias, who also watched the truck go through the junction, will testify at trial; no camera covers the junction.")],
          gold=1)),

dict(n=31, j="A", rules=["A802", "A803_6"], d=2,
q="Is the log entry admissible under Rule 803(6)?", gold=1,
doc="""Arvell v. Harlan Moss (theft by an employee) - summary of records evidence

The prosecution offers page 14 of the Fairhold Distribution Centre's "Dock Exceptions Log" for 22 November, which contains the entry: "22/11 14:35 - Trailer 88 sealed with seal no. 551093; 36 pallets per loader count (per D. Ruiz)."

The entry was typed at 14:40 by dock clerk Nell Farris, who did not go onto the loading bay herself. Loader Diego Ruiz counted the pallets and radioed the count and seal number to her as he closed the trailer, as dock procedure requires on every departure.

Fairhold's logistics manager, who oversees the log and has used it daily for six years, testifies that every departing trailer is logged this way within minutes and that the log is kept as part of the centre's ordinary operations. The defence cross-examines her at length but offers no evidence suggesting that the log is inaccurate or was prepared with any unusual motive.

The prosecution offers the entry to prove that 36 pallets left in trailer 88."""),

dict(n=32, j="A", rules=["A802", "A803_6"], d=3,
q="Does Rule 803(6) permit the entry to be admitted for that purpose?", gold=0,
doc="""Anker v. Lindgate Hotel Ltd - Arvell Circuit Court
Plaintiff's exhibit 7: Night Manager's Incident Book, entry for 3 March

"01:20 - Guest Ms R. Anker (Rm 412) came to front desk, upset, holding her wrist. States she was shoved down the bar stairs by the bartender, K. Voss, after closing. Ice pack given; offered doctor, declined. - T. Mallory, night manager."

The Incident Book is kept at the front desk, and hotel policy requires the duty manager to record every incident on the premises in it at the time it is reported. The hotel's general manager, as custodian, will testify to that practice. Nothing suggests Mallory recorded the guest's words inaccurately.

In Anker's suit against the hotel for battery by its employee, Anker offers the entry to prove that Voss shoved her down the stairs. Mallory did not see what happened on the stairs; Voss denies any contact with Anker."""),

dict(n=33, j="M", rules=["M802", "M803_6"], d=2,
q="Is the job sheet admissible under section 803(6)?", gold=1,
doc="""Morrow Vale County Court - Lindqvist v. Grenfell Plumbing Ltd
Defendant's document bundle, tab 4: job sheet, 8 Lark Terrace

"Replaced cracked compression fitting under kitchen sink; system pressure-tested at 3 bar for 15 min - no drop; no leak at completion. Fitter: Sam Okoro."

The job was done on 3 February. Okoro wrote the job sheet in the firm's job book on 8 February, when he returned to the depot after a period of out-of-town work; fitters write up every job in the job book on their return, as the firm requires. Grenfell's office manager, who is the records custodian, has signed a written certificate that the job book is made and kept in the ordinary course of the firm's business.

On 20 February the kitchen at 8 Lark Terrace flooded, and the homeowner later sued Grenfell. Grenfell offers the job sheet to prove that there was no leak when the work was completed. Okoro has emigrated and will not testify.""",
twin=dict(rep=[("Okoro wrote the job sheet in the firm's job book on 8 February,", "Okoro wrote the job sheet in the firm's job book on 14 February,")], gold=0)),

dict(n=34, j="M", rules=["M802", "M803_6"], d=2,
q="Would section 803(6) admit the entry to prove the May water ingress?", gold=0,
doc="""Pruitt v. Harbourside Self-Storage Ltd - Morrow Vale Small Claims
Note for the adjudicator

Harbourside keeps a "Unit Condition Register". When a customer moves out, a member of staff inspects the unit and records its condition on the same day, as company procedure requires.

For unit C-17, the entry dated 30 June reads: "Customer reports water came through ceiling in May and damaged 3 rugs. Unit dry at inspection; faint tide mark on rear wall. - K. Oyelaran."

A written certificate from Harbourside's records custodian states that the register is made and kept in the ordinary course of the company's business and that entries are made on the day of inspection. The register predates any dispute.

The customer, Ada Pruitt, sues Harbourside for the value of the rugs and offers the entry to prove that water came through the ceiling in May. Oyelaran saw no water ingress himself, and no Harbourside employee was present at the unit in May."""),

dict(n=35, j="H", rules=["H4", "H5", "H11"], d=3,
q="Is the delivery record admissible under section 11?", gold=1,
doc="""Halvard Reach County Court - Tessel Homewares Ltd v. Ashe
Claim for the price of goods (1,850 crowns)

Portmere Couriers' delivery system stores a signature-and-scan record for each parcel. The record for parcel PX-44120, dated 9 January of last year, shows: "Delivered 11:14 - left with neighbour at no. 9 - signed: T. Ashe." The entry was keyed into a handheld device at the doorstep by the driver, Kieran Doyle, who made the delivery.

Doyle, who handles about 140 deliveries a day, is still employed by Portmere; when interviewed he said he has no memory of this parcel.

Tessel, the seller, tenders the record through a Portmere systems manager, who explains how the records are made and stored and confirms that this one has not been altered. Tessel relies on it to prove that the goods were delivered on 9 January. Ashe denies receiving them.""",
twin=dict(rep=[("Doyle, who handles about 140 deliveries a day, is still employed by Portmere; when interviewed he said he has no memory of this parcel.",
                "Doyle is still employed by Portmere and remembers this delivery well: the neighbour's dog bit him on the doorstep that morning and he reported the injury the same day.")],
          gold=0)),

dict(n=36, j="A", rules=["A804a", "A804b3"], d=2,
q="Is Vinn's statement admissible under Rule 804(b)(3)?", gold=0,
doc="""Arvell v. Callum Pryce (criminal damage to a parked hatchback) - defence proffer

The defence proposes to call Bettina Rusk, who will testify that three days after the incident her flatmate, Jory Vinn, told her, in tears: "It was me who smashed that hatchback's windows, not Callum. I was off my head."

Corroboration: Vinn's fingerprints were found on a brick recovered beside the car, and a street camera shows a figure of Vinn's build near the car at the relevant time.

Status of the declarant: Vinn has been served with a witness subpoena, is waiting in the courthouse corridor, and has not claimed any privilege or indicated that he will refuse to testify.

The prosecution objects that Rusk's evidence of Vinn's words is inadmissible hearsay. The defence relies on Rule 804(b)(3).""",
twin=dict(rep=[("Vinn has been served with a witness subpoena, is waiting in the courthouse corridor, and has not claimed any privilege or indicated that he will refuse to testify.",
                "Vinn was called by the defence, invoked his privilege against self-incrimination, and the court upheld the privilege and excused him.")],
          gold=1)),

dict(n=37, j="M", rules=["M802", "M804_3"], d=3,
q="Would section 804(3) admit Eli's statement?", gold=0,
doc="""Morrow Vale Housing Tribunal - Kestrel Housing Association v. Gideon Marsh
Possession claim: breach of tenancy (drug use in common areas)

The Association seeks possession of Marsh's flat, alleging that on several nights in March he smoked cannabis in the building's stairwell. Possession of cannabis is a criminal offence in Morrow Vale; no one has been prosecuted.

Marsh calls his aunt, Wilma Tarrant, who will testify that at a family dinner in April her son, Eli Tarrant, who often stayed at Marsh's flat, told her: "Gideon had nothing to do with it. It was me smoking in the stairwell those nights - I'll probably get arrested if anyone finds out."

Eli is alive and has been subpoenaed by the Association. Marsh offers Wilma's evidence of Eli's words to prove that Eli, not Marsh, was the person smoking in the stairwell."""),

dict(n=38, j="A", rules=["A804a", "A804b3"], d=3,
q="Is Albescu's letter admissible as a statement against interest under Rule 804(b)(3)?", gold=0,
doc="""Arvell v. Nadia Ferrante (robbery of the Wheatsheaf bakery, 2 May) - defence exhibit D4

The defence offers a letter written by Rocco Albescu, who died in prison last month, to Ferrante's lawyer. It reads: "I robbed the Wheatsheaf bakery on 2 May, not Nadia. I used her scooter so people would think it was her."

Albescu wrote the letter while serving a life sentence without possibility of release. Prison and court records show that he was arrested in Harrowgate, 300 km away, on 29 April and was in custody there continuously until his death. No other evidence links him to the robbery or to Ferrante's scooter.

The prosecution objects that the letter is inadmissible hearsay; the defence relies on Rule 804(b)(3)."""),

dict(n=39, j="H", rules=["H4", "H5", "H13"], d=3,
q="May the court admit Halm's statement under section 13?", gold=0,
doc="""Halvard Reach Crown Court - Crown v. Esme Rudd (fraud on her employer)
Defence application to adduce hearsay

Rudd, office manager of Tarrow Builders' Merchants, is charged with stealing from the petty cash over two years. The defence wishes to call Paulo Stannard, a former bookkeeper, to repeat what his colleague Grete Halm said to him in the staff kitchen last spring: "I've been skimming the petty cash for two years; Esme never knew."

Halm is a qualified accountant who knew that what she described was theft. She resigned and moved to the Western Isles Federation, outside Halvard's jurisdiction. She has written to the court saying she will not return to give evidence, and she is in good health.

The Crown opposes the application.""",
twin=dict(rep=[("She has written to the court saying she will not return to give evidence, and she is in good health.",
                "She died there of a stroke in May.")],
          gold=1)),

dict(n=40, j="H", rules=["H4", "H5", "H13"], d=2,
q="Is Pike's remark admissible under the declarations-against-interest provision?", gold=1,
doc="""Halvard Reach County Court - Estate of Morwenna Garnet v. Estate of Luther Pike
Claim: repayment of an 800-crown loan

Garnet's estate claims that Garnet lent Luther Pike 800 crowns to repair his roof and that the loan was never repaid. Pike died in January; his estate denies that any loan was made.

Pike's nephew, Callum Pike, will testify that at Christmas, while the two of them were going through Luther's household accounts, Luther said: "Don't forget I still owe Morwenna eight hundred from the roof loan - that has to be paid before anything else."

Luther Pike was a retired bank manager who kept meticulous accounts and was mentally sharp until his death. The claimant offers Callum's evidence of the remark to prove the debt remains outstanding."""),

dict(n=41, j="C", rules=["C20", "C31"], d=2,
q="Is Kell's statement to Mott admissible under Article 31?", gold=1,
doc="""Coldmere Civil Court - Tanner v. Riggs Haulage Ltd (road collision)

Tanner claims that Riggs Haulage's lorry driver, Boris Kell, caused the collision in which Tanner was injured. Tanner wishes to call Kell's former partner, Anya Mott, who will testify that the day after the collision Kell told her: "I'd had four pints before I took the lorry out. If the firm finds out I'm finished, and I'll owe them for the damage."

Kell is not a party. Tanner served him with a witness summons. At the hearing he entered the witness box and, when asked about the collision, said he would not answer. The judge ordered him to answer; he still refused and was held in contempt.

Riggs Haulage objects to Mott's evidence as hearsay.""",
twin=dict(rep=[("Tanner served him with a witness summons. At the hearing he entered the witness box and, when asked about the collision, said he would not answer. The judge ordered him to answer; he still refused and was held in contempt.",
                "He told Tanner's solicitor by phone that he \"won't be coming to any hearing\"; Tanner has not sought a witness summons or any court order, although Kell lives locally.")],
          gold=0)),

dict(n=42, j="A", rules=["A801", "A802", "A803_1"], d=2,
q="Does Rule 803(1) allow the recording of Nemeth's words to be admitted?", gold=1,
doc="""Arvell v. Gareth Lowe (dangerous driving) - transcript of exhibit P9
Video-doorbell recording, 6 Fairmead Close. Audio only is relevant; the camera faced the driveway, not the road.

[22:47:31] Loud engine note and a screech of tyres from the direction of the road.
[22:47:33] Male voice (householder Aurel Nemeth, calling to someone indoors): "That black saloon must have been doing ninety - he's just gone straight through the stop sign at the end of the close without even slowing!"
[22:47:40] Female voice (indoors): "What?"
[22:47:42] Nemeth: "Never mind, he's gone."

Nemeth has since died. The prosecution offers the recording to prove that the black saloon, which Lowe admits he was driving, went through the stop sign without stopping."""),

dict(n=43, j="C", rules=["C20", "C30b"], d=2,
q="Is Achebe's statement admissible as an excited utterance under Article 30(b)?", gold=1,
doc="""Coldmere Civil Court - Achebe v. Stonecroft Builders Ltd
Witness statement of Dmitri Lasko (passer-by), paragraphs 3-6

3. At 16:02 on 11 June a scaffold plank fell from the fourth floor of the Stonecroft building site on Ennis Row and hit the pavement about a metre from a woman I now know to be Ruth Achebe.
4. Ms Achebe screamed and collapsed against a wall, hyperventilating. I stopped to help her.
5. At 16:09 by my phone, still gasping and crying, she said to me: "The man up there in the orange hard hat kicked it off - I saw him do it!"
6. I gave my details to the site manager.

Note: Ms Achebe has refused to give evidence despite a court order. She relies on Mr Lasko's evidence of her words to prove that a Stonecroft worker kicked the plank off the scaffold.""",
twin=dict(rep=[("5. At 16:09 by my phone,", "5. At 16:14 by my phone,")], gold=0)),

dict(n=44, j="A", rules=["A801", "A802", "A803_1"], d=2,
q="Does the voicemail qualify as a present sense impression under Rule 803(1)?", gold=0,
doc="""Voicemail received at 08:52 on 14 October, customer line, Dunmore Water Authority (transcribed):

"Hi, it's Tilde Vasko at 30 Reedmoor Road. About twenty minutes ago - around half past eight - I watched your contractor's digger rip right through the gas pipe outside number 32. There was a big hiss and the whole crew ran. I've been sitting here with my coffee since, thinking I really ought to report it. Anyway, that's what I saw. Bye."

Note for counsel: In the claim by the owner of 32 Reedmoor Road against the contractor, Ostler Groundworks, for damage caused by the gas escape, the owner offers the voicemail to prove that Ostler's digger severed the gas pipe. Ostler says the pipe was already fractured. Vasko cannot now be located despite reasonable efforts."""),
]
