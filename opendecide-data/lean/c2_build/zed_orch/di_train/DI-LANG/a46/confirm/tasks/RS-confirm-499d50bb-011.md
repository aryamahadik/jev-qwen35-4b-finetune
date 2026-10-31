# A46 gold-label confirmation (Opus) RS-confirm-499d50bb-011

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/confirm/answers/RS-confirm-499d50bb-011.json

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
  "aid": "c00550",
  "kind": "yes/no",
  "text": "Claim: Enola Gay was one of the bombers that targeted the largest city on the Japanese island of Kyushu.\n\nPassages:\n\n[Enola Gay]\nClouds and drifting smoke resulted in a secondary target, Nagasaki, being bombed instead.\n\n[Nagasaki]\nNagasaki (長崎市 , Nagasaki-shi , ]) ( ) is the capital and the largest city of Nagasaki Prefecture on the island of Kyushu in Japan.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Nagasaki is the largest city of Nagasaki Prefecture, not shown to be the largest on Kyushu."
  }
 },
 {
  "aid": "c00551",
  "kind": "yes/no",
  "text": "Tweet: The numbers talking to me!",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Very short with no context; sarcasm cannot be determined."
  }
 },
 {
  "aid": "c00552",
  "kind": "yes/no",
  "text": "Post: too many dudes are wearing birks with socks on. grow up. get the fucking toes out man.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "A sincere, blunt complaint about socks with Birkenstocks; nothing signals reversed meaning."
  }
 },
 {
  "aid": "c00553",
  "kind": "yes/no",
  "text": "Claim: The 2007 FIFA U-20 World Cup was the sixteenth edition of the FIFA U-20 World Cup (formerly called FIFA World Youth Championship), hosted by Canada held from 30 June to 22 July 2007, Argentine player Sergio Aguero was given the FIFA U-20 Golden Shoe.\n\nPassages:\n\n[2007 FIFA U-20 World Cup]\nThe 2007 FIFA U-20 World Cup was the sixteenth edition of the FIFA U-20 World Cup (formerly called FIFA World Youth Championship), hosted by Canada from 30 June to 22 July 2007.\n\n[Sergio Agüero]\nSergio Leonel \"Kun\" Agüero (] ; born 2 June 1988) is an Argentine professional footballer who plays as a striker for Premier League club Manchester City and the Argentina national team.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages never mention Agüero receiving the U-20 Golden Shoe."
  }
 },
 {
  "aid": "c00554",
  "kind": "yes/no",
  "text": "Claim: Fianna Eireann is an Irish nationalist youth organization that was founded by Bulmer Hobson and an Irish political nationalist, suffragette, and politician, that was the first woman elected to the British House of Commons.\n\nPassages:\n\n[Fianna Éireann]\nNa Fianna Éireann (The Fianna of Ireland), known as the Fianna, is an Irish nationalist youth organisation founded by Bulmer Hobson and Constance Markievicz in 1909.\n\n[Constance Markievicz]\nConstance Georgine Markievicz, known as Countess Markievicz (Polish: \"Markiewicz\" ] ; née Gore-Booth; 4 February 1868 – 15 July 1927) was an Irish Sinn Féin and Fianna Fáil politician, revolutionary nationalist, suffragette and socialist. In December 1918, she was the first woman elected to the British House of Commons, though she did not take her seat and, along with the other Sinn Féin TDs, formed the first Dáil Éireann.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Markievicz co-founded Fianna, was nationalist, suffragette, politician, first woman elected to Commons."
  }
 },
 {
  "aid": "c00555",
  "kind": "yes/no",
  "text": "Claim: Mary Edna González sexuality was omnisexuality.\n\nPassages:\n\n[Pansexuality]\nPansexuality, or omnisexuality, is the sexual, romantic or emotional attraction towards people regardless of their sex or gender identity.\n\n[Mary González]\nMary Edna González (born October 30, 1983) is an American politician who serves as State Representative of House District 75 in the Texas House of Representatives.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.92
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage states González's sexuality; the claim is unsupported."
  }
 },
 {
  "aid": "c00556",
  "kind": "yes/no",
  "text": "Post: @goldfishbabe101 crispy all day every day over here ✌🏻",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.5
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Could be a sincere preference for crispy or ironic; no context settles it."
  }
 },
 {
  "aid": "c00557",
  "kind": "yes/no",
  "text": "Tweet: i would kill a man for a forehead kiss rn",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Hyperbole that sincerely expresses longing; not ironic or the reverse of its meaning."
  }
 },
 {
  "aid": "c00558",
  "kind": "yes/no",
  "text": "Claim: St Cyrpian's Anglican Church is approximately 128 mi from London.\n\nPassages:\n\n[Nottingham]\nNottingham ( ) is a city and unitary authority area in Nottinghamshire, England, 128 mi north of London, in the East Midlands.\n\n[St Cyprian's Church, Sneinton]\nSt Cyprian's Church, Sneinton is a parish church in the Church of England in Sneinton, Nottingham.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Church is in Sneinton, Nottingham, 128 mi from London; Church of England is Anglican. Supported by short chain."
  }
 },
 {
  "aid": "c00559",
  "kind": "yes/no",
  "text": "Claim: Svetha Rao, professionally known as Raja Kumari, is an Indian American songwriter, rapper and recording artist from Claremont, California, and Kumari is best known for her collaboration with notable artists including Gwen Stefani, and is a co-founder and the lead vocalist of No Doubt.\n\nPassages:\n\n[Raja Kumari]\nKumari is best known for her collaboration with notable artists including Gwen Stefani, Iggy Azalea, Fifth Harmony, Knife Party, and Fall Out Boy.\n\n[Gwen Stefani]\nShe is a co-founder and the lead vocalist of the band No Doubt that experienced major success after their breakthrough studio album \"Tragic Kingdom\" (1995) along with various successful singles, including \"Just a Girl\", \"Don't Speak\", \"Hey Baby\", and \"It's My Life\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
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
   "reason": "The passages make Gwen Stefani, not Kumari, the No Doubt co-founder, and Claremont is not supported."
  }
 },
 {
  "aid": "c00560",
  "kind": "yes/no",
  "text": "Claim: Singer Eddie Fisher, who produced the album \"I'm in the Mood for Love\" in 1952, later had a scandalous affair with the actress Elizabeth Taylor.\n\nPassages:\n\n[Eddie Fisher (singer)]\nFisher divorced his first wife, actress Debbie Reynolds, to marry Reynolds' best friend, actress Elizabeth Taylor, after Taylor's husband, film producer Mike Todd, was killed in a plane crash. The scandalous affair was widely reported, bringing unfavorable publicity to Fisher.\n\n[I'm in the Mood for Love (Eddie Fisher album)]\nI'm in the Mood for Love is the name of a 1952 album by Eddie Fisher, reissued in 1955, featuring the song of the same name.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "The album is 'by' Fisher; whether that counts as 'produced' depends on how loosely the word is read."
  }
 },
 {
  "aid": "c00561",
  "kind": "yes/no",
  "text": "Post: I get a lot of boy who cried wolf vibes from the Red Cross and their emergency blood shortages all the time",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Direct critical opinion expressed by metaphor; no saying the opposite of what is meant."
  }
 },
 {
  "aid": "c00562",
  "kind": "yes/no",
  "text": "Claim: Matthew Pettinger's birth place is on the banks of the North Saskatchewan River.\n\nPassages:\n\n[Matt Pettinger]\nMatthew Pettinger (born October 22, 1980) is a Canadian professional ice hockey left winger who is currently an unrestricted free agent who last played for the Hamburg Freezers of the Deutsche Eishockey Liga (DEL). Pettinger was born in Edmonton, Alberta and raised in Victoria, British Columbia.\n\n[Edmonton]\nEdmonton is the capital city of the Canadian province of Alberta. Edmonton is on the North Saskatchewan River and is the centre of the Edmonton Capital Region, which is surrounded by Alberta's central region.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
   "reason": "Pettinger born in Edmonton, which is on the North Saskatchewan River. Supported."
  }
 },
 {
  "aid": "c00563",
  "kind": "yes/no",
  "text": "Claim: The star of The Big Year acted in a film with martial arts expert Tom Wu. He also voiced Lightning McQueen in the \"Cars\" franchise.\n\nPassages:\n\n[Shanghai Knights]\nDirected by David Dobkin and written by Alfred Gough and Miles Millar, it stars Jackie Chan and Owen Wilson.\n\n[The Big Year]\nThe Big Year is a 2011 American comedy film directed by David Frankel, written by Howard Franklin and starring Jack Black, Steve Martin, and Owen Wilson.\n\n[Tom Wu]\nHe is a martial arts expert who has appeared in films such as \"Revolver\", \"Shanghai Knights\", \"Batman Begins\" and the Bollywood sci-fi movie \"Ra.One\".\n\n[Owen Wilson]\nHe starred with Ben Stiller in numerous films, and is known for his roles in Frat Pack comedies and as well as voicing Lightning McQueen in the \"Cars\" franchise.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Owen Wilson starred in The Big Year, appeared in Shanghai Knights with Tom Wu, voiced McQueen; all supported."
  }
 },
 {
  "aid": "c00564",
  "kind": "yes/no",
  "text": "Claim: Heidi Brunner, a Swiss opera singer, played the role as Annio in Estates Theatre in Prague.\n\nPassages:\n\n[Heidi Brunner]\nHeidi Brunner (born 1966) is a Swiss opera singer. Among the roles she sang in Vienna were Adalgisa in \"Norma\", Annio in \"La clemenza di Tito\", and the title role in \"La Cenerentola\".\n\n[La clemenza di Tito]\nThe work premiered on 6 September 1791 at the Estates Theatre in Prague.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
   "reason": "Brunner sang Annio in Vienna; nothing says at the Estates Theatre."
  }
 },
 {
  "aid": "c00565",
  "kind": "yes/no",
  "text": "Claim: The brother-in-law of Victoria Ocampo and James Norman Hall are not both authors.\n\nPassages:\n\n[Victoria Ocampo]\nHer sister, Silvina Ocampo, also a writer, was married to Adolfo Bioy Casares.\n\n[James Norman Hall]\nJames Norman Hall (22 April 1887 – 5 July 1951) was an American author best known for the novel \"Mutiny on the Bounty\" with co-author Charles Nordhoff.\n\n[Adolfo Bioy Casares]\nAdolfo Bioy Casares (] ; September 15, 1914 – March 8, 1999) was an Argentine fiction writer, journalist, and translator.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
   "reason": "Bioy Casares (brother-in-law) is a fiction writer and Hall an author, so 'not both authors' is false."
  }
 },
 {
  "aid": "c00566",
  "kind": "yes/no",
  "text": "Tweet: Keanu reeves is killing his role in ozark season 3",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.65
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "No textual cue of irony; sarcasm depends on outside knowledge Keanu is not in Ozark."
  }
 },
 {
  "aid": "c00567",
  "kind": "yes/no",
  "text": "Claim: Nassu County, which borders Queens, has a population of 778.\n\nPassages:\n\n[Hewlett-Woodmere School District]\nThe Hewlett-Woodmere Public School District, Union Free School District 14, is located in the southwest section of Nassau County, New York and borders the New York City borough of Queens.\n\n[Woodsburgh, New York]\nThe population was 778 at the 2010 census.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
   "reason": "778 is Woodsburgh's population, not Nassau County's."
  }
 },
 {
  "aid": "c00568",
  "kind": "yes/no",
  "text": "Claim: The WEC 20 opponent in the prize bout with Mike Kyle. was the lst WEC heavyweight champion before the promotion company founded in January 2001 purchased the organization.\n\nPassages:\n\n[Zuffa]\nIt was founded in January 2001 in Las Vegas, Nevada, by Station Casinos executives Frank Fertitta III and Lorenzo Fertitta to be the parent entity of the Ultimate Fighting Championship (UFC) after they purchased it from the Semaphore Entertainment Group.\n\n[WEC 20]\n\"WEC 20\"'s main event was a heavyweight bout between Brian Olsen and Mike Kyle.\n\n[Brian Olsen]\nHe was the last WEC Heavyweight Champion before it was abolished when Zuffa purchased the organization.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Olsen fought Kyle in WEC 20 main event and was last WEC heavyweight champ before Zuffa purchase."
  }
 },
 {
  "aid": "c00569",
  "kind": "yes/no",
  "text": "Claim: Snakes on a Plane (Bring It) is the debut dingle for this band. The lead vocalist of this band and Robert Plant are not both English.\n\nPassages:\n\n[Snakes on a Plane (Bring It)]\n\"Snakes on a Plane (Bring It)\", also referred to as \"Bring It (Snakes on a Plane)\", is the debut single by Cobra Starship, released in 2006 from the soundtrack album \"\".\n\n[Gabe Saporta]\nGabriel Eduardo \"Gabe\" Saporta (born October 11, 1979) is an Uruguayan-American musician and entrepreneur.\n\n[Cobra Starship]\nCobra Starship was an American dance-pop band created by former Midtown bassist and lead vocalist Gabe Saporta in 2006 in New York City, New York.\n\n[Robert Plant]\nRobert Anthony Plant, {'1': \", '2': \", '3': \", '4': \"} (born 20 August 1948) is an English singer, songwriter, and musician, best known as the lead singer and lyricist of the rock band Led Zeppelin.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Saporta is lead vocalist of Midtown per passage, Cobra Starship role implied only; nationality part holds."
  }
 },
 {
  "aid": "c00570",
  "kind": "yes/no",
  "text": "Claim: The 133d Air Refueling Squadron unit of the Air National Guard is located at a base that was host to the 509th Bomb Wing flying the General Dynamics FB-111A.\n\nPassages:\n\n[133d Air Refueling Squadron]\nThe 133d Air Refueling Squadron (133 ARS) is a unit of the New Hampshire Air National Guard 157th Air Refueling Wing located at Pease Air National Guard Base, Portsmouth, New Hampshire, United States.\n\n[Pease Air National Guard Base]\nIt occupies a portion of what was once Pease Air Force Base, a former Strategic Air Command facility with a base-related population of 10,000 and which was home to the 509th Bomb Wing (509 BW) flying the General Dynamics FB-111A.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "133 ARS is at Pease, home to 509th Bomb Wing flying FB-111A; fully supported."
  }
 },
 {
  "aid": "c00571",
  "kind": "yes/no",
  "text": "Claim: A breed the of dog was developed in New London, Wisconsin. That breed was derived before the Estonian Hound.\n\nPassages:\n\n[New London, Wisconsin]\nThe American Water Spaniel was developed as a registered breed by F. J. Pfeifer of New London.\n\n[American Water Spaniel]\nThe breed was saved by Dr. Fred J. Pfeifer, who set up the breed club and standard, and whose work led to recognition for the breed by the United Kennel Club, and later, the American Kennel Club.\n\n[Estonian Hound]\nIt was bred in 1947 when the Soviet Union's national economy ministry decided that every country in the Union must have its own dog breed.\n\n[English Water Spaniel]\nThe English Water Spaniel is a breed of dog that has been extinct since the first part of the 20th century, with the last specimen seen in the 1930s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No date for the American Water Spaniel's development, so 'before 1947' is unverified."
  }
 },
 {
  "aid": "c00572",
  "kind": "yes/no",
  "text": "Claim: The namesake of a small island in the Town of New York was born in 1599.\n\nPassages:\n\n[Lion Gardiner]\nLion Gardiner (1599–1663), an early English settler and soldier in the New World, founded the first English settlement in what became the state of New York on Long Island. His legacy includes Gardiners Island, which is held by his descendants.\n\n[Gardiners Island]\nGardiner's Island is a small island in the Town of East Hampton, New York, in Eastern Suffolk County.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Island is in the Town of East Hampton, not 'Town of New York'; garbled claim."
  }
 },
 {
  "aid": "c00573",
  "kind": "yes/no",
  "text": "Tweet: don't cry because it happened, smile because it's over &lt;3",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
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
   "verdict": "ambiguous",
   "reason": "Inverted proverb could be a bitter ironic twist or a sincere relieved message; no context settles it."
  }
 },
 {
  "aid": "c00574",
  "kind": "yes/no",
  "text": "Claim: Mark Patrick was the host of the show Hoosier Millionaire. The game the show is based on includes the sale of the lottery game offered by 44 states.\n\nPassages:\n\n[Hoosier Lottery]\nIt is a member of the Multi-State Lottery Association (MUSL).\n\n[Mark Patrick]\nPatrick also hosted the Hoosier Lottery television game show Hoosier Millionaire for 14 years.\n\n[Powerball]\nPowerball is an American lottery game offered by 44 states, the District of Columbia, Puerto Rico and the US Virgin Islands.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
   "verdict": "wrong_gold",
   "reason": "No passage links Hoosier Lottery to selling Powerball; MUSL membership alone does not establish it."
  }
 },
 {
  "aid": "c00575",
  "kind": "yes/no",
  "text": "Claim: Amelie Simone Mauresmo has won more awards than the winner of the 2015 Family Circle Cup – Singles tournament.\n\nPassages:\n\n[2015 Family Circle Cup – Singles]\nAndrea Petkovic was the defending champion, but she lost to Angelique Kerber in the semifinals.\n\n[Amélie Mauresmo]\nAmélie Simone Mauresmo ] (born 5 July 1979) is a French former professional tennis player, and a former world No. 1. Mauresmo won two Grand Slam singles titles at the Australian Open and at Wimbledon, and also won a Silver Medal at the 2004 Summer Olympics.\n\n[Angelique Kerber]\nShe ascended to the top of the rankings on 12 September 2016, thus becoming the twenty-second and oldest player to achieve the number one ranking for the first time and the first new number one player since Victoria Azarenka in 2012.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages neither name the tournament winner nor list Kerber's awards; comparison unsupported."
  }
 },
 {
  "aid": "c00576",
  "kind": "yes/no",
  "text": "Claim: A member team of the 2009 Big East Conference football season played and won on on December 19. In this game played the future Atlanta Falcons wide receiver Mohamed Sanu Sr was the game's MVP.\n\nPassages:\n\n[2009 St. Petersburg Bowl]\nThe 2009 St. Petersburg Bowl presented by Beef 'O' Brady's, formerly known as the St. Petersburg Bowl, was the second edition of the college football bowl game and was played at Tropicana Field in St. Petersburg, Florida. Rutgers defeated UCF 45–24 in a game where Mohamed Sanu, the game's MVP, caught 4 passes for 97 yards and a touchdown in addition to rushing 14 times for 47 yards and two touchdowns.\n\n[2009 Rutgers Scarlet Knights football team]\nThe Scarlet Knights finished the season 9–4, 3–4 in Big East play and won the St. Petersburg Bowl, 45–24, over UCF.\n\n[Mohamed Sanu]\nMohamed Sanu Sr. (born August 22, 1989) is an American football wide receiver for the Atlanta Falcons of the National Football League (NFL).\n\n[2009 Big East Conference football season]\nThe Big East Conference consists of 8 football members: Cincinnati, Connecticut, Louisville, Pittsburgh, Rutgers, South Florida, Syracuse, and West Virginia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
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
   "reason": "The December 19 date of the bowl game is not in the passages."
  }
 },
 {
  "aid": "c00577",
  "kind": "yes/no",
  "text": "Claim: Multinational Monitor has fewer issues each month than In These Times does.\n\nPassages:\n\n[Multinational Monitor]\nThe Multinational Monitor was a bimonthly magazine founded by Ralph Nader in 1980.\n\n[In These Times]\nIn These Times is an American politically progressive/democratic socialist monthly magazine of news and opinion published in Chicago, Illinois.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
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
   "reason": "'Bimonthly' can mean every two months or twice a month, so comparison is unsettled."
  }
 },
 {
  "aid": "c00578",
  "kind": "yes/no",
  "text": "Claim: This music channel regularly shows the UK R&B Singles and Albums Charts. The media conglomerate owner of this channel (UK and Ireland) changed it's name in 2004. Their new acronym stand for Gesellschaft mit beschränkter Haftung.\n\nPassages:\n\n[Gesellschaft mit beschränkter Haftung]\nA Gesellschaft mit beschränkter Haftung (] , abbreviated GmbH ] and also GesmbH in Austria) is a type of legal entity very common in Germany, Austria, Switzerland (where it is equivalent to a S.à r.l.) and Liechtenstein.\n\n[UK R&amp;B Singles and Albums Charts]\nThe UK R&B chart is also shown regularly on music channels including Kiss, Viva UK, MTV Base and MTV Hits.\n\n[Viva (UK and Ireland)]\nViva (stylised as VIVA) is a music television channel in the United Kingdom and Ireland, owned by VIVA Media and thereby Viacom International Media Networks Europe.\n\n[VIVA Media]\nVIVA Media GmbH (until 2004 \"VIVA Media AG\") is a music television network originating from Germany.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Viva shows the R&B chart, its owner VIVA Media became GmbH in 2004, and GmbH is defined; all parts supported."
  }
 },
 {
  "aid": "c00579",
  "kind": "yes/no",
  "text": "Claim: \"The Closer I Get to You\" is a romantic ballad performed by African American blues, soul, R&B, and folk artist-songwriter Roberta Flack, and Donny Hathaway, an American jazz, blues, soul and gospel singer, songwriter, arranger and pianist that signed with Atlantic Records in 1969.\n\nPassages:\n\n[The Closer I Get to You]\n\"The Closer I Get to You\" is a romantic ballad performed by African American jazz, soul, R&B, and folk singer-songwriter Roberta Flack and African American soul musician Donny Hathaway.\n\n[Donny Hathaway]\nDonny Edward Hathaway (October 1, 1945 – January 13, 1979) was an American jazz, blues, soul and gospel singer, songwriter, arranger and pianist.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
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
   "reason": "Passages call Flack jazz not blues, and Hathaway signing with Atlantic in 1969 is never stated."
  }
 },
 {
  "aid": "c00580",
  "kind": "yes/no",
  "text": "Tweet: bought some index cards and a 3 ring binder the other day just so i could feel alive",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "'Just so i could feel alive' could be ironic self-mockery or sincere quirky delight."
  }
 },
 {
  "aid": "c00581",
  "kind": "yes/no",
  "text": "Claim: This airport in in south-east England ranks as the 8th busiest airport in Europe and replaced the airport where the 1921 SNETA Farman Goliath ditching first took off. It is next to the suburb of Earlswood.\n\nPassages:\n\n[Gatwick Airport]\nGatwick Airport (also known as London Gatwick) (IATA: LGW, ICAO: EGKK) is a major international airport in south-east England, 29.5 mi south of Central London and 2.7 NM north of Crawley. Gatwick is the eighth-busiest airport in Europe.\n\n[1921 SNETA Farman Goliath ditching]\nThe aircraft was operating a mail flight from Croydon Airport, United Kingdom to Brussels-Evere Airport, Belgium.\n\n[Earlswood]\nEarlswood lies on the A23 between Redhill (in the direction of London) and Horley (next to Gatwick Airport), from which the neighbouring community, Whitebushes is separated by a wide rural buffer zone.\n\n[Croydon Airport]\nCroydon Airport (ICAO: EGCR ) was an airport in South London, England. It was the main airport for London before it was replaced by Northolt Aerodrome, London Heathrow Airport and Gatwick Airport.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Passages place Horley, not Earlswood, next to Gatwick; Earlswood adjacency unsupported."
  }
 },
 {
  "aid": "c00582",
  "kind": "yes/no",
  "text": "Claim: Widewuto, a legendary ruler of the pagan Prussians, was believed to have existed before the army of the Teutonic Knights launched crusade against the Prussian peoples.\n\nPassages:\n\n[Widewuto]\nWidewuto (also \"Viduutus\", \"Vidvutus\", \"Witowudi\", \"Waidewut\") was a legendary king of the pagan Prussians who ruled along with his elder brother, the high priest Bruteno in the 6th century AD. It is unclear whether the legend was authentically Prussian (i.e. recorded from Prussian mythology) or was created by Grunau (possibly inspired by Biblical Moses and Aaron), though Lithuanian researchers tend to support in its authenticity.\n\n[Prussian mythology]\nThe Prussian mythology was a polytheistic religion of the Old Prussians, indigenous peoples of Prussia before the Prussian Crusade waged by the Teutonic Knights. No sources document pagan religion before the forced Christianization in the 13th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Widewuto is a legendary 6th-century ruler, and the crusade came in the 13th century, so the claim is supported."
  }
 },
 {
  "aid": "c00583",
  "kind": "yes/no",
  "text": "Claim: Keith County in an American state is located over the 174000 the High Plains. This area supplies water to the Texas High Plains AVA. Sherman Elementary School is located in this state.\n\nPassages:\n\n[Ogallala, Nebraska]\nOgallala is a city in Keith County, Nebraska, United States.\n\n[Texas High Plains AVA]\nThe Texas plains can be extremely dry, so most vineyards are irrigated with water from the Ogallala Aquifer.\n\n[Sherman Elementary School]\nSherman Elementary School is located at 5618 North 14th Avenue in East Omaha, Nebraska, United States.\n\n[Ogallala Aquifer]\nThe Ogallala Aquifer is a shallow water table aquifer surrounded by sand, silt, clay and gravel located beneath the Great Plains in the United States.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Keith County lying over the aquifer is not stated."
  }
 },
 {
  "aid": "c00584",
  "kind": "yes/no",
  "text": "Claim: One of the senators that proposed the Patient Freedom Act of 2017 replaced a Louisiana's senior senator in 2017. That replaced senator is an Republican lobbyist, lawyer and politician who once defeated by Bel Edwards.\n\nPassages:\n\n[Patient Freedom Act of 2017]\nThe Patient Freedom Act of 2017 was a United States healthcare plan proposed by senators Susan Collins (Maine) and Bill Cassidy (La.) on January 23, 2017, to replace the Affordable Care Act.\n\n[David Vitter]\nDavid Bruce Vitter (born May 3, 1961) is an American lobbyist, lawyer and politician who served as United States Senator for Louisiana from 2005 to 2017.\n\n[Bill Cassidy]\nCassidy became Louisiana's senior senator when David Vitter retired in 2017.\n\n[Louisiana lieutenant gubernatorial election, 2015]\nBilly Nungesser won the election defeating Kip Holden, despite a Democratic victory in the gubernatorial election, in which John Bel Edwards defeated David Vitter by a similar margin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.65
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Vitter's Republican affiliation is not stated, and Cassidy became senior senator rather than replacing Vitter."
  }
 },
 {
  "aid": "c00585",
  "kind": "yes/no",
  "text": "Post: WHO LET THE LAUNDRY PILE UP 5 BASKETS. Goodness.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "Feigned outrage over own laundry could be mock-exasperation or a literal complaint."
  }
 },
 {
  "aid": "c00586",
  "kind": "yes/no",
  "text": "Claim: Trouble Along the Way was directed by Michael Curtiz and produced by Harold Brent Wallis. Harold Brent Wallis also produced a 1942 film that starred the Dead End (1937 film).\n\nPassages:\n\n[Hal B. Wallis]\nHarold Brent Wallis (born Aaron Blum Wolowicz; October 19, 1898 – October 5, 1986) was an American film producer. He is best remembered for producing \"Casablanca\" (1942) and \"True Grit\" (1969), along with many other major films for Warner Bros. featuring such film stars as Humphrey Bogart, Bette Davis, and Errol Flynn.\n\n[Trouble Along the Way]\nThe movie was directed by Michael Curtiz, director of \"Casablanca\".\n\n[Dead End (1937 film)]\nIt stars Humphrey Bogart, Joel McCrea, and Sylvia Sidney.\n\n[Humphrey Bogart]\nHumphrey DeForest Bogart ( ; December 25, 1899January 14, 1957) was an American screen and stage actor whose performances in 1940s films noir such as \"The Maltese Falcon\", \"Casablanca\", and \"The Big Sleep\" earned him status as a cultural icon.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
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
   "verdict": "wrong_gold",
   "reason": "No passage says Wallis produced Trouble Along the Way."
  }
 },
 {
  "aid": "c00587",
  "kind": "yes/no",
  "text": "Claim: The first major improved highway is located in Wheeling, West Virginia.\n\nPassages:\n\n[Mount Echo, West Virginia]\nMount Echo is an unincorporated community in Ohio County, West Virginia, United States. It is part of the Wheeling, West Virginia Metropolitan Statistical Area.\n\n[National Road]\nThe National Road (also known as the Cumberland Road) was the first major improved highway in the United States built by the federal government.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Nothing places the National Road in Wheeling, West Virginia."
  }
 },
 {
  "aid": "c00588",
  "kind": "yes/no",
  "text": "Text: Petition to call erections social dickstanding",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.65
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "A pun joke, perhaps mocking social distancing; unclear that the meaning differs from literal."
  }
 },
 {
  "aid": "c00589",
  "kind": "yes/no",
  "text": "Claim: The show, for which Larry D. Mann voiced the character of Yukon Cornelius, aired earlier than this show. Linus and Lucy is a jazz piece from this show.\n\nPassages:\n\n[Rudolph the Red-Nosed Reindeer (TV special)]\nRudolph the Red-Nosed Reindeer is a 1964 Christmas stop motion animated television special produced by Rankin/Bass Productions and currently distributed by Universal Television. It first aired Sunday, December 6, 1964, on the NBC television network in the United States, and was sponsored by General Electric under the umbrella title of \"The General Electric Fantasy Hour\". The special was based on the Johnny Marks song \"Rudolph the Red-Nosed Reindeer\" which was itself based on the poem of the same name written in 1939 by Marks' brother-in-law, Robert L. May.\n\n[Larry D. Mann]\nHe was best known as \"The Boss\" in a series of Bell Canada television commercials in the 1980s and for voicing the character of Yukon Cornelius in \"Rudolph the Red-Nosed Reindeer\".\n\n[Linus and Lucy]\nSince that special, the piece has introduced most of the \"Peanuts\" TV cartoons, with the exceptions of the specials and other TV programs produced between 1979 and 1992.\n\n[A Charlie Brown Christmas]\nProduced by Lee Mendelson and directed by Bill Melendez, the program made its debut on CBS on December 9, 1965.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "The dates are supported, but no passage ties Linus and Lucy to A Charlie Brown Christmas ('that special' is never named)."
  }
 },
 {
  "aid": "c00590",
  "kind": "yes/no",
  "text": "Claim: \"I Do\" the song by Filipino singer Nina and described to be Mariah Carey-like was on third studio album, \"Nina\".\n\nPassages:\n\n[Mariah Carey]\nMariah Carey (born March 27, 1969 or 1970) is an American singer, songwriter, record producer, and actress.\n\n[I Do (Nina Girado song)]\n\"I Do\" is a song by Filipino singer Nina from her self-titled third studio album, \"Nina\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
   "reason": "The 'Mariah Carey-like' description is not in the passages."
  }
 },
 {
  "aid": "c00591",
  "kind": "yes/no",
  "text": "Claim: The opponent of Crawford Ashley for the World Boxing Association (WBA) World super middleweight title won a silver Olympic medal in 1984.\n\nPassages:\n\n[Virgil Hill]\nAs an amateur, Hill won a silver medal in the middleweight division at the 1984 Summer Olympics.\n\n[Crawford Ashley]\nCrawford \"Chilling\" Ashley (born Gary Crawford, 20 May 1964 in Leeds is an English professional super middle/light heavy/cruiser/heavyweight boxer of the 1980s, '90s and 2000s, who won the British Boxing Board of Control (BBBofC) Central Area light heavyweight title, BBBofC British light heavyweight title, European Boxing Union (EBU) light heavyweight title (twice), and Commonwealth light heavyweight title (twice), drew with Yawe Davis for the vacant European Boxing Union (EBU) light heavyweight title, and was a challenger for the European Boxing Union (EBU) light heavyweight title against Graciano Rocchigiani, World Boxing Association (WBA) World super middleweight title against Michael Nunn, World Boxing Association (WBA) World light heavyweight title against Virgil Hill, and World Boxing Union (WBU) cruiserweight title against Sebastiaan Rothmann, his professional fighting weight varied from 163 lb , i.e. super middleweight to 211 lb , i.e. heavyweight.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
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
   "reason": "Ashley's WBA super middleweight opponent was Nunn; Hill was the light heavyweight opponent."
  }
 },
 {
  "aid": "c00592",
  "kind": "yes/no",
  "text": "Claim: During the Cold War (1947–91) the Russia-United Kingdom relations in a position of rivalry after the abdication of Emperor Nicholas II.\n\nPassages:\n\n[Russia–United Kingdom relations]\nThey were allies again in World Wars I and II, although relations were strained by the Russian Revolution of 1917. They were at sword's point during the Cold War (1947–91).\n\n[Russian Revolution]\nThe Russian Empire collapsed with the abdication of Emperor Nicholas II and the old regime was replaced by a provisional government during the first revolution of February 1917 (March in the Gregorian calendar; the older Julian calendar was in use in Russia at the time).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "'At sword's point during the Cold War' supports rivalry, and the Cold War came after the 1917 abdication."
  }
 },
 {
  "aid": "c00593",
  "kind": "yes/no",
  "text": "Claim: Section.80 is an album. It succeeded Kendrick Lamar's album that had the song produced by the same producer as Research (Big Sean song) on it.\n\nPassages:\n\n[Research (Big Sean song)]\nIt was written by Sean, Grande, Dacoury Natchel, Michael Carlson, and Leland Wayne, and was produced by DJ Dahi and Metro Boomin.\n\n[DJ Dahi]\nDahi is perhaps best known for producing \"Worst Behavior\" by Canadian rapper Drake, as well as American rapper Kendrick Lamar's critically acclaimed album cut \"Money Trees\", which features Lamar's label-mate Jay Rock.\n\n[Good Kid, M.A.A.D City]\nGood Kid, M.A.A.D City (stylized as good kid, m.A.A.d city) is the second studio album by American rapper Kendrick Lamar. It was preceded by the release of Kendrick's debut studio album \"Section.80\" (2011), released exclusively through the iTunes Store as an independent album.\n\n[Money Trees]\n\"Money Trees\" is a song by American hip hop recording artist Kendrick Lamar, taken from his major label debut studio album \"Good Kid, M.A.A.D City\" (2012).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "Section.80 preceded Good Kid, M.A.A.D City; the claim says it succeeded it, which is reversed."
  }
 },
 {
  "aid": "c00594",
  "kind": "yes/no",
  "text": "Claim: Blake Alexander Carrington is a fictional character on the ABC television series \"Dynasty\", created by Richard and Esther Shapiro whose role was portrayed by John Forsythe, and also appeared as a guest on several talk and variety shows and as a panelist on quiz formatted game shows.\n\nPassages:\n\n[John Forsythe]\nHe also appeared as a guest on several talk and variety shows and as a panelist on numerous game shows.\n\n[Blake Carrington]\nBlake Alexander Carrington is a fictional character on the ABC television series \"Dynasty\", created by Richard and Esther Shapiro. The role was portrayed by John Forsythe from the first episode of the series in 1981 until its finale in 1989.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
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
   "reason": "Mostly supported; 'quiz formatted' game shows adds a detail the passage does not state."
  }
 },
 {
  "aid": "c00595",
  "kind": "yes/no",
  "text": "Claim: Rennae Stubs who teamed up with Elena Bovina for the 2003 Family Circle Cup – Doubles. Her and Renáta Tomanová were both tennis players\n\nPassages:\n\n[Renáta Tomanová]\nRenáta Tomanová (born 9 December 1954) is a former professional tennis player from Czechoslovakia.\n\n[2003 Family Circle Cup – Doubles]\nLisa Raymond and Rennae Stubbs were the defending champions, but Raymond did not compete in this edition.\n\n[Rennae Stubbs]\nRennae Stubbs (born 26 March 1971) is an Australian retired tennis player.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "wrong_gold",
   "reason": "No passage says Stubbs partnered Elena Bovina at the 2003 event."
  }
 },
 {
  "aid": "c00596",
  "kind": "yes/no",
  "text": "Post: Is it unreasonable to spend £50 on a bonsai tree? Asking for a friend 🤔",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
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
   "verdict": "ambiguous",
   "reason": "'Asking for a friend' is a joking trope, but the question itself may be sincere."
  }
 },
 {
  "aid": "c00597",
  "kind": "yes/no",
  "text": "Claim: A news publication, which named a woman in its list of top global tinkers, was founded in 1970. The woman translated \"Time for Outrage!\" into English.\n\nPassages:\n\n[Time for Outrage!]\nby the French diplomat, member of the French Resistance and concentration camp survivor Stéphane Hessel.\n\n[Foreign Policy]\nForeign Policy is an American news publication, founded in 1970 and focused on global affairs, current events, and domestic and international policy.\n\n[Stéphane Hessel]\nIn 2011 he was named by \"Foreign Policy\" magazine in its list of top global thinkers.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
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
   "reason": "Hessel is the male author, not a woman translator; translation into English is unsupported."
  }
 },
 {
  "aid": "c00598",
  "kind": "yes/no",
  "text": "Claim: The end of the lengthy reign of the Queen for whom the TV series \"Reign\" is based on was in 24 July 1567.\n\nPassages:\n\n[Mary, Queen of Scots]\nMary, Queen of Scots (8 December 1542 – 8 February 1587), also known as Mary Stuart or Mary I, reigned over Scotland from 14 December 1542 to 24 July 1567.\n\n[Reign (season 1)]\nThe series follows the early exploits of Mary, Queen of Scots, and was created by Stephanie SenGupta and Laurie McCarthy.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
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
   "reason": "Reign follows Mary, whose reign ended on 24 July 1567; the claim is fully supported."
  }
 },
 {
  "aid": "c00599",
  "kind": "yes/no",
  "text": "Tweet: Just at work listening to podcasts while unloading soda syrup boxes like the cultured blue collar worker I am.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  },
  "first_pass": {
   "verdict": "ambiguous",
   "reason": "'Cultured blue collar worker' may be self-ironic or sincere humorous pride."
  }
 }
]
