# A46 replay label-noise blind read RSAS04-blind_read-8bf0a32d-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS04-blind_read-8bf0a32d-000.json

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
  "qid": "q29141cbc38",
  "kind": "yes/no",
  "text": "Post: what if the next iteration of onlyfans was run by women?\n\nceo: @natalinanoel\ninvestors: @BLACCHYNA @iamcardib @miakhalifa @PrincessPiaMia @CorinnaKopf @tanamongeau @HelloImLana\nsoftware engineers (sry if incorrect terminology): @codergirl__  @sashacodes\nmarketing: @ModGirlMktg https://t.co/7lEBt3KNF5",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qf4ffa397dc",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the options carries sarcasm?",
  "options": [
   "My gf has been in the Hamptons nannying for a few hours and she has already been to a POLO match. Is she in GOSSIP GIRL?",
   "My gf has been in the Hamptons nannying for a few hours and she has already been to a POLO match. It’s like she’s in “Gossip Girl”"
  ]
 },
 {
  "qid": "qa398de1308",
  "kind": "yes/no",
  "text": "Claim: Henricus Antonius \"Han\" van Meegeren sold a flower painting to a military officer who was the recipient of Pour le Mérite.\n\nPassages:\n\n[Han van Meegeren]\nHenricus Antonius \"Han\" van Meegeren (] ; 10 October 1889 – 30 December 1947) was a Dutch painter and portraitist and is considered to be one of the most ingenious art forgers of the 20th century. Despite his life of crime, van Meegeren became a national hero after World War Two when it was revealed that he had sold a forged painting to Reichsmarschall Hermann Göring during the Nazi Occupation of the Netherlands.\n\n[Hermann Göring]\nHermann Wilhelm Göring (or Goering; ] ; 12 January 1893 – 15 October 1946) was a German political and military leader as well as one of the most powerful figures in the Nazi Party (NSDAP) that ruled Germany from 1933 to 1945. A veteran World War I fighter pilot ace, he was a recipient of the \"Pour le Mérite\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qf6acac36fb",
  "kind": "yes/no",
  "text": "Claim: The Cathedral of the Blessed Virgin Mary, Truro is located in Cornwall and not the place where Rev. John Thomas Becher was Vicar-General from 1818-1840.\n\nPassages:\n\n[Rev. John Thomas Becher]\nThe Rev. John Thomas Becher (born 1770 died 1848), was an English clergyman, social reformer and Vicar-General of Southwell Minster from 1818 to 1840.\n\n[Southwell Minster]\nSouthwell Minster or is a minster and cathedral, in Southwell, Nottinghamshire, England.\n\n[Truro Cathedral]\nThe Cathedral of the Blessed Virgin Mary, Truro is a Church of England cathedral in the city of Truro, Cornwall.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q317aaee7b1",
  "kind": "yes/no",
  "text": "Claim: Sir Alec Guiness played Professor Godbole in a movie that was based on a novel by E.M. Forster.\n\nPassages:\n\n[A Passage to India (film)]\nThe screenplay is based on the play of the same name by Santha Rama Rau, which was based on the novel of the same name by E.M. Forster.\n\n[Alec Guinness]\nHe is also known for his six collaborations with David Lean: Herbert Pocket in \"Great Expectations\" (1946), Fagin in \"Oliver Twist\" (1948), Col. Nicholson in \"The Bridge on the River Kwai\" (1957, for which he won the Academy Award for Best Actor), Prince Faisal in \"Lawrence of Arabia\" (1962), General Yevgraf Zhivago in \"Doctor Zhivago\" (1965), and Professor Godbole in \"A Passage to India\" (1984).",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q9e11153514",
  "kind": "yes/no",
  "text": "Tweet: people who hate the snow give off the same energy as people who hate cats",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q383ca04563",
  "kind": "yes/no",
  "text": "Text: did you actually fly on a plane if you didn’t post a picture of the view from your window?",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "qcb084b9655",
  "kind": "yes/no",
  "text": "Claim: The venue in Orlando opened in 1936 and is found west of the home venue for the Orlando City SC. The 2017 Pro Bowl was played there.\n\nPassages:\n\n[Orlando City Stadium]\nIt is the home venue for the Orlando City SC, which entered Major League Soccer (MLS) as an expansion franchise in 2015, and their National Women's Soccer League (NWSL) sister club, the Orlando Pride.\n\n[2017 Pro Bowl]\nThe 2017 Pro Bowl (branded as the 2017 Pro Bowl presented by Aquafina for sponsorship reasons) was the National Football League's all-star game for the 2016 season which was played at Camping World Stadium in Orlando, Florida on January 29, 2017.\n\n[Camping World Stadium]\nCamping World Stadium, also known as the Orlando Citrus Bowl, is a stadium located in Orlando, Florida. The stadium is located in the West Lakes neighborhoods of Downtown Orlando, west of new sports and entertainment facilities including the Amway Center, the Dr. Phillips Center for the Performing Arts and the Orlando City Stadium.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q2bb41a82a3",
  "kind": "yes/no",
  "text": "Claim: One of Mabel Keyes Babcock's distant relatives, William Bradford, wrote \"Of Plymouth Plantation\" and served as Governor of the Plymouth Colony.\n\nPassages:\n\n[Mabel Keyes Babcock]\nBorn in Somerville, Massachusetts, on May 20, 1862, Mabel Keyes Babcock was the daughter of botanist Henry H. Babcock and Mary Porter (Keyes) Babcock. She was a descendant of William Bradford, the governor of Plymouth Colony.\n\n[William Bradford (Plymouth Colony governor)]\nHe was a signatory to the Mayflower Compact and went on to serve as Governor of the Plymouth Colony intermittently for about 30 years between 1621 and 1657. His journal \"Of Plymouth Plantation\" covered the years from 1620 to 1657 in Plymouth.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qf0acdd37f4",
  "kind": "yes/no",
  "text": "Claim: This person, who contributed artwork to the 2008-2009 Superman: New Krypton story, was known for illustrative work on a DC Comics publication titled Firestorm.\n\nPassages:\n\n[Firestorm (comics)]\nFirestorm is the name of several fictional superheroes appearing in American comic books published by DC Comics.\n\n[Superman: New Krypton]\n\"New Krypton\" is a 2008-2009 Superman story arc written by Geoff Johns, James Robinson, and Sterling Gates with art by Gary Frank, Alex Ross, Renato Guedes, Jamal Igle and Pete Woods and published by DC Comics.\n\n[Jamal Igle]\nThe creator of the comic book series Molly Danger he is also known for his pencilling, inking and coloring work on books such as \"Supergirl\" and \"Firestorm\".",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qae75574ac1",
  "kind": "yes/no",
  "text": "Claim: The 15th pick of the 2011 NFL was born on July 24, 1989 in Washington DC.\n\nPassages:\n\n[2011 Miami Dolphins season]\nThe Dolphins made their first round selection with the 15th pick of the 2011 NFL Draft on Florida offensive lineman Mike Pouncey.\n\n[Mike Pouncey]\nJames Michael Pouncey (born July 24, 1989) is an American football center for the Miami Dolphins of the National Football League (NFL).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qe28580aa8e",
  "kind": "yes/no",
  "text": "Claim: Indie studio Jumpship developed the puzzle-platform video game, whose spiritual successor was the game Inside, which was released in July 2010.\n\nPassages:\n\n[Somerville (video game)]\nSomerville is an upcoming video game and the debut title by the indie studio Jumpship.\n\n[Limbo (video game)]\nLimbo is a puzzle-platform video game developed by independent studio Playdead. The game was released in July 2010 on Xbox Live Arcade, and has since been ported to several other systems, including the PlayStation 3 and Microsoft Windows.\n\n[Inside (video game)]\nIt is the spiritual successor to Playdead's 2010 game \"Limbo,\" and features similar 2.5D gameplay.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qa932f7386c",
  "kind": "yes/no",
  "text": "Claim: The LDS Church President that dedicated the bronze This is the Place Monument, played a more important role in the church than the director of Hail the Judge. Hail the Judge starred Stephen Crow, Cheung Man and Ng Man Tat.\n\nPassages:\n\n[Hail the Judge]\nHail the Judge () is a 1994 Hong Kong comedy film directed by Wong Jing, starring Stephen Chow, Cheung Man, and Ng Man Tat.\n\n[This is the Place Monument]\nIt was dedicated by LDS Church President George Albert Smith on 24 July 1947, the hundredth anniversary of the pioneers entering the Salt Lake Valley.\n\n[George Albert Smith]\nGeorge Albert Smith Sr. (April 4, 1870 – April 4, 1951) was an American religious leader who served as the eighth president of The Church of Jesus Christ of Latter-day Saints (LDS Church).\n\n[Wong Jing]\nWong Jing ( born 3 May 1955) is a Hong Kong film director, producer, actor, presenter, and screenwriter.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qda384a52a6",
  "kind": "yes/no",
  "text": "Claim: The genus and species of the bear in which the animal, an inhabitant of Collier-Seminole State Park, is a subspecies of, is the Ursus americanus.\n\nPassages:\n\n[American black bear]\nThe American black bear (\"Ursus americanus\") is a medium-sized bear native to North America.\n\n[Florida black bear]\nThe Florida black bear (\"Ursus americanus floridanus\") is a subspecies of the American black bear that has historically ranged throughout most of Florida and southern portions of Alabama, Georgia, and Mississippi.\n\n[Collier-Seminole State Park]\nbrown pelicans, wood storks, bald eagles, red-cockaded woodpeckers, American crocodiles, Florida black bears (\"Ursus americanus floridanus\") and Big Cypress fox squirrels (\"Sciurus niger avicennia\") also inhabit the park.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qb632861196",
  "kind": "yes/no",
  "text": "Claim: Judy Hample is a former chancellor of this educational organization. The organization and State University System of this state, for which Elwyn Thomas was a the Florida Board of Control from 1938 to 1969, have the United States in common.\n\nPassages:\n\n[Elwyn Thomas]\nElwyn Thomas (July 5, 1894 – February 15, 1971) was a Florida judge, and a Justice of the Florida Supreme Court from 1938 to 1969.\n\n[Judy Hample]\nShe is the former chancellor of the Pennsylvania State System of Higher Education and the Florida Board of Regents.\n\n[Florida Board of Regents]\nThe Florida Board of Regents was from 1965 to 2001 the governing body for the State University System of Florida, which includes all public universities in the state of Florida, United States.\n\n[State University System of Florida]\nThe State University System of Florida (SUS, or SUSF out-of-state) is a system of twelve public universities in the U.S. state of Florida.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q2f85237cb4",
  "kind": "yes/no",
  "text": "Claim: The Yule goat, which has become more or less conflated with Santa Claus, is a Finnish 2007 figure that has modern representations typically made of straw.\n\nPassages:\n\n[Yule Goat]\nThe Yule goat is a Scandinavian and Northern European Yule and Christmas symbol and tradition. Modern representations of the Yule goat are typically made of straw.\n\n[Joulupukki]\nJoulupukki is a Finnish Christmas figure. An old Scandinavian custom, the figure eventually became more or less conflated with Santa Claus.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q2fefc338df",
  "kind": "yes/no",
  "text": "Claim: On November 2, 2010, John Spratt lost to an AMerican politician who served in the South Carolina General Assembly from 2007 until 2011.\n\nPassages:\n\n[Mick Mulvaney]\nJohn Michael Mulvaney ( ; born July 21, 1967) is an American politician in the Republican Party and Director of the Office of Management and Budget (OMB). Mulvaney served in the South Carolina General Assembly from 2007–2011, first in the State House of Representatives and then the State Senate.\n\n[John Spratt]\nOn November 2, 2010, he lost to Republican challenger Mick Mulvaney.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9f7f1c6c92",
  "kind": "yes/no",
  "text": "Claim: The name of the 5th studio album of the artist Khia is Love Locs, it failed to chart on released and resulted in her being dropped by Warner Records.\n\nPassages:\n\n[Love Locs]\nLove Locs is the fifth studio album by American Hip Hop artist Khia and was released digitally on July 4, 2014 on her own label Thug Misses Entertainment.\n\n[Khia]\nKhia Shamone Finch ( ; born Khia Shamone Chambers, November 8, 1970), better known as just Khia, is an American rapper, songwriter, singer, and record producer.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q57392a9785",
  "kind": "yes/no",
  "text": "Claim: Ames–Florida House was built in 1856 in a US city between New York and Alberta Canada. This city was the most effected during the era in which Deicke and Millbrig bentonite layerswere formed.\n\nPassages:\n\n[Taconic orogeny]\nThe Taconic orogeny was a mountain building period that ended 440 million years ago and affected most of modern-day New England.\n\n[Deicke and Millbrig bentonite layers]\nThe Deicke and Millbrig bentonite layers, specifically the potassium bentonite layer, \"K-bentonite\", were formed from a volcanic eruption during the Taconic orogeny during the Late Ordovician on Laurentia, the craton of North America.\n\n[Ames–Florida House]\nThe house was built in 1856 by New England immigrants George F. Ames and his brother-in-law Joel Florida.\n\n[Queenston Delta]\nThe wedge is thickest in a band running from New York State to Quebec and extends from the Catskill mountains to Lake Huron.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qbc022c8466",
  "kind": "yes/no",
  "text": "Claim: Jane's Addiction and Weeping Willows, play the rock genre of music.\n\nPassages:\n\n[Jane's Addiction]\nJane's Addiction is an American rock band from Los Angeles, formed in 1985.\n\n[Weeping Willows]\nWeeping Willows is a Swedish indie rock group that started in 1995.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q7a2cf9b69a",
  "kind": "yes/no",
  "text": "Claim: Ron Lancaster was the starting quarterback for the winning team at a tournament in 1966. The MVP of this tournament was, along with Drake University player Johnny D. Bright, one of the greatest running backs in CFL history.\n\nPassages:\n\n[54th Grey Cup]\nGeorge Reed was the MVP with 31 rushes for 133 yards and one rushing touchdown.\n\n[Ron Lancaster]\nAs the starting quarterback for the Saskatchewan Roughriders for 16 seasons, he led the team to its first Grey Cup championship in 1966 and is the franchise's all-time leader in passing yards, attempts, completions, touchdowns, and interceptions.\n\n[George Reed (Canadian football)]\nReed, along with Mike Pringle and Johnny Bright, is one of the players most often mentioned as being the greatest running back in CFL history.\n\n[Johnny Bright]\nJohnny D. Bright (June 11, 1930 – December 14, 1983) was a professional Canadian football player in the Canadian Football League. He played college football at Drake University.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa29ca76e03",
  "kind": "yes/no",
  "text": "Claim: The star of the 1987 film Loha's maternal grandfather delivered Shakespeare performances.\n\nPassages:\n\n[Karan Kapoor]\nHis maternal grandparents, Geoffrey Kendal and Laura Kendal, were actors who toured India and Asia with their theatre group, Shakespeareana, performing Shakespeare and Shaw.\n\n[Loha (1987 film)]\nIt stars Dharmendra, Shatrughan Sinha, Karan Kapoor, Madhavi, Mandakini and Amrish Puri.\n\n[Geoffrey Kendal]\nGeoffrey Kendal (7 September 1909 – 14 May 1998) was an English actor-manager who delivered Shakespeare performances throughout India in the 1940s and 1950s.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q5e7086531b",
  "kind": "yes/no",
  "text": "Claim: The 1974–75 Philadelphia Flyers, an entirely Canadian-born team, scored 4 points in the 1975 Stanley Cup held during July.\n\nPassages:\n\n[1974–75 Philadelphia Flyers season]\nThe 1974–75 Philadelphia Flyers season was the Philadelphia Flyers eighth season in the National Hockey League (NHL). The 1974–75 Flyers were the last Stanley Cup champion to be composed entirely of Canadian-born players.\n\n[1974–75 Buffalo Sabres season]\nThe Sabres lost the series 4–2.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q6a1d57f4ad",
  "kind": "yes/no",
  "text": "Post: watching twilight with sam and i cannot wait to see his reaction to animatronic renesmee baby",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "q5d17482497",
  "kind": "yes/no",
  "text": "Claim: Mackenzie Davis appeared in the 2013 Canadian romantic comedy film directed Michael Dowse.\n\nPassages:\n\n[Mackenzie Davis]\nShe made her film debut in \"Smashed\", and later appeared in \"Breathe In\", \"That Awkward Moment\", and \"The F Word\", the latter for which she received a Canadian Screen Award nomination.\n\n[The F Word (2013 film)]\nis a 2013 Canadian romantic comedy film directed by Michael Dowse and written by Elan Mastai, based on TJ Dawe and Michael Rinaldi's play \"Toothpaste and Cigars\".",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q4aef00217e",
  "kind": "yes/no",
  "text": "Claim: A performer in the Broadway Dance Center acted in Hit the Floor. It was originally title Bounce.\n\nPassages:\n\n[Hit the Floor (TV series)]\nHit the Floor, originally titled Bounce, is an American sports drama television series on VH1 series, created by James LaRosa.\n\n[Katherine Bailess]\nKatherine Bailess (born April 24, 1980) is an American actress, singer, and dancer best known for playing the role of Erica Marsh on the CW's hit show \"One Tree Hill\", Life and Death Brigade member Stephanie on \"Gilmore Girls\", and Kyle Hart on the VH1 series \"Hit the Floor\".\n\n[Broadway Dance Center]\nDancers and performers such as Bette Middler, Brooke Shields, Britney Spears, Madonna, *NSYNC, Katherine Bailess, Jason Samuels Smith, Almamy and Elizabeth Berkley have taken class or rehearsed at the school and many Broadway performers take class there daily.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qa272e04866",
  "kind": "yes/no",
  "text": "Claim: John Stoltenberg is not the managing editor of the magazine that focuses on aging issues.\n\nPassages:\n\n[AARP The Magazine]\nAARP The Magazine is an American bi-monthly magazine, published by the American Association of Retired People, AARP, which focuses on aging issues.\n\n[John Stoltenberg]\nHe is the former managing editor of \"AARP The Magazine\", a bimonthly publication of the United States-based advocacy group AARP, a position he held from 2004 until 2012.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q216d0d8f94",
  "kind": "yes/no",
  "text": "Claim: The actor that played Gutthi on Comedy nights with Kapil Show also starred in Vaisakhi List, the 2016 Punjabi film directed by Smeep Kang.\n\nPassages:\n\n[Sunil Grover]\nSunil Grover (born 3 August 1977) is an Indian actor and stand-up comedian He has acted in many comedy shows but gained popularity on the Comedy nights with Kapil Show, for his portrayal of a character called Gutthi.\n\n[Vaisakhi List]\nVaisakhi List (Punjabi: ਵਿਸਾਖੀ ਲਿਸਟ ) is a 2016 Punjabi film directed by Smeep Kang and starring Jimmy Shergill, Shruti Sodhi and Sunil Grover as the main cast and the film was released on 22 April 2016.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "qe5da632317",
  "kind": "yes/no",
  "text": "Claim: Georgia Totto O'Keeffe painted the sets of watercolors that she made exploring a monochromatic palette with designs that were non-representational of specific objects, and was best known for her paintings of enlarged flowers and.portraits.\n\nPassages:\n\n[Georgia O'Keeffe]\nGeorgia Totto O'Keeffe (November 15, 1887 – March 6, 1986) was an American artist. She was best known for her paintings of enlarged flowers, New York skyscrapers, and New Mexico landscapes.\n\n[Blue (O'Keeffe series)]\nIt was one of the sets of watercolors that she made exploring a monochromatic palette with designs that were non-representational of specific objects.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qde63110f72",
  "kind": "yes/no",
  "text": "Claim: The team in the 2013 Alamo Bowl was not led by former American football coach Mark August Helfrich who is currently a college football analyst for Fox Sports.\n\nPassages:\n\n[2013 Alamo Bowl]\nThe 21st edition of the Alamo Bowl, it featured the Texas Longhorns from the Big 12 Conference and the Oregon Ducks from the Pac-12 Conference.\n\n[2013 Oregon Ducks football team]\nThe team was led by first year head coach Mark Helfrich and played their home games at Autzen Stadium for the 47th consecutive year.\n\n[Mark Helfrich (American football)]\nMark August Helfrich (born October 28, 1973) is a former American football coach and is currently a college football analyst for Fox Sports.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qed5ba628fd",
  "kind": "yes/no",
  "text": "Claim: The San Quentin Six were six inmates at the maximum-security San Quentin State Prison in the U.S. state of California, who were accused of participating in an escape attempt, on August 21, 1971, that left six people dead, including George Jackson, a co-founder of the Black Guerrilla Family.\n\nPassages:\n\n[Black Guerrilla Family]\nThe Black Guerilla Family, or BGF (also known as the Black Family or the Black Vanguard) is an African-American prison and street gang founded in 1966 by George Jackson and W.L. Nolen while they were incarcerated at San Quentin State Prison in Marin County, California.\n\n[San Quentin Six]\nThe San Quentin Six were six inmates at San Quentin State Prison in the U.S. state of California (Hugo Pinell, Willie Tate, Johnny Larry Spain, David Johnson, Fleeta Drumgo and Luis Talamantez), who were accused of participating in an August 21, 1971 escape attempt that left six people dead, including George Jackson, a co-founder of the Black Guerrilla Family.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc62d31c09e",
  "kind": "yes/no",
  "text": "Claim: Jhené Aiko is an American singer who appeared in music videos for R&B group B2K and also featured on the 2010 mixtape by American rapper Big Sean. The Olympicks helped produce the mixtape.\n\nPassages:\n\n[Jhené Aiko]\nShe embarked on her music career contributing vocals and appearing in several music videos for R&B group B2K.\n\n[The Olympicks]\nThe group originated in Detroit, Michigan and have been involved in the production of various projects within the hip-hop music industry, including Lil Wayne's \"I Am Not a Human Being\", Rick Ross' \"Teflon Don\", Triple C's \"Custom Cars & Cycles\", DJ Khaled's \"Kiss The Ring\", and most recently, Big Sean's \"Detroit\" mixtape.\n\n[Detroit (mixtape)]\nAmerican singers includes Chris Brown, Jhené Aiko, James Fauntleroy and Mike Posner.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q0d1001298f",
  "kind": "yes/no",
  "text": "Tweet: so like does anyone even remember what happened in september",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qa7623225a4",
  "kind": "yes/no",
  "text": "Claim: The NASDAQ ticker code for Spirit Airlines, based at Detroit Metro Airport among others and an ultra low cost carrier is SAVE.\n\nPassages:\n\n[Detroit Metropolitan Airport]\nDetroit Metropolitan Wayne County Airport (IATA: DTW, ICAO: KDTW, FAA LID: DTW) , usually called Detroit Metro Airport, Metro Airport, or just DTW, is a major international airport in the United States covering 4,850 acre in Romulus, Michigan, a suburb of Detroit.\n\n[Spirit Airlines]\nSpirit Airlines, Inc. (NASDAQ: SAVE ) is an American Ultra Low Cost Carrier, headquartered in Miramar, Florida. The airline operates bases at Atlantic City, Chicago–O'Hare, Dallas/Fort Worth, Detroit, Fort Lauderdale and Las Vegas as of 2015 .",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qf5f2f307b2",
  "kind": "yes/no",
  "text": "Claim: Barry Unsworth is from the same country as P. G. Wodehouse.\n\nPassages:\n\n[Barry Unsworth]\nUnsworth was born on 10 August 1930 in Wingate, a mining village in County Durham, England, to a family of miners.\n\n[P. G. Wodehouse]\nSir Pelham Grenville Wodehouse {'1': \", '2': \", '3': \", '4': \"} ( ; 15 October 188114 February 1975) was an English author and one of the most widely read humorists of the 20th century.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q3035e1a546",
  "kind": "yes/no",
  "text": "Claim: Pravda and Stiffelio are not both operas.\n\nPassages:\n\n[Stiffelio]\nStiffelio is an opera in three acts by Giuseppe Verdi, from an Italian libretto by Francesco Maria Piave.\n\n[Pravda]\nPravda (Russian: Правда ; ] , \"Truth\") is a Russian broadsheet newspaper, formerly the official newspaper of the Communist Party of the Soviet Union, when it was one of the most influential papers in the country with a circulation of 11 million.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q6d7ac292dc",
  "kind": "yes/no",
  "text": "Claim: In between the husband of Nora Balling and Micky Dolenz, George Michael Dolenz was the a member of the Monkees.\n\nPassages:\n\n[Nora Balling]\nNora-Isabelle Balling, also known as Nora Anders (born July 31, 1964, Koblenz, Germany) is a German fashion model, and was the first wife of the singer and former Modern Talking member, Thomas Anders, between 1984 and 1999.\n\n[Thomas Anders]\nThomas Anders (born Bernd Weidung, 1 March 1963) is a German singer, composer, and record producer.\n\n[Micky Dolenz]\nGeorge Michael Dolenz, Jr. (born March 8, 1945) is an American actor, musician, television director, radio personality and theater director, best known as a vocalist and drummer of the 1960s pop/rock band the Monkees.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc408f740a6",
  "kind": "yes/no",
  "text": "Tweet: The amount of times I had to present my intern badge to Capitol Police officers who saw me every day for months and these people are just breaking in like it’s nothing smh",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qb0b5b88120",
  "kind": "yes/no",
  "text": "Claim: The Canadian Province of Nova Scotia was captured with the support of the Mi'kmaq, Maliseet, Passamaquoddy, Abenaki, and APTN National News.\n\nPassages:\n\n[Wabanaki Confederacy]\nThe Wabanaki Confederacy (\"Wabenaki, Wobanaki\", translated roughly as \"People of the First Light\" or \"People of the Dawnland\") are a First Nations and Native American confederation of five principal nations: the Mi'kmaq, Maliseet, Passamaquoddy, Abenaki, and Penobscot.\n\n[Siege of Port Royal (1710)]\nThe successful British siege marked the beginning of permanent British control over the peninsular portion of Acadia, which they renamed Nova Scotia, and it was the first time the British took and held a French colonial possession.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q84f9538cb6",
  "kind": "yes/no",
  "text": "Claim: One of the legendary four aces skaters was born in the third largest city in a country. Leif Jenssen is from this country. The others were Ostrava, Amund Sjøbrend and Kay Stenshjemmet.\n\nPassages:\n\n[Sten Stensen]\nTogether with Amund Sjøbrend, Kay Stenshjemmet, and Jan Egil Storholt, he was one of the legendary \"four S-es\" (\"four aces\" in Norwegian), contemporary Norwegian top skaters in the 1970s and early 1980s.\n\n[Trondheim]\nIt is the third largest city in the country, with a population (2013) of 169,972 inhabitants within the city borders.\n\n[Leif Jenssen]\nLeif Jenssen (born March 19, 1948) is a former Norwegian weightlifter.\n\n[Jan Egil Storholt]\nJan Egil Storholt (born 13 February 1949) is a former speed skater from Norway. He was born in Trondheim.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q20365b0f94",
  "kind": "yes/no",
  "text": "Claim: Lou Cutell appeared on the third episode of the ninth season of an CBS sitcom that was the 187th episode overall.\n\nPassages:\n\n[Lou Cutell]\nLou Cutell (born October 6, 1930) is an American movie and television actor. In 2013, he appeared on the \"How I Met Your Mother\" episode \"Last Time in New York\".\n\n[Last Time in New York]\n\"Last Time in New York\" is the third episode of the ninth season of the CBS sitcom \"How I Met Your Mother\", and the 187th episode overall.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q70c848260f",
  "kind": "yes/no",
  "text": "Claim: Live has more members than the English band whose second album is called Sweet Sour.\n\nPassages:\n\n[Sweet Sour]\nSweet Sour is the second album by English rock band Band of Skulls.\n\n[Live (band)]\nLive ( , often typeset as LĪVE or +LĪVE+) is an American rock band from York, Pennsylvania, consisting of Ed Kowalczyk (lead vocals, rhythm guitar), Chad Taylor (lead guitar, backing vocals), Patrick Dahlheimer (bass), and Chad Gracey (drums).\n\n[Band of Skulls]\nBand of Skulls are an English rock band from Southampton, consisting of Russell Marsden (guitar, vocals), Emma Richardson (bass, vocals), and Matt Hayward (drums).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q3f99899f8d",
  "kind": "yes/no",
  "text": "Tweet: Wtf is a Justin Herbert",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qa6a82344df",
  "kind": "yes/no",
  "text": "Text: \"@elliekonsker: FLORIDA YOU LITERALLY HAVE ONE JOB\"",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q6a2ae925e1",
  "kind": "yes/no",
  "text": "Claim: The magazine that ranked Lifted Research Group at #5 on its Hot 500 list of fastest-growing companies had a longer lifespan than Optimize.\n\nPassages:\n\n[Lifted Research Group]\nEntrepreneur\" magazine ranked the company at #5 on its 2007 Hot 500 list of fastest-growing companies.\n\n[Entrepreneur (magazine)]\nEntrepreneur is an American magazine and website that carries news stories about entrepreneurship, small business management, and business. The magazine was first published in 1977. The magazine publishes 12 issues annually, available through subscription and on newsstands.\n\n[Optimize (magazine)]\nOptimize was an American monthly business magazine published between November 2001 and June 2007.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc0aaf18c61",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "6 more hours and then a whoppingly massive 2days off work! wowzers!",
   "I only have a measly 2 days off work."
  ]
 },
 {
  "qid": "qf986fc2c84",
  "kind": "yes/no",
  "text": "Text: I just heard my voice in a video and I never want to speak again",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q9bb4932e21",
  "kind": "yes/no",
  "text": "Text: victini is my favorite pokemon",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "qbccc3e6a65",
  "kind": "yes/no",
  "text": "Claim: The British fashion and lifestyle publication, for whom Rachel Egglestone-Evans is editor, and InStyle are not both US-based magazines.\n\nPassages:\n\n[Rachel Egglestone-Evans]\nRachel 'Rae' Evans (born 6 September 1980 in Congleton, Cheshire, England) is the editor of Vintage Life Magazine, a British publication focusing on vintage fashion and lifestyle from the 1920s to the 1970s.\n\n[InStyle]\nInStyle is a monthly women’s fashion magazine published in the US by Time Inc. \"InStyle\" was founded in 1994.\n\n[Vintage Life]\nVintage Life is a British glossy fashion and lifestyle magazine, published by Dragoon Publishing, focusing on the 1920s-1970s.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q71fa04683b",
  "kind": "yes/no",
  "text": "Claim: South Somercotes is a village and civil parish 8 mi north-east from Louth and approximately 2 mi south from the remote coastal village of North Somercotes in the East Lindsey district, and the Marshes area, of Lincolnshire, England.\n\nPassages:\n\n[North Somercotes]\nNorth Somercotes is a coastal village in the East Lindsey district, and the Marshes area, of Lincolnshire, England.\n\n[South Somercotes]\nSouth Somercotes is a village and civil parish 8 mi north-east from Louth and approximately 2 mi south from North Somercotes, Lincolnshire, England.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 }
]
