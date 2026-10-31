# A46 replay label-noise blind read RSBS10-blind_read-93a61eb1-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS10-blind_read-93a61eb1-001.json

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
  "qid": "qeb5434f30a",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I could tell the person to go read up on some facts it may help there IQ",
   "@Chris_Ransom @CityView1904 @Uzzell01 @BBCSport Aware she was not a tennis player when she left Canada at 2 yrs old?? aware she did not pick up a tennis racket until 6 years old??.aware last12 years trained at the same tennis club in Bromley Kent England??the girl is British no haters or doubters will take that away from her"
  ]
 },
 {
  "qid": "q243479910e",
  "kind": "yes/no",
  "text": "Claim: A genus of plant with a radians species grows in Northern Cape in a country that speaks Dutch. It has more species than the Stenocarpus genus does. Sandlane is located close to the border with the country.\n\nPassages:\n\n[Sandlane]\nIt is located close to the border with South Africa, 40 kilometres southwest of the capital, Mbabane.\n\n[Stenocarpus]\nStenocarpus is a genus of about 25 species known to science, of woody trees or shrubs, constituting part of the plant family Proteaceae.\n\n[Geissorhiza]\nGeissorhiza is a genus of about 80 species of deciduous perennial flowering plants in the iris family first described as a genus in 1803.\n\n[Geissorhiza radians]\nGeissorhiza radians is an Geissorhiza species found growing in Northern Cape, South Africa.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q871fc42e43",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "\"People on the left should not agree with the right just to win points in debates with people in the centre.\"",
   "Agreeing with the right to dunk on the centre is the real dialectical materialism"
  ]
 },
 {
  "qid": "q1c9d96b8ab",
  "kind": "yes/no",
  "text": "Claim: The band which released the debut EP \"Son of Mustang Ford\" was formed before another band. This band released the song \"Megalomaniac\".\n\nPassages:\n\n[Megalomaniac (Incubus song)]\n\"Megalomaniac\" is a song by the American rock band Incubus, from their 2004 album \"A Crow Left of the Murder...\" It was released as a single in December 2003, and eventually reached the top of \"Billboard\"' s Modern Rock Tracks, where it stayed for a six-week period.\n\n[Incubus (band)]\nThe band was formed in 1991 by vocalist Brandon Boyd, lead guitarist Mike Einziger, and drummer Jose Pasillas while enrolled in Calabasas High School and later expanded to include bassist Alex \"Dirk Lance\" Katunich, and Gavin \"DJ Lyfe\" Koppell; both of whom were eventually replaced by bassist Ben Kenney and DJ Kilmore respectively.\n\n[Son of Mustang Ford]\nSon of Mustang Ford is the debut EP by English alternative rock band, Swervedriver.\n\n[Swervedriver]\nSwervedriver are an English alternative rock band formed in Oxford in 1989 around core members Adam Franklin and Jimmy Hartridge.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q870d058075",
  "kind": "yes/no",
  "text": "Tweet: @McDonaldsUK Would love a cheeky McDonald’s breakfast before a busy day at work would set the day off on the right foot ! 💓 #FancyAMcDonalds",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q6bf0186f0a",
  "kind": "yes/no",
  "text": "Claim: Monica Heller is a physics professor at the University of Toronto located in Toronto, Ontario, Canada.\n\nPassages:\n\n[Monica Heller]\nMonica Heller (born June 1955) is a Canadian linguistic anthropologist and Professor at the University of Toronto.\n\n[University of Toronto]\nThe University of Toronto (U of T, UToronto, or Toronto) is a public research university in Toronto, Ontario, Canada on the grounds that surround Queen's Park.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2e50a94bbf",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "@PlayStationUK Nice",
   "These aren't very good games"
  ]
 },
 {
  "qid": "q21275dd5f4",
  "kind": "yes/no",
  "text": "Claim: Television station KCTV, licensed to a city, is adjacent to another television station that broadcasts in French only. This other television station aired the programme \"Check Please!\". American football coach Tim Johnson was hired in this city.\n\nPassages:\n\n[KCPT]\nOwned by Public Television 19, Inc., KCPT maintains studio facilities (which are shared with sister adult album alternative radio station KTBG (90.9 FM)) located on East 31st Street in Kansas City, Missouri's Union Hill section (adjacent to the transmitter tower of CBS affiliate KCTV (channel 5)), and its transmitter is located near 23rd Street and Stark Avenue in Kansas City, Missouri's Blue Valley section.\n\n[KCTV]\nKCTV, virtual channel 5 (UHF digital channel 24), is a CBS-affiliated television station licensed to Kansas City, Missouri, United States and also serving Kansas City, Kansas.\n\n[Tim Johnson (American football coach)]\nIn 1999 Johnson was hired by Avila University in Kansas City, Missouri to start the school's football program.\n\n[Check, Please!]\nKansas City then began airing on KCPT in 2009, and Check, Please!",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe20f9f4706",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "Someone should’ve had me committed the day I decided to buy a pair of non-stretch denim jeans",
   "I hate non-stretch denim jeans."
  ]
 },
 {
  "qid": "qfb5e6ca27b",
  "kind": "yes/no",
  "text": "Claim: This borough is the location of Flushing Meadows–Corona Park. It had a bigger population in the 2016 census than than the borough that Charles W. Leng was the borough historian of from 1923 until the 1930s.\n\nPassages:\n\n[Charles W. Leng]\nCharles William Leng (1859 – 1941) was an American naturalist and historian especially associated with Staten Island, New York, where he was the borough historian from 1923 until the 1930s.\n\n[Flushing Meadows–Corona Park]\nLocated in the borough of Queens, it is between I-678 (Van Wyck Expressway) and the Grand Central Parkway and stretches from Flushing Bay, at the southern edge of LaGuardia Airport, to Union Turnpike.\n\n[Staten Island]\nWith a 2016 Census-estimated population of 476,015, Staten Island is the least populated of the boroughs but is the third-largest in area at 58 sqmi .\n\n[Queens]\nCoterminous with Queens County since 1899, the borough of Queens is the second-largest in population (after Brooklyn), with a census-estimated 2,333,054 residents in 2016, approximately 48% of them foreign-born.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q7aa8a5b18f",
  "kind": "yes/no",
  "text": "Claim: Angostura bitters and Springbokkie are an unknown mixture.\n\nPassages:\n\n[Springbokkie]\nThe Springbokkie (\"little Springbok\" in the Afrikaans language), composed of creme de menthe (\"or substitutes\") and Amarula, is a cocktail shooter that is popular in South Africa.\n\n[Angostura bitters]\nAngostura bitters ( ) is a concentrated bitters, or botanically infused alcoholic mixture, made of water, 44.7% ethanol, gentian, herbs and spices, by House of Angostura in Trinidad and Tobago.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q370f81c190",
  "kind": "yes/no",
  "text": "Claim: Comic Court was the name of the Australian bred Thoroughbred racehorse who won Australia's most prestigious annual Thoroughbred horse race in 1950.\n\nPassages:\n\n[Comic Court]\nComic Court (1945–1973) was a most versatile post-war Australian bred Thoroughbred racehorse who set race records at distances of 6 furlongs (1,200 metres) and 2 miles (3,200 metres). He won the 1950 Melbourne Cup carrying 9 st and set an Australasian record of 3 minutes 19½ seconds.\n\n[Melbourne Cup]\nThe Melbourne Cup is Australia's most prestigious annual Thoroughbred horse race.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q47eb05c139",
  "kind": "yes/no",
  "text": "Claim: The end of the reign of the Queen for whom the TV series \"Reign\" is based on was in 24 July 1567.\n\nPassages:\n\n[Reign (season 1)]\nThe series follows the early exploits of Mary, Queen of Scots, and was created by Stephanie SenGupta and Laurie McCarthy.\n\n[Mary, Queen of Scots]\nMary, Queen of Scots (8 December 1542 – 8 February 1587), also known as Mary Stuart or Mary I, reigned over Scotland from 14 December 1542 to 24 July 1567.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q76163f3a5d",
  "kind": "yes/no",
  "text": "Claim: Of Vladimir Voevodsky and Anatoly Maltsev, Anatoly Ivanovich Maltsev was married first.\n\nPassages:\n\n[Anatoly Maltsev]\nAnatoly Ivanovich Maltsev (also: Malcev, Mal'cev; Russian: Анато́лий Ива́нович Ма́льцев; 27 November N.S./14 November O.S. 1909, Moscow Governorate – 7 June 1967, Novosibirsk) was born in Misheronsky, near Moscow, and died in Novosibirsk, USSR.\n\n[Vladimir Voevodsky]\nVladimir Alexandrovich Voevodsky ( ; Russian: Влади́мир Алекса́ндрович Воево́дский , 4 June 1966 - 30 September 2017) was a Russian mathematician.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q8ded60f043",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "If you are taking part in this dumb trend it's not very funny.",
   "Fav this and I won't send you a name of a random person, I'll just get a fav on my tweet"
  ]
 },
 {
  "qid": "q3f351cd7f6",
  "kind": "yes/no",
  "text": "Claim: Johnson & Johnson, a company founded in 1886, has owned the K-Y brand.\n\nPassages:\n\n[K-Y Jelly]\nIn March 2014, Reckitt Benckiser agreed to buy the K-Y brand from Johnson & Johnson.\n\n[Johnson &amp; Johnson]\nJohnson & Johnson is an American multinational medical devices, pharmaceutical and consumer packaged goods manufacturing company founded in 1886.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc2e7123c3f",
  "kind": "yes/no",
  "text": "Claim: \"A Swingin' Safari\" was a song written originally by German songwriter Bert Kaempfert but made popular by Billy Vaughn.\n\nPassages:\n\n[Bert Kaempfert]\nBerthold Heinrich Kämpfert, (16 October 1923 – 21 June 1980), better known as Bert Kaempfert, was a German orchestra leader, music producer, and songwriter.\n\n[A Swingin' Safari]\nThat same year, Billy Vaughn recorded it, and his cover reached number 13 on the \"Billboard\" charts that summer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qd52b69d591",
  "kind": "yes/no",
  "text": "Post: I wish i loved my body",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q9ca9b1b55f",
  "kind": "yes/no",
  "text": "Text: @kagune_kun despicable tweet, my liege",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qe060831d14",
  "kind": "yes/no",
  "text": "Claim: December 7 is the release date of the film in which Noah Lomax played the character Dennis Quaid.\n\nPassages:\n\n[Noah Lomax]\nAmong his prominent roles are: Lewis in the film \"Playing for Keeps\", Josh in the film \"Safe Haven\", and Louis Morales in the TV series \"The Walking Dead\".\n\n[Playing for Keeps (2012 film)]\nThe film was released on December 7, 2012, in the United States and Canada by FilmDistrict.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q48b0960d6d",
  "kind": "yes/no",
  "text": "Text: ITS COMING HOOOOOME",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q1a03c49213",
  "kind": "yes/no",
  "text": "Claim: The classical composer of Lento was English.\n\nPassages:\n\n[Howard Skempton]\nHoward While Skempton (born 31 October 1947) is an English composer, pianist, and accordionist.\n\n[Lento (Skempton)]\nLento is a composition for orchestra written by Howard Skempton in 1990.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb242ffd2e7",
  "kind": "yes/no",
  "text": "Claim: Leslie Dowdall, an American actress, is from a village in County Dublin. John Carney directed a 2016 musical filmed there.\n\nPassages:\n\n[Leslie Dowdall]\nLeslie Dowdall is an Irish singer-songwriter from Howth, County Dublin.\n\n[Sing Street]\nSing Street is a 2016 musical coming-of-age comedy-drama film co-written, co-produced and directed by John Carney.\n\n[Howth]\nHowth has been a filming location for movies such as \"The Last of the High Kings\", \"Boy Eats Girl\" and \"Sing Street\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q27a2002975",
  "kind": "yes/no",
  "text": "Claim: The film, in which Kirsten Olson played Nikki Fletcher, is directed by Tim Fywell, included the actress who also appeared in \"Euro Trip\" and \"Inspector Gadget\".\n\nPassages:\n\n[Ice Princess]\nIce Princess is a 2005 American figure-skating film directed by Tim Fywell, written by Hadley Davis from a story by Meg Cabot and Davis, and starring Michelle Trachtenberg, Joan Cusack, Kim Cattrall and Hayden Panettiere.\n\n[Kirsten Olson]\nAs an actress, Olson played the role of Nikki Fletcher, the 'Jumping Shrimp,' in the Disney movie \"Ice Princess\" (2005).\n\n[Michelle Trachtenberg]\nShe has also appeared in films such as \"Harriet the Spy\" (1996), \"Inspector Gadget\" (1999), \"EuroTrip\" (2004), \"Ice Princess\" (2005), \"Black Christmas\" (2006), \"17 Again\" (2009), \"Cop Out\" (2010), \"Weeds\" (2011), and \"Killing Kennedy\" (2013).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa88c9036bf",
  "kind": "yes/no",
  "text": "Claim: This person worked on the American horror film The Nightcomers. Like the filmmaker who directed and edited The Raid 2 this person is also a director.\n\nPassages:\n\n[Gareth Evans (director)]\nGareth Huw Evans (born 1980) is a Welsh film director, screenwriter, film editor and action choreographer.\n\n[The Raid 2]\nIt is the sequel to his 2011 film \"The Raid\".\n\n[The Nightcomers]\nThe Nightcomers is a 1971 British horror film directed by Michael Winner and starring Marlon Brando, Stephanie Beacham, Thora Hird, Harry Andrews and Anna Palk.\n\n[Michael Winner]\nRobert Michael Winner (30 October 1935 – 21 January 2013) was an English film director and producer, and a restaurant critic for \"The Sunday Times\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q1681d4d801",
  "kind": "yes/no",
  "text": "Claim: The high-performance aftermarket tuning company specializes in German automotive marque Smart. The company designed an automobile drivetrain similar to the Smart Forstars.\n\nPassages:\n\n[Brabus]\nBRABUS GmbH, founded 1977 in Bottrop (Ruhr Area), Germany, is a high-performance aftermarket tuning company which specializes in Mercedes-Benz, Smart, Tesla and Maybach vehicles.\n\n[Smart (marque)]\nsmart Automobile (stylized and marketed as \"smart\") is a German automotive marque and division of Daimler AG, based in Böblingen, Germany.\n\n[Smart Forstars]\nIt also has an all-electric drivetrain, which is nearly identical to the one used in the Smart Brabus electric drive.\n\n[Brabus Bullit]\nThe Brabus Bullit is an automobile designed and made by Brabus.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q635fa8d13a",
  "kind": "yes/no",
  "text": "Tweet: I love how men know they have a baby on the way in one month and they decide to go out and buy a brand new mustang wow",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qeb9081bab7",
  "kind": "yes/no",
  "text": "Claim: A mayor was the host of the game show Hoosier Millionaire. The death of the man led to the Tavistock by-election in 1942.\n\nPassages:\n\n[Powerball]\nPowerball is an American lottery game offered by 44 states, the District of Columbia, Puerto Rico and the US Virgin Islands.\n\n[Hoosier Lottery]\nIt is a member of the Multi-State Lottery Association (MUSL).\n\n[Tavistock by-election, 1942]\nThe by-election was held due to the death of the incumbent Conservative MP, Mark Patrick.\n\n[Mark Patrick]\nPatrick also hosted the Hoosier Lottery television game show Hoosier Millionaire for 14 years.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qcff6054cf4",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "My work email isn’t working so I can just log off for the day right? 🙄",
   "I wish I would log off for the day because my email isn't working."
  ]
 },
 {
  "qid": "qe020f8d171",
  "kind": "yes/no",
  "text": "Text: 2 x sand eating toddlers for sale. No previous owners. DM for details x",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qf9a86b8c62",
  "kind": "yes/no",
  "text": "Claim: Thee owner of the 165 acre drumlin or the mansion that sits on the hill donated $145,000 to the construction fund for the Benjamin Stickney Cable Memorial Hospital.\n\nPassages:\n\n[Benjamin Stickney Cable Memorial Hospital]\nCrane purchased the land on which the building sits and made a further donation of $145,000 to the construction fund.\n\n[Castle Hill (Ipswich, Massachusetts)]\nCastle Hill refers to either a 165 acre drumlin surrounded by sea and salt marsh or to the mansion that sits on the hill.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa4c678d181",
  "kind": "yes/no",
  "text": "Claim: The Spitsbergen based seed bank, the Svalbard Global Seed Vault, serves to protects agricultural diversity in the far north, 1300 km from Wakehurst Place.\n\nPassages:\n\n[Agriculture in Svalbard]\nSvalbard is also home to the Global Seed Vault, which serves to protect the world's biological and agricultural diversity.\n\n[Svalbard Global Seed Vault]\nThe Svalbard Global Seed Vault (Norwegian: \"Svalbard globale frøhvelv\" ) is a secure seed bank on the Norwegian island of Spitsbergen near Longyearbyen in the remote Arctic Svalbard archipelago, about 1300 km from the North Pole.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q91b41925e8",
  "kind": "yes/no",
  "text": "Claim: The tennis player Kenneth or Ken Eliot Flach is from a country closer to Ontario Canada than the woman who defeated Maria Sharapova in the 2015 French Open- Women's Singles.\n\nPassages:\n\n[Ken Flach]\nKenneth Eliot Flach (born May 24, 1963) is a former professional tennis player from the United States.\n\n[2015 French Open – Women's Singles]\nMaria Sharapova was the defending champion, but lost in the fourth round to Lucie Šafářová.\n\n[Lucie Šafářová]\nLucie Šafářová (] ; born 4 February 1987) is a Czech professional tennis player from Brno.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q4178892593",
  "kind": "yes/no",
  "text": "Claim: Ronan was performed at an Arizona stop of the 1989 World Tour.\n\nPassages:\n\n[Ronan (song)]\nSwift first performed the song live for Stand Up to Cancer in September 2012, and has only performed it publicly one other time, at the Glendale, Arizona stop of The 1989 World Tour, at which Thompson was in attendance.\n\n[The 1989 World Tour]\nThe 1989 World Tour was the fourth concert tour by American singer-songwriter Taylor Swift, in support of her fifth studio album, \"1989\" (2014).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2520f771f8",
  "kind": "yes/no",
  "text": "Tweet: if jesus was resurrected again i would vote for him",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q79ada75982",
  "kind": "yes/no",
  "text": "Claim: The charter airport that is a 30-minute drive from Coldwaltham, is the busiest airport in the United Kingdom outside of London.\n\nPassages:\n\n[Heathrow Airport]\nHeathrow Airport (also known as London Heathrow) (IATA: LHR, ICAO: EGLL) is a major international airport in London, United Kingdom.\n\n[Gatwick Airport]\nGatwick Airport (also known as London Gatwick) (IATA: LGW, ICAO: EGKK) is a major international airport in south-east England, 29.5 mi south of Central London and 2.7 NM north of Crawley. It is the second-busiest airport by total passenger traffic in the United Kingdom, after London Heathrow.\n\n[Coldwaltham]\nIt is around a 30-minute drive from Gatwick Airport.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2576abd466",
  "kind": "yes/no",
  "text": "Claim: Save Me is a song by the group that was part of the genre that evolved from disco in 1978.\n\nPassages:\n\n[Euro disco]\nEuro disco (or Eurodisco) is the variety of European forms of electronic dance music that evolved from disco in the later 1970s; incorporating elements of pop, new wave and rock into a disco-like continuous dance atmosphere.\n\n[Save Me (Silver Convention song)]\n\"Save Me\" is a song by the German Euro disco group Silver Convention, which became a hit in Germany.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q01c02996d4",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "I don't think Republicans have any self awareness or any idea of how the world works... Nice try though.",
   "\"I really think that older Republicans are lacking in self-awareness in the modern-day. They had a complete misstep and just ended up bullying a teenager.\""
  ]
 },
 {
  "qid": "q66400cc75d",
  "kind": "yes/no",
  "text": "Claim: The creator of Yesterday Girl and Sidney Salkow are not of the same nationality.\n\nPassages:\n\n[Sidney Salkow]\nSidney Salkow (June 16, 1911 – October 18, 2000) was an American film director (more than 50 motion pictures), screenwriter, and television director.\n\n[Alexander Kluge]\nAlexander Kluge (born 14 February 1932) is a German author, philosopher, academic and film director.\n\n[Yesterday Girl]\nYesterday Girl (German: Abschied von gestern, \"Farewell to Yesterday\") is a 1966 New German Cinema film directed and written by Alexander Kluge.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q39c74641be",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "ah yes, of the course the summer rain pours when im on foot.",
   "\"why did it have to rain when im walking?\""
  ]
 },
 {
  "qid": "q8740056ad6",
  "kind": "yes/no",
  "text": "Claim: This series developer created T-Dog on the Walking Dead. He is the Hungarian-born US film director renowned for adapting Stephen King novellas to the screen, including The Mist and The Green Mile.\n\nPassages:\n\n[The Mist (film)]\nThe film was written and directed by Frank Darabont.\n\n[T-Dog (The Walking Dead)]\n\"He was created by series developer Frank Darabont and portrayed by IronE Singleton.\n\n[Frank Darabont]\nAs a director he is known for his film adaptations of Stephen King novellas and novels such as \"The Shawshank Redemption\", \"The Green Mile\", and \"The Mist\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qcf3ae27897",
  "kind": "yes/no",
  "text": "Tweet: Dunno what’s worse us losing or this covid that’s riddled all over me body",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qec885cc77e",
  "kind": "yes/no",
  "text": "Text: Day 3. Luggage arrived, thanks @AirFranceFR. Non random Hungarian underwear. Talk delivered. Science sated. #metaxa http://t.co/6KPjLezQOF",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qb54f01701f",
  "kind": "yes/no",
  "text": "Post: OT OT",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q5cf8143129",
  "kind": "yes/no",
  "text": "Claim: Edwin Hewitt collaborated with another mathematician. An American person said the this other mathematician was \"one of the few people I have met whom I would unhesitatingly call a genius\".\n\nPassages:\n\n[Milton Friedman]\nMilton Friedman ( ; July 31, 1912 – November 16, 2006) was an American economist who received the 1976 Nobel Memorial Prize in Economic Sciences for his research on consumption analysis, monetary history and theory, and the complexity of stabilization policy.\n\n[Leonard Jimmie Savage]\nEconomist Milton Friedman said Savage was \"one of the few people I have met whom I would unhesitatingly call a genius.\"\n\n[Edwin Hewitt]\nEdwin Hewitt (January 20, 1920, Everett, Washington – June 21, 1999) was an American mathematician known for his work in abstract harmonic analysis and for his discovery, in collaboration with Leonard Jimmie Savage, of the Hewitt–Savage zero–one law.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc131901f5b",
  "kind": "yes/no",
  "text": "Claim: The band who had King ov Hell as a member are based in the Norwegian county Hordaland.\n\nPassages:\n\n[Gorgoroth]\nGorgoroth is a Norwegian black metal band based in Bergen.\n\n[King ov Hell]\nHe is best known as the former bassist of black metal band Gorgoroth, but he is also the co-founder of Ov Hell, God Seed, Jotunspor, Audrey Horne, Sahg, I and Temple of the Black Moon.\n\n[Bergen]\nBergen, historically Bjørgvin, is a city and municipality in Hordaland on the west coast of Norway.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q80eb9c7ffc",
  "kind": "yes/no",
  "text": "Claim: The film that featured Nico Liersch in the role of Rudy Steiner was directed by same director of the film About a Girl. That film is based on a young adult novel by Markus Zusak.\n\nPassages:\n\n[Nico Liersch]\nHe is mostly known for his role as Rudy Steiner in the 2013 film \"The Book Thief\".\n\n[The Book Thief (film)]\nThe film is based on the 2005 novel \"The Book Thief\" by Markus Zusak and adapted by Michael Petroni.\n\n[Brian Percival]\nBrian Percival is a British film director, known for his work on the British television series \"Downton Abbey\" and \"North & South\", as well as the feature film \"The Book Thief\".\n\n[About a Girl (2001 film)]\nAbout a Girl is a nine-minute short film directed by Brian Percival.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa82d4dd734",
  "kind": "yes/no",
  "text": "Claim: 69 Love Songs are Irish. The singer who formed a group with Kid Montana is also Irish.\n\nPassages:\n\n[Kid Montana]\nFollowing this, he was joined by American singer Dudley Kludt (The Magnetic Fields, Flare Acoustic Arts League) for the remainder of the group's lifetime.\n\n[LD Beghtol]\nLD Beghtol (born 1964, Fort Campbell, Kentucky) is an American musician, art director and writer.\n\n[69 Love Songs]\n69 Love Songs is the sixth studio album by American indie pop band The Magnetic Fields, released on September 7, 1999 by Merge Records.\n\n[Flare Acoustic Arts League]\nFlare Acoustic Arts League — a.k.a. Flare (band) — were an experimental pop band formed by guitarist Damian Costilla and singer LD Beghtol in New York in 1996 who made intense, darkly romantic, atmospheric songs deeply influenced by their love of The Smiths, The Magnetic Fields (with whom beghtol sometimes collaborated), Love, various 4AD bands and The Velvet Underground.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q1154914a3f",
  "kind": "yes/no",
  "text": "Claim: Teenager Emilio Sánchez appeared in the Olympics before one of the defending champions of the 2000 Stockholm Open - Doubles.\n\nPassages:\n\n[Piet Norval]\nThe right-hander represented his native country in the doubles competition at the 1992 Summer Olympics in Barcelona, where he partnered Wayne Ferreira.\n\n[Emilio Sánchez]\nHe won three Grand Slam doubles titles and the men's doubles silver medal at the 1988 Olympic Games. Sanchez since retiring captained his nation to Davis Cup success in 2008. In 2012 Sanchez was a tournament director for two wheelchair tennis events.\n\n[2000 Stockholm Open – Doubles]\nPiet Norval and Kevin Ullyett were the defending champions, but lost in the semifinals this year.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3ff7e584a6",
  "kind": "yes/no",
  "text": "Claim: The host of the show that featured LA Urban Rangers provided the voices of Backson and Fluffy in Disney's 51st Disney animated feature film.\n\nPassages:\n\n[Huell Howser]\nHuell Burnley Howser (October 18, 1945 – January 7, 2013) was an American television personality, actor, producer, writer, singer, and voice artist, best known for hosting, producing, and writing \"California's Gold\", his human interest show produced by KCET in Los Angeles for California PBS stations. He also voiced the Backson in \"Winnie the Pooh\" (2011).\n\n[Winnie the Pooh (2011 film)]\nIt is the 51st Disney animated feature film.\n\n[LA Urban Rangers]\nTheir most recent and longest-running outing - the Malibu Public Beach Safari - has been featured in media reports and by Huell Howser on his show.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
