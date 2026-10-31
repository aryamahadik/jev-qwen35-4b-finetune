# A46 replay label-noise blind read RSAS06-blind_read-ee5d083f-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS06-blind_read-ee5d083f-003.json

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
  "qid": "qdf07d0aaf7",
  "kind": "yes/no",
  "text": "Claim: A Pottawatomie massacre event known was Bleeding Kansas was largely brought about by the Missouri Compromise and the act which created the terrirtories of Kansas and Nebraska and was combated by the Republican Party.\n\nPassages:\n\n[History of the United States Republican Party]\nThe Republican Party, also commonly called the GOP (for \"Grand Old Party\"), is one of the world's oldest extant political parties. It emerged in 1854 to combat the Kansas–Nebraska Act, an act that dissolved the terms of the Missouri Compromise and allowed slave or free status to be decided in the territories by popular sovereignty.\n\n[Kansas–Nebraska Act]\n277 ) created the territories of Kansas and Nebraska and was drafted by Democratic Senator Stephen A. Douglas of Illinois and President Franklin Pierce.\n\n[Pottawatomie massacre]\nBleeding Kansas was largely brought about by the Missouri Compromise and the Kansas–Nebraska Act.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q430e8da8c1",
  "kind": "yes/no",
  "text": "Claim: Neither the winner of the women's singles event in the 1980 Austrian Open nor Andy Murray participate as a professional tennis player.\n\nPassages:\n\n[1980 Austrian Open (tennis)]\nFirst-seeded Guillermo Vilas won the men's singles title and the accompanying $13,000 first-prize money while Virginia Ruzici won the women's singles event.\n\n[Andy Murray]\nSir Andrew Barron Murray, {'1': \", '2': \", '3': \", '4': \"} (born 15 May 1987) is a British professional tennis player from Scotland currently ranked world no. 3 in men's singles.\n\n[Virginia Ruzici]\nVirginia Ruzici (born 31 January 1955) is a former professional tennis player from Romania.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q61837f69a2",
  "kind": "yes/no",
  "text": "Claim: Alexandre Aja directed a horror comedy. The director of the mockumentary The Life Coach participated in screenwriting that horror comedy film.\n\nPassages:\n\n[Josh Stolberg]\nHe also co-wrote the scripts for \"Man-Witch\" (starring Jack Black and directed by Todd Phillips), the remakes of \"Piranha 3D\" (directed by Alexandre Aja) and \"House on Sorority Row\", the book adaptation of \"The Spellman Files\", produced by Laura Ziskin, as well as the book adaptation of \"The Candy Shop Wars\".\n\n[Piranha 3D]\nPiranha 3D is a 2010 American 3D horror comedy film that serves as a loose remake of the 1978 horror film \"Piranha\".\n\n[The Life Coach]\nThe Life Coach is a 2005 mockumentary directed by Josh Stolberg.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q69c8e2f786",
  "kind": "yes/no",
  "text": "Claim: The Guardians of the Galaxy, are a fictional spacefaring superhero team, appearing in American comic books published by Marvel Comics. Until it was discontinued due to low sales in 1983, it had an an initial roster, including fictional superhero, Groot, who first appeared in \"Tales to Astonish\" #13 (November 1960).\n\nPassages:\n\n[Guardians of the Galaxy (2008 team)]\nDan Abnett and Andy Lanning formed the team from existing and previously unrelated characters created by a variety of writers and artists, with an initial roster of Star-Lord, Rocket Raccoon, Quasar, Adam Warlock, Gamora, Drax the Destroyer and Groot.\n\n[Groot]\nGroot ( ) is a fictional superhero appearing in American comic books published by Marvel Comics.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc6144a3311",
  "kind": "yes/no",
  "text": "Claim: This individual is co-founder of Recess Records alongside Jason White (musician). He and the band that released Fahizah, have being in a band in common.\n\nPassages:\n\n[Pinhead Gunpowder]\nPinhead Gunpowder is an American punk rock band that formed in East Bay, California, in 1990.\n\n[Jason White (musician)]\nHe is also the guitarist/vocalist for the Californian punk band Pinhead Gunpowder, lead guitarist/lead vocalist for California, and co-founder of Adeline Records alongside Billie Joe Armstrong.\n\n[Fahizah]\nFahizah is the second EP by the American punk rock band Pinhead Gunpowder.\n\n[Billie Joe Armstrong]\nBillie Joe Armstrong (born February 17, 1972) is an American musician, singer, songwriter and actor who is best known as the lead vocalist, primary songwriter, and guitarist of the punk rock band Green Day, which he co-founded with Mike Dirnt.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q61f119dbcc",
  "kind": "yes/no",
  "text": "Claim: Gangkhar Puensum is higher than Jongsong Peak.\n\nPassages:\n\n[Gangkhar Puensum]\nGangkhar Puensum (Dzongkha: གངས་དཀར་སྤུན་གསུམ་ \"Kangkar Punsum \", alternatively, Gangkar Punsum or Gankar Punzum) is the highest mountain in Bhutan and a strong candidate for the highest unclimbed mountain in the world with an elevation of 7570 m and a prominence of 2995 m .\n\n[Jongsong Peak]\nAt 7462 m it is the 57th highest peak in the world, although it is dominated by 3rd highest, Kangchenjunga, 20 km to the south.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9924f5b964",
  "kind": "yes/no",
  "text": "Claim: This 2010 American comedy-drama film stars an American actor born July 26, 1959. Danny Comden also stars in it.\n\nPassages:\n\n[Father of Invention]\nFather of Invention is a 2010 American comedy-drama film directed by Trent Cooper, and stars Kevin Spacey, Camilla Belle and Johnny Knoxville.\n\n[Kevin Spacey]\nKevin Spacey Fowler, KBE (born July 26, 1959) is an American actor, film director, producer, screenwriter, and singer.\n\n[Danny Comden]\nHe also appeared in \"Father of Invention\", \"Dunston Checks In\", \"Breakin' All the Rules\" and \"Dirt.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q49884ca2bf",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "apparently it's the biggest ask on the planet to find decently priced sandals with an enclosed toe. PLEASE, INTERNET. I just want to have vaguely summery shoes that don't involve me having my toes out to the world at all times lmfaoo",
   "I'm finding it hard to buy affordable enclosed toe sandals on the internet."
  ]
 },
 {
  "qid": "q6e522b42c2",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "Life is about happiness and friendship",
   "Life is about eating chicken finger and getting drunk"
  ]
 },
 {
  "qid": "q5e59c9342f",
  "kind": "yes/no",
  "text": "Claim: The referee of the 28 May 2011 football match at Wembley Stadium participated in the 2010 FIFA World Cup.\n\nPassages:\n\n[Viktor Kassai]\nViktor Kassai (\"Kassai Viktor\", : ; born 10 September 1975) is a Hungarian football referee. He participated in the 2010 FIFA World Cup and refereed the 2011 UEFA Champions League Final.\n\n[2011 UEFA Champions League Final]\nThe 2011 UEFA Champions League Final was a football match played on 28 May 2011 at Wembley Stadium in London that decided the winner of the 2010–11 season of the UEFA Champions League.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q738e671c96",
  "kind": "yes/no",
  "text": "Claim: The airline that was affected by the 1931 Avro Ten Southern Cloud disappearance was founded by the person who made the first trans-Pacific flight in 1928.\n\nPassages:\n\n[Australian National Airways (1930)]\nAustralian National Airways was a short-lived Australian airline, founded in 1929 by Charles Kingsford Smith and Charles Ulm.\n\n[1931 Avro Ten Southern Cloud disappearance]\nThe Southern Cloud, registered VH-UMF, was one of five Avro 618 Ten three-engined aircraft flying daily airline services between several Australian cities for Australian National Airways in the early 1930s.\n\n[Charles Kingsford Smith]\nIn 1928, he earned global fame when he made the first trans-Pacific flight from the United States to Australia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q13b15f4651",
  "kind": "yes/no",
  "text": "Tweet: Whoever’s toddler ass sprayed the entire toilet backstage, I hope you stub your toe and bite your tongue really hard. also you were clearly dehydrated, go drink some damn water like an adult",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q12f8dba43a",
  "kind": "yes/no",
  "text": "Claim: Washington-native John Stanley Carroll has been educated at Saint Mary's University, the University of Hawaii at Hilo, one of the ten branches of the University of Hawaii.\n\nPassages:\n\n[John Carroll (Hawaii politician)]\nHe is a lawyer, having been educated at Saint Mary's University, the University of Hawaii at Hilo and the University of Hawaii at Manoa.\n\n[University of Hawaii at Hilo]\nIt is one of ten branches of the University of Hawaiʻ i system.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa03ec13517",
  "kind": "yes/no",
  "text": "Claim: PDQ Chocolate is a registered trademark of Associated British Foods and was first established in 1957.\n\nPassages:\n\n[Ovaltine]\nOvaltine, a registered trademark of Associated British Foods, is made by Wander AG, a subsidiary of Twinings which acquired the brand from Novartis in 2002, except in the United States where Nestlé acquired the rights separately from Novartis later on.\n\n[PDQ Chocolate]\nPDQ Chocolate was a popular drink mix in the 1960s and 1970s. It was manufactured by Ovaltine.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q865ede589d",
  "kind": "yes/no",
  "text": "Claim: The 44th annual Berlin International Film Festival was held from February 10 to 21,1994, during which the summer 1993 courtroom drama film, In the Name of the Father, was awarded a Golden Bear.\n\nPassages:\n\n[44th Berlin International Film Festival]\nThe Golden Bear was awarded to British-Irish film \"In the Name of the Father\" directed by Jim Sheridan.\n\n[In the Name of the Father (film)]\nIn the Name of the Father is a 1993 Irish-British-American biographical courtroom drama film co-written and directed by Jim Sheridan.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q1df5b08a78",
  "kind": "yes/no",
  "text": "Tweet: if trees would simply stop producing flammable leaves climate change would not be an issue",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qcbe8b72cd3",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Jim I put some money and didi and lost some money and now am being forced to live below my usual means",
   "@jimcramer Yo jim I put my life savings in $didi at $16 as per your request now me and my family are eating MREs in full survival mode What should I do?"
  ]
 },
 {
  "qid": "q5a79bfaac4",
  "kind": "yes/no",
  "text": "Claim: Matt Miller (musician) plays bass in a band. This band and King Charles are not both from the same country.\n\nPassages:\n\n[King Charles (musician)]\nKing Charles (born Charles Costa, 6 May 1985) is a singer-songwriter from West London.\n\n[Matt Miller (musician)]\nMatt Miller is a native of El Paso, Texas and the bassist for the Post-hardcore band, Sparta.\n\n[Sparta (band)]\nSparta is an American rock band from El Paso, Texas, formed in 2001.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2bb227cf2f",
  "kind": "yes/no",
  "text": "Claim: The Walkley Heights ymca was built in 1854, located on land that was the home of a prison.\n\nPassages:\n\n[Yatala Labour Prison]\nIt was built in 1854 to enable prisoners to work at the creek, quarrying rock for roads and construction.\n\n[Walkley Heights, South Australia]\nThe suburb is located on land formerly comprising the prison farm for Yatala Labour Prison, and includes fifty-five hectares of land formerly owned by R. M. Williams which was compulsorily acquired during the time of former State Premier Sir Thomas Playford.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qfa18e436ff",
  "kind": "yes/no",
  "text": "Claim: The major benefactor who donated money to build the sport facility, which was replaced by the Manley Field House, sold his oil company to the John D Rockefeller's Xavier University.\n\nPassages:\n\n[John Dustin Archbold]\nHis small oil company was bought out by John D Rockefeller's Standard Oil Company.\n\n[Archbold Gymnasium]\nIt was built in 1908 with money donated by John Dustin Archbold, a major benefactor of the university, who also funded the building of Archbold Stadium, just to the west of the gymnasium (now the site of the Carrier Dome).\n\n[Manley Field House]\nIt was built to replace the old Archbold Gymnasium, which had served for almost 60 years prior.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8db2165e6a",
  "kind": "yes/no",
  "text": "Claim: Sakis Rouvas played the voice of Quasimodo in a Notre Dame's animated movie. Saludos Amigos was released before that film.\n\nPassages:\n\n[Sakis Rouvas filmography]\nSakis Rouvas filmed his first cinematographic works in 1996, playing the voice of Quasimodo in the Greek language dubbing of the Disney animated adaptation of \"The Hunchback of Notre Dame\" titled \"I Panayia Ton Parision.\"\n\n[Saludos Amigos]\nSaludos Amigos (Spanish for \"Greetings, Friends\") is a 1942 American live-action animated package film produced by Walt Disney and released by RKO Radio Pictures.\n\n[The Hunchback of Notre Dame (1996 film)]\nThe Hunchback of Notre Dame is a 1996 American animated musical drama film produced by Walt Disney Feature Animation for Walt Disney Pictures.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2b87c01007",
  "kind": "yes/no",
  "text": "Claim: An athlete played defense for the team Rodney Hannah plays for. The college this athlete played at is located in Louisiana.\n\nPassages:\n\n[Everson Walls]\nHe played college football at Grambling State University.\n\n[1983 Dallas Cowboys season]\nHowever, the defense gave up many points, despite strong play from Randy White, Ed \"Too Tall\" Jones, and Everson Walls.\n\n[Rodney Hannah]\nRodney Dee Hannah II (born August 9, 1987) is a former American football tight end in the National Football League for the Dallas Cowboys.\n\n[Grambling State University]\nGrambling State University (GSU) is a historically black, public, coeducational university, located in Grambling, Louisiana.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6f4037510d",
  "kind": "yes/no",
  "text": "Claim: The 2010 population of the city where a newspaper was published is 114,297. This newspaper once had physician Ronald Clair Roat as a featured writer.\n\nPassages:\n\n[Lansing State Journal]\nThe Lansing State Journal is a daily newspaper published in Lansing, Michigan owned by Gannett.\n\n[Lansing, Michigan]\nLansing is the capital of the US state of Michigan. It is mostly in Ingham County, although portions of the city extend west into Eaton County and north into Clinton County. The 2010 Census placed the city's population at 114,297, making it the fifth largest city in Michigan.\n\n[Ronald Clair Roat]\nThe newspapers included the \"Lansing State Journal\", \"Dominion News\" (Morgantown, W.Va.) , \"Dayton Daily News\", and \"The Times\" in Frankfort, Ind.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3f02d6fce1",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Unfortunately, 143 by Bobby Brackens was my song with my middle school boyfriend.",
   "oh also, my song with my middle school boyfriend was “143” by Bobby Brackins!! i really peaked geez"
  ]
 },
 {
  "qid": "qbda5f9c4f1",
  "kind": "yes/no",
  "text": "Claim: This young person contributed artwork to the 2008-2009 Superman: New Krypton story. They are also known for illustrative work on a DC Comics publication titled after the superhero whose adversary is Killer Frost.\n\nPassages:\n\n[Jamal Igle]\nThe creator of the comic book series Molly Danger he is also known for his pencilling, inking and coloring work on books such as \"Supergirl\" and \"Firestorm\".\n\n[Superman: New Krypton]\n\"New Krypton\" is a 2008-2009 Superman story arc written by Geoff Johns, James Robinson, and Sterling Gates with art by Gary Frank, Alex Ross, Renato Guedes, Jamal Igle and Pete Woods and published by DC Comics.\n\n[Killer Frost]\nKiller Frost appeared formerly as an adversary of the superhero Firestorm but is now a member of the new Justice League of America that started with the DC Rebirth in 2016.\n\n[Firestorm (comics)]\nFirestorm is the name of several fictional superheroes appearing in American comic books published by DC Comics.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5d251c9541",
  "kind": "yes/no",
  "text": "Claim: The Genesis Flood: The Biblical Record and its Scientific Implications was written in 1961 by one of the founders of the Creation Research Society.\n\nPassages:\n\n[Henry M. Morris]\nHenry Madison Morris (October 6, 1918 – February 25, 2006) was an American young Earth creationist, Christian apologist, and engineer. He is widely known for coauthoring \"The Genesis Flood\" with John C. Whitcomb in 1961.\n\n[The Genesis Flood]\nThe Genesis Flood: The Biblical Record and its Scientific Implications is a 1961 book by young earth creationists John C. Whitcomb and Henry M. Morris that, according to Ronald Numbers, elevated young earth creationism \"to a position of fundamentalist orthodoxy.\"",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qab1cfd8e3b",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "\"Not happy i have been compared to a brick wall\".",
   "Nice to be compared to a brick wall 😂"
  ]
 },
 {
  "qid": "qb841c45343",
  "kind": "yes/no",
  "text": "Claim: In 2011 the population of the town where the band with a compilation double album called 24 Carat Purple were formed was about 26,000.\n\nPassages:\n\n[Hertford]\nForming a civil parish, the 2011 census put the population of Hertford at about 26,000.\n\n[24 Carat Purple]\n24 Carat Purple is the first compilation album of the hard rock band Deep Purple released worldwide on their own record company and the third in a long line of compilation albums.\n\n[Deep Purple]\nDeep Purple are an English rock band formed in Hertford in 1968.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q909beedd5e",
  "kind": "yes/no",
  "text": "Claim: The Japanese military base that functioned as a World War II armament storage depot and is located near Seal Islands was established in 1942.\n\nPassages:\n\n[Concord Naval Weapons Station]\nConcord Naval Weapons Station was a military base established in 1942 north of the city of Concord, California at the shore of the Sacramento River where it widens into Suisun Bay. The station functioned as a World War II armament storage depot, supplying ships at Port Chicago.\n\n[Seal Islands (California)]\nSeal Islands are a pair of islands in Suisun Bay at the mouth of the Sacramento-San Joaquin River Delta in Contra Costa County, California, 10 km east of Benicia, and 500 metres off-shore from the former Concord Naval Weapons Station and Port Chicago Naval Magazine.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q33e27085ea",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Thanks @myhermes for losing my parcel but giving me someone else's. I'm nice enough to go give it to them though. Please DM me back soon 😐",
   "I am unhappy that you have lost my parcel"
  ]
 },
 {
  "qid": "q22621bc67e",
  "kind": "yes/no",
  "text": "Claim: Glenn Martin Hughes attended high school in Mineola, New York.\n\nPassages:\n\n[Glenn Hughes (Village People)]\nHe graduated in 1968 from Chaminade High School, then attended Manhattan College, where he was initiated as a member of Phi Mu Alpha Sinfonia music fraternity in 1969.\n\n[Chaminade High School]\nChaminade High School is a Roman Catholic college preparatory high school for boys in Mineola, New York, United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q1332aea14a",
  "kind": "yes/no",
  "text": "Text: im gonna keep believing that andrew and tobey arent in nwh so if it doesnt happen i wont be disappointed but if it does i will scream and cry and mostly scream",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qd675217c5a",
  "kind": "yes/no",
  "text": "Claim: Milo Parker starred in the 2014 movie Robot Overlords alongside Gillian Anderson.\n\nPassages:\n\n[Milo Parker]\nMilo Parker (born 2002) is a British child actor, known for his roles as Connor in \"Robot Overlords\", Roger Munro in \"Mr. Holmes\" and Hugh Apiston in \"Miss Peregrine's Home for Peculiar Children\".\n\n[Robot Overlords]\nRobot Overlords (originally titled Our Robot Overlords) is a 2014 British independent science fiction film, starring Callan McAuliffe, Ben Kingsley and Gillian Anderson.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0c609c626d",
  "kind": "yes/no",
  "text": "Claim: In regards to Value premium the expert who argued that no value premium exists, did not found The Vanguard Group.\n\nPassages:\n\n[John C. Bogle]\nHe is the founder and retired chief executive of The Vanguard Group.\n\n[Value premium]\nOther experts, such as John C. Bogle, have argued that no value premium exists, claiming that Fama and French's research is period dependent.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe6e8a0b27a",
  "kind": "yes/no",
  "text": "Text: know I told myself and my loved ones Id hold out longer but I don't think I can, this is it, I told myself I would do something else before Id do this again but you know lifes short and I want to watch the Sopranos for a 9th time #Sopranos",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q989e86c163",
  "kind": "yes/no",
  "text": "Claim: The group that released the live album Running on Ice started their band before this American band. North American Scum was performed by this band.\n\nPassages:\n\n[Running on Ice]\nRunning on Ice is the second album by Vertical Horizon, released independently in 1995, and later re-released by RCA.\n\n[Vertical Horizon]\nVertical Horizon is an American alternative rock band formed at Georgetown University in Washington, D.C. in 1991.\n\n[LCD Soundsystem]\nLCD Soundsystem is an American rock band from Brooklyn, New York, formed in 2002.\n\n[North American Scum]\n\"North American Scum\" is a song by American rock band LCD Soundsystem.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb46b62adf4",
  "kind": "yes/no",
  "text": "Claim: A film starred Mahek Chahal, an actress who was born on 1 February 1979. Sachein is a film that is based on this film.\n\nPassages:\n\n[Neetho]\nNeetho (English: \"With You\" ) is a 2002 Telugu romance film directed by John Mahendran, starring Prakash Kovelamudi and Mahek Chahal in their debut roles.\n\n[Mahek Chahal]\nMahek Chahal (born 1 February 1979) is a Norwegian actress and model who appears in Bollywood films.\n\n[Sachein]\nBased on the director's earlier Telugu film \"Neetho\" (2002), the film is produced by Kalaipuli S. Dhanu and has the score and soundtrack composed by Devi Sri Prasad.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5017e049e6",
  "kind": "yes/no",
  "text": "Claim: Batman: Knight Gallery was a short-lived comic book that featured art from the artist best known for work on \"Starman\" and \"Robin\".\n\nPassages:\n\n[Tom Lyle]\nThomas \"Tom\" Lyle (born November 2, 1953) is an American comics artist who is best known as for his work on \"Starman\" and \"Robin\" for DC Comics.\n\n[Batman: Knight Gallery]\nWritten by Doug Moench, and features the art of Thomas Grummett, Michael Manley, Vincent Giarrano, James Balent, Bret Blevins, Graham Nolan, Norm Breyfogle, Neal Adams, George Pérez, Stephen De Stefano, Tom Lyle, Gary Frank, David Taylor, Anton Furst.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5417c68776",
  "kind": "yes/no",
  "text": "Claim: The series that the American character actor best-known for playing General Hammond starred in the first episode was Twin Peaks.\n\nPassages:\n\n[Episode 8 (Twin Peaks)]\n\"Episode 8\", also known as \"May the Giant Be with You\", is the first episode of the second season of the American mystery television series \"Twin Peaks\".\n\n[Don S. Davis]\nDon Sinclair Davis, PhD (August 4, 1942 – June 29, 2008) was an American character actor best-known for playing General Hammond in the television series \"Stargate SG-1\" (1997–2007), and earlier for playing Major Garland Briggs on the television series \"Twin Peaks\" (1990–1991).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q7367fbbfc0",
  "kind": "yes/no",
  "text": "Claim: Natalie Anne Merchant has a wider scope of profession than Marian Gold.\n\nPassages:\n\n[Natalie Merchant]\nNatalie Anne Merchant (born October 26, 1963) is an American singer-songwriter and musician.\n\n[Marian Gold]\nHartwig Schierbaum (born 26 May 1954), better known by his stage name Marian Gold, is the lead singer of the German synthpop group Alphaville, and has also recorded as a solo artist.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4e8e58558c",
  "kind": "yes/no",
  "text": "Claim: Ernst & Young is the 220-year-old multinational professional services firm, headquartered in London, England, that is one of the \"Big Four\" accounting firms and is also a tenant in the hub of the \"Hub and Spoke Model\" where InfoPark Thrissur is one of the spokes.\n\nPassages:\n\n[Ernst &amp; Young]\nEY (formerly Ernst & Young) is a multinational professional services firm headquartered in London, England. EY is one of the largest professional services firms in the world and is one of the \"Big Four\" accounting firms.\n\n[InfoPark, Kochi]\nInfopark, Kochi (Malayalam: ഇൻഫോപാർക്ക് കൊച്ചി) is an information technology park situated in the city of Kochi, Kerala, India. The notable tenants in the park include native giants like Tata Consultancy Services, Cognizant, Wipro, IBS Software Services etc and foreign corporations like KPMG, Ernst & Young, EXL, Etisalat, UST Global, Nielsen Audio, Xerox, Conduent, Fingent etc.\n\n[InfoPark Thrissur]\nThis is the first information technology park in the state that has become operational under the 'Hub and Spoke Model', where InfoPark, Kochi acts as the hub and InfoPark Koratty as the spoke.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q08cb2dbc28",
  "kind": "yes/no",
  "text": "Claim: The head of the Imperial Family that was making a broadcast announcement of Japan's surrender in 1945 was the leader for whom Yoshihiro Tokugawa worked.\n\nPassages:\n\n[Emperor of Japan]\nThe Emperor of Japan is the head of the Imperial Family and the traditional head of state of Japan.\n\n[Masahiko Takeshita]\nIn August 1945, he helped plan a \"coup\" along with Major Kenji Hatanaka and a handful of others , with the intent of preventing the Emperor's announcement of Japan's surrender from being broadcast.\n\n[Yoshihiro Tokugawa]\nThe grandson of Tokugawa Yoshikatsu, the last lord of Owari han, he served as Grand Chamberlain of Japan from 1985 to 1988, serving as the Emperor of Japan's personal adviser.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q0c21c9a553",
  "kind": "yes/no",
  "text": "Claim: This groups sixth full-length album was called Jinsei×Boku=. The vocalist of that group and Doug Pinnick have band in common.\n\nPassages:\n\n[One Ok Rock]\nThe band currently consists of Takahiro Moriuchi (vocals), Toru Yamashita (guitar/leader), Ryota Kohama (bass), and Tomoya Kanki (drums).\n\n[Doug Pinnick]\nDouglas Theodore \"Doug\" Pinnick (born September 3, 1950), sometimes stylized as dUg Pinnick or simply dUg, is an American musician best known as the bass guitarist, songwriter, and co-lead vocalist for the hard rock/progressive metal band King's X.\n\n[Takahiro Moriuchi]\nTakahiro Moriuchi (森内 貴寛 , Moriuchi Takahiro , born April 17, 1988 in Tokyo) , known professionally as Taka, is the lead vocalist of the Japanese rock band ONE OK ROCK.\n\n[Jinsei×Boku=]\n\"Life Times Me Equals\") is the sixth full-length album by the Japanese rock band, One Ok Rock.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7e53c6ffcc",
  "kind": "yes/no",
  "text": "Claim: Francois de Fleury served in a cavalry battle in the American Revolutionary War in June of 1778. Henry Monckton was killed during that battle.\n\nPassages:\n\n[Henry Monckton]\nHe was killed leading his soldiers at the Battle of Monmouth on 28 June 1778.\n\n[Battle of Monmouth]\nThe Battle of Monmouth was an American Revolutionary War battle fought on June 28, 1778, in Monmouth County, New Jersey.\n\n[François de Fleury]\nHe served during the Monmouth Campaign in June 1778 and fought in Rhode Island in August.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q356e85ce69",
  "kind": "yes/no",
  "text": "Claim: The brand where Lauren Gold, who is most recognised as the DJ in Robbie Williams's \"Rock DJ\" music video as well as her recurring appearance in the company's ad campaigns, is currently owned by a fashion retailer based in Columbus, Ohio.\n\nPassages:\n\n[Lauren Gold]\nGold is most recognised as the DJ in Robbie Williams's \"Rock DJ\" music video as well as her recurring appearance in La Senza ad campaigns.\n\n[L Brands]\nL Brands Inc. (formerly known as \"Limited Brands Inc\" and \"The Limited Inc.\") is an American fashion retailer based in Columbus, Ohio.\n\n[La Senza]\nThe La Senza brand is currently owned by L Brands which operates and owns La Senza stores in Canada and uses a franchise model for the operation of stores outside Canada.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2ab7359414",
  "kind": "yes/no",
  "text": "Claim: This band released Echelons in March 1987. They were formed before the band Aaroh.\n\nPassages:\n\n[For Against]\nFor Against is a United States post-punk/dream pop band from Lincoln, Nebraska. Despite numerous lineup shuffles and some periods of dormancy, the band has produced material steadily from its 1984 inception to the present.\n\n[Aaroh]\nAaroh (Urdu: آروح, literal English translation: \"the ascending scale in eastern classical music\") is an alternative rock band from Karachi, Sindh, Pakistan, formed in 1998.\n\n[Echelons]\nEchelons is the debut studio album by American rock band For Against, released in 1987 by record label Independent Project.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q83a1ec26cb",
  "kind": "yes/no",
  "text": "Claim: Airbus A380 is the system that uses the one of the bootloaders that is available in JFFS2, is a wide-body, four-engine jet airliner manufactured by European manufacturer Airbus.\n\nPassages:\n\n[Airbus A380]\nThe Airbus A380 is a double-deck, wide-body, four-engine jet airliner manufactured by European manufacturer Airbus.\n\n[JFFS2]\nJFFS2 is also available for a few bootloaders, like Das U-Boot, Open Firmware, the eCos RTOS and the RedBoot.\n\n[RedBoot]\nRedBoot (an acronym for Red Hat Embedded Debug and Bootstrap firmware) is an open source application that uses the eCos real-time operating system Hardware Abstraction Layer to provide bootstrap firmware for embedded systems. RedBoot is used in both product development and in deployed products in the field, such as the entertainment systems on the Airbus A380s and Delta's Boeing 767.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf97ac0b997",
  "kind": "yes/no",
  "text": "Claim: Judy Hample is a former chancellor of this educational organization. The organization and State University System of this state, for which Elwyn Thomas was a Supreme Court Justice from 1938 to 1969, have the United States in common.\n\nPassages:\n\n[Florida Board of Regents]\nThe Florida Board of Regents was from 1965 to 2001 the governing body for the State University System of Florida, which includes all public universities in the state of Florida, United States.\n\n[Elwyn Thomas]\nElwyn Thomas (July 5, 1894 – February 15, 1971) was a Florida judge, and a Justice of the Florida Supreme Court from 1938 to 1969.\n\n[State University System of Florida]\nThe State University System of Florida (SUS, or SUSF out-of-state) is a system of twelve public universities in the U.S. state of Florida.\n\n[Judy Hample]\nShe is the former chancellor of the Pennsylvania State System of Higher Education and the Florida Board of Regents.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd0e4ab1e95",
  "kind": "yes/no",
  "text": "Claim: Bogjurgan Hill is part of a region of Lorraine, France that includes the 14th-century towerhouse Fetteresso Castle.\n\nPassages:\n\n[Fetteresso Castle]\nFetteresso Castle is a 14th-century towerhouse, rebuilt in 1761 as a Scottish gothic style Palladian manor, with clear evidence of prehistoric use of the site.\n\n[Bogjurgan Hill]\nHistorical features in this region of Kincardineshire include Fetteresso Castle, Drumtochty Castle and Muchalls Castle.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7fb12d11eb",
  "kind": "yes/no",
  "text": "Claim: Lorentz & Sakarias is a hip-hop duo from Stockholm, Sweden, which has collaborated with Swedish actor Gustaf Caspar Orm Skarsgård during the summer of 2009.\n\nPassages:\n\n[Lorentz &amp; Sakarias]\nThey have collaborated with jj, Duvchi, Newkid and Gustaf Skarsgård.\n\n[Gustaf Skarsgård]\nGustaf Caspar Orm Skarsgård (] ; born 12 November 1980) is a Swedish actor.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
