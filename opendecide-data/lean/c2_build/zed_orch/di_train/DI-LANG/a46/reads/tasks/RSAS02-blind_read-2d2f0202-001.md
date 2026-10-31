# A46 replay label-noise blind read RSAS02-blind_read-2d2f0202-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS02-blind_read-2d2f0202-001.json

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
  "qid": "q5d5ad0e586",
  "kind": "yes/no",
  "text": "Claim: Laima is the Baltic goddess of fate often confused with the goddess of fate in the Moros mythology.\n\nPassages:\n\n[Laima]\nLaima is a Baltic goddess of fate.\n\n[Dalia (mythology)]\nDalia is the goddess of fate in the Lithuanian mythology. Dalia is often confused with and hard to distinguish from Laima, another goddess of fate.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6c8f63d146",
  "kind": "yes/no",
  "text": "Claim: Director James Searle Dawley was from a country closer to Canada, than the filmmaker whose first movie was Jemima & Johnny.\n\nPassages:\n\n[Jemima &amp; Johnny]\nIt is the first film by South African filmmaker Lionel Ngakane, and won a plate at the 1966 Venice Film Festival.\n\n[Lionel Ngakane]\nLionel Ngakane (17 July 1928 – 26 November 2003) was a South African filmmaker and actor.\n\n[J. Searle Dawley]\nJames Searle Dawley (May 13, 1877 – March 30, 1949) was an American director and screenwriter.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qb1f9890702",
  "kind": "yes/no",
  "text": "Claim: The population at the 2010 census of the rural town where John Rais was born was 24,498.\n\nPassages:\n\n[Burlington, Massachusetts]\nThe population was 24,498 at the 2010 census.\n\n[John Rais]\nRais was born and raised in Burlington, Massachusetts, the youngest of seven children.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6668c1e13e",
  "kind": "yes/no",
  "text": "Claim: Munich beat the Tajikistan in a sporting event. Jack Taylor (referee) was famous for officiating at this event.\n\nPassages:\n\n[Jack Taylor (referee)]\nJohn Keith \"Jack\" Taylor, OBE (21 April 1930 – 27 July 2012) was an English football referee, famous for officiating in the 1974 FIFA World Cup Final during which he awarded two penalties in the first 30 minutes.\n\n[1974 FIFA World Cup Final]\nThe 1974 FIFA World Cup Final was the final match of the 1974 FIFA World Cup, the 10th FIFA World Cup, a competition to determine the world champion among national men's football sides. The match was contested by the Netherlands and West Germany, with the West Germans winning 2–1.\n\n[Football in Munich]\nMunich is one of the most successful footballing cities in Europe and the World with over 40 trophies, including Germany's victory in the 1974 FIFA World Cup Final.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q7c1607d131",
  "kind": "yes/no",
  "text": "Claim: The film Mad Hot Ballroom was created more recently as compared to the 1982 film for which \"Powaqqatsi\" is a sequel.\n\nPassages:\n\n[Powaqqatsi]\nPowaqqatsi ( ), or Powaqqatsi: Life in Transformation, is a 1988 American documentary film directed by Godfrey Reggio and the sequel to Reggio's experimental 1982 film, \"Koyaanisqatsi\".\n\n[Koyaanisqatsi]\nKoyaanisqatsi ( ), also known as Koyaanisqatsi: Life Out of Balance, is a 1982 American experimental film directed by Godfrey Reggio with music composed by Philip Glass and cinematography by Ron Fricke.\n\n[Mad Hot Ballroom]\nMad Hot Ballroom is a 2005 American documentary film directed and co-produced by Marilyn Agrelo and written and co-produced by Amy Sewell, about a ballroom dance program in the New York City Department of Education, the New York City public school system for fifth graders.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9458beb3d6",
  "kind": "yes/no",
  "text": "Text: Pretending to blow on my beverage as I drink wine out of a mug during my zoom class because I am the queen of deception!!!!!!!!!",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q4c017b64a2",
  "kind": "yes/no",
  "text": "Claim: The choreographer of La Vivandiere or Markitenka was the \"Maître de Ballet\" of this ballet company. Diana Vishneva is the principal ballet dancer for them,\n\nPassages:\n\n[Mariinsky Ballet]\nThe Mariinsky Ballet is the resident classical ballet company of the Mariinsky Theatre in Saint Petersburg, Russia. Founded in the 18th century and originally known as the Imperial Russian Ballet, the Mariinsky Ballet is one of the world's leading ballet companies. The Mariinsky Ballet is the parent company of the \"Vaganova Ballet Academy\", a leading international ballet school.\n\n[La Vivandière or Markitenka]\nLa Vivandière (or Markitenka, as it is known in Russia) is a ballet in one act with choreography by Arthur Saint-Léon and Fanny Cerrito, and music by Cesare Pugni.\n\n[Diana Vishneva]\n\" Vishnyova Russian: Диа́на Ви́кторовна Вишнёва ; born July 13, 1976) is a Russian ballet dancer who performs as a principal dancer with the Mariinsky Ballet (formerly the Kirov Ballet).\n\n[Arthur Saint-Léon]\nArthur Saint-Léon (17 September 1821, Paris – 2 September 1870) was the \"Maître de Ballet\" of St. Petersburg Imperial Ballet from 1859 until 1869 and is famous for creating the choreography of the ballet \"Coppélia\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q62a586ab50",
  "kind": "yes/no",
  "text": "Claim: Vishal Bhardwaj is the 1965-born field director who directed this 2002 Indian comedy horror film, in which English actor Shweta Basu Prasad won the National Film Award for Best Child Actor.\n\nPassages:\n\n[Makdee]\nMakdee (English: Spider ), promoted as The Web Of The Witch, in English, is a 2002 Indian comedy horror film directed by Vishal Bhardwaj.\n\n[Shweta Basu Prasad]\nFor her performance in the 2002 film Makdee, she won the National Film Award for Best Child Actor.\n\n[Vishal Bhardwaj]\nVishal Bhardwaj (born 4 August 1965) is an Indian film director, screenwriter, producer, music composer and playback singer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbe8fb1cdda",
  "kind": "yes/no",
  "text": "Tweet: I remember when I was a kid how I used to troll my dad. \nI’d be watching a film on sky movies and then when I knew he was in the other room I would say out loud ‘wow look at the tits on her’ \nHe would come back in the room and nothing was there but he’d ask questions like…",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q0f6a6eaa93",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "traitor by olivia rodrigo in the background ?? YES",
   "NOT OLIVIA RODRIGO TRAITOR IN THE BACKGROUND #LoveIsland"
  ]
 },
 {
  "qid": "q6db6b8de51",
  "kind": "yes/no",
  "text": "Tweet: Baffles me as to why ANY retailers still use Hermes as their chosen courier 😑",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q79d6e4eb80",
  "kind": "yes/no",
  "text": "Claim: Both the director of the horror film Mulholland Falls and Robert Redford work as a director.\n\nPassages:\n\n[Mulholland Falls]\nMulholland Falls is a 1996 American neo-noir crime thriller film directed by Lee Tamahori, written by Pete Dexter, and starring an ensemble cast featuring Nick Nolte, Jennifer Connelly, Chazz Palminteri, Michael Madsen, Chris Penn, Melanie Griffith, Andrew McCarthy, Treat Williams, and John Malkovich.\n\n[Robert Redford]\nCharles Robert Redford Jr. (born August 18, 1936) is an American actor, director, producer, businessman, environmentalist, and philanthropist.\n\n[Lee Tamahori]\nLee Tamahori (born 17 June 1950) is a New Zealand filmmaker best known for directing 1994 film \"Once Were Warriors\" and 2002 James Bond film \"Die Another Day\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q53dd077d8b",
  "kind": "yes/no",
  "text": "Tweet: @RealCandaceO Ok so when does the anger and bitterness start? Just so I can prepare properly…",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q4ecb22756c",
  "kind": "yes/no",
  "text": "Claim: The british director of the 1947 film New Orleans is not from the USA. Neither is the director of Room in the House.\n\nPassages:\n\n[Arthur Lubin]\nArthur Lubin (July 25, 1898 – May 12, 1995) was an American film director and producer who directed several \"Abbott & Costello\" films, \"Phantom of the Opera\" (1943), the \"Francis the Talking Mule\" series and created the talking-horse TV series \"Mister Ed\".\n\n[Maurice Elvey]\nMaurice Elvey (11 November 1887 – 28 August 1967) was the most prolific film director in British history.\n\n[New Orleans (film)]\nThe movie stars Arturo de Cordova and Dorothy Patrick, features Marjorie Lord, and was directed by Arthur Lubin.\n\n[Room in the House]\nRoom in the House is a 1955 comedy-drama film directed by Maurice Elvey.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qda9626d787",
  "kind": "yes/no",
  "text": "Claim: The Sumerians invented the type of script used in written autographs.\n\nPassages:\n\n[Cuneiform script]\nCuneiform script ( or or ), one of the earliest systems of writing, was invented by the Sumerians.\n\n[Autograph (Assyriology)]\nAn autograph in Assyriology is the hand-copy of a cuneiform clay-tablet.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc8b662f824",
  "kind": "yes/no",
  "text": "Claim: The Hellcat Spangled Shalalala is a song by the English band formed in the High Green suburb of Sheffield.\n\nPassages:\n\n[The Hellcat Spangled Shalalala]\n\"The Hellcat Spangled Shalalala\" is a song by the English indie rock band Arctic Monkeys, released as the second single from their fourth studio album \"Suck It and See\" and was intended to be released as a 7\" vinyl on 15 August 2011.\n\n[Arctic Monkeys]\nArctic Monkeys are an English rock band formed in 2002 in High Green, a suburb of Sheffield.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q4662016fc1",
  "kind": "yes/no",
  "text": "Claim: Randy Herman Meisner was born before the singer of I Feel for You (album). It was released on the Warner Bros. Records label in 1984.\n\nPassages:\n\n[Randy Meisner]\nRandy Herman Meisner (born March 8, 1946) is an American former musician, singer and songwriter best known as a founding member of the Eagles and Poco.\n\n[I Feel for You (album)]\nI Feel for You is the fifth solo studio album by American R&B/funk singer Chaka Khan, released on the Warner Bros. Records label in 1984.\n\n[Chaka Khan]\nChaka Khan (born Yvette Marie Stevens, March 23, 1953) is an American recording artist whose career has spanned five decades, beginning in the 1970s as the frontwoman and focal point of the funk band Rufus.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q778402e021",
  "kind": "yes/no",
  "text": "Tweet: Lol at my life :)",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qb25109f0aa",
  "kind": "yes/no",
  "text": "Claim: Twin Pines/Lone Pine Mall is the fictional name of the mall in the movie \"Back to the Future\" which was filmed at the headquarters of EverTrust Bank.\n\nPassages:\n\n[Puente Hills Mall]\nIt is most famous for serving as the filming site for the Twin Pines/Lone Pine Mall for the 1985 movie \"Back to the Future\" starring Michael J. Fox and Christopher Lloyd.\n\n[EverTrust Bank]\nEverTrust Bank (華信商業銀行), or Ever Trust Bank and Evertrust Bank, as its advertisement often appeared in the local Chinese media, is an overseas Chinese bank in the United States.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qd92beef6a1",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "For a good laugh, follow me over on @vsheltonsports to see my best attempt at covering sports business news for class this semester.",
   "I would say \"I have zero interest in sports, so definitely regretting the decision to sign up for a sports business class that's making me tweet about sports every day...\""
  ]
 },
 {
  "qid": "qf9dfe07547",
  "kind": "yes/no",
  "text": "Claim: Animated feature Monsters, Inc. Laugh Floor replaced the 1992 film The Timekeeper shown at three Disney parks.\n\nPassages:\n\n[Monsters, Inc. Laugh Floor]\nMonsters, Inc. Laugh Floor is an attraction within the Magic Kingdom, a theme park at Walt Disney World Resort. It opened on April 2, 2007 within the park's Tomorrowland section, where it replaced the Circle-Vision attraction The Timekeeper.\n\n[The Timekeeper]\nThe Timekeeper (also known as From Time to Time and Un Voyage à Travers le Temps) was a 1992 Circle-Vision 360° film that was presented at three Disney parks around the world.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7d13804594",
  "kind": "yes/no",
  "text": "Claim: The Neoclassical monument Benito Juárez Hemicycle is located in this large city of Mexico that consists of sixteen municipalities.\n\nPassages:\n\n[Mexico City]\nThe city consists of sixteen municipalities.\n\n[Benito Juárez Hemicycle]\nThe Benito Juárez Hemicycle is a Neoclassical monument located at the Alameda Central park in Mexico City, Mexico and commemorating the Mexican statesman Benito Juárez.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2dc05c4d0b",
  "kind": "yes/no",
  "text": "Claim: Lt. Robin Crusoe USN was a Disney Film. It was released before a film in which Dennis Fimple appeared.\n\nPassages:\n\n[The Apple Dumpling Gang (film)]\nThe Apple Dumpling Gang is a 1975 American comedy-western film produced by Walt Disney Productions about a slick gambler named Russell Donovan (Bill Bixby) who is duped into taking care of a group of orphans who eventually strike gold during the California Gold Rush.\n\n[Lt. Robin Crusoe, U.S.N.]\nLt. Robin Crusoe USN is a 1966 comedy film released and scripted by Walt Disney, and starring Dick Van Dyke as a U.S. Navy pilot who becomes a castaway on a tropical island.\n\n[Dennis Fimple]\nHe also had roles in films such as \"Truck Stop Women\" (1974), \"The Apple Dumpling Gang\" (1975), \"Mackintosh and T.J.\" (1975), \"Stay Hungry\" (1976), \"King Kong\" (1976), \"The Shadow of Chikara\" (1977), \"Goin' South\" (1978), \"The Wild Women of Chastity Gulch\" (1982) and \"Maverick\" (1994), and shared the lead in \"Bootleggers\" (1974) and \"Creature from Black Lake\" (1976).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qd6d796b7fb",
  "kind": "yes/no",
  "text": "Claim: This band's Bass Guitarist of set up Koolarrow Records. They and the electropop group, who recorded the 1995 debut alum Get Sharp, are from the same state.\n\nPassages:\n\n[Get Sharp]\nGet Sharp is the debut album by electropop group The Limousines.\n\n[Koolarrow Records]\nKoolarrow Records is an independent record label based in San Francisco, set up by Faith No More's Bass Guitarist Billy Gould.\n\n[Faith No More]\nFaith No More (sometimes abbreviated as FNM) is an American rock band from San Francisco, California, formed in 1979.\n\n[The Limousines]\nThe Limousines are an American indietronica band based out of California's San Francisco Bay Area.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q4e3f5ed433",
  "kind": "yes/no",
  "text": "Claim: Andrea Prodan is the youngest brother of this rock star. Singer is the occupation that is shared by him and the vocalist for Heaven 17.\n\nPassages:\n\n[Luca Prodan]\nLuca Prodan (17 May 1953 – 22 December 1987) was an Italian–Scotish musician and singer.\n\n[Heaven 17]\nThe band were a trio for most of their career, composed of Martyn Ware (keyboards), Ian Craig Marsh (keyboards) (both previously of the Human League) and Glenn Gregory (vocals).\n\n[Andrea Prodan]\nAndrea Prodan (born 16 November 1961) Scottish-Italian film actor, composer and musician is the younger brother of Argentine rock star Luca Prodan.\n\n[Glenn Gregory]\nGlenn Peter Gregory (born 16 May 1958) is an English singer, songwriter, and multi-instrumentalist whose music career spans more than 30 years.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6e177f2abe",
  "kind": "yes/no",
  "text": "Post: Lol i actually realized that I’ve justified not working out for the past three months by telling myself that my hair was too short to fit in a ponytail.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q59c31f7d68",
  "kind": "yes/no",
  "text": "Claim: Esme Melville, was an Australian theatre and concert hall, television and film actress, she was nominated for Best Supporting Actress for her role of Miss Collard in \"Romulus, My Father\", an Australian drama film, directed by Richard Roxburgh, released in the year 2007.\n\nPassages:\n\n[Romulus, My Father (film)]\nRomulus, My Father is a 2007 Australian drama film directed by Richard Roxburgh.\n\n[Esme Melville]\nAt the 2007 Australian Film Institute Awards she was nominated for Best Supporting Actress for her role of Miss Collard in \"Romulus, My Father\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6141bdf692",
  "kind": "yes/no",
  "text": "Text: Anyone else hear some like thunder or something?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q0582a7c195",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "\"This is not at all helpful information.\"",
   "\"coping strategies to help with tinnitus and hearing loss: see a doctor!\" Wow thanks internet"
  ]
 },
 {
  "qid": "qa481493258",
  "kind": "yes/no",
  "text": "Tweet: i can’t wait until the weather cools down so i can read under a tree at a park and look like a mysterious intellectual",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qc0c77b26e5",
  "kind": "yes/no",
  "text": "Claim: The plaintiff in the 1892 Barbed Wire Patent Case was born on January 18, 1813.\n\nPassages:\n\n[Joseph Glidden]\nJoseph Glidden (January 18, 1813 – October 9, 1906) was an American businessman.\n\n[The Barbed Wire Patent]\nThe Barbed Wire Patent Case, 143 U.S. 275 was a significant patent dispute in 1892 between plaintiff Joseph Glidden and the USPTO regarding the right of barbed wire.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf172cd0e11",
  "kind": "yes/no",
  "text": "Text: I’ve seen a lot of people on local Facebook groups asking AirBnB owners if they have any availability recently. If only there was a website you could use to find out if an AirBnB was available 🤔",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q0e73686c77",
  "kind": "yes/no",
  "text": "Tweet: why is it always when i have no money that my gym shoes suddenly have a hole in!! :(",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qa1c6673bd6",
  "kind": "yes/no",
  "text": "Claim: The 2018 Unibet Premier League Darts tournament, organised by the Professional Darts Corporation, is planned to finish at the multi-purpose indoor arena located in the centre of The O2 entertainment complex on the Greenwich Peninsula in south-east London.\n\nPassages:\n\n[The O2 Arena]\nThe O2 Arena (temporarily the sponsor-neutral \"North Greenwich Arena\", during the 2012 Summer Olympics and 2012 Summer Paralympics), is a multi-purpose indoor arena located in the centre of The O2 entertainment complex on the Greenwich Peninsula in south-east London.\n\n[2018 Premier League Darts]\nThe 2018 Unibet Premier League Darts will be a darts tournament organised by the Professional Darts Corporation – the fourteenth edition of the tournament. The event will begin on Thursday 1 February at the 3Arena in Dublin and will end with the Play-Offs at The O2 Arena in London on Thursday 17 May.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q21018b3fb1",
  "kind": "yes/no",
  "text": "Text: I still can’t believe England won the World Cup",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qde252c1d63",
  "kind": "yes/no",
  "text": "Claim: The building that Lyceum Theatre (Park Avenue South) was torn down for was designed by the firm of Physicians Life Insurance Company and not the 15 Hudson Yards building.\n\nPassages:\n\n[Metropolitan Life Insurance Company Tower]\nThe Metropolitan Life Insurance Company Tower, colloquially known as the Met Life Tower, is a landmark skyscraper located on Madison Avenue near the intersection with East 23rd Street, across from Madison Square Park in Manhattan, New York City. Designed by the architectural firm of Napoleon LeBrun & Sons and built by the Hedden Construction Company, the tower is modeled after the Campanile in Venice, Italy.\n\n[Lyceum Theatre (Park Avenue South)]\nIt was built in 1885 and operated until 1902, when it was torn down to make way for the Metropolitan Life Insurance Company Tower.\n\n[15 Hudson Yards]\nLocated in Chelsea near Hell's Kitchen Penn Station area, the building is a part of the Hudson Yards project, a plan to redevelop the Metropolitan Transportation Authority's West Side Yards.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q89dd6d1acf",
  "kind": "yes/no",
  "text": "Claim: A number of Carmen Robertson's writings focus on this Aboriginal Canadian artist. Which is the Aboriginal Canadian artist of the M'Chigeeng.\n\nPassages:\n\n[Norval Morrisseau]\nNorval Morrisseau, CM (March 14, 1932 – December 4, 2007), also known as Copper Thunderbird, was an Aboriginal Canadian artist.\n\n[Carmen Robertson]\nA number of Robertson's writings focus on the Aboriginal Canadian artist Norval Morrisseau.\n\n[Blake Debassige]\nBlake Debassige is a Native Canadian artist of the M'Chigeeng First Nation, born at West Bay on Manitoulin Island in Ontario on June 22, 1956.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q588bd03ced",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "I’m gonna miss scantrons shortening my name to “Christ” after 16 years",
   "I'm not going to miss scantrons shortening my name to “Christ” after 16 years"
  ]
 },
 {
  "qid": "q57c72c5a08",
  "kind": "yes/no",
  "text": "Claim: In 1972 Albert Bensadoun founded his retail shoe company.\n\nPassages:\n\n[Aldo Group]\nThe Aldo Group is a Canadian Moroccan retailer that owns and operates a worldwide chain of shoe and accessories stores. The company was founded by Aldo Bensadoun in Montreal, Quebec, in 1972, where its corporate headquarters remain today.\n\n[Aldo Bensadoun]\nAlbert \"Aldo\" Bensadoun, is originally an Algerian-Canadian businessman, investor and philanthropist. He is the founder and executive chairman of the ALDO Group, a retail shoe company based in Montreal, Quebec, Canada.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2dc15e0a91",
  "kind": "yes/no",
  "text": "Claim: This person worked on the American horror film The Nightcomers. Like the filmmaker who directed and edited The Raid 2 this person is also a director.\n\nPassages:\n\n[Gareth Evans (director)]\nGareth Huw Evans (born 1980) is a Welsh film director, screenwriter, film editor and action choreographer.\n\n[The Raid 2]\nIt is the sequel to his 2011 film \"The Raid\".\n\n[The Nightcomers]\nThe Nightcomers is a 1971 British horror film directed by Michael Winner and starring Marlon Brando, Stephanie Beacham, Thora Hird, Harry Andrews and Anna Palk.\n\n[Michael Winner]\nRobert Michael Winner (30 October 1935 – 21 January 2013) was an English film director and producer, and a restaurant critic for \"The Sunday Times\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q912a882c41",
  "kind": "yes/no",
  "text": "Claim: The Ilion Animation Studios produced CGI-animated film from 2009 was 3D. The 2009 animated film written and directed by Phil Lord and Christopher Miller was not in 3D.\n\nPassages:\n\n[Cloudy with a Chance of Meatballs (film)]\nCloudy with a Chance of Meatballs is a 2009 American computer-animated science fiction comedy film loosely based on the 1978 children's book of the same name by Judi and Ron Barrett.\n\n[Planet 51]\nPlanet 51 is a 2009 Spanish and American-British-movie 3D computer-animated science fiction comedy film directed by Jorge Blanco, written by Joe Stillman, and starring Dwayne Johnson, Jessica Biel, Justin Long, Gary Oldman, Seann William Scott, and John Cleese.\n\n[Phil Lord and Christopher Miller]\nThey are known for directing and writing the animated films \"Cloudy with a Chance of Meatballs\" (2009) and \"The Lego Movie\" (2014), as well as directing the live-action comedy film \"21 Jump Street\" (2012) and its sequel (2014).\n\n[Ilion Animation Studios]\nIlion produced the CGI-animated film, \"Planet 51\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4f8a70d9ae",
  "kind": "yes/no",
  "text": "Claim: Both the director of the 1937 Soviet documentary film, \"Kolybelnaya\", and Roger Donaldson are involved in the film industry.\n\nPassages:\n\n[Lullaby (1937 film)]\n\"Kolybelnaya\") is a 1937 Soviet documentary film directed by Dziga Vertov.\n\n[Dziga Vertov]\nDziga Vertov (Russian: Дзига Вертов ; born David Abelevich Kaufman, Russian: Дави́д А́белевич Ка́уфман , and also known as Denis Kaufman; 2 January 1896 – 12 February 1954) was a Soviet pioneer documentary film and newsreel director, as well as a cinema theorist.\n\n[Roger Donaldson]\nRoger Donaldson (born 15 November 1945) is an Australian-born New Zealand film director, producer and writer whose films include \"The World's Fastest Indian\" (2005), acclaimed 1981 relationship drama \"Smash Palace\", and a run of titles shot in the United States, including the Kevin Costner films \"No Way Out\" (1987) and \"Thirteen Days\" (2000), and the 1997 disaster film \"Dante's Peak\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1c4c6092b2",
  "kind": "yes/no",
  "text": "Tweet: Super bummed that one of my best friends from high school is a republican",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q7c6aa5dc59",
  "kind": "yes/no",
  "text": "Claim: Rick and Morty was the television series written by Hepburn and directed by Dominic Polcino that premiered on July 26th, 2015.\n\nPassages:\n\n[The Ricks Must Be Crazy]\nWritten by Dan Guterman and directed by Dominic Polcino, the episode first aired on Adult Swim in the United States on August 30, 2015.\n\n[Rick and Morty (season 2)]\nThe second season of the animated television series \"Rick and Morty\" originally aired in the United States on Cartoon Network's late night programming block, Adult Swim, which premiered on July 26, 2015 with \"A Rickle in Time\", and concluded on October 4 with \"The Wedding Squanchers\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf6c8c02655",
  "kind": "yes/no",
  "text": "Claim: Eyes of the Dead opened for Six Feet Under, an American death rock band from Tampa, Florida.\n\nPassages:\n\n[Eyes of the Dead]\nThey have toured throughout the northeastern and midwestern areas of The United States, opening for many different national touring acts, such as: The Absence, Agnostic Front, Anthrax, Carnivore, Dark Tranquility, Destruction, D.R.I., Dying Fetus, Emperor, Exodus, Goatwhore, God Forbid, Immolation, Job For A Cowboy, Krisiun, Last Chance To Reason Misfits, Misery Index, Motograter, Mushroomhead, Opeth, Revocation, Six Feet Under, Sodom, Sonata Arctica, Soulfly, Suffocation, Testament, Thy Will Be Done, Unearth, Warbringer, Winds of Plague, and many others.\n\n[Six Feet Under (band)]\nSix Feet Under is an American death metal band from Tampa, Florida, formed in 1993.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q130874fc95",
  "kind": "yes/no",
  "text": "Claim: The company that created Doravirine is American.\n\nPassages:\n\n[Doravirine]\nDoravirine (MK-1439) is a non-nucleoside reverse transcriptase inhibitor under development by Merck & Co. for use in the treatment of HIV/AIDS.\n\n[Merck &amp; Co.]\nMerck & Co., Inc. (), d.b.a. Merck Sharp & Dohme (MSD) outside the United States and Canada, is an American pharmaceutical company and one of the largest pharmaceutical companies in the world.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q37452d15e2",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Football and RuPual's Drag Race are wildly different shows.",
   "Andrews really trying to explain to me that football and rupauls drag race aren’t the same thing when it in fact is the same thing."
  ]
 },
 {
  "qid": "q1b677b8522",
  "kind": "yes/no",
  "text": "Claim: The writer of Serenade No. 6 (Mozart) was a composer. So was the writer of Brazilian national anthem L'esule di Granata.\n\nPassages:\n\n[L'esule di Granata]\nL'esule di Granata (\"The exile of Granada\") is a \"melodramma serio\" (serious opera ) in two acts by Giacomo Meyerbeer.\n\n[Serenade No. 6 (Mozart)]\nThe Serenade No. 6 for Orchestra in D major K. 239, \"Serenata notturna\", was written by Wolfgang Amadeus Mozart in Salzburg, in 1776.\n\n[Giacomo Meyerbeer]\nGiacomo Meyerbeer (born Jacob Liebmann Beer; 5 September 1791 – 2 May 1864) was a German opera composer of Jewish birth who has been described as perhaps the most successful stage composer of the nineteenth century.\n\n[Wolfgang Amadeus Mozart]\nWolfgang Amadeus Mozart ( ; ; ] ; 27 January 1756 – 5 December 1791), baptised as Johannes Chrysostomus Wolfgangus Theophilus Mozart, was a prolific and influential composer of the Classical era.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe2578820f2",
  "kind": "yes/no",
  "text": "Claim: The director of the 1936 film The Singing Cowboy was an Western actor. Kurt Neumann was not an Western actor.\n\nPassages:\n\n[Kurt Neumann (director)]\nKurt Neumann (5 April 1908, Nuremberg, Germany - 21 August 1958, Los Angeles) was a German Hollywood film director who specialized in science fiction movies in his later career.\n\n[The Singing Cowboy (1936 film)]\nThe Singing Cowboy is a 1936 American Western film directed by Mack V. Wright and starring Gene Autry, Smiley Burnette, and Lois Wilde.\n\n[Mack V. Wright]\nMack V. Wright (9 March 1894 – 14 August 1965) was an American actor and film director.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3c03182f01",
  "kind": "yes/no",
  "text": "Claim: Adam Chance Angus Rayner appeared as Juliet on stage in \"Romeo and Juliet in the town of Stratford-upon-Avon.\n\nPassages:\n\n[Adam Rayner]\nHe has also appeared on stage in \"The Rivals\" (Bristol Old Vic, 2004), \"Romeo and Juliet\" (Royal Shakespeare Theatre, 2006) and \"Much Ado About Nothing\" (Novello, 2006).\n\n[Royal Shakespeare Theatre]\nIt is located in the town of Stratford-upon-Avon – Shakespeare's birthplace – in the English Midlands, beside the River Avon.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
