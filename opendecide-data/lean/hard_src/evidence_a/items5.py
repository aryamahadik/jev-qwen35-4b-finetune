"""Items 82-99: purpose of offer (choice) and business-record requirement analysis (choice)."""

from rules import P_TRUTH, P_EFFECT, P_VERBAL, P_IMPEACH, P_MIND

ITEMS = [
dict(n=82, j="A", rules=["A801"], opts="PURPOSE", d=2,
q="For which purpose is the groom's statement to the owner being offered?", gold=P_EFFECT,
doc="""Holm v. Quarry Lane Riding School - Arvell Circuit Court
Plaintiffs' outline of evidence (extract)

Eleven-year-old Pia Holm was thrown from a pony named Tinder during a beginners' lesson on 4 June. Her parents sue the school, alleging that it knew Tinder was dangerous for beginners and used him anyway.

The plaintiffs will call a former groom, Rhian Castell, who will testify that a month before the accident she told the school's owner: "Tinder has bolted with three different kids this week - he shouldn't be used for beginners."

The owner admits that Tinder had bolted with beginners before the accident but insists she did not know about it until after Pia's fall. Castell's evidence is offered on the question of what the owner knew before 4 June.""",
twin=dict(rep=[("The owner admits that Tinder had bolted with beginners before the accident but insists she did not know about it until after Pia's fall. Castell's evidence is offered on the question of what the owner knew before 4 June.",
                "The owner admits that Castell said this to her but denies that Tinder had ever bolted with anyone before 4 June. Castell's evidence is offered on the question of whether Tinder had in fact bolted with beginners before the accident.")],
          gold=P_TRUTH)),

dict(n=83, j="A", rules=["A801"], opts="PURPOSE", d=2,
q="How is Lunde using Rosa Carrick's words?", gold=P_VERBAL,
doc="""Lunde Boatworks v. Carrick Marine - Arvell Commercial List
Claimant's witness summary: Stig Arnesen, yard foreman

On 2 April, Carrick Marine's director, Rosa Carrick, telephoned the yard. Arnesen had quoted her 3,100 marks per dinghy the previous week. According to Arnesen, she said: "I'll take the two dinghies at three thousand one hundred each, delivered by the end of May - consider that a firm order."

Lunde built and tendered both dinghies in May; Carrick refused delivery. Carrick's defence is that no order was ever placed and that Rosa Carrick "was only asking about availability."

Lunde offers Arnesen's evidence of Rosa Carrick's words."""),

dict(n=84, j="A", rules=["A801"], opts="PURPOSE", d=2,
q="What is the prosecutor's purpose in putting the text message to Moll?", gold=P_IMPEACH,
doc="""Arvell v. Kade Olsson (assault in the Kestrel superstore car park)
Transcript note, day 2

Eyewitness Freya Moll testified for the defence that the man who threw the first punch was "short and bald." Olsson is tall with thick dark hair.

On cross-examination, the prosecutor asked Moll about a text she sent her husband an hour after the fight: "Some tall guy with a mop of dark hair just decked a man outside the Kestrel superstore."

In argument on the defence objection, the prosecutor told the judge that the victim and two other witnesses have already identified Olsson as the attacker, that she will ask the jury to consider the text only in deciding whether Moll's account in court can be relied on, and that she does not object to a limiting instruction.""",
twin=dict(rep=[("that the victim and two other witnesses have already identified Olsson as the attacker, that she will ask the jury to consider the text only in deciding whether Moll's account in court can be relied on, and that she does not object to a limiting instruction.",
                "that no other witness saw who threw the first punch, and that she will ask the jury to find, on the strength of the text, that the man who threw the first punch was tall with a mop of dark hair.")],
          gold=P_TRUTH)),

dict(n=85, j="A", rules=["A801"], opts="PURPOSE", d=2,
q="What is the most accurate description of the purpose for which the nephews offer Crum's words?", gold=P_MIND,
doc="""In re the Will of Balthazar Crum - Arvell Probate Court
Caveators' statement of issues

Crum's nephews challenge his will, executed on 10 June, on the sole ground that he lacked testamentary capacity when he signed it.

They will call his housekeeper, Mrs. Ines Barrow, who will testify that on 8 June Crum told her, in all seriousness and at some length: "I am the rightful Emperor of the Moon, and the Sisters of the Tide are poisoning my soup."

No one suggests that Crum was an emperor of anything or that anyone was poisoning his soup."""),

dict(n=86, j="A", rules=["A801"], opts="PURPOSE", d=3,
q="What is the invoice being used for?", gold=P_TRUTH,
doc="""Ferro v. Greyleaf Tree Surgeons Ltd - Arvell Small Claims
Claimant's note to the adjudicator

Tamsin Ferro claims that Greyleaf overcharged her 2,400 marks for felling a beech tree in her garden, and seeks the difference between that figure and a reasonable price. Greyleaf says she agreed to 2,400 marks.

Ferro offers an invoice from a rival firm, Oakhollow Arborists, dated the same month and addressed to her neighbour, for "removal of 20 m beech, rear garden, including stump grinding - 900 marks." Ferro obtained it from the neighbour. No one from Oakhollow will testify.

Ferro's note says: "This invoice shows that 900 marks was what a comparable job actually cost on our street that month." """),

dict(n=87, j="A", rules=["A801"], opts="PURPOSE", d=3,
q="In what capacity are Tamm's words offered?", gold=P_VERBAL,
doc="""Penhale v. Morven Autos Ltd - Arvell Circuit Court
Claim: fraudulent misrepresentation on the sale of a used van

Idris Penhale bought a used van from Morven Autos after the salesman, Jory Tamm, told him: "The cambelt was replaced at sixty thousand kilometres - here's the stamp in the service book." Relying on that, Penhale paid the asking price.

The cambelt had never been replaced; it snapped a month later and destroyed the engine. Morven's workshop records and an engineer's report prove that no replacement was done.

Penhale's claim is that Morven, through its salesman, made a false statement of fact that induced the purchase. Morven denies that Tamm said anything about the cambelt. Penhale will testify to Tamm's words; Tamm has left Morven and is not a party."""),

dict(n=88, j="A", rules=["A801"], opts="PURPOSE", d=2,
q="Which purpose best describes the prosecutor's use of the anonymous caller's words?", gold=P_EFFECT,
doc="""Arvell v. Solveig Marr (handling stolen goods)
Note of argument on a defence objection

Detective Bram Heller testifies that on 3 August he and two officers went to a garage behind 12 Coopers Row, rented by Marr, because an anonymous caller had told the police tip line: "There are six stolen e-bikes in the blue garage behind 12 Coopers Row."

In opening, the defence described the investigation as "a fishing expedition that targeted Ms. Marr for no reason at all."

The prosecutor says she needs the tip to explain why the officers went to that particular garage. The theft of the e-bikes and their presence in the garage are proved by the owners' evidence and the officers' own observations, and the judge has said she will instruct the jury not to treat the call as evidence that anything was stolen or was in the garage."""),

dict(n=89, j="A", rules=["A801"], opts="PURPOSE", d=2,
q="What is the prosecution's purpose in offering Liesel's words?", gold=P_TRUTH,
doc="""Arvell v. Konrad Weil (attempted murder by poisoning)
Prosecution notice of evidence

Weil's wife, Liesel Weil, is recovering in hospital from arsenic poisoning and has been found unable to testify. Two weeks before she was admitted, she telephoned her sister, Anke, and said: "Konrad has been putting something in my tea - I'm sure of it. I feel sick every time he makes it."

The prosecution will call Anke to repeat the call. The prosecution's case theory, set out in its opening note, is that Weil dosed his wife's tea with arsenic over several weeks. There is no dispute that Liesel was poisoned; the only issue is who did it."""),

dict(n=90, j="A", rules=["A801"], opts="PURPOSE", d=3,
q="Which characterisation best fits the estate's use of Pike's forum post?", gold=P_MIND,
doc="""Estate of Rhea Solberg v. Ansgar Pike - Arvell Circuit Court
Plaintiff's exhibit list, item 12

Rhea Solberg died when a tractor she had borrowed from her neighbour, Ansgar Pike, rolled over on a slope. The estate alleges that Pike knew the tractor's rollover bar was cracked and lent it anyway.

Item 12 is a message Pike posted on a farmers' online forum a month before the accident: "Anyone know a welder near Kessel? The rollover bar on my old Brannock tractor has a crack right through the left upright."

Pike concedes that the bar was cracked at the time of the accident; that is established by the inspector's report. His defence is that he did not know about the crack before lending the tractor."""),

dict(n=91, j="A", rules=["A801"], opts="PURPOSE", d=2,
q="Which option describes how Linwood's counsel proposes to use Selby's email?", gold=P_IMPEACH,
doc="""Linwood v. Harcastle Builders Ltd - Arvell High Court
Note of argument, day 4

Site engineer Omar Selby testified for Harcastle that he personally inspected the scaffolding on the morning it collapsed.

Linwood's counsel produces Selby's email to his manager, sent the evening after the collapse: "I never got round to the scaffold inspection that morning - too many deliveries."

Linwood already has independent proof, from the site's electronic inspection system, that no inspection was logged that morning. Counsel tells the judge that she wants the jury to use the email only in deciding whether Selby's evidence today can be trusted, and she agrees to a limiting instruction."""),

dict(n=92, j="A", rules=["A803_6"], opts="BRA", d=2,
q="Which requirement of Rule 803(6), if any, does the batch 7 entry fail?", gold="made at or near the time",
doc="""Delacroix Vineyards v. Tallis Cooperage Ltd - Arvell Commercial List
Note of evidence: Tallis's quality manager, Ingrid Sollo

Tallis supplied oak barrels to Delacroix; Delacroix alleges that 40 barrels leaked. Tallis offers page 31 of its "Barrel Test Book", which records: "Batch 7 - 40 barrels pressure-tested, no leaks, 14 Sept - C. Aske."

Ms. Sollo, who keeps the book, testifies that every batch is pressure-tested before dispatch, that the tester records the result in the book, that the book is kept in the ordinary course of Tallis's business, and that Aske was the tester for batch 7.

On cross-examination she explains that Aske wrote the batch 7 entry in June of the following year, copying the result from the test rig's printed pressure strip, which has since been discarded. Delacroix offers no evidence suggesting that the entry is inaccurate.""",
twin=dict(rep=[("Aske wrote the batch 7 entry in June of the following year, copying", "Aske wrote the batch 7 entry on 14 September, as the test finished, copying")],
          gold="every requirement is satisfied")),

dict(n=93, j="A", rules=["A803_6"], opts="BRA", d=2,
q="Which element of Rule 803(6), if any, is missing?", gold="making the record was a regular practice",
doc="""Fenwick Transport Ltd v. Oriel Insurance plc - Arvell High Court
Claim under a fleet policy for a lorry destroyed by fire

Oriel alleges that the lorry had not been serviced, in breach of a policy condition. Fenwick offers a typed memo written by its fleet supervisor, Ilse Kahn, on the day of the service: "Lorry FT-12 fully serviced today by me: filters, belts, brakes, wiring loom inspected."

Fenwick's general manager, who is custodian of the company's vehicle files, testifies that the memo was placed in the lorry's file, which is kept as part of Fenwick's ordinary operations. She also testifies that Fenwick does not ordinarily make any written record of services - Kahn wrote this memo on her own initiative because she was about to go on holiday - and that no other such memo exists for any vehicle.

Kahn performed the service herself. Oriel suggests no reason to doubt the memo's accuracy."""),

dict(n=94, j="A", rules=["A803_6"], opts="BRA", d=2,
q="Which Rule 803(6) condition, if any, has not been satisfied?", gold="foundation by custodian or certification",
doc="""Salton Dental Practice v. Mira Pollard - Arvell Small Claims (unpaid treatment bill)

Salton offers a printout from its computerised treatment ledger showing a crown fitted to Pollard on 6 May. The entry bears the treating dentist's user code and a time stamp of 11:52 on 6 May, the end of the appointment.

The printout was handed up by Kit Lamb, a trainee at Salton's solicitors, who explained that he "downloaded it from the portal the practice gave us" and has no other knowledge of the practice or its systems. No one from Salton testifies about its records, and no certification from any custodian has been filed.

Pollard does not suggest that the entry is inaccurate; she says that she cannot afford to pay."""),

dict(n=95, j="A", rules=["A803_6"], opts="BRA", d=2,
q="Which requirement of Rule 803(6), if any, is unmet?", gold="every requirement is satisfied",
doc="""Arvell v. Nadine Castellan (theft by a bank employee)
Prosecution exhibit P6: Vault Count Sheet, Kessel branch, Arvell Savings Bank, 30 June

"Opening vault cash 412,600 - count by R. Ivers & N. Castellan, 08:02. Closing vault cash 402,600 - count by R. Ivers & D. Moll, 18:05."

Branch procedure requires two tellers to count the vault at opening and at close each day and to sign the sheet immediately after each count. The branch operations manager, who supervises the sheets and is responsible for keeping them, testifies to this procedure and that the sheets are kept in the branch's records.

The defence cross-examines the manager about whether the counts could have been wrong, but produces no evidence that the procedure was not followed that day or that the sheet was altered."""),

dict(n=96, j="A", rules=["A803_6"], opts="BRA", d=3,
q="Which requirement of Rule 803(6), if any, does the entry fail for that purpose?", gold="made by or from someone with knowledge acting in the activity",
doc="""Holloway v. Brisk Couriers Ltd - Arvell Small Claims (lost parcel)

Holloway claims that Brisk lost a parcel addressed to her tenant at 13 Ferry Lane. Brisk offers its "Delivery Exceptions Report" for 9 March, which states: "PX-7713: neighbour at no. 11 (name not given) told driver by intercom that recipient had moved away months ago; parcel returned to depot."

The driver, Emil Hart, typed the entry on his handheld at the doorstep, as Brisk requires for every failed delivery. Brisk's depot manager testifies to the system and that the reports are kept as part of Brisk's operations. Holloway offers nothing to suggest that Hart recorded what he heard inaccurately.

Brisk offers the entry to prove that the recipient had moved away before 9 March."""),

dict(n=97, j="A", rules=["A803_6"], opts="BRA", d=3,
q="Which Rule 803(6) requirement, if any, defeats admission of the Falls Register entry?", gold="no indication of untrustworthiness",
doc="""Cavell v. Northgate Care Home Ltd - Arvell Circuit Court

Cavell's father, a resident at Northgate, fell and broke his hip in the early hours of 11 January. Northgate offers the entry in its "Falls Register" written at 03:25 by the night supervisor, Anton Veyle: "Resident found on floor at 03:05; bed rails up and alarm mat in place; resident had climbed over rails."

Northgate's manager testifies that the register is kept for every fall and must be completed within the hour by the staff member who finds the resident, and that Veyle found Cavell's father.

Cavell's counsel then produces undisputed evidence that Veyle had been formally warned the previous week that he would be dismissed if another fall occurred on his shift with bed rails down, and a photograph taken by a paramedic at 03:15 showing the bed rails lowered and no alarm mat by the bed."""),

dict(n=98, j="M", rules=["M803_6"], opts="BRM", d=3,
q="Which condition of section 803(6), if any, prevents the report being admitted?", gold="not prepared in contemplation of litigation",
doc="""Aldren v. Castlebay Ferries Ltd - Morrow Vale County Court

Passenger Joan Aldren slipped on the car deck of the MV Kittiwake on 1 September and fractured her wrist.

On 2 September the ship's purser, Nils Ekberg, completed Castlebay's standard "Passenger Injury Report". Castlebay's claims department requires this report to be completed within 48 hours of any passenger injury, "so that the company can assess and respond to any claim that may follow." Ekberg personally inspected the deck and recorded: "Deck dry, non-slip coating intact, passenger wearing heeled sandals."

The records custodian has signed a written certificate that the report was made and kept in the ordinary course of Castlebay's business. Ekberg has since left Castlebay and will not testify. Castlebay offers the report to prove that the deck was dry."""),

dict(n=99, j="M", rules=["M803_6"], opts="BRM", d=2,
q="What element of section 803(6), if any, is not met?", gold="personal knowledge or employee source",
doc="""Pellham Estates Ltd v. Ruddock Roofing Ltd - Morrow Vale County Court

Pellham's building manager keeps a "Contractor Works Log". On 18 April she wrote, the same day: "Scaffolding at Block C struck and cracked window C-14 today - per Gus Talbot, foreman of Hurst Scaffolding (Ruddock's subcontractor), who phoned me from site."

The manager did not see the incident. The log is kept in the ordinary course of Pellham's business and was begun years before any dispute; Pellham's records custodian has provided a written certificate.

Pellham offers the entry against Ruddock to prove that the scaffolding cracked the window."""),
]
