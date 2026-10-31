# A46 replay label-noise blind read RSBS08-blind_read-13b5b8df-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS08-blind_read-13b5b8df-004.json

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
  "qid": "qe552bd5287",
  "kind": "yes/no",
  "text": "Text: Is there a zombie apocalypse going on upper street",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q2c895cb2a2",
  "kind": "yes/no",
  "text": "Claim: The Global Food Security Act of 2016, is a law introduced on March 24, 2015 in the 114th Congress by Robert Patrick \"Bob\" Casey Jr. Senator of Pennsylvania, who is an Republican attorney and politician, currently the senior United States Senator from Pennsylvania.\n\nPassages:\n\n[Bob Casey Jr.]\nRobert Patrick Casey Jr. (born April 13, 1960) is an American attorney and politician, currently the senior United States Senator from Pennsylvania.\n\n[Global Food Security Act of 2016]\n114–195 ), is a law introduced on March 24, 2015 in the 114th Congress by Representative Christopher Henry \"Chris\" Smith (New Jersey-R) and on May 7, 2015 by Senator Robert Patrick \"Bob\" Casey Jr. (Pennsylvania-D), and signed by President Barack Obama on July 20, 2016.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6ac9d44f37",
  "kind": "yes/no",
  "text": "Claim: Björn Ulvaeus was a part of a phenomenal Swedish pop group, formed in Stockholm in 1972, as well as co-producer on the film \"Mamma Mia!\" with Benny Anderson.\n\nPassages:\n\n[Björn Ulvaeus]\nBjörn Kristian Ulvaeus (] ) (born 25 April 1945; credited as Björn Ulvæus) is a Swedish songwriter, producer, a former member of the Swedish musical group ABBA (1972–1982), and co-composer of the musicals \"Chess\", \"Kristina från Duvemåla\", and \"Mamma Mia! He co-produced the film \"Mamma Mia!\" with fellow ABBA member and close friend Benny Andersson.\n\n[ABBA]\nABBA (] ) were a Swedish pop group, formed in Stockholm in 1972 by members Agnetha Fältskog, Björn Ulvaeus, Benny Andersson, and Anni-Frid Lyngstad.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q90599bc050",
  "kind": "yes/no",
  "text": "Claim: Sherwood Stewart was born before the winner of the 1993 Movistar Open singles competition.\n\nPassages:\n\n[1993 Movistar Open – Singles]\nJavier Frana defeated Emilio Sánchez 7–5, 3–6, 6–3 to win the 1993 Movistar Open singles competition.\n\n[Sherwood Stewart]\nSherwood Stewart (born June 6, 1946, in Goose Creek, Texas, United States) played amateur and professional tennis in the 1970s and 1980s.\n\n[Javier Frana]\nJavier Alberto Frana (born 25 December 1966) is a former tennis player from Argentina and current tennis commentator for ESPN Latin America.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q185d6c814f",
  "kind": "yes/no",
  "text": "Claim: John Updike and Tom Clancy both publish more than 15 bestselling novels.\n\nPassages:\n\n[Tom Clancy]\nSeventeen of his novels were bestsellers, and more than 100 million copies of his books are in print.\n\n[John Updike]\nOne of only three writers to win the Pulitzer Prize for Fiction more than once (the others were Booth Tarkington and William Faulkner), Updike published more than twenty novels, more than a dozen short-story collections, as well as poetry, art and literary criticism and children's books during his career.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qeee8ec10ad",
  "kind": "yes/no",
  "text": "Claim: The Delamere Way is a footpath running from Chester to Stockton Heath, a civil parish and suburb of Warrington, Cheshire in England.\n\nPassages:\n\n[Stockton Heath]\nStockton Heath is a civil parish and suburb of Warrington, Cheshire, England.\n\n[Delamere Way]\nThe Delamere Way is a footpath running from Frodsham to Stockton Heath within the English county of Cheshire.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc331ddc530",
  "kind": "yes/no",
  "text": "Claim: Pari Lake flows down to this gigantic lake. Sniardwy is farther north than that gigantic lake.\n\nPassages:\n\n[Pari Lake]\nThe western face of the lake is open and its water flows down to the gigantic Kundol Lake which is situated in the foothills.\n\n[Śniardwy]\nŚniardwy (German: ) is a lake in the Masurian Lake District of the Warmian-Masurian Voivodeship, Poland.\n\n[Kundol Lake]\nKundol Lake also known as \"Kundol Dand\", is a lake in Swat Valley, Khyber Pakhtunkhwa, Pakistan, which is located in the north of Utror valley at a distance of 19 km away from kalam.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q0b23b8c202",
  "kind": "yes/no",
  "text": "Claim: The co-organiser of \" White Wonderland\" is part of a partnership with a club founded by an investor of American-American heritage.\n\nPassages:\n\n[Insomniac Events]\nInsomniac is involved in the operation of three Los Angeles nightclubs—Create (in partnership with SBE, built on the site of the former Vanguard Hollywood), Exchange L.A. and the underground warehouse Factory 93, located at 1756 Naud Street.\n\n[Sam Nazarian]\nSam Nazarian (born 1975) is an Iranian-American businessman, investor and philanthropist.\n\n[White Wonderland]\nWhite Wonderland is an electronic music festival co-organized by Insomniac Events and fellow club promoter Giant.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd83eabee7d",
  "kind": "yes/no",
  "text": "Claim: The band Steve Goulding is the drummer for is not British. The singer whose debut album is Don't Let It Go to Waste isn't British either.\n\nPassages:\n\n[Don't Let It Go to Waste]\nDon't Let It Go to Waste is the debut album from Matt Willis, released on 20 November 2006.\n\n[The Mekons]\nThe Mekons are a British-American rock band.\n\n[Steve Goulding]\nSteve Goulding (born 1954, South London, England) is an English drummer, who has played as a member of Graham Parker and The Rumour, The Associates, Poi Dog Pondering, The Waco Brothers and The Mekons.\n\n[Matt Willis]\nMathew James \"Matt\" Willis (born 8 May 1983), also previously known as Mattie Jay, is an English singer-songwriter, television presenter and actor, best known as the bassist and one of the vocalists of the pop punk band, Busted.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q46810a9f80",
  "kind": "yes/no",
  "text": "Claim: Shakespearean heroine Rosalind was played by Bryce Dallas Howard in the 2006 film directed by Kenneth Branagh.\n\nPassages:\n\n[As You Like It (2006 film)]\nAs You Like It is a 2006 film written and directed by Kenneth Branagh, and based on the Shakespearean play of the same name. It stars Bryce Dallas Howard as Rosalind, David Oyelowo as Orlando De Boys, Romola Garai as Celia, Adrian Lester as Oliver De Boys, Alfred Molina as Touchstone, Kevin Kline as Jaques, Janet McTeer as Audrey, and Brian Blessed as Duke Frederick and his brother Duke Senior.\n\n[Rosalind (As You Like It)]\nRosalind is the heroine and protagonist of the play \"As You Like It\" (1600) by William Shakespeare.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qab6083a91f",
  "kind": "yes/no",
  "text": "Claim: Kevin Bookout played college basketball very well in the Big 12 Conference.\n\nPassages:\n\n[Oklahoma Sooners men's basketball]\nThe Sooners play in the Big 12 Conference.\n\n[Kevin Bookout]\nBorn in Stroud, Oklahoma, he played collegiately with the University of Oklahoma Sooners.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qdcbdcbca9d",
  "kind": "yes/no",
  "text": "Claim: Kool Keith, a Mambo artist typical of Afro-Surrealism, was born October 7, 1963.\n\nPassages:\n\n[Afro-Surrealism]\nNotable practitioners of Afro-Surrealism include Bob Kaufman, Krista Franklin, Kool Keith, Samuel R. Delany, Roman Bearden and Deana Lawson.\n\n[Kool Keith]\nKeith Thornton (born October 7, 1963), better known by his stage name Kool Keith, is an American rapper from The Bronx, New York known for his surreal, abstract and often profane or incomprehensible lyrics.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q2de51ee5b5",
  "kind": "yes/no",
  "text": "Claim: X Factor winner Leona Lewis has worked with a co-writer of the song Do It Well.\n\nPassages:\n\n[Ryan Tedder]\nAs well as being the lead vocalist for the pop rock band OneRepublic, he has an independent career as a songwriter and producer for various artists, including Madonna, U2, Adele, Beyoncé, Maroon 5, Demi Lovato, Ariana Grande, Kelly Clarkson, Jennifer Lopez, Westlife, Ed Sheeran, One Direction, Big Time Rush, Camila Cabello, Taylor Swift, Leona Lewis, Zedd and MØ.\n\n[Leona Lewis]\nLewis achieved national recognition when she won the third series of \"The X Factor\" in 2006, winning a £1 million recording contract with Simon Cowell's record label, Syco Music.\n\n[Do It Well]\nIt was written by Ryan Tedder, Leonard Caston, Anita Poree, and Frank Wilson.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qb341806434",
  "kind": "yes/no",
  "text": "Claim: A Russian linguist, was a member of the Kazan School. This Russian linguist was published by the Junior Hockey League. This publisher was founded by Ladislav Matejka.\n\nPassages:\n\n[Kazan school]\nKazan School was an influential group of linguists in Kazan. The linguistic circle included the Polish linguist Jan Baudouin de Courtenay and his student Nikolai Trubetzkoy.\n\n[Ladislav Matejka]\nIn 1962, he founded Michigan Slavic Publications, a series that has published more than 100 volumes by authors such as Roman Jakobson and Nikolai Trubetzkoy.\n\n[Nikolai Trubetzkoy]\nPrince Nikolai Sergeyevich Trubetzkoy (also Troubetskoy; Russian: Никола́й Серге́евич Трубецко́й; Moscow, April 16, 1890 – Vienna, June 25, 1938) was a Russian linguist and historian whose teachings formed a nucleus of the Prague School of structural linguistics.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q166ff5f008",
  "kind": "yes/no",
  "text": "Claim: Jang Do-yoon is mainly known for being a possible member of the pop band that belongs on the Japanese music label that made Happy Pledis 2nd Album. This pop band has 13 members.\n\nPassages:\n\n[Jang Do-yoon]\nHe is mainly known for being a possible member of the popular boy group Seventeen.\n\n[Pledis Entertainment]\nPledis Entertainment () is a South Korean record label and entertainment agency founded in 2007 by Han Sung-soo. It is currently home to K-pop artists After School, Orange Caramel, NU'EST, Han Dong Geun, Kye Bumzu, Seventeen and Pristin.\n\n[Seventeen (band)]\nThe group consists of thirteen members who are separated into three sub-units, each with different areas of specialization: a 'Hip-Hop Unit', 'Vocal Unit', and 'Performance Unit'.\n\n[Happy Pledis 2nd Album]\nHappy Pledis 2nd Album is a charity single by the South Korean music label Pledis Entertainment's artists Son Dam-bi, Kahi, After School, NU'EST's JR and Baekho, Hello Venus's Yoo Ara and Lime and Pre-School Girl Park Jung-hyun.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5d2dbee034",
  "kind": "yes/no",
  "text": "Claim: Crystal Palace F.C. doesn't present the award Player of the Year, first won by John McCormick and most recently by Wilfried Zaha.\n\nPassages:\n\n[Wilfried Zaha]\nDazet Wilfried Armel Zaha (born 10 November 1992) is a professional footballer who plays as a winger for Premier League club Crystal Palace and the Ivory Coast national team.\n\n[Crystal Palace F.C. Player of the Year]\nThe Crystal Palace Football Club Player of the Year is awarded at the end of each season. Since the inaugural award was made to John McCormick in 1972, 34 different players have won the award. Nine of these players have won the award for a second time, the most recent being Wilfried Zaha.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q88861f9c98",
  "kind": "yes/no",
  "text": "Claim: The nationality of the 38 year old professional footballer who was sold to Chelsea during the 2004–05 Olympique de Marseille season is Ivorian.\n\nPassages:\n\n[Didier Drogba]\nDidier Yves Drogba Tébily (] ; born 11 March 1978) is an Ivorian professional footballer who plays as a striker for American club Phoenix Rising FC.\n\n[2004–05 Olympique de Marseille season]\nWith striker Didier Drogba being sold to Chelsea, and replacements Habib Bamogo and Péguy Luyindula not performing at a similar level, the goal-scoring went dry, but in spite of scoring two points less than the previous season, l'OM finished two positions above the previous season.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3770c8e08f",
  "kind": "yes/no",
  "text": "Claim: Zhangye and Nan'an, Fujian are both located in the People's Republic of China.\n\nPassages:\n\n[Nan'an, Fujian]\nNan'an () is a county-level city of southern Fujian province, People's Republic of China.\n\n[Zhangye]\nZhangye, formerly romanized as Changyeh or known as Kanchow, is a prefecture-level city in central Gansu Province in the People's Republic of China.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q981513902b",
  "kind": "yes/no",
  "text": "Claim: American singer-songwriter Roy Orbison, known as \"the Caruso of Rock\", recorded on the Monument Records label and had hits such as \"Pretty One,\" and \"Uptown\".\n\nPassages:\n\n[Roy Orbison]\nRoy Kelton Orbison (April 23, 1936 – December 6, 1988) was an American singer-songwriter known for his distinctive, impassioned voice, complex song structures, and dark emotional ballads.\n\n[Early Orbison]\nEarly Orbison is an album recorded by Roy Orbison on the Monument Records label at their studios in Hendersonville, Tennessee and released in 1964. Essentially a compilation of songs from his first two Monument albums, it is most noteworthy for containing \"Pretty One\", the \"B\" side of Orbison's second Monument single, \"Uptown\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc64736b449",
  "kind": "yes/no",
  "text": "Claim: TEC-1 is not single-board kit computers. A company produced software for the computer that was also not single-board kit computers. This company developed the fiction role-playing games Silicon Dreams.\n\nPassages:\n\n[Level 9 Computing]\nFounded by Mike, Nicholas and Pete Austin, the company produced software for the BBC Micro, Nascom, ZX Spectrum, Commodore 64, Oric, Atari, Lynx 48k, RML 380Z, Amstrad CPC, MSX, Amiga, Apple II, Memotech MTX, and Enterprise platforms and is best known for its successful text adventure games until a general decline in the text adventure market forced their closure in June 1991.\n\n[TEC-1]\nThe TEC-1 is a single-board kit computer first produced by the Australian hobbyist electronics magazine Talking Electronics in the early 1980s.\n\n[Silicon Dreams]\nSilicon Dreams is a trilogy of interactive fiction games developed by Level 9 Computing during the 1980s.\n\n[Memotech MTX]\nThe Memotech MTX500, MTX512 and RS128 were a series of Zilog Z80A processor-based home computers released by Memotech in 1983 and 1984.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3b9135fc68",
  "kind": "yes/no",
  "text": "Claim: The unelected leader of the Network Italy faction within Popular Alternative is Roberto Formigioni.\n\nPassages:\n\n[Network Italy]\nMost of its members, including its long-time leader Roberto Formigoni, are members of the Catholic lay movement Communion and Liberation (CL).\n\n[Popular Alternative]\nPopular Alternative (Italian: \"Alternativa Popolare\" , AP) is a centre-right and mainly Christian-democratic political party in Italy, founded on 18 March 2017, after the dissolution of New Centre-Right (NCD).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qf861465336",
  "kind": "yes/no",
  "text": "Claim: In 1941 the historic diner in Albany, New York built, which also was a filming location for major portions of the Babenco 1987 film worked on by Lauro Escorel.\n\nPassages:\n\n[Lauro Escorel]\nIronweed\" (1987), another Babenco's film, would make him more known internationally.\n\n[Ironweed (film)]\nMajor portions of the film were shot on location in Albany, New York, including Jay Street at Lark Street, Albany Rural Cemetery and the Miss Albany Diner on North Broadway.\n\n[Miss Albany Diner]\nMiss Albany Diner (formerly known as Lil's Diner) is a historic diner in Albany, New York, built in 1941 and located at 893 Broadway, one of the oldest streets in Albany.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q4bc92b1ea1",
  "kind": "yes/no",
  "text": "Claim: Wolf Parade is a Canadian indie label and not Social Distortion.\n\nPassages:\n\n[Wolf Parade]\nWolf Parade is an indie rock band formed in 2003 in Montreal, Quebec of musicians from British Columbia.\n\n[Social Distortion]\nSocial Distortion is an American punk rock band formed in 1978 in Fullerton, California.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q932e811435",
  "kind": "yes/no",
  "text": "Claim: The singer is 6 months younger than the singer who had left their band, when it recorded Information (Berlin album). She sang vocals on the album Candyland.\n\nPassages:\n\n[Sonya Scarlet]\nSonya Scarlet (born 2 April 1980) is the singer and lyricist of the Italian extreme gothic metal band Theatres des Vampires.\n\n[Candyland (album)]\nIt is noticeably more guitar-driven than the band's previous releases with Sonya Scarlet on vocals, and its lyrics focus less on the vampiric and occult themes the band is famous for.\n\n[Information (Berlin album)]\nIt was recorded during the period when Terri Nunn had temporarily left the band to pursue an acting career and Virginia Macolino performed the lead vocals.\n\n[Terri Nunn]\nTerri Kathleen Nunn (born June 26, 1961), is an American singer and actress.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7bb7217715",
  "kind": "yes/no",
  "text": "Claim: Madrugada's final concert became popular one year after the band vocalist Kujibiki Unbalance, who is a member of MonstrO (band), sang with.\n\nPassages:\n\n[MonstrO (band)]\nMonstrO is an alternative band composed of former Still Rain, Danzig and Bloodsimple drummer Bevan Davies, former Bloodsimple, Medication and Skrew bassist Kyle Sanders, former Torche guitarist Juan Montoya and guitarist and vocalist Charlie Suarez formerly of Sunday Driver.\n\n[Madrugada (band)]\nOn 21 January 2008, the band released \"Madrugada\" and announced that they would split after one last tour. They performed their final concert on 15 November 2008.\n\n[Sunday Driver (band)]\nIn 2009 they became popular within the UK Steampunk scene.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qff63361478",
  "kind": "yes/no",
  "text": "Claim: The founder of the Westboro Baptist Church died of liver failure in 2014.\n\nPassages:\n\n[The Most Hated Family in America]\nThe Most Hated Family in America is a 2007 BBC documentary film written and presented by Louis Theroux about the family at the core of the Westboro Baptist Church. The organization was led by Fred Phelps (who has since died) and located in Topeka, Kansas.\n\n[Fred Phelps]\nFred Waldron Phelps Sr. (November 13, 1929 – March 19, 2014) was an American Baptist minister and civil rights attorney who became notorious for his vehement anti-homosexual rhetoric and protests near the funerals of homosexuals, military veterans, and disaster victims, whose deaths, he believed, were the result of God’s hatred of America’s \"bankrupt values\" and tolerance of homosexual lifestyles.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q422709b9a3",
  "kind": "yes/no",
  "text": "Claim: I Write What I Like was another title published by the owner of the pseudonym Frank Talk.\n\nPassages:\n\n[Steve Biko]\nHis ideas were articulated in a series of articles published under the pseudonym Frank Talk.\n\n[I Write What I Like]\nI Write What I Like (full name \"I Write What I Like: Selected Writings by Steve Biko\") is a compilation of writings from anti-apartheid activist Steve Biko.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q44abc125ec",
  "kind": "yes/no",
  "text": "Claim: A TV show featuring Chris Harris (actor) was later shown in the United States. It was part of a program whose featurettes focused on characters with psychic abilities.\n\nPassages:\n\n[Into the Labyrinth (TV series)]\nInto the Labyrinth is a British children's television series. The first series only was later shown in the United States as part of \"The Third Eye\" science fiction series on Nickelodeon.\n\n[The Third Eye (TV series)]\nThe Third Eye is an American anthology series on Nickelodeon. All of the program's featurettes focused on characters with psychic abilities.\n\n[Chris Harris (actor)]\nHe appeared in several UK TV series including \"Into the Labyrinth\" and \"Hey Look That's Me\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q45f4613cca",
  "kind": "yes/no",
  "text": "Claim: The meaning of \"other division\" that boxer Trevor Prangley's fought in aside from Light Weight, refers to different weight classes.\n\nPassages:\n\n[Trevor Prangley]\nHe competed in the Middleweight and Light Heavyweight divisions.\n\n[Middleweight (MMA)]\nThe middleweight division in mixed martial arts refers to different weight classes:",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q511ba4c6ce",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Non-sarcastically I'd probably say \"Oh, out of curiousity, what's the reason for Ms. Thatcher trending?\"",
   "'Margaret Thatcher' is trending... has 2016 taken another one?"
  ]
 },
 {
  "qid": "q941360973e",
  "kind": "yes/no",
  "text": "Claim: The backing vocalist on \"We've Had Enough\" is known for playing in punk bands and another singer isn't. This other singer boosted the popularity of Reggae rock.\n\nPassages:\n\n[Keith Morris]\nKeith Morris (born September 18, 1955) is an American singer and songwriter known for his role as frontman of the hardcore punk bands Black Flag, Circle Jerks, and Off!\n\n[We've Had Enough]\n\"We've Had Enough\" features backing vocals by Keith Morris, singer of the Circle Jerks and original singer of Black Flag.\n\n[Reggae rock]\nThe genre has lately found a boost in popularity with the 2010 song \"Lay Me Down\" by the Dirty Heads featuring Rome Ramirez from Sublime with Rome, which peaked at number 1 on both the US \"Billboard\" Alternative Songs and Rock Songs charts.\n\n[Rome Ramirez]\nRoman René Ramírez (born June 11, 1988 in Fremont, California), better known as Rome Ramirez or simply Rome, is an American singer and guitarist best known for playing with Eric Wilson from Sublime and Josh Freese from The Vandals in the band Sublime with Rome.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2758953b49",
  "kind": "yes/no",
  "text": "Claim: Twyla Tharp is the famous dancer, taught by Richard Thomas, that formed her own dance company in June 1966.\n\nPassages:\n\n[Twyla Tharp]\nTwyla Tharp ( ; born July 1, 1941) is an American dancer, choreographer, and author who lives and works in New York City. In 1966, she formed her own company Twyla Tharp Dance.\n\n[Richard Thomas (dancer)]\nRichard Scott Thomas (December 3, 1925 – July 27, 2013) was an American dancer, educator, and co-founder of the New York School of Ballet along with his wife Barbara Fallis. He is known as a teacher of Eliot Feld and Twyla Tharp",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q73f31364c7",
  "kind": "yes/no",
  "text": "Claim: Dronamraju Krishna Rao focused his work on the research of a British-born scientist who passed on 1 december 1964.\n\nPassages:\n\n[Dronamraju Krishna Rao]\nOne focus of his work has been the research of J. B. S. Haldane.\n\n[J. B. S. Haldane]\nJohn Burdon Sanderson Haldane ( ; 5 November 1892 – 1 December 1964) was a British-born scientist known for his work in the study of physiology, genetics, evolutionary biology, and in mathematics, where he made innovative contributions to the fields of statistics and biostatistics.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4336951b5f",
  "kind": "yes/no",
  "text": "Claim: An Mandarin rock band released My Animal. This band has more studio albums than The Invisible.\n\nPassages:\n\n[My Animal]\nMy Animal (1998) is the debut album by American rock band Boy Hits Car.\n\n[Boy Hits Car]\nBoy Hits Car released their 5th studio album \"All That Led Us Here\" in May 2014 and are following it up with a European tour.\n\n[The Invisible (band)]\nTheir self-titled debut album, released on 9 March 2009, was nominated for the Mercury Prize and selected as critics choice for iTunes album of the year.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q5405307319",
  "kind": "yes/no",
  "text": "Claim: Tevin Sherard Elliot quarterbacked for a university football team that is a member of the Big 12 Conference.\n\nPassages:\n\n[Tevin Elliot]\nTevin Sherard Elliot (born May 16, 1991) is a former Baylor American football linebacker that is currently serving 20 years in state prison for 2 rape charges against a female Baylor athlete.\n\n[Baylor Bears football]\nThey are a member of the Big 12 Conference.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q7ca7da682f",
  "kind": "yes/no",
  "text": "Claim: A 400-year-old wine cellar was below an influential rock music venue which changed little until its closure featured an American folk singer-songwriter who has had a music career spanning more than fifty years.\n\nPassages:\n\n[Tom Paxton]\nThomas Richard Paxton (born October 31, 1937) is an American folk singer-songwriter who has had a music career spanning more than fifty years.\n\n[Bunjies]\nBelow the café, in a 400-year-old wine cellar, was an influential music venue which changed little until its closure (and conversion of the premises into a restaurant) in 1999.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qcdbe109045",
  "kind": "yes/no",
  "text": "Claim: Zane Grey the author whose work has been translated into 112 films was also a co-author for Open Range.\n\nPassages:\n\n[Open Range (1927 film)]\nOpen Range is a lost 1927 American Western silent film directed by Clifford Smith and written by Roy Briant, Zane Grey, J. Walter Ruben and John Stone.\n\n[Zane Grey]\nHis novels and short stories have been adapted into 112 films, two television episodes, and a television series, \"Dick Powell's Zane Grey Theater\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf96d2eee2e",
  "kind": "yes/no",
  "text": "Claim: A genus of plant with a radians species grows in Northern Cape in a country. It has more species than the Stenocarpus genus does. Sandlane is located close to the border with the country.\n\nPassages:\n\n[Sandlane]\nIt is located close to the border with South Africa, 40 kilometres southwest of the capital, Mbabane.\n\n[Geissorhiza]\nGeissorhiza is a genus of about 80 species of deciduous perennial flowering plants in the iris family first described as a genus in 1803.\n\n[Geissorhiza radians]\nGeissorhiza radians is an Geissorhiza species found growing in Northern Cape, South Africa.\n\n[Stenocarpus]\nStenocarpus is a genus of about 25 species known to science, of woody trees or shrubs, constituting part of the plant family Proteaceae.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe8761593ad",
  "kind": "yes/no",
  "text": "Claim: The actor starred in the 2017 drama, Sidney Hall, directed by Shawn Christensen. He also appeared with Jennifer Connelly in the film Stuck in Love.\n\nPassages:\n\n[Stuck in Love]\nThe film stars Jennifer Connelly, Greg Kinnear, Lily Collins, Nat Wolff and Logan Lerman.\n\n[Sidney Hall (film)]\nSidney Hall is a 2017 American drama film directed and co-written by Shawn Christensen.\n\n[Logan Lerman]\nHe subsequently played d'Artagnan in 2011's \"The Three Musketeers\", starred in the coming-of-age dramas \"The Perks of Being a Wallflower\" (2012), \"Indignation\" (2016) and \"Sidney Hall\" (2017), and had major roles in the 2014 films \"Noah\" and \"Fury\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qd48da6d598",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which text is sarcastic?",
  "options": [
   "It is finally going to reach 45 degrees outside.",
   "The high tomorrow is 45! Anyone wanna go to the pool?"
  ]
 },
 {
  "qid": "q56902642f7",
  "kind": "yes/no",
  "text": "Claim: The person associated with The Legend of the Blue Sea, rose to fame after her as a girl in a film that's title means \"That Bizarre Girl\".\n\nPassages:\n\n[My Sassy Girl]\nMy Sassy Girl (Korean: 엽기적인 그녀 ; literally, \"That Bizarre Girl\") is a 2001 South Korean romantic comedy film directed by Kwak Jae-yong, starring Jun Ji-hyun and Cha Tae-hyun.\n\n[The Legend of the Blue Sea]\nThe Legend of the Blue Sea () is a 2016-2017 South Korean television series starring Jun Ji-hyun and Lee Min-ho.\n\n[Jun Ji-hyun]\nJun Ji-hyun (born Wang Ji-hyun on 30 October 1981), also known as Gianna Jun, is a South Korean actress. She rose to fame for her role as The Girl in the romantic comedy \"My Sassy Girl\" (2001), one of the highest-grossing Korean comedies of all time.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q974ae0bc46",
  "kind": "yes/no",
  "text": "Post: Lol i actually realized that I’ve justified not working out for the past three months by telling myself that my hair was too short to fit in a ponytail.",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qe82f3d2a72",
  "kind": "yes/no",
  "text": "Claim: Aimé Félix Tschiffely born in the European country Switzerland.\n\nPassages:\n\n[Aimé Félix Tschiffely]\nAimé Félix Tschiffely (May 7, 1895 – January 5, 1954) was a Swiss-born, Argentine professor, writer, and adventurer.\n\n[Switzerland]\nSwitzerland ( ), officially the Swiss Confederation, is a federal republic in Europe.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q295bfd3349",
  "kind": "yes/no",
  "text": "Claim: Glenn Martin Hughes attended high school in Mineola, New York.\n\nPassages:\n\n[Glenn Hughes (Village People)]\nHe graduated in 1968 from Chaminade High School, then attended Manhattan College, where he was initiated as a member of Phi Mu Alpha Sinfonia music fraternity in 1969.\n\n[Chaminade High School]\nChaminade High School is a Roman Catholic college preparatory high school for boys in Mineola, New York, United States.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q6e93890ff1",
  "kind": "yes/no",
  "text": "Claim: The Cathedral of the Blessed Virgin Mary, Truro is located in Cornwall and not the place where Rev. John Thomas Becher was Vicar-General for a period in the early 1800s.\n\nPassages:\n\n[Truro Cathedral]\nThe Cathedral of the Blessed Virgin Mary, Truro is a Church of England cathedral in the city of Truro, Cornwall.\n\n[Southwell Minster]\nSouthwell Minster or is a minster and cathedral, in Southwell, Nottinghamshire, England.\n\n[Rev. John Thomas Becher]\nThe Rev. John Thomas Becher (born 1770 died 1848), was an English clergyman, social reformer and Vicar-General of Southwell Minster from 1818 to 1840.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q1f20e82285",
  "kind": "yes/no",
  "text": "Claim: The name of the illegitimate daughter of the President involved in the Teapot Dome scandal in 1865 was Elizabeth.\n\nPassages:\n\n[Warren G. Harding]\nWarren Gamaliel Harding (November 2, 1865 – August 2, 1923) was the 29th President of the United States, serving from March 4, 1921, until his death in 1923. At the time of his death, he was one of the most popular presidents, but the subsequent exposure of scandals that took place under his administration, such as Teapot Dome, eroded his popular regard, as did revelations of an affair by Nan Britton, one of his mistresses.\n\n[Nan Britton]\nNanna Popham Britton (November 9, 1896 – March 21, 1991) was an American secretary who was the mistress of Warren G. Harding, the 29th President of the United States. In 1927, she revealed that her daughter, Elizabeth, had been fathered by Harding while he was serving in the United States Senate, one year before he was elected to the presidency.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc02af61b80",
  "kind": "yes/no",
  "text": "Claim: Horror movie R-Point, set in Vietnam, was filmed partially in a location about 3 miles south-west of Povokvil Waterfalls.\n\nPassages:\n\n[Bokor Hill Station]\nIt was used as the location for the final showdown of the movie \"City of Ghosts\" (2002) and the 2004 film \"R-Point\".\n\n[Povokvil Waterfalls]\nIt is located about 3 mi north-east of Bokor Hill Station.\n\n[R-Point]\nSet in 1972 Vietnam, during the Vietnam War, it stars Kam Woo-sung and Son Byong-ho as members of the South Korean military in Vietnam.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q78aaa44d7c",
  "kind": "yes/no",
  "text": "Claim: Massimo Giordano born in the Metropolitan City Naples.\n\nPassages:\n\n[Pompei]\nPompei (] ) is a city and \"comune\" in the Metropolitan City of Naples in Italy, home of the ancient Roman ruins part of the UNESCO World Heritage Sites.\n\n[Massimo Giordano]\nMassimo Giordano (born 19 February 1971) is an Italian-born operatic tenor who is known for his bel canto repertoire. Giordano was born in Pompei, Italy into an Italian working-class family.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6cec0c64f8",
  "kind": "yes/no",
  "text": "Claim: Blake Alexander Carrington is a fictional character on the ABC television series \"Dynasty\", created by Richard and Esther Shapiro whose role was portrayed by John Forsythe, and also appeared as a guest on several talk and variety shows and as a panelist on quiz formatted game shows.\n\nPassages:\n\n[John Forsythe]\nHe also appeared as a guest on several talk and variety shows and as a panelist on numerous game shows.\n\n[Blake Carrington]\nBlake Alexander Carrington is a fictional character on the ABC television series \"Dynasty\", created by Richard and Esther Shapiro. The role was portrayed by John Forsythe from the first episode of the series in 1981 until its finale in 1989.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qb82a724c8f",
  "kind": "yes/no",
  "text": "Claim: The writer of Serenade No. 6 (Mozart) was a composer. So was the writer of Brazilian national anthem L'esule di Granata.\n\nPassages:\n\n[L'esule di Granata]\nL'esule di Granata (\"The exile of Granada\") is a \"melodramma serio\" (serious opera ) in two acts by Giacomo Meyerbeer.\n\n[Serenade No. 6 (Mozart)]\nThe Serenade No. 6 for Orchestra in D major K. 239, \"Serenata notturna\", was written by Wolfgang Amadeus Mozart in Salzburg, in 1776.\n\n[Giacomo Meyerbeer]\nGiacomo Meyerbeer (born Jacob Liebmann Beer; 5 September 1791 – 2 May 1864) was a German opera composer of Jewish birth who has been described as perhaps the most successful stage composer of the nineteenth century.\n\n[Wolfgang Amadeus Mozart]\nWolfgang Amadeus Mozart ( ; ; ] ; 27 January 1756 – 5 December 1791), baptised as Johannes Chrysostomus Wolfgangus Theophilus Mozart, was a prolific and influential composer of the Classical era.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 }
]
