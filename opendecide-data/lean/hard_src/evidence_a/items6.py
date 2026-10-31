"""Items 100-120: chain-of-custody link, competence roster, rulings on objections, numbered-statement items (choice)."""

from rules import R_SUST_H, R_OVER_NH, R_OVER_EX, R_SUST_COMP, R_OVER_COMP, R_SUST_CHAIN

HEARSAY3 = [R_SUST_H, R_OVER_NH, R_OVER_EX]


def count_defs(k_max, noun, verb):
    out = {}
    for k in range(k_max + 1):
        if k == 0:
            out[str(k)] = f"None of the {noun} {verb}."
        elif k == 1:
            out[str(k)] = f"Exactly one of the {noun} {verb}."
        else:
            out[str(k)] = f"Exactly {k} of the {noun} {verb}."
    return out


ITEMS = [
dict(n=100, j="V", rules=["V901c"], d=2, shuffle=False,
q="Which period of custody of IH/1 is not properly accounted for under Rule 901(c)?", gold="the courier's custody",
opts=["Constable Rusk's custody", "the property officer's custody", "the courier's custody", "the intake clerk's custody", "the analyst's custody", "no period is deficient"],
defs={"Constable Rusk's custody": "From seizure at 10:15 on 4 July until hand-over to the property officer at 11:00.",
      "the property officer's custody": "From 11:00 on 4 July until release from the property store at 09:00 on 6 July.",
      "the courier's custody": "From collection at the property store at 09:00 on 6 July until delivery to the laboratory intake desk at 13:30.",
      "the intake clerk's custody": "From 13:30 until hand-over to the analyst at 14:00 on 6 July.",
      "the analyst's custody": "From 14:00 on 6 July through analysis.",
      "no period is deficient": "Every period of custody is accounted for, or any gap is excused, as Rule 901(c) requires."},
doc="""Vane Islands Supreme Court - Crown v. Ilse Harrow (supply of heroin)
Continuity schedule for Exhibit IH/1 (3.1 g of brown powder in an unsealed plastic tub)

(1) 10:15, 4 July - Constable Arne Rusk seizes the tub from Harrow's jacket pocket and keeps it with him. Rusk testifies.
(2) 11:00, 4 July - Rusk hands the tub to property officer Mae Holt, who signs the property log on receipt. Holt testifies.
(3) 09:00, 6 July - A courier from Swiftline Deliveries collects the tub from Holt for transport to the Government Laboratory. Holt signs the log to record the release. The courier is not named anywhere, made no entry in any log, and has not been traced.
(4) 13:30, 6 July - The tub is received at the laboratory intake desk by clerk Obi Nance, who signs the intake register. Nance testifies.
(5) 14:00, 6 July - Nance passes the tub to analyst Dr Lina Voss, who signs the case file and testifies to the analysis.""",
twin=dict(rep=[("The courier is not named anywhere, made no entry in any log, and has not been traced.",
                "The courier, Pim Valdez, signs both the release entry in the property log and the laboratory's intake register, and testifies.")],
          gold="no period is deficient")),

dict(n=101, j="V", rules=["V901c"], d=3, shuffle=False,
q="At which stage, if any, is the chain of custody for DO/2 deficient?", gold="no period is deficient",
opts=["the nurse's custody", "Sergeant Malin's custody", "the two days in the station refrigerator", "the courier's custody", "the analyst's custody", "no period is deficient"],
defs={"the nurse's custody": "From drawing the sample at 02:05 until hand-over to Sergeant Malin.",
      "Sergeant Malin's custody": "From hand-over by the nurse until the pouch was placed in the station refrigerator.",
      "the two days in the station refrigerator": "The period in the shared refrigerator with no sign-out sheet.",
      "the courier's custody": "Collection from the station and transport to the laboratory by an unrecorded courier.",
      "the analyst's custody": "From receipt at the laboratory through analysis.",
      "no period is deficient": "Every period of custody is accounted for, or any gap is excused, as Rule 901(c) requires."},
doc="""Vane Islands Magistrates' Court - Crown v. Doran Oake (driving with excess alcohol)
Continuity of blood sample DO/2

- Nurse Ffion Carr drew the sample at 02:05 on 10 March into a vial, sealed the vial in tamper-evident pouch no. 60214, recorded the pouch number on the hospital form, and signed it. She testifies.
- She handed the pouch to Sergeant Ruth Malin, who signed the form and drove the pouch to the station. Malin testifies.
- Malin placed the pouch in the station's evidence refrigerator, which fourteen officers can open and which has no sign-out sheet. It stayed there for two days.
- On 12 March a laboratory courier, whose identity was not recorded, collected it.
- Analyst Dr Pita Heke testifies that when she received the pouch its seal was intact and bore number 60214, which she recorded before opening it. Her result is 112 mg of alcohol per 100 ml of blood."""),

dict(n=102, j="V", rules=["V901c"], d=2, shuffle=False,
q="Which stage leaves the custody of KL/7 unaccounted for?", gold="Stage D",
opts=["Stage A", "Stage B", "Stage C", "Stage D", "Stage E", "none of the stages"],
defs={"Stage A": "Collection by DC Penn at the house and logging at 17:00.",
      "Stage B": "Overnight storage by property officer Ruiz and release to the courier at 08:00.",
      "Stage C": "Transport by courier Stroud from 08:00 to delivery at the laboratory intake at 09:15.",
      "Stage D": "From delivery at the laboratory intake at 09:15, through the move to the cold room, until 14:00.",
      "Stage E": "Removal from the cold room by Dr Salo at 14:00 and analysis.",
      "none of the stages": "Every stage is accounted for, or any gap is excused, as Rule 901(c) requires."},
doc="""Vane Islands Supreme Court - Crown v. Kasia Lorne (administering poison)
Exhibit KL/7: tea from the victim's mug, in an unsealed screw-top jar

Stage A: Detective Constable Rhodri Penn collected the tea at the house at 16:00 on 2 October and logged the jar into the property store at 17:00. He testifies.
Stage B: Property officer Amal Ruiz held the jar overnight and released it to the laboratory courier at 08:00 on 3 October, signing the log on receipt and on release. Ruiz testifies.
Stage C: The courier, Bea Stroud, signed for the jar at 08:00 and signed the laboratory's intake book when she left it at the intake desk at 09:15. Stroud testifies.
Stage D: The intake book has a further entry, "moved to cold room, 09:40", with no initials or signature. No one at the laboratory knows who moved the jar or who was at the intake desk.
Stage E: Toxicologist Dr Imre Salo took the jar from the cold room at 14:00, signed the cold-room register, and testifies that he found a toxic compound."""),

dict(n=103, j="V", rules=["V901c"], d=3, shuffle=False,
q="Which numbered stage of the continuity schedule for SM/3 fails Rule 901(c)?", gold="Stage 4",
opts=["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5", "Stage 6", "Stage 7", "no stage is deficient"],
defs={"Stage 1": "Seizure by Customs officer Brun.",
      "Stage 2": "Hand-over from Brun to supervisor Adeyemi.",
      "Stage 3": "Adeyemi's placing of the brick in the Customs strongroom.",
      "Stage 4": "Removal from the strongroom by the night-shift clerk and storage in the secondary store until 08:15.",
      "Stage 5": "Collection from the secondary store by police officer Fenn.",
      "Stage 6": "Delivery to the laboratory and receipt by intake clerk Rourke.",
      "Stage 7": "Hand-over from Rourke to analyst Dr Park and analysis.",
      "no stage is deficient": "Every stage is accounted for, or any gap is excused, as Rule 901(c) requires."},
doc="""Vane Islands Supreme Court - Crown v. Soren Makepeace (importation of cocaine)
Continuity schedule for Exhibit SM/3, a vacuum-packed brick, unsealed after it was cut open for a field test

1. Customs officer Helga Brun seizes the brick at Port Vane at 06:10 and signs the seizure log. She testifies.
2. At 06:40 Brun hands it to Customs supervisor Kofi Adeyemi, who signs the log. He testifies.
3. At 07:00 Adeyemi places it in the Customs strongroom and signs the strongroom register. He testifies.
4. At 23:30 a "night-shift clerk" removes it from the strongroom to "free up shelf space" and places it in a secondary store. The register entry is unsigned, and the staff rota for that night has been lost.
5. At 08:15 the next morning police officer Luca Fenn collects it from the secondary store and signs for it. He testifies.
6. At 10:00 Fenn delivers it to the Government Laboratory, where intake clerk Ada Rourke signs the intake register on receipt and again on hand-over at 10:30. Rourke does not testify.
7. At 10:30 analyst Dr Jun Park receives it from Rourke, signs for it, weighs it and tests it. He testifies."""),

dict(n=104, j="V", rules=["V901c"], d=2, shuffle=False,
q="Where does the continuity evidence for AL/1 break down, if anywhere?", gold="the pool-van transfer",
opts=["Constable Oakes's custody", "the pool-van transfer", "examiner Sole's custody", "no period is deficient"],
defs={"Constable Oakes's custody": "From seizure until the bag was signed out of the property store two days later.",
      "the pool-van transfer": "Transport of the bag from the station to the Digital Forensics Unit by an unidentified driver.",
      "examiner Sole's custody": "From arrival at the Digital Forensics Unit through extraction.",
      "no period is deficient": "Every period of custody is accounted for, or any gap is excused, as Rule 901(c) requires."},
doc="""Vane Islands District Court - Crown v. Aurora Linde (harassment by electronic messages)

A mobile phone, Exhibit AL/1, was seized from Linde by Constable Petra Oakes, who placed it in a tamper-evident Faraday bag, sealed the bag, and signed the property log. The log entry reads "sealed" but gives no seal number. Oakes testifies.

Oakes placed the bag in the station property store. Two days later property officer Jed Rawle signed it out of the store to "pool van driver" and testifies to doing so. The bag was then taken in the force's pool van to the Digital Forensics Unit; nothing records who drove the van, and no one signed for the bag on the journey.

At the Unit, examiner Tariq Sole found the bag's seal intact, recorded its seal number (FB-44072), opened it and extracted the messages. He testifies."""),

dict(n=105, j="V", rules=["V601", "V602"], d=2, shuffle=False,
q="Which listed witness is not competent to testify?", gold="Callum Dreyer",
opts=["Lotte Imhof", "Anders Kjell", "Rosalind Achterberg", "Callum Dreyer", "every listed witness is competent"],
defs={"Lotte Imhof": "The six-year-old witness questioned by the judge in chambers.",
      "Anders Kjell": "The witness who communicates through a sign-language interpreter.",
      "Rosalind Achterberg": "The wife of juror number 4.",
      "Callum Dreyer": "The firefighter with a perjury conviction.",
      "every listed witness is competent": "None of the listed witnesses is barred by Rules 601-602."},
doc="""Vane Islands Supreme Court - Crown v. Tobias Graff (arson of the Linfield grain store)
Prosecution witness list with notes on competence

- Lotte Imhof, aged six. Before trial the judge questioned her in chambers, without the jury, and found that she understands the difference between truth and lies.
- Anders Kjell, who has no hearing or speech and communicates through a certified sign-language interpreter. He understands the duty to tell the truth.
- Rosalind Achterberg, whose husband is juror number 4 in this trial.
- Callum Dreyer, a firefighter, who was convicted of perjury in the Vane Islands three years ago and received a suspended sentence.

All four perceived relevant events at the fire and can describe them.""",
twin=dict(rep=[("convicted of perjury in the Vane Islands three years ago", "convicted of perjury in the Vane Islands thirteen years ago")],
          gold="every listed witness is competent")),

dict(n=106, j="V", rules=["V601", "V602"], d=3, shuffle=False,
q="Which of these proposed witnesses is incompetent under Rule 601?", gold="every listed witness is competent",
opts=["Nils Harker", "Vera Lomax", "Dominic Arkwright", "Selma Ottoway", "every listed witness is competent"],
defs={"Nils Harker": "The claimant's seven-year-old son.",
      "Vera Lomax": "The yard worker with a fraud conviction.",
      "Dominic Arkwright": "The witness with managed paranoid schizophrenia.",
      "Selma Ottoway": "The witness who was drunk when she saw the collision.",
      "every listed witness is competent": "None of the listed witnesses is barred by Rules 601-602."},
doc="""Vane Islands Supreme Court (jury trial) - Harker v. Ormsby Logistics Ltd (collision in a loading yard)
Claimant's proposed witnesses

- Nils Harker, the claimant's son, aged seven. On day one the judge questioned him out of the jury's presence and recorded that he knows the difference between true and false and promises to tell the truth.
- Vera Lomax, a yard worker, convicted four years ago of fraud by false invoicing.
- Dominic Arkwright, who has paranoid schizophrenia, managed with medication. The court's psychiatrist reports that he communicates clearly and understands his obligation to tell the truth.
- Selma Ottoway, who admits she was "quite drunk" when she saw the collision from the yard canteen window. She is sober in court.

Each of them saw the collision."""),

dict(n=107, j="V", rules=["V601", "V602"], d=3, shuffle=False,
q="Which proposed witness may not give evidence at the retrial?", gold="Emrys Tallow",
opts=["Maren Voll", "Emrys Tallow", "Justice Hanna Brill", "Owen Pike", "every listed witness is competent"],
defs={"Maren Voll": "The juror from Ansell's first trial.",
      "Emrys Tallow": "The post-office clerk affected by a stroke.",
      "Justice Hanna Brill": "The judge who presided at the first trial.",
      "Owen Pike": "The eight-year-old boy.",
      "every listed witness is competent": "None of the listed witnesses is barred by Rules 601-602."},
doc="""Vane Islands Supreme Court - Crown v. Petrus Ansell (retrial for robbery of the Quay Street post office)
Proposed prosecution witnesses

- Maren Voll, who sat as a juror at Ansell's first trial, which ended when the jury could not agree. After that trial she realised that she had seen him running from the post office on the day of the robbery.
- Emrys Tallow, the post-office clerk, who suffered a severe stroke last year. Speech therapists and a court-appointed interpreter have tried spoken language, writing, picture boards and yes/no signals; he cannot reliably convey answers by any of them.
- Justice Hanna Brill, who presided at the first trial (a different judge presides at the retrial) and happened to be standing in the post-office queue during the robbery.
- Owen Pike, aged eight, who saw the robber's car. The judge has not questioned him.

Each saw part of the robbery."""),

dict(n=108, j="V", rules=["V601", "V602"], d=2, shuffle=False,
q="Which prosecution witness is not competent under the rules quoted?", gold="Ellie Marsh",
opts=["Ellie Marsh", "Ferdinand Bly", "Priya Onwuke", "Ciaran Doyle", "every listed witness is competent"],
defs={"Ellie Marsh": "The five-year-old girl.",
      "Ferdinand Bly": "The 81-year-old with mild hearing loss.",
      "Priya Onwuke": "The dog warden with an old perjury conviction.",
      "Ciaran Doyle": "The witness who testifies through a Portuguese interpreter.",
      "every listed witness is competent": "None of the listed witnesses is barred by Rules 601-602."},
doc="""Vane Islands Supreme Court (jury trial) - Crown v. Gideon Rask (dog dangerously out of control)
Prosecution witnesses, as called

- Ellie Marsh, aged five. With the jury present, the judge asked her whether it was good or bad to tell lies; she answered "bad", and the judge allowed her to give evidence.
- Ferdinand Bly, aged 81, who has mild hearing loss and uses a hearing aid. He answers questions accurately.
- Priya Onwuke, the dog warden, who was convicted of perjury eleven years before this trial.
- Ciaran Doyle, who does not speak English and gives evidence in Portuguese through an accredited interpreter.

Each witnessed the dog attack on Harbour Green."""),

dict(n=109, j="V", rules=["V601", "V602"], d=2, shuffle=False,
q="Which witness would be barred from testifying about the incident?", gold="Farah Idris",
opts=["Hugo Brandt", "Amelie Stroud", "Farah Idris", "Josef Brandt", "every listed witness is competent"],
defs={"Hugo Brandt": "The claimant's husband, who was in the room.",
      "Amelie Stroud": "The housekeeper who arrived afterwards.",
      "Farah Idris": "The night manager who was off duty in another city.",
      "Josef Brandt": "The claimant's eleven-year-old son.",
      "every listed witness is competent": "None of the listed witnesses is barred by Rules 601-602."},
doc="""Vane Islands District Court - Brandt v. Coldharbour Hotel Ltd (scalding in room 208)
Claimant's proposed witnesses

- Hugo Brandt, her husband, who was in the room and saw the kettle boil over and spray her arm.
- Amelie Stroud, the housekeeper, who arrived ten minutes later and saw water on the floor and the kettle unplugged.
- Farah Idris, the hotel's night manager, who was off duty in another city that night. Everything she knows about the incident comes from reading Stroud's report and talking to guests the next day.
- Josef Brandt, the couple's son, aged eleven, who was in the bathroom and heard his mother cry out.

Each will be asked to describe what happened in room 208 that night."""),

dict(n=110, j="A", rules=["MENU_A"], d=2,
q="How should the court rule on the defence objection?", gold=R_OVER_EX,
opts=[R_SUST_H, R_OVER_NH, R_OVER_EX, R_SUST_COMP],
doc="""Arvell v. Hector Moine (robbery of Ferris Hardware) - trial transcript, day 1

Q (Prosecutor): Mrs. Delacourt, what happened after you heard the shots?
A: About two minutes later my neighbour's boy, Luka, came hammering on my back door, white as chalk, crying so hard he could barely breathe. He said, "The man with the snake tattoo shot at Mr. Ferris - he's still in the shop!"
DEFENCE: Objection, hearsay.
PROSECUTOR: Your Honour, Luka is eleven and has been ruled unable to testify.
THE COURT: For what purpose is it offered?
PROSECUTOR: To prove that the gunman had a snake tattoo.

Note: Moine has a snake tattoo on his neck. Mrs. Delacourt is an adult of sound mind."""),

dict(n=111, j="M", rules=["MENU_M"], d=2,
q="What ruling should the court make on the respondent's objection?", gold=R_SUST_H,
opts=[R_SUST_H, R_OVER_NH, R_OVER_EX, R_SUST_COMP],
doc="""Morrow Vale County Court - Chauncey (deceased) v. Ribble Garages Ltd - hearing transcript

Q (claimant's counsel): Mr. Tate, did Mr. Chauncey say anything about the brakes?
A: Yes. When I visited him in hospital two days after the crash, he was sitting up and chatting, and he said: "When I pressed the brake pedal on Harker's Hill, it went straight to the floor."
RESPONDENT'S COUNSEL: Objection.
CLAIMANT'S COUNSEL: It's offered to show the brakes failed, which is the whole case. Mr. Chauncey died last month; Mr. Tate is simply telling us what he heard.

Note: Ribble had serviced the brakes a week before the crash. No police officer was involved in any conversation with Chauncey.""",
twin=dict(rep=[("When I visited him in hospital two days after the crash, he was sitting up and chatting, and he said:",
                "When I reached his car about five minutes after the crash, he was trapped in the seat, screaming and shaking, and he said:")],
          gold=R_OVER_EX)),

dict(n=112, j="H", rules=["H4", "H5", "H9"], d=2,
q="How should the magistrate deal with the objection?", gold=R_OVER_NH,
opts=[R_SUST_H, R_OVER_NH, R_OVER_EX, R_SUST_COMP],
doc="""Halvard Reach Magistrates' Court - Crown v. Ines Albescu (speeding on the Tannery Bypass)

Constable Mark Tennant produces a still frame from a fixed speed camera, bearing an automatically generated data strip: "14:22:07 - 112 km/h - limit 80 - lane 2", above a photograph of Albescu's car. No person enters any data into the camera; it measures, records and prints the strip itself. The camera's calibration certificate is in evidence and unchallenged.

DEFENCE: Objection - hearsay. The data strip asserts that my client was doing 112, and nobody who can be cross-examined made that statement.
PROSECUTOR: The constable is here and can be cross-examined about the camera."""),

dict(n=113, j="V", rules=["V801", "V601", "V901c"], d=2,
q="How should the court rule on the defence objection to the analyst's evidence?", gold=R_SUST_CHAIN,
opts=[R_SUST_H, R_OVER_NH, R_SUST_COMP, R_OVER_COMP, R_SUST_CHAIN],
doc="""Vane Islands Supreme Court - Crown v. Luis Mendel (possession of heroin) - transcript

PROSECUTOR: Dr Asante, what did you find when you analysed Exhibit LM/2?
DEFENCE: Objection. The Crown's own continuity evidence shows that the envelope was unsealed, and that Constable Ruiz left it overnight in the unlocked tray on the front desk at Harbour Street station, where there is no log and anyone passing could have handled it. The next morning Constable Ruiz retrieved it and signed it into the property store.
PROSECUTOR: Constable Ruiz has testified that it was the same envelope and that it did not look disturbed. Every other transfer is logged and signed, and each custodian has testified. The analyst's weight matches the seizure weight to within 1 percent.

Note: Dr Asante is a qualified analyst who personally tested the contents of the envelope."""),

dict(n=114, j="V", rules=["V801", "V601", "V602"], d=2,
q="How should the judge rule on the defence objection to Sunny's evidence?", gold=R_SUST_COMP,
opts=[R_SUST_COMP, R_OVER_COMP, R_SUST_H, R_OVER_NH],
doc="""Vane Islands Supreme Court (jury trial) - Crown v. Hal Brennock (common assault in a school playground) - transcript

PROSECUTOR: I call Sunny Paterek.
[A girl aged seven takes the witness stand.]
DEFENCE: Your Honour, before this witness is sworn -
THE COURT: I have read the registered intermediary's report, which says that she is bright, articulate and truthful. I see no need to question her myself. Proceed.
PROSECUTOR: Sunny, tell us what you saw in the playground on 9 May.
DEFENCE: Objection.

Note: Sunny saw the incident herself and will describe only what she saw."""),

dict(n=115, j="M", rules=["MENU_M"], d=3,
q="How should the court rule on the defence objection to Holm's evidence?", gold=R_SUST_H,
opts=[R_SUST_H, R_OVER_NH, R_OVER_EX],
doc="""Morrow Vale Crown Court - R v. Ansel Lanning (assault occasioning actual bodily harm outside the Bell Inn) - transcript

Q (Prosecutor): Mr. Holm, you live next door to the defendant?
A: Yes.
Q: Did he say anything to you about the fight outside the Bell?
A: The next morning, calmly over the fence, he said: "That idiot outside the Bell went down like a sack when I hit him."
DEFENCE: Objection.
PROSECUTOR: These are the defendant's own words, offered to prove that he struck the victim.

Note: Holm is not a police officer. The fight took place at about 23:00 on 14 May.""",
twin=dict(rep=[("The next morning, calmly over the fence, he said:", "About five minutes after the fight, still panting and shaking with adrenaline, he said to me in the street:")],
          gold=R_OVER_EX)),

dict(n=116, j="A", rules=["A801"], d=3, shuffle=False,
q="Which numbered statement, if any, is hearsay under Rule 801 for the purpose stated?", gold="Statement 3",
opts=["Statement 1", "Statement 2", "Statement 3", "Statement 4", "Statement 5", "none of these"],
defs={"Statement 1": "Brightwater's own email about the failed safety checks.",
      "Statement 2": "The gas engineer's warning letter to Brightwater.",
      "Statement 3": "The words spoken to the plaintiff's sister a week after the leak.",
      "Statement 4": "The maintenance clause of the tenancy agreement.",
      "Statement 5": "Brightwater's text message promising a repair visit.",
      "none of these": "None of the five statements is hearsay for the purpose for which it is offered."},
doc="""BENCH MEMO - Gallo v. Rupert Brightwater (carbon monoxide leak from a defective boiler)
Plaintiff's proposed evidence. The defendant, Rupert Brightwater, is an individual landlord.

Statement 1: An email from Brightwater to his letting agent in January: "The boiler in flat 3 has failed its safety check twice." Offered by the plaintiff to prove the boiler had failed its safety checks.
Statement 2: A letter from a gas engineer, Lars Odum, to Brightwater in February: "Boiler in flat 3 unsafe - do not use until repaired." Offered to show that Brightwater had been warned before the leak.
Statement 3: A neighbour, Olwen Pryce, telling the plaintiff's sister a week after the leak: "I could smell fumes from flat 3 for days before the leak." Offered to prove that fumes were escaping before the leak.
Statement 4: Clause 7 of the tenancy agreement: "The Landlord shall keep the boiler in safe working order." Offered to prove the terms of Brightwater's obligation.
Statement 5: A text from Brightwater to the plaintiff: "I'll send someone Monday to fix the boiler." Offered to prove that Brightwater promised a repair visit.""",
twin=dict(rep=[("Statement 3: A neighbour, Olwen Pryce, telling the plaintiff's sister a week after the leak:", "Statement 3: Brightwater himself telling the plaintiff's sister a week after the leak:")],
          gold="none of these")),

dict(n=117, j="A", rules=["A801"], d=3, shuffle=False,
q="How many of the six items are hearsay as Rule 801 defines it?", gold="2",
opts=[str(k) for k in range(7)],
defs=count_defs(6, "six items", "is hearsay as defined"),
doc="""ARVELL LAW SCHOOL - EVIDENCE TUTORIAL 6
Rhys v. Bruno Corran (trading as Corran Ice Cream): food poisoning at the Dunmore summer festival

The plaintiff offers each item below for the stated purpose. Bruno Corran, the defendant, runs the business alone.

(1) A sign on Corran's van: "All dairy kept below 4°C." Offered to show what Corran promised customers; the claim is for breach of that promise.
(2) An online review posted by a festival-goer two days later: "Got violently sick after Corran's mint choc chip." Offered to prove that the ice cream made people ill.
(3) The plaintiff's own statement to her doctor the next day: "I ate nothing except Corran's ice cream that day." Offered by the plaintiff to prove what she ate.
(4) Bruno Corran's remark to a festival steward at 14:00: "The freezer's been off since noon." Offered to prove the freezer was off.
(5) The steward's warning to Corran at 13:00: "Your freezer light's off, mate." Offered to show that Corran had been warned.
(6) The plaintiff's friend asking her that evening, "Are you going to be sick again?" Offered to prove that the plaintiff had already been sick."""),

dict(n=118, j="M", rules=["M801"], d=3, shuffle=False,
q="Under section 801, how many of the listed items are hearsay?", gold="3",
opts=[str(k) for k in range(6)],
defs=count_defs(5, "five items", "is hearsay under s.801"),
doc="""MORROW VALE UNIVERSITY - EVIDENCE PROBLEM CLASS
Kettle v. Ormsby: claim that Ormsby's bull escaped and trampled Kettle's barley

Each item is offered by Kettle for the purpose stated.

(1) Ormsby's own remark to a neighbour: "My bull got through the east fence last Tuesday." Offered to prove that the bull escaped.
(2) A sign Ormsby had fixed to his field gate: "Beware - bull loose in this field." Offered to prove that the bull was kept in that field.
(3) Kettle's farmhand telling Ormsby on Wednesday: "Your bull's in Kettle's barley." Offered only to show that Ormsby was told on Wednesday, because Kettle claims for damage after that date on the footing that Ormsby had been notified.
(4) Ormsby quietly repairing the east fence the next morning. Offered to show that the fence had been broken.
(5) The vet's invoice to Kettle: "Treatment of cow gored by bull - 40 crowns." Offered to prove that a bull injured Kettle's cow."""),

dict(n=119, j="H", rules=["H4"], d=3, shuffle=False,
q="Which item, if any, is not hearsay under section 4?", gold="Item 4",
opts=["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "all of them are hearsay"],
defs={"Item 1": "The calm emergency call about the blue coupe.",
      "Item 2": "Marr's text message to her brother.",
      "Item 3": "The motorcyclist pulling onto the verge.",
      "Item 4": "The coupe's automatic GPS speed log.",
      "Item 5": "The mechanic's note on the service record.",
      "all of them are hearsay": "Every listed item is hearsay under s.4."},
doc="""Halvard Reach Crown Court - Crown v. Delphine Marr (dangerous driving)
Items tendered by the Crown to prove that Marr was driving the blue coupe at about 140 km/h on the Weir Road at 23:10

Item 1: An emergency call made at 23:15, in which the caller, speaking calmly, says: "A blue coupe just flew past me on the Weir Road at well over a hundred."
Item 2: Marr's own text to her brother at 23:40: "Got the coupe up to 140 on the Weir Road, lol."
Item 3: The conduct of a motorcyclist who, seeing the coupe approach, pulled onto the verge and stopped. Tendered to prove that the coupe was travelling dangerously fast.
Item 4: The coupe's GPS module, which logs speed automatically without any input from the driver, recorded: "23:10:14 - 139.6 km/h - Weir Rd."
Item 5: A garage mechanic's note on the coupe's service record: "Speed limiter removed at owner's request." """),

dict(n=120, j="C", rules=["C20", "C30c"], d=3, shuffle=False,
q="How many of the five entries qualify under Article 30(c)?", gold="4",
opts=[str(k) for k in range(6)],
defs=count_defs(5, "five entries", "qualifies under Art. 30(c)"),
doc="""Coldmere Civil Court - Aldana v. Pinecrest Clinic (infection after minor surgery)

The clinic offers five entries from its "Equipment Sterilisation Register" to prove that the instruments were sterilised. The register is kept as a regular practice, and its custodian testifies. By clinic procedure, the technician who runs an autoclave cycle records it, or, when the technician is busy, the receptionist records it from the technician's report.

Entry A: Cycle of 1 February, recorded by technician Pia Sorn 20 minutes after the cycle.
Entry B: Cycle of 3 February, recorded by Sorn on 5 February, two days later, when catching up on paperwork.
Entry C: Cycle of 5 February (run by Sorn), recorded by receptionist Mo Dale two hours later from what Sorn told her.
Entry D: Cycle of 6 February, recorded by Sorn the same afternoon, after the clinic's lawyer phoned to warn that Aldana was threatening to sue and asked Sorn to write the cycle up "so we have proof."
Entry E: Cycle of 8 February, recorded by Sorn 30 hours after the cycle."""),
]
