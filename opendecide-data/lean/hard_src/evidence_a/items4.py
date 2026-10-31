"""Items 61-81: which exception, if any (choice over the jurisdiction's menu)."""

ITEMS = [
dict(n=61, j="A", rules=["MENU_A"], opts="EXC", d=2,
q="Which provision, if any, makes the recording admissible?", gold="present sense impression",
doc="""Transcript, Dunmore emergency line, 19:22:10, 6 November

Caller (Hollis Brandt, a long-haul lorry driver, speaking evenly): "I'm northbound on the Ring Road behind a silver hatchback, registration starting KT4. He's drifting across both lanes - there, he's just touched the central barrier and carried straight on. Now he's back in lane one doing maybe forty."
Operator: "Stay well back, sir."
Caller: "Will do. He's taking the Fenwick exit now."

Later in the call Brandt remarked, in the same even tone, that he had "seen worse on the Ring Road any night of the week."

Brandt died in an unrelated collision in March. In the prosecution of the hatchback's driver, Ottar Klein, for careless driving, the prosecution offers the recording to prove that the hatchback struck the central barrier. Klein denies touching the barrier."""),

dict(n=62, j="M", rules=["MENU_M"], opts="EXC", d=2,
q="Under which provision of the Code, if any, is Varn's statement to the foreman admissible to prove that Doyle was on his phone?", gold="excited utterance",
doc="""Morrow Vale High Court - Ilse Varn v. Tolbert Timber Yard Ltd
Witness statement of Aled Price, yard foreman (extract)

"At 14:10 on 9 March a forklift reversing across the yard pinned Ilse Varn's leg against a stack of beams. We had freed her by 14:15; the forklift had stopped and nothing else happened after that. She lay on the ground screaming with pain.

At 14:20, before any police or ambulance arrived, she shouted to me as I knelt beside her: 'Doyle reversed without even looking - he was on his phone!'"

Doyle, the forklift driver, denies using his phone. Varn will testify at trial, but she now remembers nothing of the first hour after the accident. The claimant offers Price's evidence of her words to prove that Doyle was using his phone while reversing.""",
twin=dict(rep=[("At 14:20, before any police or ambulance arrived,", "At 15:00, before any police or ambulance arrived,")], gold="none of these")),

dict(n=63, j="C", rules=["MENU_C"], opts="EXC", d=2,
q="Which provision, if any, admits the October temperature sheet to prove that the chamber stayed at or below -21°C?", gold="business record",
doc="""Coldmere Commercial Court - Frostline Cold Storage Ltd v. Brevik Seafoods Ltd
Claim for storage fees; counterclaim for spoiled prawns

Brevik alleges that freezer chamber 3 at Frostline's Keel Street site rose above -18°C during October. Frostline offers its "Chamber 3 Temperature Sheet" for October.

Under Frostline's standing procedure, the duty technician reads the chamber thermometer at the start of each eight-hour shift and writes the reading on the sheet within the hour, adding his or her initials. Every reading on the October sheet is -21°C or colder.

Frostline's operations manager, who is the custodian of the temperature sheets and has supervised them for nine years, testifies to the procedure. Brevik first notified any claim in December. None of the technicians will testify.""",
twin=dict(rep=[("writes the reading on the sheet within the hour, adding his or her initials.",
                "writes the reading on the sheet within the hour, adding his or her initials. The October sheet, however, was left blank during the month and was filled in on 20 November by the technicians, from memory.")],
          gold="none of these")),

dict(n=64, j="A", rules=["MENU_A"], opts="EXC", d=2,
q="Which exception, if any, would admit Horace Quill's statement to prove that the deposit remains unpaid?", gold="statement against interest",
doc="""Liang v. Hartwell Bonding Co. - Arvell Circuit Court (civil)

In 2021 Petra Liang paid Horace Quill a 9,000-mark deposit toward the purchase of his Marsh Lane lot. Hartwell Bonding Co. guaranteed the refund of the deposit if the sale failed. The sale fell through. Liang says the deposit was never refunded and sues Hartwell on the guarantee; Hartwell says Quill repaid it in cash.

Quill died in January; his estate is insolvent and is not a party.

Quill's brother, Felix, will testify that last summer, over dinner, Horace told him: "I made a mess of that Marsh Lane business. I still owe Petra Liang her nine thousand deposit, and I haven't got it." Felix says Horace was calm and "just unburdening himself" over a glass of wine.

Liang offers Felix's evidence of Horace's words."""),

dict(n=65, j="M", rules=["MENU_M"], opts="EXC", d=3,
q="Which provision, if any, permits Dorland to repeat Wilde's words to show that the cannabis was Wilde's?", gold="none of these",
doc="""Morrow Vale Employment Tribunal - Pratt v. Castlebrook Plumbing Ltd (unfair dismissal)

Castlebrook dismissed plumber Ansel Pratt after a supervisor found a bag of cannabis in the glovebox of the company van assigned to him. Pratt says his friend Jonah Wilde, who does not work for Castlebrook, borrowed the van with Pratt's permission over the weekend before the discovery.

Pratt calls Neve Dorland, who will testify that at a pub quiz a fortnight after the dismissal Wilde told her, grinning: "Ansel got sacked over my weed - that bag in the glovebox was mine."

Possession of cannabis is a criminal offence in Morrow Vale. Wilde has not been prosecuted. He has been summoned by Castlebrook and will attend the hearing."""),

dict(n=66, j="H", rules=["MENU_H"], opts="EXC", d=2,
q="Which provision, if any, of the Halvard Act lets Kerr's evidence of Moor's words be admitted?", gold="spontaneous statement",
doc="""Halvard Reach High Court - Estate of Nell Ashdown v. Corrig Bus Company
Statement of paramedic Shona Kerr (extract)

At 08:05 on 3 February a Corrig bus mounted the pavement on Tannery Hill and struck Nell Ashdown, who died at the scene. A passenger, Elias Moor, climbed out through the emergency door and sat on the kerb a few metres from the body.

Kerr reached him at about 08:25. Her notes record that he was "white, shaking uncontrollably, repeatedly looking at the body, unable to give his own address." Without any prompting he said to her: "The driver was texting - he had the phone on the wheel - and he never braked."

Moor died of a heart condition in February. The estate tenders Kerr's evidence of Moor's words to prove that the driver was texting."""),

dict(n=67, j="A", rules=["MENU_A"], opts="EXC", d=2,
q="What is the correct basis, if any, for admitting Rask's letter on the knowledge issue?", gold="not hearsay",
doc="""Holt v. Orrin Lettings Ltd - Arvell Circuit Court
Plaintiff's note on disputed exhibits

Kasimir Holt was injured when the balcony of his rented flat collapsed. The only live issue on liability is whether Orrin knew of the danger before the collapse. The balcony's defective condition is established by the council engineer's report and is not disputed.

Holt offers a letter his downstairs neighbour, Dagny Rask, sent to Orrin's property manager on 3 March: "The balcony above mine is visibly sagging and there are cracks in the brackets. Please inspect it before someone gets hurt."

The property manager admits receiving and reading the letter. Rask has since moved abroad and will not testify. Orrin objects that the letter is hearsay."""),

dict(n=68, j="C", rules=["MENU_C"], opts="EXC", d=3,
q="Which Coldmere provision, if any, makes Solis's statement admissible for the defence?", gold="statement against interest",
doc="""Coldmere Criminal Court - State v. Felix Arno (burglary of the Moss Street pharmacy)
Defence notice of hearsay evidence

The defence will call Dita Kaur, who will testify that her late partner, Ruben Solis, told her one evening in their kitchen, a week after the burglary: "I did the Moss Street pharmacy job. Felix wasn't even there."

Solis was killed in a road accident in April.

The prosecution responds that nothing else connects Solis with the burglary, that there is no corroboration of any kind for the statement, and that Solis had a well-known dislike of the police and "would have said anything to get a friend off." """),

dict(n=69, j="C", rules=["MENU_C"], opts="EXC", d=2,
q="Which Coldmere provision, if any, admits Brandt's words?", gold="contemporaneous description",
doc="""Coldmere Civil Court - Linnea Dahl v. Ferris Removals Ltd (missing furniture)

Dahl's neighbour, Olek Brandt, a retired removal man, was on the phone to Dahl, who was at work, while watching the Ferris crew from his front step. Dahl recorded the call. In a relaxed, amused voice Brandt says on the recording:

"They're carrying your walnut sideboard out now... two of them... they're not putting it in the Ferris lorry, they're loading it into a little white van with no markings, parked behind."

Brandt died in March. The sideboard never arrived at Dahl's new house. Dahl offers the recording to prove that the sideboard was loaded into the unmarked van.""",
twin=dict(rep=[("was on the phone to Dahl, who was at work, while watching the Ferris crew from his front step.",
                "phoned Dahl, who was at work, a few seconds after the Ferris crew had finished loading and driven off, having watched them from his front step."),
               ("They're carrying your walnut sideboard out now... two of them... they're not putting it in the Ferris lorry, they're loading it into a little white van with no markings, parked behind.",
                "They've just carried your walnut sideboard out... two of them... they didn't put it in the Ferris lorry, they loaded it into a little white van with no markings, and it's driven off.")],
          gold="none of these")),

dict(n=70, j="A", rules=["MENU_A"], opts="EXC", d=2,
q="On what basis, if any, can the triage entry be admitted for that purpose?", gold="business record",
doc="""Ilic v. Castell Ice Rink Ltd - Arvell Circuit Court
Plaintiff's exhibit 3: triage record, Dunmore General Hospital

Rowan Ilic claims he slipped on an unmarked wet patch at the rink; the rink contends that he was drunk. Ilic arrived at the emergency department at 22:15.

The triage record contains the entry: "No odour of alcohol noted. Speech clear. Pupils equal and reactive. - H. Blom, RN." Nurse Blom assessed him at 22:20. Hospital procedure requires the triage nurse to complete the triage record for every patient she assesses as soon as her caseload allows, and in any event before the end of her shift; Nurse Blom completed this one at 23:05.

The hospital's records custodian has provided a certification that triage records are made and kept in this way as a regular practice. Nurse Blom has emigrated. Nothing suggests the record is unreliable. Ilic offers the entry to prove that he had not been drinking."""),

dict(n=71, j="A", rules=["MENU_A"], opts="EXC", d=3,
q="Which exception, if any, admits Dinescu's account as recorded in the report?", gold="none of these",
doc="""Dunmore Police - Collision Report No. 44-1187 (extract)
Reporting officer: Constable Tobias Ferr

"Attended Brennan Street / Lowe Avenue at 17:55; collision reported at 17:15. Spoke to witness Mr Aurel Dinescu, who was sitting on a bench eating a sandwich while he waited to give his account. He stated calmly that the red van (Vehicle 2) drove through the lights as they turned red and struck Vehicle 1. I did not see the collision."

The report was completed by Constable Ferr on the day of the collision, as the traffic unit requires for every collision, and the unit's records custodian will testify to that practice.

In a civil action by the driver of Vehicle 1 against the van's owner, the plaintiff offers the report's account of Dinescu's words to prove that the van ran the red light. Dinescu cannot be found despite diligent efforts."""),

dict(n=72, j="H", rules=["MENU_H"], opts="EXC", d=2,
q="Which provision of the Halvard Act, if any, allows the dispatch-book entry to be admitted?", gold="business record",
doc="""Halvard Reach County Court - Marlow Timber Ltd v. Keane Joinery (unpaid invoice)

Marlow tenders page 212 of its yard dispatch book, recording: "14 Mar - 60 lengths oak 4x2 to Keane Joinery, Quay St - loaded by F. Oduya, signed out at gate."

Dispatch-book entries are written at the gate by the loader who has just loaded the lorry. Felix Oduya, a casual loader, left Marlow's employment last year. Marlow's solicitors made inquiries at his last known address, with former colleagues and through a tracing agent, without finding him.

Keane denies ever receiving the timber."""),

dict(n=73, j="H", rules=["MENU_H"], opts="EXC", d=2,
q="Under which provision, if any, can Moreau repeat Brack's words for the defence?", gold="declaration against interest",
doc="""Halvard Reach Crown Court - Crown v. Ormond Leary (arson of the Weir Street warehouse)
Defence application to adduce hearsay

Leary calls Agathe Moreau, a volunteer prison visitor. She will testify that three weeks before he died of cancer, inmate Silas Brack told her quietly during a visit: "The Weir Street fire was mine. I set it for the insurance money, on the owner's behalf, and I let Ormond take the blame."

Brack, a former firefighter, was well aware that arson carries a long prison sentence and that he had never been suspected of it. He died in March. The Crown opposes the application."""),

dict(n=74, j="M", rules=["MENU_M"], opts="EXC", d=3,
q="Which provision, if any, admits Ennis's report for that purpose?", gold="none of these",
doc="""Morrow Vale County Court - Quill v. Branmore Leisure Centre Ltd

On 3 May swimmer Adela Quill cut her foot on a broken tile in the main pool. On 5 May, after Quill's solicitor sent a letter threatening proceedings, Branmore's safety officer, Kurt Ennis, inspected the pool and wrote an "Incident Investigation Report" concluding: "Tile damage consistent with impact from a dropped object on 3 May; pool inspected at 07:00 that day by me and tile intact."

Branmore's policy requires such reports only for incidents in which a claim has been threatened. Branmore's records custodian has provided a written certificate for the report. Ennis has left Branmore and cannot be traced.

Branmore offers the report to prove that the tile was intact at 07:00 on 3 May."""),

dict(n=75, j="A", rules=["MENU_A"], opts="EXC", d=3,
q="Which of the exceptions quoted above, if any, admits Esk's words?", gold="none of these",
doc="""Arvell v. Corvin Stade (murder) - prosecution witness summary: Ada Linwood

At 19:30 on the night Mara Esk disappeared, Esk telephoned her friend Ada Linwood. According to Linwood, Esk sounded cheerful and relaxed and said: "I'm driving out to meet Corvin at the old boathouse at nine - wish me luck."

Esk's body was found near the boathouse two days later.

The prosecution offers Linwood's evidence of Esk's words to prove that Esk went to the boathouse that night to meet Stade. Stade denies that any meeting was arranged."""),

dict(n=76, j="C", rules=["MENU_C"], opts="EXC", d=2,
q="Which Coldmere provision, if any, permits the mother to repeat Oscar's words?", gold="excited utterance",
doc="""Coldmere Civil Court - Bryony Hale (for Oscar Hale, a minor) v. Tavish Greer (dog bite)

At 12:31 on 8 May a dog bit eight-year-old Oscar Hale in Greer's front garden. At 12:37, still sobbing and holding his arm, Oscar ran into his mother's kitchen next door and cried: "Mr Greer opened his gate and told the dog to get me!"

His mother will repeat the words. Oscar, now nine, has been found by the court to be too distressed to give evidence. Greer denies opening the gate or encouraging the dog."""),

dict(n=77, j="A", rules=["MENU_A"], opts="EXC", d=2,
q="Which Arvell provision, if any, admits Coste's words for that purpose?", gold="excited utterance",
doc="""Estate of Ilan Weiss v. Portmere Chemical Ltd - Arvell High Court
Witness summary: paramedic Johan Sturla

At 03:10 on 12 February a storage tank exploded at Portmere Chemical's Harbour Road plant, killing operator Ilan Weiss. Shift technician Mirela Coste was blown off her feet and burned on one arm.

At about 03:35, as she was being loaded into the ambulance, screaming and trying to get back to the tank to find Weiss, she shouted to Sturla: "The night crew left the relief valve on tank 3 wired shut - I told them!"

Coste later died of her injuries. The estate offers Sturla's evidence of her words to prove that the relief valve on tank 3 had been wired shut.""",
twin=dict(rep=[("screaming and trying to get back to the tank to find Weiss, she shouted to Sturla:",
                "having been sedated and bandaged, she chatted quietly with Sturla about the shift rota and then remarked:")],
          gold="none of these")),

dict(n=78, j="M", rules=["MENU_M"], opts="EXC", d=2,
q="Which section of the Code, if any, admits Soren's recorded words?", gold="present sense impression",
doc="""Morrow Vale Magistrates' Court - Wexford Borough Council v. Idris Callow (obstructing a fire hydrant)

Council parking wardens Hilde Soren and Pavel Ruzicka, a trainee, were on patrol together on Pike Street. At 10:14:05 Soren spoke into her body-worn recorder: "Silver estate, registration CX71 KLM, now parked across the hydrant outside number 40, driver walking away towards the bakery."

Ruzicka saw the same thing and will testify. Soren is on maternity leave and will not testify. No custodian's certificate has been produced for the recording.

The council offers the recording to prove that Callow's car was parked across the hydrant."""),

dict(n=79, j="M", rules=["MENU_M"], opts="EXC", d=3,
q="Which Code provision, if any, admits Keel's statement for Dray?", gold="statement against interest",
doc="""Morrow Vale County Court - Byrne v. Ottoline Dray (price of a racehorse)

Harlan Byrne sues Ottoline Dray for 4,000 crowns, the price of the mare Silver Lark, which Byrne delivered to Dray's stables in February. Dray says that the mare was bought not by her but by her former stable manager, Tomas Keel, personally, so that Keel owes the price.

Dray calls Keel's brother-in-law, Rufus Amberley, who will testify that in March Keel told him: "The Lark was my purchase, not Ottoline's. I owe Byrne the four thousand myself, and I'll pay him when I can."

Keel is alive, lives locally, and has been summoned by Byrne to give evidence at the trial."""),

dict(n=80, j="H", rules=["MENU_H"], opts="EXC", d=2,
q="Which basis, if any, supports admitting Ancell's account of Vell's words?", gold="not hearsay",
doc="""Halvard Reach Crown Court - Crown v. Garrick Vell (demanding money with menaces)

Shopkeeper Ruth Ancell testifies that on 2 October Vell came into her shop, leaned over the counter and said: "Two hundred crowns every Friday, or this place burns with you in it."

Vell denies saying anything of the kind. The Crown tenders Ancell's evidence of the words to prove that the demand and threat were made. The defence objects that Ancell is repeating a previous representation made out of court."""),

dict(n=81, j="C", rules=["MENU_C"], opts="EXC", d=2,
q="Which provision, if any, is needed to admit Kessler's words when Roth offers them?", gold="not hearsay",
doc="""Coldmere Civil Court - Sabine Roth v. Dieter Kessler (trading as Kessler Autos)

Roth bought a used hatchback from Kessler Autos, an unincorporated business run by the defendant, Dieter Kessler, alone. The engine failed eight days later.

Roth's friend, Paula Ines, will testify that while showing them the car, Kessler said: "The engine was fully rebuilt in March - there's nothing wrong with it." Roth's mechanic will say the engine had never been rebuilt.

Roth offers Ines's evidence of Kessler's words to prove that Kessler told Roth the engine had been rebuilt. Kessler objects that the words are hearsay."""),
]
