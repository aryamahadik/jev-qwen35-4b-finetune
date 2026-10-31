# A46 replay label-noise blind read RSAS05-blind_read-537c9c01-006

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS05-blind_read-537c9c01-006.json

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
  "qid": "qa7734c61bb",
  "kind": "yes/no",
  "text": "Claim: During the period known as the Second Red Scare, Alexander Trachtenberg was convicted under the Smith Act.\n\nPassages:\n\n[Alexander Trachtenberg]\nDuring the period of McCarthyism in America, Trachtenberg was twice subject to prosecution and convicted under the Smith Act; the convictions were overturned, the first by recanting of a government witness and the second by a US Circuit Court of Appeals decision in 1958.\n\n[McCarthyism]\nThe term refers to U.S. Senator Joseph McCarthy and has its origins in the period in the United States known as the Second Red Scare, lasting roughly from 1947 to 1956 and characterized by heightened political repression as well as a campaign spreading fear of influence on American institutions and of espionage by Soviet agents.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qfef492af45",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which text is sarcastic?",
  "options": [
   "I just love falling up the stairs 😑",
   "I really don't like falling up the stairs."
  ]
 },
 {
  "qid": "q55cb9f1ee7",
  "kind": "yes/no",
  "text": "Text: now that I’m working in the commercial talent business, I can’t help but wonder how much Jake from State Farm gets paid. I think about it every time I see a SF commercial",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the words carry the author's real message at face value; there is no mockery, irony or false praise."
 },
 {
  "qid": "qeae96719d1",
  "kind": "yes/no",
  "text": "Text: Nothing warms my heart more than seeing everybody come together and attack Westside’s administration ❤️ #WycoPride #YeeYee",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q5a04741ddd",
  "kind": "yes/no",
  "text": "Claim: The Garrick Club is a gentlemen's club in the heart of London founded in May 1831, since its conception has catered to members such as English actor and theatre manager Sir Herbert Beerbohm Tree, that died on 2 July 1917.\n\nPassages:\n\n[Garrick Club]\nIt is one of the oldest, most highly esteemed and most exclusive members' clubs in the world and since its conception has catered to members such as Charles Kean, Henry Irving, Herbert Beerbohm Tree, Arthur Sullivan, Laurence Olivier and John Gielgud.\n\n[Herbert Beerbohm Tree]\nSir Herbert Beerbohm Tree (17 December 1852 – 2 July 1917) was an English actor and theatre manager.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q566bd52d95",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "Twisted Teas are the best.",
   "No joke, air-fried Twisted Teas are THE BEST."
  ]
 },
 {
  "qid": "qafe6947f3e",
  "kind": "yes/no",
  "text": "Claim: Talking Smack is an American, drama talk show whose past hosts have included the current Intercontinental Champion in his seventh reign.\n\nPassages:\n\n[The Miz]\nMichael Gregory Mizanin (born October 8, 1980) is an American professional wrestler, reality television star, and actor. He is signed to WWE, where he performs on the Raw brand under the ring name The Miz and is the current Intercontinental Champion in his seventh reign.\n\n[WWE Talking Smack]\nTalking Smack is an American talk show produced by WWE and currently airing on their subscription based streaming service, the WWE Network. Past hosts have included Daniel Bryan, Shane McMahon, The Miz and Jerry Lawler.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qaf6c98a967",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "I really do not like the walk past first class to get to my coach seat.",
   "My favorite part of flying is getting to walk past the rich people to get to my poor person seat."
  ]
 },
 {
  "qid": "qb7ce53c408",
  "kind": "yes/no",
  "text": "Claim: The actor who starred in the 1965 film Frankenstein Meets the Space Monster also appeared on the third episode of the ninth season of a sitcom that was the 187th episode overall.\n\nPassages:\n\n[Frankenstein Meets the Space Monster]\nFrankenstein Meets the Space Monster (sometimes stylized as Frankenstein Meets the Spacemonster) (1965) is a science fiction cult film, directed by Robert Gaffney and starring Marilyn Hanold, James Karen, and Lou Cutell.\n\n[Lou Cutell]\nLou Cutell (born October 6, 1930) is an American movie and television actor. In 2013, he appeared on the \"How I Met Your Mother\" episode \"Last Time in New York\".\n\n[Last Time in New York]\n\"Last Time in New York\" is the third episode of the ninth season of the CBS sitcom \"How I Met Your Mother\", and the 187th episode overall.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q33875bff3c",
  "kind": "yes/no",
  "text": "Claim: Sophia Grace & Rosie featured a cover song on their Youtube channel. The song from is from an album released under the Columbia Records and Columbia Records labels.\n\nPassages:\n\n[Glory Days (Little Mix album)]\nIt was released on 18 November 2016, by Syco Music and Columbia Records.\n\n[Touch (Little Mix song)]\n\"Touch\" is a song by British girl group Little Mix. It was released as the second single from their studio album \"Glory Days\".\n\n[Sophia Grace &amp; Rosie]\nRosie has started a YouTube channel featuring her life and sang a cover of Little Mix's \"Touch\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q9c2a0e8bf7",
  "kind": "yes/no",
  "text": "Claim: The public research university which Ottey spent several years in the 1990's coaching in is located in El Paso, Texas, United States.\n\nPassages:\n\n[Milton Ottey]\nHe received a full athletic scholarship from the University of Texas El Paso, where he received his bachelor's degree in education.After retiring from active competition Ottey spent several years coaching in various universities throughout the United States, including University of Texas at El Paso (UTEP), Kent State University and University of New Mexico before moving back to Toronto.\n\n[University of Texas at El Paso]\nThe University of Texas at El Paso (UTEP) is a public research university in El Paso, Texas, United States.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q874c1a5e5a",
  "kind": "yes/no",
  "text": "Claim: Danyang, Jiangusu and this city are both cities in China. This city was the birthplace of Chen Xiuke.\n\nPassages:\n\n[Dongfang, Hainan]\nDōngfāng () is one of the seven county-level cities of Hainan province, China.\n\n[Chen Xiuke]\nChen Xiuke (born 31 December 1976 in Dongfang, Hainan) is a male Chinese sports sailor.\n\n[Danyang, Jiangsu]\nDanyang () is a county-level city under the administration of Zhenjiang, Jiangsu province, China.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qe4066c8970",
  "kind": "yes/no",
  "text": "Claim: Live While We're Young is by the English-Irish boy band Westlife who relocated to London.\n\nPassages:\n\n[Live While We're Young]\n\"Live While We're Young\" is a song by English-Irish boy band One Direction, released as the lead single from their second studio album, \"Take Me Home\" (2012).\n\n[One Direction]\nOne Direction (commonly abbreviated as 1D) are an English-Irish pop boy band based in London, composed of Niall Horan, Liam Payne, Harry Styles, Louis Tomlinson, and previously, Zayn Malik until his departure from the band on 25 March 2015.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa9fcc351c9",
  "kind": "choice",
  "text": "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "You didn't watch Varane last season, if you did, you would have a different opinion.",
   "@abhiishekkkkkk @FCBGox Did you even watch a single la Liga madrid game last season bruh Varane isn’t that good anymore"
  ]
 },
 {
  "qid": "qbd44439e5b",
  "kind": "yes/no",
  "text": "Claim: Matt Miller (musician) plays bass in a Post-hardcore band. This band and King Charles are not both from the same country.\n\nPassages:\n\n[King Charles (musician)]\nKing Charles (born Charles Costa, 6 May 1985) is a singer-songwriter from West London.\n\n[Sparta (band)]\nSparta is an American rock band from El Paso, Texas, formed in 2001.\n\n[Matt Miller (musician)]\nMatt Miller is a native of El Paso, Texas and the bassist for the Post-hardcore band, Sparta.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qa4f84dbfcd",
  "kind": "yes/no",
  "text": "Claim: The 1985 film of which Wild Search is a pseudo-remake is a country Asian film. Straight from the Heart (2003 film) is based in the romance novel by this american writer.\n\nPassages:\n\n[Pamela Wallace]\nPamela Wallace (born 1949 in Exeter, California) is an American screenwriter and author.\n\n[Witness (1985 film)]\nWitness is a 1985 American crime thriller film directed by Peter Weir and starring Harrison Ford and Kelly McGillis.\n\n[Straight from the Heart (2003 film)]\nIt is based on the romance novel by Pamela Wallace.\n\n[Wild Search]\nThe film is a pseudo-remake of the 1985 film \"Witness\" and deals with Hong Kong cops and Mainland criminals.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qac13fe59ab",
  "kind": "yes/no",
  "text": "Post: there was a bee in my house yesterday and i haven’t seen it since i hope it died",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "qf48c171fb1",
  "kind": "yes/no",
  "text": "Text: \"your pronouns are what's in your pants\" ok. juicy/dumper",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qd9071bea24",
  "kind": "yes/no",
  "text": "Claim: Operation Clarion attacked 200 Cubists communication network targets to open a campaign. This campaign was later than the one where The Battle of Fort Driant was a constituent battle in the 1944 Battle of Metz.\n\nPassages:\n\n[Operation Clarion]\nOperation Clarion was the extensive Allied campaign of Strategic bombing during World War II which attacked 200 German communication network targets to open Operation Veritable/Grenade.\n\n[Battle of Fort Driant]\nThe Battle of Fort Driant was a constituent battle in the 1944 Battle of Metz, during the Lorraine Campaign and the greater Siegfried Line Campaign.\n\n[Operation Grenade]\nDuring World War II, Operation Grenade was the crossing of the Roer (Rur) river between Roermond and Düren by the U.S. Ninth Army, commanded by Lieutenant General William Hood Simpson, in February 1945.\n\n[Lorraine Campaign]\nLorraine Campaign is a term used by U.S. Army historians to describe operations of the U.S. Third Army in Lorraine during World War II from September 1 through December 18, 1944.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q28898bfcf6",
  "kind": "yes/no",
  "text": "Post: #DominicCummings Sack him. Or better yet, charge him.",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "q33747d8f6a",
  "kind": "yes/no",
  "text": "Claim: The magazine for which James P. Comer has written more than 150 articles, and Madame Figaro are published in the same country.\n\nPassages:\n\n[James P. Comer]\nHe has also written more than 150 articles for Parents (magazine) and more than 300 articles on children's health and development and race relations.\n\n[Parents (magazine)]\nParents, published by Meredith Corporation, is an American mass circulation monthly magazine that features scientific information on child development geared to help parents in raising their children.\n\n[Madame Figaro]\nMadame Figaro is a French magazine supplement to the Saturday edition of the daily newspaper \"Le Figaro\", focusing on and catering to women.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q86170f09b4",
  "kind": "yes/no",
  "text": "Claim: The younger brother of football players Shola and Tomi Ameobi was born in a city that has the regional dialect which has the nickname Geordie.\n\nPassages:\n\n[Tomi Ameobi]\nOluwatomiwo \"Tomi\" Ameobi (born 16 August 1988) is an English footballer who plays as a forward for FC Edmonton. He was born in Newcastle upon Tyne, Tyne and Wear.\n\n[Newcastle upon Tyne]\nThe regional nickname and dialect for people from Newcastle and the surrounding area is Geordie.\n\n[Sammy Ameobi]\nHe is the younger brother of fellow players Shola and Tomi Ameobi.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qd1d5b8efe8",
  "kind": "yes/no",
  "text": "Claim: H. H. Holmes is the name of the American serial killer of the 19th century on which the 1974 psychological horror novel by Robert Bloch is based and whom murdered a total 27 people.\n\nPassages:\n\n[American Gothic (novel)]\nAmerican Gothic is a 1974 psychological horror novel by American writer Robert Bloch, a fictionalized portrayal of real life serial killer H. H. Holmes, who is renamed \"G. Gordon Gregg\" for the story.\n\n[H. H. Holmes]\nHerman Webster Mudgett (May 16, 1861 – May 7, 1896), better known under the name of Dr. Henry Howard Holmes or more commonly H. H. Holmes, was an American serial killer of the 19th century.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qb330e7863a",
  "kind": "yes/no",
  "text": "Claim: Gérard Depardieu was the lead french actor who starred in the 1986 film that inspired a Stella Artois ad campaign.\n\nPassages:\n\n[Reassuringly Expensive]\nReassuringly Expensive was the Stella Artois' advertising slogan in the United Kingdom from 1982 until 2007.\n\n[Jean de Florette]\nThe film starred three of France's most prominent actors – Gérard Depardieu, Daniel Auteuil, who won a BAFTA award for his performance, and Yves Montand in one of his last roles before his death.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q476fb5c01a",
  "kind": "yes/no",
  "text": "Claim: The director of the 1923 film April Showers is Chilean. Arturo Ripstein is not Chilean.\n\nPassages:\n\n[April Showers (1923 film)]\nApril Showers is a 1923 American silent romantic film directed by Tom Forman starring Colleen Moore.\n\n[Arturo Ripstein]\nArturo Ripstein y Rosen (born December 13, 1943) is a Mexican film director.\n\n[Tom Forman (actor)]\nTom Forman (February 22, 1893 – November 7, 1926) was an American motion picture actor, director, writer, and producer of the early 1920s.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q8c1a5d19a2",
  "kind": "yes/no",
  "text": "Claim: Unchained Memories was the documentary made before filmmaker Tigre Hill's first documentary.\n\nPassages:\n\n[The Shame of a City]\nThe Shame of a City is a 2006 feature-length documentary, which premiered at the Philadelphia Film Festival.\n\n[Tigre Hill]\nHe is perhaps best known for his first documentary, \"The Shame of a City\".\n\n[Unchained Memories]\nUnchained Memories is a 2003 documentary film about the stories of former slaves interviewed during the 1930s as part of the Federal Writers' Project and preserved in the WPA Slave Narrative Collection.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qaa293a0f9a",
  "kind": "yes/no",
  "text": "Claim: Oumar Tchomogo was born in 1986 in Cotonou, in Benin.\n\nPassages:\n\n[Cotonou]\nCotonou (] ), is the largest city and economic centre of Benin.\n\n[Oumar Tchomogo]\nOumar Tchomogo (born 7 January 1978 in Cotonou) is a Beninese footballer who plays as a forward for Rhône-Alpes Honneur Regional Ligue side Union Montilienne Sportive Football.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qe23c128938",
  "kind": "yes/no",
  "text": "Text: I've been doing physics for 40 minutes I think I deserve a break 😂😂😂😭 I'm never going to get it all done at this rate",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qfc000fdcaa",
  "kind": "yes/no",
  "text": "Claim: The Landsman Kill is a body of water. It's near the road that intersects State Route 199 at Rock City in the state where Robert F. Kennedy was a junior senator.\n\nPassages:\n\n[Rock City, New York]\nIt is located at the intersection of New York State Route 199 and Route 308, where the towns of Milan, Red Hook and Rhinebeck meet.\n\n[Robert F. Kennedy]\nHe served as the United States junior senator from New York from January 1965 until his assassination in June 1968.\n\n[Kill (body of water)]\nAs a body of water, a kill is a creek.\n\n[New York State Route 308]\nThe highway passes near the Dutchess County Fairgrounds, several historical landmarks, and the Landsman Kill.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "qa9275cef83",
  "kind": "yes/no",
  "text": "Post: i want to go back to last year when i properly discovered kpop and it was so fun and exciting💔",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q756ed0cfa2",
  "kind": "yes/no",
  "text": "Claim: The poet, for whom Darragh Park was the literary executor of his estate, publisehed books. The author of 'Love and Mr Lewisham' also published books.\n\nPassages:\n\n[H. G. Wells]\nHis most notable science fiction works include \"The Time Machine\" (1895), \"The Island of Doctor Moreau\" (1896), \"The Invisible Man\" (1897), and \"The War of the Worlds\" (1898).\n\n[Darragh Park]\nDarragh Park (July 24, 1939 – April 17, 2009) was an American Artist, and the literary executor of the estate of Pulitzer Prize–winning poet James Schuyler.\n\n[Love and Mr Lewisham]\nLove and Mr Lewisham (subtitled \"The Story of a Very Young Couple\") is a 1900 novel set in the 1880s by H. G. Wells.\n\n[James Schuyler]\nHis awards include the Pulitzer Prize for Poetry for his 1980 collection \"The Morning of the Poem\".",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q5eab759629",
  "kind": "yes/no",
  "text": "Tweet: was not aware that Crocs were appropriate business casual attire.",
  "question": "Would the author say they were being sarcastic here?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark."
 },
 {
  "qid": "qaa4eb4a619",
  "kind": "yes/no",
  "text": "Claim: The author of the semi-satirical novel The Foundation Pit died before John Masefield.\n\nPassages:\n\n[The Foundation Pit]\nThe Foundation Pit (Russian: Котлован, \"kotlovan\") is a gloomy symbolic and semi-satirical novel by Andrei Platonov.\n\n[John Masefield]\nJohn Edward Masefield, OM ( ; 1 June 1878 – 12 May 1967) English poet and writer, was Poet Laureate of the United Kingdom from 1930.\n\n[Andrei Platonov]\nAndrei Platonov (Russian: Андре́й Плато́нов , ] ; August 28 [O.S. August 16] 1899 – January 5, 1951) was the pen name of Andrei Platonovich Klimentov (Russian: Андре́й Плато́нович Климе́нтов ), a Soviet Russian writer, playwright, and poet, whose works anticipate existentialism.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qc50c896469",
  "kind": "yes/no",
  "text": "Claim: This \"Gearing\"-class destroyer was named after the first woman naval recipient of the Medal of Honor in World War II.\n\nPassages:\n\n[USS O'Hare (DD-889)]\nUSS \"O'Hare\" (DD/DDR-889) was a \"Gearing\"-class destroyer of the United States Navy, named for Lieutenant Commander Edward \"Butch\" O'Hare, Medal of Honor recipient, who was shot down at Tarawa on 27 November 1943.\n\n[Edward O'Hare]\nLieutenant Commander Edward Henry “Butch” O’Hare (March 13, 1914 – November 26, 1943) was an American naval aviator of the United States Navy, who on February 20, 1942, became the Navy's first flying ace when he single-handedly attacked a formation of nine heavy bombers approaching his aircraft carrier. On April 21, 1942, he became the first naval recipient of the Medal of Honor in World War II.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q9181c51996",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Which of the two texts is the sarcastic one?",
  "options": [
   "I would say \"Yeah, I never get why so people have the issue of maintaining eye contact, it's relatively easy for me to do.\"",
   "@kidcuisine98 Based confidence and believing in proper eye contact-pilled!"
  ]
 },
 {
  "qid": "q3223905500",
  "kind": "yes/no",
  "text": "Claim: Marty Stratton became responsible for the overall development of an award winning game. This award winning game is a reboot of the franchise developed by id Software.\n\nPassages:\n\n[2016 in video gaming]\nMany awards went to games such as \"Overwatch\", \"\", \"Inside\", \"Doom\", \"Dark Souls III\", \"The Last Guardian\", \"Dishonored 2\" and \"Titanfall 2\".\n\n[Doom (2016 video game)]\nA reboot of the \"Doom\" franchise, it is the fourth title in the main series and the first major installment since \"Doom 3\" in 2004.\n\n[Marty Stratton]\nIn 2006, he became responsible for the overall development of \"Quake Live\", \"Rage\", and \"Doom\" with ZeniMax Media and Bethesda Softworks respectively.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q6d8f322994",
  "kind": "yes/no",
  "text": "Claim: Robert Allen \"Bob\" Case is best known for inspiring the naming of 1991 Perfect Storm which ia an initial area of low pressure developed off Atlantic Canada on October 29.\n\nPassages:\n\n[1991 Perfect Storm]\nThe initial area of low pressure developed off Atlantic Canada on October 29.\n\n[Robert Case]\nHe is best known for inspiring the naming of the 1991 Perfect Storm as \"The Perfect Storm.\"",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "qa2fa0a9f5e",
  "kind": "yes/no",
  "text": "Claim: Alfred Döblin and César Vallejo were not both German nationals.\n\nPassages:\n\n[César Vallejo]\nCésar Abraham Vallejo Mendoza (March 16, 1892 – April 15, 1938) was a Peruvian poet, writer, playwright, and journalist.\n\n[Alfred Döblin]\nBruno Alfred Döblin (10 August 1878 – 26 June 1957) was a German novelist, essayist, and doctor, best known for his novel \"Berlin Alexanderplatz\" (1929).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q4124465231",
  "kind": "yes/no",
  "text": "Claim: The South Korean musician who sings \"Napal Baji\" is known domestically for his humorous videos and stage performances and released his sixth studio album in 2012\n\nPassages:\n\n[Psy]\nPark Jae-sang (Hangul: 박재상 ; Hanja: 朴載相 ; born December 31, 1977), known professionally as Psy (싸이 ; ; ] ), stylized PSY, is a South Korean singer, rapper, songwriter, and record producer. Psy is known domestically for his humorous videos and stage performances, and internationally for his hit single \"Gangnam Style\".\n\n[Gangnam Style]\n\"Gangnam Style\" (Korean: 강남스타일 , ] ) is the 18th K-pop single by the South Korean musician Psy. The song was released on July 15, 2012, as the lead single of his sixth studio album \"Psy 6 (Six Rules), Part 1\", and debuted at number one on South Korea's Gaon Chart.\n\n[Napal Baji]\n\"Napal Baji\" (; lit \"bell-bottoms\") is the 22nd K-pop single by the South Korean musician Psy.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qec40e9739b",
  "kind": "yes/no",
  "text": "Text: The best part of going out, is waking up at 2PM the next morning wondering whether you're dead or not and what day it is. 😂😳😀",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the text is literal in tone, even if it is negative, emotional or funny."
 },
 {
  "qid": "qa1e170ff79",
  "kind": "choice",
  "text": "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "Everytime i swipe through bumble when i’m bored i just get sad that no one has the same complex interests as me.",
   "everytime i swipe through bumble when i’m bored i just get sad that no one has the same complex interests as me….rude 😤🙄 /j"
  ]
 },
 {
  "qid": "q4e5545b03d",
  "kind": "yes/no",
  "text": "Claim: Archean Soundtrack are best known for their single \"Reach\", the music video of which was directed by Duncan Guymer, who oversaw the viral marketing videos for a new ride in Crystal Beach. There are eight steel roller coasters of the same type as the new ride in Crystal Beach that are currently operating worldwide.\n\nPassages:\n\n[Archean Soundtrack]\nArchean Soundtrack are best known for their single \"Reach\", the music video of which was directed by Duncan Guymer, who oversaw the viral marketing videos for Thorpe Park's new ride, \"The Swarm\".\n\n[The Swarm (roller coaster)]\nThe Swarm is a steel Wing Coaster at Thorpe Park, a theme park in the United Kingdom.\n\n[Wing Coaster]\nThere are currently eight Wing Coasters operating worldwide.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qd6b20ede6e",
  "kind": "yes/no",
  "text": "Claim: David Koepp scripted the television adaptation of a movie based off a script written in 1979 by Edwin Torres.\n\nPassages:\n\n[After Hours (novel)]\nAfter Hours is a 1979 American crime novel written by Edwin Torres and is the sequel to \"Carlito's Way\".\n\n[Carlito's Way]\nThe film adaptation was scripted by David Koepp.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc85250afaf",
  "kind": "yes/no",
  "text": "Claim: The Nirvana album that their song Sliver was rereleased on featured many artists. The list of artists includes The Vaselines, Dave Grohl, and Chad Channing.\n\nPassages:\n\n[Son of a Gun (EP)]\nSon of A Gun is the debut extended play single by Glasgow alternative rock group The Vaselines. The title-song of this EP came to a wider audience after Nirvana covered it, along with \"Molly's Lips\", on their compilation album \"Incesticide\".\n\n[Sliver (song)]\nDGC re-released the song to radio to support the release of the rarities compilation album \"Incesticide\" in 1992.\n\n[Incesticide]\nIncesticide is a compilation album by the American grunge band Nirvana. At the time, the majority of the material on \"Incesticide\" was circulating within fan communities (albeit in lower quality). Since the songs were recorded in different sessions and some were recorded when Nirvana did not have a stable formation, the album includes recordings by four different drummers: Chad Channing, Dan Peters, Dale Crover, and Dave Grohl.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q54e4fb9bd1",
  "kind": "yes/no",
  "text": "Text: thinking about when i told my old coworker i had a gf and she said i was ‘so brave’",
  "question": "Does the author mean this sarcastically?",
  "definitions": "- yes: the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.\n- no: the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks."
 },
 {
  "qid": "q1d76db0929",
  "kind": "yes/no",
  "text": "Claim: In 1942, a blacklisted screenwriter won the same award that Sredni Vashtar was later nominated for. He shared the honor with the writer and director of the 1951 horror film When I Grow Up.\n\nPassages:\n\n[Michael Kanin]\nMichael Kanin (February 1, 1910 – March 12, 1993) was an American director, producer, playwright and screenwriter who shared an Academy Award with Ring Lardner Jr. in 1942 for writing the Katharine Hepburn-Spencer Tracy film comedy \"Woman of the Year\".\n\n[When I Grow Up (film)]\nWhen I Grow Up is a 1951 American drama film written and directed by Michael Kanin.\n\n[Ring Lardner Jr.]\nRinggold Wilmer \"Ring\" Lardner Jr. (August 19, 1915 – October 31, 2000) was an American journalist and screenwriter blacklisted by the Hollywood movie studios during the Red Scare of the late 1940s and 1950s.\n\n[Sredni Vashtar (film)]\nIt won the BAFTA award for Best Short Film, and was nominated for an Academy Award Oscar.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qe12c257a4b",
  "kind": "yes/no",
  "text": "Post: I get a lot of boy who cried wolf vibes from the Red Cross and their emergency blood shortages all the time",
  "question": "Is the author being sarcastic?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement."
 },
 {
  "qid": "q8ca0f776f4",
  "kind": "yes/no",
  "text": "Claim: The 1st Battle of Kharkov was named so by a German field army born in the year 1882.\n\nPassages:\n\n[First Battle of Kharkov]\nThe 1st Battle of Kharkov, so named by Wilhelm Keitel, was the 1941 tactical battle for the city of Kharkov (now \"Kharkiv\") (Ukrainian SSR) during the final phase of Operation \"Barbarossa\" between the German 6th Army of Army Group South and the Soviet Southwestern Front.\n\n[Wilhelm Keitel]\nWilhelm Keitel (22 September 1882 – 16 October 1946) was a German field marshal who served as Chief of the Armed Forces High Command (\"Oberkommando der Wehrmacht\" or OKW) in Nazi Germany during World War II.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q500b477d1f",
  "kind": "yes/no",
  "text": "Claim: Night's Dark Terror is an adventure module co-written by a British game designer. This game designer has contributed to the single-player role-playing gamebook, the series that Eye of the Dragon is part of.\n\nPassages:\n\n[Jim Bambra]\nHe is particularly known for his contributions to \"Dungeons and Dragons\", \"Fighting Fantasy\", \"Warhammer\", and \"\" which was based on the \"Star Wars\" films.\n\n[Eye of the Dragon]\nIt forms part of Steve Jackson and Ian Livingstone's Fighting Fantasy series.\n\n[Night's Dark Terror]\nNight's Dark Terror is an adventure module for the \"Dungeons & Dragons\" (\"D&D\") fantasy role-playing game written by British game designers Jim Bambra, Graeme Morris, and Phil Gallagher.\n\n[Fighting Fantasy]\nFighting Fantasy is a series of single-player role-playing gamebooks created by Steve Jackson and Ian Livingstone.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qeda47ca5ef",
  "kind": "yes/no",
  "text": "Post: this narrative of \"protection\" that women require is infantilising and off-base. it implies requiring smothering as opposed to freedom to occupy spaces, yknow, as people.",
  "question": "Is the tone of this text sarcastic?",
  "definitions": "- yes: the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 }
]
