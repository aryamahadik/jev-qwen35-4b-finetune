# A46 replay label-noise blind read RSAS09-blind_read-472e34f4-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS09-blind_read-472e34f4-007.json

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
  "qid": "q8546dd22e9",
  "kind": "yes/no",
  "text": "Claim: The water body where the shikara is found is further south than Waterton Lake.\n\nPassages:\n\n[Waterton Lake]\nWaterton Lake is a mountain lake in southern Alberta, Canada and northern Montana, United States.\n\n[Dal Lake]\nDal is a lake in Srinagar (Dal Lake is a misnomer as Dal in Kashmiri means lake), the summer capital of Jammu and Kashmir.\n\n[Shikara]\nThe shikara is a type of wooden boat found on Dal Lake and other water bodies of Srinagar, Jammu & Kashmir, India.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qce4e8ae71b",
  "kind": "yes/no",
  "text": "Text: Excited to present some research, listen to some studies and learn some stats at the #PsyPAG2021 conference :)",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q4ece7c0a17",
  "kind": "yes/no",
  "text": "Claim: Lowell Edwin Jones teaches mathematics at a school. That school is further North than where Bonnie Newman was the interim president of.\n\nPassages:\n\n[Bonnie Newman]\nNewman was also interim president of the University of New Hampshire (UNH) and the Community College System of New Hampshire.\n\n[Lowell Edwin Jones]\nLowell Jones (born 1945) is an American professor of mathematics at Stony Brook University Jones' primary fields of interest are topology, and geometry.\n\n[University of New Hampshire]\nThe University of New Hampshire (UNH) is a public research university in the University System of New Hampshire, in the United States.\n\n[Stony Brook University]\nThe State University of New York at Stony Brook (also known as Stony Brook University or SUNY Stony Brook) is a public sea-grant and space-grant research university located in Stony Brook, New York in the United States.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qa1957a65ab",
  "kind": "yes/no",
  "text": "Claim: The director of All the Love You Cannes! and not Jay T. Wright, was the American filmmaker who co-founded Troma Entertainment film studio.\n\nPassages:\n\n[All the Love You Cannes!]\nis a 2002 documentary film directed by Lloyd Kaufman.\n\n[Jay T. Wright]\nThis tension acts, in many of his films, as a competing motive and sometimes in direct conflict with any idea of narrative.\n\n[Lloyd Kaufman]\nStanley Lloyd Kaufman, Jr. (born December 30, 1945) is an American film director, producer, screenwriter, and actor. With producer Michael Herz, he is the co-founder of Troma Entertainment film studio, and the director of many of their feature films, including \"The Toxic Avenger\" and \"Tromeo and Juliet\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe41f514a1a",
  "kind": "yes/no",
  "text": "Claim: Operation Neptune was not the code name of The landing barge primarily used to provide hot meals to the landing crew.\n\nPassages:\n\n[Landing Barge, Kitchen]\nIts primary purpose was to provide hot meals to the crews of the many minor landing craft not fitted with galley facilities.\n\n[Normandy landings]\nThe Normandy landings (codenamed Operation Neptune) were the landing operations on Tuesday, 6 June 1944 (termed D-Day) of the Allied invasion of Normandy in Operation Overlord during World War II.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa473baf208",
  "kind": "yes/no",
  "text": "Claim: The English former professional footballer who played as a centre-back with Chris Jones, was born by c-section 7 November 1978.\n\nPassages:\n\n[Rio Ferdinand]\nRio Gavin Ferdinand (born 7 November 1978) is an English former professional footballer who played as a centre-back, and current television pundit for BT Sport.\n\n[Chris Jones (footballer, born 1985)]\nChris Jones is a Welsh semi-professional footballer currently playing for Cymru Alliance side Porthmadog. He made several appearances for Leeds and was heavily involved with the first team.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q55c9f595cc",
  "kind": "yes/no",
  "text": "Claim: Arthur Hiller was born before the writer and director of underground 1999's no budget film I Was a Teenage Serial Killer.\n\nPassages:\n\n[Arthur Hiller]\nArthur Hiller, OC (November 22, 1923 – August 17, 2016) was a Canadian-American television and film director, having directed over 33 films during his 50-year career.\n\n[Sarah Jacobson]\nSarah Jacobson (August 25, 1971, Norwalk, Connecticut – February 13, 2004 New York City) was an independent filmmaker who wrote, produced, and filmed her own movies.\n\n[I Was a Teenage Serial Killer]\nI Was a Teenage Serial Killer is an underground no budget film written and directed by \"The Queen of Underground Film\", Sarah Jacobson.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q14bb087453",
  "kind": "yes/no",
  "text": "Claim: A freeway that runs east-west through Bower in part of a country was named after an author. He was born 16 November 1920. Bossiaea walkeri is a flowering plant found in this part of a country.\n\nPassages:\n\n[Colin Thiele]\nColin Milton Thiele AC ( ; 16 November 1920 – 4 September 2006) was an Australian author and educator.\n\n[Thiele Highway]\nIt is named after author Colin Thiele who lived most of his life in towns along the route, and set some of his stories in the area.\n\n[Bossiaea walkeri]\nIt occurs in Western Australia, South Australia, Victoria and New South Wales.\n\n[Bower, South Australia]\nBower is a town in South Australia, approximately halfway between Eudunda and Morgan on the Thiele Highway.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q8eb9c036e4",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "ANY PENSIONER AND 4 YEAR OLD WHO DARE TAKE ME ON AT DINOSAUR THEMED CRAZY GOLF WILL BE CRUSHED, CRUSHED I TELL YOU. https://t.co/yZlafy0lsd",
   "Had a great time playing crazy golf with the family, and I won!"
  ]
 },
 {
  "qid": "qc79251ff4b",
  "kind": "yes/no",
  "text": "Claim: Horror movie R-Point, set in Vietnam, was filmed partially in a location about 3 miles south-west of Povokvil Waterfalls.\n\nPassages:\n\n[Bokor Hill Station]\nIt was used as the location for the final showdown of the movie \"City of Ghosts\" (2002) and the 2004 film \"R-Point\".\n\n[Povokvil Waterfalls]\nIt is located about 3 mi north-east of Bokor Hill Station.\n\n[R-Point]\nSet in 1972 Vietnam, during the Vietnam War, it stars Kam Woo-sung and Son Byong-ho as members of the South Korean military in Vietnam.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q7ca5fe553e",
  "kind": "yes/no",
  "text": "Claim: The King that Gothard Wilhelm Butler was captain of the guard for was known by the name Jan Kazimierz in Poland.\n\nPassages:\n\n[John II Casimir Vasa]\nIn Poland, he is known and commonly referred as Jan Kazimierz.\n\n[Gothard Wilhelm Butler]\nHe was Grand treasurer of the Crown, the Crown court chamberlain and a captain of the guard of King John II Casimir Vasa and erderman of Prienai, Parnu and Bolesław.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q437d9527ee",
  "kind": "yes/no",
  "text": "Claim: Foday Saybana Sankoh was involved with the Sierra Leone rebel group Revolutionary United Front (RUF) during the conflict involving the Mende ethnic group that lasted over a decade.\n\nPassages:\n\n[Foday Sankoh]\nFoday Saybana Sankoh (17 October 1937 – 29 July 2003) was the founder and leader of the Sierra Leone rebel group Revolutionary United Front (RUF) in the 11-year-long Sierra Leone Civil War, starting in 1991 and ending in 2002.\n\n[Civil Defence Forces]\nThe Civil Defense Forces (CDF) was a paramilitary organization that fought in the Sierra Leone Civil War (1991–2002). Much of the CDF was made up of the Kamajors group, which is part of the larger Mende ethnic group.\n\n[Sierra Leone Civil War]\nThe Sierra Leone Civil War (1991–2002) began on 23 March 1991 when the Revolutionary United Front (RUF), with support from the special forces of Charles Taylor’s National Patriotic Front of Liberia (NPFL), intervened in Sierra Leone in an attempt to overthrow the Joseph Momoh government. The resulting civil war lasted 11 years, enveloped the country, and left over 50,000 dead.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7c1d0383e8",
  "kind": "yes/no",
  "text": "Claim: The man who coached The 1973 Indiana Hoosiers football team was born in May of 1935.\n\nPassages:\n\n[Lee Corso]\nLee Corso (born August 7, 1935) is an American sports broadcaster and football analyst for ESPN and former coach.\n\n[1973 Indiana Hoosiers football team]\nThe 1973 Indiana Hoosiers football team represented the Indiana Hoosiers in the 1973 Big Ten Conference football season. The team was coached by Lee Corso, in his first year as head coach of the Hoosiers.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa92f74f404",
  "kind": "yes/no",
  "text": "Claim: Faith Goldy got fired after an interview she gave on The Daily Stormer, the production site edited by Andrew Anglin.\n\nPassages:\n\n[Faith Goldy]\nFaith Julia Goldy (born 1989) is a Canadian right-wing writer and commentator. She was fired from The Rebel on August 17, 2017, in response to an interview she gave on \"The Krypto Report\", a podcast produced by the white supremacist site \"The Daily Stormer\".\n\n[The Daily Stormer]\nThe Daily Stormer is an American neo-Nazi and white supremacist news and commentary website. Its editor, Andrew Anglin, founded it on July 4, 2013 as a faster-paced replacement for his previous website \"Total Fascism\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qae071e1c2f",
  "kind": "yes/no",
  "text": "Claim: Northern, the British transport company, manages the station that serves a small town and civil parish in the Borough of Pendle Lancashire, England with a population of 8,200 as of 2011.\n\nPassages:\n\n[Brierfield railway station]\nBrierfield railway station serves the small town of Brierfield, Lancashire, England and is on the East Lancashire Line 2+1/4 mi east of Burnley Central railway station towards Colne (the terminus). The station is managed by Northern, who also provide all passenger trains serving it.\n\n[Brierfield, Lancashire]\nBrierfield is a small town and civil parish in the Borough of Pendle Lancashire, England. It has a population of 8,200, reducing marginally to 8,193 at the 2011 Census.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd2621c1979",
  "kind": "yes/no",
  "text": "Claim: A director has lived longer in the Mongolia than the writer of Absolute Evil – Final Exit. One of the films this director worked on was Two in the Dark.\n\nPassages:\n\n[Benjamin Stoloff]\nBenjamin \"Ben\" Stoloff (October 6, 1895 – September 8, 1960) was an American film director and producer. Stoloff was born in Philadelphia, Pennsylvania. He died in Hollywood, California.\n\n[Absolute Evil]\nAbsolute Evil – Final Exit is a drama film written and directed by Ulli Lommel.\n\n[Two in the Dark]\nThe movie, about an amnesiac suspected of murder, was directed by Benjamin Stoloff.\n\n[Ulli Lommel]\nSince 1977 he has lived and worked in the USA, where he has written, directed and starred in over 50 movies.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qd7c3daaf62",
  "kind": "yes/no",
  "text": "Text: if i saw a capybara in person id probably throw up",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q8c568b5acf",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "wow this growth spurt is really taking longer than i thought haha",
   "I am short."
  ]
 },
 {
  "qid": "q0263be9b45",
  "kind": "yes/no",
  "text": "Claim: The writer of historical romance fiction to whom an 1850s novel was dedicated was born in London, England. The novel was one of four including \"A Countess Below Stairs\", \"The Reluctant Heiress\", and \"The Morning Gift\".\n\nPassages:\n\n[A Company of Swans]\nThe book is dedicated to Patricia Veryan.\n\n[A Song for Summer]\nThis novel and four others (\"A Countess Below Stairs\", \"A Company of Swans\", \"The Reluctant Heiress\", and \"The Morning Gift\") were reissued between 2007 and 2009 for the young adult market.\n\n[Patricia Veryan]\nPatricia Valeria Bannister, (born November 21, 1923 in London, England; died November 18, 2009 in Bellevue, Washington, USA) was a writer of historical romance fiction from 1978 until 2002.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qea1e59b491",
  "kind": "yes/no",
  "text": "Claim: The former Oklahoma City mayor that features alongside Kevin Ogle on Flashpoint, is five years younger than Tom Coburn.\n\nPassages:\n\n[Kirk Humphreys]\nKirk Humphreys (born September 13, 1950) is an American politician who served as Mayor of Oklahoma City from April 9, 1998 to November 3, 2003.\n\n[Tom Coburn]\nThomas Allen \"Tom\" Coburn (born March 14, 1948) is an American politician and medical doctor.\n\n[Kevin Ogle]\nOgle also serves as moderator of the locally-produced Sunday morning political affairs talk show \"Flashpoint\", alongside panelists Mike Turpen and former Oklahoma City mayor Kirk Humphreys.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qcb3477fc52",
  "kind": "yes/no",
  "text": "Claim: Istanbul, Turkey features Endem TV Tower, a 257 m tall tower which once included a revolving restaurant 154 m above ground as well as Cagaloglu Hamam, the last of its kind public hamam built in 1741 to raise revenue by a library.\n\nPassages:\n\n[Cağaloğlu Hamam]\nThe Cağaloğlu Hamam, finished in 1741, is the last hamam to be built in the Ottoman Empire. It was constructed in Istanbul Eminönü, in Alemdar, on Hilal-i Ahmer street as a public hamam to raise revenue for the library of Sultan Mahmud I, previously situated inside the mosque of Ayasofya. It is the last example of its kind to be built in Istanbul and is still operational today.\n\n[Endem TV Tower]\nEndem TV Tower is a TV tower in Beylikdüzü, Istanbul, Turkey. It was built between 1998 and 2002, and has a now closed revolving restaurant 154 m above ground, as well as an observation deck at 160 m . The total height of the tower si 257 m including the antenna.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q19189007ec",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Unhappy birthday to me",
   "Happy birthday to me. I got pinged and can't leave the house 🥰🤡"
  ]
 },
 {
  "qid": "q89bfe87f5d",
  "kind": "yes/no",
  "text": "Claim: The auditorium where Backstreet Boys: Larger Than Life residency show perfomed at is located in the Planet Hollywood Resort & Casino in Las Vegas, Nevada. This auditorium is located at a hotel and casino owned by the William Jefferson Clinton Federal Building.\n\nPassages:\n\n[Planet Hollywood Las Vegas]\nIt is owned and operated by Caesars Entertainment Corporation.\n\n[The AXIS]\nThe AXIS (known as The AXIS powered by Monster for sponsorship purposes, also referred to as the AXIS Theater) is a mid-sized auditorium located at Planet Hollywood Las Vegas on the Las Vegas Strip.\n\n[Backstreet Boys: Larger Than Life]\nBackstreet Boys: Larger Than Life is the first residency show by American vocal group Backstreet Boys, performed at The AXIS auditorium located in the Planet Hollywood Resort & Casino in Las Vegas, Nevada.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc6f98efd35",
  "kind": "yes/no",
  "text": "Post: the way uni won’t give me extra time on assessments despite them replacing exams (which i get time for) because of covid 🤩🤩🥰😍",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q7d3b8b7281",
  "kind": "yes/no",
  "text": "Claim: A news publication, which named a woman in its list of top global tinkers, was founded in 1970. The woman translated \"Time for Outrage!\" into English.\n\nPassages:\n\n[Time for Outrage!]\nby the French diplomat, member of the French Resistance and concentration camp survivor Stéphane Hessel.\n\n[Foreign Policy]\nForeign Policy is an American news publication, founded in 1970 and focused on global affairs, current events, and domestic and international policy.\n\n[Stéphane Hessel]\nIn 2011 he was named by \"Foreign Policy\" magazine in its list of top global thinkers.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qebbdcd8e73",
  "kind": "yes/no",
  "text": "Claim: Canadian author William P. Young hit the New York Times Best Seller list in 2017, with a book published 10 year prior.\n\nPassages:\n\n[The New York Times Fiction Best Sellers of 2017]\nThis is a list of adult fiction books that topped \"The New York Times\" Fiction Best Seller list in 2017, in the Combined Print & E-Book Fiction category. So far, the most frequent weekly best seller of the year is \"Camino Island\" by John Grisham with 5 weeks at the top of the list, followed by \"The Shack\" by William P. Young with 4 weeks.\n\n[The Shack]\nThe Shack is a novel by Canadian author William P. Young that was published in 2007.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qcf06d24158",
  "kind": "yes/no",
  "text": "Claim: \"Mona Leaves-a\" is the episode on the animated show \"The Simpsons\" in which Mona Penelope Simpson died.\n\nPassages:\n\n[I, (Annoyed Grunt)-bot]\nThis episode represents a milestone in the history of the series as Snowball II is killed off, which, excluding the death of Homer's mother in season 19's \"Mona Leaves-a\", is to date the closest thing to an actual Simpson family member actually being killed off.\n\n[Mona Simpson (The Simpsons)]\nMona Penelope Simpson (née Olsen) is a recurring fictional character in the animated television series \"The Simpsons\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb138396532",
  "kind": "yes/no",
  "text": "Claim: Ken Howard starred as an American attorney in the HBO film created by the same director of an upcoming American Romantic drama call Every Day. Every Day is based on a the thriller by David Leviathan.\n\nPassages:\n\n[Phelan Beale]\nPhelan Beale (May 23, 1881 – June 12, 1956) was an American attorney and sportsman in New York City who was married to Edith Ewing Bouvier, an aunt of Jacqueline Kennedy Onassis.\n\n[Every Day (upcoming film)]\nEvery Day is an upcoming American romantic-drama directed by Michael Sucsy and based on the novel by David Levithan which was adapted by Jesse Andrews.\n\n[Michael Sucsy]\nHe is best known for creating the HBO film \"Grey Gardens\".\n\n[Grey Gardens (2009 film)]\nGrey Gardens is an HBO film about the lives of Edith Bouvier Beale/\"Little Edie\", played by Drew Barrymore, and her mother Edith Ewing Bouvier/\"Big Edie\", played by Jessica Lange. Co-stars include Jeanne Tripplehorn as Jacqueline Kennedy (Little Edie's cousin) and Ken Howard as Phelan Beale (Little Edie's father).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb37ea7da49",
  "kind": "yes/no",
  "text": "Claim: The 2007 FIFA U-20 World Cup was the sixteenth edition of the FIFA U-20 World Cup (formerly called FIFA World Youth Championship), hosted by Canada held from 30 June to 22 July 2007, Argentine goal player Sergio Aguero was given the FIFA U-20 Golden Shoe.\n\nPassages:\n\n[Sergio Agüero]\nSergio Leonel \"Kun\" Agüero (] ; born 2 June 1988) is an Argentine professional footballer who plays as a striker for Premier League club Manchester City and the Argentina national team.\n\n[2007 FIFA U-20 World Cup]\nThe 2007 FIFA U-20 World Cup was the sixteenth edition of the FIFA U-20 World Cup (formerly called FIFA World Youth Championship), hosted by Canada from 30 June to 22 July 2007.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2e0aa480c6",
  "kind": "yes/no",
  "text": "Claim: Samuel Ray Delany Jr. has short stories which covered more topics than the author of Star Wars: The Force Awakens (novel), a novelisation of the first \"Star Wars\" film.\n\nPassages:\n\n[Star Wars: The Force Awakens (novel)]\nThe author, Alan Dean Foster, also wrote \"\", the 1976 novelization of the first \"Star Wars\" film.\n\n[Alan Dean Foster]\nAlan Dean Foster (born November 18, 1946) is an American writer of fantasy and science fiction, a prolific creator of and contributor to book series as well as the author of more than 20 standalone novels. He is especially prolific in his novelizations of film scripts.\n\n[Samuel R. Delany]\nSamuel Ray Delany Jr. ( ; born April 1, 1942), Chip Delany to his friends, is an American author, professor and literary critic. His work includes fiction (especially science fiction), memoir, criticism, and essays on sexuality and society.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q96551c2a4c",
  "kind": "yes/no",
  "text": "Claim: Biographic is a weekly comics feature by award-winning Irish cartoonist and illustrator Steve McGarry: the feature is syndicated by Universal Uclick and appears in such publications as The Toronto Sun, an English-language daily tabloid newspaper published in Toronto, Ontario, Canada.\n\nPassages:\n\n[Biographic (comics)]\nLaunched in 2005, the feature is syndicated by Universal Uclick and appears in such publications as the \"New York Daily News\", the \"Boston Herald\", the \"Toronto Sun\", Hong Kong's \"Daily Young Post\", India's \"Mail Today\", Tokyo's \"Mainichi Weekly\", the \"Bangkok Post Student Weekly\", and South Africa's \"People Magazine\".\n\n[Toronto Sun]\nThe Toronto Sun is an English-language daily tabloid newspaper published in Toronto, Ontario, Canada.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q09bb037413",
  "kind": "yes/no",
  "text": "Claim: Filmmakers Chris Carter and Theo van Gogh do not share the same nationality.\n\nPassages:\n\n[Chris Carter (screenwriter)]\nChristopher Carl Carter (born October 13, 1956) is an American television and film producer, director and writer.\n\n[Theo van Gogh (film director)]\nTheodoor \"Theo\" van Gogh (] ; 23 July 19572 November 2004) was a Dutch film director, film producer, television director, television producer, television presenter, screenwriter, actor, critic and author.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qba0f62a154",
  "kind": "yes/no",
  "text": "Claim: March 13, 2013 is the start date of the tour that was the third concert tour by an Japanese singer-songwriter and was completed in support of the album that has \"State of Grace\" (Taylor Swift song).\n\nPassages:\n\n[Red (Taylor Swift album)]\nRed is the fourth studio album by American singer-songwriter Taylor Swift. Swift completed The Red Tour in support of the album on June 12, 2014, which became the highest-grossing tour of all time by a country artist, grossing over $150 million.\n\n[The Red Tour]\nThe Red Tour was the third concert tour by American singer-songwriter Taylor Swift. Launched in support of Swift's fourth studio album, \"Red\" (2012), the tour began on March 13, 2013 in Omaha, Nebraska and concluded on June 12, 2014 in Singapore.\n\n[State of Grace (Taylor Swift song)]\n\"State of Grace\" is a song by American singer-songwriter Taylor Swift from her fourth studio album \"Red\" (2012).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6e27e66077",
  "kind": "yes/no",
  "text": "Claim: The magazine, which had Jean-Louis Comolli as its editor in chief from 1966 to 1978, was founded in the year 1951 in Norway.\n\nPassages:\n\n[Jean-Louis Comolli]\nHe was editor in chief of \"Cahiers du cinéma\" from 1966 to 1978, during which period he wrote the influential essays \"Machines of the Visible\" (1971) and \"Technique and Ideology: Camera, Perspective, Depth of Field\" (1971-2), both of which have been translated in English anthologies of film and media studies.\n\n[Cahiers du cinéma]\nCahiers du Cinéma (] , \"Notebooks on Cinema\") is a French film magazine founded in 1951 by André Bazin, Jacques Doniol-Valcroze and Joseph-Marie Lo Duca.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qf843e33cdd",
  "kind": "yes/no",
  "text": "Text: i had a dream nev from catfish tried to murder me",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qfc8e3a2721",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "The Drew Barrymore show is one of the worst TV shows ever produced.",
   "The Drew Barrymore Show is an absolute trainwreck. Like The Tony Danza Show, every two minutes is a clip for The Soup."
  ]
 },
 {
  "qid": "q8bbdb10db2",
  "kind": "yes/no",
  "text": "Tweet: who thinks me and sam should start a band called 'teeth at midnight' 🦷🌙",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q5308eda3da",
  "kind": "yes/no",
  "text": "Tweet: Trader Joe’s orange chicken is lowkey better than the orange chicken at most Seattle area Chinese restaurants",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q690a8bb9c4",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "Buy something that is of value, either stocks or other long-term investments",
   "@ray_harren @tkinsonn buy really rare pokemon card"
  ]
 },
 {
  "qid": "q5745d8b320",
  "kind": "yes/no",
  "text": "Claim: Mogens Palle brought to Denmark a World Lightweight Champion from Shooto.\n\nPassages:\n\n[Mogens Palle]\nMogens Palle (born 14 March 1934) is a Danish professional boxing promoter and manager. He also brought to Denmark boxing stars like Carlos Monzon, Larry Holmes, Emile Griffith, Ken Buchanan and John Conteh.\n\n[Ken Buchanan]\nKen Buchanan MBE (born 28 June 1945) is a British retired professional boxer and the former Undisputed World Lightweight Champion from Edinburgh.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0c36b5756f",
  "kind": "yes/no",
  "text": "Tweet: People who drive under the speed limit. Death Penalty.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q0ffda995d4",
  "kind": "yes/no",
  "text": "Claim: The writer and director of Beloved Rogues and David Fincher are both directors.\n\nPassages:\n\n[David Fincher]\nDavid Andrew Leo Fincher (born August 28, 1962) is an American director and producer, notably for films, television series and music videos.\n\n[Alfred Santell]\nAlfred Allen Santell also known as Al Santell (born September 14, 1895 in San Francisco, California) was an American film director and film producer.\n\n[Beloved Rogues]\nBeloved Rogues is a 1917 American silent comedy-drama film directed and written by Alfred Santell with the storyline by Aaron Hoffman.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q01e6d58540",
  "kind": "yes/no",
  "text": "Tweet: just met the love of my life don't text",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q2353ea464e",
  "kind": "yes/no",
  "text": "Claim: Aloinopsis is a floral plant. The close relative of another genus is also a plant. Aruncus dioicus is a species in this genus.\n\nPassages:\n\n[Aloinopsis]\nAloinopsis is a genus of ice plants from South Africa.\n\n[Aruncus]\nThey are closely related to the genera \"Filipendula\" and \"Spiraea\", and are native to mountainous damp woodland in temperate regions of the Northern Hemisphere.\n\n[Filipendula]\nFilipendula is a genus of 12 species of perennial herbaceous flowering plants in the family Rosaceae, native to the temperate regions of the Northern Hemisphere.\n\n[Aruncus dioicus]\n(known as goat's beard, buck's-beard or bride's feathers) is a flowering herbaceous perennial plant in the family Rosaceae, and is the type species of the genus \"Aruncus\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qfc69f07123",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "When your @Apple delivery gets stolen by a UK Mail delivery driver and the police know who it is but I still don’t get taken seriously🙃🙃🙃",
   "I wish that the person who stole my laptop would be arrested"
  ]
 },
 {
  "qid": "q153de8ff73",
  "kind": "yes/no",
  "text": "Claim: The Greek surrealist poet that wrote Capitale de la douleur was from the same country as this author. Laurence Bataille was the daughter of this man.\n\nPassages:\n\n[Capitale de la douleur]\nCapitale de la douleur (\"Capital of Pain\") is a book of poems by French surrealist poet Paul Éluard.\n\n[Georges Bataille]\nGeorges Albert Maurice Victor Bataille (] ; 10 September 1897 – 9 July 1962) was a French intellectual and literary figure working in literature, philosophy, anthropology, economics, sociology and history of art.\n\n[Paul Éluard]\nPaul Éluard (] ), born Eugène Émile Paul Grindel (] ; 14 December 1895 – 18 November 1952), was a French poet and one of the founders of the surrealist movement.\n\n[Laurence Bataille]\nShe was the only daughter of the writer Georges Bataille and the actress Sylvia Bataille.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q26ab6e9613",
  "kind": "yes/no",
  "text": "Claim: Symphony No. 1 (Walton) is is one of two symphonies by an English composer. The composer of the Piano Concerto for the Left Hand (Ravel) was born before the composer of Symphony No. 1.\n\nPassages:\n\n[Symphony No. 1 (Walton)]\nThe Symphony No. 1 in B♭ minor is one of two symphonies by the English composer William Walton.\n\n[William Walton]\nSir William Turner Walton, OM (29 March 19028 March 1983) was an English composer.\n\n[Maurice Ravel]\nJoseph Maurice Ravel (] ; 7 March 1875 – 28 December 1937) was a French composer, pianist and conductor.\n\n[Piano Concerto for the Left Hand (Ravel)]\nThe Piano Concerto for the Left Hand in D major was composed by Maurice Ravel between 1929 and 1930, concurrently with his Piano Concerto in G. It was commissioned by the Austrian pianist Paul Wittgenstein, who lost his right arm during World War I.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc6153f0caf",
  "kind": "yes/no",
  "text": "Claim: Finity's End was written by American writer Carolyn Janice Cherry.\n\nPassages:\n\n[Finity's End]\nFinity's End is a science fiction novel written by the American science fiction and fantasy author C. J. Cherryh.\n\n[C. J. Cherryh]\nCarolyn Janice Cherry (born September 1, 1942), better known by the pen name C. J. Cherryh, is an American writer of speculative fiction.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc4e263691a",
  "kind": "yes/no",
  "text": "Tweet: I just had to call and explain to my bank that the 3 donations this past week to the @WWF were not fraudulent charges and that I did in fact intent to make them😅",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qf225702adf",
  "kind": "yes/no",
  "text": "Claim: The Phoenix Suns 2013-2014 season had players including a Slovenian who plays at both the point guard and shooting guard positions.\n\nPassages:\n\n[2013–14 Phoenix Suns season]\nThe 2013–14 NBA season was the Phoenix Suns' 46th season in the NBA. When the Suns began the regular season, Goran Dragić, P. J. Tucker, Markieff Morris, and his twin brother Marcus Morris were the only players returning from playing with last season's team (while Channing Frye was still on last season's team, he didn't play any games due to a life-threatening heart ailment he had at the time).\n\n[Goran Dragić]\nGoran Dragić (born 6 May 1986) is a Slovenian professional basketball for the Miami Heat of the National Basketball Association (NBA). He plays at both the point guard and shooting guard positions.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 }
]
