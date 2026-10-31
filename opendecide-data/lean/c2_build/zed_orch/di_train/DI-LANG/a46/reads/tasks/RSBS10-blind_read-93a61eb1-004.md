# A46 replay label-noise blind read RSBS10-blind_read-93a61eb1-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS10-blind_read-93a61eb1-004.json

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
  "qid": "q7a3bd1d70b",
  "kind": "yes/no",
  "text": "Claim: Simulink was developed by an American privately held corporation specializing in mathematical computing software. That privately held corporation supports a Professor of Mathematics at the university Massachusetts Institute of Technology.\n\nPassages:\n\n[Simulink]\nSimulink, developed by MathWorks, is a graphical programming environment for modeling, simulating and analyzing multidomain dynamic systems.\n\n[Gilbert Strang]\nStrang is the MathWorks Professor of Mathematics at the Massachusetts Institute of Technology.\n\n[MathWorks]\nThe MathWorks, Inc. (branded as simply MathWorks) is an American privately held corporation that specializes in mathematical computing software.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qad3ebe3cf8",
  "kind": "yes/no",
  "text": "Claim: The player involved in the Helmet Catch with David Tyree was the first overall pick in the NFL draft and had the Manning Field named after him.\n\nPassages:\n\n[Helmet Catch]\nThe Helmet Catch was an American football play involving New York Giants quarterback Eli Manning and wide receiver David Tyree in the final two minutes of Super Bowl XLII on February 3, 2008.\n\n[Eli Manning]\nElisha Nelson Manning (born January 3, 1981) is an American football quarterback for the New York Giants of the National Football League (NFL). He was drafted as the first overall pick in the 2004 NFL Draft by the San Diego Chargers and was immediately traded to the Giants who in return gave up a package, highlighted by fourth overall selection Philip Rivers.\n\n[Manning Field at John L. Guidry Stadium]\nThe playing surface is named Manning Field after the Manning family because Peyton Manning, Eli Manning and Archie Manning hold the Manning Passing Academy football camp at the facility.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q11d8720c09",
  "kind": "yes/no",
  "text": "Claim: The composer of Lux Aurunque born in the year 1970.\n\nPassages:\n\n[Lux Aurumque]\nLux Aurumque (\"Light and Gold\", sometimes \"Light of Gold\") is a choral composition in one movement by Eric Whitacre.\n\n[Eric Whitacre]\nEric Edward Whitacre (born January2, 1970) is a Grammy-winning American composer, conductor, and speaker, known for his choral, orchestral and wind ensemble music.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3aa8c1764f",
  "kind": "yes/no",
  "text": "Claim: The 1955 Florida Gators football team beat this non-professional team with a score of 20–14. The head coach of that team left after the 1955 college football season. He was born on July 6, 1924.\n\nPassages:\n\n[Darrell Royal]\nDarrell K Royal (July 6, 1924 – November 7, 2012) was an American football player and coach.\n\n[1955 Mississippi State Maroons football team]\nThe 1955 Mississippi State Maroons football team represented Mississippi State College during the 1955 college football season. After the season, head coach Darrell Royal left to take the job at Washington.\n\n[1955 Florida Gators football team]\nThe highlights of the 1955 season included three conference victories over the Mississippi State Maroons (20–14), LSU Tigers (18–14) and Georgia Bulldogs (19–13).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q41b15ea15c",
  "kind": "yes/no",
  "text": "Claim: The Pittsburgh Penguins lost to the New York Islanders by 3 to 1 in the opening round to the eventual Stanley Cup.\n\nPassages:\n\n[1981–82 New York Islanders season]\nThe 1981-82 New York Islanders season was the tenth season in the franchise's history. It involved winning the Stanley Cup.\n\n[1981–82 Pittsburgh Penguins season]\nThe 1981–82 Pittsburgh Penguins season was their 15th in the National Hockey League. The qualified for the playoffs for the fourth straight year, but lost in the opening round to the eventual Stanley Cup champion New York Islanders three games to two.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4d4c57c465",
  "kind": "yes/no",
  "text": "Claim: New Faces of 1952 is a musical revue with songs and comedy skits, that helped jump start the career of the young performer, and American actress and film producer Carol Lawrence.\n\nPassages:\n\n[Carol Lawrence]\nCarol Lawrence (born September 5, 1932) is an American actress, most often associated with musical theatre, but who has also appeared extensively on television.\n\n[New Faces of 1952]\nIt helped jump start the careers of several young performers including Paul Lynde, Alice Ghostley, Eartha Kitt, Robert Clary, Carol Lawrence, Ronny Graham, performer/writer Mel Brooks (as Melvin Brooks), and lyricist Sheldon Harnick.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5924ac1975",
  "kind": "yes/no",
  "text": "Claim: The band american composer Steve Goulding is the drummer for is not British. The singer whose debut album is Don't Let It Go to Waste isn't British either.\n\nPassages:\n\n[Don't Let It Go to Waste]\nDon't Let It Go to Waste is the debut album from Matt Willis, released on 20 November 2006.\n\n[The Mekons]\nThe Mekons are a British-American rock band.\n\n[Steve Goulding]\nSteve Goulding (born 1954, South London, England) is an English drummer, who has played as a member of Graham Parker and The Rumour, The Associates, Poi Dog Pondering, The Waco Brothers and The Mekons.\n\n[Matt Willis]\nMathew James \"Matt\" Willis (born 8 May 1983), also previously known as Mattie Jay, is an English singer-songwriter, television presenter and actor, best known as the bassist and one of the vocalists of the pop punk band, Busted.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb317240a34",
  "kind": "yes/no",
  "text": "Claim: Live While We're Young is by the English-Irish boy band Westlife who relocated to London.\n\nPassages:\n\n[Live While We're Young]\n\"Live While We're Young\" is a song by English-Irish boy band One Direction, released as the lead single from their second studio album, \"Take Me Home\" (2012).\n\n[One Direction]\nOne Direction (commonly abbreviated as 1D) are an English-Irish pop boy band based in London, composed of Niall Horan, Liam Payne, Harry Styles, Louis Tomlinson, and previously, Zayn Malik until his departure from the band on 25 March 2015.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe6bbc412a9",
  "kind": "yes/no",
  "text": "Claim: The genera Gordonia and Osbeckia are not in the same family.\n\nPassages:\n\n[Gordonia (plant)]\nGordonia is a genus of flowering plants in the family Theaceae, related to \"Franklinia\", \"Camellia\" and \"Stewartia\".\n\n[Osbeckia]\nOsbeckia is a genus of plants in the family Melastomataceae.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q70a63d1e0e",
  "kind": "yes/no",
  "text": "Claim: This non-fiction author wrote Chilly Scenes of Winter. The author and Edgar Rice Burroughs are not dating.\n\nPassages:\n\n[Chilly Scenes of Winter]\nChilly Scenes of Winter is Ann Beattie's first novel, published by Doubleday in September, 1976.\n\n[Edgar Rice Burroughs]\nEdgar Rice Burroughs (September 1, 1875 – March 19, 1950) was an American fiction writer best known for his celebrated and prolific output in the adventure and science-fiction genres.\n\n[Ann Beattie]\nAnn Beattie (born September 8, 1947) is an American novelist and short story writer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd3af0fbfdf",
  "kind": "yes/no",
  "text": "Claim: The event, for which Legacy (Eminem) became one of the official theme songs, took place at the home venue of the National Football League team Commonwealth Games.\n\nPassages:\n\n[Legacy (Eminem song)]\n\"Legacy\" became one of the official theme songs of WrestleMania XXX.\n\n[Mercedes-Benz Superdome]\nIt primarily serves as the home venue for the New Orleans Saints of the National Football League (NFL), and is also the home stadium for the Sugar Bowl and New Orleans Bowl in college football.\n\n[WrestleMania XXX]\nIt took place on April 6, 2014, at the Mercedes-Benz Superdome in New Orleans, Louisiana.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q1d70be5347",
  "kind": "yes/no",
  "text": "Claim: Alfred A. Marcus worked as a consultant for the utility holding company Xcel Energy Inc.\n\nPassages:\n\n[Alfred A. Marcus]\nHe has worked as a consultant with companies such as 3M, Corning Inc., Xcel Energy, Medtronic, General Mills, and IBM and has also taught as a visiting professor at Technion, INCAE, BI Norwegian Business School, and MIT.\n\n[Xcel Energy]\nXcel Energy Inc. is a utility holding company based in Minneapolis, Minnesota, serving more than 3.3 million electric customers and 1.8 million natural gas customers in Minnesota, Michigan, Wisconsin, North Dakota, South Dakota, Colorado, Texas and New Mexico.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6fe854cf1f",
  "kind": "yes/no",
  "text": "Claim: The manager of the 2000 country music group inspired by boy bands was convicted in 2008.\n\nPassages:\n\n[Marshall Dyllon]\nMarshall Dyllon was an American country music group formed in 2000, comprising vocalists Daniel Cahoon, Jesse Littleton, Michael Martin, Paul Martin, and Todd Michael Sansom. These five members were recruited by country music artist Kenny Rogers and talent manager Lou Pearlman, in an attempt to bring the boy band sound to the country music scene.\n\n[Lou Pearlman]\nIn 2008, Pearlman was convicted and sentenced to up to 25 years in prison.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfc400eb60d",
  "kind": "yes/no",
  "text": "Text: It's my 24th birthday and I'm watching adventure time. Wearing a marvels hoodie. #whatislife #wahhh24isold",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qc523d4d3b4",
  "kind": "yes/no",
  "text": "Text: Watched 127 hours... Kinda reminded me of this one time I got a bad splinter. Writing a book about it now, hit me up for an autographed copy",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qcc5489c6ab",
  "kind": "yes/no",
  "text": "Text: At least I'm used to this side effect from my infusion, and I'm very grateful that I'm not experiencing any of that full body pain I had after my last infusion. The IV steroids must be working!! And tomorrow is day one of a steroid pack",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qe414e60e1b",
  "kind": "yes/no",
  "text": "Tweet: i was so bored today that i let my computer restart to install updates 🥴",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qba06a35f62",
  "kind": "yes/no",
  "text": "Claim: Ballet Dancer Gregory Hines died on August 9, 2003. He appeared in the movie that featured the song Separate Lives.\n\nPassages:\n\n[Separate Lives]\n\"Separate Lives\" is a 1985 song recorded by Phil Collins and Marilyn Martin and featured on the soundtrack to the motion picture \"White Nights\".\n\n[White Nights (1985 film)]\nWhite Nights is a 1985 American drama film directed by Taylor Hackford and choreographed by Twyla Tharp and stars Mikhail Baryshnikov, Gregory Hines, Jerzy Skolimowski, Helen Mirren and Isabella Rossellini.\n\n[Gregory Hines]\nGregory Oliver Hines (February 14, 1946 – August 9, 2003) was an American dancer, actor, singer, and choreographer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb2cc7babe9",
  "kind": "yes/no",
  "text": "Claim: On October 1st a Canadian politician born January 2, 1979, succeeded as leader of this political party in the country that was the birthplace of John Sharples, Jr. This is the same party that the Ontario New Democratic Youth is affiliated.\n\nPassages:\n\n[New Democratic Party]\nHe was suceeded as leader by Jagmeet Singh, who won the 2017 leadership election on October 1st, with 53.8% of the vote.\n\n[Ontario New Democratic Youth]\nThe Ontario New Democratic Youth (ONDY) is the youth wing of the Ontario New Democratic Party which is in turn affiliated with the federal New Democratic Party.\n\n[John Sharples, Jr.]\nJohn Sharples (24 January 1847 – 30 July 1913) was a Canadian business person and politician.\n\n[Jagmeet Singh]\nJagmeet Singh Jimmy Dhaliwal {'1': \", '2': \", '3': \", '4': \"} (born January 2, 1979), known professionally as Jagmeet Singh ( ), is a Canadian politician who is leader of the New Democratic Party.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qd2fd137b66",
  "kind": "yes/no",
  "text": "Claim: The breed the American Water Spaniel was derived from was bred before the Estonian Hound.\n\nPassages:\n\n[Estonian Hound]\nIt was bred in 1947 when the Soviet Union's national economy ministry decided that every country in the Union must have its own dog breed.\n\n[American Water Spaniel]\nThe breed was saved by Dr. Fred J. Pfeifer, who set up the breed club and standard, and whose work led to recognition for the breed by the United Kennel Club, and later, the American Kennel Club.\n\n[English Water Spaniel]\nThe English Water Spaniel is a breed of dog that has been extinct since the first part of the 20th century, with the last specimen seen in the 1930s.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1b1f80c8fe",
  "kind": "yes/no",
  "text": "Claim: The Royal Exchange Theatre and Buzzcocks are included in the complex where the play Punk Rock was premiered.\n\nPassages:\n\n[Punk Rock (play)]\nPunk Rock is a play by the British playwright Simon Stephens which premiered at the Royal Exchange in 2009 and transferred to the Lyric Hammersmith directed by Sarah Frankcom.\n\n[Royal Exchange, Manchester]\nThe Royal Exchange is a grade II listed building in Manchester, England. The complex includes the Royal Exchange Theatre and the Royal Exchange Shopping Centre.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q91cbbd98b5",
  "kind": "yes/no",
  "text": "Claim: Southwest Airlines Flight 2294 (SWA 2294, WN 2294) was a scheduled US passenger aircraft flight which made an emergency landing due to a fire . The airport where the flight landed and and Albert J. Ellis Airport are located in the same country.\n\nPassages:\n\n[Yeager Airport]\nYeager Airport (IATA: CRW, ICAO: KCRW, FAA LID: CRW) is a public airport three miles (6 km) east of downtown Charleston, in Kanawha County, West Virginia, United States.\n\n[Albert J. Ellis Airport]\nAlbert J. Ellis Airport (IATA: OAJ, ICAO: KOAJ, FAA LID: OAJ) is a county-owned public-use airport in Onslow County, North Carolina, United States.\n\n[Southwest Airlines Flight 2294]\nSouthwest Airlines Flight 2294 (SWA 2294, WN 2294) was a scheduled US passenger aircraft flight which made an emergency landing at Yeager Airport (CRW) in Charleston, West Virginia, on July 13, 2009, after suffering a rapid depressurization of the passenger cabin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q14f0001d51",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I would probably word it as a question: Do you think that using Go Fund Me to ask for money to pay bills is a form of socialism?",
   "Are GoFundMe accounts a form of socialism? I don’t have enough money to pay my bills, so let me create an account an ask for money to help pay my bills. ??"
  ]
 },
 {
  "qid": "q5bb520f983",
  "kind": "yes/no",
  "text": "Claim: The Darjeeling Limited is an American adventure comedy-drama film, released in 2007, directed by Bill Murray, the film stars include Bill Murray in a cameo role.\n\nPassages:\n\n[The Darjeeling Limited]\nThe Darjeeling Limited is a 2007 American adventure comedy-drama film directed by Wes Anderson which he co-produced with Scott Rudin, Roman Coppola and Lydia Dean Pilcher and co-wrote with Coppola and Jason Schwartzman.\n\n[Bill Murray]\nWilliam James Murray (born September 21, 1950) is an American actor, comedian, and writer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qbf939bcc02",
  "kind": "yes/no",
  "text": "Claim: A mountain near Tomichi Dome was named in honor of an explorer born in the 1800s.\n\nPassages:\n\n[John Williams Gunnison]\nJohn Williams Gunnison (November 11, 1812 – October 26, 1853) was an American military officer and explorer.\n\n[Mount Gunnison]\nThe mountain is named in honor of John Williams Gunnison who explored the area.\n\n[Tomichi Dome]\nOther laccoliths of the Gunnison Country are Mount Crested Butte, Gothic Mountain, Whetstone Mountain, Mount Axtel, Anthracite Range, Round Mountain, Carbon Peak, Beckwith Mountain, Marcellina Mountain and Mount Gunnison.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q853d3f9459",
  "kind": "yes/no",
  "text": "Claim: Cindy Williams is an award-winning news anchor for a tv station whose transmitter is located on Winn Mountain.\n\nPassages:\n\n[Cindy Williams (journalist)]\nCindy Williams (born 1963) is an award-winning news anchor with WCSH 6 in Portland, Maine.\n\n[WCSH]\nLicensed to Portland, it broadcasts a high definition digital signal on UHF channel 44 (or virtual channel 6 via PSIP) from a transmitter on Winn Mountain in Sebago.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf66b9056ad",
  "kind": "yes/no",
  "text": "Post: Wish I was the bitch that Elijah hewson fucking hated, sad :(",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q00e35635ec",
  "kind": "yes/no",
  "text": "Claim: Aloinopsis is a floral plant. The close relative of another genus is also a plant. Aruncus dioicus is a species in this genus.\n\nPassages:\n\n[Aloinopsis]\nAloinopsis is a genus of ice plants from South Africa.\n\n[Aruncus]\nThey are closely related to the genera \"Filipendula\" and \"Spiraea\", and are native to mountainous damp woodland in temperate regions of the Northern Hemisphere.\n\n[Filipendula]\nFilipendula is a genus of 12 species of perennial herbaceous flowering plants in the family Rosaceae, native to the temperate regions of the Northern Hemisphere.\n\n[Aruncus dioicus]\n(known as goat's beard, buck's-beard or bride's feathers) is a flowering herbaceous perennial plant in the family Rosaceae, and is the type species of the genus \"Aruncus\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4578c4becc",
  "kind": "yes/no",
  "text": "Post: there was a bee in my house yesterday and i haven’t seen it since i hope it died",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qc839d8d4c8",
  "kind": "yes/no",
  "text": "Claim: Isabella (Belle) Baumfree was the birth name of the ex-slave abolitionist featured in the sculpture that also memorialized Barbe de Verrue.\n\nPassages:\n\n[Barbe de Verrue]\nShe is memorialized as a figure in \"The Dinner Party\" by Judy Chicago.\n\n[Sojourner Truth]\nSojourner Truth ( ; born Isabella (Belle) Baumfree; 1797 – November 26, 1883) was an African-American abolitionist and women's rights activist.\n\n[The Dinner Party]\nSacajawea, Sojourner Truth, Eleanor of Aquitaine, Empress Theodora of Byzantium, Virginia Woolf, Susan B. Anthony, and Georgia O'Keeffe are among the guests.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q31835699c4",
  "kind": "yes/no",
  "text": "Claim: The director of Border Street was born 3 years before the writer of \"Crane World\". The writer of \"Crane World\" is also the director.\n\nPassages:\n\n[Aleksander Ford]\nAleksander Ford (born Mosze Lifszyc; 24 November 1908 in Kiev, Russian Empire – 4 April 1980 in Naples, Florida, United States) was a Polish Jewish film director; and head of the Polish People's Army Film Crew in the Soviet Union during World War II.\n\n[Border Street]\nBorder Street (Polish:Ulica Graniczna) is a 1948 Polish drama film directed by Aleksander Ford and starring Mieczysława Ćwiklińska, Jerzy Leszczyński and Władysław Godik.\n\n[Crane World]\nCrane World (Spanish: Mundo grúa ) is an 1999 Argentine film, written and directed by Pablo Trapero.\n\n[Pablo Trapero]\nPablo Trapero (Born 4 October 1971) is an Argentine film producer, editor and director.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8ec2fd9638",
  "kind": "yes/no",
  "text": "Claim: The Hills Tavern, renamed the Century Inn, was built between 1811 and 1837 and fell down 10 year after the renaming.\n\nPassages:\n\n[Hill's Tavern]\nFor a period in the early 1900s, the inn was known as Central Hotel. Now called the Century Inn, it had been the oldest tavern in continuous use on the National Road, until the fire brought an end to its 221 years of continuous operation.\n\n[National Road]\nBuilt between 1811 and 1837, the 620 mi road connected the Potomac and Ohio Rivers and was a main transport path to the West for thousands of settlers.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8148fdc132",
  "kind": "yes/no",
  "text": "Claim: A board member of the Nantucket Film Festival holds the current state party chair in a political party. This political party D. Bruce Poole was the former Chairman of.\n\nPassages:\n\n[Kathleen Matthews]\nShe is the current chair for the Maryland Democratic Party.\n\n[Maryland Democratic Party]\nThe current state party chair is Kathleen Matthews.\n\n[Nantucket Film Festival]\nBoard members include Donick Cary, Nancy Dubac, Chris Matthews, Kathleen Matthews, Ben Stiller, and Tom Scott.\n\n[Bruce Poole]\nD. Bruce Poole is the former Chairman of the Maryland Democratic Party.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q9f94e17eef",
  "kind": "yes/no",
  "text": "Claim: Lou Cutell appeared on the third episode of the ninth season of an CBS sitcom that was the 187th episode overall.\n\nPassages:\n\n[Lou Cutell]\nLou Cutell (born October 6, 1930) is an American movie and television actor. In 2013, he appeared on the \"How I Met Your Mother\" episode \"Last Time in New York\".\n\n[Last Time in New York]\n\"Last Time in New York\" is the third episode of the ninth season of the CBS sitcom \"How I Met Your Mother\", and the 187th episode overall.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q72a775e7fd",
  "kind": "yes/no",
  "text": "Claim: Shenley Hall is a house at a parish 18.7 miles from central London.\n\nPassages:\n\n[Shenley Hall]\nShenley Hall is a Grade II listed country house at Shenley in Hertfordshire.\n\n[Shenley, Hertfordshire]\nThe village is located 18.7 miles from Central London.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qb6e95d225d",
  "kind": "yes/no",
  "text": "Claim: The proper name of the husband of Lollia Paullina was Gottlob Frege Augustus Germanicus.\n\nPassages:\n\n[Lollia Paulina]\nLollia Paulina, also known as Lollia Paullina (15-49) was a Roman Empress for six months in 38 as the third wife and consort of the Roman emperor Caligula.\n\n[Caligula]\nCaligula ( ), properly Gaius Julius Caesar Augustus Germanicus (31 August AD 12 – 24 January AD 41) was Roman emperor from AD 37–41.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q5eab5f7e17",
  "kind": "yes/no",
  "text": "Claim: The brand where Lauren Gold, who is most recognised as the DJ in Robbie Williams's \"Rock DJ\" music video as well as her recurring appearance in the company's ad campaigns, is currently owned by a fashion retailer based in Columbus, Ohio.\n\nPassages:\n\n[Lauren Gold]\nGold is most recognised as the DJ in Robbie Williams's \"Rock DJ\" music video as well as her recurring appearance in La Senza ad campaigns.\n\n[L Brands]\nL Brands Inc. (formerly known as \"Limited Brands Inc\" and \"The Limited Inc.\") is an American fashion retailer based in Columbus, Ohio.\n\n[La Senza]\nThe La Senza brand is currently owned by L Brands which operates and owns La Senza stores in Canada and uses a franchise model for the operation of stores outside Canada.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5d48236f07",
  "kind": "yes/no",
  "text": "Tweet: Avoid mass gatherings.. does this mean that I can stay home tomorrow as I work at a school? No I thought not. #schoolclosure",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qa8c8ac5c59",
  "kind": "yes/no",
  "text": "Tweet: wish i was good at singing :( it’s actually a bit embarassing",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qe2b66987d5",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "only have to physically be in uni for an hour a week looool mmmm take my 9k xxxxx",
   "9k is ridiculous for 1 hour of in person teaching a week."
  ]
 },
 {
  "qid": "qba24c05d9c",
  "kind": "yes/no",
  "text": "Claim: The Indianapolis 500 was designated a Grand Épreuve along with one of the oldest motor races in the world.\n\nPassages:\n\n[French Grand Prix]\nThe French Grand Prix (French: \"Grand Prix de France\" ), formerly known as the Grand Prix de l'ACF, is a race held as part of the Fédération Internationale de l'Automobile's annual Formula One automobile racing championships. It is one of the oldest motor races in the world.\n\n[1924 Grand Prix season]\nThe 1924 Grand Prix season again saw Grand Prix motor racing in Europe and North America. The Indianapolis 500 was again designated a Grand Épreuve by the International Sporting Commission of the AIACR, along with the French Grand Prix, held in Lyon and the Italian Grand Prix at Monza.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q9e2a164fee",
  "kind": "yes/no",
  "text": "Claim: The team produced the 2000 film The Sandman. They won an award before Alexandra Shiva.\n\nPassages:\n\n[Alexandra Shiva]\nAlexandra Elizabeth Shiva is an American film producer and director. \"Bombay Eunuch\" is her 2001 award-winning film, and in 2015 she showed \"How to Dance in Ohio\" at the Sundance Film Festival in the US Documentary Competition.\n\n[Brothers Quay]\nStephen and Timothy Quay ( ; born June 17, 1947) are American identical twin brothers better known as the Brothers Quay or Quay Brothers. They are also the recipients of the 1998 Drama Desk Award for Outstanding Set Design for their work on the play \"The Chairs\".\n\n[The Sandman (2000 film)]\nThe Sandman is a 2000 dance film made by the Brothers Quay and William Tuckett.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5d37fad4d2",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "\"I am happy for those who met him, but I wish I met Dream on hypixel\"",
   "also if u met dream on hypixel.. congrats ! im not jealous at all haha im totally normal haha Good For You .. haha"
  ]
 },
 {
  "qid": "q40f3a35e86",
  "kind": "yes/no",
  "text": "Tweet: This second jab has made me feel off the box this entire day 🤮",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q4cd187809d",
  "kind": "yes/no",
  "text": "Claim: A type of two-seat helicopter designed by a man that won the highest award at the 1912 Moscow Aviation Exhibition for the S-6-A airplane. This helicopter was in competition with the Pitcairn XO-61.\n\nPassages:\n\n[Igor Sikorsky]\nHis S-6-A received the highest award at the 1912 Moscow Aviation Exhibition.\n\n[Sikorsky R-4]\nThe Sikorsky R-4 was a two-seat helicopter designed by Igor Sikorsky with a single, three-bladed main rotor and powered by a radial engine.\n\n[Pitcairn XO-61]\nOne of the last autogyros produced, in competition with the Kellett YO-60 and the Sikorsky R-4, it fell victim to cooling problems with its rear-mounted engine and the coming of the helicopter with its ability to hover.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qadcb94442e",
  "kind": "yes/no",
  "text": "Post: .@taylorswift13 is 100% going to post another photo with 5 holes in a fence 5 days before Lover is released, isn’t she?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q79e62a4010",
  "kind": "yes/no",
  "text": "Claim: \"The Golden Jet\" was born in Point Anne, Ontario and so was Dennis Hull, as well as painter Manley MacDonald.\n\nPassages:\n\n[Point Anne, Ontario]\nPoint Anne is a ghost town on the Bay of Quinte near Belleville, Ontario, Canada. It was the birthplace of hockey greats Bobby Hull and Dennis Hull, as well as painter Manley MacDonald.\n\n[Bobby Hull]\nHis blonde hair, end to end rushes, incredible skating speed, and ability to shoot the puck at very high velocity all earned him the nickname \"The Golden Jet\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qad4211c5cc",
  "kind": "yes/no",
  "text": "Claim: The song, Suga Suga, is sampled in \"Sugar\", the 2015 pop rock album of the same name by Robin Schulz.\n\nPassages:\n\n[Sugar (Robin Schulz song)]\n\"Sugar\" is a song by German DJ and record producer Robin Schulz. The song was released in Germany on 17 July 2015, and samples Baby Bash's 2003 single \"Suga Suga\".\n\n[Sugar (Robin Schulz album)]\nSugar is the second studio album by German DJ and record producer Robin Schulz, it was released on 25 September 2015. The album includes the singles \"Headlights\", \"Sugar\", \"Show Me Love\", and \"Heatwave\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5b155963af",
  "kind": "yes/no",
  "text": "Claim: \"Lost in Space\" aired on Nickelodeon's programming block on a Sunday.\n\nPassages:\n\n[Lost in Space (American Dad!)]\nThe episode aired on May 5, 2013, on Fox's Animation Domination lineup.\n\n[Animation Domination]\nThe block aired on Sunday evenings through the entirety of that night's primetime schedule (unless preempted, usually by sports telecasts).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qfb3ea701eb",
  "kind": "yes/no",
  "text": "Claim: A freeway that runs east-west through Bower in part of a country was named after an author. He was born 16 November 1920. Bossiaea walkeri is a flowering plant found in this part of a country.\n\nPassages:\n\n[Colin Thiele]\nColin Milton Thiele AC ( ; 16 November 1920 – 4 September 2006) was an Australian author and educator.\n\n[Thiele Highway]\nIt is named after author Colin Thiele who lived most of his life in towns along the route, and set some of his stories in the area.\n\n[Bossiaea walkeri]\nIt occurs in Western Australia, South Australia, Victoria and New South Wales.\n\n[Bower, South Australia]\nBower is a town in South Australia, approximately halfway between Eudunda and Morgan on the Thiele Highway.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
