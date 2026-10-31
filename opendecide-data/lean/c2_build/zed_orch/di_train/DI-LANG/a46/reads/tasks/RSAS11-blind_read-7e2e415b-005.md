# A46 replay label-noise blind read RSAS11-blind_read-7e2e415b-005

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS11-blind_read-7e2e415b-005.json

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
  "qid": "qd9455b91bd",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Got locked out of Twitter for saying it’s embarrassing to be an arsenal fan. That’s not okay, but people can be abusive and racist and nothing?!? Okay! 🤣🙄",
   "I don’t appreciate being banned for using the word embarrasing, when others can be racist/homophobic and it’s okay"
  ]
 },
 {
  "qid": "q5a54e432b0",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Just getting some WD40 on my letter box to help the poor postman with his delivery today #valentinesday2021 #WD40",
   "Fed up of seeing forced romance, don't be told when to do something nice for a person you love."
  ]
 },
 {
  "qid": "q826f6ae13f",
  "kind": "yes/no",
  "text": "Claim: The breed of Rottweiler that Spike from Old Yeller was, not the Tibetan Terrier, is a type of gun dog.\n\nPassages:\n\n[Spike (dog)]\nSpike was a lop-eared yellow Mastador (Mastiff/ Labrador Retriever mix) and a dog actor best known for his performance as Old Yeller in the 1957 Disney film of the same name co-starring Tommy Kirk, Dorothy McGuire, Fess Parker, and Kevin Corcoran.\n\n[Tibetan Terrier]\nSome old travelers' accounts refer to the dog as Dokhi Apso or \"outdoor\" Apso, indicating a shaggy or bearded working dog which lives outdoors.\n\n[Labrador Retriever]\nThe Labrador Retriever, also Labrador, is a type of retriever-gun dog.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1827d9495d",
  "kind": "yes/no",
  "text": "Claim: The writer of American Oxygen also worked on a track with Eminem which was released in 2010.\n\nPassages:\n\n[Alex da Kid]\nHe has gained recognition for producing several hit singles for a plethora of artists in various music genres, such as Dr. Dre (\"I Need a Doctor\"), Nicki Minaj (\"Massive Attack\"), B.o.B (\"Airplanes\" featuring Hayley Williams), Eminem (\"Love the Way You Lie\" featuring Rihanna), Diddy (\"Coming Home\" with Dirty Money featuring Skylar Grey), Imagine Dragons (\"Radioactive\") and Cheryl (\"Under The Sun\").\n\n[Love the Way You Lie]\n\"Love the Way You Lie\" is a song recorded by the American rapper Eminem, featuring the Barbadian singer Rihanna, from Eminem's seventh studio album \"Recovery\" (2010).\n\n[American Oxygen]\nIt was written by Alex da Kid, Candice Pillay, Sam Harris and Rihanna; Alex da Kid and Kanye West produced it.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q068542545e",
  "kind": "yes/no",
  "text": "Claim: Shahzeb Khanzada's show \"To The Point\" is shown in Urdu.\n\nPassages:\n\n[Express News (Pakistan)]\nExpress News is an Urdu language Pakistani television news channel Based in karachi, launched on January 1, 2008.\n\n[Shahzeb Khanzada]\nHe hosted the talk show \"To The Point\" on Express News from 2011 to 2014 and has hosted the talk show \"Aaj Shahzeb Khanzada Kay Sath\" on Geo News since January 2015.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q3321c4a517",
  "kind": "yes/no",
  "text": "Claim: Sudha Kheterpal who is musician best know as the percussionist in Faithless has played with Kylie Ann Minogue who is recognized at the highest-selling Australian artist of all time by the Australian Recording industry Association.\n\nPassages:\n\n[Sudha Kheterpal]\nSudha Kheterpal is a British-Indian musician best known as the percussionist in Faithless.\n\n[Kylie Minogue]\nKylie Ann Minogue, ( ; born 28 May 1968), often known simply as Kylie, is an Australian singer, songwriter, dancer and actress. She is recognised as the highest-selling Australian artist of all time by the Australian Recording Industry Association (ARIA).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q293225d575",
  "kind": "yes/no",
  "text": "Claim: Harlan County, USA was directed and produced by Barbara Kopple, She also directed the 1969 festival production, along with Michael Wadleigh. Harlan County and another of her films have the documentary film in common.\n\nPassages:\n\n[Harlan County, USA]\nDirected and produced by Barbara Kopple, who has long been an advocate of workers' rights, \"Harlan County, U.S.A.\" is less ambivalent in its attitude toward unions than her later \"American Dream\", the account of the Hormel Foods strike in Austin, Minnesota in 1985-86.\n\n[American Dream (film)]\nAmerican Dream is a 1990 \"cinéma vérité\" documentary film directed by Barbara Kopple and co-directed by Cathy Caplan, Thomas Haneke, and Lawrence Silk.\n\n[Michael Wadleigh]\nMichael Wadleigh, also known as Michael Wadley (born September 24, 1942 in Akron, Ohio), is an American film director and cinematographer renowned for his groundbreaking documentary of the 1969 Woodstock Festival, \"Woodstock\".\n\n[Woodstock (film)]\nWoodstock is a 1970 documentary film of the watershed counterculture Woodstock Festival which took place in August 1969 near Bethel, New York. \"",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q55290d2fa3",
  "kind": "yes/no",
  "text": "Tweet: don’t make me rewatch panic 🤨",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q0291a6c2ec",
  "kind": "yes/no",
  "text": "Claim: The battle in which John W. Minick won the Medal of Honor lasted longer than Battle of Pusan Perimeter.\n\nPassages:\n\n[Battle of Pusan Perimeter]\nThe Battle of Pusan Perimeter was a large-scale battle between United Nations and North Korean forces lasting from August 4 to September 18, 1950.\n\n[Battle of Hürtgen Forest]\nThe Battle of Hürtgen Forest (German: \"Schlacht im Hürtgenwald\" ) was a series of fierce battles fought from 19 September to 16 December 1944 between American and German forces on the Western Front during World War II in the Hürtgen Forest about 50 mi2 east of the Belgian–German border.\n\n[John W. Minick]\nHe was a United States Army soldier and a recipient of the United States military's highest decoration—the Medal of Honor—for his actions during the Battle of Hürtgen Forest in World War II.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0c6a00e656",
  "kind": "yes/no",
  "text": "Claim: This author wrote Chilly Scenes of Winter. The author and the writer of a collection of two short novels The Oakdale Affair and The Rider are not dating.\n\nPassages:\n\n[Ann Beattie]\nAnn Beattie (born September 8, 1947) is an American novelist and short story writer.\n\n[Chilly Scenes of Winter]\nChilly Scenes of Winter is Ann Beattie's first novel, published by Doubleday in September, 1976.\n\n[The Oakdale Affair and The Rider]\nThe Oakdale Affair and The Rider is a collection of two short novels by Edgar Rice Burroughs.\n\n[Edgar Rice Burroughs]\nEdgar Rice Burroughs (September 1, 1875 – March 19, 1950) was an American fiction writer best known for his celebrated and prolific output in the adventure and science-fiction genres.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q51b8cfe3af",
  "kind": "yes/no",
  "text": "Claim: This author was published by Jack Shoemaker. She and the author of the 1995 novel Mrs. Ted Bliss are not both non-fiction writers.\n\nPassages:\n\n[Jack Shoemaker]\nShoemaker has published books by Guy Davenport, Romulus Linney, Gary Snyder, Wendell Berry, Evan S. Connell, MFK Fisher, James Salter, Gina Berriault, Reynolds Price, W.S. Merwin, Michael Palmer, Donald Hall, Anne Lamott, Kay Boyle, Gary Nabhan, Jane Vandenburgh, Carole Maso, and Robert Aitken.\n\n[Anne Lamott]\nAnne Lamott (born April 10, 1954) is an American novelist and non-fiction writer.\n\n[Mrs. Ted Bliss]\nMrs. Ted Bliss is a 1995 novel by American author Stanley Elkin, published by Hyperion Books.\n\n[Stanley Elkin]\nStanley Lawrence Elkin (May 11, 1930 – May 31, 1995) was an American novelist, short story writer, and essayist. His extravagant, satirical fiction revolves around American consumerism, popular culture, and male-female relation between each other.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9a863c1997",
  "kind": "yes/no",
  "text": "Claim: The star of The Secret Agent starred in a film in 2006, directed by Shane Meadows.\n\nPassages:\n\n[The Secret Agent (TV series)]\nThe show stars Toby Jones, Vicky McClure, Stephen Graham and Ian Hart.\n\n[Stephen Graham]\nStephen Graham (born 3 August 1973) is an English film and television actor, known for his roles as Tommy in the film \" Snatch\" (2000), Andrew \"Combo\" Gascoigne in \"This Is England\" (2006) as well as its television sequels, \"This Is England '86\" (2010), \"This Is England '88\" (2011) and \"This Is England '90\" (2015), notorious bank robber Baby Face Nelson in \"Public Enemies\" (2009), Scrum in the \"Pirates of the Caribbean\" films and Al Capone in the HBO series \"Boardwalk Empire\".\n\n[This Is England]\nThis Is England is a 2006 British drama film written and directed by Shane Meadows.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa90511a970",
  "kind": "yes/no",
  "text": "Tweet: Fly 👏 the 👏 L 👏 \n\n#ThisIsMyCrew",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q899087187b",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Billionaires do not need anyone to speak up on their behalf.",
   "@andy_mansell72 @VicOtley @garry_whu @NiaAnts @davidschneider Finally someone is speaking up for the billionaires."
  ]
 },
 {
  "qid": "q23260d854f",
  "kind": "yes/no",
  "text": "Claim: The high-performance aftermarket tuning company specializes in German automotive marque Smart. The company designed an automobile drivetrain similar to the Smart Forstars.\n\nPassages:\n\n[Brabus]\nBRABUS GmbH, founded 1977 in Bottrop (Ruhr Area), Germany, is a high-performance aftermarket tuning company which specializes in Mercedes-Benz, Smart, Tesla and Maybach vehicles.\n\n[Smart (marque)]\nsmart Automobile (stylized and marketed as \"smart\") is a German automotive marque and division of Daimler AG, based in Böblingen, Germany.\n\n[Smart Forstars]\nIt also has an all-electric drivetrain, which is nearly identical to the one used in the Smart Brabus electric drive.\n\n[Brabus Bullit]\nThe Brabus Bullit is an automobile designed and made by Brabus.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q5d0c1ffeaf",
  "kind": "yes/no",
  "text": "Claim: Both Cocky and cockfights have the rooster in common.\n\nPassages:\n\n[Cockfight]\nA cockfight is a blood sport between two cocks, or gamecocks, held in a ring called a cockpit.\n\n[Cocky (mascot)]\nCocky is the costumed mascot of the University of South Carolina athletics teams. He represents a cartoon version of a gamecock (a fighting rooster).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0983d7a614",
  "kind": "yes/no",
  "text": "Claim: The locals consider the township of Stirling a suburb of a southern town. That town is represented by Rebekha Carina Che Sharkie, an Australian politician.\n\nPassages:\n\n[Crafers, South Australia]\nThe town of Crafers is in the Adelaide Hills to the south-east of Adelaide, South Australia. Although technically considered to be an outer suburb of Adelaide, with many residents commuting to the city to work, locals consider Crafers to be more a suburb of the nearby township of Stirling.\n\n[Division of Mayo]\nThe Division of Mayo is an Australian electoral division located to the east, south, south-east and south-west of Adelaide, South Australia. It takes in the Adelaide Hills, Fleurieu Peninsula and Kangaroo Island, including the towns of Bridgewater, Crafers, Echunga, Gumeracha, Hahndorf, Kingscote, Langhorne Creek, Lobethal, Macclesfield, Mount Barker, Myponga, Oakbank, Stirling, Strathalbyn, Victor Harbor, Woodside, Yankalilla, and part of Birdwood.\n\n[Rebekha Sharkie]\nRepresenting the Division of Mayo since defeating Liberal Jamie Briggs at the 2016 federal election, she is the first Nick Xenophon Team member to be elected to the Australian House of Representatives.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qde1aeb77cb",
  "kind": "yes/no",
  "text": "Claim: 1614 is the founding year of the public research university in the Netherlands, where Jan Borgman was a professor from 1968 to 1988.\n\nPassages:\n\n[University of Groningen]\nThe University of Groningen (abbreviated as UG; Dutch: \"Rijksuniversiteit Groningen\" , abbreviated as \"RUG\") is a public research university in the city of Groningen in the Netherlands. The university was founded in 1614 and is one of the oldest universities in the Netherlands as well as one of its largest.\n\n[Jan Borgman]\nJan Borgman (born 30 November 1929) is a Dutch astronomer and university administrator. He was professor of astronomical observation technique at the University of Groningen from 1968 to 1988.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q581d1d09bd",
  "kind": "yes/no",
  "text": "Post: Nothing screams “I’m a glamorous cosmopolitan woman” like following your dog down the street in the midst of winter, saying “go potty! Go POTTY!” over and over again.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qe87216a499",
  "kind": "yes/no",
  "text": "Claim: This Irish director directed Friendly Enemies. He was born before the director of The Midnight Flyer.\n\nPassages:\n\n[The Midnight Flyer]\nThe Midnight Flyer is a 1918 American short action drama film directed by George Marshall and starring Hoot Gibson.\n\n[George Marshall (director)]\nGeorge E. Marshall (December 29, 1891 – February 17, 1975) was an American actor, screenwriter, producer, film and television director, active through the first six decades of movie history.\n\n[Friendly Enemies]\nThe film was directed by Allan Dwan, adapted from a play of the same name by Aaron Hoffman and Samuel Shipman.\n\n[Allan Dwan]\nAllan Dwan (3 April 1885 – 28 December 1981) was a pioneering Canadian-born American motion picture director, producer and screenwriter.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q013ae1ce96",
  "kind": "yes/no",
  "text": "Claim: Chilhowee Inn was the last stop of the Knoxville and Augusta line of the Southern Railway System, and the starting point for the railroad is operated between Charleville-Mezieres and the pioneer Appalachian and resort community Elkmont, Tennessee.\n\nPassages:\n\n[Chilhowee Inn]\nThis was the last stop of the Knoxville and Augusta line of the Southern Railway System, and the starting point for the Little River Railroad.\n\n[Little River Railroad (Tennessee)]\nThe Little River Railroad is a historic class III railroad that operated between Maryville and Elkmont, Tennessee during the period 1901 to 1939.\n\n[Elkmont, Tennessee]\nThroughout its history, the valley has been home to a pioneer Appalachian community, a logging town, and a resort community.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8bc530777d",
  "kind": "yes/no",
  "text": "Claim: The area where People of the Fire was set is a place that has both Aitxuri and this kind of geological formations. The Woodbine Foundation overlies this area.\n\nPassages:\n\n[Woodbine Formation]\nThe Woodbine overlies the Maness Shale, Buda Limestone, or older rocks, and underlies the Eagle Ford Group or Austin Chalk.\n\n[Buda Limestone]\nThe Buda Limestone is a geological formation in the High Plains and Trans-Pecos regions of West Texas whose strata date back to the Late Cretaceous.\n\n[People of the Fire]\nIt dramatizes the transition of Native American culture from Paleo-Indian to Archaic as a result of climatic warming, set in the High Plains and Western Rockies region.\n\n[High Plains (United States)]\nThe southern region of the Western High Plains ecology region contains the geological formation known as Llano Estacado which can be seen from a short distance or from on satellite maps.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc9c8f59e8b",
  "kind": "yes/no",
  "text": "Claim: This Greek poet was born before the writer of Race Matters. His works were translated to English by David Connolly.\n\nPassages:\n\n[David Connolly (translator)]\nHe has translated poetry and novels from Greek to English, including writing by Nikiforos Vrettakos, Odysseas Elytis, Kiki Dimoula and Nikos Engonopoulos.\n\n[Cornel West]\nCornel Ronald West (born June 2, 1953) is an American philosopher, political activist, social critic, author, public intellectual, and prominent member of the Democratic Socialists of America.\n\n[Race Matters]\nRace Matters is a social sciences book by Cornel West.\n\n[Odysseas Elytis]\nOdysseas Elytis (Greek: Οδυσσέας Ελύτης , ] , pen name of Odysseas Alepoudellis, Greek: Οδυσσέας Αλεπουδέλλης ; 2 November 1911 – 18 March 1996) was regarded as a major exponent of romantic modernism in Greece and the world.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6c012a4b65",
  "kind": "yes/no",
  "text": "Tweet: \"Should I wear my lime green pants?\" dad its 4th of july...",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qa492986124",
  "kind": "yes/no",
  "text": "Claim: Dollar Days was the sixth track on award winning Bowie's twenty-fifth and final studio album. The album that was released was recorded in secret.\n\nPassages:\n\n[Death of David Bowie]\nOn 10 January 2016, English singer, songwriter and actor David Bowie died at his New York City apartment, having suffered from liver cancer for the previous 18 months. His death occurred two days after the release of his twenty-fifth studio album, \"Blackstar\", which coincided with his 69th birthday.\n\n[Blackstar (album)]\nThe album was largely recorded in secret between The Magic Shop and Human Worldwide Studios in New York City with Bowie's longtime co-producer Tony Visconti and a group of local jazz musicians.\n\n[Dollar Days]\nIt is the sixth track on Bowie's twenty-fifth and final studio album, \"Blackstar\", released on 8 January 2016.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q40cbd2ffff",
  "kind": "yes/no",
  "text": "Claim: The railway that reopened the line of Broadfield railway station, is a part of Summerseat and also runs between Heywood and The Don River Railway.\n\nPassages:\n\n[Summerseat railway station]\nSummerseat railway station is a preserved railway station that serves the village of Summerseat in Greater Manchester, England. It is part of the Heritage East Lancashire Railway (which runs for 12 miles from Heywood-Rawtenstall).\n\n[Broadfield railway station]\nThe line through the station has since been reopened by the heritage East Lancashire Railway, although the station itself remains disused.\n\n[East Lancashire Railway]\nThe East Lancashire Railway is a 12+1/2 mi heritage railway line in north west England which runs between Heywood and Rawtenstall with intermediate stations at Bury Bolton Street, Burrs Country Park , Summerseat, Ramsbottom and Irwell Vale.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q77b9333421",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I reckon I could have put that in the net Morelos sir",
   "That goal should have been easy for Morelos!"
  ]
 },
 {
  "qid": "qc022e6466f",
  "kind": "yes/no",
  "text": "Claim: Emil Scaria created the role of Gurnemanz in an opera that has more acts than Manon by Massenet.\n\nPassages:\n\n[Manon]\nManon (] ) is an \"opéra comique\" in five acts by Jules Massenet to a French libretto by Henri Meilhac and Philippe Gille, based on the 1731 novel \"L’histoire du chevalier des Grieux et de Manon Lescaut\" by the Abbé Prévost.\n\n[Parsifal]\nParsifal (WWV 111) is an opera in three acts by German composer Richard Wagner.\n\n[Emil Scaria]\nIn 1882 he created the role of Gurnemanz in \"Parsifal\" for Richard Wagner at Bayreuth.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q56aa780c26",
  "kind": "yes/no",
  "text": "Claim: The tour that Lungs Tour supported U2 in was a worldwide tour that had a round stage and had a song that had never before been performed live.\n\nPassages:\n\n[U2 360° Tour]\nThe U2 360° Tour was a worldwide concert tour by rock band U2. The concerts featured the band playing \"in the round\" on a circular stage, allowing the audience to surround them on all sides.\n\n[Lungs Tour]\nThey also supported U2 on their U2 360° Tour in 2011.\n\n[Electrical Storm (song)]\nU2 did not play the song live until 2 July 2009, when they performed it on the second concert of their U2 360° Tour in Barcelona.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe60f1cabb0",
  "kind": "yes/no",
  "text": "Claim: The Highland Park and Lake Burien Railway runs from Everett to a city in Pierce County.\n\nPassages:\n\n[Tacoma, Washington]\nTacoma ( ) is a mid-sized urban port city in and the county seat of Pierce County, Washington, United States.\n\n[Highland Park and Lake Burien Railway]\nThe Highland Park and Lake Burien Railway was a branch of the Interurban System that went from Everett to Tacoma in Washington state.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q40efe50117",
  "kind": "yes/no",
  "text": "Claim: The German poet and writer of Los heraldos negros was not a German national. Neither was the author of Tales of a Long Night.\n\nPassages:\n\n[Alfred Döblin]\nBruno Alfred Döblin (10 August 1878 – 26 June 1957) was a German novelist, essayist, and doctor, best known for his novel \"Berlin Alexanderplatz\" (1929).\n\n[Los heraldos negros]\n\"Los heraldos negros\" is the title of a collection of poems written by the Peruvian poet César Vallejo between the years 1915 and 1918 and published in July 1919.\n\n[Tales of a Long Night]\nTales of a Long Night (German: \"Hamlet oder Die lange Nacht nimmt ein Ende\" ) (1956) is the last novel of German author Alfred Döblin.\n\n[César Vallejo]\nCésar Abraham Vallejo Mendoza (March 16, 1892 – April 15, 1938) was a Peruvian poet, writer, playwright, and journalist.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q808327756b",
  "kind": "yes/no",
  "text": "Claim: The father of director Guðný Halldórsdóttir and psychonaut Timothy Leary are not from the same country.\n\nPassages:\n\n[Timothy Leary]\nTimothy Francis Leary (October 22, 1920 – May 31, 1996) was an American psychologist and writer known for advocating the exploration of the therapeutic potential of psychedelic drugs under controlled conditions.\n\n[Halldór Laxness]\nHalldór Kiljan Laxness (] ; born Halldór Guðjónsson; 23 April 1902 – 8 February 1998) was a twentieth-century Icelandic writer.\n\n[Guðný Halldórsdóttir]\nHer father was writer and 1955 Nobel prize winner Halldór Laxness, while her mother was writer and textile designer Auður Laxness.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q82bc213442",
  "kind": "yes/no",
  "text": "Claim: Bouvier des Ardennes is a breed of dog. The dog Maremma Sheepdog is similar to is also a breed.\n\nPassages:\n\n[Kuvasz]\nThe Kuvasz (] ), is an ancient breed of a livestock dog of Hungarian origin.\n\n[Bouvier des Ardennes]\nBouvier des Ardennes is a rare dog breed from Belgium.\n\n[Maremma Sheepdog]\nSimilar breeds include the Pyrenean Mountain Dog, the Kuvasz of Hungary, the Tatra of Poland, the Cuvac of Slovakia and the Šarplaninac (although not white), with all of which it may share a common ancestor; and the Akbash Dog of Turkey.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qcabcd40a85",
  "kind": "yes/no",
  "text": "Claim: Realex Payments provides services for this Irish bookmaker founded in Dublin Ireland in 1988.\n\nPassages:\n\n[Paddy Power]\nPaddy Power is an Irish bookmaker founded in 1988 in Dublin, Ireland.\n\n[Realex Payments]\nThe company provides a broad range of payment gateway services and processes transactions in excess of €35 billion per annum on behalf of more than 14,000 clients including Virgin Atlantic Airways, Vodafone Ireland, the AA, AXA Insurance, Paddy Power and Aer Lingus.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q37c4f7bbf1",
  "kind": "yes/no",
  "text": "Claim: Syngenta is a Swiss agribusiness that is a client of Martin Williams Advertising in NY.\n\nPassages:\n\n[Syngenta]\nSyngenta AG is a global Swiss agribusiness that produces agrochemicals and seeds.\n\n[Martin Williams Advertising]\nClients include Payless ShoeSource, Raymond James, Syngenta, Cargill, Marvin Windows, Simmons Bedding Company, and P.F. Chang.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q14d96929eb",
  "kind": "yes/no",
  "text": "Claim: This actor starred in the film The Magnificent Seven Ride. The director who gave him a role in \"For a Few Dollars More\" was Italian not Jon Paul Puno.\n\nPassages:\n\n[Lee Van Cleef]\nAfter suffering serious injuries in a car crash, Van Cleef began to lose interest in his apparently waning career by the time Sergio Leone gave him a major role in \"For a Few Dollars More\".\n\n[The Magnificent Seven Ride]\nIt stars Lee Van Cleef as Chris Adams, succeeding Yul Brynner and George Kennedy in the role.\n\n[Sergio Leone]\nSergio Leone (] ; 3 January 1929 – 30 April 1989) was an Italian film director, producer and screenwriter, credited as the inventor of the \"Spaghetti Western\" genre.\n\n[Jon Paul Puno]\nJon Paul Puno (born 1985) is an American filmmaker and classical crossover singer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3bd5d26c7e",
  "kind": "yes/no",
  "text": "Claim: The highway that ends at the rock barrier for Heckscher State Park in Great River is located on Long Island in New York.\n\nPassages:\n\n[Heckscher State Parkway]\nThe Heckscher State Parkway (formerly known as the Heckscher Spur) is an 8.24 mi parkway on Long Island, New York, in the United States. At Islip Terrace, the Heckscher Parkway turns southward, crossing NY 27 before ending at the toll barrier for Heckscher State Park in Great River.\n\n[Great River, New York]\nGreat River, New York is a suburban hamlet and CDP in the Town of Islip, Suffolk, USA situated approximately 50 mi (55 mi driving) east of NYC on South Shore of L.I., adjoining the Great South Bay, protected from the Atlantic Ocean by Fire Island.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q51524be4fd",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "every time i send my mom pictures of me and one of my friends doing fun things the first question she asks is if we're on a date what are you trying to tell me mother",
   "my mom thinks i'm dating every one of my friends whenever i send her pictures because she thinks i'm lonely."
  ]
 },
 {
  "qid": "q5a2644a2ca",
  "kind": "yes/no",
  "text": "Claim: Chess is more popular around the world than the most popular game designed by Leo Colovini.\n\nPassages:\n\n[Chess]\nChess is a two-player strategy board game played on a chessboard, a checkered gameboard with 64 squares arranged in an 8×8 grid. The game is played by millions of people worldwide.\n\n[Leo Colovini]\nHis most popular game is \"Cartagena\".\n\n[Cartagena (board game)]\nCartagena is a critically acclaimed German-style board game released in 2000, that takes as its theme the legendary 1672 pirate-led jailbreak from the dreaded fortress of Cartagena.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qbd492e1548",
  "kind": "yes/no",
  "text": "Claim: Ogier the Dane is the name for the character also known as Holger Danske, from medieval French chansons de geste.\n\nPassages:\n\n[Holger Danske (disambiguation)]\nHolger Danske, or Ogier the Dane, is a legendary character appearing in medieval chansons de geste.\n\n[Ogier the Dane]\nOgier the Dane (French: \"Ogier le Danois\" or archaically \"Ogier de Danemarche\", Danish: \"Holger Danske\") is a legendary character who first appears in an Old French \"chanson de geste\", in the cycle of poems \"Geste de Doon de Mayence\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q2b92156081",
  "kind": "yes/no",
  "text": "Post: I am Lindt EXCELLENCE! Take the Taste Challenge quiz &amp; find out which Lindt Chocolate you are. https://t.co/UC4L1qnw5U",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qba1bbdd8a3",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "We should all be worried about Biden's tax plan",
   "the only ppl who should be worried about Biden’s tax plan r the ones who get gifts for easter"
  ]
 },
 {
  "qid": "qd1d4afc686",
  "kind": "yes/no",
  "text": "Claim: Jay Park left the South Korean music group that the star of the film Cold Eyes is a part of. He did it before the release of the group's DVD called \"Take Off\".\n\nPassages:\n\n[Cold Eyes]\n\"Stakeout\" or \"Surveillance\") is a 2013 South Korean film starring Sol Kyung-gu, Jung Woo-sung, Han Hyo-joo, Jin Kyung and Lee Junho.\n\n[Ultra Lover]\nThe single was released along with the group's second live DVD \"1st Japan Tour 2011 \"Take Off\" in Makuhari Messe\".\n\n[Go Crazy (album)]\nis the fourth Korean studio album (seventh overall) by South Korean boy band 2PM.\n\n[2PM]\nFormer leader Jay Park officially left the group in early 2010.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q951ba3c9f2",
  "kind": "yes/no",
  "text": "Text: I swear this triller event is run by teenagers",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q823ad7a0f4",
  "kind": "yes/no",
  "text": "Claim: Camelots du Roi was a branch organization of the far-right organization and journal called Action Franchise.\n\nPassages:\n\n[Action Française]\nAction française (] , AF; English: French Action ) is a French far right political movement. The name was also given to a journal associated with the movement.\n\n[Camelots du Roi]\nThe King's Camelots, officially the National Federation of the King's Camelots (French: \"Fédération nationale des Camelots du Roi\" ) was a far-right youth organization of the French militant royalist and integralist movement Action Française active from 1908 to 1936.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q10820d2f51",
  "kind": "yes/no",
  "text": "Claim: Garth Jennings directed and wrote the 2016 film featuring the voice of the host of We're Dancin'.\n\nPassages:\n\n[We're Dancin']\nTownsend Coleman was the show's host.\n\n[Townsend Coleman]\n\", \"My Life As A Teenage Robot\" and \"The Replacements\" and he also did the voice of Knotty in \"\" (1992) and he also did additional voices in films \"Fantasia 2000\" (1999) and \"Sing\" (2016)\n\n[Sing (2016 American film)]\nIt was directed and written by Garth Jennings, co-directed by Christophe Lourdelet, and starring the voices of Matthew McConaughey, Reese Witherspoon, Seth MacFarlane, Scarlett Johansson, John C. Reilly, Taron Egerton, and Tori Kelly.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q26f0bb793a",
  "kind": "yes/no",
  "text": "Claim: Wayman Tisdale, a basketball player elected to the National Collegiate Basketball Hall of Fame released music through Rendezvous Music.\n\nPassages:\n\n[Rendezvous Music]\nRendezvous Music (formerly known as Rendezvous Entertainment) is a record label founded by multiple-Grammy Award nominee and RIAA Certified Gold recording artist Dave Koz, radio entrepreneur Frank Cody and music business veteran Hyman Katz in 2002. Since its acquisition in August 2008, Rendezvous is part of the Mack Avenue Records label group and continues to release new music by Kirk Whalum, Jonathan Butler, Kyle Eastwood as well as previously unreleased music by Wayman Tisdale.\n\n[Wayman Tisdale]\nWayman Lawrence Tisdale (June 9, 1964 – May 15, 2009) was an American professional basketball player in the NBA and a smooth jazz bass guitarist. A three-time All American at the University of Oklahoma, he was elected to the National Collegiate Basketball Hall of Fame in 2009.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qab315a7866",
  "kind": "yes/no",
  "text": "Claim: The Scottish punk band that worked with Young American Recordings and Sleeper, are both from Britain.\n\nPassages:\n\n[Sleeper (band)]\nSleeper are an English Britpop band, fronted by Louise Wener and formed in London. The group had eight UK Top 40 hit singles and three UK Top 10 albums during the 1990s Their music was also featured in the soundtrack of the pop cultural hit movie \"Trainspotting\".\n\n[Young American Recordings]\nFounded by Rocco Giordano of Kinetic Records and Josh Swade of Maverick Records, it was an independent label that included groups such as British rock band South and worked with other popular groups such as Scottish punk band APB.\n\n[APB (band)]\nAPB was a Scottish post-punk band, formed in 1979, that blended funk rock, punk rock and new wave music. The group had only modest success during its brief run, yet their influence can be heard in the sound of such current bands as Franz Ferdinand, The Rapture, and Red Hot Chili Peppers.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q88f2abc224",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Telling someone when they’re wrong and being ignorant doesnt make me a cyber bully.",
   "maybe i am a cyber bully"
  ]
 },
 {
  "qid": "q0915e0296e",
  "kind": "yes/no",
  "text": "Claim: Chantal Claret is a jazz singer. So is the writer of the song \"I'm Just a Kid\".\n\nPassages:\n\n[Chantal Claret]\nShe is best known as the lead singer for the rock and power pop band Morningwood.\n\n[Pierre Bouvier]\nPierre Charles Bouvier {'1': \", '2': \", '3': \", '4': \"} (born 9 May 1979) is a Canadian singer, songwriter, musician, composer and actor who is best known as the lead singer and guitarist of the rock band Simple Plan.\n\n[I'm Just a Kid]\n\"I'm Just a Kid\" is the debut single by the band Simple Plan, written by Pierre Bouvier.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 }
]
