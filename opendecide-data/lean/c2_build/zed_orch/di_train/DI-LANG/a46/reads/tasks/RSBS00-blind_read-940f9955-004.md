# A46 replay label-noise blind read RSBS00-blind_read-940f9955-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS00-blind_read-940f9955-004.json

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
  "qid": "q477b510753",
  "kind": "yes/no",
  "text": "Claim: Philadelphia, Here I come! is a 1964 play by Brian Patrick Friel, an Irish dramatist who has been likened to an Irish Checkhov.\n\nPassages:\n\n[Brian Friel]\nBrian Patrick Friel (9 January 1929 – 2 October 2015) was an Irish dramatist, short story writer and founder of the Field Day Theatre Company. He has been likened to an \"Irish Chekhov\" and described as \"the universally accented voice of Ireland\".\n\n[Philadelphia, Here I Come!]\nPhiladelphia, Here I Come!",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q47e7b5e061",
  "kind": "yes/no",
  "text": "Tweet: i love ingesting poison and then wondering why my tummy is rumbling the next morning",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q9cb9a5c3c1",
  "kind": "yes/no",
  "text": "Tweet: So now that it's not getting banned, should I download TikTok?",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qd7ceb5d3d1",
  "kind": "yes/no",
  "text": "Tweet: We get it ESPN. Sawx and Yanks. \n\nLet's go meteor.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qd6351b4c6f",
  "kind": "yes/no",
  "text": "Claim: 1969 saw the founding of the Canadian baseball team where the future manager played from 1973-87. He managed the Tampa Bay Devil Rays season.\n\nPassages:\n\n[Kansas City Royals]\nThe team was founded as an expansion franchise in 1969, and has participated in four World Series, winning in 1985 and 2015, and losing in 1980 and 2014.\n\n[2002 Tampa Bay Devil Rays season]\nTheir manager was Hal McRae who entered his 1st full season and last season with the Devil Rays.\n\n[Hal McRae]\nHarold Abraham McRae ( ; born July 10, 1945) is a former left fielder in Major League Baseball who played for the Cincinnati Reds (1968, 1970–72) and Kansas City Royals (1973–87).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q4a23a28613",
  "kind": "yes/no",
  "text": "Claim: The author of books about playwright Ugenia Lavender was also in a pop girl group that was formed in 1994.\n\nPassages:\n\n[Spice Girls]\nThe Spice Girls were an English pop girl group formed in 1994.\n\n[Ugenia Lavender]\nUgenia Lavender is the title character in a series of children's novels written by Geri Halliwell, who achieved fame as a member of the Spice Girls and as a solo singer-songwriter before deciding to pursue a career as an author.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6ec1881242",
  "kind": "yes/no",
  "text": "Claim: Pope John X gave the mother of the ruler of Rome who secured Pope Leo VII's papacy, the title \"patricia\" of Rome.\n\nPassages:\n\n[Alberic II of Spoleto]\nAlberic II (912–954) was ruler of Rome from 932 to 954, after deposing his mother Marozia and his stepfather, King Hugh of Italy.\n\n[Marozia]\nMarozia, born Maria and also known as Mariuccia or Mariozza ( 890 – 937), was a Roman noblewoman who was the alleged mistress of Pope Sergius III and was given the unprecedented titles \"senatrix\" (\"senatoress\") and \"patricia\" of Rome by Pope John X.\n\n[Pope Leo VII]\nLeo VII's election to the papacy was secured by Alberic II of Spoleto, the ruler of Rome at the time.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q6e33e043c1",
  "kind": "yes/no",
  "text": "Tweet: dont u just love when u get ready for a cancelled date two hours early . . . yeah i wasnt excited or anything",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qd8f7601e55",
  "kind": "yes/no",
  "text": "Claim: In the film, The Aristocats, Roddy Maude-Roxby played a character based on a story by a team including Tom Rowe as a writer.\n\nPassages:\n\n[Roddy Maude-Roxby]\nRoderick A. \"Roddy\" Maude-Roxby (born 2 April 1930 in London) is an English actor who has appeared in numerous films, such as Walt Disney's \"The Aristocats\", where he appeared as Edgar Balthazar; \"Unconditional Love\"; and Clint Eastwood's \"White Hunter Black Heart\", playing Thompson.\n\n[The Aristocats]\nThe 20th Disney animated feature film, the film is based on a story by Tom McGowan and Tom Rowe, and revolves around a family of aristocratic cats, and how an alley cat acquaintance helps them after a butler has kidnapped them to gain his mistress's fortune which was intended to go to them.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q0f0ef7ccca",
  "kind": "yes/no",
  "text": "Tweet: I want to join @IdenaNetwork to become a validator of the first Proof-Of-Person Blockchain #idenainvite",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qc6d466065a",
  "kind": "yes/no",
  "text": "Claim: Rhamnus purshiana is the name of one of the native species of buckthorn that is a powerful plant-based laxative and also has antibiotic properties.\n\nPassages:\n\n[Rhamnus purshiana]\nRhamnus purshiana (cascara buckthorn, cascara, bearberry, and in the Chinook Jargon, chittem and chitticum; syn. \"Frangula purshiana\", \"Rhamnus purshianus\") is a species of buckthorn native to western North America from southern British Columbia south to central California, and eastward to northwestern Montana.\n\n[Coffee cherry tea]\nIt is different from cascara sagrada tea, a powerful plant-based laxative.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q0e0ea85ea7",
  "kind": "yes/no",
  "text": "Claim: Penlee Point, the coastal headland to the SW of the village of Rame in a southeastern county in the nippon, lies at the entrance of the Plymouth Sound. This county is the location of the Doom Bar.\n\nPassages:\n\n[Penlee Point, Rame]\nPenlee Point (Cornish: Penn Legh , meaning \"stone-slab headland\") is a coastal headland to the southeast of the village of Rame in southeast Cornwall, UK. The point lies at the entrance to Plymouth Sound.\n\n[Cornwall]\nCornwall ( , ; Cornish: Kernow ] ) is a ceremonial county in the United Kingdom.\n\n[Doom Bar]\nThe Doom Bar (previously known as Dunbar sands, Dune-bar, and similar names) is a sandbar at the mouth of the estuary of the River Camel, where it meets the Celtic Sea on the north coast of Cornwall, England.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8f73d07415",
  "kind": "yes/no",
  "text": "Claim: The producer of the Eric Church album that features the song Cold One was a member of the band In Pursuit in the 1980's.\n\nPassages:\n\n[Cold One]\nIt is the third single from his fourth studio album, \"The Outsiders\".\n\n[The Outsiders (Eric Church album)]\nLike all of his previous albums, it is produced by Jay Joyce.\n\n[Jay Joyce]\nIn the 1980s, he was a member of the rock band In Pursuit, which recorded for MTM Records.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q1e5babadcb",
  "kind": "yes/no",
  "text": "Claim: The comic book series to which the episode \"Slicked-up Pup\" belongs was created in the year 1940.\n\nPassages:\n\n[Slicked-up Pup]\nSlicked-up Pup is a 1951 American one-reel animated cartoon and is the 60th \"Tom and Jerry\" cartoon directed by William Hanna and Joseph Barbera and produced by Fred Quimby.\n\n[Tom and Jerry]\nTom and Jerry is an American animated series of short films created in 1940, by William Hanna and Joseph Barbera.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q1f57a33e39",
  "kind": "yes/no",
  "text": "Claim: Seventeen is the name of the pop band that belongs on the South Korean music label that made Happy Pledis 2nd Album, and has 13 members.\n\nPassages:\n\n[Seventeen (band)]\nThe group consists of thirteen members who are separated into three sub-units, each with different areas of specialization: a 'Hip-Hop Unit', 'Vocal Unit', and 'Performance Unit'.\n\n[Happy Pledis 2nd Album]\nHappy Pledis 2nd Album is a charity single by the South Korean music label Pledis Entertainment's artists Son Dam-bi, Kahi, After School, NU'EST's JR and Baekho, Hello Venus's Yoo Ara and Lime and Pre-School Girl Park Jung-hyun.\n\n[Pledis Entertainment]\nPledis Entertainment () is a South Korean record label and entertainment agency founded in 2007 by Han Sung-soo. It is currently home to K-pop artists After School, Orange Caramel, NU'EST, Han Dong Geun, Kye Bumzu, Seventeen and Pristin.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9ad92cf05c",
  "kind": "yes/no",
  "text": "Claim: Gretchen Magers and her partner beat Patty Fendick and Agassi in the 1989 Great American Bank Classic – Doubles. Her partner and Kevin Ullyett are both former professional tennis players.\n\nPassages:\n\n[Robin White (tennis)]\nRobin White (born December 10, 1963) is a former professional tennis player from the United States.\n\n[1989 Great American Bank Classic – Doubles]\nPatty Fendick and Jill Hetherington were the defending champions but lost in the quarterfinals to Gretchen Magers and Robin White.\n\n[Kevin Ullyett]\nKevin Ullyett (born 23 May 1972 in Salisbury, now Harare) is a former professional tennis player from Zimbabwe.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qcce16dc055",
  "kind": "yes/no",
  "text": "Claim: The type of art the Consul and the opera, which is performed as part of a double bill with Busoni's \"Turandot\", have in common is music\n\nPassages:\n\n[The Consul]\nThe Consul is an opera in three acts with music and libretto by Gian Carlo Menotti, his first full-length opera.\n\n[Arlecchino (opera)]\nHe completed the music for the opera while living in Zurich in 1916.\n\n[Turandot (Busoni)]\nThe opera is often performed as part of a double bill with Busoni's earlier one-act opera \"Arlecchino\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q33a1c30b50",
  "kind": "yes/no",
  "text": "Post: Idk how some girls put on makeup everyday. Is it just to take selfies or have you just not discovered netflix yet?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q3298800397",
  "kind": "yes/no",
  "text": "Claim: Bruce Darnell a jury member for Deutschland sucht den Superstar was an American model and choreographer born in 1957.\n\nPassages:\n\n[Deutschland sucht den Superstar (season 9)]\nJury members Fernanda Brandao and Patrick Nuo left DSDS and were replaced by Bruce Darnell and Cascada's Natalie Horler.\n\n[Bruce Darnell]\nBruce Darnell (born July 19, 1957) is an American model and choreographer based in Germany.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4b7fe87951",
  "kind": "yes/no",
  "text": "Claim: The ex member of Jonny (band) and Teenage Fanclub is older than the frontman of The Vines. The latter produced their album Wicked Nature.\n\nPassages:\n\n[Craig Nicholls]\nCraig Robert Nicholls (born 31 August 1977) is an Australian musician, best known as the lead singer, songwriter, and guitarist of the Australian alternative rock band The Vines, of which he is the only mainstay member.\n\n[Jonny (band)]\nJonny is a two-person band formed by Norman Blake of Teenage Fanclub and Euros Childs of Gorky's Zygotic Mynci.\n\n[Wicked Nature]\nThe release marks a few milestones for The Vines, with frontman Craig Nicholls taking on the role of producer for the first time, as well as introducing a completely new rhythm section with drummer Lachlan West and bassist Tim John.\n\n[Norman Blake (Scottish musician)]\nNorman Blake (born 20 October 1965, Bellshill, North Lanarkshire, Scotland) is a singer, instrumentalist and songwriter in the Glasgow based band Teenage Fanclub.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1e6e2400f2",
  "kind": "yes/no",
  "text": "Tweet: ayo govvy hook me up w that stimmy if you know how the flow goes y feel",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q157b2a761a",
  "kind": "yes/no",
  "text": "Claim: Both the winner of the singles event in the 1980 Austrian Open and Andy Murray participate as a professional tennis player.\n\nPassages:\n\n[1980 Austrian Open (tennis)]\nFirst-seeded Guillermo Vilas won the men's singles title and the accompanying $13,000 first-prize money while Virginia Ruzici won the women's singles event.\n\n[Virginia Ruzici]\nVirginia Ruzici (born 31 January 1955) is a former professional tennis player from Romania.\n\n[Andy Murray]\nSir Andrew Barron Murray, {'1': \", '2': \", '3': \", '4': \"} (born 15 May 1987) is a British professional tennis player from Scotland currently ranked world no. 3 in men's singles.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q7e1bb16d50",
  "kind": "yes/no",
  "text": "Text: ive been watching british streamers for too long. i caught myself saying aircon instead of AC",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q51c503e8c0",
  "kind": "yes/no",
  "text": "Claim: Richie Furay was born before the former Blitz Kid later to be the frontman of Tony James' band. This band released the album and single Dress for Excess.\n\nPassages:\n\n[Dress for Excess]\nDress for Excess is the second album by British band Sigue Sigue Sputnik, released in 1988 (see 1988 in music).\n\n[Blitz Kids]\nAmong the many attendees were Rusty Egan, Steve Strange, Boy George, Marilyn, Alice Temple, Perri Lister, Princess Julia, Philip Sallon, Carl Teper and Martin Degville (later to be the frontman of Tony James' Sigue Sigue Sputnik).\n\n[Richie Furay]\nPaul Richard \"Richie\" Furay (born May 9, 1944) is an American singer, songwriter, and Rock & Roll Hall of Fame member who is best known for forming the bands Buffalo Springfield with Stephen Stills, Neil Young, Bruce Palmer, and Dewey Martin, and Poco with Jim Messina, Rusty Young, George Grantham and Randy Meisner.\n\n[Martin Degville]\nMartin Degville is (born 27 January 1961 in Walsall) is the lead singer and co-songwriter of the UK pop band, Sigue Sigue Sputnik – which had a worldwide hit single in 1986 with \"Love Missile F1-11\" – and six other EMI single releases.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb133d1fa15",
  "kind": "yes/no",
  "text": "Claim: The metafamily of graphical operating systems developed, marketed, and sold by Microsoft offers software for operatic singing training.\n\nPassages:\n\n[Microsoft Windows]\nMicrosoft Windows, or simply Windows, is a metafamily of graphical operating systems developed, marketed, and sold by Microsoft.\n\n[Winsingad]\nWinSingad is a Microsoft Windows based software for singing training.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4473014fb8",
  "kind": "yes/no",
  "text": "Claim: The 1988 Nirvana album that their cover song Sliver was rereleased on featured many artists. The list of artists includes The Vaselines, Dave Grohl, and Chad Channing.\n\nPassages:\n\n[Sliver (song)]\nDGC re-released the song to radio to support the release of the rarities compilation album \"Incesticide\" in 1992.\n\n[Son of a Gun (EP)]\nSon of A Gun is the debut extended play single by Glasgow alternative rock group The Vaselines. The title-song of this EP came to a wider audience after Nirvana covered it, along with \"Molly's Lips\", on their compilation album \"Incesticide\".\n\n[Incesticide]\nIncesticide is a compilation album by the American grunge band Nirvana. At the time, the majority of the material on \"Incesticide\" was circulating within fan communities (albeit in lower quality). Since the songs were recorded in different sessions and some were recorded when Nirvana did not have a stable formation, the album includes recordings by four different drummers: Chad Channing, Dan Peters, Dale Crover, and Dave Grohl.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q1f79cfaf16",
  "kind": "yes/no",
  "text": "Claim: Ximena Navarrete was the winner of the 1959 Miss Universe pageant in which La Toya Woods competed.\n\nPassages:\n\n[La Toya Woods]\nLa Toya Woods (born 1985) is the winner of the Miss Trinidad & Tobago Universe 2010 pageant and was a contestant in the Miss Universe 2010 pageant in Las Vegas, USA.\n\n[Miss Universe 2010]\nXimena Navarrete of Mexico was crowned by Stefanía Fernández of Venezuela as her successor at the end of the event.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q03fe576d93",
  "kind": "yes/no",
  "text": "Tweet: Well done to the guy who was charging down the stairs at Ealing Broadway and sent me flying, you made me cry.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q52a8eba0ca",
  "kind": "yes/no",
  "text": "Claim: The Casey Jr. is a water play area across from Dumbo the Flying Elephant, an aerial carousel-style ride located in Fantasyland at six Disney parks around the world.\n\nPassages:\n\n[Casey Jr. Splash 'n' Soak Station]\nThis attraction is a water play area across from the Dumbo the Flying Elephant ride and The Barnstormer starring the Great Goofini.\n\n[Dumbo the Flying Elephant]\nDumbo the Flying Elephant is an aerial carousel-style ride located in Fantasyland at six Disney parks around the world.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf2b7eab7fb",
  "kind": "yes/no",
  "text": "Post: Can’t wait to get home take a big ass antihistamine and roll in some topical steroids.\n\nDamn it, skin! What did I ever do to you?!?!",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q6d338bac3f",
  "kind": "yes/no",
  "text": "Post: YouTube just gave me a gamer targeted covid vaccine ad and anyway get vaccinated gamers.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qf3f4c91ee5",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "My favorite part about running on the track is seeing how high my heart rate gets just walking up the stairs to it.",
   "My heart rate spiked when I walk up the stairs to the track"
  ]
 },
 {
  "qid": "qe295fb1e50",
  "kind": "yes/no",
  "text": "Claim: Jordan's Furniture is a furniture retailer with a location in an enclosed shopping mall on the north side of Interstate 295 near the junction with Interstate 40.\n\nPassages:\n\n[Jordan's Furniture]\nJordan's Furniture is a furniture retailer in New England. There are currently seven locations - in Reading, Avon, Taunton, Natick, Massachusetts, Nashua, New Hampshire, Warwick Mall in Warwick, Rhode Island, and New Haven, Connecticut.\n\n[Warwick Mall]\nWarwick Mall is an enclosed shopping mall in Warwick, Rhode Island, on the north side of Interstate 295 near the junction with Interstate 95.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qf36af291f2",
  "kind": "yes/no",
  "text": "Post: I would like to dedicate my hot girl summer to the Eastpointe Chick-Fil-A. Thank you!",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qc2ad0eae1f",
  "kind": "yes/no",
  "text": "Claim: This equatorial island is known for Breacachadh which is also known as Breachacha Castle. It is also home to Dùn Dubh.\n\nPassages:\n\n[Coll]\nColl is known for its sandy beaches, which rise to form large sand dunes, for its corncrakes, and for Breacachadh Castle.\n\n[Breachacha Castle]\nBreachacha Castle (also spelled Breacachadh) is either of two structures on the shore of Loch Breachacha, on the Inner Hebridean island of Coll, Scotland.\n\n[Dùn Dubh]\nDùn Dubh is a hillfort, located on the Inner Hebridean island of Coll.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q0722697c15",
  "kind": "yes/no",
  "text": "Claim: Russia Soviet pianist, composer and teacher, Tatiana Nikolayeva taught Russian pianist and music educator Maria Szraiber.\n\nPassages:\n\n[Tatiana Nikolayeva]\nTatyana Petrovna Nikolayeva (Russian: Татья́на Петро́вна Никола́ева , \"Tat'jana Petrovna Nikolaeva\"; May 4, 1924November 22, 1993) was a Russian Soviet pianist, composer and teacher.\n\n[Maria Szraiber]\nMaria Szraiber is a Polish pianist and music educator.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qc18b4f027b",
  "kind": "yes/no",
  "text": "Claim: \"Hot Lead and Cold Feet\" was released two years before the film in which Josh Flitter played \"Eddie\".\n\nPassages:\n\n[Josh Flitter]\nHe is known for playing Corky in \"Nancy Drew\", Eddie in \"The Greatest Game Ever Played\", and voiced Rudy Kangaroo in the 2008 animated film \"Horton Hears a Who!\n\n[The Greatest Game Ever Played]\nThe Greatest Game Ever Played is a 2005 biographical sports film based on the early life of golf champion Francis Ouimet.\n\n[Hot Lead and Cold Feet]\nHot Lead and Cold Feet (originally titled Welcome to Bloodshy) is a 1978 American comedy-western film produced by Walt Disney Productions and starring Jim Dale, Karen Valentine, Don Knotts, Jack Elam and Darren McGavin.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2e682f4a02",
  "kind": "yes/no",
  "text": "Claim: Director Kevin Smith co-founded View Askew Productions and produced numerous movies starring a principle actor in \"Kissing A Fool\".\n\nPassages:\n\n[Kevin Smith]\nWhile not strictly sequential, the films frequently featured crossover plot elements, character references, and a shared canon described by fans as the \"View Askewniverse\", named after his production company View Askew Productions, which he co-founded with Scott Mosier.\n\n[Kissing a Fool]\nIt primarily stars David Schwimmer, Jason Lee, Mili Avital, Kari Wührer and Vanessa Angel.\n\n[Jason Lee (actor)]\nHe is also known for his roles in Kevin Smith films such as \"Mallrats\", \"Chasing Amy\", \"Dogma\", \"Jay and Silent Bob Strike Back\", \"Jersey Girl\", \"Clerks II\" and \"Cop Out\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q5a6e80ab99",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Every time you complain about neopronouns or xenogenders we add five more",
   "Stop complaining about peoples individual gender experiences"
  ]
 },
 {
  "qid": "qb3e9ceb03f",
  "kind": "yes/no",
  "text": "Claim: Steven Harvey Goldmann directed a 2006 film that starred an American actress who appeared in Twins and Jerry Maguire. She is married to Kelly Preston.\n\nPassages:\n\n[Broken Bridges]\nBroken Bridges is a 2006 film starring Toby Keith, Lindsey Haun, Burt Reynolds and Kelly Preston.\n\n[Kelly Preston]\nKelly Preston (born October 13, 1962) is an American actress and former model. She has appeared in more than sixty television and film productions, most notably including \"Mischief\", \"Twins\" and \"Jerry Maguire\". She is married to John Travolta, with whom she collaborated on the fantasy film \"Battlefield Earth\".\n\n[Steven Goldmann]\nGoldmann also directed the movies \"Broken Bridges\" and \"Trailer Park of Terror\", and additionally directed several television programs.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf0ceab3e52",
  "kind": "yes/no",
  "text": "Claim: The birthplace of Wu Jiaduo and Gongqingcheng are both county-level cities that are located in China.\n\nPassages:\n\n[Gongqingcheng]\nGongqingcheng () is a county-level city in northern Jiangxi province, People's Republic of China, established on 10 September 2010.\n\n[Wu Jiaduo]\nWu Jiaduo (; born 19 September 1977 in Linhai, Zhejiang, China) is a female Chinese-born German table tennis player.\n\n[Linhai]\nLinhai (; Tai-chow dialect: Ling-he) is a county-level city in Taizhou, Zhejiang Province situated on the banks of the Lin River in Eastern China.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q53deb5525c",
  "kind": "yes/no",
  "text": "Claim: The 1990 European Cup Final was a football match between Sparta Rotterdam of Italy and Benfica of Portugal, played on 23 May 1990, The winning goal came in the 68th minute for Sparta Rotterdam when Alessandro Costacurta passed the ball to Marco van Basten, who slotted it to Frank Rijkaard, who ran through the defense and scored, Franklin Edmundo \"Frank\" Rijkaard, is a Dutch former footballer and former manager who played as a midfielder or defender.\n\nPassages:\n\n[Frank Rijkaard]\nFranklin Edmundo \"Frank\" Rijkaard (] ; born 30 September 1962) is a Dutch former footballer and former manager who played as a midfielder or defender.\n\n[1990 European Cup Final]\nThe 1990 European Cup Final was a football match between Milan of Italy and Benfica of Portugal, played on 23 May 1990 at the Praterstadion in Vienna, Austria.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q333803a8cb",
  "kind": "yes/no",
  "text": "Claim: The actress that plays Sarah Hurst in \"Easy Virtue\" stars with Dervla Kirwan in a November 2012 supernatural thriller film written by Steve Stone.\n\nPassages:\n\n[Entity (2012 film)]\nEntity is a 2012 British supernatural thriller film written and directed by Steve Stone. It stars Dervla Kirwan, Charlotte Riley, and Branko Tomovic and centers upon a British reality show film crew that encounters a dark entity.\n\n[Charlotte Riley]\nShe is known for her roles as Sarah Hurst in \"Easy Virtue\" and as Catherine Earnshaw in ITV's adaptation of \"Wuthering Heights\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q97b78a7174",
  "kind": "yes/no",
  "text": "Claim: Horror movie R-Point, set in 1972 Vietnam, was not filmed partially in a location about 3 miles south-west of Povokvil Waterfalls.\n\nPassages:\n\n[Bokor Hill Station]\nIt was used as the location for the final showdown of the movie \"City of Ghosts\" (2002) and the 2004 film \"R-Point\".\n\n[Povokvil Waterfalls]\nIt is located about 3 mi north-east of Bokor Hill Station.\n\n[R-Point]\nSet in 1972 Vietnam, during the Vietnam War, it stars Kam Woo-sung and Son Byong-ho as members of the South Korean military in Vietnam.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe9f8b735b7",
  "kind": "yes/no",
  "text": "Claim: The Talbot-Taylor Wildlife Sanctuary is located in the town which the Hollis/Brookline High School services.\n\nPassages:\n\n[Hollis/Brookline High School]\nHollis/Brookline High School is a public school located in Hollis, New Hampshire, serving the towns of Hollis and Brookline.\n\n[Brookline, New Hampshire]\nBrookline is a town in Hillsborough County, New Hampshire, United States. Brookline is home to the Talbot-Taylor Wildlife Sanctuary, Potanipo Pond, and the Brookline Covered Bridge.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qe3bfaa30c1",
  "kind": "yes/no",
  "text": "Claim: Rosey Grier attended Boston College. He went on to play the role of Gabe Cooper in the TV Series that Darby Hinton portrayed Israel Boone in.\n\nPassages:\n\n[Darby Hinton]\nFrom 1964–1970, he portrayed Israel Boone, a son of American pioneer Daniel Boone, on the NBC adventure series \"Daniel Boone\", with Fess Parker in the title role.\n\n[Rosey Grier]\nHe was a notable college football player for The Pennsylvania State University who earned a retrospective place in the National Collegiate Athletic Association 100th anniversary list of 100 most influential student athletes.\n\n[Daniel Boone (1964 TV series)]\nActor and former NFL football player Rosey Grier made regular appearances as Gabe Cooper in the 1969 to 1970 season.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q6833e1c6a3",
  "kind": "yes/no",
  "text": "Claim: September 8, 2010 is the year exact date that the Linkin Park album with the song \"Wretches and Kings\"was released.\n\nPassages:\n\n[Wretches and Kings]\nIt is the tenth track from their 2010 album, \"A Thousand Suns\".\n\n[A Thousand Suns]\nIt was released on September 8, 2010, by Warner Bros.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q94c6a9ec8f",
  "kind": "yes/no",
  "text": "Claim: Ekaterina Gordeeva is the Polish figure skater who danced with a Polish pair skater and in 1988 and 1994.\n\nPassages:\n\n[Sergei Grinkov]\nTogether with partner and wife Ekaterina Gordeeva, he was the 1988 and 1994 Olympic Champion and a four-time World Champion.\n\n[Ekaterina Gordeeva]\nTogether with her partner and husband, the late Sergei Grinkov, she was the 1988 and 1994 Olympic Champion and four-time World Champion in pair skating.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q06aaf2cd99",
  "kind": "yes/no",
  "text": "Text: as much as i love ginny and Georgia i hate that once again a girl only learns to masturbate bc some creep dude said to. I hate cliches",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qb6671c3df5",
  "kind": "yes/no",
  "text": "Claim: A city to the south of Qinglong Manchu Autonomous County is a Communists city. The area Qing Yan Garden is located is also a Communists city.\n\nPassages:\n\n[Qinglong Manchu Autonomous County]\nBordering county-level divisions are: Lingyuan and Jianchang County (Liaoning) to the north, Liaoning's Suizhong County and Qinhuangdao city proper to the east, Qian'an and Lulong County to the south, and Kuancheng Manchu Autonomous County and Qianxi County to the west.\n\n[Huai'an]\nHuai'an (), formerly called Huaiyin () until 2001, is a prefecture-level city in central Jiangsu province of Eastern China.\n\n[Qing Yan Garden]\nQing Yan Garden () is located in Huai'an City, Jiangsu Province, China.\n\n[Qian'an, Hebei]\nQian'an () is a city in the northeastern part of Hebei province in North China.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 }
]
