# A46 replay label-noise blind read RSAS02-blind_read-2d2f0202-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS02-blind_read-2d2f0202-002.json

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
  "qid": "q181f8c8fa1",
  "kind": "yes/no",
  "text": "Claim: The Walt Disney company produced neither the movie where H. Lee Peterson was an assistant editor nor The Strongest Man in the World.\n\nPassages:\n\n[H. Lee Peterson]\nHis credits for Walt Disney Pictures include being an assistant editor for \"The Little Mermaid\", and the lead film editor for \"Aladdin\", \"Pocahontas\", \"Dinosaur\", \"Home on the Range\" and the short film \"The Prince and the Pauper; starring Mickey Mouse\".\n\n[The Strongest Man in the World]\nThe Strongest Man in the World is a 1975 Disney film starring Kurt Russell, still a student in the fictional Medfield College.\n\n[The Little Mermaid (1989 film)]\nThe Little Mermaid is a 1989 American animated musical fantasy film produced by Walt Disney Feature Animation and released by Walt Disney Pictures.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qfa1f0bb8c4",
  "kind": "yes/no",
  "text": "Claim: Tales of Tahoe Tessie state that the creature resides in an underwater tunnel. According to the 2010 census, the population of the town located approximately seven miles south of that underwater tunnel was 842.\n\nPassages:\n\n[Cave Rock Tunnel]\nThe Cave Rock Tunnel is a dual bore highway tunnel on U.S. Route 50 (US 50) along the eastern shore of Lake Tahoe approximately seven miles (11.4 km) north of Stateline, in Douglas County, Nevada, United States.\n\n[Tahoe Tessie]\nTales of the lake-dwelling creature can be traced to stories told by members of the Washoe and Paiute tribes in the mid-19th century, stating that the creature resides in an underwater tunnel beneath Cave Rock, and sightings have continued into modern day.\n\n[Stateline, Nevada]\nThe population was 842 at the 2010 census.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qef81653785",
  "kind": "yes/no",
  "text": "Post: do i just blast maneskin to get hyped for my osce or??",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q6269616c3a",
  "kind": "yes/no",
  "text": "Claim: Although \"Perfect\" was the final commercial single from the Smashing Pumpkins fourth album that included the song \"Let Me Give the World to You\", two songs were subsequently released as promotional singles. One of these song's artwork is done by a French photographer.\n\nPassages:\n\n[Yelena Yemchuk]\nYelena Yemchuk (Ukrainian: Єлена Ємчук, born April 22, 1970) is a Ukrainian professional photographer, painter and film director, best known for her work with The Smashing Pumpkins.\n\n[Crestfallen]\n\"Crestfallen\" is a track on The Smashing Pumpkins' 1998 album, \"Adore\". The single's artwork is by Yelena Yemchuk.\n\n[Perfect (The Smashing Pumpkins song)]\nIt was the final commercial single from the album, although \"Crestfallen\" and \"To Sheila\" were subsequently released as promotional singles.\n\n[Let Me Give the World to You]\nThe song, produced with music producer Rick Rubin in 1997 during the sessions for \"Adore\" album, was removed from the album at the last second by band frontman Billy Corgan, who did so as a last-ditch effort to keep the record company from releasing it as a single against his wishes.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb8ef0763a7",
  "kind": "yes/no",
  "text": "Claim: Bassbariton had the lowest vocal range in the group that produced the album Pa un par.\n\nPassages:\n\n[Bass (voice type)]\nA bass ( ) is a type of classical male singing voice and has the lowest vocal range of all voice types.\n\n[Cosmos (band)]\nCosmos was a Latvian a cappella band that formed in Riga in 2002. The band comprised singers Jānis Šipkēvics, Andris Sējāns (both countertenors), Juris Lisenko (tenor), Jānis Ozols (baritone), Jānis Strazdiņš (bass) and Reinis Sējāns (rhythm).\n\n[Pa un par]\nPa un par (On and About) is an album by the Latvian A cappella vocal group Cosmos, that was released on the UPE record label in 2005.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q19aef125f8",
  "kind": "yes/no",
  "text": "Claim: Planes was released after Charley and the Angel.\n\nPassages:\n\n[Charley and the Angel]\nCharley and the Angel is a 1973 Disney family/comedy film set in an unidentified small city in the 1930s Depression-era Midwestern United States and starring Fred MacMurray in one of his final film appearances and his last movie for Disney.\n\n[Planes (film)]\nPlanes is a 2013 American 3D computer-animated sports comedy film produced by DisneyToon Studios and released by Walt Disney Pictures.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc5c73b9299",
  "kind": "yes/no",
  "text": "Claim: Mock orange is a mostly Holarctic genus of shrubs. That genus contains more species than Sarracenia.\n\nPassages:\n\n[Sarracenia]\nSarracenia ( or ) is a genus comprising 8 to 11 species of North American pitcher plants, commonly called trumpet pitchers.\n\n[Philadelphus]\nPhiladelphus ( ) (mock-orange) is a genus of about 60 species of shrubs from 3-20 ft (1-6 m) tall, native to North America, Central America, Asia and (locally) in southeast Europe.\n\n[Mock orange]\nMock orange or mock-orange typically means \"Philadelphus\", a mostly Holarctic genus of shrubs, particularly the species \"Philadelphus coronarius\" which is widely cultivated as an ornamental.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q803f860fdb",
  "kind": "yes/no",
  "text": "Claim: This publication is published more often than Bookmarks. Keith Moon was inducted into its Hall of Fame in the early 'eighties.\n\nPassages:\n\n[Modern Drummer]\nModern Drummer is a monthly publication targeting the interests of drummers and percussionists.\n\n[Keith Moon]\nHe was posthumously inducted into the \"Modern Drummer\" Hall of Fame in 1982, becoming only the second rock drummer to be chosen, and in 2011, Moon was voted the second-greatest drummer in history by a \"Rolling Stone\" readers' poll.\n\n[Bookmarks (magazine)]\nBookmarks is a bimonthly American literary magazine dedicated to general readers, book groups, and librarians.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q74f80c66b8",
  "kind": "yes/no",
  "text": "Claim: The broadcaster for The St Louis Cardinals team is the father of the broadcaster of The 2010 Major League Baseball All-Star Game.\n\nPassages:\n\n[Joe Buck]\nJoseph Francis \"Joe\" Buck (born April 25, 1969) is an American sportscaster and the son of sportscaster Jack Buck.\n\n[2010 Major League Baseball All-Star Game]\nThe game was held on July 13, 2010, at Angel Stadium of Anaheim, the home of the American League Los Angeles Angels of Anaheim, and was telecast by Fox Sports in the USA, with Joe Buck and Tim McCarver in the broadcast booth.\n\n[Bob Buck]\nHe was the younger brother of late St. Louis Cardinals radio broadcaster Jack Buck, and was the uncle of national television sportscaster Joe Buck.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q4aada72c0f",
  "kind": "yes/no",
  "text": "Claim: The religious scholar who analyzed the Ben Sira scroll added portions to a book of the Bible written by the author on the inspiration of his father Joshua.\n\nPassages:\n\n[Sirach]\nThe Book of the All-Virtuous Wisdom of Joshua ben Sira, commonly called the Wisdom of Sirach or simply Sirach, and also known as the Book of Ecclesiasticus (abbreviated Ecclus.) or Ben Sira, is a work of ethical teachings, from approximately 200 to 175 BCE, written by the Jewish scribe Ben Sira of Jerusalem, on the inspiration of his father Joshua son of Sirach, sometimes called Jesus son of Sirach or Yeshua ben Eliezer ben Sira.\n\n[Roy Kinneer Patteson, Jr.]\nDr. Roy Kinneer Patteson, Jr. was an American scholar whose knowledge of Biblical Hebrew, Aramaic, Syriac and Hellenistic Greek enabled him to undertake an analysis of the text of the Ben Sira Scroll discovered at Masada in Palestine in 1964. His research resulted in the establishment of a critical Hebrew text for portions of the first-century B.C. book, Sirach.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q551196de6e",
  "kind": "yes/no",
  "text": "Post: The Invisible Man was pretty good, liked it! Excited/scared to finally watch Deerskin, the last movie I planned to see in a theater before covid killed that hope. #HBOMax",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qbd846be387",
  "kind": "yes/no",
  "text": "Claim: This 72-78 passenger aircraft has parking spaces at Nakhon Si Thammarat Airport in Malyasia, which is a Total space of 2,902,400 square meters.\n\nPassages:\n\n[ATR 72]\nThe number \"72\" in its name is derived from the aircraft's standard seating configuration in a passenger-carrying configuration, which could seat 72-78 passengers in a single-class arrangement.\n\n[Nakhon Si Thammarat Airport]\nTotal space, 2,902,400 square meters.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8c22b12d24",
  "kind": "yes/no",
  "text": "Text: 2 x sand eating toddlers for sale. No previous owners. DM for details x",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qb41f979bd5",
  "kind": "yes/no",
  "text": "Post: @WalesOnline Riveting news.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q62ba69fea8",
  "kind": "yes/no",
  "text": "Claim: Southern Africa has a distribution of both the Ternstroemia and the genus of plants that Seemannaralia gerrardii was originally included in.\n\nPassages:\n\n[Ternstroemia]\nIt is distributed in tropical and subtropical regions in Africa, Asia, and the Americas.\n\n[Seemannaralia gerrardii]\nIt was originally included in genus \"Cussonia\".\n\n[Cussonia]\nIt originated in Africa and has its center of distribution in South Africa and the Mascarene Islands.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q87d9e105cc",
  "kind": "yes/no",
  "text": "Claim: The Miss Universe 2015 was held at a venue inside a casino in Las Vegas. This venue is located in a casino that is owned and operated by Dubuque Greyhound Park & Casino.\n\nPassages:\n\n[The AXIS]\nThe AXIS (known as The AXIS powered by Monster for sponsorship purposes, also referred to as the AXIS Theater) is a mid-sized auditorium located at Planet Hollywood Las Vegas on the Las Vegas Strip.\n\n[Planet Hollywood Las Vegas]\nIt is owned and operated by Caesars Entertainment Corporation.\n\n[Miss Universe 2015]\nMiss Universe 2015, the 64th Miss Universe pageant, was held on 20 December 2015 at The AXIS in Las Vegas, Nevada, United States.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q352dbd0e32",
  "kind": "yes/no",
  "text": "Claim: Josh Trank and Mike Valerio both work in the entertainment industry.\n\nPassages:\n\n[Mike Valerio]\nMike Valerio is an award-winning writer, producer, director, and executive in the entertainment industry for over 20 years.\n\n[Josh Trank]\nJoshua Benjamin \"Josh\" Trank (born February 19, 1984) is an American film director, screenwriter, and editor.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb8636fe840",
  "kind": "yes/no",
  "text": "Tweet: I love how men know they have a baby on the way in one month and they decide to go out and buy a brand new mustang wow",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q7ac23a9eb4",
  "kind": "yes/no",
  "text": "Post: Sometimes I really feel like I need coffee to survive the day and I think that's what growing up is",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q629530a97e",
  "kind": "yes/no",
  "text": "Claim: Pitchfork referenced the name of this drummer in a review of the percussion by Carla Azar on the album Future Perfect. The bandmate of the keyboardist, who also worked with Nika Boon, is also a drummer.\n\nPassages:\n\n[Future Perfect]\nA Pitchfork review stated, \"In the first 10 seconds of the album opener, Carla Azar shames most every beat-maker with her ridiculous Leibezeit-cum-Bonham percussion\".\n\n[Nika Boon]\nShe is currently working on her new album (release 2017) in collaboration with musicians namely John Baggott (who plays keyboard & moogs for Massive Attack, Portishead, Robert Plant), Ian Matthews (drummer from Kasabian), Jay Stapley (guitarist associated with Pink Floyd and Mike Oldfield) and Carey Willetts (bass player from band Athlete).\n\n[Robert Plant discography]\nAlthough Plant avoided performing Led Zeppelin songs through much of this period, his tours in 1983 (with drummer Phil Collins) and 1985 were very successful, often performing to sold-out arena-sized venues.\n\n[John Bonham]\nJohn Henry Bonham (31 May 1948 – 25 September 1980) was an English musician and songwriter, best known as the drummer for the British rock band Led Zeppelin.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf40aee878d",
  "kind": "yes/no",
  "text": "Claim: The poem Desiderata by this writer born in September 1872 was used in devotional and spoken word recordings.\n\nPassages:\n\n[Max Ehrmann]\nMax Ehrmann (September 26, 1872 – September 9, 1945) was an American writer, poet, and attorney from Terre Haute, Indiana, widely known for his 1927 prose poem \"Desiderata\" (Latin: \"things desired\").\n\n[Desiderata]\n\"Desiderata\" (Latin: \"desired things\") is a 1927 prose poem by American writer Max Ehrmann. Largely unknown in the author's lifetime, the text became widely known after its use in devotional and spoken-word recordings in 1971 and 1972.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7810df30c2",
  "kind": "yes/no",
  "text": "Text: Thoroughly enjoyed my first TeachMeet! Would definitely recommend it. It's like a teacher version of #TEDTalks @TeachMeetLeics",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qac75bc345a",
  "kind": "yes/no",
  "text": "Claim: The film that was the prequel to another movie came before Candleshoe. Winifred Deforest Coffin appeared in this other movie.\n\nPassages:\n\n[Winifred Deforest Coffin]\nCoffin was an actress who appeared in Hollywood films (\"Now You See Him, Now You Don't\"), and many television shows including \"Adam-12\", \"The Doris Day Show\", \"The Debbie Reynolds Show\", \"Lancer\", \"The Beverly Hillbillies\", \"High Chaparral\", \"Death Valley Days\", \"Petticoat Junction\", \"Perry Mason\", \"Bonanza\", \"Bewitched\", \"Honey West\", \"The Ann Sothern Show\".\n\n[The Strongest Man in the World]\nThe Strongest Man in the World is a 1975 Disney film starring Kurt Russell, still a student in the fictional Medfield College.\n\n[Candleshoe]\nCandleshoe is a 1977 American family adventure film produced by Walt Disney Productions based on the Michael Innes novel \"Christmas at Candleshoe\" and starring Jodie Foster, David Niven, Helen Hayes in her last big screen appearance and Leo McKern.\n\n[Now You See Him, Now You Don't]\nIt is the sequel to the 1969 film \"The Computer Wore Tennis Shoes\" and was followed by 1975's \"The Strongest Man in the World\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qfc139fcba7",
  "kind": "yes/no",
  "text": "Post: first day of work, and i’ve already cried on the job 👍",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q41896784d0",
  "kind": "yes/no",
  "text": "Claim: There were ten episodes made for the science heroes series with Gus Birney.\n\nPassages:\n\n[The Mist (TV series)]\nThe Mist is an American science fiction-horror thriller television series developed by Christian Torpe for Spike. The first season, consisting of ten episodes, premiered on June 22, 2017. On September 27, 2017, Spike cancelled the series after one season.\n\n[Gus Birney]\nGus Birney is an American actress, best known for her role as Alex in \"The Mist\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3de09ae34d",
  "kind": "yes/no",
  "text": "Tweet: Ah gotta love that Friday morning burnt out feeling 🌄",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qd89e8c3ce6",
  "kind": "yes/no",
  "text": "Post: too many dudes are wearing birks with socks on. grow up. get the fucking toes out man.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q5b0a9d80b3",
  "kind": "yes/no",
  "text": "Claim: In between Splash and Son of Flubber, the first one was directed by Ron Howard.\n\nPassages:\n\n[Splash (film)]\nSplash is a 1984 American fantasy romantic comedy film directed by Ron Howard, written by Lowell Ganz and Babaloo Mandel, and starring Tom Hanks, Daryl Hannah, John Candy, and Eugene Levy.\n\n[Son of Flubber]\nSon of Flubber is the 1963 sequel to the Walt Disney children's sci-fi comedy movie \"The Absent-Minded Professor\" (1961).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q37826ebb19",
  "kind": "yes/no",
  "text": "Tweet: Avoid mass gatherings.. does this mean that I can stay home tomorrow as I work at a school? No I thought not. #schoolclosure",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q09992a5304",
  "kind": "yes/no",
  "text": "Claim: This area is located just north of a constituent college of the University of a city. It stands across from the Bear Inn in the city. Heinz Cassirer lectured and lived in the city.\n\nPassages:\n\n[Christ Church, Oxford]\nChrist Church (Latin: \"Ædes Christi\" , the temple or house, \"ædēs\", of Christ, and thus sometimes known as \"The House\") is a constituent college of the University of Oxford in England.\n\n[Bear Lane]\nThe lane is located just north of Christ Church.\n\n[Heinz Cassirer]\nFollowing Paton, he moved to Oxford, lecturing at Corpus Christi College.\n\n[Bear Inn, Oxford]\nIts circa-17th century incarnation stands on the corner of Alfred Street and Blue Boar Street, opposite Bear Lane in the centre of Oxford, just north of Christ Church.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qd73cf18e3f",
  "kind": "yes/no",
  "text": "Claim: Gretchen Gotay graduated from the University of Georgia, an American public research university, which is located 72 miles northeast of Atlanta.\n\nPassages:\n\n[Gretchen Gotay]\nShe is a member of Athens Bulldogs Swim Club under her personal coach Harvey Humphries, and a graduate with a master's degree in sports management at the University of Georgia in Athens.\n\n[University of Georgia]\nThe University of Georgia, also referred to as UGA or simply Georgia, is an American public research university. Its main 762 acres campus is located in Athens, Georgia, approximately 72 mile northeast of Atlanta.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q1e6547a7cf",
  "kind": "yes/no",
  "text": "Claim: Thomas Ritter is a retired German footballer who played one game for Uruguay in 1993 against Uruguay, as a substitute for Stefan Effenberg, a retired German footballer who last managed SC Paderborn.\n\nPassages:\n\n[Stefan Effenberg]\nStefan Effenberg (] ; born 2 August 1968) is a retired German footballer who last managed SC Paderborn.\n\n[Thomas Ritter]\nThomas Ritter (born 10 October 1967 in Görlitz) is a retired German footballer. He played one game for Germany on 13 October 1993 in a friendly against Uruguay, as a substitute for Stefan Effenberg.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3d012792d4",
  "kind": "yes/no",
  "text": "Claim: A Shoulder-fired missile is a rocket propelled weapon, sometimes referred to as the \"Stovepipe\". Colonel Leslie Alfred Skinner helped develop the weapon in 1976.\n\nPassages:\n\n[Leslie Skinner]\nHe played a leading role in the development of several rocket propelled weapons during World War II, notably the first shoulder-fired missile system, the Bazooka.\n\n[Shoulder-fired missile]\nIn many instances, although not technically defining all shoulder-fired missiles, the name Bazooka is used as an informal name regularly, although the actual Bazooka is a type of original shoulder-fired missile in its own right.\n\n[Bazooka]\nAlso referred to as the \"Stovepipe\", the innovative bazooka was among the first generation of rocket-propelled anti-tank weapons used in infantry combat.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q409b7478eb",
  "kind": "yes/no",
  "text": "Claim: King of Tokyo has more game rooms than Tsuro.\n\nPassages:\n\n[Tsuro]\nTsuro is a tile-based board game designed by Tom McMurchie, originally published by WizKids and now published by Calliope Games.\n\n[King of Tokyo]\nKing of Tokyo is a tabletop game using custom dice, cards, and boards, designed by Richard Garfield and released in 2011.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1cb4bf3257",
  "kind": "yes/no",
  "text": "Claim: The star of Into the Dalek also played the role of Mr Curry in Paddington 2 .\n\nPassages:\n\n[Peter Capaldi]\nPeter Dougan Capaldi (born 14 April 1958) is a Scottish actor, writer and director, best known for playing the twelfth incarnation of the Doctor in \"Doctor Who\" and as spin doctor Malcolm Tucker in \"The Thick of It\", for which he has received four British Academy Television Award nominations, winning Best Male Comedy Performance in 2010. He further took on the role of Paddington Bear's neighbour Mr. Curry in the family comedy film \"Paddington\"; he is set to reprise the role in \"Paddington 2\".\n\n[Into the Dalek]\nStarring Peter Capaldi and Jenna Coleman the episode also introduces Samuel Anderson as Danny Pink.\n\n[Paddington 2]\nPaddington 2 is an upcoming British-French family-comedy film directed by Paul King, co written by King and Simon Farnaby, and produced by David Heyman. The film is set to release on 10 November 2017.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0fdfb5ad0e",
  "kind": "yes/no",
  "text": "Claim: Both the character, who is sometimes called the \"Mad Hatter\", and March Hare are characters in the book Alice's Adventures in Wonderland.\n\nPassages:\n\n[Mad Hatter (comics)]\nHe is modeled after the Hatter from the lunacy of Lewis Carroll's novel, \"Alice's Adventures in Wonderland\", a character often called the \"Mad Hatter\" in adaptations of Carroll.\n\n[Hatter (Alice's Adventures in Wonderland)]\nThe Hatter is a fictional character in Lewis Carroll's \"Alice's Adventures in Wonderland\" and its sequel \"Through the Looking-Glass\".\n\n[March Hare]\nThe March Hare (called Haigha in \"Through the Looking-Glass\") is a character most famous for appearing in the tea party scene in Lewis Carroll's \"Alice's Adventures in Wonderland\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q7c66ccdb84",
  "kind": "yes/no",
  "text": "Claim: The fairy Queen Mab orginated with William Shakespeare.\n\nPassages:\n\n[Maeve]\nIt is also associated with the fairy queen Queen Mab of Irish and English legend.\n\n[Queen Mab]\nQueen Mab (pronunciation: \"M/ă/v\") is a fairy referred to in William Shakespeare's play \"Romeo and Juliet\", where \"she is the fairies' midwife.\"",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf4fe517278",
  "kind": "yes/no",
  "text": "Claim: Neither the director of the 1943 film \"Young and Willing\" nor Edward Burns are from Germany.\n\nPassages:\n\n[Edward Burns]\nEdward Fitzgerald Burns (born January 29, 1968) is an American actor, film producer, writer, and director best known for appearing in several films including \"Saving Private Ryan\" (1998), \"15 Minutes\" (2001), \"Life or Something Like It\" (2002), \"A Sound of Thunder\" (2005), \"The Holiday\" (2006), \"One Missed Call\" (2008), \"27 Dresses\" (2008), \"Man on a Ledge\" (2012), \"Friends with Kids\" (2012), and \"Alex Cross\" (2012).\n\n[Edward H. Griffith]\nEdward H. Griffith (August 23, 1888 – March 3, 1975) (\"Also Known As: E H Griffith, Lieut. Edward H. Griffith, Edward Griffith, E. H. Griffith\") was an American motion picture director, screenwriter, and producer.\n\n[Young and Willing]\nYoung and Willing is a 1943 American comedy film produced and directed by Edward H. Griffith and starring William Holden, Eddie Bracken, Robert Benchley, and Susan Hayward.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4f832a3d92",
  "kind": "yes/no",
  "text": "Claim: Nelson Pereira dos Santos is a television and film director. So is the director of the movie Oscar Núñez played in, in 2000.\n\nPassages:\n\n[Nine Queens]\nNine Queens (Spanish: Nueve Reinas ) is a 2000 Argentine crime drama film written and directed by Fabián Bielinsky and starring Ricardo Darín, Gastón Pauls, Leticia Brédice, Tomás Fonzi and Alejandro Awada.\n\n[Nelson Pereira dos Santos]\nNelson Pereira dos Santos (born 22 October 1928) is a Brazilian film director.\n\n[Oscar Núñez]\nSome of his best known film credits included \"Nine Queens\" in 2000, \"Good Life Delivery\" in 2004, and \"Un novio para mi mujer\" in 2008.\n\n[Fabián Bielinsky]\nFabián Bielinsky (3 February 1959 – 28 June 2006) was an Argentine film director born in Buenos Aires.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3cba41eefe",
  "kind": "yes/no",
  "text": "Claim: The writer of the songs in All We Know Is Falling is younger than Terry Glaze.\n\nPassages:\n\n[Terry Glaze]\nTerrence Lee Glaze (born November 29, 1964, Columbus), known as Terry Lee, is a Texas-raised singer and guitarist who is most known for his work in American heavy metal bands Lord Tracy and Pantera.\n\n[All We Know Is Falling]\nAll songs were written by vocalist Hayley Williams and guitarist Josh Farro.\n\n[Hayley Williams]\nHayley Nichole Williams (born December 27, 1988) is an American singer, songwriter and musician. The band consists of Hayley Williams, Zac Farro and Taylor York.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qf3a74c89b3",
  "kind": "yes/no",
  "text": "Claim: Nick Goldsmith is half of the director/producer duo Hammer & Tongs. The other half and Lee Cheol-ha are both film writers and directors.\n\nPassages:\n\n[Hammer &amp; Tongs]\nHammer & Tongs is the pseudonym of British director and producer duo, promo and film director Garth Jennings and producer Nick Goldsmith, as well as the name of their production company.\n\n[Lee Cheol-ha]\nLee Cheol-ha is a South Korean film director known for his stylish portraits of the human experience.\n\n[Garth Jennings]\nGarth Jennings (born 1972) is a British film director, screenwriter, producer and actor.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb295667eef",
  "kind": "yes/no",
  "text": "Claim: A relative of Charles Kanaʻina inherited authority of a kind which is a belief in many myths.\n\nPassages:\n\n[Umi-a-Liloa]\nʻUmi-a-Līloa (fifteenth century) was a ruling ali'i-ai-moku (district high chief of Hawai'i) who inherited religious authority of Hawai'i from his father, High Chief Liloa, whose line is traced, unbroken to Hawaiian \"creation\".\n\n[Charles Kanaʻina]\nKanaʻina was a descendant of several figures from ancient Hawaiian history, including Liloa, Hakau and Umi-a-Liloa of Hawaiʻ i Island as well as Piilani of Maui.\n\n[Hawaiian religion]\nHawaiian religion encompasses the indigenous religious beliefs and practices of the Native Hawaiians. It is polytheistic and animistic, with a belief in many deities and spirits, including the belief that spirits are found in non-human beings and objects such as animals, the waves, and the sky.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qbeae309bca",
  "kind": "yes/no",
  "text": "Claim: Jon Mueller (baseball) is the coach of the baseball team which played in the championship game in 2009. This team is a member of the conference in which the 2015–16 Maine Black Bears women's basketball team will represent the University of Maine.\n\nPassages:\n\n[Albany Great Danes baseball]\nThe Albany Great Danes baseball team is a varsity intercollegiate athletic team of the University at Albany in Albany, New York, United States.\n\n[2009 America East Conference Baseball Tournament]\nIn the championship game, first-seeded Binghamton defeated second-seeded Albany, 16-6, to win its first tournament championship.\n\n[Jon Mueller (baseball)]\nJon Mueller (born January 26, 1970) is an American college baseball coach who has been the head coach of Albany since the start of the 2000 season.\n\n[2015–16 Maine Black Bears women's basketball team]\nThe 2015–16 Maine Black Bears women's basketball team will represent the University of Maine in the America East Conference.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q30ef4fb9e8",
  "kind": "yes/no",
  "text": "Post: where can I hand my notice in for mental illness? been working at the same thing for way too long and it’s time for a change.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qd72b882d8e",
  "kind": "yes/no",
  "text": "Claim: In the 2011 census the population of suburban area in which BA Connect is headquartered was 26,788.\n\nPassages:\n\n[BA Connect]\nHeadquartered in Didsbury, Manchester, England, it operated a network of domestic and European services from a number of airports in the United Kingdom on behalf of British Airways.\n\n[Didsbury]\nThe population at the 2011 census was 26,788.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qcfa0877e0a",
  "kind": "yes/no",
  "text": "Claim: the American Kennel Club of dens affects this dog breed. The breed that is affected and the breed Ronald Reagan's Rex (dog) was are kinds of dog.\n\nPassages:\n\n[Rex (dog)]\nRex (December 16, 1984 – August 31, 1998) was a Cavalier King Charles Spaniel owned by Ronald Reagan and his wife Nancy during his term as President of the United States.\n\n[Hypoplasia of dens]\nIt is more commonly seen in certain breeds, including the Chihuahua, the Papillon, the Pointer and the Yorkshire Terrier.\n\n[Cavalier King Charles Spaniel]\nThe Cavalier King Charles Spaniel is a small spaniel classed as a toy dog by The Kennel Club and the American Kennel Club.\n\n[Yorkshire Terrier]\nThe Yorkshire Terrier is a small dog breed of terrier type, developed during the 19th century in Yorkshire, England, to catch rats in clothing mills.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q75ebb9f579",
  "kind": "yes/no",
  "text": "Claim: Doggerland, an area that once connected Jutland to continental Europe, is thought to have been submerged around 6,200 BCE by a massive landslide along 290 km of the continental shelf.\n\nPassages:\n\n[Storegga Slide]\nThe three Storegga Slides are considered to be amongst the largest known landslides. The collapse involved an estimated 290 km length of coastal shelf, with a total volume of 3500 km3 of debris, which caused a very large tsunami in the North Atlantic Ocean.\n\n[Doggerland]\nDoggerland was an area now beneath the southern North Sea that connected Great Britain to continental Europe during and after the last glacial period. It was probably a rich habitat with human habitation in the Mesolithic period, although rising sea levels gradually reduced it to low-lying islands before its final submergence, possibly following a tsunami caused by the Storegga Slide.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc30ce0ddd9",
  "kind": "yes/no",
  "text": "Claim: On the 27 June 2013, the Aboriginal-Australian politician who has been a member of the Australian House of Representatives since 1996 was sworn into the 68th ministry of the Australian government.\n\nPassages:\n\n[Anthony Albanese]\nAnthony Norman Albanese ( ; born 2 March 1963) is an Australian politician who represents the Division of Grayndler for the Australian Labor Party as well as being the party's spokesperson on Infrastructure, Transport and Tourism. He has been a member of the Australian House of Representatives since 1996.\n\n[Second Rudd Ministry]\nThe Second Rudd Ministry (Labor) was the 68th ministry of the Australian government, led by Prime Minister Kevin Rudd. Three members of the ministry were sworn in by Governor-General Quentin Bryce on 27 June 2013. These were Kevin Rudd, Prime Minister; Anthony Albanese, Deputy Prime Minister; and Chris Bowen, Treasurer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q0d48102dfa",
  "kind": "yes/no",
  "text": "Text: Nice to see @Cardiffbus have started the new year off with the usual crap service. Just love waiting for a bus that doesn't turn up",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q75c1f68554",
  "kind": "yes/no",
  "text": "Claim: The singer and writer of the song \"Death Valley '69\" belonged to Sonic Youth. His bandmate and Michael Akerfeldt were guitarists in their respective bands.\n\nPassages:\n\n[Death Valley '69]\nThe song was written and sung by Thurston Moore and fellow New York musician Lunch, and recorded by Martin Bisi in 1984.\n\n[Thurston Moore]\nIn May 2012, \"Spin\" published a staff-selected top 100 ranking Moore and his Sonic Youth bandmate Lee Ranaldo together on number 1.\n\n[Lee Ranaldo]\nLee Mark Ranaldo (born February 3, 1956) is an American musician, singer-songwriter, guitarist, writer, visual artist and record producer, best known as a co-founder of the alternative rock band Sonic Youth. In 2004, \"Rolling Stone\" ranked Ranaldo at number 33 on its \"Greatest Guitarists of All Time\" list.\n\n[Mikael Åkerfeldt]\nLars Mikael Åkerfeldt (born 17 April 1974) is a Swedish musician, prominently known as the lead vocalist, guitarist, and primary songwriter of progressive death metal band Opeth, as well as being the former vocalist of death metal supergroup Bloodbath. He was also guitarist for the \"one-off\" band Steel, and is part of the collaboration Storm Corrosion with Steven Wilson.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
