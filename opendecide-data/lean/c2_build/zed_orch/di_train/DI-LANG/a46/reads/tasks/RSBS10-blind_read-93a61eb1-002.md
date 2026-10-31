# A46 replay label-noise blind read RSBS10-blind_read-93a61eb1-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS10-blind_read-93a61eb1-002.json

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
  "qid": "q096ed1dd17",
  "kind": "yes/no",
  "text": "Post: More Life to Me 😌🥳 #23",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qebf5807311",
  "kind": "yes/no",
  "text": "Claim: An athlete played defense for the team Rodney Hannah plays for. The college this athlete played at is located in Louisiana.\n\nPassages:\n\n[Everson Walls]\nHe played college football at Grambling State University.\n\n[1983 Dallas Cowboys season]\nHowever, the defense gave up many points, despite strong play from Randy White, Ed \"Too Tall\" Jones, and Everson Walls.\n\n[Rodney Hannah]\nRodney Dee Hannah II (born August 9, 1987) is a former American football tight end in the National Football League for the Dallas Cowboys.\n\n[Grambling State University]\nGrambling State University (GSU) is a historically black, public, coeducational university, located in Grambling, Louisiana.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q21faa888d6",
  "kind": "yes/no",
  "text": "Claim: Iris (Song) was originally written for the soundtrack of a 1998 musical film. The lead female actress in the film began her acting career in 1981.\n\nPassages:\n\n[Iris (song)]\nOriginally written for the soundtrack of the 1998 film \"City of Angels\", the song was later included on the band's sixth album \"Dizzy Up the Girl\".\n\n[Meg Ryan]\nRyan began her acting career in 1981 in minor roles, before joining the cast of the CBS soap opera \"As the World Turns\" in 1982.\n\n[City of Angels (film)]\nCity of Angels is a 1998 American romantic fantasy film directed by Brad Silberling and starring Nicolas Cage and Meg Ryan.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa082216cba",
  "kind": "yes/no",
  "text": "Claim: Fforest Fawr Geopark sits within a type of park that Timanfaya is also categorized as. Timanfaya is further south within Spain than another of these types of park which contains Tobes.\n\nPassages:\n\n[Fforest Fawr Geopark]\nIts aims largely coincide with the statutory duties and purpose of the National Park within which it sits.\n\n[Picos de Europa National Park]\nThe Picos de Europa National Park (Spanish: \"Parque Nacional de Picos de Europa\" ) is a National Park in the Picos de Europa mountain range, in northern Spain.\n\n[Tobes]\nIt is located in the Picos de Europa National Park.\n\n[Timanfaya National Park]\nTimanfaya National Park (Spanish: \"Parque Nacional de Timanfaya\" ) is a Spanish national park in the southwestern part of the island of Lanzarote, Canary Islands.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q14e022448d",
  "kind": "yes/no",
  "text": "Claim: Pyne & Marles is co-hosted by Richard Marles and an Australian politician who has been the Liberal member for the House of Representatives seat of Sturt since the beginning of 1993.\n\nPassages:\n\n[Pyne &amp; Marles]\nThe program is co-hosted by two serving frontbench MPs; Liberal minister Christopher Pyne and Labor shadow minister Richard Marles, without a journalist or moderator.\n\n[Christopher Pyne]\nChristopher Maurice Pyne (born 13 August 1967) is an Australian politician who has been the Liberal member for the House of Representatives seat of Sturt since the 1993 election.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qd916dd0f3a",
  "kind": "yes/no",
  "text": "Text: Is there anything better and more comforting to eat when you're ill than toast?? No there is not",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q3fd0e3f2fa",
  "kind": "yes/no",
  "text": "Text: OH MY GOD I AM IN LOVE WITH MY FIANCÉ. https://t.co/LRukiQpXve",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q79161b2aef",
  "kind": "yes/no",
  "text": "Claim: The actor that played Tony Soprano in \"The Sopranos\" stars with Tom Hardy in a 2014 crime drama film directed by Michaël R. Roskam.\n\nPassages:\n\n[The Drop (film)]\nThe Drop is a 2014 American crime drama film directed by Michaël R. Roskam, from a screenplay written by Dennis Lehane. The film stars Tom Hardy, Noomi Rapace and James Gandolfini, with Matthias Schoenaerts, John Ortiz and James Frecheville in supporting roles.\n\n[James Gandolfini]\nHe was best known for his role as Tony Soprano, an Italian-American crime boss, in the HBO crime drama \"The Sopranos\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q116b1d8b7f",
  "kind": "yes/no",
  "text": "Claim: Nick Saban was the coach for the team that won the 2004 Sugar Bowl.\n\nPassages:\n\n[2003 LSU Tigers football team]\nCoached by Nick Saban, the LSU Tigers played their home games at Tiger Stadium in Baton Rouge, Louisiana.\n\n[2004 Sugar Bowl]\nThe Tigers won the BCS National Championship, their second championship, defeating the Sooners by a score of 21-14.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q1125a9c78b",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I'm not doing great mentally right now.",
   "flew into a rage this morning bc i couldnt find my karaoke mic so yeah i would say things are going well for me"
  ]
 },
 {
  "qid": "q0709fdddf2",
  "kind": "yes/no",
  "text": "Text: Nice to see @Cardiffbus have started the new year off with the usual crap service. Just love waiting for a bus that doesn't turn up",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qb5c76bd2d8",
  "kind": "yes/no",
  "text": "Claim: The bassist of the group, who released \"Mothers Talk\", sang on the band's song \"Change\". Rock singer John Michael \"Ozzy\" Osbourne has released more solo albums than him.\n\nPassages:\n\n[Mothers Talk]\n\"Mothers Talk\" is a 1984 song by the British band Tears for Fears.\n\n[Change (Tears for Fears song)]\nWritten by Roland Orzabal and sung by bassist Curt Smith, it was the band's fourth single release.\n\n[Ozzy Osbourne]\nJohn Michael \"Ozzy\" Osbourne (born 3 December 1948) is an English singer, songwriter, and actor. He was fired from Black Sabbath in 1979 and went on to have a successful solo career, releasing 11 studio albums, the first seven of which were all awarded multi-platinum certifications in the US.\n\n[Curt Smith]\nAs a solo artist, he has released four solo albums.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2770822588",
  "kind": "yes/no",
  "text": "Post: i hate it here ❤️❤️❤️❤️❤️",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qd62ef4a9de",
  "kind": "yes/no",
  "text": "Claim: The person who portrayed Dr. John Watson in Sherlock Holmes (2009 film) is an English actor that was born in 1972. He was part of the ensemble cast of the movie Scott Z, which Burns wrote that screenplay for.\n\nPassages:\n\n[Scott Z. Burns]\n\" (2009), and \"Contagion\" (2011), all of which feature Matt Damon.\n\n[Sherlock Holmes (2009 film)]\nRobert Downey Jr. and Jude Law portray Sherlock Holmes and Dr. John Watson respectively.\n\n[Jude Law]\nDavid Jude Heyworth Law (born 29 December 1972) is an English actor.\n\n[Contagion (film)]\nThe film features an ensemble cast that includes Marion Cotillard, Bryan Cranston, Matt Damon, Laurence Fishburne, Jude Law, Gwyneth Paltrow, Kate Winslet, and Jennifer Ehle.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qc3befc34d6",
  "kind": "yes/no",
  "text": "Tweet: @ishkolhatkar @RosieisaHolt We think you are very, very funny and very,very,very etc …brave. You nail the issue and put those that actually believe the comments you make to shame…. Please keep doing what you’re doing….",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qfbaff01478",
  "kind": "yes/no",
  "text": "Claim: Matt McKenzie had a role on the television show that focused on the lives of teenage friends from the town of Point Place, Wisconsin.\n\nPassages:\n\n[Matt McKenzie]\nMcKenzie has also guest starred in some well-known movies (\"Gods and Monsters\" with Sir Ian McKellen, in which he portrayed Colin Clive) and TV shows such as \"\", \"\", \"JAG\", \"7th Heaven\", \"That '70s Show\", \"The O.C.\" and recently 24 as Agent Hollister.\n\n[That '70s Show]\nThe series focused on the lives of a group of teenage friends living in the fictional suburban town of Point Place, Wisconsin, from May 17, 1976, to December 31, 1979.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1dbf8abd4c",
  "kind": "yes/no",
  "text": "Claim: The Single Guy is an American television family sitcom comedy that ran for two seasons on NBC, from September 1995 to April 1997 on Monday nights; starring Ming-Na Wen as Sam's wife, Ming-Na Wen is an American actress, born November 20, 1963.\n\nPassages:\n\n[The Single Guy]\nThe series also starred Joey Slotnick as Eliot's best friend Sam Sloan, Ming-Na Wen as Sam's wife Trudy and Ernest Borgnine as doorman Manny, throughout its entire run.\n\n[Ming-Na Wen]\nMing-Na Wen (; born November 20, 1963) is an American actress.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa076261529",
  "kind": "yes/no",
  "text": "Claim: Leo Varadkar beat Irish Fine Gael politician Simon Coveney on June 2, 2017, 60% to 40%.\n\nPassages:\n\n[Simon Coveney]\nSimon Anthony Coveney (born 16 June 1972) is an Irish Fine Gael politician who has served as Minister for Foreign Affairs and Trade and Deputy Leader of Fine Gael since June 2017.\n\n[Fine Gael leadership election, 2017]\nThe 2017 Fine Gael leadership election was triggered in May 2017, when Enda Kenny resigned as party leader. On 2 June Leo Varadkar was announced as the victor, beating rival Simon Coveney 60% to 40%.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q080eb13865",
  "kind": "yes/no",
  "text": "Claim: Ray and Leo Wilson do not have the same nationality.\n\nPassages:\n\n[Leo (singer)]\nJung Taek-woon (Hangul: 정택운 , born on November 10, 1990), better known by his stage name Leo (Hangul: 레오 ), is a South Korean singer, songwriter and musical theatre actor, signed under Jellyfish Entertainment.\n\n[Ray Wilson (musician)]\nRaymond Wilson (born 8 September 1968) is a Scottish musician, best known as vocalist in the post-grunge band Stiltskin, and in Genesis from 1996 to 1998.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb2756f67b2",
  "kind": "yes/no",
  "text": "Claim: The birthday of the man who asked Andres Thomas \"Why would you even throw him a strike?\" was April 2, 1945, he was born in Rochdale.\n\nPassages:\n\n[Andrés Thomas]\nHis free-swinging prompted then-Braves' broadcaster Don Sutton to ask hypothetically during games, \"Why would you even throw him a strike?\"\n\n[Don Sutton]\nDonald Howard Sutton (born April 2, 1945) is an American former professional baseball player.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qca3cb58157",
  "kind": "yes/no",
  "text": "Claim: Jang Hyun-seung was born after Dave Peverett.\n\nPassages:\n\n[Dave Peverett]\nDavid Jack Peverett (16 April 1943 – 7 February 2000), also known as Lonesome Dave, was an English singer and musician, best known as the original lead vocalist and rhythm guitarist of the rock band Foghat, which he founded following his tenure in Savoy Brown.\n\n[Jang Hyun-seung]\nJang Hyun-seung (; born September 3, 1989) most often credited as Hyunseung, is a South Korean singer.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa6465f2251",
  "kind": "yes/no",
  "text": "Claim: Denmark's leader residing over the Cabinet of Deuntzer, was a part of the Liberal \"Venstre\" party for 12 years before the party that translates to the \"Radical Left\".\n\nPassages:\n\n[Danish Social Liberal Party]\nThe Danish Social Liberal Party (Danish: \"Radikale Venstre\" , \"Radical Left\", i.e. \"Radical Liberal Party\") is a social-liberal political party in Denmark.\n\n[Cabinet of Deuntzer]\nAfter the 1901 Danish Folketing election, the Council President Johan Henrik Deuntzer of the Venstre Reform Party became the leader of Denmark's first liberal government.\n\n[Johan Henrik Deuntzer]\nJohan Henrik Deuntzer (20 May 1845 – 16 November 1918) was a Danish politician, member of the Liberal \"Venstre\" party until 1905 where he joined the Danish Social Liberal Party.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1e55819de1",
  "kind": "yes/no",
  "text": "Claim: Pari Lake flows down to this gigantic circular lake. Sniardwy is farther north than that gigantic lake.\n\nPassages:\n\n[Kundol Lake]\nKundol Lake also known as \"Kundol Dand\", is a lake in Swat Valley, Khyber Pakhtunkhwa, Pakistan, which is located in the north of Utror valley at a distance of 19 km away from kalam.\n\n[Pari Lake]\nThe western face of the lake is open and its water flows down to the gigantic Kundol Lake which is situated in the foothills.\n\n[Śniardwy]\nŚniardwy (German: ) is a lake in the Masurian Lake District of the Warmian-Masurian Voivodeship, Poland.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q832fbec31c",
  "kind": "yes/no",
  "text": "Text: @glennhodl @EverydayDCA Hey Glenn, what is this app called?",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q4b09cdde6b",
  "kind": "yes/no",
  "text": "Claim: The town is administered by the Hindmarsh Shire Council Shire council. It is located near Higgin's Creek and Deua National Park.\n\nPassages:\n\n[Deua National Park]\nThe nearest towns on the coast are Batemans Bay, Moruya and Narooma.\n\n[Cortinarius kioloensis]\nThe type specimen was collected along Higgins Creek in Kioloa State Forest near Batemans Bay in southern New South Wales on 22 June 1980.\n\n[Batemans Bay]\nBatemans Bay is a town in the South Coast region of the state of New South Wales, Australia.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9b838a92d0",
  "kind": "yes/no",
  "text": "Claim: Pashto is the main language among a diaspora that has it's largest community in the country Pakistan.\n\nPassages:\n\n[Pashtun diaspora]\nPakistan is home to the largest Pashtun community.\n\n[Pashto]\nPashto is the main language among the Pashtun diaspora around the world.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf6e4a803e4",
  "kind": "yes/no",
  "text": "Claim: Highway Companion is the third solo studio album by a English singer-songwriter. He has been a member of more bands than Bobby Gillespie.\n\nPassages:\n\n[Highway Companion]\nHighway Companion is the third solo studio album by American singer-songwriter Tom Petty.\n\n[Tom Petty]\nHe is best known as the lead singer of Tom Petty and the Heartbreakers, but is also known as a member and co-founder of the late 1980s supergroup the Traveling Wilburys (under the pseudonyms of Charlie T. Wilbury Jr. and Muddy Wilbury), and his early band Mudcrutch.\n\n[Bobby Gillespie]\nHe is the lead singer and founding member of the alternative rock band, Primal Scream. He was also the drummer for The Jesus and Mary Chain in the mid-1980s.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qb9b48cd768",
  "kind": "yes/no",
  "text": "Claim: The college Michigan Edward Dorr Griffin served as president at from 1821 to 1836, was founded before the University of Southern California.\n\nPassages:\n\n[Williams College]\nWilliams College is a private liberal arts college in Williamstown, Massachusetts, United States. It was established in 1793 with funds from the estate of Ephraim Williams a colonist from the Province of Massachusetts Bay who was killed in the French and Indian War in 1755.\n\n[University of Southern California]\nFounded in 1880, it is the oldest private research university in California.\n\n[Edward Dorr Griffin]\nEdward Dorr Griffin (6 January 1770 – 8 November 1837) was a Christian minister and an American educator who served as President of Williams College from 1821 to 1836 and served as the first pastor of Park Street Church from 1811 to 1815.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3ed5617e7f",
  "kind": "yes/no",
  "text": "Claim: Beethoven regarded Luigi Cherubini as the greatest of his brothers, but not Franz Schreker.\n\nPassages:\n\n[Luigi Cherubini]\nLuigi Cherubini (] ; 8 or 14 September 1760 – 15 March 1842) was an Italian composer who spent most of his working life in France. Beethoven regarded Cherubini as the greatest of his contemporaries.\n\n[Franz Schreker]\nFranz Schreker (originally \"Schrecker\"; 23 March 1878, Monaco – 21 March 1934, Berlin) was an Austrian composer, conductor, teacher and administrator.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qafe94f7aca",
  "kind": "yes/no",
  "text": "Claim: The singer of the live album \" Live at the Corner Hotel\" and Kyle Patrick were both in The Click Five.\n\nPassages:\n\n[Live at the Corner Hotel]\nLive at the Corner Hotel (2008) is a live album by Canadian singer/songwriter Jeff Martin.\n\n[Kyle Patrick]\nKyle Patrick Dickherber (born May 20, 1986, Atlanta, Georgia, United States) is an American singer-songwriter, multi-instrumentalist and producer, best known as the lead singer of Boston power pop band, The Click Five.\n\n[Jeff Martin (Canadian musician)]\nJeffrey Scott Martin (born October 2, 1969 in Windsor, Ontario) is a Canadian guitarist and singer-songwriter best known for fronting the rock band The Tea Party. Martin began his career as a solo artist in October 2005, when The Tea Party went on hiatus.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7d1c723f5b",
  "kind": "yes/no",
  "text": "Tweet: ik it’s for the best but wow RIP to my italy study abroad trip, beyond wonderland, my 21st bday, edc, and now @awonderland’s red rocks show 😔",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qb7e8799a77",
  "kind": "yes/no",
  "text": "Claim: This film co-starred voice artist and comedian Richard Dawson Kiel. Cookbook author Catherine Serre also starred in the film.\n\nPassages:\n\n[Richard Kiel]\nRichard Dawson Kiel (September 13, 1939 – September 10, 2014) was an American actor, voice artist, and comedian, best known for his role as Jaws in the \"James Bond\" franchise, portraying the character in \"The Spy Who Loved Me\" (1977) and \"Moonraker\" (1979); he lampooned the role with a tongue-in-cheek cameo in \"Inspector Gadget\" (1999).\n\n[Catherine Serre]\nShe is known for her credited roles in Moonraker where she played Countess Labinsky, one of the \"perfect\" human specimens from Drax's master race, and in the French Le gendarme et les gendarmettes films, where she appeared together with Nicaise Jean Louis, another Drax Girl from Moonraker.\n\n[Moonraker (film)]\nThe third and final film in the series to be directed by Lewis Gilbert, it co-stars Lois Chiles, Michael Lonsdale, Corinne Cléry, and Richard Kiel.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q577b824eab",
  "kind": "yes/no",
  "text": "Claim: Richard Ira Bong was the famous aviator that died in California while testing a jet aircraft.\n\nPassages:\n\n[R.I. Bong Air Force Base]\nIt was named after the famous aviator, Major Richard Ira Bong, of World War II fame.\n\n[Richard Bong]\nHe died in California while testing a jet aircraft shortly before the Japanese surrendered and the war ended.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q561442d5ad",
  "kind": "yes/no",
  "text": "Claim: The town that is connected by a ferry to Kwadjokrom is a town in the Lake Volta region.\n\nPassages:\n\n[Krachi West District]\nThe Krachi West District is one of the twenty-five (25) districts in the Volta Region.\n\n[Kwadjokrom]\nKwadjokrom is connected by a ferry to the town of Kete Krachi.\n\n[Kete Krachi]\nKete Krachi is a town in the Krachi West District of the Volta Region of Ghana.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3d4510337a",
  "kind": "yes/no",
  "text": "Claim: Wagner Moura received the Golden Globe nomination for playing the lead role of \"The King of Cocaine\".\n\nPassages:\n\n[Pablo Escobar]\nHe was often called \"The King of Cocaine\" and was the wealthiest criminal in history, with an estimated known net worth of US $30 billion by the early 1990s (equivalent to about $ billion as of 2016 ), making him one of the richest men in the world in his prime.\n\n[Wagner Moura]\nHe played the lead role of Pablo Escobar in the Netflix series \"Narcos\" from 2015 to 2016, for which he received a Golden Globe nomination.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q07b03ee0bd",
  "kind": "yes/no",
  "text": "Tweet: Jfc Huntington bank and United Airlines have me fucked up",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qca71efe0c2",
  "kind": "yes/no",
  "text": "Tweet: I’ve been awake for 21 hours",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q6abacbdfbc",
  "kind": "yes/no",
  "text": "Post: I haven’t read enough Twitter today to find a reason to be cross that Kate went to the bandstand tribute so I’m going to remain just really moved and glad she did.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qd6a7d7c660",
  "kind": "yes/no",
  "text": "Claim: Robin R. Bottin is known for his meeting with an American director and producer who won an Academy Award Golden Globe and BAFTA award for what movie The Social Network.\n\nPassages:\n\n[David Fincher]\nDavid Andrew Leo Fincher (born August 28, 1962) is an American director and producer, notably for films, television series and music videos. He was nominated for the Academy Award for Best Director for \"The Curious Case of Benjamin Button\" (2008) and \"The Social Network\" (2010). For the latter, he won the Golden Globe Award for Best Director and the BAFTA Award for Best Direction.\n\n[Rob Bottin]\nRobin R. Bottin (born April 1, 1959) is an American special make-up effects creator. Known for his collaborations with directors John Carpenter, Paul Verhoeven and David Fincher, Bottin worked with Carpenter on both \"The Fog\" and \"The Thing\", with Verhoeven on \"RoboCop\", \"Total Recall\" and \"Basic Instinct\", and with Fincher on \"Se7en\" and \"Fight Club\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2515cf9e1d",
  "kind": "yes/no",
  "text": "Text: For my math exam I have to prove that rectangles do not exist.  HELP",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q0aeba8249d",
  "kind": "yes/no",
  "text": "Claim: Jane's Addiction and Weeping Willows, play the rock genre of music.\n\nPassages:\n\n[Jane's Addiction]\nJane's Addiction is an American rock band from Los Angeles, formed in 1985.\n\n[Weeping Willows]\nWeeping Willows is a Swedish indie rock group that started in 1995.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q663bbd2650",
  "kind": "yes/no",
  "text": "Text: Here is my book that no-one will ever read! 👨🏽‍🔬 https://t.co/EstLa52GEX",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qee4d36ef1f",
  "kind": "yes/no",
  "text": "Claim: Tothill Fields was an 18th-century area of Westminster in the county of Middlesex, a historic county in south-east region of England.\n\nPassages:\n\n[Middlesex]\nMiddlesex ( , abbreviation: Middx) is a historic county in south-east England.\n\n[Tothill Fields]\nTothill Fields was an 18th-century area of Westminster in the county of Middlesex that lay south of St James's Park on the north bank of the river Thames.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q68b9f9e69b",
  "kind": "yes/no",
  "text": "Tweet: Why was I not told Matthew Stafford and Cooper Kupp eat breakfast together before I drafted Robert Woods over him?",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q3fbb778122",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Repulsing people would certainly draw attention.",
   "@BellularGaming Blizzard will have to make sure it doesn't exceed the recommended fun level of 10%."
  ]
 },
 {
  "qid": "q77008a4684",
  "kind": "yes/no",
  "text": "Claim: The board game San Marco came did not come out first out of San Marco and About Time.\n\nPassages:\n\n[About Time (board game)]\nAbout Time is a general knowledge historical board game first seen on Series 5 of the BBC new-business reality show \"Dragon's Den\" on December 17, 2007.\n\n[San Marco (board game)]\nSan Marco is a 2001 designer board game by Alan R. Moon and Aaron Weissblum.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q5485f2ff37",
  "kind": "yes/no",
  "text": "Claim: The central institution of Cheyenne Indian tribal governance that Ehyophsta was not a member of was the Council of Forty-four.\n\nPassages:\n\n[Cheyenne military societies]\nCheyenne military societies are one of the two central institutions of traditional Cheyenne Indian tribal governance, the other being the Council of Forty-four.\n\n[Ehyophsta]\nShe was also a member of a secret society composed exclusively of Cheyenne women.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8e91f61ece",
  "kind": "yes/no",
  "text": "Claim: The 19 high-rise commercial buildings covering 22 acres between 48th and 51st Streets in New York City feature the Art Deco style of architecture.\n\nPassages:\n\n[Rockefeller Center]\nRockefeller Center is a large complex consisting of 19 high-rise commercial buildings covering 22 acre between 48th and 51st Streets in New York City.\n\n[Art Deco in the United States]\nThe Art Deco style, which originated in France just before World War I, had an important impact on architecture and design in the United States in the 1920s and 1930s. The most famous examples were the skyscrapers of New York, including the Empire State Building, Chrysler Building, and Rockefeller Center in New York City.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qceb9c1d670",
  "kind": "yes/no",
  "text": "Claim: The Union established the advisory board that developed the first ironclad warship in Dover, England.\n\nPassages:\n\n[USS Monitor]\nBuilt during the American Civil War, she was the first ironclad warship commissioned by the Union Navy.\n\n[Ironclad Board]\nThe Ironclad Board was an advisory board established by the Union in 1861 in response to the construction of the \"CSS Virginia\" by the Confederacy during the US Civil War.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q97201780e1",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "how you gonna ask me how i’m doing “on this fine labor day” while you’re off, as I’m ringing you out, on labor day. how do you think i am 💀",
   "“I’m working on Labor Day, I am obviously not having a great day as I could be off like you are but I’m not.”"
  ]
 }
]
