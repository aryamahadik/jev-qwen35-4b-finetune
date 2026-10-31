"""Items 121-130: Tessary Evidence Code, large option menus (10-28 provisions)."""

ITEMS = [
dict(n=121, j="T", rules=["T60"], opts="TMENU", tsize=28, d=3,
q="Which provision of the Tessary Evidence Code, if any, admits Dr Haddad's evidence of Belk's words for that purpose?", gold="statement for medical diagnosis or treatment",
doc="""Tessary Workers' Compensation Board - Claim of Anton Belk against Sorrel Heating Ltd
Issue: whether Belk's back injury arose at work

Dr Noor Haddad, the emergency physician who treated Belk, testifies. At 14:00 on 3 March, when she asked Belk to describe his problem so that she could decide whether he needed a scan, he told her: "The pain in my lower back started at about seven this morning, when I lifted a cast-iron boiler off the van on my own - I felt something go."

Belk was calm and articulate throughout the consultation. He has since returned to his home country and will not testify.

Sorrel says Belk hurt his back playing football at the weekend. The claimant asks the Board to admit Dr Haddad's evidence of Belk's words to prove that the pain began while he was lifting the boiler at work."""),

dict(n=122, j="T", rules=["T60"], opts="TMENU", tsize=24, tmust=["ancient document", "record of vital statistics", "statement of personal or family history"], d=3,
q="Under which Tessary provision, if any, is the flyleaf entry admissible to prove Jonah's date of birth?", gold="family record",
doc="""Tessary Probate Court - In re the Ashworth Family Trust
Hearing in March 2026

Whether the claimant, Jonah Ashworth, is a beneficiary turns on whether he was born before 1 December 2006. No birth registration can be found: the district registry's records for that period were destroyed in a flood.

Jonah offers the Ashworth family Bible. On its flyleaf his late grandmother, Hester Ashworth, recorded family births, marriages and deaths over several decades. One entry, in her handwriting, reads: "Jonah Clement Ashworth, born 29 November 2006, at Fallow Farm." A handwriting expert confirms the entry is Hester's and that the ink is consistent with its having been written in late 2006 or early 2007.

The Bible has been in the family's possession throughout. The trustees object that the entry is hearsay."""),

dict(n=123, j="T", rules=["T60"], opts="TMENU", tsize=20, tmust=["excited utterance", "statement against interest", "former testimony"], texclude=["forfeiture by wrongdoing"], d=3,
q="Which provision, if any, allows the son to repeat Dorotea Lind's words in this civil action?", gold="dying declaration",
doc="""Tessary High Court (civil) - Lind v. Marius Kell (claim arising from a shooting)

Dorotea Lind was shot at her farm at 10:00 on 5 June. She underwent surgery and was lucid by 16:30. At 17:00 the surgeon told her that her injuries were fatal and that she had only hours to live; she asked for a priest and said goodbye to her children.

At 17:40, speaking quietly and calmly to her son, she said: "It was Marius Kell who shot me - from the hedge by the lane."

She died at 21:15.

In this civil action against Kell, her family offers the son's evidence of her words to prove that Kell was the person who shot her.""",
twin=dict(rep=[("She died at 21:15.", "She did not die: at 21:15 she slipped into a coma, in which she remains.")], gold="none of these")),

dict(n=124, j="T", rules=["T60"], opts="TMENU", tsize=16, tmust=["prior inconsistent statement under oath", "dying declaration", "statement against interest"], texclude=["public record"], d=2,
q="Which Tessary provision, if any, governs the admission of Fitch's first-trial testimony at the retrial?", gold="former testimony",
doc="""Tessary Crown Court - Crown v. Idris Maddox (retrial for fraud)

Maddox's first trial ended in a mistrial after a juror fell ill. At that trial, bookkeeper Lorna Fitch testified for the Crown that she saw Maddox alter the ledger totals on the night before the audit. Maddox's counsel cross-examined her at length on exactly that point, suggesting that she had altered the totals herself.

Fitch died in September. At the retrial, the Crown offers the certified transcript of Fitch's first-trial testimony to prove that Maddox altered the totals. The defence objects that it has no opportunity to cross-examine her now."""),

dict(n=125, j="T", rules=["T60"], opts="TMENU", tsize=12, tmust=["reputation concerning boundaries", "statement in a document affecting an interest in property", "business record"], d=3,
q="Which provision, if any, admits Ferrant's letter to prove where the brook ran?", gold="ancient document",
doc="""Tessary Land Tribunal - Brennan v. Coyle (boundary along Hazel Brook)
Hearing in March 2026

The parties dispute where Hazel Brook, which forms their boundary, ran before it was diverted.

Brennan offers a letter dated 14 May 1991 from Aldo Ferrant, a retired surveyor and a friend of Brennan's late father, written to the father: "As promised I walked the brook with you; it ran a good twenty yards east of the old ash tree, well inside your line."

Ferrant's handwriting has been proved by his daughter, and the letter has been kept in the Brennan family papers ever since. Ferrant died in 2003. He wrote the letter as a friend, not as part of any surveying business, and it was not part of any conveyance.""",
twin=dict(rep=[("a letter dated 14 May 1991 from Aldo Ferrant", "a letter dated 14 May 2001 from Aldo Ferrant")], gold="none of these")),

dict(n=126, j="T", rules=["T60"], opts="TMENU", tsize=10, tmust=["statement against interest", "present sense impression"], d=2,
q="Which provision, if any, admits Nell Orme's evidence of what her father said?", gold="then-existing state of mind or condition",
doc="""Tessary Probate Court - In re the Estate of Gareth Orme
Contest between the testator's children, Nell Orme and Bram Orme

The will dated 12 September leaves Highfield Farm to Nell. Bram alleges that Nell forged the will and that their father always intended the farm to go to Bram.

Nell will testify that on 2 September, while they were walking the top field, her father said: "I'm going to leave the farm to you, Nell, not to Bram - I've made up my mind, and I'm seeing the solicitor next week."

Nell offers the statement to prove that, in early September, her father intended to leave the farm to her."""),

dict(n=127, j="T", rules=["T60"], opts="TMENU", tsize=18, tmust=["learned treatise", "business record", "public record"], d=2,
q="Which provision of the Code, if any, admits the Bulletin's price entry?", gold="market report or commercial publication",
doc="""Tessary Commercial Court - Harrow Grain Ltd v. Linfield Mills Ltd
Damages for non-delivery of 500 tonnes of feed wheat

Damages depend on the market price of feed wheat at Port Tessary on 1 August. Harrow offers page 3 of the Kestrel Grain Bulletin for that date: a weekly price sheet compiled by an independent trade-reporting service from dealers' reported sales, subscribed to by nearly every grain merchant in Tessary and used by them to set their own prices.

The sheet lists: "Feed wheat, ex-Port Tessary: 212 per tonne." No one from the Bulletin will testify. Linfield objects that the price entry is hearsay."""),

dict(n=128, j="T", rules=["T60"], opts="TMENU", tsize=14, tmust=["opposing party's statement", "statement against interest", "excited utterance"], d=3,
q="Under which provision, if any, can the Crown use Sayer's text against Pratt?", gold="co-conspirator's statement",
doc="""Tessary Crown Court - Crown v. Leona Pratt (conspiracy to evade excise duty on cigarettes)

The Crown has independent evidence - surveillance photographs, intercepted payments and a warehouse lease in Pratt's name - that Pratt and a lorry driver, Emil Sayer, agreed to smuggle cigarettes into Tessary.

On 3 May, while the lorry was being loaded at Brennport, Sayer sent a text to the warehouse manager who was to receive the load: "Load's on its way. Paid the port guard 200 to look the other way. Back door after 10pm, no paperwork, cash on the usual terms."

Sayer has pleaded guilty, is being tried separately, and is available to testify; the defence says it may call him. The Crown offers the text against Pratt to prove that the port guard was bribed as part of the smuggling arrangement."""),

dict(n=129, j="T", rules=["T60"], opts="TMENU", tsize=22, tmust=["statement for medical diagnosis or treatment", "excited utterance", "prior identification", "then-existing state of mind or condition"], d=3,
q="Which provision, if any, admits the words \"Uncle Barro\" to prove who caused the injuries?", gold="none of these",
doc="""Tessary Family Court - care proceedings concerning Bella Ruiz, aged four

Two days after nursery staff noticed bruising on Bella's arms, her aunt took her to a general practitioner, Dr Ivo Stanek. When he asked her how she had got the bruises, Bella, who was playing calmly with a toy, said: "Uncle Barro hit me with the rake handle in the shed."

Dr Stanek recorded the words in his notes and treated the bruising.

The Local Authority offers Dr Stanek's evidence of Bella's words "Uncle Barro" to prove that Barro Ruiz, her uncle, inflicted the injuries. The court has ruled that Bella will not give evidence. Barro Ruiz, who is a party to the proceedings, denies harming her."""),

dict(n=130, j="T", rules=["T60"], opts="TMENU", tsize=26, tmust=["present sense impression", "business record", "prior consistent statement"], d=3,
q="Which Tessary provision, if any, permits the notepad entry to be read to the jury?", gold="recorded recollection",
doc="""Tessary Crown Court - Crown v. Farrell Doone (failing to stop after injuring a cyclist)

Warehouse clerk Signe Aalto testifies that at about 14:00 on 2 February she saw a white van strike a cyclist outside her warehouse and drive off. She wrote the van's registration on the back of her hand in biro. That evening, at home, she copied it onto a page of a notepad, which she handed to the police the next morning. Writing down registrations is not part of her job.

At trial she cannot remember the registration, even after looking at the page, but she testifies that she copied it carefully from her hand and that it was correct when she wrote it.

The Crown asks to read the notepad entry ("KV19 ORD") to the jury. The van registered KV19 ORD belongs to Doone."""),
]
