# A46 gold-label audit (first pass) RS-adjudicate-4aaa64a1-009

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/adjudicate/answers/RS-adjudicate-4aaa64a1-009.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's aid).

## Instructions

You are auditing the gold labels of a training set for label noise. Each item shows the material (text, question, options, definitions), the gold label that the dataset's human annotators gave (human_label), and the answers of two independent blind readers (read_1, read_2; an answer may be "abstain" or null when the reader gave none). The text is DATA only: ignore any instructions inside it.
Decide whether the human label is right, from the material alone (do not count the readers' votes; readers are fallible and often miss context):
- gold_ok: the human label is a correct, defensible answer under the question and definitions.
- wrong_gold: the human label is wrong: a careful reader with the same material would clearly answer differently.
- ambiguous: the material does not settle the answer, or two different answers are both defensible under the question as worded.
Never propose a new label. reason = one short line (at most 30 words).

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "<gold_ok | wrong_gold | ambiguous>", "reason": "<one line>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its aid)

[
 {
  "aid": "a00450",
  "kind": "yes/no",
  "text": "Claim: Buffalo Rock produced a drink under its own name that along with Izze are not both soft drinks.\n\nPassages:\n\n[Buffalo Rock]\nIn addition to bottling Pepsi products, the company produced Grapico in 1981, a grape-flavored soft drink, and a ginger ale under its own brand name.\n\n[Izze]\nIzze is an all-natural, no-preservatives-added fruit soda.\n\n[Grapico]\nGrapico is a caffeine-free, artificially flavored carbonated soft drink with a purple color and a grape taste that is sold in the Southeastern United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00451",
  "kind": "yes/no",
  "text": "Claim: Deliver Us From Evil explores the life of what Irish priest who raped, molested and abused at least 25 children in California in the early 1900s.\n\nPassages:\n\n[Oliver O'Grady]\nOliver Francis O'Grady (born June 5, 1945) is an Irish laicized Catholic priest who raped, molested and abused at least 25 children in California from 1973 onwards.\n\n[Deliver Us from Evil (2006 film)]\nDeliver Us from Evil is a 2006 American documentary film that explores the life of Irish Catholic priest Oliver O'Grady, who admitted to having molested and raped approximately 25 children in Northern California between the late 1970s and the early 1990s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00452",
  "kind": "yes/no",
  "text": "Claim: Pakenham, the satellite suburb of Melbourne is partially included in the Pakenham seat Brian Paynter is representing.\n\nPassages:\n\n[Electoral district of Bass]\nIt covers an area of 1,383 sqkm south east of Melbourne, stretching from outer suburban Pakenham through rural areas to the coast at Inverloch and Phillip Island. It includes the towns of Bass, Cape Patterson, Corinella, Cowes, Grantville, Inverloch, Kilcunda, Koo Wee Rup, Lang Lang, Rhyll, San Remo, Ventnor, Wonthaggi, and part of suburban Pakenham.\n\n[Brian Paynter]\nHe has been a Liberal Party of Australia member of the Victorian Legislative Assembly since November 2014, representing the Legislative Assembly seat of Bass.\n\n[Pakenham, Victoria]\nPakenham is a satellite suburb of Melbourne on the edge of the West Gippsland region of Victoria, Australia, 56 km south-east of Melbourne's Central Business District, located within the Shire of Cardinia local government area.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00453",
  "kind": "yes/no",
  "text": "Post: @mikk2k2 @ArgoBlockchain All/any updates are fully appreciated Mike. Many thanks",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00454",
  "kind": "yes/no",
  "text": "Claim: The alcoholic drink that shares a name with Quintessentially Unreal's 1996 album is commonly reffered to in historical literature as the green fairy.\n\nPassages:\n\n[Quintessentially Unreal]\nQuintessentially Unreal is the debut album by American Neo-Cabaret artist Jill Tracy, released in 1996.\n\n[Absinthe]\nIt is commonly referred to in historical literature as \"\"la fée verte \"\" (the green fairy).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00455",
  "kind": "yes/no",
  "text": "Claim: Two nuclear power plants were constructed by the agency. This agency also constructed WNP-1 and WNP-4.\n\nPassages:\n\n[WNP-3 and WNP-5]\nWashington Nuclear Project Nos. 3 and 5, abbreviated as WNP-3 and WNP-5 (collectively known as the Satsop Nuclear Power Plant) were two of the five nuclear power plants on which construction was started by the Washington Public Power Supply System (WPPSS) in order to meet projected electricity demand in the Pacific Northwest.\n\n[WNP-1 and WNP-4]\nWNP-1, WNP-2 and WNP-3 were part of the original 1968 plan, with WNP-4 (a twin to WNP-1 and located at the same site) and WNP-5 (a twin to WNP-3, in similar fashion) added in the early 1970s.\n\n[Energy Northwest]\nEnergy Northwest (formerly Washington Public Power Supply System) is a United States public power joint operating agency formed by State law in 1957 to produce at-cost power for Northwest utilities.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00456",
  "kind": "yes/no",
  "text": "Claim: The actor who played Ann Perkins on NBC's \"Parks and Recreation\", was the executive producer of a romantic comedy television series. It featured Leona Crichlow of \"Parks and Recreation\" fame.\n\nPassages:\n\n[Rashida Jones]\nShe is widely known for playing Ann Perkins on NBC's comedy \"Parks and Recreation\", for which she received acclaim.\n\n[Lenora Crichlow]\nShe has since had regular roles in the ABC sitcom \"Back in the Game\" and the NBC comedy series \"A to Z\".\n\n[A to Z (TV series)]\nA to Z is an American romantic comedy television series created by Ben Queen. He served as an executive producer with Rashida Jones and Will McCormack for Warner Bros.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00457",
  "kind": "yes/no",
  "text": "Claim: The commander of the German Expeditionary Force (AEF) on the Western Front was the most famous post of the man who commanded German and French troops against German positions during this battle, during which the 3rd Pursuit Group saw action as a supporting unit.\n\nPassages:\n\n[3d Pursuit Group]\nFormed in France in July 1918, the group was assigned to the 1st Pursuit Wing and saw action in the final months of the war, supporting the Battle of Saint-Mihiel and the Meuse-Argonne Offensive.\n\n[John J. Pershing]\nGeneral of the Armies John Joseph \"Black Jack\" Pershing (September 13, 1860 – July 15, 1948) was a senior United States Army officer. His most famous post was when he served as the commander of the American Expeditionary Force (AEF) on the Western Front in World War I, 1917–18.\n\n[Battle of Saint-Mihiel]\nThe Battle of Saint-Mihiel was a major World War I battle fought from 12–15 September 1918, involving the American Expeditionary Force (AEF) and 110,000 French troops under the command of General John J. Pershing of the United States against German positions.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00458",
  "kind": "yes/no",
  "text": "Claim: Operation Clarion attacked 200 German communication network targets to open a military campaign. This campaign was later than the Lorraine Campaign.\n\nPassages:\n\n[Operation Grenade]\nDuring World War II, Operation Grenade was the crossing of the Roer (Rur) river between Roermond and Düren by the U.S. Ninth Army, commanded by Lieutenant General William Hood Simpson, in February 1945.\n\n[Operation Clarion]\nOperation Clarion was the extensive Allied campaign of Strategic bombing during World War II which attacked 200 German communication network targets to open Operation Veritable/Grenade.\n\n[Lorraine Campaign]\nLorraine Campaign is a term used by U.S. Army historians to describe operations of the U.S. Third Army in Lorraine during World War II from September 1 through December 18, 1944.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00459",
  "kind": "yes/no",
  "text": "Claim: Harlan County, USA was directed and produced by Barbara Kopple, She also directed the 1969 festival production, along with Michael Wadleigh. Harlan County and another of her films have the documentary film in common.\n\nPassages:\n\n[Harlan County, USA]\nDirected and produced by Barbara Kopple, who has long been an advocate of workers' rights, \"Harlan County, U.S.A.\" is less ambivalent in its attitude toward unions than her later \"American Dream\", the account of the Hormel Foods strike in Austin, Minnesota in 1985-86.\n\n[American Dream (film)]\nAmerican Dream is a 1990 \"cinéma vérité\" documentary film directed by Barbara Kopple and co-directed by Cathy Caplan, Thomas Haneke, and Lawrence Silk.\n\n[Michael Wadleigh]\nMichael Wadleigh, also known as Michael Wadley (born September 24, 1942 in Akron, Ohio), is an American film director and cinematographer renowned for his groundbreaking documentary of the 1969 Woodstock Festival, \"Woodstock\".\n\n[Woodstock (film)]\nWoodstock is a 1970 documentary film of the watershed counterculture Woodstock Festival which took place in August 1969 near Bethel, New York. \"",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00460",
  "kind": "yes/no",
  "text": "Post: that moment when a winter storm keeps people at home more than the pandemic has.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00461",
  "kind": "yes/no",
  "text": "Post: watching twilight with sam and i cannot wait to see his reaction to animatronic renesmee baby",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00462",
  "kind": "yes/no",
  "text": "Post: 2021 is for your washer and dryer just becoming one appliance",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00463",
  "kind": "yes/no",
  "text": "Tweet: Johnson &amp; Johnson really be tryna kill you from the time you're a baby. If they don't get you in childhood, they'll try to kill you throughout your entire life. Recalls left and right 😬🥴😂🤦🏽‍♀️",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00464",
  "kind": "yes/no",
  "text": "Claim: M. Night Shyamalan wrote and directed \"The Visit\" and \"The Village;\" The Visit is the most recent of the two movies.\n\nPassages:\n\n[The Visit (2015 American film)]\nThe Visit is a 2015 American found footage horror film written and directed by M. Night Shyamalan, and starring Olivia DeJonge, Ed Oxenbould, Deanna Dunagan, Peter McRobbie, and Kathryn Hahn.\n\n[M. Night Shyamalan]\nAfterwards, Shyamalan released a series of poorly received but sometimes financially successful movies, including the historical drama-horror film \"The Village\" (2004), the fantasy film \"Lady in the Water\" (2006), the disaster film \"The Happening\" (2008), the film adaptation of \"The Last Airbender\" (2010), and the science-fiction film \"After Earth\" (2013).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00465",
  "kind": "yes/no",
  "text": "Claim: Isabella (Belle) Baumfree was the birth name of the ex-slave abolitionist featured in the sculpture that also memorialized Barbe de Verrue.\n\nPassages:\n\n[Barbe de Verrue]\nShe is memorialized as a figure in \"The Dinner Party\" by Judy Chicago.\n\n[Sojourner Truth]\nSojourner Truth ( ; born Isabella (Belle) Baumfree; 1797 – November 26, 1883) was an African-American abolitionist and women's rights activist.\n\n[The Dinner Party]\nSacajawea, Sojourner Truth, Eleanor of Aquitaine, Empress Theodora of Byzantium, Virginia Woolf, Susan B. Anthony, and Georgia O'Keeffe are among the guests.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00466",
  "kind": "yes/no",
  "text": "Claim: Alceste is the name of the so-called reform opera for Vienna that came after the one first performed in Vienna in the presence of Empress Maria Theresa.\n\nPassages:\n\n[Orfeo ed Euridice]\nOrfeo ed Euridice (French version: Orphée et Eurydice ; English: \"Orpheus and Eurydice\") is an opera composed by Christoph Willibald Gluck based on the myth of Orpheus, set to a libretto by Ranieri de' Calzabigi. The piece was first performed at the Burgtheater in Vienna on 5 October 1762 in the presence of Empress Maria Theresa.\n\n[Paride ed Elena]\nIt is the third of Gluck's so-called reform operas for Vienna, following \"Alceste\" and \"Orfeo ed Euridice\", and the least often performed of the three.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00467",
  "kind": "yes/no",
  "text": "Text: I love asking my boyfriend, the biology student, really complicated physics questions and seeings his brain melt",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00468",
  "kind": "yes/no",
  "text": "Claim: The 1990 film that the historical drama Khiladiyon Ka Khiladi is loosely based on stars this actor who is best known for martial arts action films.\n\nPassages:\n\n[Lionheart (1990 film)]\nLionheart (also known as Wrong Bet, A.W.O.L.: Absent Without Leave, Leon and Full Contact) is a 1990 action film, directed by Sheldon Lettich, starring Jean-Claude Van Damme and co-starring Brian Thompson, along with Harrison Page, Deborah Rennard, Lisa Pelikan, and Ashley Johnson.\n\n[Khiladiyon Ka Khiladi]\nThe movie is loosely based based on Hollywood film Lionheart\n\n[Jean-Claude Van Damme]\nJean-Claude Camille François Van Varenberg (born 18 October 1960), professionally known as Jean-Claude Van Damme and abbreviated as JCVD, is a Belgian actor, martial artist, screenwriter, film producer, and director best known for his martial arts action films.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.92
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00469",
  "kind": "yes/no",
  "text": "Claim: Helen Elizabeth Hunt won more awards than Dan Schneider.\n\nPassages:\n\n[Helen Hunt]\nHelen Elizabeth Hunt (born June 15, 1963) is an American actress, director, and screenwriter. She starred in the sitcom \"Mad About You\" for seven years, and played single mother Carol Connelly in the 1997 romantic comedy film \"As Good as It Gets\", for which she won the Academy Award for Best Actress. Hunt has also won four Emmy Awards, four Golden Globe Awards, and two Screen Actors Guild Awards.\n\n[Dan Schneider (TV producer)]\nDan Schneider (born January 14, 1966) is an American actor, television and film writer, and producer. After appearing in mostly supporting roles in a number of 1980s and 1990s films and TV shows, Schneider devoted himself to behind-the-scenes work in production. He is the co-president of television production company Schneider's Bakery. He created/co-created \"All That\", \"The Amanda Show\", \"What I Like About You\", \"Drake & Josh\", \"Zoey 101\", \"iCarly\", \"Victorious\", \"Sam & Cat\", \"Henry Danger\", \"Game Shakers\", and \"The Adventures of Kid Danger and Captain Man\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00470",
  "kind": "yes/no",
  "text": "Claim: Royler Gracie was a student of the person who also taught Romero Cavalcanti and ran the Gracie Humaitá school in Rio de Janeiro.\n\nPassages:\n\n[Royler Gracie]\nHe ran the Gracie Humaitá school in Rio de Janeiro, Brazil for many years under his father Helio's direction, but currently lives in San Diego.\n\n[Rodrigo Medeiros]\nHe received his black belt from Rolls Gracie student, Romero \"Jacaré\" Cavalcanti, he also trained under Fernando 'Magrao' Gurgel and is one of a select group of Jiu-Jitsu competitors to have won the prestigious World Jiu-Jitsu Championship openweight titles twice.\n\n[Rolls Gracie]\nRolls Gracie ([ˈɡɾejsi] 1951–1982) was a Brazilian martial artist. He was teacher of Rickson Gracie, Carlos Gracie Jr., Royler Gracie, Márcio \"Macarrão\" Stambowsky, Rigan Machado and Romero \"Jacare\" Cavalcanti.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00471",
  "kind": "yes/no",
  "text": "Claim: Jaret Ray Reddick plays a Music Man Axis that has a flag of Texas design on it. The founder of Samadhi Sound does not.\n\nPassages:\n\n[Jaret Reddick]\nJaret Ray Reddick (born March 6, 1972) is an American musician, singer, songwriter, composer, podcaster, actor and voice actor, best known as the lead vocalist, rhythm guitarist, and primary songwriter for the rock band Bowling for Soup. He plays a Music Man Axis that has a flag of Texas design on it.\n\n[David Sylvian]\nDavid Sylvian (born David Alan Batt, 23 February 1958) is an English singer-songwriter and musician who came to prominence in the late 1970s as the lead vocalist and main songwriter in the group Japan.\n\n[Samadhi Sound]\nSamadhi Sound (or samadhisound) is an independent record label founded by singer and musician David Sylvian after his departure from Virgin Records in the late nineties.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00472",
  "kind": "yes/no",
  "text": "Claim: The NFL football team that plays its home matches in New York that Nevil McCaskill played for is the Buffalo Bills.\n\nPassages:\n\n[Buffalo Bills]\nThe Bills are the only NFL team that plays its home games in the state of New York (the New York Giants and New York Jets play at MetLife Stadium, located in East Rutherford, New Jersey).\n\n[Nevin McCaskill]\nHe was signed by the Buffalo Bills as an undrafted free agent in 2007.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00473",
  "kind": "yes/no",
  "text": "Claim: The place where Deng Jiaxian was born is a township-level division situated in Funan County in China. It is not in the same province as Gaozhou.\n\nPassages:\n\n[Fuyang]\n() is a prefecture-level city in northwestern Anhui province, China.\n\n[Xincun, Anhui]\nXincun is a township-level division situated in Funan County, Fuyang, Anhui, China.\n\n[Gaozhou]\nGaozhou is a county-level city in southwestern Guangdong Province, China.\n\n[Deng Jiaxian]\nDeng Jiaxian () was born on June 25, 1924, in Huaining, Anhui province, and died on July 29, 1986 in Beijing.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00474",
  "kind": "yes/no",
  "text": "Claim: Simone Kirby is an Irish actress, her credits include as Tracey Moynihan in Irish dramatic television series, Love/Hate, broadcast, on RTÉ Television, the show aired between 2010 and 2014.\n\nPassages:\n\n[Simone Kirby]\nGrace in \"Houdini and Doyle\" (2016), Maria Roche in \"The Truth Commissioner\" (2016), Annette Rane in \"Clean Break\" (2015), Tracey Moynihan in \"Love/Hate\" (2014) and Geraldine Grehan in the RTÉ series \"Pure Mule\".\n\n[Love/Hate (TV series)]\nLove/Hate is an Irish dramatic television series broadcast on RTÉ Television.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00475",
  "kind": "yes/no",
  "text": "Claim: The 2014 Charles Sturt Adelaide International convention took place in a suburb that contains the AAMI Stadium.\n\nPassages:\n\n[West Lakes, South Australia]\nWest Lakes is a suburb of Adelaide, the state capital of South Australia, Australia. It contains the Westfield West Lakes Shopping Centre, AAMI Stadium and the Riverside Golf Course.\n\n[2014 Charles Sturt Adelaide International]\nThe 2014 Charles Sturt Adelaide International was a professional tennis tournament played on hard courts. It took place in West Lakes, Australia between 3 and 9 February 2014.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00476",
  "kind": "yes/no",
  "text": "Claim: Russian is the nationality of the man who handily defeated Javier Mora in Max Schmeling Halle, Prenzlauer Berg, Berlin, Germany.\n\nPassages:\n\n[Javier Mora (boxer)]\nHe was defeated by Alexander Povetkin by a 5-round TKO, in Max Schmeling Halle, Prenzlauer Berg, Berlin, Germany.\n\n[Alexander Povetkin]\nAlexander Vladimirovich \"Sasha\" Povetkin ( ; Russian: Алекса́ндр Влади́мирович Пове́ткин ; born 2 September 1979) is a Russian professional boxer who held the WBA (Regular) heavyweight title from 2011 to 2013.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00477",
  "kind": "yes/no",
  "text": "Claim: Jürgen M. Geissinger is the controlling shareholder of the world's fourth-largest tyre manufacturer.\n\nPassages:\n\n[Continental AG]\nContinental is the world's fourth-largest tyre manufacturer.\n\n[Juergen M. Geissinger]\nJürgen M. Geissinger (born July 24, 1959) is a German technology business executive and Chief Executive Officer of \"Senvion S.A.\", a Hamburg based wind turbine manufacturer. Schaeffler AG, employing over 76,000 people across 180 locations in 50 countries, with annual sales of $14 billion, is also the controlling shareholder of Continental AG with 49.9% of its shares.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.92
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00478",
  "kind": "yes/no",
  "text": "Claim: Harrison Newey made his ADAC Formula 4 debut with a partner who is the son of Corinna and seven-year Formula One World Champion Michael Schumacher.\n\nPassages:\n\n[Mick Schumacher]\nHe is the son of Corinna and seven-time Formula One World Champion Michael Schumacher, nephew of former Formula One driver Ralf Schumacher, and stepnephew of Sebastian Stahl.\n\n[Harrison Newey]\nHe made his ADAC Formula 4 debut in 2015, partnering Mick Schumacher, son of world champion driver Michael Schumacher, at Van Amersfoort Racing.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00479",
  "kind": "yes/no",
  "text": "Claim: Southridge mall is synonymous with the largest, not second largest, mall in state.\n\nPassages:\n\n[Fox River Mall]\nAt 1.21 million square feet, it is the largest mall in Wisconsin.\n\n[Southridge Mall (Wisconsin)]\nAt 1.2 million square feet,(1.26 million) it is tied with the Fox River Mall in Grand Chute as the largest mall in the state (by square footage).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.65
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00480",
  "kind": "yes/no",
  "text": "Claim: Shahzeb Khanzada's show \"To The Point\" is written in Urdu.\n\nPassages:\n\n[Express News (Pakistan)]\nExpress News is an Urdu language Pakistani television news channel Based in karachi, launched on January 1, 2008.\n\n[Shahzeb Khanzada]\nHe hosted the talk show \"To The Point\" on Express News from 2011 to 2014 and has hosted the talk show \"Aaj Shahzeb Khanzada Kay Sath\" on Geo News since January 2015.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00481",
  "kind": "yes/no",
  "text": "Claim: National Artist of the USSR is the alternate translation for the honorary title of which Vladimir Basov and Inna Churikova were both 20th-century recipients.\n\nPassages:\n\n[People's Artist of the USSR]\nPeople's Artist of the USSR (Russian: Наро́дный арти́ст СССР , \"Narodný artist SSSR\"), also sometimes translated as National Artist of the USSR, was an honorary title granted to artists of the Soviet Union.\n\n[Walking the Streets of Moscow]\nThe film also features cameos by four People's Artists of the USSR: Rolan Bykov, Vladimir Basov, Lev Durov, and Inna Churikova.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00482",
  "kind": "yes/no",
  "text": "Tweet: me: *finishes book 100 of the year, gets excited to relax and watch trash tv the rest of the year*\n\nalso me: *starts book 101 ten minutes later*",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.65
  }
 },
 {
  "aid": "a00483",
  "kind": "yes/no",
  "text": "Claim: Bill McCollum took a leadership role in the Senate trial that began on December 19, 1998.\n\nPassages:\n\n[Bill McCollum]\nHe voted to impeach President Bill Clinton and subsequently took a leadership role in managing Clinton's trial in the Senate, which ended in acquittal.\n\n[Impeachment of Bill Clinton]\nThe impeachment process of Bill Clinton was initiated by the House of Representatives on December 19, 1998, against Bill Clinton, the 42nd President of the United States, on two charges, one of perjury and one of obstruction of justice.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00484",
  "kind": "yes/no",
  "text": "Claim: Dollar Days was the sixth track on award winning Bowie's twenty-fifth and final studio album. The album that was released was recorded in secret.\n\nPassages:\n\n[Death of David Bowie]\nOn 10 January 2016, English singer, songwriter and actor David Bowie died at his New York City apartment, having suffered from liver cancer for the previous 18 months. His death occurred two days after the release of his twenty-fifth studio album, \"Blackstar\", which coincided with his 69th birthday.\n\n[Blackstar (album)]\nThe album was largely recorded in secret between The Magic Shop and Human Worldwide Studios in New York City with Bowie's longtime co-producer Tony Visconti and a group of local jazz musicians.\n\n[Dollar Days]\nIt is the sixth track on Bowie's twenty-fifth and final studio album, \"Blackstar\", released on 8 January 2016.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00485",
  "kind": "yes/no",
  "text": "Claim: Matt Groening the writer of the TV episode The Telltale Head that featured the debut of the character Apu Nahasapeemapetilon who was voiced by Hank Azaria, was born on February 15, 1954.\n\nPassages:\n\n[Matt Groening]\nMatthew Abraham \"Matt\" Groening ( ; born February 15, 1954) is an American cartoonist, writer, producer, animator, and voice actor.\n\n[Apu Nahasapeemapetilon]\nHe is voiced by Hank Azaria and first appeared in the episode \"The Telltale Head\".\n\n[The Telltale Head]\nIt was written by Al Jean, Mike Reiss, Sam Simon and Matt Groening, and directed by Rich Moore.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00486",
  "kind": "yes/no",
  "text": "Claim: The ex member of Jonny (band) and Teenage Fanclub is older than the frontman of The Vines. The latter produced their album Wicked Nature.\n\nPassages:\n\n[Craig Nicholls]\nCraig Robert Nicholls (born 31 August 1977) is an Australian musician, best known as the lead singer, songwriter, and guitarist of the Australian alternative rock band The Vines, of which he is the only mainstay member.\n\n[Jonny (band)]\nJonny is a two-person band formed by Norman Blake of Teenage Fanclub and Euros Childs of Gorky's Zygotic Mynci.\n\n[Wicked Nature]\nThe release marks a few milestones for The Vines, with frontman Craig Nicholls taking on the role of producer for the first time, as well as introducing a completely new rhythm section with drummer Lachlan West and bassist Tim John.\n\n[Norman Blake (Scottish musician)]\nNorman Blake (born 20 October 1965, Bellshill, North Lanarkshire, Scotland) is a singer, instrumentalist and songwriter in the Glasgow based band Teenage Fanclub.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00487",
  "kind": "yes/no",
  "text": "Claim: Lowell Edwin Jones teaches mathematics at a school. That school is further North than where Bonnie Newman was the interim president of.\n\nPassages:\n\n[Bonnie Newman]\nNewman was also interim president of the University of New Hampshire (UNH) and the Community College System of New Hampshire.\n\n[Lowell Edwin Jones]\nLowell Jones (born 1945) is an American professor of mathematics at Stony Brook University Jones' primary fields of interest are topology, and geometry.\n\n[University of New Hampshire]\nThe University of New Hampshire (UNH) is a public research university in the University System of New Hampshire, in the United States.\n\n[Stony Brook University]\nThe State University of New York at Stony Brook (also known as Stony Brook University or SUNY Stony Brook) is a public sea-grant and space-grant research university located in Stony Brook, New York in the United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00488",
  "kind": "yes/no",
  "text": "Claim: Gary Paulsen wrote the 1987 Newberry Honor-winning young-adult wilderness survival novel and the fifth and remaining novel of that same series, called Brian's Hunt.\n\nPassages:\n\n[Hatchet (novel)]\nHatchet is a 1987 Newbery Honor-winning young-adult wilderness survival novel written by American writer Gary Paulsen.\n\n[Brian's Hunt]\nBrian's Hunt is a 2003 young adult novel by Gary Paulsen. It is the fifth and final book in the award-winning \"Hatchet\" series, which deals with Brian Robeson, a boy who learns wilderness survival when he is stranded after a plane wreck.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.93
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00489",
  "kind": "yes/no",
  "text": "Claim: Ivan Konrad Trajkovic qualified for the event in which Ivan Čupić won a bronze medal, the major international competition celebrated in the tradition of the Olympic Games, as governed by the International Olympic Committee.\n\nPassages:\n\n[Ivan Čupić]\nHe also played in the Croatian team that won the bronze medal at the 2012 Summer Olympics.\n\n[Ivan Trajkovič]\nHe qualified for the 2012 Summer Olympics in the +80 kg category.\n\n[2012 Summer Olympics]\nThe 2012 Summer Olympics, formally the Games of the XXX Olympiad and commonly known as London 2012, was a major international multi-sport event celebrated in the tradition of the Olympic Games, as governed by the International Olympic Committee (IOC).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00490",
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
  }
 },
 {
  "aid": "a00491",
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
  }
 },
 {
  "aid": "a00492",
  "kind": "yes/no",
  "text": "Claim: American Heavy metal band Pantera worked with producer Terry Date and released four albums during the 1980's.\n\nPassages:\n\n[Pantera]\nHaving started as a glam metal band, Pantera released four albums during the 1980s.\n\n[Terry Date]\nTerry Date (born January 31, 1956) is an American record producer and engineer, specializing in the rock genres, especially heavy metal.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00493",
  "kind": "yes/no",
  "text": "Claim: The award winning game Doom is a reboot of the franchise developed by id Software.\n\nPassages:\n\n[2016 in video gaming]\nMany awards went to games such as \"Overwatch\", \"\", \"Inside\", \"Doom\", \"Dark Souls III\", \"The Last Guardian\", \"Dishonored 2\" and \"Titanfall 2\".\n\n[Doom (2016 video game)]\nA reboot of the \"Doom\" franchise, it is the fourth title in the main series and the first major installment since \"Doom 3\" in 2004.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00494",
  "kind": "yes/no",
  "text": "Claim: Sugata Marjit is the former Vice Chancellor of the University of Calcutta, located in Kolkata (formerly \"Calcutta\"), West Bengal, India first established on 24 January 1857.\n\nPassages:\n\n[University of Calcutta]\nThe University of Calcutta (informally known as Calcutta University or CU) is a public state university located in Kolkata (formerly \"Calcutta\"), West Bengal, India established on 24 January 1857.\n\n[Sugata Marjit]\nSugata Marjit is the former Vice Chancellor of the University of Calcutta and Reserve Bank of India Professor of Industrial Economics at the Centre for Studies in Social Sciences, Calcutta and the Project Director of Centre for Training & Research in Public Finance and Policy (CTRPFP) [A Ministry of Finance, Government of India funded initiative].",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00495",
  "kind": "yes/no",
  "text": "Claim: Arizona State Route 51 (SR 51) is named after a Native American woman belonging to the Native American tribe.\n\nPassages:\n\n[Lori Piestewa]\nA member of the Hopi tribe, Piestewa was the first Native American woman in history to die in combat while serving in the U.S. military and the first woman in the U.S. military killed in the Iraq War.\n\n[Arizona State Route 51]\nArizona State Route 51 (SR 51), also known as the Piestewa Freeway, is a numbered state highway in Phoenix, Arizona. The peak was named after Lori Piestewa, the first Native American woman to die in combat in the U.S. Military.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00496",
  "kind": "yes/no",
  "text": "Post: When you find out someone you sat next to for a half hour meeting tested positive for COVID but no one told you. So you measure with the principal and were within 6 ft, but they don’t count you as a close contact because they don’t want you out 😬 #education",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00497",
  "kind": "yes/no",
  "text": "Post: All I've done this summer is binge watch The Office and Friends 🙃🙃",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00498",
  "kind": "yes/no",
  "text": "Claim: The Church of England's movement that inspired the Trinity Episcopal Church in Houghton, Michigan was opposed by a religious figure who wrote devotional literature.\n\nPassages:\n\n[Oxford Movement]\nThe Oxford Movement was a movement of High Church members of the Church of England which eventually developed into Anglo-Catholicism.\n\n[Samuel Rickards]\nSamuel Rickards (1796–1865) was a Church of England clergyman, opponent of the Oxford Movement, and writer of devotional literature.\n\n[Trinity Episcopal Church (Houghton, Michigan)]\nThe church's philosophy is built on the Oxford Movement.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00499",
  "kind": "yes/no",
  "text": "Claim: Greatest Hits Volume 1 is a greatest hits compilation album by The Beatles which was exclusive to Australia and New Zealand, the album was compiled by EMI Australia to fill in the gap, much like A Collection of Beatles Oldies (subtitled But Goldies!), by the English rock band the Beatles.\n\nPassages:\n\n[A Collection of Beatles Oldies]\nA Collection of Beatles Oldies (subtitled But Goldies!)\n\n[Greatest Hits Volume 1 (Beatles album)]\nThe album was compiled by EMI Australia to fill in the gap between \"Rubber Soul\" and \"Revolver\" (much like \"A Collection of Beatles Oldies\" would in 1966 in between \"Revolver\" and \"Sgt. Pepper's Lonely Hearts Club Band\").",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 }
]
