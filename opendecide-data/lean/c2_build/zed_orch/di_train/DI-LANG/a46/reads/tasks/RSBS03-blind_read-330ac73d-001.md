# A46 replay label-noise blind read RSBS03-blind_read-330ac73d-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSBS03-blind_read-330ac73d-001.json

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
  "qid": "qcedd4b134f",
  "kind": "yes/no",
  "text": "Claim: The opera in which Iva Pacetti starred as Elena first premiered in La Scala, Milan.\n\nPassages:\n\n[Iva Pacetti]\nShe reprised the role the following year at Loew's Lexington Theatre in New York City.\n\n[Mefistofele]\nMefistofele (] ) is an opera in a prologue, four acts and an epilogue, the only completed opera with music by the Italian composer-librettist Arrigo Boito (there are several completed operas for which he was librettist only). The opera was given its premiere on 5 March 1868 at La Scala, Milan, under the baton of the composer, despite his lack of experience and skill as a conductor.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qe0335d4038",
  "kind": "yes/no",
  "text": "Claim: The director of the film The River Rat also created the film Coal Miner's Daughter, which won Sissy Spacek an The Execution of Charles Horman:.\n\nPassages:\n\n[Thomas Rickman (writer)]\nThomas Rickman (sometimes credited as Tom Rickman) is an American film director and screenwriter known for such films as \"Coal Miner's Daughter\", \"Hooper\", \"Tuesdays with Morrie\" and \"Truman\".\n\n[Coal Miner's Daughter (film)]\nIt stars Sissy Spacek as Loretta, a role that earned her the Academy Award for Best Actress.\n\n[The River Rat]\nThe River Rat is a 1984 independent family film directed by Thomas Rickman and starring Tommy Lee Jones and Martha Plimpton.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q49be46c9d7",
  "kind": "yes/no",
  "text": "Claim: The novelist Peter Francis Straub has received Postscripts. The author of Hundred Thousand Billion Poems has not received the same award.\n\nPassages:\n\n[Peter Straub]\nPeter Francis Straub (born March 2, 1943) is an American novelist and poet. His horror fiction has received numerous literary honors such as the Bram Stoker Award, World Fantasy Award, and International Horror Guild Award.\n\n[Raymond Queneau]\nRaymond Queneau (] ; 21 February 1903 – 25 October 1976) was a French novelist, poet, critic, editor and co-founder and president of Oulipo (\"Ouvroir de littérature potentielle\"), notable for his wit and cynical humour.\n\n[Hundred Thousand Billion Poems]\nA Hundred Thousand Billion Poems or One hundred million million poems (original French title: \"Cent mille milliards de poèmes\") is a book by Raymond Queneau, published in 1961.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q298c546074",
  "kind": "yes/no",
  "text": "Claim: 1614 is the founding year of the public research university in the Amsterdam, where Jan Borgman was a professor from 1968 to 1988.\n\nPassages:\n\n[University of Groningen]\nThe University of Groningen (abbreviated as UG; Dutch: \"Rijksuniversiteit Groningen\" , abbreviated as \"RUG\") is a public research university in the city of Groningen in the Netherlands. The university was founded in 1614 and is one of the oldest universities in the Netherlands as well as one of its largest.\n\n[Jan Borgman]\nJan Borgman (born 30 November 1929) is a Dutch astronomer and university administrator. He was professor of astronomical observation technique at the University of Groningen from 1968 to 1988.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q1ea3b121d8",
  "kind": "yes/no",
  "text": "Claim: Politician Lyman Sherwood was born in the New York county called Rensselaer County.\n\nPassages:\n\n[Hoosick, New York]\nHoosick is a town in Rensselaer County, New York, United States.\n\n[Lyman Sherwood]\nLyman Sherwood (August 5, 1802 Hoosick, Rensselaer County, New York – September 2, 1865 Lyons, Wayne County, New York) was an American lawyer and politician from New York.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q8236be0504",
  "kind": "yes/no",
  "text": "Claim: Robert Pingeton was hired and fired in April 2010 to replace former head coach Cindy Stein of the team that lost in the second round of the SEC Women's Tournament to Auburn.\n\nPassages:\n\n[2015–16 Missouri Tigers women's basketball team]\nThe Tigers were led by sixth year head coach Robin Pingeton. They play their games at Mizzou Arena and are members of the Southeastern Conference.\n\n[Robin Pingeton]\nRobin Pingeton (born July 9, 1968) is the head coach of the University of Missouri's women's basketball team. She was hired in April 2010 to replace former head coach Cindy Stein.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q0b0272ee7b",
  "kind": "yes/no",
  "text": "Claim: During the period known as the Second Red Scare, Alexander Trachtenberg was convicted under the Smith Act.\n\nPassages:\n\n[Alexander Trachtenberg]\nDuring the period of McCarthyism in America, Trachtenberg was twice subject to prosecution and convicted under the Smith Act; the convictions were overturned, the first by recanting of a government witness and the second by a US Circuit Court of Appeals decision in 1958.\n\n[McCarthyism]\nThe term refers to U.S. Senator Joseph McCarthy and has its origins in the period in the United States known as the Second Red Scare, lasting roughly from 1947 to 1956 and characterized by heightened political repression as well as a campaign spreading fear of influence on American institutions and of espionage by Soviet agents.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3c2d3aba17",
  "kind": "yes/no",
  "text": "Claim: Genesee Cream Ale is a cold fermented, alcohlic beverage produced by a facility located along the Genesee River.\n\nPassages:\n\n[Genesee Cream Ale]\nGenesee Cream Ale is a cold fermented, alcohlic beverage produced by the Genesee Brewing Company in Rochester, NY.\n\n[Genesee Brewing Company]\nGenesee Brewing Company is an American brewery located along the Genesee River in Rochester, New York.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qc9ff548cb9",
  "kind": "yes/no",
  "text": "Text: Lucky for 2nd placed Brentford that there's no stand out team like Leeds this year, or they might have no chance of winning the league. #ncfc",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q2f145f869f",
  "kind": "yes/no",
  "text": "Claim: The producer of the album Beat Pyramid is the British music producer and engineer notable for working wih an English electronic band having the founders: Dave Gahan, Martin Gore, and Andy Fletcher.\n\nPassages:\n\n[Gareth Jones (music producer)]\nGareth Jones (born 1954) is a British music producer and engineer notable for working with Depeche Mode, Einstürzende Neubauten, Wire and Erasure.\n\n[Beat Pyramid]\nThe album was recorded in London and Paris during 2007 and was produced by Gareth Jones in London.\n\n[Depeche Mode]\nDepeche Mode are an English electronic band that formed in Basildon, Essex in 1980. The group consists of founders Dave Gahan (lead vocals), Martin Gore (guitar, keyboards, vocals), and Andy Fletcher (keyboards, bass guitar).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd006a1d696",
  "kind": "yes/no",
  "text": "Claim: Along with the New York Islanders and the New York Rangers, the New Jersey Devils NFL franchise is popular in the New York metropolitan area.\n\nPassages:\n\n[1974–75 New York Islanders season]\nIn the first round of the playoffs, New York defeated the New York Rangers in three games to advance to the Quarter-finals, where the team defeated the Pittsburgh Penguins in seven games, after they had lost the first three.\n\n[New York Rangers]\nThe Rangers are one of three NHL franchises in the New York metropolitan area, along with the New Jersey Devils and New York Islanders.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q99921d9211",
  "kind": "yes/no",
  "text": "Text: Can cats wear nail polish",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q2a9ab433b4",
  "kind": "yes/no",
  "text": "Claim: In addition to A Bayou Legend, William Grant Still composed more than 150 works in the 1970s, including five symphonies and eight operas.\n\nPassages:\n\n[William Grant Still]\nWilliam Grant Still (May 11, 1895 – December 3, 1978) was an American composer, who composed more than 150 works, including five symphonies and eight operas.\n\n[A Bayou Legend]\nA Bayou Legend is an American opera composed by William Grant Still, with a libretto by his wife and frequent collaborator, Verna Arvey.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3ff6417c81",
  "kind": "yes/no",
  "text": "Tweet: yesterday 4 dinner I just had rice w/ sriracha sauce on it and it was arguably the best meal I've had in a while",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q8e1f5454c9",
  "kind": "yes/no",
  "text": "Text: is it illegal to discriminate against someone on the basis that they have a joker tattoo",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q07d9f2b93c",
  "kind": "yes/no",
  "text": "Claim: This fast-food restaurant company was spun off from an American fast food company which was formerly named Tricon Global Restaurants, Inc.\n\nPassages:\n\n[Yum China]\nYum China Holdings Inc. is a Fortune 500 fast-food restaurant company incorporated in the United States and having joint headquarters in Plano, Texas and Shanghai. Spun off from Yum! Brands in 2016, its 420,000 employees represent the 3rd largest worldwide labor force among all U.S. companies.\n\n[Yum! Brands]\nYum! Brands, Inc., or Yum! and formerly Tricon Global Restaurants, Inc., is an American fast food company.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q3085d4102b",
  "kind": "yes/no",
  "text": "Claim: The metal band that released the album The General Electric has released more rock albums than Morningwood.\n\nPassages:\n\n[Morningwood]\nMorningwood was signed to Capitol Records and released two albums.\n\n[The General Electric]\nThe General Electric is the fourth album released by New Zealand band Shihad in October 1999.\n\n[Shihad]\nDuring their recording career, Shihad have produced five number-one studio albums, holding the title for most number one records for any New Zealand artist, alongside Hayley Westenra, and three top-ten singles in New Zealand.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qd0144d2358",
  "kind": "yes/no",
  "text": "Claim: Maki Nomiya and Conrad Lant are both considered musicians.\n\nPassages:\n\n[Maki Nomiya]\nMaki Nomiya (野宮 真貴 , Nomiya Maki , born March 12, 1960) is a Japanese singer and musician.\n\n[Conrad Lant]\nConrad Thomas Lant (born 15 January 1963), also known by the stage name of Cronos, is an English musician.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q05bcbc33c9",
  "kind": "yes/no",
  "text": "Claim: The non-ranking snooker player Chris Norbury lost to made the final of the 2017 China Championship. The player that made the final got the nickname \"The Magician\".\n\nPassages:\n\n[Luca Brecel]\nThe following year, he became the first player from mainland Europe to win a ranking event, defeating Shaun Murphy in the final of the 2017 China Championship.\n\n[Chris Norbury]\nHe played in the latter stages of the Paul Hunter Classic in both 2008 and 2009, losing in the first round to Shaun Murphy 4–1 in 2008, and losing to Dave Harold 4–2 in 2009.\n\n[Shaun Murphy (snooker player)]\nNicknamed \"The Magician\", Murphy is noted for his straight cue action and his long potting.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qb71d1d8653",
  "kind": "yes/no",
  "text": "Claim: The founder of the Orchestra which debuted on January 1, 1988 is of Dutch ethnicity.\n\nPassages:\n\n[André Rieu]\nAndré Léon Marie Nicolas Rieu (born 1 October 1949) is a Dutch violinist and conductor best known for creating the waltz-playing Johann Strauss Orchestra.\n\n[Johann Strauss Orchestra]\nThe Johann Strauss Orchestra was founded by André Rieu in 1987. At the time of its first concert on January 1, 1988, the orchestra consisted of 12 musicians.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa5ad4f80d1",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Simply “I’m miserable.”",
   "someone hit me w a horse tranquilizer istg ive been in a pool of sweat for 6 hours and i havent slept im so tired but i love my friend so much and oh my fucking god i cant rn"
  ]
 },
 {
  "qid": "q17bc7efe77",
  "kind": "yes/no",
  "text": "Claim: The Newcomers are known for the superhero roles as the Marvel Comics as one of their stars.\n\nPassages:\n\n[Chris Evans (actor)]\nEvans is known for his superhero roles as the Marvel Comics characters Steve Rogers / Captain America in the Marvel Cinematic Universe and Johnny Storm / Human Torch in \"Fantastic Four\" and .\n\n[The Newcomers (film)]\nThe Newcomers is a 2000 American family drama film directed by James Allen Bradley and starring Christopher McCoy, Kate Bosworth, Paul Dano and Chris Evans.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q52d7a57cfb",
  "kind": "yes/no",
  "text": "Claim: Antoinette Sandbach resigned as the Welsh Assembly Member for the Wales region to represent Eddisbury in the House of Commons in the UK Parliament in 2015.\n\nPassages:\n\n[Eddisbury (UK Parliament constituency)]\nEddisbury is a constituency in Cheshire represented in the House of Commons of the UK Parliament since 2015 by Antoinette Sandbach, a Conservative.\n\n[Antoinette Sandbach]\nThe following day, 8 May 2015, she resigned as the Welsh Assembly Member for the North Wales region.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2d55b432c0",
  "kind": "yes/no",
  "text": "Claim: The band Blue Peter opened for more people than the band who had the song Hey Leonardo (She Likes Me for Me).\n\nPassages:\n\n[Blue Peter (band)]\nBlue Peter is a Canadian new wave synthpop band founded in 1978 in Markham, Ontario by Chris Wardman and Paul Humphrey. In their heyday, Blue Peter opened for major international acts such as the Police and Simple Minds.\n\n[Hey Leonardo (She Likes Me for Me)]\n\"Hey Leonardo (She Likes Me for Me)\" is a song by American alternative rock group Blessid Union of Souls from their third album, \"Walking Off the Buzz.\"\n\n[Blessid Union of Souls]\nBlessid Union of Souls (sometimes abbreviated to Blessid Union or BUOS) is an American alternative rock band from Cincinnati, Ohio that was formed in 1990 by friends Jeff Pence and Eliot Sloan.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qee7627c1a8",
  "kind": "yes/no",
  "text": "Claim: The british director of the 1947 film New Orleans is not from the USA. Neither is the director of Room in the House.\n\nPassages:\n\n[Arthur Lubin]\nArthur Lubin (July 25, 1898 – May 12, 1995) was an American film director and producer who directed several \"Abbott & Costello\" films, \"Phantom of the Opera\" (1943), the \"Francis the Talking Mule\" series and created the talking-horse TV series \"Mister Ed\".\n\n[Maurice Elvey]\nMaurice Elvey (11 November 1887 – 28 August 1967) was the most prolific film director in British history.\n\n[New Orleans (film)]\nThe movie stars Arturo de Cordova and Dorothy Patrick, features Marjorie Lord, and was directed by Arthur Lubin.\n\n[Room in the House]\nRoom in the House is a 1955 comedy-drama film directed by Maurice Elvey.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5a2647b490",
  "kind": "yes/no",
  "text": "Claim: The author of When William Came, Jack Black, was British. The author of Green, Green My Valley Now was also British.\n\nPassages:\n\n[When William Came]\nWhen William Came: A Story of London Under the Hohenzollerns is a novel written by the British author Saki (the pseudonym of Hector Hugh Munro) and published in November 1913.\n\n[Green, Green My Valley Now]\nGreen, Green My Valley Now is a 1975 novel by Richard Llewellyn.\n\n[Richard Llewellyn]\nRichard Dafydd Vivian Llewellyn Lloyd (8 December 1906 – 30 November 1983), known by his pen name Richard Llewellyn, was a British novelist.\n\n[Saki]\nHector Hugh Munro (18 December 1870 – 14 November 1916), better known by the pen name Saki, and also frequently as H. H. Munro, was a British writer whose witty, mischievous and sometimes macabre stories satirize Edwardian society and culture.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q8bed4cf5ef",
  "kind": "yes/no",
  "text": "Claim: Bern Minster's branch of Protestantism is called The Swiss Reformed Church.\n\nPassages:\n\n[Swiss Reformed Church]\nThe Swiss Reformed Church (German: \"Evangelisch-reformierte Kirchen der Schweiz\" , \"Evangelical Reformed Churches of Switzerland\") refers to the Reformed branch of Protestantism in Switzerland started in Zürich by Huldrych Zwingli and spread within a few years to Basel (Johannes Oecolampadius), Bern (Berchtold Haller and Niklaus Manuel), St. Gallen (Joachim Vadian), to cities in southern Germany and via Alsace (Martin Bucer) to France.\n\n[Bern Minster]\nThe Bern Minster (German: \"Berner Münster\" ) is a Swiss Reformed cathedral, (or minster) in the old city of Bern, Switzerland.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2633c5ed5f",
  "kind": "yes/no",
  "text": "Tweet: fully vaxxed feeling very girlboss",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "q8303383d66",
  "kind": "yes/no",
  "text": "Claim: The head office of József Váradi's airline is located in Budapest.\n\nPassages:\n\n[Wizz Air]\n\" ), is a Hungarian low-cost airline with its head office in Budapest.\n\n[József Váradi]\nJózsef Janos Váradi (born 21 September 1965) is a Hungarian businessman who co-founded Wizz Air and has been its CEO since 2003.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qc4dc56b665",
  "kind": "yes/no",
  "text": "Claim: Ellesmere Port Town Football Club are currently members of the league, whose current principal sponsor is Carlsberg, that Ford Motors F.C. is a part of.\n\nPassages:\n\n[West Cheshire Association Football League]\nThe West Cheshire Association Football League (commonly known as the West Cheshire League) is an English football league in the county of Cheshire. Its current principal sponsor is \"Carlsberg\", also sponsor of the South West Peninsula League.\n\n[Ford Motors F.C.]\nThey compete in the West Cheshire Association Football League and reached the 4th round of the FA Vase in 1985.\n\n[Ellesmere Port Town F.C.]\nThey are currently members of the West Cheshire League Division Two and play at Dunkirk Lane.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q4ffaccc671",
  "kind": "yes/no",
  "text": "Claim: Helen Baxendale wrote the popular 2008 film for the director of the 2012 American action-comedy film \"So Undercover\".\n\nPassages:\n\n[Tom Vaughan (director)]\nHis work includes \"Cold Feet\" (1999) and \"He Knew He Was Right\" (2004) for television, and \"What Happens in Vegas\" (2008) and \"Extraordinary Measures\" (2010) for cinema.\n\n[So Undercover]\nSo Undercover is a 2012 American action-comedy film directed by Tom Vaughan and written by Allan Loeb and Steven Pearl.\n\n[What Happens in Vegas]\nWhat Happens in Vegas is a 2008 American comedy film directed by Tom Vaughan, written by Dana Fox and starring Cameron Diaz and Ashton Kutcher.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q92a3f94256",
  "kind": "yes/no",
  "text": "Claim: The 1999 French Open - Women's Doubles runner-up was born on 7 June 1981. She was also a trainer on The Biggest Loser (season 12).\n\nPassages:\n\n[The Biggest Loser (season 12)]\nAlong with existing trainer Bob Harper, two new trainers (Anna Kournikova and Dolvett Quince.)\n\n[Anna Kournikova]\nAnna Sergeyevna Kournikova (Russian: А́нна Серге́евна Ку́рникова ; ] ; born 7 June 1981) is a Russian former professional tennis player.\n\n[1999 French Open – Women's Doubles]\nNovotná instead partnered with Natasha Zvereva as the first seed, whereas Hingis partnered with Anna Kournikova as the second seed. Novotná and Zvereva retired in their quarterfinal match against Lindsay Davenport and Mary Pierce, but Hingis and Kournikova reached the final where they lost to American sisters Serena and Venus Williams, 6–3, 6–7, 8–6.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4177c35201",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "Why is this 30 yr old man trying to flirt w/ me at this wedding and talking about getting away with dating younger girls. Sir I will call the authorities",
   "I wouldn't even say I will call the authorities, or I would be more specific and say police. However these girls probably aren't under 18 so he wouldn't even get in trouble."
  ]
 },
 {
  "qid": "qc3b1338e3b",
  "kind": "yes/no",
  "text": "Text: I love calling my mom early in the morning and waking her up, I take it as pay back for all the times she never let me sleep in 😜",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q64a471d96f",
  "kind": "yes/no",
  "text": "Claim: Trembling Before G-d and Zeitgeist were not both released in 2001.\n\nPassages:\n\n[Zeitgeist (film series)]\nZeitgeist is a series of three documentary films released between 2007 and 2011 that present a number of conspiracy theories, as well as proposals for broad social and economic changes.\n\n[Trembling Before G-d]\nTrembling Before G-d is an 2001 American documentary film about gay and lesbian Orthodox Jews trying to reconcile their sexuality with their faith.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q9825e91acb",
  "kind": "yes/no",
  "text": "Claim: Lommel differential equation was developed by the German physicist who was the doctoral advisor to another German Physicist who identified the Stark effect.\n\nPassages:\n\n[Johannes Stark]\nJohannes Stark (] , 15 April 1874 – 21 June 1957) was a German physicist and Physics Nobel Prize laureate. He is known for identifying the Stark effect, and was later closely involved with the \"Deutsche Physik\" movement under the Nazi regime.\n\n[Eugen von Lommel]\nEugen Cornelius Joseph von Lommel (19 March 1837, Edenkoben – 19 June 1899, Munich) was a German physicist. He is notable for the Lommel polynomial, the Lommel function, the Lommel–Weber function, and the Lommel differential equation. He is also notable as the doctoral advisor of the Nobel Prize winner Johannes Stark.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9e3d0995ae",
  "kind": "yes/no",
  "text": "Claim: The king, whose reign was the first included in the publication which Roger de Bankwell appears as a counsel in for 1340, was also known as Edward Longshanks and the Prince Marko of the Scots.\n\nPassages:\n\n[Year Books]\nThe Year Books are the modern English name that is now typically given to the earliest law reports of England. They are extant in a continuous series from 1268 to 1535, covering the reigns of King Edward I to Henry VIII.\n\n[Roger de Bankwell]\nHe appears as a counsel in the Year book for 1340, in 1341 was appointed to a justiceship of the king's bench, and was one of those assigned to try petitions from Gascony, Wales, Ireland, Scotland, and 'other foreign parts ' between the years 1341 and 1347.\n\n[Edward I of England]\nEdward I (17/18 June 1239 – 7 July 1307), also known as Edward Longshanks and the Hammer of the Scots (Latin: \"Malleus Scotorum\" ), was King of England from 1272 to 1307.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q172254f230",
  "kind": "yes/no",
  "text": "Claim: The day Southpark is most congested is the fourth Thursday of November.\n\nPassages:\n\n[Black Friday (shopping)]\nBlack Friday ( ) is the day following Thanksgiving Day in the United States (the fourth Thursday of November).\n\n[SouthPark Mall (Charlotte, North Carolina)]\nSouthPark is the most congested shopping area in the United States during Black Friday weekend.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q5ba2b7765e",
  "kind": "yes/no",
  "text": "Claim: Robert Armstrong-Jones, the Welsh physician, was grandfather to Antony Armstrong-Jones, 1st Earl of Snowdon.\n\nPassages:\n\n[Antony Armstrong-Jones, 1st Earl of Snowdon]\nAntony Charles Robert Armstrong-Jones, 1st Earl of Snowdon, (7 March 1930 – 13 January 2017), commonly known as Lord Snowdon, was a British photographer and film maker.\n\n[Robert Armstrong-Jones]\nSir Robert Armstrong-Jones, CBE (born Robert Jones; 2 December 1857 – 31 January 1943) was a Welsh physician and psychiatrist. He was the grandfather of Antony Armstrong-Jones, 1st Earl of Snowdon (d. 2017).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q8975421b31",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which version is written sarcastically?",
  "options": [
   "love island is ending, law school is starting again…summer is really over",
   "love island is over and law school starts soon, but summer isn’t over yet."
  ]
 },
 {
  "qid": "q1afb521183",
  "kind": "yes/no",
  "text": "Post: folklore is not a happy album are you all stupid",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q8287b77980",
  "kind": "yes/no",
  "text": "Claim: Stolen Harmony is an French film directed by this man. We don't know for a fact that he directed more films than Jon Jost.\n\nPassages:\n\n[Jon Jost]\nJon Jost (born 16 May 1943 in Chicago) is an American independent filmmaker.\n\n[Alfred L. Werker]\nAlfred L. Werker (December 2, 1896 – July 28, 1975) was a film director whose work in movies spanned from 1917 through 1957. After a number of film production jobs and assistant directing, Werker co-directed his first film, \"Ridin' the Wind\" in 1925 alongside director Del Andrews. He was brought in by Fox Film Corporation executives to re-shoot and re-edit Erich von Stroheim's film \"Hello, Sister! \" (1933), co-starring Boots Mallory and ZaSu Pitts.\n\n[Stolen Harmony]\nThe movie climaxes with an exciting car chase and was directed by Alfred L. Werker.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q2df3a938eb",
  "kind": "yes/no",
  "text": "Claim: Planes was released after Charley and the Angel.\n\nPassages:\n\n[Charley and the Angel]\nCharley and the Angel is a 1973 Disney family/comedy film set in an unidentified small city in the 1930s Depression-era Midwestern United States and starring Fred MacMurray in one of his final film appearances and his last movie for Disney.\n\n[Planes (film)]\nPlanes is a 2013 American 3D computer-animated sports comedy film produced by DisneyToon Studios and released by Walt Disney Pictures.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qdc00f9aa7d",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "6 more hours and then a whoppingly massive 2days off work! wowzers!",
   "I only have a measly 2 days off work."
  ]
 },
 {
  "qid": "q6797ad7922",
  "kind": "yes/no",
  "text": "Claim: Ranjhay Hath Gandasa is a comedy film starring Pakistani-American singer-songwriter Nadia Ali.\n\nPassages:\n\n[Ranjhay Hath Gandasa]\nIt stars Nadia Ali, Rana Rehman, Fozia Rana, Durdana Rehman, Azhar Rangeela and Shafqat Cheema in lead roles.\n\n[Nadia Ali (singer)]\nNadia Ali (Urdu: ‎ , born 3 August 1980) is a Pakistani American singer-songwriter.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q40b8b5d316",
  "kind": "yes/no",
  "text": "Claim: Creolized forms of Kongo are found in traditional African religions of Africa with some influence from Christianity.\n\nPassages:\n\n[Afro-American religion]\nAfro-American religions (also known as African diasporic religions or New World traditions) are a number of related religions that developed in the Americas in various nations of Latin America, the Caribbean, and the southern United States. They derive from traditional African religions of Africa with some influence from Christianity.\n\n[Kongo language]\nFor this reason, while Kongo still is spoken in the above-mentioned countries, creolized forms of the language are found in ritual speech of Afro-American religions, especially in Brazil, Cuba, and Haiti.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q28e1d6dc38",
  "kind": "yes/no",
  "text": "Claim: A member of S Club 8 and Biff Byford are both American singers.\n\nPassages:\n\n[Stacey McClean]\nStacey McClean (born 17 February 1989) is an English solo singer.\n\n[Biff Byford]\nPeter Rodney \"Biff\" Byford (born 15 January 1951) is an English singer best known as the lead singer of the heavy metal band Saxon.\n\n[S Club 8]\nThe group's members, Frankie Sandford, Jay Asforis, Daisy Evans, Calvin Goldspink, Stacey McClean, Aaron Renfree, Hannah Richings, and Rochelle Wiseman were all in their early teens or younger when they were chosen from thousands of hopefuls on the television series \"S Club Search\" in 2001.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa440009dae",
  "kind": "yes/no",
  "text": "Text: Damn, imagine being vaxxed and then getting a cold and then losing your taste and smell.\n\nOh wait.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q099341cecf",
  "kind": "yes/no",
  "text": "Claim: The Sri Lankan who owned a piece of land died in 1999. This piece of land was once owned by Count de Mauny Talvande.\n\nPassages:\n\n[Paul Bowles]\nPaul Frederic Bowles ( ; December 30, 1910November 18, 1999) was an American expatriate composer, author, and translator.\n\n[Count de Mauny]\nMaurice Talvande, Count de Mauny Talvande (self styled), (1866–1941) was a French-born naturalised British landscaper, furniture-maker, and self-inventor, who is best known as the owner and recreator of Taprobane Island, in Sri Lanka.\n\n[Taprobane Island]\nThe islet passed on to the American author and composer Paul Bowles and then the Sri Lankan born former UN Chief Prosecutor Sir Desmond Lorenz de Silva before it came to the ownership of the Australian businessman Geoffrey Dobbs.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qd94114522f",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Remember when there was only giveaways? I do not miss that.",
   "remember when everyone’s feeds were just retweeted giveaways looool those were the days"
  ]
 }
]
