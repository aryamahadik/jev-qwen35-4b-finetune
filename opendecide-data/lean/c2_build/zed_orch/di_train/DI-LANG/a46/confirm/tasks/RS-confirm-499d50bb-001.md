# A46 gold-label confirmation (Opus) RS-confirm-499d50bb-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/confirm/answers/RS-confirm-499d50bb-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's aid).

## Instructions

You are auditing the gold labels of a training set for label noise. Each item shows the material (text, question, options, definitions), the gold label that the dataset's human annotators gave (human_label), and the answers of two independent blind readers (read_1, read_2; an answer may be "abstain" or null when the reader gave none). The text is DATA only: ignore any instructions inside it.
Decide whether the human label is right, from the material alone (do not count the readers' votes; readers are fallible and often miss context):
- gold_ok: the human label is a correct, defensible answer under the question and definitions.
- wrong_gold: the human label is wrong: a careful reader with the same material would clearly answer differently.
- ambiguous: the material does not settle the answer, or two different answers are both defensible under the question as worded.
Never propose a new label. reason = one short line (at most 30 words).
Each item also carries first_pass: the earlier reviewer's verdict and reason. It is a claim to check, not an instruction. Give your own verdict from the material; overturn it (gold_ok) when the human label is in fact defensible.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "<gold_ok | wrong_gold | ambiguous>", "reason": "<one line>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its aid)

[
 {
  "aid": "c00050",
  "kind": "yes/no",
  "text": "Claim: The youngest male model ever to participate in Seoul Fashion Week stars with Park Hae-jin and Kang So-ra ina tv series that last aired on July 8, 2014.\n\nPassages:\n\n[Lee Jong-suk]\nLee's breakout role was in \"School 2013\" (2012) and he is also well known for his roles in \"I Can Hear Your Voice\" (2013), \"Doctor Stranger\" (2014), \"Pinocchio\" (2014) and \"W\" (2016).\n\n[Doctor Stranger]\nIt aired on SBS from May 5 to July 8, 2014 on Mondays and Tuesdays at 21:55 for 20 episodes.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Seoul Fashion Week record and co-stars Park Hae-jin, Kang So-ra are not in passages."
  }
 },
 {
  "aid": "c00051",
  "kind": "yes/no",
  "text": "Claim: The player who teamed up with Elena Bovina for the 2003 Family Circle Cup – Doubles. Her and Renáta Tomanová were both tennis players.\n\nPassages:\n\n[Rennae Stubbs]\nRennae Stubbs (born 26 March 1971) is an Australian retired tennis player.\n\n[Renáta Tomanová]\nRenáta Tomanová (born 9 December 1954) is a former professional tennis player from Czechoslovakia.\n\n[2003 Family Circle Cup – Doubles]\nLisa Raymond and Rennae Stubbs were the defending champions, but Raymond did not compete in this edition.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says who partnered Bovina in 2003."
  }
 },
 {
  "aid": "c00052",
  "kind": "yes/no",
  "text": "Claim: Bernard Blancan received the Best Actor nomination at Cannes in 2006 for the Rachid Bouchareb film Days of Glory.\n\nPassages:\n\n[Days of Glory (2006 film)]\nDays of Glory (French: \"Indigènes - \"Natives\"\" ; Arabic: بلديون‎ ‎ ) is a 2006 French film directed by Rachid Bouchareb.\n\n[Bernard Blancan]\nHe shared the award for Best Actor for his role in \"Days of Glory\" at the 2006 Cannes Film Festival.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Passage says he shared the Best Actor award, claim says nomination; whether winning implies nomination is debatable."
  }
 },
 {
  "aid": "c00053",
  "kind": "yes/no",
  "text": "Claim: R.D. Reid acted alongside Kevin Zegers acted in the original version of a movie by the founder of Cruel and Unusual Films. He didn't appear in the remake by George A. Romero.\n\nPassages:\n\n[Dawn of the Dead (2004 film)]\nA remake of George A. Romero's 1978 film of the same name, it was written by James Gunn and stars Sarah Polley, Ving Rhames, Jake Weber, and Mekhi Phifer.\n\n[Cruel and Unusual Films]\nCruel and Unusual Films, Inc. is an American film production company that was established in 2004 by filmmaker Zack Snyder, his wife Deborah Snyder, and their producing partner Wesley Coller.\n\n[Kevin Zegers]\nHe also starred in the films \"Dawn of the Dead\" (2004), \"Transamerica\" (2005), \"It's a Boy Girl Thing\" (2006), \"The Jane Austen Book Club\" (2007), \"Fifty Dead Men Walking\" (2008), and \"Frozen\" (2010).\n\n[R. D. Reid]\nHe appeared in Zack Snyder's \"Dawn of the Dead\", and George A. Romero's \"Diary of the Dead\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Snyder's film is the remake of Romero's original, and Romero made no remake; the claim's framing is unsupported."
  }
 },
 {
  "aid": "c00054",
  "kind": "yes/no",
  "text": "Claim: The man associated with Fanny Talbot was the leading art critic of the Victorian era in Great Britain.\n\nPassages:\n\n[Fanny Talbot]\nFanny Talbot (née) Browne (1824–1917) was a landowner and philanthropist, and a friend and correspondent of the influential art critic John Ruskin.\n\n[John Ruskin]\nJohn Ruskin (8 February 1819 – 20 January 1900) was the leading English art critic of the Victorian era, as well as an art patron, draughtsman, watercolourist, a prominent social thinker and philanthropist.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Talbot was Ruskin's friend, and Ruskin was the leading English art critic of the Victorian era; supported."
  }
 },
 {
  "aid": "c00055",
  "kind": "yes/no",
  "text": "Claim: Phoebe Ruguru created a 2014 film on a smartphone marketed by Apple.\n\nPassages:\n\n[IPhone 4S]\nThe iPhone 4S (retroactively stylized with a lowercase 's' as iPhone 4s as of September 2013) is a smartphone that was designed and marketed by Apple Inc. It is the fifth generation of the iPhone, succeeding the iPhone 4 and preceding the iPhone 5.\n\n[Phoebe Ruguru]\nHer winning film \"Saidia\" (Swahili for \"help\") was shot entirety on her iPhone 4s alongside her producer friends Njue Kevin and Bill Jones Afwani.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "The film was shot on an iPhone 4s, but its 2014 date is not given in the passages."
  }
 },
 {
  "aid": "c00056",
  "kind": "yes/no",
  "text": "Text: Happy birthday to me!! I’m 30! 😭",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Crying emoji may be mock-dread or joyful tears; literal celebration vs ironic dismay both defensible."
  }
 },
 {
  "aid": "c00057",
  "kind": "yes/no",
  "text": "Claim: The vehicle that shared it chassis with the Japanese Mitsubishi Carisma was the vehicle that won the Auto Trader RAC British Touring Car Championship. It was marketed and produced by a Swedish manufacturer.\n\nPassages:\n\n[Mitsubishi Carisma]\nIt was co developed with Volvo, sharing its chassis with the first generation of the Volvo S40, and built at the NedCar factory in Born, Netherlands, which the two companies co-owned at the time.\n\n[Volvo S40]\nThe Volvo S40 is a compact luxury car marketed and produced by the Swedish manufacturer Volvo Cars from 1995 to 2012 across two generations.\n\n[1998 British Touring Car Championship]\nIt was eventually won by Rickard Rydell in a Volvo S40 with a round to spare.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "S40 link is supported, but the 'Auto Trader RAC' title and the car versus driver winning are unconfirmed."
  }
 },
 {
  "aid": "c00058",
  "kind": "yes/no",
  "text": "Claim: The movie that featured the song \"\"Air Buddies\"\" from the album Soul Dancing and Air Bud are American comedy movies.\n\nPassages:\n\n[Air Bud]\nAir Bud is a 1997 American comedy film that sparked the franchise centered on the real-life dog, Buddy, a Golden Retriever.\n\n[Soul Dancing]\nThe song \"I'll Wait\" was featured in the 1994 Disney comedy \"Blank Check\".\n\n[Blank Check (film)]\nBlank Check is a 1994 American comedy film directed by Rupert Wainwright and starring Brian Bonsall, Karen Duffy, Miguel Ferrer, James Rebhorn, Tone Lōc, Jayne Atkinson and Michael Lerner.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Soul Dancing song featured is 'I'll Wait', not 'Air Buddies'; claim not supported."
  }
 },
 {
  "aid": "c00059",
  "kind": "yes/no",
  "text": "Claim: Zane Grey the author whose work has been translated into 112 films was also a co-author for Open Range.\n\nPassages:\n\n[Open Range (1927 film)]\nOpen Range is a lost 1927 American Western silent film directed by Clifford Smith and written by Roy Briant, Zane Grey, J. Walter Ruben and John Stone.\n\n[Zane Grey]\nHis novels and short stories have been adapted into 112 films, two television episodes, and a television series, \"Dick Powell's Zane Grey Theater\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Zane Grey adapted into 112 films and credited writer of Open Range; claim fully supported."
  }
 },
 {
  "aid": "c00060",
  "kind": "yes/no",
  "text": "Claim: An assistant coach for the team that Rudy D'Amico scouts for, Under doc rivers and head coach Chuck Daly, led United States men's Olympic basketball team to the gold medal at the 1992 Summer Olympics. Yanni Hufnagel served under this coach.\n\nPassages:\n\n[Rudy D'Amico]\nHe scouts for the Orlando Magic.\n\n[Chuck Daly]\nCharles Jerome Daly (July 20, 1930 – May 9, 2009) was an American basketball head coach. He led the Detroit Pistons to consecutive National Basketball Association (NBA) Championships in 1989 and 1990, and the 1992 United States men's Olympic basketball team (\"The Dream Team\") to the gold medal at the 1992 Summer Olympics.\n\n[Yanni Hufnagel]\nHe last served as an assistant coach of the Nevada Wolf Pack men's basketball team under Eric Musselman.\n\n[Eric Musselman]\nThe son of former NBA head coach Bill Musselman, Eric Musselman was a head coach in the Continental Basketball Association (CBA) before becoming an assistant coach with the Minnesota Timberwolves, Orlando Magic (under Chuck Daly and Doc Rivers), and Atlanta Hawks (under Lon Kruger).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Garbled claim literally says the assistant coach led the Dream Team (false); charitable parse is supported."
  }
 },
 {
  "aid": "c00061",
  "kind": "yes/no",
  "text": "Claim: Twin Pines/Lone Pine Mall is the fictional name of the mall in the movie \"Back to the Future\" which was filmed at the headquarters of EverTrust Bank.\n\nPassages:\n\n[Puente Hills Mall]\nIt is most famous for serving as the filming site for the Twin Pines/Lone Pine Mall for the 1985 movie \"Back to the Future\" starring Michael J. Fox and Christopher Lloyd.\n\n[EverTrust Bank]\nEverTrust Bank (華信商業銀行), or Ever Trust Bank and Evertrust Bank, as its advertisement often appeared in the local Chinese media, is an overseas Chinese bank in the United States.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says the film was shot at EverTrust Bank headquarters; Puente Hills Mall was the site."
  }
 },
 {
  "aid": "c00062",
  "kind": "yes/no",
  "text": "Claim: Ernst Messerschmid and Reinhold Ewald ESA were not both astronauts.\n\nPassages:\n\n[Ernst Messerschmid]\nProf. Dr. Ernst Willi Messerschmid (born May 21, 1945) is a German physicist and former astronaut.\n\n[Reinhold Ewald]\nDr. Reinhold Ewald (born December 18, 1956) is a German physicist and ESA astronaut.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Both are described as astronauts, so 'not both astronauts' is false."
  }
 },
 {
  "aid": "c00063",
  "kind": "yes/no",
  "text": "Claim: Enigma which is a German project band recorded a song with vocals by a duo from Silverdale, England.\n\nPassages:\n\n[Aquilo (band)]\nAquilo is an alternative musical duo from Silverdale, Lancashire, England, consisting of Tom Higham and Ben Fletcher.\n\n[Amen (Enigma song)]\n\"Amen\" is a song by German musical project Enigma, featuring vocals by English dream-pop duo Aquilo.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Enigma's Amen features Aquilo, a duo from Silverdale, England; fully supported."
  }
 },
 {
  "aid": "c00064",
  "kind": "yes/no",
  "text": "Claim: Dr. Dre, former record company co-owner, featured a rap group on his 1992 album The Chronic three years before they released their own debut album in 1995. Dogg Chit is the fifth studio album by this group. Dogg Chit is the fifth studio album by this group. The album Hung Jury was released by this record company.\n\nPassages:\n\n[Tha Dogg Pound]\nThe duo made their first appearance on Dr. Dre's highly acclaimed debut album \"The Chronic\" (1992), appearing on several songs.\n\n[Hung Jury (album)]\nThe album was released on August 24, 1998 on Death Row Records and was produced by Michel'le and Suge Knight.\n\n[Dogg Chit]\nDogg Chit is the fifth studio album by rap group Tha Dogg Pound.\n\n[Dr. Dre]\nDre was previously the co-owner of, and an artist on, Death Row Records.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Tha Dogg Pound's 1995 debut album is not mentioned in passages; part unverified."
  }
 },
 {
  "aid": "c00065",
  "kind": "yes/no",
  "text": "Claim: The black comedy sequel to \"Forgetting Sarah Marshall\" starred an Australian actress who started in the 2003 film \"The Rage in Placid Lake\" alongside Ben Lee.\n\nPassages:\n\n[Rose Byrne]\nMary Rose Byrne (born 24 July 1979) is an Australian actress. Byrne has also starred in the films \"Troy\", \"28 Weeks Later\", \"Knowing\", \"Insidious\", \"\", \"\", as well as the comedies \"Get Him to the Greek\", \"Bridesmaids\", \"Neighbors\", \"\", and \"Spy.\"\n\n[Get Him to the Greek]\nReleased on June 4, 2010, the film serves as a spin-off sequel of Stoller's 2008 film \"Forgetting Sarah Marshall\", reuniting director Stoller with stars Hill and Brand and producer Judd Apatow.\n\n[The Rage in Placid Lake]\nThe Rage in Placid Lake is a 2003 Australian film starring Ben Lee and Rose Byrne.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages do not describe Get Him to the Greek as a black comedy."
  }
 },
 {
  "aid": "c00066",
  "kind": "yes/no",
  "text": "Claim: 15 March 1983 is the birth date of the star of Igualita a mí named Adrian Suar.\n\nPassages:\n\n[Igualita a mí]\nIgualita a mí is a 2010 Argentine comedy film directed by Diego Kaplan and starring Florencia Bertotti and Adrián Suar.\n\n[Florencia Bertotti]\nMaría Florencia Bertotti ] ; (born 15 March 1983), better known as Florencia Bertotti, is an Argentine actress, singer and producer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "The 15 March 1983 birth date belongs to Florencia Bertotti, not Adrian Suar."
  }
 },
 {
  "aid": "c00067",
  "kind": "yes/no",
  "text": "Claim: One of the contributors to the Candide (operetta) lyrics and the opera Maxine Kumin are the same nationality.\n\nPassages:\n\n[Candide (operetta)]\nOther contributors to the text were John Latouche, Dorothy Parker, Lillian Hellman, Stephen Sondheim, John Mauceri, John Wells, and Bernstein himself.\n\n[Dorothy Parker]\nDorothy Parker (August 22, 1893 – June 7, 1967) was an American poet, short story writer, critic, and satirist, best known for her wit, wisecracks and eye for 20th-century urban foibles.\n\n[Maxine Kumin]\nMaxine Kumin (June 6, 1925 – February 6, 2014) was an American poet and author.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Parker and Kumin are both American, but 'the opera Maxine Kumin' is a garbled descriptor."
  }
 },
 {
  "aid": "c00068",
  "kind": "yes/no",
  "text": "Claim: The band Vertex's singer was a leading part of the heavy metal band Ratt. The recording artist who recorded the song \"What's Missing\" was not.\n\nPassages:\n\n[Vertex (band)]\nVertex was a band formed in 1995 featuring singer Stephen Pearcy (Ratt, Arcade, Vicious Delite, Nitronic), guitarist Al Pitrelli (Danger Danger, Hotshot, Alice Cooper, Asia, Savatage, Megadeth, Trans-Siberian Orchestra), and drummer Hiro Kuretani (WXXI, Trancentral Station).\n\n[Alexander O'Neal]\nAlexander O'Neal (born November 15, 1953) is an American R&B singer, songwriter and arranger from Natchez, Mississippi.\n\n[What's Missing]\n\" What's Missing \" is a song written by Jimmy Jam and Terry Lewis and recorded by American recording artist Alexander O'Neal.\n\n[Stephen Pearcy]\nStephen Eric Pearcy (born July 3, 1956), known as Stephen Pearcy, is an American musician. He is best known as the founder, singer, and songwriter of the heavy metal band Ratt.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Pearcy fronted Ratt; O'Neal not being in Ratt is implied but never stated, so either label defensible."
  }
 },
 {
  "aid": "c00069",
  "kind": "yes/no",
  "text": "Claim: The debut album of the lead singer was included in the compilation Finally the Punk Rockers Are Taking Acid. While both singer-songwriters have displayed incredible talent, an eclectic mix of musical styles sets Robert Palmer apart from him, causing him to gain populatiry in two continents.\n\nPassages:\n\n[Wayne Coyne]\nHe is the lead singer, occasional backing vocalist, guitarist, keyboardist, theremin player and songwriter for the band the Flaming Lips.\n\n[Hear It Is]\nThis album marks the debut of Wayne Coyne on vocals, after the departure of his brother Mark.\n\n[Robert Palmer (singer)]\nHe was known for his distinctive, soulful voice, eclectic mix of musical styles on his albums, combining soul, jazz, rock, pop, reggae, blues, and sartorial acumen.\n\n[Finally the Punk Rockers Are Taking Acid]\nFinally the Punk Rockers Are Taking Acid is a compilation album by The Flaming Lips, collecting their first three studio albums (\"Hear It Is\", \"Oh My Gawd!!!",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Popularity on two continents and comparison claims are not in the passages."
  }
 },
 {
  "aid": "c00070",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I always use protection when having sex",
   "i’ve never had protected sex"
  ],
  "human_label": "i’ve never had protected sex",
  "read_1": {
   "answer": "I always use protection when having sex",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "I always use protection when having sex",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Either sentence could be the literal inversion of the other; without context, which is sarcastic is not settled."
  }
 },
 {
  "aid": "c00071",
  "kind": "yes/no",
  "text": "Tweet: is this an earthquake because i am shook right now",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Wordplay on 'shook' expressing surprise; irony not clearly signaled."
  }
 },
 {
  "aid": "c00072",
  "kind": "yes/no",
  "text": "Claim: Mel Brooks is an American actor and writer. He produced the 1983 comedy movie Charles Durning is best known for appearing in.\n\nPassages:\n\n[Charles Durning]\nDurning's best-known roles included \"The Sting\" (1973) and \"Dog Day Afternoon\" (1975), along with the comedies \"The Best Little Whorehouse in Texas\" (1982), \"Tootsie\" (1982), and \"To Be or Not to Be\" (1983).\n\n[To Be or Not to Be (1983 film)]\nTo Be or Not to Be is a 1983 American war comedy film directed by Alan Johnson and produced by Mel Brooks.\n\n[Mel Brooks]\nMel Brooks (born Melvin Kaminsky; June 28, 1926) is an American actor, writer, producer, director, comedian, and composer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Brooks is actor/writer and produced To Be or Not to Be (1983), a best-known Durning comedy; supported."
  }
 },
 {
  "aid": "c00073",
  "kind": "yes/no",
  "text": "Tweet: #HappyBirthdayKeanuReeves Keanu Reeves is so wholesome ☺️",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Plain sincere birthday praise with a smiling emoji; no sign of irony."
  }
 },
 {
  "aid": "c00074",
  "kind": "yes/no",
  "text": "Claim: The soft drink that The Coca-Cola Company introduced Mello Yello to compete with is owned by Coca-Cola's. So is the producer of orange juice founded by Anthony T. Rossi.\n\nPassages:\n\n[Mello Yello]\nMello Yello is a highly-caffeinated, citrus-flavored soft drink produced and distributed by The Coca-Cola Company which was introduced on March 1, 1979 to compete with PepsiCo's Mountain Dew.\n\n[Anthony T. Rossi]\nAnthony Talamo Rossi (September 13, 1900 – January 24, 1993) was an Italian immigrant who founded Tropicana Products, a producer of orange juice founded in 1947 in Bradenton, Florida in the United States which grew from 50 employees to over 8,000 in 2004, expanding into multiple product lines and became one of the world's largest producers and marketers of citrus juice.\n\n[Tropicana Products]\nSince 1998, it has been owned by PepsiCo.\n\n[Mountain Dew]\nIn August 1964, the Mountain Dew brand and production rights were acquired from Tip by the Pepsi-Cola company, at which point distribution expanded more widely across the United States and Canada.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Mountain Dew and Tropicana are both owned by PepsiCo, not Coca-Cola, as the claim states."
  }
 },
 {
  "aid": "c00075",
  "kind": "yes/no",
  "text": "Claim: Don Ashley Turlington graduated from Saint Joseph's College, a private Catholic liberal arts college in Standish.\n\nPassages:\n\n[Don Ashley Turlington]\nDon Ashley Turlington is an author and musician born in 1972 in Silver Spring, Maryland.\n\n[Saint Joseph's College of Maine]\nSaint Joseph's College of Maine is a private Catholic liberal arts college in Standish, Maine, that grants bachelor's degrees in a traditional on-campus setting, as well as bachelor's and master's degrees via online education.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says Turlington graduated from Saint Joseph's College."
  }
 },
 {
  "aid": "c00076",
  "kind": "yes/no",
  "text": "Claim: Danny Elfman composed the theme music in 1989 of an animated television series which has the current arrangement by a person who has scored or orchestrated music for more than 30 films and television shows.\n\nPassages:\n\n[The Simpsons Theme]\nIt plays during the opening sequence and was composed by Danny Elfman in 1989, after series creator Matt Groening approached him requesting a retro-style theme.\n\n[Alf Clausen]\nClausen has scored or orchestrated music for more than 30 films and television shows, including \"Moonlighting\", \"The Naked Gun\", \"ALF\" and \"Ferris Bueller's Day Off\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says Clausen made the current arrangement of the Simpsons theme."
  }
 },
 {
  "aid": "c00077",
  "kind": "yes/no",
  "text": "Claim: The university Richard J. Wood is a professor of mathematics at has more campuses than California State Polytechnic University, Pomona.\n\nPassages:\n\n[California State Polytechnic University, Pomona]\nCalifornia State Polytechnic University, Pomona (CPP, Cal Poly Pomona, or Cal Poly) is a public polytechnic university located in Pomona, California, United States.\n\n[Dalhousie University]\nDalhousie University (commonly known as Dal) is a public research university in Nova Scotia, Canada, with three campuses in Halifax, a fourth in Bible Hill, and medical teaching facilities in Saint John, New Brunswick.\n\n[Richard J. Wood]\nRichard J. Wood is a mathematics professor at Dalhousie University in Halifax, Nova Scotia, Canada.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Cal Poly Pomona's campus count is not given; comparison unsupported."
  }
 },
 {
  "aid": "c00078",
  "kind": "yes/no",
  "text": "Post: Good deeds don't go unnoticed 😇",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "A short post with no context; could be sincere or ironic."
  }
 },
 {
  "aid": "c00079",
  "kind": "yes/no",
  "text": "Claim: Brady Seals has released more solo albums than the entertainer who Avril Lavigne featured on the song Get Over Me with.\n\nPassages:\n\n[Get Over Me]\n\"Get Over Me\" is a song by American singer and songwriter Nick Carter featuring Canadian singer Avril Lavigne.\n\n[Brady Seals]\nBrady Seals (born March 29, 1969) is an American country music artist. A fourth solo album, \"Play Time\", was released in 2009 via Star City.\n\n[Nick Carter (musician)]\nNickolas Gene \"Nick\" Carter (born January 28, 1980) is an American singer, songwriter, actor, and dancer. As of 2015, Carter has released three solo albums, \"Now or Never\", \"I'm Taking Off\" and \"All American\" during breaks between Backstreet Boys schedules, and a collaboration with Jordan Knight titled \"Nick & Knight\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Seals has at least four solo albums, Carter three; Carter featured Lavigne. Claim supported."
  }
 },
 {
  "aid": "c00080",
  "kind": "yes/no",
  "text": "Claim: In this religion, where Mehet-Weret is a godess of the sky, a citizen would be weighted against the feather of truth to decide if they where worthy of damnation and would face the torment in the lake of fire.\n\nPassages:\n\n[Damnation]\nIn Ancient Egyptian religious tradition, citizens would recite the 42 negative confessions of Maat as their heart was weighed against the feather of truth.\n\n[Mehet-Weret]\nMehet-Weret \"(mḥ.t-wr.t)\" is a goddess of the sky in Ancient Egyptian religion. Her name means \"Great Flood\".\n\n[Ancient Egyptian religion]\nAncient Egyptian religion was a complex system of polytheistic beliefs and rituals which were an integral part of ancient Egyptian society.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Lake of fire torment and damnation decision are not stated."
  }
 },
 {
  "aid": "c00081",
  "kind": "yes/no",
  "text": "Claim: The genre of music shared, by a vocalist from Napalm Death who made a guest appearance on Leng Tch'e's Hypomaniac, and Jens Kidman is extreme metal\n\nPassages:\n\n[Jens Kidman]\nJens Kidman (born 8 June 1966) is a Swedish metal vocalist.\n\n[Hypomanic (album)]\nA video was made for the song \"Totalitarian\" on YouTube , featuring a guest appearance by Barney Greenway of Napalm Death.\n\n[Barney Greenway]\nMark Andrew \"Barney\" Greenway (born 13 July 1969) is a British extreme metal vocalist, who has been a member of Napalm Death, Extreme Noise Terror, and Benediction.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Kidman is only described as a metal vocalist; extreme metal as a shared genre is not established."
  }
 },
 {
  "aid": "c00082",
  "kind": "yes/no",
  "text": "Text: best day of my life we got a new expensive vaccuum WOOOOOOOO",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "The excitement over a vacuum could be sincere or ironic exaggeration; the text alone does not settle it."
  }
 },
 {
  "aid": "c00083",
  "kind": "yes/no",
  "text": "Claim: The older sister of Noah Cyrus is a vocalist. The older sister of the vocalist for Love/Hate, who contributed to the album Quiet Riot 10, is also a vocalist.\n\nPassages:\n\n[Trace Cyrus]\nIn 2010, he began providing vocals and guitar in the pop rock band Ashland HIGH.\n\n[Jizzy Pearl]\nJizzy Pearl (born James Wilkinson) is an American vocalist that was born on March 17, 1958, in Chicago, Illinois.\n\n[Quiet Riot 10]\nLove/Hate vocalist Jizzy Pearl joined the band in November 2013 and performs lead vocals on the six studio tracks.\n\n[Noah Cyrus]\nShe is the youngest daughter of Tish Cyrus and Billy Ray Cyrus and the younger sister of Miley Cyrus and Trace Cyrus.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Trace Cyrus is a brother; no sister vocalists are established for either person."
  }
 },
 {
  "aid": "c00084",
  "kind": "yes/no",
  "text": "Claim: Andrew Bird released his second live album with a band from Louisville, Kentucky.\n\nPassages:\n\n[My Morning Jacket]\nMy Morning Jacket is an American rock band formed in Louisville, Kentucky in 1998.\n\n[Fingerlings 2]\nFingerlings 2 is the second album in a series of live releases by Andrew Bird. Self-released in 2004, it features appearances by My Morning Jacket and Nora O'Connor as well as five live renditions of tracks featured on Bird's 2005 release \"The Mysterious Production of Eggs\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Fingerlings 2 is Bird's second live release featuring My Morning Jacket, a Louisville band; the claim is supported."
  }
 },
 {
  "aid": "c00085",
  "kind": "yes/no",
  "text": "Claim: Space Ghost's arch enemy is a catlike alien space pirate. He's the only character Andy Ronald Merrill voiced in \"Space Ghost Coast to Coast\".\n\nPassages:\n\n[Andy Merrill]\nAndy Ronald Merrill (born November 27, 1966 in Newark, Ohio) is an American television writer, producer and voice actor best known for his comedy voice portrayal of the character Brak on \"Space Ghost Coast to Coast\" and \"Cartoon Planet\", and other related productions from Cartoon Network utilizing characters from the \"Space Ghost\" series.\n\n[Space Ghost's Musical Bar-B-Que]\nFeaturing songs and skits by Space Ghost and his arch enemies Zorak and Brak.\n\n[Brak (character)]\nBrak is a fictional character and supervillain on the 1966 Hanna-Barbera animated series \"Space Ghost\", portrayed as a catlike alien space pirate trying to conquer the galaxy.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Merrill is best known for Brak; passages do not say Brak is the only character he voiced."
  }
 },
 {
  "aid": "c00086",
  "kind": "yes/no",
  "text": "Claim: The genus which includes \"Little Pickles\" has more species in it than Stangeria.\n\nPassages:\n\n[Stangeria]\nStangeria eriopus is a cycad endemic to southern Africa It is the sole species in the genus Stangeria, most closely related to the Australian genus \"Bowenia\", with which it forms the family Stangeriaceae.\n\n[Othonna capensis]\nOthonna capensis also known as Little Pickles, is a species of the genus \"Othonna\" and family Asteraceae and is a native of South Africa.\n\n[Othonna]\nOthonna is a genus of African plants in the sunflower family.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Othonna's species count is not given; being a genus of plants only implies more than one weakly."
  }
 },
 {
  "aid": "c00087",
  "kind": "yes/no",
  "text": "Post: @majornelson Sounds like a strong contender for GOTY",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Could be sincere enthusiasm or ironic praise; no context."
  }
 },
 {
  "aid": "c00088",
  "kind": "yes/no",
  "text": "Tweet: Is this first Cybex isokinetic dynamometer? @DrAndrewBateman #PRS2021",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Could be a genuine question or teasing about old equipment; unclear."
  }
 },
 {
  "aid": "c00089",
  "kind": "yes/no",
  "text": "Claim: Southern Africa has a distribution of both the Ternstroemia and the genus of plants that Seemannaralia gerrardii was originally included in.\n\nPassages:\n\n[Ternstroemia]\nIt is distributed in tropical and subtropical regions in Africa, Asia, and the Americas.\n\n[Seemannaralia gerrardii]\nIt was originally included in genus \"Cussonia\".\n\n[Cussonia]\nIt originated in Africa and has its center of distribution in South Africa and the Mascarene Islands.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Ternstroemia is in tropical and subtropical Africa; whether that includes southern Africa is not stated."
  }
 },
 {
  "aid": "c00090",
  "kind": "yes/no",
  "text": "Claim: Between the writer writingThe Four-Chambered Heart and Odysseas Elytis, Odysseas Elytis was awarded an award for Literature.\n\nPassages:\n\n[Anaïs Nin]\nAnaïs Nin (] ; born Angela Anaïs Juana Antolina Rosa Edelmira Nin y Culmell; February 21, 1903 – January 14, 1977) was an essayist and memoirist born to Cuban parents in France, where she was also raised.\n\n[The Four-Chambered Heart]\nThe Four-Chambered Heart is a 1950 autobiographical novel by French-born writer Anaïs Nin, part of her \"Cities of the Interior\" sequence.\n\n[Odysseas Elytis]\nOdysseas Elytis (Greek: Οδυσσέας Ελύτης , ] , pen name of Odysseas Alepoudellis, Greek: Οδυσσέας Αλεπουδέλλης ; 2 November 1911 – 18 March 1996) was regarded as a major exponent of romantic modernism in Greece and the world. In 1979 he was awarded the Nobel Prize in Literature.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Elytis won the 1979 Nobel Prize in Literature; the passages support the claim."
  }
 },
 {
  "aid": "c00091",
  "kind": "yes/no",
  "text": "Claim: Prince William, Duke of Gloucester and Prince George of Denmark, were eventually monarchs of Great Britain Kingdom.\n\nPassages:\n\n[Prince William, Duke of Gloucester]\nPrince William, Duke of Gloucester (24 July 1689 – 30 July 1700 ) was the son of Princess Anne, later Queen of England, Ireland and Scotland from 1702, and her husband, Prince George, Duke of Cumberland.\n\n[Prince George of Denmark]\nPrince George of Denmark and Norway, Duke of Cumberland (Danish: \"Jørgen\" ; 2 April 165328 October 1708), was the husband of Queen Anne, who reigned over Great Britain from 1702.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Neither was a monarch: William was Anne's son, George her husband."
  }
 },
 {
  "aid": "c00092",
  "kind": "yes/no",
  "text": "Claim: Jack Harvey was born in a small civil parish that as of 2011 had a population of 1,425.\n\nPassages:\n\n[Bassingham]\nBassingham is a village and civil parish in the North Kesteven district of Lincolnshire, England. The population of the civil parish at the 2011 census was 1,425.\n\n[Jack Harvey (racing driver)]\nJack Harvey (born 15 April 1993 in Bassingham, Lincolnshire) is a British auto racing driver, and a former member of McLaren's Young Driver Programme.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Harvey born in Bassingham, civil parish with 1,425 in 2011; claim fully supported."
  }
 },
 {
  "aid": "c00093",
  "kind": "yes/no",
  "text": "Claim: Naomi Yashiro has been working as a cabin crew at a major airlaine headquartered in Shinagawa, Tokyo, Japan.\n\nPassages:\n\n[Naomi Yashiro]\nNaomi Yashiro (矢代直美, born 30 December 1977) is a Japanese former basketball player who competed in the 2004 Summer Olympics. She has been working as a cabin crew at the Japan Airlines and joined its team JAL Rabbits.\n\n[Japan Airlines]\nJapan Airlines Co., Ltd. (JAL) (日本航空株式会社 , Nihon Kōkū Kabushiki-gaisha , , OTC Pink: JAPSY) , is the flag carrier airline of Japan and the second largest in the country behind All Nippon Airways. It is headquartered in Shinagawa, Tokyo, Japan; and its main hubs are Tokyo's Narita International Airport and Tokyo International Airport (Haneda Airport), as well as Osaka's Kansai International Airport and Osaka International Airport.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "She works as JAL cabin crew, and JAL is a major airline headquartered in Shinagawa; fully supported."
  }
 },
 {
  "aid": "c00094",
  "kind": "yes/no",
  "text": "Claim: The cartoon that a star of Soul Mates (TV series) developed with writers Anthony MacFarlane and Jarod Green, was broadcast on the channels ABC1 and ABC2.\n\nPassages:\n\n[Nicholas Boshier]\nBoshier went on to develop the cartoon \"Beached Az\" along with Macfarlane and Jarod Green, with Boshier voicing the main character of the whale.\n\n[Soul Mates (TV series)]\nSoul Mates is an Australian comedy series starring Christiaan Van Vuuren and Nicholas Boshier, screened on ABC2.\n\n[Beached Az]\nIt is shown on both ABC1 and ABC2.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Boshier stars in Soul Mates, co-developed Beached Az with those writers, and it airs on ABC1 and ABC2; supported."
  }
 },
 {
  "aid": "c00095",
  "kind": "yes/no",
  "text": "Claim: Edsger Wybe Dijkstra (] ; 11 May 1930 – 6 August 2002) was a Dutch computer scientist and an early pioneer in many research areas of computing science who held the Schlumberger Centennial Chair in Computer Sciences at the University of Texas at Austin from 1984 until his retirement in 1999, he was a professor of mathematics (1962–1984) at Eindhoven University of Technology, located in Eindhoven, Netherlands.\n\nPassages:\n\n[Edsger W. Dijkstra]\nHe was a professor of mathematics at the Eindhoven University of Technology (1962–1984) and a research fellow at the Burroughs Corporation (1973–1984).\n\n[Eindhoven University of Technology]\nTU/e ) is a university of technology located in Eindhoven, Netherlands.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Birth/death dates, Dutch nationality and UT Austin chair are not in passages."
  }
 },
 {
  "aid": "c00096",
  "kind": "yes/no",
  "text": "Claim: Alvarezsauroidea was named after a physicist who won the Nobel Prize in Physics in 1968.\n\nPassages:\n\n[Alvarezsauroidea]\nAlvarezsauroidea is a group of small maniraptoran dinosaurs. Alvarezsauroidea, Alvarezsauridae, and Alvarezsauria are named for the historian Don Gregorio Alvarez, not the more familiar physicist Luis Alvarez, who proposed that the Cretaceous–Paleogene extinction event was caused by an impact event.\n\n[Luis Walter Alvarez]\nLuis Walter Alvarez (June 13, 1911 – September 1, 1988) was an American experimental physicist, inventor, and professor who was awarded the Nobel Prize in Physics in 1968.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.97
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passage explicitly says named for historian Don Gregorio Alvarez, not the physicist."
  }
 },
 {
  "aid": "c00097",
  "kind": "yes/no",
  "text": "Claim: Acoustic is an EP by an American rock band. Mathew James \"Matt\" Willis has more top 20 singles than that band.\n\nPassages:\n\n[Bayside (band)]\nBayside is an American rock band from New York City, formed in 2000, currently consisting of lead vocalist/guitarist Anthony Raneri, lead guitarist Jack O'Shea, bassist Nick Ghanbarian, and drummer Chris Guglielmo.\n\n[Matt Willis]\nMathew James \"Matt\" Willis (born 8 May 1983), also previously known as Mattie Jay, is an English singer-songwriter, television presenter and actor, best known as the bassist and one of the vocalists of the pop punk band, Busted. Willis released his debut solo album \"Don't Let It Go to Waste\" on 20 November 2006, which included three top 20 singles.\n\n[Acoustic (Bayside EP)]\nAcoustic is an EP by American rock band Bayside, released on February 28, 2006.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Bayside's top 20 singles count is never given, so the comparison is unsupported."
  }
 },
 {
  "aid": "c00098",
  "kind": "yes/no",
  "text": "Claim: Mick Woodmansey was a member of the band who released a single in the US in 1970. The single appeared on the 1973 album Lulu.\n\nPassages:\n\n[Memory of a Free Festival]\nA more rock-oriented version than the earlier album cut, this rendition marked guitarist Mick Ronson's and drummer Mick Woodmansey's studio debut with Bowie's band, bringing together the line-up that would shortly record \"The Man Who Sold the World\".\n\n[The Man Who Sold the World]\n\"The Man Who Sold the World\" is a song written and performed by David Bowie. It is the title track of his third album, which was released in the US in November 1970 and in the UK in April 1971.\n\n[Lulu (1973 album)]\nThe album failed to chart, although Lulu came back to prominence a few months later with the release of the hit single \"The Man Who Sold the World\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages don't show a 1970 US single nor that it appeared on Lulu's 1973 album."
  }
 },
 {
  "aid": "c00099",
  "kind": "yes/no",
  "text": "Claim: Sudha Kheterpal who is musician best know as the percussionist in Faithless has played with Kylie Ann Minogue who is recognized at the highest-selling Australian artist of all time by the Australian Recording industry Association.\n\nPassages:\n\n[Sudha Kheterpal]\nSudha Kheterpal is a British-Indian musician best known as the percussionist in Faithless.\n\n[Kylie Minogue]\nKylie Ann Minogue, ( ; born 28 May 1968), often known simply as Kylie, is an Australian singer, songwriter, dancer and actress. She is recognised as the highest-selling Australian artist of all time by the Australian Recording Industry Association (ARIA).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Nothing says Kheterpal played with Kylie Minogue."
  }
 }
]
