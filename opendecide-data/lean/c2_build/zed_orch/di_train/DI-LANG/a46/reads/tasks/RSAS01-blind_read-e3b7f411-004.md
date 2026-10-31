# A46 replay label-noise blind read RSAS01-blind_read-e3b7f411-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS01-blind_read-e3b7f411-004.json

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
  "qid": "q8c58729913",
  "kind": "yes/no",
  "text": "Post: people who think it’s funny to spike drinks are the actual scum of the earth",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qcd91346a4c",
  "kind": "yes/no",
  "text": "Claim: Wikimedia Foundation runs the website surpassed by both Baidu Baike and Kickstarter.\n\nPassages:\n\n[Baidu Baike]\nIts test version was released on 20 April 2006, and within three weeks the encyclopedia had grown to more than 90,000 articles surpassing the number in Chinese Wikipedia.\n\n[Chinese Wikipedia]\nThe Chinese Wikipedia () is the (Standard) Chinese language edition of Wikipedia. It is run by the Wikimedia Foundation.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0413dafca4",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I have been eating a lot of Kitkats lately!",
   "Pregnant and constantly crave KitKats. I literally have been living off of them for the past 4 months. @KitKat_US"
  ]
 },
 {
  "qid": "qfc29b90d4a",
  "kind": "yes/no",
  "text": "Claim: Hordes of Zombies is the last album to feature this bassist. The bassist and Troy Sanders are not members of the same band.\n\nPassages:\n\n[David Vincent]\nDavid Justin Vincent (born April 22, 1965), also known as Evil D, is an American musician who is best known as the former lead vocalist and bassist for the death metal band Morbid Angel as well as the bassist for Genitorturers.\n\n[Troy Sanders]\nTroy Jayson Sanders (born September 8, 1973) is an American musician, singer, and songwriter best known as a member of the Atlanta, Georgia metal band Mastodon, in which he plays bass and shares lead vocal duties with guitarist Brent Hinds and drummer Brann Dailor.\n\n[Hordes of Zombies]\nThis is Terrorizer's first album since 2006's \"Darker Days Ahead\" and the only one to feature vocalist Anthony Rezhawk and guitarist Katina Culture and the last album to feature bassist David Vincent.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3fb5433eb9",
  "kind": "yes/no",
  "text": "Claim: The writer of American Oxygen also worked on a track with the writer of \"Crack a Bottle\"which was released in February 2010. \"Crack a Bottle\" also featured Dr. Dre and 50 Cent.\n\nPassages:\n\n[American Oxygen]\nIt was written by Alex da Kid, Candice Pillay, Sam Harris and Rihanna; Alex da Kid and Kanye West produced it.\n\n[Alex da Kid]\nHe has gained recognition for producing several hit singles for a plethora of artists in various music genres, such as Dr. Dre (\"I Need a Doctor\"), Nicki Minaj (\"Massive Attack\"), B.o.B (\"Airplanes\" featuring Hayley Williams), Eminem (\"Love the Way You Lie\" featuring Rihanna), Diddy (\"Coming Home\" with Dirty Money featuring Skylar Grey), Imagine Dragons (\"Radioactive\") and Cheryl (\"Under The Sun\").\n\n[Crack a Bottle]\n\"Crack a Bottle\" is a song by American rapper Eminem, featuring American rappers Dr. Dre and 50 Cent.\n\n[Love the Way You Lie]\n\"Love the Way You Lie\" is a song recorded by the American rapper Eminem, featuring the Barbadian singer Rihanna, from Eminem's seventh studio album \"Recovery\" (2010).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q392bd535dc",
  "kind": "yes/no",
  "text": "Claim: A star of \"Hotline\" a 2014 film and a director are not both authors. This director directed the film \"The Love Thrill\".\n\nPassages:\n\n[Jeff Ragsdale]\nJeffrey Charles \"Jeff\" Ragsdale ( ) is an American author, documentary filmmaker, actor and stand-up comedian.\n\n[Hotline (2014 film)]\nThe film stars Miss Cleo, Jeff Ragsdale, Jamie Blaine, and Tonya Jone Miller.\n\n[Millard Webb]\nMillard Webb (6 December 1893 – 21 April 1935), was an American screenwriter and director.\n\n[The Love Thrill]\nThe Love Thrill is a lost 1927 silent film comedy directed by Millard Webb and starring Laura La Plante and Tom Moore.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q08db08e97e",
  "kind": "yes/no",
  "text": "Claim: Orontioideae is a subfamily of flowering plants in a family. One to two species of skunk cabbage from North America and Asia belong to that subfamily. That subfamily and Ageratum genus are not in the same family. Arisaema candidissimum lettuce is a member of the original family.\n\nPassages:\n\n[Lysichiton]\nLysichiton is a genus in the family Araceae.\n\n[Orontioideae]\nThe subfamily consists of three genera namely, \"Lysichiton\" (one to two species of skunk cabbage from North America and Asia), \"Orontium\" (golden club, one living species from eastern North America and two extinct species known from fossils), and \"Symplocarpus\" (several species of skunk cabbage from North America and Asia).\n\n[Arisaema candidissimum]\nArisaema candidissimum is a species of flowering plant in the arum family (Araceae), originating in western China (Tibet, Sichuan, Yunnan).\n\n[Ageratum]\nAgeratum ( ), (whiteweed in the USA), is a genus of 40 to 60 tropical and warm temperate flowering annuals and perennials from the family Asteraceae, tribe Eupatorieae.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa9eb5e4d34",
  "kind": "yes/no",
  "text": "Claim: Max Domi father, who was a player for the Maple Leafs, was of Albanian origin.\n\nPassages:\n\n[Tie Domi]\nTahir \"Tie\" Domi (born November 1, 1969) is a retired Canadian professional ice hockey player of Albanian origin.\n\n[Max Domi]\nHis father is former Toronto Maple Leafs legend Tie Domi.\n\n[Ontario Raiders]\nMaple Leaf Sports & Entertainment considered purchasing the team, but ultimately a group which included Bill Watters, the then Assistant General Manager of the Toronto Maple Leafs, Paul Beeston, former president of the Toronto Blue Jays, Tie Domi, player for the Maple Leafs, and Bobby Orr, former NHL player, bought it for $250,000 and promptly relocated the team to Toronto's Maple Leaf Gardens where they rebranded it the Toronto Rock.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2c56b9900e",
  "kind": "yes/no",
  "text": "Claim: Ferraria and the genus closely allied to Platylobium are both plant genus. Out of the two, the genus closely allied to Platylobium is native to an Asian country. The fashion designer Wayne Cooper is based in the country.\n\nPassages:\n\n[Bossiaea]\nBossiaea is a genus in the pea family (Fabaceae) consisting of about 70 species which are native to Australia.\n\n[Platylobium]\nThe genus was first described by James Edward Smith, and is closely allied to \"Bossiaea\", another genus within the Mirbelioids.\n\n[Wayne Cooper (fashion designer)]\nWayne Cooper is a British-born fashion designer based in Australia.\n\n[Ferraria]\nFerraria is a genus of monocotyledonous flowering plants in the family Iridaceae, native to tropical and southern Africa.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7b8b35cc0b",
  "kind": "yes/no",
  "text": "Claim: A song by David Guetta was produced by the Dutch DJ Afrojack. The signer who wrote and recorded I Don't Wanna Grow Up guested on this song.\n\nPassages:\n\n[Bebe Rexha]\nShe is best known as a featured guest vocalist on several \"Billboard\" Hot 100 charting songs, such as G-Eazy's \"Me, Myself & I\", David Guetta's \"Hey Mama\", Martin Garrix's \"In the Name of Love\" and Cash Cash's \"Take Me Home\".\n\n[Hey Mama (David Guetta song)]\n\"Hey Mama\" is a song by French DJ and record producer David Guetta, featuring vocals from Nicki Minaj and Bebe Rexha, as well as production from Dutch DJ and producer Afrojack.\n\n[I Don't Wanna Grow Up]\nI Don't Wanna Grow Up is the debut extended play (EP) by American pop recording artist Bebe Rexha.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qdae37cca98",
  "kind": "yes/no",
  "text": "Claim: The founder of Shock Trauma developed a prototype pacemaker in 1956. This pacemaker was used by the 34th President of the USA.\n\nPassages:\n\n[Dwight D. Eisenhower]\nDwight David \"Ike\" Eisenhower ( ; October 14, 1890 – March 28, 1969) was an American politician and Army general who served as the 34th President of the United States from 1953 until 1961.\n\n[R Adams Cowley Shock Trauma Center]\nShock Trauma was founded by R Adams Cowley, who is considered the father of trauma medicine.\n\n[R Adams Cowley]\nR Adams Cowley (July 25, 1917 – October 27, 1991), the \"Father of Trauma Medicine,\" was an American surgeon considered a pioneer in emergency medicine and the treatment of shock trauma. He is also known for being one of the first surgeons to perform open-heart surgery and invented both a surgical clamp that bears his name and a prototype pacemaker that was used by Dwight D. Eisenhower.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3e00c9c213",
  "kind": "yes/no",
  "text": "Claim: Ted Tetzlaff and David Siegel were not both film actors.\n\nPassages:\n\n[David Siegel (screenwriter)]\nDavid Siegel is an American film director, screenwriter and producer, and part of a long-standing writing-directing-producing team with filmmaker Scott McGehee.\n\n[Ted Tetzlaff]\nDale H. \"Ted\" Tetzlaff (3 June 1903, Los Angeles, California – 7 January 1995, Sausalito, California) was a noted Academy Award-nominated Hollywood cinematographer active in the 1930s and 1940s.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qff9352f3a0",
  "kind": "yes/no",
  "text": "Claim: National Artist of the USSR is the alternate translation for the honorary title of which Vladimir Basov and Inna Churikova were both 20th-century recipients.\n\nPassages:\n\n[People's Artist of the USSR]\nPeople's Artist of the USSR (Russian: Наро́дный арти́ст СССР , \"Narodný artist SSSR\"), also sometimes translated as National Artist of the USSR, was an honorary title granted to artists of the Soviet Union.\n\n[Walking the Streets of Moscow]\nThe film also features cameos by four People's Artists of the USSR: Rolan Bykov, Vladimir Basov, Lev Durov, and Inna Churikova.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc7199aa5ce",
  "kind": "yes/no",
  "text": "Claim: Anthony Sandler is the Chief of Pediatric Surgery at a major hospital. Georgetown University School of Medicine works in association with the hospital that is the largest private hospital in Washington, D.C., not this hospital.\n\nPassages:\n\n[Georgetown University School of Medicine]\nThe School of Medicine works in association with the 609-bed Georgetown University Hospital, Washington Hospital Center, and nine other affiliated federal and community hospitals in the Washington metropolitan area.\n\n[Children's National Medical Center]\nChildren’s National Medical Center (formerly DC Children’s Hospital) is ranked among the top 10 children’s hospitals in the country by \"U.S. News & World Report.\"\n\n[Anthony Sandler]\nAnthony Sandler is the Chief of Pediatric Surgery at Children's National Medical Center, where he also serves as the Principal Investigator in the Children's Research Institute and the Center for Cancer and Immunology Research (CCIR).\n\n[MedStar Washington Hospital Center]\nMedStar Washington Hospital Center is the largest private hospital in Washington, D.C. A member of MedStar Health, the not-for-profit Hospital Center is licensed for 926 beds.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qf5ca74c58f",
  "kind": "yes/no",
  "text": "Claim: \"Funnybot\" is the second episode of the fifteenth season of South Park, an American and adult animated television series created by Trey Parker and Matt Stone.\n\nPassages:\n\n[South Park (season 10)]\nThe tenth season of \"South Park\", an American animated television series created by Trey Parker and Matt Stone, began airing on March 22, 2006.\n\n[Funnybot]\n\"Funnybot\" premiered in the United States on Comedy Central on May 4, 2011, the first time a \"South Park\" episode has aired in May since season 10's \"Tsst\" in 2006.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q8f8394485d",
  "kind": "yes/no",
  "text": "Claim: This band released \"We Will Become Silhouettes\" on February 8, 2005. That band has more members than the British band Missio.\n\nPassages:\n\n[We Will Become Silhouettes]\n\"We Will Become Silhouettes\" is a single by US indie band The Postal Service, released February 8, 2005 under the Sub Pop Records label.\n\n[Missio (duo)]\nIt currently consists of founding member Matthew Brue (vocals, producer), and David Butler (producer, instrumentalist).\n\n[The Postal Service]\nThe Postal Service were an American indie rock band from Seattle, Washington, consisted of vocalist Ben Gibbard (of Death Cab for Cutie), producer Jimmy Tamborello (of Dntel and Headset), with Jenny Lewis (of Rilo Kiley) on background vocals.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa3afe3c7b4",
  "kind": "yes/no",
  "text": "Claim: The director of Fallo! and Baltasar Kormákur are not both from the same country.\n\nPassages:\n\n[Tinto Brass]\nGiovanni \"Tinto\" Brass (born 26 March 1933) is an Italian filmmaker.\n\n[Baltasar Kormákur]\nBaltasar Kormákur Samper (born 27 February 1966) is an Icelandic actor, theater and film director, and film producer.\n\n[Fallo!]\nis a 2003 Italian film co-written and directed by Tinto Brass.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q7edc1f6c33",
  "kind": "yes/no",
  "text": "Claim: A sequel to a German romantic fantasy film featuring Reinhard Hauff and Solveig Dommartin is Faraway, So Close!\n\nPassages:\n\n[Richard Reitinger]\nReitinger later reunited with Wenders to write the \"Wings of Desire\" sequel \"Faraway, So Close!\n\n[Wings of Desire]\nWings of Desire (German: Der Himmel über Berlin , 'The Heavens Over Berlin' ) is a 1987 romantic fantasy film directed by Wim Wenders. One of the angels, played by Bruno Ganz, falls in love with a beautiful, lonely trapeze artist, played by Solveig Dommartin.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q758283f8d9",
  "kind": "yes/no",
  "text": "Claim: Bauneg Beg Mountain is seven meters taller than the mountain region covers the town of Ogunquit. It is a summer resort whose name means \"beautiful place by the sea\".\n\nPassages:\n\n[Bauneg Beg Mountain]\nBauneg Beg Mountain is taller than Mount Agamenticus, and has been used by mariners to navigate the Maine Coast.\n\n[Agamenticus]\nThe Mount Agamenticus region covers nearly 30,000 acres (121 km²) in the southern Maine towns of Eliot, Ogunquit, South Berwick, Wells and York.\n\n[Ogunquit]\nThe summer resort's name means \"beautiful place by the sea\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qbeb0429367",
  "kind": "yes/no",
  "text": "Claim: Angostura bitters and Springbokkie are an unknown mixture.\n\nPassages:\n\n[Springbokkie]\nThe Springbokkie (\"little Springbok\" in the Afrikaans language), composed of creme de menthe (\"or substitutes\") and Amarula, is a cocktail shooter that is popular in South Africa.\n\n[Angostura bitters]\nAngostura bitters ( ) is a concentrated bitters, or botanically infused alcoholic mixture, made of water, 44.7% ethanol, gentian, herbs and spices, by House of Angostura in Trinidad and Tobago.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q64aab27fcc",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Well. That went well. #BelgianGP",
   "No start to the race? This doesn't look good."
  ]
 },
 {
  "qid": "q27418fbb30",
  "kind": "yes/no",
  "text": "Claim: Olathe North High School is in the school district in the northwest Kansas City Metropolitan Area.\n\nPassages:\n\n[Olathe School District]\nThe Olathe Unified School District (Kansas Unified School District 233) is one of the major school districts in the Kansas City Metropolitan Area and is one of the larger school districts in the state of Kansas.\n\n[Olathe North High School]\nThe school is one of five public high schools in the Olathe School District.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8a71d3871e",
  "kind": "yes/no",
  "text": "Text: Loving the representation from South Yorkshire 🥰🥰 #GodsOwn #England #ENG #bbcfootball #bbc",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q0b57a01021",
  "kind": "yes/no",
  "text": "Text: Worked out 2 days in a row. I am quite literally the epitome of health and fitness",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qbb79179e20",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "\"I really don't like that I am still getting as frustrated over websites crashing when I'm buying tickets as I did when I was younger\"",
   "i’m sure 14 year old me would be delighted to know that 22 year old me is still getting stressed over websites crashing for bands🙃"
  ]
 },
 {
  "qid": "q4f65d499d8",
  "kind": "yes/no",
  "text": "Claim: 25 August 1954 is the birthdate of this Canadian musician, singer-songwriter, and record producer, who began his career in the early 1970s, and whose seventeenth studio album was All This Useless Beauty.\n\nPassages:\n\n[Elvis Costello]\nDeclan Patrick MacManus (born 25 August 1954), better known by his stage name Elvis Costello, is an English musician, singer-songwriter, and record producer.\n\n[All This Useless Beauty]\nAll This Useless Beauty is the seventeenth studio album by the English singer-songwriter Elvis Costello, released in 1996 by Warner Brothers.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa71407abb3",
  "kind": "yes/no",
  "text": "Claim: Andrés Muschietti directed this English-language Spanish supernatural drama horror film. This film starred an actress. The actress also starred in \"Grumpy Cat's Worst Christmas Ever\"\n\nPassages:\n\n[Megan Charpentier]\nMegan Charpentier is a Canadian actress who is perhaps best known for her role as the feral child Victoria in the 2013 horror film \"Mama\" and as the new Red Queen in \"\".\n\n[Andy Muschietti]\nAndrés Muschietti (] ;; born 26 August 1973), usually credited as Andy Muschietti, is an Argentine film director and screenwriter, best known for directing the 2013 horror film \"Mama\" and the 2017 adaptation of Stephen King's \"It\".\n\n[Mama (2013 film)]\nMama is a 2013 English-language Spanish supernatural drama horror film directed and co-written by Andy Muschietti and based on his 2008 Argentine short film \"Mamá\".\n\n[Grumpy Cat's Worst Christmas Ever]\nThe movie first aired on the Lifetime on November 29, 2014 and stars Megan Charpentier as a young girl that befriends and later adopts Grumpy Cat, only to discover that the two can communicate with one another.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q6edf2974d3",
  "kind": "yes/no",
  "text": "Claim: Saulo Ribeiro's was trained in Portuguese Jiu-Jitsu by this person. The trainer was a student of the person who also taught Romero Cavalcanti and ran the Gracie Humaitá school in Rio de Janeiro.\n\nPassages:\n\n[Rolls Gracie]\nRolls Gracie ([ˈɡɾejsi] 1951–1982) was a Brazilian martial artist. He was teacher of Rickson Gracie, Carlos Gracie Jr., Royler Gracie, Márcio \"Macarrão\" Stambowsky, Rigan Machado and Romero \"Jacare\" Cavalcanti.\n\n[Saulo Ribeiro]\nAfter earning a black belt in Judo, he began his training of Brazilian Jiu-Jitsu in Rio de Janeiro under Royler Gracie, the son of Hélio Gracie, at the famous Gracie Humaitá.\n\n[Rodrigo Medeiros]\nHe received his black belt from Rolls Gracie student, Romero \"Jacaré\" Cavalcanti, he also trained under Fernando 'Magrao' Gurgel and is one of a select group of Jiu-Jitsu competitors to have won the prestigious World Jiu-Jitsu Championship openweight titles twice.\n\n[Royler Gracie]\nHe ran the Gracie Humaitá school in Rio de Janeiro, Brazil for many years under his father Helio's direction, but currently lives in San Diego.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q377380a105",
  "kind": "yes/no",
  "text": "Post: @brruhia Nah bruh you just drinking it upside down 😂",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q27eb065b5d",
  "kind": "yes/no",
  "text": "Claim: The writer of the songs in All We Know Is Falling is younger than the lead singer of heavy metal band CWHL. I Am the Night was also the last album to feature this lead singer.\n\nPassages:\n\n[I Am the Night]\nIt was also the last album to feature lead singer Terry Glaze.\n\n[All We Know Is Falling]\nAll songs were written by vocalist Hayley Williams and guitarist Josh Farro.\n\n[Hayley Williams]\nHayley Nichole Williams (born December 27, 1988) is an American singer, songwriter and musician. The band consists of Hayley Williams, Zac Farro and Taylor York.\n\n[Terry Glaze]\nTerrence Lee Glaze (born November 29, 1964, Columbus), known as Terry Lee, is a Texas-raised singer and guitarist who is most known for his work in American heavy metal bands Lord Tracy and Pantera.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9a063574a5",
  "kind": "yes/no",
  "text": "Claim: A star of \"Hotline\" a 2014 film and a director are not both authors. This director directed the fictional film \"The Love Thrill\".\n\nPassages:\n\n[Jeff Ragsdale]\nJeffrey Charles \"Jeff\" Ragsdale ( ) is an American author, documentary filmmaker, actor and stand-up comedian.\n\n[Millard Webb]\nMillard Webb (6 December 1893 – 21 April 1935), was an American screenwriter and director.\n\n[Hotline (2014 film)]\nThe film stars Miss Cleo, Jeff Ragsdale, Jamie Blaine, and Tonya Jone Miller.\n\n[The Love Thrill]\nThe Love Thrill is a lost 1927 silent film comedy directed by Millard Webb and starring Laura La Plante and Tom Moore.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qdae98d626c",
  "kind": "yes/no",
  "text": "Claim: A 400-year-old wine cellar was below an influential rock music venue which changed little until its closure featured an American folk singer-songwriter who has had a music career spanning more than fifty years.\n\nPassages:\n\n[Tom Paxton]\nThomas Richard Paxton (born October 31, 1937) is an American folk singer-songwriter who has had a music career spanning more than fifty years.\n\n[Bunjies]\nBelow the café, in a 400-year-old wine cellar, was an influential music venue which changed little until its closure (and conversion of the premises into a restaurant) in 1999.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qd99637b4a5",
  "kind": "yes/no",
  "text": "Tweet: I like making food and then not eating it to assert my dominance",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q3b1d9b5f29",
  "kind": "yes/no",
  "text": "Claim: The white supremacist who wrote a biography about serial killer Joseph Paul Franklin founded the National Alliance major white nationalist organization.\n\nPassages:\n\n[Joseph Paul Franklin]\nJoseph Paul Franklin (born James Clayton Vaughn, Jr.; April 13, 1950 – November 20, 2013) was an American serial killer who gained notoriety for numerous murders in the late 1970s and early 1980s. His killing spree was the subject of a fictional novel entitled \"Hunter\" by White supremacist William L. Pierce, who said of Franklin that “he saw his duty as a white man and did what a responsible son of his race must do.”\n\n[William Luther Pierce]\nPierce founded the National Alliance, a major white nationalist organization, which he led for almost thirty years.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd19b4b49ac",
  "kind": "yes/no",
  "text": "Text: JUSTICE HAS BEEN DONE.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q4d5a7b4226",
  "kind": "yes/no",
  "text": "Claim: Tothill Fields was an 18th-century area of Westminster in the county of Middlesex, a historic county in south-east region of England.\n\nPassages:\n\n[Middlesex]\nMiddlesex ( , abbreviation: Middx) is a historic county in south-east England.\n\n[Tothill Fields]\nTothill Fields was an 18th-century area of Westminster in the county of Middlesex that lay south of St James's Park on the north bank of the river Thames.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q0fa8c0cd87",
  "kind": "yes/no",
  "text": "Claim: Hugh Dowding, a character played by Laurence Olivier in 1969, was an officer in the Royal Air Force.\n\nPassages:\n\n[Hugh Dowding]\nAir Chief Marshal Hugh Caswall Tremenheere Dowding, 1st Baron Dowding, (24 April 1882 – 15 February 1970) was an officer in the Royal Air Force.\n\n[Battle of Britain (film)]\nThe film drew many respected British actors to accept roles as key figures of the battle, including Sir Laurence Olivier as Hugh Dowding and Trevor Howard as Keith Park.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q674400f533",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "\"i'm reading 4 books at once, let's see if i can actually finish them all\"",
   "i’m now reading 4 books at once what could go wrong 🧡"
  ]
 },
 {
  "qid": "qa3a32a70e3",
  "kind": "yes/no",
  "text": "Claim: The manager of the 2000 country music group inspired by boy bands was convicted in 2008.\n\nPassages:\n\n[Marshall Dyllon]\nMarshall Dyllon was an American country music group formed in 2000, comprising vocalists Daniel Cahoon, Jesse Littleton, Michael Martin, Paul Martin, and Todd Michael Sansom. These five members were recruited by country music artist Kenny Rogers and talent manager Lou Pearlman, in an attempt to bring the boy band sound to the country music scene.\n\n[Lou Pearlman]\nIn 2008, Pearlman was convicted and sentenced to up to 25 years in prison.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q22b3a2553c",
  "kind": "yes/no",
  "text": "Claim: The population of the city in which the radio station WBZW is located was 41,496 in 2010.\n\nPassages:\n\n[Altamonte Springs, Florida]\nAltamonte Springs is a suburban city in Seminole County, Florida, United States, which had a population of 41,496 at the 2010 census.\n\n[WBZW]\nWBZW (1520 AM) is a radio station in Altamonte Springs, Florida.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd9530a910b",
  "kind": "yes/no",
  "text": "Post: Watching all these important venues closing over time sucks horribly, but this one hurts. Fuck. #FabricReview",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q800a8666e8",
  "kind": "yes/no",
  "text": "Claim: The Head Office of the starter of the No issue, lelo tissue ad campaign is in Islamabad.\n\nPassages:\n\n[No issue, lelo tissue]\nNo issue, lelo tissue (Urdu: ‎ ) was a Pakistani television advertisement campaign started by Jazz Pakistan, following the victory of Pakistan's cricket team in the 2017 ICC Champions Trophy Final.\n\n[Jazz Pakistan]\nJazz (Urdu: ‎ ) is the largest mobile network in Pakistan formed by the merger of Mobilink and Warid. Its Head Office is located in Islamabad, and the current CEO is Aamir Ibrahim.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7cea90fd7c",
  "kind": "yes/no",
  "text": "Claim: The IRA used a Barrack buster to shoot down a British Army Lynx helicopter.\n\nPassages:\n\n[Barrack buster]\nBarrack buster is the colloquial name given to several improvised mortars, developed in the 1990s by the engineering group of the Provisional Irish Republican Army (IRA).\n\n[1994 British Army Lynx shootdown]\nOn 20 March 1994, a British Army Lynx helicopter was shot down by the Provisional Irish Republican Army (IRA) in Northern Ireland.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q41cea37334",
  "kind": "yes/no",
  "text": "Claim: Diego Félix of Austria was the fourth son of the lord of the Seventeen Provinces of the Netherlands in 1555.\n\nPassages:\n\n[Philip II of Spain]\nFrom 1555, he was lord of the Seventeen Provinces of the Netherlands.\n\n[Diego, Prince of Asturias]\nDiego Félix of Austria, Prince of Asturias and Portugal (August 15, 1575 – November 21, 1582) was the fourth son of Philip II of Spain, and also his third son by his fourth wife Anna of Austria.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q38d359974c",
  "kind": "yes/no",
  "text": "Claim: Mr. & Mrs. Mxyzptlk is an episode of the superhero TV series that originally aired on the Sunrise Inc. network.\n\nPassages:\n\n[Mr. &amp; Mrs. Mxyzptlk]\n\"Mr. & Mrs. Mxyzptlk\" is the thirteenth episode of the second season from The CW television series \"Supergirl\", which aired on February 20, 2017.\n\n[Supergirl (TV series)]\nSupergirl is an American superhero action-adventure television series developed by Ali Adler, Greg Berlanti and Andrew Kreisberg (the latter two having previously created \"Arrow\" and \"The Flash\") that originally aired on CBS and premiered on October 26, 2015.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6dff3c3948",
  "kind": "yes/no",
  "text": "Tweet: lalisa and money are so good and perfect for lisa i’m so so proud of her and i can’t wait for the live performance",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q62d35f6a37",
  "kind": "yes/no",
  "text": "Claim: The 2015 MTV Video Music Awards pre-show premiered the music video for a piano ballad with a prominent dream pop influence.\n\nPassages:\n\n[Wildest Dreams (Taylor Swift song)]\n\"Wildest Dreams\" is a song recorded by American singer-songwriter Taylor Swift for her fifth studio album, \"1989\". Musically, \"Wildest Dreams\" is a love ballad with a prominent dream pop influence, with the lyrics describing Swift's plea for her lover to remember her.\n\n[2015 MTV Video Music Awards]\nThe 2015 MTV Video Music Awards were held on August 30, 2015. Swift's \"Wildest Dreams\" music video premiered during the pre-show.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q5b00ca1042",
  "kind": "yes/no",
  "text": "Claim: Focus is a 2015 American romantic crime comedy-drama film starring an Australian actress who was also cast in Neighbours.\n\nPassages:\n\n[Margot Robbie]\nMargot Elise Robbie ( ; born 2 July 1990) is an Australian actress and producer. She was later cast in the soap opera \"Neighbours\" (2008–2011), which earned her two Logie Award nominations.\n\n[Focus (2015 film)]\nFocus is a 2015 American romantic crime comedy-drama film written and directed by Glenn Ficarra and John Requa, starring Will Smith, Margot Robbie, and Rodrigo Santoro.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe2549870b3",
  "kind": "yes/no",
  "text": "Claim: The band whose debut album is called Tending the Rose Garden was formed earlier than Starflyer 59.\n\nPassages:\n\n[The Innocence Mission]\nThe Innocence Mission (stylized as the innocence mission on all releases since 1995) is an American folk rock band centered on husband-and-wife singer-songwriters Karen and Don Peris. The group, including Mike Bitts (bass guitar) and Steve Brown (drums), was formed in Lancaster, Pennsylvania in the early 1980s when the members met during a Catholic school production of \"Godspell\".\n\n[Starflyer 59]\nStarflyer 59 is an alternative rock band from Riverside, California that was founded in 1993 by Jason Martin, brother of Ronnie Martin of Joy Electric.\n\n[Tending the Rose Garden]\nTending the Rose Garden is the 1986 debut EP by Catholic rock band The Innocence Mission.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qf5c0d6c353",
  "kind": "yes/no",
  "text": "Post: James Harden is allowed to travel every time he drives apparently",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 }
]
