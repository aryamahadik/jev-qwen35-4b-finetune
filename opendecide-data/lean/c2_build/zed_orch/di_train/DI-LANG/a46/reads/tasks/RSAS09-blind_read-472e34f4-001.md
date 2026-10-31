# A46 replay label-noise blind read RSAS09-blind_read-472e34f4-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS09-blind_read-472e34f4-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
If an item truly cannot be settled from its text and definitions (the needed information is missing, or the question has no single defensible answer), answer exactly "abstain" instead. Use it rarely; a hard item that you can still reason out is not a reason to abstain.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no | abstain, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q6cb7d32d5f",
  "kind": "yes/no",
  "text": "Claim: The father of the Princess Charlotte of Lorraine has a descendant that includes Umberto II the final king of Italy.\n\nPassages:\n\n[Charlotte of Lorraine]\nCharlotte de Lorraine-Armagnac (6 May 1678 – 21 January 1757) was a Princess of Lorraine by birth and daughter of Louis, Count of Armagnac.\n\n[Umberto II of Italy]\nUmberto II (Italian: \"Umberto Nicola Tommaso Giovanni Maria di Savoia\" ; 15 September 190418 March 1983), was the last King of Italy.\n\n[Louis, Count of Armagnac]\nHis descendants include Albert II, Prince of Monaco, Umberto II of Italy, and Diana Álvares Pereira de Melo, 11th Duchess of Cadaval.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb68a7e59a3",
  "kind": "yes/no",
  "text": "Claim: The head office of József Váradi's airline is located in Budapest.\n\nPassages:\n\n[Wizz Air]\n\" ), is a Hungarian low-cost airline with its head office in Budapest.\n\n[József Váradi]\nJózsef Janos Váradi (born 21 September 1965) is a Hungarian businessman who co-founded Wizz Air and has been its CEO since 2003.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q47f087bcae",
  "kind": "yes/no",
  "text": "Text: quackity stream is making me so genuinely happy rn",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q1b26f81a57",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I am tired of your crap.",
   "i have bags under my eyes because im tired of your bs:)"
  ]
 },
 {
  "qid": "qb619241a65",
  "kind": "yes/no",
  "text": "Claim: The author Prof Bhabananda Deka is an economist, not the author of the 1953 fiction work, The Captive Mind.\n\nPassages:\n\n[The Captive Mind]\nThe Captive Mind (Polish: Zniewolony umysł ) is a 1953 work of nonfiction by Polish writer, academic and Nobel laureate Czesław Miłosz, published in the English translation originally by Secker and Warburg.\n\n[Bhabananda Deka]\nProf Bhabananda Deka (Assamese:ভৱানন্দ ডেকা) (19 August 1929 – 4 December 2006) has been acknowledged as the pioneer Assam economist and author, who conducted path-breaking research for the very first time on the economy of the far eastern part of India.\n\n[Czesław Miłosz]\nCzesław Miłosz ( ; 30 June 1911 – 14 August 2004) was a Polish poet, prose writer, translator and diplomat.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q8368741857",
  "kind": "yes/no",
  "text": "Claim: Alien Resurrection was the last of four Alien films to feature Sigourney Weaver.\n\nPassages:\n\n[Sigourney Weaver]\nFollowing her film debut as a minor character in \"Annie Hall\" (1977), she quickly came to prominence with her first lead role as Ellen Ripley in \"Alien\" (1979). She reprised the role in three sequels: \"Aliens\" (1986), for which she was nominated for the Academy Award for Best Actress; \"Alien 3\" (1992), and \"Alien Resurrection\" (1997).\n\n[Alien Resurrection]\nIt is the fourth installment in the \"Alien\" film series, and the final installment in the original series.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6b4d5360b8",
  "kind": "yes/no",
  "text": "Claim: The Scadoxus plant not which Enkianthus campanulatus is the hardiest species to be small enough. This plant could to be grown as an ornamental plant in tiny containers.\n\nPassages:\n\n[Scadoxus]\nSpecies of \"Scadoxus\" are grown as ornamental plants for their brilliantly coloured flowers, either in containers or in the ground in frost-free climates.\n\n[Enkianthus campanulatus]\nThe hardiest of \"Enkianthus\" species is E. campanulatus (furin-tsutsuji or redvein enkianthus), a medium-sized, narrow, upright, deciduous shrub.\n\n[Enkianthus]\nEnkianthus is a genus of shrubs or small trees in the heath family (Ericaceae).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q795f5f0a90",
  "kind": "yes/no",
  "text": "Post: One positive of the dark mornings is you can walk the dogs in your pyjamas and no one can tell 🤗🤗🤗",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q6dbb01863a",
  "kind": "yes/no",
  "text": "Post: The goal is not to change history, it is to decide which parts we celebrate. Racism should not be one of them ..",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q797f331b6d",
  "kind": "yes/no",
  "text": "Tweet: i would rather be outside reed timmers car in f3 tornado winds than go to work today",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q141410a583",
  "kind": "yes/no",
  "text": "Claim: Sabina Cvilak sang this in Ryde on the centenary of the composer's birth. That composer and Béla Bartók are not from the same country.\n\nPassages:\n\n[Béla Bartók]\nBéla Viktor János Bartók ( ; ] ; 25 March 1881 – 26 September 1945) was a Hungarian composer, pianist and an ethnomusicologist.\n\n[War Requiem]\nThe War Requiem, Op.\n\n[Sabina Cvilak]\nShe is also known for singing concerts and recitals, such as Britten's \"War Requiem\" in London on the centenary of the composer's birth.\n\n[Benjamin Britten]\nEdward Benjamin Britten, Baron Britten {'1': \", '2': \", '3': \", '4': \"} (22 November 1913 – 4 December 1976) was an English composer, conductor and pianist.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qdaf904e65e",
  "kind": "yes/no",
  "text": "Claim: An establishment observatory is located next to a historic landmark. It and Miniatürk are both in Istanbul, Turkey. Mustafa Yektaoğlu studied at this establishment.\n\nPassages:\n\n[Miniatürk]\nMiniatürk is a miniature park situated at the north-eastern shore of Golden Horn in Istanbul, Turkey.\n\n[Istanbul University Observatory]\nEstablished in 1936, it is situated next to the historic Beyazıt Tower within the main campus of the university at Beyazıt Square in Fatih district of Istanbul, Turkey.\n\n[Beyazıt Tower]\nBeyazıt Tower, also named Seraskier Tower, from the name of the Ottoman ministry of War, is an 85 m tall fire-watch tower located in the courtyard of Istanbul University's main campus (formerly Ottoman Ministry of War) on Beyazıt Square (known as the Forum Tauri in the Roman period) in Istanbul, Turkey, on top of one of the \"seven hills\" which Constantine the Great had built the city, following the model of Rome.\n\n[Mustafa Yektaoğlu]\nHe studied at the Istanbul Faculty of Medicine at Istanbul University graduating in 1978.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe90c018f72",
  "kind": "yes/no",
  "text": "Claim: The 1993 album that the song Juntos (Together) is on and The Black Hole are not both sports films.\n\nPassages:\n\n[Juntos (Together)]\nThe song was released digitally via the iTunes Store by Walt Disney Records and Universal Music Latin on January 20, 2015, as the lead single from the soundtrack for \"McFarland, USA\".\n\n[The Black Hole]\nThe Black Hole is a 1979 American science fiction film directed by Gary Nelson and produced by Walt Disney Productions.\n\n[McFarland, USA]\nMcFarland, USA (also known as McFarland) is a 2015 American sports drama film directed by Niki Caro, produced by Mark Ciardi and Gordon Gray, written by Christopher Cleveland, Bettina Gilois and Grant Thompson with music composed by Antônio Pinto.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qddc1437afb",
  "kind": "yes/no",
  "text": "Claim: The mother of Megan Phelps-Roper is best known as the former spokesperson of a church located in Topeka.\n\nPassages:\n\n[Megan Phelps-Roper]\nHer mother is Shirley Phelps-Roper, whose father was the church's founder Fred Phelps.\n\n[Shirley Phelps-Roper]\nShe is best known as the former spokesperson of the Westboro Baptist Church of Topeka, Kansas, an organization known for its highly publicized homophobic public protests conducted under the slogan \"God Hates Fags.\"",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf2a1635f9a",
  "kind": "yes/no",
  "text": "Claim: Roger Meddows Taylor was born earlier than Elizabeth Fraser.\n\nPassages:\n\n[Roger Taylor (Queen drummer)]\nRoger Meddows Taylor (born 26 July 1949) is an English musician, singer and songwriter.\n\n[Elizabeth Fraser]\nElizabeth Davidson Fraser (born 29 August 1963), sometimes known as Liz Fraser, is a British singer, songwriter and musician from Grangemouth, Scotland, best known as the vocalist for the band Cocteau Twins.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q9ec6ddc9c7",
  "kind": "yes/no",
  "text": "Claim: The name of Bruce Willis's character in the film, where Bostin Christopher had a small role, is David Dunn.\n\nPassages:\n\n[Unbreakable (film)]\nIn \"Unbreakable\", a security guard named David Dunn survives a horrific train crash.\n\n[David Dunn (character)]\nDavid Dunn is a fictional character and the main protagonist in the \"Unbreakable\" film series, portrayed by American actor Bruce Willis.\n\n[Bostin Christopher]\nChristopher also had a small role in M. Night Shyamalan's \"Unbreakable\", as a Comic Book Clerk.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7de9f1db3e",
  "kind": "yes/no",
  "text": "Claim: Democracy Day is a possible federal holiday proposed by a republican politician that represents the 13th US congressional district.\n\nPassages:\n\n[Democracy Day (United States)]\nDemocracy Day is the tentative name of a possible federal holiday in the United States, proposed by Democratic Representative John Conyers of Michigan.\n\n[John Conyers]\nJohn James Conyers Jr. (born May 16, 1929) is an American Democratic politician and the U.S. Representative for 's 13th congressional district .",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1de081dc01",
  "kind": "yes/no",
  "text": "Claim: The railroad that connects with Yancey Railroad was completed in the mid 1910s commonly used Challengers.\n\nPassages:\n\n[Yancey Railroad]\nThe Yancey Railroad (reporting mark YAN) was an American Class III shortline railroad that operated for freight service from a connection with the Clinchfield Railroad at Kona, North Carolina, through Micaville, to Burnsville, 10.6 mi .\n\n[Clinchfield Railroad]\nThe 35-mile segment from Dante, Virginia, to Elkhorn City, opening up the coal lands north of Sandy Ridge Mountains and forming a connection with the Chesapeake and Ohio Railway at Elkhorn City, was completed in 1915.\n\n[4-6-6-4]\nChallengers were most common in the Union Pacific Railroad and the Clinchfield Railroad.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q891c0fa2bf",
  "kind": "yes/no",
  "text": "Claim: The ancient Roman town near secluded private Fusaro Lake is now the commune of Bacoli.\n\nPassages:\n\n[Baiae]\nBaiae (Italian: \"Baia\" ; Neapolitan: \"Baia\" ) was an ancient Roman town situated on the northwest shore of the Gulf of Naples, and now in the \"comune\" of Bacoli.\n\n[Fusaro Lake]\nIt is about 0.5 mi from Baia, and about 1 mi south of the acropolis of Cumae.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qcc84465793",
  "kind": "yes/no",
  "text": "Claim: Italian former footballer Daniele Massaro scored in the 4-0 AC Milan win against Barcelona in the Final of the 1985 UEFA Champions league.\n\nPassages:\n\n[Daniele Massaro]\nDaniele Emilio Massaro (born 23 May 1961) is an Italian former footballer, who played as a forward.\n\n[1993–94 FC Barcelona season]\nFC Barcelona had one of its most successful seasons in the club's history, retaining the domestic league supremacy and reaching the final of the UEFA Champions League; however they collapsed 0-4 against AC Milan (goals from Daniele Massaro, Dejan Savićević and Marcel Desailly).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q21229e4070",
  "kind": "yes/no",
  "text": "Claim: Fredric March costarred in 1935 Australian drama film that Frances Drake is best know for, with the husband of Elsa Lanchester.\n\nPassages:\n\n[Les Misérables (1935 film)]\nLes Misérables is a 1935 American drama film starring Fredric March and Charles Laughton based upon the famous Victor Hugo novel of the same name.\n\n[Charles Laughton]\nIn 1927, he was cast in a play with his future wife Elsa Lanchester, with whom he lived and worked until his death; they had no children.\n\n[Frances Drake]\nFrances Drake (October 22, 1912 – January 18, 2000) was an American actress, best known for playing Eponine in \"Les Misérables\" (1935).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q8d38906c74",
  "kind": "yes/no",
  "text": "Text: @32watto Neighbours",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qa5afe794a0",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Accidentally made a friend in ASL today. I hate when that happens.",
   "I would say \"Made a friend in ASL today. I love when that happens.\""
  ]
 },
 {
  "qid": "q385d3dd870",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "hey quick question is it fall or spring???",
   "Why is it so frickin warm in November someone lmk"
  ]
 },
 {
  "qid": "q538167972d",
  "kind": "yes/no",
  "text": "Post: I would like to dedicate my hot girl summer to the Eastpointe Chick-Fil-A. Thank you!",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q7762d8561e",
  "kind": "yes/no",
  "text": "Claim: First Street is the historic meeting venue built in a style taught at the Ecole des Beaux-Arts.\n\nPassages:\n\n[Dayton Memorial Hall]\nThe Dayton Memorial Hall is a historic meeting venue on First Street in downtown Dayton, Ohio, United States. Constructed shortly after the turn of the twentieth century, this Beaux-Arts structure is one of many memorial halls statewide from the same time period, and it has been named a historic site.\n\n[Beaux-Arts architecture]\nBeaux-Arts architecture ( ; ] ) expresses the academic neoclassical architectural style taught at the \"École des Beaux-Arts\" in Paris.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8baf945467",
  "kind": "yes/no",
  "text": "Claim: Isabella (Belle) Baumfree was the birth name of the ex-slave abolitionist featured in the sculpture that also memorialized Barbe de Verrue.\n\nPassages:\n\n[Barbe de Verrue]\nShe is memorialized as a figure in \"The Dinner Party\" by Judy Chicago.\n\n[Sojourner Truth]\nSojourner Truth ( ; born Isabella (Belle) Baumfree; 1797 – November 26, 1883) was an African-American abolitionist and women's rights activist.\n\n[The Dinner Party]\nSacajawea, Sojourner Truth, Eleanor of Aquitaine, Empress Theodora of Byzantium, Virginia Woolf, Susan B. Anthony, and Georgia O'Keeffe are among the guests.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q15ec1ff255",
  "kind": "yes/no",
  "text": "Claim: The Single Guy is an American television family sitcom comedy that ran for two seasons on NBC, from September 1995 to April 1997 on Monday nights; starring Ming-Na Wen as Sam's wife, Ming-Na Wen is an American actress, born November 20, 1963.\n\nPassages:\n\n[The Single Guy]\nThe series also starred Joey Slotnick as Eliot's best friend Sam Sloan, Ming-Na Wen as Sam's wife Trudy and Ernest Borgnine as doorman Manny, throughout its entire run.\n\n[Ming-Na Wen]\nMing-Na Wen (; born November 20, 1963) is an American actress.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa7825e3fd7",
  "kind": "yes/no",
  "text": "Claim: Daniel Awde was born in Liverpool, England.\n\nPassages:\n\n[London]\nLondon is the capital and most populous city of England and the United Kingdom.\n\n[Daniel Awde]\nDaniel \"Dan\" Awde (born 22 June 1988 in Hammersmith, London) is a British 400 metres runner and former decathlete who has twice competed at the Summer Olympic Games.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qe9d6b67d52",
  "kind": "yes/no",
  "text": "Claim: This hit song was released before Love Shy (Thinking About You). It is of the genre called Garage from the country that studio album Escape from the Sun was released in, due to its 4x4 rhythm.\n\nPassages:\n\n[Love Shy (Thinking About You)]\nIt was released after the success of \"What's It Gonna Be\" with H \"Two\" O.\n\n[Bassline (music genre)]\nBassline (sometimes referred to as bassline house, Niche or 4x4) is a type of music related to UK garage that originated in Sheffield in the early 2000s.\n\n[Escape from the Sun]\nIt was released in April 2009 through Marrakesh Records, available to buy in certain stores around the UK.\n\n[What's It Gonna Be (H &quot;Two&quot; O song)]\nis a bassline (subgenre of UK garage) song performed by the duo known as H \"Two\" O (Selim Ben Rabha, \"Solution\", and Simon McDevitt, \"Oz\", who also go by \"Hit 'Em\" and \"Hard\") and the British three-person bassline vocal group Platnum (Aaron Evers, Mina Poli, and Michelle McKenna).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q9ea68ee28a",
  "kind": "yes/no",
  "text": "Claim: Norbert Holm was arrested and later demoted because of his Chief of Operations association with a military theorist popularly known as the Desert Fox.\n\nPassages:\n\n[Norbert Holm]\nNorbert Holm (16 December 1895 – 3 June 1962) was a general in the Wehrmacht of Nazi Germany during World War II. Following the 20 July plot, on 16 September 1944, Norbert Holm was arrested and later demoted because of his Chief of Operations association with Field Marsal Erwin Rommel.\n\n[Erwin Rommel]\nErwin Rommel (15 November 1891 – 14 October 1944) was a German general and military theorist. Popularly known as the Desert Fox, he served as field marshal in the Wehrmacht of Nazi Germany during World War II.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q037a51d78b",
  "kind": "yes/no",
  "text": "Claim: The Lever Brothers parted with Margarine Unie to create an Indonesian soap factory.\n\nPassages:\n\n[Unilever Indonesia]\nPT Unilever Indonesia Tbk () was established in Indonesia on December 5, 1933 as Lever Zeepfabrieken N.V., a subsidiary of Lever Brothers which initially operated a soap factory at Angke, Jakarta.\n\n[Lever Brothers]\nIn 1930, Lever Brothers merged with Margarine Unie to form Unilever.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qfc6cfab0d8",
  "kind": "yes/no",
  "text": "Claim: The Russian-British physicist who shared the Nobel Prize in Physics in 2010 has established a reserach center dedicated to continuing the work with graphene in Singapore.\n\nPassages:\n\n[Konstantin Novoselov]\nSir Konstantin Sergeevich Novoselov (born 23 August 1974) is a Russian-British physicist, and Langworthy Professor in the School of Physics and Astronomy at the University of Manchester.\n\n[Graphene Research Centre]\nThe Graphene Research Centre (GRC), at the National University of Singapore (NUS), is the first centre in Asia dedicated to graphene research.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q19099f6b24",
  "kind": "yes/no",
  "text": "Claim: Dronamraju Krishna Rao focused his work on the research of a British-born scientist who passed on 1 december 1964.\n\nPassages:\n\n[Dronamraju Krishna Rao]\nOne focus of his work has been the research of J. B. S. Haldane.\n\n[J. B. S. Haldane]\nJohn Burdon Sanderson Haldane ( ; 5 November 1892 – 1 December 1964) was a British-born scientist known for his work in the study of physiology, genetics, evolutionary biology, and in mathematics, where he made innovative contributions to the fields of statistics and biostatistics.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q822610d98f",
  "kind": "yes/no",
  "text": "Claim: Colonel Michael Mulligan was the lead prosecutor for the soilder court-martialed for the premeditated attack at Camp Pennsylvania, Kuwait.\n\nPassages:\n\n[Michael Mulligan]\nColonel Michael Mulligan is a prosecutor in the United States Army notable for serving as the lead prosecutor in the courts-martial of Hasan Akbar and of Nidal Malik Hasan, the sole accused in the November 2009 Fort Hood shooting.\n\n[United States v. Hasan K. Akbar]\nUnited States v. Hasan K. Akbar was the court-martial of a United States Army soldier for a premeditated attack in the early morning hours of March 23, 2003, at Camp Pennsylvania, Kuwait, during the start of the United States invasion of Iraq.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4747b2bd74",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "You guys, I just saw the most hysterical fake musical - Electro City! Wouldn’t it be funny if it was a real show we could produce?",
   "I picked next year's musical already...Electro City. Obvious choice."
  ]
 },
 {
  "qid": "q184f56390b",
  "kind": "yes/no",
  "text": "Claim: Excalibur Hotel and Casino developed by William G. Bennett is the casino in Las Vegas now operated by MGM Resorts International.\n\nPassages:\n\n[Excalibur Hotel and Casino]\nExcalibur Hotel and Casino is a hotel and casino located on the Las Vegas Strip in Paradise, Nevada, in the United States. It is owned and operated by MGM Resorts International.\n\n[William G. Bennett (gaming executive)]\nUnder his leadership Circus Circus would go on to develop numerous additional properties throughout Nevada, including the Excalibur and Luxor casinos in Las Vegas.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0e24d5fe5c",
  "kind": "yes/no",
  "text": "Claim: The serial killer who buried his victims in the state pine forest owned by the New South Wales Government is called Ivan Milat.\n\nPassages:\n\n[Backpacker murders]\nThe backpacker murders were a spate of serial killings that took place in New South Wales, Australia, between 1989 and 1993, committed by Ivan Milat. The bodies of seven missing young people aged 19 to 22 were discovered partially buried in the Belanglo State Forest, 15 km south west of the New South Wales town of Berrima.\n\n[Belanglo State Forest]\nThe forest is owned by the New South Wales Government and contains some of the earliest pine plantings in the state.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q37ef9c630d",
  "kind": "yes/no",
  "text": "Claim: The Diamond v. Chakrabarty court case occurred after another one. C. Lee Buxton was an appellant in this other case.\n\nPassages:\n\n[Griswold v. Connecticut]\nGriswold v. Connecticut, 381 U.S. 479 (1965) , is a landmark case in the United States in which the Supreme Court of the United States ruled that the Constitution, through the Bill of Rights, implies a fundamental right to privacy.\n\n[C. Lee Buxton]\nCharles Lee Buxton (October 14, 1904 – July 7, 1969) was an American gynecologist, professor at the Yale School of Medicine, and appellant in US Supreme Court case \"Griswold v. Connecticut\".\n\n[Diamond v. Chakrabarty]\nDiamond v. Chakrabarty, 447 U.S. 303 (1980), was a United States Supreme Court case dealing with whether genetically modified organisms can be patented.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q127c5ef1b6",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "They should seek guidance.",
   "@PFTompkins Her family should definitely not seek mental health guidance. 😬"
  ]
 },
 {
  "qid": "q3625e29f72",
  "kind": "yes/no",
  "text": "Claim: Corbin Sinclair Bryant played for the Buffalo Bills and the NFL team Burke Dales was signed to in 2002, that was founded in 1933, and is the oldest franchise in the AFC.\n\nPassages:\n\n[Pittsburgh Steelers]\nFounded in 1933 , the Steelers are the oldest franchise in the AFC.\n\n[Corbin Bryant]\nHe has also played for the Pittsburgh Steelers and Buffalo Bills.\n\n[Burke Dales]\nHe was signed by the Pittsburgh Steelers as an undrafted free agent in 2002.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qabb42d6d48",
  "kind": "yes/no",
  "text": "Claim: Charleston is the capital of North Carolina, the state Curly Ray Cline is from.\n\nPassages:\n\n[West Virginia]\nThe capital and largest city is Charleston.\n\n[Curly Ray Cline]\nCurly Ray Cline (January 10, 1923 – August 19, 1997) was an American bluegrass fiddler from West Virginia known for his work with the Lonesome Pine Fiddlers and Ralph Stanley.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q3df35d46b9",
  "kind": "yes/no",
  "text": "Claim: Ahmad Niyaltigin was the treasurer of a sultan who rose to power by seizing the Ghaznavid throne from his younger twin.\n\nPassages:\n\n[Ahmad Niyaltigin]\nAhmad Niyaltigin (Persian: ‎ ‎ ) was a treasurer of Sultan Mahmud Ghaznavi and later of his son Sultan Mas'ud Ghaznavi.\n\n[Mas'ud I of Ghazni]\nMas'ud I of Ghazni (Persian: مسعود غزنوی‎ ‎ ), known as Amīr-i Shahīd (امیر شهید ; \"the martyr king\")(998 – 17 January 1040), was \"sultan\" of the Ghaznavid Empire from 1030 to 1040. He rose to power by seizing the Ghaznavid throne from his younger twin Mohammad, who had been nominated as the heir upon the death of their father Mahmud of Ghazni.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q59848208df",
  "kind": "yes/no",
  "text": "Claim: The apparent magnitude of the spiral galaxy discovered in 2015 by Frank Leavenworth is 15.18.\n\nPassages:\n\n[Francis Preserved Leavenworth]\nFrancis Preserved Leavenworth (born September 3, 1858 in Mount Vernon, Indiana; died November 12, 1928; a.k.a. \"Frank Leavenworth\") was an American astronomer.\n\n[NGC 166]\nNGC 166 (also known as PGC 2143) is a spiral galaxy located around 2.6 million light-years away in the constellation Cetus, with an apparent magnitude of 15.18.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1f806fd6e9",
  "kind": "yes/no",
  "text": "Claim: The film, in which Kirsten Olson played Nikki Fletcher, is directed by Tim Fywell, included the actress who also appeared in \"Euro Trip\" and \"Inspector Gadget\".\n\nPassages:\n\n[Ice Princess]\nIce Princess is a 2005 American figure-skating film directed by Tim Fywell, written by Hadley Davis from a story by Meg Cabot and Davis, and starring Michelle Trachtenberg, Joan Cusack, Kim Cattrall and Hayden Panettiere.\n\n[Kirsten Olson]\nAs an actress, Olson played the role of Nikki Fletcher, the 'Jumping Shrimp,' in the Disney movie \"Ice Princess\" (2005).\n\n[Michelle Trachtenberg]\nShe has also appeared in films such as \"Harriet the Spy\" (1996), \"Inspector Gadget\" (1999), \"EuroTrip\" (2004), \"Ice Princess\" (2005), \"Black Christmas\" (2006), \"17 Again\" (2009), \"Cop Out\" (2010), \"Weeds\" (2011), and \"Killing Kennedy\" (2013).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa83a59b03c",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "@Rosievix @mouthwaite Well, illegal immigrants categorically don’t get money from the government but why let a little thing like facts get in the way of a good bit of xenophobia...",
   "I'd end the sentence by saying \"but your xenophobia means that you have ignored the facts\"."
  ]
 },
 {
  "qid": "q37df502763",
  "kind": "yes/no",
  "text": "Claim: The grandfather of Rainer Hoss conducted the negotiations with the owners and was the commandant of Auschwitz concentration and extermination camp.\n\nPassages:\n\n[Gerstein Report]\nThe Gerstein Report was written in 1945 by Kurt Gerstein, an Obersturmführer (First Lieutenant) of the Waffen-SS who rose to become the Head of Technical Disinfection Services of the SS, and in that capacity supplied hydrogen cyanide (Zyklon B) from Degesch (\"Deutsche Gesellschaft für Schädlingsbekämpfung\") to Rudolf Höss in Auschwitz and conducted the negotiations with the owners.\n\n[Rudolf Höss]\nRudolf Höss (also Höß, Hoeß or Hoess; 25 November 1901 – 16 April 1947) was a Nazi German \"SS\"-\"Obersturmbannführer\" (lieutenant colonel) and the longest-serving commandant of Auschwitz concentration and extermination camp in World War II.\n\n[Rainer Höss]\nRainer Höss, born 25 May 1965 in Stuttgart, is the grandson of Rudolf Höss.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa5e7ff9d36",
  "kind": "yes/no",
  "text": "Claim: \"Mandrake Root\" is a song by the globe's loudest free jazz band as listed in the Guinness Book of World Records from 1975.\n\nPassages:\n\n[Mandrake Root]\n\"Mandrake Root\" is a song by Deep Purple that is featured on their debut album \"Shades of Deep Purple\".\n\n[Deep Purple]\nDeep Purple are an English rock band formed in Hertford in 1968. They were listed in the 1975 \"Guinness Book of World Records\" as \"the globe's loudest band\" for a 1972 concert at London's Rainbow Theatre, and have sold over 100 million albums worldwide.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3415f85dfd",
  "kind": "yes/no",
  "text": "Claim: Rocky Boy's Indian Reservation is located in Hill and Chouteau and named after the principal leader of the Montana Chippewa-Cree.\n\nPassages:\n\n[Rocky Boy's Indian Reservation]\nRocky Boy's Indian Reservation is one of seven American Indian reservations in the U.S. state of Montana. The reservation is located in Hill and Chouteau counties in northeastern Montana, about 40 mi from the Canada–U.S. border.\n\n[Rocky Boy (Chippewa leader)]\nAsiniiwin, translated Rocky Boy or Stone Child was an important Chippewa leader who became the principal leader of the Montana Chippewa-Cree in the late 19th century and early 20th century.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qcf520a8899",
  "kind": "yes/no",
  "text": "Claim: Nobody Loves You was written by John Lennon and released on the album, Walls and Bridges, which was issued by Apple Records, and was written, recorded, and released during his 18 month separation from artist Yoko Ono.\n\nPassages:\n\n[Nobody Loves You (When You're Down and Out)]\n\"Nobody Loves You (When You're Down and Out)\" is a song written by John Lennon released on his 1974 album \"Walls and Bridges\".\n\n[Walls and Bridges]\nIt was issued by Apple Records on 26 September 1974 in the United States and on 4 October in the United Kingdom. Written, recorded and released during his 18-month separation from Yoko Ono, the album captured Lennon in the midst of his \"Lost Weekend\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 }
]
