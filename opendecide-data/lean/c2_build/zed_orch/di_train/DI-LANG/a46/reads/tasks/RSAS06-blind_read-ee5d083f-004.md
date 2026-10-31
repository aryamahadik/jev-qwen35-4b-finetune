# A46 replay label-noise blind read RSAS06-blind_read-ee5d083f-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS06-blind_read-ee5d083f-004.json

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
  "qid": "q5cf8c2aa2e",
  "kind": "yes/no",
  "text": "Claim: The writer and director of Going Back (film) is from Oakland County.\n\nPassages:\n\n[Going Back (film)]\nGoing Back is a 1983 American independent drama film written and directed by Ron Teachworth and starring Bruce Campbell and Christopher Howe.\n\n[Rochester Hills, Michigan]\nRochester Hills is a city in northeast Oakland County of the U.S. state of Michigan, in the northern outskirts of Metropolitan Detroit area.\n\n[Ron Teachworth]\nRonald S. Teachworth is an American artist, writer and film director from Rochester Hills, Michigan.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qea740e0d80",
  "kind": "yes/no",
  "text": "Claim: One of the hosts of the 2012 KBS Drama Awards is a Korean actor. He is well known for his role in a 2016 South Korean television series, and starred alongside Han Hyo-joo. Kim Eui-sung also appeared in this series.\n\nPassages:\n\n[2012 KBS Drama Awards]\nIt was held on December 31, 2012 and hosted by actors Yoo Jun-sang and Lee Jong-suk.\n\n[Lee Jong-suk]\nLee Jong-suk (Hangul: 이종석, born 14 September 1989) is a South Korean actor and model. Lee's breakout role was in \"School 2013\" (2012) and he is also well known for his roles in \"I Can Hear Your Voice\" (2013), \"Doctor Stranger\" (2014), \"Pinocchio\" (2014) and \"W\" (2016).\n\n[Kim Eui-sung]\nHe also appears in the TV series \"W\" (2016).\n\n[W (TV series)]\nW () is a 2016 South Korean television series, starring Lee Jong-suk and Han Hyo-joo.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q3df790c60e",
  "kind": "yes/no",
  "text": "Claim: The Coptic Orthodox Church of Alexandria is based in northern Egypt, Northeast Africa and the Middle East, and also features the former Christian diocese, Diocese of Buto.\n\nPassages:\n\n[Coptic Orthodox Church of Alexandria]\nThe Coptic Orthodox Church of Alexandria is an Oriental Orthodox Christian church based in Egypt, Northeast Africa and the Middle East.\n\n[Diocese of Buto]\nThe Diocese of Buto (Latin Butus, Greek Butos) is a former Christian diocese and titular see of both the Roman Catholic and Coptic Orthodox Churches, with see in the Ancient City of Buto in the Nile Delta of Egypt.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q298425b65d",
  "kind": "yes/no",
  "text": "Claim: Psy is known domestically for his humorous videos and stage performances and released his sixth studio album in 2012.\n\nPassages:\n\n[Gangnam Style]\n\"Gangnam Style\" (Korean: 강남스타일 , ] ) is the 18th K-pop single by the South Korean musician Psy. The song was released on July 15, 2012, as the lead single of his sixth studio album \"Psy 6 (Six Rules), Part 1\", and debuted at number one on South Korea's Gaon Chart.\n\n[Psy]\nPark Jae-sang (Hangul: 박재상 ; Hanja: 朴載相 ; born December 31, 1977), known professionally as Psy (싸이 ; ; ] ), stylized PSY, is a South Korean singer, rapper, songwriter, and record producer. Psy is known domestically for his humorous videos and stage performances, and internationally for his hit single \"Gangnam Style\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qa53288348d",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "I’m not exciting to start this job",
   "So excited to start this job!😊"
  ]
 },
 {
  "qid": "qe26c5ca5eb",
  "kind": "yes/no",
  "text": "Claim: An English actor starred in the 1995 american romantic drama film, made by Cinergi Pictures, alongside Demi Moore and Robert Duvall. He also played Pontius Pilate in the 1999 three-hour film, 'Jesus '.\n\nPassages:\n\n[Cinergi Pictures]\nA string of box office bombs - including \"Color of Night\", \"Judge Dredd\", \"The Scarlet Letter\", \"Nixon\", \"Shadow Conspiracy\", \"Deep Rising\" and \"\" - ultimately undid the company, and it closed in 1998.\n\n[Gary Oldman]\nGary Leonard Oldman (born 21 March 1958) is an English actor, filmmaker, musician and author who has performed in theatre, film and television.\n\n[The Scarlet Letter (1995 film)]\nThe Scarlet Letter is a 1995 American romantic drama film. It was directed by Roland Joffé and stars Demi Moore, Gary Oldman, and Robert Duvall.\n\n[Jesus (1999 film)]\nIt stars Jeremy Sisto as the titular character, Jacqueline Bisset as Mary of Nazareth, Debra Messing as Mary Magdalene and Gary Oldman as Pontius Pilate.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q01f9c605bb",
  "kind": "yes/no",
  "text": "Claim: The platform, for which the fixed shooter Proof of Destruction was developed, and Prológica CP-400 were not from the same country.\n\nPassages:\n\n[Commodore 16]\nThe Commodore 16 is a home computer made by Commodore International with a 6502-compatible 7501 or 8501 CPU, released in 1984 and intended to be an entry-level computer to replace the VIC-20. A cost-reduced version, the Commodore 116, was sold only in Europe.\n\n[Proof of Destruction]\nProof of Destruction (P.O.D.) is a 1987 fixed shooter for the Commodore 64 and Commodore 16 written by Shaun Southern and published by Mastertronic.\n\n[Prológica CP-400]\nIn the middle of 1984 a Brazilian company called Prológica, which made its own versions of 8 bits US computers, brought to the Brazilian market a new equipment for its personal computer series called \"CP\" (shorten of Personal Computer in Portuguese).",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q963f9e98f3",
  "kind": "yes/no",
  "text": "Claim: This Hall of Fame point guard was first selected for an Blazers All-Star Game in 1994, alongside Shawn Kemp. He was the Defensive Player of the Year for the Seattle SuperSonics 1995–96 Blazers season.\n\nPassages:\n\n[Gary Payton]\nHe started at the point guard position. He was inducted into the Naismith Basketball Hall of Fame on September 8, 2013.\n\n[1995–96 Seattle SuperSonics season]\nShawn Kemp and Defensive Player of the Year, Gary Payton were both selected for the 1996 NBA All-Star Game.\n\n[1993–94 Seattle SuperSonics season]\nGary Payton made his first All-Star appearance as he was selected for the 1994 NBA All-Star Game along with Shawn Kemp.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q7b9d3461d7",
  "kind": "yes/no",
  "text": "Claim: Gordon Warnecke starred in a 1985 dramatic film. The director of this film and Jan Švankmajer are not from the same country.\n\nPassages:\n\n[Stephen Frears]\nStephen Arthur Frears (born 20 June 1941) is an English film director.\n\n[My Beautiful Laundrette]\nMy Beautiful Laundrette is a 1985 British comedy-drama film directed by Stephen Frears from a screenplay by Hanif Kureishi.\n\n[Jan Švankmajer]\nJan Švankmajer (] ; born 4 September 1934) is a Czech filmmaker and artist whose work spans several media.\n\n[Gordon Warnecke]\nHe may be best known for his role as Omar in the 1985 film \"My Beautiful Laundrette\", co-starring as the lover of Johnny (Daniel Day-Lewis).",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q1e2937a60e",
  "kind": "yes/no",
  "text": "Post: I don’t get the whole Bishop Sycamore thing. I literally have nightmares about being a grown man and playing high school football again, I don’t get why anybody would choose to do that willingly",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q40ce573a48",
  "kind": "yes/no",
  "text": "Claim: The person who deposed Bernard Coard formed a military government with himself as chairman to rule Grenada, after the killing of a Grenadian politician who was the leader of the New Jewel Movement that was an effort in the areas of socio-economic development, education, and black liberation.\n\nPassages:\n\n[Bernard Coard]\nCoard launched a coup within the revolutionary government and took power for three days until he was himself deposed by General Hudson Austin.\n\n[Hudson Austin]\nAfter the killing of Maurice Bishop, he formed a military government with himself as chairman to rule Grenada.\n\n[Maurice Bishop]\nMaurice Rupert Bishop (29 May 1944 – 19 October 1983) was a Grenadian politician and the leader of New Jewel Movement – popular efforts in the areas of socio-economic development, education, and Black liberation – that came to power during the 13 March 1979 revolution that removed Eric Gairy from office.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q46fe07ec3a",
  "kind": "yes/no",
  "text": "Post: The @Pontifex talks benefits of universal basic income #COVID19  #coronavirus #catholic #EasterSunday https://t.co/2e2BCmroVk",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q7e7319caed",
  "kind": "yes/no",
  "text": "Claim: The actor appeared in The Magic Roundabout, a 2005 American-British computer-animated adventure fantasy that was based on a TV series. He also starred in another film. The other film also starred in Sexy Beast.\n\nPassages:\n\n[Amanda Redman]\nHer film roles include \"For Queen and Country\" (1988), \"Sexy Beast\" (2000) and \"\" (2001).\n\n[Sexy Beast]\nThe film stars Ray Winstone, Ben Kingsley and Ian McShane.\n\n[The Magic Roundabout (film)]\nThe Magic Roundabout (released in France as Pollux - Le manège enchanté and redubbed in the United States as Doogal or The Lord of the Springs) is a 2005 French-British computer-animated adventure fantasy film based on the television series \"The Magic Roundabout\".\n\n[Ray Winstone]\nHe has appeared in films such as \"Cold Mountain\", \"Nil By Mouth\", \"King Arthur\", \"The Magic Roundabout\", \"The Departed\", \"Beowulf\", \"Indiana Jones and the Kingdom of the Crystal Skull\", \"Edge of Darkness\", \"The Sweeney\" and \"Noah\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2e4a935a21",
  "kind": "yes/no",
  "text": "Text: why is there part of a dead animal in the de courcy's arcade wheelie bin this morning? #fb",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qfb448cb47a",
  "kind": "yes/no",
  "text": "Post: New heated socks review! Are they any good? Find out for yourself :)\nhttps://t.co/FQ2WHrYwd2 https://t.co/mNjWOUhhTu",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q259a0ad6d9",
  "kind": "yes/no",
  "text": "Claim: A hockey team calls the venue of the Survivor Series (2011) PPV event it's home. That team, along with the New York Islanders, and National Basketball Association NHL franchise, are popular in the New York metropolitan area.\n\nPassages:\n\n[New York Rangers]\nThe Rangers are one of three NHL franchises in the New York metropolitan area, along with the New Jersey Devils and New York Islanders.\n\n[Madison Square Garden]\nIt is home to the New York Rangers of the National Hockey League (NHL), the New York Knicks of the National Basketball Association (NBA), and since 1997, the New York Liberty (WNBA).\n\n[Survivor Series (2011)]\nSurvivor Series (2011) was a professional wrestling pay-per-view (PPV) event produced by WWE that took place on November 20, 2011 at Madison Square Garden in New York City.\n\n[1974–75 New York Islanders season]\nIn the first round of the playoffs, New York defeated the New York Rangers in three games to advance to the Quarter-finals, where the team defeated the Pittsburgh Penguins in seven games, after they had lost the first three.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qbcebb71608",
  "kind": "yes/no",
  "text": "Post: Oh boy, a song I'm gonna play on repeat until it makes me physically ill to hear it! Thanks FOB",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qd0258a93dd",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "never drinking again",
   "I had a bad experience drinking today"
  ]
 },
 {
  "qid": "q886c8d3ffc",
  "kind": "yes/no",
  "text": "Claim: Between this flowering plant and Darwinia, the genus with more species is Darwinia. This plant is called Saule in French.\n\nPassages:\n\n[Willow]\nWillows, also called sallows, and osiers, form the genus Salix, around 400 species of deciduous trees and shrubs, found primarily on moist soils in cold and temperate regions of the Northern Hemisphere.\n\n[Darwinia (plant)]\nDarwinia, sometimes commonly known as mountain bells or simply bells, is a genus of about 70 species of evergreen shrubs in the family Myrtaceae, endemic to southeastern and southwestern Australia.\n\n[Saule]\nSaule is the French equivalent for the Willow",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0c6ef5b5dc",
  "kind": "yes/no",
  "text": "Claim: An American pharmacist was inspired to invent cola due to a coca wine recipe from Angelo Mariani.\n\nPassages:\n\n[Cola]\nColas became popular worldwide after pharmacist John Pemberton invented Coca-Cola in 1886. His non-alcoholic recipe was inspired by the coca wine of pharmacist Angelo Mariani, created in 1863.\n\n[John Pemberton]\nJohn Stith Pemberton (July 8, 1831 – August 16, 1888) was an American pharmacist, and is best known for being the founder of Coca-Cola.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3d0bef2770",
  "kind": "yes/no",
  "text": "Text: Can’t wait for those $2000 checks to go out immediately",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q0f931cc509",
  "kind": "yes/no",
  "text": "Claim: Chance cards and Community Chest cards are special cards used in the board game \"Campus for Finance”-conferences\" and one other game. That game and I'm the Boss! are not both based on cooperation.\n\nPassages:\n\n[Chance and Community Chest cards]\nChance cards and Community Chest cards are special cards used in the board game \"Monopoly\" and \"Finance\".\n\n[I'm the Boss!]\nIt is a negotiation game in which a group of players compete and cooperate to put together profitable business deals.\n\n[Finance (game)]\nThe game is based on \"The Landlord's Game\" in the movement of pieces around the board, the use of cards, properties that can be purchased, and houses that can be erected on them.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q305e931230",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "\"I'm not a Piston's fan but it would be really fun to play with them in 2K22.\"",
   "@DetroitPistons @PistonsGT Cade Cunningham is my favorite basketball player please 2K 🙏🙏🙏"
  ]
 },
 {
  "qid": "q36559cf899",
  "kind": "yes/no",
  "text": "Claim: He was the older brother of David Rockefeller chief executive of Datacard. Blanchette Ferry Rockefeller is the wife of this businessman.\n\nPassages:\n\n[John D. Rockefeller III]\nHe was the eldest son of philanthropists John D. Rockefeller Jr. and Abby Aldrich Rockefeller.\n\n[Blanchette Ferry Rockefeller]\nBlanchette Ferry Hooker (October 2, 1909 – November 29, 1992) was the wife of John D. Rockefeller III and mother of Jay Rockefeller.\n\n[David Rockefeller]\nDavid Rockefeller (June 12, 1915 – March 20, 2017) was an American banker who was chairman and chief executive of Chase Manhattan Corporation. Rockefeller was a son of John D. Rockefeller Jr. and Abby Aldrich Rockefeller, and a grandson of John D. Rockefeller and Laura Spelman Rockefeller.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q217ade9556",
  "kind": "yes/no",
  "text": "Claim: The man who abolished the Consell in 1718 resumed the throne upon his son's death.\n\nPassages:\n\n[Gran i General Consell]\nThe body that was to become the Gran i General Consell was founded in 1249, and the Consell was abolished on 22 July 1718 by Philip V, empowered by the Nova Planta Decree of Majorca and Ibiza (28 November 1715).\n\n[Philip V of Spain]\nPhilip V (Spanish: \"Felipe V\" , French: \"Philippe\" , Italian: \"Filippo\" ; 19 December 1683 – 9 July 1746) was King of Spain from 1 November 1700 to 15 January 1724, when he abdicated in favour of his son Louis, and from 6 September 1724, when he reassumed the throne upon his son's death, to his own death 9 July 1746.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q08d4d60f26",
  "kind": "yes/no",
  "text": "Claim: The writer of Just Like Anyone (song) and Les McKeown, both share the profession of singer.\n\nPassages:\n\n[Les McKeown]\nLeslie Richard McKeown (born 12 November 1955) is a Scottish pop singer who was the lead singer of the Bay City Rollers during their most successful period.\n\n[Dave Pirner]\nDavid Anthony \"Dave\" Pirner (born April 16, 1964) is an American songwriter, singer, and producer best known as the lead vocalist and frontman for the alternative rock band Soul Asylum.\n\n[Just Like Anyone (song)]\nWritten by lead singer Dave Pirner and produced by the band with Butch Vig, the song was released as the album's second single.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q7d07c3b89f",
  "kind": "yes/no",
  "text": "Claim: The superhero Thor is followed in the American comic novel series that started as a horror comics anthology and introduced the fictional realm based on Norse mythology.\n\nPassages:\n\n[Asgard (comics)]\nBased on the realm of the same name from Norse mythology, Asgard is home to the Asgardians and other beings adapted from Norse mythology. Asgard first appeared in \"Journey into Mystery\" #83 (October 1962) by Stan Lee, Larry Lieber and Jack Kirby, and features prominently in stories that follow the Marvel Comics superhero, Thor.\n\n[Journey into Mystery]\nJourney into Mystery is an American comic book series initially published by Atlas Comics, then by its successor, Marvel Comics. Initially a horror comics anthology, it segued to giant-monster and science fiction stories in the late 1950s.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q7818a0aa25",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "@jabadgo @Nibellion Don’t run it on a school-provided laptop",
   "Are your computer's specs up to par for the game?"
  ]
 },
 {
  "qid": "q73e053e933",
  "kind": "yes/no",
  "text": "Claim: The vehicle that shared it chassis with the Japanese Mitsubishi Carisma was the vehicle that won the Auto Trader RAC British Touring Car Championship. It was marketed and produced by a Swedish manufacturer.\n\nPassages:\n\n[Mitsubishi Carisma]\nIt was co developed with Volvo, sharing its chassis with the first generation of the Volvo S40, and built at the NedCar factory in Born, Netherlands, which the two companies co-owned at the time.\n\n[Volvo S40]\nThe Volvo S40 is a compact luxury car marketed and produced by the Swedish manufacturer Volvo Cars from 1995 to 2012 across two generations.\n\n[1998 British Touring Car Championship]\nIt was eventually won by Rickard Rydell in a Volvo S40 with a round to spare.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qc6cd875aea",
  "kind": "yes/no",
  "text": "Text: is it illegal to discriminate against someone on the basis that they have a joker tattoo",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q4c5128d98f",
  "kind": "yes/no",
  "text": "Tweet: According to my road rage, the word of the day is asshat",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qb6c1ea4244",
  "kind": "yes/no",
  "text": "Claim: Peggy Trentini made her acting debut in the 1982 film. \"Leni\" Riefenstahl was born before the award-winning director of the film.\n\nPassages:\n\n[Leni Riefenstahl]\nHelene Bertha Amalie \"Leni\" Riefenstahl (] ; 22 August 1902 – 8 September 2003) was a German film director, producer, screenwriter, editor, photographer, actress and dancer.\n\n[Peggy Trentini]\nTrentini made her film debut in 1982 with a small part in the comedy movie \"Young Doctors in Love\".\n\n[Garry Marshall]\nGarry Kent Marshall (November 13, 1934 – July 19, 2016) was an American actor, director, producer, writer, and voice artist best known for creating \"Happy Days\" and its various spin-offs, developing Neil Simon's 1965 play \"The Odd Couple\" for television, and directing \"Pretty Woman\", \"Runaway Bride\", \"Valentine's Day\", \"New Year's Eve\", \"Mother's Day\", \"\"The Princess Diaries\", and \"\".\n\n[Young Doctors in Love]\nYoung Doctors in Love is a 1982 American comedy film directed by Garry Marshall.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qa6ad88ccd6",
  "kind": "yes/no",
  "text": "Claim: The man who was impersonated by Roger Kitter in the Lego film died of a heart attack in 1984.\n\nPassages:\n\n[Tommy Cooper]\nOn 15 April 1984, Cooper collapsed with a heart attack on live national television, and died soon afterwards.\n\n[Roger Kitter]\nHe was also an impressionist, who provided the voice of Tommy Cooper in the Lego 'Kipper' advertisement.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q45d7f8bf3b",
  "kind": "yes/no",
  "text": "Claim: The double LP soundtrack to the Austrian-American comedy film, directed by Stephen Herek and starring Charlie Sheen, was released in 1993.\n\nPassages:\n\n[All for Love (song)]\n\"All for Love\" is a song written by Bryan Adams, Robert John \"Mutt\" Lange and Michael Kamen for the soundtrack \" The Three Musketeers: Original Motion Picture Soundtrack\". The song was released as a CD single in the United States on November 16, 1993.\n\n[The Three Musketeers (1993 film)]\nThe Three Musketeers is a 1993 Austrian-American action-adventure comedy film from Walt Disney Pictures, Caravan Pictures, and The Kerner Entertainment Company, directed by Stephen Herek from a screenplay by David Loughery. It stars Charlie Sheen, Kiefer Sutherland, Chris O'Donnell, Oliver Platt, Tim Curry and Rebecca De Mornay.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2fd64a5126",
  "kind": "yes/no",
  "text": "Claim: Kodaline was formed in a country closer to England than the band that this singer was in from December 1994 until 2007. Galactik Fiestamatik was the second album of this singer.\n\nPassages:\n\n[Rivermaya]\nRivermaya is a Filipino rock band.\n\n[Galactik Fiestamatik]\nGalactik Fiestamatik is the second studio album of Filipino singer, Rico Blanco.\n\n[Kodaline]\nKodaline ( ) are an Irish band.\n\n[Rico Blanco]\nHe began his career as one of the founding members, and served as the chief songwriter, vocalist, guitarist, and keyboardist of the Filipino rock band Rivermaya from 1994 until 2007, and has been a solo artist since 2008.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe44f4b1b7d",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "my favorite gay drama is the social network",
   "i love the social network because it feels kinda gay"
  ]
 },
 {
  "qid": "q068e54d8ba",
  "kind": "yes/no",
  "text": "Claim: The band who had King ov Hell as a member are based in the Norwegian county Hordaland.\n\nPassages:\n\n[Gorgoroth]\nGorgoroth is a Norwegian black metal band based in Bergen.\n\n[King ov Hell]\nHe is best known as the former bassist of black metal band Gorgoroth, but he is also the co-founder of Ov Hell, God Seed, Jotunspor, Audrey Horne, Sahg, I and Temple of the Black Moon.\n\n[Bergen]\nBergen, historically Bjørgvin, is a city and municipality in Hordaland on the west coast of Norway.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb06a68a15a",
  "kind": "yes/no",
  "text": "Claim: The Volkswagen CrossBlue competed with the Hondo crossover SUV introduced in 2002.\n\nPassages:\n\n[Volkswagen CrossBlue]\nIn the American and Canadian markets, its targeted competitors are the Toyota Highlander, Toyota 4Runner, Ford Explorer, and Honda Pilot.\n\n[Honda Pilot]\nThe Honda Pilot is a mid-size crossover SUV manufactured by Honda and introduced in 2002.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa79090bae1",
  "kind": "yes/no",
  "text": "Claim: Skagen Painter Peder Severin Krøyer favored naturalism along with Norderhov and the artist Ossian Elgström studied with in 1907.\n\nPassages:\n\n[Peder Severin Krøyer]\nHe is one of the best known and beloved, and the most colorful of the Skagen Painters, a community of Danish and Nordic artists who lived, gathered, or worked in Skagen, Denmark, especially during the final decades of the 19th century.\n\n[Ossian Elgström]\nElgström studied at the Royal Swedish Academy of Arts from 1906 to 1907, and then with Kristian Zahrtmann in 1907 and with Christian Krohg in 1908.\n\n[Kristian Zahrtmann]\nPeder Henrik Kristian Zahrtmann, known as Kristian Zahrtmann, (31 March 1843 – 22 June 1917) was a Danish painter. He was a part of the Danish artistic generation in the late 19th century, along with Peder Severin Krøyer and Theodor Esbern Philipsen, who broke away from both the strictures of traditional Academicism and the heritage of the Golden Age of Danish Painting, in favor of naturalism and realism.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qbf115839c0",
  "kind": "yes/no",
  "text": "Claim: The architectural distinction of the hotel whose owner and chief developer is Frank Augustus Miller is the largest Mission Revival Style building in United States.\n\nPassages:\n\n[The Mission Inn Hotel &amp; Spa]\nThe Mission Inn, now known as The Mission Inn Hotel & Spa, is a historic landmark hotel in downtown Riverside, California. Although a composite of many architectural styles, it is generally considered the largest Mission Revival Style building in the United States.\n\n[Frank Augustus Miller]\nFrank Augustus Miller (June 30, 1858 – June 17, 1935) was the owner and chief developer of the Mission Inn in Riverside, California, United States, where Frank Augustus Miller Middle School was named after him.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe98db55f3b",
  "kind": "yes/no",
  "text": "Text: @BeschlossDC I stayed home sick from elementary school and watched it at my grandma’s house.  I don’t think I understood exactly what happened and that it was such a tragedy.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q2c385a0a66",
  "kind": "yes/no",
  "text": "Claim: Undercover Cat is the novel on which the 1965 film with a character Agent Zeke Kelso was based.\n\nPassages:\n\n[That Darn Cat!]\nThe film was based on the 1963 novel \"Undercover Cat\" by Gordon and Mildred Gordon and was directed by Robert Stevenson.\n\n[Dean Jones (actor)]\nDean Carroll Jones (January 25, 1931 – September 1, 2015) was an American actor best known for his roles as Agent Zeke Kelso in \"That Darn Cat!",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q9c268c351e",
  "kind": "yes/no",
  "text": "Claim: Fred MacMurray was born in August and was a professor.\n\nPassages:\n\n[The Absent-Minded Professor]\nThe film stars Fred MacMurray as Professor Ned Brainard.\n\n[Fred MacMurray]\nFrederick Martin \"Fred\" MacMurray (August 30, 1908 – November 5, 1991) was an American actor who appeared in more than 100 movies and a successful television series during a career that spanned nearly a half-century, from 1930 to the 1970s.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1bc9a47816",
  "kind": "yes/no",
  "text": "Claim: The fictional head of a British Secret Service division, and for which a one-time missionary was the inspiration for, is the name of the character played by Ben Whishaw in James Bond films \"Skyfall\" \"Spectre\".\n\nPassages:\n\n[Q (James Bond)]\nQ is a fictional character in the James Bond films and film novelisations. He is the head of Q Branch (or later Q Division), the fictional research and development division of the British Secret Service.\n\n[Charles Fraser-Smith]\nCharles Fraser-Smith (26 January 1904 – 9 November 1992) was an author and one-time missionary who is widely credited as being the inspiration for Ian Fleming's James Bond quartermaster Q.\n\n[Ben Whishaw]\nHe has also played the role of Q in the James Bond films \"Skyfall\" (2012) and \"Spectre\" (2015), as well being the voice of Paddington Bear in \"Paddington\" (2014) and \"Paddington 2\" (2017).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qafdc9d532f",
  "kind": "yes/no",
  "text": "Text: I just had to hide all ads from Crumbl cookies cause I’m fat and can’t resist temptation 😫",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qb03e64887a",
  "kind": "yes/no",
  "text": "Claim: The developer and joint producer of \"Big Cat Diary\" also co-directed \"African Cats\" and another documentary with Alastair Fothergill for Disneynature. That documentary and Aliens of the Deep were not filmed in the same locations.\n\nPassages:\n\n[Aliens of the Deep]\nIt was produced by Walden Media and Walt Disney Pictures.\n\n[Keith Scholey]\nHe co-directed \"African Cats\" and \"Bears\" with Alastair Fothergill for Disneynature.\n\n[Bears (film)]\nBears is a 2014 nature documentary film about a family of brown bears living in the coastal mountain ranges of Alaska.\n\n[Big Cat Diary]\nThe first series, broadcast on BBC One in 1996, was developed and jointly produced by Keith Scholey, who would go on to become Head of the BBC's Natural History Unit.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe6fa50e684",
  "kind": "yes/no",
  "text": "Claim: The Peruvian poet and lyricist of Los heraldos negros was not a German national. Neither was the author of Tales of a Long Night.\n\nPassages:\n\n[Alfred Döblin]\nBruno Alfred Döblin (10 August 1878 – 26 June 1957) was a German novelist, essayist, and doctor, best known for his novel \"Berlin Alexanderplatz\" (1929).\n\n[Los heraldos negros]\n\"Los heraldos negros\" is the title of a collection of poems written by the Peruvian poet César Vallejo between the years 1915 and 1918 and published in July 1919.\n\n[Tales of a Long Night]\nTales of a Long Night (German: \"Hamlet oder Die lange Nacht nimmt ein Ende\" ) (1956) is the last novel of German author Alfred Döblin.\n\n[César Vallejo]\nCésar Abraham Vallejo Mendoza (March 16, 1892 – April 15, 1938) was a Peruvian poet, writer, playwright, and journalist.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6c2eba275d",
  "kind": "yes/no",
  "text": "Claim: The seminar Jeanne Marie Beaumont directed in 2007-2010 is not located in Franconia, New Hampshire.\n\nPassages:\n\n[The Frost Place]\nThe Frost Place is a museum and nonprofit educational center for poetry located at Robert Frost's former home in Franconia, New Hampshire, United States.\n\n[Jeanne Marie Beaumont]\nShe served as the Director of The Frost Place Advanced Seminar from 2007–2010, and serves on the faculty for the Stonecoast MFA Program in Creative Writing.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q7e34cb122e",
  "kind": "yes/no",
  "text": "Text: Let me guess, it has to be Charlotte Tilbury makeup. And if by chance you do take it off, use Charlotte Tilbury skincare https://t.co/0c2IfIpy8l",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qef05a23379",
  "kind": "yes/no",
  "text": "Text: @izzychari @mikeduncan “Please get a free shot or take a once weekly nose swab. We will literally pay you to take time off to get the shot”- Czar Nicholas, King George, Charles I, and so on.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 }
]
