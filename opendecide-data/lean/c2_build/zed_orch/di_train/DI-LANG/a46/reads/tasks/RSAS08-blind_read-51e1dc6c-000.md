# A46 replay label-noise blind read RSAS08-blind_read-51e1dc6c-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS08-blind_read-51e1dc6c-000.json

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
  "qid": "q5ed962e0e8",
  "kind": "yes/no",
  "text": "Claim: Damian Lillard was a sixth overall pick in the April 2012 NBA draft and MVP of the 2012 NBA Summer League.\n\nPassages:\n\n[Damian Lillard]\nAfter being selected by Portland with the sixth overall pick in the 2012 NBA draft, Lillard won the NBA Rookie of the Year by unanimous decision.\n\n[2012 NBA Summer League]\nThe 2012 NBA Summer League was a pro basketball league run by the NBA just after the 2012 NBA Draft. Damian Lillard (Portland Trail Blazers) and Josh Selby (Memphis Grizzlies) won the MVP honors.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa57323f6dc",
  "kind": "yes/no",
  "text": "Post: Totall Carloss... #WTF1 @_aarava https://t.co/p70GOaCLyS",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qb5e9090b99",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "Disposing of a dead opossum was not a pleasant way to start my day.",
   "Just disposed of a dead opossum. Good morning!"
  ]
 },
 {
  "qid": "qeb1dd176b8",
  "kind": "yes/no",
  "text": "Claim: Gone with the Wind (novel) was penned by an Canadian writer. This Canadian writer and the historian that described the Minoan civilization were not both philosophical writers.\n\nPassages:\n\n[Margaret Mitchell]\nMargaret Munnerlyn Mitchell (November 8, 1900 – August 16, 1949) was an American author and journalist.\n\n[Gone with the Wind (novel)]\nGone with the Wind is a novel by American writer Margaret Mitchell, first published in 1936.\n\n[Minoan civilization]\nIt has been described as the earliest of its kind in Europe, with historian Will Durant calling the Minoans \"the first link in the European chain\".\n\n[Will Durant]\nWilliam James \"Will\" Durant ( ; November 5, 1885 – November 7, 1981) was an American writer, historian, and philosopher.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qb8bad231a3",
  "kind": "yes/no",
  "text": "Tweet: \"I know of no more encouraging fact than the unquestionable ability of man to elevate his life by conscious endeavor.\" \n Henry David Thoreau",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q16a5963202",
  "kind": "yes/no",
  "text": "Claim: Velvetpark magazine is written more for a lesbian and queer-identified female readership not Shape magazine.\n\nPassages:\n\n[Velvetpark]\n\"Velvetpark\" also hosts a social network and dating community for lesbians and queer-identified women.\n\n[Shape (magazine)]\nAt that time, Weider Enterprises consisted primarily of the bodybuilding magazine \"Muscle & Fitness\". \"Shape\" found a readership based on that formula.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe9ad005a71",
  "kind": "yes/no",
  "text": "Claim: The college Michigan Edward Dorr Griffin served as president at from 1821 to 1836, was founded before the University of Southern California.\n\nPassages:\n\n[Williams College]\nWilliams College is a private liberal arts college in Williamstown, Massachusetts, United States. It was established in 1793 with funds from the estate of Ephraim Williams a colonist from the Province of Massachusetts Bay who was killed in the French and Indian War in 1755.\n\n[University of Southern California]\nFounded in 1880, it is the oldest private research university in California.\n\n[Edward Dorr Griffin]\nEdward Dorr Griffin (6 January 1770 – 8 November 1837) was a Christian minister and an American educator who served as President of Williams College from 1821 to 1836 and served as the first pastor of Park Street Church from 1811 to 1815.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q475220c24b",
  "kind": "yes/no",
  "text": "Post: All I've done this summer is binge watch The Office and Friends 🙃🙃",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qa39a12b91c",
  "kind": "yes/no",
  "text": "Tweet: @DylanPetit17 @jaredj5 Let's listen to Dylan Petit over actually doctors, biologists and epidemiologists. 🙄",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q41854e8cd9",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "@MarkHendyHR Only joking... keep it real. HR professionals have a life too... 🤔",
   "Only joking. Keep it real. HR professionals don’t have a life."
  ]
 },
 {
  "qid": "qfcab31f788",
  "kind": "yes/no",
  "text": "Text: 5 star personality\n4.8 star uber rating",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q001e31cd30",
  "kind": "yes/no",
  "text": "Claim: Between Shades of Gray is the best-seller by Ruta Sepetys.\n\nPassages:\n\n[Ashes in the Snow]\nAshes in the Snow is a World War II drama based on the best-seller \"Between Shades of Gray\" by Ruta Sepetys.\n\n[Between Shades of Gray]\nBetween Shades of Gray, a New York Times Bestseller, is the debut novel of American novelist Ruta Sepetys.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0eaa075a2d",
  "kind": "yes/no",
  "text": "Claim: Both Elisabeth Vrba's colleague, who she coined the word exaptation with, and Ann Beattie have the profession of writer in common.\n\nPassages:\n\n[Stephen Jay Gould]\nHe was also one of the most influential and widely read writers of popular science of his generation.\n\n[Ann Beattie]\nAnn Beattie (born September 8, 1947) is an American novelist and short story writer.\n\n[Elisabeth Vrba]\nShe is well known for developing the Turnover Pulse Hypothesis, as well as coining the word exaptation with colleague Stephen Jay Gould.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf5a4821765",
  "kind": "yes/no",
  "text": "Claim: This individual directed Boxing Helena. She and the filmmaker who worked on the film Bringing Out the Dead are both directors.\n\nPassages:\n\n[Boxing Helena]\nBoxing Helena is a 1993 American romantic mystery thriller film with horror elements directed by Jennifer Lynch, and starring Sherilyn Fenn, Julian Sands, and Bill Paxton.\n\n[Martin Scorsese]\nMartin Charles Scorsese ( ; ] ; born November 17, 1942) is an American director, producer, screenwriter, and film historian, whose career spans more than 50 years.\n\n[Bringing Out the Dead]\nBringing Out the Dead is a 1999 American drama film directed by Martin Scorsese, written by Paul Schrader, based on the novel by Joe Connelly and starring Nicolas Cage, Patricia Arquette, John Goodman, Ving Rhames, and Tom Sizemore.\n\n[Jennifer Lynch]\nJennifer Chambers Lynch (born April 7, 1968) is an American film director and screenwriter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qaa4afe7979",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "just booked to see David Gray too,,, am i 40",
   "I am only 21."
  ]
 },
 {
  "qid": "qe8a2cded25",
  "kind": "yes/no",
  "text": "Claim: The person the Centro Cultural Bella Epoca bookshop is named after and Arthur Hailey share characteristics of poet and author.\n\nPassages:\n\n[Arthur Hailey]\nArthur Hailey (April 5, 1920 – November 24, 2004) was a British-Canadian novelist whose plot-driven storylines were set against the backdrops of various industries.\n\n[Rosario Castellanos]\nRosario Castellanos Figueroa (] ; 25 May 1925 – 7 August 1974) was a Mexican poet and author.\n\n[Centro Cultural Bella Época]\nIt includes the Rosario Castellanos bookshop (claimed to be the largest bookshop in Latin America) which carries over 35 thousand different titles, and has a children’s area, a coffee shop, and reading facilities.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0c3280dd60",
  "kind": "yes/no",
  "text": "Tweet: ayo govvy hook me up w that stimmy if you know how the flow goes y feel",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q94264b50a1",
  "kind": "yes/no",
  "text": "Tweet: do you think when a middle aged white man goes to buy a big lifted brand new F150 they check to make sure his penis is incredibly small?? or do they just take his word for it",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qaf0f67354a",
  "kind": "yes/no",
  "text": "Claim: Debbie Fields husband is associated with the hotel chain based in Atlanta, Georgia. Boardwalk Hotel and Casino was once a part of that chain.\n\nPassages:\n\n[Debbi Fields]\nDebbi Fields (born September 18, 1956) is the founder and spokesperson of Mrs. Fields Bakeries. She currently lives in Nashville, Tennessee, with her husband, former Holiday Inn and Harrah's CEO Michael Rose.\n\n[Boardwalk Hotel and Casino]\nIt was part of the Holiday Inn hotel chain until it was acquired by MGM in 2000.\n\n[Holiday Inn]\nHoliday Inn is an American brand of hotels, and a subsidiary of InterContinental Hotels Group. The hotel chain is based in Atlanta, Georgia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q60c70fae05",
  "kind": "yes/no",
  "text": "Claim: Of Vladimir Voevodsky and Anatoly Maltsev, Anatoly Ivanovich Maltsev was married first.\n\nPassages:\n\n[Anatoly Maltsev]\nAnatoly Ivanovich Maltsev (also: Malcev, Mal'cev; Russian: Анато́лий Ива́нович Ма́льцев; 27 November N.S./14 November O.S. 1909, Moscow Governorate – 7 June 1967, Novosibirsk) was born in Misheronsky, near Moscow, and died in Novosibirsk, USSR.\n\n[Vladimir Voevodsky]\nVladimir Alexandrovich Voevodsky ( ; Russian: Влади́мир Алекса́ндрович Воево́дский , 4 June 1966 - 30 September 2017) was a Russian mathematician.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb4bc269a01",
  "kind": "yes/no",
  "text": "Claim: Gabriela Lemus is a member of the school the Thurgood Marshall College Fund which has been affiliated with UDC.\n\nPassages:\n\n[Gabriela Lemus]\nIn 2012 she was appointed to the board of the University of the District of Columbia.\n\n[University of the District of Columbia]\nThe University of the District of Columbia (UDC) is the only public university in the U.S. capital of Washington, D.C. UDC is one of the few urban land-grant universities in the country and a member school of the Thurgood Marshall College Fund.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q88afa500de",
  "kind": "yes/no",
  "text": "Claim: The commander of The French Tenth Army (AEF) on the Western Front was the most famous post of the man who commanded American and French troops against German positions during this battle, during which the 3rd Pursuit Group saw action as a supporting unit.\n\nPassages:\n\n[Battle of Saint-Mihiel]\nThe Battle of Saint-Mihiel was a major World War I battle fought from 12–15 September 1918, involving the American Expeditionary Force (AEF) and 110,000 French troops under the command of General John J. Pershing of the United States against German positions.\n\n[3d Pursuit Group]\nFormed in France in July 1918, the group was assigned to the 1st Pursuit Wing and saw action in the final months of the war, supporting the Battle of Saint-Mihiel and the Meuse-Argonne Offensive.\n\n[John J. Pershing]\nGeneral of the Armies John Joseph \"Black Jack\" Pershing (September 13, 1860 – July 15, 1948) was a senior United States Army officer. His most famous post was when he served as the commander of the American Expeditionary Force (AEF) on the Western Front in World War I, 1917–18.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q334ac9f99e",
  "kind": "yes/no",
  "text": "Claim: Greatest Hits Volume 1 is a greatest hits compilation album by The Beatles which was exclusive to Australia and New Zealand released in 1984, the album was compiled by EMI Australia to fill in the gap, much like A Collection of Beatles Oldies (subtitled But Goldies!)\n\nPassages:\n\n[A Collection of Beatles Oldies]\nA Collection of Beatles Oldies (subtitled But Goldies!)\n\n[Greatest Hits Volume 1 (Beatles album)]\nThe album was compiled by EMI Australia to fill in the gap between \"Rubber Soul\" and \"Revolver\" (much like \"A Collection of Beatles Oldies\" would in 1966 in between \"Revolver\" and \"Sgt. Pepper's Lonely Hearts Club Band\").",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9cce5c26eb",
  "kind": "yes/no",
  "text": "Claim: The Highway that connects the major metropolitan areas of St. Louis, Louisville and Lexington in Kentucky, Charleston, West Virginia, and Richmond, Virginia opened in 1975.\n\nPassages:\n\n[Grayson, Kentucky]\nThe city has grown in size substantially since the opening of Interstate 64 in 1975 through Carter County.\n\n[Interstate 64]\nI-64 connects the major metropolitan areas of St. Louis, Louisville and Lexington in Kentucky, Charleston, West Virginia, and Richmond, Virginia.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q5546ba60be",
  "kind": "yes/no",
  "text": "Claim: A wooden roller coaster at Holiday World is located at a theme park divided into four sections.\n\nPassages:\n\n[Holiday World &amp; Splashin' Safari]\nThe theme park is divided into four sections that celebrate Christmas, Halloween, Thanksgiving and the Fourth of July with rides, live entertainment, games, and attractions.\n\n[The Voyage (roller coaster)]\nThe Voyage is a wooden roller coaster located at Holiday World & Splashin' Safari in Santa Claus, Indiana.\n\n[Wooden roller coaster]\nThere is also The Voyage at Holiday World (an example of a wooden roller coaster with a steel structure for supports) featuring three separate 90-degree banked turns.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9c5507f6f5",
  "kind": "yes/no",
  "text": "Claim: Jack Milsom (22 February 1907 – 1977) was an English footballer who reluctantly played in The Football League for League One team Rochdale Association Football Cub based in the town of Rochdale, Greater Manchester, England.\n\nPassages:\n\n[Rochdale A.F.C.]\nRochdale Association Football Club is a professional football club based in the town of Rochdale, Greater Manchester, England, that competes in League One, the third-highest division overall in the English football league system.\n\n[Jack Milsom]\nJack Milsom (22 February 1907 – 1977) was an English footballer who played in The Football League for Bolton Wanderers, Manchester City and Rochdale.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9d6a01692e",
  "kind": "yes/no",
  "text": "Claim: Nauset Regional High School is the NEASC accredited California high school that Mike DeVito attended.\n\nPassages:\n\n[Nauset Regional High School]\nNauset Regional High School an NEASC accredited high school located in North Eastham, Massachusetts.\n\n[Mike DeVito]\nDeVito attended high school at Nauset Regional High School in Eastham, Massachusetts.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2747746b84",
  "kind": "yes/no",
  "text": "Claim: Kuvasz and Bouvier des Ardennes are both breeds of dogs.\n\nPassages:\n\n[Kuvasz]\nThe Kuvasz (] ), is an ancient breed of a livestock dog of Hungarian origin.\n\n[Bouvier des Ardennes]\nBouvier des Ardennes is a rare dog breed from Belgium.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qfa4634d3a7",
  "kind": "yes/no",
  "text": "Claim: Javier Mora, a 23 year-old Mexican boxer in the Heavyweight division, was defeated by Alexander Vladimirovich \"Sasha\" Povetkin, by a 5-round TKO, in Germany.\n\nPassages:\n\n[Javier Mora (boxer)]\nHe was defeated by Alexander Povetkin by a 5-round TKO, in Max Schmeling Halle, Prenzlauer Berg, Berlin, Germany.\n\n[Alexander Povetkin]\nAlexander Vladimirovich \"Sasha\" Povetkin ( ; Russian: Алекса́ндр Влади́мирович Пове́ткин ; born 2 September 1979) is a Russian professional boxer who held the WBA (Regular) heavyweight title from 2011 to 2013.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q39d5c0ec8e",
  "kind": "yes/no",
  "text": "Claim: HeroClix is a collectible miniatures game where players construct teams from various video games such as a fighting video game franchise developed and published by Capcom.\n\nPassages:\n\n[HeroClix]\nHeroClix is a collectible miniatures game that uses the Clix system that centers on the world of superhero comic books, especially the Marvel and DC Comics universes. Players construct teams of comic book heroes, villains, or characters from various video games series such as Street Fighter, Gears of War, and Halo and engage in a turn-by-turn battle on grid maps based on various storyline locations.\n\n[Street Fighter]\nStreet Fighter (ストリートファイター , Sutorīto Faitā ) , commonly abbreviated as \"SF\" or スト (\"Suto\"), is a fighting video game franchise developed and published by Capcom.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2eeca00ed4",
  "kind": "yes/no",
  "text": "Tweet: Just made my own pitta chips after whinging at anyone who'd listen that I can't buy them locally. So that's pitta chips and apple crumble in my culinary repertoire. SOMEONE WIFE ME.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qa7d25fd259",
  "kind": "yes/no",
  "text": "Claim: The central midfielder for Premier League club Chelsea and the Spain national team and Marco Reus and Mario Balotelli marketed Puma evoPOWER.\n\nPassages:\n\n[Puma evoPOWER]\nPuma evoPOWER is a range of football boots developed by German sportswear manufacturers Puma, first released in January 2014. The evoPOWER was marketed by the likes of Cesc Fàbregas, Marco Reus and Mario Balotelli.\n\n[Cesc Fàbregas]\nFrancesc \"Cesc\" Fàbregas Soler (] ; born 4 May 1987) is a Spanish professional footballer who plays as a central midfielder for Premier League club Chelsea and the Spain national team.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q5e1c3f1c87",
  "kind": "yes/no",
  "text": "Claim: The film that Pocahontas II: Journey to a New World was a sequel to, not was made before Born in China.\n\nPassages:\n\n[Pocahontas (1995 film)]\nPocahontas is a 1995 American animated musical romantic-comedy-drama film produced by Walt Disney Feature Animation for Walt Disney Pictures.\n\n[Pocahontas II: Journey to a New World]\nPocahontas II: Journey to a New World is a 1998 straight-to-video sequel to the 1995 Disney film \"Pocahontas\".\n\n[Born in China]\nBorn in China (我們誕生在中國) is a 2016 nature documentary film directed by Lu Chuan.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8399920e83",
  "kind": "yes/no",
  "text": "Claim: The author of When William Came, Jack Black, was British. The author of Green, Green My Valley Now was also British.\n\nPassages:\n\n[When William Came]\nWhen William Came: A Story of London Under the Hohenzollerns is a novel written by the British author Saki (the pseudonym of Hector Hugh Munro) and published in November 1913.\n\n[Green, Green My Valley Now]\nGreen, Green My Valley Now is a 1975 novel by Richard Llewellyn.\n\n[Richard Llewellyn]\nRichard Dafydd Vivian Llewellyn Lloyd (8 December 1906 – 30 November 1983), known by his pen name Richard Llewellyn, was a British novelist.\n\n[Saki]\nHector Hugh Munro (18 December 1870 – 14 November 1916), better known by the pen name Saki, and also frequently as H. H. Munro, was a British writer whose witty, mischievous and sometimes macabre stories satirize Edwardian society and culture.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qe7217f2d52",
  "kind": "yes/no",
  "text": "Claim: Billy Idol is older than the Australian singer-songwriter who co-wrote \"Love No Limit\" with Dave Hall.\n\nPassages:\n\n[Billy Idol]\nWilliam Michael Albert Broad (born 30 November 1955), known professionally as Billy Idol, is an English musician, singer, songwriter, and actor.\n\n[Kenny Greene]\nKenny Greene (January 17, 1969 – October 1, 2001) was an American singer-songwriter who was also a member of the R&B group Intro.\n\n[Love No Limit]\nIt was co-written by Kenny Greene and Dave Hall for her debut album, \"What's the 411?",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qfc58633aef",
  "kind": "yes/no",
  "text": "Claim: The 1956 Summer Olympics where Robert O'Brien competed in sprint canoe were held in Ballarat.\n\nPassages:\n\n[1956 Summer Olympics]\nThe 1956 Summer Olympics, officially known as the Games of the XVI Olympiad, were an international multi-sport event which was held in Melbourne, Victoria, Australia, in 1956, apart from the equestrian events, which were held five months earlier in Stockholm.\n\n[Robert O'Brien (canoeist)]\nRobert O'Brien (born June 6, 1933) is an American sprint canoer who competed in the late 1950s and early 1960s.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qac187c181f",
  "kind": "yes/no",
  "text": "Tweet: Does anyone have any recommendations for over the counter topical pain relief that actually works?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q5ee954b857",
  "kind": "yes/no",
  "text": "Claim: The 1969 festival production, which was directed by this man, and American Dream have documentary film in common. He also directed Wolfen (film) in 1981.\n\nPassages:\n\n[American Dream (film)]\nAmerican Dream is a 1990 \"cinéma vérité\" documentary film directed by Barbara Kopple and co-directed by Cathy Caplan, Thomas Haneke, and Lawrence Silk.\n\n[Wolfen (film)]\nWolfen is a 1981 American crime horror film directed by Michael Wadleigh and starring Albert Finney, Diane Venora, Gregory Hines and Edward James Olmos.\n\n[Michael Wadleigh]\nMichael Wadleigh, also known as Michael Wadley (born September 24, 1942 in Akron, Ohio), is an American film director and cinematographer renowned for his groundbreaking documentary of the 1969 Woodstock Festival, \"Woodstock\".\n\n[Woodstock (film)]\nWoodstock is a 1970 documentary film of the watershed counterculture Woodstock Festival which took place in August 1969 near Bethel, New York. \"",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qdb1f858a14",
  "kind": "yes/no",
  "text": "Claim: An actor that was in Wonder Woman (2017 film) performed in the Academy Award Nominated film Rosa Tran produced. It was after the premier of Fargo.\n\nPassages:\n\n[Rosa Tran]\nIn 2016, she was nominated for the Academy Award for Best Animated Feature in the 88th Academy Awards for producing the film \"Anomalisa\".\n\n[Wonder Woman (2017 film)]\nThe film is directed by Patty Jenkins, with a screenplay by Allan Heinberg, from a story by Heinberg, Zack Snyder, and Jason Fuchs, and stars Gal Gadot, Chris Pine, Robin Wright, Danny Huston, David Thewlis, Connie Nielsen, and Elena Anaya.\n\n[David Thewlis]\nHe has also done voice work in the films \"James and the Giant Peach\" (1996), \"The Miracle Maker\" (2000), and \"Anomalisa\" (2015).\n\n[Fargo (TV series)]\nThe series premiered on April 15, 2014, on FX, and follows an anthology format, with each season set in a different era, and with a different story and mostly new characters and cast, although there is minor overlap.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q2a9ef527c1",
  "kind": "yes/no",
  "text": "Claim: Presque Isle is the 3112 acre and most famous Pennsylvania state park that took over 11,000 to make due to the wave action of lake Erie.\n\nPassages:\n\n[History of Presque Isle]\nThe History of Presque Isle Pennsylvania began when Presque Isle was created by the wave action of Lake Erie over the course of the 11,000 years that have passed since the last ice age.\n\n[Presque Isle State Park]\nPresque Isle State Park is a 3112 acre Pennsylvania state park on an arching, sandy peninsula that juts into Lake Erie, 4 mi west of the city of Erie, in Millcreek Township, Erie County, Pennsylvania, in the United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf809969407",
  "kind": "yes/no",
  "text": "Claim: Richard Fleischer directed the film that chronicled Reverend Stephen Kaplan's attempt to prove that the Amityville Horror hauntings were a hoax.\n\nPassages:\n\n[Amityville 3-D]\nThe film was directed by Richard Fleischer and the script was written by David Ambrose (under the pseudonym William Wales).\n\n[Stephen Kaplan]\nHis overview of the Amityville Horror became the basis for the film Amityville 3-D that chronicles his attempt to prove the story was a hoax.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q476f23f4de",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "@ThePartridgePod Defrost the freezer with the cast of Hollyoaks. Any of them that wanted an extra fun trip could pop to the recycling centre with some empty pesto jars. Magic.",
   "I would actually answer the question - 'Who would you want to spend a bank holiday with?' with an answer that I meant. I would be worried that people would mock me if I was honest though - I don't care when the tweet is clearly a joke."
  ]
 },
 {
  "qid": "q8ef67648ae",
  "kind": "yes/no",
  "text": "Claim: Tommy's Honour was a drama film that included the actor who found success with the 1962 BBC miniseries War & Peace.\n\nPassages:\n\n[Jack Lowden]\nJack Andrew Lowden (born 2 June 1990) is a Scottish stage, television, and film actor. Following a highly successful and award-winning four-year stage career, his first major international onscreen success was in the 2016 BBC miniseries \"War & Peace\", which led to starring roles in feature films.\n\n[Tommy's Honour]\nThe film is directed by Jason Connery, and the father and son are portrayed by Peter Mullan and Jack Lowden.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8129939f5e",
  "kind": "yes/no",
  "text": "Claim: The band that collaborated with Neva Dinova on the album \"One Jug of Wine, Two Vessels\" is a rock band from America. As is the band that were on the album Dracula 2000 (soundtrack).\n\nPassages:\n\n[Dracula 2000 (soundtrack)]\nThe soundtrack contains music from heavy rock/metal artists, including Pantera, Disturbed, Powerman 5000, Godhead with Marilyn Manson, System of a Down, Linkin Park, Taproot, Hed Planet Earth, Saliva, and many more.\n\n[Bright Eyes (band)]\nBright Eyes is an American indie rock band founded by singer-songwriter and guitarist Conor Oberst.\n\n[Disturbed (band)]\nDisturbed is an heavy metal band from Homer Glen, Illinois, formed in 1996.\n\n[One Jug of Wine, Two Vessels]\nOne Jug of Wine, Two Vessels is a collaborative split EP by Bright Eyes and Neva Dinova.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q11f6d18fd3",
  "kind": "yes/no",
  "text": "Text: how close i am to losing it. https://t.co/iQ5onEyYhb",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q8ce3f19ee8",
  "kind": "yes/no",
  "text": "Claim: The person who deposed Bernard Coard formed a military government with himself as chairman to rule Grenada, after the killing of a Grenadian politician who was the leader of New Jewel Movement that was an effort in the areas of socio-economic development, education, and black liberation.\n\nPassages:\n\n[Hudson Austin]\nAfter the killing of Maurice Bishop, he formed a military government with himself as chairman to rule Grenada.\n\n[Bernard Coard]\nCoard launched a coup within the revolutionary government and took power for three days until he was himself deposed by General Hudson Austin.\n\n[Maurice Bishop]\nMaurice Rupert Bishop (29 May 1944 – 19 October 1983) was a Grenadian politician and the leader of New Jewel Movement – popular efforts in the areas of socio-economic development, education, and Black liberation – that came to power during the 13 March 1979 revolution that removed Eric Gairy from office.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9a1b3fcb28",
  "kind": "yes/no",
  "text": "Claim: Wellingrove, New South Wales is 20 miles northwest of the parish and town in New England NSW.\n\nPassages:\n\n[Glen Innes, New South Wales]\nGlen Innes is a parish and town on the Northern Tablelands, in the New England region of New South Wales, Australia.\n\n[Wellingrove, New South Wales]\nWellingrove is a village located on the Wellingrove Road about 20 kilometres north west of Glen Innes, New South Wales on the Northern Tablelands, New South Wales, Australia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q0d1c4621d3",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "eurovision belongs to everyone!",
   "so many people pressed that italy won sorry eurovision belongs to the bisexuals now x #Eurovision"
  ]
 },
 {
  "qid": "q4d87efc923",
  "kind": "yes/no",
  "text": "Text: zoom university is destroying my mental health✌️",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qacb65b76fe",
  "kind": "yes/no",
  "text": "Claim: The actor Chris Hemsworth, one of the stars in the horror film Thor: The Dark World, is Australian born.\n\nPassages:\n\n[Thor: The Dark World]\nThor: The Dark World is a 2013 American superhero film based on the Marvel Comics character Thor, produced by Marvel Studios and distributed by Walt Disney Studios Motion Pictures. It stars Chris Hemsworth, Natalie Portman, Tom Hiddleston, Anthony Hopkins, Stellan Skarsgård, Idris Elba, Christopher Eccleston, Adewale Akinnuoye-Agbaje, Kat Dennings, Ray Stevenson, Zachary Levi, Tadanobu Asano, Jaimie Alexander, and Rene Russo.\n\n[Chris Hemsworth]\nChris Hemsworth (born 11 August 1983) is an Australian actor.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
