# A46 replay label-noise blind read RSBS09-blind_read-a9209673-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS09-blind_read-a9209673-002.json

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
  "qid": "q4a03cd1997",
  "kind": "yes/no",
  "text": "Claim: This film featured the actor who was a member of the Christopher Wetzel Independent Film Comedy Award comedy troupe. Dana Carvey costarred in the film.\n\nPassages:\n\n[Wayne's World (film)]\nIt also features Rob Lowe, Tia Carrere, Lara Flynn Boyle, Brian Doyle-Murray, Chris Farley, Ed O'Neill, Ione Skye, Meat Loaf, and Alice Cooper.\n\n[Dana Carvey]\nDana Thomas Carvey (born June 2, 1955) is an American actor and stand-up comedian, who is most widely known for his work as a cast member on \"Saturday Night Live\" (1986–1993) and for playing the role of Garth Algar in the \"Wayne's World\" (1992) and its sequel \"Wayne's World 2\" (1993).\n\n[Chris Farley]\nFarley was known for his loud, energetic comedic style, and was a member of Chicago's Second City Theatre and later a cast member of the NBC sketch comedy show \"Saturday Night Live\" between 1990 and 1995.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q0a55ea0c2d",
  "kind": "yes/no",
  "text": "Claim: The British fashion and lifestyle publication, for whom Rachel Egglestone-Evans is editor, and InStyle are not both US-based magazines.\n\nPassages:\n\n[Rachel Egglestone-Evans]\nRachel 'Rae' Evans (born 6 September 1980 in Congleton, Cheshire, England) is the editor of Vintage Life Magazine, a British publication focusing on vintage fashion and lifestyle from the 1920s to the 1970s.\n\n[InStyle]\nInStyle is a monthly women’s fashion magazine published in the US by Time Inc. \"InStyle\" was founded in 1994.\n\n[Vintage Life]\nVintage Life is a British glossy fashion and lifestyle magazine, published by Dragoon Publishing, focusing on the 1920s-1970s.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qadfe7161a5",
  "kind": "yes/no",
  "text": "Claim: A Shinee group member's album was distributed by KT Music.\n\nPassages:\n\n[Shinee]\nThe group is composed of five members: Onew, Jonghyun, Key, Minho and Taemin.\n\n[Kim Jong-hyun (singer)]\nKim Jong-hyun (born April 8, 1990), better known by the mononym Jonghyun, is a South Korean singer-songwriter, and radio host.\n\n[She Is]\nShe Is (Hangul: 좋아 ; RR: \"Joh ah \" \"good\") is the first studio album by South Korean singer-songwriter Jonghyun, released on May 24, 2016 by S.M. Entertainment and distributed by KT Music.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa7fec62fc0",
  "kind": "yes/no",
  "text": "Claim: I Am Legend, a post apocalyptic action film based on a graphic novel by Francis Lawrence was directed by Neal H. Moritz.\n\nPassages:\n\n[I Am Legend (film)]\nI Am Legend is a 2007 American post-apocalyptic action horror film based on the novel of the same name, directed by Francis Lawrence and starring Will Smith, who plays US Army virologist Robert Neville.\n\n[Neal H. Moritz]\nHe is the founder of Original Film and most known for \"I Know What You Did Last Summer\", \"I Am Legend\" and \"The Fast and the Furious\" franchise, and the television shows \"Prison Break\" and \"The Big C\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q2b4dd4b85a",
  "kind": "yes/no",
  "text": "Claim: The lead of the CBS series which costarred Teri Copley played Jesus in \"Godspell\".\n\nPassages:\n\n[Victor Garber]\nHe is known for playing Jesus in \"Godspell\", Anthony Hope in \"\", John Wilkes Booth in \"Assassins\", Jack Bristow in the television series \"Alias\", Max in \"Lend Me a Tenor\", Thomas Andrews in James Cameron's \"Titanic\", and Ken Taylor, Canadian Ambassador to Iran, in \"Argo\".\n\n[I Had Three Wives]\nThe series' lead was Victor Garber in his first starring role on television.\n\n[Teri Copley]\nShe is known for role on the American NBC/syndicated television series \"We Got It Made\" which premiered in 1983, and she subsequently co-starred on the 1985 CBS television series \"I Had Three Wives\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q7a7817fd86",
  "kind": "yes/no",
  "text": "Tweet: Just won 3 cents on HQ words...early retirement here I come 😍",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q4cce1defbe",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "Just dislocated my fucking knee again while out on a walk 🙃🙃🙃 FAB",
   "\"I've dislocated my knee again, ouch!!!\""
  ]
 },
 {
  "qid": "q9f05a68fba",
  "kind": "yes/no",
  "text": "Tweet: lalisa and money are so good and perfect for lisa i’m so so proud of her and i can’t wait for the live performance",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q3bafa527ce",
  "kind": "yes/no",
  "text": "Claim: Henry C. McRae served for one season as the head football coach of a college that declines to accept federal financial support on the grounds of it's anti-abortion stance.\n\nPassages:\n\n[Hillsdale College]\nHillsdale College is a co-educational, non-profit liberal arts college in Hillsdale, Michigan, United States. The college declines to accept federal financial support, instead providing private financial assistance to its students.\n\n[Harry McRae]\nHenry C. McRae was an American football coach. He served as the head football coach at Hillsdale College in Hillsdale, Michigan for one season in 1904, compiling a record of 0–7.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5bcc1c81d0",
  "kind": "yes/no",
  "text": "Claim: An American four-piece sludge metal band who released the single Honey Bucket (song) was formed earlier than another band. This other band released a compilation album titled Artifakt.\n\nPassages:\n\n[Melvins]\nThe Melvins are an American rock band that formed in 1983 in Montesano, Washington.\n\n[Better Than Ezra]\nBetter Than Ezra is an American alternative rock band based in New Orleans, Louisiana, and signed to The End Records. The band formed in 1988 in Baton Rouge, Louisiana.\n\n[Artifakt]\nArtifakt is a compilation album by Better Than Ezra, sold only at the band's concerts and through the official Better Than Ezra merchandise website beginning in 2001.\n\n[Honey Bucket (song)]\n\"Honey Bucket\" is a single from American sludge metal band Melvins released in September 21, 1993.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qb338d83583",
  "kind": "yes/no",
  "text": "Claim: Dempster Brothers, Inc. was founded by George Roby Dempster and John Dempster and their brother, who often staged political battles. The brother and the eccentric Knoxville businessman were born in 1902.\n\nPassages:\n\n[Cas Walker]\nOrton Caswell \"Cas\" Walker (March 23, 1902 – September 25, 1998), was a Tennessee businessman, politician, and personality on television and radio.\n\n[Dempster Brothers]\nThe firm was originally established by George Roby Dempster with his brothers Thomas and John Dempster.\n\n[George Roby Dempster]\nDempster also served as a city manager and mayor of Knoxville, where he became legendary for his political battles with eccentric Knoxville businessman Cas Walker and \"Knoxville Journal\" editor Guy Smith, Jr.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2ff8bb9193",
  "kind": "yes/no",
  "text": "Claim: President Bill Clinton signed into law the act made to lower barriers to adoption.\n\nPassages:\n\n[Adoption 2002]\nBased on the Adoption and Safe Families Act of 1997, the aim of the program was to lower barriers to adoption and double the rate of adoption of children in foster care by 2002 from a 1996 figure of 27,000 to a 2002 figure of 54,000.\n\n[Adoption and Safe Families Act]\nThe Adoption and Safe Families Act (ASFA, Public Law 105-89) was signed into law by President Bill Clinton on November 19, 1997, after having been approved by the United States Congress earlier in the month.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q35b941bc22",
  "kind": "yes/no",
  "text": "Claim: The writer/director/actor from Glen or Glenda and Fernand Rivers share the career titles actor, writer, producer, and director.\n\nPassages:\n\n[Ed Wood]\nEdward Davis Wood Jr. (October 10, 1924 – December 10, 1978) was an American filmmaker, actor, writer, producer, and director.\n\n[Glen or Glenda]\nGlen or Glenda is a 1953 American drama film written, directed by and starring Ed Wood (credited in his starring role as \"Daniel Davis\"), and featuring Bela Lugosi and Wood's then-girlfriend Dolores Fuller.\n\n[Fernand Rivers]\nFernand Rivers (born François Large, 6 September 1879, Saint-Lager - 12 September 1960) was a French actor, screenwriter, film producer and director.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q0578f5e790",
  "kind": "yes/no",
  "text": "Claim: Stoke City football has a new shirt sponsor based in the United Kingdom.\n\nPassages:\n\n[2012–13 Stoke City F.C. season]\nIt was also the club's 150th year in existence and to mark the occasion the club had a special crest and the away kit was the same colours that Stoke Ramblers wore back in 1863, navy and cardinal Stoke also had a new shirt sponsor Bet365 taking over from Britannia.\n\n[Bet365]\nBet365 Group Ltd (styled as \"bet365\") is a gambling company based in the United Kingdom.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7c55b182ea",
  "kind": "yes/no",
  "text": "Claim: Ricky \"Running\" Watters was the nickname given to the chess player at the University of Notre Dame where he played wide receiver on the school's 1988 national champion team, by A six-time honoree of the National Sports Media Association's \"National Sportscaster of the Year\" award.\n\nPassages:\n\n[Chris Berman]\nA six-time honoree of the National Sports Media Association's \"National Sportscaster of the Year\" award, Berman was instrumental in establishing ESPN's lasting popularity during the network's formative years.\n\n[Ricky Watters]\nWatters was known throughout his playing career for his outstanding receiving skills and his unique high-step running style, which earned him the nickname Ricky \"Running\" Watters, from ESPN sportcaster Chris Berman.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q17d8333540",
  "kind": "yes/no",
  "text": "Claim: The shopping mall located in the tallest completed building in Nevada is 500000 square feet.\n\nPassages:\n\n[Grand Canal Shoppes]\nThe Grand Canal Shoppes is a 500000 sqft upscale shopping mall inside The Venetian Hotel & Casino and The Palazzo on the Las Vegas Strip in Paradise, Nevada.\n\n[The Palazzo]\nThe Palazzo is a luxury hotel and casino resort located on the Las Vegas Strip in Paradise, Nevada. It is the tallest completed building in Nevada.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q8e3250c974",
  "kind": "yes/no",
  "text": "Claim: The band Adorable was not formed first and then the band Allen Shellenberger played drums with.\n\nPassages:\n\n[Adorable (band)]\nAdorable was an alternative rock band, formed in Coventry in 1990.\n\n[Allen Shellenberger]\nAllen Shellenberger (September 15, 1969 – August 13, 2009) was an American drummer who played in the band Lit.\n\n[Lit (band)]\nLit is an American rock band, formed in 1995 in Fullerton, California.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q0474a3b2b2",
  "kind": "yes/no",
  "text": "Claim: The sport of tennis is played by both Angelique Kerber and the player who was the defending champion, who competed, for the 2005 China Open – Men's Doubles.\n\nPassages:\n\n[2005 China Open – Men's Doubles]\nJustin Gimelstob and Graydon Oliver were the defending champions, but Oliver did not participate this year.\n\n[Justin Gimelstob]\nJustin Jeremy Gimelstob (born January 26, 1977) is a retired American tennis player.\n\n[Angelique Kerber]\nAngelique Kerber (] ; born 18 January 1988) is a German professional tennis player and former world No. 1.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q1024f91769",
  "kind": "yes/no",
  "text": "Post: Loving season 4 of trump does America. Funniest season yet #DonaldTrump #Trump #MAGA #MAGA2020",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qdb15b09384",
  "kind": "yes/no",
  "text": "Post: All I've done this summer is binge watch The Office and Friends 🙃🙃",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qf75f74d017",
  "kind": "yes/no",
  "text": "Claim: Len Wiseman was the director of the 2007 American action film starring the actress who also starred in the film Slumber.\n\nPassages:\n\n[Live Free or Die Hard]\nThe film was directed by Len Wiseman and stars Bruce Willis as John McClane.\n\n[Maggie Q]\nMargaret Denise Quigley (born May 22, 1979), professionally known as Maggie Q, is an American actress and model. She is known for starring in the action films \"\" and \"Live Free or Die Hard\" and played the title role of The CW's action-thriller series \"Nikita\", airing from 2010 to 2013.\n\n[Slumber (film)]\nThe film stars Maggie Q, Will Kemp, Sylvester McCoy and William Hope.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q769dab6c71",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which text is sarcastic?",
  "options": [
   "Gonna go cry now some no face told me to lose weight x",
   "Fuck the person who told me to lose weight"
  ]
 },
 {
  "qid": "q2d615ccdaf",
  "kind": "yes/no",
  "text": "Claim: Monsters, Inc. Laugh Floor replaced the 1992 film The Timekeeper shown at three Disney parks.\n\nPassages:\n\n[The Timekeeper]\nThe Timekeeper (also known as From Time to Time and Un Voyage à Travers le Temps) was a 1992 Circle-Vision 360° film that was presented at three Disney parks around the world.\n\n[Monsters, Inc. Laugh Floor]\nMonsters, Inc. Laugh Floor is an attraction within the Magic Kingdom, a theme park at Walt Disney World Resort. It opened on April 2, 2007 within the park's Tomorrowland section, where it replaced the Circle-Vision attraction The Timekeeper.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q967997dca9",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which text is sarcastic?",
  "options": [
   "This book makes me feel like I don't really know how to read.",
   "If you ever wanted to know what it feels like to have dyslexia I would recommend the book House of Leaves."
  ]
 },
 {
  "qid": "q08e581b1ac",
  "kind": "yes/no",
  "text": "Tweet: i know i’m going through it when i can’t even fake tan",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q01a7b60a0e",
  "kind": "yes/no",
  "text": "Claim: Niño was the nickname of the player who played his final season for the 2016 Miami Dolphins before dying in an accident.\n\nPassages:\n\n[2016 Miami Marlins season]\nThis also marked José Fernández's final season as he died in a boating accident on September 25.\n\n[José Fernández (pitcher)]\nHe was affectionately known as \"Niño\" by his teammates and fans due to the youthful exuberance with which he played the game of baseball.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qb82e2c55dd",
  "kind": "yes/no",
  "text": "Claim: The engine, for the redesigned McDonnell F3H Demon, had a name change to J35 after it was modified to a thrust of 7400 lbf.\n\nPassages:\n\n[Allison J35]\nWith the afterburner, which most models carried, it produced a thrust of 7400 lbf .\n\n[McDonnell F3H Demon]\nThe successor to the F2H Banshee, the Demon was redesigned with the J71 engine after severe problems with the Westinghouse J40 engine that was part of the original design but ultimately abandoned.\n\n[Allison J71]\nThe Allison J71 was a single spool turbojet engine, designed and built in the United States. It began development in 1948 as a much modified J35, originally designated J35-A-23.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe5a67a37f5",
  "kind": "yes/no",
  "text": "Post: If ya headcanon Cub as an alien you could also make a Lilo and Stitch AU with Scar as Lilo and Cub as Stitch",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q4c5dd90647",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "My gf has been in the Hamptons nannying for a few hours and she has already been to a POLO match. Is she in GOSSIP GIRL?",
   "My gf has been in the Hamptons nannying for a few hours and she has already been to a POLO match. It’s like she’s in “Gossip Girl”"
  ]
 },
 {
  "qid": "q71e262a859",
  "kind": "yes/no",
  "text": "Post: wearing a cute jumpsuit is all fun and games until you have to go to the bathroom",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q7eaf3c715c",
  "kind": "yes/no",
  "text": "Claim: The drug store, which merged with Leaps and Bounds in 1995, was founded in Missouri and Valentino's wasn't.\n\nPassages:\n\n[Leaps and Bounds (playplace)]\nIt was merged with competitor Discovery Zone in 1995.\n\n[Valentino's]\nValentino's is a regional Italian restaurant chain based in Lincoln, Nebraska.\n\n[Discovery Zone]\nDiscovery Zone (DZ) was a chain of entertainment facilities featuring games and elaborate indoor mazes designed for young children, including roller slides, climbing play structures and ball pits. The first location was opened in Kansas City, Missouri in October 1989.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q6419170a0f",
  "kind": "yes/no",
  "text": "Claim: Dick Clement directed the 1971 film that features the star of Thick as Thieves.\n\nPassages:\n\n[On the Buses (film)]\nOn the Buses is a 1971 British comedy film directed by Harry Booth and starring Reg Varney and Doris Hare.\n\n[Pat Ashton]\nHer engaging cockney, blonde persona is best remembered for appearances in English TV-sitcom film spin-offs \"On the Buses\" (1971) and \"Mutiny on the Buses\" (1972).\n\n[Thick as Thieves (TV series)]\nThere were 8 episodes over one series and starred Bob Hoskins, John Thaw and Pat Ashton.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q79ba20f888",
  "kind": "yes/no",
  "text": "Claim: The movie, based on a story written by brothers who are interred at Alter St.-Matthäus-Kirchhof, is loosely based off the Brother Grimm's \"Iron Henry\".\n\nPassages:\n\n[Alter St.-Matthäus-Kirchhof]\nIt is known for its interment of the Brothers Grimm, Jacob and Wilhelm Grimm, folklore tellers of \"Cinderella\" (\"Aschenputtel\"), \"The Frog Prince\" (\"Der Froschkönig\"), \"Hansel and Gretel\" (\"Hänsel und Gretel\"), \"Rapunzel\", \"Rumpelstiltskin\" (\"Rumpelstilzchen\"), and \"Snow White\" (\"Schneewittchen\"); Rudolf Virchow, variously known as \"father of modern pathology\", \"father of modern medicine\" or \"father of social medicine\"; and Claus von Stauffenberg, a German Army officer who almost assassinated Adolf Hitler.\n\n[The Frog Prince]\n\"The Frog Prince; or, Iron Henry\" (German: \"Der Froschkönig oder der eisen Heinrich\" , literally \"The Frog King; or, The Iron Heinrich\") is a fairy tale, best known through the Brothers Grimm's written version; traditionally it is the first story in their collection.\n\n[The Princess and the Frog]\nThe 49th Disney animated feature film, the film is loosely based on the novel \"The Frog Princess\" by E. D. Baker, which is in turn based on the Brothers Grimm fairy tale \"The Frog Prince\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qaebeb7f256",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "@Showmasters are basically thieves, quoting it’s in the small print so you can’t have a refund. Dates moved from summer, to a 4 hour slot on a Friday evening in November which is about as much use as a telescopic sight on a knife.#WeWantARefund @UKConsumerRight",
   "Your refund policy wasn’t very helpful at all."
  ]
 },
 {
  "qid": "q8a5b29a0ff",
  "kind": "yes/no",
  "text": "Text: Not only did I have to take care of covid patients last night but my charge nurse told me the covid scrubs make me look “unwantable”! Great!",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q085fcd3eee",
  "kind": "yes/no",
  "text": "Claim: Jude Law an Scousers actor that was born in 1972. He was part of the ensemble cast of the movie Scott Z. Burns wrote that screenplay for.\n\nPassages:\n\n[Contagion (film)]\nThe film features an ensemble cast that includes Marion Cotillard, Bryan Cranston, Matt Damon, Laurence Fishburne, Jude Law, Gwyneth Paltrow, Kate Winslet, and Jennifer Ehle.\n\n[Scott Z. Burns]\n\" (2009), and \"Contagion\" (2011), all of which feature Matt Damon.\n\n[Jude Law]\nDavid Jude Heyworth Law (born 29 December 1972) is an English actor.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q807c3dcdcb",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I hate the US health care system.",
   "everyone say a prayer to the insurance gods that they approve my heart monitor so that i may continue to have the privilege of being alive. i love the US health care system"
  ]
 },
 {
  "qid": "q9159f5c501",
  "kind": "yes/no",
  "text": "Claim: 1969 saw the founding of the baseball team where the future manager played from 1973-87. He managed the Tampa Bay Devil Rays season.\n\nPassages:\n\n[2002 Tampa Bay Devil Rays season]\nTheir manager was Hal McRae who entered his 1st full season and last season with the Devil Rays.\n\n[Hal McRae]\nHarold Abraham McRae ( ; born July 10, 1945) is a former left fielder in Major League Baseball who played for the Cincinnati Reds (1968, 1970–72) and Kansas City Royals (1973–87).\n\n[Kansas City Royals]\nThe team was founded as an expansion franchise in 1969, and has participated in four World Series, winning in 1985 and 2015, and losing in 1980 and 2014.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa68e46ab17",
  "kind": "yes/no",
  "text": "Claim: Sara Eskander Poulsen, who voiced a Phineas and Darren Jessee character, achieved mainstream success on The Suite Life of Zack & Cody.\n\nPassages:\n\n[Sara Poulsen]\nShe is best known for voicing Candace Flynn in Phineas and Ferb and for dubbing Brenda Song's character London Tipton in The Suite Life of Zack & Cody and The Suite Life on Deck.\n\n[Candace Flynn]\nCandace Gertrude Flynn is a main character of the Disney Channel animated television series \"Phineas and Ferb\", voiced by Ashley Tisdale and created and designed by Dan Povenmire.\n\n[Ashley Tisdale]\nShe achieved mainstream success as Maddie Fitzpatrick in the Disney Channel series \"The Suite Life of Zack & Cody\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa0d4fc71a8",
  "kind": "yes/no",
  "text": "Claim: The Trials of Nikki Hill is a legal thriller written by Dick Lochte and Christopher Allen \"Chris\" Darden, an American lawyer, author, actor, lecturer, and practicing attorney.\n\nPassages:\n\n[The Trials of Nikki Hill]\nThe Trials of Nikki Hill is a legal thriller written by Christopher Darden and Dick Lochte, and published Time Warner Company in 1999.\n\n[Christopher Darden]\nChristopher Allen \"Chris\" Darden (born April 7, 1956) is an American lawyer, author, actor, lecturer, and practicing attorney.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q667f50693a",
  "kind": "yes/no",
  "text": "Claim: North Blenheim, New York was destroyed by flooding caused by the Hurricane that landed in August 2011.\n\nPassages:\n\n[North Blenheim, New York]\nIt was built in 1855 and existed until 2011, when it was destroyed by flooding caused by Hurricane Irene.\n\n[Hurricane Irene]\nHurricane Irene was a large and destructive tropical cyclone, which affected much of the Caribbean and East Coast of the United States during late August 2011.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q51b10b3078",
  "kind": "yes/no",
  "text": "Claim: Alan Sokal, a professor of mathematics, authored the book Fashionable Nonsense in 1781.\n\nPassages:\n\n[Alan Sokal]\nAlan David Sokal ( ; born January 24, 1955) is a professor of mathematics at University College London and professor of physics at New York University.\n\n[Fashionable Nonsense]\nFashionable Nonsense: Postmodern Intellectuals' Abuse of Science (French: \"Impostures Intellectuelles\" ), published in the UK as Intellectual Impostures, is a book by physicists Alan Sokal and Jean Bricmont.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q0cd14e0200",
  "kind": "yes/no",
  "text": "Claim: Emory University was founded before the school that William Ridley Wills is a graduate of.\n\nPassages:\n\n[Vanderbilt University]\nFounded in 1873, it was named in honor of shipping and rail magnate Cornelius Vanderbilt, who provided the school its initial $1 million endowment despite having never been to the South.\n\n[Emory University]\nThe university was founded as Emory College in 1836 in Oxford, Georgia by the Methodist Episcopal Church and was named in honor of Methodist bishop John Emory. In 1915, the college relocated to metropolitan Atlanta and was rechartered as Emory University.\n\n[William Ridley Wills]\nWilliam Ridley Wills, born Brownsville, Tennessee on March 4, 1897, was a graduate of Vanderbilt University and a member of the Fugitive literary group.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q549b769b90",
  "kind": "yes/no",
  "text": "Claim: There are 2,956 hotel rooms are in the Las Vegas hotel which hosted the 38th Annual Daytime Emmy Awards in 2011.\n\nPassages:\n\n[38th Daytime Emmy Awards]\nThe 38th Annual Daytime Emmy Awards were held on Sunday, June 19, 2011, at the Las Vegas Hilton, and were televised on CBS.\n\n[Westgate Las Vegas Resort &amp; Casino]\nThe Westgate Las Vegas Resort & Casino is a hotel and casino in Winchester, Nevada. It has 2,956 hotel rooms including 305 suites. It opened in 1969 as the International Hotel, and was known for many years as the Las Vegas Hilton, then briefly as the LVH – Las Vegas Hotel and Casino.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q48669f1b63",
  "kind": "yes/no",
  "text": "Text: Even though my mom has to work a 12 hr shift today, I'm thankful she's happy with what she does and that she is doing what she needs to do in order to care for her children. She is the strongest and most important woman in my life. Without her, I am nothing.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qa817181bcf",
  "kind": "yes/no",
  "text": "Claim: The song of the same name of a band's album released before The Revelation was used for a WWE event that took place on May 1, 2011. This band released the EP \"Take 'Em Out\".\n\nPassages:\n\n[Take 'Em Out]\nTake 'Em Out is a four-song EP released by American hard rock band, Rev Theory.\n\n[Extreme Rules (2011)]\nExtreme Rules was a professional wrestling pay-per-view (PPV) event produced by WWE, which took place on May 1, 2011 at the St. Pete Times Forum in Tampa, Florida.\n\n[Justice (Rev Theory album)]\nThe song Justice was used for WWE's Extreme Rules (2011).\n\n[The Revelation (Rev Theory album)]\nIt is the band's first full-length studio album since \"Justice\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qb2c87d3bdd",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Mine and @livlawrencex snapchats are just stunning👌",
   "Our Snapchat’s are incredibly unattractive"
  ]
 },
 {
  "qid": "qc70258d26b",
  "kind": "yes/no",
  "text": "Claim: Grigori Vasilyevich Aleksandrov was a prominent Soviet director who worked frequently with Composer Isaak Dunayevsky.\n\nPassages:\n\n[Isaak Dunayevsky]\nIsaak Osipovich Dunayevsky (Russian: \"Исаак Осипович Дунаевский\" ; also transliterated as Dunaevski or Dunaevsky; 30 January [O.S. 18 January] 1900 25 July 1955) was a Soviet film composer and conductor of the 1930s and 1940s, who achieved huge success in music for operetta and film comedies, frequently working with the film director Grigori Aleksandrov.\n\n[Grigori Aleksandrov]\nGrigori Vasilyevich Aleksandrov or Alexandrov (Russian: Григо́рий Васи́льевич Алекса́ндров ; original family name was Мормоненко or Mormonenko; 23 January 1903 – 16 December 1983) was a prominent Soviet film director who was named a People's Artist of the USSR in 1947 and a Hero of Socialist Labor in 1973.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q2f10316239",
  "kind": "yes/no",
  "text": "Claim: Saturn AL-31 is an engine that powers the aircraft produced in the country China.\n\nPassages:\n\n[Saturn AL-31]\nThe Saturn AL-31 is a family of military turbofan engines. Currently it powers all Su-27 derivatives and the Chengdu J-10 multirole jet fighter which has been developed by China.\n\n[Chengdu J-10]\nThe Chengdu J-10 ([[Simplified Chinese characters|simplified Chinese]]: 歼-10; [[Traditional Chinese characters|traditional Chinese]]: 殲-10; [[NATO reporting name]] : Firebird) is a lightweight [[multirole combat aircraft|multirole]] [[fighter aircraft]] capable of all-weather operation, configured with a [[delta wing]] and [[Canard (aeronautics)|canard]] design, with [[fly-by-wire]] flight controls, and produced by the [[People's Republic of China]]'s [[Chengdu Aircraft Industry Group|Chengdu Aircraft Corporation (CAC)]] for the [[People's Liberation Army Air Force]] (PLAAF).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q614a825846",
  "kind": "yes/no",
  "text": "Claim: The German music group, Snap!, produced a 2003 hit rap song with Bass Bumpers and an album. Their song Colour of Love was the first single from this album.\n\nPassages:\n\n[The Madman's Return]\nThe Madman's Return is Snap! 's second studio album and contains the international massive hit \"Rhythm Is a Dancer\", which reached No. 1 in France, Ireland, Italy, the Netherlands, Germany and the United Kingdom and peaked at No. 5 in the US.\n\n[Rhythm Is a Dancer]\n\"Rhythm Is a Dancer\" is a song recorded by German group Snap!\n\n[Colour of Love (Snap song)]\nIt was released as the first single from their second studio album, \"The Madman's Return\" in December 1991.\n\n[Bass Bumpers]\nAlso known as Bass Bumpers, CJ Stone, and Bad Habit Boys, they produced their own hits such as \"Good Fun\", \"The Music's Got Me\" (a number 36 hit on \"Billboard's\" Hot Dance Club Songs chart in 1992), \"Move to the Rhythm\" and \"Rhythm Is A Dancer (2003)\" with Snap! .",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 }
]
