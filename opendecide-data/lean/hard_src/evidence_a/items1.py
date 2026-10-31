"""Items 1-24: is it hearsay? (yes/no). Gold 1 = yes."""

ITEMS = [
dict(n=1, j="A", rules=["A801", "A802"], d=2,
q="Is Oduya's remark to Pellew hearsay under Rule 801 as defined above?", gold=0,
doc="""From: Priya Anand-Holt <pah@holtlaw.arv>
To: Mendes trial team
Subject: Mendes v. Brightbasket Grocers - hearsay objection on the Oduya testimony

Team, a quick write-up for tomorrow's argument.

Our client, Lena Mendes, fell in aisle 6 of the Brightbasket store on Corran Street at 2:40 pm. Brightbasket disputes both that there was any oil on the floor and that any employee knew of a spill before she fell. We plan to call Samuel Oduya, a customer, who will testify that at about 2:10 pm he told the assistant manager, Garth Pellew: "There's a puddle of olive oil by the pasta shelf in aisle 6, someone's going to go down." Pellew replied that he would "get to it."

Separately, the store's own cleaner will testify that she mopped up broken glass and oil in aisle 6 after the fall, so the existence of the spill will be proved through her.

Brightbasket will object that Oduya's quote is hearsay. Our position is that we offer it only to establish that Pellew was told about a hazard in aisle 6 thirty minutes before the fall, and we will ask for a limiting instruction to that effect.

Please have the Arvell rules handy.
Priya""",
twin=dict(rep=[("Separately, the store's own cleaner will testify that she mopped up broken glass and oil in aisle 6 after the fall, so the existence of the spill will be proved through her.",
                "The cleaner who mopped aisle 6 after the fall has left the company and cannot be traced, so we have no other witness to the spill itself."),
               ("we offer it only to establish that Pellew was told about a hazard in aisle 6 thirty minutes before the fall, and we will ask for a limiting instruction to that effect.",
                "we offer it to establish that there really was olive oil on the floor of aisle 6 that afternoon; we will prove notice separately through the store's radio log.")],
          gold=1)),

dict(n=2, j="A", rules=["A801"], d=2,
q="Is the statement Ms. Roe repeated hearsay under the Arvell definition?", gold=0,
doc="""Dunmore County Circuit Court, Commonwealth of Arvell
Halloran v. Vesk (motor collision) - transcript excerpt, day 2

Q (Ms. Ferreira, for the plaintiff): Ms. Roe, after the collision, did anyone speak to you?
A: Yes. A man got out of the grey pickup, walked over to me and said, "I was looking at my phone, I never saw the light change."
Q: Who was that man?
A: The driver. That's him at the defence table, Mr. Vesk.
MR. DALE (for the defendant): Objection, hearsay. The witness is repeating an out-of-court statement.
THE COURT: Ms. Ferreira, for what purpose is the statement offered?
MS. FERREIRA: To prove that the pickup's driver was looking at his phone and did not see the light change, Your Honour.
MR. DALE: Which is exactly why it is hearsay. The man who said it is not on the stand.
THE COURT: I will rule after a short recess.""",
twin=dict(rep=[('said, "I was looking at my phone, I never saw the light change."', 'said, "He was looking at his phone, he never saw the light change."'),
               ("A: The driver. That's him at the defence table, Mr. Vesk.", "A: His passenger, a young man called Owen Tarly. He isn't a party to this case.")],
          gold=1)),

dict(n=3, j="M", rules=["M801", "M802"], d=3,
q="Under section 801 as quoted, is Kettering's remark to Nico hearsay?", gold=1,
doc="""Morrow Vale Law Students' Forum > Evidence > "Problem set 4, Q2 - am I overthinking this?"

Posted by quill_and_gavel:

Fact pattern from the problem set: Delia Farrow is suing her former landlord, Ambrose Kettering, for the return of a 1,200-mark security deposit. Farrow wants to call her friend Nico, who helped her move out. Nico will say that on moving-out day Kettering walked through the flat, ran a finger along the skirting boards and said, "Place looks spotless, you'll get the full deposit back by Friday." Kettering now claims the flat was left damaged and says he kept the deposit to pay for repairs.

Farrow offers Nico's account to prove that the flat was clean and undamaged when she left. Kettering is the defendant and will himself testify at the trial.

My study group says the landlord's remark is obviously fine because "it's the other side's own words, so it can't be hearsay." I'm not so sure, given how our Code is drafted. The question as set is simply: is Kettering's statement hearsay?""") ,

dict(n=4, j="A", rules=["A801", "A802"], d=2,
q="Does Dray's reply count as hearsay under Rule 801?", gold=0,
doc="""CASE FILE NOTE - Ironwood Crates Ltd v. Selbourne Orchards Ltd (Arvell Commercial List)
Prepared by: junior associate, for the pre-trial conference

Claim: breach of contract for 400 apple crates at 12 marks each. Selbourne's defence is that no contract was ever formed.

Ironwood's sales manager, Yusuf Marr, will testify that on 3 March he telephoned Selbourne's purchasing officer, Elin Dray, who has authority to place orders up to 10,000 marks. He offered 400 crates at 12 marks each for delivery by 1 April. Dray answered: "We accept - four hundred at twelve, delivery by the first." Marr confirmed the call in an email the same afternoon; Selbourne never replied to the email.

Dray has since left Selbourne and moved abroad; neither side will call her. Ironwood offers Marr's account of Dray's words to establish that Selbourne accepted the offer and a contract was formed on 3 March.

Selbourne has given notice that it will object: "Dray's words are an out-of-court statement offered to prove that Selbourne agreed to buy. That is classic hearsay."

Action: prepare a short response on the hearsay point."""),

dict(n=5, j="H", rules=["H4", "H5"], d=3,
q="Is DS Ottley's account of what the callers said hearsay under section 4?", gold=1,
doc="""HALVARD REACH POLICE - SUMMARY OF EVIDENCE FOR THE PROSECUTOR
R v. Colm Ashby - keeping a common betting house

On 14 June officers executed a search warrant at the rear office of the Gilded Pike tavern, which Ashby manages. During the ninety-minute search the office telephone rang eleven times. Detective Sergeant Wren Ottley answered each call without identifying himself.

On six of the calls, the caller, without any prompting, said words to the effect of "Put fifty on Blue Kestrel in the fourth at Harrowgate" or "Is the price on Marchbane still eight to one?" On the other five calls the caller hung up. None of the callers has been identified.

The prosecution proposes to lead DS Ottley's account of the six calls to prove that the rear office was being used to take bets. There is no other direct evidence of betting transactions: no betting slips or ledgers were found.

The defence has indicated that it objects to DS Ottley's account of the calls.""",
twin=dict(rep=[("to prove that the rear office was being used to take bets. There is no other direct evidence of betting transactions: no betting slips or ledgers were found.",
                "only to explain why the officers extended their search to the tavern's cellar, a step the defence says was unlawful. Betting use of the office is proved separately by ledgers and slips found in the desk.")],
          gold=0)),

dict(n=6, j="H", rules=["H4", "H5"], d=2,
q="Is the result line on Exhibit P3 hearsay under section 4 of the Act?", gold=0,
doc="""Halvard Reach Magistrates' Court - case file
Halvard Reach v. Imogen Salt (driving with excess alcohol)

Exhibit P3 is a single sheet from the Portmere station breath-testing unit. The unit analyses the breath sample itself and prints the sheet automatically; the result line "BrAC 0.41 mg/L" is generated by the unit, and no officer enters or alters it.

Constable Lyle Ferran, who conducted the procedure, will testify that he started the test, watched Salt provide the sample, and handed the sheet to the custody sergeant. The unit's calibration record is agreed.

The prosecution relies on the result line to prove the concentration of alcohol in Salt's breath. The defence objects to the result line as hearsay, arguing that "whoever or whatever made that statement cannot be cross-examined, and the officer is merely repeating it." """,
twin=dict(rep=[("The unit analyses the breath sample itself and prints the sheet automatically; the result line \"BrAC 0.41 mg/L\" is generated by the unit, and no officer enters or alters it.",
                "The unit analyses the breath sample and shows the reading on a small screen only; Constable Ferran read the screen and typed the result line \"BrAC 0.41 mg/L\" into the station's report template, which was then printed as the sheet."),
               ("watched Salt provide the sample, and handed the sheet", "watched Salt provide the sample, and later handed the sheet")],
          gold=1)),

dict(n=7, j="A", rules=["A801"], d=3,
q="Is Kerr's description of Haldane's conduct hearsay under Rule 801?", gold=0,
doc="""DEPOSITION OF MARCUS KERR (extract)
Estate of Rufus Bell v. Tarn Lake Outfitters - Arvell Circuit Court

Q: Mr. Kerr, you were at the north landing on the morning of 9 January?
A: Yes. I'd rented an auger from the outfitters and I was getting ready to go out.
Q: Did you see Mr. Haldane that morning?
A: Yes. Old Haldane - he's fished Tarn Lake forty winters. He walked out maybe ten yards, stopped, knelt, tapped the ice with his spud bar a few times and looked at it for a good while. He didn't say a word to anyone, and I don't think he knew I was watching. Then he walked back, loaded his sled onto his truck and drove off.
Q: What did you do?
A: I waited about an hour and then went out on the east side instead.

[Note for trial counsel: Rufus Bell went through the ice at the north landing that afternoon. The estate offers Kerr's account of Haldane's conduct to prove that the ice at the north landing was unsafe that morning. Haldane died last year.]""",
twin=dict(rep=[("He didn't say a word to anyone, and I don't think he knew I was watching.",
                "When I called out to him, \"Is it holding?\", he looked straight at me, shook his head, and pointed back toward the shore.")],
          gold=1)),

dict(n=8, j="C", rules=["C20"], d=2,
q="Is the deposition answer hearsay under the Coldmere Code?", gold=0,
doc="""MEMORANDUM - to Judge Aurelie Mennick, Coldmere District Court
From: Law clerk
Re: State v. Barlow Quint (hit-and-run) - objection pending after lunch

This morning the prosecution's eyewitness, Hester Gallo, testified that the car that struck the cyclist on Linden Row was "dark green." In a deposition taken on 2 May, under oath and with defence counsel present, she said the car was "bright red, definitely red." Quint drives a red saloon.

The prosecution wants the jury to be able to use the deposition answer as proof that the car was in fact red, not merely to cast doubt on her testimony today. Ms. Gallo remains on the stand and available for cross-examination about both accounts.

Defence counsel objects that the deposition answer is hearsay. You asked for a one-line view before the afternoon session.""",
twin=dict(rep=[("In a deposition taken on 2 May, under oath and with defence counsel present,",
                "In an informal interview with a police investigator on 2 May, which was not under oath,")],
          gold=1)),

dict(n=9, j="A", rules=["A801", "A802"], d=2,
q="Is the diary entry hearsay as Rule 801 defines it?", gold=1,
doc="""ARVELL INTERVARSITY MOOT - PROBLEM 3 (extract)
Arvell v. Dunstan Reeve (robbery of the Kessel Road pharmacy)

The cashier, Maren Holt, testifies at trial and describes the robber as a tall man in a blue parka. On direct examination she says she cannot now remember whether the robber had any marks on his face.

The prosecution then offers a page from Holt's personal diary, written two days after the robbery, which reads: "Still shaking. The man had a scar through his left eyebrow - I keep seeing it." Reeve has such a scar.

The prosecution offers the diary entry to prove that the robber had a scar through his left eyebrow. The defence objects. The prosecution's written submission argues: "The author of the entry is in the witness box and can be cross-examined about every word of it. A statement by a witness who is present and testifying cannot be hearsay."

Mooters are asked to address the hearsay question only; no exception is argued."""),

dict(n=10, j="A", rules=["A801"], d=2,
q="Used in this way, is Pike's text message hearsay under Rule 801?", gold=0,
doc="""CARROW STREET LEGAL CLINIC - TRIAL PREPARATION NOTES
Client: Imre Szabo (plaintiff, pedestrian injury claim)

Defence witness Joanna Pike is expected to testify that the pedestrian signal was showing "Don't Walk" when Szabo stepped off the kerb.

Twenty minutes after the accident, Pike texted her sister: "Poor guy had the walk light and that van just ploughed through." Her sister has given us a screenshot, and Pike's phone records confirm the message.

Plan: confront Pike with the text on cross-examination.

Supervising attorney's note: We have two other eyewitnesses who will say the walk light was showing. We will use the text only to show that Pike has given inconsistent accounts and so should not be believed; we will not ask the jury to find from the text that the walk light was on, and we will request an instruction limiting it to Pike's credibility."""),

dict(n=11, j="H", rules=["H4", "H5"], d=2,
q="Would Lint's account of Halloway's words be hearsay under section 4?", gold=0,
doc="""Halvard Reach Civil Court - Summary of pleadings and evidence
Brisk v. Halloway (defamation)

Councillor Ivo Brisk sues Marta Halloway for slander. At the public meeting of the Fennick Parish Council on 9 January, Halloway is alleged to have stood up during questions from the floor and said: "Councillor Brisk has been taking envelopes of cash from the quarry company for two years."

Halloway's defence is that she never spoke those words; she does not plead that the allegation is true.

Brisk calls Oskar Lint, who attended the meeting, to testify to what Halloway said. Halloway's counsel objects: "Lint is repeating a previous representation, made out of court, about bribes. It is hearsay and inadmissible under section 5." """),

dict(n=12, j="A", rules=["A801"], d=3,
q="Is the statement Fenn heard hearsay within the meaning of Rule 801?", gold=0,
doc="""Arvell Mutual Assurance v. Estate of Corin Dahl
Agreed statement of facts (extract) and disputed evidence

1. Dahl's accident policy took effect at 00:00 on 1 March. The insurer is liable only if Dahl was alive at or after that time.
2. At about 23:40 on 28 February a section of the Fairhold warehouse roof collapsed while Dahl was working alone inside.
3. It is agreed that Dahl was trapped under fallen shelving in bay 9 and that his leg was pinned. He was found dead at 02:10 on 1 March; the pathologist cannot fix the time of death.

Disputed evidence: Rescuer Tomas Fenn will testify that at about 00:25 he heard a voice from under the rubble in bay 9 calling, "Help - I'm trapped under the shelving, my leg's pinned!" Fenn had worked with Dahl for six years and recognised the voice as Dahl's.

The estate offers Fenn's evidence to prove that Dahl was still alive at 00:25. The insurer objects that it is hearsay."""),

dict(n=13, j="A", rules=["A801", "A802"], d=2,
q="As offered by Norbeck, are the carton labels hearsay under Rule 801?", gold=1,
doc="""ARVELL CUSTOMS TRIBUNAL - Appeal of Norbeck Trading Ltd (decision extract)

Import duty on bicycle frames is 4% if the frames were manufactured in a Treaty member state and 18% otherwise. Norbeck imported 600 frames through Port Kessel. The Customs Service assessed duty at 18%, on the basis that the frames were manufactured in Sarnath, which is not a Treaty member.

Each carton bore a printed label reading "Manufactured in Corvessa (Treaty member) by Lunde Cycleworks." At the hearing Norbeck called its warehouse manager, who testified that she personally inspected the cartons on arrival and read the labels; photographs of the labels are exhibited. No one from Lunde Cycleworks gave evidence, and Norbeck produced no certificate of origin.

Norbeck offers the labels to prove that the frames were manufactured in Corvessa. The Customs Service, the opposing party, objects under the hearsay rule. [The tribunal's ruling on the objection follows.]"""),

dict(n=14, j="C", rules=["C20"], d=3,
q="Offered this way, is the press release hearsay under Articles 20 and 21?", gold=1,
doc="""From: Tomas Reiner (associate)
To: Dagny Holloway (partner)
Subject: Reyes v. Tollan Valve Works - press release

Dagny,

Quick hearsay question before I draft the exhibit list. Tollan, our client, is the defendant. Its press release of 12 June stated: "Tollan first learned of the seal defect in the K-40 valve on 2 March and issued a recall within ten days."

The plaintiff alleges Tollan knew of the defect as early as the previous autumn, which matters for punitive damages.

At trial the press release will be offered by Tollan itself, through our communications director, to prove that Tollan's first knowledge of the defect came on 2 March.

The client's general counsel told me: "It's a party's own statement, so the hearsay rule doesn't bite." Can you confirm how Articles 20-21 apply before I promise him anything?

Tomas""",
twin=dict(rep=[("At trial the press release will be offered by Tollan itself, through our communications director, to prove that Tollan's first knowledge of the defect came on 2 March.",
                "At trial the press release will be offered by the plaintiff, through her paralegal, to prove that Tollan knew of the defect by 2 March at the latest.")],
          gold=0)),

dict(n=15, j="M", rules=["M801", "M802"], d=3,
q="Is the officer's account of Whitlow's pointing hearsay under section 801?", gold=1,
doc="""Morrow Vale Crown Court - R v. Teodor Plaskett (street robbery)
Extract from the prosecution's evidence summary

On 3 October the victim, Agnes Whitlow, viewed a live identification parade at Kellbridge station. The parade officer's report records: "When asked whether the man who took her bag was present, the witness said nothing, but raised her arm and pointed firmly at position 4 (Plaskett)."

At trial, Whitlow testifies and identifies Plaskett in the dock as the robber. She is cross-examined.

The prosecution also calls the parade officer, Sergeant Lena Hask, to describe Whitlow's pointing at the parade, in order to prove that Plaskett was the man who took the bag. The defence objects that the sergeant's evidence of the pointing is hearsay; the prosecution replies that "pointing is conduct, not a statement, and in any event the witness is here and has been cross-examined." """),

dict(n=16, j="A", rules=["A801", "A802"], d=3,
q="Is Hask's statement to Detective Sule hearsay under Rule 801?", gold=0,
doc="""PROSECUTION TRIAL MEMORANDUM (extract)
Arvell v. Ivo Stenner - burglary of Harcastle Jewellers

When interviewed separately on 8 February, Stenner's associate Rolf Hask, who is not on trial and has since left Arvell, told Detective Amara Sule: "Ivo and I were at the Palace cinema in Wendmoor from nine until midnight."

Stenner, in his own interview an hour later, gave an identical account. CCTV and ticket records show that neither man entered the cinema that night, and Stenner now concedes he was not there.

We intend to call Detective Sule to repeat Hask's words. Our argument to the jury will be that Hask and Stenner told the same invented story, from which the jury may infer that they agreed it in advance to cover the burglary. We will not suggest that anything Hask said was accurate.

Stenner's counsel has given notice of a hearsay objection to Detective Sule's evidence of Hask's words."""),

dict(n=17, j="H", rules=["H4", "H5"], d=3,
q="Under section 4, is Corrow's evidence of the captain's conduct hearsay?", gold=1,
doc="""Halvard Reach Admiralty Court
Estate of Jory Pell v. Graythorn Shipping Ltd - outline of evidence

The central issue is whether the motor vessel Sable Wren was seaworthy when she left Portmere on 4 November; she foundered two days later with all hands, including the deckhand Jory Pell.

Graythorn, the owner, contends that she was seaworthy. Its witness, harbour master Ines Corrow, will testify that on the morning of departure the master, Captain Aldous Fenwright, an officer with thirty years' experience who was lost with the vessel, spent two hours inspecting the hull and pumps and then brought his wife and two children aboard as passengers for the voyage.

Graythorn relies on this evidence as showing that the vessel was sound, on the footing that no experienced master would have taken his own family to sea in a ship he believed to be unsafe. Fenwright said nothing to anyone about the vessel's condition. The estate objects to the evidence."""),

dict(n=18, j="A", rules=["A801", "A802"], d=2,
q="Is Kale's preliminary-hearing answer, offered to prove that Lindqvist carried the cash box, hearsay under Rule 801?", gold=1,
doc="""Arvell v. Petra Lindqvist (theft from the Harrow Road bus depot)
Trial transcript, day 3 - argument in the absence of the jury

MR. OYELARAN (prosecution): Your Honour, the witness Dorian Kale testified this morning that he cannot now recall who carried the cash box out of the depot. At the preliminary hearing in March he testified, under oath and subject to cross-examination by the same defence counsel, that he saw the defendant leave the depot carrying it. I intend to read that answer from the certified transcript.

MS. VANCE (defence): Objection, hearsay.

MR. OYELARAN: With respect, it cannot be hearsay. It was sworn testimony, given in court, by a witness who is sitting in this courtroom now. The jury has seen him and can assess him.

THE COURT: The Crown offers the preliminary-hearing answer for what purpose?

MR. OYELARAN: To prove that the defendant carried the cash box out of the depot."""),

dict(n=19, j="A", rules=["A801", "A802"], d=2,
q="Is Marek's warning, offered for that purpose, hearsay under Rule 801?", gold=0,
doc="""DEFENCE TRIAL BRIEF (extract)
Arvell v. Oren Blake (wounding outside the Anchor Rest bar)

Blake admits stabbing Silas Garrow with a pocket knife outside the Anchor Rest on 30 August and relies on self-defence. Under Arvell law, self-defence requires that the defendant actually and reasonably believed that he faced imminent serious harm.

The night before the incident, Blake's co-worker Lise Marek told him: "Stay away from Garrow - he carries a blade and he's cut two men this year." Marek has since emigrated.

The defence will have Blake testify to Marek's warning in order to show that, when Garrow advanced on him with his hand in his jacket, Blake genuinely and reasonably believed Garrow was armed and dangerous. The defence accepts that no knife was found on Garrow.

The prosecution has indicated that it will object to Marek's words as hearsay.""",
twin=dict(rep=[("in order to show that, when Garrow advanced on him with his hand in his jacket, Blake genuinely and reasonably believed Garrow was armed and dangerous. The defence accepts that no knife was found on Garrow.",
                "in order to prove that Garrow was in fact carrying a knife that night and was the armed aggressor. No knife was found on Garrow, and the defence says a friend removed it.")],
          gold=1)),

dict(n=20, j="M", rules=["M801", "M802"], d=2,
q="Is Ambler's account of Bramble's alert hearsay under section 801?", gold=0,
doc="""Morrow Vale Magistrates' Court - R v. Hana Duquesne (importation of a controlled drug)
Note of evidence and objection

At the Fenwick ferry terminal, a trained detection dog, Bramble, sat down beside Duquesne's suitcase. Sitting is the trained "passive alert" by which Bramble signals the scent of controlled drugs. Bramble has a documented accuracy record, which is agreed.

Handler Constable Rhys Ambler will testify to the alert. The suitcase was searched and contained no drugs, but the prosecution relies on the alert, together with traces found on Duquesne's clothing, as evidence that drugs had recently been in the case.

The defence objects: "The dog's sitting down is a communication to its handler that drugs are present. That is an assertion, it is offered for its truth, and the dog cannot be cross-examined." """),

dict(n=21, j="A", rules=["A801", "A802"], d=2,
q="Is the letter hearsay under Rule 801?", gold=1,
doc="""In re the Estate of Ottilie Varga - Arvell Probate Court
Proponents' skeleton argument (extract)

Ottilie Varga's will, executed on 4 April, leaves her entire estate to the Dunmore Animal Refuge and nothing to her only brother, Anselm Varga. Anselm contests the will, alleging that the refuge's director exerted undue influence on Ottilie in her final months.

To rebut that allegation, the proponents offer a letter Ottilie wrote to her friend Beatrix Lund two years before her death: "I cannot stand my brother Anselm. After what he did to Mother, I want nothing to do with him, and I will not leave him a penny."

The proponents offer the letter to prove that Ottilie in fact disliked Anselm and in fact intended, long before the refuge's director came on the scene, to leave him nothing. Anselm objects. The proponents submit that "a statement about the writer's own feelings is not hearsay at all, because no one else's perception is involved." """),

dict(n=22, j="C", rules=["C20"], d=2,
q="Is Olan's repetition of what he told Bede hearsay under Article 20?", gold=1,
doc="""Coldmere Labour Court - Claim of Petra Anand v. Harwick Logistics
Note of evidence, hearing day 1

The claimant was injured when forklift 7 rolled into her at the Harwick warehouse on a Thursday in March. Harwick denies both that forklift 7 had any brake fault and that it received any warning about the forklift before the accident.

Warehouse operative Dmitri Olan testifies for the claimant. He says: "The Monday before the accident I told the shift supervisor, Carys Bede, 'The brakes on forklift 7 are gone - it rolled into the racking twice this morning.'"

The claimant's counsel states that Olan's account of his own earlier words is offered to prove that forklift 7's brakes were defective. Harwick's counsel objects. The claimant's counsel responds: "Mr Olan is here, under oath, repeating his own words. There is no one absent to cross-examine." """,
twin=dict(rep=[("is offered to prove that forklift 7's brakes were defective.",
                "is offered only to prove that Harwick, through its supervisor, had been warned of a brake problem before the accident; the brake defect itself will be proved by the engineer's inspection report.")],
          gold=0)),

dict(n=23, j="H", rules=["H4", "H5"], d=2,
q="Is Rina's evidence of Crane's words hearsay under section 4 of the Evidence Act?", gold=0,
doc="""Halvard Reach Probate Registry - Estate of Barnaby Crane v. Ludo Pell
Issue: ownership of a gold pocket watch

The estate claims that a gold pocket watch found in Ludo Pell's possession belongs to the estate, having merely been lent to Pell while he worked as Crane's carer. Pell says it was a gift.

Pell's sister, Rina Pell, will testify that on 12 April, at the kitchen table, Crane took the watch from his waistcoat, pressed it into Ludo's hand and said: "Take it. It's yours now - I want you to have it."

Pell offers Rina's evidence to show that Crane gave him the watch. The estate objects that Rina is repeating a previous representation by Crane, who is dead and cannot be questioned about what he meant.""",
twin=dict(rep=[("on 12 April, at the kitchen table, Crane took the watch from his waistcoat, pressed it into Ludo's hand and said: \"Take it. It's yours now - I want you to have it.\"",
                "on 20 June, chatting over the garden fence, Crane told her: \"I gave Ludo my gold watch back in April, for keeps.\"")],
          gold=1)),

dict(n=24, j="M", rules=["M801", "M802"], d=3,
q="Is the evidence that no other guest complained hearsay under section 801 of the Code?", gold=0,
doc="""Morrow Vale County Court - Fenner v. Linden Hall Catering Ltd
Defendant's proposed evidence (summary)

Fenner alleges that she contracted food poisoning from chicken served at a 180-guest wedding reception catered by Linden Hall on 7 August.

Linden Hall's operations manager will testify that the company runs a customer hotline, printed on every menu card and table plan at the reception, which invites guests to report "any illness or concern after your event"; that the hotline is monitored daily and every call and message is logged; and that, apart from Fenner, no guest from the 7 August reception contacted the hotline in the following four weeks.

Linden Hall offers the absence of any other complaint as evidence that the chicken served that evening was not contaminated. None of the other guests has been asked about their health, and none will testify.

Fenner objects that this is "hearsay by silence." """),
]
