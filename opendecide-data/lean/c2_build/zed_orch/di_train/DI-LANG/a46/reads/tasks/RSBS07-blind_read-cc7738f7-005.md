# A46 replay label-noise blind read RSBS07-blind_read-cc7738f7-005

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS07-blind_read-cc7738f7-005.json

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
  "qid": "q176f7d0695",
  "kind": "yes/no",
  "text": "Claim: Neither the band that James McNally (musician) was a member of or another band are an electronic dance music group. Noah Henson was the lead guitarist for the other band.\n\nPassages:\n\n[Noah Henson]\nNoah Henson I (born April 18, 1981) is the lead guitarist for the Christian rock band Pillar.\n\n[The Pogues]\nThe Pogues were an Irish punk band formed in 1982 and fronted by Shane MacGowan.\n\n[Pillar (band)]\nPillar is a Christian rock band currently located in Tulsa, Oklahoma.\n\n[James McNally (musician)]\nHe was previously a member of The Pogues and Storm (with Tom McManamon).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q0354132476",
  "kind": "yes/no",
  "text": "Claim: Canada-native Gary Paulsen wrote the 1987 Newberry Honor-winning young-adult wilderness survival novel and the fifth and final novel of that same series, called Brian's Hunt.\n\nPassages:\n\n[Brian's Hunt]\nBrian's Hunt is a 2003 young adult novel by Gary Paulsen. It is the fifth and final book in the award-winning \"Hatchet\" series, which deals with Brian Robeson, a boy who learns wilderness survival when he is stranded after a plane wreck.\n\n[Hatchet (novel)]\nHatchet is a 1987 Newbery Honor-winning young-adult wilderness survival novel written by American writer Gary Paulsen.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qaa3b1801f5",
  "kind": "yes/no",
  "text": "Claim: Double Crossed was the name of Scottish singer-songwriter James Aaron Diamond's first solo album that debuted in 1985.\n\nPassages:\n\n[Jim Diamond (singer)]\nJames Aaron Diamond (28 September 1951 – 8 October 2015) was a Scottish singer-songwriter, best known for his three Top 5 hits.\n\n[Double Crossed]\nDouble Crossed was Jim Diamond's solo début album in 1985.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7d4ed6aa42",
  "kind": "yes/no",
  "text": "Post: B/w Rain is a Good Thing stuck in my my head, the heat &amp; #GladePlugIns going in the car, hard to believe it's not Summer! #Glade #GotItFree",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qe18ee50513",
  "kind": "yes/no",
  "text": "Claim: The person who introduced the British opera Tragédie en musique was an Italian-born British composer, instrumentalist, and dancer. He produced music for the British opera Thesee.\n\nPassages:\n\n[Jean-Baptiste Lully]\nJean-Baptiste Lully (] ; born Giovanni Battista Lulli ] ; 28 November 1632 – 22 March 1687) was an Italian-born French composer, instrumentalist, and dancer who spent most of his life working in the court of Louis XIV of France.\n\n[Thésée]\nThésée (\"Theseus\") is a \"tragédie en musique\", an early type of French opera, in a prologue and five acts with music by Jean-Baptiste Lully and a libretto by Philippe Quinault based on Ovid's \"Metamorphoses\".\n\n[Tragédie en musique]\nTragédie en musique (Musical tragedy), also known as tragédie lyrique (French lyric tragedy), is a genre of French opera introduced by Jean-Baptiste Lully and used by his followers until the second half of the eighteenth century.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qcdd611a976",
  "kind": "yes/no",
  "text": "Claim: 15 March 1983 is the birth date of the star of Igualita a mí named Adrian Suar.\n\nPassages:\n\n[Igualita a mí]\nIgualita a mí is a 2010 Argentine comedy film directed by Diego Kaplan and starring Florencia Bertotti and Adrián Suar.\n\n[Florencia Bertotti]\nMaría Florencia Bertotti ] ; (born 15 March 1983), better known as Florencia Bertotti, is an Argentine actress, singer and producer.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qbee09305e9",
  "kind": "yes/no",
  "text": "Claim: The writer of historical romance fiction to whom an 1850s novel was dedicated was born in London, England. The novel was one of four including \"A Countess Below Stairs\", \"The Reluctant Heiress\", and \"The Morning Gift\".\n\nPassages:\n\n[A Company of Swans]\nThe book is dedicated to Patricia Veryan.\n\n[A Song for Summer]\nThis novel and four others (\"A Countess Below Stairs\", \"A Company of Swans\", \"The Reluctant Heiress\", and \"The Morning Gift\") were reissued between 2007 and 2009 for the young adult market.\n\n[Patricia Veryan]\nPatricia Valeria Bannister, (born November 21, 1923 in London, England; died November 18, 2009 in Bellevue, Washington, USA) was a writer of historical romance fiction from 1978 until 2002.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q687088fe92",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "Old people don’t deserve rights",
   "old people suck"
  ]
 },
 {
  "qid": "q7b4248df6f",
  "kind": "yes/no",
  "text": "Claim: Cartoon Network distributed the first in it's series film which Rick Yune played a notable role in.\n\nPassages:\n\n[The Fast and the Furious]\nThe Fast and the Furious (also known as Fast & Furious) is an American franchise based on a series of action films that is largely concerned with illegal street racing and heists, and includes material in various other media that depicts characters and situations from the films. Distributed by Universal Pictures, the series was established with the 2001 film titled \"The Fast and the Furious\"; this was followed by seven sequels, two short films that tie into the series, and as of May 2017, it has become Universal's biggest franchise of all time, currently the sixth-highest-grossing film series of all time with a combined gross of over $5 billion.\n\n[Rick Yune]\nRick Yune is an American actor, screenwriter, producer, martial artist and former model. His most notable roles have been in the movies \"Snow Falling on Cedars\", the first \"Fast and Furious\" film \"The Fast and the Furious\", and in the James Bond movie \"Die Another Day\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qab7ba9e4c5",
  "kind": "yes/no",
  "text": "Claim: Bill Murray was the actor in the miniseries Jane Anderson wrote the screenplay for. He was also starring actor in the movie Caddyshack.\n\nPassages:\n\n[Olive Kitteridge (miniseries)]\nSet in Maine, the HBO miniseries features Frances McDormand as the title character, Richard Jenkins as Olive's loving husband Henry Kitteridge, Zoe Kazan as Denise Thibodeau, and Bill Murray as Jack Kennison.\n\n[Bill Murray]\nHe first gained exposure on \"Saturday Night Live\", a series of performances that earned him his first Emmy Award, and later starred in comedy films—including \"Meatballs\" (1979), \"Caddyshack\" (1980), \"Stripes\" (1981), \"Tootsie\" (1982), \"Ghostbusters\" (1984), \"Scrooged\" (1988), \"Ghostbusters II\" (1989), \"What About Bob?\n\n[Jane Anderson]\nShe won an Emmy Award for writing the screenplay for the miniseries \"Olive Kitteridge\" (2014).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qecb55584b6",
  "kind": "yes/no",
  "text": "Claim: The highway that the closest town to Montague Island is located on is Princes Highway.\n\nPassages:\n\n[Montague Island (Australia)]\nThe nearest town located onshore from the 81 ha reserve and island is Narooma , situated approximately 9 km to the northwest.\n\n[Narooma, New South Wales]\nThe town is on the Princes Highway and the name Narooma is said to be derived from the Aboriginal word meaning ‘clear blue waters’.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q830dfcffde",
  "kind": "yes/no",
  "text": "Claim: Rocky Boy's Indian Reservation is located in Hill and Chouteau and named after the principal leader of the Montana Chippewa-Cree.\n\nPassages:\n\n[Rocky Boy's Indian Reservation]\nRocky Boy's Indian Reservation is one of seven American Indian reservations in the U.S. state of Montana. The reservation is located in Hill and Chouteau counties in northeastern Montana, about 40 mi from the Canada–U.S. border.\n\n[Rocky Boy (Chippewa leader)]\nAsiniiwin, translated Rocky Boy or Stone Child was an important Chippewa leader who became the principal leader of the Montana Chippewa-Cree in the late 19th century and early 20th century.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q1521ea9878",
  "kind": "yes/no",
  "text": "Claim: \"Tennessee\" Williams, is known with Arthur Miller's and Arthur Miller, as one of the three foremost dramatists of the 20th century. The writer of \"Stella Bain\" is not.\n\nPassages:\n\n[Tennessee Williams]\nThomas Lanier \"Tennessee\" Williams III (March 26, 1911 – February 25, 1983) was an American playwright.\n\n[Anita Shreve]\nAnita Shreve (born 1946) is an American writer.\n\n[Stella Bain]\nStella Bain is an American novel by Anita Shreve, set in World War I.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qb062328b44",
  "kind": "yes/no",
  "text": "Post: Amazing show last night from @TheMovielifeNYC (w/ special guest @brettromnes!) - thanks @vinniecaruana, @BrandonReilly and Navetta Bros. !",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q97e782d688",
  "kind": "yes/no",
  "text": "Text: There's far too much \"imagine if you had kids\" talk and far too little \"imagine if you couldn't have kids\" talk.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qaa076e1ef2",
  "kind": "yes/no",
  "text": "Tweet: I can’t wait to hear more about the life of an upper middle class East Asian American whose only personality trait is drinking boba tea https://t.co/SapbXLd0r2",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qe8ed1f11d0",
  "kind": "yes/no",
  "text": "Claim: The Good Design philosophy is associated with the Danish furniture manufacturer Hans Jørgensen Wegner whose style is often described as Organic Functionality.\n\nPassages:\n\n[Hans Wegner]\nHans Jørgensen Wegner, (April 2, 1914 – January 26, 2007), was a world-renowned Danish furniture designer. His style is often described as Organic Functionality, a modernist school with emphasis on functionality.\n\n[Good Design]\nNames associated with the movement include Charles and Ray Eames, László Moholy-Nagy and Hans Wegner,",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qab02b77905",
  "kind": "yes/no",
  "text": "Claim: The political party that Kayithi Narsi Reddy associates with was founded in February 1885.\n\nPassages:\n\n[Indian National Congress]\nFounded in 1885, it was the first modern nationalist movement to emerge in the British Empire in Asia and Africa.\n\n[Kayithi Narsi Reddy]\nKayithi Narsi Reddy is an Indian politician initially associated with INC and then with YSR Congress Party.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3ed414b551",
  "kind": "yes/no",
  "text": "Claim: The 500 ft McCarthy Building was added to the National Register of Historic Places at the same time as the oldest building on Monument Square.\n\nPassages:\n\n[McCarthy Building (Troy, New York)]\nThe McCarthy Building is located on River Street on the west side of Monument Square in Troy, New York, United States. In 1970 it was added to the National Register of Historic Places in 1970, along with the nearby Cannon Building.\n\n[Cannon Building (Troy, New York)]\nIt is the oldest building on Monument Square. In 1970 it was listed on the National Register of Historic Places.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9d7a6938a6",
  "kind": "yes/no",
  "text": "Claim: The film To Hell and Back stars a combat solider that received the Medal of Honor at 19.\n\nPassages:\n\n[To Hell and Back (film)]\nIt was directed by Jesse Hibbs and starred Audie Murphy as himself.\n\n[Audie Murphy]\nMurphy received the Medal of Honor for valor demonstrated at the age of 19 for single-handedly holding off an entire company of German soldiers for an hour at the Colmar Pocket in France in January 1945, then leading a successful counterattack while wounded and out of ammunition.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2c06f97de3",
  "kind": "yes/no",
  "text": "Claim: Pinnacle Airlines Flight 3701 was headed to a freight airport when it crashed. That airport is farther east than Cheyenne Regional Airport.\n\nPassages:\n\n[Minneapolis–Saint Paul International Airport]\nMinneapolis–Saint Paul International Airport (IATA: MSP, ICAO: KMSP, FAA LID: MSP) , also known as Wold–Chamberlain Field, is a joint civil-military public use international airport.\n\n[Cheyenne Regional Airport]\nCheyenne Regional Airport (IATA: CYS, ICAO: KCYS, FAA LID: CYS) (Jerry Olson Field) is a civil-military airport a mile north of downtown Cheyenne, in Laramie County, Wyoming.\n\n[Pinnacle Airlines Flight 3701]\nIt was an overnight repositioning flight with no passengers from Little Rock, Arkansas, U.S. to Minneapolis–Saint Paul International Airport, U.S. Both crew members were killed.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q8e8bf64ef9",
  "kind": "yes/no",
  "text": "Claim: Night's Dark Terror is an adventure module co-written by a British game designer. This game designer has contributed to the single-player role-playing gamebook, the series that Eye of the Dragon is part of.\n\nPassages:\n\n[Jim Bambra]\nHe is particularly known for his contributions to \"Dungeons and Dragons\", \"Fighting Fantasy\", \"Warhammer\", and \"\" which was based on the \"Star Wars\" films.\n\n[Eye of the Dragon]\nIt forms part of Steve Jackson and Ian Livingstone's Fighting Fantasy series.\n\n[Night's Dark Terror]\nNight's Dark Terror is an adventure module for the \"Dungeons & Dragons\" (\"D&D\") fantasy role-playing game written by British game designers Jim Bambra, Graeme Morris, and Phil Gallagher.\n\n[Fighting Fantasy]\nFighting Fantasy is a series of single-player role-playing gamebooks created by Steve Jackson and Ian Livingstone.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q64f607625f",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "The typhoon flew over me today absolutely fuming they forgot to bomb me",
   "the typhoon flew over me today and i didnt get bombed"
  ]
 },
 {
  "qid": "qa4d70ac0b4",
  "kind": "yes/no",
  "text": "Claim: An athlete played defensive lineman for the team Rodney Hannah plays for. The college this athlete played at is located in Louisiana.\n\nPassages:\n\n[1983 Dallas Cowboys season]\nHowever, the defense gave up many points, despite strong play from Randy White, Ed \"Too Tall\" Jones, and Everson Walls.\n\n[Everson Walls]\nHe played college football at Grambling State University.\n\n[Grambling State University]\nGrambling State University (GSU) is a historically black, public, coeducational university, located in Grambling, Louisiana.\n\n[Rodney Hannah]\nRodney Dee Hannah II (born August 9, 1987) is a former American football tight end in the National Football League for the Dallas Cowboys.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8a3cb6f99c",
  "kind": "yes/no",
  "text": "Claim: This individual played with Steve Denton in the 1983 Dallas Open – Doubles. He and Ekaterina Makarova are not from the same country.\n\nPassages:\n\n[Sherwood Stewart]\nSherwood Stewart (born June 6, 1946, in Goose Creek, Texas, United States) played amateur and professional tennis in the 1970s and 1980s.\n\n[Ekaterina Makarova]\nEkaterina Valeryevna Makarova (Russian: Екатери́на Вале́рьевна Мака́рова ; ] ; born on 7 June 1988) is a Russian professional tennis player.\n\n[1983 Dallas Open – Doubles]\nNduka Odizor and Van Winitsky won in the final 6–3, 7–5 against Steve Denton and Sherwood Stewart.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q438783925b",
  "kind": "yes/no",
  "text": "Claim: William Paul \"Bill\" Barretta made film debut as a principal puppeteer in a movie as Clueless I Shrunk the Kids. That movie was produced after the film where Kristine Sutherland starred as Mrs Thompson.\n\nPassages:\n\n[Kristine Sutherland]\nKristine Sutherland (born Kristine Young; April 17, 1955) is an American actress best known for her starring as Buffy Summers' mother Joyce Summers on the television show \"Buffy The Vampire Slayer\", where she appeared in every season, and her role as Mrs. Thompson in \"Honey, I Shrunk the Kids\" (1989).\n\n[Muppet Treasure Island]\nMuppet Treasure Island is a 1996 American musical adventure comedy film based on Robert Louis Stevenson's \"Treasure Island\".\n\n[Honey, I Shrunk the Kids]\nHoney, I Shrunk the Kids is a 1989 American comic science fiction film.\n\n[Bill Barretta]\nHis film debut as a principal puppeteer was in 1996's \"Muppet Treasure Island\" as Clueless Morgan.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7329abe45f",
  "kind": "yes/no",
  "text": "Claim: John Roger Kirkpatrick Scott was a member of the U.S. House of Representatives from a Commonwealth that borders New Jersey to the east.\n\nPassages:\n\n[Pennsylvania]\nPennsylvania (Pennsylvania German: \"Pennsylvaani\" or \"Pennsilfaani\"), officially the Commonwealth of Pennsylvania, is a state located in the northeastern and Mid-Atlantic regions of the United States. The Commonwealth borders Delaware to the southeast, Maryland to the south, West Virginia to the southwest, Ohio to the west, Lake Erie and the Canadian province of Ontario to the northwest, New York to the north, and New Jersey to the east.\n\n[John Roger Kirkpatrick Scott]\nJohn Roger Kirkpatrick Scott (July 6, 1873 – December 9, 1945) was a Republican member of the U.S. House of Representatives from Pennsylvania.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q445f5ddd46",
  "kind": "yes/no",
  "text": "Post: See Brexit is going well",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q10f7710087",
  "kind": "yes/no",
  "text": "Claim: The director of Tiempo de morir is from a country closer to United Kingdom that Bahman Ghobadi is. Tiempo de morir means time to die.\n\nPassages:\n\n[Arturo Ripstein]\nArturo Ripstein y Rosen (born December 13, 1943) is a Mexican film director.\n\n[Bahman Ghobadi]\nHe was born on February 1, 1969 in Baneh, Kurdistan province.\n\n[Tiempo de morir]\nTiempo de Morir (Time to Die) is a 1966 Mexican Western film directed by Arturo Ripstein and starring Marga López and Jorge Martínez de Hoyos.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc800caddde",
  "kind": "yes/no",
  "text": "Claim: Petals on the Wind (film) is the sequel to the movie that starred Kiernan Brennan known for playing Monica Shaw on Mad Men.\n\nPassages:\n\n[Kiernan Shipka]\nKiernan Brennan Shipka (born November 10, 1999) is an American actress. She is known for playing Sally Draper on the AMC series \"Mad Men.\"\n\n[Petals on the Wind (film)]\nPetals on the Wind is a 2014 Lifetime movie sequel to the 2014 adaptation \"Flowers in the Attic\", starring Heather Graham, Rose McIver, Wyatt Nash, Bailey Buntain and Ellen Burstyn.\n\n[Flowers in the Attic (2014 film)]\nFlowers in the Attic is a 2014 Lifetime movie, starring Kiernan Shipka, Ellen Burstyn, Mason Dye, and Heather Graham.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2d6bad9864",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Well done Henri, cost us the win #nffc",
   "Terrible Henri, you cost us the win."
  ]
 },
 {
  "qid": "q690446e306",
  "kind": "yes/no",
  "text": "Claim: Matt Groening was born on February 15, 1954, he was the writer of the episode that featured the debut of the character voiced by Herbert Blöcker. The character unintentionally allows a zookeeper to exploit his babies in Eight Misbehavin'.\n\nPassages:\n\n[Matt Groening]\nMatthew Abraham \"Matt\" Groening ( ; born February 15, 1954) is an American cartoonist, writer, producer, animator, and voice actor.\n\n[The Telltale Head]\nIt was written by Al Jean, Mike Reiss, Sam Simon and Matt Groening, and directed by Rich Moore.\n\n[Apu Nahasapeemapetilon]\nHe is voiced by Hank Azaria and first appeared in the episode \"The Telltale Head\".\n\n[Eight Misbehavin']\nIn the episode, after Manjula gives birth to octuplets that were the result of fertility drugs, she and Apu unintentionally allow a zookeeper to exploit their babies in exchange for help after corporate sponsors abandon them for a mom that has given birth to nonuplets.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qd72fed2298",
  "kind": "yes/no",
  "text": "Claim: St. Johns in Florida is the airport associated with transportation in Jacksonville, Florida.\n\nPassages:\n\n[Transportation in Jacksonville, Florida]\nA major bus terminal at the intermodal Rosa Parks Transit Station serves as JTA's main transit hub.\n\n[Jacksonville International Airport]\nJacksonville International Airport (IATA: JAX, ICAO: KJAX, FAA LID: JAX) is a civil-military public airport 13 miles (21 km) north of Downtown Jacksonville, in Duval County, Florida.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa9a1e4995d",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I hate leaving the doctors office crying.",
   "I love leaving the doctors office in tears. I need this kid to just decide to leave my body so we can be done and home together."
  ]
 },
 {
  "qid": "q3571444fd7",
  "kind": "yes/no",
  "text": "Text: Wizkid is the king, ok lol",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qe88dc8e1d5",
  "kind": "yes/no",
  "text": "Claim: Mervyn Leroy was a music producer. The writer and director of Surviving Desire was also a producer.\n\nPassages:\n\n[Hal Hartley]\nHal Hartley (born November 3, 1959) is an American film director, screenwriter, producer and composer who became a key figure in the American independent film movement of the 1980s and '90s.\n\n[Mervyn LeRoy]\nMervyn LeRoy (October 15, 1900 – September 13, 1987) was an American film director, film producer and occasional actor.\n\n[Surviving Desire]\nSurviving Desire is a 1991 American comedy-drama film written and directed by Hal Hartley.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qc609f8d043",
  "kind": "yes/no",
  "text": "Claim: The Italian coach of the team, that won the 2008 Texas vs. Texas Tech football game , was born March 9, 1961.\n\nPassages:\n\n[2008 Texas Tech Red Raiders football team]\nThe team was coached by Mike Leach.\n\n[2008 Texas vs. Texas Tech football game]\nThe 2008 Texas vs. Texas Tech football game was a Big 12 Conference game played between the Texas Longhorns and Texas Tech Red Raiders at Jones AT&T Stadium in Lubbock, Texas, United States.\n\n[Mike Leach (American football coach)]\nMichael Charles Leach (born March 9, 1961) is an American college football coach.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6c9f512469",
  "kind": "yes/no",
  "text": "Claim: Both the genus that Chengiopanax sciadophylloides was previously included in and another flowering bulb plant are hardy genus. Hippeastrum puniceum is not a species of this genus.\n\nPassages:\n\n[Eleutherococcus]\nEleutherococcus is a genus of 38 species of thorny shrubs and trees in the family Araliaceae.\n\n[Amaryllis]\nAmaryllis ( ) is the only genus in the subtribe Amaryllidinae (tribe Amaryllideae).\n\n[Hippeastrum puniceum]\nCommon names include Barbados lily, Easter lily, cacao lily, cocoa lily and amaryllis lily, although it is neither a lily nor a species of \"Amaryllis\".\n\n[Chengiopanax sciadophylloides]\nPreviously included in the genus \"Eleutherococcus\", it is distinguished from other members of that genus by not having spines or prickles and ITS sequence data confirmed the separation.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qee8ff8bd87",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "I like the idea of stealing a car in order to elope, but can't drive and it's illegal - so I wouldn't do that.",
   "Serious question: if I nick a car and elope to Gretna Green to shut my family up, how long will I do in prison? Can I finish my PhD there? Think I've got a plan, lads..."
  ]
 },
 {
  "qid": "q0e2cb586fc",
  "kind": "yes/no",
  "text": "Claim: The company Mats Jansson is Chief Executive Officer of is a military airline holding company located in Solna Municipality, Sweden that owns a technical aircraft maintenance company located in Arlanda, Sweden.\n\nPassages:\n\n[SAS Technical Services]\nThe company is owned by the SAS Group and provides technical maintenance of aircraft to airlines in and outside the SAS Group. It is headquartered at Arlanda outside Stockholm and has 3,600 employees.\n\n[Mats Jansson]\nHe was Chief Executive Officer of SAS Group from 2007 to 2010.\n\n[SAS Group]\nScandinavian Airlines System Aktiebolag (, Nasdaq: SAS , ), trading as SAS Group and SAS AB, is an airline holding company headquartered in the SAS Frösundavik Office Building in Solna Municipality, Sweden. It also owns the aviation services companies SAS Business Opportunities, SAS Cargo Group, SAS Ground Services, and SAS Technical Services. SAS Group is partially owned by the governments of Sweden, Denmark, and Norway, with a 21.4%, 14.3%, and 14.3% ownership, respectively.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qe1c0eb77c3",
  "kind": "yes/no",
  "text": "Claim: Yes, both the magazine Ángel Manuel Rodríguez authors in and this publication have a headquarter or editor based in Nova. This publication featured Carol Weston as an advice columnist.\n\nPassages:\n\n[Girls' Life (magazine)]\nThe magazine is headquartered in Baltimore, Maryland.\n\n[Carol Weston]\nThe author of sixteen books, both fiction and non-fiction, she has been the \"Dear Carol\" advice columnist at Girls' Life since the magazine's first issue in 1994.\n\n[Adventist World]\nEditors are based in Silver Spring, Maryland and Seoul, Korea.\n\n[Ángel Manuel Rodríguez]\nHe has written several books, and authors a monthly column in \"Adventist World\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc1d21c655f",
  "kind": "yes/no",
  "text": "Text: Stop gatekeeping retirement living communities. I am mentally and spiritually ready to move in.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q964d13ba1c",
  "kind": "yes/no",
  "text": "Claim: The airline operating in Whitehorse, Yukon handled 294,000 passengers in 2012.\n\nPassages:\n\n[Erik Nielsen Whitehorse International Airport]\nThe terminal handled 294,000 passengers in 2012, representing a 94% increase in passenger traffic since 2002.\n\n[Air North]\nIts main base is Erik Nielsen Whitehorse International Airport.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa1ccd8dfdf",
  "kind": "yes/no",
  "text": "Claim: Judy Hample is a former chancellor of this educational organization. The organization and State University System of this state, for which Elwyn Thomas was a the Florida Board of Control from 1938 to 1969, have the United States in common.\n\nPassages:\n\n[Elwyn Thomas]\nElwyn Thomas (July 5, 1894 – February 15, 1971) was a Florida judge, and a Justice of the Florida Supreme Court from 1938 to 1969.\n\n[Judy Hample]\nShe is the former chancellor of the Pennsylvania State System of Higher Education and the Florida Board of Regents.\n\n[Florida Board of Regents]\nThe Florida Board of Regents was from 1965 to 2001 the governing body for the State University System of Florida, which includes all public universities in the state of Florida, United States.\n\n[State University System of Florida]\nThe State University System of Florida (SUS, or SUSF out-of-state) is a system of twelve public universities in the U.S. state of Florida.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q0e9f5bbb09",
  "kind": "yes/no",
  "text": "Claim: Marc Shiller, who was born in Beunos Aires in the 1950s, but is a resident of the United States, belongs to the ethnic group, that includes Paz Lenchantin.\n\nPassages:\n\n[Paz Lenchantin]\nPaz Lenchantin (born December 12, 1973) is an Argentine American musician.\n\n[Marc Schiller]\nMarc Schiller is an Argentinian American man who was born in Buenos Aires, Argentina in 1957. He survived a kidnapping and attempted murder by the Sun Gym Gang in Miami, Florida in 1994.\n\n[Argentine Americans]\nArgentine Americans (Spanish: Argentino Americanos ) are Americans whose full or partial origin is in Argentina.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qb5569d25b6",
  "kind": "yes/no",
  "text": "Claim: The actor who starred in Sugarfoot was born on January 23, 1898.\n\nPassages:\n\n[Randolph Scott]\nGeorge Randolph Scott (January 23, 1898 – March 2, 1987) was an American film actor whose career spanned from 1928 to 1962.\n\n[Sugarfoot (film)]\nSugarfoot is a 1951 western film starring Randolph Scott as Jackson 'Sugarfoot' Redan and featuring Adele Jergens and Raymond Massey.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc6a3501dd1",
  "kind": "yes/no",
  "text": "Tweet: @tylerthecreator @staci_zr can i use this chiamus for my ap lang speech about parallelism lmao",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q33d2ddd351",
  "kind": "yes/no",
  "text": "Claim: The first solo art exhibition of the author of the book was in 1943. The book inspired a film. The film featured \"The Comet Song\".\n\nPassages:\n\n[Tove Jansson]\nHer first solo art exhibition was in 1943.\n\n[Moomins and the Comet Chase]\nMoomins and the Comet Chase is a 2010 3D stop motion animated fantasy adventure comedy family film compiled from the \"Comet in Moominland\"-based episodes of the 1977–1982 \"The Moomins\" TV series animated at Se-ma-for in Poland, restored and re-soundtracked with multiple voice actors replacing the single narrator.\n\n[Comet in Moominland]\nComet in Moominland (Swedish: \"Kometjakten\" / \"Mumintrollet på kometjakt\" / \"Kometen kommer\") is the second in Tove Jansson's series of Moomin books.\n\n[The Comet Song]\n\"The Comet Song\" is a song by Icelandic artist Björk, written by herself and long-time friend and collaborator Sjón as the title theme of the 2010 movie \"Moomins and the Comet Chase\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q5936a83077",
  "kind": "yes/no",
  "text": "Text: If anyone wants to know how my nights going I tried making a private story on Snapchat and instead made a group chat... I hate my life",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qdca86415cf",
  "kind": "yes/no",
  "text": "Claim: Brickyard is the call sign of the airline that operates the flight with United Express Flight 3411 incident.\n\nPassages:\n\n[United Express Flight 3411 incident]\nRepublic Airline operated the scheduled passenger flight on behalf of United Express, a United Airlines regional branch.\n\n[Republic Airline]\nIts call sign \"Brickyard\" is derived from the nickname of the Indianapolis Motor Speedway.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 }
]
