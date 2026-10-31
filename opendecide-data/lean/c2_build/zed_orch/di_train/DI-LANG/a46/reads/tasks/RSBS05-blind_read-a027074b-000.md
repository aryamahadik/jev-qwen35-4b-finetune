# A46 replay label-noise blind read RSBS05-blind_read-a027074b-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS05-blind_read-a027074b-000.json

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
  "qid": "q4cddf417c1",
  "kind": "yes/no",
  "text": "Claim: The band who \"Evie\" formed in was in the city Sydney, Australia.\n\nPassages:\n\n[The Easybeats]\nThe Easybeats were an Australian rock band which formed in Sydney, Australia, in late 1964, and disbanded at the end of 1969.\n\n[Evie (song)]\n\"Evie\" is an Australian rock song released as a single in 1974 by Australian singer and former frontman of The Easybeats, Stevie Wright.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q3a9fea3f52",
  "kind": "yes/no",
  "text": "Claim: The Battle of White Plains was the final campaign, during which the Battle of Harlem was fought as part of the American Revolutionary War, was a series of battles for control of New York City and the state of New Jersey, fought on October 28, 1776 near White Plains, New York.\n\nPassages:\n\n[Battle of Harlem Heights]\nThe Battle of Harlem Heights was fought during the New York and New Jersey campaign of the American Revolutionary War.\n\n[New York and New Jersey campaign]\nThe New York and New Jersey campaign was a series of battles for control of New York City and the state of New Jersey in the American Revolutionary War between British forces under General Sir William Howe and the Continental Army under General George Washington in 1776 and the winter months of 1777.\n\n[Battle of White Plains]\nThe Battle of White Plains was a battle in the New York and New Jersey campaign of the American Revolutionary War fought on October 28, 1776, near White Plains, New York.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0fd0316fdb",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Dear Evan Hanson cast the same type of older actors as Grease.",
   "All the shade i have been hearing about Ben Platt being unbelievable as a teenager in the @DearEvanHansen movie boggles me. Does nobody have any memories of Grease??? Name 1 actor on that film who believably looked high school age!"
  ]
 },
 {
  "qid": "q2659bffaff",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "dont you hate it when youre just chilling in your room and then theres a spider and you kill it but when you kill it you spill soda all over your keyboard yeah me too",
   "dont you love it when youre just chilling in your room and then theres a spider and you kill it but when you kill it you spill soda all over your keyboard yeah me too"
  ]
 },
 {
  "qid": "qe5edad678a",
  "kind": "yes/no",
  "text": "Claim: The 1974–75 Philadelphia Flyers, an entirely Canadian-born team, scored 4 points in the 1975 Stanley Cup held during July.\n\nPassages:\n\n[1974–75 Philadelphia Flyers season]\nThe 1974–75 Philadelphia Flyers season was the Philadelphia Flyers eighth season in the National Hockey League (NHL). The 1974–75 Flyers were the last Stanley Cup champion to be composed entirely of Canadian-born players.\n\n[1974–75 Buffalo Sabres season]\nThe Sabres lost the series 4–2.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qf41fe6e78d",
  "kind": "yes/no",
  "text": "Claim: Manaslu stands higher than the landform that is 60 km due south of Chakragil.\n\nPassages:\n\n[Chakragil]\nIt is located about 100 km southwest of Kashgar, about 60 km due north of Muztagh Ata, and 37 km northwest of Kongur Tagh.\n\n[Muztagh Ata]\nMuztagh Ata, or Muztagata (Uyghur: مۇز تاغ ئاتا, Музтаң Ата, literally \"ice-mountain-father\"; ), is the second highest (7509 metres) of the mountains which form the northern edge of the Tibetan Plateau (not the second highest of the mountains of the Tibetan Plateau).\n\n[Manaslu]\nManaslu (Nepali: मनास्लु, also known as Kutang) is the eighth highest mountain in the world at 8163 m above sea level.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q9bf2bdf858",
  "kind": "yes/no",
  "text": "Claim: Mills River is a tributary of the river that starts in the town of Brevard, in Transylvania County, North Carolina.\n\nPassages:\n\n[Mills River (North Carolina)]\nThe Mills River is located in Transylvania and Henderson counties, North Carolina, United States is a tributary of the French Broad River.\n\n[French Broad River]\nThe French Broad River flows 218 mi from near the town of Rosman in Transylvania County, North Carolina, into the state of Tennessee.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa59d7981e8",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Don't say \"dems in disarray,\" because they aren't.",
   "make it illegal to say/write \"Dems in disarray\" on account of it being stupid as fuck"
  ]
 },
 {
  "qid": "qf18782970d",
  "kind": "yes/no",
  "text": "Claim: The English crime writer Minette Walters wrote the 2005 psychological thriller \"The Devil's Feather\".\n\nPassages:\n\n[Minette Walters]\nMinette Walters (born 26 September 1949) is an English crime writer.\n\n[The Devil's Feather]\nThe Devil's Feather is a 2005 psychological thriller novel by British author Minette Walters.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q38fd947dd6",
  "kind": "yes/no",
  "text": "Claim: The star of The Big Caper was known for playing a fictionalized version of the wild politician who was the face of communist scare tact's in the early 1950's.\n\nPassages:\n\n[James Gregory (actor)]\nJames Gregory (December 23, 1911 – September 16, 2002) was an American character actor known for his deep, gravelly voice and playing brash roles such as the McCarthy-like Sen. John Iselin in \"The Manchurian Candidate\" (1962), the audacious General Ursus in \"Beneath the Planet of the Apes\" (1970), and crusty Inspector Frank Luger in the television sitcom \"Barney Miller\" (1975–1982).\n\n[The Big Caper]\nThe Big Caper is a 1957 crime drama film noir directed by Robert Stevens starring Rory Calhoun, Mary Costa and James Gregory\n\n[Joseph McCarthy]\nBeginning in 1950, McCarthy became the most visible public face of a period in the United States in which Cold War tensions fueled fears of widespread Communist subversion.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb2c06a709f",
  "kind": "yes/no",
  "text": "Claim: The 52nd Berlin International Film Festival opened with the Tom Tykwer horror movie that starred Catherine Elise Blanchett, an Australian actress who portrayed Katharine Hepburn in the 2004 film \"The Aviator\".\n\nPassages:\n\n[Heaven (2002 film)]\nHeaven is a 2002 romantic thriller film directed by Tom Tykwer, starring Cate Blanchett and Giovanni Ribisi.\n\n[Cate Blanchett]\nCatherine Elise Blanchett, {'1': \", '2': \", '3': \", '4': \"} ( ; born 14 May 1969) is an Australian actress and theatre director. Her portrayal of Katharine Hepburn in Martin Scorsese's 2004 film \"The Aviator\" brought her critical acclaim and many accolades, including the Academy Award for Best Actress in a Supporting Role, making her the only actor to win an Oscar for portraying another Oscar-winning actor.\n\n[52nd Berlin International Film Festival]\nThe festival opened with \"Heaven\" by Tom Tykwer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qee6a7dddc7",
  "kind": "yes/no",
  "text": "Claim: The critically acclaimed author of Bambi's Children: The Story of a Forest Family, originally titled his most famous work Bambi: Eine Lebensgeschichte aus dem Walde.\n\nPassages:\n\n[Bambi's Children]\nBambi's Children: The Story of a Forest Family (German: Bambis Kinder: Eine Familie im Walde ) is a novel written by Austrian author Felix Salten as a sequel to his successful work \"Bambi, A Life in the Woods\".\n\n[Bambi, a Life in the Woods]\nBambi, a Life in the Woods, originally published in Austria as Bambi: Eine Lebensgeschichte aus dem Walde is a 1923 Austrian novel written by Felix Salten and published by Ullstein Verlag.\n\n[Felix Salten]\nFelix Salten (6 September 1869 – 8 October 1945) was an Austrian author and critic in Vienna.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7651aec333",
  "kind": "yes/no",
  "text": "Claim: Gabby West won a competition on the reality show \"Scream Queens\". Her prize was a role in a movie starring Costas Mandylor. The movie had a video game released one week prior to its premier.\n\nPassages:\n\n[Saw 3D]\nSaw 3D (also known as Saw: The Final Chapter, or simply Saw VII) is a 2010 American 3D horror film directed by Kevin Greutert, written by Patrick Melton and Marcus Dunstan, and starring Tobin Bell, Costas Mandylor, Betsy Russell, Sean Patrick Flanery and Cary Elwes.\n\n[Saw II: Flesh &amp; Blood]\nIt was released in 2010 to coincide with the release of the seventh film, \"Saw 3D\", a week later.\n\n[Gabby West]\nShe won a role in \"Saw 3D\" in a competition on the reality show \"Scream Queens\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q075e497f68",
  "kind": "yes/no",
  "text": "Claim: The co-engineer of the album Ununiform released his 1996 Rolling Stone-rated \"500 Greatest\" album on Memphis-A-Fella Records and Priority Records.\n\nPassages:\n\n[Reasonable Doubt (album)]\nIt was released on June 25, 1996, by Roc-A-Fella Records and Priority Records.\n\n[Jay-Z]\nRolling Stone\" ranked three of his albums—\"Reasonable Doubt\" (1996), \"The Blueprint\" (2001), and \"The Black Album\" (2003)—among The 500 Greatest Albums of All Time.\n\n[Ununiform]\nAmerican hip hop artist Jay-Z co-engineered the album.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q19035c5d41",
  "kind": "yes/no",
  "text": "Claim: The father of the Princess Charlotte of Lorraine has a descendant that includes Umberto II the final king of Italy.\n\nPassages:\n\n[Charlotte of Lorraine]\nCharlotte de Lorraine-Armagnac (6 May 1678 – 21 January 1757) was a Princess of Lorraine by birth and daughter of Louis, Count of Armagnac.\n\n[Umberto II of Italy]\nUmberto II (Italian: \"Umberto Nicola Tommaso Giovanni Maria di Savoia\" ; 15 September 190418 March 1983), was the last King of Italy.\n\n[Louis, Count of Armagnac]\nHis descendants include Albert II, Prince of Monaco, Umberto II of Italy, and Diana Álvares Pereira de Melo, 11th Duchess of Cadaval.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q97d991217a",
  "kind": "yes/no",
  "text": "Claim: Hoop Dreams was released before LaLee's Kin: The Legacy of Cotton was.\n\nPassages:\n\n[Hoop Dreams]\nHoop Dreams is a 1994 American documentary film directed by Steve James and written by James and Frederick Marx, with Kartemquin Films.\n\n[LaLee's Kin: The Legacy of Cotton]\nLaLee's Kin: The Legacy of Cotton is a 2001 American documentary film directed by Deborah Dickson, Susan Frömke and Albert Maysles.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb628215efb",
  "kind": "yes/no",
  "text": "Claim: The writer and director of this film is Japanese. The film also starred Kari another actor. The film also starred Kari another actor. This actor also starred in Meteor Storm.\n\nPassages:\n\n[The Tree of Life (film)]\nThe Tree of Life is a 2011 American experimental epic drama film written and directed by Terrence Malick and featuring a cast of Brad Pitt, Sean Penn, Hunter McCracken, Laramie Eppler, Jessica Chastain, and Tye Sheridan in his debut feature film role.\n\n[Kari Matchett]\nShe has appeared in films such as \"Apartment Hunting\" (2000), \"Angel Eyes\" (2001), \"Men with Brooms\" (2002), \"Cypher\" (2002), \"Civic Duty\" (2006), \"The Tree of Life\" (2011), and \"Maudie\" (2016).\n\n[Terrence Malick]\nTerrence Frederick Malick ( ; born November 30, 1943) is an American film director, screenwriter and producer.\n\n[Meteor Storm]\nThe movie starred Michael Trucco and Kari Matchett.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0ef5153fb3",
  "kind": "yes/no",
  "text": "Claim: Thunbergia and Teucrium are not part of the same family.\n\nPassages:\n\n[Thunbergia]\nThunbergia is a genus of flowering plants in the family Acanthaceae, native to tropical regions of Africa, Madagascar and southern Asia.\n\n[Teucrium]\nTeucrium is a genus of mostly perennial plants in the family Lamiaceae.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q87c7c80593",
  "kind": "yes/no",
  "text": "Claim: Syngenta is a Swiss agribusiness that is a client of Martin Williams Advertising in NY.\n\nPassages:\n\n[Syngenta]\nSyngenta AG is a global Swiss agribusiness that produces agrochemicals and seeds.\n\n[Martin Williams Advertising]\nClients include Payless ShoeSource, Raymond James, Syngenta, Cargill, Marvin Windows, Simmons Bedding Company, and P.F. Chang.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5a8453292a",
  "kind": "yes/no",
  "text": "Post: i just saw the loveliest cat on the way home :)",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q86e7854c66",
  "kind": "yes/no",
  "text": "Claim: The younger brother of Harvey Jewell served as the national coordinator for the American Republican Party.\n\nPassages:\n\n[Harvey Jewell]\nHis younger brother, Marshall Jewell (1825-1883) would later be elected Governor of Connecticut and would serve as President Grant's United States Postmaster General.\n\n[Marshall Jewell]\nMarshall Jewell (October 20, 1825February 10, 1883) was a manufacturer, pioneer telegrapher, telephone entrepreneur, world traveler, and political figure who served as 44th and 46th Governor of Connecticut, the U.S. Minister to Russia, the 25th United States Postmaster General, and Republican Party National Chairman.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8eacea0031",
  "kind": "yes/no",
  "text": "Text: Wow. Liam Neeson is coming across as a rational man,isn't he!!?",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qfdd1c27186",
  "kind": "yes/no",
  "text": "Claim: Derrick Delite's rap was featured on the remix and video version of a song by an American singer that began her career as a cheerleader for The Wild Pair.\n\nPassages:\n\n[Paula Abdul]\nPaula Julie Abdul ( ; born June 19, 1962) is an American singer, songwriter, voice actress, dancer, choreographer, actress and television personality. She began her career as a cheerleader for the Los Angeles Lakers at the age of 18 before rising to prominence in the 1980s as a highly sought choreographer at the height of the music video era.\n\n[Derrick Stevens]\nDerrick Stevens (also known as Derrick ' Delite' Stevens) is a rapper and voice actor best known for lending his voice as MC Skat Kat after the character went solo. Derrick Delite's rap was featured on the remix and video version of Paula Abdul's \"Opposites Attract.\"",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qd7ad5143b9",
  "kind": "yes/no",
  "text": "Tweet: Some pretty great things are happening at the call center. Listen in to 104.5 for the Care-A-Thon! Each dollar is being matched, my friends!",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qf37acbe23f",
  "kind": "yes/no",
  "text": "Claim: Justin Bieber is the Canadian singer who was originally featured on the song \"Bankroll\" composed by American DJ Diplo.\n\nPassages:\n\n[Bankroll (song)]\nOriginally, Justin Bieber was featured on the song, but due to Bieber already having exclusives with DJ Khaled (\"I'm the One\") and David Guetta (\"2U\") at around the same time as Diplo released \"Bankroll\", Diplo was forced to remove the original from his SoundCloud account.\n\n[I'm the One (DJ Khaled song)]\n\"I'm the One\" is a song written and performed by American musician DJ Khaled; Canadian singer Justin Bieber; and American rappers Quavo, Chance the Rapper and Lil Wayne.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0cc825a79b",
  "kind": "yes/no",
  "text": "Tweet: Dating apps are like trying to find a snack in the fridge the day before your food shop; no matter how many times you lower your expectations, there are no snacks.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qb7cd042659",
  "kind": "yes/no",
  "text": "Claim: This area is located just north of a constituent college of the University of a city. It stands across from the Bear Inn in the city. Heinz Cassirer lectured and lived in the city.\n\nPassages:\n\n[Christ Church, Oxford]\nChrist Church (Latin: \"Ædes Christi\" , the temple or house, \"ædēs\", of Christ, and thus sometimes known as \"The House\") is a constituent college of the University of Oxford in England.\n\n[Bear Lane]\nThe lane is located just north of Christ Church.\n\n[Heinz Cassirer]\nFollowing Paton, he moved to Oxford, lecturing at Corpus Christi College.\n\n[Bear Inn, Oxford]\nIts circa-17th century incarnation stands on the corner of Alfred Street and Blue Boar Street, opposite Bear Lane in the centre of Oxford, just north of Christ Church.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q98e1ed11c8",
  "kind": "yes/no",
  "text": "Claim: The owner of Tatoosh (yacht) has a sister named Jo Lynn \"Jody\". He is an American business magnate, investor and philanthropist.\n\nPassages:\n\n[Paul Allen]\nPaul Gardner Allen (born January 21, 1953) is an American business magnate, investor and philanthropist.\n\n[Tatoosh (yacht)]\nTatoosh is a 303 ft private yacht owned by Paul Allen, who also owns the 416 ft \"Octopus\".\n\n[Jody Allen]\nShe is Microsoft co-founder billionaire Paul Allen's sister and served as the chief executive officer of his investment and project management company, Vulcan Inc., based in Seattle, Washington until October 2015.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qfe2f9b9a21",
  "kind": "yes/no",
  "text": "Claim: The Gujarat Lions are captained by this woman. She is the first youngest cricket captain to play in the 2016 Indian Premier League.\n\nPassages:\n\n[Gujarat Lions in 2017]\nThey are captained by Suresh Raina and coached by Brad Hodge.\n\n[Gujarat Lions in 2016]\nThey are one of the eight teams competing in the 2016 Indian Premier League. They are captained by Suresh Raina and coached by Brad Hodge.\n\n[Suresh Raina]\nHe has also captained the Indian cricket team and is the second-youngest player ever to captain India.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qafe04eac7f",
  "kind": "yes/no",
  "text": "Claim: The actor who starred in Massacre at Central High and Charles Burnett are both North American.\n\nPassages:\n\n[Andrew Stevens]\nAndrew Stevens (born June 10, 1955) is an American executive, film producer, director and actor.\n\n[Charles Burnett (director)]\nCharles Burnett (born April 13, 1944, in Vicksburg, Mississippi) is an African-American film director, film producer, writer, editor, actor, photographer, and cinematographer.\n\n[Massacre at Central High]\nMassacre at Central High is a 1976 American thriller film directed by Rene Daalder and starring Derrel Maury, Kimberly Beck, Robert Carradine, and Andrew Stevens.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9422bfc12e",
  "kind": "yes/no",
  "text": "Claim: Dennis Gansel is not from America. Neither is the director of action adventure film \"I Believed in You\".\n\nPassages:\n\n[Dennis Gansel]\nDennis Gansel (born 4 October 1973) is a film director, writer and actor from Germany.\n\n[I Believed in You]\nI Believed in You is a 1934 American drama film directed by Irving Cummings and written by William M. Conselman.\n\n[Irving Cummings]\nIrving Camisky (October 9, 1888 – April 18, 1959) was an American movie actor, director, producer and writer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qb7500f075c",
  "kind": "yes/no",
  "text": "Claim: The tour that Lungs Tour supported the band fronted by Bono in was a 2-year worldwide tour. It had a round stage and had a song that had never before been performed live.\n\nPassages:\n\n[Lungs Tour]\nThey also supported U2 on their U2 360° Tour in 2011.\n\n[Electrical Storm (song)]\nU2 did not play the song live until 2 July 2009, when they performed it on the second concert of their U2 360° Tour in Barcelona.\n\n[U2 360° Tour]\nThe U2 360° Tour was a worldwide concert tour by rock band U2. The concerts featured the band playing \"in the round\" on a circular stage, allowing the audience to surround them on all sides.\n\n[Bono]\nHe is best known as the lead vocalist and primary lyricist of rock band U2.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q858b7e8c97",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "This country is not a \"free\" country anymore.",
   "So, a country that is trillions in debt, with numbers approaching 13 million on surgical waiting lists and hurtling towards facism regime, is talking about rescuing people from a facist regime?"
  ]
 },
 {
  "qid": "q2b1cf3c209",
  "kind": "yes/no",
  "text": "Tweet: Thank god I just accidentally snapped a rando guy from high school ‘yas queen’ with acne cream all over my face",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qd7c24341c0",
  "kind": "yes/no",
  "text": "Claim: Sissy Spacek won an Academy Award for Best Actress for the Thomas Rickman film Coal Miner's Daughter.\n\nPassages:\n\n[Coal Miner's Daughter (film)]\nIt stars Sissy Spacek as Loretta, a role that earned her the Academy Award for Best Actress.\n\n[Thomas Rickman (writer)]\nThomas Rickman (sometimes credited as Tom Rickman) is an American film director and screenwriter known for such films as \"Coal Miner's Daughter\", \"Hooper\", \"Tuesdays with Morrie\" and \"Truman\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2fabb38689",
  "kind": "yes/no",
  "text": "Claim: Extract starred American actress Kristen Carroll Wiig who is notable for her work on Saturday Night Live from 2005-2012.\n\nPassages:\n\n[Kristen Wiig]\nKristen Carroll Wiig ( ; born August 22, 1973) is an American actress, comedian, writer, and producer. She is known for her work on the NBC sketch comedy series \"Saturday Night Live\" (2005–12), and such films as \"Bridesmaids\", \"The Martian\", and \"Ghostbusters\".\n\n[Extract (film)]\nExtract is a 2009 American comedy film written and directed by Mike Judge, and starring an ensemble cast featuring Jason Bateman, Mila Kunis, Kristen Wiig, and Ben Affleck, with J. K. Simmons, Clifton Collins, Jr., and Dustin Milligan.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qaf5200513f",
  "kind": "yes/no",
  "text": "Claim: The second promotional single from the album that contained \"State of Grace\" was released October 2, 2012 and failed to enter the Billboard Top 200.\n\nPassages:\n\n[State of Grace (Taylor Swift song)]\n\"State of Grace\" is a song by American singer-songwriter Taylor Swift from her fourth studio album \"Red\" (2012).\n\n[Red (Taylor Swift song)]\nIt was released on October 2, 2012, in the US by Big Machine Records as the second promotional single from \"Red\" in 2012 and serves as the album's fifth single on June 21, 2013.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q90e12022e5",
  "kind": "yes/no",
  "text": "Claim: The execution of Roger David Casement, the Irish Nationalist who made made efforts during World War I to gain German military aid for the 1916 Easter Rising that sought to gain Irish independence, took place in Casement's Fort.\n\nPassages:\n\n[Rahoneen]\nIt is notable as the location of an ancient Celtic ringfort; at one time this was known as McKenna's fort, but, after the capture and execution of Roger Casement for treason, sabotage and espionage against the Crown, it became known as Casement's Fort. \"Too weak to travel, he was discovered at McKenna's Fort where he had hidden after arranging delivery of German weapons as part of a plan of arming Irish rebels and creating a rising in 1916 against the British to achieve independence.\n\n[Roger Casement]\nDescribed as the \"father of twentieth-century human rights investigations\", he was honoured in 1905 for the Casement Report on the Congo and knighted in 1911 for his important investigations of human rights abuses in Peru.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q86d323e813",
  "kind": "yes/no",
  "text": "Claim: MGM Resorts International was the company that started the urban complex development that included the highrise building, The Harmon.\n\nPassages:\n\n[The Harmon]\nThe Harmon was a highrise building at the CityCenter development in Paradise, Nevada.\n\n[CityCenter]\nThe project was started by MGM Resorts International; Dubai World became a joint partner during the project's construction phase.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0561f38b18",
  "kind": "yes/no",
  "text": "Claim: The show, in which the host of this show also hosted, usually aired on Monday at 7 pm. Rosie Goldsmith hosted it, as well as Crossing Continents.\n\nPassages:\n\n[Rosie Goldsmith]\nShe was the host of the shows Crossing Continents, and A World in Your Ear.\n\n[The Krypton Factor]\nThe show originally ran from 7 September 1977 to 20 November 1995, and was hosted by Gordon Burns and usually broadcast on the ITV network on Mondays at 7pm.\n\n[Gordon Burns]\nHe was the host of \"The Krypton Factor\" for its original 18-year run (1977–1995) and was the chief anchorman for the BBC regional news programme \"North West Tonight\" from January 1997 to October 2011.\n\n[A Word in Your Ear]\nIt was hosted by Gordon Burns.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6ac71162ef",
  "kind": "yes/no",
  "text": "Claim: The former 10th congressional district of Minnesota is now currently represented by Californian Erik Paulsen in the US House of Representatives.\n\nPassages:\n\n[Minnesota's 3rd congressional district]\nRepublican Erik Paulsen currently represents the district in the U.S. House of Representatives, having been elected in 2008.\n\n[Minnesota's 10th congressional district]\nIt generally consisted of the current 3rd and 6th districts and the southern portion of the 8th district.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe72e579913",
  "kind": "yes/no",
  "text": "Claim: Jefferson Memorial is the name of the presidential bridge in Washington, D.C that connects to an artificial island.\n\nPassages:\n\n[Jefferson Memorial]\nThe Jefferson Memorial is a presidential memorial in Washington, D.C., dedicated to Thomas Jefferson (1743–1826), one of the most important of the American Founding Fathers as the main drafter and writer of the Declaration of Independence, member of the Continental Congress, governor of the newly independent Commonwealth of Virginia, American minister to King Louis XVI and the Kingdom of France, first U.S. Secretary of State under the first President George Washington, the second Vice President of the United States under second President John Adams, and also the third President (1801–1809), as well as being the founder of the University of Virginia at Charlottesville, Virginia.\n\n[Hains Point]\nThe island is artificial: it was built up from Potomac dredging material from 1880 to 1892.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q89507e7519",
  "kind": "yes/no",
  "text": "Claim: The BBC drama Silk would be referenced in the biographical television film, Hancock and Joan.\n\nPassages:\n\n[Maxine Peake]\nShe has since played Veronica Ball in Channel 4's Manchester-based comedy drama series \"Shameless\", barrister Martha Costello in the BBC legal drama \"Silk\" and Grace Middleton in \"The Village\".\n\n[Hancock and Joan]\nHancock and Joan is a 2008 British biographical television film based on the affair between the comedian Tony Hancock and Joan Le Mesurier, the third wife of actor John Le Mesurier.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6221c11055",
  "kind": "yes/no",
  "text": "Claim: The graphic novel author wrote fiction published by Arkham House. He died at an earlier day than the man who theorized the Eight-circuit model of consciousness.\n\nPassages:\n\n[H. P. Lovecraft]\nHoward Phillips Lovecraft ( ; August 20, 1890 – March 15, 1937) was an American author who achieved posthumous fame through his influential works of horror fiction.\n\n[Timothy Leary]\nTimothy Francis Leary (October 22, 1920 – May 31, 1996) was an American psychologist and writer known for advocating the exploration of the therapeutic potential of psychedelic drugs under controlled conditions.\n\n[Arkham House]\nArkham House is a publishing house specializing in weird fiction founded in Sauk City, Wisconsin in 1939 by August Derleth and Donald Wandrei to preserve in hardcover the best fiction of H. P. Lovecraft.\n\n[Eight-circuit model of consciousness]\nThe Eight-Circuit Model of Consciousness is a hypothesis by Timothy Leary, and later expanded on by Robert Anton Wilson and Antero Alli, that \"suggested eight periods [circuits] and twenty-four stages of neurological evolution\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qbaf31af04e",
  "kind": "yes/no",
  "text": "Text: I need a line of duty convention LOL I would go NUTS and I’d think everything was reasonably priced bc of what I have to compare it to 😂😂😂😂😩😩😩",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q077bb30e5d",
  "kind": "yes/no",
  "text": "Claim: Sherwood Stewart was born before the participant of the 1993 Movistar Open singles competition.\n\nPassages:\n\n[Sherwood Stewart]\nSherwood Stewart (born June 6, 1946, in Goose Creek, Texas, United States) played amateur and professional tennis in the 1970s and 1980s.\n\n[1993 Movistar Open – Singles]\nJavier Frana defeated Emilio Sánchez 7–5, 3–6, 6–3 to win the 1993 Movistar Open singles competition.\n\n[Javier Frana]\nJavier Alberto Frana (born 25 December 1966) is a former tennis player from Argentina and current tennis commentator for ESPN Latin America.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q525f9fd3df",
  "kind": "yes/no",
  "text": "Claim: All That is the show that the co-creator with the host of Vibe and Wild 'N Out had a debut on.\n\nPassages:\n\n[Vibe (talk show)]\nPremiering in August 1997, it was produced by Quincy Jones, hosted by Chris Spencer, and featured President Bill Clinton on its first episode.\n\n[Chris Spencer (actor)]\nChris is also one of the most sought after writers having done projects with Wayans family, Jamie Foxx, and was significant in helping Nick Cannon create MTV's \"Wild 'N Out\".\n\n[Nick Cannon]\nNicholas Scott \"Nick\" Cannon (born October 8, 1980) is an American rapper, actor, comedian, director, screenwriter, film producer, entrepreneur, record producer, radio and television personality. On television, Cannon began as a teenager on \"All That\" before going on to host \"The Nick Cannon Show\", \"Wild 'N Out\", and \"America's Got Talent\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q2f31763f6d",
  "kind": "yes/no",
  "text": "Tweet: @BBCAMERICA Thanks for disrupting your narrative continuity with commercial break previews. #SpoilerAlert",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q48a4913262",
  "kind": "yes/no",
  "text": "Claim: The German project Enigma recorded a song that featured vocals by a duo from Silverdale, England.\n\nPassages:\n\n[Amen (Enigma song)]\n\"Amen\" is a song by German musical project Enigma, featuring vocals by English dream-pop duo Aquilo.\n\n[Aquilo (band)]\nAquilo is an alternative musical duo from Silverdale, Lancashire, England, consisting of Tom Higham and Ben Fletcher.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q2ff0aec444",
  "kind": "yes/no",
  "text": "Claim: Bindy Johal of the Beeba Boys died of cancer in 1998.\n\nPassages:\n\n[Beeba Boys]\nBeeba Boys is a 2015 Canadian crime thriller film written and directed by Deepa Mehta. The film is a fictional take based on real incidents, including Bindy Johal.\n\n[Bindy Johal]\nOn December 20, 1998, he was killed from behind at a crowded nightclub in Vancouver, British Columbia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 }
]
