# A46 replay label-noise blind read RSBS00-blind_read-940f9955-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS00-blind_read-940f9955-000.json

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
  "qid": "q666b960c96",
  "kind": "yes/no",
  "text": "Claim: Penlee Point, the coastal headland to the SW of the village of Rame in a southeastern county in the UK, lies at the entrance of the Rame Peninsula. This county is the location of the Doom Bar.\n\nPassages:\n\n[Penlee Point, Rame]\nPenlee Point (Cornish: Penn Legh , meaning \"stone-slab headland\") is a coastal headland to the southeast of the village of Rame in southeast Cornwall, UK. The point lies at the entrance to Plymouth Sound.\n\n[Cornwall]\nCornwall ( , ; Cornish: Kernow ] ) is a ceremonial county in the United Kingdom.\n\n[Doom Bar]\nThe Doom Bar (previously known as Dunbar sands, Dune-bar, and similar names) is a sandbar at the mouth of the estuary of the River Camel, where it meets the Celtic Sea on the north coast of Cornwall, England.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3aa8f8248b",
  "kind": "yes/no",
  "text": "Claim: The Sewanhaka Central High School District is composed of Sewanhaka High School, Elmont Memorial High School, New Hyde Park Memorial High School, Floral Park Memorial High School, and one other. That other school serves students in the census-designated place of Nassau County in New York.\n\nPassages:\n\n[H. Frank Carey Junior-Senior High School]\nH. Frank Carey High School is a public high school located in Franklin Square, New York serving students in the seventh through twelfth grades from the towns of Franklin Square, Garden City South, West Hempstead, and Elmont.\n\n[Garden City South, New York]\nGarden City South is a hamlet and census-designated place (CDP) in Nassau County, New York, United States.\n\n[Sewanhaka Central High School District]\nThe district is currently composed of five high schools: Sewanhaka High School, Elmont Memorial High School, New Hyde Park Memorial High School, Floral Park Memorial High School, and H. Frank Carey Junior-Senior High School.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qba66b84f9b",
  "kind": "yes/no",
  "text": "Claim: This publication is published more often than Bookmarks. Keith Moon was inducted into its Hall of Fame in the early 'eighties.\n\nPassages:\n\n[Modern Drummer]\nModern Drummer is a monthly publication targeting the interests of drummers and percussionists.\n\n[Keith Moon]\nHe was posthumously inducted into the \"Modern Drummer\" Hall of Fame in 1982, becoming only the second rock drummer to be chosen, and in 2011, Moon was voted the second-greatest drummer in history by a \"Rolling Stone\" readers' poll.\n\n[Bookmarks (magazine)]\nBookmarks is a bimonthly American literary magazine dedicated to general readers, book groups, and librarians.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q84f4b5f043",
  "kind": "yes/no",
  "text": "Post: Everytime I exit and reopen the Instagram app it freezes",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q59f242cd99",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I would point out that how can a President be censored if he has his own press Corp right there in the White House",
   "@DonaldJTrumpJr If only he had a press Corp in the house...oh wait! Shut up Jr! Time to get fitted for those lovely orange jumpsuits! If you can't be orange anymore at least you can wear it!!!"
  ]
 },
 {
  "qid": "qbce9e56b71",
  "kind": "yes/no",
  "text": "Claim: The man who released \"Fare Forward Voyagers\" died from surgical infection in the year 2001.\n\nPassages:\n\n[Fare Forward Voyagers (Soldier's Choice)]\nFare Forward Voyagers (Soldier's Choice) (or simply, Fare Forward Voyagers) is an album by American fingerstyle guitarist and composer John Fahey, released in 1973.\n\n[John Fahey (musician)]\nHe died in 2001 from complications from heart surgery.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa826cc3bca",
  "kind": "yes/no",
  "text": "Claim: A building is located on the area that is home to the Luxor Obelisk in Paris. This building hosted the 7th Lumières Awards.\n\nPassages:\n\n[Hôtel de Crillon]\nLocated at the foot of the Champs-Élysées, the Crillon along with the Hotel de la Marine is one of two identical stone palaces on the Place de la Concorde.\n\n[Place de la Concorde]\nThe Place de la Concorde (] ) is one of the major public squares in Paris, France.\n\n[Luxor Obelisk]\nThe Luxor Obelisk (French: \"Obélisque de Louxor\") is a 23 m high Egyptian obelisk standing at the center of the Place de la Concorde in Paris, France.\n\n[7th Lumières Awards]\nThe winners were announced at a press conference at the Hôtel de Crillon in Paris. \"",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1db25b2b77",
  "kind": "yes/no",
  "text": "Claim: Tennessee–Tombigbee Waterway Canal is longer than the Massachusetts Segment.\n\nPassages:\n\n[Hampshire and Hampden Canal]\nThe Hampshire and Hampden Canal was the Massachusetts segment of an 86 mi canal that once connected New Haven, Connecticut to the Connecticut River north of Northampton, Massachusetts.\n\n[Farmington Canal]\nIts Massachusetts segment was known as the Hampshire and Hampden Canal.\n\n[Tennessee–Tombigbee Waterway]\nThe Tennessee–Tombigbee Waterway (popularly known as the Tenn-Tom) is a 234-mile (377-kilometer) man-made waterway that extends from the Tennessee River to the junction of the Black Warrior-Tombigbee River system near Demopolis, Alabama, United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q5465476837",
  "kind": "yes/no",
  "text": "Claim: Twin Pines/Lone Pine Mall is the fictional name of the mall in the movie \"Back to the Future\" which was filmed at the headquarters of EverTrust Bank.\n\nPassages:\n\n[Puente Hills Mall]\nIt is most famous for serving as the filming site for the Twin Pines/Lone Pine Mall for the 1985 movie \"Back to the Future\" starring Michael J. Fox and Christopher Lloyd.\n\n[EverTrust Bank]\nEverTrust Bank (華信商業銀行), or Ever Trust Bank and Evertrust Bank, as its advertisement often appeared in the local Chinese media, is an overseas Chinese bank in the United States.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q5de88d6009",
  "kind": "yes/no",
  "text": "Claim: There were ten episodes made for the science heroes series with Gus Birney.\n\nPassages:\n\n[The Mist (TV series)]\nThe Mist is an American science fiction-horror thriller television series developed by Christian Torpe for Spike. The first season, consisting of ten episodes, premiered on June 22, 2017. On September 27, 2017, Spike cancelled the series after one season.\n\n[Gus Birney]\nGus Birney is an American actress, best known for her role as Alex in \"The Mist\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9a74aa976b",
  "kind": "yes/no",
  "text": "Claim: A minor type of wheat beer is brewed in the city Givichy Universal is located in. The brewery was founded in the year 1900.\n\nPassages:\n\n[Lambic]\nLambic is a type of beer brewed in the Pajottenland region of Belgium southwest of Brussels and in Brussels itself at the Cantillon Brewery.\n\n[Cantillon Brewery]\nBrasserie-Brouwerij Cantillon (or Cantillon Brewery) is a small Belgian traditional family brewery based in Anderlecht, Brussels and founded in 1900.\n\n[Givichy Universal]\nGivichy Universal is currently located at Brussels in Belgium.\n\n[Wheat beer]\nThe two main varieties are Weissbier and Witbier; minor types include Lambic, Berliner Weisse and Gose.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qbf456ce56c",
  "kind": "yes/no",
  "text": "Claim: Lewis Moran was murdered a week after the death of the hitman from the Australian city of Melbourne.\n\nPassages:\n\n[Lewis Moran]\nHis murder occurred one week after the funeral of fellow Melbourne underworld criminal and suspected hitman Andrew Veniamin.\n\n[Andrew Veniamin]\nAndrew \"Benji\" Veniamin (16 November 1975 – 23 March 2004) was an Australian criminal from Melbourne, Victoria, Australia.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qcdf5ce278d",
  "kind": "yes/no",
  "text": "Claim: The rock band Sugar Ray began as a funk metal band, while the band Das Damen was considered alternative rock.\n\nPassages:\n\n[Das Damen]\nDas Damen was an alternative rock band from New York City, United States, formed in 1984.\n\n[Sugar Ray]\nThe band, starting off more as a funk metal band, gained mainstream fame in 1997 with their release of the song \"Fly\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2627cc8636",
  "kind": "yes/no",
  "text": "Claim: He was the older brother of David Rockefeller chief executive of Chase Manhattan Corporation. Blanchette Ferry Rockefeller is the wife of this businessman.\n\nPassages:\n\n[John D. Rockefeller III]\nHe was the eldest son of philanthropists John D. Rockefeller Jr. and Abby Aldrich Rockefeller.\n\n[David Rockefeller]\nDavid Rockefeller (June 12, 1915 – March 20, 2017) was an American banker who was chairman and chief executive of Chase Manhattan Corporation. Rockefeller was a son of John D. Rockefeller Jr. and Abby Aldrich Rockefeller, and a grandson of John D. Rockefeller and Laura Spelman Rockefeller.\n\n[Blanchette Ferry Rockefeller]\nBlanchette Ferry Hooker (October 2, 1909 – November 29, 1992) was the wife of John D. Rockefeller III and mother of Jay Rockefeller.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q4f373e1aad",
  "kind": "yes/no",
  "text": "Claim: The film Vanessa Kirby played Joanna in is a British romantic comedy-drama film that stars an Irish actor and writer who recieved a Bachelor of Arts from The Abduction Club.\n\nPassages:\n\n[Domhnall Gleeson]\nDomhnall Gleeson ( ; born 12 May 1983) is an Irish actor and writer. He received a Bachelor of Arts in Media Arts from Dublin Institute of Technology.\n\n[Vanessa Kirby]\nShe starred as Estella in the BBC adaptation of \"Great Expectations\" in 2011, as Joanna in Richard Curtis' romantic comedy \"About Time\" in 2013, and currently portrays Princess Margaret in Peter Morgan's Netflix series \"The Crown\", for which she has been nominated for the British Academy Television Award for Best Supporting Actress.\n\n[About Time (2013 film)]\nAbout Time is a 2013 British romantic comedy-drama film about a young man with the special ability to time travel who tries to change his past in order to improve his future. The film was written and directed by Richard Curtis, and stars Domhnall Gleeson, Rachel McAdams and Bill Nighy.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qccada642fe",
  "kind": "yes/no",
  "text": "Claim: Buffalo Rock produced a drink under its own name. That drink and that which Steven Reinemund acquired, are not both artificially flavored soft drinks.\n\nPassages:\n\n[Buffalo Rock]\nIn addition to bottling Pepsi products, the company produced Grapico in 1981, a grape-flavored soft drink, and a ginger ale under its own brand name.\n\n[Grapico]\nGrapico is a caffeine-free, artificially flavored carbonated soft drink with a purple color and a grape taste that is sold in the Southeastern United States.\n\n[Steven Reinemund]\nHe led the acquisitions of several other food and beverage companies including Quaker Oats, Naked Juice, Izze and Stacy’s Chips.\n\n[Izze]\nIzze is an all-natural, no-preservatives-added fruit soda.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q685890651c",
  "kind": "yes/no",
  "text": "Post: I too enjoy making shit up and pretending like I understand basic economic principles https://t.co/cHDBHaxBBR",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q1136ede348",
  "kind": "yes/no",
  "text": "Claim: After he left the World Wrestling Federation, Lanny Poffo's older brother performed in another organization. Tatsutoshi Goto also competed in the same organization.\n\nPassages:\n\n[Randy Savage]\nRandy Mario Poffo (November 15, 1952 – May 20, 2011), better known by the ring name \"Macho Man\" Randy Savage, was an American professional wrestler and color commentator best known for his time in the World Wrestling Federation (WWF, now WWE) and later World Championship Wrestling (WCW).\n\n[World Championship Wrestling]\nWorld Championship Wrestling, Inc. (WCW) was an American professional wrestling promotion, historically based in Atlanta, Georgia.\n\n[Tatsutoshi Goto]\nHe also briefly competed in WCW as part of the nWo Japan.\n\n[Lanny Poffo]\nHe is also the real-life younger brother of \"Macho Man\" Randy Savage.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qca4deab5e0",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which text is sarcastic?",
  "options": [
   "Stop putting beomsil on my timeline.",
   "next person that puts beomsil on my tl has to deal w me crying on the floor"
  ]
 },
 {
  "qid": "qdbc388d7de",
  "kind": "yes/no",
  "text": "Post: shut the hell up https://t.co/QeOnvsraNM",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qcabf4b4ffb",
  "kind": "yes/no",
  "text": "Post: Anyone need a body for a human sacrifice? Trying to find a valid excuse to not go to work today.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qac724840ad",
  "kind": "yes/no",
  "text": "Post: The most 2020 quote of the year:\n\nMe: we should go to the Van Gogh Museum!\nLittle Brother: is that the donny with one ear?",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q39e72d74d1",
  "kind": "yes/no",
  "text": "Claim: The star of The Secret Agent starred in a film in 2006, directed by Shane Meadows.\n\nPassages:\n\n[The Secret Agent (TV series)]\nThe show stars Toby Jones, Vicky McClure, Stephen Graham and Ian Hart.\n\n[Stephen Graham]\nStephen Graham (born 3 August 1973) is an English film and television actor, known for his roles as Tommy in the film \" Snatch\" (2000), Andrew \"Combo\" Gascoigne in \"This Is England\" (2006) as well as its television sequels, \"This Is England '86\" (2010), \"This Is England '88\" (2011) and \"This Is England '90\" (2015), notorious bank robber Baby Face Nelson in \"Public Enemies\" (2009), Scrum in the \"Pirates of the Caribbean\" films and Al Capone in the HBO series \"Boardwalk Empire\".\n\n[This Is England]\nThis Is England is a 2006 British drama film written and directed by Shane Meadows.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8674d3dfc4",
  "kind": "yes/no",
  "text": "Claim: Duchess Eleanor of Lan Na is the mother of the king that Walchelin de Ferriers was principal captain to.\n\nPassages:\n\n[Richard I of England]\nHe was the third of five sons of King Henry II of England and Duchess Eleanor of Aquitaine.\n\n[Walchelin de Ferriers]\nWalchelin de Ferrieres (or Walkelin de Ferrers) (died 1201) was a Norman baron and principal captain of King Richard I of England.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q48402bc39a",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Halfway through snowboarding day 1 and pretty sure I have fallen at least 69 times 😆♋️",
   "Halfway through snowboarding day 1 and pretty sure I have fallen at least 10 times."
  ]
 },
 {
  "qid": "qe9bf099960",
  "kind": "yes/no",
  "text": "Claim: The Grammy award winner for song for the year put out a 1971 album by the Carpenters and won an Academy Award for Best Original Song for A Star is Born.\n\nPassages:\n\n[Paul Williams (songwriter)]\nHe is perhaps best known for writing popular songs performed by a number of acts in the 1970s, including Three Dog Night's \"An Old Fashioned Love Song\" and \"Out in the Country\", Helen Reddy's \"You and Me Against the World\", David Bowie's \"Fill Your Heart\", and the Carpenters' \"We've Only Just Begun\" and \"Rainy Days and Mondays\", as well as for his contributions to films, such as writing the lyrics to the #1 chart-topping \"Evergreen\", the love theme from \"A Star Is Born\", starring Barbra Streisand, for which he won a Grammy for Song of the Year and an Academy Award for Best Original Song; and \"Rainbow Connection\" from \"The Muppet Movie\".\n\n[Let Me Be the One (The Carpenters song)]\n\"Let Me Be the One\" is a song written in 1971 by Roger Nichols and Paul Williams.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q0f167d74d4",
  "kind": "yes/no",
  "text": "Claim: The TV show, Home, is broadcast 24 hours a day on Sky, Virgin Media and another company. The device that shows Motorz TV can air channels from that company for free and allows users to play using a remote.\n\nPassages:\n\n[TVPlayer]\nTVPlayer is a live TV streaming service for users to watch free-to-air channels through their smart devices (Apple TV 4th Generation Only, Amazon Fire TV) desktops, smartphones and tablets.\n\n[Home (TV channel)]\nHome is broadcast 24 hours a day on Sky, Virgin Media and TVPlayer.\n\n[Amazon Fire TV]\nThe device also allows users to play video games with the included remote, via a mobile app, or with an optional game controller.\n\n[Motorz TV]\nMotorz (pronounced \"Motors\") is an American television series seen nationwide on Youtoo America, Rev'n, Untamed Sports TV, Biz Television, Tuff TV, The Auto Channel, The Rural Channel, and globally on YouTube, Amazon Fire TV, Roku and iTunes.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qaf97015327",
  "kind": "yes/no",
  "text": "Claim: Julia Smith and Tony Holland were the creators of the long-running British soap opera in which Alison Pargeter plays the role of florist Sarah Cairns.\n\nPassages:\n\n[Alison Pargeter]\nAlison Pargeter (born 31 May 1972) is an English actress who played the roles of stalker Sarah Cairns in the BBC soap opera \"EastEnders\", also Mary Slessor in an 11-part television series of\" Mary Slessor\", and the Nag's Head barmaid called Val in the BBC \"Only Fools and Horses\" prequel \"Rock & Chips\".\n\n[EastEnders]\nEastEnders is a long-running British soap opera created by Julia Smith and Tony Holland which has been broadcast on BBC One since 1985.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q48e7b7fa35",
  "kind": "yes/no",
  "text": "Claim: Markounda is a sub-prefecture that borders an African country bordered by the Sudan and another country and is known for the Dar Sila region. Gurgi Mosque is located in the other country.\n\nPassages:\n\n[Markounda]\nThe sub-prefecture borders with Chad.\n\n[Sila Region]\nSila or Dar Sila is a region of Chad which was created in 2008 from the departments of Sila and Djourf Al Ahmar previously part of Ouaddaï Region.\n\n[Gurgi Mosque]\nGurgi Mosque is a mosque in Tripoli, Libya.\n\n[Chad]\nIt is bordered by Libya to the north, Sudan to the east, the Central African Republic to the south, Cameroon and Nigeria to the southwest and Niger to the west.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q99bd2c1fe0",
  "kind": "yes/no",
  "text": "Claim: Brad Elterman is a professional photographer who addressed the rock 'n' roll lifestyle of a band that became noted for its eclectic mix of musical styles.\n\nPassages:\n\n[Blondie (band)]\nBlondie is an American rock band founded by singer Debbie Harry and guitarist Chris Stein. Over the next three years, the band achieved several hit singles including \"Call Me\", \"Rapture\" and \"Heart of Glass\" and became noted for its eclectic mix of musical styles incorporating elements of disco, pop, reggae, and early rap music.\n\n[Brad Elterman]\nBrad Elterman is a professional photographer from Beverly Hills, California, who addressed the rock 'n' roll lifestyle in Hollywood encompassing pop, punk and rock bands that included the Faces with Rod Stewart, David Bowie, Robert Plant, Sex Pistols, the Runaways, Bebe Buell, Kiss, Queen, Blondie, the Ramones, Bay City Rollers, ABBA, Boney M, Kenny Rogers, The Who, Leif Garrett, Michael Jackson, among others.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qb8acf064c7",
  "kind": "yes/no",
  "text": "Claim: Joseph Eccles was born in England.\n\nPassages:\n\n[Accrington]\nAccrington is a town in the Hyndburn borough of Lancashire, England.\n\n[Joseph Eccles]\nJoseph Eccles (13 April 1863 – 2 September 1933) was an English cricketer active from 1886 to 1889 who played for Lancashire. He was born in Accrington and died in Preston.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd87b8183a5",
  "kind": "yes/no",
  "text": "Claim: The publication which covered the subject Fortean named for Charles Hoy Fort, had Nancy Hayfield on its staff.\n\nPassages:\n\n[Nancy Hayfield]\nShe was also the last editor-in-chief of UFO Magazine when that publication ceased publication.\n\n[UFO Magazine]\n\"UFO Magazine\" was an American magazine that was devoted to the subject of unidentified flying objects (UFOs), the extraterrestrial hypothesis (ETH), as well as paranormal and Fortean subjects in general.\n\n[Charles Fort]\nThe terms \"Fortean\" and \"Forteana\" are sometimes used to characterize various such phenomena.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa208dfd14a",
  "kind": "yes/no",
  "text": "Claim: Luiz Felipe Scolari is the FIFA World Cup winner known as Big Phil that Flávio Murtosa works as an assistant coach and manager for.\n\nPassages:\n\n[Luiz Felipe Scolari]\nLuiz Felipe Scolari, (] , ] ; born 9 November 1948), also known as Felipão in Brazil and as Phil Scolari or Big Phil in the English-speaking world, is a FIFA World Cup winner Brazilian football manager and former professional footballer, who is the current manager of Chinese club Guangzhou Evergrande in the Chinese Super League.\n\n[Flávio Murtosa]\nMurtosa has a long friendship with FIFA World Cup winning manager Luiz Felipe Scolari and works mostly as his assistant coach.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q2eba1133e6",
  "kind": "yes/no",
  "text": "Claim: The city where the all-seater Róisín Dubh is located is in the Western area of Ireland. It is also the home of Sean Smyth.\n\nPassages:\n\n[Seán Smyth]\nBorn in Straide, County Mayo, and now living in Galway, Seán is an All-Ireland champion on both fiddle and whistle .\n\n[Galway]\nGalway ( ; Irish: \"Gaillimh\" , ] ) is a city in the West of Ireland in the province of Connacht.\n\n[Róisín Dubh (music venue)]\nThe Róisín Dubh is an established live music venue in Galway, Ireland.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf765d0312e",
  "kind": "yes/no",
  "text": "Claim: Nick Tosches wrote the 1993 best selling book Power in Earth detailing the connections between the Gambino crime family, the Vatican Bank and the Franklin National Bank.\n\nPassages:\n\n[Franklin National Bank]\nFranklin National Bank, based in Franklin Square in Long Island, New York was once the United States' 20th largest bank.\n\n[Power on Earth]\nPower on Earth is a biography of Mafia-linked Italian banker and accused murderer Michele Sindona written by Nick Tosches. It also details his connections with the Gambino crime family, the Vatican Bank, the Franklin National Bank in Long Island, New York, and the murder of Giorgio Ambrosoli, a lawyer overseeing the liquidation of his banks.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa6cadbdb91",
  "kind": "yes/no",
  "text": "Post: just impulse bought a mandolin and in 3-5 buisness days i will impulse learn some jigs",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qb5457a4e1b",
  "kind": "yes/no",
  "text": "Claim: Peppa Pig was the French preschool series, directed by Astley Baker Davies. The series had its music composed by the one whose theme had orchestral renditions in Wallace & Gromit's Musical Marvels.\n\nPassages:\n\n[Julian Nott]\nHe is best known for his work on the \"Wallace and Gromit\" films and Peppa Pig animations.\n\n[Peppa Pig]\nPeppa Pig is a British preschool animated television series directed and produced by Astley Baker Davies in association with Entertainment One, which originally aired on 31 May 2004.\n\n[Wallace &amp; Gromit's Musical Marvels]\nWallace & Gromit's Musical Marvels (also known as Wallace & Gromit at the Proms) is the name of Prom 20 of the 2012 season of The BBC Proms, which features orchestral renditions of Julian Nott's theme from Wallace & Gromit and classical music set to scenes from the Wallace & Gromit films.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qee7c064c68",
  "kind": "yes/no",
  "text": "Claim: The 1985 film, of which Wild Search is a pseudo-remake, and Pamela Wallace have the country Asian in common.\n\nPassages:\n\n[Witness (1985 film)]\nWitness is a 1985 American crime thriller film directed by Peter Weir and starring Harrison Ford and Kelly McGillis.\n\n[Wild Search]\nThe film is a pseudo-remake of the 1985 film \"Witness\" and deals with Hong Kong cops and Mainland criminals.\n\n[Pamela Wallace]\nPamela Wallace (born 1949 in Exeter, California) is an American screenwriter and author.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4e2d46e475",
  "kind": "yes/no",
  "text": "Claim: Studio A.C.G.T animated the TV anime adaptation of Dies irae.\n\nPassages:\n\n[Dies Irae (anime)]\nIt is animated by the studio A.C.G.T, and is an adaptation of Light's video game of the same name.\n\n[Dies irae (visual novel)]\nA TV anime adaptation, \"Dies Irae\", is planned for broadcast in 2017.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qee6065c9f1",
  "kind": "yes/no",
  "text": "Claim: The star of the show \"Mindfreak\" written by Ben Seidman generated $150 million in tourist revenue for his live performance show in Paradise, Nevada.\n\nPassages:\n\n[Luxor Las Vegas]\nLuxor Las Vegas is a hotel and casino situated on the southern end of the Las Vegas Strip in Paradise, Nevada.\n\n[Ben Seidman]\nHis inventions are employed in A&E’s program Mindfreak, starring Criss Angel, where Seidman served as writer and adviser for three seasons.\n\n[Criss Angel]\nChristopher Nicholas Sarantakos (born December 19, 1967), known by the stage name Criss Angel, is an American magician, illusionist and musician. He is known for starring in the television and stage show \"Criss Angel Mindfreak\" and his previous live performance illusion show \"Criss Angel Believe\" in collaboration with \"Cirque du Soleil\" at the Luxor casino in Las Vegas. The show generated $150 million in tourist revenue to Las Vegas in 2010, but has since been replaced by \"Mindfreak LIVE\" on 11 May 2016 (the show is partly produced by Cirque, however the directive rights are entirely with Criss Angel).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2904f8f88b",
  "kind": "yes/no",
  "text": "Claim: The 2010 head coach of the SMU Mustangs football team currently coaches in the Canadian Football League in the summer season.\n\nPassages:\n\n[2010 SMU Mustangs football team]\nThe Mustangs, led by third-year head coach June Jones, were members of Conference USA in the West Division and played their home games at Gerald J. Ford Stadium.\n\n[June Jones]\nJune Sheldon Jones III (born February 19, 1953) is an American football coach and former player, currently serving as a head coach of the Hamilton Tiger-Cats of the Canadian Football League (CFL).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q346807be19",
  "kind": "yes/no",
  "text": "Claim: The actor appeared in The Magic Roundabout, a 2005 American-British computer-animated adventure fantasy that was based on a TV series. He also starred in another film. The other film also starred in Sexy Beast.\n\nPassages:\n\n[Amanda Redman]\nHer film roles include \"For Queen and Country\" (1988), \"Sexy Beast\" (2000) and \"\" (2001).\n\n[Sexy Beast]\nThe film stars Ray Winstone, Ben Kingsley and Ian McShane.\n\n[The Magic Roundabout (film)]\nThe Magic Roundabout (released in France as Pollux - Le manège enchanté and redubbed in the United States as Doogal or The Lord of the Springs) is a 2005 French-British computer-animated adventure fantasy film based on the television series \"The Magic Roundabout\".\n\n[Ray Winstone]\nHe has appeared in films such as \"Cold Mountain\", \"Nil By Mouth\", \"King Arthur\", \"The Magic Roundabout\", \"The Departed\", \"Beowulf\", \"Indiana Jones and the Kingdom of the Crystal Skull\", \"Edge of Darkness\", \"The Sweeney\" and \"Noah\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q0d8fe5f38a",
  "kind": "yes/no",
  "text": "Claim: The soft drink that The Coca-Cola Company introduced Mello Yello to compete with is owned by Coca-Cola's. So is the producer of orange juice founded by Anthony T. Rossi.\n\nPassages:\n\n[Mello Yello]\nMello Yello is a highly-caffeinated, citrus-flavored soft drink produced and distributed by The Coca-Cola Company which was introduced on March 1, 1979 to compete with PepsiCo's Mountain Dew.\n\n[Anthony T. Rossi]\nAnthony Talamo Rossi (September 13, 1900 – January 24, 1993) was an Italian immigrant who founded Tropicana Products, a producer of orange juice founded in 1947 in Bradenton, Florida in the United States which grew from 50 employees to over 8,000 in 2004, expanding into multiple product lines and became one of the world's largest producers and marketers of citrus juice.\n\n[Tropicana Products]\nSince 1998, it has been owned by PepsiCo.\n\n[Mountain Dew]\nIn August 1964, the Mountain Dew brand and production rights were acquired from Tip by the Pepsi-Cola company, at which point distribution expanded more widely across the United States and Canada.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q79abc667f2",
  "kind": "yes/no",
  "text": "Claim: This actress is from the film that Alec Utgoff acted in, and worked as a model. She starred in X-Men: Apocalypse.\n\nPassages:\n\n[Alec Utgoff]\nHis other notable roles include Aleksandr Borovsky in \"\" (2014), Dmitri in \"Mortdecai\" (2015) and Alexi in \"San Andreas\" (2015).\n\n[Olivia Munn]\nLisa Olivia Munn (born July 3, 1980) is an American actress and model.\n\n[Mortdecai (film)]\nIt stars Johnny Depp in the title role and also features Gwyneth Paltrow, Ewan McGregor, Olivia Munn, Paul Bettany and Jeff Goldblum.\n\n[X-Men: Apocalypse]\nDirected by Bryan Singer, with a screenplay by Simon Kinberg from a story conceived by Singer, Kinberg, Michael Dougherty and Dan Harris, the film stars James McAvoy, Michael Fassbender, Jennifer Lawrence, Oscar Isaac, Nicholas Hoult, Rose Byrne, Tye Sheridan, Sophie Turner, Olivia Munn and Lucas Till.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qd358755ea7",
  "kind": "yes/no",
  "text": "Claim: The man Tony Bennet called \"The Father of Rock and Roll\" once toured with Lola Dee who once auditioned for \"Junior Junction\", and landed a recording contract in her teens.\n\nPassages:\n\n[Lola Dee]\nLola Dee is an American singer and recording artist with Mercury Records and Columbia Records labels in the 1950s and 1960s. At the age of 14, she was heard in an amateur contest and asked to audition for a network teen-aged show called \"Junior Junction\". At 16 she was signed to a recording contract. She recorded over 40 sides, including the half million best seller \"Only You\" in 1955. Her popularity as a recording artist gave her the opportunity to tour with such stars as Bob Hope, Johnnie Ray and Jimmy Durante in the late 1950s and 1960s.\n\n[Johnnie Ray]\nJohn Alvin Ray (January 10, 1927 – February 24, 1990) was an American singer, songwriter, and pianist. Extremely popular for most of the 1950s, Ray has been cited by critics as a major precursor to what would become rock and roll, for his jazz and blues-influenced music and his animated stage personality. Tony Bennett called Ray the \"father of rock and roll,\" and historians have noted him as a pioneering figure in the development of the genre.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa08190ff8f",
  "kind": "yes/no",
  "text": "Claim: Dempster Brothers, Inc. was founded by Thomas and Rothwell and their brother, who often staged political battles. The brother and the eccentric Knoxville businessman were born in 1902.\n\nPassages:\n\n[Cas Walker]\nOrton Caswell \"Cas\" Walker (March 23, 1902 – September 25, 1998), was a Tennessee businessman, politician, and personality on television and radio.\n\n[George Roby Dempster]\nDempster also served as a city manager and mayor of Knoxville, where he became legendary for his political battles with eccentric Knoxville businessman Cas Walker and \"Knoxville Journal\" editor Guy Smith, Jr.\n\n[Dempster Brothers]\nThe firm was originally established by George Roby Dempster with his brothers Thomas and John Dempster.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q51075027a3",
  "kind": "yes/no",
  "text": "Claim: Cold North Killers: Canadian Serial Murder includes a serial killer who committed murders in Canada and was American.\n\nPassages:\n\n[Cold North Killers: Canadian Serial Murder]\n\"Cold North Killer's\" own definition of what constitutes a Canadian serial killer includes both Canadians who committed murder abroad (such as Keith Hunter Jesperson and Gordon Stewart Northcott) and non-Canadians who committed murder in Canada (like William Dean Christenson and Earle Nelson).\n\n[Earle Nelson]\nEarle Leonard Nelson, known as \"the Gorilla Man,\" (May 12, 1897January 13, 1928) was an American serial killer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb3b0162b98",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "I absolutely hate potty training toddlers.",
   "Wow... the universe gave me the task of a potty training a whole human? the audacity."
  ]
 },
 {
  "qid": "qeb89b9be3f",
  "kind": "yes/no",
  "text": "Claim: Greg Costikyan did not have the same profession as the drummer of the ENglish band System of a Down.\n\nPassages:\n\n[Greg Costikyan]\nGreg Costikyan (born July 22, 1959, in New York City), sometimes known under the pseudonym \"Designer X\", is an American game designer and science fiction writer.\n\n[John Dolmayan]\nJohn Hovig Dolmayan (Armenian: Ջոն Դոլմայան , born July 15, 1973) is a Lebanese-born Armenian–American songwriter and drummer.\n\n[System of a Down]\nThe band currently consists of Serj Tankian (lead vocals, keyboards), Daron Malakian (vocals, guitar), Shavo Odadjian (bass, backing vocals) and John Dolmayan (drums).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qfb75b05b92",
  "kind": "yes/no",
  "text": "Claim: This American composer composed Troubled Island. He was born in 1895 was married to his frequent collaborator Verna Arvey.\n\nPassages:\n\n[A Bayou Legend]\nA Bayou Legend is an American opera composed by William Grant Still, with a libretto by his wife and frequent collaborator, Verna Arvey.\n\n[Troubled Island]\nTroubled Island is an American opera in three acts composed by William Grant Still, with a libretto begun by poet Langston Hughes and completed by Verna Arvey.\n\n[William Grant Still]\nWilliam Grant Still (May 11, 1895 – December 3, 1978) was an American composer, who composed more than 150 works, including five symphonies and eight operas.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 }
]
