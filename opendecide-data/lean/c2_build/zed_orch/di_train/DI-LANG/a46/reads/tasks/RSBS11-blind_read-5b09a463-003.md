# A46 replay label-noise blind read RSBS11-blind_read-5b09a463-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS11-blind_read-5b09a463-003.json

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
  "qid": "qae5b78a98d",
  "kind": "yes/no",
  "text": "Claim: Eryngium and Arnebia are in the same kingdom of life forms.\n\nPassages:\n\n[Arnebia]\nArnebia is a genus of flowering plants in the family Boraginaceae.\n\n[Eryngium]\nEryngium is a genus of flowering plants in the family Apiaceae.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qdd9d4ac74c",
  "kind": "yes/no",
  "text": "Claim: The name of the painting stolen on March 19, 1990 for which a museum initially offered a $5 million reward for information leading towards its recovery is Landscape with Obelisk and is a painting by Dutch artist Govert Flinck.\n\nPassages:\n\n[Landscape with Obelisk]\nLandscape with Obelisk is painting by Dutch artist Govert Flinck, painted in 1638. The painting hung in the Isabella Stewart Gardner Museum of Boston, Massachusetts, United States, prior to being stolen in 1990.\n\n[Isabella Stewart Gardner Museum theft]\nIn the early hours of March 18, 1990, guards at the Isabella Stewart Gardner Museum in Boston admitted two men posing as police officers responding to a disturbance call. The museum initially offered a reward of $5 million for information leading to their recovery, but in 2017 this was doubled temporarily to $10 million with an expiration date set to the end of the year.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qcd8b42c2e0",
  "kind": "yes/no",
  "text": "Claim: Franklin \"Pete\" Adreon is still alive today, not the actor who starred alongside Shareeka Epps in the 2006 film Goosebumps.\n\nPassages:\n\n[Shareeka Epps]\nShe starred in the 2006 film \"Half Nelson\", alongside Ryan Gosling and Anthony Mackie.\n\n[Franklin Adreon]\nFranklin \"Pete\" Adreon (November 18, 1902 – September 10, 1979) was an American film and television director, producer, screenwriter, and actor.\n\n[Ryan Gosling]\nRyan Thomas Gosling (born November 12, 1980) is a Canadian actor and musician.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1787c662d7",
  "kind": "yes/no",
  "text": "Claim: The Iron Gate breaks up the 4000m high mountains between Samarkand and a province which is 20 kilometers northwest of provincial capital, Mazar-e Sharif.\n\nPassages:\n\n[Balkh]\nBalkh ( ; Persian/Pashto: بلخ‎ \"Balkh\"; Bactrian: βαχλο, \"ẞaxlɔ\") is a town in the Balkh Province of Afghanistan, about 20 kilometers northwest of the provincial capital, Mazar-e Sharif, and some 74 km south of the Amu Darya river.\n\n[Iron Gate (Central Asia)]\nIt breaks up the mountains which extend from the Hisar range south towards the Amu Darya.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qee89ae3d71",
  "kind": "yes/no",
  "text": "Claim: Marathoner Jo Ann Terry won the 80m hurdles event at the Pan American Games, a Sao Paulo-based event from 1963.\n\nPassages:\n\n[1963 Pan American Games]\nThe 4th Pan American Games were held from April 20 to May 5, 1963, in São Paulo, Brazil.\n\n[Jo Ann Terry]\nAffiliated with the Tennessee State University she won the 80 m hurdles event at the 1963 Pan American Games.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q6473d4f7ab",
  "kind": "yes/no",
  "text": "Claim: Vincent Cirelli is a special effects supervisor for the 2012 sci-fi film, Prometheus, directed by Ridley Scott.\n\nPassages:\n\n[Vincent Cirelli]\nKnown for his works at Luma Pictures as a visual effects supervisor in acclaimed films such as \"\" (2007), \"No Country for Old Men\" (2007), \"The Midnight Meat Train\" (2008), \"\" (2008), \"Harry Potter and the Half-Blood Prince\" (2009), \"The Book of Eli\" (2010), \"\" (2011), \"\" (2012), \"Prometheus\" (2012), \"The Avengers\" (2012), \"Saving Mr. Banks\" (2013), \"Guardians of the Galaxy\" (2014), \"\" (2015), \"In the Heart of the Sea\" (2015), \"Deadpool\" (2015) and \"Doctor Strange\" (2016), for which he received an Academy Award for Best Visual Effects nomination at the 89th Academy Awards.\n\n[Prometheus (2012 film)]\nPrometheus ( ) is a 2012 science fiction film directed by Ridley Scott, written by Jon Spaihts and Damon Lindelof and starring Noomi Rapace, Michael Fassbender, Guy Pearce, Idris Elba, Logan Marshall-Green and Charlize Theron.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qbd7fb6dcaf",
  "kind": "yes/no",
  "text": "Claim: The bay in the body of water that is east of the Republic of Ireland is where SS Ellan Vannin (1883) was lost in a storm. It is also where Wales's first offshore wind farm is located west of london\n\nPassages:\n\n[Republic of Ireland]\nIt is otherwise surrounded by the Atlantic Ocean, with the Celtic Sea to the south, Saint George's Channel to the south-east, and the Irish Sea to the east.\n\n[Liverpool Bay]\nLiverpool Bay is a bay of the Irish Sea between northeast Wales, Cheshire, Lancashire and Merseyside to the east of the Irish Sea.\n\n[North Hoyle Offshore Wind Farm]\nNorth Hoyle Offshore Wind Farm is Wales' first offshore wind farm, and the UK's first major offshore renewable power project.\n\n[SS Ellan Vannin (1883)]\nAs \"Ellan Vannin\" she served for a further 26 years before being lost in a storm on 3 December 1909 in Liverpool Bay.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe9ddd525d0",
  "kind": "yes/no",
  "text": "Claim: Dancer Gregory Hines, who died on August 9, 2003, appeared in White Nights.\n\nPassages:\n\n[White Nights (1985 film)]\nWhite Nights is a 1985 American drama film directed by Taylor Hackford and choreographed by Twyla Tharp and stars Mikhail Baryshnikov, Gregory Hines, Jerzy Skolimowski, Helen Mirren and Isabella Rossellini.\n\n[Gregory Hines]\nGregory Oliver Hines (February 14, 1946 – August 9, 2003) was an American dancer, actor, singer, and choreographer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7ce83e7d3f",
  "kind": "yes/no",
  "text": "Claim: Former municipality Pizy merged with Aubonne in Switzerland.\n\nPassages:\n\n[Pizy]\nOn July 1, 2011 it was merged into Aubonne.\n\n[Aubonne]\nAubonne is a municipality in the district of Morges in the canton of Vaud in Switzerland.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qbd162f5fc8",
  "kind": "yes/no",
  "text": "Text: Happy New Year!",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q64909f210d",
  "kind": "yes/no",
  "text": "Claim: This species and the relative of the Fir are classified as genus in the naming system. Parnassius nordmanni is a high altitude butterfly which is found the Caucasus. The larva feeds on this species including \"C. alpestris\", \"C. conorhiza\" and \"C. emanueli\".\n\nPassages:\n\n[Parnassius nordmanni]\nThe larva feeds on \"Corydalis\" species including \"C. alpestris\", \"C. conorhiza\" and \"C. emanueli\".\n\n[Corydalis]\nCorydalis (Greek \"korydalís\" \"crested lark\") is a genus of about 470 species of annual and perennial herbaceous plants in the Papaveraceae family, native to the temperate Northern Hemisphere and the high mountains of tropical eastern Africa.\n\n[Cedrus]\nCedrus (common English name cedar) is a genus of coniferous trees in the plant family Pinaceae.\n\n[Fir]\nFirs are most closely related to the genus \"Cedrus\" (cedar).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3c509316db",
  "kind": "yes/no",
  "text": "Claim: Chasty Ballesteros directed the film which had the man, who starred in Bone Dry alongside Lance Henriksen, play the role of Jared Nomak.\n\nPassages:\n\n[Blade II]\nIt was written by David S. Goyer, who also wrote the previous film, directed by Guillermo del Toro, and had Wesley Snipes returning as the lead character and producer.\n\n[Bone Dry]\nThe film starred Luke Goss and Lance Henriksen.\n\n[Luke Goss]\nHe has appeared in numerous films including \"Blade II\" (2002) as Jared Nomak, \"One Night with the King\" (2006) as King Xerxes, \"\" (2008) as Prince Nuada, \"Tekken\" (2010) as Steve Fox and \"Interview with a Hitman\" (2012) as Viktor.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qcef232d9a9",
  "kind": "yes/no",
  "text": "Claim: Arthur Hiller was born before the writer and director of underground 1999's no budget film I Was a Teenage Serial Killer.\n\nPassages:\n\n[Arthur Hiller]\nArthur Hiller, OC (November 22, 1923 – August 17, 2016) was a Canadian-American television and film director, having directed over 33 films during his 50-year career.\n\n[Sarah Jacobson]\nSarah Jacobson (August 25, 1971, Norwalk, Connecticut – February 13, 2004 New York City) was an independent filmmaker who wrote, produced, and filmed her own movies.\n\n[I Was a Teenage Serial Killer]\nI Was a Teenage Serial Killer is an underground no budget film written and directed by \"The Queen of Underground Film\", Sarah Jacobson.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q13c0f414d7",
  "kind": "yes/no",
  "text": "Tweet: Oh no here comes the sushi craving 😫",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qe97a373947",
  "kind": "yes/no",
  "text": "Claim: This actor starred in the film The Magnificent Seven Ride. The director who gave him a role in \"For a Few Dollars More\" was Italian not Jon Paul Puno.\n\nPassages:\n\n[Lee Van Cleef]\nAfter suffering serious injuries in a car crash, Van Cleef began to lose interest in his apparently waning career by the time Sergio Leone gave him a major role in \"For a Few Dollars More\".\n\n[The Magnificent Seven Ride]\nIt stars Lee Van Cleef as Chris Adams, succeeding Yul Brynner and George Kennedy in the role.\n\n[Sergio Leone]\nSergio Leone (] ; 3 January 1929 – 30 April 1989) was an Italian film director, producer and screenwriter, credited as the inventor of the \"Spaghetti Western\" genre.\n\n[Jon Paul Puno]\nJon Paul Puno (born 1985) is an American filmmaker and classical crossover singer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q4f79b7e5f2",
  "kind": "yes/no",
  "text": "Claim: The hit song released before Love Shy (Thinking About You) is of the genre UK Garage due to its 4x4 rhythm.\n\nPassages:\n\n[What's It Gonna Be (H &quot;Two&quot; O song)]\nis a bassline (subgenre of UK garage) song performed by the duo known as H \"Two\" O (Selim Ben Rabha, \"Solution\", and Simon McDevitt, \"Oz\", who also go by \"Hit 'Em\" and \"Hard\") and the British three-person bassline vocal group Platnum (Aaron Evers, Mina Poli, and Michelle McKenna).\n\n[Love Shy (Thinking About You)]\nIt was released after the success of \"What's It Gonna Be\" with H \"Two\" O.\n\n[Bassline (music genre)]\nBassline (sometimes referred to as bassline house, Niche or 4x4) is a type of music related to UK garage that originated in Sheffield in the early 2000s.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8dff2a9e93",
  "kind": "yes/no",
  "text": "Claim: Jack Kirby was the first illustrator for a comic book character later assigned to Carlo Pagulayan.\n\nPassages:\n\n[Hulk (comics)]\nThe Hulk is a fictional superhero appearing in American comic books published by Marvel Comics. Created by writer Stan Lee and artist Jack Kirby, the character first appeared in the debut issue of \"The Incredible Hulk\" (May 1962).\n\n[Carlo Pagulayan]\nCarlo Pagulayan (born June 24, 1978) is a freelance Filipino comic book artist. He has since had assignments from a few publishers, including \"Elektra\" and \"The Incredible Hulk\" for Marvel Comics.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qb754b9d1dc",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "How does one find motivation to do basically anything? Asking for a friend.",
   "\"How does somebody find motivation to do basically anything? I haven't had motivation in ages.\""
  ]
 },
 {
  "qid": "q3533dbaa62",
  "kind": "yes/no",
  "text": "Claim: Kurt Julian Weillwas a German composer, active from the 1920s in his native country, and in his later years in the United States, with Brecht, he developed productions such as his best-known work, the Threepenny Opera is a \"play with music\" by Bertolt Brecht and who, adapted from John Gay's 18th-century English ballad opera, \"The Beggar's Opera\" with Elisabeth Hauptmann.\n\nPassages:\n\n[Kurt Weill]\nWith Brecht, he developed productions such as his best-known work \"The Threepenny Opera\", which included the ballad \"Mack the Knife\".\n\n[The Threepenny Opera]\nThe Threepenny Opera (Die Dreigroschenoper ) is a \"play with music\" by Bertolt Brecht and Elisabeth Hauptmann, adapted from John Gay's 18th-century English ballad opera, \"The Beggar's Opera\", with music by Kurt Weill and insertion ballads by François Villon and Rudyard Kipling.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q08b64c33b9",
  "kind": "yes/no",
  "text": "Claim: Beech is more south than Daviesia's native growing land.\n\nPassages:\n\n[Daviesia]\nDaviesia, commonly known as Bitter-peas, is a large genus of flowering plants in the legume family. They are native to Australia, with a center of diversity in western Australia.\n\n[Beech]\nBeech (\"Fagus\") is a genus of deciduous trees in the family Fagaceae, native to temperate Europe, Asia and North America.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6e679fd7ef",
  "kind": "yes/no",
  "text": "Claim: The man who hired Sioux Falls architect Wallace L. Dow to build a home in Sioux Falls, Minnesota founded the company Dayton's department store.\n\nPassages:\n\n[George Dayton]\nGeorge Draper Dayton (March 6, 1857 – February 18, 1938) was an American businessman and philanthropist, most famous for being the founder of Dayton's department store, which later became Target Corporation.\n\n[George D. Dayton House]\nThe George Draper Dayton House was built in 1890 in Worthington, Minnesota, United States. George Dayton hired the Sioux Falls architect Wallace L. Dow to design his grand home on a parcel that took up eight lots.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qfa3b53ce53",
  "kind": "yes/no",
  "text": "Claim: The company Crown Holdings Incorporated claims to manufacture one out of every three objects that provide a shelf life typically ranging from one to five years.\n\nPassages:\n\n[Canning]\nCanning provides a shelf life typically ranging from one to five years, although under specific circumstances it can be much longer.\n\n[Crown Holdings]\nCrown Holdings Incorporated, formerly Crown Cork & Seal Company, is an American company that makes metal beverage and food cans, metal aerosol containers, metal closures and specialty packing. It claims to manufacture one out of every five beverage cans used in the world, and one out of every three food cans used in North America and Europe.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1ec0bb853e",
  "kind": "yes/no",
  "text": "Claim: In the 1948 Los Angeles Rams season the champion team debuted the first helmet logo in league history, an idea that was conceived by running back, who is the great-grandfather to the 23rd overall pick in the 2010 Major League Baseball Draft\n\nPassages:\n\n[Christian Yelich]\nYelich was drafted out of high school by the Marlins in the 1st round (23rd overall) of the 2010 Major League Baseball Draft.\n\n[1948 Los Angeles Rams season]\nThe Rams debuted the first helmet logo in league history in 1948, an idea that was conceived by running back Fred Gehrke.\n\n[Fred Gehrke]\nHe is the great-grandfather of Miami Marlin Christian Yelich",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9bf6f63280",
  "kind": "yes/no",
  "text": "Text: I'm just living off salads and yogurt and loving it tbh",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qbb10f955f6",
  "kind": "yes/no",
  "text": "Claim: James David Barber taught political science from 1977 to 1995 at a university. It was founded before the university Donald Sur taught at after he settled in Boston, Massachusetts.\n\nPassages:\n\n[Duke University]\nDuke University is a private research university located in Durham, North Carolina. Founded by Methodists and Quakers in the present-day town of Trinity in 1838, the school moved to Durham in 1892.\n\n[Tufts University]\nTufts College was founded in 1852 by Christian Universalists who worked for years to open a nonsectarian institution of higher learning.\n\n[Donald Sur]\nAfter receiving his doctorate from Harvard in 1972, he settled in Boston, Massachusetts, where many of his works were premiered and where he taught at several local universities, including Harvard, MIT, and Tufts.\n\n[James David Barber]\nFrom 1977 to 1995, he taught political science at Duke University.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qfad2c685b2",
  "kind": "yes/no",
  "text": "Claim: Gatwick Airport in south-east England ranks as the 8th busiest airport in Central London and replaced the airport where the 1921 SNETA Farman Goliath ditching first took off.\n\nPassages:\n\n[Gatwick Airport]\nGatwick Airport (also known as London Gatwick) (IATA: LGW, ICAO: EGKK) is a major international airport in south-east England, 29.5 mi south of Central London and 2.7 NM north of Crawley. Gatwick is the eighth-busiest airport in Europe.\n\n[1921 SNETA Farman Goliath ditching]\nThe aircraft was operating a mail flight from Croydon Airport, United Kingdom to Brussels-Evere Airport, Belgium.\n\n[Croydon Airport]\nCroydon Airport (ICAO: EGCR ) was an airport in South London, England. It was the main airport for London before it was replaced by Northolt Aerodrome, London Heathrow Airport and Gatwick Airport.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa48f983ca9",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I will not be granting an extension to the student who emailed me and my co-teacher and got both of our names wrong.",
   "V excited to grant an extension to students who email me and my co-teacher and get both of our names wrong"
  ]
 },
 {
  "qid": "qab06d8c394",
  "kind": "yes/no",
  "text": "Claim: Kenneth \"Ken\" Leung is the actor that portrays a marvel character in a Eme Ikwuakor television series that was created by Scott Buck.\n\nPassages:\n\n[Ken Leung]\nKenneth \"Ken\" Leung (born January 21, 1970) is an American actor who is best known for playing Miles Straume in \"Lost\", Admiral Statura in \"\", Detective Stephen Sing in \"Saw\", and Kid Omega in \"\". He portrays the Marvel Comics character Karnak, a member of the Inhumans, on the ABC television series \"Inhumans\", which premiered in September 2017.\n\n[Inhumans (TV series)]\nMarvel's Inhumans, or simply Inhumans, is an American television series created for ABC by Scott Buck, based on the Marvel Comics race of the same name.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3933a1a752",
  "kind": "yes/no",
  "text": "Post: The @Pontifex talks benefits of universal basic income #COVID19  #coronavirus #catholic #EasterSunday https://t.co/2e2BCmroVk",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qe9060e4fc9",
  "kind": "yes/no",
  "text": "Claim: The deposition of the father of Charles Lennox Duke of Richmond was in 1651 in London, England.\n\nPassages:\n\n[Charles II of England]\nCharles II (29 May 1630 – 6 February 1685) was king of England, Scotland and Ireland. He was king of Scotland from 1649 until his deposition in 1651, and king of England, Scotland and Ireland from the restoration of the monarchy in 1660 until his death.\n\n[Duke of Richmond and Lennox]\nIn 1675, King Charles II created his illegitimate son Charles Lennox Duke of Richmond (created on 9 August 1675) and Duke of Lennox (created on 9 September 1675), and the two Dukedoms have since been held concurrently by Lennox's descendants.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8d4fbef2da",
  "kind": "yes/no",
  "text": "Claim: A naval leader in Germany before and during World War II attained the highest possible naval rank since Alfred von Tirpitz was later replaced by the man who briefly succeeded Adolf Hitler as the head of government of Germany.\n\nPassages:\n\n[Karl Dönitz]\nDönitz briefly succeeded Adolf Hitler as the head of state of Germany.\n\n[Erich Raeder resignation and later]\nRaeder attained the highest possible naval rank—that of \"Großadmiral\" (Grand Admiral) — in 1939, becoming the first person to hold that rank since Alfred von Tirpitz.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q462a47c46b",
  "kind": "yes/no",
  "text": "Claim: The coach of the Karachi Kings finished his time as coach of the Australia national cricket team on 23 June 2013.\n\nPassages:\n\n[Mickey Arthur]\nHe coached the South African national team from 2005 to 2010, and was the coach of the Australia national cricket team until his sacking on 23 June 2013.\n\n[Karachi Kings]\nThe team is currently captained by Kumar Sangakkara and coached by Mickey Arthur a former South African cricketer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc9cdae6b3b",
  "kind": "yes/no",
  "text": "Claim: The player that is featured on the cover of the Spanish version of this video game is 6 ft tall. This game is the predecessor to another game. The series the other game is in is published by Take-Two Interactive.\n\nPassages:\n\n[NBA 2K16]\nAdditionally, the French version of \"NBA 2K16\" features Tony Parker of the San Antonio Spurs as the cover athlete, the German version, Dennis Schröder of the Atlanta Hawks, and the Spanish version, Marc and Pau Gasol of the Memphis Grizzlies and Chicago Bulls respectively.\n\n[Take-Two Interactive]\nAs owner of 2K Games, Take-Two publishes its 2K Sports titles, and creates free-to-play mobile titles through Social Point.\n\n[Dennis Schröder]\nStanding at 6 ft , he plays at the point guard position.\n\n[NBA 2K17]\nIt is the 18th installment in the \"NBA 2K\" franchise and the successor to \"NBA 2K16\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe93c61f3da",
  "kind": "yes/no",
  "text": "Claim: No, the lyricist of The Lion King and Kathy Acker are both from America.\n\nPassages:\n\n[The Lion King]\nIts original songs were written by composer Elton John and lyricist Tim Rice, and original scores were written by Hans Zimmer.\n\n[Tim Rice]\nSir Timothy Miles Bindon \"Tim\" Rice (born 10 November 1944) is an English author and Academy Award, Golden Globe Award, Tony Award, and Grammy Award-winning lyricist.\n\n[Kathy Acker]\nKathy Acker (née Lehmann; April 18, 1944 – November 30, 1997) was an American experimental novelist, punk poet, playwright, essayist, postmodernist and sex-positive feminist writer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5a1accdf81",
  "kind": "yes/no",
  "text": "Claim: The director of Looking on the Bright Side and Basil the director of Godfather Part II were both alive at some point in time. Looking on the Bright side was a 1932 British musical comedy film.\n\nPassages:\n\n[Basil Dean]\nBasil Herbert Dean CBE (27 September 1888 – 22 April 1978) was an English actor, writer, film producer/film director and theatrical producer/director.\n\n[Looking on the Bright Side]\nLooking on The Bright Side is a 1932 British musical comedy film It was directed by Graham Cutts and Basil Dean and starring Gracie Fields, Richard Dolman, and Betty Shale.\n\n[The Godfather Part II]\nThe Godfather Part II is a 1974 American crime film produced and directed by Francis Ford Coppola from a screenplay co-written with Mario Puzo, starring Al Pacino and Robert De Niro.\n\n[Francis Ford Coppola]\nFrancis Ford Coppola ( ; born April 7, 1939), also credited as Francis Coppola, is a semi-retired American film director, producer, screenwriter and film composer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2dc3720fd4",
  "kind": "yes/no",
  "text": "Claim: Andrew Bird released his second live album with a band from Louisville, Kentucky.\n\nPassages:\n\n[My Morning Jacket]\nMy Morning Jacket is an American rock band formed in Louisville, Kentucky in 1998.\n\n[Fingerlings 2]\nFingerlings 2 is the second album in a series of live releases by Andrew Bird. Self-released in 2004, it features appearances by My Morning Jacket and Nora O'Connor as well as five live renditions of tracks featured on Bird's 2005 release \"The Mysterious Production of Eggs\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf693907f2e",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which text is sarcastic?",
  "options": [
   "STOP TREATING MARS LIKE A BACK-UP BOYFRIEND JUST FIX YOUR CURRENT RELATIONSHIP WITH EARTH BECAUSE YOU CAN'T LIVE HERE.",
   "'Focus on fixing Earth before you start experimenting with Mars'"
  ]
 },
 {
  "qid": "qb97015865b",
  "kind": "yes/no",
  "text": "Tweet: I'm hoping my social work class party is going to involve tequila and chip and salsa 💃🍹🎉👨",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q70c127acd0",
  "kind": "yes/no",
  "text": "Claim: An actor acted in this 1985 play. It is by an American playwright who died in June 2005. The actor portrayed Russell Taylor in The Closer.\n\nPassages:\n\n[Fences (play)]\nFences is a 1985 play by American playwright August Wilson.\n\n[August Wilson]\nAugust Wilson (April 27, 1945 – October 2, 2005) was an American playwright whose work included a series of ten plays, \"The Pittsburgh Cycle\", for which he received two Pulitzer Prizes for Drama.\n\n[Russell Taylor (The Closer)]\nAssistant Chief Russell Taylor was a fictional character featured in TNT's \"The Closer\", portrayed by Robert Gossett.\n\n[Robert Gossett]\nHe went on to act in the Broadway production of Lloyd Richard's \"Fences\", Hal Scott's \"A Raisin in the Sun\" and Donald McKayle's \"The Last Minstrel Show\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe855221479",
  "kind": "yes/no",
  "text": "Claim: Rupert Julian was born before Robert Z. Leonard.\n\nPassages:\n\n[Robert Z. Leonard]\nRobert Zigler Leonard (October 7, 1889 – August 27, 1968) was an American film director, actor, producer, and screenwriter.\n\n[Rupert Julian]\nRupert Julian (25 January 1879 – 27 December 1943) was the first New Zealand cinema actor, director, writer and producer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qbf9b92cc2f",
  "kind": "yes/no",
  "text": "Claim: Eugene Dynkin and Vladimir Voevodsky were both mathematicians from Russia.\n\nPassages:\n\n[Eugene Dynkin]\nEugene Borisovich Dynkin (Russian: Евге́ний Бори́сович Ды́нкин ; 11 May 1924 – 14 November 2014) was a Soviet and American mathematician.\n\n[Vladimir Voevodsky]\nVladimir Alexandrovich Voevodsky ( ; Russian: Влади́мир Алекса́ндрович Воево́дский , 4 June 1966 - 30 September 2017) was a Russian mathematician.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qdaf08504fd",
  "kind": "yes/no",
  "text": "Tweet: who thinks me and sam should start a band called 'teeth at midnight' 🦷🌙",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q4d07b6d0eb",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "Kepa had a great game",
   "Kepa was sh*t"
  ]
 },
 {
  "qid": "q68443d40bc",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "‘It’s only a game’ 🥴🥴",
   "Look how important these clubs are to their fans!"
  ]
 },
 {
  "qid": "qf5773b0c99",
  "kind": "yes/no",
  "text": "Claim: Ginés González García served under the President of Argentina in 2009 who was also Governor of Santa Cruz from 2003 to 2007.\n\nPassages:\n\n[Néstor Kirchner]\nNéstor Carlos Kirchner (] ; 25 February 195027 October 2010) was an Argentine politician who served as President of Argentina from 2003 to 2007 and as Governor of Santa Cruz from 1991 to 2003.\n\n[Ginés González García]\nGinés González García (born 1945) is a medical doctor and was the Minister of Health and Environment of Argentina during the administrations of Presidents Eduardo Duhalde and Néstor Kirchner.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q47aac78733",
  "kind": "yes/no",
  "text": "Claim: The murderer, by whom the character Keyser Soze was inspired, committed his murders in Westfield, New Jersey between 1972 and 1981.\n\nPassages:\n\n[Keyser Söze]\nThe character was inspired by real life murderer John List and the spy thriller \"No Way Out\", which featured a shadowy KGB mole.\n\n[John List]\nOn November 9, 1971, he killed his wife, mother, and three children in their home in Westfield, New Jersey, then disappeared.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6ebcb6244b",
  "kind": "yes/no",
  "text": "Claim: Peggy Trentini made her acting debut in the 1982 film. \"Leni\" Riefenstahl was born before the director of the film.\n\nPassages:\n\n[Garry Marshall]\nGarry Kent Marshall (November 13, 1934 – July 19, 2016) was an American actor, director, producer, writer, and voice artist best known for creating \"Happy Days\" and its various spin-offs, developing Neil Simon's 1965 play \"The Odd Couple\" for television, and directing \"Pretty Woman\", \"Runaway Bride\", \"Valentine's Day\", \"New Year's Eve\", \"Mother's Day\", \"\"The Princess Diaries\", and \"\".\n\n[Young Doctors in Love]\nYoung Doctors in Love is a 1982 American comedy film directed by Garry Marshall.\n\n[Leni Riefenstahl]\nHelene Bertha Amalie \"Leni\" Riefenstahl (] ; 22 August 1902 – 8 September 2003) was a German film director, producer, screenwriter, editor, photographer, actress and dancer.\n\n[Peggy Trentini]\nTrentini made her film debut in 1982 with a small part in the comedy movie \"Young Doctors in Love\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q100b84e7ce",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "@xNemoooo @McDonaldsUK @tasshx Say swear you didn’t down all bev’s at Acapulco’s straight after?? 😘",
   "Didn't you have all the beverages at Acapulco's last night?"
  ]
 },
 {
  "qid": "q760b495cdc",
  "kind": "yes/no",
  "text": "Claim: The Battle of Reading, which Æthelwulf of Berkshire lost his life was a battle on 4 January 871 at Reading in what is now the English county of Berkshire.\n\nPassages:\n\n[Battle of Reading (871)]\nThe first Battle of Reading was a battle on 4 January 871 at Reading in what is now the English county of Berkshire.\n\n[Æthelwulf of Berkshire]\nHe received a land grant in 843/44 from Brihtwulf, king of Mercia; and lost his life at the Battle of Reading.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q480a52b994",
  "kind": "yes/no",
  "text": "Claim: Fash Mosque is near the mosque where Muhammad Ayyub was Imam, which was originally built by Muhammad.\n\nPassages:\n\n[Fas'h mosque]\nIt is 4.5 km from Al-Masjid an-Nabawi.\n\n[Muhammad Ayyub]\nHe was an Imam of Al-Masjid an-Nabawi in Medina, Saudi Arabia.\n\n[Al-Masjid an-Nabawi]\nAl-Masjid an-Nabawī (Arabic: ٱلْمَسْجِدُ ٱلنَّبَويّ‎ , 'Prophet's Mosque' ‎ ) is a mosque established and originally built by the Islamic prophet Muhammad, situated in the city of Medina in Saudi Arabia.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 }
]
