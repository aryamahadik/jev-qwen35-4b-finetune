# A46 replay label-noise blind read RSBS08-blind_read-13b5b8df-005

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS08-blind_read-13b5b8df-005.json

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
  "qid": "q746511851c",
  "kind": "yes/no",
  "text": "Claim: Ghostbusters is a song written and recorded by Ray Parker Jr. as the theme song for a movie starring a Canadian-American actor who was an original member of the Not Ready for Prime Time Players on Saturday Night Live.\n\nPassages:\n\n[Dan Aykroyd]\nDaniel Edward Aykroyd {'1': \", '2': \", '3': \", '4': \"} (born July 1, 1952) is a Canadian-American actor, comedian, producer, screenwriter, musician and businessman. He was an original member of the \"Not Ready for Prime Time Players\" on \"Saturday Night Live\" (1975–1979).\n\n[Ghostbusters (song)]\n\"Ghostbusters\" is a song written and recorded by Ray Parker Jr. as the theme to the film of the same name starring Bill Murray, Dan Aykroyd, Harold Ramis, and Ernie Hudson.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qff1d51fbec",
  "kind": "yes/no",
  "text": "Claim: The short story from The Wind's Twelve Quarters that won the Hugo Award in 1974 was published in 1973 on January 27th.\n\nPassages:\n\n[The Ones Who Walk Away from Omelas]\n\"The Ones Who Walk Away from Omelas\" is a 1973 plotless, short, descriptive work of philosophical fiction, though popularly classified as a short story, by American writer Ursula K. Le Guin.\n\n[The Wind's Twelve Quarters]\nThe story \"The Ones Who Walk Away from Omelas\" won the Hugo Award in 1974, while \"The Day Before the Revolution\" won the Locus and Nebula Awards in 1975.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qfa1774003d",
  "kind": "yes/no",
  "text": "Claim: Space Ghost's arch enemy is a catlike alien space pirate. He's the only character Andy Ronald Merrill voiced in \"Space Ghost Coast to Coast\".\n\nPassages:\n\n[Andy Merrill]\nAndy Ronald Merrill (born November 27, 1966 in Newark, Ohio) is an American television writer, producer and voice actor best known for his comedy voice portrayal of the character Brak on \"Space Ghost Coast to Coast\" and \"Cartoon Planet\", and other related productions from Cartoon Network utilizing characters from the \"Space Ghost\" series.\n\n[Space Ghost's Musical Bar-B-Que]\nFeaturing songs and skits by Space Ghost and his arch enemies Zorak and Brak.\n\n[Brak (character)]\nBrak is a fictional character and supervillain on the 1966 Hanna-Barbera animated series \"Space Ghost\", portrayed as a catlike alien space pirate trying to conquer the galaxy.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9a67f0675d",
  "kind": "yes/no",
  "text": "Claim: The creator of the media franchise in which Malcolm Reynolds is a fictional character and the protagonist, was american. The actor Norman Mailer was also american.\n\nPassages:\n\n[Firefly (franchise)]\nThe \"Firefly\" media franchise is an American space Western media franchise created by Joss Whedon and produced by Mutant Enemy Productions.\n\n[Norman Mailer]\nNorman Kingsley Mailer (January 31, 1923 – November 10, 2007) was an American novelist, journalist, essayist, playwright, film-maker, actor, and political activist.\n\n[Malcolm Reynolds]\nMalcolm \"Mal\" Reynolds is a fictional character and the protagonist of the \"Firefly\" franchise.\n\n[Joss Whedon]\nJoseph Hill Whedon ( ; born June 23, 1964) is an American screenwriter, director, producer, comic book writer, and composer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc941979af0",
  "kind": "yes/no",
  "text": "Tweet: . @shopDisney thanks for shutting down the only Disney Store in northeastern Ohio. The other two stores went out of business yrs ago. It’s not the same with shipping costs online not to mention LE doll sales are an absolute nightmare online. So unbelievably disappointing. 💔",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q9eb27c4353",
  "kind": "yes/no",
  "text": "Claim: Marc Shiller, who was born in Beunos Aires in 1957, but is a resident of the United States, belongs to the ethnic group, that includes musician Paz Lenchantin.\n\nPassages:\n\n[Marc Schiller]\nMarc Schiller is an Argentinian American man who was born in Buenos Aires, Argentina in 1957. He survived a kidnapping and attempted murder by the Sun Gym Gang in Miami, Florida in 1994.\n\n[Argentine Americans]\nArgentine Americans (Spanish: Argentino Americanos ) are Americans whose full or partial origin is in Argentina.\n\n[Paz Lenchantin]\nPaz Lenchantin (born December 12, 1973) is an Argentine American musician.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q947e7163d8",
  "kind": "yes/no",
  "text": "Text: Turnover is the best band to cry to/drive to/daydream to/fall asleep to/ reminisce to/die to",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q2959273934",
  "kind": "yes/no",
  "text": "Claim: The 1942 romantic comedy film, named for the character Beulah Annan inspired, starred the guitarist and comedic actor who had the nickname The King of Chutzpah.\n\nPassages:\n\n[Phil Silvers]\nPhil Silvers (May 11, 1911 – November 1, 1985) was an American entertainer and comedic actor, known as \"The King of Chutzpah\".\n\n[Roxie Hart (film)]\nRoxie Hart, also known as Chicago or Chicago Gal, is a 1942 American comedy film directed by William A. Wellman and starring Ginger Rogers, Adolphe Menjou, George Montgomery, Nigel Bruce, Phil Silvers, William Frawley and Spring Byington.\n\n[Beulah Annan]\nThe play has been adapted into a 1927 silent film, 1975 stage musical, and 2002 movie musical (which won the Academy Award for Best Picture), all with that title, and a 1942 romantic comedy film, \"Roxie Hart\", named for the character Annan inspired.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6007358025",
  "kind": "yes/no",
  "text": "Claim: Sidney Olcott, not Randal Kirk II, was a Canadian film producer, director, actor and screenwriter.\n\nPassages:\n\n[Sidney Olcott]\nSidney Olcott (September 20, 1872 – December 16, 1949) was a Canadian-born film producer, director, actor and screenwriter.\n\n[Randal Kirk II]\nRandal Kirk II is an American film director, writer, producer, and cinematographer.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q488338b2ec",
  "kind": "yes/no",
  "text": "Tweet: @cassieecote413 you can copy mine",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qe1293aadee",
  "kind": "yes/no",
  "text": "Claim: Zhongyang County, covering an area of 130 sq miles, is under the administration of this city. That city has a larger population than Fuxin.\n\nPassages:\n\n[Lüliang]\nLüliang or Lyuliang () is a prefecture-level city in the west of Shanxi province, People's Republic of China, bordering Shaanxi province across the Yellow River to the west, Jinzhong and the provincial capital of Taiyuan to the east, Linfen to the south, and Xinzhou to the north. It has a total area of 21143 km2 and total population of 3,727,057. The metro area of Lüliang has a population of 320,142 at the 2010 census.\n\n[Fuxin]\nThe total population of the prefecture at the 2010 census is 1,819,339, of whom 669,317 are resident in the built up area, which comprises four urban districts, collectively known as 'Fuxin City'.\n\n[Zhongyang County]\nIt is under the administration of Lüliang city.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa860f811a7",
  "kind": "yes/no",
  "text": "Claim: The star of 1981's Sweet Talker performed in Give My Regards to Broad Street. That was a 1984 British musical drama that was directed by Peter Webb.\n\nPassages:\n\n[Sweet Talker (film)]\nSweet Talker is a 1991 Australian film starring Bryan Brown.\n\n[Give My Regards to Broad Street (film)]\nGive My Regards to Broad Street is a 1984 British musical drama film directed by Peter Webb, which starred Paul McCartney, Bryan Brown and Ringo Starr.\n\n[Bryan Brown]\nHe has performed in over eighty film and television projects since the late 1970s, both in his native Australia and abroad. Notable films include \"Breaker Morant\" (1980), \"Give My Regards to Broad Street\" (1984), \"F/X\" (1986), \"Cocktail\" (1988), \"Gorillas in the Mist\" (1988), \"F/X2\" (1991), \"Along Came Polly\" (2004), \"Australia\" (2008), \"Kill Me Three Times\" (2014) and \"Gods of Egypt\" (2016).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q4287591c35",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "@SrutisJay one of them smonks weed so it's super worth it /s",
   "None of those designs are really worth the money."
  ]
 },
 {
  "qid": "qc6ab130011",
  "kind": "yes/no",
  "text": "Claim: The nu-metal band Ashley Naylor is vocalist for, and Incubus are not known for their skill in classical music.\n\nPassages:\n\n[Incubus (band)]\nIncubus is an American rock band from Calabasas, California.\n\n[Even (band)]\nEven are an Australian indie rock three-piece fronted by singer-songwriter-guitarist, Ash Naylor, with Matthew Cotter on drums and Wally Kempton (also known as Wally Meanie) on bass guitar and backing vocals. They formed in March 1994 and played regularly around the live music scene and toured both nationally and internationally. They have released six studio albums, \"Less Is More\" (10 June 1996), \"Come Again\" (28 September 1998), \"A Different High\" (14 May 2001), \"Free Kicks\" (6 June 2004), \"Even\" (29 March 2008) and \"In Another Time\" (9 December 2011).\n\n[Ashley Naylor]\nAshley Naylor is an Australian musician, best known for his guitar and vocals in Melbourne-based band Even.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa14341a0c0",
  "kind": "yes/no",
  "text": "Claim: Hugo Rodríguez Romero is a Spanish footballer who plays for a team in the autonomous community of Murcia.\n\nPassages:\n\n[FC Cartagena]\nFútbol Club Cartagena is a Spanish football team based in Cartagena, in the autonomous community of Murcia.\n\n[Hugo Rodríguez Romero]\nHugo Rodríguez Romero (born 30 December 1989), simply known as Hugo, is a Spanish footballer who plays for FC Cartagena as a winger.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q7a31d80638",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "Why are the side effects of antidepressants so ✨scary✨",
   "The side effects of antidepressants can be concerning."
  ]
 },
 {
  "qid": "q29b84322f6",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "sure you have a paying job but are you a Silver Chick Fil A Rewards member? 😤🙄🧐",
   "People are out here working paying jobs and I'm just a Chick File A silver rewards member"
  ]
 },
 {
  "qid": "q519e0a4185",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "by simply stating the foolishness of voting in favour of brexit",
   "Fool me once shame on you. Fool me twice shame on me. Fool me multiple times I must have become a brexiter. #Brexit"
  ]
 },
 {
  "qid": "q998e96ba32",
  "kind": "yes/no",
  "text": "Claim: Hail! Hail! Rock 'n' Roll was a documentary that was filmed before Almost Sunrise.\n\nPassages:\n\n[Almost Sunrise]\nAlmost Sunrise is a 2016 American documentary film directed by Michael Collins.\n\n[Hail! Hail! Rock 'n' Roll]\nRock 'n' Roll is a 1987 documentary film directed by Taylor Hackford that chronicles two 1986 concerts celebrating rock and roll musician Chuck Berry's 60th birthday.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qcf45f2289a",
  "kind": "yes/no",
  "text": "Claim: The game which High Rollers Casino is a type been played outside of casinos.\n\nPassages:\n\n[High Rollers Casino]\nHigh Rollers Casino is a 2004 casino video game co-developed by Cinemaware and Virtual Toysfor the PlayStation 2 and Xbox gaming consoles.\n\n[Casino game]\nCasino games can also be played outside of casinos for entertainment purposes like in parties or in school competitions, some on machines that simulate gambling.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q6fd3cb1a79",
  "kind": "yes/no",
  "text": "Claim: World UFO Day is celebrated on the day an American aviator claimed to see nine hot dog shapped objects flying near Mount Rainier, Washington.\n\nPassages:\n\n[World UFO Day]\nJune 24 is the date that aviator Kenneth Arnold reported what is generally considered to be the first widely reported unidentified flying object sighting in the United States, while July 2 commemorates the supposed UFO crash in the 1947 Roswell UFO Incident.\n\n[Kenneth Arnold]\nHe is best known for making what is generally considered the first widely reported unidentified flying object sighting in the United States, after claiming to have seen nine unusual objects flying in tandem near Mount Rainier, Washington on June 24, 1947.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa761c0be31",
  "kind": "yes/no",
  "text": "Claim: An American football quarterback for the Chicago Bears was a star of a game released on July 14, 2009.\n\nPassages:\n\n[Mark Sanchez]\nMark Travis John Sanchez (born November 11, 1986) is an American football quarterback for the Chicago Bears of the National Football League (NFL).\n\n[NCAA Football 10]\nNCAA Football 10 is a college football video game created by Electronic Arts. It was released on July 14, 2009 for the Xbox 360, PlayStation 3, PlayStation Portable, and PlayStation 2 consoles. Brian Johnson, Brian Orakpo, Mark Sanchez, and Michael Crabtree were the cover athletes for the game.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q8b70db518e",
  "kind": "yes/no",
  "text": "Text: I’ve seen a lot of people on local Facebook groups asking AirBnB owners if they have any availability recently. If only there was a website you could use to find out if an AirBnB was available 🤔",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q3b8a2207f1",
  "kind": "yes/no",
  "text": "Claim: Oregon has a college football team and a player from Pago Pago, American Samoa played for it.\n\nPassages:\n\n[Oregon Ducks football]\nThe Oregon Ducks football program is a college football team for the University of Oregon, located in the U.S. state of Oregon.\n\n[Matt Toeaina]\nHe is from Pago Pago, American Samoa and played college football at Oregon.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qdc96bf8190",
  "kind": "yes/no",
  "text": "Tweet: @pamparoni keyboard and mouse weigh nothing the monitors are a little iffy though",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qdbc9612bc3",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Day 1 in our new dystopian society is not going well",
   "I'm literally out here trading eggs for potatoes Day 1 in our new dystopian society is going well #coronavirusUK #coronavirus"
  ]
 },
 {
  "qid": "q415ea768e5",
  "kind": "yes/no",
  "text": "Claim: Enola Gay was one of the bombers that targeted the largest city on the Japanese island of Kyushu.\n\nPassages:\n\n[Enola Gay]\nClouds and drifting smoke resulted in a secondary target, Nagasaki, being bombed instead.\n\n[Nagasaki]\nNagasaki (長崎市 , Nagasaki-shi , ]) ( ) is the capital and the largest city of Nagasaki Prefecture on the island of Kyushu in Japan.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q25a50266fd",
  "kind": "yes/no",
  "text": "Text: Day 3 of night shift: “Can I get a triple shot puppuccinio?”",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qaec823a3b9",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "watching olympic womens beach volleyball for the plot",
   "I watch women's beach volleyball for the hot women."
  ]
 },
 {
  "qid": "q6b9ed75169",
  "kind": "yes/no",
  "text": "Claim: Pakenham, the satellite suburb of Melbourne is partially included in the Legislative Assembly seat Brian Paynter is representing.\n\nPassages:\n\n[Electoral district of Bass]\nIt covers an area of 1,383 sqkm south east of Melbourne, stretching from outer suburban Pakenham through rural areas to the coast at Inverloch and Phillip Island. It includes the towns of Bass, Cape Patterson, Corinella, Cowes, Grantville, Inverloch, Kilcunda, Koo Wee Rup, Lang Lang, Rhyll, San Remo, Ventnor, Wonthaggi, and part of suburban Pakenham.\n\n[Brian Paynter]\nHe has been a Liberal Party of Australia member of the Victorian Legislative Assembly since November 2014, representing the Legislative Assembly seat of Bass.\n\n[Pakenham, Victoria]\nPakenham is a satellite suburb of Melbourne on the edge of the West Gippsland region of Victoria, Australia, 56 km south-east of Melbourne's Central Business District, located within the Shire of Cardinia local government area.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc411589f51",
  "kind": "yes/no",
  "text": "Text: why is there part of a dead animal in the de courcy's arcade wheelie bin this morning? #fb",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q209b28fe2e",
  "kind": "yes/no",
  "text": "Claim: An actor who appeared in all eight \"American Pie Films\" also stared alongside John Candy in a film made by screenwriter Joe Seely.\n\nPassages:\n\n[Armed and Dangerous (1986 film)]\nArmed and Dangerous is a 1986 American action-crime comedy film starring John Candy, Eugene Levy, Robert Loggia and Meg Ryan.\n\n[Eugene Levy]\nHe is the only actor to have appeared in all eight of the \"American Pie\" films, in his role as Noah Levenstein.\n\n[Joe Seely]\nHis other films are \"Armed and Dangerous\", \"Tough Guys\", and \"Shag\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa2b1755600",
  "kind": "yes/no",
  "text": "Claim: Kamay Lau is best known as the failed hit lady in this movie. It was a 2005 crime thriller starring the American actor Jason Statham and was directed by a director. The driector also directed the 2019 film Aladdin.\n\nPassages:\n\n[Jason Statham]\nJason Statham ( born 26 July 1967) is an English actor, and a former model and competitive diver.\n\n[Aladdin (2019 film)]\nAladdin is an upcoming American musical romantic fantasy film directed by Guy Ritchie from a screenplay written by John August, Ritchie and Vanessa Taylor, and co-produced by Walt Disney Pictures, Lin Pictures, and Marc Platt Productions.\n\n[Kamay Lau]\nKamay Lau is a British actress, best known as the failed hitlady in \"Revolver\".\n\n[Revolver (2005 film)]\nRevolver is a 2005 British-French crime thriller film co-written and directed by Guy Ritchie and starring Jason Statham, Ray Liotta, Vincent Pastore and André Benjamin.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q921c2d9849",
  "kind": "yes/no",
  "text": "Text: i love siriusxm. siriusxm is my friend",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q731d9f84b6",
  "kind": "yes/no",
  "text": "Claim: A sports group's head coach was in his 6th season. This New England coach was the two time Walter Camp Coach of the Year winner who led the 2000 Oklahoma Sooners to an Orange Bowl victory. The sport's group defeated the Colorado Buffaloes in the 2004 Big 12 Championship Game.\n\nPassages:\n\n[2004 Oklahoma Sooners football team]\nThe team was led by two-time Walter Camp Coach of the Year Award winner, Bob Stoops, in his sixth season as head coach.\n\n[2015 Oklahoma Sooners football team]\nThe team was led by two-time Walter Camp Coach of the Year Award winner, Bob Stoops, in his 17th season as head coach.\n\n[2004 Big 12 Championship Game]\nThe #2 Oklahoma Sooners defeated the Colorado Buffaloes 42-3.\n\n[Bob Stoops]\nDuring the 2000 season, Stoops led the Sooners to an Orange Bowl victory and a national championship.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q15b23fe4fd",
  "kind": "yes/no",
  "text": "Claim: A band that collaborated in American Underdog was formed earlier than the Jon Spencer Blues Explosion.\n\nPassages:\n\n[Unwritten Law]\nUnwritten Law is an American rock band formed in 1990 in Poway, California They have released seven full-length studio albums and have toured internationally, including performances on the Warped Tour.\n\n[American Underdog]\nThis album includes collaborations with Daddy X, The Dirtball, Johnny Richter, Scott Russo of Unwritten Law, Jared of Hed PE, and John E. Necro.\n\n[Jon Spencer Blues Explosion]\nThe Jon Spencer Blues Explosion is an American alternative rock trio, formed in 1991 and based in New York City, New York.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q73ae74d0c2",
  "kind": "yes/no",
  "text": "Text: Here we go again! We are expecting! Our third baby is due Feb 2022! Absolutely terrified of having 2 under 2 and a 10 year old but we move baby! This is the last addition to the family so going to enjoy this for the very last time ❤️👶🏽",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qe1e2a18d97",
  "kind": "yes/no",
  "text": "Claim: Playwrights Eugène Ionesco and Paul Scott lived during the same time period.\n\nPassages:\n\n[Eugène Ionesco]\nEugène Ionesco (born Eugen Ionescu, ] ; 26 November 1909 – 28 March 1994) was a Romanian-French playwright who wrote mostly in French, and one of the foremost figures of the French Avant-garde theatre.\n\n[Paul Scott (novelist)]\nPaul Mark Scott (25 March 19201 March 1978) was an English novelist, playwright, and poet, best known for his monumental tetralogy \"The Raj Quartet.\"",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q1318648b30",
  "kind": "yes/no",
  "text": "Claim: The 2002 runner up sang two cover songs with Kelly Clarkson on American Idol: Greatest Moments.\n\nPassages:\n\n[Justin Guarini]\nJustin Guarini (born Justin Eldrin Bell; October 28, 1978) is an American singer/musician, actor, host and producer, who in 2002 was the runner-up on the first season of \"American Idol.\"\n\n[American Idol: Greatest Moments]\nAmerican Idol: Greatest Moments is the first \"American Idol\" soundtrack, with music from the first season of \"American Idol\". It contains two cover songs from both Kelly Clarkson and Justin Guarini, the winner and runner-up of the original season, one song from the remaining eight finalists, one song by all the finalists, and Clarkson's two songs from her debut single as bonus tracks.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q34e9fdcb6c",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "im about to just walk into a place and start working then and there and they'll have no choice but to hire me on the spot",
   "I wish someone would hire me so I don't have to go through hoops and hurdles."
  ]
 },
 {
  "qid": "qac1fb67566",
  "kind": "yes/no",
  "text": "Post: I haven’t used snap in so long and my short attention span/short term memory can’t keep track of what we’re talking about 😩",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qec5716a3ba",
  "kind": "yes/no",
  "text": "Claim: AEthelweard was an author of a Latin version of the collection of annals where everything known of Cynric comes from. The collection is written in the old language that includes words like Kine, which means weasel.\n\nPassages:\n\n[Æthelweard (historian)]\nÆthelweard (also Ethelward; d. c. 998), descended from the Anglo-Saxon King Æthelred I of Wessex, the elder brother of Alfred the Great, was an ealdorman and the author of a Latin version of the \"Anglo-Saxon Chronicle\" known as the \"Chronicon Æthelweardi\".\n\n[Cynric]\nEverything known about him comes from the \"Anglo-Saxon Chronicle\".\n\n[The Kine Saga]\nThe name \"Kine\" comes from an Old English word for the weasel.\n\n[Anglo-Saxon Chronicle]\nThe Anglo-Saxon Chronicle is a collection of annals in Old English chronicling the history of the Anglo-Saxons.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6b98b86689",
  "kind": "yes/no",
  "text": "Claim: SWX Right Now airs on the station that broadcasts on channel 8 in Billings, Montana.\n\nPassages:\n\n[SWX Right Now]\nThe channel is operated by Cowles Company and airs over Cowles' three NBC affiliated channels in Eastern Washington, including Spokane's KHQ, KNDO in Yakima and Richland's KNDU, as well as Billings' KULR in Montana, and on most cable systems throughout the markets they serve.\n\n[KULR-TV]\nKULR-TV, virtual channel 8, is an NBC affiliate broadcasting on channel 11 in Billings, Montana.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4d43527ded",
  "kind": "yes/no",
  "text": "Claim: The actor Thomas Gregory played in a drama television series based on Israeli series the \"Yellow Peppers\".\n\nPassages:\n\n[Thomas Gregory (actor)]\nThomas Gregory (born 10 November 1995) is an English actor who played Luke Taylor in BBC One drama \"The A Word\", first broadcast in March 2016.\n\n[The A Word]\nThe A Word is a BBC drama television series based on Israeli series the \"Yellow Peppers\" (פלפלים צהובים) by Keren Margalit.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9d1df2fbf9",
  "kind": "yes/no",
  "text": "Claim: A sporting event was announced by Brad Nessler and this former player. Wizard of Westwood is the nickname of the head coach on whose team the announcer played in the early 1970s. Wizard of Westwood is the nickname of the head coach on whose team the announcer played in the early 1970s. Luicios Harris played in the sporting event.\n\nPassages:\n\n[John Wooden]\nNicknamed the \"Wizard of Westwood,\" he won ten NCAA national championships in a 12-year period as head coach at UCLA, including a record seven in a row.\n\n[Lucious Harris]\nHe played in the 2002 and 2003 NBA Finals as a member of the Nets.\n\n[2003 NBA Finals]\nThe series was broadcast on U.S. television on ABC, with Brad Nessler, Bill Walton, and Tom Tolbert announcing.\n\n[Bill Walton]\nWalton became known playing for John Wooden's powerhouse UCLA Bruins in the early 1970s, winning three successive College Player of the Year Awards, while leading the Bruins to two Division I national titles.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q876f9d2c63",
  "kind": "yes/no",
  "text": "Claim: Israeli actress, Odeya Rush, is known for her lead role in 2015 American horror comedy film based on the children's book series created by R.L. Stine.\n\nPassages:\n\n[Goosebumps (film)]\nGoosebumps is a 2015 American horror comedy film based on the children's book series of the same name by R.L. Stine.\n\n[Odeya Rush]\nOdeya Rush (Hebrew: אודיה רש‎ ‎ ; born Odeya Rushinek; May 12, 1997) is an Israeli actress and model. She is known for her lead roles in \"The Giver\" (2014) and \"Goosebumps\" (2015).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1eaeb08936",
  "kind": "yes/no",
  "text": "Claim: Eli Roth, famous for his role as Donny \"The Bear Jew\" Donowitz, wrote the 2012 film that was directed by the founder of Soul Temple Records.\n\nPassages:\n\n[Eli Roth]\nEli Raphael Roth (born April 18, 1972) is an American film director, producer, writer, and actor. As an actor, his most prominent role was as Donny \"The Bear Jew\" Donowitz in Quentin Tarantino's war film \"Inglourious Basterds\" for which he won both a SAG Award (Best Ensemble) and a BFCA Critic's Choice Award (Best Acting Ensemble).\n\n[The Man with the Iron Fists]\nThe Man with the Iron Fists is a 2012 American martial arts film directed by RZA and written by RZA and Eli Roth.\n\n[Soul Temple Records]\nSoul Temple Records is an American record label founded in 2012 by hip hop music recording artist RZA and Bob Perry, after the release of the RZA directed \"The Man with the Iron Fists\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q66f1632c77",
  "kind": "yes/no",
  "text": "Post: I get a lot of boy who cried wolf vibes from the Red Cross and their emergency blood shortages all the time",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qff7f91e01c",
  "kind": "yes/no",
  "text": "Claim: The magazine Golf Digest has not been around longer than the publication which placed Daron Malakian 30th in their List of The 100 Greatest Heavy Metal Guitarists of All Time.\n\nPassages:\n\n[Daron Malakian]\nHe is placed 30th in Guitar World's List of The 100 Greatest Heavy Metal Guitarists of All Time.\n\n[Golf Digest]\nGolf Digest is a monthly golf magazine published by Condé Nast Publications in the United States. The magazine started in 1950, and was sold to The New York Times Company in 1969. The headquarters of \"Golf Digest\" is in Des Moines, Iowa.\n\n[Guitar World]\nGuitar World is a monthly music magazine devoted to guitarists, published since July 1980.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb7f61fccb6",
  "kind": "yes/no",
  "text": "Claim: In the 28th season a Spanish rally driver won the racing series which was competed in by Harri Rovanperä from the 1990's to the 2000's.\n\nPassages:\n\n[2000 World Rally Championship]\nThe 2000 World Rally Championship was the 28th season of the FIA World Rally Championship.\n\n[Harri Rovanperä]\nHe drove for SEAT (1997–00), Peugeot (2001–04), Mitsubishi (2005) and Red Bull Škoda Team (2006).\n\n[Carlos Sainz]\nCarlos Sainz Cenamor (born 12 April 1962 in Madrid, Spain) is a Spanish rally driver.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
