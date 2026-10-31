# A46 replay label-noise blind read RSAS06-blind_read-ee5d083f-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/di_train/DI-LANG/a46/reads/answers/RSAS06-blind_read-ee5d083f-007.json

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
  "qid": "q63ee3f085a",
  "kind": "yes/no",
  "text": "Claim: A star of Hello! Stranger is the younger brother of the mixed martial artist of French nationality.\n\nPassages:\n\n[Denis Kang]\nDenis Kang (Hangul: 강대수 , born September 17, 1977) is a Canadian professional mixed martial artist who most recently competed in the Middleweight division.\n\n[Hello! Stranger]\nStranger () is a 2014 South Korean television program starring Kim Kwang-kyu, Julien Kang, Kangnam and Mina Fujii.\n\n[Julien Kang]\nHe is the younger brother of mixed martial artist Denis Kang.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q5d18417c25",
  "kind": "yes/no",
  "text": "Claim: The Trans-Karakoram Tract is recognized by India as part of the state of Jammu and Kashmir.\n\nPassages:\n\n[Trans-Karakoram Tract]\nThe Trans-Karakoram Tract (Hindi: शक्स्गम् , \"Shaksgam\"; also known as Shaksgam or the Shaksgam Tract, is an area of more than 9900 km² along both sides of the Shaksgam River and extending from the Karakoram to the Kunlun range.\n\n[Jammu and Kashmir]\nJammu and Kashmir ( ) is a state in northern India, often denoted by the acronym J&K.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q450f11a885",
  "kind": "yes/no",
  "text": "Claim: Eli Roth, famous for his role as Donny \"The Bear Jew\" Donowitz, wrote the 2012 film that was directed by the founder of Soul Temple Records.\n\nPassages:\n\n[Eli Roth]\nEli Raphael Roth (born April 18, 1972) is an American film director, producer, writer, and actor. As an actor, his most prominent role was as Donny \"The Bear Jew\" Donowitz in Quentin Tarantino's war film \"Inglourious Basterds\" for which he won both a SAG Award (Best Ensemble) and a BFCA Critic's Choice Award (Best Acting Ensemble).\n\n[The Man with the Iron Fists]\nThe Man with the Iron Fists is a 2012 American martial arts film directed by RZA and written by RZA and Eli Roth.\n\n[Soul Temple Records]\nSoul Temple Records is an American record label founded in 2012 by hip hop music recording artist RZA and Bob Perry, after the release of the RZA directed \"The Man with the Iron Fists\".",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qe0a4ce0091",
  "kind": "yes/no",
  "text": "Claim: All That is the show that the co-creator with the host of Vibe and Wild 'N Out had a debut on.\n\nPassages:\n\n[Vibe (talk show)]\nPremiering in August 1997, it was produced by Quincy Jones, hosted by Chris Spencer, and featured President Bill Clinton on its first episode.\n\n[Chris Spencer (actor)]\nChris is also one of the most sought after writers having done projects with Wayans family, Jamie Foxx, and was significant in helping Nick Cannon create MTV's \"Wild 'N Out\".\n\n[Nick Cannon]\nNicholas Scott \"Nick\" Cannon (born October 8, 1980) is an American rapper, actor, comedian, director, screenwriter, film producer, entrepreneur, record producer, radio and television personality. On television, Cannon began as a teenager on \"All That\" before going on to host \"The Nick Cannon Show\", \"Wild 'N Out\", and \"America's Got Talent\".",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qec601e138d",
  "kind": "yes/no",
  "text": "Claim: Israeli actress, Odeya Rush, is known for her lead role in 2015 American horror comedy film based on the children's book series created in 1984 by R.L. Stine.\n\nPassages:\n\n[Goosebumps (film)]\nGoosebumps is a 2015 American horror comedy film based on the children's book series of the same name by R.L. Stine.\n\n[Odeya Rush]\nOdeya Rush (Hebrew: אודיה רש‎ ‎ ; born Odeya Rushinek; May 12, 1997) is an Israeli actress and model. She is known for her lead roles in \"The Giver\" (2014) and \"Goosebumps\" (2015).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qf7f54f04a3",
  "kind": "yes/no",
  "text": "Claim: Kate Kung Foo practiced badminton. She practiced on Réunion in which Carl Hilsenberg collected plants.\n\nPassages:\n\n[Kate Foo Kune]\nShe began playing badminton in Mauritius at age six.\n\n[Carl Hilsenberg]\nCarl (or Karl) Theodor Hilsenberg (11 March 1802 – 11 September 1824) was a German naturalist, botanist and ornithologist, who collected plants in Madagascar and Mauritius.\n\n[Mauritius]\nMauritius ( or ; French: \"Maurice\" ), officially the Republic of Mauritius (French: \"République de Maurice\" ), is an island nation in the Indian Ocean about 2000 km off the southeast coast of the African continent.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows."
 },
 {
  "qid": "q5124fc3ccf",
  "kind": "yes/no",
  "text": "Claim: The club that played Manchester City in the 1972 FA Charity Shield was founded in 1874.\n\nPassages:\n\n[1972 FA Charity Shield]\nThe 1972 FA Charity Shield was contested between Manchester City and Aston Villa.\n\n[Aston Villa F.C.]\nFounded in 1874, they have played at their current home ground, Villa Park, since 1897.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qfe7279d0e7",
  "kind": "yes/no",
  "text": "Claim: This German-born philologist and Orientalist, who lived in Britain for most of his life. The philologist is considered one of the most important German scholars in Indian Philology alongside an Indologist who worked on the subject of Indology. The Indologist coined the term the National Institute of Science, Technology and Development.\n\nPassages:\n\n[Heinrich Zimmer]\nHe was the most important German scholar in Indian Philology after Max Müller (1823-1900).\n\n[Transtheism]\nTranstheism is a term coined by either philosopher Paul Tillich or Indologist Heinrich Zimmer referring to a system of thought or religious philosophy which is neither theistic, nor atheistic, but is beyond them.\n\n[Max Müller]\nFriedrich Max Müller (6 December 1823 – 28 October 1900), generally known as Max Müller, was a German-born philologist and Orientalist, who lived and studied in Britain for most of his life. Müller wrote both scholarly and popular works on the subject of Indology.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q8ad67bc574",
  "kind": "yes/no",
  "text": "Claim: Republican Dan Boren is a retired American politician who was a U. S. representative of Oklahoma's 2nd Congressional District whom Oklahoma politician Jim Wilson ran against during the July 27, 1992 Democratic primary.\n\nPassages:\n\n[Dan Boren]\nDaniel David Boren (born August 2, 1973) is a retired American politician, who served as the U.S. Representative for Oklahoma 's 2 congressional district from 2005 to 2013.\n\n[Jim Wilson (Oklahoma politician)]\nHe ran unsuccessfully against Democratic Incumbent US Rep. Dan Boren in Oklahoma's 2nd Congressional District in the July 27 Democratic primary.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q47a19ae30f",
  "kind": "yes/no",
  "text": "Claim: The head of the Imperial Family that was making a broadcast announcement of Japan's surrender in 1945 was the leader for whom Yoshihiro Tokugawa served as a personal advisor.\n\nPassages:\n\n[Masahiko Takeshita]\nIn August 1945, he helped plan a \"coup\" along with Major Kenji Hatanaka and a handful of others , with the intent of preventing the Emperor's announcement of Japan's surrender from being broadcast.\n\n[Yoshihiro Tokugawa]\nThe grandson of Tokugawa Yoshikatsu, the last lord of Owari han, he served as Grand Chamberlain of Japan from 1985 to 1988, serving as the Emperor of Japan's personal adviser.\n\n[Emperor of Japan]\nThe Emperor of Japan is the head of the Imperial Family and the traditional head of state of Japan.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qdd599ca375",
  "kind": "yes/no",
  "text": "Claim: The Peruvian poet and writer of Los heraldos negros was not a German national. Neither was the author of Tales of a Long Night.\n\nPassages:\n\n[Tales of a Long Night]\nTales of a Long Night (German: \"Hamlet oder Die lange Nacht nimmt ein Ende\" ) (1956) is the last novel of German author Alfred Döblin.\n\n[Alfred Döblin]\nBruno Alfred Döblin (10 August 1878 – 26 June 1957) was a German novelist, essayist, and doctor, best known for his novel \"Berlin Alexanderplatz\" (1929).\n\n[Los heraldos negros]\n\"Los heraldos negros\" is the title of a collection of poems written by the Peruvian poet César Vallejo between the years 1915 and 1918 and published in July 1919.\n\n[César Vallejo]\nCésar Abraham Vallejo Mendoza (March 16, 1892 – April 15, 1938) was a Peruvian poet, writer, playwright, and journalist.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qf87028a823",
  "kind": "yes/no",
  "text": "Post: I have more fun with my parents and boyfriend than anyone else. Is this old age?",
  "question": "Is this text written sarcastically?",
  "definitions": "- yes: the tone is mocking or ironic, and the intended meaning differs from the literal sentence.\n- no: the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe."
 },
 {
  "qid": "q790e0f7542",
  "kind": "yes/no",
  "text": "Claim: Iris (Song) was originally written for the soundtrack of a 1998 musical film. The lead female actress in the film began her acting career in 1981.\n\nPassages:\n\n[Iris (song)]\nOriginally written for the soundtrack of the 1998 film \"City of Angels\", the song was later included on the band's sixth album \"Dizzy Up the Girl\".\n\n[Meg Ryan]\nRyan began her acting career in 1981 in minor roles, before joining the cast of the CBS soap opera \"As the World Turns\" in 1982.\n\n[City of Angels (film)]\nCity of Angels is a 1998 American romantic fantasy film directed by Brad Silberling and starring Nicolas Cage and Meg Ryan.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q5d0b4f1135",
  "kind": "yes/no",
  "text": "Claim: The person who portrayed Dr. John Watson in Sherlock Holmes (2009 film) is an English actor that was born in 1972. He was part of the ensemble cast of the movie Scott Z, which Burns wrote that screenplay for.\n\nPassages:\n\n[Scott Z. Burns]\n\" (2009), and \"Contagion\" (2011), all of which feature Matt Damon.\n\n[Sherlock Holmes (2009 film)]\nRobert Downey Jr. and Jude Law portray Sherlock Holmes and Dr. John Watson respectively.\n\n[Jude Law]\nDavid Jude Heyworth Law (born 29 December 1972) is an English actor.\n\n[Contagion (film)]\nThe film features an ensemble cast that includes Marion Cotillard, Bryan Cranston, Matt Damon, Laurence Fishburne, Jude Law, Gwyneth Paltrow, Kate Winslet, and Jennifer Ehle.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1dfa1057e5",
  "kind": "yes/no",
  "text": "Claim: Buffalo Rock produced a drink under its own name. That drink and that which Steven Reinemund acquired, are not both artificially flavored soft drinks.\n\nPassages:\n\n[Buffalo Rock]\nIn addition to bottling Pepsi products, the company produced Grapico in 1981, a grape-flavored soft drink, and a ginger ale under its own brand name.\n\n[Grapico]\nGrapico is a caffeine-free, artificially flavored carbonated soft drink with a purple color and a grape taste that is sold in the Southeastern United States.\n\n[Steven Reinemund]\nHe led the acquisitions of several other food and beverage companies including Quaker Oats, Naked Juice, Izze and Stacy’s Chips.\n\n[Izze]\nIzze is an all-natural, no-preservatives-added fruit soda.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "q427b691bbf",
  "kind": "choice",
  "text": "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
  "question": "Pick the text in which the author is being sarcastic.",
  "options": [
   "My control key fell off my laptop and I cannot control my life",
   "The control button just fell off my laptop. How symbolic for my life."
  ]
 },
 {
  "qid": "qa16ee32e89",
  "kind": "yes/no",
  "text": "Claim: John Roger Kirkpatrick Scott was a member of the U.S. House of Representatives from a Commonwealth that borders New Jersey to the east.\n\nPassages:\n\n[Pennsylvania]\nPennsylvania (Pennsylvania German: \"Pennsylvaani\" or \"Pennsilfaani\"), officially the Commonwealth of Pennsylvania, is a state located in the northeastern and Mid-Atlantic regions of the United States. The Commonwealth borders Delaware to the southeast, Maryland to the south, West Virginia to the southwest, Ohio to the west, Lake Erie and the Canadian province of Ontario to the northwest, New York to the north, and New Jersey to the east.\n\n[John Roger Kirkpatrick Scott]\nJohn Roger Kirkpatrick Scott (July 6, 1873 – December 9, 1945) was a Republican member of the U.S. House of Representatives from Pennsylvania.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "qa4b13724a8",
  "kind": "yes/no",
  "text": "Claim: Patricia Jude Francis Kensit was the lead singer of Eighth Wonder and who was born on March, 4th in 1968.\n\nPassages:\n\n[Patsy Kensit]\nPatricia Jude Francis Kensit (born 4 March 1968) is a British actress, singer, model, and former child star.\n\n[Eighth Wonder]\nThe band were composed of singer (future model and actress) Patsy Kensit, her brother Jamie Kensit, Steve Grantley and Geoff Beauchamp.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qc200a5b534",
  "kind": "yes/no",
  "text": "Claim: Hormel Foods Corporation is the brand who makes canned meats that had its own cook off in Coahuila until 2007.\n\nPassages:\n\n[Spamarama]\nSpamarama (SPAMARAMA) was a long-time annual festival and competitive cookoff held in Austin, Texas from 1976 to 2007 in recognition of Spam.\n\n[Spam (food)]\nSpam (stylized SPAM) is a brand of canned cooked meat made by Hormel Foods Corporation.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q29e1c3c82d",
  "kind": "yes/no",
  "text": "Claim: A 2007 American-American comedy film was directed by an actor who graduated from Northwestern University. Lorna Gayle appeared in that film.\n\nPassages:\n\n[Lorna Gayle]\nLorna Gayle is a British actress, known for appearing in the films, \"Run Fatboy Run\" (2007), \"The Dark Knight\" (2008) and \"One Day\" (2011).\n\n[Run Fatboy Run]\nRun Fatboy Run is a 2007 British-American comedy film directed by David Schwimmer, written by Michael Ian Black and Simon Pegg, and starring Pegg, Dylan Moran, Thandie Newton, Harish Patel, India de Beaufort, and Hank Azaria.\n\n[David Schwimmer]\nDavid Lawrence Schwimmer (born November 2, 1966) is an American actor, director, and producer. In 1988, he graduated from Northwestern University with a Bachelor of Arts in theater and speech.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qad05a11d4f",
  "kind": "yes/no",
  "text": "Claim: This company was acquired by RBC and is where John G. Taft was employed. It was founded before the company Johann Berenberg was co-owner of from 1748.\n\nPassages:\n\n[Johann Berenberg]\nHe was a co-owner of Berenberg Bank from 1748, with his brother, senator Paul Berenberg, and after the latter's death in 1768 the sole owner.\n\n[Dain Rauscher Wessels]\nDain Rauscher Wessels was a brokerage and investment banking firm based in Minneapolis, Minnesota. The firm traced its origins to a number of smaller regional securities firms founded in the 1920s and 1930s.\n\n[Berenberg Bank]\nKG, commonly known as Berenberg Bank, is a Hamburg-based multinational investment banking and private banking company, founded by the Belgian-origined Berenberg family in 1590.\n\n[John G. Taft]\nHis unit at Dougherty was later acquired by Dain Rauscher, and Taft began working with Royal Bank of Canada (RBC) when it acquired Dain Rauscher in 2001.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q90851e835d",
  "kind": "yes/no",
  "text": "Claim: Alvarezsauroidea was named after a physicist who won the Nobel Prize in Physics in 1968.\n\nPassages:\n\n[Alvarezsauroidea]\nAlvarezsauroidea is a group of small maniraptoran dinosaurs. Alvarezsauroidea, Alvarezsauridae, and Alvarezsauria are named for the historian Don Gregorio Alvarez, not the more familiar physicist Luis Alvarez, who proposed that the Cretaceous–Paleogene extinction event was caused by an impact event.\n\n[Luis Walter Alvarez]\nLuis Walter Alvarez (June 13, 1911 – September 1, 1988) was an American experimental physicist, inventor, and professor who was awarded the Nobel Prize in Physics in 1968.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: when the claim is checked piece by piece against the passages, at least one piece fails."
 },
 {
  "qid": "q84cedaaaf7",
  "kind": "yes/no",
  "text": "Claim: The second extended play of the American singer and songriter best known as the clean vocalist in post-hardcore band, Dance Gavin Dance, was released on September 1, 2017 on Vital Records and failed to break the Billboard Top 200.\n\nPassages:\n\n[Tilian Pearson]\nHe is best known as the clean vocalist in post-hardcore band Dance Gavin Dance.\n\n[Patient EP]\nPatient is the second extended play (EP) by American singer and songwriter Tilian Pearson. It was released on September 1, 2017 on Vital Records.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "qc847128f00",
  "kind": "yes/no",
  "text": "Claim: Horror movie R-Point set in 1972 Vietnam was filmed in part in Bokor Hill Station.\n\nPassages:\n\n[Bokor Hill Station]\nIt was used as the location for the final showdown of the movie \"City of Ghosts\" (2002) and the 2004 film \"R-Point\".\n\n[R-Point]\nSet in 1972 Vietnam, during the Vietnam War, it stars Kam Woo-sung and Son Byong-ho as members of the South Korean military in Vietnam.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9868cf8132",
  "kind": "yes/no",
  "text": "Claim: Pak Sao is a technique in the martial art specializing in close range combat.\n\nPassages:\n\n[Wing Chun]\nWing Chun () is a traditional Southern Chinese martial art specializing in close range combat.\n\n[Pak Sao]\nIn Wing Chun martial arts, Pak Sao is a blocking technique similar to a parry used in boxing.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q122b91500b",
  "kind": "yes/no",
  "text": "Claim: Deep Pal is the cinematographer for the 1998 Indian romantic thriller film in the backdrop of insurgency in Northeast India, written and directed by Gulzar, and produced by Gulzar, Ram Gopal Varma, and Shekhar Kapur.\n\nPassages:\n\n[Deep Pal]\nDeep Pal (born April 16, 1953) is an Indian cinematographer. His later work included \"Bandit Queen\" directed by Shekhar Kapur and \"Dil Se.\n\n[Dil Se..]\nDil Se (translation: \"From the Heart)\" is a 1998 Indian romantic thriller film in the backdrop of insurgency in Northeast India, written and directed by Mani Ratnam, and produced by Mani Ratnam, Ram Gopal Varma, and Shekhar Kapur.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qa8eb9c26f2",
  "kind": "yes/no",
  "text": "Claim: According to this manuscript written in a language spoken between the 8th and 16th centuries Friso was a leader of a group of Frisian colonists who had been settled in the Sabah for well over a millennium when they were discovered by Alexander the Great.\n\nPassages:\n\n[Old Frisian]\nOld Frisian is a West Germanic language spoken between the 8th and 16th centuries in the area between the Rhine and Weser on the European North Sea coast.\n\n[Oera Linda Book]\nThe Oera Linda Book is a manuscript written in a form of Old Frisian, purporting to cover historical, mythological, and religious themes of remote antiquity, from 2194 BCE to 803 CE.\n\n[Friso]\nAccording to Martinus Hamconius in his 17th century chronicle \"Frisia seu de viris rebusque illustribus\", and also the 19th century Oera Linda Book, Friso was a leader of a group of Frisian colonists who had been settled in the Punjab for well over a millennium when they were discovered by Alexander the Great.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "qcd6bb742c6",
  "kind": "yes/no",
  "text": "Claim: The Czech player who was defeated by Johan Kriek in the 1982 Australian Open – Men's Singles and Albert Costa are both tennis players, and one of them, Costa, began playing at the age of five.\n\nPassages:\n\n[Albert Costa]\nCosta began playing tennis at the age of five.\n\n[Steve Denton]\nSteve Denton (born September 5, 1956, in Kingsville, Texas) is a former professional tennis player for the ATP Tour.\n\n[1982 Australian Open – Men's Singles]\nJohan Kriek was the defending champion, and successfully defended his title, defeating Steve Denton 6–3, 6–3, 6–2 in the final to win the Men's Singles title at the 1982 Australian Open, what was the rematch of the previous year.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q9c5c919a71",
  "kind": "yes/no",
  "text": "Claim: When the Macanese general election took place on the night of, September 17, 2017, the legislature was elected according to the provisions of the Basic Law of Macau.\n\nPassages:\n\n[Elections in Macau]\nMacau elects on national level a legislature.\n\n[Macanese legislative election, 2017]\nThe 2017 Macanese general election took place on 17 September 2017 according to the provisions of the Basic Law of Macau.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q5415b4837f",
  "kind": "yes/no",
  "text": "Claim: Francisco Rafael Arellano Félix was the eldest brother of the Mexican drug trafficker born 12 March 1952.\n\nPassages:\n\n[Francisco Rafael Arellano Félix]\nFrancisco Rafael Arellano Félix (24 October 1949 – 18 October 2013) was a Mexican drug lord and former leader of the Tijuana Cartel, a drug trafficking organization. He was the oldest of seven brothers and headed the criminal organization early in the 1990s alongside them. Through his brother Benjamín, Francisco Rafael joined the Tijuana Cartel in 1989 following the arrest of Miguel Ángel Félix Gallardo, one of the most prominent drug czars in Mexico during the 1980s.\n\n[Benjamín Arellano Félix]\nBenjamín Arellano Félix (born 12 March 1952) is a Mexican drug trafficker and former leader of the Mexican criminal organization known as the Tijuana Cartel or 'Arellano-Félix Organization'.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "q92d8ecab07",
  "kind": "yes/no",
  "text": "Claim: Nobel Laureate Vernon Smith teaches at Chapman University.\n\nPassages:\n\n[Vernon L. Smith]\nVernon Lomax Smith (born January 1, 1927) is an American professor of economics at Chapman University's Argyros School of Business and Economics and School of Law in Orange, California, formerly a research scholar at George Mason University Interdisciplinary Center for Economic Science, and a Fellow of the Mercatus Center, all in Arlington, Virginia.\n\n[Journal of Behavioral Finance]\nThe founding Board of Editors were Brian Bruce, David Dreman, Paul Slovic, Nobel Laureate Vernon Smith and Arnold Wood.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q3d640eec8a",
  "kind": "choice",
  "text": "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
  "question": "Which version is written sarcastically?",
  "options": [
   "a level tudor history can do one",
   "I want my a-level history course to be finished"
  ]
 },
 {
  "qid": "qc2c77d2328",
  "kind": "yes/no",
  "text": "Claim: Love at First Sting, released on 27 March 1984 as a boxed set, featured the heavy metal ballad that reached number 64 on \"Billboard\" Hot 100 in July 1984.\n\nPassages:\n\n[Still Loving You]\n\"Still Loving You\" is a heavy metal ballad by the German rock band Scorpions. It was released in July 1984 as the second single from their ninth studio album, \"Love at First Sting\" (1984). The song reached number 64 on \"Billboard\" Hot 100.\n\n[Love at First Sting]\nLove at First Sting is the ninth studio album by German hard rock band Scorpions. The album contains \"Rock You Like a Hurricane\", \"Still Loving You\", and \"Big City Nights\", three of the band's most famous songs.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q19e1e5a0a0",
  "kind": "yes/no",
  "text": "Claim: Amelie Simone Mauresmo has won more awards than the winner of the 2015 Family Circle Cup – Singles tournament.\n\nPassages:\n\n[2015 Family Circle Cup – Singles]\nAndrea Petkovic was the defending champion, but she lost to Angelique Kerber in the semifinals.\n\n[Amélie Mauresmo]\nAmélie Simone Mauresmo ] (born 5 July 1979) is a French former professional tennis player, and a former world No. 1. Mauresmo won two Grand Slam singles titles at the Australian Open and at Wimbledon, and also won a Silver Medal at the 2004 Summer Olympics.\n\n[Angelique Kerber]\nShe ascended to the top of the rankings on 12 September 2016, thus becoming the twenty-second and oldest player to achieve the number one ranking for the first time and the first new number one player since Victoria Azarenka in 2012.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the evidence establishes the whole claim as correct, including the connection between the entities it links.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "qc5e1c1565a",
  "kind": "yes/no",
  "text": "Claim: The Indianapolis 500 was designated a Grand Épreuve along with one of the oldest motor races in the world.\n\nPassages:\n\n[French Grand Prix]\nThe French Grand Prix (French: \"Grand Prix de France\" ), formerly known as the Grand Prix de l'ACF, is a race held as part of the Fédération Internationale de l'Automobile's annual Formula One automobile racing championships. It is one of the oldest motor races in the world.\n\n[1924 Grand Prix season]\nThe 1924 Grand Prix season again saw Grand Prix motor racing in Europe and North America. The Indianapolis 500 was again designated a Grand Épreuve by the International Sporting Commission of the AIACR, along with the French Grand Prix, held in Lyon and the Italian Grand Prix at Monza.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q7068261232",
  "kind": "yes/no",
  "text": "Claim: Park So-yeon was a members of a three piece girl group. So was the writer of the song that was the second single released from the group TLC, \"Hands Up\".\n\nPassages:\n\n[Hands Up (TLC song)]\nIt was written and produced by both Babyface and Daryl Simmons for the band's fourth studio album, \"3D\" (2002), and released as the album's second single following \"Girl Talk\" in the United States in November 2002.\n\n[Girl Talk (TLC song)]\nIt was written by band members Lisa Lopes and Tionne Watkins along with Anita McLoud, Edmund \"Eddie Hustle\" Clement, and Kandi Burruss for the group's fourth studio album, \"3D\" (2002).\n\n[Park So-yeon (singer)]\nShe is best known as the former main vocalist and member of South Korean girl group T-ara.\n\n[Tionne Watkins]\nBorn in Des Moines, Iowa, Watkins rose to fame in the early 1990s as a member of the girl-group TLC.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q3371483e5d",
  "kind": "yes/no",
  "text": "Claim: The Delgados are Arab. They are not the band who released \"Disappointed\".\n\nPassages:\n\n[Electronic (band)]\nElectronic were an English alternative dance supergroup formed by New Order singer and guitarist Bernard Sumner and ex-Smiths guitarist Johnny Marr.\n\n[The Delgados]\nThe Delgados were a Scottish indie rock band from Motherwell, North Lanarkshire.\n\n[Disappointed]\n\"Disappointed\" was the fourth single by the English band Electronic.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q120d26a260",
  "kind": "yes/no",
  "text": "Claim: Jude Law an Scousers actor that was born in 1972. He was part of the ensemble cast of the movie Scott Z. Burns wrote that screenplay for.\n\nPassages:\n\n[Contagion (film)]\nThe film features an ensemble cast that includes Marion Cotillard, Bryan Cranston, Matt Damon, Laurence Fishburne, Jude Law, Gwyneth Paltrow, Kate Winslet, and Jennifer Ehle.\n\n[Scott Z. Burns]\n\" (2009), and \"Contagion\" (2011), all of which feature Matt Damon.\n\n[Jude Law]\nDavid Jude Heyworth Law (born 29 December 1972) is an English actor.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q796531e489",
  "kind": "yes/no",
  "text": "Claim: The village and civil parish where Harold Temple White was born is in North East Lincolnshire, England. It is 1.75 miles from the place the River Freshney, according to folk lore, springs from.\n\nPassages:\n\n[River Freshney]\nIt rises from at least four springs on the edge of the Lincolnshire Wolds, although local folklore and oral tradition has it springing from Welbeck Hill.\n\n[Harold Temple White]\nHe was born in Laceby, Lincolnshire, England, in 1881, and resided in Wellington for much of his life.\n\n[Laceby]\nLaceby is a village and civil parish in North East Lincolnshire, England.\n\n[Welbeck Hill]\nWelbeck Hill is the site of Roman and early Saxon pottery finds, and an Anglo-Saxon cemetery, located around 1.75 miles from Laceby, and around 3 miles from Riby, in North East Lincolnshire, England.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 },
 {
  "qid": "qecf5765bc7",
  "kind": "yes/no",
  "text": "Claim: George Edward Entwistle (born 8 July 1962) was Director-General of the BBC from January to December 2012, succeeding Mark John Thompson, the current Chief Executive Officer (CEO) of The New York Times Company.\n\nPassages:\n\n[George Entwistle]\nGeorge Edward Entwistle (born 8 July 1962) was Director-General of the BBC during 2012, succeeding Mark Thompson.\n\n[Mark Thompson (media executive)]\nMark John Thompson (born 31 July 1957) is the current Chief Executive Officer (CEO) of The New York Times Company.",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages."
 },
 {
  "qid": "q64772f37ce",
  "kind": "yes/no",
  "text": "Claim: The follow-up to 2012's \"Transporter 2\" is the third film in a franchise that Camile Delamarre edited.\n\nPassages:\n\n[Camille Delamarre]\nHe edited films including \"Transporter 3\" and \"Taken 2 \", among others.\n\n[Transporter 3]\nTransporter 3 (French: Le Transporteur 3) is a 2008 French action film and the third installment in the \"Transporter\" franchise.\n\n[Transporter 2]\nIt is the sequel to \"The Transporter\" (2002), and is followed by \"Transporter 3\" (2008).",
  "question": "Using only the passages as evidence, does the whole claim hold?",
  "definitions": "- yes: every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.\n- no: the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence."
 },
 {
  "qid": "q76e95ba63d",
  "kind": "yes/no",
  "text": "Claim: The American star of Neal Dodson's \"Jonathan\", played a professional getaway driver in \"Baby Driver\".\n\nPassages:\n\n[Neal Dodson]\nNeal executive produced \"Another Cinderella Story\" staring Selena Gomez and Jane Lynch, \"Banshee Chapter\" starring Katia Winter, \"\"Hollidaysburg\"\" starring Rachel Keller, \"\"Jonathan\"\" starring Ansel Elgort, \"\"Love On A Limb\"\" starring Ashley Williams (actress) and Marilu Henner, \"Never Here\" starring Mireille Enos and Sam Shepard, and \"\"Periods\"\" as well as co-producing \"Hateship, Loveship\" starring Kristin Wiig.\n\n[Baby Driver]\nThe plot follows Baby, a young getaway driver and music lover who must work for a kingpin.\n\n[Ansel Elgort]\nAs a film actor, he played Tommy Ross in the horror film \"Carrie\" (2013), Caleb Prior in \"The Divergent Series \" franchise, Augustus Waters in the romantic teen drama \"The Fault in Our Stars\" (2014), and the title character in Edgar Wright's action thriller \"Baby Driver\" (2017).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "q11676d4b68",
  "kind": "yes/no",
  "text": "Claim: Innervision is a song from the studio album released on November 26, 2002 and is a cover of the Stevie Wonder song.\n\nPassages:\n\n[Innervision]\nThe song is from the \"Steal This Album!\n\n[Steal This Album!]\nis the third studio album by Armenian American rock band System of a Down, released on November 26, 2002, on American Recordings.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there."
 },
 {
  "qid": "q8d3765bbe6",
  "kind": "yes/no",
  "text": "Claim: The birthplace of Hou Yifan, and Jingdezhen both border the same town to the north.\n\nPassages:\n\n[Jingdezhen]\nJingdezhen (or the Town of Jingde) is a prefecture-level city, previously a town, in northeastern Jiangxi province, China, with a total population of 1,554,000 (2007), bordering Anhui to the north.\n\n[Hou Yifan]\nHou Yifan ( ) (born 27 February 1994, Xinghua, Jiangsu, China) is a Chinese chess grandmaster and former chess prodigy.\n\n[Xinghua, Jiangsu]\nXinghua () is a county-level city under the administration of Taizhou, Jiangsu province, China. It borders the prefecture-level cities of Yancheng to the north and east and Yangzhou to the west.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: a single wrong or unsupported detail is enough: the claim is then not fully supported."
 },
 {
  "qid": "q96d745ad20",
  "kind": "yes/no",
  "text": "Claim: The 1955 film that had a prequel called Davy Crockett and the River Pirates, and Herbie Rides Again were both by Walt Disney Productions.\n\nPassages:\n\n[Davy Crockett and the River Pirates]\nThis film acts as a prequel to 1955's \"Davy Crockett, King of the Wild Frontier\" and is an edited compilation of the fourth and fifth stories featuring the Disney television series \"Davy Crockett\":\n\n[Herbie Rides Again]\nHerbie Rides Again is a 1974 American comedy film and a sequel to \"The Love Bug,\" released six years earlier, and the second in a series of films made by Walt Disney Productions starring an anthropomorphic (and quite autonomous) 1963 Volkswagen racing Beetle named Herbie.\n\n[Davy Crockett, King of the Wild Frontier]\nDavy Crockett, King of the Wild Frontier is a 1955 live-action Walt Disney adventure film starring Fess Parker as Davy Crockett.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.\n- no: the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified."
 },
 {
  "qid": "qeb59ec0485",
  "kind": "yes/no",
  "text": "Claim: Say Yes is the 12th episode of the zombie horror series shown on AMC.\n\nPassages:\n\n[The Walking Dead (season 7)]\nThe seventh season of \"The Walking Dead\", an American post-apocalyptic horror television series on AMC, premiered on October 23, 2016, and concluded on April 2, 2017, consisting of 16 episodes.\n\n[Say Yes (The Walking Dead)]\n\"Say Yes\" is the twelfth episode of the seventh season and 95th episode overall of the post-apocalyptic horror television series \"The Walking Dead\", which aired on AMC on March 5, 2017.",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q1ee50eba18",
  "kind": "yes/no",
  "text": "Claim: The composer of Kamarinskaya is not the same nationality as another composer. This composer wrote the opera \"I puritani\"\n\nPassages:\n\n[Vincenzo Bellini]\nVincenzo Salvatore Carmelo Francesco Bellini (] ; 3 November 1801 – 23 September 1835) was an Italian opera composer, who was known for his long-flowing melodic lines for which he was named \"the Swan of Catania\".\n\n[I puritani]\nI puritani (\"The Puritans\") is an opera in by Vincenzo Bellini.\n\n[Kamarinskaya]\nKamarinskaya (Russian: камаринская ) is a Russian traditional folk dance, which is mostly known today as the Russian composer Mikhail Glinka's composition of the same name.\n\n[Mikhail Glinka]\nMikhail Ivanovich Glinka (Russian: Михаи́л Ива́нович Гли́нка ; 1 June [O.S. 20 May] 1804 15 February [O.S. 3 February] 1857 ) was the first Russian composer to gain wide recognition within his own country, and is often regarded as the fountainhead of Russian classical music.",
  "question": "Is every part of the claim backed up by the passages?",
  "definitions": "- yes: reading the passages together proves every statement inside the claim, with no part left unverified.\n- no: the passages leave part of the claim unproven, or show that part of it is false."
 },
 {
  "qid": "q17c5a3f16a",
  "kind": "yes/no",
  "text": "Claim: Bruce Darnell was a jury member for a German talent show Vanessa Krasniqi took part in. He was also an American model and choreographer born in 1950's.\n\nPassages:\n\n[Vanessa Krasniqi]\nShe rose to fame after taking part in the ninth season of the German talent show \"Deutschland sucht den Superstar\".\n\n[Bruce Darnell]\nBruce Darnell (born July 19, 1957) is an American model and choreographer based in Germany.\n\n[Deutschland sucht den Superstar (season 9)]\nJury members Fernanda Brandao and Patrick Nuo left DSDS and were replaced by Bruce Darnell and Cascada's Natalie Horler.",
  "question": "Do the passages together prove all of what the claim says?",
  "definitions": "- yes: all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qf2f8d44d8f",
  "kind": "yes/no",
  "text": "Claim: VEU, the American television channel owned by Golden West Broadcasting was similar to a defunct television servied owned by National Subscription Television.\n\nPassages:\n\n[VEU]\nVEU (Video Entertainment Unlimited) was an American subscription television channel owned by Golden West Broadcasting. The channel was similar to ONTV, another scrambled UHF service, and was carried by many stations including KAUT-TV in Oklahoma City, WVEU in Atlanta and KNBN in the Dallas/Fort Worth Metroplex.\n\n[ONTV (pay TV)]\nONTV (later known as ON Subscription Television from 1983 until its shutdown in 1985) is a defunct American subscription television service that was owned by National Subscription Television, a joint venture between Oak Industries (a manufacturer of satellite and pay television decoders and equipment), Chartwell Enterprises (owned by Norman Lear) and media executive A. Jerrold Perenchio.",
  "question": "Do the passages fully support the claim?",
  "definitions": "- yes: the claim contains nothing the passages fail to confirm, and every fact it combines is supported.\n- no: at least one part of the claim is contradicted by the passages, or is not confirmed by them."
 },
 {
  "qid": "qaa2df12a9c",
  "kind": "yes/no",
  "text": "Claim: The main character in the biographical war drama, which co-starred Spencer Lofranco, was an Olympic distance runner in the World War II.\n\nPassages:\n\n[Louis Zamperini]\nLouis Silvie \"Louie\" Zamperini (January 26, 1917 – July 2, 2014) was a US prisoner of war survivor in World War II, a Christian evangelist and an Olympic distance runner.\n\n[Unbroken (film)]\nThe film revolves around the life of USA Olympian and army officer Louis \"Louie\" Zamperini.\n\n[Spencer Lofranco]\nHe then co-starred as Harry Brooks in the biographical war drama \"Unbroken\" (2014) and Billy in the crime drama \"Dixieland\" (2015).",
  "question": "Can the claim be confirmed in full from the passages above?",
  "definitions": "- yes: the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.\n- no: the claim says something the passages do not back up, or says the opposite of what they state."
 }
]
