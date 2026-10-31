# A46 replay label-noise blind read RSAS07-blind_read-95379c1f-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS07-blind_read-95379c1f-002.json

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
  "qid": "qa3494cbad8",
  "kind": "yes/no",
  "text": "Claim: The star of The Big Caper was known for playing a fictionalized version of the wild politician who was the face of communist scare tact's in the early 1950's.\n\nPassages:\n\n[James Gregory (actor)]\nJames Gregory (December 23, 1911 – September 16, 2002) was an American character actor known for his deep, gravelly voice and playing brash roles such as the McCarthy-like Sen. John Iselin in \"The Manchurian Candidate\" (1962), the audacious General Ursus in \"Beneath the Planet of the Apes\" (1970), and crusty Inspector Frank Luger in the television sitcom \"Barney Miller\" (1975–1982).\n\n[The Big Caper]\nThe Big Caper is a 1957 crime drama film noir directed by Robert Stevens starring Rory Calhoun, Mary Costa and James Gregory\n\n[Joseph McCarthy]\nBeginning in 1950, McCarthy became the most visible public face of a period in the United States in which Cold War tensions fueled fears of widespread Communist subversion.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qbfb2c70699",
  "kind": "yes/no",
  "text": "Claim: The European city that Liu Xiwu was born in is in China. The county that is located where the old Quan (state) was once established is also in China.\n\nPassages:\n\n[Mengzhou]\nMengzhou () is a County-level city in Henan province, People's Republic of China.\n\n[Shayang County]\nShayang () is a county of west-central Hubei province, People's Republic of China.\n\n[Liu Xiwu]\nHe was born in Meng County, Henan Province (modern Mengzhou, Jiaozuo, Henan Province) and educated in Kaifeng.\n\n[Quan (state)]\nQuan was founded by Wen Ding’s son Quan Wending (权文丁) in the area of modern day Maliang Town (马良镇), Shayang County, Jingmen City, Hubei Province, next to what would later emerge as the State of Chu.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q85ff33a6fd",
  "kind": "yes/no",
  "text": "Claim: Raymond Andrew \"Ray\" Winstone, is an English film and television actor, he has appeared in films such as The Magic Roundabout, a French-British computer-animated adventure fantasy film based on the television series \"The Magic Roundabout\", released in 2005.\n\nPassages:\n\n[The Magic Roundabout (film)]\nThe Magic Roundabout (released in France as Pollux - Le manège enchanté and redubbed in the United States as Doogal or The Lord of the Springs) is a 2005 French-British computer-animated adventure fantasy film based on the television series \"The Magic Roundabout\".\n\n[Ray Winstone]\nHe has appeared in films such as \"Cold Mountain\", \"Nil By Mouth\", \"King Arthur\", \"The Magic Roundabout\", \"The Departed\", \"Beowulf\", \"Indiana Jones and the Kingdom of the Crystal Skull\", \"Edge of Darkness\", \"The Sweeney\" and \"Noah\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q997b836899",
  "kind": "yes/no",
  "text": "Claim: Deliver Us From Evil explores the life of what Irish priest who raped, molested and abused at least 25 children in California in the early 1900s.\n\nPassages:\n\n[Oliver O'Grady]\nOliver Francis O'Grady (born June 5, 1945) is an Irish laicized Catholic priest who raped, molested and abused at least 25 children in California from 1973 onwards.\n\n[Deliver Us from Evil (2006 film)]\nDeliver Us from Evil is a 2006 American documentary film that explores the life of Irish Catholic priest Oliver O'Grady, who admitted to having molested and raped approximately 25 children in Northern California between the late 1970s and the early 1990s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q6345a39a8f",
  "kind": "yes/no",
  "text": "Post: Men love making women think they were the problem when they finally decide to leave after putting up with mistreatment for god knows how long \n\n“You were supposed to be my ride or die 😩”\n\nOkay, so die then.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q3426102ab2",
  "kind": "yes/no",
  "text": "Claim: Vikram played a lead role in the film that Ranja is a remake of and has been awarded an Honorary Doctorate by the People's University of Milan.\n\nPassages:\n\n[Dhool]\nDhool (English: Super ) is a 2003 Indian Tamil-language action masala film directed by Dharani. The film featured Vikram, Jyothika and Reemma Sen in the lead roles, while Vivek, Sayaji Shinde, Telangana Sakunthala and Pasupathy among others play supporting roles.\n\n[Vikram (actor)]\nKennedy John Victor, known professionally as Vikram or Chiyaan Vikram, is an Indian film actor who predominantly appears in Tamil language films and has won seven Filmfare Awards as well as one National Film Award and Tamil Nadu State Film Award amongst other recognitions and was awarded an Honorary Doctorate by the People's University of Milan in May 2011.\n\n[Ranja]\nRanja (Sinhalese: \"රන්ජා\" ) is a 2014 Sri Lankan Sinhala action thriller film directed by Sudesh Wasantha Peiris and produced by Sunil T. Fernando for Sunil T. Films.It was the remake of 2003 Tamil language film Dhool.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qfb3314fd0d",
  "kind": "yes/no",
  "text": "Post: It's been a productive last day. Maxed Out all my credit cards in preparation of my Rapture tomorrow!!! #iwishwehadallbeenready",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q902bb4dfb7",
  "kind": "yes/no",
  "text": "Claim: The African-American composer, Scott Joplin, co-wrote Air.\n\nPassages:\n\n[Scott Joplin]\nScott Joplin ( ; 1867/68 or November 24, 1868– April 1, 1917) was an African-American composer and pianist.\n\n[Air Lore]\nAir Lore is an album by the improvisational trio Air featuring Henry Threadgill, Steve McCall, and Fred Hopkins performing compositions by Jelly Roll Morton and Scott Joplin.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q3ba1562ebd",
  "kind": "yes/no",
  "text": "Claim: The exhibition basketball game which will be held at the Staples Center in Los Angeles, California will be played February 18, 2018.\n\nPassages:\n\n[2017–18 NBA season]\nThe 2018 NBA All-Star Game will be played on February 18, 2018, at the Staples Center in Los Angeles, California.\n\n[2018 NBA All-Star Game]\nThe 2018 NBA All-Star Game will be the 67th edition and is an exhibition basketball game that will be played on February 18, 2018.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q176fdf6363",
  "kind": "yes/no",
  "text": "Claim: The four-peice Eyes of the Dead opened for Six Feet Under, an American death metal band from Tampa, Florida.\n\nPassages:\n\n[Eyes of the Dead]\nThey have toured throughout the northeastern and midwestern areas of The United States, opening for many different national touring acts, such as: The Absence, Agnostic Front, Anthrax, Carnivore, Dark Tranquility, Destruction, D.R.I., Dying Fetus, Emperor, Exodus, Goatwhore, God Forbid, Immolation, Job For A Cowboy, Krisiun, Last Chance To Reason Misfits, Misery Index, Motograter, Mushroomhead, Opeth, Revocation, Six Feet Under, Sodom, Sonata Arctica, Soulfly, Suffocation, Testament, Thy Will Be Done, Unearth, Warbringer, Winds of Plague, and many others.\n\n[Six Feet Under (band)]\nSix Feet Under is an American death metal band from Tampa, Florida, formed in 1993.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q278955f5b7",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I wish I could work with Jack Antonoff.",
   "jack antonoff once ur done with clairo i’m right here sweetie"
  ]
 },
 {
  "qid": "q3dac118cb4",
  "kind": "yes/no",
  "text": "Post: Leave it to the nice people of Hutch to yell at me to \"eat shit\" while I run. Jokes on them, I do.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q910ba9cb0e",
  "kind": "yes/no",
  "text": "Claim: The awards ceremony that was hosted in 2007 by an American commercial broadcast television network headquartered on Pico Boulevard was hosted at the Shrine Auditorium in Texas.\n\nPassages:\n\n[Fox Broadcasting Company]\nFox Broadcasting Company (often shortened to Fox and stylized as FOX) is an American commercial broadcast television network owned by Fox Entertainment Group, a subsidiary of 21st Century Fox. The network is headquartered at 20th Century Fox studio on Pico Boulevard in Century City of Los Angeles with additional major offices and production facilities at the Fox Television Center in nearby West Los Angeles and Fox Broadcasting Center in the Yorkville neighborhood of Manhattan, New York City.\n\n[59th Primetime Emmy Awards]\nThe 59th Primetime Emmy Awards were held on Sunday, September 16, 2007, honoring the best in U.S. prime time television programming at the Shrine Auditorium in Los Angeles, California. The ceremony was televised live on Fox at 8:00 p.m. EDT for the first time in high definition (on tape delay three hours later on the West Coast of the United States at 8:00 p.m.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q63d348cfe3",
  "kind": "yes/no",
  "text": "Claim: Louis King directed the film which starred Steve Cochran and the actor who played Sheriff Vincent Sherman in \"Bonanza\".\n\nPassages:\n\n[Ray Teal]\nHis longest-running role was as Sheriff Roy Coffee on NBC's western series \"Bonanza\" (1960–1972).\n\n[The Lion and the Horse]\nThe Lion and the Horse is a 1952 Western film directed by Louis King and written by Crane Wilbur. It stars Steve Cochran, Ray Teal and a horse named Wildfire.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd19f87f05d",
  "kind": "yes/no",
  "text": "Claim: A star of \"Hotline\" a 2014 comedy film and Millard Webb are not both authors.\n\nPassages:\n\n[Jeff Ragsdale]\nJeffrey Charles \"Jeff\" Ragsdale ( ) is an American author, documentary filmmaker, actor and stand-up comedian.\n\n[Millard Webb]\nMillard Webb (6 December 1893 – 21 April 1935), was an American screenwriter and director.\n\n[Hotline (2014 film)]\nThe film stars Miss Cleo, Jeff Ragsdale, Jamie Blaine, and Tonya Jone Miller.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa5b2e3f7c5",
  "kind": "yes/no",
  "text": "Tweet: Going to M&amp;S food will be the highlight of my day later, can’t wait👌🏻😅",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qffd79c9373",
  "kind": "yes/no",
  "text": "Claim: Lommel differential equation was developed by the German physicist who was the doctoral advisor to another German Physicist who identified the Stark effect.\n\nPassages:\n\n[Johannes Stark]\nJohannes Stark (] , 15 April 1874 – 21 June 1957) was a German physicist and Physics Nobel Prize laureate. He is known for identifying the Stark effect, and was later closely involved with the \"Deutsche Physik\" movement under the Nazi regime.\n\n[Eugen von Lommel]\nEugen Cornelius Joseph von Lommel (19 March 1837, Edenkoben – 19 June 1899, Munich) was a German physicist. He is notable for the Lommel polynomial, the Lommel function, the Lommel–Weber function, and the Lommel differential equation. He is also notable as the doctoral advisor of the Nobel Prize winner Johannes Stark.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qf7290c62a9",
  "kind": "yes/no",
  "text": "Claim: The son of Souleyman Sané plays in the football Premier League.\n\nPassages:\n\n[Leroy Sané]\nLeroy Aziz Sané (] , ] ; born 11 January 1996) is a German professional footballer who plays as a winger for Premier League club Manchester City and the Germany national team.\n\n[Souleyman Sané]\nSouleyman Sané (born 26 February 1961) is a retired Senegalese footballer who played as a striker. He is the father of Manchester City FC and Germany forward Leroy Sané.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q9ef8b36e4b",
  "kind": "yes/no",
  "text": "Claim: The publication from George Vradenburg and Moment are both a type of magazine.\n\nPassages:\n\n[George Vradenburg]\nHe is co-founder and chairman of USAgainstAlzheimer's (USA2), an Alzheimer's advocacy organization., and co-publisher of \"Tikkun\", an English-language magazine with a progressive viewpoint.\n\n[Moment (magazine)]\nMoment is an independent magazine for a Jewish-American audience and is not tied to any movement or ideology.\n\n[Tikkun (magazine)]\nTikkun is a quarterly interfaith Jewish left-progressive magazine, published in the United States, that analyzes American and Israeli culture, politics, religion, and history in the English language.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q8f8df7d39d",
  "kind": "yes/no",
  "text": "Claim: Michael John McKean is older than Simon Neil.\n\nPassages:\n\n[Michael McKean]\nMichael John McKean (born October 17, 1947) is an American actor, comedian, and musician, known for a variety of roles played since the 1970s.\n\n[Simon Neil]\nSimon Alexander Neil (born 31 August 1979) is a Scottish vocalist, guitarist, and songwriter.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q4381637854",
  "kind": "yes/no",
  "text": "Text: finally found the perfect cowboy boots on ebay after searching for weeks 🤠",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q955d9fc46a",
  "kind": "yes/no",
  "text": "Claim: The author of Varieties of Disturbance wrote shorter works than Raymond Carver.\n\nPassages:\n\n[Varieties of Disturbance]\nVarieties of Disturbance is Lydia Davis's fourth collection of short stories.\n\n[Raymond Carver]\nRaymond Clevie Carver Jr. (May 25, 1938 – August 2, 1988) was an American short-story writer and poet. Carver contributed to the revitalization of the American short story during the 1980s.\n\n[Lydia Davis]\nLydia Davis (born July 15, 1947) is an American writer noted for literary works of extreme brevity (commonly called \"flash fiction\").",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q50c24828e4",
  "kind": "yes/no",
  "text": "Claim: Universal Studios is host to both the Back to the Future Ride, and the attraction adjacent to Springfield (Universal Studios Hollywood).\n\nPassages:\n\n[Back to the Future: The Ride]\nBack to the Future: The Ride was a simulator ride at Universal Studios theme parks. It was previously located at Universal Studios Florida and Universal Studios Hollywood, where it has since been replaced by \"The Simpsons Ride\", and at Universal Studios Japan where it has since been replaced by \"\".\n\n[The Simpsons Ride]\n\"The Simpsons\" Ride is a simulator ride featured at the Universal Studios Florida and Universal Studios Hollywood theme parks.\n\n[Springfield (Universal Studios Hollywood)]\nIt opened on May 13, 2015 adjacent to The Simpsons Ride.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q60915e7281",
  "kind": "yes/no",
  "text": "Claim: The breed the American Water Spaniel was derived from was bred before the Estonian Hound.\n\nPassages:\n\n[Estonian Hound]\nIt was bred in 1947 when the Soviet Union's national economy ministry decided that every country in the Union must have its own dog breed.\n\n[American Water Spaniel]\nThe breed was saved by Dr. Fred J. Pfeifer, who set up the breed club and standard, and whose work led to recognition for the breed by the United Kennel Club, and later, the American Kennel Club.\n\n[English Water Spaniel]\nThe English Water Spaniel is a breed of dog that has been extinct since the first part of the 20th century, with the last specimen seen in the 1930s.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q93d1063004",
  "kind": "yes/no",
  "text": "Claim: John E. EchoHawk is a leading member in a social movement that wants to reverse the paternalistic policies enacted upon Native American tribes.\n\nPassages:\n\n[John EchoHawk]\nHe is a leading member of the Native American self-determination movement.\n\n[Native American self-determination]\nSelf-determination\" is meant to reverse the paternalistic policies enacted upon Native American tribes since the U.S. government created treaties and established the reservation system.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q018111a8f3",
  "kind": "yes/no",
  "text": "Claim: Kamal Haasan starred in a film directed by the director of \"Sundara Swapnagalu\".\n\nPassages:\n\n[Sundara Swapnagalu]\nThe film was a remake of director's own Tamil film \"Sollathaan Ninaikkiren\".\n\n[Sollathaan Ninaikkiren]\nSollathaan Ninaikkiren is a 1973 Tamil language film scripted and directed by K. Balachander starring Sivakumar, S. V. Subbaiah, Jayachitra, Srividya, Shubha, Kamal Haasan and Jayasudha in the lead roles.\n\n[Kamal Haasan]\nKamal Haasan (born 7 November 1954) is an Indian film actor, director, screenwriter, producer, playback singer and lyricist who works primarily in Tamil cinema.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q0a4b71dd8d",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Mental shoot out ends. Silent pause. Sirens start 🚨 Always so perfectly timed 🚔🚓👍🏽 #LineOfDuty #LineofDuty6 #LOD6 #LOD",
   "The sirens always start just as the gunfire finishes"
  ]
 },
 {
  "qid": "q6d0bd67f38",
  "kind": "yes/no",
  "text": "Claim: A television series created for Netflix, which American producer and writer Liz Friedman is especially known for her work on, is the second in the series of the shows that lead to \"The Defenders\" miniseries after Petrie released on Netflix earlier.\n\nPassages:\n\n[The Defenders (miniseries)]\nMarvel's The Defenders, or simply The Defenders, is an American web television miniseries created by Douglas Petrie and Marco Ramirez for Netflix, based on the Marvel Comics characters Daredevil, Jessica Jones, Luke Cage and Iron Fist, who form the eponymous superhero team.\n\n[Liz Friedman]\nLiz Friedman is an American television producer and television writer known especially for her work on \"\", \"Young Hercules\", \"House\" and \"Jessica Jones\".\n\n[Jessica Jones (TV series)]\nMarvel's Jessica Jones, or simply Jessica Jones, is an American web television series created for Netflix by Melissa Rosenberg, based on the Marvel Comics character of the same name. It is set in the Marvel Cinematic Universe (MCU), sharing continuity with the films of the franchise, and is the second in a series of shows that lead to \"The Defenders\" crossover miniseries.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q4349b34c0d",
  "kind": "yes/no",
  "text": "Claim: The artist, who has played and recorded with Sev Lewkowicz, and Maja Ivarsson are both lead singers.\n\nPassages:\n\n[Maja Ivarsson]\nMaja Ivarsson, (] , born 2 October 1979) is a Swedish singer and lead vocalist of the Swedish indie rock band The Sounds.\n\n[Sev Lewkowicz]\nHe has played and recorded with Mungo Jerry, Dennis Locorriere, Any Trouble, Tim Smit, Sarah Miles, Jeff Duff and Tony Clarke.\n\n[Dennis Locorriere]\nDennis Michael Locorriere (born June 13, 1949; Union City, New Jersey, United States) is the American former lead vocalist and guitarist of the soft rock group Dr. Hook & the Medicine Show, later Dr. Hook.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc0fdedc87d",
  "kind": "yes/no",
  "text": "Claim: In alphabetical order, the third name of the author of the novel that the film Nuit de Chien was based on comes before Richard Llewellyn's.\n\nPassages:\n\n[Juan Carlos Onetti]\nJuan Carlos Onetti Borges (July 1, 1909, Montevideo – May 30, 1994, Madrid) was an Uruguayan novelist and author of short stories.\n\n[Nuit de chien]\nIt is based on the novel \"Para esta noche\" by Juan Carlos Onetti.\n\n[Richard Llewellyn]\nRichard Dafydd Vivian Llewellyn Lloyd (8 December 1906 – 30 November 1983), known by his pen name Richard Llewellyn, was a British novelist.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q12940177bf",
  "kind": "yes/no",
  "text": "Claim: The American web televison series, which is set in the MCU, stars an actress who is also known as \"scream queen\" for having rolls in horror films such as \"Prom Night\" and \"Vampire Bats\".\n\nPassages:\n\n[Jessica Stroup]\nJessica Leigh Stroup (born October 23, 1986) is an American actress, best known for her role as Erin Silver on \"90210\", Max Hardy on \"The Following\", and Joy Meachum in \"Iron Fist\". She is regarded as a scream queen for starring in the horror films \"Prom Night\", \"Vampire Bats\", \"Left in Darkness\", and \"The Hills Have Eyes 2\".\n\n[Iron Fist (TV series)]\nMarvel's Iron Fist, or simply Iron Fist, is an American web television series created for Netflix by Scott Buck, based on the Marvel Comics character of the same name. It is set in the Marvel Cinematic Universe (MCU), sharing continuity with the films of the franchise and is the fourth in a series of shows that lead to \"The Defenders\" crossover miniseries.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa4db9a1bfe",
  "kind": "yes/no",
  "text": "Tweet: @kmflett And with a plentiful supply of rhubarb.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q6b1ef6109c",
  "kind": "yes/no",
  "text": "Claim: The community Alamorio, in Imperial County, California is partly named after a species of tree that is native to North America, Europe, and western Asia.\n\nPassages:\n\n[Alamorio, California]\nAlamorio is an unincorporated community in Imperial County, California. The community resides along the Alamo River, and was named by combining the Spanish words \"alamo\" (meaning \"poplar\" or \"cottonwood\") and \"rio\" (meaning \"river\").\n\n[Populus sect. Aigeiros]\nThe species are native to North America, Europe, and western Asia.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8b3daf25eb",
  "kind": "yes/no",
  "text": "Claim: Makoto Koshinaka is eight years younger than the musician from Hello, Blue Roses. Makoto was born on July 15, 1980.\n\nPassages:\n\n[Hello, Blue Roses]\nHello, Blue Roses is a Canadian musical collaboration involving Dan Bejar (of Destroyer and The New Pornographers) and his girlfriend, Sydney Hermant, a visual artist from Vancouver.\n\n[Makoto Koshinaka]\nMakoto Koshinaka (越中睦 / 越中睦士 or Makoto, born July 15, 1980 in Moto Azabu, Tokyo) is a Japanese singer, songwriter, actor and model, activating both in Japan and in Thailand, starting with the year 1999.\n\n[Dan Bejar]\nDaniel Bejar ( ; born October 4, 1972) is an independent singer-songwriter from Vancouver, British Columbia, Canada.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q17c6e32d45",
  "kind": "yes/no",
  "text": "Claim: Aloinopsis and Eriogonum are both ice plants.\n\nPassages:\n\n[Aloinopsis]\nAloinopsis is a genus of ice plants from South Africa.\n\n[Eriogonum]\nEriogonum is the scientific name for a genus of flowering plants in the family Polygonaceae.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qe28156db2d",
  "kind": "yes/no",
  "text": "Claim: Jo Ann Terry won the 80m hurdles event at the Pan American Games, a Mexico City-based event from 1963.\n\nPassages:\n\n[Jo Ann Terry]\nAffiliated with the Tennessee State University she won the 80 m hurdles event at the 1963 Pan American Games.\n\n[1963 Pan American Games]\nThe 4th Pan American Games were held from April 20 to May 5, 1963, in São Paulo, Brazil.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q791c5cea19",
  "kind": "yes/no",
  "text": "Claim: Caroline Cruice Goodall, is an English actress and screenwriter, her other film appearances include the October 2015 Australian revenge comedy-drama film, The Dressmaker, written and directed by Jocelyn Moorhouse, based on the novel of the same name by Rosalie Ham.\n\nPassages:\n\n[Caroline Goodall]\nHer other film appearances include \"Hook\" (1991), \"Cliffhanger\" (1993), \"Schindler's List\" (1993), \"Disclosure\" (1994), \"White Squall\" (1996), \"The Princess Diaries\" (2001) and \"The Dressmaker\" (2015).\n\n[The Dressmaker (2015 film)]\nThe Dressmaker is a 2015 Australian revenge comedy-drama film written and directed by Jocelyn Moorhouse, based on the novel of the same name by Rosalie Ham.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q343d1ff481",
  "kind": "yes/no",
  "text": "Claim: the ATX Television Festival was the network premiere for the series that the co-writer of \"Shall We Gather at the River\", from the series \"Falling Skies\" started working on in 2014.\n\nPassages:\n\n[Bradley Thompson]\nThompson and Weddle are currently working on \"The Strain\", the television adaptation of the novel series by Guillermo del Toro and Chuck Hogan.\n\n[Shall We Gather at the River (Falling Skies)]\nIt was written by Bradley Thompson & David Weddle and directed by Greg Beeman.\n\n[The Strain (TV series)]\nThe Strain is an American horror drama television series that premiered on FX on July 13, 2014.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe15d2dec12",
  "kind": "yes/no",
  "text": "Claim: The Australian professional women's basketball team Erin Phillips played for has an Chinese playing in it.\n\nPassages:\n\n[Adelaide Lightning]\nThe Adelaide Lightning are an Australian professional women's basketball team competing in the Women's National Basketball League (WNBL).\n\n[Erin Phillips]\nShe has played basketball in Australia's WNBL for the Australian Institute of Sport and the Adelaide Lightning.\n\n[Colleen Planeta]\nColleen Planeta (born September 3, 1988) is an American professional basketball player. She currently plays for the Adelaide Lightning in the WNBL.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q199f82d6bb",
  "kind": "yes/no",
  "text": "Claim: The man who was portrayed on television by the star of The Fifth Missile served in the U.S. military.\n\nPassages:\n\n[Robert Conrad]\nHe portrayed World War II ace Pappy Boyington in the television series \"Baa Baa Black Sheep\" (later syndicated as \"Black Sheep Squadron\").\n\n[The Fifth Missile]\nThe Fifth Missile is a 1986 TV movie starring Robert Conrad, Sam Waterston and David Soul about an American ballistic missile submarine, based on the novel \"The Gold Crew\" by Frank M. Robinson and Thomas N. Scortia.\n\n[Pappy Boyington]\nGregory \"Pappy\" Boyington (December 4, 1912 – January 11, 1988) was an American combat pilot who was a United States Marine Corps fighter ace during World War II.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc7748e1f10",
  "kind": "yes/no",
  "text": "Text: these two girls are on the beach in lawn chairs, i love shoobies",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qbefefc58a9",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "if you see me crying in the self-service car wash in my rosati’s uniform, no you didn’t ❤️",
   "No."
  ]
 },
 {
  "qid": "q4521f61218",
  "kind": "yes/no",
  "text": "Tweet: Do you think anyone on Bachelor in Paradise has seen Oscar winner Parasite?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qb2370979bf",
  "kind": "yes/no",
  "text": "Claim: The Silver Nugget is a casino and arena located in a major city that was incorporated on May 16, 1946.\n\nPassages:\n\n[North Las Vegas, Nevada]\nNorth Las Vegas is a city in Clark County, Nevada, United States, located in the Las Vegas Valley. The city was incorporated on May 16, 1946.\n\n[Silver Nugget]\nThe Silver Nugget is a casino and arena located on Las Vegas Boulevard North in North Las Vegas, Nevada.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qeff59bb3e1",
  "kind": "yes/no",
  "text": "Text: Amazing how fast this team can go winning from 13 straight to losing three in a row. Lol. Horrible managing tonight. I really hope this Boone experiment is over soon.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q50986af645",
  "kind": "yes/no",
  "text": "Claim: The award given to Matt James in 2012 has its name derived from the EN World web site.\n\nPassages:\n\n[Matt James (game designer)]\nIn 2012 James won an ENnie Award for \"\" and has been nominated for several Origins Awards.\n\n[ENnies]\nThe name of the award is derived from the EN World web site that has hosted the awards since their inception in 2001.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe14a659bf7",
  "kind": "yes/no",
  "text": "Claim: The actor that plays Joe MacMillan in \"Halt and Catch Fire\" also starred with Scott Glenn in the 2017 horror film The Keeping Hours.\n\nPassages:\n\n[Lee Pace]\nHe currently stars as protagonist Joe MacMillan in AMC's \"Halt and Catch Fire\".\n\n[The Keeping Hours]\nThe Keeping Hours is a 2017 American supernatural romantic horror film directed by Karen Moncrieff and written by Rebecca Sonnenshine. The film stars Lee Pace and Carrie Coon.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q8017932744",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "wow. i left on time today and the airport connector is all the way backed up. love that",
   "I'm so mad that I'm stuck in traffic and late to school, especially because I left early."
  ]
 },
 {
  "qid": "q4375a5dc6e",
  "kind": "yes/no",
  "text": "Claim: Both where Katie Jacobs Stanton sits on The Herald of Christian Science and the Christian Science Sentinel are the same product. They both are magazines.\n\nPassages:\n\n[Christian Science Sentinel]\nThe Christian Science Sentinel (originally the \"Christian Science Weekly\") is a magazine published by the Christian Science Publishing Society based in Boston, Massachusetts.\n\n[Time (magazine)]\nTime is an American weekly news magazine published in New York City.\n\n[Katie Jacobs Stanton]\nStanton sits on the Board of Directors for Vivendi and Time.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qbd912c31e6",
  "kind": "yes/no",
  "text": "Claim: Steven Jackson, an American running back, played baseball for Oregon State and was coached by Paul Boudreau.\n\nPassages:\n\n[Paul Boudreau]\nPaul T. Boudreau (born December 30, 1949) is an American football coach who last served as offensive line coach for the Los Angeles Rams of the National Football League (NFL). Boudreau’s stellar offensive lines over the years have helped pave the way for five running backs to top the 10,000-yard career rushing mark, including Barry Sanders, Curtis Martin, Thurman Thomas, Fred Taylor and Steven Jackson.\n\n[Steven Jackson]\nSteven Rashad Jackson (born July 22, 1983) is a former American football running back.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 }
]
