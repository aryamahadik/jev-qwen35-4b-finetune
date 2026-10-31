# A46 replay label-noise blind read RSBS11-blind_read-5b09a463-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS11-blind_read-5b09a463-006.json

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
  "qid": "qebbcc6ead8",
  "kind": "yes/no",
  "text": "Claim: The person from Albania who is known for the 1980 film Cannibal Holocaust and Mexican Alejandro Springall, are both film directors.\n\nPassages:\n\n[Alejandro Springall]\nAlejandro Springall is a Mexican film director and producer.\n\n[Ruggero Deodato]\nRuggero Deodato (born 7 May 1939) is an Italian film director, screenwriter, and actor.\n\n[Cannibal Holocaust]\nCannibal Holocaust is a 1980 Italian cannibal horror film directed by Ruggero Deodato from a screenplay by Gianfranco Clerici.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q64feaa4cb6",
  "kind": "yes/no",
  "text": "Claim: The actress stars in a 2013 film. Shim Hyung-rae directed the film that she starred in in 2007. Shim Hyung-rae directed the film that she starred in in 2007. The 2013 film starred Lauren Shacher.\n\nPassages:\n\n[Amanda Brooks]\nAmanda Brooks (born June 22, 1981) is an actress who starred in the 2007 film \"D-War\" and in the 2006 film \"Cut Off\".\n\n[The Canyons (film)]\nThe film is set in Los Angeles and stars Lindsay Lohan, James Deen, Nolan Funk, Amanda Brooks, and Gus Van Sant.\n\n[D-War]\nD-War (Korean: 디워, released in North America as Dragon Wars: D-War), is a 2007 South Korean action-adventure fantasy film written and directed by Shim Hyung-rae, and starring Jason Behr, Amanda Brooks, Robert Forster, and Elizabeth Peña.\n\n[Lauren Schacher]\nLauren Schacher (born August 2, 1985) is an American actress and screenwriter most known for her role in Paul Schrader's \"The Canyons\" and as a co-founder of podcast \"Chicks Who Script\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q48716bee0f",
  "kind": "yes/no",
  "text": "Post: @BarbosaBox The best thing is Greg Paul’s face in the back",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qf655e2bc0e",
  "kind": "yes/no",
  "text": "Post: day 5 of people being mad about ellen sitting by gw bush is when we'll finally get to the bottom of this",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q3768327d66",
  "kind": "yes/no",
  "text": "Claim: Karl von Eberstein and Sturmabteilung are related by the Nazi Party as artistic goose steppers.\n\nPassages:\n\n[Karl von Eberstein]\nFriedrich Karl Freiherr von Eberstein (14 January 1894 – 10 February 1979) was a member of the German nobility, early member of the Nazi Party, the SA, and the SS (introducing Reinhard Heydrich to Heinrich Himmler in July 1931).\n\n[Sturmabteilung]\nThe Sturmabteilung (SA; ] ), literally Storm Detachment, functioned as the original paramilitary wing of the Nazi Party (NSDAP).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qd271e44f5b",
  "kind": "yes/no",
  "text": "Claim: The First Lady who inaugurated the National Arts Center is the person known also as Jane Ryan, and has a highway in the Philippines name after her.\n\nPassages:\n\n[Felix Avenue]\nF.P. Felix Avenue, also known as Imelda Avenue, is a four-lane major road which connects Marcos Highway to Ortigas Avenue Extension. The road is named after Francisco P. Felix, a former mayor of Cainta, and Imelda Marcos, the wife of the former President Ferdinand Marcos and former First Lady.\n\n[Imelda Marcos]\nShe remains one of the richest politicians in the Philippines through her collection of clothing, artwork, and jewelry, along with money in offshore bank accounts under the pseudonym \"Jane Ryan\".\n\n[National Arts Center]\nThe establishment was inaugurated in 1976 by First Lady Imelda Marcos.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q2b47ff1425",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Actually considering applying for the undateables",
   "Why is my lovelife so dead?"
  ]
 },
 {
  "qid": "q6ec3ee2d3c",
  "kind": "yes/no",
  "text": "Post: I don’t get the whole Bishop Sycamore thing. I literally have nightmares about being a grown man and playing high school football again, I don’t get why anybody would choose to do that willingly",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q0d348e0a63",
  "kind": "yes/no",
  "text": "Tweet: The amount of times I had to present my intern badge to Capitol Police officers who saw me every day for months and these people are just breaking in like it’s nothing smh",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qacf6ebb067",
  "kind": "yes/no",
  "text": "Claim: ICI House is now named after the company that provides explosives.\n\nPassages:\n\n[Orica]\nOrica Limited () is an Australian-based multinational corporation that is one of the world’s largest provider of commercial explosives and blasting systems to the mining, quarrying, oil and gas and construction markets, a supplier of sodium cyanide for gold extraction, and a specialist provider of ground support services in mining and tunnelling.\n\n[ICI House]\nICI House (now Orica House) is a 19-storey office building in East Melbourne, Victoria, Australia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe89aa89288",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Frank Ocean really did something with this new music.",
   "our lord and savior, frank ocean, has saved us all once again."
  ]
 },
 {
  "qid": "qa6732e750f",
  "kind": "yes/no",
  "text": "Post: I accidentally made butter when trying to whip cream this morning and I think that’s a great representation of how I’ve reached my capacity for working from home",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q9bc4c7ecd3",
  "kind": "yes/no",
  "text": "Post: \"are you experiencing suicidal or homicidal ideation?\"\n\"only while trying to talk to a human when I call @Walgreens pharmacy\"",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q26c98861cc",
  "kind": "yes/no",
  "text": "Claim: Caroline Grace Cassidy is best known for her role in the film which Ben Best was the co-writer. The director of this movie and Larry Hagman are not both actors.\n\nPassages:\n\n[Ben Best (screenwriter)]\nHe also co wrote the films \"The Foot Fist Way\" and \"Your Highness\".\n\n[Larry Hagman]\nLarry Martin Hagman (September 21, 1931 November 23, 2012) was an American film and television actor, director and producer best known for playing ruthless oil baron J.R. Ewing in the 1980s primetime television soap opera \"Dallas\" and befuddled astronaut Major Anthony \"Tony\" Nelson in the 1960s sitcom, \"I Dream of Jeannie\".\n\n[Caroline Grace Cassidy]\nShe is best known for her role in David Gordon Green's \"Your Highness\".\n\n[David Gordon Green]\nDavid Gordon Green (born April 9, 1975) is an American filmmaker.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q00217f9a90",
  "kind": "yes/no",
  "text": "Claim: Cliburn railway halt was a station situated on This railway that ran between Clifton Junction junction Penrith and Kirkby Stephen via Appleby-in-Westmorland.\n\nPassages:\n\n[Eden Valley Railway]\nIt ran between Clifton Junction near Penrith and Kirkby Stephen via Appleby-in-Westmorland.\n\n[Cliburn railway station]\nCliburn railway station was a station situated on the Eden Valley Railway in Cumbria, England.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7d5e5adab6",
  "kind": "yes/no",
  "text": "Text: I couldn’t have imagined how much fun I would have with people I’ve met through streaming. I’m so thankful to live in this timeline even if it is relatively garbage.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qd83b19b403",
  "kind": "yes/no",
  "text": "Claim: Gin and tonic is usually garnished with a slice of lime. The soda that's name was invented in an establishment is not garnished this way. Henry Bain sauce was first served at this establishment.\n\nPassages:\n\n[Gin and tonic]\nA gin and tonic is a highball cocktail made with gin and tonic water poured over ice. It is usually garnished with a slice or wedge of lime.\n\n[Henry Bain sauce]\nHenry Bain sauce is a condiment for meats, first served at the Pendennis Club in Louisville, Kentucky.\n\n[Old Fashioned]\nThe Old Fashioned is a cocktail made by muddling sugar with bitters, then adding alcohol, such as whiskey or brandy, and a twist of citrus rind.\n\n[Pendennis Club]\nSometime in the 1880s, the club was the birthplace (by name, not invention) of the Old Fashioned, possibly the first mixed drink to be called a cocktail.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1fc7ca298e",
  "kind": "yes/no",
  "text": "Tweet: happy one year vegetarian to me ❤️🌱",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qde8dd49f82",
  "kind": "yes/no",
  "text": "Claim: The writer and director of Beloved Rogues and David Fincher are both in the film industry.\n\nPassages:\n\n[Alfred Santell]\nAlfred Allen Santell also known as Al Santell (born September 14, 1895 in San Francisco, California) was an American film director and film producer.\n\n[David Fincher]\nDavid Andrew Leo Fincher (born August 28, 1962) is an American director and producer, notably for films, television series and music videos.\n\n[Beloved Rogues]\nBeloved Rogues is a 1917 American silent comedy-drama film directed and written by Alfred Santell with the storyline by Aaron Hoffman.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8185d5a976",
  "kind": "yes/no",
  "text": "Claim: Francis Key Hunt was named after the British poet who was born at the historic home, Terra Rubra. That poet wrote a poem entitled at first \"The Defence of Fort McHenry\".\n\nPassages:\n\n[Terra Rubra]\nIt was the birth site of Francis Scott Key in 1779.\n\n[Francis Scott Key]\nFrancis Scott Key (August 1, 1779January 11, 1843) was an American lawyer, author, and amateur poet from Frederick, Maryland and later Georgetown, D.C., near Washington, D.C. who wrote the lyrics for a poem entitled at first \"The Defence of Fort McHenry\", which when set to an old English gentlemens' society tune, eventually became the United States' national anthem, \"The Star-Spangled Banner\".\n\n[Loudoun House]\nDesigned by New York architect Alexander Jackson Davis, the house was built in 1851 for Francis Key Hunt (1817–1879), who was named after his mother's cousin, Francis Scott Key.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf78be53f67",
  "kind": "yes/no",
  "text": "Claim: The place where \"Shout! The Legend of The Wild One\" premiered in 1999 is part of a performing arts centre located in the Australian suburb of Southbank.\n\nPassages:\n\n[Shout! The Legend of The Wild One]\nIt premiered in Melbourne at the State Theatre in December 2000, before seasons in Sydney, Adelaide and Brisbane through 2001.\n\n[Arts Centre Melbourne]\nThe Arts Centre Melbourne, originally known as the Victorian Arts Centre and briefly officially called the Arts Centre, is a performing arts centre consisting of a complex of theatres and concert halls in the Melbourne Arts Precinct, located in the central Melbourne suburb of Southbank in Victoria, Australia.\n\n[State Theatre (Melbourne)]\nThe State Theatre opened in 1984 and is part of the Arts Centre Melbourne located by the Yarra River and St Kilda Road.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q13d875719b",
  "kind": "yes/no",
  "text": "Claim: A small regional passenger airline from Killeen, Texas moved its operations from a city owned public airport 6 miles northwest of Downtown Dallas to Dallas/Fort Worth International Airport.\n\nPassages:\n\n[Rio Airways]\nRio Airways was a regional passenger airline headquartered in Killeen, Texas, United States, which was operational from 1967 to 1987. Prior to operations at DFW it operated at Dallas Love Field, having its roots in two smaller commuter air carriers, Dal Airways and Hood Airways.\n\n[Dallas Love Field]\nDallas Love Field (IATA: DAL, ICAO: KDAL, FAA LID: DAL) is a city-owned public airport 6 miles (10 km) northwest of downtown Dallas, Texas. It was Dallas' main airport until 1974 when Dallas/Fort Worth International Airport (DFW) opened.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q4cc5d34937",
  "kind": "yes/no",
  "text": "Claim: Brisingr is the third novel in the trilogy \"Inheritance Cycle\", a young adult tetralogy of high fantasy novels written by the American author Christopher Paolini.\n\nPassages:\n\n[Brisingr]\nBrisingr is the third novel in the \"Inheritance Cycle\" by Christopher Paolini.\n\n[Inheritance Cycle]\nThe Inheritance Cycle is a young adult tetralogy of high fantasy novels written by American author Christopher Paolini.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q56fe3e81ec",
  "kind": "yes/no",
  "text": "Claim: The movie co-directed by Lee Unkrich and the singalong \"Mary Poppins\" are both made by the same company.\n\nPassages:\n\n[Monsters, Inc.]\nMonsters, Inc. is a 2001 American computer-animated comedy film produced by Pixar Animation Studios and distributed by Walt Disney Pictures.\n\n[Mary Poppins (film)]\nMary Poppins is a 1964 American musical-fantasy film directed by Robert Stevenson and produced by Walt Disney, with songs written and composed by the Sherman Brothers.\n\n[Lee Unkrich]\nAfter co-directing \"Monsters, Inc.\" and \"Finding Nemo\", Unkrich made his solo directorial debut with \"Toy Story 3\", for which he won the Academy Award for Best Animated Film in 2011.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa81558ec6a",
  "kind": "yes/no",
  "text": "Claim: The Garrick Club is a gentlemen's club in the heart of London founded in 1831, since its conception has catered to members such as English actor and theatre manager Sir Herbert Beerbohm Tree, that died on 2 July 1917.\n\nPassages:\n\n[Garrick Club]\nIt is one of the oldest, most highly esteemed and most exclusive members' clubs in the world and since its conception has catered to members such as Charles Kean, Henry Irving, Herbert Beerbohm Tree, Arthur Sullivan, Laurence Olivier and John Gielgud.\n\n[Herbert Beerbohm Tree]\nSir Herbert Beerbohm Tree (17 December 1852 – 2 July 1917) was an English actor and theatre manager.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q53ab1136f1",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "me: trying to sleep slightly earlier than usual bc I feel like shit my friend, texting the group chat 13 separate times at nearly 4am: hello I don’t think so! how abt I tell u abt how bad things are going instead :)",
   "I might say “I am so annoyed that my roommate won’t stop venting to me when I’m trying to sleep, I already don’t feel good and was trying to sleep Early for Self Care and having them bombard me with their problems at 4am is really putting a damper on things”"
  ]
 },
 {
  "qid": "q606df80524",
  "kind": "yes/no",
  "text": "Claim: Princess of Wales Isabella Kelly was born at a ruined castle characterized as one of the most isolated fortifications in Britain by The Changing Scottish Landscape.\n\nPassages:\n\n[Cairnburgh Castle]\nCairnburgh Castle is a ruined castle that is located on the islands of Cairn na Burgh Mòr and Cairn na Burgh Beag, Argyll and Bute, Scotland. 1991's \"The Changing Scottish Landscape\" characterizes it as \"one of the most isolated fortifications in Britain...[and] also one of the strangest.\"\n\n[Isabella Kelly]\nIsabella Kelly, née Fordyce, also Isabella Hedgeland (born at Cairnburgh Castle in the Scottish Highlands and baptised on 4 May 1759 – died on 25 June 1857 in London) was a Scottish novelist and poet.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qdd099b9f0d",
  "kind": "yes/no",
  "text": "Claim: Lilli Cooper and Fiorello H. LaGuardia High School have New York City in common.\n\nPassages:\n\n[Lilli Cooper]\nLilli Cooper is a New York City-born actress who played Elphaba in the Australian Tour of Wicked as the standby.\n\n[Fiorello H. LaGuardia High School]\nFiorello H. LaGuardia High School of Music & Art and Performing Arts is a high school specializing in teaching visual arts and performing arts, situated near Lincoln Center in the Lincoln Square neighborhood of the Upper West Side, Manhattan, New York City, in the U.S. state of New York.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qe96a575697",
  "kind": "yes/no",
  "text": "Claim: Kind Hearts and Coronets was the name of the 1949 British black comedy film that the hotel popular for Dirty weekends appeared on.\n\nPassages:\n\n[Kind Hearts and Coronets]\nKind Hearts and Coronets is a 1949 British black comedy film.\n\n[Skindles]\nThe hotel appears in the film Kind Hearts and Coronets.\n\n[Dirty weekend]\nPlaces which became famous for this include Brighton and the Skindles hotel in Maidenhead.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q9f516d3050",
  "kind": "yes/no",
  "text": "Claim: Australian National Airways was founded by the person who made the first trans-Pacific flight in 1928.\n\nPassages:\n\n[Charles Kingsford Smith]\nIn 1928, he earned global fame when he made the first trans-Pacific flight from the United States to Australia.\n\n[Australian National Airways (1930)]\nAustralian National Airways was a short-lived Australian airline, founded in 1929 by Charles Kingsford Smith and Charles Ulm.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q6a6386ca23",
  "kind": "yes/no",
  "text": "Claim: The director who gave Lee Van Cleef a role in \"For a Few Dollars More\" was the Italian, Jon Paul Puno.\n\nPassages:\n\n[Sergio Leone]\nSergio Leone (] ; 3 January 1929 – 30 April 1989) was an Italian film director, producer and screenwriter, credited as the inventor of the \"Spaghetti Western\" genre.\n\n[Lee Van Cleef]\nAfter suffering serious injuries in a car crash, Van Cleef began to lose interest in his apparently waning career by the time Sergio Leone gave him a major role in \"For a Few Dollars More\".\n\n[Jon Paul Puno]\nJon Paul Puno (born 1985) is an American filmmaker and classical crossover singer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q799fc84ee2",
  "kind": "yes/no",
  "text": "Claim: Halocyan Records, founded in 1951, has released records for the Chicago-based group who began acid-house, which spread to the United Kingdom and Europe\n\nPassages:\n\n[Phuture]\nPhuture is an American, Chicago-based acid-house group of electronic musicians, founded in 1985 by Spanky, DJ Pierre and Herb J.\n\n[Halocyan Records]\nBased in Los Angeles, CA, the label has released music by artists such as DJ Pierre of Chicago-based acid house group Phuture, Paul Woolford, techno pioneer Joey Beltram, Vladislav Delay (as Sistol), ASC, xxxy, Appleblim & Al Tourettes, Extrawelt and many more.\n\n[Acid house]\nAcid house spread to the United Kingdom and continental Europe, where it was played by DJs in the acid house and later rave scenes.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qec67258fa7",
  "kind": "yes/no",
  "text": "Claim: Nassu County, which borders Queens on its southern boundary, has a population of 778.\n\nPassages:\n\n[Hewlett-Woodmere School District]\nThe Hewlett-Woodmere Public School District, Union Free School District 14, is located in the southwest section of Nassau County, New York and borders the New York City borough of Queens.\n\n[Woodsburgh, New York]\nThe population was 778 at the 2010 census.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q259ee07d79",
  "kind": "yes/no",
  "text": "Post: Started watching house of cards, 4 episodes in. Already I can see it was a good choice😄",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q07ba94fd14",
  "kind": "yes/no",
  "text": "Claim: The fairy Queen Mab orginated with William Shakespeare in 1723.\n\nPassages:\n\n[Maeve]\nIt is also associated with the fairy queen Queen Mab of Irish and English legend.\n\n[Queen Mab]\nQueen Mab (pronunciation: \"M/ă/v\") is a fairy referred to in William Shakespeare's play \"Romeo and Juliet\", where \"she is the fairies' midwife.\"",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q7ab5aaeca0",
  "kind": "yes/no",
  "text": "Claim: Mathilde Ludendorff was the wife of the German General who was victorious at two battles, the Battle of Liège and the Battle of Tannenberg which both took place in 1942.\n\nPassages:\n\n[Erich Ludendorff]\nErich Friedrich Wilhelm Ludendorff (9 April 1865 – 20 December 1937) was a German general, the victor of the Battle of Liège and the Battle of Tannenberg.\n\n[Mathilde Ludendorff]\nHer third husband was General Erich Ludendorff.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe1e1375bd2",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which version is written sarcastically?",
  "options": [
   "So my Twitter feed has to show me what tweets people I follow like. ...😐 If I unfollowed you, just know I'm tired of seeing porn",
   "Twitter is showing that some people I follow are liking porn and I need to unfollow them to stop seeing that"
  ]
 },
 {
  "qid": "q4eed2b4b72",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "\"Just watched a man smoke crack on the R train in front of 3 families. New York is continuing to become less safe.\"",
   "Just watched a man smoke crack on the R train in front of 3 families. New York is healing ✨"
  ]
 },
 {
  "qid": "q055bf98cf2",
  "kind": "yes/no",
  "text": "Post: \"This is not just a black people issue, this is a HUMAN RIGHTS issue.\" Leslie Redmond, President, NAACP Minneapolis",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qe0137ae198",
  "kind": "yes/no",
  "text": "Post: @jimrossignol I choose to interpret it as \"XD\": the universal emoticon for laughing at those poor, poor folks in Ubisoft's marketing department who have to deal with that branding until the servers quietly shut down 8 months after launch.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q02c9e1177a",
  "kind": "yes/no",
  "text": "Claim: Party of British Unity was established in the wake of a public statement that announced support for the establishment of a \"national home for the Jewish people\" in Palestine.\n\nPassages:\n\n[Balfour Declaration]\nThe Balfour Declaration was a public statement issued by the British government during World War I announcing support for the establishment of a \"national home for the Jewish people\" in Palestine, then an Ottoman region with a minority Jewish population.\n\n[Declaration to the Seven]\nThe Declaration to the Seven was a document written by the British diplomat Sir Henry McMahon and released on June 16, 1918 in response to a memorandum issued anonymously by seven Syrian notables in Cairo who were members of the newly formed Party of Syrian Unity, established in the wake of the Balfour Declaration and the November 23, 1917 publication by the Bolsheviks of the secret May 1916 Sykes-Picot Agreement between Britain and France.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2b79d1599c",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which text is sarcastic?",
  "options": [
   "I'm not happy about me fronting during chaos.",
   "Of course the moment I front the system is in utter chaos 🥴"
  ]
 },
 {
  "qid": "q94edb70798",
  "kind": "yes/no",
  "text": "Text: update my gran called me an emo and walked out",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q15b10284b2",
  "kind": "yes/no",
  "text": "Text: The meaning behind Little Talks - @monstersandmen has to be the most pure example of love I've heard in a song for at least a little while #ILoveYou",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qaa365a27e9",
  "kind": "yes/no",
  "text": "Claim: Sir John Wedderburn and the brother of Henry Benedict Stuart fought in the unsuccessful Jacobite uprising of 1745. This ended with defeat at the conflict in which Simon Fraser, 11th Lord Lovat fought.\n\nPassages:\n\n[Henry Benedict Stuart]\nUnlike his father, James Francis Edward Stuart, and brother, Charles Edward Stuart, Henry made no effort to seize the throne.\n\n[Sir John Wedderburn, 5th Baronet of Blackness]\nSir John Wedderburn, 5th Baronet of Blackness was a Perthshire gentleman who joined the 1745 rebellion of Charles Edward Stuart and, captured at the Battle of Culloden, was afterwards convicted of treason.\n\n[Simon Fraser, 11th Lord Lovat]\nLovat was among the Highlanders defeated at the Battle of Culloden and convicted of treason against the Crown, following which he was sentenced to death and subsequently beheaded.\n\n[Charles Edward Stuart]\nCharles is perhaps best known as the instigator of the unsuccessful Jacobite uprising of 1745, in which he led an insurrection to restore his family to the throne of Great Britain.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qd83966106c",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Inspired by the ‘dinner with Jay Z’ guy still going strong. I choose now to believe him",
   "I do not like this man"
  ]
 },
 {
  "qid": "qcd4a75e9f5",
  "kind": "yes/no",
  "text": "Claim: The university where Ingenia Communications Corporation was incubated is located in the United States. The university where Howard Bailey played baseball is not located in the United States.\n\nPassages:\n\n[Grand Valley State University]\nGrand Valley State University (commonly referred to as GVSU, GV, or Grand Valley) is a public liberal arts university located in Allendale, Michigan, United States.\n\n[Carleton University]\nCarleton University is a comprehensive university located in Ottawa, Ontario, Canada.\n\n[Ingenia Communications Corporation]\nThe company was incubated at the Carleton University Faculty of Engineering and Design in Ottawa, Ontario, Canada.\n\n[Howard Bailey (baseball)]\nHe was signed by the Detroit Tigers as an amateur free agent in 1978 after playing his college ball at Grand Valley State University.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q3fab670ede",
  "kind": "yes/no",
  "text": "Claim: H. Frank Carey Junior-Senior High School for boys is in Garden City South.\n\nPassages:\n\n[Garden City South, New York]\nGarden City South is a hamlet and census-designated place (CDP) in Nassau County, New York, United States.\n\n[H. Frank Carey Junior-Senior High School]\nH. Frank Carey High School is a public high school located in Franklin Square, New York serving students in the seventh through twelfth grades from the towns of Franklin Square, Garden City South, West Hempstead, and Elmont.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2842428806",
  "kind": "yes/no",
  "text": "Text: being single during college must be really fun when ur nOT IN A GLOBAL PANDEMIC",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q16365ad71a",
  "kind": "yes/no",
  "text": "Claim: In 2009, The Forum Shops at Caesars, a 636000 sqft shopping mall connected to Caesars Palace was ranked as America's most profitable by US News & World Report.\n\nPassages:\n\n[The Forum Shops at Caesars]\nThe Forum Shops at Caesars (also known as simply The Forum) is a major 636000 sqft shopping mall connected to Caesars Palace on the Las Vegas Strip in Las Vegas, Nevada.\n\n[Ala Moana Center]\nAla Moana is consistently ranked among the top ten most successful malls in the United States and, in 2009, was ranked by \"U.S. News & World Report\" as America's second most profitable, behind The Forum Shops at Caesars in Las Vegas, Nevada.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 }
]
