# A46 replay label-noise blind read RSBS07-blind_read-cc7738f7-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS07-blind_read-cc7738f7-000.json

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
  "qid": "q476f291c87",
  "kind": "yes/no",
  "text": "Claim: The metafamily of graphical operating systems developed, marketed, and sold by Microsoft offers software for singing training.\n\nPassages:\n\n[Microsoft Windows]\nMicrosoft Windows, or simply Windows, is a metafamily of graphical operating systems developed, marketed, and sold by Microsoft.\n\n[Winsingad]\nWinSingad is a Microsoft Windows based software for singing training.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc57ecdc396",
  "kind": "yes/no",
  "text": "Claim: The pageant was held at a venue inside a casino in Las Vegas. This venue is located in a casino that is owned and operated by the Caesars Entertainment Corporation. Miss Dominican Republic 2015 represented the Dominican Republic in the pagaent.\n\nPassages:\n\n[The AXIS]\nThe AXIS (known as The AXIS powered by Monster for sponsorship purposes, also referred to as the AXIS Theater) is a mid-sized auditorium located at Planet Hollywood Las Vegas on the Las Vegas Strip.\n\n[Miss Universe 2015]\nMiss Universe 2015, the 64th Miss Universe pageant, was held on 20 December 2015 at The AXIS in Las Vegas, Nevada, United States.\n\n[Planet Hollywood Las Vegas]\nIt is owned and operated by Caesars Entertainment Corporation.\n\n[Miss Dominican Republic 2015]\nThe winner represented the Dominican Republic in Miss Universe 2015.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q880b1f3471",
  "kind": "yes/no",
  "text": "Claim: The residence at 200 West Street is taller than the one at the location of Pershing Square Capital Management.\n\nPassages:\n\n[888 7th Avenue]\n888 7th Avenue is a 628 ft (191m) tall modern-style office skyscraper in Midtown Manhattan which was completed in 1969 and has 46 floors.\n\n[200 West Street]\n200 West Street is the global headquarters of the Goldman Sachs investment banking firm. The building is a 749 ft , 44-story building located on West Street, between Vesey and Murray Streets in Lower Manhattan.\n\n[Pershing Square Capital Management]\nPershing Square Capital Management is an American hedge fund management company founded and run by Bill Ackman, located at 888 7th Avenue in New York.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qdc862242e4",
  "kind": "yes/no",
  "text": "Claim: Legends of the Fall was based on a novella by the poetry and fiction writer James Harrison.\n\nPassages:\n\n[Legends of the Fall]\nBased on the 1979 novella of the same title by Jim Harrison, the film is about three brothers and their father living in the wilderness and plains of Montana in the early 20th century and how their lives are affected by nature, history, war and love.\n\n[Jim Harrison]\nJames Harrison (December 11, 1937 – March 26, 2016) was an American writer known for his poetry, fiction, reviews, essays about the outdoors, and writings about food.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q1262be7586",
  "kind": "yes/no",
  "text": "Claim: The singer Sonya Scarlet is younger than the singer who had left their band, when it recorded Information for an album. This album is from John Crawford (musician), an American singer-songwriter.\n\nPassages:\n\n[Sonya Scarlet]\nSonya Scarlet (born 2 April 1980) is the singer and lyricist of the Italian extreme gothic metal band Theatres des Vampires.\n\n[John Crawford (musician)]\nJohn Buckner Crawford (born January 17, 1960) is an American singer-songwriter whose efforts with the band Berlin were an essential part of their rise to fame in the early 1980s.\n\n[Terri Nunn]\nTerri Kathleen Nunn (born June 26, 1961), is an American singer and actress.\n\n[Information (Berlin album)]\nIt was recorded during the period when Terri Nunn had temporarily left the band to pursue an acting career and Virginia Macolino performed the lead vocals.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6ddd804b50",
  "kind": "yes/no",
  "text": "Claim: The novelty song King of the Road was originally recorded by country music artist in November 1964. This country music artist also recorded the song \"(And You Had a) Do-Wacka-Do\".\n\nPassages:\n\n[King of the Road (song)]\n\"King of the Road\" is a song written and originally recorded in November 1964 by country singer Roger Miller.\n\n[Roger Miller]\nRoger Dean Miller, Sr. (January 2, 1936 – October 25, 1992) was an American singer-songwriter, musician, and actor, best known for his honky-tonk-influenced novelty songs. His most recognized tunes included the chart-topping country and pop hits \"King of the Road\", \"Dang Me\", and \"England Swings\", all from the mid-1960s Nashville sound era.\n\n[Do-Wacka-Do]\n\"(And You Had a) Do-Wacka-Do\" is a song, released in 1965, by American country music artist Roger Miller.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q0434f1087e",
  "kind": "yes/no",
  "text": "Claim: Hobart Paving is a single by a band formed in 1990.\n\nPassages:\n\n[Saint Etienne (band)]\nSaint Etienne are an English band from London, formed in 1990.\n\n[Hobart Paving]\n\"Hobart Paving\" is a single by British pop group Saint Etienne.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qdbcb19995e",
  "kind": "yes/no",
  "text": "Claim: The military unit that The 43d Aeromedical Evacuation Squadron is part of is stationed at the largest military installation, Fort Bragg.\n\nPassages:\n\n[43d Aeromedical Evacuation Squadron]\nIt is part of the 43d Air Mobility Operations Group at Pope Army Air Field, North Carolina.\n\n[43d Air Mobility Operations Group]\nThe 43d Air Mobility Operations Group is an active duty air mobility unit at Pope Field, Fort Bragg, North Carolina (formerly Pope AFB), and is part of the Air Mobility Command (AMC) USAF Expeditionary Center.\n\n[Fort Bragg]\nFort Bragg, North Carolina, is a military installation of the United States Army and is the largest military installation in the world (by population) with more than 50,000 active duty personnel.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q114b9e73da",
  "kind": "yes/no",
  "text": "Claim: Blake LeVine collected an autograph from Brad Pitt, the American actor and producer, born 1963.\n\nPassages:\n\n[Blake LeVine]\nAs a child, he was featured on Entertainment Tonight, Maury Povich, The Jon Stewart Show, CNN, The New York Post, Premiere Magazine, The Los Angeles Times and numerous radio programs about his experiences collecting autographs from celebrities including Princess Diana, Mother Teresa, Brad Pitt, Frank Sinatra and over 1,000 notables.\n\n[Brad Pitt]\nWilliam Bradley Pitt (born December 18, 1963) is an American actor and producer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q815d84356d",
  "kind": "yes/no",
  "text": "Claim: Podocarpus is a more numerous species than Osmunda.\n\nPassages:\n\n[Podocarpus]\nPodocarpus ( ) is a genus of conifers, the most numerous and widely distributed of the podocarp family, Podocarpaceae. \"Podocarpus\" are evergreen shrubs or trees, usually from 1 to tall, known to reach 40 m at times. There are approximately 97 to 107 species in the genus depending on the circumscription of the species.\n\n[Osmunda]\nFive to ten species have been listed for this genus.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd4731cb6cc",
  "kind": "yes/no",
  "text": "Claim: Radio was the technology that used to be how the school that educator Adelaide Miethke conducted classes.\n\nPassages:\n\n[Adelaide Miethke]\nAdelaide Laetitia \"Addie\" Miethke, {'1': \", '2': \", '3': \", '4': \"} (8 June 1881 – 4 February 1962), was a South Australian educator and teacher who was pivotal in the formation of the School of the Air using the existing Royal Flying Doctor Service radio network.\n\n[School of the Air]\nSchool of the Air is a generic term for correspondence schools catering for the primary and early secondary education of children in remote and outback Australia where some or all classes were traditionally conducted by radio, although this is now being replaced by internet technology.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd930c3503f",
  "kind": "yes/no",
  "text": "Claim: Tom Hewitt died in Ravalli County, Montana.\n\nPassages:\n\n[Victor, Montana]\nVictor is a census-designated place (CDP) in Ravalli County, Montana, United States.\n\n[Tom Hewitt (actor)]\nTom Hewitt (born c. 1957) is an American actor and Broadway stage performer, and a native of Victor, Montana.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qebde65bd3e",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "rewatching degrassi for the millionth time",
   "“Watching Degrassi again “"
  ]
 },
 {
  "qid": "q726b95bd5a",
  "kind": "yes/no",
  "text": "Claim: Every Rose Has Its Thorn was the number one single by Poison, the band that features a lead singer who won the season finale of a television reality game show that premiered in 2010 on NBC.\n\nPassages:\n\n[The Apprentice (U.S. season 9)]\nThe Celebrity Apprentice 3 (also known as The Apprentice 9) is the ninth installment of the reality game show, \"Celebrity Apprentice\". On April 29, 2009, NBC officially announced the renewal of \"Celebrity Apprentice\" for Spring 2010. The show premiered on Sunday, March 14, 2010. The two-hour season finale was on Sunday, May 23, 2010, 9–11 p.m., ET/PT and the winner was Poison lead singer and \"Rock of Love\" star Bret Michaels.\n\n[Bret Michaels]\nBret Michael Sychak (born March 15, 1963), professionally known as Bret Michaels, is an American singer-songwriter and musician. The band has also charted ten singles to the Top 40 of the \"Billboard\" Hot 100, including six Top 10 singles and a number-one single, \"Every Rose Has Its Thorn\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q6852a9b8db",
  "kind": "yes/no",
  "text": "Claim: Hear It Is is the debut album of the lead singer. While both singer-songwriters have displayed incredible talent, an eclectic mix of musical styles sets Robert Palmer apart from him, causing him to gain popularity in parts of the world.\n\nPassages:\n\n[Wayne Coyne]\nHe is the lead singer, occasional backing vocalist, guitarist, keyboardist, theremin player and songwriter for the band the Flaming Lips.\n\n[Hear It Is]\nThis album marks the debut of Wayne Coyne on vocals, after the departure of his brother Mark.\n\n[Robert Palmer (singer)]\nHe was known for his distinctive, soulful voice, eclectic mix of musical styles on his albums, combining soul, jazz, rock, pop, reggae, blues, and sartorial acumen.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf2cf79478b",
  "kind": "yes/no",
  "text": "Claim: NFL quarterback, Heisman winner, and OU football player graduated from Putnam City North High School in Tennessee.\n\nPassages:\n\n[University of Oklahoma]\nThe University of Oklahoma (OU) is a coeducational public research university in Norman, Oklahoma.\n\n[Sam Bradford]\nBradford attended Putnam City North High School in Oklahoma City, where he starred in football, basketball and golf.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q64ec624ee4",
  "kind": "yes/no",
  "text": "Claim: A highway replaced by another highway has a junction at Cairo Junction. It is 1286 miles long. Streatorland is the area east of the other highway.\n\nPassages:\n\n[Streatorland]\nIt can be more broadly defined as the area east of Interstate 39, west of Interstate 55, and south of the Illinois River.\n\n[Cairo Junction, Illinois]\nCairo Junction is located at the junction of U.S. Route 51, Illinois Route 3, and Illinois Route 37 north of Cairo.\n\n[U.S. Route 51]\nU.S. Route 51 is a south-north United States highway that runs for 1286 mi from the western suburbs of New Orleans, Louisiana to within 100 ft of the Wisconsin–Michigan border.\n\n[Interstate 39]\nI-39 was designed to replace U.S. Route 51 (US 51), which in the early 1980s was one of the busiest two-lane highways in the United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q411b6ff842",
  "kind": "yes/no",
  "text": "Claim: Debbie Fields husband is associated with the hotel chain based in Atlanta, Georgia. Boardwalk Hotel and Casino was once a part of that chain.\n\nPassages:\n\n[Debbi Fields]\nDebbi Fields (born September 18, 1956) is the founder and spokesperson of Mrs. Fields Bakeries. She currently lives in Nashville, Tennessee, with her husband, former Holiday Inn and Harrah's CEO Michael Rose.\n\n[Boardwalk Hotel and Casino]\nIt was part of the Holiday Inn hotel chain until it was acquired by MGM in 2000.\n\n[Holiday Inn]\nHoliday Inn is an American brand of hotels, and a subsidiary of InterContinental Hotels Group. The hotel chain is based in Atlanta, Georgia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q40e5876234",
  "kind": "yes/no",
  "text": "Text: just wondering how to get my diss down by 1500 words .. such fun",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q15ff4d6d13",
  "kind": "yes/no",
  "text": "Claim: Alex Jesaulenko, former Ukrainian rules footballer and coach won the award The Goal of the Year in 2001.\n\nPassages:\n\n[Goal of the Year (AFL)]\nThe official award was first given in 2001.\n\n[Alex Jesaulenko]\nAlex Jesaulenko (Ukrainian: Олександр Єсауленко , transcribed \"Oleksandr Yesaulenko\", ] ) MBE (born 2 August 1945 in Salzburg, Austria) is a former Australian rules footballer and coach who represented Carlton and St Kilda in the Victorian Football League (VFL) from the 1960s to the 1980s.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd703c3b81f",
  "kind": "yes/no",
  "text": "Text: Love it when I forget to transfer my rent money over from my savings 🥴",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q497b4682bb",
  "kind": "yes/no",
  "text": "Tweet: so many cute dogs at ikea rn",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q60523a1c01",
  "kind": "yes/no",
  "text": "Claim: The cemetery that George W. Wallace is buried at, is located at a park that is part of Golden Gate National Recreation Area.\n\nPassages:\n\n[George W. Wallace]\nHe is buried at San Francisco National Cemetery.\n\n[San Francisco National Cemetery]\nSan Francisco National Cemetery is an United States national cemetery, located in the Presidio of San Francisco, California.\n\n[Presidio of San Francisco]\nThe Presidio of San Francisco (originally, El Presidio Real de San Francisco or The Royal Fortress of Saint Francis) is a park and former U.S. Army military fort on the northern tip of the San Francisco Peninsula in San Francisco, California, and is part of the Golden Gate National Recreation Area.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3ba5a8689c",
  "kind": "yes/no",
  "text": "Tweet: thanks @SovietWomble for ratting my location out on stream and then embarrassing me 😂 it made my day though https://t.co/3b7Cjql2GO",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q044d2e6b2d",
  "kind": "yes/no",
  "text": "Claim: Sarah MacLean wrote the 2014 RITA Award winning crime novel No Good Duke Goes Unpunished.\n\nPassages:\n\n[Sarah MacLean]\nShe is a two-time winner of the Romance Writers of America RITA Award for Best Historical Romance for \"A Rogue by Any Other Name\" in 2013 and \"No Good Duke Goes Unpunished\" in 2014.\n\n[No Good Duke Goes Unpunished]\nNo Good Duke Goes Unpunished is a historical romance written by Sarah MacLean and published by Avon in 2013.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q705d6c8063",
  "kind": "yes/no",
  "text": "Claim: The Russian-British physicist who shared the Nobel Prize in Physics in 2010 has established a reserach center dedicated to continuing the work with graphene in Singapore.\n\nPassages:\n\n[Konstantin Novoselov]\nSir Konstantin Sergeevich Novoselov (born 23 August 1974) is a Russian-British physicist, and Langworthy Professor in the School of Physics and Astronomy at the University of Manchester.\n\n[Graphene Research Centre]\nThe Graphene Research Centre (GRC), at the National University of Singapore (NUS), is the first centre in Asia dedicated to graphene research.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q438957a2be",
  "kind": "yes/no",
  "text": "Tweet: I like making food and then not eating it to assert my dominance",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qed462a3913",
  "kind": "yes/no",
  "text": "Claim: 3D Wayfinder is an indoor wayfinding software and service used to help visitors to navigate large public buildings such as institutions which award academic degrees.\n\nPassages:\n\n[University]\nA university (Latin: \"universitas\" , \"a whole\") is an institution of higher (or tertiary) education and research which awards academic degrees in various academic disciplines.\n\n[3D Wayfinder]\n3D Wayfinder is an indoor wayfinding software and service used to help visitors to navigate in large public buildings (shopping centers, airports, train stations, hospitals, universities etc.)",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q957f3ff5eb",
  "kind": "yes/no",
  "text": "Post: dad: \"are ya sending any of those boys from 5soz (wtf is a 5soz dad) a valentines gift?\" \nme: yes dad yes i am cuz im dating all of them duh",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qc9d181c326",
  "kind": "yes/no",
  "text": "Claim: The star of the 2009 film The Good Guy also starred in \"Violet and Daisy.\" She won a Primetime Emmy Award for her work on the Netflix drama series \"The Handmaid's Tale\".\n\nPassages:\n\n[The Good Guy (film)]\nThe Good Guy is a 2009 romantic comedy film directed by Julio DePietro starring Alexis Bledel, Scott Porter, and Bryan Greenberg.\n\n[Violet &amp; Daisy]\nViolet & Daisy is a 2011 American comedy crime drama film written, produced, and directed by Geoffrey S. Fletcher in his directorial debut after winning an Oscar for Best Adapted Screenplay for the film Precious. The film stars Saoirse Ronan, Alexis Bledel, Marianne Jean-Baptiste, Danny Trejo, and James Gandolfini in one of his last acting roles before his death on June 19, 2013.\n\n[Alexis Bledel]\nKimberly Alexis Bledel ( ; ] ; born September 16, 1981) is an American actress and model. She won a Primetime Emmy Award for her work on the Hulu drama series \"The Handmaid's Tale\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6b98787ea4",
  "kind": "yes/no",
  "text": "Claim: Park So-yeon was a members of a three piece girl group. So was the writer of the song that was the second single released from the group TLC, \"Hands Up\".\n\nPassages:\n\n[Hands Up (TLC song)]\nIt was written and produced by both Babyface and Daryl Simmons for the band's fourth studio album, \"3D\" (2002), and released as the album's second single following \"Girl Talk\" in the United States in November 2002.\n\n[Girl Talk (TLC song)]\nIt was written by band members Lisa Lopes and Tionne Watkins along with Anita McLoud, Edmund \"Eddie Hustle\" Clement, and Kandi Burruss for the group's fourth studio album, \"3D\" (2002).\n\n[Park So-yeon (singer)]\nShe is best known as the former main vocalist and member of South Korean girl group T-ara.\n\n[Tionne Watkins]\nBorn in Des Moines, Iowa, Watkins rose to fame in the early 1990s as a member of the girl-group TLC.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd620089ac7",
  "kind": "yes/no",
  "text": "Claim: St Anne's Academy is an 11–18 mixed comprehensive academy is located in a town that had 42,972 inhabitants in 2011.\n\nPassages:\n\n[Middleton, Greater Manchester]\nIn 2001, Middleton had a population of 45,580, reducing to 42,972 at the 2011 Census.\n\n[St Anne's Academy]\nSt Anne's Academy is an 11–18 mixed comprehensive academy in Middleton area of the Metropolitan Borough of Rochdale in Greater Manchester, United Kingdom.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6d8c9de876",
  "kind": "yes/no",
  "text": "Claim: Jordan Fished played the role of John Laurens in the Broadway production Hamilton.\n\nPassages:\n\n[Hamilton (musical)]\nHamilton: An American Musical is a sung- and rapped-through musical about the life of American Founding Father Alexander Hamilton, with music, lyrics and book by Lin-Manuel Miranda, inspired by the 2004 biography \"Alexander Hamilton\" by historian Ron Chernow. Notably incorporating hip-hop, rhythm and blues, pop music, traditional-style show tunes and color-conscious casting of non-white actors as the Founding Fathers and other historical figures, the musical achieved both critical acclaim and box office success.\n\n[Jordan Fisher]\nJordan William Fisher (born April 24, 1994) is an American singer, dancer and actor. He assumed the role of John Laurens/Philip Hamilton in the Broadway production of \"Hamilton\" on November 22, 2016.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q86bd6cd72a",
  "kind": "yes/no",
  "text": "Claim: Peggy Trentini made her acting debut in the 1982 film. \"Leni\" Riefenstahl was born before the award-winning director of the film.\n\nPassages:\n\n[Leni Riefenstahl]\nHelene Bertha Amalie \"Leni\" Riefenstahl (] ; 22 August 1902 – 8 September 2003) was a German film director, producer, screenwriter, editor, photographer, actress and dancer.\n\n[Peggy Trentini]\nTrentini made her film debut in 1982 with a small part in the comedy movie \"Young Doctors in Love\".\n\n[Garry Marshall]\nGarry Kent Marshall (November 13, 1934 – July 19, 2016) was an American actor, director, producer, writer, and voice artist best known for creating \"Happy Days\" and its various spin-offs, developing Neil Simon's 1965 play \"The Odd Couple\" for television, and directing \"Pretty Woman\", \"Runaway Bride\", \"Valentine's Day\", \"New Year's Eve\", \"Mother's Day\", \"\"The Princess Diaries\", and \"\".\n\n[Young Doctors in Love]\nYoung Doctors in Love is a 1982 American comedy film directed by Garry Marshall.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe81f84d8ab",
  "kind": "yes/no",
  "text": "Claim: A star of Hello! Stranger is the brother of the mixed martial artist of Canadian nationality.\n\nPassages:\n\n[Julien Kang]\nHe is the younger brother of mixed martial artist Denis Kang.\n\n[Hello! Stranger]\nStranger () is a 2014 South Korean television program starring Kim Kwang-kyu, Julien Kang, Kangnam and Mina Fujii.\n\n[Denis Kang]\nDenis Kang (Hangul: 강대수 , born September 17, 1977) is a Canadian professional mixed martial artist who most recently competed in the Middleweight division.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa2b67a4ba9",
  "kind": "yes/no",
  "text": "Claim: The host of the news program Way Too Early frequently serves as fill-in anchor on \"Today\" for a tv journalist that was the host of \"PM Magazine\" from 1980-86.\n\nPassages:\n\n[Willie Geist]\nGeist also frequently serves as fill-in anchor on \"Today\" for Matt Lauer.\n\n[Matt Lauer]\nHe was also host of \"PM Magazine\" (or \"Evening Magazine\" 1980–86).\n\n[Way Too Early]\nIt premiered on July 27, 2009 hosted by Willie Geist.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5ac55b190c",
  "kind": "yes/no",
  "text": "Claim: Ben Poquette graduated from Central Michigan University established in 1892.\n\nPassages:\n\n[Central Michigan University]\nCentral Michigan University (CMU) is a public research university located in Mount Pleasant in the U.S. state of Michigan. Established in 1892, Central Michigan University is one of the largest universities in the state of Michigan and one of the nation's 100 largest public universities.\n\n[Ben Poquette]\nBorn in Ann Arbor, Michigan, he graduated from East Lansing High School and Central Michigan University.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd08a5942c9",
  "kind": "yes/no",
  "text": "Claim: Kyriakos Georgiou is best known for playing this role. The man who he won the organisation's Tag Team Championship with is Canadian. Vengeance was a 2006 event produced by the organisation.\n\nPassages:\n\n[Vladimir Kozlov]\nHe is best known for his time in WWE, where he won the WWE Tag Team Championship once with Santino Marella.\n\n[Vengeance (2006)]\nVengeance (2006) was a professional wrestling pay-per-view (PPV) event produced by World Wrestling Entertainment (WWE), which took place on June 25, 2006, at the Charlotte Bobcats Arena in Charlotte, North Carolina.\n\n[Kyriakos Georgiou]\nHe is best known for playing the role of 'Vladimir Kozlov' in the films Criminals Game/Criminals Game II, he has also starred as James Baker in the film 'Duality' (\"written and directed by Jaimal Patel\").\n\n[Santino Marella]\nAnthony Carelli (born March 14, 1974) is a Canadian sports analyst, trainer, entrepreneur, actor, and retired professional wrestler and mixed martial artist, who currently works for the Canadian sports TV network Sportsnet.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q78ce43a98a",
  "kind": "yes/no",
  "text": "Claim: Wichita City Carnegie Library Building is centrally located in the most populous city in Kansas was built in 1915, and listed on the National Register of Historic Places in 1987.\n\nPassages:\n\n[Sedgwick County, Kansas]\nThe county seat is Wichita, the most populous city in the state.\n\n[Wichita City Carnegie Library Building]\nThe Wichita City Carnegie Library Building located at 220 S. Main Street in Wichita, Kansas, Sedgwick County, Kansas, United States, is a Carnegie library built in 1915. It was listed on the National Register of Historic Places in 1987.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q0dc295a509",
  "kind": "yes/no",
  "text": "Claim: The University at which Helmut Anheier holds a chair is located at Heidelberg, Baden-Württemberg.\n\nPassages:\n\n[Heidelberg University]\nHeidelberg University (German: \"Ruprecht-Karls-Universität Heidelberg\" ; Latin: \"Universitas Ruperto Carola Heidelbergensis\" ) is a public research university in Heidelberg, Baden-Württemberg, Germany.\n\n[Helmut Anheier]\nHe holds a chair at the Max Weber Institute of Sociology, Heidelberg University, where he is also the Academic Director of the Center for Social Investment and Innovation.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q7733e8ba1f",
  "kind": "yes/no",
  "text": "Claim: Imagine Dragons recorded the EP which features the song \"Hear Me\" at a studio. This recording studio is located in the unincorporated town that is part of Clark County.\n\nPassages:\n\n[Winchester, Nevada]\nWinchester is an unincorporated town and census-designated place (CDP) and part of Las Vegas Township in Clark County, Nevada, United States that contains part of the Las Vegas Strip.\n\n[Hell and Silence]\nIt was recorded at Battle Born Studios.\n\n[Hear Me (song)]\n\"Hear Me\" is a song by American rock band Imagine Dragons, originally written and recorded for their second extended play, \"Hell and Silence\".\n\n[Battle Born Studios]\nBattle Born Studios, located in the Winchester, Nevada, is a 2000 sqft recording studio owned by The Killers.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe7fe615c29",
  "kind": "yes/no",
  "text": "Post: @benshapiro it’s true, every time my little cousins put on their masks they choke to death and have to be revived. it’s very stressful for us.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qea6a23cd57",
  "kind": "yes/no",
  "text": "Claim: American singer Aaliyah had a video director that directed Soothe My Soul, and also had to face allegation of illegal marriage with R. Kelly.\n\nPassages:\n\n[Warren Fu]\nHe has directed promos for Daft Punk, The Weeknd, Snoop Dogg, Pharrell Williams, The Strokes, HAIM, The Killers, Depeche Mode, Weezer, Mark Ronson, Julian Casablancas, and Aaliyah.\n\n[Soothe My Soul]\nThe music video directed by Warren Fu was premiered on 28 March 2013.\n\n[Aaliyah]\nAfter facing allegations of an illegal marriage with R. Kelly, Aaliyah ended her contract with Jive and signed with Atlantic Records.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6987859d0e",
  "kind": "yes/no",
  "text": "Claim: This punk-influenced band and Catherine are linked by the rock genre of music. They released the compilation album The Best: Make the Music Go Bang!.\n\nPassages:\n\n[The Best: Make the Music Go Bang!]\nis a compilation American punk rock band X released in 2004.\n\n[Catherine (alternative rock band)]\nCatherine was an alternative rock band from Chicago, Illinois that was active from 1985 to 1998.\n\n[X (American band)]\nX is an American punk rock band, formed in Los Angeles in 1977, among the first wave of American punk.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2723f1cc88",
  "kind": "yes/no",
  "text": "Claim: The Contra Costa Canal was completed in an earlier year than the Deep Water Ship Channel.\n\nPassages:\n\n[Sacramento Deep Water Ship Channel]\nThe Sacramento Deep Water Ship Channel (also known as Sacramento River Deep Water Ship Channel or SRDWSC) is a canal from the Port of Sacramento in West Sacramento, California to the Sacramento River, which flows into San Francisco Bay. It was completed by the United States Army Corps of Engineers in 1963.\n\n[Contra Costa Canal]\nThe Contra Costa Canal is a 47 mi aqueduct in the U.S. state of California. Its construction began in 1937, with delayed completion until 1948 due to World War II shortages in labor and materials.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7c81644cd5",
  "kind": "yes/no",
  "text": "Text: Trader Joe's Candy Cane Joe-Joes are pure crack and I cave to them every year.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q3905204d31",
  "kind": "yes/no",
  "text": "Claim: The Curzon Ashton L.F.C. consists of ladies of the night.\n\nPassages:\n\n[Curzon Ashton F.C.]\nCurzon Ashton Football Club is a semi-professional football club based in the market town of Ashton-under-Lyne, Greater Manchester, England, that competes in the National League North, the sixth-highest division overall in the English football league system, and are members of the Manchester County Football Association.\n\n[Curzon Ashton L.F.C.]\nCurzon Ashton Ladies Football Club is an English women's football club affiliated with Curzon Ashton F.C..",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qb130d989c7",
  "kind": "yes/no",
  "text": "Claim: Robert Johnson Tenner played collegiate ball for a university. That university and Baylor College of Medicine are not located in the same state.\n\nPassages:\n\n[University of Minnesota]\nThe University of Minnesota, Twin Cities (often referred to as The University of Minnesota, Minnesota, the U of M, UMN, or simply the U) is a public research university in Minneapolis and Saint Paul, Minnesota.\n\n[Baylor College of Medicine]\nBaylor College of Medicine (BCM), located in the Texas Medical Center in Houston, Texas, US, is a health sciences university.\n\n[Bob Tenner]\nTenner played collegiate ball for the University of Minnesota and played professionally for 1 season, in 1935.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qfeea5ea268",
  "kind": "yes/no",
  "text": "Claim: The animated movie starring Lightning McQueen was released by the same company which used songs written by Lin-Manuel Miranda in another of its movies.\n\nPassages:\n\n[Lin-Manuel Miranda]\nLin-Manuel Miranda ( ; born January 16, 1980) is an American composer, lyricist, playwright, and actor best known for creating and starring in the Broadway musicals \"Hamilton\" and \"In the Heights\". He co-wrote the songs for Disney's \"Moana\" soundtrack (2016) and is set to star in their upcoming film \"Mary Poppins Returns\".\n\n[Cars 2]\nCars 2 is a 2011 American computer-animated action comedy spy film produced by Pixar Animation Studios for Walt Disney Pictures.\n\n[Lightning McQueen]\nLightning McQueen, typically referred to by his surname McQueen, is an anthropomorphic stock car in the animated Pixar film \"Cars\" (2006), its sequels \"Cars 2\" (2011), \"Cars 3\" (2017), and TV shorts known as \"Cars Toons.\"",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q66431b9971",
  "kind": "yes/no",
  "text": "Claim: The builder of the Hyundai Stellar is located in Seoul.\n\nPassages:\n\n[Hyundai Stellar]\nThe Hyundai Stellar (Hangul: ) was a mid-size rear-wheel drive automobile produced by the Hyundai Motor Company to succeed the soon to be replaced Ford Cortina that Hyundai were building under licence.\n\n[Hyundai Motor Company]\nThe Hyundai Motor Company (Hangul: 현대자동차 ; Hanja: 現代自動車 ; RR: \"Hyeondae Jadongcha \" ; Hangul: 현대 ; Hanja: 現代 ; MR: \"Hyŏndae \" , ] , \"modernity\"; ) is a South Korean multinational automotive manufacturer headquartered in Seoul, South Korea.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 }
]
