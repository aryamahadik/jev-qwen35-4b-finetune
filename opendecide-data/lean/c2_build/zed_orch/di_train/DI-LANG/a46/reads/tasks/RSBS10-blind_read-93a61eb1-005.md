# A46 replay label-noise blind read RSBS10-blind_read-93a61eb1-005

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS10-blind_read-93a61eb1-005.json

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
  "qid": "q9d34d1af76",
  "kind": "yes/no",
  "text": "Claim: This individual was enlisted as vocalist on 1998's Rough and Ready (album). He and Marilyn Manson are both songwriters.\n\nPassages:\n\n[Marilyn Manson]\nBrian Hugh Warner (born January 5, 1969), known professionally as Marilyn Manson, is an American singer, songwriter, musician, composer, actor, painter, author and former music journalist.\n\n[Bobby Tench]\nRobert Tench also known as Bobby Tench, is a British vocalist, guitarist, sideman, songwriter and arranger.\n\n[Rough and Ready (album)]\nBeck enlisted Bobby Tench as vocalist and it is also the first time keyboardist Max Middleton is heard.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q02e6e44f08",
  "kind": "yes/no",
  "text": "Claim: Marvel Classics Comics specialized in adaptations of literary classics, such as a novel by American writer Herman Melville, that was published in Canada in 1851.\n\nPassages:\n\n[Marvel Classics Comics]\nIt specialized in adaptations of literary classics such as \"Moby-Dick\", \"The Three Musketeers\", and \"The Iliad\".\n\n[Moby-Dick]\nMoby-Dick; or, The Whale is a novel by American writer Herman Melville, published in 1851 during the period of the American Renaissance.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa48618c965",
  "kind": "yes/no",
  "text": "Claim: The author of The Lost World (Crichton novel) is not an actor. McG is also not an American actor.\n\nPassages:\n\n[McG]\nJoseph McGinty Nichol (born August 9, 1968), known mononymously as McG, is an American director, producer, and former record producer.\n\n[The Lost World (Crichton novel)]\nThe Lost World is a techno thriller novel written by Michael Crichton and published in 1995 by Knopf.\n\n[Michael Crichton]\nJohn Michael Crichton ( ; October 23, 1942 – November 4, 2008) was an American best-selling author, screenwriter, film director and producer best known for his work in the science fiction, medical fiction and thriller genres.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q577d0fc54a",
  "kind": "yes/no",
  "text": "Claim: William Michael Albert Broad, not the person who started \"Ascension of The Watchers\", is known professionally as Billy Idol.\n\nPassages:\n\n[Ascension of the Watchers]\nAscension of The Watchers is a band that was started by Burton C. Bell (Fear Factory, G/Z/R) and John Bechdel (Ministry, Fear Factory, Killing Joke, Prong, Murder, Inc.).\n\n[Burton C. Bell]\nBurton Christopher Bell (born February 19, 1969) is an American musician and vocalist.\n\n[Billy Idol]\nWilliam Michael Albert Broad (born 30 November 1955), known professionally as Billy Idol, is an English musician, singer, songwriter, and actor.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd41011d9cd",
  "kind": "yes/no",
  "text": "Claim: The academic publication responsible for the Global Open Access Forum was published before Dwell.\n\nPassages:\n\n[Global Open Access Forum]\nIt was created by the American Scientist, which is published by Sigma Xi, in September 1998, before the term \"Open Access\" (OA) was coined, and it was originally called the \"September98-Forum.\"\n\n[American Scientist]\nAmerican Scientist (informally abbreviated AmSci) is an American bimonthly science and technology magazine published since 1913 by Sigma Xi, The Scientific Research Society.\n\n[Dwell (magazine)]\nIt was launched with a magazine in September 2000 to bridge the gap between design professionals and enthusiasts by Lara Hedberg Deam with architecture and design critic Karrie Jacobs as its Editor-in-Chief.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc3af54bd10",
  "kind": "yes/no",
  "text": "Claim: French schoolteacher and publisher was the occupation of the man who published an individualist anarchist journal.\n\nPassages:\n\n[Lucifer the Lightbearer]\nLucifer the Lightbearer was an individualist anarchist journal published by Moses Harman in the late 19th and early 20th centuries.\n\n[Moses Harman]\nMoses Harman (October 12, 1830January 30, 1910) was an American schoolteacher and publisher notable for his staunch support for women's rights.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q596613525b",
  "kind": "yes/no",
  "text": "Claim: Jo Ann Terry won the 80m hurdles event at the Pan American Games, a Mexico City-based event from 1963.\n\nPassages:\n\n[Jo Ann Terry]\nAffiliated with the Tennessee State University she won the 80 m hurdles event at the 1963 Pan American Games.\n\n[1963 Pan American Games]\nThe 4th Pan American Games were held from April 20 to May 5, 1963, in São Paulo, Brazil.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q00f3a9a013",
  "kind": "yes/no",
  "text": "Post: Well done @WestHam and @premierleague, great leadership! https://t.co/4IPXaK0Jpu",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q75f84956f3",
  "kind": "yes/no",
  "text": "Claim: The City of Blue Mountains local government area containing the town of Winmalee is located in the Blue Mountain range west of Sydney.\n\nPassages:\n\n[City of Blue Mountains]\nThe city is located in the Blue Mountains range west of Sydney.\n\n[Winmalee, New South Wales]\nWinmalee is located 80 kilometres west of Sydney, in the local government area of the City of Blue Mountains.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc7389a7eed",
  "kind": "yes/no",
  "text": "Claim: William Sydney Robinson principally owns the parent company of Hindustan Zinc Limited.\n\nPassages:\n\n[Vedanta Resources]\nThe company is principally owned by Indian billionaire Anil Agarwal through Volcan Investments, a holding vehicle with a 61.7% stake in the business.\n\n[Hindustan Zinc]\nIt is a subsidiary of Vedanta Resources PLC.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9ac16a9453",
  "kind": "yes/no",
  "text": "Claim: The brand where Lauren Gold, who is most recognised as the DJ in Robbie Williams's \"Rock DJ\" music video, is currently owned by a fashion retailer based in Columbus, Ohio.\n\nPassages:\n\n[L Brands]\nL Brands Inc. (formerly known as \"Limited Brands Inc\" and \"The Limited Inc.\") is an American fashion retailer based in Columbus, Ohio.\n\n[La Senza]\nThe La Senza brand is currently owned by L Brands which operates and owns La Senza stores in Canada and uses a franchise model for the operation of stores outside Canada.\n\n[Lauren Gold]\nGold is most recognised as the DJ in Robbie Williams's \"Rock DJ\" music video as well as her recurring appearance in La Senza ad campaigns.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6dfd44370e",
  "kind": "yes/no",
  "text": "Text: Watching Vivo at 4.30 for first time, my 6 year old already knows the soundtrack as she loves @Lin_Manuel I'm pretty impressed!",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q09e947e516",
  "kind": "yes/no",
  "text": "Claim: The 2000 French crime thriller starred the writer and director Virginie Despentes and Coralie Trinh Thi.\n\nPassages:\n\n[Baise-moi]\nBaise-moi (\"Fuck me \") is a 2000 French crime thriller film with elements of a rape and revenge film written and directed by Virginie Despentes and Coralie Trinh Thi and starring Karen Lancaume and Raffaëla Anderson.\n\n[Coralie Trinh Thi]\nCoralie Trinh Thi (born April 11, 1976) is a former pornographic actress and French author, also known for writing and directing with Virginie Despentes the film \"Baise-moi\" (2000).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qee3c1895b4",
  "kind": "yes/no",
  "text": "Claim: The band which released the record \"Son of Mustang Ford\" was formed before Incubus.\n\nPassages:\n\n[Incubus (band)]\nThe band was formed in 1991 by vocalist Brandon Boyd, lead guitarist Mike Einziger, and drummer Jose Pasillas while enrolled in Calabasas High School and later expanded to include bassist Alex \"Dirk Lance\" Katunich, and Gavin \"DJ Lyfe\" Koppell; both of whom were eventually replaced by bassist Ben Kenney and DJ Kilmore respectively.\n\n[Swervedriver]\nSwervedriver are an English alternative rock band formed in Oxford in 1989 around core members Adam Franklin and Jimmy Hartridge.\n\n[Son of Mustang Ford]\nSon of Mustang Ford is the debut EP by English alternative rock band, Swervedriver.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9be2076778",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "@MarkHendyHR Only joking... keep it real. HR professionals have a life too... 🤔",
   "Only joking. Keep it real. HR professionals don’t have a life."
  ]
 },
 {
  "qid": "qb9412a7b2b",
  "kind": "yes/no",
  "text": "Claim: This film producer produced Mickey, Donald, Goofy: The Three Musketeers. It also produced the 1999 film that National Treasure: Book of Secrets is a sequel to and The Computer Wore Tennis Shoes.\n\nPassages:\n\n[Mickey, Donald, Goofy: The Three Musketeers]\nThis film was directed by Donovan Cook, produced by Walt Disney Pictures and DisneyToon Studios, and released directly to VHS and DVD on August 17, 2004, by Walt Disney Studios Home Entertainment, and was later re-released on Blu-ray Disc on August 12, 2014, coinciding with the film's 10th anniversary.\n\n[National Treasure: Book of Secrets]\nIt is a sequel to the 2004 film \"National Treasure\" and is the second part of the \"National Treasure\" franchise.\n\n[The Computer Wore Tennis Shoes]\nIt was produced by Walt Disney Productions and distributed by Buena Vista Distribution Company as part of \"The Last Laughs of the 1960s\".\n\n[National Treasure (film)]\nNational Treasure is a 2004 American adventure heist film produced and released by Walt Disney Pictures.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q728d5a2ee9",
  "kind": "yes/no",
  "text": "Text: did you actually fly on a plane if you didn’t post a picture of the view from your window?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q519c2d12a4",
  "kind": "yes/no",
  "text": "Claim: This 2010 American comedy-drama film stars an American actor born July 26, 1959. Danny Comden also stars in it.\n\nPassages:\n\n[Father of Invention]\nFather of Invention is a 2010 American comedy-drama film directed by Trent Cooper, and stars Kevin Spacey, Camilla Belle and Johnny Knoxville.\n\n[Kevin Spacey]\nKevin Spacey Fowler, KBE (born July 26, 1959) is an American actor, film director, producer, screenwriter, and singer.\n\n[Danny Comden]\nHe also appeared in \"Father of Invention\", \"Dunston Checks In\", \"Breakin' All the Rules\" and \"Dirt.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6ff259b984",
  "kind": "yes/no",
  "text": "Claim: Actress, Rashi Bunny, appeared in a Bollywood movie based on a novella written by Antoine de Saint-Exupéry in 1943.\n\nPassages:\n\n[Rashi Bunny]\nRashi Bunny (Hindi: राशी बनी ) is an Indian theatre and cinema actress. She has performed in Bhisham Sahni's \"Madhavi\", Manjula Padmanabhan's Hidden Fires, and Antoine de Saint-Exupéry's \"The Little Prince\" with director Arvind Gaur. Rashi Bunny was selected as \"one of the 50 Icons: Emerging personality of India\" by Sahara India group with Rahul Gandhi. Rashi Bunny also known for \"I have a dream\" theatre workshop for self-exploration and creative expression.\n\n[The Little Prince]\nThe Little Prince (French: \"Le Petit Prince\"; ] ), first published in 1943, is a novella, the most famous work of French aristocrat, writer, poet, and pioneering aviator Antoine de Saint-Exupéry.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q77ef6b1dc1",
  "kind": "yes/no",
  "text": "Claim: No One Would Tell is based on the true story of Jamie Fuller, who murdered his girlfriend of three years in a city in Essex County, Massachusetts, with a population of 39,502.\n\nPassages:\n\n[Beverly, Massachusetts]\nBeverly is a city in Essex County, Massachusetts, United States. The population was 39,502 at the 2010 census.\n\n[No One Would Tell]\nIt is based on the true story of Jamie Fuller, a 16-year-old high school student who murdered his 14-year-old girlfriend, Amy Carnevale, on August 23, 1991, in Beverly, Massachusetts.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qbffcf60810",
  "kind": "yes/no",
  "text": "Claim: Greatest Hits Volume 1 is a greatest hits compilation album by The Beatles which was exclusive to Australia and New Zealand released in 1984, the album was compiled by EMI Australia to fill in the gap, much like A Collection of Beatles Oldies (subtitled But Goldies!)\n\nPassages:\n\n[A Collection of Beatles Oldies]\nA Collection of Beatles Oldies (subtitled But Goldies!)\n\n[Greatest Hits Volume 1 (Beatles album)]\nThe album was compiled by EMI Australia to fill in the gap between \"Rubber Soul\" and \"Revolver\" (much like \"A Collection of Beatles Oldies\" would in 1966 in between \"Revolver\" and \"Sgt. Pepper's Lonely Hearts Club Band\").",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4ff45eaf23",
  "kind": "yes/no",
  "text": "Claim: A fictional character is featured by the P.L.Travers's third book and last novel in the Mary Poppins series.\n\nPassages:\n\n[Mary Poppins (character)]\nMary Poppins is a fictional character and the eponymous protagonist of P. L. Travers' \"Mary Poppins\" books and all of their adaptations.\n\n[Mary Poppins Opens the Door]\nMary Poppins Opens the Door is a British children's fantasy novel by the Australian-British writer P.L. Travers, the third book and last novel in the \"Mary Poppins\" series that features the magical English nanny Mary Poppins.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q0348a309f5",
  "kind": "yes/no",
  "text": "Claim: The NFL football team that plays its home matches in New York that Nevil McCaskill played for is the Buffalo Bills.\n\nPassages:\n\n[Buffalo Bills]\nThe Bills are the only NFL team that plays its home games in the state of New York (the New York Giants and New York Jets play at MetLife Stadium, located in East Rutherford, New Jersey).\n\n[Nevin McCaskill]\nHe was signed by the Buffalo Bills as an undrafted free agent in 2007.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q69c2faf25f",
  "kind": "yes/no",
  "text": "Claim: Louder Than Bombs is the 2015 internationally co-produced drama film directed by Joachim Trier that was produced in 2015. The producer was the son of a. The producer was the son of a director. The director directed Begynnelsen på en historie.\n\nPassages:\n\n[Louder Than Bombs (film)]\nLouder Than Bombs is a 2015 internationally co-produced drama film directed by Joachim Trier, and co-written with Eskil Vogt.\n\n[Begynnelsen på en historie]\nBegynnelsen på en historie (English: The beginning of a story ) is a 1988 Norwegian drama film directed by Margarete Robsahm, starring Linda Pedersen, Wenche Foss and Linn Stokke.\n\n[Margarete Robsahm]\nShe is the mother of director Thomas Robsahm and sister of the actor Fred Robsahm.\n\n[Thomas Robsahm]\nIn 2015 he produced the film \"Louder Than Bombs\" by Joachim Trier.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc6d30cb1bd",
  "kind": "yes/no",
  "text": "Post: @Mike_Fabricant This aged well",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q7f87da8f0c",
  "kind": "yes/no",
  "text": "Text: i had a dream nev from catfish tried to murder me",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qa24b73baaf",
  "kind": "yes/no",
  "text": "Text: my hobbies include leaving projects for the night before and then complaining that the teacher didn't give us enough time 🙃🙃",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qd38fc0c225",
  "kind": "yes/no",
  "text": "Text: @RangersFC Well done 👍",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q58122a7f73",
  "kind": "yes/no",
  "text": "Claim: The 2010 Insight Bowl was the 22nd edition, of the college football bowl game, played at Sun Devil Stadium in Tempe, Arizona on Tuesday, December 28, 2010, it featured the 2010 Missouri Tigers football team that represented the University of Missouri, in the 2010 NCAA Division I FBS football season and the game ended in a draw.\n\nPassages:\n\n[2010 Insight Bowl]\nIt featured the Missouri Tigers from the Big 12 Conference versus the Iowa Hawkeyes from the Big Ten Conference.\n\n[2010 Missouri Tigers football team]\nThe 2010 Missouri Tigers football team represented the University of Missouri in the 2010 NCAA Division I FBS football season.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q67a2c64621",
  "kind": "yes/no",
  "text": "Claim: The fifth studio album by English musician that guitarist George Harrison released as the follow-up to the album that was certified gold by the Recording Industry Association of America two days after release, was Dark Horse.\n\nPassages:\n\n[Living in the Material World]\nThe album was certified gold by the Recording Industry Association of America two days after release, on its way to becoming Harrison's second number 1 album in the United States, and produced the international hit \"Give Me Love (Give Me Peace on Earth)\".\n\n[Dark Horse (George Harrison album)]\nDark Horse is the fifth studio album by English musician George Harrison, released on Apple Records in December 1974 as the follow-up to \"Living in the Material World\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q0dbd61c9a4",
  "kind": "yes/no",
  "text": "Tweet: Don't let people walk all over you. Or breathe on you. Either one.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q4344509d25",
  "kind": "yes/no",
  "text": "Claim: Hariharan Pillai Happy Aanu contains music by the arranger Stephen Devassy from Kerala.\n\nPassages:\n\n[Stephen Devassy]\nStephen Devassy (Malayalam:സ്റ്റീഫൻ ദേവസ്സി, born 23 February 1981) is a musician hailing from Palakkad, Kerala.\n\n[Hariharan Pillai Happy Aanu]\nThis was Viswanathan's debut film as a director and the debut music directorial venture of renowned pianist and arranger, Stephen Devassy.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q94520f1f28",
  "kind": "yes/no",
  "text": "Claim: John Spalvins, born David Jones, in 1936, in Latvia, was Managing Director of the Adelaide Steamship Company from 1977 until the company's collapse in 1991, it was formed by a group of South Australian businessmen in 1875.\n\nPassages:\n\n[John Spalvins]\nJohn Spalvins, born Janis Gunnars Spalvins, in 1936, in Latvia, was Managing Director of the Adelaide Steamship Company from 1977 until the company's collapse in 1991.\n\n[Adelaide Steamship Company]\nThe Adelaide Steamship Company was formed by a group of South Australian businessmen in 1875.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q62b540c6be",
  "kind": "yes/no",
  "text": "Claim: The genus that includes Disporum viridescens has more species than Boltonia.\n\nPassages:\n\n[Boltonia]\nBoltonia is a genus of plants in the sunflower family native primarily to North America with one species in eastern Asia.\n\n[Disporum]\nDisporum (commonly known as fairy bells) is a genus of about 20 species of perennial flowering plants, found in Asia from northern India to Japan, south to Indonesia and north into the Russian Far East.\n\n[Disporum viridescens]\nDisporum viridescens is a species of flowering plant in the genus \"Disporum\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6d3648ecb5",
  "kind": "yes/no",
  "text": "Claim: Director of The Object of My Affection and Maya Deren never worked in the same role in the film industry.\n\nPassages:\n\n[Nicholas Hytner]\nSir Nicholas Robert Hytner (born 7 May 1956) is an English theatre director, film director, and film producer.\n\n[The Object of My Affection]\nThe film is directed by Nicholas Hytner, and the screenplay was written by Wendy Wasserstein.\n\n[Maya Deren]\nMaya Deren (April 29, 1917 – October 13, 1961), born Eleanora Derenkowskaia (Russian: Элеоно́ра Деренко́вская ), was a Russian-American filmmaker and one of the most important American experimental filmmakers and entrepreneurial promoters of the avant-garde in the 1940s and 1950s. Deren was also a choreographer, dancer, film theorist, poet, lecturer, writer and photographer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa34a7bff62",
  "kind": "yes/no",
  "text": "Tweet: as much as i like being home i miss my uni pals and messing around in the kitchen at 2am",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q5ee5a0161d",
  "kind": "yes/no",
  "text": "Claim: The writer Renascence (poem) of and the author whose second novel is At Heaven's Gate are both Pulitzer Prize-winners. They both won prizes for their poetry.\n\nPassages:\n\n[Edna St. Vincent Millay]\nShe received the Pulitzer Prize for Poetry in 1923, the third woman to win the award for poetry, and was also known for her feminist activism.\n\n[Renascence (poem)]\n\"Renascence\" (also \"Renasance\") is a 1912 poem by Edna St. Vincent Millay, credited with introducing her to the wider world, and often considered one of her finest poems.\n\n[At Heaven's Gate]\nAt Heaven's Gate is the second novel by Robert Penn Warren.\n\n[Robert Penn Warren]\nHe received the 1947 Pulitzer Prize for the Novel for his novel \"All the King's Men\" (1946) and the Pulitzer Prize for Poetry in 1958 and 1979. He is the only person to have won Pulitzer Prizes for both fiction and poetry.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q3b7278c4d0",
  "kind": "yes/no",
  "text": "Claim: The band who Strange Talk are likened to and Shearwater do not specialize in the exact same genre.\n\nPassages:\n\n[Strange Talk]\nFormed in 2010, their sound has been likened to that of Cut Copy, Passion Pit, Phoenix and Yeasayer.\n\n[Shearwater (band)]\nShearwater is an American indie rock band from Austin, Texas, led by multi-instrumentalist and lead singer Jonathan Meiburg, a singer-songwriter.\n\n[Phoenix (band)]\nPhoenix is an indie pop band from Versailles, France, consisting of Thomas Mars (lead vocals), Deck d'Arcy (bass/ keyboards/ backing vocals), Christian Mazzalai (guitar/ keyboards/ backing vocals) and Laurent Brancowitz (guitar/ backing vocals).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3eb341f02e",
  "kind": "yes/no",
  "text": "Claim: This person, who contributed artwork to the 2008-2009 Superman: New Krypton story, was known for illustrative work on a DC Comics publication titled Firestorm.\n\nPassages:\n\n[Firestorm (comics)]\nFirestorm is the name of several fictional superheroes appearing in American comic books published by DC Comics.\n\n[Superman: New Krypton]\n\"New Krypton\" is a 2008-2009 Superman story arc written by Geoff Johns, James Robinson, and Sterling Gates with art by Gary Frank, Alex Ross, Renato Guedes, Jamal Igle and Pete Woods and published by DC Comics.\n\n[Jamal Igle]\nThe creator of the comic book series Molly Danger he is also known for his pencilling, inking and coloring work on books such as \"Supergirl\" and \"Firestorm\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q59e2759f10",
  "kind": "yes/no",
  "text": "Text: Teachers are such precious gems",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qfd37c14400",
  "kind": "yes/no",
  "text": "Claim: The defending champions of the 1999 Challenge Bell – Doubles were Lori McNeil and her partner. Her partner is younger than Joakim Nystrom.\n\nPassages:\n\n[Joakim Nyström]\nJoakim \"Jocke\" Nyström (born 20 February 1963) is a former top ten ranked tennis player from Sweden who won 13 singles titles during his professional career.\n\n[1999 Challenge Bell – Doubles]\nLori McNeil and Kimberly Po were the defending champions, but lost in the quarterfinals to Amy Frazier and Katie Schlukebir.\n\n[Kimberly Po]\nKimberly Po-Messerli (born October 20, 1971) is a former professional tennis player from the United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qbcdb06dd9a",
  "kind": "yes/no",
  "text": "Claim: The class Jodie Esquibel competes professionally in belongs to mixed martial arts.\n\nPassages:\n\n[Liz McCarthy (fighter)]\nLiz McCarthy is an American mixed martial artist who competes in the Atomweight division.\n\n[Jodie Esquibel]\nJodie Esquibel is an American mixed martial artist who competes in the Atomweight division.\n\n[Atomweight (MMA)]\nThe atomweight division in mixed martial arts generally refers to competitors weighing at or less than 105 lb .",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q5985abe05b",
  "kind": "yes/no",
  "text": "Post: Republicans have nobody to blame but themselves.  They allowed this to happen. https://t.co/wkvmsb6LFo",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qf16be8120d",
  "kind": "yes/no",
  "text": "Post: how old were u when u found out omaha steaks wasn't a restaurant",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qa2f7356b91",
  "kind": "yes/no",
  "text": "Claim: Jane Mayer is writing a book about the billionaires who funded Citizens United (organization) and who control the on of the largest privately owned companies in the United States.\n\nPassages:\n\n[Dark Money (book)]\nDark Money: The Hidden History of the Billionaires Behind the Rise of the Radical Right (2016) is a non-fiction book written by the American investigative journalist Jane Mayer, about a network of extremely wealthy conservative libertarians, foremost among them Charles and David Koch, who have together funded an array of organizations that work in tandem to influence academic institutions, think tanks, the courts, statehouses, Congress, and the American presidency for their own benefit.\n\n[Koch family]\nThe Koch family ( ) is an American family engaged in business, most noted for their political activities and control of Koch Industries, the second-largest privately owned company in the United States (with 2013 revenues of $115 billion).\n\n[Citizens United (organization)]\nCitizens United is a conservative 501(c)(4) non-profit organization in the United States started in 1988 with major funding from the billionaire Koch family.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qc5429d2aa4",
  "kind": "yes/no",
  "text": "Post: but clinton's emails!\noh.\nemm.\nfucking.\ngee.\n\nclinton's god damnèd emails.\n\nthe humanity of it all.\n\n🤮 https://t.co/cibY5Tn9s6",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q51aff991c2",
  "kind": "yes/no",
  "text": "Claim: The Yule goat, which has become more or less conflated with Santa Claus, is a Finnish Christmas figure that has modern representations typically made of straw.\n\nPassages:\n\n[Joulupukki]\nJoulupukki is a Finnish Christmas figure. An old Scandinavian custom, the figure eventually became more or less conflated with Santa Claus.\n\n[Yule Goat]\nThe Yule goat is a Scandinavian and Northern European Yule and Christmas symbol and tradition. Modern representations of the Yule goat are typically made of straw.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q91827d3a83",
  "kind": "yes/no",
  "text": "Claim: The Danish singer Lucky Yates is known for his voice-over roles as Dr. Krieger on a spy sitcom created by Adam Reed.\n\nPassages:\n\n[Archer (TV series)]\nArcher is an American adult animated spy sitcom created by Adam Reed for the FX network.\n\n[Lucky Yates]\nHe is known for his voice-over roles as Dr. Krieger on \"Archer\" and The Xtacles on \"Frisky Dingo\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q36a303fc85",
  "kind": "yes/no",
  "text": "Tweet: Blatantly obvious that Lionel Messi is now set for a move to Leeds.\n\nThe Newell’s old boys network.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q00d391a8d3",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I do not like the certified lover boy artwork",
   "CLB cover art makes me want to pound my knees with a hammer."
  ]
 }
]
