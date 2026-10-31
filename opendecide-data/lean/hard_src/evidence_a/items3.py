"""Items 45-60: witness competence and chain of custody (Vane Islands), yes/no."""

ITEMS = [
dict(n=45, j="V", rules=["V601", "V602"], d=2,
q="Is Mira competent to testify under Rule 601 as set out above?", gold=1,
doc="""Vane Islands Supreme Court - Crown v. Rafe Holloway (arson of the Saltmarsh boathouse)
Note of proceedings, day 2

The prosecution called Mira Tolland, aged six, who lives opposite the boathouse and says she saw a man carrying a petrol can near it shortly before the fire.

Before Mira was sworn, the jury was sent out. The presiding judge, Justice Okafor-Lind, then asked Mira a series of questions (for example, whether it would be the truth or a lie to say that the judge's robe was green) and recorded a finding that Mira understands the difference between the truth and a lie and knows that she must tell the truth in court. The jury was then brought back.

Mira speaks clearly and answers questions sensibly. The defence objects: "A six-year-old cannot be a competent witness under Rule 601." """,
twin=dict(rep=[("Before Mira was sworn, the jury was sent out. The presiding judge, Justice Okafor-Lind, then asked", "Before Mira was sworn, with the jury in its seats, the presiding judge, Justice Okafor-Lind, asked"),
               (" The jury was then brought back.", "")],
          gold=0)),

dict(n=46, j="V", rules=["V601"], d=2,
q="Is Varga competent to give evidence under Rule 601?", gold=0,
doc="""Vane Islands District Court (civil) - Pembrook v. Sallis (boundary fence)
Ruling requested on the competence of the claimant's witness

Pembrook calls Hollis Varga, a neighbour, to testify that the boundary fence between the parties' gardens was moved about two metres in June.

Cross-examination on the voir dire established that Varga was convicted of perjury by the Vane Islands Supreme Court on 3 March, eight years before the current trial, arising from false evidence he gave in an insurance dispute. He received a suspended sentence and has had no convictions since. He watched the fence being moved from his kitchen window.

Pembrook argues that the conviction is "old history, relevant at most to how much weight the court gives his evidence." Sallis submits that Varga cannot be called at all.""",
twin=dict(rep=[("on 3 March, eight years before the current trial,", "on 3 March, twelve years before the current trial,")], gold=1)),

dict(n=47, j="V", rules=["V601"], d=2,
q="Under Rule 601, may Lennart testify?", gold=1,
doc="""Vane Islands Magistrates' Court - Crown v. Talia Brum (common assault at the Harbour Street bus shelter)

The only independent eyewitness is Oskar Lennart, who has been profoundly deaf since birth and does not speak. He communicates fluently in Vane Islands Sign Language. The court has appointed a certified sign-language interpreter, who has interpreted for Lennart in earlier proceedings; both sides accept her accreditation.

Through the interpreter, Lennart has confirmed that he understands he must tell the truth in court and that he could be punished for lying. In a short preliminary exchange he described his address and occupation clearly.

The defence argues that because Lennart "cannot express himself orally, and cannot hear the oath or the questions put to him, he is not a competent witness." """),

dict(n=48, j="V", rules=["V601"], d=1, role="neg",
q="Is Duhr barred from testifying in this trial by the rules above?", gold=1,
doc="""Vane Islands Supreme Court - Crown v. Hester Quayle (dangerous driving)
Note from the judge's clerk, day two

During the morning session, juror number 7, Anneliese Duhr, passed a note to the usher: "I have just realised the junction in the photographs is outside my old flat. I think I saw this crash from my window. I'd like to tell the court what I saw."

The prosecution applies to call Duhr as a witness in this trial, arguing that she has direct personal knowledge and that her evidence is highly relevant. It proposes that she then continue to sit as a juror "to avoid the expense of a retrial." The defence opposes the application.

Duhr is an adult of sound mind and would be able to describe what she saw."""),

dict(n=49, j="V", rules=["V601", "V602"], d=2,
q="Is Greta a competent witness under Rule 601?", gold=1,
doc="""Vane Islands Probate Court - In re Estate of Nils Aberlin
Objection to the competence of the proponent's attesting witness

Aberlin's sister, Greta Aberlin, aged 88, is called to testify that she watched her brother sign his will at his kitchen table four years ago.

Greta has a diagnosis of moderate vascular dementia and sometimes forgets what she has eaten that day. A court-appointed psychiatrist reports that she is oriented, speaks clearly, understands that she is in court and must tell the truth, and has a firm and detailed recollection of events from several years ago, including the signing of the will, which she describes consistently.

The objector submits that "a person with a formal dementia diagnosis is incompetent to testify as a matter of law." """),

dict(n=50, j="V", rules=["V601", "V602"], d=2,
q="Is Fenner competent, under Rules 601 and 602, to testify that Kenworth took the cash box?", gold=0,
doc="""Vane Islands Magistrates' Court - Crown v. Idris Kenworth (theft from the Northpoint Fishing Co-operative)

The prosecution calls the co-operative's treasurer, Maud Fenner, to testify that Kenworth took the cash box from the co-op office on 11 August.

On a voir dire, Fenner explains that she was in hospital in another town from 9 to 14 August. She knows about the theft because three co-op members told her about it when she returned, and she says she "has no doubt at all" that it was Kenworth, because he had been "acting strangely" for weeks.

Fenner is an adult of sound mind who clearly understands the duty to tell the truth."""),

dict(n=51, j="V", rules=["V601", "V602"], d=2,
q="Is Pell competent to testify to what she saw outside the pub?", gold=1,
doc="""Vane Islands Supreme Court - Crown v. Soren Bask (unlawful wounding outside the Harbour Lantern)

Prosecution witness Jonna Pell admits that she had drunk "five or six ciders" on the night in question. She testifies that she was standing by the pub door, about four metres away, when she saw Bask swing a bottle at the victim's head.

She is sober in court, gives coherent answers, and affirms that she understands her duty to tell the truth.

The defence submits that Pell was "too drunk that night to be a competent witness" and asks the court to exclude her evidence under Rule 601."""),

dict(n=52, j="V", rules=["V601"], d=2,
q="Was Arlo competent to testify under Rule 601 as quoted?", gold=0,
doc="""Vane Islands Magistrates' Court (magistrate sitting alone, no jury) - Crown v. Dessa Wick (dog dangerously out of control)

The prosecution called Arlo Brenner, a seven-year-old boy, who said that Wick's dog chased him and knocked him off his bicycle on Quarry Lane.

The magistrate did not question Arlo about truth and lies before he gave evidence, remarking: "There is no jury here to protect, and the boy is obviously bright." Arlo answered all questions clearly and consistently, and nothing in his evidence suggested any difficulty in expressing himself.

On appeal, Wick argues that Arlo's evidence should not have been received.""",
twin=dict(rep=[("Arlo Brenner, a seven-year-old boy,", "Arlo Brenner, a nine-year-old boy,")], gold=1)),

dict(n=53, j="V", rules=["V901c"], d=2,
q="Has the Crown adequately accounted for the custody of PK/1 under Rule 901(c)?", gold=1,
doc="""Vane Islands Supreme Court - Crown v. Pieter Klaw (possession of a controlled drug with intent to supply)
Continuity statement, Exhibit PK/1 (white powder)

5 May: Constable Ines Rourke seized the powder from Klaw's car and weighed it at 48.2 g. She placed it in a tamper-evident bag, sealed the bag, and recorded the seal number, VX-30917, in her notebook and on the property log, which she signed. She placed the bag in the station safe. Rourke testifies.

7 May: The bag was taken from the station safe to the Government Analyst by a courier from a private firm. The courier has not been identified, and there is no log entry for the journey.

8 May: Analyst Dr Sanna Petrov testifies that she received the bag, found the seal intact, and recorded its number as VX-30917 before opening it. She weighed the contents at 47.9 g and identified them as a controlled drug.""",
twin=dict(rep=[("recorded its number as VX-30917 before opening it", "recorded its number as VX-30971 before opening it")], gold=0)),

dict(n=54, j="V", rules=["V901c"], d=2, role="neg",
q="Is the chain of custody for the blood sample deficient under Rule 901(c)?", gold=1,
doc="""Vane Islands Magistrates' Court - Crown v. Harriet Moss (driving with excess alcohol)
Continuity of the blood sample

01:40: Nurse Ben Cardew drew a blood sample from Moss into a vial labelled with her name. The vial was not placed in any sealed container. Cardew testifies.

01:45: Cardew handed the vial to Sergeant Pol Ivers, who signed the hospital's specimen release form. At 02:15 Ivers placed the vial in the station's evidence refrigerator and recorded this in the refrigerator log. Ivers testifies.

09:00: The vial was removed from the refrigerator. The removal entry in the log reads "lab staff"; it is unsigned, and no laboratory employee can say who collected it.

11:30: Toxicologist Dr Aveline Grosz testifies that she found the vial on the laboratory's intake bench, unsealed, with Moss's name on the label, and tested it."""),

dict(n=55, j="V", rules=["V901c", "V901d"], d=3,
q="Can EV/3 be authenticated despite the gap, under Rule 901 as quoted?", gold=1,
doc="""Vane Islands Supreme Court - Crown v. Ezra Valk (armed robbery of the Kittiwake filling station)
Defence objection to Exhibit EV/3

The Crown offers a revolver, Exhibit EV/3, bearing serial number TR-448213 and a distinctive brass inlay on the grip. Constable Dana Hurle seized it from the glovebox of Valk's car and recorded the serial number and a description of the inlay in her notebook.

The revolver then sat in an unlocked cupboard at the Harbourmouth police post for about five weeks. There is no log of who had access, and several officers used the cupboard.

Hurle testifies that the revolver in court bears the same serial number and inlay and is the one she seized. The Crown relies on it only as the weapon found in Valk's car; no forensic tests were carried out on it. The defence objects that "the chain of custody is broken beyond repair." """),

dict(n=56, j="V", rules=["V901c"], d=2,
q="Is LC/2 admissible so far as Rule 901(c) is concerned?", gold=1,
doc="""Vane Islands Supreme Court - Crown v. Lotte Crane (possession of cannabis resin with intent to supply)
Continuity and weight, Exhibit LC/2

Detective Constable Aiden Moyo seized the resin, weighed it at the scene on a calibrated scale at 250.0 g, sealed it in tamper-evident bag no. SB-7741, recorded the seal number, and signed the property log.

Property officer Ruth Asante signed the log when she received the bag and again when she released it to the laboratory's courier, Josef Dunn, who signed the laboratory's intake register on arrival.

Moyo, Asante and Dunn all testify. The analyst testifies that the seal was intact and matched SB-7741, and that she weighed the contents at 243.0 g on a calibrated scale. The Crown offers no explanation for the difference in weight.""",
twin=dict(rep=[("weighed the contents at 243.0 g", "weighed the contents at 228.0 g")], gold=0)),

dict(n=57, j="V", rules=["V901c"], d=2,
q="Has the prosecution satisfied Rule 901(c) for the USB drive?", gold=0,
doc="""Vane Islands District Court - Crown v. Imogen Tresk (false accounting)
Continuity of Exhibit IT/1 (USB drive)

14 February: Detective Sergeant Farid Olsen seized a USB drive from Tresk's desk. He did not bag or seal it. He put it in his own unlocked desk drawer in the open-plan CID office.

15-16 February: Olsen was on leave. A colleague recalls seeing a USB drive of the same colour lying on a shared bench in the CID office on 16 February, but cannot say who put it there or whether it was the same drive.

17 February: Olsen took the drive from his drawer, logged it into the property store and signed the entry. From that point every transfer to the digital-forensics unit is logged and signed, and the examiner testifies to the files she recovered from it.

Olsen testifies that the drive he logged on 17 February "looked like" the one he seized."""),

dict(n=58, j="V", rules=["V901c"], d=2, role="neg",
q="Is there any period in the custody of NP/4 that Rule 901(c) leaves unaccounted for?", gold=0,
doc="""Vane Islands Supreme Court - Crown v. Nuno Pasco (supply of MDMA tablets)
Continuity schedule, Exhibit NP/4 (112 tablets in an unsealed plastic tub)

(1) 14:05, 2 July: Constable Jess Morland seized the tub and kept it on her person until she handed it to the property clerk at 14:40, when she signed the property log. She testifies.
(2) 14:40, 2 July - 09:10, 3 July: Property clerk Hamid Rahel took the tub into the property store, signing the log at 14:40, and released it to the laboratory clerk at 09:10 the next day, signing the log at that time. Rahel has since retired abroad and does not testify.
(3) 09:10 - 10:00, 3 July: Laboratory clerk Paula Sim signed for the tub at 09:10 and handed it to the analyst at 10:00, signing the laboratory register. She testifies.
(4) 10:00 onward: Analyst Dr Ferro testifies that she received the tub from Sim at 10:00 and counted 112 tablets, the number Morland recorded at seizure."""),

dict(n=59, j="V", rules=["V901c"], d=3,
q="Does the prosecution's evidence satisfy the custody requirement of Rule 901(c)?", gold=0,
doc="""Vane Islands Supreme Court - Crown v. Beatrix Holm (possession of methylamphetamine)
Continuity evidence, Exhibit BH/1 (crystals in an unsealed envelope)

21:10, 2 June: Constable Idris Fane seized the crystals, put them in an envelope, and at 22:00 handed the envelope to the night property officer, Constable Wes Arden. Fane testifies.

22:00, 2 June - 08:00, 3 June: Arden kept the envelope in the property store and at 08:00 handed it to the laboratory courier, who signed for it. The courier testifies, as does the analyst who tested the crystals.

Arden did not complete the property log that night. On 17 June, after an audit flagged the omission, he filled in and signed entries for 2 and 3 June from memory. Arden is on long-term sick leave and will not testify."""),

dict(n=60, j="V", rules=["V901c"], d=3,
q="Has the Crown established the chain of custody for MO/5 as Rule 901(c) requires?", gold=0,
doc="""Vane Islands Supreme Court - Crown v. Mathis Orr (failing to stop after a fatal collision)
Continuity of Exhibit MO/5 (paint fragments)

Scenes-of-crime officer Freya Lund recovered paint fragments from the victim's clothing, placed them in a tamper-evident bag and sealed it at the scene. She testifies to this. Her notes say only "sealed"; she did not record the seal number.

The bag was then placed in a transit locker at the police station and collected by a driver for the regional laboratory. The driver has not been identified, and there is no record of the transfer.

The laboratory analyst testifies that the bag arrived with its seal intact, that she recorded the seal number (TE-58210) on arrival before opening it, and that she compared the fragments with paint from Orr's car."""),
]
