# A46 replay label-noise blind read RSAS04-blind_read-8bf0a32d-003

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS04-blind_read-8bf0a32d-003.json

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
  "qid": "q5790c70acc",
  "kind": "yes/no",
  "text": "Tweet: I may look happy on the outside bit on the inside I'm dying #painful #sad",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qb613172c15",
  "kind": "yes/no",
  "text": "Text: Remember the hundred emails from companies when Covid started getting real? I’ve gotten three in regards to support for protests. And only @SavageXFenty shared helpful links and actually said black lives matter... we love capitalism 🥰🙌🏼",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qf46e178d22",
  "kind": "yes/no",
  "text": "Claim: This retired tennis player and model won the singles title at the 1988 Swan Premium Open. The winner of The 1974 Pacific Coast Open singles tournament, reached a higher career-high singles ranking than she did.\n\nPassages:\n\n[1974 Pacific Coast Open]\nUnseeded Ross Case won the singles title and the accompanying $16,000 first prize money and 80 Grand Prix points.\n\n[1988 Swan Premium Open]\nFifth-seeded Slobodan Živojinović won the singles title.\n\n[Slobodan Živojinović]\nAs a singles player, he reached the semi-finals of the 1985 Australian Open and the 1986 Wimbledon Championships, achieving a career-high ranking of World No. 19.\n\n[Ross Case]\nRoss Case (born 1 November 1951) is an Australian former tennis player.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q7b12e22ad0",
  "kind": "yes/no",
  "text": "Claim: This 1980's book was a list of films considered the worst. It was written by a US film critic born in 1948.\n\nPassages:\n\n[List of films considered the worst]\nExamples of such sources include Metacritic, Roger Ebert's list of most-hated films, \"The Golden Turkey Awards\", \"Leonard Maltin's Movie Guide\", Rotten Tomatoes, the Stinkers Bad Movie Awards, \"Mystery Science Theater 3000\", and the Golden Raspberry Awards (\"Razzies\").\n\n[Michael Medved]\nMichael S. Medved (born October 3, 1948) is an American radio show host, author, political commentator, and film critic.\n\n[The Golden Turkey Awards]\nThe Golden Turkey Awards is a 1980 book by film critic Michael Medved and his brother Harry.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q25772af28d",
  "kind": "yes/no",
  "text": "Text: There is nothing new in an oliver james publication that can't be found elsewhere for free. He's a leftist living a straight bourgeois life",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q4e46e598fc",
  "kind": "yes/no",
  "text": "Tweet: help why do i keep having nightmares about being amish",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q4fa553e92c",
  "kind": "yes/no",
  "text": "Claim: NFL quarterback, Heisman winner, and OU football player graduated from Putnam City North High School.\n\nPassages:\n\n[University of Oklahoma]\nThe University of Oklahoma (OU) is a coeducational public research university in Norman, Oklahoma.\n\n[Sam Bradford]\nBradford attended Putnam City North High School in Oklahoma City, where he starred in football, basketball and golf.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb76af424ac",
  "kind": "yes/no",
  "text": "Claim: A star of \"Hotline\", a 2014 film, and Millard Webb are both authors.\n\nPassages:\n\n[Millard Webb]\nMillard Webb (6 December 1893 – 21 April 1935), was an American screenwriter and director.\n\n[Hotline (2014 film)]\nThe film stars Miss Cleo, Jeff Ragsdale, Jamie Blaine, and Tonya Jone Miller.\n\n[Jeff Ragsdale]\nJeffrey Charles \"Jeff\" Ragsdale ( ) is an American author, documentary filmmaker, actor and stand-up comedian.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2a607d4708",
  "kind": "yes/no",
  "text": "Claim: A genus containing Butein, and Aruncus are both examples of genus fern plant catagorization.\n\nPassages:\n\n[Aruncus]\nAruncus is a genus of clump forming herbaceous perennial plants in the family Rosaceae.\n\n[Butein]\nIt can be found in \"Toxicodendron vernicifluum\" (or formerly \"Rhus verniciflua\"), \"Dahlia\", \"Butea\" (\"Butea monosperma\") and \"Coreopsis\" It has antioxidative, aldose reductase and advanced glycation endproducts inhibitory effects.\n\n[Dahlia]\nDahlia ( or ) is a genus of bushy, tuberous, herbaceous perennial plants native to Mexico.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5bb1130aa1",
  "kind": "yes/no",
  "text": "Claim: One of the bands that collaborated in American Underdog was formed earlier than the Jon Spencer Blues Explosion.\n\nPassages:\n\n[Jon Spencer Blues Explosion]\nThe Jon Spencer Blues Explosion is an American alternative rock trio, formed in 1991 and based in New York City, New York.\n\n[American Underdog]\nThis album includes collaborations with Daddy X, The Dirtball, Johnny Richter, Scott Russo of Unwritten Law, Jared of Hed PE, and John E. Necro.\n\n[Unwritten Law]\nUnwritten Law is an American rock band formed in 1990 in Poway, California They have released seven full-length studio albums and have toured internationally, including performances on the Warped Tour.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q4b94a9d4ee",
  "kind": "yes/no",
  "text": "Claim: The magazine that Robert W. McElroy writes for is headquartered in Manhattan.\n\nPassages:\n\n[Robert W. McElroy]\nRobert Walter McElroy (born February 5, 1954) is a Roman Catholic prelate and bishop. McElroy was educated by the Jesuits and writes for their official publication in the United States, \"America\".\n\n[America (magazine)]\nAmerica is a national weekly magazine published by the Jesuits of the United States and headquartered in midtown Manhattan.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4d89d85874",
  "kind": "yes/no",
  "text": "Claim: The song that was scored by the bandmate of O'Neill Spencer, that is often the piece of music played during an evening of revelry, is \"Loch Lomond\".\n\nPassages:\n\n[John Kirby (musician)]\nIn addition to sideman work (prominently with Benny Goodman), Kirby is remembered for leading a successful chamber jazz sextet in the late 1930s and early 1940s, which scored several hit songs including \"Loch Lomond\" and the debut recording of \"Undecided\", a jazz standard.\n\n[O'Neill Spencer]\nHe is most known for his work in the John Kirby Sextet.\n\n[The Bonnie Banks o' Loch Lomond]\nIn Scotland, the song is often the final piece of music played during an evening of revelry (a dance party or dinner, etc.).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qf5f305f4d0",
  "kind": "yes/no",
  "text": "Claim: Hermann Neubacher held a diplomatic passport as an Austrian Nazi politician in the Albanian Kingdom, when it was under the control of the Kingdom of Italy.\n\nPassages:\n\n[Albanian Kingdom (1943–44)]\nThe Albanian Kingdom (Albanian: \"Mbretëria Shqiptare\", German: \"Königreich Albanien\") existed as a \"de jure\" independent country, between 1943 and 1944. Before the armistice between Italy and the Allied armed forces on 8 September 1943, Albania had been in a de jure personal union with and was de facto under the control of the Kingdom of Italy.\n\n[Hermann Neubacher]\nDuring the Second World War, he was appointed as the leading German foreign ministry official for the Balkans (including Greece, Serbia, Albania and Montenegro).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q6b8c8854c7",
  "kind": "yes/no",
  "text": "Claim: Wolfgang Amadeus Mozart was a composer. So was the composer of L'esule di Granata.\n\nPassages:\n\n[Wolfgang Amadeus Mozart]\nWolfgang Amadeus Mozart ( ; ; ] ; 27 January 1756 – 5 December 1791), baptised as Johannes Chrysostomus Wolfgangus Theophilus Mozart, was a prolific and influential composer of the Classical era.\n\n[Giacomo Meyerbeer]\nGiacomo Meyerbeer (born Jacob Liebmann Beer; 5 September 1791 – 2 May 1864) was a German opera composer of Jewish birth who has been described as perhaps the most successful stage composer of the nineteenth century.\n\n[L'esule di Granata]\nL'esule di Granata (\"The exile of Granada\") is a \"melodramma serio\" (serious opera ) in two acts by Giacomo Meyerbeer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qe67fdec6b9",
  "kind": "yes/no",
  "text": "Claim: The director of the silent film The Italian Straw Hat, also wrote the film. The writer and director was born before the director of the Mexican movie Bugambilia.\n\nPassages:\n\n[Emilio Fernández]\nEmilio \"El Indio\" Fernández (born Emilio Fernández Romo, ] ; March 26, 1904 – August 6, 1986) was a Mexican film director, actor and screenwriter.\n\n[The Italian Straw Hat (film)]\nThe Italian Straw Hat (French: Un chapeau de paille d'Italie ) is a 1928 French silent film comedy written and directed by René Clair, in his feature debut, based on the 1851 play \"Un chapeau de paille d'Italie\", by Eugène Marin Labiche and Marc-Michel.\n\n[Bugambilia]\nBugambilia (\"Bougainvillea\") is a Mexican movie of 1945 directed by Emilio Fernández and starring Dolores del Río and Pedro Armendáriz.\n\n[René Clair]\nRené Clair (11 November 1898 – 15 March 1981) born René-Lucien Chomette, was a French filmmaker and writer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qa18136ec39",
  "kind": "yes/no",
  "text": "Claim: Thee owner of the 165 acre drumlin or the mansion that sits on the hill donated $145,000 to the construction fund for the Benjamin Stickney Cable Memorial Hospital.\n\nPassages:\n\n[Benjamin Stickney Cable Memorial Hospital]\nCrane purchased the land on which the building sits and made a further donation of $145,000 to the construction fund.\n\n[Castle Hill (Ipswich, Massachusetts)]\nCastle Hill refers to either a 165 acre drumlin surrounded by sea and salt marsh or to the mansion that sits on the hill.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q2709158e31",
  "kind": "yes/no",
  "text": "Claim: Yes, both the nature magazine Ángel Manuel Rodríguez authors in and this publication have a headquarter or editor based in Maryland. This publication featured Carol Weston as an advice columnist.\n\nPassages:\n\n[Adventist World]\nEditors are based in Silver Spring, Maryland and Seoul, Korea.\n\n[Carol Weston]\nThe author of sixteen books, both fiction and non-fiction, she has been the \"Dear Carol\" advice columnist at Girls' Life since the magazine's first issue in 1994.\n\n[Ángel Manuel Rodríguez]\nHe has written several books, and authors a monthly column in \"Adventist World\".\n\n[Girls' Life (magazine)]\nThe magazine is headquartered in Baltimore, Maryland.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qab39719137",
  "kind": "yes/no",
  "text": "Claim: The southern Georgia city of Valdosta features the Blazers college athletic teams.\n\nPassages:\n\n[Valdosta, Georgia]\nValdosta is a city in and the county seat of Lowndes County, located on the southern border of Georgia, United States.\n\n[Valdosta State Blazers]\nThe Valdosta State Blazers are the athletic programs of Valdosta State University in Valdosta, Georgia.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qfd31870a18",
  "kind": "yes/no",
  "text": "Claim: The Wu-Tang Clan is the New York City–based hip-hop musical group that consists of rappers including Cappadonna.\n\nPassages:\n\n[Wu-Tang Clan anthology]\nThe Wu-Tang Clan is a New York City–based hip-hop musical group, consisting of ten American rappers: RZA, GZA, Raekwon, U-God, Ghostface Killah, Inspectah Deck, Method Man, Masta Killa, Cappadonna, and the late Ol' Dirty Bastard.\n\n[Cappadonna]\nDarryl Hill (born September 18, 1969), best known by his stage name Cappadonna, is an American rapper and official member of the hip-hop collective Wu-Tang Clan.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5aa031d6ee",
  "kind": "yes/no",
  "text": "Claim: The notable work from French music video director Yoann Lemoine, Back to December, features an apology and plea for forgiveness.\n\nPassages:\n\n[Back to December]\nAccording to Swift, \"Back to December\" is the first time she ever apologizes to someone in a song. \"Back to December\" is considered an orchestral country pop ballad and its lyrics are a remorseful plea for forgiveness for breaking up with a former lover.\n\n[Yoann Lemoine]\nYoann Lemoine (born 16 March 1983) is a French music video director, graphic designer and singer-songwriter. His most notable works include his music video direction for Katy Perry's \"Teenage Dream\", Taylor Swift's single \"Back to December\", Lana Del Rey's \"Born to Die\" and Mystery Jets' \"Dreaming of Another World\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1a2e8a7c32",
  "kind": "yes/no",
  "text": "Post: quit a high paying job for a blind fantasy with no family, no friends, no backup plan… deserved every tear streaming down his face https://t.co/y7KxPh3hwx",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q6387541aa8",
  "kind": "yes/no",
  "text": "Claim: The end of the lengthy reign of the Queen for whom the TV series \"Reign\" is based on was in 24 July 1567.\n\nPassages:\n\n[Mary, Queen of Scots]\nMary, Queen of Scots (8 December 1542 – 8 February 1587), also known as Mary Stuart or Mary I, reigned over Scotland from 14 December 1542 to 24 July 1567.\n\n[Reign (season 1)]\nThe series follows the early exploits of Mary, Queen of Scots, and was created by Stephanie SenGupta and Laurie McCarthy.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q251cd37dcb",
  "kind": "yes/no",
  "text": "Claim: The birthplace of Wu Jiaduo and Gongqingcheng are both cities that are located in China.\n\nPassages:\n\n[Linhai]\nLinhai (; Tai-chow dialect: Ling-he) is a county-level city in Taizhou, Zhejiang Province situated on the banks of the Lin River in Eastern China.\n\n[Gongqingcheng]\nGongqingcheng () is a county-level city in northern Jiangxi province, People's Republic of China, established on 10 September 2010.\n\n[Wu Jiaduo]\nWu Jiaduo (; born 19 September 1977 in Linhai, Zhejiang, China) is a female Chinese-born German table tennis player.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qef205e3226",
  "kind": "yes/no",
  "text": "Claim: The Beatles released their 1974 album that featured the song \"Simply Shady\" during the American tour.\n\nPassages:\n\n[The Beatles' 1966 US tour]\nThe Beatles staged their third concert tour of America in August 1966, and it was the last commercial tour they would ever undertake.\n\n[Dark Horse (George Harrison album)]\nAlthough keenly anticipated on release, \"Dark Horse\" is associated with the controversial North American tour that Harrison staged with co-headliner Ravi Shankar in November and December that year.\n\n[Simply Shady]\n\"Simply Shady\" is a song by English musician George Harrison that was released on his 1974 album \"Dark Horse\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q310a726b0e",
  "kind": "yes/no",
  "text": "Claim: The author of and H. L. Mencken were both known for being satirists.\n\nPassages:\n\n[Mythago Wood]\nMythago Wood is a fantasy novel by British writer Robert Holdstock, published in the United Kingdom in 1984.\n\n[Robert Holdstock]\nRobert Paul Holdstock (2 August 1948 – 29 November 2009) was an English novelist and author best known for his works of Celtic, Nordic, Gothic and Pictish fantasy literature, predominantly in the fantasy subgenre of mythic fiction.\n\n[H. L. Mencken]\nHenry Louis Mencken (September 12, 1880 – January 29, 1956) was an American journalist, satirist, cultural critic and scholar of American English.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3893ec8090",
  "kind": "yes/no",
  "text": "Claim: Osho Times was a monthly news and current affairs magazine in the Hindi and English language on themes related to Rajneesh a spiritual teacher, that spent time in Mumbai initiating followers, and based on his talks.\n\nPassages:\n\n[Osho Times]\nOsho Times was a monthly magazine in the Hindi and English language on themes related to spiritual teacher Osho, and based on his talks.\n\n[Rajneesh]\nIn 1970 Rajneesh spent time in Mumbai initiating followers known as \"neo-sannyasins.\"",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qacef1f21e4",
  "kind": "yes/no",
  "text": "Claim: William Henry Oliphant Smeaton best known work The Hounds of Zaroff was also published as the story that Bloodlust! is based on.\n\nPassages:\n\n[The Most Dangerous Game]\n\"The Most Dangerous Game\", also published as \"The Hounds of Zaroff\", is a short story by Richard Connell, first published in \"Collier's\" on January 19, 1924.\n\n[Seven Faces]\nBased upon the piece of short fiction \"A Friend of Napoleon\" which was published in the June 30, 1923, issue of \"The Saturday Evening Post\" magazine by popular writer Richard Connell (whose best known work, \"The Most Dangerous Game\", was filmed three years later), it was directed by Berthold Viertel and stars Paul Muni in his second screen appearance.\n\n[Bloodlust!]\nis a 1961 American horror thriller film based on Robert Connell's short story \"The Most Dangerous Game.\"",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q4e37383512",
  "kind": "yes/no",
  "text": "Claim: The football ground that held a match is in this multi-use sports and recreation facility that currently houses professional football club Dynamo Kyiv. The Italy–Spain football rivalry was held at this match.\n\nPassages:\n\n[FC Dynamo Kyiv]\nFootball Club Dynamo Kyiv (Ukrainian: Футбольний клуб «Динамо» Київ , ] ) is a Ukrainian professional football club based in Kiev. Their home is the 70,050 capacity Olimpiyskiy National Sports Complex.\n\n[Olimpiyskiy National Sports Complex]\nThe Olympic National Sports Complex (also known as Olympic Stadium; Ukrainian: Національний спортивний комплекс \"Олімпійський\" ) is a multi-use sports and recreation facility in Kiev, Ukraine, located on the slopes of the city's central Cherepanov Hill, Pechersk Raion.\n\n[UEFA Euro 2012 Final]\nThe UEFA Euro 2012 Final was a football match that took place on 1 July 2012 at the Olympic Stadium in Kiev, Ukraine, to determine the winner of UEFA Euro 2012.\n\n[Italy–Spain football rivalry]\nMost notably, the two met at the UEFA Euro 2012 Final, which Spain won 4–0.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q815d426c38",
  "kind": "yes/no",
  "text": "Claim: The founder of the Westboro Baptist Church died of liver failure in 2014.\n\nPassages:\n\n[The Most Hated Family in America]\nThe Most Hated Family in America is a 2007 BBC documentary film written and presented by Louis Theroux about the family at the core of the Westboro Baptist Church. The organization was led by Fred Phelps (who has since died) and located in Topeka, Kansas.\n\n[Fred Phelps]\nFred Waldron Phelps Sr. (November 13, 1929 – March 19, 2014) was an American Baptist minister and civil rights attorney who became notorious for his vehement anti-homosexual rhetoric and protests near the funerals of homosexuals, military veterans, and disaster victims, whose deaths, he believed, were the result of God’s hatred of America’s \"bankrupt values\" and tolerance of homosexual lifestyles.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q92c51488da",
  "kind": "yes/no",
  "text": "Claim: The head office of József Váradi's airline is located in Mountain View.\n\nPassages:\n\n[Wizz Air]\n\" ), is a Hungarian low-cost airline with its head office in Budapest.\n\n[József Váradi]\nJózsef Janos Váradi (born 21 September 1965) is a Hungarian businessman who co-founded Wizz Air and has been its CEO since 2003.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qc6659d63b1",
  "kind": "yes/no",
  "text": "Claim: The American politician and attorney which Thomas J. Connolly ran for Governor of Maine in 1998 against was born March 31, 1944.\n\nPassages:\n\n[Angus King]\nAngus Stanley King Jr. (born March 31, 1944) is an American politician and attorney who is the junior United States Senator from Maine.\n\n[Thomas J. Connolly]\nConnolly, a Scarborough resident and attorney based in Portland's Old Port, ran for Governor of Maine in 1998 against incumbent unenrolled Angus King, receiving 13%.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qf1d221c19e",
  "kind": "yes/no",
  "text": "Claim: Duncan Kenworthy produced the film that featured the the song \"No Matter What\" on the US edition of the soundtrack.\n\nPassages:\n\n[No Matter What (Boyzone song)]\nThe song was also featured on the US edition of the soundtrack to the 1999 film \"Notting Hill\", and was released to American radio on 10 May 1999.\n\n[Notting Hill (film)]\nThe screenplay was by Richard Curtis, who had written \"Four Weddings and a Funeral\" (1994), and the film was produced by Duncan Kenworthy and directed by Roger Michell.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa8b637030b",
  "kind": "yes/no",
  "text": "Claim: Kenneth \"Ken\" Leung is the actor that portrays a marvel character in a Eme Ikwuakor television series that was created by Scott Buck.\n\nPassages:\n\n[Ken Leung]\nKenneth \"Ken\" Leung (born January 21, 1970) is an American actor who is best known for playing Miles Straume in \"Lost\", Admiral Statura in \"\", Detective Stephen Sing in \"Saw\", and Kid Omega in \"\". He portrays the Marvel Comics character Karnak, a member of the Inhumans, on the ABC television series \"Inhumans\", which premiered in September 2017.\n\n[Inhumans (TV series)]\nMarvel's Inhumans, or simply Inhumans, is an American television series created for ABC by Scott Buck, based on the Marvel Comics race of the same name.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q70be3a140e",
  "kind": "yes/no",
  "text": "Claim: Anil Agarwal principally owns the parent company of Hindustan Zinc Limited.\n\nPassages:\n\n[Hindustan Zinc]\nIt is a subsidiary of Vedanta Resources PLC.\n\n[Vedanta Resources]\nThe company is principally owned by Indian billionaire Anil Agarwal through Volcan Investments, a holding vehicle with a 61.7% stake in the business.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q42427c5c3f",
  "kind": "yes/no",
  "text": "Claim: J. Walter Duncan sold the USFL team who played home baseball games at Giants Stadium to Donald Trump in 1983.\n\nPassages:\n\n[New Jersey Generals]\nHome games were played at Giants Stadium in East Rutherford, New Jersey, which was called The Meadowlands for Generals games.\n\n[J. Walter Duncan]\nIn 1983, he became owner of the New Jersey Generals, he sold the team to Donald Trump after the 1983 USFL season.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4699ac0e58",
  "kind": "yes/no",
  "text": "Claim: In the 1990's business executive Petrie Dierman Kughn built one of the three mills landmarks in California in 1994.\n\nPassages:\n\n[Great Mall of the Bay Area]\nThe Great Mall of the Bay Area (often simply called The Great Mall) is a large indoor outlet shopping mall in Milpitas, California built by Ford Motor Land Development and Petrie Dierman Kughn in 1994.\n\n[Ontario Mills]\nIt is one of three Mills landmarks in California that are now owned by Simon Property Group since April 2007.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7b67ec9a20",
  "kind": "yes/no",
  "text": "Claim: The creature HNoMS Draug is named from Faroese mythology.\n\nPassages:\n\n[HNoMS Draug]\nTwo ships of the Royal Norwegian Navy have borne the name HNoMS \"Draug\", after the sea revenant Draugr:\n\n[Draugr]\nThe draugr or draug (Old Norse: \"draugr\" , plural draugar ; modern Icelandic: \"draugur\" , Faroese: \"dreygur\" and Danish, Swedish, and Norwegian: \"draug\" ), also called aptrganga or aptrgangr , literally \"again-walker\" (Icelandic: \"afturganga\" ) is an undead creature from Norse mythology.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe6f7374cbc",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which text is sarcastic?",
  "options": [
   "The only thing I got from college is a caffeine addiction",
   "College is really difficult, expensive, tiring, and I often question if a degree is worth the stress."
  ]
 },
 {
  "qid": "qbd71f47a8e",
  "kind": "yes/no",
  "text": "Claim: The Mercury tracer is based on variations of the sporty Mazada Protege which is manufactured by the Mazda Familia company.\n\nPassages:\n\n[Mercury Tracer]\nAll three generations of the Tracer were based on variations of the Mazda 323/Protegé.\n\n[Mazda Familia]\nThe Mazda Familia, also marketed prominently as the Mazda 323 and Mazda Protegé, was a small family car that was manufactured by Mazda between 1963 and 2003. The Familia line was replaced by the Mazda3/Axela for 2004.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qb586771a8f",
  "kind": "choice",
  "text": "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
  "question": "Which text is sarcastic?",
  "options": [
   "Once I get a Bachelor`s degree I will be the same person, just with a slip of paper.",
   "\"I can't wait to be a piece of shit with a bachelors degree\""
  ]
 },
 {
  "qid": "q5d7cf06399",
  "kind": "yes/no",
  "text": "Post: YouTube just gave me a gamer targeted covid vaccine ad and anyway get vaccinated gamers.",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q295949651c",
  "kind": "yes/no",
  "text": "Tweet: A wrong impression is once again my specialty",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q537ed37ed9",
  "kind": "yes/no",
  "text": "Claim: Director Robert Stevenson was from a geographically smaller country than another Baltic director. That director directed his final film Romance of Astree and Celadon.\n\nPassages:\n\n[Robert Stevenson (director)]\nRobert Stevenson (31 March 1905 – 30 April 1986) was an English film writer and director.\n\n[Romance of Astree and Celadon]\nRomance of Astrea and Celadon (French: \"Les Amours d'Astrée et de Céladon\" ) is the final film directed by Éric Rohmer.\n\n[Éric Rohmer]\nJean Marie Maurice Schérer or Maurice Henri Joseph Schérer, known as Éric Rohmer (] , 21 March 192011 January 2010), was a French film director, film critic, journalist, novelist, screenwriter and teacher.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q2d63c92435",
  "kind": "yes/no",
  "text": "Claim: The name of Peter Gifford's rock band (1980-1987) came to be chosen by drawing the name out of a hat.\n\nPassages:\n\n[Midnight Oil]\nBy late 1976, Garrett moved to Sydney to complete his law degree, and Farm changed its name to Midnight Oil by drawing the name out of a hat.\n\n[Peter Gifford]\nFrom 1980 until 1987 he played bass guitar, Chapman Stick and sang backing vocals for Australian rock band Midnight Oil.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q9daedcf85d",
  "kind": "yes/no",
  "text": "Text: Accidentally ordered a chicken sandwich from McD’s without the bun… they had to put fried chicken with two pickles on top in a box. I hope I made them laugh",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qce73b43f25",
  "kind": "yes/no",
  "text": "Text: @kagune_kun despicable tweet, my liege",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qd4865df0fc",
  "kind": "yes/no",
  "text": "Claim: Joseph Eccles was born in England.\n\nPassages:\n\n[Accrington]\nAccrington is a town in the Hyndburn borough of Lancashire, England.\n\n[Joseph Eccles]\nJoseph Eccles (13 April 1863 – 2 September 1933) was an English cricketer active from 1886 to 1889 who played for Lancashire. He was born in Accrington and died in Preston.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qdc17624142",
  "kind": "yes/no",
  "text": "Tweet: Dunno what’s worse us losing or this covid that’s riddled all over me body",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q28119157be",
  "kind": "yes/no",
  "text": "Claim: Sarah Kate Silverman, partner of Jash, was born in 1970.\n\nPassages:\n\n[Mickey Meyer]\nMickey Meyer (born October 28, 1984) is a digital media producer and co-founder of Jash—a multi-tiered studio with partners Sarah Silverman, Reggie Watts, Tim & Eric, and Michael Cera.\n\n[Sarah Silverman]\nSarah Kate Silverman (born December 1, 1970) is an American stand-up comedian, actress, producer, and writer.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q7e8c0a085b",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I feel like my dad hates me",
   "does ur dad hate you for no reason or are you normal?"
  ]
 }
]
