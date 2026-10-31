# A46 replay label-noise blind read RSAS03-blind_read-625d486d-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS03-blind_read-625d486d-001.json

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
  "qid": "q0900bc914c",
  "kind": "yes/no",
  "text": "Claim: The 99p Challenge is presented by an English comedian who was born in East Dulwich, south London, and who came to prominence through her comedy partnership with Mel Giedroyc in Mel and Sue.\n\nPassages:\n\n[The 99p Challenge]\nThe show is presented by Sue Perkins and features a selection of regular panelists such as Armando Iannucci and regular writers Kevin Cecil, Andy Riley, Jon Holmes and Tony Roche.\n\n[Sue Perkins]\nSusan Elizabeth \"Sue\" Perkins (born 22 September 1969) is an English comedian, broadcaster, actress and writer, born in East Dulwich, south London. Originally coming to prominence through her comedy partnership with Mel Giedroyc in \"Mel and Sue\", she has since become best known as a radio broadcaster and television presenter, notably of \"The Great British Bake Off\" (2010–2016) and \"Insert Name Here\" (2016–present).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7c45ac6e34",
  "kind": "yes/no",
  "text": "Claim: The charter airport that is a 30-minute drive from Coldwaltham, is the busiest airport in the United Kingdom outside of London.\n\nPassages:\n\n[Heathrow Airport]\nHeathrow Airport (also known as London Heathrow) (IATA: LHR, ICAO: EGLL) is a major international airport in London, United Kingdom.\n\n[Gatwick Airport]\nGatwick Airport (also known as London Gatwick) (IATA: LGW, ICAO: EGKK) is a major international airport in south-east England, 29.5 mi south of Central London and 2.7 NM north of Crawley. It is the second-busiest airport by total passenger traffic in the United Kingdom, after London Heathrow.\n\n[Coldwaltham]\nIt is around a 30-minute drive from Gatwick Airport.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9adef7ff2c",
  "kind": "yes/no",
  "text": "Claim: A band that covered \"The Metro\" is Dionysian. The developer of the Donchian channel is also Dionysian.\n\nPassages:\n\n[System of a Down]\nSystem of a Down, sometimes shortened to System and abbreviated as SOAD, is an Armenian-American heavy metal band from Glendale, California, formed in 1994.\n\n[Richard Donchian]\nRichard Davoud Donchian (born September 1905, Hartford, Connecticut – d. 1993) was an Armenian-American commodities and futures trader, and pioneer in the field of managed futures.\n\n[The Metro (song)]\nIt has been covered by a number of artists, including System of a Down, Alkaline Trio, John Frusciante, Hannah Fury, Idle Warship and The Interrupters.\n\n[Donchian channel]\nThe Donchian channel is an indicator used in market trading developed by Richard Donchian.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe0dba08259",
  "kind": "yes/no",
  "text": "Claim: This individual, along with Jacki Bond, was one of two British female vocalists signed to Strike or its subsidiary, Go. Her husband, George Michael Dolenz, contains more letters in his name than Jesse James Dupree.\n\nPassages:\n\n[Samantha Juste]\nIn 1968 she married Micky Dolenz of the Monkees.\n\n[Jesse James Dupree]\nDupree is the lead singer, guitarist, and primary songwriter in the rock band Jackyl, founded in 1991.\n\n[Jacki Bond]\nShe came from South London and, with Samantha Juste, who co-hosted BBC television's \"Top of the Pops\", was one of two British female vocalists signed to Strike or (in Juste's case) its subsidiary, Go.\n\n[Micky Dolenz]\nGeorge Michael Dolenz, Jr. (born March 8, 1945) is an American actor, musician, television director, radio personality and theater director, best known as a vocalist and drummer of the 1960s pop/rock band the Monkees.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q41a01d2d16",
  "kind": "yes/no",
  "text": "Claim: Libya in the Maghreb region of North Africa has the 34,000 capacity First Statement Stadium.\n\nPassages:\n\n[First Statement Stadium]\nFirst Statement Stadium (Arabic: ملعب البيان الأول‎ ‎ ) is a multi-purpose stadium in Benghazi, Libya.\n\n[Libya]\nLibya (Arabic: ليبيا‎ ‎ \"Lībiyā \") is a country in the Maghreb region of North Africa, bordered by the Mediterranean Sea to the north, Egypt to the east, Sudan to the southeast, Chad and Niger to the south and Algeria and Tunisia to the west.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2429aa0144",
  "kind": "yes/no",
  "text": "Claim: Domenico Salvatori is a famous male singer with a voice equivalent to that of a soprano, mezzo-soprano, or contralto.\n\nPassages:\n\n[Domenico Salvatori]\nDomenico Salvatori (27 September 1855 – 11 December 1909) along with Alessandro Moreschi, Domenico Mustafà and Giovanni Cesari, was one of the famous castrati singers of the late 19th century.\n\n[Castrato]\nA castrato (Italian, plural: \"castrati\") is a type of classical male singing voice equivalent to that of a soprano, mezzo-soprano, or contralto.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfe6b0863e8",
  "kind": "yes/no",
  "text": "Claim: Green on Red and Hollywood Undead are both rock bands.\n\nPassages:\n\n[Green on Red]\nGreen on Red was an American rock band, formed in the Tucson, Arizona punk scene, but based for most of its career in Los Angeles, California, where it was loosely associated with the Paisley Underground.\n\n[Hollywood Undead]\nHollywood Undead is an American rap rock band from Los Angeles, California, formed in 2005.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q5c46062504",
  "kind": "yes/no",
  "text": "Claim: The older sister of Noah Cyrus is a vocalist. The older sister of the vocalist for Love/Hate, who contributed to the album Quiet Riot 10, is also a vocalist.\n\nPassages:\n\n[Trace Cyrus]\nIn 2010, he began providing vocals and guitar in the pop rock band Ashland HIGH.\n\n[Jizzy Pearl]\nJizzy Pearl (born James Wilkinson) is an American vocalist that was born on March 17, 1958, in Chicago, Illinois.\n\n[Quiet Riot 10]\nLove/Hate vocalist Jizzy Pearl joined the band in November 2013 and performs lead vocals on the six studio tracks.\n\n[Noah Cyrus]\nShe is the youngest daughter of Tish Cyrus and Billy Ray Cyrus and the younger sister of Miley Cyrus and Trace Cyrus.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q22607002b9",
  "kind": "yes/no",
  "text": "Claim: This woman directed the 2005 Disney Channel Original starring Whitney Sloan as Hollywood Henderson and whose soundtrack was released on June 7th. She also directed the musical film Sugar & Spice.\n\nPassages:\n\n[Sugar &amp; Spice]\nSugar & Spice is a 2001 American teen crime comedy film directed by Francine McDougall, and starring Marley Shelton, Marla Sokoloff, Mena Suvari, James Marsden, and Melissa George.\n\n[Whitney Sloan]\nWhitney Adela Sloan (born 21 August 1988 in London) is a British-born actress best known for playing her role as \"Hollywood Henderson\" in the Disney Channel Original Movie \"Go Figure\".\n\n[Go Figure (film)]\nGo Figure is 2005 Disney Channel Original Movie. Walt Disney Records released the \"Go Figure\" soundtrack on June 7, featuring the title track by Everlife along with a music video.\n\n[Francine McDougall]\nShe also directed the Disney Channel Original Movies \"Go Figure\" (2005) and \"Cow Belles\" (2006).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q385b6991a8",
  "kind": "yes/no",
  "text": "Post: Started watching house of cards, 4 episodes in. Already I can see it was a good choice😄",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q06d2a6055d",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Halfway through snowboarding day 1 and pretty sure I have fallen at least 69 times 😆♋️",
   "Halfway through snowboarding day 1 and pretty sure I have fallen at least 10 times."
  ]
 },
 {
  "qid": "q5ad8fc45e7",
  "kind": "yes/no",
  "text": "Claim: The 24th Hong Kong Film Awards ceremony was a positive for the 2004 Hong Kong romantic film written and produced by Wong Kar-wai.\n\nPassages:\n\n[24th Hong Kong Film Awards]\nTwenty-nine winners in nineteen categories were unveiled, with films \"Kung Fu Hustle\" and \"2046\" being the year's biggest winners.\n\n[2046 (film)]\n2046 is a 2004 Hong Kong romantic drama film written and directed by Wong Kar-wai.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qcdc04d2b7b",
  "kind": "yes/no",
  "text": "Claim: Third Division Stoke City football club has a new shirt sponsor based in the United Kingdom.\n\nPassages:\n\n[Bet365]\nBet365 Group Ltd (styled as \"bet365\") is a gambling company based in the United Kingdom.\n\n[2012–13 Stoke City F.C. season]\nIt was also the club's 150th year in existence and to mark the occasion the club had a special crest and the away kit was the same colours that Stoke Ramblers wore back in 1863, navy and cardinal Stoke also had a new shirt sponsor Bet365 taking over from Britannia.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q98fc4c3beb",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Sky news is bias",
   "What happened to unbiased journalism @SkyNews?"
  ]
 },
 {
  "qid": "q634db1c1f4",
  "kind": "yes/no",
  "text": "Claim: In the early 17th-century the black Angolan who was one of the earliest African-American landowners in the United States,acieved freedom.\n\nPassages:\n\n[Zipporah Potter Atkins]\nThe purchase of her home, dated 1670, makes her the first African American to own land in the city of Boston, and with Anthony Johnson (colonist) one of the earliest African-American landowners in what would become the United States.\n\n[Anthony Johnson (colonist)]\nAnthony Johnson ( 1600 – 1670) was a black Angolan who achieved freedom in the early 17th-century Colony of Virginia after serving his term of indenture.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe39e3029af",
  "kind": "yes/no",
  "text": "Claim: The 2010 population of the city where a newspaper was published is 114,297. This newspaper once had Ronald Clair Roat as a writer.\n\nPassages:\n\n[Lansing, Michigan]\nLansing is the capital of the US state of Michigan. It is mostly in Ingham County, although portions of the city extend west into Eaton County and north into Clinton County. The 2010 Census placed the city's population at 114,297, making it the fifth largest city in Michigan.\n\n[Ronald Clair Roat]\nThe newspapers included the \"Lansing State Journal\", \"Dominion News\" (Morgantown, W.Va.) , \"Dayton Daily News\", and \"The Times\" in Frankfort, Ind.\n\n[Lansing State Journal]\nThe Lansing State Journal is a daily newspaper published in Lansing, Michigan owned by Gannett.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2f17461557",
  "kind": "yes/no",
  "text": "Claim: The political party that Kayithi Narsi Reddy associates with was founded in February 1885.\n\nPassages:\n\n[Indian National Congress]\nFounded in 1885, it was the first modern nationalist movement to emerge in the British Empire in Asia and Africa.\n\n[Kayithi Narsi Reddy]\nKayithi Narsi Reddy is an Indian politician initially associated with INC and then with YSR Congress Party.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7f76ebfbc1",
  "kind": "yes/no",
  "text": "Tweet: I just love when Twitter decides to reload the timeline seconds after you just opened it up and are in the middle of reading it.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q52e855ff51",
  "kind": "yes/no",
  "text": "Claim: The 1962 film where Dan Shor plays Ram, stars Jeff Bridges as a computer programmer, not The Million Dollar Duck.\n\nPassages:\n\n[Dan Shor]\nHis most recognized roles include Ram in \"Tron\" (1982) and Billy the Kid in \"Bill & Ted's Excellent Adventure\" (1989).\n\n[The Million Dollar Duck]\nThe Million Dollar Duck (also titled as The $1,000,000 Duck) is a 1971 American comedy film produced by Walt Disney Productions about a goose that lays golden eggs scenario.\n\n[Tron]\nTron is a 1982 American science fiction action-adventure film written and directed by Steven Lisberger, based on a story by Lisberger and Bonnie MacBird and produced by Walt Disney Productions. The film stars Jeff Bridges as a computer programmer who is transported inside the software world of a mainframe computer where he interacts with programs in his attempt to escape.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8faa7d55c7",
  "kind": "yes/no",
  "text": "Claim: The film Vanessa Kirby played Joanna in is a British romantic comedy-drama film that stars an Irish actor and writer who recieved a Bachelor of Arts from The Abduction Club.\n\nPassages:\n\n[Domhnall Gleeson]\nDomhnall Gleeson ( ; born 12 May 1983) is an Irish actor and writer. He received a Bachelor of Arts in Media Arts from Dublin Institute of Technology.\n\n[Vanessa Kirby]\nShe starred as Estella in the BBC adaptation of \"Great Expectations\" in 2011, as Joanna in Richard Curtis' romantic comedy \"About Time\" in 2013, and currently portrays Princess Margaret in Peter Morgan's Netflix series \"The Crown\", for which she has been nominated for the British Academy Television Award for Best Supporting Actress.\n\n[About Time (2013 film)]\nAbout Time is a 2013 British romantic comedy-drama film about a young man with the special ability to time travel who tries to change his past in order to improve his future. The film was written and directed by Richard Curtis, and stars Domhnall Gleeson, Rachel McAdams and Bill Nighy.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q65b3e5b25d",
  "kind": "yes/no",
  "text": "Claim: A participant in the 2013 Big Ten Conference football season was led by Kevin Reece Wilson. He is the current offensive coordinator at the Indiana University.\n\nPassages:\n\n[Kevin Wilson (American football)]\nKevin Reece Wilson (born October 23, 1961) is an American football coach and former player who is the current offensive coordinator at Ohio State University.\n\n[2013 Big Ten Conference football season]\nThe conference began its season on Thursday, August 29, as Minnesota and Indiana began their 2013 season of NCAA Division I FBS (Football Bowl Subdivision) competition.\n\n[2013 Indiana Hoosiers football team]\nThe 2013 Indiana Hoosiers football team represented the Indiana University during the 2013 NCAA Division I FBS football season. The team was led by head coach Kevin Wilson, who was in his third season.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q792d3ba034",
  "kind": "yes/no",
  "text": "Post: @AaronBastani @char_gerada Congratulations to you both. A happy life together…..",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q010888992c",
  "kind": "yes/no",
  "text": "Claim: Tome Sizemore had a role in a movie that starred an actor and Sun Tzu. Richard Nord worked on this film. The second actor also starred in Down in the Delta.\n\nPassages:\n\n[Tom Sizemore]\nHe is known for his supporting roles in films such as \"Born on the Fourth of July\" (1989), \"Harley Davidson and the Marlboro Man\" (1991), \"Passenger 57\" (1992), \"True Romance\" (1993), \"Natural Born Killers\" (1994), \"Strange Days\" (1995), \"Heat\" (1995), \"Saving Private Ryan\" (1998), \"Red Planet\" (2000), \"Black Hawk Down\" (2001), \"Pearl Harbor\" (2001), and for voicing Sonny Forelli in the video game \"\".\n\n[Down in the Delta]\nThe film stars Alfre Woodard, Al Freeman, Jr., Esther Rolle (in her final film appearance before her death), Loretta Devine, and Wesley Snipes.\n\n[Richard Nord]\nRichard Nord is a film editor who is best known for \"The Fugitive\" and \"Passenger 57\".\n\n[Passenger 57]\nThe film stars Wesley Snipes and Bruce Payne.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q8d4ac2d839",
  "kind": "yes/no",
  "text": "Text: My mouth while drunk….. unstoppable",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q67ef12d7a1",
  "kind": "yes/no",
  "text": "Claim: The movie that Scott Shepherd (actor) appeared in stars a Venona intelligence officer with the name Rudolf Abel.\n\nPassages:\n\n[Bridge of Spies (film)]\nSet during the Cold War, the film tells the story of lawyer James B. Donovan, who is entrusted with negotiating the release of Francis Gary Powers—a U.S. Air Force pilot whose U-2 spy plane was shot down over the Soviet Union in 1960—in exchange for Rudolf Abel, a convicted Soviet KGB spy held under the custody of the United States, whom he represented at trial.\n\n[Rudolf Abel]\nRudolf Ivanovich Abel (Russian: Рудольф Иванович Абель ), real name Vilyam \"Willie\" Genrikhovich Fisher (Вильям \"Вилли\" Генрихович Фишер), (July 11, 1903 – November 15, 1971) was a Soviet intelligence officer.\n\n[Scott Shepherd (actor)]\nScott Shepherd is an American film, theater, and television actor, best known for his appearances in the films \"Bridge of Spies\", \"Side Effects\" and \"Jason Bourne\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q0708bc1b47",
  "kind": "yes/no",
  "text": "Claim: San Francisco National Cemetery that George W. Wallace is buried at, is located at a park that is part of Golden Gate National Recreation Area.\n\nPassages:\n\n[San Francisco National Cemetery]\nSan Francisco National Cemetery is an United States national cemetery, located in the Presidio of San Francisco, California.\n\n[George W. Wallace]\nHe is buried at San Francisco National Cemetery.\n\n[Presidio of San Francisco]\nThe Presidio of San Francisco (originally, El Presidio Real de San Francisco or The Royal Fortress of Saint Francis) is a park and former U.S. Army military fort on the northern tip of the San Francisco Peninsula in San Francisco, California, and is part of the Golden Gate National Recreation Area.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6450400c46",
  "kind": "yes/no",
  "text": "Post: The best possible Saturday night is going out for dinner and drinks, having a couple too many, and being home for Match of the Day, happy weekend everyone",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q211110ab31",
  "kind": "yes/no",
  "text": "Claim: This island is known for Breacachadh which is also known as Breachacha Castle. It is also home to Dùn Dubh.\n\nPassages:\n\n[Breachacha Castle]\nBreachacha Castle (also spelled Breacachadh) is either of two structures on the shore of Loch Breachacha, on the Inner Hebridean island of Coll, Scotland.\n\n[Coll]\nColl is known for its sandy beaches, which rise to form large sand dunes, for its corncrakes, and for Breacachadh Castle.\n\n[Dùn Dubh]\nDùn Dubh is a hillfort, located on the Inner Hebridean island of Coll.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q553df92839",
  "kind": "yes/no",
  "text": "Claim: The namesake of a small island in the Town of New York was born in 1599.\n\nPassages:\n\n[Lion Gardiner]\nLion Gardiner (1599–1663), an early English settler and soldier in the New World, founded the first English settlement in what became the state of New York on Long Island. His legacy includes Gardiners Island, which is held by his descendants.\n\n[Gardiners Island]\nGardiner's Island is a small island in the Town of East Hampton, New York, in Eastern Suffolk County.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb7bd4d81f2",
  "kind": "yes/no",
  "text": "Claim: The American known as \"the Caruso of Rock\", had hits such as \"Pretty One,\" and \"Uptown\". He recorded \"I Drove All Night\" the year before his death. He recorded on the Monument Records label.\n\nPassages:\n\n[Roy Orbison]\nRoy Kelton Orbison (April 23, 1936 – December 6, 1988) was an American singer-songwriter known for his distinctive, impassioned voice, complex song structures, and dark emotional ballads.\n\n[I Drove All Night]\nThe song was originally intended for Roy Orbison, who recorded it in 1987, the year before his death, but his rendition was not released until 1992, after Lauper's version of it had become a top 10 hit on both sides of the Atlantic in 1989.\n\n[Early Orbison]\nEarly Orbison is an album recorded by Roy Orbison on the Monument Records label at their studios in Hendersonville, Tennessee and released in 1964. Essentially a compilation of songs from his first two Monument albums, it is most noteworthy for containing \"Pretty One\", the \"B\" side of Orbison's second Monument single, \"Uptown\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q4dbc9c9f25",
  "kind": "yes/no",
  "text": "Claim: The auditorium where Backstreet Boys: Larger Than Life residency show perfomed at is located in the Planet Hollywood Resort & Casino in Las Vegas, Nevada. This auditorium is located at a hotel and casino owned by Caesars Entertainment Corporation.\n\nPassages:\n\n[The AXIS]\nThe AXIS (known as The AXIS powered by Monster for sponsorship purposes, also referred to as the AXIS Theater) is a mid-sized auditorium located at Planet Hollywood Las Vegas on the Las Vegas Strip.\n\n[Backstreet Boys: Larger Than Life]\nBackstreet Boys: Larger Than Life is the first residency show by American vocal group Backstreet Boys, performed at The AXIS auditorium located in the Planet Hollywood Resort & Casino in Las Vegas, Nevada.\n\n[Planet Hollywood Las Vegas]\nIt is owned and operated by Caesars Entertainment Corporation.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3b8dfcc407",
  "kind": "yes/no",
  "text": "Claim: Marine Air Control Squadron 24 falls under the command of the 4th Marine Aircraft Wing and the group that is stationed at Naval Station Great Lakes which is located at Springflield in Lake County, Illinois.\n\nPassages:\n\n[Marine Air Control Group 48]\nMarine Air Control Group 48 (MACG-48) is a United States Marine Corps aviation command and control unit based at Naval Station Great Lakes that is currently composed of 4 squadrons that provide the 4th Marine Aircraft Wing and Marine Forces Reserve with a tactical headquarters, positive and procedural control of aircraft, air defense and aviation command and control.\n\n[Marine Air Control Squadron 24]\nThey fall under the command of Marine Air Control Group 48 and the 4th Marine Aircraft Wing.\n\n[Naval Station Great Lakes]\nNaval Station Great Lakes (NAVSTA Great Lakes) is the home of the United States Navy's only boot camp, located near North Chicago, in Lake County, Illinois.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qef7b829178",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "love waking up in a panic 🥴🥴",
   "I do not like waking up in a panic"
  ]
 },
 {
  "qid": "qec2cdae41b",
  "kind": "yes/no",
  "text": "Claim: The author of The Lost World (Crichton novel) is not an actor. McG is also not an actor.\n\nPassages:\n\n[The Lost World (Crichton novel)]\nThe Lost World is a techno thriller novel written by Michael Crichton and published in 1995 by Knopf.\n\n[McG]\nJoseph McGinty Nichol (born August 9, 1968), known mononymously as McG, is an American director, producer, and former record producer.\n\n[Michael Crichton]\nJohn Michael Crichton ( ; October 23, 1942 – November 4, 2008) was an American best-selling author, screenwriter, film director and producer best known for his work in the science fiction, medical fiction and thriller genres.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q582b22f86b",
  "kind": "yes/no",
  "text": "Text: Vaccinated this morning. Not sure it's worked - still committed to Apple and no extra autism detected. Bloody science.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q02cd30f064",
  "kind": "yes/no",
  "text": "Claim: Grand Forks International Airport is closer to the settlement it is near, than the airport close by to The Texas Air & Space Museum.\n\nPassages:\n\n[Texas Air &amp; Space Museum]\nThe Texas Air & Space Museum is an aviation museum located near Rick Husband Amarillo International Airport in Amarillo, Texas.\n\n[Grand Forks International Airport]\nGrand Forks International Airport (IATA: GFK, ICAO: KGFK, FAA LID: GFK) is a public airport five miles (8 km) northwest of Grand Forks, in Grand Forks County, North Dakota.\n\n[Rick Husband Amarillo International Airport]\nRick Husband Amarillo International Airport (IATA: AMA, ICAO: KAMA, FAA LID: AMA) is a public airport six miles (10 km) east of downtown Amarillo, in Potter and Randall Counties, Texas, United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qcf0a048a54",
  "kind": "yes/no",
  "text": "Claim: John Constantine is the fictional antihero from comic books published by DC Comics, who sometimes acts as a cab driver, and was created by Don Simpson, Steve Bissette, and John Totleben.\n\nPassages:\n\n[Chas Chandler (comics)]\nChas is John Constantine's closest and longest surviving friend, who acts as his sidekick and cab driver.\n\n[John Constantine]\nJohn Constantine ( ) is a fictional antihero, appearing in comic books published by DC Comics and its alternative imprint Vertigo. 2 No. 25 (June 1984), and was created by Alan Moore, Steve Bissette and John Totleben.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf1ed262a50",
  "kind": "yes/no",
  "text": "Text: justin bieber is and always has been so hot sue me I’ll never stop being a belieber",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q7bdf028e50",
  "kind": "yes/no",
  "text": "Claim: The address of the building on U.S. Route 3 that was the tallest building in New Hampshire when completed in 1972 was 1000 Elm Street.\n\nPassages:\n\n[City Hall Plaza (Manchester)]\nCity Hall Plaza, City Hall Plaza Tower or 900 Elm Street (U.S. Route 3), is a prominent 275 ft office tower in Manchester, New Hampshire.\n\n[Brady Sullivan Plaza]\nBrady Sullivan Plaza, formerly known as the Hampshire Plaza, is a 259 ft , 20-story high-rise located at 1000 Elm Street, Manchester, New Hampshire. For 20 years, from its completion in 1972 until the completion of the 275 ft One City Hall Plaza at 900 Elm Street in 1992, it was the tallest building in the U.S. state of New Hampshire and in northern New England.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q003bf6383e",
  "kind": "yes/no",
  "text": "Post: shut the hell up https://t.co/QeOnvsraNM",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q09cf95d33c",
  "kind": "yes/no",
  "text": "Claim: The prominent role that this actor played in HBO Mini series Band of Brothers was Donald Malarkey. This same actor also voiced the son of Stan in the episode I Am the Walrus (American Dad!).\n\nPassages:\n\n[I Am the Walrus (American Dad!)]\nIt mainly centers around Stan and his son Steve, who are both competing for the dominant role of the house.\n\n[Steve Smith (American Dad!)]\n\", voiced by Scott Grimes.\n\n[Donald Malarkey]\nMalarkey was portrayed in the HBO miniseries \"Band of Brothers\" by Scott Grimes.\n\n[Scott Grimes]\nSome of his most prominent roles include appearances in \"ER\" as Dr. Archie Morris, \"Party of Five\" as Will McCorkle, \"Band of Brothers\" as Technical Sergeant Donald Malarkey, and the animated sitcom \"American Dad!",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9448442589",
  "kind": "yes/no",
  "text": "Claim: The name of the 40th president who was in office when the Job Partnership Act of 1982 was passed is Ronald Reagan.\n\nPassages:\n\n[Job Training Partnership Act of 1982]\nThe Job Training Partnership Act of 1982 (Pub.L. 97–300 , , et seq.) was a United States federal law passed October 13, 1982, by the United States Department of Labor during the Ronald Reagan administration.\n\n[Ronald Reagan]\nRonald Wilson Reagan ( ; February 6, 1911 – June 5, 2004) was an American statesman and actor who served as the 40th President of the United States from 1981 to 1989.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q1414370d59",
  "kind": "yes/no",
  "text": "Claim: \"Licence Revoked\" was the original title during production of a war film that has the actor from Maniac Cop 2. The actor stars as villain Franz Sanchez in \"Licence Revoked\".\n\nPassages:\n\n[Licence to Kill]\nOriginally titled \"Licence Revoked\" in line with the plot, the name was changed during post-production due to test audiences associating the term with driving.\n\n[Robert Davi]\nAmong his most recognized roles are opera-singing heavy Jake Fratelli in \"The Goonies\" (1985), Vietnam veteran and FBI Special Agent Big Johnson in \"Die Hard\" (1988), Bond villain Franz Sanchez in \"Licence to Kill\" (1989), police deputy chief Phil Heinemann in \"Predator 2\" (1990), strip club manager Al Torres in \"Showgirls\" (1995) and Albanian mob boss Goran Vata in \"The Expendables 3\" (2014).\n\n[Maniac Cop 2]\nit stars Robert Davi, Claudia Christian, Michael Lerner, and Bruce Campbell.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qcec1677e97",
  "kind": "yes/no",
  "text": "Claim: Christelyn Karazin is an American writer, columnist, and blogger on the subject of interracial dating, particularly black women dating outside their race. She has written for Jet, an American weekly digital magazine, marketed toward African-American readers, that was founded in the fall of 1951 by John H. Johnson of the Johnson Publishing Company in Chicago, Illinois.\n\nPassages:\n\n[Christelyn Karazin]\nShe hosts the blog \"Beyond Black & White\" and has written for \"Woman's Day\", \"Ebony\", \"Jet\", and Reuters.\n\n[Jet (magazine)]\nJet is a digital magazine.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q12c4551d69",
  "kind": "yes/no",
  "text": "Claim: MGM Resorts International was the company that started the urban complex development that included the highrise building, The Harmon.\n\nPassages:\n\n[The Harmon]\nThe Harmon was a highrise building at the CityCenter development in Paradise, Nevada.\n\n[CityCenter]\nThe project was started by MGM Resorts International; Dubai World became a joint partner during the project's construction phase.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q14ac835c7c",
  "kind": "yes/no",
  "text": "Claim: Jaap J. Vermeulen specializes in this genus of flowering plant. It has more species than the flower Bismarckia which are suspectible to Rhynchophorus cruentatus. Rhynchophorus cruentatus is also called a palmetto weevil.\n\nPassages:\n\n[Bulbophyllum]\nBulbophyllum is the largest genus in the orchid family Orchidaceae. With more than 2,000 species, it is also one of the largest genera of flowering plants, exceeded only by \"Astragalus\".\n\n[Jaap J. Vermeulen]\nJaap J. Vermeulen (born 1955) is a Dutch Botanist, specializing in the Orchidaceae Genus Bulbophyllum\n\n[Rhynchophorus cruentatus]\nIts main target is the Canary Island date palm, but date palms (a different species than the Canary Island date palm), sabal palms (the palmetto weevil's traditional target), saw palmetto (the palmetto weevil's traditional alternative target), \"Washingtonia\", \"Pritchardia\", royal palms, \"Latania\", coconut palms, \"Caryota\", and \"Bismarckia\" are also susceptible.\n\n[Bismarckia]\nThe genus is named for the first chancellor of the German Empire Otto von Bismarck and the epithet for its only species, Bismarckia nobilis, comes from Latin for 'noble'.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q78d27e0ad8",
  "kind": "yes/no",
  "text": "Claim: Romans stars the Tamil and Telugu actress Nivetha Thomas.\n\nPassages:\n\n[Niveda Thomas]\nNivetha Thomas is an Indian film actress known for her natural acting style. She has acted in various Tamil, Malayalam, and Telugu films.\n\n[Romans (2013 film)]\nThe film stars Kunchacko Boban, Biju Menon and Niveda Thomas in the lead roles, along with Lalu Alex, T. G. Ravi, Nelson Sooranad, Kalabhavan Shaju, Kochu Preman, and Vijayaraghavan in supporting roles.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8fc1016743",
  "kind": "yes/no",
  "text": "Claim: Leo Varadkar beat Irish Fine Gael politician Simon Coveney on June 2, 2017, 60% to 40%.\n\nPassages:\n\n[Simon Coveney]\nSimon Anthony Coveney (born 16 June 1972) is an Irish Fine Gael politician who has served as Minister for Foreign Affairs and Trade and Deputy Leader of Fine Gael since June 2017.\n\n[Fine Gael leadership election, 2017]\nThe 2017 Fine Gael leadership election was triggered in May 2017, when Enda Kenny resigned as party leader. On 2 June Leo Varadkar was announced as the victor, beating rival Simon Coveney 60% to 40%.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfec2560d61",
  "kind": "yes/no",
  "text": "Claim: Ana Beatriz Barros is a Brizilian actress and model known for appearances with an American designer of women's premium lingerie, the largest American retailer of women's lingerie, wholloy owned by L Brands.\n\nPassages:\n\n[Victoria's Secret]\nVictoria's Secret is an American designer, manufacturer, and marketer of women's premium lingerie, womenswear, and beauty products. Victoria's Secret is wholly owned by L Brands, a publicly traded company.\n\n[Ana Beatriz Barros]\nAna Beatriz Barros (born 29 May 1982) is a Brazilian model known for her multiple appearances in the \"Sports Illustrated Swimsuit Issue\" and for her work with Intimissimi, Guess? , bebe, Victoria's Secret, Chanel cosmetics, and Jennifer Lopez's JLO fashion line.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc13d5ba09e",
  "kind": "yes/no",
  "text": "Claim: Cotton Mather was known for his promotion of inoculation for disease prevention and owned the slave Onesimus.\n\nPassages:\n\n[Onesimus (Boston slave)]\nOnesimus (late 1600s–1700s) was an African-born man held as a slave by Puritan minister Cotton Mather, who helped mitigate the impact of a smallpox outbreak in Boston by introducing Mather to the principle of inoculation.\n\n[Cotton Mather]\nHe left a scientific legacy due to his hybridization experiments and his promotion of inoculation for disease prevention, though he is most frequently remembered today for his vigorous support for the Salem witch trials.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 }
]
