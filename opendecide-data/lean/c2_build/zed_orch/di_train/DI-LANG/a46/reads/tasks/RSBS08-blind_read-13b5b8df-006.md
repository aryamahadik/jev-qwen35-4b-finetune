# A46 replay label-noise blind read RSBS08-blind_read-13b5b8df-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS08-blind_read-13b5b8df-006.json

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
  "qid": "q8ef6d720ce",
  "kind": "yes/no",
  "text": "Claim: The type of students who can't attend the school adjacent to Pilgram Hospital are girls aged 11 to 18.\n\nPassages:\n\n[Boston High School]\nBoston High School, also known as \"Boston High School for Girls\", is a selective grammar school and sixth form college for girls aged 11 to 18 in Boston, Lincolnshire, England.\n\n[Pilgrim Hospital]\nPilgrim Hospital is a large hospital in the east of Lincolnshire on the A16, north of the town of Boston near the mini-roundabout with the A52. It is situated virtually on the Greenwich Meridian and adjacent to Boston High School.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3f98025ff7",
  "kind": "yes/no",
  "text": "Claim: A star of \"Hotline\", a 2014 film, and Millard Webb are both authors.\n\nPassages:\n\n[Millard Webb]\nMillard Webb (6 December 1893 – 21 April 1935), was an American screenwriter and director.\n\n[Hotline (2014 film)]\nThe film stars Miss Cleo, Jeff Ragsdale, Jamie Blaine, and Tonya Jone Miller.\n\n[Jeff Ragsdale]\nJeffrey Charles \"Jeff\" Ragsdale ( ) is an American author, documentary filmmaker, actor and stand-up comedian.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q917d1462df",
  "kind": "yes/no",
  "text": "Claim: The Cinematic Orchestra was signed to the record label based in London.\n\nPassages:\n\n[The Cinematic Orchestra]\nThe group is signed to independent record label Ninja Tune.\n\n[Ninja Tune]\nNinja Tune is an English independent record label based in London.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q58b572aec3",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "shoutout to the kid who brought a pineapple to hc and threw it around #madrespect",
   "\"Screw the kid who brought a pineapple to homecoming and threw it around\""
  ]
 },
 {
  "qid": "q8f25cf8bd9",
  "kind": "yes/no",
  "text": "Claim: The film Killing of a Sacred Deer with actor Barry Keoghan was selected to compete for the Palme d'Or.\n\nPassages:\n\n[Barry Keoghan]\nBarry Keoghan (born 18 October 1992) is an Irish actor. He has appeared in the films \"Dunkirk\" along with Mark Rylance, Tom Hardy, Cillian Murphy, Kenneth Branagh, Tom Glynn-Carney; \"The Killing of a Sacred Deer\" with Nicole Kidman, Colin Farrell and Alicia Silverstone; and \"Trespass Against Us\" with Michael Fassbender and Brendan Gleeson.\n\n[The Killing of a Sacred Deer]\nIt was selected to compete for the Palme d'Or in the main competition section at the 2017 Cannes Film Festival.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe38b236447",
  "kind": "yes/no",
  "text": "Tweet: When you get woken up at 3am because of aftershocks from an earthquake 👍😩",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qddd6f4c60d",
  "kind": "yes/no",
  "text": "Claim: The player who teamed up with Elena Bovina for the 2003 Family Circle Cup – Doubles. Her and Renáta Tomanová were both tennis players.\n\nPassages:\n\n[Rennae Stubbs]\nRennae Stubbs (born 26 March 1971) is an Australian retired tennis player.\n\n[Renáta Tomanová]\nRenáta Tomanová (born 9 December 1954) is a former professional tennis player from Czechoslovakia.\n\n[2003 Family Circle Cup – Doubles]\nLisa Raymond and Rennae Stubbs were the defending champions, but Raymond did not compete in this edition.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3052209afc",
  "kind": "yes/no",
  "text": "Text: @ArenaSwansea @creedfs Specialty starter or light bite featuring laverbread.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qf2ebd8e8b6",
  "kind": "yes/no",
  "text": "Claim: The Cincinnati metropolitan area at the south of the location where DMAX (engines) is based had a population of 2,114,580 in 2010 U.S. Census.\n\nPassages:\n\n[Cincinnati metropolitan area]\nAs of the 2010 U.S. Census, this MSA had a population of 2,114,580, the largest metropolitan area involving Ohio and 27th largest in the United States.\n\n[Moraine, Ohio]\nMoraine, as part of the Dayton area, is situated within the Miami Valley region of Ohio, just north of the Cincinnati metropolitan area.\n\n[DMAX (engines)]\nDMAX of Moraine, Ohio, is a manufacturer of diesel engines for trucks. DMAX, originally announced in December 1998, is a 60-40 joint venture between and operated by General Motors and Isuzu.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q294c2e2fff",
  "kind": "yes/no",
  "text": "Claim: Pelle Almqvist is younger than the saxophonist who played synthesizers on the track \"Got a Hold on Me\".\n\nPassages:\n\n[Pelle Almqvist]\nPer \"Pelle\" Almqvist (born 29 May 1978), also known as Howlin' Pelle Almqvist, is a Swedish singer and songwriter.\n\n[Got a Hold on Me]\nSynthesizers on the track were played by Steve Winwood, while the guitars were played by Todd Sharp (the song's co-writer) and McVie's Fleetwood Mac bandmate Lindsey Buckingham.\n\n[Steve Winwood]\nStephen Lawrence \"Steve\" Winwood (born 12 May 1948) is an English musician whose genres include rock, blue-eyed soul, rhythm and blues, blues rock, pop rock, and jazz.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q0ad949786f",
  "kind": "yes/no",
  "text": "Claim: The director of All the Love You Cannes! and not Jay T. Wright, was the American filmmaker who co-founded Troma Entertainment film studio.\n\nPassages:\n\n[All the Love You Cannes!]\nis a 2002 documentary film directed by Lloyd Kaufman.\n\n[Jay T. Wright]\nThis tension acts, in many of his films, as a competing motive and sometimes in direct conflict with any idea of narrative.\n\n[Lloyd Kaufman]\nStanley Lloyd Kaufman, Jr. (born December 30, 1945) is an American film director, producer, screenwriter, and actor. With producer Michael Herz, he is the co-founder of Troma Entertainment film studio, and the director of many of their feature films, including \"The Toxic Avenger\" and \"Tromeo and Juliet\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q48cc4d9cb8",
  "kind": "yes/no",
  "text": "Claim: Doñana National Park was a nature reserve that was established in 1969. The place where the river Tiétar flows into the Baikal lynx was not established in 1969.\n\nPassages:\n\n[Tiétar (river)]\nIt flows into the Tagus at Monfragüe.\n\n[Monfragüe]\nMonfragüe (Spanish: \"Parque Nacional Monfragüe\") is a Spanish national park noted for its bird-life.\n\n[Doñana National Park]\nDoñana National Park is a natural reserve in Andalusia, southern Spain, in the provinces of Huelva (most of its territory) and Seville. It was established as a nature reserve in 1969 when the World Wildlife Fund joined with the Spanish government and purchased a section of marshes to protect it.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q289bda6c17",
  "kind": "yes/no",
  "text": "Claim: The Greek surrealist poet that wrote Capitale de la douleur was from the same country as this author. Laurence Bataille was the daughter of this man.\n\nPassages:\n\n[Capitale de la douleur]\nCapitale de la douleur (\"Capital of Pain\") is a book of poems by French surrealist poet Paul Éluard.\n\n[Georges Bataille]\nGeorges Albert Maurice Victor Bataille (] ; 10 September 1897 – 9 July 1962) was a French intellectual and literary figure working in literature, philosophy, anthropology, economics, sociology and history of art.\n\n[Paul Éluard]\nPaul Éluard (] ), born Eugène Émile Paul Grindel (] ; 14 December 1895 – 18 November 1952), was a French poet and one of the founders of the surrealist movement.\n\n[Laurence Bataille]\nShe was the only daughter of the writer Georges Bataille and the actress Sylvia Bataille.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q73207ee324",
  "kind": "yes/no",
  "text": "Claim: The writer of Anne of Avonlea (1975 drama film), is the author that is known for her \"Anne of Green Gables\" books. She is not to be confused with the author of The Mitford Years.\n\nPassages:\n\n[Anne of Avonlea (1975 film)]\nIt is based on \"Anne of Avonlea\", the sequel to \"Anne of Green Gables\" by Lucy Maud Montgomery.\n\n[Lucy Maud Montgomery]\nLucy Maud Montgomery {'1': \", '2': \", '3': \", '4': \"} (November 30, 1874 – April 24, 1942) published as L.M. Montgomery, was a Canadian author best known for a series of novels beginning in 1908 with \"Anne of Green Gables\".\n\n[Jan Karon]\nJan Karon is an American novelist who writes for both adults and young readers.\n\n[The Mitford Years]\nThe Mitford Years is a series of ten novels by American writer Jan Karon, set in the fictional town of Mitford, North Carolina.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf9276ce718",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I love this site",
   "Hate this site [CHIRPBIRDICON]"
  ]
 },
 {
  "qid": "qa859062de5",
  "kind": "yes/no",
  "text": "Tweet: Pro tip don’t eat half a jar of spicy salsa late at night.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qc88b17528a",
  "kind": "yes/no",
  "text": "Post: @ZionWarrior6 I think lunch was ready at the care home, then it was time for nap and then Countdown.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q8553f49518",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "My ancestors spoke about a lot of true things",
   "“tit for tat, butter for fat, you kill my dog, i eat your cat” is a liberian proverb for “an eye for an eye”. my ancestors were spittin’"
  ]
 },
 {
  "qid": "qe4acd96bd4",
  "kind": "yes/no",
  "text": "Claim: The 1986 film \"Look Out, Officer!\" is a remake of a comedy film. The original starred Hong Kong-based actress that also starred in comedy Tv series Last Song in Paris.\n\nPassages:\n\n[Look Out, Officer!]\n\", which starred Sammo Hung.\n\n[Last Song in Paris]\nLast Song in Paris is a 1986 Hong Kong romance film written and directed by Chor Yuen and starring Leslie Cheung, Anita Mui, Joey Wong and Cecilia Yip\n\n[Where's Officer Tuba?]\nis a 1986 Hong Kong action comedy film directed by Philip Chan and Ricky Lau and starring Sammo Hung, David Chiang, Jacky Cheung and Joey Wong.\n\n[Joey Wong]\nJoey Wong Cho-Yee (AKA Joey Wang, Wang Tsu Hsien, or Joey Ong Jyo Han/Hen) (, born January 31, 1967) is a Hong Kong based Taiwanese-born actress.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qb06c53d021",
  "kind": "yes/no",
  "text": "Post: @Schadenfury I know! Just pop the subtitles on. Sorted.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q3f682d2c3a",
  "kind": "yes/no",
  "text": "Claim: A cocktail served in a Hurricane drinking glass and Fish House Punch both contain alcohol.\n\nPassages:\n\n[Hurricane glass]\nOther drinks served in this glass include the Singapore Sling, June bug, Piña colada and Blue Hawaii.\n\n[Fish House Punch]\nFish House Punch is a strong, rum-based punch containing rum, cognac, and peach brandy.\n\n[Singapore Sling]\nThe Singapore Sling is a gin-based cocktail from Singapore.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q755e2eb9dd",
  "kind": "yes/no",
  "text": "Claim: Undercover Cat is the novel on which the 1965 film with a character Agent Zeke Kelso was based.\n\nPassages:\n\n[That Darn Cat!]\nThe film was based on the 1963 novel \"Undercover Cat\" by Gordon and Mildred Gordon and was directed by Robert Stevenson.\n\n[Dean Jones (actor)]\nDean Carroll Jones (January 25, 1931 – September 1, 2015) was an American actor best known for his roles as Agent Zeke Kelso in \"That Darn Cat!",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4351ded32b",
  "kind": "yes/no",
  "text": "Claim: The singer of the first half of Brand New Love Affair (Song) is not Aeolian. Neither is the vocalist of The Halo Method.\n\nPassages:\n\n[Brand New Love Affair (song)]\nGuitarist Terry Kath sings the first half while bassist Peter Cetera sings the second half.\n\n[Terry Kath]\nTerry Alan Kath (January 31, 1946 – January 23, 1978) was an American musician and songwriter, best known as the original guitarist, one of the lead singers and founding members of the rock band Chicago.\n\n[Lukas Rossi]\nLukas Rossi (born December 21, 1976) is a Canadian rock musician and was the winner of the CBS Television reality series \"\" - a televised audition contest to become lead singer of the hard rock supergroup \"Rock Star Supernova\".\n\n[The Halo Method]\nIt consisted of guitarist Ben Moody (We Are the Fallen, ex-Evanescence), drummer Miles McPherson, vocalist Lukas Rossi (ex-Rock Star Supernova, ex-Daylight Division) and bassist Josh Newell (ex-In This Moment).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q94cd9db0ff",
  "kind": "yes/no",
  "text": "Tweet: Very good analysis and a good demonstration of why you should treat anything your told by the BBC with the utmost care. https://t.co/V6rO4FZqeP",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q31b26b72ff",
  "kind": "yes/no",
  "text": "Claim: Rudolf Kjellén's work was influenced by the person who coined the phrase Lebensraum; the political movement which made it notorious by taking it to extremes was the German Nazi Party.\n\nPassages:\n\n[Lebensraum]\n<ref name=\"E/N301\"> </ref> The most extreme form of this ideology was supported by the Nazi Party (NSDAP) and Nazi Germany until the end of World War II.\n\n[Friedrich Ratzel]\nFriedrich Ratzel (August 30, 1844 – August 9, 1904) was a German geographer and ethnographer, notable for first using the term \"Lebensraum\" (\"living space\") in the sense that the National Socialists later would.\n\n[Rudolf Kjellén]\nHis work was influenced by Friedrich Ratzel.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc2232d256a",
  "kind": "yes/no",
  "text": "Tweet: According to my road rage, the word of the day is asshat",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q703e7255ee",
  "kind": "yes/no",
  "text": "Claim: Saulo Ribeiro's was trained in Portuguese Jiu-Jitsu by this person. The trainer was a student of the person who also taught Romero Cavalcanti and ran the Gracie Humaitá school in Rio de Janeiro.\n\nPassages:\n\n[Rolls Gracie]\nRolls Gracie ([ˈɡɾejsi] 1951–1982) was a Brazilian martial artist. He was teacher of Rickson Gracie, Carlos Gracie Jr., Royler Gracie, Márcio \"Macarrão\" Stambowsky, Rigan Machado and Romero \"Jacare\" Cavalcanti.\n\n[Saulo Ribeiro]\nAfter earning a black belt in Judo, he began his training of Brazilian Jiu-Jitsu in Rio de Janeiro under Royler Gracie, the son of Hélio Gracie, at the famous Gracie Humaitá.\n\n[Rodrigo Medeiros]\nHe received his black belt from Rolls Gracie student, Romero \"Jacaré\" Cavalcanti, he also trained under Fernando 'Magrao' Gurgel and is one of a select group of Jiu-Jitsu competitors to have won the prestigious World Jiu-Jitsu Championship openweight titles twice.\n\n[Royler Gracie]\nHe ran the Gracie Humaitá school in Rio de Janeiro, Brazil for many years under his father Helio's direction, but currently lives in San Diego.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q864fef4d18",
  "kind": "yes/no",
  "text": "Claim: The genus that includes Disporum viridescens has species in country that the 72nd meridian east runs through. There are two more species in that country than in Boltonia.\n\nPassages:\n\n[Disporum viridescens]\nDisporum viridescens is a species of flowering plant in the genus \"Disporum\".\n\n[72nd meridian east]\nThe meridian 72° east of Greenwich is a line of longitude that extends from the North Pole across the Arctic Ocean, Asia, the Indian Ocean, the Southern Ocean, and Antarctica to the South Pole.\n\n[Boltonia]\nBoltonia is a genus of plants in the sunflower family native primarily to North America with one species in eastern Asia.\n\n[Disporum]\nDisporum (commonly known as fairy bells) is a genus of about 20 species of perennial flowering plants, found in Asia from northern India to Japan, south to Indonesia and north into the Russian Far East.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa5a01add23",
  "kind": "yes/no",
  "text": "Claim: The logo of the American athletic shoe and clothing manufacturer who trademarked the slogan coined by Dan Wieden has made $26 billion in profit. Dan Wieden co-founded Wieden+Kennedy.\n\nPassages:\n\n[Swoosh]\nThe Swoosh is the logo of American athletic shoe and clothing manufacturer Nike, Inc. Today, it has become one of the most recognizable brand logos in the world, and the most profitable, having a worth of $26 billion alone.\n\n[Just Do It]\nJust Do It (stylized as JUST DO IT.) is a trademark of shoe company Nike, and one of the core components of Nike's brand.\n\n[Dan Wieden]\nDan Wieden (born 1945) Pronounced \"Why-den,\" is an American advertising executive who co-founded Wieden+Kennedy and coined the Nike tagline \"Just Do It.\"",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q028d1879a3",
  "kind": "yes/no",
  "text": "Claim: Henricus Antonius \"Han\" van Meegeren sold a flower painting to a military officer who was the recipient of Pour le Mérite.\n\nPassages:\n\n[Han van Meegeren]\nHenricus Antonius \"Han\" van Meegeren (] ; 10 October 1889 – 30 December 1947) was a Dutch painter and portraitist and is considered to be one of the most ingenious art forgers of the 20th century. Despite his life of crime, van Meegeren became a national hero after World War Two when it was revealed that he had sold a forged painting to Reichsmarschall Hermann Göring during the Nazi Occupation of the Netherlands.\n\n[Hermann Göring]\nHermann Wilhelm Göring (or Goering; ] ; 12 January 1893 – 15 October 1946) was a German political and military leader as well as one of the most powerful figures in the Nazi Party (NSDAP) that ruled Germany from 1933 to 1945. A veteran World War I fighter pilot ace, he was a recipient of the \"Pour le Mérite\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q91ed59fd18",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which version is written sarcastically?",
  "options": [
   "just found ive been walking on a broken foot for the past 6 months 🤪🤪🤪",
   "Just found out I've been walking on a broken foot for the past six months :( may have to get surgery again"
  ]
 },
 {
  "qid": "qe9c9923d8d",
  "kind": "yes/no",
  "text": "Claim: The Basset Bleu de Gascogne and the Beagle are breeds of small hound.\n\nPassages:\n\n[Beagle]\nThe Beagle is a breed of small hound, similar in appearance to the much larger foxhound.\n\n[Basset Bleu de Gascogne]\nThe Basset Bleu de Gascogne (] ), also known as the Blue Gascony Basset, is a long-backed, short legged breed of dog of the hound type.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4570e8dcae",
  "kind": "yes/no",
  "text": "Claim: Sord M5 spanned farther distances regarding sales than Interact Home Computer.\n\nPassages:\n\n[Interact Home Computer]\nMost were sold by the liquidator \"Protecto Enterprizes\" of Barrington, Illinois through mail order sales. The Interact Model One Home Computer debuted at the Consumer Electronics Show in Chicago in June 1978 at a price of $499. The majority of sales were thru Mail Order houses and you could buy it off the shelf at Highland Appliance in the Detroit, MI area and Newman Computer Exchange in Ann Arbor.\n\n[Sord M5]\nPrimarily the Sord M5 competed in the Japanese home computer market. It was also sold as the CGL M5 in the United Kingdom by Computer Games Limited, and was reasonably popular in Czechoslovakia, where the M5 stood as one of the first affordable computers available to the general public. Takara also sold models in Japan as the Game M5, and models were also exported to South Korea.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q823d225aa1",
  "kind": "yes/no",
  "text": "Claim: Norman Blake is older than the frontman of The Vines, that produced their album Wicked Nature.\n\nPassages:\n\n[Wicked Nature]\nThe release marks a few milestones for The Vines, with frontman Craig Nicholls taking on the role of producer for the first time, as well as introducing a completely new rhythm section with drummer Lachlan West and bassist Tim John.\n\n[Craig Nicholls]\nCraig Robert Nicholls (born 31 August 1977) is an Australian musician, best known as the lead singer, songwriter, and guitarist of the Australian alternative rock band The Vines, of which he is the only mainstay member.\n\n[Norman Blake (Scottish musician)]\nNorman Blake (born 20 October 1965, Bellshill, North Lanarkshire, Scotland) is a singer, instrumentalist and songwriter in the Glasgow based band Teenage Fanclub.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qbc9cbdd972",
  "kind": "yes/no",
  "text": "Claim: The founder of Legendary Entertainment produced a comedy movie directed by Lawrence Sher. The movie was based in Las Vegas..\n\nPassages:\n\n[The Hangover]\nThe Hangover is a 2009 American comedy film directed by Todd Phillips, co-produced with Daniel Goldberg, and written by Jon Lucas and Scott Moore. It tells the story of Phil Wenneck, Stu Price, Alan Garner, and Doug Billings, who travel to Las Vegas for a bachelor party to celebrate Doug's impending marriage.\n\n[Thomas Tull]\nThomas Tull (born 1970) is an American businessman and film producer.\n\n[Legendary Entertainment]\nThe company was founded by Thomas Tull in 2000 and in 2005, concluded an agreement to co-produce and co-finance films with Warner Bros., and began a similar arrangement with Universal Studios in 2014.\n\n[Lawrence Sher]\nLawrence Sher (born February 4, 1970) is an American cinematographer and film director, best known for comedy films such as \"Garden State\", \"The Hangover\" and \"The Dictator\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf9697f1f44",
  "kind": "yes/no",
  "text": "Claim: 3D Wayfinder is an indoor wayfinding tool and service used to help students to navigate large public buildings such as institutions which award academic degrees.\n\nPassages:\n\n[3D Wayfinder]\n3D Wayfinder is an indoor wayfinding software and service used to help visitors to navigate in large public buildings (shopping centers, airports, train stations, hospitals, universities etc.)\n\n[University]\nA university (Latin: \"universitas\" , \"a whole\") is an institution of higher (or tertiary) education and research which awards academic degrees in various academic disciplines.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q5972afcf50",
  "kind": "yes/no",
  "text": "Post: Is it unreasonable to spend £50 on a bonsai tree? Asking for a friend 🤔",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q76a8ca5677",
  "kind": "yes/no",
  "text": "Claim: The actress known for her role as Dr. Scott Peters in Rogues' Gallery (Gotham) also starred in the remake of the 1983 scifi miniseries created by Kenneth Johnson. Her nationality is Brazilian American.\n\nPassages:\n\n[V (2009 TV series)]\nA remake of the 1983 miniseries created by Kenneth Johnson, the new series chronicles the arrival on Earth of a technologically-advanced alien species which ostensibly comes in peace, but actually has sinister motives. \"V\" stars Elizabeth Mitchell and Morena Baccarin, and is executive produced by Scott Rosenbaum, Yves Simoneau, Scott Peters, Steve Pearlman, and Jace Hall.\n\n[Rogues' Gallery (Gotham)]\nIn this episode, Gordon (Ben McKenzie) is transferred to Arkham Asylum and tries to avoid a conflict when inmates riot with the help of Dr. Leslie Thompkins (Morena Baccarin).\n\n[Morena Baccarin]\nMorena Silva de Vaz Setta Baccarin (] ; born June 2, 1979) is a Brazilian American actress.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qccc965f292",
  "kind": "yes/no",
  "text": "Claim: MedStar Georgetown University Hospital and Providence Hospital are in the U.S. state District of Columbia.\n\nPassages:\n\n[MedStar Georgetown University Hospital]\nIt is a not-for-profit, acute care teaching and research facility located in the Georgetown neighborhood of the Northwest Quadrant of Washington, D.C.\n\n[Providence Hospital (Washington, D.C.)]\nProvidence Hospital is a 408 bed hospital located in the District of Columbia.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9505b85cb9",
  "kind": "yes/no",
  "text": "Claim: David Cutcliffe was the head coach of the Duke Blue Devils football team when they played at Wallace Wade Stadium and has won multiple college football coach of the year awards.\n\nPassages:\n\n[David Cutcliffe]\nHe also earned multiple college football coach of the year awards from the Walter Camp Football Foundation, the Maxwell Football Club, and the Bobby Dodd Foundation.\n\n[2013 Duke Blue Devils football team]\nThe team was led by head coach David Cutcliffe, in his sixth year, and played its home games at Wallace Wade Stadium in Durham, North Carolina.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8a676a6809",
  "kind": "yes/no",
  "text": "Claim: Thomas Ritter is a retired German footballer who played one game for Uruguay in 1993 against Uruguay, as a substitute for Stefan Effenberg, a retired German footballer who last managed SC Paderborn.\n\nPassages:\n\n[Stefan Effenberg]\nStefan Effenberg (] ; born 2 August 1968) is a retired German footballer who last managed SC Paderborn.\n\n[Thomas Ritter]\nThomas Ritter (born 10 October 1967 in Görlitz) is a retired German footballer. He played one game for Germany on 13 October 1993 in a friendly against Uruguay, as a substitute for Stefan Effenberg.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qb6198ecb03",
  "kind": "yes/no",
  "text": "Claim: Highway Companion is the third solo studio album by a singer-songwriter. He has been a member of more bands than the drummer who replaced Murray Dalglish in The Jesus and Mary Chain.\n\nPassages:\n\n[Highway Companion]\nHighway Companion is the third solo studio album by American singer-songwriter Tom Petty.\n\n[Bobby Gillespie]\nHe is the lead singer and founding member of the alternative rock band, Primal Scream. He was also the drummer for The Jesus and Mary Chain in the mid-1980s.\n\n[Tom Petty]\nHe is best known as the lead singer of Tom Petty and the Heartbreakers, but is also known as a member and co-founder of the late 1980s supergroup the Traveling Wilburys (under the pseudonyms of Charlie T. Wilbury Jr. and Muddy Wilbury), and his early band Mudcrutch.\n\n[Murray Dalglish]\nMurray Dalglish was the original drummer for The Jesus and Mary Chain from their formation in early 1984 until November 1984 when he was replaced by Bobby Gillespie.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q21a4cb5f6c",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Use the hashtag #wastedtime instead",
   "It really bugs me when teachers uncap and recap highlighters three or four times per book when marking - Poor time management! #efficiency"
  ]
 },
 {
  "qid": "qa874aec35f",
  "kind": "yes/no",
  "text": "Text: really honoured to have shared a coach today with a group of girls who didn’t know downing street was real and thought the prime minister and the queen lived together at buckingham palace",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qa7502ad872",
  "kind": "yes/no",
  "text": "Claim: National Artist of the USSR is the alternate translation for the honorary title of which Vladimir Basov and Inna Churikova were both 20th-century recipients.\n\nPassages:\n\n[People's Artist of the USSR]\nPeople's Artist of the USSR (Russian: Наро́дный арти́ст СССР , \"Narodný artist SSSR\"), also sometimes translated as National Artist of the USSR, was an honorary title granted to artists of the Soviet Union.\n\n[Walking the Streets of Moscow]\nThe film also features cameos by four People's Artists of the USSR: Rolan Bykov, Vladimir Basov, Lev Durov, and Inna Churikova.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q91502cd1f9",
  "kind": "yes/no",
  "text": "Claim: The place where glaciers in South America develop exclusively, is a mountain range that extends through multiple countries southeast of Jaigaon.\n\nPassages:\n\n[Andes]\nThe Andes or Andean Mountains (Spanish: \"Cordillera de los Andes\" ) are the longest continental mountain range in the world. The Andes extend from north to south through seven South American countries: Venezuela, Colombia, Ecuador, Peru, Bolivia, Argentina and Chile.\n\n[List of glaciers in South America]\nGlaciers in South America develop exclusively on the Andes and are subject to the Andes various climatic regimes namely the Tropical Andes, Dry Andes and the Wet Andes.\n\n[Auqui]\nAwki lies southeast of Jacabamba.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qd755df257b",
  "kind": "yes/no",
  "text": "Claim: Linzhou, Henan has a larger population than the town where the Liaoning Finance and Trade College is located.\n\nPassages:\n\n[Xingcheng]\nXingcheng (), former name Ningyuan (宁远), is a county-level city of southwest Liaoning province, China, with a population of approximately 140,000 urban inhabitants, and is located on the Liaodong Bay, i.e. the northern coast of the Bohai Sea.\n\n[Liaoning Finance and Trade College]\nLiaoning Finance and Trade College (), formerly known as Shenyang Shifan University Bohai College, is a small, partially walled private undergraduate college located on the Liaodong Bay of the Bohai coast in Xingcheng, southwest of Huludao in Liaoning province on the east coast of China.\n\n[Linzhou, Henan]\nIt covers an area of 2046 square kilometers and has a population of about one million.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb07bf42701",
  "kind": "yes/no",
  "text": "Claim: The character played by Rod Taylor in Darker than Amber (film) was a precursor to Stephanie Plum, a contemporary mystery protagonist, in a series that has been on multiple best seller lists.\n\nPassages:\n\n[Travis McGee]\nTravis McGee is a fictional character, created by American mystery writer John D. MacDonald. All 21 books have the theme of a color in the title, one of the earliest examples of detective/mystery fiction series to have a 'title theme' (e.g. the Sue Grafton 'alphabet' series; Janet Evanovich's 'number' series of Stephanie Plum books, etc.)\n\n[Janet Evanovich]\nShe began her career writing short contemporary romance novels under the pen name Steffie Hall, but gained fame authoring a series of contemporary mysteries featuring Stephanie Plum, a former lingerie buyer from Trenton, New Jersey, who becomes a bounty hunter to make ends meet after losing her job. The novels in this series have been on \"The New York Times\", USA Today, \"Wall Street Journal\" and Amazon bestseller lists.\n\n[Darker than Amber (film)]\nIt starred Rod Taylor as Travis McGee.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6f0ac380f7",
  "kind": "yes/no",
  "text": "Post: I'm going to miss #DesperateHousewives sooo much! So depressing that in 45 minutes it will be over forever 😭!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q660b652117",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Friendly reminder you’re not vegan if you swallow cum",
   "Cum is vegan"
  ]
 }
]
